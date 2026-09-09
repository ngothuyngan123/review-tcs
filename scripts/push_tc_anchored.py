# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-api-python-client",
#   "google-auth",
# ]
# ///
"""Push TCs vào sheet TC human/master, bắt đầu tại cột ANCHOR ("Main Function").

Khác với scripts/push_tc.py (ghi từ cột A vào tab AI pre-create), script này:
  - Ghi 5 cột: TC ID, Title, Precondition, Steps, Expected
  - Ghi vào 5 cột LIÊN TIẾP bắt đầu ĐÚNG tại cột header "Main Function"
  - APPEND xuống dưới row cuối cùng có data (đo theo cột anchor)
  - KHÔNG ghi header (sheet human đã có header sẵn)
  - Nguồn TC: 04-tc-list.md (--source 04) hoặc 05-review-report.md §5 (--source 05)

Usage:
  uv run scripts/push_tc_anchored.py <review-folder> --source 04|05
                                     [--url <Google Sheet URL>]
                                     [--sheet <tên tab>]
                                     [--anchor "Main Function"]
                                     [--row <1-indexed start row>]

  --row: ép ghi bắt đầu tại row cụ thể (bỏ qua auto-detect last-data-row). Dùng khi
         cột anchor "Main Function" chỉ có data ở dòng đầu mỗi block (merged-style),
         khiến auto-detect đếm sai và có nguy cơ đè data cũ.

Target precedence (url + sheet tab name):
  CLI --url/--sheet  >  HTML comment `<!-- sync-tcs: ... -->` trong 04-tc-list.md
"""
import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path(__file__).parent.parent
CREDS_PATH = ROOT / "credentials" / "google-service-account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_URL_RE = re.compile(r"/d/([a-zA-Z0-9_-]+)")
SYNC_TCS_RE = re.compile(r"<!--\s*sync-tcs:\s*(.+?)\s*-->", re.DOTALL)
DEFAULT_ANCHOR = "Main Function"


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def col_letter(idx0: int) -> str:
    """0-based column index → A1 column letter (0→A, 26→AA)."""
    s = ""
    n = idx0 + 1
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def extract_spreadsheet_id(value: str) -> str:
    value = value.strip()
    m = SPREADSHEET_URL_RE.search(value)
    return m.group(1) if m else value


def parse_sync_tcs_comment(path: Path) -> dict:
    """Đọc `<!-- sync-tcs: url=<URL> | sheet=<tab> | anchor=<col> -->` trong file 04.

    Trả về {'url': ..., 'sheet': ..., 'anchor': ...} (chỉ key có giá trị).
    """
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    m = SYNC_TCS_RE.search(text)
    if not m:
        return {}
    payload = m.group(1).strip()
    out = {}
    for token in payload.split("|"):
        if "=" not in token:
            continue
        k, _, v = token.partition("=")
        k, v = k.strip().lower(), v.strip()
        if not v or (v.startswith("<") and v.endswith(">")):
            continue
        if k in ("url", "sheet", "anchor"):
            out[k] = v
    return out


# ---------- Markdown TC table parsing ----------

def _split_row(line: str) -> list:
    return [c.strip().replace("<br>", "\n") for c in line.strip().strip("|").split("|")]


def _match_idx(headers: list, *needles: str):
    """Trả về index cột đầu tiên mà header (lower) chứa 1 trong các needle."""
    low = [h.lower() for h in headers]
    for needle in needles:
        for i, h in enumerate(low):
            if needle in h:
                return i
    return None


def _is_placeholder(val: str) -> bool:
    v = val.strip()
    return not v or (v.startswith("<") and v.endswith(">"))


