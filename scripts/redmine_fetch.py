# -*- coding: utf-8 -*-
"""Fetch 1 issue Redmine qua REST API (API key), thay cho MCP redmine.

Dung cho /new-task BUOC 1. Doc `REDMINE_URL` + `REDMINE_API_KEY` truc tiep tu file
`.env` o root project (khong can export env vao shell truoc khi mo Claude Code).

  python scripts/redmine_fetch.py https://redmine.example.com/issues/36437
  python scripts/redmine_fetch.py 36437 --json out.json     # + dump JSON goc
  python scripts/redmine_fetch.py 36437 --no-journals       # bo journals cho nhe
  python scripts/redmine_fetch.py --check                   # test ket noi + API key
  python scripts/redmine_fetch.py 39446 --download-attachments MCP/<folder>/docs
                                                            # tai attachment tai lieu (/new-task-mcp)

stdout = digest markdown (metadata + description nguyen van + journals co notes),
du de auto-fill 01-bug-task.md / 03-dev-impact.md. --json ghi payload goc ra file.
--download-attachments chi tai file tai lieu (DOC_EXTS, bo anh/video); .zip giai nen
vao <DIR>/<ten zip>/. Danh sach file da luu in them o cuoi stdout.

Exit code: 0 OK - 2 thieu config/tham so - 3 URL sai - 4 loi HTTP - 5 khong ket noi duoc.
"""
import argparse
import io
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
SETUP_DOC = "docs/REDMINE-SETUP.md"
TIMEOUT = 30
DOWNLOAD_TIMEOUT = 120
ISSUE_URL_RE = re.compile(r"^(?P<base>https?://.+?)/issues/(?P<id>\d+)(?:[/?#].*)?$", re.I)
# Attachment duoc coi la tai lieu (docs MCP) - anh / video / log binary bo qua.
DOC_EXTS = (".md", ".markdown", ".html", ".htm", ".txt", ".pdf", ".json", ".yaml", ".yml",
            ".csv", ".xlsx", ".docx", ".zip")
ZIP_MAX_BYTES = 200 * 1024 * 1024  # tong dung luong giai nen toi da / 1 zip
UNSAFE_NAME_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def die(msg, code=1, hint=True):
    print(f"ERROR: {msg}", file=sys.stderr)
    if hint:
        print(f"Xem huong dan setup: {SETUP_DOC}", file=sys.stderr)
    sys.exit(code)


def load_env():
    """Env cua shell uu tien; thieu thi doc tu .env o root project."""
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    for k in ("REDMINE_URL", "REDMINE_API_KEY", "REDMINE_VERIFY_SSL"):
        if os.environ.get(k):
            env[k] = os.environ[k]
    return env


def resolve_target(arg, env):
    """(base_url, issue_id) tu arg (URL day du hoac so thuan) + env."""
    issue_id = None
    base = None
    if arg:
        arg = arg.strip().strip('"').strip("'")
        if arg.isdigit():
            issue_id = arg
        else:
            m = ISSUE_URL_RE.match(arg)
            if not m:
                die(f"URL khong hop le: {arg} - expect `<base>/issues/<so>` hoac so thuan.", 3, hint=False)
            base, issue_id = m.group("base"), m.group("id")
    if not base:
        base = (env.get("REDMINE_URL") or "").strip()
        if not base:
            die("Thieu REDMINE_URL (.env) va arg khong phai URL day du.", 2)
    return base.rstrip("/"), issue_id


def http_get(url, key, verify_ssl=True, accept="application/json", timeout=TIMEOUT):
    """GET 1 URL Redmine kem API key, tra ve bytes. Loi HTTP / mang -> die()."""
    req = urllib.request.Request(url, headers={
        "X-Redmine-API-Key": key,
        "Accept": accept,
        "User-Agent": "lme-review-TCs/redmine_fetch",
    })
    ctx = None
    if not verify_ssl:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        reason = {
            401: "API key sai hoac het han - lay lai key o Redmine: My account -> API access key.",
            403: "Khong co quyen xem issue nay (project private) hoac REST API bi tat tren Redmine.",
            404: "Issue khong ton tai, hoac REDMINE_URL sai (base URL phai la goc site, khong kem /projects/...).",
        }.get(e.code, "")
        die(f"HTTP {e.code} khi GET {url}. {reason}".strip(), 4)
    except urllib.error.URLError as e:
        host = urllib.parse.urlsplit(url).netloc or url
        die(f"Khong ket noi duoc {host}: {e.reason}. Verify REDMINE_URL / VPN / mang noi bo.", 5)


