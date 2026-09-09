# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 9-10: hệ quả sau khi chạy bulk action (last message,
bộ đếm 未確認) và xử lý lỗi / hiệu năng của job.

Nguồn chính: 10.3 TCsLine_Friendlist → tab「Testcase」r46-r133.

⚠ MT-03 — CẢNH BÁO NIÊN ĐẠI GẦN NHAU: trong CÙNG một ô kết quả mong đợi của TC gốc
có 2 tầng expected ngược nhau:
  • Bug KH #35071 (03/2026):『update last_message và last_time_message』
  • SpecImprove #35389 (04/2026):『Spec change 4/2026: KHÔNG update last message của
    friend — time không update, nội dung không update』
Hai mốc chỉ cách nhau 1 tháng nên quy tắc『ưu tiên TC mới nhất』là căn cứ YẾU nếu chỉ
xét ngày. Kho chọn tầng #35389 vì: (a) nó tự khai báo là SPEC CHANGE chứ không phải
bug fix, (b) cột kết quả #35389 có đầy đủ trạng thái OK ở step/staging trong khi cột
#35071 đã bị nó thay thế, (c) cột「Actual Result」của r60-r71 đều ghi lại chính câu
spec change này. Toàn bộ TC dưới đây viết theo #35389 và ghi rõ TC gốc nói khác.
Spec-features KHÔNG ghi quy tắc nào về last_message khi chạy action → spec bỏ sót.
"""
from _common import tc

BOT = ("- Đăng nhập Admin (role 主管理者) của bot đã liên kết LINE OA\n"
       "- Bot có ≥ 10 friend, trong đó ≥ 3 friend đang có last message cũ (ghi lại nội dung "
       "và thời điểm trước khi test)\n"
       "- Mở /basic/friendlist")
BOT_CONF = ("- Đăng nhập Admin của bot đã liên kết LINE OA\n"
            "- Chuẩn bị 2 friend: 1 đang ở trạng thái ĐÃ xác nhận, 1 đang CHƯA xác nhận\n"
            "- Ghi lại số 未確認 hiện tại của bot\n"
            "- Mở /basic/friendlist")

S5 = [
    # ═══════════ 9. Bulk action — last message & bộ đếm 未確認 ═══════════
    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "⭐ Gửi action text từ friendlist KHÔNG update last message và last time của friend",
       BOT,
       "1. Ghi lại nội dung「最新メッセージ」và thời điểm hiển thị ở màn friendlist của 1 friend\n"
       "2. Ghi lại nội dung + thời gian tin cuối trên màn chat 1:1 của friend đó\n"
       "3. Tích friend đó → chạy action gửi text「テスト送信」\n"
       "4. Xác nhận friend ĐÃ nhận được tin trên app LINE\n"
       "5. Reload màn friendlist và màn chat 1:1, đọc lại 2 giá trị ở bước 1-2",
       "1 friend · action gửi 1 text",
       "- Friend nhận được tin「テスト送信」trên app LINE (action chạy thành công)\n"
       "- Cột「最新メッセージ」ở màn friendlist KHÔNG đổi — vẫn là thời điểm cũ\n"
       "- Nội dung last message ở màn chat 1:1 KHÔNG đổi\n"
       "- Chỉ tin nhắn friend GỬI ĐẾN mới làm 2 giá trị này thay đổi",
       spec="Đã hỏi leader",
       note="Nguồn: r46 (viết theo tầng SpecImprove #35389, 04/2026). ⚠ TC gốc tầng cũ "
            "(Bug KH #35071, 03/2026) nói NGƯỢC LẠI:『update last_message và last_time_message』"
            "→ nếu Leader chốt theo tầng cũ thì TC này DỰ KIẾN FAIL và phải raise bug. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "Gửi nhiều action text / template / trộn cả hai — vẫn không update last message",
       BOT,
       "1. Ghi lại「最新メッセージ」của 5 friend test\n"
       "2. Lần lượt chạy 5 tổ hợp action, mỗi tổ hợp cho 1 friend:\n"
       "   a. nhiều action text cùng lúc\n"
       "   b. 1 action template chỉ có 1 message\n"
       "   c. 1 action template gồm nhiều message\n"
       "   d. action text + action template\n"
       "   e. nhiều text + nhiều template\n"
       "3. Xác nhận cả 5 friend nhận đủ tin trên app LINE\n"
       "4. Reload màn friendlist, đọc lại「最新メッセージ」của 5 friend",
       "5 friend · 5 tổ hợp action gửi tin",
       "- Cả 5 friend nhận đủ tin nhắn trên app LINE\n"
       "- Cả 5 friend có「最新メッセージ」KHÔNG đổi so với bước 1\n"
       "- Nội dung last message ở chat 1:1 của cả 5 friend KHÔNG đổi",
       spec="Đã hỏi leader",
       note="Nguồn: r47-r53 (7 dòng gộp thành 1 TC vì CÙNG 1 kết quả mong đợi — RULE tách TC: "
            "nhiều input, cùng expected → giữ chung, liệt kê đủ input ở cột Dữ liệu nhập). "
            "Viết theo tầng #35389. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "Action KHÔNG phải text/template (start scenario, add tag, add friend info) "
       "kể cả khi bên trong có message gửi ngay",
       BOT + "\n- Chuẩn bị: scenario có message gửi ngay, tag có action gửi template, "
             "friend info có action gửi message",
       "1. Ghi lại「最新メッセージ」của 3 friend test\n"
       "2. Friend 1: chạy action start scenario (scenario có message send ngay)\n"
       "3. Friend 2: chạy action add tag (tag có action gửi template)\n"
       "4. Friend 3: chạy action ghi friend info (info có action gửi message)\n"
       "5. Xác nhận cả 3 friend nhận được message trên app LINE\n"
       "6. Reload màn friendlist và chat 1:1, đọc lại giá trị",
       "3 friend · 3 loại action gián tiếp gửi message",
       "- Cả 3 friend nhận được message trên app LINE\n"
       "- KHÔNG update last_message và last_time_message\n"
       "- Màn chat 1:1 hiển thị message mới nhưng thời gian tin cuối ở danh sách KHÔNG đổi\n"
       "- Cột「最新メッセージ」ở màn friendlist hiển thị đúng giá trị cũ",
       spec="Đã hỏi leader",
       note="Nguồn: r54, r55, r56. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "Action trộn: start scenario/remind (có message gửi ngay) + text hoặc template",
       BOT + "\n- Chuẩn bị scenario và remind đều có message gửi ngay",
       "1. Ghi lại「最新メッセージ」của 3 friend test\n"
       "2. Friend 1: action start scenario (có msg gửi ngay) + action text\n"
       "3. Friend 2: action text + action start scenario (có step gửi ngay)\n"
       "4. Friend 3: action template + action start remind (có message gửi ngay)\n"
       "5. Reload, đọc lại giá trị của 3 friend",
       "3 friend · 3 tổ hợp action trộn",
       "- Cả 3 friend nhận đủ message trên app LINE\n"
       "- KHÔNG update last message: cả thời gian lẫn nội dung đều giữ nguyên\n"
       "- Cột「最新メッセージ」ở màn friendlist không đổi",
       spec="Đã hỏi leader",
       note="Nguồn: r57, r58, r59. ⚠ r59 có ghi chú thực tế:『Message send ngay của remind là do "
            "bên web send nên CÓ update last message → Spec change』— tức nhánh remind từng có "
            "hành vi khác. Gắn MT-03, cần Leader xác nhận nhánh remind đã thống nhất chưa."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "Regression — nội dung last message khi thật sự có cập nhật (friend gửi tin đến)",
       BOT + "\n- Chuẩn bị friend có friend info「誕生日」đã có giá trị, 1 friend info đã bị xoá",
       "1. Với mỗi trường hợp dưới đây, cho friend GỬI TIN ĐẾN rồi bot trả lời tương ứng, "
       "sau đó đọc cột「最新メッセージ」ở màn friendlist:\n"
       "   a. text thường\n"
       "   b. text bắt đầu bằng {name}\n"
       "   c. text bắt đầu bằng mã friend info CÓ giá trị\n"
       "   d. text bắt đầu bằng mã friend info KHÔNG có giá trị\n"
       "   e. text bắt đầu bằng mã friend info ĐÃ BỊ XOÁ",
       "5 dạng nội dung text",
       "- a. Hiển thị đúng nội dung message\n"
       "- b. {name} được thay bằng tên friend\n"
       "- c. Mã friend info được thay bằng giá trị của friend\n"
       "- d. Vị trí mã friend info để TRỐNG, KHÔNG hiện mã thô\n"
       "- e. Vị trí mã friend info để TRỐNG, KHÔNG hiện mã thô",
       spec="Đã hỏi leader",
       note="Nguồn: r60-r64. TC gốc viết cho luồng send action ở friendlist, nhưng cột Actual "
            "ghi rõ『Spec change 4/2026: không update last message』→ kho chuyển thành TC hồi quy "
            "cho luồng CÒN cập nhật last message (friend gửi tin đến), giữ nguyên 5 quy tắc thay "
            "biến. Đây là suy luận của AI để không mất nội dung — cần Leader xác nhận cách xử lý."),

    tc("Bulk action — last message & bộ đếm 未確認", "OUT-TRUTH-001", "Normal",
       "Regression — nhãn last message cho message không phải text",
       BOT,
       "1. Với mỗi loại message dưới đây, tạo tình huống last message thật sự được cập nhật, "
       "rồi đọc cột「最新メッセージ」/ nội dung tin cuối:\n"
       "   panel button · ảnh · video · audio · stamp · location · group template nhiều loại",
       "7 loại message",
       "- panel button →「カルーセル」\n"
       "- ảnh →「画像」\n"
       "- video →「動画」\n"
       "- audio →「音声」\n"
       "- stamp →「スタンプ」\n"
       "- location →「位置」\n"
       "- group template nhiều loại → nhãn của message CUỐI CÙNG trong nhóm",
       spec="Đã hỏi leader",
       note="Nguồn: r65-r71 (7 dòng, mỗi dòng 1 nhãn khác nhau → giữ CHUNG 1 TC vì cùng một "
            "quy tắc『nhãn theo loại message』và cùng cách kiểm chứng; 7 giá trị liệt kê đủ ở "
            "cột Kết quả mong đợi). Cột Actual của cả 7 dòng đều ghi spec change 4/2026 → "
            "chuyển sang luồng còn cập nhật last message. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-001", "Normal",
       "Gửi action cho NHIỀU friend cùng lúc và gửi liên tiếp nhiều lần",
       BOT,
       "1. Ghi lại「最新メッセージ」của 10 friend\n"
       "2. Tích cả 10 friend → chạy action gửi text → reload, đọc lại 10 giá trị\n"
       "3. Chạy tiếp action gửi text cho cùng 10 friend, lặp 3 lần liên tiếp\n"
       "4. Reload, đọc lại 10 giá trị",
       "10 friend · gửi 1 lần rồi gửi liên tiếp 3 lần",
       "- Cả 10 friend nhận đủ tin ở mọi lần gửi\n"
       "- KHÔNG friend nào bị update last message hoặc last time\n"
       "- Cột「最新メッセージ」của cả 10 friend giữ nguyên giá trị ban đầu",
       spec="Đã hỏi leader",
       note="Nguồn: r72, r73. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "REG-SHARED-001", "Normal",
       "Regression — action từ tính năng KHÁC cũng không update last message",
       BOT,
       "1. Ghi lại「最新メッセージ」của các friend liên quan\n"
       "2. Chạy lần lượt các nguồn action ngoài friendlist, mỗi nguồn cho 1 friend:\n"
       "   a. Send Action line user: text · template · template + text · action khác\n"
       "   b. Job: action khi kết bạn · autoreply · scenario · broadcast · remind · "
       "action button/image map/richmenu\n"
       "3. Reload màn friendlist, đọc lại「最新メッセージ」",
       "10 nguồn action ngoài màn friendlist",
       "- Mọi friend đều nhận đúng action tương ứng\n"
       "- KHÔNG nguồn nào làm update last_message hoặc last_time_message\n"
       "- Cột「最新メッセージ」của tất cả friend giữ nguyên",
       spec="Đã hỏi leader",
       note="Nguồn: r74-r83 (10 dòng, cùng 1 kết quả mong đợi → giữ chung 1 TC, liệt kê đủ 10 "
            "nguồn ở cột Dữ liệu nhập). Đây là vùng regression rộng: fix ở friendlist không "
            "được làm hỏng các nguồn action khác. Gắn MT-03."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Bot KHÔNG bật tự động xác nhận — gửi action không đổi trạng thái và số 未確認",
       BOT_CONF + "\n- Bot TẮT setting tự động xác nhận tin nhắn",
       "1. Ghi lại trạng thái xác nhận của 2 friend và số 未確認 của bot\n"
       "2. Tích 2 friend → chạy action gửi text → đọc lại trạng thái + số 未確認\n"
       "3. Lặp lại với action gửi template\n"
       "4. Lặp lại với action không phải text/template (add tag)",
       "2 friend (1 đã xác nhận, 1 chưa) · 3 loại action · bot TẮT auto-confirm",
       "- Trạng thái xác nhận của cả 2 friend KHÔNG đổi sau cả 3 lần\n"
       "- Số 未確認 của bot KHÔNG đổi\n"
       "- Badge hiển thị số 未確認 trên menu cũng không đổi",
       spec="Đã hỏi leader",
       note="Nguồn: r84, r85, r86. ⭐ Spec-features KHÔNG ghi quy tắc auto-confirm khi chạy "
            "action từ friendlist → spec bỏ sót, xem MT-11."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Bot BẬT tự động xác nhận — gửi text/template chuyển friend chưa xác nhận sang đã xác nhận",
       BOT_CONF + "\n- Bot BẬT setting tự động xác nhận tin nhắn",
       "1. Ghi lại trạng thái xác nhận của 2 friend và số 未確認 của bot (VD 未確認 = 8)\n"
       "2. Tích 2 friend → chạy action gửi text\n"
       "3. Đọc lại trạng thái 2 friend và số 未確認\n"
       "4. Lặp lại với action gửi template (dùng 2 friend mới ở cùng 2 trạng thái)",
       "2 friend (1 đã xác nhận, 1 chưa) · bot BẬT auto-confirm · số 未確認 ban đầu = 8",
       "- Friend đang ĐÃ xác nhận: giữ nguyên trạng thái, số 未確認 không đổi vì friend này\n"
       "- Friend đang CHƯA xác nhận: chuyển thành ĐÃ xác nhận\n"
       "- Số 未確認 của bot giảm đúng 1 → còn 7\n"
       "- Kết quả giống nhau ở cả action text và action template",
       spec="Đã hỏi leader",
       note="Nguồn: r87, r88. Gắn MT-11 (spec bỏ sót quy tắc auto-confirm)."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Bot BẬT tự động xác nhận nhưng action KHÔNG phải text/template — không đổi trạng thái",
       BOT_CONF + "\n- Bot BẬT setting tự động xác nhận tin nhắn",
       "1. Ghi lại trạng thái 2 friend và số 未確認 của bot\n"
       "2. Tích 2 friend → chạy lần lượt 4 action: start scenario · start remind · "
       "add tag · ghi friend info\n"
       "3. Sau mỗi action, đọc lại trạng thái 2 friend và số 未確認",
       "2 friend · 4 action không phải text/template · bot BẬT auto-confirm",
       "- Trạng thái xác nhận của 2 friend KHÔNG đổi sau cả 4 action\n"
       "- Số 未確認 của bot KHÔNG đổi",
       spec="Đã hỏi leader",
       note="Nguồn: r89. Gắn MT-11."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Gửi action cho nhiều friend cùng lúc — số 未確認 giảm đúng bằng số friend chưa xác nhận",
       "- Đăng nhập Admin của bot BẬT setting tự động xác nhận\n"
       "- Chuẩn bị 10 friend: 6 CHƯA xác nhận + 4 ĐÃ xác nhận\n"
       "- Ghi lại số 未確認 hiện tại của bot (VD = 20)\n"
       "- Mở /basic/friendlist",
       "1. Tích cả 10 friend\n"
       "2. Chạy action gửi text\n"
       "3. Đọc lại trạng thái xác nhận của từng friend trong 10 friend\n"
       "4. Đọc lại số 未確認 của bot và badge trên menu",
       "10 friend (6 chưa xác nhận + 4 đã xác nhận) · số 未確認 ban đầu = 20",
       "- Cả 10 friend đều chuyển sang / giữ trạng thái ĐÃ xác nhận\n"
       "- Số 未確認 giảm đúng 6 → còn 14 (không giảm 10, không giảm 0)\n"
       "- Badge trên menu hiển thị đúng 14",
       spec="Đã hỏi leader",
       note="Nguồn: r90 — TC gốc CHỈ CÓ TIÊU ĐỀ (『Check case send action cho nhiều user cùng "
            "lúc』), không có kết quả mong đợi. Kết quả mong đợi do AI viết bằng cách áp quy tắc "
            "của r87-r89 cho nhóm nhiều friend + thêm phép tính tay — cần Leader xác nhận. "
            "Gắn MT-11."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Action qua job (> 200 friend) — quy tắc last message và auto-confirm giữ nguyên",
       "- Đăng nhập Admin của bot có > 200 friend, BẬT setting tự động xác nhận\n"
       "- Ghi lại số 未確認 của bot và「最新メッセージ」của 5 friend mẫu\n"
       "- Mở /basic/friendlist",
       "1. Tích 全選択 + checkbox chọn toàn bộ → chạy action gửi text\n"
       "2. Chờ job chạy xong\n"
       "3. Đọc lại「最新メッセージ」của 5 friend mẫu\n"
       "4. Đọc lại số 未確認 của bot\n"
       "5. Lặp lại với action start scenario / add tag (không phải text/template)",
       "> 200 friend → luồng action schedule · bot BẬT auto-confirm",
       "- Action text qua job: KHÔNG update last message/last time của bất kỳ friend nào\n"
       "- Action text qua job: các friend chưa xác nhận chuyển sang đã xác nhận, số 未確認 "
       "giảm đúng bằng số friend chưa xác nhận trong nhóm\n"
       "- Action start scenario / add tag qua job: KHÔNG đổi last message, KHÔNG đổi số 未確認",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r99-r111 (last message qua job) + r120-r126 (auto-confirm qua job) + r130. "
            "Gộp thành 1 TC vì cùng khẳng định『luồng job giữ nguyên quy tắc của luồng trực "
            "tiếp』. Gắn MT-03 + MT-11. RULE-08: job → PRODUCTION."),

    tc("Bulk action — last message & bộ đếm 未確認", "DATA-COUNT-001", "Normal",
       "Action qua job CÓ filter — chỉ friend thoả filter nhận action và đổi trạng thái",
       "- Đăng nhập Admin của bot có > 200 friend\n"
       "- Chuẩn bị TagA gắn cho 250 friend, trong đó 30 friend CHƯA xác nhận\n"
       "- Bot BẬT setting tự động xác nhận, ghi lại số 未確認\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai",
       "1. Lọc「タグ = TagA」→ tích 全選択 + checkbox (N = 250) → chạy action gửi text\n"
       "2. Chờ job chạy xong\n"
       "3. Đếm số friend nhận được tin (qua màn chat 1:1 / bằng cách gắn kèm tag mới)\n"
       "4. Kiểm tra 5 friend KHÔNG thuộc TagA xem có nhận tin không\n"
       "5. Đọc lại số 未確認 của bot",
       "TagA = 250 friend, 30 trong đó chưa xác nhận",
       "- Đúng 250 friend thoả filter nhận action\n"
       "- 5 friend không thoả filter KHÔNG nhận action\n"
       "- Số 未確認 giảm đúng 30\n"
       "- Trigger ở chat 1:1 hiển thị đủ các loại như case gửi toàn bộ friend "
       "(start/stop scenario · start/stop remind · send template · send text · block/ẩn friend)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r128, r129, r130, r131. Gắn MT-03 + MT-11."),

    # ═══════════ 10. Bulk action — lỗi & hiệu năng ═══════════
    tc("Bulk action — lỗi & hiệu năng", "MSG-005", "Abnormal",
       "Gửi action cho nhiều friend, một số friend lỗi giới hạn tin nhắn",
       "- Đăng nhập Admin của bot đã gần chạm giới hạn số tin gửi của LINE OA\n"
       "- Bot BẬT setting tự động xác nhận\n"
       "- Chuẩn bị sao cho khi gửi hàng loạt sẽ có friend gửi thành công và friend bị lỗi\n"
       "- Mở /basic/friendlist",
       "1. Tích nhiều friend → chạy action gửi text\n"
       "2. Ghi lại danh sách friend nhận được tin trên app LINE (nhóm thành công)\n"
       "3. Ghi lại danh sách friend không nhận được (nhóm lỗi)\n"
       "4. Mở màn 配信エラー (/basic/error-list-v2) tìm bản ghi lỗi\n"
       "5. Kiểm tra last message và trạng thái xác nhận của cả 2 nhóm",
       "nhóm friend gửi thành công + nhóm friend lỗi giới hạn tin nhắn",
       "- Nhóm thành công: nhận được tin trên app LINE; last message KHÔNG đổi; nếu bot bật "
       "auto-confirm thì chuyển sang đã xác nhận\n"
       "- Nhóm lỗi: KHÔNG nhận tin; last message KHÔNG đổi; trạng thái xác nhận KHÔNG đổi\n"
       "- Màn 配信エラー hiển thị message lỗi cho đúng nhóm friend bị lỗi\n"
       "- Lỗi ở một số friend KHÔNG làm dừng việc gửi cho các friend còn lại",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r91, r133. Gắn MT-03 (phần last message). RULE-08: giới hạn gửi tin + job "
            "→ PRODUCTION."),

    tc("Bulk action — lỗi & hiệu năng", "JOB-001", "Abnormal",
       "Job action schedule gửi lỗi TOÀN BỘ friend trong nhóm",
       "- Đăng nhập Admin của bot đã chạm giới hạn số tin gửi của LINE OA\n"
       "- Bot có > 200 friend\n"
       "- Ghi lại「最新メッセージ」của 5 friend mẫu và số 未確認 của bot",
       "1. Tích 全選択 + checkbox → chạy action gửi text (tạo action schedule)\n"
       "2. Chờ job chạy\n"
       "3. Mở màn 配信エラー kiểm tra bản ghi lỗi\n"
       "4. Đọc lại「最新メッセージ」của 5 friend mẫu và số 未確認\n"
       "5. Kiểm tra bản ghi action schedule sau khi job chạy xong",
       "> 200 friend, toàn bộ gửi lỗi",
       "- Màn 配信エラー hiển thị message lỗi\n"
       "- KHÔNG update last_time_message và last_message của friend nào\n"
       "- KHÔNG update trạng thái xác nhận, số 未確認 giữ nguyên\n"
       "- Bản ghi action schedule vẫn bị xoá sau khi chạy (chạy 1 lần), không lặp vô hạn",
       env="PRODUCTION",
       note="Nguồn: r132. RULE-08: job → PRODUCTION."),

    tc("Bulk action — lỗi & hiệu năng", "PERF-LARGE-001", "Normal",
       "Job gửi ĐÚNG và ĐỦ message cho toàn bộ friend trong nhóm — không sót, không trùng",
       "- Đăng nhập Admin của bot có > 1.000 friend\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai\n"
       "- Mở /basic/friendlist",
       "1. Tích 全選択 + checkbox chọn toàn bộ → ghi lại N\n"
       "2. Chạy action gồm: gửi text + gắn tag mới (để đếm được chính xác)\n"
       "3. Ghi lại thời điểm bắt đầu job\n"
       "4. Chờ job chạy xong, ghi lại thời điểm kết thúc\n"
       "5. Đếm số friend trên màn chi tiết tag\n"
       "6. Kiểm tra 5 friend ngẫu nhiên xem có nhận trùng 2 lần tin không",
       "> 1.000 friend",
       "- Số friend được gắn tag = N (không sót friend nào)\n"
       "- 5 friend kiểm tra chỉ nhận đúng 1 lần tin, không trùng\n"
       "- Job hoàn tất trong giới hạn 30 phút, không bị restart giữa chừng\n"
       "- Màn 配信エラー không có bản ghi lỗi mới",
       env="PRODUCTION",
       note="Nguồn: r127, r131. feature-spec.md §7.1: job timeout 30 phút → process exit + "
            "restart; xử lý bằng parallelStream nên có thể gây tải cao lên LINE API. "
            "RULE-08: performance + job → PRODUCTION."),

    tc("Bulk action — lỗi & hiệu năng", "PERF-LARGE-001", "Normal",
       "Tốc độ chạy action dây chuyền từ màn friendlist (action lồng nhiều tầng)",
       "- Đăng nhập Admin\n"
       "- Chuẩn bị chuỗi action lồng nhau: form → item select có action gắn tag → "
       "tag có action start scenario\n"
       "- Mở /basic/friendlist",
       "1. Tích 1 friend → chạy action gửi form đã chuẩn bị\n"
       "2. Cho friend chọn item select trong form\n"
       "3. Ghi lại thời gian từ lúc chọn tới lúc friend nhận message đầu của scenario\n"
       "4. Kiểm tra tag đã được gắn và scenario đã bắt đầu",
       "chuỗi 3 tầng: form → tag → scenario",
       "- Tag được gắn cho friend\n"
       "- Scenario bắt đầu chạy NGAY sau khi friend chọn item, không phải chờ chu kỳ job\n"
       "- Friend nhận được message đầu của scenario\n"
       "- Ghi lại thời gian thực tế để Leader chốt ngưỡng chấp nhận",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: TCsLine_Improve chung → tab「Improve speed」r4-r5 (『Friendlist』là 1 trong 2 "
            "màn action của web; case KH lỗi: send form → select → gắn tag → start scenario, "
            "ghi chú『chạy scenario luôn ngay sau khi select』). TC gốc không có ngưỡng thời gian "
            "cụ thể → cần Leader chốt. RULE-08: performance → PRODUCTION."),

    tc("Bulk action — lỗi & hiệu năng", "FUNC-SEQ-001", "Abnormal",
       "Lưu multi action ở màn friendlist nhiều lần liên tiếp và sau khi reload",
       "- Đăng nhập Admin\n"
       "- Đã tạo sẵn 1 scenario để gắn vào action\n"
       "- Mở /basic/friendlist",
       "1. Mở panel chọn action, cấu hình multi action có start scenario → lưu\n"
       "2. Lưu liên tiếp thêm 3 lần nữa mà không đóng panel\n"
       "3. Reload màn hình, mở lại panel action kiểm tra cấu hình đã lưu\n"
       "4. Tích 1 friend → chạy action → kiểm tra friend có nhận đúng không\n"
       "5. Lặp lại toàn bộ với multi action STOP scenario",
       "multi action start scenario · multi action stop scenario · lưu 4 lần liên tiếp",
       "- Cả 4 lần lưu đều thành công, không lỗi\n"
       "- Sau reload, cấu hình action vẫn đúng, không bị nhân bản hay mất mục\n"
       "- Friend nhận được action đúng như cấu hình\n"
       "- Kết quả giống nhau ở cả start và stop scenario",
       note="Nguồn: TCsLine_Improve chung → tab「Improve nhỏ」r510-r515 (SpecImprove #35842 — "
            "triển khai ngang lỗi array_search + array_splice không check false, dẫn tới lấy sai "
            "phần tử khi lưu multi action)."),
]
