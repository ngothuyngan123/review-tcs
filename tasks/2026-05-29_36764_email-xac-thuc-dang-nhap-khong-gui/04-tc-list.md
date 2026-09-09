<!-- sync-target: https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=2035099260#gid=2035099260 -->

# 04 — TC List (fetched từ Sheet master)

> ⚠️ **TCs này fetch từ Sheet master — read-only.** KHÔNG sửa Title/Expected dù bug fix đổi behavior. Nếu cần chỉnh, confirm với Leader trước.
>
> **Lưu ý format:** Tab "Send email" KHÔNG dùng format 10 cột chuẩn template. Đây là format phân cấp gốc của team (Assign / Main Function / Sub1-5 / Expect Result / Test Result / Note). Giữ NGUYÊN cấu trúc cột gốc. Ô trống = cell merge với row trên (Main Function trải dài nhiều dòng).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | `https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=2035099260#gid=2035099260` (tab "Send email", line 2~29) |

---

## Context từ Sheet (line 2~3 — KHÔNG phải TC)

- **Line 2** = nguyên văn "Đánh giá ảnh hưởng phía dev" → đã map sang `03-dev-impact.md`.
- **Line 3** = "Tái hiện case KH" → đã map sang `01-bug-task.md` (Steps to reproduce).

## TC List (line 4~29)

| Assign | Main Function | Sub1 | Sub2 | Sub3 | Sub4 | Sub5 | Expect Result | Test Result | Note |
|---|---|---|---|---|---|---|---|---|---|
| | Đăng ký tài khoản<br>Đăng ký user thường | hotmai: dinhthikimcuc1710@hotmail.com | check khi đăng ký ở browser chorme | | | | - user có nhận được email<br>- user đăng ký qua thành công | OK | |
| | | | check khi đăng ký ở browser chorme ở mac | | | | | OK | |
| | | | check khi đăng ký ở browser safari | | | | | OK | |
| | | | check khi đăng ký ở browser Edge | | | | | OK | |
| | | | check khi đăng ký ở browser Firebox | | | | | OK | |
| | | | Check khi thao tác đăng ký liền tục | đăng ký lần 1 => user đã nhận được email<br>=> tiếp tục nhấn vào đăng ký | | | - user có nhận được email<br>- user đăng ký qua thành công | OK | |
| | Đăng ký tài khoản<br>Đăng ký có affliate | hotmai: dinhthikimcuc1710@hotmail.com | check khi đăng ký ở browser chorme | | | | - user có nhận được email<br>- user đăng ký qua thành công | OK | |
| | | | check khi đăng ký ở browser chorme ở mac | | | | | OK | |
| | | | check khi đăng ký ở browser safari | | | | | OK | |
| | | | check khi đăng ký ở browser Edge | | | | | OK | |
| | | | check khi đăng ký ở browser Firebox | | | | | OK | |
| | | | Check khi thao tác đăng ký liền tục | đăng ký lần 1 => user đã nhận được email<br>=> tiếp tục nhấn vào đăng ký | | | - user có nhận được email<br>- user đăng ký qua thành công | OK | |
| | Gửi mail mã xác thực khi đăng nhập / xác thực 2 bước (認証メール) | user đang đang nhập ở trên các browser khác nhau | check khi đăng nhập ở browser chorme | | | | - user có nhận được email xác thực 2 bước để login<br>- login thành công | OK | |
| | | | check khi đăng nhập ở browser chorme ở mac | | | | | OK | |
| | | | check khi đăng nhập ở browser safari | | | | | OK | |
| | | | check khi đăng nhập ở browser Edge | | | | | OK | |
| | | | check khi đăng nhập ở browser Firebox | | | | | OK | |
| | | | Check khi thao tác login liền tục | | | | | OK | |
| | Mail đặt lại mật khẩu (ResetPassword) | user đang đang nhập ở trên các browser khác nhau | check khi đăng nhập ở browser chorme | | | | - user có nhận được email để reset password<br>- đổi mật khâu thành công | OK | |
| | | | check khi đăng nhập ở browser chorme ở mac | | | | | OK | |
| | | | check khi đăng nhập ở browser safari | | | | | OK | |
| | | | check khi đăng nhập ở browser Edge | | | | | OK | |
| | | | check khi đăng nhập ở browser Firebox | | | | | OK | |
| | | | Check khi thao tác login liền tục | | | | | OK | |
| | Mail thông báo thanh toán tự động | | | | | | | | |
| | Các mail giao dịch khác đi qua MailApiService (cập nhật số tài khoản, cấp quyền staff, BotController) | | | | | | | | |

---

## Member tự check trước khi review

> ⚠️ Quan sát coverage (Leader verify ở `/review-tc`): TCs hiện chỉ test **1 domain** `hotmail.com`. Fix cover 7 domain Microsoft (hotmail.com, hotmail.co.jp, outlook.com, outlook.jp, live.com, live.jp, msn.com) + luồng cũ cho domain ngoài nhóm. 2 dòng cuối (Mail thanh toán tự động, mail giao dịch khác) chưa có sub-step / kết quả.

<!-- Source: fetched từ Redmine #36764 Link TCs, range A2:J29 tab "Send email" lúc 2026-05-29. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
