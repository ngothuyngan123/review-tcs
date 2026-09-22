# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 17-18.

S17 Phân quyền & bảo mật · S18 Hồi quy & môi trường.

⚠️ Nhóm 17 là vùng RỦI RO NHẤT của FA-041: spec ghi rõ 1 lỗ hổng NGHIÊM TRỌNG
(BR-03 mass assignment) và 2 lỗ hổng CAO/TRUNG BÌNH (BR-04 IDOR, BR-06 không
kiểm quyền Staff ở backend) — nhưng KHÔNG nguồn TC nào trong corpus từng kiểm.
Các TC dưới đây là TC BỔ SUNG do AI viết từ spec (không có TC gốc), đã đánh dấu
rõ ở cột Ghi chú. Xem MT-14 và MT-15.
"""
from _common import tc

ADMIN = "- Đăng nhập Admin của LOA, đã chọn 1 bot"
AI_NEW = "🆕 TC BỔ SUNG do AI viết từ spec — KHÔNG có TC gốc trong corpus. "

S17 = [
    tc("Phân quyền & bảo mật", "PERM-001", "Normal",
       "Admin — truy cập và thao tác được trên cả 8 tab",
       "- Tài khoản Admin của LOA",
       "1. Đăng nhập bằng tài khoản Admin\n"
       "2. Truy cập `/basic/chat-setting`\n"
       "3. Bấm lần lượt tất cả 8 tab ở thanh tab\n"
       "4. Thử thao tác chính ở từng tab (thêm trạng thái, tạo CSV, lưu cấu hình)",
       "—",
       "- Cả 8 tab hiển thị và truy cập được\n"
       "- Mọi chức năng chính hoạt động: CRUD trạng thái (Tab 1), tạo CSV (Tab 2),\n"
       "  lưu cấu hình (Tab 3-6 và Tab 8)",
       note="Nguồn: v2 r161 (TC-SC-053, Pass staging + production)"),

    tc("Phân quyền & bảo mật", "SEC-001", "Abnormal",
       "Chưa đăng nhập — truy cập URL bị đẩy về trang đăng nhập",
       "- Chưa đăng nhập (không có phiên hợp lệ) hoặc phiên đã hết hạn",
       "1. Truy cập thẳng URL `/basic/chat-setting`",
       "—",
       "- Bị chuyển hướng về `/login`\n"
       "- KHÔNG hiển thị bất kỳ nội dung nào của màn cài đặt chat",
       note="Nguồn: v2 r162 (TC-SC-054, Pass staging + production)"),

    tc("Phân quyền & bảo mật", "PERM-002", "Normal",
       "Staff theo vai trò tùy chỉnh — tab không có quyền phải ẩn hoặc chỉ đọc",
       "- Tài khoản Staff của LOA, được gán vai trò tùy chỉnh liên quan cài đặt chat (FA-036)",
       "1. Đăng nhập bằng tài khoản Staff\n"
       "2. Truy cập `/basic/chat-setting`\n"
       "3. Quan sát các tab hiển thị\n"
       "4. Thử thao tác trên từng tab",
       "—",
       "- Staff chỉ truy cập được đúng phạm vi vai trò được cấp\n"
       "- Tab không có quyền phải ẩn hoặc hiển thị rõ ràng ở chế độ chỉ đọc\n"
       "- KHÔNG xảy ra màn hình trắng hay lỗi khó hiểu",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-14 — ⏳ QA-027 chưa có ma trận quyền cụ thể cho từng tab nên Expected "
            "CHƯA chốt được chi tiết. Nguồn: v2 r163 (TC-SC-102, Not Tested) · SC r220 (chỉ ghi "
            "『Check thao tác bằng account staff / OK』, không có kết quả mong đợi)"),

    tc("Phân quyền & bảo mật", "PERM-003", "Abnormal",
       "Staff KHÔNG có quyền — gọi thẳng API cũng phải bị chặn, không chỉ ẩn menu",
       "- Tài khoản Staff KHÔNG được cấp quyền với màn cài đặt chat\n"
       "- Đã lấy được đường dẫn API từ phiên của Admin",
       "1. Đăng nhập bằng tài khoản Staff không có quyền\n"
       "2. Xác nhận menu「チャット設定」bị ẩn trên giao diện\n"
       "3. Gọi thẳng `GET /basic/chat-setting` bằng URL\n"
       "4. Gọi thẳng API lấy danh sách trạng thái và API lưu cấu hình bằng phiên của Staff này",
       "—",
       "- Bước 3: bị chặn (báo không có quyền hoặc chuyển hướng), không render được màn\n"
       "- Bước 4: API trả về lỗi không có quyền; KHÔNG trả dữ liệu, KHÔNG ghi được cấu hình\n"
       "- Việc ẩn menu trên giao diện KHÔNG được dùng thay cho kiểm quyền ở backend",
       spec="Đã hỏi leader",
       note=AI_NEW + "⚠️ MT-14 — spec BR-06 ghi rõ backend CHỈ kiểm đăng nhập + quyền sở hữu bot, "
            "KHÔNG kiểm vai trò tùy chỉnh ⇒ DỰ KIẾN FAIL. Corpus không có TC nào kiểm ở tầng API"),

    tc("Phân quyền & bảo mật", "SEC-ISO-001", "Abnormal",
       "Gọi API sắp xếp trạng thái với id của bot KHÁC — phải bị từ chối",
       "- 2 bot A và B thuộc 2 tài khoản khác nhau\n"
       "- Biết `id` của 1 bản ghi trạng thái thuộc bot B\n"
       "- Đang đăng nhập bằng tài khoản của bot A",
       "1. Ghi lại thứ tự hiện tại của danh sách trạng thái bot B\n"
       "2. Từ phiên của bot A, gọi API sắp xếp trạng thái (đường dẫn cũ `/ajax/sort-status-chat`)\n"
       "   với `id` của trạng thái thuộc bot B\n"
       "3. Đăng nhập lại bằng tài khoản bot B và đối chiếu thứ tự danh sách",
       "id trạng thái của bot B",
       "- API trả về lỗi không có quyền, KHÔNG thực hiện thay đổi\n"
       "- Thứ tự danh sách trạng thái của bot B giữ nguyên như bước 1",
       spec="Đã hỏi leader",
       note=AI_NEW + "⚠️ MT-15 — spec BR-04 ghi rõ đường dẫn cũ này THIẾU lọc theo bot ⇒ DỰ KIẾN "
            "FAIL (lỗ hổng IDOR mức CAO). Corpus không có TC nào kiểm"),

    tc("Phân quyền & bảo mật", "SEC-002", "Abnormal",
       "Gửi thêm trường lạ vào API lưu cấu hình — không được ghi đè cột ngoài phạm vi màn",
       ADMIN + "\n- Ghi lại giá trị hiện tại của gói cước và trạng thái hoạt động của bot",
       "1. Mở Tab 4「送信ショートカット」, bật DevTools > Network\n"
       "2. Bấm「保存」và bắt request lưu cấu hình\n"
       "3. Gửi lại request đó nhưng thêm 1 trường KHÔNG thuộc màn cài đặt chat\n"
       "   (vd trường gói cước hoặc trạng thái hoạt động của bot) với giá trị khác\n"
       "4. Đọc lại thông tin gói cước và trạng thái hoạt động của bot ở màn hợp đồng",
       "Request lưu cấu hình + 1 trường lạ",
       "- Máy chủ BỎ QUA trường lạ, chỉ ghi các trường thuộc màn cài đặt chat\n"
       "- Gói cước và trạng thái hoạt động của bot KHÔNG đổi so với bước tiền điều kiện",
       spec="Đã hỏi leader",
       note=AI_NEW + "⚠️ MT-15 — spec đánh giá BR-03 là lỗ hổng NGHIÊM TRỌNG: API lưu cấu hình dùng "
            "mass assignment toàn bộ request lên bảng `bots` với `$guarded = []` ⇒ DỰ KIẾN FAIL. "
            "Corpus KHÔNG có TC nào kiểm. Chạy trên môi trường test, KHÔNG chạy trên bot thật"),

    tc("Phân quyền & bảo mật", "STATE-001", "Abnormal",
       "Phiên hết hạn khi đang lưu — bị đẩy về đăng nhập, không lưu nửa vời",
       ADMIN,
       "1. Mở Tab 5「短縮URLの利用」, đổi trạng thái toggle\n"
       "2. Để phiên hết hạn (hoặc vô hiệu phiên từ phía máy chủ)\n"
       "3. Bấm「保存」\n"
       "4. Đăng nhập lại và quay lại Tab 5",
       "—",
       "- Bị chuyển hướng về `/login`\n"
       "- Sau khi đăng nhập lại: cấu hình VẪN là giá trị cũ, thay đổi ở bước 1 không được lưu\n"
       "- Không để lại dữ liệu nửa vời",
       note="Nguồn: v2 r166 (TC-SC-056, Pass staging + production)"),
]

S18 = [
    tc("Hồi quy & môi trường", "OUT-TRUTH-001", "Normal",
       "Toast「保存しました」hiện sau MỌI thao tác lưu thành công trên cả 6 tab có form",
       ADMIN,
       "1. Tab 1: thêm 1 trạng thái + Enter\n"
       "2. Tab 3: đổi 1 checkbox → bấm「保存」\n"
       "3. Tab 4: đổi lựa chọn phím tắt → bấm「保存」\n"
       "4. Tab 5: đổi toggle → bấm「保存」\n"
       "5. Tab 6: đổi toggle → bấm「保存」\n"
       "6. Tab 8: đổi toggle (tự lưu)",
       "—",
       "- Sau mỗi thao tác: toast「保存しました」xuất hiện\n"
       "- Toast tự biến mất sau vài giây, không cần đóng tay",
       note="Nguồn: v2 r165 (TC-SC-055, Pass staging + production)"),

    tc("Hồi quy & môi trường", "UI-002", "Normal",
       "Chạy cùng luồng chính trên Chrome (Windows) và Safari (Mac) — không lệch hành vi",
       "- Đăng nhập Admin trên cả Chrome (Windows) và Safari (Mac)",
       "1. Trên Chrome/Windows: thêm trạng thái ở Tab 1, tạo CSV ở Tab 2, lưu cấu hình Tab 3-8\n"
       "2. Trên Safari/Mac: lặp lại đúng luồng trên\n"
       "3. So sánh kết quả và giao diện giữa 2 trình duyệt",
       "—",
       "- Không có khác biệt về chức năng hay hiển thị gây ảnh hưởng thực tế\n"
       "- Đặc biệt đúng ở 3 chỗ: bộ chọn ngày (Tab 2), bộ chọn màu (Tab 1), kéo thả sắp xếp (Tab 1)",
       note="Nguồn: v2 r167 (TC-SC-103, Not Tested) — UI-002"),

    tc("Hồi quy & môi trường", "UI-001", "Boundary",
       "Độ phân giải tối thiểu 1366×768 — bố cục không vỡ",
       "- Đăng nhập Admin, đặt độ phân giải trình duyệt 1366×768",
       "1. Truy cập `/basic/chat-setting` ở độ phân giải 1366×768\n"
       "2. Duyệt qua từng tab trong 8 tab\n"
       "3. Thao tác thử các hành động chính (thêm trạng thái, tạo CSV, bật/tắt cấu hình)",
       "1366×768",
       "- Bố cục không vỡ ở độ phân giải thấp nhất được hỗ trợ\n"
       "- Thanh 8 tab, form, bảng lịch sử CSV đều hiển thị đủ\n"
       "- Các nút thao tác chính vẫn bấm được, không tràn ra ngoài màn hình",
       note="Nguồn: v2 r168 (TC-SC-104, Not Tested) — UI-001 / Catalog B UIC-13"),

    tc("Hồi quy & môi trường", "NOTI-MAIL-001", "Normal",
       "Friend nhắn tin — mỗi người dùng của bot nhận ĐÚNG 1 thông báo đẩy trên app",
       "- Bot có 2 cấu hình thông báo (admin + staff), cả 2 đều bật thông báo app và bật mục「1:1チャット」\n"
       "- Cả 2 đã đăng nhập app mobile admin",
       "1. Từ tài khoản LINE test gửi 1 tin nhắn tới LOA\n"
       "2. Quan sát thông báo đẩy trên app của admin và của staff\n"
       "3. Đếm số thông báo mỗi người nhận được cho tin này",
       "1 tin nhắn text",
       "- Admin nhận ĐÚNG 1 thông báo; staff nhận ĐÚNG 1 thông báo\n"
       "- KHÔNG ai nhận 2 thông báo cho cùng 1 tin đến\n"
       "- Số bản ghi thông báo sinh ra đúng bằng số người nhận, không nhân theo số vòng lặp",
       env="PRODUCTION",
       note="⚠️ Thuộc FA-006 nhưng là side-effect trực tiếp của bộ đếm chưa xác nhận ở Tab 3 → giữ "
            "trong kho FA-041 làm TC hồi quy. Nguồn: v2 r184 (TC-SC-184, Not Tested)"),

    tc("Hồi quy & môi trường", "NOTI-MAIL-001", "Normal",
       "Friend nhắn tin — mỗi người bật thông báo PC nhận ĐÚNG 1 web push",
       "- Bot có 2 cấu hình thông báo; cả 2 người dùng đã bật thông báo PC và đăng ký web push\n"
       "- Có thêm 1 người dùng đã TẮT thông báo PC để đối chứng",
       "1. Từ tài khoản LINE test gửi 1 tin nhắn tới LOA\n"
       "2. Quan sát web push thực tế trên trình duyệt của từng người\n"
       "3. Đếm số bản ghi thông báo PC sinh ra cho sự kiện này",
       "1 tin nhắn text",
       "- Mỗi người đã bật thông báo PC nhận ĐÚNG 1 web push (2 người → 2 thông báo)\n"
       "- Người đã TẮT thông báo PC KHÔNG nhận gì và không sinh bản ghi",
       env="PRODUCTION",
       note="Nguồn: v2 r185 (TC-SC-185, Not Tested)"),

    tc("Hồi quy & môi trường", "DATA-COUNT-001", "Normal",
       "Friend nhắn tin — số chưa xác nhận trên app tăng đúng 1 cho mỗi người dùng",
       "- Bot có 2 cấu hình thông báo (admin + staff)\n"
       "- Ghi lại số chưa xác nhận hiện tại trên app của admin và của staff",
       "1. Ghi lại số chưa xác nhận trước sự kiện của cả 2 người\n"
       "2. Từ tài khoản LINE test gửi 1 tin nhắn tới LOA\n"
       "3. Đọc lại số chưa xác nhận của cả 2 người trên app\n"
       "4. Đối chiếu với số hội thoại chưa xác nhận hiển thị trên web",
       "1 tin nhắn text",
       "- Số của admin tăng ĐÚNG 1, số của staff tăng ĐÚNG 1\n"
       "- Không ai tăng 2 cho 1 tin đến\n"
       "- Số trên app khớp với số hội thoại chưa xác nhận đếm được trên web",
       env="PRODUCTION",
       note="Nguồn: v2 r186 (TC-SC-186, Not Tested)"),

    tc("Hồi quy & môi trường", "PERM-004", "Normal",
       "Staff tắt mục「1:1チャット」trong cài đặt thông báo — chỉ mình staff ngừng nhận",
       "- Bot có 2 cấu hình thông báo (admin + staff)",
       "1. Staff tắt mục「1:1チャット」trong `/basic/notify-setting` của chính mình\n"
       "2. Từ tài khoản LINE test gửi 1 tin nhắn tới LOA\n"
       "3. Quan sát thông báo đẩy của admin và của staff\n"
       "4. Kiểm tra cấu hình thông báo của admin",
       "—",
       "- Staff KHÔNG nhận thông báo cho tin 1:1\n"
       "- Admin VẪN nhận ĐÚNG 1 thông báo\n"
       "- Thao tác của staff không làm đổi cấu hình thông báo của admin",
       env="PRODUCTION",
       note="Nguồn: v2 r190 (TC-SC-190, Not Tested)"),

    tc("Hồi quy & môi trường", "ENV-001", "Normal",
       "Đối chiếu cấu hình giữa staging và production cho cùng 1 bot",
       "- Có cùng 1 bot dùng được ở cả staging và production (hoặc 2 bot tương đương)",
       "1. Trên staging: ghi lại toàn bộ cấu hình 8 tab của bot\n"
       "2. Trên production: mở cùng màn và ghi lại cấu hình tương ứng\n"
       "3. So sánh từng tab: số tab hiển thị, trạng thái mặc định, các nút thao tác",
       "—",
       "- Số tab và thứ tự tab giống nhau ở 2 môi trường\n"
       "- Các tab có mặt ở staging nhưng chưa có ở production (hoặc ngược lại) được ghi ra rõ ràng\n"
       "- Không có khác biệt nào làm đổi hành vi lưu cấu hình",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=AI_NEW + "Cơ sở: bộ v2 có cột kết quả RIÊNG cho staging và production và đã ghi nhận "
            "ÍT NHẤT 3 TC cho kết quả KHÁC NHAU giữa 2 môi trường (TC-SC-020 Fail staging/Pass "
            "production · TC-SC-021 Fail staging/Skipped production · TC-SC-088 Blocked staging/"
            "Fail production) ⇒ cần 1 TC đối chiếu môi trường"),

    tc("Hồi quy & môi trường", "REG-RUN-001", "Normal",
       "Chạy lại các case từng Không đạt và đã được fix",
       "- Có danh sách bug đã đóng của FA-041: BUG-006 · BUG-007 · BUG-008 · BUG-011 ·\n"
       "  BUG-017 · BUG-018 · BUG-022",
       "1. Với mỗi bug đã đóng, xác định TC tương ứng trong kho\n"
       "2. Chạy lại đúng TC đó trên môi trường hiện hành\n"
       "3. Ghi kết quả từng case vào bảng theo dõi",
       "—",
       "- 7 bug đã đóng đều có TC tương ứng trong kho và đều được chạy lại\n"
       "- Không case nào tái phát\n"
       "- Case nào chưa có TC tương ứng thì bổ sung, không bỏ qua âm thầm",
       note=AI_NEW + "RULE-12 mục (3): mọi case từng Không đạt và được fix phải nằm trong bộ hồi quy. "
            "Danh sách bug lấy từ cột Ghi chú của v2 (các bug ghi『Closed』)"),

    tc("Hồi quy & môi trường", "REG-RUN-001", "Abnormal",
       "Theo dõi 4 bug còn MỞ — xác nhận còn tái hiện hay đã hết",
       "- Danh sách bug còn mở của FA-041: BUG-021 (mất trạng thái khi kéo thả liên tiếp) ·\n"
       "  BUG-023 (chặn nhầm khoảng đúng 180 ngày) · BUG-024 (gói trả phí bị chặn như gói free) ·\n"
       "  TC-SC-070 (tin đã thu hồi trong file CSV)",
       "1. Chạy lại TC tương ứng từng bug trên môi trường hiện hành\n"
       "2. Với BUG-021: chạy CẢ bằng thao tác tay lẫn tự động (bug chỉ tái hiện khi chạy tự động)\n"
       "3. Ghi rõ kết quả và môi trường chạy của từng case",
       "—",
       "- Mỗi bug có kết luận rõ: còn tái hiện / đã hết / không đủ cơ sở kết luận\n"
       "- BUG-021 ghi rõ kết quả của CẢ 2 cách chạy, không kết luận chỉ dựa vào 1 cách\n"
       "- Các case DỰ KIẾN FAIL trong kho được cập nhật lại trạng thái theo kết quả",
       env="PRODUCTION",
       note=AI_NEW + "⚠️ Liên quan MT-06 · MT-12 · MT-20. BUG-024 mức CAO (ảnh hưởng khách trả tiền) "
            "→ ưu tiên chạy trước"),
]
