# 03 — Đánh giá ảnh hưởng từ Dev

> Nguồn: Redmine #34227, journal `132716` do **AI LME Fix bug** đăng lúc `2026-08-25T02:42:09Z` (report tự động "★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST").

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine hiện tại: `Đoàn Thị Bích Hảo` |
| Commit / Pull Request | repo `sns-line`, commit `d226859eed` (1 file) — không có link PR Github/Gitlab. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=34227 |
| Branch | `ai_fixbug_34227` (nhánh gốc `release_step_20260805`) — đã push |
| Ngày submit đánh giá | `2026-08-25` |
| Auto-filled | `2026-09-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" của report. -->

Thứ tự kéo-thả các lựa chọn (label) của câu hỏi radio KHÔNG được ghi vào dữ liệu ngay lúc thả chuột, mà chỉ lưu tạm một danh sách mã tạm dùng chung cho cả màn rồi mới áp lúc bấm Lưu. Trong khoảng treo đó, mã tạm của từng lựa chọn bị đánh số lại và danh sách lựa chọn có thể bị thay mới bởi các thao tác khác (chọn lại câu hỏi, đổi liên kết tag/thông tin bạn bè, thêm-xoá lựa chọn), nên thứ tự cũ bị áp lên bộ mã mới và các label nhảy lung tung khi lưu.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" của report. -->

Áp thứ tự kéo-thả vào danh sách lựa chọn NGAY trong sự kiện thả chuột (5 chỗ khởi tạo kéo-thả lựa chọn: chọn lại câu hỏi, liên kết thông tin bạn bè, không liên kết, đổi chế độ tag của lựa chọn đơn và của lựa chọn nhiều) thay vì để treo tới lúc bấm Lưu — theo đúng mẫu đã duyệt ở màn quản lý tag. Thêm kiểm tra tồn tại câu hỏi trước khi sắp xếp để không lỗi khi chưa chọn câu hỏi nào. CHỈ sửa 1 file JS, KHÔNG bump số phiên bản tài nguyên tĩnh (theo rule của đội: cache-bust là việc của đội release). Quét ngang: không màn nào khác dùng cơ chế treo thứ tự này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Danh sách nguyên văn ở mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN". Cột "Thay đổi" / "Lý do" chỉ điền khi report có nêu; còn lại ghi rõ Dev không ghi. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `sortOptionItemForm` — `public/js/form_answer/v3/setting_form_items.js` | Thêm kiểm tra tồn tại câu hỏi (null-guard) trước khi sắp xếp | Không lỗi khi chưa chọn câu hỏi nào (mục 2) |
| 2 | `showItemComponent` — `public/js/form_answer/v3/setting_form_items.js` | Áp thứ tự ngay trong sự kiện thả chuột (chế độ chọn lại câu hỏi) | 1 trong 5 chỗ khởi tạo kéo-thả (mục 2) |
| 3 | `initSortNotLink` — `public/js/form_answer/v3/setting_form_items.js` | Áp thứ tự ngay trong sự kiện thả chuột (chế độ không liên kết) | 1 trong 5 chỗ khởi tạo kéo-thả (mục 2) |
| 4 | `initSortFriendInfo` — `public/js/form_answer/v3/setting_form_items.js` | Áp thứ tự ngay trong sự kiện thả chuột (liên kết thông tin bạn bè) | 1 trong 5 chỗ khởi tạo kéo-thả (mục 2) |
| 5 | `changeTagAndFriend` — `public/js/form_answer/v3/setting_form_items.js` | Áp thứ tự ngay trong sự kiện thả chuột (đổi chế độ tag của lựa chọn đơn) | 1 trong 5 chỗ khởi tạo kéo-thả (mục 2) |
| 6 | `changeTagCheckbox` — `public/js/form_answer/v3/setting_form_items.js` | Áp thứ tự ngay trong sự kiện thả chuột (đổi chế độ tag của lựa chọn nhiều) | 1 trong 5 chỗ khởi tạo kéo-thả (mục 2) |
| 7 | `saveFormAnswer` — `public/js/form_answer/v3/setting_form_items.js` | Giữ nguyên lời gọi cũ — sau fix chỉ còn là bước dự phòng | Nêu ở mục TỰ REVIEW của report |
| 8 | `changePage` — `public/js/form_answer/v3/setting_form_items.js` | Dev không ghi | Đã check (mục 3) |
| 9 | `appendSelect` / `changeAutoAddOther` / `deleteItemForm` — `public/js/form_answer/v3/setting_form_items.js` | Dev không ghi | Đã check (mục 3) |
| 10 | `radio.blade.php` khối kéo-thả 3 chế độ — `resources/views/basic/form_answer/components/v3/radio.blade.php` | Dev không ghi | Đã check (mục 3) |
| 11 | `FormAnswerController::saveV3` — `app/Http/Controllers/Basic/FormAnswerController.php` | Không sửa | Xác nhận server lưu nguyên thứ tự client gửi (json_encode selectable, dòng 1532) |
| 12 | `FormAnswerController::makeDataEditV3` — `app/Http/Controllers/Basic/FormAnswerController.php` | Không sửa | Xác nhận màn sửa đọc lại nguyên thứ tự (json_decode settings, dòng 4893) |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ Mục "4.1" của report gốc **chỉ ghi File thay đổi**, KHÔNG liệt kê function. Bảng F1–F8 dưới đây trích từ **mục 2 + mục 3** của report; cột `Mức độ ảnh hưởng` do `/new-task` suy ra từ nội dung report — **tester verify lại với Dev trước khi dùng làm base coverage**.

**Nguyên văn 4.1:**

```
 • 4.1 File thay đổi:
   - public/js/form_answer/v3/setting_form_items.js
