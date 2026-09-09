# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#28450 — [Salon] [List course] Sau khi copy course => Chưa add id course vào những staff đã select all course trước đó` |
| Redmine URL | https://redmine.watermelon.vn/issues/28450 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2025-02-25` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set category, không có custom field. Gợi ý từ subject: Lịch salon → màn danh sách khóa "List course") |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ>` (description không ghi env; báo cáo fix ghi "Không tái hiện được trên dev") |

### Thông tin bổ sung từ Redmine (ngoài template)

| Trường | Giá trị |
|---|---|
| Project | Lme |
| Tracker | Bug tự detect |
| Status | Fix done - Đợi test |
| Assigned to | Ngô Thúy Ngần |
| Parent issue | #26684 |
| Created / Updated | 2025-02-25 / 2026-08-26 |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Staff có is_all_course = 1
Sau khi copy tạo ra course mới chưa insert id course vào calendar_salon_staff.course_ids

=> Expect: Logic Giống case tạo mới course => Insert course_ids cho những staff có is_all_course = 1

https://redmine.watermelon.vn/attachments/download/17296/course1.png
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" / "Steps to reproduce" → để trống theo quy tắc /new-task. -->

1.
2.
3.

## Expected result

<!-- Không có section "Tái hiện bug" tách riêng. Xem dòng "=> Expect: ..." trong "Mô tả bug" phía trên. -->

-

## Actual result

<!-- Không có section "Tái hiện bug" tách riêng. Xem 2 dòng đầu của "Mô tả bug" phía trên. -->

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

| # | File | URL |
|---|---|---|
| 1 | salon-1.png (attachment của issue) | https://redmine.watermelon.vn/attachments/download/20977/salon-1.png |
| 2 | course1.png (link trong description) | https://redmine.watermelon.vn/attachments/download/17296/course1.png |

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — Redmine không có section "Tái hiện bug" theo format chuẩn (Steps / Expected / Actual để trống). Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

Điểm cần lưu ý khi dựng test:

- Description có sẵn dòng `=> Expect:` — đây là expected result gốc do người báo bug ghi, đã giữ nguyên văn trong "Mô tả bug".
- Bug được fix bởi **hệ thống Auto-fixbug LME (AI)**, không phải dev người — xem journal 2026-08-26 trong file `03-dev-impact.md`.
- Báo cáo fix ghi rõ **không tái hiện được trên dev** (MySQL `host.docker.internal:3306` Connection refused) → bug xác định bằng đối chiếu code 2 nhánh (tạo mới vs copy), **chưa có bằng chứng chạy thực tế trên môi trường có DB**.
- Có **RECOVER DATA**: các khóa đã copy TRƯỚC fix vẫn thiếu id trong `calendar_salon_staff.course_ids` — fix không tự vá dữ liệu cũ.
