# -*- coding: utf-8 -*-
"""Sinh index tra nhanh cho 2 file quan diem nang nhat cua framework/.

    framework/checklist-lme.md  (574 dong, ~23k token)  -> checklist-lme.index.md
    framework/catalog-lme.md    (375 dong, ~14k token)  -> catalog-lme.index.md

Muc dich: /review-tc va /write-tc chi can doc INDEX de chon quan diem Trigger khop
task, roi `sed -n '<Dong>p'` doc chi tiet cua vai chuc ma da chon — thay vi nap toan
van 2 file goc moi lan chay.

    python scripts/build_indexes.py            # sinh / ghi de 2 file index
    python scripts/build_indexes.py --verify   # so index tren dia voi ban sinh moi
                                               # exit 1 neu lech (dung cho pre-commit)

2 file index la OUTPUT — KHONG sua tay. Nguon su that van la 2 file goc.
"""
import argparse
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
CHECKLIST = ROOT / "framework" / "checklist-lme.md"
CATALOG = ROOT / "framework" / "catalog-lme.md"
CHECKLIST_IDX = ROOT / "framework" / "checklist-lme.index.md"
CATALOG_IDX = ROOT / "framework" / "catalog-lme.index.md"

BANNER = ("<!-- AUTO-GENERATED bởi scripts/build_indexes.py từ %s — KHÔNG sửa tay. "
          "Sửa file gốc rồi chạy lại script. -->")

VP_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d{3}\b")
VP_HEAD_RE = re.compile(r"^#### `([^`]+)`\s*(★?)\s*—\s*(.*)$")
VP_META_RE = re.compile(r"^(?P<name>.*?)\s*·\s*\*\*(?P<prio>[^*]+)\*\*(?P<rest>.*)$")
GROUP_RE = re.compile(r"^### (\d+\.\d+ .*)$")
CAT_BLOCK_RE = re.compile(r"^## (Catalog [A-Z0-9]+)\s*—\s*(.*)$")
CAT_SUB_RE = re.compile(r"^### (?:`([A-Z]+-\d+)`\s*)?(.*)$")
ROW_ID_RE = re.compile(r"^\|\s*\*{0,2}([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*)\*{0,2}\s*\|")
SEP_ROW_RE = re.compile(r"^\|[\s:|-]+$")


def cell(s, limit=0):
    """Chuan hoa 1 doan text cho o bang markdown."""
    s = re.sub(r"\s+", " ", (s or "")).strip().replace("|", "\\|")
    if limit and len(s) > limit:
        s = s[:limit - 1].rstrip() + "…"
    return s


def block_end(lines, start, stops=("#### ", "### ", "## ", "---")):
    """Dong cuoi (co noi dung) cua block bat dau tai index `start`."""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if any(lines[j].startswith(s) for s in stops):
            end = j
            break
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    return end


# --------------------------------------------------------------------------- #
# checklist-lme.md - 80 quan diem
# --------------------------------------------------------------------------- #
def parse_viewpoints(lines):
    heads = [i for i, l in enumerate(lines) if l.startswith("#### `")]
    out = []
    for i in heads:
        m = VP_HEAD_RE.match(lines[i])
        if not m:
            print("[!] Heading la, bo qua dong %d: %s" % (i + 1, lines[i][:80]), file=sys.stderr)
            continue
        code, star, rest = m.group(1), m.group(2), m.group(3)

        mm = VP_META_RE.match(rest)
        if mm:
            name, prio, tail = mm.group("name"), mm.group("prio"), mm.group("rest")
        else:                                    # khong co phan **uu tien**
            name, prio, tail = rest, "?", ""
        cat, cond = "—", tail
        if "· Catalog" in tail:
            cond, cat = tail.split("· Catalog", 1)
        cond = cond.strip(" ·()")

        end = block_end(lines, i)
        trig = ""
        for b in lines[i + 1:end]:
            if b.startswith("- **Trigger**:"):
                trig = b.split(":", 1)[1]
                break
        if trig:
            # Dieu kien nang uu tien o heading ("(→ Cao khi ...)") quyet dinh
            # BLOCKER vs MAJOR o BUOC 3b -> phai giu lai o cot Uu tien.
            if cond:
                prio = "%s (%s)" % (prio, cond)
        else:                                    # 5 quan diem ghi dieu kien ngay o heading
            trig = cond or "(xem phần Kiểm tra)"

        grp = ""
        for j in range(i, -1, -1):
            g = GROUP_RE.match(lines[j])
            if g:
                grp = g.group(1)
                break

        out.append({
            "code": code, "star": bool(star), "name": name, "prio": prio,
            "base": (mm.group("prio").strip() if mm else "?").split("→")[0].strip(),
            "cat": cat, "trigger": trig, "group": grp,
            "lines": "%d,%d" % (i + 1, end),
        })
    return out


