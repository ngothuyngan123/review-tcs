# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-filled từ Redmine #40451 (Journal #140138) bằng `/new-task` lúc 2026-10-13.
>
> ⚠️ **Lệch format chuẩn 4 mục**: ticket này là **Feature mới** (không phải bug fix), nên Journal #140138 không viết theo cấu trúc 1.Nguyên nhân/2.Cách fix/3.Caller/4.1-4.3 mà theo cấu trúc riêng của Dev (■1 Chặn · ■2 Cảnh báo vùng lan · ■3 Việc bắt buộc khi deploy · ■4 Đề nghị QA hồi quy · ■5 Đã verify/chưa verify). Bên dưới là nội dung Journal được **tổng hợp lại** vào khung 4 mục cho khớp template — **đọc nguyên văn Journal #140138 trên Redmine để đối chiếu** nếu nghi ngờ sai lệch khi tổng hợp.
> ⚠️ Mục 4 (Đánh giá ảnh hưởng) có **bổ sung chéo** từ MCP LME TEST STUDIO task #364 (`task_get_context` → `dev_impact` + `requirements`, fetch cùng lúc ở BƯỚC 6b của `/new-task` để lấy TC) để đầy đủ hơn — các dòng lấy từ Studio được đánh dấu `[Studio #364]`. Phần còn lại lấy từ Journal #140138.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<chưa rõ>` — Redmine assignee ticket = **Kim Cúc**; người submit đánh giá ảnh hưởng (Journal #140138) = **Do Van Tu (TuDV)**. Cần hỏi lại ai là Dev code chính. |
| Commit / Pull Request | Không có link PR trong Redmine. Journal ghi: branch `ai-feature-41389` @ commit `a3741414cb` (gồm commit "add click" 10-01 và "enqueue" 10-02) |
| Branch | `ai-feature-41389` (ticket con `#41389` Spec Ads) — so với `origin/release_step_20260930` và `origin/release_step_20260930_v2` |
| Ngày submit đánh giá | 2026-10-05 (Journal #140138) |
| Auto-filled | 2026-10-13 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Journal #140138 trên Redmine + task #364 trên Studio và xác nhận tổng hợp bên dưới không sai lệch.

---

## 1. Nguyên nhân

⚠️ Không áp dụng theo nghĩa "root cause lỗi" — đây là **tính năng mới**. Tóm tắt mục đích/scope (từ description Redmine + `dev_impact` Studio):

- Cho phép Admin kết nối LINE OA với Google Ads / Meta Ads để tự động gửi conversion「友だち追加」(và các conversion khác qua action `広告コンバージョン`) phục vụ tối ưu chiến dịch quảng cáo.
- Quy mô thay đổi (theo Journal, so với `release_step_20260930_v2`): **15 commit · 132 file · +10335 / -3 dòng · 59 file mới · 73 file có sẵn bị chèn code · 10 migration**.
- Theo `spec_delta` Studio #364 (tính tại 2026-10-07, có thể lệch nhẹ do code đổi tiếp sau Journal 10-05): **150 file, +11766/-18**, 10 bảng/migration mới + 1 bảng có sẵn bị sửa (`t_actions_detail` thêm cột `bot_id`).
- Journal đánh giá Dev: phần chèn vào file có sẵn **gần như toàn bộ là code THÊM MỚI** — chỉ 2 dòng cũ bị sửa (gán giá trị trả về của `ActionLineUser::create` vào biến). Mọi nhánh logic mới tách riêng theo loại action `ad_api`.

## 2. Cách fix

⚠️ Đọc là "Cách triển khai" (implementation), không phải fix bug:

- Hook `AdsConversionEnqueueService` vào `sendAction()` — hàm thực thi action dùng chung (`app/Helpers/functions.php` + `HelperService.php`). Action không có `ad_api` → không thêm query, không ảnh hưởng hiệu năng. Action có `ad_api` → chỉ xếp vào `ads_conversion_queue` khi bạn bè có click id còn hạn VÀ bot có kết nối dùng được; gửi thật sang Google/Meta do **job Java** đảm nhận (hợp đồng ở `.claude/docs/ads-job-handoff.md`).
- Bắt click quảng cáo (`gclid`/`gbraid`/`wbraid`/`fbclid`) ở **7 luồng end-user**: `LiffController` (thêm bạn qua landing), `AppBookingCalendar`, `Mobile/CalendarController`, `Mobile/CalendarSalonController`, `SalesStripePaymentController`, `SalesManagementV2Controller` (Univapay), `FormAnswerService`. `capture()` tự nuốt lỗi, không ném ra ngoài.
- Thêm loại action mới `ad_api` vào hệ thống アクション dùng chung (`Actions.php`, `ActionDetail.php`, `ActionController`) — các loại action cũ không đổi hành vi (nhánh tách riêng theo `type == 'ad_api'`); ~45 blade preview action chỉ thêm `v-if="item.type == 'ad_api'"`.
- Màn mới `/basic/ads-setting` (OAuth Google/Meta, chọn đích, đồng bộ conversion, bật/tắt gửi, ngắt kết nối) + tab 送信ログ (log gửi). Menu `広告連携設定` thêm vào sidebar; quyền staff mới `広告連携` (nhóm 商品販売).
- **Quyết định cần chốt**: commit "enqueue" gỡ mã hoá Crypt khỏi model `AdsConnection` → access/refresh token Google/Meta lưu **plaintext** trong `ads_connections`, lệch Technical Spec §7 (quy định mã hoá). Ghi rõ trong `.claude/docs/ads-job-handoff.md` mục 9 (để job Java đọc token trực tiếp từ DB).
- 10 migration chỉ tạo bảng mới (`ads_connections`, `ads_conversions`, `ads_friend_clicks`, `ads_send_logs`, `ads_conversion_queue`, `ads_conversion_sent`) + 1 migration thêm cột `bot_id` cho `t_actions_detail` (idempotent). Riêng `2026_09_26_100100` **drop + tạo lại** `ads_send_logs` có PARTITION → mất data log trên môi trường đã chạy migration cũ (staging).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | Mô phỏng merge (`git merge-tree`) với cả 2 branch release | Không sửa code | Xác nhận merge base + xung đột giống nhau giữa 2 branch release song song |
| 2 | `php -l` toàn bộ file PHP của branch | Không sửa code | Đảm bảo syntax hợp lệ |
| 3 | check-php-calls (lời gọi method không tồn tại) | Không sửa code | Không phát hiện lời gọi method không tồn tại trong dòng branch thêm |
| 4 | Mọi method repository mà `AdsConversionEnqueueService` gọi | Không sửa code | Xác nhận method tồn tại đủ |
| 5 | Biến tại điểm chèn `sendAction()` | Không sửa code | Xác nhận không phát sinh Notice (biến truyền vào đã định nghĩa trước) |
| 6 | `node --check` các file JS bị sửa | Không sửa code | Syntax JS hợp lệ |
| 7 | check-blade-quotes (1441 view) | Không sửa code | Không lỗi quote trong blade |
| 8 | grep nơi gọi / nơi implement cho mọi file dùng chung | Không sửa code | Xác nhận không có caller bị bỏ sót |
| 9 | Job Java `linect-service` (đối chiếu snapshot 05-12) | Không sửa code | `ActionData` có `@JsonIgnoreProperties(ignoreUnknown = true)`, switch theo type không có default → `ad_api` bị bỏ qua êm, không hỏng action khác. **Cần team Java xác nhận lại trên code mới nhất** (chưa verify) |

⚠️ **Chưa verify** (Dev tự nêu): chạy runtime (container AI không có DB/Redis, không gọi ra Google/Meta được); code Java mới nhất.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `sendAction()` — hàm thực thi action dùng chung | `app/Helpers/functions.php`, `HelperService.php` | Direct | **Mọi action của mọi bot** (tag, シナリオ, テンプレート, 友だち情報, リッチメニュー…) đi qua đây. Nếu merge xung đột (xem F4) làm hỏng → hỏng toàn bộ hệ thống action, không riêng quảng cáo |
| F2 | 3 file xung đột merge dùng chung | `app/Exceptions/Handler.php`, `app/Providers/RepositoryServiceProvider.php`, `config/sns-line.php` | Direct | `#41389` và `#40041`/`#40044` cùng chèn 1 khối vào đúng 1 chỗ — giải xung đột sai 1 chỗ ⇒ hỏng toàn bộ. `RepositoryServiceProvider` phải còn đủ **6 binding** `AdsConnection`/`AdsConversion`/`AdsFriendClick`/`AdsSendLog`/`AdsActionDetail`/`AdsConversionQueue`; `Handler.php` khối `AdsApiException` phải đứng TRƯỚC nhánh ajax |
| F3 | 7 luồng end-user bắt click quảng cáo | `LiffController`, `AppBookingCalendar`, `Mobile/CalendarController`, `Mobile/CalendarSalonController`, `SalesStripePaymentController`, `SalesManagementV2Controller`, `FormAnswerService` | Indirect | Ở 2 luồng thanh toán, lời gọi capture nằm TRƯỚC bước trừ tiền nhưng không ném lỗi ra ngoài. Endpoint đặt lịch dùng bot_id + LINE uid client gửi; `captureByLineUid` tra theo `line_id` KHÔNG lọc bot ⇒ có thể ghi click giả cho cặp (bot, bạn bè) tuỳ ý (pattern cũ, nay dữ liệu được gửi ra ngoài Google/Meta) |
| F4 | Hệ thống アクション dùng chung — loại mới `ad_api` | `Actions.php`, `ActionDetail.php`, `ActionController`, ~45 blade preview, `modal_select_action.blade.php`, `select_action.js` | Direct | Nút 「広告コンバージョン」 hiện cho MỌI bot kể cả chưa liên kết; menu 「広告連携設定」 hiện cho mọi user — **cần PO/BA xác nhận ý đồ** |
| F5 | `AdApiActionNormalizer` | `app/Services/Ads/AdApiActionNormalizer.php` | Direct | Khi LƯU action chỉ ép kiểu `(int)` id conversion, **không kiểm id có thuộc bot không** (lệch ownership rule BE-coding-rules.md). Khi GỬI, enqueue tra bằng `findByIdForBot` (có lọc bot) nên không gửi nhầm bot khác — nhưng preview (`Actions.php`, `ActionDetail.php`) dùng `find()` không lọc bot nên có thể hiện tên conversion bot khác |
| F6 | `routes/web.php` | 20 route mới dưới prefix `ads-setting` | Direct (nhẹ) | Route callback OAuth thiếu middleware `is_expire` (các route ads khác có) |
| F7 | `[Studio #364]` Modal chọn action + 7 điểm khởi phát cho phép (`BR-10-02/03`) | — | Direct | Chỉ フォーム/商品/イベント/サロン予約/レッスン予約/QRコード/あいさつメッセージ được thêm action quảng cáo; điểm khác bị khoá nút; nếu block đã có sẵn ở điểm không cho phép → cảnh báo, lưu thì block bị bỏ |
| F8 | Job Java `linect-service` | `ActionData` (có `@JsonIgnoreProperties`) | Indirect | Chưa verify trên code Java mới nhất (xem mục 3) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `ads_connections` (gồm `access_token`/`refresh_token`) | CREATE | **Token lưu plaintext**, không mã hoá Crypt (lệch Technical Spec §7) — cần PO/BA/security chốt rủi ro |
| D2 | `ads_conversions` | CREATE | Conversion đồng bộ từ Google / custom + standard Meta |
| D3 | `ads_friend_clicks` | CREATE | Click id quảng cáo (gclid/gbraid/wbraid/fbclid), có hạn (Google 90 ngày / Meta 7 ngày theo `[Studio #364]` REQ-014) |
| D4 | `ads_send_logs` | DROP rồi CREATE lại (PARTITION theo tháng + `pmax`) | **Mất dữ liệu log** trên môi trường đã chạy migration cũ (staging). Cần job thêm partition hàng tháng |
| D5 | `ads_conversion_queue` | CREATE | Hàng đợi gửi job Java |
| D6 | `ads_conversion_sent` | CREATE | `[Studio #364]` Chống gửi trùng — theo QA đã xác nhận (08/10): **không bao giờ xoá**, không áp hạn 3 tháng/click TTL |
| D7 | `t_actions_detail.bot_id` | UPDATE (thêm cột) | Idempotent — production đã có cột ⇒ migration không làm gì |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Mọi action hiện có (tag, シナリオ, テンプレート, 友だち情報, リッチメニュー) chạy từ step/broadcast/đặt lịch/form | F1, F2 | **High** — nếu binding/exception merge sai |
| T2 | 7 luồng end-user: thêm bạn landing/QR, đặt lịch (booking_news/salon/app booking), thanh toán (Stripe/Univapay), mở form LIFF | F3 | Medium |
| T3 | Modal chọn action dùng chung + preview (step message, broadcast, rich menu, tag, QR, calendar...) | F4, F5 | Medium |
| T4 | Sao chép / backup bot (`BackupBotTask` Java, `Recover*` PHP) có action `広告コンバージョン` | D1-D6 | Medium — copy nguyên data `ad_api` kèm id conversion bot GỐC; sang bot khác thì action vô hiệu (enqueue lọc bot) nhưng preview vẫn hiện tên conversion bot gốc |
| T5 | `[Studio #364]` Màn あいさつメッセージ (tin nhắn chào mới) — thêm URL đo lường + QR + ghi chú | REQ-020 | **High** — `dev_impact` Studio ghi: route công khai `/fl/{hashBotId}` lệch cơ chế landing-qr tech spec §0.3; đổi ô URL/QR sang link `/fl` trái **D-48=C** (giữ URL LINE gốc) — cần xác nhận lại với PO/BA |
| T6 | `[Studio #364]` Phân quyền staff — mục mới `広告連携` (nhóm 商品販売) | REQ-002 | High — mặc định chỉ 副管理人; migration bật quyền cho 副管理人 hiện hữu; cần kiểm lại command `recover:ads_setting_permission` |
| T7 | Deploy: `config('sns-line.version')` chưa bump trong branch, nhưng JS/CSS đã đổi (`select_action.js`, JS đặt lịch/mua hàng, CSS `ads_setting`) | Journal ■3.1 | Medium — không bump thì browser giữ JS cũ, bấm 「広告コンバージョン」 lỗi. **Việc bắt buộc khi deploy, không phải TC**, nhưng Leader nên biết |
| T8 | Meta app ở Development mode (chưa Business Verification + App Review + Publish) | Journal ■3.3 | Low/Medium — khách ngoài chưa liên kết được cho tới khi publish |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

⚠️ **2 điểm BLOCKED theo Journal, cần PO/BA/security chốt trước khi review TC coverage đầy đủ**:
1. Token OAuth lưu plaintext (D1) — lệch Technical Spec §7.
2. 3 xung đột merge dùng chung (F2) — ảnh hưởng toàn hệ thống action nếu giải sai.
