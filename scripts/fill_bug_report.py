# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-api-python-client",
#   "google-auth",
# ]
# ///
# -*- coding: utf-8 -*-
"""Ghi (fill) nội dung vào 1 cột của sheet "エルメ- Report BUG" theo từng dòng.

Dùng bởi skill /giai-trinh-bug để ghi draft giải trình vào cột "Test report"
của tab tháng (`YYYY.MM`). Cột target + cột khóa được xác định **THEO TÊN HEADER**
(vị trí cột đổi theo từng tháng), KHÔNG theo chữ cái cố định.

Input là file JSON các entry — mỗi entry = 1 ô cần ghi:

    [
      {"row": 2, "text": "1. Hiện tượng: ...", "match": "#41837"},
      ...
    ]

  - row   : số dòng **1-indexed** trên sheet (dòng 1 = header). BẮT BUỘC.
  - text  : nội dung ghi vào ô cột target. BẮT BUỘC.
  - match : (tùy chọn) chuỗi con PHẢI xuất hiện trong ô cột khóa (mặc định
            "ID redmine") ở ĐÚNG dòng đó. Dùng để chống lệch dòng giữa lúc đọc
            (fetch_grid) và lúc ghi: không khớp → BỎ QUA entry + báo, KHÔNG ghi.

Usage:
  python scripts/fill_bug_report.py <spreadsheet_id|url> "<tab>" <entries.json>
      [--col "Test report"] [--key "ID redmine"] [--dry-run] [--overwrite]

Mặc định AN TOÀN:
  - CHỈ ghi ô **trống / placeholder** (placeholder = chỉ còn khung
    "1. Hiện tượng: ... 2. Tại sao không test ra: ... 3. Biện pháp khắc phục:"
    không có nội dung thật).
  - Ô đã có nội dung THẬT (người viết) → BỎ QUA + báo, trừ khi có --overwrite.
  - --dry-run: chỉ IN kế hoạch, KHÔNG ghi gì.
"""
import sys
import io
import re
import json
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

# Nhãn khung Test report / Dev report — gỡ hết ra khi xét ô có phải placeholder.
PLACEHOLDER_LABELS = [
    "hiện tượng", "tại sao không test ra", "biện pháp khắc phục",
    "trường hợp lỗi", "nguyên nhân", "cách fix", "triển khai ngang",
    "action tránh lặp",
]


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def col_letter(idx0: int) -> str:
    """0-based column index -> A1 column letter (0->A, 26->AA)."""
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


def is_placeholder(val: str) -> bool:
    """True nếu ô rỗng hoặc chỉ còn khung nhãn (không có nội dung thật)."""
    low = (val or "").lower()
    for lab in PLACEHOLDER_LABELS:
        low = low.replace(lab, "")
    # còn lại chỉ số thứ tự / dấu câu / khoảng trắng -> placeholder
    return re.sub(r"[\d\.\:\-\)\(•\*\s　]", "", low) == ""


def find_tab_title(service, ss_id: str, sheet_name: str) -> str:
    meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
    titles = [s["properties"]["title"] for s in meta.get("sheets", [])]
    if sheet_name in titles:
        return sheet_name
    for t in titles:
        if t.strip().lower() == sheet_name.strip().lower():
            return t
    die(f"Không tìm thấy tab '{sheet_name}'. Các tab hiện có: {titles}")


def find_col(headers: list, needles: list, what: str) -> int:
    low = [str(h).strip().lower() for h in headers]
    for needle in needles:
        for i, h in enumerate(low):
            if needle in h:
                return i
    die(f"Không tìm thấy cột {what} (thử: {needles}) trong header: {headers}")