def api_get(base, path, params, key, verify_ssl=True):
    url = f"{base}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    raw = http_get(url, key, verify_ssl)
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        die(f"Response tu {url} khong phai JSON - co the URL tro vao trang login (API key sai / REST API tat).", 4)


def safe_name(name):
    """Ten file an toan tren Windows: bo thu muc, thay ky tu cam bang '_'."""
    name = UNSAFE_NAME_RE.sub("_", PurePosixPath(name.replace("\\", "/")).name).strip(" .")
    return name or "attachment"


def extract_zip(zip_path, dest):
    """Giai nen zip vao dest, bo entry tuyet doi / co '..' (path traversal). Tra ve list file."""
    out = []
    with zipfile.ZipFile(zip_path) as zf:
        members = [m for m in zf.infolist() if not m.is_dir()]
        total = sum(m.file_size for m in members)
        if total > ZIP_MAX_BYTES:
            print(f"  ! bo qua giai nen {zip_path.name}: {total} bytes > {ZIP_MAX_BYTES}", file=sys.stderr)
            return out
        root = dest.resolve()
        for m in members:
            parts = PurePosixPath(m.filename.replace("\\", "/")).parts
            if not parts or parts[0] in ("/", "") or ".." in parts or ":" in parts[0]:
                print(f"  ! bo qua entry khong an toan trong {zip_path.name}: {m.filename}", file=sys.stderr)
                continue
            target = root.joinpath(*[safe_name(p) for p in parts]).resolve()
            if root not in target.parents:
                print(f"  ! bo qua entry nam ngoai thu muc dich: {m.filename}", file=sys.stderr)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(m) as src:
                target.write_bytes(src.read())
            out.append(target)
    return out


def download_attachments(issue, out_dir, key, verify_ssl):
    """Tai attachment tai lieu (DOC_EXTS) ve out_dir. Trung ten: ban moi nhat giu ten goc,
    ban cu them tien to `<attachment_id>_`. Tra ve (saved, skipped)."""
    atts = issue.get("attachments") or []
    docs = [a for a in atts if Path(a.get("filename") or "").suffix.lower() in DOC_EXTS]
    skipped = [a.get("filename") for a in atts if a not in docs]
    newest = {}
    for a in docs:
        n = safe_name(a.get("filename") or "")
        if n not in newest or int(a.get("id") or 0) > int(newest[n].get("id") or 0):
            newest[n] = a
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for a in sorted(docs, key=lambda x: int(x.get("id") or 0)):
        n = safe_name(a.get("filename") or "")
        fname = n if newest[n] is a else f"{a.get('id')}_{n}"
        path = out_dir / fname
        path.write_bytes(http_get(a.get("content_url"), key, verify_ssl,
                                  accept="*/*", timeout=DOWNLOAD_TIMEOUT))
        saved.append(path)
        if path.suffix.lower() == ".zip":
            try:
                saved += extract_zip(path, out_dir / path.stem)
            except zipfile.BadZipFile:
                print(f"  ! {fname} khong phai zip hop le - giu nguyen file, khong giai nen", file=sys.stderr)
    return saved, skipped


def fmt_user(d, field):
    v = (d or {}).get(field) or {}
    return v.get("name", "") or "-"


