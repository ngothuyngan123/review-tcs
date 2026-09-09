# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37743 — User đã login và select bot ngày hôm sau user vào đang không lưu lịch sử access` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa điền trong file 04>` |
| Ngày review | `2026-06-17` |
| Version TCs | `v1` |
| Vòng review | `Round 1` |

> **Spec reference**: KHÔNG có `02-spec-reference.md` cho task này → dùng `templates/LME-SYSTEM-SPEC.md` tổng. Lưu ý: nhiều TC trong file 04 tham chiếu business rule (BR-004, BR-012, BR-013, EP-12) + checklist (CL1/CL5/CL11/CL27) **không có trong input** → reviewer KHÔNG verify được expected của các TC đó đúng/sai so với spec. Đề nghị member đính kèm spec nguồn (file 02).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED**

**Lý do ngắn gọn**: Bộ TC mức độ chi tiết tốt và coverage rộng (dedup / race / impersonation / permission / regression), nhưng (1) **bỏ lọt failure-mode của fix trong global middleware** — không có TC verify "ghi history lỗi KHÔNG được chặn access trang" (BLOCKER); (2) input chưa được tester verify (2× MAJOR) + mâu thuẫn data impact (4.2 ghi "k có" trong khi fix là *lưu lịch sử*); (3) 4 TC có expected bỏ ngỏ "⏳ Pending QA". Cần fix + review lại Round 2.

---

## 2. Tóm tắt cho member

Bộ TC viết rất kỹ — bao quát được dedup theo ngày, race condition multi-tab, ranh giới nửa đêm, impersonation, phân quyền và regression `setBotInvite`; coverage cho bug root cause + middleware đầy đủ. Điểm cần fix lớn nhất: fix nằm trong **middleware chạy cho MỌI request authenticated**, nên phải có TC chứng minh "khi ghi history thất bại thì user vẫn vào được trang" (không thì lỗi logging làm sập toàn bộ truy cập) — đây là rủi ro production cao nhất hiện chưa cover. Ngoài ra cần đối chiếu lại file 03 với Dev (mục 4.2 ghi "không có data" nhưng cách fix là tạo bản ghi lịch sử) và đóng 4 câu hỏi "Pending QA" trước khi execute.

---

## 3. Coverage Matrix

> File 04 không có cột "Map to Impact" — mapping dưới đây là **suy luận** từ Title/Precondition/Steps/Expected.

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG — chưa lưu lịch sử access khi đã select bot trước đó | Fix | — | TC-AH-001, 003, 005 | 3 | **OK** |
| F1 — `BasicAccess.php` (middleware check login) | Function | Direct | TC-AH-001, 002, 003, 004, 005, 006, 012, 013, 014, 015, 016, 017 | 12 | **OK** (đủ positive + negative + boundary) |
| D1 — bản ghi access-history (Dev khai "k có" — thực tế là CREATE) | Data | — | TC-AH-001, 002, 004, 007, 008, 009, 011 | 7 | **OK trên TC** / ⚠️ **mâu thuẫn input** (xem §4.2) |
| T1 — Access các màn sau khi select bot (regression) | Feature | (Dev chưa ghi risk) | TC-AH-005, 010, 019, 020 | 4 | **RISK** — thiếu failure-mode + performance của middleware (xem §3.5, §4.1) |

**Coverage ngoài scope file 03 (TC tốt nhưng input không document — nên bổ sung vào file 03):**

| Khía cạnh test có trong TC | TCs | Ghi chú |
|---|---|---|
| Impersonation không ghi history (BR-013) | TC-AH-012, 013 | Không có trong file 03 → Dev cần confirm rule này tồn tại |
| Phân quyền màn アクセス履歴 (BR-004) | TC-AH-014 | Màn hình MỚI → cần thêm security checklist (xem §4.2) |
| Snapshot tên + ngoại lệ admin (EP-12) | TC-AH-008 | Expected dựa trên rule không có trong input |

