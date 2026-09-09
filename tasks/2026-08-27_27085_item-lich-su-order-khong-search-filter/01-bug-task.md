# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#27085 — [Item] [Lịch sử order] Nếu đang ở một page khác page 1 thì không search được cũng không filter được` |
| Redmine URL | https://redmine.watermelon.vn/issues/27085 |
| Auto-filled | `2026-08-27 by /new-task` |
| Ngày báo cáo | `2024-11-01` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `Item / Lịch sử order (販売履歴)` — suy từ prefix subject Redmine `[Item] [Lịch sử order]`; Redmine không set category/custom field |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi>` |

### Trạng thái Redmine (tại thời điểm fetch 2026-08-27)

| Trường | Giá trị |
|---|---|
| Tracker | `Bug tự detect` |
| Status | `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |
| Cập nhật gần nhất | `2026-08-26T04:33:08Z` (journal AI Auto-fixbug) |
| Attachments | `0` |
| Relations | `không có` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
1. Vào MH lịch sử order
2. Click vào page 2
3. Nhập tên friend/ tên item/ order ID => Click search 
=> BUG: Không search được

1. Vào MH lịch sử order
2. Click vào page 2
3. Click button filter và tiến hành filter theo trạng thái bill
=> BUG: Không filter được
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

**Luồng 1 — Search:**
1. Vào MH lịch sử order
2. Click vào page 2
3. Nhập tên friend / tên item / order ID => Click search

**Luồng 2 — Filter:**
1. Vào MH lịch sử order
2. Click vào page 2
3. Click button filter và tiến hành filter theo trạng thái bill

## Expected result

- `<Redmine KHÔNG ghi expected — tester fill>`
- Tham chiếu mục 1 của [03-dev-impact.md](03-dev-impact.md): Dev mô tả hành vi đúng là danh sách phải nạp lại **từ trang 1** sau khi đổi điều kiện lọc.

## Actual result

- Luồng 1: `=> BUG: Không search được`
- Luồng 2: `=> BUG: Không filter được`
- (Theo phân tích của Dev ở file 03: thực chất request vẫn kèm số trang cũ → server trả trang 2 rỗng → bảng trắng + thanh phân trang biến mất, người dùng **tưởng** là không search/filter được.)

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue #27085 **không có attachment nào** (`attachments = 0`).

## Ghi chú thêm của Leader

- **Tiền điều kiện bắt buộc để tái hiện**: bot phải có **> 20 order** ở tab đang test để danh sách có ≥ 2 trang (server phân trang 20 bản ghi/trang), và điều kiện search/filter phải cho ra tập kết quả **≤ 20 bản ghi** (co về 1 trang) thì mới lộ bug.
- ⚠️ Dev **không tái hiện được trên môi trường dev** (MySQL `host.docker.internal:3306` báo Connection refused) — mức verify của Dev chỉ là `lint` + đọc mã nguồn. Xem mục 6 trong [03-dev-impact.md](03-dev-impact.md).
- ⚠️ Dev ghi nhận màn **Chi tiết sản phẩm** còn **cùng lỗi** khi đổi tháng nhưng **không sửa** (ngoài phạm vi ticket) → nếu Leader muốn cover thì phải mở ticket riêng, không gộp vào #27085.
