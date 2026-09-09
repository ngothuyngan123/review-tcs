# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39742 — Action khi mở page ở formanwer, bill tiền => thêm param vào url sau khi action xong` |
| Redmine URL | https://redmine.watermelon.vn/issues/39742 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2026-08-19` |
| Khách hàng / PM báo | `Kieu Son Tung` |
| Module / Màn hình | `Khác` (category Redmine) — theo mục 4.3 của Dev: Form Builder (FA-011) · Single Product / Sales (FA-026) · Action Settings (SC-004) |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>` |

**Metadata thêm (không có trong template — giữ để Leader tham chiếu):**

| Trường | Giá trị |
|---|---|
| Tracker | `Triển khai ngang` — **KHÔNG phải bug report từ khách**, mà là ticket port cách fix có sẵn sang nhánh release |
| Status hiện tại | `Fix done - Đợi test` |
| Assigned to | `Thanh Phương` |
| Project | `Lme` |
| Commit Date (custom field) | `2026-08-19` |
| Updated on | `2026-08-27` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description từ Redmine #39742. KHÔNG diễn giải lại. -->

```
Action khi mở page ở formanwer, bill tiền => thêm param vào url sau khi action xong
Tham khảo branch improve-action-open-link
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine #39742 KHÔNG có section "Tái hiện bug". Để trống theo đúng nguồn. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> `issue.attachments` rỗng — Redmine #39742 không đính kèm file nào.
> Evidence duy nhất nằm ở **LME TEST STUDIO** (task #171): trace + video của bug #40150,
> path `465/tc-12247/trace.zip` và `465/tc-12247/page_f3990bdec037de418884d8e27ad952c6.webm`.

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — description chỉ có 1 dòng tiêu đề + 1 dòng trỏ branch tham khảo, không có Steps / Expected / Actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). **TCs nên tập trung verify cách fix + regression impact**, không cố dựng lại repro từ ticket.

⚠️ **Đây là ticket "Triển khai ngang", không phải bug do khách báo.** Bản chất: cách fix đã tồn tại ở nhánh `improve-action-open-link` nhưng **chưa bao giờ được merge lên nhánh release đang dùng**, nên cả 2 màn (form answer + bill tiền) trên release vẫn còn lỗi. Rủi ro đặc thù của loại ticket này: **port thiếu chỗ** — Dev đã tự chốt phạm vi đúng 2 chỗ bằng cách tra schema DB (chỉ có `form_answer.action_open_id` và `s_items.action_show_page_id`), điểm này cần Leader thẩm định lại ở bước review.

⚠️ **Fix do AI Auto-fixbug thực hiện** (journal 2026-08-19 của user `AI LME Fix bug`), không phải Dev người viết. Nhánh `ai_fixbug_39742`, commit `afe26df872`, 7 file. Mức verify Dev tự chạy mới chỉ là **lint** (`php -l` / `node --check`) — **chưa chạy test chức năng**, và Dev ghi rõ **KHÔNG query được DB dev** (MySQL `host.docker.internal:3306` Connection refused) nên **không tự đếm được dữ liệu thật**.

⚠️ **Liên quan bill tiền** → theo **RULE-08**, kết luận không được rút ra từ local/staging. Xem cảnh báo môi trường ở `04-tc-list.md`.
