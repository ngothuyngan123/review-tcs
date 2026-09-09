# 05 — Review Report (draft cho Leader verify)

## Thông tin

| Trường | Giá trị |
|---|---|
| Task folder | `tasks/2026-08-27_28418_talk-list-sau-khi-change-1-status-thi-ko/` |
| Ticket | Redmine #28418 — [Talk-list] Sau khi change 1 status thì ko change tiếp được |
| Feature | **FA-002 — Quản lý chat 「チャット管理」** (`/basic/talk-list`) |
| Người review | Claude (`/review-tc`) — **draft, Leader phải verify** |
| Ngày review | 2026-08-27 |
| Vòng review | 1 |

---

## 0. Nguồn TC

| Mục | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, `task_id = 175` |
| Ticket Studio | 28418 · feature `talk` · type `fix-bug` · branch `ai_fixbug_28418` · round `1` · `archived = false` |
| Thời điểm fetch | 2026-08-27 (re-verify `task_list` ngay đầu phiên review — `exec` không đổi so với lúc `/new-task`) |
| **Tổng TC lấy về** | **22** |
| Status Studio | `done-ai` · **`aiResult = fail`** · `reviewState = leader` · **`reviewed = false`** · `openBugs = 0` · `submittedWithoutMcp = false` |
| Nguồn 2 (Sheet human) | **Không dùng** — đã dừng ở nguồn 1 (có TC). Human không cung cấp link; không tự đi tìm. |
| Nguồn 3 (file `04-tc-list.md`) | **Không dùng làm nguồn** — đã dừng ở nguồn 1. |
| Đối chiếu chéo nguồn | **KHÔNG** — theo quy tắc dừng ở nguồn đầu tiên có TC. |
| Snapshot đã ghi | **Không ghi đè** — `04-tc-list.md` đã có header `<!-- source: MCP LME TEST STUDIO — task_id=175 ... -->` (snapshot do `/new-task` sinh cùng ngày) và nội dung **trùng khớp** bản fetch mới (exec 17/4/1 không đổi) → refresh là no-op, giữ nguyên file. |
| **Nguồn spec đã dùng** | **Nguồn #1 — `spec-features/admin/chat-management/feature-spec.md`** (spec reverse-engineer từ source, FA-002). Folder **không có `02-spec-reference.md`** → đọc thẳng theo thứ tự ưu tiên, không tạo file 02. Trích dùng: BR-01…BR-11 (§5 Business Rules), §4.3 Actions (mục 18/19), §"Kiến trúc Confirm/Unconfirm", §"Kiến trúc Message Sharding". Không cần tra tới nguồn #2 (lme.jp/manual) hay #3 (Confluence). Mục lục tra `FA-002` lấy từ `templates/LME-SYSTEM-SPEC.md` §3.3. |
| Review comment vòng trước | `review_list_comments(task_id=175)` → **rỗng**, chưa có comment nào. Không có issue cũ để tránh raise lại. |

