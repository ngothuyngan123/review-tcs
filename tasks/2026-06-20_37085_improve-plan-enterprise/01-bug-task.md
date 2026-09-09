# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#37085 — Improve plan enterprise` |
| Redmine URL | https://redmine.watermelon.vn/issues/37085 |
| Auto-filled | `2026-06-20 by /new-task` |
| Ngày báo cáo | `2026-06-04` |
| Khách hàng / PM báo | `Ngọc Ánh` |
| Module / Màn hình | `<chưa rõ — tester fill>` (liên quan: Quản lý hợp đồng / Plan enterprise / kết nối LOA) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Tên gốc: おまとめプランからLINE公式アカウントを接続する場合の仕様修正
1.Chỉ owner おまとめプラン mới có thể thao tác với các slot chưa kết nối của plan enterprise.
※ Button おまとめ割引の契約を変更する chỉ được hiển thị cho owner plan enterprise.
2. Không hiển thị mục lựa chọn owner (主管理者) trên màn hình kết nối LOA của plan enterprise.
3. Sửa phần nội dung hiển thị tên LOA của plan enterprise => おまとめ割引.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments (Redmine #37085):
- https://redmine.watermelon.vn/attachments/download/26347/____________________________2026-06-04_17.45.06.png
- https://redmine.watermelon.vn/attachments/download/26349/loa___________________________.png
- https://redmine.watermelon.vn/attachments/download/26350/____________________________2026-06-04_17.46.29.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

⚠️ Đây là **task spec/feature** (tracker = Feature), KHÔNG phải bug tái hiện — Redmine không có Section "Tái hiện bug" nên Steps/Expected/Actual để trống. TCs nên tập trung verify đúng spec mới (owner-only thao tác plan enterprise) + regression với standard/pro.

Tài liệu tham chiếu (từ Redmine journals):
- Design (Figma): https://www.figma.com/design/enai7WD4z5CPzyUrcN61xQ/01-09-%E5%A5%91%E7%B4%84%E7%AE%A1%E7%90%86?node-id=213-6522
- Thảo luận (Slack): https://l-message.slack.com/archives/C08DACWUDMM/p1780562693787309?thread_ts=1780472912.533349&cid=C08DACWUDMM
