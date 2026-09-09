# -*- coding: utf-8 -*-
"""FA-021 イベント予約 — Nhóm 21-24: thanh toán Stripe · UnivaPay · 3D Secure · hoàn tiền.

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Improve bill tiền stripe」(10/2025 → 03/2026) — booking mới + change có bill, job quét kết quả,
    SpecImprove #34857 (description trên Stripe)
  - tab「Improve bill tiền univapay」(04/2025 → 03/2026) — bill kiểu cũ (polling) và kiểu mới (callback),
    Bug KH #33787 (18/01/2026), SpecImprove #34895 (giảm sleep)
  - tab「improve bill tiền 3D secure」(03/2024) — ma trận thẻ 3DS + tổ hợp liên kết/hủy liên kết cổng
  - tab「Task nhỏ + fix bug KH」r85-r92 (bill và số remain), r295-r314 (Bug tự detect #38690 — refund fail)
  - tab「Event booking 1.0」r262-r269, r307-r310, r347-r350 (bill khi duyệt, refund)
"""
from _common import tc

PAY = ("- Bot A đã liên kết Stripe (`status_strip_bot = 3`) và UnivaPay (`univapay_app_id` khác rỗng)\n"
       "- Event E bật「決済機能の利用」, có slot S1 và コース P1 料金 = 5000円\n"
       "- Có tài khoản LINE test U1 là friend của bot A")
STR = PAY + "\n- Event E chọn「利用する決済システム」= Stripe"
UNI = PAY + "\n- Event E chọn「利用する決済システム」= UnivaPay"

