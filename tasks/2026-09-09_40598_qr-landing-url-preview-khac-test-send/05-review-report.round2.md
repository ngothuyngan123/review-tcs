# 05 — Review Report (vòng 2)

## 0. Nguồn TC

- **Nguồn đã dùng**: MCP LME TEST STUDIO — task `#285` (round 1, branch `ai_fixbug_40598`, `status=tc-ready`, `reviewState=leader`, `aiResult=fail`, `ranAt=2026-09-14`, `exec: 17 pass / 2 fail / 1 error / 4 skip / 1 blocked`).
- **Tổng số TC review**: 25 (vòng 1: 15 — thêm 12, bỏ 2: `NEW-5`, `NEW-15`).

---

## 1. Coverage — 2 chiều `dev-impact` + `diff code`

**Kết luận: 11/16 mục §4.3 của Dev đã có TC `pass` · 7 GAP · 3 RISK · 4/12 file trong diff chưa có TC nào chạy xong.**

> ⚠️ **Phạm vi fix đã đổi kể từ vòng 1**: `spec_delta` của Studio nay là **12 file / +199 −26** (vòng 1 review trên bản **3 file**). Bộ TC đã bám theo bản mới — 3 GAP lớn của vòng 1 (`G3` Scenario, `G4` Broadcast, `G8` quick reply, `G9` image map, `G13` DATA-REF) **đã được lấp và pass**.

### 1a. Từng file trong diff có TC nào chạy xong không (adversarial Q1)

| # | File trong `spec_delta` | TC chạm | Kết quả mới nhất |
|---|---|---|---|
| 1 | `app/Services/TemplateService.php` | NEW-1/2/3/4/6/62 | ✅ pass (NEW-2 `error`) |
| 2 | `app/Helpers/ChatMessages.php` | NEW-18/23/41/44/63/64 | ⚠️ pass + 2 `fail` |
| 3 | `app/Http/Controllers/Api/ChatController.php` | NEW-20 | ✅ pass |
| 4 | `app/Services/ChatService.php` | NEW-17/18 | ✅ pass |
| 5 | `CalendarCourseBookingService.php` | NEW-56 | ✅ pass |
| 6 | `CalendarSalonLineBookingService.php` | NEW-56 | ✅ pass |
| 7 | `EventBookingService.php` | NEW-56 | ✅ pass |
| 8 | `FormAnswerService.php` | NEW-58 | ✅ pass |
| 9 | `app/Http/Controllers/Basic/UserController.php` | NEW-26 | ⛔ `skip` ×2 → **G2** |
| 10 | `app/Http/Controllers/LiffController.php` | NEW-59 | ⛔ `blocked` → **G1** |
| 11 | `app/Services/HelperService.php` | NEW-59 | ⛔ `blocked` → **G1** |
| 12 | `app/Services/Sales/SalesService.php` | NEW-59 | ⛔ `blocked` → **G1** |

### 1b. GAP / RISK

| Mã | Chiều | Vùng ảnh hưởng | Vấn đề | Status | Severity |
|---|---|---|---|---|---|
| **G1** | `diff code` | T12 · T13 · F9 — `SalesService` · `LiffController` · `HelperService::sendAction` | **3 file trong diff, 0 kết luận**. Cả 3 dồn vào **một** TC `NEW-59`, TC này `blocked` (note: *"Item: chỉ có multi action (job send); Action khi open form (link LIFF) => job send"*). Gộp 4 luồng vào 1 TC nên chặn 1 luồng là mất kết luận của cả 3 file | **GAP** | `[BLOCKER]` |
| **G2** | `diff code` | F6 — `executeActionOpenMobile` / `...Normal`, 5 biểu thức sửa ở `UserController.php:3145, 3289, 3292, 3616, 3619` | `NEW-26` **`skip` cả 2 lần** (local 09-14 04:55 · staging 09-14 09:39), lý do ghi đúng 1 chữ *"API"*; runner báo *"bot 1261 không có action open-mobile nào chứa đồng thời 3 URL và không dựng được bằng luồng người dùng"*. File này **không TC nào chạy xong** | **GAP** | `[BLOCKER]` |
| **G3** | `diff code` | `BUG` nhóm fix (C) — chống xoá trắng: `catch` của `makeLinkLandingPageIntro` (2 bản sao) + **5 hàm bên `ChatMessages`** + `makeLinkConversion` trả lại mã + `switch default` + sửa `catch \Exception` | `NEW-52` **`skip` ×2** — lần local: *"công cụ duy nhất (tạm gỡ bảng QR action) làm `getTemplate` trả mảng rỗng, gửi thử HTTP 500"*; lần staging: *"không dựng được tiền điều kiện"*. `NEW-48`/`NEW-50` chỉ phủ nhánh **dữ liệu không hợp lệ**, không phải nhánh **ném lỗi runtime**. Guard này do chính bản fix thêm vào — hỏng là tin gửi đi **rỗng**. **AP-1**: fix dạng generic catch ở 6 hàm mà **0 trigger chạy được** | **GAP** | `[BLOCKER]` |
| **G4** | `dev-impact` | T16 · D2 — URL Analytics (FA-023), **đếm lượt bấm** | `NEW-2` nay **đã có** bước đo `+1 click` trên màn 「URL分析」 (lấp đúng vế vòng 1 thiếu) nhưng kết quả mới nhất là **`error`**, triage: *"TEST-BUG — ô 短縮URL trên màn soạn tin là ô PHỦ ĐỊNH… mẫu tin bị lưu `is_shorten_url=0`"* → external URL không vào vòng rút gọn, **không kết luận được gì**. Chưa raise ticket bug, chưa chạy lại | **RISK** | `[BLOCKER]` |
| **G5** | `dev-impact` | T5 — Chat 1:1 web, nhánh **「sửa nội dung ngay trước khi gửi」** (Dev kê đích danh ở §4.3 mục 4) | `NEW-17` gửi template **nguyên bản**; không TC nào đi qua màn preview-sửa-gửi. Kho có đúng luồng này (`TC-CHT-216`) nhưng **không có mã giới thiệu** trong nội dung. Sau fix, nội dung sửa tay đi qua đúng cặp `sendShortUrl` / `makeLinkInMessage` vừa tách | **GAP** | `[MAJOR]` |
| **G6** | `dev-impact` | D1 · D2 — URL **có setting action** mà thôi được rút gọn | Kho `TC-TMT-138` ghi rule **action-thắng-checkbox**: URL có setting action **phải** bị shorten để hệ thống bắt action; `TC-TMT-158/159/160/161` cho thấy action click chạy qua `url_shorten.action`. Sau fix, link dựng từ mã + URL cùng miền **không còn bản ghi rút gọn** → action click và đếm click có nguy cơ ngừng chạy. **0 TC** (giữ nguyên từ vòng 1, §6-2 chưa chốt) | **GAP** | `[BLOCKER]` |
| **G7** | `diff code` | F5 · D1 · T16 — phân loại link theo **domain** | `NEW-4` vẫn dùng *"một đường dẫn trên miền hệ thống"* (**số ít**); `NEW-16` (custom domain, đối chiếu domain web↔job) **`skip`** lý do *"Job"*. 4 domain nội bộ Leader đã liệt kê (`step.lme.jp` · `s.lmes.jp` · `sl.lmes.jp` · `form.lmes.jp`) **không TC nào liệt kê đủ**; guard dùng `stripos` (so khớp chuỗi con) nên URL ngoài chứa tên domain nội bộ trong query có thể bị phân loại nhầm — **0 TC** | **GAP** | `[BLOCKER]` |
| **G8** | `dev-impact` | D3 — dữ liệu / link **đời cũ** | `NEW-30` **`skip`**, lý do người chạy ghi *"Đã release"*; runner ghi *"bot 1261 chưa có BẤT KỲ bản ghi rút gọn nào… không thể tự tạo link phát trước khi sửa"*. Vòng 1 đã cảnh báo đúng chỗ này: tiền đề phụ thuộc may rủi nên `COMPAT-LEGACY-001` (ưu tiên **Cao**) vẫn **không có kết luận** | **RISK** | `[MAJOR]` |
| **G9** | `diff code` | F3 — 3 nhánh trong `getTemplate` | `NEW-6` vẫn giữ bước tuỳ nghi *"**Nếu có** `template_url_redirect`, chạy lại biến thể B"*. Lượt auto của TC này bị `skip` (thiếu 4 loại mã trên bot 1261), sau đó được chấm `pass` **thủ công** — không có gì chứng minh nhánh redirect đã chạy | **RISK** | `[MAJOR]` |
| **G10** | `dev-impact` | T7 — **Action Schedule** (FA-016), tin gửi theo lịch | Nằm trong `NEW-59` (`blocked`). Bước *"chờ đúng thời điểm schedule chạy"* chưa bao giờ thực thi; note người chạy: *"chỉ có multi action (job send)"* | **GAP** | `[MAJOR]` |

