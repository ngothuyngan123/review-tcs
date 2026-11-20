# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ Ticket này fix qua **9 vòng lặp (round 1 → round 9, tag D-1 → D-15)** vì hệ thống tự detect + QA tiếp tục bắt case mới trong lúc test từng vòng. File này **gộp (consolidate)** nội dung "Nguyên nhân / Cách fix / Đánh giá ảnh hưởng" của Dev trải qua tất cả các vòng (xem nguyên văn từng vòng ở `01-bug-task.md` mục Journal). Tester verify cần đọc đủ các vòng trước khi tick checkbox dưới đây.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Dev Studio (AI, `dev-studio@api`) — PIC ticket: Kieu Son Tung |
| Commit / Pull Request | Không có link PR — chỉ có chuỗi commit trên branch (commit cuối, vòng 8/9): `be42361322af53b8ff3e67ae784f8a872625a0f0` |
| Branch | `ai_studio_fixbug_45961` (nhánh gốc `release_step_20261106 @5badcb9a89f3`) |
| Ngày submit đánh giá | `2026-11-13` → `2026-11-18` (9 vòng, xem breakdown dưới) |
| Auto-filled | `2026-11-20 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại toàn bộ 9 vòng journal gốc (file 01) và xác nhận file này gộp đủ, không sót fix/case nào.

---

## 1. Nguyên nhân

**Vòng 1 (13/11, commit `d6e3cb60...`):**
- **Lỗi 1 (gốc ticket):** `refresh()` (chat-v2.js) khi lịch sử tin về, tìm hội thoại đang chọn trong `listFriend` rồi gọi `Vue.set(listFriend[index])` **không kiểm `index`**. Đổi bộ lọc/tìm kiếm → danh sách bị xoá để tải lại nhưng hội thoại đang chọn vẫn giữ → `index = -1` → Vue 2.2.6 văng `Cannot convert undefined or null to object`.
- **Lỗi 3:** `pushManager.subscribe` (layout chung `header.blade.php`/`footer.blade.php`) không có `.catch()`; bộ lọc lỗi push của chat-v2.js không khớp đúng message `Registration failed - could not retrieve the public key` → lỗi bị báo nhầm thành unhandledrejection.
- **Lỗi 2:** `status 0` (browser không nhận được response — trang rời đi / mất mạng) bị nhánh error của `loadFriend` báo trong **cả hai** trường hợp, không phân biệt được.

**Vòng 2 (13/11, commit `847363b2...`) — phát sinh từ chính fix vòng 1:**
- **Bug #5805:** guard của `refresh()` ở vòng 1 chỉ so `conversation_id`, không chặn response lịch sử **cũ** bị áp dụng sau khi danh sách bạn đã bị tải lại (đổi loại bạn/tìm kiếm/bộ lọc) → lẫn tin hội thoại cũ vào khung.
- **Bug #5806:** cờ bật ở `beforeunload` (vòng 1) không bao giờ được hạ, mà `beforeunload` vẫn bắn cả khi điều hướng **bị huỷ** → lỗi mất mạng thật (status 0) bị bỏ báo nhầm.
- **Bug #5807:** nhánh lỗi `get-friends` không hạ cờ `isFetching`/`isLoadingSearch` → sau 1 lần lỗi tìm kiếm, danh sách không tải lại được nữa (kẹt trạng thái đang tìm).

**Vòng 3 (16/11, commit `7d3e3264...`):**
- **Bug #5814:** cơ chế chặn báo status 0 ở vòng 2 chỉ dựa vào `pagehide` (chờ 3s) — một số trình duyệt huỷ request của trang cũ ngay sau `beforeunload`, còn `pagehide` chỉ chạy khi trang mới đã thay trang cũ. Trang đích phản hồi chậm hơn 3s → timer chạy trước, báo nhầm.

**Vòng 6 (16/11, commit `e71d3dc8...`) — quyết định nghiệp vụ + case mới do PIC phát hiện (Journal #154722):**
- **Quyết định của TungKS:** gỡ điều kiện so sánh tham chiếu `listFriend` (gọi là "D-5" trong journal, được thêm ở vòng giữa để chặn áp response lịch sử cũ) → **chấp nhận quay lại hành vi lẫn tin cũ của base** khi đổi bộ lọc lúc lịch sử đang tải. TypeError gốc (dòng 1428) vẫn được chặn nhờ D-1 (`index > -1`). ⚠️ Bug Studio #5805 do đó **fail lại có chủ đích** — không phải regression.
- **Case mới:** `EmptyRanges` (Safari nội bộ, không có file) bị báo nhầm là lỗi JS thật.
- **Case mới:** `getBotProfile()` trả `{success:false}` (phiên bị đăng xuất / token đổi) gây TypeError khi tải hồ sơ người gửi.
- **Bug #5849 — không phải bug:** do quy ước dự án "fix không tự tăng version asset" (việc của đội release) nên F5 thường dùng cache cũ; QA cần Ctrl+F5 hoặc chờ release tăng `sns-line.version`.

**Vòng 8 (18/11, commit `be423613...`):**
- **MetaMask:** bộ bắt `unhandledrejection` chỉ lọc lỗi push/permission, không lọc promise reject từ script của browser extension (`chrome-extension://...`) → lỗi "Failed to connect to MetaMask" (không phải lỗi sản phẩm) vẫn bị báo vào Chatwork.
- **SKIPPED_PAGE:** khi cuộn tới đáy, handler tăng `friendCurrentPage` **trước** khi gọi `loadFriend()`; nhánh error không lùi lại số trang → lần cuộn sau xin trang N+1, bạn của trang N (lỗi) không bao giờ được tải; nếu trang N+1 rỗng thì danh sách dừng tải hẳn.
- Note: tại thời điểm vòng 8, **production vẫn chạy bản chưa gộp nhánh fix** (`v=202611171542`) nên toàn bộ lỗi đã fix ở vòng 1-6 vẫn tiếp tục được báo trên prod.

