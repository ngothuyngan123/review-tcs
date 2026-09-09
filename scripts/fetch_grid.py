# -*- coding: utf-8 -*-
"""Fetch tab values + merge ranges, expand merged cells so every row is self-contained.

Usage: python scripts/fetch_grid.py <ssid> <out.json> [tab ...]
"""
import sys, io, json
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS = Path(__file__).parent.parent / "credentials" / "google-service-account.json"
creds = service_account.Credentials.from_service_account_file(str(CREDS), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
svc = build("sheets", "v4", credentials=creds)

HELP = """Ví dụ:
  python scripts/fetch_grid.py 17izrWjE... out.json "Improve tag t2/2025"
  (bỏ tên tab = lấy TOÀN BỘ tab)

Script bung merged cell bằng sheets.merges — BẮT BUỘC dùng cho file TCs cũ có cấu
trúc cây Main Function / Sub1..Sub5, vì values.get thuần trả ô rỗng ở các ô gộp và
làm SAI phân cấp (TC bị gán nhầm nhóm cha).

Tìm spreadsheet_id + tên tab: python scripts/list_tc_sources.py <keyword>"""

if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
    print(__doc__)
    print(HELP)
    sys.exit(0)

ssid, out = sys.argv[1], Path(sys.argv[2])
want = sys.argv[3:]

meta = svc.spreadsheets().get(spreadsheetId=ssid, fields="properties.title,sheets.properties,sheets.merges").execute()
res = {"_file": meta["properties"]["title"], "_id": ssid, "sheets": {}}
for s in meta["sheets"]:
    tab = s["properties"]["title"]
    if want and tab not in want:
        continue
    vals = svc.spreadsheets().values().get(spreadsheetId=ssid, range=f"'{tab}'").execute().get("values", [])
    rows = [[(c or "").strip() for c in r] for r in vals]
    while rows and not any(rows[-1]): rows.pop()
    ncol = max((len(r) for r in rows), default=0)
    for r in rows: r += [""] * (ncol - len(r))
    merges = s.get("merges", [])
    n = 0
    for m in merges:
        r0, r1 = m.get("startRowIndex", 0), m.get("endRowIndex", 0)
        c0, c1 = m.get("startColumnIndex", 0), m.get("endColumnIndex", 0)
        if r0 >= len(rows): continue
        v = rows[r0][c0] if c0 < ncol else ""
        if not v: continue
        for ri in range(r0, min(r1, len(rows))):
            for ci in range(c0, min(c1, ncol)):
                if not rows[ri][ci]:
                    rows[ri][ci] = v; n += 1
    res["sheets"][tab] = rows
    print(f"  {tab}: {len(rows)}r x {ncol}c, {len(merges)} merges, {n} cells filled", file=sys.stderr)
out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"-> {out}", file=sys.stderr)
