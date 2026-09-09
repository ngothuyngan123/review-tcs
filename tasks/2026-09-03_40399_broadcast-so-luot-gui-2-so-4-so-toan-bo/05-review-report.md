# 05 — Review Report

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| **Nguồn đã dùng** | **NGUỒN 1 — MCP LME TEST STUDIO**, `task_id = 272`, ticket `40399` |
| Vì sao không dùng nguồn dưới | Nguồn 1 có TC → **dừng ngay**, KHÔNG fetch Sheet human, KHÔNG đối chiếu chéo với file `04-tc-list.md` |
| Thời điểm fetch | 2026-09-03 (`testcase_list` + `task_get_context` + `task_get_report` + `review_list_comments`) |
| Tổng TC lấy về | **19** |
| Task Studio | `status = tc-ready` · `round = 1` · `branch = ai_fixbug_40399` · `aiResult = null` · `reviewState = leader` · `reviewed = false` · `submittedWithoutMcp = false` |
| `exec` | total 19 · pass 17 · fail 0 · other 1 (`skip`) · untested 1 |
| Comment vòng review trước | `review_list_comments` = **rỗng** → chưa có vòng review nào, không có issue đã đóng cần tránh raise lại |
| **Nguồn spec đã dùng** | ① [spec-features/admin/message-send-all/feature-spec.md](../../spec-features/admin/message-send-all/feature-spec.md) — §4 hàng 6/7/17 (mapping `配信数` → `broadcast.filter_number`), §5 **BR-06** (filter_number là cache, nút 「再計算」), **BR-07** (Sao chép broadcast), **BR-08** (Bot Switch Guard), Hành động 4 (dòng 110) · ② [templates/LME-SYSTEM-SPEC.md §3.7 FA-008](../../templates/LME-SYSTEM-SPEC.md) dùng làm mục lục |
| Kho TCs đối chiếu | [kho-tcs/fa008-broadcast-メッセージ配信.md](../../kho-tcs/fa008-broadcast-メッセージ配信.md) — nhóm 「配信先絞込み & 再計算」(21 TC) · 「配信数 & danh sách friend đã gửi」(17 TC) · 「Copy broadcast」(14 TC) · 「配信数上限アラート」(3 nhóm, 39 TC) · 「Job gửi & vòng đời trạng thái」(7 TC) |
| Snapshot đã ghi | `04-tc-list.md` đã có header `<!-- source: MCP LME TEST STUDIO ... -->` (do `/new-task` sinh cùng ngày, cùng `task_id=272`, cùng 19 TC) → **không cần refresh**, nội dung trùng khít |

### 0.6 — Cảnh báo chất lượng nguồn (Studio)

| # | Nội dung | Kết quả | Flag |
|---|---|---|---|
| 1 | **Kết quả thực thi thật** | `pass` 17/19 = **89,5%** (≥ 80%) | Không flag theo ngưỡng. **NHƯNG** xem #7 — 17 `pass` này không kiểm chứng được |
| 2 | **TC `fail` / `error` / gắn ticket bug** | `fail` = 0 · `error` = 0 · `bug_tickets` rỗng toàn bộ · `openBugs = 0` | Không có TC fail chưa raise ticket ✓ |
| 3 | **Môi trường đã chạy** | **100% `staging`** (18/18 lần chạy). **0 TC chạy `production`**. Task chạm **job nền** (broadcast gửi bằng Spring Boot job poll bảng `broadcast`) và **quota tin nhắn** | **`[MAJOR]` RULE-08 / ENV-003** |
| 4 | **Ai chạy** | 100% `source = manual`, `by = anhptn` (**QA người chạy tay**). Auto run `#816` env `staging` đang **`queued` — chưa từng chạy**; `auto.totals` = pass 0/fail 0/skip 0/error 0. `submittedWithoutMcp = false` | **`[MAJOR]`** — 19/19 TC khai `exec_mode = auto` nhưng runner chưa chạy lần nào |
| 5 | **Tác giả TC** | **18/19 do AI sinh** (`provenance.source = ai`, `created_job_id = 832`) = 94,7%; 1 TC do người viết (`#15552`, `provenance.source = human`, `author = anhptn@mcp`). `reviewState = leader`, **chưa `done`** | **`[MAJOR]`** — ≥ 50% TC do AI sinh mà review chưa `done` |
| 6 | **Mã quan điểm Studio ngoài `checklist-lme.md`** | **5 mã / 7 TC**: `TOOL-KNOW-002` (2) · `TOOL-SCOPE-001` (1) · `TOOL-NEGCTRL-001` (2) · `DATA-HIST-001` (1) · `PERF-LATENCY-001` (1). Prefix `TOOL-*` không tồn tại trong checklist; `PERF-*` chỉ có `PERF-LARGE-001`; `DATA-*` có 9 mã, không có `DATA-HIST-*` | **7 TC này KHÔNG được tính là cover** ở §3 / §3.6 |
| 7 | **Evidence** (bổ sung — `task_get_report`) | **`evidence: []` cho cả 18/18 kết quả manual**; `actual = null` cho 17 TC `pass`; TC `skip` ghi `actual = "skip api"` | **`[BLOCKER]` RULE-02** — xem §4.1 |
| 8 | **Độ phủ spec do Studio tự chấm** | `coverage.summary` = **total 14 · covered 0 · partial 14 · none 0** — Studio tự khai **KHÔNG có spec ref nào đạt `covered`** | Xác nhận đánh giá `RISK` ở §3 |

---

## 1. Verdict

> ## ⛔ REJECTED

**3 `[BLOCKER]`** — trong đó **BLOCKER-1 có khả năng bug của khách hàng CHƯA được fix**, và **BLOCKER-3 làm toàn bộ 17 kết quả `Đạt` mất giá trị chứng minh**.

Không được đóng ticket #40399 với bộ TC hiện tại.

---

## 2. Tóm tắt cho member

**Điểm tốt** — bộ TC có chất lượng viết **cao hơn mặt bằng chung rõ rệt**: tiền điều kiện dựng lại được (số friend cụ thể, số snapshot cũ cụ thể, dặn "tuyệt đối không bấm nút tính lại khi chuẩn bị"), kết quả mong đợi **đo lường được** bằng con số thật (`12人（予定）` chứ không phải "hiển thị đúng"), và có **3 TC đối chứng âm** rất tốt (`#15510` `#15522` `#15523` — chốt phạm vi fix không tràn sang broadcast có filter / không ghi đè bản gốc). TC `#15509` còn **phản biện lại chính Dev**: Dev nói "khách không có cách nào làm mới con số", nhưng nút 「再計算」 trên **màn danh sách** không hề bị khoá.

**Phải fix** — (1) bộ TC bỏ sót **đúng trạng thái mà khách hàng nhiều khả năng đang gặp**: broadcast để 「すべての友だち」 nhưng **còn sót bản ghi điều kiện lọc cũ** — fix rẽ nhánh theo "có bản ghi filter hay không" nên trạng thái này **không được fix**, mà kho TCs (MT-05) đã ghi nhận trạng thái này có thật; (2) Dev khai "3 chỗ khác dùng chung giá trị ảnh chụp" nhưng **không nêu tên**, 0 TC cover; (3) **19/19 TC không có evidence**, nên 17 chữ "Đạt" hiện không chứng minh được điều gì.

---

## 3. Coverage Matrix

> Cột `Status (coverage)` = xét theo TC có/thiếu chiều.
> Cột `Status (thực chất)` = sau khi trừ đi **BLOCKER-3** (evidence rỗng 19/19 → không xác minh được đã chạy thật) theo BƯỚC 0.6. Đây mới là trạng thái Leader phải dùng để quyết định.

