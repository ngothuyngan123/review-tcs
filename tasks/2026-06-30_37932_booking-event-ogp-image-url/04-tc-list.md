<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 | sheet=Task nhỏ + fix bug KH | anchor=Main Function -->

# 04 — TC List (fetch từ Sheet master — read-only)

> ⚠️ TCs dưới đây **fetch nguyên văn** từ Google Sheet master (range A202:J214, tab "Task nhỏ + fix bug KH"). **KHÔNG sửa** nếu chưa confirm với Leader. Giá trị cell giữ nguyên; cột TC ID được đánh số tự động (sheet gốc để trống) để tiện review.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `Thanh Phương` (Link TC từ journal Redmine #37932) |
| Ngày submit | `2026-06-29` |
| Version TCs | `v1` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1r6N_p59tudrzfEjoK5xrnWQG5oYwv9hM8daBSuM8kLY/edit?gid=29229128#gid=29229128 (sheet "Task nhỏ + fix bug KH", row 202~214) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Share url event lên Facebook | | | Check case event disable bill tiền | | Preview hiển thị đúng title và description của event<br>Không bị hiển thị ảnh American Express | ở comment fb Hiện tên title của text server callback của liff app | | OK staging |
| TC002 | Share URL sự kiện lên LINE | | | | | | | | OK staging |
| TC003 | Share URL qua Email | | | | | | send qua mail không hiện preview url | | OK staging |
| TC004 | Share URL lên Messenger | | | | | | | | OK staging |
| TC005 | Event có title dài | | | | | | Text dài sẽ tự động cắt, không bị hiển thị lỗi | | OK staging |
| TC006 | Event có description dài | | | | | | | | OK staging |
| TC007 | Event có ký tự tiếng Nhật | | | | | | | | OK staging |
| TC008 | Event có Emoji | | | | | | | | OK staging |
| TC009 | Check user mở các url được share ở các môi trường khác nhau | | | | | User mở được url, hiển thị màn booking event | case mở từ Messenger thì đang mở vào màn chat của user với bot, không hiện được màn hình booking | | OK staging |
| TC010 | Check user booking từ các url được share ở các môi trường khác nhau | | | | | User booking được bình thường | | | OK staging |
| TC011 | Check share nhiều event liên tiếp | | | | | Hiển thị đúng preview của từng url | | | OK staging |
| TC012 | Check refresh màn hình sau khi share url | | | | | | | | OK staging |
| TC013 | Edit title và description của event => share lại url | | | | | Hiển thị preview của url theo text mới nhất | | | OK staging |

### Chú thích cột

- **Type**: `Positive` / `Negative` / `Boundary` / `Regression` — sheet gốc để trống, member/Leader bổ sung khi review.
- **Priority**: `High` / `Medium` / `Low` — sheet gốc để trống.
- **Output note** / **Assignee** / **Status**: giữ nguyên giá trị fetch từ sheet.

### Environment (note)

Sheet gốc đánh dấu status `OK staging` → TCs đã chạy trên **Staging** (`staging.lme.jp`).

---

## Member tự check trước khi submit

`<member điền sau khi review>`

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

<!-- Source: fetched từ Redmine #37932 Link TCs (journal Thanh Phương 2026-06-29), range A202:J214 tab "Task nhỏ + fix bug KH" lúc 2026-06-30. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
