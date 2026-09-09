# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 3: gửi text, friend info, shorten URL, media, PDF, sticker, template, multi action."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3, đang mở hội thoại friend A"
NOPREV = BOT + "\n- Cài đặt chat: TẮT 送信プレビュー (gửi thẳng, không qua preview)"
PREV = BOT + "\n- Cài đặt chat: BẬT 送信プレビュー (hiện preview trước khi gửi)"
INFOSET = ("- Friend A đã có giá trị cho: システム表示名, SĐT, email, sinh nhật, tỉnh (5 info địa chỉ id -6..-10)\n"
           "- Friend A có friend info tự tạo đủ 6 kiểu: lựa chọn / ký tự / ngày / ảnh / PDF / điểm")
LASTMSG = ("Theo SpecImprove #35389 (4/2026): KHÔNG update tin nhắn cuối của bạn bè\n"
           "- conversation.last_time_message KHÔNG đổi\n"
           "- conversation.last_message KHÔNG đổi\n"
           "- Dòng bạn bè ở danh sách KHÔNG nhảy vị trí")
MT01 = ("MT-01: spec feature-spec.md:57 + db-mapping.md:879 vẫn ghi UPDATE conversation(last_message, last_time_message) "
        "khi admin gửi tin — TC theo SpecImprove #35389 (4/2026) nói NGƯỢC LẠI. Dự kiến FAIL nếu code chưa fix → raise bug.")

