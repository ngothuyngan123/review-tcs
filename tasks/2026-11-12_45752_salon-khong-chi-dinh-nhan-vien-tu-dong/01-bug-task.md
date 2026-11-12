# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45752 — [11-11-2026][T12699][Salon] Đặt lịch Salon với lựa chọn 「指名なし」(không chỉ định nhân viên) nhưng chức năng tự động phân bổ nhân viên không hoạt động, khách hỏi nguyên nhân.` |
| Module / Màn hình | `Salon — Đặt lịch salon・phỏng vấn (サロン・面談予約), chức năng tự động phân bổ nhân viên khi chọn 「指名なし」(không chỉ định), trigger từ app LME (Flutter)` |

## Mô tả bug (bản dịch tiếng Việt)

Dù đã đặt lịch Salon với 「指名なし」(không chỉ định nhân viên) nhưng chức năng tự động phân bổ (自動振り分け) không hoạt động, khách không biết nguyên nhân.

- Tên friend báo lỗi: 森平
- Bot: エッコネイル広島京橋店
- Chức năng: Đặt lịch salon・phỏng vấn (サロン・面談予約)
- Thời điểm phản hồi (khách hỏi): 2026/11/11 14:29:49
- Nguồn: Tayori — task #12699 (操作方法に関するお問い合わせフォーム)

## Steps to reproduce

<!-- Tổng hợp từ Journal #153826 (data ca lỗi) + Journal #154091 (Đỗ Quyên — tái hiện) + Journal #153920/#153974 (Dev Studio — root cause). -->

1. Mở Salon có cấu hình chế độ phân bổ tự động nhân viên (ランダム / theo thứ tự ưu tiên) khi khách chọn 「指名なし」.
2. Trên **app LME (Flutter)** — màn thêm đặt lịch salon — chọn nhân viên ở trạng thái 「選択してください」(tức không chỉ định / 指名なし), lưu booking.
3. Quan sát: booking được tạo, nhưng không có job tự động phân bổ nhân viên nào chạy (so với khi thực hiện cùng thao tác trên web quản trị hoặc LIFF).

## Expected result

- Job `CalendarSalonStaffAssignmentAdmin` chạy, random/chọn một nhân viên hợp lệ gán cho booking; lịch sử booking có nhãn 「指定なし自動割り当て」; tin xác nhận, remind, Sheet, sự kiện Google Calendar gửi sau khi gán (hoặc gửi ngay nếu không còn nhân viên trống, giữ 指定なし + nhãn 「指定なし自動割り当て（スタッフ指定なし）」).

## Actual result

