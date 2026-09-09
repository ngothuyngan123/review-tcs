<!-- sync-tcs: url=<chưa có — Redmine #39592 KHÔNG có "Link TCs" human> | sheet=<chưa có> | anchor=Main Function -->
<!-- source: MCP LME TEST STUDIO — task_id=69, ticket 39592, testcase_list (13 TC), fetch lúc 2026-08-13. Redmine KHÔNG có Link TCs human. -->

# 04 — TC List

## ⚠️ ĐỌC TRƯỚC — TCs này KHÔNG do member người viết

| Hạng mục | Giá trị |
|---|---|
| Nguồn | **MCP LME TEST STUDIO** — task `#69`, ticket `39592`, feature `detail-contract`, type `fix-bug` |
| Người viết TC | **`author = AI`** (toàn bộ 13/13 TC), `provenance.source = ai`, `created_job_id = 330` |
| Task added by | `hanhntb` — 2026-08-13 06:34 |
| Trạng thái task | `status = done-ai` · `pipelineStage = done-ai` · `aiResult = pass` · `round = 1` · `reviewed = false` · `reviewState = tester` |
| Chạy bởi | Task-level `runBy = pipeline` (2026-08-13 08:26, 78.85 phút). **Từng TC**: `last_exec.source = manual`, `by = anhptn` |
| Kết quả | **13/13 `Đạt`** — 0 fail, 0 error, 0 chưa chạy, `openBugs = 0` |
| Môi trường đã chạy | **`staging` — 13/13 TC** |
| `status` của TC | `draft` (13/13) — chưa được duyệt trên Studio |

### 🔴 Cảnh báo RULE-08 — bill tiền chạy toàn bộ trên STAGING

Task này thuộc nhóm **bill tiền / hóa đơn gửi khách**. Theo **RULE-08**, media · domain · job · loadbalance · **bill tiền** **không** được kết luận từ staging. Hiện **13/13 TC đều `env = staging`**, **0 TC chạy PRODUCTION** ⇒ kết quả `Đạt` chưa đủ để đóng ticket.

