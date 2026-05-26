# 03 — Đánh giá ảnh hưởng từ Dev

> Trích nguyên văn từ sheet `Quản lý hợp đồng` row 1429 (commit 12/5).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | _<chưa rõ — verify từ PR>_ |
| Commit / Pull Request | `bugs/fix_bug_36303` (chưa có link PR cụ thể) |
| Branch | `bugs/fix_bug_36303` → release `release_step_20260511` |
| Ngày submit đánh giá | 2026-05-12 (commit theo note "=> commit 12/5") |

---

## 1. Nguyên nhân

Quyền đang check theo bot đang select. User là **staff** của bot kia và **không có quyền màn point setting** trên bot đó.

→ Khi user vào **detail hợp đồng của chính user** (user là owner contract), hệ thống bị đẩy ra vì đang lấy quyền theo bot đang select (sai logic — phải check ownership trước).

## 2. Cách fix

- Kiểm tra **nếu hợp đồng là của chính mình** (ownership) → **không cần check quyền** bot.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev không tách rõ "đã sửa" vs "chỉ check". Coi tất cả mục 4.1 là caller đã verify.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|
| F1 | `getRouteFromRoleAccess` | Direct | Function chính bị sửa — entry point check quyền |
| F2 | `getRouterBotInvite` | Indirect | Caller của F1 |
| F3 | `detailContract` | Direct | Function chính — màn detail hợp đồng (root cause bug) |
| F4 | `detailContractBillMaxFriendError` | Direct | Function detail max-friend contract |
| F5 | `changeCard` | Direct | Đổi card thanh toán |
| F6 | `changeBillType` | Direct | Đổi kỳ thanh toán (tháng/năm) |
| F7 | `changePaymentMethod` | Direct | Đổi phương thức thanh toán |
| F8 | `updateSubCard` | Direct | Update sub card |
| F9 | `deleteSubCard` | Direct | Xóa sub card |
| F10 | `authenticationBotContract` | Direct | Authenticate contract scope với bot |

### 4.2. List data bị update khi fix bug

| # | Data | Ghi chú |
|---|---|---|
| _ | _**không có**_ — fix chỉ thay đổi logic check quyền, không động database | Theo dev report |

### 4.3. List tính năng bị ảnh hưởng

| # | Tính năng | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Phân quyền các màn** (tổng quát) | F1, F2 | High |
| T2 | Detail hợp đồng | F3 | High |
| T3 | Detail hợp đồng **max friend** | F4 | High |
| T4 | Change card | F5 | Medium |
| T5 | Change phương thức thanh toán | F7 | Medium |
| T6 | Change sub card (đăng ký + update) | F8 | Medium |
| T7 | Xóa sub card | F9 | Medium |
| T8 | Change type bill | F6 | Medium |

---

## 5. PR

- Branch: `bugs/fix_bug_36303`
- Release: `release_step_20260511`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **chưa có snippet code** trong dev report, Leader nên hỏi dev cụ thể: ownership check dựa trên field nào (`contracts.user_id`? `contracts.owner_id`?)
- [ ] Mục 3 đã check đủ caller — **dev report không tách bạch "đã sửa" vs "chỉ verify caller"** → Leader nên hỏi rõ
- [ ] Mục 4.1 không thiếu function (so với mục 3) — OK
- [ ] Mục 4.2 không thiếu data — dev khẳng định "không có" nhưng cần verify (có dùng cache permission không?)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** — chưa rõ với **contract state**: đã connect vs chưa connect / đã expired / đang trial / standalone
- [ ] **Nghi vấn cần hỏi dev**:
  - Logic ownership check dựa vào field nào? (user_id của contract record vs user login)
  - Có rule khác cho **max friend contract** không?
  - Khi user là staff trên CHÍNH bot mà contract đó connect tới (vd contract Standard đã connect bot Y, user là staff của bot Y) → permission check thế nào?
  - Có ảnh hưởng cache permission (Redis) không?
