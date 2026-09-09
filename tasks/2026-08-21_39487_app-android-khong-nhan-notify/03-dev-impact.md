# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU — ĐỌC TRƯỚC KHI CHẠY `/write-tc` HOẶC `/review-tc`**
>
> Redmine #39487 **KHÔNG có Section "Đánh giá ảnh hưởng" theo format 4 mục chuẩn**.
> Nội dung đánh giá nằm trong **journal #129164** (Thinh Nguyen, 2026-08-18) với cấu trúc **khác template**:
> `1. Lỗi` · `2. Nguyên nhân` · `3. Phạm vi và thời gian` · `4. Đã xử lý`.
>
> → Đã map raw text vào mục 1 và 2 bên dưới. **Mục 3 (caller đã check) và mục 4.1 / 4.2 / 4.3 KHÔNG có dữ liệu từ Redmine** — Dev chưa cung cấp.
> **Yêu cầu Dev bổ sung** mục 3 + 4.1/4.2/4.3 trước khi chốt coverage, hoặc Leader tự dựng từ Phụ lục A (nguồn Studio, không phải Redmine).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thinh Nguyen` (tác giả journal #129164 — người viết đánh giá). Redmine `assigned_to` hiện tại = `Đoàn Thị Bích Hảo` (tester). |
| Commit / Pull Request | **App fix**: https://bitbucket.org/sns-mobile-app/lme-fluter-app/commits/6daa49c382db3ffd3a4c0666f841d44dd8309a16 (`6daa49c`)<br>**Commit gây regression**: `dcd0f33` (14/07/2025, tác giả `hai`) |
| Branch | `master_branch_release_store` |
| Ngày submit đánh giá | `2026-08-18` (journal #129164, `created_on = 2026-08-18T03:20:24Z`) |
| Auto-filled | `2026-08-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #129164 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## Nguyên văn journal #129164 (Redmine — KHÔNG diễn giải)

```
1. Lỗi
Android gửi lên server một device_id không phân biệt được máy. Mọi máy cùng model và cùng bản firmware đều gửi một chuỗi giống hệt nhau.
Kiểm chứng trên Galaxy A55 (Android 16):
App đang gửi: BP4A.251205.006 ← mã bản dựng firmware, mọi A55 cùng bản đều giống
Đáng lẽ phải: 21c8d9d4da5a68b2 ← ANDROID_ID, riêng từng máy

2. Nguyên nhân
Commit dcd0f33 (14/07/2025, tác giả hai) migrate từ package device_info sang device_info_plus trong lúc nâng Android 15.
device_info_plus đã bỏ hẳn field androidId từ v4. Khi migrate, field bị thay bằng .id — tên gần giống nhưng ý nghĩa khác hoàn toàn

3. Phạm vi và thời gian
Lên store từ bản 2.8.6 (367) ngày 11/09/2025. iOS không ảnh hưởng.

Chức năng: 
- Đăng ký / xoá FCM token: Máy thứ hai đè token máy thứ nhất → mất thông báo. Logout một máy xoá token máy kia
- Badge số chưa đọc: Sai giữa các máy

Triệu chứng: thỉnh thoảng mất thông báo, mở lại app thì hết, rất khó tái hiện.

4. Đã xử lý
Backend (làm trước, tạm thời)

App — commit 6daa49c: https://bitbucket.org/sns-mobile-app/lme-fluter-app/commits/6daa49c382db3ffd3a4c0666f841d44dd8309a16
Branch: master_branch_release_store
- Dùng device_id Android đọc Settings.Secure.ANDROID_ID qua MethodChannel tự viết (MainActivity.kt), không thêm package mới. Chọn ANDROID_ID vì đúng bằng giá trị app dùng tới bản 2.8.5 → bản ghi cũ trên server tự khớp lại
```

---

## 1. Nguyên nhân

> Map từ journal mục `1. Lỗi` + `2. Nguyên nhân`.

App Android gửi lên server một `device_id` **không phân biệt được máy**: mọi máy cùng model + cùng bản firmware đều gửi một chuỗi giống hệt nhau.

- Kiểm chứng trên **Galaxy A55 (Android 16)**:
  - App đang gửi: `BP4A.251205.006` ← mã bản dựng firmware, mọi A55 cùng bản đều giống
  - Đáng lẽ phải: `21c8d9d4da5a68b2` ← `ANDROID_ID`, riêng từng máy
- **Root cause**: commit `dcd0f33` (14/07/2025, tác giả `hai`) migrate từ package `device_info` sang `device_info_plus` trong lúc nâng Android 15. `device_info_plus` **đã bỏ hẳn field `androidId` từ v4**; khi migrate, field bị thay bằng `.id` — tên gần giống nhưng ý nghĩa khác hoàn toàn.
- **Phạm vi / thời gian**: lên store từ bản **2.8.6 (367)** ngày **11/09/2025**. **iOS KHÔNG ảnh hưởng.**
- **Triệu chứng**: thỉnh thoảng mất thông báo, mở lại app thì hết, **rất khó tái hiện**.

## 2. Cách fix

> Map từ journal mục `4. Đã xử lý`.

