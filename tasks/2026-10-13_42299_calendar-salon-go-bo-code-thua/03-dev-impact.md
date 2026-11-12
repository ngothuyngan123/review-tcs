# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Kieu Son Tung (TungKS) |
| Commit / Pull Request | `<chưa có — commit trace qua branch dưới>` |
| Branch | `ai_studio_fixbug_42299` (nhánh gốc `release_step_20260930_v2` @`bdeac6b86989`; commit cuối `3d10a367f647914465a380babdf9faa66c436c49`) |
| Ngày submit đánh giá | 2026-10-07 (v1: Journal #140882 → v2: #140959/#140966 → v3: #140999/#141009, cùng ngày) |
| Auto-filled | 2026-10-13 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Ticket không yêu cầu fix 1 bug cụ thể — gộp nguyên nhân cả 3 vòng đánh giá (v1 → v2 → v3), Dev confirm lần lượt qua các journal. -->

Ticket không báo triệu chứng: người phụ trách (TungKS) yêu cầu gỡ các lớp code mà **5 lượt AI fixbug trước** đã thêm vào, cụ thể:

- **v1** — gỡ 3 lớp code từ #41304/#41321, #41258, #41216/#41953:
  - Transaction kèm khoá và try/catch trong `deleteCalendarSalon`.
  - Phép kiểm `hasShiftAdjacentToExisting` (chặn ca mới dính sát ca đã có trong ngày) ở `addWorkScheduleForStaff` của service web và API app.
  - Băng cảnh báo đổi tài khoản LINE do `showBotSessionChangedNotice` dựng ở chat 1:1.
- **v2** — ở bản thực thi v1, hàm `deleteCalendarSalon` vẫn còn sót bước đọc lại lịch `$target` + cờ `$lostRace` kèm nhánh trả 404/403/422 — phần còn lại của cơ chế chống xoá song song (#41321). TungKS chốt bỏ luôn cơ chế này, chỉ xoá bình thường (guard đầu hàm độc lập với cơ chế đó → giữ lại).
- **v3** — gỡ thêm lớp code từ #41228 (vòng 2): commit đó bọc phần ghi của `ChatController::changeStatusSettingCons` trong `DB::transaction` và thêm `lockForUpdate` vào truy vấn `$conList`, khiến 2 lượt bấm song song phải chờ nhau. Trong `ChatController` chỉ có đúng 1 transaction + 1 lockForUpdate, cả hai đều ở hàm này.

Vị trí code và commit gốc của từng lớp đã được Dev xác định chính xác ở cả 3 vòng.

## 2. Cách fix

**Hướng sửa (D-1 → D-7, theo đúng số Dev đặt):**

- D-1 Bỏ transaction và try/catch khi xoá lịch salon.
- D-2 Bỏ kiểm ca liền kề ca đã có ở màn web.
- D-3 Bỏ kiểm ca liền kề ca đã có ở API app.
- D-4 Xoá các hàm hỗ trợ không còn nơi gọi.
- D-5 Bỏ băng cảnh báo đổi tài khoản LINE ở chat 1:1.
- D-6 Bỏ bước đọc lại lịch và cơ chế `$lostRace` khi xoá lịch salon.
- D-7 Bỏ transaction và `lockForUpdate` ở `changeStatusSettingCons`.

**Nội dung thay đổi cuối cùng (bản v3 — cumulative, theo Dev handoff #141009):**

- **Màn chi tiết lịch salon, nút xoá lịch (web)**: chuỗi xoá chạy thẳng, không transaction, không đọc lại/lostRace; lỗi hệ thống (nếu có) trả theo Handler chung thay cho 500 「カレンダーの削除に失敗しました…」; mã 400/403/404/422 ở guard đầu hàm **giữ nguyên**; hai request xoá song song có thể cùng trả 200.
- **Màn 「シフト追加」 (web)**: thêm ca dính sát ca đã có trong ngày **không còn bị chặn**, ca cũ trong ngày bị **thay bằng ca mới**.
- **API app `add-work-schedule-for-staff`**: tương tự web, bỏ chặn ca liền kề.
- **Chat 1:1**: không còn băng vàng 「別のタブでLINEアカウントが切り替えられました…」 + nút 再読み込み; màn **vẫn** bỏ qua dữ liệu của tài khoản khác (hành vi data không đổi).
- **Chat 1:1, đổi trạng thái hàng loạt** (chọn nhiều hội thoại → trạng thái): không còn transaction và khoá hội thoại; response, validate 400/422, guard 403/404, cộng/trừ bộ đếm nguyên tử **giữ nguyên**; bấm 2 lần/2 tab song song có thể gặp 500 hoặc bộ đếm lệch như trước #41228.

**Lưu ý khi deploy**: không có migration/cấu hình. QA + user cần **Ctrl+F5** để nạp `chat-v2.js` mới (không bump version JS).

**Việc cần người làm thêm (ngoài phạm vi task, Dev ghi rõ không raise ở review này)**: sửa riêng 4 file PHPUnit đã lỗi sẵn trên base (`BillingServiceTest`, `ChatMediaSizeValidationTest`, `ContractExpireServiceTest`, `ExampleTest`) — không thuộc ticket #42299.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `CalendarSalonTimeBookingService::addWorkScheduleForStaff` | Bỏ `hasShiftAdjacentToExisting` | Service dùng chung cho cả web + app — sửa 1 nơi, check cả 2 lối vào |
| 2 | `Api/CalendarSalonController` (app) | Bỏ check ca liền kề tương tự web | Đồng bộ hành vi app với web sau khi bỏ D-2/D-3 |
| 3 | `Basic/CalendarSalonController::deleteCalendarSalon` | Bỏ transaction/try-catch + bỏ đọc lại `$target`/`$lostRace` | D-1 + D-6 cùng chạm 1 hàm — Dev gộp kiểm tra 1 lượt ở v2 |
| 4 | `chat-v2.js` — `isBotSessionChanged` (gọi từ `get_message`/`get-badge`/`confirm-message`/`get-bot-data`) | Bỏ hiển thị băng vàng + nút reload | Dev xác nhận **không đổi hành vi dữ liệu** ở các điểm gọi này, chỉ bỏ UI cảnh báo |
| 5 | `ChatController::changeStatusSettingCons` | Bỏ `DB::transaction` + `lockForUpdate` trên `$conList` | D-7 — route/response/JS (`chat-v2.js` và `chat.js`) giữ nguyên |
| 6 | 4 file PHPUnit lỗi sẵn trên base | Không sửa (ngoài phạm vi) | Dev ghi rõ lỗi sẵn trên base, không liên quan ticket |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `deleteCalendarSalon` (xoá lịch salon, web) | `Controllers/Basic/CalendarSalonController.php` | Direct | D-1 + D-6: bỏ transaction/try-catch/đọc lại/`$lostRace`; guard 400/403/404/422 đầu hàm giữ nguyên |
| F2 | `addWorkScheduleForStaff` (service, dùng chung web + app) | `CalendarSalonTimeBookingService.php` | Direct | D-2: bỏ `hasShiftAdjacentToExisting` — ca liền kề không còn bị chặn, ca cũ bị ghi đè |
| F3 | `addWorkScheduleForStaff` (API app) | `Controllers/Api/CalendarSalonController.php` | Direct | D-3: tương tự F2, qua lối vào app |
| F4 | `showBotSessionChangedNotice` / `isBotSessionChanged` (chat 1:1) | `public/js/chats/chat-v2.js` | Direct | D-5: bỏ băng cảnh báo UI; các điểm gọi `get_message`/`get-badge`/`confirm-message`/`get-bot-data` không đổi hành vi data |
| F5 | `changeStatusSettingCons` (đổi trạng thái hàng loạt chat 1:1) | `app/Http/Controllers/ChatController.php` | Direct | D-7: bỏ transaction + lockForUpdate trên `$conList`; response/guard/JS giữ nguyên |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | 14 bảng con + lịch cha của lịch salon (course, course_menu, history_change_setting_payment, line_booking + history_action, mobile_notify, google calendar + history, csv sync, setting limit/notify/send_forms/send_message/time_free, staff, time_booking, events type 5 + step/step_time) | DELETE | F1 — cùng điều kiện xoá như bản đang chạy; **không rollback** nếu lỗi DB giữa chừng ⇒ có thể xoá dở |
| D2 | `time_booking` (ca làm nhân viên salon) | UPDATE/CREATE | F2/F3 — ca mới liền kề ca cũ trong ngày ghi đè ca cũ; gộp ca cùng lần gửi + booking 予約確定 + ngày nghỉ **vẫn** bị chặn (không đổi) |
| D3 | `conversation`, `status_chat` (count), `bots.count_user_unconfirm`, sync Elasticsearch | UPDATE | F5 — cộng/trừ bộ đếm giữ nguyên logic nhưng **không còn** transaction/lock ⇒ lỗi giữa chừng không rollback, 2 request song song có thể lệch đếm/500 deadlock |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Xoá lịch salon (web — màn chi tiết lịch salon) | F1, D1 | High — mất rollback, lỗi giữa chừng có thể để dữ liệu xoá dở; 2 request xoá song song có thể cùng 200 |
| T2 | Thêm ca làm nhân viên salon (web 「シフト追加」) | F2, D2 | Medium — đổi hành vi có chủ đích (TungKS chốt): ca liền kề không còn bị chặn, ca cũ bị thay; cần test hồi quy BR-13 (gộp ca cùng lần gửi) + BR-14 (予約確定/ngày nghỉ) **không đổi** |
| T3 | Thêm ca làm nhân viên salon (API app `add-work-schedule-for-staff`) | F3, D2 | Medium — cùng service với T2, lặp lại các case trên lối vào app |
| T4 | Chat 1:1 — băng cảnh báo đổi tài khoản LINE | F4 | Low — chỉ mất UI cảnh báo; hành vi dữ liệu (bỏ qua data account khác) không đổi; cần Ctrl+F5 để nạp JS mới |
| T5 | Chat 1:1 — đổi trạng thái hàng loạt (`/basic/change_status_cons`) | F5, D3 | Medium — guard/response/JS giữ nguyên nhưng mất transaction/lock ⇒ risk 500 deadlock hoặc lệch bộ đếm khi bấm 2 lần/2 tab song song (rủi ro Dev đã chấp nhận, không coi là bug) |

---

## Ghi chú thêm — đối chiếu MCP LME TEST STUDIO (task #375)

<!-- Thông tin lấy từ task_get_context(sections=["dev_impact","requirements"]) — bổ sung tham khảo, KHÔNG thay thế mục 1-4 trên (nguồn chính = Redmine Section B). -->

Studio đã có task #375 cho ticket này, `dev_impact` do Dev ghi trên tab Thông tin khớp với nội dung trên (bổ sung chi tiết: endpoint `EP-A50`/`EP-B15` cho thêm ca, `EP-A11`/`BR-12` cho xoá lịch, `/chat-v3` cho chat 1:1, `/basic/change_status_cons` không có UI sống gọi tới ⇒ kiểm bằng API). Studio cũng có sẵn 9 `requirements` (REQ-001 → REQ-009) map tương ứng F1-F5/T1-T5 trên — dùng tham khảo khi `/review-tc` đối chiếu coverage, không copy nguyên văn vào đây.

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