Đáng chú ý riêng `TC-DEPLOYASSET001-01` (Studio #10120): `env_scope` của chính TC này khai `["dev","staging","prd"]` và nội dung TC là **kiểm cache JS sau khi release** — nhưng vẫn chỉ được chạy ở `staging`, tức mục tiêu chính của TC chưa được kiểm ở môi trường thật.

### 🟠 Cảnh báo — độ tin cậy của kết quả `Đạt`

- Dev verify chỉ ở mức **`lint`**, chưa chạy trình duyệt thật (xem `03-dev-impact.md` §6). Toàn bộ bằng chứng đúng/sai dồn vào 13 TC này.
- 9/13 TC có `env_tag = local-only` hoặc `exec_mode = auto` nhưng `last_exec.source = manual` — cần confirm QA thật sự thao tác tay hay chỉ submit kết quả.
- **Evidence rỗng toàn bộ** — `testcase_list` không trả về evidence. Theo **RULE-02**, TC `Đạt` bắt buộc phải có evidence. Leader phải yêu cầu `anhptn` bổ sung file PDF / ảnh chụp cho ít nhất các TC trục chính.

### 🟡 Mã quan điểm Studio KHÔNG có trong `framework/checklist-lme.md`

`/review-tc` sẽ **không map được coverage** cho các mã dưới đây:

| Mã Studio | TC dùng | Ghi chú |
|---|---|---|
| `TOOL-KNOW-002` | TC-TOOLKNOW002-01 | Không thuộc 80 quan điểm tầng 1. Gần nhất: `REG-SPEC-001` / `FUNC-SEQ-001` |
| `SELECT-SCOPE-001` | TC-SELECTSCOPE001-01 | Không có. Gần nhất: `BULK-001` / `LIST-001` |
| `PERF-LATENCY-001` | TC-PERFLATENCY001-01 | Không có. Gần nhất: **`PERF-LARGE-001`** |
| `RULE-06` | TC-RULE06-01 | Đây là **RULE**, không phải mã quan điểm — không hợp lệ ở cột "Mã quan điểm liên kết". Gần nhất: `OUT-TRUTH-001` / `OUT-EXPORT-001` |

8 mã còn lại (`FUNC-SEQ-001`, `OUT-TRUTH-001`, `UI-003`, `DEPLOY-ASSET-001`, `CONC-003`, `FUNC-004`, `REG-SHARED-001`) khớp checklist tầng 1.

### Phân bố

| Chiều | Phân bố |
|---|---|
| `case_type` | **Normal 9** · **Abnormal 1** · **Boundary 3** |
| `tc_group` | `ui` — 13/13 (0 TC nhóm `api`) |
| `exec_mode` | `auto` 11 · `manual` 2 |
| `env_tag` | `local-only` 8 · `read-only` 4 · `env-safe` 1 |
| `screen` | `SCR-DC-09` Lịch sử thanh toán (12) · Chi tiết hợp đồng `/basic/detail-contract/{id}` (1) |
| `requirement_keys` | REQ-001 (8) · REQ-002 (2) · REQ-003 (1) · REQ-004 (3) · REQ-005 (3) · REQ-006 (1) · REQ-007 (1) · **REQ-008 (0 ❗)** · REQ-009 (1) · REQ-010 (1) · REQ-011 (1) |

**❗ REQ-008 không có TC nào** — *"Dữ liệu endpoint cấp cho biên lai phải đúng phạm vi tháng và số trang yêu cầu"* (category `api`, risk `Medium`). Đây là requirement duy nhất bị bỏ trống, và cũng là requirement khoanh vùng "lỗi nằm ở tầng hiển thị chứ không phải tầng dữ liệu".

### Ghi chú thêm

- `temp_id` có khoảng trống: NEW-2,3,4,5,**8**,**9**,**11**,**15**,**17**,**18**,**19**,**20**,**23** — thiếu NEW-6,7,10,12,13,14,16,21,22 ⇒ **9 TC đã bị xoá/gộp** trong quá trình AI sinh. Leader nên hỏi Studio xem các TC bị loại có phải trục quan trọng không.
- 3 TC có `version > 1` (#10105 v5, #10112 v2, #10116 v3) → đã qua chỉnh sửa; xem `testcase_get_history` nếu cần.

---

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `AI` (LME TEST STUDIO, job #330) — QA chạy: `anhptn` |
| Ngày submit | `2026-08-13` |
| Version TCs | `round 1` (Studio) |
| Link TC gốc (nếu có) | MCP LME TEST STUDIO — `task_id=69` |

---

## TC List

> **TCs dưới đây là READ-ONLY** — chép nguyên văn từ Studio, KHÔNG sửa title / precondition / steps / expected. Muốn sửa thì sửa trên Studio (`testcase_update`) rồi fetch lại.

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-TOOLKNOW002-01 | TOOL-KNOW-002 | Normal | Tái hiện lỗi khách báo: tải hóa đơn tháng 7 rồi tải tháng 6 trong cùng phiên | Tài khoản quản trị có phát sinh thanh toán ở CẢ tháng 6/2026 và tháng 7/2026, và tập giao dịch hai tháng phải khác nhau rõ ràng (khác số dòng, khác tên tài khoản LINE, khác tổng tiền) để phân biệt được bằng mắt. | 1. Mở màn 「決済履歴・領収書のダウンロード」 tại /basic/payment-history<br>2. Bấm 「詳細を確認 >」 ở dòng 「2026年07月分」<br>3. Bấm 「一括ダウンロード」, ở popup nhập 宛名 「株式会社トライズ」, chọn 「御中」, bấm 「領収書ダウンロード」 và chờ tải xong<br>4. KHÔNG tải lại trang, không bấm F5: quay lại bảng tổng hợp theo năm và bấm 「詳細を確認 >」 ở dòng 「2026年06月分」<br>5. Đối chiếu bảng chi tiết trên màn đang hiển thị đúng các giao dịch tháng 6<br>6. Bấm 「一括ダウンロード」, giữ nguyên 宛名, bấm 「領収書ダウンロード」 và chờ tải xong<br>7. Mở file vừa tải ở bước 6 và đối chiếu với bảng chi tiết tháng 6 trên màn | Lần 1: 2026年07月; lần 2: 2026年06月; 宛名 = 「株式会社トライズ」; 敬称 = 「御中」 | File tải ở lần thứ hai chứa ĐÚNG các giao dịch của tháng 6/2026: số dòng, từng dòng và tổng tiền khớp bảng chi tiết tháng 6 đang hiển thị. Không có dòng nào của tháng 7 lọt vào, tổng tiền không phải tổng của tháng 7, và số trang tính theo số giao dịch tháng 6. File lần thứ nhất vẫn đúng tháng 7. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10099 (NEW-2) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-001 · spec_ids=[TICKET-39592, SCR-DC-09, commit:233c4ae] · v1 · **Mã quan điểm không có trong checklist-lme.md** · **RULE-08: bill tiền nhưng chạy staging** · Note AI: "Đây là test case tái hiện đúng khiếu nại gốc của khách và cũng là bằng chứng cho việc gửi lại hóa đơn tháng 6 đúng. BẮT BUỘC thao tác trên trình duyệt thật và tuyệt đối không tải lại trang giữa hai lần tải — nếu reload thì lỗi không tái hiện được và kết quả pass là vô nghĩa. Cấm dùng cách gọi thẳng endpoint hoặc đọc mã nguồn thấy đã đổi sang v-if để kết luận pass." |
| TC-FUNCSEQ001-01 | FUNC-SEQ-001 | Normal | Tải hóa đơn cùng một tháng hai lần liên tiếp không nhân đôi và không thiếu dòng | Tài khoản quản trị có từ 3 giao dịch trở lên trong tháng 6/2026. | 1. Mở màn 「決済履歴・領収書のダウンロード」 và bấm 「詳細を確認 >」 ở dòng 「2026年06月分」<br>2. Bấm 「一括ダウンロード」 rồi bấm 「領収書ダウンロード」, chờ tải xong<br>3. KHÔNG tải lại trang, bấm tiếp 「一括ダウンロード」 rồi 「領収書ダウンロード」 lần thứ hai với cùng tháng<br>4. So sánh nội dung hai file vừa tải | Cùng tháng 2026年06月 cho cả hai lần tải | Hai file có nội dung giống hệt nhau: cùng số trang, cùng số dòng, cùng tổng tiền, không có dòng nào bị lặp lại hai lần và không có dòng nào bị thiếu. Ngày phát hành trên cả hai file là ngày thao tác. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10100 (NEW-3) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=[all] · REQ-001, REQ-005 · spec_ids=[SCR-DC-09, commit:233c4ae] · v1 · regression · Note AI: "Đối chứng cho chính cơ chế fix: việc huỷ rồi dựng lại khối biên lai mỗi lần tải không được sinh trùng node dẫn tới lặp dòng, cũng không được làm mất dòng khi dữ liệu hai lần tải giống nhau." |
| TC-OUTTRUTH001-01 | OUT-TRUTH-001 | Normal | Tải hóa đơn từng dòng cho hai dòng khác nhau liên tiếp ra đúng dòng tương ứng | Tháng 6/2026 có ít nhất 2 giao dịch với số tiền và tên tài khoản LINE khác nhau để phân biệt được. | 1. Mở màn 「決済履歴・領収書のダウンロード」 và bấm 「詳細を確認 >」 ở dòng 「2026年06月分」<br>2. Bấm công tắc 「個別発行」 để bảng hiện cột chọn và nút tải ở từng dòng<br>3. Ghi lại nội dung dòng thứ nhất và dòng thứ hai trên màn<br>4. Bấm nút tải ở CUỐI dòng thứ nhất, ở popup bấm 「領収書ダウンロード」, chờ tải xong<br>5. KHÔNG tải lại trang, bấm nút tải ở cuối dòng thứ hai, bấm 「領収書ダウンロード」, chờ tải xong<br>6. Đối chiếu nội dung hai file với hai dòng đã ghi ở bước 3 | Dòng 1 và dòng 2 của bảng chi tiết tháng 2026年06月 | File thứ nhất chỉ chứa đúng 1 giao dịch là dòng thứ nhất, tổng tiền bằng số tiền dòng đó. File thứ hai chỉ chứa đúng 1 giao dịch là dòng thứ hai, tổng tiền bằng số tiền dòng thứ hai — không phải dòng thứ nhất. Cả hai file đều 1 trang, không hiển thị đánh số trang. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10101 (NEW-4) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-002, REQ-001 · spec_ids=[SCR-DC-09, TICKET-39592] · v1 · **Đây là flow KH báo trong steps to reproduce (tab 個別発行)** · Note AI: "Bước điều tra chưa khẳng định chắc hai nút tải dùng chung một đường mã nguồn, nên phải test riêng nút tải từng dòng thay vì suy ra từ case tải hàng loạt." |
| TC-SELECTSCOPE001-01 | SELECT-SCOPE-001 | Normal | Tải hàng loạt theo các dòng đã tick rồi đổi lựa chọn tải lại ra đúng lựa chọn mới | Tháng 6/2026 có ít nhất 5 giao dịch với số tiền khác nhau. | 1. Mở màn 「決済履歴・領収書のダウンロード」, bấm 「詳細を確認 >」 ở dòng 「2026年06月分」, bấm công tắc 「個別発行」<br>2. Tick chọn dòng 1 và dòng 2, ghi lại tổng tiền hai dòng này<br>3. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」, chờ tải xong<br>4. KHÔNG tải lại trang: bỏ tick dòng 1 và dòng 2, tick chọn dòng 3, 4, 5 và ghi lại tổng tiền ba dòng này<br>5. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」 lần hai, chờ tải xong<br>6. Đối chiếu nội dung hai file với hai tập dòng đã tick | Lần 1: tick dòng 1-2; lần 2: tick dòng 3-4-5 của bảng chi tiết 2026年06月 | File thứ nhất chứa đúng 2 giao dịch của dòng 1 và 2, tổng tiền bằng tổng hai dòng đó. File thứ hai chứa đúng 3 giao dịch của dòng 3, 4, 5, tổng tiền bằng tổng ba dòng đó — không lẫn dòng 1, 2 và không giữ lại tổng tiền của lần tải trước. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10102 (NEW-5) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-002, REQ-004 · spec_ids=[SCR-DC-09] · v1 · **Mã quan điểm không có trong checklist-lme.md** · Note AI: "Phủ đồng thời phạm vi lựa chọn (nội dung file phải khớp tuyệt đối tập đã tick) và trục tải liên tiếp trong cùng phiên." |
| TC-OUTTRUTH001-02 | OUT-TRUTH-001 | Normal | Đổi tên người nhận và kính ngữ giữa hai lần tải không giữ giá trị cũ | Tài khoản có giao dịch trong tháng 6/2026. | 1. Mở tháng 6/2026.<br>2. Tải lần 1 với 宛名「株式会社テストA」, 敬称「御中」.<br>3. Không reload trang.<br>4. Tải lần 2 với 宛名「山田太郎」, 敬称「様」.<br>5. Mở file lần 2 và đối chiếu. | Lần 1: 株式会社テストA + 御中<br>Lần 2: 山田太郎 + 様 | File lần 2 hiển thị 「山田太郎 様」, không giữ tên/kính ngữ của lần 1.<br>Dữ liệu giao dịch vẫn đúng tháng 6/2026. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10105 (NEW-8) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=[all] · REQ-010 · spec_ids=[SCR-DC-09] · **v5 — đã sửa nhiều lần** · Note AI: "Kiểm phần đầu biên lai được dựng lại theo lựa chọn hiện tại, không giữ nội dung cũ — cùng root cause với bug nhưng ở vùng khác của trang biên lai. Đã gộp biến thể ký tự đặc biệt tiếng Nhật vào dữ liệu nhập thay vì tạo case riêng, vì biên lai được chụp thành ảnh nên lỗi font là rủi ro có thật." |
| TC-UI003-01 | UI-003 | Normal | Sau khi tải xong màn hình trở về trạng thái sạch, không còn khối biên lai trên trang | Tài khoản có giao dịch trong tháng 6/2026. | 1. Mở màn 「決済履歴・領収書のダウンロード」, bấm 「詳細を確認 >」 ở dòng 「2026年06月分」<br>2. Chụp lại giao diện màn hình trước khi tải<br>3. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」, chờ tới khi file được tải xong<br>4. Quan sát màn hình ngay sau khi file tải xong và cuộn hết trang<br>5. Chụp lại giao diện và so sánh với ảnh ở bước 2 | Tháng 2026年06月 | Ngay sau khi tải xong: popup 「領収書ダウンロード設定」 tự đóng, lớp phủ đang tải biến mất, bảng chi tiết tháng 6 vẫn hiển thị bình thường và có thể thao tác tiếp. Khối biên lai dùng để chụp ảnh không còn xuất hiện trên trang và không để lại khoảng trắng thừa, thanh cuộn hay phần tử chồng lấn; giao diện khớp với ảnh chụp trước khi tải. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10106 (NEW-9) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=[all] · REQ-007 · spec_ids=[SCR-DC-09, commit:233c4ae] · v1 · regression (hệ quả v-show→v-if) · Evidence bắt buộc: 2 ảnh chụp màn trước/sau · Note AI: "Kiểm hệ quả trực tiếp của việc chuyển từ ẩn node sang huỷ node: trước đây khối biên lai vẫn nằm trong DOM sau khi tải, nay bị gỡ hẳn, nên cần xác nhận không phát sinh nhảy layout hay khoảng trắng." |
| TC-RULE06-01 | RULE-06 | Normal | Mở file biên lai vừa tải bằng mắt để xác nhận đầu ra cuối chuỗi | Đã chạy xong kịch bản tái hiện lỗi (tải tháng 7 rồi tháng 6 trong cùng phiên) và còn giữ hai file vừa tải. | 1. Mở file tải ở lần thứ nhất bằng trình xem PDF<br>2. Mở file tải ở lần thứ hai bằng trình xem PDF<br>3. Đối chiếu bằng mắt tiêu đề 「領収書」, tên người nhận, ngày phát hành, bảng 内訳 và các con số tổng của từng file với bảng tương ứng trên màn<br>4. Kiểm chữ tiếng Nhật trong file có hiển thị rõ, không vỡ chữ, không mất ký tự | Hai file 「領収書.pdf」 của tháng 7/2026 và tháng 6/2026 | File thứ hai hiển thị đúng nội dung tháng 6/2026 khi xem bằng mắt, không phải nội dung tháng 7. Chữ tiếng Nhật rõ nét, không lỗi font, bảng 内訳 không bị cắt mất cột, các con số tổng đọc được và khớp bảng trên màn. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10108 (NEW-11) · tc_group=ui · **exec_mode=manual** · env_tag=read-only · env_scope=[all] · REQ-001, REQ-004 · spec_ids=[TICKET-39592, SCR-DC-09] · v1 · **"RULE-06" là RULE chứ không phải mã quan điểm — cột này không hợp lệ** · Evidence bắt buộc: file PDF thật · Note AI: "Bắt buộc manual: mỗi trang biên lai được tạo bằng cách chụp khối HTML thành ảnh rồi chèn vào PDF, nên file không có lớp text để so khớp tự động — chất lượng hiển thị và lỗi font chỉ xác nhận được bằng mắt." |
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Normal | Sau khi phát hành bản fix, chỉ tải lại trang bình thường vẫn nhận bản mới và tải hóa đơn đúng | Có môi trường đang chạy bản CŨ (chưa có fix) và kế hoạch phát hành bản fix lên chính môi trường đó. Tài khoản có giao dịch ở tháng 6/2026 và tháng 7/2026. | 1. Trước khi phát hành: mở màn 「決済履歴・領収書のダウンロード」 bằng bản cũ và thực hiện một lần tải hóa đơn để trình duyệt lưu cache toàn bộ tệp giao diện<br>2. Giữ nguyên tab đó, không đóng trình duyệt và không xóa cache<br>3. Phát hành bản fix lên môi trường<br>4. Trên chính tab cũ, bấm F5 thường (KHÔNG dùng Ctrl+F5 hay xóa cache)<br>5. Mở tab công cụ dành cho nhà phát triển, thẻ Network, đối chiếu đường dẫn và nội dung tệp giao diện của luồng hóa đơn xem đã là bản mới chưa<br>6. Chạy lại kịch bản tải hóa đơn tháng 7 rồi tháng 6 trong cùng phiên và kiểm nội dung file thứ hai | Tab trình duyệt giữ cache bản cũ; sau phát hành chỉ F5 thường | Sau khi F5 thường, trình duyệt nạp đúng tệp giao diện của bản mới (đường dẫn tệp kèm tham số phiên bản đã thay đổi hoặc nội dung tệp đã là bản mới), không có lỗi JavaScript trên console, màn hình hiển thị đầy đủ. Kịch bản tải hóa đơn tháng 7 rồi tháng 6 cho kết quả đúng: file thứ hai chứa nội dung tháng 6. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10120 (NEW-23) · tc_group=ui · **exec_mode=manual** · env_tag=env-safe · **env_scope=[dev,staging,prd] nhưng chỉ chạy staging → chưa verify được mục tiêu của TC** · REQ-011, REQ-001 · spec_ids=[TICKET-39592, SCR-DC-09, source: config/sns-line.php:62] · v1 · Note AI: "LƯU Ý QUAN TRỌNG CHO LEADER: tệp JS của luồng này được nhúng kèm tham số phiên bản lấy từ cấu hình ứng dụng, mà commit fix KHÔNG thay đổi giá trị cấu hình đó. Template blade do máy chủ dựng nên tới người dùng ngay, nhưng tệp JS có thể vẫn là bản cache cũ. Nếu quy trình phát hành không tự tăng số phiên bản thì phải yêu cầu dev tăng trước khi lên bản chính thức; test case này chính là chỗ phát hiện điều đó." |
| TC-CONC003-01 | CONC-003 | Abnormal | Đổi tháng và tải tiếp khi lần tải trước chưa xong không được ra file trộn hai tháng | Tháng 6/2026 và tháng 7/2026 đều có giao dịch, tập dữ liệu hai tháng khác nhau rõ ràng. Có công cụ làm chậm mạng để request lấy dữ liệu mất khoảng 3-5 giây. | 1. Bật chế độ mạng chậm cho request lấy lịch sử thanh toán<br>2. Mở màn 「決済履歴・領収書のダウンロード」, bấm 「詳細を確認 >」 ở dòng 「2026年07月分」<br>3. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」<br>4. Trong lúc lớp phủ đang tải còn hiển thị, chuyển ngay sang 「2026年06月分」 và bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」 lần nữa<br>5. Chờ mọi tiến trình kết thúc, kiểm toàn bộ file đã tải về | Lần 1: 2026年07月 (mạng chậm); lần 2: 2026年06月 chèn vào khi lần 1 chưa xong | Không file nào được chứa dữ liệu trộn giữa tháng 7 và tháng 6.<br>Nếu thao tác thứ hai được hệ thống chấp nhận, receipt tương ứng phải chứa trọn vẹn đúng dữ liệu của tháng được yêu cầu.<br>Sau khi các request hoàn tất, popup/loading phải kết thúc và màn hình tiếp tục thao tác được. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10112 (NEW-15) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-009, REQ-001 · spec_ids=[SCR-DC-09, commit:233c4ae] · v2 · **TC Abnormal DUY NHẤT của cả bộ** · Note AI: "Rủi ro còn lại của bản fix: mã nguồn không xếp hàng hay huỷ request cũ, mỗi response về đều tự gán dữ liệu và kích hoạt dựng biên lai. Nếu case này lộ ra file trộn dữ liệu thì đó là biến thể chưa được xử lý của chính bug gốc, cần báo cho dev thay vì bỏ qua." |
| TC-FUNC004-01 | FUNC-004 | Boundary | Biên lai của tháng có 11 giao dịch ra 2 trang đúng bố cục | Dựng dữ liệu để tháng thử nghiệm có ĐÚNG 11 giao dịch thanh toán, số tiền khác nhau để phân biệt thứ tự dòng. | 1. Mở màn 「決済履歴・領収書のダウンロード」 và mở chi tiết tháng đã dựng 11 giao dịch<br>2. Xác nhận bảng chi tiết trên màn hiển thị đúng 11 dòng<br>3. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」, chờ tải xong<br>4. Kiểm từng trang của file | Tháng có đúng 11 giao dịch | File có đúng 2 trang. Trang 1 chứa 10 dòng đầu, hiển thị 「1/2ページ」, có ô 合計金額 và dòng 「次ページに続く」. Trang 2 chứa 1 dòng còn lại, hiển thị 「2/2ページ」 và dòng 合計 bằng tổng của cả 11 giao dịch (không phải tổng riêng của trang 2). Tổng số dòng trên hai trang bằng 11, không lặp và không thiếu dòng nào. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10114 (NEW-17) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-005, REQ-004 · spec_ids=[SCR-DC-09, source: UserController.php handleTotalPagePdf] · v1 · Note AI: "Biên trên của trang đầu: vượt 10 giao dịch là sinh trang thứ hai chứa tối đa 20 giao dịch. Lưu ý dev đã ghi nhận lỗi có sẵn về thứ tự trang với biên lai nhiều trang — nếu gặp sai thứ tự, báo issue riêng, không đánh trượt ticket này." |
| TC-FUNCSEQ001-02 | FUNC-SEQ-001 | Boundary | Tải tháng nhiều trang rồi tải tháng ít trang không để lại trang thừa | Dựng dữ liệu: tháng A có 25 giao dịch (2 trang), tháng B có 3 giao dịch (1 trang), hai tháng trong cùng một năm. | 1. Mở màn 「決済履歴・領収書のダウンロード」 và mở chi tiết tháng A (25 giao dịch)<br>2. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」, chờ tải xong và ghi lại số trang<br>3. KHÔNG tải lại trang: mở chi tiết tháng B (3 giao dịch)<br>4. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」, chờ tải xong<br>5. Kiểm số trang và nội dung file thứ hai<br>6. Lặp lại theo chiều ngược lại: tải tháng B trước rồi tháng A, kiểm file của tháng A | Tháng A: 25 giao dịch; tháng B: 3 giao dịch | File của tháng B có đúng 1 trang với 3 dòng, không kèm trang trắng hay trang chứa dòng của tháng A, tổng tiền bằng tổng 3 giao dịch tháng B. Ở chiều ngược lại, file của tháng A có đúng 2 trang với đủ 25 dòng, không bị cắt bớt còn 1 trang theo lần tải trước. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10115 (NEW-18) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-005, REQ-001 · spec_ids=[TICKET-39592, SCR-DC-09, commit:233c4ae] · v1 · Note AI: "Trục số trang giao với trục tải liên tiếp: đây là kịch bản dễ lộ ra node trang cũ còn sót nhất, vì số lượng phần tử trang thay đổi giữa hai lần tải." |
| TC-PERFLATENCY001-01 | PERF-LATENCY-001 | Boundary | Biên lai nhiều trang của tháng nhiều giao dịch dựng xong trong ngưỡng chờ, không treo màn hình | Có tháng đủ nhiều giao dịch để receipt sinh ít nhất 3 trang. | 1. Mở màn 「決済履歴・領収書のダウンロード」 và mở chi tiết tháng có khoảng 100 giao dịch<br>2. Bấm 「一括ダウンロード」 rồi 「領収書ダウンロード」 và bấm giờ từ lúc bấm<br>3. Theo dõi màn hình liên tục cho tới khi có file hoặc tới khi quá 30 giây<br>4. Kiểm số trang và số dòng của file<br>5. KHÔNG tải lại trang, lặp lại lần tải thứ hai với cùng tháng và theo dõi tương tự | Tháng có khoảng 100 giao dịch (biên lai khoảng 6 trang) | Không có trang nào bị timeout khi chờ render.<br>File được tạo đủ số trang/dòng; popup và loading kết thúc bình thường.<br>Không xuất hiện cảnh báo timeout của waitForElement trong console. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10116 (NEW-19) · tc_group=ui · exec_mode=auto · env_tag=local-only · env_scope=[local,dev,staging] · REQ-006 · spec_ids=[SCR-DC-09, redmine: journal mục TỰ REVIEW] · v3 · **Mã quan điểm không có trong checklist-lme.md (gần nhất: PERF-LARGE-001)** · Evidence bắt buộc: log console + thời gian đo · Note AI: "Dev tự cảnh báo danh sách dài dựng DOM lâu hơn. Điểm gãy cụ thể: cơ chế đợi phần tử chỉ chờ tối đa 5 giây cho mỗi trang, quá ngưỡng thì chỉ ghi cảnh báo ra console và dừng, khiến tiến trình chờ toàn bộ trang không bao giờ hoàn tất nên lệnh lưu file, đóng popup và tắt lớp phủ đều không chạy." |
| TC-REGSHARED001-01 | REG-SHARED-001 | Normal | Tải biên lai hai lần liên tiếp trên màn Chi tiết hợp đồng vẫn ra đúng nội dung | Tài khoản có một hợp đồng đang hoạt động với ít nhất 2 kỳ thanh toán trong quá khứ. | 1. Mở màn danh sách hợp đồng rồi vào chi tiết một hợp đồng có lịch sử thanh toán<br>2. Bấm nút 「過去決済分の領収書ダウンロード」<br>3. Ở popup 「領収書ダウンロード設定」, nhập 宛名 「株式会社テストＡ」, chọn 「御中」, bấm 「領収書ダウンロード」, chờ tải xong<br>4. KHÔNG tải lại trang: bấm lại 「過去決済分の領収書ダウンロード」, đổi 宛名 thành 「株式会社テストＢ」, bấm 「領収書ダウンロード」, chờ tải xong<br>5. So sánh nội dung hai file | Lần 1: 宛名 「株式会社テストＡ」; lần 2: 宛名 「株式会社テストＢ」; cùng một hợp đồng | Cả hai file đều chứa đúng và đủ lịch sử thanh toán của hợp đồng đang xem, số dòng và tổng tiền giống nhau, không dòng nào bị lặp hay bị thiếu. File thứ hai hiển thị 「株式会社テストＢ 御中」 chứ không phải tên của lần tải thứ nhất. Sau mỗi lần tải, popup đóng, lớp phủ đang tải tắt và trang chi tiết hợp đồng không bị chèn thêm khối biên lai. | Đạt | | STAGING | anhptn | 2026-08-13 | | | Studio #10117 (NEW-20) · tc_group=ui · exec_mode=auto · env_tag=read-only · env_scope=[all] · REQ-003, REQ-001 · spec_ids=[TICKET-39592, SCR-DC-01, source: bill/detail.blade.php:539] · v1 · **TC DUY NHẤT cover màn T2 (Chi tiết hợp đồng /basic/detail-contract/{id})** · regression · Note AI: "Màn này dùng chung đúng template biên lai và mixin đã sửa nên bắt buộc có test case thực thi riêng, không được suy ra kết quả từ màn Lịch sử thanh toán." |

---

## Requirements từ Studio (đối chiếu coverage với `03-dev-impact.md`)

| REQ | Risk | Category | Tiêu đề | TC cover |
|---|---|---|---|---|
| REQ-001 | High | ui | Biên lai tải lần thứ hai trở đi trong cùng phiên phải khớp đúng tháng vừa chọn | TC-TOOLKNOW002-01, TC-FUNCSEQ001-01, TC-OUTTRUTH001-01, TC-RULE06-01, TC-DEPLOYASSET001-01, TC-CONC003-01, TC-FUNCSEQ001-02, TC-REGSHARED001-01 |
| REQ-002 | High | ui | Tải từng dòng và tải theo lựa chọn phải khớp đúng dòng đã chọn ở mỗi lần bấm | TC-OUTTRUTH001-01, TC-SELECTSCOPE001-01 |
| REQ-003 | High | ui | Màn Chi tiết hợp đồng dùng chung template phải hết lỗi tương tự | TC-REGSHARED001-01 |
| REQ-004 | High | ui | Nội dung biên lai phải khớp bảng hiển thị trên màn ở mọi cột và mọi con số tổng | TC-SELECTSCOPE001-01, TC-RULE06-01, TC-FUNC004-01 |
| REQ-005 | High | ui | Số trang biên lai phải đúng quy tắc chia trang và không thừa trang của lần tải trước | TC-FUNCSEQ001-01, TC-FUNC004-01, TC-FUNCSEQ001-02 |
| REQ-006 | Medium | ui | Biên lai nhiều trang phải dựng xong trong ngưỡng chờ, không treo màn hình | TC-PERFLATENCY001-01 |
| REQ-007 | Medium | ui | Trạng thái màn hình sau khi tải xong phải sạch, không để lại khối biên lai trên trang | TC-UI003-01 |
| **REQ-008** | **Medium** | **api** | **Dữ liệu endpoint cấp cho biên lai phải đúng phạm vi tháng và số trang yêu cầu** | **❗ KHÔNG CÓ TC** |
| REQ-009 | Medium | ui | Thao tác bất thường không được sinh biên lai sai hoặc báo thành công giả | TC-CONC003-01 |
| REQ-010 | Medium | ui | Thông tin đầu biên lai phải lấy theo lựa chọn của lần tải hiện tại | TC-OUTTRUTH001-02 |
| REQ-011 | Medium | ui | Sau khi phát hành bản fix, người dùng chỉ tải lại trang bình thường vẫn phải chạy bản mới | TC-DEPLOYASSET001-01 |

> REQ-009 khai 4 kịch bản bất thường (*chưa chọn dòng nào* · *request lấy dữ liệu thất bại* · *bấm liên tiếp nút tải* · *đổi tháng lúc lần tải trước chưa xong*) nhưng chỉ có **1 TC** (TC-CONC003-01) cover kịch bản cuối. 3 kịch bản còn lại chưa có TC.

---

## Member tự check trước khi submit

> Bộ TC này do **AI sinh trên Studio**, không qua bước member tự check. Các mục dưới để Leader đánh giá khi chạy `/review-tc`.

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC** verify tính năng cũ không hỏng cho mỗi tính năng trong 4.3 (ghi "regression" ở Ghi chú)
- [ ] Có **ít nhất 1 Abnormal + 1 Boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC có `Mã quan điểm liên kết`, steps rõ ràng, `Kết quả mong đợi` đo lường được
- [ ] `Tiêu đề test case` chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base quan điểm test LME (2 tầng)

**Tầng 1 — quan điểm**: [framework/checklist-lme.md](../../framework/checklist-lme.md) (80 quan điểm + 12 RULE).
**Tầng 2 — catalog**: [framework/catalog-lme.md](../../framework/catalog-lme.md).

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã tra | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| `<Studio không trả về test_viewpoint_selection — null. Leader duyệt lại tầng 1 khi chạy /review-tc>` | | | | | |

- [ ] Đã duyệt **toàn bộ** tầng 1 từ trên xuống, không bỏ nhóm nào
- [ ] Mỗi quan điểm ◯ **đã mở đúng catalog** ở tầng 2 và **duyệt hết** khối tương ứng
- [ ] Mọi quan điểm ◯ ưu tiên **Cao** có đủ 3 loại case Normal + Abnormal + Boundary (**RULE-01**)
- [ ] Mọi × đều có lý do; × ở quan điểm **Cao** đã báo Leader duyệt (**RULE-03**)
- [ ] TC có output ra ngoài → `Kết quả mong đợi` đi tới **output cuối trên thiết bị thật** (**RULE-06**)
- [ ] TC CRUD verify đủ **3 tầng** DB + màn hình + output (**RULE-07**)
- [ ] Task chạm **media / domain / job / loadbalance / bill tiền** → có TC ghi `Môi trường test = PRODUCTION` (**RULE-08**) — ❌ **hiện 0/13**
- [ ] Task chạm đối tượng đã từng version-up → test **cả nhánh cũ và mới** (**RULE-09**)
- [ ] Mỗi TC đã ghi **loại evidence bắt buộc** ở Ghi chú (**RULE-02**) — ❌ **Evidence rỗng 13/13**
- [ ] Mọi TC có `Trạng thái đánh giá spec` — ❌ **`spec_status = null` 13/13, cột để trống**
