# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #41139 — **Journal #137972** (Thanh Duy Nguyen, 2026-09-23, "📊 Báo cáo đánh giá ảnh hưởng (AI tạo tự động)"). Description Redmine không có Section "Đánh giá ảnh hưởng" riêng; báo cáo trong journal dùng format 5 mục (Mục đích / Cách thực hiện / Đã check / Đánh giá ảnh hưởng / Commit) → map sang 4 mục template.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Do Van Tu TuDV (journal #137563, #137835) · báo cáo impact đăng bởi Thanh Duy Nguyen (AI tạo tự động) |
| Commit / Pull Request | Commit `3672558d429f6da176a9871b449af4f99a9eff1f` (chưa có link PR) |
| Branch | `m_202609_check-bot-contract-status_41139` (base `release-t08-2026`) |
| Ngày submit đánh giá | 2026-09-23 |
| Auto-filled | 2026-09-25 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

(Mục "1. Mục đích" của báo cáo — nguyên văn)

- Bot đã huỷ hợp đồng nhưng vẫn giữ kết nối LINE official thì các job phía LME (あいさつメッセージ khi thêm bạn, hiển thị richmenu, action, callback) vẫn chạy và ghi đè cài đặt của LINE official.
- Bổ sung điều kiện chặn theo `bot_contracts.status = 3` (đã huỷ hđ) bên cạnh 2 điều kiện cũ là `expired_date` quá hạn 7 ngày và `status_bill_fail = 5`.

## 2. Cách fix

(Mục "2. Cách thực hiện" — nguyên văn)

- Thêm `BotRepository.findContractStatusByBotId`: `bots.id` -> `bot_slots.bot_id` -> `bot_slots.bot_contract_id` -> `bot_contracts.status` (join giống `findContractTypeById` sẵn có).
- Thêm `BotContractManager` cache kết quả 1 phút/bot; `Bot.isExpiredOver7Day` gọi thêm nhánh chặn khi `expired_date` đã quá hạn và contract status = 3. Chỉ query khi `expired_date` hợp lệ và nhỏ hơn hiện tại nên bot đang chạy bình thường không phát sinh query.

Bổ sung từ journal #137835 (Dev): bot chưa hết hạn chỉ chuyển được về trạng thái chờ cancel và vẫn dùng bình thường; khi bot hết hạn, job crontab mới tự động chuyển sang cancel → chỉ cần check status hợp đồng khi bot đã hết hạn.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Bot.isExpiredOver7Day` — cổng dùng chung của **24 caller** (ActionService, DelayMessageService, ActionScheduleBotTask, NewScenarioTaskV3, SettingDisplayRichMenuHistoriesThread, BroadcastNewJob, HandlePostbackTask, các HandlePushNotify*...) | Sửa: thêm nhánh chặn theo contract status | Signature không đổi nên không caller nào phải sửa, tất cả tự hưởng điều kiện chặn mới. |
| 2 | 4 query lọc sẵn trong `NotifySettingRepository` | Giữ nguyên | Tầng Java vẫn tự check nên không cần thêm join vào SQL. |

⚠️ Dev chỉ nêu 7/24 caller theo tên ("..."), chưa có danh sách đầy đủ 24 caller.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `Bot.isExpiredOver7Day` | `<chưa rõ>` (Bot.java) | Direct | Cổng dùng chung 24 caller |
| F2 | `Bot.isExpiredDatePassed` (mới) | `<chưa rõ>` (Bot.java) | Direct | |
| F3 | `BotContractManager.isContractCancelled` | `src/main/java/sns/line/helper/BotContractManager.java` (file mới) | Direct | Cache 1 phút/bot |
| F4 | `BotRepository.findContractStatusByBotId` (mới) | `<chưa rõ>` (BotRepository) | Direct | Join bots → bot_slots → bot_contracts |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | Không có | — | Chỉ đọc thêm `bot_contracts.status` và `bot_slots.bot_contract_id`, không có DDL/migration/config thay đổi. |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Lời chào khi thêm bạn và richmenu: test bot có `bot_contracts.status = 3` và `expired_date` quá hạn thì LME không gửi lời chào, không set richmenu nữa. | F1–F4 | `<Dev không ghi>` |
| T2 | Action schedule, scenario, delay message, broadcast: test bot hợp đồng còn hiệu lực (status 0/1/2) vẫn chạy bình thường, không bị chặn nhầm. | F1 | `<Dev không ghi>` |
| T3 | Thông báo App/PC/Chatwork: test bot đã huỷ hợp đồng thì ngừng đẩy notify. | F1 | `<Dev không ghi>` |
| T4 | Bot free plan hoặc `expired_date` rỗng: test không phát sinh query `bot_contracts` (giữ nguyên hành vi cũ). | F2, F4 | `<Dev không ghi>` |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
