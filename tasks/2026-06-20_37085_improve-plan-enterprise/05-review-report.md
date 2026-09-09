# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37085 — Improve plan enterprise` |
| Reviewer (Leader) | `<Leader fill>` |
| Tester được review | `Thanh Phương` (người submit Link TC) |
| Ngày review | `2026-06-20` |
| Version TCs | fetched từ Sheet "Quản lý hợp đồng" Line 242-293 |
| Vòng review | `Round 1` |

> **Note nguồn input**: TCs fetch từ Redmine #37085 Link TCs (không phải `/write-tc` sinh). File 04 ở **format cây phân cấp (merged cells)** của team, không phải 10-cột chuẩn template — review suy luận coverage từ cột Hạng mục/Scenario/Case/Thao tác/Expected.
> **Spec reference**: dùng `templates/LME-SYSTEM-SPEC.md` tổng (không có `02-spec-reference.md` riêng cho task này).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue BLOCKER/MAJOR, cần fix và review lại

**Lý do ngắn gọn**: TC set cover UI rất tốt (owner thấy/thao tác, non-owner bị ẩn/disable + hiển thị LOA → おまとめ割引), NHƯNG **thiếu test enforcement phía server cho các action ghi dữ liệu** (addBotToSlot / botDelete / cancel / change-owner) khi non-owner gửi request trực tiếp bypass UI bị disable — đây chính là lõi của spec "chỉ owner mới thao tác". Disabled button ≠ security control. Thêm 2 MAJOR thủ tục: cả `01` và `03` auto-fill nhưng tester chưa verify; PR link trống nên không verify được shape enforcement thực tế.

---

## 2. Tóm tắt cho member

Bộ TC này khá mạnh: đã tách rõ 3 nhóm (owner / staff-không-quyền / staff-có-quyền), cover đủ 3 yêu cầu spec gồm cả boundary hiển thị số slot (10枠/20枠) và chặn truy cập GET URL bằng thông báo 権限. Điểm cần bổ sung quan trọng nhất: với mỗi **action thay đổi dữ liệu** (add bot vào slot, xóa/hủy kết nối bot, cancel hợp đồng, change owner) phải có TC gửi **request trực tiếp** từ account non-owner (không qua nút đã disable) và verify **server từ chối** (báo lỗi 権限), vì isNotOwnerContractEnterprise() chạy ở backend — nếu chỉ test "nút bị disable" sẽ bỏ lọt lỗ hổng phân quyền. Ngoài ra cần tick xác nhận đã đọc lại Redmine ở file 01 + 03 và xin Dev PR link.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (Row) | # TC | Status |
|---|---|---|---|---|---|
| BUG / Spec#1 — chỉ owner mới thao tác slot chưa kết nối enterprise | Fix | — | 247-266 (owner làm được), 267-284 (non-owner bị chặn) | nhiều | **RISK** — mutating action chỉ test UI disable, thiếu server-side reject |
| Spec#1b — button おまとめ割引の契約を変更する chỉ owner thấy | Fix | — | 251 (owner mở được), 274 (non-owner ẩn) | 2 | OK |
| Spec#2 — ẩn lựa chọn owner (主管理者) màn kết nối LOA | Fix | — | 243 | 1 | **RISK** — note ghi "hiện không có màn tạo mới enterprise" → chưa execute được |
| Spec#3 — tên LOA enterprise => おまとめ割引 + số slot | Fix | — | 250, 273 (10枠/20枠) | 2 | OK |
| F1/F8 — `isNotOwnerContractEnterprise()` (functions.php + detail.js) | Function | Direct | 247-284 | nhiều | **RISK** — chỉ verify nhánh GET + UI; nhánh POST/action chưa verify |
| F2 — `botDelete()` | Function | Direct | 263 (owner xóa), 282 (non-owner disable) | 2 | **RISK** — thiếu non-owner gọi botDelete trực tiếp |
| F3 — `index()` list bot enterprise | Function | Direct | 247, 267, 270, 284 | 4 | OK |
| F4 — `addBotToSlot()` | Function | Direct | 248, 261-262, 288 | 4 | **RISK** — thiếu non-owner POST addBotToSlot trực tiếp |
| F5 — `detailContract()` | Function | Direct | 249, 272, 269, 283 | 4 | OK |
| F6 — `confirmCancelView()` | Function | Direct | 258 (owner cancel), 281 (non-owner disable) | 2 | **RISK** — thiếu non-owner gọi cancel trực tiếp |
| F7 — `detail.css` | Function | Direct | (visual ở 250/272/273) | — | OK |
| F9 — `detail.blade.php` | Function | Direct | 250, 272, 273 | 3 | OK |
| 4.2 Data | Data | — | Dev ghi "Không có" | — | N/A (xem MINOR-2) |
| T1 — access list bot enterprise | Feature | — | 247, 267, 270, 284, 285 | nhiều | OK |
| T2 — detail hợp đồng | Feature | — | 249, 272, 286 | 3 | OK |
| T3 — xóa bot | Feature | — | 263, 282 | 2 | **RISK** (đồng F2) |
| T4 — add bot to slot | Feature | — | 248, 261, 288 (regression std/pro) | 3 | OK |

