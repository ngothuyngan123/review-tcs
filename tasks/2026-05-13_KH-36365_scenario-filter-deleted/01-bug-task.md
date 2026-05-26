# 01 — Bug Task từ khách hàng

> Overwrite từ Redmine #36365 ngày 2026-05-13 (auto-fill từ data fetch qua REST API). Raw JSON: [_redmine-36365-raw.json](_redmine-36365-raw.json).

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | KH #36365 (回答ID 10833) |
| Redmine URL | https://redmine.watermelon.vn/issues/36365 |
| Auto-filled | `2026-05-13 by /write-tc` (REST fetch) |
| Tracker / Category | Bug KH / Scenario |
| Status | New |
| Priority (Redmine) | Normal |
| Parent issue | #36192 |
| Author | AI CSS (id 160) |
| Assignee | Kieu Son Tung (id 80) |
| Ngày báo cáo (created_on) | 2026-05-11 |
| Updated_on | 2026-05-13 |
| Khách hàng / Bot | User `sokuyaku0601@gmail.com` — Bot `AURORA CLINIC` |
| Module / Màn hình | Scenario → Step message → Modal tạo step (có filter manager) |
| Môi trường phát hiện | Production (suy luận theo bot_id thực) |

## Mô tả bug (nguyên văn description từ Redmine)

> **Subject:** [11-05-2026][10833][Scenario] Friend 「さや」: ステップ配信「問診票＋1H、1日、2日」 mốc 01時間00分後 gửi 2 lần (duplicate)

```
User: sokuyaku0601@gmail.com
Bot Name: AURORA CLINIC

Đối với friend 「さや」, trên ステップ配信「問診票＋1H、1日、2日」, message ở mốc 01時間00分後 (sau 1 giờ 0 phút) đã được gửi **2 lần** (2通送信されている) — bị duplicate send.

Link Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0B30GSMLRF
```

### 原文 (JP)

```
友だち「さや」に対して、ステップ配信「問診票＋1H、1日、2日」の01時間00分後のメッセージが2通送信されている。
```

TaskRef: `user_report:Rec0B30GSMLRF`

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — đã đọc lại Redmine 36365 (description + 3 journals + 2 attachments) và xác nhận:
  - Description match nguyên văn customer report
  - Steps to reproduce + dev impact (journal #118250) đầy đủ
  - 2 ảnh attachment đã được kiểm tra (id 25682, 25683)
  - Không bỏ sót journal nào

## Steps to reproduce (theo journal #118250 — Ngần phân tích)

1. User mở **2 tab** tạo scenario (cùng browser, cùng login session)
2. **Tab 1** → Tạo 1 filter → Thực hiện **xóa filter**
3. **Tab 2** → Thực hiện tạo 1 step trong màn filter đó (KH tạo step `send sau XX giờ`)

## Expected result

- Tab 2 khi tạo step phải **fail** vì filter đã bị xóa ở tab 1 → hiển thị msg `フィルターが削除されたため、画面を再読み込みしてください` (filter đã bị xóa, vui lòng reload màn hình)
- DB **không tạo** scenario_step với `filter_id` đã xóa
- LINE user **không nhận** message duplicate

## Actual result

- Tab 2 **vẫn add** step message vào scenario với `filter_id` đã bị xóa
- Hệ quả ngoài LINE: scenario chạy step → message mốc `01時間00分後` bị gửi **2 lần** ra friend 「さや」
- DB state thực tế (journal #117866 — Ngần check):
  - `bot_id=68612`
  - `scenario_id=256461`
  - `line_id=43413410`
  - `message_id=1958315734, 1958315735` (1 msg text bị duplicate)
  - line_id tương tự cùng pattern: `44512507`, `52493370`

## Ảnh / video / log đính kèm

- [x] Có screenshot — 2 file (Redmine attachment id 25682, 25683):
  - [SnapCrab_NoName_2026-5-11_17-35-36_No-00.png](https://redmine.watermelon.vn/attachments/download/25682/SnapCrab_NoName_2026-5-11_17-35-36_No-00.png) (115 KB)
  - [SnapCrab_NoName_2026-5-11_17-36-45_No-00.png](https://redmine.watermelon.vn/attachments/download/25683/SnapCrab_NoName_2026-5-11_17-36-45_No-00.png) (52 KB)
- [ ] Có video
- [x] Có log DB — 3 line_id (43413410, 44512507, 52493370) phát hiện cùng pattern duplicate trên prod

## Journals (full timeline)

| ID | Người | Thời gian | Nội dung |
|---|---|---|---|
| 117865 | AI CSS | 2026-05-11 08:50 | Edit lại subject + description (chuẩn hóa wording JP) |
| 117866 | Ngô Thúy Ngần | 2026-05-11 08:56 | Identify DB: bot_id=68612, scenario_id=256461, line_id=43413410, message_id=1958315734/1958315735 duplicate. Phát hiện line_id tương tự: 44512507, 52493370 |
| 118250 | Ngô Thúy Ngần | 2026-05-13 08:12 | **Phân tích bug + dev impact** — cách tái hiện 2-tab race, root cause (filter đã xóa nhưng GUI không refresh), cách fix (validate filter_id + remove try/catch swallow), function impact (`createScenarioStep` trong `ScenarioController.php`) |

## Ghi chú thêm của Leader

- Đây là **race condition** classic giữa 2 tab + state stale (filter manager bị xóa ở tab 1, tab 2 vẫn dùng filter_id stale).
- Root cause: function `createScenarioStep` không validate filter_id còn tồn tại trước khi insert step.
- Dev đã note "Xóa try/catch để notify chatwork" → nghĩa là code cũ swallow exception → bug không được alert sớm.
- Câu hỏi mở (Leader cần verify khi review):
  - Bug ngoài LINE là **duplicate send** — nhưng dev fix chỉ chặn ở step "create step với filter đã xóa". **Liên kết giữa step có filter_id stale → duplicate send** chưa được làm rõ trong dev impact. Có thể cần thêm journal hoặc verify với dev.
  - Các loại step khác (send ngay, send sau XX ngày, send theo giờ cố định) có cùng vấn đề?
  - Function `updateScenarioStep` (edit step) có cùng vấn đề không? — dev chỉ list `createScenarioStep`.
  - Filter bị xóa bởi **chính user** ở tab 1 — có scenario filter bị xóa bởi **user khác** (cross-staff trong cùng bot) không?
  - 3 line_id (43413410, 44512507, 52493370) đều thuộc cùng bot_id=68612 hay khác bot?
