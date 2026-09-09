# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #35783 — Add thêm phân quyền Change LOA (SpecImprove) |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<chưa rõ — TC fetch từ Sheet master, chưa có tên member>` |
| Ngày review | 2026-07-07 |
| Version TCs | fetch từ Sheet "Improve 7/10/2024" row 506–517 (read-only) |
| Vòng review | Round 1 |

> **Spec reference**: dùng LME-SYSTEM-SPEC tổng, không có `02-spec-reference.md` riêng cho task này.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — Có issue MAJOR (input chưa verify + thiếu chiều security cho T3 + dev-impact mâu thuẫn/thiếu), cần fix và review lại.

**Lý do ngắn gọn**: Coverage cốt lõi (spec change + owner + staff đã phân quyền) khá tốt, nhưng **T3 (staff chưa phân quyền) thiếu chiều security URL trực tiếp + thực hiện action**, đồng thời **cả 01 và 03 đều auto-fill từ Redmine mà chưa được tester verify** và **dev-impact có mâu thuẫn (mục 2 xóa DB ↔ mục 4.2 "k có" data) + mục 3 caller trống** → chưa đủ tin cậy để approve.

---

## 2. Tóm tắt cho member

Bộ TC bám sát 3 nhóm role rất tốt (owner giữ quyền, staff cũ mất quyền, staff chưa có quyền) và đã cover đa access-vector cho staff đã phân quyền (menu thường / favorite / URL trực tiếp / thực hiện) — đây là điểm mạnh. **Cần bổ sung**: (1) test **URL trực tiếp + thực hiện change bot** cho staff *chưa* phân quyền (T3) để đóng lỗ hổng security, (2) yêu cầu Dev làm rõ mục 4.2 (fix xóa DB nhưng ghi "k có" data) + liệt kê caller ở mục 3, và (3) tester tick 2 checkbox verify auto-fill trước khi review có giá trị pháp lý.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG — Remove mục 「LINE公式アカウント入れ替え」khỏi màn phân quyền | Fix (spec change) | — | TC001, TC002 | 2 | **OK** |
| F1 — "Không sửa function" (theo Dev) | Function | — | (Dev khẳng định không sửa) | 0 | N/A |
| D1 — Xóa bản ghi phân quyền trong DB | Data | — | TC007, TC008, TC009, TC010 (verify hệ quả qua UI) | 4 (gián tiếp) | **RISK** — verify qua hệ quả, chưa có TC check ghost-reference ở màn/tính năng khác + Dev ghi "k có" data (mâu thuẫn) |
| T1 — Owner change bot | Feature | High | TC003, TC004, TC005, TC006 | 4 | **OK** — cover menu thường/favorite/URL/thực hiện |
| T2 — Staff cũ **đã** được phân quyền change bot | Feature | (Dev chưa ghi risk) | TC007, TC008, TC009, TC010 | 4 | **OK** — cover menu/favorite/URL trực tiếp/thực hiện |
| T3 — Staff **chưa** được phân quyền change bot | Feature | (Dev chưa ghi risk) | TC011, TC012 | 2 | **RISK** — chỉ cover menu thường + favorite; **thiếu URL trực tiếp + thực hiện action** (T2 có, T3 không) |

### ORPHAN TCs

| TC ID | Title | Lý do orphan | Hành động đề xuất |
|---|---|---|---|
| — | — | Không có TC lạc chủ đề — cả 12 TC đều map BUG/T1/T2/T3 | — |

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **Permission/authorization data removal** (DELETE bản ghi phân quyền trong DB) — gần nhất bucket "soft-delete/DELETE data" + authorization guard |
| Trigger space cần cover | 3 role state (owner / staff-đã-phân-quyền / staff-chưa-phân-quyền) × access-vector (menu thường / menu favorite / URL trực tiếp / hyperlink / thực hiện action) × auth-state (đã login / chưa login) |
| Số trigger TCs hiện cover | Owner: 4 vector (menu/favorite/URL/action) ✅ · Staff-đã: 4 vector ✅ · Staff-chưa: **2/4** (menu+favorite, **thiếu URL trực tiếp + action**) · Chưa-login: **0** · Hyperlink/param bot khác: **0** |
| KH report dạng | **Có root cause cụ thể** (spec change rõ ràng: remove item, default 主管理者) — KHÔNG symptom-only → AP-2 không áp dụng |
| Alternative root causes cần verify | N/A |
| Anti-patterns dính | **AP-4** (PR/Commit trống — không verify được fix shape từ code) · **AP-6** (mục 3 caller trống) · một phần **AP-3** (T3 regression nông, chỉ happy menu-level) |

