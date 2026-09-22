# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38537 — [Salon] Tạo lịch làm việc từ 19h-00 giờ, ở app hiển thị O cả ngày hôm sau` |
| Module / Màn hình | Salon Booking (FA-020) — **app mobile LME (phía admin)**: màn Calendar → xem lịch làm việc. Web admin (tab 「予約カレンダー」) là vùng **regression**, không phải nơi phát sinh lỗi. |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Trường `description` của Redmine #38537 **để trống**. Nội dung dưới lấy từ **Journal #126414 (Kim Cúc — 2026-07-16)** và **làm rõ bởi human ngày 2026-09-16**: bug nằm ở **phía app mobile**.

Tạo lịch làm việc cho salon với khung giờ **19:00–00:00** (ca kết thúc sát cuối ngày, đúng nửa đêm). Khi xem lịch làm việc trên **app mobile**, ngày hôm sau cũng bị hiển thị **O** (có lịch làm việc) dù thực tế ngày hôm sau không có ca làm nào.

## Steps to reproduce

1. Tạo lịch làm việc từ **19:00 – 00:00** ngày **18/9/2026** (lịch làm việc sát với cuối ngày).
2. Trên **app mobile** vào **Calendar** → vào **xem lịch làm việc**.

<!-- Bước tái hiện do human cung cấp 2026-09-16. Bản gốc trên Redmine (Journal #126414) dùng ngày 16/7/2026 → 17/7/2026, cùng thao tác. -->

## Expected result

- Ngày **18/9/2026** hiển thị **O** (có ca làm 19:00–00:00).
- Ngày **19/9/2026** **KHÔNG** hiển thị O — ca kết thúc đúng nửa đêm nằm trọn trong ngày 18/9, không được tách sang hôm sau.
- Web admin hiển thị lịch làm việc **không bị ảnh hưởng** bởi bản fix.

<!-- ⚠️ Redmine KHÔNG ghi rõ expected. Nội dung trên suy từ tiêu đề ticket + mục 1 "Nguyên nhân" (file 03) + chỉ đạo của human 2026-09-16 — Leader verify lại. -->

## Actual result

- Trên app mobile, màn calendar hiển thị **O** (có lịch làm việc) lan sang **cả ngày 19/9/2026**.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- Screenshot_14.png — https://redmine.watermelon.vn/attachments/download/27876/Screenshot_14.png

## Ghi chú thêm của Leader

- **Làm rõ của human (2026-09-16)**: bug ở **phía app mobile**. TC phải tập trung vào **hiển thị lịch làm việc trên app mobile với nhiều kiểu lịch làm việc khác nhau**, kèm **regression hiển thị lịch làm việc trên web** không bị ảnh hưởng.
- **Redmine description trống** — mọi thông tin bug + đánh giá ảnh hưởng nằm trong 3 journal (#125237, #126414, #127213).
- Status Redmine hiện tại: **Fix done - Đợi test** (cập nhật 2026-08-19). Tracker: **Bug tự detect**.
- **Fix do AI Auto-fixbug LME thực hiện** (journal #125237), branch `ai_fixbug_38537` trên repo `sns-line`. Journal #127213 (Thinh Nguyen) ghi thêm: **App sửa trên commit `2c6c861d` nhánh `master_branch_release_store`** → có **2 nơi chạm code**, cần xác nhận bản đang test chứa đủ cả 2.
- Dev tự ghi nhận **không kiểm chứng được parent ticket #26684** (ticket rất cũ, offline) → coi như đã đóng/release. Rủi ro giả định này cần Leader verify.
- Bug liên quan **biên nửa đêm** → khi test phải chú ý timezone (JST) và các biên cuối tuần / cuối tháng / cuối năm.
- **Link test case của QA** (Journal #126414): https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1366329610 — sheet `#38520`. Redmine **không ghi `Row: <start>-<end>`** và MCP `google-sheets` lỗi kết nối → file `04-tc-list.md` lấy từ **MCP LME TEST STUDIO** thay thế.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<không có trong ticket>` |
| Friend | `<không có trong ticket>` |
| Đối tượng cấu hình | Ca làm salon 19:00–00:00 ngày 16/7/2026 (bảng `calendar_salon_time_booking`) |
| Thời điểm lỗi | Ngày có ca: `2026/07/16` — ngày hiển thị sai: `2026/07/17` |
| Đối chứng | Ca **qua đêm thật** (vd `20:00–02:00`) vẫn phải tạo ca hôm sau `00:00–02:00` → ngày hôm sau hiển thị O là ĐÚNG |
| Bản ghi mẫu (DB dev, từ Journal #125237) | `calendar_salon_time_booking` id `14580` (20:00–00:00), id `14576` (19:30–00:00) |

## Journal / note từ Redmine (nguyên văn)

**Journal #125237 — AI LME Fix bug — 2026-07-08:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
(nội dung đầy đủ 6 mục đã chép nguyên văn vào 03-dev-impact.md — không lặp lại ở đây)
```

**Journal #126414 — Kim Cúc — 2026-07-16:**

```
Thao tác tái hiện:
1. Tạo lịch làm việc từ 19:00-00:00 ngày 16/7/2026( lịch làm việc sát với cuối ngày)
Hiện tượng: Check ở app màn calendar hiển thị O có lịch làm việc sang cả ngày 17/7/2026

Link test case:
https://docs.google.com/spreadsheets/d/1SojySaGybmKs6knh32-sXmsoPV1Yje3a0dzW5we0L8s/edit?gid=1366329610#gid=1366329610
sheet: #38520
```

**Journal #127213 — Thinh Nguyen — 2026-07-27:**

```
App sửa trên commit 2c6c861d nhánh master_branch_release_store
```
