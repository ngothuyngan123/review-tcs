# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | #38761 — [Popup] Chức năng 「ポップアップ」 bị ảnh hưởng chính sách Google hạ đánh giá popup nút Back |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | human (TC01–TC22) + AI review (RV-01…RV-06) |
| Ngày review | 2026-07-21 |
| Version TCs | fetched read-only từ Sheet "Popup" row 112–139 |
| Vòng review | Round 1 (draft cho Leader) |

> **Spec reference**: dùng LME-SYSTEM-SPEC tổng (FA-018 Popup nhúng), không có file `02-spec-reference.md` riêng cho task này.
> **Nguồn file 04**: `/new-task` fetch từ Redmine Link TCs (sheet human/master), **KHÔNG** phải format 16 cột canonical — sheet dạng checklist phân cấp (Main Function/Sub1-4/Expect Result). Map quan điểm ở đây phải **suy luận** từ Tiêu đề/Steps/Expected (file 04 không có cột `Mã quan điểm liên kết`).

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — có 1 [BLOCKER] (asset-cache) + vài [MAJOR] cần đóng trước khi nghiệm thu.

**Lý do ngắn gọn**: Bộ TC phủ hành vi rất tốt (3 kiểu popup, close_page mobile/desktop, calendar salon, note, coexist, legacy, leak, edit-mode). Nhưng fix **sửa 2 file JS tĩnh** (`default_setting.js` chạy trên **website khách bên ngoài**, `calendar_salon/index.js`) mà **không có TC nào cover DEPLOY-ASSET-001 / cache** — đúng điểm rủi ro cao nhất: browser/site khách còn cache JS cũ vẫn giữ hành vi bẫy nút Back mà Google phạt. Cộng thêm hành vi mobile thật (surface khách cuối) đang để "Không test".

---

## 2. Tóm tắt cho member

Bộ TC rất chắc về mặt **hành vi & logic** — đặc biệt các RV-01…RV-06 bổ sung đối chứng âm (after_open_page, màn lịch khác, note coexist, legacy data, leak note JP, edit-mode gating) rất tốt, đúng tinh thần RULE-06/RULE-09. Điểm phải bổ sung: (1) fix bản chất là **sửa JS tĩnh** nên **bắt buộc** có TC nghiệm thu **cache/asset version bằng F5 thường** (DEPLOY-ASSET-001) — nhất là `default_setting.js` nhúng trên site khách; (2) đưa 1 lượt verify **thật trên iOS Safari + Android Chrome** (hiện đang "Không test") vì đó chính là output cuối cho khách (RULE-06/ENV-003). Ngoài ra 2 file input auto-fill từ Redmine **chưa được tester tick verify**.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map (suy luận) | # TC | Status |
|---|---|---|---|---|---|
| BUG — bỏ `pushState`+`popstate` ở `close_page`, không bẫy nút Back | Fix | — | TC05, RV-01, TC01 (note) | 3 | **RISK** — hành vi mobile thật để "Không test" (RULE-06) |
| F1 — `default_setting.js` `close_page` (bỏ pushState+popstate; bỏ pushState dư `popupInsertAdjacentHTML`) | Function | Direct | TC05, TC06, TC07, TC08, TC11, RV-01 | 6 | **RISK** — thiếu chiều asset-cache (DEPLOY-ASSET) |
| F2 — `calendar_salon/index.js` (bỏ khối pushState+popstate cuối file) | Function | Direct | TC14, TC15, TC16, TC17, RV-02 | 5 | **RISK** — TC15/16/17 "Không test" (cần màn live), asset-cache thiếu |
| F3 — Blade màn thiết lập Popup: note chú thích (`text__msg__blockview`, flex-column) | Function | Direct | TC01, TC02, TC03, TC04, TC18, RV-03, RV-05, RV-06 | 8 | **OK** |
| D — (không có data update) | Data | — | — | 0 | N/A (fix thuần view) |
| T1 — Popup `close_page` (mobile mất exit-intent; desktop giữ visibilitychange/blur) | Feature | High | TC05, TC06, TC07, TC08, RV-01 | 5 | **RISK** — real-device deferred |
| T2 — Popup `after_open_page` / `location` (không đổi) | Feature | Low | TC02, TC03, TC09, TC10, RV-01 (đối chứng âm) | 5 | **OK** |
| T3 — Lịch Salon (không còn chặn Back) | Feature | Medium | TC14, TC15, TC16, TC17, TC21, RV-02 | 6 | **RISK** — TC15/16/17/21 "Không test" |
| T4 — Note UI (coexist ghi chú ※ cũ, responsive) | Feature | Low | TC01, TC04, TC18, RV-03 | 4 | **OK** |
| ✱ DEPLOY-ASSET / cache JS (cross-cutting) | Non-func | Cao | — | 0 | **GAP** → §4.1 |

