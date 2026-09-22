# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #314 |
| Tổng số TC review | 20 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `0/8 vùng dev-impact đủ TC` (toàn bộ 20 TC chưa chạy — xem I1) · ngoài lý do chưa chạy: `1 GAP · 4 RISK (dev-impact) · 3 RISK (diff code) · 1 orphan`.

`Input thiếu: không có diff` — Studio `spec_delta.diffAvailable = false` (không tìm thấy ref `m_202609_replace_json_41108`), commit `fcee76a` không truy cập được → chiều (b) suy từ `dev_impact` của Studio + mục 1/2/3 file 03.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — ca KH đã report (friend `つか咲"き`, bot つっつん, production) | `dev-impact` | NEW-1, NEW-7 | RISK — Dev **không phục hồi data cũ** (4.2) → sau deploy hội thoại của chính KH báo lỗi **vẫn trắng**. NEW-7 ghi rõ "không tính là fail của #41108". Không TC nào verify ca KH được giải quyết. Ticket có thể đóng trong khi KH vẫn lỗi. | `[BLOCKER]` |
| G2 | `F2 — isJsonContent` (mới) | `dev-impact` | NEW-6, NEW-9, NEW-13 | RISK — chỉ test content `RemindBookingContent`. Hàm áp cho **mọi** content JSON đi qua `applyReplaceContent`, nhưng Dev không kê loại content JSON nào khác. Kho `TC-CHT-249` cho thấy template button (standard / color / ảnh) và quick reply đều trích dẫn được. Quy tắc nhận diện JSON chưa có (NEW-6 đang chờ Dev). | `[MAJOR]` |
| G3 | `D1` — bản ghi `quote_message_content` hỏng trước fix | `dev-impact` | NEW-7, NEW-17, NEW-18 | RISK — NEW-18 (kiểm kê bản ghi hỏng) chỉ khai `env_scope = local` → không đáp ứng **RULE-04** (thống kê **toàn hệ thống**). Số hội thoại KH còn trắng trên production chưa có. | `[MAJOR]` |
| G4 | `T3` — trích dẫn **tin friend gửi** | `dev-impact` | không có | GAP — Dev kê "tin friend gửi: check không thay đổi behavior", Studio `dev_impact` ghi `checkFindQuoteMessage` gồm 3 nhánh (tin bot / tin friend / tin hành động từ đặt lịch). Nhánh **tin friend** 0 TC. | `[MAJOR]` |
| G5 | `T4` — callback group / inactive user | `dev-impact` | NEW-11 | RISK — 1 TC Normal, tiền đề "bạn bè đã chặn bot" không gửi tin được (xem I8) → nhánh `handleMessageInactiveUser` thực tế chưa có cách chạy **[AP-3]**. | `[MAJOR]` |
| G6 | Escape generic trong `applyReplaceContent` | `diff code` | NEW-8, NEW-15 | RISK — trigger đã test: `"` · `\` · xuống dòng `\n`. **Chưa có trigger ngoài danh sách Dev kê**: `\r` (CRLF khi nhập textarea friend info trên web), tab, ký tự điều khiển, `$` / `\` trong chuỗi thay thế nếu code dùng `replaceAll` (regex). Không có diff nên chưa biết Dev escape bằng Jackson toàn bộ hay tay 3 ký tự. | `[MAJOR]` |
| G7 | Chức năng tương tự: cặp **Salon / Lesson / Event** | `diff code` | NEW-1 (salon), NEW-2 (lesson) | RISK — REG-SHARED-001 nêu cặp Salon/Lesson/Booking Event là điểm lặp. Kho `TC-CHT-252` có đường gửi "Event remind (cũ và mới)" được friend trích dẫn lại. Dev chỉ kê salon/lesson; event remind + form remind chưa có TC. | `[MAJOR]` |
| G8 | Web `chat-v2.js` `showMessageQuotedSalonLesson` — `JSON.parse` không `try/catch`, code web **không đổi** | `diff code` | NEW-7 | RISK — chỉ 1 bản ghi hỏng (dữ liệu cũ hoặc trigger ở G6) vẫn làm trắng **cả** khung chat PC. TC không khắc phục được → không đề xuất TC, đưa §6 để Dev/Leader chốt hardening. | `[MAJOR]` |
| G9 | NEW-19 | `orphan` | — | TC test API lịch sử tin của web (`ChatController.php`) — code web không bị sửa **[AP-5]**. Giữ làm regression hoặc bỏ. | `[NIT]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `8 quan điểm Trigger khớp task · 6 chưa cover đủ` (đã đủ: DATA-TEXT-001 — NEW-8 · SYNC-APP-001 — NEW-20).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | RISK — nội dung luồng chính **có** (NEW-1 UI, NEW-9 job) nhưng gắn mã lạ `TOOL-KNOW-002` / `SEC-INJECT-001` → theo quy tắc mã lạ tính là **chưa cover**. Xử lý = gắn lại mã (I6), không cần TC mới. Sau khi gắn: Abnormal = NEW-7, Boundary = NEW-8. | `[BLOCKER]` |
| Q2 | `ENV-003` | Cao | GAP — fix nằm ở **job callback** (production tách job callback riêng khỏi broadcast/scenario), 0 TC chạy production. Toàn bộ TC job khai `local`. **RULE-08**. | `[BLOCKER]` |
| Q3 | `COMPAT-LEGACY-001` | Cao | GAP — Kiểm tra bắt buộc cặp **remind cũ ⇄ remind mới (salon / lesson / form)** — 0 TC. Nhánh "bản ghi trước ⇄ sau" đã có ở NEW-7 nhưng gắn mã lạ `TOOL-OLDREC-001`. | `[BLOCKER]` |
| Q4 | `REG-SHARED-001` | Cao | RISK — NEW-3, NEW-10 chỉ Normal và chỉ tin template **văn bản**. Thiếu: event remind (G7), template dạng JSON (G2), nhánh tin friend (G4). | `[MAJOR]` |
| Q5 | `FRIEND-001` | Cao | RISK RULE-01 — chỉ NEW-2 (Normal, friend info kiểu text). Boundary có nội dung ở NEW-8 (gắn `DATA-TEXT-001`), Abnormal gần nhất là NEW-14 (c) giá trị rỗng (tầng job). Chưa ghi lý do thiếu loại case. | `[MAJOR]` |
| Q6 | `MSG-USER-001` | Cao | RISK RULE-01 — chỉ NEW-11 (Normal), tiền đề inactive không dựng được (I8). | `[MAJOR]` |

