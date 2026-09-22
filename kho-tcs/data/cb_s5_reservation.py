# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 9: Đặt lịch đổi LOA.

Màn「05-A 予約済み」+ modal xác nhận xóa đặt lịch + modal xác nhận thực hiện đổi LOA.
Tính năng đặt hẹn đổi LOA được thêm ở đợt 04/2026 (tab Info: "Thêm tính năng đặt hẹn
change bot"), CHỈ dành cho bot plan Standard trở lên (bot Free bị khoá — xem S3).

⚠️ MT-11 — tên bảng hàng đợi: spec job (lesson-booking/job/job-spec.md §2.6) ghi
`schedule_change_bot` (số ít), TCs ghi `schedule_change_bots` (số nhiều). Chưa chốt.
"""
from _common import tc

RES = ("- Đăng nhập Admin chủ (主管理者) của bot plan Standard trở lên\n"
       "- Đã hoàn tất luồng đặt lịch đổi LOA với 1 LOA mới hợp lệ\n"
       "- Đang ở màn đã đặt lịch (「05-A 予約済み」)")
NEW = ("- Đăng nhập Admin chủ của bot plan Standard trở lên\n"
       "- Bot CHƯA có đặt lịch đổi LOA nào\n"
       "- Đã chuẩn bị 1 LOA mới hợp lệ (Messaging API + LINE Login cùng provider)")

S9 = [
    # ═══════════════ 9. Đặt lịch đổi LOA ═══════════════
    tc("Đặt lịch đổi LOA", "FUNC-UNIQ-001", "Normal",
       "Đặt lịch đổi LOA thành công → vào màn danh sách đặt lịch, 1 bot chỉ được 1 item",
       NEW,
       "1. Vào màn chọn phương thức, chọn option 2「LINE公式アカウント入れ替え予約をする」\n"
       "2. Nhập 4 field thông tin kết nối hợp lệ, đi hết các bước xác nhận\n"
       "3. Quan sát màn hình sau khi xác nhận\n"
       "4. Query DB bảng schedule_change_bots đếm số bản ghi của bot này\n"
       "5. Thử đặt lịch lần 2 cho cùng bot đó",
       "1 LOA mới hợp lệ; thử đặt lịch 2 lần",
       "- Sau khi xác nhận: chuyển tới màn danh sách item đặt lịch đổi LOA\n"
       "- DB schedule_change_bots: ĐÚNG 1 bản ghi cho bot này\n"
       "- Thử đặt lịch lần 2: bị chặn (hoặc bị điều hướng về màn đã đặt lịch hiện có)\n"
       "- KHÔNG tồn tại 2 item đặt lịch cho cùng 1 bot",
       note="Nguồn: Change bot r104 (TR=OK, '1 bot chỉ được 1 item đặt lịch change bot') + r253 + "
            "TC-CBF-021 (BR-12/BR-34; Pass dev). ⚠️ MT-11 tên bảng. RULE-07 — verify DB. "
            "Evidence: ảnh màn đích + query schedule_change_bots + ảnh lần đặt lịch thứ 2."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Màn đã đặt lịch hiển thị thông tin LOA MỚI, KHÔNG hiển thị thông tin LOA cũ",
       RES,
       "1. Vào màn đã đặt lịch\n"
       "2. Đối chiếu tên bot / Channel ID hiển thị với LOA MỚI đã đặt lịch\n"
       "3. Kiểm tra có dòng nào hiển thị thông tin LOA CŨ (đang dùng) không\n"
       "4. Query DB bảng schedule_change_bots đối chiếu giá trị",
       "LOA mới: tên + Channel ID đã ghi lại khi đặt lịch",
       "- Hiển thị thông tin LOA MỚI: tên bot, Channel ID (masked)\n"
       "- KHÔNG hiển thị thông tin LOA cũ lẫn vào khu vực này\n"
       "- Giá trị trên màn KHỚP bản ghi trong schedule_change_bots",
       note="Nguồn: Change bot r191 (TR=OK, stg=OK: 'hiển thị thông tin change bot mới / không hiển thị "
            "thông tin bot cũ / check db: schedule_change_bots'). RULE-07. "
            "Evidence: ảnh màn + query schedule_change_bots."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Màn đã đặt lịch hiển thị đúng banner trạng thái và mốc thời gian đặt lịch",
       RES + "\n- Đã ghi lại thời điểm (ngày giờ) thao tác đặt lịch",
       "1. Ghi lại thời điểm chính xác khi bấm xác nhận đặt lịch\n"
       "2. Vào màn đã đặt lịch\n"
       "3. Đọc banner trạng thái phía trên\n"
       "4. Đối chiếu mốc「予約操作日時」với thời điểm đã ghi ở bước 1\n"
       "5. Query DB cột thời gian tạo bản ghi",
       "Thời điểm đặt lịch ghi tay theo đồng hồ thật",
       "- Có banner trạng thái nêu rõ bot đang ở trạng thái ĐÃ ĐẶT LỊCH đổi LOA\n"
       "- Mốc「予約操作日時」KHỚP thời điểm thao tác (lệch không quá 1 phút)\n"
       "- Giá trị trên màn khớp cột thời gian trong DB\n"
       "- Không hiển thị timestamp sai múi giờ (lệch 7/9 giờ)",
       note="Nguồn: TC-CBF-069 (BR-32, QA-spec-019 CONFIRMED; Pass dev, Blocked staging). "
            "Điểm bổ sung của AI: kiểm múi giờ — không nguồn nào nói, nhưng LME có dữ liệu JP. "
            "RULE-07. Evidence: ảnh màn + giờ thật + query DB."),

    tc("Đặt lịch đổi LOA", "STATE-001", "Normal",
       "Bot mới ở trạng thái chỉ-lưu-credentials — CHƯA kết nối thật, bot cũ vẫn hoạt động bình thường",
       RES + "\n- Bot cũ vẫn đang có friend và hoạt động",
       "1. Sau khi đặt lịch, kiểm tra bên LINE: webhook URL của LOA MỚI có bị đổi chưa\n"
       "2. Kiểm tra bên LINE: LINE Login channel của LOA mới có LIFF app mới nào chưa\n"
       "3. Cho 1 friend gửi tin cho LOA CŨ → kiểm tra chat 1:1 của L Message\n"
       "4. Query DB bảng bots: có bản ghi mới nào không\n"
       "5. Kiểm tra dữ liệu bot cũ (friend, tag) còn nguyên không",
       "LOA mới đã đặt lịch nhưng chưa thực hiện",
       "- Bên LINE: webhook URL của LOA mới CHƯA bị đổi sang L Message\n"
       "- Bên LINE: CHƯA tạo LIFF app mới cho LOA mới\n"
       "- LOA CŨ vẫn hoạt động: friend gửi tin vẫn vào chat 1:1 bình thường\n"
       "- DB bots: KHÔNG có bản ghi mới (chỉ có bản ghi trong schedule_change_bots)\n"
       "- Dữ liệu bot cũ (friend, tag, scenario) còn nguyên, không bị xóa",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-070 (STATE-001, BR-33, QA-spec-020 CONFIRMED 'chỉ lưu credentials, chưa kết nối "
            "thật'; Blocked cả 2 env). RULE-06 (verify trên LINE app) + RULE-07 + RULE-08. "
            "Evidence: ảnh LINE Developers (webhook + LIFF) + ảnh chat 1:1 + query bots."),

    tc("Đặt lịch đổi LOA", "STATE-001", "Boundary",
       "Đặt lịch KHÔNG có thời hạn — vẫn active sau nhiều ngày, không tự hết hiệu lực",
       RES + "\n- Bản ghi đặt lịch được tạo cách đây ≥7 ngày (seed hoặc chờ thật)",
       "1. Đặt lịch đổi LOA, ghi lại thời điểm\n"
       "2. Sau ≥7 ngày, vào lại màn đổi LOA của bot đó\n"
       "3. Quan sát có còn hiển thị màn đã đặt lịch không\n"
       "4. Query DB schedule_change_bots kiểm tra trạng thái bản ghi\n"
       "5. Thử bấm nút thực hiện đổi LOA",
       "Bản ghi đặt lịch tuổi ≥7 ngày",
       "- Sau ≥7 ngày: vẫn hiển thị màn đã đặt lịch, đặt lịch vẫn active\n"
       "- DB: bản ghi schedule_change_bots vẫn còn, trạng thái không tự chuyển sang hết hạn\n"
       "- Nút thực hiện đổi LOA vẫn bấm được\n"
       "- Không có thông báo 'đặt lịch đã hết hạn'",
       note="Nguồn: TC-CBF-071 (STATE-001, BR-35, QA-spec-021 CONFIRMED 'không có thời hạn'; Pass dev). "
            "⚠️ RISK: đặt lịch không hết hạn nghĩa là credentials LOA mới có thể bị lưu vô thời hạn — "
            "nếu LOA mới bị xóa/đổi secret bên LINE thì đặt lịch thành rác (xem TC execute re-validate). "
            "Evidence: query DB theo 2 mốc thời gian + ảnh màn."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Bấm「LINE公式アカウント 入れ替えを実行」→ hiện modal xác nhận thực hiện",
       RES,
       "1. Ở màn đã đặt lịch, bấm nút「LINE公式アカウント 入れ替えを実行」\n"
       "2. Quan sát modal hiện ra\n"
       "3. Đếm số dòng cảnh báo trong modal\n"
       "4. Quan sát màu 2 nút của modal",
       "Bot Standard có đặt lịch active",
       "- Hiện modal xác nhận thực hiện đổi LOA\n"
       "- Modal có ĐỦ 3 dòng cảnh báo (bullet) trước khi cho xác nhận\n"
       "- Nút xác nhận「入れ替えを実行する」màu vàng/cam (mức caution)\n"
       "- Có nút「キャンセル」",
       note="Nguồn: Change bot r193 (TR=OK, stg=OK) + TC-CBF-073 (Pass dev) + TC-CBF-074 (UI-003, BR-39 "
            "'đủ 3 bullet cảnh báo'; Blocked cả 2 env) + TC-CBF-075 (UI-003, BR-40 màu nút). "
            "Evidence: ảnh modal full + đếm bullet."),

    tc("Đặt lịch đổi LOA", "UI-003", "Normal",
       "Màu nút phân biệt mức nghiêm trọng: xóa đặt lịch màu ĐỎ vs thực hiện đổi LOA màu VÀNG/CAM",
       RES,
       "1. Mở modal xác nhận XÓA đặt lịch, chụp ảnh nút「削除する」\n"
       "2. Đóng modal\n"
       "3. Mở modal xác nhận THỰC HIỆN đổi LOA, chụp ảnh nút「入れ替えを実行する」\n"
       "4. Đặt 2 ảnh cạnh nhau, đối chiếu màu",
       "2 modal của cùng màn đã đặt lịch",
       "- Nút「削除する」màu ĐỎ (destructive)\n"
       "- Nút「入れ替えを実行する」màu VÀNG/CAM (caution), KHÁC màu đỏ\n"
       "- 2 màu phân biệt rõ bằng mắt thường, không cùng tông",
       note="Nguồn: TC-CBF-075 (UI-003, BR-40; Blocked cả 2 env). "
            "Evidence: 2 ảnh nút đặt cạnh nhau."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Modal xác nhận thực hiện — bấm「入れ替えを実行する」→ chuyển NGAY sang màn tiến trình",
       RES + "\n- Modal xác nhận thực hiện đang mở",
       "1. Mở modal xác nhận thực hiện đổi LOA\n"
       "2. Bấm「入れ替えを実行する」, bấm đồng hồ bấm giây\n"
       "3. Đo thời gian tới lúc màn tiến trình hiện ra\n"
       "4. Query DB bảng bots + schedule_change_bots",
       "Bot Standard có đặt lịch active",
       "- Chuyển sang màn tiến trình đổi LOA NGAY (dưới 2 giây), không có delay/chờ đợi\n"
       "- Không hiện màn trắng giữa 2 màn\n"
       "- DB: tiến trình đổi LOA được khởi động (bản ghi bots mới hoặc trạng thái swap được set)\n"
       "- Sau khi hoàn tất: hiện modal thành công",
       env="PRODUCTION",
       note="Nguồn: Change bot r194 (TR=OK, stg=OK) + TC-CBF-076 (BR-38/FN-15, QA-spec-029 CONFIRMED "
            "'chuyển NGAY, không delay'; Blocked cả 2 env). ⚠️ MT-01. RULE-08. "
            "Evidence: video đo thời gian + query DB."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Modal xác nhận thực hiện — bấm「キャンセル」→ đóng modal, đặt lịch KHÔNG đổi",
       RES + "\n- Modal xác nhận thực hiện đang mở",
       "1. Ghi lại nội dung bản ghi schedule_change_bots\n"
       "2. Mở modal xác nhận thực hiện, bấm「キャンセル」\n"
       "3. Quan sát màn hình\n"
       "4. Query lại schedule_change_bots đối chiếu",
       "Bot Standard có đặt lịch active",
       "- Modal đóng, quay về màn đã đặt lịch\n"
       "- Đặt lịch VẪN active, không bị hủy\n"
       "- DB schedule_change_bots: bản ghi KHÔNG đổi (giống hệt trước khi mở modal)\n"
       "- KHÔNG khởi động tiến trình đổi LOA",
       note="Nguồn: Change bot r195 (TR=OK, stg=OK) + TC-CBF-078 (Pass dev). RULE-07. "
            "Evidence: ảnh màn + query DB trước/sau."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Bấm「接続予約を削除」→ hiện modal xác nhận xóa kèm cảnh báo không hoàn tác được",
       RES,
       "1. Ở màn đã đặt lịch, bấm nút「接続予約を削除」\n"
       "2. Quan sát modal hiện ra\n"
       "3. Đọc nội dung cảnh báo\n"
       "4. Quan sát 2 nút của modal",
       "Bot Standard có đặt lịch active",
       "- Hiện modal xác nhận xóa đặt lịch\n"
       "- Có cảnh báo「この操作は元に戻せません」(hoặc nội dung tương đương)\n"
       "- Có nút「削除する」màu đỏ và nút「キャンセル」\n"
       "- Modal KHÔNG tự xóa đặt lịch khi vừa mở",
       note="Nguồn: Change bot r192 (TR=OK, stg=OK: 'hiển thị modal confirm cancel') + TC-CBF-079 (Pass dev). "
            "Evidence: ảnh modal full."),

    tc("Đặt lịch đổi LOA", "DATA-DB-001", "Normal",
       "Xác nhận xóa đặt lịch → hiện thông báo thành công, xóa sạch dữ liệu, về màn chọn phương thức",
       RES + "\n- Modal xác nhận xóa đang mở",
       "1. Ghi lại id bản ghi trong schedule_change_bots\n"
       "2. Mở modal xác nhận xóa, bấm「削除する」\n"
       "3. Đọc thông báo hiện ra\n"
       "4. Quan sát màn hình đích\n"
       "5. Query DB schedule_change_bots tìm lại id đã ghi\n"
       "6. Kiểm tra bên LINE: có LIFF app / webhook nào bị thay đổi không",
       "id bản ghi đặt lịch đã ghi ở bước 1",
       "- Hiện thông báo「接続予約を削除しました」\n"
       "- Điều hướng về màn chọn phương thức đổi LOA\n"
       "- DB: bản ghi trong schedule_change_bots bị XÓA (không còn, hoặc chuyển trạng thái đã xóa rõ ràng)\n"
       "- Bên LINE: KHÔNG có thay đổi gì (vì đặt lịch chưa từng kết nối thật)\n"
       "- Bot cũ vẫn hoạt động bình thường",
       note="Nguồn: Change bot r196 (TR=OK, stg=OK) + TC-CBF-080 (DATA-DB-001, BR-36/BR-37, "
            "QA-spec-027/028 CONFIRMED; Pass dev). DATA-DB-001 BẮT BUỘC với mọi DELETE — RULE-07 "
            "không thay DB bằng UI. Evidence: ảnh thông báo + ảnh màn đích + query DB trước/sau."),

    tc("Đặt lịch đổi LOA", "FUNC-001", "Normal",
       "Modal xác nhận xóa — bấm「キャンセル」→ đặt lịch giữ nguyên",
       RES + "\n- Modal xác nhận xóa đang mở",
       "1. Ghi lại bản ghi schedule_change_bots\n"
       "2. Mở modal xác nhận xóa, bấm「キャンセル」\n"
       "3. Quan sát màn hình\n"
       "4. Query lại schedule_change_bots",
       "Bot Standard có đặt lịch active",
       "- Modal đóng, quay về màn đã đặt lịch\n"
       "- Đặt lịch VẪN active\n"
       "- DB: bản ghi KHÔNG bị xóa, không đổi giá trị",
       note="Nguồn: Change bot r197 (TR=OK, stg=OK) + TC-CBF-081 (Pass dev). RULE-07. "
            "Evidence: ảnh màn + query DB trước/sau."),

    tc("Đặt lịch đổi LOA", "CONC-001", "Boundary",
       "Double-click「削除する」→ chỉ xóa 1 lần, click thứ 2 không gây lỗi / không xóa thêm",
       RES + "\n- Modal xác nhận xóa đang mở",
       "1. Mở DevTools tab Network, xóa log\n"
       "2. Mở modal xác nhận xóa\n"
       "3. Double-click nhanh (<300ms) vào nút「削除する」\n"
       "4. Đếm số request DELETE trong Network\n"
       "5. Quan sát có thông báo lỗi nào không + query DB",
       "Double-click trong 300ms",
       "- Network: 1 request DELETE thành công; request thứ 2 (nếu có) trả lỗi không-tìm-thấy, không lỗi 500\n"
       "- Chỉ hiện 1 thông báo thành công, không hiện 2 lần\n"
       "- DB: bản ghi bị xóa 1 lần, không phát sinh lỗi dữ liệu\n"
       "- KHÔNG hiện thông báo lỗi khó hiểu cho user",
       note="Nguồn: TC-CBF-082 (CONC-001; Pass dev). CONC-001 BẮT BUỘC khi có nút thực thi hành động "
            "quan trọng. Evidence: Network đếm request + ảnh thông báo + query DB."),

    tc("Đặt lịch đổi LOA", "INTG-LINE-001", "Abnormal",
       "Thực hiện đổi LOA từ đặt lịch CŨ mà LOA mới đã bị xóa/đổi secret bên LINE → báo lỗi, không thực hiện",
       RES + "\n- Sau khi đặt lịch, đã vào LINE Developers XÓA channel hoặc ĐỔI channel secret của LOA mới",
       "1. Đặt lịch đổi LOA với LOA mới\n"
       "2. Vào LINE Developers, đổi channel secret của Messaging API channel đó (hoặc xóa channel)\n"
       "3. Quay lại L Message, bấm nút thực hiện đổi LOA\n"
       "4. Xác nhận ở modal\n"
       "5. Quan sát thông báo + query DB bots + kiểm tra bot cũ còn hoạt động không",
       "Channel secret của LOA mới đã bị đổi sau khi đặt lịch",
       "- Hệ thống RE-VALIDATE và báo lỗi rõ ràng, KHÔNG thực hiện đổi LOA\n"
       "- DB: KHÔNG tạo bản ghi bots mới, bot cũ giữ nguyên is_delete = 0\n"
       "- Bot CŨ vẫn hoạt động bình thường (friend gửi tin vẫn vào chat 1:1)\n"
       "- Đặt lịch vẫn còn để user sửa lại thông tin (hoặc được yêu cầu xóa và đặt lại)",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-077 (INTG-LINE-001; Blocked cả 2 env). ⏳ QA-dev-008 — TA đề xuất re-validate "
            "BẮT BUỘC nhưng CHƯA CONFIRMED bởi reviewer → hành vi mong đợi là SUY LUẬN, cần Leader chốt. "
            "Đây là rủi ro NẶNG kết hợp với TC-CBF-071 (đặt lịch không có thời hạn): credentials lưu vô "
            "thời hạn + không re-validate = đổi LOA sang channel chết. RULE-05 + RULE-08. "
            "Evidence: ảnh LINE Developers + ảnh thông báo lỗi + query bots + ảnh chat 1:1 bot cũ.",
       spec="Đã hỏi leader"),

    tc("Đặt lịch đổi LOA", "PERM-002", "Abnormal",
       "Staff gọi thẳng API xóa đặt lịch qua DevTools → bị từ chối",
       ("- Có tài khoản Staff thuộc cùng bot Standard\n"
        "- Bot có 1 đặt lịch đổi LOA đang active\n"
        "- Đã bắt được endpoint xóa đặt lịch từ phiên Admin"),
       "1. Đăng nhập Admin, mở DevTools, thực hiện xóa đặt lịch để bắt endpoint + payload\n"
       "2. Đặt lại 1 đặt lịch mới\n"
       "3. Đăng nhập bằng Staff, mở DevTools Console\n"
       "4. Gọi thẳng endpoint xóa đặt lịch với payload đã bắt\n"
       "5. Quan sát response + query DB schedule_change_bots",
       "Endpoint DELETE đặt lịch + payload bắt từ phiên Admin",
       "- Response trả 403 (hoặc mã lỗi quyền theo kết luận MT-02)\n"
       "- DB: bản ghi đặt lịch VẪN CÒN, không bị xóa\n"
       "- Không rò rỉ thông tin đặt lịch trong response",
       note="⚠️ MT-02 — quyền Staff chưa chốt. Nguồn: TC-CBF-099 (PERM-002 + MAP-PERM-02; Pass dev) + "
            "TC-CBF-093 (Staff gọi thẳng API bất kỳ endpoint bot-swap → 403). "
            "PERM-002 BẮT BUỘC khi có thao tác nhạy cảm (xóa). RULE-07. "
            "Evidence: ảnh response + query DB.",
       spec="Đã hỏi leader"),

    tc("Đặt lịch đổi LOA", "SEC-002", "Normal",
       "Chi tiết đặt lịch hiển thị channel info của LOA mới dạng masked, không lộ full secret",
       RES,
       "1. Vào màn đã đặt lịch\n"
       "2. Quan sát giá trị Channel ID và Channel secret của LOA mới\n"
       "3. Mở DevTools Network, xem response của request lấy chi tiết đặt lịch\n"
       "4. Tìm chuỗi secret đầy đủ trong response body",
       "Channel secret thật 32 ký tự (đã ghi lại khi nhập)",
       "- Trên màn: Channel secret hiển thị dạng MASKED\n"
       "- Response body KHÔNG chứa channel secret đầy đủ dạng plaintext\n"
       "- Channel ID có thể hiển thị (không phải bí mật) nhưng secret thì phải mask",
       note="Nguồn: TC-CBF-101 (SEC-002, TD EP-11 'Mask sensitive data (channel secret)'; Pass dev). "
            "SEC-002 BẮT BUỘC khi chức năng xử lý credential. Evidence: ảnh màn + ảnh response body."),

    tc("Đặt lịch đổi LOA", "PERM-003", "Abnormal",
       "Channel ID trùng tenant khác cũng bị chặn khi tạo ĐẶT LỊCH (không chỉ khi đổi ngay)",
       NEW + "\n- Biết Channel ID của bot đang hoạt động thuộc tenant khác",
       "1. Chọn option 2 (đặt lịch) ở màn chọn phương thức\n"
       "2. Nhập Messaging API Channel ID = Channel ID của bot tenant khác\n"
       "3. Nhập 3 field còn lại, bấm đi tiếp\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Query DB schedule_change_bots",
       "Channel ID của bot tenant khác (bots.is_delete = 0)",
       "- Bị chặn với thông báo lỗi giống nhánh đổi ngay "
       "(「このLINE公式アカウントは、すでにL Messageに接続されています。…」)\n"
       "- DB schedule_change_bots: KHÔNG tạo bản ghi mới\n"
       "- Validate được áp dụng ở CẢ nhánh đặt lịch, không chỉ nhánh đổi ngay",
       note="Nguồn: TC-CBF-100 (PERM-003, TD EP-08 Server Validation kế thừa EP-04; Blocked cả 2 env). "
            "⚠️ RISK: đây là nhánh dễ bị lọt khi dev chỉ thêm validate ở luồng đổi ngay. "
            "PERM-003 BẮT BUỘC với change bot. Evidence: ảnh thông báo lỗi + query DB."),

    tc("Đặt lịch đổi LOA", "REG-RUN-001", "Normal",
       "Đặt lịch tạo TRƯỚC một đợt release vẫn hiển thị và dùng được SAU release",
       RES + "\n- Đã tạo đặt lịch TRƯỚC thời điểm release\n- Đã có 1 đợt release lên môi trường test",
       "1. Tạo đặt lịch đổi LOA trước release, ghi lại toàn bộ nội dung bản ghi DB\n"
       "2. Chờ đợt release được deploy\n"
       "3. Sau release, vào lại màn đổi LOA của bot đó\n"
       "4. Đối chiếu thông tin hiển thị với nội dung đã ghi\n"
       "5. Bấm nút thực hiện đổi LOA và kiểm tra flow chạy được",
       "Bản ghi đặt lịch tạo trước release",
       "- Sau release: vẫn hiển thị đúng màn đã đặt lịch\n"
       "- Thông tin LOA mới hiển thị KHỚP nội dung trước release\n"
       "- Bấm thực hiện đổi LOA: flow chạy bình thường, không lỗi 500 / không mất dữ liệu\n"
       "- Không phải đặt lịch lại",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-115 (REG-RUN-001; Blocked cả 2 env — 'bổ trợ cho check tương tự ở tầng job'). "
            "REG-RUN-001 BẮT BUỘC với mọi release khi hệ thống có job/dữ liệu đang chạy dở. RULE-08. "
            "Evidence: query DB trước/sau release + ảnh màn sau release."),
]