S4 = [
    # ══════════════════ 21. Thanh toán — Stripe ══════════════════
    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Event bật 決済 nhưng booking KHÔNG phát sinh tiền → không hiện màn nhập thẻ",
       STR + "\n- Slot S_noplan KHÔNG có コース\n- コース P_free có 料金 để trống",
       "1. U1 đặt 1 chỗ ở slot S_noplan → quan sát có màn nhập thẻ không\n"
       "2. U1 đặt 1 chỗ chọn コース P_free → quan sát\n"
       "3. Tắt 決済 của event rồi đặt 1 chỗ ở コース P1 (5000円) → quan sát",
       "3 trường hợp: slot không コース · コース không 料金 · event tắt 決済",
       "- Cả 3 trường hợp: **KHÔNG hiện màn nhập thẻ**, đặt chỗ xong ngay\n"
       "- `b_user_booking`: `status_payment` = 0, `status_webhook` = 1",
       note="Nguồn: Improve bill tiền stripe r4-r6 + Improve bill tiền univapay r4-r6. "
            "3 input khác nhau nhưng cùng 1 kết quả mong đợi → gộp 1 TC."),

    tc("Thanh toán — Stripe", "PAY-CONFIRM-001", "Normal",
       "Booking リクエスト制 có bill → tạo booking chờ duyệt, CHƯA thu tiền",
       STR + "\n- コース P1 承認方法 = リクエスト制, 料金 5000円",
       "1. U1 đặt 1 chỗ chọn P1, nhập thẻ 4242 4242 4242 4242 → xác nhận\n"
       "2. Query `b_user_booking` bản ghi vừa tạo\n3. Kiểm tra Stripe dashboard",
       "Thẻ hợp lệ, リクエスト制",
       "- `status` = **3** · `status_payment` = **0** · `status_webhook` = **1**\n"
       "- **KHÔNG có giao dịch** trên Stripe dashboard (chưa thu tiền)\n"
       "- Thông tin thẻ được lưu để dùng khi admin duyệt",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r7 + Event booking 1.0 r267「Bill tiền = 0, khi nào admin approve "
            "thì bill tiền」. RULE-08 — bill tiền BẮT BUỘC test PRODUCTION. ⚠ RULE-01: quan điểm `PAY-CONFIRM-001` trong bộ này KHÔNG có loại case **Abnormal, Boundary** — lý do: corpus và spec không mô tả nhánh bất thường nào cho quan điểm này."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Booking 全承認 có bill — trạng thái trung gian ngay khi user bấm đặt chỗ",
       STR + "\n- コース P1 承認方法 = 全承認, 料金 5000円\n- `use_people` S1 = 0, `remain_limit` P1 = 0",
       "1. U1 đặt 1 chỗ chọn P1, nhập thẻ → bấm xác nhận\n"
       "2. NGAY LẬP TỨC query `b_user_booking` bản ghi mới\n3. Đọc `b_slot.use_people` và `b_plan_slot.remain_limit`",
       "全承認, chưa có kết quả bill",
       "- Bản ghi mới: `status` = **5** · `status_payment` = **0** · `status_webhook` = **3**\n"
       "- `use_people` = **+1** · `remain_limit` = **+1** (giữ chỗ trước khi có kết quả bill)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r8. Trạng thái trung gian này quyết định hành vi ở TC bill "
            "success/fail phía dưới."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Bill Stripe THÀNH CÔNG → cập nhật status_payment = 1, gửi action và thêm remind",
       STR + "\n- コース P1 全承認, 料金 5000円\n- Slot bật remind, đã set action「予約完了」",
       "1. U1 đặt 1 chỗ, nhập thẻ 4242 4242 4242 4242 → xác nhận\n"
       "2. Query `b_user_booking`\n3. Query bảng `user_event`\n4. Đọc tin trên LINE app\n"
       "5. Kiểm tra Stripe dashboard",
       "Thẻ success 4242 4242 4242 4242, 5000円",
       "- `status_webhook` = **1** · `status_payment` = **1**\n"
       "- Có gửi action「予約完了」(đọc được trên LINE app và chat 1:1)\n"
       "- Có bản ghi remind trong `user_event`\n- Stripe dashboard có giao dịch **5.000 JPY** thành công",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r9. RULE-07 (DB + LINE + gateway)."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Abnormal",
       "Bill Stripe THẤT BẠI → XÓA booking vừa tạo và hoàn lại bộ đếm",
       STR + "\n- コース P1 全承認, 料金 5000円\n- `use_people` S1 = 2, `remain_limit` P1 = 2 trước khi test",
       "1. U1 đặt 1 chỗ, nhập thẻ fail 4000 0000 0000 0341 → xác nhận\n"
       "2. Query `b_user_booking` tìm booking của U1\n3. Đọc `use_people` và `remain_limit`\n"
       "4. Quan sát màn hình phía U1",
       "Thẻ fail 4000 0000 0000 0341",
       "- Booking vừa tạo bị **XÓA khỏi `b_user_booking`**\n"
       "- `use_people` quay về **2**, `remain_limit` quay về **2**\n"
       "- U1 thấy thông báo lỗi thanh toán, không bị hiểu nhầm là đã đặt xong",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r11. Đây là điểm quan trọng của cơ chế giữ chỗ trước — "
            "verify bộ đếm là bắt buộc."),

    tc("Thanh toán — Stripe", "JOB-001", "Normal",
       "Job quét kết quả bill Stripe — kết quả SUCCESS → cập nhật booking + gửi tin thanh toán thành công",
       STR + "\n- Có 1 booking `status_webhook = 3` (đang chờ kết quả bill) do trình duyệt bị đóng giữa chừng\n"
       "- Job quét kết quả bill đang bật",
       "1. Tạo trạng thái booking `status_webhook = 3` với charge đã success bên Stripe\n"
       "2. Chờ job chạy\n3. Query `b_user_booking`\n4. Query `user_event`\n5. Đọc tin trên LINE app",
       "1 booking chờ job, bill thật đã success",
       "- `status_webhook` = **1** · `status_payment` = **1**\n- Có gửi action + thêm remind\n"
       "- LINE user nhận tin **「決済が完了しました。」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r13. RULE-08 — job BẮT BUỘC test PRODUCTION. ⚠ RULE-01: quan điểm `JOB-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Thanh toán — Stripe", "JOB-001", "Abnormal",
       "Job quét kết quả bill Stripe — kết quả FAIL → xóa booking và gửi tin thanh toán thất bại",
       STR + "\n- Chuẩn bị theo cách test của corpus (xem cột Dữ liệu test)",
       "1. Nhập thẻ fail 4000 0000 0000 0341 khi đặt chỗ → bản ghi `status_webhook = 3` bị xóa\n"
       "2. Fake lại trong DB một bản ghi giống hệt bản vừa bị xóa, cập nhật lại số count\n"
       "3. Chờ job chạy\n4. Query `b_user_booking` + bộ đếm\n5. Đọc tin trên LINE app",
       "Bản ghi fake `status_webhook = 3` với charge fail",
       "- Booking bị **xóa**\n- `use_people` và `remain_limit` được hoàn lại đúng\n"
       "- LINE user nhận tin **「決済に失敗しました。カードのご利用枠や有効期限などをご確認いただき再度、購入手続きを行なってください。」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r14 (kèm nguyên văn cách test 2 bước b1/b2 của tester)."),

    tc("Thanh toán — Stripe", "PAY-ABANDON-001", "Abnormal",
       "3DS — user ĐÓNG TRÌNH DUYỆT ở modal xác thực → job KHÔNG tính là bill fail (change spec 10/2025)",
       STR + "\n- コース P1 全承認, 料金 5000円\n- Thẻ 3DS 4000 0000 0000 3220 (bắt buộc xác thực mọi giao dịch)",
       "1. U1 đặt 1 chỗ, nhập thẻ 3DS → modal xác thực hiện ra\n"
       "2. ĐÓNG trình duyệt (không bấm complete / fail / cancel)\n3. Chờ job quét kết quả chạy\n"
       "4. Query `b_user_booking` + bộ đếm\n5. Kiểm tra LINE user có nhận tin gì không",
       "Đóng trình duyệt giữa 3DS",
       "- Booking bị **xóa**; `use_people` và `remain_limit` được hoàn lại (-1 mỗi cái)\n"
       "- **KHÔNG gửi tin「決済に失敗しました」** cho user (khác với case bill fail thật)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r15「10/2025: Change spec: khi job quét sẽ không tính là bill fail」. "
            "⚠ MT-12 — nội dung expected của corpus TỰ MÂU THUẪN (nói không tính fail nhưng vẫn xóa booking) → "
            "cần Leader chốt."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Đổi lịch KHÔNG phát sinh tiền → không hiện màn nhập thẻ, cập nhật booking ngay",
       STR + "\n- U1 có booking đã thanh toán ở コース P1\n"
       "- Chuẩn bị các slot/コース theo cột Dữ liệu test",
       "1. Với từng trường hợp, U1 thực hiện đổi lịch và quan sát có màn nhập thẻ không\n"
       "2. Query `status_webhook` của booking sau khi đổi",
       "(a) event tắt 決済 · (b) đổi slot A→B đều không tiền · (c) đổi từ CÓ コース sang KHÔNG コース · "
       "(d) đổi sang コース không set 料金 · (e) chỉ đổi friend info",
       "- Cả 5 trường hợp: **KHÔNG hiện màn nhập thẻ**\n"
       "- Booking được update ngay, `status_webhook` = **1**",
       note="Nguồn: Improve bill tiền stripe r17-r21 + univapay r14-r18. 5 input cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Booking đang 承認待ち → user đổi sang コース CÓ tiền: lưu thông tin thanh toán nhưng KHÔNG thu tiền",
       STR + "\n- U1 có booking `status = 3` (承認待ち) ở コース không tính tiền",
       "1. U1 đổi sang コース P1 (5000円) → xác nhận\n2. Query `b_user_booking`\n"
       "3. Kiểm tra Stripe dashboard",
       "Booking status 3 → đổi sang コース có 料金",
       "- Booking update bình thường, có **lưu thông tin thanh toán**\n"
       "- `status` = **3** · `status_webhook` = **1**\n- **KHÔNG có giao dịch** trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r22 + univapay r19."),

    tc("Thanh toán — Stripe", "PAY-CONFIRM-001", "Normal",
       "Đổi lịch リクエスト制 CÓ phát sinh tiền → hiện màn nhập thẻ, tạo cặp booking status = 6, chưa thu tiền",
       STR + "\n- U1 có booking gốc ở slot có 予約変更 = リクエスト制",
       "1. Với từng trường hợp ở cột Dữ liệu test, U1 đổi lịch → quan sát có màn nhập thẻ không\n"
       "2. Nhập thẻ → bấm xác nhận đổi\n3. Query 2 bản ghi booking\n4. Kiểm tra Stripe dashboard",
       "(a) không コース → CÓ コース có 料金 · (b) コース không tiền → コース có tiền · "
       "(c) コース 3000円 → コース 8000円 · (d) đổi số lượng nhỏ hơn · (e) đổi số lượng lớn hơn",
       "- Cả 5 trường hợp: **CÓ hiện màn nhập thẻ**\n"
       "- Sau khi xác nhận: tạo được booking mới `status = 6`; booking gốc cũng `status = 6`, "
       "`status_webhook` = 1\n- **CHƯA thu tiền** trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r23-r27 + univapay r20-r24. 5 input cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — Stripe", "PAY-AMOUNT-001", "Normal",
       "Đổi lịch 全承認 CÓ tiền — bill thành công thì cập nhật charge mới và toàn bộ dữ liệu booking",
       STR + "\n- U1 có booking đã thanh toán 3000円 ở コース P_a\n"
       "- Slot cho phép đổi 全承認; コース P_b có 料金 8000円",
       "1. U1 đổi sang コース P_b, nhập thẻ 4242 4242 4242 4242 → xác nhận\n"
       "2. Query `b_user_booking` (chú ý cột `charge_tmp_id`)\n3. Đọc 4 bộ đếm\n"
       "4. Đọc tin trên LINE app\n5. Kiểm tra Stripe dashboard",
       "3000円 → 8000円",
       "- `status_webhook` = **1** · `status_payment` = **1**\n"
       "- Thông tin booking cập nhật đúng theo dữ liệu user đã đổi; thông tin charge mới được ghi đè\n"
       "- 4 bộ đếm cập nhật đúng; có gửi action change được duyệt + thêm remind\n"
       "- Stripe dashboard: giao dịch mới **8.000 JPY** thành công",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r28-r29「Khi change card bảng b_user_booking lưu thêm charge_id mới "
            "vào cột charge_tmp_id: bill success => update lại thông tin charge mới」."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Abnormal",
       "Đổi lịch 全承認 CÓ tiền — bill THẤT BẠI thì KHÔNG cập nhật dữ liệu booking",
       STR + "\n- U1 có booking đã thanh toán 3000円 ở コース P_a; slot cho đổi 全承認",
       "1. U1 đổi sang コース P_b (8000円), nhập thẻ fail 4000 0000 0000 0341 → xác nhận\n"
       "2. Query `b_user_booking`\n3. Kiểm tra thông tin charge cũ\n4. Kiểm tra Stripe dashboard",
       "Thẻ fail khi đổi lịch",
       "- `status_webhook` = **1**, **KHÔNG update các dữ liệu khác** (booking giữ nguyên コース P_a, 3000円)\n"
       "- **Thông tin charge trước đó KHÔNG bị ghi đè**\n- Không có giao dịch 8.000 JPY thành công trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r28, r31「bill fail => không update thông tin charge trước đó」."),

    tc("Thanh toán — Stripe", "JOB-001", "Abnormal",
       "Job quét kết quả bill khi ĐỔI LỊCH — fail thì set status_webhook = 2 và gửi tin thất bại",
       STR + "\n- Chuẩn bị theo cách test của corpus",
       "1. Nhập thẻ fail 4000 0000 0000 0341 → bấm đổi lịch\n2. Update DB `status_webhook = 6`\n"
       "3. Chờ job chạy\n4. Query `b_user_booking`\n5. Đọc tin trên LINE app",
       "status_webhook fake = 6, charge fail",
       "- `status_webhook` = **2**\n- **KHÔNG update các dữ liệu khác, KHÔNG gửi action**\n"
       "- LINE user nhận tin **「決済に失敗しました。…」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r34 (kèm nguyên văn 3 bước b1/b2/b3 của tester)."),

    tc("Thanh toán — Stripe", "PAY-AMOUNT-001", "Normal",
       "Description trên Stripe hiện đúng tên event + tên コース với mọi kiểu ký tự",
       STR + "\n- Chuẩn bị các event/コース có tên theo cột Dữ liệu test",
       "1. Với từng kiểu tên, đặt 1 chỗ và thanh toán bằng thẻ 4242 4242 4242 4242\n"
       "2. Mở Stripe dashboard xem giao dịch tương ứng\n3. Đối chiếu trường description / shipping_details",
       "Tên = 0 ký tự · space đầu · space cuối · nhiều space giữa · ký tự đặc biệt latinh "
       "` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [] |. , / * \\ : ? · ký tự đặc biệt Nhật "
       "・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞ · Hiragana+Katakana+Kanji「まことボット智恵助」· "
       "Nhật+Latin+emoji「AIボット🤖_Ver1」· ký tự đặc biệt + emoji「こーだい/プレゼント専用🎁」· tên có xuống dòng",
       "- Mọi trường hợp: booking thành công\n"
       "- Stripe hiện description đúng format **「イベント予約 【Tên event】+【Tên コース】」**\n"
       "- Không mất ký tự / không mojibake / không lỗi API do ký tự đặc biệt",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r44-r53 và r61-r70 (SpecImprove #34857, 03/2026). "
            "10 input cùng 1 kết quả mong đợi → gộp 1 TC, liệt kê đủ ở cột Dữ liệu test."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Abnormal",
       "Bill FAIL vẫn ghi nhận giao dịch failed trên Stripe (không im lặng)",
       STR,
       "1. U1 đặt 1 chỗ, nhập thẻ fail 4000 0000 0000 0341 → xác nhận\n"
       "2. Mở Stripe dashboard tìm giao dịch\n"
       "3. Lặp lại với thẻ 3DS 4000 0038 0000 0446 rồi bấm fail/hủy ở modal",
       "Thẻ fail thường và thẻ 3DS bị hủy",
       "- Stripe dashboard **CÓ ghi nhận** giao dịch với status **failed** (không phải không có bản ghi nào)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r54-r55「Vẫn bill sang stripe với status failed」."),

    tc("Thanh toán — Stripe", "CONC-001", "Abnormal",
       "Double-click nút xác nhận ở màn thanh toán → chỉ phát sinh 1 giao dịch",
       STR,
       "1. U1 tới màn nhập thẻ, nhập thẻ hợp lệ\n2. Double-click nhanh nút xác nhận thanh toán\n"
       "3. Đếm giao dịch trên Stripe dashboard\n4. Đếm bản ghi `b_user_booking`\n5. Đọc `use_people`",
       "1 lần double-click",
       "- Stripe chỉ có **1** giao dịch 5.000 JPY\n- Chỉ **1** booking được tạo\n"
       "- `use_people` chỉ +1",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r56, r73 (TC gốc chỉ có tiêu đề, không có expected) → "
            "expected do AI viết theo CONC-001. Đây là rủi ro TIỀN nên phải có TC rõ ràng."),

    tc("Thanh toán — Stripe", "PAY-CONFIRM-001", "Normal",
       "Admin đặt hộ khi slot リクエスト制 → KHÔNG thu tiền dù event bật 決済",
       STR + "\n- コース P1 承認方法 = リクエスト制 (admin duyệt)",
       "1. Admin vào màn đặt chỗ hộ, đặt 1 chỗ cho U1 ở コース P1\n2. Query `b_user_booking`\n"
       "3. Kiểm tra Stripe dashboard",
       "Admin đặt hộ, コース có 料金 5000円",
       "- Booking tạo thành công\n- **KHÔNG có giao dịch** trên Stripe (admin đặt hộ không bill tiền)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r57, r74「Booking thành công — admin booking không bill tiền」."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Admin duyệt booking chờ duyệt CÓ tiền (ở web và ở app) → tiến hành thu tiền, description đúng",
       STR + "\n- U1 đã đặt 1 chỗ ở コース P1 (リクエスト制), booking `status = 3`, đã lưu thông tin thẻ",
       "1. Admin duyệt booking ở **web** → query `b_user_booking` + kiểm tra Stripe\n"
       "2. Chuẩn bị booking tương tự, admin duyệt ở **app mobile** → kiểm tra tương tự",
       "Duyệt ở web · duyệt ở app",
       "- Cả 2 nơi: duyệt thành công, thu tiền thành công (`status` = 1, `status_payment` = 1, "
       "`amount` cập nhật)\n"
       "- Stripe hiện description đúng format 「イベント予約 【Tên event】【Tên コース】」kèm server "
       "https://step.lme.jp/",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r58-r59 (SpecImprove #34857) + Event booking 1.0 r268. "
            "2 kênh cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Admin TỪ CHỐI booking chờ duyệt có tiền → KHÔNG thu tiền",
       STR + "\n- Booking `status = 3` của U1 ở コース P1, đã lưu thông tin thẻ",
       "1. Admin bấm từ chối booking\n2. Query `b_user_booking`\n3. Kiểm tra Stripe dashboard",
       "Từ chối booking có tiền",
       "- `status` = **2** (否認) · `status_payment` vẫn = **0**\n- **KHÔNG có giao dịch** trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Event booking 1.0 r269 + univapay r97."),

    # ══════════════════ 22. Thanh toán — UnivaPay ══════════════════
    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Normal",
       "Bill kiểu CŨ (polling) — có kết quả trong vòng 5 phút, bill thành công",
       UNI + "\n- Bot A đang dùng cơ chế bill UnivaPay **kiểu cũ** (không dùng callback)\n"
       "- コース P1 全承認, 料金 5000円",
       "1. U1 đặt 1 chỗ, nhập thẻ hợp lệ → xác nhận\n2. Chờ kết quả trả về (<5 phút)\n"
       "3. Query `b_user_booking`\n4. Query `user_event`\n5. Đọc tin trên LINE app",
       "Kết quả trả về trong <5 phút, bill success",
       "- `status_webhook` = **1**\n- Có gửi action + thêm remind\n"
       "- Giao dịch trên UnivaPay thành công 5.000 JPY",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r8-r9 (04/2025)."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Abnormal",
       "Bill kiểu CŨ — bill FAIL trong 5 phút → xóa booking và hoàn bộ đếm",
       UNI + "\n- Cơ chế bill kiểu cũ, コース P1 全承認\n- `use_people` = 2, `remain_limit` = 2 trước test",
       "1. U1 đặt 1 chỗ, nhập thẻ bị từ chối → xác nhận\n2. Chờ kết quả\n"
       "3. Query `b_user_booking`\n4. Đọc `use_people` và `remain_limit`",
       "Bill fail trong <5 phút",
       "- Booking bị **xóa**\n- `use_people` quay về **2**, `remain_limit` quay về **2**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r10."),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-002", "Abnormal",
       "Bill kiểu CŨ — quá 5 phút chưa có kết quả → KHÔNG xóa booking, chờ job",
       UNI + "\n- Cơ chế bill kiểu cũ\n- Mô phỏng UnivaPay trả kết quả chậm (>5 phút)",
       "1. U1 đặt 1 chỗ, nhập thẻ → xác nhận\n2. Chờ quá 5 phút\n"
       "3. Query `b_user_booking` xem booking còn không\n4. Chờ job 15 phút chạy",
       ">5 phút chưa có kết quả",
       "- Booking **KHÔNG bị xóa**, vẫn ở trạng thái chờ\n- Đợi job chạy quét kết quả",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r11."),

    tc("Thanh toán — UnivaPay", "JOB-001", "Normal",
       "Job quét kết quả bill UnivaPay (15 phút / lần) — success và fail cho kết quả khác nhau",
       UNI + "\n- Có booking đang chờ kết quả bill (kiểu cũ)",
       "1. Chuẩn bị 1 booking chờ với giao dịch UnivaPay đã success → chờ job → kiểm tra\n"
       "2. Chuẩn bị 1 booking chờ với giao dịch UnivaPay đã fail → chờ job → kiểm tra",
       "2 booking: 1 success, 1 fail",
       "- Booking success: `status_payment` = 1, `status_webhook` = 1; có gửi action + remind; "
       "LINE user nhận **「決済が完了しました。」**\n"
       "- Booking fail: booking bị **xóa**, bộ đếm hoàn lại; LINE user nhận "
       "**「決済に失敗しました。…」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r12-r13. 2 nhánh giữ chung 1 TC vì là 2 kết quả của cùng "
            "1 lần chạy job cần đối chứng — nếu Leader muốn tách thì tách theo nhánh."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Normal",
       "Bill kiểu MỚI (callback) — trạng thái ngay khi user bấm đặt chỗ",
       UNI + "\n- Bot A dùng cơ chế bill UnivaPay **kiểu mới (callback)**\n- コース P1 全承認, 料金 5000円",
       "1. U1 đặt 1 chỗ, nhập thẻ → bấm xác nhận\n2. NGAY LẬP TỨC query `b_user_booking`\n"
       "3. Đọc `use_people` / `remain_limit`",
       "Kiểu mới, chưa có callback",
       "- Bản ghi mới: `status` = **5** · `status_payment` = **0** · `status_webhook` = **0**\n"
       "- Bộ đếm `use_people` / `remain_limit` đã cập nhật (giữ chỗ)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r51. ⚠ Khác kiểu cũ: `status_webhook` = 0 (không phải 3)."),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-001", "Normal",
       "Bill kiểu MỚI — callback success trong 2 phút → đóng màn, KHÔNG gửi tin báo thành công",
       UNI + "\n- Cơ chế bill kiểu mới, コース P1 全承認",
       "1. U1 đặt 1 chỗ, nhập thẻ hợp lệ → xác nhận\n2. Chờ callback (<2 phút)\n"
       "3. Quan sát màn hình phía U1\n4. Query `b_user_booking`\n5. Kiểm tra tin nhắn U1 nhận được",
       "Callback success <2 phút",
       "- Phía LINE user: booking success, màn hình đóng về màn chat\n"
       "- `status_payment` = 1, `status_webhook` = 1\n"
       "- **KHÔNG gửi tin「決済が完了しました。」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r52「send message báo bill success 決済が完了しました。 => "
            "sửa lại case này không send message báo bill success nữa」. ⚠ MT-13 — corpus ghi CẢ 2 hành vi "
            "trong cùng 1 ô expected, cần Leader chốt bản cuối."),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-001", "Abnormal",
       "Bill kiểu MỚI — callback FAIL → hiện lỗi, quay lại màn nhập thẻ, gửi tin thất bại",
       UNI + "\n- Cơ chế bill kiểu mới",
       "1. U1 đặt 1 chỗ, nhập thẻ bị từ chối → xác nhận\n2. Chờ callback fail\n"
       "3. Quan sát màn hình phía U1\n4. Đọc tin trên LINE app\n5. Query `b_user_booking`",
       "Callback fail",
       "- Phía U1: hiện message lỗi, **quay lại màn nhập thẻ** để nhập lại\n"
       "- Nhận tin **「決済に失敗しました。カードのご利用枠や有効期限などをご確認いただき再度、購入手続きを行なってください。」**\n"
       "- Booking được cập nhật theo cơ chế bill lỗi (xem TC callback fail >5 phút)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r53, r57."),

    tc("Thanh toán — UnivaPay", "UI-003", "Abnormal",
       "Quá 2 phút chưa có callback → hiện màn thông báo chờ theo design mới, có nút đóng màn",
       UNI + "\n- Cơ chế bill kiểu mới\n- Mô phỏng callback chậm (>2 phút)",
       "1. U1 đặt 1 chỗ, nhập thẻ → xác nhận\n2. Chờ quá 2 phút\n3. Quan sát màn hình\n"
       "4. Bấm nút「画面を閉じる」",
       ">2 phút chưa có callback",
       "- Hiện màn thông báo chờ theo design mới\n- Bấm「画面を閉じる」→ **đóng màn hình**, "
       "không làm hỏng luồng thanh toán đang chạy nền",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r54-r55. Design: "
            "https://xd.adobe.com/view/6d6b04be-0175-4ffe-a980-d57cf80ef7a9-3838/specs/"),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-002", "Abnormal",
       "Quá 5 phút chưa có callback → status_webhook = 4, chờ callback hoặc job 15 phút",
       UNI + "\n- Cơ chế bill kiểu mới\n- Mô phỏng callback chậm (>5 phút)",
       "1. U1 đặt 1 chỗ, nhập thẻ → xác nhận\n2. Chờ quá 5 phút\n3. Query `b_user_booking.status_webhook`\n"
       "4. Cho callback success tới → query lại\n"
       "5. Với booking khác, cho callback FAIL tới → query lại",
       ">5 phút chưa có callback",
       "- Sau 5 phút: `status_webhook` = **4**\n"
       "- Callback success về sau: `status_payment` = 1, `status_webhook` = 1, ghi charge id, "
       "gửi action + remind, cập nhật bộ đếm\n"
       "- Callback fail về sau: **KHÔNG xóa booking** mà đổi `status` = cancel; `status_payment` = 0, "
       "`status_webhook` = 2 kèm mã lỗi",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r58-r60. ⚠ Đây là điểm KHÁC BIỆT lớn giữa kiểu cũ (xóa booking) "
            "và kiểu mới (đổi sang cancel) khi bill fail — xem MT-12."),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-001", "Normal",
       "Đổi lịch 全承認 kiểu mới — status_webhook = 5 khi bấm đổi, chỉ cập nhật khi có callback",
       UNI + "\n- Cơ chế bill kiểu mới\n- U1 có booking đã thanh toán ở コース không tiền; slot cho đổi 全承認",
       "1. U1 đổi sang コース P1 (5000円), nhập thẻ → bấm xác nhận đổi\n"
       "2. NGAY LẬP TỨC query `b_user_booking`\n3. Chờ callback success (<2 phút) → query lại\n"
       "4. Đọc tin trên LINE app",
       "Đổi lịch 全承認 có tiền",
       "- Ngay sau khi bấm: `status_webhook` = **5**, các thông tin booking **giữ nguyên**\n"
       "- Sau callback success: `status_webhook` = 1, `status_payment` = 1, thông tin booking cập nhật "
       "đúng theo dữ liệu đã đổi, bộ đếm cập nhật, gửi action + remind",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r73-r74."),

    tc("Thanh toán — UnivaPay", "INTG-HOOK-002", "Abnormal",
       "Đổi lịch kiểu mới — quá 5 phút chưa callback → status_webhook = 7, chờ callback / job",
       UNI + "\n- Cơ chế bill kiểu mới, đang đổi lịch có tiền",
       "1. U1 bấm xác nhận đổi lịch có tiền\n2. Chờ quá 5 phút không có callback\n"
       "3. Query `status_webhook`\n4. Cho callback success tới → query lại + đọc tin LINE\n"
       "5. Với booking khác, cho callback fail tới → query lại + đọc tin LINE",
       ">5 phút chưa callback khi đổi lịch",
       "- Sau 5 phút: `status_webhook` = **7**\n"
       "- Callback success: `status_webhook` = 1, cập nhật đủ dữ liệu + bộ đếm + action + remind; "
       "gửi tin **「決済が完了しました。」**\n"
       "- Callback fail: `status_webhook` = 2, **không cập nhật dữ liệu, không gửi action**; "
       "gửi tin **「決済に失敗しました。…」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r79-r81."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Abnormal",
       "Admin duyệt booking có bill UnivaPay → chặn thao tác tiếp khi đang chờ callback",
       UNI + "\n- Booking `status = 3` của U1, コース P1 5000円, cơ chế kiểu mới",
       "1. Admin bấm duyệt booking → `status_webhook` chuyển 0, hiện loading\n"
       "2. Reload màn hình, bấm duyệt lại booking đó\n3. Ghi lại message\n"
       "4. Reload lần nữa, bấm TỪ CHỐI booking đó\n5. Ghi lại message",
       "Đang chờ callback (`status_webhook = 0`)",
       "- Cả 2 thao tác (duyệt lại / từ chối) đều **bị chặn**\n"
       "- Hiện message **「決済処理を行っていますので、操作できません。」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r87, r93-r94. Spec BR-10."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Normal",
       "Admin duyệt booking có bill — callback success / fail cho kết quả khác nhau",
       UNI + "\n- 2 booking `status = 3` của U1 với thông tin thẻ đã lưu",
       "1. Duyệt booking 1, cho callback success tới trong 2 phút → query DB, quan sát màn hình\n"
       "2. Duyệt booking 2, cho callback fail tới → query DB, quan sát màn hình\n"
       "3. Kiểm tra tin nhắn U1 nhận được ở cả 2 case",
       "1 callback success · 1 callback fail",
       "- Success: `status_webhook` = 1, `status` = 1 (màn hình reload hiện status mới), "
       "`status_payment` = 1 + thông tin charge; có gửi action + remind; "
       "**KHÔNG gửi tin bill thành công** (khác luồng đặt mới); bộ đếm cập nhật\n"
       "- Fail: báo lỗi, `status_webhook` = 2, **không đổi status booking**, không đổi `status_payment`, "
       "không gửi action + remind, **không gửi tin bill fail**; bộ đếm **giữ nguyên**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r88-r89, r91-r92."),

    tc("Thanh toán — UnivaPay", "UI-003", "Abnormal",
       "Admin duyệt booking — quá 2 phút chưa có callback → hiện message chờ, chưa cập nhật booking",
       UNI + "\n- Booking `status = 3`, mô phỏng callback chậm",
       "1. Admin bấm duyệt booking\n2. Chờ quá 2 phút\n3. Quan sát màn hình\n4. Query `b_user_booking`",
       ">2 phút chưa có callback",
       "- Hiện message **「この処理には2~3分かかる場合があります。画面を閉じてお待ちください」**\n"
       "- Booking **chưa được cập nhật**; chỉ cập nhật khi callback tới",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r90, r101, r107."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Normal",
       "Admin duyệt request ĐỔI có bill — duyệt từ booking GỐC hay booking MỚI đều cho cùng kết quả",
       UNI + "\n- U1 có cặp booking `status = 6` (gốc + mới) do đổi lịch có tiền, cơ chế kiểu mới",
       "1. Admin mở detail booking **GỐC** → bấm duyệt → quan sát `status_webhook` của cả 2 bản ghi\n"
       "2. Chờ callback success → query lại cả 2 bản ghi + bộ đếm + tin LINE\n"
       "3. Chuẩn bị cặp booking khác, admin mở detail booking **MỚI** → bấm duyệt → lặp lại",
       "Duyệt từ booking gốc · duyệt từ booking mới",
       "- Khi bấm duyệt: chỉ `status_webhook` của **bản ghi đang mở** chuyển 0 và hiện loading; "
       "bản ghi còn lại giữ `status_webhook` = 1\n"
       "- Sau callback success (cả 2 cách): **xóa booking gốc**; booking mới `status` = 1, "
       "`status_payment` = 1, `status_webhook` = 1; gửi action của コース mới + thêm remind; "
       "cập nhật `b_slot` và `b_plan_slot`",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r98-r99, r104-r105. Spec BR-16."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Abnormal",
       "Admin duyệt request đổi — callback FAIL thì chỉ đánh dấu lỗi ở bản ghi vừa thao tác",
       UNI + "\n- Cặp booking `status = 6` (gốc + mới)",
       "1. Admin duyệt từ booking GỐC, cho callback fail → query cả 2 bản ghi\n"
       "2. Chuẩn bị cặp khác, duyệt từ booking MỚI, cho callback fail → query cả 2 bản ghi",
       "Callback fail ở 2 điểm thao tác",
       "- Duyệt từ gốc: **booking gốc** `status_webhook` = 2; dữ liệu khác của cả 2 bản ghi giữ nguyên\n"
       "- Duyệt từ mới: **booking mới** `status_webhook` = 2; dữ liệu khác của cả 2 bản ghi giữ nguyên\n"
       "- Cả 2 case: KHÔNG xóa bản ghi nào, cặp booking vẫn ở `status = 6`",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r100, r106."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Abnormal",
       "Admin KHÔNG hủy được booking đang chờ thanh toán",
       UNI + "\n- Chuẩn bị 6 booking theo cột Dữ liệu test",
       "1. Với từng booking, admin bấm hủy\n2. Ghi lại kết quả và message",
       "(a) status 5 + `status_webhook` 3 · (b) status 5 + `status_webhook` 0 · "
       "(c) status 5 + `status_webhook` 4 · (d) status 1/5 + `status_webhook` 6 · "
       "(e) `status_webhook` 5 · (f) `status_webhook` 7",
       "- **Cả 6 trường hợp: KHÔNG cho hủy**\n"
       "- Hiện message **「決済処理を行っていますので、操作できません。」**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r139-r144. Spec BR-10 (`status_webhook ∈ {0,3,4,5,6,7}`). "
            "6 input cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — UnivaPay", "PAY-STATE-001", "Normal",
       "Admin HỦY ĐƯỢC booking khi không vướng thanh toán",
       UNI + "\n- 2 booking: (a) `status ∈ {1,5}` + `status_webhook` = 1 · (b) `status ∈ {1,5}` + "
       "`status_webhook` = NULL (booking cũ)",
       "1. Admin bấm hủy từng booking\n2. Query `status` sau khi hủy\n3. Đọc bộ đếm",
       "2 booking không vướng thanh toán",
       "- Cả 2: **hủy được**, `status` = 4\n- Bộ đếm `use_people` / `remain_limit` giảm đúng",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r137-r138."),

    tc("Thanh toán — UnivaPay", "SEC-002", "Abnormal",
       "Bot chưa cấu hình Webhook ID của UnivaPay → xác nhận hành vi khi thanh toán",
       "- Bot C liên kết UnivaPay nhưng **chưa set Webhook ID**\n- Event bật 決済 = UnivaPay, コース có 料金",
       "1. U1 đặt 1 chỗ, nhập thẻ → xác nhận\n2. Quan sát màn hình phía U1\n"
       "3. Query `b_user_booking`\n4. Kiểm tra giao dịch trên UnivaPay",
       "Bot thiếu Webhook ID",
       "- Ghi rõ hành vi thật: chặn ngay khi bật 決済 / báo lỗi khi thanh toán / hay bị treo chờ callback\n"
       "- KHÔNG được rơi vào trạng thái **đã thu tiền nhưng booking mãi không xác nhận**",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r182「Check setting không Webhook ID」(TC gốc chỉ có tiêu đề). "
            "⚠ Liên quan spec TD-05 (webhook UnivaPay KHÔNG xác thực chữ ký) — xem MT-10."),

    tc("Thanh toán — UnivaPay", "SEC-002", "Abnormal",
       "Webhook UnivaPay giả mạo → hệ thống KHÔNG được đánh dấu booking đã thanh toán",
       UNI + "\n- Có 1 booking đang chờ thanh toán (`status_webhook` ∈ {0,4})\n"
       "- Có quyền gửi HTTP request tới endpoint webhook (môi trường test)",
       "1. Ghi lại `status_payment` của booking\n"
       "2. Gửi POST giả mạo tới endpoint webhook UnivaPay với body `charge_finished` và "
       "`data.metadata.module` trỏ tới booking đó, KHÔNG có chữ ký hợp lệ\n"
       "3. Query lại `status_payment` / `status_webhook`\n4. Đối chiếu với UnivaPay dashboard",
       "Webhook giả mạo, không chữ ký",
       "- Booking **KHÔNG được đánh dấu đã thanh toán**\n"
       "- Nếu booking bị đánh dấu `status_payment = 1` mà UnivaPay không có giao dịch → "
       "**LỖ HỔNG NGHIÊM TRỌNG, RAISE BUG NGAY**",
       env="STAGING",
       note="TC bổ sung theo spec TD-05 (🔴 BẢO MẬT — webhook UnivaPay chỉ dựa vào `data.metadata.module`). "
            "Corpus KHÔNG có TC này → GAP bảo mật. Chỉ chạy trên môi trường được phép, xem MT-10."),

    # ══════════════════ 23. Thanh toán — 3D Secure ══════════════════
    tc("Thanh toán — 3D Secure", "PAY-CONFIRM-001", "Normal",
       "Thẻ yêu cầu xác thực 3DS → hiện popup xác thực trước khi hoàn tất",
       STR + "\n- Chuẩn bị 2 loại thẻ 3DS theo cột Dữ liệu test",
       "1. U1 đặt 1 chỗ có tiền, nhập thẻ 4000 0000 0000 3220 → xác nhận → quan sát\n"
       "2. Lặp lại với thẻ 4000 0038 0000 0446",
       "4000 0000 0000 3220 (xác thực MỌI giao dịch) · 4000 0038 0000 0446 (xác thực 1 lần)",
       "- Cả 2 thẻ: **hiện popup 3D Secure** trước khi hoàn tất giao dịch",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r3, r7, r19, r23, r31, r35, r51, r55 (03/2024). "
            "2 thẻ cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — 3D Secure", "PAY-ABANDON-001", "Abnormal",
       "3DS — bấm cancel hoặc fail ở popup → đóng popup, báo lỗi, quay lại màn nhập thẻ và XÓA thẻ đã nhập",
       STR + "\n- U1 đang ở màn nhập thẻ, dùng thẻ 3DS",
       "1. Nhập thẻ 3DS → popup xác thực hiện ra → bấm **cancel**\n2. Quan sát màn hình + các ô nhập thẻ\n"
       "3. Lặp lại nhưng bấm **fail** ở popup",
       "cancel · fail",
       "- Cả 2: đóng popup, **hiện message lỗi**, redirect về màn nhập thẻ\n"
       "- **Thông tin thẻ đã nhập bị xóa sạch** (không giữ lại số thẻ / hạn / CVC)",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r4-r5, r8-r9, r20-r21, r24-r25, r32-r33, r36-r37, "
            "r52-r53, r56-r57. Việc clear thông tin thẻ là yêu cầu bảo mật (SEC-002)."),

    tc("Thanh toán — 3D Secure", "PAY-STATE-001", "Normal",
       "3DS complete — booking 全承認 thì thu tiền ngay (status_payment = 1)",
       STR + "\n- コース P1 全承認, 料金 5000円",
       "1. U1 đặt 1 chỗ, nhập thẻ 3DS 4000 0000 0000 3220 → popup → bấm **complete**\n"
       "2. Quan sát màn hình\n3. Query `b_user_booking.status_payment`\n4. Kiểm tra Stripe dashboard",
       "3DS complete, 全承認",
       "- Đóng popup, hiện navigation của trình duyệt\n"
       "- `status_payment` = **1**\n- Stripe: thanh toán **success**",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r22, r26."),

    tc("Thanh toán — 3D Secure", "PAY-CONFIRM-001", "Normal",
       "3DS complete — booking CHỜ DUYỆT thì chưa thu tiền (status_payment = 0)",
       STR + "\n- コース P1 リクエスト制, 料金 5000円",
       "1. U1 đặt 1 chỗ, nhập thẻ 3DS → popup → bấm **complete**\n"
       "2. Query `b_user_booking.status_payment`\n3. Kiểm tra Stripe dashboard",
       "3DS complete, リクエスト制",
       "- `status_payment` = **0** (chưa thu tiền, chờ admin duyệt)\n"
       "- Stripe: chưa có giao dịch thành công thu tiền",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r6, r10, r34, r38."),

    tc("Thanh toán — 3D Secure", "PAY-STATE-001", "Abnormal",
       "Thẻ decline / error → báo lỗi Your card was declined, quay lại màn nhập thẻ và xóa thẻ",
       STR,
       "1. U1 nhập thẻ 4000 0084 0000 1629 (decline) → xác nhận → ghi message\n"
       "2. Nhập thẻ 4000 0084 0000 1280 (error) → xác nhận → ghi message\n"
       "3. Quan sát các ô nhập thẻ sau lỗi",
       "4000 0084 0000 1629 · 4000 0084 0000 1280",
       "- Cả 2 thẻ: báo lỗi **「Your card was declined」**\n"
       "- Redirect về màn nhập thẻ, **thông tin thẻ đã nhập bị xóa**",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r11-r12, r27-r28, r39-r40, r59-r60."),

    tc("Thanh toán — 3D Secure", "COMPAT-LEGACY-001", "Normal",
       "Thẻ KHÔNG hỗ trợ 3DS (American Express) → vẫn thanh toán được, không hiện popup",
       STR,
       "1. U1 nhập thẻ 3782 8224 6310 005 (not support 3DS) → xác nhận\n"
       "2. Quan sát có popup 3DS không\n3. Query `status_payment`\n4. Kiểm tra Stripe dashboard",
       "3782 8224 6310 005 (American Express)",
       "- **KHÔNG hiện popup 3DS**\n- Vẫn bill được: hiện navigation trình duyệt\n"
       "- `status_payment` đúng theo chế độ duyệt của コース (1 nếu 全承認, 0 nếu リクエスト制)\n"
       "- Stripe: thanh toán success",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r14, r17, r30, r42, r46, r62. "
            "⚠ Chính logo thẻ American Express trên màn thanh toán là nguyên nhân bug OGP #37932."),

    tc("Thanh toán — 3D Secure", "PAY-STATE-001", "Abnormal",
       "Admin duyệt booking dùng thẻ BẮT BUỘC 3DS mọi giao dịch → KHÔNG duyệt được",
       STR + "\n- U1 đã đặt chỗ với thẻ 4000 0000 0000 3220, booking `status = 3`, `status_payment` = 0",
       "1. Admin mở detail booking → bấm duyệt\n2. Quan sát thông báo\n"
       "3. Query `b_user_booking.status` và `status_payment`",
       "Thẻ 4000 0000 0000 3220 (required authen mọi giao dịch)",
       "- Hiện **alert thông báo thẻ cần xác thực** (message tiếng Anh do Stripe trả về)\n"
       "- **KHÔNG duyệt được** booking; `status` vẫn = 3, `status_payment` vẫn = 0",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r15, r43. Đây là giới hạn nghiệp vụ quan trọng: "
            "thẻ 3DS-mọi-giao-dịch không dùng được với luồng リクエスト制."),

    tc("Thanh toán — 3D Secure", "PAY-STATE-001", "Normal",
       "Admin duyệt booking với thẻ 3DS-một-lần / thẻ thường / AmEx → thu tiền thành công",
       STR + "\n- 3 booking `status = 3` của U1 dùng 3 loại thẻ ở cột Dữ liệu test",
       "1. Admin duyệt lần lượt 3 booking\n2. Query `status_payment` từng booking\n"
       "3. Kiểm tra Stripe dashboard",
       "4242 4242 4242 4242 · 4000 0038 0000 0446 · 3782 8224 6310 005",
       "- Cả 3: duyệt thành công, `status_payment` = **1**\n- Stripe: 3 giao dịch **success**",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r16-r18, r44-r46. 3 thẻ cùng 1 kết quả → gộp 1 TC."),

    tc("Thanh toán — 3D Secure", "STATE-DEP-001", "Abnormal",
       "Tổ hợp LIÊN KẾT / HỦY LIÊN KẾT cổng thanh toán giữa chừng — Stripe",
       STR + "\n- Chuẩn bị được thao tác liên kết / hủy liên kết Stripe ở màn liên kết cổng",
       "1. Với từng kịch bản ở cột Dữ liệu test, thực hiện đúng thứ tự thao tác\n"
       "2. Quan sát có màn nhập thẻ không và kết quả thu tiền\n3. Query `status_payment`",
       "(a) chưa liên kết → booking chờ duyệt → liên kết → duyệt\n"
       "(b) đã liên kết → booking chờ duyệt → hủy liên kết → duyệt\n"
       "(c) chưa liên kết → request change (không màn thẻ) → liên kết → duyệt ở bản gốc\n"
       "(d) như (c) nhưng duyệt ở bản mới\n"
       "(e) chưa liên kết → booking → liên kết → request change (CÓ màn thẻ) → duyệt (bản mới / bản gốc)\n"
       "(f) đã liên kết → booking → hủy liên kết → request change (không màn thẻ) → duyệt (bản mới / bản gốc)\n"
       "(g) đã liên kết → request change (CÓ màn thẻ) → hủy liên kết → duyệt (bản gốc / bản mới)",
       "- (a) **KHÔNG thanh toán** (tính theo thời điểm booking — không có thông tin thẻ)\n"
       "- (b) **VẪN thanh toán** (thời điểm booking đã có thông tin thẻ)\n"
       "- (c), (d) **KHÔNG bill được** do không có thông tin thẻ\n"
       "- (e) **thanh toán được**\n- (f) **KHÔNG bill được**\n- (g) **thanh toán được**\n"
       "→ Quy tắc: thu tiền hay không phụ thuộc **thời điểm tạo booking/request có thông tin thẻ hay không**, "
       "không phụ thuộc trạng thái liên kết lúc duyệt",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r67-r76 (Stripe). Đây là ma trận quan trọng và rất dễ lọt bug. "
            "⚠ MT-15 — spec KHÔNG mô tả quy tắc 'tính theo thời điểm booking' này."),

    tc("Thanh toán — 3D Secure", "STATE-DEP-001", "Abnormal",
       "Tổ hợp LIÊN KẾT / HỦY LIÊN KẾT cổng thanh toán giữa chừng — UnivaPay",
       UNI + "\n- Chuẩn bị được thao tác liên kết / hủy liên kết UnivaPay",
       "1. Lặp lại đúng 7 kịch bản như TC tương ứng của Stripe\n"
       "2. Với case thanh toán được, kiểm tra thêm transaction trên UnivaPay có dữ liệu không",
       "7 kịch bản (a)–(g) giống ma trận Stripe",
       "- Kết quả từng kịch bản **giống ma trận Stripe**\n"
       "- Với case thanh toán được: **transaction trên UnivaPay có dữ liệu** đầy đủ",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r79-r88 (UnivaPay)."),

    tc("Thanh toán — 3D Secure", "PAY-STATE-001", "Abnormal",
       "Event chọn cổng KHÁC với cổng bot đang liên kết → booking thành công nhưng KHÔNG thu tiền",
       "- Bot A chỉ liên kết 1 trong 2 cổng\n- Event chọn cổng còn lại",
       "1. Bot liên kết UnivaPay, event chọn Stripe → U1 đặt chỗ có tiền → quan sát\n"
       "2. Bot liên kết Stripe, event chọn UnivaPay → U1 đặt chỗ có tiền → quan sát\n"
       "3. Bot liên kết đúng cổng event chọn → U1 đặt chỗ → quan sát",
       "3 tổ hợp liên kết × cổng event chọn",
       "- (1) và (2): **booking success nhưng KHÔNG bill tiền**\n"
       "- (3): booking success và **CÓ bill tiền**",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r98-r101. ⚠ Hành vi 'booking success mà không thu tiền' là "
            "rủi ro nghiệp vụ (mất doanh thu âm thầm) — nên xác nhận lại với Leader, xem MT-15."),

    tc("Thanh toán — 3D Secure", "UI-003", "Abnormal",
       "Event chọn Stripe rồi HỦY liên kết Stripe ở màn liên kết → màn nhập thẻ báo lỗi",
       "- Event E đã lưu 決済 = Stripe\n- Sau đó vào màn liên kết cổng hủy liên kết Stripe",
       "1. Hủy liên kết Stripe của bot\n2. U1 mở link event, đặt chỗ tới màn nhập thẻ\n3. Quan sát",
       "Event trỏ Stripe nhưng bot đã hủy liên kết",
       "- Màn nhập thẻ **hiển thị lỗi** (không nhập thẻ được)\n"
       "- Không rơi vào trạng thái booking treo giữa chừng không rõ trạng thái",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r103「đến mh nhập card sẽ hiển thị lỗi (từ trước đã để như vậy)」."),

    # ══════════════════ 24. Hoàn tiền 返金 ══════════════════
    tc("Hoàn tiền 返金", "UI-003", "Normal",
       "Booking KHÔNG có thanh toán → màn detail KHÔNG hiện nút hoàn tiền",
       STR + "\n- Booking B của U1 có `status_payment = 0` (không thu tiền)",
       "1. Admin mở màn detail booking B\n2. Quan sát vùng nút thao tác",
       "status_payment = 0",
       "- **KHÔNG hiện nút 返金 (hoàn tiền)**",
       note="Nguồn: Event booking 1.0 r347."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Hoàn tiền QUA CỔNG (reason_refund = 1) — Stripe charge kiểu cũ (ch_) và kiểu mới (pi_)",
       STR + "\n- 2 booking đã thanh toán Stripe: B_old có `strip_charge_id` bắt đầu bằng **ch_**, "
       "B_new có `strip_charge_id` bắt đầu bằng **pi_**",
       "1. Admin mở detail B_old → bấm 返金 → chọn hoàn tiền qua cổng → xác nhận\n"
       "2. Query `b_user_booking`: `status_payment`, `refund_date`, `reason_refund`\n"
       "3. Kiểm tra Stripe dashboard\n4. Mở màn detail friend → tab lịch sử booking\n"
       "5. Lặp lại toàn bộ với B_new (pi_)",
       "ch_ (Strip_customer_id: cus_S0pwpBofXvUsyz / Strip_card_id: card_1R6oGbEojkVpWWGaV2io7Max) · pi_",
       "- Cả 2: refund success, `status_payment` = **2**, có `refund_date` và `reason_refund`\n"
       "- Stripe dashboard: giao dịch **đã được hoàn tiền**\n"
       "- Lịch sử booking ở màn detail friend ghi nhận hành động hoàn tiền",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r296-r297 (Bug tự detect #38690, 07/2026 — 'Thao tác refund bị refund "
            "fail'). Spec BR-21. Đây là bộ TC của bug MỚI NHẤT trong corpus."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Hoàn tiền CHỈ TRONG LME (reason_refund ≠ 1) → đánh dấu DB nhưng KHÔNG gọi cổng",
       STR + "\n- Booking đã thanh toán Stripe 5000円",
       "1. Admin mở detail booking → bấm 返金 → chọn「chỉ hoàn trong LME, không hoàn trên cổng」→ xác nhận\n"
       "2. Query `status_payment` / `refund_date`\n3. Kiểm tra Stripe dashboard\n"
       "4. Mở lịch sử booking ở màn detail friend",
       "reason_refund ≠ 1 (エルメから)",
       "- `status_payment` = **2** + có `refund_date`\n"
       "- Giao dịch trên Stripe **KHÔNG bị hoàn tiền**\n- Lịch sử booking vẫn ghi nhận thao tác hoàn tiền",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r298 + Event booking 1.0 r350. Spec BR-21."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Hoàn tiền UnivaPay — có dùng webhook và không dùng webhook, cùng chọn hoàn qua cổng",
       UNI + "\n- 2 booking đã thanh toán UnivaPay: 1 bot dùng webhook, 1 bot không dùng webhook",
       "1. Với từng booking, admin bấm 返金 → chọn hoàn qua cổng → xác nhận\n"
       "2. Query `status_payment`\n3. Kiểm tra UnivaPay dashboard\n4. Mở lịch sử booking",
       "UnivaPay có webhook · UnivaPay không webhook",
       "- Cả 2: refund success, `status_payment` = **2**\n"
       "- UnivaPay dashboard: giao dịch **đã hoàn tiền**\n"
       "- Lịch sử booking hiển thị ở màn detail friend\n"
       "- DB: `univapay_charge_id` được set NULL (theo spec Field Matrix #56)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r299-r300 + Event booking 1.0 r349. Spec Field Matrix #56."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Normal",
       "Hoàn tiền UnivaPay chỉ trong LME → không hoàn trên UnivaPay",
       UNI + "\n- Booking đã thanh toán UnivaPay",
       "1. Admin bấm 返金 → chọn chỉ hoàn trong LME → xác nhận\n2. Query `status_payment`\n"
       "3. Kiểm tra UnivaPay dashboard\n4. Mở lịch sử booking",
       "reason_refund ≠ 1",
       "- `status_payment` = **2**\n- UnivaPay: giao dịch **KHÔNG bị hoàn**\n- Lịch sử booking có ghi nhận",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r301."),

    tc("Hoàn tiền 返金", "PAY-STATE-001", "Abnormal",
       "Hoàn tiền khi strip_charge_id RỖNG / NULL → không được rơi vào nhánh PaymentIntent sai",
       STR + "\n- Booking có bill Stripe nhưng `b_user_booking.strip_charge_id` = NULL hoặc chuỗi rỗng "
       "(VD booking thanh toán fail trước đó, hoặc dữ liệu import cũ)",
       "1. Admin mở màn quản lý booking event → chọn booking đó\n"
       "2. Bấm 返金 (có tick hoàn tiền trên Stripe)\n3. Quan sát thông báo\n4. Query DB",
       "strip_charge_id = NULL / ''",
       "- Hiện thông báo lỗi **rõ nguyên nhân** (không có giao dịch để hoàn)\n"
       "- KHÔNG báo success giả; `status_payment` **KHÔNG** chuyển 2\n"
       "- Không phát sinh request lỗi tới Stripe",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r302 (TC-NEW-01 do AI đề xuất trong bộ human, gắn bug #38690)."),

    tc("Hoàn tiền 返金", "DATA-MIG-001", "Boundary",
       "Xác nhận phạm vi giá trị strip_charge_id trên production (chỉ ch_ và pi_?)",
       "- Có quyền query DB production (read-only)\n- Đã hẹn trước với PM",
       "1. Chạy `SELECT LEFT(strip_charge_id,3) AS p, COUNT(*) FROM b_user_booking GROUP BY p`\n"
       "2. Đối chiếu kết quả với 2 nhánh code refund (ch_ / else)\n"
       "3. Nếu xuất hiện prefix ngoài ch_/pi_ (VD py_) → tạo booking mẫu prefix đó và thử hoàn tiền",
       "Query production",
       "- Chỉ tồn tại 2 prefix **ch_** và **pi_** (khớp 2 nhánh code)\n"
       "- Nếu có prefix thứ 3 → **RAISE BUG**: nhánh else xử lý sai, refund sẽ fail",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r303 (TC-NEW-02 do AI đề xuất, RULE-04 — xác minh phạm vi dữ liệu thật)."),

    tc("Hoàn tiền 返金", "CONC-001", "Abnormal",
       "Hoàn tiền LẠI booking đã hoàn → báo lỗi đúng, Stripe không phát sinh refund thứ 2",
       STR + "\n- Booking pi_ đã hoàn tiền thành công",
       "1. Mở 2 tab màn quản lý booking, mở sẵn modal 返金 ở cả 2\n"
       "2. Tab 1 bấm hoàn tiền (lần 1)\n3. Tab 2 bấm hoàn tiền (lần 2)\n"
       "4. Quan sát GUI + query DB + kiểm tra Stripe dashboard",
       "2 tab cùng hoàn 1 booking",
       "- GUI báo lỗi **đúng nguyên nhân** (giao dịch đã được hoàn tiền)\n"
       "- Stripe **KHÔNG phát sinh refund thứ 2**\n- DB không sinh bản ghi lịch sử hoàn tiền trùng",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r304, r306 (TC-NEW-03 / TC-NEW-06 do AI đề xuất). "
            "⚠ Spec TD-10: refund KHÔNG idempotent — **dự kiến FAIL**, xem MT-07."),

    tc("Hoàn tiền 返金", "ENV-001", "Abnormal",
       "Hoàn tiền khi Stripe timeout / trả 5xx → không báo success giả",
       STR + "\n- Booking pi_ chưa hoàn tiền\n- Dùng Stripe sandbox mock lỗi hoặc chặn outbound tới "
       "api.stripe.com ngay lúc bấm hoàn tiền",
       "1. Bấm 返金\n2. Chờ response\n3. Query DB `status_payment`\n4. Kiểm tra Stripe dashboard",
       "Timeout / HTTP 5xx từ Stripe",
       "- GUI hiện lỗi (timeout / kết nối), **KHÔNG báo success giả**\n"
       "- `status_payment` **KHÔNG** = 2\n- Không có refund treo bên Stripe\n"
       "- Có đường thoát cho người dùng (thử lại được)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r305 (TC-NEW-04 do AI đề xuất)."),

    tc("Hoàn tiền 返金", "SEC-ISO-001", "Abnormal",
       "Hoàn tiền booking của bot A KHÔNG được đụng booking trùng của bot B",
       "- 2 bot / 2 tài khoản, mỗi bên có 1 booking event trùng tên + trùng ngày, đều có bill Stripe pi_",
       "1. Query DB ghi lại `status_payment` của cả 2 booking\n"
       "2. Đăng nhập bot A, hoàn tiền booking của bot A\n3. Query lại DB cả 2 booking\n"
       "4. Thử gửi request hoàn tiền với `bot_id` bị sửa thành bot B",
       "2 booking trùng thông tin ở 2 bot",
       "- Chỉ booking của bot A đổi `status_payment` = 2 + `refund_date` + `reason_refund`\n"
       "- Booking của bot B **KHÔNG đổi**\n"
       "- Request sửa `bot_id`: **phải bị từ chối**; nếu hoàn được tiền booking bot khác → "
       "**LỖ HỔNG IDOR, RAISE BUG NGAY**",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r307 (TC-NEW-07 do AI đề xuất) + spec TD-02 (🔴 IDOR ở refundMoneyBookingEvent — "
            "lấy `bot_id` TỪ REQUEST). **Dự kiến FAIL** — xem MT-06."),

    tc("Hoàn tiền 返金", "PAY-AMOUNT-001", "Normal",
       "Số tiền hoàn khớp giữa Stripe ↔ màn admin ↔ phép tính tay",
       STR + "\n- Booking pi_ có số tiền cụ thể (VD 5.500 JPY, có thuế)",
       "1. Ghi lại số tiền booking trên màn admin\n2. Bấm 返金 qua cổng\n"
       "3. Mở Stripe dashboard xem số tiền hoàn thực tế\n4. Query DB `refund_date`, `reason_refund`, `amount`",
       "5.500 JPY (đã gồm thuế)",
       "- Số tiền hoàn trên Stripe = **5.500 JPY** = số tiền booking = phép tính tay\n"
       "- Không hoàn thiếu / thừa / hoàn theo đơn giá thay vì tổng tiền",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r308 (TC-NEW-08 do AI đề xuất). PAY-AMOUNT-001 tách riêng khỏi PAY-STATE-001."),

    tc("Hoàn tiền 返金", "ENV-003", "Normal",
       "Smoke hoàn tiền trên PRODUCTION và đối soát Stripe thật",
       "- Booking thật hoặc booking test trên production có bill Stripe pi_\n- Đã hẹn trước với PM",
       "1. Thực hiện hoàn tiền trên step.lme.jp\n2. Đối soát bản ghi trên dashboard Stripe account thật\n"
       "3. Query DB production",
       "1 booking production",
       "- Refund success\n- Bản ghi Stripe production khớp **số tiền + trạng thái**\n"
       "- `status_payment` = 2\n- Evidence: ảnh dashboard Stripe + ảnh màn admin + kết quả query",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r309 (TC-NEW-09 do AI đề xuất, RULE-08)."),

    tc("Hoàn tiền 返金", "REG-SHARED-001", "Normal",
       "Regression — hoàn tiền Stripe ở salon / lesson / item với charge pi_ không bị lỗi giống #38690",
       "- Dev đã cung cấp danh sách nơi gọi `refundMoney(`\n"
       "- Chuẩn bị booking/đơn hàng có charge pi_ ở từng luồng Dev xác nhận",
       "1. Với mỗi luồng (salon / lesson / item): thực hiện hoàn tiền Stripe\n"
       "2. Quan sát GUI + Stripe dashboard",
       "3 luồng × charge pi_",
       "- Hoàn tiền **thành công ở mọi luồng**\n"
       "- Nếu luồng nào báo「refund fail」với pi_ → **cùng bug #38690, mở ticket riêng**",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r310 (TC-NEW-10 do AI đề xuất). Ghi 'regression' theo quy chuẩn Loại case."),

    tc("Hoàn tiền 返金", "DATA-AUDIT-001", "Normal",
       "Lịch sử sau hoàn tiền — mỗi lần hoàn sinh đúng 1 bản ghi đủ 4 thông tin, cho cả ch_ và pi_",
       STR + "\n- 1 booking ch_ và 1 booking pi_ đều vừa được hoàn tiền",
       "1. Mở màn detail friend → tab lịch sử booking\n"
       "2. Đối chiếu bản ghi lịch sử với thao tác vừa làm",
       "2 booking vừa hoàn tiền",
       "- Mỗi lần hoàn sinh **đúng 1** bản ghi lịch sử\n"
       "- Bản ghi ghi đủ: **người thực hiện / thời gian / hành động (hoàn tiền, không phải「thêm mới」)**",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r311 (TC-NEW-12 do AI đề xuất). ⚠ Spec G-11: bảng `b_user_booking_history` "
            "không có trong DB dump → mapping cột tin cậy Trung bình."),

    tc("Hoàn tiền 返金", "PERM-002", "Abnormal",
       "Phân quyền — account staff không được cấp quyền KHÔNG được hoàn tiền qua URL trực tiếp",
       "- Có 2 account staff của bot A: staff X KHÔNG được cấp quyền màn event booking, "
       "staff Y ĐƯỢC cấp quyền\n- Có 1 booking đã thanh toán",
       "1. Đăng nhập staff X → truy cập trực tiếp route/nút hoàn tiền booking event\n"
       "2. Gửi thẳng request hoàn tiền bằng công cụ (bypass UI)\n"
       "3. Đăng nhập staff Y → thực hiện hoàn tiền qua UI\n4. Query DB sau mỗi bước",
       "staff X (không quyền) · staff Y (có quyền)",
       "- staff X: **KHÔNG hoàn tiền được** ở cả UI lẫn request trực tiếp; `status_payment` không đổi\n"
       "- staff Y: hoàn tiền thành công, lịch sử ghi đúng tên staff Y",
       env="STAGING",
       note="Nguồn: Task nhỏ r312 (RV-07 do AI đề xuất). ⚠ Spec TD-03 (route /ajax KHÔNG có `basic_access`) + "
            "corpus「Improve nhỏ」r320 (Bug Tester #33106 — các màn booking không phân quyền vẫn access được, "
            "trạng thái NG) → **dự kiến FAIL**, xem MT-09."),

    tc("Hoàn tiền 返金", "DATA-DB-001", "Abnormal",
       "Guard — hoàn tiền booking không tồn tại / event đã bị xóa",
       STR + "\n- Biết id của 1 booking đã bị xóa và 1 booking thuộc event đã bị xóa",
       "1. Gửi thao tác hoàn tiền với `booking_id` không tồn tại\n"
       "2. Gửi thao tác hoàn tiền với booking mà `b_event_detail` đã bị xóa (mở 2 tab để tái hiện)\n"
       "3. Quan sát thông báo lỗi + log",
       "booking_id không tồn tại · event đã xóa",
       "- Cả 2 trường hợp: hiện **thông báo lỗi rõ ràng**, KHÔNG lỗi 500 / trang trắng\n"
       "- Không phát sinh request hoàn tiền tới cổng thanh toán",
       env="STAGING",
       note="Nguồn: Task nhỏ r313 (RV-08 do AI đề xuất). Liên quan TD-01 (xóa cascade không transaction "
            "→ có thể còn booking mồ côi)."),

    tc("Hoàn tiền 返金", "ENV-003", "Normal",
       "Hoàn tiền chọn đúng secret key theo môi trường test / live",
       STR + "\n- 1 booking có `flag_environment = 0` (test) và 1 booking `flag_environment = 1` (live), "
       "cả 2 đều đã thanh toán Stripe",
       "1. Hoàn tiền booking môi trường test qua cổng\n2. Hoàn tiền booking môi trường live qua cổng\n"
       "3. Với mỗi lần, xác nhận giao dịch xuất hiện trên đúng dashboard Stripe (test / live)",
       "flag_environment 0 và 1",
       "- Booking test: hoàn tiền xuất hiện ở **dashboard test**\n"
       "- Booking live: hoàn tiền xuất hiện ở **dashboard live**\n"
       "- Không lần nào gọi nhầm key (không có lỗi authentication, không hoàn nhầm môi trường)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r314 (RV-11 do AI đề xuất). Spec Field Matrix #28."),
]

# ── Bổ sung sau BƯỚC 7 (audit coverage vs Field Traceability Matrix + corpus) ──
S4 += [
    tc("Thanh toán — Stripe", "SEC-002", "Abnormal",
       "KHÔNG lưu số thẻ / CVC ở bất kỳ đâu trong hệ thống LME",
       STR + "\n- U1 vừa thanh toán thành công bằng thẻ 4242 4242 4242 4242, CVC 123",
       "1. Query `b_user_booking` của booking vừa tạo, đọc toàn bộ cột liên quan thanh toán\n"
       "2. Tìm chuỗi '4242424242424242' và '123' trong toàn bộ bản ghi\n"
       "3. Mở màn detail booking phía admin → quan sát vùng thông tin thanh toán\n"
       "4. Kiểm tra log ứng dụng quanh thời điểm thanh toán",
       "Thẻ 4242 4242 4242 4242, CVC 123",
       "- DB chỉ lưu `strip_pm_id` / `univapay_token` + **4 số cuối** (`*_last4`) + tên brand thẻ\n"
       "- **KHÔNG tìm thấy** số thẻ đầy đủ và CVC ở bất kỳ cột nào\n"
       "- Màn admin chỉ hiện 4 số cuối + brand\n- Log KHÔNG chứa số thẻ / CVC",
       env="PRODUCTION",
       note="Nguồn: spec Field Matrix #59 (🔑 **KHÔNG lưu số thẻ** — chỉ `strip_pm_id`/`univapay_token` + "
            "`*_last4` + `*_brand_name`). Corpus KHÔNG có TC kiểm chiều này → bổ sung sau BƯỚC 7 audit."),

    tc("Thanh toán — Stripe", "PAY-STATE-001", "Normal",
       "Đổi thẻ thanh toán (change card) — bill thành công / thất bại xử lý đúng",
       STR + "\n- U1 có booking đang chờ duyệt, đã lưu thông tin thẻ cũ",
       "1. U1 vào luồng đổi thẻ, nhập thẻ mới hợp lệ 4242 4242 4242 4242 → xác nhận\n"
       "2. Query `b_user_booking` đọc thông tin thẻ (last4 / brand)\n"
       "3. Admin duyệt booking → kiểm tra Stripe dashboard xem thu bằng thẻ nào\n"
       "4. Với booking khác: đổi sang thẻ fail 4000 0000 0000 0341 → xác nhận → query DB\n"
       "5. Lặp lại toàn bộ với cổng UnivaPay",
       "Thẻ mới hợp lệ · thẻ mới bị từ chối · 2 cổng",
       "- Đổi thẻ thành công: DB cập nhật `*_last4` / `*_brand_name` sang thẻ mới; khi duyệt thì thu tiền "
       "bằng **thẻ mới**\n"
       "- Đổi thẻ thất bại: **KHÔNG ghi đè** thông tin thẻ cũ, booking giữ nguyên trạng thái",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r40-r41「check lại case change card bill univapay — change card "
            "bill success / change card bill fail」(TC gốc chỉ có tiêu đề, không có expected) → expected do AI "
            "viết theo PAY-STATE-001. Bổ sung sau BƯỚC 7 audit; cần Leader xác nhận luồng đổi thẻ có tồn tại "
            "ở event booking hay không."),

    tc("Thanh toán — Stripe", "REG-SHARED-001", "Normal",
       "Booking phát sinh từ FORM có liên kết thanh toán → duyệt bên LME vẫn thu tiền đúng",
       "- Form answer có liên kết thanh toán (callback về form) và tạo booking event\n"
       "- Booking ở trạng thái chờ duyệt, đã qua màn nhập thẻ bên form (thẻ 4242 4242 4242 4242)\n"
       "- Bot A liên kết cả Stripe và UnivaPay",
       "1. Với cổng **Stripe**: admin duyệt booking bên LME (không cần chuyển callback, bấm duyệt luôn) → "
       "query `status_payment` → kiểm tra Stripe dashboard\n"
       "2. Chuẩn bị request đổi lịch chờ duyệt (đã qua màn nhập thẻ bên form): duyệt ở **bản gốc** → kiểm tra\n"
       "3. Lặp lại: duyệt ở **bản mới** → kiểm tra\n"
       "4. Lặp lại toàn bộ 3 bước với cổng **UnivaPay**",
       "2 cổng × 3 điểm duyệt · thẻ 4242 4242 4242 4242",
       "- Cả 6 trường hợp: **bill tiền success**, `status_payment` = **1**\n"
       "- Giao dịch xuất hiện đúng trên dashboard Stripe / UnivaPay tương ứng",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r89-r96 (khối「case cũ: stripe / univapay」— booking sinh từ "
            "form có liên kết thanh toán, duyệt bên LME). Đây là điểm chạm chéo FA-011 Form ↔ FA-021 Event "
            "booking. Bổ sung sau BƯỚC 7 audit."),
]
