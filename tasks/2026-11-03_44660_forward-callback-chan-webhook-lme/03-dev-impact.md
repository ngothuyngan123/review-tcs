# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #44660 qua `/new-task` + đối chiếu `task_get_context(task_id=526, sections=[dev_impact, requirements, spec_delta])` của MCP LME TEST STUDIO.
>
> ⚠️ **Input gốc KHÔNG theo đúng format heading chuẩn** (`1. Nguyên nhân` / `2. Cách fix` / `3. Caller đã check` / `4.1-4.3`). Redmine #44660 ghi đánh giá ảnh hưởng dưới dạng **journal "Dev Studio"** (quy trình bàn giao AI dev, 3 lượt 2026-10-28 → 2026-11-02) — xem nguyên văn ở `01-bug-task.md`. AI đã **tổng hợp lại** theo cấu trúc 4 mục bên dưới từ nội dung journal + `dev_impact`/`requirements` của Studio (task #526). **Tester BẮT BUỘC đọc lại journal gốc trước khi tick checkbox verify.**

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `Dev Studio` (bàn giao tự động, `issue.assigned_to = -`) |
| Commit / Pull Request | `<chưa có PR link>` — commit HEAD: `sns-line@676e01b687cc2d70c455c210fe0eed4f77116ec1` (bản 3; bản 1 = `3ddf9d4c11c1`, bản 2 = `4d8510dcf864`) |
| Branch | `ai_studio_fixbug_44660` (gốc `release_step_20260930_v2` @`303a131b9c03`) |
| Ngày submit đánh giá | `2026-11-02` (journal #150058 — bản bàn giao cuối cùng, HEAD) |
| Auto-filled | `2026-11-03 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal gốc ở `01-bug-task.md` và xác nhận AI tổng hợp đúng, không sót impact.

---

## 1. Nguyên nhân

Ô 「転送先URL」 của cả hai kênh (tab LINE và tab LME) chỉ được kiểm ở server bởi `WebhookUrlValidator::validate()`, gồm 4 luật cũ: bắt buộc khi bật, `https://`, ≤1024 ký tự, chống SSRF (host ra IP public, cổng 443). **Không luật nào nhận diện URL webhook của chính LME** (`{DOMAIN_ENDPOINT_WEBHOOK}line/callback/add/{bot_id}`) — vì host LME là IP public, cổng 443, URL này vẫn pass 4 luật cũ và lưu được → tạo vòng lặp webhook. Spec `webhook-relay` §6.5 cũng thiếu luật này.

Bug con phát sinh trong lúc fix (**#44843**): ở bản 1 (`3ddf9d4c`), hàm `isLmeWebhookUrl()` **chưa rút gọn đoạn `.`/`..`** (kể cả `%2e`) trong path trước khi so khớp → URL dạng `/line/./callback/add/1` lách qua được. Đã vá ở bản 2 (`4d8510dcf8`), giữ ở bản 3/HEAD (`676e01b687cc`, xử lý thêm `\` / `%5C`).

## 2. Cách fix

- **D-1**: Thêm luật `isLmeWebhookUrl()` vào `WebhookUrlValidator` — sau khi **chuẩn hoá** path (decode `%xx`, đổi `\`/`%5C` → `/`, gộp `//`, rút gọn `.`/`..` không vượt gốc), nếu path chứa `/line/callback/add` → từ chối **HTTP 422**, lỗi 「このURLは転送先に指定できません。」hiện dưới ô URL, **không lưu**. Áp dụng **mọi domain, mọi bot_id**, không phân biệt hoa/thường, dù công tắc BẬT hay TẮT (miễn URL không rỗng).
- **D-2**: Unit test cho luật mới — `tests/Unit/WebhookUrlValidatorLmeWebhookTest.php` (29 ca ở bản HEAD).
- Luật path-based này **chạy trước** luật SSRF/DNS hiện có, trả cùng mã lỗi/message `URL_NOT_ALLOWED` như case SSRF/URL hỏng → **cần URL đối chứng cụ thể** khi viết TC (không chỉ dựa vào mã lỗi để phân biệt nguyên nhân chặn).
- Áp dụng cho **cả 2 tab** LINE (SCR-01) và LME (SCR-02), dùng chung qua `POST /admin/webhook-relay/save` (EP-02).
- **Không đổi** FE, DB, route, job Java, MCP. **Rủi ro mới**: chuẩn hoá path rộng hơn có thể vô tình chặn URL ngoài nếu path sau rút gọn trùng `/line/callback/add` (đúng chủ đích); ngược lại URL khác path (`/webhook`, `/line/callback`, `/line/callback/addx`) **phải vẫn lưu được** — đây là nguồn RISK cần TC verify không chặn nhầm (REQ-003).
- Cấu hình cũ đã lưu URL LME trước bản sửa: **không tự sửa** — vẫn hiển thị, job vẫn forward; lần `保存する` kế tiếp ở tab đó bị chặn (kể cả chỉ tắt switch) cho tới khi khách xoá/đổi URL (REQ-006).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `WebhookUrlValidator::validate()` / `isLmeWebhookUrl()` — `app/Services/WebhookRelay/WebhookUrlValidator.php` | Thêm luật path-based + bước chuẩn hoá path (`%xx`, `\`/`%5C`, `//`, `.`/`..`) | Chặn URL webhook LME lúc lưu, kể cả biến thể lách encode |
| 2 | `tests/Unit/WebhookUrlValidatorLmeWebhookTest.php` | Thêm 29 ca unit test | Cover luật mới + mọi biến thể encode path đã biết (bao gồm fix cho #44843) |
| 3 | `WebhookRelayService::save` → `POST /admin/webhook-relay/save` (EP-02) — **caller duy nhất** của validator theo Dev xác nhận | Không đổi route/logic khác, chỉ nhận lỗi 422 mới từ validator | Đảm bảo cả tab LINE + tab LME đều bị chặn (dùng chung 1 validator) |

> Dev xác nhận: "caller duy nhất `WebhookRelayService::save` → EP-02" — không có caller khác cần check thêm.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `WebhookUrlValidator::validate()` / `isLmeWebhookUrl()` | `app/Services/WebhookRelay/WebhookUrlValidator.php` | Direct | Luật mới + bước chuẩn hoá path; chạy trước SSRF/DNS, cùng mã lỗi `URL_NOT_ALLOWED` |
| F2 | `WebhookRelayService::save` → `POST /admin/webhook-relay/save` (EP-02) | (controller/service gọi F1) | Indirect | Nhận 422 mới từ F1 cho cả 2 tab (channel 1 LINE / channel 2 LME); input lạ không gây 5xx |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `webhook_relay_setting.endpoint_url` / `notify_endpoint_url` | **KHÔNG ĐỔI** (migration/diff: Dev xác nhận không có thay đổi dữ liệu) | Cấu hình cũ đã lưu URL webhook LME (nếu có) **không bị dọn tự động** — chỉ bị chặn ở lần `保存する` kế tiếp. Follow-up: Leader cân nhắc yêu cầu check production bằng `SELECT bot_id, is_enabled, notify_is_enabled FROM webhook_relay_setting WHERE endpoint_url LIKE '%/line/callback/add/%' OR notify_endpoint_url LIKE '%/line/callback/add/%'` |

> Không có migration / CREATE / UPDATE / DELETE nào — Dev xác nhận "đã kiểm diff".

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Webhook転送 — tab 「LINE公式アカウントデータ転送」 (SCR-01) | F1, F2 | High — chặn lưu mới đúng chủ đích, nhưng risk chặn nhầm URL ngoài hợp lệ có path trùng `/line/callback/add` sau chuẩn hoá (REQ-003) |
| T2 | Webhook転送 — tab 「L Messageデータ転送」 (SCR-02) | F1, F2 | High — tương tự T1, dùng chung validator |
| T3 | Job Java chuyển tiếp webhook (`HandleForwardCallbackEventTask` / `HandleForwardLmeEventTask`, module job) | D1 (cấu hình cũ chưa dọn) | Medium — **không đổi trong task này**; cấu hình cũ trỏ webhook LME vẫn được job forward tới. Dev đề xuất ticket riêng — **ngoài phạm vi task hiện tại, không đẻ TC ở đây** |
| T4 | Spec `admin/webhook-relay/` §6.5 | Nguyên nhân (spec thiếu luật) | Low — cần update spec sau khi fix (follow-up riêng, không phải TC) |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót) — Dev đã xác nhận caller duy nhất
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — Dev xác nhận không có migration
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — chú ý REQ-003 (không chặn nhầm URL ngoài)
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
