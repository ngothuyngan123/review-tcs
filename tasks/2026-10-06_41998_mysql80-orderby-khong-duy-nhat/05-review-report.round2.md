# 05 — Review Report (Round 2)

> Review lại sau khi Dev handoff bản v2 (branch đổi `ai_small_41998` → `origin/ai_studio_implement_41998`, commit `c0345c21ba` + `c26bab43bb`) và chạy lại toàn bộ bộ TC. So với [05-review-report.md](05-review-report.md) (round 1) — chỉ ghi phần **thay đổi** + phát hiện mới.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #368 (round 1, `status = tc-ready`, branch **đổi** sang `origin/ai_studio_implement_41998`) |
| Tổng số TC review | **29** (tăng từ 17 gốc → 27 sau round 1 → **29** sau round 2: **+3** TC mới (NEW-27/28/29) **−1** TC bị xoá (NEW-21)) |

⚠️ **`03-dev-impact.md` đã STALE** — file này vẫn là Journal #140373 (bản fix v1, branch `ai_small_41998`). Chiều `diff code` ở §1 dưới đây dùng **Studio `dev_impact`/`spec_delta` mới nhất** (v2), không dùng file 03. Đề nghị `/new-task` fetch lại Redmine hoặc Leader note tay vào file 03 trước khi đóng ticket.

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả round 1 | Kết quả round 2 |
|---|---|---|
| **(a) dev-impact** (file 03 — stale, không đổi) | 14/15 — CHƯA ĐỦ | 14/15 — **CHƯA ĐỦ** (không đổi vì file 03 không refresh) |
| **(b) diff code** (Studio `dev_impact` v2) | 14/15 — CHƯA ĐỦ | **6/8 nhóm vấn đề đã đóng — vẫn CHƯA ĐỦ**, 2 nhóm còn RISK (G1, G4 — xem bảng) |

**Kết luận**: 6/8 GAP·RISK của round 1 đã đóng bằng code fix + TC pass thật · 2 RISK còn mở (G1, G4 — chưa chạy trên MySQL 8 thật) · **1 phát hiện mới ngoài coverage** (SQL injection, §5).

| # | Vùng (round 1) | Trạng thái round 2 | Bằng chứng |
|---|---|---|---|
| G1 | `BUG` — thứ tự dòng hoà trên MySQL 8 thật | **RISK — VẪN MỞ** | `NEW-17`, `NEW-18` (test trên MySQL 8 có `SELECT VERSION()`) vẫn **`skip`**, chưa chạy. Cả 29 TC chỉ chạy `env=local`. **Chưa có bằng chứng thật nào xác nhận fix giải quyết lỗi gốc trên MySQL 8** — đây là tiêu chí nghiệm thu chính của ticket #41998. | `[BLOCKER]` (giữ nguyên) |
| G2 | F2 `ChatController::getFriends` cũ không TC | **✅ ĐÃ ĐÓNG** | `NEW-20` (`TC-FUNC001-02`) pass — xác nhận `/chat-v2` không còn lối vào | — |
| G3 | F9+F10 mobile web `/list-friend`, `/chat-mobile` thiếu tầng bookmark/thời gian | **✅ ĐÃ CHỐT — ngoài phạm vi #41998** | Dev handoff v2 xác nhận rõ: "Mobile web ... bookmark vẫn không lên đầu như trước, hành vi cũ" — tách thành ticket riêng **#42278 / #42279**. `TC-LIST001-01` (NEW-21, TC tôi đề xuất round 1 để bắt gap này) **đã bị xoá khỏi Studio** — hợp lý vì đúng theo quyết định ngoài phạm vi, không còn ý nghĩa test trong #41998 | — (theo dõi ở #42278/#42279, không phải việc của #41998) |
| G4 | Rủi ro hồi quy hiệu năng trên bảng lớn | **RISK — MỞ RỘNG, VẪN CHƯA ĐO THẬT** | v2 đổi khoá phụ `id` sang ASC cho **cả danh sách chat** (không chỉ QR) → `ORDER BY is_bookmark DESC, last_time_message DESC, id ASC` **trộn chiều, không dùng được index** `idx_bot_hide_bookmark_time` → **mỗi lần cuộn phải sort toàn bộ hội thoại của bot**. Dev tự đo 2 số **mâu thuẫn nhau** (~0,35s/trang trong handoff vs ~900ms trong journal 09:30) cho cùng bot 217k hội thoại — xem §5 I-NEW-2. 2 TC mới `NEW-28`, `NEW-29` (đo ngưỡng 4s) đã thêm nhưng **chỉ chạy `env=local`**, chưa có số đo thật trên MySQL 8 | `[BLOCKER]` (nâng từ `[MAJOR]` round 1 — rủi ro hiệu năng giờ ảnh hưởng **toàn bộ màn chat**, không chỉ QR, và số đo của Dev tự mâu thuẫn) |
| G5 | Nhánh `filterTypeFriend` thiếu dữ liệu hoà | **✅ PHẦN LỚN ĐÃ ĐÓNG** | Web: `NEW-23` (`非表示中`). App: `NEW-27` (mới, filter nhãn + từ khoá + ẩn, có dữ liệu hoà, `tc_group=api`) | Còn thiếu `schedule`/`groupChat`/`status` — `[NIT]`, không chặn release |
| G6 | F3 API app thiếu tầng bookmark | **✅ ĐÃ ĐÓNG** | `NEW-25` (`TC-SYNCAPP001-01`) pass | — |
| G7 | F4 QR thiếu khoá chính `time_click` | **✅ ĐÃ ĐÓNG** | `NEW-26` pass | — |
| G8 | 13 TC cũ expect `id DESC` sai chiều | **✅ ĐÃ ĐÓNG** | Tôi đã sửa 13 TC (`NEW-1,2,3,4,5,6,7,9,10,12,13,14,16`) sang `id ASC` ngày 2026-10-07; Dev v2 cũng đổi code sang ASC cùng lúc → **cả 13 TC pass** | — |

