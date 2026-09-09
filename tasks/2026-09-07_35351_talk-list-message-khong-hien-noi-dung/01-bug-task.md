# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#35351 — [Talk-list] Một số message không hiển thị được nội dung` |
| Module / Màn hình | Chat / Talk Management (FA-002) — màn **Danh sách hội thoại 「チャット管理」** (`SCR-TLK-01`) + **Modal chi tiết tin nhắn** (`SCR-TLK-02`) |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ **Trường `description` của Redmine #35351 TRỐNG HOÀN TOÀN** (0 ký tự). Toàn bộ nội dung bug bên dưới lấy từ **tiêu đề ticket + journal điều tra** của người báo (Thanh Phương), giữ nguyên văn tiếng Việt gốc — KHÔNG diễn giải thêm.

Trên màn **Talk-list** (Danh sách hội thoại 「チャット管理」), **một số message không hiển thị được nội dung** — ô nội dung bị trắng.

Diễn tiến ghi nhận qua 2 lần check của người báo:

1. **(2026-04-13)** "Đã sửa message text của salon, lesson, remind có hiển thị được nội dung. Check vẫn còn **1 số message không hiển thị được** cần check lại." → tức là sau 1 vòng fix trước đó, các message text của **salon / lesson / remind** đã hiển thị được, nhưng **vẫn còn nhóm message khác bị trắng**.
2. **(2026-04-13)** "**Modal detail: message sticker không hiển thị được nội dung**" → triệu chứng thứ hai, nằm ở **popup chi tiết tin nhắn**, với tin loại **nhãn dán (sticker)**.

→ Ticket gồm **HAI triệu chứng riêng biệt**:
- **(a)** Cột nội dung **ngoài danh sách hội thoại** bị trắng với một số loại message.
- **(b)** **Modal chi tiết** không hiển thị được nội dung tin nhãn dán (sticker).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — description trống. Người báo chỉ đính kèm screenshot. -->

1. *(Không có trong ticket — xem screenshot đính kèm bên dưới)*
2.
3.

## Expected result

- *(Không có trong ticket)*

## Actual result

- Cột nội dung của một số message trên Talk-list hiển thị **trắng** (theo screenshot `2026_04_13_12_06_58_Window.png`).
- Modal chi tiết của message **sticker** không hiển thị được nội dung (theo screenshot `2026_04_13_12_24_12_Window.png`).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/24585/2026_03_24_15_53_00_%E3%83%81%E3%83%A3%E3%83%83%E3%83%88%E7%AE%A1%E7%90%86.png — `2026_03_24_15_53_00_チャット管理.png` (ảnh gốc lúc tạo ticket 2026-03-24)
- https://redmine.watermelon.vn/attachments/download/25140/2026_04_13_12_06_58_Window.png — `2026_04_13_12_06_58_Window.png` (kèm journal #116521 — message còn trắng ở danh sách)
- https://redmine.watermelon.vn/attachments/download/25142/2026_04_13_12_24_12_Window.png — `2026_04_13_12_24_12_Window.png` (kèm journal #116534 — modal detail sticker)

## Ghi chú thêm của Leader

- ⚠️ **Bug KHÔNG có steps tái hiện trong Redmine** — `description` trống, không có section "Tái hiện bug", không có Expected/Actual do người báo ghi. Root cause đã được Dev/AI confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). **TCs nên tập trung verify cách fix + regression impact**, và dựa vào 3 screenshot đính kèm để suy ra hiện trạng.
- ⚠️ **Ticket đã qua NHIỀU vòng fix** — không phải fix 1 lần:
  - Vòng trước 2026-04: đã sửa message text của salon / lesson / remind (người báo confirm ở journal #116521) → **vùng này là regression cũ, phải verify lại không hỏng**.
  - PR human `#10057` (bitbucket, journal #116805 — 2026-04-16) trên nhánh dev `BugTester_35351_talklist_T4_2026`.
  - **AI auto-fixbug đợt 1** — 2026-08-28, commit `f424bda154`, 3 file.
  - **AI auto-fixbug đợt 2** — 2026-09-05, commit `2b3402c7a6` (bản mới nhất, đang chờ test).
- 🔴 **Đợt 2 là thay đổi CÓ ẢNH HƯỞNG HÀNH VI** (chính AI ghi trong journal #134561): sau khi lên, **màn danh sách ở trạng thái mặc định sẽ có thêm nhóm tin gửi bằng mẫu tin / hành động / hẹn giờ vốn trước nay CHƯA TỪNG xuất hiện**, nên **số dòng và phân trang sẽ đổi**. Cần Leader/PO xác nhận đây đúng là mong muốn trước khi kết luận Đạt.
- ⚠️ **Xung đột nhánh**: nhánh dev `BugTester_35351_talklist_T4_2026` (PR #10057) sửa **cùng vùng code** với `ai_fixbug_35351`. Nếu PR đó được merge sau sẽ xung đột — người review phải quyết định lấy bản nào.
- ⚠️ **Fix chưa được verify bằng mắt / bằng dữ liệu thật** — AI ghi rõ: MySQL dev `host.docker.internal:3306` báo `Connection refused`, mức verify chỉ là `lint`.
- **Môi trường phát hiện**: ticket KHÔNG ghi rõ env (Production / Staging / Dev). Screenshot có tiêu đề 「チャット管理」 nhưng không đủ để xác định env — cần hỏi lại người báo nếu TC cần chốt env.
- **Tần suất**: ticket không ghi. Theo mô tả root cause (điều kiện `v-if` sai logic, thiếu nhánh `displayType` cho loại 16/18) thì lỗi mang tính **deterministic 100%** theo loại tin, không phải xác suất.
- **Tracker** = `Bug tự detect` (đổi từ tracker cũ ở journal #120885), **Status hiện tại** = `Fix done - Đợi test`, assignee = Ngô Thúy Ngần.

## Journal / note từ Redmine (nguyên văn)

**Journal #116521 — Thanh Phương — 2026-04-13:**

```
1. Đã sửa message text của salon, lesson, remind có hiển thị được nội dung. Check vẫn còn 1 số message không hiển thị được cần check lại
```

**Journal #116534 — Thanh Phương — 2026-04-13:**

```
2. Modal detail: message sticker không hiển thị được nội dung
```

**Journal #116805 — Nga Vũ Thị — 2026-04-16:**

```
https://bitbucket.org/snstool/sns-line/pull-requests/10057/diff
```

**Journal #131658 — Nga Vũ Thị — 2026-08-21:**

```
Dev done
```

> 2 journal còn lại (#133410 — 2026-08-28, #134561 — 2026-09-05) là **báo cáo AI auto-fixbug** → đã chép nguyên văn sang [03-dev-impact.md](03-dev-impact.md), không lặp lại ở đây.
