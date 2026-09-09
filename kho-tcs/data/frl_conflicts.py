# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ ĐANG CHỜ QUYẾT ĐỊNH của Leader (2026-08-26).

Nguồn TCs: 10.3 TCsLine_Friendlist (tab「Testcase」+ tab「#38866」) + TCsLine_Improve
chung (tab「ESticsearch」·「Improve nhỏ」·「Improve filter + url」·「Improve speed」·
「Phân quyền」).
Nguồn spec: spec-features/admin/friend-list/ (chốt 2026-03-25, cross-check 64/64).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "Ô tìm kiếm「友だち名・システム表示名」có khớp cột メールアドレス không? "
     "Spec TỰ MÂU THUẪN ở 4 chỗ",
     "Tab「#38866」(07/2026, tab mới nhất) coi search-khớp-email là hành vi ĐÚNG và dành hẳn "
     "17 dòng cho nhóm này:\n"
     "• r18: friend CHỈ khớp keyword qua Email vẫn phải hiển thị trong danh sách\n"
     "• r19:『⭐⚠ RỦI RO CHÍNH CỦA FIX — lúc đếm (advanceFilterPost) quét 3 cột 友だち名 + "
     "Email + システム表示名 nên N CÓ tính friend khớp email; nếu điều kiện lọc lưu cho job chỉ "
     "có LINE名 + システム表示名 thì nhóm khớp email bị sót』\n"
     "• r20:『⭐⏳ Bug ẩn』— keyword khớp 200 friend qua tên + 120 friend CHỈ qua email, "
     "expect đủ 320 friend nhận action\n"
     "• r22: search「tanaka」khớp cả friend TÊN tanaka lẫn friend EMAIL bắt đầu bằng tanaka\n"
     "• r23-r24: search domain「gmail.com」/ ký tự「@」khớp friend qua email\n"
     "• r31: friend có email NULL không được khớp nhầm",
     "4 chỗ trong spec nói 3 con số cột KHÁC NHAU:\n"
     "• web/logic-spec.md:395 —『Keyword search: Tách keyword theo space, search OR trên "
     "line_user.name, line_user.email, line_user.view_name』(3 cột, CÓ email)\n"
     "• web/api-spec.md:101 —『keyword: Từ khoá tìm kiếm (tên LINE, email, system name)』"
     "(3 cột, CÓ email)\n"
     "• feature-spec.md §2『Luồng end-to-end: Tìm kiếm』—『searchLineUser(): line_user.name "
     "LIKE '%keyword%', is_blocked=0』(1 cột, KHÔNG email, KHÔNG cả view_name)\n"
     "• ui/ui-spec.md:48 — placeholder ô tìm kiếm là「友だち名・システム表示名」(2 cột, "
     "KHÔNG nhắc email)",
     "Đây là khác biệt NHÌN THẤY ĐƯỢC ở phía khách hàng: nếu search có khớp email thì KH gõ "
     "tên người này vẫn vô tình chọn phải người khác (trùng chuỗi trong email) → số friend "
     "nhận action phình lên ngoài ý muốn; nếu không khớp email thì placeholder đúng nhưng "
     "toàn bộ nhóm 17 TC của #38866 là sai gốc. Nghiêm trọng hơn: nếu tầng ĐẾM quét 3 cột mà "
     "tầng LƯU ĐIỀU KIỆN LỌC cho job chỉ lưu 2 cột thì số N trên nhãn KHÔNG BAO GIỜ bằng số "
     "friend thực tế nhận action — chính là lớp bug #38866 chưa được đóng hết. "
     "Placeholder cũng cần chốt: nếu giữ khớp email thì placeholder hiện tại đang gây hiểu nhầm.",
     "Nhóm『Tìm kiếm theo từ khoá』: TC search khớp メールアドレス · nhóm TRỘN tên+email >200 · "
     "search theo DOMAIN · friend khớp cả email lẫn tên · friend không có email · keyword email "
     "các dạng · email hoa/thường. "
     "Nhóm『Bulk action — ngưỡng 200 & schedule』: TC chẩn đoán 4 con số · TC đặt lịch với "
     "keyword khớp email. "
     "Nhóm『Màn danh sách — hiển thị』: TC toolbar (placeholder).",
     "",
     ""],

    ["MT-02", "CAO", W,
     "Kết quả TÌM KIẾM phân trang 50 hay 200 friend/trang? Chi phối toàn bộ biên 200/201 "
     "của nhóm checkbox",
     "Tab「#38866」(07/2026) khẳng định 1 trang = 200 kể cả khi có search:\n"
     "• r59:『Kết quả search ≤200 → tích 全選択 → checkbox KHÔNG hiển thị / Vì 1 page = 200 "
     "nên 全選択 đã chọn hết toàn bộ kết quả』\n"
     "• r10 và r75:『Search keyword → chỉ tích 全選択, không tích checkbox → chỉ 200 friend "
     "của page hiện tại nhận action, 112 friend còn lại KHÔNG nhận』(tổng kết quả 312)\n"
     "• r61:『Kết quả search = 201 → checkbox HIỂN THỊ, chưa tích thì panel vẫn 選択中 200人』\n"
     "Tab「Testcase」r8, r24:『Không có case này do số user 1 page max là 200』(đánh Reject "
     "case chọn 201 friend trong cùng 1 trang)",
     "3 chỗ trong spec nói 50:\n"
     "• web/logic-spec.md:62 (hàm searchLineUser) —『Phân trang thủ công: offset = (page-1)*50, "
     "limit = 50』\n"
     "• web/logic-spec.md:609 —『Search result: 50 items/page — :266-267』\n"
     "• feature-spec.md §2『Luồng end-to-end: Tìm kiếm』—『Response: HTML partial (50 items/page)』\n"
     "Spec cũng nói danh sách chính (filter v2) mới là 200/page (logic-spec.md:607, "
     "feature-spec.md BR-04)",
     "Hai luồng khác nhau: EP-04 result_search (50/trang) và EP-02 post-advance-filter-v2 "
     "(200/trang). TC gốc giả định thao tác search cũng chạy qua luồng 200/trang. Nếu spec "
     "đúng thì mọi con số 200 trong nhóm checkbox phải là 50, và biên hiển thị checkbox phải "
     "là >50 chứ không phải >200 — tức toàn bộ TC boundary của #38866 lệch. Nếu TC gốc đúng "
     "thì frontend không dùng EP-04 nữa mà gọi EP-02 kèm keyword, và spec đang mô tả một "
     "endpoint đã hết dùng. Đây là chênh lệch NHÌN THẤY ĐƯỢC: số friend nhận action khác nhau "
     "150 người chỉ vì con số phân trang.",
     "Nhóm『Sắp xếp & phân trang』: TC phân trang 200/trang. "
     "Nhóm『Chọn friend & checkbox 全選択』: TC biên hiển thị checkbox 199/200/201. "
     "Nhóm『Bulk action — ngưỡng 200 & schedule』: TC không chọn quá 200 trong 1 trang · "
     "TC regression tích 全選択 nhưng không tích checkbox.",
     "",
     ""],

    ["MT-03", "CAO", W,
     "Chạy action từ màn friendlist CÓ update last_message / last_time_message của friend "
     "không? ⚠ 2 mốc chỉ cách nhau 1 tháng",
     "Trong CÙNG một ô kết quả mong đợi của tab「Testcase」có 2 tầng NGƯỢC NHAU:\n"
     "• Tầng cũ (Bug KH #35071, 03/2026) — r46-r53:『update last_message và last_time_message "
     "cho user hiển thị ở màn chat 1:1 / Nội dung của last message là text của message được "
     "send cuối cùng / Check hiển thị đúng last_time_message ở màn friendlist』\n"
     "• Tầng mới (SpecImprove #35389, 04/2026) — cùng ô:『Spec change 4/2026: Không update "
     "last message của friend / + Time của last message không update / + Nội dung last message "
     "không update』\n"
     "Cột「Actual Result」của r60-r71 và r99-r110 đều chép lại chính câu spec change này.\n"
     "• r59 còn ghi thêm:『Message send ngay của remind là do bên web send nên CÓ update last "
     "message → Spec change』— tức nhánh remind từng lệch so với các nhánh khác.\n"
     "Nội dung ticket ở tab Info r6:『SpecImprove #35389 Sửa khi send message ko update last "
     "message và last time send, Chỉ update khi có message friend gửi đến』",
     "Spec KHÔNG có quy tắc nào về last_message khi chạy action:\n"
     "• db/db-mapping.md:411 chỉ nói『Cột tin nhắn mới 最新メッセージ ← conversation."
     "last_time_message — Cache trên conversation, không query messages mỗi lần』\n"
     "• web/logic-spec.md:375-376 chỉ liệt kê 2 cột last_message / last_time_message\n"
     "• feature-spec.md §2『Luồng end-to-end』của EP-17 sendAction KHÔNG nhắc gì tới việc cập "
     "nhật 2 cột này",
     "⚠ CẢNH BÁO NIÊN ĐẠI: 03/2026 và 04/2026 chỉ cách nhau 1 tháng nên quy tắc『ưu tiên TC mới "
     "nhất』là căn cứ YẾU nếu chỉ xét ngày. Kho tạm chọn tầng #35389 vì 3 lý do có thể kiểm "
     "chứng được: (a) #35389 TỰ KHAI BÁO là spec change chứ không phải bug fix; (b) cột kết quả "
     "#35389 có đủ trạng thái OK ở step/staging trong khi cột #35071 đã bị nó thay thế; "
     "(c) cột Actual của 20+ dòng đều ghi lại câu spec change này. Nhưng đây vẫn là suy luận — "
     "nếu Leader chốt theo tầng cũ thì toàn bộ TC của nhóm 9 sẽ DỰ KIẾN FAIL và phải raise bug. "
     "Ngoài ra spec-features hoàn toàn im lặng về quy tắc này → dù chốt hướng nào cũng phải "
     "bổ sung vào spec, vì nó ảnh hưởng trực tiếp cột「最新メッセージ」mà Admin nhìn thấy.",
     "Toàn bộ nhóm『Bulk action — last message & bộ đếm 未確認』(11 TC) và TC lỗi giới hạn "
     "tin nhắn ở nhóm『Bulk action — lỗi & hiệu năng』",
     "",
     ""],

    ["MT-04", "CAO", W,
     "Ngưỡng chuyển sang job là >200 hay ≥200, và có tồn tại bảng `action_lineuser` "
     "(SpecImprove #34720) không?",
     "Tab「Testcase」có 2 tầng expected chồng nhau trong cùng ô, ở r5-r34:\n"
     "• Tầng cũ (SpecImprove #34438, 02/2026):『Send được action luôn cho các user được chọn / "
     "Không tạo action schedule』\n"
     "• Tầng mới (SpecImprove #34720, 03/2026):『Không send action luôn cho user / Add record "
     "vào bảng action_lineuser (type = friendList, type_start_scenario = 15001), mỗi line user "
     "là 1 record / Check job send được action cho các user được chọn』\n"
     "→ tức #34720 đưa MỌI trường hợp qua job, kể cả ≤ 200 friend.\n"
     "Kết quả test 2 cột NGƯỢC NHAU ở cùng 1 dòng: r12, r13, r20, r21, r28, r29, r33, r34 "
     "(các case 1.000 / 1.001 friend) — cột #34720 đánh **Reject**, cột #34438 đánh **OK**.\n"
     "Nội dung ticket ở tab Info r3:『Improve performance /basic/friendlist/send-action』, "
     "trạng thái dev『Coding』, kết quả test『NG』.",
     "• web/logic-spec.md:244-250 —『Nếu tổng > 200 → Tạo ActionSchedule (background "
     "processing) / Nếu tổng <= 200 → gọi sendAction() trực tiếp』\n"
     "• web/logic-spec.md:252 — thông báo hiển thị cho user:『対象の友だち数が200人以上の場合、"
     "処理に時間がかかる場合があります。』(200人以上 = ≥ 200)\n"
     "• feature-spec.md BR-05 —『> 200 users → tạo ActionSchedule. <= 200 → xử lý trực tiếp』\n"
     "• Bảng `action_lineuser` và giá trị `type_start_scenario = 15001`: grep toàn bộ "
     "spec-features/admin/friend-list/ trả về **0 kết quả**",
     "Hai điểm lệch riêng biệt: (1) Ngưỡng — logic là >200 nhưng CHÍNH câu thông báo hiển thị "
     "cho user lại ghi 200人以上 (≥200); đúng ở mốc 200 friend, user đọc thông báo sẽ tưởng "
     "phải chờ job trong khi thực tế chạy ngay. (2) Luồng — nếu #34720 đã release thì mô hình "
     "『≤200 chạy trực tiếp』trong spec đã lỗi thời và mọi TC『không tạo action schedule』phải "
     "đổi expected; nếu #34720 chưa release (khớp với trạng thái Coding/NG và các ô Reject) thì "
     "tầng expected này phải bị gỡ khỏi TC gốc để không gây nhầm cho người test sau. "
     "Không được tự chọn — phải hỏi Dev xem #34720 hiện đang ở nhánh nào.",
     "Toàn bộ nhóm『Bulk action — ngưỡng 200 & schedule』(13 TC), đặc biệt các TC biên "
     "199/200/201 và TC 1.000/1.001 friend",
     "",
     ""],

    ["MT-05", "TRUNG BÌNH", W,
     "Đổi keyword tìm kiếm khi đang tích 全選択 + checkbox — trạng thái chọn-all có bị reset "
     "không?",
     "Tab「#38866」r57 và r72 mô tả cùng một rủi ro qua 2 đường kích hoạt (nhấn Enter và "
     "click nút tìm kiếm), kết quả mong đợi do người viết TC đề xuất:\n"
     "『Expect: search mới PHẢI reset lựa chọn (bỏ tích 全選択 + checkbox, panel về 選択中 0人) / "
     "Nếu trạng thái chọn-all được giữ → action apply theo keyword MỚI chứ không phải nhóm "
     "user thấy lúc chọn / Label N phải update』\n"
     "Cả 2 dòng đều gắn ghi chú『⏳ Cần confirm TA — nghi ngờ trạng thái không reset』, "
     "tức người viết TC CHƯA xác nhận được đây là hành vi thật hay chỉ là mong đợi.",
     "Spec KHÔNG mô tả checkbox「条件に当てはまる友だち{N}人全員を選択」ở bất kỳ file nào — "
     "ui/ui-spec.md:74 và feature-spec.md §2 chỉ có checkbox「全選択」. Vì vậy cũng KHÔNG có "
     "quy tắc nào về vòng đời trạng thái chọn khi đổi điều kiện lọc.",
     "Đây là cùng lớp với bug #38866: user nhìn thấy 312 người, đổi keyword rồi bấm chạy "
     "action, nếu trạng thái chọn-all còn giữ ngầm thì action áp cho nhóm 500 người của "
     "keyword mới. Hậu quả giống hệt bug gốc (gắn tag nhầm cho nhóm khác) nhưng đi bằng đường "
     "khác nên fix của #38866 chưa chắc đã đóng. TC gốc chỉ ghi mong đợi chứ chưa có bằng "
     "chứng chạy — cần Leader chốt hành vi đúng rồi mới khoá expected.",
     "Nhóm『Tìm kiếm theo từ khoá』: TC đang tích 全選択 + checkbox rồi search keyword mới. "
     "Nhóm『Chọn friend & checkbox 全選択』: TC tích checkbox rồi đổi keyword search.",
     "",
     ""],

    ["MT-06", "TRUNG BÌNH", W,
     "Dấu cách full-width (U+3000) trong keyword làm lệch số friend nhận action — bug #38951 "
     "còn mở",
     "Tab「#38866」có 5 dòng về dấu cách full-width, trong đó 2 dòng đã FAIL và 3 dòng chưa chạy:\n"
     "• r39 (keyword「6期生　太郎」dùng IME tiếng Nhật) — kết quả **NG**, cột Actual ghi "
     "『bug: #38951』. TC gốc đánh dấu『⏳⚠ Ưu tiên cao nhất trong nhóm dấu cách — KH người Nhật "
     "gõ IME mặc định ra full-width space, xác suất gặp RẤT CAO』\n"
     "• r58 (Enter + dấu cách full-width) — kết quả **NG**\n"
     "• r40 (full-width space ở đầu/cuối), r41 (trộn 2 loại space), r27 (email + full-width "
     "space) — CHƯA có kết quả ở bất kỳ cột ticket nào\n"
     "r40 nêu rõ cơ chế:『Nếu full-width space bị trị như dấu tách và sinh fragment rỗng → "
     "LIKE %% → khớp TOÀN BỘ 4.500 friend → TÁI HIỆN ĐÚNG BUG #38866』",
     "web/logic-spec.md:395 —『Tách keyword theo space, search OR trên...』— KHÔNG nói rõ "
     "『space』gồm những ký tự nào (half-width U+0020, full-width U+3000, tab...), cũng không "
     "nói xử lý mảnh rỗng khi có nhiều dấu cách liên tiếp.",
     "Bug #38951 đang mở và nằm ĐÚNG trên cơ chế đã sinh ra bug KH #38866. Ba dòng chưa chạy "
     "(r40, r41, r27) chính là các biến thể nguy hiểm nhất của cùng cơ chế — nếu chỉ fix riêng "
     "case r39 mà không xử lý mảnh rỗng thì bug vẫn tái phát ở đầu/cuối chuỗi. Spec không định "
     "nghĩa tập ký tự phân tách nên Dev và Tester không có mốc chung để đối chiếu.",
     "Nhóm『Tìm kiếm theo từ khoá』: TC dấu cách full-width giữa 2 từ · full-width space đầu/cuối · "
     "trộn 2 loại space · Enter với keyword có dấu cách · keyword email có dấu cách thừa",
     "",
     ""],

    ["MT-07", "TRUNG BÌNH", W,
     "Biên hiển thị checkbox「条件に当てはまる友だち{N}人全員を選択」và hành vi khi bỏ tích "
     "1 friend lẻ",
     "Tab「#38866」:\n"
     "• r60 (kết quả search = 200):『Expect: checkbox KHÔNG hiển thị / Panel hiển thị 選択中 "
     "200人』kèm ghi chú『⏳ Cần confirm TA — biên hiển thị khi >200 hay ≥200』\n"
     "• r61 (= 201): checkbox HIỂN THỊ\n"
     "• r71 (tích checkbox rồi bỏ tích 1 friend lẻ):『⚠ Cần confirm spec: Expect panel hiện "
     "選択中 311人 và số friend nhận action = 311, HOẶC checkbox tự bỏ tích / Nếu vẫn giữ "
     "trạng thái chọn-all → friend đã bỏ tích VẪN nhận action → LỖI』kèm『⏳ Cần confirm TA』",
     "Spec KHÔNG có checkbox này. ui/ui-spec.md:74 và feature-spec.md §2 chỉ mô tả checkbox "
     "「全選択」và panel「友だち一括アクション」với counter「選択中 {N}人」. "
     "feature-spec.md §9 Gaps #1 ghi『Nút「アクション選択」— chưa mở xem danh sách actions』, "
     "tức phần bulk action panel mới chỉ được quan sát bề mặt.",
     "Đây vừa là spec BỎ SÓT (một checkbox điều khiển phạm vi của toàn bộ bulk action mà spec "
     "không hề ghi) vừa là 2 câu hỏi hành vi chưa ai chốt. Hậu quả trực tiếp: (a) biên 200 vs "
     "201 quyết định user có được chọn quá 1 trang hay không; (b) nếu bỏ tích 1 friend lẻ mà "
     "trạng thái chọn-all vẫn giữ thì friend đó vẫn nhận action — user thấy mình đã loại người "
     "đó ra nhưng hệ thống vẫn gửi.",
     "Nhóm『Chọn friend & checkbox 全選択』: TC biên hiển thị checkbox 199/200/201 · TC tích "
     "checkbox rồi bỏ tích 1 friend lẻ",
     "",
     ""],

    ["MT-08", "TRUNG BÌNH", W,
     "Keyword tìm kiếm có bị TÁCH theo dấu cách không, hay LIKE nguyên chuỗi? "
     "Spec tự mâu thuẫn + nghiệp vụ chưa chốt",
     "Tab「#38866」:\n"
     "• r35 (keyword「6期生 太郎」):『Lúc đếm và lúc job chạy phải tách keyword GIỐNG NHAU "
     "(cùng tách theo space, hoặc cùng LIKE nguyên chuỗi)』kèm ghi chú『⏳ Cần confirm TA — "
     "web tách theo space, check job có tách giống không』\n"
     "• r42 (friend tên đúng là「山田 太郎」):『⚠ Cần confirm nghiệp vụ: user muốn tìm ĐÚNG "
     "friend tên 山田 太郎 hay tìm tất cả friend có 山田 HOẶC 太郎?』kèm『⏳ Cần confirm BA/KH』, "
     "CHƯA có kết quả test\n"
     "• r48:『・là ký tự phân cách thường gặp trong tên người Nhật → check có bị coi là dấu "
     "tách không』",
     "• web/logic-spec.md:395 —『Keyword search: TÁCH KEYWORD THEO SPACE, search OR trên "
     "line_user.name, line_user.email, line_user.view_name』\n"
     "• feature-spec.md §2『Luồng end-to-end: Tìm kiếm』—『searchLineUser(): line_user.name "
     "LIKE %keyword%』(LIKE NGUYÊN CHUỖI, không tách)",
     "Hai file spec của cùng một tính năng mô tả 2 thuật toán khác nhau cho cùng ô tìm kiếm. "
     "Khác biệt nhìn thấy được: với keyword「山田 太郎」, tách-theo-space cho ra tất cả friend có "
     "山田 HOẶC 太郎 (có thể hàng trăm người), LIKE nguyên chuỗi chỉ cho ra friend tên đúng "
     "「山田 太郎」. Nếu tầng ĐẾM và tầng JOB dùng 2 thuật toán khác nhau thì số N khác số friend "
     "thực tế nhận action — lại đúng lớp bug #38866. Ngoài kỹ thuật còn cần chốt NGHIỆP VỤ: "
     "KH mong đợi hành vi nào.",
     "Nhóm『Tìm kiếm theo từ khoá』: TC keyword 1 dấu cách giữa 2 từ · TC friend có tên chứa "
     "dấu cách「山田 太郎」· TC ký tự đặc biệt tiếng Nhật (「・」) · TC trộn 2 loại dấu cách · "
     "TC email có dấu cách thừa",
     "",
     ""],

    ["MT-09", "THẤP", W,
     "Cơ chế ẩn bạn bè (非表示) được kích hoạt từ đâu? — TC LẤP GAP #7 của spec",
     "Tab「Testcase」r39:『Check random 1 số action của tính năng khác → Action ẩn friend → "
     "Ẩn được friend / Màn chat 1:1 không có message ẩn friend』— kết quả OK step.\n"
     "Tab「Testcase」r118, r119: action ẩn friend chạy QUA JOB thì chat 1:1 LẠI hiển thị "
     "message ẩn friend kèm tên user thao tác.\n"
     "→ Ẩn bạn bè là MỘT LOẠI ACTION trong bulk action của màn friendlist.\n"
     "Tab「ESticsearch」r283 xác nhận chiều ngược lại:『bỏ ẩn friend → nhấn bỏ ẩn ở màn "
     "/basic/friendlist/hidden → {\"is_hide\":0}』",
     "feature-spec.md §9 Gaps #2 —『Cơ chế trigger ẩn bạn bè (非表示) — KHÔNG thấy nút「非表示」"
     "trên SCR-FRL-01 hay SCR-FRL-03. Mức độ: Trung bình. Đề xuất: Kiểm tra FA-001 (Chat) hoặc "
     "bulk action』\n"
     "ui/ui-spec.md『Flow 5: Ẩn và hiện lại bạn bè』—『(Cơ chế ẩn chưa rõ — có thể từ bulk "
     "action hoặc action khác trên chi tiết)』",
     "Không phải mâu thuẫn mà là SPEC BỎ SÓT có thể đóng ngay: TC gốc đã chứng minh ẩn friend "
     "là một action trong danh sách bulk action của màn friendlist, và đã có kết quả test OK. "
     "Đưa vào bảng vì cần Leader duyệt việc cập nhật spec (đóng Gaps #2 và sửa Flow 5 của "
     "ui-spec).",
     "Nhóm『Bulk action — các loại action』: TC action ẩn friend. "
     "Nhóm『Màn 非表示中の友だち』: TC nút 再表示 · TC bulk 再表示. "
     "Nhóm『Đồng bộ Elasticsearch』: TC bỏ ẩn friend.",
     "",
     ""],

    ["MT-10", "THẤP", W,
     "Nút「アクション選択」mở ra những action nào? — TC LẤP GAP #1 của spec",
     "Tab「Testcase」r35-r43 liệt kê 13 loại action chạy được từ màn friendlist, mỗi loại có "
     "kết quả mong đợi riêng và đều đã test OK step:\n"
     "send text · send template · start/stop scenario · start/stop remind · ẩn friend · "
     "block friend · unhide · unblock · gắn tag · gán richmenu · ghi friend info · bookmark · "
     "gán 対応ステータス.\n"
     "r126 bổ sung:『CHeck send các action khác (tag, friend info, add rich menu ...) → Send "
     "được action cho user bình thường』",
     "feature-spec.md §9 Gaps #1 —『Nút「アクション選択」trong bulk action panel — CHƯA MỞ XEM "
     "danh sách actions. Mức độ: Trung bình. Đề xuất: Thu thập — mở dropdown/modal, ghi nhận "
     "danh sách actions』\n"
     "ui/ui-spec.md:120 —『Nút「アクション選択」: Mở dropdown/modal chọn action — chưa mở để xem "
     "nội dung』\n"
     "feature-spec.md §8 —『SC-004 Action Settings: Component chọn action cho bulk operation — "
     "SCR-FRL-01「アクション選択」(cần xác nhận)』",
     "SPEC BỎ SÓT có thể đóng ngay bằng dữ liệu đã có. Đưa vào bảng vì Leader cần duyệt: "
     "(a) cập nhật spec đóng Gaps #1; (b) xác nhận nút「アクション選択」đúng là SC-004 hay là "
     "danh sách rút gọn riêng của màn friendlist — điều này quyết định phạm vi TC nào thuộc "
     "FA-013 và phạm vi nào thuộc feature SC-004 tách riêng.",
     "Toàn bộ nhóm『Bulk action — các loại action』(6 TC) và nhóm『Màn danh sách — hiển thị』: "
     "TC panel 友だち一括アクション",
     "",
     ""],

    ["MT-11", "TRUNG BÌNH", W,
     "Quy tắc tự động xác nhận tin nhắn (bot bật confirm_message_user_send) khi chạy action "
     "từ friendlist — spec không ghi",
     "Tab「Testcase」r84-r91 và r120-r126, r130 mô tả quy tắc đầy đủ, đã test OK step:\n"
     "• Bot TẮT auto-confirm: gửi action text / template / action khác → KHÔNG đổi trạng thái "
     "xác nhận, số 未確認 của bot không đổi\n"
     "• Bot BẬT auto-confirm + action text hoặc template: friend đang『chưa xác nhận』chuyển "
     "thành『đã xác nhận』, số 未確認 của bot GIẢM; friend đang『đã xác nhận』giữ nguyên\n"
     "• Bot BẬT auto-confirm + action KHÔNG phải text/template (start scen, start remind, "
     "add tag, add info): KHÔNG đổi trạng thái, số 未確認 không đổi\n"
     "• r90 (nhiều friend cùng lúc) và r130 (qua job có filter) CHỈ CÓ TIÊU ĐỀ, không có "
     "kết quả mong đợi",
     "spec-features/admin/friend-list/ KHÔNG có quy tắc nào về auto-confirm khi chạy action. "
     "Chuỗi `confirm_message_user_send` grep ra 0 kết quả. Spec chỉ nhắc `count_user_unconfirm` "
     "ở 3 luồng khác: block (feature-spec.md:258), xoá (:280), bỏ block (:368) — "
     "web/api-spec.md:465 và :724 cũng chỉ nói『Cập nhật count_user_unconfirm』ở 2 luồng đó.",
     "SPEC BỎ SÓT một quy tắc có tác động nhìn thấy được: badge số 未確認 trên menu là thứ "
     "Admin dùng để biết còn bao nhiêu hội thoại chưa xử lý. Nếu chạy bulk action cho 5.000 "
     "friend mà quy tắc auto-confirm sai thì badge nhảy sai hàng nghìn đơn vị. Ngoài ra 2 dòng "
     "r90/r130 chỉ có tiêu đề → kho phải TỰ VIẾT kết quả mong đợi bằng cách suy rộng quy tắc "
     "của r87-r89 (có ghi rõ ở Ghi chú của TC), cần Leader xác nhận trước khi khoá.",
     "Toàn bộ 5 TC bộ đếm 未確認 trong nhóm『Bulk action — last message & bộ đếm 未確認』",
     "",
     ""],

    ["MT-12", "TRUNG BÌNH", W,
     "Phân quyền staff trên màn friendlist có được enforce ở TẦNG API không? — vùng mù "
     "giữa TC và spec",
     "TCsLine_Improve chung → tab「Phân quyền」(34 dòng, TC dùng chung cho mọi màn của tool) "
     "CHỈ kiểm ở tầng giao diện:\n"
     "• r4-r5: hover vào mục menu bị khoá → hiện text「操作できません。/ この機能の操作権限が"
     "付与されていません。/ 主管理者に操作権限を付与してもらうことで操作が可能となります。」, "
     "text bám đúng vị trí khi cuộn trang\n"
     "• r7, r9, r12, r14: với từng role (副管理者 · 運用者) → không click được vào màn không "
     "có quyền, click được vào màn có quyền\n"
     "KHÔNG có dòng nào gọi thẳng API bằng phiên đăng nhập của staff không có quyền.",
     "feature-spec.md §9 Gaps #7 —『Staff permissions — controller KHÔNG có middleware phân "
     "quyền riêng. Đề xuất: Kiểm tra route middleware group + Blade views @can/@role』\n"
     "web/api-spec.md『Middleware chung』—『Tất cả endpoints: web, "
     "NotifyChatworkRequestTimeSlow, LogRequestMultipart』— cả 3 đều KHÔNG phải middleware "
     "phân quyền.\n"
     "feature-spec.md §1 bảng Actors —『Staff: Tương tự Admin, giới hạn theo quyền (chưa xác "
     "nhận chi tiết — xem Gaps #7)』",
     "VÙNG MÙ giữa 2 nguồn: TC chỉ chứng minh UI ẩn menu, spec tự thừa nhận chưa xác nhận có "
     "middleware nào chặn ở tầng server. Nếu quả thật không có middleware thì staff bị tắt "
     "quyền vẫn có thể gọi thẳng post-advance-filter-v2 để đọc toàn bộ danh sách bạn bè, hoặc "
     "gọi delete-user-block để xoá friend — UI ẩn menu không phải là kiểm soát truy cập. "
     "FA-013 lại là màn nắm dữ liệu cá nhân của toàn bộ friend nên mức rủi ro cao hơn các màn "
     "khác. Kho đã ĐỀ XUẤT 1 TC mới ở tầng API (không có trong corpus) — cần Leader duyệt.",
     "Nhóm『Phân quyền & môi trường』: TC staff không có quyền gọi thẳng API (TC do AI đề xuất) · "
     "TC staff không có quyền — menu bị khoá · TC staff có quyền",
     "",
     ""],

    ["MT-13", "THẤP", W,
     "Giá trị `type` của bản ghi đồng bộ Elasticsearch khi XOÁ bạn bè: 2 hay 11?",
     "TCsLine_Improve chung → tab「ESticsearch」r4:『Delete Line user → Xóa ở mypage và friend "
     "list → Tạo bản ghi trong bảng sync_esticsearch, **type=2**, data_sync NULL』— kết quả "
     "test OK, cột Note ghi lại『data_sync NULL』.",
     "feature-spec.md §7.2 bảng『Type values liên quan Friend List』:\n"
     "• TYPE_BOT_LINE_USER = 0 (hide/unhide)\n"
     "• TYPE_LINE_USER = 1 (cập nhật tên)\n"
     "• TYPE_CONVERSATION = **2** (thay đổi conversation)\n"
     "• TYPE_TAG = 3 · TYPE_FRIEND_INFO = 4\n"
     "• TYPE_DELETE_LINE_USER = **11** (xoá user → Delete document)\n"
     "feature-spec.md §2『Luồng xoá bạn bè』bước 6 —『Ghi sync_elasticsearch "
     "(TYPE_DELETE_LINE_USER = 11)』",
     "Hai nguồn ghi 2 con số khác nhau cho cùng thao tác xoá, và con số của TC (2) lại trùng "
     "với mã dành cho thao tác KHÁC trong spec (TYPE_CONVERSATION). Mức độ thấp vì không nhìn "
     "thấy trực tiếp bằng mắt trên giao diện, nhưng nếu TC đúng thì tài liệu ES sai và người "
     "test sau sẽ kiểm nhầm mã; nếu spec đúng thì TC gốc đã ghi sai từ 1 lần chạy cũ. "
     "Cần Dev xác nhận giá trị enum hiện hành. Lưu ý tên bảng cũng lệch: TC ghi "
     "`sync_esticsearch`, spec ghi `sync_elasticsearch`.",
     "Nhóm『Đồng bộ Elasticsearch』: TC xoá friend → hàng đợi đồng bộ",
     "",
     ""],

    ["MT-14", "TRUNG BÌNH", W,
     "Action block / ẩn friend: chạy TRỰC TIẾP thì chat 1:1 KHÔNG có message, chạy QUA JOB "
     "thì LẠI CÓ",
     "Tab「Testcase」— cùng loại action, 2 kết quả ngược nhau:\n"
     "• Chạy trực tiếp (≤ 200 friend) — r39:『Action ẩn friend → Ẩn được friend / Màn chat 1:1 "
     "KHÔNG có message ẩn friend』; r40:『Action block friend → Block được friend / Màn chat 1:1 "
     "KHÔNG có message block friend』\n"
     "• Chạy qua job (> 200 friend, action schedule tạo từ friendlist) — r116-r117:『Check "
     "action block friend → Check trigger ở chat 1:1 → Màn chat 1:1 HIỆN message block friend, "
     "Tên user thao tác là user chính / user staff』; r118-r119: tương tự cho action ẩn friend\n"
     "• Đối chứng ngược lại — r137, r138 (action schedule tạo TAY ở màn "
     "アクションスケジュール実行):『Action block friend → KHÔNG tạo message trigger block friend』; "
     "『Action ẩn friend → KHÔNG tạo message trigger ẩn friend』\n"
     "→ 3 đường đi cho cùng 1 action, 2 kết quả khác nhau. Tất cả đều đánh OK.",
     "spec-features/admin/friend-list/ KHÔNG mô tả message trigger ở màn chat 1:1 cho action "
     "block/ẩn. feature-spec.md §2『Luồng block bạn bè』(EP-31) liệt kê 5 bước cập nhật DB "
     "nhưng không nhắc việc tạo message; chỉ luồng BỎ block (:368) mới ghi rõ『messages_v2s "
     "(INSERT)』.",
     "Cùng một action, cùng một màn khởi phát, chỉ khác ở chỗ số friend vượt hay không vượt "
     "ngưỡng 200 — nhưng lịch sử hội thoại mà Admin nhìn thấy lại khác nhau. Nếu là cố ý thì "
     "spec phải ghi rõ để tester không báo nhầm bug; nếu không cố ý thì đây là bug hiển thị: "
     "cùng thao tác mà lịch sử chat lúc có lúc không, làm Admin không truy được ai đã block "
     "friend khi số lượng nhỏ. Đường thứ 3 (action schedule tạo tay) lại giống đường trực tiếp, "
     "càng cho thấy quy tắc chưa nhất quán.",
     "Nhóm『Bulk action — các loại action』: TC action ẩn friend · TC action block friend. "
     "Nhóm『Bulk action — trigger & profile gửi』: TC action block/ẩn qua job · TC regression "
     "action schedule tạo tay.",
     "",
     ""],
]