---

## 2. Thiếu so với quan điểm test

Không đổi so với round 1 **trừ**:
- `SYNC-APP-001`, `LIST-001` nay có thêm TC đúng mã (`NEW-27` dù vẫn mang mã lạ `SEARCH-001`) — không đổi kết luận Q3 (vẫn cần đổi `viewpoint` trên Studio cho nhóm TC mã lạ, bao gồm cả `NEW-27/28/29` mới — `SEARCH-001`, `PERF-LATENCY-001` x2 — vẫn không có trong `checklist-lme.md`).
- `SEC-002` (Cao, "BẮT BUỘC khi chức năng xử lý credential/token") — phát sinh **Q5 mới**: không TC nào kiểm `line_id` là input độc hại (SQL injection) ở `Mobile\ListFriendController` / `Mobile\ChatMobileController`. Xem §5 — đây là lỗ hổng **tiền tồn tại**, không phải lỗi do #41998 gây ra, nên không bắt buộc có TC trong phạm vi ticket này, nhưng phải mở ticket bảo mật riêng (đã có đề xuất của Dev, chưa thấy số ticket).

**Kết luận**: không đổi số quan điểm GAP coverage; thêm 1 dòng cảnh báo bảo mật ngoài phạm vi.

---

## 3. TC trùng lặp nội dung

Đã rà 3 TC mới (`NEW-27`, `NEW-28`, `NEW-29`) với toàn bộ 29 TC — không phát hiện trùng lặp:
- `NEW-27` (API, filter+hoà) khác `NEW-23` (web, cùng filter) ở tầng kiểm chứng (API vs UI) và khác `NEW-5` (web search) ở nhóm dữ liệu.
- `NEW-28`/`NEW-29` (đo thời gian trên bot 217k hội thoại) khác `NEW-6` (đối chiếu không lặp/sót trên env thật) và `NEW-1` (đúng thứ tự trên local) — mục đích khác (ngưỡng thời gian vs tính đúng).

---

## 4. Mâu thuẫn trong TCs

| # | Loại | Trạng thái round 1 | Trạng thái round 2 |
|---|---|---|---|
| C1 | `CONF-KHO` (broadcast có update `last_time_message` hay không — MT-01) | Mở | **Vẫn mở** — Dev handoff v2 không đề cập; chưa thấy quyết định |
| C2 | `CONF-KHO` (phân trang tab 本日／新着 20 vs 50/100) | Mở | **✅ Đã chốt + sửa kho** 2026-10-07 (`TC-LSN-120`, `TC-LSN-155`) |
| C3 | `CONF-SPEC` (code `id DESC` vs Leader chốt `id ASC`) | `[BLOCKER]` | **✅ ĐÃ ĐÓNG HOÀN TOÀN** — Dev v2 đổi code sang ASC ở toàn bộ 14 vị trí, tôi đã sửa 13 TC cũ, **chạy lại pass 100%** (NEW-1,2,3,4,5,6,7,9,10,12,13,14,16, 8,11, 19,23,24,25,26,27) |
| C4 | `CONF-SPEC` (mobile web thiếu tầng bookmark) | `[BLOCKER]` | **✅ ĐÃ CHỐT — ngoài phạm vi**, tách ticket #42278/#42279 (xem G3 ở §1) |

