# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT THIẾU: Redmine #40896 KHÔNG có mục "Đánh giá ảnh hưởng phía dev".**
> Ticket #40896 là bug do AI Test Studio raise (tracker `Bug Tester`, status `New`, 0 journal) — Dev **chưa** viết đánh giá cho root cause "job chạy 2 vòng quét callback + 0 thread vòng quét media khi MODE=NORMAL".
>
> Nội dung dưới đây được lấy từ **ticket cha #40889** (Journal #136198 — Thanh Duy Nguyen — 2026-09-12), **cùng branch + commit** với bug. Đánh giá đó **chỉ nói về việc đổi định dạng cột `callback_event.request`** — **KHÔNG** cover nguyên nhân số thread/scheduler sai của #40896.
>
> 👉 **Yêu cầu Dev bổ sung đánh giá riêng cho #40896 trước khi chạy `/write-tc` hoặc `/review-tc`.** Mục 1 / 2 / 3 / 4 bên dưới hiện là **bối cảnh của ticket cha**, không phải cách fix bug này.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen (assignee #40896 và #40889) |
| Commit / Pull Request | `f6104a3` (ticket cha #40889) — ticket #40896 ghi commit tái hiện là `f6104a35`. **Chưa có commit fix cho #40896.** |
| Branch | `m_202609_forward_webhook_40475_release-callback` (branch callback) · `m_202609_forward_webhook_40475_cb_full_request` (branch job thường) |
| Ngày submit đánh giá | 2026-09-12 (Journal #136198 của #40889) — **#40896 chưa có** |
| Auto-filled | `2026-09-15 by /new-task` (nguồn: **ticket cha #40889**, không phải #40896) |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 0. Root cause quan sát được của #40896 (từ QA, CHƯA có xác nhận Dev)

<!-- Ghi lại quan sát của ticket bug để không mất thông tin. KHÔNG phải đánh giá của Dev. -->

- Với `MODE` mặc định (`NORMAL`) + `ENABLE_POSTBACK=1` + `ENABLE_DOWNLOAD_MEDIA=1`, `jstack` đếm được:
  - `HandlePostbackTask$1` (vòng quét `callback_event`) = **2 thread** → mỗi webhook bị 2 vòng quét nhặt, xử lý nhân đôi (2 bản ghi `messages_v2s`, 2 bản ghi `auto_reply_history`).
  - `HandlePostbackTask$2` (worker) = **203 thread**.
  - `lambda$startJobGetMediaEvent` (vòng quét media) = **0 thread** → row có media kẹt vĩnh viễn ở trạng thái **30**.
- ⚠️ **Input thiếu**: Dev chưa xác nhận vì sao MODE=NORMAL lại khởi động 2 vòng quét callback và bỏ qua vòng quét media; chưa có danh sách MODE khác (và số thread kỳ vọng của từng MODE) để đối chiếu.

---

## 1. Nguyên nhân

> Nguồn: **ticket cha #40889** — không phải nguyên nhân của #40896.

- Feature #40044 yêu cầu forward "gửi nguyên trạng event mà LINE OA nhận được", nhưng `callback_event.request` đang chỉ lưu riêng mảng `events` (bóc ra rồi serialize lại nên mất `destination`, đổi thứ tự key, escape ký tự non-ASCII).
- Sửa để lưu nguyên full body LINE gửi, đồng thời job xử lý callback + download media vẫn đọc được các row format cũ còn trong DB.

## 2. Cách fix

> Nguồn: **ticket cha #40889** — không phải cách fix của #40896.

- `HandlePostbackTask.addCallback` (`HandlePostbackTask.java:767`): bỏ bước `readValue(HashMap)` rồi `writeValueAsString(get("events"))`, lưu thẳng chuỗi request gốc.
- `HandlePostbackTask.parseCallbackEventData` (`HandlePostbackTask.java:5029`): nhận dạng format theo ký tự mở đầu — `{` là full body (đọc node `events`; `events` rỗng hoặc thiếu thì trả list rỗng cho case LINE verify webhook URL), `[` là mảng events của row cũ nên giữ nguyên logic cũ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Nguồn: **ticket cha #40889**.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.parseCallbackEventData` (`HandlePostbackTask.java:5029`) | Đã sửa — nhận dạng format theo ký tự mở đầu | Chỉ có **1 caller** là `startHandleCallbackEvent` (`HandlePostbackTask.java:333`), dùng chung cho **cả callback thường lẫn luồng download media** → sửa 1 chỗ là cả 2 luồng cùng support |
| 2 | `HandlePostbackTask.addCallback` (`HandlePostbackTask.java:767`) | Đã sửa — ghi thẳng chuỗi request gốc | Nơi **ghi duy nhất** vào cột `request` |
| 3 | `HandleForwardCallbackEventTask.buildBody` | **Không sửa** | Nơi đọc thứ 2 của cột `request`; forward nguyên trạng, không parse nên không cần sửa |
| 4 | Query DB select cột `request` | **Không có** | Dev xác nhận không có query nào select cột này |

⚠️ **Chưa có mục 3 cho #40896** — chưa biết hàm nào khởi tạo scheduler theo MODE, có bao nhiêu caller, MODE nào khác cũng dùng chung hàm đó.

---

## 4. Đánh giá ảnh hưởng

> Nguồn: **ticket cha #40889**. Các tag `F*` / `D*` / `T*` dưới đây là impact của **thay đổi format request**, KHÔNG phải impact của fix #40896.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandlePostbackTask.addCallback` | `HandlePostbackTask.java:767` | Direct | Ghi full body vào `callback_event.request` |
| F2 | `HandlePostbackTask.parseCallbackEventData` | `HandlePostbackTask.java:5029` | Direct | Nhận dạng 2 format `{` / `[` |
| F3 | `HandlePostbackTask.startHandleCallbackEvent` | `HandlePostbackTask.java:333` | Indirect | Caller duy nhất của F2; dùng chung cho callback thường + download media |
| F4 | `HandleForwardCallbackEventTask.buildBody` | — | Indirect | Không sửa, nhưng body forward ra bên thứ 3 đổi nội dung |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.request` | UPDATE (đổi định dạng giá trị ghi mới) | Từ mảng `events` → full body. **Chỉ áp dụng cho row mới**; row cũ giữ nguyên, **không backfill** |
| D2 | — | Không có | Dev xác nhận không thay đổi DB schema / config / constant |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Xử lý callback LINE (message / postback / follow / unfollow / videoPlayComplete) + download media — bắn event thật kèm ảnh/video, row `callback_event` lưu full body và chạy tới DONE, tin nhắn vào đúng phòng chat, scenario/tag/richmenu và tải file chạy bình thường | F2, F3, D1 | **High** |
| T2 | Tương thích row cũ — để lại vài row format cũ `[{...}]` đang NEW/retry rồi restart job, phải parse và xử lý được, không nhảy `STATUS_ERROR` | F2, D1 | **High** |
| T3 | Forward webhook Kênh 1 — bên thứ 3 nhận nguyên body có cả `destination` và `events` thay vì mảng trần; test lại endpoint đối tác, check tiếng Nhật/emoji không bị escape | F1, F4, D1 | **High** |
| T4 | Verify webhook URL trên LINE Developers (LINE gửi `events` rỗng) — bấm 検証, job không văng lỗi parse, row phải là `STATUS_UNKNOWN_TYPE` | F2 | **Medium** |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] ⚠️ **Đã yêu cầu Dev viết đánh giá ảnh hưởng RIÊNG cho #40896** (nguyên nhân MODE=NORMAL sinh 2 vòng quét callback + 0 vòng quét media, cách fix, caller, impact) — mục 1→4 hiện chỉ là bối cảnh ticket cha #40889