def parse_md_table(lines: list, start_idx: int = 0, stop_heading_prefix: str = None) -> list:
    """Parse bảng TC markdown đầu tiên (từ start_idx). Map 5 field theo tên header.

    Trả về list dict {tc_id, title, precondition, steps, expected}.
    """
    headers = None
    fmap = {}
    tcs = []
    in_table = False
    for raw in lines[start_idx:]:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stop_heading_prefix and stripped.startswith(stop_heading_prefix) and in_table:
            break
        if not stripped.startswith("|"):
            if in_table:
                break  # bảng kết thúc
            continue
        cells = _split_row(stripped)
        if set(cells) <= {"", "-", "---", ":--", "--:", ":-:"} or all(
            set(c) <= {"-", ":", " "} for c in cells if c
        ):
            continue  # dòng separator |---|
        if headers is None:
            # dòng header: phải chứa cột TC No./TC ID + Tiêu đề/Title.
            # Match cả header VN (format canonical sheet "7. Ví dụ test case")
            # lẫn header EN (format cũ của các task trước 2026-07-16).
            # "tc no"/"tc id" = 16 cột canonical & format cũ; "id" = 12 cột kho
            # (§5 report từ 2026-08-27). "id" để CUỐI vì "evidence" cũng chứa "id".
            tc_i = _match_idx(cells, "tc no", "tc id", "tc", "id")
            title_i = _match_idx(cells, "tiêu đề", "title", "tên case")
            if tc_i is None or title_i is None:
                continue
            headers = cells
            fmap = {
                "tc_id": tc_i,
                "title": title_i,
                "precondition": _match_idx(
                    cells, "điều kiện tiền đề", "tiền điều kiện", "tiền đề",
                    "precondition", "precon",
                ),  # 12 cột kho dùng "Tiền điều kiện"
                "steps": _match_idx(cells, "các bước", "bước thực hiện", "steps", "step"),
                # "mong đợi" phải đứng trước "kết quả" để không dính "Kết quả thực thi"
                "expected": _match_idx(cells, "kết quả mong đợi", "mong đợi", "expected"),
            }
            in_table = True
            continue
        # data row
        def cell(key):
            i = fmap.get(key)
            return cells[i] if i is not None and i < len(cells) else ""
        tc_id = cell("tc_id")
        title = cell("title")
        if _is_placeholder(tc_id) and _is_placeholder(title):
            continue  # dòng template trống
        if _is_placeholder(title) and _is_placeholder(cell("steps")):
            continue
        tcs.append({
            "tc_id": tc_id,
            "title": title,
            "precondition": cell("precondition"),
            "steps": cell("steps"),
            "expected": cell("expected"),
        })
    return tcs


def parse_source_04(path: Path) -> list:
    if not path.exists():
        die(f"Not found: {path}")
    lines = path.read_text(encoding="utf-8").split("\n")
    return parse_md_table(lines)


def parse_source_05(path: Path) -> list:
    """Parse bảng §5 'TCs đề xuất bổ sung' trong 05-review-report.md."""
    if not path.exists():
        die(f"Not found: {path}")
    lines = path.read_text(encoding="utf-8").split("\n")
    sec_idx = None
    for i, raw in enumerate(lines):
        s = raw.strip()
        if s.startswith("## 5") or (s.startswith("##") and "đề xuất bổ sung" in s.lower()):
            sec_idx = i + 1
            break
    if sec_idx is None:
        die("Không tìm thấy section '## 5. TCs đề xuất bổ sung' trong 05-review-report.md")
    return parse_md_table(lines, start_idx=sec_idx, stop_heading_prefix="## ")


# ---------- Sheets helpers ----------

def find_tab_title(service, ss_id: str, sheet_name: str) -> str:
    meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
    titles = [s["properties"]["title"] for s in meta.get("sheets", [])]
    if sheet_name in titles:
        return sheet_name
    for t in titles:
        if t.strip().lower() == sheet_name.strip().lower():
            return t
    die(
        f"Không tìm thấy tab tên '{sheet_name}' trong spreadsheet {ss_id}.\n"
        f"  Các tab hiện có: {titles}"
    )


def find_anchor_col(service, ss_id: str, tab: str, anchor: str) -> tuple:
    """Quét ~15 dòng đầu, tìm ô header == anchor. Trả về (header_row_1idx, col_idx_0based)."""
    resp = service.spreadsheets().values().get(
        spreadsheetId=ss_id, range=f"'{tab}'!A1:ZZ15",
    ).execute()
    rows = resp.get("values", [])
    anchor_low = anchor.strip().lower()
    for r_idx, row in enumerate(rows):
        for c_idx, cell in enumerate(row):
            if str(cell).strip().lower() == anchor_low:
                return r_idx + 1, c_idx
    preview = "\n".join(f"  row {i+1}: {row}" for i, row in enumerate(rows[:5]))
    die(
        f"Không tìm thấy cột header '{anchor}' trong 15 dòng đầu của tab '{tab}'.\n"
        f"  5 dòng đầu:\n{preview}\n"
        f"  Kiểm tra tên cột anchor (--anchor) hoặc header sheet."
    )


def find_last_data_row(service, ss_id: str, tab: str, col_idx0: int) -> int:
    """Row cuối có data, đo theo cột anchor. Trả về row 1-indexed của ô trống kế tiếp."""
    letter = col_letter(col_idx0)
    resp = service.spreadsheets().values().get(
        spreadsheetId=ss_id, range=f"'{tab}'!{letter}1:{letter}",
    ).execute()
    values = resp.get("values", [])
    return len(values) + 1


# ---------- Main ----------

