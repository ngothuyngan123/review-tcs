# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39036 bởi `/new-task`. Nguồn: journal #131913 (2026-08-21) — báo cáo **AI AUTO-FIXBUG**.
> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assignee hiện tại trên Redmine: `Đoàn Thị Bích Hảo` |
| Commit / Pull Request | commit `73014385e8` (1 file) — *không có link Github/Gitlab trong ticket*. Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39036 |
| Branch | `ai_fixbug_39036` (repo `sns-line`, nhánh gốc `release_step_20260623`) — đã push lên origin |
| Ngày submit đánh giá | `2026-08-21` (journal #131913, 03:53Z) |
| Auto-filled | `2026-08-26 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

> ⚠️ **Lưu ý format**: báo cáo Auto-fixbug dùng khung 6 mục riêng (1 Nguyên nhân · 2 Cách fix · 3 Đã check function/data · 4 Đánh giá ảnh hưởng · 5 Recover data · 6 Verify), **không** khớp 1:1 với template 4 mục. Mục 4.1 của báo cáo là **"File thay đổi"** chứ không phải "function bị ảnh hưởng" → bảng 4.1 bên dưới được dựng lại từ mục 3 + 4.1 gốc để gắn tag `F`; **văn bản gốc giữ nguyên** trong các khối trích dẫn.

---

## 1. Nguyên nhân

> Nguyên văn từ Redmine:

Ảnh xem trước ở màn Popup CHỈ bị giới hạn bề RỘNG (200px, do reset.css toàn cục đã có `img{max-width:100%}`) mà KHÔNG có giới hạn chiều CAO. Ảnh dọc sau khi resize (2048x10000 → 419x2048) co còn 200px rộng nhưng cao tới ~980px, trong khi khung điện thoại mẫu chỉ cao 500px → ảnh tràn cả lên trên lẫn xuống dưới khung. Ảnh bằng chứng của tester xác nhận: console hiện naturalWidth=419 / naturalHeight=2048 và ảnh hiển thị đúng 200px ngang nhưng dài quá khung.

## 2. Cách fix

> Nguyên văn từ Redmine:

Sửa rule `.preview__body img` trong `public/css/popup/detail.css`: thay ràng buộc bề rộng (vốn đã có sẵn ở reset.css nên fix lần trước không có tác dụng gì) bằng giới hạn CHIỀU CAO tối đa 320px kèm `max-width 100%` → ảnh dọc cực dài tự co theo tỉ lệ để nằm gọn trong khung xem trước cao 500px; ảnh vuông/ngang (tỉ lệ cao/rộng ≤ 1.6) giữ nguyên hiển thị như cũ. Cách làm bám đúng chuẩn sẵn có của repo (`.c_h_file-preview img` và preview kịch bản đều dùng max-width + max-height). **Yokoten**: popup thật hiển thị trên site khách (`embedded-popup/default_setting.js`) cũng chỉ set width 100% không giới hạn chiều cao — cùng pattern nhưng khác phạm vi ticket nên **chỉ ghi nhận, không sửa**.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguyên văn mục 3 "ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" là **danh sách phẳng các nơi dev đã đọc/đối chiếu**, không nói rõ nơi nào bị sửa. Theo mục 4.1, chỉ `public/css/popup/detail.css` bị sửa. Cột "Thay đổi" bên dưới là suy ra từ mục 4.1 — tester confirm với dev nếu nghi ngờ.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `.preview__body img` — `public/css/popup/detail.css:322` | **CÓ SỬA** — thay `max-width` bằng `max-height:320px` + `max-width:100%` | Rule gây bug: thiếu giới hạn chiều cao |
| 2 | `.preview__main` / `.popup__preview` / `.preview__content` — `public/css/popup/detail.css:246-270` | Không sửa | Khung điện thoại mẫu cao 500px — cơ sở chọn ngưỡng 320px |
| 3 | khối `popup__preview` — `resources/views/basic/popup/create-or-update.blade.php:343-410` | Không sửa | Markup chứa thẻ ảnh preview bị áp rule |
| 4 | `img{max-width:100%}` toàn cục — `public/css/reset.css:80` (nạp ở `layout/basic/header.blade.php:22`) | Không sửa | Giải thích vì sao fix lần trước là no-op |
| 5 | `pickFile` + `validateImageDimensions` — `public/js/popup/detail.js:184`, `public/js/common/image-validation.js:12` | Không sửa | Luồng chọn file / validate kích thước phía client |
| 6 | `uploadImgBase64V2` → `resizeImageToMaxSize 2048` — `app/Helpers/functions.php:509,995` | Không sửa | Luồng resize server, cạnh lớn về tối đa 2048px |
| 7 | `PopupService::uploadImagePopup` — `app/Services/PopupService.php:167` | Không sửa | Luồng lưu ảnh popup |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> Mục 4.1 gốc của dev chỉ ghi **"File thay đổi: `public/css/popup/detail.css`"**. Bảng dưới dựng lại theo tag `F` để map coverage.

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Rule CSS `.preview__body img` — render ảnh trong khối 「プレビュー」 màn tạo/sửa popup | `public/css/popup/detail.css:322` | **Direct** — file DUY NHẤT bị sửa | `max-height:320px` + `max-width:100%`. Áp cho **mọi** ảnh nằm trong `.preview__body`, không riêng ảnh dọc |
| F2 | Luồng upload / validate / resize ảnh popup (`pickFile`, `validateImageDimensions`, `uploadImgBase64V2`, `resizeImageToMaxSize`, `PopupService::uploadImagePopup`) | `public/js/popup/detail.js`, `public/js/common/image-validation.js`, `app/Helpers/functions.php`, `app/Services/PopupService.php` | **Không đổi** (dev đã check, không sửa) | Ảnh lưu xuống server vẫn 419×2048 như cũ — fix chỉ đổi cách **hiển thị preview** |
| F3 | Popup thật render trên site khách | `public/js/embedded-popup/default_setting.js` | **Không đổi** — dev ghi nhận cùng pattern lỗi nhưng **KHÔNG sửa** (ngoài phạm vi ticket) | ⚠️ Điểm Leader cần quyết: có test / tách ticket không |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục 4.2: **"Không có"**. Mục 5 báo cáo: **"✔ Không cần recover data"**.

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Fix thuần CSS tĩnh, không chạm DB / cache / config / migration. Ảnh đã upload trước fix **không bị đổi** — chỉ đổi cách hiển thị |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

> Nguyên văn mục 4.3: *"Popup (FA-018) — khung xem trước ở màn tạo/sửa popup: giới hạn chiều cao ảnh để không tràn khung điện thoại mẫu"*.

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Popup (FA-018)** — khối 「プレビュー」 ở màn tạo/sửa popup (SCR-PU-02) | F1 | **Medium** — rule mới áp cho MỌI ảnh trong `.preview__body`: ảnh vuông/ngang (tỉ lệ ≤ 1.6) phải giữ nguyên hiển thị, ảnh dọc phải co lại |
| T2 | Popup thật hiển thị trên site khách | F3 (**không sửa**) | **Low cho fix này** — không đụng code. Nhưng dev xác nhận vẫn còn cùng lỗi ở đây |

---

## Thông tin bổ sung từ báo cáo Auto-fixbug (ngoài 4 mục template)

### 5. Recover data

✔ Không cần recover data

### 6. Verify của dev — mức `lint` (KHÔNG có unit / integration test)

- Chỉ sửa 1 file CSS tĩnh, không có PHP/Java → **không chạy** `php -l` / gradle. Kiểm cân bằng dấu ngoặc CSS bằng node: braces balanced = true.
- `git diff release_step_20260623...ai_fixbug_39036`: đúng 1 rule CSS trong `public/css/popup/detail.css`.
- Tính lại kích thước render sau fix (**tính tay**, không phải chạy thật): `419x2048 → 65x320` (nằm trong khung) · `1000x1000 → 200x200` (không đổi) · `2048x1024 → 200x100` (không đổi).
- Bằng chứng dev dựa vào: ảnh tester (prnt.sc/efd28xbC67TS) cho thấy tràn theo chiều **DỌC** chứ không phải ngang; `.popup__preview` cao 500px, ảnh mock `preview-popup.png` 395x779 render 253x500 → vùng màn hình trong khung ~449px; tổng nội dung sau fix ≈ 320 (ảnh) + ~70 (header/text/footer) < 449px.
- Chuẩn tham chiếu có sẵn trong repo: `detail.css:138 .c_h_file-preview img{max-width:210px;max-height:400px}` · `scenario/list-message.css:1330 {width:100%;max-height:300px;object-fit:contain}`.

### TỰ REVIEW của AI — ⚠️ rủi ro dev tự nêu (BẮT BUỘC cover khi viết / review TC)

- **Fix trước nhắm SAI hướng** (tưởng tràn ngang, thêm `max-width` vốn đã có sẵn ở reset.css → **no-op**, bug vẫn còn). Lần này thêm `max-height:320px`.
- **Rủi ro 1**: ảnh có tỉ lệ cao/rộng > 1.6 giờ hiển thị **hẹp hơn 200px** trong khung xem trước (vd `1000x2000 → 160x320`) — đúng ý đồ để vừa khung, nhưng **preview sẽ nhỏ hơn tỉ lệ thật của popup trên site khách** → preview không còn phản ánh đúng popup thật.
- **Rủi ro 2**: `320px` là con số **cố định** hợp với khung 500px hiện tại; nếu sau này đổi kích thước `.popup__preview` thì phải chỉnh lại.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Câu hỏi treo cho Leader / Dev

1. **F3 / yokoten**: popup thật trên site khách còn nguyên lỗi cùng pattern (dev tự thừa nhận) — tách ticket mới hay ép vào ticket này?
2. **Ngưỡng 320px** là *technical oracle* hay *requirement*? Studio đã ghi rõ "oracle implementation, không phải requirement nghiệp vụ" → expected của TC nên viết theo *"không tràn khung + giữ tỉ lệ"* thay vì chốt cứng 320px.
3. **Rủi ro 1** (preview hẹp hơn thật với ảnh tỉ lệ > 1.6) đã được PM / khách chấp nhận chưa, hay là bug mới?
