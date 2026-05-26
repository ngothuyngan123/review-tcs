# 02 — Spec Reference

> Trích spec liên quan đến bug KH #36202. **KHÔNG** paste toàn bộ spec.
> Nguồn đầy đủ: [spec-features/admin/staff-management/feature-spec.md](../../spec-features/admin/staff-management/feature-spec.md) (FA-035, version 1.0, 2026-05-07).

## Section liên quan

### Tổng quan: Hai flow song song

Tính năng staff management có **2 flow song song** trong code:

| Tiêu chí | Legacy Flow | **Invite URL Flow** (bug fix nhắm vào) |
|---|---|---|
| Endpoint tạo | POST `/employees-management/add` | POST `/ajax/generate-link-invite-staff` |
| Model tạo | `User` trực tiếp | `InviteStaff` + `UserStaffBot` (pending) |
| Bảng count limit | `access_bot` | `user_staff_bots` |
| UI hiện tại | Không còn UI (route still alive) | SCR-EMP-02 (đang dùng) |

Bug KH #36202 nằm ở **Invite URL Flow** — `generateLinkInviteStaff` + `acceptInviteStaff`.

### BR-005: Free plan không được tạo staff (có ngoại lệ legacy)

> **Source:** `StaffManagementController.php:85-87`

- Bot `plan_type = 2` (free) → **bị loại bỏ** khỏi form invite (không hiển thị)
- ⚠️ **Ngoại lệ legacy**: Bot free **tạo TRƯỚC 2021-07-01** vẫn cho phép có staff (legacy data)
- UI cảnh báo: 「※ フリープラン場合、スタッフの追加はできません。」

### BR-006: Standard 10 staff limit + Legacy standard exception

> **Source:** `UserController.php:3428-3438` + Dev clarify 2026-05-08

#### BR-006a — Standard mới (post-cutoff): áp limit 10
- Bot có `contract_type = 'standard'` + `flag_contract_new = 1` (HOẶC bot tạo SAU 2023-05-01 — Q9 confirm field implementation)
- Count `user_staff_bots WHERE bot_id=X AND is_admin=0 AND status=1`, nếu `>= 10` → lỗi: 「スタンダードプランの上限に達しています。プロプランへの変更が必要...」
- ĐÂY là rule mà bug fix add vào Invite URL flow (trước fix chỉ enforce ở legacy `addEmployee` qua `access_bot`).

#### BR-006b — ✅ Legacy standard exception (Dev confirm 2026-05-08)
- Bot có `contract_type = 'standard'` nhưng **tạo TRƯỚC 2023-05-01** → **đối xử như Pro plan** (KHÔNG giới hạn tạo staff)
- Implementation field cần Dev clarify (Q9): có thể qua `flag_contract_new = 0`, hoặc check `bots.created_at < '2023-05-01'`, hoặc combination.
- Effect: bot legacy standard có thể có > 10 staff thoải mái — không bị BR-006a chặn.

#### Plan limits tổng quan (sau khi cộng 2 BR)

| Loại bot | Giới hạn staff |
|---|---|
| Pro | Unlimited |
| **Standard tạo trước 2023-05-01** (BR-006b) | **Unlimited** (treated as Pro) |
| Standard tạo từ 2023-05-01 trở đi (BR-006a) | Max 10 active staff |
| Free tạo trước 2021-07-01 (BR-005 ngoại lệ) | Unlimited (legacy) — Q4 confirm |
| Free tạo từ 2021-07-01 trở đi | KHÔNG được tạo staff (hide khỏi form) |

> ⚠️ **Spec note gốc**: "Giới hạn này áp dụng qua `access_bot` (legacy). **Chưa xác nhận có áp dụng cho invite URL flow qua `user_staff_bots` hay không.**" → ĐÂY CHÍNH LÀ BUG mà KH báo cáo. Bug fix = thêm check tương tự vào Invite URL flow + áp dụng đúng exception cho standard cũ.

### BR-007: Admin auto-tạo UserStaffBot record

> **Source:** `StaffManagementController.php:527-546`

Khi `getStaffByBot` được gọi, nếu admin chưa có record `UserStaffBot` cho bot:
```
UserStaffBot.create({
  bot_id, user_id,
  is_admin = 1,
  role_id = 0,
  status = 1
})
```

⚠️ **Quan trọng cho count limit**: Admin (is_admin=1) xuất hiện trong `user_staff_bots`. Logic check max staff **PHẢI filter** `is_admin = 0` (và nên filter `status = 1` — STATUS_ACCEPT) để không nhầm.

