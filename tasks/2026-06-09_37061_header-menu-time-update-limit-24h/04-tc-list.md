<!-- sync-target: https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=412698763 -->
# 04 — TC List (do member viết)

> ⚠️ **TCs CŨ FETCH TỪ SHEET — READ-ONLY.** Bộ TC này được fetch nguyên văn từ Google Sheet master (tab `Improve 2026/05/13`, rows 280–293) lúc 2026-06-09. **KHÔNG sửa Title / Expected** — đây là TC cũ team đã viết/chạy (phần lớn status `OK`). Nếu cần bổ sung TC mới (delta) cho impact chưa cover → chạy `/write-tc` và để Claude sinh phần thiếu, KHÔNG override TC dưới đây.
>
> Cấu trúc gốc trong Sheet là dạng cây `Main Function → Sub1 → Sub2`; cột "Expected" lấy từ cột H (Actual Result) của sheet, cột "Status" lấy từ cột I (`Support #37061`). Title bên dưới = `<Main Function> — <Sub path>` để giữ ngữ cảnh.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | `v1 (fetched từ Sheet)` |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=412698763 (tab `Improve 2026/05/13`, rows 280–293) |

---

## TC List

> Bảng TC dùng **10 cột chuẩn team**. Khi `/sync-tc` push lên Google Sheet master, cột Status sẽ có dropdown 4 giá trị: `OK` / `NG` / `Not test` / `NG -> Đã fix`.
>
> Cột `Type` / `Priority` / `Precondition` để trống/`<member bổ sung>` vì sheet gốc không có các cột này — KHÔNG bịa. Member verify rồi điền.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check hiển thị đúng format 24h — Alert hiển thị limit (header/menu) | | | `<member bổ sung>` | 1. Đăng nhập admin, mở header/menu<br>2. Xem alert hiển thị limit | hiển thị theo format HH:MM 24h | | | OK |
| TC002 | Check giá trị thời gian đã lưu (Bot get limit) — job hàng ngày lấy limit | | | `<member bổ sung>` | 1. Job hàng ngày lấy limit chạy<br>2. Kiểm tra thời gian update hiển thị | - Hiển thị đúng time update khi job chạy<br>- Trên GUI hiển thị time định dạng 24h<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC003 | Check giá trị thời gian đã lưu — click vào màn summary message send | | | `<member bổ sung>` | 1. Click vào màn summary message send<br>2. Kiểm tra thời gian update hiển thị | - Hiển thị đúng time update khi job chạy<br>- Trên GUI hiển thị time định dạng 24h<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC004 | Check giá trị thời gian đã lưu — summary message send, click liên tiếp | | | `<member bổ sung>` | 1. Vào màn summary message send<br>2. Click liên tiếp nhiều lần | Vẫn hiển thị đúng time update<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC005 | Check giá trị thời gian đã lưu — click btn reload lại thông tin bot | | | `<member bổ sung>` | 1. Click btn reload lại thông tin bot<br>2. Kiểm tra thời gian update hiển thị | - Hiển thị đúng time update khi job chạy<br>- Trên GUI hiển thị time định dạng 24h<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC006 | Check giá trị thời gian đã lưu — btn reload, click liên tiếp | | | `<member bổ sung>` | 1. Click btn reload lại thông tin bot<br>2. Click liên tiếp nhiều lần | - Vẫn hiển thị đúng time update<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC007 | Check thời gian hiển thị trùng thời điểm get limit đã lưu — có upgrade limit | | | `<member bổ sung>` | 1. Bot có upgrade limit<br>2. Kiểm tra thời gian hiển thị có trùng thời điểm get limit lưu trước đó | - Vẫn hiển thị đúng time update<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC008 | Check thời gian hiển thị trùng thời điểm get limit đã lưu — giữ nguyên limit | | | `<member bổ sung>` | 1. Bot giữ nguyên limit (không upgrade)<br>2. Kiểm tra thời gian hiển thị | - Vẫn hiển thị đúng time update<br>- Giữ nguyên đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | OK |
| TC009 | Check hiển thị time update khi mới tạo bot — add bot mới chưa có time | | | `<member bổ sung>` | 1. Add bot mới (chưa có time get limit)<br>2. Kiểm tra hiển thị time update | Hiển thị time update sau khi tạo bot thành công<br>- db: bots.limit_message_loa_last_updated | | | |
| TC010 | Check hiển thị time update khi mới tạo bot — sau khi bot được get limit | | | `<member bổ sung>` | 1. Bot mới được get limit<br>2. Kiểm tra hiển thị time | - Hiển thị đúng time update khi job chạy<br>- Trên GUI hiển thị time định dạng 24h<br>- Hiển thị đúng limit message loa của bot sau khi update<br>- db: bots.limit_message_loa_last_updated | | | |
| TC011 | Check hiển thị đúng khi change bot — change bot free | | | `<member bổ sung>` | 1. Change sang bot free<br>2. Kiểm tra thời gian hiển thị | `<sheet gốc để trống Expected — member bổ sung>` | | | |
| TC012 | Check hiển thị đúng khi change bot — change bot có phí | | | `<member bổ sung>` | 1. Change sang bot có phí<br>2. Kiểm tra thời gian hiển thị | hiển thị đúng thời gian tương ứng sau khi change bot<br>- db: bots.limit_message_loa_last_updated | | | |
| TC013 | Kiểm tra tại màn Summary Message — truy cập màn Summary Message | | | `<member bổ sung>` | 1. Truy cập màn Summary Message | thời gian hiển thị đúng với bot đang chọn<br>Get lại time khi bot có upgrade | | | |
| TC014 | Kiểm tra tại màn Summary Message — đứng tại summary → upgrade → reload | | | `<member bổ sung>` | 1. Đứng tại màn summary message send<br>2. Thực hiện upgrade<br>3. Reload màn hình summary message send | `<sheet gốc để trống Expected — member bổ sung>` | | | |

### Chú thích cột

- **Type**:
  - `Positive` — happy path đúng theo fix
  - `Negative` — input sai / điều kiện sai, verify xử lý lỗi
  - `Boundary` — giá trị biên (min/max, null, empty, max length, race condition, multi-tab)
  - `Regression` — verify tính năng cũ không bị ảnh hưởng
- **Priority**:
  - `High` — block release nếu fail
  - `Medium` — quan trọng nhưng có workaround
  - `Low` — nice-to-have
- **Output note** / **Assignee** / **Status**: Status giữ nguyên từ sheet gốc (cột `Support #37061`). Các TC chưa có status = chưa chạy.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). TC liên quan **job hàng ngày lấy limit** (TC002) có thể cần chờ job chạy hoặc trigger thủ công trên Dev (`form.watermeru.com`).

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng:

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22 (chọn mục liên quan task)
- [ ] A.2 Non-function: Regression (bắt buộc), Compatibility (UI thay đổi format giờ)

**§B Checklist job**:
- [ ] B.1 Job callback
- [ ] B.2 Job sync Java — CLJ01

**§C Các tính năng chung**:
- [ ] C.2 Send message
- [ ] C.7 Plan limits

---

<!-- Source: fetched từ Redmine #37061 Link TCs, range A280:J293 tab "Improve 2026/05/13" lúc 2026-06-09. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
