# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `b84b175` |
| Branch | `m_202609_form_googlesheet_fix_empty_data_40734` |
| Ngày submit đánh giá | 2026-09-12 (Journal #136168) |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

*(Nguyên văn Journal #136168)*

- Khách mở form rồi bấm gửi mà không nhập câu trả lời nào thì job hiểu nhầm là "câu trả lời này không thuộc trang nào", nên bỏ qua luôn, không ghi dòng nào lên Google Sheet.
- Chỉ xảy ra khi sheet đã có sẵn dữ liệu. Sheet còn trống thì vẫn ghi bình thường, nên khách xoá sheet tạo lại thì thấy dữ liệu hiện ra đủ, đúng như khách mô tả. Record bị bỏ qua vẫn bị đánh dấu là "đã đồng bộ" nên job không ghi lại lần nữa (record mẫu: 2026-08-19 10:47, form 228620).

## 2. Cách fix

*(Nguyên văn Journal #136168)*

- Sửa lại điều kiện: chỉ cần câu trả lời thuộc trang đang ghi là tạo 1 dòng trên sheet, kể cả khi khách không nhập nội dung nào. Dòng đó có 回答ID, thời gian, tên LINE user, các cột câu hỏi để trống - giống hệt cách sheet trống đang ghi.
- Thêm mã câu trả lời vào log để lần sau tra được record nào bị bỏ qua.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

*(Dev ghi dạng plain text ở Journal #136168, convert sang bảng — nguyên văn ở phần trích dưới bảng)*

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandleFormAnswerSyncGoogleSheetTask.handleNonEmptySheet` (hàm dựng dòng ghi lên sheet) | **Có sửa** — đổi điều kiện tạo dòng | Root cause: điều kiện cũ bỏ qua bản ghi không có câu trả lời |
| 2 | Caller 1 — đồng bộ theo lô | Không sửa | Không đổi tham số và kết quả trả về của hàm được sửa |
| 3 | Caller 2 — đồng bộ lại từng record khi retry | Không sửa | Không đổi tham số và kết quả trả về của hàm được sửa |
| 4 | Xử lý khi sheet còn trống | Không đụng tới | Ngoài phạm vi fix |
| 5 | Xoá dòng trên sheet | Không đụng tới | Ngoài phạm vi fix |

*Nguyên văn Dev:*

```
- Chỉ sửa bên trong hàm dựng dòng ghi lên sheet, không đổi tham số và kết quả trả về, nên 2 chỗ gọi tới nó (đồng bộ theo lô và đồng bộ lại từng record khi retry) giữ nguyên, không phải sửa.
- Không đụng tới phần xử lý khi sheet còn trống và phần xoá dòng trên sheet.
```

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandleFormAnswerSyncGoogleSheetTask.handleNonEmptySheet` | `HandleFormAnswerSyncGoogleSheetTask.java` | Direct | Hàm duy nhất Dev sửa (nguyên văn mục 4.1) |

*Nguyên văn Dev mục 4.1:*

```
- HandleFormAnswerSyncGoogleSheetTask.handleNonEmptySheet
```

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | *(Dev ghi: **Không có**)* | — | Không có migration / update dữ liệu kèm bản fix |

*Nguyên văn Dev mục 4.2:*

```
- Không có
```

> ⚠️ Lưu ý cho Leader: mục 4.2 ghi "Không có" nghĩa là **bản fix không kèm bước khôi phục dữ liệu đã mất**. Các record bị bỏ qua trước khi deploy vẫn đang ở trạng thái "đã đồng bộ" và sẽ không tự lên sheet (xem mục 1). Cần chốt riêng việc rà soát + khôi phục (RULE-04).

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form đã có dữ liệu trên sheet — mở form bấm gửi không nhập gì → phải thấy 1 dòng mới có 回答ID + thời gian + tên LINE user, các cột câu hỏi để trống | F1, BUG | *(Dev không ghi mức)* — đây là hành vi mới của bản fix |
| T2 | Trả lời form bình thường (nhập đủ) — dữ liệu vẫn lên đúng cột như trước, không lệch cột, không bị ghi trùng dòng | F1 | *(Dev không ghi mức)* |
| T3 | Form nhiều trang — trả lời 1 trang thì chỉ sheet của trang đó có dòng mới, sheet trang khác không phát sinh dòng thừa | F1 | *(Dev không ghi mức)* |
| T4 | Sheet còn trống — lần ghi đầu vẫn ra đủ tiêu đề cột và các câu trả lời cũ như trước | F1 (dùng chung hàm) | *(Dev không ghi mức)* |

*Nguyên văn Dev mục 4.3:*

```
- Form đã có dữ liệu trên sheet: mở form bấm gửi mà không nhập gì, phải thấy 1 dòng mới có 回答ID + thời gian + tên LINE user, các cột câu hỏi để trống.
- Trả lời form bình thường (nhập đủ): dữ liệu vẫn lên đúng cột như trước, không lệch cột, không bị ghi trùng dòng.
- Form nhiều trang: trả lời 1 trang thì chỉ sheet của trang đó có dòng mới, sheet trang khác không phát sinh dòng thừa.
- Sheet còn trống: lần ghi đầu vẫn ra đủ tiêu đề cột và các câu trả lời cũ như trước.
```

---

## 5. Commit / Branch (nguyên văn mục 5 của Dev)

```
5.1 Commit hoặc pull request
    - b84b175
5.2 Branch hiện tại của task
    - m_202609_form_googlesheet_fix_empty_data_40734
```

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
