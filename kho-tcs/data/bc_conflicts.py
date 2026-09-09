# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ ĐANG CHỜ QUYẾT ĐỊNH của Leader (2026-08-26).

Nguồn TCs: 03. TCsLine_Broadcast (12 tab) + TCsLine_Improve chung (3 tab).
Nguồn spec: spec-features/admin/message-send-all/ (chốt 2026-03-26).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-20", "CAO", W,
     "PHẠM VI — tính năng「配信数上限アラート」(#36436) KHÔNG có trong spec. Phải chốt TRƯỚC vì ảnh hưởng ~28 TC",
     "3 tab của file 03. TCsLine_Broadcast mô tả 1 tính năng HOÀN TOÀN MỚI:\n"
     "•「[AI] alert_limit」(99 TC, format 12 cột) ·「UI Tests 36436」(29 TC) ·「API Tests 36436」(29 TC)\n"
     "• Modal「配信数上限アラート」5 biến thể V1→V5 hiện khi 配信対象 vượt quota LINE OA hoặc エルメ\n"
     "• 3 nút:「配信対象を見直す」·「下書き保存する」·「このまま登録する」+ 2 nút upgrade\n"
     "• 2 endpoint mới: kiểm tra quota (quota-check) trước khi đăng ký, và đăng ký có status draft/wait_to_send\n"
     "• Công thức: 配信可能数 = 月間上限 − 配信済み · 超過 = max(0, 今回の配信予定数 − 配信可能数)",
     "feature-spec.md — KHÔNG nhắc tới modal alert nào. §6 liệt kê 40 endpoint EP-01→EP-40, KHÔNG có "
     "endpoint quota-check. §5 BR-10 chỉ nói『Free plan: tối đa 1,000 tin/tháng』và『hết quota LINE plan → "
     "ghi MessageError code REACH_LIMIT_LINE, không retry』— tức xử lý ở JOB, KHÔNG có cảnh báo trước ở UI.\n"
     "ui-spec.md:59 — header hiển thị 配信数 và link「詳細を見る」, không có modal cảnh báo.\n"
     "Spec chốt 2026-03-26; ticket #36436 phát sinh sau đó.",
     "Nếu #36436 ĐÃ release thì spec thiếu hẳn 1 màn (modal) + 1 endpoint + toàn bộ business rule về "
     "cảnh báo quota, và ~28 TC nhóm『配信数上限アラート』phải chạy ngay. Nếu CHƯA release thì 28 TC đó "
     "chưa giao được cho member và phải đánh dấu là chờ. Không thể tự đoán vì spec không có bất kỳ dấu vết nào.",
     "Toàn bộ nhóm「配信数上限アラート — trigger & modal」·「— nút thao tác」·「— quota & job cắt vượt」",
     "",
     "Chốt xong phải: ① xác nhận #36436 đã release lên production chưa; ② bổ sung màn SCR-BC-06 (modal) "
     "vào ui-spec.md; ③ bổ sung 2 endpoint vào api-spec.md; ④ bổ sung BR về công thức quota vào feature-spec.md §5."],

    ["MT-03", "CAO", W,
     "TRẠNG THÁI broadcast mới tạo — 'draft' hay 'unregistered'? Và 'unregistered' hiện ở tab nào?",
     "Tab master r17, r394: 『check status khi tạo broadcast success / không msg → unregistered』\n"
     "Tab master r24: 『không có message vẫn đang lưu được (chưa fix)』— tức TC kỳ vọng KHÔNG cho lưu\n"
     "Tab master r62: 『メッセージ登録 → validate trường bắt buộc』, kết quả ghi『chưa validate』\n"
     "file 03/tab function r110-r111: 『không có template, action → hiển thị ở drap; có template/action → "
     "hiển thị ở tab chờ send』",
     "feature-spec.md §5 BR-01: 『Broadcast V2 bắt đầu với `draft` khi tạo mới』\n"
     "feature-spec.md §2 bước 4: 『Tạo broadcast với status='draft'』\n"
     "logic-spec.md:27: 『**create**: Tạo broadcast mới với `status = 'unregistered'`』← NGƯỢC với feature-spec\n"
     "logic-spec.md:182: 『Tạo mới luôn bắt đầu với `status = 'draft'`』\n"
     "logic-spec.md:87: tab 下書き = status IN ('draft','unregistered','not_delivery')\n"
     "db-mapping.md:223: `unregistered` → Tab UI = '-' , UI Display JP = '(không hiển thị)' ← NGƯỢC lại",
     "Spec TỰ MÂU THUẪN 2 chỗ: (a) logic-spec:27 nói create → 'unregistered' còn logic-spec:182 và "
     "feature-spec §5 nói → 'draft'; (b) logic-spec:87 xếp 'unregistered' vào tab 下書き còn db-mapping:223 "
     "nói '(không hiển thị)'. Tester không biết bản ghi chưa có tin nhắn phải nằm ở tab nào, và có được "
     "phép lưu hay phải bị validate chặn.",
     "TC nhóm「配信タイミング設定 — gửi ngay/đặt lịch」(broadcast không có tin nhắn) · "
     "「メッセージ登録 — thêm/sửa/xóa」(lưu broadcast không có tin nhắn) · "
     "「Job gửi & vòng đời trạng thái」(vòng đời trạng thái đầy đủ)",
     "",
     "Chốt xong phải: ① sửa logic-spec.md:27 hoặc :182 cho nhất quán; ② sửa db-mapping.md:223 hoặc "
     "logic-spec.md:87 cho nhất quán về tab của 'unregistered'; ③ chốt việc lưu broadcast không có tin nhắn "
     "là hợp lệ hay phải validate chặn (r62 ghi『chưa validate』)."],

    ["MT-17", "CAO", W,
     "CỬA SỔ ĐÓNG BĂNG FILTER trước giờ gửi — 5 phút, 10 phút, hay con số khác?",
     "Improve chung/tab「Improve sendall scenario」:\n"
     "• r11: 『broadcast setting time - update filter / thêm filter trong vòng **10p** trước time send → "
     "vẫn send cho user đó, ko update filter』\n"
     "• r12: 『> **10p** trước time send → update filter, ko send cho user đó』\n"
     "• r3-r8 (cho SCENARIO step): dùng mốc **5p** cho cùng loại hành vi\n"
     "• r17: 『case tạo gần với time send <10p → update filter liên tục』← NGƯỢC với r11\n"
     "• r19-r21 (chặn EDIT filter ở UI): dùng mốc **5p**",
     "job-spec.md:195: 『Mỗi **60 giây** scan broadcasts sắp đến giờ gửi (trong khoảng "
     "`PREPARE_FILTER_BROADCAST_BEFORE` phút tới)』— chỉ ghi TÊN HẰNG SỐ, KHÔNG ghi giá trị.\n"
     "logic-spec.md:491-495 BR-02: rule 5 phút chỉ nói về CHẶN EDIT ở tầng web, KHÔNG nói về đóng băng filter.\n"
     "feature-spec.md §7: 『PrepareFilterTask pre-filter danh sách users trước giờ gửi (mỗi 60s)』— "
     "cũng không ghi cửa sổ.",
     "Đây là 2 cơ chế KHÁC NHAU dễ bị lẫn: (a) rule 5 phút CHẶN EDIT ở tầng web; (b) cửa sổ pre-filter "
     "ĐÓNG BĂNG danh sách người nhận ở tầng job. Corpus nói cửa sổ (b) của broadcast là 10 phút, của "
     "scenario step là 5 phút, nhưng r17 lại nói dưới 10 phút filter vẫn update liên tục. "
     "Tester không biết ranh giới thật để dựng TC, và khách hàng có thể gửi nhầm cho nhóm người đã bị gỡ tag.",
     "TC nhóm「Edit broadcast & rule 5 phút」— 4 TC về cửa sổ đóng băng filter và đổi giờ gửi",
     "",
     "Chốt xong phải: ① tra giá trị thật của `PREPARE_FILTER_BROADCAST_BEFORE` trong code job và ghi vào "
     "job-spec.md:195; ② ghi rõ 2 cơ chế (chặn edit vs đóng băng filter) là khác nhau vào feature-spec.md §5; "
     "③ giải thích mâu thuẫn giữa r11 và r17."],

    ["MT-13", "CAO", W,
     "配信数 của broadcast ĐÃ GỬI lấy theo send_count hay tính lại theo filter?",
     "Tab master r707-r711 (Bug #31527, 07/2025): 『check count số user đã send … → check count lấy theo "
     "**send_count** bảng broadcast => chỉ sửa ở tab 3 này』— áp cho 5 trường hợp: có filter và có sửa "
     "friend thỏa/không thỏa, không sửa friend, không filter, và copy broadcast.\n"
     "Tab master r714: 『Check count số user đã send ở chat 1:1 → hiển thị count số user đã send theo send_count』\n"
     "NHƯNG tab master r222, r336 (tab 概要 của popup preview): cột kết quả ghi "
     "『test bug: #31527 spect tính count vẫn như cũ (**k count theo send_count**)』",
     "feature-spec.md §4 hàng 7: 『配信数 → broadcast.filter_number, Read, Cập nhật khi nhấn「再計算」』\n"
     "logic-spec.md:94: 『`number_send`: **send_count** nếu delivered, rỗng nếu chưa』\n"
     "db-mapping.md:184: 『Số lượng gửi | 配信数 | broadcast | **send_count / filter_number** | Direct | Cao』"
     "← ghi CẢ HAI, không nói khi nào dùng cái nào",
     "Cùng 1 con số 配信数 nhưng nguồn khác nhau tùy vị trí hiển thị: màn list tab 配信履歴 dùng send_count, "
     "còn tab 概要 trong popup preview lại『vẫn như cũ』(filter_number). Nếu 2 chỗ hiển thị 2 số khác nhau "
     "cho cùng 1 broadcast thì khách hàng sẽ báo bug — chính là bug gốc #31527 "
     "(『Số user đã send hiển thị là 8,871 trên màn hình danh sách, nhưng trong màn hình chi tiết là 6,864 friend』).",
     "TC nhóm「配信数 & danh sách friend đã gửi」— 4 TC về send_count · TC「Preview — 3 tab nội dung」"
     "(tab 概要 hiển thị 配信数)",
     "",
     "Chốt xong phải: ① ghi rõ trong feature-spec.md §4 hàng 7 rằng 配信数 = filter_number khi CHƯA gửi và "
     "= send_count khi ĐÃ gửi; ② chốt tab 概要 của popup preview dùng nguồn nào; ③ sửa db-mapping.md:184 "
     "cho rõ điều kiện."],

    ["MT-01", "TRUNG BÌNH", W,
     "SỐ DÒNG mỗi trang — 50 dòng/trang (TCs) hay dropdown 100/200/500 (spec)?",
     "Tab master r379 (tab 配信予約) và r767 (tab 配信履歴): 『check sl bản ghi trong 1 trang → "
     "**50 bản ghi/1 trang**』\n"
     "Corpus KHÔNG có TC nào cho dropdown「表示件数」.",
     "ui-spec.md:134: 『[Tab 配信履歴] Có thêm: ô tìm kiếm, filter「全期間」, và dropdown「表示件数」"
     "(**100件 / 200件 / 500件**)』\n"
     "ui-spec.md:140: 『Tab「配信履歴」có dropdown chọn số dòng hiển thị (100/200/500), **2 tab kia không thấy**』",
     "Nếu tab 配信履歴 có dropdown 100/200/500 thì con số 50 của corpus sai cho tab đó; nếu chỉ 2 tab kia "
     "cố định 50 thì spec đúng nhưng thiếu con số cho 2 tab đó. Cũng có thể dropdown là tính năng thêm sau "
     "khi corpus được viết. Ảnh hưởng trực tiếp tới TC kiểm phân trang và TC hiệu năng khi nhiều bản ghi.",
     "TC nhóm「Phân trang & số dòng hiển thị」— 2 TC về số dòng/trang và dropdown 表示件数",
     "",
     "Chốt xong phải: ① xác nhận trên production tab nào có dropdown 表示件数; ② ghi số dòng mặc định của "
     "tab 配信予約 và 下書き vào ui-spec.md; ③ nếu dropdown là tính năng mới, ghi ngày release."],

    ["MT-16", "TRUNG BÌNH", W,
     "RULE 5 PHÚT — mốc chặn thật là 5 phút hay 6 phút?",
     "Tab master r262: 『edit filter của bản ghi gần đến giờ send (trước 5 phút) → không cho chỉnh sửa』\n"
     "Improve chung/tab「Improve sendall scenario」r21: 『< 5p → ko cho edit filter, "
     "配信予定日時5分前からは配信内容の編集はできません。』\n"
     "Corpus chỉ test 2 mốc thô: > 5 phút (cho sửa) và < 5 phút (chặn) — KHÔNG đo mốc 6 phút.",
     "feature-spec.md §5 BR-02: 『Broadcast wait_to_send không thể sửa hoặc xoá nếu thời gian gửi - hiện tại "
     "< 5 phút. **Thực tế trong code: buffer 6 phút (`subMinutes(6)`) — UI hiển thị「5分前」**』\n"
     "logic-spec.md:95: 『Code dùng `subMinutes(6)` nhưng UI hiện「5分前」— thực tế buffer thêm 1 phút』\n"
     "feature-spec.md §9 M-01 đã tự ghi nhận đây là mâu thuẫn cần xác nhận.",
     "Khách hàng đọc thông báo「5分前」sẽ tin rằng còn 5 phút 30 giây vẫn sửa được, nhưng thực tế bị chặn "
     "từ 6 phút. Đây là khoảng 1 phút mà người dùng bị chặn không rõ lý do. Tester dựng TC theo con số 5 "
     "sẽ cho kết quả PASS/FAIL không ổn định ở vùng 5-6 phút.",
     "TC nhóm「Edit broadcast & rule 5 phút」— TC đo ranh giới 7/6/5/4 phút và TC chặn sửa dưới 5 phút",
     "",
     "Chốt xong phải: ① quyết định sửa code về đúng 5 phút HAY sửa text thông báo thành「6分前」; "
     "② cập nhật feature-spec.md §5 BR-02 và §9 M-01; ③ cập nhật thông báo lỗi trong code."],

    ["MT-05", "TRUNG BÌNH", W,
     "Chuyển 絞り込み → すべての友だち: giữ hay xóa điều kiện filter đã đặt?",
     "file 03/tab「test filte」r6-r7 (khi CHƯA tạo broadcast): 『filte xong tick sang all friend → "
     "hiển thị sl all; sau đấy lại tick lại thu hẹp → hiển thị sl all, **xóa bỏ hết đk lọc trước đó**』\n"
     "file 03/tab「test filte」r12-r13 (khi ĐÃ tạo xong broadcast): 『filte xong tick sang all friend → "
     "sau đấy lại tick lại thu hẹp → hiển thị sl đã filte, **vẫn giu đk lọc trước đó**』",
     "feature-spec.md §4 hàng 6: 『配信先絞込み → broadcast.flag_setting_filter + filters_v2.data. "
     "0=tất cả, 1=có filter』— KHÔNG nói gì về việc chuyển qua lại giữa 2 lựa chọn.\n"
     "logic-spec.md — không mô tả hành vi này ở bất kỳ mục nào.",
     "Cùng 1 thao tác UI cho 2 kết quả trái ngược tùy broadcast đã lưu hay chưa. Người dùng dễ tưởng đã "
     "xóa filter nhưng thực ra vẫn còn (hoặc ngược lại) → gửi nhầm đối tượng. Đây chính là họ hàng của "
     "bug #32229 (『Copy từ broadcast có filter sau đó đặt lịch gửi, nhưng broadcast copy lại bị gửi cho "
     "all friend』). Spec bỏ sót hoàn toàn quy tắc này.",
     "TC nhóm「配信先絞込み & 再計算」— 2 TC về chuyển qua lại giữa 絞り込み và すべての友だち",
     "",
     "Chốt xong phải: ① chốt hành vi ĐÚNG cho cả 2 trường hợp (chưa lưu / đã lưu); ② bổ sung quy tắc vào "
     "feature-spec.md §5 BR-06; ③ nếu 2 hành vi khác nhau là cố ý thì phải có chỉ dẫn trên UI cho người dùng."],

    ["MT-10", "TRUNG BÌNH", W,
     "Filter và tin nhắn được LƯU NGAY khi bấm lưu ở modal, không cần bấm lưu broadcast",
     "Tab master r833: 『sau khi edit không nhấn save → nhấn nút back về màn list → không lưu thay đổi "
     "=> **Case này sẽ vẫn lưu là có filter vì khi nhấn save ở modal đã lưu filter rồi**』\n"
     "file 03/tab function r122: 『**filter người nhận, template edit là được lưu lại luôn không cần nhấn lưu**』\n"
     "Ngược lại tab master r264, r269-r270: các trường khác (tiêu đề, thời gian) thì KHÔNG lưu nếu không "
     "bấm nút lưu broadcast — popup「作業を中断しますか？」reset lại dữ liệu.",
     "feature-spec.md §2 flow — mô tả filter được lưu ở bước 「絞り込み」+「設定」→「保存」quay lại form, "
     "sau đó mới「配信内容を確認して送信に進む」. KHÔNG nói rõ modal filter ghi thẳng vào DB.\n"
     "logic-spec.md — không mô tả điểm này.",
     "Trong cùng 1 màn edit, một số trường lưu ngay (filter, tin nhắn) còn một số trường chỉ lưu khi bấm nút "
     "(tiêu đề, thời gian, người gửi). Popup「作業を中断しますか？」nói『data trước đó thay đổi sẽ reset』"
     "nhưng thực tế KHÔNG reset filter — người dùng bị lừa. Đây là nguồn bug thầm lặng: đổi filter rồi hủy, "
     "tưởng đã hủy nhưng broadcast vẫn gửi theo filter mới.",
     "TC nhóm「配信先絞込み & 再計算」(TC sửa filter rồi Back không lưu) · "
     "「Edit broadcast & rule 5 phút」(TC sửa đủ trường nhưng không lưu)",
     "",
     "Chốt xong phải: ① liệt kê rõ trường nào lưu ngay / trường nào lưu khi bấm nút, ghi vào feature-spec.md §5; "
     "② quyết định có sửa text popup「作業を中断しますか？」cho đúng phạm vi reset không."],

    ["MT-19", "TRUNG BÌNH", W,
     "Status 'delivered' = ĐÃ ĐƯA VÀO HÀNG ĐỢI, không phải LINE đã gửi xong — tester dễ hiểu nhầm",
     "Corpus KHÔNG có TC nào phân biệt 2 khái niệm này. Toàn bộ TC gửi tin chỉ verify『friend nhận được "
     "message』mà không đo độ trễ giữa lúc status = delivered và lúc friend cuối cùng nhận tin.",
     "feature-spec.md §7: 『**Quan trọng**: `status='delivered'` được set ngay sau khi đẩy hết requests vào "
     "in-memory queue — KHÔNG phải sau khi LINE API xác nhận gửi xong. Tức là `delivered` = "
     "\"đã đưa vào hàng đợi gửi\"』\n"
     "feature-spec.md §9 M-02 đã tự ghi nhận: 『có thể gây hiểu nhầm cho tester』",
     "Với bot có hàng chục nghìn bạn bè, khoảng cách giữa status = delivered và lúc friend cuối nhận tin "
     "có thể rất lớn. Tester nhìn status = delivered rồi kết luận『gửi xong』sẽ bỏ lọt bug ở phần đuôi "
     "danh sách (rate limit, message_error, friend cuối không nhận). Cần chốt cách đo để TC có kết quả "
     "đáng tin.",
     "TC nhóm「Job gửi & vòng đời trạng thái」— TC về status delivered và TC hiệu năng quy mô lớn",
     "",
     "Chốt xong phải: ① chốt cách đo『gửi xong thật』cho tester (dựa vào send_count? message_error? "
     "hay lấy mẫu friend cuối danh sách?); ② cân nhắc bổ sung trạng thái hoặc chỉ báo tiến độ trên UI; "
     "③ ghi hướng dẫn này vào feature-spec.md §9 M-02."],

    ["MT-22", "TRUNG BÌNH", W,
     "PHÂN QUYỀN staff cho màn broadcast — có enforce ở tầng route/API không?",
     "Tab master r952 (Bug KH #36730, 05/2026): 『Account staff không quyền broadcast → Hiển thị "
     "\"Không có quyền\" hoặc redirect về dashboard. KHÔNG hiển thị broadcast. **Direct URL không bypass được.**』\n"
     "03/tab「[AI] alert_limit」r79-r83: TC-BAL-078 → 082 yêu cầu gọi thẳng API bằng session staff không "
     "quyền phải trả 403, và gọi với broadcast_id thuộc bot khác cũng phải 403.",
     "feature-spec.md §6, phần **Lưu ý middleware**: 『Tất cả routes broadcast dùng middleware chung `web` + "
     "`auth`. **Không có middleware access control riêng** — phân quyền Staff/Admin xử lý ở middleware layer "
     "chung (`RoleAccess`, `AccessFeature`)』\n"
     "feature-spec.md §9 U-10: 『Staff có quyền gì khác so với Admin? Module permission cụ thể?』— "
     "Ưu tiên Trung bình, CHƯA có lời giải.",
     "Spec nói broadcast KHÔNG có middleware riêng và để ngỏ câu hỏi staff có quyền gì. TCs lại khẳng định "
     "direct URL không bypass được. Đây đúng là kiểu bug『UI ẩn menu nhưng API vẫn trả dữ liệu』— nếu "
     "RoleAccess/AccessFeature không phủ hết các endpoint ajax của broadcast thì staff không quyền vẫn "
     "đọc/sửa được broadcast bằng cách gọi thẳng API.",
     "TC nhóm「Phân quyền & môi trường」— 4 TC về staff không quyền, gọi thẳng API, cross-tenant, chưa đăng nhập",
     "",
     "Chốt xong phải: ① liệt kê đầy đủ endpoint broadcast và xác nhận từng cái có qua RoleAccess/AccessFeature "
     "không; ② trả lời U-10 trong feature-spec.md §9; ③ nếu có endpoint hở thì raise bug bảo mật."],

    ["MT-02", "THẤP", W,
     "THỨ TỰ SẮP XẾP mặc định của danh sách nhiều mốc gửi — tăng dần hay giảm dần?",
     "Tab master r48-r59: 『Danh sách list item hiển thị - Hiển thị all ngày giờ chờ send **giảm dần**』\n"
     "Tab master r75, r83: 『check thứ tự sắp xếp → **từ bé đến lớn**』, kết quả ghi **NG** "
     "(『time con bé hơn cha ngoài màn list đang hiện thị cha trước』)\n"
     "Tab master r418: 『check thứ tự sắp xếp → từ bé đến lớn』, kết quả OK (ở tab 下書き)",
     "logic-spec.md:89: 『**Sort**: mặc định **DESC** theo send_day, send_time, id』(tức giảm dần)\n"
     "ui-spec.md:89: cột「配信予定日時」có icon sort up/down, không nói chiều mặc định.",
     "Corpus tự mâu thuẫn: r48-r59 nói giảm dần, r75/r83/r418 nói tăng dần. Spec nói giảm dần. "
     "Thêm nữa r75 ghi kết quả NG cho việc bản ghi con có thời gian nhỏ hơn cha vẫn bị xếp sau cha — "
     "tức là sort đang tính theo quan hệ cha/con chứ không theo giá trị thời gian. Ảnh hưởng tới việc "
     "tester đọc danh sách và tới trải nghiệm khách hàng khi có nhiều mốc gửi.",
     "TC nhóm「Tab 配信予約 — cột & hiển thị」(TC nhiều lịch gửi) · 「Sắp xếp & lọc theo thời gian」"
     "(TC bản ghi con sớm hơn cha)",
     "",
     "Chốt xong phải: ① chốt chiều sort mặc định; ② chốt sort tính theo GIÁ TRỊ thời gian chứ không theo "
     "quan hệ cha/con; ③ nếu r75 vẫn NG thì raise bug."],

    ["MT-04", "THẤP", W,
     "Đặt lịch ở thời gian QUÁ KHỨ — alert xác nhận hay validate chặn?",
     "Tab master r60, r76: 『tạo broadcast time nhỏ hơn time khi lưu → hiển thị **alert** "
     "配信日時に現在時刻より前の時間が設定されています。配信登録を押すと即時配信となりますがよろしいですか？』, "
     "cột kết quả ghi『**chưa có nút hủy**』\n"
     "Tab master r84 (cùng tab master, khối tích 配信予約): 『time cũ (time quá khú) → **validate**』, "
     "kết quả ghi **NG**\n"
     "Tab master r19, r396: 『time quá khứ → wait-to-send』(tức vẫn lưu được)",
     "feature-spec.md §4 hàng 4: 『配信予約 — Ngày gửi → Bắt buộc, format YYYY-MM-DD. Không được trống hoặc "
     "'0000:00:00'』— KHÔNG cấm ngày quá khứ.\n"
     "logic-spec.md:180: 『`send_day` bắt buộc (không phải `0000:00:00`)』— cũng không cấm quá khứ.\n"
     "ui-spec.md — không mô tả alert này.",
     "Trong cùng 1 tab master, cùng thao tác『chọn thời gian quá khứ』được ghi 2 kết quả mong đợi khác nhau "
     "(alert vs validate). Thêm nữa alert được ghi là『chưa có nút hủy』— nếu vậy người dùng lỡ chọn nhầm "
     "ngày quá khứ sẽ bị gửi ngay cho toàn bộ bạn bè mà không rút lại được. Đây là rủi ro thật với khách hàng.",
     "TC nhóm「配信タイミング設定 — gửi ngay/đặt lịch」— 3 TC về thời gian quá khứ",
     "",
     "Chốt xong phải: ① chốt hành vi duy nhất (alert có nút hủy / validate chặn); ② nếu là alert thì "
     "BẮT BUỘC có nút hủy — raise bug nếu chưa có; ③ ghi quy tắc vào feature-spec.md §5."],

    ["MT-06", "THẤP", W,
     "Tab 下書き có cột「クイックテスト」không?",
     "Tab master r390 (khối 下書き): danh sách cột KHÔNG liệt kê クイックテスト\n"
     "NHƯNG tab master r436-r438 (vẫn trong khối 下書き): có TC đầy đủ cho "
     "『クイックテスト未設定 (setting quick test) → default → クイックテスト未設定 gạch chân → "
     "Check khi click vào → Hiển thị popup preview send test → tick quick send』",
     "ui-spec.md:103-115 (Tab 下書き): danh sách 9 cột KHÔNG có「クイックテスト」\n"
     "ui-spec.md:141: 『Tab「配信予約」có cột「クイックテスト」, **2 tab kia không có**』",
     "Có thể là 2 thứ khác nhau: cột「クイックテスト」ở MÀN LIST (chỉ tab 配信予約 có) và chức năng "
     "クイックテスト未設定 ở MÀN ĐĂNG KÝ tin nhắn (mọi luồng đều có). Nếu vậy thì không mâu thuẫn. "
     "Nhưng cần chốt để tester không đi tìm cột không tồn tại ở tab 下書き.",
     "TC nhóm「Tab 下書き — cột & hiển thị」· 「Tài khoản test & quick test」",
     "",
     "Chốt xong phải: ① xác nhận cột「クイックテスト」chỉ có ở tab 配信予約; ② ghi rõ chức năng quick test "
     "ở màn đăng ký áp dụng cho mọi luồng vào ui-spec.md."],

    ["MT-07", "THẤP", W,
     "Broadcast nhiều mốc gửi ở tab 配信履歴 — hiển thị 1 dòng (mốc gần nhất) hay đủ các mốc con?",
     "Tab master r679: 『Khi có item / default → hiển thị các item đã gửi, cái mới nhất trên đầu, "
     "**nếu item nào có nhiều time hiển thị time của thằng con send gần nhất**』\n"
     "file 03/tab function r21: 『màn đã send』, cột Note ghi 『**đang hiển thị hết tất cả thằng con**』",
     "ui-spec.md:119-133 (Tab 配信履歴): mô tả 7 cột, không nói về broadcast nhiều mốc.\n"
     "logic-spec.md:90: 『`delivery_dates`: children broadcasts (parent_id)』— chỉ nói enrich, không nói "
     "cách hiển thị ở màn list.\n"
     "feature-spec.md §5 BR-03 chỉ mô tả cấu trúc cha/con, không nói cách hiển thị.",
     "Nếu 1 broadcast 10 mốc gửi hiển thị thành 10 dòng ở tab 配信履歴 thì danh sách bị phình và khách "
     "hàng khó đọc; nếu chỉ 1 dòng thì không xem được lịch sử từng mốc. Corpus ghi 2 hành vi trái ngược "
     "ở 2 tab khác nhau của cùng file.",
     "TC nhóm「Tab 配信履歴 — cột & hiển thị」— TC broadcast nhiều lịch ở tab lịch sử",
     "",
     "Chốt xong phải: ① chốt cách hiển thị; ② nếu chỉ 1 dòng thì phải có cách xem chi tiết từng mốc; "
     "③ bổ sung vào ui-spec.md phần Tab 配信履歴."],

    ["MT-08", "THẤP", W,
     "Sửa cùng broadcast trên 2 tab — thứ tự lưu quyết định kết quả filter theo cách khó đoán",
     "Tab master r831: 『tab1 chọn sang có filter → save tab 1 trước; tab 2 chọn k filter → save "
     "→ **broadcast không filter**』\n"
     "Tab master r832: 『tab1 chọn không filter → save tab 1 trước; tab 2 chọn có filter → save "
     "→ **broadcast có filter** … Khi save tab 1 đã xóa các đk filter cũ rồi => tab 2 nếu k edit lại filter "
     "thì khi lưu lại broadcast vẫn sẽ là không filter』",
     "feature-spec.md, logic-spec.md — KHÔNG có mục nào về xử lý sửa đồng thời (concurrency) cho broadcast.\n"
     "feature-spec.md §5 BR-08 chỉ nói về Bot Switch Guard (kiểm tra botIdCurrent), không nói về việc "
     "2 tab cùng sửa 1 broadcast.",
     "Kết quả cuối phụ thuộc vào việc tab 2 có mở lại modal filter hay không — một điều kiện người dùng "
     "không nhận biết được. Cùng thao tác 'tab 2 chọn có filter rồi save' cho kết quả khác nhau tùy tab 1 "
     "đã làm gì. Rủi ro: gửi nhầm cho toàn bộ bạn bè khi tưởng đã đặt filter. Spec bỏ trống hoàn toàn "
     "vấn đề concurrency.",
     "TC nhóm「配信先絞込み & 再計算」— TC sửa cùng broadcast trên 2 tab",
     "",
     "Chốt xong phải: ① chốt chiến lược xử lý xung đột (last-write-wins? cảnh báo? khóa bản ghi?); "
     "② bổ sung mục concurrency vào feature-spec.md §5; ③ cân nhắc cảnh báo trên UI khi phát hiện bản ghi "
     "đã bị người khác sửa."],

    ["MT-09", "THẤP", W,
     "Profile người gửi của broadcast hiển thị ở chat 1:1 — trực tiếp hay phải bấm「詳細情報」?",
     "Improve chung/tab「Profile sender」r157-r164 (khối Test job / Send all): kết quả mong đợi là "
     "『Check profile ở chat 1:1 và phía line user là ảnh và tên bot / của sender đã chọn』, "
     "NHƯNG cột kết quả thực tế ghi: 『**Chat 1:1 thì Send all hiển thị profile khi click vào button 詳細情報**』"
     " — tức phải bấm mới thấy.\n"
     "Cùng tab r165: 『**Scenario không hiển thị profile sender ở chat 1:1**』— hành vi lại khác nữa.\n"
     "r179-r181: 『Hiện tại job này không set profile sender』cho Remind, Resend message error, Schedule send chat.",
     "feature-spec.md §5 BR-05: 『Default profile = tên và avatar LINE Official Account. Admin có thể tạo "
     "nhiều custom profiles』— KHÔNG nói profile hiển thị ở đâu trong chat 1:1.\n"
     "db-mapping — `messages_v2s.profile_send` tham chiếu bots_profiles, nhưng không mô tả cách render ở UI.",
     "Nếu profile sender chỉ hiện khi bấm「詳細情報」thì admin nhìn lướt chat 1:1 sẽ tưởng tin gửi bằng "
     "profile bot gốc. Thêm nữa hành vi khác nhau giữa broadcast / scenario / remind / resend / schedule chat "
     "— chưa rõ đâu là cố ý, đâu là thiếu sót.",
     "TC nhóm「送信者名 — áp dụng khi gửi」— TC job gửi broadcast thật",
     "",
     "Chốt xong phải: ① chốt cách hiển thị profile sender ở chat 1:1 cho broadcast; ② liệt kê job nào có "
     "set profile sender, job nào không, và ghi vào feature-spec.md §5 BR-05; ③ 3 job chưa set "
     "(Remind, Resend, Schedule chat) là bug hay hạn chế được chấp nhận?"],

    ["MT-11", "THẤP", W,
     "Số 配信数 ở màn list LỆCH với danh sách chi tiết khi chưa bấm「再計算」— bug hay hành vi cache?",
     "file 03/tab「test filte」r17: 『khi mở chặn friend / chưa reset → **sl bên ngoài vẫn như cũ nhưng khi "
     "click vào thì ra sl không khớp vs bên ngoài**』— cột kết quả ghi **OK** (tức tester chấp nhận).\n"
     "Tab master r249: 『check double click text số người dự định send → tính 1 lần, hiển thị danh sách "
     "người dự định send』, cột kết quả ghi『**hiển thị sai số ng dự định send**』.",
     "feature-spec.md §4 hàng 7: 『配信数 → broadcast.filter_number → Cập nhật khi nhấn「再計算」hoặc thay đổi filter』\n"
     "logic-spec.md:97-103: getFilterNumber() chỉ chạy khi bấm 再計算, cập nhật filter_number + filter_date.\n"
     "→ Spec ngầm xác nhận đây là giá trị CACHE.",
     "Spec ngầm cho phép lệch (vì filter_number là cache), nhưng khách hàng nhìn 2 số khác nhau cho cùng "
     "1 broadcast thì sẽ báo bug — đây chính là bản chất của bug #31527 đã từng phát sinh. Cần chốt để "
     "tester biết khi nào ghi NG, khi nào ghi OK.",
     "TC nhóm「配信先絞込み & 再計算」— TC friend bỏ block nhưng chưa bấm 再計算",
     "",
     "Chốt xong phải: ① chốt lệch số là chấp nhận được hay là bug; ② nếu chấp nhận thì bổ sung chỉ dẫn "
     "trên UI (VD ghi ngày tính lại gần nhất từ filter_date); ③ ghi quy tắc vào feature-spec.md §4 hàng 7."],

    ["MT-12", "THẤP", W,
     "Giới hạn số điều kiện filter AND/OR — 100 item hay 5 item?",
     "Improve chung/tab「Improve sendall scenario」r18 (tiêu đề khối): "
     "『2. filter and và or ko add quá **100 item**』\n"
     "Cùng tab r22 (dòng ngay dưới): 『2. filter and và or ko add quá 100 item **(test với mỗi cái 5 item)**』\n"
     "r23-r34: toàn bộ TC thực tế đo ở mốc **5 item** — 『> 5 item → これ以上追加できません。』",
     "feature-spec.md §5 BR-06: 『Hỗ trợ tổ hợp AND (tất cả điều kiện phải thoả) + OR (ít nhất 1 điều kiện "
     "thoả). 11 loại filter』— KHÔNG nói giới hạn số điều kiện.\n"
     "ui-spec.md §SCR-BC-03 — không nói giới hạn.",
     "Con số 100 ở tiêu đề và con số 5 trong TC chênh nhau 20 lần. Có thể 5 chỉ là dữ liệu test cho tiện "
     "(dev hạ ngưỡng khi test), nhưng cũng có thể giới hạn thật là 5. Ảnh hưởng tới TC ranh giới và tới "
     "khách hàng cần lọc phức tạp. Spec bỏ trống hoàn toàn.",
     "TC nhóm「配信先絞込み & 再計算」— TC ranh giới số điều kiện AND/OR",
     "",
     "Chốt xong phải: ① tra giới hạn thật trong code/config; ② bổ sung vào feature-spec.md §5 BR-06; "
     "③ nếu là 100 thì phải test lại ở mốc 100 vì hiệu năng query filter có thể là vấn đề."],

    ["MT-14", "THẤP", W,
     "Danh sách friend đã gửi của broadcast CŨ (trước 08:00 ngày 15/01/2025) không được hỗ trợ",
     "file 03/tab「Update list friend đã send」r4: 『data cũ / trước 8h ngày 15/1/2025 → các send all send "
     "trước 2025, tìm trong bảng message theo năm theo điều kiện sender_id = broadcast_id và msg_kind = 3 "
     "→ **ko support => click vào vẫn ra mh friendlist**』\n"
     "Cùng tab r5: 『sau 8h ngày 15/1/2025 → các send all mới 2025 message lưu ở bảng message_v2s, "
     "tìm theo sourse_message_id và msg_kind = 3, type = 14 → ở ngoài hiển thị số lượng bn thì trong hiển thị bấy nhiêu』",
     "feature-spec.md §3: liệt kê `messages_v2s` là bảng log từng tin nhắn đã gửi. KHÔNG nhắc tới bảng "
     "`message` cũ hay mốc chuyển đổi 15/01/2025.\n"
     "db-mapping.md — không có mục về migration dữ liệu message cũ.",
     "Khách hàng có broadcast từ trước 2025 bấm vào số 配信数 sẽ ra màn friendlist chung thay vì danh sách "
     "người đã nhận — nhìn như bug. Không có thông báo giải thích. Spec không ghi lại quyết định "
     "『không hỗ trợ dữ liệu cũ』nên người sau đọc spec sẽ tưởng đây là bug.",
     "TC nhóm「配信数 & danh sách friend đã gửi」— TC broadcast cũ trước 15/01/2025",
     "",
     "Chốt xong phải: ① xác nhận quyết định không hỗ trợ dữ liệu cũ; ② bổ sung mốc 15/01/2025 và 2 bảng "
     "dữ liệu vào db-mapping.md; ③ cân nhắc hiển thị thông báo thay vì đưa về friendlist."],

    ["MT-15", "THẤP", W,
     "Popup preview KHÔNG có trong spec — 3 tab, tên tab khác nhau giữa các màn",
     "Tab master r160-r232 (từ màn edit), r274-r347 (từ tab 配信予約/下書き), r699-r748 (từ tab 配信履歴): "
     "~150 TC cho popup preview.\n"
     "Tên tab: ở màn edit và tab 予約/下書き là「メッセージ」·「概要」·「アクション」; "
     "ở tab 配信履歴 là「トークルーム」·「アクション」(2 tab, tab đầu đổi tên).",
     "feature-spec.md §9 U-01: 『Màn hình xác nhận gửi (sau「配信内容を確認して送信に進む」) trông như thế nào?』"
     " — Ưu tiên **Cao**, CHƯA có lời giải.\n"
     "feature-spec.md §9 U-07: 『Quick test hoạt động như thế nào? Gửi thử cho ai?』— Ưu tiên Trung bình, chưa giải.\n"
     "ui-spec.md — KHÔNG có mục nào mô tả popup preview.",
     "Popup preview là nơi tập trung nhiều TC nhất (~150 dòng corpus) nhưng spec bỏ trống hoàn toàn và tự "
     "ghi nhận là unknown U-01/U-07. Tên tab khác nhau giữa các màn cũng chưa rõ là cố ý hay lỗi. "
     "Tester không có căn cứ spec để đánh giá đúng/sai.",
     "TC nhóm「Preview — 3 tab nội dung」·「Tài khoản test & quick test」·「テスト送信 & 一括テスト送信」",
     "",
     "Chốt xong phải: ① bổ sung màn popup preview vào ui-spec.md (đóng U-01 và U-07); ② chốt tên tab ở "
     "tab 配信履歴 là「トークルーム」có cố ý không; ③ ghi rõ quick test tối đa 3 người vào feature-spec.md §5."],

    ["MT-18", "THẤP", W,
     "Bản COPY không sửa được filter trước khi lưu lần đầu — ràng buộc không có trong spec",
     "Tab master r852-r862 (Bug #32229, 02/10/2025): lặp lại 8 lần cùng 1 kết quả mong đợi "
     "『**Khi chưa nhấn save broadcast thì không edit được filter** => setting filter của broadcast mới sẽ "
     "giống broadcast gốc => Sau khi nhấn save xong thì edit filter của broadcast mới được bình thường』",
     "feature-spec.md §5 BR-07 (Sao chép broadcast): 『Khi copy: broadcast, templates, actions, filters, "
     "child broadcasts đều được clone. Broadcast bản copy luôn bắt đầu với status = 'draft'』"
     " — KHÔNG nói gì về việc khóa sửa filter trước lần lưu đầu.\n"
     "logic-spec.md — không mô tả ràng buộc này.",
     "Đây là ràng buộc phát sinh từ fix bug #32229 (copy broadcast có filter bị gửi cho all friend). "
     "Người dùng copy xong muốn đổi filter ngay sẽ thấy bị khóa mà không rõ lý do — trải nghiệm khó hiểu. "
     "Spec không ghi lại nên người sau đọc spec sẽ tưởng đây là bug.",
     "TC nhóm「Copy broadcast」— TC bản copy không sửa được filter trước khi lưu",
     "",
     "Chốt xong phải: ① bổ sung ràng buộc vào feature-spec.md §5 BR-07; ② cân nhắc hiển thị chỉ dẫn trên UI "
     "(VD disable nút 設定 kèm tooltip giải thích) thay vì im lặng."],

    ["MT-21", "THẤP", W,
     "Broadcast legacy ĐÃ GỬI có mở được màn chi tiết/edit không?",
     "Tab master r792 (khối CHECK COVER CASE CŨ): 『send all đã send / type send / send khi click button / "
     "check list temp con』— cột kết quả ghi **『Not test — ko vào dc mh edit』**\n"
     "Các dòng lân cận r793-r804 (check filter, check ng send, check copy, check preview) đều ghi OK.",
     "feature-spec.md §5 BR-01: 『**Không thể chỉnh sửa/xoá broadcast khi `delivering` hoặc `delivered`**』"
     " — tức KHÔNG vào được màn edit là ĐÚNG spec.\n"
     "Nhưng ui-spec.md:131 (Tab 配信履歴) vẫn liệt kê cột「操作」với『Action buttons』mà không nói rõ có nút nào.\n"
     "feature-spec.md §9 U-08: 『Cột「操作」chứa nút nào? Sửa? Xoá? Sao chép?』— chưa có lời giải.",
     "Nếu không vào được màn edit là đúng theo BR-01 thì ghi chú『Not test』của corpus là do hiểu nhầm, và "
     "TC đó nên chuyển thành TC xác nhận KHÔNG vào được. Nhưng r793-r804 lại kiểm tra được filter và người "
     "gửi — nghĩa là có màn XEM nào đó. Cần chốt để tester biết vào bằng đường nào.",
     "TC nhóm「Broadcast cũ & tương thích」— TC broadcast legacy đã gửi",
     "",
     "Chốt xong phải: ① chốt broadcast đã gửi mở được màn XEM (read-only) hay không mở được gì; "
     "② trả lời U-08 — liệt kê nút trong cột「操作」của từng tab vào ui-spec.md."],
]
