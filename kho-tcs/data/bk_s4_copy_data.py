# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 16-21: タグ / 友だち情報 / イベント予約 & リマインド /
コンバージョン・URL・対応ステータス / 友だち追加時設定 / アクションスケジュール.

Quy ước: **bot A = LOA gửi**, **bot B = LOA nhận** (theo spec; xem MT-01).
"""
from _common import tc

CP = ("- Bot A (LOA gửi) và bot B (LOA nhận) đều plan Standard/Pro, job nền đang bật\n"
      "- Bot B là LOA TRỐNG (chưa có dữ liệu cùng loại) để dễ đối chiếu\n"
      "- Đã dựng xong dữ liệu ở bot A theo mục điều kiện riêng bên dưới")
RUN = "1. Ở bot A, xác nhận dữ liệu đã dựng đúng\n2. Thực hiện copy A → B và chờ trạng thái hoàn tất\n"
FI12 = ("2 folder (folder chưa phân loại + folder tự tạo) × 6 kiểu "
        "(mô tả · ảnh · PDF · lựa chọn · điểm · ngày tháng) = 12 mục")
BASIC9 = ("Tên hệ thống · số điện thoại · email · ngày sinh · 5 mục địa chỉ "
          "(郵便番号 / 都道府県名 / 市区町村名 / 町名番地 / 建物名・部屋番号)")

S4 = [
    # ═══════════════ 16. Copy タグ ═══════════════
    tc("Copy タグ", "FUNC-001", "Normal",
       "Copy folder thẻ và danh sách thẻ — đủ số lượng, đúng thứ tự, đúng folder",
       CP + "\n- Bot A có 3 folder thẻ (ngoài mặc định): FD-1 có 5 thẻ, FD-2 có 3 thẻ, FD-3 rỗng\n"
            "- Folder mặc định có 2 thẻ",
       RUN + "3. Mở màn タグ ở bot B\n"
             "4. Đếm số folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số thẻ và đối chiếu tên thẻ",
       "3 folder tự tạo + folder mặc định · tổng 10 thẻ",
       "- Bot B có đủ 3 folder tự tạo, đúng tên và đúng thứ tự\n"
       "- Số thẻ mỗi folder khớp bot A (5 / 3 / 0), folder mặc định có 2 thẻ\n"
       "- Tên từng thẻ khớp bot A, thứ tự trong folder giữ nguyên",
       note="Nguồn: Backup 1.0 r187, r189 · Backup (job) r203, r205."),

    tc("Copy タグ", "FUNC-MULTI-001", "Normal",
       "Copy cài đặt gắn thẻ 1 lần / nhiều lần",
       CP + "\n- Bot A có 1 thẻ đặt gắn 1 lần và 1 thẻ đặt gắn nhiều lần",
       RUN + "3. Mở chi tiết cả 2 thẻ ở bot B\n4. Đối chiếu cài đặt số lần gắn",
       "1 thẻ 1 lần + 1 thẻ nhiều lần",
       "- Bot B giữ đúng cài đặt của cả 2 thẻ\n"
       "- Không bị đảo giá trị",
       note="Nguồn: Backup 1.0 r188 · Backup (job) r204."),

    tc("Copy タグ", "DATA-ID-001", "Normal",
       "Copy hành động gắn kèm của thẻ — trỏ đúng dữ liệu bot nhận",
       CP + "\n- Bot A có thẻ「タグ-ACT」cài hành động khi được gắn: gửi tin + bắt đầu kịch bản",
       RUN + "3. Mở chi tiết thẻ đó ở bot B, mở phần hành động\n"
             "4. Đối chiếu số hành động con và kịch bản được trỏ tới\n"
             "5. Gắn thẻ cho 1 bạn bè của bot B và quan sát trên LINE",
       "1 thẻ có 2 hành động con",
       "- Hành động đủ 2 mục ở bot B\n"
       "- Hành động bắt đầu kịch bản trỏ tới kịch bản của BOT B\n"
       "- Bước 5: bạn bè nhận tin và vào kịch bản của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r190 · Backup (job) r206. RULE-06 verify tới tin trên LINE."),

    tc("Copy タグ", "DATA-001", "Abnormal",
       "Thẻ đã xoá ở bot gửi KHÔNG được copy sang",
       CP + "\n- Bot A có 3 thẻ đang dùng và 2 thẻ đã xoá",
       RUN + "3. Mở màn タグ ở bot B, đếm số thẻ\n"
             "4. Mở màn thẻ đã xoá ở bot B\n"
             "5. Đối chiếu với bot A",
       "3 thẻ đang dùng + 2 thẻ đã xoá tên「タグ-DEL1」「タグ-DEL2」",
       "- Bot B chỉ có 3 thẻ đang dùng\n"
       "- Màn thẻ đã xoá của bot B KHÔNG có「タグ-DEL1」và「タグ-DEL2」\n"
       "- Tổng số thẻ ở bot B đúng bằng 3",
       note="Nguồn: Backup (job) r207 —「Không backup các tag đã xóa mềm (deleted_at IS NOT NULL)」."),

    tc("Copy タグ", "DATA-COUNT-001", "Normal",
       "Bộ đếm số người gắn thẻ ở bot nhận bắt đầu từ 0",
       CP + "\n- Bot A có thẻ「タグ-CNT」đang gắn cho 25 bạn bè",
       RUN + "3. Mở màn タグ ở bot B, xem cột số người gắn của thẻ「タグ-CNT」\n"
             "4. Gắn thẻ đó cho 2 bạn bè của bot B\n"
             "5. Xem lại cột số người gắn",
       "Bot A: 25 người gắn thẻ",
       "- Bước 3: số người gắn ở bot B là 0 (bạn bè không được copy)\n"
       "- Bước 5: số người gắn ở bot B là 2\n"
       "- Số người gắn ở bot A vẫn là 25, không bị đụng",
       note="Suy luận của AI theo DATA-COUNT-001 — corpus KHÔNG có TC cho bộ đếm sau copy. "
            "Cần Leader xác nhận (bạn bè không nằm trong 13 loại được copy)."),

    tc("Copy タグ", "SEC-ISO-001", "Normal",
       "Sửa thẻ ở bot nhận KHÔNG ảnh hưởng thẻ ở bot gửi",
       CP + "\n- Đã copy thẻ「タグ-X」từ A sang B",
       "1. Ở bot B, đổi tên thẻ「タグ-X」thành「タグ-X-改」và đổi màu\n"
       "2. Ở bot B, xoá 1 thẻ khác đã copy\n"
       "3. Quay lại bot A, mở màn タグ\n"
       "4. Đối chiếu tên, màu và số lượng thẻ",
       "1 thẻ đổi tên + 1 thẻ xoá",
       "- Thẻ ở bot A vẫn tên「タグ-X」, màu cũ\n"
       "- Thẻ bị xoá ở bot B vẫn còn nguyên ở bot A\n"
       "- Hai bên hoàn toàn độc lập sau khi copy",
       note="Suy luận của AI theo SEC-ISO-001 — corpus không có TC kiểm tra tính độc lập sau copy cho tag. "
            "Cần Leader xác nhận."),

    # ═══════════════ 17. Copy 友だち情報 ═══════════════
    tc("Copy 友だち情報", "FUNC-001", "Abnormal",
       "Phạm vi copy thông tin bạn bè — copy TẤT CẢ hay chỉ mục ĐANG ĐƯỢC DÙNG?",
       CP + "\n- Bot A có 6 thông tin bạn bè tự tạo:\n"
            "  · 2 mục ĐANG được dùng trong biểu mẫu\n"
            "  · 2 mục ĐANG được dùng trong hành động\n"
            "  · 2 mục KHÔNG được dùng ở đâu cả",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Đếm số thông tin tự tạo và đối chiếu tên với 6 mục ở bot A\n"
             "5. Ghi rõ 2 mục không được dùng có sang bot B không",
       "6 mục: 2 dùng ở biểu mẫu · 2 dùng ở hành động · 2 không dùng",
       "- Kết quả theo quyết định MT-18:\n"
       "  · nếu chốt copy TẤT CẢ: bot B có đủ 6 mục\n"
       "  · nếu chốt chỉ copy mục đang dùng: bot B chỉ có 4 mục, 2 mục không dùng bị bỏ\n"
       "- Ghi rõ số lượng thực tế quan sát được",
       spec="Đã hỏi leader",
       note="MT-18 — Backup 1.0 r191 ghi「Chỉ back up các friend infor có setting ở form và trong action」; "
            "feature-spec §1.3 + §7.5 nói copy cả bảng `friend_information_setting`. Đây là TC quyết định phạm vi."),

    tc("Copy 友だち情報", "FUNC-001", "Normal",
       "Thông tin bạn bè MẶC ĐỊNH không được copy — bot nhận vốn đã có sẵn",
       CP + "\n- Bot A và bot B đều là LOA bình thường",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Kiểm tra sự tồn tại của 9 mục mặc định ở cột dữ liệu test\n"
             "5. Đếm xem có mục mặc định nào bị nhân đôi không",
       BASIC9,
       "- Bot B có đủ 9 mục mặc định (vốn có sẵn từ khi tạo LOA)\n"
       "- KHÔNG có mục mặc định nào bị NHÂN ĐÔI sau khi copy\n"
       "- Mỗi mục chỉ xuất hiện đúng 1 lần",
       note="Gộp 9 mục vì CÙNG 1 kết quả「dạng cơ bản sẽ ko backup, mặc định bot nào cũng sẽ có」. "
            "Nguồn: Backup 1.0 r193-r201."),

    tc("Copy 友だち情報", "FUNC-001", "Abnormal",
       "Folder thông tin bạn bè có bị NHÂN ĐÔI sau khi copy không?",
       CP + "\n- Bot A có 2 folder thông tin bạn bè tự tạo, mỗi folder 3 mục",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. ĐẾM số folder và đọc tên từng folder\n"
             "5. Kiểm tra có folder nào trùng tên nhau không\n"
             "6. Đếm số mục trong từng folder",
       "2 folder tự tạo × 3 mục",
       "- Bot B có ĐÚNG 2 folder tự tạo, không nhiều hơn\n"
       "- KHÔNG có folder nào bị nhân đôi (trùng tên)\n"
       "- Mỗi folder có đúng 3 mục\n"
       "- ⚠️ Nếu có folder nhân đôi thì raise bug",
       spec="Đã hỏi leader",
       note="MT-18 — Backup 1.0 r191 (Note):「đang bị DUPLICATE FOLDER」. Backup (job) không ghi chú. "
            "⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy 友だち情報", "FUNC-001", "Normal",
       "Copy thông tin bạn bè kiểu mô tả, ảnh và PDF",
       CP + "\n- Bot A có 6 mục ở 2 folder: mỗi folder 1 mục mô tả, 1 mục ảnh, 1 mục PDF\n"
            "- Cả 6 mục đều KHÔNG có hành động gắn kèm",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Đối chiếu 6 mục: tên, kiểu, folder\n"
             "5. Mở cài đặt hành động của từng mục",
       "2 folder × 3 kiểu (mô tả · ảnh · PDF)",
       "- Bot B có đủ 6 mục, đúng kiểu, đúng folder, đúng tên\n"
       "- Cả 6 mục đều KHÔNG có hành động gắn kèm (giống bot A)\n"
       "- Popup cài đặt hành động mở được, không lỗi",
       note="Gộp 6 điểm vì CÙNG 1 kết quả. Nguồn: Backup 1.0 r202-r204, r211-r213 · Backup (job) r224-r226, r233-r235 "
            "—「setting_value sẽ ko có action_id」."),

    tc("Copy 友だち情報", "DATA-REF-001", "Normal",
       "Copy thông tin kiểu lựa chọn / điểm / ngày tháng — KHÔNG có hành động gắn thẻ",
       CP + "\n- Bot A có 6 mục ở 2 folder: mỗi folder 1 mục lựa chọn, 1 mục điểm, 1 mục ngày tháng\n"
            "- Cả 6 mục đều có hành động NHƯNG không phải hành động gắn thẻ",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Mở popup cài đặt hành động của từng mục trong 6 mục\n"
             "5. Kiểm tra hành động có hiển thị đúng không\n"
             "6. Kích hoạt điều kiện của 1 mục điểm và quan sát hành động chạy",
       "2 folder × 3 kiểu (lựa chọn · điểm · ngày tháng)",
       "- Cả 6 mục có hành động ở bot B, popup hiển thị đúng hành động\n"
       "- Hành động trỏ tới dữ liệu của BOT B\n"
       "- Bước 6: hành động chạy đúng trên bạn bè của bot B",
       note="Gộp 6 điểm vì CÙNG 1 kết quả「backup ⇒ hiển thị action id của bot mới dạng số」. "
            "Nguồn: Backup 1.0 r205, r207, r209, r214, r216, r218 · Backup (job) r227, r229, r231, r236, r238, r240."),

    tc("Copy 友だち情報", "DATA-REF-001", "Abnormal",
       "Copy thông tin kiểu lựa chọn / ngày tháng CÓ hành động gắn thẻ (bug #32413)",
       CP + "\n- Bot A có 4 mục ở 2 folder: mỗi folder 1 mục lựa chọn và 1 mục ngày tháng\n"
            "- Cả 4 mục đều có hành động GẮN THẺ",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Mở popup cài đặt hành động của từng mục — kiểm tra popup CÓ HIỂN THỊ hành động không\n"
             "5. Kiểm tra thẻ được trỏ tới là thẻ của bot nào\n"
             "6. Kích hoạt điều kiện và kiểm tra thẻ có được gắn cho bạn bè bot B không",
       "2 folder × 2 kiểu (lựa chọn · ngày tháng), đều có hành động gắn thẻ",
       "- Popup cài đặt hành động ở bot B HIỂN THỊ ĐƯỢC hành động — không để trống\n"
       "- Hành động trỏ tới thẻ của BOT B\n"
       "- Bước 6: thẻ được gắn đúng cho bạn bè bot B\n"
       "- ⚠️ Nếu popup trống thì đây là bug #32413 tái phát — raise bug",
       note="Bug #32413 (20/10/2025):「Sau khi backup dữ liệu, action khi đạt điểm không chạy — "
            "setting_value có action_id dạng text nhưng backup không xử lý được」. "
            "Gộp 4 điểm vì cùng 1 kết quả. Nguồn: Backup 1.0 r206, r210, r215, r219 · Backup (job) r228, r232, r237, r241."),

    tc("Copy 友だち情報", "DATA-REF-001", "Abnormal",
       "Copy thông tin kiểu ĐIỂM có hành động cộng điểm — đúng tình huống khách hàng gặp (bug #32413)",
       CP + "\n- Bot A có 2 mục kiểu điểm (1 ở mỗi folder)\n"
            "- Mỗi mục có hành động cộng điểm được SỬA LẠI từ một hành động khác trước đó",
       RUN + "3. Mở màn 友だち情報 ở bot B\n"
             "4. Mở popup cài đặt hành động của 2 mục điểm — kiểm tra popup có hiển thị hành động không\n"
             "5. Cho bạn bè bot B đạt ngưỡng điểm (qua biểu mẫu hoặc hành động)\n"
             "6. Kiểm tra hành động khi đạt điểm CÓ CHẠY không",
       "2 mục điểm, hành động cộng điểm được sửa lại từ hành động khác, ngưỡng = 10 điểm",
       "- Popup cài đặt hành động HIỂN THỊ ĐƯỢC ở bot B\n"
       "- Bước 6: hành động khi đạt điểm CHẠY đúng trên bạn bè bot B\n"
       "- ⚠️ Nếu hành động không chạy thì bug #32413 chưa được fix triệt để — raise bug",
       env="PRODUCTION",
       note="Bug #32413 —「CASE CỦA KH: có action cộng point (edit lại từ action khác trước đó)」. "
            "Đây là tình huống KHÁCH HÀNG THẬT gặp. Nguồn: Backup 1.0 r208, r217 · Backup (job) r230, r239."),

    tc("Copy 友だち情報", "FUNC-DATE-001", "Abnormal",
       "Thông tin kiểu ngày tháng có đặt giờ chạy hành động — cài đặt giờ có bị mất không?",
       CP + "\n- Bot A có 1 mục thông tin kiểu ngày tháng, có đặt hành động chạy vào một giờ cụ thể",
       RUN + "3. Mở màn 友だち情報 ở bot B, mở chi tiết mục ngày tháng đó\n"
             "4. Kiểm tra phần cài đặt GIỜ chạy hành động\n"
             "5. Đối chiếu với bot A\n"
             "6. Đặt giá trị ngày cho 1 bạn bè bot B và chờ tới giờ đó",
       "Hành động chạy trước 3 ngày, vào lúc 10:00",
       "- Cài đặt giờ chạy ở bot B khớp bot A (trước 3 ngày, 10:00)\n"
       "- Bước 6: hành động chạy đúng giờ ở bot B\n"
       "- ⚠️ Nếu phần cài đặt giờ bị trống thì raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-18 — Backup 1.0 r191 (Note):「Friend infor type date bị MẤT setting time action」. "
            "PRODUCTION theo RULE-08 (phụ thuộc job chạy theo ngày). ⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy 友だち情報", "FUNC-001", "Normal",
       "Copy danh sách giá trị của thông tin kiểu lựa chọn",
       CP + "\n- Bot A có 1 mục kiểu lựa chọn với 5 giá trị, trong đó có giá trị tiếng Nhật và emoji",
       RUN + "3. Mở chi tiết mục lựa chọn đó ở bot B\n"
             "4. Đếm số giá trị và đối chiếu từng giá trị + thứ tự\n"
             "5. Ghi giá trị cho 1 bạn bè bot B từ màn quản lý",
       "5 giá trị:「A」「B」「未回答」「その他🎁」「N/A」",
       "- Bot B có đủ 5 giá trị, đúng nội dung và đúng thứ tự\n"
       "- Giữ nguyên tiếng Nhật và emoji\n"
       "- Bước 5: chọn và lưu được giá trị bình thường",
       note="Suy luận của AI mở rộng từ Backup (job) r209「select」— corpus không tách riêng TC cho "
            "danh sách giá trị của mục lựa chọn. Cần Leader xác nhận."),

    tc("Copy 友だち情報", "DATA-001", "Normal",
       "GIÁ TRỊ thông tin bạn bè KHÔNG được copy — chỉ copy phần cài đặt",
       CP + "\n- Bot A có mục「info-point-A」với 30 bạn bè đã có giá trị điểm",
       RUN + "3. Mở màn 友だち情報 ở bot B, mở danh sách câu trả lời của mục đó\n"
             "4. Đếm số bạn bè có giá trị\n"
             "5. Xem cột số người đã trả lời",
       "Bot A: 30 bạn bè có giá trị",
       "- Bot B: mục thông tin CÓ tồn tại (phần cài đặt được copy)\n"
       "- Danh sách câu trả lời ở bot B TRỐNG — 0 bạn bè có giá trị\n"
       "- Số người đã trả lời = 0\n"
       "- Dữ liệu bạn bè ở bot A không bị đụng",
       note="Suy luận của AI — bạn bè không nằm trong 13 loại được copy nên giá trị cũng không sang. "
            "Corpus không có TC này. Cần Leader xác nhận."),

    tc("Copy 友だち情報", "SEC-ISO-001", "Normal",
       "Sửa thông tin bạn bè ở bot nhận KHÔNG ảnh hưởng bot gửi",
       CP + "\n- Đã copy thông tin bạn bè từ A sang B",
       "1. Ở bot B, đổi tên 1 mục thông tin và thêm 1 giá trị lựa chọn mới\n"
       "2. Ở bot B, xoá 1 mục thông tin khác\n"
       "3. Quay lại bot A, mở màn 友だち情報\n"
       "4. Đối chiếu tên, danh sách giá trị và số lượng mục",
       "1 mục sửa + 1 mục xoá",
       "- Ở bot A: tên mục không đổi, danh sách giá trị không có mục mới\n"
       "- Mục bị xoá ở bot B vẫn còn ở bot A\n"
       "- Hai bên độc lập hoàn toàn",
       note="Suy luận của AI theo SEC-ISO-001 — corpus không có TC. Cần Leader xác nhận."),

    # ═══════════════ 18. Copy イベント予約 & リマインド ═══════════════
    tc("Copy イベント予約 & リマインド", "FUNC-001", "Abnormal",
       "Copy folder sự kiện — kiểm tra có bị nhân đôi folder không",
       CP + "\n- Bot A có 2 folder sự kiện KHÁC folder mặc định, mỗi folder 2 sự kiện",
       RUN + "3. Mở màn イベント予約 ở bot B\n"
             "4. ĐẾM số folder và đọc tên từng cái\n"
             "5. Kiểm tra có folder nào trùng tên không\n"
             "6. Mở từng folder đếm số sự kiện",
       "2 folder tự tạo × 2 sự kiện",
       "- Bot B có ĐÚNG 2 folder tự tạo, không nhiều hơn\n"
       "- KHÔNG có folder nào bị nhân đôi\n"
       "- Mỗi folder có đúng 2 sự kiện, nằm đúng folder\n"
       "- ⚠️ Nếu có folder nhân đôi thì raise bug",
       spec="Đã hỏi leader",
       note="MT-20 — Backup 1.0 r221 (Note):「setting 2 folder khác folder default thì có 1 folder bị duplicate?」 "
            "— nguyên văn có dấu hỏi, chưa ai xác nhận."),

    tc("Copy イベント予約 & リマインド", "FUNC-001", "Normal",
       "Copy danh sách sự kiện và đường dẫn sự kiện",
       CP + "\n- Bot A có 3 sự kiện, đã ghi lại đường dẫn công khai của từng cái",
       RUN + "3. Mở màn イベント予約 ở bot B, đếm và đối chiếu tên 3 sự kiện\n"
             "4. Ghi lại đường dẫn công khai của 3 sự kiện ở bot B\n"
             "5. So sánh với đường dẫn ở bot A\n"
             "6. Mở đường dẫn của bot B trên trình duyệt ẩn danh",
       "3 sự kiện",
       "- Bot B có đủ 3 sự kiện, đúng tên\n"
       "- Đường dẫn ở bot B KHÁC đường dẫn bot A (mã mới)\n"
       "- Bước 6: mở ra trang đặt lịch của bot B, đặt chỗ được và ghi nhận ở bot B",
       note="Nguồn: Backup 1.0 r222-r223 · Backup (job) r244-r245."),

    tc("Copy イベント予約 & リマインド", "FUNC-001", "Normal",
       "Copy cài đặt chung của sự kiện: tên, loại sự kiện, ảnh, địa chỉ, đường dẫn, số lượt đặt",
       CP + "\n- Bot A có 2 sự kiện: 1 loại 1 ngày và 1 loại nhiều ngày, cả 2 đều có ảnh, "
            "địa chỉ, đường dẫn tham khảo và giới hạn số lượt đặt",
       RUN + "3. Mở cài đặt chung của cả 2 sự kiện ở bot B\n"
             "4. Đối chiếu từng mục với bot A\n"
             "5. Mở trang đặt lịch công khai của bot B",
       "2 sự kiện · ảnh JPG · địa chỉ「東京都渋谷区...」· giới hạn 3 lượt/người",
       "- Cả 2 sự kiện giữ đúng loại (1 ngày / nhiều ngày)\n"
       "- Ảnh hiển thị được, đường dẫn ảnh khác bot A\n"
       "- Địa chỉ, đường dẫn, giới hạn số lượt đặt khớp bot A\n"
       "- Bước 5: trang đặt lịch hiển thị đủ các thông tin trên",
       env="PRODUCTION",
       note="Gộp 5 mục vì cùng 1 kết quả (giữ nguyên cài đặt). "
            "Nguồn: Backup 1.0 r224-r228 · Backup (job) r246-r250. PRODUCTION vì có ảnh (RULE-08)."),

    tc("Copy イベント予約 & リマインド", "FUNC-DATE-001", "Normal",
       "Copy khung giờ của sự kiện: ngày giờ, hạn đặt, số chỗ tối đa",
       CP + "\n- Bot A có sự kiện với 3 khung giờ, mỗi khung có ngày giờ, hạn đặt và số chỗ khác nhau",
       RUN + "3. Mở chi tiết sự kiện ở bot B, xem danh sách khung giờ\n"
             "4. Đếm số khung và đối chiếu ngày giờ / hạn đặt / số chỗ từng khung\n"
             "5. Mở trang đặt lịch công khai của bot B",
       "3 khung: 2026-09-10 10:00 (hạn 09-09, 5 chỗ) · 09-10 14:00 (hạn 09-09, 10 chỗ) · "
       "09-11 10:00 (hạn 09-10, 3 chỗ)",
       "- Bot B có đủ 3 khung giờ, đúng ngày giờ\n"
       "- Hạn đặt và số chỗ tối đa khớp chính xác từng khung\n"
       "- Bước 5: trang đặt lịch hiển thị đủ 3 khung với đúng số chỗ còn trống",
       note="Gộp 3 mục cài đặt vì cùng 1 kết quả. Nguồn: Backup 1.0 r229-r231 · Backup (job) r251-r253."),

    tc("Copy イベント予約 & リマインド", "FUNC-001", "Normal",
       "Copy cài đặt duyệt, đổi lịch, địa chỉ và hiển thị của khung giờ",
       CP + "\n- Bot A có sự kiện với 2 khung giờ: 1 khung bật duyệt + cho đổi lịch, "
            "1 khung tắt duyệt + không cho đổi; mỗi khung có địa chỉ và đường dẫn riêng\n"
            "- 1 khung đặt ẩn, 1 khung đặt hiện",
       RUN + "3. Mở chi tiết 2 khung giờ ở bot B\n"
             "4. Đối chiếu từng cài đặt với bot A\n"
             "5. Mở trang đặt lịch công khai và kiểm tra khung ẩn có hiện không",
       "2 khung × (duyệt · đổi lịch · địa chỉ · đường dẫn · ẩn/hiện)",
       "- Cả 5 nhóm cài đặt của 2 khung đều khớp bot A\n"
       "- Bước 5: khung đặt ẩn KHÔNG hiển thị trên trang công khai, khung đặt hiện thì có",
       note="Gộp 5 cài đặt vì cùng 1 kết quả. Nguồn: Backup 1.0 r232-r235 · Backup (job) r254-r257."),

    tc("Copy イベント予約 & リマインド", "DATA-COUNT-001", "Normal",
       "Số lượt đã đặt của khung giờ ở bot nhận bắt đầu từ 0",
       CP + "\n- Bot A có sự kiện với khung giờ 10 chỗ, đã có 7 lượt đặt",
       RUN + "3. Mở chi tiết khung giờ đó ở bot B\n"
             "4. Xem số lượt đã đặt và số chỗ còn trống\n"
             "5. Mở danh sách người đã đặt",
       "Bot A: 10 chỗ, 7 lượt đã đặt",
       "- Bot B: số chỗ tối đa vẫn là 10 (cài đặt được copy)\n"
       "- Số lượt đã đặt = 0, còn trống 10 chỗ\n"
       "- Danh sách người đã đặt TRỐNG (bạn bè không được copy)\n"
       "- Số liệu ở bot A không đổi",
       note="Nguồn: Backup 1.0 r236 · Backup (job) r258 —「số lượng book」. "
            "Kết quả「bắt đầu từ 0」do AI viết vì corpus không ghi expect. Cần Leader xác nhận."),

    tc("Copy イベント予約 & リマインド", "DATA-REF-001", "Abnormal",
       "Nhắc lịch gắn với khung giờ sự kiện — kiểm tra có còn trỏ bot gửi không",
       CP + "\n- Bot A có sự kiện với khung giờ gắn nhắc lịch「リマインド-EV」",
       RUN + "3. Mở màn リマインド配信 ở bot B, ghi lại nhắc lịch đã copy\n"
             "4. Mở chi tiết khung giờ ở bot B, xem nhắc lịch được gắn\n"
             "5. Đặt chỗ bằng 1 bạn bè của bot B và chờ tới giờ nhắc",
       "1 nhắc lịch gắn khung giờ",
       "- Khung giờ ở bot B gắn nhắc lịch của BOT B\n"
       "- Bước 5: bạn bè nhận tin nhắc từ bot B\n"
       "- ⚠️ Nếu trỏ nhắc lịch bot A hoặc để trống thì raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-16 — Backup 1.0 r237 (Note):「đang bị lấy id remind của bot gốc」. "
            "Backup (job) r259 không ghi chú. ⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy イベント予約 & リマインド", "DATA-ID-001", "Normal",
       "Copy hành động gắn với khung giờ sự kiện",
       CP + "\n- Bot A có khung giờ gắn hành động: gửi tin + gắn thẻ khi đặt chỗ thành công",
       RUN + "3. Mở chi tiết khung giờ ở bot B, mở phần hành động\n"
             "4. Đối chiếu hành động và thẻ được trỏ tới\n"
             "5. Đặt chỗ bằng bạn bè bot B và kiểm tra tin + thẻ",
       "2 hành động con",
       "- Hành động đủ ở bot B, thẻ trỏ tới thẻ của BOT B\n"
       "- Bước 5: bạn bè nhận tin và được gắn thẻ ở bot B",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r238 · Backup (job) r260."),

    tc("Copy イベント予約 & リマインド", "PAY-AMOUNT-001", "Normal",
       "Copy gói giá của sự kiện: tên, số lượng tối đa, số tiền, hành động",
       CP + "\n- Bot A có sự kiện với 3 gói giá khác nhau về tên, số lượng và số tiền\n"
            "- Mỗi gói có hành động riêng",
       RUN + "3. Mở phần gói giá của sự kiện ở bot B\n"
             "4. Đếm số gói và đối chiếu tên / số lượng tối đa / SỐ TIỀN từng gói\n"
             "5. Kiểm tra hành động của từng gói\n"
             "6. Mở trang đặt lịch công khai xem giá hiển thị",
       "3 gói: 一般 5000円 (20 chỗ) · 学生 3000円 (10 chỗ) · VIP 15000円 (5 chỗ)",
       "- Bot B có đủ 3 gói, đúng tên\n"
       "- SỐ TIỀN từng gói khớp CHÍNH XÁC bot A — không sai lệch dù 1 đồng\n"
       "- Số lượng tối đa khớp\n"
       "- Hành động từng gói trỏ dữ liệu bot B\n"
       "- Bước 6: giá hiển thị đúng trên trang công khai",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r239-r242 · Backup (job) r261-r264. "
            "PRODUCTION theo RULE-08 (liên quan tiền). Số tiền sai = rủi ro cao nhất của nhóm này."),

    tc("Copy イベント予約 & リマインド", "DATA-REF-001", "Abnormal",
       "Thông tin bạn bè gắn với sự kiện — có liên kết được với thông tin mặc định không?",
       CP + "\n- Bot A có sự kiện thu thập thông tin bạn bè, gồm cả mục MẶC ĐỊNH (tên, email, số điện thoại) "
            "và mục tự tạo",
       RUN + "3. Mở phần thu thập thông tin của sự kiện ở bot B\n"
             "4. Kiểm tra các mục MẶC ĐỊNH có liên kết đúng không\n"
             "5. Kiểm tra các mục tự tạo có trỏ tới thông tin của bot B không\n"
             "6. Đặt chỗ bằng bạn bè bot B, điền đủ thông tin rồi mở chi tiết bạn bè",
       "3 mục mặc định + 2 mục tự tạo",
       "- Các mục tự tạo trỏ tới thông tin bạn bè của BOT B\n"
       "- Các mục MẶC ĐỊNH liên kết được bình thường\n"
       "- Bước 6: giá trị điền vào được ghi đúng vào chi tiết bạn bè bot B\n"
       "- ⚠️ Nếu mục mặc định không liên kết được thì raise bug",
       spec="Đã hỏi leader",
       note="MT-20 — Backup 1.0 r243 (Note):「không liên kết được với friend infor basic」. "
            "Backup (job) r265 không ghi chú. ⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy イベント予約 & リマインド", "UI-FIELD-001", "Normal",
       "Copy quy chế / điều khoản của sự kiện",
       CP + "\n- Bot A có sự kiện có nội dung quy chế dài (>500 ký tự, có xuống dòng)",
       RUN + "3. Mở phần quy chế của sự kiện ở bot B\n"
             "4. Đối chiếu nội dung với bot A\n"
             "5. Mở trang đặt lịch công khai xem quy chế hiển thị",
       "Quy chế >500 ký tự, có xuống dòng và đường dẫn",
       "- Nội dung quy chế ở bot B giống hệt bot A, không bị cắt\n"
       "- Giữ nguyên xuống dòng\n"
       "- Bước 5: hiển thị đủ trên trang công khai",
       note="Nguồn: Backup 1.0 r244 · Backup (job) r266."),

    tc("Copy イベント予約 & リマインド", "FUNC-001", "Abnormal",
       "Copy folder nhắc lịch — có được copy không?",
       CP + "\n- Bot A có 2 folder nhắc lịch tự tạo, mỗi folder 2 nhắc lịch",
       RUN + "3. Mở màn リマインド配信 ở bot B\n"
             "4. ĐẾM số folder và đọc tên\n"
             "5. Kiểm tra 4 nhắc lịch nằm ở folder nào",
       "2 folder × 2 nhắc lịch",
       "- Kết quả theo quyết định MT-19:\n"
       "  · nếu chốt CÓ copy folder: bot B có đủ 2 folder, nhắc lịch nằm đúng folder\n"
       "  · nếu chốt KHÔNG copy: cả 4 nhắc lịch rơi vào folder mặc định\n"
       "- Ghi rõ hiện trạng quan sát được",
       spec="Đã hỏi leader",
       note="MT-19 — Backup 1.0 r245 (Note):「9. Remind > folder — CHƯA BACK UP FOLDER」. "
            "Backup (job) r267 không ghi chú."),

    tc("Copy イベント予約 & リマインド", "FUNC-001", "Normal",
       "Copy danh sách nhắc lịch",
       CP + "\n- Bot A có 4 nhắc lịch với tên khác nhau",
       RUN + "3. Mở màn リマインド配信 ở bot B\n4. Đếm và đối chiếu tên 4 nhắc lịch",
       "4 nhắc lịch",
       "- Bot B có đủ 4 nhắc lịch, đúng tên, đúng thứ tự",
       note="Nguồn: Backup 1.0 r246 · Backup (job) r268."),

    tc("Copy イベント予約 & リマインド", "FUNC-DATE-001", "Normal",
       "Copy 3 kiểu bước của nhắc lịch",
       CP + "\n- Bot A có nhắc lịch với 3 bước: gửi ngay, gửi trước N ngày lúc HH:mm, "
            "gửi trước N giờ M phút so với giờ sự kiện",
       RUN + "3. Mở nhắc lịch đó ở bot B\n"
             "4. Đếm số bước và đối chiếu kiểu + tham số thời gian từng bước\n"
             "5. Cho bạn bè bot B đặt chỗ và chờ nhận đủ 3 tin nhắc",
       "① gửi ngay ② trước 3 ngày lúc 10:00 ③ trước 2 giờ 30 phút",
       "- Bot B có đủ 3 bước, đúng kiểu và đúng tham số thời gian\n"
       "- Bước 5: nhận đủ 3 tin nhắc đúng thời điểm",
       env="PRODUCTION",
       note="Gộp 3 kiểu vì cùng 1 kết quả (giữ nguyên cài đặt). "
            "Nguồn: Backup 1.0 r247-r249 · Backup (job) r269-r271. PRODUCTION theo RULE-08 (job nhắc)."),

    tc("Copy イベント予約 & リマインド", "DATA-REF-001", "Abnormal",
       "Bộ lọc của nhắc lịch — có được copy không?",
       CP + "\n- Bot A có nhắc lịch với bước gắn bộ lọc theo thẻ",
       RUN + "3. Mở bước đó ở bot B, xem phần bộ lọc\n"
             "4. Nếu có: đối chiếu điều kiện và thẻ được trỏ tới",
       "1 bộ lọc theo thẻ",
       "- Ghi rõ hiện trạng: bộ lọc CÓ hay KHÔNG được copy\n"
       "- Nếu có: điều kiện trỏ tới thẻ của BOT B",
       spec="Đã hỏi leader",
       note="⚠️ Backup 1.0 r250 ghi「không support」; Backup (job) r272 để TRỐNG ô kết quả. "
            "Nhưng nhánh kịch bản và richmenu (bản mới) lại nói bộ lọc CÓ được copy. Xem MT-13."),

    tc("Copy イベント予約 & リマインド", "MSG-001", "Abnormal",
       "Tin nhắn soạn trực tiếp trong bước nhắc lịch — có được copy không?",
       CP + "\n- Bot A có nhắc lịch với bước chứa tin văn bản soạn trực tiếp tại màn nhắc lịch",
       RUN + "3. Mở bước đó ở bot B, đọc nội dung tin\n"
             "4. Đối chiếu với bot A\n"
             "5. Cho bạn bè bot B đặt chỗ và chờ nhận tin nhắc",
       "Nội dung:「明日のご予約のリマインドです」",
       "- Nội dung tin ở bot B PHẢI giống bot A, không được rỗng\n"
       "- Bước 5: nhận đúng nội dung đó trên LINE\n"
       "- ⚠️ Nếu bước không có nội dung tin thì raise bug",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-19 — Backup 1.0 r251 (Note):「KHÔNG BACK UP ĐƯỢC MSG」. Backup (job) r273 không ghi chú. "
            "⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy イベント予約 & リマインド", "DATA-REF-001", "Normal",
       "Bước nhắc lịch dùng mẫu tin từ thư viện và bước sao chép từ mẫu tin",
       CP + "\n- Bot A có nhắc lịch với 1 bước dùng mẫu tin từ thư viện và 1 bước sao chép nội dung mẫu tin",
       RUN + "3. Mở 2 bước đó ở bot B\n"
             "4. Kiểm tra bước dùng thư viện trỏ tới mẫu tin nào\n"
             "5. Sửa mẫu tin gốc ở bot B, xem bước nào đổi theo",
       "1 bước dùng chung + 1 bước sao chép",
       "- Bước dùng thư viện trỏ tới mẫu tin của BOT B\n"
       "- Bước sao chép giữ nội dung riêng\n"
       "- Bước 5: chỉ bước dùng thư viện đổi theo mẫu tin",
       note="Nguồn: Backup 1.0 r252-r253 · Backup (job) r274-r275."),

    tc("Copy イベント予約 & リマインド", "DATA-COUNT-001", "Normal",
       "Danh sách người đã đặt chỗ KHÔNG được copy sang bot nhận",
       CP + "\n- Bot A có sự kiện với 15 lượt đặt chỗ của bạn bè thật",
       RUN + "3. Mở chi tiết sự kiện ở bot B, mở danh sách người đã đặt\n"
             "4. Đếm số bản ghi\n"
             "5. Kiểm tra ở bot A xem 15 lượt đặt còn nguyên không",
       "Bot A: 15 lượt đặt",
       "- Danh sách người đã đặt ở bot B TRỐNG\n"
       "- KHÔNG có thông tin bạn bè của bot A lọt sang bot B\n"
       "- Bot A vẫn giữ nguyên 15 lượt đặt",
       note="Suy luận của AI theo SEC-ISO-001 — corpus không có TC. "
            "Đây là điểm rủi ro rò rỉ dữ liệu cá nhân giữa 2 LOA. Cần Leader xác nhận."),

    # ═══════════════ 19. Copy コンバージョン・URL・対応ステータス ═══════════════
    tc("Copy コンバージョン・URL・対応ステータス", "DATA-REF-001", "Abnormal",
       "Phạm vi copy trang chuyển đổi — tất cả hay chỉ trang đang được dùng trong hành động?",
       CP + "\n- Bot A có 4 trang chuyển đổi: 2 đang được dùng trong hành động mở liên kết, "
            "2 không được dùng ở đâu",
       RUN + "3. Mở màn コンバージョン ở bot B\n"
             "4. Đếm số trang chuyển đổi và đối chiếu tên\n"
             "5. Ghi rõ 2 trang không được dùng có sang bot B không",
       "4 trang: 2 đang dùng · 2 không dùng",
       "- Ghi rõ hiện trạng: bot B có 4 hay chỉ 2 trang chuyển đổi\n"
       "- Nếu chỉ 2: xác nhận đúng là 2 trang đang được dùng",
       spec="Đã hỏi leader",
       note="MT-17 — Backup 1.0 r254 ghi「Chỉ back up các conversion có setting ở action friend "
            "(action open link conversion)」; feature-spec §7.5 nói copy cả bảng `conversion`."),

    tc("Copy コンバージョン・URL・対応ステータス", "FUNC-001", "Abnormal",
       "Trang chuyển đổi sau khi copy có nằm ĐÚNG folder ở bot nhận không?",
       CP + "\n- Bot A có 2 folder trang chuyển đổi tự tạo, mỗi folder 2 trang",
       RUN + "3. Mở màn コンバージョン ở bot B\n"
             "4. ĐẾM số folder, đọc tên\n"
             "5. Kiểm tra từng trang chuyển đổi nằm ở folder nào\n"
             "6. Kiểm tra có trang nào rơi vào folder lạ hoặc không hiển thị không",
       "2 folder × 2 trang",
       "- Bot B có đủ 2 folder đúng tên\n"
       "- Mỗi trang chuyển đổi nằm ĐÚNG folder tương ứng như bot A\n"
       "- KHÔNG có trang nào bị gán vào folder không tồn tại hoặc biến mất khỏi danh sách\n"
       "- ⚠️ Nếu trang không hiện hoặc nằm sai folder thì raise bug",
       spec="Đã hỏi leader",
       note="MT-17 — Backup 1.0 r254 (Note):「bị backup SAI FOLDER (chưa tạo folder mới mà đang lấy theo "
            "folder id của bot cũ)」. Backup (job) r276 không ghi chú. ⚠️ DỰ KIẾN FAIL nếu chưa fix."),

    tc("Copy コンバージョン・URL・対応ステータス", "REG-URL-001", "Normal",
       "Trang chuyển đổi sau copy hoạt động độc lập ở bot nhận",
       CP + "\n- Đã copy trang chuyển đổi「CV-01」từ A sang B",
       "1. Mở màn コンバージョン ở bot B, lấy đường dẫn của「CV-01」\n"
       "2. So sánh đường dẫn với bot A\n"
       "3. Mở đường dẫn của bot B bằng tài khoản là bạn bè của bot B\n"
       "4. Xem số lượt truy cập ở cả 2 bot",
       "1 trang chuyển đổi",
       "- Đường dẫn ở bot B KHÁC bot A\n"
       "- Bước 4: lượt truy cập tăng ở bot B, KHÔNG tăng ở bot A",
       note="Suy luận của AI mở rộng từ Backup (job) r276 (ô kết quả để trống). Cần Leader xác nhận."),

    tc("Copy コンバージョン・URL・対応ステータス", "REG-URL-001", "Abnormal",
       "URL rút gọn / URL chuyển hướng — có được copy không?",
       CP + "\n- Bot A có 3 URL rút gọn trong màn URL và 1 mẫu tin văn bản chứa URL chuyển hướng",
       RUN + "3. Mở màn quản lý URL ở bot B, đếm số URL\n"
             "4. Mở mẫu tin văn bản ở bot B, đọc URL chuyển hướng trong nội dung\n"
             "5. Gửi mẫu tin cho bạn bè bot B và bấm vào URL",
       "3 URL rút gọn + 1 URL chuyển hướng trong mẫu tin",
       "- Ghi rõ hiện trạng theo quyết định MT-28:\n"
       "  · nếu URL rút gọn ĐƯỢC copy: bot B có đủ 3 URL, mỗi cái có mã rút gọn MỚI\n"
       "  · nếu KHÔNG copy: màn URL của bot B trống\n"
       "- Bước 5: URL trong mẫu tin KHÔNG được trỏ tới URL rút gọn của bot A "
       "(nếu có thì là rò rỉ dữ liệu chéo bot — raise bug)",
       spec="Đã hỏi leader",
       note="MT-28 — Backup (job) r277 ghi「11. url redirect — không support」; "
            "db-mapping.md:417 ghi bảng `url` (order 27) là `is_enable=1` (được copy). Mâu thuẫn thẳng."),

    tc("Copy コンバージョン・URL・対応ステータス", "FUNC-001", "Normal",
       "Copy trạng thái xử lý (対応ステータス)",
       CP + "\n- Bot A có 4 trạng thái xử lý tự tạo, mỗi cái có tên và màu riêng",
       RUN + "3. Mở màn cài đặt trạng thái xử lý ở bot B\n"
             "4. Đếm số trạng thái và đối chiếu tên + màu + thứ tự\n"
             "5. Mở màn chat 1:1 ở bot B, thử gán 1 trạng thái cho bạn bè",
       "4 trạng thái:「未対応」「対応中」「保留」「完了」với 4 màu khác nhau",
       "- Bot B có đủ 4 trạng thái, đúng tên, đúng màu, đúng thứ tự\n"
       "- Bước 5: gán được cho bạn bè bot B bình thường",
       note="⚠️ Backup (job) r346 ghi「13. Status đối ứng (CHƯA CÓ TESTCASE)」— corpus xác nhận đây là "
            "VÙNG TRỐNG. TC này do AI viết theo feature-spec §1.3 mục 11 (`status_chat`). Cần Leader duyệt."),

    tc("Copy コンバージョン・URL・対応ステータス", "DATA-REF-001", "Normal",
       "Hành động đổi trạng thái xử lý ở các tính năng khác trỏ đúng trạng thái bot nhận",
       CP + "\n- Bot A có trạng thái xử lý「対応中」và 1 auto reply + 1 richmenu có hành động gán trạng thái đó",
       RUN + "3. Mở màn cài đặt trạng thái ở bot B, xác nhận「対応中」đã copy\n"
             "4. Mở auto reply và richmenu ở bot B, xem hành động trỏ tới trạng thái nào\n"
             "5. Kích hoạt từ máy LINE thật rồi mở màn chat 1:1 ở bot B",
       "1 trạng thái + 2 nơi dùng",
       "- Cả 2 hành động trỏ tới trạng thái của BOT B\n"
       "- Bước 5: bạn bè được gán đúng trạng thái ở bot B",
       env="PRODUCTION",
       note="TC do AI bổ sung để phủ nhánh ánh xạ của `status_chat` — corpus có nhắc hành động status chat "
            "trong khối autoreply/richmenu nhưng không có TC riêng cho tính năng này. Cần Leader duyệt."),

    # ═══════════════ 20. Copy 友だち追加時設定 ═══════════════
    tc("Copy 友だち追加時設定", "FUNC-001", "Normal",
       "Cài đặt khi thêm bạn được GHI ĐÈ lên bản ghi sẵn có của bot nhận",
       CP + "\n- Bot A đã cài đặt đầy đủ cho 3 tình huống: bạn bè MỚI, bạn bè CŨ quay lại, bỏ chặn\n"
            "- Bot B đã có sẵn cài đặt khi thêm bạn KHÁC bot A",
       RUN + "3. Mở màn 友だち追加時設定 ở bot B\n"
             "4. Đối chiếu cài đặt của cả 3 tình huống với bot A\n"
             "5. Đếm xem có bản ghi cài đặt nào bị nhân đôi không",
       "3 tình huống × cài đặt khác nhau ở 2 bot",
       "- Cài đặt ở bot B được thay bằng cài đặt của bot A cho cả 3 tình huống\n"
       "- CHỈ có 1 bộ cài đặt — KHÔNG bị nhân đôi bản ghi\n"
       "- Cài đặt cũ của bot B bị ghi đè, không còn tồn tại song song",
       note="Nguồn: feature-spec BR-11 —「add_friend_setting không được clone mới, chỉ UPDATE record của LOA đích」. "
            "Corpus Backup (job) r347 (khối「14. Setting kết bạn thường」). TC ghi-đè do AI bổ sung để verify BR-11."),

    tc("Copy 友だち追加時設定", "MSG-001", "Normal",
       "Tin gửi cho bạn bè MỚI — mã chèn thông tin mặc định giữ nguyên",
       CP + "\n- Bot A có tin gửi cho bạn bè mới, chèn đủ 9 mã thông tin mặc định",
       RUN + "3. Mở màn 友だち追加時設定 ở bot B, phần bạn bè MỚI\n"
             "4. Đọc nội dung tin, đối chiếu TỪNG mã chèn\n"
             "5. Dùng 1 tài khoản LINE chưa từng kết bạn để kết bạn với bot B\n"
             "6. Đọc tin chào nhận được trên LINE",
       BASIC9,
       "- Cả 9 mã chèn GIỮ NGUYÊN, không bị thay đổi\n"
       "- Bước 6: tin chào hiển thị đúng giá trị của bạn bè bot B ở các mục đã có dữ liệu\n"
       "- Không hiển thị mã thô",
       env="PRODUCTION",
       note="Gộp 9 mục vì CÙNG 1 kết quả「dạng này giữ nguyên code cố định」. "
            "Bug #32414. Nguồn: Backup 1.0 r258-r262 · Backup (job) r348-r352."),

    tc("Copy 友だち追加時設定", "DATA-REF-001", "Normal",
       "Tin gửi cho bạn bè MỚI — mã chèn thông tin TỰ TẠO được thay sang bot nhận",
       CP + "\n- Bot A có thông tin bạn bè tự tạo ở CẢ 2 folder, mỗi folder đủ 6 kiểu\n"
            "- Tin gửi cho bạn bè mới chèn đủ 12 mã đó",
       RUN + "3. Mở màn 友だち情報 ở bot B, xác nhận 12 mục đã copy\n"
             "4. Mở phần bạn bè MỚI, đối chiếu TỪNG mã chèn trong nội dung tin\n"
             "5. Kết bạn mới với bot B bằng tài khoản LINE sạch\n"
             "6. Đọc tin chào và mở chi tiết bạn bè đó ở bot B",
       FI12,
       "- CẢ 12 mã chèn được thay thành mã của BOT B\n"
       "- KHÔNG còn mã nào của bot A\n"
       "- Bước 6: tin chào hiển thị đúng giá trị của bạn bè bot B, không hiển thị mã thô",
       env="PRODUCTION",
       note="Gộp 12 điểm vì CÙNG 1 kết quả「replace code friend infor khác với bot gốc」. "
            "Bug #32414. Nguồn: Backup 1.0 r263-r274 · Backup (job) r353-r364."),

    tc("Copy 友だち追加時設定", "MSG-001", "Normal",
       "Tin gửi cho bạn bè CŨ quay lại — mã chèn thông tin mặc định giữ nguyên",
       CP + "\n- Bot A có tin gửi cho bạn bè cũ quay lại, chèn đủ 9 mã thông tin mặc định",
       RUN + "3. Mở phần bạn bè CŨ ở bot B, đối chiếu 9 mã chèn\n"
             "4. Dùng tài khoản LINE đã từng kết bạn với bot B, huỷ kết bạn rồi kết bạn lại\n"
             "5. Đọc tin nhận được trên LINE",
       BASIC9,
       "- Cả 9 mã chèn GIỮ NGUYÊN\n"
       "- Bước 5: nhận đúng tin dành cho bạn bè CŨ (khác tin bạn bè mới), hiển thị đúng giá trị",
       env="PRODUCTION",
       note="Gộp 9 mục vì cùng 1 kết quả. Nguồn: Backup 1.0 r275-r279 · Backup (job) r365-r369."),

    tc("Copy 友だち追加時設定", "DATA-REF-001", "Normal",
       "Tin gửi cho bạn bè CŨ quay lại — mã chèn thông tin tự tạo được thay sang bot nhận",
       CP + "\n- Bot A có tin gửi cho bạn bè cũ, chèn đủ 12 mã thông tin tự tạo (2 folder × 6 kiểu)",
       RUN + "3. Mở phần bạn bè CŨ ở bot B, đối chiếu TỪNG mã chèn\n"
             "4. Dùng tài khoản LINE đã từng kết bạn với bot B để kết bạn lại\n"
             "5. Đọc tin nhận được và mở chi tiết bạn bè ở bot B",
       FI12,
       "- CẢ 12 mã chèn được thay thành mã của BOT B\n"
       "- Bước 5: hiển thị đúng giá trị của bạn bè bot B",
       env="PRODUCTION",
       note="Gộp 12 điểm vì cùng 1 kết quả. Nguồn: Backup 1.0 r280-r291 · Backup (job) r370-r381."),

    tc("Copy 友だち追加時設定", "MSG-001", "Normal",
       "Tin gửi khi bạn bè BỎ CHẶN — mã chèn thông tin mặc định giữ nguyên",
       CP + "\n- Bot A có tin gửi khi bạn bè bỏ chặn, chèn đủ 9 mã thông tin mặc định",
       RUN + "3. Mở phần bỏ chặn ở bot B, đối chiếu 9 mã chèn\n"
             "4. Dùng tài khoản LINE chặn bot B rồi bỏ chặn\n"
             "5. Đọc tin nhận được trên LINE",
       BASIC9,
       "- Cả 9 mã chèn GIỮ NGUYÊN\n"
       "- Bước 5: nhận đúng tin dành cho tình huống bỏ chặn, hiển thị đúng giá trị",
       env="PRODUCTION",
       note="Gộp 9 mục vì cùng 1 kết quả. Nguồn: Backup 1.0 r292-r296 · Backup (job) r382-r386."),

    tc("Copy 友だち追加時設定", "DATA-REF-001", "Normal",
       "Tin gửi khi bạn bè BỎ CHẶN — mã chèn thông tin tự tạo được thay sang bot nhận",
       CP + "\n- Bot A có tin gửi khi bỏ chặn, chèn đủ 12 mã thông tin tự tạo (2 folder × 6 kiểu)",
       RUN + "3. Mở phần bỏ chặn ở bot B, đối chiếu TỪNG mã chèn\n"
             "4. Dùng tài khoản LINE chặn bot B rồi bỏ chặn\n"
             "5. Đọc tin nhận được và mở chi tiết bạn bè ở bot B",
       FI12,
       "- CẢ 12 mã chèn được thay thành mã của BOT B\n"
       "- Bước 5: hiển thị đúng giá trị của bạn bè bot B",
       env="PRODUCTION",
       note="Gộp 12 điểm vì cùng 1 kết quả. Nguồn: Backup 1.0 r297-r308 · Backup (job) r387-r398."),

    tc("Copy 友だち追加時設定", "DATA-REF-001", "Normal",
       "Hành động kèm theo trong cài đặt khi thêm bạn trỏ đúng dữ liệu bot nhận",
       CP + "\n- Bot A có cài đặt khi thêm bạn với hành động: gắn thẻ + bắt đầu kịch bản + gửi mẫu tin",
       RUN + "3. Mở màn 友だち追加時設定 ở bot B, mở phần hành động\n"
             "4. Kiểm tra thẻ / kịch bản / mẫu tin được trỏ tới là của bot nào\n"
             "5. Kết bạn mới với bot B và kiểm tra kết quả ở màn 友だちリスト",
       "3 hành động con",
       "- Cả 3 hành động trỏ tới dữ liệu của BOT B\n"
       "- Bước 5: bạn bè mới được gắn thẻ, vào kịch bản và nhận mẫu tin đều của bot B",
       env="PRODUCTION",
       note="Nguồn: feature-spec BR-11 —「UPDATE ... remap action_id và template_id đã remapped từ LOA nguồn」. "
            "Corpus không tách TC riêng cho phần hành động này — do AI bổ sung. Cần Leader duyệt."),

    # ═══════════════ 21. Copy アクションスケジュール ═══════════════
    tc("Copy アクションスケジュール", "FUNC-001", "Normal",
       "Copy folder và danh sách lịch chạy hành động",
       CP + "\n- Bot A có 2 folder lịch chạy hành động, mỗi folder 2 mục",
       RUN + "3. Mở màn アクションスケジュール ở bot B\n"
             "4. Đếm folder, đọc tên và thứ tự\n"
             "5. Mở từng folder đếm số mục và đối chiếu tên",
       "2 folder × 2 mục",
       "- Bot B có đủ 2 folder, đúng tên và thứ tự\n"
       "- Mỗi folder có đúng 2 mục, đúng tên, nằm đúng folder",
       note="Nguồn: Backup (job) r309-r310."),

    tc("Copy アクションスケジュール", "UI-FIELD-001", "Normal",
       "Copy tên quản lý của lịch chạy hành động",
       CP + "\n- Bot A có 3 lịch chạy với tên quản lý khác nhau, 1 tên có tiếng Nhật và ký tự đặc biệt",
       RUN + "3. Mở chi tiết 3 lịch chạy ở bot B\n4. Đối chiếu tên quản lý từng cái",
       "①「毎日リマインド」②「月末キャンペーン★」③「schedule-03」",
       "- Cả 3 tên ở bot B giống hệt bot A, không bị cắt, giữ nguyên ký tự đặc biệt",
       note="Nguồn: Backup (job) r311."),

    tc("Copy アクションスケジュール", "DATA-REF-001", "Normal",
       "Copy bộ lọc đối tượng của lịch chạy hành động",
       CP + "\n- Bot A có lịch chạy gắn bộ lọc theo thẻ và theo thông tin bạn bè",
       RUN + "3. Mở chi tiết lịch chạy ở bot B, mở bộ lọc\n"
             "4. Đối chiếu điều kiện lọc và các mục được trỏ tới\n"
             "5. Sửa bộ lọc ở bot B rồi kiểm tra ở bot A",
       "Bộ lọc 2 điều kiện: có thẻ「タグ-S」và thông tin điểm ≥ 10",
       "- Điều kiện lọc giống bot A nhưng trỏ tới thẻ và thông tin của BOT B\n"
       "- Bước 5: sửa ở bot B KHÔNG ảnh hưởng bot A",
       note="Nguồn: Backup (job) r312 · feature-spec §7.4 —「actionSchedulesBackup → fix filter_ids」. "
            "Xem thêm MT-13."),

    tc("Copy アクションスケジュール", "DATA-ID-001", "Normal",
       "Copy hành động của lịch chạy",
       CP + "\n- Bot A có lịch chạy với hành động: gửi mẫu tin + gắn thẻ",
       RUN + "3. Mở chi tiết lịch chạy ở bot B, mở phần hành động\n"
             "4. Đối chiếu mẫu tin và thẻ được trỏ tới\n"
             "5. Chỉnh giờ chạy về gần hiện tại và chờ lịch chạy",
       "2 hành động con",
       "- Hành động trỏ tới mẫu tin và thẻ của BOT B\n"
       "- Bước 5: lịch chạy đúng giờ, bạn bè bot B nhận mẫu tin và được gắn thẻ",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r313. PRODUCTION theo RULE-08 (phụ thuộc job chạy theo lịch)."),

    tc("Copy アクションスケジュール", "FUNC-DATE-001", "Normal",
       "Copy ngày giờ bắt đầu của lịch chạy",
       CP + "\n- Bot A có 2 lịch chạy với ngày giờ bắt đầu khác nhau",
       RUN + "3. Mở chi tiết 2 lịch chạy ở bot B\n4. Đối chiếu ngày giờ bắt đầu",
       "① 2026-09-01 09:00 ② 2026-12-31 23:59",
       "- Ngày giờ bắt đầu ở bot B khớp CHÍNH XÁC bot A, không lệch phút\n"
       "- Không bị đổi sang thời điểm copy",
       note="Nguồn: Backup (job) r314."),

    tc("Copy アクションスケジュール", "FUNC-DATE-001", "Normal",
       "Copy 3 kiểu điều kiện dừng của lịch chạy",
       CP + "\n- Bot A có 3 lịch chạy: 1 không dừng, 1 dừng theo ngày giờ, 1 dừng theo số lần",
       RUN + "3. Mở chi tiết cả 3 lịch chạy ở bot B\n"
             "4. Đối chiếu kiểu dừng và tham số kèm theo",
       "① không dừng ② dừng 2026-12-31 23:59 ③ dừng sau 10 lần",
       "- Cả 3 kiểu dừng giữ đúng ở bot B\n"
       "- Tham số (ngày giờ dừng, số lần) khớp chính xác\n"
       "- Không có lịch nào bị đổi sang kiểu dừng khác",
       note="Gộp 3 kiểu vì cùng 1 kết quả (giữ nguyên cài đặt). Nguồn: Backup (job) r315-r317."),

    tc("Copy アクションスケジュール", "FUNC-DATE-001", "Normal",
       "Copy kiểu lặp theo ngày và theo thứ trong tuần",
       CP + "\n- Bot A có 1 lịch lặp theo ngày (mỗi 3 ngày) và 1 lịch lặp theo thứ (thứ 2, 4, 6)",
       RUN + "3. Mở chi tiết 2 lịch chạy ở bot B\n"
             "4. Đối chiếu kiểu lặp và tham số\n"
             "5. Chỉnh về gần hiện tại và quan sát 2 lần chạy liên tiếp",
       "① mỗi 3 ngày ② thứ 2, 4, 6",
       "- Kiểu lặp và tham số giữ đúng ở bot B\n"
       "- Bước 5: khoảng cách giữa 2 lần chạy đúng như cài đặt",
       env="PRODUCTION",
       note="Nguồn: Backup (job) r318-r319."),

    tc("Copy アクションスケジュール", "FUNC-DATE-001", "Boundary",
       "Copy kiểu lặp theo ngày trong tháng — 3 biến thể",
       CP + "\n- Bot A có 3 lịch chạy lặp theo tháng với 3 biến thể ở cột dữ liệu test",
       RUN + "3. Mở chi tiết cả 3 lịch chạy ở bot B\n"
             "4. Đối chiếu biến thể và tham số từng cái\n"
             "5. Chỉnh lịch「ngày cuối tháng」sang tháng có 28/30/31 ngày và quan sát ngày chạy thực tế",
       "① ngày 15 hàng tháng ② ngày CUỐI THÁNG ③ thứ 2 của tuần thứ 3 mỗi tháng",
       "- Cả 3 biến thể giữ đúng ở bot B, không bị quy về cùng 1 kiểu\n"
       "- Bước 5: lịch「ngày cuối tháng」chạy đúng ngày 28 / 30 / 31 tuỳ tháng, "
       "KHÔNG bị cố định thành ngày 30 hay 31",
       env="PRODUCTION",
       note="Gộp 3 biến thể ở bước đối chiếu nhưng TÁCH riêng bước 5 vì「ngày cuối tháng」là điểm biên "
            "hay sinh lỗi. Nguồn: Backup (job) r320-r322."),

    tc("Copy アクションスケジュール", "JOB-001", "Normal",
       "Lịch chạy sau khi copy hoạt động độc lập ở bot nhận",
       CP + "\n- Đã copy lịch chạy hành động từ A sang B",
       "1. Ở bot B, chỉnh lịch chạy về gần thời điểm hiện tại\n"
       "2. Chờ lịch chạy\n"
       "3. Kiểm tra bạn bè của bot B có nhận hành động không\n"
       "4. Kiểm tra bạn bè của bot A CÓ bị ảnh hưởng không",
       "1 lịch chạy",
       "- Bước 3: bạn bè bot B nhận đúng hành động\n"
       "- Bước 4: bạn bè bot A KHÔNG nhận gì thêm\n"
       "- Lịch ở bot A vẫn giữ nguyên cài đặt gốc",
       env="PRODUCTION",
       note="Suy luận của AI theo SEC-ISO-001 + JOB-001 — corpus không có TC kiểm tra tính độc lập của "
            "lịch chạy sau copy. Cần Leader xác nhận."),
]
