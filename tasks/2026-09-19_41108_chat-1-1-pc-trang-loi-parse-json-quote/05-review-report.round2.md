# 05 — Review Report (round 2 — trọng tâm: logic trích dẫn theo từng loại tin nhắn)

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.
> Round 1 (`05-review-report.md`) đã xử lý trục remind cũ/mới · production · ca KH · ký tự biên. Round 2 rà lại bộ 27 TC hiện tại theo **từng loại tin nhắn được trích dẫn** đi qua `applyReplaceContent` / `isJsonContent`.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #314 (round 1, refresh 2026-09-19) |
| Tổng số TC review | 27 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `3/8 vùng đủ TC` (T2 text `{name}` — NEW-5, NEW-13 · T3 tin friend — NEW-26 · F1 escape ký tự biên — NEW-15, NEW-27) · `2 GAP · 5 RISK`.

`Input thiếu: không có diff` — Studio `spec_delta.diffAvailable = false` (không tìm thấy ref `m_202609_replace_json_41108`) → chiều (b) suy từ Studio `dev_impact` + file 03 mục 1/2/3 + spec `chat-management` / `salon-booking` / `lesson-booking`.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | **Tin đặt lịch salon gửi theo trạng thái booking**: 予約完了時 · 予約リクエスト受付時 · 予約リクエスト承認時 · 予約リクエスト否認時 · キャンセル完了時 · キャンセルリクエスト受付/承認/否認時 | `dev-impact` (BUG) | không có | GAP — ticket ghi rõ tin KH trích dẫn là **「サロン予約受付時メッセージ」**, nhưng **cả 27 TC** chỉ dùng **tin nhắc (remind)**. Tin theo trạng thái booking do web gửi qua `createMessageV2` với `msg_kind = KIND_MESSAGE_ACTION_FROM_BOOKING` (type 20 salon / 21 lesson — [chat-management logic-spec:256-258](../../spec-features/admin/chat-management/web/logic-spec.md#L256-L258)), đúng loại nội dung `RemindBookingContent` đã vỡ JSON ([error-message job-spec:326](../../spec-features/admin/error-message/job/job-spec.md#L326)). Chưa TC nào tái hiện đúng loại tin của KH. NEW-1 ghi "tái hiện đúng hiện tượng gốc" nhưng dùng tin nhắc. | `[BLOCKER]` |
| G2 | Tin đặt lịch **lesson** theo trạng thái booking + tin admin gửi từ màn chi tiết booking (`sendMessageAction`) | `diff code` | không có | GAP — [lesson-booking job-spec:578](../../spec-features/admin/lesson-booking/job/job-spec.md#L578): admin gửi tin theo mốc booking cũng ghi `KIND_MESSAGE_ACTION_FROM_BOOKING` / `TYPE_MESSAGE_ACTION_FROM_BOOKING_LESSON` → cùng hàm hiển thị `showMessageQuotedSalonLesson`. NEW-2, NEW-23 chỉ có lesson remind. | `[MAJOR]` |
| G3 | Giá trị thay thế **không phải tên LINE**: token đặt lịch do admin nhập (tên course · tên cửa hàng · tên staff · URL hủy) | `diff code` | không có | RISK — tin đặt lịch chèn được 5 token `[SALON_CALENDAR_*]` (kho `TC-SLN-295`), giá trị là **tên course / cửa hàng do admin tự đặt**, có thể chứa `"` `\`. Mọi TC chỉ đặt ký tự đặc biệt vào tên LINE hoặc friend info. Chưa rõ các token này có đi qua `replace_content` hay đã thay sẵn lúc gửi → hỏi Dev (§6 #4). Dù đi đường nào, hiển thị trích dẫn vẫn phải đúng. | `[MAJOR]` |
| G4 | Template dạng JSON **nhiều panel / có ảnh** + **template pack nhiều tin** (`buildQuoteMessageContent`) | `diff code` | NEW-25 (1 panel standard + quick reply text 1 nút) | RISK — kho `TC-CHT-249` liệt kê template button standard / color / ảnh × 1 panel / nhiều panel × có ảnh / không ảnh, quick reply text / ảnh × 1 nút / nhiều nút. NEW-25 chỉ có 2/12 biến thể. Template pack: `replace_content` áp cho **cả pack**, friend trích dẫn bong bóng thứ 2–3 thì `buildQuoteMessageContent` phải lấy đúng bong bóng, và phần thay thế cũng chạy trên nội dung JSON của ảnh/nút → 0 TC. | `[MAJOR]` |
| G5 | Tin **media / sticker / PDF / vị trí / audio** do bot gửi — nội dung là JSON nên nay rơi vào nhánh `isJsonContent = true` | `diff code` | không có | RISK — hành vi đổi so với trước: trước fix mọi nội dung chèn thô, sau fix nội dung JSON đi nhánh escape. Chưa có diff nên không biết Dev chỉ escape giá trị hay parse rồi ghi lại cả JSON (có thể đổi `\/` trong URL, đổi thứ tự khóa, đổi ký tự Nhật thành `\uXXXX`). Friend trích dẫn được cả audio và vị trí trên LINE (kho `TC-CHT-249`). 0 TC verify hiển thị trích dẫn của các loại này không đổi. | `[MAJOR]` |
| G6 | Đường gửi qua job: 一斉配信 · ステップ配信 · 自動応答 có `{name}` / friend info | `dev-impact` (T2) | NEW-3, NEW-10 (không ghi tin template gửi từ đâu) | RISK — `replace_content` được ghi ở từng đường gửi (kho `TC-CHT-252` gộp ~50 đường). NEW-3 / NEW-10 không ghi đường gửi → chỉ kết luận được cho 1 đường. | `[MINOR]` |
| G7 | Escape **2 lần** — giá trị trông giống chuỗi đã escape: `\"` · `\\` · `\u0022` · chữ `\n` | `diff code` | NEW-5 (`"` và `\` riêng rẽ), NEW-15 | RISK — lỗi hay gặp nhất của sửa escape bằng tay: escape lặp (hiện `\\"`) hoặc bỏ escape nhầm (`\u0022` hiện thành `"`). Chưa TC nào đặt các chuỗi này **liền nhau**. | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `8 quan điểm Trigger khớp task · 4 chưa cover đủ` (đã đủ sau round 1: `COMPAT-LEGACY-001` — NEW-23 pass + NEW-7 · `DATA-TEXT-001` — NEW-8, NEW-27 · `SYNC-APP-001` — NEW-20 · `FRIEND-001` phần tên LINE).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | GAP — luồng chính của **đúng loại tin KH** (予約受付時メッセージ) chưa có TC (G1). NEW-22 (ca KH thật) chưa chạy và phụ thuộc quyết định xử lý dữ liệu cũ. NEW-1 / NEW-9 chỉ tin nhắc, gắn mã lạ. | `[BLOCKER]` |
| Q2 | `REG-SHARED-001` | Cao | RISK — cùng dạng nội dung JSON dùng chung cho **salon / lesson / event / form / template**: đã có remind (NEW-23), template 1 panel (NEW-25), tin friend (NEW-26); **thiếu** tin trạng thái booking (G1, G2), template nhiều panel + pack (G4), media (G5). NEW-24 (event/form remind) chưa chạy. | `[MAJOR]` |
| Q3 | `DATA-TEXT-001` (nâng Cao — text được gửi LINE) | Cao | RISK — Boundary mới có cho **tên LINE / friend info**; thiếu nguồn dữ liệu thứ 3 là **tên course / cửa hàng do admin nhập** (G3) và chuỗi dễ escape 2 lần (G7). | `[MAJOR]` |
| Q4 | `MSG-USER-001` | Cao | RISK RULE-01 (giữ nguyên từ round 1) — chỉ NEW-11 (job, Normal); tiền đề inactive không dựng được. | `[MAJOR]` |

Đã loại khỏi phạm vi:
- **Admin trích dẫn tin từ chat 1:1** (bot trả lời kèm trích dẫn — kho `TC-CHT-245`, `TC-CHT-254`): nội dung trích dẫn dựng ở web lúc gửi, không đi qua callback job `HandlePostbackTask` (Studio `dev_impact`: fix chỉ ở job, web không đổi code).
- **Image map**: không trích dẫn được (kho `TC-CHT-241`).
- **Action text của event booking (予約受付時アクション)**: gửi qua Action Settings, không phải `ACTION_FROM_BOOKING`. Nếu Dev xác nhận có dùng `RemindBookingContent` thì thêm vào TC-REGSHARED001-05.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Trích dẫn tin nhắc salon, friend tên chứa `"`, chat PC | NEW-23 (pass, gồm salon remind mới) | NEW-1 → **gộp** vào NEW-23 (thêm bước mở Console + kỳ vọng "Console không có `SyntaxError`") | `DUP-SUBSET` | `FUNC-001`/`COMPAT-LEGACY-001` × Normal × trích dẫn tin nhắc salon mới trên LINE rồi xem chat PC × friend tên chứa `"` sau khi áp fix | `[MINOR]` |

- Gate xóa: NEW-1 mang mã lạ `TOOL-KNOW-002` nên đang không tính cover; gộp không làm mất cover. Nếu Leader muốn giữ NEW-1 làm TC xác nhận ca KH thì **đổi dữ liệu sang 予約受付時メッセージ** (G1) thay vì xóa. Khi đó NEW-1 và TC-FUNC001-02 ở §5 trùng nhau → chỉ giữ 1.
- Đã rà 7 TC mới (NEW-21 → NEW-27) với 20 TC cũ: NEW-27 ↔ NEW-8 khác bộ ký tự · NEW-26 ↔ NEW-6 khác người gửi tin gốc (friend vs bot) · NEW-21 ↔ NEW-23 khác môi trường → không trùng.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ | **15/27 pass (55%)** — 9 `skip` (gồm TC lõi NEW-1, NEW-2, NEW-8) + 3 chưa chạy (NEW-21, NEW-22, NEW-24). Toàn bộ kết quả ở `local`. | Chạy lại NEW-2, NEW-8 (friend info + ký tự biên trên UI), NEW-24; NEW-21 chạy sau deploy production. |
| I2 | `[MAJOR]` | NEW-21 | **RULE-08 / ENV-003**: 0 TC chạy production (`envAuto.prd.runs = 0`). Fix ở job callback. | Chạy NEW-21 sau khi deploy production. |
| I3 | `[MAJOR]` | Fix shape | **[AP-4]** vẫn chưa có diff → không phân biệt được Dev chỉ escape giá trị hay parse rồi ghi lại cả JSON (quyết định G5 có rủi ro thật hay không). | Yêu cầu Dev push branch / gửi link PR; hỏi rõ cách escape (§6 #2). |
| I4 | `[MAJOR]` | Spec | `spec-features/admin/chat-11/` chưa có nghiệp vụ trích dẫn (chỉ cột DB ở [db-mapping.md:119-121](../../spec-features/admin/chat-11/db/db-mapping.md#L119-L121)). 27/27 TC trống `Trạng thái đánh giá spec`. | Giữ nguyên từ round 1 — điền `Spec không ghi` + người đã hỏi. |
| I5 | `[MAJOR]` | `03-dev-impact.md` | Checkbox "Tester verify auto-fill chính xác" vẫn chưa tick; mục 4.3 T1 ghi "tin nhắc đặt lịch" trong khi ticket là **予約受付時メッセージ** → nhiều khả năng Dev dùng "nhắc" cho cả nhóm tin `ACTION_FROM_BOOKING`. | Hỏi Dev để chốt T1 gồm những loại tin nào, sửa 4.3 rồi tick checkbox. |
| I6 | `[MAJOR]` | 12 TC mang 9 mã lạ | Chưa gắn lại mã (`TOOL-*`, `RULE-TOOL-029`, `SEC-INJECT-001`, `API-CONTRACT-001`, `RULE-04`) → không tính cover. | Giữ đề xuất gắn lại của round 1 (I6). |
| I7 | `[MAJOR]` | NEW-3, NEW-10 | Tiền đề "template văn bản có chứa mã tên" không ghi **đường gửi** (chat 1:1 / 一斉配信 / ステップ配信 / 自動応答) → người khác chạy lại ra kết quả khác nhau. | Ghi rõ đường gửi; các đường còn lại lấp bằng TC-REGSHARED001-08. |
| I8 | `[MAJOR]` | NEW-11 | Giữ nguyên từ round 1 — tiền đề "bạn bè đã chặn bot rồi gửi tin" không chạy được. | Hỏi Dev định nghĩa inactive user. |

---

## 5. TCs đề xuất bổ sung (8)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md` (TC-CHT-240 → 255) · `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (TC-SLN-295, 300, 447) · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (TC-LSN-327, MT-22) |
| Vùng regression phát hiện từ kho | 8 mẫu tin salon (TC-SLN-295 / 300) và 4 mẫu tin lesson (TC-LSN-327) chèn được `{name}` + token đặt lịch · 12 biến thể template (TC-CHT-249) · ~50 đường gửi (TC-CHT-252) |
| Conflict expected vs kho | Không. Lưu ý kho `MT-22` (lesson): 否認時 đặt lịch và 否認時 hủy **dùng chung nội dung** → TC-REGSHARED001-05 chỉ kỳ vọng hiển thị trích dẫn đúng **nội dung tin đã nhận**, không kỳ vọng nội dung nào cụ thể |
| GAP dùng lại TC kho | Không — TC kho không có dữ liệu chứa `"` / `\`, nên viết mới và dẫn chiếu ID kho |
| Xác nhận chống trùng | Đã đối chiếu 27 TC ở BƯỚC 0 + 3 file kho. **Không TC đề xuất nào trùng**: không TC nào ở BƯỚC 0 dùng tin trạng thái booking, token đặt lịch, template nhiều panel/pack, media, đường gửi job, hay chuỗi escape liền nhau |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC001-02 | UI | FUNC-001 | Reply / quote message | Normal | auto | Tất cả | Salon — friend tên LINE chứa `"` trích dẫn **tin gửi lúc đặt lịch** (予約完了時 / 予約リクエスト受付時 / 承認時 / 否認時), chat 1:1 PC hiển thị đầy đủ | - Bản fix đã deploy<br>- Bot test có 2 lịch salon: lịch A 承認方法 = 自動 (全承認), lịch B = リクエスト制<br>- Ở tab 予約設定 của cả 2 lịch, 4 mẫu tin đặt lịch đều bấm 例文を挿入する và chèn thêm token LINE名 ở đầu<br>- Tài khoản LINE test đổi tên thành `テスト"太郎`, màn 友だち詳細 đã hiện tên mới | 1. Friend đặt lịch A → nhận tin 予約完了時<br>2. Friend đặt lịch B → nhận tin 予約リクエスト受付時<br>3. Admin duyệt booking B → friend nhận 承認時<br>4. Friend đặt lịch B lần 2, admin từ chối → friend nhận 否認時<br>5. Trên LINE, friend trả lời kèm trích dẫn **từng** tin ở bước 1–4<br>6. Trên PC, mở 1:1チャット → hội thoại friend → mở Console (F12) → F5<br>7. Quan sát khung hội thoại, 4 khối trích dẫn và Console | Tên LINE: `テスト"太郎` · Tin trả lời: `OK1` … `OK4` | - Khung hội thoại PC hiển thị đủ lịch sử, không vùng trắng<br>- Cả 4 tin `OK1`–`OK4` có khối trích dẫn đúng nội dung tin đặt lịch tương ứng, tên hiện `テスト"太郎` (1 dấu `"`, không có `\`)<br>- Console không có `SyntaxError` | | Lấp G1, Q1 · Đúng loại tin KH báo lỗi (サロン予約受付時メッセージ) — tin gửi từ web qua `ACTION_FROM_BOOKING`, không phải tin nhắc từ job · Abnormal = NEW-7, Boundary = TC-DATATEXT001-02 · dẫn từ TC-SLN-295 · Đánh giá spec: Spec không ghi · Evidence: screenshot chat PC 4 khối trích dẫn + Console |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Salon — friend tên chứa `"` trích dẫn **tin gửi lúc hủy lịch** (キャンセル完了時 / キャンセルリクエスト受付時 / 承認時 / 否認時) | - Bản fix đã deploy<br>- Bot test có lịch salon A: cài hủy = 自動; lịch B: cài hủy = リクエスト制<br>- 4 mẫu tin hủy đã bấm 例文を挿入する và chèn token LINE名<br>- Friend `テスト"太郎` đã có 1 booking ở A và 2 booking ở B | 1. Friend hủy booking ở A → nhận キャンセル完了時<br>2. Friend gửi yêu cầu hủy booking B-1 → nhận キャンセルリクエスト受付時; admin duyệt → nhận 承認時<br>3. Friend gửi yêu cầu hủy booking B-2, admin từ chối → nhận 否認時<br>4. Trên LINE, trả lời kèm trích dẫn từng tin<br>5. Trên PC, F5 hội thoại friend → quan sát khối trích dẫn | Tên LINE: `テスト"太郎` | - Mỗi tin trả lời có khối trích dẫn đúng nội dung tin hủy tương ứng, tên đúng nguyên văn<br>- Khung hội thoại không trắng | | Lấp G1, Q2 · regression — cùng kênh `ACTION_FROM_BOOKING` với tin đặt lịch · dẫn từ TC-SLN-300 · Đánh giá spec: Spec không ghi · Evidence: screenshot khối trích dẫn |
| TC-REGSHARED001-05 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Lesson — friend tên chứa `"` trích dẫn tin đặt lịch / hủy lịch và **tin admin gửi từ màn chi tiết booking** | - Bản fix đã deploy<br>- Bot test có lịch lesson ở 全体設定: 4 mẫu tin đặt lịch + tin hủy đã bấm 例文を挿入する và chèn token LINE名<br>- Friend `テスト"太郎` đã kết bạn bot | 1. Friend đặt 1 lesson → nhận 予約完了時 (hoặc 予約リクエスト受付時 nếu リクエスト制)<br>2. Admin mở chi tiết booking đó → gửi tin cho friend có chèn tên (`{name}さん、当日よろしくお願いします`)<br>3. Friend hủy lesson → nhận tin hủy<br>4. Trên LINE, trả lời kèm trích dẫn cả 3 tin<br>5. Trên PC, F5 hội thoại friend → quan sát | Tên LINE: `テスト"太郎` | - 3 khối trích dẫn hiện đúng nội dung tin gốc, tên `テスト"太郎` đúng nguyên văn<br>- Khung hội thoại không trắng | | Lấp G2, Q2 · regression — lesson dùng `TYPE_MESSAGE_ACTION_FROM_BOOKING_LESSON` (lesson-booking job-spec:578) · dẫn từ TC-LSN-327 · Đánh giá spec: Spec không ghi · Evidence: screenshot khối trích dẫn |
| TC-DATATEXT001-02 | UI | DATA-TEXT-001 | Reply / quote message | Boundary | auto | Tất cả | Tên **course / cửa hàng** do admin nhập chứa `"` và `\` — friend trích dẫn tin đặt lịch salon hiển thị đúng | - Bản fix đã deploy<br>- Lịch salon test: tên cửa hàng `サロン"東京"店`, course `カット\カラー`<br>- Mẫu 予約完了時 chèn 3 token: 店舗名 · コース名 · 予約日時<br>- Friend tên thường `田中太郎` (để tách nguồn ký tự đặc biệt khỏi tên LINE) | 1. Friend đặt course `カット\カラー` → nhận 予約完了時<br>2. Trên LINE, xác nhận tin hiện đúng `サロン"東京"店` và `カット\カラー`<br>3. Friend trả lời kèm trích dẫn tin đó<br>4. Trên PC, mở Console → F5 hội thoại friend → quan sát | Tên cửa hàng: `サロン"東京"店` · Tên course: `カット\カラー` | - Khung hội thoại không trắng, Console không có `SyntaxError`<br>- Khối trích dẫn hiện `サロン"東京"店` (2 dấu `"`) và `カット\カラー` (1 dấu `\`), giống hệt tin friend thấy trên LINE | | Lấp G3, Q3 · Hỏi Dev (§6 #4): token đặt lịch có lưu vào `replace_content` không; dù có hay không, hiển thị phải đúng · dẫn từ TC-SLN-295 · Đánh giá spec: Spec không ghi · Evidence: screenshot LINE + khối trích dẫn + Console |
| TC-DATATEXT001-03 | UI | DATA-TEXT-001 | Reply / quote message | Boundary | auto | Tất cả | Tên LINE chứa chuỗi **trông như đã escape** (`\"` · `\\` · `\u0022` · chữ `\n`) — trích dẫn hiện nguyên văn, không escape 2 lần | - Bản fix đã deploy<br>- Bot test có tin nhắc salon và 1 template văn bản `{name}さん、こんにちは`, đều chèn tên friend<br>- 1 tài khoản LINE test | 1. Đổi tên LINE thành bộ 1, đợi 友だち詳細 hiện tên mới<br>2. Gửi template văn bản cho friend từ 1:1チャット; phát sinh 1 tin nhắc salon<br>3. Trên LINE, trả lời kèm trích dẫn cả 2 tin<br>4. Trên PC, F5 hội thoại → quan sát 2 khối trích dẫn + Console<br>5. Lặp lại với bộ 2, bộ 3 | Bộ 1: `a\"b` · Bộ 2: `a\\"b` · Bộ 3: `a\u0022b\nc` (gõ đúng các ký tự `\` `u` `0` `0` `2` `2` và `\` `n`, không phải ký tự đặc biệt) | - Cả 3 bộ: khung hội thoại không trắng, Console không có `SyntaxError`<br>- Khối trích dẫn của **cả tin nhắc (JSON) và tin văn bản** hiện đúng nguyên văn tên đã đặt: bộ 1 `a\"b`, bộ 2 `a\\"b`, bộ 3 `a\u0022b\nc` (không thành `"`, không xuống dòng)<br>- 2 khối trích dẫn hiện giống nhau | | Lấp G7, Q3 · Kiểm cả nhánh JSON và nhánh text của `isJsonContent` · Tên LINE có thể bị giới hạn ký tự — nếu LINE không cho đặt thì dùng friend info kiểu text với cùng bộ dữ liệu · Đánh giá spec: Spec không ghi · Evidence: screenshot 2 khối trích dẫn mỗi bộ |
| TC-REGSHARED001-06 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Trích dẫn template **nhiều panel / có ảnh** và quick reply **ảnh / nhiều nút** có chèn tên — friend tên chứa `"` | - Bản fix đã deploy<br>- Bot test có 5 template ở cột Dữ liệu, tiêu đề / nội dung / nhãn nút đều chèn `{name}`<br>- Friend `テスト"太郎` | 1. Từ 1:1チャット, gửi lần lượt 5 template cho friend<br>2. Trên LINE, trả lời kèm trích dẫn từng tin<br>3. Trên PC, F5 hội thoại friend → quan sát 5 khối trích dẫn | template button standard 3 panel có ảnh · template button color 2 panel · template button ảnh 3 panel · quick reply text 3 nút · quick reply ảnh 2 nút | - 5 khối trích dẫn hiển thị đúng nội dung tin gốc, tên `テスト"太郎` không có `\` thừa<br>- Ảnh panel vẫn hiện (URL ảnh không bị hỏng)<br>- Khung hội thoại không trắng | | Lấp G4, Q2 · regression — bổ sung các biến thể NEW-25 chưa có · dẫn từ TC-CHT-249 · Đánh giá spec: Spec không ghi · Evidence: screenshot 5 khối trích dẫn |
| TC-REGSHARED001-07 | UI | REG-SHARED-001 | Reply / quote message | Abnormal | auto | Tất cả | **Template pack nhiều tin** (text có tên + ảnh + template button) — friend trích dẫn bong bóng thứ 2 và thứ 3, trích dẫn lấy đúng bong bóng | - Bản fix đã deploy<br>- Bot test có 1 template pack 3 tin: (1) text `{name}さん、ご案内です` (2) ảnh (3) template button 1 panel, nhãn chèn `{name}`<br>- Friend `テスト"太郎` | 1. Từ 1:1チャット, gửi template pack cho friend<br>2. Trên LINE, trả lời kèm trích dẫn lần lượt bong bóng 1, 2, 3<br>3. Trên PC, F5 hội thoại friend → quan sát 3 khối trích dẫn | Template pack 3 tin · tên `テスト"太郎` | - Khối trích dẫn thứ 1 hiện text với tên đúng; thứ 2 hiện ảnh + chữ 画像; thứ 3 hiện template button với nhãn chứa tên đúng<br>- Mỗi khối là **đúng bong bóng đã trích dẫn**, không lấy nhầm bong bóng khác trong pack<br>- Khung hội thoại không trắng | | Lấp G4 · `buildQuoteMessageContent` dựng trích dẫn cho tin template capture; phần thay tên chạy trên nội dung của cả pack, gồm nội dung JSON của ảnh · Đánh giá spec: Spec không ghi · Evidence: screenshot 3 khối trích dẫn |
| TC-REGSHARED001-08 | UI | REG-SHARED-001 | Reply / quote message | Normal | auto | Tất cả | Trích dẫn tin **media / sticker / PDF / vị trí / audio** và tin text `{name}` gửi qua **一斉配信 · ステップ配信 · 自動応答** — hiển thị như trước fix | - Bản fix đã deploy<br>- Bot test đã gửi cho friend `テスト"太郎`: ảnh · video · audio · PDF · sticker · vị trí (từ 1:1チャット)<br>- Có 1 broadcast, 1 scenario step, 1 auto-reply (keyword `test`), mỗi cái là text `{name}さん、お知らせです` | 1. Gửi broadcast cho friend; chạy scenario tới step đó; friend gửi `test` để nhận auto-reply<br>2. Trên LINE, friend trả lời kèm trích dẫn từng tin: 6 tin media + 3 tin text<br>3. Trên PC, F5 hội thoại friend → quan sát 9 khối trích dẫn<br>4. So với 1 khối trích dẫn tương tự tạo **trước** khi deploy (nếu có) | 6 loại media + 3 đường gửi text · tên `テスト"太郎` | - Media: khối trích dẫn hiện đúng dạng như kho TC-CHT-242 (ảnh + 画像, video + 動画, sticker + スタンプ, PDF tên file, vị trí địa chỉ); ảnh / video / sticker hiện được, không mất ảnh thu nhỏ<br>- 3 tin text: tên `テスト"太郎` đúng nguyên văn<br>- Khung hội thoại không trắng | | Lấp G5, G6, Q2 · regression — nội dung media là JSON nên nay đi nhánh escape; rủi ro phụ thuộc cách Dev ghi lại JSON (I3) · dẫn từ TC-CHT-249, TC-CHT-252 · Đánh giá spec: Spec không ghi · Evidence: screenshot 9 khối trích dẫn |

Không đề xuất TC mới cho:
- **Q4 (`MSG-USER-001`)** — chờ Dev định nghĩa inactive user rồi sửa NEW-11 (I8).
- **NEW-24 (event / form remind)** — TC đã có, chỉ cần chạy (I1).

---

## 6. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/feature-spec.md` — chưa có mục trích dẫn | Giữ nguyên từ round 1 #1 — bổ sung nghiệp vụ trích dẫn + bảng **loại tin nào dựng trích dẫn ở job, loại nào ở web** | I4 | PM / Leader |
| 2 | Cách escape của `applyReplaceContent` | Dev chốt: chỉ escape giá trị thay thế rồi chèn chuỗi, hay parse → sửa → ghi lại cả JSON? Nếu ghi lại cả JSON thì nội dung media / template có đổi định dạng không (G5) | Không có diff (I3) | Dev |
| 3 | Xử lý dữ liệu cũ + `try/catch` ở `showMessageQuotedSalonLesson` | Giữ nguyên từ round 1 #3 | File 03 mục 4.2 | Leader + Dev |
| 4 | Phạm vi T1 "tin nhắc đặt lịch" | Dev chốt: (a) T1 gồm **mọi tin `KIND_MESSAGE_ACTION_FROM_BOOKING`** (予約完了時 / リクエスト受付・承認・否認時 / キャンセル系 / admin gửi từ chi tiết booking) hay chỉ tin nhắc; (b) token đặt lịch `[SALON_CALENDAR_*]` / tên course lesson có lưu vào `replace_content` không (G3) | Ticket: 「サロン予約受付時メッセージ」 vs file 03 4.3: "tin nhắc đặt lịch" | Dev |
