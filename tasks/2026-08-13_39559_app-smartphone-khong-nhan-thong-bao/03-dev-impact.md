# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39559 bằng `/new-task`. Nguồn: **journal AI AUTO-FIXBUG mới nhất** (2026-08-13T11:21:51Z).
>
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` — **hệ thống Auto-fixbug LME tự động**, không có dev người nào ký tên. Redmine `assigned_to` = `Ngô Thúy Ngần` (QA, đang chờ test) |
| Commit / Pull Request | `<không có link Github/Gitlab/PR trong Redmine>` — chỉ có repo + branch + commit hash: repo `sns-line`, commit **`3233088f19`** (2 file). Phiên AI: https://claude-admin.melonglobal.net/?project=implement-task-small-lme&tab=events&session=99b2388b-0436-4c2c-9143-e3b0b85db201 · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=39559 |
| Branch | `ai_small_39559` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-13` (journal mới nhất 2026-08-13T11:21:51Z) |
| Auto-filled | `2026-08-13 by /new-task` |
| Verify của Dev | **Mức: `static`** — Dev tự ghi. Kiểm chứng chỉ gồm `php -l` sạch + dựng lại câu SQL bằng query builder + đối chiếu tay theo case NEW-6. **Không chạy thật, không có DB dev** (Dev tự nêu "DB dev không chạy") |
| Recover data | **✔ Không cần recover data** (Dev khẳng định) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## ⚠️ Lịch sử vòng fix — ticket qua 3 vòng AI Auto-fixbug, file này chỉ lấy vòng CUỐI

| Vòng | Journal (UTC) | Commit | Nội dung |
|---|---|---|---|
| 1 | 2026-08-13T03:39:10Z | `1cba79c51d` | Rollback commit `4dd0eb47` của lần fix trước đó; fix gốc theo `device_id` trùng (2 file, 3 điểm). **Superseded** |
| 2 | 2026-08-13T06:40:34Z | `caa3c277b7` | Thêm fix theo **#39635** (token mới bị xoá mất). **Superseded** |
| **3 (dùng file này)** | **2026-08-13T11:21:51Z** | **`3233088f19`** | Thêm fix theo **#39636** (API trả token/badge của người khác) + chặn `user_token` rỗng + 2 vòng spec bổ sung của dev về `getFirebaseToken` |

> ⚠️ **Rủi ro review**: mục 2 dưới đây là **cách fix cộng dồn qua nhiều vòng trong cùng 1 hàm** (`updateFirebaseToken`, `getFirebaseToken`), có vòng **đảo lại quyết định của vòng trước** (vòng 3 "BỎ HẲN nhánh dự phòng" mà vòng 2 vừa siết; rồi lại "BỎ HẲN điều kiện hệ điều hành" mà chính vòng 3 vừa thêm). Leader cần đọc kỹ để không viết TC theo hành vi đã bị thay đổi.
>
> ⚠️ **Mục 3 và mục 4 KHÔNG được cập nhật qua 3 vòng** — nội dung giống hệt vòng 1 (đã diff xác nhận), dù vòng 2/3 đã sửa thêm `getFirebaseToken` và thêm chốt chặn cho **3 API** (`getFirebaseToken`, `updateFirebaseToken`, xoá token). Nghĩa là **mục 4.1/4.2/4.3 có thể đã lạc hậu so với code thực tế** → đây là nguồn GAP tiềm năng.

---

## 1. Nguyên nhân

<!-- Nguyên văn journal AI AUTO-FIXBUG 2026-08-13T11:21:51Z, mục ■ 1. NGUYÊN NHÂN -->

