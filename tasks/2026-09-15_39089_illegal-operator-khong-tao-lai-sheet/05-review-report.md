# 05 — Review Report

## 0. Nguồn TC

- **Nguồn đã dùng**: MCP LME TEST STUDIO — task #183 (ticket 39089), round 1, branch `ai_fixbug_39089`, `reviewState = leader`.
- **Tổng số TC review**: 15 (10 `pass` · 0 `fail` · 3 `skip` · 2 chưa chạy).

---

## 1. Coverage — `dev-impact` + `diff code`

> **Phạm vi review**: fix chỉ sửa **web** — 1 file `FormAnswerController.php` (callback connect / reconnect Google Spreadsheet của form). Job `CreateGoogleSheetFormAnswerCommand` và cơ chế sync câu trả lời **không bị sửa code** ⇒ `F2`, `D3` (phía job xử lý), `T2` **loại khỏi phạm vi coverage**, chỉ cần smoke qua kết quả hiển thị của luồng connect.

**Kết luận**: 4/8 vùng ảnh hưởng đủ TC · **2 GAP** · **2 RISK**.

| Mã | Chiều | Vùng ảnh hưởng | TC hiện có | Status | Vấn đề |
|---|---|---|---|---|---|
| **G1** | dev-impact | `F3` / `T3` — thao tác change bot ở màn 「LINE公式アカウント入れ替え」 (nguồn sinh state lỗi: xoá mốc liên kết, giữ email) | — | **GAP** | 15/15 TC đều **seed thẳng `datetime_connect_google_sheet = NULL` vào DB**. Không TC nào dựng state bằng thao tác change bot thật ⇒ chưa chứng minh đường người dùng thật đi tới bug, và chưa kiểm màn liên kết Google hiển thị gì sau change bot. |
| **G2** | dev-impact | `T1` — Form Builder FA-011, luồng reconnect Google Spreadsheet | NEW-5 (E2E), NEW-9 (mock) | **RISK** | TC E2E đường người dùng thật (**NEW-5**) **chưa chạy**. 10 TC `pass` đều là mock OAuth ở `env=local`. NEW-9 pass **không thay** được NEW-5 (xem §3 nhóm 2). |
| **G3** | diff code | Câu hỏi 3 — hàm **trùng tên** `redirectUriGoogleSheet` ở 3 controller (Form / CalendarSalon / CalendarManagement) | NEW-1 | **RISK** | Dev **có** kê danh sách caller và có TC smoke, nhưng **NEW-1 chưa chạy** ⇒ vùng regression do Dev chỉ định (RULE-12 phần 2) chưa được verify. |
| **G4** | diff code | Nhánh "email trùng + form **ĐÃ CÓ** `google_sheet_id`" trong callback connect | — | **GAP** | NEW-5 và NEW-9 chỉ expected "sinh record cho form **chưa có** `google_sheet_id`". **Không TC nào** nói form đã có sheet thì sau change bot + reconnect sẽ ghi vào file nào ⇒ mâu thuẫn với kho `TC-CB-155` (xem **§6 #1**). |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 10 quan điểm Trigger khớp phạm vi connect/reconnect · 3 đủ TC · **3 GAP** · **4 RISK**.

| Mã | Quan điểm | Ưu tiên | Status | Thiếu gì |
|---|---|---|---|---|
| **Q1** | `STATE-CLEAN-001` — dọn dẹp khi ngắt kết nối / gỡ tích hợp | Cao | **GAP** `[BLOCKER]` | **0 TC** đi qua thao tác gỡ tích hợp thật: thao tác change bot ở màn 「LINE公式アカウント入れ替え」 (xoá mốc, **giữ** email) và hủy liên kết Google (xoá email, **giữ** mốc). Đây là 2 đường sinh ra state đi vào đoạn code vừa sửa. Liên quan **G1**. |
| **Q2** | `COMPAT-LEGACY-001` ★ — dữ liệu đời cũ song song | Cao | **GAP** `[BLOCKER]` | **0 TC** cho bot liên kết Google **trước** bản bổ sung cột email (kho `TC-FORM-372`: bot cũ **không có** `google_sheet_account_email`) ⇒ reconnect rơi nhánh khác hẳn nhánh được fix, cần chứng minh không lỗi. |
| **Q3** | `STATE-001` — quy trình nhiều bước bị gián đoạn | Cao | **GAP** `[MAJOR]` | Chính bug này đã để lại state dở dang trên các bot đang dính lỗi (**token đã lưu, chưa tạo bản ghi yêu cầu tạo sheet**). **0 TC** verify bot đang kẹt ở state đó reconnect lại được sau khi deploy fix. |
| **Q4** | `INTG-HOOK-001` — callback trễ / trùng | Cao | **RISK** `[MAJOR]` | 3 TC guard đầu callback (NEW-12/13/14) đã tốt, nhưng **thiếu idempotency**: gọi lại **cùng URL callback** (user F5) → phải chỉ xử lý **1 lần**, không sinh yêu cầu tạo sheet trùng ⇒ nguy cơ 2 spreadsheet cho 1 form. |
| **Q5** | `DATA-DB-001` ★ — WHERE scope tầng DB | Cao | **RISK** `[MAJOR]` | Nội dung **đã được cover** bởi NEW-11 (2 bot + 2 `type_result`), nhưng TC mang mã `TOOL-NEGCTRL-001` — **không có trong `framework/checklist-lme.md`** ⇒ không map được coverage; thiếu evidence query trước/sau trên 2 bot. |
| **Q6** | `OUT-TRUTH-001` — UI/message khớp trạng thái THẬT | Cao | **RISK** `[MAJOR]` | NEW-5 có kiểm message 「Googleスプレッドシートに連携処理を行っています。」 nhưng **chưa chạy**, và phần "đã thật sự liên kết" đang verify bằng DB thay vì trên màn hình (icon spreadsheet ở list form). |
| **Q7** | `INTG-SHEET-001` — đồng bộ spreadsheet ngoài (**regression**) | Cao | **RISK** `[MAJOR]` | Job sync không bị sửa code, nhưng fix quyết định việc job **có dữ liệu để chạy hay không** sau connect/reconnect. TC duy nhất (NEW-2) **`skip`** + mock `createSheet` ⇒ chưa có bằng chứng job sync chạy bình thường sau khi liên kết lại. Chỉ cần **smoke end-to-end**, không test logic nội bộ job (retry / rate limit / backoff). |

> Quan điểm Trigger khớp và **đã đủ TC**: `FUNC-001` (nhánh email khác / lần đầu — NEW-6, NEW-7), `REG-SHARED-001` (NEW-1 — nhưng chưa chạy, xem G3), `DATA-001` (NEW-8, NEW-15).
>
> **Đã loại khỏi phạm vi** (job sync không bị sửa code — `spec_delta.files` chỉ có `FormAnswerController.php`; riêng `INTG-SHEET-001` giữ 2 case smoke regression ở Q7): `JOB-001`, logic nội bộ của `INTG-SHEET-001` (retry, rate limit, sync đứt giữa chừng), `CONC-002`, `REG-RUN-001`, `PERF-LARGE-001`, `ENV-003` (phần job production), `COMPAT-LEGACY-001` cặp header spreadsheet cũ/mới. Không đề xuất TC cho các mục này.

---

## 3. TC trùng lặp

Đã rà **toàn bộ 15 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`). Phát hiện **2 nhóm**:

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Biên mốc `created_at` khi `datetime` có giá trị | **NEW-15** (Boundary — R1 < T0 giữ, R2 = T0 và R3 > T0 reset) | **NEW-8** → **GỘP**, không xóa | `DUP-SUBSET` | Cùng `TOOL-OLDREC-001` · cùng thao tác (callback OAuth email trùng, mốc = T0) · cùng tiền đề (bản ghi trước/sau mốc) · expected của NEW-8 nằm trọn trong NEW-15 | `[MINOR]` |
| Reconnect cùng email + mốc NULL | **Giữ CẢ HAI** — NEW-5 (E2E, OAuth thật) và NEW-9 (mock, tầng logic) | **KHÔNG xóa TC nào** | `DUP-INFLATE` (che RISK) | Cùng `TOOL-KNOW-002` · cùng thao tác · cùng tiền đề (email E + mốc NULL) · expected tương đương (không exception + reset + tạo record) | `[MAJOR]` |

**Chi tiết xử lý**:

- **Nhóm 1** — đề nghị **gộp chứ không xóa**: NEW-8 là TC `Normal` **duy nhất** của `TOOL-OLDREC-001`, xóa đi sẽ mất loại case Normal (gate BƯỚC 4b). Cách gộp: giữ NEW-15, bổ sung vào expected của nó phần NEW-8 đang có thêm — *"sinh `form_answer_connect_googles` cho form chưa có `google_sheet_id`"*.
- **Nhóm 2** — **không phải trùng thừa** mà là 2 tầng kiểm chứng có chủ ý (Studio note ghi rõ). Vấn đề là **hiệu ứng che RISK**: NEW-9 `pass` (mock, local) làm REQ-001 trông như đã verify, trong khi NEW-5 — đường người dùng thật, TC verify-fixed lõi — **chưa chạy**. ⇒ đã mở lại RISK ở **§1 G2**. Đề nghị: chỉ được kết luận REQ-001 đạt **sau khi NEW-5 chạy trên môi trường có OAuth Google thật**.

---

## 4. Issues khác

### Chất lượng nguồn TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | `[MAJOR]` | NEW-5, NEW-1 + 10 TC `pass` | 2 TC quan trọng nhất của phạm vi connect **chưa chạy**: NEW-5 (E2E reconnect — TC verify-fixed lõi) và NEW-1 (smoke 2 màn Lịch). 10 TC `pass` đều chạy ở `env = local` với **OAuth Google bị mock**, do `pipeline` AI tự chạy. Bug gốc nằm trên luồng OAuth thật ⇒ mock không chứng minh được fix. | Chạy NEW-5 + NEW-1 trên môi trường có Google OAuth thật trước khi kết luận. |
| 2 | `[MAJOR]` | 13/15 TC | **RULE-02** — có `Kết quả thực thi` nhưng cột `Evidence thực tế` **rỗng toàn bộ** ⇒ kết quả tự khai. | Bổ sung evidence (ảnh màn liên kết, ảnh list form có icon spreadsheet, log). |
| 3 | `[MAJOR]` | 11/15 TC | **Mã quan điểm không có trong `framework/checklist-lme.md`**: `TOOL-KNOW-002` (3), `TOOL-ERRHYG-001` (3), `TOOL-OLDREC-001` (2), `TOOL-NEGCTRL-001` (1), `JOB-002` (2). Coverage không map được. | Đổi mã trên Studio (`testcase_update`): NEW-11 → `DATA-DB-001` · NEW-12/13/14 → `INTG-HOOK-001` · NEW-8/NEW-15 → `DATA-001` · NEW-5/9/10 → `FUNC-001`. |
| 4 | `[MAJOR]` | Nguồn spec | Studio `critique.excludedOrDeferred` kết luận *"Không tìm thấy spec feature"* — **SAI**. Repo **có** spec: `spec-features/admin/form-answer/` (BR-08 / BR-14, EP-17 / EP-20, `db-mapping.md`) và `spec-features/admin/change-bot/` (job change bot đặt mốc liên kết = NULL, giữ email). | Nạp lại spec vào task Studio. |
| 5 | `[MAJOR]` | Phạm vi ảnh hưởng | **RULE-04** — Dev ghi *"Không truy vấn được DB dev để đếm số bot dính"*. Chưa có thống kê số bot đang ở state mốc NULL + email còn (và số bot đang kẹt do bug cũ) ⇒ không biết bao nhiêu khách đang không liên kết lại được. | Yêu cầu Dev query production đếm trước khi đóng ticket; danh sách này cũng là input của `TC-STATE001-01`. |

### Chất lượng từng TC + anti-pattern

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 6 | `[MAJOR]` | NEW-5 | Tiền đề **seed DB** (`datetime_connect_google_sheet = NULL`) thay vì dựng bằng thao tác thật; expected verify "đã liên kết" bằng DB thay vì trên màn hình. | Sửa trên Studio theo §5 bảng "Sửa TC có sẵn". |
| 7 | `[MAJOR]` | `[AP-2]` File 01 | **Symptom-only**: tiêu đề ticket là hiện tượng *"không tạo lại sheet khi connect"*; Dev fix 1 root cause (WHERE NULL). Có thể có root cause thứ 2 cho cùng hiện tượng ở luồng connect: form đã có `google_sheet_id` trỏ tới file **đã bị xoá trên Drive** → reconnect cùng email bỏ qua form này (chỉ tạo cho form *chưa có* sheet), kho `TC-FORM-379` cũng ghi *"không tự tạo lại file"*. | Hỏi Dev: log exception này có phải nguyên nhân duy nhất của các case KH báo "không tạo lại sheet" không. |
| 8 | `[MINOR]` | `[AP-5]` NEW-2, NEW-3, NEW-4 | Job `CreateGoogleSheetFormAnswerCommand` **không bị sửa code**. NEW-3 / NEW-4 test **logic nội bộ** của job (retry, ngưỡng retry cuối) ⇒ over-coverage; ngoài ra 2 TC này seed `status = ERROR(3)` trong khi `db-mapping.md` định nghĩa ERROR là **giá trị âm**. NEW-2 cùng mục đích smoke với `TC-INTGSHEET001-01` nhưng mock `createSheet` nên không chứng minh được file thật được tạo. | NEW-3 / NEW-4: re-label `regression`, ưu tiên thấp, sửa giá trị status nếu giữ. NEW-2: thay bằng `TC-INTGSHEET001-01` (chạy với Google thật) hoặc sửa NEW-2 bỏ mock. |
| 9 | `[MINOR]` | NEW-9 | **`case_type` sai**: gắn `Abnormal` nhưng nội dung là happy-path sau fix. TC `Abnormal` đúng nghĩa là NEW-10 (tái hiện trên build chưa fix). | Đổi NEW-9 sang `Normal`. |
| 10 | `[MINOR]` | Toàn bộ 15 TC | Tất cả còn `status = draft`, `reviewed = false` trên Studio. | Sau khi sửa theo report → chuyển trạng thái. |
| 11 | `[NIT]` | Ngoài phạm vi ticket | Nhánh không có `code` gọi `redirect()` **thiếu `return`** — Dev đã khoanh ngoài scope. | Mở ticket riêng. |

---

## 5. TCs đề xuất bổ sung (6)

> **Đã đối chiếu 15 TC ở BƯỚC 0 + `kho-tcs/fa011-taobieumau-フォーム作成.md` (nhóm "Liên kết Google Sheet" + "Sync Google Sheet & job", `TC-FORM-360` → `TC-FORM-380`) + `kho-tcs/fa039-changebot-LINE公式アカウント入れ替え機能.md` (`TC-CB-155`) — không TC đề xuất nào trùng.**
>
> Phạm vi: **luồng connect / reconnect Google Spreadsheet của form trên web** + **2 case smoke regression** job sync chạy bình thường sau khi liên kết lại. Không test logic nội bộ của job (không bị sửa code).
>
> 2 case regression đi qua **nhánh vừa fix** (change bot → liên kết lại cùng tài khoản) nên không trùng kho `TC-FORM-370` (đi đường hủy liên kết), `TC-FORM-371` (tài khoản khác), `TC-FORM-376` (liên kết lần đầu).

**Sửa / dùng lại TC có sẵn (không đẻ TC mới)**:

| Mã | TC | Việc cần làm |
|---|---|---|
| **G1 · Q1 · Q6** | **NEW-5** (sửa trên Studio) | (1) Tiền đề: thay "seed `datetime_connect_google_sheet = NULL`" bằng **thao tác change bot ở màn 「LINE公式アカウント入れ替え」** sang LINE OA khác, giữ nguyên tài khoản Google E. (2) Thêm bước: sau change bot, mở màn 「Googleスプレッドシート連携」 kiểm tra đang hiển thị **chưa liên kết**. (3) Expected: kiểm trên màn hình — không lỗi, hiện message 「Googleスプレッドシートに連携処理を行っています。」, sau 3–5 phút form chưa có spreadsheet **hiện icon spreadsheet** ở list form (thay cho kiểm DB). |
| **Q1** | Kho **`TC-FORM-370`** (dùng lại) | Đường hủy liên kết → liên kết lại **cùng email** đã có sẵn trong kho. Chạy lại nguyên TC này làm regression. ⚠️ Expected của kho ("giữ file cũ") cần đối chiếu lại với code — xem **§6 #2**. |
| **G2 · G3** | NEW-5, NEW-1 | TC đã có và đúng — chỉ cần **chạy** trên môi trường có OAuth Google thật. |
| **G4** | — | **Không đề xuất TC** vì expected đang mâu thuẫn giữa kho `TC-CB-155` và `TC-FORM-370` → chờ Leader/Dev chốt ở **§6 #1**. |
| **Q5** | **NEW-11** | Nội dung đúng — đổi mã quan điểm sang `DATA-DB-001` + bổ sung evidence (§4 #3). |

**TC mới**:

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGSHEET001-01 | UI | INTG-SHEET-001 | Googleスプレッドシート連携 (form) → Google Spreadsheet | Normal | manual | Tất cả | Change bot rồi liên kết lại cùng tài khoản → form chưa có spreadsheet được tạo file và câu trả lời mới ghi lên đúng | - Đăng nhập admin bot A, bot A đã liên kết Google bằng tài khoản E<br>- Có 1 LINE OA khác để change bot<br>- Có 1 LINE user đã kết bạn với LINE OA **mới** | 1. Vào màn 「LINE公式アカウント入れ替え」, thực hiện change bot sang LINE OA khác, chờ xử lý xong<br>2. Tạo form F2 mới (form chưa có spreadsheet)<br>3. Mở màn 「Googleスプレッドシート連携」, liên kết lại Google bằng **đúng tài khoản E**<br>4. Chờ 3–5 phút, mở list form kiểm tra icon spreadsheet của F2<br>5. Cho LINE user trả lời F2 → submit<br>6. Chờ job sync, bấm icon spreadsheet của F2 mở file, đối chiếu với màn kết quả trả lời | Tài khoản Google E; form F2 tạo sau change bot; 1 câu trả lời | F2 hiện icon spreadsheet, mở ra được file trên Google Drive của tài khoản E · file có dòng tiêu đề + **đúng 1 dòng** câu trả lời vừa submit · nội dung từng cột khớp màn kết quả trả lời |  | Lấp Q7 · regression — smoke job tạo file + ghi câu trả lời sau reconnect, không test logic nội bộ job · Evidence: ảnh list form + ảnh file spreadsheet + ảnh màn kết quả trả lời (RULE-06) |
| TC-INTGSHEET001-02 | UI | INTG-SHEET-001 | Googleスプレッドシート連携 (form) → Google Spreadsheet | Normal | manual | Tất cả | Câu trả lời phát sinh trong lúc mất liên kết (sau change bot) được sync bù sau khi liên kết lại cùng tài khoản, không trùng dòng | - Bot A đã liên kết Google bằng tài khoản E, form F1 đã có spreadsheet và đã có câu trả lời sync lên sheet<br>- Có 1 LINE OA khác để change bot, có LINE user đã kết bạn với LINE OA mới | 1. Mở spreadsheet của F1 (bấm icon ở list form), ghi lại số dòng data hiện có<br>2. Vào màn 「LINE公式アカウント入れ替え」, thực hiện change bot sang LINE OA khác, chờ xử lý xong<br>3. **Trước khi liên kết lại**, cho LINE user trả lời F1 2 lần → submit<br>4. Mở màn 「Googleスプレッドシート連携」, liên kết lại Google bằng **đúng tài khoản E**<br>5. Chờ job sync chạy (3–5 phút)<br>6. Bấm icon spreadsheet của F1 mở file, đếm số dòng và đối chiếu với màn kết quả trả lời | Tài khoản Google E; 2 câu trả lời submit trong lúc mất liên kết | 2 câu trả lời phát sinh lúc mất liên kết **có mặt** trong spreadsheet đang được map với F1 · **không dòng nào bị lặp** (các dòng đã sync trước change bot không bị ghi lại lần nữa) · nội dung khớp màn kết quả trả lời |  | Lấp Q7 · regression — đây là mục đích của việc reset dữ liệu lỗi trong đoạn code vừa sửa · ⚠️ file đích (cũ hay mới) phụ thuộc kết luận **§6 #1** — kiểm file mà icon spreadsheet đang mở ra, không tự chọn · Evidence: ảnh spreadsheet trước/sau + ảnh màn kết quả trả lời |
| TC-STATECLEAN001-01 | UI | STATE-CLEAN-001 | Googleスプレッドシート連携 (form) | Boundary | manual | Tất cả | Change bot rồi liên kết lại cùng email khi bot CHƯA có câu trả lời form nào → không lỗi, form được liên kết | - Đăng nhập admin bot B, bot B đã liên kết Google bằng tài khoản E<br>- Bot B có 2 form nhưng **chưa có câu trả lời nào** (chưa từng sync, nên không có dữ liệu lỗi đồng bộ)<br>- Có 1 LINE OA khác để change bot | 1. Vào màn 「LINE公式アカウント入れ替え」, thực hiện change bot sang LINE OA khác, chờ xử lý xong<br>2. Mở màn 「Googleスプレッドシート連携」, xác nhận đang hiển thị chưa liên kết<br>3. Bấm liên kết Google, đăng nhập **đúng tài khoản E**, cấp đủ quyền<br>4. Quan sát màn hình trả về<br>5. Chờ 3–5 phút, mở list form kiểm tra icon spreadsheet | Tài khoản Google E (trùng tài khoản trước change bot); 2 form, 0 câu trả lời | Không xuất hiện lỗi 500 / 「Illegal operator and value combination」 · màn trả về hiển thị 「Googleスプレッドシートに連携処理を行っています。」 · sau 3–5 phút cả 2 form hiện icon spreadsheet |  | Lấp G1 · Lấp Q1 · Biên: không có dữ liệu lỗi nào để reset (cặp với NEW-5 là ca có dữ liệu lỗi) · Cần OAuth Google thật · Evidence: ảnh màn liên kết trước/sau + ảnh list form |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Googleスプレッドシート連携 (form) | Normal | manual | Tất cả | Bot liên kết Google TRƯỚC khi hệ thống lưu email tài khoản → liên kết lại không lỗi | - Bot D đã liên kết Google **từ trước** khi hệ thống bổ sung lưu email tài khoản Google (Dev cung cấp bot thỏa điều kiện), form đang có spreadsheet | 1. Mở màn 「Googleスプレッドシート連携」 của bot D, ghi lại trạng thái hiện tại<br>2. Thực hiện change bot ở màn 「LINE公式アカウント入れ替え」 (hoặc hủy liên kết Google)<br>3. Liên kết lại Google bằng tài khoản cũ, cấp đủ quyền<br>4. Quan sát màn hình trả về<br>5. Chờ 3–5 phút, mở list form kiểm tra icon spreadsheet | Bot D đời cũ | Không xuất hiện lỗi ở bất kỳ bước nào · màn trả về hiển thị message đang xử lý · sau 3–5 phút các form hiện icon spreadsheet |  | Lấp Q2 · RULE-09 — nhánh dữ liệu đời cũ · dẫn từ TC-FORM-372 · Evidence: ảnh màn liên kết + ảnh list form |
| TC-INTGHOOK001-01 | UI | INTG-HOOK-001 | Googleスプレッドシート連携 (form) | Abnormal | manual | Tất cả | Tải lại (F5) trang callback sau khi liên kết → chỉ xử lý 1 lần, không tạo 2 spreadsheet cho 1 form | - Bot A đã change bot ở màn 「LINE公式アカウント入れ替え」, tài khoản Google E còn lưu, có 2 form chưa có spreadsheet | 1. Liên kết Google bằng tài khoản E cho tới khi trình duyệt quay về màn của LME<br>2. **Bấm F5** tải lại đúng trang vừa quay về<br>3. Quan sát màn hình sau khi tải lại<br>4. Chờ 3–5 phút, mở Google Drive của tài khoản E đếm số file spreadsheet của từng form | Cùng 1 URL callback mở 2 lần | Lần tải lại không gây lỗi 500 · mỗi form chỉ có **đúng 1** file spreadsheet trên Drive · list form hiển thị icon spreadsheet bình thường |  | Lấp Q4 · Chỉ có Abnormal — idempotency chỉ có 1 kịch bản phá · Evidence: ảnh Drive đếm file + ảnh màn sau F5 |
| TC-STATE001-01 | UI | STATE-001 | Googleスプレッドシート連携 (form) | Abnormal | manual | Tất cả | Bot đang kẹt do bug cũ (đã liên kết lỗi, form chưa có spreadsheet) → sau deploy fix liên kết lại được | - Bot E thuộc danh sách bot **đang dính bug** (Dev cung cấp từ query phạm vi — §4 #5): đã từng liên kết lại thất bại, form vẫn chưa có spreadsheet<br>- Đã deploy bản fix | 1. Mở list form của bot E, xác nhận form chưa có icon spreadsheet<br>2. Mở màn 「Googleスプレッドシート連携」, ghi lại trạng thái hiển thị<br>3. Liên kết lại Google bằng đúng tài khoản đã dùng trước đó<br>4. Quan sát màn hình trả về<br>5. Chờ 3–5 phút, mở lại list form | Bot đang kẹt từ trước khi fix | Liên kết không lỗi · màn trả về hiển thị message đang xử lý · sau 3–5 phút form hiện icon spreadsheet ⇒ bot dính bug **tự phục hồi được bằng thao tác liên kết lại**, không cần Dev can thiệp dữ liệu |  | Lấp Q3 · Dữ liệu thật chỉ có trên môi trường đã phát sinh bug — chạy nơi Dev cung cấp được bot · Evidence: ảnh list form trước/sau |

---

## 6. Spec update needed

| # | Điểm cần chốt | Mâu thuẫn / thiếu | Ai chốt |
|---|---|---|---|
| 1 | **Sau thao tác change bot ở màn 「LINE公式アカウント入れ替え」, form ĐÃ CÓ spreadsheet mà liên kết lại cùng tài khoản Google thì ghi vào spreadsheet CŨ hay MỚI?** | (a) kho FA-039 `TC-CB-155` + MT-09 (đã hỏi leader, **chờ quyết định**): *"sync vào **SPREADSHEET MỚI**, spreadsheet cũ KHÔNG nhận thêm dòng nào"*; (b) kho FA-011 `TC-FORM-370`: *"form đã có file Google thì **KHÔNG tạo file mới, vẫn map file cũ**"*; (c) **code sau fix 39089**: reconnect cùng email chỉ tạo yêu cầu cho form **chưa có** `google_sheet_id` ⇒ nghiêng về (b). ⚠️ Nếu (a) đúng thì dữ liệu của LINE OA mới tiếp tục chảy vào spreadsheet gắn với LINE OA cũ. | Leader + Dev |
| 2 | **Hủy liên kết Google rồi liên kết lại cùng tài khoản — giữ file cũ hay tạo file mới?** | Kho `TC-FORM-370` expected "giữ file cũ", nhưng Dev ghi hủy liên kết (`edit_v2` nhánh unlink) **xoá email** ⇒ lần liên kết lại không còn email cũ để so, rơi nhánh "email khác / lần đầu" (tạo mới cho mọi form). Một trong hai sai. | Dev |
| 3 | **Schema bảng lỗi đồng bộ `result_error_googles` chưa có trong spec** | `db-mapping.md` chỉ nhắc tên bảng; đoạn code vừa sửa reset `status` / `retry_time` / `next_time_retry` theo `type_result` nhưng không có spec để đối chiếu. | Dev bổ sung spec |
| 4 | **Hành vi UI khi Google trả lỗi ở callback connect** | Tab Thông tin Studio ghi *"Google exception → update bot status=0, log error, **không redirect** (silent fail — cần confirm UI behavior)"*. Chưa có spec nói màn hình phải hiện gì. | Leader + Dev |
