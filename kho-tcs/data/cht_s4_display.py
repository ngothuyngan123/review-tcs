# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 4: reply/quote, hiển thị message, message hệ thống, marker & modal chi tiết action."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3, đang mở hội thoại friend A"
QUOTE = BOT + "\n- Hội thoại friend A đã có đủ các loại tin nhắn của cả 2 phía"
TMPL = ("template button standard (1 panel/nhiều panel × có ảnh/không ảnh) · "
        "template button color (tương tự) · template button ảnh (1 panel/nhiều panel) · "
        "quick reply text (1 nút/nhiều nút) · quick reply ảnh (1 nút/nhiều nút)")

S4 = [
    # ═══════════════ Reply / quote message ═══════════════
    tc("Reply / quote message", "UI-002", "Normal",
       "Icon trả lời và icon AI trên tin nhắn — màu mặc định và hiệu ứng khi rê chuột",
       QUOTE,
       "1. Rê chuột lên 1 tin nhắn của friend gửi → quan sát icon mũi tên và icon AI\n"
       "2. Đọc màu và tooltip của từng icon\n3. Lặp lại với tin do bot gửi",
       "Tin của friend và tin của bot, loại text",
       "- Mặc định 2 icon màu #888888\n"
       "- Rê chuột vào icon trả lời: màu #759CD0, hiện tooltip「このメッセージに返信」\n"
       "- Rê chuột vào icon AI (chỉ ở tin của friend): màu chuyển gradient, hiện tooltip「AIで返信メッセージを自動生成」\n"
       "- Tin của bot: chỉ có icon trả lời, không có icon AI",
       spec="Spec không ghi",
       note="MT-20: spec chat-11 không nhắc tính năng AI tạo tin trả lời. Nguồn: Content: Hiển thị msg r6-r13"),

    tc("Reply / quote message", "UI-002", "Normal",
       "Loại tin nào có icon trả lời — text, ảnh, video, PDF có; audio và vị trí không có",
       QUOTE,
       "1. Rê chuột lần lượt lên từng loại tin ở cột Dữ liệu test (cả tin của friend và tin của bot)\n"
       "2. Ghi nhận tin nào hiện icon trả lời",
       "text · ảnh · video · PDF · audio · vị trí · sticker · image map",
       "- Text, ảnh, video, PDF: CÓ icon trả lời\n"
       "- Audio và vị trí: KHÔNG có icon trả lời\n"
       "- Image map: không có trích dẫn; ảnh thường thì có",
       spec="Spec không ghi",
       note="MT-02: spec chat-11 chỉ có cột quote_token/quote_message_id/quote_message_content ở db-mapping.md:119-121, "
            "KHÔNG có quy tắc nào về trả lời. Nguồn: Content: Hiển thị msg r916, r917, r924, r926, r961, r962, r965"),

    tc("Reply / quote message", "UI-001", "Normal",
       "Trích dẫn tin của BẠN BÈ — khung trích dẫn hiện avatar, tên và nội dung tương ứng",
       QUOTE,
       "1. Bấm icon trả lời trên từng loại tin của friend ở cột Dữ liệu test\n"
       "2. Quan sát khung trích dẫn phía trên ô nhập tin",
       "text · sticker · ảnh · video · tin trả lời nút bấm",
       "- Khung trích dẫn hiện avatar và tên LINE của friend\n"
       "- Text: hiện nội dung, text dài thì cắt bớt kèm dấu ba chấm\n"
       "- Sticker: hiện chữ スタンプ + hình sticker\n"
       "- Ảnh: hiện ảnh + chữ 画像\n- Video: hiện video + chữ 動画",
       spec="Spec không ghi",
       note="MT-02. Nguồn: Content: Hiển thị msg r910-r918"),

    tc("Reply / quote message", "UI-001", "Normal",
       "Trích dẫn tin của BOT — khung trích dẫn hiện đúng profile người gửi tin gốc",
       QUOTE + "\n- Có tin gửi bằng profile mặc định và tin gửi bằng profile khác",
       "1. Bấm icon trả lời trên tin bot gửi bằng profile MẶC ĐỊNH → quan sát khung trích dẫn\n"
       "2. Bấm icon trả lời trên tin bot gửi bằng profile KHÁC → quan sát\n"
       "3. Lặp lại với từng loại tin ở cột Dữ liệu test",
       "text · ảnh · video · PDF · sticker · " + TMPL,
       "- Khung trích dẫn hiện đúng avatar + tên của profile đã gửi tin gốc (không phải profile đang chọn)\n"
       "- Nội dung trích dẫn hiển thị đúng theo từng loại tin",
       spec="Spec không ghi",
       note="MT-02. Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r919-r943"),

    tc("Reply / quote message", "STATE-CLEAN-001", "Normal",
       "Bấm X trên khung trích dẫn — chỉ xoá trích dẫn, giữ nội dung đang gõ",
       QUOTE,
       "1. Trích dẫn 1 tin, CHƯA nhập nội dung → bấm X → quan sát → gõ tin và gửi\n"
       "2. Trích dẫn lại, ĐÃ nhập nội dung → bấm X → quan sát ô nhập → bấm gửi",
       "2 trường hợp: chưa nhập và đã nhập nội dung",
       "- Trường hợp 1: khung trích dẫn biến mất; gửi tin bình thường không có trích dẫn\n"
       "- Trường hợp 2: khung trích dẫn biến mất nhưng NỘI DUNG ĐANG GÕ vẫn giữ; gửi ra tin thường",
       note="Nguồn: Content: Hiển thị msg r944, r945"),

    tc("Reply / quote message", "MSG-001", "Normal",
       "Gửi tin trả lời — chat 1:1 và app LINE đều hiển thị dạng trích dẫn",
       QUOTE,
       "1. Trích dẫn 1 tin text của friend, nhập nội dung trả lời (có xuống dòng) → gửi\n"
       "2. Quan sát tin vừa gửi ở chat 1:1: khung trích dẫn + nội dung trả lời\n"
       "3. Kiểm tra trên app LINE của friend\n4. Lặp lại: trả lời bằng sticker",
       "Trả lời bằng text nhiều dòng; trả lời bằng sticker",
       "- Chat 1:1: tin gửi có khung trích dẫn tin gốc + nội dung trả lời\n"
       "- App LINE: friend thấy đúng dạng trả lời trích dẫn\n"
       "- Profile người gửi và thời gian hiển thị đúng",
       spec="Spec không ghi",
       note="MT-02. Nguồn: Content: Hiển thị msg r946, r947, r953-r957"),

    tc("Reply / quote message", "MSG-004", "Abnormal",
       "Trả lời bằng media / template — không giữ trích dẫn, gửi như tin thường",
       QUOTE,
       "1. Trích dẫn 1 tin của friend\n2. Chọn gửi ảnh (hoặc video, audio, file, template)\n3. Bấm gửi\n"
       "4. Quan sát tin ở chat 1:1 và app LINE",
       "Trả lời bằng: ảnh · video · audio · file · template",
       "- Tin gửi ra là tin THƯỜNG, KHÔNG có khung trích dẫn\n- Cả chat 1:1 và app LINE đều không hiện trích dẫn",
       spec="Spec không ghi",
       note="MT-02. Nguồn: Content: Hiển thị msg r948"),

    tc("Reply / quote message", "STATE-001", "Normal",
       "Trích dẫn tin này rồi trích dẫn tin khác — giữ tin trích dẫn cuối cùng",
       QUOTE,
       "1. Trích dẫn tin M1\n2. Chưa gửi, trích dẫn tiếp tin M2\n3. Quan sát khung trích dẫn\n4. Gửi và kiểm tra",
       "2 tin M1, M2 khác nhau",
       "- Khung trích dẫn hiện tin M2 (tin trích dẫn cuối cùng)\n- Tin gửi ra trích dẫn đúng M2",
       note="Nguồn: Content: Hiển thị msg r949"),

    tc("Reply / quote message", "STATE-CLEAN-001", "Abnormal",
       "Trích dẫn rồi chuyển sang bạn bè khác — trích dẫn và nội dung bị xoá",
       QUOTE + "\n- Có friend A và friend B",
       "1. Ở hội thoại A: trích dẫn 1 tin, nhập nội dung, CHƯA gửi\n"
       "2. Nhập từ khoá tìm kiếm bạn bè → hội thoại đầu tiên hiện lên\n"
       "3. Quan sát khung trích dẫn và ô nhập\n"
       "4. Lặp lại: trích dẫn + nhập nội dung ở A rồi click sang B",
       "Trích dẫn ở A rồi tìm kiếm / chuyển sang B",
       "- Cả 2 cách: khung trích dẫn và nội dung đang gõ đều bị XOÁ\n"
       "- Không bị lỗi khi bấm gửi ở hội thoại mới",
       note="Bug Support #29057 (03/2025) — trước fix giữ lại trích dẫn gây lỗi khi gửi. "
            "Nguồn: Content: Send message r1202-r1204 + Content: Hiển thị msg r950"),

    tc("Reply / quote message", "MSG-003", "Normal",
       "Bạn bè trích dẫn tin của BOT trên app LINE — chat 1:1 hiển thị đúng dạng trích dẫn",
       QUOTE + "\n- Bot đã gửi cho friend A đủ loại tin ở cột Dữ liệu test (thử cả tin gửi từ web và tin gửi từ job)",
       "1. Trên app LINE, friend A trích dẫn 1 tin của bot và trả lời\n"
       "2. Quan sát tin đó ở chat 1:1: khung trích dẫn, profile, nội dung\n"
       "3. Lặp lại với từng loại tin ở cột Dữ liệu test",
       "text · ảnh · video · audio · PDF · vị trí · sticker · " + TMPL,
       "- Chat 1:1 hiển thị dạng trích dẫn\n"
       "- Phần người gửi của tin gốc: hiện đúng profile đã gửi (mặc định hoặc profile khác)\n"
       "- Hiện đúng nội dung tin gốc và nội dung tin trả lời của friend",
       env="PRODUCTION", spec="Spec không ghi",
       note="MT-02 + Feature #28618 (02/2025), Support #27755. Gộp vì cùng kết quả. "
            "Nguồn: Content: Hiển thị msg r994-r1014"),

    tc("Reply / quote message", "MSG-003", "Normal",
       "Bạn bè trích dẫn tin CHÍNH MÌNH đã gửi — chat 1:1 hiện avatar và tên LINE của bạn bè",
       QUOTE,
       "1. Cho friend A gửi các loại tin ở cột Dữ liệu test cho bot\n"
       "2. Cho friend A trích dẫn chính tin của mình và trả lời\n3. Quan sát ở chat 1:1",
       "text · sticker · ảnh · video · audio · file · tin trả lời nút bấm · vị trí",
       "- Chat 1:1 hiển thị dạng trích dẫn\n"
       "- Phần người gửi của tin gốc: hiện ảnh và tên LINE của friend\n"
       "- Hiện đúng nội dung tin gốc và tin trả lời",
       env="PRODUCTION", spec="Spec không ghi",
       note="MT-02. Nguồn: Content: Hiển thị msg r1015-r1022"),

    tc("Reply / quote message", "SYNC-APP-001", "Normal",
       "Trích dẫn hiển thị đúng trên APP MOBILE LME",
       "- App mobile LME đăng nhập account admin bot A, mở hội thoại friend A\n"
       "- Đã có sẵn tin trích dẫn của friend (trích dẫn tin bot và trích dẫn tin của chính friend)",
       "1. Ở app mobile: mở hội thoại friend A\n2. Quan sát các tin có trích dẫn\n"
       "3. Đối chiếu với hiển thị trên chat 1:1 web",
       "Trích dẫn tin bot (đủ loại) và trích dẫn tin friend (đủ loại)",
       "- App mobile hiển thị dạng trích dẫn giống web: đúng profile, đúng nội dung tin gốc và tin trả lời",
       env="PRODUCTION",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r1023-r1051"),

    tc("Reply / quote message", "MSG-003", "Normal",
       "Mọi đường gửi tin của LME — bạn bè trích dẫn lại đều hiển thị được ở chat 1:1",
       QUOTE + "\n- Đã chuẩn bị đủ các đường gửi ở cột Dữ liệu test",
       "1. Với mỗi đường gửi: gửi tin cho friend A\n"
       "2. Trên app LINE, friend A trích dẫn tin đó và trả lời\n"
       "3. Kiểm tra chat 1:1 có hiển thị dạng trích dẫn không",
       "WEB: chat 1:1 (text/media/PDF/sticker/text+media/text+PDF/template đơn/template nhóm/multi action) · "
       "send test (Broadcast, Template, Remind, Scenario) · trả lời ở talk list · remind gửi ngay · "
       "action text của salon/lesson/kết bạn/QR landing/form · action gắn tag\n"
       "APP: chat 1:1 (text/media/file/sticker/template) · action tag · salon · lesson\n"
       "JOB: Broadcast · Scenario · Event remind (cũ và mới) · action khi có callback · tin gửi giãn cách · "
       "gửi lại tin lỗi · lịch gửi của chat 1:1 · action schedule · nút bấm / rich menu / image map / video · "
       "action ở các tính năng khác · send test toàn bộ scenario",
       "- Với TẤT CẢ đường gửi: friend nhận được tin và khi trích dẫn thì chat 1:1 hiển thị đúng dạng trích dẫn",
       env="PRODUCTION", spec="Spec không ghi",
       note="MT-02. Gộp ~50 đường gửi vì CÙNG kết quả. Nguồn: Content: Hiển thị msg r1054-r1137",),

    tc("Reply / quote message", "COMPAT-LEGACY-001", "Abnormal",
       "Bạn bè trích dẫn tin bot gửi TRƯỚC KHI có tính năng trích dẫn — hiển thị như tin thường",
       QUOTE + "\n- Có tin bot gửi từ trước ngày phát hành tính năng trích dẫn",
       "1. Trên app LINE, friend trích dẫn 1 tin cũ của bot\n2. Quan sát tin đó ở chat 1:1",
       "Tin bot gửi trước khi phát hành Feature #28618",
       "- Chat 1:1 hiển thị tin GIỐNG trường hợp không trích dẫn (không có khung trích dẫn)\n"
       "- Không lỗi, không màn trắng",
       note="Nguồn: Content: Hiển thị msg r1138"),

    tc("Reply / quote message", "MSG-001", "Normal",
       "Bot trích dẫn tin — kiểm tra ở cả web và app mobile",
       QUOTE,
       "1. Trên WEB: trích dẫn 1 tin của friend rồi trả lời → kiểm tra chat 1:1 và app LINE\n"
       "2. Trên WEB: trích dẫn 1 tin do chính bot gửi rồi trả lời → kiểm tra\n"
       "3. Lặp lại toàn bộ trên APP MOBILE",
       "Bot trích dẫn tin friend và tin của chính bot, trên web và app",
       "- Cả 4 trường hợp: trích dẫn thành công, chat 1:1 và app LINE đều hiển thị dạng trích dẫn",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r1139, r1140"),

    tc("Reply / quote message", "UI-002", "Abnormal",
       "Bấm vào khung trích dẫn — không nhảy tới tin gốc",
       QUOTE + "\n- Có tin dạng trích dẫn trong lịch sử",
       "1. Cuộn tới 1 tin có khung trích dẫn\n2. Bấm vào khung trích dẫn\n3. Quan sát khung hội thoại",
       "1 tin có trích dẫn",
       "- KHÔNG cuộn tới tin gốc (chưa hỗ trợ)\n- Không lỗi JS, không màn trắng",
       spec="Spec không ghi",
       note="Nguồn: Content: Hiển thị msg r991 — TC gốc ghi rõ 「không support」"),

    # ═══════════════ Hiển thị message — media & định dạng ═══════════════
    tc("Hiển thị message — media & định dạng", "UI-FIELD-001", "Normal",
       "Dòng phân nhóm theo ngày trong lịch sử chat",
       BOT + "\n- Hội thoại friend A có tin nhắn ở 3 ngày khác nhau, trong đó có hôm nay",
       "1. Mở hội thoại friend A, cuộn hết lịch sử\n"
       "2. Quan sát dòng phân nhóm ngày giữa các cụm tin nhắn\n"
       "3. Đọc định dạng ngày của dòng phân nhóm\n"
       "4. Gửi 1 tin mới hôm nay → kiểm tra tin nằm đúng dưới dòng phân nhóm của hôm nay",
       "Tin nhắn ở 3 ngày: hôm nay, hôm qua và 1 ngày cũ hơn",
       "- Mỗi ngày có tin nhắn đều có 1 dòng phân nhóm ngày riêng, định dạng kiểu 2026年03月24日\n"
       "- Tin nhắn được nhóm đúng dưới dòng ngày tương ứng, không lẫn sang ngày khác\n"
       "- Tin mới gửi hôm nay nằm dưới dòng phân nhóm của hôm nay",
       note="Field Traceability §4.2 #1 (feature-spec.md:389) — corpus KHÔNG có TC riêng cho dòng phân nhóm ngày, "
            "đây là TC lấp GAP do AI viết theo spec, CẦN LEADER XÁC NHẬN"),

    tc("Hiển thị message — media & định dạng", "UI-FIELD-001", "Normal",
       "Tin BOT gửi — hiển thị đúng thời gian, tên người gửi và nội dung",
       BOT + "\n- Bot đã gửi cho friend A đủ các loại ở cột Dữ liệu test",
       "1. Với mỗi loại tin: đọc thời gian, tên người gửi và nội dung trong bong bóng\n"
       "2. Đối chiếu tên người gửi với tên staff/profile đã dùng",
       "Ảnh (dọc/ngang/vuông) · video (dọc/ngang) · audio (tên + dung lượng) · PDF (tên + link) · vị trí (địa chỉ)",
       "- Thời gian hiển thị theo định dạng MM/DD HH:mm (ví dụ 09/30 13:45)\n"
       "- Tên người gửi hiển thị đúng tên staff/profile đã dùng để gửi\n"
       "- Ảnh/video hiện đúng tỉ lệ; audio hiện tên và dung lượng; PDF hiện tên có đuôi .pdf và link; vị trí hiện địa chỉ",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r80-r106"),

    tc("Hiển thị message — media & định dạng", "UI-FIELD-001", "Normal",
       "Tin BẠN BÈ gửi — hiển thị đúng thời gian, tên bạn bè và nội dung",
       BOT + "\n- Friend A đã gửi đủ các loại tin ở cột Dữ liệu test",
       "1. Với mỗi loại tin: đọc thời gian, tên người gửi và nội dung\n"
       "2. Đối chiếu tên với tên LINE của friend A",
       "Ảnh (dọc/ngang/vuông) · video (dọc/ngang) · audio · PDF · vị trí",
       "- Thời gian định dạng MM/DD HH:mm\n- Tên người gửi là tên LINE của friend A\n"
       "- Nội dung từng loại hiển thị đúng như tin bot gửi",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r107-r133"),

    tc("Hiển thị message — media & định dạng", "OUT-PREVIEW-001", "Normal",
       "Xem trước và tải file media từ chat 1:1",
       BOT + "\n- Hội thoại có ảnh, video, audio, PDF của cả bot và friend",
       "1. Click vào ảnh → quan sát bản xem trước\n2. Thử phóng to / thu nhỏ trong bản xem trước\n"
       "3. Click tải ảnh ở ngoài khung hội thoại 1 lần → đếm số file tải về\n"
       "4. Click tải trong bản xem trước → đếm\n5. Lặp lại với video, audio\n"
       "6. Với PDF và vị trí: click link → quan sát tab mở ra",
       "Ảnh, video, audio, PDF, vị trí của cả bot và friend",
       "- Click ảnh: hiện ảnh giữa màn hình, nền phía sau tối\n"
       "- Phóng to/thu nhỏ: KHÔNG hoạt động (thư viện khác thiết kế) — ghi rõ ở evidence\n"
       "- Tải 1 lần: chỉ tải về 1 bản, không tải trùng\n"
       "- PDF và vị trí: link mở ở TAB MỚI",
       note="Gộp vì cùng chuỗi thao tác. Nguồn: Content: Hiển thị msg r82-r85, r102, r106, r109-r112"),

    tc("Hiển thị message — media & định dạng", "COMPAT-LEGACY-001", "Normal",
       "Tin nhắn dữ liệu CŨ — hiển thị được đủ loại, phần thiếu thông tin thì hiển thị rút gọn",
       BOT + "\n- Hội thoại có tin nhắn từ bảng dữ liệu cũ (trước 2023) của cả bot và friend",
       "1. Cuộn tới vùng tin nhắn cũ\n2. Với mỗi loại tin: kiểm tra hiển thị, xem trước và tải\n"
       "3. So sánh với hiển thị của tin dữ liệu mới",
       "Ảnh · video · audio · PDF · vị trí — dữ liệu cũ, của cả bot và friend",
       "- Tất cả loại tin cũ đều hiển thị được, xem trước và tải được\n"
       "- Audio dữ liệu cũ: nếu dữ liệu chỉ có đường dẫn thì hiển thị rút gọn; nếu có tên và dung lượng thì hiển thị "
       "như thiết kế mới\n- Không lỗi, không màn trắng",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r135-r182"),

    tc("Hiển thị message — media & định dạng", "MSG-004", "Abnormal",
       "File media lỗi (đường dẫn hỏng) — hiện thông báo lỗi thay vì vỡ giao diện",
       BOT + "\n- Nhờ Dev sửa đường dẫn file của 1 tin nhắn thành đường dẫn sai (thêm/bớt ký tự)",
       "1. Mở hội thoại chứa tin nhắn có đường dẫn hỏng\n2. Quan sát bong bóng tin đó\n"
       "3. Thử click vào tin\n4. Lặp lại với tin dữ liệu cũ",
       "Đường dẫn file bị sửa sai, cả dữ liệu mới và dữ liệu cũ",
       "- Hiển thị thông báo「LINE公式アカウント側の不具合によりメッセージの受信ができませんでした。"
       "受信したメッセージはLINE公式アカウント管理画面のチャットからご確認ください。」\n"
       "- Không vỡ giao diện, không lỗi JS",
       note="Nguồn: Content: Hiển thị msg r134, r183"),

    tc("Hiển thị message — media & định dạng", "UI-FIELD-001", "Normal",
       "Tin template BUTTON — hiển thị đủ panel, ảnh, tiêu đề, nút và điều hướng panel",
       BOT + "\n- Bot đã gửi template button đủ loại ở cột Dữ liệu test",
       "1. Với mỗi loại: kiểm tra profile (tên + ảnh), thời gian, tên người gửi\n"
       "2. Kiểm tra nội dung: ảnh, tiêu đề, mô tả, tên nút\n"
       "3. Với template nhiều panel: kiểm tra icon điều hướng ở panel đầu, giữa và cuối",
       TMPL,
       "- Profile, thời gian, tên người gửi hiển thị đúng\n"
       "- Nội dung panel đầy đủ (ảnh/tiêu đề/mô tả/nút)\n"
       "- Nhiều panel: panel đầu chỉ có nút sang phải; panel giữa có cả 2 nút; panel cuối chỉ có nút sang trái\n"
       "- Số icon điều hướng khớp số panel",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r638-r665"),

    tc("Hiển thị message — media & định dạng", "SYNC-APP-001", "Normal",
       "Profile người gửi thay đổi — tin cũ và tin mới hiển thị đúng profile tương ứng",
       BOT + "\n- Đã có tin gửi bằng profile P1",
       "1. Ghi lại profile hiển thị của tin cũ\n2. Sửa tên và ảnh của P1 → lưu\n"
       "3. Quan sát tin CŨ ở chat 1:1\n4. Gửi tin MỚI bằng P1, quan sát",
       "Sửa profile P1 đang được dùng",
       "- Ghi nhận thực tế: tin CŨ hiển thị profile cũ hay đã đổi theo\n"
       "- Tin MỚI chắc chắn hiển thị profile đã sửa\n"
       "- Đối chiếu với hành vi xoá profile (xem TC 「Xoá profile — ảnh hưởng…」)",
       spec="Đã hỏi leader",
       note="Liên quan cùng vấn đề chưa chốt với TC xoá profile ở nhóm Profile người gửi. "
            "Nguồn: Content: Hiển thị msg r640"),

    tc("Hiển thị message — media & định dạng", "COMPAT-LEGACY-001", "Normal",
       "Tin dạng 紹介 (giới thiệu) — chỉ hiển thị được tin cũ, không tạo mới",
       BOT + "\n- Có template dạng 紹介 cũ trong hệ thống",
       "1. Kiểm tra ở màn Quản lý template có tạo mới được template 紹介 không\n"
       "2. Gửi template 紹介 cũ cho friend A qua từng đường ở cột Dữ liệu test\n"
       "3. Quan sát hiển thị ở chat 1:1 và app LINE",
       "Gửi qua: send test · gửi template · multi action · callback (job) · Broadcast (job)",
       "- KHÔNG tạo mới được template dạng 紹介\n"
       "- Template 紹介 cũ vẫn gửi được qua mọi đường và hiển thị đúng ở chat 1:1 và app LINE",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r76, r77, r1385-r1389"),

    tc("Hiển thị message — media & định dạng", "UI-FIELD-001", "Normal",
       "Tin nhắn hiển thị tên STAFF khi staff thao tác gửi",
       BOT + "\n- Có account staff của bot A",
       "1. Đăng nhập bằng account staff, gửi lần lượt các loại ở cột Dữ liệu test cho friend A\n"
       "2. Đăng nhập lại bằng user chính, mở hội thoại friend A\n"
       "3. Đọc tên người gửi của từng tin",
       "Gửi template · gửi multi action · send test",
       "- Mọi tin đều hiển thị tên người gửi là tên của STAFF đã thao tác\n"
       "- Tin gửi qua multi action: tên staff hiển thị trong phần thông tin nguồn gửi",
       note="Nguồn: Content: Hiển thị msg r1422-r1424 + Content: Send message r9, r10"),

    # ═══════════════ Message hệ thống — kết bạn, block, ẩn ═══════════════
    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Kết bạn MỚI qua QR landing — message hệ thống hiện tên QR và ghi chú lịch sử",
       BOT + "\n- Đã tạo QR landing tên「テスト QR」\n- Tài khoản LINE T1 CHƯA từng kết bạn với bot A",
       "1. Cho T1 quét QR landing để kết bạn\n2. Mở hội thoại T1 ở chat 1:1\n"
       "3. Đọc message hệ thống: avatar, tên, ngày giờ, tên QR, ghi chú\n"
       "4. Kiểm tra DB: conversation.is_old_friend và trường lưu tên QR trong bảng tin nhắn",
       "Tài khoản LINE mới hoàn toàn, kết bạn qua QR landing",
       "- Message hệ thống hiện: tên friend + ngày giờ + 新規友だち + 流入経路 + tên QR + "
       "ghi chú「※ LINE公式アカウント側の1:1チャットにはこの友だちは表示されていない場合があります。」\n"
       "- Tên hiển thị lấy システム表示名, không có thì lấy LINE名\n"
       "- DB: is_old_friend = 0; trường lưu tên QR có giá trị",
       note="Nguồn: Content: Hiển thị msg r14, r22-r26"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Kết bạn MỚI qua các đường khác QR — message KHÔNG hiện tên QR",
       BOT + "\n- Tài khoản LINE T2, T3, T4 chưa từng kết bạn với bot A",
       "1. Với mỗi đường ở cột Dữ liệu test: cho 1 tài khoản kết bạn\n"
       "2. Mở hội thoại tương ứng, đọc message hệ thống",
       "Link/QR kết bạn của bot · mở link booking / form / item rồi kết bạn · link của đối tác giới thiệu",
       "- Message hệ thống hiện 新規友だち và dòng 通常友だち追加URL\n"
       "- KHÔNG hiện tên QR landing",
       note="Gộp 3 đường vì cùng kết quả. Nguồn: Content: Hiển thị msg r15-r17"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Kết bạn LẠI sau khi đã bị xoá khỏi hệ thống — message hiện tên QR nếu quét QR",
       BOT + "\n- Friend T5 đã bị xoá bản ghi ở LME (xoá từ màn chat 1:1 hoặc my_page) nhưng vẫn là bạn trên LINE",
       "1. Cho T5 quét QR landing để kết bạn lại\n2. Mở hội thoại T5, đọc message hệ thống\n"
       "3. Lặp lại với các đường khác (link bot, link booking/form/item, link đối tác)",
       "T5 kết bạn lại qua QR landing và qua 3 đường khác",
       "- Qua QR landing: message hiện TÊN QR đã tạo\n"
       "- Qua 3 đường khác: message hiện 通常友だち追加URL, không hiện tên QR",
       note="Nguồn: Content: Hiển thị msg r18-r21"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Kết bạn CŨ (bạn bè cũ trên LINE, chưa có dữ liệu ở LME) — message ghi rõ không có lịch sử cũ",
       BOT + "\n- Tài khoản LINE T6 đang là bạn của bot trên LINE nhưng chưa có bản ghi ở LME",
       "1. Với mỗi đường ở cột Dữ liệu test: kích hoạt để LME ghi nhận T6\n"
       "2. Mở hội thoại T6, đọc message hệ thống\n"
       "3. Kiểm tra DB: conversation.is_old_friend",
       "Quét QR landing · link/QR kết bạn của bot · mở link booking/form/item · link đối tác · gửi tin cho bot",
       "- Message hiện ngày giờ + 既存友だち + nguồn (tên QR nếu qua QR, hoặc 通常友だち追加URL, "
       "hoặc メッセージ受信により追加) + ghi chú「※過去のトーク履歴はエルメには表示されません」\n"
       "- DB: is_old_friend = 1\n- Lịch sử chat trước đó KHÔNG hiển thị ở chat 1:1",
       note="Gộp 5 đường vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r29-r33, r38-r43"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Bỏ block rồi kết bạn lại — message hiện 「ブロックを解除しました」",
       BOT + "\n- Friend T7 đã có bản ghi ở LME và đang block bot",
       "1. Cho T7 bỏ block bot bằng từng cách ở cột Dữ liệu test\n"
       "2. Mở hội thoại T7, đọc message hệ thống: avatar, tên, ngày giờ, tên QR (nếu có)\n"
       "3. Kiểm tra DB: conversation.is_blocked",
       "Bỏ block qua: QR landing · link/QR kết bạn của bot · link booking/form/item · link đối tác",
       "- Message hiện ngày giờ +「ブロックを解除しました」\n"
       "- Riêng qua QR landing: hiện thêm 流入経路 + tên QR\n- DB: is_blocked = 0",
       note="Nguồn: Content: Hiển thị msg r34-r37, r53-r65"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Bạn bè block bot — message hệ thống và không thao tác được",
       BOT + "\n- Friend T8 đang là bạn bình thường",
       "1. Cho T8 block bot trên app LINE\n2. Mở hội thoại T8 ở chat 1:1\n"
       "3. Đọc message hệ thống: avatar, tên, ngày giờ, nội dung\n"
       "4. Thử gõ và gửi tin\n5. Kiểm tra DB: is_blocked và trường lưu thời điểm block",
       "Friend T8 block bot",
       "- Message hiện avatar + tên friend + ngày giờ block + text「ブロックされました」\n"
       "- Không thao tác gửi tin được\n- DB: is_blocked = 1, trường thời điểm block có giá trị",
       note="Nguồn: Content: Hiển thị msg r47-r52"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FRIEND-001", "Normal",
       "Bot block bạn bè — message hiện tên staff thao tác",
       BOT + "\n- Friend T9 đang bình thường",
       "1. Bot block T9 (qua modal quick action)\n2. Mở hội thoại T9\n"
       "3. Đọc message hệ thống: tên staff, nội dung, ngày giờ",
       "Bot block friend T9",
       "- Message hiện tên staff thao tác + text「ブロックしました」+ ngày giờ định dạng MM/DD HH:mm",
       note="Nguồn: Content: Hiển thị msg r44-r46"),

    tc("Message hệ thống — kết bạn, block, ẩn", "FUNC-001", "Normal",
       "Ẩn bạn bè — có lưu message hệ thống; bỏ ẩn thì KHÔNG lưu",
       BOT + "\n- Friend T10 đang hiển thị bình thường",
       "1. Ẩn T10 → mở hội thoại T10 → đọc message hệ thống\n"
       "2. Bỏ ẩn T10 → mở lại hội thoại → kiểm tra có message mới không",
       "Ẩn rồi bỏ ẩn friend T10",
       "- Khi ẩn: có message hệ thống hiện tên staff + text「非表示しました」+ ngày giờ MM/DD HH:mm\n"
       "- Khi bỏ ẩn: KHÔNG sinh message hệ thống nào",
       note="Nguồn: Content: Hiển thị msg r66-r69"),

    tc("Message hệ thống — kết bạn, block, ẩn", "MSG-003", "Normal",
       "Bạn bè thu hồi tin trên app LINE — nội dung tin đổi thành thông báo thu hồi, thời gian giữ nguyên",
       BOT + "\n- Friend A đã gửi ≥3 tin cho bot",
       "1. Ghi lại nội dung và thời gian của 3 tin\n2. Cho A thu hồi 1 tin trên app LINE\n"
       "3. Quan sát tin đó ở chat 1:1: nội dung và thời gian\n4. Thu hồi thêm 2 tin nữa → quan sát",
       "3 tin nhắn của friend, thu hồi lần lượt",
       "- Mỗi tin bị thu hồi: nội dung đổi thành「友だちがメッセージを送信取り消しました」\n"
       "- Thời gian của tin KHÔNG đổi\n- Các tin còn lại không bị ảnh hưởng",
       note="Nguồn: Content: Hiển thị msg r70-r73"),

    tc("Message hệ thống — kết bạn, block, ẩn", "UI-002", "Normal",
       "Rê chuột vào dòng chữ đỏ trong message kết bạn — hiện chú thích",
       BOT + "\n- Có message hệ thống kết bạn mới trong hội thoại",
       "1. Rê chuột vào dòng chữ màu đỏ trong message kết bạn\n2. Đọc nội dung hiện ra\n3. Click vào dòng đó",
       "Message kết bạn mới có dòng chữ đỏ",
       "- Rê chuột: hiện「友だち側からメッセージを送ってもらうことで LINE公式アカウント側のチャットにも表示されます。」\n"
       "- Click: không xảy ra hành động gì",
       note="Nguồn: Content: Hiển thị msg r27, r28"),

    # ═══════════════ Marker & modal chi tiết action ═══════════════
    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Tin gửi bằng action — có dấu hiệu nhận biết, ngày giờ và nút xem chi tiết",
       BOT + "\n- Đã cấu hình action gửi 1 tin và action gửi nhiều tin cho friend A",
       "1. Kích hoạt action gửi 1 tin → quan sát ở chat 1:1\n"
       "2. Kích hoạt action gửi nhiều tin → quan sát cách nhóm\n"
       "3. Đọc ngày giờ và tìm nút xem chi tiết",
       "Action gửi 1 tin và action gửi nhiều tin",
       "- Tin có dấu hiệu nhận biết là gửi bằng action\n"
       "- Action gửi nhiều tin: các tin được GỘP vào 1 dấu hiệu chung\n"
       "- Hiện ngày giờ gửi định dạng 2024年10月01日（金） 13:20 và có nút xem chi tiết",
       note="Nguồn: Content: Hiển thị msg r1149-r1153, r1301"),

    tc("Marker & modal chi tiết action", "UI-001", "Normal",
       "Modal chi tiết action — 4 thông tin: tên tính năng, tên quản lý, chi tiết action, thời điểm kích hoạt",
       BOT + "\n- Có tin gửi bằng action từ cài đặt kết bạn",
       "1. Bấm nút xem chi tiết trên tin gửi bằng action\n2. Quan sát modal: bố cục, 4 mục thông tin\n"
       "3. Bấm nút X đóng, mở lại bấm nút 閉じる",
       "Action từ cài đặt kết bạn (kết bạn mới)",
       "- Modal hiện đủ 4 mục: tên tính năng「友だち追加時設定」/ tên quản lý (dấu - nếu không có) / "
       "chi tiết action「新規友だち用アクション」/ thời điểm kích hoạt định dạng 2026年01月22日（木） 16:19\n"
       "- Nút X và nút 閉じる đều đóng modal",
       note="Nguồn: Content: Hiển thị msg r1154-r1156, r1304, r1305"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn Cài đặt kết bạn (3 loại) hiển thị đúng chi tiết",
       BOT + "\n- Đã cấu hình action riêng cho kết bạn mới, kết bạn cũ và bỏ block",
       "1. Với mỗi loại ở cột Dữ liệu test: kích hoạt để sinh tin action\n"
       "2. Bấm xem chi tiết, đọc 4 mục thông tin\n"
       "3. Thử với: chỉ có action text riêng / chỉ có action trong multi action / có cả hai",
       "Kết bạn mới · kết bạn cũ · bỏ block — mỗi loại × 3 cách cấu hình action",
       "- Tên tính năng luôn là「友だち追加時設定」, tên quản lý hiện dấu -\n"
       "- Chi tiết action: kết bạn mới =「新規友だち用アクション」; kết bạn cũ =「既存友だち用アクション」; "
       "bỏ block =「ブロック解除友だち用アクション」\n- Thời điểm kích hoạt hiển thị đúng",
       note="Gộp 9 tổ hợp vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r1156-r1164"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn Template (URL, nút bấm, ảnh, video)",
       BOT + "\n- Template T có action ở: URL chuyển hướng, nút bấm các loại, image map, video",
       "1. Cho friend A kích hoạt lần lượt từng loại action ở cột Dữ liệu test\n"
       "2. Bấm xem chi tiết trên tin action tương ứng, đọc 4 mục thông tin",
       "URL chuyển hướng (còn hạn và hết hạn) · nút bấm standard / màu / ảnh / quick text / quick ảnh "
       "(chỉ multi action, có cả action phía bạn bè, action khi vượt số lần bấm) · image map · video",
       "- Tên tính năng luôn là「テンプレート」\n"
       "- Tên quản lý hiện tên template CHA\n"
       "- Chi tiết action: URL =「URLタップ」; nút bấm =「パネルボタンタップ」; image map =「画像タップ」; video =「動画視聴」\n"
       "- Thời điểm kích hoạt hiển thị đúng",
       note="Gộp vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r1165-r1182"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn QR landing, Form, Tự động trả lời, Rich menu, Conversion, Friend info",
       BOT + "\n- Đã cấu hình action cho từng nguồn ở cột Dữ liệu test",
       "1. Với mỗi nguồn: kích hoạt để sinh tin action cho friend A\n"
       "2. Bấm xem chi tiết, đọc tên tính năng, tên quản lý và chi tiết action",
       "QR landing: action kết bạn mới / kết bạn cũ / giới thiệu\n"
       "Form: khi mở form / khi hoàn thành trả lời\n"
       "Tự động trả lời: mọi tin nhắn / theo từ khoá\n"
       "Rich menu: khi chạm\nConversion: khi hiển thị trang\n"
       "Friend info: khi đăng ký thông tin (kiểu lựa chọn / điểm / ngày)",
       "- QR landing: 「QRコードアクション」+ tên landing + 「URL読み込み」hoặc「紹介時アクション」\n"
       "- Form: 「フォーム作成」+ tên form + 「表示時アクション」hoặc「回答完了時アクション」\n"
       "- Tự động trả lời: 「自動応答」+ dấu - + 「全てのメッセージ」hoặc「キーワード」\n"
       "- Rich menu: 「リッチメニュー」+ tên rich menu + 「タップ」\n"
       "- Conversion: 「コンバージョン」+ tên conversion + 「ページ表示時アクション」\n"
       "- Friend info: 「友だち情報管理」+ tên thông tin + 「情報登録時アクション」",
       note="Gộp vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r1183-r1191, r1238, r1239"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn Tag (gắn tag từ nhiều nơi)",
       BOT + "\n- Tag T1 có action gửi tin; tag T2 có action khi đạt giới hạn",
       "1. Gắn tag T1 cho friend A từ từng nơi ở cột Dữ liệu test\n"
       "2. Với mỗi lần: bấm xem chi tiết tin action, đọc 3 mục thông tin\n"
       "3. Lặp lại với tag T2 (action khi đạt giới hạn)",
       "Gắn tag từ: modal multi action ở chat 1:1 · quick action ở danh sách trái · tab タグ管理 ở cột phải · "
       "my_page · màn friend list · nhập từ file CSV · khi bấm nút · app mobile (chat 1:1 và my_page)",
       "- Tên tính năng luôn là「タグ管理」, tên quản lý là tên tag\n"
       "- Chi tiết action: gắn tag thường =「タグ追加時アクション」\n"
       "- Action khi đạt giới hạn: theo thiết kế là「制限到達後のタグ追加時アクション」— ghi nhận text thực tế "
       "(hiện đang hiển thị「タグ追加時アクション」)",
       spec="Đã hỏi leader",
       note="Corpus ghi rõ text hiện tại chưa khớp thiết kế. Nguồn: Content: Hiển thị msg r1227-r1237"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn đặt lịch (calendar, event, salon, lesson)",
       BOT + "\n- Đã cấu hình action cho đủ các mốc đặt lịch của 4 tính năng",
       "1. Với mỗi tính năng và mỗi mốc ở cột Dữ liệu test: thực hiện thao tác để sinh tin action\n"
       "2. Bấm xem chi tiết, đọc tên tính năng, tên quản lý và chi tiết action",
       "Calendar booking (12 mốc: đặt / yêu cầu đặt / duyệt / từ chối / đổi lịch / yêu cầu đổi / duyệt đổi / "
       "từ chối đổi / huỷ / yêu cầu huỷ / duyệt huỷ / từ chối huỷ)\n"
       "Event booking (12 mốc tương tự + admin đặt hộ) · Salon (9 mốc) · Lesson (9 mốc + hết chỗ và có chỗ trống)",
       "- Tên tính năng: 「カレンダー予約」/「イベント予約」/「サロン・面談予約」/「レッスン予約」\n"
       "- Tên quản lý: tên bản ghi tương ứng\n"
       "- Chi tiết action khớp đúng mốc thao tác (予約受付時 / 予約リクエスト受付時 / 予約リクエスト承認時 / "
       "予約リクエスト否認時 / 予約変更時 / 変更リクエスト受付時 / 変更リクエスト承認時 / 変更リクエスト否認時 / "
       "予約キャンセル時 / キャンセルリクエスト受付時 / キャンセルリクエスト承認時 / キャンセルリクエスト否認時)",
       env="PRODUCTION",
       note="Gộp ~42 mốc vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r1240-r1284, r1440-r1496"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn bán hàng (item 1 lần và item chu kỳ)",
       BOT + "\n- Đã cấu hình action cho các mốc của item bán 1 lần và item chu kỳ",
       "1. Với mỗi mốc ở cột Dữ liệu test: thực hiện để sinh tin action\n"
       "2. Bấm xem chi tiết, đọc 3 mục thông tin",
       "Item 1 lần: mở trang · hoàn tất đăng ký · huỷ\n"
       "Item chu kỳ: mở trang · hoàn tất đăng ký · kết thúc dùng thử · thanh toán lần đầu · "
       "thanh toán từ lần 2 · thanh toán lỗi · huỷ",
       "- Tên tính năng: 「単品商品販売」hoặc「継続商品販売」, tên quản lý là tên item\n"
       "- Chi tiết action khớp đúng mốc (商品ページ表示時 / 申し込み完了時 / トライアル終了時 / 初回決済時 / "
       "2回目以降決済時 / 決済エラー発生時 / 解約時アクション)",
       env="PRODUCTION",
       note="Gộp 10 mốc vì cùng dạng. Nguồn: Content: Hiển thị msg r1285-r1294"),

    tc("Marker & modal chi tiết action", "UI-FIELD-001", "Normal",
       "Modal chi tiết action — nguồn thao tác thủ công và lịch chạy action",
       BOT + "\n- Có account user chính và account staff",
       "1. Ở chat 1:1: user chính thực hiện multi action → xem chi tiết\n"
       "2. Ở chat 1:1: staff thực hiện multi action → xem chi tiết\n"
       "3. Ở màn friend list: user chính và staff thực hiện action → xem chi tiết\n"
       "4. Tạo lịch chạy action, chờ chạy → xem chi tiết",
       "Thao tác thủ công ở chat 1:1 và friend list (user chính và staff) · lịch chạy action",
       "- Thao tác thủ công: tên tính năng「手動操作」, tên quản lý dấu -, chi tiết là TÊN NGƯỜI thao tác\n"
       "- Lịch chạy action: tên tính năng「アクションスケジュール実行」, tên quản lý là tên lịch, chi tiết dấu -",
       note="Nguồn: Content: Hiển thị msg r1295-r1297, r533-r536, r612, r613"),

    tc("Marker & modal chi tiết action", "MSG-003", "Abnormal",
       "Tin gửi từ Scenario và Broadcast — KHÔNG có nguồn action gửi tin",
       BOT + "\n- Có scenario S và broadcast B đã gửi cho friend A",
       "1. Xem tin do step của scenario gửi → tìm nút xem chi tiết action\n"
       "2. Xem tin do broadcast gửi → tìm nút xem chi tiết action\n"
       "3. So sánh với tin gửi bằng action từ nguồn khác",
       "Tin từ step scenario · tin từ broadcast",
       "- Cả 2 loại tin: KHÔNG có nút xem chi tiết action gửi tin\n"
       "- Chỉ tin bắt đầu / dừng scenario mới có nút xem chi tiết",
       note="Nguồn: Content: Hiển thị msg r397, r1299, r1300"),

    tc("Marker & modal chi tiết action", "DATA-REF-001", "Abnormal",
       "Action đã bị xoá — modal chi tiết hiện thông báo kèm người xoá và thời điểm xoá",
       BOT + "\n- Có tin gửi bằng action; account user chính và account staff đều có quyền xoá action",
       "1. Sau khi action gửi tin cho friend, dùng user CHÍNH xoá/sửa action đó\n"
       "2. Bấm xem chi tiết trên tin action ở chat 1:1 → đọc modal\n"
       "3. Lặp lại nhưng dùng account STAFF xoá action",
       "Action bị xoá bởi user chính và bởi staff",
       "- Modal hiện thêm text「メッセージの送信アクションはすでに変更・削除済みです。」\n"
       "- Hiện ngày giờ xoá định dạng 2024年10月03日（日） 15:01 và TÊN người đã xoá\n"
       "- Đúng cho cả 2 trường hợp user chính và staff",
       note="Nguồn: Content: Hiển thị msg r1302, r1303"),

    # ═══════════════ Marker step, remind, broadcast, send test ═══════════════
    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin bắt đầu scenario — nội dung khác nhau giữa bắt đầu từ đầu và bắt đầu từ giữa",
       BOT + "\n- Có scenario S nhiều bước",
       "1. Bắt đầu scenario S cho friend A TỪ ĐẦU → quan sát tin ở chat 1:1\n"
       "2. Dừng, rồi bắt đầu lại TỪ NGÀY THỨ 3 → quan sát tin\n"
       "3. Đọc ngày giờ, tên scenario và nội dung của từng tin",
       "Scenario S: bắt đầu từ đầu và bắt đầu từ ngày thứ 3",
       "- Bắt đầu từ đầu: hiện 「ステップ配信開始」+ tên scenario + ngày giờ định dạng 2024/09/30 13:45\n"
       "- Bắt đầu từ giữa: hiện「（途中からの）ステップ配信開始」+ tên scenario + số ngày bắt đầu",
       note="2 nội dung khác nhau nhưng cùng 1 chuỗi kiểm chứng. "
            "Nguồn: Content: Hiển thị msg r222-r224, r1199"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Modal nguồn bắt đầu / dừng scenario — hiển thị đúng nguồn kích hoạt",
       BOT + "\n- Có scenario S; đã cấu hình đủ nguồn kích hoạt ở cột Dữ liệu test",
       "1. Với mỗi nguồn: kích hoạt bắt đầu scenario S cho friend A\n"
       "2. Bấm vào tên scenario ở tin → đọc modal nguồn kích hoạt\n"
       "3. Lặp lại với các nguồn dừng scenario",
       "Bắt đầu: multi action ở chat 1:1 · cột phải chat 1:1 · my_page · màn friend list · tự động trả lời · "
       "bấm nút · kết bạn mới / kết bạn cũ · quét QR · chạm rich menu · gắn tag · chạm image map\n"
       "Dừng: multi action ở chat 1:1 · cột phải · my_page · chạm rich menu · tự động trả lời · trả lời form",
       "- Modal hiện tiêu đề「このステップの開始トリガー」hoặc「このステップの停止トリガー」\n"
       "- Hiện tên tính năng nguồn (「手動操作」/「友だち追加時設定」/「リッチメニュー」…), tên quản lý và chi tiết\n"
       "- Với thao tác thủ công: chi tiết hiện TÊN NGƯỜI đã thao tác\n"
       "- Hiện thời điểm kích hoạt định dạng 2026年01月22日（木） 16:19",
       note="Gộp ~17 nguồn vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r1192-r1211, r226-r304, r306-r310"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Abnormal",
       "Bắt đầu scenario nhưng không còn bước nào thoả điều kiện — hiện thông báo tương ứng",
       BOT + "\n- Scenario S chỉ có bước ở ngày thứ 2; friend A bắt đầu từ ngày thứ 3\n"
       "- Scenario S2 chưa đăng ký tin nhắn nào",
       "1. Bắt đầu S cho A từ ngày thứ 3 (từ web) → quan sát tin ở chat 1:1\n"
       "2. Lặp lại trường hợp bắt đầu qua job\n3. Bắt đầu S2 (chưa có tin nhắn) → quan sát",
       "S không còn bước thoả điều kiện · S2 chưa có tin nhắn",
       "- S: hiện tin dừng scenario kèm「既に購読したステップのため終了しました。」\n"
       "- S2: hiện tin bắt đầu kèm「※ このステップ配信にはメッセージは登録されていません」\n"
       "- Đúng cho cả bắt đầu từ web và từ job",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r311, r1212, r1213"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin do step scenario gửi — dấu hiệu ステップ配信 kèm tên scenario, điều kiện lọc và mốc thời gian",
       BOT + "\n- Scenario S có bước gửi ngay, bước sau X giờ, bước theo ngày giờ chỉ định; có bước có lọc và không lọc",
       "1. Chờ từng bước gửi cho friend A\n"
       "2. Với mỗi tin: đọc dấu hiệu, profile, tên scenario, điều kiện lọc, mốc thời gian, nội dung đầu tiên\n"
       "3. Bấm nút xem trước nội dung",
       "Bước gửi ngay · bước sau 5 phút · bước sau 1 ngày lúc 01:00 · bước có lọc và không lọc",
       "- Có dấu hiệu「ステップ配信」+ profile (mặc định hoặc profile đã cấu hình)\n"
       "- Hiện tên scenario; điều kiện lọc hiện「ステップ購読者全員」nếu không lọc, hoặc tên bộ lọc\n"
       "- Mốc thời gian: 「ステップ開始直後」/「00時間05分後」/「1日後01:00」\n"
       "- Nội dung: tin text hiện nội dung; loại khác hiện nhãn loại tin\n"
       "- Có nút xem trước, KHÔNG có nút xem chi tiết nguồn",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r386-r398"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Normal",
       "Nội dung đầu tiên hiển thị theo loại tin — nhãn loại tin cho tin không phải text",
       BOT + "\n- Có scenario / broadcast với bước đầu là từng loại tin ở cột Dữ liệu test",
       "1. Với mỗi loại: cho gửi cho friend A\n2. Đọc dòng nội dung tóm tắt trong khung dấu hiệu",
       "text (ngắn và dài) · button · ảnh · image map · video · audio · sticker · vị trí",
       "- Text: hiện nội dung, dài thì cắt kèm dấu ba chấm\n"
       "- Button: 【カルーセル】· ảnh và image map: 【画像】· video: 【動画】· audio: 【音声】· "
       "sticker: 【スタンプ】· vị trí: 【位置】",
       note="Gộp vì cùng quy tắc. Nguồn: Content: Hiển thị msg r193-r200, r399-r406, r619-r634"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Abnormal",
       "Bước scenario KHÔNG gửi được do ngoài điều kiện lọc — vẫn hiển thị kèm ghi chú",
       BOT + "\n- Scenario S có bước với bộ lọc mà friend A KHÔNG thoả",
       "1. Chờ tới thời điểm gửi của bước đó\n2. Quan sát chat 1:1 của friend A\n"
       "3. Lặp lại với từng loại tin ở cột Dữ liệu test",
       "text · button (standard/màu/ảnh/quick text/quick ảnh) · ảnh · image map · audio · video · sticker · vị trí",
       "- Tin VẪN hiển thị ở chat 1:1\n"
       "- Có thêm ghi chú「このメッセージは配信（絞り込み） 対象外のため送信されていません。」\n"
       "- Friend KHÔNG nhận tin trên app LINE",
       env="PRODUCTION",
       note="Gộp 11 loại vì cùng kết quả. Nguồn: Content: Hiển thị msg r424-r435"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Abnormal",
       "Bước scenario chỉ có action, không có tin nhắn — không hiển thị ở chat 1:1",
       BOT + "\n- Scenario S có 1 bước chỉ cấu hình multi action, không có tin nhắn",
       "1. Chờ bước đó chạy cho friend A\n2. Quan sát chat 1:1\n"
       "3. Kiểm tra action có thực sự chạy không (ví dụ tag được gắn)",
       "Bước chỉ có action, không có tin nhắn",
       "- Action ĐƯỢC thực hiện (kiểm chứng qua kết quả action)\n"
       "- KHÔNG hiển thị tin nào ở chat 1:1",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r437"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin bắt đầu / dừng remind và tin do remind gửi — dấu hiệu リマインド配信",
       BOT + "\n- Có remind R gắn với event booking",
       "1. Kích hoạt bắt đầu remind R cho friend A → quan sát tin\n"
       "2. Chờ bước remind gửi → quan sát dấu hiệu, profile, thời gian, tên remind, mốc thời gian\n"
       "3. Dừng remind → quan sát tin\n4. Bấm vào tên remind → đọc modal nguồn kích hoạt",
       "Remind R: bắt đầu, gửi bước, dừng",
       "- Tin bắt đầu: hiện thời gian sự kiện + text「リマインド配信開始」+ tên remind (dạng liên kết)\n"
       "- Tin dừng: hiện thời điểm dừng + text「リマインド配信を停止」+ tên remind\n"
       "- Tin do remind gửi: dấu hiệu「リマインド配信」+ profile mặc định + tên remind + mốc thời gian "
       "(「リマインド開始直後」/「終了1日前 12:30」/「終了 00時間30分前」) + nội dung đầu tiên + nút xem trước\n"
       "- Modal nguồn kích hoạt hiện tên tính năng, tên quản lý, chi tiết và thời điểm",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r440-r462, r1216-r1226"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Abnormal",
       "Remind của salon / lesson / form — chưa có dấu hiệu remind trên chat 1:1",
       BOT + "\n- Có salon, lesson và form có cấu hình remind",
       "1. Kích hoạt remind của salon → chờ gửi → quan sát tin ở chat 1:1\n"
       "2. Lặp lại với lesson và với form\n3. Tìm nút xem chi tiết nguồn kích hoạt",
       "Remind của salon · lesson · form",
       "- Tin hiển thị như tin thường, KHÔNG có dấu hiệu remind\n"
       "- KHÔNG có nguồn kích hoạt hiển thị trên chat 1:1\n"
       "- Ghi rõ hiện trạng này làm evidence",
       env="PRODUCTION", spec="Spec không ghi",
       note="Corpus ghi rõ hiện trạng chưa hỗ trợ. Nguồn: Content: Hiển thị msg r455, r456, r1219-r1221"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin do Broadcast gửi — dấu hiệu 一斉配信 kèm tiêu đề quản lý, thời gian và nút xem trước",
       BOT + "\n- Có broadcast B với tiêu đề quản lý và nhiều tin nhắn",
       "1. Gửi B cho friend A (thử cả gửi ngay và gửi theo lịch, gửi 1 lần và nhiều lần)\n"
       "2. Quan sát tin ở chat 1:1: profile, dấu hiệu, thời gian đặt gửi, tiêu đề, nội dung đầu, thời gian gửi\n"
       "3. Bấm nút xem trước → quan sát modal",
       "Broadcast B: gửi ngay · gửi theo lịch 1 lần · gửi theo lịch nhiều lần",
       "- Profile: hiện profile mặc định hoặc profile đã cấu hình\n"
       "- Dấu hiệu「一斉配信」, thời gian đặt gửi định dạng 2024年09月30日（月） 13:45\n"
       "- Tiêu đề hiện tên quản lý của broadcast; nội dung đầu tiên cắt bớt nếu dài\n"
       "- Thời gian gửi định dạng MM/DD HH:mm\n- Nút xem trước mở modal xem nội dung tin",
       env="PRODUCTION",
       note="Nguồn: Content: Hiển thị msg r185-r203"),

    tc("Marker step, remind, broadcast, send test", "OUT-PREVIEW-001", "Normal",
       "Modal xem trước nội dung tin — đủ loại tin và tab action",
       BOT + "\n- Có broadcast / step scenario chứa đủ loại tin ở cột Dữ liệu test, có cấu hình action",
       "1. Bấm nút xem trước trên tin có dấu hiệu\n2. Ở tab nội dung: kiểm tra từng loại tin\n"
       "3. Chuyển sang tab action: kiểm tra khi không có action và khi có action",
       "Loại tin: text · button (standard/màu/ảnh/quick text/quick ảnh) · ảnh · image map · video · audio · "
       "sticker · vị trí\nAction: không có action · có action (thứ tự, dữ liệu, có/không bộ lọc)",
       "- Tab nội dung hiển thị đúng và đủ từng loại tin\n"
       "- Tab action: không có action thì hiện trạng thái rỗng; có action thì hiện đúng thứ tự, dữ liệu và bộ lọc",
       note="Gộp vì cùng kết quả. Nguồn: Content: Hiển thị msg r204-r219, r407-r423"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin Send test — dấu hiệu テスト送信 với đủ thông tin, mỗi template con 1 dấu hiệu riêng",
       BOT + "\n- Có group template T nhiều template con đủ loại; friend A là tài khoản test",
       "1. Gửi test T từ màn Template (cả quick test và modal xem trước)\n"
       "2. Quan sát ở chat 1:1: profile, dấu hiệu, nội dung, thời gian, người thao tác\n"
       "3. Lặp lại từ Broadcast, từ Scenario (từng bước và toàn bộ), từ Remind\n"
       "4. Với group template nhiều con: đếm số dấu hiệu",
       "Send test từ: Template (quick test, modal, gửi cả nhóm, gửi 1 template con) · "
       "Broadcast (màn tạo, màn danh sách) · Scenario (quick test, gửi 1 bước, gửi 1 template trong bước, "
       "gửi cả scenario qua job 3 kiểu) · Remind (gửi toàn bộ mốc)",
       "- Mọi đường: hiện dấu hiệu「テスト送信」+ profile (tên và ảnh) + nội dung + thời gian định dạng "
       "MM/DD HH:mm + tên người thao tác\n"
       "- Group template nhiều con: MỖI template con hiển thị 1 dấu hiệu riêng\n"
       "- Friend nhận đủ tin trên app LINE",
       env="PRODUCTION",
       note="Gộp ~17 đường vì cùng kết quả. Nguồn: Content: Send message r1184-r1200 + Content: Hiển thị msg r666-r704"),

    tc("Marker step, remind, broadcast, send test", "OUT-PREVIEW-001", "Normal",
       "Send test từ Broadcast / Scenario / Remind — nội dung đầu tiên và xem trước hiển thị đúng thứ tự",
       BOT + "\n- Broadcast B, scenario S, remind R đều chứa đủ loại template con",
       "1. Gửi test B → quan sát: thời gian đặt gửi, tiêu đề quản lý, nội dung đầu tiên\n"
       "2. Bấm xem trước → kiểm tra đủ template con, đúng thứ tự\n"
       "3. Lặp lại với S (kiểm tra thêm tên scenario, tên bộ lọc, mốc thời gian) và R (tên remind, mốc thời gian)\n"
       "4. Với S gửi qua job: kiểm tra thứ tự các bước và bước không thoả bộ lọc",
       "B, S, R với template con đủ loại: text (có/không rút gọn URL) · button các loại · ảnh · image map · "
       "video (có/không thumbnail) · audio · sticker · vị trí",
       "- Nội dung đầu tiên hiển thị theo đúng quy tắc nhãn loại tin\n"
       "- Xem trước hiển thị ĐỦ template con theo ĐÚNG thứ tự, giống thiết kế khi gửi thật\n"
       "- Scenario gửi qua job: các bước hiển thị đúng thứ tự; bước không thoả bộ lọc vẫn hiển thị theo thiết kế "
       "nhưng KHÔNG thay giá trị chèn (vì thực tế không gửi)",
       env="PRODUCTION",
       note="Gộp vì cùng dạng kết quả. Nguồn: Content: Hiển thị msg r705-r860"),

    tc("Marker step, remind, broadcast, send test", "UI-FIELD-001", "Normal",
       "Tin gửi khi đặt lịch booking — dấu hiệu 予約送信 với profile, nội dung và thời gian",
       BOT + "\n- Có salon và lesson đã cấu hình action gửi tin khi đặt lịch",
       "1. Cho friend A đặt lịch salon → quan sát tin ở chat 1:1\n"
       "2. Đọc profile, dấu hiệu, nội dung, thời gian gửi\n3. Lặp lại với lesson",
       "Đặt lịch salon và lesson có cấu hình action gửi tin",
       "- Tin hiện dấu hiệu「予約送信」+ profile + nội dung trong khung + thời gian gửi",
       env="PRODUCTION",
       note="Support #29869 (05/2025) yêu cầu đổi các tin remind/booking sang dạng có nút xem chi tiết "
            "giống tin gửi bằng action — cần kiểm chứng hiện trạng. Nguồn: Content: Hiển thị msg r866-r871"),

    tc("Marker step, remind, broadcast, send test", "MSG-003", "Normal",
       "Đặt lịch booking — chỉ gửi tin khi có bật cấu hình action",
       BOT + "\n- Lesson L1 CÓ bật cấu hình action gửi tin; lesson L2 KHÔNG bật",
       "1. Với L1: cho friend đặt lịch, admin đặt hộ, yêu cầu đặt, huỷ, yêu cầu huỷ → kiểm tra tin ở chat 1:1\n"
       "2. Với L2: lặp lại toàn bộ thao tác → kiểm tra tin\n"
       "3. Lặp lại với cấu hình action riêng theo khoá học và theo nhân viên",
       "L1 bật action · L2 không bật; thao tác bởi friend và bởi admin; cấu hình chung / theo khoá / theo nhân viên",
       "- L1: gửi tin tương ứng theo từng mốc, hiển thị đúng ở chat 1:1 và app LINE\n"
       "- L2: KHÔNG gửi tin nào\n"
       "- Cấu hình theo khoá / theo nhân viên: gửi đúng tin của cấu hình đó",
       env="PRODUCTION",
       note="Gộp vì cùng dạng. Nguồn: Content: Hiển thị msg r872-r907"),
]
