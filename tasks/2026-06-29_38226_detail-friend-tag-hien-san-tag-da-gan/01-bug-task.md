# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #38226 bằng `/new-task`. Tester verify lại rồi tick checkbox bên dưới.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38226 — [Detail friend][Tag] Friend đang có tag được gắn thì mong muốn hiển thị sẵn các tag đang được gắn ngay từ đầu, không cần phải click vào tên folder để mở ra mới xem được` |
| Redmine URL | https://redmine.watermelon.vn/issues/38226 |
| Auto-filled | `2026-06-29 by /new-task` |
| Ngày báo cáo | `2026-06-26` |
| Khách hàng / PM báo | `Ngọc Ánh` |
| Module / Màn hình | `Detail friend / tab Tag (/basic/friendlist/my_page)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

Tracker: **SpecImprove** — parent #36376.

Description (Redmine):
https://l-message.slack.com/archives/C08DACWUDMM/p1782447890959379?thread_ts=1782184213.062539&cid=C08DACWUDMM

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Từ journal "Tái hiện" của Hạnh Nguyễn (2026-06-27) -->

1. Mở màn **Detail friend** (`/basic/friendlist/my_page`) của 1 friend đang có tag được gắn.
2. Bấm sang **tab Tag** (現在ついているタグ).
3. Quan sát danh sách folder chứa tag ngay khi vừa load.

## Expected result

- Các folder chứa tag được gắn cho friend **hiển thị được xổ sẵn (mở dropdown) ngay từ đầu**, không cần click vào tên folder mới xem được tag bên trong.

## Actual result

- Các folder có chứa tag bên trong tại detail friend tab tag **không được xổ sẵn**, vẫn đang trong trạng thái đóng dropdown → phải click tên folder mới mở ra xem được.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/27590/snapcrab_noname_2026-6-24_15-5-18_no-00.png

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- Đây là ticket **SpecImprove** (cải tiến UX hiển thị), không phải bug lỗi nghiệp vụ. Fix thuần frontend JS (xem file 03).
