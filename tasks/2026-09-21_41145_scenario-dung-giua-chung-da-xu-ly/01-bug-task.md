# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41145 — [Scenario] Sửa lỗi kịch bản (scenario) bị dừng giữa chừng khi nhiều xử lý chạy cùng lúc` |
| Module / Màn hình | Scenario (ステップ配信) — job gửi step theo giờ hẹn · start/stop scenario từ auto reply / action / thêm bạn mới / gắn tag · màn danh sách scenario (số người đang nhận / chưa hoàn thành) |

## Mô tả bug (bản dịch tiếng Việt)

■ Hiện tượng trước khi sửa

Khi hai xử lý cùng đụng tới lịch gửi step của cùng một người bạn tại cùng thời điểm, hệ thống báo lỗi và bỏ dở phần việc còn lại. Hậu quả đã ghi nhận trên môi trường thật:

- Có bạn bị dừng scenario cũ nhưng KHÔNG được đưa vào scenario mới → không nhận được các tin của scenario mới
- Số người "đang nhận scenario" / "chưa hoàn thành" hiển thị ở màn hình scenario bị lệch.

■ Nội dung sửa

1. Lúc đến giờ hẹn, hệ thống gửi step cho rất nhiều bạn cùng lúc. Việc dọn lịch gửi đã xong của từng bạn có thể bị tranh nhau và báo lỗi, làm dừng luôn phần việc còn lại của lần gửi đó (chạy action kèm theo, cập nhật kết quả gửi).
   → Đã cho thử lại vài lần; nếu vẫn không được thì chỉ ghi log, không làm dừng phần còn lại.

2. Khi một tin nhắn kích hoạt cùng lúc hai xử lý ngược nhau (ví dụ: một auto reply dừng scenario, một auto reply khác bật scenario mới), hai bên cùng dọn lịch gửi của người bạn đó và báo lỗi, khiến scenario mới không được bật.
   → Đã sửa lại cách dọn lịch gửi để không còn phát sinh lỗi này.

Không đổi màn hình, không đổi dữ liệu hay cấu hình. Chỉ sửa xử lý bên trong.

■ Phạm vi cần test lại

- Bật scenario cho bạn (từ auto reply, action, thêm bạn mới, gắn tag)
- Dừng scenario / đổi sang scenario khác
- Bạn chặn bot hoặc hủy kết bạn
- Scenario gửi theo giờ hẹn cho nhiều bạn cùng lúc

■ Gợi ý test case (nguyên văn của Dev)

1. Bạn mới thêm bot → nhắn ngay từ khóa khớp 2 auto reply (1 cái gỡ tag + dừng scenario, 1 cái gắn tag + bật scenario khác).
   → Mong đợi: bạn nằm đúng scenario mới, tag đúng, không có lỗi, các step sau vẫn đến đúng giờ.
2. Đang trong scenario → dừng scenario → không còn tin nào của scenario được gửi tiếp.
3. Đang trong scenario → đổi sang scenario khác → chỉ nhận step của scenario mới.
4. Đang trong scenario → chặn bot / hủy kết bạn → không nhận thêm step. Kết bạn lại → chạy đúng theo thiết lập thêm bạn.
5. Hẹn giờ scenario cho vài chục bạn vào cùng một mốc phút → tất cả nhận đủ tin, không ai bị thiếu, trạng thái gửi hiển thị đúng.
6. Mở màn hình scenario, đối chiếu số người đang nhận scenario với thực tế → phải khớp.

## Steps to reproduce

<!-- Ticket không có section "Tái hiện bug" theo format chuẩn. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #41145 không có attachment. Log prod được Dev trích trong journal (xem cuối file). -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được bằng thao tác tay theo kịch bản cố định** — đây là **race condition** (`Bug tự detect`), chỉ xảy ra khi 2 luồng cùng xoá `scenario_step_time` của cùng 1 friend tại cùng thời điểm. Root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify **cách fix** (bulk DELETE không ném exception khi xoá 0 row · retry deadlock 1213) + **regression impact**.
- **Tần suất lỗi trên prod**: log ngày 18/09 ghi nhận **5 lần** `StaleStateException` — KHÔNG phải 100% lần nào cũng lỗi. Reproduce cần ép đồng thời (2 auto reply ngược nhau trên cùng 1 tin nhắn, hoặc job gửi step hàng loạt).
- **Môi trường phát hiện**: Production (log prod 18/09).
- Fix **không đổi schema, không migration, không đổi màn hình** → mọi TC đổi UI/data đều nằm ngoài phạm vi; trọng tâm là hành vi job + tính nhất quán số đếm.
- ⚠️ Bug đã làm **lệch `count_follow` / `count_unfinish`** của scenario trên dữ liệu prod cũ. Bản vá **không tự sửa** dữ liệu đã lệch từ trước → cần phân biệt "số lệch do bug cũ" và "số lệch mới phát sinh sau khi deploy".
- Branch: `m_202608_bug_detect_delete_scenario_step_time` · Commit: `938c171` + `a83d475`.

