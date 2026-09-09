# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 1-3: điều hướng 3 trang, khối thông tin đầu
trang, khối 友だち追加URL & QR.

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」
(05/2025 → 03/2026, tab master còn sống). Số dòng `r<n>` ở cột Ghi chú là dòng của
tab master, trừ khi ghi rõ file/tab khác.
"""
from _common import tc

NEW = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA (role 主管理者)\n"
       "- Vào Sidebar →「友だち追加設定」→「あいさつメッセージ」→ trang 新規友だち用\n"
       "  (/basic/setting-add-friend)")
OLD = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang 既存友だち用 (/basic/setting-add-friend-old)")
UNB = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang ブロック解除時用 (/basic/setting-add-friend-unblock)")

S1 = [
    # ═══════════ 1. Điều hướng & khung 3 trang ═══════════
    tc("Điều hướng & khung 3 trang", "FUNC-001", "Normal",
       "Mở đủ 3 trang あいさつメッセージ từ menu — đúng URL, đúng sub-title",
       NEW,
       "1. Đăng nhập Admin, chọn 1 bot\n"
       "2. Mở lần lượt 3 mục con của「あいさつメッセージ」trên sidebar\n"
       "3. Với mỗi trang: đọc thanh URL + sub-title phía trên tiêu đề",
       "3 trang: 新規友だち用 · 既存友だち用 · ブロック解除時用",
       "- Trang 1: URL /basic/setting-add-friend · sub-title「新規友だち用」\n"
       "- Trang 2: URL /basic/setting-add-friend-old · sub-title「既存友だち用」\n"
       "- Trang 3: URL /basic/setting-add-friend-unblock · sub-title「ブロック解除時用」\n"
       "- Cả 3 trang đều có title chính「あいさつメッセージ設定」\n"
       "- Không trang nào lỗi 404/500, console không có lỗi JavaScript",
       note="Nguồn: r4 (Check điều hướng), r118, r256 + feature-spec.md §2.1-2.3. "
            "TC gốc chỉ có tiêu đề『Check điều hướng』, không có kết quả mong đợi — expected do AI "
            "viết bám ui-spec.md:39/92/131, cần Leader xác nhận."),

    tc("Điều hướng & khung 3 trang", "UI-001", "Normal",
       "Cả 3 trang hiển thị đủ 2 tab メッセージ・アクション設定 và テスト方法, tab 1 active mặc định",
       NEW,
       "1. Mở lần lượt 3 trang あいさつメッセージ\n"
       "2. Quan sát dải tab ngay dưới khối thông tin đầu trang\n"
       "3. Click tab「テスト方法」rồi quan sát thanh URL và nút cuối trang",
       "3 trang: add_new / add_old / unblock",
       "- Mỗi trang có đúng 2 tab:「メッセージ・アクション設定」và「テスト方法」\n"
       "- Tab「メッセージ・アクション設定」đang active khi vừa vào trang\n"
       "- Click tab「テスト方法」→ đổi nội dung ngay, KHÔNG reload trang (URL không đổi)\n"
       "- Nút「保存」vẫn hiển thị cuối trang kể cả khi đang ở tab テスト方法",
       note="Nguồn: r5 (Check UI) + ui-spec.md:60-62, :205. Gộp 3 trang vì cùng 1 kết quả."),

    tc("Điều hướng & khung 3 trang", "UI-001", "Normal",
       "Title chính「あいさつメッセージ設定」hiển thị đúng trên cả 3 trang",
       NEW,
       "1. Mở lần lượt 3 trang\n"
       "2. Đọc dòng tiêu đề chính",
       "3 trang: add_new / add_old / unblock",
       "- Cả 3 trang hiển thị nguyên văn「あいさつメッセージ設定」\n"
       "- Không trang nào còn tên cũ「友だち追加時設定」ở tiêu đề",
       note="Nguồn: r6, r120, r258. Gộp 3 trang vì cùng 1 kết quả."),

    tc("Điều hướng & khung 3 trang", "UI-001", "Normal",
       "Trang tải xong tự lấy cấu hình — hiển thị lại đúng tin nhắn và action đã lưu",
       NEW + "\n- Trang 新規友だち用 đã lưu sẵn 1 tin nhắn và 2 action",
       "1. Mở trang 新規友だち用\n"
       "2. Chờ trang tải xong\n"
       "3. Quan sát ô nhập tin nhắn và danh sách action dưới nút アクション追加・編集\n"
       "4. F5 tải lại trang, quan sát lại",
       "Tin nhắn:「{name}さん、友だち追加ありがとうございます！」(có ký tự xuống dòng) · "
       "2 action type テキスト",
       "- Ô nhập hiển thị đúng nội dung tin nhắn đã lưu, giữ nguyên ký tự xuống dòng\n"
       "- Danh sách action hiển thị đủ 2 action, đúng thứ tự đã lưu\n"
       "- Sau F5 nội dung không đổi, không bị rỗng",
       note="Nguồn: r51 + feature-spec.md §2.1. Đối chứng live MCP dev 2026-08-26: API lấy cấu hình "
            "trả về {actionId, message, detailAction[], urlAddFriend, qrCode}."),

    tc("Điều hướng & khung 3 trang", "FUNC-001", "Normal",
       "Bot chưa từng lưu cấu hình — vào trang vẫn hiển thị bình thường, không báo lỗi",
       "- Có 1 bot MỚI liên kết LOA, chưa từng mở/lưu màn あいさつメッセージ",
       "1. Đăng nhập Admin, chọn bot mới\n"
       "2. Mở lần lượt 3 trang あいさつメッセージ\n"
       "3. Quan sát nội dung trang\n"
       "4. Bấm 保存 khi chưa nhập gì, rồi mở lại trang",
       "Bot mới, chưa có cấu hình chào mừng",
       "- Cả 3 trang mở được, KHÔNG hiện lỗi『không tìm thấy cấu hình』\n"
       "- Ô nhập tin nhắn rỗng, bộ đếm hiển thị 0/5,000\n"
       "- Khối action hiển thị「エルメアクションは登録されていません」\n"
       "- Bấm 保存 thành công, mở lại trang vẫn rỗng và không lỗi",
       note="Nguồn: feature-spec.md §5 BR-01 (tự tạo cấu hình khi bot chưa có). Corpus TCs KHÔNG có "
            "case này — TC do AI bổ sung từ spec, cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Điều hướng & khung 3 trang", "UI-003", "Abnormal",
       "Mất mạng lúc trang đang tải cấu hình — không hiện màn rỗng như thể chưa cấu hình",
       NEW + "\n- Trang 新規友だち用 đã lưu sẵn tin nhắn + action\n"
             "- Mở DevTools → tab Network",
       "1. Ở DevTools chọn chế độ Offline\n"
       "2. Mở trang 新規友だち用\n"
       "3. Quan sát ô nhập tin nhắn, danh sách action, thông báo trên màn\n"
       "4. Bật mạng lại, F5 và quan sát",
       "Ngắt mạng đúng thời điểm trang gọi API lấy cấu hình",
       "- KHÔNG hiển thị ô tin nhắn rỗng như thể chưa từng cấu hình (false success)\n"
       "- Có dấu hiệu lỗi hoặc trạng thái loading rõ ràng để admin biết chưa tải được dữ liệu\n"
       "- Sau khi bật mạng và F5, dữ liệu cũ hiện lại nguyên vẹn, không bị mất",
       note="TC do AI bổ sung (UI-003 — rủi ro false success: admin tưởng chưa cấu hình rồi bấm 保存 "
            "sẽ XÓA cấu hình cũ). Corpus không có. Cần Leader xác nhận.",
       spec="Spec không ghi"),

    # ═══════════ 2. Khối thông tin đầu trang ═══════════
    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Info box trang 新規友だち用 — đúng 3 mảnh text và marker 新規友だち",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Đọc nguyên văn nội dung trong info box (khối có icon)",
       "Trang add_new",
       "- Info box ghép đủ 3 mảnh:「このページで設定したメッセージ・アクションは」+ marker "
       "「新規友だち」+「のみ稼働します。」\n"
       "- Marker「新規友だち」được tô nổi bật khác phần text còn lại\n"
       "- Icon minh họa hiển thị đủ, không vỡ ảnh",
       note="Nguồn: r25-r30 + ui-spec.md:44-46."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Info box trang 既存友だち用 — có thêm dòng lưu ý về friend tự động import",
       OLD,
       "1. Mở trang 既存友だち用\n"
       "2. Đọc nguyên văn info box",
       "Trang add_old",
       "- Dòng 1:「このページで設定したメッセージ・アクションは」+ marker「既存友だち」+"
       "「のみ稼働します。」\n"
       "- Dòng 2 (chỉ trang này mới có):「認証済みアカウントを接続した時に、自動で取得される"
       "既存の友だちにはアクションは稼働しません。」",
       note="Nguồn: r123-r127 + ui-spec.md:99-102. Đây là điểm KHÁC trang 新規 → tách TC riêng."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Info box trang ブロック解除時用 — marker ブロックを解除した友だち",
       UNB,
       "1. Mở trang ブロック解除時用\n"
       "2. Đọc nguyên văn info box",
       "Trang unblock",
       "- Info box có marker「ブロックを解除した友だち」(KHÔNG phải 新規友だち / 既存友だち)\n"
       "- Kết câu「のみ稼働します」",
       note="Nguồn: r261-r265 + feature-spec.md §2.3."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Link phụ đầu trang — 2 trang kết bạn dùng 流入経路, trang unblock dùng ブロック解除経路",
       NEW,
       "1. Mở trang 新規友だち用, đọc link phụ cạnh tiêu đề\n"
       "2. Làm tương tự với trang 既存友だち用 và ブロック解除時用",
       "3 trang",
       "- Trang 新規友だち用 và 既存友だち用:「友だちの流入経路を分析したい場合はこちら」\n"
       "- Trang ブロック解除時用:「友だちのブロック解除経路を分析したい場合はこちら」\n"
       "- Cả 3 link đều đổi con trỏ thành hình bàn tay khi hover",
       note="Nguồn: r349, r355, r375 + ui-spec.md:43, :98, :137. Giữ chung 1 TC vì cùng 1 phép so "
            "sánh, giá trị mong đợi của từng trang đã liệt kê đủ."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Click link 友だちの流入経路を分析したい場合はこちら — hiện khối giải thích QRコードアクション",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click link「友だちの流入経路を分析したい場合はこちら」\n"
       "3. Đọc nội dung hiện ra",
       "Trang add_new",
       "- Hiện khối nội dung tiêu đề「流入経路（友だち追加経路）を分析したい場合」\n"
       "- Nội dung nêu: dùng QRコードアクション để phân tích nguồn và cài tin nhắn/action riêng "
       "cho từng nguồn\n"
       "- Trong nội dung có hyperlink「QRコードアクション」",
       note="Nguồn: r349. Trang unblock (r375) nội dung nói về ブロック解除経路 — xem TC kế."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Click link phân tích trên trang ブロック解除時用 — nội dung nói về ブロック解除経路",
       UNB,
       "1. Mở trang ブロック解除時用\n"
       "2. Click link「友だちのブロック解除経路を分析したい場合はこちら」\n"
       "3. Đọc nội dung hiện ra",
       "Trang unblock",
       "- Nội dung nêu phân tích「ブロック解除経路」(KHÔNG phải 友だち追加経路)\n"
       "- Có hyperlink「QRコードアクション」",
       note="Nguồn: r375 (nội dung đối chiếu r355 khối trang old). Kết quả KHÁC trang 新規 → "
            "tách TC riêng."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Đóng khối giải thích 流入経路 — click ra ngoài hoặc click lại chính link đều tắt",
       NEW,
       "1. Mở trang 新規友だち用, click link 流入経路 để hiện khối giải thích\n"
       "2. Click ra vùng trống bên ngoài → quan sát\n"
       "3. Click lại link 流入経路 để mở, rồi click chính link đó lần nữa → quan sát",
       "Trang add_new",
       "- Bước 2: khối giải thích tắt\n"
       "- Bước 3: khối giải thích tắt (click lại link đang mở = đóng)",
       note="Nguồn: r350, r351."),

    tc("Khối thông tin đầu trang", "REG-URL-001", "Normal",
       "Click hyperlink QRコードアクション — mở TAB MỚI sang màn QR landing của đúng bot",
       NEW,
       "1. Mở trang 新規友だち用, nhập 1 tin nhắn nhưng CHƯA bấm 保存\n"
       "2. Click link 流入経路 → click hyperlink「QRコードアクション」\n"
       "3. Quan sát tab trình duyệt\n"
       "4. Quay lại tab あいさつメッセージ, kiểm tra ô nhập tin nhắn",
       "Tin nhắn nháp: test chua luu",
       "- Mở TAB MỚI, tab あいさつメッセージ vẫn còn nguyên\n"
       "- Tab mới là màn QRコードアクション của ĐÚNG bot đang chọn\n"
       "- Nội dung nháp ở tab cũ không bị mất",
       note="Nguồn: r352, r356, r376. Lặp ở cả 3 trang, cùng kết quả → gộp 1 TC. "
            "Bước 4 (giữ nội dung nháp) do AI bổ sung theo FUNC-DRAFT-001."),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Click marker 新規友だち — hiện khối định nghĩa 新規友だちとは？",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click vào marker「新規友だち」ở khối thông tin đầu trang\n"
       "3. Đọc nội dung hiện ra",
       "Trang add_new",
       "- Hiện khối nội dung tiêu đề「新規友だちとは？」\n"
       "- Nội dung nêu: là friend lần đầu thêm LINE OA; friend đã có từ trước khi dùng エルメ và "
       "friend từng block rồi bỏ block ĐỀU KHÔNG phải 新規友だち",
       note="Nguồn: r353 (khối improve mới, dưới header r348). ⚠️ MÂU THUẪN MT-05 với r28-r29 cùng "
            "tab ghi『Marker 新規友だち — Click: Không click được』. Hai khối cùng 1 tab, không có "
            "ngày riêng → quy tắc『ưu tiên TC mới nhất』là căn cứ YẾU; chọn khối r348+ vì mô tả chi "
            "tiết hơn và khớp đợt improve 流入経路. CHỜ LEADER CHỐT.",
       spec="Spec không ghi"),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Click marker 既存友だち — hiện khối định nghĩa 既存友だちとは？",
       OLD,
       "1. Mở trang 既存友だち用\n"
       "2. Click vào marker「既存友だち」\n"
       "3. Đọc nội dung hiện ra",
       "Trang add_old",
       "- Hiện khối nội dung tiêu đề「既存友だちとは？」\n"
       "- Nội dung nêu: friend có từ trước khi dùng エルメ, được hiện lên エルメ khi friend nhắn tin "
       "tới; nếu bắt đầu dùng エルメ cùng lúc mở LINE OA thì KHÔNG có 既存友だち",
       note="Nguồn: r357 (tiêu đề dòng gốc ghi『click vào 新規友だち』nhưng nội dung expected là "
            "既存友だちとは？— đọc theo nội dung). Liên quan MT-05.",
       spec="Spec không ghi"),

    tc("Khối thông tin đầu trang", "UI-001", "Normal",
       "Hover và click ảnh minh họa trong info box — không có tác dụng gì",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Rê chuột qua ảnh minh họa trong info box → quan sát\n"
       "3. Click vào ảnh minh họa → quan sát",
       "Trang add_new",
       "- Hover ảnh: không hiện tooltip, không đổi trạng thái\n"
       "- Click ảnh: không mở link, không mở modal, trang không đổi",
       note="Nguồn: r25, r26, r123."),

    # ═══════════ 3. 友だち追加URL & QR ═══════════
    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Khối 友だち追加URL hiển thị đủ: label, URL, nút copy, QR, nút tải, link giải thích",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Quan sát khối「友だち追加URL」",
       "Bot đã liên kết LOA, có URL kết bạn",
       "- Có label「友だち追加URL」\n"
       "- URL dạng https://line.me/R/ti/p/%40<line_id của bot>\n"
       "- Có nút copy URL, ảnh QR hiển thị được (không vỡ ảnh, không 404), nút download QR\n"
       "- Có link「LINE公式アカウントの友だち追加URLとの違い」",
       note="Nguồn: r9, r21, r22 + ui-spec.md:50-56. Đối chứng live MCP dev 2026-08-26."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Khối 友だち追加URL cũng hiển thị trên trang 既存友だち用 và ブロック解除時用",
       OLD,
       "1. Mở trang 既存友だち用 → tìm khối「友だち追加URL」\n"
       "2. Mở trang ブロック解除時用 → tìm khối「友だち追加URL」\n"
       "3. Ở mỗi trang kiểm tra: URL, nút copy, ảnh QR, nút tải, link giải thích\n"
       "4. So URL/QR với trang 新規友だち用",
       "Trang add_old và unblock, cùng 1 bot",
       "- CẢ HAI trang đều có đủ khối 友だち追加URL với các thành phần như trang 新規友だち用\n"
       "- URL và QR trùng khớp với trang 新規友だち用 (cùng bot → cùng URL kết bạn)",
       note="Nguồn: r355-r374 (trang old) và r375-r393 (trang unblock). ⚠️ MÂU THUẪN MT-03: "
            "ui-spec.md:104 và :342 ghi trang 既存友だち用『KHÔNG hiển thị khu vực URL/QR』. "
            "Đối chứng live MCP dev 2026-08-26: API lấy cấu hình với type=add_old VẪN trả "
            "urlAddFriend + qrCode. CHỜ LEADER CHỐT."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Ô URL không sửa được — click 1 lần và double click đều không vào chế độ nhập",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click 1 lần vào ô hiển thị URL → thử gõ ký tự\n"
       "3. Double click vào ô URL → thử gõ ký tự\n"
       "4. F5 và đọc lại URL",
       "URL kết bạn của bot",
       "- Không vào được chế độ nhập, không gõ được ký tự nào\n"
       "- Sau F5, URL giữ nguyên giá trị ban đầu",
       note="Nguồn: r10, r11, r359-r360, r378-r379. Lặp ở cả 3 trang, cùng kết quả → gộp 1 TC."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Hover nút Copy URL — đậm nút và hiện tooltip URLをコピー",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Rê chuột lên nút copy cạnh URL\n"
       "3. Quan sát nút và tooltip",
       "Dùng chuột trên PC (không phải touch)",
       "- Nút đậm lên (đổi trạng thái hover)\n"
       "- Hiện tooltip「URLをコピー」",
       note="Nguồn: r12. Dòng r361/r380 (trang old/unblock) chỉ ghi『Đậm button và hiển thị text "
            "Copy』— đã lấy mô tả chi tiết nhất."),

    tc("友だち追加URL & QR", "FUNC-001", "Normal",
       "Click nút Copy 1 lần — copy đúng URL vào clipboard và hiện コピーしました",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút copy cạnh URL\n"
       "3. Quan sát thông báo trên màn\n"
       "4. Dán (Ctrl+V) vào ô nhập tin nhắn để đối chiếu, sau đó xóa đi (không bấm 保存)",
       "URL kết bạn của bot đang chọn",
       "- Hiện thông báo「コピーしました」\n"
       "- Nội dung dán ra TRÙNG KHỚP từng ký tự với URL hiển thị trên màn",
       note="Nguồn: r13, r362, r381."),

    tc("友だち追加URL & QR", "FUNC-SEQ-001", "Normal",
       "Click nút Copy nhiều lần liên tiếp — lần nào cũng copy đúng, không sinh lỗi",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút copy 2 lần liên tiếp thật nhanh\n"
       "3. Dán ra ô nhập để đối chiếu\n"
       "4. Click tiếp 5 lần nữa, dán lại đối chiếu\n"
       "5. Mở console trình duyệt kiểm tra lỗi",
       "Click 2 lần, rồi 5 lần liên tiếp",
       "- Mỗi lần click đều copy đúng URL (nội dung dán không bị nhân đôi, không rỗng)\n"
       "- Console không có lỗi JavaScript\n"
       "- Thông báo「コピーしました」không chồng nhiều lớp che nội dung trang",
       note="Nguồn: r14, r363, r382 (『Click 2 lần → Copy URL』)."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Ảnh QR không click được — click 1 lần và double click đều không có tác dụng",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click 1 lần vào ảnh QR → quan sát\n"
       "3. Double click vào ảnh QR → quan sát",
       "Ảnh QR của bot",
       "- Không mở lightbox, không mở tab mới, không tải file\n"
       "- Trang không đổi trạng thái",
       note="Nguồn: r15, r16, r364-r365, r383-r384."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Hover nút Download QR — đậm nút và hiện tooltip ダウンロード",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Rê chuột lên nút download dưới ảnh QR",
       "Dùng chuột trên PC",
       "- Nút đậm lên\n"
       "- Hiện tooltip「ダウンロード」",
       note="Nguồn: r17."),

    tc("友だち追加URL & QR", "MEDIA-IMG-001", "Normal",
       "Tải QR về — file ảnh mở được và quét ra đúng URL kết bạn của bot",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút download QR\n"
       "3. Mở file vừa tải trong thư mục Downloads\n"
       "4. Dùng app LINE quét ảnh vừa tải",
       "Bot có line_id @<id>",
       "- Tải về đúng 1 file ảnh PNG, mở xem được, không lỗi file hỏng\n"
       "- Quét QR ra đúng URL https://line.me/R/ti/p/%40<line_id của bot>\n"
       "- Quét bằng app LINE dẫn tới đúng LINE OA của bot đang chọn",
       env="PRODUCTION",
       note="Nguồn: r18 (『Click 1 lần → Download 1 QR』). RULE-06: TC gốc dừng ở『tải được file』, "
            "đã kéo tới output cuối là ảnh mở được + quét ra đúng OA. RULE-08: ảnh nằm trên media "
            "server → bắt buộc chạy PRODUCTION."),

    tc("友だち追加URL & QR", "FUNC-SEQ-001", "Normal",
       "Click Download QR N lần — tải đúng N file, không thiếu không lẫn",
       NEW,
       "1. Xóa sạch thư mục Downloads (hoặc ghi lại số file hiện có)\n"
       "2. Mở trang 新規友だち用\n"
       "3. Click nút download QR 2 lần liên tiếp → đếm file\n"
       "4. Click tiếp 3 lần → đếm file\n"
       "5. Mở lần lượt các file để kiểm tra",
       "Click 2 lần, rồi 3 lần (tổng 5)",
       "- Sau bước 3: có đúng 2 file QR trong Downloads\n"
       "- Sau bước 4: có đúng 5 file QR\n"
       "- Mọi file đều mở được và quét ra cùng 1 URL kết bạn",
       env="PRODUCTION",
       note="Nguồn: r19, r20, r367-r369, r386-r388."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Nội dung giải thích dưới khối URL — đúng nguyên văn",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Đọc đoạn text mô tả dưới khối 友だち追加URL",
       "Trang add_new",
       "- Nguyên văn:「システムの仕様でURLは異なりますが、それぞれに違いはありません。"
       "※エルメ接続後も、LINE公式アカウント管理画面から取得できる友だち追加URLも引き続き利用が可能です。」",
       note="Nguồn: r21."),

    tc("友だち追加URL & QR", "UI-001", "Normal",
       "Link LINE公式アカウントの友だち追加URLとの違い — hiển thị, hover gạch chân, click hiện giải thích",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Kiểm tra nguyên văn text link\n"
       "3. Rê chuột lên link → quan sát\n"
       "4. Click link → đọc nội dung hiện ra",
       "Trang add_new",
       "- Text link đúng:「LINE公式アカウントの友だち追加URLとの違い」\n"
       "- Hover: text hiện gạch chân\n"
       "- Click: hiện khối「LINE公式アカウント管理画面で取得できる友だち追加URLとの違い」kèm giải "
       "thích URL khác nhau nhưng không có khác biệt về chức năng, và URL của LINE OA vẫn dùng được",
       note="Nguồn: r22, r23, r24, r354, r370-r372, r389-r391."),

    tc("友だち追加URL & QR", "DATA-CACHE-001", "Normal",
       "Đổi sang bot khác — URL kết bạn và ảnh QR đổi theo đúng bot mới",
       "- Tài khoản Admin có ≥2 bot đã liên kết LOA (bot A và bot B, line_id khác nhau)",
       "1. Chọn bot A, mở trang 新規友だち用, ghi lại URL và tải QR\n"
       "2. Đổi sang bot B bằng bộ chọn bot, mở lại trang 新規友だち用\n"
       "3. Ghi lại URL và tải QR của bot B\n"
       "4. So sánh 2 cặp URL/QR, quét cả 2 ảnh bằng app LINE",
       "2 bot có line_id khác nhau",
       "- URL của bot B khác bot A và khớp line_id của bot B\n"
       "- Ảnh QR của bot B khác ảnh của bot A, quét ra đúng OA của bot B\n"
       "- Không hiện lại QR cũ do cache trình duyệt",
       env="PRODUCTION",
       note="TC do AI bổ sung theo DATA-CACHE-001 + BR-06 (URL ảnh QR có tham số ?v=<timestamp> "
            "chống cache — feature-spec.md §5 BR-06). Corpus không có case đổi bot ở màn này. "
            "Cần Leader xác nhận.",
       spec="Spec không ghi"),
]
