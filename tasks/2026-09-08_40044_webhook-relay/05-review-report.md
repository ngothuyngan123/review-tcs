# 05 — Review Report

> Draft cho Leader verify. Ticket #40044 「Webhook転送」 — Feature (tính năng mới), không phải bug fix.
> Vòng này đối chiếu bộ TC với **tài liệu hợp đồng outbound bản 1.0.0 (16/09/2026 18:30 JST, WSSJ)** do human cung cấp trực tiếp trong chat — nguồn spec hợp lệ theo BƯỚC 1.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `(1) MCP LME TEST STUDIO — task #269 (ticket 40044, round 1, branch merge-40041-40044), fetch 2026-09-22` |
| Tổng số TC review | `214` |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | **KHÔNG ĐÁNH GIÁ ĐƯỢC — Input thiếu**: mục 4.1 `F*` / 4.2 `D*` / 4.3 `T*` đều là `<Input thiếu — Dev chưa cung cấp>`. ⚠️ Redmine #40044 **nay ĐÃ CÓ** note đánh giá ảnh hưởng đầy đủ (thấy qua Studio `spec_delta.redmine.lastNotes`) nhưng file 03 chưa đồng bộ → xem `I4` §5. |
| **(b) diff code** — suy từ diff thật (Studio `dev_impact` + `spec_delta`) | `8/22 điểm đủ TC` — **CHƯA ĐỦ**. `diffAvailable=true`, `diffStat` 62 file / +7104 dòng. |

**Kết luận**: `8/22 vùng ảnh hưởng đủ TC · 9 GAP · 7 RISK`.

