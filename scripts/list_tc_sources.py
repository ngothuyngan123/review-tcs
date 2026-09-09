# -*- coding: utf-8 -*-
"""Liệt kê file + tab trong folder TCs trên Drive — BƯỚC 1 của /collect-tcs.

  python scripts/list_tc_sources.py                 # toàn bộ file + tab
  python scripts/list_tc_sources.py tag             # chỉ file/tab khớp keyword "tag"
  python scripts/list_tc_sources.py tag --json out.json

Lọc bỏ sẵn các tab KHÔNG phải test case (Info, ListBug, Q&A, Copy of *, ...).
Yêu cầu: credentials/google-service-account.json có quyền đọc folder.
"""
import sys, io, json, re, time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build

FOLDER_ID = "1eWgC1GnG6n8JvYGcBcbyPZLfDRiJLIKG"
CREDS = Path(__file__).parent.parent / "credentials" / "google-service-account.json"

# Tab KHÔNG phải test case — loại khỏi phạm vi gom
NOISE = re.compile(
    r"^(info|listbug|list bug|q&a|bug ui|bug logic|bugui|buglogic|bug comment|bugcomment|"
    r"draft|tmp|temp|readme|summary|test data)\s*$|^copy of |^bản sao của |"
    r"^(trang tính|sheet)\s*\d*\s*$", re.I)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keyword = args[0] if args else None
    out_path = None
    if "--json" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--json") + 1])

    creds = service_account.Credentials.from_service_account_file(
        str(CREDS), scopes=["https://www.googleapis.com/auth/drive.readonly",
                            "https://www.googleapis.com/auth/spreadsheets.readonly"])
    drive = build("drive", "v3", credentials=creds)
    sheets = build("sheets", "v4", credentials=creds)

    files, token = [], None
    while True:
        r = drive.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed=false",
            fields="nextPageToken,files(id,name,mimeType,modifiedTime,createdTime)",
            pageSize=200, pageToken=token,
            supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        files += r.get("files", [])
        token = r.get("nextPageToken")
        if not token:
            break
    files.sort(key=lambda f: f["modifiedTime"], reverse=True)

    # Khớp theo RANH GIỚI TỪ (cho phép hậu tố số nhiều "s"):
    #   - không có lookbehind  → "tag" khớp nhầm "sTAGing"
    #   - lookahead quá chặt   → "tag" bỏ sót tab "8.Tags"
    kw = re.compile(r"(?<![a-z0-9])" + re.escape(keyword) + r"s?(?![a-z0-9])",
                    re.I) if keyword else None
    result, n_file, n_tab, failed = {}, 0, 0, []

    kho_id = None
    kho_state = Path(__file__).parent.parent / "kho-tcs" / ".sheet-id"
    if kho_state.exists():
        kho_id = kho_state.read_text().strip()

    for f in files:
        if f["mimeType"] != "application/vnd.google-apps.spreadsheet":
            continue
        if kho_id and f["id"] == kho_id:
            continue  # bỏ qua chính file kho TCs tổng hợp (đích, không phải nguồn)
        # Sheets API hay trả 503 rải rác khi quét nhiều file → retry có backoff.
        meta, err = None, None
        for attempt in range(4):
            try:
                meta = sheets.spreadsheets().get(spreadsheetId=f["id"]).execute()
                break
            except Exception as e:
                err = e
                if attempt < 3:
                    time.sleep(1.5 * (attempt + 1))
        if meta is None:
            print(f"ERR (bỏ qua sau 4 lần thử) {f['name']}: {str(err)[:110]}", file=sys.stderr)
            failed.append(f["name"])
            continue

        tabs = []
        for s in meta.get("sheets", []):
            p = s["properties"]
            t = p["title"]
            if NOISE.search(t.strip()):
                continue
            tabs.append({"gid": p["sheetId"], "title": t,
                         "rows": p["gridProperties"].get("rowCount"),
                         "hidden": p.get("hidden", False)})

        file_hit = bool(kw and kw.search(f["name"]))
        hits = [t for t in tabs if (not kw) or file_hit or kw.search(t["title"])]
        if kw and not hits:
            continue

        result[f["name"]] = {"id": f["id"], "modified": f["modifiedTime"][:10],
                             "created": f["createdTime"][:10], "tabs": hits}
        n_file += 1
        n_tab += len(hits)
        print(f"\n{f['name']}   [mod {f['modifiedTime'][:10]}]   id={f['id']}")
        for t in hits:
            mark = " (tên file khớp keyword)" if file_hit and kw and not kw.search(t["title"]) else ""
            print(f"    gid={t['gid']:<12} {t['title']}  ({t['rows']}r)"
                  f"{' HIDDEN' if t['hidden'] else ''}{mark}")

    print(f"\n=== {n_file} file · {n_tab} tab"
          + (f' khớp "{keyword}"' if keyword else " (đã lọc tab không phải TC)"), file=sys.stderr)
    if failed:
        print(f"=== ⚠️ {len(failed)} file KHÔNG đọc được (Sheets API lỗi). PHẢI chạy lại "
              f"trước khi kết luận là đã quét hết nguồn: " + ", ".join(failed), file=sys.stderr)
    print("=== Bước tiếp: đọc tab Info của từng file để xác định NIÊN ĐẠI, "
          "rồi dùng scripts/fetch_grid.py để lấy grid (bung merged cell).", file=sys.stderr)

    if out_path:
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"-> {out_path}", file=sys.stderr)


main()