### ORPHAN TCs

Không có. Cả 28 TC đều thuộc scope BUG / F1–F3 / T1–T4 hoặc quan điểm LME (COMPAT-LEGACY, REG-SHARED, UI, FUNC). Không có case lạc chủ đề.

---

## 3.5 Fix-shape analysis (adversarial)

| Mục | Giá trị |
|---|---|
| Fix shape (đọc mục 2 dev-impact) | **"JS / asset"** (xoá code `history.pushState` + `addEventListener('popstate')` ở 2 file JS tĩnh + thêm note ở 1 blade) — **Khác**: KHÔNG phải generic-catch, KHÔNG validation, KHÔNG payment. Đồng thời là **"sửa hàm dùng chung"** — `default_setting.js` là template JS **dùng chung mọi popup** (mục 1). |
| Trigger space cần cover | (a) **Asset/cache** (DEPLOY-ASSET-001): F5-thường trên browser/site khách còn cache JS cũ → nhận bản mới, không còn bẫy Back. (b) **Shared-JS** (REG-SHARED-001): mọi kiểu popup dùng chung template + màn lịch khác không đụng. (c) **Real device** (RULE-06/ENV-003): iOS Safari + Android Chrome thật. |
| Số trigger TCs hiện cover | (a) **0/1** — GAP. (b) **~2/2 OK** (RV-01 đối chứng âm after_open_page; RV-02 đối chứng âm màn lịch khác). (c) **0/2** — TC12/TC13 = "Không test". |
| KH report dạng | **Không phải symptom-bug** — là **câu hỏi support** ("popup của LME có thuộc diện Google phạt không?") → chuyển thành spec-change (nhánh B). Root cause rõ ràng (close_page dùng pushState+popstate). ⇒ AP-2 **N/A**. |
| Alternative root causes cần verify | N/A (không phải symptom-only; root cause đã xác định ở source). |
| Anti-patterns dính | **AP-4 (một phần)**: mục "Commit/PR" trống → không trace được diff (nhưng fix là *xoá code*, không phải generic-catch → rủi ro thấp, hạ xuống MINOR). **AP-1/AP-2/AP-3/AP-6 = Không** (mục 3 dev-impact đã list caller; regression có đối chứng âm; không generic-catch). |

> **Kết luận Bước 3c**: trigger (a) asset/cache **0 cover** → nâng thành **[BLOCKER] FIX-SHAPE** (DEPLOY-ASSET-001 ưu tiên Cao, trigger khớp "release sửa JS"). Trigger (c) real-device **0 cover** → **[MAJOR] RULE-06**.

---

## 4. Issues phát hiện

### 4.1 Blocker (phải fix trước khi merge)

- **[BLOCKER] FIX-SHAPE / GAP-ASSET (DEPLOY-ASSET-001, Cao):** Fix xoá `pushState`+`popstate` trong **`public/js/embedded-popup/default_setting.js`** và **`public/js/calendar_salon/index.js`** — cả 2 là **JS tĩnh cache ở browser**. `default_setting.js` còn chạy trên **website của khách (bên ngoài)** — nơi ta không kiểm soát cache. Không có TC nào nghiệm thu bằng **F5 thường** (KHÔNG Ctrl+F5) trên browser/site còn cache bản cũ, cũng không kiểm Network trả **200 với version/hash mới** (Catalog D — **ENV-ASSET**). Rủi ro: sau deploy, khách vẫn nạp JS cũ → **vẫn bẫy nút Back** = đúng hành vi Google phạt mà ticket muốn gỡ, kéo dài không xác định. — **Fix:** thêm TC DEPLOY-ASSET (xem §5 TC-DEPLOYASSET001-01/02), verify version/hash query đổi + F5-thường nhận bản mới trên **cả admin (calendar_salon) lẫn site khách nhúng popup**. ⚠️ *Nếu Dev xác nhận popup JS được **server-render inline** per-request (không phải file tĩnh cache) thì Leader có thể hạ xuống [MAJOR]* — cần hỏi Dev: `default_setting.js` nạp qua `<script src>` tĩnh hay sinh inline?

### 4.2 Major (nên fix)

