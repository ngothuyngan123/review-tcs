# -*- coding: utf-8 -*-
"""Build kho TCs tổng hợp LME.

  python kho-tcs/build.py md      → sinh file .md trong kho-tcs/
  python kho-tcs/build.py sheet   → tạo/cập nhật Google Sheet, share cho user
"""
import sys, io, json, importlib, unicodedata
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "data"))

import _common  # noqa: E402
from _common import COLS, SECTIONS, build, section_summary  # noqa: E402

SA_EMAIL = "mcp-shhets@snappy-run-490703-k8.iam.gserviceaccount.com"
STATE = ROOT / ".sheet-id"

# Tab tổng hợp (dùng chung cho MỌI tính năng) — đứng trước các tab tính năng.
TAB_README = "_README"
TAB_SOURCES = "_Nguồn & phạm vi"
TAB_CONFLICTS = "_Mâu thuẫn cần quyết"
META_TABS = (TAB_README, TAB_SOURCES, TAB_CONFLICTS)


def tab_title(f):
    """Tên tab = <Mã màn hình> <Tên tiếng Việt> (<Tên màn hình tiếng Nhật>).

    VD: FA-001 Chat 1:1 (1:1チャット). Tên tiếng Việt là tên user gõ khi chạy
    /collect-tcs; tên tiếng Nhật lấy từ bảng feature ở templates/LME-SYSTEM-SPEC.md.
    """
    for k in ("code", "vi", "jp"):
        if not f.get(k):
            raise SystemExit(f"Feature thiếu khoá {k!r}: {f.get('code') or f.get('vi')}")
    return f"{f['code']} {f['vi']} ({f['jp']})"

