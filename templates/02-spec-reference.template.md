# 02 — Spec Reference (trích phần liên quan)

> Chỉ trích phần spec **LIÊN QUAN trực tiếp** đến bug. Không paste toàn bộ spec.
>
> **Ưu tiên**: trỏ đến section trong [LME-SYSTEM-SPEC.md](LME-SYSTEM-SPEC.md) thay vì paste lại.
> Chỉ paste nguyên văn khi cần highlight business rule cụ thể.
>
> Nếu spec nằm ngoài (Confluence, Google Docs, manual LME https://lme.jp/manual/,...) → ghi link + trích đoạn key.

## Nguồn spec

| Trường | Giá trị |
|---|---|
| Tên spec | `<e.g. Broadcast Spec v2.3>` |
| Link spec | `<URL>` |
| Version / Last updated | `<e.g. v2.3 — 2026-01-15>` |
| Section liên quan | `<e.g. 3.2 Scheduled broadcast>` |

## Trích nội dung spec liên quan

<!-- Paste nguyên văn đoạn spec liên quan đến bug.
     Highlight phần mà bug đang vi phạm (bôi **đậm** hoặc quote). -->

### Section: `<tên section>`

>

### Section: `<tên section khác nếu có>`

>

## Business rules liên quan

<!-- List các rule nghiệp vụ mà TCs cần verify -->

- Rule 1:
- Rule 2:
- Rule 3:

## Mâu thuẫn spec ↔ bug (nếu có)

<!-- Nếu spec cũ KHÔNG cover case bug này, hoặc spec sai → flag ở đây.
     Leader quyết định: update spec hay fix theo spec. -->

- [ ] Spec đã cover case này (bug là do code sai)
- [ ] Spec CHƯA cover case này → cần update spec
- [ ] Spec cũ đang SAI → cần update spec
