# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | `#37246 — [Add bot/Setting bot] Không đổi được ảnh & tên tài khoản từ 「LINE公式アカウント表示設定」` |
| Reviewer (Leader) | `<Leader verify>` |
| Tester được review | `<member điền — file 04 chưa ghi tên>` |
| Ngày review | `2026-07-01` |
| Version TCs | `v2` |
| Vòng review | `Round 2` (sau khi human rewrite theo cơ chế auto-save) |

> Spec reference: dùng `templates/LME-SYSTEM-SPEC.md` tổng (không có `02-spec-reference.md` riêng).

---

## 0. Cơ chế thực tế (Leader clarify — nền tảng review)

| Khu vực màn 「LINE公式アカウント表示設定」 | Cơ chế save | Validate / call API LINE? |
|---|---|---|
| **Tên + ảnh account** | **AUTO-SAVE** (không nút confirm) | **KHÔNG** |
| **Messaging API** (Channel Secret,...) | Nút confirm → save | **CÓ** validate |
| **LINEログイン** (Channel ID,...) | Nút confirm → save | **CÓ** validate |

**Bug repro đúng**: key Messaging API / LINE login **đang LỖI** → user đổi **tên/ảnh (auto-save)** → bị báo lỗi 「入力した情報が間違っています」 dù không nên call API LINE. Fix = chỉ validate khi key thật sự đổi.

---

## 1. Verdict

- [ ] **APPROVED**
- [ ] **APPROVED WITH CHANGES**
- [x] **REJECTED** — *nhưng đã rất gần approve*. Toàn bộ **BLOCKER cơ chế của Round 1 đã được sửa đúng**. Còn lại vài MAJOR cần dọn: 1 mâu thuẫn expected + trùng nhãn, thiếu TC security, giảm regression coverage, và 2 checkbox verify auto-fill vẫn chưa tick.

**Lý do ngắn gọn**: Bản v2 **sửa đúng trọng tâm** — đã bỏ bước "Lưu" thủ công (dùng auto-save), và tách rõ điều kiện **"channel secret bị lỗi" vs "hợp lệ"** → reproduce đúng hiện tượng bug. Vấn đề còn lại đều là dọn dẹp/bổ sung, không còn sai bản chất.

---

## 2. Delta so với Round 1

| Issue Round 1 | Trạng thái v2 |
|---|---|
| **[BLOCKER] Cơ chế sai — mô tả "bấm nút Lưu"** | ✅ **RESOLVED** — v2 dùng "Change tên/ảnh" auto-save, bỏ nút Lưu. |
| **[BLOCKER] Reproduce sai — precondition key hợp lệ** | ✅ **RESOLVED** — v2 tách "Bot có channel secret **bị lỗi**" + Change tên/ảnh → "Change thành công". Đúng điều kiện repro. |
| **[BLOCKER] GAP T4 — LINEログイン** | ⚠️ **PARTIAL** — v2 thêm section LINEログイン **nhưng chỉ test confirm-form (validate Channel ID)**, chưa test "LINE login key **lỗi** + auto-save tên/ảnh → OK". Xem §4.2. |
| **[MAJOR] Security getData secret leak** | ❌ **CHƯA cover** — v2 không thêm TC security. Vẫn mở. |
| **[MAJOR] Auto-fill chưa verify (01 & 03)** | ❌ **Vẫn chưa tick** cả 2 checkbox. |
| **[MINOR] TC020 thiếu metadata** | ✅ Đã gộp vào cấu trúc mới (No.2/No.4: xóa tên → lỗi required). |

---

## 3. Coverage Matrix (v2 — theo No. trong file 04)

| Impact | Loại | TCs map | Status |
|---|---|---|---|
| BUG (key LỖI + auto-save tên/ảnh → vẫn Change thành công) | Fix | No.1 (tên), No.5 (ảnh) | ✅ **OK** — đúng repro |
| F1 — `SettingBotController@update` (guard secretChanged) | Direct | No.1,3,5,9 + confirm No.13-21 | **OK** |
| F2 — `SettingBotController@getData` (trả secret thật, không mask) | Direct | — | **GAP (security)** — không TC nào verify secret không bị lộ |
| F3 — `setting-bot.js` (auto-save không đụng key) | Direct | No.1,3,5,9 | **OK** |
| F4 — `validateTokenAddBot` (invalid → error) | Indirect | No.14,17,20 | **OK** |
| D1 — `channel_secret` (không bị ghi đè rỗng) | Data | (ngầm qua No.1,5) | **RISK** — v1 có TC010 query DB, v2 bỏ → không còn TC verify DB trực tiếp |
| T1 — Auto-save tên/ảnh | Feature | No.1-12 | ✅ **OK** (mạnh: valid/empty/wrong-format/>10MB/xóa) |
| T2 — Messaging API confirm+validate | Feature | No.13-15, 19-21 | **OK** (nhưng có mâu thuẫn — §4.2) |
| **T4 — LINE login key LỖI + auto-save tên/ảnh** | Feature | — | **GAP** (chỉ test confirm form No.16-18, không test auto-save khi LINE login lỗi) |
| T3 — An toàn dữ liệu channel_secret | Feature | (ngầm) | **RISK** |