### ORPHAN TCs

Không có TC orphan — toàn bộ 20 TC đều map về BUG / F1 / D1 / T1 hoặc một mục checklist LME (CL1, CL5/CL27, CL11). Một số TC test sâu hơn phạm vi file 03 (impersonation, snapshot name) nhưng **liên quan trực tiếp feature**, không phải lạc chủ đề.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Add check + Daily-dedup write trong global middleware** (lai giữa "validate/add check" + "race-condition" + tạo bản ghi mới) |
| Trigger space cần cover | (a) access lần đầu/ngày → ghi; (b) access lần 2+ → không ghi; (c) sang ngày mới → ghi; (d) đa bot; (e) **2 request đồng thời lần đầu** (race); (f) ranh giới ngày 23:59/00:01; (g) impersonation không ghi; (h) **ghi history THẤT BẠI → access KHÔNG bị chặn** ← *thiếu*; (i) **performance: middleware thêm query mỗi request** ← *thiếu* |
| Số trigger TCs hiện cover | 7/9 (thiếu **failure-mode** và **performance** của middleware) |
| KH report dạng | **Symptom + root cause do Dev cung cấp** (file 01 description rỗng; root cause lấy từ journal Dev). Không phải symptom-only thuần, nhưng KH report cực mỏng, không có log/error cụ thể |
| Alternative root causes cần verify | Bug mô tả "không lưu lịch sử access" — root cause Dev đưa = "chưa lưu khi đã select bot từ trước". Plausible alternative: ghi nhưng sai `bot_id`/`user_staff_bot_id` (ghi nhầm bot khác) → đã được TC-AH-009 cover một phần. N/A thêm |
| Anti-patterns dính | **AP-6** (mục 3 caller trống), **AP-4** (PR link trống — không verify được fix shape thực tế từ code) |

> ⚠️ Fix nằm trong `BasicAccess.php` — middleware **chạy cho mọi request authenticated**. Đây là điểm khuếch đại rủi ro: một lỗi nhỏ trong nhánh ghi history có thể chặn truy cập TẤT CẢ màn. Trigger space (h) là **BLOCKER** vì thiếu nó = bỏ lọt bug nghiêm trọng nhất. → xem §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-1 — Failure-mode của middleware**: Fix ghi history **đồng bộ trong `BasicAccess.php`** (chạy mọi request authenticated). KHÔNG có TC nào verify trường hợp **ghi history thất bại** (DB lỗi/timeout/unique-constraint violation khi race) → user vẫn phải vào được trang bình thường. Nếu fix không bọc try-catch, một lỗi logging sẽ chặn truy cập toàn hệ thống. → **Bổ sung TC-NEW-01** (graceful degradation). Đồng thời yêu cầu Dev xác nhận nhánh ghi history có nuốt lỗi (không throw) hay không.

### 4.2 Major (nên fix)

