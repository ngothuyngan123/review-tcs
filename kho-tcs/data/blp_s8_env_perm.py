# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 38-40: ảnh hưởng khi hợp đồng hết hạn, phân quyền & staff, môi trường & regression.

Nguồn chính: TCsLine_Bill tiền → tab「Logic chung」(08/2025 — expired_date + 7 ngày ảnh hưởng
  trang phía LINE user của Lesson/Salon/Form/Item/Booking Event; SpecChange #32268 đổi địa chỉ trên
  file hóa đơn & estimation).
Bổ sung: tab「Quản lý hợp đồng」r268-r305 (phân quyền enterprise), r820-r827 (middleware bot A ↔ bot B),
  r1580-r1653 (Bug KH #36303 — ma trận 68 TC phân quyền staff).
"""
from _common import tc

STAFF = ("- Có user A là staff của bot B (owner là user C)\n"
         "- Role của A cấu hình quyền màn 契約情報 (pointSettings) theo từng case")

S8 = [
    # ═════════════ 38. Hợp đồng hết hạn ảnh hưởng tính năng ═════════════
    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "INTG-002", "Boundary",
       "Bot plan trả phí quá hạn: mốc expired_date + 7 ngày quyết định LINE user mở được trang hay không",
       "- Bot plan_type = 1 (standard) có trang mua mới của Lesson\n"
       "- Chỉnh expired_date_contract để tạo 3 mốc so với hiện tại",
       "1. Set expired_date + 7d > now → LINE user mở link màn mua mới\n"
       "2. Set expired_date + 7d = now → mở link\n3. Set expired_date + 7d < now → mở link",
       "3 mốc: +7d > now, = now, < now",
       "- expired_date + 7d > now: MỞ ĐƯỢC màn mua mới\n"
       "- expired_date + 7d = now: KHÔNG mở được\n- expired_date + 7d < now: KHÔNG mở được",
       note="Nguồn: tab「Logic chung」r3-r5 (08/2025). RULE-06: kiểm ở phía LINE user, không dừng ở admin. "
            "Mốc '+7 ngày' này KHÔNG có trong feature-spec.md — xem MT-40."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "INTG-002", "Normal",
       "Bot plan FREE: mọi mốc thời gian đều mở được trang phía LINE user",
       "- Bot plan_type = 2 (free) có trang mua mới của Lesson",
       "1. Set expired_date + 7d > now → LINE user mở link màn mua mới\n"
       "2. Set = now → mở link\n3. Set < now → mở link",
       "3 mốc, bot plan free",
       "Cả 3 mốc đều MỞ ĐƯỢC màn mua mới (plan free không bị chặn theo expired_date hợp đồng)",
       note="Nguồn: tab Logic chung r6-r8."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "INTG-002", "Boundary",
       "Cùng quy tắc +7 ngày áp cho màn LỊCH SỬ của Lesson và Salon",
       "- Bot standard và bot free, có Lesson và Salon đã cấu hình",
       "1. Với bot standard: 3 mốc +7d (>, =, <) → LINE user mở màn lịch sử Lesson\n"
       "2. Lặp lại với Salon\n3. Lặp lại toàn bộ với bot free",
       "2 tính năng (Lesson, Salon) × 2 plan × 3 mốc",
       "- Bot standard: +7d > now mở được màn lịch sử; = now và < now KHÔNG mở được\n"
       "- Bot free: cả 3 mốc đều mở được",
       note="Nguồn: tab Logic chung r9-r26 (gộp theo cùng quy tắc, liệt kê đủ tổ hợp ở Dữ liệu test)."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "INTG-002", "Boundary",
       "Quy tắc +7 ngày áp cho FORM và BOOKING EVENT phía LINE user",
       "- Bot standard và bot free, có form và event booking đã public",
       "1. Với bot standard: 3 mốc +7d → LINE user mở link form\n2. Lặp lại với link Booking Event\n"
       "3. Lặp lại toàn bộ với bot free",
       "2 tính năng (Form, Booking Event) × 2 plan × 3 mốc",
       "- Bot standard: +7d > now mở được (「mở form bình thường」/「mở Booking Event bình thường」); "
       "= now và < now → 「Không mở được form」/「Không mở được Booking Event」\n"
       "- Bot free: mở được ở cả 3 mốc",
       note="Nguồn: tab Logic chung r27-r50, r87-r92."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "INTG-002", "Boundary",
       "Quy tắc +7 ngày áp cho ITEM (màn mua, màn bill UnivaPay/Stripe, màn Cancel)",
       "- Bot standard và bot free, có item bill 1 lần và item bill nhiều lần (chu kỳ)",
       "1. Với bot standard, item bill nhiều lần: 3 mốc +7d → LINE user mở màn mua, "
       "màn bill UnivaPay, màn bill Stripe, màn Cancel\n"
       "2. Lặp lại với item bill 1 lần\n3. Lặp lại toàn bộ với bot free",
       "2 loại item × 4 màn × 2 plan × 3 mốc",
       "- Bot standard: +7d > now mở được cả 4 màn; = now và < now đều KHÔNG mở được\n"
       "- Bot free: mở được ở cả 3 mốc",
       note="Nguồn: tab Logic chung r51-r86."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "COMPAT-BROWSER-001", "Normal",
       "Kiểm tra lại quy tắc +7 ngày trên PC (không chỉ trên LINE app mobile)",
       "- Bot standard có link Form và link Item đã public",
       "1. Mở link bằng trình duyệt PC ở mốc +7d > now\n2. Mở ở mốc +7d < now",
       "Trình duyệt PC (Chrome)",
       "Hành vi mở/chặn giống hệt khi mở trong LINE app; không có nhánh nào bị bỏ chặn trên PC",
       note="Nguồn: tab Logic chung r93 (chỉ có tiêu đề). Kết quả mong đợi do AI viết theo quy tắc "
            "chung — CẦN LEADER XÁC NHẬN."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "DATA-006", "Normal",
       "Đổi địa chỉ công ty trên file hóa đơn và báo giá (SpecChange #32268)",
       "- Có ≥ 1 hóa đơn cũ (trước ngày đổi địa chỉ) và ≥ 1 hóa đơn mới",
       "1. Tải hóa đơn MỚI từ /basic/payment-history → mở PDF, đọc địa chỉ\n"
       "2. Tải hóa đơn CŨ → mở PDF, đọc địa chỉ\n"
       "3. Tạo và tải file 見積書 từ /admin/plan-estimation → đọc địa chỉ và font chữ",
       "Hóa đơn cũ + hóa đơn mới + 1 báo giá",
       "- Hóa đơn mới và báo giá: hiện ĐỊA CHỈ MỚI\n"
       "- File 見積書 dùng font Gothic và có phần text được bổ sung theo spec change\n"
       "- Hóa đơn cũ: kiểm tra và ghi nhận địa chỉ hiển thị (cũ hay mới)",
       note="Nguồn: tab Logic chung r95, r97-r126 (SpecChange #32268, 04/10/2025). "
            "⚠ Corpus KHÔNG nêu rõ hóa đơn CŨ dùng địa chỉ nào → cần Leader chốt, xem MT-41."),

    tc("Hợp đồng hết hạn ảnh hưởng tính năng", "DATA-006", "Normal",
       "Tên bot trên file hóa đơn/báo giá hiển thị đúng với mọi bộ ký tự",
       "- Chuẩn bị 3 bot có tên: tiếng Nhật, latinh, ký tự đặc biệt",
       "1. Tải hóa đơn của từng bot → mở PDF, đọc tên bot\n"
       "2. Tạo báo giá nhập tên tương ứng → mở PDF, đọc tên",
       "3 bộ ký tự: tiếng Nhật「テストBOT」, latinh「Test BOT」, đặc biệt「Test&<>BOT#1」",
       "Cả 3 bộ ký tự đều hiển thị đúng trên PDF, không lỗi font, không bị escape sai, không cắt chữ",
       note="Nguồn: tab Logic chung r97-r126 (các dòng Check tên bot). "
            "Nhiều input khác nhau nhưng CÙNG 1 kết quả → giữ chung 1 TC theo quy tắc tách TC."),

    # ═════════════ 39. Phân quyền & staff ═════════════
    tc("Phân quyền & staff", "PERM-001", "Normal",
       "Staff mở /basic/point-settings ở 4 ngữ cảnh chọn bot → đều access được màn list",
       STAFF,
       "1. Chưa chọn bot nào → mở /basic/point-settings\n"
       "2. Chọn bot ĐƯỢC phân quyền → mở lại\n3. Chọn bot KHÔNG được phân quyền → mở lại\n"
       "4. Chọn bot mà chính user đó làm owner → mở lại",
       "4 ngữ cảnh chọn bot",
       "Cả 4 ngữ cảnh: access thành công vào màn list hợp đồng "
       "(chỉ hiển thị các hợp đồng user có quyền)",
       note="Nguồn: r1583, r1600, r1617, r1634 (Bug KH #36303, 07/05/2026 — 4 dòng cùng expected → gộp)."),

    tc("Phân quyền & staff", "PERM-001", "Normal",
       "Staff mở detail hợp đồng CHƯA add bot / hợp đồng ĐƯỢC phân quyền / hợp đồng mình làm owner → OK",
       STAFF,
       "1. Với từng ngữ cảnh chọn bot (4 ngữ cảnh), mở detail của: hợp đồng chưa add bot, "
       "hợp đồng của bot được phân quyền, hợp đồng mà chính user làm owner",
       "4 ngữ cảnh × 3 loại hợp đồng = 12 tổ hợp",
       "Cả 12 tổ hợp: access thành công vào màn chi tiết hợp đồng",
       note="Nguồn: r1584, r1585, r1593, r1601, r1602, r1610, r1618, r1619, r1627, r1635, r1636, r1644 "
            "(12 dòng cùng expected → gộp)."),

    tc("Phân quyền & staff", "PERM-001", "Normal",
       "Staff thực hiện được 6 thao tác trên hợp đồng mình có quyền",
       STAFF + "\n- Staff A có quyền pointSettings với bot B",
       "1. Ở màn detail hợp đồng được phân quyền, thực hiện: đổi phương thức thanh toán, "
       "đổi kỳ thanh toán, đăng ký thẻ phụ, sửa thẻ phụ, xóa thẻ phụ, hủy hợp đồng\n"
       "2. Lặp lại ở cả 4 ngữ cảnh chọn bot",
       "6 thao tác × 4 ngữ cảnh",
       "Cả 24 tổ hợp: thao tác thực hiện được, hợp đồng cập nhật đúng",
       note="Nguồn: r1586-r1591, r1594-r1599, r1603-r1608, r1611-r1616, r1620-r1625, r1628-r1633, "
            "r1637-r1642, r1645-r1650 (48 dòng cùng nhóm → gộp)."),

    tc("Phân quyền & staff", "PERM-002", "Abnormal",
       "Staff mở detail hợp đồng của bot KHÔNG được phân quyền → báo lỗi và không thấy ở màn list",
       STAFF + "\n- Có bot D mà staff A KHÔNG được phân quyền",
       "1. Ở từng ngữ cảnh chọn bot (4 ngữ cảnh), dán URL /basic/detail-contract/{id bot D}\n"
       "2. Kiểm tra màn /basic/point-settings có hiện hợp đồng bot D không",
       "4 ngữ cảnh chọn bot; hợp đồng của bot D",
       "- Cả 4 ngữ cảnh: hiện message không có quyền truy cập, KHÔNG vào được màn chi tiết\n"
       "- Màn point-setting KHÔNG hiển thị hợp đồng của bot D",
       note="Nguồn: r1592, r1609, r1626, r1643, r1298, r1299 (4 dòng cùng expected → gộp)."),

    tc("Phân quyền & staff", "PERM-002", "Abnormal",
       "Reproduce Bug KH #36303: staff không quyền hủy được Standard slot chưa kết nối bot",
       "- User A đăng ký 1 Standard Plan slot CHƯA kết nối bot (A là owner của slot đó)\n"
       "- A được mời làm staff cho bot B (owner = user C) với role KHÔNG có quyền màn 契約情報",
       "1. Login bằng A, chọn ngữ cảnh bot B (bot staff)\n"
       "2. Mở /basic/point-settings\n3. Tìm hợp đồng Standard slot chưa kết nối của chính A\n"
       "4. Thực hiện hủy hợp đồng đó",
       "A là owner slot standard chưa connect, đồng thời là staff không quyền của bot B",
       "A hủy được hợp đồng của CHÍNH MÌNH; KHÔNG bị chặn bằng lỗi「không có quyền」",
       note="Nguồn: r1581 (Bug KH #36303, 07/05/2026). Đây là TC tái hiện bug — nếu FAIL thì raise lại bug."),

    tc("Phân quyền & staff", "SEC-002", "Abnormal",
       "URL tampering: user B lấy URL detail contract của user A → bị chặn",
       "- User A có hợp đồng X; user B có hợp đồng Y (cùng plan)\n- Đang login bằng user B",
       "1. Lấy URL /basic/detail-contract/{id hợp đồng X}\n2. Dán vào trình duyệt đang login B\n"
       "3. Thử gọi trực tiếp API thay đổi hợp đồng X (đổi kỳ / hủy) bằng công cụ HTTP",
       "id hợp đồng X thuộc user A",
       "- Mở URL: bị chặn (404 hoặc message không có quyền)\n"
       "- Gọi API trực tiếp: server chặn ở TẦNG API, không thay đổi được hợp đồng X",
       note="Nguồn: r1652 (corpus chỉ mô tả kịch bản, không ghi expected). "
            "Kết quả mong đợi do AI viết theo BR-07 authenticationBotContract → CẦN LEADER XÁC NHẬN. "
            "Bước 3 (API tampering) bắt buộc theo tiền lệ bug 'API list không enforce quyền dù UI ẩn menu'."),

    tc("Phân quyền & staff", "SEC-003", "Abnormal",
       "Đổi quyền giữa phiên: staff load màn detail rồi bị gỡ quyền → submit phải bị chặn",
       "- Staff A đang mở màn detail contract của bot B (owner = C)",
       "1. A load màn detail contract\n2. Owner C gỡ quyền pointSettings của A\n"
       "3. Trên session cũ của A, bấm submit 1 thay đổi hợp đồng (đổi kỳ / hủy)\n"
       "4. Kiểm tra bot_contracts",
       "Quyền bị gỡ SAU khi A đã load trang",
       "Server chặn thao tác submit, hợp đồng KHÔNG bị thay đổi; A nhận message không có quyền",
       note="Nguồn: r1653 (CL18 — corpus chỉ mô tả kịch bản). Kết quả mong đợi do AI viết — "
            "CẦN LEADER XÁC NHẬN."),

    tc("Phân quyền & staff", "SEC-002", "Abnormal",
       "Middleware bot A ↔ bot B: 8 màn thao tác hợp đồng đều chặn truy cập chéo",
       "- Đang chọn ngữ cảnh bot A\n- Biết id hợp đồng và id slot của bot B (khác owner)",
       "1. Dán lần lượt URL của bot B: /basic/detail-contract/{id} · /basic/change-bill-type/{id} · "
       "/basic/change-payment-method/{id} · /basic/detail/extend-contract/{id} · "
       "/basic/detail-contract/{id}/cancel · /basic/re-contract/{id} · /basic/change-card/{id} · "
       "/basic/sub-card-setting/{id}\n"
       "2. Ghi lại kết quả từng URL",
       "8 URL của bot B",
       "Cả 8 URL đều KHÔNG cho phép truy cập (chặn bằng middleware, không render màn của bot B)",
       note="Nguồn: r820-r827 (corpus liệt kê 8 màn, KHÔNG ghi expected riêng — kết quả gộp từ tiêu đề "
            "「Không cho phép access vào màn hình…」). 8 URL này bổ sung cho danh sách endpoint ở "
            "feature-spec.md §6 (spec chỉ có 12 EP, thiếu các màn change-card / change-bill-type / "
            "extend-contract / re-contract / sub-card-setting) — xem MT-42."),

    tc("Phân quyền & staff", "PERM-002", "Abnormal",
       "Enterprise: staff KHÔNG được phân quyền → ẩn thông báo slot trống, chặn 3 URL",
       "- Hợp đồng enterprise của owner C, còn slot trống\n"
       "- Staff A KHÔNG được phân quyền màn quản lý hợp đồng",
       "1. Login A, mở màn list bot → quan sát thông báo slot trống\n"
       "2. Mở /basic/point-settings → tìm hợp đồng enterprise\n"
       "3. Dán URL /basic/detail-contract/1991\n"
       "4. Dán URL /admin/bot-add-v2?bot_slot_id=4401&type=2\n"
       "5. Dán URL /admin/bots/list-bot-enterprise/1991",
       "Hợp đồng EP id=1991, slot id=4401",
       "- Màn list bot KHÔNG hiện thông báo slot trống của enterprise\n"
       "- Màn list hợp đồng KHÔNG hiển thị hợp đồng enterprise\n"
       "- Cả 3 URL đều báo lỗi「この権限は許可されていません。」",
       note="Nguồn: r270-r274 (Feature #37085)."),

    tc("Phân quyền & staff", "PERM-003", "Normal",
       "Enterprise: staff ĐƯỢC phân quyền → xem được detail nhưng bị chặn 3 thao tác nhạy cảm",
       "- Hợp đồng enterprise của owner C\n- Staff A ĐƯỢC phân quyền màn quản lý hợp đồng",
       "1. Login A, mở /basic/point-settings → tìm hợp đồng enterprise, mở detail\n"
       "2. Quan sát nút「おまとめ割引の契約を変更する」\n"
       "3. Thử: đổi kỳ bill, gia hạn, đổi phương thức bill, đổi thẻ chính, đổi thẻ phụ\n"
       "4. Thử: đổi owner hợp đồng, hủy hợp đồng, hủy kết nối bot",
       "Staff A có quyền pointSettings với bot của hợp đồng EP",
       "- Mở được màn detail, hiện「おまとめ割引 N枠」đúng số slot\n"
       "- Nút「おまとめ割引の契約を変更する」bị ẨN\n"
       "- 5 thao tác ở bước 3: thực hiện được\n"
       "- 3 thao tác ở bước 4 (đổi owner / hủy hợp đồng / hủy kết nối bot): DISABLE, không thực hiện được",
       note="Nguồn: r275-r287."),

    tc("Phân quyền & staff", "PERM-002", "Abnormal",
       "Enterprise: staff được phân quyền vẫn bị chặn màn quản lý slot",
       "- Staff A ĐƯỢC phân quyền màn quản lý hợp đồng của hợp đồng EP id=1991",
       "1. Ở màn list, click text「おまとめ割引」của dòng EP\n"
       "2. Dán URL /admin/bot-add-v2?bot_slot_id=4401&type=2\n"
       "3. Khi CHƯA select vào bot của EP: dán URL /admin/bots/list-bot-enterprise/1991\n"
       "4. Khi ĐÃ select vào bot của EP: dán lại URL đó",
       "Staff A có quyền pointSettings; EP id=1991",
       "Cả 4 lối đều báo lỗi「この権限は許可されていません。」— staff không vào được màn quản lý slot EP "
       "dù đã select đúng bot",
       note="Nguồn: r288-r291."),

    tc("Phân quyền & staff", "PERM-003", "Normal",
       "Owner mở màn quản lý slot enterprise từ mọi ngữ cảnh bot đều được",
       "- Owner của hợp đồng EP id=1991, đồng thời là staff của bot thuộc owner khác",
       "1. Đang select vào 1 bot khác cùng owner → mở /admin/bots/list-bot-enterprise/1991\n"
       "2. Đang select vào 1 bot staff (thuộc owner khác) → mở lại URL đó",
       "2 ngữ cảnh chọn bot",
       "Cả 2 ngữ cảnh: mở được màn quản lý slot enterprise, KHÔNG báo lỗi phân quyền",
       note="Nguồn: r268, r269."),

    tc("Phân quyền & staff", "REG-002", "Normal",
       "Regression: hợp đồng standard/pro không bị ảnh hưởng bởi thay đổi phân quyền enterprise",
       "- Có hợp đồng standard/pro với owner C và staff A (được và không được phân quyền)",
       "1. Owner: add bot vào slot trống ở màn list bot; mở detail; thao tác thay đổi hợp đồng; "
       "áp bot free vào slot standard/pro\n"
       "2. Staff KHÔNG được phân quyền: kiểm tra hiển thị slot trống, mở URL add bot to slot, "
       "màn list hợp đồng, URL detail hợp đồng\n"
       "3. Staff ĐƯỢC phân quyền: kiểm tra 4 điểm tương tự",
       "Hợp đồng standard và pro; 3 vai trò",
       "- Owner: mọi thao tác cho phép, hiển thị đúng tên bot\n"
       "- Staff không quyền: không hiện slot trống của owner khác; URL add bot to slot và URL detail "
       "đều báo「この権限は許可されていません。」; màn list không hiện bot chưa được phân quyền\n"
       "- Staff có quyền: hiện được bot đã phân quyền, mở được detail, thao tác được; "
       "vẫn không hiện slot trống của owner khác và vẫn bị chặn URL add bot to slot",
       note="Nguồn: r292-r305 (Feature #37085 regression). Ghi 'regression'."),

    # ═════════════ 40. Môi trường & regression ═════════════
    tc("Môi trường & regression", "ENV-001", "Normal",
       "Giá plan trên PRODUCTION khác dev/staging → mọi TC tiền phải chạy trên PRODUCTION",
       "- Có quyền truy cập cả staging và PRODUCTION",
       "1. Trên staging: mở màn chọn plan, ghi lại giá standard/pro theo tháng và năm\n"
       "2. Trên PRODUCTION: làm tương tự\n3. So sánh",
       "standard tháng: dev/stg 4.500 vs PRODUCTION 10.780; standard năm 10%OFF: PRODUCTION 9.702/tháng",
       "- Giá 2 môi trường KHÁC nhau như dữ liệu test\n"
       "- Kết luận: mọi TC kiểm số tiền, hóa đơn, báo giá phải chạy trên PRODUCTION (RULE-08)",
       env="PRODUCTION",
       note="Nguồn: r38, r39, r59, r60 (ghi chú của tester:「dev và stg là 4050/4500」). Xem MT-06."),

    tc("Môi trường & regression", "ENV-002", "Normal",
       "3D Secure chỉ bật ở PRODUCTION → TC 3DS không kết luận được trên staging",
       "- Tài khoản UnivaPay trên staging và PRODUCTION",
       "1. Trên staging: thực hiện bill bằng thẻ có 3DS → quan sát có popup 3DS không\n"
       "2. Trên PRODUCTION: thực hiện tương tự",
       "Thẻ có 3D Secure",
       "- Staging: KHÔNG hiện popup 3DS (tài khoản staging chưa bật 3DS) → không kết luận được\n"
       "- PRODUCTION: hiện popup xác thực 3DS trước khi charge",
       env="PRODUCTION",
       note="Nguồn: tab「Bill tiền univapay: 3D secure」r3 (ghi chú:「trên staging acc bill tiền vẫn chưa "
            "có 3D => test job bill bình thường là được」)."),

    tc("Môi trường & regression", "DEPLOY-001", "Normal",
       "Kiểm tra lại toàn bộ luồng chính sau khi release lên branch release / staging",
       "- Branch release đã deploy lên staging",
       "1. Chạy lại bộ main case: mua mới (card/transfer) · upgrade · job bill · đổi kỳ · đổi phương thức · "
       "đổi thẻ · gia hạn · hủy · hợp đồng lại · tải hóa đơn\n"
       "2. Ghi kết quả từng luồng vào cột kết quả branch release",
       "10 luồng chính",
       "Cả 10 luồng đều PASS trên staging trước khi lên PRODUCTION; "
       "mọi kết quả NG phải có ticket bug tương ứng",
       note="Nguồn: tab「Check lịch sử hợp đồng」cột「Brach rls」và tab「Quản lý hợp đồng」các cột "
            "「bran release」/「Staging」. ⚠ Corpus ghi nhận 1 NG chưa rõ trạng thái ở "
            "「Mua mới slot: pro năm - bill transfer」(Check lịch sử hợp đồng r21) — xem MT-43."),

    tc("Môi trường & regression", "REG-003", "Normal",
       "Ma trận 27 modal lịch sử phải đúng sau MỌI đợt sửa hợp đồng",
       "- Bot có đủ 27 loại bản ghi lịch sử theo tab「Check lịch sử hợp đồng」",
       "1. Sau mỗi đợt release có sửa luồng hợp đồng, mở lần lượt 27 modal lịch sử\n"
       "2. Đối chiếu tiêu đề + các trường của từng modal với ma trận gốc\n"
       "3. Ghi nhận modal nào hiển thị thiếu trường",
       "27 loại lịch sử",
       "Cả 27 modal hiển thị đúng tiêu đề và đủ trường; không modal nào thiếu trường "
       "(đặc biệt お支払い期間, thông tin bot, thời gian extend)",
       note="Nguồn: tab「Check lịch sử hợp đồng」r2-r103. ⚠ Corpus đã ghi 3 điểm thiếu: "
            "「Modal này c đang thấy thiếu thông tin cột お支払い期間」(r10), 「Không get được thông tin "
            "thời gian extend」(r39), 「Không get được thông tin bot」(r40) — xem MT-19. Ghi 'regression'."),

    tc("Môi trường & regression", "REG-003", "Normal",
       "Regression sau khi sửa hiển thị ngày cưỡng chế hủy: kiểm cả overdue card và overdue transfer",
       "- 1 hợp đồng overdue bill CARD và 1 hợp đồng overdue bill TRANSFER",
       "1. Với từng hợp đồng: đọc ngày cưỡng chế hủy ở màn list\n"
       "2. Mở màn detail và đọc ngày cưỡng chế hủy\n3. So sánh 2 màn\n"
       "4. Kiểm tra thêm hợp đồng bill lỗi MAX FRIEND (overdueDate dùng cardBillMaxFriend)",
       "3 loại: overdue card, overdue transfer, bill lỗi max friend",
       "- Ngày cưỡng chế hủy ở màn list và màn detail GIỐNG NHAU ở cả 3 loại\n"
       "- Hợp đồng bill lỗi max friend không bị ảnh hưởng bởi thay đổi hàm overdueDate()",
       note="Nguồn: r1695-r1721 (Bug KH #37109, 05/06/2026). Ghi 'regression'."),

    tc("Môi trường & regression", "PERF-003", "Boundary",
       "Màn list hợp đồng với số lượng hợp đồng lớn",
       "- Tài khoản có ≥ 200 hợp đồng (đủ loại trạng thái)",
       "1. Mở /basic/point-settings và đo thời gian tải\n2. Chuyển phân trang 100\n"
       "3. Search theo keyword\n4. Mở modal sắp xếp",
       "≥ 200 hợp đồng",
       "- Trang tải xong trong ngưỡng chấp nhận được, không timeout\n"
       "- Phân trang, search và modal sắp xếp hoạt động đúng với dữ liệu lớn",
       env="PRODUCTION",
       note="Nguồn: corpus KHÔNG có TC hiệu năng cho màn list → TC do AI bổ sung theo PERF/RULE-08, "
            "CẦN LEADER XÁC NHẬN ngưỡng thời gian chấp nhận. Xem MT-21."),

    tc("Môi trường & regression", "COMPAT-LEGACY-003", "Normal",
       "Hợp đồng cũ (trước các đợt improve) vẫn hiển thị và thao tác đúng",
       "- Có hợp đồng tạo từ trước đợt improve 12/2024 và trước đợt 12/2025",
       "1. Mở màn list và màn detail của các hợp đồng cũ\n"
       "2. Kiểm tra các trường mới (bill_type_old, payment_method_old, last_four_card ở lịch sử)\n"
       "3. Thử thao tác đổi kỳ / đổi phương thức / tải hóa đơn",
       "Hợp đồng tạo 2024 và hợp đồng tạo trước 12/2025",
       "- Hiển thị đầy đủ, không lỗi do trường mới bị NULL\n"
       "- Thao tác đổi kỳ / đổi phương thức / tải hóa đơn đều hoạt động\n"
       "- Hóa đơn cũ tải được, hiển thị đúng dữ liệu tại thời điểm đó",
       note="Nguồn: r837, r849 (Check các hóa đơn cũ) + r1294-r1296 (Check recover). "
            "Ghi 'regression'."),
]
