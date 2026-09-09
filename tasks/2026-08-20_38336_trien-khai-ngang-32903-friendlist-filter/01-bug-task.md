# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #38336 bởi `/new-task` ngày 2026-08-20.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#38336 — Triển khai ngang Bug KH #32903: Action friend list redirect từ các màn send all, csv, tag, richmenu thì bị lỗi không theo filter` |
| Redmine URL | https://redmine.watermelon.vn/issues/38336 |
| Auto-filled | `2026-08-20 by /new-task` |
| Ngày báo cáo | `2026-06-30` |
| Khách hàng / PM báo | `Ngô Thúy Ngần` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine không set `category`; Studio ghi `feature = friend-list`) |
| Priority | `High` (Redmine priority = High) |
| Môi trường phát hiện | `<chưa rõ>` (description không nêu môi trường) |

### Thông tin bổ sung từ Redmine

| Trường | Giá trị |
|---|---|
| Tracker | `Triển khai ngang` |
| Project | `Lme` |
| Trạng thái hiện tại | `Fix done - Đợi test` |
| Assigned to | `Ngô Thúy Ngần` |
| Commit Date (custom field) | `2026-08-13` |
| Bug gốc liên quan | `#32903` (nêu trong subject; Redmine **không** khai báo relation chính thức) |
| Cập nhật gần nhất | `2026-08-13T07:56:11Z` |

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
1. Test triển khai ngang khi access friend list từ các MH:
- Màn send all
- Màn quản lý tag
- màn quản lý csv
- Màn richmenu
2. Trigger của action schedule tự tạo sửa lại: 【自動生成】友だち一括アクション
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — xem Ghi chú của Leader bên dưới. -->

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

> Redmine #38336 **không có attachment nào** (`attachments = []`).

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — ticket này là **"Triển khai ngang"** (tracker `Triển khai ngang`), không phải bug report trực tiếp từ khách hàng. Description chỉ nêu **phạm vi cần test**, không có Steps / Expected / Actual. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

**Bối cảnh cần nắm trước khi viết/review TC:**

1. **Ticket có 2 yêu cầu tách biệt**, phải cover cả hai:
   - **Yêu cầu 1** — triển khai ngang bug gốc #32903 cho **4 màn nguồn**: gửi hàng loạt (send all), quản lý tag, quản lý CSV, rich menu.
   - **Yêu cầu 2** — trigger của action schedule tự tạo phải là `【自動生成】友だち一括アクション`. Dev báo mục này **đã đúng sẵn trên release** từ commit `0d54f99d53` → **không sửa gì**. Vẫn cần TC verify, nhưng đây là verify hiện trạng, không phải verify fix.

2. **Bug gốc #32903 và ticket này đi qua 2 cơ chế khác nhau** (theo mục ■6 báo cáo Dev):
   - #32903 xử lý bộ lọc truyền qua **tham số URL** (`scenario_unfinish_id`), fix ở nhánh `fix-bug-32903` (merge `6f24af4732`).
   - 4 màn của ticket này truyền bộ lọc qua **localStorage** → không được nhánh cũ bao phủ.
   - ⇒ Khi viết TC **không được giả định** flow #32903 và flow #38336 giống nhau.

3. **Rủi ro cache asset — ảnh hưởng trực tiếp tới việc chấm kết quả test**: Dev **KHÔNG tăng version tài nguyên tĩnh** (theo yêu cầu human). File JS nhúng kèm `?v=config('sns-line.version')` → trình duyệt đã cache bản cũ sẽ **không tự tải bản mới**. Tester **bắt buộc Ctrl+F5** (hard reload) trước khi test, nếu không sẽ chấm nhầm "fix không có tác dụng".

4. **Cảnh báo hành vi thay đổi với người dùng cuối**: trước fix, bấm số người luôn hiện **toàn bộ** bạn bè; sau fix chỉ hiện **nhóm đã lọc**. Đây là hành vi **đúng theo thiết kế**, không phải regression — nhưng cần thông báo cho KH.

5. **Nguy cơ ẩn Dev tự nêu**: các nhánh nạp bộ lọc bên dưới 4 điều kiện lỗi (gửi hàng loạt, tag, CSV, rich menu, lịch hành động, phân tích chéo) **lần đầu thực sự chạy sau nhiều năm bị chặn** → phải test kỹ từng màn để chắc dữ liệu bộ lọc bàn giao vẫn đúng định dạng hiện tại.

**Trạng thái TC hiện có:** Redmine không có "Link TCs" human. File `04-tc-list.md` được fetch từ **MCP LME TEST STUDIO** (`task_id=71`) — 49 TC **do AI sinh**, `aiResult = fail`, chỉ **6/49 Đạt**, 1 fail, 37 skip, 5 chưa chạy. Xem cảnh báo chi tiết ở đầu file 04.

<!-- Source: Redmine #38336 (REST API /issues/38336.json?include=journals,attachments,relations), fetch 2026-08-20 bởi /new-task. MCP redmine không khả dụng trong session → gọi trực tiếp REST API với credentials trong .env. -->
