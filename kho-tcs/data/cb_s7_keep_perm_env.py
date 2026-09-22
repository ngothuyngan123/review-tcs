# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 12-14.

S12 Setting giữ nguyên sau khi đổi (cấu hình bot cũ phải được kế thừa và chạy đúng với friend mới)
S13 Phân quyền & bảo mật
S14 Hồi quy & môi trường

Nguyên tắc phân biệt với nhóm 10-11: nhóm 10-11 kiểm DỮ LIỆU GẮN VỚI FRIEND CŨ phải bị
xóa; nhóm 12 kiểm CẤU HÌNH của bot phải được GIỮ và áp dụng đúng cho friend mới. Hai mặt
của cùng 1 thao tác nhưng kết quả mong đợi NGƯỢC nhau nên tách nhóm.

⚠️ MT-02 — quyền Staff với màn đổi LOA đang mâu thuẫn 3 nguồn, toàn nhóm 13 phụ thuộc.
"""
from _common import tc

KEEP = ("- Đã hoàn tất đổi LOA sang LOA mới và job dọn dữ liệu đã chạy xong\n"
        "- Trước khi đổi LOA đã ghi lại/chụp ảnh cấu hình của tính năng đang kiểm\n"
        "- Có ≥1 friend MỚI kết bạn với LOA mới để test phía LINE")
PRD = dict(env="PRODUCTION")
MT02 = "⚠️ MT-02 — quyền Staff chưa chốt. "

S12 = [
    # ═══════════════ 12. Setting giữ nguyên sau khi đổi ═══════════════
    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Chat 1:1 — hồ sơ người gửi và các trạng thái đối ứng được giữ nguyên, áp dụng cho friend mới",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥1 hồ sơ người gửi và ≥3 trạng thái đối ứng tự tạo",
       "1. Trước khi đổi LOA: chụp ảnh danh sách hồ sơ người gửi + danh sách trạng thái đối ứng\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào chat 1:1, mở cấu hình hồ sơ người gửi, đối chiếu với ảnh\n"
       "4. Mở danh sách trạng thái đối ứng, đối chiếu với ảnh\n"
       "5. Gửi tin cho friend MỚI bằng hồ sơ người gửi đó\n"
       "6. Kiểm tra trên LINE app của friend mới: tên và ảnh người gửi",
       "≥1 hồ sơ người gửi + ≥3 trạng thái đối ứng",
       "- Danh sách hồ sơ người gửi GIỮ NGUYÊN (đủ số lượng, đúng tên và ảnh)\n"
       "- Danh sách trạng thái đối ứng GIỮ NGUYÊN (đủ số lượng, đúng tên và màu)\n"
       "- Gửi tin bằng hồ sơ người gửi: friend mới nhận được tin với ĐÚNG tên + ảnh của hồ sơ đó trên LINE app\n"
       "- Không có hồ sơ / trạng thái nào bị mất hoặc đổi giá trị",
       group="UI",
       note="Nguồn: Change bot r198-r199 (TR=OK, stg=OK) + AddBot/Testcase r228-r229. "
            "MSG-USER-001 BẮT BUỘC khi tương tác friend LINE. RULE-06 — verify ở output cuối trên LINE app. "
            "RULE-08. Evidence: 2 ảnh cấu hình trước/sau + ảnh tin trên LINE app friend mới.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Tự động trả lời — từ khóa và cấu hình hành động giữ nguyên, friend mới gửi từ khóa thì bot trả lời đúng",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥2 quy tắc tự động trả lời với từ khóa và hành động khác nhau",
       "1. Trước khi đổi LOA: chụp ảnh danh sách quy tắc tự động trả lời + cấu hình hành động từng quy tắc\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào /basic/reply, đối chiếu danh sách quy tắc + từ khóa + hành động với ảnh\n"
       "4. Trên LINE app, cho friend MỚI gửi đúng từ khóa của quy tắc 1\n"
       "5. Quan sát tin bot trả lời + hành động được chạy (gắn tag / đổi rich menu...)\n"
       "6. Lặp lại với từ khóa của quy tắc 2",
       "≥2 quy tắc với 2 từ khóa và 2 loại hành động khác nhau",
       "- Danh sách quy tắc tự động trả lời GIỮ NGUYÊN đủ số lượng\n"
       "- Từ khóa và cấu hình hành động của từng quy tắc KHÔNG đổi\n"
       "- Friend mới gửi từ khóa 1: nhận ĐÚNG tin trả lời của quy tắc 1 và hành động chạy đúng\n"
       "- Friend mới gửi từ khóa 2: nhận đúng tin + hành động của quy tắc 2",
       group="UI",
       note="Nguồn: Change bot r200-r201 (TR=OK, stg=OK) + AddBot/Testcase r230-r231. "
            "MSG-USER-001. RULE-06 + RULE-08. Evidence: 2 ảnh danh sách quy tắc + ảnh tin trên LINE app + "
            "ảnh kết quả hành động (tag đã gắn).", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Rich Menu CŨ gán cho friend mới sau khi đổi LOA — gửi thành công và bấm chạy được hành động",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥1 rich menu đã cấu hình hành động",
       "1. Trước khi đổi LOA: chụp ảnh danh sách rich menu + cấu hình hành động\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào /basic/rich-menu, xác nhận rich menu CŨ còn trong danh sách\n"
       "4. Gán rich menu CŨ đó cho 1 friend MỚI\n"
       "5. Trên LINE app của friend mới: quan sát rich menu hiển thị\n"
       "6. Bấm vào từng ô của rich menu, quan sát hành động chạy",
       "≥1 rich menu cũ có ≥2 ô đã cấu hình hành động",
       "- Rich menu CŨ vẫn còn trong danh sách, cấu hình hành động không đổi\n"
       "- Gán cho friend mới: thành công, không lỗi\n"
       "- LINE app của friend mới: rich menu hiển thị đúng hình và đúng vùng bấm\n"
       "- Bấm từng ô: hành động chạy đúng như cấu hình (gắn tag / gửi tin / mở URL)",
       group="UI",
       note="Nguồn: Change bot r202 (TR=OK, stg=OK) + AddBot/Testcase r232 + Bill tiền/change_bot r29. "
            "⚠️ Rich menu phải được ĐĂNG KÝ LẠI với LINE channel mới — đây là điểm dễ lỗi nhất của nhóm này. "
            "MSG-USER-001 + INTG-LINE-001. RULE-06 + RULE-08. "
            "Evidence: ảnh danh sách rich menu + ảnh rich menu trên LINE app + ảnh kết quả hành động.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Rich Menu tạo MỚI sau khi đổi LOA — gửi được và bấm chạy được hành động",
       KEEP,
       "1. Sau khi đổi LOA, vào /basic/rich-menu, tạo 1 rich menu MỚI với ≥2 ô có hành động\n"
       "2. Gán rich menu mới cho 1 friend MỚI\n"
       "3. Trên LINE app của friend mới: quan sát rich menu hiển thị\n"
       "4. Bấm vào từng ô, quan sát hành động chạy\n"
       "5. Kiểm tra màn thống kê rich menu: số friend đang theo",
       "1 rich menu mới, 2 ô có hành động (gắn tag + gửi tin)",
       "- Tạo rich menu mới thành công, không lỗi khi đăng ký với LINE\n"
       "- Gán cho friend mới thành công\n"
       "- LINE app: rich menu mới hiển thị đúng\n"
       "- Bấm các ô: hành động chạy đúng\n"
       "- Màn thống kê: số friend đang theo rich menu mới = 1",
       group="UI",
       note="Nguồn: Change bot r203 (TR=OK, stg=OK) + AddBot/Testcase r233 + Bill tiền/change_bot r30. "
            "Tách riêng khỏi TC rich menu cũ vì luồng khác (tạo mới vs dùng lại) và rủi ro khác. "
            "RULE-06 + RULE-08. Evidence: ảnh rich menu trên LINE app + ảnh màn thống kê.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MEDIA-IMG-001", "Normal",
       "Danh sách ảnh Rich Menu của bot cũ được giữ nguyên sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥3 ảnh trong màn tạo hình ảnh Rich Menu",
       "1. Trước khi đổi LOA: vào /basic/image-richmenu, chụp ảnh danh sách, đếm số ảnh\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào lại /basic/image-richmenu, đếm số ảnh, đối chiếu với ảnh đã chụp\n"
       "4. Mở xem 1 ảnh để xác nhận ảnh còn tải được (không lỗi ảnh vỡ)\n"
       "5. Dùng 1 ảnh cũ để tạo rich menu mới",
       "≥3 ảnh rich menu của bot cũ",
       "- Danh sách ảnh rich menu GIỮ NGUYÊN đủ số lượng\n"
       "- Mở xem ảnh: ảnh tải được, không bị ảnh vỡ / 404\n"
       "- Dùng được ảnh cũ để tạo rich menu mới",
       note="Nguồn: Change bot r204 (TR=OK, stg=OK) + AddBot/Testcase r234. "
            "MEDIA-IMG-001 nâng BẮT BUỘC khi ảnh gửi ra phía LINE user / dùng cho rich menu. "
            "RULE-08 — media KHÔNG kết luận từ staging (đường dẫn media khác nhau giữa các môi trường). "
            "Evidence: 2 ảnh danh sách + ảnh mở xem 1 ảnh.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "NOTI-MAIL-001", "Normal",
       "Cài đặt thông báo của bot cũ được giữ nguyên sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ đã cấu hình thông báo (bật/tắt từng loại, email nhận)",
       "1. Trước khi đổi LOA: vào /basic/notify-setting, chụp ảnh toàn bộ cấu hình\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào lại /basic/notify-setting, đối chiếu từng mục với ảnh\n"
       "4. Tạo 1 sự kiện trigger thông báo (VD friend mới trả lời form)\n"
       "5. Kiểm tra hộp thư email nhận thông báo",
       "Cấu hình thông báo: ≥2 loại đã bật, email nhận đã điền",
       "- Cấu hình thông báo GIỮ NGUYÊN từng mục (trạng thái bật/tắt + email nhận)\n"
       "- Trigger sự kiện: email thông báo được gửi tới ĐÚNG hộp thư đã cấu hình\n"
       "- Nội dung email không còn thông tin LOA cũ (tên bot trong email là LOA mới)",
       group="UI",
       note="Nguồn: Change bot r205 (TR=OK, stg=OK) + AddBot/Testcase r235. "
            "Điểm bổ sung của AI: kiểm tên bot trong nội dung email — không nguồn nào nói, cần Leader xác nhận. "
            "NOTI-MAIL-001 nâng BẮT BUỘC. RULE-06 (verify trong hộp thư thật) + RULE-08. "
            "Evidence: 2 ảnh cấu hình + ảnh email nhận được.",
       spec="Đã hỏi leader", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Tin nhắn chào mừng — cấu hình giữ nguyên và chạy đúng cho cả 3 nhánh kết bạn",
       KEEP + "\n- Trước khi đổi LOA: bot cũ đã cấu hình tin chào mừng cho cả 3 trang "
       "(bạn mới · bạn cũ · bỏ chặn) kèm hành động\n"
       "- Có 3 tài khoản LINE test cho 3 nhánh",
       "1. Trước khi đổi LOA: chụp ảnh cấu hình cả 3 trang tin chào mừng + hành động\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào /basic/setting-add-friend, đối chiếu cả 3 trang với ảnh\n"
       "4. Nhánh A: cho tài khoản LINE 1 kết bạn MỚI qua URL kết bạn → quan sát tin + hành động\n"
       "5. Nhánh B: cho tài khoản LINE 2 kết bạn qua mã QR ở màn cài đặt kết bạn → quan sát\n"
       "6. Nhánh C: cho tài khoản LINE 3 chặn rồi bỏ chặn → quan sát tin bỏ chặn",
       "3 nhánh: kết bạn mới qua URL · kết bạn qua QR · bỏ chặn",
       "- Cấu hình cả 3 trang tin chào mừng GIỮ NGUYÊN (nội dung + hành động)\n"
       "- Nhánh A: friend nhận đúng tin chào mừng bạn mới + hành động chạy đúng\n"
       "- Nhánh B: kết bạn qua QR cũng nhận đúng tin + hành động\n"
       "- Nhánh C: friend bỏ chặn nhận đúng tin của trang bỏ chặn\n"
       "- Cả 3 nhánh: hành động đã cấu hình đều chạy (gắn tag / gửi template)",
       group="UI",
       note="Nguồn: Change bot r206-r207 (TR=OK, stg=OK) + AddBot/Testcase r236-r237. "
            "Nguồn gốc ghi cả 3 nhánh trong 1 dòng ('Kết bạn new friend / Kết bạn old friend / Unblock' + "
            "'Kết bạn qua url kết bạn / Kết bạn qua QR ở màn hình setting kết bạn') — giữ chung 1 TC vì CÙNG "
            "kết quả mong đợi 'thực hiện action đã setting', liệt kê đủ 3 nhánh ở Dữ liệu nhập. "
            "MSG-USER-001. RULE-06 + RULE-08. Evidence: ảnh cấu hình + 3 ảnh LINE app của 3 tài khoản.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "LIFF-ENTRY-001", "Normal",
       "Biểu mẫu CŨ gửi cho friend mới sau khi đổi LOA — trả lời được và lưu câu trả lời",
       KEEP + "\n- Trước khi đổi LOA: bot cũ đã tạo ≥1 form",
       "1. Trước khi đổi LOA: ghi lại form cũ (tên + số item)\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Xác nhận form cũ vẫn còn trong danh sách form\n"
       "4. Gửi form cũ đó cho friend MỚI qua chat 1:1\n"
       "5. Trên LINE app của friend mới: bấm link form, điền và gửi câu trả lời\n"
       "6. Vào màn kết quả form trên L Message, kiểm tra câu trả lời đã lưu",
       "1 form cũ có ≥3 item; 1 friend mới trả lời",
       "- Form cũ vẫn còn trong danh sách, cấu hình item không đổi\n"
       "- Gửi form cho friend mới: link mở được trên LINE app (LIFF ID mới hoạt động)\n"
       "- Friend điền và gửi: thành công, không lỗi\n"
       "- Màn kết quả form: câu trả lời của friend mới được lưu ĐÚNG nội dung đã điền\n"
       "- Số người trả lời tăng đúng 1",
       note="Nguồn: Change bot r208 (TR=OK, stg=OK) + AddBot/Testcase r238 + Bill tiền/change_bot r23 + "
            "Setting Liên kết BOT/Test logic r9. ⚠️ Đây là điểm RỦI RO CAO: form cũ dùng LIFF ID cũ "
            "(xem TC-CBF-090 ở nhóm 10 — link form cũ ĐÃ GỬI thì 404). Phải phân biệt: link ĐÃ GỬI TRƯỚC "
            "khi đổi LOA = 404; form GỬI LẠI SAU khi đổi LOA = phải hoạt động. "
            "LIFF-ENTRY-001 BẮT BUỘC. RULE-06 + RULE-08. "
            "Evidence: ảnh form trên LINE app + ảnh màn kết quả form.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "LIFF-ENTRY-001", "Normal",
       "Biểu mẫu tạo MỚI sau khi đổi LOA — gửi và trả lời được bình thường",
       KEEP,
       "1. Sau khi đổi LOA, tạo 1 form MỚI với ≥3 item\n"
       "2. Gửi form mới cho friend MỚI\n"
       "3. Trên LINE app: bấm link, điền và gửi\n"
       "4. Vào màn kết quả form, kiểm tra câu trả lời\n"
       "5. Kiểm tra số người trả lời trên màn danh sách form",
       "1 form mới 3 item; 1 friend mới trả lời",
       "- Tạo form mới thành công\n"
       "- Link form mở được trên LINE app, không lỗi LIFF\n"
       "- Câu trả lời được lưu đúng nội dung\n"
       "- Số người trả lời = 1",
       note="Nguồn: Change bot r209 (TR=OK, stg=OK, devnote=OK) + AddBot/Testcase r239 + "
            "Bill tiền/change_bot r24. RULE-06 + RULE-08. Evidence: ảnh form trên LINE app + màn kết quả.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "LIFF-ENTRY-001", "Normal",
       "Đặt lịch sự kiện CŨ và MỚI đều đặt chỗ được sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ đã tạo ≥1 sự kiện",
       "1. Trước khi đổi LOA: ghi lại sự kiện cũ\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Gửi link đặt lịch sự kiện CŨ cho friend MỚI → friend đặt chỗ\n"
       "4. Kiểm tra màn quản lý sự kiện: đặt chỗ mới có hiện không\n"
       "5. Tạo 1 sự kiện MỚI, gửi cho friend mới → đặt chỗ\n"
       "6. Kiểm tra lại màn quản lý",
       "1 sự kiện cũ + 1 sự kiện mới; 1 friend mới đặt chỗ mỗi sự kiện",
       "- Sự kiện CŨ: friend mới mở được link và đặt chỗ THÀNH CÔNG\n"
       "- Sự kiện MỚI: friend mới đặt chỗ thành công\n"
       "- Màn quản lý sự kiện hiển thị đủ 2 đặt chỗ của friend mới\n"
       "- Không lẫn đặt chỗ của friend LOA cũ",
       note="Nguồn: Change bot r210-r211 (TR=OK, stg=OK, devnote=OK) + AddBot/Testcase r240-r241 + "
            "Bill tiền/change_bot r27-r28. Gộp cũ + mới vì CÙNG kết quả 'booking thành công'. "
            "LIFF-ENTRY-001. RULE-06 + RULE-08. Evidence: ảnh LINE app 2 lần đặt chỗ + ảnh màn quản lý.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "INTG-CAL-001", "Normal",
       "Đặt lịch salon — friend mới đặt chỗ thành công và đồng bộ Google Spreadsheet + Google Calendar",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có lịch salon đã liên kết Google Spreadsheet và Google Calendar",
       "1. Trước khi đổi LOA: lưu ID spreadsheet + ID calendar đang đồng bộ\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Vào màn cấu hình đồng bộ Google của lịch salon, quan sát trạng thái liên kết\n"
       "4. Nếu mất liên kết: liên kết lại theo kết luận MT-09\n"
       "5. Gửi link đặt lịch salon cho friend MỚI → friend đặt chỗ\n"
       "6. Kiểm tra Google Spreadsheet và Google Calendar xem có dòng/sự kiện mới không",
       "ID spreadsheet + ID calendar cũ đã lưu; 1 friend mới đặt chỗ",
       "- Friend mới mở được link đặt lịch salon và đặt chỗ THÀNH CÔNG\n"
       "- Sau khi đặt chỗ: Google Spreadsheet có thêm dòng đúng nội dung đặt chỗ\n"
       "- Google Calendar có thêm sự kiện đúng thời gian đặt chỗ\n"
       "- Đích đồng bộ (spreadsheet/calendar nào) theo đúng kết luận MT-09",
       group="UI",
       note="⚠️ MT-09 — Change bot r212 (TR=OK, stg=OK, devnote=OK) nói 'sync google spread và google calendar "
            "BÌNH THƯỜNG' (hàm ý còn liên kết) nhưng r32 cùng tab nói 'sau khi change sẽ bị MẤT liên kết => "
            "phải liên kết lại, sync vào spread MỚI'. Cần Leader chốt có phải liên kết lại hay không. "
            "INTG-CAL-001 BẮT BUỘC khi đồng bộ 2 chiều với Google Calendar. RULE-06 + RULE-08. "
            "Evidence: ảnh màn cấu hình đồng bộ + ảnh dòng mới trong spreadsheet + ảnh sự kiện trong calendar.",
       spec="Đã hỏi leader", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "INTG-SHEET-001", "Normal",
       "Đặt lịch bài học — friend mới đặt chỗ thành công và đồng bộ Google Spreadsheet",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có lịch bài học đã liên kết Google Spreadsheet",
       "1. Trước khi đổi LOA: lưu ID spreadsheet đang đồng bộ\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Kiểm tra trạng thái liên kết Google của lịch bài học, liên kết lại nếu mất\n"
       "4. Gửi link đặt lịch bài học cho friend MỚI → friend đặt chỗ\n"
       "5. Kiểm tra Google Spreadsheet có dòng mới không\n"
       "6. Kiểm tra màn quản lý lịch bài học",
       "ID spreadsheet cũ đã lưu; 1 friend mới đặt chỗ bài học",
       "- Friend mới mở được link và đặt chỗ bài học THÀNH CÔNG\n"
       "- Google Spreadsheet có thêm dòng đúng nội dung đặt chỗ\n"
       "- Màn quản lý lịch bài học hiển thị đặt chỗ mới\n"
       "- Bộ đếm chỗ đã đặt của khóa học tăng đúng 1",
       group="UI",
       note="⚠️ MT-09. Nguồn: Change bot r213 (TR=OK, stg=OK, devnote=OK) + Bill tiền/change_bot r25-r26. "
            "INTG-SHEET-001 BẮT BUỘC khi ghi dữ liệu khách hàng ra spreadsheet ngoài. RULE-06 + RULE-08. "
            "Evidence: ảnh màn quản lý + ảnh dòng mới trong spreadsheet.",
       spec="Đã hỏi leader", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-004", "Normal",
       "Gửi thử mẫu tin nhắn đủ các loại nội dung sau khi đổi LOA — friend mới nhận đúng",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có mẫu tin nhắn đủ các loại nội dung\n"
       "- Đã thêm 1 tài khoản gửi thử cho LOA mới",
       "1. Sau khi đổi LOA, thêm tài khoản gửi thử cho LOA mới\n"
       "2. Mở mẫu tin nhắn CŨ loại text, bấm gửi thử → kiểm tra LINE app\n"
       "3. Lặp lại với mẫu loại ảnh thường, ảnh imagemap, nút bấm, video, audio\n"
       "4. Với từng loại: đối chiếu nội dung nhận được trên LINE với nội dung cấu hình\n"
       "5. Với mẫu nút bấm: bấm nút và kiểm tra hành động chạy",
       "6 loại nội dung: text · ảnh thường · ảnh imagemap · nút bấm · video · audio",
       "- CẢ 6 loại đều gửi thử thành công, không lỗi\n"
       "- Trên LINE app: nội dung nhận được KHỚP cấu hình từng loại (text đúng chữ, ảnh đúng ảnh, "
       "video/audio phát được, imagemap đúng vùng bấm)\n"
       "- Mẫu nút bấm: bấm nút → hành động chạy đúng cấu hình\n"
       "- Không loại nào bị lỗi media / lỗi không tải được",
       group="UI",
       note="Nguồn: Change bot r214 (TR=OK, stg=OK, devnote=OK) + AddBot/Testcase r244 + "
            "Bill tiền/change_bot r31. Gộp 6 loại vào 1 TC vì CÙNG kết quả mong đợi 'gửi thành công + "
            "hiển thị đúng' — liệt kê đủ 6 điểm ở Dữ liệu nhập. MSG-004 BẮT BUỘC khi output là nội dung "
            "user cuối nhìn thấy trên LINE. RULE-06 + RULE-08 (media KHÔNG kết luận từ staging). "
            "Evidence: 6 ảnh LINE app theo từng loại.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-004", "Normal",
       "Gửi tin ở chat 1:1 cho friend mới sau khi đổi LOA — đủ loại nội dung đều tới được",
       KEEP,
       "1. Sau khi đổi LOA, vào chat 1:1 với friend MỚI\n"
       "2. Gửi tin text → kiểm tra LINE app\n"
       "3. Gửi ảnh → kiểm tra LINE app\n"
       "4. Gửi 1 mẫu tin nhắn có nút bấm → kiểm tra LINE app\n"
       "5. Với tin có nút: bấm nút và kiểm tra hành động chạy\n"
       "6. Kiểm tra tin đã gửi hiển thị đúng trong lịch sử chat trên L Message",
       "3 loại: text · ảnh · mẫu có nút bấm",
       "- CẢ 3 loại tin đều tới được LINE app của friend mới, nội dung đúng\n"
       "- Bấm nút của mẫu tin: hành động chạy đúng cấu hình\n"
       "- Lịch sử chat trên L Message hiển thị đủ 3 tin vừa gửi\n"
       "- Không lỗi gửi tin trong màn lỗi phát hành",
       group="UI",
       note="Nguồn: Change bot r215 (TR=OK, stg=OK, devnote=OK) + AddBot/Testcase r245 + "
            "Bill tiền/change_bot r32. MSG-004. RULE-06 + RULE-07 (DB + màn hình + output) + RULE-08. "
            "Evidence: 3 ảnh LINE app + ảnh lịch sử chat.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "LIFF-ENTRY-001", "Normal",
       "QR Code Action CŨ và MỚI đều kết bạn được sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥1 QR code action",
       "1. Trước khi đổi LOA: ghi lại QR code action cũ\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Lấy link/ảnh QR code action CŨ từ màn quản lý (không dùng link đã lưu từ trước)\n"
       "4. Dùng 1 tài khoản LINE chưa kết bạn quét QR cũ đó → kết bạn\n"
       "5. Tạo 1 QR code action MỚI, quét bằng tài khoản LINE khác → kết bạn\n"
       "6. Kiểm tra 2 friend mới xuất hiện trong danh sách và hành động QR chạy đúng",
       "1 QR cũ + 1 QR mới; 2 tài khoản LINE chưa kết bạn",
       "- QR CŨ (lấy lại từ màn quản lý sau khi đổi LOA): quét kết bạn THÀNH CÔNG với LOA mới\n"
       "- QR MỚI: quét kết bạn thành công\n"
       "- Cả 2 friend xuất hiện trong danh sách bạn bè\n"
       "- Hành động cấu hình trong QR code action chạy đúng cho cả 2 friend",
       note="Nguồn: Change bot r217-r218 (TR=OK, stg=OK, devnote=OK) + AddBot/Testcase r247-r248 + "
            "Bill tiền/change_bot r34-r35. ⚠️ Phân biệt với TC ở nhóm 10: link/ảnh QR ĐÃ LƯU TRƯỚC khi đổi "
            "LOA thì KHÔNG còn chạy action; còn QR lấy lại từ màn quản lý SAU khi đổi LOA thì phải hoạt động. "
            "LIFF-ENTRY-001. RULE-06 + RULE-08. Evidence: 2 ảnh LINE app + ảnh danh sách bạn bè + "
            "ảnh kết quả hành động.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "LIFF-ENTRY-001", "Normal",
       "Popup CŨ và MỚI đều nhúng được và thống kê đúng sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥1 popup đã nhúng vào 1 trang web test",
       "1. Trước khi đổi LOA: ghi lại popup cũ + trang web đã nhúng\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Lấy lại mã nhúng của popup CŨ từ màn quản lý, nhúng lại vào trang test\n"
       "4. Mở trang test, quan sát popup hiển thị, bấm vào popup\n"
       "5. Kiểm tra màn thống kê popup: lượt click có tăng không\n"
       "6. Tạo popup MỚI, nhúng và lặp bước 4-5",
       "1 popup cũ + 1 popup mới; 1 trang web test để nhúng",
       "- Popup CŨ: hiển thị được trên trang test, bấm được\n"
       "- Màn thống kê popup cũ: lượt click tăng đúng 1\n"
       "- Popup MỚI: hiển thị và bấm được, thống kê tăng đúng\n"
       "- Không hiển thị lại dữ liệu thống kê của LOA cũ",
       note="Nguồn: Change bot r219-r220 (TR=OK, stg=OK) + AddBot/Testcase r249-r250. "
            "⚠️ Nguồn r219 chỉ ghi expected 'Check việc nhúng popup và count data thống kê bình thường' — "
            "các con số cụ thể do AI viết, cần Leader xác nhận. "
            "LIFF-ENTRY-001 + DATA-COUNT-001. RULE-08. "
            "Evidence: ảnh popup trên trang test + ảnh màn thống kê trước/sau click.",
       spec="Đã hỏi leader", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "PAY-STATE-001", "Normal",
       "Sản phẩm CŨ và MỚI — friend mới mua được cả sản phẩm đơn lẻ và định kỳ sau khi đổi LOA",
       KEEP + "\n- Trước khi đổi LOA: bot cũ có ≥1 sản phẩm đơn lẻ và ≥1 sản phẩm định kỳ\n"
       "- Có phương thức thanh toán test hợp lệ",
       "1. Trước khi đổi LOA: ghi lại 2 sản phẩm cũ (đơn lẻ + định kỳ)\n"
       "2. Hoàn tất đổi LOA, chờ job xong\n"
       "3. Gửi sản phẩm đơn lẻ CŨ cho friend MỚI → friend mua và thanh toán\n"
       "4. Gửi sản phẩm định kỳ CŨ cho friend mới → friend mua\n"
       "5. Tạo 2 sản phẩm MỚI (đơn lẻ + định kỳ), gửi và cho friend mua\n"
       "6. Kiểm tra lịch sử mua hàng trên L Message + giao dịch ở cổng thanh toán",
       "2 sản phẩm cũ (đơn lẻ + định kỳ) và 2 sản phẩm mới; 1 friend mới mua cả 4",
       "- CẢ 4 lần mua đều thành công, friend nhận được xác nhận trên LINE\n"
       "- Lịch sử mua hàng trên L Message hiển thị đủ 4 đơn của friend mới\n"
       "- Cổng thanh toán có đủ 4 giao dịch tương ứng, số tiền đúng\n"
       "- Sản phẩm định kỳ: lịch bill chu kỳ tiếp theo được tạo đúng",
       group="UI",
       note="Nguồn: Change bot r221-r222 (TR=OK, stg=OK) + AddBot/Testcase r251-r252. "
            "PAY-STATE-001 BẮT BUỘC với mọi chức năng có giao dịch tiền. "
            "RULE-06 (verify ở cổng thanh toán + LINE) + RULE-08 (bill tiền KHÔNG kết luận từ staging). "
            "Evidence: 4 ảnh LINE app + ảnh lịch sử mua hàng + ảnh giao dịch cổng thanh toán.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "MSG-USER-001", "Normal",
       "Kết bạn thường (qua URL kết bạn của LOA mới) hoạt động bình thường sau khi đổi LOA",
       KEEP + "\n- Có 1 tài khoản LINE chưa kết bạn với LOA mới",
       "1. Sau khi đổi LOA, lấy URL kết bạn của bot từ màn cài đặt\n"
       "2. Mở URL đó trên điện thoại có LINE\n"
       "3. Bấm kết bạn\n"
       "4. Quan sát tin chào mừng nhận được\n"
       "5. Kiểm tra friend xuất hiện trong danh sách bạn bè + chat 1:1",
       "1 tài khoản LINE chưa kết bạn; URL kết bạn của LOA mới",
       "- URL kết bạn mở đúng LOA MỚI (tên bot khớp)\n"
       "- Kết bạn thành công\n"
       "- Nhận được tin chào mừng đã cấu hình\n"
       "- Friend xuất hiện trong danh sách bạn bè và chat 1:1 của L Message",
       group="UI",
       note="Nguồn: Bill tiền/change_bot r36 ('kết bạn thường → kết bạn thành công', TR=OK). "
            "MSG-USER-001. RULE-06 + RULE-08. Evidence: ảnh LINE app + ảnh danh sách bạn bè.", **PRD),

    tc("Setting giữ nguyên sau khi đổi", "PAY-PLAN-001", "Normal",
       "Đổi LOA thành công ở CẢ 3 gói — friend kết bạn và hành động chạy bình thường, không thấy friend LOA cũ",
       ("- Có 3 bot riêng ở 3 gói: Free (trong campaign) · Standard · Pro\n"
        "- Mỗi bot đều có friend và dữ liệu trước khi đổi LOA\n"
        "- Có 3 LOA mới hợp lệ để đổi"),
       "1. Với bot gói Free: thực hiện đổi LOA đến khi hoàn tất\n"
       "2. Cho 1 friend mới kết bạn, kiểm tra hành động chạy + danh sách bạn bè\n"
       "3. Lặp bước 1-2 với bot gói Standard\n"
       "4. Lặp bước 1-2 với bot gói Pro\n"
       "5. Với cả 3: kiểm tra không còn friend của LOA cũ",
       "3 gói: Free (campaign) · Standard · Pro",
       "- CẢ 3 gói: đổi LOA thành công\n"
       "- CẢ 3: friend mới kết bạn thành công, hành động chạy bình thường\n"
       "- CẢ 3: KHÔNG hiển thị friend của LOA cũ\n"
       "- Không gói nào bị chặn/lỗi riêng",
       group="UI",
       note="Nguồn: Change bot r245-r247 (stg=OK cho cả 3 gói: 'check change bot / add bot free / standard / "
            "pro → change bot thành công, friend kết bạn thành công, send action bình thường, không hiển thị "
            "friend của bot cũ'). ⚠️ MT-04 — nhánh gói Free phụ thuộc kết luận về điều kiện vào màn. "
            "⚠️ Change bot r242-r244 (cùng khối, kiểm ADD BOT cho 3 gói) KHÔNG thuộc phạm vi FA-039 — "
            "đã ghi vào excluded. PAY-PLAN-001 BẮT BUỘC với thao tác thay đổi gói/hợp đồng. RULE-08. "
            "Evidence: 3 ảnh màn hoàn tất + 3 ảnh LINE app + 3 ảnh danh sách bạn bè.",
       spec="Đã hỏi leader", **PRD),
]

S13 = [
    # ═══════════════ 13. Phân quyền & bảo mật ═══════════════
    tc("Phân quyền & bảo mật", "PERM-001", "Abnormal",
       "Staff KHÔNG được cấp quyền đổi LOA → không thấy mục menu ở cả menu thường và menu favourite",
       ("- Có tài khoản Staff thuộc bot Standard\n"
        "- Admin CHƯA cấp quyền truy cập tính năng đổi LOA cho Staff đó"),
       "1. Đăng nhập bằng tài khoản Staff chưa được cấp quyền\n"
       "2. Mở sidebar, tìm mục「LINE公式アカウント入れ替え」\n"
       "3. Mở khu vực menu favourite, tìm mục tương tự\n"
       "4. Dùng Ctrl+F trên trang để tìm chuỗi「入れ替え」",
       "Staff chưa được cấp quyền",
       "- Sidebar: KHÔNG có mục「LINE公式アカウント入れ替え」\n"
       "- Menu favourite: KHÔNG có mục đó (không ghim được)\n"
       "- Không có link nào dẫn tới màn đổi LOA trên toàn trang",
       note=MT02 + "Nguồn: Change bot r224-r225 ('Không được phép access từ menu') + TC-CBF-092 "
            "(PERM-001 + MAP-PERM-01, BR-45; Pass dev). PERM-001 BẮT BUỘC khi chức năng có phân biệt quyền. "
            "Evidence: ảnh sidebar + ảnh menu favourite + ảnh Ctrl+F.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & bảo mật", "PERM-002", "Abnormal",
       "Staff KHÔNG được cấp quyền → truy cập trực tiếp URL màn đổi LOA bị chặn và đá về trang chủ",
       ("- Có tài khoản Staff chưa được cấp quyền đổi LOA\n"
        "- Biết URL màn đổi LOA"),
       "1. Đăng nhập Staff chưa được cấp quyền\n"
       "2. Dán URL màn đổi LOA vào thanh địa chỉ, Enter\n"
       "3. Quan sát URL cuối và thông báo\n"
       "4. Kiểm tra response body có chứa thông tin bot không",
       "Staff chưa được cấp quyền; URL màn đổi LOA",
       "- Hiển thị thông báo lỗi quyền\n"
       "- Bị đá về /basic/overview (hoặc 403 theo kết luận MT-02)\n"
       "- Response KHÔNG chứa Channel ID / thông tin kết nối của bot",
       note=MT02 + "Nguồn: Change bot r226 ('Báo lỗi và quay lại màn hình home: "
            "https://staging.lme.jp/basic/overview') + TC-CBF-026 (Pass dev + staging). "
            "PERM-002 BẮT BUỘC khi có thao tác nhạy cảm. Evidence: URL cuối + ảnh thông báo + response body.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & bảo mật", "PERM-001", "Normal",
       "Staff ĐƯỢC cấp quyền đổi LOA — 3 vai trò truy cập và thao tác được qua cả 3 đường vào",
       ("- Có 3 tài khoản Staff ở 3 vai trò: 副管理人 · 運用者 · サポート\n"
        "- Admin ĐÃ cấp quyền truy cập tính năng đổi LOA cho cả 3"),
       "1. Đăng nhập Staff vai trò 副管理人, vào màn đổi LOA từ MENU THƯỜNG → thao tác thử tới bước nhập\n"
       "2. Đăng nhập Staff vai trò 運用者, vào từ MENU FAVOURITE → thao tác thử\n"
       "3. Đăng nhập Staff vai trò サポート, vào bằng URL TRỰC TIẾP → thao tác thử\n"
       "4. Với cả 3: ghi lại có vào được màn và thao tác được không",
       "3 vai trò × 3 đường vào: 副管理人 (menu thường) · 運用者 (menu favourite) · サポート (URL trực tiếp)",
       "- Kết quả theo đúng kết luận MT-02 của Leader\n"
       "- Nếu Leader chốt 'Staff được cấp quyền thì thao tác được': cả 3 vai trò vào được và thao tác bình thường\n"
       "- Nếu Leader chốt 'Staff KHÔNG bao giờ được đổi LOA': cả 3 bị chặn dù đã cấp quyền\n"
       "- Không được có kết quả khác nhau giữa 3 đường vào của cùng 1 vai trò",
       note="⚠️ MT-02 — ĐÂY LÀ TC TRUNG TÂM của mâu thuẫn, 3 nguồn nói 3 kiểu: "
            "(1) Change bot r227-r229 (04/2026): cả 3 vai trò 'được access từ menu và thao tác change bot "
            "bình thường'; (2) AddBot/Testcase r342-r344: expected ghi '運用者/サポート ko có quyền' nhưng "
            "ghi nhận thực tế 'Account staff VẪN thao tác change bot bt' + comment 'Check lại TCs này, c thấy "
            "account staff vẫn change đc? => Confirm lại a Tư'; (3) TC-CBF-092/093 (07-08/2026): Staff KHÔNG "
            "thấy menu + gọi API → 403 (BR-45). ⚠️ Nguy hiểm: đổi LOA là thao tác KHÔNG hoàn tác được, "
            "nếu Staff làm được mà lẽ ra không thì là lỗ hổng quyền NẶNG. "
            "Evidence: 3 ảnh màn + 3 ảnh kết quả thao tác.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & bảo mật", "PERM-002", "Abnormal",
       "Staff gọi thẳng API của tính năng đổi LOA qua DevTools (bypass UI) → bị từ chối ở mọi endpoint",
       ("- Có tài khoản Staff (chưa được cấp quyền đổi LOA)\n"
        "- Đã bắt được danh sách endpoint của tính năng đổi LOA từ phiên Admin"),
       "1. Đăng nhập Admin, mở DevTools Network, chạy hết flow đổi LOA để bắt danh sách endpoint + payload\n"
       "2. Ghi lại ≥4 endpoint đại diện (validate channel · tạo đặt lịch · thực hiện đổi · xóa đặt lịch)\n"
       "3. Đăng nhập bằng Staff, mở DevTools Console\n"
       "4. Gọi lần lượt ≥4 endpoint đó với payload đã bắt\n"
       "5. Ghi lại mã response của từng endpoint + query DB kiểm tra có dữ liệu nào bị ghi không",
       "≥4 endpoint: validate channel · tạo đặt lịch · thực hiện đổi LOA · xóa đặt lịch",
       "- TẤT CẢ endpoint đều trả 403 (hoặc mã chặn theo kết luận MT-02)\n"
       "- DB: KHÔNG có bản ghi nào được tạo/sửa/xóa bởi các request của Staff\n"
       "- Bên LINE: không có LIFF app / webhook nào bị thay đổi\n"
       "- Response không rò rỉ Channel ID / secret",
       note=MT02 + "Nguồn: TC-CBF-093 (PERM-002 + MAP-PERM-02, BR-45; Pass dev) + TC-CBF-099. "
            "⚠️ Đây là điểm kiểm TẦNG API, không chỉ tầng UI — bài học từ bug phân quyền trước đây "
            "(API list không enforce quyền dù UI đã ẩn menu). PERM-002 BẮT BUỘC. RULE-07. "
            "Evidence: ảnh response từng endpoint + query DB + ảnh LINE Developers.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & bảo mật", "PERM-003", "Abnormal",
       "Admin KHÔNG phải chủ bot đổi bot_id trên URL sang bot của Admin khác → bị chặn ở MỌI bước",
       ("- Có 2 tài khoản Admin A và B, mỗi người sở hữu bot riêng\n"
        "- Admin A biết Hashids id bot của Admin B"),
       "1. Đăng nhập Admin A\n"
       "2. Ở bước chọn phương thức: đổi bot_id trên URL sang bot của B → quan sát\n"
       "3. Ở bước nhập thông tin: đổi bot_id → quan sát\n"
       "4. Ở bước xác nhận: đổi bot_id → quan sát\n"
       "5. Ở màn đã đặt lịch: đổi bot_id → quan sát\n"
       "6. Với mọi bước: kiểm tra có thông tin nào của bot B bị lộ không + query DB bot B",
       "bot_id của Admin B; thử ở 4 bước của flow",
       "- CẢ 4 bước đều bị reject, KHÔNG bước nào cho đi tiếp với bot của B\n"
       "- KHÔNG lộ thông tin bot B ở bất kỳ bước nào (tên bot, Channel ID, số bạn bè)\n"
       "- DB: bot B không bị sửa/tạo bản ghi nào\n"
       "- Không bước nào trả lỗi 500 (phải là lỗi quyền rõ ràng)",
       note="Nguồn: TC-CBF-094 (PERM-003 + MAP-PERM-03; Blocked cả 2 env) + TC-CBF-095. "
            "PERM-003 ghi rõ trigger 'BẮT BUỘC khi tổ chức vận hành nhiều LINE OA hoặc có chức năng change bot' "
            "→ đây là quan điểm bắt buộc số 1 của tính năng này. RULE-07. "
            "Evidence: 4 ảnh response + query DB bot B."),

    tc("Phân quyền & bảo mật", "SEC-ISO-001", "Boundary",
       "2 tab cùng Admin thao tác đổi LOA cho 2 BOT KHÁC NHAU → dữ liệu không lẫn giữa 2 tab",
       ("- Đăng nhập Admin sở hữu 2 bot X và Y (đều Standard)\n"
        "- Có 2 LOA mới khác nhau để đổi cho X và Y"),
       "1. Tab A: vào flow đổi LOA cho bot X, nhập 4 field của LOA mới 1\n"
       "2. Tab B: vào flow đổi LOA cho bot Y, nhập 4 field của LOA mới 2\n"
       "3. Ở tab A bấm đi tiếp → quan sát màn xác nhận hiển thị thông tin LOA nào\n"
       "4. Ở tab B bấm đi tiếp → quan sát màn xác nhận hiển thị thông tin LOA nào\n"
       "5. Query DB sau mỗi bước",
       "bot X + LOA mới 1; bot Y + LOA mới 2",
       "- Tab A: màn xác nhận hiển thị ĐÚNG LOA mới 1 cho bot X\n"
       "- Tab B: màn xác nhận hiển thị ĐÚNG LOA mới 2 cho bot Y\n"
       "- KHÔNG lẫn: tab A không hiển thị LOA mới 2 và ngược lại\n"
       "- DB: bản ghi của bot X trỏ LOA 1, bot Y trỏ LOA 2, không đảo",
       note="Nguồn: TC-CBF-098 (SEC-ISO-001; Blocked cả 2 env). SEC-ISO-001 BẮT BUỘC khi UI tải/hiển thị "
            "nhiều đối tượng dữ liệu đồng thời. RULE-07. Evidence: 2 ảnh màn xác nhận + query DB."),

    tc("Phân quyền & bảo mật", "SEC-001", "Abnormal",
       "Chưa đăng nhập truy cập mọi URL của tính năng đổi LOA → redirect login, không lộ dữ liệu",
       ("- Đã đăng xuất / mở cửa sổ ẩn danh\n"
        "- Có sẵn danh sách URL các bước của flow đổi LOA"),
       "1. Mở cửa sổ ẩn danh\n"
       "2. Dán lần lượt URL của ≥4 bước (chọn phương thức · nhập thông tin · màn đã đặt lịch · URL cũ)\n"
       "3. Với mỗi URL: ghi URL cuối và nội dung trang\n"
       "4. Kiểm tra response body có chứa thông tin bot nào không",
       "≥4 URL của flow đổi LOA",
       "- TẤT CẢ URL đều redirect về màn login\n"
       "- KHÔNG URL nào render nội dung màn đổi LOA\n"
       "- Response body không chứa tên bot / Channel ID / số bạn bè",
       note="Nguồn: TC-CBF-012 (SEC-001, BR-06/FN-11; Pass dev + staging — đã chạy cho URL trang campaign) "
            "mở rộng cho các URL còn lại của flow. SEC-001 BẮT BUỘC khi chức năng chạm dữ liệu cá nhân. "
            "Evidence: 4 ảnh URL cuối + response body."),
]

S14 = [
    # ═══════════════ 14. Hồi quy & môi trường ═══════════════
    tc("Hồi quy & môi trường", "UI-002", "Normal",
       "Toàn bộ flow đổi LOA chạy nhất quán trên Chrome (Windows) và Safari (Mac)",
       ("- Có máy Windows cài Chrome và máy Mac cài Safari\n"
        "- Đăng nhập cùng Admin chủ bot Standard trên cả 2 máy\n"
        "- Có 2 LOA mới hợp lệ để chạy 2 lần"),
       "1. Trên Win Chrome: chạy hết flow đổi LOA từ màn chọn phương thức đến màn hoàn tất, "
       "chụp ảnh TỪNG màn\n"
       "2. Trên Mac Safari: chạy lại flow tương tự với LOA mới thứ 2, chụp ảnh từng màn\n"
       "3. Đặt cặp ảnh từng màn cạnh nhau, đối chiếu layout · text tiếng Nhật · vị trí và màu nút\n"
       "4. Ghi lại mọi điểm khác biệt",
       "2 môi trường: Windows Chrome + Mac Safari",
       "- Layout từng màn nhất quán giữa 2 trình duyệt (không lệch cột, không tràn)\n"
       "- Text tiếng Nhật hiển thị đúng trên cả 2, không lỗi font\n"
       "- Vị trí và màu nút giống nhau\n"
       "- Flow hoàn tất được ở CẢ 2 trình duyệt, không nhánh nào bị chặn",
       note="Nguồn: TC-CBF-102 (UI-002 + UIC-13 'Mac Safari là nhóm user chính cần chú trọng'; "
            "Blocked cả 2 env). RULE-08. Evidence: bộ ảnh từng màn × 2 trình duyệt đặt cạnh nhau.", **PRD),

    tc("Hồi quy & môi trường", "UI-001", "Normal",
       "Toàn bộ flow hiển thị đúng ở độ phân giải tối thiểu 1366×768, không vỡ layout",
       ("- Đăng nhập Admin chủ bot Standard\n"
        "- Đặt cửa sổ trình duyệt đúng 1366×768"),
       "1. Đặt cửa sổ trình duyệt về đúng 1366×768\n"
       "2. Chạy hết flow đổi LOA, chụp ảnh từng màn\n"
       "3. Với mỗi màn: kiểm tra có phải cuộn NGANG không\n"
       "4. Kiểm tra các nút CTA và hộp cảnh báo có nằm trong vùng nhìn thấy không\n"
       "5. Kiểm tra modal có bị cắt mép không",
       "Độ phân giải 1366×768",
       "- KHÔNG màn nào phải cuộn ngang\n"
       "- Nút CTA của từng màn nhìn thấy được (không bị đẩy khỏi khung)\n"
       "- Hộp cảnh báo không bị cắt\n"
       "- Modal (xác nhận xóa / xác nhận thực hiện / tiến trình) không bị cắt mép",
       note="Nguồn: TC-CBF-105 (UI-001 + UIC-13; Blocked cả 2 env). "
            "Evidence: bộ ảnh từng màn ở 1366×768."),

    tc("Hồi quy & môi trường", "UI-001", "Normal",
       "Mọi nút CTA xuyên suốt flow có hiệu ứng hover + con trỏ tay, trạng thái disabled rõ ràng",
       ("- Đăng nhập Admin chủ bot Standard\n"
        "- Chạy qua từng màn của flow đổi LOA"),
       "1. Ở từng màn của flow, đưa chuột vào nút CTA chính → quan sát hiệu ứng và con trỏ\n"
       "2. Với nút đang DISABLED: đưa chuột vào → quan sát con trỏ và hiệu ứng\n"
       "3. Lặp cho nút phụ (キャンセル, quay lại bước trước)\n"
       "4. Lặp cho 4 nút của 2 modal (xác nhận xóa / xác nhận thực hiện)",
       "Toàn bộ nút CTA + nút phụ + nút trong modal của flow",
       "- Nút ENABLED: có hiệu ứng hover rõ (đổi màu/đổ bóng), con trỏ hình TAY\n"
       "- Nút DISABLED: KHÔNG có hiệu ứng hover, con trỏ KHÔNG phải tay, màu nhạt rõ rệt\n"
       "- Phân biệt được enabled/disabled bằng mắt thường, không cần hover mới biết\n"
       "- Không nút nào thiếu trạng thái hover",
       note="Nguồn: TC-CBF-109 (UI-001 + UIC-02; Blocked cả 2 env) + Change bot r121 "
            "(bản #34632 kiểm double click các nút). Evidence: ảnh hover từng nút + ảnh nút disabled."),

    tc("Hồi quy & môi trường", "UI-004", "Normal",
       "User lần đầu dùng hoàn thành được flow đổi LOA mà không bị lạc",
       ("- Có 1 người chưa từng dùng tính năng đổi LOA (không phải tester đã quen)\n"
        "- Cung cấp 4 giá trị Channel ID/secret hợp lệ và KHÔNG hướng dẫn thêm"),
       "1. Giao cho người đó tài khoản Admin + 4 giá trị Channel, yêu cầu tự đổi LOA\n"
       "2. Quan sát, KHÔNG nhắc, ghi lại mỗi lần họ ngập ngừng > 30 giây\n"
       "3. Ghi lại số lần họ phải bấm vào link hướng dẫn/video\n"
       "4. Ghi lại thời gian hoàn thành\n"
       "5. Phỏng vấn ngắn: chỗ nào khó hiểu nhất",
       "1 người chưa dùng tính năng; 4 giá trị Channel hợp lệ",
       "- Người đó hoàn thành được flow mà KHÔNG cần hỏi ai\n"
       "- Ghi nhận đầy đủ danh sách điểm ngập ngừng (để cải thiện UX)\n"
       "- Không bị kẹt vĩnh viễn ở bước nào",
       note="Nguồn: TC-CBF-106 (UI-004; Blocked cả 2 env). ⚠️ Ghi chú nguồn: 'không phải gate chặn release, "
            "chỉ ghi nhận feedback UX' → TC này KHÔNG dùng để chặn release. UI-004 ưu tiên Thấp, chỉ áp dụng "
            "cho onboarding/flow phức tạp. Evidence: biên bản quan sát + thời gian hoàn thành."),

    tc("Hồi quy & môi trường", "REG-SHARED-001", "Normal",
       "Tính năng thêm LOA mới (add bot) KHÔNG bị ảnh hưởng bởi thay đổi ở tính năng đổi LOA",
       ("- Có tài khoản Admin còn slot để thêm bot mới\n"
        "- Có 1 LOA mới hợp lệ chưa kết nối L Message\n"
        "- Đã có đợt release thay đổi tính năng đổi LOA"),
       "1. Sau đợt release tính năng đổi LOA, vào /admin/bot-add\n"
       "2. Chạy hết flow THÊM bot mới (không phải đổi LOA) với LOA mới\n"
       "3. Kiểm tra bot mới được thêm thành công\n"
       "4. Cho 1 friend kết bạn với bot mới, kiểm tra nhận tin chào mừng\n"
       "5. Query DB: bots, bot_contract, bot_slots của bot mới\n"
       "6. Kiểm tra dữ liệu khởi tạo của bot mới (template, tag, auto-reply mặc định)",
       "1 LOA mới hợp lệ; flow add bot (không phải change bot)",
       "- Flow thêm bot mới chạy hoàn tất bình thường, không lỗi\n"
       "- DB: bots + bot_contract + bot_slots được tạo đủ cho bot mới\n"
       "- Friend kết bạn thành công, nhận được tin chào mừng\n"
       "- Dữ liệu khởi tạo của bot mới đầy đủ như trước release",
       note="Nguồn: TC-CBF-114 (REG-SHARED-001, TD Section 7.1 '`botChange()` GIỮ NGUYÊN — logic được "
            "THAM KHẢO cho job đổi LOA, không sửa trực tiếp'; Blocked cả 2 env). "
            "REG-SHARED-001 BẮT BUỘC với mọi release sửa code dùng chung. RULE-08. "
            "Evidence: ảnh màn thêm bot thành công + query 3 bảng + ảnh LINE app friend.", **PRD),

    tc("Hồi quy & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Bot ĐÃ từng đổi LOA trước đây mở lại màn LOA接続設定 vẫn hoạt động bình thường",
       ("- Có 1 bot đã từng đổi LOA ở đợt trước (có cột dữ liệu cũ như id_bot_change)\n"
        "- Đã có đợt release thêm cột mới cho tính năng đổi LOA"),
       "1. Xác định 1 bot đã từng đổi LOA trước đợt release (query cột id_bot_change khác NULL)\n"
       "2. Sau release, vào /admin/bot-edit?id={id} của bot đó\n"
       "3. Quan sát màn có load đủ không, có lỗi không\n"
       "4. Bấm nút kiểm tra kết nối → quan sát kết quả\n"
       "5. Bấm nút「LINE公式アカウント入れ替え」→ quan sát có vào được flow mới không\n"
       "6. Kiểm tra Console có lỗi JS không",
       "1 bot có id_bot_change khác NULL từ đợt đổi LOA trước",
       "- Màn LOA接続設定 load đủ, không lỗi 500, không trang trắng\n"
       "- Kiểm tra kết nối trả kết quả bình thường\n"
       "- Vào được flow đổi LOA mới từ nút trên toolbar\n"
       "- Console không có lỗi JS do cột dữ liệu cũ/mới lệch nhau",
       note="Nguồn: TC-CBF-116 (COMPAT-LEGACY-001, TD Section 3 Altered Tables 'cột mới thêm vào, "
            "không sửa cột cũ'; Blocked cả 2 env) + spec bot-edit/db/db-mapping.md:51 "
            "(`id_bot_change` int(11) NULL — 'ID bot thay thế (LOA入れ替え)'). "
            "COMPAT-LEGACY-001 BẮT BUỘC, RULE-09 cũ & mới song song. "
            "Evidence: ảnh màn LOA接続設定 + ảnh Console + query cột dữ liệu cũ."),

    tc("Hồi quy & môi trường", "DATA-MIG-001", "Normal",
       "Bot có dữ liệu đổi LOA tạo TRƯỚC release vẫn đọc đúng sau khi thêm cột mới",
       ("- Có bản ghi liên quan đổi LOA tạo TRƯỚC đợt release (bot đã đổi LOA hoặc có đặt lịch cũ)\n"
        "- Đợt release có thêm cột mới vào bảng liên quan"),
       "1. Trước release: query và lưu toàn bộ giá trị các bản ghi liên quan đổi LOA của 1 bot\n"
       "2. Sau release: query lại các bản ghi đó\n"
       "3. Đối chiếu từng giá trị cột CŨ với bản đã lưu\n"
       "4. Kiểm tra cột MỚI có giá trị mặc định hợp lý không (không NULL gây lỗi)\n"
       "5. Mở màn liên quan trên UI, kiểm tra hiển thị đúng",
       "Bộ bản ghi đổi LOA trước release đã lưu",
       "- Giá trị các cột CŨ KHÔNG bị đổi sau migration\n"
       "- Cột MỚI có giá trị mặc định không gây lỗi khi đọc (không NULL ở chỗ code không xử lý NULL)\n"
       "- UI hiển thị đúng với dữ liệu cũ, không lỗi\n"
       "- Không bản ghi nào bị mất",
       note="Nguồn: TC-CBF-116 (TD Section 3 Altered Tables) mở rộng theo DATA-MIG-001. "
            "DATA-MIG-001 BẮT BUỘC khi release đổi cấu trúc dữ liệu và tồn tại dữ liệu cũ. "
            "Evidence: so sánh dump 2 thời điểm + ảnh UI."),

    tc("Hồi quy & môi trường", "DATA-BACKUP-001", "Normal",
       "Tính năng sao chép dữ liệu không bị ảnh hưởng bởi bảng/cột mới của tính năng đổi LOA",
       ("- Có 2 bot A và B cùng Admin, đều Standard\n"
        "- Bot A có dữ liệu đầy đủ và đã từng đổi LOA"),
       "1. Với bot A (đã từng đổi LOA), vào /basic/backup\n"
       "2. Thực hiện sao chép dữ liệu từ A sang B theo luồng chuẩn\n"
       "3. Chờ job sao chép hoàn tất\n"
       "4. Kiểm tra dữ liệu bot B: đủ các loại dữ liệu đã copy\n"
       "5. Kiểm tra bot B có bị copy nhầm bản ghi đặt lịch đổi LOA / cột đổi LOA của bot A không",
       "bot A đã từng đổi LOA, có dữ liệu đầy đủ; bot B là đích",
       "- Sao chép dữ liệu hoàn tất, không lỗi\n"
       "- Bot B có đủ dữ liệu đã copy theo đúng danh sách của tính năng sao chép\n"
       "- Bot B KHÔNG bị copy bản ghi đặt lịch đổi LOA của bot A\n"
       "- Bot B KHÔNG thừa hưởng cột đổi LOA (id_bot_change) của bot A",
       note="⚠️ Đây là TC BỔ SUNG của AI theo DATA-BACKUP-001 ('BẮT BUỘC khi tính năng thêm/đổi bảng DB, "
            "hoặc chạm backup / copy bot'): tính năng đổi LOA thêm bảng/cột mới nên phải rà tương tác với "
            "tính năng sao chép dữ liệu (FA-033). KHÔNG có nguồn TC nào cover điểm này → cần Leader xác nhận "
            "có đưa vào bộ chính thức. RULE-08. Evidence: query DB bot B sau khi copy.",
       spec="Đã hỏi leader", **PRD),

    tc("Hồi quy & môi trường", "ENV-003", "Normal",
       "Webhook URL và LIFF ID sinh ra khi đổi LOA đúng domain của TỪNG môi trường",
       ("- Có quyền chạy flow đổi LOA trên nhiều môi trường (dev / staging / production)\n"
        "- Biết domain callback mong đợi của từng môi trường"),
       "1. Trên môi trường dev: chạy tới bước webhook, ghi lại Webhook URL hiển thị\n"
       "2. Trên staging: lặp lại, ghi Webhook URL\n"
       "3. Trên production: lặp lại, ghi Webhook URL\n"
       "4. Đối chiếu 3 URL với domain mong đợi của từng môi trường\n"
       "5. Sau khi đổi LOA trên production: kiểm tra LIFF endpoint URL của 2 LIFF app mới",
       "3 môi trường: dev · staging · production",
       "- Webhook URL của từng môi trường dùng ĐÚNG domain của môi trường đó, không lẫn\n"
       "- Production KHÔNG dùng domain dev/staging (nếu lẫn → webhook LINE gọi sai server)\n"
       "- LIFF endpoint URL của 2 LIFF app mới cũng đúng domain production\n"
       "- Không URL nào còn chứa domain cũ sau khi đổi LOA",
       note="⚠️ TC BỔ SUNG của AI theo ENV-003 ('BẮT BUỘC khi tính năng chạm media/file, URL/domain, job nền, "
            "thanh toán' — không được đánh × với lý do 'staging đã pass', RULE-08). Nguồn đối chiếu: "
            "Change bot r291 ghi Webhook URL dev là https://lme.watermeru.com/line/callback/add/0. "
            "KHÔNG có nguồn TC nào kiểm chéo 3 môi trường → cần Leader xác nhận. "
            "Evidence: 3 ảnh Webhook URL theo môi trường + ảnh LIFF endpoint URL.",
       spec="Đã hỏi leader", **PRD),

    tc("Hồi quy & môi trường", "JOB-001", "Normal",
       "Job dọn dữ liệu khi đổi LOA chạy đúng trên production với nhiều bản ghi xếp hàng",
       ("- Có quyền xem log/trạng thái job nền trên production\n"
        "- Có thể tạo ≥3 yêu cầu đổi LOA gần nhau (3 bot khác nhau)"),
       "1. Tạo ≥3 yêu cầu đổi LOA cho 3 bot khác nhau trong vòng 5 phút\n"
       "2. Query bảng hàng đợi đếm số bản ghi ở trạng thái chờ\n"
       "3. Theo dõi log job dọn dữ liệu\n"
       "4. Ghi lại thời gian từ lúc vào hàng đợi tới lúc xử lý xong của từng bản ghi\n"
       "5. Kiểm tra CẢ 3 bot: dữ liệu bot cũ đã bị xóa đủ chưa\n"
       "6. Kiểm tra không có bản ghi nào bị bỏ sót trong hàng đợi",
       "3 yêu cầu đổi LOA trong 5 phút",
       "- CẢ 3 bản ghi trong hàng đợi đều được xử lý, không bản ghi nào bị bỏ sót\n"
       "- Dữ liệu bot cũ của CẢ 3 bot bị xóa đủ theo danh sách bảng\n"
       "- Job không bị treo/chết khi có nhiều bản ghi\n"
       "- Log không có lỗi chưa xử lý",
       note="⚠️ TC BỔ SUNG của AI theo JOB-001 ('BẮT BUỘC khi tính năng thêm/sửa job nền'). "
            "Nguồn đối chiếu spec: lesson-booking/job/job-spec.md §2.6 — job poll "
            "findTop50ByStatusOrderByIdAsc(STATUS_WAITING) theo nhịp SCAN_INTERVAL_MS / PER_RECORD_DELAY_MS, "
            "lỗi thì ERROR_BACKOFF_MS ⇒ có cơ chế xếp hàng 50 bản ghi/lượt và backoff khi lỗi, "
            "nhưng KHÔNG nguồn TC nào kiểm nhánh nhiều bản ghi. RULE-08 (job nền → PRODUCTION). "
            "Evidence: query hàng đợi theo thời gian + log job + query dữ liệu 3 bot.",
       spec="Đã hỏi leader", **PRD),

    tc("Hồi quy & môi trường", "DEPLOY-LIVE-001", "Normal",
       "Release tính năng đổi LOA lên production không bật bảo trì — yêu cầu đang dở không bị lỗi",
       ("- Biết thời điểm release lên production\n"
        "- Có 1 phiên đổi LOA đang ở giữa flow (bước nhập thông tin) lúc release diễn ra"),
       "1. Trước release: mở flow đổi LOA tới bước nhập thông tin, nhập 4 field, KHÔNG submit\n"
       "2. Giữ nguyên tab, chờ release được deploy\n"
       "3. Sau release: bấm nút đi tiếp ở tab đang mở\n"
       "4. Quan sát kết quả (thành công / lỗi / bị đá về đầu flow)\n"
       "5. Kiểm tra đặt lịch đổi LOA đang active trước release có còn dùng được\n"
       "6. Kiểm tra job dọn dữ liệu đang chạy lúc release có hoàn tất không",
       "1 phiên đang ở bước nhập thông tin + 1 đặt lịch active + 1 job đang chạy lúc release",
       "- Phiên đang dở: hoặc đi tiếp được, hoặc bị đá về đầu flow với thông báo RÕ RÀNG — "
       "KHÔNG lỗi 500, KHÔNG trang trắng\n"
       "- Đặt lịch active trước release: vẫn hiển thị và dùng được\n"
       "- Job đang chạy lúc release: hoàn tất, không để lại dữ liệu nửa vời\n"
       "- Không bot nào bị kẹt ở trạng thái đang-xử-lý sau release",
       note="⚠️ TC BỔ SUNG của AI theo DEPLOY-LIVE-001 ('BẮT BUỘC với mọi release lên production không bật "
            "maintain, đặc biệt khi đổi payload API / field form / cấu trúc request') + REG-RUN-001. "
            "Nguồn đối chiếu: TC-CBF-115 chỉ kiểm đặt lịch qua release, KHÔNG kiểm phiên đang dở và job "
            "đang chạy → đây là khoảng trống. Cần Leader xác nhận. RULE-08. "
            "Evidence: ảnh kết quả ở tab đang dở + query đặt lịch + log job qua mốc release.",
       spec="Đã hỏi leader", **PRD),

    tc("Hồi quy & môi trường", "DEPLOY-ASSET-001", "Normal",
       "Release đổi JS/CSS của wizard — trình duyệt không dùng bản cache cũ gây lỗi giao diện",
       ("- Đã mở màn wizard đổi LOA TRƯỚC release (đã cache JS/CSS cũ)\n"
        "- Đợt release có sửa file JS/CSS của wizard"),
       "1. Trước release: mở flow đổi LOA để trình duyệt cache JS/CSS, KHÔNG đóng tab\n"
       "2. Sau release: bấm F5 thường (không hard reload)\n"
       "3. Quan sát giao diện wizard và Console\n"
       "4. Kiểm tra các nút, validate 4 field, enable/disable CTA có chạy đúng không\n"
       "5. So sánh với trạng thái sau khi hard reload (Ctrl+Shift+R)",
       "F5 thường vs hard reload sau release",
       "- Sau F5 thường: giao diện và hành vi ĐÚNG như sau hard reload (không lệch)\n"
       "- Console KHÔNG có lỗi JS do file cache cũ gọi hàm không còn tồn tại\n"
       "- Validate 4 field và enable/disable CTA vẫn chạy đúng\n"
       "- Không phải dặn user hard reload mới dùng được",
       note="⚠️ TC BỔ SUNG của AI theo DEPLOY-ASSET-001 ('BẮT BUỘC khi release có sửa file JS/CSS/font/icon "
            "hoặc đổi cấu trúc dữ liệu mà GUI render'). KHÔNG nguồn TC nào cover → cần Leader xác nhận. "
            "RULE-08. Evidence: ảnh giao diện sau F5 + sau hard reload + ảnh Console.",
       spec="Đã hỏi leader", **PRD),
]