### ORPHAN / lưu ý format
- No.22 ([CL1] staff) còn ở **format 10 cột cũ**, lệch với cấu trúc phân cấp mới → nên chuẩn hóa lại cho đồng nhất (MINOR).

---

## 3.5 Fix-shape analysis (v2)

| Mục | Giá trị |
|---|---|
| Fix shape | Specific conditional guard — bỏ re-validate token trong luồng auto-save tên/ảnh. |
| Điều kiện repro cover | **Channel secret lỗi: OK** (No.1,5). **LINE login lỗi: CHƯA** (chỉ test confirm form). |
| Assertion "không call API LINE" | ❌ Expected v2 ghi "Change thành công / Lưu" nhưng **chưa assert rõ "không có request gọi API LINE"** — điểm quan sát cốt lõi của fix. |
| Anti-patterns | AP-3 nhẹ (regression coverage giảm so với v1). AP-1/AP-2/AP-6 không dính. |

---

## 4. Issues phát hiện

### 4.1 Blocker
- Không còn BLOCKER. ✅ (Các BLOCKER cơ chế Round 1 đã fix.)

### 4.2 Major (nên fix trước approve)

- **[MAJOR] No.19-21 trùng nhãn + expected MÂU THUẪN**: No.13-15 và No.19-21 cùng nhãn "Change Messaging API - Channel Secret". Riêng case **xóa→để trống**: No.15 expected `Channel Secretを入力してください。` nhưng No.21 expected `入力した情報が間違っています`. Cùng 1 field, 2 expected khác nhau → tester chạy sẽ mâu thuẫn. — **Fix**: xác nhận No.19-21 thực chất là field nào (nghi là **LINEログイン - Channel Secret** hoặc **Messaging API - Channel ID**), sửa nhãn + expected cho đúng.

- **[MAJOR] GAP — LINE login key LỖI + auto-save tên/ảnh chưa test**: Bug repro trên **cả** Messaging API lẫn LINE login key lỗi (§0). v2 chỉ vary "channel secret" ở section auto-save; section LINEログイン (No.16-18) là test **confirm form**, khác scenario. — **Fix**: thêm điều kiện "Bot có **LINE login key bị lỗi**" cho section change tên/ảnh (giống No.1/No.5), expected = auto-save OK. Hỏi Dev: fix có cover nhánh này, hay LINE login đã guard sẵn (mục 3 dev-impact)?

- **[MAJOR] Security — F2 getData trả channel_secret thật ra FE (chưa có TC)**: Vẫn như Round 1 — TC không verify secret không bị lộ cho user/staff không quyền. Rủi ro mạo danh Messaging API channel. — **Fix**: thêm TC security (§5 TC-NEW-01); hỏi Dev có thể so sánh phía server thay vì trả secret plaintext không.

- **[MAJOR] Regression coverage giảm so với v1**: v1 có multi-bot (CL11), reload (CL2), double-click (CL5), path URL/ảnh cũ 404 (CL22), query DB channel_secret (D1). v2 bỏ gần hết, chỉ giữ CL1 staff. — **Fix**: giữ lại ít nhất **multi-bot (chỉ bot đang thao tác đổi, WHERE bot_id)** và **query DB verify channel_secret không bị ghi đè rỗng (D1)** — 2 cái này bảo vệ đúng scope fix.

- **[MAJOR] Auto-fill 01 & 03 chưa verify**: 2 checkbox "Tester verify auto-fill chính xác" vẫn `[ ]`. — **Fix**: tester đọc lại Redmine, tick.

### 4.3 Minor

- **[MINOR] Chưa assert "KHÔNG call API LINE"** ở các TC auto-save khi key lỗi — nên thêm bước quan sát Network/log vào Expected (đây là bằng chứng trực tiếp fix hoạt động).

