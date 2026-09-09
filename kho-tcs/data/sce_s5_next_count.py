# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 22-24: Next scenario · Bộ đếm friend · Màn list friend theo scenario.

Nguồn: tab「Testcase」(master) · tab「Job scenario」(Bug tự detect next qua ngày · Bug KH #32903 12/2025)
· tab「text fix bug Kh」(Bug #28916 03/2025 — cột 途中で終了した友だち)
· tab「Improve count scenario + tag」(12/2023, TCsLine_Improve chung).
"""
from _common import tc

SCE = "- Đăng nhập admin (主管理者), bot A\n- Scenario S1, S2 thuộc cùng bot; friend test đã kết bạn với bot A"
LIST = "- Đăng nhập admin (主管理者), bot A, màn /basic/scenario"

S5 = [
    # ══════════════════ 22. Next scenario ══════════════════
    tc("Next scenario", "UI-FIELD-001", "Normal",
       "Điều kiện HIỂN THỊ phần next scenario: tối thiểu 2 step, gồm (send ngay HOẶC 経過時間) VÀ (日時で指定) — chỉ hiển thị ở filter default",
       SCE + "\n- S1 có 2 filter: default và F-A",
       "1. Ở filter default, tạo 2 step: ステップ開始直後 + 日時で指定 1日後 10:00 → quan sát phần next scenario\n"
       "2. Thay bằng: 経過時間 02時間00分後 + 日時で指定 1日後 10:00 → quan sát\n"
       "3. Thay bằng: ステップ開始直後 + 経過時間 02時間00分後 (nhiều step) + 日時で指定 → quan sát\n"
       "4. Chuyển sang filter F-A, tạo cùng tổ hợp step → quan sát phần next scenario ở F-A",
       "3 tổ hợp step hợp lệ; kiểm tra ở cả filter default và filter branch",
       "- Cả 3 tổ hợp ở filter default: HIỂN THỊ phần chọn next scenario\n"
       "- Ở filter F-A: KHÔNG hiển thị phần next scenario (chỉ hiển thị ở filter default)",
       note="Nguồn: r833, r835, r837, r839"),

    tc("Next scenario", "UI-FIELD-001", "Abnormal",
       "Điều kiện KHÔNG hiển thị next scenario: không có step · chỉ 1 step · 2 step CÙNG loại timing",
       SCE + "\n- S1 chỉ có filter default",
       "1. Filter default không có step nào → quan sát phần next scenario\n"
       "2. Chỉ 1 step「ステップ開始直後」→ quan sát\n3. Chỉ 1 step「経過時間 02時間00分後」→ quan sát\n"
       "4. 2 step CÙNG loại 経過時間 (01時間 và 02時間) → quan sát\n"
       "5. 2 step CÙNG loại 日時で指定 (1日後 và 2日後) → quan sát",
       "5 trường hợp không đủ điều kiện",
       "- Cả 5 trường hợp: KHÔNG hiển thị phần chọn next scenario",
       note="5 input cùng 1 kết quả → giữ chung. Lưu ý: 1 filter chỉ có 1 step send ngay nên không có case 2 step send ngay. "
            "Nguồn: r840-r844"),

    tc("Next scenario", "UI-FIELD-001", "Abnormal",
       "Nhiều filter: filter default có step 経過時間, filter branch có step 日時で指定 → phần next scenario phải hiển thị theo tổng hợp step của scenario",
       SCE + "\n- S1: filter default chỉ có 1 step 経過時間 02時間00分後; filter F-A có 1 step 日時で指定 1日後 10:00",
       "1. Tạo cấu hình như tiền đề\n2. Đứng ở filter default, quan sát phần next scenario\n"
       "3. Thử các biến thể: filter gần nhau / xa nhau; filter đầu tiên là step send ngay hoặc 経過時間",
       "filter default: 経過時間 · F-A: 日時で指定",
       "- Phần next scenario HIỂN THỊ ở filter default (tổng hợp step của cả scenario đã đủ 2 loại timing)",
       spec="Đã hỏi leader",
       note="MT-33 — corpus r834 ghi kết quả thực thi:『filter default step duration + filter1 step send sau ngày giờ "
            "> KHÔNG hiển thị next sce』, trái với kết quả mong đợi ghi ở cùng dòng. Cần chốt quy tắc: điều kiện hiển thị "
            "tính theo TỪNG filter hay theo TOÀN scenario. Nguồn: r834, r836, r838"),

    tc("Next scenario", "DATA-DB-001", "Normal",
       "Chọn next scenario → DB scenario.after_scenario_id_1 lưu đúng id scenario kế tiếp",
       SCE + "\n- S1 đủ điều kiện hiển thị next scenario; có S2, S3 ở cùng folder và khác folder",
       "1. Ở S1, chọn next scenario = S2 (cùng folder) → lưu → query `scenario`.`after_scenario_id_1`\n"
       "2. Đổi sang S3 (khác folder) → lưu → query lại\n3. Đổi sang 1 scenario ở folder default 未分類 → lưu → query lại",
       "S2 cùng folder · S3 khác folder · 1 scenario ở 未分類",
       "- Cả 3 lần: `scenario`.`after_scenario_id_1` = id scenario vừa chọn\n"
       "- Dropdown chọn next scenario liệt kê được scenario ở CẢ 3 loại folder",
       note="Nguồn: r829"),

    tc("Next scenario", "OUT-001", "Normal",
       "Chạy hết scenario S1 → tự động start S2, friend nhận ĐỦ message của S2 và ĐÚNG thứ tự",
       SCE + "\n- S1 có 2 step (ステップ開始直後 + 経過時間 00時間02分後), next = S2\n"
       "- S2 có 3 step: ステップ開始直後 + 経過時間 00時間02分後 + 日時で指定 1日後 10:00\n- Friend「たろう」chưa start scenario nào",
       "1. Start S1 cho friend「たろう」\n2. Chờ S1 gửi hết 2 step\n3. Quan sát LINE app: có nhận message của S2 không\n"
       "4. Đếm số message và kiểm tra thứ tự\n5. Query `scenario_lineuser` của cả S1 và S2 cho friend đó\n"
       "6. Kiểm tra màn my_page của friend",
       "S1 (2 step) → next S2 (3 step)",
       "- Sau khi S1 gửi xong step cuối: S2 tự động được start cho friend\n"
       "- LINE app nhận ĐỦ message của S2, ĐÚNG thứ tự\n"
       "- `scenario_lineuser`: S1 chuyển sang trạng thái đã hoàn thành, S2 có bản ghi đang follow\n"
       "- Màn my_page hiển thị friend đang chạy S2",
       env="PRODUCTION",
       note="RULE-06 + RULE-07 + RULE-08 (job nền). Nguồn: r829, r13, r14"),

    tc("Next scenario", "MSG-001", "Normal",
       "Trigger next scenario hiển thị trên chat 1:1 với 機能名 ステップ配信 và 管理名 = tên scenario gốc",
       SCE + "\n- S1 next sang S2; friend「たろう」đã chạy xong S1",
       "1. Chờ S1 chạy xong và S2 được start\n2. Mở màn chat 1:1 của friend「たろう」\n"
       "3. Tìm trigger start scenario S2 → đọc nội dung chi tiết",
       "S1 → next S2",
       "- Chat 1:1 hiển thị trigger:\n  機能名:「ステップ配信」\n  管理名: tên của scenario S1 (scenario gốc)\n  詳細: -",
       env="PRODUCTION",
       note="Nguồn: r1058"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có step「ステップ開始直後」→ start được B và gửi ngay step đó",
       SCE + "\n- S1 (scenario A) next sang S2 (scenario B)\n- S2 có step「ステップ開始直後」và KHÔNG có loại step khác",
       "1. Start S1 cho friend, chờ chạy xong\n2. Quan sát LINE app khi S2 được start\n"
       "3. Query `scenario_lineuser` của S2\n4. Kiểm tra trigger ở màn chat 1:1",
       "S2 chỉ có 1 step ステップ開始直後",
       "- S2 được start thành công\n- Friend nhận NGAY message của step「ステップ開始直後」\n"
       "- Trigger start S2 hiển thị đúng trên màn chat 1:1",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r3"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có step 経過時間 (delay_type=2) → gửi sau đúng số giờ kể từ lúc B được start",
       SCE + "\n- S1 next sang S2\n- S2 có: step「ステップ開始直後」+ step 経過時間 00時間05分後, KHÔNG có step 日時で指定",
       "1. Start S1, chờ chạy xong, ghi lại thời điểm S2 được start (T0)\n"
       "2. Quan sát LINE app: thời điểm nhận step「ステップ開始直後」\n3. Quan sát thời điểm nhận step 経過時間\n"
       "4. Query `scenario_step_time`.`send_time` của step 経過時間",
       "S2: ステップ開始直後 + 経過時間 00時間05分後",
       "- Step「ステップ開始直後」gửi ngay tại T0\n"
       "- Step 経過時間 gửi tại T0 + 5 phút; `send_time` = T0 + 00:05",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r4, r13"),

    tc("Next scenario", "FUNC-DATE-001", "Boundary",
       "Bug tự detect: next scenario B có step 日時で指定 với ステップ開始から = 0 ngày — giờ gửi <, = hoặc > giờ hiện tại → quyết định gửi hôm nay hay ngày mai",
       SCE + "\n- S1 next sang S2\n- S2 có step「ステップ開始直後」+ step 日時で指定 0日後 lúc HH:MM\n"
       "- Chuẩn bị 3 lần chạy với 3 mốc giờ khác nhau so với thời điểm S2 được start",
       "1. Chạy S1 → S2 được start lúc 15:00. S2 có step 0日後 10:00 (< giờ hiện tại) → quan sát send_time\n"
       "2. Lặp với step 0日後 15:00 (= giờ hiện tại) → quan sát\n"
       "3. Lặp với step 0日後 18:00 (> giờ hiện tại) → quan sát\n"
       "4. Sau mỗi lần: query `scenario_step_time`.`send_time` + kiểm tra LINE app",
       "S2 start lúc 15:00; step 0日後 lần lượt 10:00 · 15:00 · 18:00",
       "- 10:00 (< giờ hiện tại): send_time = NGÀY MAI 10:00\n"
       "- 15:00 (= giờ hiện tại): send_time = NGÀY MAI 15:00\n"
       "- 18:00 (> giờ hiện tại): send_time = HÔM NAY 18:00\n"
       "- Cả 3 lần: step「ステップ開始直後」vẫn gửi ngay lúc 15:00",
       env="PRODUCTION",
       note="RULE-08. 3 mốc giờ cho 3 kết quả KHÁC nhau → nhưng nằm trong 1 chuỗi so sánh biên → giữ chung 1 TC boundary. "
            "Nguồn:「Job scenario」r5-r7, r14-r16"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có step 日時で指定 với ステップ開始から > 0 ngày → luôn gửi sau N ngày kể từ lúc B start",
       SCE + "\n- S1 next sang S2; S2 có step「ステップ開始直後」+ step 日時で指定 1日後 10:00",
       "1. Chạy S1 → S2 start lúc 15:00 ngày D\n2. Query `scenario_step_time`.`send_time` của step 1日後\n"
       "3. Kiểm tra LINE app tại thời điểm dự kiến",
       "S2 start 15:00 ngày D; step 1日後 10:00",
       "- send_time = ngày D+1 lúc 10:00\n- Friend nhận message đúng thời điểm đó",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r8, r17"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có ĐỒNG THỜI step 経過時間 và step 日時で指定 → cả 2 loại đều được lên lịch đúng, không lẫn nhau",
       SCE + "\n- S1 next sang S2\n- S2 có: ステップ開始直後 + 経過時間 00時間30分後 + 日時で指定 0日後 (3 biến thể giờ) và 1日後",
       "1. Chạy S1 → S2 start lúc 15:00\n2. Query `scenario_step_time` của TẤT CẢ step của S2\n"
       "3. Đối chiếu send_time từng step\n4. Kiểm tra LINE app nhận đủ message theo đúng mốc",
       "S2 start 15:00: step 経過時間 00時間30分後; step 0日後 10:00 / 15:00 / 18:00; step 1日後 10:00",
       "- Step ステップ開始直後: gửi ngay 15:00\n- Step 経過時間 00時間30分後: send_time = 15:30 cùng ngày\n"
       "- Step 0日後 10:00 và 15:00: send_time = ngày mai\n- Step 0日後 18:00: send_time = hôm nay 18:00\n"
       "- Step 1日後 10:00: send_time = ngày mai 10:00",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r9-r12, r18-r21"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có NHIỀU step 日時で指定: khi step day=0 bị đẩy sang ngày mai thì các step day>0 cũng dịch theo",
       SCE + "\n- S1 next sang S2; S2 có step 0日後 10:00 và step 1日後 10:00",
       "1. Chạy S1 → S2 start lúc 15:00 ngày D (giờ 10:00 đã qua)\n"
       "2. Query `scenario_step_time`.`send_time` của cả 2 step\n"
       "3. Lặp với S2 start lúc 08:00 ngày D (giờ 10:00 CHƯA qua)",
       "Lần 1: S2 start 15:00 (10:00 đã qua)\nLần 2: S2 start 08:00 (10:00 chưa qua)",
       "- Lần 1: step 0日後 → ngày D+1 lúc 10:00; step 1日後 → ngày D+2 lúc 10:00 (dịch theo)\n"
       "- Lần 2: step 0日後 → ngày D lúc 10:00; step 1日後 → ngày D+1 lúc 10:00",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r22-r24"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Next scenario B có NHIỀU step cùng day=0 khác giờ → xét theo step có time NHỎ NHẤT, tất cả cùng dịch sang ngày mai hoặc cùng gửi trong ngày",
       SCE + "\n- S1 next sang S2; S2 có 3 step day=0 lúc 10:00, 14:00, 20:00",
       "1. Chạy S1 → S2 start lúc 15:00 (step 10:00 và 14:00 đã qua)\n"
       "2. Query send_time của cả 3 step\n3. Lặp với S2 start lúc 08:00 (chưa step nào qua)",
       "3 step day=0: 10:00 · 14:00 · 20:00; S2 start 15:00 và 08:00",
       "- Start 15:00: TẤT CẢ 3 step day=0 dịch sang NGÀY MAI (10:00, 14:00, 20:00 ngày D+1)\n"
       "- Start 08:00: cả 3 step gửi TRONG NGÀY D",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-34 — quy tắc『xét theo step có time nhỏ nhất, tất cả cùng dịch』(r25-r27) khác với quy tắc『step nào quá giờ "
            "thì riêng nó dịch』ở TC start bình thường (r1026-r1027, r797). Cần Leader chốt phạm vi áp dụng. Nguồn:「Job scenario」r25-r27"),

    tc("Next scenario", "FUNC-DATE-001", "Abnormal",
       "Bug KH: scenario A có step day 0 lúc 20:00, next sang B cũng có step day 0 → step của B KHÔNG gửi ngay mà lùi sang ngày hôm sau",
       SCE + "\n- S1 (A) có 1 step 日時で指定 0日後 20:00, next sang S2 (B)\n- S2 (B) có 1 step 日時で指定 0日後 (giờ đã qua so với 20:00)",
       "1. Start S1 cho friend vào buổi sáng\n2. Chờ tới 20:00, S1 gửi step cuối và next sang S2\n"
       "3. Query `scenario_step_time`.`send_time` của step S2\n4. Quan sát LINE app: friend có nhận message S2 ngay lúc 20:00 không",
       "S1 step 0日後 20:00 → next S2 step 0日後 (giờ đã qua)",
       "- Step của S2 KHÔNG gửi ngay lúc 20:00\n- send_time lùi sang NGÀY HÔM SAU đúng giờ đã setting",
       env="PRODUCTION",
       note="Case lỗi của khách hàng đã được xử lý. Nguồn:「Job scenario」r28"),

    tc("Next scenario", "FUNC-DATE-001", "Normal",
       "Start scenario BÌNH THƯỜNG (không phải next) có step day=0: giờ <, = hiện tại → sang ngày mai; giờ > hiện tại → trong ngày",
       SCE + "\n- S1 có step 日時で指定 0日後 lúc HH:MM; friend chưa chạy scenario nào",
       "1. Start S1 lúc 15:00 với step 0日後 10:00 → query send_time\n2. Lặp với step 0日後 15:00 → query\n"
       "3. Lặp với step 0日後 18:00 → query\n4. Kiểm tra LINE app từng lần",
       "Start lúc 15:00; step 0日後 lần lượt 10:00 · 15:00 · 18:00",
       "- 10:00 và 15:00: send_time = NGÀY MAI\n- 18:00: send_time = HÔM NAY 18:00",
       env="PRODUCTION",
       note="Nguồn:「Job scenario」r29-r31, r1026, r1027"),

    tc("Next scenario", "STATE-DEP-001", "Abnormal",
       "Xoá step khiến scenario KHÔNG còn đủ điều kiện hiển thị next scenario → sau khi chạy xong scenario gốc, KHÔNG start next scenario đã chọn trước đó",
       SCE + "\n- S1 đủ điều kiện, đã chọn next = S2; S1 có 2 step (ステップ開始直後 + 日時で指定 1日後 10:00)",
       "1. Chọn next scenario = S2 cho S1, lưu\n2. Xoá step 日時で指定 → S1 chỉ còn 1 step, phần next scenario biến mất khỏi UI\n"
       "3. Query `scenario`.`after_scenario_id_1` của S1\n4. Start S1 cho friend, chờ chạy xong step còn lại\n"
       "5. Kiểm tra friend có được start S2 không + query `scenario_lineuser` của S2",
       "S1 chọn next = S2, sau đó xoá step khiến không đủ điều kiện",
       "- Phần chọn next scenario biến mất khỏi UI\n"
       "- Sau khi S1 chạy xong: friend KHÔNG được start S2\n- `scenario_lineuser` của S2 không có bản ghi mới cho friend đó",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Corpus r846 chỉ có tiêu đề và mô tả, KHÔNG có kết quả mong đợi cụ thể → kết quả mong đợi do AI viết ở tầng "
            "quan sát UI + LINE app. CẦN LEADER XÁC NHẬN. Nguồn: r845, r846"),

    tc("Next scenario", "STATE-DEP-001", "Abnormal",
       "Đang trong quá trình chạy S1, THAY ĐỔI next scenario → friend nhận đúng scenario mới và nhận ĐỦ message",
       SCE + "\n- S1 next = S2; friend đang chạy S1, còn 1 step chưa gửi; có S3 để đổi sang",
       "1. Start S1 cho friend\n2. Trong lúc S1 đang chạy, đổi next scenario của S1 từ S2 sang S3 → lưu\n"
       "3. Chờ S1 chạy xong\n4. Kiểm tra friend được start scenario nào\n"
       "5. Đếm số message friend nhận của scenario mới + query `scenario_lineuser`",
       "Đổi next từ S2 sang S3 khi S1 đang chạy",
       "- Friend được start S3 (scenario mới), KHÔNG start S2\n- Friend nhận ĐỦ message của S3, đúng thứ tự",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-35 — corpus r830 ghi kết quả thực thi:『db hiển thị status = 2 nhưng friend KHÔNG nhận đủ msg』. "
            "TC dự kiến FAIL → cần raise bug. Nguồn: r830"),

    tc("Next scenario", "STATE-DEP-001", "Normal",
       "Đang chạy scenario được start TỪ ACTION, khi tới lượt next scenario → next vẫn hoạt động đúng",
       SCE + "\n- S1 được start cho friend qua action (autoreply / tag / button), S1 next = S2",
       "1. Trigger action start S1 cho friend (vd qua autoreply)\n2. Chờ S1 chạy hết step\n"
       "3. Kiểm tra friend có được start S2 không\n4. Kiểm tra trigger trên chat 1:1",
       "S1 start qua action autoreply, next = S2",
       "- Friend được start S2 sau khi S1 chạy xong\n- Trigger next scenario hiển thị đúng trên chat 1:1",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Corpus r831 chỉ có tiêu đề, KHÔNG có kết quả mong đợi và KHÔNG có kết quả thực thi → kết quả mong đợi do AI "
            "suy từ r829. CẦN LEADER XÁC NHẬN. Nguồn: r831"),

    tc("Next scenario", "STATE-DEP-001", "Abnormal",
       "Đang chạy scenario, edit message / time / filter / action / tên step / sort msg → thay đổi được áp dụng đúng cho các step chưa gửi",
       SCE + "\n- S1 đang chạy cho friend, còn 2 step chưa gửi",
       "1. Start S1 cho friend\n2. Trong lúc chạy, lần lượt: thêm tên step · xoá msg · add msg · sort msg · edit msg · "
       "add action · edit filter · edit time\n3. Sau mỗi thao tác, query `step_message` và `scenario_step_time`\n"
       "4. Chờ tới lượt gửi step → kiểm tra LINE app friend nhận nội dung nào",
       "8 loại thao tác edit khi scenario đang chạy",
       "- Các thay đổi được lưu vào `step_message`\n- Với step CHƯA gửi: friend nhận nội dung MỚI NHẤT\n"
       "- Edit time: `scenario_step_time`.`send_time` được tính lại đúng",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-36 — corpus r832 ghi kết quả thực thi:『edit time trong ngày KHÔNG được cập nhật (từ 15p xuống 7p)』; "
            "r798 ghi『anh Tư chốt: Trong ngày KHÔNG update các TH — scenario đang start + add thêm step msg tương lai; "
            "edit time của step từ ngày giờ sang send sau bn phút』. Cần chốt: đây là hành vi cố ý hay bug. Nguồn: r832, r798"),

    # ══════════════════ 23. Bộ đếm friend ══════════════════
    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Tạo scenario mới → count_follow = 0, count_stop = 0, count_unfinish = 0; 3 cột đếm ngoài màn list đều hiển thị 0人",
       LIST,
       "1. Tạo scenario mới S-new\n2. Quan sát 3 cột 購読中の友だち / 途中で終了した友だち / 読了済の友だち ở màn list\n"
       "3. Query `scenario`.`count_follow`, `count_stop`, `count_unfinish` WHERE id = <S-new>",
       "Scenario vừa tạo",
       "- Cả 3 cột hiển thị 0人\n- DB: count_follow = 0, count_stop = 0, count_unfinish = 0",
       note="Nguồn:「Improve count scenario + tag」r3"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Start MỚI scenario cho friend (chưa có bản ghi scenario_lineuser) → count_follow +1, các counter khác giữ nguyên",
       LIST + "\n- Scenario S1 có count_follow = 3, count_stop = 2, count_unfinish = 1\n- Friend「たろう」chưa có bản ghi scenario_lineuser với S1",
       "1. Ghi lại 3 counter của S1\n2. Từ màn my_page của friend「たろう」, start scenario S1\n"
       "3. Query lại 3 counter + `scenario_lineuser` của「たろう」\n4. Quan sát 3 cột đếm ngoài màn list",
       "count_follow 3 → ? · friend chưa từng chạy S1",
       "- count_follow = 4 (+1)\n- count_stop = 2 và count_unfinish = 1 (giữ nguyên)\n"
       "- `scenario_lineuser`: tạo bản ghi mới với is_following = 1\n- Cột 購読中の友だち ngoài màn list hiển thị 4人",
       note="Nguồn:「Improve count scenario + tag」r4, r15"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Start LẠI scenario cho friend đã có bản ghi: is_following = 1 → giữ nguyên counter",
       LIST + "\n- Friend「たろう」đang có `scenario_lineuser` với S1, is_following = 1",
       "1. Ghi lại 3 counter của S1\n2. Start lại S1 cho「たろう」từ màn my_page\n3. Query lại 3 counter",
       "friend đang 購読中 (is_following = 1)",
       "- Cả 3 counter GIỮ NGUYÊN (không cộng thêm)",
       note="Nguồn:「Improve count scenario + tag」r5, r16"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Start LẠI scenario cho friend đã DỪNG GIỮA CHỪNG (is_following = 0) → count_follow +1, count_unfinish −1",
       LIST + "\n- Friend「たろう」có `scenario_lineuser` với S1, is_following = 0 (途中で終了)\n- S1: count_follow = 3, count_unfinish = 2",
       "1. Ghi lại 3 counter\n2. Start lại S1 cho「たろう」\n3. Query lại 3 counter + `scenario_lineuser`.`is_following`\n"
       "4. Quan sát 3 cột đếm ngoài màn list",
       "is_following trước = 0; count_follow 3, count_unfinish 2",
       "- count_follow = 4 (+1)\n- count_unfinish = 1 (−1)\n- count_stop giữ nguyên\n"
       "- `is_following` chuyển sang 1\n- Cột 途中で終了した友だち giảm 1, cột 購読中の友だち tăng 1",
       spec="Đã hỏi leader",
       note="MT-01 — mapping is_following ↔ counter. Corpus 03/2025 (「text fix bug Kh」r61) ghi is_following = 0 "
            "⇔ count_unfinish; nhưng `feature-spec.md` §6 và `db/db-mapping.md:419` ghi is_following = 0 ⇔ 読了済 ⇔ count_stop. "
            "Corpus CŨ 12/2023 (r6) còn ghi is_following = 0 → count_stop −1 (thời điểm chưa có count_unfinish). Nguồn: r6, r61"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Start LẠI scenario cho friend đã CHẠY XONG (is_following = 2) → count_follow +1, count_stop −1",
       LIST + "\n- Friend「たろう」có `scenario_lineuser` với S1, is_following = 2 (読了済)\n- S1: count_follow = 3, count_stop = 4",
       "1. Ghi lại 3 counter\n2. Start lại S1 cho「たろう」\n3. Query lại 3 counter + `is_following`\n4. Quan sát 3 cột đếm",
       "is_following trước = 2; count_follow 3, count_stop 4",
       "- count_follow = 4 (+1)\n- count_stop = 3 (−1)\n- count_unfinish giữ nguyên\n- `is_following` chuyển sang 1",
       spec="Đã hỏi leader",
       note="MT-01. Nguồn:「text fix bug Kh」r62;「Improve count scenario + tag」r7, r18"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Stop scenario GIỮA CHỪNG cho friend → count_follow −1, count_unfinish +1, friend hiện ở cột 途中で終了した友だち",
       LIST + "\n- Friend「たろう」đang chạy S1 (is_following = 1), còn 2 step chưa gửi\n- S1: count_follow = 4, count_unfinish = 1",
       "1. Ghi lại 3 counter\n2. Từ màn my_page hoặc chat 1:1, action STOP scenario S1 cho「たろう」\n"
       "3. Query 3 counter + `scenario_lineuser`.`is_following`\n"
       "4. Ở màn list scenario, click nút 表示 cột 途中で終了した友だち → tìm「たろう」\n5. Kiểm tra LINE app: có nhận msg stop không",
       "count_follow 4, count_unfinish 1; stop giữa chừng",
       "- count_follow = 3 (−1), count_unfinish = 2 (+1), count_stop giữ nguyên\n"
       "- `is_following` = 0\n- Friend「たろう」xuất hiện trong danh sách 途中で終了した友だち\n- Friend nhận msg stop trên LINE",
       env="PRODUCTION",
       note="Bug #28916 (12-03-2025) bổ sung cột 途中で終了した友だち. RULE-07. Nguồn:「text fix bug Kh」r36, r59;"
            "「Improve count scenario + tag」r8, r19"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Abnormal",
       "Friend ĐANG DỪNG rồi lại có action STOP tiếp → counter giữ nguyên (không trừ/cộng 2 lần)",
       LIST + "\n- Friend「たろう」đã stop S1 (is_following = 0)",
       "1. Ghi lại 3 counter\n2. Thực hiện action STOP scenario S1 cho「たろう」lần nữa\n3. Query lại 3 counter",
       "friend đã ở trạng thái stop",
       "- Cả 3 counter GIỮ NGUYÊN, không thay đổi",
       note="Nguồn:「Improve count scenario + tag」r9, r20"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Abnormal",
       "Stop scenario cho friend CHƯA từng start scenario nào → không có action nào xảy ra, không tăng/giảm counter",
       LIST + "\n- Friend「はなこ」chưa từng start scenario nào",
       "1. Ghi lại 3 counter của S1\n2. Ở chat 1:1 hoặc friend list, chọn action Stop scenario cho「はなこ」\n"
       "3. Query 3 counter + `scenario_lineuser`\n4. Kiểm tra LINE app của「はなこ」",
       "Friend chưa từng start scenario",
       "- KHÔNG có action nào xảy ra\n- Cả 3 counter không thay đổi\n"
       "- `scenario_lineuser` không tạo bản ghi mới\n- Friend không nhận message stop",
       note="Nguồn:「text fix bug Kh」r35"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Abnormal",
       "Start scenario nhưng KHÔNG còn step nào thoả mãn giờ gửi → dừng ngay, friend vào cột 途中で終了した友だち",
       LIST + "\n- Scenario S1 chỉ có 1 step 日時で指定 0日後 10:00; thời điểm start là 15:00 hôm đó\n"
       "- Trường hợp b: friend đã có bản ghi is_following = 1; trường hợp c: is_following = 0 hoặc 2",
       "1. Trường hợp a — friend CHƯA có bản ghi: start S1 lúc 15:00 → query 3 counter + is_following\n"
       "2. Trường hợp b — friend đang is_following = 1: start lại → query\n"
       "3. Trường hợp c — friend đang is_following = 0 hoặc 2: start lại → query\n"
       "4. Với mỗi trường hợp: quan sát cột 途中で終了した友だち ngoài màn list",
       "3 trạng thái trước đó của friend",
       "- (a) chưa có bản ghi: count_follow GIỮ NGUYÊN, count_unfinish +1\n"
       "- (b) is_following = 1: count_follow −1, count_unfinish +1\n"
       "- (c) is_following = 0 hoặc 2: cả 3 counter giữ nguyên\n"
       "- Cả 3 trường hợp: `scenario_lineuser`.`is_following` → 2 và friend hiển thị ở cột 途中で終了した友だち",
       spec="Đã hỏi leader",
       note="MT-01 — MÂU THUẪN NGAY TRONG CÙNG TAB: r58 ghi『途中で終了した友だち = 1, count_unfinish = 1, is_follow = 2』"
            "nhưng r60 (cùng tab, 03/2025) ghi『is_following = 2 → count_stop +1』. Ngoài ra r10-r12 (12/2023) ghi "
            "count_stop +1 và đánh dấu『đang bị cộng count_follow』. Nguồn: r58, r60, r10-r12, r21-r23, r35-r37"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Friend đang chạy scenario A → được start sang scenario B: A giảm follow tăng unfinish, B tăng follow",
       LIST + "\n- Friend「たろう」đang chạy S1 (is_following = 1); S2 là scenario khác\n"
       "- Trường hợp 1: friend chưa có bản ghi với S2; Trường hợp 2: friend đã có bản ghi với S2 (is_following = 2)",
       "1. Ghi lại counter của S1 và S2\n2. Trường hợp 1: start S2 cho「たろう」→ query counter cả S1 và S2\n"
       "3. Trường hợp 2 (chuẩn bị lại): friend đã từng chạy xong S2, start lại S2 → query counter cả 2",
       "S1 đang chạy; S2 chưa/đã có bản ghi",
       "- S1: count_follow −1, count_unfinish +1 (dừng giữa chừng)\n"
       "- S2 trường hợp 1: count_follow +1, count_stop giữ nguyên\n"
       "- S2 trường hợp 2: count_follow +1, count_stop −1",
       spec="Đã hỏi leader",
       note="MT-01 — corpus 12/2023 (r13, r14) ghi S1『count_follow −1, count_stop +1』(thời điểm chưa có count_unfinish); "
            "corpus 03/2025 (「text fix bug Kh」r38, r56) ghi『stop scen A: count_unfinish = 1』. Đã áp bản mới. "
            "Ghi chú corpus r14:『chưa trừ count_stop của B』. Nguồn: r13, r14, r24, r25, r38, r56"),

    tc("Bộ đếm friend", "BULK-001", "Normal",
       "Action start/stop scenario cho NHIỀU friend cùng lúc → số cộng/trừ vào counter đúng bằng số friend được action",
       LIST + "\n- S1 có count_follow = 0; chuẩn bị 10 friend chưa từng chạy S1",
       "1. Từ màn friend list, chọn 10 friend → action START scenario S1\n2. Query `scenario`.`count_follow`\n"
       "3. Chọn 6 trong 10 friend đó → action STOP\n4. Query lại count_follow và count_unfinish",
       "10 friend start, sau đó 6 friend stop",
       "- Sau start: count_follow = 10\n- Sau stop 6 friend: count_follow = 4, count_unfinish = 6",
       env="PRODUCTION",
       note="Nguồn:「Improve count scenario + tag」r26"),

    tc("Bộ đếm friend", "FRIEND-001", "Normal",
       "Bot BLOCK friend → counter cập nhật (count_follow −1) cho scenario friend đó đang chạy",
       LIST + "\n- Friend「たろう」đang chạy S1 (is_following = 1); S1 count_follow = 5",
       "1. Ghi lại 3 counter của S1\n2. Bot thực hiện block friend「たろう」\n3. Query lại 3 counter + `scenario_lineuser`\n"
       "4. Quan sát 3 cột đếm ngoài màn list",
       "Bot block friend đang chạy scenario",
       "- count_follow = 4 (−1)\n- Counter tương ứng trạng thái dừng tăng 1",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-02 — corpus 12/2023 (r27) ghi『count_follow −1, count_stop +1』và đánh dấu『chưa cộng count_stop』; "
            "sau khi Bug #28916 (03/2025) tách cột 途中で終了 thì friend bị block giữa chừng thuộc nhóm nào (count_stop hay "
            "count_unfinish) CHƯA có TC nào verify lại. Spec không ghi. Nguồn: r27, r234-r237"),

    tc("Bộ đếm friend", "DATA-CASCADE-001", "Normal",
       "XOÁ friend → duyệt toàn bộ bản ghi scenario_lineuser của friend đó và trừ counter tương ứng",
       LIST + "\n- Friend「たろう」có bản ghi ở 3 scenario: S1 (is_following = 1), S2 (is_following = 0), S3 (is_following = 2)",
       "1. Ghi lại 3 counter của cả S1, S2, S3\n2. Xoá friend「たろう」ở màn friend list\n"
       "3. Query lại 3 counter của cả 3 scenario",
       "Friend có bản ghi ở 3 scenario với 3 trạng thái khác nhau",
       "- S1 (is_following = 1): count_follow −1\n"
       "- S2 (is_following = 0): counter tương ứng trạng thái dừng −1\n"
       "- S3 (is_following = 2): counter tương ứng −1\n- Không counter nào bị âm",
       env="PRODUCTION",
       note="MT-01 liên quan (counter nào ứng với is_following 0 / 2). Nguồn:「Improve count scenario + tag」r28"),

    tc("Bộ đếm friend", "JOB-001", "Normal",
       "Start / stop scenario TỪ PHÍA JOB (multi action của autoreply, tag, button...) → counter cập nhật giống phía web",
       LIST + "\n- Chuẩn bị autoreply có action start scenario S1 và autoreply khác có action stop S1\n"
       "- Chuẩn bị friend ở 3 trạng thái: chưa có bản ghi · is_following = 1 · is_following = 0/2",
       "1. Trigger autoreply START S1 cho friend chưa có bản ghi → query counter\n"
       "2. Trigger START cho friend đang is_following = 1 → query\n3. Trigger START cho friend is_following = 0 và = 2 → query\n"
       "4. Trigger STOP cho friend đang chạy → query\n5. Trigger STOP lần 2 cho friend đã dừng → query\n"
       "6. Start scenario nhưng không còn step thoả mãn → query",
       "6 kịch bản, tất cả trigger qua JOB",
       "- Kết quả counter GIỐNG HỆT các case tương ứng ở phía web (start mới +1 follow; start lại theo trạng thái cũ; "
       "stop −1 follow +1 unfinish; stop lần 2 giữ nguyên)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-37 — corpus「Improve count scenario + tag」r30 ghi chú『Vẫn bị update』(khi is_following = 1 start lại), "
            "r33 ghi『không update』(stop giữa chừng), r35 ghi『đang bị cộng count_follow』→ phía JOB có ít nhất 3 điểm lệch "
            "so với phía web. RULE-08: job nền → PRODUCTION. Nguồn:「Improve count scenario + tag」r29-r38"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Cột 購読中の友だち: hiển thị số friend đang follow; double click vào số không gây lỗi; friend chạy xong chuyển sang 読了済",
       LIST + "\n- S1 có 10 friend đang chạy, 0 friend đã xong",
       "1. Quan sát cột 購読中の友だち và 読了済の友だち\n2. Double click vào con số ở cột 購読中の友だち\n"
       "3. Chờ toàn bộ 10 friend chạy xong scenario\n4. Quan sát lại 2 cột\n"
       "5. Query `step_message`.`send_count` của các step đã gửi",
       "10 friend chạy S1 từ đầu tới cuối",
       "- Ban đầu: 購読中 = 10人, 読了済 = 0人\n- Double click vào số: chỉ mở 1 lần màn list friend, không lỗi\n"
       "- Sau khi chạy xong: 購読中 = 0人, 読了済 = 10人\n"
       "- `step_message`.`send_count` của từng step = số friend đã nhận step đó",
       env="PRODUCTION",
       note="Nguồn: r231-r233, r238-r241"),

    tc("Bộ đếm friend", "FRIEND-001", "Abnormal",
       "Friend BỊ CHẶN trong quá trình scenario chạy → chuyển sang cột hiển thị trạng thái dừng; mở chặn giữa chừng không đưa lại về 購読中",
       LIST + "\n- S1 đang chạy cho 5 friend, trong đó 2 friend sẽ block bot giữa chừng",
       "1. Start S1 cho 5 friend\n2. Trong lúc chạy, cho 2 friend block bot\n"
       "3. Quan sát 3 cột đếm TRONG quá trình chạy\n4. Cho 1 trong 2 friend mở chặn giữa chừng → quan sát 3 cột\n"
       "5. Chờ scenario chạy xong → quan sát 3 cột",
       "5 friend; 2 friend block; 1 friend mở chặn giữa chừng",
       "- Trong quá trình chạy: 購読中 = số friend đang follow; friend bị chặn chuyển sang cột trạng thái dừng\n"
       "- Sau khi chạy xong: 購読中 = 0人, toàn bộ friend nằm ở cột trạng thái đã kết thúc",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-02 — corpus r234-r237 (2024, TRƯỚC Bug #28916) chỉ có 2 cột và ghi friend bị chặn vào 読了済の友だち; "
            "sau khi tách cột 途中で終了した友だち (03/2025) thì friend bị chặn giữa chừng thuộc cột nào CHƯA được retest. "
            "TC > 2 năm tuổi — **CẦN VERIFY LẠI**. Nguồn: r234-r237"),

    tc("Bộ đếm friend", "DATA-COUNT-001", "Normal",
       "Bug #28916: xoá STEP CUỐI của scenario đang chạy → friend đang chờ step đó chuyển sang trạng thái đã kết thúc",
       LIST + "\n- S1 có 3 step; 5 friend đang chạy: 2 friend đã nhận xong step 2, đang chờ step 3",
       "1. Ghi lại 3 counter của S1\n2. Xoá step 3 (step cuối)\n3. Query 3 counter + `scenario_lineuser`.`is_following` của 5 friend\n"
       "4. Quan sát 3 cột đếm ngoài màn list\n5. Trường hợp b: friend đã chạy hết step 2, đang chờ step 3 có time xa (N ngày) → lặp bước 2-4",
       "5 friend, 2 friend đang chờ step cuối",
       "- Friend đang chờ step bị xoá chuyển sang cột 読了済の友だち (đã gửi hết)\n"
       "- count_follow của các friend đang chạy chuyển sang counter trạng thái kết thúc",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-01 — corpus r41 ghi『hiển thị ở 読了済の友だち, scenario trường count_unfinish』— NÊU 2 THỨ TRÁI NHAU trong cùng "
            "1 dòng (hiển thị ở 読了済 nhưng ghi vào count_unfinish). Nguồn:「text fix bug Kh」r41, r42"),

    tc("Bộ đếm friend", "FUNC-DATE-001", "Normal",
       "Action start scenario TỪ GIỮA (chọn option start sau N ngày): N khớp với step → gửi; N vượt quá step cuối → dừng luôn",
       SCE + "\n- S1 có step 日時で指定 2日後 10:00 là step cuối",
       "1. Ở chat 1:1, multi action → start scenario S1, chọn option start sau 2 ngày → quan sát\n"
       "2. Query `scenario_lineuser` + `scenario_step_time`\n"
       "3. Lặp: chọn option start sau 3 ngày (vượt quá step cuối) → quan sát\n"
       "4. Query `scenario_lineuser`.`is_following` + `scenario`.`count_stop` / `count_unfinish`\n"
       "5. Kiểm tra LINE app friend",
       "S1 step cuối = 2日後; chọn start sau 2 ngày và sau 3 ngày",
       "- Chọn 2 ngày: thoả mãn, friend được start và nhận message của step đó\n"
       "- Chọn 3 ngày: gửi msg「không thoả mãn」; `scenario_lineuser`.`is_following` = 2; counter trạng thái dừng +1",
       env="PRODUCTION",
       note="Nguồn:「text fix bug Kh」r39, r40"),

    tc("Bộ đếm friend", "REG-SHARED-001", "Normal",
       "Bug #28916: cột 途中で終了した友だち hoạt động đúng với scenario tạo mới ở cả 3 loại step và với bản copy",
       LIST,
       "1. Tạo scenario mới với step「ステップ開始直後」→ start + stop giữa chừng cho 1 friend → kiểm tra 3 cột\n"
       "2. Lặp với step 日時で指定 N日後 00:00\n3. Lặp với step 経過時間 XX時間YY分後\n"
       "4. Tạo step send ngay rồi XOÁ luôn step đó → click ra ngoài → kiểm tra 3 cột ở màn list\n"
       "5. Copy 1 scenario có sẵn → kiểm tra bản copy có đủ step như bản gốc và 3 cột đếm = 0",
       "3 loại step + case xoá hết step + case copy",
       "- 3 loại step: cột 途中で終了した友だち đếm đúng khi stop giữa chừng\n"
       "- Xoá hết step: cả 3 cột hiển thị 0人\n- Bản copy: đủ step như bản gốc, 3 cột đếm = 0人",
       note="Bug #28916. Nguồn:「text fix bug Kh」r28-r34"),

    tc("Bộ đếm friend", "JOB-001", "Normal",
       "Bug #28916 (triển khai ngang): cột 途中で終了した友だち cập nhật đúng khi start/stop scenario từ 10 nguồn action khác nhau",
       LIST + "\n- Chuẩn bị 10 điểm trigger action scenario",
       "1. Với mỗi nguồn dưới đây, trigger start hoặc stop scenario S1 cho friend test\n"
       "2. Sau mỗi lần: query 3 counter + `scenario_lineuser`.`is_following` + quan sát 3 cột ngoài màn list",
       "10 nguồn: (1) màn setting add friend · (2) Template button · (3) Template image map · (4) Rich menu · "
       "(5) Action autoreply · (6) action schedule · (7) action của tag · (8) action của scenario · (9) action broadcast · "
       "(10) action form / booking / item",
       "- Cả 10 nguồn: 3 counter và 3 cột đếm cập nhật ĐÚNG như thao tác từ màn my_page\n"
       "- `scenario_lineuser`.`is_following` chuyển đúng trạng thái",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Corpus r43-r55 ghi 10 nguồn nhưng KHÔNG có kết quả mong đợi (chỉ đánh OK/để trống ở r52, r55) → kết quả "
            "mong đợi do AI suy từ quy tắc chung. CẦN LEADER XÁC NHẬN. RULE-08: job nền → PRODUCTION. "
            "Nguồn:「text fix bug Kh」r43-r55"),

    # ══════════════════ 24. Màn list friend theo scenario ══════════════════
    tc("Màn list friend theo scenario", "LIST-001", "Normal",
       "Click nút 表示 ở 3 cột đếm → mở màn danh sách friend đúng nhóm trạng thái",
       LIST + "\n- S1 có 5 friend 購読中, 3 friend 途中で終了, 4 friend 読了済",
       "1. Click nút「表示」ở cột 購読中の友だち → đếm số friend trong danh sách\n"
       "2. Quay lại, click「表示」ở cột 途中で終了した友だち → đếm\n3. Click「表示」ở cột 読了済の友だち → đếm\n"
       "4. Đối chiếu với con số hiển thị ở từng cột",
       "5 購読中 · 3 途中で終了 · 4 読了済",
       "- Mỗi lần mở đúng danh sách friend của nhóm tương ứng\n"
       "- Số friend trong danh sách KHỚP con số hiển thị ở cột",
       note="Nguồn: r231-r241 + spec SCR-SCE-06 (type=0, userCount='start'/'stop')"),

    tc("Màn list friend theo scenario", "FUNC-001", "Normal",
       "Bug KH #32903: từ list friend 途中で終了 — chọn ALL / chọn 1 friend / thêm filter, với ≤ ngưỡng friend → web send, chỉ friend được chọn nhận action",
       LIST + "\n- S1 có 5 friend ở nhóm 途中で終了; bot có tổng ≥ 20 friend khác không thuộc nhóm này\n"
       "- Chuẩn bị action gắn tag「テストタグ」",
       "1. Click「表示」cột 途中で終了した友だち → màn list friend\n2. Chọn ALL friend hiển thị → setting action gắn tag → thực hiện\n"
       "3. Query `filters_v2` (bản ghi vừa insert) + kiểm tra tag của TẤT CẢ friend của bot\n"
       "4. Lặp: chỉ chọn 1 friend → send action → kiểm tra\n5. Lặp: thêm filter rồi chọn → send action → kiểm tra",
       "5 friend nhóm 途中で終了 (≤ ngưỡng); bot có ≥ 25 friend tổng",
       "- Cả 3 cách chọn: DB insert bản ghi `filters_v2`\n"
       "- CHỈ những friend được chọn nhận action gắn tag\n- Các friend khác của bot KHÔNG bị gắn tag",
       env="PRODUCTION",
       note="Bug KH #32903 (26-11-2025) — bug gốc là『setting gắn tag cho list friend trong mục 表示された友だち "
            "nhưng tag lại được gắn cho ALL friends』. RULE-07. Nguồn:「Job scenario」r205-r207"),

    tc("Màn list friend theo scenario", "BULK-001", "Normal",
       "Bug KH #32903: list friend 途中で終了 với số friend VƯỢT ngưỡng — không tick 条件に当てはまる友だち{XX}人全員を選択 → WEB send; có tick → JOB send (tạo action schedule)",
       LIST + "\n- S1 có > ngưỡng friend ở nhóm 途中で終了 (môi trường test đặt ngưỡng 5; PRODUCTION là 1000)",
       "1. Mở list friend 途中で終了 (số friend > ngưỡng)\n"
       "2. Chọn all friend nhưng KHÔNG tick「条件に当てはまる友だち{XX}人全員を選択」→ send action → quan sát cơ chế gửi\n"
       "3. Chọn all friend và CÓ tick option đó → send action → query bảng action schedule\n"
       "4. Thêm điều kiện filter AND ra > ngưỡng friend + tick option → send action → quan sát\n"
       "5. Lặp bước 4 với filter OR\n6. Kiểm tra friend nhận action đúng phạm vi",
       "Ngưỡng test = 5 friend (PRODUCTION = 1000 friend)",
       "- Không tick: WEB send trực tiếp\n- Có tick (cả 3 case: all / filter AND / filter OR): JOB send, có tạo action schedule\n"
       "- Friend nhận action đúng phạm vi đã chọn/lọc",
       env="PRODUCTION",
       note="⚠️ NGƯỠNG KHÁC NHAU GIỮA MÔI TRƯỜNG: mô tả bug ghi『> 1000 friend → job send; < 1000 friend → web send』"
            "nhưng TC chạy với ngưỡng 5 friend (config môi trường test) → phải verify lại ngưỡng thật trên PRODUCTION. "
            "Nguồn:「Job scenario」r204, r208-r211"),

    tc("Màn list friend theo scenario", "FUNC-001", "Normal",
       "Bug KH #32903: lặp toàn bộ kịch bản action với list friend 読了済 (đã send xong)",
       LIST + "\n- S1 có 5 friend nhóm 読了済 (case ≤ ngưỡng) và > 5 friend (case vượt ngưỡng)",
       "1. Click「表示」cột 読了済の友だち\n2. Case ≤ ngưỡng: chọn all / chọn 1 friend / thêm filter → send action → kiểm tra\n"
       "3. Case > ngưỡng: không tick / có tick option 全員を選択 / filter AND / filter OR → send action → kiểm tra",
       "Nhóm 読了済: 5 friend và > 5 friend",
       "- ≤ ngưỡng: insert `filters_v2`, chỉ friend được chọn nhận action\n"
       "- > ngưỡng: không tick → web send; có tick → job send tạo action schedule",
       env="PRODUCTION",
       note="Bug KH #32903. Nguồn:「Job scenario」r213-r219"),

    tc("Màn list friend theo scenario", "FUNC-001", "Normal",
       "Bug KH #32903: lặp kịch bản action với list friend ĐANG SEND (購読中) — có filter thì chỉ friend thoả filter nhận action",
       LIST + "\n- S1 có 5 friend nhóm 購読中 và > 5 friend cho case vượt ngưỡng",
       "1. Click「表示」cột 購読中の友だち\n2. ≤ ngưỡng: chọn all → send action; thêm filter → send action → kiểm tra phạm vi\n"
       "3. > ngưỡng: không tick option → web send cho ALL friend đang chạy scenario\n"
       "4. > ngưỡng: có tick option → job send tạo action schedule, send cho all friend đang chạy scenario\n"
       "5. > ngưỡng + filter ra > 5 friend + tick option → job send, chỉ friend đang chạy scenario VÀ thoả filter nhận action",
       "Nhóm 購読中: 5 friend và > 5 friend, có/không filter",
       "- ≤ ngưỡng chọn all: insert filters_v2, đúng friend được chọn\n"
       "- ≤ ngưỡng + filter: CHỈ friend thoả filter nhận action\n"
       "- > ngưỡng không tick: web send cho all friend đang chạy scenario\n"
       "- > ngưỡng có tick: job send; nếu có filter thì giao của (đang chạy scenario) ∩ (thoả filter)",
       env="PRODUCTION",
       note="Bug KH #32903. Nguồn:「Job scenario」r220-r224"),

    tc("Màn list friend theo scenario", "REG-SHARED-001", "Normal",
       "Bug KH #32903: màn friend list vào từ MENU (không qua scenario) — kịch bản action vẫn đúng",
       "- Đăng nhập admin, bot A\n- Vào màn 友だち管理 từ menu, bot có ≥ 20 friend",
       "1. Vào màn friend list từ menu\n2. ≤ ngưỡng: chọn all / chọn 1 friend / thêm filter → send action → kiểm tra\n"
       "3. > ngưỡng: không tick option → web send\n4. > ngưỡng: có tick option → job send cho ALL friend\n"
       "5. > ngưỡng + filter + tick option → job send cho friend thoả filter",
       "Ngưỡng test = 5 friend",
       "- ≤ ngưỡng: insert `filters_v2`, đúng friend được chọn nhận action\n"
       "- > ngưỡng không tick: web send\n- > ngưỡng có tick: job send tạo action schedule, gửi cho all friend\n"
       "- > ngưỡng + filter: chỉ friend thoả filter nhận action",
       env="PRODUCTION",
       note="Bug KH #32903 — cover màn gốc. Nguồn:「Job scenario」r225-r230"),

    tc("Màn list friend theo scenario", "CONC-001", "Abnormal",
       "Bug KH #32903: job chưa kịp chạy mà user vào thao tác trên GUI → sau khi edit action và bật lại job, vẫn send đúng số lượng người",
       LIST + "\n- Đã tạo action schedule (job send) cho list friend 途中で終了 nhưng job đang TẮT",
       "1. Tạo action schedule cho list friend (chưa bật job)\n2. Trong lúc job chưa chạy, vào modal edit filter của action đó → quan sát\n"
       "3. Click hiển thị số lượng người → quan sát\n4. Edit action rồi lưu\n5. Bật lại job → chờ job chạy\n"
       "6. Đếm số friend thực tế nhận action",
       "Action schedule chưa được job xử lý",
       "- Vào modal edit filter: type mới KHÔNG hiển thị được điều kiện filter; click hiển thị số lượng người KHÔNG ra kết quả\n"
       "- Sau khi edit action và bật lại job: VẪN send đúng số lượng người ở list friend đang dừng scenario",
       env="PRODUCTION",
       note="Bug KH #32903. Nguồn:「Job scenario」r212"),

    tc("Màn list friend theo scenario", "REG-SHARED-001", "Normal",
       "Bug KH #32903 (triển khai ngang sau release): 4 màn khác cũng dùng cùng cơ chế list friend + action phải hoạt động đúng",
       "- Đăng nhập admin, bot A; chuẩn bị data cho 4 màn dưới",
       "1. Màn send all → tab 配信予約 → click vào 配信数 → mở list friend → chọn + send action → kiểm tra phạm vi\n"
       "2. Màn send all → tab 下書き → click vào 配信数 → lặp\n"
       "3. Màn quản lý tag → click button 表示 của cột 友だち数 → lặp\n"
       "4. Màn quản lý CSV → cột 対象人数 → lặp\n"
       "5. Màn richmenu → setting hiển thị/stop richmenu → chọn đối tượng → lặp",
       "5 điểm tham chiếu ngoài màn scenario",
       "- Cả 5 điểm: mở đúng list friend, action CHỈ áp dụng cho friend được chọn/thoả filter\n"
       "- Không xảy ra hiện tượng gắn tag cho ALL friend của bot",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Corpus「Job scenario」r231-r235 chỉ có tiêu đề, KHÔNG có kết quả mong đợi → kết quả mong đợi do AI suy từ "
            "root cause Bug KH #32903 (thiếu filter khi tạo action schedule). CẦN LEADER XÁC NHẬN. Nguồn:「Job scenario」r231-r235"),
]
