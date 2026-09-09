# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn: journal AI Auto-fixbug** (Redmine #39735, journal #129281, 2026-08-19 04:17 UTC) — **KHÔNG phải Dev người viết**. Nội dung dưới đây paste nguyên văn từ báo cáo AI. Tester/Leader phải đối chiếu lại mục 3 (caller đã check) và mục 4.1 trước khi chốt coverage.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee Redmine hiện tại: `Ngọc Ánh` |
| Commit / Pull Request | `sns-line` commit `497e386f64` (2 file) — **đã push**. Không có link PR Github/Gitlab trong Redmine. Session AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=757652ac-2209-47aa-b974-d196d72d2684 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=39735 |
| Branch | `ai_fixbug_39735` (nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-19` |
| Auto-filled | `2026-08-25 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" của journal #129281 -->

Trong modal chọn hành động (dùng chung cho khoảng 30 màn, trong đó có chat 1:1), popup thêm tag mới không có chỗ nào hiển thị lỗi. Mã JS khi gọi API xong đã gán nội dung lỗi trả về vào biến `error_message`, nhưng giao diện của popup lại thiếu dòng hiển thị biến này, nên lỗi trùng tên tag bị nuốt mất và người dùng thấy như bấm lưu không có phản ứng gì.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" của journal #129281 -->

Sửa popup thêm tag mới trong modal chọn hành động: thay vì gán nội dung lỗi vào biến rồi không ai hiển thị, nay bật thẳng hộp thoại cảnh báo (`alert`) với đúng nội dung lỗi API trả về — trùng tên tag hiện `そのタグ名はすでに利用されています`, bỏ trống tên hiện `新しいタグ名を入力してください`. Chỉ sửa 2 dòng trong tệp JS, không đụng giao diện blade. Tăng số phiên bản tài nguyên tĩnh để trình duyệt nạp lại tệp JS mới. Cách này khớp với các chỗ báo lỗi khác trong cùng tệp (đều dùng `alert`).

**Bổ sung từ mục "■ 6. VERIFY" của báo cáo AI:**

- Mức verify: `lint` (chỉ lint, **không có unit test / integration test**).
- Lệnh: `node --check public/js/select_action.js` → OK; `php -l resources/views/layout/modal_setting/modal_select_action.blade.php` → OK (đã hoàn nguyên, không còn thay đổi); `git diff --stat release_step_20260805...ai_fixbug_39735` → 2 file, +3/-3.
- Bằng chứng AI đưa ra: `ActionController::saveAddTag` trả HTTP 200 kèm `status=false` + `msg そのタグ名はすでに利用されています` nên chạy nhánh `.done()`, nay `alert(b.msg)` hiện đúng câu lỗi ticket mong đợi; các chỗ báo lỗi khác trong cùng `public/js/select_action.js` (dòng 569, 931, 952, 971...) đều dùng `alert` nên cách này đồng nhất với tệp; `grep modalAddTagModalAction` toàn repo chỉ ra **1 popup duy nhất** → không sót chỗ nào.

**Mục "■ TỰ REVIEW (AI)" — rủi ro / lưu ý khi test (nguyên văn):**

- Tăng phiên bản tài nguyên khiến toàn bộ tệp js/css nạp lại 1 lần sau khi lên bản — bình thường theo quy ước dự án.
- Trường `objectTag.error_message` giờ không còn được dùng để hiện lỗi (chỉ còn dòng gán rỗng lúc lưu thành công, vốn có sẵn từ trước) — giữ nguyên, không dọn để tránh sửa ngoài phạm vi.

**Mục "■ 5. RECOVER DATA":** ✔ Không cần recover data.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" — AI list dạng plain, convert sang bảng. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `saveAddTag` — `public/js/select_action.js` | **CÓ SỬA** (2 dòng: 258, 273 — theo `spec_ids` của Studio) | Nơi gán `error_message` mà không ai hiển thị → đổi sang `alert(b.msg)` |
| 2 | `ActionController::saveAddTag` — `app/Http/Controllers/Basic/ActionController.php` | Không sửa | API trả HTTP 200 + `status=false` + `msg` — hợp đồng giữ nguyên |
| 3 | `modalAddTagModalAction` — popup thêm tag, `resources/views/layout/modal_setting/modal_select_action.blade.php` | Không sửa (**đã hoàn nguyên** về nguyên trạng) | Popup dùng chung; AI grep toàn repo chỉ ra 1 popup duy nhất |
| 4 | `Basic\ChatController::index` — `app/Http/Controllers/Basic/ChatController.php` | Không sửa | Màn chat 1:1 include modal — nơi phát hiện bug |

> ⚠️ **Điểm cần Leader hỏi lại**: mục 3 chỉ liệt kê **4 function/file**, trong khi mục 1 nói modal dùng chung cho **~30 màn** và requirement REQ-005 trên Studio ghi modal được include ở **55 file blade**. AI chỉ grep `modalAddTagModalAction` (tên popup) chứ **không liệt kê từng caller màn**. → caller list ở mức màn hình **chưa được liệt kê đầy đủ**.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- ⚠️ Báo cáo AI ghi mục 4.1 là "File thay đổi" (mức file), KHÔNG phải "function bị ảnh hưởng" (mức function). Giữ nguyên nội dung AI đưa, không suy diễn thêm. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveAddTag` (nhánh `.done()` xử lý response) | `public/js/select_action.js` | Direct | AI ghi ở mục 4.1 là "File thay đổi". Diff: +3/-3, dòng 258 & 273 |
| F2 | Cấu hình version tài nguyên tĩnh (asset version → `202608190316`) | `config/sns-line.php` | Direct | Dòng 62. Tăng version → **toàn bộ** file js/css nạp lại 1 lần sau khi lên bản |

> ⚠️ **Input thiếu**: báo cáo AI **không có** bảng function-level cho 4.1 (chỉ có file-level). Các function `ActionController::saveAddTag`, `modalAddTagModalAction`, `ChatController::index` nằm ở mục 3 với trạng thái *"đã check, không sửa"* — Leader cần confirm với Dev là chúng thật sự không bị ảnh hưởng gián tiếp.

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "■ 4.2 Data ảnh hưởng" -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(không có)* | — | Nguyên văn AI: "Không có - chỉ sửa hiển thị phía giao diện, không đụng dữ liệu" |

> Không cần recover data (mục 5 của báo cáo AI).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "■ 4.3 Tính năng liên quan". Cột "Nguy cơ regression" AI KHÔNG ghi → để trống, Leader tự đánh giá. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Action Settings (SC-004)** — popup cấu hình hành động dùng chung cho khoảng 30 màn, nay báo lỗi khi thêm tag mới | F1 | `<AI không ghi — Leader đánh giá>` |
| T2 | **Tag Management (FA-012)** — tạo tag mới ngay trong popup hành động, báo rõ khi tên tag bị trùng | F1 | `<AI không ghi — Leader đánh giá>` |
| T3 | **1-on-1 Chat (FA-001)** — màn phát hiện lỗi, popup nhiều hành động trong chat 1:1 | F1 | `<AI không ghi — Leader đánh giá>` |
| T4 | *(suy từ F2)* Mọi màn admin nạp js/css — asset version tăng → nạp lại 1 lần sau deploy | F2 | `<Leader đánh giá — AI xếp là "bình thường theo quy ước dự án">` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — ⚠️ **xem cảnh báo ở mục 3: modal dùng chung ~30 màn / 55 blade nhưng caller chỉ liệt kê 4 mục**
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ **4.1 chỉ ở mức file, không có function-level**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — lưu ý: fix có tăng **asset version** → ảnh hưởng cache trình duyệt/CDN, AI xếp là "không đụng dữ liệu"
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