- **[MINOR] Assertion "hiển thị lịch sử change name/ảnh"** là yêu cầu MỚI — cần confirm màn 表示設定 thực sự có **change history**. Nếu không có feature này → expected sai.

- **[MINOR] No.22 (CL1 staff) lệch format** — chuẩn hóa về cấu trúc phân cấp.

### 4.4 Nit

- **[NIT] Bất đối xứng message "để trống"**: Channel Secret trống → `Channel Secretを入力してください。` (message "bắt buộc" cụ thể), nhưng LINEログイン Channel ID trống → `入力した情報が間違っています` (generic). Nếu đây là 2 message spec khác nhau thì OK; nếu không → có thể là điểm cần Dev thống nhất (empty nên ra message "required" riêng, không phải generic invalid).

---

## 5. TCs đề xuất bổ sung

| TC ID | Title | Precondition | Steps | Expected | Priority | Type | Map |
|---|---|---|---|---|---|---|---|
| TC-NEW-06 | LINE login key ĐANG LỖI + đổi tên/ảnh account (auto-save) → vẫn lưu, không call API LINE | Bot có **LINEログイン key lỗi/không hợp lệ**. Mở Network tab. | 1. Vào 表示設定.<br>2. Đổi tên hoặc ảnh (auto-save).<br>3. Quan sát Network/log. | Auto-save OK; không báo lỗi; KHÔNG có request call API LINE. (Nếu vẫn lỗi → Dev: fix chưa cover nhánh LINE login.) | High | Regression | T4 (GAP), F1 |
| TC-NEW-08 | D1 — channel_secret KHÔNG bị ghi đè rỗng khi auto-save tên/ảnh (key đang lỗi) | Bot có channel_secret ở trạng thái lỗi nhưng ≠ rỗng. Có quyền query DB. | 1. Ghi lại channel_secret DB.<br>2. Đổi tên/ảnh (auto-save).<br>3. Query lại DB. | channel_secret GIỮ NGUYÊN, không bị set rỗng/null sau auto-save. | High | Boundary | D1, T3 |
| TC-NEW-09 | Multi-bot: auto-save tên/ảnh bot A (key lỗi) → chỉ bot A đổi, bot B nguyên | 2 bot A,B cùng account. | 1. 表示設定 bot A → đổi tên/ảnh.<br>2. Kiểm tra bot B. | Chỉ bot A đổi (đúng WHERE bot_id); bot B không đổi. | High | Boundary | F1, checklist CL11 |
| TC-NEW-01 | Security: channel_secret KHÔNG lộ plaintext ra FE/response cho user không được phép | Bot có Channel Secret hợp lệ. 1 staff không quyền. DevTools Network. | 1. Account có quyền: xem response getData + page source.<br>2. Staff không quyền: gọi endpoint getData bot đó. | channel_secret không plaintext cho user không phép; staff không quyền không lấy được. | High | Negative/Security | F2, checklist §A.2 |

---

## 6. Spec / Dev confirm needed

- [x] **Cần Dev confirm**:
  - (1) No.19-21 là field nào? (trùng nhãn + expected mâu thuẫn No.15)
  - (2) Fix có cover nhánh **LINE login key lỗi + auto-save tên/ảnh** không, hay đã guard sẵn?
  - (3) `getData` có trả channel_secret plaintext ra FE không? Behavior mới do fix? (có thể escalate BLOCKER security)
  - (4) Màn 表示設定 có feature **change history** (lịch sử change name/ảnh) như expected v2 giả định không?
  - (5) "Để trống" của Channel Secret vs LINEログイン Channel ID có 2 message khác nhau đúng spec không?

---

## 7. Checklist đã chạy

- [x] A. Coverage — BUG ✅ repro đúng / Function ✅ / Data RISK (D1 mất TC) / Feature: GAP T4 LINE-login-broken-autosave / A.6 fix-shape ✅
- [x] B. Chất lượng từng TC — cải thiện nhiều; còn mâu thuẫn No.19-21
- [x] C. Bộ TC tổng thể — regression coverage giảm (§4.2)
- [x] D. Spec alignment — 5 điểm cần Dev confirm (§6)
- [x] E. Hành chính — thiếu tên Tester; No.22 lệch format
- [x] F. Base checklist LME — F.1 web: CL1 giữ, CL2/3/5/11/16/22 giảm; A.2 Security chưa cover. F.2/F.3: N/A

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | | |
| Tester | (đã đọc & hiểu feedback) | |
