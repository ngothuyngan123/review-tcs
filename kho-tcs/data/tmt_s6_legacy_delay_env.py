# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 34-40: template legacy & tương thích, delay message, gửi template từ màn khác,
copy & backup, recover dữ liệu lỗi, app mobile, phân quyền & môi trường.

Nguồn chính: 02. TCsLine_Template
  - tab「Task nhỏ+ check Bug Kh」r494-r613 (Bug KH #35871 — edit template rồi send không apply)
  - tab「Improve list template」r493-r572 (tùy chọn delay message) + r573-r632 (Bug KH #36384)
  - tab「Tcs #38987」(08/2026 — bộ TC hợp nhất Bug KH #38987: delay + bot_profile_id)
  - tab「Template type text」r201-r271 (gắn template ở màn send all / scenario / remind, category âm)
  - tab「Template button」r1467-r1497 (Bug KH #33911 — recover ảnh button, capture_templates)
  - tab「Type introduce」(loại legacy 紹介文) ·「Test app」(preview / send phía app)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Mở /basic/message-template")
U1 = "\n- Đã đăng ký friend U1 làm クイックテストユーザー"
GD = (ADM + "\n- Có group template G_DELAY gồm 3 template con (text, パネル・ボタン, 画像)\n"
      "- Bot A có 1 friend U1 đã kết bạn" + U1)

S6 = [
    # ═════════════ 34. Template legacy & tương thích ═════════════
    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Template loại 紹介文 (introduce) cũ: hiện đủ dữ liệu, edit LINE ID và 紹介文 lưu đúng",
       ADM + "\n- Có template loại 紹介文 tạo từ trước (legacy)",
       "1. Mở edit template 紹介文 → đối chiếu toàn bộ trường đã nhập\n"
       "2. Ô LINE ID: bỏ trống → 保存 → quan sát\n3. Nhập LINE ID bằng text Nhật → 保存 → quan sát\n"
       "4. Nhập LINE ID thiếu「@」→ 保存 → quan sát\n"
       "5. Ô 紹介文: bỏ trống → 保存 → quan sát; nhập text Nhật → 保存; nhập có xuống dòng → 保存",
       "LINE ID: rỗng / text Nhật / thiếu @; 紹介文: rỗng / text Nhật / xuống dòng",
       "- Màn edit hiện ĐẦY ĐỦ dữ liệu các trường đã nhập\n"
       "- LINE ID rỗng: báo required, không lưu\n"
       "- LINE ID là text Nhật hoặc thiếu「@」: LƯU THÀNH CÔNG (không validate định dạng)\n"
       "- 紹介文 rỗng: báo required; text Nhật và có xuống dòng: lưu thành công",
       note="Nguồn: Type introduce r3-r9. ⚠ LINE ID thiếu「@」vẫn lưu được — spec không ghi validate "
            "→ xem MT-43."),

    tc("Template legacy & tương thích", "MSG-004", "Abnormal",
       "紹介文: chat 1:1 KHÔNG xuống dòng, phía LINE user CÓ xuống dòng như đã nhập",
       ADM + "\n- Template 紹介文 có ô 紹介文 nhập 2 dòng" + U1,
       "1. Gửi template 紹介文 cho U1\n2. Quan sát nội dung 紹介文 ở chat 1:1 của tool\n"
       "3. Quan sát nội dung ở LINE của U1\n4. U1 bấm vào nội dung → quan sát màn hình mở ra",
       "紹介文 2 dòng",
       "- Chat 1:1 của tool: nội dung 紹介文 KHÔNG xuống dòng\n"
       "- Phía LINE user: nội dung 紹介文 CÓ xuống dòng đúng như đã nhập\n"
       "- U1 bấm vào → mở màn add bot của LINE OA được giới thiệu",
       note="Nguồn: Type introduce r15-r17. Lệch hiển thị web ↔ LINE — spec không ghi → xem MT-43."),

    tc("Template legacy & tương thích", "MSG-004", "Normal",
       "紹介文: ô パソコン版LINEアプリ・通知欄の表示テキスト để trống → tự fill LINEアプリよりご覧ください",
       ADM + "\n- Template 紹介文",
       "1. Bỏ trống ô「パソコン版LINEアプリ・通知欄の表示テキスト」→ 保存\n2. Vào lại màn edit → quan sát ô đó\n"
       "3. Nhập text có xuống dòng → 保存 → vào edit → quan sát",
       "để trống / text có xuống dòng",
       "- Để trống: 保存 thành công; vào edit thì ô TỰ FILL「LINEアプリよりご覧ください」\n"
       "- Nhập text có xuống dòng: 保存 thành công và giữ đúng nội dung",
       note="Nguồn: Type introduce r10-r11. ⚠ Default này KHÁC default「メッセージをご確認ください」mà spec "
            "Field Matrix #23 ghi cho panel/button → xem MT-34."),

    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Bug KH #35871: template text CŨ (từ 2022, không có group) — edit ở modal preview rồi send thì apply nội dung mới",
       ADM + "\n- Có template text CŨ tạo từ 2022 (loại KHÔNG có group template)\n"
              "- Friend A và friend B đã kết bạn",
       "1. Vào chat 1:1 của friend A → bấm「テンプレート送信」→ chọn template cũ\n"
       "2. Ở modal preview-send: sửa nội dung (thêm text latinh, text Nhật, số, ký tự đặc biệt)\n"
       "3. Bấm gửi → quan sát preview trước khi gửi, tin phía LINE user và tin trên chat 1:1\n"
       "4. Lặp lại với friend B nhưng sửa nội dung KHÁC\n5. So sánh tin của A và B",
       "template text cũ 2022; friend A và B sửa nội dung khác nhau",
       "- Preview hiển thị đúng nội dung ĐÃ SỬA\n"
       "- Sau khi send: LINE user nhận đúng nội dung đã sửa; chat 1:1 cũng hiện nội dung đã sửa\n"
       "- Friend A nhận nội dung sửa cho A, friend B nhận nội dung sửa cho B (không lẫn nhau)",
       note="Nguồn: Task nhỏ+ check Bug Kh r495-r515 (Bug KH #35871, 15/04/2026)."),

    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Bug KH #35871: KHÔNG edit khi gửi → send đúng nội dung gốc của template",
       ADM + "\n- Có template text cũ 2022 và template text MỚI (loại có group)",
       "1. Vào chat 1:1 → 「テンプレート送信」→ chọn template cũ → KHÔNG sửa gì → gửi\n"
       "2. Quan sát nội dung tin phía LINE user và chat 1:1\n3. Lặp lại với template text mới",
       "template cũ và mới; không edit",
       "- Cả 2 loại: LINE user nhận đúng nội dung GỐC của template\n- Chat 1:1 hiện đúng nội dung gốc",
       note="Nguồn: Task nhỏ+ check Bug Kh r514, r520, r572."),

    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Bug KH #35871: gửi template qua MULTI ACTION → không cho edit, gửi đúng nội dung template",
       ADM + "\n- Có multi action gắn template text cũ 2022 và 1 action gắn template text mới",
       "1. Trigger multi action gắn template cũ tới friend A\n2. Quan sát có màn edit hiện ra hay không\n"
       "3. Quan sát nội dung tin trên LINE\n4. Lặp lại với template text mới\n"
       "5. Lặp lại với template loại KHÁC text (button, ảnh, sticker, location)",
       "multi action; template cũ, mới và các loại khác text",
       "- Case gửi bởi multi action: KHÔNG cho edit nội dung\n"
       "- Tin trên LINE đúng nội dung template đã cấu hình\n"
       "- Chỉ loại TEXT là edit được ở modal preview; các loại khác không edit được",
       note="Nguồn: Task nhỏ+ check Bug Kh r516, r611-r613."),

    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Bug KH #35871: đặt lịch gửi template — edit rồi save 1 lần / 2 lần → gửi theo nội dung mới nhất",
       ADM + "\n- Có template text cũ 2022 và template text mới",
       "1. Ở màn đặt lịch send msg: chọn template, KHÔNG edit → đặt lịch → chờ job → quan sát tin\n"
       "2. Chọn template, EDIT → 保存 → đặt lịch → chờ job → quan sát preview và tin\n"
       "3. Chọn template, edit → 保存 lần 1 → edit tiếp → 保存 lần 2 → đặt lịch → chờ job → quan sát\n"
       "4. Lặp lại 3 bước với template text mới",
       "3 kịch bản edit × template cũ và mới",
       "- Preview hiển thị đúng nội dung tại thời điểm đặt lịch\n"
       "- Tin phía LINE user và trên chat 1:1 khớp nội dung sau lần 保存 CUỐI CÙNG",
       note="Nguồn: Task nhỏ+ check Bug Kh r517-r519, r549-r571."),

    tc("Template legacy & tương thích", "SYNC-APP-001", "Abnormal",
       "Bug KH #35871 phía APP: gửi template ngay / có đặt lịch → đặt lịch thì DISABLE không cho edit",
       ADM + "\n- Đã cài app mobile LME và đăng nhập bot A\n- Có template text cũ 2022 và template text mới",
       "1. Trên app, vào chat 1:1 → gửi template ngay, KHÔNG edit → quan sát tin trên LINE\n"
       "2. Trên app, chọn template rồi ĐẶT LỊCH gửi → quan sát ô nội dung template\n"
       "3. Thử sửa nội dung khi đã đặt lịch → quan sát\n4. Lặp lại với template text mới",
       "app mobile; gửi ngay và đặt lịch; template cũ và mới",
       "- Gửi ngay không edit: LINE user nhận đúng nội dung GỐC của template\n"
       "- Khi đã có đặt lịch: ô nội dung template bị DISABLE, KHÔNG cho edit",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ+ check Bug Kh r520-r548, r572-r610. RULE-08 + SYNC-APP: hành vi app mobile "
            "phải xác nhận trên PRODUCTION."),

    tc("Template legacy & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Template dạng CŨ gắn ở scenario / send all / remind (clone và get thẳng) → send, preview, edit đúng",
       ADM + "\n- Có template text và template button dạng CŨ" + U1,
       "1. Ở màn scenario: get thẳng template cũ vào step → gửi → quan sát preview và tin trên LINE\n"
       "2. Ở màn scenario: clone template cũ rồi edit → gửi → quan sát\n"
       "3. Lặp lại 2 bước ở màn send all và màn remind",
       "2 cách gắn (clone / get thẳng) × 3 màn × template text và button dạng cũ",
       "- Mọi tổ hợp: send được, preview đúng và vào edit hiện đủ dữ liệu\n"
       "- Tin trên LINE khớp nội dung template",
       note="Nguồn: Template type text r218-r223, r242-r247, r265-r270, r289-r294."),

    # ═════════════ 35. Delay message ═════════════
    tc("Delay message", "UI-001", "Normal",
       "Tùy chọn メッセージを1通ずつ数秒遅延させて送信する: default OFF, bật thì lưu is_delay_message = 1",
       GD,
       "1. Mở màn list template con của G_DELAY → quan sát tùy chọn delay và giá trị default\n"
       "2. Kiểm tra `template.is_delay_message` khi đang OFF\n3. Bật tùy chọn → 保存\n"
       "4. Kiểm tra lại `template.is_delay_message`\n5. Reload màn hình → quan sát trạng thái tùy chọn",
       "G_DELAY 3 template con",
       "- Tùy chọn hiển thị đúng design, mặc định là OFF và `is_delay_message` = 0\n"
       "- Sau khi bật và 保存: `is_delay_message` = 1\n- Reload vẫn giữ trạng thái ON",
       note="Nguồn: Improve list template r493-r496."),

    tc("Delay message", "JOB-001", "Normal",
       "Delay OFF: gửi qua web → các message gửi CÙNG LÚC theo thứ tự, không duplicate",
       GD + "\n- G_DELAY đang TẮT delay",
       "1. Gửi G_DELAY qua send test → quan sát thời điểm 3 tin đến LINE\n"
       "2. Gửi qua chat 1:1 (icon ngôi sao →テンプレート) → quan sát\n"
       "3. Gửi bằng action ở màn friend list và màn tag → quan sát\n"
       "4. Kiểm tra bảng `send_random_messages`",
       "delay OFF; 4 đường gửi web",
       "- 3 tin đến CÙNG LÚC, đúng thứ tự template con, KHÔNG bị duplicate\n"
       "- KHÔNG sinh bản ghi nào trong `send_random_messages`",
       note="Nguồn: Improve list template r497-r504 + Tcs #38987 r43 (NEW-148)."),

    tc("Delay message", "JOB-001", "Normal",
       "Delay ON + gửi qua WEB: tin ĐẦU gửi ngay, các tin sau vào send_random_messages cách nhau 2-5s",
       GD + "\n- G_DELAY đang BẬT delay",
       "1. Gửi G_DELAY qua send test → quan sát thứ tự và khoảng cách 3 tin trên LINE\n"
       "2. Kiểm tra bảng `send_random_messages`: số bản ghi và cột `time_send`\n"
       "3. Lặp lại qua chat 1:1, qua action ở màn friend list và màn tag, qua remind gửi ngay, "
       "qua resend message lỗi, qua send message reply ở màn talklist",
       "delay ON; 7 đường gửi web; group 3 template con",
       "- Tin THỨ NHẤT gửi ngay (do web send)\n"
       "- 2 tin còn lại được insert vào `send_random_messages`, `time_send` tăng dần thêm 2-5 giây mỗi tin\n"
       "- Job gửi đúng 2 tin đó, LINE user nhận đủ 3 tin đúng thứ tự, cách nhau 2-5s, không duplicate",
       note="Nguồn: Improve list template r526-r537 + Tcs #38987 r12 (NEW-147), r11 (NEW-13)."),

    tc("Delay message", "JOB-001", "Abnormal",
       "Delay ON nhưng KHÔNG áp cho send all và scenario → vẫn gửi cùng lúc, không duplicate",
       GD + "\n- G_DELAY đang BẬT delay, đã gắn vào 1 broadcast (send all) và 1 step scenario",
       "1. Chạy broadcast có G_DELAY → quan sát thời điểm 3 tin đến LINE\n"
       "2. Chạy scenario step có G_DELAY → quan sát\n3. Kiểm tra bảng `send_random_messages`",
       "delay ON; send all và scenario",
       "- Cả send all và scenario: 3 tin gửi CÙNG LÚC (delay KHÔNG được áp)\n"
       "- Không bị duplicate tin\n- Không sinh bản ghi delay cho 2 luồng này",
       note="Nguồn: Improve list template r538-r539 (Expect gốc「KO APPLY - vẫn send all cùng 1 lúc」). "
            "⚠ Spec §7 mô tả delay chỉ dùng cho quick test group → phạm vi áp dụng thực tế rộng hơn "
            "nhưng loại trừ send all/scenario; spec không ghi → xem MT-44."),

    tc("Delay message", "JOB-001", "Normal",
       "Delay ON + REMIND: mỗi message cách nhau đúng theo logic, ghi event_step_time và send_random_messages",
       GD + "\n- G_DELAY BẬT delay, đã gắn vào 1 remind (gửi trước 5 phút và gửi ngay sau start)",
       "1. Trigger remind gửi ngay sau start → quan sát thứ tự và khoảng cách tin trên LINE\n"
       "2. Trigger remind gửi trước 5 phút → chờ tới thời điểm remind bắn → quan sát\n"
       "3. Kiểm tra bảng `event_step_time` và `send_random_messages`",
       "2 kiểu remind; group 3 template con",
       "- Tin gửi theo thứ tự, cách nhau đúng theo logic delay, KHÔNG duplicate\n"
       "- Bảng `event_step_time` và `send_random_messages` có bản ghi khớp số tin và thời điểm",
       note="Nguồn: Improve list template r540, r567-r568 + Tcs #38987 r38-r39 (TC-DLY-021/022)."),

    tc("Delay message", "JOB-001", "Normal",
       "Delay ON áp cho template gắn trong ACTION: button, image map, rich menu, form, auto reply, add friend",
       GD + "\n- G_DELAY BẬT delay, đã gắn vào action của: nút template, vùng image map, rich menu, "
             "form (action mở form và action submit), auto reply, add friend / landing",
       "1. Với mỗi điểm gắn, trigger action tới U1: bấm nút template, bấm vùng ảnh image map, "
       "bấm vùng rich menu, mở form và submit form, gửi keyword auto reply, quét mã add friend\n"
       "2. Với mỗi lượt, quan sát thứ tự và khoảng cách các tin trên LINE\n"
       "3. Kiểm tra `send_random_messages` cho từng lượt",
       "7 điểm gắn action",
       "- Mỗi luồng đều nhận đủ 3 tin của G_DELAY, giãn cách 2-5s đúng logic delay\n"
       "- Nội dung tin đúng với template đã gán trong từng action\n"
       "- `send_random_messages` sinh bản ghi cho các tin từ thứ 2 trở đi",
       note="Nguồn: Improve list template r541-r561 + Tcs #38987 r40 (TC-DLY-023). Gộp 7 điểm vì "
            "CÙNG 1 kết quả mong đợi."),

    tc("Delay message", "FUNC-SEQ-001", "Normal",
       "2 group template liền nhau (cha1 ON – cha2 OFF) → tin đầu cha1 và cả cụm cha2 gửi cùng lúc, con cha1 giãn 2-5s",
       ADM + "\n- Có group cha1 (BẬT delay, 3 template con) và cha2 (TẮT delay, 2 template con)\n"
              "- Cả 2 group được gắn liền nhau vào multi action" + U1,
       "1. Trigger multi action tới U1\n2. Quan sát thứ tự và thời điểm tất cả tin trên LINE\n"
       "3. Kiểm tra `t_actions`, `t_actions_detail`, `send_random_messages`",
       "cha1 delay ON (3 con) + cha2 delay OFF (2 con)",
       "- Template ĐẦU của cha1 và CẢ CỤM cha2 gửi CÙNG LÚC\n"
       "- Sau đó các template con còn lại của cha1 gửi cách nhau 2-5 giây\n"
       "- Bản ghi `send_random_messages` khớp các tin bị delay",
       note="Nguồn: Improve list template r569 + Tcs #38987 r35 (TC-DLY-018)."),

    tc("Delay message", "FUNC-SEQ-001", "Normal",
       "2 group template liền nhau (cha1 ON – cha2 ON) → gửi liền mạch, mọi tin cách nhau 2-5s",
       ADM + "\n- Có group cha1 và cha2 đều BẬT delay, mỗi group 3 template con\n"
              "- Cả 2 được gắn liền nhau vào multi action" + U1,
       "1. Trigger multi action tới U1\n2. Quan sát thứ tự và thời điểm toàn bộ tin trên LINE\n"
       "3. Kiểm tra `send_random_messages`",
       "cha1 và cha2 đều delay ON, mỗi group 3 con",
       "- Gửi hết template con CUỐI của cha1 rồi sang template con ĐẦU của cha2 liền mạch\n"
       "- Tất cả tin trong cả 2 group cách nhau 2-5 giây\n- Không tin nào bị duplicate hoặc mất",
       note="Nguồn: Improve list template r570 + Tcs #38987 r36 (TC-DLY-019)."),

    tc("Delay message", "DATA-ID-001", "Normal",
       "Bug KH #38987: profile MẶC ĐỊNH + delay ON → mọi tin cùng 1 tên người gửi, KHÔNG hiện アカウント名 from アカウント名",
       ADM + "\n- Bot A có nhiều người gửi: profile MẶC ĐỊNH + ≥2 profile tuỳ chỉnh\n"
              "- Người gửi ĐANG CHỌN là profile MẶC ĐỊNH\n"
              "- Group G_DELAY gồm template text「テストメッセージ1」+ template パネル・ボタン (1 panel 2 nút), "
              "BẬT delay" + U1,
       "1. Mở màn list template, xác nhận người gửi đang chọn là profile mặc định\n"
       "2. Bấm nút ở cột「クイックテスト」của G_DELAY → chọn U1 → xác nhận gửi\n"
       "3. Chờ nhận đủ cả 2 tin trên LINE\n4. Đối chiếu tên người gửi của tin 1 và tin 2\n"
       "5. Kiểm tra cột `send_random_messages.bot_profile_id`",
       "profile mặc định; group text + panel/button; delay ON; 1 tester",
       "- Tin thứ nhất (text) và tin thứ 2 (panel/button) hiển thị CÙNG một tên người gửi là tên tài "
       "khoản chính thức\n"
       "- Tin thứ 2 KHÔNG hiển thị「アカウント名 from アカウント名」\n"
       "- `send_random_messages.bot_profile_id` = NULL (rỗng) cho các bản ghi hàng đợi",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r4 (NEW-139), r6 (NEW-16), r8-r9 (NEW-56/NEW-62), r5 (NEW-144). "
            "Đây là ca TÁI HIỆN chính của Bug KH #38987 (parent #38389). RULE-08: cần đối chiếu tên "
            "người gửi render trên LINE app thật. Cột `bot_profile_id` có trong db-mapping.md:390 "
            "nhưng spec §7 không mô tả quy tắc chuẩn hoá → xem MT-45."),

    tc("Delay message", "DATA-ID-001", "Normal",
       "Bug KH #38987 — chống over-fix: profile TUỲ CHỈNH + delay ON → mọi tin vẫn hiện 「tên người gửi from tên OA」",
       ADM + "\n- Bot A có profile mặc định P0 và profile tuỳ chỉnh P1 (nick_name「担当スタッフ田中」)\n"
              "- Người gửi đang chọn là P1\n- Group G_DELAY 3 template con, BẬT delay" + U1,
       "1. Chọn người gửi = P1\n2. Quick test G_DELAY cho U1\n"
       "3. Quan sát nhãn người gửi của TẤT CẢ tin trên LINE\n"
       "4. Kiểm tra `send_random_messages.bot_profile_id`",
       "profile tuỳ chỉnh P1; delay ON; 3 template con",
       "- MỌI tin (kể cả tin bị giãn cách) đều hiển thị「担当スタッフ田中 from {tên OA}」\n"
       "- `send_random_messages.bot_profile_id` = id của P1 (không phải NULL)",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r26-r29 (NEW-140/NEW-17/NEW-89/NEW-63). Đây là cặp ĐỐI CHỨNG chống "
            "over-fix của bản fix #38987."),

    tc("Delay message", "DATA-ID-001", "Normal",
       "Bug KH #38987: đổi người gửi giữa 2 lần quick test → lần sau ghi đúng profile mới",
       ADM + "\n- Bot A có profile mặc định P0 và profile tuỳ chỉnh P1\n- Group G_DELAY BẬT delay" + U1,
       "1. Chọn người gửi = P0 (mặc định) → quick test G_DELAY cho U1 → quan sát nhãn và `bot_profile_id`\n"
       "2. Đổi người gửi sang P1 → quick test lần 2 → quan sát nhãn và `bot_profile_id`\n"
       "3. Đổi lại về P0 → quick test lần 3 → quan sát",
       "3 lượt gửi, đổi profile giữa các lượt",
       "- Lượt 1 (P0): tin không có nhãn「from」, `bot_profile_id` = NULL\n"
       "- Lượt 2 (P1): tin có nhãn「{nick_name P1} from {tên OA}」, `bot_profile_id` = id của P1\n"
       "- Lượt 3 (P0): trở lại không nhãn, `bot_profile_id` = NULL",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r30-r31 (NEW-141/NEW-142)."),

    tc("Delay message", "DATA-ID-001", "Boundary",
       "Bug KH #38987: đổi cờ is_default giữa các profile → hành vi bám theo cờ RUNTIME, không hardcode id",
       ADM + "\n- Bot A có P0 (đang là mặc định) và P1 (phụ)\n- Group G_DELAY BẬT delay" + U1,
       "1. Vào setting profile, đặt P1 làm profile MẶC ĐỊNH (P0 thành phụ)\n"
       "2. Chọn người gửi = P1 → quick test G_DELAY cho U1 → quan sát nhãn và `bot_profile_id`\n"
       "3. Chọn người gửi = P0 → quick test → quan sát nhãn và `bot_profile_id`",
       "P1 trở thành mặc định, P0 thành phụ",
       "- Bước 2 (P1 giờ là mặc định): các tin KHÔNG có nhãn sender; `bot_profile_id` = NULL\n"
       "- Bước 3 (P0 giờ là phụ): các tin có nhãn「{nick_name P0} from {tên OA}」; "
       "`bot_profile_id` = id của P0\n"
       "- Hành vi bám đúng cờ `is_default` tại thời điểm gửi",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r33 (TC-DLY-011 — bổ sung ngoài TCS tool). Xác nhận helper query cờ "
            "`is_default` runtime chứ không hardcode id."),

    tc("Delay message", "DATA-ID-001", "Abnormal",
       "Bug KH #38987: 2 người gửi TRÙNG tên hiển thị → chọn đúng theo định danh, không theo tên",
       ADM + "\n- Bot A có 2 profile tuỳ chỉnh TRÙNG tên hiển thị (đều là「サポート」, khác ảnh đại diện) "
              "cộng profile mặc định\n- Group G_DELAY 3 template con, BẬT delay" + U1,
       "1. Mở màn quản lý người gửi, xác nhận có 2 người gửi cùng tên「サポート」\n"
       "2. Chọn người gửi THỨ HAI trong 2 mục trùng tên\n3. Quick test G_DELAY cho U1\n"
       "4. Kiểm tra `bot_profile_id` của các bản ghi hàng đợi\n"
       "5. Quan sát ảnh đại diện và nhãn người gửi trên LINE",
       "2 profile cùng tên「サポート」, chọn mục thứ hai",
       "- Bản ghi hàng đợi lưu ĐÚNG định danh của người gửi thứ hai (không phải người thứ nhất trùng "
       "tên và không phải profile mặc định)\n"
       "- Trên LINE, mọi tin hiện đúng ẢNH ĐẠI DIỆN của người gửi đã chọn và cùng chuỗi「サポート from ...」",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r32 (NEW-154). RULE-08: phần đối chiếu ảnh đại diện cần LINE app thật."),

    tc("Delay message", "DATA-ID-001", "Normal",
       "Bug KH #38987: bot chỉ có 1 profile mặc định / chưa có profile nào → gửi bình thường, không lỗi",
       ADM + "\n- Bot B chỉ có 1 profile mặc định; Bot C chưa có profile nào (hoặc không chọn profile)\n"
              "- Mỗi bot có 1 group G_DELAY 3 template con, BẬT delay",
       "1. Với bot B: quick test G_DELAY → quan sát nhãn từng tin\n"
       "2. Với bot C: quick test G_DELAY → quan sát nhãn và kiểm tra có lỗi hệ thống hay không\n"
       "3. Kiểm tra `send_random_messages.bot_profile_id` ở cả 2 bot",
       "bot 1 profile mặc định; bot chưa có profile",
       "- Bot B: mọi tin KHÔNG có hậu tố「from」\n"
       "- Bot C: gửi bình thường, KHÔNG lỗi hệ thống, không tin nào có nhãn sai\n"
       "- `bot_profile_id` = NULL ở cả 2 bot",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r10 (NEW-138), r24 (TC-DLY-007 — Edge case)."),

    tc("Delay message", "MSG-004", "Normal",
       "Bug KH #38987: tin panel/button đến SAU delay vẫn hiện đủ ảnh, tiêu đề, nội dung và các nút",
       GD + "\n- G_DELAY BẬT delay, template con thứ 2 là パネル・ボタン có ảnh + title + nội dung + 2 nút",
       "1. Quick test G_DELAY cho U1\n2. Chờ nhận tin panel/button (tin đến sau delay)\n"
       "3. Đối chiếu ảnh, tiêu đề, nội dung, số nút và text nút với cấu hình\n4. Bấm 1 nút → quan sát action",
       "panel/button 1 panel 2 nút, đến sau delay",
       "- Tin panel/button hiển thị ĐẦY ĐỦ ảnh, tiêu đề, nội dung và cả 2 nút\n"
       "- Bấm nút chạy đúng action đã set",
       note="Nguồn: Tcs #38987 r14 (NEW-157)."),

    tc("Delay message", "SYNC-APP-001", "Normal",
       "Bug KH #38987: tên người gửi của tin delay hiển thị GIỐNG nhau trên LINE iOS và LINE Android",
       GD + "\n- G_DELAY BẬT delay; có 1 tester dùng LINE iOS và 1 tester dùng LINE Android",
       "1. Quick test G_DELAY cho cả 2 tester\n2. Trên LINE iOS: quan sát tên người gửi từng tin\n"
       "3. Trên LINE Android: quan sát tên người gửi từng tin\n4. So sánh 2 nền tảng",
       "2 nền tảng LINE",
       "- Tên người gửi của mọi tin GIỐNG nhau trên iOS và Android\n"
       "- Không nền tảng nào hiện dạng lặp「アカウント名 from アカウント名」",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r15 (NEW-12). RULE-08: khác biệt render giữa 2 OS chỉ thấy trên app thật."),

    tc("Delay message", "SEC-002", "Boundary",
       "Bug KH #38987: tên người gửi DÀI sát giới hạn → hiển thị đúng, không bị cắt thành dạng lặp",
       ADM + "\n- Bot A có profile tuỳ chỉnh với nick_name dài sát giới hạn ký tự cho phép\n"
              "- Group G_DELAY BẬT delay" + U1,
       "1. Chọn người gửi là profile có nick_name dài sát giới hạn\n2. Quick test G_DELAY cho U1\n"
       "3. Quan sát nhãn người gửi của từng tin trên LINE",
       "nick_name dài sát giới hạn",
       "- Nhãn hiển thị đầy đủ dạng「{nick_name} from {tên OA}」\n"
       "- KHÔNG bị cắt thành dạng lặp「アカウント名 from アカウント名」",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r16 (NEW-10)."),

    tc("Delay message", "CONC-001", "Boundary",
       "Bug KH #38987: gọi quick test 2 lần liên tiếp / 2 request song song → hàng đợi không sinh bản ghi trùng",
       GD + "\n- G_DELAY BẬT delay",
       "1. Gọi quick test 2 lần liên tiếp với cùng dữ liệu → đếm tin U1 nhận và bản ghi "
       "`send_random_messages`\n"
       "2. Gửi 2 request quick test SONG SONG với cùng dữ liệu → đếm tin và bản ghi\n"
       "3. Lặp lại bằng endpoint gửi thử V3",
       "2 lần liên tiếp và 2 request song song",
       "- 2 lần liên tiếp: mỗi lượt sinh đúng bộ bản ghi của lượt đó, U1 nhận đúng 2 bộ tin\n"
       "- 2 request song song: hàng đợi KHÔNG sinh bản ghi trùng ngoài kiểm soát\n"
       "- Endpoint V3 cho kết quả tương đương",
       note="Nguồn: Tcs #38987 r20-r23 (NEW-28/NEW-49/NEW-19/NEW-20)."),

    tc("Delay message", "MSG-001", "Normal",
       "Bug KH #38987: quick test tới 2 và nhiều tester → dữ liệu tách biệt, ai cũng nhận đủ tin",
       GD + "\n- Đã đăng ký 3 tester U1, U2, U3; G_DELAY BẬT delay",
       "1. Quick test G_DELAY tới U1 và U2 cùng lúc → quan sát tin của từng người\n"
       "2. Quick test tới cả 3 tester → quan sát tin từng người\n"
       "3. Kiểm tra bản ghi `send_random_messages` theo từng line_user",
       "2 tester rồi 3 tester",
       "- Mỗi tester nhận ĐỦ 3 tin, đúng thứ tự và cùng thông tin người gửi\n"
       "- Dữ liệu hàng đợi của từng người TÁCH BIỆT, không lẫn nhau",
       note="Nguồn: Tcs #38987 r18-r19 (NEW-160/NEW-161)."),

    tc("Delay message", "JOB-001", "Normal",
       "Bug KH #38987: job xử lý bản ghi delay sinh từ multi action / remind với profile mặc định",
       ADM + "\n- Profile đang chọn là mặc định P0\n- Có multi action và remind gắn template delay" + U1,
       "1. Trigger multi action có template delay tới U1\n2. Trigger remind có template delay tới U1\n"
       "3. Query `send_random_messages` cho cả 2 lượt\n4. Quan sát tin trên LINE của cả 2 luồng",
       "2 nguồn sinh bản ghi delay: multi action và remind; profile P0",
       "- Cả 2 nguồn tạo bản ghi với `bot_profile_id` = NULL\n"
       "- Job gửi tin KHÔNG gắn sender\n- Không tin nào hiển thị「アカウント名 from アカウント名」\n"
       "- Thứ tự và giãn cách đúng logic từng luồng",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r41 (TC-DLYJ-007). Vùng fix HelperService::sendAction — "
            "TCS tool KHÔNG phủ nhánh này."),

    tc("Delay message", "DATA-ID-001", "Normal",
       "Bug KH #38987 — chống over-fix ở multi action: profile phụ P1 → mọi tin vẫn có nhãn 「P1 from tên OA」",
       ADM + "\n- Profile đang chọn = P1 (phụ, nick_name「担当スタッフ田中」)\n"
              "- Multi action có template cha1 và cha2 đều BẬT delay" + U1,
       "1. Chọn profile P1\n2. Trigger multi action tới U1\n3. Quan sát nhãn từng tin trên LINE\n"
       "4. Kiểm tra `send_random_messages.bot_profile_id`",
       "profile phụ P1; cha1 ON – cha2 ON",
       "- MỌI tin (kể cả tin giãn cách) hiển thị「担当スタッフ田中 from {tên OA}」\n"
       "- `bot_profile_id` = id của P1",
       env="PRODUCTION",
       note="Nguồn: Tcs #38987 r37 (TC-DLY-020) — cặp đối chứng của TC-DLY-018/019."),

    tc("Delay message", "PERM-001", "Normal",
       "Nhân viên (staff) được cấp quyền màn template → quick test được và tên người gửi hiển thị đúng",
       ADM + "\n- Bot A có staff S1 ĐƯỢC phân quyền màn template\n- Đăng nhập bằng S1\n"
              "- Group G_DELAY BẬT delay" + U1,
       "1. S1 mở màn list template → quick test G_DELAY cho U1\n"
       "2. Quan sát tin trên LINE và nhãn người gửi\n3. Kiểm tra `send_random_messages.bot_profile_id`",
       "staff S1 có quyền template; profile mặc định",
       "- S1 gửi thử thành công\n- U1 nhận đủ tin và nhãn người gửi hiển thị đúng "
       "(không lặp「アカウント名 from アカウント名」)",
       note="Nguồn: Tcs #38987 r17 (NEW-2)."),

    tc("Delay message", "DATA-BACKUP-001", "Normal",
       "Copy và Backup group template có delay → giữ nguyên trạng thái 送信オプション",
       GD + "\n- G_DELAY đang BẬT delay",
       "1. Copy G_DELAY → mở bản copy, quan sát tùy chọn delay và kiểm tra `is_delay_message`\n"
       "2. Gửi bản copy → quan sát khoảng cách tin\n"
       "3. Backup sang bot B → mở group tương ứng ở bot B, kiểm tra `is_delay_message`",
       "copy và backup group có delay ON",
       "- Bản copy giống bản gốc và 送信オプション cũng được BẬT như bản gốc\n"
       "- Bản backup ở bot B cũng giữ `is_delay_message` = 1",
       note="Nguồn: Improve list template r526, r571-r572."),

    # ═════════════ 36. Gửi template từ màn khác ═════════════
    tc("Gửi template từ màn khác", "DATA-DB-001", "Normal",
       "Tạo template TẠI màn send all → lưu category_id = -11, name = broadcast; edit và xóa đúng",
       ADM + "\n- Đang ở màn broadcast (メッセージ配信), tạo broadcast mới" + U1,
       "1. Tại màn send all, tạo mới 1 template text với nội dung có gắn giá trị (friend info) → lưu\n"
       "2. Kiểm tra bảng `template`: `category_id` và `name`\n"
       "3. Gửi broadcast cho U1 → quan sát nội dung và giá trị đã gán\n"
       "4. Mở preview → quan sát\n5. Edit template đó → lưu → kiểm tra `category_id`\n"
       "6. Xóa template đó → kiểm tra bản ghi trong bảng `template`",
       "template tạo tại màn send all",
       "- Tạo thành công; `template.category_id` = -11 và `name` = broadcast\n"
       "- Gửi cho user thành công, các giá trị gán được replace đúng\n"
       "- Edit: lưu thành công và `category_id` vẫn = -11\n"
       "- Xóa: bản ghi tương ứng bị xóa khỏi bảng `template`",
       note="Nguồn: Template type text r201-r205. ⚠ TC gốc r205 note「chưa thấy xóa trong DB」→ "
            "nhánh xóa là điểm rủi ro, xem MT-46."),

    tc("Gửi template từ màn khác", "DATA-DB-001", "Normal",
       "Tạo template TẠI màn scenario → category_id = -111, name = scenario; tại remind → category_id = -99",
       ADM + "\n- Có 1 scenario và 1 remind đã tạo" + U1,
       "1. Tại màn scenario, tạo mới template text trong step → lưu → kiểm tra `category_id` và `name`\n"
       "2. Gửi cho U1 (cả nhánh gửi ngay qua web và nhánh gửi theo time qua job) → quan sát\n"
       "3. Edit template đó → lưu → kiểm tra `category_id`\n4. Xóa → kiểm tra bảng `template`\n"
       "5. Lặp lại toàn bộ tại màn remind",
       "template tạo tại scenario và tại remind",
       "- Scenario: `category_id` = -111, `name` = scenario\n"
       "- Remind: `category_id` = -99, `name` để trống\n"
       "- Gửi được ở cả nhánh web và job, giá trị gán replace đúng\n"
       "- Edit giữ nguyên `category_id`; xóa thì bản ghi bị xóa",
       note="Nguồn: Template type text r225-r229, r248-r252, r272-r276, r295-r299."),

    tc("Gửi template từ màn khác", "STATE-DEP-001", "Normal",
       "CLONE template từ thư viện vào màn khác → 2 bản ĐỘC LẬP (sửa/xóa bản này không ảnh hưởng bản kia)",
       ADM + "\n- Có template text T_LIB trong thư viện template" + U1,
       "1. Ở màn send all, CLONE T_LIB rồi edit → lưu → gửi cho U1 → quan sát\n"
       "2. Edit bản clone → mở T_LIB gốc đối chiếu\n3. Edit T_LIB gốc → mở bản clone đối chiếu\n"
       "4. Xóa bản clone → kiểm tra T_LIB gốc\n5. Xóa T_LIB gốc → kiểm tra bản clone ở send all\n"
       "6. Lặp lại toàn bộ ở màn scenario (cả gửi ngay và gửi theo time) và màn remind",
       "clone ở 3 màn; sửa/xóa 2 chiều",
       "- Bản clone gửi được và giá trị gán replace đúng\n"
       "- Edit bản clone: T_LIB gốc KHÔNG bị ảnh hưởng\n- Edit T_LIB gốc: bản clone KHÔNG bị ảnh hưởng\n"
       "- Xóa bản clone: T_LIB gốc vẫn còn\n- Xóa T_LIB gốc: bản clone vẫn còn ở màn đó",
       note="Nguồn: Template type text r206-r211, r230-r235, r253-r258, r277-r282, r300-r305."),

    tc("Gửi template từ màn khác", "STATE-DEP-001", "Normal",
       "GET THẲNG template từ thư viện → dùng CHUNG id, sửa/xóa bên nào cũng ảnh hưởng bên kia",
       ADM + "\n- Có template text T_LIB trong thư viện template" + U1,
       "1. Ở màn send all, GET THẲNG T_LIB vào broadcast → lưu → kiểm tra id template được gắn\n"
       "2. Gửi cho U1 → quan sát nội dung và giá trị gán\n"
       "3. Edit T_LIB gốc → mở broadcast đối chiếu nội dung\n"
       "4. Edit template ở broadcast → mở T_LIB gốc đối chiếu\n"
       "5. Xóa T_LIB gốc → kiểm tra template gắn ở broadcast\n"
       "6. Xóa template ở broadcast → kiểm tra T_LIB gốc\n"
       "7. Lặp lại toàn bộ ở màn scenario và remind",
       "get thẳng ở 3 màn; sửa/xóa 2 chiều",
       "- Template gắn ở màn khác chính là id của T_LIB gốc\n"
       "- Edit T_LIB gốc: template gắn ở màn khác ĐỔI THEO\n"
       "- Edit ở màn khác: T_LIB gốc cũng ĐỔI THEO\n"
       "- Xóa T_LIB gốc: template gắn ở màn khác BỊ XÓA theo\n"
       "- Xóa ở màn khác: T_LIB gốc KHÔNG bị ảnh hưởng",
       note="Nguồn: Template type text r212-r217, r236-r241, r259-r264, r283-r288, r306-r311."),

    tc("Gửi template từ màn khác", "FUNC-001", "Normal",
       "Copy cả broadcast / scenario / remind → các template bên trong giữ nguyên vị trí",
       ADM + "\n- Có 1 broadcast, 1 scenario và 1 remind, mỗi cái chứa ≥3 template theo thứ tự xác định",
       "1. Copy broadcast → mở bản copy, đối chiếu thứ tự template bên trong\n"
       "2. Copy scenario → đối chiếu thứ tự template trong từng step\n3. Copy remind → đối chiếu",
       "3 loại đối tượng, mỗi cái ≥3 template",
       "- Bản copy của cả 3: các template bên trong GIỮ NGUYÊN thứ tự như bản gốc",
       note="Nguồn: Template type text r224, r271 + khối copy remind."),

    tc("Gửi template từ màn khác", "REG-URL-001", "Normal",
       "Template tạo tại màn khác: action URL redirect (còn hạn / hết hạn / expired msg) lưu và chạy đúng",
       ADM + "\n- Tạo template text có URL tại màn send all / scenario / remind" + U1,
       "1. Tại mỗi màn, tạo template text có URL và setting action redirect (action còn hạn, "
       "action hết hạn, message hết hạn) → lưu\n"
       "2. Kiểm tra bản ghi `template_url_redirect`\n3. Gửi cho U1 → U1 bấm URL khi còn hạn → quan sát\n"
       "4. Chờ qua hạn → U1 bấm URL → quan sát",
       "3 màn × 3 cấu hình action URL",
       "- `template_url_redirect` lưu đúng action_id, out_time_action_id và message hết hạn\n"
       "- Bấm khi còn hạn: chạy action còn hạn\n- Bấm sau hạn: chạy action hết hạn / hiện message hết hạn",
       note="Nguồn: Template type text r204, r228, r251, r275, r298."),

    # ═════════════ 37. Copy & Backup ═════════════
    tc("Copy & Backup", "DATA-BACKUP-001", "Normal",
       "Backup template text (mới và cũ) → backup nội dung + setting shorten URL, KHÔNG backup setting url redirect",
       ADM + "\n- Bot A có template text MỚI và template text CŨ, đều có URL và tick/không tick shorten URL\n"
              "- Bot B là bot nhận backup",
       "1. Ở bot A tạo folder template đủ các loại (text, button, media, stamp, location)\n"
       "2. Bot nhận: sao chép mã dữ liệu (コピーコード) của bot B\n"
       "3. Ở bot A: dán mã bot nhận vào データ受信コード → chờ hệ thống xử lý\n"
       "4. Xem trạng thái ở bot gốc tới khi hiện 処理完了済\n"
       "5. Ở bot B: kiểm tra nội dung message, trạng thái checkbox shorten URL và tab URL redirect",
       "template text mới và cũ; backup A → B",
       "- Bot B có template với ĐÚNG nội dung message của bot A\n"
       "- Trạng thái checkbox shorten URL được backup đúng\n"
       "- Setting của URL redirect (action, thời hạn) KHÔNG được backup",
       env="PRODUCTION",
       note="Nguồn: Template type text r168, r176 + Improve list template r572. ⚠ TC gốc r168 note "
            "「job chưa sửa」. Spec KHÔNG có mục backup cho FA-010 → xem MT-11. "
            "RULE-08: backup là job nền, phải xác nhận trên PRODUCTION."),

    tc("Copy & Backup", "DATA-BACKUP-001", "Normal",
       "Backup template text: code/link được replace sang bản ghi MỚI của bot nhận theo từng loại",
       ADM + "\n- Bot A có template text chèn: link form-answer, code form, code friend info basic, "
              "code friend info tự tạo, link item, code conversion, link booking event, link booking calendar\n"
              "- Bot B là bot nhận backup",
       "1. Backup dữ liệu bot A sang bot B\n2. Ở bot B mở template text tương ứng\n"
       "3. Đối chiếu từng code/link với bản ghi mới của bot B\n4. Gửi template ở bot B cho 1 friend và bấm link",
       "8 loại code/link trong 1 template",
       "- link form-answer: thay bằng link form MỚI của bot B\n"
       "- code form: thay bằng code form tương ứng của bot B\n"
       "- code friend info BASIC: giữ NGUYÊN\n"
       "- code friend info tự tạo `[FRIEND_INFO_<id mã hoá>]`: thay đúng id friend info mới của bot B\n"
       "- link item: GIỮ NGUYÊN (item chưa support backup)\n"
       "- code conversion: thay bằng code conversion mới\n"
       "- link booking event: thay bằng link event mới\n"
       "- link booking calendar: GIỮ NGUYÊN (calendar chưa support backup)",
       env="PRODUCTION",
       note="Nguồn: Template type text r169-r182. ⚠ TC gốc r174 note「Nhắn Duy sửa thêm backup cho link "
            "booking event」→ cần xác nhận trạng thái hiện tại; item và calendar chưa support backup "
            "→ xem MT-11."),

    tc("Copy & Backup", "DATA-BACKUP-001", "Normal",
       "Backup template đủ 5 loại (text / button / media / stamp / location) → bot nhận có đủ và gửi được",
       ADM + "\n- Bot A có folder template chứa đủ 5 loại template\n- Bot B là bot nhận backup",
       "1. Backup dữ liệu bot A sang bot B, chờ tới trạng thái 処理完了済\n"
       "2. Ở bot B: mở màn template, đối chiếu folder và danh sách template\n"
       "3. Mở edit từng loại template ở bot B → đối chiếu dữ liệu\n"
       "4. Gửi từng loại cho 1 friend của bot B → quan sát tin trên LINE",
       "5 loại template; backup A → B",
       "- Bot B có đủ folder và 5 loại template với dữ liệu khớp bot A\n"
       "- Mở edit hiện đủ dữ liệu từng loại\n- Gửi được và tin trên LINE hiện đúng nội dung",
       env="PRODUCTION",
       note="Nguồn: Improve list template r572 + các dòng「Backup temp」của Type stamp / Type location / "
            "Type ảnh. ⚠ Phần lớn TC gốc chỉ có tiêu đề → kết quả mong đợi ở đây là SUY LUẬN CỦA AI, "
            "cần Leader xác nhận. Xem MT-11."),

    # ═════════════ 38. Recover dữ liệu lỗi ═════════════
    tc("Recover dữ liệu lỗi", "DATA-MIG-001", "Normal",
       "Bug KH #33911: recover img_path của tmp_button có 1 hoặc 2 dấu / ở đầu → ảnh button hiển thị lại được",
       ADM + "\n- Bảng `tmp_button` có bản ghi `img_path` bị 1 dấu「/」ở đầu và bản ghi bị 2 dấu「//」\n"
              "- Đã tạo template cho cả 4 loại button để test\n- Job recover chưa chạy",
       "1. TRƯỚC recover: mở màn edit template button và preview → ghi nhận ảnh bị lỗi\n"
       "2. Chạy job recover bảng `tmp_button`\n3. Mở lại màn edit template → quan sát ảnh\n"
       "4. Preview ở màn list template, màn list template con của group, và preview khi send template\n"
       "5. Lặp lại cho cả trường hợp 1 dấu / và 2 dấu //",
       "`img_path` có 1 dấu / và 2 dấu //; 4 loại button",
       "- Trước recover: button hiển thị ảnh LỖI\n"
       "- Sau recover: button HIỂN THỊ ĐƯỢC ảnh ở màn edit và ở cả 3 điểm preview\n"
       "- Kết quả giống nhau với cả 4 loại button",
       env="PRODUCTION",
       note="Nguồn: Template button r1467-r1482 (Bug KH #33911, 22/01/2026 — không hiển thị preview "
            "của template; recover data cho KH). RULE-08: job recover data phải xác nhận trên PRODUCTION."),

    tc("Recover dữ liệu lỗi", "MSG-001", "Normal",
       "Bug KH #33911: sau recover, gửi template button qua web và job → ảnh hiện đúng ở LINE, chat 1:1 và app",
       ADM + "\n- Đã chạy job recover `tmp_button`" + U1,
       "1. Gửi template button qua web (send test / chat 1:1) cho U1 → quan sát ảnh trên LINE, "
       "trên chat 1:1 của tool và trên app mobile\n"
       "2. Gửi qua job (broadcast) → quan sát 3 nơi\n3. Lặp lại cho cả 4 loại button",
       "2 đường gửi × 3 nơi hiển thị × 4 loại button",
       "- Mọi lượt: ảnh button hiển thị ĐÚNG ở LINE user, chat 1:1 và app mobile",
       env="PRODUCTION",
       note="Nguồn: Template button r1473-r1489."),

    tc("Recover dữ liệu lỗi", "FUNC-001", "Normal",
       "Bug KH #33911: copy template vừa recover → bản copy hiển thị ảnh đúng",
       ADM + "\n- Đã chạy job recover `tmp_button`" + U1,
       "1. Copy 1 template button vừa được recover\n2. Mở bản copy → quan sát ảnh ở màn edit và preview\n"
       "3. Gửi bản copy cho U1 → quan sát ảnh trên LINE",
       "template vừa recover",
       "- Bản copy hiển thị được ảnh ĐÚNG ở màn edit, preview và trong tin trên LINE",
       note="Nguồn: Template button r1490."),

    tc("Recover dữ liệu lỗi", "DATA-MIG-001", "Normal",
       "Bug KH #33911: recover bảng capture_templates (type = 2) — thumbnail_path dạng //ext-media-s...",
       ADM + "\n- Bảng `capture_templates` có bản ghi `type` = 2 với `content` chứa `thumbnail_path` lỗi "
              "dạng「//ext-media-s...」\n- Gồm bản ghi lưu kiểu TEXT thường (job) và kiểu ENCODE (web)",
       "1. Với bản ghi kiểu TEXT thường: ghi nhận `content` trước recover (1 ảnh lỗi và nhiều ảnh lỗi)\n"
       "2. Với bản ghi kiểu ENCODE (web): ghi nhận `content` trước recover (1 ảnh lỗi và nhiều ảnh lỗi)\n"
       "3. Chạy job recover bảng `capture_templates`\n"
       "4. Đối chiếu `content` sau recover cho từng bản ghi\n"
       "5. Kiểm tra thêm một vài `template_capture_id` khác chọn ngẫu nhiên",
       "capture_templates type = 2; kiểu text thường và kiểu encode; 1 ảnh và nhiều ảnh lỗi",
       "- Sau recover: `thumbnail_path` trong `content` được sửa về đúng dạng đường dẫn hợp lệ\n"
       "- Cả 2 kiểu lưu (text thường và encode) đều được recover đúng\n"
       "- Trường hợp nhiều ảnh lỗi: TẤT CẢ ảnh trong `content` đều được sửa\n"
       "- Các `template_capture_id` chọn ngẫu nhiên cũng đúng",
       env="PRODUCTION",
       note="Nguồn: Template button r1491-r1497 (Bug KH #33911 — recover bảng capture_templates ở "
            "Database message). Spec liệt kê `capture_templates` là bảng audit nhưng không mô tả cấu "
            "trúc `content` → xem MT-47."),

    tc("Recover dữ liệu lỗi", "SEC-ISO-001", "Abnormal",
       "Bug KH #36384: URL edit template con chứa /?utm_source=... → template_child_id phải ép int, content group không nhiễm",
       ADM + "\n- Có group template G (id = X) chứa ≥1 template con (id = Y)",
       "1. Mở URL: /basic/template-v2/add-template?template_group_id=X&template_child_id=Y"
       "/?utm_source=line&utm_medium=social&utm_id=syanai20260515\n"
       "2. Quan sát màn edit template con có load đúng template Y hay không\n"
       "3. Sửa nội dung text (thêm 1 ký tự)\n4. Bấm 保存\n5. Back ra màn list folder template\n"
       "6. Kiểm tra `template.content` của group X",
       "URL edit có đuôi /?utm_source=line&utm_medium=social&utm_id=syanai20260515",
       "- Bước 2: load ĐÚNG template Y, KHÔNG hiển thị error\n- Bước 4: 保存 thành công, không alert lỗi\n"
       "- Bước 5: màn list template render bình thường, KHÔNG có error\n"
       "- Bước 6: `template.content` của group X là chuỗi int phân tách bằng dấu phẩy, "
       "KHÔNG chứa「/?utm_source」hay bất kỳ ký tự non-numeric nào",
       note="Nguồn: Improve list template r630 (TC-NEW-01 của Bug KH #36384, 12/05/2026 — click folder "
            "'定期配信用' hiển thị error). Spec KHÔNG mô tả validate tham số URL → xem MT-48."),

    tc("Recover dữ liệu lỗi", "SEC-ISO-001", "Abnormal",
       "Bug KH #36384: storeTemplate / updateTemplate / cloneTemplate cũng phải ép int template_*_id",
       ADM + "\n- Có group template và template con hợp lệ\n"
              "- (Chỉ chạy sau khi Dev confirm 3 function này cùng nhận template_*_id từ request)",
       "1. Gọi endpoint storeTemplate với `template_child_id=12345/?utm_source=line` → kiểm tra "
       "`template.content` của group\n2. Lặp lại với updateTemplate\n3. Lặp lại với cloneTemplate",
       "input `template_child_id=12345/?utm_source=line` cho 3 function",
       "- Cả 3 function đều ép int ĐÚNG — không function nào lưu chuỗi gốc vào `template.content`\n"
       "- `content` của group luôn là chuỗi int CSV",
       note="Nguồn: Improve list template r631 (TC-NEW-08). ⚠ Điều kiện tiền đề của TC gốc ghi rõ "
            "「chỉ chạy sau khi Dev confirm scope」→ cần Leader xác nhận trước khi chạy."),

    tc("Recover dữ liệu lỗi", "SEC-ISO-001", "Abnormal",
       "Bug KH #36384 — bảo mật: user bot A paste URL edit template của bot B → bị từ chối, không corrupt data bot B",
       ADM + "\n- Đã login bot A\n- Biết `template_group_id` và `template_child_id` của bot B",
       "1. Login bot A\n2. Paste URL /basic/template-v2/add-template?template_group_id={B_group}"
       "&template_child_id={B_child}\n3. Quan sát màn load\n4. Cố bấm 保存 với nội dung mới\n"
       "5. Kiểm tra dữ liệu template của bot B",
       "URL edit template của bot B, login bằng bot A",
       "- Bước 3: hệ thống TỪ CHỐI access (redirect / 403 / hiển thị message lỗi), KHÔNG load template "
       "của bot B\n"
       "- Bước 4: KHÔNG lưu được\n- Bước 5: dữ liệu template của bot B không bị thay đổi",
       note="Nguồn: Improve list template r632 (TC-NEW-04 — Cross-account/Security, checklist LME "
            "§A.2 Security). ⚠ Spec BR-03 chỉ mô tả check `botIdCurrent == getBotId()` ở `store()`, "
            "không nói về màn edit → xem MT-48."),

    tc("Recover dữ liệu lỗi", "REG-RUN-001", "Normal",
       "Bug KH #36384 — regression: tạo / edit / copy template ở folder default và folder khác default đều đúng",
       ADM + "\n- Có folder 未分類 (default) và folder F1 (khác default)" + U1,
       "1. Ở folder 未分類: tạo group template; tạo lần lượt template con các loại "
       "(text, button standard/color/image/quick reply, image thường, image map, video, audio, sticker, "
       "location) → mỗi lần kiểm tra màn list, màn edit, preview và gửi cho U1\n"
       "2. Ở folder 未分類: edit từng loại template con → kiểm tra 4 điểm trên\n"
       "3. Ở folder 未分類: copy group template và copy template đơn → kiểm tra\n"
       "4. Lặp lại toàn bộ ở folder F1 (khác default)",
       "2 loại folder × 11 loại template con × 3 thao tác (tạo / edit / copy)",
       "- Mọi tổ hợp: tạo/edit/copy thành công\n"
       "- Template hiển thị bình thường ở màn list, màn edit và preview\n"
       "- Gửi cho U1 nhận đúng nội dung",
       note="Nguồn: Improve list template r574-r629 (regression của Bug KH #36384). Gộp ma trận vì "
            "CÙNG 1 kết quả mong đợi. Folder 未分類 (category_id = 0) có nhánh code riêng → xem MT-18."),

    # ═════════════ 39. App mobile ═════════════
    tc("App mobile", "SYNC-APP-001", "Normal",
       "Preview template trên APP: template dạng cũ và 11 dạng mới đều hiện đủ nội dung, ảnh, màu, ngắt dòng",
       ADM + "\n- Đã cài app mobile LME và đăng nhập bot A\n"
              "- Có template dạng CŨ và 11 template dạng mới (text, btn standard, btn color, btn ảnh, "
              "btn quick, ảnh thường, ảnh image map, audio, video, stamp, location)",
       "1. Trên app, mở preview template dạng CŨ → quan sát\n"
       "2. Mở preview lần lượt 11 template dạng mới → với mỗi loại kiểm tra: hiển thị đủ nội dung, "
       "ảnh, màu (với btn color) và ngắt dòng",
       "template dạng cũ + 11 dạng mới",
       "- Preview trên app hiện ĐỦ nội dung của từng loại\n"
       "- Btn standard: đủ nội dung, ảnh và ngắt dòng\n- Btn color: đúng cả MÀU\n"
       "- Media/stamp/location hiện đúng dạng đặc trưng",
       env="PRODUCTION",
       note="Nguồn: Test app r3-r14. RULE-08 + SYNC-APP: hành vi app mobile phải xác nhận trên PRODUCTION."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "Send template từ APP: 11 dạng template → kiểm 3 nơi (chat 1:1 app, chat 1:1 web, LINE user)",
       ADM + "\n- Đã cài app mobile LME và đăng nhập bot A\n- Có 11 template dạng mới + 1 template dạng cũ" + U1,
       "1. Trên app, gửi lần lượt từng template cho U1\n"
       "2. Với mỗi lượt: quan sát tin ở chat 1:1 trên APP, ở chat 1:1 trên WEB và ở LINE của U1\n"
       "3. Với btn color: kiểm tra kích cỡ và màu",
       "12 loại template × 3 nơi hiển thị",
       "- Mọi loại: tin hiển thị đúng ở cả 3 nơi (chat 1:1 app, chat 1:1 web, LINE user)\n"
       "- Btn color: kích cỡ và màu đúng",
       env="PRODUCTION",
       note="Nguồn: Test app r15-r26. RULE-07: xác nhận 3 tầng cho cùng 1 hành động."),

    tc("App mobile", "SYNC-APP-001", "Normal",
       "Preview template button standard trên app KHÔNG bị đổi style theo Review #30710",
       ADM + "\n- Đã cài app mobile\n- Có 4 biến thể template button standard",
       "1. Trên app, mở preview khi send template button standard\n"
       "2. So sánh style với preview trên web (đã áp text xanh #3771BE, bỏ border)",
       "4 biến thể button standard",
       "- Preview trên app giữ style CŨ, KHÔNG áp style mới của Review #30710\n"
       "- Đây là hành vi chủ ý, không phải bug",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ+ check Bug Kh r100 (「preview vẫn như cũ, không sửa」)."),

    # ═════════════ 40. Phân quyền & môi trường ═════════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff ĐƯỢC phân quyền template → thao tác đầy đủ trên màn template",
       "- Bot A có staff S1 ĐƯỢC phân quyền màn template\n- Đăng nhập bằng account S1" + U1,
       "1. S1 mở /basic/message-template → quan sát màn hình\n2. S1 tạo folder và group template\n"
       "3. S1 tạo / edit / copy / xóa template con các loại\n4. S1 sort folder và sort template\n"
       "5. S1 mở modal preview - send test và gửi test cho U1\n"
       "6. S1 hover vào nút (...) của panel để xem menu thao tác panel",
       "staff S1 có quyền template",
       "- S1 truy cập được màn template và thực hiện được toàn bộ thao tác ở bước 2-5\n"
       "- Hover nút (...) của panel: hiện đủ thông tin thao tác panel\n"
       "- Gửi test thành công, U1 nhận được tin",
       note="Nguồn: Template button r965-r975, r1618 + Improve list template r492 + "
            "Task nhỏ+ check Bug Kh r99."),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "Staff KHÔNG được phân quyền template → chặn cả ở UI và ở tầng API (truy cập URL trực tiếp)",
       "- Bot A có staff S2 KHÔNG được phân quyền màn template\n- Đăng nhập bằng account S2",
       "1. S2 mở menu chính → quan sát có mục template hay không\n"
       "2. S2 paste trực tiếp URL /basic/message-template → quan sát\n"
       "3. S2 paste URL màn edit template /basic/template-v2/add-template?template_group_id=X"
       "&template_child_id=Y → quan sát\n"
       "4. S2 gọi trực tiếp endpoint POST /ajax/init-template và POST /ajax/template-v2/save-template "
       "→ quan sát response\n5. Kiểm tra dữ liệu template của bot A có bị thay đổi hay không",
       "staff S2 không có quyền template; 2 URL + 2 endpoint API",
       "- Menu chính KHÔNG hiện mục template\n"
       "- Truy cập trực tiếp 2 URL: bị từ chối (redirect / 403 / message lỗi), không load được màn\n"
       "- Gọi trực tiếp 2 endpoint API: bị từ chối, KHÔNG ghi/sửa được dữ liệu\n"
       "- Dữ liệu template của bot A không bị thay đổi",
       note="Nguồn: Template button r1619 (Account staff không quyền template). ⚠ Spec ghi rõ "
            "「Staff permission: Kiểm tra ở middleware level (không thấy trong controller) "
            "[Trung bình]」→ rủi ro chưa enforce ở tầng API, xem MT-49. "
            "Chiều API là SUY LUẬN mở rộng của AI theo checklist PERM — cần Leader xác nhận."),

    tc("Phân quyền & môi trường", "SEC-ISO-001", "Abnormal",
       "Bot ID verification: đã chuyển sang account khác rồi submit form tạo template → bị chặn",
       ADM + "\n- Đăng nhập admin có quyền trên bot A và bot B",
       "1. Mở màn tạo template của bot A, nhập 管理名 nhưng CHƯA bấm tạo\n"
       "2. Ở tab khác, chuyển account sang bot B\n3. Quay lại tab cũ, bấm「テンプレートを作成」\n"
       "4. Quan sát thông báo và kiểm tra bảng `template` của cả 2 bot",
       "chuyển bot giữa lúc đang mở form tạo",
       "- Hiện thông báo lỗi dạng「別のアカウントに切り替えたので...」\n"
       "- KHÔNG tạo được template ở cả bot A và bot B",
       note="Nguồn: spec BR-03 (`MessageTemplateController@store:346` kiểm tra "
            "`botIdCurrent == getBotId()`). ⚠ Corpus KHÔNG có TC nào cho rule này → TC bổ sung để lấp "
            "GAP, cần Leader xác nhận nguyên văn thông báo lỗi."),

    tc("Phân quyền & môi trường", "STATE-001", "Abnormal",
       "Backup đang chạy → mọi thao tác GHI trên màn template bị chặn kèm thông báo",
       ADM + "\n- Bot A đang có tiến trình backup ở trạng thái đang chạy",
       "1. Trong lúc backup đang chạy, thử tạo folder template\n2. Thử tạo group template\n"
       "3. Thử 保存 template con\n4. Thử xóa / sort / chuyển folder\n"
       "5. Quan sát thông báo ở từng thao tác\n6. Chờ backup xong rồi thử lại các thao tác trên",
       "backup đang chạy; 5 thao tác ghi",
       "- Toàn bộ thao tác GHI bị chặn, hiện thông báo về việc đang backup\n"
       "- Dữ liệu template không bị thay đổi trong lúc backup\n"
       "- Sau khi backup xong: các thao tác chạy bình thường",
       note="Nguồn: spec BR-02 (`MessageTemplateController@store/save/ajaxInitTemplate` kiểm tra "
            "`BackupHistory`, trả `MESSAGE_NOTIFY_BACKUP`). ⚠ Corpus KHÔNG có TC nào cho rule này → "
            "TC bổ sung để lấp GAP, cần Leader xác nhận nguyên văn thông báo."),

    tc("Phân quyền & môi trường", "STATE-001", "Normal",
       "Cookie folder_template: folder đang chọn được ghi nhớ theo bot, hết hạn thì reset về mặc định",
       ADM + "\n- Bot A có folder F1, F2, F3",
       "1. Ở bot A chọn folder F2 → reload màn hình → quan sát folder đang chọn\n"
       "2. Chuyển sang bot B, chọn folder khác → quay lại bot A → quan sát folder đang chọn\n"
       "3. Xóa cookie `folder_template` của trình duyệt → reload → quan sát folder đang chọn",
       "cookie folder_template theo bot_id, expire 14400 phút (10 ngày)",
       "- Reload: vẫn giữ folder F2 đang chọn\n"
       "- Chuyển bot rồi quay lại bot A: vẫn giữ F2 (cookie tách theo bot_id)\n"
       "- Xóa cookie: folder đang chọn reset về mặc định (未分類)",
       note="Nguồn: spec BR-13 (`BasicController@folderSetCookie`, cookie `folder_template`, "
            "key = bot_id, expire 14400 phút). ⚠ Corpus KHÔNG có TC nào cho rule này → TC bổ sung để "
            "lấp GAP, cần Leader xác nhận."),

    tc("Phân quyền & môi trường", "ENV-001", "Normal",
       "Regression trên PRODUCTION: media, domain và job gửi tin của template chạy đúng",
       "- Đăng nhập admin bot thật trên môi trường PRODUCTION\n- Có template đủ 5 loại và 1 broadcast đặt lịch",
       "1. Upload ảnh / video / audio cho template trên PRODUCTION → quan sát URL media server\n"
       "2. Gửi từng loại template cho 1 friend thật → quan sát tin trên LINE\n"
       "3. Đặt lịch broadcast có template → chờ job chạy → quan sát tin\n"
       "4. Bấm URL trong template text và bấm nút/vùng ảnh → quan sát domain của link mở ra",
       "5 loại template; job đặt lịch; media server và domain",
       "- Upload media thành công, URL trỏ về media server của PRODUCTION\n"
       "- Tin gửi qua web và qua job đều đến LINE user đầy đủ\n- Domain của link mở ra là domain production",
       env="PRODUCTION",
       note="RULE-08: media · domain · job · loadbalance bắt buộc xác nhận trên PRODUCTION. "
            "⚠ Corpus KHÔNG có tab riêng cho môi trường của FA-010 → TC bổ sung theo RULE-08, "
            "cần Leader xác nhận phạm vi."),
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
for _r in S6:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