# ── Đăng ký feature: (tên tab, module phần TC, module conflicts) ──────────────
FEATURES = [
    {
        "code": "FA-012", "vi": "Quản lý thẻ", "jp": "タグ管理",
        "applied": "2026-08-19",   # ngày ÁP quyết định Leader vào TCs
        "parts": ["tag_s1_folder.S1", "tag_s2_create.S2", "tag_s3_edit.S3",
                  "tag_s4_delete_list.S4", "tag_s5_action.S5"],
        "conflicts": "tag_conflicts",
        "spec": "spec-features/admin/tag-management/",
        "sources": [
            "10.1 TCsLine_Tag → tab「Improve tag t2/2025」(02/2025 → 04/2026, tab master còn sống)",
            "10.1 TCsLine_Tag → tab「Add tag bằng CSV」(06/2023 — đã bị tab master thay thế)",
            "TCsLine_Improve chung → tab「Improve tag」(2024-05-20)",
            "TCsLine_ModalAction → tab「Add tag mới ở modal action」(05/2023)",
        ],
        "excluded": [
            "TCsLine_MCP → 8.Tags / Create_tag_func / Create_tag_e2e — test tầng MCP tool, không phải màn Quản lý tag của LME (đề xuất tách sheet riêng 'MCP')",
            "TCsLine_Improve chung → 'Improve count scenario + tag' — nội dung chủ yếu là count scenario, thuộc feature Scenario",
            "10.1 TCsLine_Tag → tab ListBug — nhật ký bug UI, không phải test case",
        ],
    },
    {
        "code": "FA-001", "vi": "Chat 1:1", "jp": "1:1チャット",
        "prefix": "CHT",
        "sections": "SECTIONS_CHT",
        "parts": ["cht_s1_list_filter.S1", "cht_s2_quick_profile.S2", "cht_s3_send.S3",
                  "cht_s4_display.S4", "cht_s5_schedule_right.S5", "cht_s6_group_env.S6"],
        "conflicts": "cht_conflicts",
        "spec": "spec-features/admin/chat-11/ (⚠️ SCR-CHT-02 màn cài đặt chat còn ghi 6 tab — xem MT-04)",
        "sources": [
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Content: Hiển thị msg」(10/2024 → 06/2026, 1689 dòng, "
            "846 TC lá — tab master lớn nhất, 4 cột ticket #37831 #36859 #28618 #33833)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Content: Send message」(10/2024 → 04/2026, 1257 dòng, "
            "533 TC lá — 5 cột ticket SpecImprove #35389 #35523 #34297, Bug #32595 #32589)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Leftbar+Header」(10/2024 → 04/2026, 581 dòng, 446 TC lá "
            "— filter, search, quick action, profile sender, header, CRUD 対応ステータス; SpecImprove #35144 #33731, Bug #31202)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Rightbar」(10/2024, 459 dòng, 273 TC lá — 5 tab cột phải "
            "+ đặt lịch gửi + preview trước khi gửi)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Test fix bug Kh」(12/2025 → 2026, 146 dòng, 82 TC lá "
            "— Bug KH #33113, Bug tự detect #39257)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Feature #28859」(06/2025, 8 TC lá — giới hạn 180 ngày bot free)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Maincase」(bảng phẳng 40 dòng, không có kết quả mong đợi "
            "— dùng làm danh mục đối chiếu coverage)",
            "01. TCsLine_Chat1:1 (file CŨ, mod 2026-05-04) → tab「Group chat」(05/2023) ·「Improve move database」(09/2023) · "
            "「Improve server image」(11/2023) ·「Send media」+「Improve performance」(09/2024) ·「Test fix bug KH」 "
            "— từ 10/2024 đã bị file master thay thế (theo tab Info r6)",
            "TCsLine_Improve chung → tab「Profile sender」(12/2025, 184 TC lá — Bug KH #33072/#33052)",
            "TCsLine_Improve chung → tab「improve count comfirm_message」(120 TC lá — vòng đời bộ đếm chưa xác nhận)",
            "TCsLine_Improve chung → tab「Improve socket」(26 TC lá) ·「Send msg reply token」(7) ·「Phân quyền」(34) · "
            "「Improve ảnh profile」(3) ·「gửi tin nhắn từ web」(1)",
            "TCsLine_Improve chung / TCsLine_JOB → tab「Job move message」(12 TC lá — job chuyển tin nhắn sang bảng lưu trữ)",
        ],
        "excluded": [
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Chat GPT」(991 dòng, 780 TC lá) và「Bug chatGPT」(227 dòng) "
            "— tính năng ChatGPT連携 (học liệu folder/WEB/PDF, 基本設定, API key). Truy cập từ icon trong chat 1:1 "
            "nhưng là TÍNH NĂNG RIÊNG, CHƯA CÓ spec-features. ĐỀ XUẤT: tách feature riêng『ChatGPT連携』— HỎI USER XÁC NHẬN",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Setting Chat」(220 dòng, 175 TC lá) + 4 tab「[AI] Flow_setting_chat_v2」"
            "「[AI] Flow_validate_3333」「AI_TCs_Setting_chat_v1」「[AI] Bugs」— thuộc FA-041 Cài đặt chat "
            "(có spec riêng spec-features/admin/chat-setting/). ĐỀ XUẤT: gom khi chạy /collect-tcs cho FA-041; "
            "lưu ý 4 tab [AI] là bộ MỚI NHẤT (06-07/2026) và nói 8 tab thay vì 6 — xem MT-04",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Leftbar+Header」r473-r503 (khối talk list: get/filter/search, "
            "format hiển thị msg, change status message) — thuộc FA-002 Quản lý chat (/basic/talk-list), có spec riêng",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Leftbar+Header」r574-r581 (modal quy chế mới theo Figma MCP連携) "
            "— popup điều khoản hiển thị ở TẤT CẢ màn của tool, thuộc FA đăng nhập/user chứ không riêng chat 1:1",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Content: Hiển thị msg」r1515-r1562 (rà layout header admin qua "
            "màn đăng nhập / đăng ký / reset password / form / booking salon-lesson / landing / item) "
            "— là sweep hồi quy toàn tool, không phải TC của chat 1:1",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Content: Send message」r812-r975 (ma trận action đầy đủ của "
            "template button: multi action × friend action × URL scheme × giới hạn số lần bấm, ~160 dòng) "
            "— thuộc FA-010 Template (đã gom ở tab FA-010). Ở FA-001 chỉ giữ TC mức『gửi template có action → "
            "friend bấm thì action chạy đúng』",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「BugUI」(309 dòng) ·「BugLogic」(418) ·「Bug staging」(20) · "
            "「Bug comment」(33) ·「[AI] Bugs」(26) ·「Q&A」(69) ·「Data base message」(2 dòng) ·「Info」 "
            "— nhật ký bug và hỏi đáp, không phải test case có kết quả mong đợi",
            "TCsLine_Improve chung → tab「Improve talklist」(3 TC lá) — thuộc FA-002 Quản lý chat",
            "TCsLine_MCP → tab「11. Chat」(1072 dòng, format phẳng TC ID | MCP Tool | Category | Scenario) "
            "— test tầng MCP tool chứ không phải màn chat 1:1 của LME. ĐỀ XUẤT: tách sheet riêng『MCP』"
            "(giữ nguyên đề xuất như FA-012 và FA-011) — HỎI USER XÁC NHẬN",
        ],
    },
    {
        "code": "FA-011", "vi": "Tạo biểu mẫu", "jp": "フォーム作成",
        "applied": "2026-08-19 + 2026-08-22",   # ngày ÁP quyết định Leader vào TCs
        "prefix": "FORM",
        "parts": ["form_s1_list.S1", "form_s2_items.S2", "form_s3_page_setting.S3",
                  "form_s4_result_sync.S4", "form_s5_lineuser.S5"],
        "conflicts": "form_conflicts",
        "spec": "spec-features/admin/form-answer/ (bổ sung sau MT-00; ⚠️ index.md dòng 21 vẫn ghi CHƯA)",
        "sources": [
            "07. TCsLine_Form Answer → tab「Improve form 01/2025」(01/2025 → 06/2026, 3828 dòng — tab master phía admin, còn sống)",
            "07. TCsLine_Form Answer → tab「Improve form 01/2025 Line user」(01/2025 → 05/2026, 1580 dòng — tab master phía LINE user, còn sống)",
            "07. TCsLine_Form Answer → tab「Sync google」(03/2026 → 07/2026, 519 dòng — tab MỚI NHẤT, chủ đề đồng bộ Google Sheet)",
            "07. TCsLine_Form Answer → tab「#39053」(07/2026 — bug submit form nhiều item, 59 TC đã lọc)",
            "07. TCsLine_Form Answer → tab「Test fix bug KH」(10/2025) · 「Task nhỏ」(07/2025, export CSV 1 query) · 「SpecChange #30681」(07/2025, tạo sheet cho mọi page)",
            "07. TCsLine_Form Answer → tab「Maincase 04/2025」·「Mở form」(01/2024) ·「Form-answer dùng link liff app」(05/2023) ·「Thêm option hiển thị info」(09/2023) ·「Css, JS,HTML」·「Test setting chung」",
            "TCsLine_Improve chung → tab「Improve count form」(đếm số user trả lời) và tab「Improve tiny form」(font chữ)",
            "TCsLine_Limit all tính năng → tab「Limit Form answer」(03/2026 — 8 mục giới hạn)",
        ],
        "excluded": [
            "07. TCsLine_Form Answer → tab「Bug fix comment」(295 dòng) và「Bug phía line friend」(138 dòng) — nhật ký bug UI theo cột Priority/Mô tả/Ảnh/STT dev, KHÔNG phải test case có kết quả mong đợi",
            "07. TCsLine_Form Answer → tab「Message error」(36 dòng) — bảng tra cứu text validate (VN ↔ JP), là dữ liệu tham chiếu chứ không phải TC. ĐỀ XUẤT: dùng làm nguồn đối chiếu message khi Leader chốt MT-01/MT-06/MT-10",
            "TCsLine_Improve chung → tab「Improve tiny form」các dòng của tính năng khác (booking event, bill item, calendar salon/lesson, QR code, affiliate) — chỉ lấy phần Form answer",
            "TCsLine_MCP → toàn bộ tab — test tầng MCP tool, không phải màn Form của LME (giữ nguyên đề xuất tách sheet riêng 'MCP' như FA-012)",
        ],
    },
    {
        "code": "FA-004", "vi": "Rich Menu", "jp": "リッチメニュー",
        "applied": "2026-08-22",   # ngày ÁP quyết định Leader vào TCs
        "prefix": "RM",
        "parts": ["rm_s1_list_folder.S1", "rm_s2_create_step12.S2", "rm_s3_action.S3",
                  "rm_s4_step4_save.S4", "rm_s5_display_job.S5", "rm_s6_stats_env.S6"],
        "conflicts": "rm_conflicts",
        "spec": "spec-features/admin/rich-menu/",
        "sources": [
            "06. TCsLine_Richmenu → tab「Improve richmenu 2025.09」(09/2025 → 08/2026, 1955 dòng, 1834 TC lá — tab master còn sống, 12 cột kết quả theo ticket #32940 #32950 #32988 #32989 #33287 #33396 #33471 #33769 #36064 #37468 #39229)",
            "06. TCsLine_Richmenu → tab「Maincase 2025.09」(09/2025, 146 TC lá — bộ case chính + khối Backup)",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2025.09 (Line user)」(09/2025, 69 TC lá — ma trận switch richmenu phía LINE + job open_date/close_date + bug KH #32988)",
            "06. TCsLine_Richmenu → tab「Test fix bug KH」(09/2024, 27 TC lá — bug #26675 default richmenu, bug #26741 limit plan free)",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2023.03」(03/2023, 31 TC lá — job link/unlink theo cơ chế default cũ; TC > 2 năm, phần lớn đã bị đợt improve 09/2025 thay thế)",
            "06. TCsLine_Richmenu → tab「Sử dụng liff app booking」(02/2024, 10 dòng — ma trận kiểm tra, KHÔNG có kết quả mong đợi)",
            "TCsLine_Improve chung → tab「Improve richmenu」(2024-05-14, 15 TC lá — multi action + open url các tính năng LME)",
        ],
        "excluded": [
            "06. TCsLine_Richmenu → tab「Image richmenu」(120 dòng) — toàn bộ nội dung thuộc màn「Tạo hình ảnh Rich Menu」(FA-005 /basic/image-richmenu), là TÍNH NĂNG KHÁC với FA-004 và CHƯA CÓ spec-features. ĐỀ XUẤT: gộp riêng khi chạy /collect-tcs cho FA-005 (bug #31953, #33970)",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2023.03」các dòng r67-r85 — khối bug #31953 upload ảnh PNG, cũng thuộc màn tạo ảnh richmenu (FA-005). Riêng rủi ro lặp lại ở Step 1 của FA-004 đã được giữ lại thành 1 TC + MT-07",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2023.03」các dòng r12-r16 (xóa lịch sử action khi xóa friend: auto_reply_history, user_button, user_open_formanswer, bot_line_user_item) — thuộc AutoReply / Template / Form / Item, không phải Rich Menu",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2023.03」các dòng r19-r50 (Button, Image map) — thuộc tính năng Template (FA-010); phần Rich menu r51-r66 đã được phủ bởi TC action mở URL của tập master",
            "06. TCsLine_Richmenu → tab「Sheet7」— kết quả truy vấn SQL (bot_id, email, ngày xóa), là dữ liệu điều tra chứ không phải test case",
            "06. TCsLine_Richmenu → tab「Info」/「Q&A」/「ListBug」— nhật ký niên đại, hỏi đáp và bug UI, không phải test case",
            "TCsLine_Header/Menu (toàn bộ file) — khớp keyword 'menu' nhưng là header/menu của admin portal, không phải LINE Rich Menu",
        ],
    },
    {
        "code": "FA-015", "vi": "Quản lý thông tin bạn bè", "jp": "友だち情報管理",
        "prefix": "FRI",
        "parts": ["fri_s1_list_folder.S1", "fri_s2_create_types.S2", "fri_s3_edit_copy_delete.S3",
                  "fri_s4_value_count.S4", "fri_s5_action_job.S5", "fri_s6_default_env.S6"],
        "conflicts": "fri_conflicts",
        "spec": "spec-features/admin/friend-information/",
        "sources": [
            "10.2 TCsLine_friend_information → tab「test fix bug」(08/2024 → 07/2026, 586 dòng — tab master còn sống, 9 cột kết quả theo ticket #26541 #26532 #30558 #33697 #34625 #36201 #37606 #38469 #38536 #38591 #38727)",
            "10.2 TCsLine_friend_information → tab「check setting-action-friend-info-date」(10/2025 → 04/2026, 390 dòng — tab master của action/job kiểu ngày tháng: Bug #32287, Bug KH #34675, Bug Tester #35967)",
            "10.2 TCsLine_friend_information → tab「Feature #29832」(06/2025, 276 dòng — thêm folder thông tin địa chỉ 5 trường vào toàn bộ tính năng của tool)",
            "10.2 TCsLine_friend_information → tab「Improve count phía web」(06/2025, 142 dòng — quy tắc cộng/giữ/trừ 回答人数 + reset khi change bot)",
            "10.2 TCsLine_friend_information → tab「Change spec info type select」(12/2024, Bug #27314, 84 dòng — option select có mã riêng + cascade 7 bảng)",
            "TCsLine_Improve chung → tab「Improve filter friend info + sửa domain liff app」(07/2023, phần filter friend info r3-r93 — TC > 3 năm, đã đánh dấu CẦN VERIFY LẠI)",
            "TCsLine_Improve chung → tab「Test bug folder all màn」(Bug Tester #27083, 04/2026 — khối 7. Màn friend info r106-r122)",
            "TCsLine_Improve chung → tab「recover bảng category」(06/2025 — dòng kind=12 friend info) ·「Phân quyền」(11/2023 — message quyền dùng chung mọi màn)",
            "TCsLine_ModalAction → tab「Thêm option random cho action friend infor point」(11/2023 + Feature #24521 10/2023 — random điểm ghi đè/cộng/trừ; TC ~2.8 năm, CẦN VERIFY LẠI)",
            "TCsLine_Modal Filter → tab「Filter point & date」(10/2023 — điều kiện filter friend info kiểu ngày tháng và điểm; CẦN VERIFY LẠI)",
        ],
        "excluded": [
            "TCsLine_MCP → tab 9.Friend_info / Friend-info_func / Friend-info_e2e / 2.Friend_stats / 12.Friend_list / Setting-add-friend_* / Update_trạng_thái_đối_ứng_friend — test tầng MCP tool, không phải màn 友だち情報管理 của LME (giữ nguyên đề xuất tách sheet riêng 'MCP' như FA-012/FA-011/FA-004)",
            "TCsLine_Detail_Friend (toàn bộ file: Improve 2026.05, Trigger action, [AI] TCs_*, [AI] Bugs) — thuộc FA-014 màn 友だち詳細, là tính năng KHÁC (có spec riêng spec-features/admin/detail-friend/). Phần giao nhau (ghi/xóa giá trị friend info ở màn 友だち詳細) đã lấy từ tab master của 10.2, không lấy lại từ file này",
            "10.3 TCsLine_Friendlist → tab Testcase / #38866 — thuộc FA-013 Danh sách bạn bè",
            "07. TCsLine_Form Answer → tab「Bug phía line friend」·「Thêm option hiển thị info」— đã gộp vào kho FA-011 Form; phần liên kết friend info của form lấy qua tab master của 10.2",
            "15.3 TCsLine_ChangeBot → tab「Get old friend」· TCsLine_Bill tiền_Improve2025 → tab「Bill max friend」· 03. TCsLine_Broadcast → tab「Update list friend đã send」· TCsLine_JOB + TCsLine_Improve chung → tab「Test callback friend」— khớp keyword 'friend' nhưng thuộc tính năng khác (đổi bot, bill tiền, broadcast, callback bot)",
            "10.2 TCsLine_friend_information → tab「list bug」(29 dòng) — nhật ký bug, không phải test case có kết quả mong đợi",
        ],
    },
    {
        "code": "FA-009", "vi": "Phát hành theo bước", "jp": "ステップ配信",
        "prefix": "SCE",
        "sections": "SECTIONS_SCE",
        "parts": ["sce_s1_folder_list.S1", "sce_s2_step_filter.S2", "sce_s3_message_action.S3",
                  "sce_s4_preview_test.S4", "sce_s5_next_count.S5", "sce_s6_job_env.S6"],
        "conflicts": "sce_conflicts",
        "spec": "spec-features/admin/scenario/",
        "sources": [
            "04. TCsLine_Scenario → tab「Testcase」(4/2024 → 06/2026, 1067 dòng — tab master còn sống, 4 cột kết quả theo ticket Bug KH #36365, Feature #30571, Bug #32281 + Test Result/staging/step)",
            "04. TCsLine_Scenario → tab「Job scenario」(7/2025 → 03/2026, 256 dòng — tab master phía job, 4 khối ticket: Bug tự detect next qua ngày · Bug lặp vô hạn · Bug #32469 · Bug #32802 · Bug KH #32903 · Bug KH #34489)",
            "04. TCsLine_Scenario → tab「text fix bug Kh」(04/2025 → 06/2026, 140 dòng — Bug #29551 profile sender · Bug #28916 cột 途中で終了した友だち · Bug #32587 link manual · Bug KH #37711 trùng line_user)",
            "04. TCsLine_Scenario → tab「improve sce 20/6」(20/6/2024, 38 dòng — giới hạn 100 step/filter + màn preview theo tuần)",
            "04. TCsLine_Scenario → tab「21/11」(21/11/2023, 28 dòng — thêm cột order_number cho step_message)",
            "04. TCsLine_Scenario → tab「2/12」(2/12/2023, 15 dòng — send test 3 option, không tính vào số lượng đã send)",
            "TCsLine_Improve chung → tab「Improve update msg scenario」(2025-01-16, 88 dòng — mapping step_message ↔ template_mapping_tables, update template group/đơn/clone)",
            "TCsLine_Improve chung → tab「Improve count scenario + tag」(2023-12-10, 90 dòng — quy tắc cộng/trừ count_follow, count_stop phía web và phía job; phần tag đã loại, thuộc FA-012)",
            "TCsLine_Improve chung → tab「Improve sendall scenario」(88 dòng — cửa sổ 5 phút cập nhật filter trước giờ gửi; phần Send all 10 phút đã loại, thuộc FA-003)",
            "TCsLine_Improve chung → tab「Scenario write DB rieng」(21 dòng — tách DB scenario, verify bot cũ/bot mới sau release)",
            "TCsLine_Improve chung → tab「#35968」(06/2026 — khối Scenario r113-r169 + TCS bổ sung chung r170-r174: sort item/folder sau kéo-thả)",
            "TCsLine_Improve chung → tab「Test bug folder all màn」(Bug #32468, 04/2026 — khối 4. Màn scenario r55-r62)",
            "TCsLine_Improve chung → tab「Phân quyền」(11/2023 — message quyền dùng chung mọi màn; TC ~2.8 năm tuổi, đã đánh dấu CẦN VERIFY LẠI)",
        ],
        "excluded": [
            "TCsLine_MCP → tab「Scenario_func」·「Scenario_e2e」·「06.Scenario」— test tầng MCP tool, không phải màn ステップ配信 của LME (giữ nguyên tiền lệ FA-012/FA-011/FA-004/FA-015 — đề xuất tách sheet riêng 'MCP'). Đã được user xác nhận.",
            "TCsLine_JOB → toàn bộ tab — file này dùng CHÍNH gid với TCsLine_Improve chung (ví dụ gid=523928908「Improve update msg scenario」), là bản sao của cùng spreadsheet → không gộp lại để tránh nhân đôi TC",
            "04. TCsLine_Scenario → tab「Bug improve sce 20/6」(44 dòng) — cấu trúc Màn hình/Mô tả/Ảnh/Assign/Dev/Test dev, là nhật ký bug UI chứ KHÔNG phải test case có kết quả mong đợi",
            "Bug KH #37711 → các dòng thuần add-friend (mua item bill 1 lần/chu kỳ r124-r125, booking event/salon/lesson r127-r129) — root cause ở tầng add-friend/callback, không quan sát được từ màn Scenario. Đã giữ lại phần scenario-observable theo xác nhận của user.",
            "TCsLine_Improve chung → tab「Improve count scenario + tag」r56-r90 (phần count_user_tag) — thuộc FA-012 Quản lý thẻ, đã gộp ở kho FA-012",
            "TCsLine_Improve chung → tab「Improve sendall scenario」r11-r34 (phần Send all/broadcast, cửa sổ 10 phút, giới hạn 100 item filter AND/OR) — thuộc FA-003 Broadcast",
            "TCsLine_Improve chung → tab「#35968」các khối Template/QR/Form/URL/Cross — thuộc tính năng khác; chỉ lấy khối Scenario và khối TCS bổ sung chung có nhắc Scenario",
            "TCsLine_Modal Filter · TCsLine_ModalAction — đã rà toàn bộ, KHÔNG có tab nào thuộc màn ステップ配信 (nội dung là modal filter/action dùng chung, đã gộp ở FA-012/FA-015)",
            "TCsLine_BackUp — backup cấp bot, không riêng scenario; phần backup scenario đã lấy từ khối「Check backup」r76-r89 của tab master",
        ],
    },
    {
        "code": "FA-026", "vi": "Bill tiền item", "jp": "商品販売",
        "prefix": "BIL",
        "sections": "SECTIONS_BIL",
        "parts": ["bil_s1_admin_item.S1", "bil_s2_lineuser_buy.S2", "bil_s3_change_cancel.S3",
                  "bil_s4_payment_engine.S4", "bil_s5_job_action.S5", "bil_s6_history_setting.S6",
                  "bil_s7_audit_add.S7"],
        "conflicts": "bil_conflicts",
        "spec": "spec-features/admin/bill-item/",
        "sources": [
            "12. TCsLine_Item → tab「Quản lý sản phẩm」(02/2023 → 02/2026, 452 dòng — tab MASTER còn sống: "
            "toàn bộ vòng đời sản phẩm + luồng mua + job bill; 3 khối ticket Feature #30651 (02/2026), "
            "Bug KH #33732 (01/2026), Update spec chuyển UnivaPay sang bill job)",
            "12. TCsLine_Item → tab「Improve bill tiền univapay」(05/2025 → 06/2026, 327 dòng — tab MASTER của "
            "cơ chế bill: Bug KH #33787 (18+29/01/2026 — đổi mốc chờ kết quả 2p5s → 1p → 5s), "
            "Bug KH #36443 (05/2026 — hạn mức + message lỗi), Bug Tester #38077 (06/2026 — status Authorized)",
            "12. TCsLine_Item → tab「Improve bill tiền stripe」(10/2025 → 04/2026, 146 dòng — cơ chế tạo order "
            "trước + change spec 10/2025 (đóng trình duyệt ở 3DS không tính bill fail) + SpecImprove #34857 "
            "(03/2026 description Stripe) + Bug KH #35992 (04/2026 — TỒN KHO, khối mới nhất)",
            "12. TCsLine_Item → tab「test fix bug」(08/2024 → 02/2026, 368 dòng — 6 khối bug: #26568 mã chèn số "
            "tiền · #26719 preview ≠ edit · #26850 action bill lỗi · #28262 thanh toán trùng · #29472 change card "
            "không action · #29752 refund lỗi · #31068 redirect về chat (5 điểm mở link × 4 môi trường) · "
            "#31871 表示設定 không update · #32729 export CSV ký tự đặc biệt)",
            "12. TCsLine_Item → tab「Màn liên kết bill tiền」(06/2024 → 01/2026, 152 dòng — tab MASTER của màn "
            "liên kết cổng: brand card + Bug #32455/#32370 ẩn App ID + Bug #32535 webhook domain + "
            "Support #32786 domain LIFF/redirect)",
            "12. TCsLine_Item → tab「improve bill tiền 3D secure」(67 dòng — ma trận thẻ 3DS Stripe + refund "
            "cơ chế cũ/mới)",
            "12. TCsLine_Item → tab「Test invoice (stripe)」(24 dòng — setting thuế 8%/10% + tạo 4 TaxRate khi "
            "liên kết Stripe + hóa đơn ở 3 luồng)",
            "12. TCsLine_Item → tab「Sheet2」(6 dòng — bot hết hạn thì job bill chu kỳ dừng; là căn cứ của MT-23)",
            "12. TCsLine_Item → tab「Info」(19 dòng) và「ListBug」(25 dòng) — dùng để xác định NIÊN ĐẠI và "
            "truy vết bug cũ, không lấy làm TC",
            "TCsLine_Improve chung → tab「Monitor bill tiền」khối ITEM r66-r91 (11/2025 — job monitor đối soát "
            "giao dịch item với UnivaPay/Stripe; khối cũ 2023 r6-r8 đã bị thay thế, xem MT-29)",
        ],
        "excluded": [
            "TCsLine_Bill tiền (22 tab) và TCsLine_Bill tiền_Improve2025 (9 tab) — TOÀN BỘ thuộc **FA-031 "
            "Hợp đồng và thanh toán gói SaaS của chính bot** (plan, hợp đồng, add bot, refund hợp đồng, campaign, "
            "phân bổ, hóa đơn). `feature-spec.md:1083` §8.3 nêu rõ ranh giới: payment_histories, "
            "request_paypal_item, cron job:check_auto_payment_univapay **KHÔNG thuộc FA-026**. "
            "★ CẦN USER XÁC NHẬN — đề xuất gom riêng thành kho FA-031",
            "11.1 TCsLine_SalonCalendar ·11.2 TCsLine_LessonCalendar · 11.3 TCsLine_EventBooking → các tab "
            "「Improve bill tiền stripe」「Improve bill tiền univapay」「improve bill tiền 3D secure」"
            "「Liên kết bill tiền」— cùng ĐỢT IMPROVE nhưng nội dung là booking salon/lesson/event "
            "(bảng calendar_salon_line_booking / calendar_course_bookings / b_user_booking), KHÔNG phải bill item. "
            "Đã xác minh bằng cách đọc grid tab SalonCalendar. Phần regression liên quan đã giữ lại 1 TC ở "
            "『Bill UnivaPay — callback & webhook』",
            "TCsLine_MCP → tab「15.Product」(165 dòng: list_products / get_product_detail / "
            "get_product_order_history) — test tầng MCP tool (input bot_id, output field mapping, mã lỗi HTTP), "
            "KHÔNG phải màn 商品販売 của LME. Giữ nguyên tiền lệ FA-012/FA-011/FA-004/FA-015/FA-009 — "
            "đề xuất tách sheet riêng 'MCP'. ★ CẦN USER XÁC NHẬN",
            "TCsLine_JOB → tab「Monitor bill tiền」— trùng gid=1905032532 với TCsLine_Improve chung "
            "(cùng 1 spreadsheet nội dung), không gộp lại để tránh nhân đôi TC",
            "TCsLine_Improve chung / Monitor bill tiền → khối「Check bill tiền bot」r11-r65 (verify giao dịch "
            "hợp đồng BOT với UnivaPay/Stripe, bảng payment_history) — thuộc FA-031, chỉ lấy khối ITEM r66-r91",
            "12. TCsLine_Item → tab「Quản lý sản phẩm」r232 và「test fix bug」r2/r29/r47/r60/r71/r82/r92/r299 — "
            "các dòng mô tả bug/đánh giá ảnh hưởng (độ dài > 200 ký tự, gộp hết cột path), là HEADER KHỐI "
            "chứ không phải test case",
            "12. TCsLine_Item → tab「Quản lý sản phẩm」r314-r323 (ma trận subscription UnivaPay theo period "
            "monthly/weekly/Quarterly/Semiannually/Annually) — đã bị khối r388+ thay thế "
            "(「chuyển qua bill job như stripe, không dùng subcription nữa」). Giữ lại 1 TC thăm dò + MT-13",
            "TCsLine_Affiliate · [AI] TCs · TCsLine_Admin · TCsLine_Test Limit theo plan · "
            "TCsLine_Limit all tính năng · TCsLine_Setting Liên kết BOT · TCsLine_ModalAction · "
            "TCsLine_Modal Filter — đã rà toàn bộ danh sách tab, KHÔNG có tab nào thuộc màn 商品販売",
        ],
    },
    {
        "code": "FA-021", "vi": "Event booking", "jp": "イベント予約",
        "prefix": "EBK",
        "sections": "SECTIONS_EBK",
        "parts": ["ebk_s1_admin_event.S1", "ebk_s2_setting_pages.S2", "ebk_s3_lineuser.S3",
                  "ebk_s4_payment.S4", "ebk_s5_admin_booking.S5", "ebk_s6_remind_job_env.S6"],
        "conflicts": "ebk_conflicts",
        "spec": "spec-features/admin/event-booking/",
        "sources": [
            "11.3 TCsLine_EventBooking → tab「Task nhỏ + fix bug KH」(09/2024 → 07/2026, 313 dòng — "
            "tab MASTER còn sống, 7 khối ticket: Bug #26616 highlight thông tin đổi · xóa cascade "
            "slot/plan/event · bộ đếm use_people/remain_limit · SpecImprove #33649 (03/2026 job recover "
            "count) · Bug KH #34738 (03/2026 change booking không update remind) · Bug KH #38200 "
            "(06/2026 リクエスト制) · Support #37932 (06/2026 OGP khi share URL) · Bug Tester #38312 "
            "(06/2026 lịch sử friend info) · Bug tự detect #38690 (07/2026 refund fail — KHỐI MỚI NHẤT)",
            "11.3 TCsLine_EventBooking → tab「Event booking 1.0」(03/2023 → 09/2025, 355 dòng — bộ case gốc "
            "toàn bộ màn admin + LINE user; khối cuối là Bug #31908 (09/2025) và disable button submit khi "
            "chưa lấy được line id)",
            "11.3 TCsLine_EventBooking → tab「Event booking 2.0」(05/2023 → 10/2025, 97 dòng — setting theo "
            "duration, max plan/max slot, SpecChange quy tắc đổi lịch, Bug #32366 (10/2025) replace data khi "
            "duyệt đổi lịch, + 2 bug TỰ DETECT chưa fix ở r81-r97)",
            "11.3 TCsLine_EventBooking → tab「SpecChange #26808」(14/10/2024, 73 dòng — TOÀN BỘ ma trận giới "
            "hạn số chỗ slot × コース, phân biệt「báo lỗi」vs「không cho chọn」)",
            "11.3 TCsLine_EventBooking → tab「Improve bill tiền univapay」(04/2025 → 03/2026, 183 dòng — bill "
            "kiểu cũ (polling) và kiểu mới (callback), màn lịch sử booking theo status_webhook, Bug KH #33787 "
            "(18/01/2026), SpecImprove #34895 (giảm sleep), SpecImprove #34857 (description trên cổng))",
            "11.3 TCsLine_EventBooking → tab「Improve bill tiền stripe」(10/2025 → 03/2026, 80 dòng — booking "
            "mới + đổi lịch có bill, job quét kết quả, change spec 10/2025 về 3DS đóng trình duyệt, "
            "SpecImprove #34857)",
            "11.3 TCsLine_EventBooking → tab「improve bill tiền 3D secure」(03/2024, 103 dòng — ma trận thẻ 3DS "
            "+ ma trận liên kết/hủy liên kết cổng giữa chừng cho cả Stripe và UnivaPay)",
            "11.3 TCsLine_EventBooking → tab「Event booking 3.0」(07/2023, r3-r17 — export CSV thêm cột friend "
            "info; phần r19-r66 thuộc màn 商品販売 đã loại, xem excluded)",
            "11.3 TCsLine_EventBooking → tab「Sheet4」(Bug #24441, 10/2023, 8 dòng — công thức tính 定員 của 1 "
            "ngày. ⚠ Tab BỊ ẨN, noise filter của list_tc_sources.py loại khỏi listing — phải fetch toàn bộ "
            "file mới thấy)",
            "11.3 TCsLine_EventBooking → tab「Info」(18 dòng) — dùng để xác định NIÊN ĐẠI 17 đợt thay đổi "
            "(03/2023 → 07/2026), không lấy làm TC",
            "TCsLine_Test Limit theo plan → tab「[AI] Test limit v2」r81-r95 (TC-LMT-058→069, 224→226 — 15 TC "
            "giới hạn số event theo gói Free/Standard/Pro, đã có kết quả Pass/Partial)",
            "TCsLine_Improve chung → tab「Improve nhỏ」r320 (Bug Tester #33106 — màn booking không phân quyền "
            "vẫn access được, kết quả NG) · r304+r334 (Bug Tester #33107 — bot A access link bot B) · "
            "r324/r330 (line user mở link khi là / không là friend) · r386 (header không hiện gói giá) · "
            "r454-456/r500 (ảnh header khi tạo/sửa/copy event) · r1152/r1173 (preview sub action 当日日付を登録)",
            "TCsLine_Improve chung → tab「Test bug folder all màn」r174 (Bug #32468, 10/2025 — khối「11. Màn "
            "booking event」: tạo folder trùng tên)",
            "TCsLine_Improve chung → tab「Improve tiny form」r9 (Booking event — selectbox font chữ, link "
            "staging /basic/booking-event-day/1118/edit)",
        ],
        "excluded": [
            "11.3 TCsLine_EventBooking → tab「Event booking 3.0」r19-r66 (48 dòng: export CSV ở màn「商品販売」"
            "— sản phẩm bill 1 lần / bill chu kỳ, filter theo môi trường/cổng/status, nội dung file CSV) — "
            "**thuộc FA-026 商品販売**, đã gom ở tab FA-026. Đợt improve 3.0 (07/2023) thêm cột friend info cho "
            "**cả 2** tính năng nên nằm chung 1 tab. ĐỀ XUẤT: giữ nguyên ở FA-026, không nhân bản sang đây — "
            "**cần bạn xác nhận**",
            "11.3 TCsLine_EventBooking → tab「Improve event cũ 2023.03」(03/2023, 40 dòng) — toàn bộ là dòng "
            "**chỉ có tiêu đề, KHÔNG có kết quả mong đợi**; nội dung (đổi thông tin booking từ màn list người "
            "tham gia / màn list slot) nghi thuộc bộ **event v1** (`type_event_new = 0`) — spec §1.3 xếp v1 là "
            "**tính năng riêng, ngoài phạm vi**. ĐỀ XUẤT: tách sang kho riêng cho event v1 — "
            "**cần bạn xác nhận** (xem MT-33)",
            "11.3 TCsLine_EventBooking → tab「 list bug improve bill tiền」(2 dòng) — nhật ký bug theo cột "
            "Ngày/Màn hình/Mô tả/Assign/Status, KHÔNG phải test case có kết quả mong đợi",
            "11.4 TCsLine_Remind (event) → tab「Improve」(SpecImprove #34887, 03/2026, 24 dòng) — test màn "
            "**danh sách remind** `/basic/events` (query N+1, count user_event, sort/copy/xóa remind), thuộc "
            "**FA-022 リマインド配信** — spec §1.3 xếp FA-022 ngoài phạm vi (chỉ tham chiếu qua dropdown "
            "「リマインド選択」). Các TC remind trong kho này chỉ gồm phần **gắn remind vào booking**. "
            "ĐỀ XUẤT: tách tab riêng cho FA-022 — **cần bạn xác nhận**",
            "TCsLine_Data warehouse → tab「Event_Tracking」và「Event Tracking TCs_old」— khớp keyword \"event\" "
            "nhưng là **Event Tracking của data warehouse** (sync data, CDC, matrix screen/browser/device), "
            "không liên quan màn イベント予約",
            "11.1 TCsLine_SalonCalendar · 11.2 TCsLine_LessonCalendar · TCsLine_Booking Calendar — khớp keyword "
            "\"booking\" nhưng thuộc **FA-020 サロン・面談予約** và lịch học; spec §1.3 ghi rõ không dùng chung bảng",
            "06. TCsLine_Richmenu → tab「Sử dụng liff app booking」(02/2024, 10 dòng) — ma trận kiểm tra "
            "**KHÔNG có kết quả mong đợi**, đã được gom ở tab FA-004 Rich Menu",
            "TCsLine_Improve chung → tab「Improve nhỏ」r766-r786 (multi action — xóa template/scenario/tag đang "
            "được dùng): khối này ghi「Events」= màn **remind** `/basic/events`, không phải event booking. "
            "Đã viết 1 TC suy sang slot event booking — **cần bạn xác nhận phạm vi**",
            "TCsLine_MCP · TCsLine_ModalAction · TCsLine_Modal Filter · TCsLine_JOB · TCsLine_Limit all tính "
            "năng — đã rà toàn bộ danh sách tab, KHÔNG có tab nào dành riêng cho màn イベント予約",
        ],
    },
    {
        "code": "FA-031", "vi": "Bill tiền tool", "jp": "契約プラン・決済情報",
        "prefix": "BLP",
        "sections": "SECTIONS_BLP",
        "parts": ["blp_s1_list.S1", "blp_s2_buy_upgrade.S2", "blp_s3_detail_change.S3",
                  "blp_s4_cancel_history.S4", "blp_s5_invoice_estimate.S5",
                  "blp_s6_job_billing.S6", "blp_s7_maxfriend_campaign.S7",
                  "blp_s8_env_perm.S8"],
        "conflicts": "blp_conflicts",
        "spec": "spec-features/admin/billing-plan/",
        "sources": [
            "TCsLine_Bill tiền_Improve2025 → tab「Quản lý hợp đồng」(12/2025 → 07/2026, 1731 dòng, "
            "1506 TC lá — tab MASTER còn sống, 15 cột kết quả theo ticket: Bug KH #39059, Feature #37085, "
            "Bug KH #37109, #36835, #36373, #36492, #36303, SpecImprove Test #36076, Specchange 03/2026, "
            "Support #35316, Bug KH #35635, SpecImprove #35441, Bug KH #35467, SpecImprove #34505, "
            "Bug KH #34792, #34521, #34408)",
            "TCsLine_Bill tiền_Improve2025 → tab「Màn hình bill tiền」(12/2025 → 07/2026, 647 dòng, 531 TC lá — "
            "màn chọn plan, xác nhận plan, nhập thẻ, chuyển khoản, logic bill tiền, job bill, ngày expired_date; "
            "Bug tự detect #38298 và #38957)",
            "TCsLine_Bill tiền_Improve2025 → tab「Bill max friend」(12/2025 → 04/2026, 402 dòng, 319 TC lá — "
            "Bug KH #34409, Bug Tester #35650, SpecImprove #35441)",
            "TCsLine_Bill tiền_Improve2025 → tab「List main case」(347 dòng — bộ main case của đợt improve) và "
            "tab「Campaign + Tutorial」(327 dòng, 265 TC — chỉ lấy phần Campaign 初月無料; cột Expect Result bị "
            "lệch sang cột 'Actual Result', đã bù khi đọc)",
            "TCsLine_Bill tiền_Improve2025 → tab「Check lịch sử hợp đồng」(103 dòng — ma trận 27 loại lịch sử) và "
            "tab「Compare logic cũ」(18 dòng — bảng đối chiếu trạng thái list bot cũ ↔ list hợp đồng mới)",
            "TCsLine_Bill tiền_Improve2025 → tab「Feature #36994」(07/2026, 41 dòng — thêm mục 「お住まい」vào "
            "trang thanh toán; đây là bộ TC AI-format có cột Actual Result ghi kết quả thật)",
            "TCsLine_Bill tiền → tab「Improve màn download quản lý hóa đơn」(09/2025 → 11/2025, 349 dòng, "
            "323 TC lá — Feature #30564, Bug #32649, Bug KH #32953)",
            "TCsLine_Bill tiền → tab「Improve bill tiền 12/2024」(12/2024 → 01/2025, 630 dòng, 405 TC lá — "
            "SpecChange #30442, Bug #32358, Bug #32681)",
            "TCsLine_Bill tiền → tab「Logic chung」(08/2025, 104 TC — expired_date + 7 ngày chặn trang LINE user "
            "của Lesson/Salon/Form/Item/Booking Event; SpecChange #32268 đổi địa chỉ trên hóa đơn & báo giá). "
            "⚠ Cột Expect Result thật nằm ở cột 'Sub 5'",
            "TCsLine_Bill tiền → tab「Plan bill tiền mới 1.0」(04/2023, 77 TC) ·「Cố định ngày bill tiền」(07/2023, "
            "22 TC) ·「Redirect khi bill success」(09/2024, 35 TC) ·「Estimation」(09/2023, phần lớn CHỈ CÓ TIÊU ĐỀ) · "
            "「Change bill tiền theo năm」(12/2023, 12 TC) ·「Task nhỏ」(12/2023, 11 TC) ·"
            "「Bill tiền univapay: 3D secure」(03/2025, 11 TC)",
            "TCsLine_Bill tiền → tab「Logic refund」(04/2023, 21 TC) ·「Refund update 1.0」(05/2023, 12 TC) — "
            "thao tác từ admin portal nội bộ nhưng hậu quả nằm trong bot_contracts (xem MT-00b)",
            "TCsLine_Bill tiền → tab「Info」(23 dòng) và TCsLine_Bill tiền_Improve2025 → tab「Info」(41 dòng) — "
            "dùng để xác định NIÊN ĐẠI và truy vết ticket, không lấy làm TC",
        ],
        "excluded": [
            "TCsLine_Bill tiền → tab「Improve add bot」(130 TC) ·「change_bot」(33 TC) ·"
            "「Change design add bot」(21 TC) ·「Bug_Change design add bot」·「Add bot ot」(12 TC) — "
            "toàn bộ là luồng ADD BOT / CHANGE BOT (quét QR, provider, webhook verify), thuộc "
            "spec-features/admin/bot-add-v2/ và file 15.3 TCsLine_ChangeBot. ★ CẦN USER XÁC NHẬN",
            "TCsLine_Bill tiền → tab「Bill tiền/ phân bổ/ TOP」(18 TC) — màn bill tiền / phân bổ / TOP của "
            "ADMIN PORTAL NỘI BỘ (super admin), thuộc file TCsLine_Admin (tab「Thống kê doanh số admin」). "
            "★ CẦN USER XÁC NHẬN — liên quan MT-00b",
            "TCsLine_Bill tiền → tab「Bug improve 12/2024」(57 dòng) ·「Bug_Change design add bot」(24 dòng) ·"
            "「ListBug」(30 dòng) — nhật ký bug UI theo cột Priority/Mô tả/Ảnh/Status dev, KHÔNG phải test case "
            "có kết quả mong đợi",
            "TCsLine_Bill tiền → tab「Draft」(27 dòng) và TCsLine_Bill tiền_Improve2025 → tab「Draft for Ngan」"
            "(34 dòng, rỗng) — bản nháp; nội dung tab Draft đã được hoàn thiện thành「Compare logic cũ」và"
            "「Check lịch sử hợp đồng」ở file Improve2025",
            "TCsLine_Bill tiền → tab「Test fix bug」(26 dòng, chỉ 2 TC có expected) và"
            "「Check lại job bill tiền sau khi thêm plan」(14 dòng, 0 TC có expected) — chỉ có tiêu đề, "
            "nội dung đã bị các đợt improve sau thay thế",
            "TCsLine_Bill tiền_Improve2025 → tab「Campaign + Tutorial」phần TUTORIAL (modal ようこそ, floating "
            "banner, mini floating, job ScanHasTutorial — khoảng 150 dòng) — thuộc onboarding, không liên quan "
            "hợp đồng/tiền. ★ CẦN USER XÁC NHẬN — xem MT-00c",
            "11.1 TCsLine_SalonCalendar · 11.2 TCsLine_LessonCalendar · 11.3 TCsLine_EventBooking · "
            "12. TCsLine_Item → các tab「Improve bill tiền stripe/univapay」「improve bill tiền 3D secure」"
            "「Liên kết bill tiền」— cùng đợt improve nhưng nội dung là bill tiền của ITEM / BOOKING, "
            "thuộc FA-026 và FA-021 (đã gom ở kho riêng)",
            "TCsLine_Improve chung / TCsLine_JOB → tab「Monitor bill tiền」khối ITEM r66-r91 — thuộc FA-026 "
            "(kho bill item đã lấy). Kho FA-031 chỉ lấy khối『Check bill tiền bot』r11-r65, và mới ở mức TC "
            "khung — xem MT-31",
            "TCsLine_Admin → tab「Coupon」— màn coupon của admin portal nội bộ. Corpus FA-031 KHÔNG có TC "
            "coupon nào dù UI production có nút 「クーポンコードを入力する」— xem MT-23",
            "TCsLine_Test Limit theo plan · TCsLine_Limit all tính năng · TCsLine_Mypage · TCsLine_QLStaff · "
            "TCsLine_Setting Liên kết BOT · TCsLine_MCP — đã rà toàn bộ danh sách tab, KHÔNG có tab nào thuộc "
            "5 màn của FA-031",
        ],
    },
    {
        "code": "FA-010", "vi": "Mẫu tin nhắn", "jp": "テンプレート",
        "prefix": "TMT",
        "sections": "SECTIONS_TMT",
        "parts": ["tmt_s1_list_folder.S1", "tmt_s2_child_quicktest.S2", "tmt_s3_text_url.S3",
                  "tmt_s4_panel_button.S4", "tmt_s5_quickreply_media.S5",
                  "tmt_s6_legacy_delay_env.S6"],
        "conflicts": "tmt_conflicts",
        "spec": "spec-features/admin/message-template/",
        "sources": [
            "02. TCsLine_Template → tab「Task nhỏ+ check Bug Kh」(08/2023 → 06/2026, 737 dòng, 653 TC lá "
            "— tab MASTER còn sống, 4 cột kết quả theo ticket: Triển khai ngang #35968, "
            "SpecImprove #33326, Bug KH #35871 4/2026, staging)",
            "02. TCsLine_Template → tab「Template button」(2023 → 03/2026, 1619 dòng, 953 TC lá — tab "
            "MASTER của loại パネル・ボタン, cột kết quả theo SpecImprove #36203, Bug KH #35114/#35112, "
            "Bug KH #34923)",
            "02. TCsLine_Template → tab「Improve list template」(12/2023 → 05/2026, 632 dòng, 334 TC lá "
            "— tab MASTER của màn danh sách, cột kết quả Bug KH #36384)",
            "02. TCsLine_Template → tab「Type ảnh」(507 dòng, 400 TC lá — ảnh thường + image map; "
            "Bug #31838 replace [name], Bug #31454 action lặp khi reload trình duyệt)",
            "02. TCsLine_Template → tab「Template type text」(2023 → 10/2025, 420 dòng, 184 TC lá — "
            "cột kết quả Bug #32109 30/9/2025 và Bug #32590 30/10/2025)",
            "02. TCsLine_Template → tab「Modal action」(66 TC) và「Modal act Text」(32 TC) — nhãn hiển "
            "thị của ~33 loại action trong modal và tab 詳細設定",
            "02. TCsLine_Template → tab「Type location」(63 TC — Bug #32364 vị trí bị override bởi "
            "geolocation) ·「Type stamp」(19 TC) ·「Type video」(27 TC) ·「Type audio」(18 TC) · "
            "「Type introduce」(12 TC — loại legacy 紹介文)",
            "02. TCsLine_Template → tab「Preview URL」(15 TC — setting hiển thị preview URL trên LINE) · "
            "「Improve tạo temp」(19 TC — SpecChange #24890 title/description 40/60, SpecChange #24912 "
            "thêm emoji)",
            "02. TCsLine_Template → tab「open url của button image map」(01/2024, 11 TC — ma trận open "
            "url trong/ngoài LINE + エルメで設定したページを開く) ·「Test app」(3 TC — preview/send phía app mobile)",
            "02. TCsLine_Template → tab「Tcs #38987」(08/2026, 40 TC — BỘ TC HỢP NHẤT Bug KH #38987 "
            "(parent #38389): delay message + chuẩn hoá bot_profile_id; đây là tab MỚI NHẤT, đã dùng "
            "format AI 20 cột)",
            "02. TCsLine_Template → tab「Info」(25 dòng) — dùng để xác định NIÊN ĐẠI và truy vết ticket "
            "(08/2023 → 06/2026), không lấy làm TC",
            "TCsLine_Improve chung → tab「Improve template btn + image map」(12 dòng — ma trận multi "
            "action + friend action mở url ngoài/trong LME với 2 kiểu hết hạn; KHÔNG có nội dung ở cột "
            "Expect Result, chỉ có Test Result = OK)",
        ],
        "excluded": [
            "TCsLine_MCP → tab「Template_func」(989 dòng) và「Template_e2e」(60 dòng) — test tầng **MCP "
            "tool** (format phẳng: TC ID | MCP Tool | Category | Scenario | Prompt (Input) | Expected "
            "Tool Call & Params), kiểm `list_templates` / `get_template_detail` / `create_template` chứ "
            "không phải màn テンプレート của LME. ĐỀ XUẤT: tách sheet riêng 'MCP' (giữ nguyên như "
            "FA-012/FA-011/FA-004/FA-015) — **cần bạn xác nhận**",
            "02. TCsLine_Template → tab「Task nhỏ+ check Bug Kh」các dòng r224-r238 (khối「Màn QR landing "
            "— Design QR カラーコード」, 15 TC) — thuộc **FA-009 QR Landing**, là triển khai ngang của "
            "SpecChange #32577 (validate mã màu). Đã giữ 1 TC regression ở nhóm『Panel/Button — mã màu』; "
            "chi tiết để lại cho kho FA-009 — **cần bạn xác nhận**",
            "02. TCsLine_Template → tab「Task nhỏ+ check Bug Kh」các dòng r239-r478 (khối「Màn Form-Answer "
            "— tab 共通デザイン設定 / フォーム編集 / 各種設定」, ~227 TC) — thuộc **FA-011 Form** (đã gom ở tab FA-011). "
            "Cùng đợt triển khai ngang validate mã màu nên nằm chung tab. ĐỀ XUẤT: giữ ở FA-011, không "
            "nhân bản sang đây — **cần bạn xác nhận**",
            "02. TCsLine_Template → tab「ListBug」(1128 dòng) — nhật ký bug UI theo cột Priority/Mô tả/"
            "Ảnh/Status dev, KHÔNG phải test case có kết quả mong đợi",
            "02. TCsLine_Template → tab「Sheet6」(102 dòng — ghi chú「Cách test bản cũ」dạng checklist 1 "
            "cột) và「Sheet7」(173 dòng — bảng đánh dấu tiến độ send test/scenario/degrade/staff/backup "
            "bằng ô 'ok') — bản nháp / bảng theo dõi, không có cấu trúc Main Function / Expect Result",
            "Test infra system → tab「template_testcase」— tab RỖNG (chỉ có 2 dòng: header + 1 dòng "
            "Assignee=NganNT), không có TC nào",
            "TCsLine_AddBot → tab「Template_Onboarding trải nghiệm」(17 dòng) — là **nội dung kịch bản "
            "onboarding** (Trigger/Action/Message của 体験①→④), thuộc FA Add Bot v2 / Onboarding; không "
            "phải TC của màn テンプレート",
            "TCsLine_Improve chung → tab「Improve backup media」·「media config server」·「improve ảnh」· "
            "「Improve upload ảnh lên server dropbox」— khớp keyword 'media/ảnh' nhưng là hạ tầng media "
            "server / Dropbox dùng chung toàn tool, không phải màn template",
            "TCsLine_Server mới → tab「Test media」· Test infra system → tab「Check access media」· "
            "01. TCsLine_Chat1:1 → tab「Send media」— khớp keyword 'media' nhưng thuộc hạ tầng server và "
            "FA-001 Chat 1:1",
            "TCsLine_ModalAction → tab「Thêm emoji vào action text」— emoji của **action text** (SC-004), "
            "không phải ô nội dung template. Phần emoji trong template đã lấy từ「Improve tạo temp」r19 "
            "(SpecChange #24912)",
            "06. TCsLine_Richmenu → tab「Improve richmenu 2023.03」r19-r50 (Button, Image map) — đã được "
            "kho FA-004 liệt vào `excluded` và ghi là「thuộc tính năng Template (FA-010)」. Nội dung này "
            "đã được phủ bởi tab「Template button」và「Type ảnh」của file 02 — **cần bạn xác nhận không "
            "cần đọc lại**",
        ],
    },
    {
        "code": "FA-003", "vi": "Tự động trả lời", "jp": "自動応答",
        "prefix": "RPL",
        "sections": "SECTIONS_RPL",
        "parts": ["rpl_s1_list_folder.S1", "rpl_s2_form_filter.S2", "rpl_s3_keyword.S3",
                  "rpl_s4_schedule_action.S4", "rpl_s5_runtime.S5", "rpl_s6_backup_env.S6"],
        "conflicts": "rpl_conflicts",
        "spec": "spec-features/admin/auto-reply/",
        "sources": [
            "08. TCsLine_AutoReply → tab「Ver1.0」(07/2023 → 07/2026, 199 dòng — tab TC DUY NHẤT của file, "
            "vẫn còn sống, 6 khối ticket: checkbox【〇〇】(07/2023) · Bug KH #32967 keyword rác (12/2025) · "
            "Bug KH #35729 group_open (04/2026) · Task #35989 recover modal action (04/2026) · "
            "Bug KH #38369 ON/OFF nhảy folder (07/2026) · Bug tự detect #38413 keyword 30 ký tự "
            "(07/2026 — khối MỚI NHẤT)",
            "08. TCsLine_AutoReply → tab「Info」(6 dòng) và「ListBug」(3 dòng) — dùng xác định NIÊN ĐẠI và "
            "truy vết bug cũ (2 bug keyword rác khi xóa autoreply/folder), không lấy làm TC",
            "TCsLine_Modal Filter → tab「Sửa filter autoreply」(08/2023, 86 TC lá — ma trận đầy đủ 5 loại "
            "điều kiện lọc: tag 4 ĐK · ステップ 5 ĐK · conversion 2 ĐK · QRコード 4 ĐK · 友だち情報 4 type, "
            "mỗi loại chạy cả khối AND và khối OR. ⚠️ TC ~3 năm tuổi, toàn bộ đã đánh dấu CẦN VERIFY LẠI)",
            "TCsLine_Improve chung → tab「Improve nhỏ」khối AUTO REPLY r542-r563 (Triển khai ngang #37710 — "
            "modal multi action khi action bên trong bị xóa, 7 loại action × 3 case) + r892-r894 (filter bên "
            "trong multi action bị xóa data gốc) + r335-r337 (Bug Tester #33107 — bot A access URL bot B) + "
            "r949-r957 (regression + check staff)",
            "TCsLine_Improve chung → tab「Test bug folder all màn」khối「1. Màn autoreply」r4-r20 "
            "(Bug #32468, 10/2025 — 17 TC modal tạo/sửa folder, ĐÃ TỪNG LỖI chưa clear input)",
            "TCsLine_Improve chung → tab「recover bảng category」r4 (kind=1 ⇒ autoreply, xóa bản ghi map theo "
            "category_id) ·「Phân quyền」(11/2023 — message quyền dùng chung mọi màn, 3 role staff)",
            "TCsLine_JOB → tab「Test callback friend」r3-r17 + r29-r40 (ma trận 8 loại message × có/không "
            "autoreply + đổi domain callback cb.lmes.jp → cb-2.lmes.jp)",
            "TCsLine_JOB → tab「Test fix bug KH」khối Bug #31873 r144-r235 (14/09/2025 — 自動確認済み + action "
            "của autoreply với status chat / block / ẩn / bookmark; user bị bot block r218-r226) và r39 "
            "(対象人数 của autoreply)",
            "TCsLine_JOB / TCsLine_Improve chung → tab「Send msg reply token」r11 (auto reply dùng reply token "
            "— corpus KHÔNG ghi kết quả mong đợi, đã tự viết theo BR-21)",
            "TCsLine_BackUp → tab「Backup (job)」r2-r22 và「Backup 1.0」r3-r23 (21 TC khối『1. Autoreply』: "
            "folder / keyword / time action / active-block friend / 10 loại action / filter / ON-OFF. "
            "Backup 1.0 có 10 cột kết quả theo 10 đợt backup — nguồn xác định các điểm ĐÃ TỪNG NG)",
            "15.3 TCsLine_ChangeBot → tab「Change bot」r200-r201 (giữ keyword + setting action sau change bot; "
            "friend mới gửi keyword hợp lệ vẫn nhận action)",
            "16. TCsLine_ErrorList → tab「improve 28/11」r256-r279 (Send action callback: Autoreply — send text "
            "/ template / cả hai, ma trận retry 1p/2p/5p × success/fail) + r430-r434 (action callback bot FREE, "
            "template rỗng → mã lỗi 006)",
            "01. TCsLine_Chat1:1 (Improve 10/2024) → tab「AI_TCs_Setting_chat_v1」r105-r108 (BS_032 — 2 checkbox "
            "自動確認済み riêng cho 自動応答 [すべてのメッセージに反応] và [設定したキーワードに反応]) + "
            "tab「Content: Hiển thị msg」r242-r243 / r322-r323 / r1117-r1118 / r1189-r1190 / r1195 / r1210 "
            "(trigger 自動応答 ở chat 1:1, quote message, start/stop scenario từ auto reply)",
            "TCsLine_ModalAction → tab「Update tên action」r45 (04/2025 — dòng『auto reply』của ma trận đổi tên "
            "action) ·「Support name」r9+r16 (12/2023 — auto reply trong danh sách send từ job) · "
            "「Thêm option random cho action friend infor point」r30/r72/r99 (11/2023 — dòng『autoreply』) · "
            "「Improve action 1.0」r7-r9 (02/2023 — start/stop scenario từ auto reply)",
        ],
        "excluded": [
            "08. TCsLine_AutoReply → tab「Ver1.0」r122-r172 (khối『CHECK TRIÊN KHAI NGANG CÁC MÀN KHÁC』, "
            "51 dòng TC-YOKO-01 → TC-YOKO-50) — triển khai ngang bug #38369 sang **7 màn KHÁC**: FA-005 Rich "
            "Menu Image Maker · FA-025 Conversion · FA-015 Friend Information · FA-016 Action Schedule · "
            "FA-021 Event Booking v2 · FA-026 商品販売 · FA-024 Cross Analysis. Nội dung là thao tác folder của "
            "các màn đó, KHÔNG phải màn 自動応答. ĐỀ XUẤT: đưa vào kho của từng tính năng tương ứng — "
            "**cần bạn xác nhận**",
            "08. TCsLine_AutoReply → tab「Ver1.0」r173 (『Check user đăng ký ⇒ add bot thành công』) — thuộc "
            "luồng đăng ký / add bot, không phải auto reply",
            "TCsLine_MCP → tab「Auto-reply_func」(144 hit) ·「Auto-reply_e2e」(45 hit) ·「16.Auto Reply」(34 hit) "
            "·「Msg validate」— test tầng **MCP tool** (list_autoreply / get_autoreply_detail / "
            "change_status_autoreply / get_autoreply_reply_history), KHÔNG phải màn 自動応答 của LME. Giữ nguyên "
            "tiền lệ FA-012/FA-011/FA-004/FA-015/FA-009/FA-026 — đề xuất tách sheet riêng 'MCP'. "
            "**★ CẦN BẠN XÁC NHẬN** — riêng với FA-003 đây là nguồn LỚN NHẤT (266 hit), lớn hơn cả tab master, "
            "nên nếu bạn muốn gộp thì kho này sẽ đổi khá nhiều",
            "TCsLine_Detail_Friend → tab「Trigger action」r180-r187 (hiển thị text trigger 自動応答 "
            "[すべてのメッセージに反応] / [設定したキーワードに反応] ở modal trigger) và r583+ (lịch sử friend info từ "
            "action friend info tại auto-reply, ~76 hit) — điểm quan sát là **màn 友だち詳細 (FA-014)**, có spec "
            "riêng `spec-features/admin/detail-friend/`. Giữ nguyên tiền lệ FA-015 (đã loại toàn bộ file này). "
            "**★ CẦN BẠN XÁC NHẬN** — nếu muốn phủ output cuối của action friend info thì nên bổ sung vào kho FA-014",
            "TCsLine_Notify setting → tab「02. Setting notify」r348-r368 (thêm 2 option notify: "
            "自動応答 [すべてのメッセージに反応] のメッセージ / [設定したキーワードに反応] のメッセージ) và "
            "tab「03. Push, list noti」r29-r31 (push notify khi message thỏa mãn auto reply) — điểm quan sát là "
            "**màn 通知設定 và app mobile**, thuộc `spec-features/admin/notify-setting/`. **★ CẦN BẠN XÁC NHẬN**",
            "TCsLine_AddBot → tab「[AI] Onboarding trải nghiệm_v2」·「[AI] Onboarding (staging 07-06)」·"
            "「[AI] Onboarding trải nghiệm」·「[AI] TCs_flow (staging 07-14)」(69 hit) — kịch bản onboarding tự "
            "động tạo sẵn auto reply mẫu cho bot mới, thuộc **FA Add Bot v2 / Onboarding**, không phải màn 自動応答",
            "TCsLine_Data warehouse (51 hit) — bảng đối chiếu schema / sync data (Sheet13/15/18, Table xoá data, "
            "Matrix_Screen), là tài liệu hạ tầng dữ liệu chứ không phải test case có kết quả mong đợi",
            "TCsLine_Improve chung → tab「Improve nhỏ」r564-r948 (các khối #37710 của Template IMG map / scenario "
            "/ Template Button / Remind / Tag / Richmenu / Friend info / QR landing / Salon / Lesson / Bill item "
            "/ Events / Conversion / Kết bạn thường / Broadcast / Action Schedule / Form answer) — cùng đợt "
            "triển khai ngang nhưng điểm quan sát là màn của tính năng khác; chỉ lấy khối AUTO REPLY r543-r563 "
            "và r892-r894",
            "TCsLine_Improve chung → tab「Improve nhỏ」r365-r405 (SpecImprove #33297 xóa hiển thị plan type trên "
            "header — dòng r368『Auto reply』chỉ là 1 ô trong ma trận ~40 màn, nội dung thuộc header/menu)",
            "TCsLine_Improve chung / TCsLine_JOB → các tab TRÙNG gid (Test callback friend gid=1706615087, "
            "Send msg reply token gid=1620919708, Improve nhỏ gid=703112589, Test fix bug KH gid=1396622666) — "
            "2 file dùng CHUNG spreadsheet nội dung; chỉ đọc bản có nhiều dòng hơn để tránh nhân đôi TC",
            "16. TCsLine_ErrorList → tab「improve 28/11」r471-r491 (Check send message bởi job case lỗi không "
            "xác định — dev sửa code để tái hiện lỗi) — là quy trình test nội bộ của dev, không phải TC vận hành; "
            "phần auto reply đã lấy ở r256-r279",
            "02. TCsLine_Template · 10.1 TCsLine_Tag · 10.2 TCsLine_friend_information · 06. TCsLine_Richmenu · "
            "07. TCsLine_Form Answer · 04. TCsLine_Scenario · TCsLine_Header/Menu · TCsLine_QLStaff · "
            "13.1 TCsLine_URL analysis · TCsLine_Admin · TCsLine_Server mới · TCsLine_summary-message-send · "
            "TCsLine_Bill tiền · Info DB chung · Test infra system — đã quét NỘI DUNG toàn bộ 57 file "
            "(1 batchGet/file), các file này chỉ NHẮC TỚI auto reply như 1 ô trong ma trận triển khai ngang hoặc "
            "1 điều kiện tiền đề, KHÔNG có khối TC nào của màn 自動応答",
        ],
    },
    {
        "code": "FA-033", "vi": "Backup", "jp": "データコピー",
        "prefix": "BK",
        "sections": "SECTIONS_BK",
        "parts": ["bk_s1_screen.S1", "bk_s2_job.S2", "bk_s3_copy_msg.S3",
                  "bk_s4_copy_data.S4", "bk_s5_copy_analytics.S5", "bk_s6_media_env.S6"],
        "conflicts": "bk_conflicts",
        "spec": "spec-features/admin/backup/ (⚠️ spec chốt 2026-03-30 tả GIAO DIỆN CŨ — xem MT-00)",
        "sources": [
            "TCsLine_BackUp → tab「Backup 1.0」(03/2023 → 07/2026, 330 dòng — tab master còn sống, "
            "13 cột kết quả theo từng bot; 3 đợt bổ sung mới: Bug #32413 + #32414 (20/10/2025), "
            "「Validate backup không backup chính bot đó」(02/02/2026), Bug tự detect #38411 (07/2026))",
            "TCsLine_BackUp → tab「Backup (job)」(05/2023 → 05/2026, 399 dòng — tab master thứ 2, chủ đề "
            "chuyển backup sang job nền; khối「2.1 Richmenu (Improve 10/2025)」r54-r120 là bản MỚI NHẤT của "
            "richmenu, thay thế r23-r53; cột Bug Tester #36322 (05/2026 — step_message start_time ≥ 24h))",
            "TCsLine_BackUp → tab「[AI]UI TCs」(2026, 72 dòng — TC-BK-001…033 theo bộ màn MỚI SCR-01…SCR-07, "
            "kèm khối「Các case bổ xung」r35-r42 và khối Comment 6/7 r43-r47 là bản mới nhất về plan Free)",
            "TCsLine_BackUp → tab「[AI]API TCs」(2026, 29 dòng — TC-BK-034…061 cho EP-01…EP-05, "
            "trong đó EP-04 GET /ajax/backup-status/{id} và EP-05 POST /ajax/reissue-transfer-code là ENDPOINT MỚI)",
            "TCsLine_BackUp → tab「[MN]Job TCs」(2026, 112 dòng — 2 phần: r2-r9 là TC job nền TC-BK-062…076 "
            "dạng phẳng; r12-r112 là khối cây「1. Check back cross」+「2. Check back up csv」theo "
            "SpecImprove #34158 (04/2026 — thêm CSV管理・クロス分析 vào phạm vi copy))",
            "TCsLine_BackUp → tab「improve url image」(31/10/2024 → 24/08/2025, 42 dòng — ma trận media "
            "theo đường dẫn ảnh cũ/mới; bản MỚI NHẤT, thay thế tab「Backup image」)",
            "TCsLine_BackUp → tab「Backup image」(≤2024, 43 dòng — bản CŨ của ma trận media; giữ lại vì "
            "có kết quả NG cho video-thumbnail mà bản mới không đo lại, xem MT-24)",
            "TCsLine_Improve chung → tab「Improve backup media」(24/01/2024, 146 dòng — đợt chuyển media "
            "sang server khác; là nguồn DUY NHẤT liệt kê đủ 8 nhóm media KHÔNG được copy. "
            "⚠️ Đã 2 năm 7 tháng — CẦN VERIFY LẠI)",
        ],
        "excluded": [
            "TCsLine_Improve chung → tab「Improve nhỏ」r406-r484 (Bug Tester #34318 —「Triển khai ngang: sửa "
            "path folder dùng admin của bot cho case upload, copy media」, Info r54) — điểm quan sát là màn "
            "upload media của từng tính năng chứ không phải màn データコピー. ĐỀ XUẤT: gom khi chạy "
            "/collect-tcs cho tính năng media/server — HỎI USER XÁC NHẬN",
            "TCsLine_Improve chung → tab「chang từ dùng link dropbox sang path」(19/04/2024) · "
            "「Improve upload ảnh lên server dropbox」·「Upload ảnh dropbox」(01/07/2023) · "
            "「media config server」(04/01/2024) — thuộc tầng hạ tầng lưu trữ media, backup chỉ là 1 trong "
            "nhiều nơi bị ảnh hưởng. ĐỀ XUẤT: tách feature riêng『Hạ tầng media』— HỎI USER XÁC NHẬN",
            "15.3 TCsLine_ChangeBot (5 tab) và TCsLine_AddBot (11 tab) — đổi bot / thêm bot là tính năng KHÁC "
            "(spec-features/admin/bot-add-v2/), tuy cùng nhóm『システム管理関連』. Corpus backup có nhắc "
            "「Check khi bot đang backup > đổi bot」nhưng đó là 1 TC của backup, đã đưa vào tab này",
            "TCsLine_MCP (45 tab) — test tầng công cụ MCP chứ không phải màn admin của LME. "
            "ĐỀ XUẤT: tách sheet riêng『MCP』(giữ nguyên đề xuất như FA-012 / FA-011 / FA-001) — HỎI USER XÁC NHẬN",
            "TCsLine_BackUp → tab「Info」— nhật ký niên đại của file, đã dùng để xác định thứ tự ưu tiên "
            "giữa các tab, không phải test case",
            "Backup (job) r280-r308 (28 dòng chi tiết TC popup) — popup đã bị tắt khỏi phạm vi copy "
            "(r280:「tạm thời không backup nữa」, db-mapping.md:415 `is_enable=0`). Kho chỉ giữ 2 TC xác nhận "
            "KHÔNG copy. ĐỀ XUẤT giữ nguyên như vậy — xem MT-22, HỎI USER XÁC NHẬN",
            "[MN]Job TCs r54-r57 (validate tên file CSV khi TẠO MỚI) — thuộc màn CSV管理 chứ không phải "
            "hành vi copy. Kho giữ lại 1 TC hồi quy vì corpus xếp nó trong khối backup — HỎI USER XÁC NHẬN",
        ],
    },
    {
        "code": "FA-019", "vi": "Đặt lịch bài học", "jp": "レッスン予約",
        "prefix": "LSN",
        "sections": "SECTIONS_LSN",
        "parts": ["lsn_s1_list_course.S1", "lsn_s2_course_detail.S2", "lsn_s3_calendar_view.S3",
                  "lsn_s4_reception.S4", "lsn_s5_booking_ops.S5", "lsn_s6_setting.S6",
                  "lsn_s7_remind_page.S7", "lsn_s8_payment.S8", "lsn_s9_lineuser.S9", "lsn_s10_gap.S10"],
        "conflicts": "lsn_conflicts",
        "spec": "spec-features/admin/lesson-booking/ (ĐẠT có điều kiện · 47 màn · 114 endpoint · "
                "93 business rule · TOP-12 rủi ro trong đó 6 mức Nghiêm trọng · 13 Gap chưa xác minh)",
        "sources": [
            "11.2 TCsLine_LessonCalendar → tab「Setting calendar」(05/2024 → 05/2026, 1610 dòng, "
            "1130 TC lá — tab LỚN NHẤT; toàn bộ 全体設定: メッセージ・アクション, 予約の開始・締切, "
            "1人あたりの予約上限, 質問項目 (+ bộ Create/Edit Form redmine #29272), リマインド "
            "(SpecImprove #36037 · SpecChange #32367 · Support #33648), 空き枠通知 (Bug KH #36729 05/2026 "
            "— KHỐI MỚI NHẤT), 予約ページ表示設定 & filter, トップ・店舗情報・利用規約, 予約システムの削除, "
            "Googleスプレッドシート連携 (Bug #31595 · Support #32733); 23 cột ticket)",
            "11.2 TCsLine_LessonCalendar → tab「Quản lý calendar_new」(1056 dòng, 478 TC lá — mô tả "
            "GIAO DIỆN MỚI: tuần có 2 view コース別/一覧, modal edit slot, xóa nhiều slot 一括削除, "
            "sort history mới nhất lên đầu; khớp ui-spec.md:1264 và BR-17 — xem MT-11)",
            "11.2 TCsLine_LessonCalendar → tab「Quản lý calendar」(1072 dòng, 460 TC lá — tab master "
            "còn cột ticket MỚI NHẤT: Support #32704 11/2025 · Bug #29484 04/2025 · Feature #27978 01/2025 · "
            "Bug #26943 10/2024; chứa riêng khối Test security và Feature #26528 hiển thị bill tiền — "
            "xem MT-11)",
            "11.2 TCsLine_LessonCalendar → tab「Booking phía line user」(576 dòng, 395 TC lá, "
            "05/2024 → 07/2026 — toàn bộ luồng LIFF: entry × trạng thái kết bạn (Bug #31477), "
            "chọn course/slot (SpecImprove #32808 · #32884 · #32887), form & timeout (SpecImprove #32567), "
            "lịch sử & xóa booking chờ hủy (Feature #35707), hủy (SpecChange #32646), "
            "ẩn text bill tiền (Feature #31268), race condition Bug KH #38280 06/2026 kèm 11 TC "
            "dạng AI NEW-*/RV-* — KHỐI MỚI NHẤT của tab)",
            "11.2 TCsLine_LessonCalendar → tab「Task nhỏ + fix bug KH」(199 dòng, 126 TC lá — "
            "sửa logic booking có bill tiền giống event booking · Review #29331 tuần/tháng có lịch làm việc · "
            "Support #29830 nhập 24h · Bug #30002 ưu tiên action course · retry sync Google · "
            "Bug KH #35173 03/2026 add slot lệch ngày)",
            "11.2 TCsLine_LessonCalendar → tab「Sửa bill tiền univapay」(173 dòng, 143 TC lá, "
            "2025 → 06/2026 — callback/webhook 2 pha, khóa thao tác theo status_webhook, metadata bot_id, "
            "bill kiểu cũ + job 15 phút, SpecImprove #34857, Bug Tester #38077 06/2026)",
            "11.2 TCsLine_LessonCalendar → tab「Quản lý course」(226 dòng, 129 TC lá — CRUD course, "
            "action/filter cấp course, Bug KH #34561 02/2026, Support #27091 11/2024, Feature #27496)",
            "11.2 TCsLine_LessonCalendar → tab「Liên kết bill tiền」(135 dòng, 100 TC lá — setting "
            "決済連携 + ma trận 11 luồng × Stripe/UnivaPay × test/product)",
            "11.2 TCsLine_LessonCalendar → tab「Calendar list」(63 dòng, 56 TC lá — màn list + wizard "
            "tạo calendar + giới hạn theo plan)",
            "11.2 TCsLine_LessonCalendar → tab「Today&NewBooking」(65 dòng, 45 TC lá — spec change "
            "8/10/2024 dùng user_update_time)",
            "11.2 TCsLine_LessonCalendar → tab「Improve bill tiền stripe」(61 dòng, 41 TC lá — "
            "tạo order trước khi thu tiền, job quét kết quả, SpecImprove #34857 03/2026)",
            "11.2 TCsLine_LessonCalendar → tab「Message error」(52 dòng — bảng đối chiếu message lỗi "
            "VN/JP, dùng làm nguồn text cho cột Kết quả mong đợi, không phải TC)",
            "11.2 TCsLine_LessonCalendar → tab「Fill msg default」(31 dòng — 4 mẫu message mặc định) · "
            "「Pattern-history」(17 dòng — bảng ánh xạ thao tác ↔ nội dung lịch sử) · "
            "「Ngần check_step」(59 dòng — ma trận coverage theo màn, KHÔNG có kết quả mong đợi, "
            "dùng đối chiếu độ phủ) ·「Improve lesson」(7 dòng, ma trận count booking khi xóa friend)",
            "TCsLine_Improve chung → tab「add link salon và lesson」(82 dòng, 8 TC lá — Support #26549 "
            "08/2024: chèn link booking/lịch sử lesson vào template, send all, scenario, remind, rich menu)",
        ],
        "excluded": [
            "TCsLine_Booking Calendar (TOÀN BỘ FILE, 12 tab) — đây là hệ 予約管理 THẾ HỆ CŨ, đã bị "
            "Feature #30540 (07/2025) GỠ KHỎI TOOL và Feature #28419 chặn tạo slot mới từ 01/04/2025; "
            "tab「Redirect sang calendar mới」(08/2024) xác nhận đã redirect sang salon/lesson. "
            "spec-features §1.4 cũng loại `b_c_*` / `booking_calendar` khỏi phạm vi FA-019. "
            "ĐỀ XUẤT: archive cả file — HỎI USER XÁC NHẬN",
            "TCsLine_MCP → tab「18. Lesson」(104 dòng, 61 TC lá — test 3 MCP tool "
            "`list_lesson_calendars` / `get_lesson_calendar_detail` / `get_lesson_calendar_bookings`: "
            "bearer token, bot_id, phân trang, schema response). Đây là test TẦNG MCP TOOL, "
            "KHÔNG phải màn admin/LIFF của LME. ĐỀ XUẤT: tách sheet riêng『MCP』chung với 8.Tags / "
            "17. Salon / 9.Friend_info… — HỎI USER XÁC NHẬN",
            "TCsLine_Limit all tính năng → tab「Limit Lesson」— tab RỖNG (0 dòng, 0 ô có dữ liệu), "
            "không dùng được",
            "11.2 TCsLine_LessonCalendar → tab「Info」(nhật ký ticket, dùng xác định niên đại) · "
            "「BugComment」「BugUI」「BugLogic」「Q&A」(nhật ký bug và hỏi đáp, không phải test case)",
            "Spreadsheet `1zVpYexiqtNV6E_j5gDaPFg-YrAtVJnqSGUzzLCxa_Ss` — bản COPY CŨ của chính file "
            "11.2 (dùng CÙNG bộ gid: 1974520139 Setting calendar · 461872290 Quản lý calendar · "
            "2021990578 Booking phía line user · 110079709 Sửa bill tiền univapay…). "
            "Toàn bộ link trong tab Info từ 05/2026 trở đi đã chuyển sang file 1337DD hiện hành. "
            "Service account không đọc được file này (403/503) nhưng nội dung đã nằm trong file mới",
            "TCsLine_JOB · TCsLine_QLStaff · TCsLine_Modal Filter · TCsLine_ModalAction · "
            "TCsLine_Test Limit theo plan — đã rà toàn bộ danh sách tab, KHÔNG có tab nào dành riêng "
            "cho màn レッスン予約",
        ],
    },
    {
        "code": "FA-020", "vi": "Đặt lịch salon", "jp": "サロン・面談予約",
        "prefix": "SLN",
        "sections": "SECTIONS_SLN",
        "parts": ["sln_s1_list_create.S1", "sln_s2_booking_mgmt.S2", "sln_s3_shift.S3",
                  "sln_s4_course_staff.S4", "sln_s5_setting.S5", "sln_s6_google.S6",
                  "sln_s7_payment.S7", "sln_s8_lineuser.S8"],
        "conflicts": "sln_conflicts",
        "spec": "spec-features/admin/salon-booking/ (confidence Cao 75% · 3 vấn đề Trung bình · 10 open questions)",
        "sources": [
            "11.1 TCsLine_SalonCalendar → tab「Quản lý calendar」(07/2024 → 07/2026, 6179 dòng, 4097 TC lá "
            "— tab MASTER lớn nhất, 9 cột ticket: Bug #34667 · Bug Tester #34185 · SpecImprove #33147 · "
            "Bug #32775 · SpecChange #32679 · Bug #32568 · Support #32704 · Bug KH #36938; chứa cả "
            "Feature #27976 スタッフ自動割り当て (01/2025), Review #29803 lịch sử change staff, "
            "Bug #29918/#30555 điều kiện staff khả dụng, ma trận 受付上限 r3369-r6179)",
            "11.1 TCsLine_SalonCalendar → tab「Setting calendar」(07/2024 → 05/2026, 2013 dòng, 1482 TC lá "
            "— toàn bộ tab 予約設定: メッセージ・アクション, 開始・締切, 質問項目, リマインド (SpecImprove #36037), "
            "空き枠通知, トップ・店舗情報・利用規約, システムワード, 予約ページの非表示, Googleスプレッドシート連携, 予約システムの削除)",
            "11.1 TCsLine_SalonCalendar → tab「Booking phía line user」(07/2024 → 07/2026, 1436 dòng, "
            "1191 TC lá — toàn bộ luồng LIFF: entry × trạng thái kết bạn, chọn course/staff/slot, form, "
            "lịch sử & copy, hủy, verify API, Bug KH #38280 race condition, Bug tự detect #38629)",
            "11.1 TCsLine_SalonCalendar → tab「Sync google calendar」(09/2024 → 07/2026, 634 dòng, 440 TC lá "
            "— Bug #26653 · #26739 · #28770 · #29169 · #29844 · #30419 · Bug KH #35312 · Support #35768 · "
            "Bug tự detect #38446)",
            "11.1 TCsLine_SalonCalendar → tab「Quản lý course&staff」(07/2024 → 06/2026, 705 dòng, 458 TC lá "
            "— コース/スタッフ CRUD, menu nhóm, hard limit 200/200/100 (08/2025), Feature #27496 OFF course/staff, "
            "Bug Tester #34656)",
            "11.1 TCsLine_SalonCalendar → tab「Calendar list」(07/2024 → 2025, 332 dòng, 228 TC lá — màn list "
            "calendar + toàn bộ wizard 4 bước + giới hạn plan)",
            "11.1 TCsLine_SalonCalendar → tab「#38520」(07/2026, 102 dòng, 99 TC format phẳng AI — Bug KH "
            "#38519/#38520/#38537 ca chạm nửa đêm; KHỐI MỚI NHẤT, bao phủ thêm phân quyền staff, LIFF entry, "
            "multi-tenant, audit log, release, dữ liệu cũ)",
            "11.1 TCsLine_SalonCalendar → tab「Liên kết bill tiền」(305 dòng, 232 TC lá) ·「Improve bill tiền "
            "univapay」(170) ·「Improve bill tiền stripe」(72) ·「Bill tiền Univapay(#32856)」(78)",
            "11.1 TCsLine_SalonCalendar → tab「Test limit booking_V4_2」(02/2026, 257 TC lá — bộ 受付上限 "
            "MỚI NHẤT, gồm SpecImprove #34506 và thay đổi「option limit 3 count cả booking ngoài giờ lv」)",
            "11.1 TCsLine_SalonCalendar → tab「Task nhỏ + test fix bug kh」(666 TC lá) ·「SpecImprove #33408」"
            "(424, improve performance 01/2026) ·「Main case」(62, logic tuần/tháng phía LINE user) ·"
            "「Today&NewBooking」(39) ·「#30919」(53) ·「Check middle ware」(14) ·「Setting lịch lv」(9) ·「Staff」"
            "(bảng liệt kê màn con để test acc staff, không có kết quả)",
        ],
        "excluded": [
            "11.1 TCsLine_SalonCalendar → tab「Test limit booking」(157 TC lá) ·「Test Limit booking_V2」(722) ·"
            "「Test limit booking_V3_9/2025」(2631) ·「Test limit booking_V4_11/2025」(~600) — 4 phiên bản CŨ của "
            "cùng bộ ma trận 受付上限, đã bị「Test limit booking_V4_2」(02/2026) thay thế. Kho giữ V4_2 + các khối "
            "限界 trong「Quản lý calendar」. ĐỀ XUẤT giữ nguyên — HỎI USER XÁC NHẬN",
            "11.1 TCsLine_SalonCalendar → tab「BugLogic」(934 dòng) ·「Bug comment」(334) ·「BugUI」(229) ·"
            "「Q&A」(115) — nhật ký bug và hỏi đáp, không phải test case có kết quả mong đợi",
            "11.1 TCsLine_SalonCalendar → tab「Message error」(52 dòng) — bảng tra cứu text validate (VN ↔ JP), "
            "là dữ liệu tham chiếu. ĐỀ XUẤT: dùng làm nguồn đối chiếu message khi Leader chốt MT-23/MT-26/MT-31",
            "11.1 TCsLine_SalonCalendar → tab「Info」(nhật ký niên đại) ·「Trang tính14」(23 dòng nháp) — "
            "đã dùng để xác định thứ tự ưu tiên giữa các tab, không phải test case",
            "11.2 TCsLine_LessonCalendar (8 tab) — レッスン予約 là TÍNH NĂNG RIÊNG "
            "(spec-features/admin/lesson-booking/), tuy dùng chung nhiều logic (event_step_time, "
            "NewEventRemindTask, ma trận 受付上限). ĐỀ XUẤT: chạy /collect-tcs riêng cho Lesson — HỎI USER XÁC NHẬN",
            "TCsLine_Booking Calendar (10 tab, 2023 → 07/2025) — tính năng calendar booking CŨ, đã bị "
            "「Feature #30540: Bỏ tính năng calendar booking cũ khỏi tool」(7/2025) gỡ khỏi tool; tab "
            "「Redirect sang calendar mới」(08/2024) là luồng chuyển đổi sang salon/lesson. ĐỀ XUẤT: KHÔNG gom "
            "vì tính năng đã bị gỡ — HỎI USER XÁC NHẬN nếu vẫn cần TC hồi quy cho redirect",
            "TCsLine_Improve chung → tab「add link salon và lesson」(1020 dòng) — nội dung là chèn LINK đặt lịch "
            "vào các tính năng khác (template, richmenu, auto-reply…), thuộc các feature đó chứ không phải màn "
            "salon. Kho chỉ giữ 1 TC LIFF entry「mở link từ button / image map / rich menu」— HỎI USER XÁC NHẬN",
            "TCsLine_Limit all tính năng → tab「Limit Salon」(03/2026) — đã đối chiếu và hợp nhất vào nhóm "
            "「Giới hạn theo plan」; không giữ riêng",
            "TCsLine_QLStaff (6 tab) — 管理スタッフ (tài khoản phụ của tool), KHÁC với スタッフ của salon. "
            "Có spec riêng spec-features/admin/staff-management/. ĐỀ XUẤT: chạy /collect-tcs riêng — "
            "HỎI USER XÁC NHẬN",
            "TCsLine_MCP → tab「17. Salon」(999 dòng, format phẳng TC ID | MCP Tool | Category | Scenario) — "
            "test tầng công cụ MCP chứ không phải màn salon của LME. ĐỀ XUẤT: tách sheet riêng『MCP』"
            "(giữ nguyên đề xuất như FA-012 / FA-011 / FA-001 / FA-033) — HỎI USER XÁC NHẬN",
            "06. TCsLine_Richmenu → tab「Sử dụng liff app booking」(02/2024) — thuộc feature Rich Menu, "
            "đã được gom ở tab FA-004",
        ],
    },
    {
        "code": "FA-007", "vi": "Setting add friend", "jp": "あいさつメッセージ",
        "prefix": "SAF",
        "sections": "SECTIONS_SAF",
        "parts": ["saf_s1_screen.S1", "saf_s2_message.S2", "saf_s3_action.S3",
                  "saf_s4_testtab.S4", "saf_s5_runtime.S5", "saf_s6_landing.S6",
                  "saf_s7_job_env.S7"],
        "conflicts": "saf_conflicts",
        "spec": "spec-features/admin/setting-add-friend/ (chốt 2026-05-22, confidence Cao ~85% · "
                "0 vấn đề nghiêm trọng · 8 gap · 5 open question — ⚠️ KHÔNG có tùy chọn "
                "「あいさつメッセージを稼働させる」 của QRコードアクション, xem MT-01/MT-02)",
        "sources": [
            "05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」(gid=857271843, 05/2025 → "
            "03/2026, 407 dòng — TAB MASTER còn sống. Cấu trúc: 3 khối theo 3 trang (Msg Kết bạn new friend "
            "r3-r116 · Msg Kết bạn old friend r117-r254 · Msg lúc xóa block r255-r347) + khối improve "
            "流入経路/友だち追加URL r348-r393 + khối Bug Tester #33322 r394-r407. Ma trận 13 case landing × "
            "loại action nằm ở r205-r252)",
            "05. TCsLine_Setting kết bạn → tab「Improve setting add fr 1.0」(gid=1908008414, 04/2023, "
            "22 dòng — đợt improve đầu, phần lớn đã bị tab 2.0 thay thế; còn dùng cho nút 保存 (r20-r22) và "
            "text hướng dẫn test của trang 既存友だち用 (r18). Xem MT-04, MT-12)",
            "05. TCsLine_Setting kết bạn → tab「Ngần review」(3 dòng — 2 câu hỏi treo của Leader về "
            "action loại テキスト, xem MT-16)",
            "05. TCsLine_Setting kết bạn → tab「Info」(niên đại: 04/2023 improve 1.0 · 05/2025 "
            "improve 2.0 · 06/2025 + 07/2025 comment design · 03/2026 Bug Tester #33322)",
            "TCsLine_JOB (= TCsLine_Improve chung) → tab「Test callback friend」(11/2025 → 08/2026, "
            "410 dòng — CHỈ lấy phần callback follow/unfollow/unblock: r30-r33, r53-r56, r162-r165, r171, "
            "r180, r184-r197, r216-r218, r245-r264, r379-r388, r410. 4 cột ticket: Feature #38620 · Bug tự "
            "detect #38694 · Bug KH #38447 · SpecImprove #36986)",
            "15.3 TCsLine_ChangeBot → tab「Change bot」(r206-r207 giữ nguyên setting sau đổi bot · "
            "r217-r218 landing cũ/mới · r242-r249 3 gói free/standard/pro)",
            "TCsLine_QLStaff → tab「Improve 7/10/2024」 r82-r83 và tab「Comment Improve staff "
            "(logic) 28/10/2024」 r154-r155 (mục『setting add friend — tạo/edit』; r83 kết quả NG ở dev)",
            "TCsLine_Improve chung → tab「Phân quyền」(r4-r34 — nội dung thông báo chuẩn khi màn "
            "không được cấp quyền, áp chung cho toàn tool)",
        ],
        "excluded": [
            "TCsLine_MCP → tab「Setting-add-friend_func」(1000 dòng) và「Setting-add-friend_e2e"
            "」(1000 dòng) — test tầng MCP tool (get_welcome_message / update_welcome_message) chứ không "
            "phải màn admin của LME. ĐỀ XUẤT: tách sheet riêng『MCP』(giữ nguyên đề xuất như FA-012, FA-011, "
            "FA-001) — HỎI USER XÁC NHẬN",
            "09. TCsLine_QR Landing → tab「Improve 1.0」(4212 dòng) và「job+ check count」"
            "(1294 dòng) — thuộc FA-017 QRコードアクション, có màn riêng. Ở FA-007 chỉ giữ phần GIAO của 2 tính "
            "năng (thứ tự chạy action, tùy chọn kích hoạt あいさつメッセージ) lấy từ tab master của FA-007. "
            "ĐỀ XUẤT: gom khi chạy /collect-tcs cho FA-017",
            "TCsLine_JOB → tab「Test callback friend」 phần callback message/postback/richmenu/"
            "imagemap (r3-r27, r37-r52, r60-r75, r199-r215, r234-r244) — thuộc FA-001 Chat 1:1 và FA-003 Tự "
            "động trả lời, đã hoặc sẽ gom ở feature tương ứng",
            "05. TCsLine_Setting kết bạn → tab「ListBug」(1 dòng) và「Sheet3」(rỗng) — "
            "không phải test case",
            "15.3 TCsLine_ChangeBot → phần còn lại của tab「Change bot」(r1-r205, r208-r241, "
            "r250-r317) — thuộc FA-038 Cài đặt kết nối LOA / quy trình đổi bot",
        ],
    },
    {
        "code": "FA-013", "vi": "Friend list", "jp": "友だちリスト",
        "prefix": "FRL",
        "sections": "SECTIONS_FRL",
        "parts": ["frl_s1_list_display.S1", "frl_s2_search.S2", "frl_s3_filter_select.S3",
                  "frl_s4_bulk_action.S4", "frl_s5_result_job.S5",
                  "frl_s6_subscreens_delete.S6", "frl_s7_sync_perm.S7"],
        "conflicts": "frl_conflicts",
        "spec": "spec-features/admin/friend-list/ (chốt 2026-03-25, cross-check 64/64, 0 vấn đề "
                "nghiêm trọng — nhưng 11 Gaps, trong đó #1 (danh sách action của nút アクション選択), "
                "#2 (cơ chế ẩn bạn bè) và #7 (phân quyền staff) đều được TC lấp: xem MT-09/MT-10/MT-12)",
        "sources": [
            "10.3 TCsLine_Friendlist → tab「Testcase」(02/2026 → 07/2026, 182 dòng, 143 TC lá — TAB MASTER "
            "còn sống, 6 cột ticket: SpecImprove #34438 (02/2026) · SpecImprove #34720 (03/2026) · "
            "Bug KH #35071 (03/2026) · SpecImprove #35389 (04/2026) · Bug tự detect #38390 (07/2026) · "
            "Bug KH #38866 (07/2026). Nội dung: 友だち一括アクション (ngưỡng 200, action schedule, 13 loại "
            "action, trigger + profile gửi), last_message & bộ đếm 未確認, xoá friend + cascade)",
            "10.3 TCsLine_Friendlist → tab「#38866」(07/2026, 75 dòng, 70 TC lá — TAB MỚI NHẤT. Bug KH "
            "[16-07-2026][T11593]: lọc「6期生」chọn đúng 312 người nhưng action gắn tag lại áp cho toàn bộ "
            "4.500 người. Phủ: search theo tên/システム表示名/email, ký tự đặc biệt, dấu cách half & "
            "full-width, ký tự tiếng Nhật, thao tác Enter, 2 checkbox 全選択 + 条件に当てはまる友だち{N}人全員を選択)",
            "TCsLine_Improve chung → tab「ESticsearch」(r4 xoá friend · r48 trạng thái scenario · "
            "r89 block friend · r283 bỏ ẩn friend — 4 dòng thuộc màn friendlist; các dòng còn lại thuộc "
            "chat 1:1 / 友だち情報)",
            "TCsLine_Improve chung → tab「Improve nhỏ」(r379 header không hiện gói giá với staff · "
            "r505-r515 SpecImprove #35842 lưu multi action · r1199/r1230/r1261-r1262/r1268/r1274 "
            "filter QRコードアクション tại màn friendlist — 14 dòng liên quan)",
            "TCsLine_Improve chung → tab「Improve filter + url」(r3-r18, danh mục 11 loại filter tại màn "
            "friendlist — CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi; dùng làm danh mục đối chiếu coverage)",
            "TCsLine_Improve chung → tab「Improve speed」(r4-r5,『Friendlist』là 1 trong 2 màn action của web; "
            "chuỗi action lồng form → tag → scenario)",
            "TCsLine_Improve chung → tab「Phân quyền」(r3-r14, TC dùng chung cho MỌI màn của tool — "
            "menu bị khoá + tooltip 3 dòng tiếng Nhật theo role 副管理者 / 運用者; FA-001 cũng dùng nguồn này)",
        ],
        "excluded": [
            "TCsLine_Detail_Friend (12 tab, ~2.000 TC lá: 「Improve 2026.05」953 lá ·「Trigger action」654 dòng · "
            "「[AI] TCs_5」891 dòng · 5 tab「[AI] TCs_UI*」·「[AI] Bugs」) — màn 「友だち情報詳細」 "
            "(/basic/friendlist/my_page/{id}) tuy là SCR-FRL-03 trong spec của FA-013 nhưng có spec RIÊNG "
            "(spec-features/admin/detail-friend/), 7 tab SPA + 4 sub-page, 37 endpoint. "
            "ĐÃ XÁC NHẬN với user (2026-08-26): TÁCH TAB RIÊNG, chạy /collect-tcs riêng. "
            "Kho FA-013 chỉ giữ TC mức『click LINE登録名 → mở được màn chi tiết』và hệ quả xoá friend",
            "TCsLine_Modal Filter (8 tab:「Improve chung from 2026.07」·「Test bug KH」·「Bug filter OR」· "
            "「improve filter 8/10/2024」·「improve filter ngày 13/11」·「Sửa filter autoreply」· "
            "「Improve filter web」·「Filter point & date」) — SC-003 Friend Filter là SHARED COMPONENT dùng "
            "chung bởi FA-002, FA-008, FA-009, FA-013, FA-024. ĐÃ XÁC NHẬN với user: giữ mức tóm tắt. "
            "Kho FA-013 chỉ giữ TC『popup filter mở được · 11 loại điều kiện · số 検索結果 khớp · điều kiện "
            "truyền đúng sang bulk action』. ĐỀ XUẤT: tách feature riêng『SC-003 絞り込み』(giữ nguyên đề "
            "xuất như FA-008)",
            "TCsLine_ModalAction (7 tab) — SC-004 Action Settings cũng là shared component (12 tính năng "
            "dùng chung). ĐÃ XÁC NHẬN với user: giữ mức tóm tắt. Kho FA-013 chỉ giữ TC『13 loại action "
            "chạy được từ màn friendlist và thực thi đúng』. ĐỀ XUẤT: tách feature riêng "
            "『SC-004 エルメアクション』",
            "Import / Export CSV của friendlist (EP-23 export · EP-24 download-csv · EP-25 màn import · "
            "EP-26 read_file_csv · EP-27 save_file_csv) và 10.4 TCsLine_Quản lý CSV (4 tab:「Import CSV」· "
            "「Export CSV」·「fix bug」·「Bổ sung mục line user id」) — ĐÃ XÁC NHẬN với user (2026-08-26): "
            "đẩy TOÀN BỘ sang FA-014「CSV管理」, gom khi chạy /collect-tcs cho FA-014",
            "TCsLine_MCP → tab「12.Friend_list」(990 dòng) và「2.Friend_stats」(1007 dòng) — format phẳng "
            "TC ID | MCP Tool | Category | Scenario, test tầng công cụ MCP chứ không phải màn admin của LME. "
            "ĐỀ XUẤT: tách sheet riêng『MCP』(giữ nguyên đề xuất như FA-012 / FA-011 / FA-001 / FA-008) "
            "— HỎI USER XÁC NHẬN",
            "15.1 TCsLine_Action Schedule (tab「Test fix bug」) — màn アクションスケジュール実行 "
            "(/basic/action-schedules) là FA-016, có màn riêng. Kho FA-013 chỉ giữ TC r134-r139 dưới dạng "
            "ĐỐI CHỨNG hồi quy (action schedule tạo TAY có hành vi khác action schedule tạo TỰ ĐỘNG từ "
            "friendlist) — xem MT-14. ĐỀ XUẤT: chạy /collect-tcs riêng cho FA-016",
            "10.3 TCsLine_Friendlist → tab「Q&A」(115 dòng, chỉ có cột số thứ tự, KHÔNG có nội dung) · "
            "tab「ListBug」(1 dòng, rỗng) · tab「Copy of Improve xxx」(2 dòng, rỗng) — không phải test case",
            "TCsLine_Improve chung → tab「Test bug folder all màn」(299 TC lá) — folder của các tính năng "
            "khác (tag, template, scenario, friend info), màn friendlist KHÔNG có folder",
            "TCsLine_Improve chung → tab「Test callback friend」(15 TC lá) — job callback follow/unfollow "
            "từ LINE, thuộc FA-007 あいさつメッセージ (đã gom ở tab FA-007)",
            "16. TCsLine_ErrorList — màn 配信エラー (/basic/error-list-v2) là FA-028 riêng. Kho FA-013 chỉ "
            "giữ TC『action gửi lỗi → có bản ghi ở màn 配信エラー』. ĐỀ XUẤT: chạy /collect-tcs riêng",
            "Link ngoài folder: tab Info r2 của 10.3 TCsLine_Friendlist trỏ tới spreadsheet "
            "1SLCxJ6gId45vN8LsYdjTZtPhcsuFKz3TSOPrGfpXYcM (SpecImprove #34438) — file này KHÔNG nằm trong "
            "folder TCs trên Drive nên không quét được. Nội dung #34438 đã có sẵn dưới dạng 1 cột kết quả "
            "trong tab「Testcase」nên không mất TC, nhưng cần user xác nhận file ngoài đó có TC riêng không",
        ],
    },
    {
        "code": "FA-008", "vi": "Broadcast", "jp": "メッセージ配信",
        "prefix": "BC",
        "sections": "SECTIONS_BC",
        "parts": ["bc_s1_list.S1", "bc_s2_create.S2", "bc_s3_profile_filter.S3",
                  "bc_s4_preview_test.S4", "bc_s5_edit_job.S5", "bc_s6_alert_env.S6"],
        "conflicts": "bc_conflicts",
        "spec": "spec-features/admin/message-send-all/ (chốt 2026-03-26, confidence Cao ~80% · "
                "8 validation issues · 10 open questions — ⚠️ KHÔNG có tính năng 配信数上限アラート #36436, xem MT-20)",
        "sources": [
            "03. TCsLine_Broadcast → tab「Improver send all(task broadcast)」(gid=0, 02/2024 → 05/2026, "
            "952 dòng, 602 TC lá — TAB MASTER còn sống, 6 cột ticket: Bug KH #36730 · SpecImprove #35253 · "
            "test #32823 · Bug #32665 · Bug #32229 · test bug #31527. Cấu trúc: 3 khối theo tab màn list "
            "(配信予約 r10-r387 · 下書き r388-r676 · 配信履歴 r677-r775) + CHECK COVER CASE CŨ r776-r807 + "
            "4 khối bug theo ticket r809-r952)",
            "03. TCsLine_Broadcast → tab「function」(02/2024 → 03/2025, 226 dòng — bảng phẳng ma trận "
            "chức năng theo 4 màn (chờ send / đăng ký / nháp / đã send); chứa 3 khối bổ sung: "
            "「24/2/2024 Luồng mới」r101-r133 (quan hệ cha/con parent_id, template そのまま vs 引用), "
            "「Task Small Send All update 14/6」r192-r220, Bug #29301 (25/03/2025 — nhiều filter gây vỡ layout))",
            "03. TCsLine_Broadcast → tab「[AI] alert_limit」(2026, 100 dòng, 99 TC TC-BAL-001…099 — "
            "ĐÃ Ở FORMAT 12 CỘT của kho; tính năng MỚI「配信数上限アラート」#36436. "
            "⚠️ Loại case dùng enum riêng F-Normal/F-Abnormal/F-Boundary/UI/UX/Permission/Regression/"
            "Side-effect — kho đã quy về 3 giá trị Normal/Abnormal/Boundary)",
            "03. TCsLine_Broadcast → tab「UI Tests 36436」(2026, 30 dòng, TC-BAL-001…030) và "
            "「API Tests 36436」(2026, 30 dòng, TC-BAL-031…059) — cùng ticket #36436, bản CŨ hơn tab "
            "「[AI] alert_limit」; kho lấy tab [AI] làm chuẩn và chỉ đối chiếu 2 tab này để bù case thiếu",
            "03. TCsLine_Broadcast → tab「broadcaset」(18/09/2024, 11 dòng — chuyên đề『Broadcase quá giờ "
            "sẽ không gửi mà hiện msg lỗi』: ma trận send_time/updated_at quá hạn 5/14/15/30 phút + "
            "case filter hỏng dữ liệu. Nguồn DUY NHẤT cho rule 15 phút)",
            "03. TCsLine_Broadcast → tab「test filte」(26 dòng — hành vi chuyển qua lại 絞り込み ⇄ "
            "すべての友だち trước/sau khi tạo broadcast, và ảnh hưởng của chặn/mở chặn friend tới 配信数. "
            "Nguồn DUY NHẤT cho MT-05 và MT-11)",
            "03. TCsLine_Broadcast → tab「Small Send All update 14/6」(31 dòng) + "
            "「Bug Task Small Send All update 14/6」(19 dòng) — đợt Task Small Send All 14/06; nội dung TC "
            "đã được gộp nguyên vào tab「function」r192-r220, 2 tab này giữ lại vì có thêm 3 bug UI/logic "
            "(copy redirect sai tab, số friend màn nháp không khớp màn detail)",
            "03. TCsLine_Broadcast → tab「Update list friend đã send」(22/04, 6 dòng — mốc chuyển dữ liệu "
            "message 08:00 ngày 15/01/2025 giữa bảng `message` cũ và `messages_v2s` mới. Nguồn DUY NHẤT cho MT-14)",
            "TCsLine_Improve chung → tab「Profile sender」(12/2025, 197 dòng, 184 TC lá — Bug KH #33072/#33052. "
            "Kho lấy r82-r112 (send test broadcast qua modal preview và qua quick test) + r157-r164 "
            "(job gửi send all); phần còn lại thuộc chat 1:1 / template / scenario / remind — xem mục Đã loại)",
            "TCsLine_Improve chung → tab「Improve sendall scenario」(34 dòng — cửa sổ đóng băng filter "
            "trước giờ gửi (10 phút cho broadcast, 5 phút cho scenario step), rule chặn edit 5 phút, "
            "và ma trận giới hạn số điều kiện filter AND/OR. Nguồn DUY NHẤT cho MT-12 và MT-17)",
            "TCsLine_Improve chung / TCsLine_JOB → tab「Move job send all」(09/2024, 6 dòng — đợt chuyển "
            "gửi send all sang job nền; 4 case cơ bản gửi ngay/đặt lịch × có/không filter)",
        ],
        "excluded": [
            "03. TCsLine_Broadcast → tab「Bug Improver send all」(139 dòng) ·「[AI] Bugs」(4 dòng) ·"
            "「List Bug」(2 dòng) ·「Trang tính11」(3 dòng) ·「Bản sao của [AI] alert_limit」·「Info」 — "
            "nhật ký bug và bản sao, không phải test case có kết quả mong đợi. Tab「Info」đã dùng để xác "
            "định niên đại 8 đợt cập nhật (02/2024 → 05/2026)",
            "Tab master r881-r921 (SpecImprove #35253 — fix URL bị thêm space thừa, áp cho 7 màn: "
            "màn template · scenario · setting remind · modal multi action · chat 1:1 web · chat 1:1 app "
            "mobile · setting schedule). Kho FA-008 CHỈ giữ phần của màn broadcast (r875-r880); 6 màn còn "
            "lại thuộc FA-010 / FA-009 / FA-022 / FA-001 và các feature action. "
            "ĐỀ XUẤT: bổ sung vào tab của từng feature khi chạy /collect-tcs cho chúng — HỎI USER XÁC NHẬN",
            "Tab master r924 (title page lịch sử gửi của ステップ配信) — thuộc FA-009. Kho giữ lại 1 TC vì là "
            "cặp đối chứng của Bug KH #35506: 2 nhánh dùng CHUNG 1 trang, fix ở FA-008 làm hỏng nhánh kia "
            "là hồi quy — HỎI USER XÁC NHẬN",
            "TCsLine_Improve chung → tab「Profile sender」r4-r81 (chat 1:1 web + app mobile, send test "
            "template) · r113-r156 (send test scenario, quick test step, send test remind) · r165-r182 "
            "(job scenario, multi action, remind, resend message error, schedule send chat) — thuộc "
            "FA-001 / FA-010 / FA-009 / FA-022. FA-001 đã gom tab này làm nguồn; phần scenario/remind "
            "bổ sung khi chạy /collect-tcs cho FA-009 / FA-022",
            "TCsLine_Modal Filter (8 tab: Bug filter OR · improve filter 8/10/2024 · improve filter ngày "
            "13/11 · Sửa filter autoreply · Improve filter web · Filter point & date · Improve chung from "
            "2026.07 · Test bug KH) — SC-003 Friend Filter là SHARED COMPONENT dùng chung bởi FA-008, "
            "FA-009, FA-013, FA-024. Kho FA-008 chỉ giữ TC ở mức『popup filter mở được, 11 loại điều kiện "
            "lưu được, số 配信数 khớp』; chi tiết từng loại filter thuộc component. "
            "ĐỀ XUẤT: tách feature riêng『SC-003 絞り込み』— HỎI USER XÁC NHẬN",
            "TCsLine_ModalAction (7 tab) — SC-004 Action Settings cũng là shared component. Kho FA-008 chỉ "
            "giữ TC『action đăng ký được, 絞り込みあり/なし chạy đúng, action sau gửi thực thi』. "
            "ĐỀ XUẤT: tách feature riêng『SC-004 エルメアクション』— HỎI USER XÁC NHẬN",
            "TCsLine_MCP → tab「05.broadcast」(977 dòng) ·「Create_broadcast」(1210 dòng) ·「P2_broadcast」"
            "(1049 dòng) ·「Docs broadcast」·「Broadcast Prototype support」·「Schedule」— format phẳng "
            "TC ID | MCP Tool | Category | Scenario, test tầng công cụ MCP chứ không phải màn admin của LME. "
            "ĐỀ XUẤT: tách sheet riêng『MCP』(giữ nguyên đề xuất như FA-012 / FA-011 / FA-001 / FA-033 / "
            "FA-020) — HỎI USER XÁC NHẬN",
            "TCsLine_summary-message-send (1 file) — FA-029「配信数サマリー」là màn RIÊNG "
            "(/basic/line/summary-message-send), tuy đọc cùng nguồn số liệu gửi tin. "
            "ĐỀ XUẤT: chạy /collect-tcs riêng — HỎI USER XÁC NHẬN",
            "16. TCsLine_ErrorList — FA-028「配信エラー」(/basic/error-list-v2) là màn RIÊNG hiển thị bảng "
            "message_error mà job broadcast ghi vào. Kho FA-008 chỉ giữ TC『job ghi message_error với code "
            "REACH_LIMIT_*』. ĐỀ XUẤT: chạy /collect-tcs riêng — HỎI USER XÁC NHẬN",
            "TCsLine_Test Limit theo plan → tab「[AI] Test limit v2」— giới hạn theo gói áp cho TOÀN TOOL, "
            "không riêng broadcast. Kho FA-008 chỉ giữ phần quota gửi tin (nhóm 配信数上限アラート). "
            "ĐỀ XUẤT: chạy /collect-tcs riêng cho『Giới hạn theo plan』— HỎI USER XÁC NHẬN",
            "02. TCsLine_Template → tab「Preview URL」— thuộc FA-010 Mẫu tin nhắn, đã gom ở tab FA-010",
        ],
    },
]

# Thứ tự tab trên Google Sheet + thứ tự dòng ở các tab dùng chung = MÃ MÀN HÌNH tăng dần.
# Thứ tự khai báo ở trên (theo thứ tự chạy /collect-tcs) không còn ảnh hưởng đến output.
FEATURES.sort(key=lambda f: f["code"])


def load(feat):
    recs = []
    for ref in feat["parts"]:
        mod, var = ref.split(".")
        recs += getattr(importlib.import_module(mod), var)
    # Feature khai báo khoá "sections" (tên list trong _common) => dùng thứ tự nhóm
    # RIÊNG của feature. Không khai báo => giữ nguyên hành vi cũ (thứ tự gộp toàn cục).
    secs = getattr(_common, feat["sections"]) if feat.get("sections") else None
    feat["_sections"] = {k: v for k, v in section_summary(recs, secs).items() if v}
    return build(recs, feat.get("prefix", "TAG"), secs)


def load_conflicts(feat):
    m = importlib.import_module(feat["conflicts"])
    return m.COLS, m.CONFLICTS


# ─────────────────────────── Markdown ────────────────────────────
def md_cell(s):
    return str(s).replace("|", "\\|").replace("\n", "<br>")


def to_md(feat, rows, ccols, conflicts):
    tab = tab_title(feat)
    n = len(rows)
    # chỉ số cột trong COLS: 1=Nhóm · 2=Mã quan điểm · 4=Loại case
    dist, gdist = {}, {}
    for r in rows:
        dist[r[4]] = dist.get(r[4], 0) + 1
        gdist[r[1]] = gdist.get(r[1], 0) + 1
    vps = sorted({r[2] for r in rows})

    out = [f"# Kho TCs tổng hợp — {tab}", ""]
    out += ["> Tổng hợp từ các file TCs rời trên Drive, đã loại trùng và xử lý conflict theo "
            "nguyên tắc **ưu tiên TC mới nhất**, rồi format lại theo **12 cột** của kho TCs "
            "(xem `kho-tcs/README.md`).", ""]

    out += ["## Nguồn đã gộp", ""]
    for x in feat["sources"]:
        out.append(f"- {x}")
    out += ["", "## Nguồn đã loại khỏi phạm vi (cần bạn xác nhận)", ""]
    for x in feat["excluded"]:
        out.append(f"- {x}")

    out += ["", "## Thống kê", "",
            "| Chỉ số | Giá trị |", "|---|---|",
            f"| Tổng TC sau khi gộp | **{n}** |",
            f"| Normal / Abnormal / Boundary | {dist.get('Normal',0)} / {dist.get('Abnormal',0)} / {dist.get('Boundary',0)} |",
            f"| Nhóm UI / API / Data | {gdist.get('UI',0)} / {gdist.get('API',0)} / {gdist.get('Data',0)} |",
            f"| Số quan điểm test được phủ | {len(vps)} |",
            f"| Điểm mâu thuẫn cần Leader quyết | **{len(conflicts)}** |",
            f"| Spec đối chiếu | `{feat['spec']}` |", ""]

    out += ["## Coverage theo màn hình/chức năng", "",
            "| # | Màn hình/chức năng | Số TC |", "|---|---|---|"]
    for i, (name, c) in enumerate(feat["_sections"].items(), start=1):
        out.append(f"| {i} | {name} | {c} |")
    out += ["", "## Quan điểm test được phủ", "", ", ".join(f"`{v}`" for v in vps), ""]

    out += ["---", "", "## Điểm mâu thuẫn với spec — CẦN QUYẾT ĐỊNH", "",
            "| " + " | ".join(ccols) + " |",
            "|" + "|".join(["---"] * len(ccols)) + "|"]
    for c in conflicts:
        out.append("| " + " | ".join(md_cell(x) for x in c) + " |")

    out += ["", "---", "", f"## TC List ({len(COLS)} cột)", "",
            "| " + " | ".join(COLS) + " |",
            "|" + "|".join(["---"] * len(COLS)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(md_cell(x) for x in r) + " |")
    out.append("")
    return "\n".join(out)


# ───────────────────────── Google Sheet ──────────────────────────
def gs_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build as gbuild
    creds = service_account.Credentials.from_service_account_file(
        str(ROOT.parent / "credentials" / "google-service-account.json"),
        scopes=["https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"])
    return gbuild("sheets", "v4", credentials=creds), gbuild("drive", "v3", credentials=creds)


README_ROWS = [
    ["KHO TCs TỔNG HỢP — DỰ ÁN LME"],
    [],
    ["Mục đích", "Gộp toàn bộ TCs rời rạc trên Drive thành 1 bộ chuẩn: mỗi tính năng = 1 tab."],
    ["Tên tab", "<Mã màn hình> <Tên tiếng Việt> (<Tên màn hình tiếng Nhật>) — VD: FA-001 Chat 1:1 (1:1チャット)"],
    ["Format", "12 cột. DÒNG 1 của mỗi tab tính năng là dòng tiêu đề cột — không có khối mô tả phía trên."],
    ["", "ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú"],
    ["Tab dùng chung", "_README (tab này) · _Nguồn & phạm vi (nguồn đã gộp / đã loại / spec của TẤT CẢ màn hình) · _Mâu thuẫn cần quyết"],
    [],
    ["NGUYÊN TẮC GỘP"],
    ["1. Loại trùng", "TC cùng đường dẫn chức năng + cùng kết quả mong đợi → giữ 1."],
    ["2. Xử lý conflict", "Cùng chức năng nhưng kết quả mong đợi khác nhau → ƯU TIÊN TC MỚI NHẤT (theo ngày ở tab Info của file gốc + tab master còn được cập nhật)."],
    ["3. Loại logic cũ", "TC thuộc luồng đã bị thay thế bởi đợt improve mới hơn → bỏ, ghi lại ở tab _Mâu thuẫn cần quyết nếu ảnh hưởng hành vi."],
    ["4. Truy vết", "Cột \"Ghi chú\" của mỗi TC ghi nguồn dạng r<số dòng> ở file/tab gốc."],
    ["5. Đối chiếu spec", "So với spec-features/. Mọi điểm lệch được đưa vào tab _Mâu thuẫn cần quyết, KHÔNG tự ý chọn bên nào."],
    [],
    ["GIÁ TRỊ CỐ ĐỊNH CỦA CỘT"],
    ["ID", "TC-<PREFIX>-01, -02, ... (PREFIX: TAG / CHT / FORM / RM / FRI / SCE / BIL / EBK / BLP / TMT / RPL / BK / LSN / SLN) — đánh số TUẦN TỰ theo thứ tự màn hình/chức năng, không đánh lại theo mã quan điểm."],
    ["Nhóm", "UI / API / Data — tầng kiểm chứng của TC. UI = nhìn thấy trên màn hình (admin hoặc LINE user). API = xử lý phía server: gửi tin, job nền, tích hợp ngoài, thanh toán, phân quyền, đồng thời, hiệu năng. Data = tầng dữ liệu: DB, đếm số, tham chiếu, migration, dữ liệu cũ."],
    ["", "Nhóm được SUY TỰ ĐỘNG từ mã quan điểm (bảng GROUP_MAP trong kho-tcs/data/_common.py). Sai chỗ nào thì ghi đè bằng tham số group=\"...\" của hàm tc()."],
    ["Mã quan điểm", "Mã trong framework/checklist-lme.md — cột để map coverage."],
    ["Màn hình/chức năng", "Nhóm chức năng trong màn (VD Tạo folder, Edit tag, Action gắn tag). Quyết định thứ tự TC trong tab; khai báo ở SECTIONS_* trong kho-tcs/data/_common.py."],
    ["Loại case", "Normal / Abnormal / Boundary  (KHÔNG có Regression — TC regression ghi chữ 'regression' ở Ghi chú)"],
    ["Tên case", "Nội dung tiêu đề TC do người viết đặt, giữ nguyên."],
    ["Kết quả thực thi", "LUÔN ĐỂ TRỐNG khi sinh. Người test tự điền Đạt / Không đạt."],
    ["Ghi chú", "Nguồn r<số dòng> · mã mâu thuẫn MT-xx · cảnh báo tuổi TC. Kèm 'Môi trường: PRODUCTION' khi TC bắt buộc chạy production (RULE-08: media, domain, job, loadbalance, bill tiền, race, performance) và 'Đánh giá spec: Spec không ghi / Đã hỏi leader' khi spec chưa rõ."],
    [],
    ["CÁCH ĐỌC TAB _Mâu thuẫn cần quyết"],
    ["", "Mỗi dòng là 1 điểm TCs và spec nói khác nhau. Cột 'Quyết định của Leader' để trống — bạn điền vào đó."],
    ["", "Mức CAO = ảnh hưởng hành vi người dùng cuối, nên chốt trước khi chạy test."],
    [],
    ["CÁCH ĐỌC TAB _Nguồn & phạm vi"],
    ["", "Với MỖI màn hình: các tab Drive đã được gộp vào (kèm niên đại), các tab đã bị loại khỏi phạm vi (kèm lý do — cần bạn xác nhận), và spec đã dùng để đối chiếu."],
    [],
    ["Nguyên tắc tách TC", "MỖI kết quả mong đợi khác nhau = 1 TC riêng. Giữ chung khi nhiều input cùng 1 kết quả, hoặc khi các bước là 1 chuỗi thao tác liên tiếp không tách rời (race, FUNC-SEQ, verify 3 tầng của cùng 1 hành động)."],
]

# ── Danh mục TOÀN BỘ màn hình Admin (trích từ templates/LME-SYSTEM-SPEC.md) ───
# Dùng để biết màn hình nào CHƯA được gom TCs. Màn hình đã gom thì lấy tên từ FEATURES.
ALL_SCREENS = [
    ("FA-001", "Chat 1:1", "1:1チャット"),
    ("FA-002", "Quản lý chat", "チャット管理"),
    ("FA-003", "Tự động trả lời", "自動応答"),
    ("FA-004", "Rich Menu", "リッチメニュー"),
    ("FA-005", "Tạo hình ảnh Rich Menu", "リッチメニュー画像作成"),
    ("FA-006", "Cài đặt thông báo", "通知設定"),
    ("FA-007", "Tin nhắn chào mừng", "あいさつメッセージ"),
    ("FA-008", "Gửi tin nhắn hàng loạt", "メッセージ配信"),
    ("FA-009", "Phát hành theo bước", "ステップ配信"),
    ("FA-010", "Mẫu tin nhắn", "テンプレート"),
    ("FA-011", "Tạo biểu mẫu", "フォーム作成"),
    ("FA-012", "Quản lý thẻ", "タグ管理"),
    ("FA-013", "Danh sách bạn bè", "友だちリスト"),
    ("FA-014", "Quản lý CSV", "CSV管理"),
    ("FA-015", "Quản lý thông tin bạn bè", "友だち情報管理"),
    ("FA-016", "Lịch hẹn hành động", "アクションスケジュール実行"),
    ("FA-017", "QR Code Action", "QRコードアクション"),
    ("FA-018", "Popup", "ポップアップ"),
    ("FA-019", "Đặt lịch bài học", "レッスン予約"),
    ("FA-020", "Đặt lịch salon", "サロン・面談予約"),
    ("FA-021", "Đặt lịch sự kiện", "イベント予約"),
    ("FA-022", "Gửi nhắc lịch", "リマインド配信"),
    ("FA-023", "Phân tích URL", "URL分析"),
    ("FA-024", "Phân tích chéo", "クロス分析"),
    ("FA-025", "Chuyển đổi", "コンバージョン"),
    ("FA-026", "Sản phẩm đơn lẻ", "単品商品"),
    ("FA-027", "Chương trình giới thiệu", "エルメ紹介プログラム"),
    ("FA-028", "Lỗi phát hành", "配信エラー"),
    ("FA-029", "Tổng hợp số phát hành", "配信数サマリー"),
    ("FA-030", "Trang chủ", "ホーム"),
    ("FA-031", "Hợp đồng và thanh toán", "契約プラン・決済情報"),
    ("FA-032", "Thêm tài khoản mới", "新規アカウント追加"),
    ("FA-033", "Sao chép dữ liệu", "データコピー"),
    ("FA-034", "Liên kết hệ thống thanh toán", "決済システム連携設定"),
    ("FA-035", "Quản lý nhân viên", "スタッフ管理"),
    ("FA-036", "Trang cá nhân", "マイページ"),
    ("FA-037", "Xác thực 2 yếu tố", "ログイン時の二段階認証"),
    ("FA-038", "Cài đặt kết nối LOA", "LOA接続設定"),
    ("FA-039", "Đăng ký tài khoản", "アカウント登録"),
    ("FA-040", "Đăng nhập", "ログイン"),
    ("FA-041", "Cài đặt chat", "チャット設定"),
]

# 5 trạng thái của 1 màn hình trong kho
ST_DONE = "✅ XONG — đã chốt mâu thuẫn + đã cập nhật TC"
ST_PARTIAL = "🔄 ĐÃ ÁP QUYẾT ĐỊNH — còn mâu thuẫn chưa chốt"
ST_NEED_UPDATE = "🟠 ĐÃ CHỐT MÂU THUẪN — CHƯA cập nhật lại TC"
ST_WAIT = "🔴 ĐÃ COLLECT — CHỜ QUYẾT ĐỊNH mâu thuẫn"
ST_NONE = "⬜ CHƯA COLLECT TCs"


def screen_status(feat):
    """Trả về (trạng thái, số mâu thuẫn đã chốt, tổng mâu thuẫn) của 1 màn hình đã gom.

    Căn cứ:
      - Cột 'Trạng thái' của bảng mâu thuẫn (bắt đầu bằng ✅ = đã chốt).
      - Khoá 'applied' trong FEATURES = ngày đã ÁP quyết định của Leader vào TCs.
        Rỗng nghĩa là TCs chưa được sửa theo quyết định.
    """
    _, conf = load_conflicts(feat)
    total = len(conf)
    done = sum(1 for c in conf if str(c[2]).lstrip().startswith("✅"))
    applied = bool(feat.get("applied"))
    if total and done == total and applied:
        return ST_DONE, done, total
    if done and applied:
        return ST_PARTIAL, done, total
    if done and not applied:
        return ST_NEED_UPDATE, done, total
    return ST_WAIT, done, total


def progress_rows(feats):
    """Bảng tiến độ theo màn hình — sắp theo mã màn hình tăng dần."""
    by_code = {f["code"]: f for f in feats}
    rows = [["TIẾN ĐỘ THEO MÀN HÌNH"],
            ["Mã", "Màn hình", "Số TC", "Mâu thuẫn (đã chốt / tổng)",
             "TC đã cập nhật theo quyết định", "Trạng thái"]]
    buckets = {ST_DONE: [], ST_PARTIAL: [], ST_NEED_UPDATE: [], ST_WAIT: [], ST_NONE: []}
    for code, vi, jp in ALL_SCREENS:
        f = by_code.get(code)
        if not f:
            rows.append([code, f"{vi} ({jp})", "", "", "", ST_NONE])
            buckets[ST_NONE].append(code)
            continue
        st, done, total = screen_status(f)
        rows.append([code, f"{f['vi']} ({f['jp']})", len(load(f)),
                     f"{done} / {total}", f.get("applied") or "—", st])
        buckets[st].append(code)
    rows.append([])
    rows.append(["TỔNG HỢP", f"{len(feats)} / {len(ALL_SCREENS)} màn hình đã gom TCs"])
    for st in (ST_DONE, ST_PARTIAL, ST_NEED_UPDATE, ST_WAIT, ST_NONE):
        b = buckets[st]
        rows.append([st, f"{len(b)} màn hình" + (f" — {' · '.join(b)}" if b else "")])
    return rows


def sources_rows(feats):
    """Tab _Nguồn & phạm vi — gom thông tin nguồn/phạm vi/spec của TẤT CẢ màn hình."""
    rows = [["Màn hình", "Loại", "Nội dung"]]
    for f in feats:
        tab = tab_title(f)
        for x in f["sources"]:
            rows.append([tab, "Nguồn đã gộp", x])
        for x in f["excluded"]:
            rows.append([tab, "Đã loại khỏi phạm vi (cần xác nhận)", x])
        rows.append([tab, "Spec đối chiếu", f["spec"]])
    return rows


# ── ĐỊNH DẠNG CHUẨN CỦA TAB TÍNH NĂNG ────────────────────────────────────────
# Lấy từ tab FA-012 Quản lý thẻ (タグ管理) — Leader chốt làm chuẩn cho MỌI tab tính năng,
# kể cả các tab tạo mới sau này. Sửa ở đây là đổi cho tất cả.
#   ID · Nhóm · Mã quan điểm · Màn hình/CN · Loại case · Tên case · Tiền ĐK ·
#   Các bước · Dữ liệu nhập · KQ mong đợi · KQ thực thi · Ghi chú
TAB_WIDTHS = [80, 64, 64, 80, 73, 244, 244, 244, 200, 244, 80, 300]
TAB_FROZEN_ROWS = 1
TAB_FROZEN_COLS = 4          # đóng băng ID · Nhóm · Mã quan điểm · Màn hình/chức năng
TAB_HEAD_RGB = {"red": .85, "green": .89, "blue": .96}

# Tab meta giữ định dạng riêng (số cột khác 12)
META_WIDTHS = {
    "readme":    [110, 520, 90, 200, 220, 330],
    "sources":   [300, 240, 900],
    "conflicts": [230, 170, 80, 90, 130, 300, 330, 330, 280, 200, 320, 360],
}


def fmt_reqs_for_tab(sid, ncol=None, widths=None, rgb=None, frozen_cols=None):
    """Yêu cầu batchUpdate định dạng 1 tab: đóng băng + tiêu đề đậm/nền + wrap + độ rộng cột."""
    widths = TAB_WIDTHS if widths is None else widths
    ncol = len(widths) if ncol is None else ncol
    rgb = TAB_HEAD_RGB if rgb is None else rgb
    frozen_cols = TAB_FROZEN_COLS if frozen_cols is None else frozen_cols
    reqs = [
        {"updateSheetProperties": {"properties": {"sheetId": sid, "gridProperties": {
            "frozenRowCount": TAB_FROZEN_ROWS, "frozenColumnCount": frozen_cols}}, "fields":
            "gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}},
        {"repeatCell": {"range": {"sheetId": sid, "endRowIndex": 1,
                                  "startColumnIndex": 0, "endColumnIndex": ncol},
                        "cell": {"userEnteredFormat": {"textFormat": {"bold": True},
                                                       "backgroundColor": rgb}},
                        "fields": "userEnteredFormat(textFormat,backgroundColor)"}},
        {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1},
                        "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP",
                                                       "verticalAlignment": "TOP"}},
                        "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}},
    ]
    for idx, w in enumerate(widths):
        reqs.append({"updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "COLUMNS",
                      "startIndex": idx, "endIndex": idx + 1},
            "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    return reqs


def apply_format(feats):
    """Áp ĐỊNH DẠNG CHUẨN cho các tab đã có sẵn — KHÔNG ghi đè dữ liệu trong tab.

    Dùng khi chỉ cần đồng bộ độ rộng cột / đóng băng mà không muốn build lại nội dung
    (giữ nguyên mọi ô Leader đã điền tay, ví dụ cột Quyết định ở tab _Mâu thuẫn)."""
    svc, _ = gs_service()
    ssid = STATE.read_text().strip()
    meta = svc.spreadsheets().get(spreadsheetId=ssid).execute()
    existing = {sh["properties"]["title"]: sh["properties"]["sheetId"] for sh in meta["sheets"]}

    reqs = []
    for f in feats:
        tab = tab_title(f)
        if tab not in existing:
            print(f"  BỎ QUA (chưa có tab): {tab}")
            continue
        reqs += fmt_reqs_for_tab(existing[tab])
        print(f"  {tab}: freeze {TAB_FROZEN_ROWS} dòng / {TAB_FROZEN_COLS} cột, {len(TAB_WIDTHS)} cột")

    if TAB_README in existing:
        reqs += fmt_reqs_for_tab(existing[TAB_README], ncol=6, widths=META_WIDTHS["readme"],
                                 rgb={"red": .93, "green": .93, "blue": .93}, frozen_cols=1)
    if TAB_SOURCES in existing:
        reqs += fmt_reqs_for_tab(existing[TAB_SOURCES], widths=META_WIDTHS["sources"],
                                 rgb={"red": .87, "green": .94, "blue": .87}, frozen_cols=1)
    if TAB_CONFLICTS in existing:
        reqs += fmt_reqs_for_tab(existing[TAB_CONFLICTS], widths=META_WIDTHS["conflicts"],
                                 rgb={"red": .98, "green": .85, "blue": .8}, frozen_cols=1)

    svc.spreadsheets().batchUpdate(spreadsheetId=ssid, body={"requests": reqs}).execute()
    print(f"\nSheet: https://docs.google.com/spreadsheets/d/{ssid}/edit")


def to_sheet(feats):
    svc, drive = gs_service()

    ssid = STATE.read_text().strip() if STATE.exists() else None
    if ssid:
        try:
            svc.spreadsheets().get(spreadsheetId=ssid).execute()
        except Exception:
            ssid = None

    if not ssid:
        # Service account KHÔNG có Drive storage → không tự tạo file được.
        # File phải được tạo sẵn bằng tài khoản user rồi share quyền writer cho service account,
        # sau đó ghi id vào kho-tcs/.sheet-id
        raise SystemExit(
            "Thiếu kho-tcs/.sheet-id.\n"
            "Tạo 1 Google Sheet rỗng bằng tài khoản của bạn, share quyền Editor cho\n"
            f"  {SA_EMAIL}\n"
            "rồi lưu spreadsheetId vào kho-tcs/.sheet-id")

    meta = svc.spreadsheets().get(spreadsheetId=ssid).execute()
    existing = {sh["properties"]["title"]: sh["properties"]["sheetId"] for sh in meta["sheets"]}

    tabs = [tab_title(f) for f in feats]
    want = list(META_TABS) + tabs

    # ── Đổi tên tab cũ thay vì xoá+tạo lại, để GIỮ NGUYÊN gid (link cũ không chết,
    #    comment/định dạng thủ công của Leader không mất). Khớp theo mã màn hình.
    reqs = []
    for f, new_title in zip(feats, tabs):
        if new_title in existing:
            continue
        pref = f["code"] + " "
        cand = [t for t in existing if t.startswith(pref) and t not in want]
        old = cand[0] if cand else None
        if old:
            reqs.append({"updateSheetProperties": {
                "properties": {"sheetId": existing[old], "title": new_title}, "fields": "title"}})
            existing[new_title] = existing.pop(old)
            print(f"  đổi tên tab: {old!r} → {new_title!r}")
    if reqs:
        svc.spreadsheets().batchUpdate(spreadsheetId=ssid, body={"requests": reqs}).execute()

    reqs = []
    for t in want:
        if t not in existing:
            reqs.append({"addSheet": {"properties": {"title": t, "gridProperties": {"frozenRowCount": 1}}}})
    # xoá tab thừa (tab mặc định của Google, tên phụ thuộc locale: Sheet1 / Trang tính1 / ...)
    for t, sid in existing.items():
        if t not in want:
            print(f"  XOÁ tab thừa: {t!r}")
            reqs.append({"deleteSheet": {"sheetId": sid}})
    if reqs:
        svc.spreadsheets().batchUpdate(spreadsheetId=ssid, body={"requests": reqs}).execute()
    meta = svc.spreadsheets().get(spreadsheetId=ssid).execute()
    existing = {sh["properties"]["title"]: sh["properties"]["sheetId"] for sh in meta["sheets"]}

    # sắp xếp lại thứ tự tab
    order = [{"updateSheetProperties": {"properties": {"sheetId": existing[t], "index": i},
                                        "fields": "index"}} for i, t in enumerate(want) if t in existing]
    if order:
        svc.spreadsheets().batchUpdate(spreadsheetId=ssid, body={"requests": order}).execute()

    def write(tab, values):
        svc.spreadsheets().values().clear(spreadsheetId=ssid, range=f"'{tab}'").execute()
        svc.spreadsheets().values().update(
            spreadsheetId=ssid, range=f"'{tab}'!A1",
            valueInputOption="RAW", body={"values": values}).execute()

    write(TAB_README, README_ROWS + [[]] + progress_rows(feats))
    write(TAB_SOURCES, sources_rows(feats))

    ccols, all_conf = None, []
    for f in feats:
        ccols, conf = load_conflicts(f)
        all_conf += [[tab_title(f)] + c for c in conf]
    write(TAB_CONFLICTS, [["Màn hình"] + ccols] + all_conf)

    fmt_reqs = []
    for f, tab in zip(feats, tabs):
        rows = load(f)
        # DÒNG 1 = tiêu đề cột. Mọi thông tin nguồn/phạm vi/spec nằm ở tab _Nguồn & phạm vi.
        write(tab, [COLS] + rows)
        # ĐỊNH DẠNG CHUẨN (theo tab FA-012) — xem TAB_WIDTHS / TAB_FROZEN_COLS ở đầu file
        fmt_reqs += fmt_reqs_for_tab(existing[tab], ncol=len(COLS))
        print(f"  {tab}: {len(rows)} TC")

    fmt_reqs += fmt_reqs_for_tab(existing[TAB_README], ncol=6, widths=META_WIDTHS["readme"],
                                 rgb={"red": .93, "green": .93, "blue": .93}, frozen_cols=1)
    fmt_reqs += fmt_reqs_for_tab(existing[TAB_SOURCES], widths=META_WIDTHS["sources"],
                                 rgb={"red": .87, "green": .94, "blue": .87}, frozen_cols=1)
    fmt_reqs += fmt_reqs_for_tab(existing[TAB_CONFLICTS], ncol=len(ccols) + 1,
                                 widths=META_WIDTHS["conflicts"],
                                 rgb={"red": .98, "green": .85, "blue": .8}, frozen_cols=1)

    svc.spreadsheets().batchUpdate(spreadsheetId=ssid, body={"requests": fmt_reqs}).execute()
    url = f"https://docs.google.com/spreadsheets/d/{ssid}/edit"
    print(f"\nSheet: {url}")
    return url


def _slug_vi(s):
    """Tên tiếng Việt → slug ASCII liền: 'Chat 1:1' → 'chat11' · 'Quản lý thẻ' → 'quanlythe'."""
    s = unicodedata.normalize("NFD", s.lower()).replace("đ", "d")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s if c.isascii() and c.isalnum())


def _slug_jp(s):
    r"""Tên tiếng Nhật → giữ nguyên, chỉ bỏ khoảng trắng + ký tự Windows cấm (\ / : * ? " < > |)."""
    return "".join(c for c in s if c not in '\/:*?"<>|' and not c.isspace())


def md_path(f):
    """Tên file markdown = <mã màn hình>-<tên VN>-<tên JP>.md — VD fa001-chat11-11チャット.md"""
    code = f["code"].lower().replace("-", "")
    return ROOT / f"{code}-{_slug_vi(f['vi'])}-{_slug_jp(f['jp'])}.md"


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "md"
    if mode == "md":
        made = set()
        for f in FEATURES:
            rows = load(f)
            ccols, conf = load_conflicts(f)
            out = md_path(f)
            out.write_text(to_md(f, rows, ccols, conf), encoding="utf-8")
            made.add(out.name)
            print(f"{out}  ({len(rows)} TC, {len(conf)} mâu thuẫn)")
        stale = sorted(x.name for x in ROOT.glob("*.md")
                       if x.name not in made and x.name != "README.md")
        if stale:
            print("\nFile .md cũ không còn được sinh (xoá tay nếu không cần):")
            for x in stale:
                print(f"  - kho-tcs/{x}")
    elif mode == "sheet":
        to_sheet(FEATURES)
    elif mode == "format":
        # Chỉ đồng bộ ĐỊNH DẠNG (đóng băng + độ rộng cột), KHÔNG ghi đè dữ liệu trong tab
        apply_format(FEATURES)
    else:
        print("usage: build.py [md|sheet|format]")