| Impact | Loại | TC cover (suy luận) | # TC | Exec | Status (coverage) | Status (thực chất) |
|---|---|---|---|---|---|---|
| `BUG` — tái hiện triệu chứng KH (list 2 chữ số / màn sửa 4 chữ số) | Root cause | `#15505` | 1 | 1/1 pass | `OK` | **`RISK`** — không evidence; và **không cover** trạng thái flag=0 + còn filters_v2 (xem GAP-01) |
| `F1` `ajaxGetListBroadcastVer2` | Direct | `#15505` `#15506` `#15507` `#15508` `#15510` `#15511` `#15512` `#15513` `#15529` | 9 | 8/9 | `OK` | **`RISK`** |
| `F2` `saveCopyBroadCastV2New` | Direct | `#15520` `#15521` `#15522` `#15523` `#15524` `#15525` `#15552` | 7 | 6/7 (`#15552` **skip**) | `RISK` | **`RISK`** — TC duy nhất verify contract server bị skip |
| `F3` `getFilterNumber` (perf — thêm 1 query đếm/lần load + 1/lần copy) | Indirect | `#15509` `#15529` | 2 | 1/2 (`#15529` **chưa chạy**) | `RISK` | **`RISK`** — TC đo query chưa chạy; không TC nào ở quy mô thật |
| `F4` `getBroadcastLimitAlert` (cảnh báo 50% hạn mức) | Indirect | — | 0 | — | **`GAP`** | **`GAP`** |
| **`BUG-GAP-01`** — 3 chỗ khác dùng chung `filter_number`/`filter_date` (Dev **không nêu tên**) | Chưa xác định | — | 0 | — | **`GAP`** | **`GAP`** → BLOCKER-2 |
| `D1` `broadcast.filter_number` CREATE (bản copy) | Data | `#15520` `#15521` `#15525` `#15552` | 4 | 3/4 | `OK` | **`RISK`** |
| `D2` `broadcast.filter_date` CREATE (bản copy) | Data | `#15520` `#15521` `#15525` | 3 | 3/3 | `OK` | **`RISK`** — không TC nào kiểm **múi giờ** của mốc thời gian hiển thị |
| `D3` bản ghi cũ KHÔNG bị ghi đè | Data | `#15508` `#15512` `#15513` `#15522` | 4 | 4/4 | `OK` | **`RISK`** |
| `T1` Danh sách tab 下書き / 配信予約 | Feature (High) | `#15505` `#15506` | 2 | 2/2 | `RISK` | **`RISK`** — thiếu chiều phân trang / tìm kiếm (GAP-07) |
| `T2` Luồng sao chép broadcast | Feature (High) | `#15520` → `#15525` | 6 | 6/6 | `OK` | **`RISK`** — thiếu chiều cross-bot (GAP-05) + double-click (kho `TC-BC-251`) |
| `T3` Friend Filter / Segment — broadcast CÓ lọc | Feature (Medium) | `#15510` `#15523` | 2 | 2/2 | `OK` | **`RISK`** — chỉ verify tới tầng data/UI, không tới người nhận thật (kho `TC-BC-257`) |
| `T4` Tab 配信履歴 (đã gửi / đang gửi / gửi lỗi) | Feature (Medium) | `#15511` | 1 | 1/1 | `RISK` | **`RISK`** — 1 TC, không cover tab 概要 của popup preview (kho MT-13) |
| `T5` Cảnh báo chạm hạn mức 50% | Feature (Low) | — | 0 | — | **`GAP`** | **`GAP`** |

**Tổng kết**: `OK` 0 · `RISK` 11 · `GAP` 3 (sau khi trừ evidence).

### ORPHAN TCs

**Không có TC lạc chủ đề.** Đã trace từng TC về code path Dev sửa:

- `#15528` (nút 「再計算」 vẫn bị vô hiệu) **không** phải orphan — đây là TC chốt **giới hạn phạm vi fix**: Dev cố ý KHÔNG mở khoá nút này. Nếu nút bỗng dùng được thì fix đã vượt mô tả. Giữ nguyên.
- `#15527` (lưu lại từ màn sửa) **không** phải orphan — đây chính là đường mà khách vô tình "chữa" được triệu chứng (lưu lại nháp thì số nhảy sang 4 chữ số), thuộc `T1` + regression đường lưu thường.
- **AP-5 (layer-downstream over-coverage): KHÔNG dính.** Bộ TC bám đúng 2 điểm Dev sửa, không đi lan sang tầng gửi tin / template / action vốn không bị chạm code.

---

## 3.5 Fix-shape analysis (adversarial)

Fix shape đọc từ `03-dev-impact.md` mục 2 → khớp **3 shape** cùng lúc:

| Fix shape | Câu hỏi adversarial | Trả lời từ bộ TC | Kết luận |
|---|---|---|---|
| **"số đếm / count / thống kê"** (`DATA-COUNT-001`) | Đối chiếu đủ **4 nguồn** (summary / detail / CSV / API) + **phép tính tay** trên bộ dữ liệu biết trước kết quả? Mẫu số xử lý friend **đã block** đúng spec? | **Phép tính tay ✓ xuất sắc** — 12 chưa chặn + 3 đã chặn, expect 12 (`#15509` `#15520`). **Block ✓**. **4 nguồn ✗** — chỉ đối chiếu list + màn sửa + DB. **Tab 概要 của popup preview** (nơi kho MT-13 ghi nhận từng dùng nguồn số KHÁC) **không có TC nào** | **`[MAJOR]`** → GAP-02 |
| **"sửa hàm dùng chung"** (`REG-SHARED-001`) | Có **danh sách nơi ảnh hưởng do DEV cung cấp**? TC test **từng nơi** trong danh sách? | Dev viết nguyên văn: *"Quét ngang thấy **3 chỗ khác** dùng chung giá trị ảnh chụp này nhưng thuộc màn/tính năng khác nên chỉ ghi nhận, không sửa"* — **KHÔNG nêu tên 3 chỗ đó**. 0 TC | **`[BLOCKER]`** → BLOCKER-2 |
| **"cache / performance"** (`PERF-LARGE-001`) | Test với **quy mô khách hàng lớn nhất THỰC TẾ**? | **✗** — toàn bộ 19 TC dùng **12 bạn bè**. Khách báo bug (アドライフ株式会社) có **~15.000 lượt gửi / hạn mức 30.000**. TC đo số query (`#15529`) khai `env_scope = local` và **chưa chạy** | **`[MAJOR]`** → GAP-04 |

### Symptom-only KH report check → **AP-2 DÍNH**

`01-bug-task.md` mục "Mô tả bug": khách chỉ mô tả **hiện tượng** — *"dù cài đặt gửi cho toàn bộ nhưng số hiển thị chỉ có 2 chữ số, còn khi tạo lại bản nháp thì số người toàn bộ lại hiển thị 4 chữ số"*. **Không có** error code / log / screenshot của màn danh sách kèm bản ghi cụ thể.

Nghiêm trọng hơn: **không ai kiểm chứng được trên tài khoản thật của khách** —
- Dev: *"DB dev `host.docker.internal:3306` Connection refused nên không kiểm chứng được bằng dữ liệu runtime; kết luận dựa trên đối chiếu code"*.
- Khách: *"Hôm nay số liệu đã được reset"* → hiện trường đã mất.

⇒ Dev tái hiện **1 root cause** (snapshot đóng băng). Bộ TC bám đúng 1 root cause đó. **Root cause thay thế cùng tạo ra triệu chứng này chưa được loại trừ**, đặc biệt là GAP-01 dưới đây. → **`[MAJOR]` AP-2**

### Anti-patterns

| AP | Dính? | Ghi chú |
|---|---|---|
| AP-1 Single-trigger generic-fix | ✗ | Fix không phải generic catch |
| **AP-2 Symptom-only KH report** | **✓** | Xem trên → `[MAJOR]` |
| **AP-3 Happy-path-only regression** | **✓ một phần** | `T4` chỉ 1 TC; `T3` 2 TC nhưng đều precondition "data sạch"; không TC nào chạy regression ở edge state (broadcast quá hạn, đang gửi dở, bản ghi legacy trước 15/01/2025 — kho MT-14) → `[MAJOR]` |
| **AP-4 Specific code-check disguised as generic catch** | **✓ một phần** | `03-dev-impact.md` mục "Commit / Pull Request" = **không có link PR**, chỉ có branch + commit hash `1348f867e2`. Không review được diff thật → `[MAJOR]` |
| AP-5 Layer-downstream over-coverage | ✗ | Bộ TC không over-test tầng không bị chạm ✓ |
| **AP-6 Mục 3 dev-impact trống** | **✓ một phần** | Mục 3 **có** list 13 function ✓, nhưng "3 chỗ dùng chung" ở mục 2 lại **không** được đưa vào mục 3 → cùng gốc với BLOCKER-2 |

---

## 3.6 Bảng quan điểm đối chiếu

