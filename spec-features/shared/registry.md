# Danh sách thành phần dùng chung (Shared Components)

> Cập nhật tự động bởi `/scan-admin`, `/scan-system` và `/spec`.
> Khi component được scan → trạng thái chuyển sang ĐÃ SCAN.

## Registry

| Mã | Tên component | Tên JP | Mô tả | Trạng thái | Được dùng bởi |
|----|-------------|--------|-------|-----------|---------------|
| SC-001 | Template Message | 「テンプレート」 | Mẫu tin nhắn dùng chung trong broadcast, step delivery, greeting, chat | CHƯA SCAN | FA-001, FA-007, FA-008, FA-009, FA-010, FA-012 |
| SC-002 | Tag Selector | 「タグ」 | Component chọn/gán thẻ cho bạn bè, dùng để phân nhóm và lọc | CHƯA SCAN | FA-001, FA-008, FA-009, FA-012, FA-013 |
| SC-003 | Friend Filter/Segment | 「絞り込み」 | Bộ lọc bạn bè theo tag, thuộc tính, hành vi — dùng khi gửi tin, xem danh sách | CHƯA SCAN | FA-002, FA-008, FA-009, FA-013, FA-024 |
| SC-004 | Action Settings | 「アクション設定」 | Cấu hình hành động tự động (gắn tag, gửi tin, di chuyển step...) — dùng trong nhiều tính năng | CHƯA SCAN | FA-001, FA-003, FA-004, FA-007, FA-008, FA-009, FA-011, FA-012, FA-013, FA-015, FA-016, FA-017 |
| SC-005 | Rich Text / Message Editor | 「メッセージ編集」 | Soạn thảo nội dung tin nhắn (text, image, video, flex message) | CHƯA SCAN | FA-001, FA-007, FA-008, FA-009, FA-010 |
| SC-006 | Delivery Target Selector | 「配信先」 | Chọn đối tượng nhận tin — dùng trong broadcast, step, reminder | CHƯA SCAN | FA-008, FA-009, FA-022 |
| SC-007 | Schedule/Timer Settings | 「配信日時」 | Cài đặt thời gian gửi — dùng trong broadcast, step, reminder, action schedule, chat | CHƯA SCAN | FA-001, FA-008, FA-009, FA-016, FA-022 |

## Hướng dẫn
- Shared component = thành phần UI/logic xuất hiện ở nhiều tính năng khác nhau
- VD: Template (mẫu tin nhắn), Action (hành động tự động), Filter/Segment (bộ lọc), Tag (nhãn)
- Khi scan tính năng, nếu phát hiện dùng shared component → thêm vào đây
- Spec shared component lưu tại: `features/shared/{tên-component}/shared-spec.md`
- Danh sách trên được suy luận từ cấu trúc menu và tên tính năng — cần xác nhận khi chạy `/spec` cho từng tính năng