- **[MAJOR] INPUT — `01-bug-task.md` auto-filled chưa verify**: File auto-filled `2026-06-17 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" CHƯA tick, và description Redmine **rỗng** (không có steps/expected/actual). Yêu cầu tester đọc lại Redmine #37743 + journal, bổ sung repro/expected và tick checkbox — nếu không, review chỉ dựa trên đánh giá Dev rất mỏng.
- **[MAJOR] INPUT — `03-dev-impact.md` auto-filled chưa verify**: Checkbox "Tester verify" CHƯA tick. F/D/T có thể chưa đủ.
- **[MAJOR] INPUT — Mâu thuẫn data impact (D1)**: Mục 4.2 ghi **"k có"** data update, trong khi cách fix (mục 2) là **lưu bản ghi lịch sử access**. Đây là một thao tác **CREATE** trên bảng access-history (TC gọi là `user_access_bot`). Yêu cầu Dev sửa 4.2 → khai rõ bảng + thao tác CREATE, để coverage data được verify đúng. (TC hiện đã cover D1, nhưng input sai khiến không trace được.)
- **[MAJOR][AP-6] — Mục 3 (caller) trống**: Dev chỉ ghi "Đã check function/data", không liệt kê caller cụ thể. Vì fix ở middleware dùng chung, cần biết những flow nào đi qua nhánh mới. Yêu cầu Dev list caller/flow bị ảnh hưởng.
- **[MAJOR][AP-4] — PR link trống**: Mục "Commit / Pull Request" chỉ có tên branch `bugs/fix_bug_save_access_bot_16062026`, không có link PR. Không verify được fix là check-then-insert (có race) hay có unique-constraint/transaction. Yêu cầu Dev cung cấp PR để verify fix shape thực tế (ảnh hưởng trực tiếp validity của TC-AH-015/016).
- **[MAJOR] SECURITY / GAP-2 — Màn hình MỚI `アクセス履歴` thiếu security test (checklist-lme A.2)**: TC-AH-014 mới cover staff không quyền. Thiếu: (a) gõ URL khi **chưa đăng nhập** → redirect login; (b) đổi `bot_id` param sang **bot/tenant khác** → từ chối (IDOR cross-tenant access history). → **Bổ sung TC-NEW-02**.
- **[MAJOR] PERFORMANCE / GAP-3 — Middleware thêm query mỗi request**: Logic "check trong ngày access lần đầu" = thêm tối thiểu 1 SELECT trên **mọi** request authenticated. Không có TC verify chỉ phát sinh 1 query (không N+1) và không làm chậm rõ rệt mọi trang. → **Bổ sung TC-NEW-03**.
- **[MAJOR] EXPECTED bỏ ngỏ — 4 TC "⏳ Pending QA"**: TC-AH-010 (Q2: có update `最終ログイン` không), TC-AH-017 (Q3: timezone ranh giới ngày), TC-AH-018 (Q4: no-bot-context có ghi không), TC-AH-020 (Q1: setBotInvite có tính vào dedup-ngày không) — expected hiện là "giả định...". Theo checklist B.1, expected phải đo lường được. Yêu cầu BA/Dev đóng 4 câu hỏi này, chốt expected trước khi execute.

### 4.3 Minor (có thể fix sau)

- **[MINOR] TC-AH-008**: Trộn 2 expected khác nhau trong 1 TC (snapshot name giữ nguyên + ngoại lệ admin hiển thị tên thật EP-12) → không atomic. Nên tách case admin thành TC riêng.
- **[MINOR] File 04 — thông tin tester trống**: "Tester viết TCs" / "Ngày submit" / "Member tự check" để `<member điền>`. Yêu cầu member điền trước khi submit chính thức.
- **[MINOR] Type "Edge Case"**: Sheet gốc dùng `Edge Case` thay vì `Boundary` của template chuẩn — chấp nhận được, chỉ note để thống nhất.

### 4.4 Nit (gợi ý)

- **[NIT]** Cân nhắc thêm TC i18n cho màn lịch sử (hiển thị JP) và compatibility Win/Mac (checklist A.2) nếu màn là UI admin web mới.
- **[NIT]** TC-AH-007 verify IPv6 — nên thêm 1 case dữ liệu IPv6 thực tế (vd `2001:db8::1`) trong precondition để rõ.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo.

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Ghi history thất bại KHÔNG chặn truy cập trang (graceful degradation middleware) | User đã có bot context bot X, hôm nay chưa access. Mô phỏng được lỗi ghi history (vd DB access-history tạm không ghi được / unique-constraint conflict khi race). | 1. Gây điều kiện ghi history lỗi (nhờ Dev cung cấp cách mock, hoặc tạo race insert trùng key)<br>2. User access 1 trang authenticated của bot X | - Trang vẫn load bình thường, user KHÔNG bị chặn / không thấy lỗi 500<br>- Lỗi ghi history được nuốt (log lại phía server), không ném ra request<br>- Không có record rác/half-written | High | Negative | BUG, F1, T1 |
| TC-NEW-02 | Security màn アクセス履歴 — chưa login redirect + IDOR cross-bot | Có URL màn access-history `/admin/access-histories?bot_id=X`. Có bot Y thuộc account/tenant khác. | 1. Gõ URL khi CHƯA đăng nhập<br>2. Đăng nhập user của bot X, đổi param `bot_id` sang bot Y (không có quyền)<br>3. Quan sát kết quả | - Bước 1: redirect về màn login<br>- Bước 2: từ chối access (redirect/thông báo không có quyền), KHÔNG xem được history của bot Y<br>- Không lộ dữ liệu bot/tenant khác | High | Negative | F1, T1, checklist A.2 Security |
| TC-NEW-03 | Performance — middleware chỉ thêm 1 query/ request, không N+1 | User đã có record hôm nay (đã qua lần ghi đầu). Bật query log / debug bar. | 1. Access liên tiếp nhiều trang authenticated trong ngày (sau khi đã có record)<br>2. Quan sát số query phát sinh do logic access-history trên mỗi request | - Mỗi request chỉ thêm tối đa 1 SELECT dedup (không INSERT lại, không N+1)<br>- Thời gian load không tăng đáng kể so với trước fix | Medium | Boundary | F1, T1 |
| TC-NEW-04 (tùy chọn) | Snapshot tên — ngoại lệ Admin hiển thị tên thật (tách từ TC-AH-008) | Record access hôm nay của một user **là Admin** (is_admin=1), tên cũ '田中太郎'. | 1. Sau khi ghi record, admin đổi tên thành '田中花子'<br>2. Vào màn アクセス履歴 xem dòng record cũ | - Với admin: màn hiển thị **tên thật hiện tại** '田中花子' (theo EP-12), khác hành vi snapshot của staff thường | Medium | Edge Case | D1 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] Cần làm rõ spec / business rule — chi tiết:
  - **Section**: Access history (アクセス履歴) — chưa có spec riêng (`02-spec-reference.md` thiếu).
  - **Nội dung cần làm rõ**: 4 câu hỏi Pending QA (Q1 dedup setBotInvite, Q2 update `最終ログイン`, Q3 timezone ranh giới ngày, Q4 no-bot-context); xác nhận tồn tại các rule BR-004 / BR-012 / BR-013 / EP-12 mà TC đang dựa vào; chốt bảng + cột của access-history (tên bảng, `bot_id`, `user_staff_bot_id`, `staff_name`, datetime, IP).
  - **Người chịu trách nhiệm**: BA + Dev (Ngô Thúy Ngần / Do Van Tu) — confirm trước khi member execute.

---

## 7. Checklist đã chạy

- [x] A. Coverage — BUG/F1/D1/T1 đều có TC; phát hiện 3 GAP (failure-mode, security, performance)
- [x] B. Chất lượng từng TC — phát hiện expected bỏ ngỏ (Pending QA) + 1 TC không atomic
- [x] C. Chất lượng bộ TC tổng thể — phân bổ lệch về Edge Case, ít Negative (chấp nhận); có test role/permission
- [x] D. Spec alignment — thiếu file 02; TC dựa rule ngoài input → đã note §6
- [x] E. Hành chính — thiếu tên tester / version member
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — CL1 (staff, TC-AH-006/014 ✓), CL5/CL27 (race/double, TC-AH-015/016 ✓), CL11 (CRUD đúng bot, TC-AH-009 ✓); **A.2 Security cho màn mới — THIẾU** (§4.2 GAP-2); CL15 phân trang màn history & Compatibility Win/Mac — chưa cover (NIT)
  - [x] F.2 Checklist job — không chạm job/sync Google → N/A
  - [x] F.3 Các tính năng chung — task không chạm Bill/Send message/Friend info/Tag/Google sheet/Plan limit/Sort → N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
