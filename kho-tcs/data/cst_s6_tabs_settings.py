# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 10-14: Tab 3 → Tab 7.

S10 Tự động xác nhận tin nhắn (SCR-04「メッセージの自動確認済み変更」)
S11 Phím tắt gửi (SCR-05「送信ショートカット」)
S12 URL rút gọn (SCR-06「短縮URLの利用」)
S13 Xem trước khi gửi (SCR-07「送信プレビュー」)
S14 Hiển thị đã đọc — FAQ (SCR-08A「既読情報の表示」)

✅ MT-01 đã chốt 2026-09-21: màn có 8 tab ⇒ đánh số tab theo bản 8 tab —
tab 3 = auto-confirm, tab 4 = shortcut, tab 5 = shorten URL, tab 6 = preview,
tab 7 = FAQ. Spec hiện còn đánh số lùi 1 (auto-confirm là『Tab 2』) và PHẢI ĐƯỢC
SỬA theo việc (4) của MT-01.

⚠️ MT-03: danh sách checkbox của Tab 3 KHÔNG khớp giữa spec và corpus 2026.
File này viết theo corpus 2026 (có checkbox「メディア」) và ghi rõ ở từng TC.
"""
from _common import tc

ADMIN = "- Đăng nhập Admin của LOA, đã chọn 1 bot"
T3 = ADMIN + "\n- Đang ở `/basic/chat-setting` Tab 3「メッセージの自動確認済み変更」"
T4 = ADMIN + "\n- Đang ở Tab 4「送信ショートカット」"
T5 = ADMIN + "\n- Đang ở Tab 5「短縮URLの利用」"
T6 = ADMIN + "\n- Đang ở Tab 6「送信プレビュー」"
T7 = ADMIN + "\n- Đang ở Tab 7「既読情報の表示」"
FRIEND = "- Có tài khoản LINE test đã kết bạn với LOA đang dùng"
MT03 = "⚠️ Phụ thuộc MT-03 (danh sách checkbox Tab 3 lệch giữa spec và corpus 2026). "

S10 = [
    tc("Tự động xác nhận tin nhắn", "UI-003", "Normal",
       "Trạng thái mặc định của Tab 3 — 4 checkbox + 2 toggle",
       T3 + "\n- Bot chưa từng đổi cấu hình Tab 3",
       "1. Quan sát toàn bộ form Tab 3",
       "—",
       "- Checkbox「【○○】メッセージ」(`confirm_message_button`): ĐÃ tích (ON)\n"
       "- Checkbox「スタンプ」(`confirm_message_stamp`): chưa tích (OFF)\n"
       "- Checkbox「メディア」: chưa tích (OFF)\n"
       "- Checkbox「自動応答キーワード」: chưa tích (OFF)\n"
       "- Toggle「返信時の自動確認済み変更」: OFF\n"
       "- Toggle「ブロックされた友だちの自動確認済み変更」: OFF",
       spec="Đã hỏi leader",
       note=MT03 + "⚠️ MT-04 — DỰ KIẾN FAIL: v2 r113 (TC-SC-034) **Fail cả staging lẫn production**. "
            "3 nguồn nói 3 kiểu: v2 nói【○○】メッセージ default ON; SC r7/r16/r24/r32/r48 (2025) + "
            "spec DB nói TẤT CẢ = 0 (OFF); v1 r111 (BS_036) nói toggle ブロック default =「利用する」(ON). "
            "CẦN LEADER CHỐT trước khi chạy"),

    tc("Tự động xác nhận tin nhắn", "FUNC-001", "Normal",
       "Đổi 1 checkbox → nút「保存」bật lên → lưu thành công",
       T3 + "\n- Nút「保存」đang mờ (disabled)",
       "1. Quan sát nút「保存」— xác nhận đang mờ, không bấm được\n"
       "2. Tích checkbox「スタンプ」\n"
       "3. Quan sát lại nút「保存」\n"
       "4. Bấm「保存」",
       "—",
       "- Bước 1: nút「保存」mờ, không bấm được\n"
       "- Bước 3: nút「保存」chuyển sang bấm được\n"
       "- Bước 4: toast「保存しました」xuất hiện",
       note="BR-04-03: nút bật khi form có thay đổi (QA-017). Nguồn: v2 r111 (TC-SC-032, Pass "
            "staging + production)"),

    tc("Tự động xác nhận tin nhắn", "FUNC-001", "Abnormal",
       "Chưa đổi gì — nút「保存」vẫn mờ, không bấm được",
       T3 + "\n- Vừa tải trang hoặc vừa lưu thành công",
       "1. Không đổi bất kỳ checkbox hay toggle nào\n"
       "2. Quan sát và thử bấm nút「保存」",
       "—",
       "- Nút「保存」ở trạng thái mờ (disabled)\n"
       "- Bấm không có phản hồi, không gửi request lưu",
       note="Nguồn: v2 r112 (TC-SC-033, Pass staging + production)"),

    tc("Tự động xác nhận tin nhắn", "FUNC-SEQ-001", "Normal",
       "Lưu cấu hình rồi F5 — trạng thái checkbox/toggle giữ nguyên",
       T3 + "\n- Đang ở trạng thái mặc định",
       "1. Tích checkbox「スタンプ」\n"
       "2. Bật toggle「返信時の自動確認済み変更」\n"
       "3. Bấm「保存」, chờ toast「保存しました」\n"
       "4. Nhấn F5 rồi quay lại Tab 3",
       "—",
       "- Sau bước 3: toast「保存しました」xuất hiện\n"
       "- Sau F5: checkbox「スタンプ」vẫn tích, toggle「返信時の自動確認済み変更」vẫn ON\n"
       "- Khớp y hệt trạng thái ngay trước khi reload",
       note="Nguồn: v2 r114 (TC-SC-089, Not Tested)"),

    tc("Tự động xác nhận tin nhắn", "FUNC-SEQ-001", "Normal",
       "Đổi checkbox nhưng KHÔNG bấm「保存」rồi F5 — quay về giá trị đã lưu",
       T3,
       "1. Tích / bỏ tích 1 checkbox (vd「スタンプ」) hoặc bật 1 toggle\n"
       "2. KHÔNG bấm「保存」\n"
       "3. Nhấn F5\n"
       "4. Quan sát lại các checkbox / toggle",
       "—",
       "- Sau reload: checkbox / toggle trở về giá trị đã lưu trước đó\n"
       "- Thay đổi chưa lưu bị bỏ hoàn toàn, không lưu nhầm",
       note="Nguồn: v2 r117 (TC-SC-135, Pass staging + production) · SC r14 · r22 · r30 · r44 · r54"),

    tc("Tự động xác nhận tin nhắn", "UI-004", "Normal",
       "Tooltip (?) cạnh「【○○】メッセージ」— có nội dung và nút「詳細記事を見る」",
       T3,
       "1. Hover (hoặc bấm) icon (?) cạnh checkbox「【○○】メッセージ」\n"
       "2. Quan sát tooltip / popover\n"
       "3. Bấm「詳細記事を見る」",
       "—",
       "- Hiển thị tooltip / popover có nội dung giải thích\n"
       "- Có nút「詳細記事を見る」\n"
       "- Bấm nút mở bài hướng dẫn tương ứng",
       note="Nguồn: v2 r116 (TC-SC-134, Blocked / Not Tested). Chuỗi「詳細記事を見る」đã confirm ở "
            "screens/SCR-04-auto-read-message.md"),

    tc("Tự động xác nhận tin nhắn", "DATA-DB-001", "Normal",
       "Tích「【○○】メッセージ」rồi lưu — ghi đúng cờ vào bot đang chọn, bot khác không đổi",
       T3 + "\n- Tài khoản quản lý ≥ 2 bot; ghi lại cấu hình Tab 3 của bot B trước khi thao tác",
       "1. Ở bot A, tích checkbox「【○○】メッセージ」→ bấm「保存」\n"
       "2. Kiểm tra `bots.confirm_message_button` của bot A\n"
       "3. Mở phiên đăng nhập riêng cho bot B, vào Tab 3 và đối chiếu với cấu hình đã ghi",
       "—",
       "- `bots.confirm_message_button` của bot A = 1\n"
       "- Cấu hình Tab 3 của bot B KHÔNG thay đổi so với lúc ghi nhận ban đầu",
       note="Nguồn: SC r9 · SC r15 (OK). ⚠️ Đổi bot ở 1 tab là đổi cho cả trình duyệt → phải dùng "
            "2 phiên đăng nhập riêng"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật「【○○】メッセージ」— tin dạng【…】từ friend KHÔNG làm tăng số chưa xác nhận",
       T3 + "\n- Checkbox「【○○】メッセージ」đã bật ON và đã lưu\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại với friend test\n"
       "2. Từ tài khoản LINE test, gửi tin「【テスト】」(bắt đầu bằng【 và kết thúc bằng】) tới LOA\n"
       "3. Mở màn chat 1:1 (FA-001), tìm hội thoại vừa nhận tin\n"
       "4. Quan sát trạng thái chưa xác nhận của hội thoại",
       "【テスト】",
       "- Tin「【テスト】」vào đúng hội thoại\n"
       "- Hội thoại KHÔNG bị tính là có tin chưa xác nhận vì tin này\n"
       "- Số chưa xác nhận trên hội thoại KHÔNG tăng so với bước 1",
       note=MT03 + "BR-04-01: Spring Boot `HandlePostbackTask` bỏ qua INSERT `unconfirm_message` khi "
            "tin khớp `^【.*】$` và cờ = 1. Nguồn: v2 r115 (TC-SC-090, Not Tested) · SC r10 · "
            "v1 r102 (BS_029, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật「スタンプ」— sticker từ friend KHÔNG làm tăng số chưa xác nhận",
       T3 + "\n- Checkbox「スタンプ」đã bật ON và đã lưu\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi 1 sticker tới LOA\n"
       "3. Mở màn chat 1:1, quan sát hội thoại",
       "1 sticker bất kỳ",
       "- Sticker vào đúng hội thoại\n"
       "- Số chưa xác nhận KHÔNG tăng so với bước 1",
       note=MT03 + "`bots.confirm_message_stamp`. Nguồn: SC r19 (OK + staging OK) · v1 r103 (BS_030, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "TẮT「スタンプ」— sticker từ friend LÀM TĂNG số chưa xác nhận",
       T3 + "\n- Checkbox「スタンプ」đã TẮT và đã lưu\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi 1 sticker tới LOA\n"
       "3. Mở màn chat 1:1, quan sát hội thoại",
       "1 sticker bất kỳ",
       "- Số chưa xác nhận TĂNG thêm 1 so với bước 1\n"
       "- Hội thoại hiển thị trạng thái có tin chưa xác nhận",
       note=MT03 + "Đối xứng với TC bật「スタンプ」— giữ riêng vì kết quả mong đợi ngược nhau. "
            "Nguồn: SC r20-r21 (OK + staging OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật「メディア」— tin ảnh/video/audio/file từ friend KHÔNG làm tăng số chưa xác nhận",
       T3 + "\n- Checkbox「メディア」đã bật ON và đã lưu\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test lần lượt gửi: 1 ảnh, 1 video, 1 audio, 1 file khác\n"
       "3. Mở màn chat 1:1, quan sát hội thoại",
       "1 ảnh + 1 video + 1 audio + 1 file",
       "- Cả 4 tin đều vào đúng hội thoại\n"
       "- Số chưa xác nhận KHÔNG tăng với bất kỳ tin nào trong 4 loại",
       spec="Đã hỏi leader",
       note=MT03 + "⚠️ Checkbox「メディア」và cột `bots.auto_confirm_message_media` CHỈ có ở corpus "
            "2026 (v1 r104 / BS_031, OK), KHÔNG có trong spec (spec chỉ có 4 cờ button/stamp/"
            "autoreply_all/autoreply_specified). Gộp 4 loại media vì cùng 1 kết quả mong đợi"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật「自動応答[すべてのメッセージに反応]」— tin khớp auto-reply toàn bộ không tăng số chưa xác nhận",
       T3 + "\n- Checkbox tương ứng đã bật ON và đã lưu\n"
       "- FA-003 đang có 1 auto-reply kiểu「すべてのメッセージに反応」đang bật\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi 1 tin text bất kỳ tới LOA\n"
       "3. Xác nhận bot đã trả lời tự động\n"
       "4. Mở màn chat 1:1, quan sát hội thoại",
       "Tin text bất kỳ",
       "- Bot trả lời tự động\n"
       "- `bots.confirm_message_autoreply_all` = 1\n"
       "- Số chưa xác nhận KHÔNG tăng so với bước 1",
       note=MT03 + "BR-12: nếu 1 tin khớp cả KEYWORD_ANY lẫn keyword cụ thể thì chỉ áp cờ _all. "
            "Nguồn: v1 r105 (BS_032, OK) · SC r27"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "TẮT「自動応答[すべてのメッセージに反応]」— tin khớp auto-reply toàn bộ VẪN tăng số chưa xác nhận",
       T3 + "\n- Checkbox tương ứng đã TẮT và đã lưu\n"
       "- FA-003 đang có 1 auto-reply kiểu「すべてのメッセージに反応」đang bật\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi 1 tin text bất kỳ tới LOA\n"
       "3. Mở màn chat 1:1, quan sát hội thoại",
       "Tin text bất kỳ",
       "- `bots.confirm_message_autoreply_all` = 0\n"
       "- Số chưa xác nhận TĂNG thêm 1 so với bước 1",
       note=MT03 + "Nguồn: v1 r106 (BS_032 bản『bỏ tích』, OK) · SC r28-r29"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật「自動応答[設定したキーワードに反応]」— tin khớp từ khóa không tăng số chưa xác nhận",
       T3 + "\n- Checkbox tương ứng đã bật ON và đã lưu\n"
       "- FA-003 đang có 1 auto-reply theo từ khóa cụ thể「テスト」đang bật\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi đúng từ khóa「テスト」tới LOA\n"
       "3. Xác nhận bot trả lời tự động\n"
       "4. Mở màn chat 1:1, quan sát hội thoại",
       "テスト",
       "- Bot trả lời tự động theo từ khóa\n"
       "- `bots.confirm_message_autoreply_specified` = 1\n"
       "- Số chưa xác nhận KHÔNG tăng so với bước 1",
       note=MT03 + "Nguồn: v1 r107 (BS_032 bản『キーワード』, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "TẮT「自動応答[設定したキーワードに反応]」— tin khớp từ khóa VẪN tăng số chưa xác nhận",
       T3 + "\n- Checkbox tương ứng đã TẮT và đã lưu\n"
       "- FA-003 đang có 1 auto-reply theo từ khóa cụ thể「テスト」đang bật\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi đúng từ khóa「テスト」tới LOA\n"
       "3. Mở màn chat 1:1, quan sát hội thoại",
       "テスト",
       "- `bots.confirm_message_autoreply_specified` = 0\n"
       "- Số chưa xác nhận TĂNG thêm 1 so với bước 1",
       note=MT03 + "Nguồn: v1 r108 (BS_032 bản『bỏ tích キーワード』, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-COUNT-001", "Normal",
       "Bật cờ cho 1 loại tin — chỉ loại đó không tăng, loại khác vẫn tăng đúng 1",
       T3 + "\n- Chỉ bật checkbox cho ĐÚNG 1 loại tin (loại A), các loại còn lại tắt, đã lưu\n" + FRIEND,
       "1. Ghi lại số chưa xác nhận hiện tại của hội thoại\n"
       "2. Từ tài khoản LINE test gửi 1 tin loại A (loại đã bật cờ)\n"
       "3. Quan sát số chưa xác nhận\n"
       "4. Gửi tiếp 1 tin thuộc loại KHÁC (chưa bật cờ)\n"
       "5. Quan sát lại số chưa xác nhận",
       "1 tin loại A + 1 tin loại khác",
       "- Sau bước 3: số chưa xác nhận KHÔNG tăng (BR-04-01)\n"
       "- Sau bước 5: số chưa xác nhận tăng ĐÚNG 1, không tăng 2 (BR-04-02)\n"
       "- Kết quả giống nhau khi xem bằng tài khoản admin và tài khoản staff",
       note=MT03 + "TC đối chứng chéo — bảo vệ chống việc bật 1 cờ làm tắt nhầm cả loại khác. "
            "Nguồn: v2 r187 (TC-SC-187, Not Tested)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "Bật toggle「返信時の自動確認済み変更」— admin trả lời thì các tin chưa xác nhận được xác nhận",
       T3 + "\n- Toggle「返信時の自動確認済み変更」đã bật ON và đã lưu\n"
       "- Hội thoại X đang có ≥ 1 tin chưa xác nhận",
       "1. Ghi lại số chưa xác nhận của hội thoại X\n"
       "2. Mở màn chat 1:1, gửi 1 tin text trả lời cho hội thoại X\n"
       "3. Quan sát lại trạng thái chưa xác nhận của hội thoại X",
       "Tin text bất kỳ",
       "- Sau khi admin gửi tin, các tin chưa xác nhận của hội thoại X được đánh dấu đã xác nhận\n"
       "- Số chưa xác nhận của hội thoại X về 0",
       note="`bots.confirm_message_user_send` = 1. Nguồn: SC r33-r34 (OK + staging OK) · "
            "v1 r110 (BS_034, OK). ⚠️ BR-05 của spec cảnh báo cờ này thực chất được Laravel "
            "`ChatService` dùng để tính lại `count_user_unconfirm`, ngữ nghĩa có thể khác kỳ vọng UI"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "「返信時」ON — mọi loại tin admin gửi đều kích hoạt tự xác nhận",
       T3 + "\n- Toggle「返信時の自動確認済み変更」đã bật ON và đã lưu\n"
       "- Có 7 hội thoại khác nhau, mỗi hội thoại đang có tin chưa xác nhận",
       "1. Ở hội thoại 1 gửi tin text\n"
       "2. Ở hội thoại 2 gửi sticker\n"
       "3. Ở hội thoại 3 gửi ảnh\n"
       "4. Ở hội thoại 4 gửi audio\n"
       "5. Ở hội thoại 5 gửi video\n"
       "6. Ở hội thoại 6 gửi file\n"
       "7. Ở hội thoại 7 gửi vị trí\n"
       "8. Quan sát số chưa xác nhận của cả 7 hội thoại",
       "text · sticker · ảnh · audio · video · file · vị trí",
       "- Cả 7 hội thoại đều được tự xác nhận sau khi admin gửi\n"
       "- Số chưa xác nhận của cả 7 hội thoại về 0",
       note="Gộp 7 loại tin vì CÙNG 1 kết quả mong đợi. Nguồn: SC r34-r42 (OK + staging OK, liệt kê "
            "text/stamp/image/audio/video/file/location/keyword auto reply/template)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "「返信時」ON — sau khi tự xác nhận, friend nhắn tin mới thì lại thành chưa xác nhận",
       T3 + "\n- Toggle「返信時の自動確認済み変更」đã bật ON\n"
       "- Hội thoại X vừa được tự xác nhận (số chưa xác nhận = 0)\n" + FRIEND,
       "1. Xác nhận hội thoại X đang ở trạng thái đã xác nhận hết\n"
       "2. Từ tài khoản LINE test gửi 1 tin mới tới LOA\n"
       "3. Quan sát lại hội thoại X ở màn chat 1:1",
       "Tin text bất kỳ",
       "- Hội thoại X quay lại trạng thái CHƯA xác nhận\n"
       "- Số chưa xác nhận tăng lên 1",
       note="Nguồn: SC r43 (OK + staging OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-001", "Normal",
       "TẮT toggle「返信時」— admin trả lời KHÔNG tự xác nhận các tin cũ",
       T3 + "\n- Toggle「返信時の自動確認済み変更」đã TẮT và đã lưu\n"
       "- Hội thoại X đang có ≥ 1 tin chưa xác nhận",
       "1. Ghi lại số chưa xác nhận của hội thoại X\n"
       "2. Mở màn chat 1:1, gửi 1 tin trả lời cho hội thoại X\n"
       "3. Quan sát lại trạng thái chưa xác nhận của hội thoại X",
       "Tin text bất kỳ",
       "- `bots.confirm_message_user_send` = 0\n"
       "- Hội thoại X VẪN ở trạng thái chưa xác nhận, số chưa xác nhận không đổi\n"
       "- Chỉ khi bấm nút xác nhận thủ công thì mới chuyển sang đã xác nhận",
       note="Nguồn: SC r45-r46 (OK + staging OK) · v1 r109 (BS_033, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-DB-001", "Normal",
       "Bật toggle「ブロックされた友だちの…」— friend block bot thì tin chưa xác nhận bị xóa đúng phạm vi",
       T3 + "\n- Toggle「ブロックされた友だちの自動確認済み変更」đã bật ON và đã lưu\n"
       "- Có 2 hội thoại X và Y, cả hai đều đang có tin chưa xác nhận",
       "1. Ghi lại số chưa xác nhận của X và Y\n"
       "2. Friend của hội thoại X thực hiện block / unfollow LOA trên LINE\n"
       "3. Quan sát hội thoại X và hội thoại Y ở màn chat 1:1\n"
       "4. Kiểm tra `unconfirm_message` của X và Y, và `conversation.confirm_count` của X",
       "—",
       "- Toàn bộ tin chưa xác nhận của hội thoại X bị xóa; hội thoại X hiển thị đã xác nhận hết\n"
       "- Hội thoại Y KHÔNG bị đụng tới, số chưa xác nhận của Y giữ nguyên\n"
       "- `conversation.confirm_count` của X = 0",
       note="BR-13 — cờ này áp cho CẢ event unfollow lẫn leave group. Nguồn: v2 r189 (TC-SC-189, "
            "Not Tested) · SC r49-r51 (OK + staging OK) · v1 r111 (BS_036)"),

    tc("Tự động xác nhận tin nhắn", "DATA-DB-001", "Normal",
       "TẮT toggle「ブロックされた友だちの…」— friend block bot thì tin vẫn ở trạng thái chưa xác nhận",
       T3 + "\n- Toggle「ブロックされた友だちの自動確認済み変更」đã TẮT và đã lưu\n"
       "- Hội thoại X đang có tin chưa xác nhận",
       "1. Ghi lại số chưa xác nhận của hội thoại X\n"
       "2. Friend của hội thoại X thực hiện block / unfollow LOA trên LINE\n"
       "3. Quan sát hội thoại X ở màn chat 1:1 và kiểm tra `unconfirm_message` của X",
       "—",
       "- `bots.confirm_message_user_block_bot` = 0\n"
       "- Tin của hội thoại X VẪN ở trạng thái chưa xác nhận, `unconfirm_message` không bị xóa\n"
       "- Số chưa xác nhận của X giữ nguyên như bước 1",
       note="⚠️ Phụ thuộc MT-19 — tab「improve count comfirm_message」(2023) r20/r58/r96 ghi "
            "『user block bot → confirm_count vẫn giữ nguyên』, khớp với nhánh cờ TẮT này. "
            "Nguồn: SC r52-r53 (OK + staging OK) · v1 r112 (BS_037, OK)"),

    tc("Tự động xác nhận tin nhắn", "DATA-COUNT-001", "Normal",
       "「返信時」ON — `bots.count_user_unconfirm` tính lại đúng, không âm, không nhân đôi",
       T3 + "\n- Toggle「返信時」đã bật ON và đã lưu\n"
       "- Hội thoại X đang có ≥ 1 tin chưa xác nhận\n"
       "- Bot có 2 tài khoản dùng (admin + staff) đều đang xem",
       "1. Ghi lại `bots.count_user_unconfirm` và số hiển thị trên màn của cả admin lẫn staff\n"
       "2. Admin gửi 1 tin trả lời cho hội thoại X từ màn chat 1:1\n"
       "3. Đọc lại `bots.count_user_unconfirm` và `unconfirm_message`\n"
       "4. Đọc lại số hiển thị của admin và của staff",
       "—",
       "- `count_user_unconfirm` giảm đúng bằng số hội thoại vừa được xử lý\n"
       "- Giá trị KHÔNG âm, không tăng ngược, không nhân đôi\n"
       "- Số hiển thị của admin và staff cùng phản ánh một con số nhất quán",
       note="BR-05 — Laravel `ChatService` tính lại `count_user_unconfirm`. Nguồn: v2 r188 "
            "(TC-SC-188, Not Tested)"),
]

S11 = [
    tc("Phím tắt gửi", "UI-003", "Normal",
       "Mặc định — chọn sẵn「送信：Shift + Enter　改行：Enter」",
       T4 + "\n- Bot mới hoặc chưa từng đổi cấu hình này",
       "1. Mở Tab 4「送信ショートカット」\n"
       "2. Quan sát 2 nút chọn (radio)",
       "—",
       "- Nút「送信：Shift + Enter　改行：Enter」đang được chọn (●)\n"
       "- `bots.setting_shortcut` = 0",
       note="Nguồn: v2 r119 (TC-SC-036, Pass staging + production) · SC r56"),

    tc("Phím tắt gửi", "FUNC-001", "Normal",
       "Chọn「送信：Enter」rồi lưu — toast hiện và lựa chọn được giữ",
       T4 + "\n- Đang chọn option 1 (Shift+Enter để gửi)",
       "1. Bấm chọn「送信：Enter　改行：Shift + Enter」\n"
       "2. Bấm nút「保存」\n"
       "3. Nhấn F5 rồi quay lại Tab 4",
       "—",
       "- Toast「保存しました」xuất hiện\n"
       "- Option 2 được chọn (●), `bots.setting_shortcut` = 1\n"
       "- Sau F5 vẫn là option 2, không quay về mặc định",
       note="Nguồn: v2 r118 (TC-SC-035, Pass) + v2 r120 (TC-SC-091, Not Tested) · SC r64"),

    tc("Phím tắt gửi", "FUNC-SEQ-001", "Normal",
       "Đổi lựa chọn nhưng KHÔNG bấm「保存」rồi F5 — quay về giá trị đã lưu",
       T4,
       "1. Chọn option khác với option hiện tại\n"
       "2. KHÔNG bấm「保存」\n"
       "3. Nhấn F5\n"
       "4. Quan sát 2 nút chọn",
       "—",
       "- Sau reload: lựa chọn trở về option đã lưu trước đó\n"
       "- Thay đổi chưa lưu bị bỏ",
       note="Nguồn: v2 r122 (TC-SC-136, Pass staging + production) · SC r61 · SC r67"),

    tc("Phím tắt gửi", "UI-FIELD-001", "Normal",
       "Bấm vào phần chữ (label) cũng chọn được option",
       T4,
       "1. Bấm vào phần chữ của option (KHÔNG bấm trúng nút tròn)",
       "—",
       "- Option tương ứng vẫn được chọn (●)",
       note="Nguồn: v1 r117 (BS_040, Pass)"),

    tc("Phím tắt gửi", "DATA-001", "Normal",
       "Đã lưu「送信：Enter」— ở màn chat 1:1 nhấn Enter là gửi tin",
       T4 + "\n- Đã lưu option 2「送信：Enter　改行：Shift + Enter」",
       "1. Mở màn chat 1:1 (FA-001), chọn 1 hội thoại\n"
       "2. Nhập nội dung tin nhắn vào khung soạn thảo\n"
       "3. Nhấn phím Enter (không giữ Shift)",
       "ショートカットテスト",
       "- Tin nhắn được GỬI ngay khi nhấn Enter\n"
       "- Hành vi đúng theo cấu hình vừa lưu, không phải mặc định Shift+Enter",
       note="BR-05-02 — cấu hình chỉ tác động phía trình duyệt (`chat.js`/`chat-v2.js`). "
            "Nguồn: v2 r121 (TC-SC-092, Not Tested) · SC r65"),

    tc("Phím tắt gửi", "DATA-001", "Normal",
       "Đã lưu「送信：Enter」— ở màn chat 1:1 nhấn Shift+Enter là xuống dòng",
       T4 + "\n- Đã lưu option 2「送信：Enter　改行：Shift + Enter」",
       "1. Mở màn chat 1:1, chọn 1 hội thoại\n"
       "2. Nhập nội dung tin nhắn\n"
       "3. Nhấn Shift + Enter",
       "ショートカットテスト",
       "- Con trỏ xuống dòng trong khung soạn thảo\n"
       "- Tin nhắn KHÔNG được gửi",
       note="Nguồn: SC r66 (OK). Tách riêng vì kết quả mong đợi ngược với TC gửi bằng Enter"),

    tc("Phím tắt gửi", "DATA-001", "Normal",
       "Đã lưu「送信：Shift + Enter」— Shift+Enter gửi tin, Enter xuống dòng",
       T4 + "\n- Đã lưu option 1「送信：Shift + Enter　改行：Enter」",
       "1. Mở màn chat 1:1, nhập nội dung tin nhắn\n"
       "2. Nhấn Shift + Enter\n"
       "3. Nhập nội dung khác, nhấn Enter (không giữ Shift)",
       "ショートカットテスト",
       "- Bước 2: tin nhắn được GỬI\n"
       "- Bước 3: con trỏ xuống dòng, tin nhắn KHÔNG được gửi",
       note="Nguồn: SC r59-r60 (OK)"),

    tc("Phím tắt gửi", "SEC-ISO-001", "Normal",
       "Cấu hình phím tắt lưu theo BOT, không theo từng người dùng",
       "- Bot đang chọn có 2 tài khoản dùng chung: user A (admin) và user B (staff)\n"
       "- Cả 2 đăng nhập ở 2 trình duyệt riêng, cùng 1 bot",
       "1. User A vào Tab 4 chọn option 1 → bấm「保存」\n"
       "2. User B vào Tab 4 chọn option 2 → bấm「保存」\n"
       "3. User A nhấn F5 và quan sát lại Tab 4",
       "—",
       "- Sau bước 3: user A thấy option 2 (giá trị của lần lưu CUỐI)\n"
       "- Cấu hình lưu vào `bots.setting_shortcut` theo BOT, không tách theo từng người dùng",
       note="Nguồn: v1 r116 (BS_039, OK — tiêu đề TC ghi『Lưu theo user』nhưng kết quả mong đợi ghi "
            "『Lưu theo bot』, khớp với spec `bots.setting_shortcut`)"),
]

S12 = [
    tc("URL rút gọn", "UI-003", "Normal",
       "Mặc định — toggle「短縮URLの利用」đang TẮT",
       T5 + "\n- Bot mới hoặc chưa từng đổi cấu hình này",
       "1. Mở Tab 5「短縮URLの利用」\n"
       "2. Quan sát toggle",
       "—",
       "- Toggle ở trạng thái TẮT (「利用しない」)\n"
       "- `bots.is_shorten_url` = 0",
       note="Nguồn: v1 r118 (BS_041, OK STG) · SC r69"),

    tc("URL rút gọn", "FUNC-001", "Normal",
       "Bật toggle rồi lưu — toast hiện và giá trị được giữ sau F5",
       T5 + "\n- Toggle đang TẮT",
       "1. Bấm toggle「短縮URLの利用」sang BẬT\n"
       "2. Bấm nút「保存」\n"
       "3. Nhấn F5 rồi quay lại Tab 5",
       "—",
       "- Toast「保存しました」xuất hiện\n"
       "- Toggle ở trạng thái BẬT, `bots.is_shorten_url` = 1\n"
       "- Sau F5 toggle vẫn BẬT",
       note="Nguồn: v2 r123 (TC-SC-037, Pass staging + production) · SC r70"),

    tc("URL rút gọn", "UI-FIELD-001", "Normal",
       "Khung「短縮リンクの例」luôn hiển thị dù toggle BẬT hay TẮT",
       T5,
       "1. Quan sát trang khi toggle đang TẮT\n"
       "2. Bấm toggle sang BẬT\n"
       "3. Quan sát lại",
       "—",
       "- Bước 1: khung「短縮リンクの例」hiển thị\n"
       "- Bước 3: khung「短縮リンクの例」VẪN hiển thị, không bị ẩn\n"
       "- Dạng URL trong khung: `https://s.lmes.jp/l/abcdefgh`",
       note="BR-06-03 / BR-06-04 (QA-018/019). Nguồn: v2 r124 (TC-SC-038, Pass staging + production)"),

    tc("URL rút gọn", "FUNC-SEQ-001", "Normal",
       "Bật/tắt toggle nhưng KHÔNG bấm「保存」rồi F5 — quay về giá trị đã lưu",
       T5,
       "1. Đổi trạng thái toggle「短縮URLの利用」\n"
       "2. KHÔNG bấm「保存」\n"
       "3. Nhấn F5\n"
       "4. Quan sát toggle",
       "—",
       "- Sau reload: toggle về đúng giá trị đã lưu trước đó\n"
       "- Thay đổi chưa lưu bị bỏ",
       note="Nguồn: v2 r126 (TC-SC-137, Pass staging + production) · SC r75"),

    tc("URL rút gọn", "DATA-001", "Normal",
       "Toggle BẬT — gửi tin chứa URL ở chat 1:1 thì link được rút gọn",
       T5 + "\n- Toggle「短縮URLの利用」đã BẬT và đã lưu",
       "1. Mở màn chat 1:1 (FA-001), chọn 1 hội thoại\n"
       "2. Soạn tin nhắn chứa 1 URL dài\n"
       "3. Gửi tin\n"
       "4. Quan sát tin trên màn chat 1:1 và trên LINE của friend",
       "https://example.com/very/long/path",
       "- Tin gửi thành công\n"
       "- URL trong tin đã gửi hiển thị dạng rút gọn `https://s.lmes.jp/l/xxxxxxxx`, không phải URL gốc\n"
       "- Trên LINE của friend cũng hiển thị link rút gọn",
       env="PRODUCTION",
       note="BR-06-02 — rút gọn thực hiện ở phía server (`ChatMessages.php`/`functions.php:7944`). "
            "Nguồn: v2 r125 (TC-SC-093, Not Tested) · SC r71. RULE-08: domain → chạy PRODUCTION"),

    tc("URL rút gọn", "INTG-LINE-001", "Normal",
       "Link rút gọn bấm được và mở đúng trang gốc",
       T5 + "\n- Toggle đã BẬT và đã gửi 1 tin chứa URL cho friend test",
       "1. Trên LINE của friend, bấm vào link rút gọn vừa nhận\n"
       "2. Quan sát trang được mở",
       "https://example.com/very/long/path",
       "- Link mở đúng trang gốc đã gửi\n"
       "- Không báo lỗi 404 hay chuyển hướng sai",
       env="PRODUCTION",
       note="Nguồn: SC r72 (OK)"),

    tc("URL rút gọn", "DATA-COUNT-001", "Normal",
       "Link rút gọn xuất hiện ở màn URL分析 và đếm lượt bấm",
       T5 + "\n- Toggle đã BẬT, đã gửi tin chứa URL và friend đã bấm vào link 1 lần",
       "1. Mở menu「URL分析」(FA-023)\n"
       "2. Tìm bản ghi link vừa gửi\n"
       "3. Đọc số lượt người dùng đã bấm",
       "1 lượt bấm từ friend test",
       "- Link vừa gửi có trong danh sách của màn URL分析\n"
       "- Số lượt bấm = 1, khớp với số lần friend thực sự bấm",
       env="PRODUCTION",
       note="Liên kết FA-023/FA-024. Nguồn: SC r73-r74 (OK)"),

    tc("URL rút gọn", "DATA-001", "Normal",
       "Toggle TẮT — gửi tin chứa URL thì giữ nguyên link gốc",
       T5 + "\n- Toggle「短縮URLの利用」đã TẮT và đã lưu",
       "1. Mở màn chat 1:1, soạn tin chứa 1 URL dài\n"
       "2. Gửi tin\n"
       "3. Quan sát tin trên màn chat 1:1 và trên LINE của friend\n"
       "4. Mở menu「URL分析」và tìm link vừa gửi",
       "https://example.com/very/long/path",
       "- Link hiển thị nguyên dạng gốc, KHÔNG bị rút gọn\n"
       "- Không sinh bản ghi link rút gọn mới ở màn URL分析",
       env="PRODUCTION",
       note="Nguồn: SC r76-r79 (OK) · Improve chung / tab「Improve shorten」r19-r20 "
            "(『setting ở template và chat 11』→『hiển thị link gốc, ko insert vào bảng url_shorten』)"),

    tc("URL rút gọn", "COMPAT-LEGACY-001", "Normal",
       "Link rút gọn CŨ (tạo trước đợt đổi định dạng) vẫn mở được",
       "- Có tin nhắn cũ trong hội thoại chứa link rút gọn theo định dạng cũ\n"
       "  (dạng `https://s.lmes.jp/s/<bot_id>/...` còn kèm bot_id)",
       "1. Mở hội thoại có tin nhắn cũ trên LINE của friend\n"
       "2. Bấm vào link rút gọn cũ\n"
       "3. Quan sát trang được mở",
       "Link rút gọn định dạng cũ",
       "- Link cũ vẫn mở được đúng trang gốc\n"
       "- Không báo lỗi, không chuyển hướng sai",
       env="PRODUCTION",
       note="Nguồn: Improve chung / tab「Improve shorten」(2024-01-17) r21-r22 (『link cũ → user vẫn "
            "mở được』, OK). Tab này chủ yếu thuộc FA-023/FA-024, chỉ lấy phần hồi quy liên quan Tab 5"),

    tc("URL rút gọn", "DATA-DB-001", "Boundary",
       "Gửi cùng 1 URL nhiều lần — mỗi lần sinh 1 mã rút gọn riêng",
       T5 + "\n- Toggle「短縮URLの利用」đã BẬT và đã lưu",
       "1. Ở màn chat 1:1 gửi 1 tin chứa URL X\n"
       "2. Gửi tiếp tin thứ 2 cũng chứa đúng URL X\n"
       "3. So sánh 2 link rút gọn nhận được\n"
       "4. Bấm thử cả 2 link",
       "Cùng 1 URL gửi 2 lần",
       "- 2 lần gửi sinh ra 2 mã rút gọn KHÁC NHAU\n"
       "- Cả 2 link đều mở đúng URL gốc",
       env="PRODUCTION",
       note="Nguồn: Improve chung / tab「Improve shorten」r4 (『mỗi lần send gen ra 1 unique_key khác "
            "nhau và msg_id khác nhau』, OK + staging + branch release + step)"),
]

S13 = [
    tc("Xem trước khi gửi", "UI-003", "Normal",
       "Mặc định — toggle「送信プレビュー」đang BẬT",
       T6 + "\n- Bot mới hoặc chưa từng đổi cấu hình này",
       "1. Mở Tab 6「送信プレビュー」\n"
       "2. Quan sát toggle",
       "—",
       "- Toggle ở trạng thái BẬT (「利用する」)\n"
       "- `bots.preview_after_send` = 1 (giá trị mặc định của DB)",
       note="BR-07-01. Nguồn: v2 r129 (TC-SC-041, Pass staging + production) · SC r81 · v1 r123 (BS_047)"),

    tc("Xem trước khi gửi", "FUNC-001", "Normal",
       "Tắt toggle rồi lưu — toast hiện và giá trị được giữ sau F5",
       T6 + "\n- Toggle đang BẬT (mặc định)",
       "1. Bấm toggle「送信プレビュー」sang TẮT\n"
       "2. Bấm nút「保存」\n"
       "3. Nhấn F5 rồi quay lại Tab 6",
       "—",
       "- Toast「保存しました」xuất hiện\n"
       "- Toggle ở trạng thái TẮT, `bots.preview_after_send` = 0\n"
       "- Sau F5 toggle vẫn TẮT",
       note="Nguồn: v2 r127 (TC-SC-039, Pass staging + production) · SC r85"),

    tc("Xem trước khi gửi", "UI-FIELD-001", "Normal",
       "Khung「ご注意」luôn hiển thị dù toggle BẬT hay TẮT",
       T6,
       "1. Quan sát trang khi toggle đang BẬT\n"
       "2. Bấm toggle sang TẮT\n"
       "3. Quan sát lại",
       "—",
       "- Bước 1: khung cảnh báo「ご注意」(nền hồng, viền đỏ) hiển thị cùng link「詳細を見る」\n"
       "- Bước 3: khung「ご注意」VẪN hiển thị, không bị ẩn\n"
       "- Link「詳細を見る」vẫn còn",
       note="BR-07-03 (QA-020). Nguồn: v2 r128 (TC-SC-040, Pass staging + production)"),

    tc("Xem trước khi gửi", "UI-001", "Normal",
       "Link「詳細を見る」trong khung「ご注意」mở trang hướng dẫn ở tab mới",
       T6,
       "1. Bấm link「詳細を見る」trong khung「ご注意」\n"
       "2. Quan sát tab trình duyệt mới",
       "—",
       "- Mở `https://lme.jp/manual/cancel_sent_message/` ở tab trình duyệt MỚI\n"
       "- Trang Tab 6 không bị thay đổi",
       note="Nguồn: v2 r131 (TC-SC-139, Pass staging + production). URL đã confirm ở "
            "screens/SCR-07-send-preview.md. SC r87 ghi link「こちら」trỏ tayori.com — CẦN VERIFY "
            "xem là 2 link khác nhau hay đã đổi"),

    tc("Xem trước khi gửi", "FUNC-SEQ-001", "Normal",
       "Đổi toggle nhưng KHÔNG bấm「保存」rồi F5 — quay về giá trị đã lưu",
       T6,
       "1. Đổi trạng thái toggle「送信プレビュー」\n"
       "2. KHÔNG bấm「保存」\n"
       "3. Nhấn F5\n"
       "4. Quan sát toggle",
       "—",
       "- Sau reload: toggle về giá trị đã lưu (mặc định BẬT nếu chưa từng đổi)\n"
       "- Thay đổi chưa lưu bị bỏ",
       note="Nguồn: v2 r130 (TC-SC-138, Pass staging + production) · SC r84"),

    tc("Xem trước khi gửi", "OUT-PREVIEW-001", "Normal",
       "Toggle BẬT — bấm gửi ở chat 1:1 thì hiện modal xem trước",
       T6 + "\n- Toggle「送信プレビュー」đã BẬT và đã lưu",
       "1. Mở màn chat 1:1 (FA-001), chọn 1 hội thoại\n"
       "2. Nhập nội dung tin nhắn\n"
       "3. Bấm nút gửi",
       "プレビューテスト",
       "- Modal xem trước hiện ra TRƯỚC khi tin được gửi\n"
       "- Nội dung trong modal khớp đúng nội dung vừa soạn\n"
       "- Tin chỉ được gửi sau khi xác nhận trong modal",
       note="Nguồn: v2 r129 · SC r83 (OK) · v1 r123 (BS_047, OK STG)"),

    tc("Xem trước khi gửi", "OUT-PREVIEW-001", "Normal",
       "Toggle TẮT — bấm gửi ở chat 1:1 thì gửi thẳng, không hiện modal",
       T6 + "\n- Toggle「送信プレビュー」đã TẮT và đã lưu",
       "1. Mở màn chat 1:1, nhập nội dung tin nhắn\n"
       "2. Bấm nút gửi",
       "プレビューテスト",
       "- KHÔNG hiện modal xem trước\n"
       "- Tin được gửi ngay",
       note="Nguồn: v1 r122 (BS_046, Pass) · SC r85"),

    tc("Xem trước khi gửi", "STATE-001", "Normal",
       "Tích「không hiển thị preview nữa」trong modal — toggle Tab 6 chuyển sang TẮT",
       T6 + "\n- Toggle「送信プレビュー」đang BẬT",
       "1. Mở màn chat 1:1, soạn tin và bấm gửi → modal xem trước hiện ra\n"
       "2. Tích ô「không hiển thị preview nữa」trong modal rồi xác nhận gửi\n"
       "3. Quay lại `/basic/chat-setting` Tab 6 và quan sát toggle\n"
       "4. Gửi 1 tin khác ở chat 1:1",
       "プレビューテスト",
       "- Sau bước 3: toggle「送信プレビュー」ở Tab 6 đã chuyển sang TẮT\n"
       "- Bước 4: không còn hiện modal xem trước",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-24 — cơ chế ô tích trong modal tự tắt toggle Tab 6 KHÔNG có trong spec "
            "(feature-spec §3.9 chỉ mô tả toggle). Nguồn: v1 r125 (BS_049, Pass OK STG)"),

    tc("Xem trước khi gửi", "STATE-001", "Normal",
       "Bật lại toggle sau khi đã tích「không hiển thị preview nữa」— modal hiện lại",
       T6 + "\n- Toggle「送信プレビュー」đang TẮT do đã tích ô trong modal xem trước",
       "1. Bật lại toggle「送信プレビュー」→ bấm「保存」\n"
       "2. Mở màn chat 1:1, soạn tin và bấm gửi",
       "プレビューテスト",
       "- Toggle ở trạng thái BẬT (「利用する」)\n"
       "- Modal xem trước hiện lại bình thường khi bấm gửi",
       note="⚠️ Phụ thuộc MT-24. Nguồn: v1 r126 (BS_050, Pass OK STG)"),
]

S14 = [
    tc("Hiển thị đã đọc (FAQ)", "FUNC-001", "Normal",
       "Tab 7 là trang FAQ tĩnh — 3 cặp hỏi đáp, không có form, không có nút lưu",
       T7,
       "1. Bấm tab 7「既読情報の表示」ở thanh tab\n"
       "2. Quan sát toàn bộ nội dung trang",
       "—",
       "- Trang hiển thị 3 cặp hỏi đáp về thông tin đã đọc\n"
       "- KHÔNG có ô nhập nào trên trang\n"
       "- KHÔNG có nút「保存」\n"
       "- Các link「詳細はこちら」hiển thị",
       note="BR-08A-01. Nguồn: v2 r132 (TC-SC-042, Pass staging + production) · SC r88-r89"),

    tc("Hiển thị đã đọc (FAQ)", "UI-001", "Normal",
       "3 link「詳細はこちら」mở đúng 3 trang FAQ tương ứng ở tab mới",
       T7,
       "1. Bấm「詳細はこちら」của câu hỏi 1 (既読確認) — quan sát URL mở ra\n"
       "2. Quay lại, bấm của câu hỏi 2 (既読マーク)\n"
       "3. Quay lại, bấm của câu hỏi 3 (既読がつかない)",
       "—",
       "- Mỗi link mở 1 tab trình duyệt MỚI tới đúng trang tayori.com tương ứng:\n"
       "  Q1 → `.../2428a5bc23663bf2b0480f4736914b500a651929/`\n"
       "  Q2 → `.../42526ee2955b317d4877e250bbb714cf57b974aa/`\n"
       "  Q3 → `.../83730f1da300fb8945775099760c320054b054cf/`\n"
       "- Trang Tab 7 không bị thay đổi",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-25 — 3 URL cụ thể lấy từ SC r89-r91 (2025, OK) và v1; spec/screens chỉ "
            "ghi chung『tayori.com FAQ』. v2 r134 (TC-SC-140, Pass) cũng ghi『verify lại URL chính xác "
            "khi automation』. Nguồn: v2 r133-r134 (TC-SC-043, TC-SC-140)"),

    tc("Xem trước khi gửi", "UI-001", "Normal",
       "Link「こちら」trong khung「ご注意」của Tab 6 mở đúng trang FAQ",
       T6,
       "1. Ở Tab 6「送信プレビュー」, tìm khung「ご注意」\n"
       "2. Bấm link「こちら」\n"
       "3. Quan sát tab trình duyệt mới",
       "—",
       "- Mở tab mới tới trang FAQ tayori.com\n"
       "  (`.../0a5aee0439630290b4f...` theo ghi nhận 2025)\n"
       "- Trang Tab 6 không bị thay đổi",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-25 — SC r87 (OK + staging + step OK) ghi link「こちら」trỏ tayori.com, "
            "còn v2 r131 (TC-SC-139) ghi link「詳細を見る」trỏ `lme.jp/manual/cancel_sent_message/`. "
            "CẦN LEADER CHỐT là 2 link khác nhau hay 1 link đã đổi đích"),
]