**Đã rà**: không phát hiện mâu thuẫn mới giữa 3 TC mới và spec/kho.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I-NEW-1 | `[BLOCKER]`* | `Mobile\ListFriendController`, `Mobile\ChatMobileController` | **Phát hiện mới từ Dev khi sửa code**: tham số request `line_id` được nối thẳng vào `orderByRaw` — nguy cơ **SQL injection**. Dev tự ghi nhận, đề xuất "mở ticket riêng", nhưng chưa thấy số ticket được tạo. *Lỗi **tiền tồn tại**, không do #41998 gây ra — không chặn release #41998, nhưng là lỗ hổng bảo mật nghiêm trọng cần xử lý khẩn cấp ở ticket riêng. | Yêu cầu Leader/PM mở ticket bảo mật riêng NGAY, ép kiểu số (`(int)`) hoặc dùng query binding cho `line_id` trước khi raw vào ORDER BY. Không để trôi theo backlog thường. |
| I-NEW-2 | `[MAJOR]` | Dev handoff v1 (09:30) vs v2 (handoff doc) | Dev tự đo **2 số hiệu năng mâu thuẫn** cho cùng bot 217k hội thoại: ~900ms (journal) vs ~0,35s/trang (handoff v2). Dev tự nhận "2 số không khớp nên tester tự đo". | Bắt buộc tester đo lại bằng `NEW-28`/`NEW-29` trên môi trường MySQL 8 thật trước khi chấp nhận mức độ chậm "đã được chấp nhận". |
| I-NEW-3 | `[MAJOR]` | 8 TC pass: `NEW-1,3,13,19,23,24,25,26` | Vẫn còn gắn **bug ticket** (`42280`–`42284`) dù `last_exec = pass`. Đây là bug mở trong giai đoạn code v1 còn DESC (trước khi Dev đổi sang v2 ASC) — nay đã fix nhưng Redmine chưa chắc đã đóng các sub-ticket này. | Leader/Dev xác nhận đóng 5 ticket con `42280`–`42284` trên Redmine (nêu rõ lý do: đã quyết định `id ASC`, code v2 + TC đều khớp, pass). |
| I-NEW-4 | `[MAJOR]` | `NEW-17`, `NEW-18`, `NEW-22` | 3 TC bắt buộc chạy trên MySQL 8 thật vẫn ở trạng thái `skip` — **tiêu chí nghiệm thu chính của #41998 (xác nhận hết lặp/sót trên MySQL 8) chưa có bằng chứng thật**, toàn bộ 29 TC mới chỉ chạy `local`. | Cấp env MySQL 8 có `SELECT VERSION()` xác nhận, chạy 3 TC này trước khi chuyển ticket sang Resolved/Closed. |
| I-NEW-5 | `[MINOR]` | `NEW-27`, `NEW-28`, `NEW-29` | `spec_status` để trống (`null`) — theo quy tắc nên là `Đã hỏi leader` (dòng id ASC) hoặc `Spec không ghi` (ngưỡng hiệu năng 4s là Dev tự đề xuất, spec không ghi) | Set `spec_status` cho 3 TC mới trên Studio |
| I-NEW-6 | `[NIT]` | — | Việc xoá `NEW-21` (test mobile web bookmark) là **hợp lý** theo quyết định G3 ở §1 — ghi nhận lại để Leader xác nhận không cần khôi phục | Không cần hành động nếu Leader đồng ý |

Các issue round 1 không liệt kê lại ở đây (I1–I10 của [05-review-report.md](05-review-report.md)) — I1 (0 TC chạy) **đã hết hiệu lực** (29/29 TC đã chạy, pass 25/29); I2 (RULE-08 local-only) **vẫn còn** (0 TC chạy prd/staging, trùng G1/G4); I4 (RULE-13 mã HTTP) đã có trong expected của `NEW-27` (ghi HTTP 200) — các TC cũ `NEW-1/9/12` round 1 cần verify lại đã bổ sung HTTP 200 chưa (chưa xác nhận, giữ nguyên `[MAJOR]` round 1).

---

## 6. TCs thừa / ngoài phạm vi task

Không có TC thừa mới. `NEW-21` không còn tồn tại (xem G3/I-NEW-6) — không phải do tôi đề nghị xoá, QA/pipeline đã xoá theo quyết định phạm vi.

---

## 7. TCs đề xuất bổ sung (0)

Không đề xuất TC mới trong round này — 2 RISK còn mở (G1, G4) là vấn đề **thực thi** (chạy đúng env/dữ liệu), không phải thiếu TC: `NEW-17`, `NEW-18`, `NEW-22`, `NEW-28`, `NEW-29` đã tồn tại và đúng thiết kế, chỉ cần **chạy trên MySQL 8 thật** trước khi đóng ticket.

---

## 8. Spec update needed

Giữ nguyên 4 dòng của round 1 ([05-review-report.md](05-review-report.md) §8) + cập nhật trạng thái:

| # | Trạng thái round 2 |
|---|---|
| #1 (bổ sung khoá phụ id vào spec) | Vẫn mở — spec chưa sửa, nhưng hướng đã chốt là **ASC**, code v2 đã khớp |
| #2 (MT-01 broadcast update last_time_message) | Vẫn mở |
| #3 (phân trang 50/100 tab 本日／新着) | **✅ Đã sửa kho** 2026-10-07 |
| #4 (mobile web bookmark — PO chốt) | **✅ Đã chốt: ngoài phạm vi #41998**, theo dõi #42278/#42279 |

**Thêm #5 (mới)**: Mở ticket bảo mật riêng cho SQL injection ở `line_id` (`Mobile\ListFriendController`, `Mobile\ChatMobileController`) — xem §5 I-NEW-1. Ai chốt: **PM/Leader — khẩn**.