def digest(issue, base, want_journals):
    out = []
    iid = issue.get("id")
    out.append(f"# Redmine #{iid} - {issue.get('subject', '').strip()}")
    out.append("")
    out.append(f"- URL: {base}/issues/{iid}")
    out.append(f"- Project: {fmt_user(issue, 'project')} | Tracker: {fmt_user(issue, 'tracker')} | "
               f"Status: {fmt_user(issue, 'status')} | Priority: {fmt_user(issue, 'priority')}")
    out.append(f"- Author: {fmt_user(issue, 'author')} | Assignee: {fmt_user(issue, 'assigned_to')}")
    out.append(f"- Created: {issue.get('created_on', '-')} | Updated: {issue.get('updated_on', '-')}")

    filled = [c for c in (issue.get("custom_fields") or []) if str(c.get("value") or "").strip()]
    if filled:
        out.append("- Custom fields: " + " | ".join(f"{c.get('name')}={c.get('value')}" for c in filled))

    atts = issue.get("attachments") or []
    out.append(f"- Attachments ({len(atts)}):" + ("" if atts else " -"))
    for a in atts:
        out.append(f"  - {a.get('filename')} ({a.get('filesize')} bytes) - {a.get('content_url')}")

    rels = issue.get("relations") or []
    if rels:
        out.append(f"- Relations ({len(rels)}): " + " | ".join(
            f"{r.get('relation_type')} #{r.get('issue_to_id') if r.get('issue_id') == iid else r.get('issue_id')}"
            for r in rels))

    out.append("")
    out.append("## Description (nguyen van)")
    out.append("")
    out.append((issue.get("description") or "").strip() or "_(trong)_")

    if want_journals:
        js = [j for j in (issue.get("journals") or []) if (j.get("notes") or "").strip()]
        out.append("")
        out.append(f"## Journals co notes ({len(js)})")
        for j in js:
            out.append("")
            out.append(f"**Journal #{j.get('id')} - {fmt_user(j, 'user')} - {(j.get('created_on') or '')[:10]}:**")
            out.append("")
            out.append("```")
            out.append((j.get("notes") or "").strip())
            out.append("```")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Fetch issue Redmine qua REST API (API key).")
    p.add_argument("target", nargs="?", help="Redmine issue URL (<base>/issues/<id>) hoac issue id thuan.")
    p.add_argument("--json", metavar="PATH", help="Dump JSON goc cua issue ra file.")
    p.add_argument("--no-journals", action="store_true", help="Khong fetch/in journals.")
    p.add_argument("--check", action="store_true", help="Test ket noi + API key (GET /users/current.json) roi thoat.")
    p.add_argument("--download-attachments", metavar="DIR",
                   help="Tai attachment tai lieu (" + " ".join(DOC_EXTS) + ") ve DIR; .zip giai nen vao DIR/<ten zip>/.")
    args = p.parse_args()

    env = load_env()
    key = (env.get("REDMINE_API_KEY") or "").strip()
    if not key or key == "your-api-key-here":
        die("Thieu REDMINE_API_KEY - dien vao .env o root project (copy tu .env.example).", 2)
    verify_ssl = (env.get("REDMINE_VERIFY_SSL", "1").strip().lower() not in ("0", "false", "no"))

    if args.check:
        base = (env.get("REDMINE_URL") or "").strip().rstrip("/")
        if args.target:
            base, _ = resolve_target(args.target, env)
        if not base:
            die("Thieu REDMINE_URL trong .env.", 2)
        me = api_get(base, "/users/current.json", None, key, verify_ssl).get("user", {})
        print(f"OK - {base} - dang nhap voi: {me.get('login')} "
              f"({me.get('firstname', '')} {me.get('lastname', '')})".replace(" )", ")"))
        return

    if not args.target:
        die("Thieu tham so. Cu phap: python scripts/redmine_fetch.py <redmine-url|issue-id>", 2, hint=False)

    base, issue_id = resolve_target(args.target, env)
    include = "attachments,relations" if args.no_journals else "journals,attachments,relations"
    data = api_get(base, f"/issues/{issue_id}.json", {"include": include}, key, verify_ssl)
    issue = data.get("issue")
    if not issue:
        die(f"Response khong co key `issue` - payload la: {list(data)[:5]}", 4, hint=False)

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[json] {out}", file=sys.stderr)

    print(digest(issue, base, not args.no_journals))

    if args.download_attachments:
        out_dir = Path(args.download_attachments)
        saved, skipped = download_attachments(issue, out_dir, key, verify_ssl)
        print("")
        print(f"## Attachments da tai ({len(saved)}) -> {out_dir.as_posix()}")
        for f in saved:
            try:
                rel = f.resolve().relative_to(out_dir.resolve()).as_posix()
            except ValueError:
                rel = f.as_posix()
            print(f"- {rel} ({f.stat().st_size} bytes)")
        if not saved:
            print("- (khong co attachment tai lieu nao)")
        if skipped:
            print(f"- Bo qua (khong phai tai lieu): {', '.join(skipped)}")


if __name__ == "__main__":
    main()