> ⚠️ **Cảnh báo nền cho toàn bộ §1**: Studio `dev_impact` ghi rõ bản JOB đã sync (`f4e53fa9`) **CHƯA có** 2 commit fix `#41038` (`29dc078`) và `#41040` (`9fadcf4`). Mọi TC chạm 2 vùng này đang chạy trên **code cũ** → kết quả `pass` không kết luận được. Re-sync rồi chạy lại trước khi chốt round.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | **`#41038` — forward TOÀN BỘ status trừ `0/1/100/101`** (trước chỉ quét `2/102`, nên `ERROR 3` · `UNKNOWN_TYPE 9` · `IGNORE_GROUP_MESSAGE 10` · `IGNORE_DUPLICATE_WEBHOOK 11` · `MEDIA_ERROR 33` không bao giờ được chuyển tiếp) | `diff code` | `NEW-241` (0/1/100/101 **không** forward) · `NEW-242` (2/102 vẫn forward) | `GAP` — 2 TC chỉ phủ **2 rìa**, **0 TC cho chính nhánh được fix**: 5 status lỗi/bỏ qua NAY phải được forward. Đây là toàn bộ giá trị của commit. Khớp doc §1 「không phụ thuộc LME có xử lý được hay không」 | `[BLOCKER]` |
| G2 | **`#41040` — retry 3 lần CÁCH NHAU 1 PHÚT** qua bảng `webhook_relay_queue` **mới** + `status_sync=5 (RETRY)` + `HandleRetryWebhookRelay*` | `diff code` | `NEW-137` (v2, sửa 2026-09-16) — **skip, chưa chạy lần nào** | `GAP` — 0 TC chốt **nhịp 1 phút** (doc §2/§6: vòng đời ~2 phút), 0 TC cho trạng thái `status_sync=5`, 0 TC cho bảng retry mới. `NEW-137` chỉ ghi "giãn cách tăng dần" → **pass được cả code cũ lẫn mới**, không bắt được lệch | `[BLOCKER]` |
| G3 | **`X-Lme-Delivery-Id`** — giữ nguyên qua cả 3 lần gửi, và các row gộp trong cùng 1 request dùng chung 1 giá trị | `diff code` | `NEW-137` (skip) · `NEW-64` · `NEW-81` (chỉ kiểm UUID **duy nhất giữa các dòng DB**) | `RISK` — đây là khoá chống trùng của bên nhận (doc §5 · §7). Không TC nào kiểm **header thật gửi đi**; chiều "cùng 1 delivery_id cho lô gộp" **0 TC** | `[BLOCKER]` |
| G4 | **`X-Lme-Timestamp`** (doc §5: epoch mili giây, cả 2 kênh, mỗi lần gửi lại là giá trị mới) | `diff code` | `không có` | `GAP` — **0/214 TC** nhắc tới, và **không xuất hiện trong mô tả code của cả nhánh WEB lẫn JOB** (trong khi `X-Lme-Signature` + `X-Lme-Delivery-Id` đều được nêu đích danh) → nghi **chưa implement**. Doc §7 bảo bên nhận dùng header này để xử lý thứ tự | `[BLOCKER]` |
| G5 | **`Content-Type: application/json; charset=utf-8`** (doc §2, cả 2 kênh) | `diff code` | `không có` | `GAP` — 0 TC. Header duy nhất từng được kiểm trong 214 TC là `X-Lme-Signature` | `[MAJOR]` |
| G6 | **Bảng 10 built-in `field_id` ÂM** (`-1 システム表示名` … `-10 建物名・部屋番号`), custom field = ID dương (doc §4) | `diff code` | `không có` | `GAP` — 0 TC verify ánh xạ. TC hiện có chỉ nói chung *"có trường định danh trường thông tin bị thao tác"*. Sai 1 ID = bên thứ 3 ghi nhầm cột dữ liệu khách | `[BLOCKER]` |
| G7 | **`value` VẮNG MẶT khi `action=clear`** (doc §4: absent ≠ `null` ≠ `""`) | `diff code` | `NEW-73` (skip) · `NEW-134` (skip) | `RISK` — cả 2 chỉ ghi "không kèm giá trị" ở **tầng hàng đợi**, không chốt absent vs null, và **cả 2 đều chưa có kết luận** | `[MAJOR]` |
| G8 | **`line_friend_id` = chuỗi rỗng** khi friend đã bị xoá khỏi LME trước lúc gửi (doc §4) | `diff code` | `không có` | `GAP` — 0 TC. Doc yêu cầu bên nhận fallback sang `lmessage_friend_id` | `[MAJOR]` |
| G9 | **Gom request kênh LME**: tối đa **1.000 phần tử `events[]`**/request, vượt thì chia nhiều request; **1 request = 1 LINE OA duy nhất** (doc §4) | `diff code` | `không có` | `GAP` — 0 TC cả 2 chiều. Code chỉ nói `batch 500` (khái niệm khác). Trộn 2 OA trong 1 request = **rò rỉ dữ liệu chéo khách hàng** | `[BLOCKER]` |
| G10 | **Kênh LINE gửi nguyên văn body** kể cả `destination` (doc §3 「加工せずそのまま」) | `diff code` | `NEW-138` (pass@staging) | `RISK` — expected của TC đúng ("không thêm trường") nhưng note của chính TC + `dev_impact` đều ghi bản dựng **bọc envelope 3 trường** mà TC vẫn `pass` → false pass. Trường `destination` **0 TC** verify riêng. Xem `C2` §4 | `[BLOCKER]` |
| G11 | **Media kênh LINE chỉ mang ID nội dung**, không chứa file (doc §3) | `diff code` | `NEW-178` · `NEW-179` · `NEW-180` (image/video/audio, pass@staging) | `RISK` — 3 TC verify forward được, nhưng **không TC nào chốt payload KHÔNG kèm file/nhị phân** — đúng điểm doc nhấn mạnh (bên nhận phải tự gọi LINE Content API) | `[MAJOR]` |
| G12 | **OA bị xoá / hết hạn quá 7 ngày** → ngừng forward, cấu hình giữ nguyên, khôi phục là dùng lại được (doc §3) | `diff code` | `không có` | `GAP` — 0 TC. Biên 7 ngày, 3 nhánh (còn hạn / quá 7 ngày / khôi phục) | `[MAJOR]` |
| G13 | **Ma trận 7 dòng mã lỗi → chuỗi JP** (doc §6) | `diff code` | `NEW-32` (pass) · `NEW-147` (pass) · `NEW-33` (pass) · `NEW-139` (**skip**) | `RISK` — `NEW-32` expected mơ hồ (*"hiển thị theo fallback được BA/implementation chốt"*) → không phải oracle. Thiếu TC riêng cho `401/403 → 認証エラー` · `404 → 転送先が見つかりません` · `503 → 転送先が一時的に応答できません` · `5xx khác → 転送先でエラーが発生しました`; **`408/504` 0 TC**. `NEW-33`/`NEW-139` còn xung đột với commit `319053d100` — xem `C5` §4 | `[MAJOR]` |
| G14 | **Cửa sổ trễ cấu hình ~1 phút khi vừa BẬT kênh** (doc §1, tình huống 1/3) | `diff code` | `NEW-117` (skip — chỉ đổi URL + tắt kênh) · `NEW-60` (skip — hiệu lực tức thì phía web) | `GAP` — tình huống nguy hiểm nhất chưa ai chạm: event trong cửa sổ **không được forward VÀ không xuất hiện trong danh sách lỗi** → mất dữ liệu âm thầm, không dấu vết. `NEW-103`/`NEW-104` đặt tiền đề *"sau khi Job đã nhận config mới"* → **né** cửa sổ thay vì test nó | `[BLOCKER]` |
| G15 | **Thứ tự không đảm bảo** + **gửi trùng có thể xảy ra** (doc §2 · §7) | `diff code` | `không có` | `GAP` — 0 TC cho cả hai. Doc yêu cầu bên nhận tự xử lý; không có TC thì không chứng minh được LME thật sự hành xử như doc mô tả | `[MAJOR]` |
| G16 | **Đổi index `callback_event`** `(status, status_sync, id)` → `(status_sync, id)` — bắt buộc đổi TRƯỚC khi deploy `#41038`, nếu không câu quét mới full scan + filesort trên bảng nóng nhất hệ thống | `diff code` | `NEW-145` (chỉ kiểm index **tồn tại**) | `RISK` — 0 TC đo trên quy mô thật; `NEW-130`/`NEW-146` (index không làm chậm ghi khi tải cao) đang skip. **0/214 TC chạy production** → RULE-08 cấm kết luận | `[MAJOR]` |
| G17 | **Endpoint debug `/api/webhook-decode/{secret}`** — không auth, không lấy `bot_id` từ session, trả về `bot_id` gắn với secret | `diff code` | `NEW-207` (**skip**, ticket #40764) | `RISK` — Studio + review release đều gắn nhãn **CHẶN RELEASE**; TC tồn tại nhưng **chưa có kết luận** | `[BLOCKER]` |
| G18 | **Endpoint `/api/callback/webhook-test`** — công khai, không auth, không throttle, không log | `diff code` | `không có` | `GAP` — 0 TC. Redmine note liệt kê ở mục rủi ro (S6) | `[MAJOR]` |
| G19 | **Sidebar + `layout-v2-admin.css`** — ảnh hưởng **MỌI màn admin v2** | `diff code` | `không có` | `GAP` — 0 TC hồi quy menu/icon toàn hệ thống dù Redmine note nêu đích danh | `[MAJOR]` |
| G20 | **`AddAccessFeatureWebhookRelay@handle`** — shift `order` hàng loạt trên `access_feature`, **không bọc transaction**, chạy tay lúc release | `diff code` | `NEW-50` (pass, #40528 — chỉ kiểm vị trí mục quyền) | `RISK` — 0 TC cho chạy lại 2 lần / đứt giữa chừng, đúng loại rủi ro Redmine note (W1) nêu | `[MAJOR]` |
| G21 | **`HelperService` — điểm gắn/gỡ tag DÙNG CHUNG** (chat · kịch bản · tự động · CSV · form), không chỉ modal 「タグ編集」 | `diff code` | `NEW-162` · `NEW-163` (skip) · `NEW-164` (chưa chạy) · `NEW-127` (skip) | `RISK` — 4/4 TC **không có kết luận**. Redmine note yêu cầu hồi quy tag ở **TẤT CẢ lối vào** | `[BLOCKER]` |
| G22 | **Bảng `webhook_relay_queue` phía web bị bỏ hẳn** (`#40763`) — nhưng `#41040` **tạo lại bảng CÙNG TÊN** cho hàng đợi retry của job | `diff code` | `NEW-210` (skip, #40763) · `NEW-171` (skip) | `RISK` — 2 TC đang nói về **bảng cũ đã bị gỡ**; sau `#41040` cùng tên đó là bảng khác hẳn về mục đích → expected hiện hành dễ gây hiểu nhầm. Xem `X1` §6 | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `31 quan điểm Trigger khớp task · 14 chưa cover đủ`.

> **Đã loại khỏi phạm vi** (RULE-03), Leader xác nhận 2026-09-08 — giữ nguyên vòng này:
> `DATA-BACKUP-001` (backup/copy bot không hỗ trợ 3 bảng của Webhook転送) · `DEPLOY-LIVE-001` (release có bật maintain).
> Mã `Q*` giữ số cũ để cột `Ghi chú` §7 trỏ đúng.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `SEC-001` | Cao | `RISK` — 2 TC nhưng **0 kết luận**: `NEW-26` (consent gửi PII lần bật đầu) **fail** + bug #40519 bị **reject**; `NEW-206` (negative control — sự kiện ngoài phase 1 không bị gửi ra) **skip**. Đây là 2 chốt chặn duy nhất cho việc đẩy PII của friend ra hệ thống bên thứ 3 | `[BLOCKER]` |
| Q2 | `PERM-002` | Cao | `GAP kết luận` — **2/2 TC đều `fail`** (`NEW-51` staff chưa cấp quyền vẫn vào được màn · `NEW-52` vẫn gọi được 5 đường dẫn dữ liệu). Bug liên quan #40536 đã bị **reject** → chưa rõ fail là lỗi thật hay expected sai. Chặn ở UI mà không chặn ở server = lộ signing secret | `[BLOCKER]` |
| Q3 | `PERM-004` | Cao | `RISK` — TC duy nhất `NEW-54` (thu hồi quyền lúc staff đang mở màn) đang **fail**, không có TC thay thế | `[MAJOR]` |
| Q4 | `BULK-001` | Cao | `RISK` — 3 TC đủ 3 loại case nhưng **0/3 có kết luận** (`NEW-162`·`NEW-163` skip, `NEW-164` chưa chạy). Chiều bắt buộc là **đếm**: số friend thật sự bị tác động khớp 100% số đã lọc | `[BLOCKER]` |
| Q5 | `FRIEND-001` | Cao | `RISK` — 9 TC nhưng **7/9 không có kết luận**. Thiếu hẳn trục **`field_id` âm** (G6) và trục `value` vắng mặt khi `clear` (G7). `NEW-134` (TC bao quát nhất) vẫn skip | `[BLOCKER]` |
| Q6 | `JOB-001` | Cao | `RISK` — chỉ 2 TC (`NEW-170` pass · `NEW-169` chưa chạy), **thiếu `Normal`** → vi phạm RULE-01. Thiếu chiều "số bản ghi vào = số thành công + số ghi lỗi" ở quy mô thật | `[MAJOR]` |
| Q7 | `SEC-ISO-001` | Cao | `RISK` — TC duy nhất `NEW-56` (user không thuộc OA truy cập cấu hình + secret của OA khác) đang **skip**. Cộng thêm chiều mới từ doc §4: 1 request không được trộn 2 OA (G9) | `[BLOCKER]` |
| Q8 | `DATA-AUDIT-001` | Cao | `RISK` — **3/3 TC đều skip** (`NEW-48` lưu cấu hình · `NEW-172` tái tạo secret + bật/tắt kênh · `NEW-173` gọi thẳng EP-02/EP-03). Đúng nhóm thao tác nhạy cảm nhất của màn | `[MAJOR]` |
| Q9 | `ENV-003` | Cao | `RISK` — 3 TC `pass` nhưng **0/214 TC chạy production** (staging 154 · local 43 · dev 0 · prd 0). Tính năng chạm domain đích ngoài + job nền + online DDL bảng nóng → **RULE-08** cấm kết luận từ staging | `[MAJOR]` |
| Q10 | `REG-SHARED-001` | Cao | `RISK` — 21 TC nhưng chỉ **5 pass**, 16 không kết luận (12 skip + 4 chưa chạy). Vùng hồi quy Redmine note nêu (`HelperService` mọi lối gắn tag · sidebar toàn admin v2) chưa có TC — xem G19 · G21 | `[BLOCKER]` |
| Q11 | `REG-RUN-001` | Cao | `RISK` — 2 TC, `NEW-143` skip + `NEW-230` (ALTER 3 bảng nóng lúc webhook đang đổ về) **chưa chạy**; `NEW-230` khai `env_scope=prd` mà chưa có vòng chạy production nào | `[MAJOR]` |
| Q12 | `CONC-002` + `DATA-MIG-001` | Cao | `RISK` — `NEW-121` (chạy lại script recover `status_sync=4` nhiều lần) **skip**; không TC nào chạy script **ĐỒNG THỜI** với traffic mới. Không recover trước khi bật cờ = forward ngược **toàn bộ lịch sử** ra endpoint khách (Dev ghi rõ ở `extra_info` mục 4.2) | `[BLOCKER]` |
| Q13 | `DATA-CACHE-001` | Cao | `RISK` — 4 TC, 2 pass nhưng **2 TC đúng trọng tâm đều skip** (`NEW-60`, `NEW-117`). Cửa sổ trễ 1 phút là hành vi doc §1 · §5 mô tả kỹ nhất — xem G14 | `[BLOCKER]` |
| Q14 | `MEDIA-001` | Cao | `GAP` — 0 TC mang mã này. Trigger khớp: kênh LINE forward event media (ảnh · video · audio · file). Doc §3 chốt payload **chỉ mang ID nội dung** + bên nhận tự gọi LINE Content API — xem G11 | `[MAJOR]` |

---

## 3. TC trùng lặp nội dung

**Đã rà 214 TC** (so theo **ý định test**: `mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương` → `expected`).

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-209` | `NEW-39` | `DUP-SUBSET` | Cùng `TOOL-VAL2-001` · cùng `Abnormal` · **cùng nguyên văn tiêu đề** "EP-02 vẫn kiểm đủ luật URL khi bỏ qua giao diện" · cùng tiền đề. `NEW-39` = 5 ca URL; `NEW-209` = **đúng 5 ca đó + 2 ca mới** (#40728 host không phân giải). `NEW-209` là superset thật sự | `[MINOR]` |
| DUP-2 | `NEW-175`…`NEW-195` (21 TC lẻ theo từng loại event) | `NEW-136` | `DUP-SUBSET` (chiều ngược — TC cũ là superset) | Cùng luồng forward kênh LINE · cùng `Normal` · `NEW-136` gộp **6 thao tác** (message · postback×2 · follow×2 · unfollow) vào 1 TC, nay đã được tách thành TC lẻ từng loại | `[MINOR]` |

- **Gate đã chạy**: giả định xóa `NEW-39` + `NEW-136` → coverage §1 và quan điểm §2 **còn nguyên** (`TOOL-VAL2-001` vẫn còn `NEW-209`; `JOB-002` còn `NEW-137`·`NEW-142`·`NEW-156`; luồng 6 thao tác đã có 21 TC lẻ cover chi tiết hơn). ✔ Xóa hợp lệ.
- `DUP-EXACT`: không có. `DUP-INFLATE`: không có → không che GAP nào.
- ⚠️ **141 cặp có độ giống văn bản > 0,62 đã soi tay và LOẠI khỏi bảng trên** — phần lớn là `NEW-175`…`NEW-200`: chúng dùng chung một đoạn `expected` mẫu ("mỗi event chỉ sinh đúng 1 request… kênh LINE không có `X-Lme-Signature`…") nhưng **khác `đối tượng`** (mỗi TC một loại event LINE riêng) → **không phải trùng**. Tương tự các cặp gương 2 kênh (`NEW-97↔98`, `NEW-99↔100`, `NEW-30↔150`, `NEW-34↔151`, `NEW-35↔152`) và cặp cách ly 2 chiều (`NEW-63↔75`).
- Xóa thật do human thực hiện trên Studio (`testcase_delete`) — **không tự xóa**.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: `214` TC × **tài liệu hợp đồng outbound bản 1.0.0 (16/09/2026)** + `kho-tcs/fa012-quanlythe-タグ管理.md` + `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md`.
⚠️ `spec-features/` **không có** thư mục webhook-relay và `LME-SYSTEM-SPEC.md` không có 「Webhook転送」 → `CONF-SPEC` dưới đây đối chiếu với **doc 1.0.0 human cung cấp**, không phải `feature-spec.md`.
`kho-tcs` **chưa có** tính năng 「Webhook転送」 → `CONF-KHO`: **không đối chiếu được** (không ghi là "đã rà sạch").

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | `NEW-140` · `NEW-118` (cả 2 `pass@staging`) | Giá trị header `X-Lme-Signature` của kênh LME | `NEW-140`: *"giá trị là chuỗi hex khớp đúng `hex(HMAC-SHA256(raw body, signing secret))`. **Plaintext signing secret không xuất hiện trong body, header hay log**"* | **Doc 1.0.0 §5**: *"Giá trị **secret** của tài khoản LINE chính thức đó, dạng `whsec_…`. **So sánh chuỗi là đủ**"* | Doc yêu cầu **đúng cái TC đang cấm**. Có **2 bản hợp đồng outbound mâu thuẫn**: doc 1.0.0 vs `docs/api/webhook-relay-outbound-contract.md` trong repo (commit `acd29bcc97` *"chốt X-Lme-Signature = HEX + bàn giao hợp đồng outbound cho linect-service"*). Code + TC theo HEX. Bên thứ 3 code theo doc 1.0.0 sẽ **reject 100% request** | `[BLOCKER]` | `PM + Dev` |
| C2 | `CONF-SPEC` | `NEW-138` (`pass@staging`) | Nội dung body kênh LINE gửi ra | `NEW-138`: *"không thêm trường, không bớt trường, không đổi thứ tự"* — nhưng **note của chính TC** ghi bản dựng bọc payload vào lớp vỏ thêm 3 trường (định danh LINE OA · id `callback_event` · loại event), và `dev_impact` xác nhận `buildBody()` BỌC envelope | **Doc 1.0.0 §3**: *"**NGUYÊN VĂN** request body mà LINE Platform gửi tới LME, giữ nguyên không thêm bớt — gồm cả `destination` lẫn mảng `events`. LME không bóc tách, không dựng lại JSON"* | Doc **đã chốt** → không còn là câu hỏi spec mà là **lỗi code**; `NEW-138` phải là `Không đạt` + raise ticket. Hoặc doc 1.0.0 phải sửa theo bản dựng | `[BLOCKER]` | `Dev + PM` |
| C3 | `CONF-SPEC` | `NEW-140` · `NEW-155` (cả 2 `pass`) | Hành vi sau khi tái tạo signing secret | `NEW-140`: *"request LME kế tiếp có chữ ký khớp secret **MỚI** và **không còn khớp secret cũ**"*; `NEW-155`: *"secret cũ hết hiệu lực **ngay**"* | **Doc 1.0.0 §5**: *"luồng chuyển tiếp đọc cấu hình theo chu kỳ 1 phút, nên **trong khoảng tới 1 phút sau khi tái tạo, LME vẫn gửi kèm secret CŨ**"* + khuyến nghị bên nhận chấp nhận cả 2 secret trong 2 phút | Hai bên nói ngược nhau. Review release của Dev còn ghi *"Secret cũ hết hiệu lực NGAY ⇒ phá tích hợp phía đối tác"* → **3 nguồn, 2 hành vi**. Nếu doc đúng thì `NEW-140`/`NEW-155` expected sai | `[BLOCKER]` | `Dev + PM` |
| C4 | `CONF-SPEC` | `NEW-118` · `NEW-73` · `NEW-134` | Tập giá trị `action` của event `friend_info` | `NEW-118`: *"type/action đúng với **set/update/clear/point**"*; `NEW-73`/`NEW-134`: *"đặt giá trị, xoá giá trị, **cộng điểm**"* | **Doc 1.0.0 §4**: friend_info action **chỉ** `set` \| `clear` (tag chỉ `add` \| `remove`) | `update` và `point` **không tồn tại** trong hợp đồng doc. Hoặc doc thiếu 2 giá trị, hoặc TC khai giá trị chưa được duyệt — `NEW-118` note tự ghi *"testcase không tự bịa mapping chưa approved"* nhưng vẫn liệt kê 4 giá trị | `[MAJOR]` | `PM + Dev` |
| C5 | `CONF-SPEC` | `NEW-139` (skip) · `NEW-33` (`pass@staging`) | Cột `エラーコード` khi gửi hết thời gian chờ | `NEW-139`: *"ghi dòng lỗi … cột mã HTTP **để trống**; cột 「エラーコード」 hiển thị 「—」"*; `NEW-33`: *"dòng không có mã HTTP hiển thị 「—」"* (ca timeout) | Commit **`319053d100`** *"TIMEOUT ghi `http_status = 408` thay vì NULL"* + **doc 1.0.0 §6** liệt kê ca timeout với mã `—, 408, 504` | Expected của cả 2 TC **đã lỗi thời** so với code. Hệ quả thêm: doc §6 đề xuất tách 2 chuỗi *"tuỳ theo cột mã lỗi có giá trị hay không"* — **phương án đó nay bất khả thi** vì timeout của chính LME cũng ghi `408`, không phân biệt được với endpoint tự trả `408` | `[MAJOR]` | `Dev + BA` |
| C6 | `CONF-SPEC` | `NEW-61` (`pass@local`) | Event LINE mà LME không xử lý được có được forward không | `NEW-61`: *"Với sự kiện `delivery`: … hệ thống **không** ghi dòng sự kiện gọi lại và do đó cũng **KHÔNG** sinh dòng hàng đợi chuyển tiếp"* → tức **không forward** | **Doc 1.0.0 §1**: kênh LINE forward *"**toàn bộ event** LINE Platform gửi tới — không lọc theo loại, **không phụ thuộc LME có xử lý được hay không**"*. Bug `#41038` cũng đã đảo điều kiện quét theo hướng này | `NEW-61` khoá đúng hành vi mà `#41038` vừa fix bỏ → expected **trái doc**. Còn một câu hỏi mở: event LME **không ghi vào `callback_event`** (như `delivery`) thì vẫn không có nguồn để forward — `#41038` chưa giải quyết ca này | `[MAJOR]` | `Dev + PM` |

- Mỗi dòng trên đã có 1 dòng tương ứng ở **§8**.
- `C1` · `C2` · `C3` làm **mất chuẩn đánh giá Đạt–Không đạt** cho toàn bộ nhóm TC hợp đồng outbound → đã thêm `G3` · `G4` · `G10` ở §1 và `Q5` ở §2.
- `CONF-TC` (2 TC nội bộ loại trừ nhau): **không phát hiện**.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ nhóm TC job | **Code đang test lệch code mới nhất.** Studio `dev_impact`: bản JOB đã sync `f4e53fa9` **CHƯA có** commit `29dc078` (`#41038`) và `9fadcf4` (`#41040`). Mọi kết quả của `NEW-241` · `NEW-242` · `NEW-137` và nhóm retry/forward-status đang chạy trên **hành vi cũ** → `pass` không có giá trị kết luận | Re-sync nhánh job lên Studio, chạy lại toàn bộ TC thuộc `G1` · `G2` · `G3` trước khi chốt round 1 |
| I2 | `[BLOCKER]` | Toàn bộ 214 TC | **Tỷ lệ có kết luận chỉ 132/214 = 61,7%**: 6 fail · 59 skip · 17 chưa chạy = **82 TC (38%) không có kết luận**. Phần skip tập trung đúng vào job nền, phát hành, phân quyền và hợp đồng payload — nhóm rủi ro cao nhất | Chạy hết 82 TC; ưu tiên nhóm `G1`–`G3`, `Q1`, `Q2`, `Q12` |
| I3 | `[BLOCKER]` | 214 TC · mọi run | **0 TC chạy production** (staging 154 · local 43 · dev 0 · prd 0). Tính năng chạm **domain đích ngoài (SSRF) · job nền · online DDL trên `callback_event`** — bảng nóng nhất hệ thống → **RULE-08** / `ENV-003` cấm kết luận từ staging | Bổ sung vòng chạy production cho nhóm TC ghi `Phạm vi ENV = product` ở §7, có DevOps trực |
| I4 | `[MAJOR]` | `03-dev-impact.md` | **File 03 đã lỗi thời.** Redmine #40044 **nay ĐÃ CÓ** note "★ ĐÁNH GIÁ ẢNH HƯỞNG" đầy đủ (phạm vi · file dùng chung bị sửa · data · tính năng liên quan · recover · verify · rủi ro), nhưng file 03 trong folder vẫn ghi `<Input thiếu — Dev chưa cung cấp>` ở cả 4 mục → **chiều (a) của §1 trống oan** | Chạy lại `/new-task 40044` để đồng bộ file 03, rồi review lại §1 chiều (a). Vòng này đã dùng tạm note đó qua Studio `spec_delta.redmine.lastNotes` |
| I5 | `[MAJOR]` | `NEW-138` | **Kết quả `pass` mâu thuẫn chính nội dung TC** — expected "không thêm trường" trong khi note của TC và `dev_impact` đều xác nhận bản dựng bọc envelope. `pass` ở đây là **false success che một lệch hợp đồng** | Re-triage `NEW-138`. Chốt `C2` §4 trước, rồi hoặc sửa expected hoặc raise bug |
| I6 | `[MAJOR]` | 6 TC fail | **6 TC `fail` — không TC nào có bug ticket Redmine**: `NEW-13` (nút 「使い方を見る」) · `NEW-26` (consent PII, #40519 bị reject) · `NEW-51` · `NEW-52` · `NEW-54` (3 TC phân quyền) · `NEW-157` (a11y sort, #40535 bị reject). 3 TC phân quyền fail cùng lúc là tín hiệu **lỗi hệ thống phân quyền**, không phải lỗi lẻ | Raise ticket cho `NEW-13` · `NEW-51` · `NEW-52` · `NEW-54`. `NEW-26`/`NEW-157` chờ chốt spec (§8) rồi mới đóng hay sửa expected |
| I7 | `[MAJOR]` | Nguồn spec | **Không có spec trong repo cho tính năng.** `spec-features/` không có thư mục webhook-relay; `LME-SYSTEM-SPEC.md` chỉ có `FA-038 LOA接続設定`. Chuẩn đánh giá hiện là 21 `REQ-*` Studio tự sinh + doc 1.0.0 human dán trực tiếp + `docs/api/webhook-relay-outbound-contract.md` nằm trong repo `sns-line` (ngoài tầm với của review này) | Bổ sung `spec-features/admin/webhook-relay/feature-spec.md`, hoặc chốt doc 1.0.0 là spec chính thức rồi dán link vào lệnh review sau |
| I8 | `[MAJOR]` | 214/214 TC | **`spec_status` = null toàn bộ** và **`spec_change` = 0 toàn bộ**, trong khi đã có ≥ 6 quyết định spec mới phát sinh sau khi TC được viết (5 bug reject + doc 1.0.0). Không có dấu vết rà lại TC theo `REG-SPEC-001` (4 trạng thái `[Giữ nguyên]`/`[Cần sửa]`/`[Cần thêm mới]`/`[Hết hiệu lực]`) | Điền `spec_status` cho nhóm TC thuộc `C1`–`C6` trước khi Leader duyệt |
| I9 | `[MINOR]` | 98/214 TC | **98 TC không gắn `requirement_keys`** và **7 TC không gắn mã quan điểm** (`NEW-232`…`236`, `NEW-241`, `NEW-242`) → không map được vào coverage của Studio lẫn của `/review-tc` | Gắn `requirement_keys` + mã quan điểm cho nhóm TC mới thêm 2026-09-16 |
| I10 | `[MINOR]` | 214/214 TC | Tất cả TC còn `status = draft`, `reviewed = false`; `toolWritten.human = 0` (116 `author=AI` · 65 `ngannt@mcp` · 33 `haodtb@mcp`) — chưa có TC nào do QA người soạn đối chứng | Leader duyệt và chuyển trạng thái trước khi dùng làm bằng chứng release |

---

## 6. TCs thừa / ngoài phạm vi task

**Đã rà 214 TC.** Phát hiện 2 TC cần xử lý:

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | `NEW-171` | Test **bảng `webhook_relay_queue` phía web** — bảng này **đã bị gỡ hẳn** theo quyết định thiết kế `#40763`; job nay đọc thẳng từ bảng nguồn. Đối tượng test không còn tồn tại theo hình dạng TC mô tả | `NEW-210` expected: *"Theo quyết định thiết kế đã chốt là **bỏ hẳn cơ chế hàng đợi**, phía web KHÔNG còn được sinh dòng hàng đợi nào nữa"*; `dev_impact`: *"enqueue+emitter DEAD (C-001)"* | **Viết lại, không xóa**: `#41040` tạo bảng **cùng tên** cho hàng đợi retry của job — đổi `NEW-171` sang kiểm bảng retry mới (dọn dữ liệu, không phình) thay vì bảng web cũ | `[MINOR]` |
| X2 | `NEW-157` | Test **accessibility** (icon sort + nút 「最新に更新」 thao tác bằng bàn phím). Không map `BUG`/`F*`/`D*`/`T*`; không nằm trong điểm sửa / rủi ro hồi quy nào Studio `dev_impact` nêu; `A11Y-001` **không phải** quan điểm trong `framework/checklist-lme.md`. Bug tương ứng #40535 đã bị Dev **reject** | `spec_delta.diffStat` không có thay đổi nào về a11y; `dev_impact` không nhắc accessibility; TC đang `fail` mà không raise được ticket vì #40535 rejected | **Leader chốt trước**: a11y có nằm trong chuẩn nghiệm thu màn mới không (§8 mục 8). `Không` → bỏ khỏi phạm vi task; `Có` → giữ và raise lại ticket | `[NIT]` |

- **Gate đã chạy**: `NEW-171` không phải TC duy nhất cover `DATA-001` (còn `NEW-160` pass) ✔ · `NEW-157` là TC duy nhất mang `A11Y-001`, nhưng `A11Y-001` **không thuộc bộ 80 quan điểm** nên không làm thủng coverage §2 ✔ — dù vậy vẫn để `[NIT]` + chờ Leader chốt, **không đề nghị xóa thẳng**.
- Nhóm 21 TC theo từng loại event (`NEW-175`…`NEW-195`) và nhóm hồi quy downstream (`NEW-212`…`NEW-231`) **KHÔNG** phải TC thừa: dẫn được từ rủi ro hồi quy Studio (*"ALTER 3 bảng nóng đụng nhận webhook/auto-reply/scenario/richmenu/tag/friend info/CSV/form"*) và từ doc §1 (forward toàn bộ loại event).
- **Không tự xóa** — human xử lý trên Studio.

---