**Vòng 9 (18/11, không có commit mới):**
- **Bug #5985 — không phải bug:** testcase Studio **NEW-17** vẫn kỳ vọng hành vi **cũ** (trang lỗi → cuộn sau nhảy sang trang kế, bỏ sót trang lỗi, báo `SKIPPED_PAGE`). Hành vi **mới** sau D-15 (vòng 8) là lùi số trang khi lỗi → không còn `SKIPPED_PAGE`. Đây là testcase lỗi thời cần Test Studio cập nhật, không phải lỗi sản phẩm.

## 2. Cách fix

| Tag | Vòng | Nội dung |
|---|---|---|
| D-1 | 1 | `refresh()`: bỏ qua `Vue.set(listFriend[index])` khi `index` của hội thoại đang chọn không có trong `listFriend` (check `index > -1`) |
| D-2 | 1 | Không gửi báo lỗi JS cho mọi lỗi Web Push "Registration failed - could not retrieve the public key …" |
| D-3 | 1 | `loadFriend`: không báo `loadFriend_AJAX` khi request bị huỷ vì trang đang rời đi (`beforeunload`/`pagehide`, bước đầu) |
| — | 2 | Fix #5805: `refresh()` bỏ áp response lịch sử cũ khi danh sách bạn đã bị tải lại (thêm điều kiện so tham chiếu `listFriend`, sau gọi tắt là "D-5") |
| — | 2 | Fix #5806: bỏ cờ đặt ở `beforeunload`; lỗi status 0 chờ ~3s và chỉ bị bỏ khi trang **thật sự** bị ẩn (`pagehide`) |
| — | 2 | Fix #5807: nhánh lỗi `get-friends` hạ cờ `isFetching`/`isLoadingSearch` → sau lỗi 500, xoá từ khoá tải lại được 20 hội thoại đầu |
| — | 3 | Fix #5814: thêm điều kiện — request đang chạy mà trang bắt đầu rời đi (`beforeunload`) thì lỗi status 0 **không** báo dù trang đích chậm/nhanh; request gửi **sau** một điều hướng bị huỷ vẫn báo như #5806 |
| D-5 (gỡ) | 6 | **Gỡ** điều kiện so tham chiếu `listFriend` thêm ở vòng 2, theo yêu cầu TungKS → chấp nhận hành vi lẫn tin cũ của base |
| — | 6 | Bỏ qua lỗi JS có `filename`/`source` = chuỗi `"undefined"` (script nội bộ trình duyệt không có file, vd `EmptyRanges` của Safari) |
| — | 6 | `getBotProfile()`: response `{success:false}` → bỏ qua, không TypeError, không báo lỗi |
| — | 6 | API `/api/notify-exception-chat11` (`ChatController::notifyExceptionChat11`): tin Chatwork thêm dòng `User agent` (≤200 ký tự, làm sạch `[` `]` → `［` `］`) |
| D-14 | 8 | Bỏ qua lỗi JS/`unhandledrejection` có nguồn là browser extension (stack/`source`/`filename` bắt đầu `*-extension://`, vd MetaMask) |
| D-15 | 8 | `loadFriend` lỗi (trang > 1) → **lùi số trang** để lần cuộn sau tải lại đúng trang bị lỗi (không còn bỏ sót trang) |
| — | 9 | Không có code mới — chỉ phản hồi bug Studio #5985 (not-a-bug, do hành vi D-15) + đề nghị Test Studio cập nhật kỳ vọng testcase **NEW-17** |

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `refresh()` — `public/js/chats/chat-v2.js` | D-1 (vòng 1) + D-5 thêm vòng 2, gỡ vòng 6 | Chạy mỗi lần chọn hội thoại + khi cuộn lên tải tin cũ; điểm va của TypeError gốc |
| 2 | `loadFriend()` / AJAX error handler — `chat-v2.js` | D-3 (v1), fix #5814 (v3), D-15 (v8) | Nhánh lỗi tải danh sách bạn — cờ đang tải, báo lỗi, lùi trang |
| 3 | `window.onerror` / listener `error` — `chat-v2.js` | Bỏ EmptyRanges (v6), bỏ extension (D-14, v8) | Bộ lọc lỗi JS toàn trang — phải giữ báo lỗi JS **thật** |
| 4 | listener `unhandledrejection` — `chat-v2.js` | D-2 (v1), D-14 (v8) | Web Push + MetaMask filter — lỗi promise khác vẫn phải báo |
| 5 | listener `beforeunload` / `pagehide` (mới) — `chat-v2.js` | Thêm v1, sửa v2/v3 | Đặt cạnh listener `beforeunload` sẵn có của socket (gửi `stop-typing`) — chỉ đặt cờ/tăng bộ đếm, **không** chặn rời trang, không hiện hộp xác nhận |
| 6 | `changeConfirm()` ("Đánh dấu tất cả đã đọc") — `chat-v2.js` | Không sửa trực tiếp, chỉ bị ảnh hưởng gián tiếp bởi D-15 | Gửi page = số trang hiện tại; sau một trang lỗi có thể nhỏ hơn 1 đơn vị nhưng Dev đảm bảo luôn ≥ 1 |
| 7 | `getBotProfile()` — `chat-v2.js` | Thêm guard v6 | Gọi khi mở trang + sau thêm/sửa/xoá hồ sơ bạn |
| 8 | `Basic\ChatController::notifyExceptionChat11` — `app/Http/Controllers/Basic/ChatController.php` | Thêm dòng User agent v6 | Nội dung tin Chatwork báo lỗi room `chat11` |

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `refresh()` | `public/js/chats/chat-v2.js` | Direct | D-1 (index guard) + lịch sử lẫn tin cũ **chấp nhận** (base behavior, quyết định TungKS 16/11) |
| F2 | `loadFriend()` + handler cuộn tải thêm | `public/js/chats/chat-v2.js` | Direct | D-3, D-15 — đổi hành vi báo lỗi + lùi trang khi lỗi; TC Studio NEW-17 lỗi thời |
| F3 | `window.onerror` / listener `error` | `public/js/chats/chat-v2.js` | Direct | Bỏ lọc nhầm `EmptyRanges`, extension — rủi ro lọc **quá tay** làm ẩn lỗi JS thật nếu điều kiện lọc không chặt |
| F4 | listener `unhandledrejection` | `public/js/chats/chat-v2.js` | Direct | D-2 (Web Push), D-14 (extension) |
| F5 | listener `beforeunload` / `pagehide` (mới) | `public/js/chats/chat-v2.js` | Direct (mới thêm) | Đặt cạnh listener `beforeunload` **sẵn có** của socket (`stop-typing`) — cần kiểm không đè/chặn lẫn nhau |
| F6 | `changeConfirm()` | `public/js/chats/chat-v2.js` | Indirect | Nhận page number có thể bị ảnh hưởng gián tiếp bởi D-15 (lùi trang khi lỗi) |
| F7 | `getBotProfile()` | `public/js/chats/chat-v2.js` | Direct | Guard `{success:false}` — ảnh hưởng modal thêm/sửa/xoá hồ sơ bạn gửi |
| F8 | `Basic\ChatController::notifyExceptionChat11` | `app/Http/Controllers/Basic/ChatController.php` | Direct | Thêm field `User agent` trong payload gửi Chatwork — PHP, có hiệu lực ngay khi deploy (không cần bump JS version) |