def render_checklist_index(vps, rule_range):
    o = [BANNER % "framework/checklist-lme.md", "",
         "# Index quan điểm test LME — tầng 1 (%d quan điểm)" % len(vps), "",
         "> Bảng tra nhanh cho **BƯỚC 3b** của `/review-tc` và `/write-tc`.",
         "> Chọn quan điểm có **Trigger khớp task** ở bảng dưới, rồi đọc chi tiết "
         "(`Kiểm tra` + `Evidence`) **chỉ của các mã đã chọn**:",
         ">",
         "> ```",
         "> sed -n '<Dòng>p' framework/checklist-lme.md",
         "> ```",
         ">",
         "> **KHÔNG nạp toàn văn** [checklist-lme.md](checklist-lme.md) (574 dòng ≈ 23k token).",
         "> Nguồn sự thật vẫn là file gốc — file này là output tự sinh.",
         ">",
         "> **12 RULE bắt buộc** — đọc đủ, rẻ: `sed -n '%sp' framework/checklist-lme.md`."
         % rule_range,
         "> **§4 \"Quan điểm chưa đủ bằng chứng\"** (FORM-01, CHAT-01, ADM-01/03/04, TPL-01) "
         "KHÔNG có trong bảng này — theo **RULE-11** chỉ được nêu ở mức `[NIT]`.", "",
         "| Mã | Ưu tiên | Catalog | Nhóm | Trigger | Dòng |", "|---|---|---|---|---|---|"]
    for v in vps:
        o.append("| `%s`%s | %s | %s | %s | %s | %s |" % (
            v["code"], " ★" if v["star"] else "", cell(v["prio"]), cell(v["cat"]),
            cell(v["group"]), cell(v["trigger"]), v["lines"]))

    tally = {}
    for v in vps:                                # gom theo uu tien NEN, bo dieu kien nang
        tally[cell(v["base"])] = tally.get(cell(v["base"]), 0) + 1
    o += ["", "## Phân bố theo ưu tiên nền", "",
          "> Đếm theo mức **nền**. `(→ Cao khi ...)` / `→ BẮT BUỘC (nâng Cao)` ở cột `Ưu tiên` là"
          " **điều kiện nâng lên Cao** — khớp điều kiện thì xử lý như quan điểm ưu tiên Cao"
          " (thiếu TC = `[BLOCKER]`, và RULE-01 bắt buộc đủ 3 loại case).", "",
          "| Ưu tiên nền | Số quan điểm |", "|---|---|"]
    o += ["| %s | %d |" % (k, n) for k, n in sorted(tally.items(), key=lambda x: (-x[1], x[0]))]
    o.append("")
    return "\n".join(o)


# --------------------------------------------------------------------------- #
# catalog-lme.md - muc catalog + tra nguoc quan diem -> catalog
# --------------------------------------------------------------------------- #
def parse_catalog(lines):
    blocks, entries = [], []
    cur_block, cur_sub = "", ""
    for i, l in enumerate(lines):
        mb = CAT_BLOCK_RE.match(l)
        if mb:
            cur_block, cur_sub = mb.group(1), ""
            blocks.append({"name": cur_block, "title": mb.group(2),
                           "start": i + 1, "end": block_end(lines, i, ("## ",))})
            continue
        if l.startswith("### "):
            ms = CAT_SUB_RE.match(l)
            eid, title = (ms.group(1) or ""), ms.group(2)
            cur_sub = title
            if eid:                              # Catalog A: ### `DI-01` Text (1 dong)
                end = block_end(lines, i)
                vps = []
                for b in lines[i + 1:end]:
                    if b.startswith("- **Quan điểm**"):
                        vps = VP_RE.findall(b)
                entries.append({"id": eid, "block": cur_block, "name": title,
                                "vps": vps, "lines": "%d,%d" % (i + 1, end)})
            continue
        mr = ROW_ID_RE.match(l)
        if mr and cur_block:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= set("-: "):
                continue
            # bo dong TIEU DE bang (dong ke tiep la dong ngan cach |---|---|)
            if i + 1 < len(lines) and SEP_ROW_RE.match(lines[i + 1]):
                continue
            name = re.sub(r"\*\*", "", cells[1])
            entries.append({"id": mr.group(1),
                            "block": cur_block + (" / " + cur_sub if cur_sub else ""),
                            "name": name, "vps": VP_RE.findall(cells[-1]),
                            "lines": str(i + 1)})
    return blocks, entries


