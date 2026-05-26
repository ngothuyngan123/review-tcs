# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "google-api-python-client",
#   "google-auth",
# ]
# ///
"""Fetch specific sheets from a Google Sheet using service account auth.

Usage:
  uv run scripts/fetch_sheet.py <spreadsheet_id> <sheet_name_1> [<sheet_name_2> ...]
"""
import sys
import io
import json
from pathlib import Path

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDS_PATH = Path(__file__).parent.parent / "credentials" / "google-service-account.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def main():
    if len(sys.argv) < 3:
        print("Usage: fetch_sheet.py <spreadsheet_id> <sheet_name> [<sheet_name> ...]")
        sys.exit(1)

    ss_id = sys.argv[1]
    sheet_names = sys.argv[2:]

    creds = service_account.Credentials.from_service_account_file(
        str(CREDS_PATH), scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=creds)

    # List all sheets first for verification
    meta = service.spreadsheets().get(spreadsheetId=ss_id).execute()
    all_sheets = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print(f"=== All sheets in file: {all_sheets}", file=sys.stderr)

    result = {}
    for name in sheet_names:
        if name not in all_sheets:
            print(f"WARN: sheet '{name}' not found. Available: {all_sheets}", file=sys.stderr)
            continue
        resp = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=ss_id, range=name)
            .execute()
        )
        result[name] = resp.get("values", [])

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