### ORPHAN TCs

| Row | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| 243-244 | Mua mới hợp đồng enterprise (Check UI / mua success) | Note cột J: "Hiện tại không có màn tạo mới hợp đồng enterprise" → không execute được | Giữ làm spec-note, đánh dấu **Not test / Blocked**, hoặc xác nhận lại với Dev có path tạo mới không |
| 252-259, 275-279 | change main card / subcard / extend / change phương thức bill | Fix #37085 không chạm logic bill — đây là regression của màn detail, ngoài scope permission | Giữ làm **regression** nhưng gắn nhãn rõ, không tính là TC verify fix (xem AP-5) |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (mục 2 dev-impact) | **Validation / Permission check** — "phải là owner mới được thao tác" (thêm `if isNotOwnerContractEnterprise()` deny). Enforcement ở **2 layer**: backend (functions.php, gọi bởi botDelete/addBotToSlot/index/detailContract/confirmCancelView) + frontend (detail.js disable/ẩn button). |
| Trigger space cần cover | Theo entry-point: (1) owner; (2) staff KHÔNG quyền; (3) staff CÓ quyền nhưng không phải owner; (4) **owner của hợp đồng enterprise KHÁC** (cross-contract); × theo **mỗi endpoint mutating**: addBotToSlot, botDelete, confirmCancel, change-owner, tăng/giảm slot, 一括解除 — qua **request trực tiếp** chứ không chỉ qua UI. |
| Số trigger TCs hiện cover | GET/navigation deny: **2/2** endpoint (detail-contract 269/283, list-bot-enterprise 270/284) → OK. **Mutating action server-side reject: 0/6** → chỉ test "nút disable" (frontend). Cross-contract owner: **0**. |
| KH report dạng | **N/A** — đây là Feature spec (không phải bug symptom report; file 01 không có Steps/Expected/Actual). AP-2 không áp dụng. |
| Alternative root causes cần verify | N/A (feature spec, không có root-cause đoán). |
| Anti-patterns dính | **AP-4** (PR link trống → không verify được enforcement là server-side thật hay chỉ frontend), **AP-5** (over-coverage bill ops 252-259/275-279), mảng nhẹ **AP-3** (regression std/pro chỉ happy-path). AP-1/AP-2/AP-6 không dính. |

> Mutating-action server-side enforcement cover **0/6** < tổng → flag **[BLOCKER] FIX-SHAPE** trong §4.1.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / Security — GAP-1**: Spec#1 "chỉ owner mới thao tác" là **permission enforcement phía server** (F1 `isNotOwnerContractEnterprise()` gọi trong addBotToSlot/botDelete/confirmCancelView). TCs hiện chỉ verify **nút bị disable/ẩn** (frontend F8) cho non-owner ở các action ghi dữ liệu (row 280-282: change owner / cancel / hủy kết nối). **Disabled button KHÔNG phải security control** — non-owner có thể gửi request trực tiếp (POST/đổi param, như cách row 269/270/284 đã làm với GET). → Cần TC: non-owner (staff có & không quyền) gửi **request trực tiếp** tới `addBotToSlot`, `botDelete`, action cancel (`confirmCancelView`), change-owner, tăng/giảm slot, 一括解除 → verify **server từ chối** (báo lỗi `この権限は許可されていません。`, không thay đổi data). Map: F1, F2, F4, F6, T3, T4. (Xem TC-NEW-01..04.)

