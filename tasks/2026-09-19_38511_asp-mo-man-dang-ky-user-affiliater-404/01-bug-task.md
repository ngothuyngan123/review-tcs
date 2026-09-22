# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #38511 bởi `/new-task` (2026-09-19). File này **chỉ giữ thông tin cần để viết/review TC** — metadata Redmine tra thẳng trên Redmine.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38511 — [Asp] Mở màn đăng ký user affiliater bị hiện lỗi 404` |
| Module / Màn hình | ASP管理 (Quản lý ASP) — chọn user owner → link login affiliater (`/aff/v2/login/<mã>`) → màn đăng ký affiliater `ASP管理 紹介者（登録）` (`/affiliate/<mã>/regist`) |

## Mô tả bug (bản dịch tiếng Việt)

Ở màn hình quản lý ASP, chỗ chọn user owner:
- Chọn vào user A → copy link login → mở link, sau đó nhấn mở màn regist (đăng ký) thì hiển thị được.
  https://staging.lme.jp/aff/v2/login/eaNArJeWyE27
- Chọn vào user B → copy link login → mở link, sau đó nhấn mở màn regist thì hiển thị màn lỗi 404.
  https://staging.lme.jp/aff/v2/login/vO3nqdjKW2Z8

## Steps to reproduce

1. Mở màn quản lý ASP (ASP管理), ở chỗ chọn user owner chọn user B.
2. Copy link login affiliater của user B (vd `https://staging.lme.jp/aff/v2/login/vO3nqdjKW2Z8`).
3. Mở link login → nhấn mở màn regist (đăng ký).

## Expected result

- Màn đăng ký affiliater hiển thị được (giống user A).

## Actual result

- Hiển thị màn lỗi 404.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- 2026_07_06_16_45_18_ASP管理_運営_一覧_.png — https://redmine.watermelon.vn/attachments/download/27851/2026_07_06_16_45_18_ASP%E7%AE%A1%E7%90%86_%E9%81%8B%E5%96%B6_%E4%B8%80%E8%A6%A7_.png

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Staging** (`staging.lme.jp`).
- Theo điều tra của AI auto-fixbug: 2 mã trong ticket giải ra id chủ tài khoản `2` (mở được) và `409` (404). Màn login `/aff/v2/login/<mã>` của cả 2 đều hiển thị bình thường — khác biệt chỉ ở bước kiểm tra riêng của màn đăng ký (lọc role 0/1). Chưa dump được cột role của user 409 (DB dev không kết nối được) → kết luận role của user B dựa trên code, chưa xác nhận bằng dữ liệu.
- Màn đăng ký chỉ hiện form khi chủ tài khoản bật cho phép đăng ký affiliater mới; chưa có cấu hình affiliate → hiện thông báo tạm dừng đăng ký (hành vi sẵn có).
- Branch release: `release_step_20260827` (Journal #137186).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Owner mở được (đối chứng) | user A — mã `eaNArJeWyE27` → user id `2` |
| Owner bị 404 | user B — mã `vO3nqdjKW2Z8` → user id `409` |
| URL login | `https://staging.lme.jp/aff/v2/login/<mã>` |
| URL đăng ký | `/affiliate/<mã>/regist` |
| Thời điểm báo lỗi | 2026-07-06 (ticket tạo) |

## Journal / note từ Redmine (nguyên văn)

**Journal #131962 — AI LME Fix bug — 2026-08-21:** — nội dung đánh giá ảnh hưởng đã tách sang `03-dev-impact.md`; phần VERIFY + TỰ REVIEW chép nguyên văn:

```
■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Aff/AffiliateController.php: No syntax errors detected; git diff --stat origin/release_step_20260805...ai_fixbug_38511: đúng 1 file, 2 thêm 3 bớt
   Bằng chứng: Tái hiện trên staging (chỉ GET, read-only): /affiliate/eaNArJeWyE27/regist trả về màn đăng ký (title ASP管理 紹介者（登録）), /affiliate/vO3nqdjKW2Z8/regist trả về trang Page Not Found; 2 mã trong ticket giải ra id chủ tài khoản 2 (mở được) và 409 (404); cả 2 màn đăng nhập /aff/v2/login/<mã> đều hiện bình thường ⇒ khác biệt nằm ở bước kiểm tra riêng của màn đăng ký; DB dev (host.docker.internal:3306) không kết nối được nên không dump được cột role của user 409; kết luận dựa trên đường dẫn code duy nhất dẫn tới trang 404 và đối chiếu các màn cùng luồng

■ TỰ REVIEW (AI)
Sửa đúng root cause và tối thiểu: chỉ bỏ điều kiện lọc loại tài khoản trong 1 bước kiểm tra, giữ nguyên việc chặn mã không hợp lệ (tài khoản không tồn tại vẫn ra 404). Không đụng luồng tạo affiliater, không đổi giao diện, không bump version cấu hình.
 • Rủi ro / lưu ý khi test:
   - Màn đăng ký nay mở được cho cả tài khoản quản trị nội bộ/nhân viên nếu tài khoản đó được chọn làm chủ tài khoản ASP. Rủi ro thấp: API tạo affiliater vốn đã không kiểm tra loại tài khoản nên guard cũ không có tác dụng bảo vệ, và việc bật/tắt đăng ký vẫn do cấu hình của chủ tài khoản quyết định.
   - Chủ tài khoản chưa có cấu hình affiliate sẽ thấy màn báo tạm dừng đăng ký (hành vi sẵn có) — cần chủ tài khoản bật cho phép đăng ký mới thì form mới hiện.

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_38511 (nhánh gốc release_step_20260805, commit c31b07792a, 1 file)  [đã push]
```

**Journal #137186 — Kieu Son Tung — 2026-09-19:**

```
branch release: release_step_20260827
```
