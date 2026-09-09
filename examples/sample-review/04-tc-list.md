# 04 — TC List (do member viết)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | Trần Thị B |
| Ngày submit | 2026-04-23 |
| Version TCs | v1 |
| Link TC gốc | https://sheets.internal/lme/TC-LME-2054-v1 |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Scheduled broadcast gửi đúng số friend tại send time khi tag thay đổi | Positive | High | Bot có 150 friends tag "VIP" | 1. Tạo scheduled broadcast cho tag "VIP", set send sau 10 phút.<br>2. Add thêm 50 friend vào tag "VIP".<br>3. Chờ đến giờ send. | Broadcast gửi đến 200 friends. |  |  |  |
| TC002 | Scheduled broadcast khi tag bị remove khỏi friend sau lúc create | Positive | High | Bot có 100 friends tag "VIP" | 1. Tạo scheduled broadcast cho tag "VIP", send sau 10 phút.<br>2. Remove tag "VIP" khỏi 20 friends.<br>3. Chờ đến giờ send. | Broadcast chỉ gửi đến 80 friends còn tag "VIP". |  |  |  |
| TC003 | Preview count màn create broadcast hiển thị note "may vary at send time" | Positive | Medium | — | 1. Vào create broadcast.<br>2. Chọn tag "VIP".<br>3. Xem preview. | Dưới số recipients có note "Preview only — actual count may vary at send time". |  |  |  |
| TC004 | Immediate broadcast vẫn hoạt động bình thường (regression) | Regression | High | Bot có 50 friends tag "VIP" | 1. Tạo immediate broadcast tag "VIP".<br>2. Gửi ngay. | Broadcast gửi đến 50 friends. |  |  |  |
| TC005 | Broadcast detail screen không còn hiển thị field cached_recipient_ids | Regression | Low | Có 1 broadcast đã gửi | 1. Mở broadcast detail. | Không có field/label nào liên quan tới cached recipients. |  |  |  |
| TC006 | Send scheduled broadcast cho tag rỗng (boundary) | Boundary | Medium | Tạo tag mới chưa có friend | 1. Tạo scheduled broadcast cho tag rỗng.<br>2. Chờ đến giờ send. | Broadcast complete với 0 recipients, không lỗi. |  |  |  |
| TC007 | Migration clear cached_recipient_ids cho scheduled broadcasts | Positive | High | Có scheduled broadcast pending | 1. Run migration.<br>2. Query DB. | Field `cached_recipient_ids` = null cho các scheduled broadcast pending. |  |  |  |
| TC008 | Friend block bot sau khi tạo broadcast — vẫn không gửi cho friend block | Positive | High | Bot có 10 friends tag "VIP" | 1. Tạo scheduled broadcast tag "VIP".<br>2. 2 friends block bot.<br>3. Chờ send. | Broadcast gửi đến 8 friends (loại bỏ blocked). |  |  |  |

### Chú thích cột

- **Type**: Positive / Negative / Boundary / Regression
- **Priority**: High / Medium / Low
- **Output note** / **Assignee** / **Status**: để trống khi sinh draft. QA fill sau khi run TC. Status có dropdown trên Sheet (`OK` / `NG` / `Not test` / `NG -> Đã fix`) khi sync.

---

## Member tự check trước khi submit

- [x] Đã đọc kỹ `01-bug-task.md`
- [x] Đã đọc kỹ spec của tính năng
- [x] Đã đọc kỹ `03-dev-impact.md`
- [x] Mỗi impact trong 4.1 / 4.2 / 4.3 đều có ít nhất 1 TC verify (Title chứa keyword)
- [x] Có TC verify trực tiếp bug fix (TC001)
- [ ] Có TC regression cho mỗi tính năng trong 4.3 — *tôi đang thiếu T3, T4, T5*
- [ ] Có negative + boundary cho mỗi data quan trọng — *chỉ có 1 boundary (TC006)*
- [x] Mọi TC đều có steps rõ ràng
