# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 25-28: media & ảnh, dữ liệu KHÔNG được copy,
hồi quy sau copy, môi trường & legacy.

Toàn bộ nhóm Media đặt Môi trường test = PRODUCTION theo RULE-08.
Quy ước: **bot A = LOA gửi**, **bot B = LOA nhận** (theo spec; xem MT-01).
"""
from _common import tc

CP = ("- Bot A (LOA gửi) và bot B (LOA nhận) đều plan Standard/Pro, job nền đang bật\n"
      "- Bot B là LOA TRỐNG để dễ đối chiếu\n"
      "- Đã dựng xong dữ liệu ở bot A theo mục điều kiện riêng bên dưới")
RUN = "1. Ở bot A, xác nhận dữ liệu đã dựng đúng\n2. Thực hiện copy A → B và chờ trạng thái hoàn tất\n"
P = "PRODUCTION"
OLD = ("- Đường dẫn ảnh kiểu cũ 1: `/msg_template/image/<tên tệp>.png`\n"
       "- Đường dẫn ảnh kiểu cũ 2: `/msg_template/image/<thư mục>/<tên tệp>.jpg`\n"
       "- Đường dẫn ảnh kiểu mới: `/ext-media-step/media/images/<id bot>/<id admin>/<thư mục>/<tên tệp>`")
MT23 = ("MT-23 — quy tắc sinh đường dẫn ảnh sau copy KHÔNG có trong spec (BR-12 chỉ nói "
        "「copy file vật lý qua Dropbox API」). ")

S6 = [
    # ═══════════════ 25. Media & ảnh khi copy ═══════════════
    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh richmenu sau copy — xem được ở màn quản lý và hiển thị được cho bạn bè",
       CP + "\n- Bot A có 2 richmenu đã gắn ảnh và đã đăng ký lên LINE",
       RUN + "3. Mở chi tiết 2 richmenu ở bot B, xem ảnh có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh ở cả 2 bot\n"
             "5. Bật hiển thị richmenu ở bot B và xem trên LINE bằng tài khoản bạn bè bot B",
       "2 richmenu có ảnh",
       "- Ảnh hiển thị ở màn quản lý bot B\n"
       "- Đường dẫn ảnh bot B KHÁC bot A\n"
       "- Bước 5: bạn bè bot B nhìn thấy đúng ảnh richmenu trên LINE",
       env=P,
       note="Nguồn: improve url image r3-r4 · Backup image r2-r3. RULE-06: verify tới hiển thị trên LINE."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh trong mẫu tin nút bấm — 4 kiểu nút, dữ liệu MỚI",
       CP + "\n- Bot A có 4 mẫu tin nút bấm tạo MỚI (đường dẫn ảnh kiểu mới), "
            "mỗi mẫu 1 kiểu ở cột dữ liệu test",
       RUN + "3. Mở 4 mẫu tin ở bot B, xem ảnh có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh ở 2 bot\n"
             "5. Gửi cả 4 mẫu tin cho bạn bè bot B và xem trên LINE",
       "① nút tiêu chuẩn ② nút màu ③ nút ảnh ④ nút trả lời nhanh có ảnh",
       "- Cả 4 mẫu tin: ảnh hiển thị ở màn quản lý bot B\n"
       "- Đường dẫn ảnh bot B khác bot A\n"
       "- Bước 5: bạn bè nhận và xem được ảnh trên LINE ở cả 4 mẫu",
       env=P,
       note="Gộp 4 kiểu nút vì CÙNG 1 kết quả. Nguồn: improve url image r5-r20 (nhánh data mới, "
            "kết quả OK Step / OK dev)."),

    tc("Media & ảnh khi copy", "COMPAT-LEGACY-001", "Abnormal",
       "Ảnh trong mẫu tin nút bấm — dữ liệu CŨ (đường dẫn kiểu cũ)",
       CP + "\n- Bot A có 4 mẫu tin nút bấm tạo từ lâu, ảnh còn nằm ở đường dẫn KIỂU CŨ\n" + OLD,
       RUN + "3. Mở 4 mẫu tin ở bot B, xem ảnh có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh ở bot B\n"
             "5. Gửi cả 4 cho bạn bè bot B và xem trên LINE",
       "4 kiểu nút, ảnh ở đường dẫn kiểu cũ",
       "- Cả 4 mẫu tin: ảnh hiển thị ĐƯỢC ở màn quản lý bot B (không vỡ ảnh)\n"
       "- Đường dẫn ảnh mới sinh ra theo quy tắc Leader chốt ở MT-23\n"
       "- Bước 5: bạn bè xem được ảnh trên LINE\n"
       "- ⚠️ Nếu ảnh vỡ thì raise bug",
       env=P,
       spec="Đã hỏi leader",
       note=MT23 + "improve url image r5-r20 (nhánh data cũ) BỎ TRỐNG kết quả ở nhiều dòng — "
            "nhánh này chưa được đo đầy đủ."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Abnormal",
       "Ảnh thường kiểu cũ dạng 1 — đường dẫn phẳng (case từng bị lỗi)",
       CP + "\n- Bot A có mẫu tin ảnh thường với ảnh ở đường dẫn kiểu cũ dạng PHẲNG "
            "`/msg_template/image/<tên tệp>.png`",
       RUN + "3. Mở mẫu tin ở bot B, xem ảnh có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh mới ở bot B\n"
             "5. Kiểm tra thư mục ảnh của bot B: có bị copy NGUYÊN CẢ THƯ MỤC `image` không\n"
             "6. Gửi cho bạn bè bot B và xem ảnh trên LINE",
       "Ảnh ở `/msg_template/image/1611379719RRWmi7.png`",
       "- Ảnh hiển thị được ở bot B\n"
       "- Đường dẫn mới theo quy tắc Leader chốt ở MT-23\n"
       "- Bước 5: CHỈ copy đúng tệp ảnh đó — KHÔNG copy cả thư mục `image` sang bot B\n"
       "- Bước 6: bạn bè xem được ảnh trên LINE",
       env=P,
       spec="Đã hỏi leader",
       note=MT23 + "Tab Info r5 (24/08/2025) —「[Bug tự detect] Backup template image folder dạng cũ "
            "/msg_template/image BỊ COPY CẢ FOLDER image」. improve url image r21 ghi rõ「CASE BỊ BUG」, "
            "kết quả OK Step. Đây là TC hồi quy chính của bug đó."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh thường kiểu cũ dạng 2 và kiểu mới",
       CP + "\n- Bot A có 2 mẫu tin ảnh thường: 1 ảnh ở đường dẫn kiểu cũ dạng có thư mục con, "
            "1 ảnh ở đường dẫn kiểu mới",
       RUN + "3. Mở 2 mẫu tin ở bot B, xem ảnh\n"
             "4. Ghi lại đường dẫn ảnh mới ở bot B\n"
             "5. Gửi cho bạn bè bot B và xem trên LINE",
       "① `/msg_template/image/16208990343AS/16208990343AS.jpg` "
       "② `/ext-media-step/media/images/118495/157064/1752577402E2j7Kf/1752577402E2j7Kf.jpg`",
       "- Cả 2 ảnh hiển thị ở bot B\n"
       "- Đường dẫn mới sinh theo quy tắc Leader chốt ở MT-23, giữ đúng cấu trúc thư mục con\n"
       "- Bước 5: bạn bè xem được cả 2 ảnh trên LINE",
       env=P,
       spec="Đã hỏi leader",
       note=MT23 + "improve url image r22-r23 (kết quả OK dev / OK Step)."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh của mẫu tin ảnh có vùng bấm — cả dữ liệu cũ và mới",
       CP + "\n- Bot A có 3 mẫu tin ảnh có vùng bấm: 1 ảnh đường dẫn cũ dạng phẳng, "
            "1 đường dẫn cũ có thư mục con, 1 đường dẫn kiểu mới",
       RUN + "3. Mở 3 mẫu tin ở bot B, xem ảnh và bố cục vùng bấm\n"
             "4. Ghi lại đường dẫn ảnh ở bot B\n"
             "5. Gửi cả 3 cho bạn bè bot B và bấm thử vùng trên LINE",
       "3 mẫu tin ảnh có vùng bấm × 3 kiểu đường dẫn",
       "- Cả 3 ảnh hiển thị ở bot B, không vỡ ảnh\n"
       "- Bố cục vùng bấm giữ nguyên\n"
       "- Bước 5: bạn bè xem được ảnh và bấm vùng chạy đúng hành động",
       env=P,
       spec="Đã hỏi leader",
       note=MT23 + "improve url image r24-r26. Ô Note r24 ghi「Case này chỉ fake data test ở dev, "
            "còn trên step Duy bảo thực tế sẽ không có」— cần Leader xác nhận có cần test trên production không."),

    tc("Media & ảnh khi copy", "MEDIA-001", "Abnormal",
       "Ảnh đại diện của mẫu tin video — cả dữ liệu cũ và mới",
       CP + "\n- Bot A có 2 mẫu tin video: 1 tạo từ lâu (đường dẫn cũ), 1 tạo mới",
       RUN + "3. Mở 2 mẫu tin ở bot B, xem ẢNH ĐẠI DIỆN có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh đại diện ở bot B\n"
             "5. Gửi cả 2 cho bạn bè bot B và xem trên LINE",
       "1 video dữ liệu cũ + 1 video dữ liệu mới",
       "- Ảnh đại diện của CẢ 2 video hiển thị được ở màn quản lý bot B\n"
       "- Bước 5: bạn bè xem được video và ảnh đại diện trên LINE\n"
       "- ⚠️ Nếu ảnh đại diện của video dữ liệu cũ không hiện thì raise bug",
       env=P,
       spec="Đã hỏi leader",
       note="MT-24 — Backup image r28/r30 ghi NG cho「video - thumbnail > check ảnh」ở CẢ 2 nhánh; "
            "improve url image r29-r30 (mới hơn) = OK Step nhưng CHỈ đo nhánh dữ liệu mới, "
            "nhánh dữ liệu cũ (r27-r28) bỏ trống. ⚠️ DỰ KIẾN FAIL ở nhánh dữ liệu cũ."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh nền và ảnh do người dùng tải lên trong biểu mẫu — cả dữ liệu cũ và mới",
       CP + "\n- Bot A có 2 biểu mẫu: 1 tạo từ lâu, 1 tạo mới; cả 2 đều có ảnh nền "
            "và có mục cho người dùng tải ảnh lên",
       RUN + "3. Mở 2 biểu mẫu ở bot B, xem ảnh nền\n"
             "4. Mở đường dẫn công khai của 2 biểu mẫu trên điện thoại\n"
             "5. Tải 1 ảnh lên qua mục tải tệp và gửi\n"
             "6. Ở bot B, mở màn kết quả trả lời và xem ảnh vừa tải lên",
       "2 biểu mẫu (dữ liệu cũ + mới), mỗi cái 1 ảnh nền",
       "- Ảnh nền hiển thị ở cả màn quản lý và trang công khai của bot B\n"
       "- Đường dẫn ảnh khác bot A\n"
       "- Bước 6: ảnh người dùng tải lên lưu vào bot B và xem lại được",
       env=P,
       spec="Đã hỏi leader",
       note=MT23 + "improve url image r31-r38 · Backup image r32-r39 · Improve backup media r25-r26, r72."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Normal",
       "Ảnh của sự kiện đặt lịch — cả dữ liệu cũ và mới",
       CP + "\n- Bot A có 2 sự kiện đặt lịch: 1 tạo từ lâu, 1 tạo mới, cả 2 đều có ảnh",
       RUN + "3. Mở 2 sự kiện ở bot B, xem ảnh\n"
             "4. Ghi lại đường dẫn ảnh ở bot B\n"
             "5. Mở trang đặt lịch công khai của bot B trên điện thoại",
       "2 sự kiện (dữ liệu cũ + mới)",
       "- Ảnh hiển thị ở màn quản lý bot B\n"
       "- Đường dẫn khác bot A\n"
       "- Bước 5: ảnh hiển thị đúng trên trang đặt lịch công khai",
       env=P,
       note="Nguồn: improve url image r39-r42 · Backup image r40-r43 · Improve backup media r24, r75."),

    tc("Media & ảnh khi copy", "MEDIA-001", "Normal",
       "Tệp âm thanh sau copy",
       CP + "\n- Bot A có 2 mẫu tin âm thanh với thời lượng khác nhau",
       RUN + "3. Mở 2 mẫu tin ở bot B, phát thử ở màn quản lý\n"
             "4. Ghi lại đường dẫn tệp ở bot B\n"
             "5. Gửi cho bạn bè bot B và nghe trên LINE",
       "2 tệp âm thanh: 10 giây và 3 phút",
       "- Phát thử được ở màn quản lý bot B, thời lượng đúng\n"
       "- Đường dẫn khác bot A\n"
       "- Bước 5: bạn bè nghe được trên LINE",
       env=P,
       note="Nguồn: Improve backup media r9, r17, r49, r70, r91 · Backup (job) r164."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Boundary",
       "Ảnh có kích thước và dung lượng khác nhau sau copy",
       CP + "\n- Bot A có 5 mẫu tin ảnh với 5 kích thước / dung lượng khác nhau ở cột dữ liệu test",
       RUN + "3. Mở 5 mẫu tin ở bot B, xem ảnh\n"
             "4. Tải ảnh từ bot B về, so kích thước và dung lượng với ảnh gốc\n"
             "5. Gửi cả 5 cho bạn bè bot B",
       "① 100×100 (10KB) ② 1024×768 (300KB) ③ 2500×1686 (2MB) "
       "④ ảnh dài 1040×5000 ⑤ ảnh gần mức tối đa cho phép",
       "- Cả 5 ảnh hiển thị được ở bot B\n"
       "- Kích thước và dung lượng giống ảnh gốc, KHÔNG bị nén hay cắt\n"
       "- Bước 5: bạn bè xem được cả 5 ảnh trên LINE",
       env=P,
       note="Gộp 5 kích thước vì CÙNG 1 kết quả. Nguồn: Improve backup media r21 "
            "—「check các size: btn color OK / btn ảnh OK」+ r39 —「tạo data có ảnh, có kích thước khác nhau」."),

    tc("Media & ảnh khi copy", "MEDIA-CLEAN-001", "Normal",
       "Ảnh ở BOT GỬI vẫn nguyên vẹn sau khi copy — không bị di chuyển hay xoá",
       CP + "\n- Bot A có đầy đủ media: richmenu, mẫu tin ảnh, ảnh có vùng bấm, video, âm thanh, "
            "biểu mẫu có ảnh, sự kiện có ảnh",
       RUN + "3. Quay lại BOT A, mở lần lượt từng nơi có ảnh\n"
             "4. Kiểm tra ảnh còn hiển thị không\n"
             "5. Vào sửa 1 mẫu tin có ảnh ở bot A và lưu lại\n"
             "6. Gửi mẫu tin đó cho bạn bè của BOT A",
       "≥7 nơi có media ở bot A",
       "- TẤT CẢ ảnh ở bot A vẫn hiển thị bình thường sau khi copy\n"
       "- Bước 5: sửa và lưu được, ảnh không mất\n"
       "- Bước 6: bạn bè bot A vẫn nhận và xem được ảnh\n"
       "- Đường dẫn ảnh ở bot A KHÔNG đổi",
       env=P,
       note="Nguồn: Improve backup media r60-r80 (khối「Check bot gốc: vào xem và send ok」) "
            "và r102-r121 (khối「Bot gốc check edit」). Đây là TC hồi quy quan trọng nhất về media."),

    tc("Media & ảnh khi copy", "MEDIA-CLEAN-001", "Normal",
       "Ảnh ở 2 bot độc lập — xoá ảnh ở bot nhận không làm mất ảnh bot gửi",
       CP + "\n- Đã copy mẫu tin có ảnh từ A sang B",
       "1. Ở bot B, xoá mẫu tin có ảnh vừa copy\n"
       "2. Quay lại bot A, mở mẫu tin gốc\n"
       "3. Kiểm tra ảnh còn hiển thị không\n"
       "4. Gửi mẫu tin đó cho bạn bè bot A\n"
       "5. Làm ngược lại: xoá mẫu tin ở bot A rồi kiểm tra ở bot B",
       "1 mẫu tin có ảnh",
       "- Bước 3: ảnh ở bot A vẫn hiển thị bình thường\n"
       "- Bước 4: bạn bè bot A vẫn nhận được ảnh\n"
       "- Bước 5: mẫu tin ở bot B (nếu chưa xoá) vẫn còn ảnh\n"
       "- Hai bot dùng 2 tệp ảnh RIÊNG, không dùng chung",
       env=P,
       note="Suy luận của AI theo MEDIA-CLEAN-001 — corpus không có TC xoá chéo. "
            "Đây là rủi ro cao (nếu dùng chung tệp thì xoá 1 bên làm hỏng bên kia). Cần Leader xác nhận."),

    tc("Media & ảnh khi copy", "MEDIA-IMG-001", "Abnormal",
       "Media của các tính năng KHÔNG nằm trong phạm vi copy — bot gửi vẫn dùng được bình thường",
       CP + "\n- Bot A có media ở các tính năng KHÔNG được copy: popup, lịch đặt (ảnh lịch / nhân viên / khoá học), "
            "sản phẩm, ảnh bot ở đối tác giới thiệu",
       RUN + "3. Ở BOT A, mở lần lượt từng tính năng trên\n"
             "4. Kiểm tra ảnh còn hiển thị và sửa được không\n"
             "5. Với popup: kiểm tra popup nhúng ở trang web ngoài còn hiện ảnh không\n"
             "6. Với sản phẩm: gửi trang mua hàng cho bạn bè bot A và xem ảnh",
       "4 nhóm media không thuộc phạm vi copy",
       "- TẤT CẢ ảnh ở bot A vẫn hiển thị và sửa được\n"
       "- Bước 5: popup nhúng vẫn hiện ảnh đúng\n"
       "- Bước 6: trang mua hàng hiển thị ảnh sản phẩm bình thường\n"
       "- Việc copy KHÔNG làm hỏng media của các tính năng ngoài phạm vi",
       env=P,
       note="Nguồn: Improve backup media r39 —「kể cả các chỗ ko backup ⇒ cần check ở bot gốc xem có hiện dc ảnh ko, "
            "có edit dc ko? send cho user ok ko?」+ r94-r101. "
            "⚠️ TC nguồn từ 2024-01 (>2 năm) — CẦN VERIFY LẠI."),

    # ═══════════════ 26. Dữ liệu KHÔNG được copy ═══════════════
    tc("Dữ liệu KHÔNG được copy", "FUNC-001", "Abnormal",
       "Đối chiếu TOÀN BỘ danh sách dữ liệu KHÔNG được copy",
       CP + "\n- Bot A có dữ liệu ở TẤT CẢ các tính năng ngoài phạm vi copy "
            "(theo danh sách ở cột dữ liệu test)",
       RUN + "3. Ở bot B, mở lần lượt màn của TỪNG tính năng trong danh sách\n"
             "4. Ghi lại: màn đó trống hay có dữ liệu\n"
             "5. Lập bảng đối chiếu với danh sách「上記以外のデータはコピーされません」trên màn データコピー",
       "popup · lịch đặt (salon/lesson) · sản phẩm · đối tác giới thiệu · URL rút gọn · "
       "mã QR / trang đích · bạn bè · tin nhắn chat · ảnh tạo trong công cụ richmenu",
       "- Mọi tính năng trong danh sách đều TRỐNG ở bot B\n"
       "- KHÔNG có bản ghi nào của bot A lọt sang\n"
       "- Bảng đối chiếu khớp với những gì UI nói với người dùng\n"
       "- Ghi rõ mọi điểm lệch giữa hiện trạng và danh sách trên UI",
       spec="Đã hỏi leader",
       note="MT-28 — 3 nguồn (Improve backup media r83-r101 / Backup (job) r277, r334, r343 / "
            "feature-spec §7.5) liệt kê KHÁC NHAU. Đây là TC tổng để chốt danh sách thật."),

    tc("Dữ liệu KHÔNG được copy", "FUNC-001", "Abnormal",
       "Popup — có sang bot nhận không?",
       CP + "\n- Bot A có 2 popup: 1 popup đơn giản, 1 popup có đầy đủ cài đặt "
            "(ảnh, nút, đếm ngược, môi trường hiển thị, số lần hiện)",
       RUN + "3. Mở màn popup ở bot B\n"
             "4. Đếm số popup và số folder popup\n"
             "5. Nếu có popup: kiểm tra mã nhúng và cài đặt bên trong",
       "2 popup ở bot A",
       "- Màn popup ở bot B TRỐNG — 0 popup, 0 folder\n"
       "- KHÔNG có mã nhúng nào của bot A lọt sang\n"
       "- ⚠️ Nếu popup CÓ sang thì phải kiểm tra 28 hạng mục chi tiết trong corpus (xem MT-22)",
       spec="Đã hỏi leader",
       note="MT-22 — Backup (job) r280:「13. Popup ⇒ tạm thời không backup nữa」nhưng r281-r308 vẫn có "
            "28 dòng TC chi tiết. Improve backup media r94:「ko backup」. db-mapping.md:415: `popup` is_enable=0."),

    tc("Dữ liệu KHÔNG được copy", "FUNC-001", "Abnormal",
       "Lịch đặt salon / lesson (予約カレンダー) — có sang bot nhận không?",
       CP + "\n- Bot A có 1 salon và 1 lesson với đầy đủ nhân viên, khoá học, lịch trống",
       RUN + "3. Mở màn salon và màn lesson ở bot B\n"
             "4. Kiểm tra danh sách salon / lesson / nhân viên / khoá học\n"
             "5. Kiểm tra có bản ghi nào bị tạo ra ở trạng thái LỖI không",
       "1 salon + 1 lesson đầy đủ",
       "- Cả 2 màn ở bot B TRỐNG\n"
       "- KHÔNG có bản ghi nào bị tạo ra rồi bị lỗi (không có mục nào mở ra báo lỗi)\n"
       "- Không có nhân viên / khoá học nào của bot A lọt sang",
       spec="Đã hỏi leader",
       note="MT-21 — Backup 1.0 r256:「Chưa support nhưng test thì THẤY CÓ TẠO EVENT nhưng BỊ LỖI do "
            "`setting_date_id` vẫn lấy id của bot cũ ⇒ Tạm thời sửa để không backup event mới」. "
            "TC này để xác nhận bản sửa đó còn hiệu lực."),

    tc("Dữ liệu KHÔNG được copy", "PAY-AMOUNT-001", "Abnormal",
       "Sản phẩm bán hàng — không sang bot nhận, và các nơi tham chiếu tới sản phẩm xử lý an toàn",
       CP + "\n- Bot A có 3 sản phẩm (1 lần và theo chu kỳ)\n"
            "- Bot A có richmenu và mẫu tin văn bản có tham chiếu tới sản phẩm",
       RUN + "3. Mở màn 商品販売 ở bot B — đếm số sản phẩm\n"
             "4. Mở richmenu ở bot B, kiểm tra vùng có hành động sản phẩm\n"
             "5. Mở mẫu tin văn bản ở bot B, đọc phần mã chèn sản phẩm\n"
             "6. Gửi mẫu tin đó cho bạn bè bot B",
       "3 sản phẩm + 2 nơi tham chiếu",
       "- Bot B có 0 sản phẩm\n"
       "- Vùng richmenu: danh sách chọn sản phẩm RỖNG, không trỏ tới sản phẩm bot A\n"
       "- Bước 6: tin gửi ra KHÔNG chứa liên kết mua hàng của bot A\n"
       "- Không có nguy cơ khách hàng của bot B thanh toán vào tài khoản của bot A",
       env=P,
       note="Nguồn: Backup (job) r87-r90 · Backup 1.0 r36 · Improve backup media r97-r98, r100-r101. "
            "PRODUCTION theo RULE-08 (liên quan tiền)."),

    tc("Dữ liệu KHÔNG được copy", "REG-URL-001", "Abnormal",
       "Mã QR / trang đích — không sang bot nhận, và các nơi tham chiếu xử lý an toàn",
       CP + "\n- Bot A có 2 mã QR / trang đích và có bộ lọc dùng điều kiện mã QR, "
            "có popup dùng mã QR",
       RUN + "3. Mở màn QR / trang đích ở bot B — đếm số bản ghi\n"
             "4. Mở bộ lọc có điều kiện mã QR ở bot B\n"
             "5. Ghi rõ điều kiện đó còn hay bị bỏ",
       "2 mã QR + 1 bộ lọc + 1 popup tham chiếu",
       "- Màn QR / trang đích ở bot B TRỐNG\n"
       "- Điều kiện lọc theo mã QR xử lý theo quyết định MT-13\n"
       "- KHÔNG có mã QR nào của bot A lọt sang",
       spec="Đã hỏi leader",
       note="MT-13 + MT-28 — Backup (job) r334 · r292 (「Do không backup qr code nên chỗ id của qr code "
            "trong popup rỗng」) · [MN]Job r34, r63-r64."),

    tc("Dữ liệu KHÔNG được copy", "REG-URL-001", "Abnormal",
       "URL rút gọn / URL chuyển hướng — làm rõ có sang hay không",
       CP + "\n- Bot A có 3 URL rút gọn và 1 mẫu tin văn bản có URL chuyển hướng",
       RUN + "3. Mở màn quản lý URL ở bot B — đếm số bản ghi\n"
             "4. Mở mẫu tin văn bản ở bot B, đọc URL trong nội dung\n"
             "5. Gửi mẫu tin cho bạn bè bot B và bấm URL đó\n"
             "6. Kiểm tra thống kê lượt bấm ở cả 2 bot",
       "3 URL rút gọn + 1 URL chuyển hướng",
       "- Ghi rõ hiện trạng theo quyết định MT-28\n"
       "- Bước 6: lượt bấm KHÔNG được ghi vào bot A\n"
       "- ⚠️ Nếu URL ở bot B vẫn trỏ tới URL rút gọn của bot A thì raise bug rò rỉ dữ liệu chéo bot",
       env=P,
       spec="Đã hỏi leader",
       note="MT-28 — Backup (job) r277:「11. url redirect — không support」vs db-mapping.md:417 "
            "ghi bảng `url` (order 27) là is_enable=1. Mâu thuẫn thẳng."),

    tc("Dữ liệu KHÔNG được copy", "FRIEND-001", "Abnormal",
       "Bạn bè và lịch sử hội thoại — không sang bot nhận",
       CP + "\n- Bot A có ≥50 bạn bè với lịch sử chat, đánh dấu, trạng thái xử lý, ghi chú",
       RUN + "3. Mở màn 友だちリスト ở bot B — đếm số bạn bè\n"
             "4. Mở màn chat 1:1 ở bot B — đếm số hội thoại\n"
             "5. Tìm kiếm tên một bạn bè của bot A trong danh sách bot B",
       "Bot A: ≥50 bạn bè có lịch sử chat",
       "- Số bạn bè ở bot B = số bạn bè VỐN CÓ của bot B (không cộng thêm của bot A)\n"
       "- Màn chat 1:1 không có hội thoại nào của bot A\n"
       "- Tìm kiếm không ra bạn bè nào của bot A\n"
       "- KHÔNG rò rỉ dữ liệu cá nhân giữa 2 LOA",
       note="Suy luận của AI — bạn bè không nằm trong 13 loại được copy. Corpus không có TC này. "
            "Đây là điểm bảo mật quan trọng nhất của tính năng. Cần Leader xác nhận."),

    tc("Dữ liệu KHÔNG được copy", "MEDIA-IMG-001", "Abnormal",
       "Ảnh tạo bằng công cụ tạo ảnh richmenu — không sang bot nhận",
       CP + "\n- Bot A có 3 ảnh đã tạo bằng công cụ tạo ảnh richmenu (リッチメニュー画像作成)",
       RUN + "3. Mở màn công cụ tạo ảnh richmenu ở bot B\n"
             "4. Đếm số ảnh đã lưu\n"
             "5. Kiểm tra richmenu ở bot B có hiển thị ảnh không",
       "3 ảnh đã tạo bằng công cụ",
       "- Màn công cụ tạo ảnh ở bot B TRỐNG — 0 ảnh đã lưu\n"
       "- Bước 5: richmenu ở bot B VẪN hiển thị ảnh (ảnh gắn vào richmenu là bản riêng, đã được copy)\n"
       "- 2 việc này độc lập nhau",
       env=P,
       note="Nguồn: Improve backup media r83 —「tạo ảnh richmenu: ko backup」và r62/r103 (bot gốc vẫn edit được). "
            "⚠️ TC nguồn từ 2024-01 (>2 năm) — CẦN VERIFY LẠI."),

    tc("Dữ liệu KHÔNG được copy", "FUNC-001", "Abnormal",
       "Dữ liệu đối tác giới thiệu — không sang bot nhận",
       CP + "\n- Bot A có ≥2 đối tác giới thiệu và ảnh bot ở màn đối tác giới thiệu\n"
            "- Bot A có bộ lọc dùng điều kiện đối tác giới thiệu",
       RUN + "3. Mở màn đối tác giới thiệu ở bot B — đếm số bản ghi\n"
             "4. Mở bộ lọc có điều kiện đối tác giới thiệu ở bot B\n"
             "5. Ghi rõ điều kiện đó còn hay bị bỏ",
       "2 đối tác giới thiệu + 1 bộ lọc",
       "- Màn đối tác giới thiệu ở bot B TRỐNG\n"
       "- Điều kiện lọc xử lý theo quyết định MT-13\n"
       "- Không có ảnh bot của bot A lọt sang",
       spec="Đã hỏi leader",
       note="MT-13 + MT-28 — Backup (job) r343 · Improve backup media r78, r99 · [MN]Job r63-r64."),

    tc("Dữ liệu KHÔNG được copy", "FUNC-001", "Abnormal",
       "Sự kiện đặt lịch bản mới (release 29.3) — không sang bot nhận",
       CP + "\n- Bot A có sự kiện đặt lịch bản MỚI (release 29.3)",
       RUN + "3. Mở màn sự kiện bản mới ở bot B\n"
             "4. Đếm số sự kiện\n"
             "5. Nếu có sự kiện: mở chi tiết xem có mở được không, có báo lỗi không",
       "1 sự kiện bản mới",
       "- Màn sự kiện bản mới ở bot B TRỐNG\n"
       "- KHÔNG có sự kiện nào bị tạo ra ở trạng thái lỗi\n"
       "- ⚠️ Nếu có sự kiện mà mở ra báo lỗi thì raise bug",
       spec="Đã hỏi leader",
       note="MT-21 — Backup 1.0 r256 · Backup (job) r278. TC gốc bỏ trống kết quả mong đợi."),

    tc("Dữ liệu KHÔNG được copy", "DATA-001", "Abnormal",
       "Dữ liệu đã XOÁ ở bot gửi không sang bot nhận — rà đủ các tính năng",
       CP + "\n- Bot A có bản ghi ĐÃ XOÁ ở mỗi tính năng: thẻ, richmenu, mẫu tin, biểu mẫu, "
            "kịch bản, phân tích chéo",
       RUN + "3. Ở bot B, mở màn của TỪNG tính năng trong danh sách\n"
             "4. Tìm bản ghi đã xoá ở bot A trong danh sách đang dùng\n"
             "5. Mở màn「đã xoá」của từng tính năng ở bot B",
       "6 tính năng × ≥1 bản ghi đã xoá",
       "- KHÔNG có bản ghi đã xoá nào của bot A xuất hiện ở bot B\n"
       "- Cả trong danh sách đang dùng lẫn màn「đã xoá」\n"
       "- Số lượng bản ghi ở bot B = số bản ghi ĐANG DÙNG ở bot A",
       note="Gộp 6 tính năng vì CÙNG 1 kết quả. Nguồn: Backup (job) r118 (richmenu), r207 (tag), "
            "[MN]Job r44 (cross). Các tính năng còn lại là suy luận mở rộng của AI — cần Leader xác nhận."),

    tc("Dữ liệu KHÔNG được copy", "DATA-001", "Abnormal",
       "Số liệu thống kê và kết quả chạy không sang bot nhận",
       CP + "\n- Bot A có: thống kê lượt bấm richmenu, kết quả trả lời biểu mẫu, "
            "số người gắn thẻ, kết quả phân tích chéo, lịch sử nhập CSV",
       RUN + "3. Ở bot B, mở từng nơi trong danh sách và ghi lại số liệu\n"
             "4. Đối chiếu với số liệu ở bot A",
       "5 loại số liệu thống kê",
       "- TẤT CẢ số liệu ở bot B đều bắt đầu từ 0 hoặc trống\n"
       "- KHÔNG có số liệu nào của bot A lọt sang\n"
       "- Số liệu ở bot A không bị đụng",
       note="Gộp 5 loại vì CÙNG 1 kết quả. Nguồn: [MN]Job r47 (kết quả phân tích), r108 (lịch sử nhập CSV). "
            "3 loại còn lại là suy luận mở rộng của AI — cần Leader xác nhận."),

    # ═══════════════ 27. Hồi quy sau copy ═══════════════
    tc("Hồi quy sau copy", "REG-RUN-001", "Normal",
       "Bot GỬI giữ nguyên toàn bộ dữ liệu sau khi copy",
       CP + "\n- Đã ghi lại số lượng từng loại dữ liệu ở bot A TRƯỚC khi copy",
       RUN + "3. Quay lại BOT A, mở lần lượt màn của 13 loại dữ liệu\n"
             "4. Đếm lại số lượng từng loại\n"
             "5. So sánh với số đã ghi trước khi copy",
       "13 loại dữ liệu, ghi số lượng trước và sau",
       "- Số lượng từng loại ở bot A KHÔNG đổi\n"
       "- Không có bản ghi nào bị xoá, đổi tên hay đổi thứ tự\n"
       "- Không có bản ghi nào bị nhân đôi ở bot A",
       note="Nguồn: feature-spec §9.1 BK-Q09 —「dữ liệu ở tài khoản nguồn có bị thay đổi không? "
            "→ Không bị thay đổi — job chỉ SELECT từ nguồn」. TC này để đóng BK-Q09 bằng bằng chứng thật."),

    tc("Hồi quy sau copy", "REG-RUN-001", "Normal",
       "Bot GỬI vẫn hoạt động bình thường sau khi copy",
       CP + "\n- Đã copy xong A → B",
       "1. Ở bot A, tạo mới 1 thẻ và 1 mẫu tin\n"
       "2. Sửa 1 richmenu và lưu lại\n"
       "3. Gửi tin cho 1 bạn bè của bot A từ màn chat 1:1\n"
       "4. Kích hoạt 1 auto reply từ máy LINE thật\n"
       "5. Kiểm tra kịch bản đang chạy có gửi bước tiếp theo không",
       "5 thao tác thường ngày",
       "- Cả 5 thao tác đều chạy bình thường, không báo lỗi\n"
       "- Bạn bè của bot A nhận đúng tin\n"
       "- Kịch bản đang chạy không bị gián đoạn",
       env=P,
       note="Nguồn: Improve backup media r102-r121 (khối「Bot gốc check edit」). "
            "PRODUCTION theo RULE-08 (verify tới LINE thật)."),

    tc("Hồi quy sau copy", "REG-RUN-001", "Normal",
       "Bot NHẬN thao tác được trên dữ liệu vừa copy — sửa, sao chép, xoá, sắp xếp",
       CP + "\n- Đã copy xong A → B",
       "1. Ở bot B, sửa tên 1 thẻ đã copy và lưu\n"
       "2. Sao chép 1 mẫu tin đã copy\n"
       "3. Xoá 1 kịch bản đã copy\n"
       "4. Kéo đổi thứ tự richmenu\n"
       "5. Chuyển 1 biểu mẫu sang folder khác",
       "5 thao tác trên 5 loại dữ liệu",
       "- Cả 5 thao tác đều thành công, không báo lỗi\n"
       "- Thay đổi được lưu lại sau khi tải lại trang\n"
       "- Dữ liệu ở bot A KHÔNG bị ảnh hưởng",
       note="Gộp 5 thao tác vì cùng dạng kết quả. Nguồn: [MN]Job r48-r51 (cross) và r99-r102 (CSV) "
            "— mở rộng sang các tính năng khác là suy luận của AI. Cần Leader xác nhận."),

    tc("Hồi quy sau copy", "REG-RUN-001", "Normal",
       "Bot NHẬN gửi được tin dùng dữ liệu vừa copy",
       CP + "\n- Đã copy xong A → B\n- Bot B có ít nhất 3 bạn bè thật",
       "1. Ở bot B, tạo 1 lượt gửi tin hàng loạt dùng mẫu tin đã copy\n"
       "2. Đặt bộ lọc đối tượng bằng bộ lọc đã copy\n"
       "3. Xem trước nội dung và gửi thử cho chính mình\n"
       "4. Gửi thật và kiểm tra trên LINE\n"
       "5. Xem báo cáo kết quả gửi",
       "1 lượt gửi hàng loạt, 3 bạn bè",
       "- Chọn được mẫu tin và bộ lọc đã copy\n"
       "- Xem trước hiển thị đúng nội dung, ảnh hiện được\n"
       "- Bước 4: bạn bè của BOT B nhận đúng tin\n"
       "- Bước 5: báo cáo ghi nhận đúng số người nhận của bot B",
       env=P,
       note="Suy luận của AI — corpus không có TC gửi hàng loạt sau copy. "
            "Đây là cách khách hàng thực sự dùng dữ liệu vừa copy. Cần Leader xác nhận."),

    tc("Hồi quy sau copy", "DATA-001", "Abnormal",
       "Copy vào LOA ĐÃ CÓ SẴN dữ liệu — cộng dồn hay ghi đè?",
       "- Bot A có 5 thẻ, 3 mẫu tin, 2 kịch bản\n"
       "- Bot B ĐÃ CÓ SẴN 4 thẻ, 2 mẫu tin, 1 kịch bản (tên khác hẳn bot A)\n"
       "- Job nền đang bật",
       RUN + "3. Mở màn タグ / テンプレート / ステップ配信 ở bot B\n"
             "4. Đếm số lượng từng loại\n"
             "5. Kiểm tra dữ liệu CŨ của bot B còn nguyên không",
       "Bot A: 5 thẻ / 3 mẫu tin / 2 kịch bản · Bot B: 4 thẻ / 2 mẫu tin / 1 kịch bản",
       "- Ghi rõ hiện trạng: bot B có 9 thẻ (cộng dồn) hay 5 thẻ (ghi đè)?\n"
       "- Dữ liệu CŨ của bot B có bị xoá không\n"
       "- ⚠️ Nếu dữ liệu cũ của bot B bị xoá mà UI không cảnh báo thì đây là rủi ro MẤT DỮ LIỆU — raise bug",
       spec="Spec không ghi",
       note="Corpus KHÔNG có TC nào cho tình huống bot nhận đã có dữ liệu — mọi TC đều giả định bot nhận trống. "
            "Spec cũng không mô tả. Đây là VÙNG MÙ CẢ 2 PHÍA và là tình huống dùng thật phổ biến. "
            "Kết quả mong đợi do AI viết, cần Leader chốt."),

    tc("Hồi quy sau copy", "DATA-001", "Abnormal",
       "Copy 2 lần liên tiếp cùng cặp bot — dữ liệu có bị nhân đôi ở bot nhận không?",
       CP + "\n- Bot A có 5 thẻ, 3 mẫu tin, 2 kịch bản",
       RUN + "3. Đếm số lượng từng loại ở bot B sau lần copy 1\n"
             "4. Chạy copy A → B LẦN 2 và chờ hoàn tất\n"
             "5. Đếm lại số lượng từng loại ở bot B",
       "2 lần copy cùng cặp bot",
       "- Ghi rõ hiện trạng: sau lần 2 bot B có 5 hay 10 thẻ?\n"
       "- Nếu nhân đôi: mỗi thẻ xuất hiện 2 lần cùng tên\n"
       "- ⚠️ Nhân đôi dữ liệu là rủi ro cao (khách hàng phải xoá tay hàng trăm bản ghi) — cần Leader chốt",
       env=P,
       spec="Đã hỏi leader",
       note="Liên quan MT-06 và MT-26. [AI]UI r39 (TC-BK-038) có TC backup liên tiếp 3 lần nhưng "
            "kết quả chỉ ghi「Backup all cả 3 lần ... download csv bình thường」— KHÔNG nói dữ liệu ở bot đích ra sao."),

    tc("Hồi quy sau copy", "INTG-LINE-001", "Normal",
       "Richmenu đã copy đăng ký được lên LINE và thay thế richmenu cũ ở bot nhận",
       CP + "\n- Bot B ĐÃ CÓ 1 richmenu đang hiển thị trước khi copy\n"
            "- Bot A có 1 richmenu khác",
       RUN + "3. Ở bot B, bật hiển thị richmenu vừa copy\n"
             "4. Mở LINE bằng tài khoản bạn bè của bot B\n"
             "5. Quan sát richmenu dưới màn chat\n"
             "6. Tắt richmenu vừa copy và xem richmenu cũ có quay lại không",
       "Bot B có richmenu cũ + richmenu vừa copy",
       "- Bước 5: bạn bè bot B thấy richmenu vừa copy\n"
       "- Bước 6: tắt đi thì richmenu cũ hoặc trạng thái mặc định quay lại\n"
       "- Việc bật/tắt có tác dụng thật trên LINE",
       env=P,
       note="Nguồn: Backup (job) r120 · Backup 1.0 r53. Liên quan MT-10 (`queue_richmenu_id`)."),

    tc("Hồi quy sau copy", "JOB-001", "Normal",
       "Các job nền chạy đúng trên dữ liệu vừa copy ở bot nhận",
       CP + "\n- Đã copy sang bot B: kịch bản có bước theo giờ, nhắc lịch, lịch chạy hành động, "
            "thông tin bạn bè kiểu ngày tháng có hành động theo giờ",
       "1. Ở bot B, chỉnh các mốc thời gian về gần hiện tại\n"
       "2. Cho 1 bạn bè của bot B vào kịch bản\n"
       "3. Đặt chỗ sự kiện để kích hoạt nhắc lịch\n"
       "4. Chờ qua các mốc thời gian\n"
       "5. Kiểm tra bạn bè bot B nhận được gì trên LINE",
       "4 loại job × 1 bạn bè bot B",
       "- Cả 4 loại job đều chạy đúng giờ trên bot B\n"
       "- Bạn bè bot B nhận đủ tin của cả 4 loại\n"
       "- Bạn bè bot A KHÔNG nhận thêm tin nào\n"
       "- Không có tin nào gửi nhầm sang bot A",
       env=P,
       note="Nguồn: Backup (job) r141-r143 (kiểm tra ngẫu nhiên tính năng khác) mở rộng theo RULE-06. "
            "TC tổng hợp do AI viết để phủ RULE-08 (job). Cần Leader duyệt."),

    tc("Hồi quy sau copy", "REG-SHARED-001", "Normal",
       "Đếm SỐ LƯỢNG từng loại dữ liệu ở bot nhận khớp chính xác bot gửi",
       CP + "\n- Đã ghi lại số lượng CHÍNH XÁC của 13 loại dữ liệu ở bot A",
       RUN + "3. Ở bot B, mở màn của 13 loại và đếm số lượng từng loại\n"
             "4. Lập bảng đối chiếu số lượng 2 bên\n"
             "5. Với loại nào lệch, mở ra tìm bản ghi bị thiếu",
       "13 loại dữ liệu, ghi số lượng cụ thể",
       "- Số lượng từng loại ở bot B BẰNG số bản ghi ĐANG DÙNG ở bot A\n"
       "- Không loại nào thiếu bản ghi ở cuối danh sách\n"
       "- Nếu loại nào lệch thì ghi rõ lệch bao nhiêu và bản ghi nào thiếu",
       note="TC đối chiếu tổng do AI viết — corpus có TC lẻ cho từng loại nhưng không có TC đếm tổng. "
            "Đây là chốt chặn phát hiện lỗi cắt danh sách. Cần Leader duyệt."),

    tc("Hồi quy sau copy", "SEC-ISO-001", "Normal",
       "Hai bot hoàn toàn độc lập sau khi copy — sửa 1 bên không ảnh hưởng bên kia",
       CP + "\n- Đã copy xong A → B",
       "1. Ở bot B, sửa nội dung 1 mẫu tin, 1 thẻ, 1 kịch bản đã copy\n"
       "2. Quay lại bot A, mở 3 bản ghi gốc và đối chiếu\n"
       "3. Ở bot A, sửa nội dung 3 bản ghi đó\n"
       "4. Quay lại bot B và đối chiếu",
       "3 loại dữ liệu × 2 chiều sửa",
       "- Bước 2: 3 bản ghi ở bot A hoàn toàn không đổi\n"
       "- Bước 4: 3 bản ghi ở bot B giữ nguyên nội dung đã sửa ở bước 1\n"
       "- Không có bản ghi nào dùng chung giữa 2 bot",
       note="Nguồn: Backup (job) r80 (nguyên tắc độc lập của bộ lọc) mở rộng cho toàn bộ dữ liệu. "
            "Cần Leader duyệt."),

    # ═══════════════ 28. Môi trường & Legacy ═══════════════
    tc("Môi trường & Legacy", "ENV-001", "Normal",
       "Chạy copy trên PRODUCTION — đối chiếu với kết quả trên môi trường thử",
       "- Đã chạy xong bộ TC chính trên môi trường thử\n"
       "- Có 2 LOA thật trên PRODUCTION được phép dùng để thử copy\n"
       "- Đã được Leader duyệt cho chạy trên PRODUCTION",
       "1. Dựng bộ dữ liệu rút gọn ở LOA nguồn trên PRODUCTION\n"
       "2. Chạy copy và ghi lại thời gian hoàn tất\n"
       "3. Đối chiếu dữ liệu ở LOA nhận\n"
       "4. So sánh hành vi với kết quả trên môi trường thử",
       "Bộ dữ liệu rút gọn: 5 thẻ · 3 mẫu tin có ảnh · 1 kịch bản · 1 richmenu · 1 biểu mẫu",
       "- Hành vi trên PRODUCTION GIỐNG môi trường thử\n"
       "- Media (ảnh, video) hiển thị đúng trên PRODUCTION\n"
       "- Richmenu đăng ký được lên LINE thật\n"
       "- Ghi rõ mọi điểm khác biệt giữa 2 môi trường",
       env=P,
       note="RULE-08 — media, đăng ký LINE API và job nền BẮT BUỘC verify trên PRODUCTION. "
            "Corpus có cột kết quả riêng cho「Test Result account test」/「Staging」/「Step」 "
            "nhưng không có TC đối chiếu môi trường."),

    tc("Môi trường & Legacy", "ENV-002", "Abnormal",
       "Cấu hình bảng cần copy — xác định nguồn cấu hình thật sự đang dùng",
       "- Có quyền xem cấu hình phía máy chủ\n- Nhờ Dev hỗ trợ đối chiếu",
       "1. Nhờ Dev cho biết dịch vụ job đọc bảng cấu hình nào\n"
       "2. So sánh nội dung 2 bảng cấu hình cùng cấu trúc\n"
       "3. Ghi lại danh sách bảng được bật ở mỗi bảng cấu hình\n"
       "4. Chạy 1 lần copy và đối chiếu tập dữ liệu thực tế sang bot nhận với danh sách đó",
       "2 bảng cấu hình cùng cấu trúc",
       "- Xác định được bảng cấu hình thật sự đang dùng\n"
       "- Danh sách bảng được bật khớp với dữ liệu thực tế copy sang\n"
       "- Nếu 2 bảng cấu hình lệch nhau thì ghi rõ lệch ở mục nào",
       env=P,
       spec="Đã hỏi leader",
       note="MT-29 — feature-spec §9.3 mục 4 tự nhận CHƯA RÕ Spring Boot đọc `backup_config` hay "
            "`backup_config_dung`. Corpus KHÔNG có TC nào. ⚠️ TC viết THUẦN THEO SPEC — cần Leader duyệt trước khi giao."),

    tc("Môi trường & Legacy", "ENV-002", "Abnormal",
       "Danh sách bảng được copy khớp giữa các môi trường",
       "- Có quyền xem cấu hình trên cả môi trường thử và PRODUCTION\n- Nhờ Dev hỗ trợ",
       "1. Lấy danh sách bảng được bật copy ở môi trường thử\n"
       "2. Lấy danh sách tương ứng trên PRODUCTION\n"
       "3. So sánh 2 danh sách\n"
       "4. Ghi rõ bảng nào có ở môi trường này mà không có ở môi trường kia",
       "2 môi trường",
       "- 2 danh sách GIỐNG NHAU\n"
       "- Nếu lệch: ghi rõ bảng nào lệch — vì lệch nghĩa là kết quả test trên môi trường thử "
       "KHÔNG phản ánh đúng PRODUCTION",
       env=P,
       spec="Đã hỏi leader",
       note="MT-29 — TC do AI bổ sung theo ENV-002. Corpus không có TC. Cần Leader duyệt."),

    tc("Môi trường & Legacy", "COMPAT-LEGACY-001", "Abnormal",
       "Copy LOA có nhiều dữ liệu kiểu CŨ",
       CP + "\n- Bot A là LOA đã dùng ≥3 năm, có: ảnh đường dẫn kiểu cũ, kịch bản có cài richmenu kiểu cũ, "
            "richmenu có dữ liệu lịch hiển thị kiểu cũ, biểu mẫu tạo trước đợt nâng cấp, "
            "mẫu tin có mã chèn sản phẩm kiểu cũ",
       RUN + "3. Ở bot B, mở lần lượt 5 nhóm dữ liệu kiểu cũ\n"
             "4. Kiểm tra mở được không, có báo lỗi không\n"
             "5. Với mỗi nhóm: thử sửa và lưu lại\n"
             "6. Gửi thử cho bạn bè bot B",
       "5 nhóm dữ liệu kiểu cũ",
       "- Cả 5 nhóm mở được ở bot B, không báo lỗi\n"
       "- Ảnh kiểu cũ hiển thị được (xem MT-23)\n"
       "- Sửa và lưu được bình thường\n"
       "- Bước 6: bạn bè nhận được nội dung đúng",
       env=P,
       spec="Đã hỏi leader",
       note="Tổng hợp các nhánh「data cũ」rải rác trong corpus (improve url image, Backup (job) r115-r117, r137, r149). "
            "TC tổng do AI viết. Cần Leader duyệt."),

    tc("Môi trường & Legacy", "PERF-LARGE-001", "Boundary",
       "Bảng ánh xạ id tăng trưởng lớn — copy vẫn chạy đúng",
       "- Môi trường đã có lượng dữ liệu ánh xạ id lớn (≥100.000 bản ghi)\n"
       "- Bot A có bộ dữ liệu đầy đủ 13 loại",
       RUN + "3. Ghi lại thời gian hoàn tất\n"
             "4. Đối chiếu số lượng dữ liệu ở bot B\n"
             "5. Chạy thêm 1 lần copy nữa và so thời gian với lần trước",
       "Bảng ánh xạ id ≥100.000 bản ghi",
       "- Copy hoàn tất, không chuyển sang trạng thái thất bại\n"
       "- Dữ liệu ở bot B đầy đủ\n"
       "- Bước 5: thời gian lần 2 KHÔNG chậm đi rõ rệt so với lần 1",
       env=P,
       note="feature-spec §3.1 ghi bảng ánh xạ id có「155.241 rows trong production」. "
            "Corpus KHÔNG có TC hiệu năng. TC do AI bổ sung theo PERF-LARGE-001. Cần Leader duyệt."),

    tc("Môi trường & Legacy", "DEPLOY-LIVE-001", "Abnormal",
       "Triển khai mã mới trong lúc đang có backup chạy",
       "- Đang có 1 backup ở trạng thái đang thực hiện\n"
       "- Có thể triển khai lại dịch vụ web trên môi trường thử",
       "1. Bắt đầu 1 lượt copy dữ liệu lớn\n"
       "2. Trong lúc job đang chạy, triển khai lại dịch vụ web (không đụng dịch vụ job)\n"
       "3. Theo dõi trạng thái backup\n"
       "4. Sau khi triển khai xong, mở lại màn データコピー",
       "1 backup đang chạy + 1 lần triển khai web",
       "- Job nền KHÔNG bị gián đoạn (job chạy ở dịch vụ riêng)\n"
       "- Backup vẫn đi tới trạng thái hoàn tất\n"
       "- Bước 4: bảng lịch sử phản ánh đúng trạng thái\n"
       "- Không có bản ghi bị kẹt vô thời hạn",
       env=P,
       spec="Spec không ghi",
       note="Kết quả mong đợi do AI viết theo DEPLOY-LIVE-001 — corpus và spec đều không có TC. "
            "Cần Leader xác nhận."),

    tc("Môi trường & Legacy", "COMPAT-LEGACY-001", "Abnormal",
       "Đo lại các hạng mục có TC nguồn trên 2 năm tuổi",
       "- Đã chuẩn bị đủ dữ liệu cho các hạng mục trong danh sách\n"
       "- Bot A và bot B sẵn sàng",
       "1. Chạy lại toàn bộ hạng mục trong danh sách ở cột dữ liệu test\n"
       "2. Ghi lại kết quả thực tế từng hạng mục\n"
       "3. Đối chiếu với kết quả ghi trong TC nguồn\n"
       "4. Lập danh sách hạng mục có kết quả KHÁC so với TC nguồn",
       "① Backup 1.0 (03/2023) — toàn bộ khối autoreply / richmenu / scenario / template bản cũ\n"
       "② Backup (job) khối gốc (05/2023)\n"
       "③ Improve backup media (2024-01) — toàn bộ ma trận media\n"
       "④ Backup image (không có ngày trong tab Info, cũ hơn improve url image 31/10/2024)",
       "- Ghi rõ hạng mục nào còn đúng, hạng mục nào đã đổi hành vi\n"
       "- Với hạng mục đổi hành vi: xác định là do cải tiến hay do lỗi\n"
       "- ⚠️ KHÔNG được coi kết quả trong TC nguồn là hiện trạng — phải đo lại",
       env=P,
       spec="Đã hỏi leader",
       note="Quy tắc TC > 2 năm tuổi. Tính tới 2026-08-25: Backup 1.0 và Backup (job) khối gốc đã 3 năm; "
            "Improve backup media đã 2 năm 7 tháng. Đây là TC ĐIỀU PHỐI — Leader nên giao thành 1 đợt rà soát riêng."),

    tc("Môi trường & Legacy", "SEC-ISO-001", "Abnormal",
       "Copy giữa 2 LOA thuộc 2 KHÁCH HÀNG khác nhau — kiểm tra rò rỉ dữ liệu",
       "- Bot A thuộc khách hàng X, bot B thuộc khách hàng Y (2 tài khoản hoàn toàn khác nhau)\n"
       "- Khách hàng X cung cấp mã copy cho khách hàng Y (kịch bản dùng thật)\n"
       "- Job nền đang bật",
       RUN + "3. Đăng nhập tài khoản của khách hàng Y, kiểm tra dữ liệu ở bot B\n"
             "4. Rà TẤT CẢ nơi có thể chứa dữ liệu cá nhân: danh sách bạn bè, lịch sử chat, "
             "câu trả lời biểu mẫu, danh sách đặt chỗ, file CSV đã xuất\n"
             "5. Ghi rõ có bản ghi nào chứa dữ liệu cá nhân của khách hàng X không",
       "2 tài khoản khách hàng khác nhau",
       "- Bot B nhận đúng phần CẤU HÌNH (thẻ, mẫu tin, kịch bản...)\n"
       "- TUYỆT ĐỐI KHÔNG có dữ liệu cá nhân của khách hàng X: không bạn bè, không lịch sử chat, "
       "không câu trả lời biểu mẫu, không danh sách đặt chỗ\n"
       "- ⚠️ Nếu có bất kỳ dữ liệu cá nhân nào lọt sang thì đây là sự cố bảo mật — dừng test và báo ngay",
       env=P,
       note="Nguồn: [MN]Job r97 —「Check back up từ bot User A, sang bot của user B」(chỉ có ở khối CSV). "
            "TC này mở rộng thành rà soát bảo mật toàn diện — đây là kịch bản dùng thật của tính năng "
            "(nhân bản cấu hình cho khách hàng khác). Cần Leader duyệt."),

    tc("Môi trường & Legacy", "PERM-003", "Abnormal",
       "Nhân viên của bot nhận thao tác được trên dữ liệu vừa copy",
       CP + "\n- Đã copy xong A → B\n- Bot B có tài khoản Nhân viên được cấp quyền một số màn",
       "1. Đăng nhập bằng tài khoản Nhân viên của bot B\n"
       "2. Mở các màn được cấp quyền (thẻ, mẫu tin, kịch bản)\n"
       "3. Kiểm tra dữ liệu vừa copy có hiển thị không\n"
       "4. Thử sửa 1 bản ghi vừa copy\n"
       "5. Mở Sidebar tìm mục データコピー",
       "1 tài khoản Nhân viên có quyền 3 màn",
       "- Nhân viên nhìn thấy dữ liệu vừa copy ở các màn được cấp quyền\n"
       "- Sửa được bình thường theo đúng quyền đã cấp\n"
       "- Bước 5: mục データコピー KHÔNG hiển thị với Nhân viên\n"
       "- Không có dữ liệu nào bị ẩn đi chỉ vì nó đến từ copy",
       spec="Đã hỏi leader",
       note="MT-25 — corpus có 5 dòng「check bot staff」nhưng đều bỏ trống kết quả. "
            "TC này tách riêng góc「nhân viên dùng dữ liệu SAU copy」, khác với「nhân viên THỰC HIỆN copy」. "
            "Cần Leader duyệt."),
]
