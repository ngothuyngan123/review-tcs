# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Thanh Duy Nguyen |
| Commit / Pull Request | `938c171` + `a83d475` |
| Branch | `m_202608_bug_detect_delete_scenario_step_time` |
| Ngày submit đánh giá | 2026-09-20 |
| Auto-filled | `2026-09-21 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

- 3 method xoá `scenario_step_time` đang là **derived delete của Spring Data** (SELECT row rồi DELETE theo từng id); luồng khác xoá cùng row trước thì DELETE được 0 row → `org.hibernate.StaleStateException` "Batch update returned unexpected row count from update [0]" tại `ScenarioModel.java:481` và `:510` (log prod 18/09 có 5 lần).
- Exception làm **bỏ dở phần việc còn lại**: friend bị dừng scenario cũ nhưng không được đưa vào scenario mới; `count_follow` / `count_unfinish` của scenario bị trừ 2 lần.

## 2. Cách fix

- **938c171**: đổi 3 method delete trong `ScenarioStepTimeRepository` sang **bulk DELETE** bằng `@Query(nativeQuery = true)` — xoá 0 row vẫn là thành công, không ném exception; **giữ nguyên tên và signature**.
- **a83d475**: **retry tối đa 3 lần (delay tăng dần)** cho `deleteById` step vừa gửi trong `SentMessageHelper.actionStepSend` khi gặp **deadlock MySQL 1213**; hết retry chỉ **log + notify**, không ném ra ngoài làm mất phần chạy action và cập nhật kết quả gửi.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `ScenarioModel.java:448` | Không sửa | Gọi dạng `void`, không dùng giá trị trả về, signature không đổi |
| 2 | `ScenarioModel.java:481` | Không sửa | Nt — đây là 1 trong 2 điểm ném `StaleStateException` trên log prod |
| 3 | `ScenarioModel.java:510` | Không sửa | Nt — điểm ném `StaleStateException` thứ 2 trên log prod |
| 4 | `BotLineUserModel.java:108` | Không sửa | Gọi dạng `void`, signature không đổi |
| 5 | `HandlePostbackTask.java:2211` | Không sửa | Gọi dạng `void`, signature không đổi |

> Ghi chú của Dev: bảng `scenario_step_time` có index `user_id` và `bot_id_2` (`bot_id`, `user_id`) nên câu DELETE mới **chỉ khoá row của đúng friend**, không quét cả bảng.

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `SentMessageHelper.actionStepSend` | `SentMessageHelper.java` | Direct | Thêm `deleteScenarioStepTime`, `sleepQuietly` — retry 3 lần khi deadlock 1213 |
| F2 | `ScenarioStepTimeRepository.deleteAllByUserIdAndBotId` | `ScenarioStepTimeRepository.java` | Direct | Đổi sang bulk DELETE `@Query(nativeQuery = true)` |
| F3 | `ScenarioStepTimeRepository.deleteAllByUserIdAndBotIdAndStatus` | `ScenarioStepTimeRepository.java` | Direct | Nt |
| F4 | `ScenarioStepTimeRepository.deleteAllByBotIdAndUserIdAndStatus` | `ScenarioStepTimeRepository.java` | Direct | Nt |
| F5 | `ScenarioModel.stopFollowingScenario` | `ScenarioModel.java` | Indirect (caller) | Điểm ném exception cũ (`:481` / `:510`) |
| F6 | `ScenarioModel.startScenarioWithCreatedSentNow` | `ScenarioModel.java` | Indirect (caller) | Bật scenario mới — nơi bị bỏ dở khi exception |
| F7 | `BotLineUserModel.unFollow` | `BotLineUserModel.java` | Indirect (caller) | Hủy kết bạn / chặn bot |
| F8 | `HandlePostbackTask.doHandleUnFollowEvent` | `HandlePostbackTask.java` | Indirect (caller) | Xử lý event unfollow từ LINE |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | **Không có** | — | Dev khẳng định: không đổi schema, SQL migration, config hay hằng số; **chỉ đổi cách thực thi câu xoá** trên bảng `scenario_step_time` |

> ⚠️ Leader lưu ý: tuy Dev ghi "không có data bị update", **hành vi runtime** trên 2 bảng vẫn thay đổi → cần theo dõi khi viết TC:
> - `scenario_step_time` — cách xoá đổi từ per-id sang bulk DELETE.
> - `scenario.count_follow` / `scenario.count_unfinish` — trước fix bị trừ 2 lần; sau fix phải đúng. **Dữ liệu đã lệch từ trước KHÔNG được bản vá tự sửa.**

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Bật scenario cho friend (auto reply / action / thêm bạn mới / gắn tag) — friend mới nhắn từ khoá khớp **2 auto reply ngược nhau**, check vào đúng scenario mới | F2, F3, F4, F6 | High |
| T2 | Dừng / đổi scenario — check không còn nhận step của scenario cũ | F2, F3, F4, F5 | High |
| T3 | Friend chặn bot hoặc hủy kết bạn — check không nhận thêm step; kết bạn lại chạy đúng thiết lập thêm bạn | F7, F8 | High |
| T4 | Scenario gửi theo giờ hẹn cho **nhiều friend cùng lúc** — check không friend nào bị thiếu tin, trạng thái gửi đúng | F1 | High |
| T5 | Màn hình scenario (ステップ配信) — check số người đang nhận scenario khớp thực tế | F5, F6 | Medium |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

<!-- Auto-filled 2026-09-21 by /new-task từ Redmine #41145 journal #137276 (nguyên văn). -->