> **Adversarial Q1** (mỗi file trong diff có TC đi qua?) — ❌ 12/12 file **có** TC, nhưng chỉ **8/12** có TC chạy xong → **G1, G2**.
> **Adversarial Q2** (nhánh mới; generic-fix ≥ 3 trigger + 1 trigger chưa biết) — ❌ nhóm fix (C) chạm **6 hàm** mà trigger duy nhất (`NEW-52`) chưa chạy được lần nào → **G3**, **AP-1**.
> **Adversarial Q3** (hàm dùng chung có danh sách caller + TC từng nơi?) — ✅ Dev có danh sách; TC nay phủ **12/16** mục §4.3 và đã pass 11 → phần lớn đã đóng so với vòng 1.
> **Adversarial Q4** (hành vi đổi: verify cả chiều mới lẫn chiều cũ không hỏng?) — ⚠️ chiều mới có TC pass; chiều **"cũ không hỏng"** vẫn thiếu vế đo lường (đếm click **G4**, action click **G6**, dữ liệu đời cũ **G8**).

---

## 2. Quan điểm test còn thiếu

**Kết luận: 7/20 quan điểm khớp trigger đã cover đủ · 13 thiếu.**

| Mã | Quan điểm | Ưu tiên | Vì sao thiếu | Status | Severity |
|---|---|---|---|---|---|
| **Q1** | `REG-URL-001` ★ | Trung bình → **Cao** (CR chạm màn soạn tin + URL) | Ma trận checkbox 「URL gốc」 (kho `TC-TMT-136/137/138/139`) **không TC nào mang mã**. Nặng hơn: tiền đề TC Studio viết *"template **BẬT** rút gọn URL"* trong khi UI chỉ có ô **phủ định** 「URL gốc」 (`:checked="is_shorten_url == 0"`, spec Field Matrix #9 `Checked=0 / Unchecked=1`) → người chạy tick ngược là ra kết luận ngược (đã xảy ra: `NEW-2`, `NEW-3` `error`) | **GAP** | `[BLOCKER]` |
| **Q2** | `MSG-USER-001` | **Cao** | TC duy nhất mang mã là `NEW-64`, đang **`fail`**, và bug sinh ra từ nó (#1021) đã bị **reject** vì *"Group (`line_user.type=1`) sẽ không shorten + ko gen code"* → expected TC sai, chưa sửa ⇒ quan điểm này **chưa có kết luận hợp lệ** | **RISK** | `[BLOCKER]` |
| **Q3** | `INTG-LINE-001` | **Cao** | TC duy nhất mang mã là `NEW-52` — `skip` ×2 (xem G3) | **RISK** | `[BLOCKER]` |
| **Q4** | `DATA-COUNT-001` | **Cao** (BẮT BUỘC khi màn hình có con số đếm) | Chỉ `NEW-2` chạm số đếm 「URL分析」 và đang `error` (G4). Vế **đo mức mất số liệu** của URL cùng miền đã bị Leader loại ở vòng 1 — ghi nhận, không đề xuất lại | **RISK** | `[MAJOR]` |
| **Q5** | `ENV-003` ★ | **Cao** (BẮT BUỘC khi chạm URL/domain, job nền) | `envAuto` cho thấy **`prd`: runs = 0** — task chạm domain · URL rút gọn · job nền · số liệu click mà **0 TC chạy production**. TC mang mã (`NEW-16`) lại `skip`. **RULE-08** | **RISK** | `[MAJOR]` |
| **Q6** | `COMPAT-LEGACY-001` ★ | **Cao** | `NEW-30` `skip` (G8). Nhánh template **đời cũ chứa URL đã bị xóa khỏi bảng `url`** (kho `TC-TMT-163/164`) vẫn **0 TC**. **RULE-09** | **RISK** | `[MAJOR]` |
| **Q7** | `JOB-001` ★ | **Cao** | `NEW-14` (đối chiếu web ↔ richmenu) nay **pass** ✅ — vế chính đã đóng. Nhưng `NEW-16` — vế **so miền referral do job sinh vs do web sinh** — `skip` lý do *"Job"*, tức nửa còn lại của câu hỏi khách (URL hai đường khác miền) chưa verify | **RISK** | `[MAJOR]` |
| **Q8** | `FUNC-003` | **Cao** (nâng — field liên quan URL) | **0 TC `Boundary`** trên toàn bộ 25 TC. Fix đổi đúng vùng **nhận dạng URL** + thứ tự xử lý, nhưng không TC nào thử URL biên: URL cuối câu có dấu chấm, URL trong 「」, 2 URL liền nhau, mã nằm ngay sát URL, URL rất dài | **GAP** | `[MAJOR]` |
| **Q9** | `REG-SHARED-001` | **Cao** | 13 TC (nhiều nhất bộ) nhưng **0 `Boundary`** — **RULE-01**, không TC nào ghi lý do | **RISK** | `[MAJOR]` |
| **Q10** | `OUT-TRUTH-001` | **Cao** | 5 TC = 3 `Normal` + 2 `Abnormal`, **0 `Boundary`** — **RULE-01**. Ngoài ra TC `Normal` đại diện (`NEW-2`) đang `error` | **RISK** | `[MAJOR]` |
| **Q11** | `MSG-004` | **Cao** (BẮT BUỘC khi output là nội dung user cuối thấy trên LINE) | **0 TC mang mã**. Rủi ro: link giới thiệu nay là URL **đầy đủ** (dài hơn short link) → tin dài ra, nguy cơ chạm giới hạn ký tự LINE. ⚠️ `TC-MSG004-02`/`-03` đã bị **Leader loại 2026-09-09** → không đề xuất lại, nhưng rủi ro vẫn **chưa được xử lý** | **GAP** | `[MAJOR]` |
| **Q12** | `DATA-CACHE-001` | **Cao** (nâng — output user-facing) | **0 TC**. Trigger nêu đích danh *"chức năng dùng short link / preview"* — fix đổi cả hai. Kho còn ghi cache 30 giây của nguồn tin ở chat 1:1 (`TC-CHT-222/225`, MT-18). ⚠️ `TC-DATACACHE001-01` bị **Leader loại 2026-09-09** → ghi nhận, không đề xuất lại | **GAP** | `[MAJOR]` |
| **Q13** | `LIFF-ENTRY-001` ★ | **Cao** | `NEW-1` nay **mở link giới thiệu thật** và verify trang đích + `u_code` ✅. Còn thiếu: `[FORM_x]` / `[CONVERSION_x]` / `[ITEM_x]` ở `NEW-6` chỉ kiểm *"ra URL thật, không còn ngoặc vuông"* — **không mở link**, không xác nhận form/conversion/item load đúng và ghi nhận đúng người | **RISK** | `[MAJOR]` |

> Quan điểm đã cover đủ (không ghi dòng): `FUNC-001` · `FUNC-MULTI-001` · `DATA-TEXT-001` · `DATA-REF-001` (nay có `NEW-48`/`NEW-50` pass) · `SYNC-APP-001` (`NEW-20` pass sau khi bug #40935 closed) · `OUT-PREVIEW-001` (`NEW-17`/`18`/`56`/`58` nay verify đủ `messages_v2s.content` + bong bóng admin + `conversation.last_message`) · `FRIEND-001` (`NEW-23` pass, đã có biến thể friend info **nằm trong URL**).

---

## 3. TC trùng lặp

**Đã rà đủ 25 TC** theo 4 yếu tố (`mã quan điểm` × `loại case` × `đối tượng + thao tác` × `tiền đề tương đương`) — phát hiện **1 nhóm trùng**.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa/gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| Hội thoại `line_user.type = 1` | **NEW-63** (có đủ 2 nhánh bot ON/OFF) | **NEW-64** → **GỘP**, không xóa | `DUP-SUBSET` | Đối tượng + thao tác: *gửi tin chứa `[LANDING_INTRO_x]` tới hội thoại `type=1`* — **giống hệt** (Dev reject cả 2 bug bằng **cùng một câu**: *"Group (`line_user.type=1`) sẽ không shorten + ko gen code do ko xác định được friend"*). Tiền đề tương đương, `Kết quả mong đợi` tương đương (*"không đầu ra nào còn raw `LANDING_INTRO`"*), cùng `fail` trong cùng run #1402. Khác duy nhất: nhãn `Loại case` (`Normal` vs `Abnormal`) và mã quan điểm | `[MINOR]` |

⚠️ **Gate xóa**: `NEW-64` là TC **duy nhất** mang `MSG-USER-001` → **không đề nghị xóa**, chỉ **gộp**: giữ `NEW-63`, bổ sung mã quan điểm `MSG-USER-001` + nhánh `Abnormal` vào nó, rồi xóa `NEW-64` trên Studio. Nếu giữ cả hai thì phải **sửa expected cả hai** (§4-1) — giữ nguyên như hiện tại là bộ TC có 2 TC đỏ vĩnh viễn vì cùng một lý do.

**Ghi nhận chồng lấn một phần (KHÔNG đề nghị xóa/gộp):**

| Cặp | Chồng lấn | Vì sao vẫn giữ cả hai |
|---|---|---|
| `NEW-3` / `NEW-4` ↔ `NEW-26` (A/B) | Cùng kiểm hai chiều của biểu thức `/landing-qr/` | Khác file trong diff (`TemplateService` vs `UserController`) — `NEW-26` là TC **duy nhất** chạm `UserController` |
| `NEW-18` ↔ `NEW-3`/`NEW-4` | Cùng bộ 3 dạng URL | Khác đường gửi (`ChatMessages` free-text vs `TemplateService` test send) |
| `NEW-48` ↔ `NEW-50` | Cùng expected *"không dựng được link thì giữ nguyên mã"* | Khác nhánh code (`makeLinkLandingPageIntro` vs `makeLinkConversion` + `switch default`) |
| `NEW-41` / `NEW-44` / `NEW-45` | Cùng khuôn *"biến thể A qua `TemplateService`, B qua `ChatHelper`, × bot ON/OFF"* | Khác đối tượng gửi (text · quick reply · image map) → 3 cặp hàm khác nhau |

---

## 4. Issues khác

### Chất lượng nguồn TC

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 1 | `[BLOCKER]` | **NEW-63**, **NEW-64** | **Expected mâu thuẫn quyết định của Dev.** Bug #1048 + #1021 đã **rejected** với lý do *"Group (`line_user.type=1`) sẽ không shorten + ko gen code do ko xác định được friend (do có nhiều friend trong 1 group)"* — tức sản phẩm đang chạy **đúng thiết kế**, còn expected TC (*"không đầu ra nào còn raw `LANDING_INTRO`"*) là **sai**. Hệ quả: `last_exec` vẫn `fail`, bộ TC không bao giờ xanh; và trạng thái đã đảo 4 lần trong 1 ngày (`fail` 04:44 → `pass` 04:54 → `blocked` 08:36 → `fail` 09:22) trên cùng một lý do | `testcase_update` expected theo quyết định Dev, rồi **chạy lại**. ⚠️ Trước đó phải chốt §6-1: bằng chứng run #1402 cho thấy tin gửi lên LINE group **còn nguyên** `紹介:[LANDING_INTRO_WZnzuU]` → **người dùng cuối nhìn thấy mã thô**; chưa ai xác nhận đó là chấp nhận được |
| 2 | `[BLOCKER]` | **NEW-62** | **TC tự khai không có tiêu chí pass/fail nhưng được chấm `pass`.** Expected ghi nguyên văn *"Nếu quan sát đúng như vậy thì **KHÔNG kết luận pass hay fail**, mà chuyển cho người phát triển xác nhận"* — vậy mà `last_exec = pass` (run #1402). Đây chính là bug **#979** (đang `stale`) và Studio `dev_impact` khẳng định: *"**Bug 979 CHƯA vá**: `getTemplate` vẫn chỉ đọc `template->is_shorten_url`, bỏ qua `bot->is_shorten_url`"* → một defect **đã biết** đang được đánh dấu Đạt | Đổi `pass` → `blocked`; chốt **REQ-017** ở §6-2 trước khi đóng ticket. Không dùng `NEW-62` làm bằng chứng cho bất kỳ kết luận nào |
| 3 | `[BLOCKER]` | **NEW-2** | `error` và **chưa raise ticket bug** (0.6-2). Đây là TC **duy nhất** đo lượt bấm 「URL分析」 (G4) | Sửa tiền đề theo issue #4, chạy lại; nếu vẫn lỗi thì raise bug |
| 4 | `[BLOCKER]` | ~10 TC (`NEW-1/2/3/4/6/62` + mọi TC ghi *"template BẬT rút gọn"*) | **Tiền đề ghi ngược semantics UI.** Trên màn soạn tin **không có** ô "bật rút gọn" — chỉ có ô **phủ định** 「URL gốc」: `:checked="is_shorten_url == 0"` (triage run #1402), khớp spec `message-template/feature-spec.md:338, 621` (*Checked=0 (URL gốc), Unchecked=1 (shortened)*) và kho `TC-TMT-136/137`. Người chạy đọc *"BẬT rút gọn"* rồi **tick** ô → lưu `is_shorten_url=0` → kết quả ngược. Đã làm hỏng 2 lượt chạy (`NEW-2`, `NEW-3` cùng `error` với đúng nguyên nhân này) | Viết lại tiền đề bằng **thao tác UI**: *"**KHÔNG tick** ô 「URL gốc」 (⇒ URL ngoài được rút gọn)"* / *"**Tick** ô 「URL gốc」 (⇒ giữ URL gốc)"*. Rà lại toàn bộ TC dùng cụm "BẬT/TẮT rút gọn của **mẫu tin**" — cụm này ở **cấp bot** thì đúng, ở **cấp mẫu tin** thì ngược |
| 5 | `[MAJOR]` | Toàn bộ 25 TC | **Tỷ lệ pass thật = 17/25 = 68% (< 80%)** → 0.6-1. 8 TC **không có kết luận**: 2 `fail` · 1 `error` · 4 `skip` · 1 `blocked` | Mọi dòng đánh ✅ ở §1a chỉ là "có TC pass"; các vùng còn lại chưa được verify |
| 6 | `[MAJOR]` | **43/43 lượt chạy manual** | **RULE-02 — `evidence = []` ở 100% lượt chạy.** Không lượt nào đính ảnh tin trên LINE / ảnh màn 「URL分析」 / bản ghi `messages_v2s.content`. Mọi kết luận "Đạt" hiện là **tự khai** | Bổ sung loại evidence bắt buộc vào `Ghi chú` từng TC và yêu cầu đính kèm trước khi Leader duyệt |
| 7 | `[MAJOR]` | Toàn bộ 25 TC | **RULE-08 / ENV-003 — 0 TC chạy production** (`envAuto`: `prd` total 25, automated 0, **runs 0**). Task chạm **domain · URL rút gọn · job nền · số liệu click** — đúng 4 hạng mục RULE-08 cấm kết luận từ staging | Chốt nhóm TC bắt buộc chạy `product` (tối thiểu: domain nội bộ, đếm click, đối chiếu web↔job) |
| 8 | `[MAJOR]` | **NEW-59** | **Không atomic** — 1 TC gộp **4 luồng** (Sales · LIFF · Action trực tiếp · Action Schedule) và **3 file** trong diff. `blocked` một luồng làm mất kết luận của cả 3 file (G1) | Tách thành 4 TC độc lập để 1 luồng bị chặn không kéo 3 luồng còn lại |
| 9 | `[MAJOR]` | **NEW-16**, **NEW-26**, **NEW-30**, **NEW-52** | **Lý do `skip` không tái lập được** — ghi đúng 1–2 chữ: *"Job"* · *"API"* · *"Đã release"* · *"Không dựng được tiền điều kiện"*. Không nêu fixture còn thiếu nên không ai biết cần chuẩn bị gì để chạy được (**RULE-03**). Log runner có mô tả chi tiết hơn hẳn phần người chạy ghi | Ghi rõ fixture thiếu + ai chuẩn bị + env nào chạy được; 4 TC này đều thuộc quan điểm ưu tiên **Cao** |
| 10 | `[MAJOR]` | 23/25 TC | **Thiếu `Trạng thái đánh giá spec`** — `spec_status` rỗng ở 23 TC (chỉ 2 TC ghi `needs-human-review`). Không TC nào khai `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` → không phân biệt được expected nào dựa trên spec, expected nào do người viết tự suy | Điền `spec_status` trước khi duyệt; các TC chạm rule **không có trong spec** (action-thắng-checkbox, cờ bot vs cờ template, hành vi group) phải ghi `Spec không ghi` + nêu đã hỏi ai |
| 11 | `[MAJOR]` | 25/25 TC | **`status = draft` ở toàn bộ TC** trong khi task đã `tc-ready` và `reviewState = leader` — chưa TC nào được chốt | Chốt trạng thái TC trên Studio trước khi đưa Leader duyệt |
| 12 | `[MINOR]` | **NEW-1**, **NEW-62** | **2 mã quan điểm không có trong `framework/checklist-lme.md`**: `TOOL-KNOW-002`, `TOOL-AXIS-001` (mã nội bộ Studio) → không map được coverage (vòng 1 issue #3, **chưa xử lý**). ✅ `NEW-23` đã sửa xong sang `REG-SHARED-001` | `NEW-1` → `LIFF-ENTRY-001`; `NEW-62` → `REG-URL-001` |
| 13 | `[MINOR]` | 24/25 TC | `env_tag = local-only` trong khi thực tế đã chạy trên `staging` → nhãn môi trường sai lệch (vòng 1 issue #2, chưa xử lý) | Đồng bộ `env_tag` với `env_scope` thật |
| 14 | `[MINOR]` | `NEW-1/2/3/4/6/26/48/50` | `Dữ liệu test` còn placeholder cho field nghiệp vụ: `abc123`, `zzz999`, `form01`, `cv01`, `example.com` (vòng 1 issue #12, chưa xử lý) | Thay bằng mã QR / `u_code` / domain thật của env test |

### Chất lượng từng TC + anti-pattern

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| 15 | `[AP-1]` `[BLOCKER]` | Nhóm fix (C) chống xoá trắng | **Single-trigger generic-fix** — fix áp cho **6 hàm** (`makeLinkLandingPageIntro` ×2, 5 nhánh catch `ChatMessages`, `makeLinkConversion`, `switch default`) nhưng chỉ có **1 TC trigger** (`NEW-52`) và TC đó **chưa chạy được lần nào** | Cần ≥ 3 trigger khác nhau + 1 trigger "lỗi chưa biết". Chờ Dev trả lời §6-6 (điều kiện ném lỗi) |
| 16 | `[AP-3]` `[MAJOR]` | Toàn bộ 25 TC | **Happy-path-only** — 17 `Normal` + 8 `Abnormal` + **0 `Boundary`**; 4 quan điểm ưu tiên **Cao** thiếu loại case mà không TC nào ghi lý do (**RULE-01**) | Bổ sung `TC-FUNC003-01` ở §5 |
| 17 | `[MAJOR]` | **NEW-6** | Bước 4 vẫn tuỳ nghi (*"**Nếu có** `template_url_redirect`"*) — vòng 1 issue #8 **chưa xử lý**. Lượt auto đã `skip` vì bot thiếu 4 loại mã, sau đó chấm `pass` thủ công → không chứng minh được nhánh redirect đã chạy (G9) | Tách nhánh `template_url_redirect` thành TC riêng, tiền đề **bắt buộc** |
| 18 | `[MAJOR]` | **NEW-16** | `Kết quả mong đợi` vẫn **không đo lường được**: *"Nếu hai domain khác nhau thì không tự kết luận pass… phải chuyển Dev/PM xác nhận"* (vòng 1 issue #10, chưa xử lý) | Chốt §6-3 trước, rồi viết expected thành giá trị cụ thể |
| 19 | `[MINOR]` | **NEW-59** | Tự cho phép bỏ qua: *"nếu môi trường không chạy được scheduler thì testcase phải skip phần này"* → TC ưu tiên Cao có sẵn đường thoát | Tách Action Schedule thành TC riêng có tiền đề bắt buộc (cùng issue #8) |

---

## 5. TCs đề xuất bổ sung (5)

> Bảng **14 cột** = 12 cột kho + `Chạy` + `Phạm vi ENV`.
> ⚠️ **Không đề xuất lại** 11 TC Leader đã loại ngày 2026-09-09 (`TC-DATACOUNT001-02/-03`, `TC-FRIEND001-02`, `TC-COMPATLEGACY001-02/-03`, `TC-ENV003-03`, `TC-MSG004-02/-03`, `TC-OUTTRUTH001-04`, `TC-DATACACHE001-01`, `TC-REGSHARED001-13`) — hệ quả còn treo đã ghi ở **Q11 · Q12 · Q4**.
> ⚠️ `G1` · `G2` · `G3` · `G10` **không đẻ TC mới** — TC đã tồn tại, việc phải làm là **tách / dựng fixture / chạy lại** (§4-8, §4-9, §4-15).

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa010-mautinnhan-テンプレート.md` · `kho-tcs/fa001-chat11-11チャット.md` — ⚠️ kho **chưa có FA-017** (QR Landing), không đối chiếu được phần trang giới thiệu |
| Vùng regression phát hiện từ kho | `TC-TMT-136/137/138/139` (ma trận checkbox 「URL gốc」) · `TC-TMT-158→161` (action click qua `url_shorten.action`) · `TC-TMT-163/164` (template đời cũ, URL đã xóa) · `TC-CHT-216` (sửa nội dung ngay tại preview trước khi gửi) · `TC-CHT-222/225` (cache 30 giây nguồn tin chat 1:1) |
| Conflict expected vs kho | `TC-REGURL001-01` vs `TC-TMT-138` — kho ghi *"URL có setting action **vẫn bị shorten**"*, còn hệ quả fix (D1/D2) là *"URL cùng miền + link dựng từ mã **không còn** bản ghi rút gọn"* → **`[MAJOR]` SPEC-CONFLICT, đã đưa §6-4**. Không tự chọn bên |
| GAP dùng lại TC kho (không viết mới) | `Q1` → `TC-TMT-136` · `TC-TMT-137` · `TC-TMT-139` (ma trận checkbox đúng semantics) · `Q6` → `TC-TMT-163` · `TC-TMT-164` (template đời cũ) · `Q12` → `TC-CHT-222` · `TC-CHT-225` (cache 30 giây) |
| Xác nhận chống trùng | Đã đối chiếu **25** TC ở BƯỚC 0 + 2 file kho — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-REGSHARED001-14 | UI | REG-SHARED-001 | Chat 1:1 — gửi template có sửa nội dung tại preview | Normal | manual | Tất cả | Sửa nội dung template ngay tại màn preview rồi gửi — mã giới thiệu vẫn ra link đầy đủ | - Đăng nhập admin, đang chọn bot A, mở màn chat 1:1 với friend U1 đã kết bạn và **có `u_code`**<br>- Bot A **BẬT** rút gọn URL (setting cấp bot)<br>- Có group template T gồm 1 template con dạng text, nội dung chứa `[LANDING_INTRO_<mã QR còn hoạt động>]` + 1 URL ngoài<br>- Ô 「URL gốc」 của template con **KHÔNG tick** (⇒ URL ngoài sẽ được rút gọn) | 1. Ở chat 1:1 của U1, chọn group template T → bấm gửi → màn preview trước khi gửi hiện ra<br>2. Hover vào nội dung template con → bấm nút sửa<br>3. Thêm 1 dòng chữ mới vào **trước** mã giới thiệu và sửa URL ngoài thành URL ngoài khác<br>4. Quay lại preview, bấm 「上記の内容で送信」<br>5. Mở LINE của U1, ghi lại nguyên văn tin nhận được<br>6. Tải lại màn chat 1:1, đọc lại bong bóng tin vừa gửi<br>7. Lặp lại bước 1–6 nhưng bấm 「元の内容にリセットする」 trước khi gửi | Template con: `ご案内です。\n紹介: [LANDING_INTRO_<mã QR>]\n資料: <URL ngoài 1>`<br>Sửa tại preview thành: `本日のご案内です。\n紹介: [LANDING_INTRO_<mã QR>]\n資料: <URL ngoài 2>` | - Tin trên LINE: mã giới thiệu ra **URL đầy đủ** `<miền>/landing/page-intro/<mã QR>/<u_code của U1>`, **không** còn chuỗi `[LANDING_INTRO_…]`; URL ngoài **2** (bản đã sửa) ở dạng rút gọn và mở đúng đích<br>- Bong bóng chat admin sau reload: hiện **URL ngoài 2 dạng đầy đủ** + link giới thiệu đầy đủ, không còn mã thô<br>- Dòng chữ mới thêm vẫn còn nguyên, không bị cắt<br>- Lần chạy có bấm reset: gửi đúng nội dung **gốc**, quy tắc dựng link không đổi |  | Lấp `G5` · Đánh giá spec: Spec không ghi · dẫn từ `TC-CHT-216` (luồng preview-sửa-gửi) · Evidence: ảnh tin trên LINE + ảnh bong bóng chat sau reload |
| TC-REGURL001-01 | UI | REG-URL-001 | Mẫu tin — 「URL表示期限・アクション設定」 | Abnormal | manual | product | URL có setting action sau fix — action click còn chạy và còn đếm được không | - Đăng nhập admin, bot A **BẬT** rút gọn URL<br>- Có template text TU chứa 1 URL ngoài đã **setting action khi click** = gắn tag T (tab 「URL表示期限・アクション設定」)<br>- Có template text TU2 chứa `[LANDING_INTRO_<mã QR>]` đã setting action khi click cho chính link giới thiệu (nếu UI cho phép)<br>- Friend U1 đã kết bạn, có `u_code`, **chưa** có tag T | 1. Với TU: **tick** ô 「URL gốc」 → 保存 → gửi thử cho U1<br>2. Quan sát URL trong tin trên LINE: có bị rút gọn không<br>3. U1 bấm URL → kiểm tra mở đúng đích, kiểm tra U1 **đã được gắn tag T** chưa<br>4. Mở màn 「URL分析」 đối chiếu lượt bấm của URL đó<br>5. Với TU2: gửi thử cho U1, bấm link giới thiệu, kiểm tra action và lượt bấm tương tự<br>6. Ghi lại có/không sinh bản ghi rút gọn mới cho từng URL | TU: 1 URL ngoài + action gắn tag T + tick 「URL gốc」<br>TU2: `[LANDING_INTRO_<mã QR>]` + action (nếu setting được) | - TU: URL **vẫn bị rút gọn** dù đã tick 「URL gốc」 (rule action-thắng-checkbox), U1 **được gắn tag T**, lượt bấm trên 「URL分析」 tăng đúng 1<br>- TU2: ghi rõ link giới thiệu sau fix **có** sinh bản ghi rút gọn hay không; nếu **không** thì ghi nhận action click và lượt bấm của link giới thiệu **không chạy** — đây là hệ quả cần Dev/PM chốt, **không tự kết luận pass** |  | Lấp `G6` · `Q1` · RULE-08 (đếm click + domain) · Đánh giá spec: Spec không ghi — rule action-thắng-checkbox chỉ có ở kho `TC-TMT-138` (MT-08) · SPEC-CONFLICT → §6-4 · Evidence: ảnh tin LINE + ảnh màn 「URL分析」 + ảnh tag của U1 |
| TC-ENV003-04 | UI | ENV-003 | Mẫu tin — gửi thử, phân loại link theo domain | Normal | manual | product | Từng domain nội bộ của LME có đúng là KHÔNG bị rút gọn không | - Đăng nhập admin trên **production**, bot A **BẬT** rút gọn URL<br>- Template text TD **không tick** 「URL gốc」<br>- Nội dung TD chứa **mỗi domain nội bộ một URL riêng** + 1 URL ngoài làm đối chứng<br>- Friend U1 đã kết bạn, có `u_code` | 1. Tạo TD với đủ các URL ở cột Dữ liệu nhập → 保存<br>2. Gửi thử TD cho U1<br>3. Đọc tin trên LINE, ghi lại **từng** URL ở dạng đầy đủ hay dạng `<miền>/l/<khóa>`<br>4. Mở màn 「URL分析」 đối chiếu URL nào sinh bản ghi rút gọn mới<br>5. Bấm lần lượt từng link trên LINE, xác nhận mở đúng trang đích | Mỗi dòng 1 URL: `step.lme.jp/...` · `s.lmes.jp/...` · `sl.lmes.jp/...` · `form.lmes.jp/...` · 1 URL chứa `/landing-qr/` · 1 URL ngoài `https://example.com/campaign` | - **Từng** URL trên 4 domain nội bộ: ghi rõ giữ nguyên dạng đầy đủ hay bị rút gọn, và có sinh bản ghi rút gọn không<br>- URL chứa `/landing-qr/`: **vẫn bị rút gọn** (ngoại lệ có chủ ý)<br>- URL ngoài: **vẫn bị rút gọn** và vẫn đếm được lượt bấm<br>- Mọi link đều mở đúng trang đích<br>- Nếu có domain nội bộ nào **vẫn bị rút gọn** → ghi nhận từng domain, không kết luận pass chung |  | Lấp `G7` · `Q5` · RULE-08 (domain, bắt buộc production) · Đánh giá spec: Đã hỏi leader (danh sách 4 domain, 2026-09-09) — chờ §6-8 · Evidence: ảnh tin LINE liệt kê đủ các URL + ảnh màn 「URL分析」 |
| TC-ENV003-05 | UI | ENV-003 | Mẫu tin — gửi thử, phân loại link theo domain | Abnormal | manual | product | URL ngoài có chứa tên domain nội bộ trong query — không được phân loại nhầm | - Như `TC-ENV003-04`<br>- Template text TE **không tick** 「URL gốc」 | 1. Tạo TE với các URL ở cột Dữ liệu nhập → 保存<br>2. Gửi thử TE cho U1<br>3. Đọc tin trên LINE, ghi lại dạng của **từng** URL<br>4. Bấm từng link, xác nhận mở đúng trang đích (không bị cắt query)<br>5. Đối chiếu bản ghi rút gọn mới trên 「URL分析」 | `https://tracker.example.com/r?to=https://s.lmes.jp/abc` · `https://example.com/landing-qr/fake` · `https://example.com/?ref=step.lme.jp` | - Cả 3 URL đều là URL **ngoài** → **phải bị rút gọn** và đếm được lượt bấm<br>- Bấm vào mở đúng trang đích, **query giữ nguyên**, không bị cắt ở đoạn chứa tên domain nội bộ<br>- Nếu có URL nào bị **giữ nguyên** (phân loại nhầm thành nội bộ) hoặc `https://example.com/landing-qr/fake` được xử lý như link QR thật → ghi nhận là lỗi phân loại `stripos` so khớp chuỗi con |  | Lấp `G7` · RULE-08 · Đánh giá spec: Spec không ghi · Evidence: ảnh tin LINE + ảnh URL đích sau khi bấm |
| TC-FUNC003-01 | UI | FUNC-003 | Mẫu tin — gửi thử, nhận dạng URL biên | Boundary | manual | Tất cả | Dạng URL biên nằm cạnh mã giới thiệu — nhận dạng và dựng link vẫn đúng | - Đăng nhập admin, bot A **BẬT** rút gọn URL<br>- Template text TB **không tick** 「URL gốc」<br>- Nội dung TB gồm đủ các dạng biên ở cột Dữ liệu nhập<br>- Friend U1 đã kết bạn, có `u_code` | 1. Tạo TB với nội dung ở cột Dữ liệu nhập → 保存<br>2. Gửi thử TB cho U1<br>3. Đọc tin trên LINE, đối chiếu **từng dòng** với nội dung gốc<br>4. Bấm từng link, xác nhận mở đúng đích<br>5. Tải lại chat 1:1 / màn xem lại tin, đối chiếu nội dung lưu | Dòng 1: `詳細はこちら https://example.com/a。` (URL cuối câu, liền dấu chấm tiếng Nhật)<br>Dòng 2: `「https://example.com/b」をご覧ください` (URL trong ngoặc kép JP)<br>Dòng 3: `https://example.com/c https://example.com/d` (2 URL liền nhau)<br>Dòng 4: `紹介:[LANDING_INTRO_<mã QR>]https://example.com/e` (mã dính sát URL, không có khoảng trắng)<br>Dòng 5: 1 URL ngoài dài > 300 ký tự có nhiều query<br>Dòng 6: `https://example.com/f?name={name}&info=[FRIEND_INFO_<mã>]` | - Mọi URL được nhận dạng **đúng biên**: dấu `。` và `」` **không** bị nuốt vào URL, 2 URL liền nhau được xử lý thành 2 link riêng<br>- Dòng 4: mã giới thiệu ra link đầy đủ **và** URL ngoài liền sau vẫn được xử lý riêng, không dính thành một chuỗi<br>- Dòng 5: URL dài được rút gọn và mở đúng đích, không bị cắt query<br>- Dòng 6: `{name}` và `[FRIEND_INFO_x]` được thay bằng giá trị thật **trước** khi rút gọn; mở link ra query chứa giá trị thật<br>- Toàn tin: không mất chữ, không thừa ký tự, nội dung lưu khớp nguyên tắc (LINE rút gọn / chat gốc) |  | Lấp `Q8` · `Q9` · `Q10` (RULE-01 — TC `Boundary` duy nhất của bộ) · Đánh giá spec: Spec không ghi · Evidence: ảnh tin LINE + ảnh bong bóng chat sau reload |

### 5a. Truy vết — mọi `G<x>` / `Q<x>` phải có TC hoặc lý do

| Mã | Nội dung rút gọn | Lấp bằng |
|---|---|---|
| G1 | Sales · LIFF · `HelperService::sendAction` — `NEW-59` blocked | ❌ Không viết TC mới — **tách `NEW-59` thành 4 TC** (§4-8) rồi chạy lại. Đẻ TC mới không giải quyết được nguyên nhân (fixture + gộp luồng) |
| G2 | `UserController` open-mobile — `NEW-26` skip ×2 | ❌ Không viết TC mới — cần **dựng fixture action chứa đủ 3 URL** (§4-9); TC đã đủ chi tiết, vấn đề là env |
| G3 | Nhánh `catch` (6 hàm) — `NEW-52` skip ×2 | ❌ Chưa viết được TC — **chờ Dev trả lời §6-6** (điều kiện nào làm hàm ném lỗi). Cách duy nhất env hiện có (gỡ bảng QR action) làm `getTemplate` chết trước, không chạm được nhánh cần test |
| G4 | URL Analytics đếm click — `NEW-2` error | ❌ Không viết TC mới — `NEW-2` **đã có** bước đo click; sửa tiền đề checkbox (§4-4) rồi chạy lại |
| G5 | Sửa nội dung trước khi gửi | ✅ `TC-REGSHARED001-14` |
| G6 | URL có setting action | ✅ `TC-REGURL001-01` |
| G7 | 4 domain nội bộ + so khớp chuỗi con | ✅ `TC-ENV003-04` · `TC-ENV003-05` |
| G8 | Dữ liệu / link đời cũ — `NEW-30` skip | ⚠️ Dùng lại kho `TC-TMT-163` · `TC-TMT-164`. TC mới đã bị **Leader loại** vòng 1 → không đề xuất lại; vẫn cần **chuẩn bị dữ liệu link đời cũ** như tiền đề bắt buộc |
| G9 | 3 nhánh `getTemplate` — `NEW-6` tuỳ nghi | ❌ Không viết TC mới — **tách nhánh `template_url_redirect`** khỏi `NEW-6` (§4-17) |
| G10 | Action Schedule | ❌ Không viết TC mới — nằm trong phần tách `NEW-59` (§4-8) |
| Q1 | `REG-URL-001` | ✅ `TC-REGURL001-01` + dùng lại kho `TC-TMT-136` · `-137` · `-139` |
| Q2 | `MSG-USER-001` | ❌ Không viết TC mới — **sửa expected `NEW-63`/`NEW-64`** theo §6-1 rồi chạy lại (§4-1) |
| Q3 | `INTG-LINE-001` | ❌ Trùng G3 — chờ §6-6 |
| Q4 | `DATA-COUNT-001` | ⚠️ Chỉ còn vế "link ngoài vẫn đếm đúng" trong `NEW-2` (chờ chạy lại) + `TC-REGURL001-01`. Vế **đo mức mất số liệu** đã bị Leader loại vòng 1 |
| Q5 | `ENV-003` / RULE-08 | ✅ `TC-ENV003-04` · `TC-ENV003-05` (cả hai `product`) |
| Q6 | `COMPAT-LEGACY-001` | ⚠️ Dùng lại kho `TC-TMT-163` · `-164` (TC mới đã bị Leader loại vòng 1) |
| Q7 | `JOB-001` | ❌ Không viết TC mới — `NEW-16` đã đúng phạm vi, cần **env có job + chốt §6-3** rồi chạy lại |
| Q8 | `FUNC-003` — URL biên | ✅ `TC-FUNC003-01` |
| Q9 | `REG-SHARED-001` RULE-01 (thiếu Boundary) | ✅ `TC-FUNC003-01` (Boundary) + `TC-REGSHARED001-14` (Normal) |
| Q10 | `OUT-TRUTH-001` RULE-01 | ✅ `TC-FUNC003-01` phủ chiều Boundary; Normal/Abnormal đã có `NEW-2/17/48/50` |
| Q11 | `MSG-004` | ⛔ **TRỐNG** — `TC-MSG004-02`/`-03` bị Leader loại 2026-09-09. Rủi ro *link đầy đủ làm tin dài ra → chạm giới hạn ký tự LINE* hiện **không có TC nào**; `[MAJOR]` ở §2 giữ nguyên chưa xử lý |
| Q12 | `DATA-CACHE-001` | ⚠️ `TC-DATACACHE001-01` bị Leader loại 2026-09-09 → dùng lại kho `TC-CHT-222` · `TC-CHT-225` (cache 30 giây nguồn tin chat 1:1) |
| Q13 | `LIFF-ENTRY-001` | ❌ Không viết TC mới — **bổ sung bước mở link** cho `[FORM_x]`/`[CONVERSION_x]`/`[ITEM_x]` vào `NEW-6` thay vì đẻ TC mới (tránh trùng) |

**RULE-01 — quan điểm ưu tiên Cao thiếu loại case, ghi lý do:**

| Quan điểm | Thiếu | Lý do |
|---|---|---|
| `ENV-003` | Boundary | Biên của môi trường là **có/không khai báo `BASE_URL`** và **có/không custom domain** — đã nằm trong tiền đề của `TC-ENV003-04` và `NEW-16`, không tách TC riêng |
| `REG-URL-001` | Normal | Nhánh Normal (URL **không** setting action → theo đúng checkbox) đã có ở kho `TC-TMT-136`/`-137`/`-139`, dùng lại thay vì viết mới |
| `MSG-004` · `DATA-CACHE-001` | Toàn bộ | ⚠️ **Không phải lý do kỹ thuật** — TC bị Leader loại ngày 2026-09-09 |

---

## 6. Spec update needed

| # | Điểm cần chốt | Hiện trạng | Ai chốt |
|---|---|---|---|
| **1** | 🆕 **Hội thoại nhóm / `line_user.type = 1`: để mã thô lọt tới người dùng cuối có chấp nhận được không?** | Dev **reject** bug #1048 + #1021 với lý do *"Group sẽ không shorten + ko gen code do ko xác định được friend (do có nhiều friend trong 1 group)"*. Bằng chứng run #1402: tin trên LINE group và bong bóng chat đều là `紹介:[LANDING_INTRO_WZnzuU] 資料:https://example.com/...` → **khách nhìn thấy nguyên chuỗi mã**. Reject reason mới giải thích **vì sao không gen được link**, **chưa nói** hiển thị mã thô là hành vi mong muốn. Spec `chat-11` không có business rule nào cho nhánh group. 3 lựa chọn: (a) giữ mã thô, (b) **bỏ mã** khỏi tin gửi nhóm, (c) dựng link không kèm `u_code` | **Dev + PM** — chốt rồi mới `testcase_update` expected `NEW-63`/`NEW-64` (§4-1) và bổ sung rule vào spec `chat-11` |
| **2** | 🆕 **REQ-017 — cờ rút gọn cấp bot có override cờ cấp mẫu tin không?** | `NEW-62` để ngỏ (*"không kết luận pass hay fail"*) nhưng đã bị chấm **`pass`**; bug **#979** (*"tắt rút gọn URL ở cấp bot không có tác dụng"*) đang `stale`; Studio `dev_impact` ghi rõ **"Bug 979 CHƯA vá: `getTemplate` vẫn chỉ đọc `template->is_shorten_url`, bỏ qua `bot->is_shorten_url`"**. Spec `message-template/feature-spec.md:621` chỉ định nghĩa cờ **cấp template**, không nói quan hệ với cờ cấp bot | **Dev + PM** — nếu là bug thì tách ticket, **không đóng #40598 là hoàn tất** |
| **3** | 🆕 **Nhãn ô 「URL gốc」 là ô phủ định — ghi rõ vào spec phần mô tả UI** | `feature-spec.md:621` (Field Matrix #9) **có** ghi `Checked=0 (URL gốc), Unchecked=1 (shortened)`, nhưng phần mô tả màn hình (`:307`, `:338`) chỉ gọi là *"checkbox URL gốc"* → người viết TC đọc thành "bật/tắt rút gọn" và làm ngược (§4-4, đã gây 2 lượt `error`). Kho đã đánh dấu MT-08 cho chính vùng này | **Leader** — bổ sung 1 dòng vào mô tả UI của `SCR-TMT-04` |
| **4** | **URL có setting action mà thôi được rút gọn thì action còn chạy không?** (giữ từ vòng 1 — **chưa chốt**) | Kho `TC-TMT-138` ghi rule action-thắng-checkbox; `TC-TMT-158→161` cho thấy action click chạy qua `url_shorten.action`. Sau fix, link dựng từ mã + URL cùng miền **không còn bản ghi rút gọn** (D1/D2) → action click và đếm click có nguy cơ ngừng chạy. Dev **không nêu** rủi ro này trong đánh giá ảnh hưởng. `TC-REGURL001-01` ở §5 dùng để đo, **không** để phán | **Dev + PM** — trước khi release |
| **5** | **Miền của link giới thiệu: miền hệ thống hay miền rút gọn riêng của bot?** (giữ từ vòng 1 — **chưa chốt**) | Spec `qr-landing` `BR-02` nói link QR chuẩn **không** dùng `domain_url_shorten`, nhưng `EP-65` (`logic-spec.md:365`, `api-spec.md:798`) lại ưu tiên `bots.domain_url_shorten`. Web dựng bằng miền hệ thống, job dựng bằng miền riêng của bot; fix **không chạm** phần này. `NEW-16` để ngỏ expected và đang `skip` | **Dev + PM** — chốt rồi viết lại expected `NEW-16` |
| **6** | **`makeLinkLandingPageIntro` (và 5 hàm catch bên `ChatMessages`) ném lỗi trong điều kiện nào?** (giữ từ vòng 1 — **chưa chốt**) | Bản fix thêm `return $message` vào nhánh `catch` ở **6 hàm**; sau khi đảo thứ tự đây là lời gọi **cuối** → guard hỏng là tin gửi đi **rỗng**. `NEW-52` đã thử 2 lần: cách duy nhất env có (tạm gỡ bảng QR action) làm `getTemplate` chết trước với HTTP 500, **không chạm được** nhánh cần test | **Dev** — cho biết điều kiện ném lỗi để viết TC; nếu không ép được từ UI thì ghi nhận là vùng **không test được bằng manual** và yêu cầu unit test |
| **7** | **Phần "preview text khác nhau" của khách đã được fix chưa?** (giữ từ vòng 1 — **đã có tiến triển**) | `NEW-14` nay **pass** trên cả staging và local, gồm bước *"preview/history của message từ richmenu không còn raw `LANDING_INTRO`"* → vế (b) của khách **có dấu hiệu đã đóng**. Nhưng fix **không chạm** `linect-service` (Java), nơi `MessageBuilder.replaceFriendInfo:4081` là chỗ **duy nhất** ghi `mapReplaceContent` → cần Dev giải thích vì sao preview job nay đúng dù không sửa Java | **Dev** — xác nhận cơ chế, tránh kết luận nhầm từ 1 lượt chạy không có evidence (§4-6) |
| **8** | **Danh sách ĐẦY ĐỦ domain nội bộ không được shorten + cách so khớp domain** (giữ từ vòng 1 — **chưa chốt**) | Leader cho biết 4 domain (`step.lme.jp` · `s.lmes.jp` · `sl.lmes.jp` · `form.lmes.jp`), nhưng `framework/catalog-lme.md:313` ghi **`step.lmes.jp`** — lệch 1 chữ ở đúng chỗ so khớp chuỗi; `MAP-LIFF-04` + RULE-09 còn nêu `step3.lmes.jp` (form cũ); guard hiện chỉ so `BASE_URL` (**1** domain) + `domain_url_shorten` của bot; biểu thức dùng `stripos` (so khớp **chuỗi con**). `TC-ENV003-04`/`-05` ở §5 để đo, **không** để phán | **Leader** chốt danh sách chuẩn · **Dev** xác nhận guard phủ được mấy domain |
| **9** | **Giá trị friend info chứa URL có nên bị rút gọn không?** (giữ từ vòng 1 — **chưa chốt**) | Sau khi đảo thứ tự, tên và friend info được ghép **trước** bước rút gọn. `NEW-23` biến thể B nay đã verify *"mở short URL ra query chứa giá trị thật"* và **pass** ✅ — nhưng câu hỏi **phình dữ liệu** (mỗi friend sinh 1 bản ghi rút gọn riêng) vẫn chưa ai trả lời | **Dev** — xác nhận hành vi mong muốn |
| **10** | **Mất số liệu lượt bấm của URL cùng miền hệ thống có chấp nhận được không?** (giữ từ vòng 1 — **chưa chốt**) | Dev tự nêu: khi `BASE_URL` có giá trị (môi trường thật có), **mọi URL trỏ về miền hệ thống thôi được rút gọn** → mất số liệu lượt bấm; hệ thống đã chạy nhiều năm với chốt chặn không hoạt động. Kho `TC-TMT-139` ghi expected *"URL trong hệ thống → giữ nguyên link"* (hành vi mới **đúng** với kho), nhưng hệ quả mất số liệu vẫn là thật | **PM** — xác nhận chấp nhận đánh đổi |

> ✅ **Đã chốt và đã xử lý xong ở vòng 2** (không cần theo dõi tiếp): mục 1 của vòng 1 — *chat 1:1 hiện URL gốc, LINE hiện URL rút gọn*. Expected `NEW-17` và `NEW-18` **đã được sửa đúng** trên Studio và cả hai **pass**. Việc còn lại duy nhất: bổ sung rule này vào spec `message-template` `BR-15` để người viết TC sau không hiểu sai lại.
