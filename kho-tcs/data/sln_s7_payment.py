# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Nhóm 41-43: 決済連携 (cài đặt), thanh toán bằng thẻ + 3D Secure, 現地決済.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Liên kết bill tiền」(232 TC lá — setting phía admin, ma trận tính tiền course + staff,
    Stripe 3D Secure, UnivaPay, calendar thường và calendar private)
  - tab「Improve bill tiền stripe」(72) ·「Improve bill tiền univapay」(170) ·
    「Bill tiền Univapay(#32856)」(78 — action lúc booking không fill friend info)
  - tab「Quản lý calendar」r2781-r2825 (Feature #27976 mục 3: thêm 現地決済)
"""
from _common import tc

PAY = ("- Đăng nhập admin (主管理者) bot A, plan có phí (standard trở lên)\n"
       "- Calendar「サロンA」loại スタッフ, course C1 5,000 yên, staff S1 phụ phí 1,000 yên\n"
       "- Đã bật 2 câu hỏi mặc định 名前 + メール ở tab 質問項目\n"
       "- Mở /basic/calendar-salon/{id} → tab「決済連携」")

S7 = [
    # ══════════════ 41. 決済連携 — cài đặt ══════════════
    tc("決済連携 — cài đặt", "PAY-LIMIT-001", "Abnormal",
       "Bot plan free không bật được 決済",
       PAY.replace("plan có phí (standard trở lên)", "plan FREE"),
       "1. Mở tab 決済連携 → bật「決済機能の利用」→ lưu\n2. Đọc thông báo",
       "Bot plan free",
       "- Lỗi「決済機能のご利用には有料プランへのアップグレードが必要です。」\n- Không bật được 決済",
       note="Nguồn: Liên kết bill tiền r7. Spec BR-05."),

    tc("決済連携 — cài đặt", "PAY-LIMIT-001", "Abnormal",
       "Chưa liên kết Stripe/UnivaPay → không bật được 決済, hiện hướng dẫn liên kết",
       PAY + "\n- Bot A CHƯA liên kết Stripe và UnivaPay",
       "1. Mở tab 決済連携 → quan sát\n2. Đóng popup hướng dẫn → bật 決済 lần nữa\n"
       "3. Kiểm tra dropdown chọn nhà cung cấp",
       "Chưa có bản ghi StripBot",
       "- `checkLinkPayment` = true → hiện hướng dẫn liên kết Stripe/UnivaPay\n"
       "- Đóng popup rồi bật lại: hiện lại popup hướng dẫn\n"
       "- Nhà cung cấp chưa liên kết KHÔNG hiện trong dropdown lựa chọn",
       note="Nguồn: Liên kết bill tiền r10, r86-r87. Spec BR-05, EP-17."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Normal",
       "Form cài đặt 決済 — 5 trường và ràng buộc khoá nhà cung cấp",
       PAY + "\n- Đã liên kết cả Stripe và UnivaPay",
       "1. Bật「決済機能の利用」→ chọn Stripe → chọn môi trường テスト → chọn 予約時決済の選択 → lưu\n"
       "2. Reload → thử đổi nhà cung cấp sang UnivaPay\n"
       "3. Đổi môi trường sang 本番 → lưu\n4. Đổi 予約時決済の選択 → lưu",
       "Stripe + môi trường test",
       "- Lưu thành công, các giá trị ghi đúng vào `calendar_salon`\n"
       "- Sau khi lưu lần đầu: KHÔNG đổi được nhà cung cấp nữa\n"
       "- Môi trường và phương thức thanh toán: vẫn đổi được",
       note="Nguồn: Spec feature-spec.md §2.5 + Liên kết bill tiền r4-r17. EP-18."),

    tc("決済連携 — cài đặt", "UI-001", "Normal",
       "Nội dung 特定商取引法に基づく表記 (TinyMCE) hiển thị phía LINE user",
       PAY + "\n- Đã bật 決済",
       "1. Bỏ trống nội dung → lưu → LINE user mở màn 特定商取引法に関する記載\n"
       "2. Nhập 5000 ký tự tiếng Nhật kèm định dạng (bold, italic, căn lề, màu chữ) → lưu → "
       "LINE user mở lại màn\n3. Kiểm tra ở cả môi trường test và production",
       "Nội dung 5000 ký tự có định dạng HTML",
       "- Bỏ trống: màn 特定商取引法に関する記載 phía LINE user KHÔNG hiển thị nội dung gì\n"
       "- Có nội dung: hiển thị đúng text và đầy đủ các thuộc tính định dạng (bold, italic, "
       "căn trái/phải/giữa/đều, màu chữ)",
       note="Nguồn: Liên kết bill tiền r18-r19, r31. Spec Field #53 (SC-005 TinyMCE)."),

    tc("決済連携 — cài đặt", "DATA-AUDIT-001", "Normal",
       "Lịch sử thay đổi cài đặt 決済 (決済利用 変更履歴)",
       PAY + "\n- Đã đổi trạng thái 決済 nhiều lần bởi các admin khác nhau",
       "1. Bật 決済 với môi trường テスト → xem lịch sử\n2. Đổi sang môi trường 本番 → xem lịch sử\n"
       "3. Tắt 決済 → xem lịch sử\n4. Đối chiếu cột ngày giờ / người thao tác / nội dung",
       "≥ 3 lần thay đổi",
       "- Mỗi lần đổi sinh 1 bản ghi trong `calendar_salon_history_change_setting_payment`\n"
       "- Cột 日時 = `created_at`, 操作した人 = tên admin, 内容 = dạng「停止 → 利用中(テスト環境)」\n"
       "- Đổi môi trường cũng sinh bản ghi (本番 → テスト và ngược lại)",
       note="Nguồn: Liên kết bill tiền r72-r80, r212-r220. Spec BR-06."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Abnormal",
       "Account TẮT 決済 nhưng course/staff vẫn có giá → không bill nhưng vẫn hiện số tiền",
       PAY + "\n- Calendar TẮT「決済機能の利用」\n- Course C1 có giá 5,000, staff S1 phụ phí 1,000",
       "1. LINE user đặt lịch với C1 + S1\n2. Quan sát các màn phía LINE user\n"
       "3. Kiểm tra `payment_status` của booking",
       "Course và staff có giá, 決済 tắt",
       "- LINE user đặt lịch bình thường, KHÔNG qua bước nhập thẻ\n"
       "- VẪN hiển thị số tiền của course và staff (nếu cài đặt hiển thị giá)\n"
       "- Booking không phát sinh thanh toán, cột 決済 hiện「決済なし」",
       note="Nguồn: Liên kết bill tiền r5-r6."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Abnormal",
       "Đã bật 決済 rồi HỦY liên kết Stripe/UnivaPay → bỏ qua bước nhập thẻ",
       PAY + "\n- Calendar đã bật 決済 với Stripe (hoặc UnivaPay)",
       "1. Vào màn liên kết → hủy liên kết Stripe\n"
       "2. LINE user đặt lịch với course có giá → quan sát luồng\n"
       "3. Lặp lại với UnivaPay",
       "Đã hủy liên kết nhà cung cấp",
       "- Bỏ qua bước nhập thẻ, LINE user đi thẳng đến bước xác nhận đặt lịch\n"
       "- Booking tạo thành công, không phát sinh thanh toán",
       note="Nguồn: Liên kết bill tiền r16-r17."),

    tc("決済連携 — cài đặt", "PAY-AMOUNT-001", "Boundary",
       "Ma trận tính số tiền bill = giá course + phụ phí staff",
       PAY + "\n- Calendar đã bật 決済 môi trường テスト",
       "1. Course không giá + staff không phụ phí → LINE user đặt\n"
       "2. Course 5,000 + staff không phụ phí → đặt\n3. Course không giá + staff 1,000 → đặt\n"
       "4. Course 5,000 + staff 1,000 → đặt\n5. Chọn course 5,000 + staff 指定なし → đặt\n"
       "6. Không dùng course + chọn staff 1,000 → đặt\n"
       "7. Không dùng course + staff 指定なし → đặt",
       "Course 0/5,000 · staff 0/1,000",
       "- B1: KHÔNG hiện màn bill, đi thẳng bước xác nhận\n- B2: bill 5,000\n- B3: bill 1,000\n"
       "- B4: bill 6,000\n- B5: bill 5,000 (staff 指定なし không có phụ phí)\n"
       "- B6: bill 1,000\n- B7: KHÔNG bill",
       note="Nguồn: Liên kết bill tiền r21-r27, r45-r51 (có phép tính tay — RULE-05)."),

    tc("決済連携 — cài đặt", "PAY-AMOUNT-001", "Normal",
       "TẮT 決済 ở account → mọi tổ hợp course/staff đều không bill",
       PAY + "\n- Admin DISABLE liên kết 決済 ở cấp account",
       "1. Có dùng course: thử 4 tổ hợp (course có/không giá × staff có/không phụ phí) → LINE user đặt\n"
       "2. Chọn course + staff 指定なし → đặt\n"
       "3. Không dùng course: chọn staff có phí / không phí / 指定なし → đặt\n"
       "4. Với mỗi trường hợp, kiểm tra `payment_system` và `payment_status` của booking",
       "8 tổ hợp",
       "- Tất cả: booking THÀNH CÔNG, KHÔNG bill tiền\n"
       "- `payment_status` = 2 (決済なし), `payment_system` không ghi nhà cung cấp",
       spec="Đã hỏi leader",
       note="Nguồn: Liên kết bill tiền r90-r97. ⚠ Corpus để dấu hỏi「payment_system = NULL?」→ "
            "giá trị DB chưa được xác nhận, xem MT-36."),

    # ══════════════ 42. 決済 — thẻ & 3D Secure ══════════════
    tc("決済 — thẻ & 3D Secure", "PAY-STATE-001", "Normal",
       "Stripe môi trường TEST: đặt lịch có thanh toán bằng thẻ test",
       PAY + "\n- Đã bật 決済 Stripe, môi trường テスト\n- Course C1 5,000 yên",
       "1. LINE user đặt lịch chọn C1 → đến màn nhập thẻ\n"
       "2. Nhập thẻ test hợp lệ → xác nhận đặt lịch\n"
       "3. Kiểm tra `payment_status`, `payment_amount`, thông tin thẻ ở detail booking\n"
       "4. Kiểm tra dashboard Stripe (test mode)\n5. Kiểm tra tin nhắn LINE user nhận",
       "Thẻ test Stripe hợp lệ",
       "- Thanh toán thành công, booking tạo với `payment_amount` = 5000\n"
       "- Detail booking hiện số thẻ「XXXXXXXX1234」, hạn thẻ, hệ thống thanh toán = Stripe\n"
       "- Dashboard Stripe (test) có giao dịch tương ứng\n- LINE user nhận tin nhắn hoàn tất",
       note="Nguồn: Liên kết bill tiền r22-r24, r90-r136. RULE-07 (3 tầng: DB + màn hình + Stripe)."),

    tc("決済 — thẻ & 3D Secure", "PAY-STATE-001", "Abnormal",
       "Stripe môi trường TEST: nhập thẻ THẬT → bị từ chối",
       PAY + "\n- Đã bật 決済 Stripe, môi trường テスト",
       "1. LINE user đặt lịch đến màn nhập thẻ → nhập thẻ thật → xác nhận\n2. Đọc thông báo lỗi\n"
       "3. Kiểm tra booking có được tạo không",
       "Thẻ thật",
       "- Lỗi「Your card was declined. Your request was in test mode, but used a non test (live) card. …」\n"
       "- KHÔNG tạo booking",
       note="Nguồn: Liên kết bill tiền r28."),

    tc("決済 — thẻ & 3D Secure", "FUNC-003", "Boundary",
       "Giới hạn brand thẻ theo cài đặt ở màn list-item (Stripe)",
       PAY + "\n- Đã bật 決済 Stripe\n- Ở màn cài đặt chọn brand: visa + master + amex",
       "1. LINE user vào màn nhập thẻ → quan sát icon brand\n"
       "2. Nhập thẻ visa / master / amex → xác nhận\n"
       "3. Nhập thẻ JCB / diners club → xác nhận\n"
       "4. Đổi cài đặt sang đủ 5 brand → lặp lại bước 1-3",
       "Thẻ test 5 brand",
       "- Cài 3 brand: icon hiện đúng 3 brand; thẻ trong 3 brand → pass; ngoài 3 brand → báo lỗi\n"
       "- Cài 5 brand: icon hiện đủ 5; cả 5 brand đều pass",
       note="Nguồn: Liên kết bill tiền r29-r30."),

    tc("決済 — thẻ & 3D Secure", "FUNC-003", "Normal",
       "UnivaPay: giới hạn brand chỉ ảnh hưởng ICON, không chặn thẻ",
       PAY + "\n- Đã bật 決済 UnivaPay môi trường テスト",
       "1. Cài chỉ chọn brand visa → LINE user vào màn nhập thẻ → quan sát icon\n"
       "2. Lần lượt cài từng brand master / amex / JCB / diners và cài cả 5 brand → quan sát icon\n"
       "3. Nhập thẻ THẬT ở môi trường test → xác nhận",
       "Thẻ test và thẻ thật UnivaPay",
       "- Icon brand hiển thị đúng theo cài đặt\n"
       "- UnivaPay CHỈ kiểm tra được phần hiển thị icon, không chặn brand ở tầng nhập thẻ\n"
       "- Nhập thẻ thật ở môi trường test: VẪN bill thành công (khác Stripe)",
       note="Nguồn: Liên kết bill tiền r52-r58. ⚠ Hành vi UnivaPay khác Stripe rõ rệt — nêu rõ khi test."),

    tc("決済 — thẻ & 3D Secure", "UI-001", "Normal",
       "Popup danh sách thẻ dummy テスト決済時のダミーカード番号一覧",
       PAY + "\n- Đã bật 決済 môi trường テスト",
       "1. LINE user vào màn nhập thẻ → bấm「テスト決済時のダミーカード番号一覧」\n"
       "2. Quan sát popup\n3. Bấm X / bấm「閉じる」",
       "-",
       "- Popup hiển thị giữa màn hình, nền phía sau tối đi\n"
       "- Bấm X hoặc 閉じる: đóng popup",
       note="Nguồn: Liên kết bill tiền r70."),

    tc("決済 — thẻ & 3D Secure", "PAY-ABANDON-001", "Normal",
       "Stripe 3D Secure: luồng xác thực thêm khi đặt lịch",
       PAY + "\n- Đã bật 決済 Stripe (Stripe có 3D Secure)",
       "1. LINE user đặt lịch, nhập thẻ test YÊU CẦU 3D Secure → xác nhận\n"
       "2. Hoàn tất bước xác thực 3D Secure → quan sát\n"
       "3. Lặp lại nhưng HỦY / thất bại ở bước 3D Secure\n"
       "4. Kiểm tra booking và `payment_status` ở cả 2 nhánh",
       "Thẻ test yêu cầu 3D Secure",
       "- Nhánh xác thực thành công: booking tạo, thanh toán thành công\n"
       "- Nhánh hủy/thất bại: KHÔNG tạo booking (hoặc booking không được thanh toán), "
       "hiển thị lỗi rõ ràng, không để lại dữ liệu nửa vời",
       note="Nguồn: Liên kết bill tiền r90-r136 (khối「Test bill tiền stripe môi trường test "
            "(stripe có 3d secure)」)."),

    tc("決済 — thẻ & 3D Secure", "PAY-CONFIRM-001", "Normal",
       "Thanh toán khi booking cần DUYỆT: bill vào lúc admin duyệt",
       PAY + "\n- Đã bật 決済; approve_type = 2 (admin duyệt thủ công)\n- Course C1 5,000 yên",
       "1. LINE user đặt lịch, nhập thẻ → xác nhận → kiểm tra `payment_status`\n"
       "2. Admin duyệt booking → kiểm tra `payment_status` và dashboard nhà cung cấp\n"
       "3. Lặp lại nhưng admin TỪ CHỐI booking → kiểm tra",
       "Booking chờ duyệt, course có giá",
       "- Sau khi user đặt: `payment_status` = 0 (未決済), chưa trừ tiền\n"
       "- Sau khi admin duyệt: `payment_status` = 1 (決済成功), giao dịch xuất hiện trên dashboard\n"
       "- Admin từ chối: KHÔNG bill tiền",
       note="Nguồn: Quản lý calendar r1362-r1365 + Setting calendar r1575-r1576."),

    tc("決済 — thẻ & 3D Secure", "PAY-STATE-001", "Abnormal",
       "Chưa liên kết nhà cung cấp nhưng calendar cấu hình 決済 → booking vẫn thành công",
       PAY + "\n- Ở màn liên kết: CHƯA liên kết cả Stripe lẫn UnivaPay",
       "1. LINE user đặt lịch được duyệt ngay → quan sát\n"
       "2. LINE user đặt lịch chờ duyệt → quan sát\n3. Admin duyệt booking đó → quan sát\n"
       "4. Admin từ chối booking đó → quan sát",
       "Chưa liên kết nhà cung cấp",
       "- Cả 4 trường hợp: booking THÀNH CÔNG, không phát sinh thanh toán, không lỗi màn",
       note="Nguồn: Liên kết bill tiền r82-r85."),

    tc("決済 — thẻ & 3D Secure", "PAY-STATE-001", "Abnormal",
       "Chọn nhà cung cấp CHƯA liên kết → không hiện màn nhập thẻ",
       PAY + "\n- Chỉ liên kết UnivaPay; calendar chọn Stripe (hoặc ngược lại)",
       "1. LINE user đặt lịch mới → đến bước thanh toán → quan sát\n"
       "2. Với booking đã đặt TRƯỚC đó có thông tin thẻ, admin duyệt → kiểm tra thanh toán",
       "Nhà cung cấp lệch với liên kết",
       "- Booking mới: màn nhập thẻ KHÔNG hiển thị được phần nhập thẻ\n"
       "- Booking cũ có thông tin thẻ: vẫn bill được (cần xác nhận rõ hành vi mong muốn)",
       spec="Đã hỏi leader",
       note="Nguồn: Liên kết bill tiền r86-r89. ⚠ Corpus để dấu hỏi「vẫn bill tiền do có thông tin card ?」"
            "→ cần Leader chốt, xem MT-37."),

    tc("決済 — thẻ & 3D Secure", "PAY-AMOUNT-001", "Normal",
       "Bill tiền ở calendar loại 個人 — số tiền chỉ tính theo course",
       PAY.replace("loại スタッフ", "loại 個人") + "\n- Calendar 個人 đã bật 決済",
       "1. Course C1 5,000 yên → LINE user đặt lịch có thanh toán\n"
       "2. Course không giá → LINE user đặt lịch\n"
       "3. Kiểm tra `payment_amount` và trạng thái thanh toán\n"
       "4. Kiểm tra lịch sử thay đổi cài đặt 決済 của calendar 個人",
       "Calendar 個人, course có/không giá",
       "- Course có giá: bill đúng giá course (KHÔNG có phụ phí staff)\n"
       "- Course không giá: không bill, đi thẳng bước xác nhận\n"
       "- Lịch sử thay đổi cài đặt hoạt động giống calendar loại スタッフ",
       note="Nguồn: Liên kết bill tiền r174-r305."),

    tc("決済 — thẻ & 3D Secure", "ENV-003", "Normal",
       "Thanh toán trên môi trường PRODUCTION với Stripe và UnivaPay",
       "- Bot production đã liên kết Stripe / UnivaPay môi trường 本番\n"
       "- Calendar bật 決済, course giá nhỏ nhất có thể",
       "1. LINE user thật đặt lịch, nhập thẻ THẬT → xác nhận\n"
       "2. Kiểm tra `payment_status` và dashboard nhà cung cấp\n"
       "3. Kiểm tra thông báo trừ tiền trên app ngân hàng\n"
       "4. Đối chiếu cột 決済ステータス trong Google Sheet\n5. Lặp lại với nhà cung cấp còn lại",
       "Thẻ thật, số tiền nhỏ nhất",
       "- Thanh toán thành công thật sự, tiền được trừ đúng số\n"
       "- `payment_status` = 1, dashboard nhà cung cấp có giao dịch\n"
       "- Google Sheet ghi「決済済み」",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r31-r37, r62-r65, r173, r305. RULE-08: bill tiền BẮT BUỘC "
            "test production."),

    tc("決済 — thẻ & 3D Secure", "INTG-HOOK-002", "Normal",
       "SpecImprove #34895: giảm thời gian chờ kiểm tra UnivaPay khi đặt lịch",
       PAY + "\n- Đã bật 決済 UnivaPay",
       "1. LINE user đặt lịch có thanh toán → đo thời gian từ lúc bấm xác nhận đến khi hoàn tất\n"
       "2. Kiểm tra booking và trạng thái thanh toán\n"
       "3. Lặp lại với trường hợp UnivaPay dùng webhook và không dùng webhook",
       "UnivaPay có/không webhook",
       "- Thời gian chờ giảm rõ rệt so với trước, không treo màn\n"
       "- Booking và trạng thái thanh toán vẫn đúng ở cả 2 cấu hình webhook",
       env="PRODUCTION",
       note="Nguồn: Info r48 (SpecImprove #34895, 03/2026) + Booking phía line user r1424-r1425. "
            "RULE-08."),

    tc("決済 — thẻ & 3D Secure", "FRIEND-001", "Abnormal",
       "Bug #32856: action lúc booking KHÔNG fill thông tin friend info (luồng UnivaPay)",
       PAY + "\n- Đã bật 決済 UnivaPay\n"
             "- Action lúc booking có chèn token friend info (tên, email…)",
       "1. LINE user đặt lịch có thanh toán UnivaPay và điền form friend info\n"
       "2. Đọc tin nhắn action nhận được trên LINE\n"
       "3. Kiểm tra friend info của khách trên tool\n"
       "4. Lặp lại với luồng KHÔNG thanh toán để đối chiếu",
       "Action có token friend info",
       "- Tin nhắn action phải chèn ĐỦ thông tin friend info khách vừa nhập\n"
       "- Friend info của khách được cập nhật đúng\n"
       "- Kết quả giống luồng không thanh toán",
       note="Nguồn: tab「Bill tiền Univapay(#32856)」(Bug #32856, 19/11/2025)."),

    tc("決済 — thẻ & 3D Secure", "OUT-TRUTH-001", "Normal",
       "Feature #31268: ẩn bớt text về thẻ khi calendar không bật 決済 hoặc course/staff miễn phí",
       PAY,
       "1. Calendar KHÔNG bật 決済 → LINE user đến màn xác nhận request booking và màn hoàn tất → đọc text\n"
       "2. Calendar BẬT 決済 nhưng course + staff KHÔNG có giá → đọc text ở 2 màn\n"
       "3. Calendar BẬT 決済 và course + staff CÓ giá → đọc text ở 2 màn\n"
       "4. Lặp lại với calendar loại 個人",
       "3 cấu hình giá",
       "- B1, B2: BỎ text「※前ページでカード情報を入力された方は、リクエストが承認された時に、"
       "カード決済が行われます。」và「※予約時にカード情報を入力された方は、リクエストが承認された時に、"
       "カード決済が行われます。」\n"
       "- B3: GIỮ NGUYÊN 2 text trên\n- Calendar 個人 cho kết quả tương tự",
       note="Nguồn: Booking phía line user r1259-r1270 (Feature #31268, 27/01/2026)."),

    tc("決済 — thẻ & 3D Secure", "PAY-BATCH-001", "Normal",
       "Duyệt HÀNG LOẠT booking có thanh toán → re-check trạng thái mới nhất trước khi bill",
       PAY + "\n- approve_type = 2; có 3 booking 予約リクエスト đều có thẻ và course 5,000 yên\n"
             "- 1 trong 3 booking vừa được hoàn tiền / hủy ở tab khác",
       "1. Tick cả 3 booking → 一括操作 → 承認する → thực thi\n"
       "2. Kiểm tra `payment_status` của từng booking\n3. Kiểm tra dashboard nhà cung cấp\n"
       "4. Đối chiếu số giao dịch phát sinh với số booking thực sự được duyệt",
       "3 booking, 1 booking đã đổi trạng thái ở luồng khác",
       "- Hệ thống kiểm tra lại trạng thái thanh toán MỚI NHẤT trước khi bill từng booking\n"
       "- Booking đã hủy/hoàn tiền KHÔNG bị bill lại\n"
       "- Số giao dịch trên dashboard khớp đúng số booking được duyệt (không bill thừa)",
       env="PRODUCTION",
       note="Spec §2.2a (`changeStatusBooking` — 「nếu có thanh toán liên quan → kiểm tra paymentStatus」). "
            "⚠ Corpus KHÔNG có TC cho nhánh re-check khi duyệt hàng loạt → TC bổ sung theo spec. RULE-08."),

    tc("決済連携 — cài đặt", "PAY-PLAN-001", "Abnormal",
       "Hạ gói xuống free khi đang vượt giới hạn calendar / course / staff",
       PAY + "\n- Bot A plan pro, đang có 5 calendar, mỗi calendar 5 course và 5 staff",
       "1. Hạ gói bot A xuống free\n2. Mở màn list calendar → quan sát danh sách và bộ đếm\n"
       "3. Mở 1 calendar → quan sát course/staff\n4. Thử tạo calendar / course / staff mới\n"
       "5. LINE user mở link đặt lịch của các calendar vượt giới hạn\n"
       "6. Kiểm tra chức năng 決済 (chỉ dành cho gói có phí)",
       "Bot vượt giới hạn free sau khi hạ gói",
       "- Dữ liệu cũ KHÔNG bị xóa\n- Không tạo thêm được (báo lỗi giới hạn plan)\n"
       "- Chức năng 決済 bị chặn theo gói free\n"
       "- Hành vi phía LINE user với các calendar vượt giới hạn phải rõ ràng, không lỗi màn trắng",
       spec="Đã hỏi leader",
       note="Spec BR-01/BR-02 chỉ mô tả giới hạn khi TẠO MỚI, KHÔNG mô tả hành vi khi HẠ GÓI. "
            "⚠ Corpus KHÔNG có TC cho nhánh này → TC bổ sung, cần Leader chốt (xem MT-02)."),

    # ══════════════ 43. 現地決済 ══════════════
    tc("現地決済", "PAY-STATE-001", "Normal",
       "Cài đặt 予約時決済の選択 = 選択可能 → LINE user thấy 2 lựa chọn thanh toán",
       PAY + "\n- Đã bật 決済; `payment_time` = 2 (選択可能)\n- Course C1 5,000 yên",
       "1. LINE user đặt lịch chọn C1 → đến bước thanh toán → quan sát\n"
       "2. Đổi `payment_time` = 1 (thanh toán trước のみ) → LINE user đặt lại → quan sát",
       "payment_time = 1 và 2",
       "- payment_time = 2: hiện 2 lựa chọn「thanh toán trước」và「thanh toán tại chỗ」\n"
       "- payment_time = 1: chỉ có luồng nhập thẻ, không có lựa chọn tại chỗ",
       note="Nguồn: Quản lý calendar r2796 + Spec Field #52. "
            "⚠ Spec §9.1 mục 1 ghi 現地決済 KHÔNG có constants trong source → MT-12."),

    tc("現地決済", "PAY-STATE-001", "Normal",
       "Chọn thanh toán TRƯỚC khi có 2 lựa chọn → luồng thẻ như bình thường",
       PAY + "\n- payment_time = 2; course C1 5,000 yên",
       "1. LINE user chọn「thanh toán trước」→ nhập thẻ → xác nhận\n"
       "2. Kiểm tra detail booking phía admin\n3. Kiểm tra cột 決済 ở Google Sheet\n"
       "4. Kiểm tra hiển thị phía LINE user",
       "Thẻ test",
       "- Detail booking: hiện số tiền + trạng thái「テスト決済」+ thông tin thẻ; "
       "KHÔNG hiển thị lịch sử cập nhật trạng thái\n"
       "- Google Sheet cột 決済:「テスト決済」\n- LINE user thấy trạng thái「テスト決済」",
       note="Nguồn: Quản lý calendar r2797, r2803."),

    tc("現地決済", "PAY-STATE-001", "Normal",
       "Chọn thanh toán TẠI CHỖ → booking tạo với trạng thái 現地決済：未決済",
       PAY + "\n- payment_time = 2; course C1 5,000 yên",
       "1. LINE user chọn「thanh toán tại chỗ」→ quan sát màn xác nhận\n2. Hoàn tất đặt lịch\n"
       "3. Kiểm tra detail booking phía admin\n4. Kiểm tra Google Sheet\n"
       "5. Kiểm tra hiển thị phía LINE user\n6. Kiểm tra `payment_time` và `payment_status` trong DB",
       "Course 5,000 yên",
       "- Màn xác nhận hiện phần thanh toán tại chỗ theo design\n"
       "- Detail booking admin: số tiền + trạng thái「現地決済：未決済」+ nút cập nhật trạng thái; "
       "chưa có lịch sử cập nhật\n"
       "- Google Sheet: số tiền + trạng thái 現地決済\n"
       "- DB: `payment_time` = 2, `payment_status` = 0",
       note="Nguồn: Quản lý calendar r2798, r2804, r2824."),

    tc("現地決済", "PAY-STATE-001", "Normal",
       "Admin cập nhật trạng thái 現地決済 từ 2 màn — có ghi lịch sử",
       PAY + "\n- Có booking 現地決済：未決済",
       "1. Cập nhật thành「đã thanh toán」từ màn 本日／新着の予約 → kiểm tra\n"
       "2. Cập nhật ngược lại thành「chưa thanh toán」từ màn detail booking → kiểm tra\n"
       "3. Kiểm tra lịch sử cập nhật trạng thái ở detail booking\n"
       "4. Kiểm tra Google Sheet sau mỗi lần cập nhật\n5. Kiểm tra hiển thị phía LINE user",
       "1 booking 現地決済",
       "- Cập nhật được từ CẢ 2 màn\n"
       "- Đã thanh toán: hiện「現地決済：決済済み」, `payment_status` = 1\n"
       "- Chưa thanh toán: hiện「現地決済：未決済」, `payment_status` = 0\n"
       "- Sau khi cập nhật: HIỆN lịch sử cập nhật trạng thái\n"
       "- Google Sheet và màn phía LINE user cập nhật theo",
       note="Nguồn: Quản lý calendar r2799-r2801, r2805-r2806, r2825. "
            "⚠ Corpus đánh NG cho cột Google Sheet ở 2 nhánh (r2800, r2801, r2806) → cần verify lại "
            "giá trị ghi vào Sheet, xem MT-38."),

    tc("現地決済", "PAY-STATE-001", "Normal",
       "Duyệt booking 現地決済 KHÔNG làm đổi trạng thái thanh toán",
       PAY + "\n- approve_type = 2; có booking request chọn 現地決済",
       "1. Admin duyệt booking\n2. Kiểm tra trạng thái thanh toán trước và sau khi duyệt",
       "Booking request + 現地決済",
       "- Sau khi duyệt: các trạng thái thanh toán VẪN giữ nguyên (không tự chuyển sang đã thanh toán)",
       note="Nguồn: Quản lý calendar r2807."),

    tc("現地決済", "PAY-AMOUNT-001", "Normal",
       "Admin book / random staff: lấy giá tại thời điểm booking cho 指定なし",
       PAY + "\n- Đã bật 決済 và bật random staff (option 2 hoặc 3)",
       "1. LINE user đặt lịch chọn 指定なし → hệ thống random vào S1 (phụ phí 1,000)\n"
       "2. Kiểm tra `amount` / `payment_amount` của booking\n"
       "3. Lặp lại với admin đặt lịch chọn 指定なし",
       "Random staff bật, S1 có phụ phí",
       "- Số tiền lấy tại THỜI ĐIỂM BOOKING cho 指定なし (không cộng phụ phí của staff được random sau)\n"
       "- Trường `amount` của `calendar_salon_line_booking` ghi đúng giá trị tại thời điểm đặt",
       note="Nguồn: Quản lý calendar r2791-r2792, r2808-r2809. ⚠ Đây là điểm dễ hiểu nhầm: khách bị "
            "tính tiền theo 指定なし dù cuối cùng được gán staff có phụ phí — cần Leader xác nhận có "
            "đúng ý đồ nghiệp vụ không, xem MT-39."),

    tc("現地決済", "PAY-CONFIRM-001", "Normal",
       "Admin book khi bật 現地決済 — alert cảnh báo không tính phí",
       PAY + "\n- payment_time = 2; course C1 có giá, staff S1 có phụ phí",
       "1. Admin book C1 + S1 → bấm lưu → quan sát alert\n"
       "2. Xác nhận lưu → kiểm tra detail booking\n"
       "3. Admin book course + staff KHÔNG có giá → bấm lưu → quan sát",
       "Course/staff có và không có giá",
       "- Có giá: hiện alert cảnh báo「…有料コースの場合でも、お客様に料金は請求されませんが…」\n"
       "- Sau khi lưu: detail hiện số tiền + trạng thái「決済なし」, không có lịch sử cập nhật\n"
       "- Không có giá: KHÔNG hiện alert, booking thành công",
       note="Nguồn: Quản lý calendar r2785-r2786, r2789-r2790, r2793-r2794."),
]