S3 = [
    # ═══════════════ Gửi text & phím tắt ═══════════════
    tc("Gửi text & phím tắt", "MSG-001", "Normal",
       "Gửi tin nhắn text — latinh, tiếng Nhật, xuống dòng đều gửi được và hiển thị 2 phía",
       NOPREV,
       "1. Với mỗi nội dung ở cột Dữ liệu test: gõ vào ô nhập, bấm nút gửi\n"
       "2. Quan sát bong bóng tin nhắn ở chat 1:1\n3. Kiểm tra tin nhắn trên app LINE của friend A",
       "`Hello LME test` (latinh) · `テストメッセージです` (tiếng Nhật) · text 3 dòng có xuống dòng · "
       "chỉ emoji · text + emoji (emoji trước / emoji sau)",
       "- Tất cả nội dung đều gửi thành công\n"
       "- Chat 1:1 hiển thị đúng nguyên văn, giữ đúng xuống dòng và emoji\n"
       "- App LINE của friend A nhận đúng nội dung tương ứng",
       note="Gộp vì cùng kết quả. Đi tới output cuối app LINE (RULE-06). "
            "Nguồn: Content: Send message r11-r13, r36, r42, r43"),

    tc("Gửi text & phím tắt", "DATA-001", "Normal",
       "Gửi text từ LME — KHÔNG cập nhật tin nhắn cuối của bạn bè",
       NOPREV + "\n- Ghi lại nội dung + thời gian tin nhắn cuối của friend A ở danh sách và trong DB",
       "1. Ghi lại conversation.last_message và last_time_message của A\n"
       "2. Gửi 1 tin text từ chat 1:1\n"
       "3. Quan sát dòng của A ở danh sách bạn bè (không reload)\n"
       "4. Kiểm tra lại last_message và last_time_message trong DB",
       "Tin nhắn `khong-update-last-message`",
       LASTMSG,
       spec="Đã hỏi leader", note=MT01 + " Nguồn: Content: Send message r32-r35, r302"),

    tc("Gửi text & phím tắt", "DATA-001", "Normal",
       "Bạn bè gửi tin đến bot — CÓ cập nhật tin nhắn cuối",
       BOT,
       "1. Ghi lại last_message + last_time_message của friend A\n"
       "2. Cho friend A gửi lần lượt từng loại ở cột Dữ liệu test tới bot\n"
       "3. Sau mỗi lần: quan sát dòng A ở danh sách và kiểm tra DB",
       "text · sticker · ảnh · video · audio · file · bấm nút của template có gửi tin dạng text button · "
       "gửi danh thiếp LINE · gửi vị trí",
       "- Với TẤT CẢ: conversation.last_message và last_time_message ĐƯỢC cập nhật\n"
       "- Dòng A ở danh sách hiện nội dung và thời gian tin mới nhất, nhảy lên đầu danh sách",
       note="Gộp 9 điểm vì cùng kết quả. Cặp đối lập với TC trên. Nguồn: Content: Send message r303-r311"),

    tc("Gửi text & phím tắt", "DATA-001", "Normal",
       "Mọi đường gửi tin từ LME (web) đều KHÔNG cập nhật tin nhắn cuối",
       BOT + "\n- Đã chuẩn bị: template, broadcast, scenario, remind, tag có action, form, salon/lesson/event booking",
       "1. Với mỗi đường gửi ở cột Dữ liệu test: thực hiện gửi cho friend A\n"
       "2. Sau mỗi lần: kiểm tra friend A nhận được tin trên app LINE\n"
       "3. Kiểm tra conversation.last_message và last_time_message của A không đổi",
       "Đặt lịch gửi ở chat 1:1 · send test ở Template / Broadcast / Scenario (1 step và toàn bộ) / Remind · "
       "trả lời ở màn talk list · remind gửi ngay · action text độc lập của salon, lesson, kết bạn (mới/cũ/unblock), "
       "QR landing, form (submit và chẩn đoán) · form gửi bản sao câu trả lời · action gắn tag và action limit tag · "
       "kết bạn lại của old friend",
       "- TẤT CẢ: friend A nhận được tin trên app LINE\n"
       "- TẤT CẢ: last_message và last_time_message của A KHÔNG thay đổi",
       spec="Đã hỏi leader",
       note=MT01 + " Gộp ~20 đường gửi vì cùng kết quả. Nguồn: Content: Send message r312-r334",),

    tc("Gửi text & phím tắt", "SYNC-APP-001", "Normal",
       "Gửi tin từ APP MOBILE và từ JOB — cũng KHÔNG cập nhật tin nhắn cuối",
       "- App mobile LME đăng nhập account admin bot A\n- Có scenario/broadcast/action schedule đã cấu hình cho friend A",
       "1. Ở app mobile: gửi text, media, sticker, template, đặt lịch gửi, action gắn tag, thao tác salon/lesson\n"
       "2. Qua job: gửi action text và action template ở màn friend list (gửi thường và qua action schedule)\n"
       "3. Chạy thêm 2-3 tính năng gửi qua job khác: Broadcast, Scenario, Event remind\n"
       "4. Sau mỗi lần: kiểm tra friend nhận tin và kiểm tra last_message/last_time_message",
       "App: text · media · sticker · template · đặt lịch · action tag · salon · lesson\n"
       "Job: friend list action text/template/nhiều action, action schedule, Broadcast, Scenario, Event remind",
       "- TẤT CẢ: friend nhận được tin\n- TẤT CẢ: last_message và last_time_message KHÔNG đổi",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=MT01 + " Job → RULE-08 bắt buộc PRODUCTION. Nguồn: Content: Send message r335-r350"),

    tc("Gửi text & phím tắt", "UI-INPUT-001", "Normal",
       "Phím tắt gửi — theo cài đặt 送信ショートカット",
       BOT,
       "1. Ở màn cài đặt chat, đặt 送信ショートカット = Shift+Enter gửi → quay lại chat, gõ text và bấm Enter, rồi Shift+Enter\n"
       "2. Đổi cài đặt sang Enter gửi → gõ text và bấm Enter, rồi Shift+Enter",
       "2 cấu hình phím tắt × 2 tổ hợp phím",
       "- Cấu hình Shift+Enter gửi: Enter xuống dòng, Shift+Enter gửi tin\n"
       "- Cấu hình Enter gửi: Enter gửi tin, Shift+Enter xuống dòng\n"
       "- Tin gửi thành công, friend nhận được trên app LINE",
       note="Mỗi cấu hình có kết quả phím khác nhau nhưng cùng 1 chuỗi kiểm chứng. "
            "Nguồn: Content: Send message r156, r157 + spec feature-spec.md:207"),

    tc("Gửi text & phím tắt", "DATA-TEXT-001", "Abnormal",
       "Chọn gợi ý bàn phím tiếng Nhật rồi gửi — gửi đúng text đã chọn, không phải text đang gõ",
       BOT + "\n- Bật bộ gõ tiếng Nhật (IME)",
       "1. Gõ `なにとぞ` vào ô nhập\n2. Chọn gợi ý `何卒宜しくお願いします` bằng phím Tab/Space/mũi tên\n"
       "3. Gửi bằng cách ở cột Dữ liệu test\n4. Kiểm tra nội dung tin ở chat 1:1 và trên app LINE\n"
       "5. Lặp lại nhưng chọn gợi ý bằng CLICK CHUỘT",
       "Chọn gợi ý bằng phím và bằng chuột × gửi bằng: click nút gửi / Enter / Shift+Enter / qua preview",
       "- Cả 8 tổ hợp: tin gửi đi đúng `何卒宜しくお願いします` (text đã chọn từ gợi ý)\n"
       "- KHÔNG gửi nhầm `なにとぞ` hay text dở dang\n- Chat 1:1 và app LINE đều đúng",
       note="Gộp 8 tổ hợp vì cùng kết quả. Nguồn: Content: Send message r155-r162"),

    tc("Gửi text & phím tắt", "DATA-TEXT-001", "Abnormal",
       "Nhập rồi xoá rồi nhập lại / nhập text dài / dán text dài — gửi đúng nội dung cuối cùng",
       BOT,
       "1. Gõ text A, xoá hết, gõ text B → gửi bằng 4 cách (nút / Enter / Shift+Enter / preview)\n"
       "2. Gõ tay 1 đoạn text dài (>500 ký tự) → gửi bằng 4 cách\n"
       "3. Dán (paste) 1 đoạn text dài → gửi bằng 4 cách",
       "3 kịch bản × 4 cách gửi",
       "- Mọi tổ hợp: nội dung gửi đúng bằng nội dung đang có trong ô nhập tại thời điểm gửi\n"
       "- Text dài không bị cắt, hiển thị đủ ở chat 1:1 và app LINE",
       note="Gộp 12 tổ hợp vì cùng kết quả. Nguồn: Content: Send message r163-r174"),

    tc("Gửi text & phím tắt", "STATE-001", "Normal",
       "Gõ text chưa gửi rồi chuyển sang bạn bè khác và quay lại — giữ lại nội dung đang gõ",
       BOT,
       "1. Ở hội thoại friend A: gõ `何卒宜しくお願いします` (chọn từ gợi ý IME), KHÔNG gửi\n"
       "2. Click sang hội thoại friend B\n3. Quay lại hội thoại friend A\n4. Quan sát ô nhập",
       "Text chọn từ gợi ý IME",
       "- Ô nhập của A vẫn giữ đúng text `何卒宜しくお願いします`\n"
       "- Text không còn gạch chân của IME (đã xác định xong)",
       note="Nguồn: Content: Send message r197"),

    tc("Gửi text & phím tắt", "STATE-001", "Boundary",
       "Lưu nháp nội dung đang gõ — tối đa 3 hội thoại",
       BOT + "\n- Có ≥5 friend trong danh sách",
       "1. Gõ nội dung khác nhau (không gửi) cho 3 friend liên tiếp F1, F2, F3\n"
       "2. Quay lại từng friend kiểm tra nội dung còn giữ\n"
       "3. Gõ tiếp cho friend thứ 4 (F4)\n4. Quay lại F1 kiểm tra\n"
       "5. Lặp lại với 4 friend KHÔNG liên tiếp (xen kẽ friend khác)",
       "Nội dung nháp cho F1, F2, F3, F4",
       "- Sau bước 2: cả 3 friend đều giữ đúng nội dung đang gõ\n"
       "- Sau bước 4: nội dung nháp của F1 (friend gõ đầu tiên) BỊ XOÁ; F2, F3, F4 vẫn giữ\n"
       "- Kết quả giống nhau dù gõ liên tiếp hay không liên tiếp",
       spec="Spec không ghi",
       note="Spec chat-11 không mô tả cơ chế lưu nháp này. Nguồn: Content: Send message r280-r282"),

    tc("Gửi text & phím tắt", "MSG-004", "Abnormal",
       "Gửi tin cho bạn bè đã block — bị chặn, không có nút gửi",
       BOT + "\n- Friend V: bot đã block\n- Friend W: đã block bot",
       "1. Mở hội thoại của V, quan sát khu vực nhập tin và nút gửi\n"
       "2. Hover vào vị trí nút gửi\n3. Lặp lại với W\n"
       "4. Nếu gửi được: kiểm tra thông báo lỗi",
       "V (bot block friend) · W (friend block bot)",
       "- Cả 2: KHÔNG hiện nút gửi tin nhắn, không hiện tooltip\n"
       "- Nếu vẫn gọi được API gửi: trả lỗi「ブロックしていますので、メッセージが送信できません。」",
       note="Khớp spec BR-09 (feature-spec.md:471). Nguồn: Content: Send message r1221, r1222"),

    tc("Gửi text & phím tắt", "CONC-001", "Abnormal",
       "Double click nút gửi — chỉ gửi 1 tin nhắn",
       NOPREV,
       "1. Gõ tin nhắn `double-click-test`\n2. Double click nhanh nút gửi\n"
       "3. Đếm số bong bóng tin ở chat 1:1\n4. Đếm số tin friend nhận trên app LINE\n"
       "5. Kiểm tra Network chỉ có 1 request",
       "Double click trong < 300ms",
       "- Chat 1:1 chỉ có 1 bong bóng tin\n- Friend chỉ nhận 1 tin trên app LINE\n- Chỉ 1 request gửi",
       note="Nguồn: Content: Send message r272 + Improve socket r7"),

    tc("Gửi text & phím tắt", "UI-002", "Normal",
       "Tooltip nút gửi khi BẬT 送信プレビュー",
       PREV,
       "1. Chưa nhập gì: hover vào nút gửi → đọc tooltip\n2. Nhập text: hover lại → đọc tooltip\n"
       "3. Chọn media rồi hover → đọc tooltip\n4. Chọn PDF rồi hover → đọc tooltip",
       "4 trạng thái ô nhập, cài đặt preview BẬT",
       "- Cả 4 trường hợp đều hiện tooltip「プレビューを確認後、送信」",
       note="Nguồn: Content: Send message r1212-r1215 (SpecImprove #34297 02/2026)"),

    tc("Gửi text & phím tắt", "UI-002", "Normal",
       "KHÔNG hiện tooltip nút gửi khi TẮT 送信プレビュー",
       NOPREV,
       "1. Chưa nhập gì: hover nút gửi\n2. Nhập text: hover lại\n3. Chọn media: hover\n4. Chọn PDF: hover",
       "4 trạng thái ô nhập, cài đặt preview TẮT",
       "- Cả 4 trường hợp đều KHÔNG hiện tooltip「プレビューを確認後、送信」",
       note="Cặp đối lập với TC trên → 2 TC riêng. Nguồn: Content: Send message r1216-r1219"),

    # ═══════════════ Chèn friend info vào tin nhắn ═══════════════
    tc("Chèn friend info vào tin nhắn", "MSG-005", "Normal",
       "Chèn friend info vào text — thay thế đúng giá trị ở cả chat 1:1 và app LINE",
       NOPREV + "\n" + INFOSET,
       "1. Soạn tin có chèn mã của từng nhóm info ở cột Dữ liệu test\n2. Gửi cho friend A\n"
       "3. Kiểm tra nội dung hiển thị ở chat 1:1\n4. Kiểm tra nội dung trên app LINE của friend A",
       "Info mặc định: システム表示名 · SĐT · email · sinh nhật\n"
       "Info địa chỉ: 5 mã tỉnh/địa chỉ (id -6, -7, -8, -9, -10)\n"
       "Info tự tạo: kiểu lựa chọn · kiểu ký tự · kiểu ngày · ảnh · PDF · điểm",
       "- App LINE: mã được thay bằng ĐÚNG giá trị của friend A\n"
       "- Chat 1:1: tin nhắn hiển thị cũng đã được thay giá trị (không hiện mã thô)",
       note="Gộp 15 mã vì cùng kết quả. Nguồn: Content: Send message r14-r28"),

    tc("Chèn friend info vào tin nhắn", "MSG-005", "Abnormal",
       "Chèn friend info mà bạn bè CHƯA có giá trị — để trống, không hiện mã thô",
       NOPREV + "\n- Friend B chưa nhập SĐT và email; đã có システム表示名",
       "1. Soạn tin chèn cả 3 mã: システム表示名 + SĐT + email\n2. Gửi cho friend B\n"
       "3. Kiểm tra nội dung ở chat 1:1 và app LINE\n"
       "4. Gửi tin CHỈ chèn các mã friend B không có giá trị",
       "Friend B: có システム表示名, thiếu SĐT và email",
       "- Mã có giá trị được thay bình thường; mã KHÔNG có giá trị để TRỐNG\n"
       "- KHÔNG hiện mã thô kiểu `[FRIEND_INFO_phone]` ở cả chat 1:1 và app LINE\n"
       "- Trường hợp toàn bộ mã đều không có giá trị: tin nhắn vẫn gửi được, phần chèn để trống",
       note="Nguồn: Content: Send message r29, r30, r219, r220"),

    tc("Chèn friend info vào tin nhắn", "DATA-REF-001", "Abnormal",
       "Chèn friend info ĐÃ BỊ XOÁ khỏi hệ thống — để trống, không hiện mã thô",
       NOPREV + "\n- Friend info tự tạo I1 đã bị xoá ở màn Quản lý thông tin bạn bè\n- Friend info I2 vẫn còn và friend A có giá trị",
       "1. Soạn tin chèn cả mã của I1 (đã xoá) và I2 (còn)\n2. Gửi cho friend A\n"
       "3. Kiểm tra nội dung ở chat 1:1 và app LINE",
       "I1 đã xoá · I2 còn giá trị",
       "- Mã của I1: để trống, không hiện mã thô, không lỗi\n- Mã của I2: thay đúng giá trị\n"
       "- Tin nhắn vẫn gửi thành công",
       note="Nguồn: Content: Send message r31, r221"),

    tc("Chèn friend info vào tin nhắn", "MSG-005", "Normal",
       "Gửi tin có chèn info cho 2 bạn bè liên tiếp — mỗi người nhận đúng giá trị của mình",
       NOPREV + "\n- Friend A và friend B đều có giá trị SĐT + システム表示名 KHÁC nhau",
       "1. Soạn tin chèn システム表示名 + SĐT, gửi cho friend A\n"
       "2. Click ngay sang friend B, soạn tin tương tự, gửi\n"
       "3. Kiểm tra nội dung ở chat 1:1 của A và của B\n4. Kiểm tra app LINE của A và của B",
       "A và B có giá trị info khác nhau",
       "- A nhận đúng giá trị của A; B nhận đúng giá trị của B\n"
       "- Không lẫn giá trị giữa 2 người ở cả chat 1:1 và app LINE\n"
       "- last_message của cả A và B đều KHÔNG bị cập nhật",
       spec="Đã hỏi leader",
       note=MT01 + " Nguồn: Content: Send message r82, r154, r621"),

    tc("Chèn friend info vào tin nhắn", "OUT-PREVIEW-001", "Normal",
       "Preview trước khi gửi — hiển thị text GỐC (chưa thay giá trị), tin gửi đi thì đã thay",
       PREV + "\n" + INFOSET,
       "1. Soạn tin chèn mã friend info\n2. Bấm gửi → modal preview hiện ra\n"
       "3. Đọc nội dung trong modal preview\n4. Bấm gửi trong modal\n"
       "5. Kiểm tra nội dung ở chat 1:1 và trên app LINE",
       "Text chèn mã システム表示名 + SĐT",
       "- Modal preview hiển thị text GỐC còn nguyên mã (chưa thay giá trị)\n"
       "- Sau khi gửi: chat 1:1 và app LINE đều hiển thị nội dung ĐÃ THAY giá trị",
       note="Nguồn: Content: Send message r86-r100"),

    tc("Chèn friend info vào tin nhắn", "MSG-005", "Normal",
       "Gửi text chèn info kèm media/PDF — text thay giá trị đúng, media gửi bình thường",
       NOPREV + "\n" + INFOSET,
       "1. Soạn text có chèn mã friend info, đồng thời chọn 1 ảnh\n2. Bấm gửi\n"
       "3. Kiểm tra thứ tự và nội dung ở chat 1:1 và app LINE\n"
       "4. Lặp lại với video, audio, PDF",
       "Text chèn info + ảnh / video / audio / PDF",
       "- Text gửi TRƯỚC, media gửi sau\n- Text đã thay đúng giá trị info ở cả 2 phía\n"
       "- Media gửi thành công, friend mở/tải được",
       note="Gộp 4 loại media vì cùng kết quả. Nguồn: Content: Send message r56-r74, r443"),

    tc("Chèn friend info vào tin nhắn", "MSG-005", "Normal",
       "Chèn info khi gửi qua đặt lịch và qua reply — vẫn thay đúng giá trị",
       BOT + "\n" + INFOSET,
       "1. Đặt lịch gửi 1 tin có chèn mã info cho friend A, chờ tới giờ gửi\n"
       "2. Kiểm tra nội dung ở chat 1:1 và app LINE\n"
       "3. Quote 1 tin của friend A, soạn tin reply có chèn mã info, gửi\n"
       "4. Kiểm tra nội dung ở chat 1:1 và app LINE",
       "Cùng bộ mã info như TC gửi trực tiếp",
       "- Cả 2 đường (đặt lịch, reply): mã được thay đúng giá trị của friend A ở cả chat 1:1 và app LINE\n"
       "- Info không có giá trị / đã bị xoá thì để trống, không hiện mã thô",
       note="Nguồn: Content: Send message r249-r270, r275"),

    # ═══════════════ Shorten URL ═══════════════
    tc("Shorten URL", "MSG-003", "Normal",
       "Gửi các loại URL của LME trong tin nhắn text — friend mở được đúng trang",
       NOPREV + "\n- Đã tạo sẵn: 1 form, 1 lịch calendar booking, 1 salon booking, 1 event booking",
       "1. Với mỗi loại URL ở cột Dữ liệu test: dán vào ô nhập và gửi cho friend A\n"
       "2. Trên app LINE: bấm vào link\n3. Kiểm tra trang mở ra",
       "URL thường (ví dụ https://example.com) · URL form · URL calendar booking · URL salon booking · URL event booking",
       "- Tất cả gửi thành công, friend bấm vào mở đúng trang tương ứng\n"
       "- URL của LME mở đúng form/lịch booking của bot A",
       note="Gộp 5 loại vì cùng kết quả. Nguồn: Content: Send message r198-r202"),

    tc("Shorten URL", "MSG-003", "Normal",
       "BẬT 短縮URLの利用 — chat 1:1 hiện URL GỐC, app LINE nhận URL rút gọn",
       BOT + "\n- Cài đặt chat: BẬT 短縮URLの利用",
       "1. Dán 1 URL dài vào ô nhập, gửi cho friend A\n"
       "2. Đọc URL hiển thị trong bong bóng tin ở chat 1:1\n"
       "3. Đọc URL friend nhận trên app LINE\n4. Bấm vào URL trên app LINE",
       "URL `https://example.com/a-very-long-path?utm_source=test&utm_campaign=abc`",
       "- Chat 1:1 hiển thị URL GỐC (nguyên như đã nhập)\n"
       "- App LINE hiển thị URL RÚT GỌN (domain của tool)\n"
       "- Bấm URL rút gọn mở đúng trang đích ban đầu",
       spec="Đã hỏi leader",
       note="MT-13: spec BR-15 (feature-spec.md:477) chỉ nói URL được chuyển thành short URL, KHÔNG nói chat 1:1 "
            "vẫn hiện link gốc. Nguồn: Content: Send message r203, r545, r546, r1101-r1112"),

    tc("Shorten URL", "MSG-003", "Normal",
       "TẮT 短縮URLの利用 — cả chat 1:1 và app LINE đều giữ URL gốc",
       BOT + "\n- Cài đặt chat: TẮT 短縮URLの利用",
       "1. Dán URL dài vào ô nhập, gửi cho friend A\n2. Đọc URL ở chat 1:1\n"
       "3. Đọc URL friend nhận trên app LINE\n4. Bấm vào URL",
       "Cùng URL như TC trên",
       "- Chat 1:1: URL gốc\n- App LINE: URL gốc, KHÔNG bị rút gọn\n- Bấm vào mở đúng trang",
       note="Cặp đối lập → TC riêng. Nguồn: Content: Send message r226, r1112"),

    tc("Shorten URL", "MSG-005", "Normal",
       "Chèn friend info + URL rút gọn trong cùng 1 tin — cả 2 xử lý đúng",
       BOT + "\n" + INFOSET + "\n- Cài đặt chat: BẬT 短縮URLの利用",
       "1. Soạn tin có cả mã friend info và 1 URL dài\n2. Gửi cho friend A\n"
       "3. Kiểm tra chat 1:1: giá trị info và dạng URL\n"
       "4. Kiểm tra app LINE: giá trị info và dạng URL\n5. Lặp lại khi TẮT shorten",
       "Text = `{システム表示名} さん、こちら → https://example.com/very/long/path` + các mã info khác",
       "- BẬT shorten: chat 1:1 thay đúng giá trị info + hiện URL gốc; app LINE thay giá trị info + URL rút gọn\n"
       "- TẮT shorten: cả 2 phía đều thay giá trị info + URL gốc",
       note="Nguồn: Content: Send message r204-r248"),

    tc("Shorten URL", "MSG-003", "Normal",
       "Cài đặt shorten của Template và của chat 1:1 — quy tắc hiển thị nhất quán",
       BOT + "\n- Template T có URL và có cấu hình rút gọn riêng\n- Có cả 2 trạng thái cài đặt shorten ở chat 1:1",
       "1. Đặt chat 1:1 BẬT shorten: gửi template T (preview template, preview trước gửi, gửi thật, "
       "gửi qua multi action, gửi qua action từ nút bấm) → kiểm tra URL ở chat 1:1 và app LINE\n"
       "2. Đặt chat 1:1 TẮT shorten: lặp lại toàn bộ bước 1",
       "Template T có URL; 2 trạng thái cài đặt shorten × 5 đường gửi",
       "- Với MỌI tổ hợp: chat 1:1 và màn preview hiển thị URL GỐC\n"
       "- App LINE hiển thị theo cấu hình rút gọn của TEMPLATE, không phụ thuộc cài đặt shorten của chat 1:1",
       spec="Đã hỏi leader",
       note="MT-13. Gộp 10 tổ hợp vì cùng kết quả. Nguồn: Content: Send message r1101-r1110"),

    # ═══════════════ Gửi media ═══════════════
    tc("Gửi media", "UI-001", "Normal",
       "Mở chức năng gửi media — hiện popup định dạng hỗ trợ và màn phủ chọn file",
       BOT,
       "1. Hover vào nút gửi media, quan sát\n2. Click nút chữ i, đọc popup định dạng hỗ trợ\n"
       "3. Click nút gửi media, quan sát màn phủ chọn file",
       "Màn chat, chưa chọn file nào",
       "- Hover nút gửi media: có hiệu ứng, có gợi ý\n"
       "- Popup chữ i hiển thị danh sách định dạng file được hỗ trợ\n"
       "- Click nút gửi media: hiện màn phủ cho phép chọn hoặc kéo thả file",
       note="Nguồn: Content: Send message r394-r396"),

    tc("Gửi media", "MEDIA-001", "Normal",
       "Upload media hợp lệ — qua nút chọn file và qua kéo thả đều thành công",
       BOT,
       "1. Click nút gửi media → chọn từng file ở cột Dữ liệu test bằng hộp thoại chọn file\n"
       "2. Lặp lại bằng cách KÉO THẢ file vào màn phủ\n3. Quan sát danh sách file đã chọn",
       "Ảnh JPG · ảnh PNG · ảnh JPEG · ảnh vuông / dọc / ngang · video MP4 · audio M4A · "
       "file có tên tiếng Nhật · file có tên chứa khoảng trắng",
       "- Cả 2 cách upload đều thành công với mọi file trên\n"
       "- Ảnh hiện thumbnail tương ứng; video và audio hiện icon; tên file hiển thị đúng nguyên văn",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r397-r407, r416"),

    tc("Gửi media", "MEDIA-001", "Abnormal",
       "Upload media vượt dung lượng cho phép — bị chặn",
       BOT,
       "1. Với mỗi file ở cột Dữ liệu test: thử upload\n2. Ghi nhận thông báo và kết quả",
       "Ảnh > 10 MB · video > 200 MB · audio > 25 MB",
       "- Cả 3 loại đều bị chặn, hiện thông báo lỗi rõ ràng\n"
       "- File không được đưa vào danh sách gửi, không gửi được cho friend",
       spec="Đã hỏi leader",
       note="MT-10: spec chat-11 KHÔNG ghi giới hạn dung lượng nào. Nguồn: Content: Send message r409-r411"),

    tc("Gửi media", "MEDIA-001", "Abnormal",
       "Upload media sai định dạng — bị chặn",
       BOT,
       "1. Thử upload từng file ở cột Dữ liệu test\n2. Ghi nhận thông báo và kết quả",
       "Ảnh: TIFF, GIF · Video: AVI, WMV, MKV · Audio: WMA, WAV, MKV, MP3",
       "- Tất cả bị chặn hoặc không hiện trong hộp thoại chọn file\n- Không đưa vào danh sách gửi",
       spec="Đã hỏi leader",
       note="MT-10: spec không liệt kê định dạng được phép. Nguồn: Content: Send message r413-r415"),

    tc("Gửi media", "MEDIA-001", "Boundary",
       "Giới hạn 5 file media mỗi lần gửi",
       BOT,
       "1. Chọn 5 file media hợp lệ → quan sát\n2. Thử chọn thêm file thứ 6 → ghi nhận thông báo\n"
       "3. Xoá 1 file khỏi danh sách → thử upload thêm 1 file mới",
       "5 file hợp lệ, thử thêm file thứ 6",
       "- Chọn được đúng 5 file\n"
       "- File thứ 6: hiện thông báo「同時にアップロードできるのは最大5つだけです。」\n"
       "- Sau khi xoá bớt 1 file: upload thêm được 1 file mới",
       note="Nguồn: Content: Send message r412, r428"),

    tc("Gửi media", "MEDIA-001", "Abnormal",
       "Bấm gửi khi chưa chọn file và chưa nhập nội dung — báo lỗi",
       BOT,
       "1. Mở màn phủ gửi media, không chọn file, không nhập nội dung\n2. Bấm gửi",
       "Không file, không nội dung",
       "- Hiện thông báo「メッセージが配信できませんでした。」\n- Không gửi gì cho friend",
       note="Nguồn: Content: Send message r408"),

    tc("Gửi media", "UI-002", "Normal",
       "Danh sách file đã chọn — xem trước, xoá và sắp xếp thứ tự",
       BOT,
       "1. Chọn 1 ảnh + 1 video + 1 audio\n2. Click vào từng file để xem trước\n"
       "3. Hover nút X của từng file, rồi bấm X xoá 1 file\n"
       "4. Kéo thả để đưa 1 file lên đầu, xuống cuối, vào giữa",
       "3 file: ảnh, video, audio",
       "- Xem trước: ảnh hiện ảnh; video tự phát; audio tự phát\n"
       "- Hover nút X: có gợi ý; bấm X: xoá đúng file đó, các file khác giữ nguyên\n"
       "- Kéo thả: thứ tự file thay đổi đúng theo vị trí thả",
       note="Gộp vì đều là thao tác trên danh sách file trước khi gửi. "
            "Nguồn: Content: Send message r424-r440"),

    tc("Gửi media", "MSG-001", "Normal",
       "Gửi media kèm nội dung text — text gửi trước, media gửi sau",
       BOT,
       "1. Chọn 1 ảnh + 1 video + 1 audio (3 file)\n2. Nhập nội dung text có xuống dòng và sticker\n"
       "3. Bấm gửi\n4. Quan sát thứ tự tin nhắn ở chat 1:1 và trên app LINE",
       "Text nhiều dòng + 3 file media",
       "- Text được gửi TRƯỚC, sau đó tới các file media theo đúng thứ tự đã sắp xếp\n"
       "- Cả cụm hiển thị đúng ở chat 1:1 và app LINE\n"
       "- Mỗi tin nhắn trong cụm được tính là 1 tin gửi",
       note="Nguồn: Content: Send message r441-r443"),

    tc("Gửi media", "MEDIA-IMG-001", "Normal",
       "Chất lượng ảnh sau khi gửi — kiểm tra hiệu ứng resize",
       BOT,
       "1. Chuẩn bị ảnh gốc kích thước lớn (ví dụ 3000×2000, 8 MB)\n2. Gửi cho friend A\n"
       "3. Trên app LINE: mở ảnh, phóng to, kiểm tra độ nét\n"
       "4. Ở chat 1:1: tải ảnh về, so sánh kích thước và độ nét với ảnh gốc",
       "Ảnh 3000×2000, 8 MB",
       "- Ảnh gửi được, friend xem được rõ ràng trên app LINE\n"
       "- Ghi nhận kích thước ảnh thực tế sau khi gửi làm evidence (spec nói resize còn 1040px)",
       env="PRODUCTION",
       note="RULE-08: media bắt buộc PRODUCTION. Nguồn: Content: Send message r444 + spec feature-spec.md:77"),

    tc("Gửi media", "MEDIA-001", "Abnormal",
       "Bấm gửi khi file chưa upload xong — không gửi tin lỗi",
       BOT + "\n- Bật throttling mạng chậm ở DevTools",
       "1. Chọn 1 video dung lượng lớn (gần giới hạn)\n"
       "2. Trong lúc thanh tiến trình đang chạy, bấm nút gửi\n3. Quan sát kết quả",
       "Video lớn, mạng chậm",
       "- Không gửi được tin lỗi hoặc file rỗng\n"
       "- Hoặc nút gửi bị vô hiệu tới khi upload xong, hoặc hiện thông báo chờ upload",
       note="Nguồn: Content: Send message r445"),

    tc("Gửi media", "MEDIA-001", "Normal",
       "Media gửi từ chat 1:1 lưu đúng server media hiện tại",
       BOT,
       "1. Gửi lần lượt ảnh, video, audio, PDF từ chat 1:1 web\n"
       "2. Với mỗi tin: kiểm tra đường dẫn file trong DB bảng tin nhắn\n"
       "3. Kiểm tra hiển thị ở chat 1:1 web, app mobile và app LINE của friend\n"
       "4. Lặp lại khi gửi từ app mobile",
       "4 loại file × 2 client (web, app mobile)",
       "- Đường dẫn file trỏ đúng domain server media đang dùng\n"
       "- File hiển thị/tải được ở cả 3 nơi: chat 1:1 web, app mobile, app LINE",
       env="PRODUCTION",
       note="Nguồn: file 01. TCsLine_Chat1:1 (cũ) → tab Improve server image r3-r10 (11/2023, TC > 2 năm — CẦN VERIFY LẠI)"),

    # ═══════════════ Gửi PDF ═══════════════
    tc("Gửi PDF", "UI-001", "Normal",
       "Chọn file PDF — hộp thoại chỉ hiện file PDF, có tiến trình tải và ghi chú chuyển URL",
       BOT,
       "1. Click nút gửi PDF\n2. Quan sát hộp thoại chọn file\n3. Chọn 1 file PDF\n"
       "4. Quan sát khu vực nhập nội dung trong lúc tải và sau khi tải xong",
       "1 file PDF hợp lệ",
       "- Hộp thoại chỉ hiển thị file PDF\n"
       "- Trong lúc tải: hiện icon PDF + tên file + biểu tượng đang tải\n"
       "- Sau khi tải xong: hiện dòng chú thích「送信後、URLに自動変換されます」\n"
       "- Khu vực nhập ẩn bớt các nút khác",
       note="Nguồn: Content: Send message r447-r449, r453"),

    tc("Gửi PDF", "UI-002", "Normal",
       "Xem trước và xoá file PDF đã chọn",
       BOT + "\n- Đã chọn 1 file PDF",
       "1. Click vào icon PDF → quan sát bản xem trước\n2. Hover nút X → quan sát\n3. Bấm X",
       "1 file PDF",
       "- Click icon: mở bản xem trước nội dung file PDF\n"
       "- Hover nút X: màu nhạt đi\n- Bấm X: file bị gỡ khỏi danh sách gửi",
       note="Nguồn: Content: Send message r450-r452"),

    tc("Gửi PDF", "MSG-001", "Normal",
       "Gửi PDF — friend nhận và mở được, tên file hiển thị đúng",
       BOT,
       "1. Gửi PDF không kèm nội dung → kiểm tra chat 1:1 và app LINE\n"
       "2. Gửi PDF kèm nội dung text (có xuống dòng và sticker) → kiểm tra thứ tự\n"
       "3. Trên app LINE: bấm vào file, mở/tải file\n4. Kiểm tra tên file hiển thị phía friend",
       "File PDF tên `テスト資料 2026.pdf`",
       "- Gửi không kèm text: friend nhận được file, mở/tải được\n"
       "- Gửi kèm text: text gửi TRƯỚC, file gửi sau\n"
       "- Phía friend hiển thị ĐÚNG TÊN file (không phải chuỗi số ngẫu nhiên)",
       note="Bug #29946 (05/2025): trước fix phía friend hiện tên file là chuỗi số. "
            "Nguồn: Content: Send message r454-r456, r1205, r1206"),

    tc("Gửi PDF", "SYNC-APP-001", "Normal",
       "Gửi PDF từ APP MOBILE — tên file hiển thị đúng ở cả 2 phía",
       "- App mobile LME đăng nhập account admin bot A\n- Đang mở hội thoại friend A",
       "1. Ở app mobile: gửi 1 file PDF có tên tiếng Nhật\n"
       "2. Kiểm tra tên file hiển thị trên màn chat của app mobile\n"
       "3. Kiểm tra tên file phía friend trên app LINE\n4. Kiểm tra hiển thị trên chat 1:1 web",
       "File PDF tên `テスト資料 2026.pdf`, gửi từ app mobile",
       "- Cả 3 nơi (app mobile, app LINE của friend, chat 1:1 web) đều hiển thị đúng tên file",
       env="PRODUCTION",
       note="Nguồn: Content: Send message r1208, r1209 (Bug #29946)"),

    tc("Gửi PDF", "MSG-003", "Abnormal",
       "PDF gửi qua job (Broadcast) — hiển thị dạng link thay vì tên file",
       BOT + "\n- Template có file PDF, đã tạo Broadcast dùng template đó",
       "1. Gửi Broadcast chứa template có PDF cho friend A\n"
       "2. Kiểm tra hiển thị phía friend trên app LINE\n3. Kiểm tra hiển thị ở chat 1:1",
       "PDF đính trong template, gửi qua job Broadcast",
       "- Phía friend hiển thị dạng LINK (không phải tên file) vì file PDF được tạo trong template\n"
       "- Đây là hành vi khác với gửi trực tiếp từ chat 1:1 — ghi rõ ở evidence",
       env="PRODUCTION", spec="Spec không ghi",
       note="Nguồn: Content: Send message r1207 — TC gốc ghi 「riêng send từ job sẽ hiển thị link」"),

    tc("Gửi PDF", "MEDIA-001", "Abnormal",
       "Bấm gửi PDF khi file chưa tải xong — không gửi tin lỗi",
       BOT + "\n- Bật throttling mạng chậm",
       "1. Chọn 1 file PDF dung lượng lớn\n2. Trong lúc đang tải, bấm nút gửi\n3. Quan sát kết quả",
       "PDF lớn, mạng chậm",
       "- Không gửi tin lỗi hoặc file rỗng\n- Hoặc chặn nút gửi, hoặc hiện thông báo chờ",
       note="Nguồn: Content: Send message r457"),

    # ═══════════════ Gửi sticker ═══════════════
    tc("Gửi sticker", "UI-INPUT-001", "Abnormal",
       "Chưa chọn sticker — nút gửi bị vô hiệu",
       BOT,
       "1. Mở modal chọn sticker\n2. Không chọn sticker nào\n3. Quan sát nút gửi",
       "Modal sticker vừa mở",
       "- Nút gửi ở trạng thái vô hiệu, không bấm được",
       note="Nguồn: Content: Send message r360"),

    tc("Gửi sticker", "MSG-001", "Normal",
       "Chọn và gửi sticker — friend nhận đúng sticker đã chọn",
       BOT,
       "1. Mở modal sticker → chọn 1 sticker ở nhóm đầu tiên → gửi\n"
       "2. Mở lại → đổi sang nhóm khác → chọn sticker → gửi\n"
       "3. Chọn sticker A rồi đổi sang sticker B cùng nhóm → gửi\n"
       "4. Chọn sticker A → đổi nhóm → chọn sticker B → gửi\n"
       "5. Đổi sticker và nhóm nhiều lần rồi gửi\n"
       "6. Với mỗi lần: kiểm tra sticker ở chat 1:1 và trên app LINE",
       "Sticker ở nhiều nhóm khác nhau",
       "- Mọi trường hợp: gửi ĐÚNG sticker được chọn cuối cùng\n"
       "- Chat 1:1 và app LINE hiển thị đúng sticker đó",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r361-r363, r365, r368"),

    tc("Gửi sticker", "STATE-CLEAN-001", "Abnormal",
       "Chọn sticker rồi đổi nhóm mà không chọn lại (WEB) — xoá lựa chọn cũ, vô hiệu nút gửi",
       BOT,
       "1. Mở modal sticker trên WEB, chọn sticker A ở nhóm 1\n"
       "2. Chuyển sang nhóm 2, KHÔNG chọn sticker nào\n3. Quan sát nút gửi và trạng thái sticker A",
       "Sticker A ở nhóm 1, chuyển sang nhóm 2",
       "- Lựa chọn sticker A bị xoá\n- Nút gửi trở lại trạng thái vô hiệu\n- Không gửi được sticker A",
       note="Bug #32589 (10/2025). Hành vi WEB khác APP → tách 2 TC. Nguồn: Content: Send message r364"),

    tc("Gửi sticker", "SYNC-APP-001", "Abnormal",
       "Chọn sticker rồi đổi nhóm mà không chọn lại (APP MOBILE) — vẫn gửi được sticker cũ",
       "- App mobile LME đăng nhập account admin bot A, mở hội thoại friend A",
       "1. Mở modal sticker trên APP, chọn sticker A ở nhóm 1\n"
       "2. Chuyển sang nhóm 2, KHÔNG chọn sticker nào\n3. Bấm gửi\n4. Kiểm tra sticker friend nhận",
       "Sticker A ở nhóm 1, chuyển sang nhóm 2, trên app mobile",
       "- Vẫn gửi được sticker A cho friend\n"
       "- Khác với hành vi trên WEB (web xoá lựa chọn) — ghi rõ chênh lệch ở evidence",
       env="PRODUCTION", spec="Spec không ghi",
       note="Chênh lệch web/app được ghi rõ trong corpus. Nguồn: Content: Send message r379"),

    tc("Gửi sticker", "STATE-001", "Normal",
       "Chọn sticker rồi đóng modal, mở lại — lựa chọn cũ được giữ",
       BOT,
       "1. Mở modal sticker, chọn sticker A, đóng modal (không gửi)\n"
       "2. Mở lại modal → quan sát sticker đang chọn\n3. Bấm gửi luôn → kiểm tra sticker friend nhận\n"
       "4. Lặp lại nhưng lần này chọn sticker B rồi gửi",
       "Sticker A, sau đó sticker B",
       "- Mở lại modal: sticker A vẫn đang được chọn\n"
       "- Gửi luôn: friend nhận sticker A\n- Chọn B rồi gửi: friend nhận sticker B",
       note="Nguồn: Content: Send message r366, r367"),

    tc("Gửi sticker", "STATE-001", "Abnormal",
       "Chọn sticker ở friend A, chuyển sang friend B — sticker vẫn giữ, gửi được cho B",
       BOT + "\n- Có friend A và friend B",
       "1. Ở friend A: mở modal sticker, chọn sticker S1, đóng modal (không gửi)\n"
       "2. Chuyển sang friend B, mở lại modal sticker\n"
       "3. Bấm gửi luôn → kiểm tra friend B nhận gì\n"
       "4. Lặp lại nhưng đổi sang sticker khác (cùng nhóm / khác nhóm / đổi nhóm không chọn) rồi gửi",
       "Sticker S1 chọn ở A, gửi cho B; sau đó thử đổi sticker",
       "- Mở modal ở B: sticker S1 vẫn đang chọn; bấm gửi thì B nhận S1\n"
       "- Khi đổi sticker: B nhận đúng sticker được chọn cuối cùng",
       note="Bug #32589. Nguồn: Content: Send message r369-r372"),

    tc("Gửi sticker", "CONC-001", "Abnormal",
       "Double click nút gửi sticker — chỉ gửi 1 tin",
       BOT,
       "1. Chọn 1 sticker\n2. Double click nhanh nút gửi\n"
       "3. Đếm sticker ở chat 1:1 và trên app LINE",
       "Double click trong < 300ms",
       "- Chỉ 1 sticker được gửi ở cả chat 1:1 và app LINE",
       note="Nguồn: Content: Send message r373, r388"),

    tc("Gửi sticker", "DATA-001", "Normal",
       "Gửi sticker — tin nhắn cuối của bạn bè KHÔNG bị cập nhật",
       BOT,
       "1. Ghi lại last_message + last_time_message của friend A\n2. Gửi 1 sticker\n"
       "3. Quan sát dòng A ở danh sách và kiểm tra DB",
       "1 sticker",
       LASTMSG,
       spec="Đã hỏi leader", note=MT01 + " Nguồn: Content: Send message r283"),

    # ═══════════════ Gửi template — chọn & preview ═══════════════
    tc("Gửi template — chọn & preview", "UI-001", "Normal",
       "Popup chọn template — hiện đủ folder và template, đúng thứ tự, có scroll",
       BOT + "\n- Bot A có folder mặc định + ≥2 folder tự tạo, tổng ≥15 template, có template tên rất dài",
       "1. Click nút gửi template\n2. Quan sát popup: folder đang focus, danh sách folder, số lượng và thứ tự\n"
       "3. Chọn 1 folder nhiều template, kiểm tra số lượng, thứ tự, tên dài, scroll\n"
       "4. Đối chiếu với màn Quản lý template",
       "≥3 folder, ≥15 template, 1 template tên dài",
       "- Mặc định focus vào folder mặc định\n"
       "- Số lượng và thứ tự folder/template khớp đúng màn Quản lý template\n"
       "- Tên dài không vỡ layout; danh sách dài có scroll",
       note="Nguồn: Content: Send message r459-r469"),

    tc("Gửi template — chọn & preview", "OUT-PREVIEW-001", "Normal",
       "Preview template TEXT — hiển thị đủ ký tự, giá trị chèn và URL",
       BOT + "\n- Template text T1 chứa đủ các thành phần ở cột Dữ liệu test",
       "1. Mở popup chọn template, chọn T1 → mở preview\n"
       "2. Đọc nội dung preview, đối chiếu với nội dung template gốc\n"
       "3. Thử cuộn khi nội dung dài\n4. Đóng preview bằng nút X và bằng nút 閉じる",
       "Ký tự: latinh · tiếng Nhật · ký tự đặc biệt · emoji · xuống dòng\n"
       "Giá trị chèn: LINE名 · 経過日数 (dạng ngày và dạng còn lại) · 配信日の日付 · "
       "friend info mặc định (5 loại) · friend info tự tạo (6 loại)\n"
       "URL: form · item (bill 1 lần, bill chu kỳ: link mua/đổi thẻ/huỷ) · calendar/salon/lesson/event booking "
       "(link đặt + link lịch sử) · URL thường (có/không rút gọn) · URL có đặt tên hiển thị và ảnh",
       "- Preview hiển thị đầy đủ và đúng mọi thành phần trên\n"
       "- Nội dung dài có scroll\n- Nút X và nút 閉じる đều đóng preview và quay lại popup chọn template",
       note="Gộp ~35 điểm vì cùng kết quả hiển thị preview. Nguồn: Content: Send message r472-r511"),

    tc("Gửi template — chọn & preview", "OUT-PREVIEW-001", "Normal",
       "Preview template BUTTON — đủ loại panel, ảnh, tiêu đề, nút",
       BOT + "\n- Có template button đủ 5 loại: standard, color, ảnh, quick-text, quick-ảnh; mỗi loại có bản 1 panel và nhiều panel",
       "1. Mở preview lần lượt từng loại template button ở cột Dữ liệu test\n"
       "2. Với mỗi loại: kiểm tra số panel, ảnh, tiêu đề, mô tả, tên nút, cỡ chữ, icon, giá trị chèn, xuống dòng",
       "Standard (có ảnh/không ảnh × 1 panel/nhiều panel) · Color (tương tự) · "
       "Button ảnh (1 ảnh/nhiều ảnh × có tiêu đề/không tiêu đề) · Quick text (nội dung đủ loại ký tự và giá trị chèn) · "
       "Quick ảnh (1 nút/nhiều nút)",
       "- Preview hiện đủ số panel, đúng ảnh, đúng tiêu đề/mô tả/tên nút\n"
       "- Cỡ chữ đậm nhạt, icon, giá trị chèn, xuống dòng hiển thị đúng\n- Nội dung dài có scroll",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r622-r671"),

    tc("Gửi template — chọn & preview", "OUT-PREVIEW-001", "Normal",
       "Preview template MEDIA / sticker / location — hiển thị đúng loại nội dung",
       BOT + "\n- Có template ảnh thường, image map, video (có/không thumbnail), audio, sticker, location",
       "1. Mở preview lần lượt từng template ở cột Dữ liệu test\n2. Quan sát nội dung preview",
       "Ảnh thường (dọc/vuông/ngang) · image map (dọc/vuông/ngang) · video có thumbnail · "
       "video không thumbnail · audio · sticker · location",
       "- Ảnh thường và image map: hiện đúng ảnh theo tỉ lệ\n"
       "- Video: KHÔNG hiển thị trong preview (cả trường hợp có và không có thumbnail)\n"
       "- Audio, sticker, location: hiển thị đúng dạng tương ứng",
       note="Nguồn: Content: Send message r978-r1003, r1071-r1078"),

    tc("Gửi template — chọn & preview", "OUT-PREVIEW-001", "Normal",
       "Preview TRƯỚC KHI GỬI — sửa nội dung template ngay tại preview",
       BOT + "\n- Group template T có ≥2 template con dạng text",
       "1. Chọn T → bấm gửi → hiện màn preview trước khi gửi\n"
       "2. Hover vào nội dung 1 template con → quan sát\n3. Bấm nút sửa → sửa nội dung → quay lại preview\n"
       "4. Quan sát nút 元の内容にリセットする → bấm nút này\n5. Bấm gửi 上記の内容で送信",
       "Group template T có 2 template con text",
       "- Hover: nội dung mờ đi, hiện nút sửa và nút xoá\n"
       "- Bấm sửa: mở ô sửa nội dung của template con tương ứng\n"
       "- Sau khi sửa: nút 元の内容にリセットする xuất hiện; bấm vào thì nội dung trở về bản gốc\n"
       "- Bấm gửi: đóng preview, quay về chat 1:1, gửi đúng nội dung như trên preview",
       note="Nguồn: Content: Send message r549-r559"),

    tc("Gửi template — chọn & preview", "FUNC-001", "Abnormal",
       "Xoá template con ở màn preview trước khi gửi — không xoá được nếu chỉ còn 1 con",
       BOT + "\n- Group template T1 chỉ có 1 template con\n- Group template T2 có 3 template con",
       "1. Chọn T1 → preview trước khi gửi → hover nội dung → bấm nút xoá\n"
       "2. Chọn T2 → preview → xoá 1 template con → quan sát\n"
       "3. Kiểm tra group template gốc ở màn Quản lý template",
       "T1: 1 template con · T2: 3 template con",
       "- T1: KHÔNG cho xoá template con cuối cùng\n"
       "- T2: xoá thành công, preview còn 2 template con\n"
       "- Group template GỐC ở màn Quản lý template KHÔNG bị ảnh hưởng",
       note="Nguồn: Content: Send message r551, r552"),

    tc("Gửi template — chọn & preview", "OUT-PREVIEW-001", "Abnormal",
       "Template MEDIA ở màn preview trước khi gửi — không có chức năng sửa/xoá",
       BOT + "\n- Group template M gồm các template con dạng media",
       "1. Chọn M → preview trước khi gửi\n2. Hover vào nội dung template media\n"
       "3. Tìm nút sửa và nút xoá\n4. Quan sát nút 元の内容にリセットする",
       "Group template chỉ có template con dạng media",
       "- Hover: KHÔNG có hiệu ứng mờ, KHÔNG hiện nút sửa/xoá\n"
       "- Nút 元の内容にリセットする bị ẩn hoặc vô hiệu (vì không sửa/xoá được gì)",
       note="Khác hẳn template text → TC riêng. Nguồn: Content: Send message r1004-r1009"),

    tc("Gửi template — chọn & preview", "STATE-CLEAN-001", "Normal",
       "Đóng preview trước khi gửi bằng X hoặc 戻る — quay lại popup chọn template, không gửi",
       BOT + "\n- Group template T có ≥2 template con",
       "1. Chọn T → preview trước khi gửi\n2. Bấm X → quan sát\n"
       "3. Lặp lại, bấm 戻る → quan sát\n4. Kiểm tra friend có nhận tin không",
       "Đóng bằng X và bằng 戻る",
       "- Cả 2 cách: đóng preview và quay về popup chọn template\n- Friend KHÔNG nhận tin nhắn nào",
       note="Nguồn: Content: Send message r557, r558, r720, r721, r1010, r1011, r1087, r1088"),

    # ═══════════════ Gửi template — nội dung & action ═══════════════
    tc("Gửi template — nội dung & action", "MSG-001", "Normal",
       "Gửi template TEXT — nội dung, giá trị chèn và URL đều đúng ở 2 phía",
       BOT + "\n- Template text T1 chứa đủ thành phần ở cột Dữ liệu test",
       "1. Chọn T1 → gửi cho friend A\n2. Kiểm tra nội dung ở chat 1:1\n"
       "3. Kiểm tra nội dung trên app LINE của friend A\n4. Bấm thử các URL trên app LINE",
       "Ký tự latinh / tiếng Nhật / ký tự đặc biệt / emoji / xuống dòng · "
       "giá trị chèn LINE名, 経過日数, 配信日の日付, friend info mặc định và tự tạo · "
       "URL form, item, calendar/salon/lesson/event booking, URL thường có/không rút gọn, URL có tên hiển thị và ảnh",
       "- Gửi thành công; chat 1:1 và app LINE đều hiển thị đúng nội dung\n"
       "- Giá trị chèn được thay đúng theo friend A\n- URL bấm vào mở đúng trang đích",
       note="Gộp ~35 điểm vì cùng kết quả. Nguồn: Content: Send message r562-r598"),

    tc("Gửi template — nội dung & action", "MSG-001", "Normal",
       "Gửi template BUTTON / MEDIA / sticker / location — hiển thị đúng ở 2 phía",
       BOT + "\n- Có đủ template button (standard, color, ảnh, quick-text, quick-ảnh; 1 panel và nhiều panel), "
       "media (ảnh thường, image map, video có/không thumbnail, audio), sticker, location",
       "1. Gửi lần lượt từng template ở cột Dữ liệu test cho friend A\n"
       "2. Với mỗi lần: kiểm tra hiển thị ở chat 1:1 và trên app LINE",
       "Button: standard/color (có ảnh × 1 panel/nhiều panel; không ảnh × 1 panel/nhiều panel) · "
       "button ảnh (1 ảnh/nhiều ảnh × có/không tiêu đề) · quick text · quick ảnh (1 nút/nhiều nút)\n"
       "Media: ảnh thường (dọc/vuông/ngang/GIF) · image map · video · audio · sticker · location",
       "- Tất cả gửi thành công\n"
       "- Chat 1:1 hiển thị đúng số panel, ảnh, tiêu đề, nút, cỡ chữ, giá trị chèn\n"
       "- App LINE của friend hiển thị đúng tương ứng",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r723-r769, r1013-r1024, r1090-r1092"),

    tc("Gửi template — nội dung & action", "DATA-REF-001", "Normal",
       "Sửa template rồi gửi lại — chat 1:1 hiển thị nội dung MỚI NHẤT",
       BOT + "\n- Group template T có 1 template con text",
       "1. Gửi T cho friend A lần 1, ghi lại nội dung ở chat 1:1\n"
       "2. Vào màn Quản lý template, sửa nội dung template con → lưu\n"
       "3. Gửi lại T cho friend A NGAY (trong vòng 30 giây)\n"
       "4. So sánh nội dung ở chat 1:1 và trên app LINE của friend",
       "Sửa nội dung template rồi gửi lại trong < 30 giây",
       "- Chat 1:1 hiển thị nội dung MỚI NHẤT, khớp đúng với nội dung phía app LINE\n"
       "- KHÔNG hiển thị nội dung cũ",
       spec="Đã hỏi leader",
       note="MT-18: Bug KH #37831 (06/2026) — cache 30 giây làm chat 1:1 hiện nội dung cũ. Spec không mô tả cache này. "
            "Nguồn: Content: Hiển thị msg r1682 (TC-NEW-01)"),

    tc("Gửi template — nội dung & action", "DATA-REF-001", "Normal",
       "Thêm / xoá / sắp xếp template con rồi gửi lại — chat 1:1 khớp phía LINE",
       BOT + "\n- Group template T ban đầu có 1 template con",
       "1. Gửi T cho friend A qua action gắn tag → ghi lại nội dung ở chat 1:1\n"
       "2. Thêm template con 2, 3, 4, 5 (mỗi lần thêm xong gửi lại và kiểm tra)\n"
       "3. Xoá dần template con 5, 4, 3, 2 (mỗi lần xoá xong gửi lại và kiểm tra)\n"
       "4. Đổi thứ tự template con nhiều lần, mỗi lần gửi lại và kiểm tra\n"
       "5. Sửa nội dung template con nhiều lần, mỗi lần gửi lại và kiểm tra\n"
       "6. Kết hợp: xoá 1 + sửa 1 + thêm 1 + đổi thứ tự rồi gửi lại",
       "Thêm/xoá/sắp xếp/sửa template con; group template từ 1 đến 5 con",
       "- Sau MỖI thao tác: chat 1:1 hiển thị đủ và đúng thứ tự các template con hiện tại\n"
       "- Nội dung ở chat 1:1 KHỚP với nội dung friend nhận trên app LINE\n"
       "- Đặc biệt: template con MỚI THÊM phải hiển thị đủ ở chat 1:1",
       spec="Đã hỏi leader",
       note="MT-18 + TC-NEW-05 (root cause so sánh 1 chiều danh sách template). "
            "Nguồn: Content: Hiển thị msg r1614-r1632, r1686"),

    tc("Gửi template — nội dung & action", "DATA-REF-001", "Normal",
       "Cùng template dùng cho cả action tag và step scenario — sửa 1 lần, cả 2 đều cập nhật",
       BOT + "\n- Template T được dùng đồng thời trong action của tag A và trong 1 step của scenario S\n"
       "- Friend F thoả điều kiện trigger của step",
       "1. Gửi T cho F qua action gắn tag A và qua step của scenario S → ghi lại nội dung ở chat 1:1\n"
       "2. Sửa nội dung T → lưu\n"
       "3. Trong < 30 giây: gửi lại qua CẢ 2 đường\n4. Kiểm tra nội dung ở chat 1:1 của cả 2 tin",
       "Template T dùng chung cho action tag và step scenario",
       "- Chat 1:1 hiển thị nội dung T MỚI ở CẢ tin từ action lẫn tin từ step scenario\n"
       "- Không đường nào còn hiện nội dung cũ",
       spec="Đã hỏi leader",
       note="MT-18: kiểm tra xoá cache cả 2 phía. Nguồn: Content: Hiển thị msg r1684 (TC-NEW-03)"),

    tc("Gửi template — nội dung & action", "DATA-CACHE-001", "Normal",
       "Gửi lại template sau hơn 30 giây (cache hết hạn) — không regress hành vi cũ",
       BOT + "\n- Tag A có action gửi template T",
       "1. Gắn tag A cho friend F → F nhận T\n2. KHÔNG sửa gì, đợi > 30 giây, gắn lại tag A\n"
       "3. Kiểm tra nội dung ở chat 1:1\n4. Lặp lại nhưng CÓ sửa nội dung T trước khi gắn lại",
       "2 kịch bản: không sửa và có sửa, đều đợi > 30 giây",
       "- Cả 2 trường hợp: chat 1:1 hiển thị đúng nội dung HIỆN TẠI của T\n"
       "- Không phát sinh lỗi mới so với hành vi trước khi sửa cache",
       note="Nguồn: Content: Hiển thị msg r1685 (TC-NEW-04)"),

    tc("Gửi template — nội dung & action", "CONC-002", "Abnormal",
       "Sửa template ở tab này trong lúc tab kia đang gửi lại — không kẹt nội dung cũ",
       BOT + "\n- Mở 2 tab admin cùng bot, cùng template T",
       "1. Tab A: bắt đầu gửi lại template T cho friend F\n"
       "2. Gần như đồng thời, Tab B: sửa nội dung T → lưu\n"
       "3. Kiểm tra nội dung tin nhắn ở chat 1:1 và trên app LINE của F\n4. Gửi lại lần nữa và kiểm tra",
       "2 tab thao tác gần đồng thời trên cùng template",
       "- Nội dung hiển thị ở chat 1:1 khớp với nội dung friend thực nhận\n"
       "- Không kẹt nội dung cũ ở lần gửi tiếp theo",
       spec="Spec không ghi",
       note="TC do AI bổ sung theo hướng race giữa socket xoá cache và gửi lại, CẦN LEADER XÁC NHẬN. "
            "Nguồn: Content: Hiển thị msg r1689 (TC-NEW-08)"),

    tc("Gửi template — nội dung & action", "DATA-TEXT-001", "Abnormal",
       "Tên template chứa ký tự & và ký tự nửa chiều rộng — hiển thị đúng, không bị mã hoá lặp",
       BOT,
       "1. Tạo/sửa group template với từng tên ở cột Dữ liệu test\n"
       "2. Lưu → mở lại màn chi tiết → lưu lần 2 → mở lại\n"
       "3. Kiểm tra tên hiển thị ở: màn Quản lý template, popup chọn template ở chat 1:1, preview\n"
       "4. Kiểm tra giá trị lưu trong DB",
       "`A＆B` (& toàn chiều rộng) · `A&B` (& nửa chiều rộng) · `A&B&C＆D` · `ABC123-_()` · `ＡＢＣ123` · "
       "`テスト＆サンプル` · `テスト&サンプル` · `ﾃｽﾄABC123` · `< > & ' \"`",
       "- Mọi tên hiển thị đúng NGUYÊN VĂN ở cả 3 nơi\n"
       "- Ký tự & KHÔNG bị biến thành `&amp;` hay `&amp;amp;` sau nhiều lần lưu\n"
       "- Giá trị trong DB không bị mã hoá lặp",
       note="Bug KH #37831 mục 2 (06/2026). Gộp 9 điểm vì cùng kết quả. "
            "Nguồn: Content: Hiển thị msg r1674-r1681, r1687"),

    tc("Gửi template — nội dung & action", "MSG-002", "Normal",
       "Cài đặt gửi giãn cách của template (delay) — tin đầu gửi ngay, các tin sau do job gửi",
       BOT + "\n- Group template T có 4 template con, BẬT cài đặt gửi giãn cách",
       "1. Gửi T cho friend A từ chat 1:1\n2. Quan sát thứ tự và khoảng cách thời gian các tin ở chat 1:1\n"
       "3. Quan sát phía app LINE của friend A\n4. Kiểm tra hiển thị người gửi của từng tin",
       "Group template 4 con, bật gửi giãn cách",
       "- Tin đầu tiên gửi ngay; các tin sau được job gửi cách nhau vài giây\n"
       "- Ghi lại khoảng cách thực tế giữa các tin làm evidence (đối chiếu MT-05)\n"
       "- Các tin phía sau hiển thị như tin gửi template thường, CÓ thông tin người gửi",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-05: spec ghi giãn cách 2-4 giây (feature-spec.md:104), corpus ghi 2-5 giây. Job → RULE-08. "
            "Nguồn: Content: Send message r1093-r1094"),

    tc("Gửi template — nội dung & action", "MSG-002", "Normal",
       "Template delay gửi qua nút bấm / callback — các tin sau KHÔNG có thông tin người gửi",
       BOT + "\n- Group template T bật gửi giãn cách, được gán vào action của nút bấm và action tự động trả lời",
       "1. Cho friend A bấm nút của template có action gửi T → quan sát chat 1:1\n"
       "2. Cho friend A kích hoạt tự động trả lời có action gửi T → quan sát chat 1:1\n"
       "3. So sánh với trường hợp gửi T từ chat 1:1 và từ multi action",
       "T bật delay, gửi qua nút bấm và qua callback tự động trả lời",
       "- Tin gửi qua nút bấm / callback: các tin phía sau KHÔNG có thông tin người gửi\n"
       "- Tin gửi từ chat 1:1 / multi action: CÓ thông tin người gửi\n"
       "- Cả 2 đều hiển thị như gửi template thường, không mang định dạng gửi bằng action",
       env="PRODUCTION",
       note="Tách khỏi TC trên vì kết quả hiển thị người gửi khác nhau. Nguồn: Content: Send message r1095-r1097"),

    tc("Gửi template — nội dung & action", "MSG-004", "Abnormal",
       "Sửa template thành chuỗi chỉ có khoảng trắng rồi gửi — web và app xử lý khác nhau",
       BOT + "\n- Group template T có template con dạng text",
       "1. Trên WEB: sửa nội dung template con thành 1 ký tự khoảng trắng → lưu → bấm gửi ở chat 1:1\n"
       "2. Ghi nhận thông báo và kết quả\n3. Lặp lại trên APP MOBILE",
       "Nội dung template = 1 ký tự khoảng trắng",
       "- WEB: khi bấm gửi hiện thông báo, không gửi được nội dung rỗng\n"
       "- APP: gửi lại nội dung CŨ (không phải khoảng trắng) — ghi rõ chênh lệch web/app ở evidence",
       spec="Spec không ghi",
       note="Nguồn: Content: Send message r619, r620"),

    tc("Gửi template — nội dung & action", "MSG-001", "Normal",
       "Sửa nội dung template ngay trong preview 2 lần rồi gửi — gửi đúng bản sửa lần cuối",
       BOT + "\n- Group template T có ≥1 template con text\n- Kiểm tra trên cả web và app mobile",
       "1. Chọn T → preview trước khi gửi → sửa nội dung lần 1 (chưa gửi)\n"
       "2. Sửa tiếp lần 2 (nhập tiếng Nhật / tiếng Việt / có icon)\n3. Bấm gửi\n"
       "4. Kiểm tra nội dung ở chat 1:1 và trên app LINE\n5. Lặp lại trên app mobile",
       "Sửa 2 lần liên tiếp, nội dung có tiếng Nhật, tiếng Việt và icon",
       "- Tin gửi đi đúng bằng nội dung của lần sửa THỨ 2\n"
       "- Chat 1:1 và app LINE khớp nhau\n- Đúng trên cả web và app mobile",
       note="Bug #30992 (07/2025 — edit 2 lần thì lần 2 không phản ánh). "
            "Nguồn: Content: Send message r610-r617"),

    tc("Gửi template — nội dung & action", "MSG-001", "Normal",
       "Gửi template có action cho bạn bè — bấm nút thì action chạy đúng",
       BOT + "\n- Template button T có action: gửi text, gửi template, bắt đầu scenario, bắt đầu remind\n"
       "- Có cả action phía bạn bè: mở URL (trong/ngoài LINE), mở form/conversion/salon/event, nhập SĐT, nhập email",
       "1. Gửi T cho friend A từ chat 1:1\n2. Trên app LINE, friend bấm từng nút\n"
       "3. Kiểm tra action thực thi: tin nhắn nhận được, scenario/remind bắt đầu, URL mở đúng\n"
       "4. Kiểm tra hiển thị tin action ở chat 1:1",
       "Action LME: gửi text · gửi template · bắt đầu scenario · bắt đầu remind\n"
       "Action bạn bè: mở URL trong/ngoài LINE · mở form/conversion/salon/event · nhập SĐT · nhập email",
       "- Mọi action đều chạy đúng khi friend bấm nút\n"
       "- Tin nhắn do action gửi hiển thị ở chat 1:1 kèm dấu hiệu gửi bằng action\n"
       "- Scenario/remind được bắt đầu, kiểm chứng ở tab 基本情報 của cột phải",
       env="PRODUCTION",
       note="Ma trận action đầy đủ theo loại nút thuộc phạm vi FA-010 Template; ở đây chỉ phủ mức "
            "gửi-từ-chat-1:1 → action chạy đúng. Nguồn: Content: Send message r812-r975"),

    tc("Gửi template — nội dung & action", "DATA-001", "Normal",
       "Gửi template và các loại tin khác — tin nhắn cuối KHÔNG bị cập nhật",
       BOT,
       "1. Với mỗi loại ở cột Dữ liệu test: gửi cho friend A\n"
       "2. Sau mỗi lần: quan sát dòng A ở danh sách và kiểm tra DB last_message/last_time_message",
       "Template text (có/không chèn info, info không có giá trị, info đã xoá) · template button · "
       "template ảnh · template video · template audio · template sticker · template location · "
       "group template nhiều loại · template gửi giãn cách · action text · action template",
       LASTMSG,
       spec="Đã hỏi leader",
       note=MT01 + " Gộp ~15 điểm vì cùng kết quả. Nguồn: Content: Send message r284-r301"),

    # ═══════════════ Gửi multi action ═══════════════
    tc("Gửi multi action", "UI-001", "Normal",
       "Mở modal chọn action — hiện danh sách action, nút đóng và nút lưu",
       BOT,
       "1. Click nút アクション ở khu vực nhập tin\n2. Quan sát modal: danh sách action, nút X, nút lưu",
       "Màn chat, chưa chọn action",
       "- Modal hiện danh sách các loại action có thể gửi\n- Có nút X đóng và nút lưu/thực thi",
       note="Nguồn: Content: Send message r1115-r1118"),

    tc("Gửi multi action", "MSG-001", "Normal",
       "Action gửi text và action gửi template — friend nhận đúng, chat 1:1 hiển thị đúng nguồn",
       BOT + "\n" + INFOSET,
       "1. Mở modal action, chọn action gửi text (có chèn LINE名 và friend info) → thực thi\n"
       "2. Kiểm tra tin ở chat 1:1 và app LINE\n"
       "3. Lặp lại với action gửi template các dạng ở cột Dữ liệu test (có filter và không filter)",
       "Action text: không chèn / chèn LINE名 / chèn friend info cơ bản / chèn friend info tự tạo\n"
       "Action template: dạng text · dạng button · dạng media · dạng location — mỗi dạng thử có filter và không filter",
       "- Friend nhận đúng tin trên app LINE, giá trị chèn được thay đúng\n"
       "- Chat 1:1 hiển thị tin kèm dấu hiệu gửi bằng action và có thông tin người thao tác",
       note="Gộp vì cùng kết quả. Nguồn: Content: Send message r1126-r1138"),

    tc("Gửi multi action", "FUNC-001", "Normal",
       "Action bắt đầu / dừng scenario — trạng thái scenario của bạn bè thay đổi đúng",
       BOT + "\n- Có scenario S nhiều bước, friend A chưa chạy scenario nào",
       "1. Mở modal action, chọn bắt đầu scenario S từ đầu (thử cả có filter và không filter) → thực thi\n"
       "2. Kiểm tra tab 基本情報 của cột phải và message hệ thống ở chat 1:1\n"
       "3. Lặp lại với bắt đầu scenario từ ngày thứ N\n"
       "4. Chọn action dừng scenario → thực thi → kiểm tra lại",
       "Scenario S; bắt đầu từ đầu / từ ngày thứ N / dừng — mỗi loại thử có filter và không filter",
       "- Bắt đầu: tab 基本情報 hiện tên scenario đang chạy; chat 1:1 có message bắt đầu scenario\n"
       "- Bắt đầu từ ngày thứ N: message ghi rõ bắt đầu từ ngày thứ mấy\n"
       "- Dừng: tab 基本情報 về 配信中のステップなし; chat 1:1 có message dừng scenario",
       note="Nguồn: Content: Send message r1119-r1124"),

    tc("Gửi multi action", "FUNC-001", "Normal",
       "Các action thao tác dữ liệu bạn bè — gắn/gỡ tag, rich menu, bookmark, trạng thái, block, ẩn",
       BOT + "\n- Có tag T1, rich menu R1, trạng thái đối ứng S1",
       "1. Với mỗi action ở cột Dữ liệu test: mở modal action → chọn → thực thi\n"
       "2. Sau mỗi lần: kiểm tra kết quả ở nơi tương ứng (tab タグ管理, tab 基本情報, danh sách bạn bè)\n"
       "3. Kiểm tra DB tương ứng",
       "Gắn tag / gỡ tag (có filter và không filter) · gắn rich menu / gỡ rich menu · "
       "gắn bookmark / gỡ bookmark · gán trạng thái / gỡ trạng thái · block / bỏ block · hiển thị / ẩn",
       "- Mỗi action đều có hiệu lực đúng, kiểm chứng được ở màn hình và DB\n"
       "- Gắn tag có action gửi tin: friend nhận được tin của action đó",
       note="Gộp vì cùng dạng kết quả. Nguồn: Content: Send message r1139-r1181"),

    tc("Gửi multi action", "FUNC-001", "Normal",
       "Action ghi giá trị friend info — đủ mọi kiểu info, cả đăng ký và xoá giá trị",
       BOT + "\n" + INFOSET,
       "1. Với mỗi kiểu info ở cột Dữ liệu test: chọn action đăng ký giá trị → thực thi → kiểm tra tab 友だち情報\n"
       "2. Chọn action xoá giá trị → thực thi → kiểm tra tab 友だち情報\n"
       "3. Với kiểu điểm: thử gán giá trị chỉ định và ngẫu nhiên, cộng điểm, trừ điểm",
       "Info mặc định: システム表示名 · SĐT · email · sinh nhật (theo ngày chọn và theo hôm nay) · tỉnh\n"
       "Info tự tạo: text · lựa chọn · ngày (theo ngày chọn và theo hôm nay) · ảnh · PDF · "
       "điểm (gán chỉ định/ngẫu nhiên, cộng chỉ định/ngẫu nhiên, trừ chỉ định/ngẫu nhiên, xoá)",
       "- Đăng ký: tab 友だち情報 hiện đúng giá trị vừa ghi\n"
       "- Xoá: giá trị bị xoá khỏi tab 友だち情報\n"
       "- Điểm: giá trị cộng/trừ đúng phép tính; giá trị ngẫu nhiên nằm trong khoảng đã cấu hình",
       note="Gộp vì cùng dạng kết quả. Nguồn: Content: Send message r1147-r1175"),

    tc("Gửi multi action", "MSG-002", "Normal",
       "Gửi nhiều action cùng lúc — cách gộp marker theo cấu hình gửi giãn cách",
       BOT + "\n- Có template T1 KHÔNG bật gửi giãn cách và template T2 CÓ bật gửi giãn cách",
       "1. Mở modal action, chọn đồng thời: action gửi text + action gửi template T1 → thực thi\n"
       "2. Quan sát cách hiển thị marker, người gửi và thời gian ở chat 1:1\n"
       "3. Lặp lại với T2 (có bật gửi giãn cách)\n"
       "4. Thử thêm: action bắt đầu scenario gửi cùng action text",
       "T1 không delay · T2 có delay · action scenario + action text",
       "- Với T1: các tin gửi cùng lúc hiển thị CHUNG 1 marker, chung 1 người gửi, chung 1 thời gian\n"
       "- Với T2: template đầu tiên chung marker với các action khác, các tin sau tách riêng\n"
       "- Với scenario: tin của step hiển thị marker và thời gian RIÊNG (do job gửi)",
       note="Mỗi cấu hình có cách gộp marker khác nhau nhưng cùng 1 chuỗi kiểm chứng. "
            "Nguồn: Content: Send message r1125, r1134, r1135"),
]