Đã loại khỏi phạm vi (Trigger khớp chữ nhưng fix không chạm): `INTG-LINE-001` · `INTG-HOOK-001` · `JOB-001` — fix chỉ đổi cách **dựng nội dung trích dẫn**, không đổi cách nhận webhook / gọi LINE API / xử lý lô / retry (nguồn: file 03 mục 2 + Studio `dev_impact`). `DATA-DB-001` (NEW-16 đang gắn) — fix không có UPDATE/DELETE.

---

## 3. TC trùng lặp nội dung

Đã rà 20 TC, **không phát hiện trùng lặp**.

- 4 cặp cùng kịch bản nhưng **khác tầng kiểm chứng** → không tính là trùng: NEW-1 ↔ NEW-9 · NEW-3 ↔ NEW-10 · NEW-5 ↔ NEW-13 · NEW-8 ↔ NEW-15 (TC đầu quan sát màn chat PC, TC sau parse 2 lớp dữ liệu ở job). Cặp nào cũng khác `đối tượng + thao tác` nên không phải DUP.
- Không có `DUP-INFLATE`: không cặp nào làm 1 quan điểm trông như đủ 3 loại case.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 20 TC | **0/20 TC đã chạy** (`last_exec = null`, `runs = 0` ở cả local/dev/staging/prd) → pass 0%. Mọi coverage ở §1/§2 chưa có kết luận. | Chạy bộ TC sau khi có nhánh fix; TC UI end-to-end ưu tiên trước. |
| I2 | `[MAJOR]` | 7 TC `job` + 2 `data` + NEW-17 | **RULE-08 / ENV-003**: 10 TC chỉ khai `env_scope = local`. Không TC nào chạy callback job trên production. | Bổ sung `TC-ENV003-01` (§5). Với NEW-18 → đổi sang chạy trên production (query read-only) để đáp ứng RULE-04. |
| I3 | `[MAJOR]` | Fix shape | **[AP-4]** Commit `fcee76a` / branch `m_202609_replace_json_41108` không truy cập được (Studio `diffAvailable = false`, NEW-12 tự ghi BLOCKER lỗi xác thực git). Không verify được escape bằng Jackson toàn bộ hay tay 3 ký tự, `replace` hay `replaceAll`. | Yêu cầu Dev push branch / gửi link PR. Hỏi Dev: escape đủ mọi ký tự điều khiển JSON chưa, thay chuỗi bằng `replace` hay `replaceAll`? |
| I4 | `[MAJOR]` | Spec | **Không có spec nghiệp vụ trích dẫn**: `spec-features/admin/chat-11/` chỉ có cột `quote_message_content` / `replace_content` ([db-mapping.md:116-121](../../spec-features/admin/chat-11/db/db-mapping.md#L116-L121)). Kho `MT-02` cùng kết luận "spec KHÔNG có mô tả nghiệp vụ nào". 20/20 TC để trống `Trạng thái đánh giá spec` → nguy cơ tự suy diễn expected. | Điền `Spec không ghi` + người đã hỏi cho từng TC; đưa rule vào §6. |
| I5 | `[MAJOR]` | `03-dev-impact.md` | Auto-fill từ Redmine (`2026-09-19 by /new-task`) nhưng checkbox "Tester verify auto-fill chính xác" chưa tick → F/D/T có thể thiếu. Dev ghi mức rủi ro T1–T4 trống. | Tester đọc lại Journal #137146, tick checkbox; hỏi Dev mức rủi ro T1–T4. |
| I6 | `[MAJOR]` | 12 TC mang 9 mã lạ | NEW-1, NEW-4, NEW-5, NEW-6, NEW-7, NEW-9, NEW-12, NEW-13, NEW-14, NEW-17, NEW-18, NEW-19 dùng mã không có trong `checklist-lme.md` (`TOOL-*`, `RULE-TOOL-029`, `SEC-INJECT-001`, `API-CONTRACT-001`, `RULE-04`) → không tính cover (gây Q1, Q3). | Đề xuất gắn lại (Leader chốt): NEW-1, NEW-9 → `FUNC-001` · NEW-7 → `COMPAT-LEGACY-001` · NEW-4, NEW-5, NEW-6, NEW-13, NEW-14 → `DATA-TEXT-001` · NEW-17, NEW-18 → `DATA-MIG-001` hoặc giữ + ghi RULE-04 ở ghi chú · NEW-19 → `DATA-001` · NEW-12 → xem I9. |
| I7 | `[MAJOR]` | NEW-1, NEW-2, NEW-8 | Tiền đề chưa đủ để dựng lại: (1) NEW-1 cần **đổi tên hiển thị trên tài khoản LINE thật** thành `つか咲"き` và xác nhận LME đã cập nhật tên mới (màn 友だち詳細) **trước** khi tin nhắc được gửi — tên thay vào nội dung lấy tại thời điểm gửi; (2) NEW-2, NEW-8 ghi "Chờ (hoặc kích hoạt) hệ thống gửi tin nhắc" mà không nói cách kích hoạt (đặt lịch lúc nào, tin nhắc cài bao lâu trước giờ hẹn). NEW-8 phải lặp 5 vòng đặt lịch → chi phí cao. | Ghi rõ cách đổi tên LINE + điểm xác nhận tên đã đồng bộ; ghi cụ thể cấu hình đặt lịch + thời điểm tin nhắc để 1 vòng chạy < 10 phút. |
| I8 | `[MAJOR]` | NEW-11 | Tiền đề "bạn bè đã chặn/ngừng theo dõi bot" rồi gửi tin trích dẫn — bạn bè đã chặn **không gửi tin được** cho OA, nên nhánh `handleMessageInactiveUser` không chạy được bằng tiền đề này. | Hỏi Dev "inactive user" trong `handleMessageInactiveUser` là trạng thái nào và dựng bằng cách nào, rồi sửa NEW-11. |
| I9 | `[MINOR]` | NEW-12 | Là **đọc code** trên nhánh fix, không phải TC manual tester chạy được; đang bị chặn vì không có nhánh. | Chuyển thành checklist tự kiểm của Dev / bỏ khỏi bộ TC khi đã có diff (I3). |
| I10 | `[MINOR]` | NEW-20 | Ticket ghi 「スマホ版は正常です」 — chưa rõ là **app admin mobile** hay **web giao diện điện thoại**. NEW-20 chỉ đối chiếu app admin. | Hỏi CS/OEM; nếu là web trên điện thoại thì thêm đối chứng trên trình duyệt điện thoại. |

---

## 5. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` — nhóm "Reply / quote message" (TC-CHT-240 → TC-CHT-255) |
| Vùng regression phát hiện từ kho | `TC-CHT-249` (friend trích dẫn tin bot — có template button / quick reply) · `TC-CHT-250` (friend trích dẫn tin chính mình) · `TC-CHT-252` (mọi đường gửi của LME, gồm Event remind cũ và mới) · `TC-CHT-253` (tin trước khi có tính năng trích dẫn) |
| Conflict expected vs kho | Không — kho chỉ kỳ vọng "hiển thị đúng dạng trích dẫn, không lỗi, không màn trắng", khớp hướng fix |
| GAP dùng lại TC kho (không viết mới) | Không — TC kho không có dữ liệu tên/friend info chứa ký tự đặc biệt, nên viết mới và dẫn chiếu ID kho ở `Ghi chú` |
| Xác nhận chống trùng | Đã đối chiếu 20 TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** (không TC nào ở BƯỚC 0 chạy production, remind cũ, event remind, template JSON, tin friend tự trích dẫn, hay ký tự CR/tab/`$`) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENV003-01 | UI | ENV-003 | Reply / quote message | Normal | manual | product | Production — friend tên LINE chứa `"` trả lời trích dẫn tin nhắc đặt lịch salon, chat 1:1 PC hiển thị đầy đủ | - Bản fix #41108 đã deploy lên production (job callback)<br>- Bot test trên production đã bật lịch salon, tin nhắc đặt lịch có chèn tên bạn bè<br>- 1 tài khoản LINE test đã đổi tên hiển thị thành `テスト"太郎`, đã kết bạn bot test; màn 友だち詳細 của bạn bè này hiện đúng tên mới<br>- Ghi lại giờ deploy | 1. Đặt 1 lịch salon cho bạn bè test sao cho tin nhắc được gửi SAU giờ deploy<br>2. Trên LINE, xác nhận nhận được tin nhắc có tên `テスト"太郎`<br>3. Trên LINE, bấm giữ tin nhắc → Trả lời → gửi `了解です`<br>4. Trên PC, mở 1:1チャット của bot test → chọn hội thoại bạn bè test → F5<br>5. Quan sát khung hội thoại và khối trích dẫn phía trên tin `了解です` | Tên LINE: `テスト"太郎` · Tin trả lời: `了解です` | - Khung hội thoại PC hiển thị đủ lịch sử, không vùng trắng<br>- Tin `了解です` có khối trích dẫn, bên trong là nội dung tin nhắc với tên đúng `テスト"太郎` (1 dấu `"`, không có `\` phía trước)<br>- Mở lại hội thoại lần 2 vẫn hiển thị như trên | | Lấp Q2 · RULE-08: fix nằm ở job callback, production tách job callback riêng nên không kết luận từ local/staging · Thiếu Abnormal/Boundary: không có khái niệm biên riêng cho môi trường; chạy lại NEW-5, NEW-8 trên production nếu Leader yêu cầu · manual vì môi trường production + xác nhận tin trên app LINE thật · Đánh giá spec: Spec không ghi · Evidence: screenshot chat PC + screenshot LINE app + giờ deploy |
| TC-FUNC001-01 | UI | FUNC-001 | Reply / quote message | Normal | manual | product | Ca KH đã report (bot つっつん, friend `つか咲"き`) — hội thoại chat 1:1 PC mở được sau khi fix + xử lý dữ liệu cũ | - Leader/Dev đã **chốt và thực hiện** cách xử lý bản ghi trích dẫn hỏng trước fix (§6 #3)<br>- Có quyền xem bot つっつん trên production (tài khoản hỗ trợ của CS)<br>- **Chưa chốt xử lý dữ liệu cũ → TC để trạng thái chờ, không chạy** | 1. Đăng nhập admin production, chọn bot つっつん<br>2. Mở 1:1チャット → chọn hội thoại friend `つか咲"き`<br>3. Mở Console trình duyệt (F12) → F5<br>4. Cuộn tới tin trả lời có trích dẫn tin nhắc đặt lịch salon ngày 2026/08/28 17:16 | Không nhập dữ liệu — hội thoại thật của KH (T12182) | - Khung hội thoại PC hiển thị đủ lịch sử, không vùng trắng<br>- Khối trích dẫn tin nhắc 2026/08/28 hiển thị tên `つか咲"き` đúng nguyên văn<br>- Console không có `SyntaxError ... JSON` | | Lấp G1 · Là TC xác nhận đóng ticket với KH, không phải chỉ với dữ liệu mới · Phụ thuộc quyết định §6 #3 · manual vì môi trường production (bot thật của KH) · Đánh giá spec: Spec không ghi · Evidence: screenshot chat PC + Console |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Reply / quote message | Normal | auto | Tất cả | Trích dẫn tin nhắc đặt lịch **remind cũ và remind mới** của salon và lesson — friend tên chứa `"` | - Bản fix đã deploy<br>- Bot test có cả remind cũ và remind mới cho salon và cho lesson (hỏi Dev cách bật từng loại nếu bot chưa có)<br>- Tài khoản LINE test tên `テスト"太郎`, LME đã hiện đúng tên mới | 1. Lần lượt cho 4 loại tin nhắc ở cột Dữ liệu gửi tới bạn bè test<br>2. Với mỗi tin: trên LINE, trả lời kèm trích dẫn tin nhắc đó<br>3. Trên PC, mở 1:1チャット → hội thoại bạn bè test → F5<br>4. Quan sát khối trích dẫn của từng tin trả lời | salon remind cũ · salon remind mới · lesson remind cũ · lesson remind mới — tên `テスト"太郎` | - Cả 4 tin trả lời đều có khối trích dẫn đúng nội dung tin nhắc, tên `テスト"太郎` đúng nguyên văn<br>- Khung hội thoại không trắng | | Lấp Q3 · RULE-09 · Abnormal = NEW-7 (bản ghi trước fix) sau khi gắn lại mã; Boundary không áp dụng (quan điểm so 2 nhánh, không có khái niệm biên) · dẫn từ TC-CHT-252 · Đánh giá spec: Spec không ghi · Evidence: screenshot từng khối trích dẫn |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Trích dẫn tin nhắc **event booking (cũ và mới)** và tin nhắc **form** — friend tên chứa `"` | - Bản fix đã deploy<br>- Bot test có event booking (イベント予約) với tin nhắc cũ và mới, có form có tin nhắc (nếu bot không có loại nào thì ghi skip loại đó)<br>- Tài khoản LINE test tên `テスト"太郎` | 1. Đăng ký event (và gửi form) để phát sinh từng tin nhắc ở cột Dữ liệu<br>2. Trên LINE, trả lời kèm trích dẫn từng tin nhắc<br>3. Trên PC, mở 1:1チャット → hội thoại bạn bè test → F5<br>4. Quan sát khối trích dẫn của từng tin trả lời | event remind cũ · event remind mới · form remind — tên `テスト"太郎` | - Mỗi tin trả lời có khối trích dẫn đúng nội dung tin nhắc, tên đúng nguyên văn<br>- Khung hội thoại không trắng | | Lấp G7, Q4 · regression — cặp Salon/Lesson/Event của REG-SHARED-001 · dẫn từ TC-CHT-252 · Hỏi Dev: nội dung các tin nhắc này có lưu dạng JSON không · Đánh giá spec: Spec không ghi · Evidence: screenshot từng khối trích dẫn |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Reply / quote message | Abnormal | auto | Tất cả | Trích dẫn tin **template button / quick reply** có chèn tên bạn bè — friend tên chứa `"` | - Bản fix đã deploy<br>- Dev đã xác nhận loại template nào lưu nội dung dạng JSON (G2)<br>- Bot test có template button standard và quick reply text, phần chữ có chèn tên bạn bè<br>- Tài khoản LINE test tên `テスト"太郎` | 1. Từ 1:1チャット, gửi lần lượt template button standard và quick reply cho bạn bè test<br>2. Trên LINE, trả lời kèm trích dẫn từng tin<br>3. Trên PC, F5 hội thoại bạn bè test<br>4. Quan sát khối trích dẫn | template button standard (1 panel, có chèn tên) · quick reply text (1 nút, có chèn tên) — tên `テスト"太郎` | - Khối trích dẫn hiển thị đúng nội dung tin gốc với tên `テスト"太郎`, không có `\` thừa<br>- Khung hội thoại không trắng | | Lấp G2, Q4 · regression — nơi gọi thứ 2 `buildQuoteMessageContent` với content JSON (nhánh `isJsonContent = true` ngoài tin nhắc) · dẫn từ TC-CHT-249 · Đánh giá spec: Spec không ghi · Evidence: screenshot khối trích dẫn |
| TC-REGSHARED001-03 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Friend trích dẫn **tin chính mình đã gửi** có dấu `"` và nội dung dạng JSON — hiển thị nguyên văn như trước fix | - Bản fix đã deploy<br>- Bạn bè test bất kỳ đã kết bạn bot test | 1. Trên LINE, bạn bè gửi lần lượt 2 tin ở cột Dữ liệu<br>2. Bạn bè trả lời kèm trích dẫn từng tin của chính mình<br>3. Trên PC, mở 1:1チャット → hội thoại bạn bè test → F5<br>4. So nội dung khối trích dẫn với bong bóng tin gốc | Tin 1: `山田"太郎"です` · Tin 2: `{"memo":"テスト"}` | - Khối trích dẫn hiện đúng nguyên văn 2 tin, giống hệt bong bóng tin gốc, không thêm `\`<br>- Khung hội thoại không trắng | | Lấp G4, Q4 · regression — nhánh tin friend của `checkFindQuoteMessage` · dẫn từ TC-CHT-250 · Đánh giá spec: Spec không ghi · Evidence: screenshot tin gốc + khối trích dẫn |
| TC-DATATEXT001-01 | UI | DATA-TEXT-001 | Reply / quote message | Boundary | auto | Tất cả | Giá trị friend info chứa **ký tự Dev chưa kê** (CRLF, tab, `$`) — trích dẫn tin nhắc vẫn hiển thị và tin của friend không bị mất | - Bản fix đã deploy<br>- Bot test có tin nhắc lesson dùng mã friend info (text)<br>- Bạn bè test bất kỳ | 1. Ở tab 友だち情報 của 1:1チャット, nhập giá trị friend info theo bộ 1 (xuống dòng bằng Enter trong ô nhập) → lưu<br>2. Phát sinh tin nhắc lesson tới bạn bè → trên LINE trả lời kèm trích dẫn<br>3. Trên PC, F5 hội thoại → quan sát khối trích dẫn + tin trả lời + Console<br>4. Lặp lại cho bộ 2, bộ 3 | Bộ 1: `山田` + Enter + `太郎` (nhập trên web, có thể lưu dạng CRLF) · Bộ 2: `山田` + tab + `太郎` (dán từ Excel) · Bộ 3: `価格$100\円` | - Cả 3 bộ: khung hội thoại không trắng, Console không có `SyntaxError`<br>- Khối trích dẫn hiện đúng giá trị (bộ 1 thành 2 dòng; bộ 2 giữ khoảng tab; bộ 3 đúng `$100\円`)<br>- Tin trả lời của bạn bè luôn hiện trong hội thoại — không mất tin dù trích dẫn lỗi | | Lấp G6 · Trigger ngoài 3 ký tự Dev kê (`"` `\` `\n`) để kiểm fallback của escape · Hỏi Dev (I3): `replace` hay `replaceAll` · Đánh giá spec: Spec không ghi · Evidence: screenshot khối trích dẫn + Console |

Không đề xuất TC mới cho:
- **G3** — sửa NEW-18 sang chạy trên production (query read-only) là đủ đáp ứng RULE-04 (I2).
- **G5, Q6** — cần Dev định nghĩa "inactive user" trước (I8), sau đó sửa tiền đề NEW-11. Thiếu Boundary: vòng đời friend không có khái niệm biên ở fix này.
- **G8** — TC không thay được việc thêm `try/catch` ở web, đưa §6 #3.
- **G9** — orphan, chỉ quyết giữ / bỏ.
- **Q1, Q5** — nội dung đã có (NEW-1, NEW-9, NEW-7, NEW-8, NEW-14), xử lý bằng gắn lại mã quan điểm (I6) + ghi lý do thiếu loại case.

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/feature-spec.md` — chưa có mục trích dẫn | Bổ sung nghiệp vụ trích dẫn: nội dung trích dẫn lưu ở đâu, tên / friend info thay vào lấy tại thời điểm nào (lúc gửi tin gốc hay lúc trích dẫn), ký tự đặc biệt phải hiển thị nguyên văn | Kho `MT-02` (đang chờ quyết định) + I4 | PM / Leader |
| 2 | Quy tắc nhận diện nội dung JSON của `isJsonContent` | Chốt: tin văn bản thường có nội dung tình cờ đúng cú pháp JSON (NEW-6) có bị coi là JSON và escape không; danh sách loại content JSON đi qua `applyReplaceContent` (G2) | NEW-6 ghi "CẦN DEV XÁC NHẬN" | Dev |
| 3 | Xử lý dữ liệu cũ + hardening web | (a) Có phục hồi bản ghi `quote_message_content` hỏng trước fix không (NEW-17 đã chỉ ra cách: xóa rỗng cột để web tự dựng lại) — nếu không, hội thoại KH T12182 vẫn trắng sau deploy (G1). (b) Có thêm `try/catch` cho `JSON.parse` ở `showMessageQuotedSalonLesson` để 1 bản ghi hỏng không làm trắng cả hội thoại không (G8) | File 03 mục 4.2 "không tự sửa" vs mục tiêu ticket KH | Leader + Dev |
