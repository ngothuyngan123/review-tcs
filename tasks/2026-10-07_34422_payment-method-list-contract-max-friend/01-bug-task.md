# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34422 — [Quản lý hợp đồng] Bot chính bill transfer nhấn change sang bill tháng (card) success => Màn list pt bill của bot chính hiện transfer còn pt bill của max friend thì hiện card` |
| Module / Màn hình | Quản lý hợp đồng (Point Setting / Bill) — màn danh sách hợp đồng 契約情報・領収書 (SCR-DC-01), cột 決済方法 (Phương thức thanh toán) của dòng phí theo số bạn bè (max friend). Liên quan **Contract Plan & Payment (FA-031)**. |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Redmine **description trống** — chỉ có tiêu đề ticket (đã là tiếng Việt). Diễn giải lại từ tiêu đề:

Bot chính (hợp đồng chính) đang bill theo phương thức **chuyển khoản** (transfer). Khách bấm đổi sang bill theo **tháng** bằng **thẻ** (card) và thao tác đổi thành công. Sau đó, trên **màn danh sách hợp đồng (list bill)**:
- Dòng của **bot chính (gói chính)** hiển thị đúng **「銀行振込」(chuyển khoản/transfer)**.
- Dòng **phí theo số bạn bè (max friend)** của **cùng hợp đồng đó** lại hiển thị **「カード決済」(thẻ/card)**.

→ Hai dòng của cùng 1 hợp đồng hiển thị **mâu thuẫn nhau** về phương thức thanh toán.

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — để trống. Xem Dev impact (file 03) để biết root cause + kịch bản tái hiện Dev đã tự dựng. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- `2026_02_11_15_22_48_契約情報_領収書_一覧_.png` — https://redmine.melonglobal.net/attachments/download/23456/2026_02_11_15_22_48_%E5%A5%91%E7%B4%84%E6%83%85%E5%A0%B1_%E9%A0%98%E5%8F%8E%E6%9B%B8_%E4%B8%80%E8%A6%A7_.png

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (description trống, không có section "Tái hiện bug") — root cause đã được Dev confirm qua đánh giá ảnh hưởng (`03-dev-impact.md`, từ journal AI auto-fixbug #133049). TCs nên tập trung verify cách fix + regression impact, không cần tái lập đúng bước khách hàng.
- Ticket status Redmine: **Fix done - Đợi test**. Priority: Normal. Tracker: **Bug tự detect** (phát hiện qua AI auto-fixbug, không phải khách hàng báo trực tiếp).
- Branch fix đã **push**, verify của Dev mới ở mức **lint + biên dịch Blade/Vue** — **CHƯA verify được trên UI thật / dữ liệu dev** (MySQL dev từ chối kết nối tại thời điểm Dev điều tra). Cần tester verify lại trên giao diện thật.
- Trên **MCP LME TEST STUDIO**, task #237 (ticket 34422) đã có sẵn **14 TC do AI sinh**, đã chạy **2026-10-07** (13 Đạt / 1 skip), xem `04-tc-list.md`.

