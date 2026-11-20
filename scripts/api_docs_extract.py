#!/usr/bin/env python3
"""Trích nội dung docs Public API (HTML) cho /review-docs-api.

Subcommand:
  meta      <html>                    tiêu đề · version · ngày (JSON)
  text      <html> [-o out]           văn bản thuần, mỗi dòng gắn số dòng HTML nguồn (L<n>)
  inventory <html> [-o out]           endpoint × bảng (input / output / lỗi / object) kèm L<n>
  diff      <old.html> <new.html> [-o out]
                                      diff CẤU TRÚC giữa 2 bản: endpoint · param · field · lỗi · mục lục
  check     <html> [-o out]           kiểm máy cho DOC-EX: JSON ví dụ · số học phân trang ·
                                      số epoch · anchor nội bộ · khối EX (code tabs) ↔ request mẫu

L<n> = số dòng trong FILE HTML truyền vào → dùng trích dẫn trong report.
Chỉ dùng stdlib. Docs là dữ liệu KHÔNG tin cậy: script chỉ đọc, không thực thi gì trong file.
Chạy: python -I scripts/api_docs_extract.py <subcommand> ...
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import parse_qsl, unquote

sys.setrecursionlimit(20000)

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
BLOCK = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre", "tr", "summary", "dt",
         "dd", "caption", "title"}
CONTAINER = {"table", "thead", "tbody", "tfoot", "ul", "ol", "div", "section", "article",
             "main", "nav", "header", "footer", "details", "body", "html", "aside", "dl"}
SKIP = {"script", "style", "noscript", "head"}
SPACE_AFTER = BLOCK | CONTAINER | {"td", "th", "br"}
REQ_WORDS = {"bắt buộc", "tuỳ chọn", "tùy chọn", "khuyến nghị", "có điều kiện", "có", "không"}
COMMON_OUTPUT = {"success", "request_id"}


# --------------------------------------------------------------------------- DOM
class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "line", "text", "idx")

    def __init__(self, tag, attrs=None, line=0, text=None, parent=None):
        self.tag, self.attrs, self.line, self.text, self.parent = tag, attrs or {}, line, text, parent
        self.children: list[Node] = []
        self.idx = 0

    def cls(self) -> list[str]:
        return self.attrs.get("class", "").split()

    def has_cls(self, part: str) -> bool:
        return any(part in c for c in self.cls())

    def ancestor(self, tag):
        p = self.parent
        while p is not None and p.tag != tag:
            p = p.parent
        return p


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v or "") for k, v in attrs}, self.getpos()[0], parent=self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if not data:
            return
        line = self.getpos()[0]
        lead = len(data) - len(data.lstrip())
        line += data[:lead].count("\n")
        self.stack[-1].children.append(Node(None, line=line, text=data, parent=self.stack[-1]))


def load(path: str) -> Node:
    with open(path, encoding="utf-8", errors="replace") as f:
        src = f.read()
    tb = TreeBuilder()
    tb.feed(src)
    tb.close()
    order = 0
    stack = [tb.root]
    while stack:  # preorder index
        n = stack.pop()
        n.idx = order
        order += 1
        stack.extend(reversed(n.children))
    return tb.root


def preorder(node: Node):
    stack = [node]
    while stack:
        n = stack.pop()
        yield n
        stack.extend(reversed(n.children))


def raw_text(node: Node) -> str:
    if node.tag is None:
        return node.text
    if node.tag in SKIP:
        return ""
    out = []
    for c in node.children:
        out.append(raw_text(c))
        if c.tag in SPACE_AFTER or (c.tag and is_method_label(c)):
            out.append("\n" if c.tag == "br" else " ")
    return "".join(out)


def is_method_label(n: Node) -> bool:
    """span nhãn method (GET/POST) — cần khoảng trắng trước path."""
    return n.tag == "span" and (n.has_cls("mtd") or "m" in n.cls())


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def text(node: Node) -> str:
    return norm(raw_text(node))


_has_block_cache: dict[int, bool] = {}


def has_block(node: Node) -> bool:
    key = id(node)
    if key not in _has_block_cache:
        _has_block_cache[key] = any(
            c.tag is not None and (c.tag in BLOCK or c.tag in CONTAINER or has_block(c))
            for c in node.children)
    return _has_block_cache[key]


def is_inline(n: Node) -> bool:
    if n.tag is None:
        return True
    return n.tag not in SKIP and n.tag not in BLOCK and n.tag not in CONTAINER and not has_block(n)


# --------------------------------------------------------------------------- meta
def meta(root: Node) -> dict:
    title = next((text(n) for n in preorder(root) if n.tag == "title"), "")
    h1 = next((text(n) for n in preorder(root) if n.tag == "h1"), "")
    version = date = ""
    for n in preorder(root):
        if n.tag in ("span", "p", "div", "li") and not has_block(n):
            t = text(n)
            m = re.search(r"Bản\s*:?\s*([0-9]+(?:\.[0-9]+)+)\s*(?:\((\d{1,2}/\d{1,2}/\d{4})\))?", t)
            if m:
                version, date = m.group(1), m.group(2) or ""
                break
    return {"title": title, "h1": h1, "version": version, "date": date}


# --------------------------------------------------------------------------- text
PREFIX = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "h5": "##### ", "li": "- "}


def emit(node: Node, out: list):
    if node.tag in SKIP:
        return
    if node.tag == "tr":
        cells = [c for c in node.children if c.tag in ("td", "th")]
        out.append((node.line, "| " + " | ".join(text(c).replace("|", "\\|") for c in cells) + " |"))
        return
    if node.tag == "pre":
        body = raw_text(node).strip("\n")
        for i, ln in enumerate(body.split("\n")):
            out.append((node.line + i, "    " + ln.rstrip()))
        return
    if node.tag in BLOCK:
        t = text(node)
        if t:
            out.append((node.line, PREFIX.get(node.tag, "") + t))
        return
    buf, bline = [], None

    def flush():
        nonlocal buf, bline
        t = norm("".join(buf))
        if t:
            out.append((bline, t))
        buf, bline = [], None

    for c in node.children:
        if is_inline(c):
            t = raw_text(c)
            if t.strip() and bline is None:
                bline = c.line
            buf.append(t + (" " if c.tag and is_method_label(c) else ""))
        else:
            flush()
            emit(c, out)
    flush()


def cmd_text(root: Node) -> str:
    out: list = []
    emit(root, out)
    return "\n".join(f"L{ln:>4}: {t}" for ln, t in out)


# --------------------------------------------------------------------------- tables / inventory
def rows_of(table: Node):
    """tr thuộc trực tiếp table này (không lấy tr của bảng lồng)."""
    res = []
    stack = list(reversed(table.children))
    while stack:
        n = stack.pop()
        if n.tag == "tr":
            res.append(n)
        elif n.tag != "table" and n.tag is not None:
            stack.extend(reversed(n.children))
    return res


def cell_key(cell: Node) -> str:
    for n in preorder(cell):
        if n.tag == "code":
            return text(n)
    return text(cell)


def kind_of(heading: str, headers: list[str], in_endpoint: bool) -> str:
    h = (heading or "").lower()
    first = (headers[0] if headers else "").lower()
    joined = " ".join(headers).lower()
    if first.startswith("http") or first.startswith("lỗi") or (
            re.search(r"lỗi|error", h) and "message" in joined):
        return "error"
    if in_endpoint and re.search(r"query|request|body|header|input", h):
        return "input"
    if in_endpoint and re.search(r"response|output", h):
        return "output"
    if first in ("field", "parameter", "output field", "field chung"):
        return "field"
    return "other"


def normalize_endpoint(method: str, path: str) -> str:
    path = re.sub(r"^https?://[^/]+", "", path.strip())
    path = re.sub(r"^/v1(?=/)", "", path)
    return f"{method.strip().upper()} {path}"


def collect(root: Node) -> dict:
    endpoints: dict[str, dict] = {}
    tables: list[dict] = []
    headings: list[tuple] = []
    st = {"h2": None, "h3": None, "h4": None, "ep": None}
    for n in preorder(root):
        if n.tag in ("h2", "h3", "h4"):
            t = text(n)
            headings.append((n.tag, t, n.line))
            if n.tag == "h2":
                st.update(h2=t, h3=None, h4=None, ep=None)
            elif n.tag == "h3":
                st.update(h3=t, h4=None)
                par = n.parent
                if par is not None and any(c.tag and c.has_cls("mtd") for c in par.children):
                    if st["ep"] and endpoints[st["ep"]]["title"] is None:
                        endpoints[st["ep"]]["title"] = t
            else:
                st["h4"] = t
        elif n.tag == "span" and n.has_cls("mtd"):
            sibs = [c for c in n.parent.children if c.tag]
            i = sibs.index(n)
            path = next((s for s in sibs[i + 1:] if any(c.endswith("path") for c in s.cls())), None)
            if path is not None:
                key = normalize_endpoint(text(n), text(path))
                st["ep"] = key
                st["h4"] = None
                endpoints.setdefault(key, {"key": key, "path_raw": text(path), "title": None,
                                           "line": n.line})
        elif n.tag == "table":
            trs = rows_of(n)
            if not trs:
                continue
            head_tr = next((tr for tr in trs if any(c.tag == "th" for c in tr.children)), None)
            headers = [text(c) for c in head_tr.children if c.tag in ("td", "th")] if head_tr else []
            body = []
            for tr in trs:
                if tr is head_tr:
                    continue
                cells = [c for c in tr.children if c.tag in ("td", "th")]
                if not cells:
                    continue
                body.append({"line": tr.line, "cells": [text(c) for c in cells],
                             "key": cell_key(cells[0])})
            # cột "bắt buộc" không có tiêu đề
            for ci, hname in enumerate(headers):
                if hname == "":
                    vals = {r["cells"][ci].lower() for r in body if ci < len(r["cells"]) and r["cells"][ci]}
                    if vals and vals <= REQ_WORDS:
                        headers[ci] = "Bắt buộc"
            heading = st["h4"] or st["h3"] or st["h2"] or ""
            ctx = st["ep"] or " › ".join(x for x in (st["h2"], st["h3"]) if x)
            tables.append({"endpoint": st["ep"], "context": ctx, "heading": heading,
                           "kind": kind_of(heading, headers, bool(st["ep"])), "headers": headers,
                           "rows": body, "line": n.line})
    return {"endpoints": endpoints, "tables": tables, "headings": headings}


def esc(s: str, cap: int = 400) -> str:
    s = s.replace("|", "\\|")
    return s if len(s) <= cap else s[:cap] + "…"


ID_RE = re.compile(r"(^|[._\]\[])(id|\w+_ids?)$")


def cmd_inventory(root: Node, path: str) -> str:
    m = meta(root)
    data = collect(root)
    eps, tables = data["endpoints"], data["tables"]
    out = [f"# Inventory docs Public API — {m['h1'] or m['title']} · bản {m['version'] or '?'}"
           f"{' (' + m['date'] + ')' if m['date'] else ''}", "",
           f"> Nguồn: `{path}` · sinh bởi `scripts/api_docs_extract.py inventory` · "
           "**L = số dòng trong file HTML nguồn** (dùng để trích dẫn trong report).",
           "> Ô trống = docs không ghi → nguyên liệu `DOC-MISS`. KHÔNG sửa tay — chạy lại script.", "",
           f"## Endpoint ({len(eps)})", "", "| # | Method · Path | Tiêu đề | L |", "|---|---|---|---|"]
    for i, e in enumerate(eps.values(), 1):
        out.append(f"| {i} | `{e['key']}` | {e['title'] or ''} | L{e['line']} |")
    out.append("")

    def dump(tbls):
        for t in tbls:
            out.append(f"### [{t['kind']}] {t['heading'] or '(không tiêu đề)'} (L{t['line']})")
            hdr = ["L"] + [h or "(trống)" for h in t["headers"]]
            if len(hdr) == 1:
                width = max((len(r["cells"]) for r in t["rows"]), default=0)
                hdr += [f"c{i + 1}" for i in range(width)]
            out.append("| " + " | ".join(hdr) + " |")
            out.append("|" + "---|" * len(hdr))
            for r in t["rows"]:
                cells = r["cells"] + [""] * (len(hdr) - 1 - len(r["cells"]))
                out.append(f"| L{r['line']} | " + " | ".join(esc(c) for c in cells[:len(hdr) - 1]) + " |")
            out.append("")

    for key, e in eps.items():
        out.append(f"## `{key}` — {e['title'] or ''} (L{e['line']})")
        out.append("")
        dump([t for t in tables if t["endpoint"] == key])
    rest = [t for t in tables if not t["endpoint"]]
    if rest:
        out.append("## Bảng ngoài endpoint (quy ước chung · object · bảng giá trị · changelog)")
        out.append("")
        ctx = None
        for t in rest:
            if t["context"] != ctx:
                ctx = t["context"]
                out.append(f"#### › {ctx}")
            dump([t])

    # tổng hợp
    n_in = sum(len(t["rows"]) for t in tables if t["kind"] in ("input", "field"))
    out += ["## Tổng hợp", "",
            f"- {len(eps)} endpoint · {len(tables)} bảng · {n_in} dòng param/field (input + object) · "
            f"{sum(len(t['rows']) for t in tables if t['kind'] == 'error')} dòng lỗi", "",
            "### Param kiểu ID theo endpoint (nguyên liệu ma trận bot A ↔ B — DOC-SEC)", "",
            "| Endpoint | Param ID (L) |", "|---|---|"]
    for key in eps:
        ids = []
        for t in tables:
            if t["endpoint"] == key and t["kind"] in ("input", "field"):
                for r in t["rows"]:
                    k = r["key"].replace("[]", "")
                    if ID_RE.search(k):
                        ids.append(f"`{r['key']}` (L{r['line']})")
        out.append(f"| `{key}` | {', '.join(ids) or '—'} |")
    obj_ids = []
    for t in rest:
        if t["kind"] in ("field", "input", "other"):
            for r in t["rows"]:
                k = r["key"].replace("[]", "")
                if re.fullmatch(r"[\w.\[\]]+", r["key"]) and ID_RE.search(k) and "request_id" not in k:
                    obj_ids.append(f"`{r['key']}` (L{r['line']}, {t['context']})")
    if obj_ids:
        out += ["", "Param ID trong object (message / action):", ""] + [f"- {x}" for x in obj_ids]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- diff
def req_norm(v: str) -> str:
    v = v.lower().strip()
    if v in ("có", "bắt buộc", "yes", "✔"):
        return "Y"
    if v in ("không", "tuỳ chọn", "tùy chọn", "no"):
        return "N"
    if "điều kiện" in v:
        return "C"
    if "khuyến nghị" in v:
        return "R"
    return v


def col(headers, name_pred):
    for i, h in enumerate(headers):
        if name_pred(h.lower()):
            return i
    return None


SKIP_KEYS = {"", "—", "-", "không có", "không", "none"}


def canon(key: str) -> str:
    """`actions[].tag_ids[]` → `actions.tag_ids` — bỏ ký hiệu mảng để 2 bản viết khác nhau vẫn khớp."""
    return key.strip().strip("`").replace("[]", "")


def type_norm(t: str) -> str:
    return re.sub(r"\s+", "", t.lower().replace(",", "|"))


def rows_by_kind(data, ep, kind):
    res = {}
    for t in data["tables"]:
        if t["endpoint"] != ep or t["kind"] != kind:
            continue
        ti = col(t["headers"], lambda h: h == "type")
        ri = col(t["headers"], lambda h: h in ("bắt buộc",))
        mi = col(t["headers"], lambda h: "message" in h)
        for r in t["rows"]:
            if kind == "error":
                key = norm((r["cells"][mi] if mi is not None and mi < len(r["cells"]) else " ".join(r["cells"]))).lower()
                if key in SKIP_KEYS:
                    continue
                http = r["cells"][0] if r["cells"] else ""
                res.setdefault(key, {"line": r["line"], "http": http, "label": key[:120]})
            else:
                key = canon(r["key"])
                if key.lower() in SKIP_KEYS:
                    continue
                res.setdefault(key, {
                    "line": r["line"], "label": r["key"].strip().strip("`"),
                    "type": r["cells"][ti] if ti is not None and ti < len(r["cells"]) else None,
                    "req": req_norm(r["cells"][ri]) if ri is not None and ri < len(r["cells"]) else None})
    return res


def object_leaves(data) -> dict:
    """Leaf param của bảng ngoài endpoint (message object / action object) → dòng L."""
    res = {}
    for t in data["tables"]:
        if t["endpoint"] or t["kind"] == "error":
            continue
        for r in t["rows"]:
            k = canon(r["key"])
            if re.fullmatch(r"[\w.]+", k):
                res.setdefault(k.split(".")[-1], []).append((r["line"], t["context"]))
    return res


def resolve_ellipsis(a: dict, b: dict):
    full = [k for k in list(a) + list(b) if not k.startswith(("…", "..."))]
    for side in (a, b):
        for k in [k for k in side if k.startswith(("…", "..."))]:
            rest = k.lstrip("….")
            cand = {f for f in full if f == rest or f.endswith("." + rest)}
            if len(cand) == 1:
                tgt = cand.pop()
                if tgt not in side:
                    side[tgt] = side.pop(k)


def strip_num(h: str) -> str:
    return re.sub(r"^\d+(\.\d+)*\.?\s*", "", h).strip().lower()


def cmd_diff(old_root, new_root, old_path, new_path) -> str:
    mo, mn = meta(old_root), meta(new_root)
    do, dn = collect(old_root), collect(new_root)
    out = [f"# Diff cấu trúc docs Public API — bản {mo['version'] or '?'} → {mn['version'] or '?'}", "",
           f"> Cũ: `{old_path}` · Mới: `{new_path}` · L cũ / L mới = số dòng trong từng file HTML.",
           "> **Heuristic** — khớp theo tên param/field và message lỗi. Mỗi dòng là ỨNG VIÊN: mở L hai bên để xác nhận "
           "trước khi ghi `DOC-VER`. Đổi câu chữ message lỗi sẽ hiện thành 1 dòng bớt + 1 dòng thêm.", "",
           "## 1. Endpoint", "", "| Trạng thái | Endpoint | L cũ | L mới |", "|---|---|---|---|"]
    keys = list(dict.fromkeys(list(do["endpoints"]) + list(dn["endpoints"])))
    for k in keys:
        a, b = do["endpoints"].get(k), dn["endpoints"].get(k)
        st = "giữ" if a and b else ("**bỏ**" if a else "**thêm**")
        out.append(f"| {st} | `{k}` | {'L' + str(a['line']) if a else '—'} | {'L' + str(b['line']) if b else '—'} |")
    out += ["", "## 2. Thay đổi theo endpoint", "",
            "| Endpoint | Loại | Thay đổi | Key | Cũ | Mới |", "|---|---|---|---|---|---|"]
    n_change = 0
    new_obj = object_leaves(dn)
    for k in keys:
        if k not in do["endpoints"] or k not in dn["endpoints"]:
            continue
        for kind in ("input", "output", "error"):
            a, b = rows_by_kind(do, k, kind), rows_by_kind(dn, k, kind)
            if kind != "error":
                resolve_ellipsis(a, b)
            if kind == "output":
                for c in COMMON_OUTPUT:
                    a.pop(c, None)
                    b.pop(c, None)
            for key in sorted(set(a) | set(b)):
                ra, rb = a.get(key), b.get(key)
                label = esc((ra or rb)["label"], 120)
                if ra and not rb:
                    leaf = key.split(".")[-1]
                    if kind == "input" and "." in key and leaf in new_obj:
                        pref = key.split(".")[0].rstrip("s").lower()
                        ln, ctx = next((x for x in new_obj[leaf] if pref in x[1].lower()), new_obj[leaf][0])
                        out.append(f"| `{k}` | {kind} | chuyển sang mục object | `{label}` | L{ra['line']} | L{ln} ({esc(ctx, 60)}) |")
                    else:
                        out.append(f"| `{k}` | {kind} | bớt | `{label}` | L{ra['line']} | — |")
                elif rb and not ra:
                    out.append(f"| `{k}` | {kind} | thêm | `{label}` | — | L{rb['line']} |")
                else:
                    if kind != "error" and ra["type"] and rb["type"] and type_norm(ra["type"]) != type_norm(rb["type"]):
                        out.append(f"| `{k}` | {kind} | đổi kiểu | `{label}` | {esc(ra['type'], 60)} (L{ra['line']}) | {esc(rb['type'], 60)} (L{rb['line']}) |")
                    elif kind != "error" and ra["req"] and rb["req"] and ra["req"] != rb["req"]:
                        out.append(f"| `{k}` | {kind} | đổi bắt buộc | `{label}` | {ra['req']} (L{ra['line']}) | {rb['req']} (L{rb['line']}) |")
                    else:
                        continue
                n_change += 1
    if not n_change:
        out.append("| — | — | không phát hiện thay đổi cấu trúc | — | — | — |")
    ho = {strip_num(t): (lv, t, ln) for lv, t, ln in do["headings"] if lv in ("h2", "h3")}
    hn = {strip_num(t): (lv, t, ln) for lv, t, ln in dn["headings"] if lv in ("h2", "h3")}
    out += ["", "## 3. Mục lục (h2/h3) thêm / bớt", "", "| Thay đổi | Mục | L |", "|---|---|---|"]
    for key in sorted(set(ho) - set(hn)):
        out.append(f"| bớt | {ho[key][1]} | cũ L{ho[key][2]} |")
    for key in sorted(set(hn) - set(ho)):
        out.append(f"| thêm | {hn[key][1]} | mới L{hn[key][2]} |")
    out += ["", f"Tổng: {len(keys)} endpoint · {n_change} thay đổi param/field/lỗi (ứng viên)."]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- check
def json_candidates(t: str):
    t = t.strip()
    if t.startswith("curl"):
        m = re.search(r"-d '(.*)'\s*$", t, re.S)
        return [("curl -d", m.group(1))] if m else []
    first = t.split("\n", 1)[0]
    if re.match(r"^(GET|POST|PUT|PATCH|DELETE)\s+\S+", first):
        parts = re.split(r"\n\s*\n", t, maxsplit=1)
        return [("body", parts[1])] if len(parts) > 1 else []
    if first.startswith("HTTP/"):
        return [("body", t.split("\n", 1)[1] if "\n" in t else "")]
    return [("json", t)]


def try_parse(s: str):
    if "..." in s or "…" in s:
        return "placeholder", None
    try:
        return "ok", json.loads(s)
    except ValueError:
        pass
    try:
        return "fragment", json.loads("{" + s + "}")
    except ValueError:
        pass
    lines = [ln for ln in s.split("\n") if ln.strip()]
    try:
        return "lines", [json.loads(ln) for ln in lines]
    except ValueError:
        return "fail", None


def walk_json(v, fn, path="$"):
    fn(v, path)
    if isinstance(v, dict):
        for k, x in v.items():
            walk_json(x, fn, f"{path}.{k}")
    elif isinstance(v, list):
        for i, x in enumerate(v):
            walk_json(x, fn, f"{path}[{i}]")


def js_literal_to_json(s: str):
    s = re.sub(r'([{,]\s*)([A-Za-z_$][\w$]*)\s*:', r'\1"\2":', s)
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return json.loads(s)


def extract_ex(root: Node):
    for n in preorder(root):
        if n.tag == "script":
            src = "".join(c.text for c in n.children if c.tag is None)
            m = re.search(r"var\s+EX\s*=\s*\{", src)
            if not m:
                continue
            i, depth, in_str, esc_ = m.end() - 1, 0, False, False
            for j in range(i, len(src)):
                ch = src[j]
                if in_str:
                    if esc_:
                        esc_ = False
                    elif ch == "\\":
                        esc_ = True
                    elif ch == '"':
                        in_str = False
                elif ch == '"':
                    in_str = True
                elif ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        return js_literal_to_json(src[i:j + 1]), n.line
    return None, None


def deep_diff(a, b, path="$"):
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        return [path]
    if isinstance(a, dict):
        res = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                res.append(f"{path}.{k}")
            else:
                res += deep_diff(a[k], b[k], f"{path}.{k}")
        return res
    if isinstance(a, list):
        if len(a) != len(b):
            return [f"{path} (độ dài {len(a)} ≠ {len(b)})"]
        res = []
        for i, (x, y) in enumerate(zip(a, b)):
            res += deep_diff(x, y, f"{path}[{i}]")
        return res
    return [] if a == b else [f"{path} ({a!r} ≠ {b!r})"]


def cmd_check(root: Node) -> str:
    m = meta(root)
    out = [f"# Check máy docs — {m['h1'] or m['title']} · bản {m['version'] or '?'} {m['date']}", "",
           "> Kết quả là ỨNG VIÊN `DOC-EX` / `DOC-INT` — AI mở L<n> xác nhận trước khi ghi report.", ""]
    # 1. JSON
    stats = {"ok": 0, "fragment": 0, "lines": 0, "placeholder": 0, "fail": 0}
    fails, pag = [], []
    for n in preorder(root):
        if n.tag != "pre":
            continue
        for label, body in json_candidates(raw_text(n)):
            kind, val = try_parse(body)
            stats[kind] += 1
            if kind == "fail":
                fails.append(f"| L{n.line} | {label} | `{esc(norm(body), 90)}` |")
                continue
            if val is None:
                continue

            def chk(v, p, line=n.line):
                if isinstance(v, dict) and "total_items" in v and "total_pages" in v:
                    ti, tp = v["total_items"], v["total_pages"]
                    if "limit" in v and isinstance(v["limit"], int) and v["limit"] > 0:
                        exp = math.ceil(ti / v["limit"]) if ti else 0
                        if tp != exp:
                            pag.append(f"| L{line} | `{p}` | total_pages={tp}, kỳ vọng ceil({ti}/{v['limit']})={exp} |")
                        if "has_next" in v and "page" in v and v["has_next"] != (v["page"] < tp):
                            pag.append(f"| L{line} | `{p}` | has_next={v['has_next']} nhưng page={v['page']}, total_pages={tp} |")
                    else:
                        pag.append(f"| L{line} | `{p}` | có total_items/total_pages nhưng không có limit — kiểm tay theo request mẫu |")
            walk_json(val, chk)
    out += ["## 1. JSON trong khối code", "",
            f"ok {stats['ok']} · fragment {stats['fragment']} · nhiều dòng {stats['lines']} · "
            f"có placeholder (bỏ qua) {stats['placeholder']} · **không parse được {stats['fail']}**", ""]
    if fails:
        out += ["| L | Loại | Nội dung |", "|---|---|---|"] + fails + [""]
    out += ["## 2. Số học phân trang", ""]
    out += (["| L | JSON path | Vấn đề |", "|---|---|---|"] + pag) if pag else ["Không phát hiện lệch."]
    out.append("")
    # 3. epoch
    ep = []
    for n in preorder(root):
        if n.tag is None and n.parent is not None and n.parent.tag not in SKIP:
            for mm in re.finditer(r"(?<![\d.])(1[4-9]\d{8})(?!\d)", n.text):
                v = int(mm.group(1))
                utc = datetime.fromtimestamp(v, tz=timezone.utc)
                jst = utc.astimezone(timezone(timedelta(hours=9)))
                ep.append(f"| L{n.line} | `{v}` | {utc:%Y-%m-%d %H:%M:%S} UTC | {jst:%Y-%m-%d %H:%M:%S} JST |")
    out += ["## 3. Số epoch (giây) trong docs — so với ngày phát hành docs " + (m["date"] or "?"), ""]
    out += (["| L | Giá trị | UTC | JST |", "|---|---|---|---|"] + ep) if ep else ["Không có."]
    out.append("")
    # 4. anchor
    ids, dup = {}, []
    for n in preorder(root):
        i = n.attrs.get("id") if n.tag else None
        if i:
            if i in ids:
                dup.append(f"| L{n.line} | id trùng `{i}` (lần đầu L{ids[i]}) |")
            ids.setdefault(i, n.line)
    broken = [f"| L{n.line} | `href=\"{n.attrs['href']}\"` không có id đích |"
              for n in preorder(root) if n.tag == "a" and n.attrs.get("href", "").startswith("#")
              and len(n.attrs["href"]) > 1 and n.attrs["href"][1:] not in ids]
    out += ["## 4. Anchor nội bộ", ""]
    out += (["| L | Vấn đề |", "|---|---|"] + broken + dup) if (broken or dup) else ["Không có link hỏng / id trùng."]
    out.append("")
    # 5. EX ↔ request mẫu
    out += ["## 5. Code tabs (khối `EX` trong script) ↔ request mẫu cùng endpoint", ""]
    try:
        ex, ex_line = extract_ex(root)
    except ValueError as e:
        ex, ex_line = None, None
        out += [f"Không parse được khối EX ({e}) — kiểm tay curl/Python/Node/Ruby với request mẫu.", ""]
    if ex:
        nodes = list(preorder(root))
        res = []
        for box in nodes:
            if box.tag != "div" or "data-ex" not in box.attrs:
                continue
            k = box.attrs["data-ex"]
            e = ex.get(k)
            if e is None:
                res.append(f"| L{box.line} | `{k}` | không có trong EX |")
                continue
            art = box.ancestor("article")
            samples = [p for p in nodes if p.tag == "pre" and p.has_cls("http") and p.idx < box.idx
                       and (art is None or p.ancestor("article") is art)
                       and re.match(r"^(GET|POST)\s+/v1", raw_text(p).strip())]
            if not samples:
                res.append(f"| L{box.line} | `{k}` | không thấy request mẫu `GET|POST /v1…` phía trước |")
                continue
            sp = samples[-1]
            body_txt = raw_text(sp).strip()
            first = body_txt.split("\n", 1)[0]
            meth, url = first.split()[0], first.split()[1]
            path_, _, qs = url.partition("?")
            if meth != e.get("m") or path_ != e.get("p"):
                res.append(f"| L{sp.line} | `{k}` | request mẫu `{meth} {path_}` ≠ EX `{e.get('m')} {e.get('p')}` (L{ex_line}) |")
            q_sample = {a: unquote(b) for a, b in parse_qsl(qs, keep_blank_values=True)}
            q_ex = {a: str(b).lower() if isinstance(b, bool) else str(b) for a, b in (e.get("q") or {}).items()}
            if q_sample != q_ex:
                miss = sorted(set(q_sample.items()) ^ set(q_ex.items()))
                res.append(f"| L{sp.line} | `{k}` | query khác EX: {esc(str(miss), 160)} |")
            hm = re.search(r"^Idempotency-Key:\s*(\S+)", body_txt, re.M)
            if (hm.group(1) if hm else None) != e.get("idem"):
                res.append(f"| L{sp.line} | `{k}` | Idempotency-Key mẫu `{hm.group(1) if hm else '—'}` ≠ EX `{e.get('idem')}` |")
            if meth == "POST":
                parts = re.split(r"\n\s*\n", body_txt, maxsplit=1)
                kind, val = try_parse(parts[1]) if len(parts) > 1 else ("fail", None)
                if kind != "ok":
                    res.append(f"| L{sp.line} | `{k}` | body mẫu không parse được ({kind}) |")
                else:
                    d = deep_diff(val, e.get("b"))
                    if d:
                        res.append(f"| L{sp.line} | `{k}` | body khác EX tại: {esc(', '.join(d), 200)} |")
        out += (["| L | data-ex | Lệch |", "|---|---|---|"] + res) if res else [
            f"Khớp toàn bộ ({sum(1 for b in nodes if b.tag == 'div' and 'data-ex' in b.attrs)} code tabs)."]
    elif ex is None and not any("Không parse" in x for x in out[-2:]):
        out.append("Không có khối EX (docs không dùng code tabs) — bỏ qua.")
    out.append("")
    out += example_checks(root)
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- check ví dụ ↔ docs
COMMON_RES = {"success", "request_id", "data", "pagination", "error"}
ENTITY = {"tags": "tag", "scenarios": "scenario", "templates": "template", "fields": "field",
          "friend_info": "field", "handling_status": "handling", "friend_detail": "friend",
          "conversations": "friend", "friend": "friend"}
FRIEND_ATTRS = ("line_name", "system_name", "email", "phone", "line_friend_id")


def enum_tables(data) -> dict:
    """Enum lấy từ chính docs: bảng `Field | Giá trị` (vd §7.5) + bảng có cột đầu `message_type` / `field_type`."""
    enums: dict[str, set] = {}
    for t in data["tables"]:
        if t["endpoint"] or not t["headers"]:
            continue
        h = [x.lower() for x in t["headers"]]
        if h[0] == "field" and len(h) > 1 and h[1].startswith("giá trị"):
            for r in t["rows"]:
                if len(r["cells"]) < 2:
                    continue
                leaf = r["cells"][0].split(".")[-1].replace("[]", "").strip("` ")
                vals = {v.strip().strip("`") for v in r["cells"][1].split("/") if v.strip()}
                if leaf and vals:
                    enums.setdefault(leaf, set()).update(vals)
        elif h[0] in ("message_type", "field_type"):
            vals = set()
            for r in t["rows"]:
                for v in r["cells"][0].split(","):
                    v = v.strip().strip("`")
                    if re.fullmatch(r"[A-Za-z_]+", v):
                        vals.add(v)
            enums[h[0]] = vals
    return enums


def flatten(v, p=""):
    out = []
    if isinstance(v, dict):
        for k, x in v.items():
            q = f"{p}.{k}" if p else k
            out.append((q, x))
            out += flatten(x, q)
    elif isinstance(v, list):
        for x in v:
            out += flatten(x, p)
    return out


def type_ok(val, t: str) -> bool:
    t = (t or "").lower()
    if not t:
        return True
    for o in (x.strip() for x in t.split("|")):
        if o == "null" and val is None:
            return True
        if o.startswith("integer") and isinstance(val, int) and not isinstance(val, bool):
            return True
        if o.startswith("number") and isinstance(val, (int, float)) and not isinstance(val, bool):
            return True
        if o.startswith("string") and isinstance(val, str):
            return True
        if o.startswith("boolean") and isinstance(val, bool):
            return True
        if o.startswith("datetime") and isinstance(val, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}", val):
            return True
        if o.startswith("date") and not o.startswith("datetime") and isinstance(val, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", val):
            return True
        if o.startswith("array") and isinstance(val, list):
            return True
        if o.startswith("object") and isinstance(val, dict):
            return True
    return False


def example_checks(root: Node) -> list[str]:
    """6. field/kiểu/enum của ví dụ ↔ bảng field · 7. cùng ID khác dữ liệu giữa các ví dụ · 8. số phần tử ↔ phân trang."""
    data = collect(root)
    enums = enum_tables(data)
    schema, facts, arrays = [], {}, []
    st = {"ep": None, "art": None, "query": {}}
    for n in preorder(root):
        if n.tag == "h2":
            st.update(ep=None, art=None, query={})
        if n.tag == "span" and n.has_cls("mtd"):
            sibs = [c for c in n.parent.children if c.tag]
            i = sibs.index(n)
            p = next((s for s in sibs[i + 1:] if any(c.endswith("path") for c in s.cls())), None)
            if p is not None:
                st.update(ep=normalize_endpoint(text(n), text(p)), query={})
        if n.tag != "pre" or not st["ep"] or not (n.has_cls("code") or n.has_cls("http")):
            continue
        ep = st["ep"]
        raw = raw_text(n).strip()
        first = raw.split("\n", 1)[0]
        m = re.match(r"^GET\s+/v1\S*\?(\S+)", first)
        if m:
            st["query"] = {a: b for a, b in parse_qsl(m.group(1))}
        for label, body in json_candidates(raw):
            kind, val = try_parse(body)
            if kind != "ok" or not isinstance(val, dict):
                continue
            is_req = raw.startswith(("POST", "GET", "curl"))
            ktables = {}
            for t in data["tables"]:
                if t["endpoint"] == ep and t["kind"] == ("input" if is_req else "output"):
                    ti = col(t["headers"], lambda h: h == "type")
                    for r in t["rows"]:
                        ktables[canon(r["key"])] = (r["cells"][ti] if ti is not None and ti < len(r["cells"]) else "", r["line"])

            def resolve(cp):
                if cp in ktables:
                    return cp
                for k in ktables:
                    if k.startswith(("…", "...")):
                        rest = k.lstrip("….")
                        if cp == rest or cp.endswith("." + rest):
                            return k
                return None

            if is_req:
                if isinstance(val, dict):
                    for key in val:
                        if resolve(key) is None:
                            schema.append(f"| L{n.line} | `{ep}` request | field `{key}` không có trong bảng Request body |")
                continue
            if not ({"success", "data"} & set(val)):
                continue  # mảnh ví dụ, không phải response đầy đủ
            for path, v in flatten(val):
                top = path.split(".")[0]
                if path in COMMON_RES or top in ("error", "pagination"):
                    continue
                k = resolve(path)
                if k is None:
                    parts = path.split(".")
                    if any(resolve(".".join(parts[:i])) for i in range(len(parts) - 1, 0, -1)):
                        continue  # field con của object/mảng đã mô tả ở dòng cha
                    if any(tk.startswith(path + ".") for tk in ktables):
                        continue  # object/mảng cha được mô tả qua các dòng field con
                    if isinstance(v, (dict, list)) and any(tk.startswith(("…", "...")) for tk in ktables):
                        continue  # container của các dòng "…[].x"
                    schema.append(f"| L{n.line} | `{ep}` | `{path}` không có trong bảng Response |")
                    continue
                t, tl = ktables[k]
                if not type_ok(v, t):
                    schema.append(f"| L{n.line} | `{ep}` | `{path}` = `{esc(json.dumps(v, ensure_ascii=False), 50)}` trái kiểu `{esc(t, 40)}` (bảng L{tl}) |")
                leaf = path.split(".")[-1]
                allowed = enums.get("field_type") if (leaf == "type" and "friend_info" in path) else enums.get(leaf)
                if allowed and isinstance(v, str) and v not in allowed:
                    schema.append(f"| L{n.line} | `{ep}` | `{path}` = `{v}` ngoài tập giá trị docs liệt kê ({', '.join(sorted(allowed))}) |")

            # 7. facts theo thực thể
            def walk(v, p, line=n.line):
                if isinstance(v, dict):
                    seg = p.split(".")[-1] if p else ""
                    ent = ENTITY.get(seg)
                    if ep == "GET /handling-statuses" and p == "data":
                        ent = "handling"
                    if "lmessage_friend_id" in v and ent in (None, "friend") and seg not in ("tags", "scenarios"):
                        ent = "friend"
                    if ent == "friend" and "lmessage_friend_id" in v:
                        for a in FRIEND_ATTRS:
                            if a in v:
                                facts.setdefault(("friend", v["lmessage_friend_id"], a), set()).add((json.dumps(v[a], ensure_ascii=False), line))
                    elif ent:
                        idv = next((v[x] for x in ("scenario_id", "template_id", "field_id", "id") if x in v), None)
                        name = v.get("name", v.get("title"))
                        if idv is not None and name is not None:
                            facts.setdefault((ent, idv, "name"), set()).add((json.dumps(name, ensure_ascii=False), line))
                        tv = v.get("field_type", v.get("type")) if ent == "field" else None
                        if idv is not None and tv is not None:
                            facts.setdefault((ent, idv, "type"), set()).add((json.dumps(tv, ensure_ascii=False), line))
                    for k2, x in v.items():
                        walk(x, f"{p}.{k2}" if p else k2)
                elif isinstance(v, list):
                    for x in v:
                        walk(x, p)
            walk(val, "")

            # 8. số phần tử ↔ phân trang
            d = val.get("data")
            pg = val.get("pagination") if isinstance(val.get("pagination"), dict) else {}
            total = d.get("total_items") if isinstance(d, dict) and isinstance(d.get("total_items"), int) else pg.get("total_items")
            if isinstance(d, dict) and isinstance(total, int):
                limit = pg.get("limit") or int(st["query"].get("limit", 100) or 100)
                limit = min(max(limit, 1), 500)
                page = pg.get("page") or max(int(st["query"].get("page", 1) or 1), 1)
                arr_key = next((k2 for k2, x in d.items() if isinstance(x, list) and k2 != "warnings"), None)
                if arr_key is not None:
                    exp = min(limit, max(total - (page - 1) * limit, 0))
                    got = len(d[arr_key])
                    if got != exp:
                        arrays.append(f"| L{n.line} | `{ep}` | `data.{arr_key}` có {got} phần tử; theo total_items={total}, page={page}, limit={limit} phải là {exp} — không ghi rút gọn |")
    out = ["## 6. Ví dụ ↔ bảng field của docs (field · kiểu · tập giá trị)", ""]
    out += (["| L | Endpoint | Lệch |", "|---|---|---|"] + schema) if schema else ["Không lệch."]
    out += ["", "## 7. Dữ liệu mẫu giữa các ví dụ (cùng ID mà khác giá trị)", ""]
    conf = []
    for (ent, idv, attr), vals in sorted(facts.items(), key=lambda x: (x[0][0], str(x[0][1]), x[0][2])):
        if len({v for v, _ in vals}) > 1:
            conf.append(f"| {ent} `{idv}` | `{attr}` | " + " · ".join(f"{esc(v, 40)} (L{ln})" for v, ln in sorted(vals, key=lambda x: x[1])) + " |")
    out += (["| Thực thể | Thuộc tính | Giá trị ở các ví dụ |", "|---|---|---|"] + conf) if conf else ["Nhất quán."]
    out += ["", "## 8. Số phần tử mảng ↔ phân trang", ""]
    out += (["| L | Endpoint | Lệch |", "|---|---|---|"] + arrays) if arrays else ["Khớp."]
    out += ["", "> Mục 6–8 là ứng viên `DOC-INT` (ví dụ ↔ docs / ví dụ bất hợp lý). Các quy tắc ngữ nghĩa (thứ tự sắp xếp, "
            "quy tắc riêng endpoint, câu chuyện dữ liệu giữa endpoint) vẫn phải rà tay."]
    return out


# --------------------------------------------------------------------------- main
def write(s: str, dest: str | None):
    if dest:
        with open(dest, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
        print(f"Đã ghi {dest} ({s.count(chr(10))} dòng)")
    else:
        sys.stdout.write(s)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("meta", "text", "inventory", "check"):
        p = sub.add_parser(name)
        p.add_argument("html")
        p.add_argument("-o", "--out")
    p = sub.add_parser("diff")
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("-o", "--out")
    a = ap.parse_args()
    if a.cmd == "meta":
        write(json.dumps(meta(load(a.html)), ensure_ascii=False) + "\n", a.out)
    elif a.cmd == "text":
        write(cmd_text(load(a.html)) + "\n", a.out)
    elif a.cmd == "inventory":
        write(cmd_inventory(load(a.html), a.html.replace("\\", "/")), a.out)
    elif a.cmd == "check":
        write(cmd_check(load(a.html)), a.out)
    elif a.cmd == "diff":
        write(cmd_diff(load(a.old), load(a.new), a.old.replace("\\", "/"), a.new.replace("\\", "/")), a.out)


if __name__ == "__main__":
    main()