def client_email() -> str:
    try:
        return json.loads(CREDS_PATH.read_text(encoding="utf-8")).get("client_email", "<không đọc được>")
    except Exception:
        return "<không đọc được client_email>"


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        die('Usage: fill_bug_report.py <ssid|url> "<tab>" <entries.json> '
            '[--col "Test report"] [--key "ID redmine"] [--dry-run] [--overwrite]')

    ss_id = extract_spreadsheet_id(args[0])
    tab_arg = args[1]
    entries_path = Path(args[2])

    col_name = "Test report"
    key_name = "ID redmine"
    dry_run = False
    overwrite = False
    i = 3
    while i < len(args):
        a = args[i]
        if a == "--col" and i + 1 < len(args):
            col_name = args[i + 1]; i += 2; continue
        if a == "--key" and i + 1 < len(args):
            key_name = args[i + 1]; i += 2; continue
        if a == "--dry-run":
            dry_run = True; i += 1; continue
        if a == "--overwrite":
            overwrite = True; i += 1; continue
        i += 1

    if not CREDS_PATH.exists():
        die(f"Credentials not found: {CREDS_PATH}\n  See docs/MCP-SETUP.md.")
    if not entries_path.exists():
        die(f"Không thấy file entries: {entries_path}")

    entries = json.loads(entries_path.read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        die("entries.json phải là list không rỗng các {row, text, match?}.")

    creds = service_account.Credentials.from_service_account_file(str(CREDS_PATH), scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    try:
        tab = find_tab_title(service, ss_id, tab_arg)

        hdr = service.spreadsheets().values().get(
            spreadsheetId=ss_id, range=f"'{tab}'!1:1",
        ).execute().get("values", [[]])
        headers = hdr[0] if hdr else []
        if not headers:
            die(f"Tab '{tab}' không có dòng header (dòng 1 trống).")

        col_idx = find_col(headers, [col_name.strip().lower()], f"target '{col_name}'")
        key_idx = find_col(
            headers,
            [key_name.strip().lower(), "id redmine", "link redmine", "redmine"],
            f"khóa '{key_name}'",
        )
        col_l = col_letter(col_idx)
        key_l = col_letter(key_idx)

        max_row = max(int(e["row"]) for e in entries)
        cur_target = service.spreadsheets().values().get(
            spreadsheetId=ss_id, range=f"'{tab}'!{col_l}1:{col_l}{max_row}",
        ).execute().get("values", [])
        cur_key = service.spreadsheets().values().get(
            spreadsheetId=ss_id, range=f"'{tab}'!{key_l}1:{key_l}{max_row}",
        ).execute().get("values", [])

        def cell(vals, row1):
            idx = row1 - 1
            if 0 <= idx < len(vals) and vals[idx]:
                return vals[idx][0] if vals[idx] else ""
            return ""

        to_write = []   # (row, text)
        plan = []       # (row, action, reason, key_preview, text_preview)
        for e in entries:
            row = int(e["row"])
            text = str(e.get("text", ""))
            match = e.get("match")
            kcell = cell(cur_key, row)
            tcell = cell(cur_target, row)
            kprev = (kcell[:42] + "…") if len(kcell) > 42 else kcell

            if row <= 1:
                plan.append((row, "SKIP", f"row {row} là header/không hợp lệ", kprev, "")); continue
            if not text.strip():
                plan.append((row, "SKIP", "text rỗng", kprev, "")); continue
            if match and match.strip().lower() not in kcell.lower():
                plan.append((row, "SKIP", f"LỆCH DÒNG: cột khóa không chứa '{match}'", kprev, "")); continue
            if tcell.strip() and not is_placeholder(tcell) and not overwrite:
                plan.append((row, "SKIP", "ô đã có nội dung người viết (dùng --overwrite để đè)", kprev, "")); continue

            to_write.append((row, text))
            plan.append((row, "WRITE", "", kprev, text.replace("\n", " ⏎ ")[:70]))

        # In kế hoạch
        print(f"Target: spreadsheet={ss_id}  tab='{tab}'  col='{headers[col_idx]}' ({col_l})  key='{headers[key_idx]}' ({key_l})",
              file=sys.stderr)
        print(f"{'row':>4} | {'action':6} | key | text/lý do", file=sys.stderr)
        for row, action, reason, kprev, tprev in plan:
            info = reason if action == "SKIP" else tprev
            print(f"{row:>4} | {action:6} | {kprev} | {info}", file=sys.stderr)

        n_write = len(to_write)
        n_skip = len(plan) - n_write
        if dry_run:
            print(f"\n[DRY-RUN] Sẽ ghi {n_write} ô, bỏ qua {n_skip}. KHÔNG ghi gì (bỏ --dry-run để ghi thật).")
            return
        if not to_write:
            print(f"Không có ô nào để ghi (bỏ qua {n_skip}). Không gọi API ghi.")
            return

        data = [
            {"range": f"'{tab}'!{col_l}{row}", "values": [[text]]}
            for row, text in to_write
        ]
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=ss_id,
            body={"valueInputOption": "RAW", "data": data},
        ).execute()

    except HttpError as e:
        if "PERMISSION_DENIED" in str(e) or getattr(e, "resp", None) and e.resp.status == 403:
            die(
                "403 Permission denied — Sheet 'エルメ- Report BUG' chưa share quyền Editor cho service account.\n"
                f"  Mở Sheet → Share → thêm email (Editor):\n    {client_email()}\n"
                "  (Chỉ cần quyền Editor trên đúng file này.)"
            )
        die(f"Sheets API error: {e}")

    print(f"OK: đã ghi {n_write} ô vào cột '{headers[col_idx]}' ({col_l}) của tab '{tab}', bỏ qua {n_skip}.")
    print(f"URL: https://docs.google.com/spreadsheets/d/{ss_id}/edit")


if __name__ == "__main__":
    main()
