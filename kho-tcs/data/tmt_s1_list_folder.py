# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 1-9: màn danh sách, folder, group template, sort/search, bulk, phân trang.

Nguồn chính: 02. TCsLine_Template
  - tab「Improve list template」(12/2023 → 05/2026, 632 dòng — tab MASTER của màn list,
    có cột kết quả Bug KH #36384)
  - tab「Task nhỏ+ check Bug Kh」(08/2023 → 06/2026, tab MASTER còn sống — Bug KH #34410 tạo
    template, SpecImprove #36385 font, Triển khai ngang #35968 sort)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Mở /basic/message-template")
F3 = ADM + "\n- Bot A đã có 3 folder template: F1「案内」, F2「予約」, F3「請求」(ngoài 未分類)"
G3 = F3 + "\n- Folder F1 đã có 3 group template: G1, G2, G3"

S1 = [
    # ═════════════ 1. Màn list template ═════════════
    tc("Màn list template", "UI-001", "Normal",
       "Mở màn danh sách template → layout 2 panel + 7 cột bảng đúng design",
       G3,
       "1. Mở /basic/message-template\n"
       "2. Quan sát panel trái (folder) và panel phải (bảng danh sách)\n"
       "3. Đối chiếu từng cột của bảng với design\n"
       "4. Thu nhỏ cửa sổ về 1366x768 rồi quan sát lại",
       "3 folder + 3 group template",
       "- Panel trái: nút「フォルダ追加」,「並べ替え」, mục「未分類 (n)」và F1/F2/F3 kèm số lượng trong ngoặc\n"
       "- Panel phải: nút「新規作成」,「並べ替え」, ô tìm kiếm「管理名を入力」\n"
       "- Bảng có đủ cột: checkbox |「管理名」|「内容」|「作成日」|「最終編集日」|「クイックテスト」|「操作」\n"
       "- Text/màu/size/bo góc/căn lề/hover/con trỏ hình tay khớp design; ở 1366x768 không vỡ layout",
       note="Nguồn: Improve list template r3-r8. Spec ui-spec.md SCR-TMT-01."),

    tc("Màn list template", "UI-003", "Normal",
       "Folder không có template → bảng hiện empty state「データがありません。」",
       F3 + "\n- Folder F3「請求」chưa có group template nào",
       "1. Mở /basic/message-template\n2. Click folder F3「請求」\n3. Quan sát vùng bảng",
       "F3 = 0 template",
       "- Bảng không có dòng dữ liệu, hiện đúng chuỗi「データがありません。」\n"
       "- Số trong ngoặc cạnh tên folder F3 hiện (0)",
       note="Nguồn: Improve list template r94. Spec ui-spec.md SCR-TMT-01 Empty state."),

    tc("Màn list template", "UI-002", "Normal",
       "Link「マニュアル」mở đúng trang hướng dẫn ở tab mới",
       ADM,
       "1. Mở /basic/message-template\n2. Quan sát nút/link「マニュアル」cạnh heading「テンプレート」\n"
       "3. Click vào「マニュアル」",
       "—",
       "- Link「マニュアル」hiện cạnh heading\n"
       "- Click → mở https://lme.jp/manual/templete/ ở TAB MỚI, tab hiện tại vẫn ở màn list",
       note="Nguồn: Improve list template r10-r11. Spec ui-spec.md SCR-TMT-01 heading."),

    tc("Màn list template", "UI-001", "Normal",
       "Font chữ ô nhập tên folder / tên template dùng Noto Sans JP + Yu Gothic, bỏ sans-serif",
       ADM + "\n- Máy test chạy Windows (SpecImprove #36385 chỉ tái hiện trên Windows)",
       "1. Mở /basic/message-template trên Windows\n"
       "2. Bấm「フォルダ追加」→ inspect ô nhập tên folder\n"
       "3. Bấm「新規作成」→ inspect ô nhập「管理名」\n"
       "4. Vào màn edit của 1 template → inspect ô tên",
       "Nhập cả text Nhật (漢字・ひらがな) và latinh",
       "- Cả 3 ô đều có `font-family: 'Noto Sans JP'`, family name resolve = Yu Gothic\n"
       "- KHÔNG còn khai báo `sans-serif` trong font-family\n"
       "- Chữ Nhật hiển thị rõ, không bị nhòe/khó đọc",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ+ check Bug Kh r697-r702 (SpecImprove #36385, 12/05/2026). "
            "RULE-08: font render phụ thuộc asset build nên xác nhận lại trên PRODUCTION. "
            "Spec KHÔNG ghi quy định font → xem MT-16."),

    tc("Màn list template", "REG-SHARED-001", "Normal",
       "Font Noto Sans JP áp cả ở ô tên folder/template của scenario · broadcast · form-answer",
       "- Đăng nhập admin bot A trên Windows\n- Các màn scenario / broadcast / form-answer đều có dữ liệu",
       "1. Vào màn scenario → mở ô nhập tên folder và tên template\n"
       "2. Làm tương tự ở màn broadcast (メッセージ配信)\n"
       "3. Làm tương tự ở màn form-answer\n"
       "4. Inspect font-family từng ô",
       "3 màn dùng chung component ô nhập tên",
       "- Cả 3 màn: `font-family: 'Noto Sans JP'`, family name = Yu Gothic, không có `sans-serif`\n"
       "- Không màn nào bị vỡ layout sau khi đổi font",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ+ check Bug Kh r703-r707. regression — component ô nhập tên là shared."),

    # ═════════════ 2. Folder template ═════════════
    tc("Folder template", "FUNC-001", "Normal",
       "Tạo folder mới với tên 1-15 ký tự → folder xuất hiện ở CUỐI danh sách",
       F3,
       "1. Mở /basic/message-template\n2. Bấm「フォルダ追加」→ inline form mở\n"
       "3. Nhập tên folder\n4. Bấm「決定」\n5. Quan sát vị trí folder mới trong panel trái",
       "Tên folder =「新規フォルダ」(6 ký tự)",
       "- Tạo folder thành công, đóng inline form\n"
       "- Folder mới nằm ở CUỐI danh sách folder (dưới F3)\n"
       "- Số lượng template của folder mới hiện (0)",
       note="Nguồn: Improve list template r14-r17. ⚠ TC gốc ghi「Nhập từ 1-15 ký tự」nhưng spec "
            "ui-spec.md:140 ghi max 20 → xem MT-01."),

    tc("Folder template", "UI-INPUT-001", "Abnormal",
       "Tên folder > 15 ký tự → chặn lưu, báo lỗi フォルダ名は15文字以内で入力してください。",
       F3,
       "1. Bấm「フォルダ追加」\n2. Nhập tên folder 16 ký tự\n3. Bấm「決定」\n"
       "4. Quan sát thông báo lỗi + panel trái",
       "「あいうえおかきくけこさしすせそた」(16 ký tự Nhật)",
       "- KHÔNG tạo được folder\n- Hiện msg lỗi chính xác:「フォルダ名は15文字以内で入力してください。」\n"
       "- Panel trái không có folder mới",
       note="Nguồn: Improve list template r26. ⚠ MÂU THUẪN với spec (max 20) → MT-01. "
            "Nếu Leader chốt theo spec thì TC này dự kiến FAIL → cần raise bug."),

    tc("Folder template", "UI-INPUT-001", "Boundary",
       "Tên folder đúng 15 ký tự → lưu thành công; đúng 16 ký tự → báo lỗi",
       F3,
       "1. Bấm「フォルダ追加」→ nhập đúng 15 ký tự → 「決定」\n"
       "2. Bấm「フォルダ追加」→ nhập đúng 16 ký tự → 「決定」",
       "15 ký tự:「あいうえおかきくけこさしすせそ」/ 16 ký tự: thêm 1 ký tự「た」",
       "- Bước 1: tạo folder thành công, hiện đủ 15 ký tự trong panel trái\n"
       "- Bước 2: chặn lưu + msg「フォルダ名は15文字以内で入力してください。」",
       note="Nguồn: suy ra biên từ Improve list template r16 + r26 — ĐÂY LÀ SUY LUẬN CỦA AI để đủ biên "
            "theo RULE-01, cần Leader xác nhận con số biên sau khi chốt MT-01."),

    tc("Folder template", "UI-INPUT-001", "Abnormal",
       "Tên folder để rỗng → báo lỗi フォルダ名を入力して下さい",
       F3,
       "1. Bấm「フォルダ追加」\n2. Không nhập gì\n3. Bấm「決定」",
       "Ô tên folder = rỗng",
       "- KHÔNG tạo được folder\n- Hiện msg lỗi chính xác:「フォルダ名を入力して下さい」",
       note="Nguồn: Improve list template r27."),

    tc("Folder template", "FUNC-UNIQ-001", "Normal",
       "Tạo folder TRÙNG tên folder đã có → vẫn tạo thành công, xuống cuối danh sách",
       F3,
       "1. Bấm「フォルダ追加」\n2. Nhập đúng tên folder F1「案内」\n3. Bấm「決定」\n"
       "4. Quan sát danh sách folder",
       "Tên =「案内」(trùng F1)",
       "- Tạo folder thành công (hệ thống KHÔNG chặn trùng tên)\n"
       "- Folder trùng tên nằm ở CUỐI danh sách, tồn tại song song với F1\n"
       "- 2 folder cùng tên có `category.id` khác nhau",
       note="Nguồn: Improve list template r17. Spec KHÔNG ghi rule trùng tên folder → xem MT-19."),

    tc("Folder template", "FUNC-001", "Normal",
       "Sau khi tạo folder lỗi → nhập lại giá trị hợp lệ thì tạo được bình thường",
       F3,
       "1. Bấm「フォルダ追加」→ để rỗng → 「決定」(báo lỗi)\n"
       "2. Nhập tên hợp lệ 5 ký tự vào chính ô đang báo lỗi\n3. Bấm「決定」",
       "Lần 1: rỗng · Lần 2:「テスト」",
       "- Lần 2 tạo folder thành công, msg lỗi biến mất\n- Folder mới hiện ở cuối danh sách",
       note="Nguồn: Improve list template r28."),

    tc("Folder template", "FUNC-001", "Normal",
       "Bấm「キャンセル」ở form tạo folder → đóng form, không tạo bản ghi",
       F3,
       "1. Bấm「フォルダ追加」\n2. Nhập tên「テスト」\n3. Bấm「キャンセル」\n4. Quan sát panel trái",
       "「テスト」",
       "- Inline form đóng lại\n- Danh sách folder không có folder mới nào",
       note="Nguồn: Improve list template r29."),

    tc("Folder template", "CONC-001", "Abnormal",
       "Double click nút「決定」khi tạo folder → chỉ tạo 1 bản ghi folder",
       F3,
       "1. Bấm「フォルダ追加」\n2. Nhập tên「二重」\n3. Double click nhanh nút「決定」\n"
       "4. Reload màn hình và đếm folder tên「二重」",
       "「二重」+ double click",
       "- Chỉ có ĐÚNG 1 folder「二重」trong panel trái sau reload\n- Không tạo folder trùng lặp",
       note="Nguồn: Improve list template r30 + r15."),

    tc("Folder template", "FUNC-001", "Normal",
       "Đổi tên folder qua menu 3 chấm →「フォルダ名変更」→ tên mới hiển thị ngay",
       G3,
       "1. Click icon 3 chấm của folder F1\n2. Chọn「フォルダ名変更」\n3. Sửa tên thành 10 ký tự\n"
       "4. Bấm「保存」\n5. Quan sát panel trái",
       "Tên mới =「案内リニューアル」",
       "- Tên folder trong panel trái đổi thành tên mới\n"
       "- Số lượng template của folder KHÔNG đổi\n- Các group template bên trong vẫn còn nguyên",
       note="Nguồn: Improve list template r62-r63."),

    tc("Folder template", "UI-INPUT-001", "Abnormal",
       "Đổi tên folder > 15 ký tự hoặc để rỗng → chặn lưu, giữ tên cũ",
       F3,
       "1. Menu 3 chấm folder F1 →「フォルダ名変更」\n2. Nhập 16 ký tự → 「保存」→ quan sát\n"
       "3. Xóa trắng ô tên → 「保存」→ quan sát",
       "16 ký tự Nhật · rỗng",
       "- Cả 2 lần đều KHÔNG đổi được tên; tên folder trong danh sách vẫn là「案内」\n"
       "- Hiện msg lỗi tương ứng (giới hạn ký tự / bắt buộc nhập)",
       note="Nguồn: Improve list template r73-r75. TC gốc không ghi nguyên văn msg lỗi → "
            "cần Leader xác nhận chuỗi msg thật khi chạy."),

    tc("Folder template", "FUNC-001", "Normal",
       "Bấm「キャンセル」khi đổi tên folder → giữ nguyên tên cũ",
       F3,
       "1. Menu 3 chấm folder F1 →「フォルダ名変更」\n2. Sửa tên thành「変更後」\n3. Bấm「キャンセル」",
       "「変更後」",
       "- Panel trái vẫn hiện tên cũ「案内」\n- Không có bản ghi `category` nào bị sửa",
       note="Nguồn: Improve list template r73."),

    tc("Folder template", "DATA-REF-001", "Normal",
       "Xóa folder RỖNG → folder mất khỏi danh sách, category ghi is_deleted = 1",
       F3 + "\n- Folder F3「請求」đang rỗng",
       "1. Menu 3 chấm folder F3 →「フォルダ削除」\n2. Bấm xác nhận xóa trên popup\n"
       "3. Quan sát panel trái\n4. Reload màn hình",
       "F3 = 0 template",
       "- Popup xác nhận đóng lại, hiện thông báo xóa thành công\n"
       "- F3 không còn trong panel trái (cả sau reload)\n"
       "- Bản ghi `category` của F3 KHÔNG bị xóa vật lý mà chỉ set `is_deleted = 1` (soft delete)",
       note="Nguồn: Improve list template r77-r78. Xác nhận 3 tầng theo RULE-07 (popup + danh sách + DB)."),

    tc("Folder template", "DATA-REF-001", "Abnormal",
       "Xóa folder CÓ template → cascade xóa group + template con, nhưng tmp_button/buttons KHÔNG xóa",
       G3 + "\n- G1 chứa 1 template con パネル・ボタン (2 panel, 3 button)\n"
            "- G2 chứa 1 template con 位置情報; G3 chứa 1 template con 画像 bật image map",
       "1. Menu 3 chấm folder F1 →「フォルダ削除」→ xác nhận\n"
       "2. Kiểm tra folder F1 và các group G1/G2/G3 trong màn list\n"
       "3. Mở lại các màn có gắn template của F1 (chat 1:1, broadcast) và tìm template đã xóa",
       "F1 chứa 3 group, mỗi group ≥1 template con đủ loại",
       "- F1 mất khỏi panel trái; `category.is_deleted = 1`\n"
       "- Toàn bộ group template G1/G2/G3 và template con bên trong KHÔNG còn ở bất kỳ màn nào "
       "(list template, modal chọn template của chat 1:1 / broadcast / scenario)\n"
       "- Dữ liệu phụ thuộc bị xóa theo: tmp_location, tmp_introduction, tmp_question, image_map, "
       "image_map_items, t_actions, t_actions_detail\n"
       "- ⚠ tmp_button và buttons KHÔNG bị xóa (giữ hành vi hiện tại) → còn dữ liệu mồ côi",
       note="Nguồn: Improve list template r80-r81. ⚠ MÂU THUẪN spec BR-05/BR-06 "
            "(spec ghi cascade xóa hết relationships) → xem MT-05."),

    tc("Folder template", "FUNC-001", "Normal",
       "Bấm hủy trên popup xóa folder → folder vẫn còn nguyên",
       F3,
       "1. Menu 3 chấm folder F2 →「フォルダ削除」\n2. Trên popup bấm hủy / dấu X\n3. Quan sát panel trái",
       "F2「予約」",
       "- Popup đóng lại\n- F2 vẫn còn trong panel trái với đủ số lượng template như trước",
       note="Nguồn: Improve list template r90-r91."),

    tc("Folder template", "CONC-001", "Abnormal",
       "Double click nút「フォルダ削除」→ chỉ xử lý xóa 1 lần, không lỗi",
       F3,
       "1. Menu 3 chấm folder F2 →「フォルダ削除」\n2. Double click nhanh nút xác nhận xóa\n3. Reload màn hình",
       "F2 + double click",
       "- Chỉ thực hiện xóa 1 lần, không hiện lỗi hệ thống\n"
       "- Sau reload F2 mất, các folder khác không bị ảnh hưởng",
       note="Nguồn: Improve list template r92."),

    tc("Folder template", "FUNC-001", "Abnormal",
       "Folder mặc định「未分類」không có menu xóa / không xóa được",
       F3,
       "1. Đưa chuột vào mục「未分類」ở panel trái\n2. Quan sát có icon 3 chấm hay không\n"
       "3. Nếu có, mở menu và quan sát các lựa chọn",
       "Folder 未分類 (category_id = 0)",
       "- Không có lựa chọn「フォルダ削除」cho「未分類」(hoặc bấm vào bị chặn, folder vẫn còn)\n"
       "- 「未分類」luôn nằm ở đầu danh sách folder",
       note="Nguồn: Improve list template r33 + spec BR-04 (`group_id = 0` không cho xóa, "
            "logic-spec.md:296)."),

    tc("Folder template", "PERF-LARGE-001", "Boundary",
       "Danh sách folder rất dài → panel trái scroll được, không mất folder nào",
       ADM + "\n- Bot A có 30 folder template",
       "1. Mở /basic/message-template\n2. Scroll panel trái từ đầu tới cuối\n3. Đếm số folder hiển thị",
       "30 folder",
       "- Panel trái xuất hiện thanh scroll dọc\n"
       "- Scroll tới cuối thấy đủ 30 folder + 未分類, không folder nào bị cắt/che",
       note="Nguồn: Improve list template r93."),

    # ═════════════ 3. Sắp xếp & ẩn folder ═════════════
    tc("Sắp xếp & ẩn folder", "LIST-001", "Normal",
       "Popup「並べ替え」folder chỉ hiện folder chưa xóa của bot, thứ tự position giảm dần",
       F3,
       "1. Bấm「並べ替え」ở panel trái\n2. Quan sát popup sắp xếp\n"
       "3. Đối chiếu danh sách trong popup với danh sách folder ngoài màn hình",
       "3 folder + 未分類",
       "- Popup mở đúng design, hiện danh sách folder kéo-thả được\n"
       "- CHỈ hiện folder của bot hiện tại và chưa bị xóa (`is_deleted = 0`)\n"
       "- Thứ tự trong popup KHỚP thứ tự ngoài màn hình: 未分類 trước, sau đó folder mới nhất lên trên "
       "(sắp theo `category.position` giảm dần)",
       note="Nguồn: Improve list template r32-r34 (TC gốc kèm câu SQL đối chiếu)."),

    tc("Sắp xếp & ẩn folder", "FUNC-001", "Normal",
       "Nút「一番上の移動」/「一番下の移動」đẩy folder về đầu / cuối và cập nhật position",
       F3,
       "1. Bấm「並べ替え」→ mở menu (...) của folder F3\n2. Bấm「一番上の移動」→ quan sát\n"
       "3. Mở menu (...) của F1 → bấm「一番下の移動」→ quan sát\n4. Bấm「保存」rồi reload màn list",
       "F3 lên đầu, F1 xuống cuối",
       "- F3 nhảy lên đầu (ngay sau 未分類), F1 xuống cuối; các folder còn lại dịch đúng 1 bậc\n"
       "- Sau「保存」+ reload, panel trái giữ đúng thứ tự mới\n"
       "- `category.position` được update khớp thứ tự mới",
       note="Nguồn: Improve list template r37-r41."),

    tc("Sắp xếp & ẩn folder", "FUNC-001", "Abnormal",
       "Folder đang ở đầu → disable「一番上の移動」; folder cuối → disable「一番下の移動」",
       F3,
       "1. Bấm「並べ替え」\n2. Mở menu (...) của folder ĐẦU danh sách → quan sát「一番上の移動」\n"
       "3. Mở menu (...) của folder CUỐI danh sách → quan sát「一番下の移動」",
       "Folder đầu và folder cuối",
       "- Folder đầu:「一番上の移動」ở trạng thái disable (không bấm được)\n"
       "- Folder cuối:「一番下の移動」ở trạng thái disable\n- Nút còn lại của mỗi folder vẫn enable",
       note="Nguồn: Improve list template r38 + r40."),

    tc("Sắp xếp & ẩn folder", "FUNC-001", "Normal",
       "Kéo-thả 1 folder / nhiều folder → vị trí và position đổi đúng, giữ sau reload",
       F3,
       "1. Bấm「並べ替え」\n2. Kéo F1 xuống dưới F3 → thả\n3. Kéo folder cuối lên vị trí đầu → thả\n"
       "4. Kéo tiếp 2 folder khác nhau\n5. Bấm「保存」→ reload màn list",
       "3 lượt kéo-thả liên tiếp",
       "- Mỗi lượt kéo-thả, folder về đúng vị trí đã thả; các folder khác dịch đúng bậc\n"
       "- Sau「保存」+ reload, thứ tự ngoài màn list khớp thứ tự đã kéo\n"
       "- `category.position` update đúng cho mọi folder bị dịch",
       note="Nguồn: Improve list template r42-r44."),

    tc("Sắp xếp & ẩn folder", "STATE-001", "Abnormal",
       "Kéo-thả xong nhưng KHÔNG bấm「保存」→ thứ tự folder giữ nguyên như trước",
       F3,
       "1. Bấm「並べ替え」\n2. Kéo F1 xuống cuối\n3. Đóng popup bằng dấu X (không bấm「保存」)\n"
       "4. Quan sát panel trái\n5. Mở lại popup「並べ替え」",
       "Kéo F1 xuống cuối, không lưu",
       "- Panel trái giữ nguyên thứ tự cũ (F1 vẫn ở vị trí ban đầu)\n"
       "- Popup mở lại hiện đúng thứ tự CŨ (state được reset)",
       note="Nguồn: Improve list template r45-r47. ⚠ Khối group template cùng thao tác này có note "
            "「popup không reset」→ cần kiểm lại ở folder, xem MT-20."),

    tc("Sắp xếp & ẩn folder", "REG-SHARED-001", "Normal",
       "Sau khi đổi thứ tự folder → các màn khác dùng folder template cũng hiện thứ tự mới",
       G3,
       "1. Đổi thứ tự folder ở màn template và「保存」\n"
       "2. Mở chat 1:1 → modal「テンプレート送信」→ quan sát menu folder\n"
       "3. Lặp lại ở: modal action, broadcast (メッセージ配信), button trong template, scenario, remind, "
       "màn 予約設定 của calendar, màn アクション設定 của 単品商品",
       "Thứ tự mới: F3 → F2 → F1; 8 điểm dùng chung folder template",
       "- Mọi màn ở bước 2-3 đều hiện folder template theo ĐÚNG thứ tự mới\n"
       "- Không màn nào còn dùng thứ tự cũ (kể cả sau khi reload từng màn)",
       note="Nguồn: Improve list template r48-r57 (ma trận 8 màn). Gộp 1 TC vì mọi màn CÙNG 1 kết quả "
            "mong đợi; danh sách màn liệt kê đủ ở cột Các bước."),

    tc("Sắp xếp & ẩn folder", "STATE-001", "Normal",
       "Ẩn folder (フォルダを非表示) → reload / vào lại màn thì panel folder MẶC ĐỊNH vẫn hiện",
       F3,
       "1. Bấm icon ẩn folder ở panel trái\n2. Reload màn /basic/message-template → quan sát\n"
       "3. Vào lại màn template từ menu chính → quan sát\n4. Bấm icon mở lại panel folder",
       "—",
       "- Sau khi ẩn: panel folder thu lại, bảng danh sách chiếm hết chiều rộng\n"
       "- Sau reload VÀ sau khi vào lại từ menu: panel folder HIỆN lại như mặc định "
       "(trạng thái ẩn không được lưu)\n"
       "- Bấm icon mở lại → panel folder hiện lại bình thường",
       note="Nguồn: Improve list template r58-r61 (đã confirm với anh Tư: mặc định vẫn hiển thị folder)."),

    # ═════════════ 4. Màn list group template ═════════════
    tc("Màn list group template", "UI-001", "Normal",
       "Bảng group template hiển thị đúng 管理名 / 作成日 / 最終編集日, ngày sửa cập nhật sau khi edit",
       G3,
       "1. Click folder F1\n2. Quan sát từng dòng của bảng bên phải\n"
       "3. Đối chiếu 管理名, 作成日, 最終編集日 với dữ liệu đã tạo\n"
       "4. Vào edit G2, sửa tên, lưu, quay lại list",
       "3 group template G1/G2/G3",
       "- Mỗi dòng hiện đúng 管理名 của group\n- 作成日 / 最終編集日 format YYYY.MM.DD\n"
       "- Sau khi sửa G2: 最終編集日 của G2 = ngày hôm nay, 作成日 KHÔNG đổi",
       note="Nguồn: Improve list template r94-r95, r354. Spec feature-spec.md Field Matrix #3-#4."),

    tc("Màn list group template", "UI-001", "Normal",
       "Cột「内容」hiện preview đúng theo từng loại template con",
       F3 + "\n- Folder F1 có 5 group, mỗi group chứa 1 template con của 1 loại: "
             "text / パネル・ボタン / スタンプ / 画像・動画・音声 / 位置情報",
       "1. Click folder F1\n2. Quan sát cột「内容」của từng dòng\n"
       "3. So sánh với nội dung thật của template con",
       "5 group ứng 5 loại template",
       "- Dòng template text: hiện đoạn đầu nội dung text (rút gọn)\n"
       "- Các loại còn lại: hiện thumbnail/icon đặc trưng theo type (button, stamp, media, location)\n"
       "- Không dòng nào để trống cột「内容」khi template con đã có dữ liệu",
       note="Nguồn: Improve list template r349-r353. Spec ui-spec.md xếp「内容」vào mục điểm chưa rõ #2 "
            "→ TC này lấp Gap, xem MT-13."),

    # ═════════════ 5. Tạo group template ═════════════
    tc("Tạo group template", "FUNC-001", "Normal",
       "Tạo group template thành công → redirect sang màn list template con, group nằm CUỐI folder",
       F3,
       "1. Click folder F1\n2. Bấm「新規作成」→ modal mở\n3. Nhập「管理名」\n"
       "4. Giữ nguyên folder mặc định (F1)\n5. Bấm「テンプレートを作成」\n6. Quan sát màn hình kế tiếp",
       "管理名 =「お知らせ配信」",
       "- Redirect sang màn danh sách TEMPLATE CON (テンプレート作成) của group vừa tạo, KHÔNG phải màn editor\n"
       "- Quay lại màn list: folder F1 có thêm 1 dòng, group mới ở CUỐI danh sách, số lượng F1 tăng 1",
       note="Nguồn: Improve list template r111-r112. ⚠ MÂU THUẪN spec feature-spec.md:262 "
            "(ghi redirect đến trang editor SCR-TMT-04~10) → xem MT-06."),

    tc("Tạo group template", "FUNC-001", "Normal",
       "Chọn folder khác trong dropdown khi tạo → group mới vào đúng folder đã chọn",
       F3,
       "1. Đang ở folder F1, bấm「新規作成」\n2. Nhập「管理名」\n3. Mở dropdown「フォルダ」→ chọn F2\n"
       "4. Bấm「テンプレートを作成」\n5. Quay lại màn list, kiểm tra F1 và F2",
       "管理名 =「予約案内」, folder = F2「予約」",
       "- Group mới nằm trong F2 (ở cuối), KHÔNG nằm trong F1\n- Số lượng F2 tăng 1, F1 không đổi",
       note="Nguồn: Improve list template r109, r111."),

    tc("Tạo group template", "UI-INPUT-001", "Abnormal",
       "管理名 bỏ trống → báo lỗi 管理名を入力してください。",
       F3,
       "1. Bấm「新規作成」\n2. Để trống ô「管理名」\n3. Bấm「テンプレートを作成」",
       "管理名 = rỗng",
       "- KHÔNG tạo được group template\n- Hiện msg lỗi chính xác:「管理名を入力してください。」\n- Modal vẫn mở",
       note="Nguồn: Task nhỏ+ check Bug Kh r489 (Regression test của Bug KH #34410)."),

    tc("Tạo group template", "UI-INPUT-001", "Boundary",
       "管理名 20 ký tự → lưu OK; 21 ký tự → báo lỗi 管理名は20文字以内で入力してください。",
       F3,
       "1. Bấm「新規作成」→ nhập đúng 20 ký tự → 「テンプレートを作成」→ quan sát\n"
       "2. Bấm「新規作成」→ nhập đúng 21 ký tự → 「テンプレートを作成」→ quan sát",
       "20 ký tự:「あいうえおかきくけこさしすせそたちつてと」/ 21 ký tự: thêm「な」",
       "- 20 ký tự: tạo group thành công, tên trong list hiện đủ 20 ký tự\n"
       "- 21 ký tự: chặn lưu + msg「管理名は20文字以内で入力してください。」",
       note="Nguồn: Task nhỏ+ check Bug Kh r487, r490. Khớp spec ui-spec.md:161 (max 20)."),

    tc("Tạo group template", "UI-INPUT-001", "Abnormal",
       "管理名 chỉ gồm khoảng trắng → bị chặn (cảnh báo bắt buộc nhập)",
       F3,
       "1. Bấm「新規作成」\n2. Nhập 5 dấu space vào ô「管理名」\n3. Bấm「テンプレートを作成」",
       "「     」(5 space)",
       "- KHÔNG tạo được group template, hiện cảnh báo bắt buộc nhập\n"
       "- Không có group nào tên rỗng trong danh sách",
       note="Nguồn: Improve list template r101. ⚠ Corpus KHÔNG kết luận hệ thống có tự trim space "
            "đầu/cuối hay không (r103 chỉ có tiêu đề) → xem MT-21."),

    tc("Tạo group template", "UI-INPUT-001", "Normal",
       "Paste tên quản lý bằng Ctrl+V / chuột phải / paste nhiều lần → tạo group thành công",
       F3 + "\n- Clipboard chứa chuỗi「貼り付けテスト」\n- Chạy trên cả máy Windows và macOS",
       "1. Bấm「新規作成」→ paste vào「管理名」bằng Ctrl+V (Cmd+V trên Mac) → 「テンプレートを作成」\n"
       "2. Lặp lại nhưng paste bằng chuột phải → Paste (Mac: File → Edit → Paste)\n"
       "3. Lặp lại: ô đang có data, Ctrl+A rồi paste đè\n4. Lặp lại: paste 2 lần liên tiếp rồi tạo",
       "clipboard =「貼り付けテスト」; 4 cách paste; 2 hệ điều hành",
       "- Cả 4 cách paste đều nhập được text vào ô「管理名」\n"
       "- Mỗi lần bấm「テンプレートを作成」đều tạo group thành công và redirect sang màn list template con\n"
       "- Kết quả giống nhau trên Windows và macOS",
       note="Nguồn: Task nhỏ+ check Bug Kh r481-r486 (tái hiện Bug KH #34410). "
            "Gộp vì mọi cách paste CÙNG 1 kết quả mong đợi."),

    tc("Tạo group template", "UI-INPUT-001", "Abnormal",
       "Ô 管理名 đang có data + clipboard RỖNG rồi paste → vẫn tạo được group với data cũ",
       F3 + "\n- Clipboard đã được xóa trắng",
       "1. Bấm「新規作成」→ nhập「テスト」vào「管理名」\n2. Đặt con trỏ vào ô, paste khi clipboard rỗng\n"
       "3. Bấm「テンプレートを作成」",
       "ô có「テスト」, clipboard rỗng",
       "- Nội dung ô không bị xóa/đổi thành rỗng, vẫn là「テスト」\n- Tạo group thành công với tên「テスト」",
       note="Nguồn: Task nhỏ+ check Bug Kh r484 — chính là nhánh gây Bug KH #34410."),

    tc("Tạo group template", "CONC-001", "Abnormal",
       "Double click nút「テンプレートを作成」→ chỉ tạo 1 group template",
       F3,
       "1. Bấm「新規作成」→ nhập「二重作成」\n2. Double click nhanh「テンプレートを作成」\n"
       "3. Quay lại màn list, đếm số group tên「二重作成」",
       "「二重作成」+ double click",
       "- Chỉ có ĐÚNG 1 group「二重作成」\n- Không tạo bản ghi duplicate trong bảng `template`",
       note="Nguồn: Task nhỏ+ check Bug Kh r488 + Improve list template r110."),

    tc("Tạo group template", "UI-001", "Normal",
       "Dropdown「フォルダ」ở modal tạo: mặc định = folder đang chọn, hiện đủ folder, có scroll",
       ADM + "\n- Bot A có 25 folder template, đang đứng ở folder F2",
       "1. Bấm「新規作成」\n2. Quan sát giá trị mặc định của ô「フォルダ」\n"
       "3. Click vào ô folder (bất kỳ vị trí nào trong ô) → quan sát dropdown\n"
       "4. Scroll trong dropdown tới cuối\n5. Chọn 1 folder khác",
       "25 folder, đang ở F2",
       "- Mặc định ô「フォルダ」hiện tên folder đang chọn trước đó (F2)\n"
       "- Click bất kỳ vị trí trong ô đều mở dropdown\n"
       "- Dropdown hiện đủ 25 folder + 未分類 theo đúng thứ tự panel trái, có thanh scroll\n"
       "- Chọn folder khác → ô ghi nhận đúng folder vừa chọn",
       note="Nguồn: Improve list template r104-r109."),

    tc("Tạo group template", "STATE-CLEAN-001", "Normal",
       "Đóng modal tạo group bằng (X) → dữ liệu đã nhập được reset khi mở lại",
       F3,
       "1. Bấm「新規作成」→ nhập「テスト」, chọn folder F3\n2. Bấm (X) đóng modal\n"
       "3. Bấm「新規作成」lần nữa → quan sát 2 ô",
       "「テスト」+ folder F3",
       "- Modal mở lại có ô「管理名」rỗng\n"
       "- Ô「フォルダ」trở về folder đang chọn ngoài màn list, không giữ F3",
       note="Nguồn: Improve list template r121-r122."),

    tc("Tạo group template", "REG-SHARED-001", "Normal",
       "Group template mới tạo hiển thị được ở toàn bộ màn có chọn template",
       G3 + "\n- Vừa tạo group「新規案内」có 1 template con dạng text",
       "1. Mở chat 1:1 → modal「テンプレート送信」→ tìm group「新規案内」\n"
       "2. Lặp lại ở: modal action, broadcast, button trong template, scenario, remind, "
       "calendar 予約設定, 単品商品 アクション設定",
       "group「新規案内」+ 8 điểm gắn template",
       "- Mọi điểm ở bước 1-2 đều thấy group「新規案内」trong danh sách chọn template\n"
       "- Chọn được và gửi được nội dung template con của group đó tới LINE user",
       note="Nguồn: Improve list template r113-r132. Gộp vì mọi điểm CÙNG 1 kết quả mong đợi."),

    # ═════════════ 6. Sửa & xóa group template ═════════════
    tc("Sửa & xóa group template", "FUNC-001", "Normal",
       "Sửa 管理名 / folder của group → cập nhật đúng, hiện thông báo 変更内容が保存されました",
       G3,
       "1. Ở dòng G1 bấm「編集」\n2. Quan sát giá trị mặc định 2 ô\n3. Sửa「管理名」thành tên mới\n"
       "4. Đổi「フォルダ」sang F2\n5. Bấm lưu\n6. Kiểm tra F1 và F2",
       "管理名 mới =「案内改」, folder: F1 → F2",
       "- 2 ô mặc định hiện đúng 管理名 và folder hiện tại của G1\n"
       "- Hiện thông báo「変更内容が保存されました」\n"
       "- F1 giảm 1 group và không còn G1; F2 tăng 1 group và có G1 với tên mới",
       note="Nguồn: Improve list template r232-r237, r358-r361."),

    tc("Sửa & xóa group template", "UI-INPUT-001", "Abnormal",
       "Sửa group: bỏ trống 管理名 hoặc bỏ trống フォルダ → chặn lưu, highlight ô lỗi",
       G3,
       "1. Bấm「編集」ở G1\n2. Xóa trắng「管理名」→ bấm lưu → quan sát\n"
       "3. Nhập lại tên, bỏ chọn「フォルダ」(nếu cho phép) → bấm lưu → quan sát",
       "管理名 rỗng · フォルダ rỗng",
       "- Cả 2 trường hợp KHÔNG lưu được\n- Ô「管理名」được highlight và hiện cảnh báo bắt buộc nhập\n"
       "- Dữ liệu G1 ngoài màn list không đổi",
       note="Nguồn: Improve list template r238-r239, r248."),

    tc("Sửa & xóa group template", "CONC-001", "Abnormal",
       "Double click nút lưu ở màn sửa group → chỉ ghi 1 lần, không tạo bản ghi mới",
       G3,
       "1. Bấm「編集」ở G1 → sửa tên thành「案内2」\n2. Double click nút lưu\n3. Quay lại màn list",
       "「案内2」+ double click",
       "- Chỉ có 1 group tên「案内2」, số lượng group của folder không tăng\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r248."),

    tc("Sửa & xóa group template", "STATE-001", "Normal",
       "Bấm「戻る」ở màn sửa group → không lưu thay đổi, dữ liệu reset",
       G3,
       "1. Bấm「編集」ở G1 → sửa 管理名 và đổi folder\n2. Bấm「戻る」\n"
       "3. Quan sát màn list\n4. Vào lại「編集」của G1",
       "Sửa tên + đổi folder rồi back",
       "- Màn list vẫn hiện G1 với tên và folder CŨ\n- Vào lại màn sửa, 2 ô hiện giá trị cũ (đã reset)",
       note="Nguồn: Improve list template r250, r491."),

    tc("Sửa & xóa group template", "FUNC-001", "Normal",
       "Sao chép group template → bản sao có đủ template con như bản gốc",
       G3 + "\n- G1 chứa 3 template con: text, パネル・ボタン, 画像",
       "1. Ở dòng G1 chọn thao tác sao chép\n2. Quan sát danh sách group của folder F1\n"
       "3. Mở group vừa copy → đối chiếu danh sách template con với G1",
       "G1 có 3 template con",
       "- Folder F1 có thêm 1 group mới, số lượng tăng 1\n"
       "- Group copy có đủ 3 template con giống bản gốc (đúng loại, đúng nội dung, đúng thứ tự)\n"
       "- Sửa group copy KHÔNG làm đổi G1 gốc",
       note="Nguồn: Improve list template r305-r312. Spec BR-07 deep clone recursive."),

    tc("Sửa & xóa group template", "FUNC-001", "Normal",
       "Sửa bản copy (tên / folder / thêm-bớt template con) → không ảnh hưởng group gốc",
       G3 + "\n- Đã copy G1 thành G1'",
       "1. Vào G1' đổi 管理名 và folder\n2. Thêm 1 template con dạng スタンプ vào G1'\n"
       "3. Xóa 1 template con của G1'\n4. Mở lại G1 gốc và đối chiếu",
       "G1' đổi tên/folder, +1 và -1 template con",
       "- G1' có tên/folder mới, số template con tăng rồi giảm đúng như thao tác\n"
       "- G1 gốc giữ nguyên 管理名, folder và đủ 3 template con ban đầu",
       note="Nguồn: Improve list template r306-r310."),

    tc("Sửa & xóa group template", "DATA-REF-001", "Normal",
       "Xóa 1 group template → mất khỏi danh sách và khỏi mọi màn đang gắn template đó",
       G3 + "\n- G2 đã được gắn vào 1 broadcast draft và 1 step của scenario",
       "1. Ở dòng G2 chọn xóa → popup xác nhận → xác nhận xóa\n2. Quan sát danh sách group của F1\n"
       "3. Mở modal chọn template ở chat 1:1 / broadcast / scenario / remind và tìm G2\n"
       "4. Chạy broadcast/scenario đã gắn G2 và quan sát tin nhắn phía LINE user",
       "G2 + 4 điểm đang gắn",
       "- Popup xác nhận hiện đúng, xác nhận → xóa thành công\n"
       "- G2 không còn trong danh sách group của F1, số lượng folder giảm 1\n"
       "- Không màn nào ở bước 3 còn thấy G2\n"
       "- Tin nhắn gửi đi ở bước 4 KHÔNG còn nội dung của G2, các message khác vẫn gửi bình thường",
       note="Nguồn: Improve list template r320-r329. Spec BR-06 hard delete + BR-15 propagate "
            "`template_mapping_tables`. RULE-06: đi tới output cuối là tin nhắn trên LINE."),

    tc("Sửa & xóa group template", "FUNC-001", "Normal",
       "Bấm Cancel trên popup xóa group → group vẫn còn nguyên",
       G3,
       "1. Ở dòng G2 chọn xóa\n2. Trên popup bấm Cancel\n3. Quan sát danh sách",
       "G2",
       "- Popup đóng\n- G2 vẫn còn trong danh sách với đủ template con",
       note="Nguồn: Improve list template r321-r322."),

    # ═════════════ 7. Sort & search template ═════════════
    tc("Sort & search template", "LIST-001", "Normal",
       "Popup「並べ替え」group template hiển thị đúng list và thứ tự position giảm dần",
       G3,
       "1. Click folder F1\n2. Bấm「並べ替え」ở panel phải\n3. Đối chiếu list trong popup với bảng ngoài",
       "3 group template",
       "- Popup mở đúng design, list group kéo-thả được\n"
       "- Thứ tự trong popup KHỚP bảng ngoài, sắp theo `template.position` giảm dần "
       "(query lọc bot_id + category_id + `in_park = 0`)",
       note="Nguồn: Improve list template r133-r135 (TC gốc kèm SQL đối chiếu)."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Move đầu/cuối và kéo-thả group template → thứ tự + position đổi đúng, giữ sau reload",
       G3,
       "1. Bấm「並べ替え」→ menu (...) của G3 →「一番上の移動」\n"
       "2. Menu (...) của G1 →「一番下の移動」\n3. Kéo-thả G2 xuống cuối\n"
       "4. Bấm「保存」→ reload màn list",
       "3 thao tác đổi vị trí liên tiếp",
       "- Mỗi thao tác đưa group về đúng vị trí, các group khác dịch đúng bậc\n"
       "- Sau「保存」+ reload, bảng ngoài giữ đúng thứ tự mới\n"
       "- `position` của các group được update khớp thứ tự",
       note="Nguồn: Improve list template r137-r149."),

    tc("Sort & search template", "FUNC-001", "Abnormal",
       "Group ở đầu / cuối danh sách → nút move tương ứng bị disable",
       G3,
       "1. Bấm「並べ替え」\n2. Mở menu (...) group ĐẦU → quan sát「一番上の移動」\n"
       "3. Mở menu (...) group CUỐI → quan sát「一番下の移動」",
       "Group đầu và group cuối",
       "- Group đầu: nút「一番上の移動」disable\n- Group cuối: nút「一番下の移動」disable",
       note="Nguồn: Improve list template r139, r141."),

    tc("Sort & search template", "STATE-001", "Abnormal",
       "Kéo-thả group xong đóng popup không lưu → thứ tự ngoài màn list giữ nguyên",
       G3,
       "1. Bấm「並べ替え」\n2. Kéo G1 xuống cuối\n3. Đóng popup (X) không bấm「保存」\n"
       "4. Quan sát bảng ngoài\n5. Mở lại popup",
       "Kéo G1 xuống cuối, không lưu",
       "- Bảng ngoài giữ thứ tự cũ\n- Popup mở lại hiện đúng thứ tự CŨ (đã reset)",
       note="Nguồn: Improve list template r146 — ⚠ TC gốc có note「popup không reset」và r456 note "
            "「thay đổi trong popup chưa lưu >> ngoài màn list đã thay đổi」(bug đã phát hiện). "
            "Expected ở đây viết theo hành vi ĐÚNG → xem MT-20, dự kiến FAIL nếu chưa fix."),

    tc("Sort & search template", "LIST-001", "Normal",
       "Sort theo 作成日 tăng / giảm dần → thứ tự đúng, reload trở về mặc định",
       G3 + "\n- 3 group được tạo cách nhau rõ về thời gian",
       "1. Click mũi tên sort của cột「作成日」(tăng dần) → quan sát\n2. Click tiếp (giảm dần) → quan sát\n"
       "3. Reload màn hình → quan sát thứ tự\n4. Kiểm tra search / copy / xóa trên màn sau khi sort",
       "3 group khác 作成日",
       "- Tăng dần: group tạo sớm nhất ở trên (ORDER BY created_at ASC)\n"
       "- Giảm dần: group tạo muộn nhất ở trên\n"
       "- Reload → trở về thứ tự MẶC ĐỊNH theo position giảm dần (sort không được lưu)\n"
       "- Thứ tự sort KHÔNG ảnh hưởng các màn khác; các chức năng khác vẫn hoạt động",
       note="Nguồn: Improve list template r160-r168."),

    tc("Sort & search template", "LIST-001", "Normal",
       "Sort theo 管理名 tăng / giảm dần → thứ tự alphabet đúng, reload trở về mặc định",
       G3,
       "1. Click mũi tên sort cột「管理名」(tăng dần) → quan sát\n2. Click tiếp (giảm dần) → quan sát\n"
       "3. Chuyển sang trang khác rồi quay lại → quan sát\n4. Reload màn hình",
       "管理名: 「あ案内」/「か予約」/「さ請求」",
       "- Tăng dần: sắp theo 管理名 A→Z (kana あ→さ)\n- Giảm dần: ngược lại\n"
       "- Chuyển trang rồi quay lại: dữ liệu khớp vị trí trang\n- Reload → về thứ tự mặc định",
       note="Nguồn: Improve list template r164-r168, r171-r174."),

    tc("Sort & search template", "LIST-001", "Normal",
       "Sort ở folder mặc định 未分類 hoạt động giống folder thường",
       ADM + "\n- Folder 未分類 có 3 group template khác nhau về 作成日 và 管理名",
       "1. Click folder「未分類」\n2. Sort theo 作成日 tăng/giảm\n3. Sort theo 管理名 tăng/giảm\n4. Reload",
       "3 group trong 未分類",
       "- Sort chạy đúng cả 4 chiều như folder thường\n- Reload → về thứ tự mặc định",
       note="Nguồn: Improve list template r169-r175. Folder 未分類 (category_id = 0) có nhánh code "
            "RIÊNG nên phải test lại đầy đủ — xem MT-18."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Search theo 管理名 → tìm được trên TOÀN BỘ folder, không chỉ folder đang chọn",
       G3 + "\n- Folder F2 có group「予約テンプレ」; đang đứng ở folder F1",
       "1. Đang ở folder F1, nhập「予約」vào ô「管理名を入力」\n2. Bấm Enter\n"
       "3. Quan sát kết quả + panel folder\n4. Lặp lại với keyword khớp TOÀN PHẦN tên group",
       "keyword =「予約」và「予約テンプレ」, group đích nằm ở F2 (khác folder đang chọn)",
       "- Kết quả trả về CÓ group「予約テンプレ」của folder F2 (search all folder)\n"
       "- Khi hiện kết quả, menu folder được đóng lại\n- Cả search 1 phần và toàn phần đều ra kết quả",
       note="Nguồn: Task nhỏ+ check Bug Kh r3-r9 + Improve list template r179, r188. "
            "⚠ MÂU THUẪN spec logic-spec.md:141 `searchByKeyWord($group_id, $keyword)` — spec ghi "
            "search TRONG folder → xem MT-02."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Click vào kết quả search (template cha) → mở đúng list template con của group đó",
       G3 + "\n- Group「予約テンプレ」ở folder F2 có 2 template con",
       "1. Search「予約」ở folder F1\n2. Click vào dòng kết quả「予約テンプレ」\n3. Quan sát màn hình",
       "kết quả search thuộc folder khác",
       "- Mở màn danh sách template CON của đúng group「予約テンプレ」\n"
       "- Danh sách hiện đủ 2 template con đúng thứ tự",
       note="Nguồn: Task nhỏ+ check Bug Kh r6, r9."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Search không phân biệt hoa/thường và khớp 1 phần → vẫn ra kết quả",
       G3 + "\n- Có group tên「Welcome Message」",
       "1. Search「welcome message」(toàn chữ thường) → quan sát\n2. Search「Welcome」(1 phần) → quan sát\n"
       "3. Search「WELCOME MESSAGE」→ quan sát",
       "3 biến thể hoa/thường/1 phần của「Welcome Message」",
       "- Cả 3 lần đều trả về group「Welcome Message」",
       note="Nguồn: Improve list template r180-r181."),

    tc("Sort & search template", "FUNC-001", "Abnormal",
       "Search tên không tồn tại → hiện empty state, không lỗi",
       G3,
       "1. Nhập「存在しない名前ABC」vào ô search\n2. Bấm Enter",
       "keyword không khớp bất kỳ group nào",
       "- Bảng không có dòng nào, hiện「データがありません。」\n- Không hiện lỗi hệ thống",
       note="Nguồn: Improve list template r187."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Ô search để rỗng rồi Enter → trả về toàn bộ group template của folder đang chọn",
       G3,
       "1. Search「予約」→ có kết quả\n2. Xóa trắng ô search → bấm Enter\n3. Quan sát bảng",
       "keyword rỗng",
       "- Bảng hiện lại TOÀN BỘ group template của folder đang chọn (F1: 3 group)\n"
       "- Panel folder trở lại trạng thái bình thường",
       note="Nguồn: Improve list template r186, r195."),

    tc("Sort & search template", "PERF-LARGE-001", "Normal",
       "Search ra nhiều kết quả → phân trang và các chức năng trong màn vẫn hoạt động",
       ADM + "\n- Bot A có 60 group template mà 管理名 đều chứa「案内」",
       "1. Search「案内」\n2. Quan sát phân trang\n3. Chuyển sang trang 2, trang 3\n"
       "4. Trên trang 2 thử sort theo 管理名, copy 1 group, mở preview",
       "60 kết quả, 20 dòng/trang",
       "- Kết quả chia trang đúng (3 trang), mỗi trang tối đa 20 dòng\n"
       "- Chuyển trang hiện đúng phần dữ liệu tương ứng\n"
       "- Sort / copy / preview trên trang kết quả vẫn hoạt động đúng",
       note="Nguồn: Improve list template r184-r185."),

    tc("Sort & search template", "FUNC-001", "Normal",
       "Kết hợp search rồi sort → thứ tự kết quả search được sắp lại đúng",
       ADM + "\n- Có 5 group 管理名 chứa「案内」, khác nhau 作成日 và 管理名",
       "1. Search「案内」\n2. Sort kết quả theo 作成日 tăng dần → quan sát\n"
       "3. Sort kết quả theo 管理名 giảm dần → quan sát",
       "5 kết quả search",
       "- Sau mỗi lần sort, danh sách vẫn CHỈ gồm 5 group khớp keyword\n"
       "- Thứ tự đúng theo tiêu chí sort đã chọn",
       note="Nguồn: Improve list template r197-r198."),

    # ═════════════ 8. Chuyển folder & xóa hàng loạt ═════════════
    tc("Chuyển folder & xóa hàng loạt", "BULK-001", "Normal",
       "Nút「一括フォルダ変更」disable khi chưa tick, enable khi đã tick group",
       G3,
       "1. Click folder F1, không tick checkbox nào → quan sát nút「一括フォルダ変更」\n"
       "2. Tick 1 group → quan sát nút\n3. Bỏ tick → quan sát nút",
       "0 / 1 / 0 group được tick",
       "- Chưa tick: nút「一括フォルダ変更」disable\n- Tick ≥1: nút enable\n"
       "- Bỏ tick hết: nút trở lại disable",
       note="Nguồn: Improve list template r199-r200, r208."),

    tc("Chuyển folder & xóa hàng loạt", "BULK-001", "Normal",
       "Chuyển hàng loạt group giữa các folder (4 chiều) → group sang folder đích, số đếm 2 folder đổi đúng",
       G3 + "\n- F2 đang có 1 group; 未分類 có 1 group",
       "1. Ở F1 tick G1 và G2 → bấm「一括フォルダ変更」→ chọn F2 → xác nhận\n"
       "2. Kiểm tra danh sách và số đếm của F1, F2\n"
       "3. Lặp lại: chuyển 1 group từ 未分類 sang F3\n4. Từ F3 về 未分類\n5. Từ F2 sang F3",
       "4 chiều chuyển: F1→F2, 未分類→F3, F3→未分類, F2→F3",
       "- Các group được tick chuyển sang folder đích và KHÔNG còn ở folder cũ\n"
       "- Số trong ngoặc: folder đích tăng đúng số group đã chuyển, folder cũ giảm đúng số đó\n"
       "- Sau khi thành công, nút「一括フォルダ変更」trở lại disable",
       note="Nguồn: Improve list template r204-r208. Gộp 4 chiều vì CÙNG 1 kết quả mong đợi."),

    tc("Chuyển folder & xóa hàng loạt", "BULK-001", "Normal",
       "Tick chọn TẤT CẢ group của trang rồi chuyển folder → chuyển hết, không sót",
       ADM + "\n- Folder F1 có 20 group (đủ 1 trang)",
       "1. Tick checkbox ở header để chọn cả trang\n2. Bấm「一括フォルダ変更」→ chọn F2 → xác nhận\n"
       "3. Kiểm tra F1 và F2",
       "20 group / 1 trang",
       "- Cả 20 group chuyển sang F2\n- F1 hiện (0) và empty state; F2 tăng đúng 20",
       note="Nguồn: Improve list template r205."),

    tc("Chuyển folder & xóa hàng loạt", "UI-001", "Normal",
       "Popup「一括フォルダ変更」mặc định hiện 未分類, list folder đủ và có scroll khi dài",
       ADM + "\n- Bot A có 25 folder; folder F1 có ≥1 group",
       "1. Tick 1 group ở F1 → bấm「一括フォルダ変更」\n2. Quan sát giá trị mặc định trong popup\n"
       "3. Mở list folder trong popup, scroll tới cuối",
       "25 folder",
       "- Popup mặc định chọn folder「未分類」\n"
       "- List hiện đủ 25 folder + 未分類 theo đúng thứ tự panel trái, có scroll",
       note="Nguồn: Improve list template r202-r203."),

    tc("Chuyển folder & xóa hàng loạt", "CONC-001", "Abnormal",
       "Double click「一括フォルダ変更」→ chỉ xử lý 1 lần",
       G3,
       "1. Tick G1 → double click nhanh nút「一括フォルダ変更」\n2. Xác nhận chuyển folder\n"
       "3. Kiểm tra số đếm folder nguồn và đích",
       "double click",
       "- Chỉ mở 1 popup, chỉ thực hiện chuyển folder 1 lần\n- Số đếm folder không bị trừ/cộng 2 lần",
       note="Nguồn: Improve list template r201."),

    tc("Chuyển folder & xóa hàng loạt", "REG-SHARED-001", "Normal",
       "Sau khi chuyển folder hàng loạt → các màn khác hiện template ở folder mới",
       G3,
       "1. Chuyển G1 từ F1 sang F2\n2. Mở modal chọn template ở chat 1:1 / modal action / broadcast / "
       "button / scenario / remind / calendar / 単品商品\n3. Tìm G1 trong cây folder của từng màn",
       "G1 chuyển F1 → F2, 8 điểm chọn template",
       "- Mọi màn đều thấy G1 nằm dưới folder F2, không còn dưới F1\n- Gửi được nội dung G1 từ folder mới",
       note="Nguồn: Improve list template r209-r216. Gộp vì CÙNG 1 kết quả mong đợi."),

    tc("Chuyển folder & xóa hàng loạt", "BULK-001", "Normal",
       "Xóa hàng loạt group template → nút enable/disable đúng, popup xác nhận, xóa hết mục đã tick",
       G3,
       "1. Không tick gì → quan sát nút「一括削除」\n2. Tick G1 + G2 → quan sát nút\n"
       "3. Bấm「一括削除」→ quan sát popup\n4. Xác nhận xóa\n5. Kiểm tra danh sách và số đếm F1",
       "0 rồi 2 group được tick",
       "- Chưa tick: nút「一括削除」disable; tick ≥1: enable\n- Popup xác nhận hiện đúng nội dung\n"
       "- Sau xác nhận: G1 và G2 mất khỏi danh sách, F1 giảm 2\n- Nút「一括削除」trở lại disable",
       note="Nguồn: Improve list template r330-r335."),

    # ═════════════ 9. Phân trang ═════════════
    tc("Phân trang", "LIST-001", "Normal",
       "Phân trang mặc định 20 bản ghi / trang, chuyển trang hiện đúng dữ liệu, không có cột STT",
       ADM + "\n- Folder F1 có 45 group template",
       "1. Click folder F1\n2. Đếm số dòng trang 1 và quan sát vùng phân trang\n"
       "3. Bấm sang trang 2, trang 3 → đếm số dòng\n4. Bấm nút < và >\n"
       "5. Trên trang 2, thử search + sort + copy 1 group",
       "45 group, 20 dòng/trang",
       "- Trang 1 và 2 mỗi trang đúng 20 dòng, trang 3 có 5 dòng\n"
       "- Chuyển trang hiện đúng phần dữ liệu của trang đó; nút </> chuyển đúng 1 trang\n"
       "- Bảng KHÔNG có cột số thứ tự (STT)\n- Search/sort/copy trên trang 2 vẫn hoạt động đúng",
       note="Nguồn: Improve list template r341-r346. TC này lấp Gap của spec "
            "(ui-spec.md điểm chưa rõ #5「Có pagination không?」) → xem MT-14."),
]

# ── Cột「Trạng thái đánh giá spec」──
# Quy tắc: TC tham chiếu ít nhất 1 mã MÂU THUẪN thuộc nhóm SPEC-SILENT (spec không ghi / spec tự
# nhậ­n chưa rõ) →「Spec không ghi」. Các MT còn lại là trưồng hợp spec CÓ ghi nhưng LỆCH với TC
# → giữ「Spec ghi rõ」. TC do AI suy luậ­n mà cả corpus và spec đều không có cũng đánh「Spec không ghi」.
_SPEC_SILENT_MT = {
    "MT-04", "MT-08", "MT-09", "MT-10", "MT-11", "MT-12", "MT-13", "MT-14", "MT-15", "MT-16",
    "MT-17", "MT-18", "MT-19", "MT-20", "MT-21", "MT-22", "MT-23", "MT-24", "MT-25", "MT-26",
    "MT-27", "MT-28", "MT-29", "MT-30", "MT-31", "MT-32", "MT-34", "MT-35", "MT-36", "MT-37",
    "MT-39", "MT-41", "MT-42", "MT-43", "MT-45", "MT-47", "MT-48", "MT-49",
}
_AI_INFER = "SUY LUẬN CỦA AI"
for _r in S1:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