Ứng dụng gửi lên device_id KHÔNG duy nhất giữa các máy: bản Android gửi build ID của ROM (BP4A.251205.006 có 135 tài khoản khác nhau dùng chung, CP2A.260705.006 có 101, CP1A.260505.005 có 101...) thay vì mã máy thật, chiếm 2.958/3.071 ca lỗi (~96%). API cập nhật mã đẩy thông báo (Api/MobileController::updateFirebaseToken) tra bản ghi CHỈ theo device_id + hệ điều hành, KHÔNG kèm người dùng, nên khi người dùng B đăng nhập, truy vấn khớp đúng bản ghi của người dùng A rồi rơi vào nhánh CẬP NHẬT: ghi đè người dùng và mã đẩy của A. A mất bản ghi, mọi lần gọi lấy mã đẩy sau đó đều trả rỗng nên máy A không nhận được thông báo. Bằng chứng trực tiếp: bản ghi id 237937 (device CP1A.260505.005) đổi chủ 8 lần trong 45 phút (128182 → 166111 → 107234 → 104839 → 126234/33675 → 175686/113644 → 128719/154668 → 100512); riêng tài khoản 33675 sau đó nhận rỗng 63 lần. Hệ quả nặng hơn mất thông báo: mã đẩy của máy đó bị lệnh đăng ký chủ đề gắn vào chủ đề bot của người đang chiếm bản ghi, có khả năng đẩy thông báo bot của người khác sang máy sai. Đoạn dọn trùng ở cuối hàm còn xoá NGƯỢC (sắp giảm dần theo id rồi xoá bản đầu = xoá bản MỚI nhất, giữ bản cũ), làm hỏng thêm bản ghi vừa ghi. Nguyên nhân thứ 2 (19 máy, chủ yếu iOS với device_id dạng UUID hợp lệ, không trùng): ứng dụng KHÔNG BAO GIỜ gọi API cập nhật mã đẩy — đăng nhập xong chỉ liên tục gọi API lấy mã và nhận rỗng (vd 9C45B568-01DB-4957-A7B6-DAE39AFFFA73 của tài khoản 47350, DEBFC3EA-F83E-4165-A536-58110901881B của tài khoản 60057). Phần này nằm ở PHÍA ỨNG DỤNG (người dùng từ chối quyền thông báo, hoặc lấy mã Firebase thất bại) — máy chủ không có dấu vết vì API không được gọi, KHÔNG sửa được ở phía web.

## 2. Cách fix

<!-- Nguyên văn journal AI AUTO-FIXBUG 2026-08-13T11:21:51Z, mục ■ 2. CÁCH FIX. Giữ nguyên cách chia 5 khối "PHẦN ĐÃ CÓ / PHẦN VỪA THÊM" của Dev. -->

**PHẦN ĐÃ CÓ (fix gốc theo device_id trùng):** API cập nhật mã đẩy thông báo (Api/MobileController::updateFirebaseToken) resolve người dùng từ mã người dùng TRƯỚC, rồi tra bản ghi theo device_id + hệ điều hành + NGƯỜI DÙNG; có thì chỉ cập nhật mã đẩy + cờ đăng ký chủ đề của ĐÚNG bản ghi đó (theo id, không cập nhật hàng loạt theo thiết bị, không ghi đè cột người dùng), không có thì tạo bản ghi mới — mỗi người dùng có bản ghi riêng trên cùng một device_id nên máy của người khác không bị chiếm. Đảo chiều đoạn dọn trùng: chỉ dọn trong phạm vi người dùng + thiết bị + hệ điều hành, GIỮ bản mới nhất (id lớn nhất) và xoá các bản cũ hơn bằng một câu xoá duy nhất. Vá 2 chỗ hệ quả: API đăng xuất (Api/AuthMobileController::logout) lấy người dùng đang đăng nhập TRƯỚC khi đăng xuất rồi mới tìm bản ghi kèm người dùng đó, có chốt chặn khi không lấy được người dùng; API lấy mã đẩy (getFirebaseToken) ở nhánh dự phòng chỉ nhận bản ghi CHƯA gắn mã người dùng hoặc gắn đúng mã đang hỏi (ưu tiên bản mới nhất). Bỏ ghi mã đẩy nguyên văn ra log.

