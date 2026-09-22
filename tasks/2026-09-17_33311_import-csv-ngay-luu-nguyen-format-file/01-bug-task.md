# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33311 — Khi import thì đang lưu vào DB theo đúng data trong file` |
| Module / Màn hình | Quản lý CSV (CSV管理) — **import CSV bạn bè**, job nền `HandleImportCsvTask`. Chỗ lỗi hiện ra: **Chat 1:1 (chat 11)** → friend info kiểu ngày (date picker). |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine vốn đã viết tiếng Việt → giữ nguyên câu chữ, chỉ bổ sung chú thích trong ngoặc. -->

Base branch: `release-t07-2026`
Job: `HandleImportCsvTask`

**1.** Expect: chuyển về cùng định dạng data `yyyy-MM-dd`
vì khi lưu theo các định dạng khác `yyyy/MM/dd`, `yyyy/M/d`, `yyyy-M-d`
ở màn hình chat 11 (Chat 1:1) => click vào friend info kiểu date => đang không hiển thị được ngày tương ứng trên date picker
click ra ngoài => báo lỗi sai format date

**2.** Nhập các ngày không tồn tại thì vẫn cho import vào

- `2025-02-29`
- `2025-13-01`
- `2025-00-10`

Hiện tại: Import success và trên chat 11 đang hiển thị `Invalid date`
Expect: Báo lỗi, không cho import vào

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — description chỉ ghi hiện trạng + expect, không có steps. Không tự suy steps. -->

## Expected result

<!-- Lấy nguyên văn từ description (dòng "Expect"), không phải từ section "Tái hiện bug". -->

- (1) Dữ liệu ngày khi import được chuyển về cùng định dạng `yyyy-MM-dd`.
- (2) Ngày không tồn tại (`2025-02-29`, `2025-13-01`, `2025-00-10`): báo lỗi, không cho import vào.

## Actual result

<!-- Lấy nguyên văn từ description (tiêu đề ticket + dòng "Hiện tại"). -->

- (1) Import lưu vào DB đúng nguyên chuỗi trong file (`yyyy/MM/dd`, `yyyy/M/d`, `yyyy-M-d`) → ở chat 11, click vào friend info kiểu date thì date picker không hiển thị được ngày tương ứng; click ra ngoài thì báo lỗi sai format date.
- (2) Import success và trên chat 11 đang hiển thị `Invalid date`.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- 25-12-2025-03-34-23.png — https://redmine.watermelon.vn/attachments/download/22278/25-12-2025-03-34-23.png

## Ghi chú thêm của Leader

⚠️ **Redmine không có section "Tái hiện bug"** (không có steps chuẩn) — description chỉ ghi hiện trạng + expect. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** (chuẩn hoá 4 định dạng về `yyyy-MM-dd` + chặn ngày không tồn tại) + **regression impact**.

- Ticket gồm **2 lỗi**: (1) lưu nguyên định dạng ngày trong file; (2) ngày không tồn tại vẫn import được. Lỗi (2) được Hoang Xuan Thang ghi ở Journal #129534 (2026-08-19), sau đó Dev gộp vào description (2026-08-21).
- Phạm vi cột ngày theo Dev: **生年月日 (birthday)** + **friend info kiểu lịch (typeData=3)**.
- Base branch `release-t07-2026`; branch fix của Dev: `m_202608_import-csv-date-format_33311` (xem file 03).
- Môi trường phát hiện: ticket không ghi rõ.
- Tracker `Bug tự detect`, parent #26684. Status hiện tại: `Fix done - Đợi test`.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | Ticket không ghi |
| Friend | Ticket không ghi |
| Đối tượng cấu hình | Cột ngày trong file CSV import: 生年月日 + friend info kiểu lịch (theo Dev, file 03) |
| Input lỗi (1) — sai định dạng | `yyyy/MM/dd`, `yyyy/M/d`, `yyyy-M-d` |
| Input lỗi (2) — ngày không tồn tại | `2025-02-29`, `2025-13-01`, `2025-00-10` |
| Thời điểm lỗi | Ticket tạo 2025-12-25 (không ghi thời điểm lỗi cụ thể) |
| Đối chứng | Định dạng `yyyy-MM-dd` — định dạng mong đợi |

## Journal / note từ Redmine (nguyên văn)

**Journal #129534 — Hoang Xuan Thang — 2026-08-19:**

```
nhập các ngày không tồn tại thì vẫn cho import vào 

2025-02-29
2025-13-01
2025-00-10  
Hiện tại: Import success và trên chat 11 đang hiển thị Invalid date
Expect: Báo lỗi không cho import vào
```

> Journal #132130 — Thanh Duy Nguyen — 2026-08-21: báo cáo đánh giá ảnh hưởng (AI tạo tự động) → đã tách sang [03-dev-impact.md](03-dev-impact.md).
