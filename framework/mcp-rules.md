# Rule test tính năng MCP (LME MCP tool)

> **Bắt buộc với mọi task MCP** — task nằm trong folder `MCP/` ở gốc repo (tạo bởi `/new-task-mcp`).
> Đọc bởi `/review-docs-mcp` (BƯỚC 4 — docs có nói gì về các rule này không), `/write-tc-mcp` (BƯỚC 2 → 4 — viết TC theo các rule này) và `/review-tc-mcp` (BƯỚC 2 → 4 — bộ TC có cover các rule này không).
> File này **bổ sung**, không thay thế [checklist-lme.md](checklist-lme.md) + [catalog-lme.md](catalog-lme.md): mỗi rule ghi rõ **mã quan điểm checklist** mà TC dùng để map coverage. Chỉ 2 mã mới `MCP-E2E-001` / `MCP-E2E-002` (mục 3) được định nghĩa riêng ở đây.
>
> "MCP tool" = tool LME expose qua MCP server cho client AI (ChatGPT / Claude…) — vd `create_form_survey`, `update_tag`, `list_friends`, `get_form_detail`. Danh sách tool + param của từng task lấy ở `MCP/<folder>/_tool-inventory.md` (do `/review-docs-mcp` sinh từ docs MCP ở `spec-features/mcp/docs/`).

---

## 1. 8 rule bắt buộc

