# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine bằng `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee ticket: `Ngô Thúy Ngần` (QA) |
| Commit / Pull Request | repo `sns-line` · commit `4a2c301858` (4 file) · đã push. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=39372 |
| Branch | `ai_fixbug_39372` (nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-08-07` (journal Redmine 2026-08-07T08:00:51Z — bản chốt) |
| Auto-filled | `2026-08-08 by /new-task` |

> ⚠️ **Có 2 vòng báo cáo Auto-fixbug trên Redmine #39372**:
> - Vòng 1 — `2026-08-06`, commit `6f2cf54301`, **3 file**, thuộc tính badge đặt tên là `data-badge-menu`.
> - Vòng 2 — `2026-08-07`, commit `4a2c301858`, **4 file**, đổi tên thuộc tính thành **`data-badge-route`** + bổ sung 2 thay đổi mới (đồng bộ chấm đỏ sidebar thu gọn, dọn nguồn dữ liệu màn テンプレート).
>
> **File này chép nguyên văn vòng 2 (bản chốt).** Nếu QA checkout branch thấy `data-badge-menu` thay vì `data-badge-route` ⇒ đang ở commit cũ, hỏi lại Dev.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN — báo cáo Auto-fixbug 2026-08-07 -->

Badge cạnh menu "送信エラー" bị JS của màn chat 1:1 GHI ĐÈ bằng số hội thoại chưa đọc — con số trên badge không hề lấy từ dữ liệu lỗi gửi tin. Hàm setBadge (public/js/chats/chat-v2.js:5835) quét document.querySelectorAll('.badge-span') rồi gán CÙNG một con số cho MỌI phần tử khớp, đồng thời bật/tắt class hidden. Con số đó là số hội thoại chưa đọc, lấy từ socket khi có tin đến (chat-v2.js:334) và từ /ajax/get-badge (:367, :2750, :4155). Trong khi đó sidebar bản mới (resources/views/layout/v2/basic/sidebar.blade.php) gắn class .badge-span cho TẤT CẢ badge menu — gồm cả badge 送信エラー (dòng 214) và badge ở danh sách menu yêu thích (dòng 146) — chứ không riêng badge chat. Màn chat lại dùng chung layout với sidebar này (layout/basic/main.blade.php:16 include layout.v2.basic.sidebar, còn basic/chat/index.blade.php:173 nạp chat-v2.js), nên mỗi khi bạn bè gửi tin tới, badge 送信エラー nhảy lên đúng bằng số tin chưa đọc và tăng dần theo. Khi khách bấm vào xem thì trang tải lại, badge được server render lại từ totalErrorMessage (= 0) và danh sách trống — đúng hiện tượng khách mô tả: badge báo lỗi tăng theo số tin chưa đọc nhưng mở ra không có nội dung lỗi nào.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX — báo cáo Auto-fixbug 2026-08-07 -->

Sửa tận gốc cơ chế cập nhật badge sidebar, thay vì vá theo điều kiện.

1) ĐẶT TÊN RIÊNG CHO TỪNG BADGE: mỗi badge menu nay mang tên của chính menu đó qua thuộc tính data-badge-route (= tên route, vd chatBasicV3 / errorListV2). Áp cho toàn bộ 6 chỗ render badge ở 2 sidebar CÒN SỐNG: resources/views/layout/v2/basic/sidebar.blade.php (4 chỗ — menu yêu thích bind :data-badge-route="fmenu.route", 3 nhánh menu chính dùng data-badge-route="{{ $key }}") và resources/views/layout/admin_v2/sidebar.blade.php (2 chỗ badge chat 1:1). Thay đổi ở blade là THUẦN THÊM thuộc tính — giữ nguyên class .badge-span cũ, không gỡ gì, nên không ảnh hưởng bất kỳ chỗ nào khác có thể đang bám vào class đó.

2) setBadge NEO THEO TÊN MENU CHAT: public/js/chats/chat-v2.js chỉ chọn [data-badge-route="chatBasicV3"] thay vì quét class dùng chung .badge-span. Nhờ vậy số chưa đọc của chat về mặt CẤU TRÚC không thể ghi vào badge menu khác, kể cả badge của menu thêm mới sau này. Tên thuộc tính đặt trùng nhánh ai_small_38691 (chưa merge, cùng mục đích) để repo không phát sinh 2 quy ước song song.

3) ĐỒNG BỘ CHẤM ĐỎ KHI THU GỌN SIDEBAR: setBadge nay cập nhật thêm class badge-item trên .layout-v2-menu-item cha — đây mới là thứ vẽ chấm đỏ lúc sidebar thu gọn (.collapsed .badge-item:before, public/css/layout-v2.css:698). Trước đây Blade set class này lúc render nhưng không ai cập nhật khi số badge đổi, nên chấm đỏ sai trạng thái.

4) DỌN NGUỒN DỮ LIỆU Ở MÀN テンプレート: public/js/msg_template/index.js addGroup() lấy group_id từ state Vue self.id_group thay vì $('.active').attr('data-id'). Truy vấn DOM đó quét toàn trang nên lấy trúng tab 利用規約 của popup trong header (luôn render, đứng trước nội dung trang) và trả undefined. self.id_group chính là giá trị đang gán cho data.id ngay dòng dưới, và controller MessageTemplateController@ajaxInitTemplate case 'addAndEditGroup' (dòng 2825) vốn chỉ đọc $request->id + group_name nên hành vi server không đổi — đây là dọn đúng nguồn dữ liệu, không phải đổi logic.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN — convert list plain sang bảng, giữ nguyên chữ của Dev. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `setBadge` (public/js/chats/chat-v2.js:5835) | **CÓ SỬA** — đổi bộ chọn | ĐIỂM GHI ĐÈ: querySelectorAll('.badge-span') gán cùng 1 số cho mọi badge |
| 2 | 4 nơi gọi setBadge (chat-v2.js:334 socket có tin đến, :367 / :2750 / :4155 từ /ajax/get-badge) | Không sửa | Nguồn số đều là số chưa đọc |
| 3 | resources/views/layout/v2/basic/sidebar.blade.php — 4 chỗ render badge: :146 menu yêu thích (Vue bind), :172 badge chat, :185 nhánh menu-có-submenu (hiện không menu nào khai báo badge), :214 badge 送信エラー | **CÓ SỬA** — thêm `data-badge-route` | Đặt tên riêng cho từng badge |
| 4 | resources/views/layout/admin_v2/sidebar.blade.php:424, :772 — 2 badge chat 1:1 | **CÓ SỬA** — thêm `data-badge-route` | 2 badge chat 1:1 cũng mang .badge-span |
| 5 | layout/basic/main.blade.php:16 | Không sửa | Layout của màn chat include đúng sidebar v2 (nên badge lỗi nằm chung trang với JS chat) |
| 6 | basic/chat/index.blade.php:173 | Không sửa | Nạp chat-v2.js |
| 7 | `totalErrorMessage` (app/Helpers/functions.php:4102) | **GIỮ NGUYÊN** (đã revert hướng fix sai vòng trước) | Nguồn số badge server render: ĐÃ ĐỐI CHIẾU, KHÔNG sai |
| 8 | `MessageErrorController::ajaxGetMessageError` (:157) | **GIỮ NGUYÊN** (đã revert) | Bộ lọc màn danh sách lỗi |
| 9 | public/css/layout-v2.css:695-706 — `.badge-item` / `.collapsed .badge-item:before` | Không sửa CSS (JS nay cập nhật class) | Chấm đỏ khi thu gọn sidebar |
| 10 | msg_template/index.js `addGroup` (:659) + `editGroup` (:677 đặt self.id_group) + MessageTemplateController@ajaxInitTemplate case addAndEditGroup (:2825) | **CÓ SỬA** — addGroup lấy id từ state Vue | Dọn nguồn dữ liệu, hành vi server không đổi |
| 11 | layout/basic/header.blade.php:1389 — `.term-tab.active` | Không sửa | Gây nhiễu `$('.active')` (xem mục Quét ngang) |
| 12 | CSS: grep `.badge-span` trong public/css, public/_assets, resources/assets, public/lme-ui/src/css | Không có | KHÔNG có khai báo style nào (thuần hook JS) |
| 13 | Sidebar cũ layout/basic\|admin/sidebar.blade.php | Không đụng | Không được @include ở đâu, màn chết |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn "■ 4.1 File thay đổi" — Dev liệt kê theo FILE, không theo function. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `setBadge()` — cập nhật badge sidebar từ JS chat | `public/js/chats/chat-v2.js` | Direct | Đổi bộ chọn `.badge-span` → `[data-badge-route="chatBasicV3"]`; thêm cập nhật class `badge-item` trên `.layout-v2-menu-item` cha |
| F2 | Render badge sidebar người dùng (4 chỗ: menu yêu thích, badge chat, nhánh có submenu, badge 送信エラー) | `resources/views/layout/v2/basic/sidebar.blade.php` | Direct | Thuần THÊM thuộc tính `data-badge-route`, giữ nguyên class `.badge-span` |
| F3 | Render badge chat 1:1 trên sidebar quản trị (2 chỗ: :424, :772) | `resources/views/layout/admin_v2/sidebar.blade.php` | Direct | Thuần THÊM thuộc tính `data-badge-route="chatBasicV3"` |
| F4 | `addGroup()` — thêm/đổi tên thư mục màn テンプレート | `public/js/msg_template/index.js` | Direct | Lấy `group_id` từ state Vue `self.id_group` thay vì `$('.active').attr('data-id')`; controller không đổi |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn "■ 4.2 Data ảnh hưởng" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Chỉ thêm thuộc tính HTML trên badge và đổi bộ chọn phần tử trong JS; không đọc/ghi bảng nào |
| — | Recover data | — | ✔ Không cần recover data |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn "■ 4.3 Tính năng liên quan" -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Delivery Error List (FA-028)** — badge 送信エラー trên sidebar không còn bị số chưa đọc của chat ghi đè, giữ đúng số lỗi thật do server render | F1, F2 | High |
| T2 | **Chat 1:1 (FA-001)** — badge số hội thoại chưa đọc của menu 1:1チャット vẫn cập nhật realtime như cũ, trên CẢ sidebar người dùng (layout/v2/basic) lẫn sidebar quản trị (layout/admin_v2), gồm cả khi menu được ghim vào お気に入り | F1, F2, F3 | High |
| T3 | **Sidebar / menu お気に入り** — badge của mọi menu khác (hiện có và thêm mới sau này) an toàn theo cấu trúc vì mỗi badge mang tên riêng, không còn dùng chung điểm móc | F1, F2 | Medium |
| T4 | **Sidebar thu gọn** — chấm đỏ (`badge-item`) trên menu 1:1チャット nay đồng bộ đúng khi số chưa đọc thay đổi, trước đây chỉ đúng lúc tải trang | F1 | Medium |
| T5 | **Message Template (テンプレート)** — thao tác Thêm/Đổi tên thư mục lấy id thư mục từ state Vue thay vì truy vấn DOM; hành vi server không đổi vì controller vốn chỉ dùng `$request->id` | F4 | Medium |

---

## 5. Verify của Dev + Rủi ro tự nêu (nguyên văn — dùng để dựng TC)

### Mức verify: **lint** (KHÔNG có verify runtime trên trình duyệt)

`node --check public/js/chats/chat-v2.js`: OK; `node --check public/js/msg_template/index.js`: OK; Compile 2 blade sidebar bằng chính BladeCompiler của Laravel rồi `php -l` file compile: OK cả 2; Kiểm output compile: đủ 6 badge đều có `data-badge-route` VÀ vẫn giữ class `badge-span` (v2/basic :146 bind theo fmenu.route, :172/:185/:214 theo `$key`; admin_v2 :424/:772 = `chatBasicV3`); Đối chiếu tên route dùng làm tên badge: menu chat trong `$sections` có key `'chatBasicV3'`, `favBadgeMap` cũng khoá theo `'chatBasicV3'`, `toggleFavourite` lưu route bằng chính `$key` ⇒ `fmenu.route` của menu chat = `'chatBasicV3'`, khớp bộ chọn của setBadge; `git merge` thử lên `origin/release_step_20260805`: exit 0, KHÔNG xung đột; `git merge-base --is-ancestor origin/ai_fixbug_39372 HEAD`: CÓ; `git diff --stat release_step_20260623...HEAD`: 4 file, 20 thêm / 10 bớt; PHPUnit: fix nằm ở view blade + JS, không thuộc app/Services|app/Helpers, không có test liên quan.

**QUÉT NGANG cùng họ lỗi trên toàn repo** (JS ghi đè phần tử qua selector dùng chung): 84 chỗ dùng `querySelectorAll` theo class, chỉ 4 chỗ có ghi giá trị, và DUY NHẤT `setBadge` ghi ở phạm vi `document`; 2 chỗ còn lại (`booking_news/booking.js:1410`, `calendar_salon/booking.js:1932`) giới hạn trong `info.el` của FullCalendar nên an toàn. Cũng đã rà 15 hook đếm/badge của sidebar+header: chỉ `.badge-span` bị script cấp trang ghi vào.

⚠️ **CHƯA chạy được kiểm chứng trên trình duyệt**: DB dev `host.docker.internal:3306` trả Connection refused nên không đăng nhập/gửi tin thử được; kết luận dựa trên đối chiếu code đầy đủ từ điểm ghi đè tới điểm render.

### Rủi ro / lưu ý khi test (Dev tự nêu — nguyên văn)

- Nếu sau này thêm sidebar/badge mới mà quên gắn `data-badge-route` thì badge đó sẽ không được cập nhật realtime (im lặng). An toàn hơn hẳn trạng thái cũ (badge lạ bị ghi số sai), nhưng cần dev nhớ quy ước khi thêm menu có badge
- Badge 送信エラー nay **chỉ cập nhật khi tải lại trang** (server render). Trước đây nó có 'cập nhật realtime' nhưng bằng con số SAI nên không phải mất tính năng; muốn realtime thật thì dùng trường `totalErrorMessage` sẵn có của InfoEvent — hiện KHÔNG có JS nào lắng nghe event này (code chết), nên phải tách ticket riêng
- Badge ở mục お気に入り nằm dưới `v-if="favBadge(...) > 0"` và `favBadgeMap` là dữ liệu tĩnh server render: nếu lúc tải trang số chưa đọc = 0 thì phần tử badge không tồn tại, có tin mới đến sẽ chưa hiện cho tới khi tải lại trang. Đây là hành vi **CÓ SẴN từ trước**, không phải hồi quy của fix này; nhánh `ai_small_38691` đã có cách xử lý đúng bằng Vue `$set(favBadgeMap, ...)`
- Nhánh `ai_small_38691` (chưa merge) cũng thêm `data-badge-route` cho 3 badge menu chính nhưng KHÔNG sửa `setBadge` và KHÔNG gắn cho badge yêu thích — khi merge cần rà lại để không trùng lặp/thiếu
- Chưa chạy thử được trên trình duyệt do DB dev không kết nối được; cần QA verify theo bước tái hiện đã ghi

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
