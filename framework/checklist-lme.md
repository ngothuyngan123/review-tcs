# Checklist LME — Cho review TCs

> **Nguồn**: Tổng hợp **đúng 3 sheet** từ file checklist dự án LME — [Google Sheet](https://docs.google.com/spreadsheets/d/1oO95JR4Na9Fyzi5-GeFLJIk54YW8kHVrM8V6m2sIG5U/edit):
>
> 1. Sheet **Checklist web**
> 2. Sheet **Checklist job**
> 3. Sheet **Các tính năng chung**
>
> Các sheet khác (Checklist gốc, UI checklist, Các tính năng riêng, Data Input, Media-Lme, Old, Info) **không** được đưa vào file này.
>
> **Cách dùng khi review**: Leader dùng file này để verify member đã "base checklist" của dự án chưa — đây là tiêu chuẩn bắt buộc ở [framework/review-checklist.md](review-checklist.md) mục F.
>
> **Sync**: Chạy `uv run scripts/fetch_sheet.py 1oO95JR4Na9Fyzi5-GeFLJIk54YW8kHVrM8V6m2sIG5U "Checklist web" "Checklist job" "Các tính năng chung"` để sync lại.
>
> Ngày fetch: 2026-04-24

---

## A. Checklist web

### A.1 Function checklist

| ID | Ngày add | Main checklist | Sub / ghi chú |
|----|----------|----------------|---------------|
| **CL22** | 2026-04-16 | Đối với **tất cả các chức năng upload file**: check path URL **trước và sau khi save** → đảm bảo path giống nhau. Check preview sau upload (chưa click save) và sau khi save → đảm bảo preview bình thường. | VD: Màn template, sau khi upload video (chưa click save) vẫn preview mở video bt, và sau khi save vẫn preview và mở video bt. |
| **CL21** | 2026-03-03 | Về các format dữ liệu hiển thị phía line user: chú ý format datetime theo đúng design (**dấu ngoặc Nhật** nếu có), **dấu cách** theo design là cách Nhật hay cách thường. Format khi **web send / send test / job send** phải hoàn toàn giống nhau về hiển thị. | |
| **CL20** | 2026-02-24 | Khi version up đã test lại case **hủy hợp đồng** hay chưa? Khi hết hạn hợp đồng các tính năng không được chạy nữa. | Khi hủy hợp đồng: **1)** Clear toàn bộ richmenu của line user. **2)** Hủy hết các schedule: Schedule Broadcast / Step message / Remind (event, lesson, salon, form) / Action schedule / Schedule send từ chat 1:1 / Schedule send từ message error / Schedule hiển thị-stop richmenu. **3)** QR code: không được chạy action nữa. |
| **CL19** | 2026-02-24 | Tính năng cần hiển thị trigger trên chat 1:1 → đã hiển thị **đầy đủ** trigger hay chưa? | |
| **CL18** | 2026-01-28 | Khi test deploy luôn có case **load UI trước và submit sau** với trường hợp release không lock maintain. | VD: để sẵn màn form phía line user lúc chưa release → sau khi release submit form. Expect: vẫn submit bình thường (lưu result, ghi google spread, action form...). |
| **CL17** | 2026-01-27 | Khi test tính năng liên quan đến **setting action**: **DB** — nếu xóa hết `action_detail` thì phải xóa `action_id` trong setting action đó. **GUI** — kiểm tra lại màn list, màn detail, các chỗ preview action **không bị lỗi** khi xóa hết action. | |
| **CL16** | 2026-01-07 | Tính năng liên quan đến tạo file (ảnh/audio/video/PDF/CSV...) phải có quan điểm **xóa file** khi xóa/change file mới → **không để lại file rác**. Xóa cả server local và server B2. | VD: change ảnh A → B phải xóa ảnh A khỏi server. Check access link ảnh trả về **404** là đúng. Trên production check cả 2 server: verify `p.lmes.jp/...?v=x` trả 404 là đã xóa. |
| **CL15** | 2025-11-24 | Tính năng **phân trang** — kiểm tra hành vi scroll khi chuyển page/rẽ nhánh. | Khi next sang page khác phải tự động **scroll lên đầu page**. |
| **CL14** | 2025-11-19 | Rule đặt tên và validate dữ liệu: `{tên tính năng}_{tên quản lý}_yyyymmdd_hhmmss`. Tên tính năng lấy tên menu. Tên quản lý: **validate ký tự đặc biệt không cho nhập + không cho trùng**. | |
| **CL13** | 2025-08-26 | **[Line Friend]** Các tính năng access link tool LME (Form, Item, Event, Salon, Lesson, Conversion, QR code): check user LINE đã là friend chưa? Nếu chưa → redirect sang màn kết bạn. | Test case: open in app LINE / open trình duyệt ngoài / open từ button (nếu có) / open từ PC (nếu có). |
| **CL12** | 2025-08-08 | Đã check **max** cho toàn bộ dữ liệu chưa? (Nếu spec không nói thì nego với KH để tránh lỗi về sau) | Max ký tự / max số lượng item. |
| **CL11** | NA | CRUD **đúng bản ghi** account đang test — không hiển thị/update nhầm account khác. | Check khi update/delete đã `WHERE` đúng điều kiện (`bot_id`, `staff_id`, `course_id`, `date`...) bằng cách tạo bản ghi có cùng dữ liệu ở 2 account, 2 staff → kiểm tra DB verify. |
| **CL10** | NA | Case update/delete data liên quan ảnh hưởng dữ liệu hiện tại như nào? | Xóa 1 item gốc → các chỗ khác có chứa item có còn hiển thị? Có lỗi không? Update 1 item gốc → các màn khác có hiển thị update chưa? |
| **CL9** | NA | Tính năng **search** theo từ khóa. | Search text tiếng Nhật? Result search khi có phân trang/loadmore? |
| **CL8** | NA | Function có tính năng **copy/preview** → đã kiểm tra lại chưa? | |
| **CL7** | NA | Các tính năng liên quan **giới hạn plan** (xem [file giới hạn plan](https://docs.google.com/spreadsheets/d/1_GdktZFY3QVP2Vg_z2pu_odIAYPWLRk15Yn9sho3Ksg/edit)). | 5 case: tạo mới / copy / khôi phục (soft-delete) / mở 2 tab → thao tác / double click ở lần limit cuối. **Phân server**: Dev + Staging + Product → test mọi tính năng bằng **account staff + free** (tính năng cần check limit plan thì check lại của các plan khác). |
| **CL6** | NA | Check data input khác (tham khảo sheet Data Input). | Data đã check nhập text Nhật? Đã nhập số 0? Area text có enter? Tự resize form? Validate invalid? **Upload ảnh**: tự resize nếu w/h > 2048px (giữ nguyên tỷ lệ). Ảnh > 10,000px KHÔNG cho upload. Test aspect với rule **fix chiều rộng, giãn chiều cao**. Upload theo recommend size trong design (e.g. `推奨 1000×500`) → check hiển thị mọi chỗ có bị co/giãn không. |
| **CL5** | NA | **Double click** ở các button có bị duplicate bản ghi không? | |
| **CL4** | NA | Check các **thao tác liên tục**. | Add→Add tiếp; Xóa→Xóa tiếp; Xóa→Add mới; Sort xong edit trạng thái; Add mới→Sort; Edit→Sort; Xóa→Sort; Sort→Sort tiếp; Edit→Edit tiếp; ... |
| **CL3** | NA | Check thao tác **chuyển tab setting** khác. | Màn nhiều tab → check chuyển qua lại giữa tab xem dữ liệu có bị thay đổi sau save không. |
| **CL2** | NA | Sau khi **save/sửa/xóa/sort** → check reload màn hình có lỗi gì không. | |
| **CL1** | NA | Test **account staff**. | Staff không được phân quyền → không được access. Staff được phân quyền → thao tác giống account chính. |

### A.2 Non-function checklist

#### URLs đo lường conversion — **KHÔNG được thay đổi** khi có CR
- Đăng ký user thành công: `https://step.lme.jp/register/success`
- Top khi đăng ký user và login: `https://step.lme.jp/admin/home`
- Top sau khi login (đã có bot): `https://step.lme.jp/basic/overview`
- Bill standard tháng thành công: `https://step.lme.jp/monthly/standard_success`
- Bill standard năm thành công: `https://step.lme.jp/yearly/standard_success`
- Bill pro tháng thành công: `https://step.lme.jp/monthly/pro_success`
- Bill pro năm thành công: `https://step.lme.jp/yearly/pro_success`
- Kết nối bot thành công: `https://step.lme.jp/admin/bot-add-v2?status=successful`

#### Regression test (hồi quy)
- [ ] Đã verify các chức năng đã list trong **effect range** của Dev
- [ ] Từ quan điểm Tester, task có khả năng ảnh hưởng chức năng khác không? Nếu có → list effect:
  - [ ] Tính năng mới có update DB không? Nếu có → check lại **backup + copy**
  - [ ] Phía **job** có cần update không?
  - [ ] Phía **app mobile** có cần update không?
  - [ ] Có tính năng nào khác liên quan đến update lần này không?
- [ ] Data cũ chạy bình thường sau khi update code mới

#### Security Testing — khi có màn hình mới (URL mới)
- [ ] Gõ trực tiếp URL khi chưa đăng nhập → **redirect** login
- [ ] Sau khi login → đổi param ID của URL bằng của user/bot khác → **từ chối** access
- [ ] Check access URL khi staff không được cấp quyền (của BOT hoặc của MH template)

#### Compatibility Testing
- [ ] Web: check cả **Win + Mac** (chrome + safari)
- [ ] App: test cả **Android + iOS**

---

## B. Checklist job

> Sheet này hiện tại chỉ có 2 loại job + 1 item. Team sẽ bổ sung dần.

### B.1 Job callback
_(Chưa có item nào được ghi nhận trong sheet)_

### B.2 Job sync Java

| ID | Ngày add | Main checklist | Sub |
|----|----------|----------------|-----|
| **CLJ01** | 2026-04-16 | **Sync Google**: kiểm tra rate limit từ docs API của Google → tạo TCs với **dữ liệu request lớn và liên tục** để kiểm tra việc retry của job. | Đảm bảo job sync lỗi có **retry**. Hạn chế việc xảy ra **rate limit** với các API thứ 3. |

---

## C. Các tính năng chung

> Khi bug/feature chạm đến 1 trong các màn hình dưới → bắt buộc check đủ các mục tương ứng, phân theo **Type** (Admin web / Admin app / Line user / Job / Cả admin và user / Cả web và job).

### C.1 Bill tiền

- [ ] **Admin web** — Bill tiền có case **delay của callback** đã check chưa?
- [ ] Các tính năng sử dụng bill tiền trên tool:
  - [ ] Bill tiền **bot**
  - [ ] Bill tiền **item**: item 1 lần + item chu kỳ
  - [ ] Bill tiền **salon**
  - [ ] Bill tiền **lesson**
  - [ ] Bill tiền **event booking**

#### Error scenarios — phải cover khi fix chạm payment gateway (Univapay / Stripe / 3D Secure)

> Khi cách fix là **generic error handler** ("set error message", "return error", "handle exception" tại payment controller) → bắt buộc cover **≥ 4 error type** dưới đây. Dùng test card numbers của Univapay/Stripe sandbox để trigger.

- [ ] **Card declined** (`decline_code: card_declined`)
- [ ] **Insufficient funds** (`decline_code: insufficient_funds`)
- [ ] **Expired card** (`decline_code: expired_card`)
- [ ] **3D Secure fail / authentication failed** (`three_ds_failed`)
- [ ] **Amount exceeded max** (`amount_exceeded` / `amount_too_large`)
- [ ] **Amount below min** (`amount_too_small`)
- [ ] **Network timeout / API 5xx** (gateway down)
- [ ] **Unknown error code** (mock gateway trả error code chưa được handle riêng → verify fallback generic message hiển thị)
- [ ] **Duplicate transaction** (cùng order_id submit 2 lần)
- [ ] **Account suspended / 不正利用検知** (gateway block account)

**Verify**: với mỗi error type → frontend hiển thị **message lỗi business-friendly** (không phải raw API error), KHÔNG silent fail (không tự đóng màn / không quay về talklist im lặng), có UX recovery (nút quay lại / nút thử lại).

### C.2 Send message

#### Yêu cầu cơ bản (cover cả admin và user)
- [ ] Gửi **đúng thứ tự** — khi test tính năng nào thì confirm lại logic cũ trước đó
- [ ] **Replace** các content (name, friend info) chưa?
- [ ] Check **trigger hiển thị** trên chat 1:1 của web + app
- [ ] **Preview message** ở các màn hiển thị đúng chưa?
- [ ] **Profile sender** đã đúng chưa?
- [ ] Có update `last_message` và `last_time_message` hay không? (tùy logic)
- [ ] Gửi đúng **filter** chưa
- [ ] Gửi bị **duplicate** không?
- [ ] Có bị lỗi: không gửi được msg hoặc gửi sai account khác không?

#### 12 nguồn send từ **JOB** — phải cover
1. **Broadcast**
2. **Scenario**
3. **Event remind** (remind cũ + remind mới của salon, lesson, form)
4. **Action khi có callback**: add friend thường, landing; auto reply
5. **Delay message** của template (random msg)
6. **Send schedule** cho `message_error` (`sending_schedule_setting`) → resend msg error
7. **Send schedule chat** cho user đặt lịch (`schedule_send_chat`) → đặt lịch send ở chat 1:1
8. **Action schedule**
9. **Postback**: button / rich menu / image map / video
10. **Toàn bộ action ở các tính năng khác**: form / booking calendar / booking event / tag / friend info / item bill tiền / url / conversion
11. **Send test ở scenario**
12. **Send action ở friend list**

#### 7 nguồn send từ **WEB** — phải cover
1. **Chat 1:1**
2. **Friend list** → từ 03/2026 đã chuyển hết sang job send
3. **Add tag**
4. **Send test** — ở màn: template / broadcast / scenario (send từng step msg) / remind
5. **Send message reply** ở màn talklist
6. **Remind** — case message kiểu gửi ngay
7. **Send action text** (msg độc lập) của: salon / lesson / kết bạn / QR / form

#### Từ **App Admin**
- [ ] Send chat 1:1
- [ ] Add tag
- [ ] Approve/deny booking salon
- [ ] Approve/deny booking lesson

#### Case message error — Admin web
- [ ] Lưu **đúng error** chưa?
- [ ] Check case **resend**

#### Case friend block — Line user
- [ ] Friend đã bị block / friend block bot → **KHÔNG** send message (không action + không remind)

### C.3 Friend info

#### 3 loại folder — tính năng liên quan hiển thị phải check đủ
- [ ] Folder **chưa phân loại**
- [ ] **2 folder default**
- [ ] Các folder do **admin tạo**

#### Nơi hiển thị friend info — Admin web
- [ ] Quản lý info friend — `/basic/friend-information`
- [ ] Quản lý info friend → list friend có info — `/basic/friend-information/item/{id}`
- [ ] Chat 1:1 → Right bar
- [ ] My page → Tab 基本情報
- [ ] Quản lý CSV → Export CSV
- [ ] Màn phân tích cross: setting trục tham chiếu case chọn `友だち情報` — `/basic/cross-analysis/result-cross/{id}`
- [ ] Modal **action**
- [ ] Modal **filter**

#### Nơi hiển thị friend info — Line user (khi booking / mua / trả lời form)
- [ ] Event booking
- [ ] Lesson booking
- [ ] Salon booking
- [ ] Item (khi mua)
- [ ] Form (khi trả lời)

#### Nơi hiển thị friend info — Admin app
- [ ] App mobile → Màn my page

#### Nơi **update** friend info
| Type | Chỗ update |
|---|---|
| Admin web | Chat 1:1 → right bar |
| Admin web | My page → update friend info |
| Job | QR landing có set import param → update sau khi kết bạn |
| Job | CSV → import file CSV |
| Cả web và job | Multi action |
| Line user | Event booking → admin tạo form nhập info → user trả lời |
| Line user | Lesson booking (tương tự) |
| Line user | Salon booking (tương tự) |
| Line user | Item (tương tự) |
| Line user | Form (tương tự) |
| Admin app | App mobile → màn my page |

#### Insert code friend info + replace dữ liệu động (cả admin và user)
- [ ] Modal **multi action** → action text có insert friend info — check hiển thị: line user / chat 1:1 web / chat 1:1 app
- [ ] **Template text** insert friend info — check hiển thị: line user / chat 1:1 web / chat 1:1 app
- [ ] **Remind** — check hiển thị: line user / chat 1:1 web / chat 1:1 app

### C.4 Tag

#### Nơi hiển thị tag — Admin web
- [ ] Quản lý tag → list tag
- [ ] Chat 1:1 → Right bar
- [ ] My page → Tab タグ
- [ ] Quản lý CSV → Export CSV
- [ ] Tính năng form (item gắn tag): item trả lời 1 lần (radio, droplist) + item checkbox
- [ ] Cross analysis
- [ ] Modal **multi action**
- [ ] Modal **filter**

#### Nơi hiển thị tag — Admin app
- [ ] App mobile: màn chat 1:1 + màn My page

#### Nơi **update** tag — Admin web
- [ ] Chat 1:1 → Right bar
- [ ] My page → Tab タグ
- [ ] Quản lý CSV → Import CSV
- [ ] Trả lời form: item có gắn tag (radio/droplist/checkbox)
- [ ] Modal multi action

#### Nơi update tag — Admin app
- [ ] App mobile: chat 1:1 + My page

### C.5 Google sheet

- [ ] Các tính năng liên kết Google spread (Admin web):
  - [ ] Form answer
  - [ ] Salon
  - [ ] Lesson
  - [ ] QR code
- [ ] Lúc liên kết mà **chưa cấp quyền** → hiển thị msg báo lỗi, không cho liên kết
- [ ] Sau khi liên kết mà **mất quyền / mất liên kết** → hiển thị **alert cảnh báo** để user liên kết lại
- [ ] File name tạo ra lúc liên kết có chứa **ký tự đặc biệt** thì có lỗi không?
- [ ] Case tiêu đề cột ở spread có **xuống dòng** hay chưa?
- [ ] Khi có update của tính năng cần test lại **job retry** (hiện tại: Salon, Lesson, Form có job retry nếu sync google bị lỗi)
  - Riêng **Form**: Google spread có **2 loại header** mới + cũ → test cả 2:
    - Header cũ: chỉ có 1 cột tên người trả lời
    - Header mới: 2 cột — Tên LINE + Tên hệ thống (システム表示名)

### C.6 Google calendar
_(Chưa có item nào được ghi nhận trong sheet)_

### C.7 Các tính năng liên quan giới hạn plan

- [ ] Tham chiếu [file giới hạn plan](https://docs.google.com/spreadsheets/d/1_GdktZFY3QVP2Vg_z2pu_odIAYPWLRk15Yn9sho3Ksg/edit)
- [ ] Test giới hạn lúc **tạo mới**
- [ ] Test giới hạn lúc **copy**
- [ ] Test giới hạn lúc **khôi phục data đã xóa** (với tính năng xóa mềm)
- [ ] Test case **mở 2 tab** → thao tác
- [ ] Test **double click** ở lần limit cuối
- [ ] Phân server:
  - **Dev**: account **free** (+ check các plan khác cho tính năng có limit)
  - **Staging**: account **pro** (+ check các plan khác cho tính năng có limit)
  - **Product**: account **standard** (+ check các plan khác cho tính năng có limit)

### C.8 Tính năng sort (màn nào có sort)

| Type | Màn hình |
|---|---|
| Admin web | **Sort folder** ở các màn hình |
| Admin web | **Sort bot** ở overview |
| Admin web | **Chat 1:1**: sort hiển thị info friend + sort status chat |
| Admin web | **My page** → sort hiển thị info friend |
| Admin web | Rich menu |
| Admin web | Image richmenu |
| Admin web | Scenario |
| Admin web | Auto reply |
| Admin web | Formanswer màn list |
| Admin web | Template |
| Admin web | Tag |
| Admin web | QR code |
| Admin web | Friend info |
| Admin web | Action schedule |
| Admin web | Remind |
| Admin web | Popup |
| Admin web | Booking event |
| Admin web | **Salon**: sort course/staff + sort item form |
| Admin web | **Lesson**: sort course + sort item form |
| Admin web | QL CSV |
| Admin web | QL item |
| Admin web | QL staff |
| Admin web | Conversion |
| Admin web | URL |