**PHẦN VỪA THÊM (theo Redmine #39635 — token mới bị xoá mất, bản còn lại giữ token cũ):** sửa mâu thuẫn giữa 2 khối trong cùng hàm updateFirebaseToken — khối cập nhật lấy bản ghi bằng truy vấn KHÔNG sắp xếp (thực tế trả bản id NHỎ nhất) rồi ghi mã đẩy mới vào đó, trong khi khối dọn trùng ngay bên dưới lại GIỮ bản id LỚN nhất và xoá các bản nhỏ hơn ⇒ chính bản vừa ghi mã đẩy mới bị xoá, bản sống sót giữ mã đẩy CŨ và cờ đăng ký chủ đề vẫn = 1 nên lệnh nền firebase:subscribe_topic (chỉ xử lý cờ 0 và 2) không đăng ký lại chủ đề ⇒ máy vẫn không nhận được thông báo. Đã thêm sắp xếp id giảm dần vào truy vấn tra bản ghi để bản được cập nhật CHÍNH LÀ bản mà khối dọn trùng giữ lại (khi tạo mới thì bản mới cũng luôn là id lớn nhất), bảo đảm bất biến: sau mỗi lần gọi API, mỗi người dùng chỉ còn 1 bản ghi trên mỗi thiết bị + hệ điều hành, mang mã đẩy MỚI và cờ đăng ký chủ đề = 0; bản ghi của người dùng khác trên cùng device_id không bị đụng. Giữ nguyên cách dọn trùng bằng id lớn nhất (thay vì xoá theo id vừa ghi) vì nó an toàn hơn với 2 request tạo mới song song — cả hai cùng giữ lại một bản, không xoá lẫn nhau. Rà cùng lỗi 'truy vấn không sắp xếp' ở 2 chỗ còn lại của chính luồng mã đẩy này (dữ liệu cũ vẫn còn bản trùng cho tới khi ứng dụng gọi lại API): đăng xuất (Api/AuthMobileController::logout) nay đánh dấu huỷ đăng ký chủ đề vào bản MỚI nhất — trước đây có thể đánh dấu vào bản cũ khiến bản đang dùng vẫn theo chủ đề, người đã đăng xuất vẫn nhận thông báo; và nhánh chính của getFirebaseToken lấy bản MỚI nhất — trước đây có thể trả mã đẩy + bot đang chọn đã cũ.

**PHẦN VỪA THÊM (theo spec bổ sung — Redmine #39636: API lấy mã đẩy vẫn trả mã đẩy + số thông báo chưa xem của NGƯỜI KHÁC):** ở API lấy mã đẩy (Api/MobileController::getFirebaseToken), nhánh dự phòng dành cho ứng dụng còn giữ mã người dùng cũ trước đây nhận bản ghi có cột mã người dùng CHƯA gắn (NULL) HOẶC gắn đúng mã đang hỏi. Đã kiểm chứng bằng quét toàn bộ app/: cột mã người dùng của bảng user_firebase_token (thêm 2022 kèm migration, mọi bản ghi cũ để trống) chỉ được ghi duy nhất tại chính nhánh dự phòng này — hàm cập nhật mã đẩy tạo bản ghi mới KHÔNG hề set cột này, đăng nhập/đăng xuất chỉ đụng cột mã người dùng của bảng users ⇒ gần như 100% bản ghi để trống ⇒ vế NULL luôn đúng ⇒ truy vấn thoái hoá thành 'lấy bản ghi mới nhất của device_id đó'. Vì device_id ứng dụng Android gửi lên là build ID của ROM (BP4A.251205.006 có 135 tài khoản dùng chung), chỉ cần gọi API với mã người dùng sai/rác kèm device_id công khai đó là API trả về mã đẩy Firebase + số thông báo chưa xem của người dùng khác, đồng thời GHI ĐÈ mã rác đó vào bản ghi của họ (chiếm bản ghi). Đã bỏ vế NULL: nhánh dự phòng chỉ nhận bản ghi gắn ĐÚNG mã người dùng đang hỏi (mã là chuỗi bí mật 60 ký tự nên khớp đúng mới đủ định danh, ưu tiên bản mới nhất), và bỏ luôn đoạn ghi mã người dùng vào bản ghi chưa gắn (chính là cơ chế chiếm bản ghi, nay không còn tới được). Không xác định được người dùng thì API trả về rỗng như trường hợp 'không có người dùng' vốn đã có sẵn, không đổi cấu trúc phản hồi.

**CHẶN THÊM MÃ NGƯỜI DÙNG RỖNG (bắt buộc để bản vá trên có tác dụng):** Eloquent tự đổi where('user_token', null) thành 'WHERE user_token IS NULL' (đã kiểm tại vendor/laravel/framework Query/Builder::where), nên gọi API mà KHÔNG gửi mã người dùng sẽ khớp bừa một tài khoản chưa từng đăng nhập ứng dụng (cột mã còn trống) — đúng lại lỗi trả dữ liệu của người khác. Đã thêm chốt chặn mã rỗng cho cả 3 API cùng luồng trong file này: lấy mã đẩy (trả rỗng), cập nhật mã đẩy (không ghi mã đẩy của máy này vào tài khoản khớp nhầm), xoá mã đẩy (không xoá mất bản ghi đẩy của tài khoản khớp nhầm).

**PHẦN VỪA THÊM (theo spec bổ sung của dev — "$userFirebaseTokenCheck cần where theo user_id và os, không cần theo user_token"):** ở API lấy mã đẩy (Api/MobileController::getFirebaseToken) đã BỎ HẲN nhánh dự phòng tra người dùng qua cột mã người dùng của bảng bản ghi mã đẩy ($userFirebaseTokenCheck) — vòng trước mới chỉ siết nhánh này thành 'chỉ nhận bản ghi gắn ĐÚNG mã người dùng đang hỏi'. Nay người dùng CHỈ được xác định từ bảng người dùng (users.user_token, chuỗi bí mật cấp lúc đăng nhập); không xác định được thì API trả rỗng để ứng dụng đăng ký lại, KHÔNG đoán chủ nhân theo thiết bị nữa (cột mã người dùng trên bảng bản ghi mã đẩy chỉ được ghi tại chính nhánh dự phòng đó nên gần như mọi bản ghi đều để trống ⇒ điều kiện luôn đúng ⇒ trả bản ghi mới nhất bất kỳ của device_id, mà device_id ứng dụng Android gửi lên là build ID của ROM dùng chung hàng trăm máy). Sau khi có người dùng, truy vấn bản ghi mã đẩy nay tra theo NGƯỜI DÙNG + HỆ ĐIỀU HÀNH (kèm device_id, lấy bản mới nhất) đúng như spec, đồng nhất với API cập nhật mã đẩy và API đăng xuất. LƯU Ý dev: bản ứng dụng hiện tại gọi API lấy mã đẩy CHỈ gửi device_id + mã người dùng, KHÔNG gửi hệ điều hành (đã kiểm trong mã nguồn ứng dụng Flutter: lib/service/networking/apis/fcm_api.dart) — nếu ép điều kiện hệ điều hành khi ứng dụng không gửi thì câu lệnh thành 'hệ điều hành IS NULL', không khớp bản ghi nào và API sẽ luôn trả mã đẩy rỗng cho mọi khách; vì vậy điều kiện hệ điều hành chỉ áp dụng KHI ứng dụng có gửi lên (dùng when(!empty($os))), ứng dụng cập nhật gửi thêm hệ điều hành là tự động lọc đúng. Cột mã người dùng của bảng bản ghi mã đẩy sau thay đổi này không còn chỗ nào đọc/ghi (giữ nguyên cột, không đụng cấu trúc bảng).

**PHẦN VỪA THÊM (theo spec bổ sung của dev — "userFirebaseToken bỏ where os"):** ở API lấy mã đẩy (Api/MobileController::getFirebaseToken) đã BỎ HẲN điều kiện hệ điều hành khi tra bản ghi mã đẩy — vòng trước còn áp điều kiện này theo kiểu "chỉ lọc khi ứng dụng có gửi lên" (when(!empty($os))), nay bỏ luôn cả khối đó. Truy vấn chỉ còn: theo thiết bị (device_id) + NGƯỜI DÙNG (user_id đã xác định từ users.user_token), lấy bản mới nhất (id giảm dần). Lý do: bản ứng dụng hiện tại gọi API lấy mã đẩy CHỈ gửi device_id + mã người dùng, không gửi hệ điều hành (đã kiểm trong mã nguồn ứng dụng Flutter: lib/service/networking/apis/fcm_api.dart), nên điều kiện hệ điều hành hoặc vô tác dụng, hoặc (nếu ép cứng) biến thành "hệ điều hành IS NULL" khiến API luôn trả mã đẩy rỗng; bỏ hẳn cho đơn giản và không còn nhánh điều kiện thừa. An toàn về quyền riêng tư vẫn giữ nguyên vì điều kiện chốt là NGƯỜI DÙNG (user_id) chứ không phải thiết bị. LƯU Ý dev: nếu cùng một người dùng có bản ghi trên nhiều hệ điều hành mà device_id lại trùng nhau (device_id ứng dụng Android gửi lên là build ID của ROM), truy vấn sẽ lấy bản mới nhất bất kể hệ điều hành — chấp nhận theo yêu cầu; API cập nhật mã đẩy và API đăng xuất VẪN tra kèm hệ điều hành như cũ (không đụng tới).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN. Dev list dạng plain → convert sang bảng template, giữ nguyên chữ của Dev ở cột "Lý do". -->

| # | Function / File | Thay đổi (nếu có) | Lý do (nguyên văn Dev) |
|---|---|---|---|
| 1 | `insertMobileNotify` — `app/Helpers/functions.php` | Không sửa (vòng 1 đã **rollback** phần đẩy thông báo trong hàm này) | hàm tạo thông báo dùng chung cho mọi loại |
| 2 | `FirebaseService::pushNotifyToTopic` — `app/Services/FirebaseService.php` | Không sửa | đẩy thông báo theo topic của bot |
| 3 | `MobileNotify` — `app/MobileNotify.php` | Không sửa | hằng số trạng thái |
| 4 | `MobileNotifyService::insertNotifySalon` / `insertNotifyLesson` — `app/Services/Notify/MobileNotifyService.php` | Không sửa | đều gọi vào hàm dùng chung nên hưởng fix |
| 5 | `HandlePushMessageNotify::handle` — `app/Console/Commands/HandlePushMessageNotify.php` | Không sửa | luồng gửi gộp theo lịch, **không bị ảnh hưởng** |
| 6 | `HandlePushMessageNotifyService` — `linect-service` | Không sửa | luồng gửi gộp bên job, **không bị ảnh hưởng** |
| 7 | `NotifyController` — `app/Http/Controllers/Api/NotifyController.php` | Không sửa | các truy vấn danh sách/đếm của ứng dụng lọc theo trạng thái đã gửi |
| 8 | `HandleSubscribeTopic` + `FirebaseService::subscribeTopic` | Không sửa | đã kiểm chứng cơ chế đăng ký topic vẫn dùng xác thực mới, **không phải nguyên nhân** |

> ⚠️ Bảng trên là **nguyên văn vòng 1** và **không được cập nhật** ở vòng 2/3. Không có dòng nào cho `getFirebaseToken`, cho **API xoá mã đẩy** (vòng 3 mới thêm chốt chặn), hay cho **2 API popup bảo trì** cùng file (Studio nêu ở REQ-011). Đây là **caller list thiếu** → Leader cần chất vấn Dev.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục ■ 4.1 — Dev CHỈ ghi "File thay đổi", KHÔNG list function. Tag F1/F2 do /new-task gán theo quy ước repo. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Dev chỉ ghi tên file, không list function>` | `app/Http/Controllers/Api/MobileController.php` | Direct | Nguyên văn mục 4.1 của Dev. Từ mục 1+2 suy ra ít nhất: `updateFirebaseToken`, `getFirebaseToken`, **API xoá mã đẩy** (vòng 3 thêm chốt chặn `user_token` rỗng cho cả 3) |
| F2 | `<Dev chỉ ghi tên file, không list function>` | `app/Http/Controllers/Api/AuthMobileController.php` | Direct | Nguyên văn mục 4.1 của Dev. Từ mục 2 suy ra: `logout` |
| F3 | `HandleSubscribeTopic` (job `firebase:subscribe_topic`) | `app/Console/Commands/HandleSubscribeTopic.php` | Indirect | **Dev KHÔNG ghi ở 4.1** nhưng ghi ở 4.3 ("đầu vào không đổi, nhưng dữ liệu vào đã đúng chủ"). Studio có REQ-006 cho job này |
| F4 | 2 API ẩn / đọc popup thông báo bảo trì (cùng file `MobileController.php`) | `app/Http/Controllers/Api/MobileController.php` | **Chưa fix — khoảng trống cùng root cause** | **Dev KHÔNG ghi ở bất kỳ mục nào.** Studio REQ-011: 2 API này "vẫn tra và cập nhật theo mã thiết bị + hệ điều hành không kèm mã người dùng", không nằm trong diff → **leader quyết mở phạm vi ticket hay tách ticket mới** |
| F5 | Lệnh `recover:user_firebase_token` (chạy tay, không có trong lịch) | `<chưa rõ file>` | **Cố ý KHÔNG fix — còn lỗi cùng họ** | Dev tự nêu ở mục rủi ro: sau fix, 2 tài khoản trên cùng máy vật lý chung mã đẩy sẽ thành nhóm trùng → **lệnh sẽ xoá bản ghi của người vừa đăng nhập**. Đề nghị PM/leader quyết |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục ■ 4.2. Tag D1..D4 do /new-task gán. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú (nguyên văn Dev) |
|---|---|---|---|
| D1 | `user_firebase_token` (toàn bảng — mô hình dữ liệu) | CREATE / DELETE | từ nay mỗi (người dùng, device_id, hệ điều hành) là MỘT bản ghi riêng; trước đây mỗi (device_id, hệ điều hành) chỉ có 1 bản ghi bị chuyền tay giữa các người dùng. Số bản ghi của bảng sẽ tăng theo số tài khoản dùng chung một chuỗi device_id (bảng hiện rất nhỏ, ~79KB) |
| D2 | `user_firebase_token.user_id` | UPDATE (nay **không** còn ghi đè) | API cập nhật mã đẩy KHÔNG còn ghi đè cột này lên bản ghi đang có (chỉ gán khi TẠO bản ghi mới) |
| D3 | `user_firebase_token.status_subscribe_topic` | UPDATE | vẫn đặt về 0 mỗi lần ứng dụng gửi mã mới để lệnh nền đăng ký lại chủ đề; API đăng xuất vẫn đặt 2 nhưng nay đúng bản ghi của người vừa đăng xuất |
| D4 | Dữ liệu cũ đã bị chiếm (`user_firebase_token` tồn đọng) | Không migrate — **TỰ LÀNH** | các bản ghi đã bị chiếm không khôi phục lại được chủ cũ (cột người dùng đã bị ghi đè, không lưu vết) — nhưng TỰ LÀNH: người dùng bị mất bản ghi chỉ cần mở lại ứng dụng, lần gọi API cập nhật mã đẩy kế tiếp sẽ tạo bản ghi mới cho chính họ. Không cần và KHÔNG NÊN chạy lệnh `recover:user_firebase_token` (xem mục rủi ro) |
| D5 | `user_firebase_token.user_token` (cột mã người dùng của bảng token) | **Không còn đọc/ghi** | Từ mục 2 vòng 3: "Cột mã người dùng của bảng bản ghi mã đẩy sau thay đổi này **không còn chỗ nào đọc/ghi** (giữ nguyên cột, không đụng cấu trúc bảng)". **Dev KHÔNG ghi ở 4.2** — `/new-task` bổ sung từ mục 2 |

> ⚠️ **Không có migration / không thêm index**. Studio REQ-007 xác nhận: bảng **không có unique constraint** theo (device_id, os) → nhiều bản ghi cùng device_id là trạng thái hợp lệ, toàn bộ việc phân tách do **tầng ứng dụng** đảm nhiệm.
>
> ⚠️ Dev tự nêu: **chưa kiểm tra được bảng có index nào cho (device_id, os, user_id)** vì DB dev không chạy. Đề nghị dev kiểm `SHOW INDEX` trên môi trường thật.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục ■ 4.3. Tag T1..T5 do /new-task gán. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Notification Settings (FA-006)** — thông báo đẩy lên ứng dụng Elme: người dùng trên máy có device_id trùng không còn bị mất đăng ký mã đẩy nên nhận lại được thông báo | F1, D1, D2 | High |
| T2 | **System Notifications (FS-014)** — thông báo hệ thống đẩy lên ứng dụng đi cùng cơ chế mã đẩy/chủ đề bot nên cùng được khôi phục | F1, D1 | High |
| T3 | **Đăng nhập / đăng xuất ứng dụng** (`Api/AuthMobileController`) — luồng đăng xuất nay huỷ đăng ký chủ đề đúng người, không chạm bản ghi của tài khoản khác trên máy trùng device_id | F2, D3 | High |
| T4 | **Lệnh nền đăng ký chủ đề Firebase** (`firebase:subscribe_topic`) — đầu vào không đổi (vẫn đọc cờ 0/2), nhưng dữ liệu vào đã đúng chủ nên không còn gắn mã đẩy của máy này vào chủ đề bot của người khác | F3, D3 | High (job nền — **RULE-08**) |
| T5 | **Badge / đếm chưa đọc trên ứng dụng** — lấy theo (người dùng, bot) nên hưởng lợi gián tiếp khi bản ghi mã đẩy không còn bị chiếm | D1, D2 | Medium |

---

## 5. Rủi ro / lưu ý khi test (nguyên văn Dev — mục ■ TỰ REVIEW)

1. Lệnh `recover:user_firebase_token` (chạy tay, KHÔNG có trong lịch) vẫn còn nguyên lỗi cùng họ: gom theo (device_id, mã đẩy) rồi xoá bản MỚI nhất. Sau fix này, hai tài khoản trên CÙNG một máy vật lý có chung mã đẩy sẽ thành một nhóm trùng và lệnh sẽ xoá bản ghi của người vừa đăng nhập. Cố ý KHÔNG sửa vì đây là công cụ vận hành và tiền đề 'mỗi thiết bị 1 bản ghi' của nó đã không còn đúng — ĐỀ NGHỊ dev/PM quyết: ngừng dùng lệnh này hoặc mở ticket riêng viết lại theo (người dùng, thiết bị, hệ điều hành)
2. Một máy vật lý đăng nhập 2 tài khoản sẽ có 2 bản ghi cùng mã đẩy: chủ đề Firebase gắn theo MÃ ĐẨY chứ không theo người dùng nên tại một thời điểm máy chỉ theo được chủ đề của một tài khoản (lệnh nền có bước huỷ đăng ký các chủ đề không thuộc bot của người dùng hiện tại). Đây là giới hạn sẵn có của cơ chế chủ đề, không phải do fix này gây ra, và luồng đăng xuất đúng vẫn dọn sạch
3. Chưa kiểm tra được bảng có chỉ mục nào cho (device_id, os, user_id) hay không vì DB dev không chạy và bản lược đồ trong kho tham chiếu đã bị lược bỏ chỉ mục. Bảng rất nhỏ (~79KB) nên không lo hiệu năng, nhưng nếu muốn chắc thì dev kiểm SHOW INDEX trên môi trường thật
4. Không sửa được nhóm 19 máy iOS chưa từng gọi API đăng ký — cần đội ứng dụng kiểm tra quyền thông báo và bước lấy mã Firebase; đây là phần còn lại của ticket sau khi phía web đã đúng
5. Đề xuất số 2 trong phân tích (ứng dụng Android gửi mã máy thật thay vì build ID của ROM) thuộc phía ứng dụng, KHÔNG nằm trong thay đổi này. Fix phía web đã đủ để hết chồng lấn, nhưng nếu ứng dụng sửa được thì dữ liệu sẽ sạch hơn
6. Bản ghi trùng CŨ đang tồn tại chỉ được dọn khi ứng dụng gọi lại API cập nhật mã đẩy cho đúng cặp (người dùng, thiết bị, hệ điều hành) đó. Máy nào không mở lại ứng dụng thì dữ liệu trùng vẫn nằm im — không gây lỗi thêm (mọi truy vấn của luồng nay đều ưu tiên bản mới nhất) nhưng nếu muốn sạch ngay thì cần dev chạy một câu dọn dữ liệu thủ công, KHÔNG dùng lệnh `recover:user_firebase_token` sẵn có vì lệnh đó còn lỗi cùng họ (xem rủi ro bên trên).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### ⚠️ Điểm cần chất vấn Dev (do `/new-task` phát hiện khi parse — Leader tự quyết)

1. **Mục 3 + 4.1/4.2/4.3 là bản của vòng 1, không cập nhật sau 2 vòng sửa thêm** → caller list và impact list có thể lạc hậu so với commit `3233088f19`.
2. **4.1 không list function**, chỉ list 2 file → không map được impact xuống mức function để viết TC.
3. **API xoá mã đẩy** được sửa ở vòng 3 (thêm chốt chặn `user_token` rỗng) nhưng **không xuất hiện** ở mục 3 hay 4.1/4.3.
4. **2 API popup bảo trì** cùng file vẫn tra theo device_id không kèm user (Studio REQ-011) — Dev **không nhắc**. Cùng root cause, chưa fix.
5. **Verify mức `static`** + **DB dev không chạy** → toàn bộ khẳng định về hành vi SQL chỉ là suy luận trên query builder, chưa chạy thật.
6. **#39635 và #39636 không được set `relations`** trên Redmine → tra cứu liên ticket phải đọc journal.
7. **Nguyên nhân 2 (19 máy iOS) không được fix** — nhưng journal QA lại ghi *iOS nhận được, Android không nhận*. Cần xác định triệu chứng của khách `rintaro@ssks.work` thuộc nhóm nào để biết fix này có đóng được bug của khách hay không.
