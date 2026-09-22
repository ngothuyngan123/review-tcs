# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 6: Đồng bộ trạng thái đối ứng sang nơi dùng.

Trạng thái đối ứng được tạo ở Tab 1 nhưng ĐƯỢC DÙNG ở 3 nơi khác:
• dropdown「対応ステータス」cột phải màn chat 1:1 (FA-001)
• modal lọc「対応ステータス」của màn chat 1:1 / quản lý chat (FA-002)
• app mobile admin (KHÔNG phải LIFF)

Đây là vùng hay lọt bug nhất của FA-041 vì thay đổi ở màn cài đặt phải phản ánh
sang 3 nơi trên. Nguồn chủ yếu là tab「Setting Chat」(07/2025, đã chạy OK + staging)
vì corpus [AI] 2026 để phần lớn nhóm này ở trạng thái Not Tested.
"""
from _common import tc

SETUP = ("- Đăng nhập Admin của LOA, đã chọn 1 bot\n"
         "- Mở được cả `/basic/chat-setting` Tab 1 và màn chat 1:1 (FA-001) của cùng bot")
APP = ("- Đăng nhập app mobile admin (KHÔNG phải LIFF) bằng cùng tài khoản, cùng bot\n"
       "- Mở được màn chat 1:1 trên app")

S6 = [
    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Thêm trạng thái mới — xuất hiện ở dropdown「対応ステータス」màn chat 1:1",
       SETUP,
       "1. Tại Tab 1 bấm「＋ 新規追加」→ nhập「テスト」+ Enter\n"
       "2. Sang màn chat 1:1, chọn 1 hội thoại\n"
       "3. Mở dropdown「対応ステータス」ở cột phải",
       "テスト",
       "- Trạng thái「テスト」có trong dropdown chọn trạng thái của hội thoại\n"
       "- Đứng đúng thứ tự `position` (cuối danh sách vì vừa thêm)",
       note="Nguồn: v2 r38 (TC-SC-133, Not Tested) · SC r198 (OK + staging OK) · SC r210"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Sửa tên + màu trạng thái — dropdown màn chat 1:1 cập nhật theo",
       SETUP + "\n- Đã có trạng thái「テスト」",
       "1. Tại Tab 1 sửa tên「テスト」thành「更新済み」và đổi màu + Enter\n"
       "2. Sang màn chat 1:1, mở dropdown「対応ステータス」",
       "更新済み",
       "- Dropdown hiển thị tên mới「更新済み」với màu mới\n"
       "- Không còn mục tên cũ「テスト」",
       note="Nguồn: SC r158 (OK + staging OK) · v2 r38 (TC-SC-133)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Sửa trạng thái ĐANG được gán cho hội thoại — chip trên hội thoại đổi theo",
       SETUP + "\n- Có hội thoại X đang được gán trạng thái A",
       "1. Tại Tab 1 sửa tên + màu của trạng thái A\n"
       "2. Sang màn chat 1:1, mở hội thoại X\n"
       "3. Quan sát chip trạng thái của hội thoại X",
       "—",
       "- Chip trạng thái của hội thoại X hiển thị tên MỚI và màu MỚI\n"
       "- Hội thoại X vẫn giữ nguyên liên kết với trạng thái A (không bị gỡ về「ステータスなし」)",
       note="Nguồn: SC r157 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Kéo thả sắp xếp — dropdown màn chat 1:1 hiển thị đúng thứ tự mới",
       SETUP + "\n- Có ≥ 3 trạng thái",
       "1. Tại Tab 1 kéo thả đổi thứ tự các trạng thái\n"
       "2. Sang màn chat 1:1, mở dropdown「対応ステータス」\n"
       "3. Đối chiếu thứ tự với danh sách ở Tab 1",
       "—",
       "- Thứ tự trong dropdown khớp đúng thứ tự vừa sắp xếp (theo cột `position`)",
       note="Nguồn: SC r202 (OK + staging OK) · SC r209"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-REF-001", "Normal",
       "Xóa trạng thái đang được gán — hội thoại về「ステータスなし」, dropdown bỏ mục đó",
       SETUP + "\n- Trạng thái X đang được gán cho ≥ 1 hội thoại",
       "1. Tại Tab 1 xóa trạng thái X (xác nhận modal「削除する」)\n"
       "2. Sang màn chat 1:1, tìm hội thoại từng gán trạng thái X\n"
       "3. Quan sát chip trạng thái của hội thoại và mở dropdown chọn trạng thái",
       "—",
       "- Hội thoại chuyển về「ステータスなし」(không có trạng thái)\n"
       "- Dropdown KHÔNG còn trạng thái X\n"
       "- `conversation.id_status` được đặt về NULL (BR-02)",
       note="Nguồn: v2 r36 (TC-SC-131, Not Tested) · SC r186-r187 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "UI-003", "Boundary",
       "Tên trạng thái dài 20 ký tự — hiển thị rút gọn ở màn chat 1:1",
       SETUP,
       "1. Tại Tab 1 tạo trạng thái tên dài đúng 20 ký tự\n"
       "2. Sang màn chat 1:1, mở dropdown「対応ステータス」và gán cho 1 hội thoại\n"
       "3. Quan sát cách hiển thị tên",
       "あ × 20",
       "- Tên hiển thị rút gọn khoảng 10 ký tự +「…」, không tràn khung\n"
       "- Hover / mở dropdown vẫn xem được tên đầy đủ (hoặc theo thiết kế hiện hành)",
       spec="Đã hỏi leader",
       note="⚠️ Mốc『10 ký tự + …』lấy từ SC r199 · r201 · r211 · r213 (2025, OK + staging OK); "
            "v2 r38 (TC-SC-133) ghi『⚠ Verify truncation với Figma』— CẦN VERIFY LẠI với giao diện 2026"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Thêm / sửa / xóa trạng thái — modal lọc「対応ステータス」cập nhật theo",
       SETUP,
       "1. Tại Tab 1 thêm trạng thái「フィルタ用」\n"
       "2. Sang màn chat 1:1, mở modal lọc, xem mục「対応ステータス」\n"
       "3. Quay lại Tab 1 sửa tên thành「フィルタ済」\n"
       "4. Mở lại modal lọc và quan sát\n"
       "5. Quay lại Tab 1 xóa trạng thái đó\n"
       "6. Mở lại modal lọc và quan sát",
       "フィルタ用 → フィルタ済",
       "- Bước 2: modal lọc có mục「フィルタ用」\n"
       "- Bước 4: mục đổi thành「フィルタ済」, không còn tên cũ\n"
       "- Bước 6: mục đó biến mất khỏi modal lọc",
       note="Nguồn: SC r159 · SC r210 · SC r212 · SC r214 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-REF-001", "Abnormal",
       "Đang lọc theo 1 trạng thái thì trạng thái đó bị xóa — kết quả lọc trống, mục biến mất",
       SETUP + "\n- Màn chat 1:1 đang lọc theo trạng thái X",
       "1. Ở phiên khác (hoặc app) xóa trạng thái X tại Tab 1\n"
       "2. Quay lại màn chat 1:1 đang lọc theo X, bấm tìm lại\n"
       "3. Mở modal lọc và quan sát mục「対応ステータス」",
       "—",
       "- Kết quả tìm kiếm hiển thị trống\n"
       "- Mở modal lọc: không còn trạng thái X trong danh sách chọn\n"
       "- Không lỗi trắng màn, không lỗi JS",
       note="Nguồn: SC r216 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "SYNC-APP-001", "Normal",
       "Thêm trạng thái trên web — app mobile admin hiển thị trạng thái mới",
       SETUP + "\n" + APP,
       "1. Trên web, Tab 1 thêm trạng thái「アプリ確認」+ Enter\n"
       "2. Trên app mobile mở màn chat 1:1, kéo refresh\n"
       "3. Mở danh sách chọn trạng thái của 1 hội thoại",
       "アプリ確認",
       "- Danh sách trạng thái trên app có「アプリ確認」\n"
       "- Đúng màu và đúng thứ tự như trên web",
       note="Nguồn: SC r205 (OK + staging OK). App ở đây là APP MOBILE ADMIN, không phải LIFF"),

    tc("Đồng bộ trạng thái sang nơi dùng", "SYNC-APP-001", "Normal",
       "Sửa trạng thái trên web — app mobile admin cập nhật, kể cả hội thoại đang dùng",
       SETUP + "\n" + APP + "\n- Có hội thoại đang gán trạng thái A",
       "1. Trên web sửa tên + màu trạng thái A\n"
       "2. Trên app kéo refresh màn chat 1:1\n"
       "3. Quan sát danh sách trạng thái và hội thoại đang gán A",
       "—",
       "- Danh sách trạng thái trên app hiển thị tên + màu mới\n"
       "- Hội thoại đang gán A hiển thị tên + màu mới, không bị gỡ trạng thái",
       note="Nguồn: SC r206-r207 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "SYNC-APP-001", "Normal",
       "Xóa / sắp xếp trạng thái trên web — app mobile admin phản ánh đúng",
       SETUP + "\n" + APP + "\n- Có ≥ 3 trạng thái",
       "1. Trên web xóa 1 trạng thái\n"
       "2. Trên web kéo thả đổi thứ tự các trạng thái còn lại\n"
       "3. Trên app kéo refresh màn chat 1:1, mở danh sách chọn trạng thái",
       "—",
       "- Trạng thái đã xóa không còn trong danh sách trên app\n"
       "- Thứ tự trên app khớp đúng thứ tự vừa sắp xếp trên web",
       note="Nguồn: SC r208-r209 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "CONC-002", "Abnormal",
       "Web sửa — app xóa cùng 1 trạng thái: xóa thắng, web không hiện \"lưu xong rồi mất\"",
       SETUP + "\n" + APP + "\n- Có trạng thái A",
       "1. Trên web: sửa tên/màu trạng thái A nhưng CHƯA reload\n"
       "2. Trên app: xóa trạng thái A\n"
       "3. Trên web: nhấn Enter để lưu phần sửa A\n"
       "4. Reload cả web lẫn app",
       "—",
       "- Sau reload: trạng thái A đã bị xóa ở CẢ 2 phía (xóa thắng)\n"
       "- Web KHÔNG rơi vào cảnh「保存しました」rồi trạng thái biến mất sau ~1 giây\n"
       "- Dữ liệu nhất quán giữa web và app, không có bản ghi mồ côi",
       note="⚠️ Vùng bug cũ: SC r203 ghi rõ『Actual: Save thành công nhưng bị mất sau 1s』và SC r219 "
            "『App báo sửa thành công nhưng reload lại không hiển thị』. Nguồn: v2 r37 (TC-SC-132, "
            "Not Tested — multi-actor, ngoài scope automation) · SC r203 · SC r218-r219"),

    tc("Đồng bộ trạng thái sang nơi dùng", "CONC-002", "Abnormal",
       "Web và app cùng sửa 1 trạng thái — lần lưu cuối thắng, không trộn dữ liệu",
       SETUP + "\n" + APP + "\n- Có trạng thái A",
       "1. Trên web sửa tên A thành「WEB」(chưa lưu)\n"
       "2. Trên app sửa tên A thành「APP」rồi lưu\n"
       "3. Trên web nhấn Enter để lưu「WEB」\n"
       "4. Reload cả 2 phía",
       "WEB / APP",
       "- Sau reload cả 2 phía cùng hiển thị「WEB」(giá trị của lần lưu CUỐI)\n"
       "- KHÔNG có trạng thái nào mang tên lai giữa 2 lần sửa\n"
       "- Chỉ còn đúng 1 bản ghi của trạng thái A",
       note="Nguồn: SC r217 (『Update theo lần save cuối』, OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "CONC-002", "Abnormal",
       "2 tab trình duyệt: tab 1 xóa trạng thái A, tab 2 đang sửa chính A",
       SETUP + "\n- Mở `/basic/chat-setting` Tab 1 trên 2 tab trình duyệt của cùng phiên",
       "1. Tab trình duyệt 2: bấm vào ô nhập tên của trạng thái A, sửa tên (chưa Enter)\n"
       "2. Tab trình duyệt 1: xóa trạng thái A\n"
       "3. Tab trình duyệt 2: nhấn Enter để lưu\n"
       "4. Reload tab trình duyệt 2",
       "—",
       "- Bước 3: hệ thống báo lỗi rõ ràng (bản ghi không còn) HOẶC không tạo lại bản ghi đã xóa\n"
       "- Sau reload: trạng thái A không còn ở cả 2 tab\n"
       "- KHÔNG xảy ra cảnh「保存しました」rồi mất sau 1 giây mà không báo gì",
       spec="Đã hỏi leader",
       note="Nguồn: SC r203 (『Khi xóa status A tại tab 1 >> Edit+save status A tại tab 2』, "
            "Actual ghi『Save thành công nhưng bị mất sau 1s』). Kết quả mong đợi ở đây là SUY LUẬN "
            "của AI theo hướng『không được im lặng』— CẦN LEADER CHỐT hành vi đúng"),

    tc("Đồng bộ trạng thái sang nơi dùng", "DATA-001", "Normal",
       "Thêm trạng thái rồi chuyển tab khác và quay lại — trạng thái mới vẫn trong danh sách",
       SETUP,
       "1. Tại Tab 1 thêm trạng thái mới + Enter\n"
       "2. Bấm sang tab 4「送信ショートカット」\n"
       "3. Bấm quay lại tab 1「対応ステータス編集」",
       "タブ切替テスト",
       "- Danh sách Tab 1 hiển thị đủ trạng thái vừa thêm\n"
       "- Không mất bản ghi, không hiện trùng 2 dòng",
       note="Nguồn: SC r204 (OK + staging OK)"),

    tc("Đồng bộ trạng thái sang nơi dùng", "SEC-ISO-001", "Normal",
       "Sửa trạng thái ở bot A — bot B không bị đụng",
       "- Tài khoản Admin quản lý ≥ 2 bot (A và B)\n"
       "- Cả 2 bot đều có danh sách trạng thái riêng\n"
       "- Ghi lại danh sách trạng thái của bot B trước khi thao tác",
       "1. Chọn bot A ở dropdown account, vào Tab 1\n"
       "2. Thêm 1 trạng thái, sửa 1 trạng thái, xóa 1 trạng thái, kéo thả đổi thứ tự\n"
       "3. Đổi dropdown account sang bot B (mở phiên đăng nhập/trình duyệt riêng)\n"
       "4. Vào Tab 1 của bot B và đối chiếu với danh sách đã ghi ở tiền điều kiện",
       "—",
       "- Danh sách trạng thái của bot B KHÔNG thay đổi: đúng số dòng, đúng tên, màu, thứ tự\n"
       "- Mọi bản ghi `status_chat` được tạo/sửa/xóa đều mang đúng `bot_id` của bot A",
       note="Nguồn: SC r15 · r23 · r31 · r47 · r55 · r62 · r68 · r80 · r86 (『Check update đúng bản "
            "ghi của bot ... (bot khác ko bị update)』, OK). ⚠️ Đổi bot ở 1 tab là đổi cho cả trình "
            "duyệt → phải dùng 2 phiên đăng nhập riêng. Liên quan BR-04 (IDOR trên EP-09 legacy)"),
]
