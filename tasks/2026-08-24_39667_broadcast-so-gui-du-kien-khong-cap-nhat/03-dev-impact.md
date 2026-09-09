# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39667 bằng `/new-task`. Nguồn: **journal #130706** (AI LME Fix bug, 2026-08-20T06:04:41Z) — báo cáo `★ AI AUTO-FIXBUG`.
>
> ⚠️ **Fix do AI Auto-fixbug thực hiện**, không phải human dev. Human dev có tham gia review (đưa lỗi thật lúc review) và ra "chỉ đạo human" về phạm vi sửa.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — có "chỉ đạo human" về phạm vi (decision #68, #71, #72, #74, #75) |
| Commit / Pull Request | `sns-line` commit `d0b0ddc1d2` (5 file). Không có link Github/Gitlab trong ticket. |
| Branch | `ai_fixbug_39667` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-20` (journal #130706) · Commit Date custom field = `2026-08-20` |
| Auto-filled | `2026-08-24 by /new-task` |
| Phiên xử lý AI | https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=31394d46-3f4e-432a-93e8-07ba0903e475 |
| Dashboard fixbug | https://dashboard.melonglobal.net/fixbug-lme/?id=39667 |
| Thời gian AI xử lý | 9 phút 40 giây |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■ 1. NGUYÊN NHÂN, journal #130706 -->

Câu đếm số bạn theo điều kiện lọc (`Conversation::advanceFilterPost`) nổ lỗi cơ sở dữ liệu 1390 `Prepared statement contains too many placeholders` trên tài khoản nhiều bạn bè. Hàm này có **26 chỗ** kéo toàn bộ mã người dùng về mã nguồn rồi nhét ngược lại vào điều kiện lọc của câu truy vấn, nên số tham số bằng đúng số bạn bè của tài khoản và **vượt giới hạn 65535** của cơ sở dữ liệu. Vì câu đếm này được dùng ở **cả nút tính lại số gửi dự kiến lẫn lúc lưu điều kiện lọc**, nên tài khoản lớn bấm gì cũng hỏng.

## 2. Cách fix

<!-- Nguyên văn mục ■ 2. CÁCH FIX, journal #130706 -->

Ba nhóm thay đổi theo chỉ đạo human.

1. **Câu truy vấn bộ lọc chính**: đổi toàn bộ **26 chỗ** trong `Conversation::advanceFilterPost` từ kiểu kéo danh sách mã người dùng về mã nguồn rồi nhét lại vào điều kiện, sang **truy vấn lồng (subquery)**; áp cho tất cả loại lọc ở **cả nhánh VÀ lẫn nhánh HOẶC**, các nhánh loại trừ thêm điều kiện bỏ giá trị rỗng.
2. **Bỏ khối bắt lỗi** bao quanh hàm tính lại số gửi dự kiến để lỗi nổi lên thay vì bị nuốt, thân hàm giữ nguyên.
3. **Quét cả mã nguồn** tìm cùng kiểu lỗi rồi sửa các chỗ **CÒN ĐANG DÙNG**: màn danh sách hội thoại lọc theo thẻ, ba chỗ lọc theo kịch bản ở màn danh sách bạn bè, và hai hàm dựng danh sách hội thoại của màn quản lý hội thoại.

**KHÔNG sửa** hai lệnh chạy nền theo yêu cầu human. **KHÔNG sửa** phần lọc theo mã hội thoại của bảng tin nhắn vì bảng đó nằm ở **cơ sở dữ liệu khác** nên không lồng truy vấn được — đã ghi rõ giới hạn này để người phụ trách hạ tầng quyết định.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3, journal #130706 -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Conversation::advanceFilterPost` + `Conversation::advanceFilter` (`app/Conversation.php`) | ĐÃ SỬA — 26 chỗ | Bộ lọc bạn bè **dùng chung toàn hệ thống** |
| 2 | `BroadcastController::getFilterNumber` (`app/Http/Controllers/Basic/BroadcastController.php`) | ĐÃ SỬA — bỏ khối bắt lỗi | Lỗi bị nuốt im lặng |
| 3 | `ConversationService::getFriend` (`app/Services/ConversationService.php`) | ĐÃ SỬA | Màn hội thoại bản mới — lọc theo thẻ |
| 4 | `FriendlistController::sendActionFriend` (2 chỗ) + `postFilterAdvance` (1 chỗ) (`app/Http/Controllers/Basic/FriendlistController.php`) | ĐÃ SỬA | Lọc theo kịch bản |
| 5 | `BotLineUser::makeDataTalkList` + `BotLineUser::getMsgTalkList` (`app/BotLineUser.php`) | ĐÃ SỬA | Màn quản lý hội thoại |
| 6 | `ConversationReplicate::advanceFilter` + `advanceFilterPost` | **KHÔNG sửa** | Mã chết — không nơi nào gọi |
| 7 | Toàn bộ `BotLineUserPackage` | **KHÔNG sửa** | Mã chết — không nơi nào gọi |
| 8 | `ChatController::getFriends` (màn hội thoại bản cũ) | **KHÔNG sửa** | Mã chết — tuyến đã bị chú thích |
| 9 | Hai lệnh chạy nền phân tích chéo | **KHÔNG sửa** | Theo **yêu cầu human** — vẫn còn lỗi cũ |
| 10 | Đường API cho ứng dụng di động | **KHÔNG sửa** | Theo yêu cầu human (ngoài phạm vi project) |
| 11 | `BotLineUser::getListMessages` + 3 biến thể | **KHÔNG sửa được** | Bảng tin nhắn ở **cơ sở dữ liệu khác** → không lồng truy vấn được |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục ■ 4.1 File thay đổi, journal #130706 -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `advanceFilterPost` + `advanceFilter` — 26 chỗ đổi mảng PHP sang truy vấn lồng | `app/Conversation.php` | **Direct** | ⚠️ Đây là **bộ lọc bạn bè DÙNG CHUNG cho toàn hệ thống** |
| F2 | `getFilterNumber` — bỏ khối bắt lỗi nuốt lỗi, thân hàm giữ nguyên | `app/Http/Controllers/Basic/BroadcastController.php` | Direct | Đổi hành vi lỗi: từ "thất bại im lặng" → trả lỗi hệ thống |
| F3 | `getFriend` — lọc theo thẻ ở màn hội thoại, 2 nhánh (đủ tất cả thẻ / có ít nhất một thẻ) | `app/Services/ConversationService.php` | Direct | |
| F4 | `sendActionFriend` (2 chỗ) + `postFilterAdvance` (1 chỗ) — lọc theo kịch bản | `app/Http/Controllers/Basic/FriendlistController.php` | Direct | |
| F5 | `makeDataTalkList` + `getMsgTalkList` — dựng danh sách hội thoại theo bộ lọc | `app/BotLineUser.php` | Direct | ⚠️ Tải chuyển từ máy chủ dự phòng sang **máy chủ chính** |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục ■ 4.2 Data ảnh hưởng, journal #130706 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Cột số gửi dự kiến + cột mốc thời gian của broadcast | UPDATE | Hàm tính lại số gửi dự kiến vẫn ghi **đúng hai cột như cũ** |
| D2 | — | (chỉ đọc) | Không thêm, sửa hay xoá bản ghi nào. Toàn bộ phần còn lại chỉ đọc |
| D3 | Tập kết quả lọc | (không đổi) | Nhánh loại trừ đã thêm điều kiện bỏ giá trị rỗng; nhánh không khớp bạn bè nào vẫn trả mã `-1` nên câu phía sau lọc ra rỗng y như cũ |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục ■ 4.3 Tính năng liên quan, journal #130706 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **BỘ LỌC BẠN BÈ (SC-003)** — 5 loại điều kiện **ĐÃ ĐỔI**, áp cho cả nhóm VÀ lẫn nhóm HOẶC: (1) Trạng thái xác nhận tin nhắn; (2) Trạng thái đăng ký kịch bản — cả vế đang đăng ký lẫn vế không đăng ký; (3) Thông tin bạn bè; (4) Trạng thái đối ứng — cả vế thuộc trạng thái đã chọn lẫn vế không thuộc hoặc chưa đặt; (5) Bạn mới hay bạn cũ | F1 | **High** |
| T2 | **BỘ LỌC BẠN BÈ (SC-003)** — chi tiết loại *Thông tin bạn bè*: 5 phép so sánh với ô nhập chữ (khớp hoàn toàn, khớp một phần, không khớp hoàn toàn, không khớp một phần, có đăng ký thông tin) áp cho **cả trường mặc định lẫn trường tự tạo**; 3 nhánh kiểu ngày (khoảng ngày cụ thể, khoảng tháng-ngày không có năm, ngày tháng năm chỉ định); và nhánh có hoặc không có giá trị | F1 | **High** |
| T3 | **BỘ LỌC BẠN BÈ (SC-003)** — 7 loại điều kiện **KHÔNG ĐỔI** vì vốn không dùng mảng PHP: Thẻ, Tên bạn bè, Ngày thêm bạn, Chuyển đổi, Mã QR, Hành động mã QR, Đại lý giới thiệu | — | Low (verify không đổi) |
| T4 | **Gửi tin nhắn hàng loạt (FA-008)** — nút tính lại số gửi dự kiến, lưu điều kiện lọc khi soạn tin, số gửi dự kiến của tin đặt lịch. **Đây là chỗ khách báo lỗi** | F1, F2, D1 | **High** |
| T5 | **Quản lý chat (FA-002)** — màn quản lý hội thoại: dựng danh sách hội thoại theo bộ lọc bạn bè (hai hàm) không còn kéo toàn bộ mã bạn bè về mã nguồn | F5 | **High** |
| T6 | **Chat 1:1 (FA-001)** — màn hội thoại bản mới: lọc bạn bè theo thẻ, cả vế phải đủ tất cả thẻ đã chọn lẫn vế chỉ cần một thẻ | F3 | **High** |
| T7 | **Danh sách bạn bè (FA-013)** — lọc theo kịch bản ở luồng gửi hành động (đang chạy kịch bản, chưa hoàn thành kịch bản) và ở lọc nâng cao (đang chạy kịch bản) | F4 | **High** |
| T8 | **Quản lý thông tin bạn bè (FA-015)** — các điều kiện lọc theo trường thông tin bạn bè nói trên | F1 | **High** |
| T9 | **Phát hành theo bước (FA-009)**, **Rich Menu (FA-004)**, **Quản lý CSV (FA-014)**, **Gửi nhắc lịch (FA-022)**, **Đặt lịch bài học (FA-019)**, **Đặt lịch salon (FA-020)**, **Phân tích chéo (FA-024)** — các màn này gọi chung bộ lọc bạn bè nên hưởng lợi theo, **cần kiểm thử lại bộ lọc trên từng màn** | F1 | Medium |

---

## 5. Recover data

✔ **Không cần recover data.**

## 6. Verify (Dev đã làm)

**Mức: unit**

- `php -l` cho cả 5 file: No syntax errors.
- Dựng SQL thật qua `advanceFilterPost` cho 6 loại lọc × 2 nhánh VÀ/HOẶC + 8 nhánh thông tin bạn bè: tất cả ra truy vấn lồng, 4-7 tham số.
- Dựng SQL tổ hợp 5 điều kiện VÀ + 5 điều kiện HOẶC: 34 tham số, 10 truy vấn lồng.
- Dựng SQL cho lọc theo thẻ ở màn hội thoại: 3 tham số, có mệnh đề gom nhóm và điều kiện đếm nằm trong truy vấn lồng.
- Dựng SQL cho lọc theo kịch bản ở màn danh sách bạn bè: 4 tham số, truy vấn lồng.
- Dựng SQL cho hàm dựng danh sách hội thoại của màn quản lý hội thoại: 5 tham số, 2 tầng truy vấn lồng.
- Đối chiếu ngữ nghĩa nhánh rỗng: không bạn bè nào khớp thì vẫn trả về mã `-1`.
- `git diff --stat release_step_20260805...ai_fixbug_39667`: 5 file.

**Bằng chứng:** Human dev đưa lỗi thật lúc review: `SQLSTATE[HY000] General error 1390 Prepared statement contains too many placeholders` trên **tài khoản bot 111533**. Giới hạn 65535 tham số cho một câu truy vấn chuẩn bị sẵn. Đã trace đường vào của từng chỗ trước khi sửa. Đã loại các chỗ là mã chết.

> ⚠️ **KHÔNG tái hiện được trên dev**: cơ sở dữ liệu vẫn từ chối kết nối; kiểm chứng bằng cách dựng câu truy vấn rồi đọc câu sinh ra. **Chưa chạy trên cơ sở dữ liệu thật.**

## 7. Tự review (AI) — rủi ro / lưu ý khi test

> Nguyên văn mục ■ TỰ REVIEW (AI). **Đây là input quan trọng nhất để chấm coverage TCs.**

- ⚠️ **Còn rủi ro CHƯA xử lý**: phần lọc tin nhắn theo mã hội thoại trong **bốn hàm** dựng danh sách tin nhắn vẫn dùng mảng. Bảng tin nhắn ở kết nối riêng và bảng theo năm ở nhà cung cấp khác nên không lồng truy vấn được. **Nếu số hội thoại khớp bộ lọc vượt 65535 thì màn quản lý hội thoại VẪN nổ lỗi cũ**; muốn xử lý phải chia lô hoặc gộp cơ sở dữ liệu — là quyết định hạ tầng.
- ⚠️ Ở màn quản lý hội thoại, phần lọc bạn bè trước đây chạy trên **máy chủ dự phòng** rồi mới ghép ở máy chủ chính; nay gộp thành một câu chạy trên **máy chủ chính** nên **tải chuyển sang máy chủ chính**. Nếu hạ tầng muốn giữ tải ở máy chủ dự phòng thì đổi câu ngoài sang lớp nhân bản, nhưng khi đó dữ liệu hội thoại chịu **độ trễ của bản sao** — cần người phụ trách quyết.
- ⚠️ Truy vấn lồng chạy trên kết nối của câu ngoài; khi **bật máy chủ dự phòng** thì các bảng phụ đọc từ bản sao thay vì máy chủ chính — cần xác nhận bản sao có đủ bảng.
- ⚠️ Phạm vi đã lan sang **màn hội thoại, màn danh sách bạn bè và màn quản lý hội thoại** nên cần kiểm thử lại **cả ba màn**, không chỉ màn gửi tin hàng loạt.
- ⚠️ **KHÔNG sửa hai lệnh chạy nền phân tích chéo** theo yêu cầu human — hai lệnh đó **vẫn còn lỗi cũ**.
- ⚠️ **KHÔNG sửa đường API cho ứng dụng di động** (ngoài phạm vi project).
- ⚠️ **Chưa chạy được trên cơ sở dữ liệu thật** vì môi trường dev không kết nối được.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Điểm Leader cần quyết trước khi test

1. **Fix generic dùng chung** — `Conversation::advanceFilterPost` là bộ lọc bạn bè của **toàn hệ thống**, sửa 26 chỗ. Fix chạm 9 nhóm tính năng (T1–T9) ⇒ phải cover đủ **cả 12 loại điều kiện lọc** (5 đã đổi + 7 không đổi) trên **cả nhánh VÀ lẫn HOẶC**.
2. **Rủi ro treo được Dev khai báo** (bốn hàm lọc tin nhắn theo mã hội thoại, hai lệnh chạy nền, API mobile) — là **giới hạn đã biết**, không phải regression. Nhưng cần Leader ghi rõ để QA không kết luận nhầm.
3. **Điều kiện tái hiện**: bug chỉ nổ khi **> 65535 tham số** ⇒ TC "vượt giới hạn" **không thể** verify từ local/staging ít friend (**RULE-08**).
4. Studio đã bổ sung 3 requirement (REQ-022 / REQ-023 / REQ-024) ghi rõ **"CHƯA có code trong nhánh hiện tại"** — tương ứng 4 TC chưa chạy lần nào trong `04-tc-list.md`. Leader cần chốt các mục này thuộc scope ticket này hay tách ticket mới.
