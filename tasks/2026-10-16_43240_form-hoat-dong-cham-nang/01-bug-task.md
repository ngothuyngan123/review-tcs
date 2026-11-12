# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #43240 bằng `/new-task` (REST API, `scripts/redmine_fetch.py`) — 2026-10-16.
> ⚠️ Ticket **KHÔNG có section "Tái hiện bug"** — khách hàng chỉ complain chung "form nặng/chậm", không có steps cụ thể trong Redmine. Root cause được Dev **tự điều tra và xác nhận** qua 3 Journal "Dev Studio" (không theo format 4-mục chuẩn) — xem `03-dev-impact.md` (có cảnh báo riêng về format).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43240 — [16-10-2026] [TY-12429] [Form] Form hoạt động chậm/nặng, khách hỏi nguyên nhân` |
| Module / Màn hình | Modal 「アクション」 — tab 「タグ」 (Studio feature tag: `action-settings`). Là component **dùng chung bởi ~40 màn** include modal này: Form v3 (nơi khách phát hiện), Rich menu, Kịch bản/step, Auto reply, màn quản lý タグ, Friend info... |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine đã ở tiếng Việt (OEM báo qua Slack), paste nguyên văn phần nội dung hỏi, bỏ khối "原文 (JP)" trùng lặp. -->

Mã quản lý：TY-12429
Địa chỉ：shu.hosono@gmail.com
Tên LOA：アレルバランス｜HCL【公式】
Người phụ trách：沖原
Công cụ：リンク

Nội dung hỏi:
Hành vi của form có vẻ nặng/chậm nói chung.
Xin hãy cho biết lý do của việc này.
https://www.loom.com/share/b2c434afc3ab4e2d8a1f95ae14e7de0e

> Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ). Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1792108520887359 — Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12429

## Steps to reproduce

<!-- Không có trong Redmine — khách chỉ complain chung, kèm video Loom (link ở trên). Theo note của TC Studio NEW-1: "video Loom/ảnh không xem được nên kịch bản lấy theo phân tích của Dev (tab タグ)" — xem file 04. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video (chỉ có **link** Loom trong description, không phải attachment Redmine, và theo note Studio — không xem được)
- [ ] Có log / request-response

Attachments (1):
- screenshot1.png — https://redmine.melonglobal.net/attachments/download/34089/screenshot1.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev confirm qua điều tra chủ động (không phải theo steps khách cung cấp), xem `03-dev-impact.md`.
- **Root cause tóm tắt** (Journal #144707): API `/ajax/get-list-group-tag` (`TagController@ajaxGetListCategoryTag`) không phân trang khi modal 「アクション」 gọi → duyệt **mọi tag trong folder**; mỗi tag có アクション lại dựng chi tiết action để preview (chạy nhiều query/dòng) + mỗi dòng nạp lại toàn bộ tag 未分類 của bot — modal không dùng dữ liệu này. Từ commit `fixbug_37710` (21/07/2026) mỗi tag tốn thêm nhiều truy vấn → bot có **895 tag phải chờ 295 giây**.
- **Fix**: modal 「アクション」 tải tag qua API **mới, nhẹ, có phân trang** (`/ajax/get-data-for-tag-action`, tối đa 50 tag/lần) thay cho API cũ.
- **Phạm vi ảnh hưởng**: chỉ sửa JS dùng chung của modal 「アクション」 (git grep `modal_select_action` ra ~55 view) → mọi màn include modal này tải tag nhanh hơn. API cũ + màn quản lý タグ + các picker khác **giữ nguyên**, không đổi.
- **CSRF — cố ý KHÔNG sửa trong ticket này** (Journal #144901): middleware CSRF miễn kiểm tra toàn bộ `/ajax/*` từ trước ticket, nên API mới (và mọi API ajax khác) không kiểm CSRF token. API chỉ đọc, vẫn đòi phiên đăng nhập và chỉ trả tag của bot trong session → người phụ trách quyết định không fix. Nếu Leader/BA thấy đây là rủi ro bảo mật cần theo dõi riêng (ngoài phạm vi #43240).
- **3 bug tìm thấy lúc automation test KHÔNG phải lỗi sản phẩm** (Journal #144955, vòng 6): do kịch bản test đọc trang trước khi render xong hoặc tiền điều kiện sai (ở màn ticket không sửa); bug `category_id` là thay đổi có chủ đích của v6; bug lệch thứ tự tag chỉ xảy ra ở các tag **trùng `position`** — màn quản lý タグ không có tiêu chí sắp xếp phụ, modal giữ `position` giảm + `id` giảm giống API cũ.
- **Studio task #457** (feature `action-settings`, branch `ai_studio_fixbug_43240`): round 1, `aiResult=fail`, `reviewState=tester`, `openBugs=2`, 47 TC (44 pass / 1 fail / 2 skip chưa chạy), 100% toolWritten (AI viết, chưa có TC viết tay). **Toàn bộ 47 TC chỉ chạy ở env `local`** (0 TC trên staging/prd) — xem cảnh báo RULE-08 ở file 04.
  - TC fail: `NEW-17` — "API tải tag cho modal アクション — phân trang 50 tag/trang..." (gắn ticket bug #43345).
  - TC skip/chưa chạy: `NEW-32` (verify JS mới nhận sau release không cần hard-reload) và `NEW-25` (regression Rich menu v2).
  - 8 TC khác đang gắn **5 ticket bug con** mở trong lúc test round này: #43316, #43317 (x4 TC), #43343, #43344, #43345 — Leader cần tra các ticket con này (có thể đã resolve ở round sau, Redmine #43240 chưa phản ánh).
- Không có `bot_id` / `line_user_id` cụ thể của khách TY-12429 trong Redmine — chỉ biết đặc điểm "bot nhiều tag" (quy mô tham chiếu: 895 tag → 295s) từ phân tích Dev, KHÔNG phải số liệu đo trên bot thật của khách.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Mã quản lý (OEM) | TY-12429 |
| LOA / khách hàng | アレルバランス｜HCL【公式】 |
| Người phụ trách CS | 沖原 |
| bot_id | `<không có trong Redmine>` |
| Đặc điểm bot gây chậm | Theo phân tích Dev: bot có **~895 tag** → modal 「アクション」 tải tag cũ mất **~295 giây** (không phải số đo trên bot thật của khách TY-12429) |
| Đối chứng | `<không có — khách không cung cấp video/log xem được>` |

## Journal / note từ Redmine (nguyên văn)

<!-- Bỏ qua Journal #144663 / #144664 — chỉ là phản hồi CS "đang kiểm tra, mong đợi thêm", không có nội dung điều tra. -->

**Journal #144707 — Dev Studio — 2026-10-16:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
API /ajax/get-list-group-tag (TagController@ajaxGetListCategoryTag) không phân trang khi modal アクション gọi, nên duyệt mọi tag trong folder. Với mỗi tag có action, API dựng lại chi tiết action để xem trước: chạy nhiều truy vấn cho từng dòng action, và mỗi dòng lại nạp toàn bộ tag 未分類 của bot. Modal không dùng dữ liệu này. Từ commit fixbug_37710 (21/07/2026), mỗi tag tốn thêm nhiều truy vấn, nên bot 895 tag phải chờ 295 giây.

Hướng sửa:
- D-1 Modal アクション tải tag qua API nhẹ có sẵn

Ảnh hưởng / rủi ro:
Chỉ sửa JS của modal アクション dùng chung (khoảng 40 màn include), nên mọi màn này cùng tải tag nhanh hơn. API cũ, màn quản lý tag và các picker khác giữ nguyên. Cần kiểm modal ở vài màn và kiểm modal lọc vẫn hoạt động (cùng dùng API nhẹ).
```

**Journal #144901 — Dev Studio — 2026-10-16:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Middleware CSRF của app miễn kiểm tra cho toàn bộ đường dẫn /ajax/* từ trước ticket, nên API mới cũng như mọi API ajax khác không kiểm CSRF token. API chỉ đọc, vẫn đòi phiên đăng nhập và chỉ trả tag của bot trong session, nên người phụ trách đã quyết định không sửa trong ticket này.

Ảnh hưởng / rủi ro:
Không có thay đổi code ở vòng này; bản đã giao ở vòng 3 giữ nguyên.
```

**Journal #144955 — Dev Studio — 2026-10-16:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Không có lỗi sản phẩm mới. Ba bug do kịch bản đọc trang trước khi render xong hoặc tiền điều kiện sai, ở các màn mà ticket không sửa. Bug về category_id là thay đổi có chủ đích của v6. Bug thứ tự chỉ lệch ở các tag trùng position: màn quản lý tag không có tiêu chí sắp xếp phụ, còn modal giữ thứ tự position giảm, id giảm như API cũ.

Ảnh hưởng / rủi ro:
Không có thay đổi code ở vòng này; bản đã giao ở vòng 6 giữ nguyên.
```
