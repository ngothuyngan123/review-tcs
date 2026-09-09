# -*- coding: utf-8 -*-
"""FA-015 — Nhóm 4: Màn danh sách câu trả lời · Export CSV · Bộ đếm 回答人数 · Ghi giá trị.

Nguồn chính:
- 10.2 /「Improve count phía web」(06/2025) r3-r142 — quy tắc cộng/trừ/giữ nguyên count.
- 10.2 /「test fix bug」khối Bug tự detect #38591 (07/2026) r313-r498 — count khi add/update/xóa
  ở màn my_page và right bar chat 1:1 + RV-01..RV-16 (AI Review bổ sung, chỉ có tiêu đề + các bước).
- 10.2 /「test fix bug」khối 2024-08 r3-r31, r100-r142 — set/update/xóa value và xóa bạn bè.
- 10.2 /「test fix bug」khối Bug tự detect #38727 (07/2026) r575-r586 — lịch sử khi info đã bị xóa.
"""
from _common import tc

FIELDS15 = ("15 trường: tên hệ thống · số điện thoại · email · ngày sinh · 郵便番号 · 都道府県名 · "
            "市区町村名 · 町名/番地 · 建物名・部屋番号 · text · select · point · date · ảnh · pdf")
MYPAGE = "màn 友だち詳細 /basic/friendlist/my_page/{id} → tab 基本情報 → 友だち情報"
RIGHTBAR = "right bar màn chat 1:1 /basic/chat-v3 → tab 友だち情報"

