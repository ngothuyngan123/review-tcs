# 01 — Bug Task từ khách hàng

> Auto-filled từ Redmine #36428 bởi `/new-task`. Tester verify lại các field bên dưới rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#36428 — [15-05-2026][回答ID：28184][Form] Form "初回アンケート" hiển thị "0 người trả lời" nhưng vào "表示" thì có data thực` |
| Redmine URL | https://redmine.watermelon.vn/issues/36428 |
| Auto-filled | 2026-05-18 by /new-task |
| Ngày báo cáo | 2026-05-15 |
| Khách hàng / PM báo | AI CSS |
| Module / Màn hình | Form (各種設定 — tab setting số 5 của form) |
| Priority | Medium (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không nêu rõ env) |

## Mô tả bug (nguyên văn từ khách hàng)

User: rameruzo@mama3.org
Bot Name: クラブ虹【公式】

Khách báo: trên form "初回アンケート" (Khảo sát ban đầu), thông tin trả lời hiển thị là "0人" (0 người), nhưng khi nhấn "表示" (Hiển thị) thì lại thấy có dữ liệu trả lời tồn tại.

→ Có vẻ count tổng response và data thực tế không khớp — cần điều tra logic đếm respondent.

---
Nội dung gốc (JP):
フォーム作成：初回アンケート
回答情報は「0人」と表示されているが、「表示」を押すと回答情報が存在している。

[Đính kèm 2 file: F0B3ZALUZL2, F0B3X8LEA06 — xem Slack permalink]

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B3VUMP3MK

---

### 原文 (JP)
```
フォーム作成：初回アンケート
回答情報は「0人」と表示されているが、「表示」を押すと回答情報が存在している。
```

<!-- TaskRef: user_report:Rec0B3VUMP3MK -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> Trích từ note journal Kim Cúc (2026-05-18) — Section "Tái hiện case KH":

1. User trả lời form
2. Admin thực hiện nhấn save ở màn setting tab số 5 (chỉ nhấn save k cần setting gì cả)

## Expected result

- Màn list count đúng số lượng user đã trả lời form (count_user_reply giữ nguyên giá trị mới nhất sau khi user submit).

## Actual result

- Ở màn list **không count** số lượng user trả lời form (hiển thị "0人" mặc dù đã có user submit).

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

Attachments từ Redmine:
- https://redmine.watermelon.vn/attachments/download/25759/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-15%2011.23.41.png
- https://redmine.watermelon.vn/attachments/download/25760/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-05-15%2011.23.35.png

## Ghi chú thêm của Leader

- Note bổ sung từ Ngọc Ánh (2026-05-17): nội dung inquiry mô tả ban đầu là "form đã cài giới hạn 1 lần trả lời, nhưng ngay cả khi user chưa trả lời thì vẫn hiển thị text giới hạn → không trả lời được". Theo KH, trước bản update chức năng vẫn hoạt động bình thường. → Tester cần verify cả 2 framing: (a) count_user_reply bị reset sai về data cũ → khiến số trả lời hiển thị 0; (b) hệ quả là form check "đã trả lời rồi" sai → block user trả lời lần đầu.
- Assigned dev: Kieu Son Tung. Eval dev do Kim Cúc submit.
