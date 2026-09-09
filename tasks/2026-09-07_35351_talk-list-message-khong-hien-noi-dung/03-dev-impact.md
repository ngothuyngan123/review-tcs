# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — 2 đợt. Dev human trước đó: `Nga Vũ Thị` (PR #10057, journal #131658 "Dev done") |
| Commit / Pull Request | **Đợt 2 (mới nhất, đang chờ test)**: commit `2b3402c7a6` — 4 file<br>Đợt 1: commit `f424bda154` — 3 file<br>PR human (nhánh khác): https://bitbucket.org/snstool/sns-line/pull-requests/10057/diff |
| Branch | `ai_fixbug_35351` (nhánh gốc `release_step_20260805`)<br>⚠️ Nhánh dev song song sửa **cùng vùng code**: `BugTester_35351_talklist_T4_2026` (PR #10057) |
| Ngày submit đánh giá | `2026-09-05` (journal #134561 — đợt 2). Đợt 1: `2026-08-28` (journal #133410) |
| Auto-filled | `2026-09-07 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## ⚠️ Cảnh báo chất lượng nguồn (Leader đọc trước)

> Các điểm dưới đây là **nhận xét của `/new-task` về tính nhất quán của input**, KHÔNG phải lời Dev. Cần confirm lại với Dev/AI trước khi member viết TC.

1. 🔴 **Mục 4 của đợt 2 KHÔNG được cập nhật theo đợt 2** — toàn bộ mục 4.1 / 4.2 / 4.3 (và cả mục 3, mục 6 VERIFY) trong journal #134561 **chép y nguyên từ journal #133410 của đợt 1**. Bằng chứng: mục 4.1 chỉ liệt kê **3 file** và mục 6 ghi `git diff --stat ... đúng 3 file, 76 thêm / 3 xoá`, trong khi khối **BRANCH/COMMIT của chính đợt 2 ghi `commit 2b3402c7a6, 4 file`** và mục 2 mô tả một thay đổi ở **model tin nhắn** (tách hằng số dùng chung) — file thứ 4 này **không có trong 4.1**.
2. 🔴 **Mục 4.3 KHÔNG phản ánh thay đổi hành vi lớn nhất của đợt 2**. Mục 2 tự nói: *"đây là thay đổi có ảnh hưởng hành vi — sau khi lên, màn danh sách ở trạng thái mặc định sẽ có thêm nhóm tin gửi bằng mẫu tin/hành động/hẹn giờ vốn trước nay chưa từng xuất hiện, nên **số dòng và phân trang sẽ đổi**"*, nhưng 4.3 chỉ ghi lại nội dung đợt 1 (hiển thị được nội dung). **Impact "đổi số dòng + đổi phân trang + đổi count các tab" bị thiếu khỏi bảng 4.3.**
3. ⚠️ **Mục 4.2 ghi "Không ghi dữ liệu"** — đúng về mặt CRUD, nhưng đợt 2 **đổi tập dữ liệu ĐỌC RA** (nới bộ lọc ngoặc vuông), tức đổi kết quả truy vấn danh sách. Đây là data impact dạng READ-SCOPE, không phải WRITE.
4. ⚠️ **Verify mức `lint` — chưa chạy thật**. AI ghi: MySQL dev `host.docker.internal:3306` báo `Connection refused` → *"Không kiểm chứng được bằng dữ liệu thật"*, *"chưa xác nhận bằng mắt"*.

---

## 1. Nguyên nhân

*(Nguyên văn mục ■ 1 — journal #134561, giống hệt journal #133410)*

Ticket gồm HAI triệu chứng.

**(a) Popup chi tiết tin nhắn**: điều kiện hiển thị nhãn dán viết sai (đòi trường loại-dữ-liệu vừa bằng `"msg"` vừa bằng `"sticker"` cùng lúc nên không bao giờ đúng) và **thiếu hẳn khối hiển thị cho tin tệp PDF (loại 11)**.

**(b) Cột nội dung ngoài danh sách hội thoại**: tin **gửi bằng mẫu tin (loại 16)** và **hành động (loại 18)** không tự lưu nội dung hiển thị mà phải phân giải qua `source_message` → `capture_template`; luồng dựng danh sách không làm việc này, hàm `displayType` cũng không có nhánh nào cho mã 16/18 nên rơi xuống nhánh cuối, mà cột `is_blocked` được select là `NULL` nên kết quả là chuỗi rỗng ⇒ **dòng tin hiện trắng**.

## 2. Cách fix

### Đợt 2 — commit `2b3402c7a6` (2026-09-05, bản đang chờ test)

*(Nguyên văn mục ■ 2 — journal #134561)*

Bổ sung đợt 2 theo yêu cầu human (2026-09-05), commit `2b3402c7a6` trên branch `ai_fixbug_35351`. Vấn đề còn lại: tin gửi bằng mẫu tin/hành động **KHÔNG lưu nội dung vào cột nội dung** của bảng tin nhắn (để trống, nội dung thật nằm ở bản chụp mẫu tin), mà **bộ lọc sẵn có dùng để ẩn tin dạng ngoặc vuông so sánh trực tiếp trên cột đó** — trong MySQL so sánh với giá trị rỗng-null luôn trả về `null` nên **TOÀN BỘ nhóm tin này bị loại ngay ở truy vấn**, chưa kịp tới bước lấy nội dung từ bản chụp; vì vậy ở trạng thái mặc định của màn danh sách chúng không xuất hiện, chỉ khi người dùng tự bật bộ lọc loại tin mới thấy (và trước đây thấy dưới dạng dòng trắng).

**Cách sửa**: giữ NGUYÊN ý nghĩa bộ lọc ngoặc vuông, chỉ **bọc nó thành một nhóm điều kiện HOẶC với một ngoại lệ hẹp** — cho qua những dòng có **cột nội dung để trống VÀ có liên kết tới bản ghi gửi VÀ loại tin nằm đúng nhóm mà bước map nội dung xử lý được** (mẫu tin, hành động, hành động từ đặt lịch / đặt lịch salon / đặt lịch khoá học / trả lời form). Nhờ giới hạn theo loại tin nên **các loại chưa có cách hiển thị (gửi hàng loạt, kịch bản, sự kiện) vẫn bị ẩn như cũ**, không phát sinh dòng trắng mới. Danh sách loại tin được **tách thành hằng số dùng chung ở model tin nhắn** để truy vấn và bước map luôn khớp nhau, tránh lệch về sau. **Sửa 3 file.** Đã kiểm chứng câu lệnh sinh ra đóng ngoặc đúng nhóm HOẶC.

> 🔴 **Lưu ý cho người review (nguyên văn AI)**: *"đây là thay đổi có ảnh hưởng hành vi — sau khi lên, màn danh sách ở trạng thái mặc định sẽ có thêm nhóm tin gửi bằng mẫu tin/hành động/hẹn giờ vốn trước nay chưa từng xuất hiện, nên **số dòng và phân trang sẽ đổi**; cần xác nhận đúng mong muốn và **đo lại hiệu năng truy vấn trên dữ liệu thật**."*
>
> ⚠️ Mâu thuẫn nội tại: đoạn trên ghi *"Sửa 3 file"* nhưng khối BRANCH/COMMIT của cùng journal ghi *"commit `2b3402c7a6`, **4 file**"*.

### Đợt 1 — commit `f424bda154` (2026-08-28)

*(Nguyên văn mục ■ 2 — journal #133410)*

Bổ sung theo yêu cầu human (2026-08-27), 2 điểm trên cùng branch `ai_fixbug_35351`, commit `f424bda154`.

**(1)** Danh sách loại tin lấy nội dung qua mẫu tin: trước chỉ có tin gửi bằng mẫu tin (16) và hành động (18); nay **thêm 4 loại**: hành động sinh từ **đặt lịch (19)**, **đặt lịch salon (20)**, **đặt lịch khoá học (21)** và **trả lời form (22)** — các tin này có liên kết tới bản chụp mẫu tin nên cột nội dung ngoài danh sách hội thoại lấy nội dung của mẫu tin đầu tiên, đúng như popup chi tiết vốn ưu tiên bản chụp mẫu tin khi tin có liên kết. Nhánh xử lý cũ cho 3 loại đặt lịch **vẫn giữ nguyên** và chỉ bị ghi đè khi thực sự tra được bản chụp, nên tin không có liên kết hiển thị y như trước.

**(2)** Truy vấn dựng danh sách hội thoại **loại bỏ hẳn các bản ghi sự kiện hệ thống** theo nhóm tin: thêm bạn mới, thêm bạn cũ, bạn chặn, bạn bỏ chặn, ẩn bạn, chặn bạn, xoá tin nhắn — đây là bản ghi sự kiện, không phải tin hội thoại và không có nội dung hiển thị nên trước đó lọt vào danh sách thành dòng trống.

Sửa 2 file, không đụng file khác, không bump version.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

*(Nguyên văn mục ■ 3 — giống nhau ở cả 2 journal; ⚠️ KHÔNG được cập nhật cho đợt 2)*

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `resources/views/basic/talk_list/index.blade.php` — khối popup chi tiết tin nhắn (`v-if` nhãn dán, `v-if` tệp đính kèm) | **Có sửa** | Điều kiện `v-if` nhãn dán sai logic; thiếu khối hiển thị PDF (loại 11) |
| 2 | `TalkListController::getDetailMessageTalkList` (`app/Http/Controllers/Basic/TalkListController.php`) | Đã check | Dữ liệu trả về cho popup |
| 3 | `TalkListController::ajaxGetTalkListData` (`app/Http/Controllers/Basic/TalkListController.php`) | **Có sửa** | Dữ liệu danh sách — thêm bước phân giải `source_message` → `capture_template` |
| 4 | `BotLineUser::getListMessagesV2` / `getListMessagesOld` (`app/BotLineUser.php`) | **Có sửa** | Truy vấn và bộ lọc nhãn dán; đợt 2 nới bộ lọc ngoặc vuông + loại bản ghi sự kiện hệ thống |
| 5 | `talk_list/index.js` — `displayType` + `getDetailMessageTalkList` (`public/js/talk_list/index.js`) | Đã check | Dựng nội dung cột danh sách và mở popup |
| 6 | `chat/content_chat.blade.php` | Đã check (đối chiếu, **không sửa**) | Đối chiếu cách chat 1:1 hiển thị nhãn dán và PDF |
| 7 | *(đợt 2)* Model tin nhắn — hằng số dùng chung danh sách loại tin | **Có sửa** | Để truy vấn và bước map luôn khớp nhau. ⚠️ **File này KHÔNG có tên trong mục 4.1** |

---

## 4. Đánh giá ảnh hưởng

> ⚠️ Toàn bộ mục 4 dưới đây là **nguyên văn của ĐỢT 1** — journal đợt 2 chép lại y nguyên, chưa cập nhật. Xem "Cảnh báo chất lượng nguồn" ở đầu file.

### 4.1. List function bị ảnh hưởng

*(Nguyên văn mục ■ 4.1 — Dev chỉ liệt kê **file**, không tách function)*

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Popup chi tiết tin nhắn (khối `v-if` nhãn dán / tệp đính kèm) | `resources/views/basic/talk_list/index.blade.php` | Direct | Sửa điều kiện sticker + thêm khối PDF (loại 11) |
| F2 | `getListMessagesV2` / `getListMessagesOld` — truy vấn + bộ lọc danh sách | `app/BotLineUser.php` | Direct | Đợt 1: loại bản ghi sự kiện hệ thống. Đợt 2: nới bộ lọc ngoặc vuông bằng nhóm điều kiện HOẶC |
| F3 | `ajaxGetTalkListData` — dựng dữ liệu danh sách | `app/Http/Controllers/Basic/TalkListController.php` | Direct | Thêm bước phân giải `source_message` → `capture_template` (2 truy vấn `whereIn`) |
| F4 | *(đợt 2 — Dev KHÔNG kê)* Model tin nhắn — hằng số danh sách loại tin | `<chưa rõ tên file — Dev chưa cung cấp>` | Direct | ⚠️ Suy từ mục 2 đợt 2 + khối BRANCH/COMMIT ghi 4 file. **Cần hỏi Dev bổ sung.** |
| F5 | *(gián tiếp)* `displayType` — dựng nội dung cột danh sách | `public/js/talk_list/index.js:128-181` | Indirect | Dev ghi "mọi giá trị đích đều có nhánh xử lý trong `displayType`" nhưng không kê là file thay đổi |
| F6 | *(gián tiếp)* Luồng **đổi trạng thái hàng loạt** dùng chung truy vấn danh sách | `app/BotLineUser.php` | Indirect | ⚠️ Dev KHÔNG kê. Suy từ `REQ-005` của Studio: *"luồng đổi trạng thái hàng loạt dùng chung truy vấn vẫn chạy đúng"* |

### 4.2. List data bị update khi fix bug

*(Nguyên văn mục ■ 4.2)*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `source_messages`, `capture_templates` | **READ** (thêm) | Nguyên văn: *"Không ghi dữ liệu — chỉ đọc thêm hai bảng `source_messages` và `capture_templates` để dựng nội dung hiển thị"* |
| D2 | Truy vấn danh sách — thêm 2 `whereIn` / mỗi lần tải | **READ** (thêm) | Nguyên văn: *"tối đa 100 tin/trang, chỉ chạy khi trang có tin loại 16/18; không có truy vấn trong vòng lặp"*. ⚠️ Đợt 2 mở rộng tập loại tin (16/18/19/20/21/22) → điều kiện "chỉ chạy khi có 16/18" có thể đã lỗi thời |
| D3 | `messages_v2s.source_message_id` · `source_messages.list_capture_template_id` | READ | Dev xác nhận 2 cột có thật (đối chiếu `share/db/db-refined/schema-annotated`) |
| D4 | *(Dev KHÔNG kê)* **Tập dữ liệu ĐỌC RA của danh sách hội thoại** | **READ-SCOPE thay đổi** | ⚠️ Đợt 2 nới bộ lọc → thêm nhóm tin 16/18/19/20/21/22 vào kết quả mặc định; đồng thời loại bản ghi sự kiện hệ thống (loại gửi 12–18). **Số dòng, phân trang và count các tab đều đổi.** |
| — | Recover data | — | ✔ Nguyên văn: *"Không cần recover data"* |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

*(Nguyên văn mục ■ 4.3 — chỉ 2 dòng đầu; T3–T5 là bổ sung của `/new-task`, đánh dấu rõ)*

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Chat / Talk Management (FA-002)** — cột nội dung trong Danh sách hội thoại nay hiển thị được tin gửi bằng mẫu tin và tin hành động; popup chi tiết hiển thị được tin nhãn dán và tin tệp PDF | F1, F2, F3, D1 | **High** *(nguyên văn Dev)* |
| T2 | **1-on-1 Chat (FA-001)** — chỉ đối chiếu cách phân giải mẫu tin, **không sửa** | — | **Low** *(nguyên văn Dev)* |
| T3 | ⚠️ *(Dev KHÔNG kê)* **Phân trang + nút 「次へ」 + đếm số dòng của Talk-list** (tab 「一覧」 / 「未確認のみ」) | D4, F2 | **High** — chính AI nói *"số dòng và phân trang sẽ đổi"*; Studio `REQ-005` cũng bắt buộc verify |
| T4 | ⚠️ *(Dev KHÔNG kê)* **Đổi trạng thái hàng loạt** trên Talk-list (dùng chung truy vấn) | F6, D4 | **Medium** — Studio `REQ-005` |
| T5 | ⚠️ *(Dev KHÔNG kê)* **Tìm kiếm / bộ lọc loại tin** trên Talk-list | D4 | **Medium** — Studio `REQ-011` ghi rõ *"spec chưa quy định"* hành vi khi tuỳ chọn ẩn nhãn dán/media đang tắt, hoặc khi tìm bằng chữ nhìn thấy trên cột nội dung → **cần leader xác nhận** |

---

## 5. Verify của Dev (nguyên văn ■ 6)

| Mục | Nội dung |
|---|---|
| **Mức verify** | `lint` — **KHÔNG chạy thật, KHÔNG xác nhận bằng mắt** |
| Lệnh | `php -l` sạch trên 3 file; kiểm autoload `App\SourceMessage`; hằng `CaptureTemplate` 1-9 và `MessagesV2` 16/18 resolve đúng; `ConversationService::isJson` phân biệt đúng JSON và đường dẫn ảnh; `git diff --stat origin/release_step_20260805...ai_fixbug_35351` → **3 file, 76 thêm / 3 xoá** ⚠️(số liệu của đợt 1) |
| 🔴 Không kiểm chứng được | **MySQL dev `host.docker.internal:3306` báo `Connection refused`** → không kiểm chứng được bằng dữ liệu thật |

### Rủi ro / lưu ý khi test (nguyên văn ■ TỰ REVIEW)

1. **Không chạy được trên môi trường dev** (web/MySQL không kết nối được) nên chưa xác nhận bằng mắt; cần tester mở Danh sách hội thoại với **tin gửi bằng mẫu tin, tin hành động, tin nhãn dán và tin PDF**.
2. **Mẫu tin loại `image_map`**: nội dung lưu là **đường dẫn ảnh thuần** nên nay ánh xạ về loại ảnh và dùng thẳng làm đường dẫn; **nếu tồn tại bản ghi cũ lưu dạng JSON thì ô sẽ hiện nhãn ảnh kèm ảnh hỏng thay vì ảnh thật** — vẫn tốt hơn ô trắng và không gây lỗi (không kết nối được CSDL dev để kiểm chứng dữ liệu cũ).
3. **Thêm 2 truy vấn `whereIn` mỗi lần tải danh sách**; đã giới hạn theo đúng id của trang hiện tại (tối đa 100 tin) và chỉ chạy khi trang có tin loại 16/18.
4. **Nhánh dev `BugTester_35351_talklist_T4_2026` (PR #10057) sửa cùng vùng code**; nếu PR đó được gộp sau này sẽ có xung đột — người review cần quyết định lấy bản nào.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — 🔴 **HIỆN ĐANG THIẾU file thứ 4 (model tin nhắn) của đợt 2**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — 🔴 **HIỆN ĐANG THIẾU impact READ-SCOPE (D4)**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — 🔴 **HIỆN ĐANG THIẾU T3 (phân trang/count), T4 (bulk status), T5 (search/filter)**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Câu hỏi cần hỏi Dev/AI trước khi viết TC

1. **File thứ 4 của commit `2b3402c7a6` là file nào?** (mục 2 nói tách hằng số ở "model tin nhắn" nhưng 4.1 chỉ có 3 file)
2. **Việc màn danh sách mặc định có thêm nhóm tin 16/18/19/20/21/22 — có đúng là hành vi mong muốn không?** Ai (PO/Leader) đã duyệt? Số dòng + phân trang + count tab đổi là **chấp nhận được**?
3. **Đợt 2 mở rộng tập loại tin lên 16/18/19/20/21/22, nhưng 4.2 vẫn ghi "chỉ chạy khi trang có tin loại 16/18"** — điều kiện kích hoạt 2 truy vấn `whereIn` thực tế là tập nào?
4. **Chốt nhánh nào**: `ai_fixbug_35351` hay `BugTester_35351_talklist_T4_2026` (PR #10057)?
5. **Có bản ghi `image_map` cũ lưu dạng JSON trên production không?** (rủi ro #2 — Dev không kiểm chứng được vì mất kết nối DB dev)