- **[MAJOR] SYMPTOM/ENV — GAP real-device (RULE-06 / ENV-003):** TC05 (mobile Back) = Pass nhưng **TC12 (Safari iOS) + TC13 (Chrome Android) = "Không test"** với lý do "cần thiết bị thật". Đây chính là **output cuối trên surface khách** — hành vi nút Back trên mobile thật là mục tiêu của fix. Verify bằng oracle/source **chưa đủ** theo RULE-06/RULE-08. — **Fix:** bắt buộc chạy ít nhất 1 lượt thật iOS Safari + Android Chrome (production/real device), nâng TC12/TC13 từ "Không test" → có evidence (xem §5 TC-ENV003-01). Nếu thật sự không có thiết bị → phải có phiếu Leader duyệt + phương án giám sát (RULE-08), không tự cho Đạt.
- **[MAJOR] CACHE — GAP popup cache riêng (DATA-CACHE-001 / Catalog ENV-POPUP):** Catalog D ghi rõ "**popup có cache riêng** → hiển thị nội dung cũ sau khi admin sửa; kiểm popup trên browser **đã từng xem popup cũ**". Bộ TC không có case: đã xem popup close_page bản cũ (còn bẫy Back) → sau deploy mở lại **cùng browser đó** → hành vi Back đã theo bản mới. — **Fix:** xem §5 TC-DATACACHE001-01.
- **[MAJOR] AUTO-FILL chưa verify — `01-bug-task.md`:** file có `Auto-filled: 2026-07-21 by /new-task` nhưng checkbox **"Tester verify auto-fill chính xác" CHƯA tick**. Review chỉ có giá trị khi tester đã đọc lại description + attachment Redmine và xác nhận. — **Fix:** tester đọc lại #38761, tick checkbox.
- **[MAJOR] AUTO-FILL chưa verify — `03-dev-impact.md`:** tương tự, `Auto-filled: 2026-07-21 by /new-task` + checkbox chưa tick. F/D/T ở đây map từ cấu trúc Redmine **Files/Data/Tính năng** (không phải 4.1/4.2/4.3 chuẩn) → càng cần tester verify không sót impact. Lưu ý mục 1 & 2 trong Redmine có dòng kết thúc bằng "…" (nghi bị cắt) — cần verify full text. — **Fix:** tester đọc lại journal Redmine, tick checkbox, xác nhận không sót caller/impact.

### 4.3 Minor (có thể fix sau)