> 7 TC mang mã Studio ngoài `checklist-lme.md` (BƯỚC 0.6 #6) **không được tính là cover** — cột "TC cover" chỉ ghi TC map được về mã tầng 1.

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover | Exec | Kết luận |
|---|---|---|---|---|---|
| `DATA-COUNT-001` | **Cao** | ◯ — "BẮT BUỘC khi màn hình có bất kỳ con số đếm/tỷ lệ/tổng hợp nào". Đây là **lõi** của task | `#15509` (N) `#15521` (N) `#15552` (Ab) | 2/3 (1 skip) | **`[MAJOR]` RULE-01** — thiếu **Boundary** cho chính mã này (biên 0 friend đang gắn `FUNC-004`, không gắn `DATA-COUNT-001`); và **thiếu chiều 4 nguồn** → GAP-02 |
| `DATA-DB-001` ★ | **Cao** | ◯ — "BẮT BUỘC với mọi chức năng có UPDATE/DELETE" (luồng copy ghi thật `filter_number`/`filter_date`) | `#15508` (N) `#15522` (Ab) `#15512` (Ab) | 3/3 | `OK` — có verify DB thật ✓ RULE-07 3 tầng ✓. Đã có TC kiểm `WHERE` scope trên **2 bot** (`#15512`) ✓ nhưng **chỉ ở màn danh sách**, không ở luồng ghi (copy) → xem `PERM-003` |
| `PERM-003` | **Cao** | ◯ — "BẮT BUỘC khi vận hành nhiều LINE OA hoặc có chức năng change bot" | `#15512` (Ab) | 1/1 | **`[MAJOR]`** — chỉ cover **màn danh sách**. Luồng **copy** không cover, trong khi **Studio tự khai `REQ-013`**: *"mã hiện tại không kiểm bot của broadcast gốc"* → GAP-05. Thiếu Normal + Boundary (RULE-01) |
| `REG-SHARED-001` | **Cao** | ◯ — "BẮT BUỘC với mọi release sửa code dùng chung". Dev nêu 3 chỗ dùng chung | `#15523` (Ab) | 1/1 | **`[BLOCKER]`** — `#15523` chỉ test copy broadcast có filter, **không** cover "3 chỗ dùng chung" → BLOCKER-2 |
| `DATA-001` | **Cao** | ◯ — "mọi chức năng cập nhật dữ liệu được tham chiếu ở nơi khác". `filter_number` được tham chiếu ở ≥3 nơi khác | — | — | **`[BLOCKER]`** — gộp vào BLOCKER-2 |
| `FUNC-001` | **Cao** | ◯ — luôn bắt buộc | `#15527` (N) | 1/1 | `OK` |
| `FUNC-004` | **Cao** | ◯ — "chức năng có giới hạn số lượng" (biên 0 bạn bè) | `#15513` (B) `#15525` (B) | 2/2 | `OK` — 2 Boundary ở 2 luồng khác nhau ✓. Thiếu Normal/Abnormal riêng nhưng đã cover ở mã khác → chấp nhận |
| `FUNC-003` | Trung bình | ◯ — validate ngày giờ gửi | `#15524` (Ab) | 1/1 | `OK` — có bắt điểm tinh: nhánh copy trả **HTTP 200 kèm thông báo lỗi** ✓ |
| `STATE-001` | **Cao** | ◯ — "BẮT BUỘC khi nghiệp vụ gồm ≥2 bước ghi dữ liệu tuần tự (… **copy**)". Copy ghi: broadcast cha + các mốc con + templates + actions + filters | `#15521` (N) `#15524` (Ab) | 2/2 | **`[MAJOR]`** — `#15524` chỉ cover nhánh **từ chối sớm**. Không TC nào cover **copy hỏng giữa chừng** (ghi xong bản ghi cha thì lỗi khi clone template → còn broadcast mồ côi mang `filter_number` mới?) |
| `MSG-001` | **Cao** | ◯ — "BẮT BUỘC với mọi chức năng gửi tin có điều kiện lọc" | `#15510` `#15523` (tầng data) | 2/2 | **`[MAJOR]` RULE-06** — dừng ở màn admin/DB, **không đi tới người nhận thật**. Kho có sẵn `TC-BC-257` đúng vùng này (bug #32229 cũ: *copy từ broadcast có filter lại bị gửi cho ALL friend*) → GAP-03 |
| `MSG-005` | **Cao** | ◯ — "BẮT BUỘC khi chức năng tiêu thụ quota tin nhắn". Đây là **câu hỏi thứ 2 của khách** (cảnh báo 15.000/30.000) | — | — | **`[MINOR]`** — Dev **không sửa** `getBroadcastLimitAlert` nên không phải rủi ro regression code. Kho đã có sẵn 39 TC nhóm 「配信数上限アラート」 → **dùng lại kho**, không viết mới. Nhưng ticket vẫn **chưa có bằng chứng** trả lời khách → §6 |
| `JOB-001` ★ | **Cao** | ◯ — broadcast gửi bằng **Spring Boot job poll bảng `broadcast`** (spec FA-008). Fix đổi số hiển thị của broadcast `wait_to_send` — chính là loại job sẽ gửi | — | — | **`[MAJOR]`** — 0 TC để job chạy thật rồi đối chiếu → GAP-06 |
| `ENV-003` ★ | **Cao** | ◯ — "BẮT BUỘC khi tính năng chạm … **job nền**, thanh toán". **Không được đánh × với lý do 'staging đã pass'** (RULE-08) | — | 0 TC production | **`[MAJOR]`** — 100% chạy `staging` |
| `PERF-LARGE-001` | Trung bình **→ Cao** (gửi tin) | ◯ — fix thêm 1 query đếm mỗi lần load list + mỗi lần copy | `#15529` (B) | **0/1 chưa chạy** | **`[MAJOR]`** — TC có nhưng chưa chạy, và quy mô test (12 friend) cách xa quy mô khách (~15.000) → GAP-04 |
| `LIST-001` | Trung bình | ◯ — màn danh sách có search/filter/pagination; fix chèn logic vào đúng vòng lặp dựng danh sách | — | — | **`[MAJOR]`** — không TC nào kiểm số hiển thị ở **trang 2** hoặc **sau khi tìm kiếm/lọc thời gian** → GAP-07 |
| `UI-FIELD-001` | Trung bình | ◯ — nút 「再計算」 phụ thuộc lựa chọn cha | `#15528` (Ab) | 1/1 | `OK` — tái dùng nguyên case kho `BR-017` (gốc #39667) ✓ |
| `DATA-CACHE-001` | Trung bình | ◯ — `filter_number` **chính là** cache; fix đổi ngữ nghĩa cache | `#15508` (N) | 1/1 | `RISK` — cover việc "không ghi đè" nhưng **không** cover: cache 1 lần/request có bị dùng lại sai khi đổi bot trong cùng request không (`#15512` test qua nhiều request) |
| `CONC-001` / `CONC-002` | **Cao** / TB | ◯ một phần — nút 「コピー」 nay chạy thêm 1 query đếm trước khi ghi | — | — | **`[MINOR]`** — hành vi đồng thời **không bị fix chạm**, nhưng kho đã có `TC-BC-251` (double-click copy → chỉ 1 bản) và `TC-BC-263` (2 tab cùng copy) → đưa vào **vùng regression**, dùng lại kho, không viết mới |
| `FUNC-DATE-001` | **Cao** | ◯ một phần — fix ghi `filter_date = thời điểm hiện tại` và hiển thị 「… 時点の配信予定数」 | `#15521` (so trùng khít cha/con) | 1/1 | **`[MINOR]`** — không TC nào verify **múi giờ** của mốc thời gian hiển thị (JST) |
| `COMPAT-LEGACY-001` ★ | **Cao** | ◯ — tồn tại **2 đường copy**: `copyBroadcastV2` (Dev khẳng định là code chết) và `saveCopyBroadCastV2New` (đường đang chạy) | `#15528` gián tiếp | 1/1 | **`[MAJOR]`** — Dev kết luận `copyBroadcastV2` là code chết chỉ bằng cách đọc **3 file blade**. Không TC nào chứng minh endpoint cũ thật sự không gọi tới được. Nếu còn đường vào → nhánh cũ **không có fix** |
| `REG-RUN-001` | **Cao** | ◯ — deploy khi có broadcast đang `delivering` / đã đặt lịch | `#15511` (Ab) | 1/1 | `RISK` — cover hiển thị, không cover deploy giữa lúc job đang chạy |
| `OUT-TRUTH-001` | **Cao** | ◯ — thao tác lưu có thông báo kết quả | `#15524` (Ab) | 1/1 | `OK` ✓ |
| `DATA-BACKUP-001` ★ | Cao | ✗ | — | — | Không thêm/đổi bảng, không chạm backup/copy bot — **lý do hợp lệ** (RULE-03) |
| `DEPLOY-ASSET-001` ★ | Cao | ✗ | — | — | Diff = **2 file PHP**, không sửa JS/CSS/asset — **lý do hợp lệ** |
| `MEDIA-*` · `PAY-*` · `LIFF-*` · `INTG-*` · `SEC-*` · `NOTI-MAIL-*` | — | ✗ | — | — | Task không chạm media/thanh toán/LIFF/webhook/PII/mail — **lý do hợp lệ** |

**Quan điểm ◯ nhưng KHÔNG có TC nào cover**: `DATA-001` · `MSG-005` · `JOB-001` · `ENV-003` · `LIST-001` — trong đó `DATA-001` là **BLOCKER**, còn lại `[MAJOR]` / `[MINOR]`.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

**`[BLOCKER] GAP-01` — Bộ TC bỏ sót đúng trạng thái mà khách hàng nhiều khả năng đang gặp; bug có thể CHƯA được fix**

Fix rẽ nhánh theo **"broadcast có bản ghi điều kiện lọc hay không"** — Studio ghi rõ trong note của `#15510` (*"chỉ broadcast KHÔNG có **bản ghi điều kiện lọc** mới được hiển thị đè"*) và `#15523` (*"chỉ tính lại khi bản gốc KHÔNG có **bản ghi điều kiện lọc**"*, `BroadcastV2Controller.php:838-845`).

Nhưng theo `feature-spec.md` §4 hàng 6, "gửi toàn bộ" là **`broadcast.flag_setting_filter = 0`**, còn điều kiện lọc nằm ở bảng **`filters_v2`** — **hai thứ khác nhau**. Và kho TCs đã ghi nhận trạng thái lệch giữa hai thứ này là **có thật**:

> **kho MT-05** (⏳ CHỜ QUYẾT ĐỊNH): *"filte xong tick sang all friend → sau đấy lại tick lại thu hẹp → hiển thị sl đã filte, **vẫn giu đk lọc trước đó**"* — áp dụng khi broadcast **ĐÃ được tạo**.

⇒ Tồn tại trạng thái: **`flag_setting_filter = 0` (màn hình hiển thị 「未設定（全員）」 = gửi toàn bộ) NHƯNG vẫn còn bản ghi `filters_v2` sót lại**. Ở trạng thái này fix **không kích hoạt**, số cũ vẫn đóng băng — **đúng y hệt triệu chứng khách báo**: *"全員配信の設定でも表示が2桁で少なく"* (đặt gửi toàn bộ mà số vẫn 2 chữ số).

**0/19 TC** cover trạng thái này. Cả `#15505` (all friends, không filter) lẫn `#15510` (có filter, `flag = 1`) đều là **trạng thái sạch**.

→ **Fix**: bổ sung `TC-DATACOUNT001-04` + `TC-DATACOUNT001-05` (§5). **Đồng thời hỏi Dev ngay**: điều kiện rẽ nhánh trong code đọc `flag_setting_filter` hay đọc sự tồn tại của bản ghi `filters_v2`? Nếu là vế sau → **fix chưa giải quyết được ca của khách**, phải sửa lại code chứ không chỉ bổ sung TC.

---

**`[BLOCKER] BUG-GAP-01` — "3 chỗ khác dùng chung giá trị ảnh chụp" không được nêu tên, 0 TC** *(FIX-SHAPE: sửa hàm dùng chung → `REG-SHARED-001`, `DATA-001`)*

`03-dev-impact.md` mục 2, nguyên văn: *"Quét ngang thấy **3 chỗ khác dùng chung giá trị ảnh chụp này** nhưng thuộc màn/tính năng khác nên chỉ ghi nhận, không sửa."* — Dev **không liệt kê** 3 chỗ đó, và mục 3 / 4.1 cũng không có.

Đây là fix-shape "sửa hàm dùng chung": **không có danh sách nơi ảnh hưởng ⇒ không chốt được phạm vi regression ⇒ BLOCKER** theo BƯỚC 3c.

Rủi ro cụ thể, không phải giả định suông — kho TCs đã ghi nhận `filter_number` bị dùng ở nơi khác và **từng gây bug thật**:
> **kho MT-13** (CAO, ⏳ CHỜ QUYẾT ĐỊNH): `db-mapping.md:184` ghi 配信数 lấy từ **`send_count / filter_number`** — *"ghi CẢ HAI, không nói khi nào dùng cái nào"*. Bug gốc **#31527**: *"Số user đã send hiển thị là **8.871** trên màn hình danh sách, nhưng trong màn hình chi tiết là **6.864** friend"*. Và **tab 概要 của popup preview** được ghi là *"vẫn như cũ (k count theo send_count)"* — tức vẫn đọc `filter_number`.

⇒ Nếu tab 概要 của popup preview là 1 trong "3 chỗ" đó, fix vừa **tái tạo lại đúng bug #31527** ở dạng mới (list hiện số live, popup hiện số cache).

→ **Fix**: yêu cầu Dev **liệt kê đích danh 3 chỗ** trước khi test tiếp. Bổ sung `TC-REGSHARED001-02` (§5) đối chiếu 配信数 ở **mọi nơi hiển thị**.

---

**`[BLOCKER] RULE-02` — 19/19 TC không có evidence; 17 chữ "Đạt" không chứng minh được điều gì**

`task_get_report` xác nhận: **`evidence: []` cho cả 18/18 kết quả**, `actual = null` cho toàn bộ 17 TC `pass`.

Nghiêm trọng hơn — **dấu thời gian nộp kết quả dồn cụm** so với khối lượng chuẩn bị mà chính TC yêu cầu:

| Cặp liên tiếp | Cách nhau | TC sau đó đòi hỏi gì |
|---|---|---|
| `#15521` → `#15522` | **4 giây** | Ghi lại giá trị DB của **4 broadcast**, thực hiện 1 lần copy đầy đủ (nhập tiêu đề + ngày giờ + lưu), rồi đối chiếu lại **4 bản ghi** + mở màn sửa |
| `#15522` → `#15523` | **6 giây** | Copy 1 broadcast có filter, đối chiếu DB bản cha + bản con, **mở hộp thoại filter đối chiếu từng điều kiện**, rồi quay lại danh sách |
| `#15511` → `#15512` | **6 giây** | Chuyển qua lại giữa **2 bot** 3 lượt + đối chiếu DB của 2 broadcast |
| `#15505` → `#15506` | **9 giây** | Mở tab 配信予約, đọc số, hover đọc chú thích, chuyển tab qua lại rồi đọc lại |

**13/18 kết quả** được nộp cách nhau ≤ 20 giây. Toàn bộ 19 TC đều đòi **dựng data nặng** (bot riêng, đúng 12 bạn bè chưa chặn, 3 bạn đã chặn, snapshot cũ = 3 với mốc thời gian quá khứ, 2 mốc lịch con…).

> Cách hiểu vô hại: QA chạy hết rồi **nộp kết quả theo lô** ở cuối. Điều đó hoàn toàn có thể. **Nhưng vì `evidence` rỗng 100% và `actual` = null 100%, không có cách nào phân biệt** "đã chạy thật rồi nộp lô" với "tick pass hàng loạt".

⇒ Theo RULE-02, **không TC nào trong 19 TC đủ điều kiện tick Đạt**. Toàn bộ `Status = OK` ở §3 phải hạ xuống `RISK`.

→ **Fix**: `#15505` (tái hiện bug) · `#15508` (không ghi đè DB) · `#15520` `#15521` `#15552` (nhánh ghi thật khi copy) **bắt buộc** đính kèm evidence trước khi được tính là Đạt — ảnh màn danh sách có con số + ảnh/kết xuất giá trị DB trước-sau. Các TC còn lại tối thiểu ảnh màn hình.

### 4.2 Major (nên fix)

**`[MAJOR] FIX-SHAPE: PERF` GAP-04 — quy mô test cách quy mô khách 1.000 lần**
Toàn bộ 19 TC dùng **12 bạn bè**. Khách báo bug có **~15.000 lượt gửi / hạn mức 30.000**. Bản chất bug là "2 chữ số vs 4 chữ số" — với 12 friend thì **chưa bao giờ tái hiện được vế 4 chữ số**. Fix lại thêm 1 query đếm mỗi lần load danh sách; TC đo số query (`#15529`) khai `env_scope = local` và **chưa chạy lần nào**. → `TC-PERFLARGE001-01` (§5).

**`[MAJOR] AP-2 SYMPTOM-ONLY` — chưa loại trừ root cause thay thế**
Khách chỉ mô tả hiện tượng, không có log/error code. Dev **không kiểm chứng được bằng runtime** (DB dev `Connection refused`), khách thì *"hôm nay số liệu đã được reset"* → hiện trường đã mất. Root cause thay thế khả dĩ nhất chính là **GAP-01**. → Hỏi Dev: có xác nhận được trên chính tài khoản `adlife1001@gmail.com` rằng broadcast đó **không** có bản ghi `filters_v2` sót lại không?

**`[MAJOR] AP-4` — không có link PR**
`03-dev-impact.md` mục "Commit / Pull Request" chỉ có branch `ai_fixbug_40399` + commit `1348f867e2`, **không có link PR**. Không review được diff thật → không tự xác minh được điều kiện rẽ nhánh ở BLOCKER-1. → Yêu cầu Dev cung cấp PR/diff.

**`[MAJOR] RULE-08 / ENV-003` — 0 TC chạy production**
100% chạy `staging`. Task chạm **job nền** (Spring Boot poll bảng `broadcast`) và **quota tin nhắn**. Thêm nữa, cả 19 TC khai `env_tag = local-only` nhưng lại chạy ở `staging` → **khai báo mâu thuẫn thực tế**, cần chỉnh trên Studio.

**`[MAJOR] GAP-05 / PERM-003` — `REQ-013` do chính Studio khai nhưng 0 TC**
Studio khai `REQ-013`: *"Sao chép một broadcast không thuộc bot đang chọn không được tạo ra bản ghi mang số bạn bè của bot khác. Kỳ vọng chính xác cần Dev/PM xác nhận vì **mã hiện tại không kiểm bot của broadcast gốc**"* (`category = permission`, `BroadcastV2Controller.php:803-806`). Fix vừa thêm phép đếm bạn bè **theo bot đang chọn** vào chính luồng này → nếu copy được broadcast của bot khác thì bản sao sẽ mang số bạn bè **sai bot**. `#15512` chỉ cover màn danh sách. → `TC-PERM003-02` (§5). Lưu ý spec **BR-08 Bot Switch Guard** chỉ áp cho form legacy.

**`[MAJOR] GAP-03 / MSG-001 / RULE-06` — chưa đi tới người nhận thật**
`#15510` `#15523` dừng ở màn admin + DB. Kho đã ghi nhận bug quá khứ **#32229**: *"Copy từ broadcast có filter sau đó đặt lịch gửi, nhưng broadcast copy lại bị gửi cho all friend"* — đúng luồng mà fix đang sửa. → **Dùng lại kho `TC-BC-257`**, bổ sung bước để job gửi thật + đối chiếu người nhận trên LINE app.

**`[MAJOR] GAP-06 / JOB-001` — broadcast đã đặt lịch: số hiển thị đổi nhưng chưa ai để job gửi thật**
`#15506` xác nhận tab 配信予約 hiển thị số live. Đây đều là broadcast `wait_to_send` mà **job sẽ gửi thật**. Không TC nào chạy tới lúc job fire. → `TC-JOB001-01` (§5).

**`[MAJOR] GAP-07 / LIST-001` — không kiểm phân trang / tìm kiếm**
Fix chèn logic vào vòng lặp dựng danh sách + dùng 1 biến cache đếm 1 lần/request. Không TC nào kiểm số hiển thị ở **trang 2** hay **sau khi tìm kiếm / lọc theo thời gian**. → `TC-LIST001-01` (§5).

**`[MAJOR] GAP-02 / DATA-COUNT-001` — chưa đối chiếu đủ các nơi hiển thị 配信数**
Chỉ đối chiếu list + màn sửa + DB. **Tab 概要 của popup preview** (kho MT-13 ghi nhận dùng nguồn số khác) không có TC. → `TC-REGSHARED001-02` (§5).

**`[MAJOR] COMPAT-LEGACY-001` — "code chết" chưa được chứng minh bằng test**
Dev kết luận `copyBroadcastV2` là code chết bằng cách đọc **3 file blade**. Không TC nào chứng minh endpoint `/ajax/copy-broadcast-v2` (spec liệt kê là **EP-16**, vẫn tồn tại trong api-spec) không còn đường vào. Nếu còn → nhánh đó **không có fix**. → Yêu cầu Dev xác nhận đã gỡ route, hoặc bổ sung TC gọi thẳng EP-16.

**`[MAJOR] STATE-001` — copy hỏng giữa chừng**
Copy ghi tuần tự: broadcast cha → các mốc con → templates → actions → filters. `#15524` chỉ cover nhánh **từ chối sớm** (thiếu ngày giờ). Không TC nào cover lỗi **giữa chừng** → có sinh bản ghi mồ côi mang `filter_number` mới không?

**`[MAJOR] AP-3` — regression chỉ chạy happy path**
`T4` chỉ 1 TC; `T3` 2 TC, tất cả precondition đều "data sạch". Không TC nào chạy regression ở edge state: broadcast quá hạn gửi, đang gửi dở, hoặc **bản ghi legacy trước 08:00 15/01/2025** (kho MT-14 — nhóm dữ liệu này lưu ở bảng `message` cũ, không phải `messages_v2s`).

**`[MAJOR]` — `Trạng thái đánh giá spec` rỗng 19/19**
`spec_status = null` toàn bộ. Trong khi task có **ít nhất 4 điểm spec chưa chốt** (§6). Nguy cơ tự suy diễn rồi cho Đạt — đặc biệt `#15507`, mà chính Studio ghi trong note: *"cần PM/BA xác nhận … Không dùng TC này làm release blocker cho tới khi REQ-003 được xác nhận"* — **nhưng TC vẫn được tick `pass`**.

**`[MAJOR]` — TC ưu tiên `High` bị skip không rõ lý do**
`#15552` (`priority = High`, do **người** viết) là TC **duy nhất** verify contract server: *server phải bỏ qua `count_filter` client gửi và tự đếm*. Kết quả `skip`, `actual = "skip api"`. Đây đúng là điểm mà Dev nhấn mạnh trong mục 2 (*"đếm ở server, không tin số client gửi"*) → **không được bỏ**.

**`[MAJOR]` — 19/19 TC khai `exec_mode = auto` nhưng runner chưa chạy**
Auto run `#816` (env `staging`) vẫn `queued`; `auto.totals` toàn 0. Hoặc chạy runner, hoặc sửa `exec_mode` về `manual` cho khớp thực tế.

**`[MAJOR]` — 18/19 TC do AI sinh, review chưa `done`**
`reviewState = leader`, `reviewed = false`, `status` của cả 19 TC vẫn là `draft`.

### 4.3 Minor (có thể fix sau)

- **`[MINOR]` `MSG-005`** — câu hỏi **thứ 2** của khách (cảnh báo 「配信数上限が近づいています」 khi 15.000/30.000) không có TC. Dev **không sửa** code này nên không phải rủi ro regression, nhưng ticket chưa có bằng chứng để trả lời khách. Kho đã có **39 TC** nhóm 「配信数上限アラート」 → dùng lại kho (lưu ý kho MT-20 đang ⏳ chờ quyết định vì tính năng #36436 không có trong spec).
- **`[MINOR]` `FUNC-DATE-001`** — không TC nào verify **múi giờ** của mốc 「… 時点の配信予定数」 nay được set bằng thời điểm hiện tại (JST vs UTC).
- **`[MINOR]` `CONC-002`** — nút 「コピー」 nay chạy thêm 1 query đếm trước khi ghi. Hành vi đồng thời không bị fix chạm, nhưng nên đưa kho `TC-BC-251` (double-click → chỉ 1 bản copy) và `TC-BC-263` (2 tab cùng copy) vào **vùng regression** (RULE-12 mục 2).
- **`[MINOR]` BƯỚC 0.6 #6** — 5 mã quan điểm Studio không có trong `checklist-lme.md` (`TOOL-KNOW-002`, `TOOL-SCOPE-001`, `TOOL-NEGCTRL-001`, `DATA-HIST-001`, `PERF-LATENCY-001`) → 7 TC không map được coverage. Hoặc bổ sung mã vào checklist, hoặc gán lại mã tầng 1.
- **`[MINOR]` `DATA-CACHE-001`** — biến cache đếm 1 lần/request: chưa có TC đổi bot **trong cùng một phiên tải danh sách**.

### 4.4 Nit (gợi ý)

- **`[NIT]`** — Studio còn **task #273 rỗng** (0 TC, `feature = null`, `status = new`, cùng ticket 40399, chưa archive) → nên archive để lần review sau không chọn nhầm.
- **`[NIT]`** — `TC No.` trên Studio dùng `temp_id` dạng `NEW-3`…`NEW-24`, không theo format repo `TC-<mã quan điểm bỏ gạch>-<nn>`. Đã quy đổi khi ghi `04-tc-list.md`.
- **`[NIT]`** — `#15505` gán `spec_ids` có cả `SCR-BC-02` dù TC chủ yếu ở `SCR-BC-01`; nhãn hơi rộng, không ảnh hưởng coverage.

---

## 4.5 TC trùng lặp nội dung

**Đã rà toàn bộ 19 TC theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`) — KHÔNG phát hiện trùng lặp.**

Các cặp **trông giống nhưng KHÔNG trùng** (ghi lại để Leader khỏi rà lại):

| Cặp | Vì sao KHÔNG trùng |
|---|---|
| `#15505` vs `#15506` | Khác **tab**: 下書き vs 配信予約. Fix lọc theo **trạng thái** chứ không theo tab → bắt buộc kiểm riêng từng tab (đúng như note của Studio) |
| `#15510` vs `#15523` | Khác **màn**: broadcast có filter ở **danh sách** vs ở **luồng copy**. Hai nhánh code khác nhau |
| `#15513` vs `#15525` | Cùng biên 0 bạn bè nhưng khác **nửa của fix**: nửa **hiển thị** (không ghi DB) vs nửa **ghi thật** (ghi DB). `#15525` còn phân biệt được "đã tính ra 0" vs "còn giá trị mặc định" qua mốc thời gian |
| `#15520` vs `#15552` | Khác **tầng**: UI copy vs API copy; và `#15552` thêm yếu tố đối kháng **client cố ý gửi `count_filter = 999`** mà `#15520` không có |
| `#15522` vs `#15524` | Cùng verify "bản gốc không bị đụng" nhưng khác **đường**: copy **thành công** vs copy **bị từ chối** |
| `#15508` vs `#15522` | Cùng verify "không ghi đè DB" nhưng khác **thao tác kích hoạt**: mở danh sách vs bấm copy |

⚠️ Không TC nào bị đề nghị xóa → **không có `DUP-INFLATE` che GAP**. Các GAP ở §3 là GAP thật, không phải do trùng lặp tạo ảo giác đủ.

---

## 5. TCs đề xuất bổ sung

> **Đã đối chiếu 19 TC ở BƯỚC 0 + [kho-tcs/fa008-broadcast-メッセージ配信.md](../../kho-tcs/fa008-broadcast-メッセージ配信.md) — không TC đề xuất nào trùng.**
>
> **3 GAP dùng lại TC kho, KHÔNG viết mới** (theo BƯỚC 5a):
> - **GAP-03** → dùng lại **`TC-BC-257`** *"Copy broadcast CÓ filter — bản copy giữ nguyên filter, KHÔNG gửi cho all friend"* (gốc bug #32229). **Cần chỉnh**: thêm bước để job gửi thật rồi đối chiếu **người nhận trên LINE app** (RULE-06), vì bản kho dừng ở tầng cấu hình.
> - **GAP-09 (regression đồng thời)** → dùng lại **`TC-BC-251`** (double-click コピー → chỉ 1 bản) + **`TC-BC-263`** (2 tab cùng copy). Không chỉnh gì, chỉ đưa vào vùng regression vì luồng copy vừa bị sửa.
> - **`MSG-005`** (cảnh báo 50% hạn mức) → dùng lại nhóm kho 「配信数上限アラート」 (39 TC). ⚠️ Kho **MT-20** đang ⏳ chờ quyết định (tính năng #36436 không có trong spec) → xem §6.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATACOUNT001-04 | Data | DATA-COUNT-001 | 配信先絞込み & 再計算 | Abnormal | manual | staging | Broadcast để 「すべての友だち」 nhưng còn sót điều kiện lọc cũ — danh sách phải hiện số bạn bè hiện tại | - Bot riêng của testcase, có **12 bạn bè chưa chặn**, trong đó **5 bạn** gắn thẻ 「TC40399_A」<br>- Chưa có broadcast nào tên 「TC40399_LEFTOVER」 | 1. Tạo broadcast bản nháp 「TC40399_LEFTOVER」, ở khối 配信先絞込み chọn 「絞り込み」 với điều kiện 「タグ」=「TC40399_A」, bấm 設定 rồi **lưu nháp**<br>2. Về danh sách, xác nhận dòng đó hiển thị 「5人（予定）」 và cột đối tượng gửi là 「設定済み」<br>3. Mở lại màn sửa của chính broadcast đó, **chuyển khối 配信先絞込み sang 「すべての友だち」**, rồi **lưu nháp** lần nữa<br>4. Về danh sách, đọc cột đối tượng gửi và cột 配信数 của dòng đó<br>5. Kết bạn thêm **2 bạn mới** cho bot (thành 14 chưa chặn)<br>6. Tải lại màn danh sách và đọc lại con số của dòng đó<br>7. Mở màn sửa của broadcast đó và đọc con số ở khối 配信先絞込み | Bot 12 bạn chưa chặn → 14 sau bước 5; thẻ 「TC40399_A」 gắn 5 bạn<br>Phép tính tay: sau bước 5, số đúng phải là **14**, KHÔNG phải 5 | - Bước 4: cột đối tượng gửi hiển thị 「未設定（全員）」 và cột 配信数 hiển thị 「12人（予定）」 — **KHÔNG còn 5**<br>- Bước 6: danh sách hiển thị 「14人（予定）」, đổi theo số bạn bè hiện tại<br>- Bước 7: màn sửa cũng hiển thị 「14人(予定)」 — **danh sách và màn sửa khớp nhau**<br>- Chú thích 「… 時点の配信予定数」 hiển thị mốc thời gian của lần mở màn, không phải mốc cũ | | **Lấp GAP-01 · cover impact F1 + BUG** · Đánh giá spec: **Spec không ghi** (đã hỏi Dev — chờ trả lời điều kiện rẽ nhánh đọc `flag_setting_filter` hay sự tồn tại bản ghi `filters_v2`) · Evidence: ảnh màn danh sách ở bước 4 + bước 6 (thấy rõ con số và cột đối tượng gửi) + ảnh màn sửa bước 7 · **dẫn từ kho MT-05** (chuyển 絞り込み → すべての友だち trên broadcast ĐÃ LƯU thì đk lọc cũ vẫn được giữ) · ⚠️ **Nếu TC này KHÔNG đạt thì bug của khách chưa được fix** |
| TC-DATACOUNT001-05 | Data | DATA-COUNT-001 | Copy broadcast | Abnormal | manual | staging | Sao chép broadcast 「すべての友だち」 còn sót điều kiện lọc cũ — bản sao phải mang số bạn bè hiện tại | - Bot riêng của testcase, có **12 bạn bè chưa chặn**, 5 bạn gắn thẻ 「TC40399_A」<br>- Có broadcast 「TC40399_LEFTOVER_SRC」 đã được đưa về trạng thái: đối tượng gửi 「すべての友だち」 **nhưng từng đặt filter thẻ trước đó** (dựng theo bước 1–3 của `TC-DATACOUNT001-04`)<br>- Số gửi dự kiến đang lưu của nó = **5**, mốc thời gian là ngày trong quá khứ | 1. Ở màn 一斉配信 chọn 「コピー」 trên dòng 「TC40399_LEFTOVER_SRC」<br>2. Trên màn sao chép, đọc con số ở khối 配信先絞込み và đọc khối đó đang chọn 「すべての友だち」 hay 「絞り込み」<br>3. Nhập tiêu đề 「TC40399_LEFTOVER_COPY」, chọn ngày giờ gửi trong tương lai, bấm lưu<br>4. Mở lại màn sửa của bản sao, đọc con số ở khối 配信先絞込み<br>5. Về danh sách, đọc cột 配信数 và cột đối tượng gửi của dòng bản sao<br>6. Đối chiếu ở tầng dữ liệu số gửi dự kiến + mốc thời gian đã lưu của bản sao<br>7. Đối chiếu ở tầng dữ liệu số gửi dự kiến của **bản gốc** | Bot 12 bạn chưa chặn; bản gốc đang lưu số 5 với mốc thời gian cũ<br>Phép tính tay: bản sao phải lưu **12** | - Bản sao lưu số gửi dự kiến = **12** và mốc thời gian là thời điểm sao chép — **KHÔNG bê nguyên số 5** và không lấy mốc cũ<br>- Màn sửa bản sao và màn danh sách đều hiển thị 「12人（予定）」<br>- Cột đối tượng gửi của bản sao hiển thị 「未設定（全員）」, đúng như bản gốc<br>- Bản gốc vẫn giữ nguyên số 5 và mốc thời gian cũ | | **Lấp GAP-01 · cover impact F2 + D1 + D2** · Đánh giá spec: **Spec không ghi** (đã hỏi Dev, cùng câu hỏi với `TC-DATACOUNT001-04`) · Evidence: kết xuất giá trị đã lưu của bản sao + bản gốc (trước và sau) + ảnh màn sửa bản sao · **dẫn từ kho MT-05** · Bổ sung chiều **ghi thật** cho GAP-01 mà `TC-DATACOUNT001-04` (chỉ hiển thị) không cover |
| TC-REGSHARED001-02 | UI | REG-SHARED-001 | 配信数 & danh sách friend đã gửi | Abnormal | manual | staging | Cùng một broadcast — số 配信数 phải khớp ở MỌI nơi hiển thị, không chỉ danh sách và màn sửa | - Bot riêng của testcase có **12 bạn bè chưa chặn**<br>- Có broadcast bản nháp gửi toàn bộ 「TC40399_ALLPLACES」, số gửi dự kiến đang lưu = **3** với mốc thời gian cũ<br>- **Trước khi chạy: xin Dev danh sách đích danh "3 chỗ khác dùng chung giá trị ảnh chụp"** và bổ sung các nơi đó vào bước kiểm | 1. Mở màn 一斉配信 tab 下書き, đọc số ở cột 配信数 của dòng đó<br>2. Mở màn sửa của broadcast đó, đọc số ở khối 配信先絞込み<br>3. Quay lại danh sách, mở **popup xem trước (preview)** của chính broadcast đó và đọc số 配信数 ở **tab 概要**<br>4. Bấm vào chính con số 配信数 ở danh sách để mở danh sách bạn bè dự kiến nhận, đếm số dòng<br>5. Kiểm tra thêm **từng nơi trong danh sách Dev cung cấp** ở tiền điều kiện<br>6. Đối chiếu ở tầng dữ liệu số gửi dự kiến đang lưu của broadcast | Bot 12 bạn chưa chặn; số đang lưu = 3<br>Phép tính tay: mọi nơi hiển thị phải ra **12** | - Bước 1, 2, 3, 4 đều ra **12** — **bốn nơi khớp nhau tuyệt đối**<br>- Đặc biệt **tab 概要 của popup xem trước KHÔNG được hiển thị 3** (giá trị cache cũ)<br>- Mọi nơi trong danh sách Dev cung cấp cũng hiển thị 12<br>- Ở tầng dữ liệu giá trị 3 vẫn nguyên (danh sách chỉ hiển thị đè) | | **Lấp GAP-02 + BUG-GAP-01 · cover impact BUG-GAP-01 + F1** · Đánh giá spec: **Spec không ghi** (đã hỏi Dev — chờ danh sách 3 chỗ dùng chung) · Evidence: ảnh **cả 4 nơi** trong cùng một phiên, thấy rõ cùng một con số · **dẫn từ kho MT-13** (`db-mapping.md:184` ghi 配信数 lấy từ `send_count / filter_number`, không nói khi nào dùng cái nào; bug gốc **#31527**: list 8.871 vs chi tiết 6.864) · ⚠️ TC này **chỉ chạy được đầy đủ sau khi Dev nêu tên 3 chỗ** — trước đó chạy phần bước 1–4 |
| TC-PERM003-02 | API | PERM-003 | Phân quyền & môi trường | Abnormal | manual | staging | Sao chép broadcast KHÔNG thuộc bot đang chọn — bản sao không được mang số bạn bè của bot khác | - Tài khoản quản trị có quyền trên **2 bot**: bot A có **12 bạn bè chưa chặn**, bot B có **3 bạn bè chưa chặn**<br>- Bot A có broadcast gửi toàn bộ 「TC40399_CROSSBOT」, số gửi dự kiến đang lưu = 3<br>- Ghi lại mã của broadcast đó | 1. Đang chọn **bot A**, mở màn 一斉配信 và bấm 「コピー」 trên 「TC40399_CROSSBOT」, ghi lại đường dẫn màn sao chép (có chứa mã broadcast gốc)<br>2. Thoát ra, **chuyển sang bot B**<br>3. Trong lúc đang ở bot B, mở lại **đúng đường dẫn màn sao chép** đã ghi ở bước 1<br>4. Quan sát màn hình: có mở được không, hay hiện thông báo chặn<br>5. Nếu mở được: nhập tiêu đề 「TC40399_CROSSBOT_COPY」 + ngày giờ gửi rồi bấm lưu, quan sát kết quả<br>6. Đối chiếu ở tầng dữ liệu: bản sao (nếu có) thuộc bot nào, số gửi dự kiến bằng bao nhiêu<br>7. Về màn 一斉配信 của **cả 2 bot**, kiểm bản sao xuất hiện ở đâu | Bot A: 12 bạn chưa chặn · Bot B: 3 bạn chưa chặn · broadcast gốc thuộc bot A, đang lưu số 3<br>Số sai cần bắt: bản sao thuộc bot B nhưng mang số **12** của bot A | - Hệ thống **chặn** thao tác: không tạo bản sao nào, hiển thị thông báo từ chối rõ ràng<br>- **Nếu hệ thống cho phép tạo** thì đây là lỗi cần raise ticket: bản sao **không được** mang số 12 của bot A trong khi nằm ở bot B<br>- Không bot nào xuất hiện bản sao lạ ở màn 一斉配信<br>- Broadcast gốc của bot A giữ nguyên số 3 | | **Lấp GAP-05 · cover impact F2 + D1** · Đánh giá spec: **Spec không ghi** — Studio tự khai `REQ-013` *"mã hiện tại không kiểm bot của broadcast gốc"*, **đã hỏi Dev/PM, CHỜ chốt kỳ vọng**; spec **BR-08 Bot Switch Guard** chỉ áp cho form legacy · Evidence: kết xuất bản ghi bản sao (bot nào + số gửi dự kiến) hoặc ảnh thông báo chặn · ⚠️ **Không tự chấm Không đạt khi hệ thống chặn** — chặn là kỳ vọng mong muốn |
| TC-PERFLARGE001-01 | API | PERF-LARGE-001 | Phân trang & số dòng hiển thị | Boundary | manual | product | Danh sách broadcast ở tài khoản quy mô thật (≥10.000 bạn bè) — số hiện đúng và màn không chậm thêm | - Tài khoản **production** có **≥10.000 bạn bè chưa chặn** (quy mô tương đương khách báo bug: ~15.000 lượt gửi / hạn mức 30.000)<br>- Tài khoản đó có **≥20 broadcast** ở tab 下書き / 配信予約, trong đó ≥10 broadcast gửi toàn bộ chưa gửi<br>- Ghi lại thời gian tải màn danh sách **trước khi deploy** làm mốc so sánh | 1. Trước deploy: mở màn 一斉配信 tab 下書き, bấm giờ thời gian từ lúc bấm tới lúc bảng hiển thị xong, ghi lại. Lặp 3 lần lấy trung bình<br>2. Sau deploy: lặp lại đúng thao tác đó, ghi lại thời gian, lặp 3 lần<br>3. Đọc con số ở cột 配信数 của các broadcast gửi toàn bộ<br>4. Mở màn sửa của 1 trong số đó và đối chiếu con số<br>5. Chuyển sang tab 配信予約 và lặp lại bước 1–2<br>6. Bấm 「コピー」 1 broadcast gửi toàn bộ, bấm giờ tới lúc màn sao chép hiển thị xong | Bot ≥10.000 bạn bè chưa chặn; ≥20 broadcast/trang<br>Phép tính tay: con số hiển thị phải bằng đúng tổng bạn bè chưa chặn hiện tại của tài khoản (đối chiếu với màn 友だちリスト) | - Con số ở danh sách là **số có 5 chữ số đúng bằng tổng bạn bè chưa chặn hiện tại**, khớp với màn 友だちリスト và khớp màn sửa — đây là lần đầu vế "4–5 chữ số" của bug được tái hiện ở quy mô thật<br>- Thời gian tải danh sách sau deploy **không tăng quá 20%** so với mốc trước deploy, ở cả 2 tab<br>- Màn sao chép hiển thị trong thời gian tương đương trước deploy<br>- Không có lỗi timeout / màn trắng | | **Lấp GAP-04 · cover impact F1 + F3** · Đánh giá spec: **Spec ghi rõ** (feature-spec §4 hàng 7) · Evidence: bảng thời gian đo 3 lần trước/sau deploy + ảnh màn danh sách thấy rõ số 5 chữ số · **RULE-08 → bắt buộc `product`**: chi phí query đếm trên 10.000+ bạn bè không kết luận được từ staging (12 bạn bè) · ⚠️ **Chỉ đọc, KHÔNG tạo/xoá dữ liệu thật**; bổ trợ cho `#15529` (đếm số query, `env_scope = local`) chứ không thay thế |
| TC-JOB001-01 | API | JOB-001 | Job gửi & vòng đời trạng thái | Normal | manual | staging | Broadcast đã đặt lịch có số hiển thị thay đổi — job vẫn gửi đúng và đủ người nhận | - Bot riêng của testcase có **8 bạn bè chưa chặn**, trong đó **≥1 tài khoản LINE thật** để nhận tin<br>- Có broadcast 「TC40399_JOB」 đặt lịch gửi **sau 10 phút**, đối tượng 「すべての友だち」, số gửi dự kiến đang lưu = **3** với mốc thời gian cũ<br>- Nội dung tin: 1 template text 「TC40399 job test」 | 1. Mở màn 一斉配信 tab 配信予約, đọc con số ở cột 配信数 của 「TC40399_JOB」<br>2. Kết bạn thêm **2 bạn mới** cho bot (thành 10 chưa chặn), tải lại danh sách và đọc lại con số<br>3. Chờ tới thời điểm đã đặt lịch, để job gửi<br>4. Sau khi gửi xong, mở tab 配信履歴 và đọc con số ở cột 配信数 của dòng đó<br>5. Bấm vào con số đó để mở danh sách bạn bè đã nhận, đếm số dòng<br>6. Mở **LINE app trên điện thoại thật** của tài khoản bạn bè test, kiểm tin đã tới chưa và nội dung có đúng không<br>7. Đối chiếu ở tầng dữ liệu số người đã gửi của bản ghi đó | 8 bạn chưa chặn ban đầu → 10 sau bước 2; số đang lưu = 3<br>Phép tính tay: bước 2 hiển thị **10**; số người thực nhận phải là **10** | - Bước 1 hiển thị 「8人（予定）」, bước 2 hiển thị 「10人（予定）」 — không phải 3<br>- Job gửi đúng thời điểm đã đặt, **không bị bỏ qua và không gửi trùng**<br>- Tab 配信履歴 hiển thị số **người đã gửi thật = 10**, KHÔNG bị thay bằng số bạn bè hiện tại nếu số này thay đổi tiếp<br>- Danh sách bạn bè đã nhận có đúng **10 dòng**<br>- **Tin nhắn tới thật trên LINE app**, nội dung đúng 「TC40399 job test」<br>- Số người đã gửi ở tầng dữ liệu = 10 | | **Lấp GAP-06 · cover impact F1 + T1 + T4** · Đánh giá spec: **Spec ghi rõ** (FA-008 — background job poll bảng `broadcast`; feature-spec §4 hàng 13 mapping trạng thái) · Evidence: ảnh LINE app trên máy thật + ảnh tab 配信履歴 + danh sách người nhận (**RULE-06** — đi tới output cuối chuỗi) · **regression** — nối tiếp `#15506` (chỉ dừng ở hiển thị) và `#15511` (chỉ dừng ở đọc số đã gửi) |
| TC-LIST001-01 | UI | LIST-001 | Phân trang & số dòng hiển thị | Normal | manual | staging | Số gửi dự kiến hiển thị đúng ở trang 2 và sau khi tìm kiếm / lọc thời gian | - Bot riêng của testcase có **12 bạn bè chưa chặn**<br>- Tab 下書き có **≥25 broadcast gửi toàn bộ** (đủ tràn sang trang 2 với cỡ trang mặc định), trong đó ≥5 broadcast đang lưu số cũ khác 12 (ví dụ 3)<br>- Có ≥1 broadcast **có điều kiện lọc** đang lưu số 2, nằm ở trang 2 | 1. Mở màn 一斉配信 tab 下書き trang 1, đọc con số của các broadcast gửi toàn bộ<br>2. Chuyển sang **trang 2**, đọc con số của các broadcast gửi toàn bộ ở trang này<br>3. Đọc con số của broadcast **có điều kiện lọc** ở trang 2<br>4. Quay về trang 1 rồi sang trang 2 lần nữa, đọc lại<br>5. Dùng **ô tìm kiếm** nhập tên 1 broadcast gửi toàn bộ đang lưu số cũ, đọc con số ở kết quả tìm kiếm<br>6. Dùng bộ **lọc theo thời gian** (「全期間」 → 1 khoảng thời gian), đọc lại con số của broadcast gửi toàn bộ trong kết quả<br>7. Đổi **số dòng hiển thị mỗi trang** sang mức lớn hơn để dồn tất cả về 1 trang, đọc lại toàn bộ | Bot 12 bạn chưa chặn; ≥25 broadcast, ≥5 broadcast đang lưu số cũ = 3; 1 broadcast có filter lưu số 2 | - Broadcast gửi toàn bộ hiển thị 「12人（予定）」 **ở cả trang 1 và trang 2**, không có trang nào rơi về số cũ 3<br>- Broadcast **có điều kiện lọc** ở trang 2 vẫn hiển thị 「2人（予定）」 kèm mốc thời gian cũ — không bị đổi thành 12<br>- Kết quả **tìm kiếm** và kết quả **lọc thời gian** đều hiển thị 12<br>- Sau khi đổi số dòng/trang, toàn bộ broadcast gửi toàn bộ vẫn hiển thị 12<br>- Không dòng nào để trống hoặc hiển thị lỗi | | **Lấp GAP-07 · cover impact F1 + F3 + T1** · Đánh giá spec: **Spec ghi rõ** (feature-spec §4 hàng 7) · Evidence: ảnh trang 1 + trang 2 + kết quả tìm kiếm, thấy rõ con số từng dòng · Bổ trợ cho `#15529` (đếm số query 1 lần/trang) ở góc **đúng/sai giá trị**, không phải góc hiệu năng |

**Kiểm RULE-01 sau khi bổ sung**:

| Quan điểm Cao | Normal | Abnormal | Boundary | Trạng thái |
|---|---|---|---|---|
| `DATA-COUNT-001` | `#15509` `#15521` | `#15552` + **`-04`** + **`-05`** | — | ⚠️ **vẫn thiếu Boundary** — biên 0 bạn bè đang gắn `FUNC-004` (`#15513` `#15525`). Đề nghị Leader chấp nhận cross-reference, hoặc gán lại mã cho `#15513`/`#15525` |
| `PERM-003` | — | `#15512` + **`-02`** | — | ⚠️ thiếu Normal + Boundary — ghi lý do: quan điểm phân quyền ở task này không có khái niệm biên; Normal (chọn đúng bot, copy bình thường) đã nằm trong `#15520` |
| `REG-SHARED-001` | — | `#15523` + **`-02`** | — | ⚠️ chưa đủ cho tới khi Dev nêu tên 3 chỗ dùng chung |
| `JOB-001` | **`-01`** | — | — | ⚠️ thiếu Abnormal (job gửi lỗi / quá hạn) — đề nghị lấy từ kho nhóm 「Job — quá hạn, lỗi & resume」 (6 TC) |
| `PERF-LARGE-001` | — | — | **`-01`** + `#15529` | ✓ |

---

## 6. Spec update needed

| # | Vấn đề | Nguồn | Cần ai chốt |
|---|---|---|---|
| **S1** | **Điều kiện rẽ nhánh của fix**: "broadcast gửi toàn bộ" xác định bằng `broadcast.flag_setting_filter = 0` hay bằng **sự tồn tại bản ghi `filters_v2`**? Hai thứ này **có thể lệch nhau** (kho MT-05). Đây là điểm quyết định BLOCKER-1 | `feature-spec.md` §4 hàng 6 vs note của Studio `#15510` `#15523` | **Dev — gấp** |
| **S2** | **kho MT-11** (⏳ CHỜ QUYẾT ĐỊNH): *"Số 配信数 ở màn list LỆCH với danh sách chi tiết khi chưa bấm 再計算 — bug hay hành vi cache?"* — corpus ghi tester **từng chấp nhận lệch là OK**. Fix nay **đảo ngược** kết luận đó cho broadcast không filter. MT-11 vẫn chưa được chốt | kho FA-008 MT-11 · `feature-spec.md` §5 BR-06 (*"`filter_number` được lưu cache"*) | **PM/BA + Leader** |
| **S3** | **kho MT-13** (CAO, ⏳ CHỜ QUYẾT ĐỊNH): 配信数 của broadcast **đã gửi** lấy `send_count` hay `filter_number`? `db-mapping.md:184` ghi **cả hai**. Tab 概要 của popup preview được ghi là *"vẫn như cũ"* (dùng `filter_number`) → có thể là 1 trong "3 chỗ dùng chung" | kho FA-008 MT-13 · bug gốc #31527 | **Dev + PM/BA** |
| **S4** | **`REQ-003` (Studio)** — hành vi số ở danh sách **đổi theo thời gian thực**: Dev ghi *"là thay đổi hiển thị nên cần PM/BA xác nhận"*; Studio ghi trong note `#15507` *"Không dùng TC này làm release blocker cho tới khi REQ-003 được xác nhận"*. **Nhưng TC đã bị tick `pass`** | `03-dev-impact.md` mục 7 · Studio `#15507` | **PM/BA** |
| **S5** | **`REQ-013` (Studio)** — ràng buộc bot của luồng sao chép: *"mã hiện tại không kiểm bot của broadcast gốc"*. Kỳ vọng đúng là **chặn** hay **cho phép**? | Studio `REQ-013` · `feature-spec.md` §5 BR-08 | **Dev + PM/BA** |
| **S6** | **Bản sao CÓ điều kiện lọc giữ nguyên mốc thời gian gốc "có thể rất cũ"** — Dev ghi là **cố ý** nhưng *"nếu nghiệp vụ muốn bản sao luôn tính mới thì phải mở khoá nút 再計算 trong lúc copy — nằm ngoài phạm vi ticket"*. Cần chốt để tester biết chấm Đạt hay Không đạt | `03-dev-impact.md` mục 7 rủi ro #3 · Studio `#15523` | **PM/BA** |
| **S7** | **Cập nhật `feature-spec.md` §4 hàng 7** — hiện ghi *"配信数 → `broadcast.filter_number`, Read, Cập nhật khi nhấn 「再計算」 hoặc thay đổi filter"*. Sau fix, với broadcast **không filter + chưa gửi** thì danh sách **không** đọc `filter_number` nữa mà đếm trực tiếp. Spec đang **sai so với code** | `feature-spec.md` §4 hàng 7 | **Dev cập nhật spec sau khi S1/S2 chốt** |
| **S8** | **kho MT-20** (CAO, ⏳ CHỜ QUYẾT ĐỊNH) — tính năng 「配信数上限アラート」 (#36436, ngưỡng cảnh báo) **không có trong spec**, ảnh hưởng ~39 TC kho. Đây là **câu hỏi thứ 2 của khách** ở ticket này | kho FA-008 MT-20 | **PM/BA + Leader** |
| **S9** | **Trả lời khách** — Dev kết luận cảnh báo 15.000/30.000 là **đúng thiết kế** (ngưỡng 50%), nhưng **không có TC nào** và không có bằng chứng đính kèm. Trao đổi với khách vẫn đang mở (journal 2026-09-03, ホアン vẫn đang xác nhận lại triệu chứng) | `01-bug-task.md` · Redmine journal 133791/133792 | **Leader + support** |

---

*Draft do Claude sinh cho Leader verify. TC ở mọi nguồn là read-only — mọi đề xuất xóa/sửa TC phải do human thực hiện trên Studio (`testcase_update` / `testcase_delete`).*
