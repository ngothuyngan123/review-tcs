# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#43088 — Xóa Bot cần xóa các file media ở các serve lưu tạm, trên B2, local` |
| Module / Màn hình | Job nền xóa bot (`job:FlowDeleteBot`, chạy cron 02:00). **Không có màn hình/API nào thay đổi** (Dev xác nhận) — chỉ đổi hành vi job + 2 bảng DB mới. |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây **không phải** báo lỗi tái hiện được mà là **yêu cầu cải tiến nội bộ** (tracker "Improve nội bộ") — mô tả gốc là spec yêu cầu, không có "Tái hiện bug". Xem cảnh báo ở "Ghi chú thêm của Leader".

Bước 1: Tạo bảng `delete_folder_media_action`
- Các cột:
  1. `bot_id`
  2. `media_type`
  3. `server_ip`
  4. `status` (0: chưa chạy, 1: trong proccess, 2: done, 3: error)
  5. `delete_time` (thời gian muốn xóa)

- `media_type` và `server_ip` có 5 server:
  - tạm SSD contabo
  - tạm SSD leasedweb
  - B2: lưu lâu dài
  - contabo: backup HDD: lưu lâu dài
  - local HDD: backup

=> Tạo config cho các server (IP + thời gian muốn xóa), config có thể cấu hình riêng cho từng server.

Bước 2: Khi job xóa bot chạy:
=> Nếu server đang là staging giữ nguyên logic hiện tại (xóa thư mục local ngay).
=> Nếu trên production thì tạo record xóa cho từng server vào bảng `delete_folder_media_action` (thay vì xóa thư mục local ngay).

## Steps to reproduce

<!-- Không áp dụng — đây là yêu cầu cải tiến (feature request), không phải bug tái hiện theo bước cụ thể. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Không có attachment trên Redmine (`Attachments (0)`).

## Ghi chú thêm của Leader

⚠️ **Ticket không có "Tái hiện bug"** — đây là task cải tiến nội bộ (tracker "Improve nội bộ"), yêu cầu ban đầu là spec do `Do Van Tu TuDV` viết (mục Description), không phải mô tả hiện tượng lỗi. Root cause / cách fix nằm rải trong **12 journal** (Dev Studio tự "mở lại task" 7 vòng — v1 → v7) thay vì 1 block "Đánh giá ảnh hưởng" có cấu trúc 4 mục như quy ước — xem file [03-dev-impact.md](03-dev-impact.md) đã tổng hợp lại.