> Trigger space cover **< tổng** (staff-chưa-phân-quyền thiếu vector security URL/action; thiếu case chưa-login) → flag [MAJOR] FIX-SHAPE ở §4.2.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- Không có issue **BLOCKER** thuần: spec change cốt lõi (TC001-002) + owner (T1) + staff đã phân quyền (T2) đã được cover đủ chiều. Các gap còn lại ở mức MAJOR.

### 4.2 Major (nên fix)

- **[MAJOR] FIX-SHAPE / GAP-1 (T3 — security)**: Staff **chưa** được phân quyền (TC011-012) chỉ test chặn ở **menu thường + favorite**, KHÔNG test **URL trực tiếp** và **thực hiện change bot** — trong khi staff *đã* phân quyền (TC009-010) lại có. Đây là chiều **security bắt buộc** (checklist LME `CL-NonF-2`: access URL khi staff không được cấp quyền từ menu chính/favourite/**trực tiếp URL**/hyperlink). Lỗ hổng nếu guard URL khác guard menu. → Thêm **TC-NEW-01** (URL trực tiếp) + **TC-NEW-02** (thực hiện action) cho T3.
- **[MAJOR] [AP-6] Mục 3 dev-impact trống**: Dev chỉ ghi heading "Đã check function/data", không liệt kê caller. Quyền LOA入れ替え được kiểm ở nhiều nơi (render menu, middleware guard URL, action change-bot). Không có danh sách caller → rủi ro sót 1 điểm check. → Yêu cầu Dev list các function/middleware đọc phân quyền này.
- **[MAJOR] GAP-2 (D1 mâu thuẫn)**: Mục 2 "Xóa phân quyền trong **database**" nhưng mục 4.2 ghi "**k có**" data update. → Yêu cầu Dev xác định rõ bảng/bản ghi bị xóa (permission/role table) để (a) tester verify D1, (b) rà **ghost-reference**: sau khi xóa item quyền, các màn khác đọc list quyền (màn assign quyền staff, export, ...) có bị lỗi/hiển thị rác không (`CL-Func-17` analog). → Thêm **TC-NEW-03**.
- **[MAJOR] [AP-4] PR/Commit trống**: Mục "Commit / Pull Request" = `<chưa có>` → không đọc được diff để xác nhận fix là DELETE data thật hay ẩn UI. → Yêu cầu Dev cung cấp PR link.
- **[MAJOR] 01-bug-task auto-fill chưa verify**: `01-bug-task.md` có `Auto-filled: 2026-07-07 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** — thêm nữa description gốc ("Add thêm") **mâu thuẫn** với spec cuối ("Xóa quyền"). Tester phải đọc lại Redmine (đặc biệt journal 26/6 của Ngọc Ánh) + tick checkbox trước khi review có giá trị.
- **[MAJOR] 03-dev-impact auto-fill chưa verify**: `03-dev-impact.md` có `Auto-filled: 2026-07-07 by /new-task` nhưng checkbox "Tester verify auto-fill chính xác" **chưa tick** — F/D/T có thể chưa đầy đủ (đặc biệt D1). Yêu cầu tester đọc lại Redmine + tick trước khi chốt coverage.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Security chưa-login (`CL-NonF-5`)**: Chưa có TC gõ URL change-bot khi **chưa đăng nhập** → phải redirect login. → **TC-NEW-04**.
- **[MINOR] Member self-check trống**: Section "Member tự check" + "Base checklist LME" trong `04-tc-list.md` để placeholder (do TC fetch từ Sheet master, không phải member viết qua `/write-tc`). Không ảnh hưởng coverage nhưng Leader nên xác nhận ai chịu trách nhiệm bộ TC này.
- **[MINOR] Domain env TC**: URL trong TC là `booking.watermeru.com` — verify đúng môi trường test (Staging `staging.lme.jp`?) trước khi run.

### 4.4 Nit (gợi ý)

- **[NIT] T1 full E2E**: TC006 "thực hiện change bot" expected chỉ ghi "success" chung. Với tính năng High-risk (đổi LOA), nên có TC E2E verify bot **thực sự** được thay (cả `immediate` lẫn `scheduled`). → **TC-NEW-05** (optional).
- **[NIT] Staff mới tạo**: T3 hiện chỉ test "staff cũ chưa phân quyền". Có thể thêm case **staff mới tạo hoàn toàn** để chắc chắn cùng bị chặn. → **TC-NEW-06** (optional).
- **[NIT] `CL-NonF-4` param bot khác**: Chưa có TC đổi `bot_hash` trong URL sang bot của account khác → verify từ chối access.

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` ở round tiếp theo. (TC read-only fetch từ Sheet — nếu bổ sung, ghi rõ là TC do reviewer đề xuất, confirm Leader trước khi push.)

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Staff CHƯA phân quyền — access URL trực tiếp change bot bị từ chối | Login account staff **không** được phân quyền change bot | Paste trực tiếp vào trình duyệt lần lượt 4 URL: `.../admin/change-bots-new/{bot_hash}`; `.../admin/change-bot-sub/{bot_hash}?type_change=immediate`; `.../admin/change-bots-new/{bot_hash}?type=change_sub&change_success=1`; `.../admin/change-bot-sub/{bot_hash}?type_change=scheduled` | Redirect về màn `admin/home` + hiển thị message `この権限は許可されていません。` (giống TC009 của staff đã phân quyền) | High | Negative / Security | T3, `CL-NonF-2/4` |
| TC-NEW-02 | Staff CHƯA phân quyền — không thực hiện được change bot | Login staff không phân quyền | Cố gắng thực hiện thao tác change bot (qua mọi đường tới được màn) | Không access được màn hình nên cũng không thực hiện được change bot (giống TC010) | High | Negative | T3 |
| TC-NEW-03 | Màn setting phân quyền không lỗi sau khi remove mục LOA入れ替え (ghost-reference) | Login owner 主管理者, mở màn assign quyền cho staff | 1) Mở màn setting/assign phân quyền staff → xem list các mục quyền còn lại. 2) Tick/save 1 staff với vài quyền bất kỳ. 3) Mở lại detail staff đó. | Không còn mục 「LINE公式アカウント入れ替え」; các mục quyền khác vẫn hiển thị & save/load bình thường, không lỗi layout/exception | High | Regression | D1, BUG |
| TC-NEW-04 | Gõ URL change bot khi CHƯA đăng nhập → redirect login | Đã logout | Paste 1 trong các URL change-bot vào trình duyệt | Redirect sang màn login | Medium | Security | `CL-NonF-5` |
| TC-NEW-05 | (Optional) Owner thực hiện LOA入れ替え end-to-end thành công | Login owner 主管理者, có bot hợp lệ để đổi | Vào change bot → thực hiện LOA入れ替え cả `immediate` và `scheduled` → kiểm tra kết quả | LOA入れ替え thành công cả 2 loại; bot thực sự được thay (verify ở màn overview/detail) | Medium | Positive (E2E) | T1 |
| TC-NEW-06 | (Optional) Staff MỚI TẠO cũng bị chặn change bot | Tạo staff mới hoàn toàn (chưa từng có quyền) | Login staff mới → mở menu / paste URL change-bot | Không thấy quyền / bị chặn giống staff chưa phân quyền (menu disable + URL redirect + msg no permission) | Low | Negative | T3 |

