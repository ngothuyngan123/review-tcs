# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-api-python-client",
#   "google-auth",
# ]
# ///
"""Push 04-tc-list.md from a review folder to a SPECIFIC TAB in a Google Sheet.

Usage:
  uv run scripts/push_tc.py <review-folder> [--config <path>]
                                             [--spreadsheet <url-with-gid>]

Reads:  <review-folder>/04-tc-list.md
Writes: APPEND to the tab pointed by `gid` in the spreadsheet URL.
        Each sync = 1 new block of (header + rows) appended below existing data.
        Does NOT create a new tab — user must pre-create the tab.

Target precedence (URL must include ?gid=<tab_id>):
  CLI --spreadsheet > HTML comment in 04-tc-list.md > config fallback
"""
import sys
import io
import json
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ROOT = Path(__file__).parent.parent
CREDS_PATH = ROOT / "credentials" / "google-service-account.json"
DEFAULT_CONFIG = ROOT / "scripts" / "sync-tc.config.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def die(msg: str, code: int = 1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


SPREADSHEET_URL_RE = re.compile(r"/d/([a-zA-Z0-9_-]+)")
GID_RE = re.compile(r"[?&#]gid=(\d+)")
SYNC_TARGET_RE = re.compile(r"<!--\s*sync-target:\s*(.+?)\s*-->")


def parse_url(value: str) -> dict:
    """Extract {spreadsheet_id, gid} from a Google Sheets URL or bare ID."""
    value = value.strip()
    ss_match = SPREADSHEET_URL_RE.search(value)
    spreadsheet_id = ss_match.group(1) if ss_match else value
    gid_match = GID_RE.search(value)
    gid = int(gid_match.group(1)) if gid_match else None
    return {"spreadsheet_id": spreadsheet_id, "gid": gid}


def parse_sync_target_comment(path: Path) -> dict:
    """Read first ~30 lines for `<!-- sync-target: <URL with gid> -->`.

    Accepts either:
      <!-- sync-target: https://docs.google.com/spreadsheets/d/<id>/edit?gid=<n> -->
      <!-- sync-target: spreadsheet=<URL or ID> [gid=<n>] -->
    Returns: {'spreadsheet_id': '<id>', 'gid': <int or None>}
    """
    if not path.exists():
        return {}
    out = {}
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= 30:
                break
            m = SYNC_TARGET_RE.search(line)
            if not m:
                continue
            payload = m.group(1).strip()
            if payload.startswith("http"):
                parsed = parse_url(payload)
                out["spreadsheet_id"] = parsed["spreadsheet_id"]
                if parsed["gid"] is not None:
                    out["gid"] = parsed["gid"]
                break
            for token in payload.split():
                if "=" not in token:
                    continue
                k, _, v = token.partition("=")
                k = k.strip().lower()
                v = v.strip()
                if k == "spreadsheet" and v:
                    parsed = parse_url(v)
                    out["spreadsheet_id"] = parsed["spreadsheet_id"]
                    if parsed["gid"] is not None and "gid" not in out:
                        out["gid"] = parsed["gid"]
                elif k == "gid" and v.isdigit():
                    out["gid"] = int(v)
            break
    return out


def parse_folder_name(folder: Path) -> dict:
    parts = folder.name.split("_", 2)
    if len(parts) >= 3:
        return {"date": parts[0], "bug_id": parts[1], "slug": parts[2]}
    return {"date": "", "bug_id": folder.name, "slug": ""}


