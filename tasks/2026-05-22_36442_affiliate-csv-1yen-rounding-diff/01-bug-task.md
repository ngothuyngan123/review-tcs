# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | #36442 — [15-05-2026][Admin] Master admin — sai lệch 1円 trang đại lý vs CSV (32 user, dư 32 yên) |
| Redmine URL | https://redmine.watermelon.vn/issues/36442 |
| Auto-filled | 2026-05-22 by /new-task |
| Ngày báo cáo | 2026-05-15 |
| Khách hàng / PM báo | AI CSS |
| Module / Màn hình | Admin / 代理店報酬 (Tiền hoa hồng đại lý) — và export CSV 振込用CSV |
| Priority | Medium (Redmine: Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (KH báo có dữ liệu chuyển khoản thực tế kỳ 2025/04 → khả năng Production) |

## Mô tả bug (nguyên văn từ khách hàng)

User:
Bot Name:

Khách báo trouble: Trang Master admin — Tiền hoa hồng đại lý.

[補足 / Bổ sung]
Kỳ thanh toán 2025/04:
Số tiền hiển thị trên trang "代理店報酬" (Tiền hoa hồng đại lý) và số tiền trên CSV dùng để chuyển khoản chênh lệch 1円 ở 32 user.

Thực tế đã chuyển dư 32円 (32 yên) → yêu cầu fix.

[Đính kèm: F0B41RWKM1Q — xem Slack permalink]

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DV32EMRS?record_id=Rec0B3LCGFDUP

---

### 原文 (JP)

```
マスター管理画面 代理店報酬に関して

[補足]
2025/04支払い分
代理店報酬ページに記載されている金額と
振込用CSVに記載されている金額が1円相違しているユーザーが32件発生した。

実際に32円分多く支払われてしまったため、修正をお願いします。
```

<!-- TaskRef: wssj_check:Rec0B3LCGFDUP -->

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

(Trích "Tái hiện case KH" từ journal #118957 — Kim Cúc, 2026-05-21)

1. Vào admin → màn `代理店報酬` (Tiền hoa hồng đại lý).
2. Download CSV ở Cột 1 `振込用CSV` của tháng 4 (kỳ 2025/04).
3. So sánh số tiền hiển thị trên GUI admin vs số tiền trên CSV.

## Expected result

- Số tiền `報酬額` hiển thị trên GUI admin và trên CSV `振込用CSV` **bằng nhau** (cùng quy tắc làm tròn nhất quán).
- Tổng amount thực tế chuyển khoản khớp với số hiển thị trên admin.

## Actual result

- GUI admin: số tiền `報酬額` được **làm tròn xuống** (floor) → không có phần lẻ.
- CSV download: số tiền được **làm tròn đến số gần nhất** (rounding) → có thể +1 yên so với GUI.
- Kỳ 2025/04: **32 user lệch 1円** → tổng đã chuyển dư 32円 so với GUI.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response (file dữ liệu 32 user chênh lệch)

Attachments:
- [振込金額_差異リスト.xlsx](https://redmine.watermelon.vn/attachments/download/25770/%E6%8C%AF%E8%BE%BC%E9%87%91%E9%A1%8D_%E5%B7%AE%E7%95%B0%E3%83%AA%E3%82%B9%E3%83%88.xlsx) — danh sách 32 user lệch 1円 kỳ 2025/04.

## Ghi chú thêm của Leader

<!-- Điều kiện tiên quyết, account test, feature flag, timezone,... nếu có -->

- ⚠️ Bug có data tài chính thực tế (đã chuyển dư 32円) → khi viết TC verify, dùng **staging** + dataset test có amount có phần lẻ (.5, .6, .8) để chắc chắn cover được logic làm tròn cả 2 phía (GUI + CSV).
- ⚠️ Dev (qua Kim Cúc submit ở mục 03) ghi 4.3 "màn hình admin 商品決済" — bug context lại là "代理店報酬". Verify lại với Dev xem fix có ảnh hưởng cả 商品決済 hay chỉ 代理店報酬, hay Dev gõ nhầm tên màn.