- Job tự động phân bổ **không chạy** (bị bỏ qua). Booking tạo từ app với 「指名なし」 lưu `staff_id = 0` và nằm mãi ở hàng 「指定なし」 — không có nhân viên nào được random/gán.
- Root cause (Dev Studio, journal #153920/#153974): màn thêm đặt lịch salon của app LME (Flutter) ghép `staff_id` thành **chuỗi** "null" khi để trống nhân viên. Endpoint `Api\CalendarSalonController::createBooking` giữ nguyên chuỗi "null". Trên PHP 8.5 (web đã nâng lên bản này), `"null" > 0` trả `true` và `"null" == 0` trả `false` (so sánh chuỗi không phải số kiểu cũ không còn đúng) → code rẽ nhánh sai: bỏ qua check ngày nghỉ đúng cách, đi vào nhánh "đã có staff", và **bỏ qua dispatch job assign tự động**.
- Web quản trị và LIFF gửi `staff_id` rỗng hoặc `0` (không phải chuỗi "null") nên không bị ảnh hưởng.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.melonglobal.net/attachments/download/40214/screenshot1.png

## Ghi chú thêm của Leader

- Bug phát sinh từ đợt nâng **PHP 8.5** lên production (bản `release_step_20261106`). Đợt nâng đã rà soát các so sánh lỏng (loose comparison) nhưng **bỏ sót trường hợp client gửi chuỗi "null"/"undefined" từ request** — class lỗi tương tự có thể còn ở nơi khác (xem `framework/php-upgrade-checklist.md`).
- Cùng branch fix (`ai_studio_fixbug_45752`) gộp **2 root cause riêng** do cùng pattern PHP8 string-vs-number:
  - **D-1**: app LME gửi `staff_id="null"` khi đặt lịch salon 指名なし → job tự động phân bổ bị bỏ qua (bug chính của ticket này).
  - **D-2**: màn sửa rich menu cũ (`/rich-menu/edit/{id}`, `Basic/UserController`) qua FormData cũng nhận giá trị trống dạng chuỗi "null" → rich menu tự mở (`表示する`) trên LINE sai, lẽ ra phải giữ trạng thái không tự mở. Phát hiện cùng lúc rà soát PHP8.5, không phải do khách báo ở ticket này — Leader cân nhắc coverage cho cả 2 nhánh khi review TC (file `03-dev-impact.md` mục 4 đã tách F/D/T riêng cho từng nhánh).
- Dev đã xác định **2 booking cụ thể bị lỗi** cần recover thủ công (xem bảng "Dữ liệu định danh ca lỗi"), và cảnh báo còn các booking khác bị kẹt từ khi lên PHP 8.5 tới khi fix được deploy — danh sách đầy đủ lập bằng SQL trong `docs/investigation/v1.md` (nội bộ Dev, không có trong Redmine).
- Việc Dev liệt kê "ngoài phạm vi task" (không cần review TC cho các mục này, chỉ note cho Leader biết): `/basic/send_media` luôn trả `success:false`; `/basic/scenario/copy` trỏ hàm không tồn tại; test `WebhookUrlValidatorLmeWebhookTest` thiếu `: void` ở `setUp()` làm cả thư mục `tests/Unit` lỗi khi nạp; `UserController` còn lỗi PHPStan `App\Bots::$channel_secret`; ticket riêng cho app Flutter sửa gửi `null`/`0` đúng kiểu (staff_id salon, lineUserId salon/lesson) thay vì ghép chuỗi.
- Branch: `ai_studio_fixbug_45752` (gốc `release_step_20261106` @ `20b5bcae03df`, commit `e3d1cc9140213f8a63d610444a86e92220f83c79`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `195674` (エッコネイル広島京橋店) |
| User (login) | `ecconeil.hiroshima@gmail.com` |
| salon_id | `23996` (【会員様用】) |
| Booking lỗi #1 | `2026.12.02(水) 11:00~12:00` (đặt lúc `2026.11.11(水) 12:15`) |
| Booking lỗi #2 | `2026.12.02(水) 14:00~15:00` (đặt lúc `2026.11.11(水) 15:07`) |
| Booking lỗi #3 (tương tự) | Đặt lúc `16:03:10`, line_user_id `373909`, cùng calendar `23996` |
| ID booking (DB) đã biết | `2600339`, `2602171` |
| Đối chứng | Đặt lịch cùng salon qua web quản trị / LIFF 指名なし — không bị lỗi (staff_id gửi rỗng/0) |

## Journal / note từ Redmine (nguyên văn)

**Journal #153826 — AI bug detect Lme — 2026-11-11:**
```
Thông tin bổ sung:
User: ecconeil.hiroshima@gmail.com
bot_id: 195674
salon_id: 23996 (【会員様用】)
Check 2 booking thời điiểm này: 
2026.12.02(水) 11:00~12:00 (book lúc 2026.11.11 (水) 12:15)
2026.12.02(水) 14:00~15:00 (book lúc 2026.11.11 (水) 15:07)
```

**Journal #153882 — Do Van Tu TuDV — 2026-11-11:**
```
1. Nguyên nhân trong code
Tại CalendarSalonController.php:1613:


$staffId = $request['staff_id'] ?? 0;   // "null" không phải null → vẫn giữ "null"
Server chạy PHP 8, mà PHP 8 so sánh chuỗi không phải số với số theo kiểu so sánh chuỗi:

"null" != 0 → true, nên bước check ngày nghỉ chạy.
"null" > 0 → true ("n" > "0"), nên dòng 1926 đi vào nhánh "đã có staff".
"null" == 0 → false, nên đoạn dispatch job tự động assign ở dòng 1955 bị bỏ qua.
Kết quả là booking có staff_id bị sai và không có job assign nào chạy. Booking lúc 16:03:10 (line user 373909) trên cùng calendar cũng bị lỗi tương tự.

2. Đề xuất fix
Phía server: chuẩn hóa giá trị trước khi dùng, app gửi gì cũng xử lý được:
```

**Journal #153920 — Dev Studio — 2026-11-11:**
```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Màn thêm đặt lịch salon của app LME (Flutter) ghép staff_id thành chuỗi, nên khi để nhân viên ở 「選択してください」 (指名なし) app gửi chữ "null". Endpoint `Api\CalendarSalonController::createBooking` giữ nguyên "null". Trên PHP 8.5, `"null" > 0` là true và `"null" == 0` là false, nên server gửi luôn tin, Sheet, remind và sự kiện Google với nhân viên trống, rồi bỏ qua job `CalendarSalonStaffAssignmentAdmin`. Booking lưu `staff_id = 0` và nằm mãi ở hàng 「指定なし」. Web quản trị và LIFF gửi rỗng hoặc 0 nên không bị lỗi.

Hướng sửa:
- D-1 Coi staff_id không phải số là "không chỉ định" (0) khi thêm đặt lịch salon từ app

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng endpoint thêm đặt lịch salon của app LME; app không cần cập nhật, schema và response không đổi. Cần test lịch có và không có phân bổ tự động, lịch 1 nhân viên và trường hợp chọn nhân viên cụ thể.
```

**Journal #153974 — Dev Studio — 2026-11-11:**
```
Dev handoff — 11/11 16:16 · nhánh ai_studio_fixbug_45752

Nguyên nhân:
Một số client gửi giá trị trống dưới dạng chữ "null" (app LME khi thêm đặt lịch salon, màn sửa rich menu cũ qua FormData). Từ khi web lên PHP 8.5, chữ đó không còn bằng 0 khi so sánh với số. Vì vậy server rẽ sai nhánh: không phân bổ nhân viên (đã sửa ở D-1), hoặc đẩy rich menu lên LINE ở chế độ tự mở (D-2). Đợt nâng PHP 8.5 đã rà so sánh lỏng nhưng bỏ qua giá trị lấy từ request, nên lớp lỗi này lọt qua.

Nội dung thay đổi:
- App LME › Salon › thêm đặt lịch, không chọn nhân viên, lịch bật phân bổ tự động: job gán nhân viên trống, lịch sử có 「指定なし自動割り当て」; tin xác nhận, remind, Sheet và sự kiện Google gửi sau khi gán.
- Web › Rich menu › màn sửa cũ (/rich-menu/edit/{id}): lưu menu có trạng thái trống thì rich menu trên LINE không tự mở, như trước khi nâng PHP 8.5.

File đã sửa (php-web):
  app/Http/Controllers/Api/CalendarSalonController.php | 2 ++
  app/Http/Controllers/Basic/UserController.php        | 2 ++
  2 files changed, 4 insertions(+)

Đánh giá ảnh hưởng — Rủi ro thấp: Mỗi sửa đổi chỉ 2 dòng ở một endpoint, đưa kết quả về như thời PHP 7.4, và chỉ khác khi giá trị gửi lên không phải số.
- App thêm đặt lịch salon có chọn nhân viên và lịch 1 nhân viên: cùng hàm đã sửa, kết quả không đổi với id dạng số.
- Job phân bổ nhân viên CalendarSalonStaffAssignmentAdmin (queue database) nhận thêm việc từ app: worker queue phải chạy.
- Đồng bộ rich menu lên LINE (createRichmenuLine) dùng chung với rich menu v2, copy, API và tutorial. Các nơi đó đọc status từ DB nên không đổi, nhưng nên lướt kiểm lưu/copy rich menu v2.
- Lưu rich menu status 1/0 ở màn sửa cũ: giá trị radio "1"/"0" được giữ nguyên.
- Web quản trị và LIFF đặt lịch salon 指名なし, tạo rich menu mới: không đi qua code đã sửa.

Migration / thay đổi dữ liệu:
- [Recover · Sau deploy] Gán nhân viên thủ công cho booking salon tạo từ app với 指名なし trên lịch bật phân bổ tự động, từ khi lên PHP 8.5 (đã biết 2600339, 2602171 của calendar 23996): 1) Trên production, chạy câu SQL chỉ đọc ở mục "Ảnh hưởng dữ liệu & khôi phục" trong docs/investigation/v1.md (thay <ngày deploy bản PHP 8.5>) để lập danh sách. 2) Gán nhân viên cho từng booking trên màn quản trị salon (Tu quyết định 11/11/2026: làm tay, không script).
- [Thao tác tay · Sau deploy] Rich menu cũ lưu trong thời gian lỗi đang tự mở trên LINE: mở màn sửa và lưu lại: Khi khách báo rich menu tự mở: vào rich menu đó ở màn sửa (/rich-menu/edit/{id}) và bấm lưu, không cần đổi gì (DB đã là status 0).

Recover dữ liệu: Cần recover — Booking salon đã lỗi kẹt ở staff_id = 0, Tu đã quyết định gán thủ công. Rich menu cũ được lưu lại từ khi lên PHP 8.5 có thể đang tự mở trên LINE; chỉ ảnh hưởng hiển thị và sẽ đúng lại khi lưu lại sau bản sửa, nên không viết script.
- Ảnh hưởng: calendar_salon_line_booking: booking thêm từ app với 指名なし trên lịch có phân bổ tự động có staff_id = 0
- Ảnh hưởng: Rich menu trên LINE: menu cũ status NULL được lưu lại trên PHP 8.5 bị đặt tự mở (DB vẫn lưu 0)
- Khoảng thời gian: Từ khi bản PHP 8.5 (release_step_20261106) lên production tới khi bản sửa được deploy.
- Cách recover: Booking: gán nhân viên thủ công theo quyết định của Tu (11/11/2026), dùng câu SQL trong tài liệu điều tra bản 1. Rich menu: không tự động sửa; nếu khách báo menu tự mở thì hướng dẫn lưu lại menu sau khi deploy.
- Ảnh hưởng tới khách: Gán nhân viên thủ công không gửi thêm tin LINE. Lưu lại rich menu chỉ đổi cách menu hiển thị.

Việc cần người làm thêm (ngoài phạm vi task):
- Rich menu cũ đã được lưu lại trên PHP 8.5 có thể đang tự mở trên LINE. Nếu khách báo, hướng dẫn lưu lại menu sau khi deploy bản sửa.
- Ngoài lớp lỗi này, lúc rà thấy 2 chỗ code: `/basic/send_media` luôn trả success:false, và `/basic/scenario/copy` trỏ tới hàm không tồn tại. Nên kiểm tra trong ticket riêng.
- Gán nhân viên thủ công cho các booking salon đã lỗi (đã biết 2600339 và 2602171).
- Tạo ticket cho app Flutter để gửi null/0 đúng kiểu thay vì ghép chuỗi "$staffId".
- Rich menu cũ (status trống) đã lưu từ khi lên PHP 8.5 có thể đang tự mở trên LINE: sau khi deploy, mở màn sửa và lưu lại các menu đó để về đúng.
- Gán nhân viên thủ công cho các booking app bị kẹt 「指定なし」 từ khi lên PHP 8.5 (danh sách lập bằng SQL trong docs/investigation/v1.md), theo quyết định của Tu.
- App Flutter nên gửi 0 hoặc bỏ staff_id thay vì chuỗi "null": cần ticket riêng cho module mobile.
- tests/Unit/WebhookUrlValidatorLmeWebhookTest.php có setUp() thiếu ': void' nên chạy cả thư mục tests/Unit bị lỗi ngay khi nạp; UserController còn lỗi PHPStan App\Bots::$channel_secret có sẵn trên base: cần sửa riêng.
- Gán nhân viên thủ công cho các booking salon bị ảnh hưởng (2600339, 2602171 và các booking tìm được bằng câu SQL trong tài liệu điều tra), rồi trả lời khách T12699.
- App Flutter gửi chuỗi "null" cho staff_id (salon) và lineUserId (salon, lesson); nên mở ticket riêng để app không nội suy giá trị null thành chuỗi.
- Quy tắc soát so sánh lỏng của đợt nâng PHP 8.5 (docs/upgrade/runtime-audit.md) đã bỏ qua trường hợp client gửi chuỗi "null"/"undefined"; nên bổ sung lớp này vào quy tắc và công cụ soát cho các đợt sau.

Điểm cần test:
- Rich menu cũ có trạng thái trống: mở màn sửa, lưu không đổi gì. Rich menu trên LINE không tự mở, DB lưu status 0.
- Rich menu đã chọn bật hoặc tắt tự mở (status 1 / 0) rồi lưu: LINE đúng như đã chọn.
- Tạo rich menu mới từ màn v2: không đổi.
- Các điểm kiểm thử của D-1 (thêm đặt lịch salon từ app) giữ nguyên.
- App LME, lịch salon phân bổ tự động (theo thứ tự và ngẫu nhiên), để スタッフ 「選択してください」: booking được gán nhân viên trống, lịch sử có 「指定なし自動割り当て」, tin xác nhận/remind/Sheet/sự kiện Google chỉ một lần.
- Như trên nhưng không còn nhân viên trống: booking giữ 指名なし, lịch sử có 「指定なし自動割り当て（スタッフ指定なし）」.
- App, chọn nhân viên cụ thể hoặc lịch 1 nhân viên: hành vi như cũ (kiểm ngày nghỉ, cộng phí nhân viên, gửi tin ngay).
- Rich menu cũ có status trống (tạo dữ liệu test), mở màn sửa cũ rồi lưu không đổi gì: rich menu trên LINE không tự mở, DB status = 0.
- Rich menu đã chọn bật hoặc tắt tự mở menu rồi lưu ở màn sửa cũ: LINE đúng như đã chọn.
- Tạo rich menu mới (màn cũ và v2), copy rich menu, đặt lịch salon từ web quản trị và LIFF: không đổi.

Branch: ai_studio_fixbug_45752
- sns-line: ai_studio_fixbug_45752 (nhánh gốc release_step_20261106 @20b5bcae03df, commit e3d1cc9140213f8a63d610444a86e92220f83c79)
```

**Journal #154091 — Đỗ Quyên — 2026-11-12:**
```
Tái hiện: 
1. Salon staff: có random 
2. App: booking no staff 
Hiện tại: ko random
Exepct: random cho staff hợp lệ
```
