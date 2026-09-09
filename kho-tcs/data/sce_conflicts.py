# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "`is_following` = 0 và = 2 ứng với counter nào: count_stop hay count_unfinish?",
     "「text fix bug Kh」r59-r62 (03/2025, sau Bug #28916):\n"
     "• is_following = 0 → count_unfinish +1, count_follow −1\n"
     "• is_following = 2 → count_stop +1, count_follow −1\n"
     "• start lại: trước đó 0 → count_unfinish −1; trước đó 2 → count_stop −1\n"
     "NHƯNG CÙNG TAB r58 lại ghi: start không có step thoả mãn → 「途中で終了した友だち = 1, count_unfinish = 1, "
     "is_follow = **2**」— tức 2 ⇔ count_unfinish, TRÁI với r60.\n"
     "Corpus CŨ 12/2023 (「Improve count scenario + tag」r8) ghi: stop giữa chừng → is_following = 0 → count_stop +1 "
     "(thời điểm chưa có cột count_unfinish).",
     "`feature-spec.md` §6 bảng `scenario_lineuser.is_following`: 1 = 購読中 → count_follow · **0 = 読了済 → count_stop** "
     "· **2 = 途中で終了 → count_unfinish**.\n"
     "`db/db-mapping.md:419`: 「count_unfinish có thể tương ứng riêng với is_following = 2, còn count_stop tương ứng với "
     "is_following = 0 — **nhưng cần xác nhận thêm từ logic update counter**」.\n"
     "NGƯỢC LẠI: `web/logic-spec.md` BR-10 dòng 533: 「count_follow = số user is_following=1, **count_stop = số user "
     "is_following=2**」(không nhắc count_unfinish).\n"
     "`job/job-spec.md` BR-5: 「is_last_step = 1 → ScenarioLineuser.is_following = **2 (hoàn thành)**」.",
     "3 nguồn spec nói 2 kiểu ngược nhau, corpus cũng tự mâu thuẫn trong CÙNG 1 TAB. Đây là cột hiển thị cho khách hàng "
     "(購読中 / 途中で終了 / 読了済) — sai mapping thì SỐ LIỆU BÁO CÁO CHO KHÁCH SAI. Kéo theo hàng loạt TC counter, "
     "TC job gửi step cuối, TC xoá step/filter đều không xác định được kết quả mong đợi.",
     "TC-SCE-315, TC-SCE-316, TC-SCE-320, TC-SCE-321, TC-SCE-324, TC-SCE-328, TC-SCE-341 (Bộ đếm friend · Job gửi step & is_last_step)",
     "",
     "① Query PRODUCTION: `SELECT is_following, COUNT(*) FROM scenario_lineuser WHERE scenario_id = X GROUP BY is_following` "
     "rồi đối chiếu với 3 cột hiển thị của scenario X trên GUI.\n"
     "② Đọc code `countScenario($scenarioId)` để lấy mapping thật.\n"
     "③ Sửa cho khớp: `feature-spec.md` §6 · `db/db-mapping.md:419` · `web/logic-spec.md` BR-10 (bổ sung count_unfinish) "
     "· `web/logic-spec.md` bảng trường ScenarioLineuser dòng 398 (đang ghi「0=chưa」rất mơ hồ).\n"
     "④ Sửa lại kết quả mong đợi của toàn bộ TC nhóm『Bộ đếm friend』theo mapping đã chốt."],

    ["MT-02", "CAO", W,
     "Friend bị BLOCK giữa chừng scenario → vào cột 読了済 hay 途中で終了?",
     "r234-r237 (khối『Check data mới』, 2024 — TRƯỚC Bug #28916): 「trong quá trình start: cột 購読中の友だち = sl friend "
     "đang follow; cột **読了済の友だち = sl friend bị chặn**」.\n"
     "「Improve count scenario + tag」r27 (12/2023): 「Check stop scenario khi bot block friend → count_follow −1, "
     "**count_stop +1**」và ghi chú kết quả test『chưa cộng count_stop』.\n"
     "Sau khi Bug #28916 (12-03-2025) tách thêm cột 途中で終了した友だち thì **KHÔNG có TC nào retest lại** case block.",
     "Không có mục nào trong `feature-spec.md` / `web/logic-spec.md` / `job/job-spec.md` mô tả hành vi counter khi friend "
     "block bot giữa chừng scenario.",
     "Friend block giữa chừng về bản chất là『dừng giữa chừng』chứ không phải『đã đọc xong』. Nếu vẫn đếm vào 読了済 thì "
     "khách hàng nhìn báo cáo sẽ tưởng friend đã nhận hết chuỗi tin — sai lệch nghiệp vụ. TC nguồn > 2 năm tuổi, "
     "chưa retest sau khi tách cột.",
     "TC-SCE-323, TC-SCE-327 (Bộ đếm friend)",
     "",
     "① Chốt: friend block giữa chừng thuộc 途中で終了 hay 読了済.\n"
     "② Test lại thật trên PRODUCTION (TC đánh dấu CẦN VERIFY LẠI).\n"
     "③ Bổ sung Business Rule mới vào `feature-spec.md` §7 mô tả rõ 3 nhánh: hoàn thành step cuối / bị stop thủ công / "
     "bị block-unfollow.\n"
     "④ Kiểm tra luôn case unblock giữa chừng có đưa friend trở lại 購読中 không."],

    ["MT-03", "CAO", W,
     "Chống lặp vô hạn: đạt 10 lần/giờ thì CHỈ notify hay CÓ CHẶN start scenario?",
     "「Job scenario」r37-r41 (Bug tự detect):\n"
     "• Đạt 10 lần trong 1 giờ → 「notify chatwork **KHÔNG start scenario A**」\n"
     "• r40: start từ JOB (autoreply, tag) → 「**không start lại được** scen A: bảng scenario_lineuser không update "
     "is_following, bảng scenario_step_time không add bản ghi」nhưng『vẫn có message start hiển thị ở màn chat 1:1』và "
     "『nếu scen A có step send ngay thì **vẫn send được step send ngay**』\n"
     "• r41: start từ WEB (chat 1:1) → 「**vẫn start được** scen A」",
     "`feature-spec.md` §10 Error Handling: 「Scenario lặp vô hạn — MonitorScenarioManager: > 10 lần/giờ cho cùng "
     "scenarioId + userId → **Chatwork alert**」.\n"
     "`job/job-spec.md` cũng chỉ nêu alert. **KHÔNG chỗ nào nói có CHẶN start**, cũng không nói phân biệt nguồn "
     "job / web, cũng không nói step send ngay vẫn được gửi.",
     "Spec mô tả đây là cơ chế CẢNH BÁO, corpus mô tả là cơ chế CHẶN có điều kiện với hành vi nửa vời (chặn schedule "
     "nhưng vẫn gửi step send ngay và vẫn hiện trigger trên chat 1:1). Tester đọc spec sẽ không test nhánh chặn; "
     "dev đọc spec sẽ không biết web và job hành xử khác nhau.",
     "TC-SCE-373, TC-SCE-374 (Chống lặp vô hạn)",
     "",
     "① Xác nhận với dev: cơ chế chặn có thật không, ngưỡng là ≥ 10 hay > 10.\n"
     "② Chốt hành vi mong muốn: khi bị chặn thì có nên vẫn gửi step send ngay và vẫn hiện trigger không (hiện tại đang "
     "gây hiểu nhầm cho khách).\n"
     "③ Chốt: web có nên được miễn trừ khỏi giới hạn không.\n"
     "④ Bổ sung Business Rule mới vào `feature-spec.md` §7 và mở rộng §10 Error Handling."],

    ["MT-04", "CAO", W,
     "Cửa sổ 5 phút của job quét update step_message — spec không ghi ở bất kỳ đâu",
     "r32 (ghi chú): 「job quét update DB chạy **5p 1 lần (stg / prod)** => nếu update trong vòng 5p đó => sẽ ko update "
     "=> send cái cũ => muốn check được update cần để > 5 phút」.\n"
     "「Improve sendall scenario」r3-r10: cập nhật filter TRONG VÒNG 5 phút trước giờ gửi → job VẪN gửi theo filter CŨ, "
     "list user được send VẪN tính; > 5 phút → áp filter MỚI. (Broadcast dùng mốc **10 phút**.)\n"
     "r998: 「job update sẽ chạy 5p 1 lần => khi tbl step_message.is_new = 0 thì step đó sẽ được update vào scenario_step_time」.",
     "`feature-spec.md` §10 chỉ mô tả: PrepareFilterTask chạy **mỗi 60 giây**, PrepareTemplateTask『định kỳ』, scanner "
     "poll 100ms. **KHÔNG có job 5 phút nào được mô tả.**\n"
     "`db/db-mapping.md:100` có cột `step_message.is_new` (1 = mới, 2 = đã update — dùng cho sync) nhưng không mô tả "
     "chu kỳ job đọc cột này.",
     "Đây là cửa sổ thời gian mà thao tác của khách hàng KHÔNG có hiệu lực — khách sửa filter/nội dung sát giờ gửi thì "
     "tin vẫn đi theo bản cũ. Không có trong spec nghĩa là dev mới và tester mới sẽ không biết, dễ kết luận sai là bug. "
     "Đồng thời con số 5 phút (scenario) vs 10 phút (broadcast) khác nhau mà không ai giải thích.",
     "TC-SCE-399, TC-SCE-405 (Backup & đổi bot · Phân quyền & môi trường)",
     "",
     "① Xác nhận với dev chu kỳ thật của job quét `step_message.is_new` trên PRODUCTION.\n"
     "② Bổ sung vào `feature-spec.md` §10 và `job/job-spec.md` một mục riêng cho job đồng bộ step_message (chu kỳ, "
     "cột is_new, hệ quả cửa sổ 5 phút).\n"
     "③ Giải thích vì sao scenario 5 phút mà broadcast 10 phút.\n"
     "④ Cân nhắc hiển thị cảnh báo trên UI khi khách sửa step sát giờ gửi (giống broadcast đã có "
     "「配信予定日時5分前からは配信内容の編集はできません。」)."],

    ["MT-05", "CAO", W,
     "Xoá scenario / xoá folder chứa scenario xoá những bảng nào — corpus bỏ trống, spec có nhưng chưa ai đối chiếu",
     "r373/r387: 「xoá scenario **đang start cho user** → lúc này data như nào?」— **Cần Confirm**, bỏ trống kết quả mong đợi.\n"
     "r374/r388: 「xóa thành công thì xóa thông tin những bảng nào?」— **Cần Confirm**.\n"
     "r174 (xoá folder có scenario): 「Xóa những bảng nào? - Nếu scenario đã được add trong action của send all, remind, "
     "calendar, template, bill tiền...」— **Cần Confirm**.",
     "`feature-spec.md` §7 mục 7 + `web/logic-spec.md` `deletedDataScenario()` liệt kê ĐỦ 8 bước cascade: "
     "scenario_step_time → step_message → scenario → scenario_lineuser → step_message_history → cleanup filters_v2 "
     "(type='scenario') → cleanup action_detail (type='scenario', action ∈ 2,3). Ghi rõ「Không có soft delete — xóa vĩnh viễn」.\n"
     "NHƯNG spec chỉ mô tả cho XOÁ SCENARIO; **không mô tả cascade khi xoá FOLDER** chứa scenario.",
     "3 dòng『Cần Confirm』trong corpus là điểm mù kéo dài từ 2024 — không ai biết xoá scenario đang chạy thì friend "
     "đang nhận step sẽ ra sao, và xoá folder có kéo theo cascade đầy đủ không. Đây là thao tác KHÔNG HOÀN TÁC ĐƯỢC "
     "(hard delete), rủi ro mất dữ liệu khách hàng.",
     "TC-SCE-17, TC-SCE-104, TC-SCE-105 (Folder scenario · Xóa scenario)",
     "",
     "① Chốt kết quả mong đợi cho 3 dòng『Cần Confirm』theo spec BR-08 (TCs đề xuất đã lấp sẵn).\n"
     "② Bổ sung vào `feature-spec.md` §7 một mục riêng cho XOÁ FOLDER: có cascade sang scenario bên trong không, "
     "và cascade tới đâu.\n"
     "③ Ghi rõ hành vi với friend đang chạy scenario bị xoá (còn nhận step không, my_page hiển thị gì).\n"
     "④ Cân nhắc thêm cảnh báo trên UI trước khi xoá folder có scenario đang chạy."],

    ["MT-06", "CAO", W,
     "Đổi vị trí folder scenario → 8 điểm tham chiếu KHÔNG apply thứ tự mới",
     "r138 (Chat 1:1): kết quả thực thi **NG** — 「vị trí folder vẫn như cũ」.\n"
     "r139-r145 (Modal action, Message send all, Button, Scenario, Remind, Calendar 5-1, Bill tiền item 6): **bỏ trống "
     "hoàn toàn** cả kết quả mong đợi lẫn kết quả thực thi — tester đã dừng test sau khi thấy NG ở điểm đầu tiên.\n"
     "Đối chiếu: r156-r163 (đổi TÊN folder) và r210-r217 (tạo mới) đều OK ở cả 8 điểm.",
     "`feature-spec.md` §3 chỉ mô tả action「Sắp xếp folder — AJAX ajaxGetListScenario action=sortFolder」; "
     "`web/logic-spec.md` mô tả `sortFolder` chỉ update `Category.position`.\n"
     "**Không spec nào nói thứ tự folder phải được đồng bộ sang 8 điểm tham chiếu khác.**",
     "Đổi TÊN folder thì 8 điểm apply được, nhưng đổi THỨ TỰ thì không — hành vi không nhất quán. Khách hàng sắp xếp "
     "folder cho dễ dùng rồi vào modal action lại thấy thứ tự cũ, dễ chọn nhầm scenario khi setting action. "
     "7/8 điểm chưa từng được test.",
     "TC-SCE-34 (Sắp xếp folder)",
     "",
     "① Test lại đủ 8 điểm trên PRODUCTION (TC đã đánh dấu dự kiến FAIL).\n"
     "② Nếu vẫn tái hiện → raise bug: các màn khác đang lấy folder theo `id` hoặc `created_at` thay vì `position`.\n"
     "③ Chốt: thứ tự folder có phải là thuộc tính dùng chung toàn hệ thống không.\n"
     "④ Bổ sung Business Rule vào `feature-spec.md` §7 về phạm vi áp dụng của `category.position`."],

    ["MT-07", "THẤP", W,
     "Nút phân trang < / > khi disable vẫn hiển thị con trỏ hình bàn tay",
     "r391: kết quả thực thi **NG** — 「disable nhưng khi hover vào vẫn hiển thị hình bàn tay」.",
     "Không có mục nào trong spec mô tả trạng thái con trỏ của nút phân trang.",
     "Lỗi UI nhỏ nhưng gây hiểu nhầm: người dùng tưởng bấm được. Đây là hạng mục Check UI chung, dễ bị bỏ qua khi "
     "review vì không ảnh hưởng chức năng.",
     "TC-SCE-58 (Tìm kiếm & phân trang list)",
     "",
     "① Xác nhận còn tái hiện không.\n"
     "② Nếu còn → raise bug UI (thêm `cursor: default` / `pointer-events: none` cho nút disable).\n"
     "③ Cân nhắc triển khai ngang cho các màn khác có phân trang."],

    ["MT-08", "TRUNG BÌNH", W,
     "Đóng modal tạo scenario rồi mở lại → trường FOLDER không được reset",
     "r218-r219: 「Check dữ liệu có được reset khi click đóng (X)」→ kết quả thực thi **NG**: 「chưa reset folder」. "
     "(Trường 管理名 thì có reset.)",
     "`feature-spec.md` §3 mô tả luồng tạo scenario nhưng không nêu quy tắc reset form khi đóng modal.",
     "Người dùng mở modal, đổi folder, đóng lại, rồi mở modal khác để tạo scenario ở folder đang đứng — nhưng folder "
     "vẫn giữ giá trị lần trước → tạo scenario NHẦM FOLDER mà không nhận ra. Kết hợp với MT-09 (menu tự đổi focus) "
     "thì càng dễ nhầm.",
     "TC-SCE-69 (Tạo scenario)",
     "",
     "① Xác nhận còn tái hiện không.\n"
     "② Nếu còn → raise bug: reset toàn bộ form (kể cả folder) khi đóng modal.\n"
     "③ Bổ sung quy tắc reset form vào `ui/ui-spec.md` cho modal tạo scenario."],

    ["MT-09", "TRUNG BÌNH", W,
     "Chọn folder khác TRONG modal tạo scenario → menu folder BÊN NGOÀI cũng tự đổi focus khi chưa lưu",
     "r220: kết quả OK nhưng ghi chú 「chọn folder khác ở menu **cũng đổi luôn sang focus thằng mới**」.\n"
     "r221: 「ở trên đang sai nên **k test tiếp nữa**」— tester dừng, các case sau bỏ trống.",
     "`web/logic-spec.md` BR-01 mô tả folder active lưu trong cookie `folder_scenario`, reset về 0 nếu không hợp lệ. "
     "Không nói khi nào cookie được cập nhật (lúc chọn trong modal hay lúc lưu thành công).",
     "Nếu user mở modal, đổi folder rồi HUỶ, panel folder bên ngoài đã nhảy sang folder khác → user mất ngữ cảnh đang "
     "làm việc. Ngoài ra vì tester dừng test nên nhánh『tạo scenario ở folder 未分類』chưa được cover đầy đủ.",
     "TC-SCE-74 (Tạo scenario)",
     "",
     "① Chốt: cookie `folder_scenario` nên được cập nhật lúc CHỌN hay lúc LƯU THÀNH CÔNG.\n"
     "② Nếu chốt là lúc lưu → raise bug.\n"
     "③ Bổ sung thời điểm cập nhật cookie vào `web/logic-spec.md` BR-01.\n"
     "④ Test lại toàn bộ nhánh r221-r230 đã bị bỏ dở."],

    ["MT-10", "TRUNG BÌNH", W,
     "Đổi folder của scenario → vị trí scenario trong folder đích theo quy tắc nào?",
     "r307 (未分類 → folder khác): ghi chú 「sce đang ở **đầu** danh sách」.\n"
     "r308 (folder khác → 未分類): ghi chú 「scen đang ở **vị trí thứ 7** từ trên xuống」.\n"
     "r309 (folder A → folder B): ghi chú 「scenario hiển thị **sai vị trí** trong bảng (không ở cuối)」.\n"
     "Đối chiếu: r289-r292 (一括フォルダ変更) không nêu vấn đề vị trí.",
     "`web/logic-spec.md` `ajaxGetListScenario` action `moveItem`: 「Update `group_id` **và** `position` cho nhiều "
     "scenario sang folder khác」— có update position nhưng không nói tính thế nào.\n"
     "`ScenarioController@update` (đổi folder từ màn detail): chỉ update `name`, `after_scenario_id_1`, `group_id` — "
     "**KHÔNG update `position`**.",
     "Hai đường đổi folder (bulk 一括フォルダ変更 vs edit trong màn detail) dùng 2 code path khác nhau: một cái update "
     "position, một cái không → vị trí hiển thị bất định. Ghi chú của tester cho 3 hướng move ra 3 vị trí khác nhau.",
     "TC-SCE-80 (Sửa scenario)",
     "",
     "① Chốt quy tắc vị trí sau khi đổi folder (luôn xuống cuối / giữ position cũ / lên đầu).\n"
     "② Đối chiếu 2 code path (`update` và `moveItem`) cho thống nhất.\n"
     "③ Bổ sung quy tắc vào `feature-spec.md` §7 và `web/logic-spec.md` phần `update()`."],

    ["MT-11", "TRUNG BÌNH", W,
     "Trim space và giới hạn ký tự KHÔNG hoạt động ở nhiều ô nhập của màn scenario",
     "Các dòng đánh **NG** hoặc ghi chú lỗi:\n"
     "• r324 (管理名 scenario, nhập toàn khoảng trắng) — **NG**\n"
     "• r326 (管理名 scenario, trim space) — **NG**\n"
     "• r335 (tên điều kiện filter, > 10 ký tự) — **NG**\n"
     "• r336 / r409 (tên điều kiện filter, trim space) — **NG**\n"
     "• r407 (tên điều kiện filter, max 10 ký tự) — **NG**\n"
     "• r471 (メッセージ管理名, trim space) — **NG**\n"
     "• r352 (メッセージ管理名) — **NG**: 「nhập khoảng trắng vẫn đang success」\n"
     "Đối chiếu: r8 lại ghi「Các input text **đã** tự động trim space đầu cuối chưa?」→ OK.",
     "`feature-spec.md` §9 Validation Rules chỉ có: EP-02 `name` required max:20; EP-03 `name_edit` required; "
     "EP-18 action_image_map. **KHÔNG có rule trim space**, **KHÔNG có giới hạn 10 ký tự** cho tên filter và tên step, "
     "**KHÔNG có rule chặn chuỗi toàn khoảng trắng**.",
     "7 điểm NG trải khắp 3 ô nhập khác nhau (tên scenario, tên filter, tên step) — không phải lỗi lẻ mà là thiếu "
     "chuẩn validate chung. Chuỗi toàn khoảng trắng lọt qua `required` sẽ tạo bản ghi có tên rỗng, khách không phân "
     "biệt được các scenario/step với nhau.",
     "TC-SCE-86, TC-SCE-137, TC-SCE-188 (Sửa scenario · Filter phân nhánh 配信対象 · Tên quản lý step)",
     "",
     "① Chốt chuẩn chung: mọi ô text ở màn scenario đều trim đầu/cuối trước khi validate và trước khi lưu.\n"
     "② Chốt: chuỗi toàn khoảng trắng = rỗng → trigger rule `required`.\n"
     "③ Xác nhận giới hạn 10 ký tự cho tên filter và tên step có phải chuẩn không.\n"
     "④ Bổ sung 3 rule trên vào `feature-spec.md` §9 Validation Rules; raise bug cho 7 điểm NG."],

    ["MT-12", "THẤP", W,
     "Xoá scenario → popup sort group scenario không cập nhật ngay, phải reload",
     "r365: kết quả thực thi **NG** — 「phải reset mới mất」.\n"
     "Đối chiếu: r381 (sau xoá hàng loạt) và r294 (sau chuyển folder) đều OK.",
     "Không có mục nào trong spec mô tả việc đồng bộ popup sort sau thao tác xoá.",
     "Popup sort hiển thị scenario đã bị xoá → user kéo-thả nhầm bản ghi không tồn tại, có thể gây lỗi khi lưu thứ tự. "
     "Bất nhất với luồng xoá hàng loạt (đã đúng).",
     "TC-SCE-102 (Xóa scenario)",
     "",
     "① Xác nhận còn tái hiện không.\n"
     "② Nếu còn → raise bug: reload danh sách trong popup sort sau khi xoá đơn lẻ (giống luồng xoá hàng loạt).\n"
     "③ Rà thêm các popup khác có cùng vấn đề (popup sort folder)."],

    ["MT-13", "TRUNG BÌNH", W,
     "Đổi số bản ghi/trang từ 100 → 50 ở filter branch → bị redirect về filter default",
     "r875: kết quả thực thi **NG** — 「khi chuyển từ 100 về 50 đang **redirect sang filter default**」.\n"
     "「improve sce 20/6」r12 (20/6/2024): cùng nội dung, cũng **NG**.\n"
     "「21/11」r24: hiện tượng liên quan — 「khi ở page 2 của filter khác default => click vào filter default => "
     "đang bị **mất data**」.",
     "`web/logic-spec.md` `getListStepMessageV3`: 「Filter theo `filter_manager_id` (null → không có filter; có → có "
     "filter). `simplePaginate` theo `per_page`」. Không mô tả hành vi khi đổi per_page hay khi chuyển filter.",
     "Bug tồn tại từ 06/2024 đến nay (được ghi lại ở 2 tab cách nhau ~2 năm) mà chưa fix. Người dùng đang làm việc "
     "trên 1 nhánh filter, đổi số bản ghi hiển thị thì bị đá về nhánh khác — mất ngữ cảnh, dễ sửa nhầm step của "
     "nhánh không định sửa.",
     "TC-SCE-122 (Màn list step & phân trang)",
     "",
     "① Xác nhận còn tái hiện trên bản hiện tại không (bug ghi nhận từ 06/2024).\n"
     "② Nếu còn → raise bug: giữ `filter_manager_id` khi đổi `per_page`.\n"
     "③ Xử lý luôn case mất data khi chuyển filter từ trang 2.\n"
     "④ Bổ sung quy tắc giữ ngữ cảnh filter + reset trang về 1 vào `web/logic-spec.md`."],

    ["MT-14", "THẤP", W,
     "Text cảnh báo khi vượt giới hạn 100 step/filter: 2 nội dung khác nhau",
     "「improve sce 20/6」r6 (20/6/2024) và r869: 「hiển thị cảnh báo **「100以上登録できません。」**」.",
     "`feature-spec.md` §7 mục 11 và §9 Validation Rules: 「UI hiển thị cảnh báo "
     "**「1つの配信対象に登録できる配信タイミングは100までです。」**khi đạt giới hạn」.",
     "2 chuỗi hoàn toàn khác nhau. Spec được viết từ source code (2026) nên có thể mới hơn corpus (2024), nhưng nếu "
     "cả 2 cùng tồn tại ở 2 luồng khác nhau (thêm step thủ công vs copy hàng loạt) thì đó là bất nhất UX cần chốt.",
     "TC-SCE-124 (Màn list step & phân trang)",
     "",
     "① Kiểm tra trên PRODUCTION cả 2 luồng: (a) bấm 配信タイミング khi đã đủ 100 step, (b) 一括引用登録 làm vượt 100.\n"
     "② Nếu 2 luồng ra 2 message khác nhau → chốt thống nhất 1 message.\n"
     "③ Cập nhật `feature-spec.md` §9 cho khớp thực tế."],

    ["MT-15", "TRUNG BÌNH", W,
     "Sửa TÊN điều kiện filter làm MẤT nội dung filter đang hiển thị",
     "r413: kết quả OK nhưng ghi chú 「edit tên đk filter **mất nội dung filter**, reset mới hiển thị lại nd」.",
     "`web/logic-spec.md` `saveCommonStepMessage` (type='filter'): 「Gọi `saveFilter()` để tạo/update `FilterManager` "
     "(type='scenario'). Cập nhật `filter_v2` liên kết」. Không mô tả việc đổi tên có ảnh hưởng tới `filters_v2` không.",
     "Nếu chỉ là lỗi hiển thị (reload lại thấy) thì là bug UI; nhưng nếu `filters_v2` thật sự bị xoá khi đổi tên thì "
     "là MẤT DỮ LIỆU điều kiện lọc — scenario sẽ gửi cho sai đối tượng. Ghi chú không đủ rõ để phân biệt.",
     "TC-SCE-139 (Filter phân nhánh 配信対象)",
     "",
     "① Test lại và query `filters_v2` NGAY sau khi đổi tên (chưa reload) để xác định là lỗi hiển thị hay mất data.\n"
     "② Nếu mất data → BLOCKER, raise bug ngay.\n"
     "③ Bổ sung vào `web/logic-spec.md` mô tả rõ `saveFilter()` xử lý riêng name và data như thế nào."],

    ["MT-16", "THẤP", W,
     "Sau khi xoá filter branch → focus về filter default hay filter bên cạnh?",
     "r421: kết quả mong đợi 「sau khi xóa hệ thống **focus vào filter default 友だち全員(絞り込みなし)**」nhưng kết quả "
     "thực thi ghi 「đang **focus filter bên cạnh**」.\n"
     "r854 cũng ghi chú alert khi xoá filter『aleart đang chưa phù hợp』.",
     "Không có mục nào trong spec mô tả hành vi focus sau khi xoá filter branch.",
     "Không ảnh hưởng dữ liệu nhưng ảnh hưởng thao tác: nếu focus nhảy sang filter bên cạnh, user có thể tưởng đang ở "
     "filter default và thêm step nhầm nhánh — hệ quả là gửi tin cho sai đối tượng.",
     "TC-SCE-141 (Filter phân nhánh 配信対象)",
     "",
     "① Chốt hành vi mong muốn (default hay filter liền kề).\n"
     "② Kiểm tra luôn nội dung alert xoá filter đã phù hợp chưa (ghi chú r854).\n"
     "③ Bổ sung vào `ui/ui-spec.md`."],

    ["MT-17", "THẤP", W,
     "Filter vừa add trong cùng phiên: phải click 2 lần vào icon xoá mới hiện popup confirm",
     "r418: kết quả OK nhưng ghi chú 「đang phải **click đến lần 2** mới hiển thị popup confirm xóa」.\n"
     "r419 (filter cũ, đã reload): bình thường.",
     "Không có mục nào trong spec mô tả hành vi này.",
     "Chỉ xảy ra với filter vừa được thêm chưa reload → nghi vấn binding event của Vue chưa gắn cho phần tử mới render. "
     "Cùng họ với bug index kéo-thả ở #35968 (`:key` track theo index).",
     "TC-SCE-143 (Filter phân nhánh 配信対象)",
     "",
     "① Xác nhận còn tái hiện không.\n"
     "② Nếu còn → raise bug và kiểm tra chung cơ chế bind event cho phần tử render động ở màn scenario.\n"
     "③ Triển khai ngang: rà các nút thao tác khác trên filter vừa add (edit, thêm step)."],

    ["MT-18", "TRUNG BÌNH", W,
     "Xoá filter của scenario ĐANG start cho friend → dữ liệu tiến trình xử lý ra sao?",
     "r424: 「xoá filter của scenario đang start cho user thì ntn ạ ???」— kết quả thực thi **Cần Confirm**, ghi chú "
     "duy nhất 1 chữ 「xóa luôn」. **Không có kết quả mong đợi chi tiết.**",
     "`feature-spec.md` §7 mục 6 (BR-06): 「Khi xóa filter_manager → cascade xóa toàn bộ steps **và pending queue** của "
     "branch đó」.\n"
     "`web/logic-spec.md` `deleteFilterManager`: xoá filter_v2 + filter_manager → xoá step_message có filter_manager_id "
     "→ xoá `scenario_step_time` (status = 0) theo step IDs → với mỗi user follow scenario: cập nhật `is_last_step` "
     "hoặc `is_following = 2` → gọi `countScenario()`.",
     "Spec có mô tả đầy đủ nhưng corpus để『Cần Confirm』từ 2024 tới nay — nghĩa là hành vi này CHƯA TỪNG được verify. "
     "Đây là thao tác làm dừng scenario giữa chừng cho hàng loạt friend, phải có TC.",
     "TC-SCE-144 (Filter phân nhánh 配信対象)",
     "",
     "① Chốt kết quả mong đợi theo spec BR-06 (TC đề xuất đã lấp sẵn).\n"
     "② Chạy thật trên PRODUCTION để verify, đặc biệt phần `is_following = 2` và cập nhật counter.\n"
     "③ Cân nhắc bổ sung cảnh báo trên UI khi xoá filter của scenario đang có friend chạy."],

    ["MT-19", "TRUNG BÌNH", W,
     "3 lối thoát khỏi màn filter cho 3 hành vi KHÁC nhau với filter rỗng",
     "r849 (click sang filter khác / add filter mới): hiện alert → OK = **xoá all filter**; Cancel = ở lại.\n"
     "r850 (click back / ステップ配信一覧へ戻る): validate → OK = back và **xoá all filter**.\n"
     "r851 (reset / tự động back / back ở ngoài màn detail): **CHẤP NHẬN filter không có nội dung**.\n"
     "r852: filter rỗng khi start → 「all friend đc send sẽ nhận được msg」.\n"
     "r848 (add filter không nội dung rồi lưu): không lưu DB, ẩn button add step.",
     "`feature-spec.md` §7 mục 6 chỉ mô tả filter phân nhánh nói chung. **Không có rule nào về filter rỗng**: khi nào "
     "được phép tồn tại, khi nào bị xoá, và khi start thì hành xử ra sao.",
     "3 lối thoát khác nhau cho 3 kết quả khác nhau → người dùng không đoán được. Nguy hiểm nhất là nhánh r851-r852: "
     "một filter branch RỖNG khi start sẽ gửi cho TOÀN BỘ friend — đúng ngược lại với ý định『lọc đối tượng』của khách hàng.",
     "TC-SCE-149 (Filter phân nhánh 配信対象)",
     "",
     "① Chốt: filter rỗng có được phép tồn tại không.\n"
     "② Nếu KHÔNG được phép → thống nhất cả 3 lối thoát đều xoá filter rỗng.\n"
     "③ Nếu ĐƯỢC phép → chốt hành vi khi start (gửi all friend hay không gửi ai) và hiển thị cảnh báo rõ trên UI.\n"
     "④ Bổ sung Business Rule mới vào `feature-spec.md` §7."],

    ["MT-20", "TRUNG BÌNH", W,
     "Giới hạn 1 step「ステップ開始直後」tính theo SCENARIO hay theo FILTER?",
     "r433: 「trong **1 ground scenario** chỉ được 1 lần chọn send ngay」.\n"
     "r459: 「không được, **1 ground scenario** chỉ được 1 step send ngay」.\n"
     "r800 (khối ghi chú cuối tab, mới hơn): 「**mỗi filter** cho phép tạo 1 send ngay」.",
     "`feature-spec.md` §7 mục 5 + §9 Validation Rules: không cho phép 2 step trùng "
     "`(delay_type, start_day, start_time, **filter_manager_id**)` → vì send ngay có start_day/start_time = NULL nên "
     "khoá unique này ngụ ý giới hạn theo **FILTER**.\n"
     "`web/logic-spec.md` BR-03 nói tương tự.",
     "Corpus tự mâu thuẫn giữa 2 khối trong cùng 1 tab. Nếu giới hạn theo scenario mà UI cho tạo theo filter (hoặc "
     "ngược lại) thì có nhánh filter không thể có step gửi ngay — mất một kịch bản nghiệp vụ phổ biến (chào mừng "
     "theo nhóm đối tượng).",
     "TC-SCE-158 (配信タイミング — thêm & sửa)",
     "",
     "① Test trên PRODUCTION: tạo step send ngay ở filter default rồi thử tạo tiếp ở filter branch.\n"
     "② Chốt phạm vi giới hạn và ghi rõ vào `feature-spec.md` §7 mục 5 (hiện chỉ suy được gián tiếp qua khoá unique).\n"
     "③ Nếu là theo filter → sửa lại 2 dòng corpus r433/r459 cho khỏi gây hiểu nhầm."],

    ["MT-21", "CAO", W,
     "`delay_type = 2` lưu `start_time` dạng GIỜ:PHÚT hay PHÚT:GIÂY? — spec tự mâu thuẫn",
     "Feature #30571 (03-07-2025), r989-r994 — rất rõ ràng:\n"
     "• nhập 00 giờ 01 phút → `start_time` = **00:01**\n• nhập 23 giờ 59 phút → **23:59**\n"
     "• nhập 24 giờ 00 phút → **24:00**\n• nhập 47 giờ 59 phút → **47:59**\n• nhập 72 giờ → **72:00**\n"
     "→ Đây là GIỜ:PHÚT, và giờ có thể vượt 24.",
     "`feature-spec.md` §6: 「`2` = 経過時間で指定 — Sau N giờ M phút — start_time = **\"HH:MM:00\"** (giờ = N, phút = M)」 ✔\n"
     "`db/db-mapping.md:86` và `:109`: 「hoặc \"HH:MM:00\" biểu thị N giờ M phút」·「vd \"02:30:00\" = sau 2 giờ 30 phút」 ✔\n"
     "NHƯNG `web/logic-spec.md` BR-03: 「delay_type = 2: delay tính theo **phút:giây** (`start_time` dạng **`mm:ss:00`**)」 ✘\n"
     "và bảng trường StepMessage dòng 362: 「delay_type = 2: **`mm:ss:00`**」 ✘\n"
     "và `createScenarioStep` dòng 116: 「`2`: delay theo **phút:giây** (`start_time` dạng `mm:ss:00`)」 ✘",
     "3 chỗ trong `logic-spec.md` nói ngược với `feature-spec.md` + `db-mapping.md` + corpus. Dev đọc logic-spec sẽ "
     "hiểu sai hoàn toàn đơn vị thời gian — chênh lệch 60 lần. Ngoài ra kiểu cột `time` của MySQL chứa được tới "
     "838:59:59 nên 72:00 hợp lệ, càng khẳng định là giờ:phút.",
     "TC-SCE-160 (配信タイミング — thêm & sửa)",
     "",
     "① Query PRODUCTION: `SELECT delay_type, start_time FROM step_message WHERE delay_type = 2 LIMIT 20` để xác nhận.\n"
     "② Sửa 3 chỗ sai trong `web/logic-spec.md`: BR-03, bảng trường StepMessage dòng 362, mô tả `createScenarioStep` dòng 116.\n"
     "③ Rà lại xem có code/query nào đang parse theo mm:ss không."],

    ["MT-22", "CAO", W,
     "Giới hạn tối đa 72 giờ của `経過時間で指定` — spec KHÔNG ghi ở bất kỳ đâu",
     "Feature #30571 [03-07-2025] — 「[Scenario] [Modal add timing gửi tin nhắn] Sửa lại time tối đa có thể setting là **72h**」:\n"
     "• r986: 「update **24 => 72**; 23h59 => **72h00**」\n"
     "• r994: nhập 72 giờ → `start_time` = 72:00, tạo mới **success**\n"
     "• r995: nhập **72 giờ 01 phút** → **báo lỗi**\n"
     "• r996: nhập **73 giờ 00 phút** → **báo lỗi**\n"
     "• r984-r985: đồng thời đổi màu chữ time thành #222222",
     "`feature-spec.md` §9 Validation Rules liệt kê 8 rule — **không có rule nào về giới hạn giờ của delay_type = 2**.\n"
     "§6 chỉ mô tả「Sau N giờ M phút」mà không nêu N tối đa.\n"
     "`db/db-mapping.md`, `ui/ui-spec.md`, `web/api-spec.md` cũng không đề cập.\n"
     "Spec cũng không nhắc giới hạn CŨ là 24h (23:59) trước Feature #30571.",
     "Đây là giới hạn nghiệp vụ có thật, đã release từ 07/2025, ảnh hưởng trực tiếp tới cách khách hàng thiết kế "
     "chuỗi tin. Spec được viết 05/2026 mà vẫn thiếu → người đọc spec sẽ tưởng nhập bao nhiêu giờ cũng được.",
     "TC-SCE-163, TC-SCE-164 (配信タイミング — thêm & sửa)",
     "",
     "① Xác nhận giới hạn 72h còn hiệu lực trên bản hiện tại.\n"
     "② Bổ sung rule vào `feature-spec.md` §9 Validation Rules + §6 (bảng delay_type), kèm nội dung message lỗi thật.\n"
     "③ Ghi lại lịch sử thay đổi 24h → 72h (Feature #30571) để tránh hiểu nhầm với data cũ.\n"
     "④ Kiểm tra data cũ tạo trước 07/2025 có giá trị nào > 72h không."],

    ["MT-23", "TRUNG BÌNH", W,
     "Edit time chưa lưu → thêm message làm MẤT time vừa chọn (tuỳ cách thêm)",
     "r801: 「edit time sau đấy thêm msg dạng **template dùng luôn** => time vừa chọn chưa lưu sẽ **KHÔNG bị mất** "
     "(nếu add msg **template clone**, **tạo msg** thì sẽ **mất** time vừa chọn/vừa thêm)」.",
     "Không có mục nào trong spec mô tả trạng thái form khi chuyển sang màn thêm message giữa chừng.",
     "3 cách thêm message cho 2 hành vi khác nhau với dữ liệu chưa lưu. Người dùng chọn time rồi thêm message, quay "
     "lại thấy time đã về giá trị cũ mà không có cảnh báo → gửi tin sai thời điểm. Nguyên nhân có thể do 2 cách "
     "(clone / tạo mới) redirect sang trang khác làm mất state, còn dùng thẳng thì xử lý bằng AJAX.",
     "TC-SCE-171 (配信タイミング — thêm & sửa)",
     "",
     "① Chốt hành vi mong muốn: giữ state time chưa lưu ở cả 3 cách, hoặc cảnh báo trước khi rời trang.\n"
     "② Nếu chọn giữ state → raise task cải tiến.\n"
     "③ Bổ sung mô tả vào `ui/ui-spec.md` về luồng thêm message từ màn edit step."],

    ["MT-24", "CAO", W,
     "Copy step TRÙNG TIME: spec cấm trùng nhưng corpus nói GỘP — và còn GHI ĐÈ tên step + profile",
     "r60: 「trùng time step có sẵn → **gộp vào cùng 1 step**」.\n"
     "r799: 「copy trùng time => copy message của step kia vào step nhận」.\n"
     "r735: 「nếu trùng time với step đang có trong filter thì **copy message vào step đang có**」.\n"
     "r808 (khối『design mới』): 「nếu trùng time thì add msg, và action vào step đang có, **copy cả tên step, cả profile "
     "(ghi đè tên và profile nếu trước đó đã có)**」.",
     "`feature-spec.md` §7 mục 5: 「**Không cho phép** 2 steps trùng cùng `(delay_type, start_day, start_time, "
     "filter_manager_id)`」.\n"
     "§9 Validation Rules: 「Step timing — Không trùng — 「設定した時間に配信するメッセージが既に存在しています。」」.\n"
     "`web/logic-spec.md` `createScenarioStep` cũng nêu rule chặn trùng.\n"
     "**Spec KHÔNG nêu ngoại lệ cho luồng COPY**, và hoàn toàn không nhắc việc ghi đè tên step / profile.",
     "Rule『cấm trùng』và hành vi『gộp khi copy』là 2 quy tắc trái ngược cho cùng một ràng buộc dữ liệu. Nghiêm trọng "
     "hơn: việc GHI ĐÈ tên step và profile của step đích là MẤT DỮ LIỆU im lặng — khách hàng copy step từ nhánh khác "
     "sang thì tên và người gửi đã cấu hình ở nhánh đích bị thay mà không có cảnh báo nào.",
     "TC-SCE-172, TC-SCE-248 (配信タイミング — thêm & sửa · 一括操作)",
     "",
     "① Xác nhận trên PRODUCTION: copy step trùng time có ghi đè tên và profile thật không.\n"
     "② Chốt hành vi mong muốn — nếu ghi đè là cố ý thì phải có confirm dialog nêu rõ sẽ mất tên/profile hiện tại.\n"
     "③ Bổ sung ngoại lệ COPY vào `feature-spec.md` §7 mục 5 và §9 Validation Rules.\n"
     "④ Rà cả 3 luồng copy (copy message&action, 一括引用登録, copy step giữa filter) xem có cùng hành vi không."],

    ["MT-25", "TRUNG BÌNH", W,
     "Mở modal edit time, KHÔNG sửa gì, bấm save → vẫn update `is_new` và job vẫn chạy tính lại",
     "「Job scenario」r169 và r181: kết quả mong đợi 「**Không update** step message, không hiện alert, **Không tính "
     "toán lại** time gửi」nhưng ghi chú kết quả thực thi: 「Hiện tại vẫn đang **update is_new = 2 và job CÓ chạy để "
     "tính toán lại**」.",
     "`db/db-mapping.md:100` mô tả `step_message.is_new` (1 = mới, 2 = đã update — dùng cho sync) và `:482` "
     "(「`is_new`, `update_timestamp` — Dùng cho sync với Spring Boot」). **Không có rule nào về việc khi nào được "
     "phép set is_new.**",
     "Save không thay đổi gì vẫn kích hoạt job tính lại `send_time` cho TOÀN BỘ friend đang chạy scenario → tốn tài "
     "nguyên vô ích, và tệ hơn: nếu logic tính lại có sai lệch thì thao tác vô hại của user cũng làm lệch lịch gửi "
     "của khách. Liên quan trực tiếp tới MT-04 (cửa sổ 5 phút).",
     "TC-SCE-177 (配信タイミング — thêm & sửa)",
     "",
     "① Xác nhận còn tái hiện không.\n"
     "② Nếu còn → raise bug: chỉ set `is_new = 2` khi giá trị time thực sự thay đổi.\n"
     "③ Bổ sung rule『điều kiện set is_new』vào `db/db-mapping.md` hoặc `web/logic-spec.md`."],

    ["MT-26", "TRUNG BÌNH", W,
     "Bug KH #36365: 2 nội dung message lỗi khác nhau cho cùng 1 tình huống",
     "r964 (mô tả cách fix của dev): 「nếu không thì báo lỗi **「フィルターが削除されたため、画面を再読み込みしてください」**」.\n"
     "r966-r971 (kết quả mong đợi của TC): 「hiển thị msg: **「絞り込み条件が削除されたため、画面を再読み込みしてください」**」.\n"
     "r977 (copy step của filter đã xoá): 「**「選択したステップが削除されたため、画面を再読み込みしてください」**」.",
     "`feature-spec.md` §9 Validation Rules **không có rule nào** về việc filter_manager bị xoá khi đang tạo/sửa step. "
     "Toàn bộ nhóm message lỗi này không xuất hiện trong spec.",
     "Trong cùng 1 ticket có 2 text lỗi khác nhau cho cùng 1 tình huống — không rõ text nào đang chạy thật. Với UI "
     "tiếng Nhật, 「フィルター」và「絞り込み条件」là 2 thuật ngữ khác nhau, khách hàng đọc sẽ hiểu khác nhau. "
     "Ngoài ra rule mới này (validate filter tồn tại) hoàn toàn thiếu trong spec.",
     "TC-SCE-178 (配信タイミング — thêm & sửa)",
     "",
     "① Kiểm tra text thật trên PRODUCTION cho cả 3 tình huống (tạo step, edit step, copy step).\n"
     "② Chốt thuật ngữ thống nhất (「絞り込み条件」đang dùng ở UI hay「フィルター」).\n"
     "③ Bổ sung 3 rule validate mới + 3 message vào `feature-spec.md` §9 Validation Rules.\n"
     "④ Bổ sung mô tả `createScenarioStep` check filter tồn tại vào `web/logic-spec.md`."],

    ["MT-27", "TRUNG BÌNH", W,
     "Sort message trong step đang lỗi",
     "r356 (khối edit nội dung scenario): 「sort message」→ kết quả thực thi **NG**.\n"
     "Đối chiếu: r495-r499 (sort message bằng nút 一番上/一番下 ở màn step) đều OK.",
     "`web/logic-spec.md` `saveSortStepMessage`: 「Update `step_message.template_ids` (chuỗi IDs mới đã sort)」. "
     "Không mô tả có mấy đường sort message.",
     "Thứ tự message quyết định thứ tự khách hàng cuối nhận tin — sort sai là gửi sai kịch bản. Có 2 đường sort "
     "(nút 一番上/一番下 ở màn step, và sort ở màn edit scenario) mà chỉ 1 đường được test OK.",
     "TC-SCE-197 (Message trong step)",
     "",
     "① Xác định rõ『sort message』ở r356 là đường nào (màn edit scenario hay drag&drop).\n"
     "② Test lại cả 2 đường sort trên PRODUCTION.\n"
     "③ Nếu còn NG → raise bug.\n"
     "④ Bổ sung mô tả các đường sort message vào `ui/ui-spec.md`."],

    ["MT-28", "TRUNG BÌNH", W,
     "Xoá template group ở màn Template → `step_message.template_ids` chưa xoá id ngay",
     "「Improve update msg scenario」r16: kết quả mong đợi 「1. tbl step_message => **xóa id template đó** trong cột "
     "template_ids + update timestamp; 2. tbl mapping xóa bản ghi của template id tương ứng」\n"
     "nhưng ghi chú kết quả thực thi: 「trong tbl step_message **chưa xóa id template đó đi** => sau 1 time Tùng sẽ "
     "check bên step_message id có template ids nào thì sẽ insert tương ứng」.",
     "`feature-spec.md` §7 mục 3 mô tả `template_ids` là CSV và templates của step có `category_id = -111`.\n"
     "`web/logic-spec.md` `deleteStepMessage` mô tả xoá template TỪ PHÍA STEP. **Không mô tả chiều ngược lại**: "
     "xoá template ở màn Template thì `step_message.template_ids` được dọn thế nào.",
     "`template_ids` còn giữ id template đã bị xoá → id mồ côi. Khi job build message có thể lỗi hoặc bỏ qua im lặng, "
     "khách hàng mất một tin trong chuỗi mà không có cảnh báo. Ghi chú cho thấy đang xử lý bằng job dọn dẹp chạy sau "
     "chứ không xoá đồng bộ.",
     "TC-SCE-209 (Template từ thư viện)",
     "",
     "① Xác nhận cơ chế hiện tại: xoá đồng bộ hay có job dọn dẹp chạy sau (và chu kỳ bao lâu).\n"
     "② Chốt hành vi trong khoảng thời gian id còn mồ côi: job gửi tin xử lý thế nào.\n"
     "③ Bổ sung vào `feature-spec.md` §7 mục 3 và `db/db-mapping.md` mô tả vòng đời `template_ids` khi template bị xoá."],

    ["MT-29", "TRUNG BÌNH", W,
     "Edit action TỪ TRONG màn preview → không ghi nhận thông tin vừa sửa",
     "r641: 「edit action từ preview」→ kết quả OK nhưng ghi chú 「**đang không ghi nhận thông tin vừa edit**」.\n"
     "r677: cùng nội dung, cùng ghi chú.\n"
     "(2 dòng ở 2 popup preview khác nhau — preview step và preview trong popup copy.)",
     "`feature-spec.md` không mô tả chức năng edit action trực tiếp từ màn preview. "
     "`web/logic-spec.md` `previewScenarioMessage` chỉ mô tả là màn xem trước.",
     "Người dùng sửa action trong preview, thấy popup đóng bình thường, tưởng đã lưu — nhưng thực tế không lưu. "
     "Mất thao tác im lặng, không có thông báo lỗi. Xuất hiện ở 2 popup khác nhau nên nhiều khả năng là lỗi chung "
     "của component preview.",
     "TC-SCE-246 (一括操作)",
     "",
     "① Xác nhận còn tái hiện không, ở cả 2 popup.\n"
     "② Nếu còn → raise bug; nếu edit từ preview không phải chức năng chính thức thì ẨN nút edit đi.\n"
     "③ Bổ sung mô tả phạm vi thao tác được phép trong màn preview vào `ui/ui-spec.md`."],

    ["MT-30", "TRUNG BÌNH", W,
     "Xoá step / 一括消去 khi scenario đang chạy: `scenario_step_time` bị XOÁ hay CÒN nhưng không gửi?",
     "r69 (khối『Check data cũ』): 「step đã start cho user → **vẫn còn data trong tbl: scenario_step_time nhưng sẽ ko "
     "send cho user**」.\n"
     "r773 (一括消去 khi scenario đang start): chỉ đánh OK, **không có kết quả mong đợi**.\n"
     "r826: 「xóa step trong quá trình start → Bảng: scenario_step_time **cột status = 0**」— mô tả trạng thái chứ "
     "không nói xoá.",
     "`web/logic-spec.md` `deleteScenarioStep`: 「Xoá `scenario_step_time` (**status = 0**) của step」.\n"
     "`deleteFilterManager`: 「Xoá `scenario_step_time` (status = 0) theo step IDs」.\n"
     "`feature-spec.md` §7 mục 6: 「cascade xóa toàn bộ steps **và pending queue** của branch đó」.\n"
     "→ Spec nói XOÁ; corpus (khối data cũ) nói CÒN.",
     "Nếu bản ghi còn mà không gửi thì hàng đợi tích luỹ rác; nếu bị xoá thì phải chắc chắn cập nhật `is_last_step` "
     "cho step còn lại (nếu không friend kẹt vĩnh viễn ở trạng thái 購読中). Corpus khối data cũ có thể mô tả cơ chế "
     "CŨ trước khi đổi sang xoá — cần xác định corpus nào còn hiệu lực.",
     "TC-SCE-253 (一括操作)",
     "",
     "① Query PRODUCTION sau khi xoá step của scenario đang chạy để xác định bản ghi còn hay mất.\n"
     "② Nếu spec đúng (xoá) → đánh dấu r69 là mô tả cơ chế cũ, loại khỏi phạm vi.\n"
     "③ Nếu corpus đúng (còn) → sửa `web/logic-spec.md` và `feature-spec.md` §7 mục 6.\n"
     "④ Dù chọn hướng nào cũng phải verify `is_last_step` được cập nhật đúng cho step còn lại."],

    ["MT-31", "CAO", W,
     "Send test option 2「全てのメッセージを同時に送信」: tạo HẾT bản ghi cùng lúc hay tạo TỪNG bản ghi nối tiếp?",
     "CORPUS CŨ (2024-2025):\n"
     "• r780: 「sent_time của **tất cả** step_message_id sẽ giống nhau = thời điểm click send」\n"
     "• r816: 「**send hết step cùng lúc**」\n"
     "• r57: 「các record step hiển thị theo time hiện tại (is_last_step = 2 hết)」\n"
     "CORPUS MỚI — Bug KH #34489 (21-02-2026),「Job scenario」:\n"
     "• r242: 「Bảng scenario_step_time **chỉ tạo 1 record** cho step có send_time nhỏ nhất, **is_last_step = 3**」\n"
     "• r253: 「sau khi send xong step thì check step có send_time tiếp theo và **add vào bảng scenario_step_time**: "
     "send_time = time hiện tại, is_last_step = 3」",
     "`job/job-spec.md` dòng 28 và BR-4: 「is_last_step: 0 = bình thường, 1 = bước cuối, **2 = test step, 3 = test all**」 "
     "và 「Với `TEST_STEP_MESSAGE_ALL` → **tự động chuyển sang step tiếp theo** (`nextStepMessageSentTestScenario`)」 "
     "→ khớp với corpus MỚI.\n"
     "`feature-spec.md` §6 bảng `scenario_step_time.status` chỉ có giá trị `0`; **không mô tả is_last_step = 2 / 3** ở "
     "phía Laravel.",
     "Đây là thay đổi cơ chế do fix bug thứ tự gửi (multi-thread làm đảo thứ tự message). Corpus cũ mô tả cơ chế đã bị "
     "thay thế. Nếu tester dùng TC cũ sẽ kết luận sai là bug. Đã áp bản MỚI theo quy tắc ưu tiên TC mới nhất — "
     "**cần Leader xác nhận** vì khoảng cách niên đại lớn và corpus cũ nằm ở tab master.",
     "TC-SCE-282 (Send test 一括テスト)",
     "",
     "① Xác nhận cơ chế hiện tại trên PRODUCTION: query `scenario_step_time` ngay sau khi nhấn send test option 2.\n"
     "② Đánh dấu r780/r816/r57 là mô tả cơ chế CŨ (trước Bug KH #34489) — đã loại khỏi kho.\n"
     "③ Bổ sung `is_last_step` = 2 / 3 vào `feature-spec.md` §6 (hiện chỉ có ở job-spec).\n"
     "④ Bổ sung mô tả luồng send test 3 option vào `feature-spec.md` §3 (SCR-SCE-02/03)."],

    ["MT-32", "TRUNG BÌNH", W,
     "Send test option 3「20~30秒ごとに」— corpus ghi『Chưa thấy random』",
     "r782: kết quả mong đợi 「step đầu tiên sẽ send luôn, các step sau sẽ **random 20-30 s**」nhưng ghi chú kết quả "
     "thực thi: 「**Chưa thấy random**」.\n"
     "Đối chiếu: 「Job scenario」r241 (Bug KH #34489, 03/2026) mô tả rõ ví dụ 18:00:00 → 18:00:20 → ... (cách nhau "
     "20-30s) và đánh OK.",
     "Không mục nào trong spec mô tả 3 option của chức năng send test all, cũng không mô tả khoảng random 20-30 giây.",
     "Nếu không random thật mà gửi liên tục thì có nguy cơ đụng rate limit của LINE API khi test scenario nhiều step. "
     "2 lần test ở 2 thời điểm cho kết quả khác nhau → chưa rõ đã fix hay chưa.",
     "TC-SCE-285 (Send test 一括テスト)",
     "",
     "① Test lại trên PRODUCTION, đo khoảng cách thực tế giữa các message.\n"
     "② Nếu vẫn không random → raise bug hoặc chốt bỏ yêu cầu random.\n"
     "③ Bổ sung mô tả 3 option send test + khoảng random vào `feature-spec.md` §3 và `job/job-spec.md`."],

    ["MT-33", "TRUNG BÌNH", W,
     "Điều kiện hiển thị next scenario tính theo TỪNG FILTER hay theo TOÀN SCENARIO?",
     "r833-r839 (kết quả mong đợi): 「hiển thị phần next sce (**chỉ hiển thị ở filter default**)」với điều kiện tối "
     "thiểu 2 step gồm (send ngay HOẶC 経過時間) VÀ 日時で指定.\n"
     "r834 (kết quả thực thi): 「**filter default step duration + filter1 step send sau ngày giờ > không hiển thị next "
     "sce**」— tức là khi 2 loại step nằm ở 2 filter KHÁC nhau thì không hiển thị, trái với kết quả mong đợi cùng dòng.",
     "`feature-spec.md` §12 mục 6 (Gaps): 「**`afterScenarioId1..5` UI**: Các cột này có UI để configure không, hay chỉ "
     "qua API/DB trực tiếp?」— spec TỰ NHẬN không biết có UI hay không.\n"
     "§7 mục 12 chỉ mô tả phía job: sau bước cuối kiểm tra afterScenarioId1-5 và date range.",
     "Spec bỏ trống hoàn toàn phần UI của next scenario, trong khi corpus có 14 dòng TC mô tả điều kiện hiển thị khá "
     "phức tạp. Quy tắc『2 loại step』nếu tính theo filter thì khách phải tự nhớ, còn tính theo scenario thì UI đang sai. "
     "**TC lấp được Gap #6 của spec.**",
     "TC-SCE-295 (Next scenario)",
     "",
     "① Chốt: điều kiện tính theo filter hay theo toàn scenario.\n"
     "② Nếu theo scenario → raise bug cho case r834.\n"
     "③ **Đóng Gap #6** trong `feature-spec.md` §12: bổ sung mô tả UI next scenario vào §3 (SCR-SCE-02/03) và §7 "
     "một Business Rule về điều kiện hiển thị.\n"
     "④ Làm rõ vì sao chỉ hiển thị ở filter default."],

    ["MT-34", "TRUNG BÌNH", W,
     "Nhiều step `日時で指定` cùng day = 0: TẤT CẢ cùng dịch sang ngày mai hay chỉ step quá giờ mới dịch?",
     "「Job scenario」r25-r27 (next scenario): 「scen B có nhiều step message delay_type = 0 và setting day = 0 → "
     "Check theo step có **time send nhỏ nhất**: giờ < hoặc = giờ hiện tại → **tất cả step day 0 next sang ngày hôm sau**」.\n"
     "r22-r24: 「step day 0 next sang ngày hôm sau → **các step khác cũng next theo** (VD step day = 1 sẽ send sau step "
     "day = 0 1 ngày)」.\n"
     "NGƯỢC LẠI r1026-r1027 và r797 (start bình thường): 「case quá giờ chuyển sang ngày hôm sau... **các step 0 ngày "
     "giờ tương lai trong ngày thì cũng tính sang ngày hôm sau**」— mô tả gần giống nhưng không nói『xét theo step nhỏ nhất』.",
     "`feature-spec.md` §6 chỉ mô tả delay_type = 0 là「N ngày sau khi subscribe, lúc HH:MM」. "
     "**Không có rule nào về việc xử lý khi giờ đã qua**, cũng không nói phạm vi dịch (chỉ step đó hay tất cả step).",
     "Đây là quy tắc tính lịch gửi cốt lõi, ảnh hưởng tới toàn bộ chuỗi tin của khách hàng. Nếu dịch nhầm phạm vi thì "
     "cả chuỗi lệch 1 ngày. Corpus mô tả 2 cách hơi khác nhau cho 2 ngữ cảnh (next scenario vs start bình thường) — "
     "không rõ có thật sự khác nhau hay chỉ là cách diễn đạt.",
     "TC-SCE-305 (Next scenario)",
     "",
     "① Chốt quy tắc: dịch theo step nhỏ nhất (kéo cả cụm) hay dịch riêng từng step quá giờ.\n"
     "② Xác nhận quy tắc có giống nhau giữa start bình thường và next scenario không.\n"
     "③ Bổ sung Business Rule mới vào `feature-spec.md` §7 với ví dụ số cụ thể (spec hiện KHÔNG có mục này).\n"
     "④ Bổ sung mô tả tính send_time vào `job/job-spec.md`."],

    ["MT-35", "TRUNG BÌNH", W,
     "Đổi next scenario khi scenario đang chạy → friend không nhận đủ message của scenario mới",
     "r830: 「trong quá trình start sce 1 **thay đổi sce next**」→ ghi chú kết quả thực thi: 「**db hiển thị status = 2 "
     "nhưng friend không nhận đủ msg**」.",
     "`feature-spec.md` §7 mục 12 mô tả job kiểm tra `afterScenarioId1..5` tại thời điểm gửi bước cuối. "
     "Không mô tả điều gì xảy ra nếu giá trị này bị đổi TRONG LÚC scenario đang chạy.",
     "DB ghi nhận đã chuyển scenario (status = 2) nhưng khách hàng cuối không nhận đủ tin → mất tin im lặng, "
     "không có log lỗi. Đây là thao tác bình thường của khách (đổi kịch bản tiếp theo giữa chừng chiến dịch).",
     "TC-SCE-309 (Next scenario)",
     "",
     "① Test lại trên PRODUCTION, đếm chính xác số message friend nhận được của scenario mới.\n"
     "② Nếu còn thiếu → raise bug, kiểm tra thời điểm job đọc `after_scenario_id_1` (đọc lúc start hay lúc gửi bước cuối).\n"
     "③ Bổ sung vào `feature-spec.md` §7 mục 12 mô tả thời điểm giá trị next scenario được đọc."],

    ["MT-36", "CAO", W,
     "『Trong ngày không update』— quy tắc do a Tư chốt, không có trong spec, mâu thuẫn với hành vi mong đợi",
     "r798: 「**anh Tư chốt: Trong ngày không update các TH** — Scenario đang start: Add thêm step msg tương lai; "
     "edit time của step từ ngày giờ sang send sau bn phút」.\n"
     "r832: 「đang start edit msg, time, filter」→ ghi chú kết quả thực thi: 「**edit time trong ngày không được cập "
     "nhật (từ 15p xuống 7p)**」.\n"
     "ĐỐI CHIẾU: r448/r456/r461 lại mô tả chi tiết hành vi khi edit time step của scenario đang chạy (case 1/2/3, "
     "vị trí step thay đổi, có được send hay không) — tức là CÓ update.",
     "Không có mục nào trong `feature-spec.md` / `web/logic-spec.md` / `job/job-spec.md` mô tả quy tắc『trong ngày "
     "không update』.\n"
     "Ngược lại `web/logic-spec.md` mô tả `createScenarioStep` luôn reorder và job luôn tính lại send_time.",
     "Đây là quyết định nghiệp vụ (do a Tư chốt) hạn chế khả năng sửa scenario đang chạy — nhưng không nằm ở đâu "
     "ngoài 1 dòng ghi chú trong sheet. Người dùng và tester mới sẽ coi đây là bug. Đồng thời mâu thuẫn với nhóm TC "
     "r448-r464 vốn mô tả rất chi tiết hành vi khi edit time step đang chạy.",
     "TC-SCE-311 (Next scenario)",
     "",
     "① Xác nhận quy tắc『trong ngày không update』còn hiệu lực không, phạm vi áp dụng chính xác là gì.\n"
     "② Nếu còn hiệu lực → bổ sung thành Business Rule chính thức trong `feature-spec.md` §7 và hiển thị cảnh báo trên UI.\n"
     "③ Nếu không còn → xoá khỏi corpus và test lại toàn bộ nhóm TC r448-r464.\n"
     "④ Làm rõ quan hệ giữa quy tắc này và cửa sổ 5 phút của job (MT-04)."],

    ["MT-37", "CAO", W,
     "Counter phía JOB lệch phía WEB ở ít nhất 3 điểm",
     "「Improve count scenario + tag」— khối『Check start/stop scenario cho user bởi job』:\n"
     "• r30 (start lại khi is_following = 1, mong đợi giữ nguyên) → ghi chú 「**Vẫn bị update**」\n"
     "• r33 (stop giữa chừng, mong đợi count_follow −1 count_stop +1) → ghi chú 「**không update**」\n"
     "• r35 (start nhưng không còn message thoả mãn, mong đợi count_follow giữ nguyên) → ghi chú 「**đang bị cộng "
     "count_follow**」\n"
     "Cùng các case đó ở phía WEB (r16, r19, r21) đều OK.",
     "`web/logic-spec.md` BR-10: 「Hàm `countScenario($scenarioId)` được gọi sau các thao tác ảnh hưởng đến danh sách "
     "users」— mô tả như thể chỉ có MỘT cơ chế đếm.\n"
     "`job/job-spec.md` BR-5 nhắc `decreaseFollowIncreaseStopCount(scenarioId)` ở phía job. "
     "**Spec không nói 2 phía dùng 2 hàm khác nhau và có thể lệch.**",
     "Web và job dùng 2 code path đếm khác nhau → cùng một nghiệp vụ cho 2 kết quả khác nhau. Vì đa số action thực tế "
     "của khách hàng đi qua JOB (autoreply, tag, button, kết bạn), số liệu hiển thị cho khách hàng nhiều khả năng "
     "đang SAI. 3 điểm lệch được ghi nhận từ 12/2023 mà chưa rõ đã fix chưa.",
     "TC-SCE-325 (Bộ đếm friend)",
     "",
     "① Test lại toàn bộ 10 case counter phía job trên PRODUCTION và đối chiếu từng case với phía web.\n"
     "② Với mỗi điểm lệch còn tồn tại → raise bug.\n"
     "③ Chốt: hợp nhất về 1 hàm `countScenario()` dùng chung cho cả web và job.\n"
     "④ Bổ sung vào `web/logic-spec.md` BR-10 và `job/job-spec.md` mô tả rõ cơ chế đếm ở từng phía."],

    ["MT-38", "TRUNG BÌNH", W,
     "Nhóm TC edit step khi scenario đang chạy PHẢI bật『job web』thủ công mới test được",
     "「Job scenario」r72: 「case edit các step msg sau khi start scenario **(RIÊNG CÁC CASE EDIT NÀY PHẢI BÁO WEB BẬT JOB)**」.\n"
     "Nhiều dòng trong nhóm này để kết quả **Pending** (r77, r78, r92, r94-r104) — chưa test xong.",
     "`feature-spec.md` §10 nêu feature flag 「`ENABLE_SCENARIO = true` (config.properties)」cho job scenario. "
     "**Không có mục nào mô tả một『job web』riêng cần bật thủ công**, cũng không mô tả job này khác `NewScenarioTaskV3` ở đâu.",
     "Một nhánh chức năng quan trọng (tính lại lịch gửi khi khách sửa scenario đang chạy) phụ thuộc vào một job phải "
     "bật thủ công — nghĩa là trên môi trường test mặc định nó KHÔNG chạy, và nhiều TC đã bị bỏ dở ở trạng thái Pending. "
     "Rủi ro: hành vi trên PRODUCTION khác hẳn kết quả test.",
     "TC-SCE-347 (Job gửi step & is_last_step)",
     "",
     "① Xác nhận『job web』là job nào, tên chính xác, trên PRODUCTION có luôn bật không.\n"
     "② Bổ sung vào `job/job-spec.md` mô tả job này (chu kỳ, điều kiện kích hoạt, quan hệ với `step_message.is_new`).\n"
     "③ Bổ sung vào `framework/catalog-lme.md` mục D/D2 (khác biệt môi trường) để tester biết phải bật trước khi test.\n"
     "④ Chạy nốt các case đang Pending."],

    ["MT-39", "THẤP", W,
     "Trigger scenario trên chat 1:1 hiển thị 管理名 =「-」— thiếu dữ liệu hay cố ý?",
     "r1030: 「Start scenario từ Modal multi action (chat 1:1) → Title: このステップの開始トリガー / 機能名: 手動操作 / "
     "**管理名: -**」và ghi chú: 「**trên step cũng hiển thị tên quản lý là -**」.\n"
     "Các nguồn khác có 管理名 thật: click button → tên button; quét QR → tên landing; tap richmenu → tên richmenu.",
     "Không có mục nào trong spec mô tả nội dung block trigger hiển thị trên chat 1:1.",
     "Với các nguồn『手動操作』(thao tác thủ công từ chat 1:1 / right bar / my page) thì không có đối tượng để đặt tên "
     "nên「-」có thể là cố ý. Nhưng ghi chú của tester cho thấy đang nghi ngờ. Ảnh hưởng tới khả năng truy vết: khách "
     "hàng nhìn lịch sử không biết ai/thao tác nào đã start scenario.",
     "TC-SCE-353 (Job gửi step & is_last_step)",
     "",
     "① Chốt:「-」là cố ý cho nhóm 手動操作 hay là thiếu dữ liệu (nên hiển thị tên nhân viên thao tác).\n"
     "② Đối chiếu với nhóm start-từ-giữa (r1041) — nhóm đó có 詳細「テスト：<tên user thao tác>」.\n"
     "③ Bổ sung bảng nội dung trigger (機能名 / 管理名 / 詳細 theo từng nguồn) vào `feature-spec.md` §3 hoặc `ui/ui-spec.md` "
     "— hiện spec hoàn toàn không có."],

    ["MT-40", "CAO", W,
     "Edit step ĐÃ GỬI cho user, thoả mãn giờ gửi → CÓ thêm bản ghi `scenario_step_time` hay KHÔNG?",
     "MÂU THUẪN NGAY TRONG CÙNG TAB「Testcase」:\n"
     "• r908 và r938: 「Bot A: Bảng scenario_step_time: **Thêm bản ghi** cho step vừa edit」\n"
     "• r920 và r929: 「Bảng scenario_step_time: Thêm bản ghi cho step vừa edit **=> Không thêm bản ghi**」— "
     "câu sau phủ định câu trước ngay trong cùng ô\n"
     "• r922, r923, r931, r932: cũng có dòng 「**=> không thêm bản ghi**」nối sau mô tả is_last_message\n"
     "「Job scenario」r142, r177: 「**Thêm bản ghi** cho step vừa edit」(không có phủ định).",
     "`feature-spec.md` §10 mô tả luồng job nhưng không mô tả quy tắc khi Laravel ghi bản ghi mới vào "
     "`scenario_step_time` cho step ĐÃ gửi.\n"
     "`web/logic-spec.md` không có mục nào về `updateScenarioStep`.\n"
     "Corpus r908 còn ghi chú tiêu đề: 「Check logic hiện tại **vẫn tạo thêm** scenario_step_time nếu thỏa mãn giờ」.",
     "Nếu THÊM bản ghi cho step đã gửi thì friend sẽ nhận LẠI message của step đó — gửi trùng cho khách hàng cuối. "
     "Đây chính là họ bug đã từng xảy ra (Bug KH #36365 gửi duplicate). Corpus tự phủ định trong cùng 1 ô cho thấy "
     "spec ban đầu và hành vi thực tế khác nhau, tester sửa tay nhưng không sửa hết.",
     "TC-SCE-368 (Job khi edit step đang chạy)",
     "",
     "① Query PRODUCTION: edit step đã gửi (thoả giờ) rồi kiểm tra `scenario_step_time` có bản ghi mới không, "
     "và friend có nhận lại message không.\n"
     "② Chốt hành vi đúng — theo nghiệp vụ thì KHÔNG nên gửi lại step đã gửi.\n"
     "③ Sửa lại toàn bộ 8 dòng corpus mâu thuẫn (r908-r911, r920-r923, r929-r932, r938-r941).\n"
     "④ Bổ sung mô tả `updateScenarioStep` + quy tắc này vào `web/logic-spec.md` và `feature-spec.md` §7."],

    ["MT-41", "CAO", W,
     "Job scenario và job callback chạy trên 2 SERVER khác nhau → bộ đếm chống lặp đếm riêng",
     "「Job scenario」r40 (ghi chú kết quả thực thi trên môi trường step): 「trên step **job scen và callback đang ở 2 "
     "server khác nhau**, nên đang **count số lần start khác nhau** -> bị limit khi next scen rồi nhưng start từ "
     "[callback] vẫn được」.",
     "`feature-spec.md` §10 mô tả `NewScenarioTaskV3` như MỘT tiến trình (1 scanner + 200 worker) với "
     "`MonitorScenarioManager` đếm số lần lặp. **Không mô tả kiến trúc nhiều server**, không nói bộ đếm là in-memory "
     "hay chia sẻ qua DB/cache.\n"
     "`job/job-spec.md` cũng không đề cập.",
     "Nếu bộ đếm chống lặp là in-memory per-server thì cơ chế chống lặp vô hạn (MT-03) KHÔNG đáng tin: scenario có thể "
     "vượt ngưỡng thật mà mỗi server chỉ thấy một phần. Đây đúng là kịch bản mà cơ chế được sinh ra để ngăn — "
     "vòng lặp A↔B chạy vô hạn, spam khách hàng cuối và đốt quota LINE API.",
     "TC-SCE-404 (Phân quyền & môi trường)",
     "",
     "① Xác nhận với dev: `MonitorScenarioManager` lưu bộ đếm ở đâu (in-memory / Redis / DB) và có mấy instance job "
     "trên PRODUCTION.\n"
     "② Nếu là in-memory per-server → raise bug kiến trúc: chuyển bộ đếm sang store dùng chung.\n"
     "③ Bổ sung mô tả kiến trúc triển khai (số instance, cách chia sẻ state) vào `job/job-spec.md`.\n"
     "④ Bổ sung khác biệt môi trường này vào `framework/catalog-lme.md` mục D/D2."],
]
