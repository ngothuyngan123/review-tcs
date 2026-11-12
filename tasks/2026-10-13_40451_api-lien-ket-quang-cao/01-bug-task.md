# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #40451 bằng `/new-task` lúc 2026-10-13.
>
> ⚠️ Ticket này có **Tracker: Feature** (không phải Bug) — không có section "Tái hiện bug" trong Redmine. Các section Steps/Expected/Actual bên dưới để trống vì không áp dụng. Phần "Đánh giá ảnh hưởng" (rất chi tiết) nằm ở Journal #140138, đã chuyển sang `03-dev-impact.md`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40451 — API liên kết quảng cáo` |
| Module / Màn hình | `<chưa rõ — Redmine không gán category>`. Suy từ description: màn mới **広告連携設定** (Ads Setting) ở menu trái + khối action mới **広告コンバージョン** (Ad conversion) trong modal chọn action dùng chung + sửa màn tin nhắn chào mừng bạn mới (あいさつメッセージ 新規) |

## Mô tả bug (bản dịch tiếng Việt)

Tên gốc: 広告API連携 (Liên kết API quảng cáo)

Cho phép Admin kết nối LINE OA với các nền tảng (媒体) quảng cáo (Google 広告, Meta 広告) để tự động gửi sự kiện「友だち追加」(thêm bạn) như một conversion outbound về nền tảng quảng cáo, phục vụ tối ưu chiến dịch.

- Link design html: https://docs.missiona.co/product_lme/ad-platform-settings/
- Tài khoản login html: `missiona58174` / `Vk3mPwRn7xQe`
- Link prototype: https://github.com/missiona-inc/prototype-lme/blob/main/ad-platform-settings/index.html

Thêm phần setting liên kết quảng cáo vào menu trái, phía dưới phần đổi bot (change bot).
- Link design html: https://docs.missiona.co/product_lme/sidemenu.html
- Link git: https://github.com/missiona-inc/prototype-lme/blob/main/sidemenu.html
- Link task: https://missiona-tools.vercel.app/lme-dev/tickets/e91c98ad-eab1-4592-a866-a786ca97056c

Sửa thêm design màn tin nhắn chào mừng bạn mới (new friend):
- Thêm dòng chú thích cho phần 通常の友だち追加URL (URL thêm bạn thông thường): 「LINE公式アカウント管理画面で取得できる友だち追加URLと違いはありません。エルメ接続後も、それぞれの友だち追加URLは引き続き利用が可能です。」(Không khác URL thêm bạn lấy từ màn quản trị LINE OA chính thức. Sau khi liên kết エルメ, mỗi URL thêm bạn vẫn tiếp tục dùng được như trước.)
- Thêm phần 広告API連携用友だち追加URL (URL thêm bạn dùng cho liên kết API quảng cáo) phía dưới URL thêm bạn thông thường, kèm dòng chú thích: 「広告API連携を稼働させるには、上記の友だち追加URLを広告に設定してください。通常の友だち追加URLから追加された友だちには、広告API連携のコンバージョンが発火しません。」(Để vận hành liên kết API quảng cáo, hãy đặt URL thêm bạn nêu trên vào quảng cáo. Bạn bè thêm qua URL thêm bạn thông thường sẽ không phát sinh conversion của liên kết API quảng cáo.)
- Design gốc: https://xd.adobe.com/view/22061b55-bb8f-41c2-a520-26c3f1b05607-7755/
- Design clone: https://www.figma.com/design/eO25tRJu8LwAyt0Xr8VokV/追加修正_-Tin-nhắn-chào-mừng?node-id=0-1&p=f&t=aqXFzUNYhuIXNJOd-0

## Steps to reproduce

<!-- Không áp dụng — ticket Feature, không có bug cụ thể cần tái hiện. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40451 không có attachment (0). -->

## Ghi chú thêm của Leader

⚠️ Ticket Redmine vẫn ở status **New** (chưa Resolved/Closed) — theo **RULE-11** của `framework/checklist-lme.md`, trạng thái này KHÔNG phải bằng chứng hợp lệ để flag `[BLOCKER]`/`[MAJOR]` dựa trên "chưa đủ bằng chứng", nhưng cũng có nghĩa Dev/PO có thể còn đang sửa — Tester cần đối chiếu lại trạng thái mới nhất trên Redmine trước khi review.

⚠️ Ticket con `#41389` (Spec Ads) là nguồn chứa Technical Spec đầy đủ — Redmine #40451 không có link trực tiếp tới spec chi tiết, chỉ có đánh giá ảnh hưởng dev ở Journal #140138 tham chiếu `#41389`.

⚠️ **MCP LME TEST STUDIO đã có task #364 cho ticket này, round 5, status `tc-ready`, 208 TC, đã chạy** (xem `04-tc-list.md`) — tiến độ Studio đã đi trước nhiều so với trạng thái "New" trên Redmine. Dùng Studio làm nguồn TC chính khi review.

Tài khoản demo login html design (không phải account LME): `missiona58174` / `Vk3mPwRn7xQe` — không dùng để test thật trên LME, chỉ để xem design.

## Dữ liệu định danh ca lỗi

<!-- Không áp dụng — ticket Feature, không có ca lỗi cụ thể để dựng env. Dữ liệu định danh env test (bot_id mẫu, flag GOOGLE_*/META_*,...) xem `03-dev-impact.md` + `.claude/docs/ads-setup.md` (Dev note trong journal). -->