def parse_tc_file(path: Path) -> dict:
    """Parse 04-tc-list.md → {meta: {...}, tcs: [{...}]}."""
    if not path.exists():
        die(f"Not found: {path}")
    text = path.read_text(encoding="utf-8")

    meta = {}
    tcs = []
    in_meta = False
    in_tc_table = False
    tc_headers = []

    for raw in text.split("\n"):
        line = raw.strip()

        if line.startswith("## Thông tin"):
            in_meta = True
            in_tc_table = False
            continue
        if in_meta and line == "---":
            in_meta = False
            continue
        if in_meta and line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] not in ("Trường", ""):
                key = cells[0].lower().replace(" ", "_").replace("/", "_")
                val = cells[1].strip("`").strip()
                if val.startswith("<") and val.endswith(">"):
                    val = ""
                meta[key] = val
            continue

        if line.startswith("| TC ID |"):
            tc_headers = [c.strip() for c in line.strip("|").split("|")]
            in_tc_table = True
            continue
        if in_tc_table and line.startswith("|---"):
            continue
        if in_tc_table and line.startswith("|"):
            cells = [c.strip().replace("<br>", "\n") for c in line.strip("|").split("|")]
            if len(cells) == len(tc_headers) and cells[0].startswith("TC"):
                row = dict(zip(tc_headers, cells))
                tcs.append({
                    "tc_id": row.get("TC ID", ""),
                    "title": row.get("Title", ""),
                    "environment": row.get("Environment", ""),
                    "precondition": row.get("Precondition", ""),
                    "steps": row.get("Steps", ""),
                    "expected": row.get("Expected", ""),
                    "priority": row.get("Priority", ""),
                    "type": row.get("Type", ""),
                    "map_to_impact": row.get("Map to Impact", ""),
                })
            continue
        if in_tc_table and not line.startswith("|"):
            in_tc_table = False

    return {"meta": meta, "tcs": tcs}


def find_tab_by_gid(service, ss_id: str, gid: int) -> dict:
    """Return {sheet_id, title} for tab matching gid, or die if not found."""
    meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
    for sheet in meta.get("sheets", []):
        props = sheet["properties"]
        if props.get("sheetId") == gid:
            return {"sheet_id": gid, "title": props["title"]}
    available = "\n".join(
        f"  - gid={s['properties']['sheetId']}  title={s['properties']['title']!r}"
        for s in meta.get("sheets", [])
    )
    die(
        f"No tab found with gid={gid} in spreadsheet {ss_id}.\n"
        f"Available tabs:\n{available}"
    )


def find_next_empty_row(service, ss_id: str, tab_title: str) -> int:
    """Return 1-indexed row number of first empty row after existing data in column A."""
    result = service.spreadsheets().values().get(
        spreadsheetId=ss_id,
        range=f"'{tab_title}'!A:A",
    ).execute()
    values = result.get("values", [])
    return len(values) + 1