def main():
    args = sys.argv[1:]
    if not args:
        die("Usage: push_tc_anchored.py <review-folder> --source 04|05 [--url <URL>] [--sheet <tab>] [--anchor <col>]")

    folder = Path(args[0])
    source = None
    cli_url = cli_sheet = cli_anchor = ""
    cli_row = None
    i = 1
    while i < len(args):
        a = args[i]
        if a == "--source" and i + 1 < len(args):
            source = args[i + 1]; i += 2; continue
        if a == "--url" and i + 1 < len(args):
            cli_url = args[i + 1]; i += 2; continue
        if a == "--sheet" and i + 1 < len(args):
            cli_sheet = args[i + 1]; i += 2; continue
        if a == "--anchor" and i + 1 < len(args):
            cli_anchor = args[i + 1]; i += 2; continue
        if a == "--row" and i + 1 < len(args):
            try:
                cli_row = int(args[i + 1])
            except ValueError:
                die(f"--row phải là số nguyên (1-indexed), nhận: {args[i + 1]!r}")
            if cli_row < 1:
                die("--row phải >= 1.")
            i += 2; continue
        i += 1

    if source not in ("04", "05"):
        die("--source bắt buộc là '04' hoặc '05'.")
    if not folder.is_dir():
        die(f"Not a directory: {folder}")
    if not CREDS_PATH.exists():
        die(f"Credentials not found: {CREDS_PATH}\n  See docs/MCP-SETUP.md.")

    tc_file_04 = folder / "04-tc-list.md"

    # Resolve target: CLI > config block trong 04-tc-list.md
    cfg = parse_sync_tcs_comment(tc_file_04)
    url = cli_url or cfg.get("url", "")
    sheet_name = cli_sheet or cfg.get("sheet", "")
    anchor = cli_anchor or cfg.get("anchor", "") or DEFAULT_ANCHOR

    if not url:
        die(
            "Thiếu target URL Sheet TC human.\n"
            "  Thêm config vào 04-tc-list.md:\n"
            "  <!-- sync-tcs: url=<Google Sheet URL> | sheet=<tên tab> | anchor=Main Function -->\n"
            "  hoặc truyền --url <URL> --sheet <tab>."
        )
    if not sheet_name:
        die("Thiếu tên tab (--sheet hoặc 'sheet=' trong config sync-tcs).")

    ss_id = extract_spreadsheet_id(url)

    # Parse TCs theo source
    if source == "04":
        tcs = parse_source_04(tc_file_04)
        src_label = "04-tc-list.md (TC do AI viết)"
    else:
        tcs = parse_source_05(folder / "05-review-report.md")
        src_label = "05-review-report.md §5 (TC bổ sung reviewer)"

    if not tcs:
        die(f"Không có TC nào parse được từ {src_label}.")

    print(
        f"Folder: {folder.name}\n"
        f"Source: {src_label} → {len(tcs)} TC\n"
        f"Target: spreadsheet={ss_id}  sheet='{sheet_name}'  anchor='{anchor}'",
        file=sys.stderr,
    )

    try:
        creds = service_account.Credentials.from_service_account_file(str(CREDS_PATH), scopes=SCOPES)
        service = build("sheets", "v4", credentials=creds)

        tab = find_tab_title(service, ss_id, sheet_name)
        header_row, anchor_col = find_anchor_col(service, ss_id, tab, anchor)
        if cli_row is not None:
            start_row = cli_row
            if start_row <= header_row:
                die(f"--row {start_row} nằm ở/ trên header row {header_row} — sẽ đè header. Chọn row > {header_row}.")
            print(f"[--row] Ép ghi bắt đầu tại row {start_row} (bỏ qua auto-detect).", file=sys.stderr)
        else:
            start_row = find_last_data_row(service, ss_id, tab, anchor_col)
            if start_row <= header_row:
                start_row = header_row + 1

        start_letter = col_letter(anchor_col)
        end_letter = col_letter(anchor_col + 4)
        print(
            f"Resolved tab: '{tab}' | anchor '{anchor}' tại cột {start_letter} (header row {header_row})\n"
            f"Row trống kế tiếp: {start_row} → ghi {start_letter}{start_row}:{end_letter}",
            file=sys.stderr,
        )

        rows = [
            [tc["tc_id"], tc["title"], tc["precondition"], tc["steps"], tc["expected"]]
            for tc in tcs
        ]

        service.spreadsheets().values().update(
            spreadsheetId=ss_id,
            range=f"'{tab}'!{start_letter}{start_row}",
            valueInputOption="RAW",
            body={"values": rows},
        ).execute()
    except HttpError as e:
        if "PERMISSION_DENIED" in str(e) or e.resp.status == 403:
            die(
                "403 Permission denied — Sheet chưa share quyền Editor cho service account.\n"
                "  Mở Sheet → Share → paste client_email từ credentials/google-service-account.json (Editor)."
            )
        die(f"Sheets API error: {e}")

    end_row = start_row + len(rows) - 1
    print(
        f"OK: ghi {len(rows)} TC vào tab '{tab}' "
        f"cột {start_letter}:{end_letter}, row {start_row}-{end_row}"
    )
    print(f"URL: https://docs.google.com/spreadsheets/d/{ss_id}/edit")


if __name__ == "__main__":
    main()
