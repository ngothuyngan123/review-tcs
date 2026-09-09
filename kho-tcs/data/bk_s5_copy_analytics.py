# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 22-24: フィルタ / クロス分析 / CSV管理.

⚠️ Toàn bộ nhóm クロス分析 và CSV管理 phụ thuộc MT-04 (2 tính năng này có nằm trong
danh sách「コピーされるデータ」hiển thị cho người dùng hay không).

Quy ước: **bot A = LOA gửi**, **bot B = LOA nhận** (theo spec; xem MT-01).
"""
from _common import tc

CP = ("- Bot A (LOA gửi) và bot B (LOA nhận) đều plan Standard/Pro, job nền đang bật\n"
      "- Bot B là LOA TRỐNG (chưa có dữ liệu cùng loại) để dễ đối chiếu\n"
      "- Đã dựng xong dữ liệu ở bot A theo mục điều kiện riêng bên dưới")
RUN = "1. Ở bot A, xác nhận dữ liệu đã dựng đúng\n2. Thực hiện copy A → B và chờ trạng thái hoàn tất\n"
CROSS = ("- Chỉ copy ĐIỀU KIỆN, KHÔNG copy số người thoả mãn\n"
         "- Sau khi copy, sửa/thêm/xoá điều kiện ở bot B thì danh sách người thoả mãn "
         "tính lại theo dữ liệu của BOT B")

S5 = [
    # ═══════════════ 22. Copy フィルタ ═══════════════
    tc("Copy フィルタ", "FUNC-001", "Normal",
       "Copy bộ lọc kiểu VÀ và kiểu HOẶC — giữ đúng cách ghép điều kiện",
       CP + "\n- Bot A có 1 bộ lọc ghép kiểu VÀ (3 điều kiện) và 1 bộ lọc ghép kiểu HOẶC (3 điều kiện)",
       RUN + "3. Ở bot B, mở tính năng có dùng bộ lọc (ví dụ 一斉配信) và mở 2 bộ lọc đã copy\n"
             "4. Đối chiếu kiểu ghép và số điều kiện của từng bộ lọc\n"
             "5. Bấm xem danh sách bạn bè thoả mãn ở bot B",
       "1 bộ lọc VÀ (3 điều kiện) · 1 bộ lọc HOẶC (3 điều kiện)",
       "- Kiểu ghép (VÀ / HOẶC) giữ đúng ở bot B\n"
       "- Đủ 3 điều kiện mỗi bộ lọc, đúng thứ tự\n"
       "- Bước 5: danh sách bạn bè tính theo dữ liệu của BOT B, không phải bot A",
       note="Nguồn: Backup (job) r323 —「Filter and / filter or」."),

    tc("Copy フィルタ", "DATA-REF-001", "Normal",
       "Copy điều kiện lọc theo thẻ — trỏ đúng thẻ của bot nhận",
       CP + "\n- Bot A có thẻ「タグ-FL1」「タグ-FL2」và bộ lọc dùng 2 thẻ đó",
       RUN + "3. Mở màn タグ ở bot B, xác nhận 2 thẻ đã copy\n"
             "4. Mở bộ lọc ở bot B, xem điều kiện thẻ trỏ tới thẻ nào\n"
             "5. Xem danh sách bạn bè thoả mãn",
       "2 thẻ",
       "- Điều kiện lọc trỏ tới thẻ của BOT B\n"
       "- KHÔNG trỏ tới thẻ của bot A\n"
       "- Bước 5: danh sách bạn bè tính theo thẻ ở bot B",
       note="Nguồn: Backup (job) r324."),

    tc("Copy フィルタ", "FUNC-001", "Normal",
       "Copy điều kiện lọc theo tên bạn bè — cả tên LINE và tên hệ thống",
       CP + "\n- Bot A có 1 bộ lọc theo tên LINE và 1 bộ lọc theo tên hệ thống",
       RUN + "3. Mở 2 bộ lọc ở bot B\n"
             "4. Đối chiếu loại tên được chọn và chuỗi tìm kiếm\n"
             "5. Xem danh sách bạn bè thoả mãn",
       "① tên LINE chứa「田中」② tên hệ thống chứa「テスト」",
       "- Cả 2 bộ lọc giữ đúng loại tên và chuỗi tìm kiếm\n"
       "- Bước 5: lọc đúng bạn bè của BOT B",
       note="Gộp 2 loại vì cùng 1 kết quả. Nguồn: Backup (job) r325-r326."),

    tc("Copy フィルタ", "FUNC-DATE-001", "Normal",
       "Copy điều kiện lọc theo ngày kết bạn — 2 kiểu nhập",
       CP + "\n- Bot A có 1 bộ lọc nhập ngày/tháng/năm cụ thể và 1 bộ lọc nhập số ngày gần đây",
       RUN + "3. Mở 2 bộ lọc ở bot B\n"
             "4. Đối chiếu kiểu nhập và giá trị\n"
             "5. Xem danh sách bạn bè thoả mãn ở bot B",
       "① từ 2026-01-01 đến 2026-06-30 ② trong 30 ngày gần đây",
       "- Cả 2 bộ lọc giữ đúng kiểu nhập và giá trị\n"
       "- Bước 5: bộ lọc「số ngày gần đây」tính theo NGÀY HIỆN TẠI, không phải ngày copy",
       note="Gộp 2 kiểu ở bước đối chiếu. Nguồn: Backup (job) r327-r328."),

    tc("Copy フィルタ", "DATA-REF-001", "Normal",
       "Copy điều kiện lọc theo tình trạng kịch bản — đủ 5 điều kiện con",
       CP + "\n- Bot A có kịch bản và 5 bộ lọc, mỗi bộ dùng 1 trong 5 điều kiện tình trạng kịch bản",
       RUN + "3. Mở màn ステップ配信 ở bot B, xác nhận kịch bản đã copy\n"
             "4. Mở 5 bộ lọc ở bot B, đối chiếu điều kiện và kịch bản được trỏ tới\n"
             "5. Xem danh sách bạn bè thoả mãn của từng bộ lọc",
       "5 điều kiện tình trạng kịch bản khác nhau",
       "- Cả 5 bộ lọc trỏ tới kịch bản của BOT B\n"
       "- Điều kiện con giữ đúng, không bị quy về cùng 1 điều kiện\n"
       "- Bước 5: danh sách tính theo dữ liệu bot B",
       note="Gộp 5 điều kiện vì cùng 1 kết quả. Nguồn: Backup (job) r329-r333 (đk1 → đk5)."),

    tc("Copy フィルタ", "DATA-REF-001", "Abnormal",
       "Bộ lọc chứa điều kiện MÃ QR — điều kiện không được copy",
       CP + "\n- Bot A có 2 bộ lọc:\n"
            "  · bộ lọc 1: CHỈ có 1 điều kiện mã QR\n"
            "  · bộ lọc 2: ghép VÀ gồm điều kiện thẻ + điều kiện mã QR",
       RUN + "3. Mở cả 2 bộ lọc ở bot B\n"
             "4. Ghi rõ: bộ lọc còn tồn tại không, còn mấy điều kiện\n"
             "5. Xem danh sách bạn bè thoả mãn của bộ lọc 2 ở bot B và so với bot A",
       "Bộ lọc 1: 1 điều kiện QR · Bộ lọc 2: thẻ VÀ QR",
       "- Kết quả theo quyết định MT-13 — ghi rõ hiện trạng:\n"
       "  · bộ lọc 1: bị bỏ hoàn toàn hay còn nhưng rỗng điều kiện?\n"
       "  · bộ lọc 2: còn cả 2 điều kiện, hay chỉ còn điều kiện thẻ?\n"
       "- ⚠️ Nếu bộ lọc 2 chỉ còn điều kiện thẻ thì bộ lọc ở bot B LỎNG HƠN bot A "
       "⇒ gửi tin sai đối tượng — phải raise bug",
       spec="Đã hỏi leader",
       note="MT-13 — Backup (job) r334:「không backup ⇒ không tạo bản ghi filter_v2 đối với type này」. "
            "Corpus KHÔNG nói bộ lọc CHA xử lý ra sao. Đây là rủi ro gửi tin sai đối tượng."),

    tc("Copy フィルタ", "DATA-REF-001", "Normal",
       "Copy điều kiện lọc theo trang chuyển đổi",
       CP + "\n- Bot A có trang chuyển đổi và bộ lọc theo điều kiện đã truy cập trang đó",
       RUN + "3. Mở màn コンバージョン ở bot B, xác nhận đã copy\n"
             "4. Mở bộ lọc ở bot B, xem điều kiện trỏ tới trang chuyển đổi nào\n"
             "5. Xem danh sách bạn bè thoả mãn",
       "1 trang chuyển đổi",
       "- Điều kiện trỏ tới trang chuyển đổi của BOT B\n"
       "- Bước 5: danh sách tính theo lượt truy cập ở bot B",
       note="Nguồn: Backup (job) r335. Xem thêm MT-17."),

    tc("Copy フィルタ", "FUNC-001", "Normal",
       "Copy điều kiện lọc theo tình trạng xác nhận",
       CP + "\n- Bot A có 1 bộ lọc「chưa xác nhận」và 1 bộ lọc「đã xác nhận」",
       RUN + "3. Mở 2 bộ lọc ở bot B\n4. Đối chiếu điều kiện\n5. Xem danh sách bạn bè thoả mãn",
       "2 bộ lọc, 2 trạng thái xác nhận",
       "- Cả 2 bộ lọc giữ đúng điều kiện, không bị đảo\n"
       "- Bước 5: danh sách tính theo dữ liệu bot B",
       note="Gộp 2 trạng thái vì cùng 1 kết quả. Nguồn: Backup (job) r336-r337."),

    tc("Copy フィルタ", "DATA-REF-001", "Normal",
       "Copy điều kiện lọc theo thông tin bạn bè — đủ 4 kiểu",
       CP + "\n- Bot A có 4 thông tin bạn bè (mô tả, lựa chọn, ngày tháng, điểm) "
            "và 4 bộ lọc tương ứng",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận 4 mục đã copy\n"
             "4. Mở 4 bộ lọc ở bot B, đối chiếu điều kiện và mục được trỏ tới\n"
             "5. Xem danh sách bạn bè thoả mãn của từng bộ lọc",
       "4 kiểu: mô tả (chứa「東京」) · lựa chọn (= A) · ngày tháng (trong tháng này) · điểm (≥ 10)",
       "- Cả 4 bộ lọc trỏ tới thông tin bạn bè của BOT B\n"
       "- Điều kiện so sánh (chứa / bằng / khoảng / ≥) giữ đúng\n"
       "- Bước 5: danh sách tính theo giá trị của bạn bè bot B",
       note="Gộp 4 kiểu vì cùng 1 kết quả. Nguồn: Backup (job) r338-r341."),

    tc("Copy フィルタ", "DATA-REF-001", "Normal",
       "Copy điều kiện lọc theo trạng thái xử lý",
       CP + "\n- Bot A có trạng thái xử lý「対応中」và bộ lọc theo trạng thái đó",
       RUN + "3. Mở màn cài đặt trạng thái ở bot B, xác nhận đã copy\n"
             "4. Mở bộ lọc ở bot B, xem điều kiện trỏ tới trạng thái nào\n"
             "5. Xem danh sách bạn bè thoả mãn",
       "1 trạng thái xử lý",
       "- Điều kiện trỏ tới trạng thái của BOT B\n"
       "- Bước 5: danh sách tính theo bạn bè bot B",
       note="Nguồn: Backup (job) r342."),

    tc("Copy フィルタ", "DATA-REF-001", "Abnormal",
       "Bộ lọc chứa điều kiện ĐỐI TÁC GIỚI THIỆU — điều kiện không được copy",
       CP + "\n- Bot A có 2 bộ lọc: 1 chỉ có điều kiện đối tác giới thiệu, "
            "1 ghép VÀ gồm thẻ + đối tác giới thiệu",
       RUN + "3. Mở cả 2 bộ lọc ở bot B\n"
             "4. Ghi rõ bộ lọc còn tồn tại không, còn mấy điều kiện\n"
             "5. Xem danh sách bạn bè thoả mãn của bộ lọc ghép và so với bot A",
       "Bộ lọc 1: chỉ đối tác giới thiệu · Bộ lọc 2: thẻ VÀ đối tác giới thiệu",
       "- Kết quả theo quyết định MT-13, ghi rõ hiện trạng như TC điều kiện mã QR\n"
       "- ⚠️ Nếu bộ lọc ghép chỉ còn điều kiện thẻ thì bộ lọc LỎNG HƠN bot A — raise bug",
       spec="Đã hỏi leader",
       note="MT-13 — Backup (job) r343:「không backup ⇒ không tạo bản ghi filter_v2 đối với type này」."),

    tc("Copy フィルタ", "FUNC-001", "Normal",
       "Copy điều kiện lọc bạn bè mới / bạn bè cũ và điều kiện xem trước nội dung",
       CP + "\n- Bot A có 1 bộ lọc theo bạn bè mới/cũ và 1 bộ lọc theo xem trước nội dung",
       RUN + "3. Mở 2 bộ lọc ở bot B\n4. Đối chiếu điều kiện\n5. Xem danh sách bạn bè thoả mãn",
       "2 bộ lọc",
       "- Cả 2 bộ lọc giữ đúng điều kiện\n"
       "- Bước 5: danh sách tính theo dữ liệu bot B",
       note="Gộp 2 loại vì cùng 1 kết quả. Nguồn: Backup (job) r344-r345."),

    tc("Copy フィルタ", "SEC-ISO-001", "Normal",
       "Bộ lọc ở 2 bot hoàn toàn độc lập sau khi copy",
       CP + "\n- Đã copy bộ lọc từ A sang B",
       "1. Ở bot B, thêm 1 điều kiện vào bộ lọc đã copy\n"
       "2. Quay lại bot A, mở bộ lọc gốc và đếm số điều kiện\n"
       "3. Ở bot A, xoá 1 điều kiện khỏi bộ lọc gốc\n"
       "4. Quay lại bot B, mở bộ lọc và đếm số điều kiện",
       "1 bộ lọc 3 điều kiện",
       "- Bước 2: bộ lọc ở bot A vẫn 3 điều kiện\n"
       "- Bước 4: bộ lọc ở bot B vẫn 4 điều kiện (3 gốc + 1 vừa thêm)\n"
       "- Hai bộ lọc là 2 bản ghi riêng, không dùng chung",
       note="Nguồn: Backup (job) r80 —「Khi edit filter ở bot nguồn hoặc bot đích thì không ảnh hưởng đến "
            "filter của bot còn lại」. Áp dụng cho toàn bộ nhóm bộ lọc."),

    # ═══════════════ 23. Copy クロス分析 ═══════════════
    tc("Copy クロス分析", "FUNC-001", "Normal",
       "Copy folder phân tích chéo — đủ số lượng, đúng thứ tự, không gồm mục đã xoá",
       CP + "\n- Bot A có 2 folder phân tích chéo, mỗi folder 3 mục; trong đó có 1 mục đã xoá",
       RUN + "3. Mở màn クロス分析 ở bot B\n"
             "4. Đếm folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số mục phân tích",
       "2 folder × 3 mục · 1 mục đã xoá tên「CROSS-DEL」",
       "- Bot B có đủ 2 folder, đúng tên, đúng thứ tự\n"
       "- Số mục mỗi folder khớp bot A\n"
       "- Mục「CROSS-DEL」KHÔNG xuất hiện ở bot B, kể cả ở màn đã xoá",
       spec="Đã hỏi leader",
       note="MT-04 + MT-15 — [MN]Job TCs r15 (category theo kind) và r44 (không copy mục đã xoá)."),

    tc("Copy クロス分析", "FUNC-001", "Normal",
       "Copy tên và vị trí hiển thị của mục phân tích chéo",
       CP + "\n- Bot A có 4 mục phân tích chéo với tên và thứ tự khác nhau",
       RUN + "3. Mở màn クロス分析 ở bot B\n4. Đối chiếu tên và thứ tự 4 mục",
       "4 mục, 1 tên có tiếng Nhật và emoji",
       "- Bot B có đủ 4 mục, đúng tên (giữ tiếng Nhật và emoji)\n"
       "- Thứ tự hiển thị giống hệt bot A",
       spec="Đã hỏi leader",
       note="MT-04 + MT-15 — [MN]Job TCs r16-r17."),

    tc("Copy クロス分析", "FUNC-001", "Normal",
       "Mục phân tích chéo nằm đúng folder ở bot nhận",
       CP + "\n- Bot A có 1 mục phân tích ở folder mặc định và 1 mục ở folder tự tạo",
       RUN + "3. Mở màn クロス分析 ở bot B\n4. Kiểm tra 2 mục nằm ở folder nào",
       "1 mục folder mặc định + 1 mục folder tự tạo",
       "- Mỗi mục nằm ĐÚNG folder tương ứng ở bot B\n"
       "- KHÔNG có mục nào bị gán vào folder của bot A hoặc folder không tồn tại",
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r18-r19 —「Backup đúng folder của bot đích」."),

    tc("Copy クロス分析", "DATA-REF-001", "Normal",
       "Copy mục phân tích theo THẺ — 1 thẻ và nhiều thẻ",
       CP + "\n- Bot A có 1 mục phân tích chọn 1 thẻ và 1 mục chọn 4 thẻ",
       RUN + "3. Mở màn タグ ở bot B, xác nhận các thẻ đã copy\n"
             "4. Mở 2 mục phân tích ở bot B, xem thẻ được chọn\n"
             "5. Đếm số thẻ được chọn và đối chiếu với bot A",
       "1 mục 1 thẻ · 1 mục 4 thẻ",
       "- Cả 2 mục trỏ tới thẻ của BOT B\n"
       "- Số thẻ được chọn khớp bot A (1 và 4), không thiếu thẻ nào\n" + CROSS,
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r20-r21 —「Tạo ra các tag_id ... Chỉ back up điều kiện, "
            "không back up số friend thỏa mãn」."),

    tc("Copy クロス分析", "DATA-REF-001", "Normal",
       "Copy mục phân tích theo THÔNG TIN BẠN BÈ",
       CP + "\n- Bot A có mục phân tích chọn thông tin bạn bè",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận thông tin đã copy\n"
             "4. Mở mục phân tích ở bot B, xem thông tin được chọn\n"
             "5. Thử chọn thêm thông tin khác xem giao diện cho chọn mấy mục",
       "1 mục phân tích theo thông tin bạn bè",
       "- Mục phân tích trỏ tới thông tin của BOT B\n"
       "- Bước 5: ghi lại giới hạn số thông tin chọn được (corpus ghi「Chỉ chọn đc 1 loại friend info」)\n" + CROSS,
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r22-r23. Ô Note gốc r22 ghi「Chỉ chọn đc 1 loại friend info」— "
            "nhưng r23 lại có TC「Case chọn nhiều friend info」. Cần Leader làm rõ."),

    tc("Copy クロス分析", "FUNC-DATE-001", "Normal",
       "Copy mục phân tích theo NGÀY KẾT BẠN — số người được tính lại theo bot nhận",
       CP + "\n- Bot A có 1 mục phân tích theo 1 tháng và 1 mục theo 3 tháng\n"
            "- Bot A và bot B có số bạn bè kết bạn trong khoảng đó KHÁC nhau rõ rệt",
       RUN + "3. Mở 2 mục phân tích ở bot B, đối chiếu khoảng thời gian đã chọn\n"
             "4. Xem SỐ NGƯỜI ở kết quả phân tích của bot B\n"
             "5. Đối chiếu số người đó với số bạn bè thật của bot B trong cùng khoảng",
       "① tháng 2026-06 ② tháng 2026-04 đến 2026-06; bot A 120 người, bot B 37 người",
       "- Khoảng thời gian giữ đúng ở bot B\n"
       "- Số người ở bot B tính theo BẠN BÈ CỦA BOT B (37), KHÔNG phải số của bot A (120)\n"
       "- Việc tính lại xảy ra tự động, không cần bấm gì thêm",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-14 + MT-15 — [MN]Job TCs r20/r24-r25 —「tại bot nhận backup sẽ thực hiện COUNT LẠI các friend "
            "nằm trong date from-to」. ⚠️ Spec KHÔNG có job nào làm việc này. PRODUCTION theo RULE-08."),

    tc("Copy クロス分析", "STATE-001", "Normal",
       "Copy mục phân tích ở trạng thái nháp và trạng thái đã đủ điều kiện",
       CP + "\n- Bot A có 1 mục phân tích ở trạng thái nháp (chưa đủ điều kiện) "
            "và 1 mục đã đủ điều kiện phân tích",
       RUN + "3. Mở màn クロス分析 ở bot B\n"
             "4. Đối chiếu trạng thái của 2 mục\n"
             "5. Mở chi tiết từng mục kiểm tra điều kiện bên trong",
       "1 mục nháp + 1 mục hoàn chỉnh",
       "- Bot B có đủ 2 mục, giữ đúng trạng thái nháp / hoàn chỉnh\n"
       "- Thứ tự hiển thị giữ nguyên\n"
       "- Chi tiết điều kiện bên trong khớp bot A",
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r26-r27 (`is_draft` = 1 / 0)."),

    tc("Copy クロス分析", "DATA-REF-001", "Normal",
       "Copy bộ lọc điều kiện trước khi phân tích",
       CP + "\n- Bot A có mục phân tích gắn bộ lọc điều kiện trước (theo thẻ + thông tin bạn bè)",
       RUN + "3. Mở mục phân tích ở bot B, mở bộ lọc điều kiện trước\n"
             "4. Đối chiếu điều kiện và các mục được trỏ tới\n"
             "5. Xem số người thoả mãn bộ lọc ở bot B",
       "1 bộ lọc 2 điều kiện",
       "- Bộ lọc được nhân bản riêng cho bot B, điều kiện trỏ tới dữ liệu BOT B\n"
       "- Bước 5: số người thoả mãn tính theo bạn bè của BOT B\n"
       "- Sửa bộ lọc ở bot B không ảnh hưởng bot A",
       spec="Đã hỏi leader",
       note="MT-13 + MT-15 — [MN]Job TCs r28-r29."),

    tc("Copy クロス分析", "DATA-REF-001", "Normal",
       "Copy điều kiện phân tích — 8 loại điều kiện đơn",
       CP + "\n- Bot A có 8 mục phân tích, mỗi mục dùng 1 loại điều kiện ở cột dữ liệu test",
       RUN + "3. Mở lần lượt 8 mục phân tích ở bot B\n"
             "4. Đối chiếu loại điều kiện và giá trị được trỏ tới\n"
             "5. Xem danh sách người thoả mãn của từng mục",
       "① thẻ ② tên bạn bè ③ ngày kết bạn ④ đang chạy kịch bản ⑤ trang chuyển đổi "
       "⑥ tin xác nhận ⑦ thông tin bạn bè ⑧ trạng thái xử lý",
       "- Cả 8 điều kiện giữ đúng loại ở bot B\n"
       "- Các điều kiện có tham chiếu (thẻ, kịch bản, chuyển đổi, thông tin, trạng thái) "
       "đều trỏ tới dữ liệu của BOT B\n" + CROSS,
       spec="Đã hỏi leader",
       note="Gộp 8 loại vì CÙNG 1 kết quả. MT-15 — [MN]Job TCs r30-r37. "
            "Ô Note r34 ghi「QR không backup」— xem MT-13."),

    tc("Copy クロス分析", "FUNC-001", "Normal",
       "Copy điều kiện phân tích theo tình trạng ẩn / chặn bạn bè",
       CP + "\n- Bot A có mục phân tích dùng điều kiện ẩn / chặn bạn bè",
       RUN + "3. Mở mục phân tích ở bot B, đối chiếu điều kiện\n"
             "4. Xem danh sách người thoả mãn",
       "1 điều kiện ẩn/chặn",
       "- Điều kiện giữ đúng ở bot B\n" + CROSS,
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r38."),

    tc("Copy クロス分析", "BULK-001", "Boundary",
       "Copy mục phân tích có NHIỀU điều kiện — kiểm tra tới mốc 10 điều kiện",
       CP + "\n- Bot A có 1 mục phân tích 5 điều kiện và 1 mục 10 điều kiện",
       RUN + "3. Mở 2 mục phân tích ở bot B\n"
             "4. ĐẾM số điều kiện của từng mục\n"
             "5. Đối chiếu từng điều kiện với bot A\n"
             "6. Xem danh sách người thoả mãn",
       "1 mục 5 điều kiện · 1 mục 10 điều kiện",
       "- Bot B giữ ĐỦ số điều kiện (5 và 10) — không thiếu điều kiện nào ở cuối\n"
       "- Nội dung và thứ tự từng điều kiện khớp bot A\n" + CROSS,
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r39-r40. Mốc 10 điều kiện là điểm biên chống lỗi cắt danh sách."),

    tc("Copy クロス分析", "UI-002", "Normal",
       "Copy cài đặt cột hiển thị của mục phân tích — 3 biến thể",
       CP + "\n- Bot A có 3 mục phân tích: 1 hiển thị đủ 3 cột, 1 hiển thị 2 cột, 1 hiển thị 1 cột",
       RUN + "3. Mở lần lượt 3 mục phân tích ở bot B\n"
             "4. Đếm số cột hiển thị và đọc tên cột của từng mục",
       "① 有効 / ブロック / 被ブロック ② 有効 / ブロック ③ 被ブロック",
       "- Cả 3 mục giữ ĐÚNG số cột và ĐÚNG cột nào được chọn\n"
       "- Không mục nào bị đặt về mặc định 3 cột",
       spec="Đã hỏi leader",
       note="Gộp 3 biến thể vì cùng dạng kết quả (giữ nguyên cài đặt). "
            "MT-15 — [MN]Job TCs r41-r43 (`cross_analysis.data_column_display`)."),

    tc("Copy クロス分析", "DATA-001", "Normal",
       "Ngày tạo / ngày cập nhật của mục phân tích ở bot nhận là thời điểm copy",
       CP + "\n- Bot A có mục phân tích tạo từ ≥1 tháng trước",
       RUN + "3. Ghi lại thời điểm chạy copy\n"
             "4. Mở màn クロス分析 ở bot B, xem ngày tạo của mục phân tích\n"
             "5. Đối chiếu với bot A",
       "Mục phân tích tạo cách đây ≥1 tháng",
       "- Ngày tạo ở bot B là THỜI ĐIỂM CHẠY COPY, không phải ngày tạo gốc\n"
       "- Ngày ở bot A không đổi",
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r45 —「created_at / updated_at: Lấy theo thời điểm backup」."),

    tc("Copy クロス分析", "DATA-001", "Normal",
       "KẾT QUẢ phân tích KHÔNG được copy sang bot nhận",
       CP + "\n- Bot A có mục phân tích ĐÃ chạy xong, có bảng kết quả với số liệu cụ thể",
       RUN + "3. Ghi lại số liệu kết quả phân tích ở bot A\n"
             "4. Mở mục phân tích tương ứng ở bot B, xem bảng kết quả\n"
             "5. Đối chiếu số liệu 2 bên",
       "Bot A: kết quả phân tích đã có số liệu",
       "- Bot B KHÔNG hiển thị số liệu kết quả của bot A\n"
       "- Bảng kết quả ở bot B trống hoặc chờ chạy lại\n"
       "- KHÔNG có số liệu nào của bot A lọt sang bot B",
       spec="Đã hỏi leader",
       note="MT-15 — [MN]Job TCs r46-r47 —「số lượng filter_parent_id: Không backup / Kết quả phân tích: Không backup」."),

    tc("Copy クロス分析", "JOB-001", "Normal",
       "Mục phân tích đã copy được job chạy lại theo dữ liệu bot nhận",
       CP + "\n- Đã copy mục phân tích từ A sang B\n- Bot B có bạn bè thật thoả mãn điều kiện",
       "1. Ở bot B, mở mục phân tích đã copy\n"
       "2. Chờ job phân tích chạy (hoặc kích hoạt theo cách hệ thống quy định)\n"
       "3. Xem bảng kết quả ở bot B\n"
       "4. Đối chiếu số liệu với số bạn bè thật của bot B",
       "Bot B có ≥20 bạn bè, trong đó 8 người thoả mãn điều kiện",
       "- Job chạy và điền kết quả cho mục phân tích ở bot B\n"
       "- Số liệu khớp với dữ liệu THẬT của bot B (8 người)\n"
       "- KHÔNG dùng lại số liệu của bot A",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-14 + MT-15 — [MN]Job TCs r52 —「Các cross đã backup sẽ được job chạy đúng với data của bot đích」. "
            "⚠️ Spec không mô tả job này. PRODUCTION theo RULE-08."),

    tc("Copy クロス分析", "REG-RUN-001", "Normal",
       "Thao tác trên mục phân tích ở bot nhận sau khi copy — sao chép, xoá, sửa, sắp xếp",
       CP + "\n- Đã copy ≥3 mục phân tích từ A sang B",
       "1. Ở bot B, sao chép 1 mục phân tích\n"
       "2. Sửa điều kiện của 1 mục khác\n"
       "3. Xoá 1 mục\n"
       "4. Kéo đổi thứ tự các mục còn lại\n"
       "5. Mở lại màn クロス分析 kiểm tra kết quả",
       "3 mục phân tích",
       "- Cả 4 thao tác đều thành công, không báo lỗi\n"
       "- Bản sao chép có đủ điều kiện như bản gốc\n"
       "- Thứ tự sau khi kéo được lưu lại\n"
       "- Dữ liệu ở bot A không bị đụng",
       spec="Đã hỏi leader",
       note="Gộp 4 thao tác vì cùng 1 dạng kết quả (thao tác thành công, không lỗi). "
            "MT-15 — [MN]Job TCs r48-r51."),

    # ═══════════════ 24. Copy CSV管理 ═══════════════
    tc("Copy CSV管理", "DATA-TEXT-001", "Normal",
       "Copy tên file CSV — các kiểu tên hợp lệ đều giữ nguyên",
       CP + "\n- Bot A có 4 file CSV với 4 kiểu tên hợp lệ ở cột dữ liệu test",
       RUN + "3. Mở màn CSV管理 ở bot B\n"
             "4. Đối chiếu TỪNG KÝ TỰ của 4 tên file với bot A\n"
             "5. Tải file xuống và kiểm tra tên file tải về",
       "①「・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞」"
       "②「まことボット智恵助」③ tên có khoảng trắng đầu / giữa / cuối ④「顧客リスト2026」",
       "- Cả 4 tên ở bot B giống hệt bot A, không mất ký tự, không bị đổi mã hoá\n"
       "- Khoảng trắng giữ nguyên vị trí\n"
       "- Bước 5: tên file tải về đúng như hiển thị",
       spec="Đã hỏi leader",
       note="Gộp 4 kiểu tên vì CÙNG 1 kết quả. MT-04 — [MN]Job TCs r58-r61."),

    tc("Copy CSV管理", "UI-INPUT-001", "Abnormal",
       "Tên file CSV không hợp lệ — hệ thống báo lỗi khi tạo ở bot nhận",
       CP + "\n- Đã copy CSV sang bot B, đang ở màn CSV管理 của bot B",
       "1. Ở bot B, tạo file CSV mới\n"
       "2. Nhập lần lượt các tên ở cột dữ liệu test\n"
       "3. Mỗi lần bấm lưu và ghi lại thông báo",
       "① 0 ②「` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [] |. , / * \\ : ?」"
       "③「AIボット🤖_Ver1」④「こーだい/プレゼント専用🎁」",
       "- Cả 4 lần đều BÁO LỖI, không tạo được file\n"
       "- Thông báo lỗi hiển thị rõ ràng, không phải lỗi 500\n"
       "- Danh sách file CSV không tăng thêm dòng nào",
       spec="Đã hỏi leader",
       note="Gộp 4 input vì CÙNG 1 kết quả (báo lỗi). MT-04 — [MN]Job TCs r54-r57. "
            "⚠️ TC gốc thuộc phạm vi CSV管理 chứ không phải backup — đây là hồi quy sau copy. "
            "Cần Leader xác nhận có giữ trong tab này không."),

    tc("Copy CSV管理", "FUNC-001", "Normal",
       "Copy file CSV KHÔNG có bộ lọc",
       CP + "\n- Bot A có 1 file CSV không đặt bộ lọc đối tượng xuất",
       RUN + "3. Mở file CSV đó ở bot B, xem phần bộ lọc\n"
             "4. Xem số đối tượng hiển thị\n"
             "5. Tải file xuống và mở ra xem nội dung",
       "1 file CSV không lọc",
       "- File CSV ở bot B không có bộ lọc, giống bot A\n"
       "- Bước 4: số đối tượng tính theo BẠN BÈ CỦA BOT B\n"
       "- Bước 5: nội dung file chứa thông tin bạn bè của BOT B, không có dữ liệu bot A",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 + MT-14 — [MN]Job TCs r62. PRODUCTION theo RULE-08 (tệp xuất ra + job tính lại)."),

    tc("Copy CSV管理", "DATA-REF-001", "Normal",
       "Copy bộ lọc đối tượng xuất của file CSV — ghép kiểu VÀ",
       CP + "\n- Bot A có file CSV với bộ lọc ghép VÀ gồm các điều kiện ở cột dữ liệu test",
       RUN + "3. Mở file CSV đó ở bot B, mở bộ lọc đối tượng xuất\n"
             "4. Đối chiếu từng điều kiện và các mục được trỏ tới\n"
             "5. Xem số đối tượng ở bot B\n"
             "6. Tải file xuống và kiểm tra danh sách bạn bè trong file",
       "Điều kiện VÀ: タグ · 友だち名 · 友だち追加日 · ステップ購読状況 · コンバージョン · "
       "確認状況 · 友だち情報 · 対応ステータス · 新規・既存友だち",
       "- Các điều kiện có tham chiếu đều trỏ tới dữ liệu của BOT B\n"
       "- Số điều kiện khớp bot A, không thiếu điều kiện nào\n"
       "- Bước 6: file tải về chỉ chứa bạn bè của BOT B thoả mãn điều kiện",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r63. ⚠️ TC gốc ghi「QRコードアクション ⇒ qr k back up được」và "
            "「アフィリエイター ⇒ k back up được」— 2 điều kiện đó xử lý theo MT-13, tách sang TC riêng."),

    tc("Copy CSV管理", "DATA-REF-001", "Normal",
       "Copy bộ lọc đối tượng xuất của file CSV — ghép kiểu HOẶC",
       CP + "\n- Bot A có file CSV với bộ lọc ghép HOẶC gồm cùng bộ điều kiện như TC trên",
       RUN + "3. Mở file CSV đó ở bot B, mở bộ lọc\n"
             "4. Xác nhận kiểu ghép là HOẶC và đối chiếu từng điều kiện\n"
             "5. Xem số đối tượng và tải file xuống",
       "Cùng bộ điều kiện, ghép kiểu HOẶC",
       "- Kiểu ghép HOẶC giữ đúng ở bot B, KHÔNG bị đổi thành VÀ\n"
       "- Các điều kiện trỏ tới dữ liệu BOT B\n"
       "- Số đối tượng ở kiểu HOẶC LỚN HƠN hoặc bằng kiểu VÀ với cùng bộ điều kiện",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r64. Tách khỏi TC ghép VÀ vì kết quả số đối tượng khác nhau."),

    tc("Copy CSV管理", "DATA-REF-001", "Abnormal",
       "Bộ lọc CSV chứa điều kiện MÃ QR hoặc ĐỐI TÁC GIỚI THIỆU",
       CP + "\n- Bot A có 2 file CSV: 1 bộ lọc chứa điều kiện mã QR, 1 chứa điều kiện đối tác giới thiệu",
       RUN + "3. Mở bộ lọc của 2 file CSV ở bot B\n"
             "4. Ghi rõ điều kiện đó còn hay bị bỏ, và bộ lọc còn mấy điều kiện\n"
             "5. Tải file xuống và so số dòng với bot A",
       "1 file lọc QR · 1 file lọc đối tác giới thiệu",
       "- Kết quả theo quyết định MT-13\n"
       "- ⚠️ Nếu điều kiện bị bỏ mà bộ lọc vẫn chạy thì file xuất ra ở bot B "
       "chứa NHIỀU bạn bè hơn dự kiến — rủi ro lộ danh sách sai phạm vi, phải raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-13 + MT-04 — [MN]Job TCs r63-r64 ghi「qr k back up được」/「アフィリエイター k back up được」 "
            "nhưng ô kết quả chung vẫn ghi「back up thành công」."),

    tc("Copy CSV管理", "FUNC-001", "Normal",
       "Copy cài đặt lọc theo bạn bè bị chặn và bạn bè chặn bot",
       CP + "\n- Bot A có 1 file CSV bật điều kiện「bạn bè đã bị chặn」"
            "và 1 file bật「bạn bè đã chặn bot」",
       RUN + "3. Mở 2 file CSV ở bot B, đối chiếu cài đặt\n"
             "4. Tải file xuống và kiểm tra danh sách trong file",
       "2 file, mỗi file 1 điều kiện",
       "- Cả 2 cài đặt giữ đúng ở bot B, không bị đảo\n"
       "- Bước 4: file tải về chứa đúng nhóm bạn bè tương ứng của BOT B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 2 điều kiện vì cùng 1 kết quả. MT-04 — [MN]Job TCs r65-r66."),

    tc("Copy CSV管理", "OUT-EXPORT-001", "Normal",
       "Copy cài đặt cột xuất kiểu chọn đơn — 7 mục",
       CP + "\n- Bot A có file CSV bật đủ 7 cột xuất kiểu chọn đơn ở cột dữ liệu test",
       RUN + "3. Mở file CSV đó ở bot B, xem danh sách cột đã chọn\n"
             "4. Đối chiếu đủ 7 mục với bot A\n"
             "5. Tải file xuống và kiểm tra tiêu đề cột trong file",
       "① ステータスメッセージ ② 個別メモ ③ 友だち追加日 ④ 対応マーク "
       "⑤ 最終メッセージ受信日時 ⑥ 配信中ステップ ⑦ 流入経路",
       "- Bot B bật đúng 7 cột như bot A, không thiếu không thừa\n"
       "- Bước 5: file tải về có đủ 7 cột, dữ liệu là của bạn bè BOT B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 7 mục vì CÙNG 1 kết quả. MT-04 — [MN]Job TCs r67-r73."),

    tc("Copy CSV管理", "DATA-REF-001", "Normal",
       "Copy cài đặt cột xuất theo THẺ",
       CP + "\n- Bot A có 3 file CSV: 1 không chọn thẻ nào, 1 chọn thẻ ở folder mặc định, "
            "1 chọn thẻ ở folder tự tạo",
       RUN + "3. Mở 3 file CSV ở bot B, xem danh sách thẻ đã chọn\n"
             "4. Kiểm tra thẻ được trỏ tới là của bot nào\n"
             "5. Tải file xuống và kiểm tra cột thẻ trong file",
       "3 file: không chọn · thẻ folder mặc định · thẻ folder tự tạo",
       "- File không chọn thẻ: giữ nguyên trạng thái không chọn\n"
       "- 2 file còn lại: thẻ được chọn là thẻ của BOT B\n"
       "- Bước 5: file tải về có cột thẻ với dữ liệu của bạn bè bot B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 3 trường hợp vì cùng 1 kết quả (ánh xạ đúng thẻ bot đích). "
            "MT-04 — [MN]Job TCs r74-r76 (`export_tags`)."),

    tc("Copy CSV管理", "DATA-REF-001", "Normal",
       "Copy cài đặt cột xuất theo THÔNG TIN BẠN BÈ mặc định và địa chỉ",
       CP + "\n- Bot A có file CSV chọn 4 thông tin mặc định và 5 mục địa chỉ",
       RUN + "3. Mở file CSV đó ở bot B, xem danh sách thông tin đã chọn\n"
             "4. Đối chiếu đủ 9 mục\n"
             "5. Tải file xuống và kiểm tra 9 cột tương ứng",
       "4 mục mặc định (tên hệ thống · email · số điện thoại · ngày sinh) "
       "+ 5 mục địa chỉ (郵便番号 / 都道府県名 / 市区町村名 / 町名番地 / 建物名・部屋番号)",
       "- Bot B chọn đúng 9 mục như bot A\n"
       "- Bước 5: file tải về có đủ 9 cột, dữ liệu của bạn bè BOT B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 9 mục vì CÙNG 1 kết quả. MT-04 — [MN]Job TCs r78-r87."),

    tc("Copy CSV管理", "DATA-REF-001", "Normal",
       "Copy cài đặt cột xuất theo THÔNG TIN BẠN BÈ tự tạo — đủ 6 kiểu",
       CP + "\n- Bot A có file CSV chọn 6 thông tin bạn bè tự tạo, đủ 6 kiểu",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận 6 mục đã copy\n"
             "4. Mở file CSV ở bot B, xem 6 thông tin đã chọn và kiểm tra trỏ tới mục nào\n"
             "5. Tải file xuống và kiểm tra 6 cột",
       "6 kiểu: mô tả · lựa chọn · ngày tháng · điểm · ảnh · PDF",
       "- Cả 6 mục được chọn ở bot B đều trỏ tới thông tin của BOT B\n"
       "- KHÔNG trỏ tới thông tin của bot A\n"
       "- Bước 5: file tải về có đủ 6 cột với dữ liệu của bạn bè bot B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 6 kiểu vì CÙNG 1 kết quả. MT-04 — [MN]Job TCs r88-r93 (`export_friend_info_value`). "
            "TC gốc r77 còn có case「không chọn friend info nào」— gộp vào TC thẻ ở trên."),

    tc("Copy CSV管理", "LIST-001", "Normal",
       "Thứ tự hiển thị file CSV ở bot nhận giống bot gửi",
       CP + "\n- Bot A có 5 file CSV, đã sắp xếp theo thứ tự riêng",
       RUN + "3. Mở màn CSV管理 ở bot B\n4. Ghi lại thứ tự 5 file\n5. Đối chiếu với bot A",
       "5 file CSV đã sắp xếp",
       "- Thứ tự 5 file ở bot B GIỐNG HỆT bot A\n"
       "- Không bị sắp lại theo thời gian tạo",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r94 —「Vị trí hiển thị của các file CSV sẽ giống với bot nguồn」."),

    tc("Copy CSV管理", "OUT-EXPORT-001", "Normal",
       "Tải file CSV từ màn quản lý ở bot nhận",
       CP + "\n- Đã copy file CSV từ A sang B\n- Bot B có ≥10 bạn bè thoả mãn điều kiện lọc",
       "1. Ở bot B, mở màn CSV管理\n"
       "2. Bấm tải file CSV\n"
       "3. Mở file vừa tải bằng phần mềm bảng tính\n"
       "4. Kiểm tra số dòng và nội dung",
       "≥10 bạn bè thoả mãn",
       "- Tải xuống thành công, không báo lỗi\n"
       "- File mở được, không lỗi mã hoá tiếng Nhật\n"
       "- Nội dung là thông tin bạn bè của BOT B\n"
       "- KHÔNG có dòng nào là bạn bè của bot A",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r95. PRODUCTION theo RULE-08 (tệp xuất ra)."),

    tc("Copy CSV管理", "REG-URL-001", "Normal",
       "Tải file CSV bằng đường dẫn ở bot nhận",
       CP + "\n- Đã copy file CSV từ A sang B",
       "1. Ở bot B, lấy đường dẫn tải file CSV\n"
       "2. So sánh đường dẫn với bot A\n"
       "3. Mở đường dẫn của bot B trên trình duyệt\n"
       "4. Mở file tải về và kiểm tra nội dung",
       "1 file CSV",
       "- Đường dẫn ở bot B KHÁC bot A và chứa định danh của BOT B\n"
       "- Bước 3: tải được file\n"
       "- Bước 4: nội dung là bạn bè của BOT B",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r96 —「check csv_management trường file_name_new down load hiển thị "
            "bot id của bot B」."),

    tc("Copy CSV管理", "SEC-ISO-001", "Normal",
       "Copy CSV giữa 2 LOA thuộc 2 TÀI KHOẢN khác nhau",
       "- Bot A thuộc tài khoản người dùng U1\n"
       "- Bot B thuộc tài khoản người dùng U2 (khác U1)\n"
       "- Job nền đang bật; đã dựng file CSV có bộ lọc ở bot A",
       RUN + "3. Đăng nhập tài khoản U2, mở màn CSV管理 của bot B\n"
             "4. Xác nhận file CSV đã sang\n"
             "5. Tải file xuống và kiểm tra nội dung",
       "2 tài khoản người dùng khác nhau",
       "- Copy thành công giữa 2 tài khoản khác nhau\n"
       "- Bước 5: file tải về chứa thông tin bạn bè của BOT B\n"
       "- KHÔNG có thông tin bạn bè của bot A trong file",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r97. Đây là TC quan trọng về rò rỉ dữ liệu cá nhân giữa 2 khách hàng."),

    tc("Copy CSV管理", "REG-RUN-001", "Normal",
       "Thao tác trên file CSV ở bot nhận sau khi copy — nhập lại, sao chép, xoá, sửa, sắp xếp",
       CP + "\n- Đã copy ≥3 file CSV từ A sang B",
       "1. Ở bot B, tải 1 file CSV xuống rồi nhập ngược trở lại hệ thống\n"
       "2. Sao chép 1 file CSV\n"
       "3. Sửa cài đặt của 1 file CSV\n"
       "4. Xoá 1 file CSV\n"
       "5. Kéo đổi thứ tự các file còn lại",
       "3 file CSV",
       "- Cả 5 thao tác đều thành công, không báo lỗi\n"
       "- Bước 1: dữ liệu nhập vào gắn với bạn bè của BOT B\n"
       "- Bản sao chép có đủ cài đặt như bản gốc\n"
       "- Thứ tự sau khi kéo được lưu lại\n"
       "- Dữ liệu ở bot A không bị đụng",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Gộp 5 thao tác vì cùng dạng kết quả. MT-04 — [MN]Job TCs r98-r102."),

    tc("Copy CSV管理", "DATA-001", "Normal",
       "Ngày tạo file và ngày cập nhật điều kiện ở bot nhận là thời điểm copy",
       CP + "\n- Bot A có file CSV tạo từ ≥1 tháng trước, đã sửa điều kiện cách đây 2 tuần",
       RUN + "3. Ghi lại thời điểm chạy copy\n"
             "4. Mở màn CSV管理 ở bot B, xem cột ngày tạo và ngày cập nhật điều kiện\n"
             "5. Đối chiếu với bot A",
       "File tạo ≥1 tháng trước, sửa cách đây 2 tuần",
       "- Cả 2 mốc thời gian ở bot B đều là THỜI ĐIỂM CHẠY COPY\n"
       "- Không lấy theo ngày gốc ở bot A\n"
       "- Ngày ở bot A không đổi",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r103, r107 —「Lấy là thời điểm backup」."),

    tc("Copy CSV管理", "DATA-COUNT-001", "Normal",
       "Số đối tượng của file CSV được tự động tính lại theo bot nhận",
       CP + "\n- Bot A có 3 file CSV: 1 có bộ lọc cho 0 người, 1 có bộ lọc cho nhiều người, "
            "1 không đặt bộ lọc\n"
            "- Bot A và bot B có số bạn bè khác nhau rõ rệt",
       RUN + "3. Ngay sau khi copy xong, mở màn CSV管理 ở bot B — KHÔNG bấm tải lại, KHÔNG sửa file\n"
             "4. Đọc cột số đối tượng của cả 3 file\n"
             "5. Đối chiếu với số bạn bè thật của bot B thoả mãn từng điều kiện",
       "Bot A: 120 bạn · Bot B: 37 bạn (trong đó 12 người thoả mãn bộ lọc thứ 2)",
       "- Bước 4: số đối tượng đã được điền SẴN, không phải 0 hay số của bot A\n"
       "- File không lọc: số đối tượng = số bạn bè đang hoạt động của BOT B\n"
       "- File lọc cho 0 người ở bot A: tính lại theo bot B (có thể khác 0)\n"
       "- KHÔNG cần bấm tải lại hay sửa file mới thấy số đúng\n"
       "- ⚠️ Nếu số vẫn là của bot A hoặc bằng 0 thì raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-14 + MT-04 — [MN]Job TCs r104-r106 —「sau khi back up 100% JOB SẼ PHẢI TỰ ĐỘNG CHẠY ... "
            "mà k cần nhấn vào reload file hoặc edit file mới tính toán」. "
            "⚠️ Spec KHÔNG có job nào làm việc này — vùng mù."),

    tc("Copy CSV管理", "DATA-001", "Normal",
       "Lịch sử nhập dữ liệu KHÔNG được copy sang bot nhận",
       CP + "\n- Bot A có file CSV đã có 5 lần nhập dữ liệu trong lịch sử",
       RUN + "3. Mở file CSV đó ở bot B, mở tab lịch sử nhập\n"
             "4. Đếm số bản ghi lịch sử\n"
             "5. Kiểm tra lại ở bot A",
       "Bot A: 5 lần nhập dữ liệu",
       "- Tab lịch sử nhập ở bot B TRỐNG — 0 bản ghi\n"
       "- KHÔNG có thông tin lần nhập nào của bot A lọt sang\n"
       "- Bot A vẫn giữ đủ 5 bản ghi lịch sử",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r108 —「Không backup lịch sử import. Vào tab import ⇒ Phần lịch sử trống」."),

    tc("Copy CSV管理", "REG-SHARED-001", "Normal",
       "Kiểm tra ngẫu nhiên vài tính năng khác vẫn copy đủ khi copy CSV và phân tích chéo",
       CP + "\n- Bot A có ≥10 thẻ, ≥10 mẫu tin, ≥3 kịch bản, đồng thời có file CSV và mục phân tích chéo",
       RUN + "3. Mở màn タグ ở bot B, đếm số thẻ\n"
             "4. Mở màn テンプレート ở bot B, đếm số mẫu tin\n"
             "5. Mở màn ステップ配信 ở bot B, đếm số kịch bản\n"
             "6. Đối chiếu cả 3 với bot A",
       "10 thẻ + 10 mẫu tin + 3 kịch bản",
       "- Bot B có đủ số lượng cả 3 loại\n"
       "- Việc copy CSV và phân tích chéo KHÔNG làm thiếu dữ liệu của các tính năng khác",
       spec="Đã hỏi leader",
       note="MT-04 — [MN]Job TCs r109-r112 —「Check cover 1 vài tính năng khác chạy được bình thường: "
            "Tag / Template / Scenario — Backup bình thường」."),
]
