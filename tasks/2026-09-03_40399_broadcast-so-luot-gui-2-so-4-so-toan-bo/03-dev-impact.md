# 03 — Đánh giá ảnh hưởng từ Dev

> **Nguồn**: Redmine #40399 — journal `133876` (2026-09-03T06:52:33Z, user `AI LME Fix bug`), báo cáo **AI AUTO-FIXBUG**.
> Nội dung 4 mục bên dưới **paste nguyên văn** từ Redmine; bảng phía sau mỗi mục là phần Claude parse lại theo template (đánh tag F/D/T) để map coverage.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI Auto-fixbug LME` (báo cáo tự động, không có dev người). Redmine assigned_to = `Ngô Thúy Ngần` (QA nhận test) |
| Commit / Pull Request | Repo `sns-line`, commit `1348f867e2` — **không có link PR** trong Redmine |
| Branch | `ai_fixbug_40399` (nhánh gốc `release_step_20260827`, 2 file, đã push origin) |
| Ngày submit đánh giá | `2026-09-03` |
| Auto-filled | `2026-09-03 by /new-task` |

**Link phiên xử lý AI** (Dev cung cấp): https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=21f63d79-423a-4ddf-8ee3-ad9506ac8d53 · Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=40399

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục "■ 1. NGUYÊN NHÂN" từ Redmine journal 133876. -->

Ở danh sách broadcast (tab bản nháp / chờ gửi), cột số người dự kiến lấy từ giá trị đã lưu trong bảng broadcast — là ảnh chụp tại thời điểm lưu chứ không phải số hiện tại. Với broadcast gửi toàn bộ (không đặt điều kiện lọc), con số này bị đóng băng từ lần lưu đầu tiên và khách không có cách nào làm mới nó ở màn sửa, vì nút Tính lại bị khoá khi chọn gửi toàn bộ. Tài khoản có bạn bè tăng dần theo thời gian nên thấy số cũ rất nhỏ (2 chữ số) ở danh sách, trong khi màn tạo/sửa nháp tính tươi nên ra số thật (4 chữ số); lưu lại bản nháp cũng làm số được ghi đè lại cho đúng — khớp đúng mô tả của khách. Riêng cảnh báo sắp chạm giới hạn gửi KHÔNG phải lỗi: hệ thống chủ động cảnh báo ngay khi đạt 50% hạn mức, nên 15.000 trên 30.000 là vừa chạm ngưỡng cảnh báo.

## 2. Cách fix

<!-- Nguyên văn mục "■ 2. CÁCH FIX" từ Redmine journal 133876. -->

Sửa 2 điểm cùng một gốc — số người dự kiến của broadcast gửi toàn bộ bị lấy từ ảnh chụp cũ. (1) Danh sách broadcast (BroadcastController::ajaxGetListBroadcastVer2): với broadcast không có điều kiện lọc và chưa gửi, trả về số bạn bè hiện tại thay cho giá trị ảnh chụp đang lưu, kèm mốc thời gian là hiện tại; không ghi DB, không đụng broadcast có lọc và broadcast đã gửi. (2) Luồng COPY (BroadcastV2Controller::saveCopyBroadCastV2New): hàm này dựng bản sao bằng replicate() nên bê nguyên cả số dự kiến lẫn mốc thời gian của bản gốc, và khác luồng lưu thường là nó bỏ qua hoàn toàn count_filter do màn hình gửi lên — nên bản sao của một broadcast gửi toàn bộ vừa tạo đã mang sẵn con số cũ nhỏ, tức là copy chính là đường lan con số sai sang các bản nháp mới. Nay khi bản gốc không có điều kiện lọc thì chốt lại số bạn bè hiện tại (đếm ở server, không tin số client gửi) cho cả bản sao cha lẫn các lần gửi con; bản sao CÓ điều kiện lọc vẫn giữ nguyên ảnh chụp + mốc thời gian gốc để chú thích thời điểm không nói sai. Quét ngang thấy 3 chỗ khác dùng chung giá trị ảnh chụp này nhưng thuộc màn/tính năng khác nên chỉ ghi nhận, không sửa.

**⚠️ Điểm cần hỏi lại Dev**: "3 chỗ khác dùng chung giá trị ảnh chụp này" — Dev **không liệt kê tên** 3 chỗ đó. Leader cần yêu cầu Dev nêu rõ trước khi chốt phạm vi regression (xem mục 4.1 — `BUG-GAP-01`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" — Dev list dạng plain, Claude convert sang bảng template. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BroadcastController::ajaxGetListBroadcastVer2` — `app/Http/Controllers/Basic/BroadcastController.php` | **CÓ sửa** | Trả số bạn bè hiện tại thay ảnh chụp, cho broadcast không lọc + chưa gửi |
| 2 | `BroadcastV2Controller::saveCopyBroadCastV2New` — `app/Http/Controllers/Basic/BroadcastV2Controller.php` | **CÓ sửa** | `replicate()` bê nguyên `filter_number`/`filter_date` của bản gốc → chốt lại số hiện tại khi bản gốc không lọc |
| 3 | `BroadcastController::getFilterNumber` — `BroadcastController.php` | Không sửa (đã check) | Nguồn công thức đếm bạn bè |
| 4 | `BroadcastV2Controller::addBroadcastV2` — `BroadcastV2Controller.php` | Không sửa (đã check) | Luồng tạo mới |
| 5 | `BroadcastV2Controller::saveBroadcastV2` — `BroadcastV2Controller.php` | Không sửa (đã check) | Luồng lưu thường (dùng `count_filter` từ client); nhánh `type=copy` gọi sang `saveCopyBroadCastV2New` |
| 6 | `BroadcastV2Controller::getDetailBroadcastV2` — `BroadcastV2Controller.php` | Không sửa (đã check) | Màn sửa broadcast |
| 7 | `FilterController::saveFilterV2` — `app/Http/Controllers/Basic/FilterController.php` | Không sửa (đã check) | Lưu điều kiện lọc |
| 8 | `TemplateV2Controller::getBroadcastLimitAlert` — `app/Http/Controllers/Basic/TemplateV2Controller.php` | Không sửa (đã check) | Cảnh báo chạm hạn mức (ngưỡng 50%) — kết luận **đúng thiết kế, không sửa** |
| 9 | `Conversation::advanceFilterPost` — `app/Conversation.php` | Không sửa (đã check) | Lọc bạn bè nâng cao |
| 10 | `initDeliveryModalState` — `public/js/layout_v2_header.js` | Không sửa (đã check) | State modal gửi |
| 11 | `saveBroadcast` / `getNumberFilter` — `public/js/broadcast/add-broadcast.js` | Không sửa (đã check) | JS màn tạo/sửa broadcast |
| 12 | `getNumberFilter` — `public/js/broadcast/index.js` | Không sửa (đã check) | JS màn danh sách |
| 13 | `draff.blade.php` / `wait-to-send.blade.php` / `edit-broadcast.blade.php` — `resources/views/basic/broadcast` | Không sửa (đã check) | View 3 tab danh sách + màn sửa |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn mục "■ 4.1 File thay đổi":
     - app/Http/Controllers/Basic/BroadcastController.php
     - app/Http/Controllers/Basic/BroadcastV2Controller.php
     ⚠️ Dev chỉ liệt kê FILE, không liệt kê function ở 4.1. Bảng dưới do Claude suy từ mục 2 + mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BroadcastController::ajaxGetListBroadcastVer2` (API load danh sách broadcast tab bản nháp / chờ gửi) | `app/Http/Controllers/Basic/BroadcastController.php` | **Direct** | Với broadcast **không lọc + chưa gửi**: trả số bạn bè **hiện tại** + mốc thời gian **hiện tại** thay cho giá trị lưu trong DB. **Không ghi DB.** |
| F2 | `BroadcastV2Controller::saveCopyBroadCastV2New` (luồng COPY broadcast) | `app/Http/Controllers/Basic/BroadcastV2Controller.php` | **Direct** | Bản gốc **không lọc** → chốt số bạn bè hiện tại (đếm **ở server**, không tin `count_filter` từ client) cho cả bản sao cha lẫn các lần gửi con. Bản gốc **có lọc** → giữ nguyên ảnh chụp + mốc thời gian gốc. |
| F3 | `BroadcastController::getFilterNumber` | `BroadcastController.php` | Indirect | Công thức đếm dùng chung với màn sửa; nay bị gọi thêm 1 lần/request ở danh sách và 1 lần mỗi lần bấm sao chép → **rủi ro performance** |
| F4 | `TemplateV2Controller::getBroadcastLimitAlert` | `TemplateV2Controller.php` | Indirect (không sửa) | Cảnh báo 50% hạn mức — Dev kết luận đúng thiết kế. Cần regression: fix không làm lệch ngưỡng cảnh báo |
| **BUG-GAP-01** | **3 chỗ khác dùng chung giá trị ảnh chụp `filter_number`/`filter_date`** | **Dev KHÔNG nêu tên** | **Chưa xác định** | Dev ghi "chỉ ghi nhận, không sửa" nhưng không liệt kê → **không chốt được phạm vi regression**. Leader phải hỏi Dev. |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn mục "■ 4.2 Data ảnh hưởng":
Không có dữ liệu cũ bị sửa. Từ nay bản sao MỚI tạo của broadcast gửi toàn bộ sẽ lưu số dự kiến đúng vào broadcast.filter_number + filter_date; các bản ghi cũ giữ nguyên và được màn danh sách hiển thị đè bằng số hiện tại. -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `broadcast.filter_number` | **CREATE** (chỉ bản ghi mới sinh từ luồng COPY) | Bản sao của broadcast **không lọc** → ghi số bạn bè hiện tại. Bản sao **có lọc** → vẫn copy y nguyên giá trị gốc. |
| D2 | `broadcast.filter_date` | **CREATE** (chỉ bản ghi mới sinh từ luồng COPY) | Đi kèm D1. Bản sao có lọc giữ mốc thời gian gốc (**có thể rất cũ** — cố ý). |
| D3 | Bản ghi `broadcast` **cũ** đã tồn tại | **KHÔNG thay đổi** | Không migrate, không backfill. Giá trị cũ vẫn nằm trong DB, chỉ bị **màn danh sách hiển thị đè** bằng số hiện tại (F1) → **DB và UI cố ý lệch nhau** với broadcast không lọc chưa gửi. |

**⚠️ Lưu ý cho RULE-07 (khớp DB + màn hình + output)**: fix này **cố ý tạo lệch** giữa `broadcast.filter_number` trong DB và số hiển thị ở danh sách. TC không được kết luận "sai" khi thấy DB ≠ UI ở đúng nhóm broadcast không lọc + chưa gửi.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục "■ 4.3 Tính năng liên quan":
- Broadcast (FA-008) — số người dự kiến của broadcast gửi toàn bộ: đúng ở danh sách bản nháp/chờ gửi và được chốt đúng khi sao chép
- Friend Filter / Segment (SC-003) — không đổi: broadcast có đặt điều kiện lọc vẫn dùng ảnh chụp + nút Tính lại như cũ, kể cả khi sao chép -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Broadcast (FA-008)** — danh sách tab **bản nháp** / **chờ gửi**: số người dự kiến của broadcast gửi toàn bộ | F1, D3 | **High** |
| T2 | **Broadcast (FA-008)** — luồng **sao chép** broadcast (`showCopyV2` → `saveBroadcastV2 type=copy` → `saveCopyBroadCastV2New`) | F2, D1, D2 | **High** |
| T3 | **Friend Filter / Segment (SC-003)** — broadcast **có** điều kiện lọc: vẫn dùng ảnh chụp + nút 再計算 (Tính lại) như cũ, kể cả khi sao chép | F1, F2 | **Medium** (Dev khẳng định "không đổi" → cần regression chứng minh) |
| T4 | Broadcast tab **đã gửi** (delivered) — không được đụng tới | F1 | **Medium** (regression: số của broadcast đã gửi phải **đứng yên**, không bị tính lại) |
| T5 | Cảnh báo chạm hạn mức gửi 「配信数上限が近づいています」 (ngưỡng 50%) | F4 | **Low** (không sửa code, nhưng là nội dung khách hỏi → cần TC xác nhận đúng thiết kế) |

---

## 5. Recover data

<!-- Nguyên văn mục "■ 5. RECOVER DATA" -->

✔ Không cần recover data

## 6. Verify của Dev

<!-- Nguyên văn mục "■ 6. VERIFY" -->

**Mức: lint** (⚠️ **không có test runtime**)

- `php -l app/Http/Controllers/Basic/BroadcastController.php`: No syntax errors detected
- `php -l app/Http/Controllers/Basic/BroadcastV2Controller.php`: No syntax errors detected
- `git diff --stat origin/release_step_20260827...ai_fixbug_40399`: 2 files changed, 47 insertions(+), 1 deletion(-)
- Xác nhận luồng copy đang chạy là `showCopyV2` → `saveBroadcastV2 (type=copy)` → `saveCopyBroadCastV2New`; hàm `copyBroadcastV2` phía server đã bị comment ở cả 3 tab nên không còn được gọi

**Bằng chứng Dev đưa ra**:
- `draff.blade.php:121`, `wait-to-send.blade.php:137`, `delivered.blade.php:121` — nút sao chép gọi `showCopyV2`, dòng gọi `copyBroadcastV2` bị comment ⇒ `copyBroadcastV2` là code chết
- `index.js:232` `showCopyV2` chuyển hướng sang `/basic/add-broadcast-v2?broadcast_id=<id gốc>&type=copy`
- `edit-broadcast.blade.php:1742` đọc `type` từ URL
- `BroadcastV2Controller::saveBroadcastV2:163` nhánh `type=copy` gọi `saveCopyBroadCastV2New` ⇒ **bản gốc KHÔNG bị ghi đè** (đã kiểm vì đây là rủi ro rõ nhất của việc gửi kèm id bản gốc)
- `saveCopyBroadCastV2New:808` `replicate()` copy cả `filter_number`/`filter_date` và không dùng `$request->count_filter` — khác nhánh lưu thường ở `saveBroadcastV2:217`
- `edit-broadcast.blade.php:771` nút 再計算 bị khoá khi `type==copy` nên trong lúc copy khách không thể tự tính lại
- ⚠️ **DB dev `host.docker.internal:3306` Connection refused nên không kiểm chứng được bằng dữ liệu runtime**

## 7. Tự review của AI + rủi ro khi test

<!-- Nguyên văn mục "■ TỰ REVIEW (AI)" -->

Fix đúng root cause ở 2 điểm cùng một gốc: màn danh sách hiển thị ảnh chụp cho loại broadcast mà khách không thể làm mới, và luồng sao chép nhân bản luôn ảnh chụp đó sang bản nháp mới. Đã xác nhận luồng copy đang chạy là `saveCopyBroadCastV2New` (hàm `copyBroadcastV2` là code chết) và bản gốc KHÔNG bị ghi đè khi bấm sao chép. Giữ nguyên hành vi cho broadcast có điều kiện lọc và broadcast đã gửi. Phần khách hỏi về cảnh báo chạm hạn mức đã đối chiếu code và xác định đúng thiết kế (ngưỡng 50%), không sửa.

**Rủi ro / lưu ý khi test (Dev nêu)**:
1. Thêm **1 truy vấn đếm bạn bè mỗi lần tải danh sách** (chỉ khi trang có broadcast gửi toàn bộ chưa gửi, đã cache 1 lần/request) và **1 truy vấn đếm mỗi lần bấm sao chép**. Cùng công thức màn sửa vẫn đang chạy nên chi phí tương đương. → **cần TC performance với account nhiều bạn bè**.
2. Số ở danh sách nay **đổi theo thời gian thực** với broadcast gửi toàn bộ, khác trước là đứng yên — là ý đồ của fix, khớp màn sửa, nhưng là **thay đổi hiển thị nên cần PM/BA xác nhận**.
3. Bản sao của broadcast **CÓ điều kiện lọc** vẫn mang số + mốc thời gian của bản gốc (**có thể rất cũ**). Cố ý giữ để chú thích thời điểm không nói sai; khách bấm Tính lại sau khi lưu. Nếu nghiệp vụ muốn bản sao luôn tính mới thì phải mở khoá nút Tính lại trong lúc copy — **nằm ngoài phạm vi ticket**.
4. **Chưa kiểm chứng được bằng dữ liệu runtime vì DB dev không kết nối được; kết luận dựa trên đối chiếu code.**

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### ⚠️ Điểm nghi vấn Claude phát hiện — Leader hỏi Dev trước khi giao TC

| # | Nội dung | Ảnh hưởng tới TC |
|---|---|---|
| Q1 | **`BUG-GAP-01`** — Dev nói "3 chỗ khác dùng chung giá trị ảnh chụp" nhưng **không nêu tên**. | Không chốt được phạm vi regression của 4.1 / 4.3 |
| Q2 | Mục 4.1 của Dev chỉ liệt kê **file**, không liệt kê **function** theo format template. | Bảng F1–F4 ở trên là Claude suy ra từ mục 2 + 3 — **cần Dev/Leader confirm** |
| Q3 | Verify **chỉ mức lint**, DB dev không kết nối được ⇒ **0 bằng chứng runtime**. | Toàn bộ hành vi phải verify tay bằng TC; không được tin kết luận code-review |
| Q4 | Thay đổi hiển thị (số động theo thời gian thực ở danh sách) **chưa có PM/BA xác nhận**. | TC `Trạng thái đánh giá spec` nên là `Spec không ghi` / `Đã hỏi leader`, không tự cho `Đạt` |
| Q5 | Không có **link PR**, chỉ có branch + commit hash. | QA phải checkout `ai_fixbug_40399` để test; không review được diff qua PR |