## Journal / note từ Redmine (nguyên văn)

**Journal #137276 — Thanh Duy Nguyen — 2026-09-20:**

```
Bug tự detect #41145 [Scenario] Sửa lỗi kịch bản (scenario) bị dừng giữa chừng khi nhiều xử lý chạy cùng lúc

1. Nguyên nhân
   - 3 method xoá scenario_step_time đang là derived delete của Spring Data (SELECT row rồi DELETE theo từng id); luồng khác xoá cùng row trước thì DELETE được 0 row → org.hibernate.StaleStateException "Batch update returned unexpected row count from update [0]" tại ScenarioModel.java:481 và :510 (log prod 18/09 có 5 lần).
   - Exception làm bỏ dở phần việc còn lại: friend bị dừng scenario cũ nhưng không được đưa vào scenario mới; count_follow/count_unfinish của scenario bị trừ 2 lần.

2. Cách fix
   - 938c171: đổi 3 method delete trong ScenarioStepTimeRepository sang bulk DELETE bằng @Query(nativeQuery = true) — xoá 0 row vẫn là thành công, không ném exception; giữ nguyên tên và signature.
   - a83d475: retry tối đa 3 lần (delay tăng dần) cho deleteById step vừa gửi trong SentMessageHelper.actionStepSend khi gặp deadlock MySQL 1213; hết retry chỉ log + notify, không ném ra ngoài làm mất phần chạy action và cập nhật kết quả gửi.

3. Đã check và sửa các function sử dụng đến function/data vừa sửa
   - 5 caller của 3 method delete: ScenarioModel.java:448, :481, :510, BotLineUserModel.java:108, HandlePostbackTask.java:2211 — đều gọi dạng void, không dùng giá trị trả về, signature không đổi nên không phải sửa caller nào.
   - Bảng scenario_step_time có index user_id và bot_id_2 (bot_id, user_id) nên câu DELETE mới chỉ khoá row của đúng friend, không quét cả bảng.

4. Đánh giá ảnh hưởng
        4.1 List function
            - SentMessageHelper.actionStepSend (thêm deleteScenarioStepTime, sleepQuietly)
            - ScenarioStepTimeRepository.deleteAllByUserIdAndBotId / deleteAllByUserIdAndBotIdAndStatus / deleteAllByBotIdAndUserIdAndStatus
            - ScenarioModel.stopFollowingScenario, ScenarioModel.startScenarioWithCreatedSentNow
            - BotLineUserModel.unFollow, HandlePostbackTask.doHandleUnFollowEvent
        4.2 List những data bị update khi fix bug
            - Không có (không đổi schema, SQL migration, config hay hằng số; chỉ đổi cách thực thi câu xoá)
        4.3 Dựa vào 2 mục trên list những tính năng sẽ ảnh hưởng
            - Bật scenario cho friend (auto reply / action / thêm bạn mới / gắn tag): friend mới nhắn từ khoá khớp 2 auto reply ngược nhau, check vào đúng scenario mới
            - Dừng / đổi scenario: check không còn nhận step của scenario cũ
            - Friend chặn bot hoặc hủy kết bạn: check không nhận thêm step, kết bạn lại chạy đúng thiết lập thêm bạn
            - Scenario gửi theo giờ hẹn cho nhiều friend cùng lúc: check không friend nào bị thiếu tin, trạng thái gửi đúng
            - Màn hình scenario: check số người đang nhận scenario khớp thực tế

5. Commit / Branch
        5.1 Commit hoặc pull request
            - a83d475 + 938c171
        5.2 Branch hiện tại của task
            - m_202608_bug_detect_delete_scenario_step_time
```
