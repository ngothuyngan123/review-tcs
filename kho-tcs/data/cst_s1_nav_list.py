# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 1-2.

S1 Vào màn & điều hướng tab · S2 Danh sách trạng thái đối ứng.

✅ 2 mâu thuẫn NỀN đã được Leader chốt 2026-09-21 (xem kho-tcs/data/cst_conflicts.py):
• MT-01 — màn có **8 tab** (thêm「チャットのCSVエクスポート」và「重複送信防止機能」).
• MT-02 — CRUD và sắp xếp trạng thái đối ứng là thao tác **INLINE** (＋新規追加 + Enter).
File này đã viết đúng theo 2 quyết định đó. Spec (bản 2025: 6 tab + modal) nay xác định
là LẠC HẬU — việc sửa spec liệt kê ở cột "Việc phải làm tiếp" của MT-01/MT-02.

Nguồn chính: tab「[AI] Flow_setting_chat_v2」(06-07/2026, có kết quả chạy staging +
production) — gọi tắt `v2`; bổ sung từ「AI_TCs_Setting_chat_v1」(`v1`),
「Setting Chat」(10/2024→07/2025, `SC`) và「[AI] Flow_validate_3333」(08/2026, `V3333`).
"""
from _common import tc

ADMIN = "- Đăng nhập Admin của LOA, đã chọn 1 bot bất kỳ trong dropdown account"
TAB1 = ADMIN + "\n- Đang ở `/basic/chat-setting`, Tab 1「対応ステータス編集」đang active"
MT01 = "✅ MT-01 đã chốt 2026-09-21: màn có 8 tab. "
MT02 = "✅ MT-02 đã chốt 2026-09-21: CRUD + sắp xếp trạng thái là thao tác inline. "

S1 = [
    tc("Vào màn & điều hướng tab", "FUNC-001", "Normal",
       "Mở màn cài đặt chat — hiển thị đủ 8 tab đúng thứ tự, Tab 1 active",
       ADMIN,
       "1. Hover menu「1:1チャット」ở sidebar\n"
       "2. Bấm「チャット設定」\n"
       "3. Quan sát URL, tiêu đề trang và danh sách tab ở cột nội dung",
       "—",
       "- URL là `/basic/chat-setting`, trang tải xong không lỗi\n"
       "- Tiêu đề trang là「1:1チャット設定」\n"
       "- Hiển thị đúng 8 tab theo thứ tự: 1「対応ステータス編集」· 2「チャットのCSVエクスポート」·\n"
       "  3「メッセージの自動確認済み変更」· 4「送信ショートカット」· 5「短縮URLの利用」·\n"
       "  6「送信プレビュー」· 7「既読情報の表示」· 8「重複送信防止機能」\n"
       "- Tab 1「対応ステータス編集」active mặc định",
       note=MT01 + "Nguồn: v2 r2 (TC-SC-001, Pass staging + production) · SC r5-r6 (chỉ có title, "
            "chưa có 8 tab). Spec ui-spec.md:47 còn ghi 6 tab → phải sửa theo MT-01"),

    tc("Vào màn & điều hướng tab", "FUNC-001", "Normal",
       "Bấm lần lượt 8 tab — nội dung đổi đúng, không reload cả trang",
       TAB1,
       "1. Bấm tab 2「チャットのCSVエクスポート」\n"
       "2. Bấm tab 3「メッセージの自動確認済み変更」\n"
       "3. Bấm tab 4「送信ショートカット」\n"
       "4. Bấm tab 5「短縮URLの利用」\n"
       "5. Bấm tab 6「送信プレビュー」\n"
       "6. Bấm tab 7「既読情報の表示」\n"
       "7. Bấm tab 8「重複送信防止機能」",
       "—",
       "- Sau mỗi lần bấm: vùng nội dung đổi đúng theo tab được chọn\n"
       "- Tab vừa bấm chuyển sang trạng thái active (highlight), tab trước đó bỏ active\n"
       "- Không reload toàn trang, không lỗi JS trên console",
       note=MT01 + "Nguồn: v2 r3 (TC-SC-002, Pass staging + production)"),

    tc("Vào màn & điều hướng tab", "FUNC-001", "Normal",
       "Vào màn trạng thái đối ứng từ icon bút cạnh dropdown ở màn chat 1:1",
       ADMIN + "\n- Đang mở màn chat 1:1 (FA-001), đã chọn 1 hội thoại",
       "1. Bấm icon bút (✏) cạnh dropdown「対応ステータス」ở cột phải màn chat 1:1\n"
       "2. Quan sát màn hình vừa mở",
       "—",
       "- Mở màn「対応ステータス編集」(Tab 1 của `/basic/chat-setting`)\n"
       "- Tab 1 là option đang active",
       note="Nguồn: SC r94 (OK + staging OK). Lối vào thứ 2 ngoài menu"),

    tc("Vào màn & điều hướng tab", "UI-003", "Normal",
       "Rời tab CSV đang chạy job rồi quay lại — loading state vẫn còn, % không reset",
       ADMIN + "\n- Đang có job CSV chạy dở (status = processing) cho bot đang chọn\n"
       "- Đang xem Tab 2 sub-tab「データ作成」với thanh tiến trình đang chạy",
       "1. Xác nhận sub-tab「データ作成」đang hiển thị loading kèm thanh tiến trình\n"
       "2. Bấm sang tab 4「送信ショートカット」\n"
       "3. Bấm quay lại tab 2「チャットのCSVエクスポート」",
       "—",
       "- Sau bước 2: nội dung tab 4 hiển thị bình thường\n"
       "- Sau bước 3: sub-tab「データ作成」hiển thị LẠI loading kèm thanh tiến trình,\n"
       "  KHÔNG reset về form trống\n"
       "- Giá trị % tiếp tục tăng theo tiến trình thật của job, không nhảy về 0",
       note="Nguồn: v2 r4 (TC-SC-003, Pass staging) — BR-CSV-07 (QA-007)"),

    tc("Vào màn & điều hướng tab", "UI-003", "Abnormal",
       "Mất kết nối khi load 1 tab — báo lỗi rõ, không trắng màn, không báo thành công giả",
       ADMIN,
       "1. Mở DevTools > Network, đặt Offline (hoặc chặn request GET của tab cần test)\n"
       "2. Bấm vào tab 1「対応ステータス編集」\n"
       "3. Lặp lại với tab 2「チャットのCSVエクスポート」",
       "—",
       "- Hiển thị thông báo lỗi rõ ràng khi không tải được dữ liệu\n"
       "- KHÔNG phải màn hình trắng, KHÔNG phải spinner quay vô hạn\n"
       "- KHÔNG hiển thị nhầm trạng thái「保存しました」/ thành công trong khi thực tế lỗi kết nối",
       note="Nguồn: v2 r169 (TC-SC-105, Not Tested) — UI-003"),
]

S2 = [
    tc("Danh sách trạng thái đối ứng", "UI-003", "Normal",
       "Bot mới — hiển thị đúng 5 trạng thái mặc định, cuối danh sách chỉ có nút ＋新規追加",
       ADMIN + "\n- Bot MỚI, chưa từng tùy chỉnh trạng thái đối ứng",
       "1. Mở `/basic/chat-setting`, ở Tab 1「対応ステータス編集」\n"
       "2. Quan sát danh sách và phần cuối danh sách",
       "—",
       "- Hiển thị đúng 5 trạng thái mặc định theo thứ tự:\n"
       "  1「見込みあり」(vàng) · 2「対応中」(xanh dương) · 3「フォロー」(xanh lá) ·\n"
       "  4「トラブル」(đỏ) · 5「対応完了」(đen)\n"
       "- Mỗi dòng có đủ: tay cầm kéo (⠿), ô nhập tên, bộ chọn màu, icon xóa (🗑)\n"
       "- Cuối danh sách KHÔNG có dòng nhập trống nào, chỉ có nút「＋ 新規追加」\n"
       "- Không hiển thị bộ đếm「0/20」ở trạng thái này",
       note=MT02 + "Nguồn: v2 r16 (TC-SC-012, Pass staging + production; expected cũ khẳng định "
            "có sẵn dòng nhập trống đã bị sửa 2026-07-24 → BUG-018 Closed) · SC r100 (5 status default) · "
            "SC r196 (bot mới: friend nào cũng có 5 status default)"),

    tc("Danh sách trạng thái đối ứng", "UI-003", "Normal",
       "Tiêu đề và mô tả của Tab 1 hiển thị đúng",
       TAB1,
       "1. Quan sát phần đầu vùng nội dung Tab 1",
       "—",
       "- Tiêu đề「対応ステータス編集」\n"
       "- Mô tả phụ「対応ステータスのテキストとカラーが変更できます」",
       note="Nguồn: SC r95 · r98 · r99 (OK + staging OK). ⚠️ SC ghi kèm font-size/màu theo XD cũ — "
            "chỉ giữ phần chữ, không giữ thông số CSS vì chưa verify lại với Figma 2026"),

    tc("Danh sách trạng thái đối ứng", "UI-003", "Normal",
       "Bot đã thêm trạng thái — danh sách hiển thị đủ cả mặc định lẫn trạng thái đã tạo",
       TAB1 + "\n- Bot đã tạo thêm ít nhất 1 trạng thái ngoài 5 mặc định",
       "1. Quan sát danh sách trạng thái\n"
       "2. Đối chiếu với bản ghi bảng `status_chat` của đúng `bot_id` đang chọn",
       "—",
       "- Danh sách hiển thị đủ các trạng thái đã tạo, đúng thứ tự `position`\n"
       "- Số dòng hiển thị khớp số bản ghi `status_chat` của bot đang chọn",
       note="Nguồn: SC r101 (OK + staging OK) · SC r197"),

    tc("Danh sách trạng thái đối ứng", "UI-003", "Boundary",
       "Xóa hết toàn bộ trạng thái — danh sách trống nhưng vẫn thêm mới được",
       TAB1 + "\n- Đã xóa hết toàn bộ trạng thái (kể cả 5 mặc định — backend xử lý mọi trạng thái như nhau)",
       "1. Xóa lần lượt tất cả trạng thái trong danh sách (xác nhận modal mỗi lần)\n"
       "2. Quan sát vùng danh sách\n"
       "3. Bấm「＋ 新規追加」",
       "—",
       "- Danh sách hiển thị trạng thái trống, không còn dòng nào\n"
       "- Vẫn còn nút「＋ 新規追加」\n"
       "- Sau bước 3: xuất hiện dòng nhập trống với placeholder「対応ステータス（Enterで保存）」\n"
       "- Không lỗi UI, không trắng màn",
       note=MT02 + "Nguồn: v2 r31 (TC-SC-126, Pass staging + production) · SC r102 "
            "(『Khi không có data nào → hiển thị trắng』)"),

    tc("Danh sách trạng thái đối ứng", "LIST-001", "Normal",
       "Phân trang danh sách — bấm trang đầu / trang giữa / trang cuối",
       TAB1 + "\n- Số trạng thái vượt 1 trang (footer danh sách có phân trang)",
       "1. Quan sát phân trang ở footer danh sách\n"
       "2. Bấm trang đầu (1)\n"
       "3. Bấm 1 trang ở giữa (N)\n"
       "4. Bấm trang cuối",
       "—",
       "- Mỗi lần bấm: danh sách hiển thị đúng các trạng thái của trang tương ứng\n"
       "- Trang hiện tại được highlight\n"
       "- Không có trạng thái nào lặp lại giữa 2 trang",
       note="⚠️ Phụ thuộc MT-13 (số item/trang và có đổi được không chưa chốt). "
            "Nguồn: v2 r32 (TC-SC-127, Pass staging / Skipped production) · SC r188-r190"),

    tc("Danh sách trạng thái đối ứng", "LIST-001", "Boundary",
       "Kéo thả sắp xếp chỉ có hiệu lực trong trang đang xem, không kéo sang trang khác",
       TAB1 + "\n- Có > 100 trạng thái (≥ 2 trang phân trang), đang ở trang 1",
       "1. Giữ tay cầm kéo (⠿) của 1 trạng thái ở trang 1\n"
       "2. Thử kéo/thả trạng thái đó xuống vùng phân trang hoặc sang trang khác",
       "—",
       "- Chỉ sắp xếp được trong phạm vi trang hiện tại (BR-14)\n"
       "- KHÔNG di chuyển được trạng thái sang trang phân trang khác bằng kéo thả\n"
       "- Thứ tự được lưu chỉ trong phạm vi trang hiện tại",
       note="⚠️ Phụ thuộc MT-13. Nguồn: v2 r30 (TC-SC-125, Not Tested — cần > 100 status để dựng 2 trang)"),

    tc("Danh sách trạng thái đối ứng", "LIST-001", "Boundary",
       "Xóa trạng thái làm rỗng trang cuối — phân trang tự co lại, không còn trang trắng",
       TAB1 + "\n- Có đúng 11 trạng thái (trang 2 chỉ có 1 dòng), đang ở trang 2",
       "1. Xóa trạng thái duy nhất ở trang 2\n"
       "2. Quan sát vùng danh sách và phân trang",
       "11 trạng thái, trang 2 còn 1 dòng",
       "- Sau khi xóa: phân trang chỉ còn 1 trang\n"
       "- Màn hình KHÔNG đứng lại ở trang 2 trống\n"
       "- Danh sách hiển thị 10 trạng thái còn lại của trang 1",
       spec="Đã hỏi leader",
       note="Nguồn: SC r191 (『Check case Xóa status >> check phân trang』, OK + staging OK — TC gốc chỉ "
            "có tiêu đề, kết quả mong đợi do AI SUY LUẬN theo hành vi phân trang thông thường, "
            "CẦN LEADER XÁC NHẬN)"),

    tc("Danh sách trạng thái đối ứng", "UI-003", "Normal",
       "Vùng chip hiển thị trạng thái (chỉ đọc) — bấm/hover/kéo/double-click đều không đổi gì",
       TAB1 + "\n- Đang ở khối「対応ステータス」chỉ để xem, không phải khối danh sách sửa được",
       "1. Bấm vào từng chip trạng thái trong khối hiển thị\n"
       "2. Hover lên chip\n"
       "3. Thử kéo chip sang chỗ khác\n"
       "4. Double-click vào chip",
       "—",
       "- Bấm: không có phản hồi, không mở gì\n"
       "- Hover: không hiển thị tooltip hay hiệu ứng nào\n"
       "- Kéo: không di chuyển được\n"
       "- Double-click: không hiển thị gì",
       note="Nguồn: SC r172-r176 (OK + staging OK). ⚠️ Khối chip chỉ-đọc này chỉ thấy trong mô tả "
            "giao diện 2025. MT-02 chốt giao diện inline nhưng KHÔNG nói khối này còn hay đã bỏ — "
            "CẦN VERIFY LẠI trên bản đang chạy trước khi chạy TC"),
]