### 0.6 — Cảnh báo bắt buộc về chất lượng nguồn

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| **1** | **Kết quả thực thi thật** | `pass` **17/22 = 77.3%** · `fail` 4 · chưa chạy 1. **< 80%** | **`[MAJOR]`** — xem M-01 |
| **2** | **TC fail / gắn ticket bug** | 4 TC fail, **cả 4 đều đã raise ticket** (#40275, #40276, #40277, #40278 ⇄ Studio bug #670, #669, #668, #671). **Không có TC fail nào chưa raise ticket** | ✅ không BLOCKER ở mục này |
| **3** | **Môi trường đã chạy** | **local: 2 run** (#401, #660) · **staging: 1 run (#664) — `status = running`, khởi động 06:35:32, CHƯA có kết quả** · **dev: 0** · **prd: 0**. Task chạm **asset/deploy** (`DEPLOY-ASSET-001`) và **race tầng client** | **`[MAJOR]` RULE-08 / ENV-003** — xem M-02 |
| **4** | **Ai chạy** | 21/21 TC đã chạy đều `last_exec.source = "ai"` (pipeline AI, `by = trangnq`). **Run manual #665 (local) kết thúc với `status = error`: "Kết thúc mà chưa nhập kết quả TC nào trong lần test này", counts = 0/0/0/0** → **QA người CHƯA nghiệm thu tay bất kỳ TC nào** | **`[MAJOR]`** — xem M-04 |
| **5** | **Tác giả TC** | **19/22 (86%) do AI sinh** (`provenance.source = ai`, `createdJobId = 505`); 3 TC do người (`trangnq@mcp`, 2026-08-26). `reviewState = leader`, **`reviewed = false`** | **`[MAJOR]`** — xem M-03 |
| **6** | **Mã quan điểm ngoài `framework/checklist-lme.md`** | **4/10 mã** không tồn tại trong `framework/` (grep cả `checklist-lme.md` + `catalog-lme.md`): `SELECT-SCOPE-001` (11 TC) · `TOOL-KNOW-002` (1) · `TOOL-NEGCTRL-001` (1) · `API-CONTRACT-001` (2) → **15/22 TC (68%)** | **`[MAJOR]`** — các TC này **KHÔNG được tính là cover quan điểm** ở BƯỚC 2/3b. Xem M-05 |

> ⚠️ Toàn bộ kết luận pass/fail hiện tại **chỉ đến từ env `local`**. Run staging #664 treo ở trạng thái `running` hơn 20 phút (khởi động 06:35:32; run manual #665 đã kết thúc lúc 06:58:42 mà #664 vẫn chưa xong) → **nghi treo, cần kiểm tra lại trước khi dùng kết quả**.

---

## 1. Verdict

# ❌ REJECTED

Có **5 `[BLOCKER]`**. Bộ TC **không đủ cơ sở** để kết luận #28418 đã fix đạt.

Lý do cô đọng:
1. 1 TC có **`Kết quả mong đợi` trái spec** (BR-07) — TC đã bị nới lỏng để khớp hành vi lỗi quan sát được ở run #401.
2. 4 GAP ở quan điểm **ưu tiên Cao** trigger khớp task mà **0 TC** cover.
3. REQ-003 (risk **High**) chỉ **2/3 phạm vi chọn** hoạt động — nhánh 「全N件選択」 hỏng hoàn toàn (HTTP 500).

---

## 2. Tóm tắt cho member

**Điểm tốt** — bộ TC bám root cause rất sát: 5 TC quét đủ các đường nạp lại danh sách (`次へ` / bộ lọc nhanh / tìm kiếm / bộ lọc nâng cao / khoảng ngày), có đối chứng âm (NEW-5) và 2 case biên 0-phần-tử. Ghi chú kỹ thuật trong mỗi TC nêu rõ oracle ở cả tầng request lẫn tầng dữ liệu — hiếm khi thấy ở TC AI sinh. 3 TC người bổ sung (NEW-20/21/22) nhắm đúng các biến thể stale-selection còn thiếu.

**Điểm phải fix** — bộ TC đang **kiểm rất kỹ 1 code path (`initData`) và gần như bỏ trống mọi thứ xung quanh nó**: không có TC nào cho race tầng giao diện (`CONC-003`, màn này có loadmore + filter nên quan điểm này là **Cao**), không có TC nào kiểm `WHERE` scope trên **2 bot** (`DATA-DB-001`, bắt buộc với mọi UPDATE/DELETE), không có TC nào cho **tin nhắn cũ ở bảng shard legacy** (`COMPAT-LEGACY-001`), và **không có TC nào đi tới output cuối là badge trên mobile app** dù spec ghi rõ thao tác này bắn **FCM push** (BR-07). Quan trọng nhất: **`03-dev-impact.md` khai "không có data impact" là sai** — spec §4.3 liệt kê 6 bảng/cột bị ghi, nên coverage được dựng trên một base thiếu.

---

## 3. Coverage Matrix

> Impact lấy từ `03-dev-impact.md`. Cột `Exec` = `<số pass>/<số TC cover>` (nguồn Studio, run #660 env `local`).

| Impact | Loại | Priority Dev | TCs cover (suy luận) | # TC | Exec | Status |
|---|---|---|---|---|---|---|
| **BUG** — `allMessage` không reset trong `initData()` → tick lại tin cũ bị hiểu là bỏ chọn | Fix | — | TC-TOOLKNOW002-01 (tái hiện đúng steps file 01), TC-FUNCSEQ001-02 | 2 | 2/2 | **OK** ⚠️ chỉ local |
| **F1** — `talk_list.initData` (`public/js/talk_list/index.js`) | Function | **Direct** | TC-SELECTSCOPE001-01, -02, -03, -04, -05, -06, -07 | 7 | 6/7 | **OK** |
| **F2** — Số phiên bản asset (`config/sns-line.php`) | Function | **Direct** | TC-DEPLOYASSET001-01 (**fail**), TC-DATACACHE001-01 (**chưa chạy**), TC-REGSHARED001-01 (chỉ diff tĩnh) | 3 | 1/3 | **RISK** — 2 TC hành vi thật đều không có kết luận; TC pass duy nhất là kiểm tra tĩnh mã nguồn, không chứng minh asset tới được browser |
| **F3** — `talk_list.changStatus` (guard `allMessage.length == 0`) | Function | Indirect | TC-TOOLKNOW002-01, TC-SELECTSCOPE001-10, -11, TC-TOOLNEGCTRL001-01 | 4 | 4/4 | **OK** |
| **F4** — handler change `.check_msg` / `#checkAll` / `#checkAllPage` | Function | Indirect | TC-SELECTSCOPE001-08, -09, -10, -11 | 4 | 4/4 | **OK** |
| **D1** — Dev khai **"Không có data impact"** | Data | — | — | — | — | ⚠️ **KHAI SAI** — xem §3 "Data impact ẩn" bên dưới |
| **T1** — Chat / Talk Management (FA-002), đổi trạng thái hàng loạt | Feature | **High** | 19 TC nhóm `ui` | 19 | 15/18 | **RISK** — thiếu: tin legacy shard, 「返信を含める」 (msg_kind hỗn hợp), tin media/sticker bị ẩn mặc định (BR-04), cách ly đa bot |
| **T2** — **Toàn bộ màn dùng chung số phiên bản asset** | Feature | Medium | TC-REGSHARED001-01 (chỉ đối chiếu diff, **không mở màn nào khác**) | 1 | 1/1 | **GAP** — 0 TC mở **bất kỳ màn khác** sau khi nâng version để xác nhận không hỏng |

### ⚠️ Data impact ẩn — `03-dev-impact.md` mục 4.2 khai thiếu

Dev khai *"Không có — fix thuần giao diện, không đổi cấu trúc hay dữ liệu bảng nào"*. Đúng ở nghĩa **"bản vá không sửa schema"**, nhưng **luồng nghiệp vụ bị test thì ghi vào 6 bảng/cột**. Theo `spec-features/admin/chat-management/feature-spec.md` §4.3 (mục 18, 19) + BR-01/06/07:

| Data thật sự bị ghi | Thao tác | TC nào cover? | Status |
|---|---|---|---|
| `unconfirm_message` | DELETE (確認済) / INSERT (未確認) | Nhiều TC (nêu ở `Ghi chú` dạng "dữ liệu chưa xác nhận") | **OK** |
| `bots.count_user_unconfirm` | UPDATE | TC-OUTTRUTH001-01 (chỉ badge sidebar) | **RISK** |
| `conversation.confirm_count` | UPDATE | — (suy gián tiếp qua badge) | **RISK** |
| `conversation.status_last_message` | UPDATE | — | **GAP** |
| `sync_elasticsearch` (BR-06) | INSERT | **— 0 TC** | **GAP** → M-08 |
| `messages.is_confirmed` (legacy, BR-02/§4.3 #19) | UPDATE | **— 0 TC** | **GAP** → B-04 |

### ORPHAN TCs

| TC No. | Nhận xét | Kết luận |
|---|---|---|
| TC-APICONTRACT001-01 / -02 (NEW-17, NEW-18) | Gọi thẳng endpoint EP-06 — **backend KHÔNG bị bản vá chạm** (dev xác nhận). Đây là biểu hiện **AP-5 (layer-downstream over-coverage)** | **KHÔNG phải orphan cần xóa** — Studio đã note đúng là "regression, không phải acceptance của #28418", và -02 đã phát hiện bug thật severity High. **Đề nghị tách sang ticket riêng**, không dùng để gate #28418 → `[MINOR]` m-02 |
| TC-REGSHARED001-01 (NEW-19) | Là **kiểm tra tĩnh mã nguồn** (`git diff`, đếm file, xem có migration không) — không phải TC manual tester dựng env chạy được | Re-label thành mục **code-review checklist**, không tính là TC coverage của F2/T2 → `[MINOR]` m-01 |

Không có TC nào lạc hoàn toàn ngoài scope BUG / F* / T*.

---

## 3.5 Fix-shape analysis (adversarial)

**Fix shape nhận diện**: kết hợp **2 shape**
1. **`"JS" / "asset" / "build"`** — nâng số version asset trong `config/sns-line.php` (file cấu hình **dùng chung toàn hệ thống**).
2. **`"sửa hàm dùng chung"` (một phần)** — `config/sns-line.php` là shared config; dev có claim quét ngang nhưng **không kèm bằng chứng**.

*(Không thuộc shape "generic catch" / "validate input" / "race condition" / "migration" — bản vá là 1 dòng reset mảng state phía client.)*

| Câu hỏi adversarial bắt buộc | Trả lời từ bộ TC hiện tại | Kết luận |
|---|---|---|
| Test **F5 thường** (không Ctrl+F5) trên browser còn cache bản cũ? | **Có** — TC-DEPLOYASSET001-01. Nhưng TC này **FAIL** và chỉ chạy ở `local`, tức **chưa từng chạy trên một lần deploy thật** | **`[MAJOR]`** M-02, M-16 |
| Network tab có asset 404 không? | Có trong steps TC-DEPLOYASSET001-01 | OK (nhưng chưa có verdict thật) |
| DEPLOY-ASSET-001 mục (5) **font không fallback** (glyph kanji/kana + dấu tiếng Việt, không tofu ロ) | **0 TC** | **`[MAJOR]`** M-12 |
| DEPLOY-ASSET-001 mục (6) **icon-font sau merge, load lại nhiều lần không lúc có lúc mất** | **0 TC** | **`[MAJOR]`** M-12 |
| Có **danh sách nơi ảnh hưởng do DEV cung cấp** cho phần shared config? | **Không** — dev chỉ viết *"Quét ngang: mảng chọn kiểu này chỉ tồn tại ở đúng màn này"*, **không kèm kết quả grep / danh sách màn**. T2 khai "toàn bộ màn dùng chung" nhưng **không liệt kê màn nào** | **`[MAJOR]`** M-10 (không nâng BLOCKER vì phạm vi shared ở đây là *version asset*, không phải logic nghiệp vụ dùng chung) |
| TC test **từng nơi** trong danh sách ảnh hưởng? | **0 TC** mở màn khác sau bump version | **`[MAJOR]`** M-10 |

### Symptom-only KH report check → **DÍNH**

`01-bug-task.md` mục "Mô tả bug" + "Actual result" ghi đúng một dòng: **"BUG: Ko chuyển sang unconfirm được"** — thuần **triệu chứng**, không có error code / error message / log / request-response. Dev tái hiện **đúng 1 root cause** (stale `allMessage`).

**Bằng chứng có root cause thay thế THẬT** — chính bộ TC này đã tìm ra: Studio bug **#668 (severity High)** — `EP-06` với `type_action=all` trả **HTTP 500** (`Unknown column '1'`). Nếu khách hàng dùng 「全N件選択」 thì cũng ra **đúng triệu chứng "không đổi được trạng thái"** nhưng do **root cause hoàn toàn khác**, nằm ở backend. Không ai xác nhận khách hàng gặp nhánh nào.

→ **`[MAJOR]` M-06**: cần hỏi Dev + người báo bug (Ngần) xác nhận khách gặp nhánh nào; TCs phải cover **≥ 2 plausible root cause**.

Các root cause thay thế khác cùng cho ra triệu chứng "không đổi được trạng thái":
- (a) `type_action=all` HTTP 500 — **đã xác nhận có thật** (bug #668).
- (b) 「全N件選択」 không hiện do `totalMsg=0` — **đã xác nhận có thật** (bug #669).
- (c) Tin đổi sang 確認済 **biến khỏi danh sách** ở bộ lọc mặc định 「未確認のみ」 → người dùng tưởng "không đổi được" khi muốn đổi ngược lại (đây có thể chính là điều khách gặp — steps của khách nói rõ phải bấm 「一覧」 trước).
- (d) Badge/ES chưa đồng bộ → màn hiển thị trạng thái cũ dù dữ liệu đã đổi.

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| **AP-1** Single-trigger generic-fix | **Không** | Fix không phải dạng error-handling generic |
| **AP-2** Symptom-only KH report | **✅ DÍNH** | → M-06 |
| **AP-3** Happy-path-only regression | **✅ DÍNH** | T2 chỉ có 1 TC kiểm tra tĩnh, precondition không có edge state, không mở màn thật → M-10 |
| **AP-4** Specific check disguised as generic | **Không** (nhưng thiếu PR) | Mục "Commit / Pull Request" chỉ có commit hash `c5bc8e33a1` + branch, **không có URL PR/diff** để review verify fix shape → `[MINOR]` m-04 |
| **AP-5** Layer-downstream over-coverage | **✅ DÍNH (nhẹ)** | TC-APICONTRACT001-01/-02 test backend không bị chạm → m-02 |
| **AP-6** Mục 3 dev-impact trống | **Không** | Mục 3 có đủ 6 function caller |

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] B-01` — TC-OUTTRUTH001-01: `Kết quả mong đợi` MÂU THUẪN spec BR-07**

TC ghi: *"Badge số chưa xác nhận trên sidebar **có thể chưa phản ánh ngay** trong cùng trang nếu sidebar chỉ được render lại khi reload, nên **không dùng giá trị stale trước F5 để kết luận Fail**"*.

Spec `spec-features/admin/chat-management/feature-spec.md` **BR-07** (Confidence: **Cao**) ghi ngược lại: *"Sau khi thay đổi trạng thái: cập nhật `bots.count_user_unconfirm`, gửi **FCM push notification** cập nhật badge mobile, **broadcast `InfoEvent` qua WebSocket cập nhật realtime web** (`totalUserConfirmMessage`, `totalErrorMessage`, `totalGroupConfirmMessage`)"*.

`note` của TC nói rõ oracle đã bị sửa **"theo bằng chứng run #401"** — tức **TC được nới lỏng để khớp hành vi quan sát được, thay vì khớp spec**. Nếu WebSocket `InfoEvent` không cập nhật badge realtime thì **đó là bug cần raise**, không phải điều kiện để hạ chuẩn TC. Đây là mẫu "sửa test cho vừa bug" — nguy hiểm vì nó **hợp thức hoá** một regression tiềm tàng.

→ **Fix**: khôi phục oracle realtime theo BR-07 (badge web phải đổi **không cần F5**); nếu thực tế không đổi → raise bug WebSocket/`InfoEvent` và để TC ở trạng thái Không đạt. Cần Dev xác nhận `InfoEvent` có được phát ở màn `talk-list` không (BR-07 mô tả ở `changeStatusMessage`, dùng chung cho cả 2 màn).

---

**`[BLOCKER] B-02` — GAP `DATA-DB-001` (Cao): 0 TC kiểm `WHERE` scope trên 2 tài khoản**

`DATA-DB-001` là **BẮT BUỘC với mọi chức năng có UPDATE hoặc DELETE**, và **không thay thế được bằng kiểm tra trên UI** (RULE-07). Luồng này DELETE/INSERT `unconfirm_message` + UPDATE `conversation.*` + `bots.count_user_unconfirm`.

Trong 22 TC: **không TC nào** tạo bản ghi trùng ở **2 bot** rồi thao tác ở bot A và xác nhận bot B không đổi. TC-TOOLNEGCTRL001-01 có đối chứng âm nhưng **cùng một bot**. Cộng thêm: payload `type_action=all` đi kèm bộ lọc (BR-08 `advanceFilterPost()` là **shared logic** với FA-008/FA-013/FA-009) — sai `WHERE` ở đây có thể đổi trạng thái tin của bot khác.

→ **Fix**: bổ sung TC-DATADB001-01/02/03 ở §5.

---

**`[BLOCKER] B-03` — GAP `CONC-003` (Cao ở màn này): 0 TC race tầng giao diện**

`CONC-003` — *"Trung bình (→ **Cao** khi màn có **loadmore/phân trang + filter**, hoặc nhiều tab cùng gọi API)"*. Màn `talk-list` **thoả cả hai**: BR-03 lazy load 100 record/lần qua nút 「次へ」 + bộ lọc nhanh / tìm kiếm / bộ lọc nâng cao / khoảng ngày → quan điểm này là **Cao**.

Đây là quan điểm **sát root cause nhất mà lại trống hoàn toàn**: bug gốc chính là **state phía client không khớp UI sau khi danh sách nạp lại**. Bản vá reset `allMessage` trong `initData()` — nhưng **không xử lý trường hợp response cũ về sau response mới**. 5 kiểm tra của CONC-003 (chuyển tab nhanh khi API chưa trả về · loadmore vừa load vừa filter · Slow 3G · chủ động delay 1 response · bấm filter liên tiếp) **không có TC nào**.

TC-CONC001-01 có nhắc Slow 3G nhưng chỉ để phục vụ double-click, không phải kiểm race response.

→ **Fix**: bổ sung TC-CONC003-01/02/03 ở §5.

---

**`[BLOCKER] B-04` — GAP `COMPAT-LEGACY-001` (Cao) / RULE-09: 0 TC cho tin nhắn ở bảng shard legacy**

Spec **BR-02**: tin nhắn nằm rải trên **`messages_v2s` → `messages` → `messages2025`…`messages2020` → `messages_page_2` → `messages_old`**; truy vấn ưu tiên mới → cũ. Spec **§4.3 mục 19**: đổi sang 未確認 còn UPDATE **`messages.is_confirmed` (legacy)**. Spec **BR-11**: modal chi tiết **chỉ** đọc `messages_v2s` → tin cũ **không xem được chi tiết**.

Toàn bộ 22 TC dùng precondition dạng *"có ít nhất 1 tin đang 未確認"* — **không TC nào chỉ định tin nhắn CŨ thuộc bảng shard legacy**. Ticket này mở từ **2025-02-24** và khách vẫn gặp lỗi đến 2026-08-19, nên tin nhắn thật của khách **chắc chắn nằm ở shard cũ**. RULE-09 cấm đánh × chỉ vì "dữ liệu mới chạy ổn".

→ **Fix**: bổ sung TC-COMPATLEGACY001-01/02/03 ở §5.

---

**`[BLOCKER] B-05` — REQ-003 (risk High) chỉ 2/3 phạm vi chọn hoạt động; không đủ cơ sở kết luận fix đạt**

REQ-003 của Studio: *"**Ba** cách chọn — tick từng dòng, 「ページ内選択」 và 「全N件選択」 — đều đổi trạng thái đúng phạm vi đã chọn ở lượt đầu **và vẫn hoạt động ở các lượt tiếp theo**"*, risk **High**.

Hiện trạng: nhánh 「全N件選択」 **hỏng hoàn toàn ở cả 2 tầng** —
- UI: TC-SELECTSCOPE001-02 **fail** → bug #669 — tick 「ページ内選択」 không làm hiện 「全N件選択」 (`totalMsg = 0`).
- API: TC-APICONTRACT001-02 **fail** → bug #668 (**severity High**) — `type_action=all` trả **HTTP 500**.

Vì control 「全N件選択」 **không bao giờ hiện được**, phần *"và vẫn hoạt động ở các lượt tiếp theo"* của REQ-003 cho nhánh này **chưa từng được kiểm chứng** — kể cả sau bản vá. Ticket đang ở trạng thái `Fix done - Đợi test` với `aiResult = fail`.

→ **Fix / quyết định Leader cần chốt**: (a) 2 bug này **chặn** #28418 (vì REQ-003 là requirement của chính task), hay (b) tách ticket riêng và thu hẹp phạm vi nghiệm thu #28418 xuống 2/3 phạm vi chọn — **ghi rõ vào ticket** để không ai hiểu nhầm là đã test đủ. Studio note của cả 2 TC đề xuất hướng (b); cần Leader phê duyệt chính thức chứ không để note TC tự quyết.

### 4.2 Major (nên fix)

**`[MAJOR] M-01`** — Tỷ lệ pass **77.3% (17/22)**, dưới ngưỡng 80%. Coverage "trên giấy" trông đầy đủ nhưng 5/22 TC (4 fail + 1 chưa chạy) **không cho kết luận test nào**.

**`[MAJOR] M-02` RULE-08 / ENV-003** — **0 TC chạy trên `staging` hoặc `product`**. Run staging #664 khởi động 06:35:32 và **vẫn `running`** (run manual #665 khởi động sau đã kết thúc lúc 06:58:42) → **nghi treo**. Nghiêm trọng nhất với `DEPLOY-ASSET-001` và `DATA-CACHE-001`: bản chất là verify **một lần deploy thật**, chạy ở `local` (`http://127.0.0.1:8000`) **không có giá trị kết luận**. → Chạy lại run staging, và bổ sung run `product` cho nhóm deploy/asset/race.

**`[MAJOR] M-03`** — **86% TC do AI sinh** (19/22, job #505) trong khi `reviewState = leader` và **`reviewed = false`**. Chưa ai duyệt nội dung TC trước khi chạy → rủi ro oracle sai được hợp thức hoá (chính là B-01).

**`[MAJOR] M-04`** — **QA người chưa nghiệm thu tay TC nào**. Run manual #665 kết thúc `status = error`: *"Kết thúc mà chưa nhập kết quả TC nào trong lần test này"* (`pass 0 / fail 0 / blocked 0 / skip 0 / total 0`). Toàn bộ 21 kết quả đang có đều do **pipeline AI tự chạy tự chấm**. Với nhóm rủi ro cao (REQ-001/002/003 đều `High`), kết quả Đạt chỉ do AI tự chạy là không đủ nghiệm thu.

**`[MAJOR] M-05`** — **15/22 TC (68%) gắn mã quan điểm không có trong `framework/checklist-lme.md`**: `SELECT-SCOPE-001` (11 TC), `TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `API-CONTRACT-001`. Theo quy tắc 0.6 #6 các TC này **không được tính là cover quan điểm** → bảng §7 F.1 phải đọc theo hướng "coverage quan điểm thực tế thấp hơn con số 22 rất nhiều". → Leader chốt: bổ sung 4 mã vào framework (RULE-10) hay map thủ công sang mã tương đương (`SELECT-SCOPE-001` ≈ `BULK-001` + `LIST-001`; `TOOL-NEGCTRL-001` ≈ đối chứng âm của `DATA-DB-001`).

**`[MAJOR] M-06` SYMPTOM-ONLY (AP-2)** — xem §3.5. TCs cần cover **≥ 2 plausible root cause**; đã có bằng chứng root cause thay thế tồn tại thật (bug #668/#669). Hỏi Dev + Ngần: khách gặp nhánh nào?

**`[MAJOR] M-07` RULE-06 / `SYNC-APP-001`** — Spec BR-07 ghi rõ thao tác này **gửi FCM push notification cập nhật badge mobile app**. **0/22 TC** đi tới output cuối là **mobile app trên thiết bị thật**; TC xa nhất (TC-OUTTRUTH001-01) dừng ở **badge sidebar web**. RULE-06 cấm dừng ở màn admin khi có output ra ngoài. → TC-SYNCAPP001-01 ở §5.

**`[MAJOR] M-08`** — GAP `sync_elasticsearch` (BR-06). Đổi trạng thái ghi record vào `sync_elasticsearch` để đồng bộ **dữ liệu tìm kiếm**, mà chính màn này có ô 「メッセージ検索」. **0 TC** kiểm tin vừa đổi trạng thái có tìm ra đúng bằng search sau khi sync. → TC-DATA001-01 ở §5.

**`[MAJOR] M-09`** — **`03-dev-impact.md` mục 4.2 khai "Không có data impact" là SAI** so với spec §4.3 + BR-01/06/07 (6 bảng/cột bị ghi — xem bảng "Data impact ẩn" ở §3). Coverage matrix của member/AI được dựng trên base thiếu → mọi `D*` đều không tồn tại nên **không ai đi tìm GAP data**. Yêu cầu Dev bổ sung mục 4.2 rồi rà lại coverage.

**`[MAJOR] M-10` (AP-3)** — **T2 (asset version dùng chung) = GAP thực tế**. TC-REGSHARED001-01 chỉ đối chiếu `git diff`, **không mở bất kỳ màn nào** sau khi nâng version. Dev claim *"quét ngang… không có màn nào khác dính"* **không kèm bằng chứng grep / danh sách màn** (REG-SHARED-001 yêu cầu *"dev cung cấp danh sách nơi ảnh hưởng"*). → Yêu cầu Dev cung cấp danh sách + TC-REGSHARED001-02 ở §5.

**`[MAJOR] M-11` RULE-01 / `CONC-001` (Cao)** — `CONC-001` yêu cầu **4 kịch bản**; bộ TC chỉ có **1** (double-click, TC-CONC001-01) và kịch bản đó **FAIL** (bug #670 — tạo 2 bản ghi `unconfirm_message` trùng). Thiếu: (2) cùng user 2 tab/2 thiết bị, (3) 2 user khác nhau sửa cùng bản ghi, (4) batch đa luồng. Không có TC nào ghi lý do bỏ 3 kịch bản còn lại. → TC-CONC001-02 ở §5.
> 📌 Kho TCs đã có tiền lệ chốt hành vi đúng: `kho-tcs/fa001-chat11-11チャット.md` → **TC-CHT-43** *"Double click nút 決定 của popup 全て確認済みに変更 — chỉ tính 1 lần"*. Tức **"chỉ tính 1 lần" là chuẩn đã được công nhận** ở tính năng anh em → bug #670 là bug thật, không phải hành vi chấp nhận được.

**`[MAJOR] M-12` `DEPLOY-ASSET-001` thiếu chiều** — quan điểm này là **Cao**, và vì version asset là **biến dùng chung toàn hệ thống** nên bump version làm **mọi** JS/CSS/font/icon tải lại. Thiếu mục (5) font không fallback (kanji/kana + dấu tiếng Việt, không tofu ロ) và (6) icon-font load lại nhiều lần không lúc có lúc mất. → TC-DEPLOYASSET001-02 ở §5.

**`[MAJOR] M-13`** — **Cả `01-bug-task.md` và `03-dev-impact.md` đều có `Auto-filled: 2026-08-27 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick.** Auto-fill từ Redmine chưa được tester verify → F/D/T có thể thiếu hoặc map sai (M-09 chứng minh mục 4.2 đúng là sai thật). Yêu cầu tester đọc lại Redmine #28418 và tick trước khi review này có giá trị nghiệm thu.

**`[MAJOR] M-14` `DATA-COUNT-001` (Cao)** — quan điểm *"lỗi lặp nhiều nhất lịch sử bug — 12 ticket Closed"*. Màn có số đếm 未確認 ở badge sidebar + badge bot. TC-OUTTRUTH001-01 chỉ đối chiếu **1 nguồn** (badge vs dữ liệu đã lưu), **không có phép tính tay**, không đối chiếu **4 nguồn** (màn tóm tắt / màn chi tiết / CSV / API), không xét **mẫu số friend đã block**. → TC-DATACOUNT001-01 ở §5.

**`[MAJOR] M-15` `PERM-003` (Cao)** — *"BẮT BUỘC khi tổ chức vận hành nhiều LINE OA hoặc có chức năng change bot"*. LME có change bot; màn `talk-list` gắn chặt `bot_id`. **0 TC** kiểm hành vi khi **đổi bot giữa 2 lượt đổi trạng thái** — mà đây chính là một "đường nạp lại danh sách" nữa, cùng họ với 5 đường đã test. → gộp vào TC-DATADB001-02 ở §5.

**`[MAJOR] M-16`** — **TC-DEPLOYASSET001-01 có oracle không bao giờ đạt được**. TC yêu cầu *"Console không có lỗi JavaScript"*, nhưng Studio bug **#671** cho biết **mọi trang quản trị** nạp file CSS bằng thẻ `<script>` nên Console **luôn** có lỗi cú pháp JS — lỗi hệ thống có sẵn, **ngoài phạm vi #28418**. TC vì thế fail vì lý do không liên quan, **che mất** kết luận thật về version asset. → Tách oracle Console thành TC/bug riêng; TC-DEPLOYASSET001-01 chỉ giữ oracle "asset trả 200 kèm version mới + luồng 2 lượt chạy đúng".

### 4.3 Minor (có thể fix sau)

**`[MINOR] m-01`** — TC-REGSHARED001-01 (NEW-19) là kiểm tra tĩnh mã nguồn, không phải TC chạy được bởi manual tester → re-label thành mục code-review, không tính coverage F2/T2.

**`[MINOR] m-02` (AP-5)** — TC-APICONTRACT001-01/-02 test backend **không bị bản vá chạm**. Studio đã note đúng; đề nghị **tách sang ticket riêng** cho bug #668, không dùng gate #28418.

**`[MINOR] m-03`** — 3 TC do người viết (NEW-20/21/22) có **`requirement_keys` TRỐNG** → không map được về REQ-001…007, làm lệch thống kê coverage theo requirement của Studio. Gán REQ-001 (NEW-20), REQ-003 (NEW-21), REQ-002 (NEW-22).

**`[MINOR] m-04` (AP-4)** — Mục "Commit / Pull Request" chỉ có commit hash + branch, **không có URL PR/diff** → reviewer không tự verify được fix shape thực tế. Yêu cầu Dev bổ sung link.

**`[MINOR] m-05` RULE-02** — Nhiều TC mô tả oracle rất kỹ trong `note` nhưng **không nêu rõ LOẠI EVIDENCE bắt buộc** phải đính kèm khi tick Đạt (screenshot Network tab? query DB? video?). Ví dụ TC-CONC001-01 cần *"bằng chứng số lần xử lý thực tế"* theo CONC-001 nhưng TC không ghi.

**`[MINOR] m-06`** — `TC No.` trên Studio dùng `temp_id` dạng `NEW-1`…`NEW-22`, không theo format repo `TC-<mã quan điểm bỏ gạch>-<nn>`. (ID trong `04-tc-list.md` đã được `/new-task` sinh lại đúng format; ghi nhận để đồng bộ chuẩn giữa Studio ⇄ repo.)

### 4.4 Nit (gợi ý)

**`[NIT] n-01`** — `kho-tcs/` **chưa có FA-002**. Tính năng anh em FA-001 (Chat 1:1) đã có 11 TC nhóm 「全て確認済みに変更」 dùng **cùng bảng dữ liệu**. Đề nghị chạy `/collect-tcs` cho FA-002 để lần review sau có kho đối chiếu.

**`[NIT] n-02` RULE-11** — `framework/checklist-lme.md` §4 có `CHAT-01` thuộc nhóm "quan điểm chưa đủ bằng chứng" → chỉ nêu ở mức gợi ý, **không** dùng để flag BLOCKER/MAJOR trong report này.

**`[NIT] n-03`** — Đề nghị đặt lại tên TC-TOOLKNOW002-01 cho khớp vai trò: đây là **TC tái hiện bug gốc** (A.1), nên mã quan điểm hợp lý hơn là `FUNC-SEQ-001` thay vì mã nội bộ `TOOL-KNOW-002`.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 22 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `điều kiện tiền đề tương đương` → `kết quả mong đợi` tương đương). Phát hiện **3 nhóm trùng**.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| **G1** — 4 đường nạp lại danh sách đi qua **cùng một code path `initData()` thường** | TC-SELECTSCOPE001-04 (bộ lọc nhanh) | **GỘP** TC-SELECTSCOPE001-05 (tìm kiếm), -06 (bộ lọc nâng cao), -07 (khoảng ngày) vào -04 thành **1 TC 4 biến thể theo bước** | `DUP-INFLATE` | Cùng `SELECT-SCOPE-001` · cùng `Normal` · cùng thao tác (tick tin → kích hoạt nạp lại → bấm 「変更」 khi chưa tick lại) · tiền đề tương đương (≥1–2 tin của bạn bè) · expected tương đương (mọi ô tick bỏ chọn + bộ nhớ chọn rỗng + không tin nào đổi trạng thái) | **`[MAJOR]`** |
| **G2** — chuỗi đổi trạng thái lặp lại trên **cùng 1 tin** | TC-TOOLKNOW002-01 (**TC tái hiện bug gốc**, bắt buộc giữ theo A.1) | **GỘP** TC-FUNCSEQ001-02 (NEW-20) vào -01 bằng cách nâng số chu kỳ của -01 từ 2 → 4 lượt | `DUP-SUBSET` | -01 ⊂ NEW-20 · cùng đối tượng (1 tin A) · cùng thao tác (tick lại chính tin đó rồi 「変更」) · cùng tiền đề · expected tương đương (mỗi lượt đều có hiệu lực, ô tick reset sau mỗi lần nạp lại) | `[MINOR]` |
| **G3** — lượt sau không được kéo theo tin của lượt trước | TC-TOOLNEGCTRL001-01 (NEW-5) — **Abnormal duy nhất** của trục đối chứng âm | **GỘP** TC-SELECTSCOPE001-09 (NEW-22) vào NEW-5 bằng cách thêm tin C vào lượt 1 | `DUP-SUBSET` | NEW-5 ⊂ NEW-22 (NEW-22 chỉ khác ở chỗ lượt 1 chọn 3 tin thay vì 1) · cùng thao tác · cùng tiền đề · expected tương đương (tin của lượt trước **giữ nguyên** trạng thái, request lượt 2 chỉ chứa id đang tick) | `[MINOR]` |

### Gate trước khi đề nghị xóa — đã chạy

Giả định **xóa** từng TC ở cột "đề nghị", chạy lại BƯỚC 2 + 3b trên tập còn lại:

- **G1**: xóa -05/-06/-07 → `SELECT-SCOPE-001` vẫn còn 8 TC, **F1 (Direct) vẫn OK**; nhưng **REQ-004 mất 3 trigger nghiệp vụ riêng biệt** (tìm kiếm / bộ lọc nâng cao / khoảng ngày là 3 thao tác người dùng khác nhau) → **đổi đề xuất từ "xóa" sang "GỘP"**, giữ đủ 4 biến thể trong steps của 1 TC (đúng cách TC-SELECTSCOPE001-07 đã tự gộp "đổi khoảng ngày" + 「全期間」).
- **G2**: xóa NEW-20 → mất phần "≥3 chu kỳ liên tiếp". → **GỘP** (nâng chu kỳ của -01), không xóa trắng.
- **G3**: xóa NEW-5 → **mất TC `Abnormal` duy nhất** của trục đối chứng âm, và mất luôn quan điểm `TOOL-NEGCTRL-001` → **cấm xóa NEW-5**. Xóa NEW-22 thay thế → mất biến thể multi-select. → **GỘP** vào NEW-5.

> ⚠️ **Không tự xóa TC** — TC Studio là read-only. Human quyết định, sửa bằng `testcase_update` / `testcase_delete` trên Studio.
>
> 📌 **Ý nghĩa của G1 (`DUP-INFLATE`)**: 11/22 TC dồn vào `SELECT-SCOPE-001` làm bộ TC **trông rất dày**, che mất việc `CONC-003`, `DATA-DB-001`, `COMPAT-LEGACY-001` (đều **Cao**) **trống hoàn toàn**. Gộp G1 giải phóng công sức test để lấp đúng 3 GAP đó.

---

## 5. TCs đề xuất bổ sung

### Đối chiếu kho TCs (BƯỚC 5a)

- **`kho-tcs/` CHƯA có FA-002** (`ls kho-tcs/*.md` → không có `fa002`). Không đối chiếu trực tiếp được → ghi nhận ở `[NIT] n-01`.
- **Đã đối chiếu tính năng anh em `kho-tcs/fa001-chat11-11チャット.md`** — nhóm 「全て確認済みに変更」 (11 TC) ghi/xoá **cùng bộ dữ liệu** (`unconfirm_message`, `conversation.confirm_count`, `bots.count_user_unconfirm`) ⇒ đây là **vùng regression** của task này:

  | Câu hỏi BƯỚC 5a | Kết quả |
  |---|---|
  | **Phạm vi ảnh hưởng** | `TC-CHT-34/35/36/37/38` (BULK-001 — xác nhận hàng loạt **có / không có filter**), `TC-CHT-39` (filter khớp 0), `TC-CHT-40` (DATA-001 — không đụng hội thoại đã xác nhận), `TC-CHT-41` (CONC-002 — tin mới đến giữa chừng), `TC-CHT-42` (STATE-001 — reload giữ trạng thái), `TC-CHT-43` (CONC-001 — double-click chỉ tính 1 lần). **Bộ 22 TC ở BƯỚC 0 không có TC nào chạm vùng này** → tính là GAP, đã sinh TC regression bên dưới. |
  | **Conflict expected** | **Có 1 điểm cần Leader chốt**: `TC-CHT-43` (kho) chốt *"double click → chỉ tính 1 lần"*, trong khi TC-CONC001-01 (#28418) **fail** vì tạo **2 bản ghi**. Không mâu thuẫn về chuẩn — kho **củng cố** rằng bug #670 là bug thật. Đưa vào §6 để chốt chính thức. |
  | **Đã có sẵn** | Không TC kho nào cover đúng GAP của task này (kho là màn Chat 1:1, không phải `talk-list`) → viết mới, dẫn chiếu ID kho ở `Ghi chú`. |

### Chống trùng (BƯỚC 5b)

> ✅ **Đã đối chiếu 22 TC ở BƯỚC 0 + `kho-tcs/fa001-chat11-11チャット.md` — không TC đề xuất nào trùng.** Đã kiểm cả 2 chiều: (a) vs bộ 22 TC Studio theo 4 yếu tố; (b) vs các TC khác trong chính §5. ID đề xuất tránh đụng ID đã có trong `04-tc-list.md` (`TC-CONC001-01`, `TC-DEPLOYASSET001-01`, `TC-REGSHARED001-01` đã tồn tại → bắt đầu từ `-02`).

### Bảng TC (14 cột)

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC003-01 | API | CONC-003 | Đổi trạng thái hàng loạt | Normal | manual | product | Bấm liên tiếp nhiều bộ lọc khi request trước chưa trả về — danh sách cuối khớp điều kiện CUỐI CÙNG | - Đăng nhập admin, đang chọn bot A<br>- Màn 「チャット管理」 có ≥ 200 tin trải nhiều ngày để danh sách tải chậm thấy được<br>- Mở DevTools tab Network, bật throttling **Slow 3G** | 1. Mở màn 「チャット管理」, bấm 「一覧」.<br>2. Tick 1 dòng tin bất kỳ (tin A).<br>3. Bấm 「未確認のみ」, **không chờ danh sách tải xong**, bấm ngay 「一覧」, rồi bấm ngay 「未確認のみ」 lần nữa (3 lần đổi trong ~2 giây).<br>4. Chờ mọi request hoàn tất, quan sát Network xem thứ tự response trả về.<br>5. Đối chiếu danh sách đang hiển thị với điều kiện lọc **cuối cùng** đang được chọn.<br>6. Quan sát toàn bộ ô tick và ô 「ページ内選択」.<br>7. Không tick lại gì, chọn radio 「確認済」 rồi bấm 「変更」. | 3 lần đổi bộ lọc nhanh liên tiếp trong ~2 giây dưới Slow 3G | Danh sách hiển thị đúng kết quả của điều kiện lọc **cuối cùng** (「未確認のみ」), không phải của response về sau cùng. Mọi ô tick bỏ chọn và bộ nhớ lựa chọn rỗng. Bước 7: không tin nào đổi trạng thái, tin A giữ nguyên. Không có dòng nào bị nhân đôi trên danh sách. | | Lấp GAP-1 / cover impact F1 · Đánh giá spec: Spec không ghi (đã hỏi Leader — BR-03 chỉ mô tả lazy load, không mô tả xử lý response out-of-order) · Evidence: video thao tác + screenshot Network tab thể hiện thứ tự response · regression |
| TC-CONC003-02 | API | CONC-003 | Đổi trạng thái hàng loạt | Abnormal | manual | product | Bấm 「次へ」 ngay khi 「変更」 chưa hoàn tất — lựa chọn cũ không được sống lại | - Như TC-CONC003-01<br>- Danh sách phải hiện nút 「次へ」 (bot có > 100 tin) | 1. Mở màn 「チャット管理」, bấm 「一覧」, bật Slow 3G.<br>2. Tick 2 dòng tin A và B.<br>3. Chọn radio 「確認済」, bấm 「変更」.<br>4. **Ngay lập tức** (trước khi danh sách tải lại xong) bấm nút 「次へ」.<br>5. Chờ mọi request hoàn tất, quan sát toàn bộ ô tick.<br>6. Không tick lại gì, chọn radio 「未確認」 rồi bấm 「変更」.<br>7. F5 và đối chiếu trạng thái của A, B và các tin đã tải thêm ở bước 4. | Tin A, B đang 「未確認」; thao tác chồng lấn giữa 「変更」 và 「次へ」 | Sau bước 5: mọi ô tick bỏ chọn, không có ô nào tự tick lại do response cũ về sau. Bước 6: **không tin nào bị đổi về 「未確認」** — đặc biệt A và B phải **giữ 「確認済」** đã đặt ở bước 3. Sau F5: các tin tải thêm ở bước 4 giữ nguyên trạng thái ban đầu, không tin nào bị đổi ngoài ý muốn. | | Lấp GAP-1 / cover impact F1, F3 · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: video + screenshot Network + đối chiếu trạng thái trước/sau · Đây là biến thể chồng lấn của 2 đường nạp lại (reload thường + `type='nextPage'`) mà TC-SELECTSCOPE001-03 chỉ test tuần tự |
| TC-CONC003-03 | API | CONC-003 | Đổi trạng thái hàng loạt | Boundary | manual | product | Response của lần lọc CŨ về SAU response lần lọc mới — UI phải bỏ qua response cũ | - Như TC-CONC003-01<br>- Cần DevTools có khả năng chặn/delay request (tab Network → Block request URL, hoặc dùng công cụ proxy) | 1. Mở màn 「チャット管理」, bấm 「一覧」.<br>2. Chủ động **delay** response của request nạp danh sách lần thứ nhất (giữ ~10 giây).<br>3. Trong lúc đang chờ, đổi 「表示期間」 sang một khoảng ngày hẹp → phát sinh request lần thứ hai và để nó trả về **trước**.<br>4. Thả request lần thứ nhất cho về sau.<br>5. Đối chiếu danh sách đang hiển thị với khoảng ngày đang chọn ở bước 3.<br>6. Tick 1 dòng bất kỳ, bấm 「変更」 và kiểm tra tin nào bị đổi. | Ép thứ tự response đảo ngược: request cũ về sau request mới | Danh sách hiển thị **kết quả của khoảng ngày ở bước 3**, tuyệt đối không bị response cũ ghi đè trở lại danh sách đầy đủ. Ô tick vẫn ở trạng thái bỏ chọn sau khi response cũ về. Bước 6: chỉ đúng dòng vừa tick bị đổi trạng thái, và dòng đó phải thuộc danh sách đang hiển thị. | | Lấp GAP-1 / cover impact F1 · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: screenshot Network tab thể hiện thứ tự response đảo + screenshot danh sách sau cùng · Case biên của CONC-003 mục (4) |
| TC-DATADB001-01 | Data | DATA-DB-001 | Đổi trạng thái hàng loạt | Normal | manual | staging | Đổi trạng thái ở bot A không được đụng tin trùng nội dung của bot B | - Có **2 bot** A và B mà tài khoản admin đều truy cập được<br>- Mỗi bot có 1 tin của bạn bè với **cùng nội dung text và cùng ngày nhận** (VD cùng gửi chuỗi `TEST-28418` trong cùng ngày), cả hai đang 「未確認」<br>- Ghi lại badge số chưa xác nhận của **cả 2 bot** trước khi bắt đầu | 1. Chọn bot A, mở 「チャット管理」, bấm 「一覧」.<br>2. Tick tin `TEST-28418` của bot A, chọn 「確認済」, bấm 「変更」.<br>3. Chờ danh sách tải lại; ghi lại badge số chưa xác nhận của bot A.<br>4. **Change bot** sang bot B, mở 「チャット管理」, bấm 「一覧」.<br>5. Đối chiếu trạng thái tin `TEST-28418` của bot B và badge số chưa xác nhận của bot B với giá trị ghi ở tiền điều kiện.<br>6. Nhờ Dev/QA có quyền chạy query đối chiếu bản ghi chưa xác nhận của **cả 2 bot** trước/sau thao tác. | 2 tin **trùng nội dung + trùng ngày** ở 2 bot khác nhau | Bot A: tin đổi sang 「確認済」, badge giảm đúng 1. **Bot B: tin `TEST-28418` vẫn 「未確認」, badge KHÔNG đổi.** Query đối chiếu xác nhận chỉ bản ghi thuộc bot A bị xoá — điều kiện `WHERE` có đủ `bot_id`. | | Lấp GAP-2 (B-02) / cover impact D-ẩn (`unconfirm_message`, `conversation.confirm_count`, `bots.count_user_unconfirm`) · Đánh giá spec: Spec ghi rõ (BR-01, feature-spec §4.3 mục 18/19) · Evidence: screenshot 2 bot trước/sau + ảnh chụp kết quả query kèm câu query (RULE-07) · dẫn từ TC-CHT-40 (kho FA-001) |
| TC-DATADB001-02 | Data | DATA-DB-001 | Đổi trạng thái hàng loạt | Abnormal | manual | staging | Change bot ở tab khác rồi quay lại tab cũ bấm 「変更」 — không đổi nhầm bot | - Như TC-DATADB001-01<br>- Mở **2 tab trình duyệt** cùng phiên đăng nhập | 1. Tab 1: chọn bot A, mở 「チャット管理」, bấm 「一覧」, tick tin `TEST-28418` của bot A (**chưa bấm 「変更」**).<br>2. Tab 2: **change bot** sang bot B.<br>3. Quay lại tab 1 (**không F5**), chọn radio 「確認済」 rồi bấm 「変更」.<br>4. Quan sát phản hồi trên tab 1.<br>5. Kiểm tra trạng thái tin `TEST-28418` ở **cả bot A và bot B**, và badge số chưa xác nhận của cả hai. | Bot đang chọn trong phiên bị đổi giữa lúc tab cũ còn giữ lựa chọn | **Tuyệt đối không được đổi trạng thái tin của bot B.** Hệ thống hoặc (a) đổi đúng tin của bot A, hoặc (b) báo lỗi/từ chối rõ ràng vì bot trong phiên đã đổi — **không được im lặng đổi nhầm sang bot B**, không được đổi cả hai. Badge của bot không liên quan giữ nguyên. | | Lấp GAP-2 + M-15 (`PERM-003` — cách ly đa tài khoản LINE OA) · Đánh giá spec: **Spec không ghi** — cần hỏi Dev hành vi đúng khi bot trong phiên đổi giữa chừng (đưa vào §6) · Evidence: screenshot 2 tab + trạng thái 2 bot sau thao tác · Đây cũng là kịch bản (2) của CONC-001 (cùng user, 2 tab) |
| TC-DATADB001-03 | Data | DATA-DB-001 | Đổi trạng thái hàng loạt | Boundary | manual | staging | Đổi trạng thái toàn bộ trang ở bot có ĐÚNG 1 tin, bot còn lại không bị đụng | - Có 2 bot: bot A **chỉ có đúng 1 tin** của bạn bè đang 「未確認」; bot B có nhiều tin đang 「未確認」<br>- Ghi lại badge của cả 2 bot | 1. Chọn bot A, mở 「チャット管理」, bấm 「一覧」.<br>2. Tick ô 「ページ内選択」 (chọn cả trang — ở đây chỉ có 1 dòng).<br>3. Chọn 「確認済」, bấm 「変更」, chờ danh sách tải lại.<br>4. Đối chiếu badge bot A: phải về 0 tin chưa xác nhận.<br>5. Change bot sang B, đối chiếu badge và danh sách của bot B với giá trị ghi ở tiền điều kiện.<br>6. Quay lại bot A, tick lại chính tin đó, chọn 「未確認」, bấm 「変更」 và xác nhận lượt thứ hai có hiệu lực. | Bot A có đúng **1** bản ghi (biên nhỏ nhất của phạm vi 「ページ内選択」) | Bot A: tin duy nhất đổi sang 「確認済」, badge về 0. **Bot B: badge và toàn bộ trạng thái tin KHÔNG đổi.** Bước 6: lượt đổi thứ hai vẫn có hiệu lực, tin quay lại 「未確認」, badge bot A về 1 — xác nhận biên 1-phần-tử không làm kẹt các lượt sau. | | Lấp GAP-2 / cover impact F1, F4 · Đánh giá spec: Spec ghi rõ (BR-01) · Evidence: screenshot badge 2 bot trước/sau + query đối chiếu · Case biên bổ sung cho RULE-01 của DATA-DB-001 |
| TC-COMPATLEGACY001-01 | Data | COMPAT-LEGACY-001 | Đổi trạng thái hàng loạt | Normal | manual | product | Đổi trạng thái tin nhắn CŨ nằm ở bảng shard năm trước | - Bot **production** có tin nhắn bạn bè nhận từ **năm trước trở về trước** (VD 2025 hoặc sớm hơn) — theo BR-02 tin này nằm ở bảng shard cũ, không phải `messages_v2s`<br>- Xác định trước 1 tin cũ đang 「未確認」 (gọi là tin OLD), ghi lại tên LINE + ngày nhận | 1. Mở 「チャット管理」, bấm 「一覧」.<br>2. Đặt 「表示期間」 về khoảng ngày chứa tin OLD (hoặc bấm 「全期間」 rồi bấm 「次へ」 tới khi thấy tin OLD).<br>3. Tick tin OLD, chọn 「確認済」, bấm 「変更」, chờ danh sách tải lại.<br>4. Kiểm tra badge trạng thái của tin OLD và badge số chưa xác nhận.<br>5. Tick lại chính tin OLD, chọn 「未確認」, bấm 「変更」 (kiểm luồng 2 lượt của #28418 trên dữ liệu cũ).<br>6. F5 và đối chiếu lại trạng thái tin OLD. | Tin nhắn nhận từ **năm trước** trở về trước (nằm ở bảng shard legacy) | Cả **hai lượt** đổi trạng thái đều có hiệu lực trên tin cũ, y hệt tin mới. Badge trạng thái đổi đúng ở từng lượt, badge số chưa xác nhận tăng/giảm đúng 1. Sau F5 trạng thái vẫn khớp. Không xảy ra trường hợp bấm 「変更」 mà tin cũ không đổi hoặc màn báo lỗi. | | Lấp GAP-3 (B-04) / cover impact T1 + D-ẩn (`messages.is_confirmed` legacy) · Đánh giá spec: Spec ghi rõ (BR-02 sharding, feature-spec §4.3 mục 19) · Evidence: screenshot tin cũ kèm ngày nhận trước/sau + badge · **RULE-09: bắt buộc chạy nhánh dữ liệu CŨ, không được kết luận từ tin mới** · **RULE-08: chỉ production mới có dữ liệu shard cũ thật** |
| TC-COMPATLEGACY001-02 | Data | COMPAT-LEGACY-001 | Đổi trạng thái hàng loạt | Abnormal | manual | product | Tin cũ không xem được modal chi tiết vẫn phải đổi được trạng thái | - Như TC-COMPATLEGACY001-01<br>- Chọn 1 tin OLD đủ cũ để **không nằm trong `messages_v2s`** (theo BR-11 modal chi tiết sẽ không hiển thị được) | 1. Mở 「チャット管理」, tìm tới tin OLD.<br>2. Click vào tin OLD để mở modal chi tiết 「メッセージ詳細」.<br>3. Ghi nhận hành vi: modal có mở được không, có báo lỗi hay hiện rỗng.<br>4. Đóng modal, tick tin OLD, chọn 「確認済」 rồi bấm 「変更」.<br>5. Kiểm tra trạng thái tin OLD và badge sau khi danh sách tải lại. | Tin cũ chỉ tồn tại ở bảng legacy, không có trong `messages_v2s` | Việc modal chi tiết không hiển thị được nội dung (hạn chế kiến trúc theo BR-11) **không được làm hỏng luồng đổi trạng thái**: modal phải báo trạng thái rõ ràng chứ **không sập màn / không văng lỗi JS**, và sau khi đóng modal thì tick + 「変更」 vẫn đổi được trạng thái tin OLD bình thường. | | Lấp GAP-3 / cover impact T1 · Đánh giá spec: Spec ghi rõ hạn chế (BR-11) nhưng **không ghi hành vi mong đợi của modal** → cần Leader chốt (đưa vào §6) · Evidence: screenshot modal + trạng thái tin sau 「変更」 |
| TC-COMPATLEGACY001-03 | Data | COMPAT-LEGACY-001 | Đổi trạng thái hàng loạt | Boundary | manual | product | Tick nhiều tin nằm VẮT QUA 2 bảng shard rồi đổi trạng thái 1 lượt | - Bot production có tin ở **cả 2 phía mốc chuyển bảng shard** (VD vài tin cuối tháng 12 năm trước + vài tin đầu tháng 1 năm nay), đều đang 「未確認」<br>- Ghi lại danh sách các tin sẽ tick và trạng thái ban đầu | 1. Mở 「チャット管理」, bấm 「全期間」 rồi bấm 「一覧」.<br>2. Bấm 「次へ」 tới khi danh sách hiển thị đồng thời tin của cả 2 năm.<br>3. Tick **cùng lúc** ít nhất 2 tin thuộc năm cũ và 2 tin thuộc năm mới.<br>4. Chọn 「確認済」, bấm 「変更」, chờ danh sách tải lại.<br>5. Đối chiếu trạng thái **từng tin đã tick** và badge số chưa xác nhận.<br>6. Tick lại đúng bộ tin đó, chọn 「未確認」, bấm 「変更」 và đối chiếu lần nữa. | Tập tin được chọn **vắt qua ranh giới 2 bảng shard** (biên của BR-02) | **Toàn bộ** tin đã tick đổi trạng thái đúng, không phân biệt tin đó nằm ở bảng shard nào. Badge số chưa xác nhận thay đổi đúng bằng **số tin đã tick**, không thiếu không thừa. Lượt thứ hai vẫn có hiệu lực trên đúng bộ tin đó. Không có tin nào bị bỏ sót vì thuộc bảng cũ. | | Lấp GAP-3 / cover impact T1, F1 · Đánh giá spec: Spec ghi rõ (BR-02 — truy vấn span nhiều bảng) · Evidence: bảng đối chiếu trạng thái từng tin trước/sau + badge · Case biên quan trọng vì `messages` bị chia bảng theo năm |
| TC-BULK001-01 | API | BULK-001 | Đổi trạng thái hàng loạt | Normal | manual | product | Số tin thực sự bị đổi khớp 100% số đã lọc (đếm tay) | - Bot có > 1 trang tin 「未確認」<br>- Áp một bộ lọc thu hẹp cho ra **số N xác định và đếm được** (VD lọc theo 1 tag chỉ có 7 bạn bè, hoặc khoảng ngày chỉ chứa 12 tin)<br>- **Đếm tay và ghi lại N** trước khi thao tác | 1. Mở 「チャット管理」, áp bộ lọc thu hẹp đã chuẩn bị.<br>2. **Đếm tay** số dòng tin thoả bộ lọc → ghi lại N (bấm 「次へ」 tới hết nếu nhiều trang).<br>3. Tick 「ページ内選択」, sau đó tick 「全N件選択」 và đối chiếu số N hiển thị trên control với số đếm tay ở bước 2.<br>4. Chọn 「確認済」, bấm 「変更」, chờ hoàn tất.<br>5. Bấm 「未確認のみ」 với **cùng bộ lọc** và đếm lại số tin còn 「未確認」.<br>6. Bỏ bộ lọc, kiểm tra các tin **ngoài** bộ lọc còn nguyên trạng thái ban đầu. | Bộ lọc cho ra đúng N tin (N đếm tay được, N > số dòng 1 trang) | Số N trên control 「全N件選択」 **khớp đúng** số đếm tay ở bước 2. Sau 「変更」: đúng **N** tin đổi sang 「確認済」 — không nhiều hơn (không rơi về toàn bộ tin của bot), không ít hơn (không chỉ tác động trang đầu). Bước 5 trả về 0 tin. Bước 6: **mọi tin ngoài bộ lọc giữ nguyên trạng thái**. | | Lấp GAP-4 / cover impact T1 + REQ-003 · Đánh giá spec: Spec ghi rõ (BR-08 `advanceFilterPost()`) · Evidence: **số bản ghi THẬT SỰ bị tác động khớp 100% số đã lọc** (ảnh đếm trước/sau) — bắt buộc theo BULK-001 · dẫn từ TC-CHT-35 (kho FA-001) · ⚠️ **Đang bị chặn bởi bug #669 + #668** — chạy lại sau khi 2 bug đó fix |
| TC-BULK001-02 | API | BULK-001 | Đổi trạng thái hàng loạt | Abnormal | manual | staging | Bộ lọc không khớp tin nào — bấm 「変更」 không lỗi, không đụng dữ liệu | - Bot có tin ở nhiều trạng thái<br>- Ghi lại badge số chưa xác nhận và trạng thái các tin hiện có | 1. Mở 「チャット管理」, áp bộ lọc chắc chắn **không khớp tin nào** (VD tìm kiếm một chuỗi không tồn tại, hoặc khoảng ngày trong tương lai).<br>2. Xác nhận danh sách rỗng.<br>3. Quan sát khu vực chọn: 「ページ内選択」 và 「全N件選択」 hiển thị thế nào.<br>4. Chọn radio 「確認済」 rồi bấm 「変更」.<br>5. Bỏ bộ lọc, đối chiếu badge và trạng thái toàn bộ tin với giá trị ghi ở tiền điều kiện. | Bộ lọc cho ra **0** kết quả | Không có tin nào bị đổi trạng thái, badge số chưa xác nhận **không đổi**. Màn hình không văng lỗi, không hiện exception, không gửi request đổi trạng thái với phạm vi rỗng. Sau khi bỏ lọc, toàn bộ dữ liệu y nguyên. | | Lấp GAP-4 / cover impact T1 · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: screenshot badge + danh sách trước/sau + Network tab chứng minh không có request đổi trạng thái · dẫn từ TC-CHT-39 (kho FA-001) · Case biên 0-kết-quả của trục lọc, khác với TC-SELECTSCOPE001-11 (0 lựa chọn nhưng danh sách có dữ liệu) |
| TC-SYNCAPP001-01 | API | SYNC-APP-001 | Đổi trạng thái hàng loạt | Normal | manual | product | Badge trên mobile app cập nhật sau khi đổi trạng thái trên web (FCM push) | - Bot **production**<br>- Đã cài mobile app LME, đăng nhập **cùng tài khoản**, đang chọn **cùng bot**, đã bật thông báo<br>- Ghi lại **số badge trên mobile app** và số chưa xác nhận trên web trước khi bắt đầu<br>- Để app ở màn hình chính, **không restart app** | 1. Trên **web**: mở 「チャット管理」, bấm 「一覧」, tick 1 tin đang 「未確認」, chọn 「確認済」, bấm 「変更」.<br>2. **Không thao tác gì trên app**, quan sát badge trên mobile app trong ~30 giây.<br>3. Nếu badge chưa đổi, thực hiện pull-to-refresh trên app rồi quan sát lại.<br>4. Đối chiếu badge app với số chưa xác nhận trên web.<br>5. Lặp lại theo chiều ngược: đổi 1 tin sang 「未確認」 trên web và quan sát badge app.<br>6. Ghi rõ badge cập nhật **tự động (push)** hay **chỉ sau pull-to-refresh**. | 1 tin đổi 「未確認」 → 「確認済」 rồi ngược lại | Badge số chưa xác nhận trên **mobile app** phản ánh đúng số thật sau thao tác trên web, ở **cả hai chiều**. Theo BR-07 hệ thống có gửi **FCM push** nên badge phải tự cập nhật mà không cần restart app; nếu chỉ đổi sau pull-to-refresh thì ghi nhận là **sai lệch so với spec** và raise bug. Badge app và số trên web không được lệch nhau. | | Lấp GAP-5 (M-07) / cover impact D-ẩn (`bots.count_user_unconfirm`) · Đánh giá spec: Spec ghi rõ (**BR-07** — FCM push + WebSocket) · Evidence: **screenshot cùng thao tác trên CẢ web VÀ mobile app thật** (RULE-06) · **RULE-08: FCM chỉ hoạt động đúng trên production** |
| TC-DATA001-01 | Data | DATA-001 | Đổi trạng thái hàng loạt | Normal | manual | Tất cả | Tin vừa đổi trạng thái tìm ra đúng bằng 「メッセージ検索」 (đồng bộ Elasticsearch) | - Bot có 1 tin của bạn bè chứa chuỗi đặc trưng dễ tìm (VD `ES-28418-CHECK`), đang 「未確認」<br>- Biết trước chuỗi từ khoá sẽ dùng để tìm kiếm | 1. Mở 「チャット管理」, bấm 「一覧」, nhập `ES-28418-CHECK` vào ô 「メッセージ検索」 và xác nhận tìm ra đúng tin đó cùng trạng thái 「未確認」.<br>2. Bấm 「クリア」, tick tin đó, chọn 「確認済」, bấm 「変更」.<br>3. Chờ ~1 phút cho chu kỳ đồng bộ tìm kiếm chạy.<br>4. Tìm kiếm lại `ES-28418-CHECK` và đối chiếu **trạng thái hiển thị trong kết quả tìm kiếm** với trạng thái trên danh sách thường.<br>5. Áp thêm bộ lọc nâng cao 「メッセージ確認状況」 = 「確認済み」 và xác nhận tin xuất hiện đúng nhóm.<br>6. Lặp lại theo chiều ngược (đổi về 「未確認」) và tìm kiếm lại. | Chuỗi từ khoá `ES-28418-CHECK`; 1 tin đổi trạng thái 2 chiều | Kết quả tìm kiếm hiển thị **cùng trạng thái** với danh sách thường ở cả hai chiều đổi. Bộ lọc 「メッセージ確認状況」 phân loại tin vào **đúng nhóm** sau khi đổi. Không xảy ra trường hợp danh sách thường hiện 「確認済」 nhưng kết quả tìm kiếm / bộ lọc vẫn coi tin là 「未確認」. | | Lấp GAP-6 (M-08) / cover impact D-ẩn (`sync_elasticsearch`) · Đánh giá spec: Spec ghi rõ (**BR-06** — ghi `sync_elasticsearch` khi `confirm_count` đổi) · Evidence: screenshot kết quả tìm kiếm + danh sách thường **cạnh nhau**, cả 2 chiều · `Tất cả` vì cần đối chiếu độ trễ đồng bộ giữa các môi trường |
| TC-DATACOUNT001-01 | Data | DATA-COUNT-001 | Đổi trạng thái hàng loạt | Normal | manual | staging | Số chưa xác nhận khớp giữa 4 nguồn + phép tính tay | - Bot test **sạch**, biết trước chính xác số tin 「未確認」 ban đầu (VD chuẩn bị đúng **10** tin chưa xác nhận từ **4** bạn bè khác nhau, trong đó **1 bạn bè đã block**)<br>- Ghi lại: badge sidebar, badge bot ở menu chọn bot, số dòng đếm tay trên màn 「未確認のみ」 | 1. Ghi lại số ban đầu ở **cả 3 nơi** trên web + đếm tay số dòng.<br>2. Tick đúng **3** tin, chọn 「確認済」, bấm 「変更」.<br>3. F5 rồi đối chiếu lại **cả 3 nơi**: badge sidebar, badge bot, số dòng đếm tay ở 「未確認のみ」. Phép tính tay: `10 − 3 = 7`.<br>4. Kiểm tra nguồn thứ 4: mở màn có hiển thị số chưa xác nhận khác (VD Chat 1:1 / mobile app / export nếu có) và đối chiếu.<br>5. Kiểm riêng cách tính với bạn bè **đã block**: xác nhận tin của bạn bè bị block được tính hay loại khỏi mẫu số theo đúng spec.<br>6. Đổi 2 tin về 「未確認」 và lặp lại đối chiếu (`7 + 2 = 9`). | 10 tin 「未確認」 từ 4 bạn bè, **1 bạn bè đã block**; đổi 3 tin rồi đổi ngược 2 tin | Cả **4 nguồn** hiển thị **cùng một con số** và khớp **phép tính tay** ở từng bước (10 → 7 → 9). Không nguồn nào lệch. Cách xử lý tin của bạn bè **đã block** nhất quán giữa các nguồn và đúng spec — nếu spec không quy định thì ghi nhận và hỏi Leader, **không tự suy diễn**. | | Lấp GAP-7 (M-14) / cover impact D-ẩn (`bots.count_user_unconfirm`, `conversation.confirm_count`) · Đánh giá spec: **Spec không ghi** cách xử lý friend đã block trong mẫu số → hỏi Leader (đưa vào §6) · Evidence: **bảng đối chiếu 4 nguồn + phép tính tay** (bắt buộc theo DATA-COUNT-001) · ⚠️ Quan điểm có 12 ticket Closed trong lịch sử |
| TC-CONC001-02 | API | CONC-001 | Đổi trạng thái hàng loạt | Abnormal | manual | product | Hai tab cùng user đổi trạng thái CÙNG một tin gần như đồng thời | - Đăng nhập admin, mở **2 tab** cùng bot A, cùng màn 「チャット管理」, cùng bấm 「一覧」<br>- Có 1 tin A đang 「未確認」 hiển thị trên **cả hai tab**<br>- Bật Slow 3G ở cả 2 tab để kéo dài khoảng chờ | 1. Tab 1: tick tin A, chọn 「確認済」 (**chưa bấm 「変更」**).<br>2. Tab 2: tick tin A, chọn 「未確認」 (**chưa bấm 「変更」**).<br>3. Bấm 「変更」 ở **tab 1**, rồi trong ~1 giây bấm 「変更」 ở **tab 2**.<br>4. Chờ cả 2 request hoàn tất.<br>5. F5 **cả hai tab** và đối chiếu trạng thái cuối của tin A.<br>6. Nhờ Dev/QA chạy query đếm số bản ghi chưa xác nhận của tin A. | Tin A: tab 1 đặt 「確認済」, tab 2 đặt 「未確認」, bấm cách nhau ~1 giây | Trạng thái cuối của tin A **xác định và nhất quán** trên cả 2 tab sau F5 (theo nguyên tắc last-write-wins là trạng thái của tab 2). Bản ghi chưa xác nhận của tin A **chỉ có tối đa 1**, không nhân đôi. Badge số chưa xác nhận khớp trạng thái cuối, **không bị đếm lệch**. Hệ thống không được âm thầm xử lý trùng làm badge sai. | | Lấp GAP-8 (M-11) / cover impact D-ẩn · Đánh giá spec: Spec không ghi cơ chế khoá/xung đột → hỏi Dev (đưa vào §6) · Evidence: **số lần xử lý thực tế đếm từ log/DB** (bắt buộc theo CONC-001) + screenshot 2 tab · dẫn từ TC-CHT-43 (kho FA-001 — chuẩn "chỉ tính 1 lần") · Đây là kịch bản (2) của CONC-001; kịch bản (1) đã có TC-CONC001-01 (đang fail, bug #40275) |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | Nâng version asset dùng chung | Normal | manual | product | Các màn KHÁC vẫn chạy đúng sau khi nâng số version asset dùng chung | - Trình duyệt đã mở và cache các màn ở bản **trước** khi vá<br>- Môi trường vừa deploy bản có #28418 (`config/sns-line.php` đã nâng version)<br>- **Yêu cầu Dev cung cấp danh sách màn dùng chung biến version asset** trước khi chạy (REG-SHARED-001) | 1. Sau deploy, **chỉ F5 thường** (không Ctrl+F5) lần lượt các màn thuộc bộ smoke cố định: 「チャット管理」, Chat 1:1, 友だちリスト, メッセージ配信, テンプレート, và màn thanh toán/hợp đồng.<br>2. Ở **từng màn**: mở DevTools tab Network kiểm tra JS/CSS trả **200 kèm tham số version mới**, không có 404.<br>3. Ở từng màn: chạy 1 thao tác chính (VD gửi 1 tin test, mở 1 template, áp 1 bộ lọc) và xác nhận không lỗi.<br>4. Ghi lại màn nào có asset 404 hoặc thao tác lỗi.<br>5. Đối chiếu danh sách màn đã test với danh sách Dev cung cấp — báo thiếu nếu có màn chưa được liệt kê. | Không nhập liệu; đối tượng kiểm tra là **phạm vi ảnh hưởng của biến version dùng chung** | **Mọi màn** trong danh sách tải asset với tham số version mới, trả 200, không 404, không lỗi Console mới phát sinh (ngoài lỗi CSS-trong-thẻ-script đã biết ở bug #671). Thao tác chính của từng màn chạy đúng ngay sau **F5 thường**. Không màn nào phải Ctrl+F5 / xoá cache mới dùng được. | | Lấp GAP-9 (M-10, AP-3) / cover impact **F2, T2** · Đánh giá spec: Spec không ghi danh sách màn → **BẮT BUỘC lấy danh sách từ Dev trước khi test** (REG-SHARED-001) · Evidence: **danh sách nơi ảnh hưởng do Dev cung cấp + kết quả test từng nơi** · regression · **RULE-08 + RULE-12** (bộ smoke cố định) |
| TC-DEPLOYASSET001-02 | API | DEPLOY-ASSET-001 | Nâng version asset dùng chung | Abnormal | manual | product | Font và icon-font sau khi nâng version — không tofu, không lúc có lúc mất | - Như TC-REGSHARED001-02<br>- Chuẩn bị nội dung test chứa **kanji + kana + dấu tiếng Việt** (VD tên bạn bè `グエン Đặng Thuỳ 髙﨑`) đã lưu sẵn trong hệ thống | 1. Sau deploy, F5 thường màn 「チャット管理」 và Chat 1:1.<br>2. Soi hiển thị chuỗi kanji + kana + dấu tiếng Việt: không có ký tự **tofu (ロ / □)**, không ký tự bị thay bằng font dự phòng khác kiểu.<br>3. Kiểm DevTools Network: file font trả **200 kèm version mới**, không 404, không fallback sang font hệ thống.<br>4. **Tải lại trang 5–10 lần liên tiếp**, mỗi lần quan sát toàn bộ icon trên thanh công cụ và trong bảng.<br>5. Ghi nhận nếu có lần nào icon bị mất / hiện thành ô vuông / hiện sai icon.<br>6. Lặp lại bước 4 trên 1 trình duyệt thứ hai. | Chuỗi `グエン Đặng Thuỳ 髙﨑`; tải lại trang 5–10 lần | Font tải đúng version mới, **không fallback**; toàn bộ glyph kanji / kana / dấu tiếng Việt hiển thị đủ, **không tofu**. Icon-font hiển thị **ổn định qua mọi lần tải lại** — không có hiện tượng lúc có lúc mất. Kết quả nhất quán trên cả 2 trình duyệt. | | Lấp GAP-10 (M-12) / cover impact F2, T2 · Đánh giá spec: Spec ghi rõ (`DEPLOY-ASSET-001` mục 5, 6) · Evidence: screenshot DevTools Network (version + 200) + screenshot màn sau **F5 thường** trên browser còn cache bản cũ · **RULE-08: phải verify trên một lần deploy thật** |

**Tổng: 17 TC đề xuất**, lấp 10 GAP. Phân bố loại case: **Normal 8 · Abnormal 6 · Boundary 3** (47/35/18 — cân hơn hẳn bộ TC gốc 77/14/9). Tất cả đều `Chạy = manual`; `Phạm vi ENV`: product 11 · staging 5 · Tất cả 1.

RULE-01 (quan điểm **Cao** cần đủ Normal + Abnormal + Boundary):
- `CONC-003` (Cao): ✅ đủ 3 — TC-CONC003-01/02/03.
- `DATA-DB-001` (Cao): ✅ đủ 3 — TC-DATADB001-01/02/03.
- `COMPAT-LEGACY-001` (Cao): ✅ đủ 3 — TC-COMPATLEGACY001-01/02/03.
- `BULK-001` (Cao): ⚠️ **thiếu Boundary** — lý do: biên của BULK-001 ở màn này là "lọc còn đúng 1 tin" và "lọc ra toàn bộ", **đã được cover** bởi TC-DATADB001-03 (biên 1 phần tử) và TC-SELECTSCOPE001-02 (toàn bộ, đang fail). Không đẻ TC trùng.
- `CONC-001` (Cao): ⚠️ vẫn **thiếu kịch bản (3) 2 user khác nhau và (4) batch đa luồng** — lý do: cần 2 tài khoản staff riêng và công cụ chạy batch, đề nghị Leader quyết định có mở rộng phạm vi #28418 hay tách ticket regression riêng.
- `DEPLOY-ASSET-001` (Cao): ⚠️ **thiếu Boundary** — lý do: quan điểm này không có khái niệm biên định lượng; Normal đã có sẵn TC-DEPLOYASSET001-01 (đang fail).
- `DATA-COUNT-001` (Cao): ⚠️ **thiếu Abnormal + Boundary** — lý do: đề nghị bổ sung ở vòng sau sau khi Leader chốt cách xử lý **friend đã block** trong mẫu số (§6 SPEC-02); viết TC biên trước khi chốt chuẩn sẽ phải viết lại.
- `SYNC-APP-001` (Trung bình → Cao với flow user-facing): 1 Normal, đạt mức tối thiểu.
- `DATA-001` (Cao): ⚠️ chỉ 1 Normal — ưu tiên xác lập được luồng đồng bộ tìm kiếm trước; bổ sung Abnormal (sync đứt giữa chừng) ở vòng sau.

---

## 6. Spec update needed

| # | Điểm cần chốt | Hiện trạng | Ai chốt |
|---|---|---|---|
| **SPEC-01** | **Badge web có cập nhật realtime không?** | Spec **BR-07** (Confidence Cao) khẳng định có broadcast `InfoEvent` qua WebSocket cập nhật realtime web. TC-OUTTRUTH001-01 lại ghi expected là **có thể stale trước F5**. Hai bên mâu thuẫn trực tiếp → là gốc của `[BLOCKER] B-01`. | **Dev + Leader** — xác nhận `InfoEvent` có được phát ở màn `talk-list` không; nếu không thì sửa spec, nếu có thì sửa TC và raise bug. |
| **SPEC-02** | **Tin của bạn bè ĐÃ BLOCK có được tính vào số chưa xác nhận không?** | `DATA-COUNT-001` yêu cầu làm rõ mẫu số; spec FA-002 **không ghi**. Ảnh hưởng trực tiếp tới oracle của TC-DATACOUNT001-01. | **Leader + PM** |
| **SPEC-03** | **Hành vi đúng khi bot trong phiên bị đổi ở tab khác** | Spec không ghi. TC-DATADB001-02 hiện chấp nhận 2 hành vi (đổi đúng bot A **hoặc** báo lỗi rõ ràng) — cần chốt 1. | **Dev + Leader** |
| **SPEC-04** | **Modal chi tiết với tin ở bảng legacy** | BR-11 ghi rõ **hạn chế** (chỉ đọc `messages_v2s`) nhưng **không ghi hành vi mong đợi** của modal khi không tìm thấy tin (báo lỗi? hiện rỗng? ẩn nút?). | **Dev + Leader** |
| **SPEC-05** | **Cơ chế chống xử lý trùng khi đổi trạng thái** | Bug #670 cho thấy double-click tạo **2 bản ghi** `unconfirm_message` trùng. Kho `fa001` **TC-CHT-43** đã chốt chuẩn *"chỉ tính 1 lần"* cho tính năng anh em 「全て確認済みに変更」. → **Chuẩn của 2 màn đang không đồng nhất trên thực tế.** | **Dev + Leader** — chốt endpoint EP-06 có phải idempotent không, rồi cập nhật spec FA-002. |
| **SPEC-06** | **Mục 4.2 của `03-dev-impact.md` khai thiếu data impact** | Khai "không có" trong khi spec §4.3 liệt kê 6 bảng/cột bị ghi (xem §3). | **Dev** — bổ sung mục 4.2 rồi rà lại coverage. |
| **SPEC-07** | **4 mã quan điểm Studio không tồn tại trong `framework/checklist-lme.md`** | `SELECT-SCOPE-001`, `TOOL-KNOW-002`, `TOOL-NEGCTRL-001`, `API-CONTRACT-001` — phủ 15/22 TC. | **Leader** — bổ sung vào framework theo **RULE-10**, hoặc ban hành bảng map chính thức Studio ⇄ framework. |

---

## 7. Checklist đã chạy

| Mục | Kết quả | Ghi chú |
|---|---|---|
| **A.1** Bug root cause | ✅ **Pass** | TC-TOOLKNOW002-01 mô phỏng **chính xác** steps file 01 (一覧 → confirm → unconfirm), expected khớp cách fix |
| **A.2** Function impact (4.1) | ⚠️ **Partial** | F1/F3/F4 OK; **F2 RISK** — 2/3 TC không có kết luận (1 fail + 1 chưa chạy) |
| **A.3** Data impact (4.2) | ❌ **Fail** | Dev khai "không có data impact" → **sai**; 3 data thật sự bị ghi hoàn toàn không có TC (`sync_elasticsearch`, `conversation.status_last_message`, `messages.is_confirmed`) |
| **A.4** Feature impact (4.3) | ❌ **Fail** | T1 RISK; **T2 GAP** — 0 TC mở màn khác sau bump version |
| **A.5** Gap & orphan | ⚠️ **Partial** | 2 TC API là AP-5 (đã note đúng, đề nghị tách ticket); TC-REGSHARED001-01 không phải TC chạy được |
| **A.6** Fix-shape adversarial | ❌ **Fail** | Xem §3.5 — thiếu font/icon, thiếu danh sách nơi ảnh hưởng từ Dev, dính AP-2/AP-3/AP-5 |
| **B.1** Rõ ràng | ✅ **Pass** | Steps đánh số rõ, precondition đầy đủ, expected đo lường được — chất lượng cao hơn mức trung bình của TC AI sinh |
| **B.2** Atomic | ✅ **Pass** | Mỗi TC 1 mục đích chính |
| **B.3** Độc lập | ✅ **Pass** | Không TC nào phụ thuộc TC khác |
| **B.4** Realistic | ⚠️ **Partial** | Precondition của TC-SELECTSCOPE001-02 (>100 tin, nhiều trang) **không dựng được ở local** — chính là lý do run #401 hiểu nhầm; TC-DATACACHE001-01 cần một lần deploy thật nên chưa từng chạy |
| **C** Chất lượng bộ TC | ❌ **Fail** | Tỷ lệ **Normal 17 : Abnormal 3 : Boundary 2** (77/14/9) — lệch nặng so với gợi ý 40/35/25. **11/22 TC dồn vào 1 quan điểm** (`SELECT-SCOPE-001`) trong khi 4 quan điểm Cao trống hoàn toàn. Không có TC phân quyền / role |
| **D** Spec alignment | ❌ **Fail** | TC-OUTTRUTH001-01 **mâu thuẫn BR-07** (B-01). Business rule chưa có TC: BR-02, BR-04, BR-06, BR-07 (phần FCM), BR-09/BR-10, BR-11 |
| **E** Hành chính | ⚠️ **Partial** | TC ID trên Studio dùng `temp_id` (m-06); `04-tc-list.md` đã lưu đúng folder; **checkbox verify auto-fill của cả file 01 và 03 chưa tick** (M-13) |
| **F.1** Quan điểm tầng 1 | ❌ **Fail** | Xem bảng bên dưới — 4 quan điểm **Cao** trigger khớp mà 0 TC cover |
| **F.2** Catalog tầng 2 | ❌ **Fail** | **B** (thành phần UI): màn có checkbox / loadmore / filter / badge nhưng không rà theo `UIC-*`. **D/D2**: task chạm deploy/asset mà **0 TC chạy production** → vi phạm RULE-08. **C**: chưa duyệt hết khối liên quan (đa bot, friend đã block) |
| **F.3** RULE quy trình | ❌ **Fail** | **RULE-02** vi phạm (m-05, TC không ghi loại evidence bắt buộc) · **RULE-06** vi phạm (M-07, không tới mobile app) · **RULE-07** vi phạm (B-02, không có TC `WHERE` scope 2 tài khoản) · **RULE-08** vi phạm (M-02, 0 TC production) · **RULE-09** vi phạm (B-04, không test nhánh dữ liệu cũ) · **RULE-12** vi phạm (M-10, không có vùng ảnh hưởng từ Dev) |

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Exec | Kết luận |
|---|---|---|---|---|---|
| `FUNC-SEQ-001` | Cao | ✅ Chuỗi thao tác liên tiếp không reload — **chính là root cause** | TC-FUNCSEQ001-01, -02 | 2/2 | ✅ **Cover** (nhưng thiếu Abnormal + Boundary → RULE-01) |
| `CONC-003` | **Cao** (màn có loadmore + filter) | ✅ Race tầng client, sát root cause nhất | **— 0 TC** | — | ❌ **`[BLOCKER]` B-03** |
| `DATA-DB-001` | **Cao** | ✅ BẮT BUỘC với mọi UPDATE/DELETE | **— 0 TC** | — | ❌ **`[BLOCKER]` B-02** |
| `COMPAT-LEGACY-001` | **Cao** | ✅ Tin nhắn shard theo năm (BR-02) + `messages.is_confirmed` legacy | **— 0 TC** | — | ❌ **`[BLOCKER]` B-04** |
| `BULK-001` | **Cao** | ✅ Bộ lọc + thao tác hàng loạt | TC-SELECTSCOPE001-02 (**fail**), TC-APICONTRACT001-02 (**fail**) | 0/2 | ❌ **`[BLOCKER]` B-05** — có TC nhưng **cả 2 đều fail**, và thiếu hẳn phép đếm khớp 100% |
| `OUT-TRUTH-001` | Cao | ✅ Thao tác có thông báo kết quả | TC-OUTTRUTH001-01 | 1/1 | ❌ **`[BLOCKER]` B-01** — expected trái spec BR-07 |
| `CONC-001` | Cao | ✅ Nút thực thi hành động quan trọng | TC-CONC001-01 (**fail**) | 0/1 | ⚠️ **`[MAJOR]` M-11** — chỉ 1/4 kịch bản, kịch bản đó fail |
| `DEPLOY-ASSET-001` | Cao | ✅ Release sửa file JS + nâng version asset | TC-DEPLOYASSET001-01 (**fail**) | 0/1 | ⚠️ **`[MAJOR]` M-12, M-16** — thiếu font/icon; oracle Console không đạt được |
| `DATA-COUNT-001` | Cao | ✅ Màn có badge số chưa xác nhận | TC-OUTTRUTH001-01 (một phần) | 1/1 | ⚠️ **`[MAJOR]` M-14** — chỉ 1 nguồn, không có phép tính tay |
| `PERM-003` | Cao | ✅ LME có change bot; màn gắn `bot_id` | **— 0 TC** | — | ⚠️ **`[MAJOR]` M-15** |
| `REG-SHARED-001` | Cao | ✅ `config/sns-line.php` là config dùng chung | TC-REGSHARED001-01 (chỉ diff tĩnh) | 1/1 | ⚠️ **`[MAJOR]` M-10** — không test nơi nào bị ảnh hưởng |
| `SYNC-APP-001` | Trung bình → **Cao** (badge user-facing) | ✅ BR-07 gửi FCM push tới mobile app | **— 0 TC** | — | ⚠️ **`[MAJOR]` M-07** (RULE-06) |
| `DATA-001` | Cao | ✅ Dữ liệu tham chiếu ở nơi khác (search index, Chat 1:1) | **— 0 TC** | — | ⚠️ **`[MAJOR]` M-08** |
| `DATA-CACHE-001` | Trung bình → Cao | ✅ Release đổi JS/asset | TC-DATACACHE001-01 (**chưa chạy**) | 0/1 | ⚠️ **`[MAJOR]` M-02** — có TC nhưng chưa từng chạy |
| `LIST-001` | Trung bình | ✅ Màn danh sách có search/filter/pagination | TC-SELECTSCOPE001-03…-07 (gián tiếp) | 5/5 | ⚠️ **`[MINOR]`** — thiếu mục (4) "click vào số đếm mở đúng danh sách" và mục (1) search bằng cả tên LINE lẫn tên quản lý |
| `STATE-001` | Trung bình | ✅ Đổi trạng thái có lifecycle | TC-FUNCSEQ001-01 (F5 giữ trạng thái) | 1/1 | ✅ **Cover** |
| `PERM-001` | Cao | ⚠️ Chưa rõ — spec FA-002 không có role matrix | **— 0 TC** | — | ⚠️ **`[NIT]`** — theo PERM-001 *"phải có role matrix trong spec trước khi test"*; kho FA-001 **MT-17** ghi nhận phân quyền Staff ở Chat 1:1 spec **tự nhận CHƯA XÁC ĐỊNH** → nêu để Leader quyết, không flag MAJOR khi chưa có chuẩn |
| `SELECT-SCOPE-001` ⚠️ | — | Mã **không có** trong framework | 11 TC | 9/11 | ⚠️ **Không tính là cover quan điểm** (M-05) — gần map nhất là `BULK-001` + `LIST-001` |
| `TOOL-KNOW-002` ⚠️ | — | Mã **không có** trong framework | 1 TC | 1/1 | ⚠️ Không tính (M-05) |
| `TOOL-NEGCTRL-001` ⚠️ | — | Mã **không có** trong framework | 1 TC | 1/1 | ⚠️ Không tính (M-05) — gần map nhất là đối chứng âm của `DATA-DB-001` |
| `API-CONTRACT-001` ⚠️ | — | Mã **không có** trong framework | 2 TC | 1/2 | ⚠️ Không tính (M-05) |

**Tổng kết coverage quan điểm**: trong **13 quan điểm ưu tiên Cao** trigger khớp task, chỉ **2** đạt (`FUNC-SEQ-001`, `STATE-001`), **5** dính BLOCKER, **6** dính MAJOR.

---

## 8. Ký duyệt

| Vai trò | Tên | Ngày | Kết luận |
|---|---|---|---|
| Người review (draft) | Claude — `/review-tc` | 2026-08-27 | ❌ **REJECTED** — 5 BLOCKER |
| Test Leader verify | `<chưa ký>` | | |
| Member nhận feedback | `trangnq` | | |

> ⚠️ **Đây là draft do `/review-tc` sinh, KHÔNG phải kết luận cuối.** Leader bắt buộc verify trước khi trả về member — đặc biệt 3 điểm sau vì chúng thay đổi phạm vi nghiệm thu ticket:
> 1. **B-01** — cần Dev xác nhận `InfoEvent` WebSocket có phát ở màn `talk-list` không.
> 2. **B-05** — Leader chốt bug #668/#669 có chặn #28418 hay tách ticket riêng.
> 3. **M-09 / SPEC-06** — Dev bổ sung mục 4.2 `03-dev-impact.md` rồi rà lại toàn bộ coverage.
