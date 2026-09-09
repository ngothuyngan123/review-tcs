# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 11-15: kiểm tra dữ liệu được copy sang LOA nhận
cho 自動応答 / リッチメニュー / ステップ配信 / テンプレート / フォーム作成.

Quy ước: **bot A = LOA gửi dữ liệu**, **bot B = LOA nhận dữ liệu** (theo spec; xem MT-01).
Mọi TC trong file này đều theo cùng một khuôn:
  dựng dữ liệu ở bot A → chạy copy A→B → mở màn tương ứng ở bot B đối chiếu.
"""
from _common import tc

CP = ("- Bot A (LOA gửi) và bot B (LOA nhận) đều plan Standard/Pro, job nền đang bật\n"
      "- Bot B là LOA TRỐNG (chưa có dữ liệu cùng loại) để dễ đối chiếu\n"
      "- Đã dựng xong dữ liệu ở bot A theo mục điều kiện riêng bên dưới")
RUN = "1. Ở bot A, xác nhận dữ liệu đã dựng đúng\n2. Thực hiện copy A → B và chờ trạng thái hoàn tất\n"
MT16 = ("MT-16 — Backup 1.0 ghi lỗi「t_action_detail đang lấy id remind của bot gốc」, "
        "bản Backup (job) mới hơn KHÔNG còn ghi chú. Chưa rõ đã fix hay chưa. ")

S3 = [
    # ═══════════════ 11. Copy 自動応答 ═══════════════
    tc("Copy 自動応答", "FUNC-001", "Normal",
       "Copy folder tự động trả lời — đủ số lượng và đúng thứ tự",
       CP + "\n- Bot A có 3 folder tự động trả lời (ngoài folder mặc định), mỗi folder chứa 2 auto reply\n"
            "- Bot A có 1 folder đã xoá",
       RUN + "3. Mở màn 自動応答 ở bot B\n4. Đếm số folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số auto reply bên trong",
       "3 folder: 「FD-01」「FD-02」「FD-03」, mỗi folder 2 auto reply; 1 folder đã xoá tên「FD-DEL」",
       "- Bot B có đủ 3 folder, đúng tên, đúng thứ tự như bot A\n"
       "- Mỗi folder chứa đúng 2 auto reply\n"
       "- Folder đã xoá「FD-DEL」KHÔNG xuất hiện ở bot B",
       note="Nguồn: Backup 1.0 r3 · Backup (job) r2."),

    tc("Copy 自動応答", "FUNC-001", "Normal",
       "Copy kiểu phản hồi theo từ khoá và kiểu phản hồi tất cả",
       CP + "\n- Bot A có 1 auto reply đặt theo từ khoá (3 từ khoá) và 1 auto reply kiểu phản hồi tất cả",
       RUN + "3. Mở màn 自動応答 ở bot B, vào chi tiết từng auto reply\n"
             "4. Đối chiếu kiểu phản hồi và danh sách từ khoá với bot A",
       "Từ khoá:「予約」「キャンセル」「営業時間」· 1 auto reply kiểu phản hồi tất cả",
       "- Auto reply kiểu từ khoá ở bot B giữ đúng kiểu và đủ 3 từ khoá, không thiếu không thừa\n"
       "- Auto reply kiểu phản hồi tất cả giữ đúng kiểu\n"
       "- Thứ tự từ khoá giữ nguyên",
       note="Gộp 2 kiểu vì cùng 1 kết quả (giữ nguyên setting). Nguồn: Backup 1.0 r4-r5 · Backup (job) r3-r4."),

    tc("Copy 自動応答", "FUNC-DATE-001", "Normal",
       "Copy auto reply đặt「luôn phản hồi」— không có giới hạn ngày giờ",
       CP + "\n- Bot A có 1 auto reply đặt luôn phản hồi (không giới hạn ngày/giờ)",
       RUN + "3. Mở chi tiết auto reply đó ở bot B\n4. Kiểm tra phần cài đặt thời gian phản hồi",
       "1 auto reply「常に反応」",
       "- Ở bot B, auto reply vẫn ở chế độ luôn phản hồi\n"
       "- Không tự sinh ra khung giờ hay ngày trong tuần nào\n"
       "- Gửi tin từ máy LINE thật vào bất kỳ giờ nào đều nhận được phản hồi",
       note="Nguồn: Backup 1.0 r6 · Backup (job) r5. RULE-06: verify tới đầu ra là tin nhận được trên LINE."),

    tc("Copy 自動応答", "FUNC-DATE-001", "Normal",
       "Copy auto reply có đặt khung giờ và thứ trong tuần",
       CP + "\n- Bot A có 1 auto reply đặt: thứ 2-6, từ 09:00 đến 18:00",
       RUN + "3. Mở chi tiết auto reply đó ở bot B\n"
             "4. Đối chiếu khung giờ và các thứ đã chọn\n"
             "5. Gửi tin từ máy LINE thật vào trong khung giờ và ngoài khung giờ",
       "Thứ 2,3,4,5,6 · 09:00–18:00",
       "- Bot B giữ đúng thứ 2-6 và khung 09:00–18:00\n"
       "- Gửi tin trong khung giờ: nhận được phản hồi\n"
       "- Gửi tin ngoài khung giờ: KHÔNG nhận phản hồi",
       note="Nguồn: Backup 1.0 r7 · Backup (job) r6. Cần máy LINE thật để verify đầu ra (RULE-06)."),

    tc("Copy 自動応答", "FRIEND-001", "Normal",
       "Copy cài đặt phản hồi riêng cho bạn bè đang hoạt động và bạn bè đã chặn",
       CP + "\n- Bot A có 1 auto reply bật phản hồi cho bạn bè đang hoạt động\n"
            "- Bot A có 1 auto reply bật phản hồi cho bạn bè đã chặn bot",
       RUN + "3. Mở chi tiết cả 2 auto reply ở bot B\n4. Đối chiếu 2 cài đặt đó với bot A",
       "2 auto reply, mỗi cái bật 1 trong 2 tuỳ chọn",
       "- Bot B giữ đúng cài đặt của cả 2 auto reply\n"
       "- Không bị bật/tắt nhầm sang tuỳ chọn còn lại",
       note="Gộp 2 tuỳ chọn vì cùng 1 kết quả. Nguồn: Backup 1.0 r8-r9 · Backup (job) r7-r8."),

    tc("Copy 自動応答", "FUNC-MULTI-001", "Normal",
       "Copy cài đặt phản hồi 1 lần / nhiều lần",
       CP + "\n- Bot A có 1 auto reply đặt phản hồi 1 lần và 1 auto reply đặt phản hồi nhiều lần",
       RUN + "3. Mở chi tiết cả 2 auto reply ở bot B\n"
             "4. Gửi cùng 1 từ khoá 2 lần liên tiếp từ máy LINE thật cho từng auto reply",
       "2 auto reply, mỗi cái 1 kiểu",
       "- Cài đặt giữ đúng ở bot B\n"
       "- Auto reply 1 lần: chỉ nhận phản hồi ở lần gửi đầu\n"
       "- Auto reply nhiều lần: nhận phản hồi ở cả 2 lần gửi",
       note="Nguồn: Backup 1.0 r10 · Backup (job) r9. RULE-06 verify tới tin trên LINE."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động gửi tin văn bản trong auto reply",
       CP + "\n- Bot A có 1 auto reply với hành động gửi tin văn bản có nội dung nhận biết được",
       RUN + "3. Mở chi tiết auto reply ở bot B\n"
             "4. Đối chiếu nội dung tin văn bản\n"
             "5. Kích hoạt auto reply từ máy LINE thật",
       "Nội dung:「ご連絡ありがとうございます。担当者より折り返します。」",
       "- Nội dung tin văn bản ở bot B giống hệt bot A\n"
       "- Kích hoạt từ LINE nhận được đúng tin đó",
       note="Nguồn: Backup 1.0 r11 · Backup (job) r10."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động bắt đầu kịch bản — trỏ đúng kịch bản MỚI của bot nhận",
       CP + "\n- Bot A có kịch bản「シナリオ-A1」và 1 auto reply có hành động bắt đầu kịch bản đó",
       RUN + "3. Mở màn ステップ配信 ở bot B, ghi lại kịch bản đã được copy sang\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động bắt đầu kịch bản trỏ tới đâu\n"
             "5. Kích hoạt auto reply từ máy LINE thật và kiểm tra bạn bè đó có vào kịch bản không",
       "1 kịch bản「シナリオ-A1」có 2 bước",
       "- Hành động trỏ tới kịch bản「シナリオ-A1」ĐÃ ĐƯỢC COPY SANG BOT B\n"
       "- KHÔNG trỏ tới kịch bản của bot A\n"
       "- Bước 5: bạn bè của bot B được đưa vào đúng kịch bản của bot B và nhận bước đầu tiên",
       note="Nguồn: Backup 1.0 r12 · Backup (job) r11 —「Phải lấy được id của scen tương ứng đã tạo ở màn scenario」."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động gắn thẻ — trỏ đúng thẻ MỚI của bot nhận",
       CP + "\n- Bot A có thẻ「タグ-A1」và 1 auto reply có hành động gắn thẻ đó",
       RUN + "3. Mở màn タグ ở bot B, xác nhận thẻ「タグ-A1」đã được copy\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động gắn thẻ trỏ tới thẻ nào\n"
             "5. Kích hoạt auto reply từ máy LINE thật rồi mở màn 友だちリスト ở bot B",
       "1 thẻ「タグ-A1」",
       "- Hành động trỏ tới thẻ「タグ-A1」của BOT B\n"
       "- Bước 5: bạn bè vừa kích hoạt được gắn thẻ「タグ-A1」ở bot B\n"
       "- Số người gắn thẻ ở bot A KHÔNG thay đổi",
       note="Nguồn: Backup 1.0 r13 · Backup (job) r12."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động gửi mẫu tin — trỏ đúng mẫu tin MỚI của bot nhận",
       CP + "\n- Bot A có mẫu tin「テンプレ-A1」và 1 auto reply có hành động gửi mẫu tin đó",
       RUN + "3. Mở màn テンプレート ở bot B, xác nhận mẫu tin đã được copy\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động gửi mẫu tin trỏ tới đâu\n"
             "5. Kích hoạt auto reply từ máy LINE thật",
       "1 mẫu tin「テンプレ-A1」kiểu văn bản",
       "- Hành động trỏ tới mẫu tin của BOT B, không phải bot A\n"
       "- Bước 5: nhận được đúng nội dung mẫu tin trên LINE",
       note="Nguồn: Backup 1.0 r14 · Backup (job) r13."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động đổi richmenu — trỏ đúng richmenu MỚI của bot nhận",
       CP + "\n- Bot A có richmenu「RM-A1」và 1 auto reply có hành động đổi sang richmenu đó",
       RUN + "3. Mở màn リッチメニュー ở bot B, xác nhận richmenu đã được copy\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động đổi richmenu trỏ tới đâu\n"
             "5. Kích hoạt auto reply từ máy LINE thật và quan sát richmenu hiển thị dưới màn chat",
       "1 richmenu「RM-A1」đã tạo trên LINE",
       "- Hành động trỏ tới richmenu「RM-A1」của BOT B\n"
       "- Bước 5: richmenu dưới màn chat của bạn bè đổi sang đúng RM-A1 của bot B",
       note="Nguồn: Backup 1.0 r15 · Backup (job) r14. RULE-06 — verify tới richmenu hiển thị trên LINE."),

    tc("Copy 自動応答", "DATA-REF-001", "Abnormal",
       "Copy hành động nhắc lịch — kiểm tra có còn trỏ id của bot gửi không",
       CP + "\n- Bot A có nhắc lịch「リマインド-A1」và 1 auto reply có hành động bắt đầu nhắc lịch đó",
       RUN + "3. Mở màn リマインド配信 ở bot B, ghi lại nhắc lịch đã được copy\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động nhắc lịch trỏ tới đâu\n"
             "5. Kích hoạt auto reply từ máy LINE thật và chờ tới giờ nhắc",
       "1 nhắc lịch「リマインド-A1」có 1 bước gửi ngay",
       "- Hành động phải trỏ tới nhắc lịch của BOT B\n"
       "- Bước 5: bạn bè của bot B nhận được tin nhắc từ bot B\n"
       "- ⚠️ Nếu popup cài đặt hành động ở bot B để trống hoặc tin nhắc gửi từ bot A thì đây là lỗi — raise bug",
       spec="Đã hỏi leader",
       note=MT16 + "Nguồn: Backup 1.0 r16 (ghi rõ「c check lại thấy vẫn lỗi」) · Backup (job) r15. "
            "⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy hành động ghi thông tin bạn bè trong auto reply",
       CP + "\n- Bot A có thông tin bạn bè「info-text-A1」(kiểu mô tả) và「info-point-A1」(kiểu điểm)\n"
            "- Bot A có 1 auto reply có hành động ghi giá trị vào 2 thông tin đó",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận 2 thông tin đã được copy\n"
             "4. Mở chi tiết auto reply ở bot B, xem hành động trỏ tới thông tin nào\n"
             "5. Kích hoạt auto reply từ máy LINE thật rồi mở chi tiết bạn bè ở bot B",
       "2 thông tin bạn bè: 1 kiểu mô tả, 1 kiểu điểm",
       "- Hành động trỏ tới thông tin bạn bè của BOT B\n"
       "- Bước 5: giá trị được ghi vào đúng bạn bè của bot B\n"
       "- Dữ liệu bạn bè ở bot A không bị đụng",
       note="Nguồn: Backup 1.0 r18 · Backup (job) r17."),

    tc("Copy 自動応答", "DATA-REF-001", "Normal",
       "Copy các hành động không cần ánh xạ: đánh dấu, trạng thái xử lý, chặn/ẩn bạn bè",
       CP + "\n- Bot A có 3 auto reply, lần lượt có hành động: đánh dấu (bookmark), "
            "đổi trạng thái xử lý, và chặn/ẩn bạn bè",
       RUN + "3. Mở chi tiết cả 3 auto reply ở bot B\n"
             "4. Đối chiếu từng hành động với bot A\n"
             "5. Kích hoạt lần lượt cả 3 từ máy LINE thật và kiểm tra ở màn 友だちリスト bot B",
       "3 auto reply × 3 loại hành động",
       "- Cả 3 hành động đều được copy đủ, không mất hành động nào\n"
       "- Hành động đổi trạng thái xử lý trỏ tới trạng thái ĐÃ ĐƯỢC COPY sang bot B\n"
       "- Bước 5: thao tác thực tế trên bạn bè của bot B chạy đúng",
       note="Gộp 3 loại vì cùng kết quả (copy nguyên setting). "
            "⚠️ Backup 1.0 r17/r19/r20 ghi「chưa tạo được action này」— tức 3 hành động này CHƯA TỪNG được đo. "
            "Nguồn: Backup (job) r16/r18/r19."),

    tc("Copy 自動応答", "FUNC-001", "Normal",
       "Copy trạng thái bật / tắt của auto reply",
       CP + "\n- Bot A có 1 auto reply đang BẬT và 1 auto reply đang TẮT",
       RUN + "3. Mở màn 自動応答 ở bot B\n"
             "4. Đọc trạng thái bật/tắt của 2 auto reply tương ứng\n"
             "5. Gửi từ khoá của auto reply đang tắt từ máy LINE thật",
       "1 auto reply bật + 1 auto reply tắt",
       "- Bot B giữ đúng: cái bật vẫn bật, cái tắt vẫn tắt\n"
       "- Bước 5: auto reply đang tắt KHÔNG phản hồi",
       note="Nguồn: Backup 1.0 r22-r23 · Backup (job) r21-r22."),

    tc("Copy 自動応答", "DATA-REF-001", "Abnormal",
       "Copy auto reply có gắn bộ lọc đối tượng",
       CP + "\n- Bot A có 1 auto reply gắn bộ lọc theo thẻ (chỉ phản hồi bạn bè có thẻ「タグ-A1」)",
       RUN + "3. Mở chi tiết auto reply ở bot B, xem phần bộ lọc\n"
             "4. Nếu có bộ lọc: kiểm tra điều kiện lọc trỏ tới thẻ nào\n"
             "5. Sửa bộ lọc ở bot B rồi kiểm tra bộ lọc ở bot A có bị đổi không",
       "1 bộ lọc theo thẻ",
       "- Ghi rõ hiện trạng: bộ lọc CÓ được copy hay KHÔNG\n"
       "- Nếu có: điều kiện lọc trỏ tới thẻ của BOT B\n"
       "- Bước 5: sửa ở bot B KHÔNG làm đổi bộ lọc ở bot A",
       spec="Đã hỏi leader",
       note="⚠️ Backup 1.0 r21 ghi「Chưa support」; Backup (job) r20 để TRỐNG ô kết quả. "
            "Nhưng Backup (job) r80 (khối richmenu) lại nói bộ lọc CÓ được copy và phải tạo bộ lọc mới. "
            "Xem thêm MT-13. Cần Leader chốt."),

    # ═══════════════ 12. Copy リッチメニュー ═══════════════
    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Copy folder richmenu — đủ số lượng, đúng thứ tự, không gồm richmenu đã xoá",
       CP + "\n- Bot A có 3 folder richmenu (ngoài mặc định): FD-1 chứa 2 richmenu, FD-2 chứa 1, FD-3 rỗng\n"
            "- Trong FD-1 có thêm 1 richmenu đã xoá",
       RUN + "3. Mở màn リッチメニュー ở bot B\n"
             "4. Đếm folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số richmenu",
       "3 folder + 1 richmenu đã xoá tên「RM-DEL」",
       "- Bot B có đủ 3 folder, đúng tên, đúng thứ tự\n"
       "- FD-1 có 2 richmenu, FD-2 có 1, FD-3 rỗng\n"
       "- Richmenu「RM-DEL」KHÔNG xuất hiện ở bot B\n"
       "- Màn「削除済み」của bot B cũng KHÔNG có RM-DEL",
       note="Nguồn: Backup (job) r54 (khối Improve 10/2025) · r118. Backup 1.0 r24 (bản cũ)."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Copy tên và vị trí hiển thị của richmenu",
       CP + "\n- Bot A có 3 richmenu tên「RM-01」「RM-02」「RM-03」ở 3 vị trí khác nhau trong danh sách",
       RUN + "3. Mở màn リッチメニュー ở bot B\n"
             "4. Đối chiếu tên và thứ tự 3 richmenu với bot A",
       "3 richmenu, thứ tự 1-2-3",
       "- Bot B có đủ 3 richmenu đúng tên\n"
       "- Thứ tự trong danh sách giống hệt bot A",
       note="Nguồn: Backup (job) r55, r57."),

    tc("Copy リッチメニュー", "MEDIA-IMG-001", "Normal",
       "Copy ảnh richmenu — tạo ảnh MỚI cùng kích thước, xem được ở cả 2 bot",
       CP + "\n- Bot A có richmenu cỡ 2500×1686 và richmenu cỡ 2500×843, đều đã gắn ảnh",
       RUN + "3. Mở chi tiết từng richmenu ở bot B, xem ảnh có hiển thị không\n"
             "4. Mở ảnh ở tab mới, ghi lại đường dẫn ảnh của bot B và bot A\n"
             "5. Kiểm tra kích thước ảnh 2 bên\n"
             "6. Mở lại richmenu ở bot A xem ảnh còn hiển thị không",
       "2 richmenu: 2500×1686 và 2500×843",
       "- Ảnh hiển thị bình thường ở bot B\n"
       "- Đường dẫn ảnh của bot B KHÁC đường dẫn của bot A (ảnh mới, không dùng chung)\n"
       "- Kích thước ảnh (rộng × cao × dung lượng) giống hệt bot A\n"
       "- Bước 6: ảnh ở bot A vẫn hiển thị bình thường, không bị mất",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r56. PRODUCTION theo RULE-08 (media). Xem thêm MT-23 về quy tắc đường dẫn."),

    tc("Copy リッチメニュー", "INTG-LINE-001", "Normal",
       "Copy richmenu CHƯA từng đăng ký lên LINE",
       CP + "\n- Bot A có 1 richmenu chưa hoàn tất 4 bước (chưa đăng ký lên LINE)",
       RUN + "3. Mở màn リッチメニュー ở bot B, tìm richmenu đó\n"
             "4. Mở chi tiết và xem đang dừng ở bước nào\n"
             "5. Hoàn tất các bước còn lại ở bot B và bật hiển thị",
       "1 richmenu dở dang",
       "- Richmenu xuất hiện ở bot B, ở đúng bước dở dang như bot A\n"
       "- Bước 5: hoàn tất và bật hiển thị được bình thường, richmenu hiện trên LINE",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r58 —「queue_richmenu_id = NULL」."),

    tc("Copy リッチメニュー", "INTG-LINE-001", "Abnormal",
       "Copy richmenu ĐÃ đăng ký lên LINE — richmenu bên bot nhận có dùng được không",
       CP + "\n- Bot A có 1 richmenu đã hoàn tất 4 bước và đang hiển thị trên LINE",
       RUN + "3. Mở màn リッチメニュー ở bot B, tìm richmenu đó\n"
             "4. Bật hiển thị richmenu ở bot B\n"
             "5. Mở LINE bằng tài khoản là bạn bè của bot B, xem richmenu\n"
             "6. Ở bot B, thử tắt hiển thị richmenu rồi bật lại",
       "1 richmenu đã đăng ký LINE ở bot A",
       "- Richmenu xuất hiện ở bot B\n"
       "- Bước 5: bạn bè của bot B nhìn thấy đúng richmenu đó\n"
       "- Bước 6: tắt/bật hiển thị ở bot B đều có tác dụng thật trên LINE\n"
       "- Richmenu ở bot A KHÔNG bị ảnh hưởng",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-10 — Backup (job) r59 TỰ MÂU THUẪN trong cùng 1 ô (vừa nói fill id vừa nói để NULL). "
            "TC này để đo hậu quả người dùng nhìn thấy. ⚠️ Nếu bước 6 không có tác dụng thì raise bug."),

    tc("Copy リッチメニュー", "STATE-001", "Normal",
       "Copy trạng thái hoàn tất các bước tạo richmenu",
       CP + "\n- Bot A có 4 richmenu dừng ở 4 bước khác nhau (bước 1, 2, 3, 4)",
       RUN + "3. Mở lần lượt 4 richmenu ở bot B\n"
             "4. Ghi lại mỗi cái đang ở bước nào",
       "4 richmenu dừng ở bước 1 / 2 / 3 / 4",
       "- Mỗi richmenu ở bot B mở ra đúng bước như ở bot A\n"
       "- Không có cái nào bị reset về bước 1",
       note="Nguồn: Backup (job) r60 —「step_active IN (1,2,3,4)」."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Copy cài đặt hiển thị ban đầu ở màn chat (表示する / 表示しない)",
       CP + "\n- Bot A có 1 richmenu đặt「表示する」và 1 richmenu đặt「表示しない」",
       RUN + "3. Mở chi tiết cả 2 richmenu ở bot B\n"
             "4. Đối chiếu cài đặt hiển thị ban đầu",
       "2 richmenu, mỗi cái 1 cài đặt",
       "- Bot B giữ đúng cài đặt của cả 2\n"
       "- Không bị đảo giá trị",
       note="Gộp 2 giá trị vì cùng kết quả. Nguồn: Backup (job) r61-r62 · Backup 1.0 r26-r27."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Copy bố cục vùng bấm — cả bố cục có sẵn và bố cục tự chia",
       CP + "\n- Bot A có 4 richmenu: cỡ lớn dùng bố cục có sẵn, cỡ lớn tự chia vùng, "
            "cỡ nhỏ dùng bố cục có sẵn, cỡ nhỏ tự chia vùng",
       RUN + "3. Mở bước bố cục của cả 4 richmenu ở bot B\n"
             "4. Đối chiếu kiểu bố cục và số vùng bấm với bot A\n"
             "5. Với richmenu tự chia, đối chiếu toạ độ từng vùng",
       "4 richmenu: 2500×1686 (bố cục sẵn + tự chia) · 2500×843 (bố cục sẵn + tự chia)",
       "- Cả 4 richmenu giữ đúng kiểu bố cục và cỡ ảnh\n"
       "- Số vùng bấm khớp bot A\n"
       "- Với richmenu tự chia: toạ độ từng vùng khớp bot A, không lệch",
       note="Gộp 4 tổ hợp vì cùng 1 kết quả (giữ nguyên bố cục). "
            "Nguồn: Backup (job) r63-r66 — template_type IN (1..7) / 8 / (9..12) / 8."),

    tc("Copy リッチメニュー", "FUNC-DATE-001", "Abnormal",
       "Richmenu có đặt lịch hiển thị — lịch có được copy sang không?",
       CP + "\n- Bot A có 3 richmenu: (a) không đặt lịch, (b) đặt cả ngày bắt đầu và ngày kết thúc, "
            "(c) chỉ đặt ngày kết thúc",
       RUN + "3. Mở phần đặt lịch hiển thị của cả 3 richmenu ở bot B\n"
             "4. Ghi lại giá trị thực tế từng cái\n"
             "5. Chờ qua mốc thời gian đã đặt ở bot A và quan sát richmenu ở bot B",
       "(a) không đặt · (b) 2026-09-01 09:00 → 2026-09-30 23:59 · (c) chỉ kết thúc 2026-09-30 23:59",
       "- Kết quả theo quyết định MT-11:\n"
       "  · nếu chốt KHÔNG copy lịch: cả 3 richmenu ở bot B đều KHÔNG có lịch hiển thị\n"
       "  · nếu chốt CÓ copy: giá trị ngày giờ khớp chính xác bot A\n"
       "- Bước 5: richmenu ở bot B KHÔNG tự bật/tắt theo lịch của bot A nếu lịch không được copy",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-11 — Backup (job) r67-r70 nói KHÔNG copy lịch; Backup 1.0 r28-r29 nói phải check lịch. "
            "PRODUCTION vì phụ thuộc job hiển thị richmenu (RULE-08)."),

    tc("Copy リッチメニュー", "DATA-ID-001", "Normal",
       "Mọi hành động trong richmenu đều được cấp mã hành động MỚI ở bot nhận",
       CP + "\n- Bot A có 1 richmenu có 4 vùng bấm, mỗi vùng gắn 1 hành động khác nhau",
       RUN + "3. Ghi lại mã hành động của 4 vùng ở bot A\n"
             "4. Mở richmenu tương ứng ở bot B, ghi lại mã hành động của 4 vùng\n"
             "5. So sánh 2 bộ mã\n"
             "6. Sửa hành động ở bot B rồi kiểm tra hành động ở bot A",
       "1 richmenu 4 vùng",
       "- 4 mã hành động ở bot B KHÁC hoàn toàn 4 mã ở bot A\n"
       "- Bước 6: sửa ở bot B KHÔNG làm đổi hành động ở bot A (hai bên độc lập)",
       note="Nguồn: Backup (job) r71, r82, r96 —「TẠO RA ACTION_ID MỚI」lặp lại ở cả 3 nhóm hành động."),

    tc("Copy リッチメニュー", "MSG-001", "Normal",
       "Hành động gửi tin văn bản có chèn thông tin bạn bè — mã chèn trỏ đúng bot nhận",
       CP + "\n- Bot A có thông tin bạn bè「info-name-A1」\n"
            "- Bot A có richmenu với 1 vùng gắn hành động gửi tin văn bản có chèn thông tin đó",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem nội dung tin văn bản\n"
             "4. Đọc mã chèn thông tin bạn bè trong nội dung\n"
             "5. Bấm vùng đó từ máy LINE thật (là bạn bè của bot B, đã có giá trị thông tin)",
       "Nội dung:「{info-name-A1}様、こんにちは」",
       "- Mã chèn trong nội dung ở bot B trỏ tới thông tin bạn bè của BOT B\n"
       "- Bước 5: tin nhận trên LINE hiển thị đúng GIÁ TRỊ của bạn bè bot B, không phải mã thô, "
       "không phải giá trị của bot A",
       note="Nguồn: Backup (job) r71 —「Check việc insert friend info đúng code của bot đích」. "
            "RULE-06 verify tới tin trên LINE."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động kịch bản trong richmenu — 3 kiểu bắt đầu/dừng đều trỏ đúng kịch bản bot nhận",
       CP + "\n- Bot A có kịch bản 5 bước và 1 richmenu có 3 vùng: bắt đầu từ đầu, bắt đầu từ giữa, dừng kịch bản",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 3 hành động kịch bản\n"
             "4. Đối chiếu kịch bản và bước được chọn với bot A\n"
             "5. Bấm lần lượt 3 vùng từ máy LINE thật và kiểm tra ở màn ステップ配信 bot B",
       "1 kịch bản 5 bước · 3 vùng bấm",
       "- Cả 3 hành động trỏ tới kịch bản ĐÃ COPY sang bot B\n"
       "- Hành động「bắt đầu từ giữa」trỏ đúng bước đã chọn (không nhảy về bước 1)\n"
       "- Bước 5: bạn bè vào/ra kịch bản đúng như thiết kế",
       note="Nguồn: Backup (job) r72 —「start scenario từ đầu / start scenario từ giữa / stop scenario」."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động gắn thẻ và gỡ thẻ trong richmenu",
       CP + "\n- Bot A có thẻ「タグ-RM」và 1 richmenu có 2 vùng: gắn thẻ và gỡ thẻ",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 2 hành động thẻ\n"
             "4. Đối chiếu thẻ được trỏ tới\n"
             "5. Bấm lần lượt 2 vùng từ máy LINE thật và kiểm tra ở màn 友だちリスト bot B",
       "1 thẻ + 2 vùng bấm",
       "- Cả 2 hành động trỏ tới thẻ của BOT B\n"
       "- Bước 5: thẻ được gắn rồi gỡ đúng trên bạn bè của bot B\n"
       "- Số người gắn thẻ ở bot A không đổi",
       note="Nguồn: Backup (job) r73 —「gắn tag / xóa tag」."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động gửi mẫu tin trong richmenu",
       CP + "\n- Bot A có mẫu tin kiểu nút bấm và 1 richmenu có vùng gắn hành động gửi mẫu tin đó",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem hành động gửi mẫu tin\n"
             "4. Đối chiếu mẫu tin được trỏ tới\n"
             "5. Bấm vùng đó từ máy LINE thật",
       "1 mẫu tin kiểu nút bấm có ảnh",
       "- Hành động trỏ tới mẫu tin của BOT B\n"
       "- Bước 5: nhận đúng mẫu tin trên LINE, ảnh hiển thị được",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r74. PRODUCTION vì có media (RULE-08)."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Abnormal",
       "Hành động nhắc lịch trong richmenu — kiểm tra có còn trỏ id bot gửi không",
       CP + "\n- Bot A có nhắc lịch và 1 richmenu có 2 vùng: bắt đầu nhắc lịch và dừng nhắc lịch",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 2 hành động nhắc lịch\n"
             "4. Kiểm tra popup cài đặt hành động có hiển thị nhắc lịch của bot B không\n"
             "5. Bấm vùng bắt đầu từ máy LINE thật và chờ tin nhắc",
       "1 nhắc lịch + 2 vùng bấm",
       "- Cả 2 hành động trỏ tới nhắc lịch của BOT B\n"
       "- Bước 5: nhận tin nhắc từ bot B\n"
       "- ⚠️ Nếu popup để trống hoặc tin gửi từ bot A thì raise bug",
       spec="Đã hỏi leader",
       note=MT16 + "Nguồn: Backup 1.0 r46 (ghi lỗi) · Backup (job) r75. ⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động đánh dấu / bỏ đánh dấu trong richmenu",
       CP + "\n- Bot A có richmenu với 2 vùng: đánh dấu và bỏ đánh dấu",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 2 hành động\n"
             "4. Bấm lần lượt 2 vùng từ máy LINE thật\n"
             "5. Kiểm tra ở màn chat 1:1 của bot B",
       "2 vùng bấm",
       "- Cả 2 hành động được copy đủ\n"
       "- Bước 4-5: bạn bè được đánh dấu rồi bỏ đánh dấu đúng ở bot B",
       note="Nguồn: Backup (job) r76 —「bookmark / unbookmark」."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động ghi thông tin bạn bè trong richmenu — đủ 6 kiểu thông tin",
       CP + "\n- Bot A có 6 thông tin bạn bè: mặc định, địa chỉ mặc định, mô tả, điểm, ngày tháng, lựa chọn\n"
            "- Bot A có richmenu với 6 vùng, mỗi vùng ghi vào 1 kiểu",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 6 hành động\n"
             "4. Đối chiếu từng hành động trỏ tới thông tin nào\n"
             "5. Bấm cả 6 vùng từ máy LINE thật rồi mở chi tiết bạn bè ở bot B",
       "6 kiểu: mặc định · địa chỉ mặc định · mô tả · điểm · ngày tháng · lựa chọn",
       "- Cả 6 hành động trỏ tới thông tin bạn bè của BOT B\n"
       "- Bước 5: cả 6 giá trị được ghi đúng vào bạn bè của bot B\n"
       "- Không có hành động nào bị mất hoặc trỏ sang bot A",
       note="Gộp 6 kiểu vì cùng 1 kết quả. Nguồn: Backup (job) r77 —「info default / info địa chỉ default / "
            "info text / info point / info date / info select」."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động đổi trạng thái xử lý và chặn/ẩn bạn bè trong richmenu",
       CP + "\n- Bot A có trạng thái xử lý tự tạo và richmenu có các vùng: gắn/bỏ trạng thái, "
            "chặn/bỏ chặn, hiện/ẩn bạn bè",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem các hành động này\n"
             "4. Kiểm tra hành động trạng thái xử lý trỏ tới trạng thái nào\n"
             "5. Bấm lần lượt từ máy LINE thật và kiểm tra ở màn 友だちリスト bot B",
       "2 vùng trạng thái + 4 vùng chặn/ẩn",
       "- Hành động trạng thái xử lý trỏ tới trạng thái ĐÃ COPY sang bot B\n"
       "- Các hành động chặn/bỏ chặn/hiện/ẩn được copy đủ 4 kiểu\n"
       "- Bước 5: thao tác chạy đúng trên bạn bè của bot B",
       note="Gộp vì cùng kết quả. Nguồn: Backup (job) r78-r79."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động có gắn bộ lọc — bộ lọc được nhân bản riêng cho bot nhận",
       CP + "\n- Bot A có 1 richmenu với vùng gắn hành động có bộ lọc (điều kiện: có thẻ「タグ-F」)",
       RUN + "3. Mở chi tiết richmenu ở bot B, mở bộ lọc của hành động đó\n"
             "4. Đối chiếu điều kiện lọc với bot A\n"
             "5. Sửa điều kiện lọc ở bot B (đổi sang thẻ khác)\n"
             "6. Quay lại bot A kiểm tra bộ lọc gốc\n"
             "7. Làm ngược lại: sửa ở bot A rồi kiểm tra ở bot B",
       "1 bộ lọc điều kiện theo thẻ",
       "- Điều kiện lọc ở bot B giống bot A nhưng trỏ tới thẻ của BOT B\n"
       "- Bước 6: bộ lọc ở bot A KHÔNG bị đổi\n"
       "- Bước 7: bộ lọc ở bot B KHÔNG bị đổi\n"
       "- Hai bộ lọc hoàn toàn độc lập",
       note="Nguồn: Backup (job) r80 —「Cần Tạo ra filter_id mới; khi edit filter ở bot nguồn hoặc bot đích "
            "thì không ảnh hưởng đến filter của bot còn lại」. Xem thêm MT-13."),

    tc("Copy リッチメニュー", "OUT-TRUTH-001", "Normal",
       "Bạn bè bấm vùng có hành động エルメ sau khi copy — hành động chạy đúng",
       CP + "\n- Đã copy xong richmenu có hành động エルメ sang bot B\n"
            "- Có tài khoản LINE là bạn bè của bot B",
       "1. Ở bot B, bật hiển thị richmenu\n"
       "2. Mở LINE bằng tài khoản bạn bè của bot B\n"
       "3. Bấm vùng có gắn hành động エルメ\n"
       "4. Quan sát tin nhận được và kiểm tra ở màn admin bot B",
       "1 vùng có hành động gửi tin + gắn thẻ",
       "- Nhận đúng tin đã cài đặt trên LINE\n"
       "- Thẻ được gắn cho đúng bạn bè đó ở bot B\n"
       "- KHÔNG có tác động nào sang bot A",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r81 —「friend click area có setting action lme, send đúng action đã setting」. "
            "PRODUCTION theo RULE-08 (verify tới LINE thật)."),

    tc("Copy リッチメニュー", "REG-URL-001", "Normal",
       "Hành động mở URL thường trong richmenu",
       CP + "\n- Bot A có richmenu với vùng mở URL thường (https://example.com/campaign)",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem hành động mở URL\n"
             "4. Đối chiếu URL với bot A\n"
             "5. Bấm vùng đó từ máy LINE thật",
       "https://example.com/campaign",
       "- URL ở bot B giống hệt bot A\n"
       "- Bước 5: mở đúng trang đó trên LINE",
       note="Nguồn: Backup (job) r82 · Backup 1.0 r32."),

    tc("Copy リッチメニュー", "REG-URL-001", "Normal",
       "Hành động mở biểu mẫu trong richmenu — trỏ đúng biểu mẫu MỚI của bot nhận",
       CP + "\n- Bot A có biểu mẫu「フォーム-A1」và richmenu có vùng mở biểu mẫu đó",
       RUN + "3. Mở màn フォーム作成 ở bot B, ghi lại mã của biểu mẫu đã copy\n"
             "4. Mở chi tiết richmenu ở bot B, xem hành động mở biểu mẫu trỏ tới đâu\n"
             "5. Bấm vùng đó từ máy LINE thật, quan sát URL biểu mẫu mở ra",
       "1 biểu mẫu「フォーム-A1」",
       "- Hành động trỏ tới biểu mẫu của BOT B\n"
       "- Bước 5: URL biểu mẫu mở ra chứa mã của BOT B, không phải mã của bot A\n"
       "- Điền và gửi được biểu mẫu, câu trả lời vào bot B",
       note="Nguồn: Backup (job) r83 · Backup 1.0 r33. RULE-06 verify tới trang biểu mẫu mở ra."),

    tc("Copy リッチメニュー", "REG-URL-001", "Abnormal",
       "Hành động mở đặt lịch salon trong richmenu — bot nhận hiển thị ra sao?",
       CP + "\n- Bot A có đặt lịch salon và richmenu có vùng mở URL salon đó",
       RUN + "3. Mở chi tiết richmenu ở bot B, mở đúng vùng đó\n"
             "4. Ghi lại nguyên trạng: vùng còn hành động không, danh sách chọn salon có gì\n"
             "5. Nếu vùng vẫn có hành động thì bấm từ máy LINE thật xem mở ra gì",
       "1 salon ở bot A",
       "- Kết quả theo quyết định MT-12 — ghi rõ 1 trong 3 khả năng:\n"
       "  (a) vùng mất hành động, (b) vùng còn hành động nhưng danh sách chọn salon rỗng, "
       "(c) vùng trỏ tới salon của BOT A (⚠️ rò rỉ dữ liệu chéo bot — raise bug ngay)",
       spec="Đã hỏi leader",
       note="MT-12 — Backup (job) r84 nguyên văn có DẤU HỎI:「2 cái này sẽ không backup được do chưa có job "
            "backup của salon và lesson?」và ô kết quả KHÔNG nói bot đích hiển thị gì."),

    tc("Copy リッチメニュー", "REG-URL-001", "Abnormal",
       "Hành động mở đặt lịch lesson trong richmenu — bot nhận hiển thị ra sao?",
       CP + "\n- Bot A có đặt lịch lesson và richmenu có vùng mở URL lesson đó",
       RUN + "3. Mở chi tiết richmenu ở bot B, mở đúng vùng đó\n"
             "4. Ghi lại nguyên trạng: vùng còn hành động không, danh sách chọn lesson có gì\n"
             "5. Nếu vùng vẫn có hành động thì bấm từ máy LINE thật xem mở ra gì",
       "1 lesson ở bot A",
       "- Kết quả theo quyết định MT-12 — ghi rõ 1 trong 3 khả năng như TC salon\n"
       "- ⚠️ Nếu trỏ tới lesson của bot A thì raise bug rò rỉ dữ liệu chéo bot",
       spec="Đã hỏi leader",
       note="MT-12 — Backup (job) r85. Tách khỏi TC salon vì là 2 tính năng khác nhau, "
            "có thể cho kết quả khác nhau."),

    tc("Copy リッチメニュー", "REG-URL-001", "Normal",
       "Hành động mở đặt lịch sự kiện trong richmenu",
       CP + "\n- Bot A có sự kiện đặt lịch và richmenu có vùng mở sự kiện đó",
       RUN + "3. Mở màn イベント予約 ở bot B, xác nhận sự kiện đã copy\n"
             "4. Mở chi tiết richmenu ở bot B, xem hành động trỏ tới sự kiện nào\n"
             "5. Bấm vùng đó từ máy LINE thật và thử đặt chỗ",
       "1 sự kiện có 2 khung giờ",
       "- Hành động trỏ tới sự kiện của BOT B\n"
       "- Bước 5: trang đặt lịch mở ra là của bot B, đặt chỗ thành công và ghi nhận ở bot B",
       note="Nguồn: Backup (job) r86 · Backup 1.0 r34."),

    tc("Copy リッチメニュー", "REG-URL-001", "Abnormal",
       "Hành động mở sản phẩm trong richmenu — sản phẩm không được copy",
       CP + "\n- Bot A có sản phẩm bán hàng và richmenu có 4 vùng: mở sản phẩm đơn, "
            "trang mua sản phẩm chu kỳ, trang đổi thẻ, trang huỷ hợp đồng",
       RUN + "3. Mở màn 商品販売 ở bot B — xác nhận KHÔNG có sản phẩm nào\n"
             "4. Mở chi tiết richmenu ở bot B, mở lần lượt 4 vùng đó\n"
             "5. Mở danh sách chọn sản phẩm trong từng vùng",
       "4 vùng × 4 kiểu trang sản phẩm",
       "- Bot B KHÔNG có sản phẩm nào (sản phẩm không nằm trong phạm vi copy)\n"
       "- Cả 4 vùng: danh sách chọn sản phẩm RỖNG\n"
       "- Vùng chỉ dừng ở mức đang chọn loại hành động sản phẩm, chưa trỏ tới sản phẩm cụ thể\n"
       "- KHÔNG trỏ tới sản phẩm của bot A",
       note="Gộp 4 kiểu vì cùng 1 kết quả. Nguồn: Backup (job) r87-r90 —「Item không backup, nên ở drop down "
            "chọn item không có item, chỉ hiển thị focus vào mục action item」. Xem MT-28."),

    tc("Copy リッチメニュー", "REG-URL-001", "Normal",
       "Hành động mở trang chuyển đổi (conversion) trong richmenu",
       CP + "\n- Bot A có 1 trang chuyển đổi và richmenu có vùng mở trang đó",
       RUN + "3. Mở màn コンバージョン ở bot B, xác nhận đã copy\n"
             "4. Mở chi tiết richmenu ở bot B, xem hành động trỏ tới đâu\n"
             "5. Bấm vùng đó từ máy LINE thật",
       "1 trang chuyển đổi",
       "- Hành động trỏ tới trang chuyển đổi của BOT B\n"
       "- Bước 5: mở đúng trang của bot B, lượt truy cập ghi nhận ở bot B",
       note="Nguồn: Backup (job) r91 · Backup 1.0 r35. Xem thêm MT-17 về folder của conversion."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Hành động gọi điện, gửi email, gửi LINE ID, gửi văn bản trong richmenu",
       CP + "\n- Bot A có richmenu với 4 vùng: số điện thoại, email, LINE ID, văn bản",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 4 vùng đó\n"
             "4. Đối chiếu từng giá trị với bot A\n"
             "5. Bấm lần lượt 4 vùng từ máy LINE thật",
       "① 0312345678 ② info@example.com ③ @linebot-a ④ こんにちは",
       "- Cả 4 giá trị ở bot B giống hệt bot A, không bị cắt hay đổi\n"
       "- Bước 5: mỗi vùng thực hiện đúng hành động tương ứng trên LINE",
       note="Gộp 4 kiểu vì cùng 1 kết quả (giữ nguyên giá trị). "
            "Nguồn: Backup (job) r92-r94 · Backup 1.0 r38-r41 (bản cũ có thêm LineID)."),

    tc("Copy リッチメニュー", "OUT-TRUTH-001", "Normal",
       "Bạn bè bấm vùng có hành động 友だち sau khi copy",
       CP + "\n- Đã copy richmenu có hành động 友だち sang bot B, đã bật hiển thị",
       "1. Mở LINE bằng tài khoản bạn bè của bot B\n"
       "2. Bấm vùng có hành động mở URL\n"
       "3. Bấm vùng có hành động gọi điện\n"
       "4. Quan sát kết quả từng lần",
       "2 vùng khác loại",
       "- Mỗi vùng thực hiện đúng hành động đã cài\n"
       "- KHÔNG mở nhầm URL hay số của bot A",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r95 —「friend click area có setting action friend, send đúng action đã setting」."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động đổi richmenu — trỏ đúng richmenu MỚI của bot nhận",
       CP + "\n- Bot A có 2 richmenu RM-1 và RM-2; RM-1 có 1 vùng đổi sang RM-2 (không kèm bộ lọc)",
       RUN + "3. Mở màn リッチメニュー ở bot B, xác nhận cả 2 richmenu đã copy\n"
             "4. Mở RM-1 ở bot B, xem vùng đổi richmenu trỏ tới đâu\n"
             "5. Bấm vùng đó từ máy LINE thật và quan sát richmenu dưới màn chat",
       "2 richmenu",
       "- Vùng trỏ tới RM-2 của BOT B\n"
       "- Bước 5: richmenu dưới màn chat đổi sang RM-2 của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r96 · r99 · Backup 1.0 r30."),

    tc("Copy リッチメニュー", "DATA-REF-001", "Normal",
       "Hành động đổi richmenu có nhiều lựa chọn và có bộ lọc",
       CP + "\n- Bot A có 1 vùng đổi richmenu cài 2 richmenu KHÔNG bộ lọc\n"
            "- Bot A có 1 vùng khác cài 5 richmenu CÓ bộ lọc",
       RUN + "3. Mở 2 vùng đó ở bot B\n"
             "4. Đếm số richmenu được cài trong mỗi vùng và đối chiếu với bot A\n"
             "5. Mở bộ lọc của vùng 5 richmenu, đối chiếu điều kiện",
       "1 vùng 2 richmenu (không lọc) · 1 vùng 5 richmenu (có lọc)",
       "- Vùng 1: đủ 2 richmenu, đúng thứ tự, trỏ tới richmenu của bot B\n"
       "- Vùng 2: đủ 5 richmenu và có bộ lọc, điều kiện lọc giống bot A nhưng trỏ tới dữ liệu bot B\n"
       "- Mã hành động ở bot B khác bot A",
       note="Nguồn: Backup (job) r97-r98 —「BOT gốc set 2 richmenu không có filter / 5 richmenu có filter」."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Hành động dừng hiển thị richmenu",
       CP + "\n- Bot A có richmenu với 1 vùng gắn hành động dừng hiển thị richmenu",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem vùng đó\n"
             "4. Bấm vùng từ máy LINE thật và quan sát richmenu dưới màn chat",
       "1 vùng dừng richmenu",
       "- Vùng ở bot B giữ đúng hành động dừng hiển thị\n"
       "- Bước 4: richmenu biến mất khỏi màn chat của bạn bè bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r100-r101 · Backup 1.0 r31."),

    tc("Copy リッチメニュー", "INTG-LINE-001", "Normal",
       "Hành động lệnh LINE (URL scheme) — 8 loại đều giữ nguyên",
       CP + "\n- Bot A có richmenu với 8 vùng, mỗi vùng 1 loại lệnh LINE",
       RUN + "3. Mở chi tiết richmenu ở bot B, xem 8 vùng đó\n"
             "4. Đối chiếu từng lệnh với bot A\n"
             "5. Bấm lần lượt cả 8 vùng từ máy LINE thật",
       "① chia sẻ tài khoản LINE ② chia sẻ văn bản cho bạn bè ③ mở camera "
       "④ mở thư viện ảnh ⑤ gửi vị trí ⑥ mở trang cá nhân tài khoản LINE khác "
       "⑦ mở trang kết bạn tài khoản khác ⑧ lệnh tự nhập",
       "- Cả 8 vùng ở bot B giữ nguyên đúng lệnh như bot A\n"
       "- Bước 5: mỗi vùng mở đúng chức năng tương ứng trên LINE\n"
       "- Lệnh tự nhập giữ nguyên chuỗi, không bị cắt ký tự",
       env="PRODUCTION",
       note="Gộp 8 loại vì cùng 1 kết quả (giữ nguyên chuỗi lệnh). "
            "Nguồn: Backup (job) r102-r110. PRODUCTION vì phải bấm trên LINE thật (RULE-08)."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Hành động của vùng bấm CUỐI CÙNG cũng được copy đủ",
       CP + "\n- Bot A có richmenu chia 6 vùng, vùng thứ 6 (cuối cùng) có gắn hành động",
       RUN + "3. Mở chi tiết richmenu ở bot B\n"
             "4. Kiểm tra riêng vùng thứ 6\n"
             "5. Bấm vùng thứ 6 từ máy LINE thật",
       "Richmenu 6 vùng, vùng 6 gắn hành động gửi tin",
       "- Vùng thứ 6 ở bot B có đủ hành động, không bị bỏ sót\n"
       "- Bước 5: hành động chạy đúng",
       note="Nguồn: Backup (job) r111 —「check action của vùng cuối cùng」. "
            "Đây là TC biên chống lỗi vòng lặp bỏ phần tử cuối."),

    tc("Copy リッチメニュー", "UI-FIELD-001", "Normal",
       "Copy chữ hiển thị trên thanh menu (メニューバーのテキスト)",
       CP + "\n- Bot A có 2 richmenu với chữ thanh menu khác nhau, 1 cái dùng tiếng Nhật có ký tự đặc biệt",
       RUN + "3. Mở chi tiết cả 2 richmenu ở bot B\n"
             "4. Đối chiếu chữ thanh menu\n"
             "5. Xem thanh menu dưới màn chat trên LINE",
       "①「メニュー」②「予約・お問合せ🎁」",
       "- Chữ thanh menu ở bot B giống hệt bot A, giữ nguyên ký tự đặc biệt và emoji\n"
       "- Bước 5: hiển thị đúng trên LINE",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r112 (title_menu)."),

    tc("Copy リッチメニュー", "FUNC-001", "Normal",
       "Copy trạng thái bật / tắt richmenu",
       CP + "\n- Bot A có 1 richmenu đang BẬT và 1 richmenu đang TẮT",
       RUN + "3. Mở màn リッチメニュー ở bot B\n"
             "4. Đọc trạng thái bật/tắt của 2 richmenu\n"
             "5. Xem richmenu hiển thị trên LINE của bạn bè bot B",
       "1 bật + 1 tắt",
       "- Bot B giữ đúng trạng thái của cả 2\n"
       "- Bước 5: chỉ richmenu đang bật hiển thị trên LINE",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r113-r114 · Backup 1.0 r52-r53."),

    tc("Copy リッチメニュー", "COMPAT-LEGACY-001", "Normal",
       "Copy các trường mới được bổ sung phía phát triển",
       CP + "\n- Bot A có richmenu dùng bố cục có sẵn, richmenu có dữ liệu lịch hiển thị kiểu cũ, "
            "và richmenu có vùng gắn hành động sản phẩm",
       RUN + "3. Mở chi tiết 3 richmenu đó ở bot B\n"
             "4. Đối chiếu kiểu bố cục, dữ liệu lịch kiểu cũ và loại hành động sản phẩm",
       "3 richmenu tương ứng 3 trường mới",
       "- Kiểu bố cục ở bot B khớp bot A\n"
       "- Dữ liệu lịch hiển thị kiểu cũ được xử lý nhất quán với quyết định MT-11\n"
       "- Loại hành động sản phẩm giữ nguyên dù sản phẩm không được copy",
       spec="Đã hỏi leader",
       note="Nguồn: Backup (job) r115-r117 — 3 cột `rich_menu.template_type`, "
            "`rich_menu.display_end_date_old_data`, `rich_menu_items.type_bill_item`. "
            "⚠️ 3 cột này KHÔNG có trong db-mapping.md — vùng mù của spec."),

    tc("Copy リッチメニュー", "DATA-001", "Normal",
       "Ngày tạo / ngày cập nhật của richmenu ở bot nhận là thời điểm copy",
       CP + "\n- Bot A có richmenu tạo từ ≥ 1 tháng trước",
       RUN + "3. Ghi lại thời điểm chạy copy\n"
             "4. Mở màn リッチメニュー ở bot B, xem ngày tạo của richmenu\n"
             "5. Đối chiếu với ngày tạo ở bot A",
       "Richmenu tạo cách đây ≥1 tháng",
       "- Ngày tạo ở bot B là THỜI ĐIỂM CHẠY COPY, không phải ngày tạo gốc ở bot A\n"
       "- Ngày tạo ở bot A không đổi",
       note="Nguồn: Backup (job) r119 —「created_at / updated_at」nằm trong nhóm「Check các data sẽ không backup」."),

    tc("Copy リッチメニュー", "INTG-LINE-001", "Normal",
       "Gán richmenu cho bạn bè cụ thể ở bot nhận sau khi copy",
       CP + "\n- Đã copy richmenu sang bot B\n- Bot B có ít nhất 2 bạn bè",
       "1. Ở bot B, mở màn 友だちリスト hoặc chat 1:1\n"
       "2. Gán richmenu vừa copy cho bạn bè số 1\n"
       "3. Mở LINE bằng tài khoản bạn bè số 1 và bạn bè số 2\n"
       "4. So sánh richmenu hiển thị",
       "2 bạn bè của bot B",
       "- Gán richmenu thành công, không báo lỗi\n"
       "- Bạn bè số 1 thấy richmenu vừa gán\n"
       "- Bạn bè số 2 không bị đổi richmenu",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r120 —「gán richmenu cho line user」· Backup 1.0 r53 "
            "—「test sau khi backup link rich menu cho user」."),

    tc("Copy リッチメニュー", "FUNC-001", "Abnormal",
       "Richmenu mặc định của bot nhận KHÔNG bị đổi theo bot gửi",
       CP + "\n- Bot A có richmenu mặc định là RM-A\n- Bot B đã có sẵn richmenu mặc định là RM-B",
       RUN + "3. Mở màn リッチメニュー ở bot B\n"
             "4. Kiểm tra richmenu nào đang là mặc định\n"
             "5. Mở LINE bằng bạn bè mới kết bạn với bot B",
       "Bot A mặc định RM-A · bot B mặc định RM-B",
       "- Richmenu mặc định của bot B VẪN là RM-B\n"
       "- KHÔNG bị đổi thành RM-A\n"
       "- Bước 5: bạn bè mới của bot B thấy RM-B",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r51 —「Không set lại rich menu default」."),

    # ═══════════════ 13. Copy ステップ配信 ═══════════════
    tc("Copy ステップ配信", "FUNC-001", "Normal",
       "Copy folder kịch bản — đủ số lượng và đúng thứ tự",
       CP + "\n- Bot A có 3 folder kịch bản (ngoài mặc định), mỗi folder có 2 kịch bản",
       RUN + "3. Mở màn ステップ配信 ở bot B\n"
             "4. Đếm folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số kịch bản",
       "3 folder: 「SCE-FD1」「SCE-FD2」「SCE-FD3」",
       "- Bot B có đủ 3 folder, đúng tên và thứ tự\n"
       "- Mỗi folder có đúng 2 kịch bản, nằm đúng folder như ở bot A",
       note="Nguồn: Backup (job) r123 · r125 · Backup 1.0 r54, r56."),

    tc("Copy ステップ配信", "FUNC-001", "Normal",
       "Copy tên kịch bản",
       CP + "\n- Bot A có 3 kịch bản với tên khác nhau, 1 tên có ký tự tiếng Nhật và emoji",
       RUN + "3. Mở màn ステップ配信 ở bot B\n4. Đối chiếu tên 3 kịch bản",
       "①「シナリオ01」②「新規向け🎁キャンペーン」③「long name 50 ký tự」",
       "- Cả 3 tên ở bot B giống hệt bot A, không bị cắt, không mất emoji",
       note="Nguồn: Backup (job) r124 · Backup 1.0 r55."),

    tc("Copy ステップ配信", "DATA-REF-001", "Normal",
       "Copy cài đặt kịch bản kế tiếp — trỏ đúng kịch bản MỚI của bot nhận",
       CP + "\n- Bot A có kịch bản S1 cài kịch bản kế tiếp là S2",
       RUN + "3. Mở màn ステップ配信 ở bot B, xác nhận cả S1 và S2 đã copy\n"
             "4. Mở cài đặt của S1 ở bot B, xem kịch bản kế tiếp trỏ tới đâu\n"
             "5. Cho 1 bạn bè của bot B chạy hết S1 và quan sát có tự vào S2 không",
       "S1 (2 bước) → S2 (2 bước)",
       "- Cài đặt kịch bản kế tiếp trỏ tới S2 của BOT B\n"
       "- KHÔNG trỏ tới S2 của bot A\n"
       "- Bước 5: bạn bè tự động chuyển sang S2 của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r126 —「id của scen được next đến là id của scen mới backup "
            "(k phải id của scen bot gốc)」. PRODUCTION vì phụ thuộc job gửi bước (RULE-08)."),

    tc("Copy ステップ配信", "FUNC-DATE-001", "Normal",
       "Copy bước kiểu chỉ định ngày giờ gửi — ngày 0 với 3 mốc giờ",
       CP + "\n- Bot A có kịch bản với 3 bước kiểu chỉ định ngày giờ, ngày = 0, giờ lần lượt 00:00 / 12:00 / 23:59",
       RUN + "3. Mở kịch bản đó ở bot B\n"
             "4. Đối chiếu kiểu bước và ngày giờ của cả 3 bước",
       "Ngày 0 · 00:00 · 12:00 · 23:59",
       "- Bot B có đủ 3 bước\n"
       "- Kiểu bước và ngày giờ khớp chính xác cả 3 mốc\n"
       "- Không bước nào bị lệch giờ hay bị đổi kiểu",
       note="Gộp 3 mốc vì cùng 1 kết quả. Nguồn: Backup (job) r127."),

    tc("Copy ステップ配信", "FUNC-DATE-001", "Normal",
       "Copy bước kiểu chỉ định ngày giờ gửi — ngày ≥ 1",
       CP + "\n- Bot A có kịch bản với các bước ngày 1, 2, 7, 30",
       RUN + "3. Mở kịch bản đó ở bot B\n4. Đối chiếu số ngày và giờ gửi của từng bước",
       "Ngày 1 · 2 · 7 · 30",
       "- Bot B có đủ 4 bước, đúng số ngày và giờ gửi\n"
       "- Thứ tự các bước giữ nguyên",
       note="Gộp 4 mốc vì cùng 1 kết quả. Nguồn: Backup (job) r128."),

    tc("Copy ステップ配信", "FUNC-001", "Normal",
       "Copy bước kiểu gửi ngay khi bắt đầu kịch bản",
       CP + "\n- Bot A có kịch bản với 1 bước gửi ngay khi bắt đầu",
       RUN + "3. Mở kịch bản đó ở bot B, kiểm tra kiểu bước\n"
             "4. Cho 1 bạn bè của bot B vào kịch bản và quan sát trên LINE",
       "1 bước gửi ngay",
       "- Bước ở bot B giữ đúng kiểu gửi ngay\n"
       "- Bước 4: bạn bè nhận tin ngay khi vào kịch bản",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r129."),

    tc("Copy ステップ配信", "FUNC-DATE-001", "Boundary",
       "Copy bước kiểu gửi sau N giờ — bao gồm mốc vượt 24 giờ (bug #36322)",
       CP + "\n- Bot A có kịch bản với các bước kiểu gửi sau N giờ ở đủ các mốc trong cột dữ liệu test",
       RUN + "3. Mở kịch bản đó ở bot B\n"
             "4. ĐẾM số bước — phải bằng số bước ở bot A\n"
             "5. Đối chiếu giờ:phút của TỪNG bước, đặc biệt các mốc ≥ 24 giờ",
       "0 giờ 1 phút · 0 giờ 59 phút · 1 giờ · 24 giờ · 25 giờ · 72 giờ",
       "- Bot B có ĐỦ 6 bước — KHÔNG thiếu bước nào\n"
       "- Các bước 24h, 25h, 72h vẫn được tạo đúng, đúng giờ:phút\n"
       "- Không có bước nào bị mất do lỗi định dạng thời gian",
       env="PRODUCTION",
       note="Bug Tester #36322 (5/2026) —「Backup bot step_message lỗi case start_time >= 24h ... "
            "'32:00:00' is an invalid TIME value」. Nguồn: Backup (job) r121-r122, r130-r134 (kết quả OK). "
            "Đây là TC hồi quy chính của bug."),

    tc("Copy ステップ配信", "DATA-REF-001", "Abnormal",
       "Copy hồ sơ người gửi của bước — có được copy không?",
       CP + "\n- Bot A có kịch bản với 1 bước đặt hồ sơ người gửi riêng (tên + ảnh)",
       RUN + "3. Mở bước đó ở bot B\n4. Kiểm tra phần hồ sơ người gửi\n"
             "5. Cho bạn bè bot B nhận bước đó và xem tên/ảnh người gửi trên LINE",
       "1 hồ sơ người gửi có tên và ảnh riêng",
       "- Ghi rõ hiện trạng: hồ sơ người gửi CÓ hay KHÔNG được copy\n"
       "- Nếu không copy: bước ở bot B dùng hồ sơ mặc định của bot B, không lỗi\n"
       "- Bước 5: tên/ảnh hiển thị trên LINE KHÔNG phải của bot A",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Backup 1.0 r61 và Backup (job) r135 đều ghi「không support」và Test Result =「Reject」. "
            "Nhưng spec không nhắc — cần Leader xác nhận đây là hành vi cố ý."),

    tc("Copy ステップ配信", "DATA-REF-001", "Normal",
       "Copy phân nhánh theo bộ lọc trong kịch bản",
       CP + "\n- Bot A có kịch bản 2 nhánh lọc: nhánh có thẻ「タグ-S」và nhánh không có thẻ đó\n"
            "- Mỗi nhánh có 2 bước riêng",
       RUN + "3. Mở kịch bản đó ở bot B\n"
             "4. Đếm số nhánh lọc và đối chiếu điều kiện\n"
             "5. Mở từng nhánh đếm số bước\n"
             "6. Sửa điều kiện lọc ở bot B rồi kiểm tra ở bot A",
       "2 nhánh × 2 bước",
       "- Bot B có đủ 2 nhánh, điều kiện lọc trỏ tới thẻ của BOT B\n"
       "- Mỗi nhánh hiển thị đúng danh sách bước như bot A\n"
       "- Bước 6: sửa ở bot B KHÔNG ảnh hưởng bot A",
       spec="Đã hỏi leader",
       note="⚠️ MÂU THUẪN theo thời gian: Backup 1.0 r62 (bản cũ) ghi「không support」, "
            "Backup (job) r136 (bản mới, kết quả OK) ghi「Back up được các filter của scenario, "
            "sau khi backup hiển thị đúng list step của từng filter」. Theo quy tắc ưu tiên TC mới nhất "
            "thì chọn bản mới. Xem thêm MT-13."),

    tc("Copy ステップ配信", "MSG-001", "Normal",
       "Copy tin nhắn soạn trực tiếp trong bước (không dùng thư viện mẫu tin)",
       CP + "\n- Bot A có kịch bản với 1 bước chứa tin văn bản soạn trực tiếp",
       RUN + "3. Mở bước đó ở bot B, đọc nội dung tin\n"
             "4. Đối chiếu với bot A\n"
             "5. Cho bạn bè bot B nhận bước đó",
       "Nội dung:「ご登録ありがとうございます」",
       "- Nội dung tin ở bot B giống hệt bot A\n"
       "- Bước 5: nhận đúng nội dung đó trên LINE",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r138 · Backup 1.0 r64."),

    tc("Copy ステップ配信", "DATA-REF-001", "Normal",
       "Copy bước dùng mẫu tin từ thư viện — trỏ đúng mẫu tin MỚI của bot nhận",
       CP + "\n- Bot A có mẫu tin「テンプレ-S1」và kịch bản có bước dùng mẫu tin đó",
       RUN + "3. Mở màn テンプレート ở bot B, xác nhận mẫu tin đã copy\n"
             "4. Mở bước đó ở bot B, xem mẫu tin được trỏ tới\n"
             "5. Sửa nội dung mẫu tin ở bot B rồi xem bước có đổi theo không",
       "1 mẫu tin dùng chung",
       "- Bước ở bot B trỏ tới mẫu tin của BOT B\n"
       "- Bước 5: sửa mẫu tin ở bot B thì nội dung bước cũng đổi theo (đúng cơ chế dùng chung)\n"
       "- Mẫu tin ở bot A KHÔNG bị đụng",
       note="Nguồn: Backup (job) r139 —「phải lấy được đúng id của template tương ứng」· Backup 1.0 r65."),

    tc("Copy ステップ配信", "DATA-REF-001", "Normal",
       "Copy bước sao chép từ mẫu tin (không dùng chung)",
       CP + "\n- Bot A có kịch bản với bước tạo bằng cách sao chép nội dung từ mẫu tin",
       RUN + "3. Mở bước đó ở bot B, đọc nội dung\n"
             "4. Sửa mẫu tin gốc ở bot B rồi xem bước có đổi theo không",
       "1 bước sao chép nội dung",
       "- Nội dung bước ở bot B giống bot A\n"
       "- Bước 4: sửa mẫu tin KHÔNG làm đổi nội dung bước (đúng cơ chế sao chép rời)",
       note="Nguồn: Backup (job) r140 · Backup 1.0 r66."),

    tc("Copy ステップ配信", "DATA-ID-001", "Normal",
       "Hành động trong bước kịch bản được cấp mã hành động mới",
       CP + "\n- Bot A có kịch bản với 1 bước gắn hành động (gửi tin + gắn thẻ)",
       RUN + "3. Mở bước đó ở bot B, mở phần hành động\n"
             "4. Đối chiếu hành động với bot A\n"
             "5. Sửa hành động ở bot B rồi kiểm tra ở bot A",
       "1 bước có 2 hành động",
       "- Hành động ở bot B đầy đủ và trỏ tới dữ liệu của bot B\n"
       "- Mã hành động ở bot B khác bot A\n"
       "- Bước 5: sửa ở bot B không ảnh hưởng bot A",
       note="Nguồn: Backup (job) r141 —「Tạo được action mới cho step của bot mới」(kết quả OK)."),

    tc("Copy ステップ配信", "COMPAT-LEGACY-001", "Abnormal",
       "Bước kịch bản có cài richmenu kiểu cũ",
       CP + "\n- Bot A có kịch bản cũ với bước còn dữ liệu cài richmenu (chức năng đã bỏ)",
       RUN + "3. Mở bước đó ở bot B\n4. Kiểm tra bước có mở được không, có hiển thị lỗi không",
       "1 bước kịch bản kiểu cũ",
       "- Bước mở được bình thường ở bot B, không lỗi\n"
       "- Không hiển thị cài đặt richmenu (chức năng đã bỏ)\n"
       "- Các nội dung khác của bước vẫn đủ",
       spec="Đã hỏi leader",
       note="Backup (job) r137 ghi「Hiện tại không còn setting richmenu này nữa」, Test Result =「Reject」. "
            "Backup 1.0 r63 vẫn liệt kê là mục phải check. TC này chỉ để đảm bảo dữ liệu cũ không gây lỗi."),

    tc("Copy ステップ配信", "REG-SHARED-001", "Normal",
       "Kiểm tra ngẫu nhiên vài tính năng khác vẫn copy đủ khi copy kịch bản",
       CP + "\n- Bot A có ≥10 thẻ và ≥10 mẫu tin",
       RUN + "3. Mở màn タグ ở bot B, đếm số thẻ\n"
             "4. Mở màn テンプレート ở bot B, đếm số mẫu tin\n"
             "5. Đối chiếu với bot A",
       "10 thẻ + 10 mẫu tin",
       "- Bot B có đủ 10 thẻ và 10 mẫu tin\n"
       "- Tên từng mục khớp bot A, không thiếu mục nào ở cuối danh sách",
       note="Nguồn: Backup (job) r142-r143 —「job chạy backup được data: Hiển thị đủ list item được backup」."),

    # ═══════════════ 14. Copy テンプレート ═══════════════
    tc("Copy テンプレート", "FUNC-001", "Normal",
       "Copy folder mẫu tin — đủ số lượng và đúng thứ tự",
       CP + "\n- Bot A có 3 folder mẫu tin (ngoài mặc định), mỗi folder chứa 3 mẫu tin",
       RUN + "3. Mở màn テンプレート ở bot B\n4. Đếm folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số mẫu tin",
       "3 folder × 3 mẫu tin",
       "- Bot B có đủ 3 folder đúng tên và thứ tự\n"
       "- Mỗi folder chứa đúng 3 mẫu tin, nằm đúng folder như bot A",
       note="Nguồn: Backup (job) r144 · Backup 1.0 r67."),

    tc("Copy テンプレート", "MSG-001", "Normal",
       "Copy mẫu tin kiểu văn bản — nội dung giữ nguyên",
       CP + "\n- Bot A có 3 mẫu tin văn bản: 1 thuần chữ Nhật, 1 có xuống dòng, 1 có emoji + ký tự đặc biệt",
       RUN + "3. Mở lần lượt 3 mẫu tin ở bot B\n4. Đối chiếu nội dung từng ký tự với bot A\n"
             "5. Gửi cả 3 cho bạn bè bot B từ màn chat 1:1",
       "①「こんにちは」②「1行目\\n2行目\\n3行目」③「🎁50%OFF ★特別価格★」",
       "- Nội dung ở bot B giống hệt bot A: giữ xuống dòng, giữ emoji, giữ ký tự đặc biệt\n"
       "- Bước 5: tin nhận trên LINE hiển thị đúng như vậy",
       env="PRODUCTION",
       note="Gộp 3 nội dung vì cùng 1 kết quả. Nguồn: Backup (job) r145 · Backup 1.0 r68."),

    tc("Copy テンプレート", "DATA-REF-001", "Normal",
       "Mã chèn biểu mẫu trong mẫu tin văn bản được thay thành mã của bot nhận",
       CP + "\n- Bot A có biểu mẫu và 1 mẫu tin văn bản có chèn mã biểu mẫu đó",
       RUN + "3. Ghi lại mã biểu mẫu ở bot A và mã biểu mẫu đã copy ở bot B\n"
             "4. Mở mẫu tin ở bot B, đọc mã chèn trong nội dung\n"
             "5. Gửi mẫu tin cho bạn bè bot B và bấm vào liên kết biểu mẫu",
       "1 biểu mẫu + 1 mẫu tin có mã chèn",
       "- Mã chèn trong mẫu tin ở bot B là mã của BOT B\n"
       "- KHÔNG còn mã của bot A\n"
       "- Bước 5: liên kết mở đúng biểu mẫu của bot B, gửi được câu trả lời vào bot B",
       note="Nguồn: Backup (job) r146 —「Check các chỗ insert code cũ → replace được thành code mới」."),

    tc("Copy テンプレート", "REG-URL-001", "Normal",
       "Đường dẫn biểu mẫu viết thẳng trong mẫu tin văn bản được thay sang bot nhận",
       CP + "\n- Bot A có mẫu tin văn bản chứa đường dẫn biểu mẫu dạng đầy đủ (dán tay)",
       RUN + "3. Mở mẫu tin ở bot B, đọc đường dẫn trong nội dung\n"
             "4. Đối chiếu với đường dẫn biểu mẫu của bot B\n"
             "5. Gửi cho bạn bè bot B và bấm vào đường dẫn",
       "Đường dẫn biểu mẫu đầy đủ dán trong nội dung",
       "- Đường dẫn ở bot B trỏ tới biểu mẫu của BOT B\n"
       "- Bước 5: mở đúng biểu mẫu bot B, không mở biểu mẫu bot A",
       note="Nguồn: Backup (job) r147 —「link của form answer」."),

    tc("Copy テンプレート", "DATA-REF-001", "Normal",
       "Mã chèn thông tin bạn bè trong mẫu tin văn bản được thay sang bot nhận",
       CP + "\n- Bot A có thông tin bạn bè「info-name」và mẫu tin văn bản có chèn mã đó",
       RUN + "3. Mở mẫu tin ở bot B, đọc mã chèn\n"
             "4. Đối chiếu với mã thông tin bạn bè của bot B\n"
             "5. Gửi cho bạn bè bot B (bạn bè này đã có giá trị thông tin) và đọc tin trên LINE",
       "Nội dung:「{info-name}様、こんにちは」",
       "- Mã chèn ở bot B trỏ tới thông tin bạn bè của BOT B\n"
       "- Bước 5: tin trên LINE hiển thị đúng GIÁ TRỊ, không hiển thị mã thô",
       note="Nguồn: Backup (job) r148 —「code của friend-infor」. RULE-06 verify tới tin trên LINE."),

    tc("Copy テンプレート", "COMPAT-LEGACY-001", "Abnormal",
       "Mã chèn sản phẩm kiểu cũ trong mẫu tin văn bản — sản phẩm không được copy",
       CP + "\n- Bot A có mẫu tin văn bản chứa mã chèn sản phẩm kiểu cũ",
       RUN + "3. Mở màn 商品販売 ở bot B — xác nhận KHÔNG có sản phẩm nào\n"
             "4. Mở mẫu tin ở bot B, đọc nội dung có mã chèn sản phẩm\n"
             "5. Gửi cho bạn bè bot B và xem tin nhận được",
       "1 mẫu tin có mã chèn sản phẩm",
       "- Ghi rõ hiện trạng: mã chèn sản phẩm ở bot B còn nguyên mã bot A, bị xoá, hay thành chuỗi rỗng\n"
       "- Bước 5: tin trên LINE KHÔNG hiển thị mã thô khó hiểu và KHÔNG trỏ tới sản phẩm của bot A\n"
       "- Không gây lỗi khi gửi",
       spec="Đã hỏi leader",
       note="MT-28 — Backup (job) r149 chỉ ghi「code của item cũ」mà KHÔNG có kết quả mong đợi. "
            "Sản phẩm nằm ngoài phạm vi copy. Kết quả trên do AI viết, cần Leader chốt."),

    tc("Copy テンプレート", "DATA-REF-001", "Normal",
       "Mã chèn trang chuyển đổi trong mẫu tin văn bản được thay sang bot nhận",
       CP + "\n- Bot A có trang chuyển đổi và mẫu tin văn bản có chèn mã đó",
       RUN + "3. Mở mẫu tin ở bot B, đọc mã chèn\n"
             "4. Đối chiếu với trang chuyển đổi của bot B\n"
             "5. Gửi cho bạn bè bot B và bấm vào liên kết",
       "1 trang chuyển đổi",
       "- Mã chèn ở bot B trỏ tới trang chuyển đổi của BOT B\n"
       "- Bước 5: lượt truy cập ghi nhận ở bot B, không ghi vào bot A",
       note="Nguồn: Backup (job) r150 —「code của conversion」. Xem thêm MT-17."),

    tc("Copy テンプレート", "MEDIA-IMG-001", "Normal",
       "Copy mẫu tin ảnh thường — xem được ở web và gửi được cho bạn bè",
       CP + "\n- Bot A có 2 mẫu tin ảnh: 1 ảnh JPG, 1 ảnh PNG",
       RUN + "3. Mở lần lượt 2 mẫu tin ở bot B, xem ảnh có hiển thị không\n"
             "4. Ghi lại đường dẫn ảnh của bot B và bot A\n"
             "5. Gửi cả 2 cho bạn bè bot B và xem ảnh trên LINE\n"
             "6. Quay lại bot A xem ảnh còn hiển thị không",
       "1 JPG + 1 PNG",
       "- Ảnh hiển thị ở màn quản lý bot B\n"
       "- Đường dẫn ảnh bot B KHÁC bot A\n"
       "- Bước 5: bạn bè nhận và xem được ảnh trên LINE\n"
       "- Bước 6: ảnh ở bot A vẫn nguyên",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r151-r152 · Backup 1.0 r69. PRODUCTION theo RULE-08 (media)."),

    tc("Copy テンプレート", "MEDIA-IMG-001", "Normal",
       "Copy mẫu tin ảnh có vùng bấm (image map) — ảnh và vùng bấm đều giữ nguyên",
       CP + "\n- Bot A có mẫu tin ảnh có vùng bấm, chia 4 vùng, mỗi vùng 1 hành động bạn bè",
       RUN + "3. Mở mẫu tin ở bot B, xem ảnh và bố cục vùng bấm\n"
             "4. Đối chiếu số vùng và hành động từng vùng với bot A\n"
             "5. Gửi cho bạn bè bot B, bấm thử từng vùng trên LINE",
       "1 image map 4 vùng",
       "- Ảnh hiển thị đúng ở bot B, đường dẫn khác bot A\n"
       "- Đủ 4 vùng, đúng toạ độ và đúng hành động\n"
       "- Bước 5: bấm mỗi vùng chạy đúng hành động",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r153, r155-r156 · Backup 1.0 r70."),

    tc("Copy テンプレート", "DATA-ID-001", "Normal",
       "Copy hành động nhiều bước trong mẫu tin ảnh có vùng bấm",
       CP + "\n- Bot A có mẫu tin ảnh có vùng bấm, 1 vùng gắn hành động nhiều bước (gửi tin + gắn thẻ + ghi thông tin)",
       RUN + "3. Mở mẫu tin ở bot B, mở hành động của vùng đó\n"
             "4. Đếm số hành động con và đối chiếu từng cái\n"
             "5. Gửi cho bạn bè bot B và bấm vùng đó",
       "1 vùng × 3 hành động con",
       "- Đủ 3 hành động con ở bot B, đúng thứ tự\n"
       "- Mỗi hành động trỏ tới dữ liệu của BOT B\n"
       "- Bước 5: cả 3 hành động cùng chạy",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r154 · Backup 1.0 r71."),

    tc("Copy テンプレート", "MEDIA-IMG-001", "Normal",
       "Copy mẫu tin kiểu nút bấm — tiêu đề, ảnh, số bảng, số nút giữ nguyên",
       CP + "\n- Bot A có mẫu tin nút bấm 3 bảng, mỗi bảng có tiêu đề + ảnh + 2 nút",
       RUN + "3. Mở mẫu tin ở bot B\n"
             "4. Đếm số bảng, số nút mỗi bảng, đối chiếu tiêu đề và ảnh\n"
             "5. Gửi cho bạn bè bot B và xem trên LINE",
       "3 bảng × 2 nút, mỗi bảng 1 ảnh",
       "- Bot B có đủ 3 bảng, mỗi bảng đủ 2 nút\n"
       "- Tiêu đề và ảnh từng bảng khớp bot A, ảnh hiển thị được\n"
       "- Bước 5: hiển thị đủ 3 bảng trên LINE, vuốt ngang được",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r157, r161 · Backup 1.0 r72."),

    tc("Copy テンプレート", "DATA-ID-001", "Normal",
       "Copy hành động của nút trong mẫu tin nút bấm",
       CP + "\n- Bot A có mẫu tin nút bấm với 1 nút gắn hành động bạn bè và 1 nút gắn hành động nhiều bước",
       RUN + "3. Mở mẫu tin ở bot B, mở hành động của 2 nút\n"
             "4. Đối chiếu với bot A\n"
             "5. Gửi cho bạn bè bot B và bấm thử 2 nút",
       "2 nút × 2 loại hành động",
       "- Cả 2 nút giữ đủ hành động, trỏ tới dữ liệu của BOT B\n"
       "- Bước 5: bấm chạy đúng hành động",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r158-r159 · Backup 1.0 r73-r74."),

    tc("Copy テンプレート", "FUNC-MULTI-001", "Normal",
       "Copy cài đặt số lần bấm được của nút trong mẫu tin",
       CP + "\n- Bot A có mẫu tin nút bấm: 1 nút đặt bấm 1 lần, 1 nút đặt bấm nhiều lần",
       RUN + "3. Mở mẫu tin ở bot B, đối chiếu cài đặt của 2 nút\n"
             "4. Gửi cho bạn bè bot B, bấm mỗi nút 2 lần",
       "1 nút 1 lần + 1 nút nhiều lần",
       "- Cài đặt giữ đúng ở bot B\n"
       "- Bước 4: nút 1 lần chỉ chạy hành động ở lần bấm đầu; nút nhiều lần chạy cả 2 lần",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r160 · Backup 1.0 r75."),

    tc("Copy テンプレート", "MEDIA-001", "Normal",
       "Copy mẫu tin video — video và ảnh đại diện đều xem được",
       CP + "\n- Bot A có 2 mẫu tin video: 1 video có ảnh đại diện tự đặt, 1 video dùng ảnh mặc định",
       RUN + "3. Mở 2 mẫu tin ở bot B, kiểm tra video và ảnh đại diện có hiển thị không\n"
             "4. Ghi lại đường dẫn video và ảnh đại diện của 2 bot\n"
             "5. Gửi cho bạn bè bot B và mở video trên LINE",
       "2 video (1 có ảnh đại diện riêng)",
       "- Video và ảnh đại diện đều hiển thị ở màn quản lý bot B\n"
       "- Đường dẫn khác bot A\n"
       "- Bước 5: bạn bè xem được video trên LINE",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-24 — Backup image r28/r30 ghi ảnh đại diện video = NG; improve url image r29-r30 (mới hơn) "
            "= OK Step nhưng chỉ đo nhánh dữ liệu mới. ⚠️ Nhánh dữ liệu cũ có thể vẫn hỏng. "
            "Nguồn: Backup (job) r162-r163 · Backup 1.0 r76."),

    tc("Copy テンプレート", "MEDIA-001", "Normal",
       "Copy mẫu tin âm thanh",
       CP + "\n- Bot A có 1 mẫu tin âm thanh",
       RUN + "3. Mở mẫu tin ở bot B, thử phát thử ở màn quản lý\n"
             "4. Ghi lại đường dẫn tệp âm thanh 2 bot\n"
             "5. Gửi cho bạn bè bot B và nghe trên LINE",
       "1 tệp âm thanh",
       "- Phát thử được ở màn quản lý bot B\n"
       "- Đường dẫn khác bot A\n"
       "- Bước 5: bạn bè nghe được trên LINE, thời lượng đúng",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r164 · Backup 1.0 r77 · Improve backup media r9."),

    tc("Copy テンプレート", "MSG-001", "Normal",
       "Copy mẫu tin nhãn dán, bản đồ và giới thiệu bạn bè",
       CP + "\n- Bot A có 3 mẫu tin: 1 nhãn dán, 1 bản đồ (có toạ độ + địa chỉ), 1 giới thiệu bạn bè",
       RUN + "3. Mở lần lượt 3 mẫu tin ở bot B\n"
             "4. Đối chiếu nội dung với bot A (mã nhãn dán, toạ độ + địa chỉ)\n"
             "5. Gửi cả 3 cho bạn bè bot B",
       "1 nhãn dán · 1 bản đồ 東京駅 · 1 giới thiệu bạn bè",
       "- Cả 3 mẫu tin ở bot B giữ nguyên nội dung như bot A\n"
       "- Bản đồ giữ đúng toạ độ và địa chỉ\n"
       "- Bước 5: cả 3 gửi được và hiển thị đúng trên LINE",
       env="PRODUCTION",
       note="Gộp 3 loại vì cùng 1 kết quả (giữ nguyên nội dung, không có ánh xạ id). "
            "Nguồn: Backup (job) r165-r167 · Backup 1.0 r78-r80."),

    # ═══════════════ 15. Copy フォーム作成 ═══════════════
    tc("Copy フォーム作成", "FUNC-001", "Normal",
       "Copy folder biểu mẫu và tên biểu mẫu",
       CP + "\n- Bot A có 2 folder biểu mẫu, mỗi folder 2 biểu mẫu\n"
            "- Mỗi biểu mẫu có tên quản lý và tên hiển thị phía LINE khác nhau",
       RUN + "3. Mở màn フォーム作成 ở bot B\n"
             "4. Đếm folder, đối chiếu tên folder và thứ tự\n"
             "5. Mở từng biểu mẫu đối chiếu tên quản lý và tên hiển thị",
       "2 folder × 2 biểu mẫu",
       "- Bot B có đủ 2 folder đúng tên, đúng thứ tự\n"
       "- Mỗi biểu mẫu ở đúng folder\n"
       "- Tên quản lý và tên hiển thị đều khớp bot A",
       note="Nguồn: Backup (job) r168-r169 · Backup 1.0 r81-r82."),

    tc("Copy フォーム作成", "DATA-ID-001", "Normal",
       "Mỗi biểu mẫu được cấp MÃ MỚI ở bot nhận — không dùng lại mã bot gửi",
       CP + "\n- Bot A có 3 biểu mẫu, đã ghi lại mã của cả 3",
       RUN + "3. Mở từng biểu mẫu ở bot B, ghi lại mã (xem ở đường dẫn công khai)\n"
             "4. So sánh 3 mã của bot B với 3 mã của bot A\n"
             "5. Mở đường dẫn biểu mẫu của bot B trên trình duyệt ẩn danh",
       "3 biểu mẫu",
       "- 3 mã ở bot B KHÁC hoàn toàn 3 mã ở bot A\n"
       "- Bước 5: mở được biểu mẫu của bot B\n"
       "- Mở đường dẫn cũ (mã bot A) vẫn ra biểu mẫu của bot A, không bị đụng",
       note="Nguồn: Backup (job) r170 · Backup 1.0 r83 —「mỗi form phải tạo code mới, "
            "không được lấy code của form gốc」."),

    tc("Copy フォーム作成", "UI-FIELD-001", "Normal",
       "Copy các mục hiển thị của biểu mẫu: tiêu đề, đoạn văn bản, ảnh",
       CP + "\n- Bot A có biểu mẫu chứa 1 mục tiêu đề, 1 mục đoạn văn bản, 1 mục ảnh",
       RUN + "3. Mở biểu mẫu ở bot B, đếm số mục và đối chiếu từng mục\n"
             "4. Mở đường dẫn công khai của biểu mẫu bot B trên điện thoại",
       "3 mục hiển thị",
       "- Bot B có đủ 3 mục, đúng thứ tự, đúng nội dung\n"
       "- Ảnh trong mục ảnh hiển thị được, đường dẫn khác bot A\n"
       "- Bước 4: cả 3 mục hiển thị đúng trên trang biểu mẫu",
       env="PRODUCTION",
       note="Gộp 3 mục vì cùng 1 kết quả. Nguồn: Backup (job) r171-r173 · Backup 1.0 r84-r86."),

    tc("Copy フォーム作成", "UI-INPUT-001", "Normal",
       "Copy cài đặt bắt buộc trả lời của mục câu hỏi",
       CP + "\n- Bot A có biểu mẫu với 1 câu hỏi bắt buộc và 1 câu hỏi không bắt buộc",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu cài đặt bắt buộc của 2 câu hỏi\n"
             "4. Mở đường dẫn công khai, bỏ trống câu bắt buộc rồi bấm gửi",
       "1 câu bắt buộc + 1 câu không bắt buộc",
       "- Cài đặt giữ đúng ở bot B\n"
       "- Bước 4: không gửi được, hiện thông báo bắt buộc nhập ở đúng câu đó",
       note="Nguồn: Backup (job) r174 · Backup 1.0 r87."),

    tc("Copy フォーム作成", "UI-INPUT-001", "Normal",
       "Copy câu hỏi kiểu mô tả — kiểu 1 dòng và nhiều dòng",
       CP + "\n- Bot A có biểu mẫu với 1 câu hỏi mô tả 1 dòng và 1 câu hỏi mô tả nhiều dòng",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu kiểu ô nhập của 2 câu\n"
             "4. Mở đường dẫn công khai và nhập thử vào cả 2 ô",
       "1 dòng + nhiều dòng",
       "- Kiểu ô nhập giữ đúng ở bot B\n"
       "- Bước 4: ô nhiều dòng xuống dòng được, ô 1 dòng thì không",
       note="Nguồn: Backup (job) r175 · Backup 1.0 r88."),

    tc("Copy フォーム作成", "UI-INPUT-001", "Normal",
       "Copy quy tắc kiểm tra dữ liệu của câu hỏi kiểu mô tả",
       CP + "\n- Bot A có biểu mẫu với 4 câu hỏi mô tả đặt 4 quy tắc: không kiểm tra, katakana, "
            "số điện thoại, email",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu quy tắc của cả 4 câu\n"
             "4. Mở đường dẫn công khai, nhập giá trị SAI quy tắc vào từng câu rồi bấm gửi",
       "① không kiểm tra ② カタカナ ③ 0312345678 ④ test@example.com; "
       "giá trị sai: 「abc」cho katakana, 「abc」cho số đt, 「abc」cho email",
       "- Cả 4 quy tắc giữ đúng ở bot B\n"
       "- Bước 4: 3 câu có quy tắc đều báo lỗi đúng loại; câu không kiểm tra thì nhận mọi giá trị",
       note="Gộp 4 quy tắc vì cùng 1 kết quả (giữ nguyên quy tắc). Nguồn: Backup (job) r176 · Backup 1.0 r89."),

    tc("Copy フォーム作成", "DATA-REF-001", "Normal",
       "Câu hỏi mô tả có liên kết thông tin bạn bè — trỏ đúng thông tin bot nhận",
       CP + "\n- Bot A có thông tin bạn bè kiểu mô tả và biểu mẫu có câu hỏi liên kết tới nó",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận thông tin đã copy\n"
             "4. Mở biểu mẫu ở bot B, xem câu hỏi liên kết tới thông tin nào\n"
             "5. Cho bạn bè của bot B mở biểu mẫu, trả lời và gửi\n"
             "6. Mở chi tiết bạn bè đó ở bot B",
       "1 thông tin bạn bè kiểu mô tả",
       "- Câu hỏi liên kết tới thông tin của BOT B\n"
       "- Bước 6: giá trị vừa gửi được ghi vào đúng bạn bè của bot B\n"
       "- Dữ liệu bạn bè ở bot A không bị đụng",
       note="Nguồn: Backup (job) r177 · Backup 1.0 r90. RULE-07 verify 3 tầng: cài đặt + trang biểu mẫu + chi tiết bạn bè."),

    tc("Copy フォーム作成", "UI-INPUT-001", "Normal",
       "Copy câu hỏi kiểu lựa chọn — 3 hình thức chọn và danh sách đáp án",
       CP + "\n- Bot A có biểu mẫu với 3 câu hỏi lựa chọn: ô tích nhiều, nút tròn, danh sách xổ xuống\n"
            "- Mỗi câu có 4 đáp án",
       RUN + "3. Mở biểu mẫu ở bot B\n"
             "4. Đối chiếu hình thức chọn của cả 3 câu\n"
             "5. Đối chiếu danh sách đáp án (nội dung và thứ tự) của từng câu\n"
             "6. Mở đường dẫn công khai và trả lời thử cả 3 câu",
       "3 câu × 4 đáp án",
       "- Cả 3 hình thức chọn giữ đúng ở bot B\n"
       "- Mỗi câu đủ 4 đáp án, đúng nội dung và đúng thứ tự\n"
       "- Bước 6: chọn và gửi được bình thường",
       note="Gộp 3 hình thức vì cùng 1 kết quả. Nguồn: Backup (job) r178-r181 · Backup 1.0 r91-r94."),

    tc("Copy フォーム作成", "DATA-REF-001", "Normal",
       "Đáp án lựa chọn có liên kết thẻ — trỏ đúng thẻ của bot nhận",
       CP + "\n- Bot A có thẻ「タグ-F1」「タグ-F2」và biểu mẫu có câu lựa chọn, "
            "mỗi đáp án liên kết 1 thẻ",
       RUN + "3. Mở màn タグ ở bot B, xác nhận 2 thẻ đã copy\n"
             "4. Mở biểu mẫu ở bot B, xem từng đáp án liên kết tới thẻ nào\n"
             "5. Cho bạn bè của bot B trả lời chọn đáp án 1 và gửi\n"
             "6. Mở màn 友だちリスト ở bot B kiểm tra thẻ của bạn bè đó",
       "2 đáp án × 2 thẻ",
       "- Các đáp án liên kết tới thẻ của BOT B\n"
       "- Bước 6: bạn bè được gắn đúng thẻ tương ứng đáp án đã chọn, ở bot B\n"
       "- Số người gắn thẻ ở bot A không đổi",
       note="Nguồn: Backup (job) r182 · Backup 1.0 r95."),

    tc("Copy フォーム作成", "DATA-REF-001", "Normal",
       "Câu hỏi lựa chọn có liên kết thông tin bạn bè",
       CP + "\n- Bot A có thông tin bạn bè kiểu lựa chọn và biểu mẫu có câu lựa chọn liên kết tới nó",
       RUN + "3. Mở biểu mẫu ở bot B, xem câu hỏi liên kết tới thông tin nào\n"
             "4. Cho bạn bè bot B trả lời và gửi\n"
             "5. Mở chi tiết bạn bè đó ở bot B",
       "1 thông tin kiểu lựa chọn có 4 giá trị",
       "- Câu hỏi liên kết tới thông tin của BOT B\n"
       "- Bước 5: giá trị đã chọn được ghi vào đúng bạn bè bot B",
       note="Nguồn: Backup (job) r183 · Backup 1.0 r96."),

    tc("Copy フォーム作成", "FUNC-DATE-001", "Normal",
       "Copy câu hỏi kiểu ngày tháng — có và không kèm giờ",
       CP + "\n- Bot A có biểu mẫu với 1 câu ngày tháng KHÔNG kèm giờ và 1 câu CÓ kèm giờ\n"
            "- Cả 2 câu đều liên kết tới thông tin bạn bè kiểu ngày tháng",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu cài đặt của 2 câu\n"
             "4. Kiểm tra liên kết thông tin bạn bè\n"
             "5. Cho bạn bè bot B trả lời và gửi, rồi mở chi tiết bạn bè ở bot B",
       "1 câu chỉ ngày · 1 câu ngày + giờ",
       "- Cài đặt kèm giờ giữ đúng ở cả 2 câu\n"
       "- Liên kết trỏ tới thông tin của BOT B\n"
       "- Bước 5: giá trị ngày (và giờ) được ghi đúng vào bạn bè bot B",
       note="Nguồn: Backup (job) r184-r185 · Backup 1.0 r97-r98."),

    tc("Copy フォーム作成", "DATA-REF-001", "Abnormal",
       "Câu hỏi kiểu nhắc lịch — kiểm tra có còn trỏ nhắc lịch của bot gửi không",
       CP + "\n- Bot A có nhắc lịch「リマインド-F1」và biểu mẫu có câu hỏi nhắc lịch với 3 hình thức chọn, "
            "mỗi đáp án gắn 1 nhắc lịch",
       RUN + "3. Mở màn リマインド配信 ở bot B, ghi lại nhắc lịch đã copy\n"
             "4. Mở biểu mẫu ở bot B, xem từng đáp án gắn nhắc lịch nào\n"
             "5. ĐẾM số mục trong biểu mẫu ở bot B, so với bot A\n"
             "6. Cho bạn bè bot B trả lời và chờ tới giờ nhắc",
       "3 hình thức chọn × các đáp án gắn nhắc lịch",
       "- Đáp án phải gắn nhắc lịch của BOT B\n"
       "- Bước 5: số mục ở bot B BẰNG bot A — KHÔNG bị nhân đôi mục\n"
       "- Bước 6: tin nhắc gửi từ bot B\n"
       "- ⚠️ Nếu mục bị nhân đôi hoặc nhắc lịch trỏ bot A thì raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=MT16 + "Nguồn: Backup 1.0 r102 —「Bảng form_answer_details, cột setting vẫn đang để id remind "
            "của bot gốc → form có remind bị thêm lỗi DUPLICATE ITEM」. Backup (job) r186-r189 không ghi chú. "
            "⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy フォーム作成", "UI-FIELD-001", "Normal",
       "Copy mục ghi chú và câu hỏi kiểu tệp đính kèm",
       CP + "\n- Bot A có biểu mẫu chứa 1 mục ghi chú và 1 câu hỏi tệp đính kèm "
            "(liên kết thông tin bạn bè kiểu tệp)",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu 2 mục\n"
             "4. Kiểm tra liên kết thông tin bạn bè của câu tệp\n"
             "5. Cho bạn bè bot B tải lên 1 tệp và gửi, rồi mở chi tiết bạn bè ở bot B",
       "1 mục ghi chú + 1 câu tệp (PDF)",
       "- Cả 2 mục có đủ ở bot B, nội dung ghi chú giữ nguyên\n"
       "- Liên kết trỏ tới thông tin của BOT B\n"
       "- Bước 5: tệp tải lên được lưu và xem lại được ở bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r190-r191 · Backup 1.0 r103-r104."),

    tc("Copy フォーム作成", "MEDIA-IMG-001", "Normal",
       "Copy ảnh nền của biểu mẫu",
       CP + "\n- Bot A có biểu mẫu đặt ảnh nền riêng",
       RUN + "3. Mở tab cài đặt chung của biểu mẫu ở bot B, xem ảnh nền\n"
             "4. Ghi lại đường dẫn ảnh nền 2 bot\n"
             "5. Mở đường dẫn công khai của biểu mẫu bot B trên điện thoại",
       "1 ảnh nền JPG",
       "- Ảnh nền hiển thị ở màn cài đặt bot B\n"
       "- Đường dẫn khác bot A\n"
       "- Bước 5: ảnh nền hiển thị đúng trên trang biểu mẫu công khai",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r192 · Backup 1.0 r105 · Improve backup media r51."),

    tc("Copy フォーム作成", "FUNC-MULTI-001", "Normal",
       "Copy cài đặt trả lời 1 lần / nhiều lần và giao diện tuỳ chỉnh",
       CP + "\n- Bot A có 1 biểu mẫu đặt trả lời 1 lần và 1 biểu mẫu đặt trả lời nhiều lần\n"
            "- Cả 2 đều có giao diện tuỳ chỉnh (CSS)",
       RUN + "3. Mở tab cài đặt chung của cả 2 biểu mẫu ở bot B\n"
             "4. Đối chiếu cài đặt số lần trả lời và nội dung giao diện tuỳ chỉnh\n"
             "5. Cho bạn bè bot B trả lời biểu mẫu 1-lần hai lần liên tiếp",
       "2 biểu mẫu + nội dung CSS tuỳ chỉnh",
       "- Cài đặt số lần trả lời giữ đúng ở cả 2\n"
       "- Nội dung giao diện tuỳ chỉnh giữ nguyên từng ký tự\n"
       "- Bước 5: lần thứ 2 bị chặn ở biểu mẫu 1-lần\n"
       "- Trang biểu mẫu công khai của bot B áp dụng đúng giao diện tuỳ chỉnh",
       note="Nguồn: Backup (job) r193-r194 · Backup 1.0 r106-r107."),

    tc("Copy フォーム作成", "DATA-ID-001", "Normal",
       "Copy hành động khi MỞ biểu mẫu",
       CP + "\n- Bot A có biểu mẫu đặt hành động khi mở: gửi tin + gắn thẻ, cài chạy 1 lần",
       RUN + "3. Mở tab cài đặt chung ở bot B, xem hành động khi mở\n"
             "4. Đối chiếu số hành động con và cài đặt số lần\n"
             "5. Cho bạn bè bot B MỞ biểu mẫu (không gửi) rồi kiểm tra thẻ và tin nhận được",
       "2 hành động con, chạy 1 lần",
       "- Hành động khi mở đủ 2 hành động con, trỏ dữ liệu BOT B\n"
       "- Cài đặt chạy 1 lần giữ đúng\n"
       "- Bước 5: mở biểu mẫu là hành động chạy, bạn bè nhận tin và được gắn thẻ ở bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r195-r196 · Backup 1.0 r108-r109."),

    tc("Copy フォーム作成", "DATA-ID-001", "Normal",
       "Copy hành động khi GỬI biểu mẫu",
       CP + "\n- Bot A có biểu mẫu đặt hành động khi gửi: gửi tin + bắt đầu kịch bản, cài chạy nhiều lần",
       RUN + "3. Mở tab cài đặt chung ở bot B, xem hành động khi gửi\n"
             "4. Đối chiếu hành động và cài đặt số lần\n"
             "5. Cho bạn bè bot B trả lời và gửi, rồi kiểm tra tin nhận được và kịch bản đã vào",
       "2 hành động con, chạy nhiều lần",
       "- Hành động khi gửi đủ 2 hành động con, trỏ dữ liệu BOT B\n"
       "- Kịch bản được bắt đầu là kịch bản của BOT B\n"
       "- Bước 5: bạn bè nhận tin và vào kịch bản của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r197-r198 · Backup 1.0 r110-r111."),

    tc("Copy フォーム作成", "REG-URL-001", "Normal",
       "Copy cài đặt trang sau khi gửi — 3 lựa chọn",
       CP + "\n- Bot A có 3 biểu mẫu, mỗi cái đặt 1 lựa chọn: về màn chat, mở URL, hiện trang nội dung tự soạn",
       RUN + "3. Mở tab cài đặt chung của cả 3 biểu mẫu ở bot B\n"
             "4. Đối chiếu lựa chọn và nội dung kèm theo (URL, nội dung tự soạn)\n"
             "5. Cho bạn bè bot B gửi từng biểu mẫu và quan sát trang hiện ra",
       "① về màn chat ② https://example.com/thanks ③ nội dung tự soạn có ảnh",
       "- Cả 3 lựa chọn giữ đúng ở bot B\n"
       "- URL và nội dung tự soạn giữ nguyên\n"
       "- Bước 5: mỗi biểu mẫu chuyển đúng trang tương ứng sau khi gửi",
       env="PRODUCTION",
       note="Gộp 3 lựa chọn vì cùng dạng kết quả (giữ nguyên cài đặt); tách bước 5 để verify tới đầu ra thật. "
            "Nguồn: Backup (job) r199-r201 · Backup 1.0 r112-r114."),

    tc("Copy フォーム作成", "FUNC-DATE-001", "Normal",
       "Copy cài đặt đếm ngược của biểu mẫu",
       CP + "\n- Bot A có biểu mẫu bật đếm ngược với mốc thời gian cụ thể",
       RUN + "3. Mở tab đếm ngược của biểu mẫu ở bot B\n"
             "4. Đối chiếu toàn bộ cài đặt với bot A\n"
             "5. Mở đường dẫn công khai của biểu mẫu bot B",
       "Đếm ngược tới 2026-09-30 23:59",
       "- Cài đặt đếm ngược ở bot B khớp bot A (bật/tắt, mốc thời gian, cách hiển thị)\n"
       "- Bước 5: đồng hồ đếm ngược hiển thị đúng trên trang biểu mẫu",
       note="Nguồn: Backup (job) r202 · Backup 1.0 r115."),

    tc("Copy フォーム作成", "MSG-001", "Normal",
       "Hành động khi GỬI biểu mẫu — thông tin bạn bè MẶC ĐỊNH giữ nguyên mã cố định",
       CP + "\n- Bot A có biểu mẫu với hành động khi gửi là tin văn bản có chèn ĐỦ các thông tin mặc định "
            "ở cột dữ liệu test",
       RUN + "3. Mở hành động khi gửi ở bot B, đọc nội dung tin\n"
             "4. Đối chiếu TỪNG mã chèn với bot A\n"
             "5. Cho bạn bè bot B (đã có đủ giá trị các thông tin đó) trả lời và gửi\n"
             "6. Đọc tin nhận được trên LINE",
       "Tên hệ thống · số điện thoại · email · ngày sinh · 5 mục địa chỉ "
       "(郵便番号 / 都道府県名 / 市区町村名 / 町名番地 / 建物名・部屋番号)",
       "- TẤT CẢ mã chèn của nhóm thông tin mặc định GIỮ NGUYÊN, không bị thay đổi\n"
       "- Bước 6: tin trên LINE hiển thị đúng giá trị của bạn bè BOT B ở cả 9 mục\n"
       "- Không hiển thị mã thô",
       env="PRODUCTION",
       note="Gộp 9 mục vì CÙNG 1 kết quả「dạng này giữ nguyên code cố định」. "
            "Nguồn: Backup 1.0 r117-r121 (bug #32414)."),

    tc("Copy フォーム作成", "DATA-REF-001", "Normal",
       "Hành động khi GỬI biểu mẫu — thông tin bạn bè TỰ TẠO được thay mã sang bot nhận",
       CP + "\n- Bot A có thông tin bạn bè tự tạo ở CẢ 2 folder (folder chưa phân loại và folder tự tạo), "
            "mỗi folder đủ 6 kiểu\n"
            "- Biểu mẫu có hành động khi gửi là tin văn bản chèn đủ 12 mã đó",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận 12 thông tin đã copy\n"
             "4. Mở hành động khi gửi ở bot B, đối chiếu TỪNG mã chèn\n"
             "5. Cho bạn bè bot B (đã có đủ giá trị) trả lời và gửi\n"
             "6. Đọc tin nhận được trên LINE và mở chi tiết bạn bè ở bot B",
       "2 folder × 6 kiểu (mô tả · ảnh · PDF · lựa chọn · điểm · ngày tháng) = 12 mã chèn",
       "- CẢ 12 mã chèn ở bot B đều được thay thành mã của BOT B\n"
       "- KHÔNG còn mã nào của bot A\n"
       "- Bước 6: tin trên LINE hiển thị đúng giá trị của bạn bè bot B; "
       "giá trị được ghi đúng vào chi tiết bạn bè ở bot B",
       env="PRODUCTION",
       note="Gộp 12 điểm vì CÙNG 1 kết quả「replace code friend infor khác với bot gốc」. "
            "Bug #32414 (20/10/2025). Nguồn: Backup 1.0 r122-r133."),

    tc("Copy フォーム作成", "MSG-001", "Normal",
       "Hành động NHẮC LỊCH của biểu mẫu — thông tin bạn bè mặc định và tự tạo",
       CP + "\n- Bot A có biểu mẫu với hành động nhắc lịch chèn cả 9 mã thông tin mặc định "
            "và 12 mã thông tin tự tạo",
       RUN + "3. Mở hành động nhắc lịch của biểu mẫu ở bot B\n"
             "4. Đối chiếu 9 mã mặc định (phải giữ nguyên) và 12 mã tự tạo (phải đổi sang bot B)\n"
             "5. Cho bạn bè bot B trả lời và chờ tới giờ nhắc\n"
             "6. Đọc tin nhắc nhận được trên LINE",
       "9 mã mặc định + 12 mã tự tạo",
       "- 9 mã mặc định GIỮ NGUYÊN\n"
       "- 12 mã tự tạo được THAY sang mã của BOT B\n"
       "- Bước 6: tin nhắc gửi từ bot B, hiển thị đúng giá trị của bạn bè bot B ở cả 21 mục",
       env="PRODUCTION",
       note="Gộp 21 điểm vì cùng nằm trong 1 tin nhắc và cùng bộ quy tắc. "
            "Nguồn: Backup 1.0 r134-r150 (bug #32414). Liên quan MT-16 về id nhắc lịch."),

    tc("Copy フォーム作成", "MSG-001", "Normal",
       "Hành động CHẨN ĐOÁN của biểu mẫu (khoảng điểm 0–5) — mã chèn thông tin bạn bè",
       CP + "\n- Bot A có biểu mẫu chẩn đoán, khoảng điểm 0–5 có hành động gửi tin chèn 9 mã mặc định "
            "và 12 mã tự tạo",
       RUN + "3. Mở cài đặt chẩn đoán của biểu mẫu ở bot B, mở khoảng điểm 0–5\n"
             "4. Đối chiếu 9 mã mặc định và 12 mã tự tạo\n"
             "5. Cho bạn bè bot B trả lời sao cho tổng điểm rơi vào khoảng 0–5 và gửi\n"
             "6. Đọc tin nhận được trên LINE",
       "Tổng điểm = 3 (rơi vào khoảng 0–5)",
       "- 9 mã mặc định giữ nguyên, 12 mã tự tạo đổi sang bot B\n"
       "- Bước 6: nhận đúng tin của khoảng điểm 0–5, hiển thị đúng giá trị bạn bè bot B",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r151-r167 (bug #32414). Tách riêng khỏi khoảng 5–10 vì kết quả khác nhau "
            "(nội dung tin của mỗi khoảng điểm khác nhau)."),

    tc("Copy フォーム作成", "MSG-001", "Normal",
       "Hành động CHẨN ĐOÁN của biểu mẫu (khoảng điểm 5–10) — mã chèn thông tin bạn bè",
       CP + "\n- Bot A có biểu mẫu chẩn đoán, khoảng điểm 5–10 có hành động gửi tin chèn 9 mã mặc định "
            "và 12 mã tự tạo",
       RUN + "3. Mở cài đặt chẩn đoán của biểu mẫu ở bot B, mở khoảng điểm 5–10\n"
             "4. Đối chiếu 9 mã mặc định và 12 mã tự tạo\n"
             "5. Cho bạn bè bot B trả lời sao cho tổng điểm rơi vào khoảng 5–10 và gửi\n"
             "6. Đọc tin nhận được trên LINE",
       "Tổng điểm = 8 (rơi vào khoảng 5–10)",
       "- 9 mã mặc định giữ nguyên, 12 mã tự tạo đổi sang bot B\n"
       "- Bước 6: nhận đúng tin của khoảng điểm 5–10 (khác nội dung khoảng 0–5)",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r168-r184 (bug #32414)."),

    tc("Copy フォーム作成", "FUNC-001", "Normal",
       "Copy biểu mẫu có phân nhánh trang — mã chèn ở cả 3 loại hành động đều đúng",
       CP + "\n- Bot A có biểu mẫu phân nhánh: trang 1 rẽ sang trang 2 hoặc trang 3 theo đáp án\n"
            "- Cả 3 loại hành động (khi gửi, nhắc lịch, chẩn đoán) đều có chèn thông tin bạn bè",
       RUN + "3. Mở biểu mẫu ở bot B, đối chiếu số trang và điều kiện rẽ nhánh\n"
             "4. Kiểm tra mã chèn ở cả 3 loại hành động\n"
             "5. Cho bạn bè bot B đi theo nhánh trang 2, rồi lần khác đi theo nhánh trang 3",
       "3 trang, 2 nhánh rẽ",
       "- Bot B có đủ 3 trang, điều kiện rẽ nhánh khớp bot A\n"
       "- Mã chèn ở cả 3 loại hành động đều đã đổi sang bot B\n"
       "- Bước 5: cả 2 nhánh rẽ đúng trang, hành động của từng nhánh chạy đúng",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r185 —「CHECK FORM RẼ NHÁNH ĐƯỢC BACKUP ĐÚNG: Replace code đúng ở các action: "
            "Submit form OK / Remind OK / Chẩn đoán」."),
]