⚠️ **Task đã có 7 vòng sửa (v1 → v7)**, trong đó **5 bug con** đã được raise + fix ngay trong chính ticket này qua automation Test Studio (xem journal #152159, #152214, #153173):
- `#45291` — đổi webhook LINE phải áp dụng ở **mọi môi trường** (không chỉ production) → đã sửa.
- `#45292` — kiểm "còn bot khác dùng path" chỉ dò các bảng trong `table_path`, chưa dò mọi bảng media → **KHÔNG sửa ở web**, chuyển sang job Java `#44036` (nhánh `ai_studio_implement_44036`). **Không thuộc phạm vi test của ticket này.**
- `#45293` — path bất thường (nối phẩy, tên trần, `..`, quá dài, JSON hỏng) không được chặn trước khi tạo lệnh xóa → đã sửa (chỉ log WARNING, không tạo lệnh).
- `#45295` — mỗi lượt job phải chỉ gửi **1 tin Chatwork** gom (trước đó có thể gửi nhiều tin) → đã sửa.
- `#45317` — lệnh xóa file/thư mục bị job Java đọc trúng lúc bot **chưa xóa xong** (race condition) → đã sửa bằng mốc chờ `9999-12-31 23:59:59`, chỉ đặt giờ thật sau khi bot bị xóa khỏi bảng `bots`.
- `#45345` — dòng B2 (`media_type=3`) ghi `server_ip = NULL` thay vì `'B2'` khi `.env` không khai `DELETE_MEDIA_B2_IP` → đã sửa (commit mới nhất, journal #153173, 2026-11-09).
- `#45325` / automation `#5123` — lệch múi giờ 9 giờ do job Java chạy JVM theo UTC khi so `delete_time` → **KHÔNG sửa ở web**, chuyển sang job Java `#44036`. **Không thuộc phạm vi test của ticket này.**

⚠️ **2 bug chuyển sang ticket Java `#44036` (ngoài phạm vi test task này)**: `#45292` (kiểm dùng chung path phải dò mọi bảng media) và `#45325`/`#5123` (lệch múi giờ JVM). Nếu review-tc thấy TC test 2 case này trong phạm vi task web — flag là **ngoài phạm vi** (§6).

⚠️ **Môi trường áp dụng khác nhau theo từng phần fix** — phải đọc kỹ khi viết TC:
- **Ghi 2 bảng lệnh xóa** (`delete_folder_media_action`, `delete_file_media_action`) + **table_path** + **mốc chờ 9999** + **path bất thường chỉ log** + **1 tin Chatwork/lượt** + **log không lộ token**: **CHỈ production**. Staging/dev/local vẫn xóa thư mục media tại chỗ ngay, không ghi lệnh.
- **Đổi webhook channel LINE của bot bị xóa**: áp dụng ở **MỌI môi trường** (production, staging, local) từ vòng v5 — ⚠️ job gọi LINE thật, nên khi test ở staging/local **chỉ dùng bot/channel test hoặc mock LINE**, kiểm DB môi trường test không có bot `is_deleted=1` mang token channel thật của khách.
- Mốc ngày bot cũ: `DELETE_FILE_MEDIA_BOT_CREATED_BEFORE` (mặc định `2024-11-01`) — chỉ bot tạo **trước** mốc này mới được ghi lệnh xóa file lẻ (~30 bảng nguồn). Bot tạo từ mốc này **không có** dòng trong `delete_file_media_action` (vẫn có 5 dòng thư mục ở `delete_folder_media_action`).
- `DELETE_BOT_WEBHOOK_URL` (mặc định `https://example.com/webhook`) — Production nên đặt URL HTTPS thật của LME (chỉ trả 200), không để mặc định `example.com`.

⚠️ **Chương trình đọc 2 bảng lệnh xóa để xóa file THẬT trên từng server KHÔNG thuộc ticket này** (đây là job Java `#44036`, nhánh `ai_studio_implement_44036`). Task `#43088` (web) chỉ **ghi lệnh** vào 2 bảng — TC không nên kỳ vọng file media bị xóa thật khỏi B2/SSD/HDD sau khi chạy job web.

⚠️ **Base branch của task trên Dev Studio vẫn chưa đổi** — Dev Studio ghi nhiều lần (journal #152031, #152108, #152214, #153173) rằng task đang base trên `release_step_20260930_v2` (Laravel cũ), nhưng code thực tế đã merge lên nền Laravel 13 (`release_staging_20261104`); người phụ trách (tuanpa quyết định) cần đổi base/chọn đúng nhánh đích khi merge. Không phải vấn đề của TC nhưng Leader nên biết khi đọc diff.

⚠️ **Dữ liệu QA/test cũ của 2 bảng lệnh xóa từ các vòng trước đã lỗi thời** (B2 = NULL, giờ thật từ v1-v6, có thể `status=3` "bot still exists") — Dev khuyến nghị xóa/UPDATE tay hoặc dùng bot mới trước khi re-test, vì code mới không tự sửa dòng cũ.

⚠️ **Dòng hiện tại trong Studio** (task #528, xem file 04): 47 TC, 29 Đạt / 5 Không đạt / 13 khác, **toàn bộ chỉ chạy ở env `local`** (0 run ở dev/staging/prd) → vi phạm tinh thần RULE-08 (bill tiền/media/domain/job nền không được kết luận chỉ từ local). `reviewState = leader` (chưa review), `aiResult = fail`.

## Dữ liệu định danh ca lỗi

<!-- Không áp dụng — ticket không có ca lỗi cụ thể (feature cải tiến), không phải 1 bug tái hiện trên 1 bot/friend cụ thể. -->

## Journal / note từ Redmine (nguyên văn)

> 12 journal có nội dung điều tra (7 vòng thiết kế v1 → v7). Tóm tắt từng vòng đã đưa vào "Ghi chú thêm của Leader" + file 03. Dưới đây chép nguyên văn 2 journal quan trọng nhất (bản thiết kế gốc v1 và bản mới nhất v7) để tra cứu; các journal còn lại (v2 → v6) đọc trực tiếp trên Redmine `#43088` khi cần chi tiết từng vòng.

**Journal #144380 — Dev Studio — 2026-10-15 (thiết kế v1):**

```
Dev Studio · Nội dung thực hiện

Bản thiết kế v1 đã xong: thêm bảng delete_folder_media_action và cấu hình 5 nơi lưu (IP và thời gian chờ xoá của từng nơi). Trên production, job xoá bot (02:00) sẽ tạo 5 lệnh xoá cho mỗi bot thay vì xoá ngay thư mục media trên đĩa local. Staging và các môi trường khác giữ nguyên logic cũ. Chương trình đọc bảng và xoá thật trên từng server không nằm trong ticket. Một số điểm (nghĩa của media_type, đơn vị thời gian chờ) đang theo mặc định đã nêu và cần người xác nhận.

Hướng sửa:
- D-1 Migration tạo bảng delete_folder_media_action
- D-2 Config delete_folder_media.servers cho 5 nơi lưu
- D-3 Model, Repository và Service createForBot ghi lệnh xoá (idempotent)
- D-4 Sửa FlowDeleteBot: production tạo lệnh xoá, staging giữ nguyên

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng job job:FlowDeleteBot (cron 02:00), thêm một bảng mới và config mới; không có màn hình hay API nào. Cần test: trên production phải tạo đủ 5 bản ghi, không xoá thư mục local, dữ liệu DB của bot vẫn bị xoá; trên staging giữ nguyên hành vi cũ; job chạy lại không sinh bản ghi trùng.
```

**Journal #153173 — Dev handoff — 2026-11-09 09/11 10:21 (bản mới nhất, vòng v7 — B2 fix):**

```
Dev handoff — 09/11 10:21 · nhánh ai_studio_implement_43088

Nguyên nhân:
Trong config sns-line.delete_folder_media.servers, server_ip của B2 lấy từ env('DELETE_MEDIA_B2_IP') mà không có giá trị mặc định. Cả hai service xoá media lại đổi chuỗi rỗng hoặc null thành NULL. Vì vậy dòng B2 ghi NULL thay vì 'B2' như đã chốt và được tuanpa xác nhận ngày 09/11.

Nội dung thay đổi:
- Job xoá bot (production): dòng B2 (media_type=3) của delete_folder_media_action và delete_file_media_action ghi server_ip='B2' khi .env không khai hoặc khai rỗng DELETE_MEDIA_B2_IP; khai giá trị khác thì ghi đúng giá trị đó.
- Job xoá bot: server_ip của mọi nơi lưu được bỏ khoảng trắng hai đầu; nơi lưu 1, 2, 4, 5 không khai IP vẫn ghi NULL.
- Giữ nguyên từ các vòng trước: mốc chờ 9999 và kích hoạt sau khi xoá bot, path bất thường chỉ ghi log, một tin Chatwork mỗi lượt, log không lộ token, đổi webhook ở mọi môi trường, table_path, admin_id, mốc 2024/11/01.

Bug QA con:
- #45345 đã sửa (commit sns-line@60b0b980b0f3): Dòng B2 (media_type=3) ở cả delete_folder_media_action và delete_file_media_action ghi server_ip='B2' khi không khai hoặc khai rỗng DELETE_MEDIA_B2_IP. Re-test bằng bot mới vì dòng cũ không tự sửa.

Bug automation Test Studio:
- Bug #5111 để sau: Lỗi nằm ở job Java #44036: phải kiểm bot khác còn dùng path ở mọi bảng, không chỉ table_path. Web đã ghi table_path đúng thiết kế v3; nhánh web không đổi gì cho bug này.
- Bug #5123 để sau: Java dùng LocalDateTime.now() theo múi giờ của JVM (DeleteFileMediaTask, DeleteFolderMediaTask). Cần sửa ở #44036, hoặc chạy JVM với -Duser.timezone=Asia/Tokyo. Web ghi delete_time theo giờ app, không đổi.

Đánh giá ảnh hưởng — Rủi ro trung bình: Vòng 7 chỉ đổi giá trị một cột cho một nơi lưu, có test và kiểm chứng ngược. Mức medium giữ từ các vòng trước vì job đổi webhook LINE ở mọi môi trường và phải merge đúng nhánh đích Laravel 13.

Lưu ý khi deploy:
- Không bắt buộc khai DELETE_MEDIA_B2_IP; mặc định là 'B2'.
- Môi trường QA: dòng thử cũ của 2 bảng (B2 NULL, giờ thật hoặc status 3 từ các vòng trước) không được sửa tự động; xoá hoặc UPDATE tay trước khi re-test.

Branch: ai_studio_implement_43088
- sns-line: ai_studio_implement_43088 (nhánh gốc release_step_20260930_v2 @da7f522dd821, commit 60b0b980b0f3bb6f7285c6c374e59963a4d26691)
```

> 10 journal còn lại (v2 → v6, các bản "Dev Studio · Nội dung thực hiện" và "Dev handoff") nằm trên Redmine `#43088`, đã tổng hợp nội dung cốt lõi vào [03-dev-impact.md](03-dev-impact.md) mục 1-4.
