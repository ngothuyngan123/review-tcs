# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 25-30: Job gửi step · Job khi edit step đang chạy
· Chống lặp vô hạn · Trùng line_user · Backup & đổi bot · Phân quyền & môi trường.

Nguồn: tab「Job scenario」(Bug #32469 10/2025 · Bug lặp vô hạn · Bug #32802 11/2025)
· tab「Testcase」r876-r962 (Bug #32281 10/2025) · tab「text fix bug Kh」(Bug KH #37711 06/2026)
· tab「Scenario write DB riêng」·「Improve sendall scenario」(TCsLine_Improve chung)
·「Phân quyền」(11/2023).
"""
from _common import tc

JOB = ("- Bot A trên môi trường có job scenario (NewScenarioTaskV3) đang chạy\n"
       "- Scenario S1 thuộc bot A; friend test đã kết bạn với bot A")
TWO_BOT = ("- Bot A và Bot B CÙNG provider\n- Friend test đã kết bạn với CẢ 2 bot\n"
           "- Cả 2 bot đều có scenario đang chạy cho friend đó")

S6 = [
    # ══════════════════ 25. Job gửi step & is_last_step ══════════════════
    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job gửi step bình thường (is_last_step = 0) → gửi được message, lưu lịch sử, KHÔNG stop scenario, trigger + profile sender đúng",
       JOB + "\n- S1 có 3 step; friend đang chạy, sắp tới step giữa (không phải step cuối)",
       "1. Chờ tới giờ gửi step giữa\n2. Quan sát LINE app friend: nội dung + tên/ảnh người gửi\n"
       "3. Mở màn my_page của friend → kiểm tra lịch sử gửi step\n4. Mở chat 1:1 → kiểm tra trigger của step message\n"
       "5. Query `step_message_history` (status) + `scenario_lineuser`.`is_following`",
       "Step giữa của scenario 3 step, có set profile 送信者A",
       "- LINE app nhận đúng message, người gửi hiển thị đúng 送信者A\n"
       "- Màn my_page có lịch sử gửi step này\n- Chat 1:1 hiển thị trigger của step message\n"
       "- `step_message_history` có bản ghi status = 2\n- `scenario_lineuser`.`is_following` VẪN = 1 (không stop)",
       env="PRODUCTION",
       note="RULE-06 + RULE-07 + RULE-08. Nguồn:「Job scenario」r247"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job gửi step CUỐI (is_last_step = 1) — KHÔNG có next scenario → gửi xong thì STOP scenario cho friend",
       JOB + "\n- S1 có 3 step, KHÔNG setting next scenario; friend sắp tới step cuối",
       "1. Chờ tới giờ gửi step cuối\n2. Quan sát LINE app + màn my_page\n"
       "3. Query `scenario_lineuser`.`is_following` + 3 counter của S1\n4. Kiểm tra trigger trên chat 1:1",
       "S1 3 step, không next scenario",
       "- Friend nhận message step cuối, profile sender đúng\n- my_page lưu lịch sử gửi và hiển thị scenario ĐÃ DỪNG\n"
       "- `scenario_lineuser`.`is_following` chuyển sang trạng thái hoàn thành\n- Counter cập nhật tương ứng",
       env="PRODUCTION",
       note="MT-01 liên quan (is_following = 0 hay 2 khi hoàn thành). Nguồn:「Job scenario」r248, r51, r53"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job gửi step CUỐI — CÓ next scenario → gửi xong thì stop scenario này và start scenario kế tiếp",
       JOB + "\n- S1 có 3 step, có setting next = S2; friend sắp tới step cuối",
       "1. Chờ tới giờ gửi step cuối của S1\n2. Quan sát LINE app + my_page\n"
       "3. Query `scenario_lineuser` của S1 và S2\n4. Kiểm tra trigger next scenario trên chat 1:1",
       "S1 3 step, next = S2",
       "- Friend nhận message step cuối của S1\n- my_page hiển thị step của NEXT SCENARIO (S2) sau khi gửi xong step cuối\n"
       "- `scenario_lineuser`: S1 chuyển trạng thái kết thúc, S2 tạo bản ghi mới is_following = 1",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r249, r52, r54"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job gửi step có FILTER: friend thoả filter nhận msg; friend không thoả → không nhận và chat 1:1 hiển thị trigger 'không thoả mãn filter'",
       JOB + "\n- S1 có filter F-A (điều kiện tag「A」); 2 friend: 「たろう」có tag A, 「はなこ」không có",
       "1. Start S1 cho cả 2 friend\n2. Chờ tới giờ gửi step của F-A\n3. Kiểm tra LINE app của cả 2 friend\n"
       "4. Mở chat 1:1 của từng friend → đọc trigger\n5. Query `step_message_history` của 2 friend\n"
       "6. Kiểm tra my_page của 2 friend",
       "friend「たろう」(tag A) ·「はなこ」(không tag)",
       "-「たろう」: nhận message, chat 1:1 hiển thị trigger step message, `step_message_history` status = 2\n"
       "-「はなこ」: KHÔNG nhận message; chat 1:1 hiển thị「このメッセージは配信（絞り込み）対象外のため送信されていません。」\n"
       "- my_page cả 2 friend đều lưu lịch sử gửi step\n- Profile sender hiển thị đúng ở cả LINE app và chat 1:1",
       env="PRODUCTION",
       note="RULE-07. Nguồn:「Job scenario」r250, r1056, r1057"),

    tc("Job gửi step & is_last_step", "JOB-001", "Boundary",
       "Bug #32469: is_last_step xác định theo THỜI GIAN ĐẶT LỊCH THỰC TẾ, không theo thứ tự setting — 4 tổ hợp step 経過時間 vs 日時で指定",
       JOB + "\n- Start scenario lúc 10:00 ngày 24/10\n- Chuẩn bị 4 scenario với 4 tổ hợp step dưới đây",
       "1. Với mỗi tổ hợp: start scenario cho friend lúc 10:00 ngày 24/10\n"
       "2. Query `scenario_step_time`.`is_last_step` của các step\n"
       "3. Theo dõi my_page: sau mỗi lần gửi, hiển thị next step hay stop scenario\n4. Đối chiếu với send_time thực tế",
       "① 経過時間 22h + 日時 0日後 16:00 (→ 経過時間 muộn hơn)\n"
       "② 経過時間 1 phút + 日時 0日後 21:00 (→ 日時 muộn hơn)\n"
       "③ 経過時間 23h59 + 日時 1日後 01:00 (→ 経過時間 muộn hơn)\n"
       "④ 経過時間 10h + 日時 1日後 21:00 (→ 日時 muộn hơn)",
       "- ①: step 経過時間 có `is_last_step` = 1; my_page: gửi xong 日時 → hiện next step, gửi xong 経過時間 → stop\n"
       "- ②: step 日時 có is_last_step = 1\n- ③: step 経過時間 có is_last_step = 1\n- ④: step 日時 có is_last_step = 1\n"
       "- Quy tắc chung: step nào có SEND_TIME THỰC TẾ MUỘN NHẤT (số giây lớn hơn) là is_last_step",
       env="PRODUCTION",
       note="Bug #32469 (18-10-2025). 4 tổ hợp minh hoạ CÙNG 1 quy tắc → giữ chung 1 TC boundary. "
            "⚠️ Nhiều dòng trong corpus có kết quả『Pending』(r61, r63, r65, r67, r69, r71) — chưa test hết. "
            "Nguồn:「Job scenario」r56-r65"),

    tc("Job gửi step & is_last_step", "JOB-001", "Boundary",
       "Bug #32469: scenario có 3 step (2 経過時間 + 1 日時) → is_last_step vẫn theo send_time thực tế; my_page hiển thị next step đúng theo thứ tự thời gian",
       JOB + "\n- Start scenario lúc 10:00 ngày 24/10; 3 tổ hợp 3 step dưới đây",
       "1. Với mỗi tổ hợp, start cho friend lúc 10:00 ngày 24/10\n"
       "2. Query `scenario_step_time`.`is_last_step`\n3. Theo dõi my_page sau mỗi lần gửi",
       "① 経過時間1 22h · 日時 1日後 01:00 · 経過時間2 1h\n"
       "② 経過時間1 10h · 日時 1日後 10:00 · 経過時間2 1h\n"
       "③ 経過時間1 1h · 日時 1日後 01:00 · 経過時間2 22h",
       "- ①: 経過時間1 (22h) là is_last_step = 1; my_page: 経過時間2 → 日時 → 経過時間1 → stop\n"
       "- ②: step 日時 là is_last_step = 1; my_page: 経過時間2 → 経過時間1 → 日時 → stop\n"
       "- ③: 経過時間2 (22h) là is_last_step = 1; my_page: 経過時間1 → 日時 → 経過時間2 → stop",
       env="PRODUCTION",
       note="Bug #32469. ⚠️ Corpus r67/r69/r71 (case có next scenario) đều『Pending』. Nguồn:「Job scenario」r66-r71"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Bug #32469: quy tắc is_last_step áp dụng đúng cho CẢ 3 nguồn start — từ job autoreply, từ job action button, và từ NEXT SCENARIO",
       JOB + "\n- Scenario có step 経過時間 22h + step 日時 0日後 16:00; start lúc 10:00 ngày 24/10",
       "1. Start scenario qua job AUTOREPLY → query `scenario_step_time`.`is_last_step` + theo dõi my_page\n"
       "2. Start qua job ACTION BUTTON → lặp\n3. Start qua NEXT SCENARIO (từ scenario trước đó) → lặp\n"
       "4. Start từ WEB (chat 1:1) → lặp để đối chiếu",
       "4 nguồn start; scenario 2 step (経過時間 22h + 日時 0日後 16:00)",
       "- Cả 4 nguồn: step 経過時間 có `is_last_step` = 1 (send_time muộn hơn)\n"
       "- my_page: gửi xong 日時 → hiện next step; gửi xong 経過時間 → stop scenario (hoặc hiện next scenario nếu có setting)",
       env="PRODUCTION",
       note="Bug #32469. 4 nguồn cùng 1 kết quả → giữ chung. Nguồn:「Job scenario」r51-r107"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Bug #32469: edit / thêm / xoá step SAU KHI đã start scenario → is_last_step được tính lại đúng",
       JOB + "\n- Scenario có 3 step: send ngay + 経過時間 10h + 日時 1日後 10:00; friend đang chạy\n"
       "- ⚠️ Cần BẬT JOB WEB trước khi test các case edit này",
       "1. Bật job web\n2. Edit time của 1 step → query `scenario_step_time`.`is_last_step` của tất cả step\n"
       "3. Thêm step mới (loại 日時で指定) sau khi start → query lại\n"
       "4. Xoá 1 step (kể cả step đang là is_last_step) → query lại\n"
       "5. Xoá 1 folder filter chứa step is_last_step → query lại\n"
       "6. Xoá toàn bộ step trong 1 folder filter chứa is_last_step → query lại",
       "3 step; 5 loại thao tác sau khi start",
       "- Sau MỖI thao tác: `is_last_step` = 1 luôn thuộc về step có send_time thực tế MUỘN NHẤT còn pending\n"
       "- Step trước đó đang là is_last_step = 1 được update về 0 nếu không còn muộn nhất",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-38 — corpus ghi rõ『RIÊNG CÁC CASE EDIT NÀY PHẢI BÁO WEB BẬT JOB』→ có phụ thuộc cấu hình môi trường chưa "
            "được spec ghi nhận. Nhiều dòng r77/r78/r102-r104 để『Pending』. Nguồn:「Job scenario」r72-r78, r100-r104"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job send message hoạt động bình thường: friend kết bạn 1 bot / 2 bot → gửi đúng step và next đúng scenario của TỪNG bot",
       TWO_BOT,
       "1. Friend chỉ kết bạn bot A: start scenario A → chờ gửi step + next scenario → kiểm tra LINE app\n"
       "2. Friend kết bạn CẢ bot A và bot B, cả 2 bot đều có scenario đang chạy\n"
       "3. Chờ tới giờ gửi step của cả 2 bot → kiểm tra LINE app từng OA\n"
       "4. Chờ cả 2 scenario chạy xong → kiểm tra next scenario của từng bot\n"
       "5. Query `scenario_step_time` / `step_message_history` theo từng bot_id",
       "Friend kết bạn 1 bot và 2 bot cùng provider",
       "- 1 bot: gửi được message, next được scenario\n"
       "- 2 bot: gửi ĐÚNG step của từng bot (không lẫn), next ĐÚNG scenario của từng bot\n"
       "- DB: bản ghi tách đúng theo bot_id",
       env="PRODUCTION",
       note="RULE-08. Nguồn: r957-r960,「Job scenario」r200-r201"),

    tc("Job gửi step & is_last_step", "JOB-001", "Abnormal",
       "Test RECOVER: friend đang is_following = 1 nhưng KHÔNG còn bản ghi scenario_step_time → update trạng thái kết thúc, cập nhật counter, KHÔNG next scenario",
       JOB + "\n- Friend「たろう」có `scenario_lineuser`.`is_following` = 1 với S1\n"
       "- Xoá thủ công toàn bộ bản ghi `scenario_step_time` của friend đó\n- S1 CÓ setting next scenario",
       "1. Ghi lại 3 counter của S1 và `is_following` của friend\n2. Xoá bản ghi `scenario_step_time` của friend\n"
       "3. Chờ job recover chạy\n4. Query `scenario_lineuser`.`is_following` + 3 counter\n"
       "5. Query `scenario_lineuser` của scenario next → có bản ghi mới không",
       "Friend is_following = 1, không còn scenario_step_time; S1 có next scenario",
       "- `is_following` được update sang trạng thái kết thúc\n- count_follow và counter trạng thái dừng được cập nhật\n"
       "- KHÔNG start next scenario",
       env="PRODUCTION",
       note="Nguồn: r961"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Test RECOVER: friend còn bản ghi scenario_step_time → step có send_time lớn nhất mà is_last_step = 0 sẽ được update thành 1",
       JOB + "\n- Friend đang chạy S1, còn 2 bản ghi `scenario_step_time`; cả 2 đều có is_last_step = 0",
       "1. Set thủ công is_last_step = 0 cho cả 2 bản ghi\n2. Chờ job recover chạy\n"
       "3. Query `scenario_step_time` của friend đó: is_last_step của từng bản ghi\n4. Đối chiếu với send_time",
       "2 bản ghi pending, cả 2 is_last_step = 0",
       "- Bản ghi có `send_time` LỚN NHẤT được update `is_last_step` = 1\n- Bản ghi còn lại giữ is_last_step = 0",
       env="PRODUCTION",
       note="Nguồn: r962"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Start scenario từ WEB và từ JOB (5 nguồn) → scenario_step_time add đúng timing và đúng is_last_step",
       JOB + "\n- S1 có 3 step đủ 3 loại timing",
       "1. Start S1 từ web: action chat 1:1 → query `scenario_step_time` (send_time + is_last_step)\n"
       "2. Start từ job — multi action của POSTBACK: click button (button chỉ setting multi action) → query\n"
       "3. Start từ job — multi action của CALLBACK: friend kết bạn → query\n"
       "4. Start từ job — multi action của job khác: click button (button setting friend action + open url) → query\n"
       "5. Đối chiếu 4 lần",
       "4 nguồn start (1 web + 3 job); S1 3 step",
       "- Cả 4 nguồn: `scenario_step_time` add đúng timing của từng step và set đúng `is_last_step`",
       env="PRODUCTION",
       note="4 nguồn cùng 1 kết quả → giữ chung. Nguồn: r1018-r1021"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "3 loại delay_type khi start: type 1 send ngay KHÔNG insert scenario_step_time; type 2 và type 0 đều insert",
       JOB + "\n- S1 có: step「ステップ開始直後」+ step 経過時間 (3 mốc: <24h, <48h, =72h) + step 日時で指定",
       "1. Start S1 cho friend\n2. NGAY sau khi start, query `scenario_step_time` WHERE user_id = <friend>\n"
       "3. Đếm số bản ghi và đối chiếu với từng step\n4. Quan sát LINE app: step send ngay có tới ngay không",
       "step send ngay + 経過時間 10h / 30h / 72h + 日時で指定 1日後",
       "- Step delay_type = 1 (send ngay): gửi LUÔN, KHÔNG insert bản ghi vào `scenario_step_time`\n"
       "- Step delay_type = 2 (経過時間) cả 3 mốc <24h, <48h, =72h: ĐỀU insert bản ghi\n"
       "- Step delay_type = 0 (日時で指定): insert bản ghi",
       env="PRODUCTION",
       note="Nguồn: r1022-r1025"),

    tc("Job gửi step & is_last_step", "MSG-001", "Normal",
       "Trigger START scenario hiển thị trên chat 1:1 với 機能名 / 管理名 / 詳細 đúng theo 7 nguồn start",
       JOB + "\n- Chuẩn bị 7 nguồn start scenario",
       "1. Với mỗi nguồn, start scenario S1 cho friend\n2. Mở chat 1:1 → đọc block trigger「このステップの開始トリガー」\n"
       "3. Đối chiếu 機能名 / 管理名 / 詳細",
       "7 nguồn: modal multi action (chat 1:1) · right bar chat 1:1 · my page · auto reply · click button template · "
       "kết bạn CŨ · quét QR",
       "- Modal multi action / right bar / my page: 機能名「手動操作」, 管理名「-」\n"
       "- Auto reply: 機能名「自動応答」, 管理名「-」, 詳細 tuỳ loại autoreply (all msg / msg chỉ định)\n"
       "- Click button: 機能名「テンプレート」, 管理名 = tên button, 詳細「パネルボタンタップ」\n"
       "- Kết bạn cũ: 機能名「友だち追加時設定」, 管理名「-」, 詳細「既存友だち用アクション」\n"
       "- Quét QR: 機能名「QRコードアクション」, 管理名 = tên landing, 詳細「URL読み込み」",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-39 — corpus r1030 ghi chú:『trên step cũng hiển thị tên quản lý là -』với modal multi action → cần xác nhận "
            "管理名 =「-」là đúng ý đồ hay thiếu dữ liệu. Nguồn: r1030, r1035-r1040"),

    tc("Job gửi step & is_last_step", "MSG-001", "Normal",
       "Chi tiết step message trên chat 1:1: hiển thị ステップ名 · 配信対象 · mốc timing đúng với 4 mức 経過時間 (<24h, 24h, <48h, 72h)",
       JOB + "\n- S1 có step 経過時間 ở 4 mốc: 23時間59分後 · 24時間00分後 · 47時間59分後 · 72時間00分後",
       "1. Start S1 cho friend qua modal multi action (chat 1:1)\n2. Mở chat 1:1, xem chi tiết từng step message\n"
       "3. Đối chiếu ステップ名 · 配信対象 · text mốc thời gian của cả 4 step",
       "4 mốc 経過時間: 23時間59分後 · 24時間00分後 · 47時間59分後 · 72時間00分後",
       "- Mỗi step hiển thị:\n  ステップ名: tên step\n  配信対象: 「ステップ購読者全員」(nếu không filter) hoặc tên filter\n"
       "  Mốc timing: đúng text tương ứng (vd「23時間59分後」,「72時間00分後」)",
       env="PRODUCTION",
       note="Nguồn: r1031-r1034, r1056"),

    tc("Job gửi step & is_last_step", "MSG-001", "Normal",
       "Trigger START TỪ GIỮA (途中から) hiển thị trên chat 1:1 với block title 途中からのステップ配信開始 và ngày bắt đầu",
       JOB + "\n- Chuẩn bị 7 nguồn start scenario TỪ GIỮA",
       "1. Với mỗi nguồn, start scenario S1 cho friend theo chế độ start từ ngày thứ N\n"
       "2. Mở chat 1:1 → đọc block trigger\n3. Đối chiếu title, date, tên scenario, số ngày, và detail trigger",
       "7 nguồn: friend list · right bar chat 1:1 · my page · tap richmenu · add tag · kết bạn MỚI · tap image map",
       "- Block hiển thị: Title「（途中からの）ステップ配信開始」· Date yyyy/mm/dd hh:mm · <Tên scenario> · <N>日後から開始\n"
       "- Detail trigger: Title「このステップの開始トリガー」· 機能名 tương ứng nguồn "
       "(手動操作 với friend list/right bar/my page; 友だち追加時設定 + 詳細「新規友だち用アクション」với kết bạn mới) "
       "· 管理名 · 詳細「テスト：<tên user thao tác>」· トリガー稼働日時",
       env="PRODUCTION",
       note="Nguồn: r1041-r1047"),

    tc("Job gửi step & is_last_step", "MSG-001", "Normal",
       "Trigger STOP scenario hiển thị trên chat 1:1 với 機能名 / 管理名 / 詳細 đúng theo 6 nguồn stop",
       JOB + "\n- Friend đang chạy S1; chuẩn bị 6 nguồn stop",
       "1. Với mỗi nguồn, stop scenario S1 cho friend\n2. Mở chat 1:1 → đọc block「ステップ配信停止」và「このステップの停止トリガー」\n"
       "3. Đối chiếu 機能名 / 管理名 / 詳細",
       "6 nguồn: modal multi action (chat 1:1) · right bar · my page · tap richmenu · auto reply · trả lời form",
       "- Block: Title「ステップ配信停止」· Date · <Tên scenario> ·「ステップ配信が停止しました」\n"
       "- Modal multi action / right bar / my page: 機能名「手動操作」, 管理名「-」, 詳細「テスト：<tên user thao tác>」\n"
       "- Tap richmenu: 機能名「リッチメニュー」, 管理名 = tên richmenu, 詳細「タップ」\n"
       "- Auto reply: 機能名「自動応答」, 管理名「-」, 詳細 tuỳ loại autoreply\n"
       "- Trả lời form: 機能名「フォーム作成」, 管理名 = tên form, 詳細 tuỳ loại action",
       env="PRODUCTION",
       note="Nguồn: r1048-r1053"),

    tc("Job gửi step & is_last_step", "MSG-001", "Abnormal",
       "Start scenario mà KHÔNG có step nào thoả mãn giờ gửi → chat 1:1 hiển thị ※ このステップ配信にはメッセージは登録されていません",
       JOB + "\n- S1 chỉ có step 日時で指定 2日後 nhưng chọn start từ ngày thứ 3 (vượt quá step cuối)",
       "1. Start S1 từ WEB cho friend với điều kiện không step nào thoả mãn → mở chat 1:1 đọc block\n"
       "2. Lặp: start từ JOB (action) → mở chat 1:1 đọc block\n"
       "3. Query `scenario_lineuser`.`is_following` + counter",
       "S1 step cuối 2日後; start từ ngày thứ 3",
       "- Start từ WEB: chat 1:1 hiển thị Title「ステップ配信開始」· yyyy/mm/dd hh:mm · <Tên scenario> "
       "·「※ このステップ配信にはメッセージは登録されていません」\n"
       "- Start từ JOB: hiển thị Title「ステップ配信開始」· yyyy/mm/dd hh:mm ·「※ このステップ配信にはメッセージは登録されていません」"
       "(KHÔNG có dòng tên scenario)\n- Scenario dừng luôn, counter cập nhật",
       env="PRODUCTION",
       note="⚠️ Corpus r1054 (web) có dòng <Tên scenario> còn r1055 (job) KHÔNG có → khác biệt hiển thị giữa 2 nguồn, "
            "cần Leader xác nhận là cố ý. Nguồn: r1054, r1055"),

    tc("Job gửi step & is_last_step", "JOB-001", "Normal",
       "Job send test hàng loạt: 3 option × dạng chỉ định / duration (trước & sau 24h) → insert scenario_step_time và gửi đúng thứ tự",
       JOB + "\n- S1 có step 日時で指定 và step 経過時間 ở 2 mốc: trước 24h (10h) và sau 24h (30h)",
       "1. Send test option 1 (theo timing) với step dạng chỉ định → query `scenario_step_time` + LINE app\n"
       "2. Lặp với step duration trước 24h và sau 24h\n"
       "3. Lặp toàn bộ với option 2 (gửi hàng loạt)\n4. Lặp toàn bộ với option 3 (cách nhau 20-30s)",
       "3 option × 3 dạng step (chỉ định / duration <24h / duration >24h) = 9 tổ hợp",
       "- Cả 9 tổ hợp: insert `scenario_step_time` đúng theo option đã chọn\n"
       "- Job send đúng THỨ TỰ cho friend, không đảo, không trùng",
       env="PRODUCTION",
       note="Nguồn: r1059-r1067"),

    # ══════════════════ 26. Job khi edit step đang chạy ══════════════════
    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: TẠO MỚI step delay_type = 1 hoặc 2 khi scenario đang chạy → BỎ QUA, không add bản ghi scenario_step_time; step khác giữ nguyên",
       TWO_BOT + "\n- Bot A có scenario đang chạy cho friend; bot B cũng có scenario đang chạy cho friend đó",
       "1. Ghi lại toàn bộ `scenario_step_time` của friend ở CẢ bot A và bot B\n"
       "2. Ở bot A, tạo mới step「ステップ開始直後」(delay_type = 1) → query lại `scenario_step_time` của cả 2 bot\n"
       "3. Tạo mới step 経過時間 (delay_type = 2) — cả 2 trường hợp thoả mãn và KHÔNG thoả mãn giờ gửi → query lại\n"
       "4. Kiểm tra riêng: step vừa tạo là last message / không phải last message → query lại\n"
       "5. Lặp toàn bộ với scenario CÓ set filter",
       "delay_type 1 và 2 × (thoả / không thoả giờ gửi) × (last / not last) × (có filter / không filter)",
       "- Bot A: BỎ QUA, KHÔNG add thêm bản ghi `scenario_step_time`; các step khác GIỮ NGUYÊN\n"
       "- Bot B: KHÔNG bị update (dữ liệu độc lập theo bot_id)",
       env="PRODUCTION",
       note="Bug #32281 (05-10-2025). Các biến thể cùng 1 kết quả → giữ chung. Nguồn: r877-r881, r886-r890"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: TẠO MỚI step delay_type = 0 (日時で指定) khi đang chạy → thoả giờ gửi thì ADD bản ghi; không thoả thì KHÔNG add",
       TWO_BOT + "\n- Bot A có scenario đang chạy cho friend",
       "1. Ở bot A, tạo mới step 日時で指定 với giờ gửi CÒN thoả mãn (tương lai) → query `scenario_step_time` của cả 2 bot\n"
       "2. Tạo mới step 日時で指定 với giờ gửi ĐÃ QUA → query lại\n3. Lặp với scenario CÓ set filter",
       "delay_type = 0 × (thoả / không thoả giờ gửi) × (có / không filter)",
       "- Thoả mãn giờ gửi: bot A ADD thêm bản ghi `scenario_step_time` cho step mới\n"
       "- Không thoả mãn (đã quá giờ): KHÔNG tạo thêm bản ghi\n- Bot B: KHÔNG bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r882, r883, r891, r892"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: tạo mới step delay_type = 0 — cập nhật is_last_message đúng khi step mới trở thành / không phải last message",
       TWO_BOT + "\n- Bot A có scenario đang chạy; đang có 1 step với `is_last_message` = 1",
       "1. Ghi lại `scenario_step_time`.`is_last_message` của các step\n"
       "2. Tạo step 日時で指定 mới có send_time SỚM HƠN step last hiện tại → query lại is_last_message của tất cả step\n"
       "3. Tạo step 日時で指定 mới có send_time MUỘN HƠN step last hiện tại → query lại\n"
       "4. Lặp với scenario CÓ set filter\n5. Kiểm tra bot B",
       "Step mới sớm hơn / muộn hơn step last hiện tại",
       "- Step mới KHÔNG phải last: bản ghi step mới có `is_last_message` = 0; step cũ vẫn giữ = 1\n"
       "- Step mới LÀ last: bản ghi step mới có `is_last_message` = 1; step cũ được update về 0\n"
       "- Bot B: KHÔNG bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r884, r885, r893, r894"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT delay_type từ 1 → 2 (send ngay sang 経過時間) khi step đã gửi cho user → bỏ qua, không add bản ghi",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step「ステップ開始直後」ĐÃ được gửi cho friend",
       "1. Ghi lại `scenario_step_time` của friend ở cả 2 bot\n2. Ở bot A, edit step từ delay_type 1 → 2 → lưu\n"
       "3. Query lại `scenario_step_time` của cả 2 bot",
       "delay_type 1 → 2; step đã gửi",
       "- Bot A: BỎ QUA, không add thêm bản ghi; các step khác giữ nguyên\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r895"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT delay_type 1 → 0 (send ngay sang 日時で指定) khi step ĐÃ gửi → vẫn tạo thêm scenario_step_time nếu thoả mãn giờ gửi",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step「ステップ開始直後」ĐÃ gửi cho friend",
       "1. Edit step từ delay_type 1 → 0 với giờ gửi CÒN thoả mãn → query `scenario_step_time`\n"
       "2. Lặp với giờ gửi ĐÃ QUA → query\n"
       "3. Kiểm tra riêng 2 trường hợp: sau edit step trở thành last / không phải last → query is_last_message\n"
       "4. Kiểm tra bot B",
       "delay_type 1 → 0; step đã gửi; thoả / không thoả giờ gửi; last / not last",
       "- Thoả mãn giờ gửi: ADD thêm bản ghi cho step vừa edit\n- Không thoả: KHÔNG tạo thêm bản ghi\n"
       "- Trở thành last: bản ghi mới is_last_message = 1, step cũ về 0\n"
       "- Không phải last: is_last_message = 0, step có send_time cuối cùng được update = 1\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r896-r899"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT delay_type 2 → 1 hoặc 0 → 1 (chuyển về send ngay) khi step CHƯA gửi → XOÁ bản ghi scenario_step_time",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step 経過時間 và step 日時で指定 đều CHƯA gửi cho friend",
       "1. Ghi lại `scenario_step_time` của friend\n"
       "2. Edit step 経過時間 → send ngay, trong khi scenario VẪN CÒN step khác chưa gửi → query lại\n"
       "3. Chuẩn bị lại: scenario KHÔNG còn step nào khác chưa gửi → edit → query `scenario_step_time`, "
       "`scenario_lineuser`.`is_following`, 3 counter, và kiểm tra next scenario\n"
       "4. Lặp bước 2-3 với step 日時で指定 → send ngay\n5. Kiểm tra bot B",
       "delay_type 2 → 1 và 0 → 1; còn / không còn step khác chưa gửi",
       "- Còn step khác chưa gửi: XOÁ bản ghi của step đó khỏi `scenario_step_time`; nếu chưa có bản ghi thì không làm gì\n"
       "- Không còn step khác chưa gửi: xoá bản ghi + `scenario_lineuser`.`is_following` = 2 (giống case xoá last message) "
       "+ KHÔNG next scenario + cập nhật count_follow / count_stop\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. 2 hướng edit cùng 1 kết quả → giữ chung. Nguồn: r900, r901, r912, r913"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT delay_type 2 → 1 hoặc 0 → 1 khi step ĐÃ gửi cho user → KHÔNG update lại bản ghi scenario_step_time",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step 経過時間 và step 日時で指定 ĐÃ gửi cho friend",
       "1. Ghi lại `scenario_step_time` của friend\n2. Edit step đã gửi từ delay_type 2 → 1 → query lại\n"
       "3. Edit step đã gửi từ delay_type 0 → 1 → query lại\n4. Kiểm tra bot B",
       "delay_type 2 → 1 và 0 → 1; step đã gửi",
       "- Cả 2 hướng: KHÔNG update lại bản ghi `scenario_step_time`\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r902, r914"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT giữa delay_type 2 ⇄ 0 khi step CHƯA gửi → update send_time; nếu quá giờ thì xoá bản ghi; is_last_message tính lại",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step CHƯA gửi cho friend",
       "1. Edit step từ 経過時間 → 日時で指定, giờ gửi CÒN thoả mãn → query `scenario_step_time`.`send_time`\n"
       "2. Edit sang giờ ĐÃ QUA, scenario còn step khác chưa gửi → query\n"
       "3. Edit sang giờ ĐÃ QUA, scenario KHÔNG còn step khác → query is_following + counter + next scenario\n"
       "4. Edit khiến step trở thành / không còn là last message → query is_last_message\n"
       "5. Lặp toàn bộ theo chiều ngược lại 日時で指定 → 経過時間\n6. Kiểm tra bot B",
       "2 chiều edit × (thoả / không thoả giờ) × (còn / không còn step khác) × (last / not last)",
       "- Thoả giờ gửi: UPDATE lại `send_time`; nếu chưa có bản ghi thì ADD mới\n"
       "- Quá giờ + còn step khác: XOÁ bản ghi của step\n"
       "- Quá giờ + không còn step khác: xoá bản ghi + is_following = 2 + KHÔNG next scenario + cập nhật counter\n"
       "- is_last_message: step trở thành last → = 1 (step cũ về 0); step hết là last → = 0 và step có send_time cuối = 1\n"
       "- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. 2 chiều đối xứng cùng quy tắc → giữ chung. Nguồn: r903-r907, r915-r919"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: EDIT chỉ THỜI GIAN (giữ nguyên delay_type 2 hoặc 0) khi step CHƯA gửi → update send_time, xử lý quá giờ và is_last_message như trên",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step 経過時間 và step 日時で指定 CHƯA gửi",
       "1. Edit thời gian của step 経過時間 (giữ delay_type = 2) sang mốc CÒN thoả mãn → query send_time\n"
       "2. Edit sang mốc ĐÃ QUA, còn step khác chưa gửi → query\n3. Edit sang mốc ĐÃ QUA, không còn step khác → query đầy đủ\n"
       "4. Edit khiến step trở thành / hết là last message → query is_last_message\n"
       "5. Lặp toàn bộ với step 日時で指定 (giữ delay_type = 0), bao gồm cả case chỉ edit GIỜ (giữ nguyên số ngày)\n"
       "6. Kiểm tra bot B",
       "delay_type 2 và 0, chỉ edit thời gian",
       "- Thoả giờ: UPDATE `send_time`; chưa có bản ghi thì ADD mới\n"
       "- Quá giờ + còn step khác: XOÁ bản ghi\n- Quá giờ + không còn step khác: xoá + is_following = 2 + không next + counter\n"
       "- is_last_message tính lại đúng\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r924-r928, r933-r937,「Job scenario」r158-r162, r170-r176"),

    tc("Job khi edit step đang chạy", "JOB-001", "Abnormal",
       "Bug #32281: EDIT step ĐÃ GỬI cho user (giữ hoặc đổi delay_type sang 0/2) → KHÔNG thêm bản ghi scenario_step_time",
       TWO_BOT + "\n- Bot A có scenario đang chạy; step ĐÃ gửi cho friend",
       "1. Edit thời gian step đã gửi (delay_type 2 hoặc 0) sang mốc CÒN thoả mãn → query `scenario_step_time`\n"
       "2. Edit sang mốc ĐÃ QUA → query\n3. Edit khiến step trở thành / hết là last message → query\n"
       "4. Lặp với edit delay_type 0 → 2 và 2 → 0 cho step đã gửi\n5. Kiểm tra bot B",
       "Step ĐÃ gửi; các kiểu edit thời gian và delay_type",
       "- KHÔNG thêm bản ghi `scenario_step_time` cho step đã gửi (kể cả khi thoả mãn giờ gửi)\n"
       "- Bot B: không bị update",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-40 — MÂU THUẪN NỘI BỘ: corpus ghi cả 2 kết quả cho cùng case『step đã gửi + thoả mãn giờ』— "
            "r908/r938 (Testcase) ghi『Thêm bản ghi cho step vừa edit』; r920/r929 lại ghi『Thêm bản ghi → **Không thêm bản ghi**』; "
            "「Job scenario」r142/r177 cũng ghi『Thêm bản ghi』. Cần chốt hành vi đúng. Nguồn: r908-r911, r920-r923, r929-r932, r938-r941"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: COPY step từ filter khác vào filter hiện tại khi scenario đang chạy → xử lý giống case TẠO MỚI theo từng delay_type",
       TWO_BOT + "\n- Bot A có scenario đang chạy, có ≥ 2 filter branch",
       "1. Copy step delay_type = 1 từ filter khác → query `scenario_step_time` của cả 2 bot\n"
       "2. Copy step delay_type = 2 (thoả và không thoả giờ gửi; last và not last) → query\n"
       "3. Copy step delay_type = 0 (thoả và không thoả giờ gửi; last và not last) → query\n4. Kiểm tra bot B",
       "3 delay_type × (thoả / không thoả) × (last / not last)",
       "- delay_type 1 và 2: BỎ QUA, không add bản ghi; step khác giữ nguyên\n"
       "- delay_type 0 thoả giờ: ADD bản ghi cho step mới; không thoả: KHÔNG add\n"
       "- delay_type 0: is_last_message tính lại đúng (mới là last → = 1, step cũ về 0)\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r942-r950,「Job scenario」r187-r195"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: XOÁ step có is_last_message = 1 → xoá bản ghi; step khác có send_time lớn nhất được update thành last",
       TWO_BOT + "\n- Bot A có scenario đang chạy; friend còn ≥ 2 bản ghi `scenario_step_time` pending",
       "1. Ghi lại `scenario_step_time` (send_time, is_last_message) của friend\n"
       "2. Xoá step đang có is_last_message = 1, scenario VẪN còn step khác chưa tới giờ send → query lại\n"
       "3. Chuẩn bị lại: scenario KHÔNG còn step nào khác đến giờ gửi → xoá step last → query `scenario_step_time`, "
       "`scenario_lineuser`.`is_following`, 3 counter, kiểm tra next scenario\n4. Kiểm tra bot B",
       "Xoá step is_last_message = 1; còn / không còn step khác",
       "- Còn step khác: xoá bản ghi của step bị xoá; step khác có `send_time` LỚN NHẤT được update `is_last_message` = 1\n"
       "- Không còn step khác: xoá bản ghi + `scenario_lineuser`.`is_following` = 2 nhưng KHÔNG thực hiện next scenario "
       "+ cập nhật count_follow / count_stop\n- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r951, r952,「Job scenario」r196, r197"),

    tc("Job khi edit step đang chạy", "JOB-001", "Normal",
       "Bug #32281: XOÁ FILTER chứa step đang là last message, hoặc xoá NHIỀU step cùng lúc (có step last) → xử lý giống xoá step last",
       TWO_BOT + "\n- Bot A có scenario đang chạy, filter F-A chứa step đang là is_last_message = 1",
       "1. Xoá filter F-A khi scenario VẪN còn step khác chưa gửi → query `scenario_step_time`\n"
       "2. Xoá filter F-A khi KHÔNG còn step nào khác đến giờ gửi → query đầy đủ\n"
       "3. Chuẩn bị lại, chọn nhiều step (có cả step last) → xoá cùng lúc, cả 2 trường hợp còn/không còn step khác\n"
       "4. Kiểm tra bot B",
       "Xoá filter chứa last step; xoá nhiều step cùng lúc",
       "- Còn step khác: xoá bản ghi các step bị xoá; step có send_time lớn nhất được update is_last_message = 1\n"
       "- Không còn step khác: xoá bản ghi + is_following = 2 + KHÔNG next scenario + cập nhật counter\n"
       "- Bot B: không bị update",
       env="PRODUCTION",
       note="Bug #32281. Nguồn: r953-r956,「Job scenario」r198, r199"),

    # ══════════════════ 27. Chống lặp vô hạn ══════════════════
    tc("Chống lặp vô hạn", "JOB-001", "Normal",
       "Scenario A next B, B next lại A: số lần start A trong 1 giờ DƯỚI 10 → vẫn start được A ở mọi nguồn",
       JOB + "\n- Scenario A next sang B; B next lại A\n- Friend test đã chạy vòng lặp < 10 lần trong 1 giờ",
       "1. Cho vòng lặp A → B → A chạy 5 lần trong 1 giờ\n2. Start lại A cho friend từ ACTION (autoreply / tag) → quan sát\n"
       "3. Chờ B chạy xong → next sang A → quan sát\n4. Start scenario C khác, sau khi C xong cũng start A → quan sát\n"
       "5. Chuỗi A → B → C → A → quan sát\n6. Query `scenario_lineuser` của A",
       "Vòng lặp chạy 5 lần (< 10) trong 1 giờ",
       "- Cả 4 nguồn (action, next từ B, next từ C, chuỗi A→B→C→A) đều START ĐƯỢC scenario A\n"
       "- `scenario_lineuser` của A cập nhật is_following = 1",
       env="PRODUCTION",
       note="RULE-08: job nền + đếm theo giờ → PRODUCTION. Nguồn:「Job scenario」r33-r36"),

    tc("Chống lặp vô hạn", "JOB-001", "Boundary",
       "Đạt ĐÚNG 10 lần start scenario A trong 1 giờ → notify Chatwork và CHẶN start A qua tính năng next scenario",
       JOB + "\n- Scenario A next B; B next lại A\n- Friend test đã start A đúng 10 lần trong 1 giờ",
       "1. Cho vòng lặp chạy đến khi số lần start A đạt 10 trong 1 giờ\n"
       "2. Chờ B chạy xong → next sang A → quan sát\n3. Kiểm tra room Chatwork có notify không\n"
       "4. Start C khác, C xong cũng next A → quan sát\n5. Chuỗi A → B → C → A → quan sát\n"
       "6. Query `scenario_lineuser` của A: is_following có đổi không",
       "Số lần start A = 10 trong 1 giờ",
       "- Cả 3 đường next: KHÔNG start scenario A\n- Có notify Chatwork NGAY khi đạt 10 lần (không chờ 1 tiếng)\n"
       "- `scenario_lineuser` của A không được update is_following",
       env="PRODUCTION",
       note="Spec §10 Error Handling ghi『MonitorScenarioManager: > 10 lần/giờ cho cùng scenarioId+userId → Chatwork alert』"
            "nhưng KHÔNG ghi là CHẶN start — corpus ghi rõ có chặn (MT-03). Nguồn:「Job scenario」r37-r39"),

    tc("Chống lặp vô hạn", "JOB-001", "Abnormal",
       "Đã bị chặn 10 lần: start A từ JOB (autoreply, tag...) → KHÔNG start được; start A từ WEB (chat 1:1) → VẪN start được",
       JOB + "\n- Friend test đã đạt 10 lần start scenario A trong 1 giờ\n- A có step「ステップ開始直後」và step 経過時間",
       "1. Trigger start A từ JOB (autoreply / gắn tag) → quan sát\n"
       "2. Query `scenario_lineuser`.`is_following` + `scenario_step_time`\n"
       "3. Mở chat 1:1 của friend → có message start hiển thị không\n4. Kiểm tra LINE app: có nhận step send ngay không\n"
       "5. Start A từ WEB (màn chat 1:1) → quan sát toàn bộ như trên",
       "Friend đã đạt limit 10 lần; start từ job và từ web",
       "- Start từ JOB: KHÔNG start lại được A — `scenario_lineuser` KHÔNG update is_following, "
       "`scenario_step_time` KHÔNG add bản ghi\n"
       "- Nhưng VẪN có message start hiển thị ở màn chat 1:1; nếu A có step send ngay thì step đó VẪN được gửi "
       "(các step type khác không gửi)\n- Start từ WEB (chat 1:1): VẪN start được A bình thường",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-03 — hành vi nửa vời (chặn schedule nhưng vẫn gửi step send ngay và vẫn hiện trigger) không được spec ghi. "
            "Corpus r40 còn ghi chú ENV:『trên step job scen và callback đang ở 2 server khác nhau, nên đang count số lần "
            "start khác nhau → bị limit khi next scen rồi nhưng start từ callback vẫn được』. Nguồn:「Job scenario」r40, r41"),

    tc("Chống lặp vô hạn", "JOB-001", "Normal",
       "Giới hạn 10 lần tính THEO TỪNG USER: user khác chưa đạt limit vẫn start được A; start cho > 10 user cùng lúc vẫn OK",
       JOB + "\n- Friend X đã đạt 10 lần start A; friend Y chưa từng chạy A; chuẩn bị 12 friend khác",
       "1. Start A cho friend Y (chưa đạt limit) → quan sát\n"
       "2. Start A cùng lúc cho 12 friend chưa đạt limit → query `scenario_lineuser` của 12 friend\n"
       "3. Đếm số friend start thành công",
       "Friend X đạt limit; friend Y và 12 friend khác chưa",
       "- Friend Y và cả 12 friend đều START ĐƯỢC scenario A\n- Giới hạn chỉ áp cho user đã đạt 10 lần",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r42, r43"),

    tc("Chống lặp vô hạn", "JOB-001", "Normal",
       "Bộ đếm reset theo giờ: sau 1 giờ, start B cho user rồi B next sang A → start A thành công trở lại",
       JOB + "\n- Friend X đã đạt 10 lần start A và đang bị chặn",
       "1. Chờ qua 1 giờ kể từ lần start đầu tiên trong chuỗi\n2. Start scenario B cho friend X\n"
       "3. Chờ B chạy xong → next sang A\n4. Query `scenario_lineuser` của A + kiểm tra LINE app",
       "Chờ > 1 giờ rồi thử lại",
       "- Start được scenario A trở lại (bộ đếm đã reset theo cửa sổ 1 giờ)",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r44"),

    tc("Chống lặp vô hạn", "JOB-001", "Abnormal",
       "Scenario A đã bị chặn, A next sang D (D chưa đạt limit): start A qua JOB → không start được A nên cũng KHÔNG next sang D; start A qua WEB → start được cả A và D",
       JOB + "\n- Scenario A đã start 10 lần trong 1 giờ cho friend X; A next sang D; D chưa đạt limit",
       "1. Trigger start A cho friend X qua ACTION JOB (autoreply / tag) → chờ → kiểm tra D có được start không\n"
       "2. Query `scenario_lineuser` của A và D\n3. Start A cho friend X từ WEB (chat 1:1) → chờ A chạy xong → kiểm tra D",
       "A bị chặn; A next D; start qua job và qua web",
       "- Qua JOB: KHÔNG start được A → cũng KHÔNG next được sang D\n"
       "- Qua WEB: start được A, và sau khi A chạy xong start được cả D",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r45, r46"),

    tc("Chống lặp vô hạn", "JOB-001", "Normal",
       "Scenario A và B KHÔNG setting next scenario → start bình thường, không bị cơ chế chống lặp ảnh hưởng (1 user và > 10 user)",
       JOB + "\n- Scenario A và B đều KHÔNG có setting next scenario",
       "1. Start A cho 1 friend → quan sát\n2. Start A cùng lúc cho 12 friend → query `scenario_lineuser`\n"
       "3. Kiểm tra không có notify Chatwork bất thường",
       "A, B không có next scenario; 1 user và 12 user",
       "- Cả 2 trường hợp: start được bình thường, không bị chặn, không notify",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r47, r48"),

    # ══════════════════ 28. Trùng line_user ══════════════════
    tc("Trùng line_user", "CONC-001", "Abnormal",
       "Bug KH #37711: kết bạn mới qua QR (thường / landing) → chỉ tạo 1 line_user, GUI hiển thị 1 tài khoản",
       "- Bot A ở LINE login đã setting Linked LINE Official Account trỏ tới bot cùng provider\n"
       "- Tài khoản LINE chưa kết bạn với bot A",
       "1. Kết bạn với bot A qua QR THƯỜNG → mở màn 友だち管理 đếm số tài khoản của user đó\n"
       "2. Query `line_user` WHERE line_id = <line_id user>\n3. Lặp với QR LANDING\n"
       "4. Lặp với trường hợp friend CŨ chưa tồn tại trên tool kết bạn lại",
       "3 đường kết bạn: QR thường (user mới) · QR landing · friend cũ chưa có trên tool",
       "- Cả 3 đường: kết bạn thành công, tạo ĐÚNG 1 bản ghi `line_user`\n"
       "- KHÔNG có duplicate line_user\n- Màn 友だち管理 hiển thị ĐÚNG 1 tài khoản cho user đó",
       env="PRODUCTION",
       note="Bug KH #37711 (16-06-2026). 3 đường cùng 1 kết quả → giữ chung. Nguồn:「text fix bug Kh」r80, r81, r86"),

    tc("Trùng line_user", "CONC-001", "Abnormal",
       "Bug KH #37711 (repro): user chưa kết bạn mở LINK FORM → web checkFriend chạy song song với callback follow của job → chỉ được 1 line_user",
       "- Bot A có scenario gắn action kết bạn\n- Tài khoản LINE chưa kết bạn với bot A\n- Có link form answer của bot A",
       "1. Từ tài khoản LINE chưa kết bạn, mở link form answer của bot (web checkFriend tạo line_user)\n"
       "2. Đồng thời hoàn tất kết bạn (job doHandleFollowEvent) → 2 luồng chạy gần như cùng lúc\n"
       "3. Mở màn 友だち管理 đếm số tài khoản hiển thị cho user\n4. Mở chat 1:1 → đếm số hội thoại\n"
       "5. Query `line_user` WHERE line_id = <line_id>\n6. Kiểm tra scenario kết bạn chạy trên mấy bản ghi",
       "1 tài khoản LINE, mở link form + kết bạn gần như đồng thời",
       "- Màn 友だち管理 chỉ hiển thị 1 tài khoản (không 2 dòng trùng tên/ảnh)\n- Chat 1:1 chỉ 1 hội thoại\n"
       "- `line_user`: chỉ 1 bản ghi cho line_id đó\n- Scenario kết bạn chỉ chạy trên 1 bản ghi, KHÔNG có 2 luồng step song song",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D01 do AI viết trong corpus, kết quả OK. Nguồn:「text fix bug Kh」r79, r96, r123, r130"),

    tc("Trùng line_user", "CONC-001", "Abnormal",
       "Bug KH #37711: double click 'Thêm bạn' / mở lại link form nhiều lần liên tiếp → KHÔNG tạo line_user trùng, scenario chỉ chạy 1 lần",
       "- Tài khoản LINE chưa kết bạn với bot A\n- Bot A có scenario gắn action kết bạn",
       "1. Mở link form, bấm「Thêm bạn」2 lần thật nhanh\n2. Mở lại link form 3–4 lần liên tiếp trong thời gian ngắn\n"
       "3. Query `line_user` WHERE line_id = <line_id>\n4. Mở màn 友だち管理 → đếm tài khoản\n"
       "5. Kiểm tra LINE app: có nhận message add-friend / step lặp không",
       "Double click 'Thêm bạn'; mở link form 3-4 lần liên tiếp",
       "- Chỉ 1 bản ghi `line_user`; tài khoản KHÔNG nhân đôi trên GUI\n"
       "- Scenario và tin add-friend chỉ chạy & gửi ĐÚNG 1 LẦN (không gửi lặp)",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D03 do AI viết trong corpus, kết quả OK. Nguồn:「text fix bug Kh」r132"),

    tc("Trùng line_user", "SEC-ISO-001", "Abnormal",
       "Bug KH #37711: 2 user KHÁC line_id kết bạn đồng thời → dedup KHÔNG xoá nhầm tài khoản của user kia",
       "- 2 tài khoản LINE A và B đều chưa là bạn của bot",
       "1. Cho A và B cùng mở link form và bấm「Thêm bạn」gần như đồng thời\n"
       "2. Vào màn 友だち管理 kiểm tra cả 2 tài khoản\n3. Query `line_user` của cả 2 line_id\n"
       "4. Cho scenario chạy cho cả 2 → kiểm tra tiến trình từng user\n5. Xoá tài khoản A → kiểm tra dữ liệu và hội thoại của B",
       "2 tài khoản LINE A và B kết bạn đồng thời",
       "- Có ĐÚNG 2 tài khoản (A và B), mỗi user 1 bản ghi\n- KHÔNG tài khoản nào bị xoá nhầm\n"
       "- Scenario chạy độc lập đúng từng user\n- Xoá A KHÔNG ảnh hưởng dữ liệu / hội thoại của B",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D04 do AI viết trong corpus, kết quả OK. Nguồn:「text fix bug Kh」r95, r133"),

    tc("Trùng line_user", "FRIEND-001", "Abnormal",
       "Bug KH #37711: friend đang BLOCK bot → mở link / re-follow không sinh line_user trùng; trong lúc block KHÔNG gửi scenario; sau unblock scenario tiếp đúng tiến trình",
       "- User đã từng kết bạn rồi block bot\n- User đang trong scenario nhiều step, còn step chưa gửi",
       "1. User block bot\n2. Chờ qua mốc gửi 1 step → kiểm tra LINE app và `step_message_history`\n"
       "3. User mở link form (web checkFriend) rồi unblock / re-follow\n4. Query `line_user` WHERE line_id = <line_id>\n"
       "5. Kiểm tra màn 友だち管理 và tiến trình scenario của user",
       "User block → mở link form → unblock",
       "- Vẫn chỉ 1 tài khoản cho user, KHÔNG tạo bản trùng\n"
       "- Trong lúc block: KHÔNG gửi message / scenario\n"
       "- Sau unblock: dùng đúng tài khoản CŨ, scenario tiếp đúng tiến trình (không chạy lại từ đầu trên bản trùng)",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D05 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r134"),

    tc("Trùng line_user", "DATA-MIG-001", "Abnormal",
       "Bug KH #37711: friend đã XOÁ MỀM trên tool → re-add qua link không sinh line_user trùng, scenario không chạy song song 2 bản",
       "- User X có `line_user` đã bị xoá (soft-delete) trên tool",
       "1. Xoá friend X trên tool\n2. User X mở link form / booking → kết bạn lại\n"
       "3. Vào màn 友だち管理 + search tên X → đếm số dòng\n4. Query `line_user` WHERE line_id = <X>\n"
       "5. Kiểm tra tiến trình scenario của X",
       "Friend đã soft-delete rồi re-add",
       "- Tạo / khôi phục ĐÚNG 1 tài khoản cho X\n- KHÔNG đồng thời tồn tại bản-đã-xoá + bản-mới gây trùng hiển thị\n"
       "- Scenario KHÔNG chạy song song trên 2 bản ghi",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D06 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r124-r129, r135"),

    tc("Trùng line_user", "OUT-001", "Normal",
       "Bug KH #37711: sau khi hết trùng line_user → mỗi step scenario gửi ĐÚNG 1 LẦN, lịch sử gửi chỉ 1 dòng/step",
       "- User đã được dedup về 1 line_user\n- Có scenario nhiều step gắn cho user",
       "1. Cho scenario chạy qua nhiều step (send quick test + tới giờ gửi step)\n"
       "2. Mở LINE app: đếm số message nhận cho từng step\n"
       "3. Mở lịch sử gửi (my_page) → đếm số dòng mỗi step\n4. Query `step_message_history` WHERE line_user_id = <user>",
       "Scenario nhiều step; user đã dedup",
       "- Mỗi step gửi ĐÚNG 1 lần\n- Lịch sử gửi chỉ 1 dòng / step cho user\n"
       "- KHÔNG có 2 luồng step song song\n- User nhận đúng số message, không trùng",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D10 do AI viết (hoàn thiện expected cho case human để trống ở r92), kết quả OK. "
            "RULE-06 + RULE-07. Nguồn:「text fix bug Kh」r83-r85, r92, r115-r117, r139"),

    tc("Trùng line_user", "FRIEND-001", "Abnormal",
       "Bug KH #37711: friend BLOCK giữa lúc scenario đang chạy → KHÔNG gửi step tiếp theo, lịch sử không ghi gửi thành công",
       "- User đang trong scenario nhiều step, còn step chưa gửi",
       "1. Khi scenario đang chạy dở, user block bot\n2. Chờ tới giờ step kế tiếp\n"
       "3. Kiểm tra LINE app: có nhận message không\n4. Query `step_message_history` của step đó\n"
       "5. Kiểm tra action và remind gắn với step đó",
       "User block giữa chừng scenario",
       "- Step sau thời điểm block KHÔNG được gửi\n- KHÔNG thực thi action và KHÔNG gửi remind\n"
       "- Lịch sử KHÔNG ghi gửi thành công cho step đó",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D11 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r140"),

    tc("Trùng line_user", "CONC-001", "Abnormal",
       "Bug KH #37711: thêm member mới vào GROUP đúng lúc member gửi tin → group_line_user không nhân đôi",
       "- Bot đã ở trong 1 group; có member chưa từng tương tác",
       "1. Thêm member mới vào group\n2. Member đó gửi tin trong group gần như cùng lúc\n"
       "3. Mở màn 友だち管理 → đếm số tài khoản của member\n"
       "4. Query `line_user` và `line_user_group` của member đó\n5. Kiểm tra tin nhắn group hiển thị",
       "Member mới vào group + gửi tin đồng thời",
       "- Member chỉ tạo 1 `line_user` và 1 `line_user_group`\n- Không nhân đôi member trong group\n"
       "- Tin nhắn group hiển thị đúng 1 nguồn",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D07 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r82, r87, r136"),

    tc("Trùng line_user", "LIFF-ENTRY-001", "Abnormal",
       "Bug KH #37711: mở link form / booking / conversion / QR từ PC hoặc trình duyệt ngoài → chỉ 1 line_user, action chạy đúng 1 lần",
       "- User chưa kết bạn; có link form/booking, link conversion và QR code của bot\n- Có thiết bị PC hoặc trình duyệt ngoài LINE",
       "1. Mở link form/booking trên PC (hoặc Safari/Chrome ngoài LINE) → web checkFriend (open_external_browser) → kết bạn\n"
       "2. Query `line_user` + kiểm tra redirect màn kết bạn\n"
       "3. Lặp: mở link Conversion khi chưa là bạn → redirect kết bạn → hoàn tất\n4. Lặp với QR code\n"
       "5. Kiểm tra action conversion / QR chạy mấy lần",
       "3 entry point: form/booking từ PC · link conversion · QR code",
       "- Cả 3 entry: sau kết bạn chỉ 1 `line_user`, không sinh tài khoản trùng\n"
       "- Redirect màn kết bạn đúng\n- Action conversion / QR chạy ĐÚNG 1 lần",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D08, TC-D09 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r137, r138"),

    tc("Trùng line_user", "DATA-ID-001", "Abnormal",
       "Bug KH #37711: dedup giữ line_user id NHỎ NHẤT, gộp hội thoại/lịch sử chat về 1 tài khoản, không để lại account rỗng mồ côi",
       "- Đã tái hiện được trùng line_user cho user X (hoặc dùng user đã trùng sẵn)",
       "1. Gây trùng `line_user` cho user X\n2. Mở 友だち管理 → chat 1:1 với X\n"
       "3. Kiểm tra số tài khoản còn lại + id bản ghi được giữ\n4. Kiểm tra hội thoại và tin add-friend\n"
       "5. Search tên X trong list friend → tìm account rỗng",
       "User X có 2 bản ghi line_user trùng line_id",
       "- Còn ĐÚNG 1 tài khoản; bản tạo TRƯỚC (id nhỏ nhất) được giữ lại\n"
       "- Hội thoại / tin nhắn KHÔNG bị tách 2 luồng, không mất tin add-friend\n"
       "- KHÔNG xuất hiện account 'rỗng' mồ côi trong list / search",
       env="PRODUCTION",
       note="Bug KH #37711 — TC-D02 do AI viết, kết quả OK. Nguồn:「text fix bug Kh」r131"),

    # ══════════════════ 29. Backup & đổi bot ══════════════════
    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup scenario: giữ đúng folder, sinh scenario id MỚI, copy scenario next thành id mới",
       "- Bot A có scenario S1 ở folder F1, có setting next = S2\n- Chức năng backup scenario đã sẵn sàng",
       "1. Thực hiện backup scenario S1\n2. Quan sát bản backup nằm ở folder nào\n"
       "3. Query `scenario` của bản backup: id, group_id, after_scenario_id_1\n4. Đối chiếu với S1 gốc",
       "S1 ở folder F1, next = S2",
       "- Bản backup hiển thị ở ĐÚNG folder của scenario gốc (F1)\n- Sinh `scenario`.`id` MỚI\n"
       "- `after_scenario_id_1` là id MỚI (không dùng chung id với bản gốc)",
       note="Nguồn: r76-r78, r80"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup scenario: 3 cột đếm friend và send_count đều RESET về 0; profile KHÔNG được backup",
       "- Bot A có S1 với 5 friend 購読中, 3 friend 読了済, step 1 send_count = 20, có set profile 送信者A",
       "1. Backup S1\n2. Quan sát 3 cột đếm của bản backup ở màn list\n3. Vào màn step: xem 配信済 từng step\n"
       "4. Xem profile 送信者名 của từng step bản backup\n"
       "5. Query `scenario`.`count_*` và `step_message`.`send_count`, `profile_id` của bản backup",
       "S1: 5 購読中, 3 読了済, send_count = 20, profile 送信者A",
       "- 3 cột đếm bản backup đều 0人; `count_follow` = `count_stop` = `count_unfinish` = 0\n"
       "- `step_message`.`send_count` = 0 ở mọi step\n- Profile KHÔNG được backup (`profile_id` = NULL, hiển thị profile default)",
       note="Nguồn: r79, r86, r88"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Backup scenario: filter branch, 3 loại step timing, message và action đều được clone với id MỚI; template dùng thẳng giữ id gốc",
       "- Bot A có S1 với: 2 filter branch, 3 step đủ 3 loại timing, mỗi step có message (tự tạo / clone / dùng thẳng) và action",
       "1. Ghi lại id của `filter_manager`, `step_message`, `template_ids`, `action_id` của S1\n2. Backup S1\n"
       "3. Query từng bảng tương ứng cho bản backup\n4. Đối chiếu từng id với bản gốc\n"
       "5. Mở màn step bản backup, đối chiếu nội dung hiển thị",
       "2 filter, 3 step (3 loại timing), message 3 nguồn, action",
       "- `filter_manager` + `filters_v2`: sinh id MỚI, nội dung giống bản gốc\n"
       "- `step_message`: 3 step sinh id MỚI, delay_type/start_day/start_time giữ nguyên\n"
       "- Template tự tạo/clone: id MỚI; template dùng thẳng: giữ id gốc\n"
       "- `action_id`: id MỚI\n- Nội dung hiển thị giống hệt bản gốc",
       note="Nguồn: r81-r85, r87"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Normal",
       "Bản backup START được cho friend và gửi message đúng",
       "- Đã backup S1 thành S1-backup",
       "1. Start S1-backup cho friend test\n2. Quan sát LINE app friend theo từng mốc timing\n"
       "3. Query `scenario_lineuser` + `scenario_step_time` của S1-backup\n4. Kiểm tra 3 cột đếm của S1-backup",
       "S1-backup với 3 step",
       "- Start thành công, `scenario_lineuser` có bản ghi mới\n- Friend nhận đủ message đúng timing\n"
       "- 3 cột đếm của S1-backup cập nhật đúng",
       env="PRODUCTION",
       note="RULE-06. Nguồn: r89"),

    tc("Backup & đổi bot", "DATA-BACKUP-001", "Abnormal",
       "Trong lúc bot đang BACKUP / TRANSFER → chặn toàn bộ thao tác ghi ở màn scenario",
       "- Bot A đang có bản ghi `BackupHistory` với status 0 hoặc 1 (đang backup/transfer)",
       "1. Mở màn /basic/scenario của bot A\n2. Lần lượt thử: tạo scenario · sửa tên scenario · xoá scenario · "
       "tạo folder · tạo step · thêm message · xoá step\n3. Quan sát message lỗi ở từng thao tác",
       "Bot đang backup (BackupHistory status = 0 hoặc 1)",
       "- TẤT CẢ thao tác ghi bị CHẶN, hiển thị message theo constant `MESSAGE_NOTIFY_BACKUP`\n"
       "- Dữ liệu scenario không bị thay đổi",
       spec="Spec không ghi",
       note="Spec BR-09 (feature-spec §7 mục 9 + logic-spec) mô tả rõ backup lock nhưng CORPUS KHÔNG CÓ TC nào cho case này "
            "→ TC do AI viết từ spec, **lấp GAP của corpus**. CẦN LEADER XÁC NHẬN. Nguồn: spec BR-09"),

    tc("Backup & đổi bot", "SEC-ISO-001", "Abnormal",
       "Mở 2 tab với 2 bot khác nhau, thao tác ghi ở tab bot cũ → chặn với message 別のアカウントに切り替えたので、要求を処理できません。",
       "- Đăng nhập admin có quyền ≥ 2 bot (bot A và bot B)",
       "1. Tab 1: mở màn scenario của bot A\n2. Tab 2: switch sang bot B\n"
       "3. Quay lại tab 1 (vẫn đang ở bot A), thực hiện: tạo scenario / sửa scenario / tạo step / thêm message\n"
       "4. Quan sát message lỗi + query DB xem có bản ghi nào được ghi không",
       "2 tab, 2 bot khác nhau",
       "- Thao tác ghi ở tab bot cũ bị CHẶN\n"
       "- Hiển thị message:「別のアカウントに切り替えたので、要求を処理できません。」\n- DB: KHÔNG có bản ghi mới",
       spec="Spec không ghi",
       note="Spec BR-10 (bot cross-check botIdCurrent) mô tả rõ nhưng CORPUS KHÔNG CÓ TC → TC do AI viết từ spec, "
            "**lấp GAP của corpus**. CẦN LEADER XÁC NHẬN. Nguồn: spec BR-10 / logic-spec Bot Cross-check"),

    tc("Backup & đổi bot", "SEC-ISO-001", "Abnormal",
       "Truy cập scenario KHÔNG thuộc bot hiện tại (sửa scenario_id trên URL) → redirect về /basic/scenario",
       "- Đăng nhập admin ở bot A\n- Biết id của scenario thuộc bot B",
       "1. Mở URL /step-message/list-message/{id scenario của bot B}\n2. Quan sát trang được điều hướng tới\n"
       "3. Lặp với /basic/scenario/copy/{id} và /step-message/create/{id}/{step_id}",
       "scenario_id thuộc bot khác",
       "- Cả 3 URL: bị redirect về /basic/scenario, KHÔNG xem/thao tác được scenario của bot khác",
       spec="Spec không ghi",
       note="Spec `OwnerGetScenario` Form Request (logic-spec Authorization) mô tả rõ nhưng CORPUS KHÔNG CÓ TC → "
            "TC do AI viết từ spec, **lấp GAP của corpus**. CẦN LEADER XÁC NHẬN. Nguồn: spec OwnerGetScenario"),

    tc("Backup & đổi bot", "DATA-MIG-001", "Normal",
       "Scenario write DB riêng: gán scenario ở chat 1:1 / friend list / callback button với đủ biến thể setting → send đúng, không duplicate, đúng staff gửi",
       "- Bot cũ (đã có data trước khi tách DB) và bot mới (tạo sau khi release)",
       "1. Gán scenario ở chat 1:1 với các biến thể: send ngay · send theo thời gian thực · send theo cộng thời gian · "
       "có setting người gửi · có setting filter · có setting richmenu (gán và gỡ) → kiểm tra LINE app\n"
       "2. Gán scenario từ friend list → kiểm tra\n3. Gán từ callback button → kiểm tra\n"
       "4. Lặp toàn bộ trên BOT MỚI và BOT CŨ sau khi release",
       "7 biến thể setting × 3 nguồn gán × bot mới / bot cũ",
       "- Tất cả trường hợp: send ĐÚNG TIME · đúng filter · KHÔNG bị duplicate · đúng staff gửi\n"
       "- Bot cũ và bot mới cho kết quả giống nhau",
       env="PRODUCTION",
       note="Tab「Scenario write DB riêng」(TCsLine_Improve chung). Nguồn: r3-r11, r17-r18"),

    tc("Backup & đổi bot", "DATA-MIG-001", "Normal",
       "Scenario write DB riêng: filter theo tag / ngày kết bạn / status / name / no filter đều đúng trên cả bot cũ và bot mới",
       "- Bot cũ và bot mới, mỗi bot có scenario với 5 loại filter",
       "1. Với mỗi loại filter (tag · ngày kết bạn · status · name · no filter), start scenario cho friend thoả và không thoả\n"
       "2. Kiểm tra LINE app từng friend\n3. Lặp toàn bộ trên bot mới và bot cũ sau khi release",
       "5 loại filter × bot cũ / bot mới",
       "- Cả 5 loại filter: chỉ friend thoả điều kiện nhận được message; no filter thì all friend nhận\n"
       "- Kết quả giống nhau trên bot cũ và bot mới",
       env="PRODUCTION",
       note="Tab「Scenario write DB riêng」. Nguồn: r12-r16, r19-r21"),

    tc("Backup & đổi bot", "CONC-001", "Boundary",
       "Improve sendall: cập nhật filter TRONG VÒNG 5 PHÚT trước giờ gửi step → job VẪN gửi theo filter CŨ; > 5 phút → gửi theo filter MỚI",
       "- Scenario S1 có step 日時で指定 sắp tới giờ gửi\n- Friend「たろう」đang thoả filter (có tag A)",
       "1. Case A — step CÓ filter: gỡ tag A của「たろう」TRONG VÒNG 5 phút trước giờ gửi → chờ tới giờ → "
       "kiểm tra LINE app + `step_message`.`send_count`\n"
       "2. Case B — step CÓ filter: gỡ tag A > 5 phút trước giờ gửi → kiểm tra\n"
       "3. Case C — step KHÔNG filter: THÊM filter trong vòng 5 phút trước giờ gửi → kiểm tra\n"
       "4. Case D — step KHÔNG filter: thêm filter > 5 phút trước giờ gửi → kiểm tra\n"
       "5. Case E — step CÓ filter: sửa filter trong vòng 5 phút / > 5 phút → kiểm tra",
       "Mốc 5 phút trước giờ gửi step",
       "- Trong vòng 5 phút: VẪN gửi cho「たろう」theo filter CŨ (DB đã update filter mới nhưng job dùng filter cũ); "
       "list user được send step VẪN tính「たろう」\n"
       "- > 5 phút: KHÔNG gửi cho「たろう」; list user được send step KHÔNG tính",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Cửa sổ 5 phút của scenario (broadcast là 10 phút) — spec KHÔNG ghi ở bất kỳ đâu (MT-04). "
            "Corpus r32 cũng ghi chú『job quét update DB chạy 5p 1 lần (stg / prod)』. RULE-08. "
            "Nguồn:「Improve sendall scenario」r3-r8"),

    tc("Backup & đổi bot", "CONC-001", "Boundary",
       "Improve sendall: đổi CẢ filter LẪN time step quanh mốc 5 phút → không gửi cho user bị loại, list send không tính",
       "- Scenario S1 có step 日時で指定 sắp tới giờ gửi; friend「たろう」đang thoả filter",
       "1. Case A: step còn > 5 phút → đổi filter + đổi time xuống còn < 5 phút → chờ → kiểm tra\n"
       "2. Case B: step còn < 5 phút → đổi filter + đổi time lên > 5 phút → chờ → kiểm tra\n"
       "3. Với mỗi case: kiểm tra LINE app「たろう」+ `step_message`.`send_count`",
       "2 hướng đổi time quanh mốc 5 phút",
       "- Cả 2 case: update filter được áp dụng → KHÔNG gửi cho「たろう」; list user được send step KHÔNG tính",
       env="PRODUCTION",
       note="Nguồn:「Improve sendall scenario」r9, r10"),

    # ══════════════════ 30. Phân quyền & môi trường ══════════════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Account STAFF không có quyền màn ステップ配信 → menu bị ẩn, hover hiển thị message không có quyền, không click vào được",
       "- Có account staff role 副管理人 và account staff role 運用者, cả 2 KHÔNG được cấp quyền màn scenario",
       "1. Đăng nhập bằng staff 副管理人\n2. Di chuột đến mục menu ステップ配信 (đang ẩn) → đọc nguyên văn message\n"
       "3. Click thử vào mục menu đó\n4. Cuộn trang xuống dưới → hover lại → kiểm tra vị trí hiển thị text\n"
       "5. Lặp toàn bộ với staff 運用者\n6. Lặp ở màn admin/home",
       "2 role staff: 副管理人 và 運用者; màn scenario không được cấp quyền",
       "- Hover hiển thị đúng nguyên văn:\n"
       "「操作できません。\nこの機能の操作権限が付与されていません。\n主管理者に操作権限を付与してもらうことで操作が可能となります。」\n"
       "- KHÔNG click vào được màn hình\n- Khi cuộn trang: text hiển thị đúng vị trí theo menu (không lệch)\n"
       "- Cùng kết quả ở màn admin/home",
       note="Tab「Phân quyền」(11/2023) — message dùng chung mọi màn. TC ~2.8 năm tuổi — **CẦN VERIFY LẠI**. "
            "Nguồn:「Phân quyền」r3-r14"),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Account STAFF CÓ quyền màn ステップ配信 → click vào được, không hiển thị text lỗi; chọn bot thành công",
       "- Account staff ĐƯỢC cấp quyền màn scenario",
       "1. Đăng nhập staff có quyền\n2. Di chuột đến mục menu ステップ配信 → quan sát\n3. Click vào mục menu\n"
       "4. Ở màn admin/home, click chọn bot",
       "Staff có quyền màn scenario",
       "- KHÔNG hiển thị text lỗi khi hover\n- Click vào được màn ステップ配信 bình thường\n- Chọn bot thành công",
       note="Nguồn:「Phân quyền」r6, r8, r10, r11, r13"),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Account STAFF thao tác trên màn scenario: xem list, tạo/sửa/xoá, send test, gửi step đều hoạt động đúng",
       "- Account staff ĐƯỢC cấp quyền màn scenario; bot A có scenario S1",
       "1. Đăng nhập staff, mở màn /basic/scenario → xem list, folder\n"
       "2. Tạo scenario mới / sửa / xoá → kiểm tra kết quả\n3. Tạo step, thêm message, thêm action → kiểm tra\n"
       "4. Send test 1 step và 一括テスト → kiểm tra LINE app\n5. Start scenario cho friend, chờ job gửi step → kiểm tra\n"
       "6. Kiểm tra profile sender khi staff send test",
       "Account staff có quyền, thao tác đầy đủ vòng đời scenario",
       "- Tất cả thao tác hoạt động đúng như account 主管理者\n- Send test và job gửi step đều thành công\n"
       "- Profile sender hiển thị đúng theo quy tắc của từng màn",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="⚠️ Corpus có nhiều dòng『Test trên account staff』/『Check account staff』(r796, r979, r202, r111, r169, "
            "「Job scenario」r202) nhưng phần lớn CHỈ ĐÁNH OK, KHÔNG có kết quả mong đợi cụ thể → kết quả mong đợi do AI "
            "viết. Spec §12 Gap #5 tự nhận『Quyền Staff: blade không có @can rõ ràng — không xác định được giới hạn quyền』. "
            "**TC lấp Gap #5** — CẦN LEADER XÁC NHẬN. Nguồn: r796, r979, r202, r111, r169, r245"),

    tc("Phân quyền & môi trường", "ENV-001", "Abnormal",
       "Khác biệt môi trường: job scen và job callback chạy trên 2 SERVER khác nhau → bộ đếm chống lặp đếm riêng, gây kết quả không nhất quán",
       JOB + "\n- Môi trường có job scenario và job callback tách server",
       "1. Cho scenario A vào trạng thái bị limit 10 lần qua đường NEXT SCENARIO\n"
       "2. Trigger start A qua CALLBACK (kết bạn) → quan sát có start được không\n"
       "3. Query bộ đếm chống lặp trên từng server (nếu truy cập được)\n"
       "4. So sánh kết quả giữa STAGING và PRODUCTION",
       "Scenario A đã bị limit qua next scenario; trigger lại qua callback",
       "- Bộ đếm chống lặp phải THỐNG NHẤT giữa các server\n"
       "- Đã bị limit qua đường next scenario thì trigger qua callback cũng bị chặn",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-41 — corpus「Job scenario」r40 ghi chú:『trên step job scen và callback đang ở 2 server khác nhau, nên đang "
            "count số lần start khác nhau → bị limit khi next scen rồi nhưng start từ callback vẫn được』. "
            "Đây là khác biệt hạ tầng, spec KHÔNG ghi. TC dự kiến FAIL → cần Leader chốt là bug hay chấp nhận được. "
            "RULE-08. Nguồn:「Job scenario」r40"),

    tc("Phân quyền & môi trường", "ENV-001", "Normal",
       "Khác biệt môi trường: job quét update step_message chạy 5 phút/lần trên staging và production → edit trong vòng 5 phút không kịp áp dụng",
       JOB + "\n- Scenario đang chạy cho friend; step sắp tới giờ gửi",
       "1. Trên STAGING: edit filter của step TRONG VÒNG 5 phút trước giờ gửi → chờ → kiểm tra LINE app\n"
       "2. Lặp trên PRODUCTION\n3. Edit filter > 5 phút trước giờ gửi trên cả 2 môi trường → kiểm tra\n"
       "4. So sánh kết quả 2 môi trường",
       "Mốc 5 phút; staging và production",
       "- Cả 2 môi trường: job quét update chạy 5 phút/lần\n"
       "- Edit trong vòng 5 phút: KHÔNG kịp áp dụng, job gửi theo data CŨ\n- Edit > 5 phút: áp dụng data MỚI",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="MT-04 — corpus r32 ghi chú:『job quét update DB chạy 5p 1 lần (stg / prod) => nếu update trong vòng 5p đó "
            "=> sẽ ko update => send cái cũ => muốn check được update cần để > 5 phút』. Spec §10 chỉ ghi PrepareFilterTask "
            "chạy mỗi 60 giây, KHÔNG ghi job 5 phút này. Nguồn: r32,「Improve sendall scenario」r3-r10"),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Scenario tạo trước bản improve (data cũ): edit khi đang start — đổi filter / thêm filter / edit time / edit msg / edit action / edit profile đều đúng",
       "- Bot có scenario DATA CŨ đang start cho friend, còn step chưa gửi",
       "1. Với scenario data cũ đang chạy: thay đổi filter của step chưa gửi → chờ > 5 phút → kiểm tra\n"
       "2. Thêm filter mới → kiểm tra\n3. Edit time send → kiểm tra friend nhận theo time đã update\n"
       "4. Edit message (thêm msg khác) → kiểm tra\n5. Edit action (no action → có action; đổi action) → kiểm tra\n"
       "6. Edit profile → kiểm tra người gửi trên LINE app",
       "Scenario data cũ đang chạy, 6 loại edit",
       "- Thay đổi filter: friend không thoả filter mới thì không nhận (cần chờ > 5 phút để job cập nhật)\n"
       "- Edit time: gửi theo time đã update\n- Edit message / action / profile: friend nhận nội dung và người gửi MỚI NHẤT",
       env="PRODUCTION",
       note="⚠️ Corpus r32 ghi chú rõ về job 5 phút. Nguồn: r32-r38"),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Scenario data cũ: dừng step giữa chừng cho friend → chỉ dừng đúng friend tương ứng",
       "- Bot có scenario DATA CŨ đang start cho 5 friend",
       "1. Dừng step giữa chừng cho 1 friend\n2. Kiểm tra 4 friend còn lại có tiếp tục nhận step không\n"
       "3. Query `scenario_lineuser` của 5 friend",
       "5 friend đang chạy scenario data cũ, dừng 1 friend",
       "- Chỉ friend được chọn bị dừng\n- 4 friend còn lại tiếp tục nhận step bình thường",
       env="PRODUCTION",
       note="Nguồn: r39"),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Scenario data cũ: check send đủ 3 loại step timing → gửi đúng time, không duplicate, đúng filter",
       "- Bot có scenario DATA CŨ với 3 step: send ngay · 日時で指定 · 経過時間; có filter AND và OR; có action richmenu",
       "1. Start scenario data cũ cho friend thoả và không thoả filter\n"
       "2. Với step send ngay (có msg, không profile, filter AND, action richmenu) → kiểm tra LINE app + richmenu\n"
       "3. Với step 日時で指定 (filter AND/OR, action richmenu) → kiểm tra\n"
       "4. Với step 経過時間 (filter AND/OR, có/không action richmenu) → kiểm tra\n"
       "5. Đếm số message nhận, kiểm tra thời điểm nhận",
       "3 loại step × filter AND/OR × có/không action richmenu",
       "- Cả 3 loại step: gửi ĐÚNG TIME, KHÔNG duplicate, ĐÚNG filter\n"
       "- Action richmenu được thực thi sau khi gửi step",
       env="PRODUCTION",
       note="RULE-06 + RULE-07. Nguồn: r29-r31"),

    tc("Phân quyền & môi trường", "DATA-MIG-001", "Normal",
       "Scenario data cũ: hiển thị đúng thời gian gửi, message, profile, action của từng step (action cần chạy recover)",
       "- Bot có scenario DATA CŨ với step có message, profile và action",
       "1. Mở màn list step của scenario data cũ\n2. Kiểm tra hiển thị: kiểu thời gian gửi của từng step\n"
       "3. Kiểm tra danh sách message trong step (đủ msg)\n4. Kiểm tra profile đã chọn\n"
       "5. Chạy job recover → kiểm tra action hiển thị",
       "Scenario data cũ có message + profile + action",
       "- Hiển thị ĐÚNG kiểu thời gian gửi của từng step\n- Hiển thị ĐỦ các message\n"
       "- Hiển thị ĐÚNG profile đã chọn\n- Sau job recover: hiển thị ĐÚNG action đã setting",
       env="PRODUCTION",
       note="⚠️ Corpus r28 ghi chú『cần chạy recover (Kiên)』để action hiển thị đúng — phụ thuộc job recover thủ công. "
            "Nguồn: r25-r28"),
]