| Rule | Nội dung | Mã quan điểm cho TC | Expected |
|---|---|---|---|
| **MCP-RULE-01** Bảo mật bot A ↔ bot B | Bot A **không** được get/list · sửa · xoá · **truyền ID** dữ liệu của bot B. Xem ma trận 2.1 | `PERM-002` · `SEC-001` | **403 / 404** |
| **MCP-RULE-02** Phân quyền staff | Staff **có** quyền tính năng → gọi được mọi tool của tính năng. Staff **không** có quyền → **mọi tool của tính năng bị chặn, kể cả tool đọc** (`list_*` / `get_*`). Bị thu hồi quyền khi OAuth token MCP **vẫn còn hiệu lực** → lần gọi kế tiếp bị chặn | `PERM-001` · `PERM-004` + catalog `MAP-PERM-01` | **403** (RULE-13) |
| **MCP-RULE-03** Limit bot Free | Bot **Free** bắt buộc test limit số lượng của tính năng: tạo tới ngưỡng thì được, vượt ngưỡng bị chặn. **Limit đếm gộp dữ liệu tạo từ web + MCP**. Khôi phục / copy trên web khi đã đủ limit (có bản tạo từ MCP) cũng bị chặn. Bot Free cũ (`flag_contract_new = 0`) → tra quy tắc riêng của tính năng (vd form: không giới hạn — Leader chốt #39446) | `PAY-LIMIT-001` + catalog `MAP-PLAN-01/02/03` | **400 hoặc 422** |
| **MCP-RULE-04** Không trùng tên quản lý | Tính năng có **tên quản lý (管理名)** bắt buộc duy nhất trong bot: MCP vs MCP · MCP vs dữ liệu tạo từ web · **đổi tên qua `update_*`** trùng tên có sẵn · khác hoa/thường, khoảng trắng đầu/cuối · **cùng tên ở bot khác → được phép** | `FUNC-UNIQ-001` | **400 hoặc 422** (trùng) / 200 (bot khác) |
| **MCP-RULE-05** Get sau ghi | Mọi TC `create_*` / `update_*` thành công **phải có bước gọi tool `get_*`** (hoặc `list_*`) để verify dữ liệu đã lưu đúng từng param vừa truyền. Có output phía web / LINE user thì kiểm thêm (vd form tạo qua MCP mở được trên editor web, form công khai hiển thị đúng) | (bước trong TC — không phải mã riêng) | giá trị `get_*` = giá trị đã truyền |
| **MCP-RULE-06** Phủ param | Mỗi param của mỗi tool đi đủ ma trận 2.2. Test sai kiểu dữ liệu phải gọi qua **raw MCP client** — client có typed-wrapper tự chặn trước khi gửi **không tính** là server đã validate | `FUNC-002` · `FUNC-003` · `FUNC-004` | xem 2.2 |
| **MCP-RULE-07** Expected validate | **400 hoặc 422 đều Đạt** (khớp RULE-13 — Leader gộp 400 / 422 từ 2026-10-14). Message lỗi **không cần giống web**, tiếng Anh được, nhưng phải nêu rõ nguyên nhân. MCP phải chặn **mọi** kịch bản web chặn, **kể cả kịch bản web chặn ngầm** (không hiện message). Cross-bot **không** nới: giữ 403 / 404 | RULE-13 | 400 / 422 |
| **MCP-RULE-08** E2E prompt | TC dùng prompt ngôn ngữ tự nhiên qua client AI thật — xem mục 3 | `MCP-E2E-001` · `MCP-E2E-002` | chuỗi tool + param + trạng thái cuối |

> Leader chốt 2026-10-14 (review #39446): MCP-RULE-01 · 02 · 03 · 04 · 07. Rule riêng của từng tính năng (giới hạn ký tự, điều kiện rẽ nhánh…) lấy từ `spec-features/` + kho-tcs, **không** ghi vào file này.

---

## 2. Ma trận chi tiết

### 2.1 MCP-RULE-01 — ma trận bot A ↔ bot B

**Mỗi param kiểu ID** của tool (`*_id`, `folder_id`, `tag_id`, `action_id`, `friend_info_id`, `template_id`, `form_id`… — lấy đủ từ `_tool-inventory.md`) × **4 giá trị**:

| Giá trị truyền vào | Expected |
|---|---|
| ID thuộc **bot khác cùng account** (1 user sở hữu 2 bot, `bot_id` bot A + ID của bot B) | 403 / 404, dữ liệu bot B không đổi |
| ID thuộc **account khác** | 403 / 404, dữ liệu account kia không đổi |
| ID **không tồn tại** | 404 (hoặc 400 / 422 nếu tool coi là validate) |
| ID **sai loại** (vd `tag_id` truyền vào `action_id`) | 400 / 422 |

Cộng thêm theo **thao tác**:
- **get / list**: `bot_id` của bot không thuộc user → 403 / 404, không lộ dữ liệu.
- **update / xoá**: ID đối tượng của bot B → 403 / 404, **verify lại bằng `get_*` phía bot B** dữ liệu không đổi.
- **Truyền dữ liệu**: tạo đối tượng ở bot A nhưng gắn ID con của bot B (tag, action, friend info, folder…) → bị chặn, không tạo nửa chừng.

### 2.2 MCP-RULE-06 — ma trận param

| Chiều | Ca test | Loại case |
|---|---|---|
| Bắt buộc | Thiếu param bắt buộc · truyền `null` · chuỗi rỗng / chỉ khoảng trắng | Abnormal |
| Kiểu | Sai kiểu (`"abc"` cho số, số cho chuỗi, object cho array…) — **raw MCP client** | Abnormal |
| Enum | Giá trị ngoài tập enum · sai hoa/thường | Abnormal |
| Biên | min · max · max + 1 (ký tự / số lượng / giá trị) — lấy từ docs, **đối chiếu spec + kho** | Boundary |
| Default | Bỏ trống param tuỳ chọn → nhận đúng default docs ghi | Normal |
| Param lạ | Truyền param không có trong schema → bỏ qua hoặc từ chối, **không** lưu rác | Abnormal |
| Kết hợp | Param phụ thuộc nhau (bật A mới được set B; param chỉ dùng cho 1 nhánh `type`) | Abnormal |
| Validate web | Mọi kịch bản validate của màn web tương ứng (spec + kho) áp sang MCP — MCP-RULE-07 | Abnormal |

Mỗi TC Abnormal / Boundary ghi **mã HTTP cụ thể** ở `Kết quả mong đợi` (RULE-13 + MCP-RULE-07).

### 2.3 MCP-RULE-05 — mẫu bước "get sau ghi"

```
1. Gọi `create_<x>` với <param = giá trị cụ thể>.
2. Ghi lại <x>_id trả về.
3. Gọi `get_<x>_detail` với <x>_id vừa tạo.
4. Mở màn web <Tên VN> <Tên JP> của bot, tìm <x> vừa tạo.        ← khi tính năng có màn web
```
Expected liệt kê **từng param** đã truyền và giá trị `get_*` trả về / web hiển thị tương ứng.

---

## 3. MCP-RULE-08 — TC E2E bằng prompt ngôn ngữ tự nhiên

Mục đích: kiểm **người dùng cuối** dùng client AI (ChatGPT / Claude) gọi được đúng tool, đúng param, ra đúng kết quả — không chỉ tool đúng khi gọi tay.

### 3.1 Phủ bắt buộc mỗi tool

| Tool | VN chi tiết | VN chung | Tiếng Nhật |
|---|---|---|---|
| `create_*` / `update_*` / `send_*` | ≥ 1 | ≥ 1 | ≥ 1 (chi tiết **hoặc** chung) — đại diện |
| `get_*` / `list_*` | — | ≥ 1 | không bắt buộc |

Tiếng Việt là chính; tiếng Nhật chỉ đại diện vài case mỗi tool.

### 3.2 2 kiểu prompt

| Mã | Kiểu | Người dùng | Cách viết |
|---|---|---|---|
| `MCP-E2E-001` | **Chi tiết** | Hiểu rõ tool, biết cần truyền gì | Nêu **giá trị cụ thể** ánh xạ được ra param. Không cần gọi tên param kỹ thuật |
| `MCP-E2E-002` | **Chung** | Không biết tool, chỉ biết mục đích | Chỉ nêu **mục đích nghiệp vụ**. **Không** nêu tên tool / tên param |

Ví dụ — tạo form trả lời (`create_form_survey` + `update_form_survey`):
- **Chung**: *"Tôi muốn tạo form khảo sát các khách hàng đã sử dụng dịch vụ A của salon XXX. Yêu cầu form thu thập đủ các thông tin cá nhân, mức độ hài lòng sau khi sử dụng."*
- **Chi tiết**: *"Tôi muốn tạo form khảo sát cho các khách hàng đã sử dụng dịch vụ A của salon XXX. Yêu cầu form thu thập đủ thông tin cá nhân họ tên, số điện thoại, ngày tháng năm sinh, địa chỉ, mức độ hài lòng gắn vào info F1, các điểm cải thiện gắn vào info F2, sau khi trả lời xong thì gắn tag T11 cho khách hàng, button trả lời màu hồng, chữ đậm."*
- **JP (chung)**: *「サロンXXXのサービスAを利用したお客様向けにアンケートフォームを作りたいです。個人情報と利用後の満足度を回答してもらえるようにしてください。」*

### 3.3 Oracle — chấm cái gì

- **Chuỗi tool được gọi + thứ tự** (vd `list_tags` → `create_form_survey` → `update_form_survey`).
- **Param đã resolve đúng**: tên trong prompt → ID thật của **đúng bot** (tag "T11" → `tag_id` của T11; info "F1" → `friend_info_id` của F1). Đặc biệt **không** lấy ID của bot khác.
- **Trạng thái cuối**: verify bằng `get_*` + màn web (MCP-RULE-05). Prompt chi tiết → **từng yêu cầu** trong prompt có mặt trong kết quả. Prompt chung → kết quả **hợp mục đích** (vd form có nhóm câu hỏi thông tin cá nhân + mức độ hài lòng).
- **KHÔNG chấm câu trả lời chữ** của AI. Khác cách diễn đạt / khác model / thêm bước đọc phụ (`list_*`, `get_*`) vẫn Đạt.

### 3.4 Prompt abnormal (≥ 1 mỗi nhóm tính năng)

| Ca | Expected |
|---|---|
| Prompt chung **thiếu dữ liệu bắt buộc** (vd không nói tên form) | AI hỏi lại hoặc dùng default hợp lý — **không bịa ID**, không tạo dữ liệu rác |
| Prompt nhắc tên **không tồn tại** trong bot (tag "T99" chưa có) | AI báo không tìm thấy / hỏi lại — không gắn nhầm tag khác |
| Prompt yêu cầu thao tác dữ liệu **của bot khác** | Tool trả 403 / 404, AI báo không có quyền — dữ liệu bot kia không đổi |
| Prompt từ account **staff không có quyền** tính năng | Tool bị chặn, AI báo không có quyền |

### 3.5 Ghi TC E2E vào bảng 15 cột

| Cột | Ghi gì |
|---|---|
| `Mã quan điểm` | `MCP-E2E-001` (chi tiết) / `MCP-E2E-002` (chung) — prompt abnormal bảo mật / quyền dùng `PERM-002` / `PERM-001` |
| `Nhóm` | `API` |
| `Màn hình/chức năng` | Dòng đầu = chuỗi tool **kỳ vọng** (`create_form_survey / update_form_survey`), `<br>` + `MCP prompt <VN/JP>: <mục đích>` |
| `Surface` | `mcp` đứng đầu; thêm `, web` khi có bước mở màn web kiểm kết quả (vd `mcp, web`) |
| `Chạy` | **`manual`** — `Ghi chú`: `manual vì client LLM thật (ChatGPT/Claude), phi tất định` (ngoại lệ thứ 5 của cột `Chạy`, chỉ cho MCP-RULE-08) |
| `Tiền điều kiện` | Client AI nào · connector MCP nào · OAuth của account / staff nào · bot nào · **dữ liệu sẵn có** (tag T11, info F1/F2…) chép đủ |
| `Các bước` | 1. Mở client AI, kết nối connector MCP …<br>2. Gửi prompt (ở `Dữ liệu nhập`)<br>3. Trả lời câu hỏi lại của AI nếu có: `<câu trả lời>`<br>4. Xem log tool call của client<br>5. Gọi `get_*` / mở màn web verify. Studio hiện bỏ qua `exec_mode` → bước cần người phải viết rõ ở đây |
| `Dữ liệu nhập` | **Prompt nguyên văn** (VN hoặc JP) |
| `Kết quả mong đợi` | `- Tool được gọi: …`<br>`- Param: … = …`<br>`- get_*: …`<br>`- Màn web: …` |
| `Ghi chú` | Mở đầu `Prompt: VN-chi tiết` / `VN-chung` / `JP-chi tiết` / `JP-chung` · `Lấp …` · `manual vì …` |

### 3.6 Định nghĩa 2 mã quan điểm mới

| Mã | Ưu tiên | Trigger | Kiểm tra | Evidence |
|---|---|---|---|---|
| `MCP-E2E-001` | Cao | Mọi task MCP có tool `create_*` / `update_*` / `send_*` | Prompt **chi tiết** → client AI gọi đúng tool, resolve đúng param, kết quả cuối khớp **từng yêu cầu** trong prompt | Log tool call của client + response `get_*` + screenshot màn web |
| `MCP-E2E-002` | Trung bình (→ Cao khi tool ghi dữ liệu) | Mọi task MCP | Prompt **chung** (chỉ mục đích) → client AI tự chọn tool hợp lý, không bịa ID, kết quả hợp mục đích | Log tool call + response `get_*` |

`GROUP_MAP` ([kho-tcs/data/_common.py](../kho-tcs/data/_common.py)) map tiền tố `MCP-` → `API`.

---

## 4. Áp dụng ở 2 skill

| Skill | Dùng file này để |
|---|---|
| `/review-docs-mcp` | §4 `DOC-MISS`: docs **không nói gì** về MCP-RULE-01 → 04 (tool có chặn bot khác / staff / limit Free / trùng tên không) → 1 dòng trong report cho Leader đọc. Docs nói **trái** rule → `DOC-SPEC` |
| `/review-tc-mcp` | §1 ma trận param (MCP-RULE-06) · §2 bảng MCP-RULE-01 → 07 · §3 E2E prompt (MCP-RULE-08) · §7 viết TC theo mục 2 + 3 |
| `/write-tc-mcp` | Lập ô yêu cầu theo mục 2 (ma trận param · bot A↔B · staff · limit · trùng tên · validate) + mục 3 (prompt) → viết TC vào `04-tc-write.md` |
