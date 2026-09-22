# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 7-8.

S7 Quét QR & kiểm tra kết nối (màn QR + đếm ngược 3 phút + màn kết nối thất bại)
S8 Tiến trình đổi LOA & hoàn tất (progress bar + màn hoàn tất + màn chưa xác thực)

⚠️ Cả 2 nhóm đều chạm webhook / domain / job nền → RULE-08: KHÔNG kết luận từ staging.
⚠️ MT-01 — kiến trúc bản ghi bot sau khi đổi (tạo bản ghi mới is_delete=2 → 0 theo TCs
2026, vs UPDATE tại chỗ vào id bot cũ theo TCs 2023) CHƯA CHỐT. Mọi TC check DB trong
2 nhóm này viết theo nhánh "tạo bản ghi mới".
"""
from _common import tc

QR = ("- Đăng nhập Admin chủ (主管理者) của bot plan Standard trở lên\n"
      "- Đã qua bước nhập thông tin kết nối + webhook, đang ở màn quét QR / kiểm tra kết nối\n"
      "- Đã có bản ghi bots mới với is_delete = 2 (chưa có bot_contract / bot_slots)\n"
      "- Có điện thoại có LINE để quét QR")
PROG = ("- Đăng nhập Admin chủ của bot plan Standard trở lên\n"
        "- Đã quét QR và kết bạn thành công, tiến trình đổi LOA đang chạy\n"
        "- Bot cũ có sẵn dữ liệu ở nhiều tính năng (friend, tag, scenario, form, booking)")
MT01 = "⚠️ MT-01 — kiến trúc bản ghi bot chưa chốt. "

S7 = [
    # ═══════════════ 7. Quét QR & kiểm tra kết nối ═══════════════
    tc("Quét QR & kiểm tra kết nối", "FUNC-DATE-001", "Boundary",
       "Đồng hồ đếm ngược 3 phút chạy đúng, hết 3 phút tự mở màn kết nối thất bại",
       QR,
       "1. Vào màn quét QR, ghi lại thời điểm bắt đầu (theo đồng hồ thật)\n"
       "2. KHÔNG quét QR, chỉ quan sát đồng hồ đếm ngược\n"
       "3. Đối chiếu đồng hồ đếm ngược với đồng hồ thật ở mốc 2:00 và 1:00 còn lại\n"
       "4. Chờ đến khi hết 3 phút, quan sát màn hình\n"
       "5. Query DB bảng bots: bản ghi is_delete = 2 còn hay đã bị xóa",
       "Không quét QR, để hết 3 phút",
       "- Đồng hồ đếm ngược giảm đúng nhịp 1 giây/giây, lệch không quá 2 giây so với đồng hồ thật sau 3 phút\n"
       "- Hết 3 phút: tự động mở màn kết nối THẤT BẠI (không cần user bấm gì)\n"
       "- DB: bản ghi bots có is_delete = 2 vừa tạo bị XÓA\n"
       "- Không còn bản ghi rác nào của lần thử này",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r162 (TR=OK, stg=OK) + r166 + r309 + r313. RULE-07 + RULE-08 "
            "(job nền + domain). Evidence: 3 ảnh đồng hồ kèm giờ thật + ảnh màn fail + query bots trước/sau."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Abnormal",
       "User quét QR nhưng CHƯA bấm kết bạn → hết 3 phút vẫn thất bại, bản ghi bots bị xóa",
       QR,
       "1. Quét QR bằng LINE trên điện thoại\n"
       "2. Màn LINE mở ra trang LOA mới nhưng KHÔNG bấm nút kết bạn\n"
       "3. Quan sát màn web: có chuyển màn không\n"
       "4. Chờ hết 3 phút, quan sát màn web\n"
       "5. Query DB bảng bots",
       "Quét QR, không bấm kết bạn",
       "- Màn web VẪN ở màn quét QR trong suốt 3 phút, không nhảy sang thành công\n"
       "- Hết 3 phút: mở màn kết nối thất bại\n"
       "- DB: bản ghi bots is_delete = 2 bị xóa\n"
       "- LOA mới KHÔNG được kết nối vào L Message",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r163 (TR=OK, stg=OK) + r310. RULE-06 (verify ở cả LINE app) + RULE-08. "
            "Evidence: ảnh LINE app + ảnh màn web sau 3 phút + query bots."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Normal",
       "CÙNG provider + user CHƯA kết bạn + quét QR rồi kết bạn → kết nối thành công, DB cập nhật tên bot mới",
       QR + "\n- Messaging API channel và LINE Login channel CÙNG provider\n"
       "- User LINE dùng để quét CHƯA từng kết bạn với LOA mới",
       "1. Ghi lại bots.view_name và bots.updated_at trước khi quét\n"
       "2. Quét QR bằng LINE trên điện thoại\n"
       "3. Trên LINE: màn thêm bạn hiển thị → bấm kết bạn\n"
       "4. Quan sát màn web ngay sau khi kết bạn\n"
       "5. Query DB: bots (is_delete, view_name, updated_at, channel_id, line_id), bot_contract, bot_slots\n"
       "6. Vào màn list template / detail scenario, kiểm tra danh sách account gửi thử",
       "LOA mới cùng provider; user LINE chưa kết bạn",
       "- Trên LINE: hiển thị màn THÊM BẠN (không phải màn chat)\n"
       "- Web: nhảy sang màn kết nối THÀNH CÔNG\n"
       "- DB bots: is_delete đổi 2 → 0; view_name đổi sang tên LOA MỚI; updated_at được cập nhật\n"
       "- DB: thêm bản ghi mới ở bot_contract và bot_slots map với bot vừa tạo\n"
       "- User vừa quét được thêm vào danh sách account gửi thử (send test)",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r145 (TR=OK) + r165 (TR=OK, stg=OK) + r281 + r312. "
            "RULE-06 (output cuối trên LINE app) + RULE-07 (3 tầng) + RULE-08. "
            "Evidence: ảnh LINE app màn thêm bạn + ảnh màn web thành công + query 3 bảng trước/sau + "
            "ảnh danh sách send test."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Normal",
       "CÙNG provider + user ĐÃ kết bạn sẵn + quét QR → kết nối thành công, LINE mở màn chat",
       QR + "\n- Messaging API và LINE Login CÙNG provider\n"
       "- User LINE ĐÃ kết bạn với LOA mới từ trước (đã chuyển bản ghi bots cũ thành is_delete=1)",
       "1. Quét QR bằng LINE trên điện thoại\n"
       "2. Quan sát màn hiện ra trên LINE\n"
       "3. Quan sát màn web\n"
       "4. Query DB bảng bots, bot_contract, bot_slots\n"
       "5. Kiểm tra danh sách account gửi thử",
       "LOA mới cùng provider; user LINE đã là bạn sẵn",
       "- Trên LINE: hiển thị màn CHAT với bot (không phải màn thêm bạn)\n"
       "- Web: nhảy sang màn kết nối THÀNH CÔNG\n"
       "- DB bots: is_delete đổi 2 → 0; thêm bản ghi bot_contract + bot_slots\n"
       "- User được thêm vào danh sách account gửi thử",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r147 (TR=OK) + r283. So với TC cùng provider + chưa kết bạn: "
            "KHÁC nhau ở màn user thấy trên LINE (chat vs thêm bạn) nên tách TC riêng. "
            "RULE-06 + RULE-08. Evidence: ảnh LINE app màn chat + ảnh màn web + query DB."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Abnormal",
       "KHÁC provider + user chưa kết bạn + quét QR → LINE hiện màn thêm bạn/unblock, web vẫn treo rồi thất bại",
       QR + "\n- Messaging API channel và LINE Login channel KHÁC provider "
       "(tạo Messaging API mới khác provider của LINE Login)\n- User LINE chưa kết bạn với LOA mới",
       "1. Quét QR bằng LINE trên điện thoại\n"
       "2. Quan sát màn trên LINE và thao tác theo (thêm bạn / bỏ chặn)\n"
       "3. Quan sát màn web ngay sau đó\n"
       "4. Chờ hết 3 phút, quan sát màn web\n"
       "5. Query DB bảng bots",
       "Messaging API và LINE Login KHÁC provider; user chưa kết bạn",
       "- Trên LINE: ra màn thêm bạn, user bấm bỏ chặn/thêm bạn\n"
       "- Web: VẪN ở màn quét QR, KHÔNG nhảy sang thành công\n"
       "- Hết 3 phút: mở màn kết nối thất bại\n"
       "- DB: bản ghi bots is_delete = 2 bị xóa",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r142 (TR=OK) + r278. RULE-06 + RULE-08. "
            "Evidence: ảnh LINE app + ảnh màn web sau 3 phút + query bots."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Abnormal",
       "KHÁC provider + user ĐÃ kết bạn (dù quét hay không quét QR) → đều thất bại sau 3 phút",
       QR + "\n- Messaging API và LINE Login KHÁC provider\n"
       "- User LINE ĐÃ kết bạn với LOA mới (bản ghi bots cũ đã chuyển is_delete = 1)",
       "1. Trường hợp A: KHÔNG quét QR, user gửi tin nhắn cho bot → chờ hết 3 phút, quan sát web\n"
       "2. Làm lại flow từ đầu\n"
       "3. Trường hợp B: QUÉT QR → chờ hết 3 phút, quan sát web\n"
       "4. Query DB bảng bots sau mỗi trường hợp",
       "2 trường hợp cùng kết quả: (A) không quét QR + user gửi tin · (B) có quét QR",
       "- CẢ 2 trường hợp: web VẪN ở màn quét QR, hết 3 phút → màn kết nối thất bại\n"
       "- CẢ 2 trường hợp: DB bản ghi bots is_delete = 2 bị xóa\n"
       "- Kết bạn hay gửi tin của user KHÔNG làm kết nối thành công khi khác provider",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r143 + r144 (cả 2 TR=OK) + r279 + r280. GỘP 2 dòng nguồn vì "
            "kết quả mong đợi GIỐNG HỆT (chỉ khác có/không quét QR) — liệt kê đủ 2 điểm ở cột Dữ liệu nhập. "
            "RULE-08. Evidence: 2 ảnh màn web sau 3 phút + 2 lần query bots."),

    tc("Quét QR & kiểm tra kết nối", "INTG-LINE-001", "Abnormal",
       "CÙNG provider + user ĐÃ kết bạn + KHÔNG quét QR, chỉ gửi tin nhắn → vẫn thất bại sau 3 phút",
       QR + "\n- Messaging API và LINE Login CÙNG provider\n- User LINE đã kết bạn với LOA mới",
       "1. KHÔNG quét QR code\n"
       "2. Trên LINE, user gửi tin nhắn bất kỳ cho LOA mới\n"
       "3. Quan sát màn web\n"
       "4. Chờ hết 3 phút, quan sát màn web\n"
       "5. Query DB bảng bots",
       "Cùng provider; đã kết bạn; chỉ gửi tin, không quét QR",
       "- Web VẪN ở màn quét QR dù user đã gửi tin\n"
       "- Hết 3 phút: mở màn kết nối thất bại\n"
       "- DB: bản ghi bots is_delete = 2 bị xóa\n"
       "- Kết luận: phải QUÉT QR mới xác nhận được kết nối, gửi tin không thay thế được",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r146 (TR=OK) + r282. RULE-08. "
            "Evidence: ảnh tin nhắn trên LINE + ảnh màn web sau 3 phút + query bots."),

    tc("Quét QR & kiểm tra kết nối", "FUNC-DATE-001", "Boundary",
       "Quét QR SÁT mốc hết 3 phút → màn thất bại hiển thị ngay dù vừa kết bạn xong",
       QR,
       "1. Chờ đồng hồ đếm ngược còn ~5 giây\n"
       "2. Quét QR và bấm kết bạn thật nhanh để hoàn tất ở mốc ~0 giây\n"
       "3. Quan sát màn web ngay sau khi kết bạn\n"
       "4. Query DB bảng bots: bản ghi is_delete=2 bị xóa hay chuyển 0",
       "Quét QR + kết bạn ở mốc còn ~5 giây",
       "- Web hiển thị màn kết nối THẤT BẠI (dù user vừa kết bạn xong)\n"
       "- DB: ghi nhận trạng thái thật của bản ghi bots — nếu vừa chuyển 0 vừa hiện màn fail thì là "
       "BẤT NHẤT giữa DB và UI, phải raise bug\n"
       "- Không được để bot ở trạng thái nửa vời (is_delete = 2 tồn tại mãi)",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r188 (TR=OK, stg=OK: 'sát tới giờ hết 3p => quét qr kết bạn, "
            "lúc quét qr xong hiển thị luôn màn hình failse'). Đây là case biên race giữa đếm ngược và "
            "callback kết bạn. RULE-07 — bắt buộc đối chiếu DB vì UI nói fail. "
            "Evidence: video quay màn web + giờ + query bots ngay sau đó."),

    tc("Quét QR & kiểm tra kết nối", "UI-001", "Normal",
       "Màn kết nối thất bại hiển thị đúng giao diện và 2 nút hành động",
       QR + "\n- Đã để hết 3 phút để vào màn kết nối thất bại",
       "1. Để hết 3 phút, vào màn kết nối thất bại\n"
       "2. Quan sát toàn bộ giao diện, đối chiếu với design\n"
       "3. Tìm nút「ステップ1に戻って再設定」và nút「有料の接続サポートを申し込む」\n"
       "4. Quan sát ở độ phân giải 1366×768 xem có bị cắt không",
       "Độ phân giải 1366×768",
       "- Giao diện hiển thị đúng như design (bản gần nhất)\n"
       "- Có đủ 2 nút:「ステップ1に戻って再設定」và「有料の接続サポートを申し込む」\n"
       "- Không bị cắt/vỡ layout ở 1366×768\n"
       "- Có thông điệp giải thích tại sao thất bại",
       note="Nguồn: Change bot r167 (TR=OK) + r314. ⚠️ Ghi chú nguồn: 'màn kết nối thất bại (chưa có "
            "design mới), tạm thời lấy theo bản gần nhất' → design CHƯA CHỐT, không assert pixel. "
            "Evidence: ảnh full màn ở 1366×768."),

    tc("Quét QR & kiểm tra kết nối", "FUNC-001", "Normal",
       "Màn thất bại — bấm「ステップ1に戻って再設定」→ về bước đầu của wizard",
       QR + "\n- Đang ở màn kết nối thất bại",
       "1. Ở màn kết nối thất bại, bấm nút「ステップ1に戻って再設定」\n"
       "2. Quan sát màn hình đích\n"
       "3. Kiểm tra 4 field thông tin kết nối có còn giá trị cũ không",
       "Bot Standard",
       "- Quay về bước 1 của wizard\n"
       "- Ghi nhận 4 field: còn giá trị cũ hay trống (nguồn không nói rõ)\n"
       "- Không lỗi JS, không trang trắng",
       note="Nguồn: Change bot r168 (TR=OK) + r315. ⚠️ Nguồn KHÔNG nói rõ 4 field có được giữ hay không → "
            "cần Leader chốt. Đối chiếu: AddBot/Bug Logic r27 ghi 'change bot fail sau đấy change lại thì "
            "từ màn 2 nhảy đến màn QR luôn' (BUG đã Fixed) với expected 'phải từng bước một theo quy trình, "
            "những thông tin trước đó đã nhập vẫn được giữ lại, user có thể edit' → nghiêng về GIỮ lại. "
            "Evidence: ảnh màn đích + ảnh 4 field.",
       spec="Đã hỏi leader"),

    tc("Quét QR & kiểm tra kết nối", "FUNC-SEQ-001", "Abnormal",
       "Sau khi thất bại và quay lại bước 1, wizard phải đi TỪNG BƯỚC, không nhảy thẳng tới màn QR",
       QR + "\n- Đã thất bại 1 lần và bấm「ステップ1に戻って再設定」",
       "1. Thất bại 1 lần, bấm quay về bước 1\n"
       "2. Sửa lại thông tin kết nối cho hợp lệ\n"
       "3. Bấm sang bước tiếp và ĐẾM số màn phải đi qua trước khi tới màn QR\n"
       "4. Đối chiếu với số màn của lần chạy đầu tiên",
       "Lần 2 sau khi fail",
       "- Số màn phải đi qua GIỐNG lần đầu (không bị nhảy tắt từ màn 2 sang màn QR)\n"
       "- Mỗi bước vẫn validate như lần đầu\n"
       "- Thông tin đã nhập trước đó cho phép user EDIT lại",
       note="Nguồn: AddBot/Bug Logic r27 (bug đã Fixed + OK: 'change bot fail sau đấy change lại thì từ màn 2 "
            "nhảy đến màn QR luôn' → expected 'phải từng bước một theo quy trình'). "
            "RULE-12 mục (3): mọi case đã từng Không đạt và được fix phải nằm trong bộ regression. "
            "Evidence: ảnh từng màn của lần 2 + đếm số màn."),

    tc("Quét QR & kiểm tra kết nối", "FUNC-001", "Normal",
       "Sau khi back về bước 1, nhập lại thông tin HỢP LỆ → tạo lại bản ghi bots và kết nối thành công",
       QR + "\n- Đã thất bại 1 lần, đã quay về bước 1\n- Có LOA mới hợp lệ (cùng provider)",
       "1. Sau khi fail, quay về bước 1\n"
       "2. Nhập lại 4 field hợp lệ, đi hết các bước tới màn QR\n"
       "3. Query DB bảng bots ngay sau khi màn QR hiển thị\n"
       "4. Quét QR và kết bạn\n"
       "5. Query lại DB bots, bot_contract, bot_slots",
       "LOA mới hợp lệ, cùng provider",
       "- Ở màn QR lần 2: DB có bản ghi bots MỚI với is_delete = 2 (bản ghi lần 1 đã bị xóa)\n"
       "- Sau khi kết bạn: web mở màn kết nối THÀNH CÔNG\n"
       "- DB bots: is_delete đổi 2 → 0\n"
       "- DB: thêm bản ghi bot_contract và bot_slots map với bot vừa tạo\n"
       "- KHÔNG còn bản ghi rác của lần thất bại",
       env="PRODUCTION",
       note=MT01 + "Nguồn: Change bot r170 (TR=OK) + r317. RULE-07 + RULE-08. "
            "Evidence: query bots 3 thời điểm (trước/ở màn QR/sau kết bạn) + ảnh màn thành công."),

    tc("Quét QR & kiểm tra kết nối", "UI-001", "Normal",
       "Màn thất bại — bấm「有料の接続サポートを申し込む」mở tab mới tới đúng landing hỗ trợ",
       QR + "\n- Đang ở màn kết nối thất bại",
       "1. Bấm nút「有料の接続サポートを申し込む」1 lần\n"
       "2. Quan sát tab mới và URL\n"
       "3. Quay lại, bấm 2 lần nhanh liên tiếp, đếm số tab mở ra",
       "Bot Standard",
       "- Mở TAB MỚI tới https://go.lmes.jp/landing-qr/1656886828-yoaLLZlp?uLand=YysU16\n"
       "- Tab hiện tại (màn thất bại) KHÔNG bị thay thế\n"
       "- Bấm 2 lần nhanh chỉ mở ĐÚNG 1 tab",
       note="Nguồn: Change bot r169 (TR=OK) + r316. ⚠️ URL landing là URL cố định trong TC gốc — "
            "nếu marketing đổi landing thì TC này phải cập nhật. Evidence: ảnh tab mới + URL."),

    tc("Quét QR & kiểm tra kết nối", "UI-001", "Normal",
       "Các link phụ trên màn QR mở đúng, double-click không mở 2 tab",
       QR,
       "1. Bấm「設定動画をスマホで見る」→ quan sát\n"
       "2. Quay lại, bấm「サポートに問い合わせ」→ quan sát URL tab mới\n"
       "3. Bấm chữ quay lại bước trước → quan sát màn đích\n"
       "4. Với từng link, bấm 2 lần nhanh và đếm số tab",
       "3 link phụ trên màn QR",
       "-「設定動画をスマホで見る」→ hiển thị ảnh QR code, quét được để xem video\n"
       "-「サポートに問い合わせ」→ mở tab mới https://app.chatplus.jp/chat/visitor/e3f8121b_1?t=btn\n"
       "- Chữ quay lại bước trước → về đúng bước webhook\n"
       "- Mỗi link bấm 2 lần nhanh chỉ mở ĐÚNG 1 tab",
       note="Nguồn: Change bot r159-r161 (TR=OK) + r306-r308. Evidence: ảnh 3 kết quả + URL."),

    tc("Quét QR & kiểm tra kết nối", "UI-001", "Normal",
       "Video hướng dẫn trên màn QR phát được, popup video đóng đúng cách",
       QR,
       "1. Bấm mở video hướng dẫn trên màn QR\n"
       "2. Quan sát video có phát được không\n"
       "3. Bấm nút × của popup video → quan sát\n"
       "4. Mở lại video, bấm ra vùng ngoài popup → quan sát\n"
       "5. Quét mã QR video bằng LINE và bằng camera điện thoại",
       "Video hướng dẫn + QR video",
       "- Video mở và phát được, không lỗi không tải\n"
       "- Bấm ×: popup video đóng, quay lại màn QR, đồng hồ đếm ngược VẪN chạy đúng (không reset)\n"
       "- Bấm ra ngoài popup: ghi nhận hành vi thật (đóng / không đóng)\n"
       "- Quét mã bằng LINE và bằng camera điện thoại đều xem được video",
       note="Nguồn: Change bot r158 + r305 (check video) + r181-r183 (màn 4 — 'khi click btn X?' và "
            "'khi click ra ngoài popup?' để TRỐNG expected → đây là điểm nguồn CHỈ CÓ TIÊU ĐỀ, "
            "expected do AI tự viết, cần Leader xác nhận) + r109/r118/r139. "
            "Điểm bổ sung của AI: kiểm đồng hồ đếm ngược không reset khi đóng video. "
            "Evidence: video thao tác + ảnh popup.",
       spec="Đã hỏi leader"),

    tc("Quét QR & kiểm tra kết nối", "FUNC-UNIQ-001", "Abnormal",
       "2 bot cùng nhập 1 Messaging API để đổi LOA → bot thứ 2 bị chặn vì đang xử lý",
       ("- Đăng nhập Admin có 2 bot A và B (đều plan Standard)\n"
        "- Có 1 LOA mới duy nhất (1 Messaging API channel)"),
       "1. Với bot A: chạy flow đổi LOA với Messaging API channel X đến khi đang xử lý\n"
       "2. Giữ nguyên tiến trình bot A (chưa hoàn tất)\n"
       "3. Mở tab khác, với bot B: chạy flow đổi LOA, nhập CÙNG Messaging API channel X\n"
       "4. Quan sát thông báo lỗi ở bot B\n"
       "5. Query DB: schedule_change_bots + bots xem có bản ghi trùng channel X không",
       "Cùng 1 Messaging API channel X cho bot A và bot B",
       "- Bot B bị chặn, hiển thị message「LOA変更処理中のため、変更できません。処理完了後に再度お試しください。」\n"
       "- DB: KHÔNG có 2 bản ghi cùng trỏ vào channel X\n"
       "- Tiến trình của bot A KHÔNG bị ảnh hưởng, vẫn chạy bình thường",
       env="PRODUCTION",
       note="Nguồn: Change bot r187 (TR=OK, stg=OK) + TC-CBF-060 (CONC-001, TD EP-06 error "
            "`SWAP_ALREADY_IN_PROGRESS`; Blocked cả 2 env). RULE-07 + RULE-08. "
            "Evidence: ảnh message ở bot B + query DB + ảnh tiến trình bot A."),

    tc("Quét QR & kiểm tra kết nối", "CONC-001", "Boundary",
       "Mở 2 tab cùng cố đổi LOA cho CÙNG 1 bot → chỉ 1 tiến trình chạy, tab còn lại bị chặn",
       ("- Đăng nhập Admin chủ bot Standard\n"
        "- Mở 2 tab trình duyệt cùng session, cùng bot"),
       "1. Tab A: chạy flow đổi LOA tới màn xác nhận\n"
       "2. Tab B: chạy flow đổi LOA cho CÙNG bot đó, cũng tới màn xác nhận\n"
       "3. Ở tab A bấm nút thực hiện đổi LOA\n"
       "4. Ngay sau đó ở tab B cũng bấm nút thực hiện\n"
       "5. Quan sát tab B + query DB đếm số tiến trình / bản ghi bots is_delete=2",
       "2 tab cùng session, cùng bot",
       "- Tab A: tiến trình đổi LOA khởi động bình thường\n"
       "- Tab B: bị chặn bằng thông báo lỗi (đang xử lý), KHÔNG khởi động tiến trình thứ 2\n"
       "- DB: ĐÚNG 1 tiến trình / 1 bản ghi bots is_delete=2, không có bản ghi trùng\n"
       "- Bên LINE: không tạo thêm LIFF app lần 2",
       env="PRODUCTION",
       note=MT01 + "Nguồn: TC-CBF-060 (CONC-001, EP-06 `SWAP_ALREADY_IN_PROGRESS`; Blocked cả 2 env). "
            "CONC-001 BẮT BUỘC. RULE-07 + RULE-08. Evidence: ảnh 2 tab + query DB + ảnh LIFF list."),
]

S8 = [
    # ═══════════════ 8. Tiến trình đổi LOA & hoàn tất ═══════════════
    tc("Tiến trình đổi LOA & hoàn tất", "UI-003", "Normal",
       "Modal tiến trình hiển thị % hoàn thành và cập nhật liên tục",
       PROG,
       "1. Ngay sau khi quét QR + kết bạn thành công, quan sát màn hình\n"
       "2. Ghi lại % hiển thị ở 3 thời điểm cách nhau 10 giây\n"
       "3. Mở DevTools tab Network, quan sát request lấy tiến độ\n"
       "4. Quan sát % có lùi ngược hay nhảy quá 100 không",
       "Bot cũ có nhiều dữ liệu để tiến trình chạy đủ lâu quan sát",
       "- Hiển thị modal/màn tiến trình có thanh % hoàn thành\n"
       "- % tăng dần theo thời gian, KHÔNG lùi ngược, KHÔNG vượt 100\n"
       "- Network: có request lấy tiến độ lặp lại theo chu kỳ (HTTP polling)\n"
       "- Thanh tiến trình chuyển động mượt, không giật khi cập nhật",
       env="PRODUCTION",
       note="Nguồn: Change bot r189 (TR=OK, stg=OK) + TC-CBF-054 (UI-003, BR-24/FN-14, QA-spec-014 "
            "CONFIRMED 'HTTP polling'; Blocked cả 2 env) + TC-CBF-110 (animation mượt). RULE-08 (job nền). "
            "Evidence: 3 ảnh % kèm giờ + ảnh Network polling."),

    tc("Tiến trình đổi LOA & hoàn tất", "STATE-001", "Normal",
       "Trong lúc đang đổi LOA — sidebar và header bị ẩn hoàn toàn, không điều hướng được",
       PROG,
       "1. Trong lúc tiến trình đang chạy, quan sát sidebar bên trái\n"
       "2. Quan sát header phía trên\n"
       "3. Thử bấm nút Back của trình duyệt\n"
       "4. Thử sửa URL sang /basic/overview và Enter",
       "Tiến trình đang ở ~50%",
       "- Sidebar bị ẩn hoàn toàn, không thấy mục menu nào\n"
       "- Header bị ẩn, không có link điều hướng\n"
       "- Bấm Back: không ra khỏi màn tiến trình (hoặc bị đẩy lại vào màn tiến trình)\n"
       "- Sửa URL sang màn khác: bị điều hướng trở lại màn tiến trình",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-055 (STATE-001, BR-22; Pass dev, Blocked staging). "
            "RULE-08. Evidence: ảnh full màn lúc đang chạy + ảnh sau khi thử Back/sửa URL."),

    tc("Tiến trình đổi LOA & hoàn tất", "CONC-001", "Boundary",
       "Bot bị khóa trong lúc đổi LOA — thao tác ghi khác trên bot bị chặn",
       PROG + "\n- Mở thêm 1 tab để thao tác ghi trên cùng bot",
       "1. Trong lúc tiến trình đang chạy, mở tab mới\n"
       "2. Thử tạo 1 tag mới cho bot đó\n"
       "3. Thử gửi 1 tin nhắn ở chat 1:1\n"
       "4. Thử lưu thay đổi ở màn「LOA接続設定」\n"
       "5. Với mỗi thao tác, ghi lại phản hồi của hệ thống và kiểm tra DB",
       "3 thao tác ghi: tạo tag · gửi tin chat 1:1 · lưu bot-edit",
       "- CẢ 3 thao tác ghi đều bị CHẶN với thông báo rõ ràng (đang xử lý đổi LOA)\n"
       "- DB: không có tag mới / tin nhắn mới / thay đổi bot nào được ghi\n"
       "- Không thao tác nào gây lỗi 500 hay treo trang",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-056 (CONC-001, BR-23 + QA-dev-012; Blocked cả 2 env). "
            "⏳ QA-dev-006 (P0) — DANH SÁCH feature bị block cụ thể CHƯA CHỐT → 3 thao tác trên là "
            "AI tự chọn làm đại diện, cần Leader chốt danh sách đầy đủ. RULE-07 + RULE-08. "
            "Evidence: 3 ảnh thông báo + query DB 3 bảng.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "OUT-TRUTH-001", "Boundary",
       "Tin chào mừng và phát hành theo bước trong lúc đang đổi LOA — ghi nhận hành vi thật",
       PROG + "\n- Bot có tin chào mừng đang bật và ≥1 scenario đang chạy\n"
       "- Có 1 user LINE chưa kết bạn để test kết bạn trong lúc đổi LOA",
       "1. Trong lúc tiến trình đang chạy, cho 1 user LINE kết bạn với bot\n"
       "2. Quan sát user có nhận được tin chào mừng không\n"
       "3. Kiểm tra scenario đang chạy có gửi bước tiếp theo trong lúc này không\n"
       "4. Sau khi tiến trình hoàn tất, kiểm tra lại trạng thái user đó + scenario",
       "1 user LINE kết bạn trong lúc đang đổi LOA",
       "- GHI NHẬN hành vi thật: user nhận / không nhận tin chào mừng\n"
       "- GHI NHẬN scenario có gửi tiếp / bị dừng\n"
       "- Bất kể kết quả nào: KHÔNG được gửi tin trùng lặp, KHÔNG gửi tin cho friend đã bị xóa\n"
       "- Sau khi hoàn tất, trạng thái user và scenario phải nhất quán với kết quả ghi nhận",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-057 (OUT-TRUTH-001, BR-26; Blocked cả 2 env). ⏳ Ghi chú nguồn: "
            "'Mâu thuẫn nội bộ TD (CM-003) — KHÔNG assert cứng, chỉ verify + báo cáo' → TC này để "
            "GHI NHẬN, cần Leader chốt expected. RULE-06 (verify trên LINE app) + RULE-08. "
            "Evidence: ảnh LINE app của user + log scenario.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "STATE-001", "Boundary",
       "Đóng tab/trình duyệt khi đang đổi LOA → tiến trình VẪN hoàn tất, vào lại thấy đúng kết quả",
       PROG,
       "1. Khi tiến trình ở ~30%, đóng hẳn tab trình duyệt\n"
       "2. Chờ 10 phút\n"
       "3. Mở lại trình duyệt, đăng nhập và vào bot đó\n"
       "4. Quan sát màn hiện ra (màn tiến trình tiếp tục / màn hoàn tất / dashboard bot mới)\n"
       "5. Query DB bảng bots + kiểm tra dữ liệu bot cũ đã bị xóa chưa",
       "Đóng tab ở ~30%, chờ 10 phút",
       "- Tiến trình đổi LOA VẪN chạy nền và hoàn tất, KHÔNG bị hủy\n"
       "- Vào lại: thấy đúng trạng thái hiện tại (tiếp tục tiến trình ở đúng % hoặc đã hoàn tất)\n"
       "- DB bots: is_delete = 0, thông tin LOA mới đã áp dụng\n"
       "- Dữ liệu bot cũ đã được xóa theo đúng danh sách bảng",
       env="PRODUCTION",
       note="Nguồn: Change bot r223 ('Trong quá trình web đang loading chuyển bot thì user tắt màn hình "
            "trình duyệt → Job vẫn tiếp tục hoàn tất thủ tục chuyển bot; khi user vào lại thì data được "
            "chuyển sang bot mới'; ghi chú gốc 'Confirm case này với a Tư trước khi test') + TC-CBF-058 "
            "(STATE-001; Pass dev). ⏳ QA-spec-015/QA-dev-015 — TA đề xuất nhưng CHƯA CONFIRMED. "
            "RULE-08 (job nền → PRODUCTION). Evidence: ảnh màn khi vào lại + query bots + query các bảng đã xóa.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "STATE-001", "Abnormal",
       "Ngắt mạng giữa lúc đang đổi LOA → khi có mạng lại, trạng thái KHÔNG nửa vời",
       PROG + "\n- Có thể ngắt mạng máy client",
       "1. Khi tiến trình ở ~50%, ngắt mạng máy client hoàn toàn\n"
       "2. Chờ 3 phút\n"
       "3. Bật mạng lại, reload trang\n"
       "4. Quan sát trạng thái tiến trình\n"
       "5. Query DB: bots, bot_contract, bot_slots + các bảng dữ liệu bot cũ",
       "Ngắt mạng client 3 phút ở mốc 50%",
       "- Khi có mạng lại: trạng thái rõ ràng — HOẶC tiếp tục/đã hoàn tất, HOẶC báo lỗi và rollback sạch\n"
       "- TUYỆT ĐỐI KHÔNG ở trạng thái nửa vời: bot mới is_delete=0 nhưng dữ liệu bot cũ mới xóa một phần\n"
       "- DB: bot_contract và bot_slots nhất quán với trạng thái bots\n"
       "- Nếu rollback: không để lại bản ghi bots is_delete=2 rác",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-059 (STATE-001; Blocked cả 2 env). ⏳ QA-spec-017 / QA-dev-005 (P0) — "
            "CHIẾN LƯỢC ROLLBACK CHƯA CHỐT. Đây là GAP P0: nếu không có rollback thì mọi lỗi giữa chừng "
            "đều để lại dữ liệu nửa vời. RULE-08. Evidence: query 5+ bảng sau khi có mạng lại.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "STATE-001", "Abnormal",
       "Tiến trình đổi LOA FAIL giữa chừng → báo lỗi rõ ràng, KHÔNG báo thành công giả",
       PROG + "\n- Có thể gây lỗi giữa tiến trình (chặn LINE API / tắt job nền)",
       "1. Khi tiến trình ở ~50%, gây lỗi (chặn domain LINE API hoặc dừng job nền)\n"
       "2. Quan sát màn tiến trình\n"
       "3. Chờ tới ngưỡng timeout\n"
       "4. Query DB: bots + các bảng dữ liệu bot cũ\n"
       "5. Kiểm tra bot có bị khóa vĩnh viễn không (thử thao tác ghi sau đó)",
       "Chặn LINE API ở mốc 50%",
       "- Màn tiến trình hiển thị LỖI rõ ràng, nêu được là đổi LOA không thành công\n"
       "- TUYỆT ĐỐI KHÔNG nhảy sang màn hoàn tất / không hiện 100%\n"
       "- Bot được MỞ KHÓA sau khi fail (thao tác ghi khác dùng lại được)\n"
       "- DB nhất quán: hoặc rollback sạch, hoặc trạng thái lỗi được ghi rõ",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-066 (STATE-001; Blocked cả 2 env) + TC-CBF-067 (UI-003, LINE API downtime → "
            "'không đứng màn hình trắng'). ⏳ QA-spec-017 (P0) / QA-dev-005 (P0) CHƯA CHỐT. "
            "UI-003 nâng Cao vì có rủi ro false-success. RULE-08. Evidence: ảnh màn lỗi + query DB.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "CONC-001", "Boundary",
       "Tiến trình chạy quá ngưỡng timeout → tự đánh dấu thất bại, mở khóa bot, thông báo cho Admin",
       PROG + "\n- Biết ngưỡng timeout mà Leader chốt (spec ghi 1 giờ, TA đề xuất 15 phút)",
       "1. Tạo tình huống tiến trình treo (chặn job nền)\n"
       "2. Ghi lại thời điểm bắt đầu\n"
       "3. Chờ tới đúng ngưỡng timeout đã chốt + 1 phút\n"
       "4. Quan sát màn hình và trạng thái bot\n"
       "5. Thử thao tác ghi trên bot (tạo tag) để xác nhận đã mở khóa",
       "Ngưỡng timeout theo quyết định của Leader (1 giờ hoặc 15 phút)",
       "- Đúng sau ngưỡng timeout: tiến trình tự chuyển sang trạng thái THẤT BẠI\n"
       "- Bot được mở khóa: tạo tag thành công\n"
       "- Admin nhận được thông báo về việc đổi LOA thất bại\n"
       "- Không treo vô hạn ở màn tiến trình",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-068 (CONC-001; Blocked cả 2 env). ⏳ QA-dev-001 (P0) — NGƯỠNG THỜI GIAN "
            "CHÍNH XÁC CHƯA CHỐT: spec ghi 1 giờ, TA đề xuất 15 phút. Phải chốt trước khi chạy TC này. "
            "RULE-08. Evidence: ảnh màn + giờ bắt đầu/kết thúc + ảnh thông báo cho Admin.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "FUNC-001", "Normal",
       "Tiến trình đạt 100% → tự chuyển màn hoàn tất, hiển thị đúng thông tin bot MỚI",
       PROG,
       "1. Chờ tiến trình chạy tới 100%\n"
       "2. Quan sát màn hình có tự chuyển không (không bấm gì)\n"
       "3. Đối chiếu tên bot / ảnh / LINE ID trên màn hoàn tất với LOA mới bên LINE\n"
       "4. Đọc text thông báo hoàn tất",
       "Tiến trình hoàn tất bình thường",
       "- Ở 100%, màn TỰ chuyển sang màn hoàn tất, không cần user bấm\n"
       "- Hiển thị thông tin bot MỚI (tên, ảnh, LINE ID của LOA mới), không phải bot cũ\n"
       "- Text hoàn tất đúng「LINE公式アカウントの入れ替えが完了しました」\n"
       "- Có nút「閉じる」",
       env="PRODUCTION",
       note="Nguồn: Change bot r190 (TR=OK, stg=OK) + TC-CBF-061 (BR-25/BR-29; Blocked cả 2 env) + "
            "TC-CBF-062 (OUT-TRUTH-001, BR-31, QA-spec-018 CONFIRMED text hoàn tất). RULE-08. "
            "Evidence: ảnh màn hoàn tất + ảnh LINE OA Manager của LOA mới."),

    tc("Tiến trình đổi LOA & hoàn tất", "FUNC-001", "Normal",
       "Đóng màn hoàn tất → về dashboard của bot MỚI, sidebar/header cập nhật tên bot mới",
       PROG + "\n- Đang ở màn hoàn tất",
       "1. Ở màn hoàn tất, bấm nút「閉じる」\n"
       "2. Quan sát URL đích\n"
       "3. Quan sát tên bot hiển thị ở header và sidebar\n"
       "4. Lặp lại bằng cách bấm × (nếu có) và đối chiếu",
       "Bot mới đã kết nối",
       "- Đóng modal/màn, chuyển về dashboard (màn home) của bot\n"
       "- Sidebar và header hiển thị đã quay lại (không còn bị ẩn như lúc đang xử lý)\n"
       "- Tên bot ở header/sidebar là tên LOA MỚI, không còn tên LOA cũ\n"
       "- Bấm × cho kết quả giống bấm「閉じる」",
       env="PRODUCTION",
       note="Nguồn: Change bot r190 ('click btn 閉じる: đóng modal, về màn home') + TC-CBF-063 (BR-30; "
            "Blocked cả 2 env). ⏳ QA-spec-026 — TRANG ĐÍCH cụ thể sau khi đóng CHƯA CHỐT (màn home "
            "hay dashboard bot). RULE-08. Evidence: URL đích + ảnh header/sidebar.",
       spec="Đã hỏi leader"),

    tc("Tiến trình đổi LOA & hoàn tất", "FUNC-001", "Normal",
       "Màn hoàn tất — bot MỚI đã xác thực (認証済み) → đi tiếp sang màn hướng dẫn",
       PROG + "\n- LOA mới ở trạng thái ĐÃ xác thực (認証済みアカウント) bên LINE",
       "1. Hoàn tất đổi LOA với LOA mới đã xác thực\n"
       "2. Ở màn hoàn tất, bấm nút「エルメの設定に進む」\n"
       "3. Quan sát màn đích\n"
       "4. Bấm 2 lần nhanh vào nút đó, đếm số lần chuyển màn",
       "LOA mới = 認証済みアカウント",
       "- Chuyển sang màn hướng dẫn (manual) — KHÔNG qua màn cảnh báo chưa xác thực\n"
       "- Bấm 2 lần nhanh chỉ chuyển màn 1 lần\n"
       "- Màn hướng dẫn có nút quay lại ở góc trên trái",
       note="Nguồn: Change bot r171 (cột kết quả TRỐNG — chưa chạy). ⚠️ RISK: nhánh bot đã xác thực "
            "chưa được chạy ở nguồn nào. Evidence: ảnh màn đích."),

    tc("Tiến trình đổi LOA & hoàn tất", "FUNC-001", "Normal",
       "Màn hoàn tất — bot MỚI CHƯA xác thực (未認証) → qua màn cảnh báo chưa xác thực trước",
       PROG + "\n- LOA mới ở trạng thái CHƯA xác thực (未認証アカウント) bên LINE",
       "1. Hoàn tất đổi LOA với LOA mới CHƯA xác thực\n"
       "2. Ở màn hoàn tất, bấm「エルメの設定に進む」\n"
       "3. Quan sát màn đích\n"
       "4. Đối chiếu tên LOA hiển thị trên màn đó với bots.view_name\n"
       "5. Bấm「動画の内容を理解したので エルメの設定に進む」và quan sát",
       "LOA mới = 未認証アカウント",
       "- Chuyển sang màn CẢNH BÁO chưa xác thực (không đi thẳng màn hướng dẫn)\n"
       "- Màn đó hiển thị đúng view_name của bot mới\n"
       "- Có video giải thích + link「関連マニュアル：既存友だち追加方法」+ link「未認証アカウント」\n"
       "- Bấm「動画の内容を理解したので エルメの設定に進む」→ sang màn hướng dẫn",
       note="Nguồn: Change bot r172-r177 (cột kết quả TRỐNG toàn bộ — chưa chạy). "
            "⚠️ RISK: cả nhánh 未認証 chưa được chạy. Link「未認証アカウント」→ "
            "https://www.lycbiz.com/jp/column/line-official-account/technique/20190726/ (r176). "
            "Evidence: ảnh màn cảnh báo + ảnh 3 link + query bots.view_name."),

    tc("Tiến trình đổi LOA & hoàn tất", "UI-001", "Normal",
       "Nút quay lại ở góc trên trái của màn cảnh báo / màn hướng dẫn → về màn admin/home",
       PROG + "\n- Đang ở màn cảnh báo chưa xác thực hoặc màn hướng dẫn",
       "1. Ở màn cảnh báo chưa xác thực, bấm nút quay lại góc trên bên trái\n"
       "2. Quan sát URL đích\n"
       "3. Làm lại tới màn hướng dẫn, bấm nút quay lại góc trên trái\n"
       "4. Quan sát URL đích",
       "2 màn: cảnh báo chưa xác thực và màn hướng dẫn",
       "- CẢ 2 màn: bấm quay lại → về /admin/home\n"
       "- Không về màn tiến trình hay màn hoàn tất\n"
       "- Bot mới vẫn ở trạng thái đã kết nối (không bị hủy)",
       note="Nguồn: Change bot r178-r179 (cột kết quả TRỐNG — chưa chạy). ⚠️ RISK chưa chạy. "
            "Evidence: 2 URL đích + query bots."),

    tc("Tiến trình đổi LOA & hoàn tất", "PERM-001", "Normal",
       "Tài khoản Staff KHÔNG bị ảnh hưởng sau khi đổi LOA — giữ nguyên quyền truy cập",
       PROG + "\n- Bot cũ có ≥2 tài khoản Staff với quyền truy cập khác nhau (đã cấp một số màn)\n"
       "- Đã ghi lại danh sách màn mà từng Staff được truy cập TRƯỚC khi đổi LOA",
       "1. Ghi lại ma trận quyền của từng Staff trước khi đổi LOA\n"
       "2. Hoàn tất đổi LOA\n"
       "3. Đăng nhập bằng từng tài khoản Staff\n"
       "4. Đối chiếu danh sách màn truy cập được với ma trận đã ghi ở bước 1\n"
       "5. Kiểm tra Staff vẫn thấy đúng bot (không bị mất bot khỏi danh sách)",
       "≥2 Staff với quyền khác nhau",
       "- Từng Staff đăng nhập được bình thường\n"
       "- Danh sách màn truy cập được KHỚP HOÀN TOÀN với ma trận trước khi đổi LOA\n"
       "- Bot vẫn nằm trong danh sách bot của Staff\n"
       "- Không Staff nào bị thêm/mất quyền",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-064 (PERM-001, BR-46/FN-18, QA-spec-023 CONFIRMED 'Staff users KHÔNG bị ảnh "
            "hưởng sau swap'; Blocked cả 2 env). ⚠️ MT-01 — nếu kiến trúc là TẠO BOT MỚI (bot_id đổi) thì "
            "quyền Staff map theo bot_id cũ có nguy cơ mất → đây là điểm rủi ro NẶNG phụ thuộc MT-01. "
            "RULE-08. Evidence: bảng ma trận quyền trước/sau + ảnh đăng nhập từng Staff."),

    tc("Tiến trình đổi LOA & hoàn tất", "FUNC-001", "Boundary",
       "Dashboard sau khi đổi LOA không hiển thị số liệu sai lệch của LOA cũ",
       ("- Vừa hoàn tất đổi LOA\n"
        "- Bot cũ TRƯỚC khi đổi có số liệu dashboard khác 0 (số bạn bè, số tin gửi, biểu đồ)\n"
        "- Đã ghi lại số liệu dashboard của bot cũ"),
       "1. Ghi lại các con số trên dashboard TRƯỚC khi đổi LOA\n"
       "2. Hoàn tất đổi LOA\n"
       "3. Vào dashboard của bot mới\n"
       "4. Đối chiếu từng con số với số đã ghi\n"
       "5. Quan sát biểu đồ 友だち数推移",
       "Số liệu dashboard bot cũ ≠ 0",
       "- Dashboard KHÔNG hiển thị lại số liệu của LOA cũ\n"
       "- Các con số về 0 hoặc hiển thị trạng thái rỗng/cảnh báo\n"
       "- Biểu đồ không vẽ dữ liệu cũ\n"
       "- Không hiển thị giá trị rác (NaN, undefined, số âm)",
       env="PRODUCTION",
       note="Nguồn: TC-CBF-091 (FUNC-001, TD Section 7.2 'Dashboard hiển thị stats bot... sau swap số liệu "
            "sai → FE hiển thị cảnh báo/empty state'; Blocked cả 2 env) + Change bot r5-r6 "
            "(bảng bot_friend_statistic bị xóa data). RULE-08. Evidence: 2 ảnh dashboard trước/sau."),
]
