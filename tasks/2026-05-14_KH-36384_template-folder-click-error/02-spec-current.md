# 02 — Spec Reference (trích phần liên quan)

> Trỏ tới section trong [LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) + spec gốc [spec-features/admin/message-template/](../../spec-features/admin/message-template/).
> Chỉ trích đoạn liên quan trực tiếp đến bug KH-36384 (parse `template_child_id` sai khi URL có hậu tố `/?utm_*`).

## Nguồn spec

| Trường | Giá trị |
|---|---|
| Tên spec | FA-010 — Mẫu tin nhắn (「テンプレート」) |
| Link spec tổng | [LME-SYSTEM-SPEC.md §3.8 FA-010](../../templates/LME-SYSTEM-SPEC.md#38-fa-010--mẫu-tin-nhắn-テンプレート) |
| Link spec chi tiết | [spec-features/admin/message-template/feature-spec.md](../../spec-features/admin/message-template/feature-spec.md) |
| API spec chi tiết | [spec-features/admin/message-template/web/api-spec.md](../../spec-features/admin/message-template/web/api-spec.md) — EP-30 `POST /ajax/template-v2/save-template` |
| Version / Last updated | Spec auto-reverse-engineer từ codebase (commit gần nhất, ngày chưa rõ) |
| Section liên quan | 3 phần: (1) Schema `template_child_id` / `template_group_id`; (2) Park/Group template (container); (3) EP-30 Save template endpoint |

## Trích nội dung spec liên quan

### Section 1: Schema `template_child_id` / `template_group_id` — EP-30 Save template

> [api-spec.md EP-30, lines 257-263](../../spec-features/admin/message-template/web/api-spec.md):

**JSON data (bên trong field `data`):**

| Key | Kiểu | Mô tả |
|-----|------|-------|
| `template_group_id` | **integer** | ID group template cha |
| `template_child_id` | **integer** | ID template con (`null` = tạo mới) |
| *(các field khác tuỳ loại template)* | — | Xử lý bởi service |

> **Spec rõ**: cả 2 ID phải là **integer**. Bug 36384 vi phạm spec ở chỗ server **không enforce** kiểu int — chấp nhận chuỗi `13305944/?utm_source=line&...` rồi lưu nguyên chuỗi vào `template_groups.content`.

### Section 2: Park / Group template (container)

> [LME-SYSTEM-SPEC.md §3.8](../../templates/LME-SYSTEM-SPEC.md), line 355:

- **Park/Group template** (container chứa nhiều template con) → đây là object bị corrupt trong bug (template_group `id=13305886` của bot KH `景品ショップマイルーム`).
- `content` của template_group lưu **danh sách `template_child_id` dạng CSV integer** (vd `"13305887,13305944"`). Khi parse thành công → render được list template con trong folder.

### Section 3: Endpoint chịu trách nhiệm

> [api-spec.md EP-30, line 244](../../spec-features/admin/message-template/web/api-spec.md):

`POST /ajax/template-v2/save-template` — delegate sang `TemplateV2Service@saveTemplateByType()`.

> **Note**: Dev impact `03-dev-impact.md` báo fix nằm ở `createTemplate` trong `app/Http/Controllers/Basic/TemplateV2Controller.php`. Cần Leader confirm: `createTemplate` controller method có gọi `TemplateV2Service@saveTemplateByType()` hay không, hoặc đây là endpoint khác (vd `/ajax/template-v2/create-template` chưa được spec rõ).

## Business rules liên quan

- **R1** — `template_group_id` và `template_child_id` truyền lên server **bắt buộc là integer**. Server phải reject hoặc ép kiểu khi input dạng string/float/chứa ký tự đặc biệt. _(Spec API có nhưng code chưa enforce — gốc bug 36384.)_
- **R2** — `template_groups.content` lưu CSV integer thuần (vd `"13305887,13305944"`). KHÔNG được chứa ký tự non-numeric ngoại trừ dấu phẩy.
- **R3** — Click folder template (mở `SCR-TMT-*` màn list template trong folder) phải parse `content` của từng group → load template con. Nếu parse fail → spec không định nghĩa rõ behavior (hiện tại: throw error). Đề xuất bổ sung rule: parse fail → log error + render danh sách rỗng cho group đó, **không crash toàn màn**.
- **R4** — URL edit template có dạng `/basic/template-v2/add-template?template_group_id={int}&template_child_id={int}`. Spec không nói rõ behavior khi URL có **trailing slash + query string thừa** (vd user paste từ LP có UTM tracking). Đề xuất: server tự **strip** trước khi parse, hoặc reject với 400.
- **R5** — Khi save template thành công (EP-30 trả `success: true`), điều hướng back ra list template phải luôn render bình thường. Không có rule nào trong spec cho phép save với content invalid rồi crash list.

## Mâu thuẫn spec ↔ bug

- [x] **Spec đã cover case này (bug là do code sai)** — Spec API EP-30 đã ghi rõ `template_*_id: integer`. Code (`createTemplate`) chưa enforce → để chuỗi `13305944/?utm_source=line` vượt qua và lưu vào DB. **Bug là implementation gap**, không phải spec gap.
- [ ] Spec CHƯA cover case này → cần update spec
- [ ] Spec cũ đang SAI → cần update spec

### Gợi ý bổ sung spec (không phải bắt buộc fix bug, nhưng nên có cho rõ)

1. **Behavior khi input invalid**: thêm rule rõ vào EP-30 — "Server **must** validate `template_*_id` là integer trước khi save. Nếu fail → trả `success: false`, message `"Invalid template ID"` hoặc tương đương." Hiện EP-30 list 4 case lỗi nhưng không có case này.
2. **Behavior khi `content` của group parse fail**: thêm rule cho UI list template — graceful degradation thay vì crash.
3. **Manual user (https://lme.jp/manual/)**: tùy chọn thêm note "Không paste URL từ LP có UTM tracking khi edit template — hãy paste URL gốc."