---

## 6. Spec update needed

- [ ] Không cần update spec
- [x] **Cần làm rõ spec** — chi tiết:
  - **Section**: Redmine #35783 description ↔ journal 26/6.
  - **Nội dung**: Description gốc ghi "**Add thêm** phân quyền LINE公式アカウント入れ替え" nhưng journal 26/6 (Ngọc Ánh) + đánh giá Dev cho thấy spec cuối là "**Xóa** quyền — chỉ 主管理者 mới đổi LOA". Đề nghị PM cập nhật lại subject/description ticket cho khớp implementation để tránh hiểu nhầm khi maintain sau này.
  - **Người chịu trách nhiệm**: PM (Ngọc Ánh) xác nhận + Dev (Thanh Phương) đồng bộ.

---

## 7. Checklist đã chạy

- [x] A. Coverage — có RISK (D1, T3), không GAP tuyệt đối
- [x] B. Chất lượng từng TC — TC rõ ràng, atomic (mỗi row 1 vector); Precondition dùng phân cấp hợp lý
- [x] C. Chất lượng bộ TC tổng thể — cân bằng role/permission tốt; thiếu chiều security cho 1 role (T3)
- [x] D. Spec alignment — có mâu thuẫn description ↔ spec cuối (xem §6)
- [x] E. Hành chính — TC ID chuẩn; version/tester chưa điền (TC fetch từ Sheet)
- [x] F. Base checklist LME
  - [x] F.1 Checklist web — **`CL-Func-1`** (test account staff phân quyền/không phân quyền) ✅ liên quan trực tiếp, cover phần lớn; **`CL-NonF-2/4/5`** (security URL) ⚠️ thiếu chiều cho T3 + chưa-login → xem §4.2/§4.3
  - [x] F.2 Checklist job — N/A (task không chạm job)
  - [x] F.3 Các tính năng chung — N/A (không chạm bill/send/friend/tag/sheet); chỉ liên quan phân quyền staff

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |

---

<!-- Draft do /review-tc sinh 2026-07-07 — Leader verify trước khi gửi member. Coverage suy luận từ Title/Precondition/Steps/Expected (file 04 không có cột Map to Impact). -->
