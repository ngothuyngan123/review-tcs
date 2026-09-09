# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 10-11: tab「テスト方法」và khối「ご注意事項」
(hướng dẫn tự test action, link video, link sang màn quản lý LINE OA).

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」:
r101-r115 (新規), r193-r204 (既存), r329-r340 (ブロック解除), r373-r374, r392-r393.
"""
from _common import tc

NEW = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang 新規友だち用 (/basic/setting-add-friend) → click tab「テスト方法」")
UNB = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang ブロック解除時用 (/basic/setting-add-friend-unblock) → tab「テスト方法」")
ALL3 = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
        "- Chuẩn bị mở tab「テスト方法」của cả 3 trang")

S4 = [
    # ═══════════ 10. Tab テスト方法 ═══════════
    tc("Tab テスト方法", "UI-001", "Normal",
       "Tab テスト方法 trang 新規友だち用 — tiêu đề khối và 4 bước hướng dẫn",
       NEW,
       "1. Mở trang 新規友だち用, click tab「テスト方法」\n"
       "2. Đọc tiêu đề khối và nội dung từng bước trong sơ đồ",
       "Trang add_new",
       "- Tiêu đề khối:「新規友だち用アクションのテスト方法」\n"
       "- Tiêu đề phụ:「すでにエルメに表示されているLINEアカウントの場合」\n"
       "- Sơ đồ có ĐỦ 4 bước, đúng nguyên văn theo thứ tự:\n"
       "  1「エルメの友だち詳細ページ「削除」より友だち情報を削除」\n"
       "  2「スマホのLINE上でLINE公式アカウントをブロック」\n"
       "  3「スマホのLINE上の設定でLINE公式アカウントを削除」\n"
       "  4「LINE公式アカウントを再度友だち追加」",
       note="Nguồn: r101-r106. ✅ ĐÓNG GAP #1 của feature-spec.md §9 — spec ghi『Nội dung tab "
            "テスト方法 cho 新規友だち用 và 既存友だち用 chưa được quan sát trực tiếp』; TC nguồn đã "
            "mô tả đủ 4 bước cho trang 新規友だち用. Đề xuất bổ sung vào ui-spec.md."),

    tc("Tab テスト方法", "UI-001", "Normal",
       "Tab テスト方法 trang ブロック解除時用 — chỉ 2 bước, tiêu đề riêng của trang",
       UNB,
       "1. Mở trang ブロック解除時用, click tab「テスト方法」\n"
       "2. Đọc tiêu đề khối và các bước trong sơ đồ",
       "Trang unblock",
       "- Tiêu đề khối:「ブロック解除時用アクションのテスト方法」\n"
       "- Sơ đồ có 2 bước:\n"
       "  1「LINE公式アカウントをブロック&ブロック解除」\n"
       "  2「設定したアクションが稼働すれば テスト成功」",
       note="⚠️ MÂU THUẪN MT-04: tab master r329-r331 (trang unblock) và r193-r195 (trang old) ghi "
            "tiêu đề khối là「新規友だち用アクションのテスト方法」— tức 3 trang dùng CHUNG tiêu đề của "
            "trang 新規. Còn ui-spec.md:190 (quan sát 05/2026) ghi「ブロック解除時用アクションの"
            "テスト方法」. Nếu TC gốc đúng thì đây là BUG hiển thị sai tiêu đề. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Tab テスト方法", "UI-001", "Normal",
       "Tab テスト方法 trang 既存友だち用 — tiêu đề khối phải là 既存友だち用アクションのテスト方法",
       "- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang 既存友だち用 (/basic/setting-add-friend-old) → tab「テスト方法」",
       "1. Mở trang 既存友だち用, click tab「テスト方法」\n"
       "2. Đọc tiêu đề khối hướng dẫn\n"
       "3. Đọc nội dung các bước",
       "Trang add_old",
       "- Tiêu đề khối là「既存友だち用アクションのテスト方法」(KHÔNG phải 新規友だち用)\n"
       "- Nội dung hướng dẫn: block rồi bỏ block LINE OA trên app LINE (theo tab "
       "「Improve setting add fr 1.0」r18: 「LINE上でLINE公式アカウントをブロック→ブロック解除を"
       "行ってください。(ブロック→ブロック解除操作は10秒間ほど間をおいて行なってください)」)",
       note="⚠️ MÂU THUẪN MT-04 (xem TC trên) — tab master r193 ghi tiêu đề là 新規友だち用. "
            "Expected ở đây viết theo hành vi ĐÚNG suy từ ui-spec + tab 1.0 → DỰ KIẾN CÓ THỂ FAIL, "
            "nếu FAIL cần raise bug. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Tab テスト方法", "REG-URL-001", "Normal",
       "Link テスト方法を動画で確認 — mở đúng video hướng dẫn trên YouTube",
       UNB,
       "1. Mở tab「テスト方法」\n"
       "2. Click link「テスト方法を動画で確認」\n"
       "3. Quan sát tab mới mở ra",
       "Trang unblock",
       "- Mở YouTube đúng video id 9TTugIBdQGs\n"
       "- Video phát được (không lỗi private/không tồn tại)\n"
       "- Link nhảy tới đúng mốc thời gian được cấu hình (tham số t)",
       note="Nguồn: r373 (ghi rõ link https://www.youtube.com/watch?si=...&t=56&v=9TTugIBdQGs) + "
            "ui-spec.md:196. ⚠️ Tham số mốc thời gian ở 2 nguồn LỆCH nhau: r373 ghi t=56, "
            "ui-spec.md:196 ghi t=354 — cần Leader chốt mốc đúng (MT-15).",
       spec="Đã hỏi leader"),

    tc("Tab テスト方法", "UI-001", "Abnormal",
       "Link テスト方法を動画で確認 trên trang ブロック解除時用 — kiểm tra link có tồn tại",
       UNB,
       "1. Mở tab「テスト方法」của trang ブロック解除時用\n"
       "2. Tìm link「テスト方法を動画で確認」\n"
       "3. Nếu có thì click và quan sát",
       "Trang unblock",
       "- Link có tồn tại và click ra đúng video hướng dẫn\n"
       "- KHÔNG có link chết (click không ra gì / 404)",
       note="Nguồn: r392 — dòng『check click vào hyperlink テスト方法を動画で確認』của trang unblock "
            "có kết quả thực thi OK nhưng cột kết quả mong đợi TRỐNG. Expected do AI viết. "
            "Cần Leader xác nhận."),

    tc("Tab テスト方法", "UI-001", "Normal",
       "Khối 友だち追加URL vẫn hiển thị khi đang ở tab テスト方法",
       UNB,
       "1. Mở trang ブロック解除時用, click tab「テスト方法」\n"
       "2. Quan sát phần trên của trang",
       "Trang unblock, tab テスト方法",
       "- Khối「友だち追加URL」(URL + nút copy + QR + nút tải + link giải thích) vẫn hiển thị đủ\n"
       "- Nút「保存」vẫn ở cuối trang",
       note="Nguồn: ui-spec.md:180-185, :205 + r354 (link 友だち追加URLとの違い được kiểm ở tab "
            "テスト方法). Corpus TCs không tách riêng — TC do AI bổ sung."),

    # ═══════════ 11. ご注意事項 & link ngoài ═══════════
    tc("ご注意事項 & link ngoài", "UI-001", "Normal",
       "Khối ご注意事項 — đúng tiêu đề và đủ 2 dòng lưu ý",
       ALL3,
       "1. Mở tab「テスト方法」của cả 3 trang\n"
       "2. Đọc nguyên văn khối「ご注意事項」",
       "3 trang",
       "- Tiêu đề khối:「ご注意事項」\n"
       "- Dòng 1:「・LINE公式アカウント管理画面のあいさつメッセージが設定されている場合は、"
       "どちらも送信されます。（エルメのみに統一することを推奨します。）」\n"
       "- Dòng 2:「・認証済みアカウントをエルメと接続した時に、自動で取得される既存の友だちには、"
       "友だち追加時アクションは稼働しません。」",
       note="Nguồn: r107-r110, r196-r199, r332-r335. ⚠️ Ở tab nguồn dòng lưu ý thứ 2 bị lặp 2 lần "
            "(r109 = r110, r198 = r199, r334 = r335) — đã gộp về 1, cần verify trên màn thật xem "
            "hiển thị 2 hay 3 dòng."),

    tc("ご注意事項 & link ngoài", "UI-001", "Normal",
       "Hộp nội dung ご注意事項 — hiển thị đúng kích thước, không click được",
       ALL3,
       "1. Mở tab「テスト方法」\n"
       "2. Quan sát khung hộp của khối「ご注意事項」(kích thước, không tràn chữ)\n"
       "3. Click vào vùng trống trong hộp → quan sát",
       "3 trang",
       "- Hộp hiển thị đủ nội dung, không tràn chữ ra ngoài, không bị cắt\n"
       "- Click vào hộp không xảy ra gì (không mở link, không mở modal)",
       note="Nguồn: r111, r112, r200, r201, r336, r337."),

    tc("ご注意事項 & link ngoài", "UI-001", "Normal",
       "Hướng dẫn tắt あいさつメッセージ của LINE OA — đúng nguyên văn chuỗi thao tác",
       ALL3,
       "1. Mở tab「テスト方法」\n"
       "2. Đọc dòng hướng dẫn tắt あいさつメッセージ phía LINE OA",
       "3 trang",
       "- Hiển thị đúng chuỗi:「LINE公式アカウント管理画面」+「にログイン > 設定 > 応答設定 > "
       "応答機能「あいさつメッセージ」をオフにする」\n"
       "- Phần「LINE公式アカウント管理画面」là hyperlink, phần còn lại là text thường",
       note="Nguồn: r113-r115, r202-r204, r338-r340."),

    tc("ご注意事項 & link ngoài", "UI-001", "Normal",
       "Hover hyperlink LINE公式アカウント管理画面 — text hiện gạch chân",
       ALL3,
       "1. Mở tab「テスト方法」\n"
       "2. Rê chuột lên hyperlink「LINE公式アカウント管理画面」",
       "Dùng chuột trên PC",
       "- Text hiện gạch chân khi hover",
       note="Nguồn: r113, r202, r338."),

    tc("ご注意事項 & link ngoài", "REG-URL-001", "Normal",
       "Click hyperlink LINE公式アカウント管理画面 — sang trang đăng nhập quản lý LINE OA",
       ALL3,
       "1. Mở tab「テスト方法」\n"
       "2. Click hyperlink「LINE公式アカウント管理画面」\n"
       "3. Quan sát trang mở ra",
       "3 trang",
       "- Mở trang đăng nhập của LINE Business (account.line.biz), sau đăng nhập vào được màn "
       "quản lý LINE Official Account\n"
       "- Link không chết, không 404",
       note="Nguồn: r114, r203, r339 và r374, r393 (ghi rõ URL account.line.biz/login?redirectUri=…"
            "manager.line.biz). ⚠️ TC từ 05/2025 — LINE có thể đã đổi URL/luồng đăng nhập, "
            "CẦN VERIFY LẠI."),

    tc("ご注意事項 & link ngoài", "MSG-USER-001", "Normal",
       "Bật あいさつメッセージ ở cả LINE OA và エルメ — friend nhận CẢ HAI tin nhắn",
       "- LINE OA của bot đang BẬT あいさつメッセージ với nội dung riêng\n"
       "- Trang 新規友だち用 của エルメ đã cài tin nhắn chào mừng riêng\n"
       "- Có 1 tài khoản LINE test chưa từng kết bạn với bot",
       "1. Vào account.line.biz → 設定 → 応答設定 → BẬT「あいさつメッセージ」với nội dung「LOA msg」\n"
       "2. Ở エルメ, trang 新規友だち用 lưu tin nhắn「ELME msg」\n"
       "3. Dùng tài khoản LINE test kết bạn với bot\n"
       "4. Đọc toàn bộ tin nhắn nhận được trên app LINE",
       "LINE OA: 「LOA msg」· エルメ: 「ELME msg」",
       "- Friend nhận ĐỦ CẢ HAI tin:「LOA msg」và「ELME msg」\n"
       "- Sau đó tắt あいさつメッセージ của LINE OA rồi kết bạn bằng tài khoản test khác: chỉ nhận "
       "「ELME msg」",
       env="PRODUCTION",
       note="Nguồn: r108, r197, r333 (nội dung lưu ý『どちらも送信されます』) + feature-spec.md §2.4. "
            "Corpus chỉ kiểm TEXT của lưu ý, KHÔNG kiểm hành vi thật — TC do AI bổ sung theo RULE-06 "
            "(đi tới output cuối trên LINE). Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("ご注意事項 & link ngoài", "MSG-USER-001", "Normal",
       "Friend cũ được tự động import khi kết nối tài khoản xác thực — KHÔNG chạy action chào mừng",
       "- Có 1 LINE OA đã xác thực (認証済みアカウント) đang có sẵn nhiều friend\n"
       "- Trang 既存友だち用 đã cài tin nhắn + action (VD gắn tag TX)\n"
       "- LINE OA này CHƯA kết nối với エルメ",
       "1. Cài tin nhắn + action gắn tag TX ở trang 既存友だち用, bấm 保存\n"
       "2. Thực hiện kết nối LINE OA đã xác thực vào エルメ\n"
       "3. Chờ hệ thống tự import danh sách friend cũ\n"
       "4. Mở màn danh sách bạn bè, kiểm tra các friend vừa import\n"
       "5. Hỏi 1 friend test trong nhóm import xem có nhận tin nhắn chào mừng không",
       "LINE OA xác thực có sẵn ≥5 friend",
       "- Các friend được auto-import KHÔNG bị gắn tag TX\n"
       "- Các friend này KHÔNG nhận tin nhắn chào mừng của trang 既存友だち用",
       env="PRODUCTION",
       note="Nguồn: r109, r198, r334 + ui-spec.md:101-102. Corpus chỉ kiểm TEXT của lưu ý — TC do "
            "AI bổ sung để kiểm hành vi thật. Rủi ro CAO: nếu chạy nhầm sẽ spam hàng loạt friend cũ. "
            "Cần Leader xác nhận.",
       spec="Đã hỏi leader"),
]
