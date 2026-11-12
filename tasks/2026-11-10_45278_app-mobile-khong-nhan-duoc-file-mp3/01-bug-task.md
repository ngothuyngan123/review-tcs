# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45278 — App mobile không nhận được file MP3` |
| Module / Màn hình | `Chat 1:1 — audio player trên app mobile LME (file MP3 nhận từ LINE)` |

## Mô tả bug (bản dịch tiếng Việt)

1/ App mobile không nhận được file MP3
App mobile LME: Không nhận được tin nhắn do lỗi phía LINE Official Account.
Trên browser: Nhận bình thường.

2/ Dung lượng MP3 hiển thị sai trên browser
Dung lượng MP3 bản browser — có lẽ thiếu dấu thập phân, nên hiển thị KHÔNG ĐÚNG.
=> đưa vào đợt sửa nhẹ (軽微修正) lần tới.

Link Chatwork thảo luận: https://www.chatwork.com/#!rid247704373-2170379964204331008

<!-- Section A "Tái hiện bug" lấy từ Journal #153503 (Ngọc Ánh) bên dưới. -->

## Steps to reproduce

1. Gửi file mp3 từ phía LINE (friend gửi file mp3 tới bot).

## Expected result

- Hiển thị/phát được file mp3.

## Actual result

- Tin nhắn gửi từ LINE của phía user không hiển thị/phát được file mp3.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.melonglobal.net/attachments/download/38625/fcc0f972-7e86-4223-b58b-efb671c68a86.png

## Ghi chú thêm của Leader

- Bug chỉ xảy ra trên **app mobile LME** (iOS/Android) — trên browser nhận bình thường.
- Issue #45278 gộp 2 nội dung: (1) **bug chính** app mobile không nhận/phát được MP3 từ LINE — fix lần này; (2) **bug phụ** dung lượng MP3 hiển thị sai trên browser (thiếu dấu thập phân) — Dev ghi rõ **dời sang đợt sửa nhẹ (軽微修正) lần tới**, KHÔNG thuộc phạm vi fix hiện tại → không đưa vào scope coverage/TC của task này.
- Status hiện tại: `Fix done - Đợi test`.

## Journal / note từ Redmine (nguyên văn)

**Journal #153502 — Thinh Nguyen — 2026-11-10:**

```
---Mobile---
Nguyên nhân: check data API trả thì link file là đuôi dạng .mpeg3 không phải đuôi file chuẩn trình phát audio trên app không play được loại file này

Hướng sửa: Copy file sang dạng đuôi đúng .mp3 để play được trên trình phát mobile

File sửa: audio_player_screen.dart, chat_item.dart

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ thêm logic copy file sang dạng đúng .mp3

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover

Điểm cần test: Phần view file audio có đuôi .mpeg3
```

**Journal #153503 — Ngọc Ánh — 2026-11-10:**

```
Tái hiện bug: gửi file mp3 từ phía Line
Actual: tin nhắn gửi từ Line của phía user không hiển thị/phát được file mp3
Expect: hiển thị/phát được file mp3
```