- **[MINOR] Format file 04 không có `Mã quan điểm liên kết`:** sheet nguồn (fetched read-only) dạng checklist, thiếu cột map quan điểm → coverage phải suy luận thủ công. Không bắt convert (read-only), nhưng khi bổ sung TC mới (§5) nên gắn mã quan điểm để dễ trace.
- **[MINOR] File 04 thiếu cột `Trạng thái đánh giá spec` + loại evidence (RULE-02):** nội dung note JP là spec-driven (nguồn SpecImprove #38918) — nên ghi `Spec ghi rõ` + loại evidence bắt buộc (screenshot màn admin + video nút Back trên device) cho các TC khi chạy thật.
- **[MINOR] AP-4 — thiếu link Commit/PR:** `03-dev-impact.md` mục "Commit / Pull Request" = `<chưa có>` (chỉ có branch `ai_small_38761`). Fix là *xoá code* nên rủi ro fix-shape thấp, nhưng nên bổ sung PR link để Leader trace diff (xác nhận đã bỏ đúng `pushState` dư trong `popupInsertAdjacentHTML`).

### 4.4 Nit (gợi ý)

- **[NIT] TC14** `staging = "Cần comfirm"` (typo "confirm") và chưa rõ confirm gì — nên ghi rõ điểm cần Leader confirm.
- **[NIT]** Nhiều TC (TC15/16/17/19/21) để "Không test" kèm lý do hợp lý (ngoài phạm vi harness) — nên gom thành 1 ghi chú "regression ngoài scope, đã có test riêng #38519/38520/38537" để Leader duyệt 1 lần thay vì rải rác.
- **[NIT]** Có thể bổ sung 1 TC `FUNC-SEQ-001` nhẹ: đổi 表示タイプ qua lại nhiều lần rồi **F5** → note hiển thị đúng theo giá trị cuối (TC04 chưa có bước F5).

---

## 5. TCs đề xuất bổ sung

> Member copy vào `04-tc-list.md` round sau (16 cột canonical). Ưu tiên đóng GAP asset-cache (BLOCKER) + real-device (MAJOR).

| TC No. | Mã quan điểm liên kết | Loại case | Tiêu đề test case | Điều kiện tiền đề | Các bước thực hiện | Dữ liệu test/input | Kết quả mong đợi | Kết quả thực thi | Evidence thực tế | Môi trường test | Người thực hiện | Ngày thực hiện | Số ticket bug | Trạng thái đánh giá spec | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DEPLOYASSET001-01 | DEPLOY-ASSET-001 | Normal | `default_setting.js` bản mới nạp bằng F5 thường trên site khách còn cache bản cũ → nút Back không còn bẫy popup | - Trang web khách có nhúng popup `close_page` bằng script LME<br>- Mở trang đó **TRƯỚC** deploy để browser cache `default_setting.js` bản cũ (còn `pushState`/`popstate`) | 1. Trước deploy: mở trang khách trên Chrome, xác nhận bấm Back **bật** popup (hành vi cũ).<br>2. Deploy bản fix.<br>3. Quay lại tab, **F5 thường** (KHÔNG Ctrl+F5).<br>4. Mở DevTools > Network, lọc `default_setting.js`.<br>5. Bấm nút Back của trình duyệt. | URL script popup nhúng của 1 bot test | Network trả `default_setting.js` **200 với query version/hash MỚI** (không 304 bản cũ, không 404). Bấm Back **quay về trang trước/thoát ngay**, popup KHÔNG hiện. | Chưa test | | PRODUCTION | | | | Spec ghi rõ | Lấp GAP-ASSET (BLOCKER §4.1). Evidence bắt buộc: screenshot Network (version+200) + video nút Back. RULE-08 → PRODUCTION vì `default_setting.js` chạy trên site khách. |
| TC-DEPLOYASSET001-02 | DEPLOY-ASSET-001 | Normal | `calendar_salon/index.js` bản mới nạp F5 thường ở màn admin Salon còn cache bản cũ → Back điều hướng bình thường | - Đăng nhập admin Salon<br>- Mở màn Calendar Salon **TRƯỚC** deploy để cache `index.js` bản cũ (còn back-trap) | 1. Trước deploy: ở màn Calendar Salon bấm Back → xác nhận bị **giữ trang** (hành vi cũ).<br>2. Deploy bản fix.<br>3. **F5 thường** màn Calendar Salon.<br>4. DevTools > Network lọc `calendar_salon/index.js`.<br>5. Bấm Back. | — | Network trả `calendar_salon/index.js` **200 version mới**, không 404. Bấm Back **điều hướng bình thường**, không bị pushState giữ trang. | Chưa test | | STAGING | | | | Spec ghi rõ | Lấp GAP-ASSET (BLOCKER §4.1) phía admin. Ghi chú: `regression` asset. |
| TC-DATACACHE001-01 | DATA-CACHE-001 | Abnormal | Browser đã từng xem popup `close_page` bản cũ → sau deploy mở lại cùng browser → hành vi Back theo bản mới (không dính cache popup riêng) | - Browser đã mở & bật popup `close_page` bản cũ ít nhất 1 lần (có cache popup)<br>- Đã deploy bản fix | 1. Trên browser đã xem popup cũ, **không xoá cache thủ công**.<br>2. Truy cập lại trang khách có popup `close_page`.<br>3. Điều hướng vào trang, bấm Back 1 lần. | — | Popup KHÔNG bị bật khi bấm Back (cache popup riêng không giữ lại listener cũ). Số history entry không tăng thêm do popup. | Chưa test | | PRODUCTION | | | | Spec ghi rõ | Lấp GAP popup-cache (MAJOR §4.2). Catalog ENV-POPUP. Evidence: video Back trên browser còn cache popup cũ. |
| TC-ENV003-01 | ENV-003 | Normal | Nút Back trên iOS Safari + Android Chrome thật (thiết bị thật) — popup `close_page` không còn hiện khi bấm Back | - Có thiết bị thật iPhone (Safari) + Android (Chrome)<br>- Trang khách nhúng popup `close_page`, bản fix đã deploy | 1. Mở trang popup `close_page` trên **Safari iOS thật**, điều hướng vào trang, bấm Back → quan sát.<br>2. Lặp lại trên **Chrome Android thật**.<br>3. Đối chứng: mở popup `after_open_page` trên cả 2 thiết bị, bấm Back. | — | Cả iOS Safari và Android Chrome: bấm Back **quay về/thoát ngay, popup KHÔNG hiện**. `after_open_page`: Back bình thường, không đổi. | Chưa test | | PRODUCTION | | | | Spec ghi rõ | Nâng TC12/TC13 từ "Không test" → có evidence thật (MAJOR §4.2, RULE-06/ENV-003). Evidence: video màn hình 2 thiết bị thật. |

---

## 6. Spec update needed

- [x] **Cần cập nhật spec** — FA-018 Popup nhúng:
  - **Section**: hành vi kiểu hiển thị `close_page` (離脱時表示型).
  - **Nội dung cần update**: từ 15/06/2026 popup `close_page` **KHÔNG** còn bật khi bấm nút Back trên mobile (bỏ back-button hijack theo chính sách Google); chỉ giữ tín hiệu `visibilitychange` (đổi tab) + `blur` (mất focus) trên desktop. Ghi rõ note chú thích JP ở màn thiết lập. Mặc định `mobile close_page` mất kênh exit-intent → cập nhật tài liệu hướng dẫn khách.
  - **Người chịu trách nhiệm update**: PM/Dev (Do Van Tu TuDV) + nguồn SpecImprove #38918.

---

## 7. Checklist đã chạy

- [x] A. Coverage — matrix §3; ORPHAN: không có.
- [x] B. Chất lượng từng TC — TC rõ ràng, atomic; một số để "Không test" có lý do.
- [x] C. Chất lượng bộ TC tổng thể — phân bố tốt (Normal + Abnormal + đối chứng âm); không trùng lặp.
- [x] D. Spec alignment — cần update spec FA-018 (§6).
- [x] E. Hành chính — file 04 fetched read-only, thiếu cột canonical (MINOR §4.3).
- [x] F. Base quan điểm test LME — bảng F.1 dưới.
  - [x] F.1 Quan điểm (tầng 1)
  - [x] F.2 Catalog (tầng 2) — B (UIC-01/15 note), D (ENV-ASSET/ENV-POPUP/ENV-DOMAIN), C (MAP-LIFF popup)
  - [x] F.3 RULE — RULE-06 (real device, MAJOR), RULE-08 (production asset, BLOCKER), RULE-09 (legacy — RV-04 OK)

### F.1 — Bảng quan điểm đối chiếu

| Mã quan điểm | Ưu tiên | Trigger khớp task? | TC cover (suy luận) | Kết luận |
|---|---|---|---|---|
| FUNC-001 (luồng chính — note hiện đúng theo `close_page`) | Cao | ◯ | TC01, TC04, RV-06 | **OK** |
| UI-FIELD-001 (field con "note" theo field cha 表示タイプ) | Trung bình | ◯ | TC02, TC03, TC04, RV-06 | **OK** |
| UI-001 (responsive note, coexist ※ cũ) | Trung bình | ◯ | TC18, RV-03 | **OK** |
| REG-SHARED-001 (`default_setting.js` dùng chung mọi popup; calendar_salon) | Cao | ◯ | RV-01 (đối chứng âm after_open_page), RV-02 (đối chứng âm màn lịch khác) | **OK** (đối chứng âm tốt) |
| COMPAT-LEGACY-001 (popup close_page tạo trước deploy tự nhận note + hành vi mới) | Cao | ◯ | RV-04 | **OK** |
| **DEPLOY-ASSET-001** (sửa 2 JS tĩnh → cache/version) | **Cao** | ◯ | — | **GAP → [BLOCKER]** |
| **ENV-003** (asset/domain production; real device mobile) | **Cao** | ◯ | TC05 (staging pass); TC12/TC13 = Không test | **RISK → [MAJOR]** |
| DATA-CACHE-001 (popup có cache riêng) | Trung bình (→Cao user-facing) | ◯ | — | **GAP → [MAJOR]** |
| FUNC-001 output-truth / RULE-06 (nút Back thật trên device) | Cao | ◯ | TC05 pass; real device deferred | **RISK → [MAJOR]** |
| DATA-DB-001 / RULE-07 (WHERE scope, CRUD) | Cao | × | — | **N/A** — fix thuần view, không UPDATE/DELETE data (lý do RULE-03) |
| MSG-* / BULK-* (gửi tin, đối tượng) | Cao | × | — | **N/A** — không chạm gửi tin |
| PAY-* (thanh toán/gói) | Cao | × | — | **N/A** — không chạm tiền |
| MEDIA-* (upload/resize) | TB→Cao | × | — | **N/A** — không upload media |
| PERM-* (phân quyền) | Cao | × | — | **N/A** — không đổi lưới quyền |
| CONC-* (đồng thời) | Cao | × | — | **N/A** — không có ghi dữ liệu tranh chấp |
| STATE-CLEAN-001 (hủy hợp đồng) | Cao | × | — | **N/A** — không chạm luồng hủy |
| DEPLOY-LIVE-001 (client cũ gọi server mới) | Cao | × | — | **N/A** — fix thuần view, không đổi payload/field/request API (lý do RULE-03) |

> **Không** dùng §4 checklist-lme (FORM-01/CHAT-01/ADM-*/TPL-01) để flag — RULE-11.

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
