# 02 — Spec Reference

> **Spec reference**: Không có spec riêng cho task này — fallback tham chiếu [LME-SYSTEM-SPEC.md](../../templates/LME-SYSTEM-SPEC.md) section **Scenario / Step message + Filter manager**.

## Điểm liên quan trong LME-SYSTEM-SPEC

- **Scenario**: Tập step messages gửi LINE user theo timing (send ngay / send sau X ngày / send sau X giờ Y phút / duration tối đa 72h theo feature #30571).
- **Step message** có thể attach **filter_manager** (lọc friend cho step) — filter_manager là object riêng có thể tạo/xóa độc lập.
- **Filter lifecycle**: User tạo filter → assign cho step → có thể xóa filter. Khi xóa filter, step đang dùng filter đó → **chưa rõ spec** xử lý ra sao (cascade delete? Block delete khi đang in-use? Soft delete?).

## Spec gap / mâu thuẫn

- **Gap spec**: Hành vi khi filter bị xóa trong lúc user đang tạo step ở tab khác **không được spec hóa rõ**. Fix introduce error message JP mới `フィルターが削除されたため、画面を再読み込みしてください` — đây là rule mới.
- **Mâu thuẫn**: Cũ có try/catch swallow exception → "lặng lẽ" insert step với filter_id ghost. Sau fix → throw error rõ ràng + notify chatwork.

## Spec update needed

- [ ] **Cần update spec** — section "Scenario → Modal tạo step message → Filter manager":
  - Bổ sung rule validation: "Khi user submit tạo step với filter_id, server **MUST** check filter còn tồn tại (`filter_managers` table, status active). Nếu filter đã bị xóa → return error 4xx + msg `フィルターが削除されたため、画面を再読み込みしてください`."
  - Định nghĩa lifecycle filter khi đang in-use: có cảnh báo trước khi xóa? Hay xóa silent + đẩy lỗi xuống các step đang dùng?
  - **Người chịu trách nhiệm update**: Dev assignee + PM.
