# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 10-11: xóa dữ liệu bot cũ.

S10 Xóa data bot cũ — web (25 tính năng bị ảnh hưởng)
S11 Xóa data bot cũ — app mobile

Đây là phần NẶNG NHẤT của tính năng: sau khi đổi LOA, job dọn dữ liệu xóa/reset dữ liệu
gắn với friend của LOA cũ ở ~35 bảng. Mỗi TC áp RULE-07 (khớp DB + màn hình + output) nên
cố ý GỘP "check db" và "check gui" của CÙNG 1 hành động đổi LOA vào 1 TC — không tách
thành 2 TC như bảng nguồn.

⚠️ Toàn nhóm chạm JOB NỀN → RULE-08: env = PRODUCTION, không kết luận từ staging.
⚠️ Mâu thuẫn liên quan: MT-07 (event_step_time có xóa?) · MT-08 (link CSV cũ 404?) ·
MT-09 (liên kết Google) · MT-10 (lịch sử send all giữ hay xóa?).
"""
from _common import tc

AFTER = ("- Bot cũ có đầy đủ dữ liệu ở tính năng đang kiểm (nêu rõ trong Dữ liệu nhập)\n"
         "- Đã ghi lại số liệu/bản ghi của bot cũ TRƯỚC khi đổi LOA\n"
         "- Đã hoàn tất đổi LOA sang 1 LOA mới và job dọn dữ liệu đã chạy xong\n"
         "- Có quyền query DB để verify")
PRD = dict(env="PRODUCTION")

S10 = [
    # ═══════════════ 10. Xóa data bot cũ — web ═══════════════
    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Ngay khi bấm thực hiện đổi LOA → sinh bản ghi hàng đợi cho job dọn dữ liệu",
       ("- Đăng nhập Admin chủ bot plan Standard trở lên\n"
        "- Đang ở bước xác nhận thực hiện đổi LOA\n"
        "- Có quyền query DB"),
       "1. Query bảng schedule_change_bots, ghi lại số bản ghi hiện có của bot\n"
       "2. Bấm nút thực hiện đổi LOA\n"
       "3. Query lại bảng schedule_change_bots NGAY sau khi bấm\n"
       "4. Quan sát trạng thái bản ghi mới (status)",
       "Số bản ghi trước khi bấm (ghi tay)",
       "- Có ĐÚNG 1 bản ghi mới trong schedule_change_bots cho bot này\n"
       "- Bản ghi ở trạng thái chờ xử lý (WAITING)\n"
       "- Sau khi job chạy xong, trạng thái bản ghi chuyển sang đã xử lý",
       note="Nguồn: Change bot r4 (TR=OK, stg=OK: 'Check khi nhấn change bot → check db → bảng: "
            "schedule_change_bots'). ⚠️ MT-11 — spec lesson-booking/job/job-spec.md §2.6 ghi tên bảng là "
            "`schedule_change_bot` (số ít) + entity `ScheduleChangeBot` + poll "
            "findTop50ByStatusOrderByIdAsc(STATUS_WAITING). RULE-07. "
            "Evidence: query DB 2 thời điểm + ảnh trạng thái bản ghi.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Trang chủ — số bạn bè và biểu đồ 友だち数推移 của LOA cũ bị xóa sạch",
       AFTER,
       "1. Trước khi đổi LOA: vào /basic/overview, ghi lại số bạn bè + ảnh biểu đồ 友だち数推移\n"
       "2. Query bảng bot_friend_statistic đếm số bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job dọn dữ liệu xong\n"
       "4. Vào lại /basic/overview, quan sát số bạn bè và biểu đồ\n"
       "5. Bấm vào detail để xem danh sách bạn bè\n"
       "6. Query lại bot_friend_statistic",
       "Bot cũ có ≥50 bạn bè và ≥7 ngày dữ liệu biểu đồ",
       "- DB bot_friend_statistic: dữ liệu của bot cũ bị XÓA\n"
       "- Màn overview: KHÔNG hiển thị số bạn bè cũ; bộ đếm số bạn bè = 0\n"
       "- Biểu đồ 友だち数推移: không vẽ dữ liệu cũ\n"
       "- Bấm detail: hiển thị danh sách bạn bè MỚI (của LOA mới), không có bạn cũ",
       note="Nguồn: Change bot r5-r6 (TR=OK, stg=OK, step=OK). RULE-07 (DB + màn hình) + RULE-08 (job nền). "
            "DATA-COUNT-001 BẮT BUỘC khi màn có con số đếm. "
            "Evidence: 2 ảnh overview trước/sau + query bot_friend_statistic 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Trang chủ — số bạn bè theo trạng thái đối ứng (対応ステータス別人数) về 0",
       AFTER,
       "1. Trước khi đổi LOA: gán trạng thái đối ứng cho ≥3 bạn bè, ghi lại con số từng trạng thái\n"
       "2. Query bảng status_chat ghi lại cột count của từng trạng thái\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào /basic/overview, quan sát khối 対応ステータス別人数\n"
       "5. Query lại status_chat",
       "≥3 trạng thái đối ứng, mỗi trạng thái ≥1 bạn bè",
       "- DB status_chat: cột count của mọi trạng thái được update về 0\n"
       "- Màn overview: khối 対応ステータス別人数 hiển thị 0 cho tất cả trạng thái\n"
       "- KHÔNG hiển thị bạn bè cũ ở bất kỳ trạng thái nào\n"
       "- Danh sách trạng thái đối ứng (cấu hình) VẪN còn, chỉ số đếm về 0",
       note="Nguồn: Change bot r7-r8 (TR=OK, stg=OK, step=OK). RULE-07 + RULE-08. "
            "Lưu ý phân biệt: XÓA BỘ ĐẾM ≠ xóa cấu hình trạng thái (cấu hình thuộc nhóm 'Setting giữ nguyên'). "
            "Evidence: 2 ảnh khối 対応ステータス別人数 + query status_chat 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "STATE-CLEAN-001", "Normal",
       "Chat 1:1 — danh sách bạn bè LOA cũ bị xóa khỏi DB và khỏi màn hình",
       AFTER,
       "1. Trước khi đổi LOA: vào chat 1:1, ghi lại số bạn bè trong danh sách + chụp ảnh\n"
       "2. Query bảng conversation và bot_line_user, ghi số bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào chat 1:1, quan sát danh sách bạn bè\n"
       "5. Cho 1 friend MỚI kết bạn và gửi tin → quan sát danh sách\n"
       "6. Query lại conversation và bot_line_user",
       "Bot cũ có ≥10 bạn bè trong chat 1:1",
       "- DB conversation: bản ghi của friend cũ bị xóa\n"
       "- DB bot_line_user: bản ghi của friend cũ bị xóa\n"
       "- Màn chat 1:1: KHÔNG hiển thị friend nào của LOA cũ\n"
       "- Friend MỚI kết bạn và gửi tin: xuất hiện trong danh sách và có bản ghi mới trong 2 bảng trên",
       note="Nguồn: Change bot r9-r11 (TR=OK, stg=OK, step=OK) + TC-CBF-083/084 (STATE-CLEAN-001, "
            "QA-spec-016 CONFIRMED). ⚠️ Bill tiền/change_bot r37-r38 ghi staging NG "
            "('chưa hiển thị bạn ở chat 1:1') → case này từng lỗi, RULE-12 mục (3) bắt buộc giữ trong "
            "bộ regression. STATE-CLEAN-001 BẮT BUỘC khi ngắt kết nối bot-OA. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh chat 1:1 + query 2 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Chat 1:1 — bộ đếm tin chưa xác nhận ngoài menu về 0, đếm lại đúng khi có tin mới",
       AFTER,
       "1. Trước khi đổi LOA: để bot cũ có ≥3 tin chưa xác nhận, ghi lại con số hiển thị ngoài menu\n"
       "2. Query bảng bots cột count_user_unconfirm\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Quan sát số tin chưa xác nhận ngoài menu\n"
       "5. Cho 1 friend MỚI gửi tin → quan sát lại con số\n"
       "6. Query lại bots.count_user_unconfirm",
       "Bot cũ có ≥3 tin chưa xác nhận; sau đổi LOA có 1 tin mới",
       "- DB bots.count_user_unconfirm được update về 0\n"
       "- Menu: KHÔNG hiển thị badge số tin chưa xác nhận\n"
       "- Sau khi friend mới gửi tin: badge hiển thị 1 và bots.count_user_unconfirm = 1\n"
       "- Bộ đếm đếm đúng từ 0, không cộng dồn vào số cũ",
       note="Nguồn: Change bot r12-r13 (TR=OK, stg=OK, step=OK). DATA-COUNT-001 BẮT BUỘC. "
            "RULE-07 + RULE-08. Evidence: 3 ảnh badge + query bots 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "LIST-001", "Normal",
       "Chat 1:1 — 3 bộ lọc ở thanh bên trái lọc ra 0 kết quả sau khi đổi LOA",
       AFTER + "\n- Trước khi đổi LOA, bot cũ có friend thỏa mãn CẢ 3 bộ lọc: tin chưa xác nhận · ẩn · đã đặt lịch gửi tin",
       "1. Trước khi đổi LOA: dùng từng bộ lọc, ghi lại số kết quả của 3 bộ lọc\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào chat 1:1, áp bộ lọc tin chưa xác nhận → đếm kết quả\n"
       "4. Áp bộ lọc friend ẩn → đếm kết quả\n"
       "5. Áp bộ lọc đã đặt lịch gửi tin → đếm kết quả",
       "3 bộ lọc: tin chưa xác nhận · friend ẩn · đã đặt lịch gửi tin — mỗi loại ≥1 friend trước khi đổi",
       "- CẢ 3 bộ lọc đều trả về 0 kết quả\n"
       "- Màn hiển thị trạng thái rỗng đúng cách, không lỗi / không spinner vô hạn\n"
       "- Không sót friend cũ nào ở bất kỳ bộ lọc nào",
       note="Nguồn: Change bot r14 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r276. "
            "Gộp 3 bộ lọc vào 1 TC vì CÙNG kết quả mong đợi (0 kết quả) — liệt kê đủ 3 điểm ở Dữ liệu nhập. "
            "RULE-08. Evidence: 3 ảnh kết quả từng bộ lọc.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Chat 1:1 — lịch sử tin nhắn của LOA cũ bị xóa ở toàn bộ bảng lưu tin nhắn",
       AFTER + "\n- Bot cũ có lịch sử tin nhắn ở cả bảng tin hiện hành và bảng lưu trữ theo năm",
       "1. Trước khi đổi LOA: query đếm bản ghi của bot ở bảng messages, messages_page_2, "
       "messages_old, messages_v2s\n"
       "2. Ghi lại số đếm từng bảng\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Query lại 4 bảng đó\n"
       "5. Vào chat 1:1, mở 1 cuộc trò chuyện cũ (nếu còn) để xác nhận không còn tin",
       "4 bảng: messages · messages_page_2 · messages_old · messages_v2s — mỗi bảng ≥1 bản ghi của bot",
       "- CẢ 4 bảng: bản ghi của bot cũ bị xóa (số đếm về 0)\n"
       "- Màn chat 1:1: không mở được cuộc trò chuyện cũ nào, không hiển thị tin nhắn cũ\n"
       "- Không sót bảng lưu trữ nào còn tin của friend cũ",
       note="Nguồn: Change bot r16 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r43. "
            "⚠️ Danh sách bảng tin nhắn có thể đổi theo đợt tách DB (TCsLine_JOB tab「Job move message」) — "
            "RULE-09 cũ & mới song song: phải xác nhận lại danh sách bảng hiện hành trước khi chạy. "
            "DATA-DB-001 BẮT BUỘC. RULE-08. Evidence: query 4 bảng × 2 lần + ảnh chat 1:1.", **PRD),

    tc("Xóa data bot cũ — web", "FUNC-001", "Normal",
       "Chat 1:1 — nhóm tin nhắn (group msg) hiển thị theo LOA mới",
       AFTER + "\n- Bot cũ có nhóm tin nhắn (group msg)",
       "1. Trước khi đổi LOA: ghi lại danh sách nhóm tin nhắn hiển thị\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào chat 1:1, quan sát khu vực nhóm tin nhắn\n"
       "4. Đối chiếu với danh sách đã ghi",
       "Bot cũ có ≥1 nhóm tin nhắn",
       "- Hiển thị nhóm tin nhắn của LOA MỚI\n"
       "- Không hiển thị nhóm tin nhắn gắn với friend của LOA cũ",
       note="Nguồn: Change bot r15 (TR=OK, stg=OK, step=OK, devnote=OK). "
            "⚠️ Nguồn chỉ ghi expected ngắn 'Hiển thị group msg của bot mới' — chưa rõ nhóm cũ bị xóa hay "
            "giữ lại rỗng. Cần Leader chốt. RULE-08. Evidence: 2 ảnh khu vực nhóm tin nhắn.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "STATE-CLEAN-001", "Normal",
       "Màn quản lý chat (talk list) — dữ liệu tin nhắn của LOA cũ bị xóa, màn không còn tin",
       AFTER + "\n- Bot cũ có dữ liệu ở màn talk-list",
       "1. Trước khi đổi LOA: vào /basic/talk-list, ghi lại số dòng hiển thị\n"
       "2. Query bảng messages_v2s và các bảng messages theo năm, ghi số bản ghi\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại /basic/talk-list, quan sát\n"
       "5. Query lại các bảng đó",
       "Bot cũ có ≥5 dòng ở màn talk-list",
       "- DB: bản ghi của bot cũ ở messages_v2s và các bảng messages theo năm bị xóa\n"
       "- Màn talk-list: KHÔNG hiển thị tin nhắn nào của LOA cũ\n"
       "- Màn hiển thị trạng thái rỗng đúng cách",
       note="Nguồn: Change bot r17-r18 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r280. "
            "RULE-07 + RULE-08. Evidence: 2 ảnh talk-list + query DB 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Rich Menu — lịch sử click và bộ đếm friend đang theo rich menu về 0",
       AFTER + "\n- Bot cũ có rich menu đã gán cho friend và có lịch sử click",
       "1. Trước khi đổi LOA: vào màn thống kê rich menu, ghi lại số friend đang theo + số click\n"
       "2. Query bảng detail_click_richmenu đếm bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào màn thống kê rich menu, quan sát các con số\n"
       "5. Query lại detail_click_richmenu",
       "Bot cũ: ≥1 rich menu đã gán ≥3 friend, có ≥5 lượt click",
       "- DB detail_click_richmenu: bản ghi của bot cũ bị xóa\n"
       "- Màn thống kê: số friend đang theo rich menu = 0, số click = 0\n"
       "- Danh sách rich menu (cấu hình) VẪN còn — chỉ bộ đếm và lịch sử bị xóa",
       note="Nguồn: Change bot r19 + r21 (TR=OK, stg=OK). DATA-COUNT-001 BẮT BUỘC. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn thống kê + query detail_click_richmenu 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "MSG-USER-001", "Normal",
       "Rich Menu — rich menu trên LINE của friend LOA cũ bị clear (verify trên LINE app thật)",
       AFTER + "\n- Trước khi đổi LOA, có ≥1 friend của LOA cũ đang hiển thị rich menu trên LINE",
       "1. Trước khi đổi LOA: mở LINE của friend, chụp ảnh rich menu đang hiển thị\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại LINE của friend đó, quan sát khu vực rich menu\n"
       "4. Thử bấm vào vị trí rich menu cũ",
       "1 friend thật của LOA cũ có rich menu đang hiển thị trên LINE",
       "- Trên LINE app của friend: rich menu cũ KHÔNG còn hiển thị\n"
       "- Bấm vào vị trí cũ: không chạy action nào\n"
       "- Không hiển thị rich menu rác / rich menu của bot khác",
       note="Nguồn: Change bot r20 (TR=OK, stg=OK: 'clear richmenu trên line của friend bot cũ') + "
            "TC-CBF-085 (STATE-CLEAN-001, MAP-CANCEL-01 richmenu cleanup pattern). "
            "RULE-06 — BẮT BUỘC verify ở output cuối trên LINE app thật, không dừng ở màn admin. RULE-08. "
            "Evidence: 2 ảnh LINE app của friend trước/sau.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Gửi tin hàng loạt — bộ đếm số đã gửi về 0; LỊCH SỬ gửi giữ hay xóa cần Leader chốt",
       AFTER + "\n- Bot cũ có lịch sử gửi tin hàng loạt: tab đã gửi, tab đặt lịch, tab nháp",
       "1. Trước khi đổi LOA: ghi lại số dòng ở tab đã gửi / đặt lịch / nháp + giá trị cột 配信数\n"
       "2. Query bảng lịch sử gửi, ghi cột send_count\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào 3 tab, đếm số dòng còn lại\n"
       "5. Quan sát cột 配信数 của từng dòng\n"
       "6. Query lại bảng lịch sử gửi",
       "≥2 dòng ở tab đã gửi, ≥1 dòng đặt lịch, ≥1 dòng nháp",
       "- DB: cột send_count được update về 0\n"
       "- Màn: cột 配信数 KHÔNG hiển thị số friend nào (0 hoặc rỗng)\n"
       "- SỐ DÒNG lịch sử: theo đúng kết luận MT-10 (giữ lại theo TC 04/2026, hoặc xóa theo [AI] v2)",
       note="⚠️ MT-10 — MÂU THUẪN TRỰC TIẾP: Change bot r22 ghi 'vẫn giữ lại lịch sử => spec cũ hiện tại "
            "như vậy, chỉ update send_count = 0' (TR=OK, stg=OK); TC-CBF-086 ghi 'lịch sử broadcast/step "
            "delivery/scenario BỊ XÓA' (QA-spec-016). Chưa chốt → số dòng lịch sử KHÔNG assert cứng. "
            "Nguồn: Change bot r22-r23. DATA-COUNT-001. RULE-08. "
            "Evidence: 2 ảnh 3 tab + query cột send_count 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Phát hành theo bước — 3 bộ đếm friend ở màn danh sách scenario về 0",
       AFTER + "\n- Bot cũ có ≥1 scenario đã chạy với 購読中の友だち > 0, 途中で終了した友だち > 0, 読了済の友だち > 0",
       "1. Trước khi đổi LOA: vào màn danh sách scenario, ghi lại 3 con số của từng scenario\n"
       "2. Query bảng scenario, ghi cột count_follow, count_stop, count_unfinish\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào màn danh sách scenario, quan sát 3 cột con số\n"
       "5. Query lại bảng scenario",
       "≥1 scenario với cả 3 con số > 0",
       "- DB scenario: count_follow = 0, count_stop = 0, count_unfinish = 0\n"
       "- Màn danh sách: 3 cột 購読中の友だち / 途中で終了した友だち / 読了済の友だち đều hiển thị 0\n"
       "- Danh sách scenario (cấu hình) VẪN còn đủ, không bị xóa scenario nào",
       note="Nguồn: Change bot r24-r25 (TR=OK, stg=OK, step=OK). DATA-COUNT-001 BẮT BUỘC. "
            "RULE-07 + RULE-08. Evidence: 2 ảnh màn danh sách scenario + query bảng scenario 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "STATE-DEP-001", "Normal",
       "Phát hành theo bước — scenario đang chạy dở của friend LOA cũ dừng hẳn, không gửi tiếp",
       AFTER + "\n- Trước khi đổi LOA, có ≥2 friend đang ở giữa scenario (chưa tới bước cuối)",
       "1. Trước khi đổi LOA: query bảng scenario_step_time, scenario_lineuser, step_message_history "
       "đếm bản ghi của bot\n"
       "2. Ghi lại friend nào đang ở bước nào\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Chờ qua mốc thời gian mà bước tiếp theo của scenario đáng lẽ gửi\n"
       "5. Kiểm tra LINE app của friend cũ: có nhận tin bước tiếp không\n"
       "6. Query lại 3 bảng trên",
       "≥2 friend đang ở giữa scenario; mốc gửi bước tiếp trong vòng 1 giờ sau khi đổi LOA",
       "- DB: bản ghi của bot cũ ở scenario_step_time, scenario_lineuser, step_message_history bị xóa\n"
       "- Friend cũ KHÔNG nhận thêm tin nào của scenario trên LINE app\n"
       "- Không có tin nào bị gửi sang LOA mới thay thế\n"
       "- Không phát sinh lỗi gửi tin trong màn lỗi phát hành",
       note="Nguồn: Change bot r26 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r39 (scenario_lineuser) "
            "+ r44 (step_message_history) + TC-CBF-086. STATE-DEP-001 BẮT BUỘC khi có hành động phụ thuộc "
            "đã lên lịch. RULE-06 (verify trên LINE app) + RULE-08. "
            "Evidence: query 3 bảng × 2 lần + ảnh LINE app friend cũ sau mốc gửi.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Biểu mẫu — số câu trả lời và dữ liệu trả lời của friend LOA cũ bị xóa",
       AFTER + "\n- Bot cũ có ≥1 form có ≥3 câu trả lời của friend cũ",
       "1. Trước khi đổi LOA: vào màn danh sách form, ghi số friend đã trả lời của từng form\n"
       "2. Vào màn kết quả form (tab 1, tab 2), ghi số dòng\n"
       "3. Query các bảng: count formanswer, user_open_formanswer, form_answer_user_accept, "
       "form_answer_result — ghi số bản ghi của bot\n"
       "4. Hoàn tất đổi LOA, chờ job xong\n"
       "5. Vào lại màn danh sách form + màn kết quả, quan sát\n"
       "6. Query lại 4 nhóm bảng trên",
       "≥1 form với ≥3 câu trả lời của friend cũ",
       "- DB: bộ đếm form answer được update về 0; xóa bản ghi ở user_open_formanswer, "
       "form_answer_user_accept, form_answer_result của bot cũ\n"
       "- Màn danh sách form: số friend đã trả lời = 0\n"
       "- Màn kết quả form tab 1 và tab 2: không còn dòng nào\n"
       "- Danh sách form (cấu hình) VẪN còn",
       note="Nguồn: Change bot r27-r28 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r227 "
            "(SpecImprove #33154, 21/01/2026: fix changeNewBotStep1 để clear thêm data friend cũ, "
            "trong đó có 'Formanswer: update count formanswer, xóa data bảng user_open_formanswer, "
            "form_answer_user_accept'). RULE-12 mục (3). DATA-COUNT-001. RULE-08. "
            "Evidence: 2 ảnh màn list + 2 ảnh màn kết quả + query 4 nhóm bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "STATE-DEP-001", "Normal",
       "Biểu mẫu — nhắc lịch (remind) đã đặt cho friend LOA cũ bị hủy, friend không nhận remind",
       AFTER + "\n- Trước khi đổi LOA: form có bật remind và ≥2 friend cũ đang được đặt lịch gửi remind "
       "trong vòng 1 giờ tới",
       "1. Trước khi đổi LOA: query bảng event_step_time đếm bản ghi remind của bot\n"
       "2. Ghi lại mốc thời gian gửi remind của từng friend\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Chờ qua mốc gửi remind\n"
       "5. Kiểm tra LINE app của friend cũ: có nhận remind không\n"
       "6. Query lại event_step_time",
       "≥2 bản ghi remind của friend cũ, mốc gửi trong 1 giờ tới",
       "- Friend cũ KHÔNG nhận được remind nào trên LINE app\n"
       "- DB event_step_time: theo đúng kết luận MT-07 (xóa bản ghi hay giữ lại)\n"
       "- Không có lỗi gửi tin phát sinh trong màn lỗi phát hành",
       note="⚠️ MT-07 — MÂU THUẪN: Change bot r29/r51/r54/r57/r59 nói XÓA event_step_time (TR=OK, stg=OK); "
            "Bill tiền/change_bot r47 (11/2023) nói 'event_step_time → bảng này k xóa'; spec "
            "lesson-booking/job/job-spec.md §3.5 chỉ nói ChangeBotJob xóa calendar_course_bookings + reset "
            "calendar_course_receptions, KHÔNG nhắc event_step_time. Rủi ro nếu KHÔNG xóa: gửi remind cho "
            "người không còn là bạn. STATE-DEP-001 BẮT BUỘC. RULE-06 + RULE-08. "
            "Evidence: ảnh LINE app friend cũ sau mốc gửi + query event_step_time 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "LIFF-ENTRY-001", "Abnormal",
       "Biểu mẫu — link form cũ (LIFF ID cũ) không mở được sau khi đổi LOA",
       AFTER + "\n- Trước khi đổi LOA: LOA cũ đã gửi link form cho friend, friend còn giữ link trong chat",
       "1. Trước khi đổi LOA: gửi link form cho friend, lưu lại URL đầy đủ\n"
       "2. Xác nhận link mở được form bình thường\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Trên LINE app của friend cũ, bấm vào link form cũ\n"
       "5. Quan sát màn hiện ra trên LIFF / trình duyệt",
       "URL form cũ (chứa LIFF ID cũ) đã lưu lại",
       "- Link form cũ KHÔNG mở được form — hiển thị lỗi 404 (hoặc lỗi LIFF rõ ràng)\n"
       "- KHÔNG mở ra form của LOA mới (tránh lẫn dữ liệu giữa 2 LOA)\n"
       "- Không trắng màn, có thông báo người dùng đọc được",
       note="Nguồn: Change bot r30 (TR=OK, stg=OK, step=OK: 'user line hiển thị lỗi 404') + TC-CBF-090 "
            "(DATA-REF-001, TD Section 7.3 — LIFF ID đổi). LIFF-ENTRY-001 BẮT BUỘC khi tính năng phát sinh "
            "URL cho LINE user. RULE-06 — verify trên LINE app thật. RULE-08. "
            "Evidence: URL đã lưu + ảnh màn lỗi trên LINE app.", **PRD),

    tc("Xóa data bot cũ — web", "OUT-EXPORT-001", "Abnormal",
       "Biểu mẫu — nút tải CSV của form LOA cũ bị vô hiệu sau khi đổi LOA",
       AFTER + "\n- Bot cũ có form có dữ liệu CSV tải được",
       "1. Trước khi đổi LOA: vào màn danh sách form và màn thống kê chi tiết, xác nhận nút tải CSV dùng được\n"
       "2. Tải 1 file CSV và lưu lại link tải\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn danh sách form + màn thống kê, quan sát nút tải CSV\n"
       "5. Thử bấm nút tải CSV",
       "Form có ≥3 câu trả lời trước khi đổi LOA",
       "- Nút tải CSV bị DISABLE ở cả màn danh sách và màn thống kê chi tiết\n"
       "- Bấm nút: không tải được file\n"
       "- Nếu tải được: file KHÔNG chứa dữ liệu của friend LOA cũ",
       note="Nguồn: Change bot r31 (TR=OK, stg=OK, step=OK). OUT-EXPORT-001 nâng BẮT BUỘC với mọi chức năng "
            "export CSV. RULE-08. Evidence: 2 ảnh nút tải CSV + ảnh kết quả khi bấm.", **PRD),

    tc("Xóa data bot cũ — web", "INTG-SHEET-001", "Normal",
       "Biểu mẫu — liên kết Google bị mất sau khi đổi LOA, phải liên kết lại rồi sync vào spreadsheet MỚI",
       AFTER + "\n- Trước khi đổi LOA: form đã liên kết Google Spreadsheet và sync được",
       "1. Trước khi đổi LOA: xác nhận form đã liên kết Google và sync câu trả lời vào spreadsheet\n"
       "2. Lưu lại ID spreadsheet đang sync\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào màn cấu hình sync Google của form, quan sát trạng thái liên kết\n"
       "5. Liên kết lại Google, cho 1 friend MỚI trả lời form\n"
       "6. Kiểm tra spreadsheet nào nhận dữ liệu",
       "ID spreadsheet cũ đã lưu; 1 câu trả lời mới sau khi liên kết lại",
       "- Sau khi đổi LOA: liên kết Google bị MẤT, màn cấu hình hiển thị trạng thái chưa liên kết\n"
       "- Sau khi liên kết lại: sync hoạt động bình thường\n"
       "- Dữ liệu sync vào SPREADSHEET MỚI (không phải spreadsheet cũ)\n"
       "- Spreadsheet cũ KHÔNG nhận thêm dòng nào",
       note="⚠️ MT-09 — Change bot r32 (TR=OK, stg=OK, step=OK) ghi 'bot cũ đã liên kết, sau khi change sẽ "
            "bị mất liên kết => phải liên kết lại / sync data bình thường / sync vào spread mới "
            "(anh Tư bảo logic cũ đã như vậy)' NHƯNG r212 (cùng tab) lại ghi booking salon 'sau khi booking "
            "success => Check việc sync google spread và google calendar bình thường' (hàm ý còn liên kết). "
            "2 dòng cùng tab nói khác nhau → cần Leader chốt. INTG-SHEET-001 BẮT BUỘC. RULE-08. "
            "Evidence: 2 ảnh màn cấu hình sync + ảnh 2 spreadsheet.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Quản lý thẻ — bộ đếm người gắn thẻ về 0, cột giới hạn số người hiển thị 'không giới hạn'",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥2 tag đã gắn friend, trong đó ≥1 tag đã đạt giới hạn số người",
       "1. Trước khi đổi LOA: vào màn danh sách tag, ghi cột số người đã gắn + cột 人数制限 của từng tag\n"
       "2. Query bảng tags (cột count user), tag_line_user, action_limit_tags — ghi số bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn danh sách tag, quan sát 2 cột đó\n"
       "5. Query lại 3 bảng",
       "≥2 tag đã gắn friend; ≥1 tag đã đạt giới hạn số người",
       "- DB tags: cột đếm user được xóa/về 0\n"
       "- DB tag_line_user và action_limit_tags: bản ghi của bot cũ bị xóa\n"
       "- Màn danh sách tag: cột số người đã gắn hiển thị「0 人」cho MỌI tag\n"
       "- Cột 人数制限 hiển thị「人数制限なし」cho tag trước đó đã đạt giới hạn\n"
       "- Danh sách tag (cấu hình) VẪN còn đủ",
       note="Nguồn: Change bot r33-r34 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r48 (tag_line_user) "
            "+ TC-CBF-085. DATA-COUNT-001 BẮT BUỘC. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn danh sách tag + query 3 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "STATE-CLEAN-001", "Normal",
       "Danh sách bạn bè — xóa sạch 4 loại friend của LOA cũ, chỉ còn friend của LOA mới",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có đủ 4 loại friend — đang hoạt động · đã ẩn · "
       "bị bot chặn · đang chặn bot",
       "1. Trước khi đổi LOA: vào 4 màn (danh sách chính + 3 màn phụ), ghi số friend từng màn\n"
       "2. Query bảng conversation, bot_line_user, line_user — ghi số bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào màn danh sách bạn bè chính, quan sát\n"
       "5. Bấm vào 3 màn phụ (friend ẩn, bị bot chặn, đang chặn bot), quan sát\n"
       "6. Query lại 3 bảng",
       "Mỗi loại friend ≥1 bản ghi (tổng ≥4 friend)",
       "- DB conversation + bot_line_user + line_user: bản ghi friend cũ bị xóa\n"
       "- Màn danh sách chính: CHỈ hiển thị friend đang hoạt động của LOA MỚI\n"
       "- CẢ 3 màn phụ đều KHÔNG có dữ liệu nào\n"
       "- Không sót friend cũ ở bất kỳ màn nào trong 4 màn",
       note="Nguồn: Change bot r35-r36 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r298 + TC-CBF-083. "
            "STATE-CLEAN-001 BẮT BUỘC. RULE-07 + RULE-08. "
            "Evidence: 4 ảnh trước + 4 ảnh sau + query 3 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "OUT-EXPORT-001", "Abnormal",
       "Quản lý CSV — link tải file CSV CŨ sau khi đổi LOA: 404 hay vẫn tải được (cần Leader chốt)",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥1 file CSV đã xuất, đã lưu link tải",
       "1. Trước khi đổi LOA: vào /basic/csv-management, xuất 1 file CSV\n"
       "2. LƯU LẠI link download đầy đủ của file CSV đó\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Dán lại link download CŨ vào trình duyệt, Enter\n"
       "5. Quan sát kết quả: tải được file hay lỗi 404\n"
       "6. Nếu tải được: mở file kiểm tra có chứa dữ liệu friend LOA cũ không",
       "Link download CSV cũ đã lưu (VD https://<domain>/msg_template/csv/<bot>/CSV_xxx.csv)",
       "- GHI NHẬN kết quả thật theo đúng kết luận MT-08 của Leader\n"
       "- Nếu Leader chốt phải 404: truy cập link cũ → lỗi 404, không tải được file\n"
       "- Nếu file vẫn tải được: file KHÔNG được chứa dữ liệu friend của LOA cũ (nếu có → raise bug rò rỉ PII)",
       note="⚠️ MT-08 — TC gốc ghi expected 'truy cập lại link download CSV cũ => Ra lỗi 404' nhưng ghi chú "
            "thực tế: 'nhấn reset => download lại data mới rồi nhưng khi down link cũ VẪN down được "
            "(anh Tư bảo logic cũ đã như vậy) — Bug Tester #33938'. Change bot r37 đánh TR=OK trong khi "
            "AddBot/Testcase r299 (CÙNG nội dung) đánh NG. Expected và hành vi thật KHÁC NHAU → Leader phải "
            "chốt: sửa expected hay raise bug. Rủi ro: link cũ tải được = rò rỉ dữ liệu friend LOA cũ (PII). "
            "OUT-EXPORT-001 + SEC-001. RULE-08. Evidence: link cũ + ảnh kết quả + nội dung file nếu tải được.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Quản lý CSV — cột số người đối tượng hiển thị theo friend LOA mới; tải CSV mới ra data mới",
       AFTER + "\n- Bot cũ có ≥1 cấu hình CSV với cột 対象人数 > 0",
       "1. Trước khi đổi LOA: ghi lại giá trị cột 対象人数 của từng dòng CSV\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Cho ≥2 friend MỚI kết bạn với LOA mới\n"
       "4. Vào /basic/csv-management, quan sát cột 対象人数\n"
       "5. Bấm tải CSV và mở file kiểm tra nội dung",
       "2 friend mới của LOA mới",
       "- Cột 対象人数 hiển thị số friend của LOA MỚI (khớp số friend thật, VD 2)\n"
       "- Không hiển thị số cũ của LOA cũ\n"
       "- File CSV tải về chứa ĐÚNG dữ liệu friend của LOA mới, không có friend cũ",
       note="Nguồn: Change bot r38 (TR=OK, stg=OK, step=OK) + r37 ('Click download CSV ở bot mới: "
            "sẽ export ra data của bot mới'). DATA-COUNT-001 + OUT-EXPORT-001. RULE-08. "
            "Evidence: 2 ảnh cột 対象人数 + nội dung file CSV mới.", **PRD),

    tc("Xóa data bot cũ — web", "FRIEND-001", "Normal",
       "Quản lý thông tin bạn bè — mọi loại thông tin về 0 người trả lời, giá trị friend cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: friend của LOA cũ đã có giá trị ở TẤT CẢ loại thông tin bạn bè",
       "1. Trước khi đổi LOA: vào màn danh sách thông tin bạn bè, ghi số người trả lời của TỪNG loại\n"
       "2. Query bảng friend_information_setting (cột total_user_has_value) và friend_information_value\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào màn danh sách thông tin bạn bè, quan sát số người trả lời của từng loại\n"
       "5. Bấm xem chi tiết danh sách của ≥3 loại bất kỳ\n"
       "6. Query lại 2 bảng",
       "Đủ các loại: thông tin cơ bản (tên hệ thống, SĐT, mail, ngày sinh) · địa chỉ (mã bưu chính, "
       "tỉnh, thành phố, quận, địa chỉ) · loại khác (text, ngày, điểm, chọn, ảnh, PDF)",
       "- DB friend_information_setting: total_user_has_value = 0 cho MỌI loại\n"
       "- DB friend_information_value: bản ghi của friend cũ bị xóa\n"
       "- Màn danh sách: số người trả lời = 0 cho TẤT CẢ loại thông tin (không sót loại nào)\n"
       "- Xem chi tiết: không có kết quả nào\n"
       "- Cấu hình các loại thông tin bạn bè VẪN còn",
       note="Nguồn: Change bot r39-r40 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r227 "
            "(SpecImprove #33154: 'Friend info: update count'). FRIEND-001 BẮT BUỘC khi chức năng đọc/ghi "
            "friend info. DATA-COUNT-001. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn danh sách (đủ mọi loại) + 3 ảnh chi tiết + query 2 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Lịch hẹn hành động — lịch sử đã chạy của friend LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥1 lịch hẹn hành động ĐÃ chạy với lịch sử",
       "1. Trước khi đổi LOA: vào màn chi tiết lịch hẹn, tab 実行履歴, ghi số dòng\n"
       "2. Query bảng action_schedule_history và action_schedules_line_users — ghi số bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn chi tiết lịch hẹn, tab 実行履歴, quan sát\n"
       "5. Query lại 2 bảng",
       "≥1 lịch hẹn đã chạy với ≥3 dòng lịch sử",
       "- DB action_schedule_history + action_schedules_line_users: bản ghi của bot cũ bị xóa\n"
       "- Tab 実行履歴: KHÔNG còn dòng dữ liệu nào\n"
       "- Cấu hình lịch hẹn VẪN còn",
       note="Nguồn: Change bot r41-r42 (TR=OK, stg=OK, step=OK). DATA-DB-001 BẮT BUỘC với DELETE. "
            "RULE-07 + RULE-08. Evidence: 2 ảnh tab 実行履歴 + query 2 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "STATE-DEP-001", "Normal",
       "Lịch hẹn hành động — friend LOA cũ không chạy tiếp; friend LOA mới thỏa điều kiện chạy bình thường",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có lịch hẹn hành động đang chờ chạy cho ≥2 friend cũ\n"
       "- Mốc chạy nằm trong 1 giờ sau khi đổi LOA",
       "1. Trước khi đổi LOA: ghi lại friend nào đang chờ chạy lịch hẹn và mốc thời gian\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Chờ qua mốc chạy lịch hẹn\n"
       "4. Kiểm tra LINE app của friend cũ: có nhận action (tin/tag) không\n"
       "5. Cho 1 friend MỚI thỏa điều kiện lịch hẹn đó, chờ tới mốc chạy\n"
       "6. Kiểm tra friend mới có được chạy action không",
       "≥2 friend cũ đang chờ; 1 friend mới thỏa điều kiện",
       "- Friend CŨ: KHÔNG chạy action nào (không nhận tin, không được gắn tag)\n"
       "- Friend MỚI thỏa điều kiện: chạy action bình thường, nhận đúng kết quả\n"
       "- Không lỗi phát hành phát sinh",
       note="Nguồn: Change bot r43 (TR=OK, stg=OK, step=OK). STATE-DEP-001 BẮT BUỘC. "
            "RULE-06 (verify trên LINE app) + RULE-08. "
            "Evidence: ảnh LINE app friend cũ + ảnh LINE app friend mới + ảnh tag đã gắn.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "QR Code Action — toàn bộ số liệu thống kê click/quét của LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥1 QR code action có dữ liệu click/quét",
       "1. Trước khi đổi LOA: vào màn danh sách QR code action, ghi cột số friend\n"
       "2. Vào màn chi tiết thống kê: ghi số liệu ở tab theo ngày, tab theo friend, tab LP, tab thống kê, "
       "các thanh trượt\n"
       "3. Query bảng detail_landing_click, collect_open_landings, landing_histories, time_action_landing\n"
       "4. Hoàn tất đổi LOA, chờ job xong\n"
       "5. Vào lại 2 màn trên, quan sát từng con số\n"
       "6. Query lại 4 bảng",
       "≥1 QR code action có ≥5 lượt quét và ≥3 friend",
       "- DB: bản ghi của bot cũ ở detail_landing_click, collect_open_landings, landing_histories, "
       "time_action_landing đều bị xóa\n"
       "- Màn danh sách: cột số friend = 0\n"
       "- Màn chi tiết: số liệu ở TẤT CẢ tab (theo ngày, theo friend, LP, thống kê) và các thanh trượt = 0\n"
       "- Cấu hình QR code action VẪN còn",
       note="Nguồn: Change bot r44-r45 (TR=OK, stg=OK, step=OK; ghi chú r45 'count action ở màn list vẫn "
            "hiển thị') + Bill tiền/change_bot r40 + r45 + AddBot/Testcase r227 (SpecImprove #33154: "
            "'Landing: xóa data bảng detail_landing_click, collect_open_landing, landing_histories'). "
            "⚠️ Đối chiếu spec qr-landing/db/db-mapping.md:1730: ChangeBotJob dọn ĐÚNG 4 bảng này theo bot_id, "
            "và reset landing.total_user_click/total_user_friend/count_action/count_action_web về 0 "
            "(db-mapping.md:220-223) — spec này KHỚP TC. DATA-COUNT-001. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn list + 2 ảnh màn chi tiết đủ tab + query 4 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "LIFF-ENTRY-001", "Abnormal",
       "QR Code Action — link QR và ảnh QR CŨ sau khi đổi LOA không còn dẫn về LOA cũ",
       AFTER + "\n- Trước khi đổi LOA: đã lưu link QR code action cũ + tải ảnh QR cũ về máy",
       "1. Trước khi đổi LOA: lưu lại URL QR code action và tải ảnh QR về máy\n"
       "2. Xác nhận quét ảnh QR cũ dẫn tới LOA cũ bình thường\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Dán URL QR cũ vào trình duyệt, quan sát\n"
       "5. Quét ảnh QR cũ bằng LINE trên điện thoại, quan sát",
       "URL QR cũ + ảnh QR cũ đã lưu",
       "- Truy cập URL QR cũ: KHÔNG dẫn tới LOA cũ; hiển thị lỗi hoặc dẫn tới LOA mới theo kết luận Leader\n"
       "- Quét ảnh QR cũ: ghi nhận hành vi thật (lỗi / dẫn tới LOA mới / không làm gì)\n"
       "- KHÔNG chạy action của QR code action cũ\n"
       "- Không gắn tag / không gửi tin theo cấu hình cũ",
       note="Nguồn: Change bot r46 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r308. "
            "⚠️ TC gốc CHỈ GHI CÁCH TEST, KHÔNG ghi kết quả mong đợi cụ thể ('Cách test: trước khi change "
            "bot lưu lại link QR code cũ và ảnh QR cũ; sau khi change bot access vào link QR code cũ và quét "
            "ảnh QR code cũ') → expected ở TC này do AI viết dựa trên TC-CBF-087 (MAP-CANCEL-03 'QR không "
            "còn chạy action sau khi liên kết cũ mất hiệu lực'), CẦN LEADER XÁC NHẬN. "
            "LIFF-ENTRY-001 BẮT BUỘC. RULE-06 + RULE-08. Evidence: ảnh 2 kết quả + ảnh LINE app.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "OUT-EXPORT-001", "Normal",
       "QR Code Action — file CSV tải về sau khi đổi LOA không chứa dữ liệu click của LOA cũ",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có dữ liệu click QR",
       "1. Trước khi đổi LOA: tải CSV từ màn danh sách và màn chi tiết thống kê, ghi số dòng\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Tải lại CSV từ màn danh sách\n"
       "4. Tải lại CSV từ màn chi tiết thống kê\n"
       "5. Mở 2 file, đếm số dòng dữ liệu click",
       "Bot cũ có ≥5 lượt click QR trước khi đổi",
       "- CẢ 2 file CSV (từ màn danh sách và màn chi tiết) KHÔNG chứa dòng click nào của LOA cũ\n"
       "- File chỉ có dòng tiêu đề hoặc dữ liệu của LOA mới\n"
       "- Không lỗi khi tải file",
       note="Nguồn: Change bot r47 (TR=OK, stg=OK, step=OK). OUT-EXPORT-001 nâng BẮT BUỘC. RULE-08. "
            "Evidence: nội dung 2 file CSV trước/sau.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Popup — dữ liệu thống kê lượt click popup của friend LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có popup đã có dữ liệu thống kê lượt click",
       "1. Trước khi đổi LOA: vào màn thống kê chi tiết popup, ghi số friend click\n"
       "2. Query bảng detail_action_popup đếm bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn thống kê chi tiết popup, quan sát\n"
       "5. Query lại detail_action_popup",
       "≥1 popup có ≥3 friend đã click",
       "- DB detail_action_popup: bản ghi friend click của bot cũ bị xóa\n"
       "- Màn thống kê: bộ đếm danh sách friend = 0, không còn friend nào\n"
       "- Cấu hình popup VẪN còn",
       note="Nguồn: Change bot r48-r49 (TR=OK, stg=OK, step=OK). DATA-COUNT-001. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn thống kê + query detail_action_popup 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Đặt lịch bài học — đặt chỗ của friend LOA cũ bị xóa và bộ đếm chỗ được reset",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥3 đặt chỗ bài học của friend cũ ở nhiều trạng thái",
       "1. Trước khi đổi LOA: vào màn quản lý lịch bài học, ghi số đặt chỗ theo từng trạng thái\n"
       "2. Query bảng calendar_course_bookings (số bản ghi) và calendar_course_receptions "
       "(các cột total_booking, total_approve, total_request, total_request_cancel, "
       "total_request_booking_wait_cancel, total_cancel)\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn quản lý lịch bài học, quan sát\n"
       "5. Query lại 2 bảng",
       "≥3 đặt chỗ ở các trạng thái: đã duyệt · chờ duyệt · chờ hủy",
       "- DB calendar_course_bookings: đặt chỗ của friend bot cũ bị XÓA\n"
       "- DB calendar_course_receptions: CẢ 6 cột bộ đếm được reset (total_booking, total_approve, "
       "total_request, total_request_cancel, total_request_booking_wait_cancel, total_cancel)\n"
       "- Màn quản lý: KHÔNG hiển thị đặt chỗ nào của friend cũ\n"
       "- Cấu hình lịch/khóa học VẪN còn",
       note="Nguồn: Change bot r50 + r52 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r227 "
            "(SpecImprove #33154: 'Lesson: Xóa booking của friend bot cũ'). "
            "✅ Điểm TC và SPEC KHỚP NHAU: lesson-booking/job/job-spec.md §3.5 ghi ChangeBotJob.step6FinalCleanup "
            "chạy deleteCalendarCourseBookingByBotId() + resetCalendarCourseReceptionsByBotId() với SQL thật "
            "(ChangeBotDataCleanupRepository.java:285-298). DATA-DB-001 BẮT BUỘC. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn quản lý + query 2 bảng × 2 lần (đủ 6 cột).", **PRD),

    tc("Xóa data bot cũ — web", "STATE-DEP-001", "Normal",
       "Đặt lịch bài học — nhắc lịch bài học của friend LOA cũ bị hủy",
       AFTER + "\n- Trước khi đổi LOA: có ≥2 friend cũ đang được đặt lịch nhắc bài học trong 1 giờ tới",
       "1. Trước khi đổi LOA: query event_step_time, ghi bản ghi nhắc lịch bài học của bot\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Chờ qua mốc gửi nhắc lịch\n"
       "4. Kiểm tra LINE app friend cũ có nhận nhắc lịch không\n"
       "5. Query lại event_step_time",
       "≥2 bản ghi nhắc lịch bài học, mốc gửi trong 1 giờ tới",
       "- Friend cũ KHÔNG nhận nhắc lịch bài học nào trên LINE app\n"
       "- DB event_step_time: theo đúng kết luận MT-07\n"
       "- Không lỗi gửi tin phát sinh",
       note="⚠️ MT-07. Nguồn: Change bot r51 (TR=OK, stg=OK, step=OK). STATE-DEP-001. "
            "RULE-06 + RULE-08. Evidence: ảnh LINE app + query event_step_time 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Đặt lịch salon — đặt chỗ và nhắc lịch của friend LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥3 đặt chỗ salon của friend cũ và ≥1 nhắc lịch salon chờ gửi",
       "1. Trước khi đổi LOA: vào màn quản lý đặt lịch salon, ghi số đặt chỗ\n"
       "2. Query bảng calendar_salon_line_booking và event_step_time (nhắc lịch salon)\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn quản lý đặt lịch salon, quan sát\n"
       "5. Chờ qua mốc gửi nhắc lịch, kiểm tra LINE app friend cũ\n"
       "6. Query lại 2 bảng",
       "≥3 đặt chỗ salon; ≥1 nhắc lịch chờ gửi trong 1 giờ tới",
       "- DB calendar_salon_line_booking: đặt chỗ của friend cũ bị xóa\n"
       "- Màn quản lý salon: KHÔNG hiển thị đặt chỗ của friend cũ\n"
       "- Friend cũ KHÔNG nhận nhắc lịch salon trên LINE app\n"
       "- DB event_step_time: theo kết luận MT-07\n"
       "- Cấu hình lịch salon / nhân sự VẪN còn",
       note="⚠️ MT-07 (phần event_step_time). Nguồn: Change bot r53-r55 (TR=OK, stg=OK, step=OK) + "
            "AddBot/Testcase r227 ('Salon: Xóa booking của friend bot cũ'). DATA-DB-001 + STATE-DEP-001. "
            "RULE-06 + RULE-07 + RULE-08. Evidence: 2 ảnh màn salon + ảnh LINE app + query 2 bảng × 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Đặt lịch sự kiện — đặt chỗ và nhắc lịch sự kiện của friend LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥3 đặt chỗ sự kiện của friend cũ và ≥1 nhắc lịch chờ gửi",
       "1. Trước khi đổi LOA: vào màn quản lý đặt lịch sự kiện, ghi số đặt chỗ\n"
       "2. Query bảng b_user_booking, user_event và event_step_time\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn quản lý sự kiện, quan sát\n"
       "5. Chờ qua mốc nhắc lịch, kiểm tra LINE app friend cũ\n"
       "6. Query lại 3 bảng",
       "≥3 đặt chỗ sự kiện; ≥1 nhắc lịch chờ gửi",
       "- DB b_user_booking: đặt chỗ của friend cũ bị xóa\n"
       "- DB user_event: bản ghi tương ứng bị xóa\n"
       "- Màn quản lý sự kiện: KHÔNG hiển thị đặt chỗ của friend cũ\n"
       "- Friend cũ KHÔNG nhận nhắc lịch sự kiện trên LINE app\n"
       "- DB event_step_time: theo kết luận MT-07",
       note="⚠️ MT-07 (phần event_step_time). Nguồn: Change bot r56-r58 (TR=OK, stg=OK, step=OK) + "
            "Bill tiền/change_bot r46 (user_event). DATA-DB-001 + STATE-DEP-001. "
            "RULE-06 + RULE-07 + RULE-08. Evidence: 2 ảnh màn sự kiện + ảnh LINE app + query 3 bảng × 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "STATE-DEP-001", "Normal",
       "Gửi nhắc lịch — friend LOA cũ bị xóa khỏi danh sách đang phát hành",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥2 friend cũ trong danh sách 配信中 của nhắc lịch",
       "1. Trước khi đổi LOA: vào /basic/events, ghi số friend ở trạng thái 配信中\n"
       "2. Query bảng event_step_time đếm bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại /basic/events, quan sát danh sách 配信中\n"
       "5. Query lại event_step_time",
       "≥2 friend trong danh sách 配信中",
       "- Màn nhắc lịch: KHÔNG còn friend cũ nào ở trạng thái 配信中\n"
       "- DB event_step_time: theo kết luận MT-07 (xóa bản ghi hay giữ)\n"
       "- Cấu hình nhắc lịch VẪN còn",
       note="⚠️ MT-07 — đây là điểm CHÍNH của mâu thuẫn (Change bot r59-r60 nói xóa event_step_time, "
            "Bill tiền/change_bot r47 nói không xóa). STATE-DEP-001. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh danh sách 配信中 + query event_step_time 2 lần.",
       spec="Đã hỏi leader", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Sản phẩm — lịch sử mua hàng của friend LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥2 friend cũ đã mua sản phẩm (cả đơn lẻ và định kỳ)",
       "1. Trước khi đổi LOA: vào màn lịch sử mua hàng, ghi số đơn và danh sách friend đã mua\n"
       "2. Query bảng s_cycle_order_history, s_order_history, s_order_history_notify\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại màn lịch sử mua hàng, quan sát\n"
       "5. Query lại 3 bảng",
       "≥2 friend đã mua: ≥1 sản phẩm đơn lẻ, ≥1 sản phẩm định kỳ",
       "- DB s_cycle_order_history + s_order_history + s_order_history_notify: bản ghi của friend cũ bị xóa\n"
       "- Màn lịch sử mua hàng: KHÔNG còn friend cũ nào\n"
       "- Cấu hình sản phẩm VẪN còn",
       note="Nguồn: Change bot r61-r62 (TR=OK, stg=OK, step=OK) + TC-CBF-088. DATA-DB-001 BẮT BUỘC. "
            "RULE-07 + RULE-08. Evidence: 2 ảnh màn lịch sử + query 3 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "PAY-BATCH-001", "Normal",
       "Sản phẩm định kỳ — friend LOA cũ KHÔNG bị trừ tiền ở chu kỳ tiếp theo",
       AFTER + "\n- Trước khi đổi LOA: có ≥1 friend cũ đang mua sản phẩm ĐỊNH KỲ, chu kỳ bill tiếp theo "
       "nằm trong 2 ngày tới",
       "1. Trước khi đổi LOA: query s_cycle_order_history, ghi lại đơn định kỳ + mốc bill tiếp theo\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Query lại s_cycle_order_history xác nhận bản ghi đã bị xóa\n"
       "4. Chờ qua mốc bill tiếp theo\n"
       "5. Kiểm tra lịch sử giao dịch phía cổng thanh toán + màn lịch sử mua hàng\n"
       "6. Kiểm tra LINE app friend cũ có nhận thông báo bill không",
       "≥1 đơn định kỳ với mốc bill trong 2 ngày tới",
       "- DB s_cycle_order_history: bản ghi đơn định kỳ của friend cũ đã bị xóa\n"
       "- Qua mốc bill: KHÔNG phát sinh giao dịch trừ tiền nào cho friend cũ ở cổng thanh toán\n"
       "- Friend cũ KHÔNG nhận thông báo bill trên LINE\n"
       "- Không phát sinh dòng lịch sử mua hàng mới",
       note="Nguồn: Change bot r63 (TR=OK, stg=OK, step=OK: 'Check các item bill chu kỳ của friend cũ: "
            "sẽ không bị bill nữa => check data trong bảng s_cycle_order_history đã bị xóa thì sẽ không "
            "bill nữa'). PAY-BATCH-001 BẮT BUỘC khi có batch tác động TIỀN. RULE-06 (verify ở cổng thanh "
            "toán + LINE) + RULE-08 (bill tiền KHÔNG kết luận từ staging). "
            "Evidence: query DB 2 lần + ảnh lịch sử giao dịch cổng thanh toán + ảnh LINE app.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Phân tích URL — toàn bộ URL ngắn và dữ liệu click của LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥2 URL ngắn có dữ liệu click",
       "1. Trước khi đổi LOA: vào /basic/url, ghi danh sách URL ngắn + số click từng URL\n"
       "2. Lưu lại 1 URL ngắn để test truy cập sau\n"
       "3. Query bảng url_shorten, url_detail_shorten, detail_url_click\n"
       "4. Hoàn tất đổi LOA, chờ job xong\n"
       "5. Vào lại /basic/url, quan sát danh sách\n"
       "6. Query lại 3 bảng + thử truy cập URL ngắn đã lưu",
       "≥2 URL ngắn, mỗi URL ≥3 lượt click; 1 URL ngắn đã lưu để test",
       "- DB url_shorten + url_detail_shorten + detail_url_click: bản ghi của bot cũ bị xóa\n"
       "- Màn /basic/url: KHÔNG còn URL ngắn nào của LOA cũ\n"
       "- Truy cập URL ngắn đã lưu: không còn dẫn đi đâu (lỗi), không chạy action",
       note="Nguồn: Change bot r64-r65 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r49-r50. "
            "DATA-DB-001 BẮT BUỘC. RULE-07 + RULE-08. "
            "Evidence: 2 ảnh màn /basic/url + query 3 bảng × 2 lần + ảnh kết quả truy cập URL ngắn.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Phân tích chéo — dữ liệu phân tích của friend LOA cũ bị xóa, áp dụng friend LOA mới",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥1 mục phân tích chéo có dữ liệu friend",
       "1. Trước khi đổi LOA: vào /basic/cross-analysis, ghi số liệu thống kê\n"
       "2. Query bảng cross_analysis_items và cross_item_line_user\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Cho ≥2 friend MỚI kết bạn và tạo dữ liệu phù hợp\n"
       "5. Vào lại /basic/cross-analysis, quan sát\n"
       "6. Query lại 2 bảng",
       "≥1 mục phân tích với ≥3 friend cũ; 2 friend mới sau khi đổi",
       "- DB cross_analysis_items + cross_item_line_user: bản ghi của bot cũ bị xóa\n"
       "- Màn thống kê: KHÔNG hiển thị dữ liệu của friend LOA cũ\n"
       "- Màn thống kê ÁP DỤNG dữ liệu friend của LOA MỚI (2 friend mới được tính)",
       note="Nguồn: Change bot r66-r67 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r227 "
            "(SpecImprove #33154: 'Cross analysic: Xóa data bảng cross_analysis_items, cross_item_line_user'). "
            "DATA-DB-001. RULE-07 + RULE-08. Evidence: 2 ảnh màn phân tích + query 2 bảng × 2 lần.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-COUNT-001", "Normal",
       "Chuyển đổi — số người phản hồi (反応人数) của LOA cũ bị xóa",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥1 mục chuyển đổi có 反応人数 > 0",
       "1. Trước khi đổi LOA: vào /basic/conversion, ghi giá trị cột 反応人数 của từng mục\n"
       "2. Query bảng conversion_result đếm bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại /basic/conversion, quan sát cột 反応人数\n"
       "5. Query lại conversion_result",
       "≥1 mục chuyển đổi với 反応人数 ≥ 3",
       "- DB conversion_result: bản ghi của bot cũ bị xóa\n"
       "- Màn chuyển đổi: cột 反応人数 = 0 cho mọi mục\n"
       "- Cấu hình mục chuyển đổi VẪN còn",
       note="Nguồn: Change bot r68-r69 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r42. "
            "DATA-COUNT-001. RULE-07 + RULE-08. Evidence: 2 ảnh màn chuyển đổi + query conversion_result.", **PRD),

    tc("Xóa data bot cũ — web", "OUT-PREVIEW-001", "Normal",
       "Danh sách tài khoản gửi thử / test nhanh của LOA cũ bị xóa ở cả scenario và mẫu tin nhắn",
       AFTER + "\n- Trước khi đổi LOA: bot cũ đã thêm ≥1 tài khoản gửi thử và ≥1 tài khoản test nhanh",
       "1. Trước khi đổi LOA: vào màn chi tiết scenario, ghi danh sách tài khoản gửi thử + test nhanh\n"
       "2. Vào màn danh sách mẫu tin nhắn, ghi danh sách tương ứng\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Vào lại 2 màn trên, quan sát danh sách tài khoản\n"
       "5. Thêm mới 1 tài khoản gửi thử + 1 tài khoản test nhanh cho LOA mới và gửi thử",
       "≥1 tài khoản gửi thử + ≥1 tài khoản test nhanh ở cả 2 màn",
       "- Màn chi tiết scenario: KHÔNG còn tài khoản gửi thử nào, KHÔNG còn tài khoản test nhanh nào\n"
       "- Màn danh sách mẫu tin nhắn: tương tự, không còn tài khoản nào\n"
       "- Thêm mới được tài khoản gửi thử + test nhanh cho LOA mới\n"
       "- Gửi thử tới tài khoản mới: nhận được tin trên LINE app",
       note="Nguồn: Change bot r70-r71 (TR=OK, stg=OK, step=OK). OUT-PREVIEW-001 BẮT BUỘC khi chức năng có "
            "chế độ preview hoặc test send. RULE-06 + RULE-08. "
            "Evidence: 4 ảnh danh sách trước/sau + ảnh tin nhận được trên LINE.", **PRD),

    tc("Xóa data bot cũ — web", "MSG-USER-001", "Normal",
       "Mã QR kết bạn sinh ra sau khi đổi LOA trỏ đúng vào LOA MỚI",
       AFTER,
       "1. Sau khi đổi LOA, vào màn có mã QR kết bạn của bot\n"
       "2. Quan sát mã QR được sinh ra\n"
       "3. Dùng điện thoại (chưa kết bạn LOA mới) quét mã QR đó\n"
       "4. Quan sát LOA nào hiện ra trên LINE\n"
       "5. Bấm kết bạn và kiểm tra friend xuất hiện ở đâu",
       "1 điện thoại chưa kết bạn với LOA mới",
       "- Mã QR sinh ra trỏ vào LOA MỚI (không phải LOA cũ)\n"
       "- Quét mã: LINE mở đúng LOA MỚI (tên bot khớp)\n"
       "- Bấm kết bạn: friend xuất hiện trong danh sách bạn bè của bot trên L Message\n"
       "- Friend nhận được tin chào mừng nếu có cấu hình",
       note="Nguồn: Change bot r72-r73 (TR=OK, step=OK). MSG-USER-001 BẮT BUỘC khi tương tác với friend LINE. "
            "RULE-06 — verify trên LINE app thật. RULE-08. "
            "Evidence: ảnh mã QR + ảnh LINE app sau khi quét + ảnh danh sách bạn bè.", **PRD),

    tc("Xóa data bot cũ — web", "DATA-DB-001", "Normal",
       "Lỗi phát hành — danh sách tin nhắn lỗi của LOA cũ không còn hiển thị",
       AFTER + "\n- Trước khi đổi LOA: bot cũ có ≥2 dòng trong màn lỗi phát hành",
       "1. Trước khi đổi LOA: vào /basic/error-list-v2, ghi số dòng lỗi\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào lại /basic/error-list-v2, quan sát danh sách\n"
       "4. Đối chiếu với số dòng đã ghi",
       "≥2 dòng lỗi phát hành của LOA cũ",
       "- Màn lỗi phát hành: KHÔNG hiển thị dòng lỗi nào của LOA cũ\n"
       "- Màn hiển thị trạng thái rỗng đúng cách\n"
       "- Lỗi phát sinh MỚI của LOA mới (nếu có) vẫn hiển thị được",
       note="Nguồn: Change bot r74 (CHỈ có step=OK, cột Test Result + staging TRỐNG — chưa chạy trên dev/staging) "
            "+ TC-CBF-086. ⚠️ RISK: case chưa có kết quả chạy đầy đủ. RULE-08. "
            "Evidence: 2 ảnh màn lỗi phát hành.", **PRD),
]

S11 = [
    # ═══════════════ 11. Xóa data bot cũ — app mobile ═══════════════
    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — bộ đếm thông báo của LOA cũ bị xóa, không còn badge thông báo",
       AFTER + "\n- Có app mobile đã đăng nhập cùng tài khoản Admin\n"
       "- Trước khi đổi LOA: số thông báo trên app của LOA cũ > 0",
       "1. Trước khi đổi LOA: mở app mobile, ghi lại số thông báo hiển thị + chụp ảnh icon\n"
       "2. Query bảng mobile_notify đếm bản ghi của bot\n"
       "3. Hoàn tất đổi LOA, chờ job xong\n"
       "4. Mở lại app mobile (đóng/mở app để tải lại), quan sát số thông báo\n"
       "5. Bấm vào chi tiết danh sách thông báo\n"
       "6. Query lại mobile_notify",
       "Số thông báo app của LOA cũ ≥3",
       "- DB mobile_notify: bản ghi của bot cũ bị xóa\n"
       "- App mobile: số thông báo của LOA mới = 0\n"
       "- Bấm chi tiết: danh sách thông báo trống\n"
       "- Icon thông báo KHÔNG hiển thị dấu hiệu có thông báo mới",
       note="Nguồn: Change bot r75 (TR=OK, stg=OK, step=OK) + Bill tiền/change_bot r41 (mobile_notify). "
            "⚠️ Ghi chú gốc r75: 'Landing k có notify nhưng vẫn hiển thị icon có notify' — đây là BUG UI đã "
            "ghi nhận, phải verify lại badge icon chứ không chỉ con số. SYNC-APP-001. RULE-06 (output cuối "
            "trên app thật) + RULE-07 + RULE-08. Evidence: 2 ảnh app mobile + query mobile_notify 2 lần.", **PRD),

    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — phần chọn bot hiển thị LOA MỚI sau khi đổi",
       AFTER + "\n- Có app mobile đã đăng nhập\n- Trước khi đổi LOA: app đang chọn LOA cũ",
       "1. Trước khi đổi LOA: mở app, xác nhận đang chọn LOA cũ, chụp ảnh tên bot\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app mobile\n"
       "4. Quan sát phần chọn bot: tên bot hiển thị là gì\n"
       "5. Mở danh sách bot trong app, đối chiếu",
       "App đang chọn LOA cũ trước khi đổi",
       "- Phần chọn bot hiển thị tên LOA MỚI\n"
       "- Không còn tên LOA cũ trong danh sách bot\n"
       "- App không bị lỗi / không crash khi bot bị đổi dưới chân",
       group="UI",
       note="Nguồn: Change bot r76 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r335. "
            "SYNC-APP-001. RULE-06 + RULE-08. Evidence: 2 ảnh app phần chọn bot.", **PRD),

    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — màn chat 1:1 hiển thị friend của LOA mới, bộ đếm tin chưa xác nhận = 0",
       AFTER + "\n- Có app mobile đã đăng nhập\n- Trước khi đổi LOA: bot cũ có tin chưa xác nhận > 0",
       "1. Trước khi đổi LOA: mở app, vào màn chat 1:1, ghi số tin chưa xác nhận + số friend\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app, vào màn chat 1:1\n"
       "4. Quan sát danh sách friend và số tin chưa xác nhận\n"
       "5. Cho 1 friend MỚI gửi tin, quan sát app",
       "Bot cũ có ≥3 tin chưa xác nhận và ≥5 friend",
       "- App màn chat 1:1: KHÔNG hiển thị friend nào của LOA cũ\n"
       "- Số tin chưa xác nhận = 0\n"
       "- Friend MỚI gửi tin: xuất hiện trong danh sách và số tin chưa xác nhận = 1\n"
       "- Tin nhắn hiển thị đúng nội dung friend mới gửi",
       group="UI",
       note="Nguồn: Change bot r77 (TR=OK, stg=OK, step=OK). SYNC-APP-001 nâng Cao với flow critical "
            "user-facing. RULE-06 + RULE-08. Evidence: 3 ảnh app màn chat 1:1.", **PRD),

    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — màn trang cá nhân của friend ở CẢ 2 LOA: dữ liệu của LOA cũ bị xóa sạch",
       AFTER + "\n- Có friend A là bạn của CẢ LOA mới và LOA cũ\n"
       "- Trước khi đổi LOA: friend A ở LOA cũ có đầy đủ thông tin bạn bè, thẻ, câu trả lời form, "
       "lịch sử đặt chỗ, lịch sử mua hàng",
       "1. Trước khi đổi LOA: mở app, vào trang cá nhân của friend A, chụp ảnh toàn bộ dữ liệu "
       "(thông tin, thẻ, form, đặt chỗ, mua hàng)\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app, tìm friend A\n"
       "4. Vào trang cá nhân của friend A, quan sát từng khối dữ liệu\n"
       "5. Đối chiếu với ảnh đã chụp",
       "friend A là bạn của cả 2 LOA, có đủ 5 loại dữ liệu ở LOA cũ",
       "- Trang cá nhân friend A: TRỐNG toàn bộ 5 loại dữ liệu (thông tin bạn bè, thẻ, câu trả lời form, "
       "lịch sử đặt chỗ, lịch sử mua hàng)\n"
       "- Không sót khối nào còn dữ liệu cũ\n"
       "- Friend A vẫn hiển thị được (vì là bạn của LOA mới), chỉ dữ liệu cũ bị xóa",
       group="UI",
       note="Nguồn: Change bot r78 (TR=OK, stg=OK, step=OK) + AddBot/Testcase r337. "
            "⚠️ Đây là case QUAN TRỌNG nhất về rò rỉ dữ liệu chéo giữa 2 LOA: nếu còn sót dữ liệu thì friend "
            "thấy dữ liệu LOA cũ qua LOA mới. Liên quan AddBot/Testcase r227 (SpecImprove #33154 — chính bug "
            "'sau khi change LOA vẫn truy xuất ngược được data friend info trong 1 tháng'). "
            "RULE-12 mục (3). SYNC-APP-001 + SEC-001. RULE-06 + RULE-08. "
            "Evidence: 2 ảnh trang cá nhân friend A trên app (đủ 5 khối).", **PRD),

    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — màn đặt lịch salon / sự kiện / biểu mẫu: không còn dữ liệu của friend LOA cũ",
       AFTER + "\n- Có app mobile đã đăng nhập\n"
       "- Trước khi đổi LOA: bot cũ có dữ liệu đặt chỗ salon, sự kiện và câu trả lời form",
       "1. Trước khi đổi LOA: mở app, vào 3 màn (đặt lịch salon, đặt lịch sự kiện, biểu mẫu), "
       "ghi số dòng từng màn\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app, vào từng màn trong 3 màn đó\n"
       "4. Đếm số dòng còn lại",
       "3 màn: đặt lịch salon · đặt lịch sự kiện · biểu mẫu — mỗi màn ≥2 dòng trước khi đổi",
       "- CẢ 3 màn: KHÔNG còn dữ liệu nào của friend LOA cũ\n"
       "- Mỗi màn hiển thị trạng thái rỗng đúng cách, không lỗi\n"
       "- Không sót màn nào còn dữ liệu cũ",
       group="UI",
       note="Nguồn: Change bot r79 (TR=OK, stg=OK, step=OK). Gộp 3 màn vào 1 TC vì CÙNG kết quả mong đợi "
            "(không còn dữ liệu) — liệt kê đủ 3 điểm ở Dữ liệu nhập. SYNC-APP-001. RULE-06 + RULE-08. "
            "Evidence: 3 ảnh trước + 3 ảnh sau.", **PRD),

    tc("Xóa data bot cũ — app mobile", "SYNC-APP-001", "Normal",
       "App mobile — đặt chỗ bài học của friend LOA cũ không còn hiển thị",
       AFTER + "\n- Có app mobile đã đăng nhập\n- Trước khi đổi LOA: bot cũ có ≥2 đặt chỗ bài học",
       "1. Trước khi đổi LOA: mở app, vào màn đặt lịch bài học, ghi danh sách đặt chỗ\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app, vào màn đặt lịch bài học\n"
       "4. Quan sát danh sách đặt chỗ",
       "≥2 đặt chỗ bài học của friend LOA cũ",
       "- App: KHÔNG hiển thị đặt chỗ bài học nào của friend LOA cũ\n"
       "- Khớp với kết quả trên web (đặt chỗ đã bị xóa khỏi DB)\n"
       "- Màn hiển thị trạng thái rỗng đúng cách",
       group="UI",
       note="Nguồn: Change bot r80 (TR=OK, stg=OK, step=OK: 'booking của user đã xóa / "
            "không hiển thị booking đó ở app'). SYNC-APP-001. RULE-06 + RULE-08. "
            "Evidence: 2 ảnh app màn đặt lịch bài học.", **PRD),

    tc("Xóa data bot cũ — app mobile", "NOTI-MAIL-001", "Normal",
       "App mobile — thông báo của LOA cũ ở MỌI loại đều bị xóa, chi tiết không còn dữ liệu",
       AFTER + "\n- Có app mobile đã đăng nhập\n"
       "- Trước khi đổi LOA: bot cũ có thông báo ở TẤT CẢ loại (đặt chỗ, form, mua hàng, chat)",
       "1. Trước khi đổi LOA: mở app, ghi số thông báo của TỪNG loại\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Mở lại app, quan sát số thông báo tổng của LOA mới\n"
       "4. Bấm vào chi tiết từng loại thông báo\n"
       "5. Đối chiếu với số đã ghi",
       "Đủ các loại thông báo: đặt chỗ · form · mua hàng · chat — mỗi loại ≥1",
       "- Số thông báo của LOA mới = 0\n"
       "- Bấm chi tiết TỪNG loại: danh sách đều trống, không sót loại nào\n"
       "- Không hiển thị thông báo nào thuộc friend LOA cũ",
       group="UI",
       note="Nguồn: Change bot r81 (TR=OK, stg=OK, step=OK). ⚠️ Lưu ý kết hợp với r75 (bug 'Landing k có "
            "notify nhưng vẫn hiển thị icon có notify') — phải kiểm cả badge icon. RULE-06 + RULE-08. "
            "Evidence: ảnh số thông báo tổng + ảnh chi tiết từng loại.", **PRD),
]
