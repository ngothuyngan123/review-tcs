# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 7-9: khối 上記メッセージ送信以外のアクション登録
(5 nút tắt, modal アクション, danh sách action đã cài) và nút 保存 + bảo vệ đổi bot.

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」:
r63-r99 (新規), r163-r192 (既存), r298-r328 (ブロック解除); tab「Improve setting add
fr 1.0」(04/2023) r20-r22 cho nút 保存.
"""
from _common import tc

NEW = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang 新規友だち用 (/basic/setting-add-friend), tab メッセージ・アクション設定")
ALL3 = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
        "- Chuẩn bị mở lần lượt cả 3 trang: 新規友だち用 · 既存友だち用 · ブロック解除時用")

S3 = [
    # ═══════════ 7. Đăng ký action — 5 nút tắt ═══════════
    tc("Đăng ký action — 5 nút tắt", "UI-001", "Normal",
       "Khối đăng ký action hiển thị đủ tiêu đề, tiêu đề nhỏ, 5 nút tắt và nút アクション追加・編集",
       ALL3,
       "1. Mở lần lượt 3 trang あいさつメッセージ\n"
       "2. Quan sát khối đăng ký action ở mỗi trang",
       "3 trang: add_new / add_old / unblock",
       "- Tiêu đề khối:「上記メッセージ送信以外のアクション登録」\n"
       "- Tiêu đề nhỏ:「よく使われる項目」\n"
       "- Có đủ 5 nút tắt và nút chính「アクション追加・編集」\n"
       "- Bố cục giống nhau ở cả 3 trang",
       note="Nguồn: r63, r64, r163, r164, r298, r299."),

    tc("Đăng ký action — 5 nút tắt", "UI-001", "Normal",
       "Danh sách 5 nút tắt — đúng nhãn và đúng số lượng",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Đọc nguyên văn nhãn của từng nút tắt trong khối「よく使われる項目」\n"
       "3. Đếm số nút",
       "Trang add_new",
       "- Có ĐÚNG 5 nút tắt\n"
       "- Ghi lại nguyên văn nhãn của cả 5 nút để đối chiếu với 2 nguồn đang lệch nhau (xem Ghi chú)",
       note="⚠️ MÂU THUẪN MT-14: tab master (05/2025) r65-r84 liệt kê 5 nút là テンプレート · タグ · "
            "友だち情報 · ステップ配信 · その他; còn ui-spec.md:78-83 (quan sát 05/2026) liệt kê "
            "「ステップ配信を開始・停止する」·「リッチメニューを表示する」·「テンプレートを送信する」·"
            "「タグを付け・外しする」·「その他のアクションをみる」— tức KHÁC nhau ở nút thứ 3 "
            "(友だち情報 ↔ リッチメニュー) và khác cả cách đặt nhãn. CHỜ LEADER CHỐT danh sách đúng."),

    tc("Đăng ký action — 5 nút tắt", "UI-001", "Normal",
       "Hover từng nút tắt — đậm nút và đổi con trỏ thành hình bàn tay",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Rê chuột lần lượt qua cả 5 nút tắt\n"
       "3. Quan sát màu nút và hình con trỏ",
       "5 nút tắt",
       "- Mỗi nút đều đậm lên khi hover\n"
       "- Con trỏ đổi thành hình bàn tay ở cả 5 nút",
       note="Nguồn: r65, r69, r73, r77, r81 (trang 新規 ghi『hiển thị icon bàn tay』) và r165, r169, "
            "r173, r177, r181 (trang 既存 ghi『Đậm button』) — gộp cả 2 mô tả."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Click nút tắt テンプレート — mở modal action và focus sẵn vào tab テンプレート",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「テンプレート」\n"
       "3. Quan sát modal アクション vừa mở",
       "Trang add_new",
       "- Modal「アクション」mở ra\n"
       "- Tab「テンプレート」đang được chọn sẵn (không phải tab đầu tiên mặc định)",
       note="Nguồn: r66, r166, r301. Đóng Gap #2 của feature-spec.md §9 (『Behavior chính xác của "
            "5 shortcut buttons chưa được xác nhận bằng click trực tiếp』)."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Click nút tắt タグ — mở modal action và focus sẵn vào tab タグ",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「タグ」\n"
       "3. Quan sát modal",
       "Trang add_new",
       "- Modal「アクション」mở ra, tab「タグ」đang được chọn sẵn",
       note="Nguồn: r70, r170, r305."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Click nút tắt 友だち情報 — mở modal action và focus sẵn vào tab 友だち情報",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「友だち情報」\n"
       "3. Quan sát modal",
       "Trang add_new",
       "- Modal「アクション」mở ra, tab「友だち情報」đang được chọn sẵn",
       note="Nguồn: r74, r174, r309. ⚠️ Liên quan MT-14 — ui-spec.md:78-83 KHÔNG có nút tắt "
            "友だち情報 mà có「リッチメニューを表示する」. Nếu Leader chốt theo spec thì TC này đổi "
            "thành nút リッチメニュー."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Click nút tắt ステップ配信 — mở modal action và focus sẵn vào tab ステップ",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「ステップ配信」\n"
       "3. Quan sát modal",
       "Trang add_new",
       "- Modal「アクション」mở ra, tab「ステップ」đang được chọn sẵn",
       note="Nguồn: r78, r178, r313."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Click nút tắt その他 — mở modal action nhưng KHÔNG focus vào tab nào",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「その他」\n"
       "3. Quan sát modal",
       "Trang add_new",
       "- Modal「アクション」mở ra\n"
       "- KHÔNG có tab nào được chọn sẵn (khác 4 nút tắt còn lại)",
       note="Nguồn: r82, r182, r317. Kết quả KHÁC 4 nút kia → tách TC riêng."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-001", "Normal",
       "Cài 1 action qua nút tắt — action hiện ngay dưới nút アクション追加・編集",
       NEW + "\n- Bot có sẵn ≥1 template và ≥1 tag",
       "1. Mở trang 新規友だち用\n"
       "2. Click nút tắt「テンプレート」, chọn 1 template, bấm 保存 trong modal\n"
       "3. Quan sát vùng dưới nút「アクション追加・編集」",
       "1 action type テンプレート",
       "- Vùng dưới nút「アクション追加・編集」hiển thị đúng 1 dòng action vừa cài\n"
       "- Dòng action ghi rõ loại action và tên đối tượng đã chọn\n"
       "- Dòng「エルメアクションは登録されていません」biến mất",
       note="Nguồn: r67, r71, r75, r79, r83, r167, r171, r175, r179, r183, r302, r306, r310, r314, "
            "r318 (『Setting 1 action → Hiển thị action đã setting bên dưới button』)."),

    tc("Đăng ký action — 5 nút tắt", "FUNC-MULTI-001", "Normal",
       "Cài N action — hiển thị đủ N action, đúng thứ tự đã cài",
       NEW + "\n- Bot có sẵn ≥2 template, ≥2 tag, ≥1 scenario",
       "1. Mở trang 新規友だち用\n"
       "2. Cài lần lượt 5 action khác loại (template, tag, friend info, scenario, text)\n"
       "3. Bấm 保存, F5 và quan sát danh sách action",
       "5 action: テンプレート → タグ → 友だち情報 → ステップ → テキスト",
       "- Danh sách hiển thị ĐỦ 5 action, KHÔNG bị cắt còn 3\n"
       "- Thứ tự hiển thị đúng thứ tự đã cài\n"
       "- Sau F5 danh sách không đổi",
       note="Nguồn: r68, r72, r76, r80, r84 (『Setting N action → Hiển thị CÁC action đã setting』). "
            "⚠️ MÂU THUẪN MT-12 với tab「Improve setting add fr 1.0」(04/2023) r7-r8 ghi『chỉ hiển "
            "thị tối đa 3 action đầu + text その他 x 件 編集』. Đợt improve 2.0 (05/2025) mới hơn → "
            "chọn theo 2.0; tab 1.0 đã bị thay thế."),

    # ═══════════ 8. Đăng ký action — modal & danh sách ═══════════
    tc("Đăng ký action — modal & danh sách", "FUNC-001", "Normal",
       "Click nút アクション追加・編集 — mở modal setting action",
       ALL3,
       "1. Mở lần lượt 3 trang\n"
       "2. Ở mỗi trang click nút「アクション追加・編集」\n"
       "3. Quan sát modal",
       "3 trang",
       "- Modal「アクション」mở ra ở cả 3 trang\n"
       "- Modal có nút X để đóng và nút 保存 trong modal",
       note="Nguồn: r85, r185, r320."),

    tc("Đăng ký action — modal & danh sách", "FUNC-SEQ-001", "Normal",
       "Double click nút アクション追加・編集 — chỉ mở 1 modal, không chồng 2 lớp",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Double click nhanh nút「アクション追加・編集」\n"
       "3. Quan sát số lớp modal\n"
       "4. Đóng modal bằng nút X và kiểm tra trang phía sau",
       "Double click nhanh",
       "- Chỉ mở 1 modal (không chồng 2 lớp, không kẹt lớp nền mờ)\n"
       "- Đóng modal 1 lần là trở lại trang bình thường, thao tác tiếp được",
       note="Nguồn: r86, r186, r321 (『Double click button → Mở modal setting action』). "
            "Vế『không chồng 2 lớp / không kẹt lớp nền』do AI làm rõ để đo được."),

    tc("Đăng ký action — modal & danh sách", "STATE-001", "Normal",
       "Chọn action trong modal rồi bấm X — hủy bỏ, không cài action nào",
       NEW + "\n- Trang 新規友だち用 đang chưa có action nào",
       "1. Mở trang 新規友だち用, click「アクション追加・編集」\n"
       "2. Chọn 1 action (VD gắn 1 tag) nhưng KHÔNG bấm 保存 trong modal\n"
       "3. Bấm nút X đóng modal\n"
       "4. Quan sát danh sách action trên trang\n"
       "5. F5 và quan sát lại",
       "1 action tag, đóng bằng X",
       "- Sau bước 3: danh sách action vẫn trống, hiển thị「エルメアクションは登録されていません」\n"
       "- Sau F5 vẫn trống — action đã chọn KHÔNG bị lưu lại",
       note="Nguồn: r87, r187, r322 (『setting action => click button X → đóng modal, chưa setting "
            "action nào』)."),

    tc("Đăng ký action — modal & danh sách", "FUNC-002", "Normal",
       "Không chọn action nào rồi bấm 保存 trong modal — cho phép, không báo lỗi bắt buộc",
       NEW,
       "1. Mở trang 新規友だち用, click「アクション追加・編集」\n"
       "2. Không chọn action nào\n"
       "3. Bấm 保存 trong modal\n"
       "4. Quan sát danh sách action trên trang",
       "Modal không chọn action nào",
       "- Không hiện lỗi bắt buộc chọn action\n"
       "- Modal đóng lại, danh sách action vẫn trống\n"
       "- Trang hiển thị「エルメアクションは登録されていません」",
       note="Nguồn: r88, r89, r188, r189, r323, r324."),

    tc("Đăng ký action — modal & danh sách", "UI-003", "Normal",
       "Trạng thái rỗng của khối action — hiện đúng câu エルメアクションは登録されていません",
       ALL3,
       "1. Ở cả 3 trang, xóa hết action (nếu có) và bấm 保存\n"
       "2. F5 từng trang\n"
       "3. Đọc nội dung vùng dưới nút「アクション追加・編集」",
       "3 trang, không có action nào",
       "- Cả 3 trang hiển thị nguyên văn「エルメアクションは登録されていません」\n"
       "- Không hiện danh sách rỗng trắng trơn hoặc lỗi",
       note="Nguồn: r90, r190, r325 + ui-spec.md:84."),

    tc("Đăng ký action — modal & danh sách", "DATA-REF-001", "Normal",
       "Xóa đối tượng đang được action tham chiếu — action đó biến mất khỏi màn cài đặt",
       "- Trang ブロック解除時用 đã cài 1 action gắn tag T và 1 action gửi template M\n"
       "- Tag T và template M vẫn đang tồn tại",
       "1. Ghi lại danh sách action của trang ブロック解除時用\n"
       "2. Sang màn Quản lý tag, xóa tag T\n"
       "3. Sang màn Template, xóa template M\n"
       "4. Quay lại trang ブロック解除時用, F5 và quan sát danh sách action\n"
       "5. Dùng tài khoản LINE test thực hiện block → unblock, quan sát action chạy",
       "Tag T và template M bị xóa sau khi đã gán vào action",
       "- Action tham chiếu tới tag T và template M biến mất khỏi danh sách (không còn dòng mồ côi)\n"
       "- Màn không hiện lỗi, các action còn lại giữ nguyên\n"
       "- Khi unblock: không phát sinh lỗi gửi, chỉ các action còn hiệu lực được chạy",
       env="PRODUCTION",
       note="Nguồn: r326 (『Các loại type action nhưng item bị xóa → xóa item, ở màn setting unblock "
            "xóa luôn action đó』). Bước 5 do AI bổ sung theo RULE-06 (kéo tới output cuối)."),

    tc("Đăng ký action — modal & danh sách", "FUNC-004", "Boundary",
       "Cài số lượng action rất lớn trong 1 trang — hiển thị đủ, lưu được và chạy đủ",
       NEW + "\n- Bot có sẵn ≥10 tag, ≥5 template\n"
             "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Mở trang 新規友だち用, cài lần lượt 20 action (10 gắn tag + 5 gửi template + 5 gửi text)\n"
       "2. Bấm 保存, F5 và đếm số dòng action hiển thị\n"
       "3. Dùng tài khoản LINE test kết bạn\n"
       "4. Đếm số tin nhắn nhận trên app LINE và số tag được gắn ở màn chi tiết friend\n"
       "5. Thử cài thêm action thứ 21 và ghi lại kết quả (có bị chặn không, có thông báo gì)",
       "20 action; sau đó thử action thứ 21",
       "- Sau F5 hiển thị đủ 20 dòng action, không bị cắt\n"
       "- Friend nhận đủ 10 tin (5 template + 5 text) và được gắn đủ 10 tag\n"
       "- Nếu hệ thống có giới hạn số action thì phải chặn kèm thông báo rõ ràng, KHÔNG lưu âm "
       "thầm mất action",
       env="PRODUCTION",
       note="TC do AI bổ sung theo FUNC-004 (RULE-01: quan điểm ưu tiên Cao cần đủ Normal + "
            "Abnormal + Boundary). Corpus chỉ có『Setting N action』chung chung, không nêu ngưỡng. "
            "CẦN LEADER CHỐT có giới hạn số action hay không.",
       spec="Đã hỏi leader"),

    tc("Đăng ký action — modal & danh sách", "MSG-001", "Normal",
       "Action có cài filter — chỉ chạy với friend thỏa mãn điều kiện",
       "- Trang 新規友だち用 đã cài 1 action gắn tag, có filter điều kiện\n"
       "- Có 2 tài khoản LINE test: 1 thỏa mãn filter, 1 không thỏa mãn",
       "1. Mở modal action của trang 新規友だち用, cài filter cho action\n"
       "2. Bấm 保存 trong modal rồi bấm 保存 trang\n"
       "3. Dùng tài khoản LINE test A (thỏa mãn filter) kết bạn → kiểm tra action đã chạy chưa\n"
       "4. Dùng tài khoản LINE test B (không thỏa mãn) kết bạn → kiểm tra",
       "1 action gắn tag + filter theo điều kiện quét QRコードアクション",
       "- Tài khoản A: action chạy, tag được gắn (xem ở màn chi tiết friend)\n"
       "- Tài khoản B: action KHÔNG chạy, không bị gắn tag",
       env="PRODUCTION",
       note="Nguồn: r94, r95 (『check khi action setting filter → thỏa mãn điều kiện filter => "
            "send cho friend』)."),

    tc("Đăng ký action — modal & danh sách", "MSG-001", "Normal",
       "Cài 2 action, 1 có filter không thỏa mãn và 1 không cài filter — chỉ action không filter chạy",
       "- Trang 新規友だち用 cài 2 action: action A có filter (friend test KHÔNG thỏa mãn), "
       "action B không cài filter\n"
       "- Có 1 tài khoản LINE test chưa kết bạn",
       "1. Cài 2 action như tiền điều kiện, bấm 保存\n"
       "2. Dùng tài khoản LINE test kết bạn với bot\n"
       "3. Kiểm tra kết quả của cả 2 action ở màn chi tiết friend / chat 1:1",
       "action A: gắn tag TA + filter không khớp · action B: gắn tag TB, không filter",
       "- Chỉ action B chạy (friend được gắn tag TB)\n"
       "- Action A KHÔNG chạy (friend không có tag TA)",
       env="PRODUCTION",
       note="Nguồn: r96 (kết quả mong đợi ở tab nguồn TRỐNG — expected do AI viết theo logic của "
            "r97). CẦN LEADER XÁC NHẬN."),

    tc("Đăng ký action — modal & danh sách", "MSG-001", "Normal",
       "Cài 2 action, 1 filter không thỏa mãn và 1 filter thỏa mãn — chỉ action thỏa mãn chạy",
       "- Trang 新規友だち用 cài 2 action đều có filter: action A không khớp, action B khớp\n"
       "- Có 1 tài khoản LINE test chưa kết bạn",
       "1. Cài 2 action như tiền điều kiện, bấm 保存\n"
       "2. Dùng tài khoản LINE test kết bạn với bot\n"
       "3. Kiểm tra kết quả của cả 2 action",
       "action A: gắn tag TA + filter không khớp · action B: gắn tag TB + filter khớp",
       "- Chỉ action B chạy (friend được gắn tag TB)\n"
       "- Action A không chạy",
       env="PRODUCTION",
       note="Nguồn: r97 (『có send action thỏa mãn filter』)."),

    tc("Đăng ký action — modal & danh sách", "DATA-REF-001", "Normal",
       "Xóa landing đang được dùng làm điều kiện filter — landing đó không còn trong modal filter",
       "- Có 1 QRコードアクション (landing) L đang được dùng làm điều kiện filter của 1 action "
       "trên trang 新規友だち用",
       "1. Ghi lại điều kiện filter đang có\n"
       "2. Sang màn QRコードアクション xóa landing L\n"
       "3. Quay lại trang 新規友だち用, mở modal action → mở modal filter\n"
       "4. Tìm landing L trong danh sách chọn",
       "Landing L bị xóa",
       "- Landing L KHÔNG còn xuất hiện trong danh sách chọn của modal filter\n"
       "- Modal filter mở được bình thường, không lỗi",
       note="Nguồn: r98 (『check khi xóa landing → không hiển thị landing đó ở modal filter』)."),

    tc("Đăng ký action — modal & danh sách", "DATA-REF-001", "Abnormal",
       "Landing trong filter đã bị xóa và landing đó đã đạt số lần action — action không chạy nữa",
       "- Action trên trang 新規友だち用 có filter theo landing L\n"
       "- Landing L đã ở trạng thái đã chạy action đủ số lần cho phép\n"
       "- Landing L sau đó bị xóa",
       "1. Chuẩn bị đúng tiền điều kiện\n"
       "2. Dùng tài khoản LINE test kết bạn qua đường dẫn tương ứng\n"
       "3. Kiểm tra action của trang 新規友だち用 có chạy không",
       "Landing L đã bị xóa và đã đạt giới hạn số lần action",
       "- Action KHÔNG chạy nữa (vì landing trong filter đã bị xóa)",
       env="PRODUCTION",
       note="Nguồn: r99 — ⚠️ Kết quả thực thi ở tab nguồn là **NG** (chưa fix tại thời điểm test). "
            "Giữ TC nguyên trạng: DỰ KIẾN FAIL → nếu vẫn FAIL phải raise bug. CHỜ LEADER CHỐT "
            "(MT-13)."),

    # ═══════════ 9. Nút 保存 & bảo vệ đổi bot ═══════════
    tc("Nút 保存 & bảo vệ đổi bot", "FUNC-001", "Normal",
       "Bấm 保存 1 lần — lưu cả tin nhắn và action, hiện thông báo thành công",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Nhập tin nhắn mới và cài 1 action mới\n"
       "3. Bấm nút「保存」1 lần\n"
       "4. Quan sát thông báo\n"
       "5. F5 và kiểm tra lại tin nhắn + action",
       "Tin nhắn 「luu 1 lan」+ 1 action gắn tag",
       "- Hiện thông báo lưu thành công\n"
       "- Sau F5, cả tin nhắn và action đều đúng nội dung vừa lưu",
       note="Nguồn: tab「Improve setting add fr 1.0」r21 (『Click btn 1 lần → Save lại các act đã "
            "set』) + api-spec.md EP-05."),

    tc("Nút 保存 & bảo vệ đổi bot", "CONC-001", "Abnormal",
       "Double click nút 保存 — chỉ tạo/cập nhật 1 bản ghi cấu hình, không nhân đôi",
       NEW,
       "1. Mở trang 新規友だち用, nhập tin nhắn mới\n"
       "2. Double click thật nhanh nút「保存」\n"
       "3. Quan sát thông báo hiện ra\n"
       "4. F5 và kiểm tra nội dung\n"
       "5. Dùng tài khoản LINE test kết bạn, đếm số tin nhắn chào mừng nhận được",
       "Double click nút 保存",
       "- Nội dung sau F5 đúng 1 lần, không bị nhân đôi\n"
       "- Cấu hình của bot vẫn là 1 bản ghi duy nhất (mở lại trang không thấy 2 bộ cấu hình)\n"
       "- Friend kết bạn nhận ĐÚNG 1 tin nhắn chào mừng (không nhận 2 tin)",
       env="PRODUCTION",
       note="Nguồn: tab「Improve setting add fr 1.0」r22 (『Double click → Save 1 bản ghi trong "
            "bảng add_friend_setting』) + feature-spec.md §5 BR-05. Bước 5 do AI bổ sung theo "
            "RULE-06."),

    tc("Nút 保存 & bảo vệ đổi bot", "SEC-ISO-001", "Abnormal",
       "Mở 2 tab, đổi bot ở tab khác rồi bấm 保存 — hệ thống chặn, không ghi nhầm sang bot kia",
       "- Tài khoản Admin có ≥2 bot (bot A và bot B)\n"
       "- Ghi lại tin nhắn chào mừng hiện tại của cả 2 bot",
       "1. Tab 1: chọn bot A, mở trang 新規友だち用, sửa tin nhắn thành「AAA」nhưng chưa bấm 保存\n"
       "2. Tab 2: đổi sang bot B\n"
       "3. Quay lại tab 1, bấm「保存」\n"
       "4. Đọc thông báo hiện ra\n"
       "5. Mở lại trang 新規友だち用 của cả bot A và bot B, đối chiếu tin nhắn",
       "Bot A và bot B, nội dung mới「AAA」",
       "- Bấm 保存 ở tab 1 bị CHẶN, hiện thông báo lỗi「別のアカウントに切り替えたので、"
       "要求を処理できません。」\n"
       "- Tin nhắn của bot B KHÔNG bị đổi thành「AAA」\n"
       "- Tin nhắn của bot A cũng giữ nguyên giá trị cũ (thay đổi chưa được lưu)",
       note="Nguồn: feature-spec.md §5 BR-02 + api-spec.md EP-05 (bảo vệ bot-switch). Corpus TCs "
            "KHÔNG có case này — TC do AI bổ sung từ spec, mức rủi ro CAO (ghi nhầm cấu hình sang "
            "bot khác). Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Nút 保存 & bảo vệ đổi bot", "UI-001", "Normal",
       "Nút 保存 hiển thị ở cuối cả 3 trang và ở cả 2 tab",
       ALL3,
       "1. Mở lần lượt 3 trang, cuộn xuống cuối trang → tìm nút「保存」\n"
       "2. Ở mỗi trang click sang tab「テスト方法」→ tìm lại nút「保存」",
       "3 trang × 2 tab",
       "- Cả 3 trang đều có nút「保存」ở cuối trang\n"
       "- Nút「保存」vẫn hiện khi đang ở tab「テスト方法」",
       note="Nguồn: tab 1.0 r20 + ui-spec.md:86, :125, :168, :205."),

    tc("Nút 保存 & bảo vệ đổi bot", "PERM-002", "Abnormal",
       "Gọi thẳng API lưu với loại cấu hình không hợp lệ — hệ thống không ghi hỏng dữ liệu",
       NEW + "\n- Có công cụ gửi request và session Admin hợp lệ\n"
             "- Ghi lại tin nhắn + action hiện tại của cả 3 trang",
       "1. Bắt request lưu khi bấm 保存 ở trang 新規友だち用\n"
       "2. Gửi lại request đó nhưng đổi tham số loại cấu hình thành giá trị không hợp lệ "
       "(VD add_xxx, rỗng, hoặc bỏ hẳn tham số)\n"
       "3. Đọc response\n"
       "4. Mở lại cả 3 trang và đối chiếu tin nhắn + action với bước 0",
       "Loại cấu hình: add_xxx · rỗng · thiếu tham số",
       "- Hệ thống trả lỗi rõ ràng hoặc bỏ qua, KHÔNG trả success giả\n"
       "- Cấu hình của cả 3 trang giữ nguyên, không bị xóa/ghi đè chéo\n"
       "- Không sinh lỗi 500 làm hỏng màn",
       note="TC do AI bổ sung theo PERM-002 + logic-spec.md:319-327 (validate type chỉ implicit qua "
            "switch-case, không có FormRequest). Corpus không có. Cần Leader xác nhận.",
       spec="Spec không ghi"),
]