S4 = [
    # ══════════════════ Màn danh sách câu trả lời ══════════════════
    tc("Màn danh sách câu trả lời", "UI-001", "Normal",
       "Click 回答人数 → mở màn 情報一覧 với tiêu đề và 2 cột 友だち名 / 情報",
       "- Trường「予約プラン」kiểu 選択肢 có 3 bạn có giá trị\n- Đăng nhập admin bot A",
       "1. Ở màn list click số「3人」của trường\n2. Quan sát URL, tiêu đề, cấu trúc bảng\n3. Chụp màn hình",
       "3 bạn có giá trị",
       "- URL /basic/friend-information/item/{id}, tiêu đề「情報一覧」\n"
       "- Hiển thị tên trường đang xem\n- Bảng có 2 cột「友だち名」và「情報」, liệt kê đủ 3 bạn\n"
       "- Cột 情報 hiển thị đúng giá trị của từng bạn",
       note="Evidence: ảnh chụp. Nguồn: spec ui-spec.md:243 + corpus r115."),

    tc("Màn danh sách câu trả lời", "FUNC-001", "Normal",
       "Click tên bạn ở màn 情報一覧 → điều hướng sang màn 友だち詳細 đúng bạn đó",
       "- Màn 情報一覧 của 1 trường đang mở, có ≥ 3 bạn",
       "1. Ghi lại tên bạn ở dòng thứ 2\n2. Click vào tên bạn đó\n3. Đối chiếu màn vừa mở",
       "Bạn ở dòng thứ 2",
       "- Mở màn 友だち詳細 (/basic/friendlist/my_page/{id}) đúng bạn đã click\n"
       "- Màn đó hiển thị đúng giá trị của trường đang xem",
       note="Nguồn: spec ui-spec.md §SCR-FRI-08/09 + feature-spec §8 (link sang FA-013)."),

    tc("Màn danh sách câu trả lời", "UI-002", "Normal",
       "Giá trị kiểu 年月日 hiển thị đúng định dạng ngày ở màn 情報一覧",
       "- Trường 年月日 có 2 bạn với giá trị 2026-09-10 và 2024-02-29",
       "1. Mở màn 情報一覧 của trường\n2. Đọc cột「情報」của 2 bạn",
       "2026-09-10 và 2024-02-29",
       "- Hiển thị đúng định dạng YYYY-MM-DD cho cả 2 bạn\n- Không hiển thị timestamp hay định dạng khác",
       note="Nguồn: spec ui-spec.md:243."),

    tc("Màn danh sách câu trả lời", "LIST-001", "Boundary",
       "Trường có 0 bạn có giá trị (回答人数 = 0人) → màn 情報一覧 hiển thị rỗng, không lỗi",
       "- Trường mới tạo chưa có bạn nào có giá trị",
       "1. Ở màn list, click số「0人」(hoặc mở thẳng URL màn 情報一覧)\n"
       "2. Quan sát bảng và Console DevTools",
       "0 bạn",
       "- Màn mở được, bảng rỗng (chỉ header), có thông báo trống nếu có thiết kế\n"
       "- Không văng lỗi, Console không có lỗi JS",
       note="Empty state — TC do AI bổ sung theo LIST-001."),

    tc("Màn danh sách câu trả lời", "DATA-COUNT-001", "Normal",
       "Số dòng ở màn 情報一覧 khớp đúng con số 回答人数 ở màn list",
       "- Trường có 5 bạn có giá trị",
       "1. Đọc 回答人数 ở màn list\n2. Mở màn 情報一覧, đếm số dòng\n"
       "3. Xóa giá trị của 1 bạn từ màn 友だち詳細\n4. Lặp lại bước 1-2",
       "5 bạn → xóa 1 → còn 4",
       "- Lần 1: 回答人数 =「5人」, màn 情報一覧 có 5 dòng\n"
       "- Lần 2: 回答人数 =「4人」, màn 情報一覧 có 4 dòng và KHÔNG còn bạn vừa xóa",
       note="RULE-07 (khớp 2 màn). Nguồn: r403, RV-16 (r491)."),

    tc("Màn danh sách câu trả lời", "BULK-001", "Normal",
       "Chọn nhiều bạn → 一括削除 giá trị: giá trị bị xóa, 回答人数 giảm đúng số lượng",
       "- Trường「予約プラン」có 5 bạn có giá trị",
       "1. Ghi 回答人数 = 5人\n2. Ở màn 情報一覧 tick chọn 3 bạn → click「一括削除」→ xác nhận\n"
       "3. Đọc lại bảng và 回答人数 ở màn list\n"
       "4. Mở 友だち詳細 của 1 bạn vừa xóa và 1 bạn còn lại",
       "Xóa giá trị của 3/5 bạn",
       "- Màn 情報一覧 còn 2 dòng\n- 回答人数 =「2人」\n"
       "- 友だち詳細 của bạn vừa xóa không còn giá trị trường này; bạn còn lại vẫn giữ giá trị",
       note="Spec EP-11. Nguồn: r403 + spec feature-spec §SCR-FRI-08/09."),

    tc("Màn danh sách câu trả lời", "BULK-001", "Boundary",
       "一括削除 TẤT CẢ bạn → 回答人数 về 0人, màn 情報一覧 rỗng, count không âm",
       "- Trường có 4 bạn có giá trị",
       "1. Tick chọn tất cả 4 bạn → xóa\n2. Đọc 回答人数 ở màn list\n"
       "3. Mở lại màn 情報一覧\n4. Thử bấm xóa lần nữa khi bảng đã rỗng",
       "Xóa 4/4 bạn",
       "- 回答人数 =「0人」, KHÔNG hiển thị số âm\n- Màn 情報一覧 rỗng, không lỗi\n"
       "- Bấm xóa khi rỗng không gây lỗi",
       note="Tương ứng RV-08 (r483 — guard count không âm). Nguồn: RV-08 + AI viết expected (TC gốc chỉ có tiêu đề)."),

    tc("Màn danh sách câu trả lời", "DATA-REF-001", "Normal",
       "Xóa giá trị trường 年月日 từ màn 情報一覧 → lịch gửi của bạn đó bị dọn",
       "- Trường 年月日 có action, bạn U1 đã sinh lịch gửi trong tương lai\n- Bạn U2 cũng có lịch (đối chứng)",
       "1. Ở màn 情報一覧 xóa giá trị của U1\n2. Chờ qua mốc gửi cũ của U1, kiểm tra LINE app U1\n"
       "3. Chờ mốc của U2, kiểm tra LINE app U2",
       "U1 bị xóa giá trị · U2 giữ nguyên",
       "- U1 KHÔNG nhận action\n- U2 VẪN nhận action đúng giờ\n- 回答人数 giảm 1",
       env="PRODUCTION",
       note="Spec EP-11 (custom id → xóa event_step_time type=3). RULE-08 job → PRODUCTION."),

    tc("Màn danh sách câu trả lời", "PERF-LARGE-001", "Boundary",
       "Trường có số bạn lớn (≥ 1000) → màn 情報一覧 load được, thao tác chọn/xóa vẫn đúng",
       "- Trường có ≥ 1000 bạn có giá trị (bot production)",
       "1. Mở màn 情報一覧, đo thời gian load\n2. Kiểm tra có phân trang không, cuộn tới cuối\n"
       "3. Chọn 50 bạn → xóa\n4. Đọc lại 回答人数",
       "≥ 1000 bạn, xóa 50",
       "- Màn load xong không timeout\n- Phân trang (nếu có) chuyển trang đúng\n"
       "- Sau khi xóa 50: 回答人数 giảm đúng 50",
       env="PRODUCTION",
       note="Spec Gap #5 (pagination chưa xác nhận). TC do AI bổ sung theo PERF-LARGE-001."),

    tc("Màn danh sách câu trả lời", "SEC-001", "Abnormal",
       "Mở màn 情報一覧 bằng id trường của bot khác → không xem được dữ liệu bạn bè của bot đó",
       "- Tài khoản admin bot A, biết id trường của bot B",
       "1. Đăng nhập bot A\n2. Mở URL /basic/friend-information/item/{id bot B}\n3. Quan sát kết quả",
       "id trường bot B",
       "- Không hiển thị danh sách bạn của bot B (báo không tìm thấy / không có quyền)\n"
       "- Không rò rỉ tên bạn bè của bot B",
       note="TC do AI bổ sung theo SEC-001 (tương ứng RV-14). Cần Leader xác nhận."),

    # ══════════════════ Export CSV ══════════════════
    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV từ màn 情報一覧 → tải được file, nội dung khớp danh sách trên màn",
       "- Trường「予約プラン」có 5 bạn có giá trị (tên bạn gồm cả ký tự JP)",
       "1. Ở màn 情報一覧 click「CSV書き出し」\n2. Tải file về\n3. Mở file bằng Excel và bằng editor UTF-8\n"
       "4. Đối chiếu từng dòng với bảng trên màn",
       "5 bạn, có tên JP full-width",
       "- File CSV tải về thành công\n- Có đủ 5 dòng dữ liệu + dòng header\n"
       "- Tên bạn và giá trị khớp 100% với bảng trên màn, không lỗi font khi mở bằng Excel",
       env="PRODUCTION",
       note="RULE-06 (đi tới file tải về). Spec EP-13/EP-14. Spec Gap #9 ghi 'format CSV chưa đọc chi tiết' → "
            "TC này lấp Gap. TC do AI bổ sung (corpus không có TC export riêng cho màn này)."),

    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV khi CHỌN một số bạn → file chỉ chứa các bạn đã chọn",
       "- Trường có 5 bạn có giá trị",
       "1. Tick chọn 2 bạn\n2. Click「CSV書き出し」\n3. Tải và mở file",
       "Chọn 2/5 bạn",
       "- File chỉ có 2 dòng dữ liệu, đúng 2 bạn đã chọn\n- Không chứa 3 bạn còn lại",
       env="PRODUCTION",
       note="Spec EP-13 có param lineIds optional. TC do AI bổ sung, cần Leader xác nhận UI có cho chọn không."),

    tc("Export CSV", "OUT-EXPORT-001", "Boundary",
       "Export CSV khi trường có 0 bạn → file rỗng (chỉ header), không lỗi",
       "- Trường chưa có bạn nào có giá trị",
       "1. Mở màn 情報一覧\n2. Click「CSV書き出し」\n3. Tải và mở file",
       "0 bạn",
       "- Tải được file, chỉ có dòng header, không có dòng dữ liệu\n- Không văng lỗi hệ thống",
       env="PRODUCTION",
       note="TC do AI bổ sung theo OUT-EXPORT-001."),

    tc("Export CSV", "DATA-TEXT-001", "Boundary",
       "Export CSV với giá trị chứa dấu phẩy / xuống dòng / dấu nháy → file không vỡ cột",
       "- Trường kiểu 記述, 3 bạn có giá trị đặc biệt",
       "1. Gán giá trị đặc biệt cho 3 bạn\n2. Export CSV\n3. Mở file bằng Excel, kiểm tra số cột từng dòng",
       "Bạn 1:「a,b,c」· Bạn 2: text 2 dòng · Bạn 3:「\"quote\"」",
       "- File mở đúng 2 cột cho cả 3 dòng, không bị tách nhầm cột\n"
       "- Nội dung giữ nguyên dấu phẩy, xuống dòng, dấu nháy",
       env="PRODUCTION",
       note="TC do AI bổ sung theo DATA-TEXT-001/OUT-EXPORT-001."),

    tc("Export CSV", "PERF-LARGE-001", "Boundary",
       "Export CSV cho trường có ≥ 1000 bạn → file đủ dòng, không timeout",
       "- Trường có ≥ 1000 bạn có giá trị (bot production)",
       "1. Click「CSV書き出し」và đo thời gian tới khi file sẵn sàng\n2. Tải file, đếm số dòng\n"
       "3. Đối chiếu với 回答人数",
       "≥ 1000 bạn",
       "- Export xong không timeout/không lỗi\n- Số dòng dữ liệu = 回答人数\n"
       "- Dòng đầu và dòng cuối đọc được đúng",
       env="PRODUCTION",
       note="RULE-08 (dữ liệu lớn → PRODUCTION). TC do AI bổ sung."),

    # ══════════════════ Bộ đếm 回答人数 ══════════════════
    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "THÊM MỚI giá trị từ màn 友だち詳細 → 回答人数 +1 (đủ 15 trường)",
       "- Bot A có đủ 15 trường (4 mặc định + 5 địa chỉ + 6 kiểu tự tạo)\n"
       "- Bạn U1 CHƯA có giá trị ở trường nào\n- Ghi lại 回答人数 ban đầu của 15 trường",
       "1. Mở " + MYPAGE + "\n2. Thêm mới giá trị cho từng trường, mỗi lần lưu 1 trường\n"
       "3. Sau mỗi lần: đọc 回答人数 ở màn list, đọc lịch sử ở 友だち詳細, mở " + RIGHTBAR,
       FIELDS15 + "\n(15 lượt thêm mới, mỗi trường U1 chưa có giá trị)",
       "- Mỗi trường: 回答人数 tăng đúng +1 so với ban đầu\n"
       "- 友だち詳細 ghi lịch sử thêm mới và hiển thị đúng giá trị\n"
       "- Right bar chat 1:1 hiển thị đúng giá trị vừa thêm\n"
       "- Click vào 回答人数 thấy U1 trong danh sách",
       note="15 trường cùng 1 kết quả nên gộp 1 TC (liệt kê đủ ở Dữ liệu test). "
            "Bug tự detect #38591 (07/2026 — trước fix count không +1 khi thêm ở my_page). Nguồn: r313-r327."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "THÊM MỚI giá trị từ right bar chat 1:1 → 回答人数 +1 (đủ 15 trường)",
       "- Như TC trên, bạn U2 chưa có giá trị ở 15 trường",
       "1. Mở " + RIGHTBAR + " của U2\n2. Thêm mới giá trị cho từng trường\n"
       "3. Sau mỗi lần: đọc 回答人数 ở màn list và kiểm tra " + MYPAGE,
       FIELDS15 + "\n(15 lượt thêm mới qua right bar chat 1:1)",
       "- Mỗi trường: 回答人数 tăng đúng +1\n"
       "- 友だち詳細 hiển thị đúng giá trị và ghi lịch sử\n- Right bar hiển thị đúng giá trị",
       note="Nguồn: r328-r342 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "CẬP NHẬT giá trị đã có (1 lần và 3 lần liên tiếp) → 回答人数 GIỮ NGUYÊN",
       "- Bạn U1 ĐÃ có giá trị ở đủ 15 trường\n- Ghi lại 回答人数 của 15 trường",
       "1. Ở " + MYPAGE + " cập nhật giá trị của từng trường 1 lần → đọc 回答人数\n"
       "2. Cập nhật tiếp 3 lần liên tiếp cho từng trường → đọc 回答人数\n"
       "3. Lặp lại toàn bộ ở " + RIGHTBAR,
       FIELDS15 + "\n2 lối vào × 15 trường × {1 lần, 3 lần} = 60 lượt",
       "- 回答人数 KHÔNG đổi ở mọi lượt cập nhật\n"
       "- 友だち詳細 ghi lịch sử cập nhật, hiển thị giá trị mới nhất\n"
       "- Right bar chat 1:1 hiển thị giá trị mới nhất",
       note="60 dòng corpus cùng 1 kết quả nên gộp 1 TC. Nguồn: r343-r402 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "XÓA giá trị đã có → 回答人数 -1 và bạn biến mất khỏi danh sách câu trả lời (đủ 15 trường, 2 lối vào)",
       "- Bạn U1 ĐÃ có giá trị ở đủ 15 trường",
       "1. Ở " + MYPAGE + " xóa trắng giá trị từng trường → lưu\n"
       "2. Sau mỗi lần: đọc 回答人数, click vào 回答人数 kiểm tra danh sách bạn\n"
       "3. Lặp lại ở " + RIGHTBAR + " với bạn U2",
       FIELDS15 + "\n2 lối vào × 15 trường",
       "- Mỗi trường: 回答人数 giảm đúng 1\n"
       "- Click 回答人数 KHÔNG còn thấy bạn vừa xóa\n"
       "- 友だち詳細 ghi lịch sử xóa; right bar không còn hiển thị giá trị",
       note="Nguồn: r403, r405, r407-r431 và r433-r461 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Xóa giá trị rồi THÊM LẠI → 回答人数 +1 trở lại (không bị lệch)",
       "- Bạn U1 đã có giá trị ở 15 trường",
       "1. Xóa giá trị 1 trường → đọc 回答人数\n2. Thêm lại giá trị mới cho trường đó → đọc 回答人数\n"
       "3. Lặp cho đủ 15 trường, ở cả 2 lối vào (友だち詳細 và right bar)",
       FIELDS15 + "\n2 lối vào × 15 trường × (xóa → thêm lại)",
       "- Sau xóa: 回答人数 giảm 1\n- Sau thêm lại: 回答人数 tăng 1, quay đúng giá trị ban đầu\n"
       "- Danh sách câu trả lời có lại bạn đó, hiển thị giá trị mới",
       note="Nguồn: r404, r406, r408-r432, r462 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Xóa giá trị rồi cập nhật lại data → count và hiển thị khớp ở màn detail count",
       "- Bạn U1 vừa bị xóa giá trị ở các trường mặc định và trường tự tạo",
       "1. Ở " + RIGHTBAR + " thêm lại giá trị cho nhóm trường mặc định (tên hệ thống, email, "
       "phone, ngày sinh, 5 trường địa chỉ)\n"
       "2. Ở " + MYPAGE + " thêm lại giá trị cho nhóm trường tự tạo (text, point, select, date, image, pdf)\n"
       "3. Sau mỗi nhóm: đọc 回答人数 và mở màn danh sách câu trả lời",
       "Nhóm mặc định 9 trường · nhóm tự tạo 6 trường",
       "- 回答人数 của từng trường tăng đúng 1\n"
       "- Màn danh sách câu trả lời hiển thị đúng bạn + đúng giá trị vừa thêm\n"
       "- 友だち詳細 ghi lịch sử thêm mới, right bar hiển thị đúng",
       note="Nguồn: r492-r495 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Ghi giá trị qua JOB (form / QR / kịch bản) sau khi xóa → count và detail count đều đúng",
       "- Có form map friend info, QR landing set param địa chỉ, kịch bản có action gán friend info\n"
       "- Bạn U1 vừa bị xóa giá trị ở các trường liên quan",
       "1. U1 trả lời form (map tên hệ thống, email, phone, ngày sinh)\n"
       "2. U1 quét QR landing có param 5 trường địa chỉ\n"
       "3. U1 nhận kịch bản có action gán 6 trường tự tạo\n"
       "4. Sau mỗi bước: đọc 回答人数 và mở màn danh sách câu trả lời",
       "Form: 4 trường · QR: 5 trường địa chỉ · Kịch bản: text, point, select, date, image, pdf",
       "- 回答人数 của mỗi trường tăng đúng 1\n"
       "- Màn danh sách câu trả lời hiển thị U1 với đúng giá trị\n"
       "- 友だち詳細 ghi lịch sử; right bar hiển thị đúng",
       note="Nguồn: r496-r498 (#38591 — khối JOB)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Thêm giá trị qua tính năng khác → 回答人数 +1 (action friendlist, form, QR param, booking event)",
       "- Bạn U1 chưa có giá trị ở trường I1",
       "1. Ghi 回答人数 ban đầu\n2. Lần lượt thực hiện 4 cách ghi giá trị, mỗi lần với 1 bạn mới:\n"
       "   (a) action ở màn danh sách bạn bè\n   (b) bạn trả lời form có map friend info\n"
       "   (c) import param của QR landing\n   (d) bạn trả lời form khi booking event\n"
       "3. Sau mỗi cách: đọc 回答人数 và kiểm tra 友だち詳細 + right bar",
       "4 cách ghi giá trị, mỗi cách 1 bạn",
       "- Mỗi cách: 回答人数 tăng đúng +1\n"
       "- 友だち詳細 ghi lịch sử thêm mới, hiển thị đúng giá trị\n- Right bar hiển thị đúng",
       note="Nguồn: r463-r466 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "GHI ĐÈ giá trị qua action QR landing (bạn đã có giá trị) → 回答人数 giữ nguyên",
       "- Bạn U1 ĐÃ có giá trị ở trường I1",
       "1. Ghi 回答人数\n2. U1 quét QR landing có action ghi đè giá trị I1\n"
       "3. Đọc 回答人数, giá trị ở 友だち詳細 và lịch sử",
       "U1 đã có giá trị, action ghi đè giá trị mới",
       "- 回答人数 KHÔNG đổi\n- Giá trị ở 友だち詳細 và right bar là giá trị mới\n"
       "- Lịch sử ghi nhận cập nhật (không phải thêm mới)",
       note="Nguồn: r467 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "XÓA giá trị qua tính năng khác → 回答人数 -1 (action salon, import CSV, form khi booking item)",
       "- Bạn U1, U2, U3 đều đang có giá trị ở trường I1",
       "1. Ghi 回答人数 ban đầu\n2. Lần lượt xóa giá trị bằng 3 cách:\n"
       "   (a) action của salon\n   (b) import CSV có giá trị rỗng\n"
       "   (c) bạn trả lời form khi booking item ghi giá trị rỗng\n"
       "3. Sau mỗi cách: đọc 回答人数, kiểm tra 友だち詳細 và right bar",
       "3 cách xóa, mỗi cách 1 bạn",
       "- Mỗi cách: 回答人数 giảm đúng 1\n"
       "- 友だち詳細 ghi lịch sử xóa, không còn hiển thị giá trị\n- Right bar không còn giá trị",
       note="Nguồn: r468-r470 (#38591)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Xóa/thêm giá trị hàng loạt cho nhiều trường cùng lúc → count từng trường đúng",
       "- Bạn U1 có giá trị ở 6 trường tự tạo (text, point, select, date, image, pdf)",
       "1. Ghi 回答人数 của 6 trường\n2. Xóa giá trị cả 6 trường trong 1 lần lưu ở 友だち詳細\n"
       "3. Đọc lại 6 con số\n4. Thêm lại giá trị cả 6 trường trong 1 lần lưu\n5. Đọc lại 6 con số",
       "6 trường xóa/thêm cùng lượt lưu",
       "- Sau xóa: cả 6 trường giảm đúng 1\n- Sau thêm lại: cả 6 trường tăng đúng 1 về giá trị ban đầu\n"
       "- Không trường nào bị lệch/đếm 2 lần",
       note="Nguồn: r471-r474 (#38591 — 'Xóa/Add value các info khác: text, point, select, date, image, pdf')."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Thêm / cập nhật / xóa giá trị từ màn chat 1:1 và màn danh sách bạn bè → count tăng / giữ / giảm đúng",
       "- Bạn U1 chưa có giá trị ở 5 trường mặc định + các trường tự tạo",
       "1. Ở màn chat 1:1: thêm giá trị → đọc count; cập nhật → đọc count; xóa → đọc count\n"
       "2. Lặp lại bằng action ở màn chat 1:1\n3. Lặp lại bằng action ở màn danh sách bạn bè",
       "3 lối vào × {thêm, cập nhật, xóa} × các trường: tên, mail, số điện thoại, ngày sinh, "
       "địa chỉ 都道府県名, và các trường tự tạo",
       "- Thêm mới: count +1\n- Cập nhật: count không đổi\n- Xóa: count -1\n"
       "- Áp dụng đồng nhất cho cả 3 lối vào và mọi trường",
       note="Nguồn: tab「Improve count phía web」r3-r56 (06/2025)."),

    tc("Bộ đếm 回答人数", "SYNC-APP-001", "Normal",
       "Thêm / cập nhật / xóa giá trị từ APP MOBILE (màn my page) → count tăng / giữ / giảm đúng",
       "- Có app mobile đăng nhập cùng bot A\n- Bạn U1 chưa có giá trị",
       "1. Trên app mobile mở màn my page của U1\n2. Thêm giá trị cho các trường → đọc count trên web\n"
       "3. Cập nhật giá trị → đọc count\n4. Xóa giá trị → đọc count\n"
       "5. Đối chiếu giá trị hiển thị giữa app và web",
       "Trường mặc định (tên, mail, số điện thoại, ngày sinh, địa chỉ) và trường tự tạo",
       "- Thêm: count +1 · Cập nhật: count không đổi · Xóa: count -1\n"
       "- Giá trị hiển thị trên app và trên web khớp nhau\n- 友だち詳細 web ghi đủ lịch sử",
       env="PRODUCTION",
       note="Tương ứng RV-07 (r482 — path mobile không dùng service đã fix). "
            "Nguồn: tab「Improve count phía web」r75-r92 + r26-r30 (khối 2024-08 từng ghi NG cho app)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Bạn trả lời form (item radio / dropdown / chẩn đoán) có map friend info → count theo đúng quy tắc",
       "- Form có item radio map trường friend info tự tạo và item chẩn đoán map friend info",
       "1. Bạn U1 trả lời form CÓ chọn câu trả lời (lần đầu) → đọc count\n"
       "2. U1 trả lời lại form, chọn câu khác (cập nhật giá trị) → đọc count\n"
       "3. Bạn U2 trả lời form KHÔNG nhập câu trả lời đó → đọc count",
       "Item radio + item chẩn đoán · 3 kịch bản",
       "- Lần 1 (thêm mới): count +1\n- Lần 2 (cập nhật): count không đổi\n"
       "- U2 không trả lời: count KHÔNG đổi (không tạo giá trị rỗng)",
       note="Nguồn: tab「Improve count phía web」r95-r100."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Booking salon / lesson có form map friend info (user book, admin book, admin sửa) → count đúng quy tắc",
       "- Salon và lesson có form nhập map trường friend info kiểu radio",
       "1. Bạn tự book CÓ chọn câu trả lời → đọc count; book lại đổi câu trả lời → đọc count\n"
       "2. Bạn book KHÔNG nhập câu trả lời → đọc count\n"
       "3. Admin book hộ (web) có/không nhập câu trả lời → đọc count\n"
       "4. Admin sửa thông tin trong modal chi tiết booking: thêm / cập nhật / xóa giá trị → đọc count\n"
       "5. Lặp toàn bộ cho cả salon và lesson",
       "2 tính năng (salon, lesson) × {user book, admin book, admin sửa} × {thêm, cập nhật, không nhập, xóa}",
       "- Thêm mới giá trị: count +1\n- Cập nhật: count không đổi\n- Không nhập: count không đổi\n"
       "- Admin xóa giá trị trong modal: count -1",
       note="Nguồn: tab「Improve count phía web」r101-r124."),

    tc("Bộ đếm 回答人数", "SYNC-APP-001", "Normal",
       "Admin book hộ trên APP MOBILE cho salon/lesson có map friend info → count đúng",
       "- App mobile admin, salon và lesson có form map friend info",
       "1. Trên app admin book hộ CÓ nhập câu trả lời → đọc count trên web\n"
       "2. Book lại đổi câu trả lời → đọc count\n3. Book KHÔNG nhập câu trả lời → đọc count",
       "App mobile × salon + lesson",
       "- Thêm mới: count +1 · Cập nhật: count không đổi · Không nhập: count không đổi\n"
       "- Giá trị hiển thị trên web khớp nội dung nhập trên app",
       env="PRODUCTION",
       note="⚠️ Corpus r107-r109, r119-r121 KHÔNG có kết quả mong đợi (chỉ có tiêu đề) → expected do AI viết "
            "theo quy tắc chung của tab, cần Leader xác nhận."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Abnormal",
       "Đổi bot (change bot) → toàn bộ 回答人数 của bot đó về 0, bot khác không bị đụng",
       "- Bot A có nhiều trường friend info với count > 0\n- Bot B (bot khác) cũng có count > 0",
       "1. Ghi lại count của tất cả trường ở bot A và bot B\n2. Thực hiện change bot cho bot A\n"
       "3. Mở màn friend information của bot A đọc count từng trường\n"
       "4. Mở bot B đọc count từng trường",
       "Trường bot A: name, email, ngày sinh, số điện thoại, 都道府県名, 4 địa chỉ còn lại, "
       "text, select, point, ngày, ảnh, pdf",
       "- Toàn bộ count của bot A hiển thị「0人」\n"
       "- Count của bot B GIỮ NGUYÊN, không bị reset",
       env="PRODUCTION",
       note="⚠️ Spec KHÔNG ghi hành vi reset count khi change bot — xem MT-14. "
            "Nguồn: tab「Improve count phía web」r125-r136."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Abnormal",
       "Account staff thực hiện change bot → count cũng về 0 như admin",
       "- Account staff có quyền change bot, bot A có count > 0",
       "1. Đăng nhập staff, thực hiện change bot cho bot A\n2. Đọc count các trường friend info\n"
       "3. Kiểm tra bot khác",
       "Staff change bot",
       "- Toàn bộ count của bot A =「0人」\n- Bot khác không bị ảnh hưởng",
       env="PRODUCTION",
       note="Nguồn: tab「Improve count phía web」r137."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Boundary",
       "回答人数 đang = 0 nhưng bạn vẫn còn giá trị sót → xóa giá trị KHÔNG làm count âm",
       "- Trường I1 có 回答人数 hiển thị「0人」nhưng bạn U1 vẫn còn giá trị (dữ liệu lệch)",
       "1. Ghi lại 回答人数 =「0人」\n2. Ở 友だち詳細 của U1 xóa trắng giá trị trường I1 → lưu\n"
       "3. Đọc lại 回答人数 ở màn list\n4. Mở màn danh sách câu trả lời",
       "Count = 0, còn 1 bạn có giá trị",
       "- 回答人数 vẫn hiển thị「0人」, KHÔNG hiển thị số âm (-1)\n"
       "- Màn danh sách câu trả lời không còn U1\n- Màn list không văng lỗi",
       note="Tương ứng RV-08 (r483) — TC gốc chỉ có tiêu đề + các bước, KHÔNG có kết quả mong đợi; expected do AI viết."),

    tc("Bộ đếm 回答人数", "DATA-001", "Boundary",
       "Lưu giá trị null vs chuỗi rỗng → cả hai đều xóa giá trị và giảm count như nhau",
       "- Bạn U1 và U2 đều đang có giá trị ở trường I1, 回答人数 = 2人",
       "1. U1: xóa trắng ô nhập (chuỗi rỗng) → lưu → đọc count\n"
       "2. U2: lưu với giá trị null (qua API/thao tác xóa của app) → đọc count\n"
       "3. Mở màn danh sách câu trả lời",
       "U1 = chuỗi rỗng · U2 = null",
       "- Cả 2 lượt đều làm 回答人数 giảm 1 (2人 → 1人 → 0人)\n"
       "- Cả U1 và U2 đều không còn trong danh sách câu trả lời\n"
       "- Không còn dòng giá trị rỗng nào hiển thị ở 友だち詳細",
       note="Tương ứng RV-09 (r484) — TC gốc chỉ có tiêu đề; expected do AI viết. Cần Leader xác nhận."),

    tc("Bộ đếm 回答人数", "DATA-001", "Boundary",
       "Bạn CHƯA có giá trị mà lưu rỗng → không tạo dòng giá trị, count giữ 0",
       "- Trường I1 có 回答人数 =「0人」\n- Bạn U1 chưa có giá trị",
       "1. Ở 友だち詳細 của U1, để trống ô nhập của I1 → bấm lưu\n"
       "2. Đọc 回答人数\n3. Mở màn danh sách câu trả lời\n4. Mở right bar chat 1:1 của U1",
       "Lưu rỗng khi chưa có giá trị",
       "- 回答人数 vẫn「0人」\n- Màn danh sách câu trả lời rỗng (không xuất hiện U1 với giá trị trống)\n"
       "- Right bar không hiển thị dòng giá trị rỗng",
       note="Tương ứng RV-10 (r485) — TC gốc chỉ có tiêu đề; expected do AI viết."),

    tc("Bộ đếm 回答人数", "CONC-001", "Abnormal",
       "Double-click nút lưu khi xóa giá trị → count chỉ giảm 1 lần, không âm, không lỗi",
       "- Bạn U1 có giá trị ở trường I1, 回答人数 = 5人",
       "1. Ở 友だち詳細 của U1 xóa trắng giá trị\n2. Double-click nhanh nút lưu\n"
       "3. Reload và đọc 回答人数\n4. Mở màn danh sách câu trả lời",
       "Double-click trong < 1 giây",
       "- 回答人数 =「4人」(giảm đúng 1 lần)\n- Không hiển thị số âm, không văng lỗi\n"
       "- U1 không còn trong danh sách câu trả lời",
       note="Tương ứng RV-11 (r486) — TC gốc chỉ có tiêu đề; expected do AI viết."),

    tc("Bộ đếm 回答人数", "CONC-002", "Abnormal",
       "Đa tab: tab A xóa giá trị, tab B (mở trước) lưu lại giá trị cũ → dữ liệu cuối và count nhất quán",
       "- Mở 友だち詳細 của U1 ở 2 tab, U1 đang có giá trị ở I1, 回答人数 = 3人",
       "1. Tab A: xóa trắng giá trị I1 → lưu\n2. Tab B (chưa reload): bấm lưu với giá trị cũ\n"
       "3. Reload cả 2 tab, đọc giá trị của U1\n4. Đọc 回答人数 và màn danh sách câu trả lời",
       "Tab A xóa · Tab B lưu lại giá trị cũ",
       "- Trạng thái cuối cùng nhất quán giữa 2 tab sau reload\n"
       "- 回答人数 khớp với số bạn thực tế đang có giá trị ở màn danh sách câu trả lời\n"
       "- Không bị count lệch (không thừa/thiếu 1)",
       note="Tương ứng RV-12 (r487) — TC gốc chỉ có tiêu đề; expected do AI viết. Cần Leader chốt tab nào thắng."),

    tc("Bộ đếm 回答人数", "SEC-ISO-001", "Abnormal",
       "Xóa giá trị của bạn A / trường X / bot này KHÔNG đụng bạn B, trường Y, bot khác",
       "- Trường X có bạn A và B cùng có giá trị\n- Bạn A còn có giá trị ở trường Y\n"
       "- Bot khác cũng có bạn cùng LINE user id và trường tương tự",
       "1. Ghi lại 回答人数 của X, Y (bot hiện tại) và của trường tương ứng ở bot khác\n"
       "2. Xóa trắng giá trị trường X của bạn A → lưu\n"
       "3. Đọc lại 3 con số và mở màn danh sách câu trả lời của X và Y\n"
       "4. Kiểm tra bạn cùng LINE user id ở bot khác",
       "Bạn A/B, trường X/Y, 2 bot",
       "- Chỉ 回答人数 của X giảm 1; bạn B vẫn còn trong danh sách của X\n"
       "- 回答人数 và giá trị của trường Y không đổi\n"
       "- Bot khác không bị đụng: count và giá trị giữ nguyên",
       note="Tương ứng RV-05 (r480) — TC gốc chỉ có tiêu đề; expected do AI viết. "
            "Cùng hướng với corpus r119 (xóa bạn ở bot A không đụng bot B)."),

    tc("Bộ đếm 回答人数", "DATA-COUNT-001", "Normal",
       "Xóa giá trị của trường thuộc MỌI loại folder (chưa phân loại / 2 folder mặc định / folder tự tạo) → count đều giảm đúng",
       "- Có trường ở「未分類」, folder thông tin cơ bản, folder thông tin địa chỉ và folder admin tự tạo\n"
       "- Bạn U1 có giá trị ở cả 4 nhóm",
       "1. Ghi 回答人数 của 4 trường\n2. Xóa trắng lần lượt giá trị của 4 trường ở 友だち詳細\n"
       "3. Sau mỗi lần đọc 回答人数 và màn danh sách câu trả lời",
       "4 loại folder",
       "- Cả 4 trường: 回答人数 giảm đúng 1\n- U1 không còn trong danh sách câu trả lời của cả 4 trường",
       note="Tương ứng RV-15 (r490) — TC gốc chỉ có tiêu đề; expected do AI viết."),

    tc("Bộ đếm 回答人数", "DATA-001", "Normal",
       "Xóa trắng giá trị → KHÔNG còn dòng dữ liệu nào của trường đó cho bạn (kể cả dòng rỗng)",
       "- Bạn U1 đang có giá trị ở trường I1",
       "1. Ở " + MYPAGE + " xóa trắng ô nhập của I1 → lưu\n"
       "2. Mở lại 友だち詳細 của U1 và quan sát khu vực trường I1\n"
       "3. Mở " + RIGHTBAR + "\n4. Mở màn danh sách câu trả lời của I1\n"
       "5. Export CSV màn đó và kiểm tra file",
       "Xóa trắng 1 trường",
       "- 友だち詳細: trường I1 hiển thị trạng thái chưa có giá trị (không có dòng giá trị rỗng)\n"
       "- Right bar không hiển thị dòng rỗng của I1\n"
       "- Màn danh sách câu trả lời và file CSV KHÔNG chứa U1 với giá trị rỗng\n- 回答人数 giảm 1",
       note="Tương ứng RV-01 (r476 — lõi ticket #38591: sau khi xóa trắng không còn dòng nào, kể cả dòng NULL). "
            "TC gốc chỉ có tiêu đề + các bước, không có kết quả mong đợi → expected do AI viết ở tầng quan sát UI."),

    tc("Bộ đếm 回答人数", "DATA-REF-001", "Abnormal",
       "Bạn bị XÓA khỏi bot → count của trường mà bạn từng có giá trị được cập nhật lại",
       "- Bạn U1 có giá trị ở 3 trường tự tạo, U2 không có giá trị ở trường nào\n"
       "- Ghi lại 回答人数 của 3 trường",
       "1. Xóa bạn U2 (không có giá trị) → đọc lại 3 con số\n"
       "2. Xóa bạn U1 (có 3 giá trị) → đọc lại 3 con số\n"
       "3. Mở màn danh sách câu trả lời của 3 trường",
       "U2 không có giá trị · U1 có 3 giá trị",
       "- Xóa U2: cả 3 回答人数 KHÔNG đổi\n"
       "- Xóa U1: cả 3 回答人数 giảm đúng 1\n- U1 không còn trong danh sách câu trả lời",
       note="Nguồn: r116-r118 (khối 2024-08)."),

    tc("Bộ đếm 回答人数", "DATA-REF-001", "Normal",
       "Xóa bạn ở các màn khác nhau (my_page / danh sách bạn bè: block, bị block, ẩn / app mobile) → count đều cập nhật đúng",
       "- Mỗi nhóm có 2 bạn có giá trị ở ≥ 2 trường tự tạo",
       "1. Xóa 1 bạn ở màn 友だち詳細 → đọc count\n"
       "2. Xóa 1 bạn ở danh sách bạn chặn bot → đọc count\n"
       "3. Xóa 1 bạn ở danh sách bạn bị bot chặn → đọc count\n"
       "4. Xóa 1 bạn ở danh sách bạn ẩn → đọc count\n"
       "5. Xóa 1 bạn trên app mobile → đọc count\n"
       "6. Xóa NHIỀU bạn cùng lúc ở danh sách bạn bè → đọc count",
       "5 lối vào xóa 1 bạn + 1 lối vào xóa nhiều bạn",
       "- Mọi lối vào: xóa bạn thành công\n"
       "- Trường mà bạn có giá trị: 回答人数 giảm đúng số bạn bị xóa\n"
       "- Trường mà bạn KHÔNG có giá trị: count không đổi\n"
       "- Trường mặc định (tên, ngày sinh, số điện thoại, địa chỉ 都道府県名): count không bị cập nhật sai",
       env="PRODUCTION",
       note="6 lối vào cùng quy tắc nên gộp 1 TC. Nguồn: r115-r141 (khối 2024-08)."),

    tc("Bộ đếm 回答人数", "SEC-ISO-001", "Abnormal",
       "Cùng 1 LINE user kết bạn với bot A và bot B → xóa bạn ở bot A không xóa giá trị ở bot B",
       "- LINE user L1 là bạn của cả bot A và bot B, có giá trị friend info ở cả 2 bot",
       "1. Ghi 回答人数 các trường ở bot A và bot B\n2. Xóa bạn L1 ở bot A\n"
       "3. Đọc count ở bot A và bot B\n4. Mở 友だち詳細 của L1 ở bot B",
       "L1 có giá trị ở cả 2 bot",
       "- Bot A: count các trường giảm đúng, L1 không còn\n"
       "- Bot B: count GIỮ NGUYÊN, L1 vẫn còn đủ giá trị friend info",
       note="Nguồn: r119 (khối 2024-08)."),

    tc("Bộ đếm 回答人数", "DATA-AUDIT-001", "Abnormal",
       "Form ghi câu trả lời vào trường đã BỊ XÓA → không ghi lịch sử friend info mồ côi (thiếu 管理名)",
       "- Trường friend info A đã bị xóa\n"
       "- Có form với các loại item từng map tới A: trả lời ngắn, trả lời dài, ngày, chọn 1 option, "
       "upload media, chẩn đoán, tên, email, ngày sinh, số điện thoại, giới tính",
       "1. Bạn U1 trả lời form với từng loại item\n2. Mở 友だち詳細 của U1 xem lịch sử 友だち情報\n"
       "3. Mở right bar chat 1:1 của U1",
       "11 loại item trong form",
       "- KHÔNG xuất hiện dòng lịch sử friend info nào không có 管理名\n"
       "- Không có mục friend info trống/mồ côi ở 友だち詳細 và right bar\n"
       "- Các câu trả lời form vẫn được lưu bình thường ở màn kết quả form",
       note="Bug tự detect #38727 (07/2026). ⚠️ Corpus r576-r586 chỉ có điều kiện tiền đề, KHÔNG có kết quả mong đợi → "
            "expected do AI viết từ tiêu đề bug, cần Leader xác nhận."),

    # ══════════════════ Ghi giá trị từ màn admin ══════════════════
    tc("Ghi giá trị từ màn admin", "FUNC-001", "Normal",
       "Sửa giá trị điểm ở danh sách friend info trong màn chat 1:1: đặt = 0 và ≠ 0 khi bạn CHƯA có giá trị",
       "- Trường ポイント「会員ポイント」\n- Bạn U1 chưa có giá trị điểm",
       "1. Mở " + RIGHTBAR + " của U1\n2. Nhập giá trị 0 → lưu → đọc lại giá trị và 回答人数\n"
       "3. Với bạn U2 (chưa có giá trị): nhập 50 → lưu → đọc lại",
       "U1 = 0 điểm · U2 = 50 điểm",
       "- U1 lưu được giá trị 0 và hiển thị「0」(không hiển thị trống)\n"
       "- U2 hiển thị「50」\n- 回答人数 tăng 1 cho mỗi bạn\n"
       "- Giá trị khớp giữa right bar, 友だち詳細 và màn danh sách câu trả lời",
       note="Bug #26541 (08/2024 — không update point về 0 được). Nguồn: r3-r4."),

    tc("Ghi giá trị từ màn admin", "FUNC-001", "Normal",
       "Cập nhật giá trị điểm đã có: 0 → khác 0, khác 0 → 0, và xóa giá trị",
       "- Bạn U1 đang có điểm = 0, U2 đang có điểm = 50",
       "1. U1: đổi 0 → 100 → lưu → đọc lại\n2. U2: đổi 50 → 0 → lưu → đọc lại\n"
       "3. U2: xóa trắng giá trị → lưu → đọc lại và đọc 回答人数",
       "U1: 0→100 · U2: 50→0 → xóa",
       "- U1 hiển thị「100」\n- U2 hiển thị「0」(không bị hiểu là xóa)\n"
       "- Sau khi xóa trắng: U2 không còn giá trị, 回答人数 giảm 1\n"
       "- 回答人数 không đổi ở 2 bước cập nhật đầu",
       note="Bug #26541. Phân biệt rõ 'giá trị 0' và 'xóa giá trị'. Nguồn: r5-r7."),

    tc("Ghi giá trị từ màn admin", "DATA-001", "Abnormal",
       "Set giá trị friend info nhiều lần từ web → KHÔNG sinh bản ghi trùng lặp cho cùng 1 bạn",
       "- Trường ポイント, bạn U1 chưa có giá trị",
       "1. Ở right bar chat 1:1 set giá trị cho U1\n2. Cập nhật liên tục 5 lần với giá trị khác nhau\n"
       "3. Mở màn danh sách câu trả lời của trường\n4. Đọc 回答人数\n"
       "5. Lọc bạn bè theo điều kiện điểm của trường này",
       "5 lần cập nhật liên tiếp",
       "- Màn danh sách câu trả lời chỉ có ĐÚNG 1 dòng cho U1, giá trị là giá trị cuối cùng\n"
       "- 回答人数 chỉ tăng 1 (không tăng theo số lần cập nhật)\n"
       "- Lọc theo điểm trả về U1 đúng 1 lần",
       note="Bug #26532 (08/2024 — filter theo point không hoạt động do lưu duplicate friend info value). "
            "Nguồn: header khối r2 + r25."),

    tc("Ghi giá trị từ màn admin", "FUNC-MULTI-001", "Normal",
       "Multi action ở màn chat 1:1: set / cộng / trừ / xóa / random điểm cho bạn CHƯA có giá trị",
       "- Trường ポイント, bạn chưa có giá trị điểm",
       "1. Mở multi action ở màn chat 1:1\n2. Thực hiện lần lượt cho các bạn khác nhau:\n"
       "   set 0 · set ≠ 0 · set random · cộng điểm · trừ điểm · xóa điểm\n"
       "3. Sau mỗi lần đọc giá trị ở right bar và 回答人数",
       "6 loại action điểm, mỗi loại 1 bạn chưa có giá trị",
       "- set 0 → hiển thị「0」· set ≠0 → đúng số · set random → nằm trong khoảng\n"
       "- cộng/trừ điểm cho bạn chưa có giá trị: ghi nhận kết quả thực tế theo quy tắc hệ thống\n"
       "- xóa điểm khi bạn chưa có giá trị: KHÔNG làm gì, 回答人数 không đổi",
       note="Nguồn: r8-r13 (r13 ghi rõ 'xóa point ⇒ k làm gì')."),

    tc("Ghi giá trị từ màn admin", "FUNC-MULTI-001", "Normal",
       "Multi action ở màn chat 1:1: set / cộng / trừ / xóa / random điểm cho bạn ĐÃ có giá trị",
       "- Trường ポイント, các bạn đã có giá trị điểm sẵn",
       "1. Với từng bạn đã có giá trị, thực hiện: 0→≠0 · ≠0→0 · set random · cộng · trừ · xóa\n"
       "2. Sau mỗi lần đọc giá trị ở right bar, 友だち詳細 và 回答人数",
       "6 loại action điểm, bạn đã có giá trị",
       "- Giá trị cập nhật đúng theo từng loại action\n"
       "- 回答人数 không đổi ở các thao tác cập nhật\n"
       "- Thao tác xóa điểm: giá trị bị xóa, 回答人数 giảm 1",
       note="Nguồn: r14-r19."),

    tc("Ghi giá trị từ màn admin", "FUNC-001", "Normal",
       "Sửa giá trị ở màn 友だち詳細 bằng phím Enter → lưu đúng",
       "- Trường ポイント, bạn U1",
       "1. Mở " + MYPAGE + " của U1\n2. Nhập giá trị vào ô rồi nhấn Enter (không bấm nút lưu)\n"
       "3. Reload màn và đọc lại giá trị\n4. Lặp với các trường hợp 0 / ≠0 / xóa trắng",
       "Nhấn Enter thay vì bấm nút lưu · giá trị 0, 50, xóa trắng",
       "- Cả 3 trường hợp đều lưu đúng sau khi nhấn Enter\n"
       "- Sau reload giá trị giữ nguyên\n- 回答人数 thay đổi đúng quy tắc",
       note="Nguồn: r20-r24 (khối 2024-08 màn mypage)."),

    tc("Ghi giá trị từ màn admin", "CONC-001", "Abnormal",
       "Thao tác cập nhật giá trị LIÊN TỤC không chờ lưu xong → dữ liệu cuối đúng, không sinh bản ghi thừa",
       "- Trường ポイント, bạn U1 đang có giá trị",
       "1. Ở " + MYPAGE + " cập nhật giá trị 10 lần liên tiếp thật nhanh\n"
       "2. Reload và đọc giá trị\n3. Mở màn danh sách câu trả lời đếm số dòng của U1\n"
       "4. Đọc 回答人数",
       "10 lần cập nhật liên tiếp",
       "- Giá trị cuối cùng = giá trị lần cập nhật cuối\n"
       "- U1 chỉ có 1 dòng ở màn danh sách câu trả lời\n- 回答人数 không bị tăng thêm",
       note="Nguồn: r25 ('thao tác update liên tục')."),

    tc("Ghi giá trị từ màn admin", "SYNC-APP-001", "Normal",
       "Set / cập nhật / xóa giá trị trên APP MOBILE (màn my page) → web hiển thị đồng bộ",
       "- App mobile đăng nhập cùng bot\n- Bạn U1 chưa có giá trị ở trường ポイント",
       "1. Trên app: set giá trị 0 → kiểm tra web\n2. Set giá trị ≠ 0 → kiểm tra web\n"
       "3. Cập nhật 0 → ≠0 và ≠0 → 0 → kiểm tra web\n4. Xóa giá trị → kiểm tra web",
       "5 thao tác trên app mobile",
       "- Sau mỗi thao tác, web (友だち詳細 + right bar + màn danh sách câu trả lời) hiển thị đúng giá trị\n"
       "- 回答人数 thay đổi đúng quy tắc thêm/cập nhật/xóa",
       env="PRODUCTION",
       note="⚠️ Corpus r26-r30 (08/2024) đánh dấu NG cho 3 case app (set 0, cập nhật 0→≠0, ≠0→0) ở cột Test Result "
            "nhưng OK ở staging/step → CẦN VERIFY LẠI, xem MT-15."),

    tc("Ghi giá trị từ màn admin", "SYNC-APP-001", "Normal",
       "Cấu hình hiển thị trường thông tin trên my page (thêm/bớt) → web và app hiển thị đồng bộ",
       "- Bot có các trường địa chỉ và trường tự tạo\n- App mobile đăng nhập cùng bot",
       "1. Trên app my page: bấm thêm (+) 1 trường vào danh sách hiển thị → kiểm tra web\n"
       "2. Bấm bớt (-) trường đó → kiểm tra web\n"
       "3. Lặp cho các trường địa chỉ 都道府県名, 郵便番号, 市区町村名, 町名/番地, 建物名・部屋番号 và trường tự tạo\n"
       "4. Đổi cấu hình hiển thị ở phía WEB → kiểm tra app",
       "5 trường địa chỉ + các trường khác · 2 chiều web ↔ app",
       "- Thêm/bớt được trường khỏi danh sách hiển thị my page\n"
       "- Màn my page phía web hiển thị đúng theo cấu hình bên app\n"
       "- Đổi cấu hình bên web thì app cũng hiển thị đúng danh sách",
       env="PRODUCTION",
       note="Bug #30558 (07/2025 — friend info trong folder địa chỉ không hiển thị trên my page ở app). "
            "Nguồn: r33-r44."),

    tc("Ghi giá trị từ màn admin", "SYNC-APP-001", "Normal",
       "Sắp xếp danh sách trường hiển thị trên my page → thứ tự đồng bộ web ↔ app",
       "- App mobile và web cùng bot, my page đang hiển thị ≥ 4 trường",
       "1. Trên app sắp xếp lại thứ tự các trường\n2. Mở my page phía web đối chiếu thứ tự\n"
       "3. Reload cả 2 phía",
       "≥ 4 trường",
       "- Thứ tự hiển thị trên web khớp thứ tự vừa sắp xếp trên app\n- Sau reload thứ tự giữ nguyên",
       env="PRODUCTION",
       note="Nguồn: r45 ('sort list info')."),

    tc("Ghi giá trị từ màn admin", "SYNC-APP-001", "Normal",
       "Hiển thị và cập nhật giá trị 5 trường địa chỉ trên app my page → khớp với web",
       "- App mobile, bạn U1 có giá trị ở 5 trường địa chỉ",
       "1. Trên app mở my page của U1, đọc giá trị 5 trường địa chỉ\n"
       "2. Đối chiếu với 友だち詳細 phía web\n"
       "3. Trên app: thêm mới / cập nhật / xóa giá trị từng trường địa chỉ\n"
       "4. Sau mỗi thao tác đối chiếu lại phía web",
       "5 trường địa chỉ: 郵便番号 · 都道府県名 · 市区町村名 · 町名/番地 · 建物名・部屋番号",
       "- Giá trị hiển thị trên app khớp web ở mọi trường\n"
       "- Thêm/cập nhật/xóa trên app đều phản ánh đúng trên web\n- 回答人数 thay đổi đúng quy tắc",
       env="PRODUCTION",
       note="Nguồn: r46-r69 (Bug #30558)."),

    tc("Ghi giá trị từ màn admin", "SYNC-APP-001", "Normal",
       "Cập nhật giá trị từ WEB → app my page hiển thị đúng (chiều ngược lại)",
       "- App mobile mở sẵn my page của U1",
       "1. Ở web 友だち詳細 của U1: thêm mới / cập nhật / xóa giá trị 5 trường địa chỉ và các trường khác\n"
       "2. Sau mỗi thao tác, refresh app my page và đối chiếu",
       "5 trường địa chỉ + các trường khác · 3 thao tác",
       "- App hiển thị đúng giá trị sau mỗi thao tác từ web\n- Không lệch dữ liệu giữa 2 phía",
       env="PRODUCTION",
       note="Nguồn: r70-r87 (Bug #30558)."),

    tc("Ghi giá trị từ màn admin", "MSG-001", "Normal",
       "Giá trị friend info được thay thế đúng trong tin nhắn gửi từ các lối gửi khác nhau",
       "- Bạn U1 có giá trị ở trường I1\n- Có template text, template button, chat 1:1 và multi action "
       "chứa mã chèn giá trị friend info",
       "1. Gửi template type text có chèn giá trị → kiểm tra LINE app U1\n"
       "2. Gửi template type button có chèn giá trị → kiểm tra\n"
       "3. Gửi tin nhắn chat 1:1 (web và app) có chèn giá trị → kiểm tra\n"
       "4. Chạy multi action gồm action text và action template → kiểm tra",
       "5 lối gửi × 1 bạn có giá trị",
       "- Cả 5 lối gửi: tin nhắn tới LINE app hiển thị GIÁ TRỊ THẬT của bạn, không còn mã chèn\n"
       "- Nội dung còn lại của tin nhắn không bị đổi",
       env="PRODUCTION",
       note="RULE-06 (đi tới LINE app). Nguồn: r92-r96 (khối 2024-08)."),

    tc("Ghi giá trị từ màn admin", "MSG-001", "Normal",
       "Giá trị friend info được thay thế đúng trong message pattern của form / salon / lesson",
       "- Bạn U1 có giá trị ở trường I1\n- Form, salon, lesson đều có message pattern chèn giá trị friend info",
       "1. U1 submit form → kiểm tra tin nhắn nhận được trên LINE app\n"
       "2. U1 booking salon → kiểm tra tin nhắn\n3. U1 booking lesson → kiểm tra tin nhắn",
       "3 tính năng có message pattern",
       "- Cả 3 tin nhắn hiển thị đúng giá trị thật của U1, không còn mã chèn\n"
       "- Bạn chưa có giá trị: kiểm tra hành vi thay thế (rỗng hay giữ mã) và ghi nhận",
       env="PRODUCTION",
       note="Nguồn: r97-r99. Vế 'bạn chưa có giá trị' do AI bổ sung — spec không ghi, cần Leader chốt."),

    tc("Ghi giá trị từ màn admin", "STATE-001", "Abnormal",
       "Xóa trắng giá trị trường Lựa chọn / Điểm CÓ gắn action → KHÔNG kích hoạt action ngoài ý",
       "- Trường 選択肢 có option A gắn action gửi text T1; trường ポイント có ngưỡng gắn action gửi text T2\n"
       "- Bạn U1 đang có giá trị ở cả 2 trường và đã nhận action trước đó\n- 稼働設定 =「何度でも稼働」",
       "1. Ở màn 友だち詳細 của U1 xóa trắng giá trị trường 選択肢 → lưu\n"
       "2. Theo dõi LINE app của U1 trong 5 phút\n"
       "3. Xóa trắng giá trị trường ポイント → lưu\n4. Theo dõi LINE app của U1\n"
       "5. Đọc 回答人数 của 2 trường",
       "Xóa trắng 2 trường có gắn action, 稼働設定 đang cho phép chạy lại",
       "- U1 KHÔNG nhận thêm tin T1 hay T2 nào sau khi xóa trắng\n"
       "- Giá trị của cả 2 trường bị xóa, 回答人数 mỗi trường giảm 1\n"
       "- Lịch sử ở 友だち詳細 ghi nhận thao tác xóa, không ghi nhận action được kích hoạt",
       note="Tương ứng RV-03 (r478) — ghi chú gốc nêu rủi ro 'triggerFriendInfoAction vẫn chạy với content=null "
            "khi xóa SELECT/POINT'. TC gốc chỉ có tiêu đề + các bước; expected do AI viết."),

    tc("Ghi giá trị từ màn admin", "JOB-001", "Abnormal",
       "Xóa trắng giá trị trường 年月日 CÓ gắn action lịch → lịch gửi được dọn, không còn lịch mồ côi",
       "- Trường 年月日 có cấu hình action lịch\n- Bạn U1 đang có giá trị và đã sinh lịch gửi tương lai\n"
       "- Bạn U2 cũng có lịch (đối chứng, không bị đụng)",
       "1. Ghi lại mốc gửi dự kiến của U1 và U2\n"
       "2. Ở màn 友だち詳細 của U1 xóa trắng giá trị trường 年月日 → lưu\n"
       "3. Chờ qua mốc gửi cũ của U1, kiểm tra LINE app U1\n"
       "4. Chờ mốc của U2, kiểm tra LINE app U2\n5. Đọc 回答人数",
       "U1 bị xóa trắng giá trị · U2 giữ nguyên",
       "- U1 KHÔNG nhận action nào tại mốc gửi cũ\n- U2 VẪN nhận action đúng giờ\n"
       "- 回答人数 giảm 1, U1 không còn ở màn danh sách câu trả lời",
       env="PRODUCTION",
       note="Tương ứng RV-04 (r479) — 'xóa dòng mà không dọn lịch sẽ để schedule trỏ dữ liệu đã xóa'. "
            "TC gốc chỉ có tiêu đề; expected do AI viết. RULE-08 (job) → PRODUCTION."),

    tc("Ghi giá trị từ màn admin", "FUNC-001", "Normal",
       "Cập nhật giá trị friend info từ mọi lối vào admin → hiển thị đồng bộ ở 3 nơi",
       "- Bạn U1, trường I1 (kiểu 選択肢)",
       "1. Thêm/cập nhật/xóa giá trị bằng tab friend info của màn chat 1:1 → đối chiếu 3 nơi\n"
       "2. Lặp bằng multi action ở màn chat 1:1 → đối chiếu\n"
       "3. Lặp bằng 友だち詳細 → đối chiếu",
       "3 lối vào × {thêm, cập nhật, xóa}",
       "- Sau mỗi thao tác, giá trị khớp nhau ở: right bar chat 1:1, 友だち詳細 và màn danh sách câu trả lời\n"
       "- 回答人数 đổi đúng quy tắc",
       note="RULE-07. Nguồn: r90-r91, r100-r105 (khối 2024-08)."),

    # ══════════════════ Ghi giá trị từ tính năng khác ══════════════════
    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Bạn trả lời FORM có map friend info → giá trị được ghi và hiển thị đủ 3 nơi",
       "- Form có item map tới trường friend info I1\n- Bạn U1 chưa có giá trị",
       "1. Gửi link form cho U1, U1 submit form với câu trả lời X\n"
       "2. Mở " + MYPAGE + " của U1\n3. Mở " + RIGHTBAR + "\n"
       "4. Mở màn danh sách câu trả lời của I1\n5. Đọc 回答人数",
       "U1 trả lời X",
       "- Cả 3 nơi hiển thị giá trị X\n- 回答人数 tăng 1\n- Lịch sử ở 友だち詳細 ghi nhận nguồn cập nhật",
       note="Nguồn: r106, r464 + tab「Change spec info type select」r11."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Booking salon / lesson (bạn tự book, admin book, có bill tiền) ghi giá trị friend info",
       "- Salon và lesson có form nhập map tới trường friend info",
       "1. Bạn tự book salon → kiểm tra giá trị và 回答人数\n2. Admin book hộ salon → kiểm tra\n"
       "3. Book salon có bill tiền → kiểm tra\n4. Lặp cả 3 kịch bản với lesson",
       "2 tính năng × 3 kịch bản (user book, admin book, có bill tiền)",
       "- Cả 6 lượt: giá trị friend info được ghi đúng, hiển thị ở 友だち詳細 và right bar\n"
       "- 回答人数 tăng đúng khi là giá trị mới\n- Trường hợp có bill tiền: giá trị vẫn ghi đủ sau khi thanh toán",
       env="PRODUCTION",
       note="RULE-08 (bill tiền → PRODUCTION). Nguồn: r107-r112 (khối 2024-08)."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Booking salon/lesson có bật tự động điền giá trị friend info lên form → form hiện sẵn giá trị cũ",
       "- Lesson/salon có item map friend info, bật tùy chọn tự động load dữ liệu\n"
       "- Bạn U1 đã có giá trị ở các trường được map",
       "1. U1 mở màn booking lesson → quan sát các ô đã map\n"
       "2. Tắt tùy chọn tự động load, U1 mở lại màn booking → quan sát\n3. Lặp với salon",
       "2 tính năng × {bật, tắt} tự động load",
       "- Khi bật: các ô hiển thị sẵn đúng giá trị friend info hiện có của U1\n"
       "- Khi tắt: các ô để trống, không tự điền",
       note="Nguồn: Feature #29832 r224-r225, r232-r233."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Bạn booking KHÔNG nhập câu trả lời → không tạo giá trị friend info, count không đổi",
       "- Lesson/salon/booking event/item có form map friend info, ô nhập không bắt buộc\n"
       "- Bạn U2 chưa có giá trị",
       "1. U2 book và bỏ trống ô map friend info\n2. Đọc 回答人数 và 友だち詳細 của U2\n"
       "3. Lặp cho booking event và mua item",
       "4 tính năng, bỏ trống ô map",
       "- Không tạo giá trị friend info cho U2\n- 回答人数 không đổi\n"
       "- 友だち詳細 không hiển thị dòng giá trị rỗng",
       note="Nguồn: Feature #29832 r226-r227, r237-r240 + tab「Improve count phía web」r97, r103."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Mua item / booking event có map friend info kiểu 選択肢 → ghi giá trị đúng option",
       "- Item và booking event có form map trường 選択肢",
       "1. Bạn U1 mua item 1 lần, chọn option A → kiểm tra giá trị và 回答人数\n"
       "2. U1 mua item theo chu kỳ → kiểm tra\n3. U1 booking event chọn option B → kiểm tra\n"
       "4. Admin book hộ event → kiểm tra",
       "Item 1 lần · item chu kỳ · event bạn book · event admin book",
       "- Cả 4 lượt hiển thị đúng danh sách option để chọn\n"
       "- Giá trị friend info ghi đúng option đã chọn\n- 回答人数 tăng khi là giá trị mới",
       env="PRODUCTION",
       note="RULE-08 (mua item liên quan bill tiền). Nguồn: Feature #29832 r237-r240."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Import CSV ghi giá trị friend info → giá trị và count cập nhật đúng",
       "- File CSV chứa cột map tới trường friend info, gồm bạn đã có giá trị và bạn chưa có",
       "1. Import CSV với 10 dòng (5 bạn chưa có giá trị, 5 bạn đã có)\n"
       "2. Chờ import xong, đọc 回答人数\n3. Mở 友だち詳細 của 2 bạn đại diện\n"
       "4. Mở màn danh sách câu trả lời",
       "10 dòng: 5 thêm mới, 5 cập nhật",
       "- 回答人数 tăng đúng 5 (chỉ tính bạn mới có giá trị)\n"
       "- 5 bạn cũ có giá trị mới theo file, không sinh dòng trùng\n"
       "- Màn danh sách câu trả lời khớp số lượng",
       env="PRODUCTION",
       note="RULE-08 (job import). Nguồn: tab「Change spec info type select」r22 + r469 (xóa qua CSV)."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "Import CSV với giá trị RỖNG cho bạn đang có giá trị → xóa giá trị, count giảm",
       "- Bạn U1, U2 đang có giá trị ở trường I1",
       "1. Import CSV với cột giá trị để trống cho U1 và U2\n2. Đọc 回答人数\n"
       "3. Mở 友だち詳細 của U1, U2\n4. Mở màn danh sách câu trả lời",
       "2 dòng CSV giá trị rỗng",
       "- 回答人数 giảm đúng 2\n- U1, U2 không còn giá trị ở I1, không có dòng rỗng\n"
       "- Không còn U1, U2 ở màn danh sách câu trả lời",
       env="PRODUCTION",
       note="Nguồn: r469 (#38591). Tương ứng RV-06 (r481 — chốt hành vi cross-feature)."),

    tc("Ghi giá trị từ tính năng khác", "INTG-HOOK-001", "Normal",
       "QR landing có set param → ghi giá trị friend info cho bạn quét mã",
       "- QR landing cấu hình param ghi vào 5 trường địa chỉ và 1 trường tự tạo",
       "1. Bạn mới quét QR (có callback kết bạn) → kiểm tra giá trị 6 trường\n"
       "2. Bạn cũ quét QR (không có callback kết bạn) → kiểm tra giá trị\n"
       "3. Đọc 回答人数 sau mỗi lượt",
       "2 kịch bản: bạn mới · bạn cũ",
       "- Cả 2 kịch bản: giá trị 6 trường được ghi đúng theo param\n"
       "- Hiển thị đúng ở 友だち詳細 và right bar\n- 回答人数 tăng đúng cho từng trường",
       env="PRODUCTION",
       note="Nguồn: r465, r497 + tab date r121-r123, r252-r256."),

    tc("Ghi giá trị từ tính năng khác", "REG-SHARED-001", "Normal",
       "Trường 選択肢 được map ở form / booking / item: đổi option ở màn friend info → nơi map cập nhật theo",
       "- Form answer, booking calendar, booking event, lesson, salon, item đều map tới trường 選択肢 I1",
       "1. Ở màn friend information: thêm option mới → kiểm tra 6 nơi map\n"
       "2. Đổi text 1 option → kiểm tra 6 nơi\n3. Xóa 1 option → kiểm tra 6 nơi\n"
       "4. Với lesson/salon kiểm tra cả loại 'map info có sẵn' và loại 'info tự gen'",
       "6 nơi map × 3 thao tác",
       "- Thêm option: cả 6 nơi có option mới trong danh sách chọn\n"
       "- Đổi text: cả 6 nơi hiển thị text mới\n- Xóa option: cả 6 nơi không còn option đó\n"
       "- Không nơi nào văng lỗi khi mở",
       note="Nguồn: tab「Change spec info type select」r25-r36, r39-r68."),

    tc("Ghi giá trị từ tính năng khác", "REG-SHARED-001", "Normal",
       "Tạo trường friend info MỚI ngay từ màn setting form nhập của lesson/salon → trường xuất hiện ở màn friend information",
       "- Lesson/salon có màn setting form nhập cho phép tạo mới friend info (loại info tự gen)",
       "1. Ở màn setting form nhập của lesson, tạo mới 1 trường friend info kiểu 選択肢 với 3 option\n"
       "2. Mở màn /basic/friend-information tìm trường vừa tạo\n"
       "3. Mở màn edit của trường đó đọc danh sách option\n4. Lặp với salon",
       "Lesson + salon, mỗi bên tạo 1 trường 3 option",
       "- Trường mới xuất hiện ở màn friend information (đúng folder mặc định)\n"
       "- Màn edit hiển thị đủ 3 option đúng text\n- Bạn booking chọn được option và giá trị ghi đúng",
       note="Nguồn: tab「Change spec info type select」r29, r33."),

    tc("Ghi giá trị từ tính năng khác", "DATA-COUNT-001", "Normal",
       "Giá trị ghi từ tính năng khác rồi bị XÓA qua chính lối đó → hành vi dòng dữ liệu + count thống nhất với lối my page",
       "- Trường I1 có giá trị được tạo lần lượt từ: form, param QR, import CSV, booking event/item",
       "1. Với mỗi nguồn: tạo giá trị cho 1 bạn riêng → ghi 回答人数\n"
       "2. Xóa giá trị qua chính nguồn đó (trả lời lại form để trống / ghi đè rỗng / CSV rỗng)\n"
       "3. Sau mỗi lần: đọc 回答人数, kiểm tra 友だち詳細 và màn danh sách câu trả lời\n"
       "4. So sánh hành vi với lối xóa ở 友だち詳細",
       "4 nguồn ghi giá trị",
       "- Mỗi nguồn: sau khi xóa, bạn KHÔNG còn ở màn danh sách câu trả lời và 回答人数 giảm 1\n"
       "- Không còn dòng giá trị rỗng nào ở 友だち詳細\n"
       "- Hành vi giống hệt lối xóa ở 友だち詳細",
       note="Tương ứng RV-06 (r481) — TC gốc chỉ có tiêu đề + các bước; expected do AI viết. "
            "⚠️ Ghi chú gốc nêu rõ fix #38591 chỉ đụng service my page nên các lối khác CẦN CHỐT SCOPE — xem MT-03."),
]
