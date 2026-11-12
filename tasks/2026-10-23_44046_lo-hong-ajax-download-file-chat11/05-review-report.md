# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; file này = round 1.
> Report chỉ ghi phần THIẾU + việc phải làm. Bảng coverage 2 chiều và bảng quan điểm đầy đủ đã chạy nội bộ, không ghi ở đây.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #509 (ticket 44046, round 1, branch `ai_studio_fixbug_44046`) — snapshot ở `04-tc-list.md` |
| Tổng số TC review | 38 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `BUG` + F1–F4 + T1–T6 ở `03-dev-impact.md` (không có D) | 11/11 mục có TC, nhưng 5 mục còn `RISK` (F3 · F4 · T1 · T5 · T6) — **CHƯA ĐỦ** |
| **(b) diff code** — 2 file `spec_delta` + 8 điểm `dev_impact` của Studio | 5/10 điểm đủ · 4 `RISK` · 1 `GAP` — **CHƯA ĐỦ** |

**Kết luận**: 11/21 vùng ảnh hưởng đủ TC · 1 GAP · 9 RISK (gộp thành 9 dòng G1–G9).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F3 — nhánh Dropbox tải thẳng (`isDropboxHost` / `fetchFromDropbox`) | dev-impact | NEW-14, NEW-25 (skip) · NEW-10, NEW-15 (pass — chỉ nhánh bị từ chối) | `RISK` — nhánh tải thành công chưa chạy lần nào; chưa có tên file tiếng Nhật, chưa có link Dropbox định dạng hiện tại có query | `[MAJOR]` |
| G2 | F4 + T5 — `/ajax/get-file-url`, caller friend info | dev-impact | NEW-36 (skip) · NEW-33, NEW-34 (pass — form answer) | `RISK` — caller friend info chưa chạy; đây là caller spec ghi rõ (detail-friend EP-28: ảnh custom field) | `[MAJOR]` |
| G3 | T1 — Chat 1:1 tải video / PDF·xlsx / preview mẫu tin | dev-impact | NEW-22, NEW-24, NEW-25 (skip) · NEW-21, NEW-23 (pass) | `RISK` — 3/5 loại nội dung chưa chạy; không TC nào tách media **friend gửi** vs **bot gửi**, chưa có nút tải trong bản xem trước ảnh (kho `TC-CHT-259`) | `[MAJOR]` |
| G4 | T6 — symlink trong thư mục allowlist trỏ ra ngoài | dev-impact | NEW-6 (skip, chỉ local) | `RISK` — Dev ghi ở "Điểm cần test", chưa chạy | `[MAJOR]` |
| G5 | Allowlist đọc local 6 thư mục (`msg_template` · `msg_template2` · `chat_images` · `chat_files` · `qr_image` · `FOLDER_MEDIA`) | diff code | NEW-21 (chat_images, pass) · QR NEW-27–31 (pass) · NEW-13, NEW-16 (skip) | `RISK` — `msg_template`, `msg_template2`, `chat_files` chưa có TC đọc file hợp lệ nào pass | `[MAJOR]` |
| G6 | URL tuyệt đối host khác (tin cũ) → bỏ host, lấy path | diff code | NEW-26, NEW-22 (skip) | `RISK` — đây là **rủi ro hồi quy chính** Dev + Studio nêu, 0 TC có kết quả; NEW-26 expected 2 nhánh (xem I6) | `[BLOCKER]` |
| G7 | Dropbox so khớp host chính xác — `dl.dropbox.com` bị loại | diff code | NEW-15 (pass) | `RISK` — expected "nhiều khả năng 502, cần human xác nhận" → pass không có nghĩa; chưa chốt link `dl.dropbox.com` có phải "link Dropbox" theo Dev handoff không (§8 #4) | `[MAJOR]` |
| G8 | Cắt query cho **mọi** type (trước chỉ audio) | diff code | NEW-13 (skip), NEW-23 (pass) — đều là audio | `GAP` — 0 TC cho type khác audio có query | `[MAJOR]` |
| G9 | `hasUnsafeSegment` chỉ decode 1 lần — path mã hoá 2 lần đi tiếp sang media server | diff code | NEW-19 (pass) | `RISK` — expected đang **chấp nhận** hành vi này (dồn sang bug 3721); cần Dev/Leader chốt chấp nhận hay phải chặn ở tầng app (§8 #5) | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 11 quan điểm Trigger khớp task · 9 chưa cover đủ (đủ: `FUNC-004`, `SEC-001` phần secret local).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `ENV-003` | Cao | `RISK` — task chạm media/file + domain; TC đúng ý định duy nhất là #33255 nhưng gắn mã `RULE-12`, `skip`, `env_scope = all` thay vì prd. Không TC prd cho file chỉ có ở domain khác | `[BLOCKER]` |
| Q2 | `COMPAT-LEGACY-001` | Cao | `RISK` — nhánh dữ liệu cũ (URL tuyệt đối) chỉ có NEW-26 (mã `TOOL-OLDREC-001`), NEW-22 (mã `RULE-09`) — đều skip; NEW-15 mang mã này nhưng expected chưa chốt | `[MAJOR]` |
| Q3 | `FUNC-001` | Cao | `RISK` — chỉ NEW-16 (skip, local). Luồng chính tải file/QR (NEW-21, 23, 24, 25, 27–31) mang mã `RULE-TOOL-027/028` → **đổi mã sang `FUNC-001`**, không cần TC mới | `[MAJOR]` |
| Q4 | `SEC-002` | Cao | `RISK` — root cause là lộ credential trong `.env`; nội dung chặn đã có (NEW-1 mã `TOOL-KNOW-002`, NEW-2…10, 19, 35 mã `SEC-INJECT-001`) → **đổi mã sang `SEC-002`**, không cần TC mới | `[MAJOR]` |
| Q5 | `OUT-TRUTH-001` | Cao | `RISK` — NEW-32, #33254 đều skip; thiếu Normal/Boundary không ghi lý do (RULE-01) | `[MAJOR]` |
| Q6 | `REG-SHARED-001` | Cao | `RISK` — NEW-36 (friend info) skip; thiếu Boundary không ghi lý do (RULE-01) | `[MAJOR]` |
| Q7 | `FUNC-003` | Cao (field URL) | `RISK` — chỉ NEW-13 (skip); chưa có Boundary cho query trong `link_url` | `[MAJOR]` |
| Q8 | `DATA-TEXT-001` | Trung bình | `RISK` — NEW-14 (skip) chỉ dùng tên file ASCII; server tự lấy segment cuối URL làm `file_name` → tên tiếng Nhật chưa được kiểm | `[MAJOR]` |
| Q9 | `PERM-003` / `SEC-001` (cách ly đa tài khoản) | Cao | `GAP` — không TC tài khoản bot B tải file chat của bot A. Fix **không đổi** phạm vi bot và file media có URL công khai trên media server → chưa có căn cứ expected. **Hỏi Dev** endpoint có cần kiểm bot không; ngoài phạm vi fix thì ghi ticket riêng. Hạ từ BLOCKER xuống MAJOR — Leader chốt | `[MAJOR]` |

- Q1 / Q2 lấp bằng TC G6 ở §7 + chạy lại #33255 trên prd. Q3 / Q4 chỉ cần đổi mã trên Studio. Q5 / Q6 lấp bằng chạy TC đang skip (lý do thiếu Normal của Q5: tải thành công không có thông báo). Q7 → TC-FUNC003-01/02. Q8 → TC-DATATEXT001-01. Q9 không đề xuất TC — chờ Dev.

---

## 3. TC trùng lặp nội dung

Đã rà 38 TC, không phát hiện trùng lặp.

- NEW-21, NEW-27–31 là tập con các bước của #33255 nhưng khác môi trường (#33255 là smoke **prd**) → không tính trùng, giữ cả.
- NEW-19 vs NEW-35 khác dạng mã hoá input (đã phân biệt trong `Ghi chú` của NEW-35) → không trùng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-33, NEW-34 | Tham số + shape response của `POST /ajax/get-file-url` | Gửi `link_url`; trả `{success, data}` / `{success:false, code:'INVALID_FILE_PATH', msg}` | `spec-features/admin/detail-friend/web/api-spec.md` L798–810 (EP-28): "**Body**: `file_path` hoặc `key`" · "**Response**: `{"url": "https://..."}`" | (A) TC gửi sai tên tham số → 422 do thiếu field, **pass giả** ở NEW-34 · (B) spec cũ hơn #43709 / task-496 → cần update | `[MAJOR]` | Dev |

**Đã rà**: 38 TC × `spec-features/admin/chat-11/feature-spec.md` (EP-39 L510 — chỉ 1 dòng mô tả, không có business rule) + `spec-features/admin/detail-friend/web/api-spec.md` (EP-28) + `kho-tcs/fa001-chat11-11チャット.md` (`TC-CHT-259`, `TC-CHT-366`) + `kho-tcs/fa007-settingaddfriend-あいさつメッセージ.md` (`TC-SAF-26`, `-27`, `-30`) — 1 mâu thuẫn (C1). Kho chưa có tab QR code v2 (qr-landing) → không đối chiếu được NEW-30, NEW-31. Không có mục khớp `framework/ignore-features.md`.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — 12 TC | Pass thật 26/38 = **68%** (< 80%). 12 skip: NEW-6, 13, 14, 16, 22, 24, 25, 26, 32, 36, #33254, #33255 (8 skip loại `need-prep`) | Chuẩn bị dữ liệu (video, PDF/xlsx, link Dropbox thật, tin cũ URL tuyệt đối, friend info có file) rồi chạy lại |
| I2 | `[MAJOR]` | Nguồn — 38 TC | **RULE-08 / ENV-003**: 38/38 chạy staging, **0 TC prd**; task chạm media/file + domain. #33255 (smoke prd) skip và `env_scope = all` | Đổi `env_scope` #33255 thành `prd`, chạy sau release; G6 chạy cả prd |
| I3 | `[MAJOR]` | Spec | `chat-11/feature-spec.md` L510 chỉ ghi "Download file (image/audio/pdf) dạng base64" — không có rule allowlist / 422 / max 2048 / Dropbox. Expected của 21 TC nhóm API lấy từ Dev handoff, chưa có chuẩn độc lập | Bổ sung spec (§8 #1) |
| I4 | `[MAJOR]` | NEW-7, NEW-8, NEW-10 | Expected "server không gọi tới host đó" nhưng bước quan sát là **tuỳ chọn** ("nếu có thể dựng listener") → pass trên staging không chứng minh được điều kiện này | Bắt buộc 1 bước quan sát (log outbound / listener do Dev cung cấp) hoặc đổi oracle sang mã HTTP + body (xem I5) |
| I5 | `[MAJOR]` | NEW-7 (payload 2), NEW-8, NEW-10, NEW-17, NEW-19 | **RULE-13**: TC gửi request trực tiếp nhưng expected không ghi mã HTTP cụ thể ("đi media server", "502/not_found hoặc nội dung từ media server") | Ghi mã cụ thể theo Dev handoff (path không có ở media server → `502`) |
| I6 | `[MAJOR]` | NEW-15, NEW-26 | Expected không đo lường được: NEW-15 "nhiều khả năng 502 — CẦN HUMAN XÁC NHẬN" nhưng đã pass; NEW-26 gộp 2 kết quả (200 hoặc 502) tuỳ dữ liệu | NEW-15 chờ §8 #4 rồi sửa expected; NEW-26 thay bằng TC-COMPATLEGACY001-01/02 ở §7 |
| I7 | `[MAJOR]` | NEW-27–31 | **RULE-06**: expected dừng ở "PNG hợp lệ (quét được)" — không đối chiếu URL quét ra = URL kết bạn của **đúng bot** (kho `TC-SAF-26`). Fix đổi cách tìm file (bỏ host, ưu tiên file local) | Bổ sung expected: quét ảnh ra `https://line.me/R/ti/p/%40<line_id bot đang chọn>` |
| I8 | `[MAJOR]` | NEW-33, NEW-36 | Tiền điều kiện không dựng lại được: NEW-33 "màn kết quả form" không nói màn nào (回答一覧 FA-011? rightbar フォーム回答 chat kho `TC-CHT-366`?); NEW-36 tự ghi "chưa xác định UI" | NEW-36: dùng ảnh custom field friend info theo spec EP-28; NEW-33: ghi route + loại file. Hỏi Dev rightbar フォーム回答 có gọi `get-file-url` không |
| I9 | `[MINOR]` | NEW-11, NEW-12 | **RULE-13**: ép riêng `400` (thiếu field / mảng) và `422` (rỗng / vượt 2048) — quy ước là **400 hoặc 422 đều Đạt** → rủi ro fail giả | Đổi expected thành `400 hoặc 422` |
| I10 | `[MINOR]` | NEW-28–31 | **[AP-3]** caller QR chỉ có happy path; chỉ header có TC lỗi (NEW-32, skip). 4 màn còn lại dùng 3 file JS xử lý lỗi khác nhau | Thêm nhánh lỗi vào NEW-28–31 hoặc ghi lý do bỏ |
| I11 | `[NIT]` | NEW-5 | 1 payload trong danh sách "Điểm cần test" của Dev (journal #147445, dòng đầu — dạng chữ `http` không có `://`) chưa nằm trong dữ liệu TC nào | Thêm vào dữ liệu NEW-5 (cùng nhánh path không bắt đầu bằng `/`) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 38 TC — không có TC nào ngoài phạm vi task.

- NEW-20 (chưa đăng nhập → 401) test middleware `check_login` không bị chạm code, nhưng **giữ**: là TC duy nhất xác nhận điều kiện khai thác của `BUG` ("chỉ cần đăng nhập").

---

## 7. TCs đề xuất bổ sung (8)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` · `kho-tcs/fa007-settingaddfriend-あいさつメッセージ.md`. Kho chưa có tab QR code v2 (qr-landing) |
| Vùng regression phát hiện từ kho | `TC-CHT-259` (tải media của cả bot và friend, tải trong bản xem trước) · `TC-SAF-26` (QR quét ra đúng OA) · `TC-CHT-366` (rightbar フォーム回答 có ảnh/PDF) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho | Không |
| Căn cứ TC regression `R<x>` | R1 ← kho `TC-CHT-259` bước 4 |
| Không đẻ TC mới | G1 (trừ phần tên JP), G2, G4: trùng NEW-14 / NEW-25, NEW-36, NEW-6 (BƯỚC 5b) → chạy TC hiện có, sửa NEW-36 theo I8 · G7, G9: chờ §8 #4, #5 · Q3, Q4: đổi mã · Q9: chờ Dev |
| Xác nhận chống trùng | Đã đối chiếu 38 TC ở BƯỚC 0 + 2 file kho — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-01 | UI | FUNC-001 | Chat 1:1 1:1チャット: Tải media do bạn bè gửi từ app LINE | Normal | auto | dev, local, prd, staging | web, line-friend | Chat 1:1: tải ảnh, video, audio, file do bạn bè gửi từ LINE sau fix download-file-chat11 | - Đăng nhập admin, chọn bot test đã liên kết LINE OA<br>- Bạn bè test F01 (システム表示名 QA44046_F01) đã kết bạn với bot<br>- Trình duyệt thật, mở DevTools Network | 1. Từ app LINE, F01 gửi vào bot: 1 ảnh JPG, 1 video MP4, 1 tin thoại, 1 file PDF.<br>2. Admin mở Chat 1:1 1:1チャット, chọn hội thoại F01.<br>3. Bấm icon tải xuống trên tin ảnh.<br>4. Bấm icon tải xuống trên tin video.<br>5. Bấm icon tải xuống trên tin thoại.<br>6. Bấm icon tải xuống trên tin file PDF.<br>7. Mở lần lượt 4 file đã tải. | Ảnh `qa44046_f01.jpg` · video `qa44046_f01.mp4` (≤ 10 giây) · tin thoại ≈ 5 giây · `qa44046_f01.pdf` (1 trang) | - Mỗi lần bấm tải đúng 1 file, mở được, không rỗng<br>- Ảnh / video / PDF trùng nội dung file F01 đã gửi; tin thoại phát được<br>- 4 request `POST /ajax/download-file-chat11` đều trả `200`, `success = true`<br>- Không hiện alert lỗi | | Lấp G3 · media friend gửi lưu ở thư mục khác media bot gửi — TC hiện có không tách · Đánh giá spec: Spec không ghi (EP-39 chỉ 1 dòng) · Evidence: file tải về + screenshot Network |
| TC-FUNC001-02 | UI | FUNC-001 | Chat 1:1 1:1チャット: Nút tải trong bản xem trước ảnh | Normal | auto | dev, local, prd, staging | web | Chat 1:1: tải ảnh từ bản xem trước (lightbox) — 1 lần bấm ra đúng 1 file | - Đăng nhập admin, chọn bot test<br>- Hội thoại F01 (QA44046_F01) có 1 tin ảnh do bot gửi và 1 tin ảnh do F01 gửi<br>- Thư mục Downloads trống | 1. Mở Chat 1:1 1:1チャット, chọn hội thoại F01.<br>2. Bấm vào tin ảnh do bot gửi để mở bản xem trước.<br>3. Bấm nút tải trong bản xem trước 1 lần.<br>4. Đếm file trong Downloads.<br>5. Lặp bước 2–4 với tin ảnh do F01 gửi. | 2 ảnh: `qa44046_bot.png` (bot gửi), `qa44046_f01.jpg` (F01 gửi) | - Mỗi lần bấm chỉ tải đúng 1 file → Downloads có tổng 2 file<br>- 2 file mở được, đúng ảnh tương ứng<br>- Không hiện alert lỗi | | Lấp R1 · regression · dẫn từ kho `TC-CHT-259` bước 4 · cần Dev xác nhận nút tải trong bản xem trước gọi cùng `downLoadFile` — nếu không thì bỏ TC · Đánh giá spec: Spec không ghi · Evidence: screenshot Downloads |
| TC-FUNC001-03 | API | FUNC-001 | Chat 1:1 1:1チャット: Endpoint download-file-chat11 đọc file hợp lệ ở từng thư mục allowlist | Boundary | auto | dev, local, staging | api | download-file-chat11: đọc được file hợp lệ ở thư mục msg_template, msg_template2, chat_files, qr_image | - Đăng nhập admin, chọn bot test<br>- Dev đặt sẵn 4 file trong `public/`: `msg_template/qa44046.png` · `msg_template2/qa44046.png` · `chat_files/qa44046.pdf` · `qr_image/qa44046.png`<br>- Có 1 request tải ảnh thành công trong Chat 1:1 để Copy as fetch | 1. Copy request `POST /ajax/download-file-chat11` thành fetch.<br>2. Đổi `link_url` = `/msg_template/qa44046.png`, gửi.<br>3. Đổi `link_url` = `/msg_template2/qa44046.png`, gửi.<br>4. Đổi `link_url` = `/chat_files/qa44046.pdf`, gửi.<br>5. Đổi `link_url` = `/qr_image/qa44046.png`, gửi.<br>6. Giải mã `data` base64 của từng response, so với file gốc. | 4 `link_url` ở bước 2–5 | - Cả 4 request trả `200`, `success = true`<br>- `data` giải mã trùng byte với file gốc tương ứng<br>- Không request nào trả `422` | | Lấp G5 · Studio `dev_impact`: allowlist 6 thư mục, mới có `chat_images` pass · không chạy prd vì phải ghi file vào `public/` của server · Đánh giá spec: Spec không ghi · Evidence: response JSON + so khớp hash file |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Chat 1:1 1:1チャット: Tin cũ lưu URL tuyệt đối domain khác — file có trên media server | Normal | auto | dev, local, prd, staging | web | Chat 1:1: tin cũ chứa URL tuyệt đối domain web khác vẫn tải được khi file có trên media server | - Đăng nhập admin, chọn bot có tin cũ (trước release) mà nội dung là URL tuyệt đối trên domain web khác domain đang chạy (vd `sns.` / `booking.`)<br>- Dev xác nhận file của tin đó **có** trên media server<br>- Trình duyệt thật, mở DevTools Network | 1. Mở Chat 1:1 1:1チャット, chọn hội thoại có tin cũ.<br>2. Bấm icon tải xuống trên tin cũ.<br>3. Xem `link_url` gửi lên ở Network.<br>4. Mở file đã tải. | Tin cũ do Dev chỉ định (ghi `bot_id` + id tin vào evidence) | - Request trả `200`, `success = true`<br>- File tải về mở được, đúng nội dung tin cũ<br>- Không hiện alert lỗi | | Lấp G6, Q1, Q2 · tách nhánh 1 của NEW-26 (I6) · RULE-08: phải có kết quả prd · Đánh giá spec: Spec không ghi · Evidence: screenshot Network + file |
| TC-COMPATLEGACY001-02 | UI | COMPAT-LEGACY-001 | Chat 1:1 1:1チャット: Tin cũ lưu URL tuyệt đối domain khác — file chỉ có ở domain đó | Abnormal | auto | dev, local, prd, staging | web | Chat 1:1: tin cũ có file chỉ nằm ở domain web khác — báo lỗi tải, không im lặng | - Đăng nhập admin, chọn bot có tin cũ mà nội dung là URL tuyệt đối trên domain web khác<br>- Dev xác nhận file **không** có ở local lẫn media server, chỉ có ở domain đó<br>- Trình duyệt thật, mở DevTools Network | 1. Mở Chat 1:1 1:1チャット, chọn hội thoại có tin cũ.<br>2. Bấm icon tải xuống trên tin cũ.<br>3. Đọc alert hiện ra.<br>4. Xem status request ở Network. | Tin cũ do Dev chỉ định (ghi `bot_id` + id tin vào evidence) | - Request trả `502`<br>- Alert 「ダウンロードに失敗しました。」<br>- Không tải file rỗng, không hiện `undefined` | | Lấp G6, Q2 · tách nhánh 2 của NEW-26 (I6) · expected theo Dev handoff — chờ §8 #3 chốt chấp nhận hồi quy · Đánh giá spec: Spec không ghi · Evidence: screenshot alert + Network |
| TC-FUNC003-01 | API | FUNC-003 | Chat 1:1 1:1チャット: Endpoint download-file-chat11 cắt query với type khác audio | Normal | auto | dev, local, prd, staging | api | download-file-chat11: link ảnh có query (type rỗng) vẫn đọc đúng file sau khi cắt query | - Đăng nhập admin, chọn bot test<br>- Hội thoại có 1 tin ảnh tải được (request `200`)<br>- Có request đó dạng Copy as fetch | 1. Ghi lại `link_url` gốc của tin ảnh (vd `/chat_images/<tên>.png`).<br>2. Gửi lại request với `link_url` = `<link gốc>?v=1729650000`, `type` rỗng.<br>3. Gửi lại request với `link_url` gốc, `type` rỗng.<br>4. So `data` của 2 response. | `?v=1729650000` nối vào `link_url` gốc | - Bước 2 và 3 đều trả `200`, `success = true`<br>- `data` của 2 response giống hệt nhau (query bị bỏ, đọc cùng 1 file) | | Lấp G8, Q7 · Studio `dev_impact`: "query luôn bị cắt (trước chỉ audio)" · ảnh QR có `?v=<timestamp>` (FA-007 BR-06) · Đánh giá spec: Spec không ghi · Evidence: 2 response JSON |
| TC-FUNC003-02 | API | FUNC-003 | Chat 1:1 1:1チャット: Endpoint download-file-chat11 giới hạn 2048 tính cả query | Boundary | auto | dev, local, prd, staging | api | download-file-chat11: link_url path ngắn + query dài — 2048 ký tự qua validate, 2049 bị chặn | - Đăng nhập admin, chọn bot test<br>- Có 1 request tải ảnh thành công dạng Copy as fetch | 1. Lấy `link_url` gốc của tin ảnh.<br>2. Nối `?q=` + chuỗi `a` sao cho tổng độ dài đúng 2048 ký tự, gửi.<br>3. Nối thêm 1 ký tự `a` (tổng 2049), gửi. | Tổng `link_url` 2048 ký tự / 2049 ký tự | - Bước 2: `200`, `success = true`, `data` đúng ảnh gốc (validate tính độ dài trước khi cắt query)<br>- Bước 3: `400` hoặc `422`, lỗi validate trường `link_url`, không có `data` | | Lấp G8, Q7 · RULE-01: Abnormal của nhánh cắt query đã có ở NEW-12, NEW-18 · Đánh giá spec: Spec không ghi (rule max:2048 từ Dev handoff) · Evidence: 2 response JSON |
| TC-DATATEXT001-01 | API | DATA-TEXT-001 | Chat 1:1 1:1チャット: Tải thẳng Dropbox — tên file tiếng Nhật, link định dạng hiện tại | Normal | auto | dev, local, prd, staging | api | download-file-chat11: link Dropbox định dạng hiện tại, tên file tiếng Nhật — tải được và file_name đúng | - Đăng nhập admin, chọn bot test<br>- Tài khoản Dropbox test có file 「研修動画_10月.mp4」 (≤ 5 MB)<br>- Lấy link chia sẻ tải trực tiếp trên host `dl.dropboxusercontent.com`, giữ nguyên tham số query Dropbox cấp<br>- Có 1 request tải ảnh thành công dạng Copy as fetch | 1. Gửi request với `link_url` = link Dropbox đã lấy (nguyên query).<br>2. Đọc trường `file_name` của response.<br>3. Giải mã `data`, mở video. | Link chia sẻ Dropbox của 「研修動画_10月.mp4」 | - Trả `200`, `success = true`<br>- `file_name` = 「研修動画_10月.mp4」 (đã giải mã, không phải chuỗi `%E7%A0…`)<br>- Video giải mã phát được, đúng file gốc | | Lấp G1, Q8 · nhánh Dropbox chưa từng pass (NEW-14, NEW-25 skip) · link Dropbox hiện tại mang query — giao với điểm "luôn cắt query" của Studio `dev_impact` · Đánh giá spec: Spec không ghi · Evidence: response JSON + video |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/feature-spec.md` L510 + `web/api-spec.md` L53 + `web/logic-spec.md` L69 (EP-39) | Bổ sung rule sau fix: allowlist thư mục · path xấu → `422` 「ファイルのパスが正しくありません。」 · `link_url` max 2048 · chỉ Dropbox tải thẳng · URL host khác bỏ host lấy path · file không có → `502` | I3 (spec không có rule) | Dev |
| 2 | `spec-features/admin/detail-friend/web/api-spec.md` L798–810 (EP-28) | Tham số (`file_path`/`key` hay `link_url`) và shape response (`{"url"}` hay `{success, data / code, msg}`) | C1 `CONF-SPEC` | Dev |
| 3 | `chat-11` EP-39 (rule dữ liệu cũ) | Tin cũ URL tuyệt đối có file chỉ ở domain khác: chấp nhận `502` (hồi quy Dev đã nêu) hay phải tải được | G6 | Leader / PM |
| 4 | `chat-11` EP-39 (Dropbox) | `dl.dropbox.com` có thuộc "link Dropbox tải thẳng" không (Studio: thiếu trong danh sách host) | G7 | Dev |
| 5 | `chat-11` EP-39 (validate path) | Path mã hoá 2 lần: chấp nhận chuyển sang media server (gộp bug 3721) hay phải chặn ở tầng app | G9 | Dev / Leader |
