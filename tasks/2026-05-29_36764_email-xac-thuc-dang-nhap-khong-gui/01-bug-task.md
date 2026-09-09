# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36764 — [25-05-2026][11031] Email xác thực (認証メール) khi đăng nhập không gửi đến email` |
| Redmine URL | `https://redmine.watermelon.vn/issues/36764` |
| Auto-filled | `2026-05-29 by /new-task` |
| Ngày báo cáo | `2026-05-26` |
| Khách hàng / PM báo | `AI CSS` |
| Module / Màn hình | `Đăng ký user/Login` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

User: naomi_m0629@hotmail.com
Bot Name: ひなたぼっこ

Khi đăng nhập bằng địa chỉ email, email xác thực (認証メール) không được gửi đến.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B60DA4Q8N

---

### 原文 (JP)
```
メールアドレスにログイン時の認証メールが届かない。
```

**Khách rep (2026-05-28):**
> Không có trong thư mục spam.
> Chỉ từ sau khi thiết lập xác thực hai bước thì đến hiện tại vẫn không nhận được mail mã xác thực, trong khi các mail thông thường vẫn nhận được.
> Trong trường hợp này có nguyên nhân nào có thể xảy ra không ạ?

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: journal #119634 (Kim Cúc) — "Tái hiện case KH" -->

1. Dùng email Microsoft (hotmail), vd: `dinhthikimcuc1710@hotmail.com`.
2. Đăng ký user, lần đầu nhấn đăng ký → không nhận được email.
3. Đăng ký lại qua Edge → có nhận được email; tiếp tục nhấn đăng ký lần 3 → không nhận được.
4. Lặp lại thao tác đăng ký/đăng nhập nhiều lần.

## Expected result

- Mỗi lần đăng ký / đăng nhập, user (kể cả email Microsoft hotmail/outlook/live/msn) đều nhận được email mã xác thực (認証メール).

## Actual result

- Nhấn đăng ký 5 lần thì chỉ nhận được email 2 lần (chập chờn) — mail bị Microsoft chặn/loại bỏ âm thầm khi gửi qua SMTP mặc định.
- Khách (naomi_m0629@hotmail.com): sau khi bật xác thực 2 bước thì không nhận được mail mã xác thực, trong khi mail thông thường vẫn tới.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(Redmine #36764 không có attachment.)

## Ghi chú thêm của Leader

⚠️ Bug tái hiện chập chờn (chỉ với email nhóm Microsoft). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix (ép gửi qua API cho domain Microsoft) + regression các mail giao dịch khác đi qua `MailApiService`.