### BR-004: Quyền truy cập

> **Source:** `StaffManagementController.php:40-43`

```
checkBotHasPermission('staff-management.inviteStaff', bot_id) = false
  → REDIRECT adminIndex (không phải hide button)
```

Staff không phân quyền **bị BE redirect**, không chỉ ẩn UI.

### Status enum của user_staff_bots

| Giá trị | Hằng số | Ý nghĩa | Có count vào limit? |
|---|---|---|---|
| 0 | STATUS_NO_ACTION | Invite tạo, chưa accept | ❌ **KHÔNG count** (Dev confirm 2026-05-08) |
| 1 | STATUS_ACCEPT | Đang hoạt động | ✅ Count |
| 2 | STATUS_REJECT | Đã từ chối | ❓ Spec chưa nói rõ (Q7 vẫn open) |

> Logic count chuẩn: `SELECT COUNT(*) FROM user_staff_bots WHERE bot_id=X AND is_admin=0 AND status=1`. Kết hợp với check-at-accept-time → khi staff accept, BE re-count active và quyết định cho/không cho.

### BR-001 + BR-002: Invite URL lifecycle

- Hết hạn sau 24h kể từ `invite_staffs.created_at` (BR-001)
- Single-use: `is_confirmed = 1` sau khi accept → mọi truy cập sau đó báo lỗi (BR-002)

→ Edge case quan trọng: invite tạo khi bot 5/10 → bot fill lên 10/10 trước khi staff accept → staff vẫn cố accept invite cũ → behavior phải là **fail with limit message** (kiểm tra max ở thời điểm accept, không phải tạo invite).

## Open questions từ spec

> **Spec section 9 - Open Questions** liên quan trực tiếp bug:

1. **Giới hạn 10 staff (BR-006) có áp dụng cho invite URL flow không?** → Bug fix đang trả lời "có"
2. Pro plan dùng `plan_type` nào? Spec chỉ liệt kê 1=standard và 2=free trong `bots.plan_type`. Pro plan có thể qua `contract_type = 'pro'` (legacy field)?

## Trạng thái spec gaps (Dev clarify 2026-05-08)

| # | Câu hỏi | Status / Ghi chú |
|---|---|---|
| ~~Q1~~ ✅ | Số `10` | **Hard-code 10**, không đọc config |
| ~~Q2~~ ✅ | Count filter | `is_admin=0 AND status=1`. Pending (status=0) KHÔNG count |
| ~~Q3~~ 🚫 | Pro plan identification | Drop — tester không cần biết DB field, chỉ cần "bot pro plan" |
| Q4 | Bot free legacy (pre-2021-07-01) có bị check max 10? | Còn open — TC021 sẽ verify khi run |
| ~~Q5~~ ✅ | Multi-bot accept message | TC008 expected đúng (per-bot hoặc tổng đều OK miễn rõ) |
| ~~Q6~~ ✅ | Soft-delete staff | **KHÔNG có** soft-delete → drop C.7 case 3 |
| ~~Q7~~ 🚫 | REJECT status mechanics | Drop — internal state, không phải tester scope |
| ~~Q8~~ 🚫 | Audit log (BotLifeCycle 24/25) | Drop — internal log, không phải tester scope |
| ~~Q9~~ 🚫 | Cutoff field name | Drop — tester chỉ cần "bot tạo trước/sau 2023-05-01" để dựng test data |
| ~~BR-006b~~ ✅ | Standard pre-2023-05-01 treat as Pro? | Đúng — TC024 + TC025 cover |

**Phụ thuộc additional (Dev confirm):**
- Bot downgrade: chỉ system admin downgrade được; vẫn cho down bình thường khi > limit (out-of-scope bug này).
- Remove role staff: count giảm 1 — đã cover TC018 (delete staff release slot).

## Liên kết tới spec đầy đủ

- [feature-spec.md](../../spec-features/admin/staff-management/feature-spec.md) — đầy đủ 1126 dòng
- [api-spec.md](../../spec-features/admin/staff-management/web/api-spec.md) — chi tiết EP-09 (generateLinkInviteStaff), EP-19 (acceptInviteStaff), EP-21 (legacy addEmployee)
- [logic-spec.md](../../spec-features/admin/staff-management/web/logic-spec.md) — flow logic + race conditions
- [db-mapping.md](../../spec-features/admin/staff-management/db/db-mapping.md) — schema chi tiết