def render_catalog_index(blocks, entries):
    o = [BANNER % "framework/catalog-lme.md", "",
         "# Index catalog LME — tầng 2 (%d mục)" % len(entries), "",
         "> Dùng sau khi đã chọn quan điểm ở [checklist-lme.index.md](checklist-lme.index.md).",
         "> **Tick ◯ một quan điểm ở tầng 1 → BẮT BUỘC mở đúng mục catalog tương ứng ở đây.** "
         "Bỏ bước hai là chỗ bug lọt.",
         ">",
         "> ```",
         "> sed -n '<Dòng>p' framework/catalog-lme.md",
         "> ```",
         ">",
         "> **KHÔNG nạp toàn văn** [catalog-lme.md](catalog-lme.md) (375 dòng ≈ 14k token).", "",
         "## 1. Khối catalog", "",
         "| Khối | Nội dung | Dòng |", "|---|---|---|"]
    for b in blocks:
        o.append("| **%s** | %s | %d,%d |" % (b["name"], cell(b["title"]), b["start"], b["end"]))

    rev = {}
    for e in entries:
        for v in e["vps"]:
            rev.setdefault(v, []).append(e)
    o += ["", "## 2. Tra ngược — quan điểm ◯ thì phải mở mục catalog nào", "",
          "| Quan điểm | Mục catalog phải mở | Dòng |", "|---|---|---|"]
    for v in sorted(rev):
        ee = rev[v]
        head, more = ee[:8], len(ee) - 8
        o.append("| `%s` | %s | %s |" % (
            v,
            cell(" · ".join("%s (%s)" % (e["id"], e["name"]) for e in head)
                 + (" …+%d mục" % more if more > 0 else "")),
            cell(" · ".join(e["lines"] for e in head))))

    o += ["", "## 3. Toàn bộ mục catalog", "",
          "| ID | Khối | Tên | Quan điểm liên kết | Dòng |", "|---|---|---|---|---|"]
    for e in entries:
        o.append("| `%s` | %s | %s | %s | %s |" % (
            e["id"], cell(e["block"]), cell(e["name"], 70),
            cell(", ".join("`%s`" % v for v in e["vps"])) or "—", e["lines"]))
    o.append("")
    return "\n".join(o)


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true",
                    help="so index tren dia voi ban sinh moi, exit 1 neu lech")
    a = ap.parse_args()

    for f in (CHECKLIST, CATALOG):
        if not f.exists():
            sys.exit("[X] Khong tim thay %s" % f)

    cl = CHECKLIST.read_text(encoding="utf-8").splitlines()
    ct = CATALOG.read_text(encoding="utf-8").splitlines()

    rule_start = next((i + 1 for i, l in enumerate(cl) if l.startswith("## 1. 12 RULE")), 0)
    rule_end = block_end(cl, rule_start - 1, ("## ", "---")) if rule_start else 0

    vps = parse_viewpoints(cl)
    blocks, entries = parse_catalog(ct)
    docs = {
        CHECKLIST_IDX: render_checklist_index(vps, "%d,%d" % (rule_start, rule_end)),
        CATALOG_IDX: render_catalog_index(blocks, entries),
    }

    stale = []
    for path, text in docs.items():
        cur = path.read_text(encoding="utf-8") if path.exists() else None
        if a.verify:
            if cur != text:
                stale.append(path)
        elif cur != text:
            path.write_text(text, encoding="utf-8")
            print("[OK] ghi %s (%d dong)" % (path.relative_to(ROOT), text.count("\n") + 1))
        else:
            print("[--] %s da dung, khong doi" % path.relative_to(ROOT))

    print("Quan diem: %d | Khoi catalog: %d | Muc catalog: %d"
          % (len(vps), len(blocks), len(entries)), file=sys.stderr)

    if a.verify:
        if stale:
            for p in stale:
                print("[X] LECH: %s — chay `python scripts/build_indexes.py` de sinh lai"
                      % p.relative_to(ROOT), file=sys.stderr)
            sys.exit(1)
        print("[OK] 2 file index khop voi file goc.")


if __name__ == "__main__":
    main()
