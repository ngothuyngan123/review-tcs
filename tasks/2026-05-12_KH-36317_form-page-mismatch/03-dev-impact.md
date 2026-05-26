# 03 — Dev Impact (đánh giá ảnh hưởng từ phía Dev)

> Paste nguyên văn từ dev.

## 1. Nguyên nhân (root cause)

- Result form lưu sai câu trả lời của page — câu trả lời của page A đang bị lưu thành page B.
- **Chưa tìm được root cause** (không reproduce được nội bộ).

## 2. Cách fix

- Khi submit, kiểm tra xem **tổng số câu trả lời của 1 page** có khác với **số câu hỏi của page trong setting admin** không. Nếu khác → return về message tiếng Nhật và hiển thị cho user:
  > フォームの質問数が変更されました。画面を再読み込みしてから再度ご回答ください

> **Bản chất**: Workaround chặn submit khi mismatch, không sửa được data đã lưu sai. Không sửa được trường hợp số câu trả lời = số câu hỏi nhưng giá trị bị nhầm page.

## 3. Đã check và sửa các function caller liên quan

- (Dev confirm) đã check và sửa các function sử dụng đến function/data vừa sửa.

## 4. Đánh giá ảnh hưởng

### 4.1 List function

| ID | Function | File | Loại |
|---|---|---|---|
| **F1** | `storeRenderForm` | `app/Services/FormAnswer/FormAnswerService.php` | Direct (server check) |
| **F2** | `form_render_v3.js` | `public/js/form_answer/form_render_v3.js` | Direct (frontend) |

### 4.2 List data bị update khi fix bug

| ID | Data | Ghi chú |
|---|---|---|
| — | (Không có) | Fix là logic check, không thay đổi schema/data. |

### 4.3 List tính năng bị ảnh hưởng (dựa 4.1 + 4.2)

| ID | Tính năng | Risk |
|---|---|---|
| **T1** | Trả lời form (case số câu trả lời user ≠ số câu hỏi admin setting) | High — nơi fix |
| **T2** (suy luận) | Trả lời form happy path (số câu trả lời = số câu hỏi) — regression | High — function chính bị chạm |
| **T3** (suy luận) | Sync data form answer → Google Spread + Form result phía admin | High — nơi KH thấy lỗi |
