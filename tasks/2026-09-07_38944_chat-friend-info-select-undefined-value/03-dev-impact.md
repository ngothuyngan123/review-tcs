# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Nguồn**: Redmine #38944 **KHÔNG có section "Đánh giá ảnh hưởng" do Dev người viết**. Nội dung dưới đây parse từ **journal #133032 của hệ thống Auto-fixbug LME** (`AI LME Fix bug`, 2026-08-26) — báo cáo tự động, không phải đánh giá tay của Dev. Tester **bắt buộc đối chiếu lại với Dev/Leader** trước khi tick verify.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (hệ thống Auto-fixbug LME)` — assignee ticket hiện tại: `Ngô Thúy Ngần` |
| Commit / Pull Request | `sns-line commit 0aa5427f22` (1 file) — không có link Github/Gitlab trên ticket. Dashboard: https://dashboard.melonglobal.net/fixbug-lme/?id=38944 |
| Branch | `ai_fixbug_38944` (nhánh gốc `release_step_20260623`) — branch release ghi ở journal #133174: `release_step_20260827` |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-09-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #133032 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

> Nguyên văn mục 1 của journal #133032:

Khi lưu một mục thông tin bạn bè kiểu 'chọn' từ khung chat 1:1, dữ liệu gửi lên chỉ chứa danh sách lựa chọn mà không có trường giá trị đã chọn. Đoạn code lưu lại đọc thẳng thuộc tính 'giá trị' của dữ liệu này mà không kiểm tra tồn tại, nên khi thiếu trường đó PHP báo lỗi thuộc tính không xác định và toàn bộ thao tác lưu bị hỏng.

## 2. Cách fix

> Nguyên văn mục 2 của journal #133032:

Sửa `ChatController::saveSettingDisplayInfoItem` (dòng 4471, sns-line): bọc `isset()` khi đọc thuộc tính giá trị của dữ liệu gửi lên trước khi so sánh, thay vì đọc trực tiếp. Khi dữ liệu không kèm trường giá trị (mục kiểu 'chọn' bỏ trống) thì coi như rỗng và đi vào nhánh xóa giá trị, không còn báo lỗi thuộc tính không xác định. Cùng khuôn mẫu đã dùng ở nhánh `type==0` (dòng 4333) trong chính hàm này.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục 3 của journal #133032 — Dev chỉ liệt kê **đúng 1 function**, không có danh sách caller.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ChatController::saveSettingDisplayInfoItem` — `app/Http/Controllers/ChatController.php:4471` | Bọc `isset()` khi đọc thuộc tính `value` của payload trước khi so sánh | Chặn `ErrorException: Undefined property: stdClass::$value` khi payload thiếu khóa `value` |

⚠️ **Input thiếu**: Dev **KHÔNG liệt kê caller** của hàm này, cũng không nêu điểm dùng chung nào khác trong `ChatController` có cùng pattern đọc thẳng `->value`. Cần hỏi Dev trước khi chốt phạm vi regression.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Journal #133032 mục 4.1 chỉ ghi **file thay đổi**, không ghi function. Bảng dưới quy về format template, giữ nguyên nội dung Dev cung cấp.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `ChatController::saveSettingDisplayInfoItem` (dòng 4471) | `app/Http/Controllers/ChatController.php` | Direct | Điểm sửa duy nhất — thêm `isset()` guard |

⚠️ **Input thiếu**: mục 4.1 gốc chỉ ghi `app/Http/Controllers/ChatController.php` (tên file), không kê function nào bị ảnh hưởng gián tiếp.

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2: "Không có — chỉ thêm kiểm tra tồn tại thuộc tính, không đổi cấu trúc/dữ liệu bảng".

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `<Dev khai: không có>` | — | Dev khẳng định không đổi cấu trúc / dữ liệu bảng |

⚠️ **Lưu ý cho Leader**: Dev khai "không có data impact" ở mức **schema**, nhưng ở mức **hành vi runtime** bản vá làm đổi kết quả: request trước kia **crash và không ghi gì** thì sau vá **đi vào nhánh xóa giá trị** — tức có thể **DELETE bản ghi giá trị thông tin bạn bè** đang có. Đây là data impact thực tế, cần TC verify phạm vi xóa (`WHERE` scope theo cặp friend × mục thông tin — RULE-07).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục 4.3 của journal #133032.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Information (FA-015) — lưu giá trị mục thông tin bạn bè kiểu 'chọn' từ khung chat 1:1 an toàn khi payload thiếu trường giá trị | F1 | `<Dev không ghi mức risk>` |

⚠️ **Input thiếu**: Dev không ghi mức High/Medium/Low, và không kê các tính năng đi qua cùng luồng lưu (mục kiểu 記述 / 年月日 / ポイント, action gắn theo lựa chọn, lịch sử thay đổi thông tin bạn bè, số 「回答人数」).

---

## Bổ sung từ báo cáo Auto-fixbug (mục 5 / 6 / tự review — nguyên văn)

**■ 5. RECOVER DATA**

```
✔ Không cần recover data
```

**■ 6. VERIFY**

```
Mức: lint
Lệnh: php -l app/Http/Controllers/ChatController.php: No syntax errors detected
Bằng chứng: Log ticket cho thấy $infos chỉ có 'valueOption' (danh sách lựa chọn), không có trường 'value' top-level → $value->value undefined tại dòng 4471; dòng 4470 dùng !empty (null-safe) còn 4471 đọc trực tiếp
```

⚠️ Mức verify của Dev **chỉ là `lint`** (kiểm tra cú pháp PHP) — **không có unit test, không có test chạy thật**. Toàn bộ gánh nặng verify hành vi dồn sang QA.

**■ TỰ REVIEW (AI)**

```
Fix tối thiểu 1 dòng: thêm isset() guard đọc thuộc tính giá trị, theo đúng khuôn mẫu đã có sẵn ở dòng 4333 cùng hàm. Không đổi luồng lưu/xóa, chỉ chặn crash khi payload thiếu trường value. Rủi ro thấp.
 • Rủi ro / lưu ý khi test:
   - Không: khi thiếu value thì valueNew='' đi vào nhánh xóa giá trị — đúng hành vi 'bỏ chọn = xóa'; dòng calendar 4474 chỉ chạy khi valueNew truthy nên không bị ảnh hưởng
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (**hiện Dev chỉ kê 1 function, KHÔNG có danh sách caller — bắt buộc hỏi lại Dev**)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (**Dev khai "không có" nhưng hành vi xóa giá trị là data impact — cần chốt lại**)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Câu hỏi tồn đọng cần hỏi Dev / PO

1. **Business rule**: payload **thiếu hẳn khóa `value`** có được hiểu tương đương thao tác **bỏ chọn / xóa giá trị** không? Hiện hành vi sau vá là **xóa bản ghi**, nhưng chưa có nguồn nghiệp vụ phát biểu rõ.
2. Khi thiếu `value` / bỏ chọn thì **action gắn ở lựa chọn cũ** có được phép chạy không?
3. **Client nào** sinh ra payload thiếu `value` trong log production ngày 2026-07-21?
4. Các điểm dùng chung khác trong `ChatController` có cùng pattern đọc thẳng `->value` (ví dụ luồng lưu danh sách hiển thị của modal 「表示内容を変更」) **có được vá cùng không**?
5. Nhánh fix tách từ `release_step_20260623` nhưng branch release là `release_step_20260827` — **đã rebase chưa**? Bản đem test có mất tính năng nào của nền mới không?
