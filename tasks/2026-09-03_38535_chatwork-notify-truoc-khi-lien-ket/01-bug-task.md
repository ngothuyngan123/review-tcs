# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38535 — [Stagging][Notify Setting][Chatwork] Chatwork gửi lại các thông báo của sự kiện phát sinh trước khi liên kết Chatwork` |
| Redmine URL | https://redmine.watermelon.vn/issues/38535 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2026-07-07` |
| Khách hàng / PM báo | `Đoàn Thị Bích Hảo` |
| Module / Màn hình | `Notify Setting` (category Redmine) — màn liên kết ChatWork (通知設定 ChatWork連携) |
| Priority | `High` (Redmine priority = High) |
| Môi trường phát hiện | `Staging (staging.lme.jp)` — subject `[Stagging]`, journal 2026-07-09: "e verify trên stg đang thấy vẫn bị" |
| Trạng thái Redmine | `Fix done - Đợi test` · Assignee hiện tại: `Ngô Thúy Ngần` · Commit Date: `2026-08-26` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Pre-conditions:
- Tạo bot mới (id 1160)
- Admin (id = 2) Bật Notify Chatwork = ON.
- Chưa liên kết Chatwork với bot.

Steps:
1. Khi bot chưa liên kết Chatwork, tạo nhiều sự kiện từ phía LINE User (ví dụ: gửi tin nhắn, thực hiện các action phát sinh notify).
2. Xác nhận trong thời điểm này Chatwork chưa nhận được thông báo do chưa liên kết.
3. Thực hiện liên kết Chatwork thành công.
4. Kiểm tra các thông báo được gửi tới Chatwork.

Actual:
4. Ngay sau khi liên kết Chatwork thành công, hệ thống gửi hàng loạt thông báo tương ứng với các sự kiện đã phát sinh trước thời điểm liên kết.

Expected:
4. Sau khi liên kết Chatwork thành công, hệ thống chỉ gửi thông báo cho các sự kiện phát sinh từ thời điểm liên kết trở đi.
Các sự kiện phát sinh trước khi liên kết không được gửi bù (không backlog).

evidence: https://prnt.sc/-u3SVXr5TZny 
=> Note: Tương tự với staff sau khi liên kết chatwork cũng bắn hàng loạt notify trước đó
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

**Pre-conditions:**
- Tạo bot mới (id 1160)
- Admin (id = 2) Bật Notify Chatwork = ON.
- Chưa liên kết Chatwork với bot.

**Steps:**
1. Khi bot chưa liên kết Chatwork, tạo nhiều sự kiện từ phía LINE User (ví dụ: gửi tin nhắn, thực hiện các action phát sinh notify).
2. Xác nhận trong thời điểm này Chatwork chưa nhận được thông báo do chưa liên kết.
3. Thực hiện liên kết Chatwork thành công.
4. Kiểm tra các thông báo được gửi tới Chatwork.

## Expected result

- **Bước 4**: Sau khi liên kết Chatwork thành công, hệ thống chỉ gửi thông báo cho các sự kiện phát sinh từ thời điểm liên kết trở đi. Các sự kiện phát sinh trước khi liên kết **không được gửi bù (không backlog)**.

## Actual result

- **Bước 4**: Ngay sau khi liên kết Chatwork thành công, hệ thống gửi hàng loạt thông báo tương ứng với các sự kiện đã phát sinh **trước** thời điểm liên kết.

## Ảnh / video / log đính kèm

- [x] Có screenshot — link ngoài trong description: https://prnt.sc/-u3SVXr5TZny
- [x] Có video — link ngoài trong journal 2026-07-09: https://screenrec.com/share/mcOoYVDMjF
- [ ] Có log / request-response

> ⚠️ `issue.attachments` = **rỗng** — mọi evidence đều là link ngoài (prnt.sc / screenrec), có nguy cơ hết hạn. Tester nên tải về lưu lại trước khi verify.

## Ghi chú thêm của Leader

**Bug đã bị re-open 2 lần trước bản fix hiện tại** (lịch sử journal Redmine):

| Ngày | Người | Sự kiện |
|---|---|---|
| 2026-07-09 | Thanh Duy Nguyen | done_ratio 0 → 100 (báo fix xong lần 1) |
| 2026-07-09 | Đoàn Thị Bích Hảo | **Re-open lần 1** — "a check lại giúp em ạ, e verify trên stg đang thấy vẫn bị ạ (9/7)" — evidence https://screenrec.com/share/mcOoYVDMjF |
| 2026-07-30 | Tuan PA | Chuyển lại `Fix done - Đợi test` (fix lần 2) |
| 2026-08-20 | Đoàn Thị Bích Hảo | **Re-open lần 2** — "bug này vẫn bị đối với trường hợp đầu tiên => khi liên kết bot vẫn push 1 loạt các notify trước đó" |
| 2026-08-26 | AI LME Fix bug | Fix lần 3 bằng **Auto-fixbug LME**, branch `ai_fixbug_38535` → `Fix done - Đợi test` |

→ **Trọng tâm test**: kịch bản re-open 2026-08-20 = **"trường hợp đầu tiên"** — người dùng **chưa từng có bản ghi cấu hình thông báo** cho bot (nhánh tạo mới), đây là nhánh 2 lần fix trước bỏ sót. Xem `REQ-002` trong `04-tc-list.md`.

**Ghi chú mở rộng phạm vi từ description**: "Tương tự với **staff** sau khi liên kết chatwork cũng bắn hàng loạt notify trước đó" → TC phải cover **cả admin lẫn nhân viên** (Dev xác nhận cả hai đi qua cùng màn liên kết).
