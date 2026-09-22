# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40336 — [Menu] Sau khi change status thì số barge (cạnh chữ 1:1チャット) đang không update luôn - phải reload mới update` |
| Module / Màn hình | Chat / Talk Management — màn 管理 danh sách hội thoại (talk list) + badge số hội thoại chưa xác nhận cạnh menu `1:1チャット` ở sidebar |

## Mô tả bug (bản dịch tiếng Việt)

Ở màn talk list (quản lý hội thoại), sau khi đổi trạng thái hội thoại sang đã xác nhận (confirm), số badge hiển thị cạnh chữ `1:1チャット` (1:1 chat) trên menu **không update ngay** — phải reload lại trang mới thấy số mới.

Exp (nguyên văn ticket): Update luôn mà k cần reload page.

Video tái hiện: https://drive.google.com/file/d/1ZOIszyI86YBXOKnjsGI9uJIf4WNc0aZu/view?usp=sharing

## Steps to reproduce

<!-- Nguồn: Journal #133469 — Do Van Tu TuDV — 2026-08-28 (description gốc chỉ có 1 dòng Exp + link video). -->

1. Vào màn hình talk list (danh sách hội thoại / quản lý chat).
2. Đổi trạng thái của 1 hội thoại sang **confirm** (đã xác nhận).
3. Quan sát số badge cạnh chữ `1:1チャット` trên menu sidebar.

## Expected result

- Số badge cạnh `1:1チャット` update ngay sang số hội thoại chưa xác nhận (unconfirm) mới nhất, **không cần reload page**.

## Actual result

- Số badge giữ nguyên giá trị cũ; chỉ khi reload trang mới hiển thị số đúng.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video
- [ ] Có log / request-response

- Video (Google Drive, do người báo bug dán trong description): https://drive.google.com/file/d/1ZOIszyI86YBXOKnjsGI9uJIf4WNc0aZu/view?usp=sharing
- Attachment Redmine: không có (0 file đính kèm trực tiếp trên ticket).

## Ghi chú thêm của Leader

- Redmine attachment trống — video nằm trên Google Drive, cần quyền truy cập Drive để xem.
- Ticket **không ghi** môi trường phát hiện, tần suất lỗi, account test → `Input thiếu`, hỏi lại người báo nếu cần dựng ca lỗi gốc.
- Fix do **AI Auto-fixbug** thực hiện (Journal #136323), là **đợt sửa thứ hai** theo yêu cầu human: ngoài fix gốc còn **refactor gộp logic badge của 2 màn thành 1 helper dùng chung** → phạm vi lan sang màn **chat 1:1 (FA-001)** vốn đang chạy ổn. Xem file `03-dev-impact.md`.
- Không có ca lỗi định danh cụ thể (không có bot_id / friend ID / thời điểm lỗi trong ticket) → bỏ section "Dữ liệu định danh ca lỗi".

## Journal / note từ Redmine (nguyên văn)

**Journal #133469 — Do Van Tu TuDV — 2026-08-28:**

```
- Vào màn hình talk list change trạng thái confirm  số barge (cạnh chữ 1:1チャット) đang không update luôn
=> expect update số unconfirm mới nhất
```

<!-- Journal #136323 (AI LME Fix bug — 2026-09-14) là báo cáo đánh giá ảnh hưởng → đã chép nguyên văn vào 03-dev-impact.md. -->
