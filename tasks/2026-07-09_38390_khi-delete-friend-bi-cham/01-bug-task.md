# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38390 — Khi delete friend bị chậm` |
| Redmine URL | https://redmine.watermelon.vn/issues/38390 |
| Auto-filled | `2026-07-09 by /new-task` |
| Ngày báo cáo | `2026-07-01` |
| Khách hàng / PM báo | `Do Van Tu TuDV` (tracker: Bug tự detect; repro bổ sung bởi Kim Cúc) |
| Module / Màn hình | `Friend List (FA-013) — Xóa/Chặn bạn (web) / Friend Information (FA-015) — Xóa bạn (APP)` |
| Priority | `Medium` (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — mặc định Staging (staging.lme.jp)>` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

⚠️ Redmine description **trống**. Bug thuộc tracker "Bug tự detect". Nội dung tái hiện lấy từ note QA (Kim Cúc, 2026-07-09) — xem Steps + Actual bên dưới.

Hiện tượng: thao tác xóa friend (đặc biệt line user có nhiều data ở bảng `url_shorten_detail`) bị **chậm / load mãi** ở màn xóa.

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

1. Line user có nhiều data, có data ở bảng `url_shorten_detail`
2. Xóa friend info

## Expected result

-

## Actual result

- Bị chậm, load mãi ở màn xóa

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

## Ghi chú thêm của Leader

⚠️ Bug performance (không phải sai chức năng). Root cause đã được Dev/AI confirm qua đánh giá ảnh hưởng (file 03): câu DELETE short-url dùng `whereIn('url_id', [~16.000 id])` gây chậm. TCs nên tập trung: (1) verify thao tác xóa nhanh sau fix, (2) **regression tính đúng đắn cascade delete** — đúng tập bản ghi bị xóa ở 4 điểm (3 web + 1 app/API), đặc biệt case xóa/chặn hàng loạt (liên quan regression #38473 — sót dọn link friend không đứng đầu).
