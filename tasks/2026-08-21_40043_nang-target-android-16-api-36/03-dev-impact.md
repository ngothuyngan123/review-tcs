# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Thinh Nguyen` (assigned_to hiện tại). **Người viết đánh giá = Đoàn Thị Bích Hảo** (journal #130654) |
| Commit / Pull Request | `<chưa có>` — Redmine không có link Github/Gitlab/Bitbucket. Custom field "Commit Date" để trống |
| Branch | `master_branch_release_store` (journal #130660, 2026-08-20 03:15) |
| Ngày submit đánh giá | `2026-08-20` (journal #130654, 03:03:51Z) |
| Auto-filled | `2026-08-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ℹ️ **Nguồn**: Redmine #40043 có `description` TRỐNG. Toàn bộ đánh giá 4 mục nằm ở **journal note #130654**. Nội dung dưới đây được **paste nguyên văn**, chỉ tách mục theo đúng đánh số Dev đã dùng.
>
> ⚠️ Dev đánh số mục 3 là **"Đã check function/data"** và mục 4 là **"Đánh giá ảnh hưởng"** với các nhóm `Files:` / `Behavior changes` / `Data:` / `Tính năng ảnh hưởng:` — **không** dùng cấu trúc 4.1/4.2/4.3 và **không** đánh tag F1/D1/T1. Phần raw giữ nguyên văn; bảng tag F/D/T bên dưới do `/new-task` map 1:1 từ raw để `/write-tc` và `/review-tc` trace được — **tester verify lại trước khi dùng**.

---

## 1. Nguyên nhân

Google Play yêu cầu tất cả app phải target Android 16 (API 36) trở lên. Từ 31/8/2026, nếu app không đạt cấp API mục tiêu trong vòng 1 năm kể từ ngày phát hành Android mới nhất, sẽ không thể cập nhật app trên Play
Console. App hiện đang target API 35 (Android 15) → không tuân thủ.

## 2. Cách fix

Build config:
- compileSdk / targetSdk: 35 → 36
- AGP: 8.1.0/8.6.0 (đang xung đột) → 8.9.1 (bản đầu tiên hỗ trợ API 36)
- Gradle wrapper: 8.7 → 8.11.1 (bắt buộc cho AGP 8.9)
- Kotlin: 1.9.10 → 2.1.0 (KGP 1.9 không chạy được với Gradle 8.11)
- google-services 4.3.8 → 4.4.2, crashlytics-gradle 2.8.0 → 3.0.2 (bản cũ không tương thích AGP 8.9)
- Bỏ package="..." khỏi 3 AndroidManifest (AGP 8.9 báo lỗi vì namespace đã khai trong build.gradle); lintOptions → lint;

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> **Nguyên văn mục 3 của Dev ("Đã check function/data")** — đây là **bằng chứng build/verify của Dev**, không phải bảng caller function. Giữ nguyên format gốc.

- Build: flutter build apk --flavor dev và flutter build appbundle --flavor prod đều pass, 0 error compile.
- Verify APK: aapt2 dump badging → targetSdkVersion:'36', compileSdkVersion='36'.
- Test trên máy thật Samsung SM-A556E chạy Android 16 (SDK 36):
- App khởi động OK
- Edge-to-edge render đúng (status bar icon tối trên nền sáng, không đè content)
- Back từ route đã push → pop đúng màn, app vẫn foreground
- Back ở route gốc → thoát sạch, không crash
- Logcat: không có error/exception/permission denied
- 16 KB page size (yêu cầu Play kèm theo): 3 file .so trong AAB đều align ≥16KB (libflutter.so, libapp.so = 64KB; libdatastore_shared_counter.so = 16KB).
- Merged manifest: property giữ portrait + targetSdk 36 đều được merge đúng.

**Bảng caller/thay đổi (map 1:1 từ mục "Files" của Dev — `/new-task` derive, tester verify):**

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `android/app/build.gradle` | compileSdk/targetSdk 36, versionCode 397, lint | Nâng target API 36 |
| 2 | `android/build.gradle` | gỡ AGP classpath xung đột, nâng Kotlin/google-services/crashlytics | Tương thích AGP 8.9 |
| 3 | `android/settings.gradle` | AGP 8.9.1, Kotlin 2.1.0 | Bản đầu tiên hỗ trợ API 36 |
| 4 | `android/gradle/wrapper/gradle-wrapper.properties` | Gradle 8.11.1 | Bắt buộc cho AGP 8.9 |
| 5 | `android/gradle.properties` | jvmargs 4096M | Build config |
| 6 | `AndroidManifest.xml` (main / debug / profile) | gỡ `package=`, thêm property portrait | AGP 8.9 báo lỗi vì namespace đã khai trong build.gradle |
| 7 | `lib/page/home/message/widgets/image_gallery.dart` | WillPopScope → PopScope | Predictive back bật mặc định ở target 36, `onBackPressed` không còn được gọi |
| 8 | `lib/page/home/lifecycle_event_handler.dart` | fix crash hidden state | Hành vi lifecycle mới |
| 9 | `ios/Runner.xcodeproj/project.pbxproj` | bump version 397 | Đồng bộ version |

---

## 4. Đánh giá ảnh hưởng

> **Nguyên văn mục 4 của Dev:**

**Files:**
- android/app/build.gradle — compileSdk/targetSdk 36, versionCode 397, lint
- android/build.gradle — gỡ AGP classpath xung đột, nâng Kotlin/google-services/crashlytics
- android/settings.gradle — AGP 8.9.1, Kotlin 2.1.0
- android/gradle/wrapper/gradle-wrapper.properties — Gradle 8.11.1
- android/gradle.properties — jvmargs 4096M
- android/app/src/main|debug|profile/AndroidManifest.xml — gỡ package=, thêm property portrait
- lib/page/home/message/widgets/image_gallery.dart — WillPopScope → PopScope
- lib/page/home/lifecycle_event_handler.dart — fix crash hidden state
- ios/Runner.xcodeproj/project.pbxproj — bump version 397

**Behavior changes của target 36:**
- Predictive back: bật mặc định, onBackPressed không còn được gọi. Sửa image_gallery.dart từ WillPopScope (deprecated, không tính vào setFrameworkHandlesBack) → PopScope.

**Data:**
- Không ảnh hưởng data. Toàn bộ thay đổi là build config + hành vi UI/OS, không đụng model, API, DB (sqflite), hay SharedPreferences. Không có migration, không đổi format request/response.

**Tính năng ảnh hưởng:**
- Trực tiếp (đã sửa, cần test kỹ): nút Back / vuốt back toàn app; xem ảnh trong chat (mở ảnh → back phải đóng ảnh, không thoát màn chat); khóa xoay màn hình trên tablet/máy gập.
- Gián tiếp (do đổi toàn bộ build engine — smoke test): media (chọn/chụp ảnh-video, tải ảnh, ghi âm/phát audio, phát video, xem PDF); realtime chat (Socket.IO); push notification (FCM) + điều hướng khi bấm noti;
booking salon/lesson/event; calendar (nhất là shift calendar ca qua đêm).
- Không ảnh hưởng logic nghiệp vụ — chỉ tương thích nền tảng. Cần regression thêm trên máy Android 13/14/15 để chắc không hồi quy.

---

### 4.4. Làm rõ từ Dev về phạm vi "nút Back" (2026-08-21)

> ⚠️ **Nguồn**: Leader chuyển lại làm rõ của Dev. **Redmine #40043 KHÔNG đổi text** — `updated_on` vẫn `2026-08-21T00:09:17Z`, mục 4 giữ nguyên nguyên văn ở trên. Đây là **làm rõ ngữ nghĩa**, không phải sửa đánh giá.

**Nguyên văn dòng gốc trong mục 4:**

```
- Trực tiếp (đã sửa, cần test kỹ): nút Back / vuốt back toàn app
```

**Làm rõ**: "nút Back" ở đây là **nút Back của hệ thống Android nằm trên navigation bar** — tức chế độ điều hướng **3 nút**. Không phải nút back trong giao diện app (mũi tên ← trên AppBar).

**Hệ quả bắt buộc với TC** — Android có 2 chế độ điều hướng loại trừ nhau:

| Chế độ điều hướng | Cách kích hoạt back | Chế độ còn lại có làm được không? |
|---|---|---|
| **3 nút** (navigation bar) | Bấm nút Back trên thanh điều hướng | ❌ Chế độ cử chỉ **không có nút Back để bấm** |
| **Cử chỉ** (gesture) | Vuốt từ cạnh màn hình (predictive back có preview) | ❌ Chế độ 3 nút **không có cử chỉ vuốt back** |

→ **`Chế độ điều hướng` là biến bắt buộc trong `Điều kiện tiền đề` của mọi TC chạm back.** Chạy 1 chế độ = bỏ trống nửa đường dẫn back. TC không ghi chế độ thì kết quả `Đạt` **không kết luận được** đã cover nhánh nào.

Chi tiết TC đã sửa/bổ sung theo làm rõ này: xem [05-review-report.md](05-review-report.md) §5.4.

---

### 4.1. List function bị ảnh hưởng

> Tag F1–F6 do `/new-task` derive 1:1 từ mục "Files" + "Behavior changes" ở trên. Dev **không** tự đánh tag.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Build config Android (compileSdk/targetSdk 35 → 36, versionCode 397) | `android/app/build.gradle` | Direct | Gốc của toàn bộ thay đổi hành vi OS |
| F2 | Toolchain build (AGP 8.1/8.6 → 8.9.1, Gradle 8.7 → 8.11.1, Kotlin 1.9.10 → 2.1.0, google-services 4.3.8 → 4.4.2, crashlytics 2.8.0 → 3.0.2) | `android/build.gradle`, `android/settings.gradle`, `gradle-wrapper.properties`, `android/gradle.properties` | Direct | Đổi **toàn bộ build engine** → mọi plugin/native lib đều được compile lại |
| F3 | Khai báo manifest (gỡ `package=`, thêm property giữ portrait) | `AndroidManifest.xml` (main / debug / profile) | Direct | Ảnh hưởng khóa xoay màn hình |
| F4 | Xử lý back khi xem ảnh trong chat (WillPopScope → PopScope) | `lib/page/home/message/widgets/image_gallery.dart` | Direct | Predictive back Android 16: `onBackPressed` không còn được gọi |
| F5 | Lifecycle handler (fix crash hidden state) | `lib/page/home/lifecycle_event_handler.dart` | Direct | Hành vi lifecycle mới của target 36 |
| F6 | Version iOS (bump 397) | `ios/Runner.xcodeproj/project.pbxproj` | Indirect | Chỉ bump version — Dev không nêu thay đổi hành vi iOS |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D0 | **(không có)** | — | Dev khẳng định nguyên văn: *"Không ảnh hưởng data. Toàn bộ thay đổi là build config + hành vi UI/OS, không đụng model, API, DB (sqflite), hay SharedPreferences. Không có migration, không đổi format request/response."* |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Tag T1–T10 do `/new-task` derive 1:1 từ mục "Tính năng ảnh hưởng" của Dev. Mức risk theo đúng phân loại **Trực tiếp / Gián tiếp** Dev đã ghi.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Nút Back / vuốt back **toàn app** (predictive back) — **nút Back = nút HỆ THỐNG ở navigation bar**, xem làm rõ bên dưới | F1, F4 | **High** — Dev xếp "Trực tiếp, cần test kỹ" |
| T2 | Xem ảnh trong chat (mở ảnh → back phải đóng ảnh, KHÔNG thoát màn chat) | F4 | **High** — Dev xếp "Trực tiếp, cần test kỹ" |
| T3 | Khóa xoay màn hình trên tablet / máy gập | F3 | **High** — Dev xếp "Trực tiếp, cần test kỹ" |
| T4 | Media: chọn/chụp ảnh-video, tải ảnh, ghi âm/phát audio, phát video, xem PDF | F2 | Medium — Dev xếp "Gián tiếp, smoke test" |
| T5 | Realtime chat (Socket.IO) | F2 | Medium — Dev xếp "Gián tiếp, smoke test" |
| T6 | Push notification (FCM) + điều hướng khi bấm noti | F2 | Medium — Dev xếp "Gián tiếp, smoke test" (google-services + crashlytics đều đổi version) |
| T7 | Booking salon / lesson / event | F2 | Medium — Dev xếp "Gián tiếp, smoke test" |
| T8 | Calendar — **nhất là shift calendar ca qua đêm** | F2 | Medium — Dev xếp "Gián tiếp, smoke test", tự nêu là điểm nhạy cảm |
| T9 | App lifecycle: khởi động, background/foreground, hidden state | F5 | Medium — Dev đã sửa crash hidden state nhưng không xếp vào nhóm Trực tiếp/Gián tiếp nào |
| T10 | Tương thích ngược **Android 13 / 14 / 15** | F1, F2 | **High** — Dev yêu cầu nguyên văn: *"Cần regression thêm trên máy Android 13/14/15 để chắc không hồi quy"* |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

## Điểm Leader cần hỏi lại Dev (`/new-task` flag — chưa có trong Redmine)

1. **Không có link commit/PR** → không trace được thay đổi thực tế so với mục "Files". Chỉ có `branch code: master_branch_release_store`.
2. **Mục 3 không phải bảng caller function** — là log build/verify của Dev. Chưa rõ Dev đã rà **toàn bộ** nơi còn dùng `WillPopScope` hay chỉ sửa mỗi `image_gallery.dart`. Đây là rủi ro lọt bug lớn nhất: predictive back ảnh hưởng **mọi** màn có chặn back (dialog, form đang nhập dở, video player, camera...), không riêng màn xem ảnh.
3. **`lifecycle_event_handler.dart` — "fix crash hidden state"** chưa được mô tả: crash xảy ra khi nào, đã reproduce chưa, fix thế nào.
4. **Ma trận thiết bị/OS bắt buộc** chưa có — Dev mới tự test 1 máy (Samsung SM-A556E / Android 16). Cần chốt danh sách máy Android 13/14/15 + tablet/máy gập (T3) trước khi giao TC.
5. **Phạm vi iOS**: chỉ bump version 397 hay có build/release kèm? Nếu có phát hành iOS thì cần smoke test iOS riêng.
6. **Build cho QA**: chưa có link APK/AAB hoặc bản phân phối nội bộ để QA cài test.