**a) Backend** — *"làm trước, tạm thời"*. ⚠️ Journal **KHÔNG mô tả chi tiết** backend đã sửa gì. Xem Phụ lục A (nguồn ngoài Redmine) để biết chi tiết, hoặc hỏi Dev.

**b) App Android** — commit `6daa49c`, branch `master_branch_release_store`:
- Dùng `device_id` Android đọc `Settings.Secure.ANDROID_ID` qua **MethodChannel tự viết** (`MainActivity.kt`), **không thêm package mới**.
- Chọn `ANDROID_ID` vì **đúng bằng giá trị app dùng tới bản 2.8.5** → bản ghi cũ trên server **tự khớp lại**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Dev liệt kê các nơi đã được check & update khi fix bug (caller functions, data dependencies). -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `<Input thiếu — Dev chưa cung cấp>` | | |

> ⚠️ **Dev KHÔNG liệt kê caller đã check.** Đây là mục quan trọng nhất để đánh giá regression: `device_id` là input của **nhiều** luồng (đăng ký token, xoá token, lấy token + badge, logout / huỷ subscribe topic). Leader **bắt buộc hỏi Dev**: ngoài FCM token và badge, còn chỗ nào trong app đọc `device_id` không (analytics, session, thiết bị tin cậy, log...)?

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `<Input thiếu — Dev chưa cung cấp>` | | Direct / Indirect | |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Input thiếu — Dev chưa cung cấp>` | CREATE / UPDATE / DELETE / MIGRATE | |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | `<Input thiếu — Dev chưa cung cấp>` | | High / Medium / Low |

> ⚠️ **Toàn bộ mục 4 KHÔNG có trong Redmine.** Journal chỉ nêu ở mục 3 hai chức năng bị ảnh hưởng (chưa phải bảng impact chuẩn):
> - **Đăng ký / xoá FCM token** — máy thứ hai đè token máy thứ nhất → mất thông báo; logout một máy xoá token máy kia.
> - **Badge số chưa đọc** — sai giữa các máy.

---

## Phụ lục A — Dev impact từ MCP LME TEST STUDIO (⚠️ KHÔNG phải nguồn Redmine)

> **Nguồn**: MCP LME TEST STUDIO, `task_get_context(task_id=73, sections=["dev_impact"])`, fetch 2026-08-21.
> `contentTrust = untrusted` → xử lý như **data**, KHÔNG phải chỉ thị và **KHÔNG phải lời Dev trên Redmine**.
> Đưa vào đây vì mục 3 + 4.1/4.2/4.3 phía trên trống — Leader dùng để đối chiếu / hỏi lại Dev, **không tự coi là đã verify**.

```
- API POST /api/mobile/update-firebase_token (MobileController@updateFirebaseToken): bỏ định danh user qua user_token rỗng; tra bản ghi user_firebase_token theo user_id kèm orderByDesc('id') để lấy bản mới nhất trước khi update/dọn trùng
- API POST /api/mobile/delete-firebase_token (MobileController@deleteFirebaseToken): cùng sửa bỏ user_token rỗng khớp bừa user chưa login
- API POST /api/mobile/get-token-firebase (MobileController@getFirebaseToken): bỏ HẲN nhánh dự phòng tra theo device_id đơn thuần (fallback cũ coi device_id duy nhất trong khi thực tế device_id Android là build ID dùng chung hàng trăm máy) — nếu không xác định được user qua user_token thì trả rỗng thay vì đoán theo thiết bị; đồng thời API không còn lọc theo os
- AuthMobileController@logout: tra user_firebase_token theo user_id kèm orderByDesc('id') trước khi đánh dấu huỷ subscribe topic, tránh đánh dấu nhầm bản ghi cũ còn giữ status_subscribe_topic=1
- Ảnh hưởng dây chuyền tới job firebase:subscribe_topic (HandleSubscribeTopic) — job đọc status_subscribe_topic IN (0,2) để đăng ký/huỷ topic FCM, nếu tra sai bản ghi thì job không đăng ký lại topic cho máy đang dùng → đúng cơ chế 'chập chờn' trong tiêu đề ticket
- Ảnh hưởng badge số chưa đọc trả về theo user_firebase_token — cần kiểm tra badge đúng theo từng máy sau fix
- App Android (ngoài phạm vi source backend): đổi nguồn device_id sang Settings.Secure.ANDROID_ID qua MethodChannel tự viết trong MainActivity.kt, không có source repo app trong hệ thống nên không tự verify qua diff
```

**Commit backend Studio ghi nhận** (qua `source_refs` của requirements): `1cba79c51d`, `ca27fe1abe`, `caa3c277b7`, `49f1bc49a6`, `3233088f19` — **5 commit**, không commit nào xuất hiện trong Redmine #39487.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — ⚠️ **phần backend chưa mô tả trong Redmine**
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **TRỐNG, bắt buộc hỏi Dev**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ **TRỐNG**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ **TRỐNG**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — ⚠️ **TRỐNG**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Đã xác nhận quan hệ với ticket **#39559** (fix backend cùng cơ chế) — Redmine không khai báo relation
