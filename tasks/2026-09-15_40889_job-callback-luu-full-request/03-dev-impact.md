# 03 — Đánh giá ảnh hưởng từ Dev

> **Đây là input QUAN TRỌNG NHẤT** để xác định coverage TCs.
> Nguồn: Redmine #40889 — Journal #136198 (Thanh Duy Nguyen, 2026-09-12). Chép nguyên văn, chỉ format lại thành bảng ở mục 3 / 4.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `f6104a3` |
| Branch | `m_202609_forward_webhook_40475_release-callback` (callback/receiver) + `m_202609_forward_webhook_40475_cb_full_request` (job thường) |
| Ngày submit đánh giá | `2026-09-12` |
| Auto-filled | `2026-09-15 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- Feature #40044 yêu cầu forward "gửi nguyên trạng event mà LINE OA nhận được", nhưng `callback_event.request` đang chỉ lưu riêng mảng `events` (bóc ra rồi serialize lại nên **mất `destination`, đổi thứ tự key, escape ký tự non-ASCII**).
- Sửa để lưu nguyên **full body** LINE gửi, đồng thời job xử lý callback + download media vẫn đọc được các row **format cũ** còn trong DB.

## 2. Cách fix

- `HandlePostbackTask.addCallback` (`HandlePostbackTask.java:767`): bỏ bước `readValue(HashMap)` rồi `writeValueAsString(get("events"))`, **lưu thẳng chuỗi request gốc**.
- `HandlePostbackTask.parseCallbackEventData` (`HandlePostbackTask.java:5029`): **nhận dạng format theo ký tự mở đầu**:
  - `"{"` = full body → đọc node `events`; `events` rỗng hoặc thiếu thì **trả list rỗng** (case LINE verify webhook URL).
  - `"["` = mảng events của row cũ → giữ nguyên logic cũ.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `HandlePostbackTask.parseCallbackEventData` (`HandlePostbackTask.java:5029`) | Đã sửa — nhận dạng format theo ký tự mở đầu | Đường đọc cột `request` |
| 2 | `HandlePostbackTask.startHandleCallbackEvent` (`HandlePostbackTask.java:333`) | Không sửa | **Caller DUY NHẤT** của `parseCallbackEventData`; dùng chung cho cả callback thường lẫn luồng download media → sửa 1 chỗ là cả 2 luồng cùng support |
| 3 | `HandlePostbackTask.addCallback` (`HandlePostbackTask.java:767`) | Đã sửa — lưu thẳng chuỗi request gốc | Nơi **ghi** DUY NHẤT vào cột `request` |
| 4 | `HandleForwardCallbackEventTask.buildBody` | Không sửa | Nơi **đọc** thứ 2 của cột `request` — forward nguyên trạng, không parse nên không cần sửa |

> Dev ghi rõ: cột `request` có **1 nơi ghi** (`addCallback`, đã sửa) và **2 nơi đọc** (`parseCallbackEventData` đã sửa, `buildBody` không cần sửa). **Không có query nào select cột này.**

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `HandlePostbackTask.addCallback` | `HandlePostbackTask.java:767` | Direct | Ghi full body thay vì mảng events |
| F2 | `HandlePostbackTask.parseCallbackEventData` | `HandlePostbackTask.java:5029` | Direct | Nhận dạng 2 format `{` / `[` |
| F3 | `HandlePostbackTask.startHandleCallbackEvent` | `HandlePostbackTask.java:333` | Indirect | Caller duy nhất của F2, dùng chung callback thường + download media |
| F4 | `HandleForwardCallbackEventTask.buildBody` | — | Indirect | Không sửa code nhưng **output thay đổi** (giờ gửi full body có `destination`) |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `callback_event.request` | UPDATE (đổi **định dạng giá trị**, không đổi schema) | Row **mới** = full body `{destination, events[...]}`; row **cũ** giữ nguyên `[{...}]`, **KHÔNG backfill / KHÔNG migrate** |

> Dev ghi rõ: **Không có thay đổi DB/config/constant.** Chỉ định dạng dữ liệu ghi vào cột `callback_event.request` đổi từ mảng events sang full body, áp dụng cho row mới.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Xử lý callback LINE** (message / postback / follow / unfollow / videoPlayComplete) **+ download media** — bắn event thật kèm ảnh/video, check row `callback_event` mới lưu full body và chạy tới status **DONE**, tin nhắn vào đúng phòng chat, scenario / tag / richmenu và tải file chạy bình thường | F1, F2, F3, D1 | **High** |
| T2 | **Tương thích row cũ** — để lại vài row format cũ `[{...}]` đang NEW/retry rồi restart job, phải parse và xử lý được, **không nhảy `STATUS_ERROR`** | F2, F3, D1 | **High** |
| T3 | **Forward webhook Kênh 1** — bên thứ 3 giờ nhận **nguyên body có cả `destination` và `events`** thay vì mảng trần; test lại endpoint đối tác, check **tiếng Nhật / emoji không bị escape** | F4, D1 | **High** |
| T4 | **Verify webhook URL trên LINE Developers** (LINE gửi `events` rỗng) — bấm **検証**, job không văng lỗi parse, row phải là **`STATUS_UNKNOWN_TYPE`** | F2, F3 | **Medium** |

---

## 5. Commit / Branch (nguyên văn từ Redmine)

- **5.1 Commit hoặc pull request**: `f6104a3`
- **5.2 Branch hiện tại của task**: `m_202609_forward_webhook_40475_release-callback`

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