### 4.2 Major (nên fix)

- **[MAJOR] INPUT — 01 chưa verify**: `01-bug-task.md` auto-filled `2026-06-20 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick**. Yêu cầu tester đọc lại Redmine #37085 (description + 3 attachments + Figma design) và tick trước khi review có giá trị.
- **[MAJOR] INPUT — 03 chưa verify**: `03-dev-impact.md` auto-filled `2026-06-20 by /new-task`, checkbox **chưa tick**. F/D/T có thể chưa đủ hoặc mapping sai (đặc biệt 4.1 Dev chưa phân loại Direct/Indirect, 4.3 chưa phân loại risk). Tester verify + tick.
- **[MAJOR] AP-4 — PR link trống**: `Commit / Pull Request = <chưa có>`. Không verify được enforcement thực tế là server-side (đúng spec) hay chỉ frontend disable. Yêu cầu Dev cung cấp PR link branch `feature/Task_Owner_Enterprise_37085` để confirm shape trước khi đóng GAP-1.
- **[MAJOR] GAP-2 — Cross-contract owner**: Permission check `isNotOwnerContractEnterprise()` so user hiện tại với owner của **đúng hợp đồng đó**. TCs chỉ test staff cùng bot (1991). Thiếu case: **owner của enterprise A** truy cập slot/detail/action của **enterprise B** (mình không phải owner) → phải bị từ chối. Map F1, F3, F5. (TC-NEW-05.)
- **[MAJOR] GAP-3 — Spec#2 không execute được**: Row 243 (ẩn lựa chọn owner màn kết nối LOA enterprise) có note "hiện không có màn tạo mới hợp đồng enterprise" → TC không chạy được. Cần Dev/Leader xác nhận đường vào màn kết nối LOA của enterprise (kết nối bot vào slot có đi qua màn này không?) để viết TC verify Spec#2 thật sự, nếu không Spec#2 đang **GAP thực thi**.

### 4.3 Minor (có thể fix sau)

- **[MINOR] MINOR-1 — format file 04**: TCs ở layout cây phân cấp (merged cells), không phải 10-cột chuẩn (thiếu TC ID / Type / Priority rõ ràng). Khó trace & khó `/sync-tc`. Đề nghị khi đưa vào pipeline review chuẩn thì gán TC ID + Type + Priority cho từng dòng leaf.
- **[MINOR] MINOR-2 — Data impact "Không có" cần soát lại**: Fix là permission-only nên Dev ghi 4.2 "Không có" hợp lý, NHƯNG action add/xóa bot-slot vẫn ghi/xóa quan hệ bot↔slot. Regression nên verify sau khi owner thao tác, **data kết nối bot-slot vẫn đúng** (đã có ở 248/263/288 — đủ, chỉ cần ghi nhận rõ).
- **[MINOR] MINOR-3 — mục 3 dev-impact dạng placeholder**: Mục 3 trỏ sang 4.1 (caller đã list ở 4.1) nên AP-6 không dính, nhưng nên điền bảng mục 3 cho rõ caller nào đã sửa thực tế.

### 4.4 Nit (gợi ý)

- **[NIT] AP-5 — over-coverage bill ops**: Row 252-259 / 275-279 (change main card / subcard / extend / phương thức bill) ngoài scope fix permission. Giữ như regression nhưng nên gắn nhãn "Regression - ngoài scope fix" để Leader vòng sau không nhầm là TC verify fix.
- **[NIT] AP-3 — regression std/pro chỉ happy-path**: Row 285-293 test standard/pro ở trạng thái sạch. Cân nhắc thêm 1 case std/pro ở trạng thái edge (slot đầy / bot đã hủy) để chắc fix owner-check không vô tình chặn nhầm non-enterprise.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round tiếp theo. (Title đặt rõ keyword để map impact.)

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Server reject addBotToSlot khi non-owner gửi request trực tiếp | Có hợp đồng enterprise của owner A (bot/slot 1991). Login bằng staff **được cấp quyền** nhưng KHÔNG phải owner | 1. Mở DevTools/Postman, lấy request POST add bot vào slot enterprise. 2. Gửi trực tiếp request (bỏ qua nút đã disable). | Server trả lỗi `この権限は許可されていません。`, **không** kết nối bot vào slot, data không đổi | High | Negative/Security | F1, F4, T4 |
| TC-NEW-02 | Server reject botDelete / hủy kết nối bot khi non-owner gửi request trực tiếp | Như trên, slot enterprise đang có bot kết nối | 1. Lấy request xóa/hủy kết nối bot khỏi slot enterprise. 2. Gửi trực tiếp bằng account non-owner. | Server từ chối (`権限` lỗi), bot **vẫn** kết nối, không bị xóa | High | Negative/Security | F1, F2, T3 |
| TC-NEW-03 | Server reject cancel hợp đồng enterprise khi non-owner gửi request trực tiếp | Hợp đồng enterprise của owner A. Login non-owner (staff có quyền) | 1. Lấy request action cancel (confirmCancelView / submit cancel). 2. Gửi trực tiếp. | Server từ chối, hợp đồng **không** bị cancel | High | Negative/Security | F1, F6 |
| TC-NEW-04 | Server reject change owner / tăng-giảm slot / 一括解除 khi non-owner gửi request trực tiếp | Như trên | Lần lượt gửi trực tiếp request: change owner, tăng slot, giảm slot, 一括解除 bằng non-owner | Mọi request bị server từ chối `権限`, data không đổi | High | Negative/Security | F1, F4 |
| TC-NEW-05 | Cross-contract: owner enterprise A không thao tác được enterprise B | Tồn tại 2 hợp đồng enterprise khác owner (A và B). Login bằng owner A | 1. Owner A mở URL detail-contract / list-bot-enterprise của hợp đồng B (đổi param id). 2. Thử add/xóa bot slot của B. | Bị từ chối truy cập & thao tác hợp đồng B (`権限` lỗi), chỉ thao tác được hợp đồng A của mình | High | Negative/Security | F1, F3, F5 |
| TC-NEW-06 | Verify đường vào màn kết nối LOA enterprise ẩn lựa chọn owner (Spec#2) | Xác nhận với Dev path kết nối bot vào slot enterprise có đi qua màn kết nối LOA | 1. Đi qua flow kết nối bot vào slot enterprise. 2. Quan sát màn kết nối LOA. | Không hiển thị mục lựa chọn owner (主管理者); mặc định owner = account đang đăng nhập | Medium | Positive | Spec#2 |

---

## 6. Spec update needed

- [x] Không cần update spec (task này CHÍNH LÀ spec change — không phát hiện mâu thuẫn với LME-SYSTEM-SPEC tổng).
- Lưu ý cần Dev/PM làm rõ (không phải spec conflict): đường vào **màn kết nối LOA của enterprise** (liên quan Spec#2) — hiện note TC ghi "không có màn tạo mới hợp đồng enterprise". Cần xác nhận flow thực tế để TC Spec#2 execute được.

---

## 7. Checklist đã chạy

- [x] A. Coverage — build matrix, phát hiện RISK ở mutating actions
- [x] B. Chất lượng từng TC — title/expected khá rõ; thiếu TC ID/Type chuẩn (MINOR-1)
- [x] C. Chất lượng bộ TC tổng thể — có phân role owner/staff (tốt); thiếu nhánh negative server-side
- [x] D. Spec alignment — khớp 3 yêu cầu spec, không mâu thuẫn
- [x] E. Hành chính — input auto-fill chưa verify (2 MAJOR), file đúng folder
- [x] F. Base checklist LME
  - [x] **F.1 Checklist web**: **CL1** (account staff được/không quyền) — cover tốt (267-293). **CL11** (CRUD đúng account — WHERE đúng owner/bot) — chính là lõi GAP-1, cần TC server-side. **A.2 Security** (đổi param ID URL của bot khác → từ chối) — cover GET (269/270/284) ✓ nhưng **thiếu cho action ghi** → GAP-1. **CL20** (hủy hợp đồng) — có ở 258/281.
  - [ ] **F.2 Checklist job**: N/A (fix không chạm job/callback/Google sync).
  - [x] **F.3 Các tính năng chung**: **C.1 Bill tiền** chạm gián tiếp qua màn detail hợp đồng (cancel/change card) — TCs có cover regression (252-259) nhưng ngoài scope fix (AP-5). C.2-C.8 không liên quan.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | `<Leader fill>` | |
| Tester | (đã đọc & hiểu feedback) | |