```

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `sortOptionItemForm` (thêm null-guard) | `public/js/form_answer/v3/setting_form_items.js` | Direct | Hàm sắp xếp dùng chung, tái dùng nguyên logic cũ |
| F2 | `showItemComponent` — sự kiện thả chuột (chọn lại câu hỏi) | `public/js/form_answer/v3/setting_form_items.js` | Direct | 1/5 chỗ khởi tạo kéo-thả được sửa |
| F3 | `initSortNotLink` — sự kiện thả chuột (không liên kết) | `public/js/form_answer/v3/setting_form_items.js` | Direct | 2/5 |
| F4 | `initSortFriendInfo` — sự kiện thả chuột (liên kết thông tin bạn bè) | `public/js/form_answer/v3/setting_form_items.js` | Direct | 3/5 |
| F5 | `changeTagAndFriend` — sự kiện thả chuột (tag lựa chọn đơn) | `public/js/form_answer/v3/setting_form_items.js` | Direct | 4/5 |
| F6 | `changeTagCheckbox` — sự kiện thả chuột (tag lựa chọn nhiều) | `public/js/form_answer/v3/setting_form_items.js` | Direct | 5/5 |
| F7 | `saveFormAnswer` | `public/js/form_answer/v3/setting_form_items.js` | Indirect | Lời gọi sắp xếp lúc bấm Lưu giữ nguyên → thành bước dự phòng |
| F8 | `FormAnswerController::saveV3` / `makeDataEditV3` | `app/Http/Controllers/Basic/FormAnswerController.php` | Indirect | Dev **xác nhận không sửa** — server giữ nguyên thứ tự client gửi |

### 4.2. List data bị update khi fix bug

**Nguyên văn 4.2:**

```
 • 4.2 Data ảnh hưởng:
   - Không có — chỉ sửa phía giao diện, không đổi cấu trúc bảng. Dữ liệu form đã lưu sai thứ tự trước đây không tự sửa, khách cần kéo-thả lại và lưu.
```

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Không có — Dev khẳng định không đổi cấu trúc bảng | — | Fix thuần phía giao diện (1 file JS) |
| D2 | Dữ liệu form đã lưu **sai thứ tự trước fix** | **KHÔNG migrate** | Khách phải kéo-thả lại + lưu thủ công thì thứ tự mới đúng |

> Mục "■ 5. RECOVER DATA" của report: **Không cần recover data**.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

**Nguyên văn 4.3:**

```
 • 4.3 Tính năng liên quan:
   - Form Builder (FA-011) — sắp xếp lựa chọn của câu hỏi lựa chọn đơn/nhiều, ở cả 3 chế độ: không liên kết, liên kết tag, liên kết thông tin bạn bè
   - Form Builder (FA-011) — câu hỏi giới tính, chẩn đoán, nhắc lịch dùng chung cơ chế kéo-thả lựa chọn nên cũng được sửa theo
```

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form Builder (FA-011) — sắp xếp lựa chọn của câu hỏi lựa chọn đơn/nhiều, ở cả 3 chế độ: không liên kết, liên kết tag, liên kết thông tin bạn bè | F1–F6 | Dev không ghi mức |
| T2 | Form Builder (FA-011) — câu hỏi giới tính, chẩn đoán, nhắc lịch (dùng chung cơ chế kéo-thả lựa chọn nên cũng được sửa theo) | F1–F6 | Dev không ghi mức |

---

## Phụ lục — mục 5 / 6 / tự review (nguyên văn từ Redmine, ngoài phạm vi template)

### ■ 5. RECOVER DATA

```
   ✔ Không cần recover data
```

### ■ 6. VERIFY

```
   Mức: lint
   Lệnh: node --check public/js/form_answer/v3/setting_form_items.js: OK; git diff --stat release_step_20260805...ai_fixbug_34227: chỉ 1 file JS (+12 −1)
   Bằng chứng: Mẫu fix đã duyệt cho cùng lớp lỗi (kéo-thả jQuery UI không đồng bộ mảng Vue): public/js/tag/index_v2.js dòng 131-142 và 181-192 — đều resync mảng ngay trong callback update; Server giữ nguyên thứ tự client gửi: FormAnswerController::saveV3 lưu json_encode($item['selectable']) (dòng 1532), makeDataEditV3 đọc lại json_decode($item->settings) (dòng 4893) — nên lỗi hoàn toàn ở phía giao diện; Không kiểm chứng được trên dev DB: MySQL host.docker.internal:3306 báo Connection refused (stack dev không chạy)
```

### ■ TỰ REVIEW (AI)

```
Fix tối giản, tự-chứa: chỉ thêm 1 lời gọi sắp xếp ngay trong 5 callback thả chuột + 1 kiểm tra tồn tại, tái dùng nguyên hàm sắp xếp cũ nên giữ đúng các quy tắc sẵn có (lựa chọn 'Khác' luôn ở cuối, lựa chọn mới thêm sau khi kéo vẫn giữ đúng vị trí). Lời gọi cũ lúc bấm Lưu được giữ nguyên, sau fix chỉ còn là bước dự phòng không tác dụng phụ. Không đụng file config nào.
 • Rủi ro / lưu ý khi test:
   - Không kiểm chứng được bằng trình duyệt trong container (không có stack dev đang chạy) — cần tester xác nhận lại thao tác kéo-thả trên cả 3 chế độ liên kết
   - KHÔNG bump config('sns-line.version') theo rule của đội, nên trình duyệt đã cache bản JS cũ có thể cần tải lại cứng (Ctrl+F5) khi test trước lúc đội release bump version
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — **lưu ý: 4.1 gốc chỉ ghi file, bảng F1–F8 là suy ra, chưa được Dev xác nhận**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