### 4.2. List data bị update khi fix bug

**Không có** — Dev xác nhận ở **mọi vòng** (1 → 9): "Migration / thay đổi dữ liệu: không có (đã kiểm diff)" và "Recover dữ liệu: Không cần recover — toàn bộ chỉ là hiển thị/log ở trình duyệt hoặc tin chẩn đoán gửi Chatwork, không có thao tác ghi DB hay gửi tin tới khách bị bỏ sót".

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Chat 1:1 — tải lịch sử tin khi đổi loại bạn/tìm kiếm/bộ lọc tag lúc lịch sử đang tải | F1 | High — TypeError đã fix (D-1), nhưng hành vi lẫn tin hội thoại cũ **được chấp nhận** (không fix) → TC phải expected đúng theo quyết định này, không theo "giống trước fix" |
| T2 | Chat 1:1 — danh sách bạn: cuộn tải thêm, phân trang khi lỗi | F2 | High — hành vi `SKIPPED_PAGE` đã đổi hẳn (D-15); TC Studio NEW-17 cũ sẽ fail đúng vì lỗi thời, không phải regression thật |
| T3 | Chat 1:1 — báo lỗi JS lên Chatwork (room chat11) | F3, F4, F8 | Medium — nhiều lớp lọc (Web Push, EmptyRanges, extension) cộng dồn qua 9 vòng; rủi ro lọc che mất lỗi JS thật mới phát sinh sau này |
| T4 | Chat 1:1 — rời trang / reload trong lúc đang tải danh sách bạn | F2, F5 | Medium — logic timing (beforeunload/pagehide/~3s) phức tạp, dễ regression khi trình duyệt khác nhau xử lý khác |
| T5 | Chat 1:1 — hồ sơ người gửi (mở/thêm/sửa/xoá) | F7 | Low |
| T6 | Chat 1:1 — "Đánh dấu tất cả đã đọc" (changeConfirm) sau một trang lỗi | F6 | Low/Medium — page number có thể lệch 1 đơn vị, Dev đảm bảo luôn ≥ 1 nhưng chưa có TC xác nhận độc lập |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] **Riêng ticket này:** xác nhận lại quyết định "chấp nhận lẫn tin cũ" (T1, bug Studio #5805) và yêu cầu Test Studio cập nhật TC NEW-17 (T2, bug Studio #5985) trước khi member viết TC bổ sung
