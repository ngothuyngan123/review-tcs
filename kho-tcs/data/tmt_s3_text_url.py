# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 14-18: template text (nội dung, insert data, PDF, shorten URL)
và URL redirect (preview/metadata, hết hạn & action).

Nguồn chính: 02. TCsLine_Template
  - tab「Template type text」(2023 → 10/2025, 420 dòng — tab master của loại text; cột kết quả
    Bug #32109 30/9/2025 và Bug #32590 30/10/2025)
  - tab「Preview URL」(setting hiển thị preview URL trên LINE)
  - tab「Task nhỏ+ check Bug Kh」r11 (logic hết hạn URL dạng duration), r19-r33 (action nào apply
    setting số lần bấm), r36-r42 (template chứa link file/media)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Folder F1 có group template G1; đang ở màn tạo template con của G1")
TXT = ADM + "\n- Đã chọn loại tin nhắn「テキスト」"
URLT = (ADM + "\n- Đã có template text TU chứa 1 URL ngoài hệ thống (https://example.com/campaign)\n"
        "- Đã đăng ký 1 friend U1 làm クイックテストユーザー")

S3 = [
    # ═════════════ 14. Text — soạn nội dung ═════════════
    tc("Text — soạn nội dung", "UI-001", "Normal",
       "Giao diện tab soạn nội dung text + popup upload PDF khớp design",
       TXT,
       "1. Quan sát tab「テキスト登録」: textarea, toolbar, checkbox, nút 保存/戻る\n"
       "2. Đối chiếu text / màu chữ / khung viền / màu tab / icon / khoảng cách / hover với design\n"
       "3. Bấm icon「PDFアップロード」→ quan sát popup\n4. Đối chiếu popup với design",
       "—",
       "- Tab soạn nội dung khớp design về text, màu chữ, khung viền, màu tab, icon, khoảng cách, hover\n"
       "- Popup upload PDF cũng khớp design về các mục trên",
       note="Nguồn: Template type text r5-r6."),

    tc("Text — soạn nội dung", "DATA-TEXT-001", "Normal",
       "Nhập nội dung text hợp lệ (Nhật, xuống dòng, multi enter, ký tự đặc biệt, emoji, full/half-width) → lưu và gửi đúng",
       TXT + "\n- Đã đăng ký 1 friend U1 làm クイックテストユーザー",
       "1. Nhập nội dung text thường (không có thẻ insert) → 保存 → gửi test → xem LINE\n"
       "2. Lặp lại với text Nhật có 1 lần xuống dòng\n3. Lặp lại với text có nhiều dòng trống liên tiếp\n"
       "4. Lặp lại với text chứa ký tự đặc biệt + emoji\n"
       "5. Lặp lại với text copy-paste full-width Japanese\n6. Lặp lại với half-width Japanese",
       "6 biến thể nội dung: thường / Nhật + enter / multi enter / ký tự đặc biệt + emoji / "
       "full-width JP (ａｂｃ) / half-width JP (ｱｲｳ)",
       "- Cả 6 biến thể đều 保存 thành công\n"
       "- Vào lại màn edit hiện đúng nội dung đã nhập (giữ nguyên xuống dòng và dòng trống)\n"
       "- Tin nhận trên LINE hiển thị đúng nội dung, đúng ngắt dòng, emoji và ký tự đặc biệt không bị lỗi",
       note="Nguồn: Template type text r7-r13. Gộp 6 biến thể input vì CÙNG 1 kết quả mong đợi "
            "(lưu + gửi đúng) — theo quy tắc tách TC."),

    tc("Text — soạn nội dung", "UI-INPUT-001", "Abnormal",
       "Không nhập nội dung → báo lỗi 本文は必ず指定してください。",
       TXT,
       "1. Để trống textarea nội dung\n2. Bấm「保存」\n3. Quan sát thông báo lỗi",
       "textarea rỗng",
       "- KHÔNG lưu được template\n- Hiện msg lỗi chính xác:「本文は必ず指定してください。」",
       note="Nguồn: Template type text r14."),

    tc("Text — soạn nội dung", "UI-INPUT-001", "Boundary",
       "Nội dung đúng 5.000 ký tự → lưu OK; vượt 5.000 → chặn, bộ đếm đúng theo từng loại ký tự",
       TXT,
       "1. Nhập đúng 5.000 ký tự latinh → quan sát bộ đếm → 保存\n"
       "2. Nhập 5.001 ký tự → quan sát bộ đếm và hành vi 保存\n"
       "3. Lặp lại đếm với full-width Japanese, half-width Japanese, symbol và emoji",
       "5.000 / 5.001 ký tự; 4 loại ký tự để kiểm bộ đếm",
       "- 5.000 ký tự: bộ đếm hiện 5000/5,000 và lưu thành công\n"
       "- Vượt 5.000: bị chặn (không nhập thêm hoặc báo lỗi khi lưu)\n"
       "- Bộ đếm tính đúng cho latinh / full-width JP / half-width JP / symbol / emoji",
       note="Nguồn: Template type text r15. Khớp spec ui-spec.md:187 (max 5.000). "
            "⚠ TC gốc không ghi rõ cách đếm emoji ở ô này → cần Leader xác nhận khi chạy."),

    tc("Text — soạn nội dung", "DATA-TEXT-001", "Abnormal",
       "Nội dung text KHÔNG tự trim space đầu/cuối",
       TXT,
       "1. Nhập「  テストメッセージ  」(có space đầu và cuối)\n2. Bấm「保存」\n3. Vào lại màn edit\n"
       "4. Gửi test và quan sát tin trên LINE",
       "「  テストメッセージ  」",
       "- Lưu thành công, nội dung GIỮ NGUYÊN space đầu/cuối\n"
       "- Màn edit hiện lại đúng chuỗi có space\n- Tin trên LINE cũng giữ space",
       note="Nguồn: Template type text r16 (「ko tự trim => đã check trên stg」). "
            "Spec KHÔNG ghi rule trim cho ô text → xem MT-21."),

    tc("Text — soạn nội dung", "OUT-PREVIEW-001", "Normal",
       "Preview template text hiện đúng nội dung ở 4 điểm preview",
       TXT + "\n- Đã lưu template text T1 có nội dung nhiều dòng",
       "1. Preview ở màn list message của group template\n2. Preview ở màn list template\n"
       "3. Preview ở modal send template của màn chat 1:1\n4. Preview khi send template phía app mobile",
       "T1 nội dung 3 dòng",
       "- Cả 4 điểm đều hiện đủ nội dung 3 dòng, giữ đúng ngắt dòng\n- Nội dung khớp tin thật gửi cho user",
       note="Nguồn: Template type text r162-r165."),

    tc("Text — soạn nội dung", "FUNC-001", "Normal",
       "Sửa template text mới → màn edit hiện đúng type và nội dung, lưu được nội dung mới",
       TXT + "\n- Đã lưu template text T1",
       "1. Mở màn edit của T1\n2. Quan sát mục type tin nhắn và nội dung\n3. Sửa nội dung\n4. 保存\n"
       "5. Gửi test và quan sát tin trên LINE",
       "T1 sửa nội dung",
       "- Màn edit hiện type「テキスト」và đúng nội dung đã lưu trước đó\n"
       "- Lưu thành công; tin trên LINE hiện nội dung MỚI",
       note="Nguồn: Template type text r155-r157, r160-r161."),

    # ═════════════ 15. Text — insert dữ liệu ═════════════
    tc("Text — insert dữ liệu", "FUNC-001", "Normal",
       "Insert LINE名 → chèn {name} vào đúng vị trí con trỏ; gửi đi replace thành tên LINE của friend",
       TXT + "\n- Friend U1 có tên LINE là「テスト太郎」và là クイックテストユーザー",
       "1. Nhập「こんにちは、」vào textarea, đặt con trỏ ở cuối\n2. Bấm「情報自動挿入」→「LINE名」\n"
       "3. Quan sát chuỗi trong textarea\n4. Nhập tiếp「さん」→ 保存\n5. Gửi test cho U1 → xem LINE",
       "Nội dung cuối:「こんにちは、{name}さん」",
       "- Bấm「LINE名」chèn đúng chuỗi `{name}` vào vị trí con trỏ, không chèn ở cuối văn bản\n"
       "- Tin trên LINE của U1 hiện「こんにちは、テスト太郎さん」",
       note="Nguồn: Template type text r17."),

    tc("Text — insert dữ liệu", "FUNC-DATE-001", "Normal",
       "Insert 日数・日付 kiểu「số ngày remain」→ validate ngày quá khứ, chèn code [remain to=...]",
       TXT,
       "1. Bấm「情報自動挿入」→「日数・日付」→ chọn kiểu insert số ngày remain\n"
       "2. Chưa chọn ngày → bấm「挿入」→ quan sát\n3. Chọn ngày = hôm nay → bấm「挿入」→ quan sát\n"
       "4. Chọn ngày > hôm nay → bấm「挿入」→ quan sát chuỗi trong textarea\n5. 保存 và gửi test",
       "Ngày: bỏ trống / hôm nay / hôm nay + 7",
       "- Chưa chọn ngày: báo lỗi「過去の日付は挿入できません」, không chèn code\n"
       "- Ngày = hôm nay: báo lỗi「過去の日付は挿入できません」, không chèn code\n"
       "- Ngày tương lai: chèn code dạng `[remain to=...]` vào textarea; lưu và gửi thành công, "
       "tin trên LINE hiện đúng số ngày còn lại",
       note="Nguồn: Template type text r18."),

    tc("Text — insert dữ liệu", "FUNC-DATE-001", "Normal",
       "Insert 日数・日付 kiểu「ngày tháng năm」→ nhập số ngày (cho cả số âm), chọn 1 trong 8 format",
       TXT,
       "1. Bấm「情報自動挿入」→「日数・日付」→ chọn kiểu insert ngày tháng năm\n"
       "2. Thử nhập text vào ô số ngày → quan sát\n3. Nhập số âm (-3) → quan sát\n"
       "4. Bấm mũi tên tăng/giảm → quan sát\n5. Mở ô chọn format → đếm số lựa chọn và xem giá trị default\n"
       "6. Chọn 1 format khác default → 挿入 → 保存 → gửi test",
       "số ngày: text / -3 / +5; 8 format ngày, default là「月日と曜日 (M月...)」",
       "- Ô số ngày CHỈ nhận số (nhập text không vào được), CHO PHÉP số âm, mũi tên tăng/giảm hoạt động\n"
       "- Ô format có đúng 8 lựa chọn, default là lựa chọn đầu tiên\n"
       "- Chèn được code vào textarea; tin trên LINE hiện ngày đúng theo format đã chọn và đúng offset ngày",
       note="Nguồn: Template type text r19."),

    tc("Text — insert dữ liệu", "FUNC-DATE-001", "Normal",
       "Insert 配信日 → chọn format ngày, chèn code [date] hoặc [date_format=...]",
       TXT,
       "1. Bấm「情報自動挿入」→「配信日」→ quan sát list format ngày\n"
       "2. Chọn format ĐẦU TIÊN → quan sát chuỗi chèn vào textarea\n"
       "3. Chọn format khác (VD Y年n月j日(D)) → quan sát chuỗi chèn\n4. 保存 và gửi test",
       "2 format: đầu tiên và「Y年n月j日(D)」",
       "- List format ngày của 配信日 giống list của 日数・日付\n"
       "- Chọn format đầu tiên → chèn `[date]`\n"
       "- Chọn format khác → chèn `[date_format=Y年n月j日(D)]`\n"
       "- Tin trên LINE hiện đúng NGÀY GỬI theo format đã chọn",
       note="Nguồn: Template type text r20."),

    tc("Text — insert dữ liệu", "FUNC-001", "Normal",
       "Insert link フォーム → list form sắp theo created_at, chèn link, user mở được form",
       TXT + "\n- Bot A có 3 form đã public, tạo ở 3 thời điểm khác nhau",
       "1. Bấm「情報自動挿入」→「フォーム」→ quan sát danh sách và thứ tự\n2. Chọn 1 form → 挿入 → 保存\n"
       "3. Gửi test cho U1\n4. Trên LINE, bấm vào link vừa nhận",
       "3 form; chọn form「アンケート」",
       "- Danh sách hiện ĐẦY ĐỦ form của bot, sắp xếp theo `created_at` (logic cũ)\n"
       "- Chèn được link form vào textarea, lưu thành công\n"
       "- User bấm link trên LINE → mở đúng trang form「アンケート」và trả lời được",
       note="Nguồn: Template type text r21-r23. RULE-06: đi tới output cuối là trang form trên LINE."),

    tc("Text — insert dữ liệu", "FRIEND-001", "Normal",
       "Insert 友だち情報 (basic và tự tạo) → gửi đi replace đúng giá trị của từng friend",
       TXT + "\n- Bot A có friend info mặc định (system name, mail, số đt, ngày sinh, địa chỉ)\n"
             "- Có 2 friend info tự tạo: kiểu Mô tả và kiểu Lựa chọn\n"
             "- Friend U1 đã có giá trị cho toàn bộ các info trên",
       "1. Bấm「情報自動挿入」→「友だち情報」→ chèn từng friend info basic\n"
       "2. Chèn tiếp 2 friend info tự tạo\n3. 保存\n4. Gửi test cho U1 → xem tin trên LINE",
       "5 friend info basic + 2 friend info tự tạo; U1 có đủ giá trị",
       "- Chèn được code cho cả friend info basic và friend info tự tạo\n"
       "- Tin trên LINE của U1 hiện ĐÚNG giá trị từng info của U1 (không còn chuỗi code)",
       note="Nguồn: Template type text r24-r25."),

    tc("Text — insert dữ liệu", "FRIEND-001", "Abnormal",
       "Friend CHƯA có giá trị friend info → phần code bị bỏ qua, không hiện chuỗi code",
       TXT + "\n- Friend U2 CHƯA có giá trị cho friend info「電話番号」và 1 friend info tự tạo",
       "1. Tạo template text có chèn code của「電話番号」và friend info tự tạo\n2. 保存\n"
       "3. Gửi test cho U2 → xem tin trên LINE",
       "U2 thiếu 2 giá trị friend info",
       "- Tin trên LINE của U2 KHÔNG hiện chuỗi code (VD `[FRIEND_INFO_...]`)\n"
       "- Phần thiếu giá trị được bỏ qua, phần còn lại của nội dung vẫn hiện bình thường",
       note="Nguồn: Template button r63-r64 (cùng cơ chế replace friend info dùng chung cho text và button)."),

    tc("Text — insert dữ liệu", "FUNC-001", "Normal",
       "Insert link 商品販売 → CHỈ hiện item mới (is_product_new = 1), user mở được trang mua",
       TXT + "\n- Bot A có 2 item mới (単品/継続) và 1 item CŨ (is_product_new = 0)",
       "1. Bấm「情報自動挿入」→「商品販売」→ quan sát danh sách\n"
       "2. Chọn 1 item → 挿入 → 保存\n3. Gửi test cho U1 → bấm link trên LINE",
       "2 item mới + 1 item cũ",
       "- Danh sách CHỈ hiện 2 item mới, KHÔNG hiện item cũ; sắp theo `created_at`\n"
       "- Chèn được link; user bấm link trên LINE → mở đúng trang bán sản phẩm",
       note="Nguồn: Template type text r26-r28 (TC gốc ghi rõ query `s_item` theo bot + "
            "`is_product_new = 1`)."),

    tc("Text — insert dữ liệu", "FUNC-001", "Normal",
       "Insert link カレンダー予約 và イベント予約 → hiện đủ danh sách, user mở được trang đặt chỗ",
       TXT + "\n- Bot A có 2 calendar 予約 và 2 event 予約 đã public",
       "1. Bấm「情報自動挿入」→「カレンダー予約」→ quan sát danh sách → chọn 1 → 挿入\n"
       "2. Bấm「情報自動挿入」→「イベント予約」→ quan sát danh sách → chọn 1 → 挿入\n"
       "3. 保存\n4. Gửi test cho U1 → bấm từng link trên LINE",
       "2 calendar + 2 event",
       "- Cả 2 danh sách hiện đầy đủ bản ghi của bot\n"
       "- Chèn được cả 2 link; user bấm từng link → mở đúng trang đặt lịch / đặt chỗ tương ứng",
       note="Nguồn: Template type text r29-r34."),

    tc("Text — insert dữ liệu", "MSG-002", "Abnormal",
       "Sau khi insert data mà nội dung vượt 5.000 ký tự khi gửi → tin lỗi, ghi nhận ở màn /basic/error-list",
       TXT + "\n- Friend U3 có friend info kiểu mail giá trị rất dài (>30 ký tự)\n"
             "- Template text nội dung sát 5.000 ký tự + nhiều code friend info",
       "1. Tạo template text có tổng nội dung sát 5.000 ký tự và chèn nhiều code friend info dài\n"
       "2. 保存 (lưu thành công vì lúc lưu code chưa được replace)\n3. Gửi cho U3\n"
       "4. Quan sát LINE của U3\n5. Mở màn /basic/error-list",
       "Nội dung sau replace vượt 5.000 ký tự",
       "- U3 KHÔNG nhận được tin (LINE trả lỗi vượt giới hạn)\n"
       "- Màn /basic/error-list ghi nhận bản ghi lỗi tương ứng, nêu được template và friend bị lỗi",
       note="Nguồn: Template type text r35. Spec KHÔNG mô tả hành vi khi nội dung sau replace vượt "
            "giới hạn → xem MT-22."),

    # ═════════════ 16. Text — PDF & shorten URL ═════════════
    tc("Text — PDF & shorten URL", "MEDIA-001", "Normal",
       "Upload PDF ≤10MB bằng nút chọn file hoặc kéo-thả → upload thành công, hiện preview",
       TXT,
       "1. Bấm icon「PDFアップロード」→ quan sát giao diện khi chưa có file\n"
       "2. Bấm nút upload → chọn file PDF 0,5MB → quan sát\n3. Đóng popup, mở lại → kéo-thả file PDF 9MB vào\n"
       "4. Quan sát giao diện sau khi đã có file",
       "PDF 0,5MB và PDF 9MB",
       "- Cả 2 cách (chọn file và kéo-thả) đều upload thành công và hiện preview file\n"
       "- Sau khi đã có file: giao diện KHÔNG còn nút upload nữa\n"
       "- Kéo file thứ 2 vào khi đã có file → KHÔNG upload được thêm",
       note="Nguồn: Template type text r36-r43. Gộp 2 cách upload vì CÙNG 1 kết quả mong đợi."),

    tc("Text — PDF & shorten URL", "MEDIA-001", "Abnormal",
       "Upload file KHÔNG phải PDF → bị chặn ngay ở popup chọn file",
       TXT,
       "1. Bấm icon「PDFアップロード」→ bấm nút upload\n"
       "2. Ở hộp thoại chọn file, quan sát các loại file được liệt kê\n3. Thử chọn file .docx / .png",
       "file .docx, .png",
       "- Hộp thoại chọn file CHỈ liệt kê file PDF; file loại khác bị lọc không hiện ra\n"
       "- Không upload được file không phải PDF",
       note="Nguồn: Template type text r44 (「chặn luôn ko cho hiển thị trong popup chọn」)."),

    tc("Text — PDF & shorten URL", "MEDIA-001", "Boundary",
       "Upload PDF > 10MB → báo lỗi ファイルが大きすぎます。10MB以下pdfファイルのみがアップロードできます。",
       TXT,
       "1. Bấm icon「PDFアップロード」→ chọn file PDF 12MB\n2. Quan sát thông báo lỗi\n"
       "3. Thử lại với file PDF đúng 10MB",
       "PDF 12MB và PDF 10MB",
       "- File 12MB: hiện msg lỗi chính xác "
       "「ファイルが大きすぎます。10MB以下pdfファイルのみがアップロードできます。」, không upload\n"
       "- File đúng 10MB: upload thành công",
       note="Nguồn: Template type text r42-r45."),

    tc("Text — PDF & shorten URL", "MEDIA-001", "Normal",
       "Nút「メッセージに挿入」chèn link PDF vào nội dung; user mở được file trên LINE",
       TXT,
       "1. Upload 1 file PDF thành công\n2. Bấm「メッセージに挿入」\n3. Quan sát chuỗi trong textarea\n"
       "4. 保存 → gửi test cho U1\n5. Trên LINE bấm vào link PDF",
       "PDF「利用規約.pdf」",
       "- Chèn được link của file PDF vừa upload vào nội dung text\n"
       "- User bấm link trên LINE → mở/tải được đúng file PDF",
       note="Nguồn: Template type text r46, r48. RULE-06: đi tới output cuối là file mở trên LINE."),

    tc("Text — PDF & shorten URL", "STATE-CLEAN-001", "Normal",
       "Đóng popup PDF rồi mở lại → file đã tải trước đó bị clear",
       TXT,
       "1. Upload 1 file PDF thành công\n2. Bấm đóng popup (không bấm 挿入)\n"
       "3. Bấm lại icon「PDF」→ quan sát popup",
       "PDF đã upload rồi đóng popup",
       "- Popup đóng lại bình thường\n- Mở lại popup: đã CLEAR file cũ, trở về trạng thái chưa có file",
       note="Nguồn: Template type text r47."),

    tc("Text — PDF & shorten URL", "REG-URL-001", "Normal",
       "Checkbox URL gốc mặc định KHÔNG tick → URL ngoài hệ thống được shorten khi gửi",
       TXT + "\n- Nội dung text chứa 1 URL ngoài hệ thống (https://example.com/campaign)",
       "1. Quan sát trạng thái mặc định của checkbox URL gốc\n2. Giữ nguyên (không tick) → 保存\n"
       "3. Gửi test cho U1\n4. Quan sát URL trong tin trên LINE",
       "URL ngoài: https://example.com/campaign, checkbox không tick",
       "- Checkbox mặc định KHÔNG được tick\n"
       "- Tin trên LINE hiện URL đã được SHORTEN (dạng short link của hệ thống), không phải URL gốc\n"
       "- Bấm short link vẫn mở đúng trang đích",
       note="Nguồn: Template type text r49-r51. ⚠ Spec Field Matrix #9 ghi「Checked=0, Unchecked=1」"
            "và tự đánh dấu [Trung bình] → TC này lấp Gap, xem MT-08."),

    tc("Text — PDF & shorten URL", "REG-URL-001", "Normal",
       "Tick checkbox URL gốc + URL KHÔNG setting action → gửi đi giữ URL gốc, không shorten",
       TXT + "\n- Nội dung text chứa 1 URL ngoài hệ thống, KHÔNG setting action cho URL đó",
       "1. Tick checkbox URL gốc → 保存\n2. Vào lại màn edit kiểm tra checkbox vẫn được tick\n"
       "3. Gửi test cho U1 → quan sát URL trong tin trên LINE",
       "URL ngoài, tick checkbox, không setting action",
       "- Trạng thái tick được lưu lại (vào edit vẫn thấy tick)\n"
       "- Tin trên LINE hiện ĐÚNG URL gốc, KHÔNG bị shorten",
       note="Nguồn: Template type text r52."),

    tc("Text — PDF & shorten URL", "REG-URL-001", "Abnormal",
       "Tick checkbox URL gốc nhưng URL CÓ setting action → vẫn bị shorten để hệ thống bắt action",
       TXT + "\n- Nội dung text chứa 1 URL ngoài hệ thống ĐÃ setting action khi click",
       "1. Setting action cho URL ở tab「URL表示期限・アクション設定」\n2. Tick checkbox URL gốc → 保存\n"
       "3. Gửi test cho U1 → quan sát URL trong tin trên LINE\n4. Bấm URL và kiểm tra action có chạy không",
       "URL ngoài + có setting action + tick checkbox URL gốc",
       "- Tin trên LINE VẪN hiện short link (bị shorten dù đã tick URL gốc)\n"
       "- Bấm link → mở đúng trang đích VÀ action đã setting được thực thi cho user",
       note="Nguồn: Template type text r53 (「vẫn shorten để hệ thống send action」). "
            "Rule action-thắng-checkbox KHÔNG có trong spec → xem MT-08."),

    tc("Text — PDF & shorten URL", "REG-URL-001", "Normal",
       "URL TRONG hệ thống (link tool) → tick hay không tick checkbox đều giữ nguyên link",
       TXT + "\n- Nội dung text chứa link trong hệ thống (link form của bot A)",
       "1. Không tick checkbox → 保存 → gửi test → quan sát URL trên LINE\n"
       "2. Tick checkbox → 保存 → gửi test → quan sát URL trên LINE",
       "link form nội bộ; 2 trạng thái checkbox",
       "- Cả 2 lần: URL trong tin trên LINE GIỮ NGUYÊN như đã nhập, không đổi dạng\n"
       "- Bấm link vẫn mở đúng trang form",
       note="Nguồn: Template type text r50."),

    tc("Text — PDF & shorten URL", "REG-URL-001", "Normal",
       "Template text chứa link file / media / ảnh / video → tạo, sửa, copy, gửi đều bình thường",
       TXT + "\n- Có URL của: trang web thường, file video trực tiếp, file ảnh trực tiếp, file tài liệu",
       "1. Tạo template text chứa lần lượt 4 loại URL trên (mỗi loại 1 template) → 保存\n"
       "2. Vào edit từng template, kiểm tra nội dung và tab URL\n3. Copy từng template\n"
       "4. Gửi test từng template cho U1 và bấm link trên LINE",
       "4 loại URL, gồm URL video lỗi của KH: "
       "https://storage.googleapis.com/msgsndr/.../media/...",
       "- Cả 4 loại URL đều lưu được, không lỗi khi lấy metadata\n"
       "- Edit và copy đều giữ đúng URL\n- User bấm link trên LINE mở/tải được nội dung tương ứng",
       note="Nguồn: Task nhỏ+ check Bug Kh r36-r42 (khối「Check tạo mới template có chứa link」, "
            "kèm URL lỗi thực tế của khách hàng). ⚠ Corpus KHÔNG ghi Expect Result cho khối này → "
            "kết quả mong đợi ở đây là SUY LUẬN CỦA AI, cần Leader xác nhận."),

    # ═════════════ 17. URL redirect — preview & metadata ═════════════
    tc("URL redirect — preview & metadata", "REG-URL-001", "Normal",
       "Detect URL: có bao nhiêu URL ngoài hệ thống trong nội dung thì hiện ra hết; URL nội bộ KHÔNG detect",
       TXT + "\n- Nội dung text chứa 3 URL ngoài hệ thống và 1 link form nội bộ của bot A",
       "1. Nhập nội dung có 3 URL ngoài + 1 link nội bộ → 保存\n"
       "2. Chuyển sang tab「URL表示期限・アクション設定」\n3. Đếm và đối chiếu danh sách URL được detect",
       "3 URL ngoài + 1 URL nội bộ",
       "- Tab hiện đủ 3 URL ngoài hệ thống\n- Link nội bộ KHÔNG xuất hiện trong danh sách detect",
       note="Nguồn: Template type text r63-r65. Spec BR-09 `detectUrlInMessageTextV2`."),

    tc("URL redirect — preview & metadata", "UI-001", "Normal",
       "Popup setting hiển thị URL trên LINE: text preview default lấy description của link",
       URLT,
       "1. Mở template TU → tab「URL表示期限・アクション設定」\n"
       "2. Bấm nút setting hiển thị URL trên màn hình LINE\n3. Quan sát popup và phần 1 (text preview)",
       "URL https://example.com/campaign có OGP description",
       "- Popup setting mở ra đúng design\n"
       "- Ô text preview được tự fill sẵn bằng description của link (OGP)",
       note="Nguồn: Template type text r66-r68."),

    tc("URL redirect — preview & metadata", "UI-INPUT-001", "Abnormal",
       "Text preview URL: để rỗng → required; nhập > 25 ký tự → báo lỗi",
       URLT,
       "1. Mở popup setting hiển thị URL\n2. Xóa trắng ô text preview → lưu → quan sát\n"
       "3. Nhập 26 ký tự → lưu → quan sát\n4. Nhập đúng 25 ký tự → lưu → quan sát",
       "rỗng / 26 ký tự / 25 ký tự",
       "- Rỗng: báo lỗi bắt buộc nhập, không lưu\n- 26 ký tự: báo lỗi vượt giới hạn, không lưu\n"
       "- 25 ký tự: lưu thành công",
       note="Nguồn: Template type text r69-r70. Giới hạn 25 ký tự KHÔNG có trong spec "
            "(spec chỉ liệt kê `meta_title` varchar(255)) → xem MT-23."),

    tc("URL redirect — preview & metadata", "MEDIA-IMG-001", "Normal",
       "Ảnh preview URL: default lấy ảnh của link; đổi ảnh khác thì LINE hiện ảnh mới",
       URLT,
       "1. Mở popup setting hiển thị URL → quan sát ảnh preview default\n"
       "2. Bấm nút update ảnh → chọn ảnh khác → lưu\n3. Gửi test cho U1 → quan sát khối preview trên LINE",
       "Ảnh mới 1200x630px",
       "- Ảnh preview default = ảnh OGP của link\n"
       "- Sau khi đổi: lưu thành công và khối preview URL trên LINE hiện ẢNH MỚI",
       note="Nguồn: Template type text r72-r73."),

    tc("URL redirect — preview & metadata", "MEDIA-IMG-001", "Normal",
       "Xóa ảnh preview URL rồi lưu → hệ thống lấy lại ảnh default của link",
       URLT,
       "1. Mở popup setting hiển thị URL\n2. Bấm nút xóa ảnh (để không có ảnh nào) → lưu\n"
       "3. Vào lại màn edit → quan sát ảnh preview\n4. Gửi test cho U1 → quan sát khối preview trên LINE",
       "Xóa ảnh, lưu khi không có ảnh",
       "- Sau khi lưu, hệ thống GET lại ảnh default của link và hiển thị\n"
       "- Vào edit cũng hiện ảnh default của link\n- LINE hiện khối preview với ảnh default",
       note="Nguồn: Template type text r74."),

    tc("URL redirect — preview & metadata", "MSG-004", "Normal",
       "Setting chung cho nhiều URL: option 表示する → LINE hiện đủ Title / Description / ảnh preview",
       URLT + "\n- Template TU2 chứa 2 URL ngoài hệ thống và 1 URL trong hệ thống",
       "1. Mở TU2 → tab URL → phần setting chung cho danh sách URL\n"
       "2. Quan sát option default\n3. Chọn「表示する」→ lưu\n4. Gửi test cho U1\n"
       "5. Quan sát tin trên LINE",
       "3 URL, option 表示する",
       "- Option default là「表示する」(có hiện preview)\n"
       "- Tin trên LINE hiện khối preview URL đầy đủ: Title, Description và ảnh preview",
       note="Nguồn: Preview URL r3-r4."),

    tc("URL redirect — preview & metadata", "MSG-004", "Normal",
       "Setting chung: option 表示しない → web hiện text 表示しない, LINE KHÔNG hiện khối preview",
       URLT + "\n- Template TU2 chứa 2 URL ngoài hệ thống",
       "1. Mở TU2 → tab URL → chọn option「表示しない」cho setting chung → lưu\n"
       "2. Quan sát text hiển thị bên web\n3. Gửi test cho U1 → quan sát tin trên LINE",
       "2 URL, option 表示しない",
       "- Bên web hiện text「表示しない」\n"
       "- Tin trên LINE KHÔNG hiện Title / Description / ảnh preview của URL (chỉ có link)",
       note="Nguồn: Preview URL r5."),

    tc("URL redirect — preview & metadata", "STATE-001", "Normal",
       "Đổi option preview URL (có ⇄ không) rồi reload/gửi lại → trạng thái lưu đúng, LINE hiện đúng",
       URLT + "\n- Template TU2 đang set「表示する」",
       "1. Đổi từ「表示する」sang「表示しない」→ lưu → reload màn hình → quan sát option\n"
       "2. Gửi test → quan sát tin trên LINE\n3. Đổi ngược lại sang「表示する」→ lưu → reload → gửi test",
       "2 chiều đổi option",
       "- Sau mỗi lần lưu + reload, option giữ đúng giá trị vừa chọn\n"
       "- Tin trên LINE khớp với option đang set (có / không có khối preview)",
       note="Nguồn: Preview URL r6-r8."),

    tc("URL redirect — preview & metadata", "MSG-004", "Normal",
       "Setting riêng cho 1 URL (URL設定を編集) → option preview CHỈ áp cho URL đó",
       URLT + "\n- Template TU3 chứa 2 URL ngoài hệ thống: A và B",
       "1. Mở TU3 → tab URL → bấm「URL設定を編集」ở URL A\n2. Quan sát màn setting và option default\n"
       "3. Chọn「表示しない」cho A, giữ「表示する」cho B → lưu → reload\n"
       "4. Gửi test cho U1 → quan sát tin trên LINE",
       "URL A =「表示しない」, URL B =「表示する」",
       "- Bấm「URL設定を編集」mở màn setting riêng, option default là「表示する」\n"
       "- Tin trên LINE: khối preview CHỈ hiện cho URL B; URL A không có khối preview\n"
       "- Reload màn hình vẫn giữ đúng setting của từng URL",
       note="Nguồn: Preview URL r10-r17."),

    tc("URL redirect — preview & metadata", "CONC-001", "Abnormal",
       "Double click nút lưu setting URL → chỉ tạo 1 bản ghi template_url_redirect",
       URLT,
       "1. Mở popup setting hiển thị URL → nhập text preview\n2. Double click nhanh nút lưu\n"
       "3. Reload màn hình và kiểm tra danh sách URL redirect",
       "double click",
       "- Chỉ tạo ĐÚNG 1 bản ghi setting cho URL đó\n- Danh sách URL redirect không có dòng trùng lặp",
       note="Nguồn: Preview URL r32."),

    tc("URL redirect — preview & metadata", "DATA-REF-001", "Normal",
       "Chỉ tạo bản ghi template_url_redirect khi CÓ setting URL redirect",
       TXT,
       "1. Tạo template text có 1 URL, KHÔNG setting url redirect → 保存 → kiểm tra tab URL\n"
       "2. Tạo template text có 1 URL, CÓ setting url redirect → 保存 → kiểm tra tab URL\n"
       "3. Lặp lại 2 bước trên với template có NHIỀU URL",
       "1 URL và nhiều URL; có / không setting",
       "- Không setting: KHÔNG tạo bản ghi `template_url_redirect` nào\n"
       "- Có setting: tạo bản ghi `template_url_redirect` và lưu cả cột `url` (URL gốc)\n"
       "- Kết quả giống nhau với template 1 URL và nhiều URL",
       note="Nguồn: Template type text r84-r87. Cột `url` được thêm khi fix Bug #32109."),

    tc("URL redirect — preview & metadata", "REG-URL-001", "Normal",
       "Get metadata đúng với nhiều dạng URL thực tế (SNS, short link, Google Form, YouTube, ...)",
       TXT,
       "1. Tạo template text lần lượt chứa từng URL trong danh sách dữ liệu test\n"
       "2. Với mỗi URL: mở tab URL, quan sát Title / Description / ảnh preview lấy về\n"
       "3. Gửi test và đối chiếu khối preview trên LINE",
       "18 URL thực tế: instagram.com/kpp_saiyo · facebook.com · instagram.com/p/... · s.lmes.jp/l/... · "
       "bit.ly/aiko_insta · bit.ly/aiko-fb · facebook.com/pasokon.hotaka · iabe.jp/2HBsihS · "
       "atmix.co/5manget · starfx.me/lp/start · gforex.asia/vip/74814 · lin.ee/yF1GATo · "
       "docs.google.com/forms/... · youtube.com/embed/... · twitter.com/tsuyopon_xyz · "
       "youtube.com/watch?v=... · police.pref.nagasaki.jp/recruit",
       "- Mỗi URL đều lấy được metadata (hoặc fallback hợp lý nếu site không có OGP), KHÔNG lỗi hệ thống\n"
       "- Khối preview trên LINE khớp metadata đã lấy",
       note="Nguồn: Template type text r125-r142 (danh sách URL thật dùng để verify sửa logic get "
            "metadata). Gộp 18 URL vì CÙNG 1 kết quả mong đợi; liệt kê đủ ở cột Dữ liệu test."),

    # ═════════════ 18. URL redirect — hết hạn & action ═════════════
    tc("URL redirect — hết hạn & action", "FUNC-DATE-001", "Normal",
       "Không setting giới hạn (利用しない) → bỏ modal setting ngoài thời gian hiển thị, action chạy theo setting số lần",
       URLT,
       "1. Mở template TU → tab URL → phần「URL表示期限」chọn option「利用しない」→ lưu\n"
       "2. Gửi test cho U1\n3. U1 bấm URL trên LINE\n4. Quan sát action nhận được",
       "option「利用しない」",
       "- Màn setting KHÔNG hiện phần cấu hình「ngoài thời gian hiển thị」\n"
       "- U1 bấm URL → mở đúng trang đích và nhận action theo setting 1 lần / nhiều lần",
       note="Nguồn: Preview URL r18 + Template type text r143."),

    tc("URL redirect — hết hạn & action", "FUNC-DATE-001", "Normal",
       "Setting hết hạn kiểu NGÀY GIỜ cố định → url_expired_time = đúng giờ đã set",
       URLT,
       "1. Mở tab URL của TU → chọn「利用する」→ chọn kiểu hết hạn = ngày giờ chỉ định\n"
       "2. Set thời điểm hết hạn = hôm nay + 1 ngày, 10:00 → lưu\n"
       "3. Kiểm tra `template_url_redirect.url_expired_time`\n4. Gửi test và bấm URL TRƯỚC hạn",
       "Hết hạn = ngày mai 10:00",
       "- Màn setting hiện thêm phần cấu hình hành vi khi ngoài thời gian hiển thị\n"
       "- `url_expired_time` = đúng ngày giờ đã set\n- Bấm URL trước hạn → mở đúng trang đích",
       note="Nguồn: Preview URL r19-r20 + Template type text r144."),

    tc("URL redirect — hết hạn & action", "FUNC-DATE-001", "Normal",
       "Setting hết hạn kiểu DURATION → hạn = ngày tạo short link + số ngày, giờ = after_day_time",
       URLT,
       "1. Mở tab URL của TU → chọn kiểu hết hạn = duration\n"
       "2. Set「1 ngày 00:01」→ lưu\n3. Gửi tin cho U1 lúc 12:00 ngày 15\n"
       "4. Kiểm tra `url_shorten.created_at`, `template_url_redirect.duration_from_delivery` và "
       "`after_day_time`\n5. Bấm URL lúc 23:00 ngày 15 → quan sát\n6. Bấm URL lúc 00:05 ngày 16 → quan sát",
       "duration = 1 ngày, giờ = 00:01; gửi lúc 12:00 ngày 15",
       "- Ngày hết hạn = `url_shorten.created_at` + `duration_from_delivery`, giờ hết hạn = `after_day_time`\n"
       "- Với ví dụ: hết hạn lúc 00:01 NGÀY 16 (không phải 1 phút sau khi gửi)\n"
       "- Bấm 23:00 ngày 15: còn hạn → mở trang đích\n- Bấm 00:05 ngày 16: đã hết hạn → xử lý theo setting hết hạn",
       note="Nguồn: Task nhỏ+ check Bug Kh r11 (sửa lại logic duration: trước đó「0 ngày 00:01」nghĩa là "
            "1 phút sau khi gửi) + Template type text r145. Spec KHÔNG mô tả công thức này → xem MT-24."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "URL đã hết hạn + setting HIỆN TEXT → user thấy đúng text đã setting",
       URLT + "\n- TU đã set hết hạn ở thời điểm quá khứ, chọn hành vi hết hạn = hiện text",
       "1. Set nội dung text khi hết hạn =「このURLの有効期限が切れました」→ lưu\n"
       "2. Gửi tin cho U1\n3. Chờ qua thời điểm hết hạn\n4. U1 bấm URL trên LINE",
       "text hết hạn =「このURLの有効期限が切れました」",
       "- U1 bấm URL sau hạn → hiện ĐÚNG text đã setting, KHÔNG mở trang đích",
       note="Nguồn: Preview URL r23 + Template type text r147."),

    tc("URL redirect — hết hạn & action", "REG-URL-001", "Normal",
       "URL đã hết hạn + setting REDIRECT sang URL khác → user được chuyển sang URL mới",
       URLT + "\n- TU đã set hết hạn ở thời điểm quá khứ, chọn hành vi hết hạn = redirect",
       "1. Set `url_redirect` = https://example.com/expired → lưu\n2. Gửi tin cho U1\n"
       "3. Chờ qua thời điểm hết hạn\n4. U1 bấm URL trên LINE",
       "url_redirect = https://example.com/expired",
       "- U1 bấm URL sau hạn → được chuyển hướng sang https://example.com/expired\n"
       "- KHÔNG mở trang đích ban đầu",
       note="Nguồn: Preview URL r24 + Template type text r148."),

    tc("URL redirect — hết hạn & action", "FUNC-001", "Normal",
       "Action khi CÒN hạn: gửi action_id, url_shorten.action = 1",
       URLT + "\n- TU set hết hạn tương lai, action khi click = gắn tag T",
       "1. Setting action khi click URL (còn hạn) = gắn tag T → lưu\n2. Gửi tin cho U1\n"
       "3. U1 bấm URL khi còn hạn\n4. Kiểm tra tag của U1 và cột `url_shorten.action`",
       "action còn hạn = gắn tag T",
       "- U1 mở được trang đích\n- U1 được gắn tag T (action `action_id` chạy)\n"
       "- `url_shorten.action` được update = 1",
       note="Nguồn: Preview URL r25 + Template type text r149."),

    tc("URL redirect — hết hạn & action", "FUNC-001", "Normal",
       "Action khi HẾT hạn: gửi out_time_action_id, url_shorten.action_time_out = 1",
       URLT + "\n- TU đã hết hạn, action khi hết hạn = gửi template text TX",
       "1. Setting action khi hết hạn = gửi template TX → lưu\n2. Gửi tin cho U1\n"
       "3. Chờ qua hạn → U1 bấm URL\n4. Quan sát tin U1 nhận và cột `url_shorten.action_time_out`",
       "action hết hạn = gửi template TX",
       "- U1 nhận được tin của template TX (action `out_time_action_id` chạy)\n"
       "- `url_shorten.action_time_out` được update = 1\n- KHÔNG chạy action của nhánh còn hạn",
       note="Nguồn: Preview URL r26 + Template type text r150."),

    tc("URL redirect — hết hạn & action", "FUNC-001", "Normal",
       "Setting action 1 LẦN: click lần 2 trở đi không gửi action nữa (cả nhánh còn hạn và hết hạn)",
       URLT + "\n- TU set action 1 lần (`number_action_url_redirect` = 1) cho cả 2 nhánh",
       "1. Set「一度のみ稼働」→ lưu → gửi tin cho U1\n2. U1 bấm URL lần 1 (còn hạn) → quan sát action\n"
       "3. U1 bấm URL lần 2 (còn hạn) → quan sát action + cột `url_shorten.action`\n"
       "4. Chờ qua hạn, U1 bấm lần 1 → quan sát action\n"
       "5. U1 bấm lần 2 sau hạn → quan sát + cột `action_time_out`",
       "action 1 lần, mỗi nhánh bấm 2 lần",
       "- Còn hạn: lần 1 có action (`action` = 0 → 1); lần 2 KHÔNG có action nữa (`action` = 1)\n"
       "- Hết hạn: lần 1 có action (`action_time_out` = 0 → 1); lần 2 KHÔNG có action "
       "(`action_time_out` = 1)\n- Trang đích/text hết hạn vẫn mở bình thường ở mọi lần bấm",
       note="Nguồn: Template type text r151-r152. Spec Field Matrix #10 "
            "(`number_action_url_redirect`: 1 =一度のみ, >1 =何度でも)."),

    tc("URL redirect — hết hạn & action", "FUNC-001", "Normal",
       "Setting action NHIỀU LẦN: mỗi lần click đều gửi action (cả nhánh còn hạn và hết hạn)",
       URLT + "\n- TU set action nhiều lần (「何度でも稼働」)",
       "1. Set「何度でも稼働」→ lưu → gửi tin cho U1\n2. U1 bấm URL 3 lần khi còn hạn → đếm action nhận được\n"
       "3. Chờ qua hạn → U1 bấm URL 3 lần → đếm action nhận được",
       "action nhiều lần, mỗi nhánh bấm 3 lần",
       "- Còn hạn: cả 3 lần bấm đều gửi action cho user\n- Hết hạn: cả 3 lần bấm đều gửi action hết hạn",
       note="Nguồn: Template type text r153-r154 + Preview URL r19."),

    tc("URL redirect — hết hạn & action", "FUNC-001", "Normal",
       "Setting số lần bấm của template button KHÔNG áp cho action mở URL / LINE URL scheme",
       ADM + "\n- Template button standard TB có 1 panel, 1 nút\n"
             "- Đã set「選択肢のタップ回数」= giới hạn 1 lần",
       "1. Set nút chỉ có multi action → gửi cho U1 → bấm nút 2 lần → quan sát action\n"
       "2. Đổi nút sang từng loại friend action dưới đây, mỗi lần gửi lại và bấm 2 lần: "
       "open url, open link LME, friend send text, open profile LOA, open LOA add friend, "
       "call số điện thoại, open mail\n"
       "3. Đổi nút sang từng LINE URL scheme: share account LINE, share text, open camera, "
       "open camera roll, share location — mỗi lần bấm 2 lần\n"
       "4. Đổi nút thành KHÔNG có action nào → bấm 2 lần",
       "1 multi action + 7 friend action + 5 LINE URL scheme + 1 trường hợp không action; mỗi loại bấm 2 lần",
       "- CÓ áp giới hạn số lần bấm: multi action, và trường hợp nút không set action nào "
       "(lần 2 bị chặn theo setting)\n"
       "- KHÔNG áp giới hạn: cả 7 friend action và 5 LINE URL scheme "
       "(bấm lần 2 vẫn mở URL/scheme bình thường)",
       note="Nguồn: Task nhỏ+ check Bug Kh r19-r33 (bảng đối chiếu「action nào apply với setting số lần "
            "bấm」). Rule này KHÔNG có trong spec → xem MT-25."),

    tc("URL redirect — hết hạn & action", "COMPAT-LEGACY-001", "Normal",
       "Template CŨ chứa URL: gửi được bình thường, preview lấy theo template_url_redirect",
       ADM + "\n- Có template text CŨ (tạo trước Bug #32109) chứa 1 URL, `template_url_redirect.url` = NULL\n"
             "- URL gốc CHƯA bị xóa khỏi bảng url",
       "1. Gửi template cũ đó cho U1 (trước khi chạy recover)\n2. Quan sát khối preview trên LINE\n"
       "3. Mở màn edit template và quan sát preview",
       "template cũ, `url` = NULL, URL chưa bị xóa",
       "- Gửi được template bình thường\n"
       "- Khối preview phía user hiện theo data trong `template_url_redirect` (metadata đã cache)\n"
       "- Màn edit cũng hiện preview khớp",
       note="Nguồn: Template type text r77."),

    tc("URL redirect — hết hạn & action", "COMPAT-LEGACY-001", "Abnormal",
       "Template CŨ chứa URL đã BỊ XÓA khỏi bảng url → gửi được nhưng preview lấy theo metadata của url",
       ADM + "\n- Template text cũ chứa 1 URL, `template_url_redirect.url` = NULL\n"
             "- Bản ghi URL gốc ĐÃ bị xóa khỏi bảng `url`",
       "1. Gửi template đó cho U1\n2. Quan sát khối preview trên LINE\n"
       "3. Kiểm tra bảng `url` và cột `url_id` của `template_url_redirect`\n"
       "4. Mở màn edit template và quan sát preview",
       "template cũ, URL gốc đã bị xóa",
       "- Vẫn gửi được template\n- Hệ thống TẠO bản ghi mới ở bảng `url` nhưng KHÔNG update `url_id` "
       "vào `template_url_redirect`\n"
       "- Preview phía user hiện theo metadata của bảng `url` (không phải setting đã lưu)\n"
       "- Màn edit cũng hiện preview theo url → admin phải vào edit lại mới đúng",
       note="Nguồn: Template type text r78 — chính là hiện tượng của Bug #32109 trước khi recover. "
            "Đây là hành vi LỖI được ghi nhận, dùng để đối chứng với TC sau recover."),

    tc("URL redirect — hết hạn & action", "DATA-MIG-001", "Normal",
       "Job recover template_url_redirect: URL còn tồn tại → điền được cột url; URL đã xóa → url = NULL",
       ADM + "\n- Có 2 template cũ: TA (URL còn trong bảng url), TB (URL đã bị xóa)\n"
             "- Job recover `template_url_redirect` chưa chạy",
       "1. Chạy job recover cho `template_url_redirect`\n2. Kiểm tra cột `url` của bản ghi thuộc TA\n"
       "3. Kiểm tra cột `url` của bản ghi thuộc TB",
       "TA: URL còn · TB: URL đã xóa",
       "- TA: cột `url` được điền đúng URL gốc\n- TB: cột `url` = NULL",
       env="PRODUCTION",
       note="Nguồn: Template type text r79-r80. RULE-08: job recover data phải xác nhận trên PRODUCTION."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "SAU recover: gửi template cũ qua web / job / app → preview lấy theo template_url_redirect",
       ADM + "\n- Đã chạy job recover; template TA có `template_url_redirect.url` đã điền",
       "1. Gửi TA từ web (chat 1:1 / send test) cho U1 → quan sát preview trên LINE\n"
       "2. Gửi TA bằng job (broadcast / scenario) cho nhiều user → quan sát preview\n"
       "3. Gửi TA từ app mobile → quan sát preview",
       "3 đường gửi: web, job, app",
       "- Cả 3 đường: preview phía user hiện theo data trong `template_url_redirect` (đúng setting)\n"
       "- Khi gửi job cho NHIỀU user, TẤT CẢ user đều thấy preview đúng (không chỉ user đầu tiên)",
       note="Nguồn: Template type text r81-r83. ⚠ TC gốc r82 có note「Khi send nhiều user thì chỉ có 1 "
            "user send đầu tiên...」→ nhánh job nhiều user là điểm rủi ro, xem MT-26."),

    tc("URL redirect — hết hạn & action", "DATA-REF-001", "Normal",
       "Edit template có URL đã bị xóa → save lại thì tạo url mới và update url_id",
       ADM + "\n- Template TB có URL đã bị xóa khỏi bảng `url`",
       "1. Mở màn edit TB → quan sát preview\n2. Bấm 保存 (không sửa gì)\n"
       "3. Kiểm tra bảng `url` và cột `url_id` của `template_url_redirect`",
       "TB có URL đã xóa",
       "- Màn edit hiện preview theo `template_url_redirect`\n"
       "- Sau khi 保存: tạo thêm 1 bản ghi `url` mới và `url_id` của `template_url_redirect` "
       "được update sang id mới",
       note="Nguồn: Template type text r88-r89."),

    tc("URL redirect — hết hạn & action", "DATA-REF-001", "Abnormal",
       "Cùng 1 URL dùng ở nhiều template, URL bị xóa → edit 1 template CHỈ update url_id của template đó",
       ADM + "\n- URL X được setting trong 3 template T1, T2, T3\n- URL X đã bị xóa khỏi bảng `url`",
       "1. Mở edit T1 → 保存\n2. Kiểm tra `url_id` của bản ghi `template_url_redirect` thuộc T1, T2, T3\n"
       "3. Gửi T2 cho U1 rồi kiểm tra lại `url_id` của T2",
       "URL X dùng ở 3 template",
       "- Sau khi 保存 T1: CHỈ `url_id` của T1 được update sang url mới\n"
       "- `url_id` của T2 và T3 vẫn là id của URL đã xóa\n"
       "- T2 chỉ được update `url_id` khi ADMIN edit setting hoặc khi hệ thống GỬI template đó",
       note="Nguồn: Template type text r90."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "Gửi template chứa NHIỀU URL trong đó có URL đã xóa → tạo url mới cho URL bị xóa, preview đúng",
       ADM + "\n- Template TM chứa 3 URL: 2 URL còn tồn tại, 1 URL đã bị xóa; cả 3 đều có setting redirect",
       "1. Gửi TM từ web cho U1 → quan sát 3 khối preview trên LINE\n"
       "2. Kiểm tra bảng `url` và `url_id` của 3 bản ghi `template_url_redirect`\n"
       "3. Gửi TM bằng job (broadcast) → quan sát preview và DB",
       "3 URL: 2 còn, 1 đã xóa",
       "- Cả 3 khối preview trên LINE hiện đúng Title / Description / ảnh theo `template_url_redirect`\n"
       "- Hệ thống tạo url mới cho URL bị xóa và update `url_id` tương ứng\n"
       "- Kết quả giống nhau ở cả web và job",
       note="Nguồn: Template type text r117-r118. ⚠ TC gốc r118 note「bên job bị cache -> khi send bị "
            "hiện preview Not found => sửa cache thời gian 1p」→ rủi ro cache, xem MT-26."),

    tc("URL redirect — hết hạn & action", "DATA-BACKUP-001", "Abnormal",
       "Copy / Backup template có URL → tạo bản ghi mới có cột url, nhưng setting url redirect KHÔNG được backup",
       ADM + "\n- Template TA có 1 URL đã setting redirect + action",
       "1. Copy TA → mở bản copy, kiểm tra tab URL và bảng `template_url_redirect`\n"
       "2. Chạy backup sang bot B → mở template tương ứng ở bot B, kiểm tra tab URL\n"
       "3. Với trường hợp URL đã bị xóa, lặp lại bước 1-2",
       "TA có URL còn tồn tại và TB có URL đã xóa",
       "- Copy: tạo bản ghi `template_url_redirect` MỚI có lưu cột `url`; nếu URL đã xóa thì `url_id` "
       "vẫn là id cũ, chỉ update khi edit hoặc gửi\n"
       "- Backup: backup được template và bảng `url`, nhưng SETTING url redirect (action, thời hạn) "
       "KHÔNG được backup sang bot B",
       note="Nguồn: Template type text r91-r94, r168, r176. Spec KHÔNG có mục backup cho FA-010 "
            "→ xem MT-11."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "URL KHÔNG setting redirect → preview lấy theo bảng url ở cả 4 đường gửi",
       ADM + "\n- Template TN chứa 1 URL ngoài hệ thống, KHÔNG setting url redirect",
       "1. Gửi TN qua web (chat 1:1) → quan sát preview trên LINE\n2. Gửi qua send test → quan sát\n"
       "3. Gửi qua job (broadcast) → quan sát\n4. Gửi từ app mobile → quan sát\n"
       "5. Lặp lại 4 bước với trường hợp URL đã bị xóa khỏi bảng `url`",
       "4 đường gửi × 2 trạng thái URL (còn / đã xóa)",
       "- Cả 8 lượt: preview phía user hiện theo data trong bảng `url`\n- Không lượt nào bị lỗi gửi tin",
       note="Nguồn: Template type text r95-r102. Gộp vì CÙNG 1 kết quả mong đợi."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "URL CÓ setting redirect + URL còn tồn tại → gửi 2 lần liên tiếp đều preview theo template_url_redirect",
       ADM + "\n- Template TA có URL còn tồn tại, đã setting redirect",
       "1. Gửi TA qua web lần 1 → quan sát preview; gửi lần 2 → quan sát\n"
       "2. Lặp lại qua send test (2 lần)\n3. Lặp lại qua job (2 lần)\n4. Gửi từ app mobile",
       "4 đường gửi, mỗi đường gửi 2 lần",
       "- Mọi lượt gửi: preview hiện theo data trong `template_url_redirect`\n"
       "- Lần gửi thứ 2 không bị đổi sang metadata của bảng `url`",
       note="Nguồn: Template type text r103-r109."),

    tc("URL redirect — hết hạn & action", "MSG-004", "Normal",
       "URL CÓ setting redirect + URL đã bị xóa → preview vẫn đúng, hệ thống tự tạo url mới và update url_id",
       ADM + "\n- Template TB có URL đã bị xóa, đã setting redirect",
       "1. Gửi TB qua web lần 1 → quan sát preview + kiểm tra bảng `url`, `url_id`\n2. Gửi lần 2 → quan sát\n"
       "3. Lặp lại qua send test (2 lần), qua job (2 lần), và từ app mobile",
       "4 đường gửi, mỗi đường gửi 2 lần; URL đã bị xóa",
       "- Mọi lượt gửi: preview phía user hiện ĐÚNG Title / Description / ảnh theo `template_url_redirect`\n"
       "- Hệ thống tạo url mới và update `url_id` vào `template_url_redirect`\n"
       "- Đây là hành vi SAU khi fix Bug #32109 (trước fix thì preview lấy theo bảng `url`)",
       note="Nguồn: Template type text r110-r116 (Bug #32109, 26/09/2025)."),

    tc("URL redirect — hết hạn & action", "REG-SHARED-001", "Normal",
       "Gửi URL trực tiếp ở chat 1:1 và trong action text → preview lấy theo bảng url",
       ADM + "\n- Chuẩn bị 1 URL ngoài hệ thống chưa từng dùng trong template",
       "1. Ở chat 1:1, gửi trực tiếp URL đó cho U1 → quan sát preview trên LINE\n"
       "2. Tạo action text có chứa URL đó, trigger qua web → quan sát preview\n"
       "3. Trigger action text đó qua job → quan sát preview",
       "3 đường: chat trực tiếp, action text web, action text job",
       "- Cả 3 đường đều gửi được URL cho user\n- Preview phía user hiện theo data trong bảng `url`",
       note="Nguồn: Template type text r121-r123. regression cho luồng URL ngoài template."),
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
for _r in S3:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