def main():
    args = sys.argv[1:]
    if not args:
        die("Usage: push_tc.py <review-folder> [--config <path>] [--spreadsheet <url-with-gid>]")

    folder = Path(args[0])
    config_path = DEFAULT_CONFIG
    cli_spreadsheet = ""
    for i, a in enumerate(args):
        if a == "--config" and i + 1 < len(args):
            config_path = Path(args[i + 1])
        elif a == "--spreadsheet" and i + 1 < len(args):
            cli_spreadsheet = args[i + 1]
        elif a.startswith("--spreadsheet="):
            cli_spreadsheet = a.split("=", 1)[1]

    if not folder.is_dir():
        die(f"Not a directory: {folder}")
    if not config_path.exists():
        die(
            f"Config not found: {config_path}\n"
            f"  Copy scripts/sync-tc.config.example.json → {config_path.name}."
        )
    if not CREDS_PATH.exists():
        die(f"Credentials not found: {CREDS_PATH}\n  See docs/MCP-SETUP.md.")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    columns = config.get("columns") or []
    if not columns:
        die(f"No columns defined in {config_path}")

    tc_file = folder / "04-tc-list.md"
    parsed = parse_tc_file(tc_file)
    if not parsed["tcs"]:
        die(f"No TCs found in {tc_file}")

    # Resolve target: CLI > HTML comment > config fallback
    if cli_spreadsheet:
        target = parse_url(cli_spreadsheet)
        target_source = "CLI --spreadsheet"
    else:
        comment_target = parse_sync_target_comment(tc_file)
        if comment_target.get("spreadsheet_id"):
            target = {
                "spreadsheet_id": comment_target["spreadsheet_id"],
                "gid": comment_target.get("gid"),
            }
            target_source = "HTML comment in 04-tc-list.md"
        else:
            config_ss = config.get("spreadsheet_id", "").strip()
            if config_ss and not config_ss.startswith("REPLACE"):
                target = parse_url(config_ss)
                target_source = f"config ({config_path.name})"
            else:
                die(
                    "No target spreadsheet resolved.\n"
                    "  Provide URL with gid via --spreadsheet, or add\n"
                    "  <!-- sync-target: <URL with gid> --> at top of 04-tc-list.md."
                )

    ss_id = target["spreadsheet_id"]
    gid = target.get("gid")
    if gid is None:
        die(
            f"Target URL has no 'gid' (no tab specified).\n"
            f"  URL must include ?gid=<tab_id> pointing to the pre-created tab.\n"
            f"  Source: {target_source}"
        )

    folder_info = parse_folder_name(folder)
    print(
        f"Folder: {folder.name}\n"
        f"Bug ID: {folder_info['bug_id']} | Date: {folder_info['date']} | TCs: {len(parsed['tcs'])}\n"
        f"Target: spreadsheet={ss_id}  gid={gid}\n"
        f"  source: {target_source}",
        file=sys.stderr,
    )

    creds = service_account.Credentials.from_service_account_file(str(CREDS_PATH), scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    tab = find_tab_by_gid(service, ss_id, gid)
    tab_title = tab["title"]
    sheet_id = tab["sheet_id"]
    print(f"Resolved tab: '{tab_title}' (gid={sheet_id})", file=sys.stderr)

    start_row = find_next_empty_row(service, ss_id, tab_title)
    print(f"Next empty row: {start_row} → writing header at A{start_row}", file=sys.stderr)

    static_values = {
        "bug_id": folder_info["bug_id"],
        "date": folder_info["date"],
        "slug": folder_info["slug"],
        "tester": parsed["meta"].get("tester_viết_tcs", ""),
        "submit_date": parsed["meta"].get("ngày_submit", ""),
        "version": parsed["meta"].get("version_tcs", ""),
        "link_goc": parsed["meta"].get("link_tc_gốc_(nếu_có)", ""),
    }

    headers = [c["header"] for c in columns]
    rows = []
    for tc in parsed["tcs"]:
        row = []
        for col in columns:
            if col.get("empty"):
                row.append("")
            elif col.get("static"):
                row.append(static_values.get(col.get("source", ""), ""))
            else:
                row.append(tc.get(col.get("source", ""), ""))
        rows.append(row)

    service.spreadsheets().values().update(
        spreadsheetId=ss_id,
        range=f"'{tab_title}'!A{start_row}",
        valueInputOption="RAW",
        body={"values": [headers] + rows},
    ).execute()

    # Post-write formatting: freeze (only on first sync) + dropdown on the new block
    format_requests = []
    data_start_row = start_row + 1  # 1-indexed where TC data begins (after this block's header)
    data_end_row = data_start_row + len(rows) - 1

    if start_row == 1:
        format_requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 1},
                },
                "fields": "gridProperties.frozenRowCount",
            }
        })

    dropdown_cols = []
    for col_idx, col in enumerate(columns):
        if col.get("dropdown"):
            dropdown_cols.append(col["header"])
            format_requests.append({
                "setDataValidation": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": data_start_row - 1,
                        "endRowIndex": data_end_row + 200,
                        "startColumnIndex": col_idx,
                        "endColumnIndex": col_idx + 1,
                    },
                    "rule": {
                        "condition": {
                            "type": "ONE_OF_LIST",
                            "values": [{"userEnteredValue": v} for v in col["dropdown"]],
                        },
                        "showCustomUi": True,
                        "strict": True,
                    },
                }
            })

    if format_requests:
        service.spreadsheets().batchUpdate(
            spreadsheetId=ss_id,
            body={"requests": format_requests},
        ).execute()

    print(f"OK: appended {len(rows)} TCs to tab '{tab_title}' starting at row {start_row} (1 header + {len(rows)} data rows)")
    if dropdown_cols:
        print(f"     Applied dropdown on: {', '.join(dropdown_cols)} (rows {data_start_row}-{data_end_row + 200})")
    print(f"URL: https://docs.google.com/spreadsheets/d/{ss_id}/edit?gid={sheet_id}")


if __name__ == "__main__":
    main()
