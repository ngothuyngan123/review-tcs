# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Nhóm 決済: 決済連携 cài đặt, Stripe, UnivaPay & webhook.

Nguồn chính: 11.2 TCsLine_LessonCalendar
  - tab「Liên kết bill tiền」(100 TC lá) — setting liên kết + ma trận bill của Stripe/UnivaPay
  - tab「Sửa bill tiền univapay」(143 TC lá, 2025 → 06/2026) — callback/webhook, Bug Tester #38077,
    SpecImprove #34857, SpecImprove #34895, Bug KH #33787
  - tab「Improve bill tiền stripe」(41 TC lá, 10/2025 → 03/2026) — tạo order trước, job quét kết quả
  - tab「Task nhỏ + fix bug KH」r2-r18 — sửa logic booking có bill tiền giống event booking
Spec: BR-50…BR-52, BR-P20…BR-P28, RP-01 (bỏ qua thanh toán bằng cờ client).
RULE-08: toàn bộ nhóm này đặt Môi trường test = PRODUCTION (bill tiền).
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, course Cp giá 5.000 yên, course Cf không giá\n"
       "- Mở /basic/calendar-management/21 > tab 決済連携")

S8 = [
    # ══════════════════ 決済連携 — cài đặt ══════════════════
    tc("決済連携 — cài đặt", "PAY-STATE-001", "Normal",
       "Default không sử dụng bill tiền; account không dùng bill nhưng course có giá",
       CAL + "\n- Calendar chưa enable bill tiền, course Cp vẫn có giá 5.000 yên",
       "1. Vào tab 決済連携 → quan sát trạng thái mặc định\n"
       "2. LINE user U1 booking course Cp → quan sát luồng\n3. Kiểm dashboard cổng thanh toán",
       "Calendar không bill, course có giá",
       "- Default: 決済連携 ở trạng thái không sử dụng\n"
       "- U1 booking BÌNH THƯỜNG, KHÔNG qua màn nhập thẻ, không bị trừ tiền\n"
       "- Không có giao dịch nào trên cổng thanh toán",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r4-r5."),

    tc("決済連携 — cài đặt", "PAY-LIMIT-001", "Abnormal",
       "Bot gói free bật bill tiền → chặn + message upgrade",
       "- Bot B gói **free**, có lesson calendar\n- Mở tab 決済連携",
       "1. Bấm bật bill tiền\n2. Quan sát message",
       "Bot free",
       "- Báo lỗi「決済機能のご利用には有料プランへのアップグレードが必要です。」\n"
       "- KHÔNG bật được bill tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r6. ⚠️ Spec BR-P21: khi bot free, `is_use_payment` bị ép 0 "
            "CHỈ TRÊN OBJECT PHP, DB không đổi; client gửi `checkHasPayment=true` thì server VẪN THU TIỀN "
            "⇒ xem TC ở nhóm Đồng thời & verify API và MT-44."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Normal",
       "Bot standard/pro/enterprise: bật bill tiền được (nếu đã liên kết hệ thống)",
       CAL + "\n- Bot A gói standard, đã liên kết Stripe (status_strip_bot = 3)",
       "1. Bấm bật bill tiền\n2. Quan sát",
       "Bot standard đã liên kết Stripe",
       "- Bật được bill tiền, hiện các option cấu hình phía dưới",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r7 — TC gốc chỉ có tiêu đề, expected do AI bổ sung."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Abnormal",
       "Chưa liên kết hệ thống bill tiền → popup hướng dẫn, không cho bật",
       CAL + "\n- Bot A CHƯA liên kết Stripe lẫn UnivaPay",
       "1. Bấm bật bill tiền → quan sát popup\n"
       "2. Bấm「決済連携をする」\n3. Đóng popup, bấm bật bill tiền lại\n"
       "4. Bấm「決済システム連携設定」",
       "Chưa liên kết cổng nào",
       "- Popup:「決済機能をご利用される場合 事前にStripeまたはUnivaPayアカウントの作成が必要です。」\n"
       "  · nền màu #FFFFFF, hiển thị ở GIỮA màn hình\n"
       "- Bấm 決済連携をする: redirect sang màn liên kết hệ thống bill tiền\n"
       "- Bước 3: hiện lại popup và KHÔNG cho phép bật\n"
       "- Bấm 決済システム連携設定: mở TAB MỚI tới /basic/list-items",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r8-r11."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Normal",
       "Droplist cổng thanh toán hiển thị theo cổng đã liên kết",
       CAL,
       "1. Bot chỉ liên kết Stripe → mở droplist chọn cổng\n"
       "2. Bot chỉ liên kết UnivaPay → mở droplist\n3. Bot liên kết cả 2 → mở droplist",
       "3 cấu hình liên kết",
       "- Chỉ Stripe: droplist chỉ có Stripe\n- Chỉ UnivaPay: chỉ có Univapay\n"
       "- Cả 2: droplist có cả 2 lựa chọn",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r12-r14, r56-r57."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Abnormal",
       "Bật bill tiền khi 2 friend info mặc định (họ tên, email) đang OFF → báo lỗi",
       CAL + "\n- 2 item mặc định họ tên và email đang OFF ở màn 質問項目",
       "1. Bấm bật bill tiền\n2. Quan sát message",
       "2 item mặc định OFF",
       "- Báo lỗi「予約時のお客様への質問項目にメールとお名前を追加してから、有効してください。」\n"
       "- KHÔNG bật được bill tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r15 + spec BR-50."),

    tc("決済連携 — cài đặt", "FUNC-004", "Boundary",
       "Ô mô tả (特商法) — biên 5000/5001 ký tự, cả 2 cổng × 2 môi trường",
       CAL + "\n- Đã bật bill tiền",
       "Với từng cấu hình (Stripe-test · Stripe-product · UnivaPay-test · UnivaPay-product):\n"
       "1. Để trống ô mô tả → Lưu\n2. Nhập 5000 ký tự tiếng Nhật → Lưu → kiểm hiển thị phía LINE user\n"
       "3. Nhập 5001 ký tự → Lưu",
       "4 cấu hình × 3 giá trị",
       "- Để trống: save success\n- 5000 ký tự: save success, LINE user thấy đúng nội dung ở màn "
       "特定商取引法に関する記載\n- 5001 ký tự: Invalid",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r16-r18, r22-r24, r28-r30, r34-r36."),

    tc("決済連携 — cài đặt", "UI-001", "Normal",
       "2 link phụ trên màn 決済連携",
       CAL,
       "1. Bấm「テスト決済時のダミーカード番号一覧」\n2. Bấm「特定商取引ガイド」",
       "—",
       "- Bước 1: hiện alert/màn chứa danh sách thẻ test\n"
       "- Bước 2: mở tab mới tới https://www.no-trouble.caa.go.jp/what/mailorder/",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r40-r41."),

    tc("決済連携 — cài đặt", "DATA-AUDIT-001", "Normal",
       "Màn lịch sử 変更履歴 của setting bill tiền — 6 loại nội dung thay đổi",
       CAL + "\n- Đã thay đổi setting bill tiền nhiều lần bởi admin chính và staff",
       "1. Mở màn 変更履歴 → quan sát cột thời gian và người thao tác\n"
       "2. Thực hiện đủ 6 chuyển đổi rồi kiểm cột nội dung:\n"
       "OFF→ON môi trường test · OFF→ON môi trường product · test→product · product→test · "
       "test→OFF · product→OFF",
       "6 chuyển đổi",
       "- Cột thời gian format「2024.09.25 (金) 10:31」\n"
       "- Cột người thao tác: đúng user chính / staff\n"
       "- Nội dung tương ứng:「停止→利用中(テスト環境) に変更」·「停止→利用中(本番環境) に変更」·"
       "「テスト環境→本番環境 に変更」·「本番環境→テスト環境 に変更」·「テスト環境→停止 に変更」·"
       "「本番環境→停止 に変更」",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r42-r50."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Abnormal",
       "Hủy liên kết cổng thanh toán SAU KHI calendar đã chọn cổng đó",
       CAL + "\n- Calendar đang chọn Stripe; U1 đã có 1 booking chờ approve với thẻ đã lưu",
       "1. Ở màn liên kết chung, HỦY liên kết Stripe\n"
       "2. U2 booking mới → quan sát màn nhập thẻ\n3. Admin approve booking cũ của U1 → quan sát",
       "Hủy liên kết sau khi có booking",
       "- Bước 2: đến màn nhập thẻ KHÔNG hiển thị được phần nhập thẻ\n"
       "- Bước 3: booking của U1 VẪN bị bill tiền (do đã có thông tin thẻ)",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r58-r59. ⚠️ TC gốc r59 ghi「vẫn bill tiền do có thông tin card ?」"
            "— có dấu hỏi, chưa chốt. Xem MT-45."),

    tc("決済連携 — cài đặt", "PAY-STATE-001", "Normal",
       "Chưa liên kết cổng nào + calendar không bill → 4 luồng booking đều thành công",
       CAL + "\n- Bot chưa liên kết Stripe/UnivaPay; calendar không bật bill tiền",
       "1. U1 book, calendar setting approve ngay → kiểm\n2. U2 book, setting chờ approve → kiểm\n"
       "3. Admin approve U2 → kiểm\n4. Admin từ chối 1 booking khác → kiểm",
       "4 luồng",
       "- Cả 4 luồng: thao tác thành công, không lỗi, không phát sinh giao dịch nào",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r52-r55."),

    # ══════════════════ 決済 — Stripe ══════════════════
    tc("決済 — Stripe", "ENV-003", "Normal",
       "Stripe môi trường TEST vs PRODUCT: thẻ thật và thẻ test cho kết quả ngược nhau",
       CAL + "\n- Calendar chọn Stripe, course Cp giá 5.000 yên",
       "1. Chọn môi trường TEST: U1 book course Cp, nhập THẺ THẬT → quan sát\n"
       "2. Cùng môi trường TEST: U2 nhập THẺ TEST (4242 4242 4242 4242) → quan sát\n"
       "3. Chọn môi trường PRODUCT: U3 nhập THẺ THẬT → quan sát\n"
       "4. Cùng PRODUCT: U4 nhập THẺ TEST → quan sát\n5. Kiểm dashboard Stripe cả 2 môi trường",
       "2 môi trường × 2 loại thẻ",
       "- TEST + thẻ thật: bill LỖI\n- TEST + thẻ test: bill THÀNH CÔNG\n"
       "- PRODUCT + thẻ thật: bill THÀNH CÔNG (tiền thật bị trừ)\n- PRODUCT + thẻ test: bill LỖI\n"
       "- Course Cf (không giá): mọi tổ hợp đều booking OK, không bill",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r19-r21, r25-r27. RULE-08."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Stripe: admin DISABLE bill tiền → mọi luồng đều không thu tiền",
       CAL + "\n- Calendar DISABLE bill tiền; course Cp có giá, Cf không giá",
       "1. U1 book Cp → kiểm\n2. U2 book Cf → kiểm\n3. Kiểm dashboard Stripe",
       "2 course",
       "- Cả 2: booking thành công, KHÔNG thu tiền, không có giao dịch trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r60-r61."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Stripe ENABLE + course KHÔNG giá → 11 luồng thao tác đều không thu tiền",
       CAL + "\n- Calendar ENABLE bill Stripe; course Cf KHÔNG có giá",
       "Thực hiện đủ 11 luồng, sau mỗi luồng kiểm `payment_status` và dashboard Stripe:\n"
       "1. Admin book\n2. User book approve ngay\n3. User book chờ approve\n4. Admin approve\n"
       "5. Admin từ chối\n6. Admin approve đồng loạt nhiều booking\n7. Admin từ chối đồng loạt\n"
       "8. Admin cancel booking\n9. User cancel được approve ngay\n10. User cancel chờ approve\n"
       "11. Admin approve request cancel / từ chối request cancel",
       "11 luồng",
       "- Cả 11 luồng: thao tác thành công, KHÔNG thu tiền của user, "
       "không có giao dịch trên Stripe, `payment_status` = 2 (決済なし)",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r62-r73 (12 dòng CÙNG kết quả → gộp 1 TC, "
            "liệt kê đủ 11 luồng ở cột Các bước)."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Stripe + course CÓ giá + thẻ thường (4242…4242): ma trận 11 luồng — thu tiền lúc nào",
       CAL + "\n- Calendar ENABLE bill Stripe môi trường test; course Cp giá 5.000 yên\n"
             "- Dùng thẻ 4242 4242 4242 4242 (không cần 3D Secure)",
       "Thực hiện 11 luồng, sau mỗi luồng kiểm `payment_status` và dashboard Stripe:\n"
       "1. Admin book\n2. User book approve ngay\n3. User book chờ approve (lúc vừa book)\n"
       "4. Admin approve booking đó\n5. Admin từ chối\n6. Admin approve đồng loạt\n"
       "7. Admin từ chối đồng loạt\n8. Admin cancel booking đã approve\n9. User cancel approve ngay\n"
       "10. User cancel chờ approve\n11. Admin approve / từ chối request cancel",
       "11 luồng",
       "- CÓ thu tiền: luồng 2 (book approve ngay), luồng 4 (admin approve), luồng 6 (các booking "
       "được approve đều bị thu)\n"
       "- KHÔNG thu tiền: luồng 1, 3, 5, 7, 8, 9, 10, 11\n"
       "- Luồng 4: đồng thời đổi trạng thái booking sang 予約確定",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r74-r85."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Stripe 3D Secure (4000 0038 0000 0446): 3 nhánh ở popup xác thực",
       CAL + "\n- Calendar ENABLE bill Stripe, course Cp giá 5.000 yên, setting approve ngay",
       "1. U1 book course Cp, nhập thẻ 3D → quan sát popup xác thực\n"
       "2. Bấm complete → kiểm booking và Stripe\n"
       "3. U2 lặp lại, bấm HỦY ở popup → quan sát\n4. U3 lặp lại, bấm FAIL ở popup → quan sát",
       "Thẻ 3D Secure",
       "- Hiện popup 3D Secure\n"
       "- complete: bill THÀNH CÔNG, booking approve\n"
       "- hủy và fail: báo lỗi, QUAY LẠI màn nhập thẻ để user nhập lại; booking KHÔNG được tạo "
       "(hoặc bị xóa) và không thu tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r87."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Stripe 3D Secure ở chế độ リクエスト制 → chỉ LƯU THẺ, thu tiền khi admin approve",
       CAL + "\n- Calendar ENABLE bill Stripe, setting リクエスト制, course Cp giá 5.000 yên",
       "1. U1 book, nhập thẻ 3D, bấm complete ở popup → kiểm booking và dashboard Stripe\n"
       "2. Admin approve booking của U1 → kiểm lại\n3. Với U2: admin TỪ CHỐI → kiểm",
       "Chế độ chờ approve",
       "- Bước 1: booking thành công status リクエスト, KHÔNG thu tiền (Stripe chỉ có setupIntent)\n"
       "- Bước 2: THU TIỀN và đổi trạng thái booking sang 予約確定\n"
       "- Bước 3: KHÔNG thu tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r88-r90 + spec BR-P22 (Stripe + approve_type=2 ⇒ chỉ lưu thẻ)."),

    tc("決済 — Stripe", "PAY-STATE-001", "Abnormal",
       "Stripe: thẻ bị từ chối (decline / error) → báo lỗi, clear thông tin thẻ",
       CAL + "\n- Calendar ENABLE bill Stripe, course Cp giá 5.000 yên",
       "1. U1 book, nhập thẻ 4000 0084 0000 1629 (decline) → quan sát\n"
       "2. U2 book, nhập thẻ 4000 0084 0000 1280 (error) → quan sát\n"
       "3. Quan sát ô nhập thẻ sau khi báo lỗi",
       "2 thẻ lỗi",
       "- Cả 2: báo lỗi「Your card was declined」\n"
       "- Redirect về màn nhập thẻ và CLEAR thông tin thẻ đã nhập\n"
       "- Không tạo booking, không thu tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r98-r99."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Đổi setting bill tiền: ảnh hưởng booking cũ và booking mới",
       CAL + "\n- Course Cp có giá; có 1 booking cũ đang chờ approve (đặt lúc calendar CHƯA bill tiền)",
       "1. Đổi từ KHÔNG bill tiền sang CÓ bill tiền\n"
       "2. Admin approve booking cũ → kiểm thu tiền\n3. Cho U2 booking MỚI → quan sát\n"
       "4. Đổi ngược từ CÓ bill sang KHÔNG bill (chuẩn bị 1 booking cũ đã nhập thẻ)\n"
       "5. Admin approve booking cũ → kiểm\n6. Cho U3 booking MỚI → quan sát",
       "2 chiều đổi setting",
       "- Bước 2: KHÔNG thu tiền (booking cũ không có thông tin thẻ)\n"
       "- Bước 3: CÓ bill tiền, U2 phải qua màn nhập thẻ\n"
       "- Bước 5: VẪN thu tiền (booking cũ đã có thông tin thẻ)\n"
       "- Bước 6: booking thành công, KHÔNG thu tiền, không qua màn nhập thẻ\n"
       "⇒ Việc thu tiền tính theo THỜI ĐIỂM BOOKING, không theo setting hiện tại",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r100-r103, r131-r134."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Improve bill Stripe: tạo booking TRƯỚC khi thu tiền, bill fail thì xóa và trừ lại bộ đếm",
       CAL + "\n- Calendar ENABLE bill Stripe, setting approve ngay, course Cp giá 5.000 yên\n"
             "- Slot S1 `total_booking` = 0, `total_approve` = 0",
       "1. U1 bấm nút booking ở màn confirm cuối → NGAY LẬP TỨC query "
       "`calendar_course_bookings` và `calendar_course_receptions`\n"
       "2. Cho bill THÀNH CÔNG (thẻ 4242…) → query lại\n"
       "3. Với U2: cho bill FAIL (thẻ 4000 0000 0000 0341) → query lại\n"
       "4. Kiểm action/remind/sync Google của U1 và U2",
       "1 booking success + 1 fail",
       "- Bước 1: phía user hiện loading; DB đã tạo booking với `payment_status` = 0, "
       "`status_webhook` = 3, đã lưu thông tin bill; `total_booking` +1, `total_approve` +1\n"
       "- Bước 2: update `payment_status` = 1, `status_webhook` = 1; GỬI action booking, "
       "ADD remind, SYNC lên Google Sheet; bộ đếm GIỮ NGUYÊN\n"
       "- Bước 3: XÓA booking vừa tạo; KHÔNG gửi action, KHÔNG add remind, KHÔNG sync Google; "
       "`total_booking` −1, `total_approve` −1",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r11-r15 + Task nhỏ + fix bug KH r2-r18. "
            "RULE-07: verify DB + bộ đếm + action + remind + Google Sheet."),

    tc("決済 — Stripe", "PAY-ABANDON-001", "Normal",
       "Improve bill Stripe: job quét kết quả bill — success / fail / đóng trình duyệt ở 3D",
       CAL + "\n- Calendar ENABLE bill Stripe",
       "1. Tạo booking rơi vào trạng thái `status_webhook` = 3, chờ job quét trả về SUCCESS → "
       "kiểm DB + tin LINE user\n"
       "2. Tái hiện fail: nhập thẻ 4000 0000 0000 0341 (booking bị xóa) → fake lại bản ghi giống hệt "
       "và update số count limit → chờ job → kiểm\n"
       "3. Với thẻ 3D: mở modal confirm rồi ĐÓNG TRÌNH DUYỆT (chưa bill) → chờ job → kiểm",
       "3 kịch bản job",
       "- Kịch bản 1: `payment_status` = 1, `status_webhook` = 1; gửi action + add remind + sync Google; "
       "user nhận msg「決済が完了しました。」\n"
       "- Kịch bản 2: XÓA booking, `total_booking` −1, `total_approve` −1; không gửi action/remind/sync; "
       "user nhận msg「決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき再度、"
       "購入手続きを行なってください。」\n"
       "- Kịch bản 3 (spec change 10/2025): KHÔNG tính là bill fail — vẫn xóa booking và trừ bộ đếm "
       "nhưng KHÔNG gửi msg thanh toán fail cho user",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r16-r18. RULE-08: job nền test PRODUCTION."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "Improve bill Stripe: full slot và booking request KHÔNG bill tiền",
       CAL + "\n- Calendar ENABLE bill Stripe, đã bật 空き枠通知受け取り設定\n- Slot S1 đã full",
       "1. U1 đăng ký nhận thông báo ở slot full → query DB\n"
       "2. Khi có chỗ trống → U1 nhận msg → U1 book lại (setting approve ngay) → query\n"
       "3. Với calendar setting リクエスト制 (không approve luôn): U2 book, nhập thẻ → query",
       "Full slot + request",
       "- Bước 1: booking status = 3, `payment_status` = 2, `payment_system` = NULL, "
       "`payment_amount` = 0, `status_webhook` = 1; user nhận msg đăng ký full slot; KHÔNG bill tiền\n"
       "- Bước 2: user nhận msg slot trống rồi book lại và bill bình thường\n"
       "- Bước 3: booking success với `payment_status` = 0, `status_webhook` = 0; "
       "`total_request` +1; CHƯA bill tiền",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r4-r10, r51-r52."),

    tc("決済 — Stripe", "PAY-STATE-001", "Normal",
       "SpecImprove #34857: description trên Stripe hiển thị tên course — 8 kiểu ký tự",
       CAL + "\n- Calendar ENABLE bill Stripe, setting approve ngay",
       "Với từng kiểu tên course, cho user booking + bill thành công rồi kiểm dashboard Stripe:\n"
       "1. Tên có ký tự「0」\n2. Tên có space phía TRƯỚC\n3. Space phía SAU\n"
       "4. Nhiều space Ở GIỮA\n5. Ký tự đặc biệt latin ` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [] |. , / * \\:?\n"
       "6. Ký tự đặc biệt Nhật ・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞\n"
       "7. Hiragana+katakana+kanji「まことボット智恵助」\n8. Nhật + latin + emoji「AIボット🤖_Ver1」và"
       "「こーだい/プレゼント専用🎁」",
       "8 kiểu tên course",
       "- Cả 8 kiểu: booking thành công; trên Stripe hiển thị description chứa TÊN COURSE\n"
       "- DB: `payment_system` = 0, `payment_status` = 1, `status_webhook` = 1\n"
       "- Space đầu/cuối tự động TRIM khi bấm Lưu course\n"
       "- Space ở GIỮA không tự clear khi lưu, nhưng khi hiển thị phía user và trong description "
       "trên Stripe thì được clear\n"
       "- Format description bên Stripe:「Server https://step.lme.jp/-> (tên course)」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r36-r44, r58-r59 (SpecImprove #34857, 03/2026)."),

    tc("決済 — Stripe", "PAY-STATE-001", "Abnormal",
       "SpecImprove #34857: calendar KHÔNG bill tiền → không hiện gì trên Stripe",
       CAL + "\n- Calendar KHÔNG setting bill tiền",
       "1. Setting không approve luôn: U1 book → kiểm dashboard Stripe\n"
       "2. Setting approve luôn: U2 book → kiểm",
       "2 chế độ duyệt",
       "- Cả 2: booking thành công, KHÔNG có giao dịch nào trên màn quản lý Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r33-r34."),

    tc("決済 — Stripe", "PAY-STATE-001", "Abnormal",
       "SpecImprove #34857: bill fail VẪN hiện trên Stripe với status failed",
       CAL + "\n- Calendar ENABLE bill Stripe, setting approve ngay",
       "1. U1 book, nhập thẻ fail 4000 0000 0000 0341 → kiểm dashboard Stripe\n"
       "2. U2 book, nhập thẻ 3D 4000 0038 0000 0446 rồi bấm FAIL/HỦY ở modal → kiểm",
       "2 kiểu fail",
       "- Cả 2: trên Stripe VẪN có bản ghi giao dịch với status = failed "
       "(không phải im lặng không tạo gì)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r49-r50."),

    tc("決済 — Stripe", "PAY-STATE-001", "Abnormal",
       "SpecImprove #34857: admin book (web và app) KHÔNG bill tiền, không lên Stripe",
       CAL + "\n- Calendar ENABLE bill Stripe, course Cp giá 5.000 yên",
       "1. Admin book ở WEB cho friend TRONG hệ thống → kiểm Stripe\n"
       "2. Admin book ở WEB cho khách NGOÀI hệ thống → kiểm\n"
       "3. Admin book ở APP cho friend trong hệ thống → kiểm\n"
       "4. Admin book ở APP cho khách ngoài hệ thống → kiểm",
       "4 lối admin book",
       "- Cả 4: booking thành công, KHÔNG bill tiền, không có giao dịch trên Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r45-r48, r54-r57."),

    tc("決済 — Stripe", "FUNC-002", "Abnormal",
       "SpecImprove #34857: course KHÔNG có tên → chặn",
       CAL,
       "1. Thử tạo/sửa course với tên rỗng → Lưu",
       "Tên course rỗng",
       "- Tên course là BẮT BUỘC, không lưu được course không tên "
       "⇒ luôn có description để gửi lên Stripe",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r60."),

    tc("決済 — Stripe", "CONC-001", "Abnormal",
       "Double click nút booking ở màn confirm bill tiền → không bill 2 lần",
       CAL + "\n- Calendar ENABLE bill Stripe, course Cp giá 5.000 yên",
       "1. U1 đến màn confirm cuối, double click nhanh nút booking\n"
       "2. Query `calendar_course_bookings`\n3. Kiểm dashboard Stripe",
       "1 lần đặt, 2 click",
       "- Chỉ tạo ĐÚNG 1 booking\n- Trên Stripe chỉ có ĐÚNG 1 giao dịch (không bill trùng)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r21, r53 + Sửa bill tiền univapay r23 "
            "— TC gốc CHỈ CÓ TIÊU ĐỀ ở phần Stripe; kết quả mong đợi lấy theo TC tương đương "
            "của UnivaPay (r23) đã có kết quả rõ."),

    tc("決済 — Stripe", "CONC-001", "Abnormal",
       "Slot còn 1 chỗ, 2 user cùng bấm mua → 1 người book được, người kia báo lỗi",
       CAL + "\n- Calendar ENABLE bill tiền (test cả Stripe và UnivaPay)\n- Slot S1 còn ĐÚNG 1 chỗ",
       "1. U1 và U2 cùng bấm nút mua/booking trong cùng 1 giây\n"
       "2. Query `calendar_course_bookings` đếm booking chiếm chỗ của slot S1\n"
       "3. Kiểm dashboard cổng thanh toán\n4. Kiểm tin LINE của U1 và U2",
       "2 user, 1 chỗ",
       "- Chỉ 1 user book được, user còn lại BÁO LỖI\n"
       "- DB: chỉ 1 booking chiếm chỗ; `total_booking` = 1\n"
       "- Cổng thanh toán: chỉ 1 giao dịch thành công — user thua KHÔNG bị trừ tiền "
       "(hoặc nếu bị trừ thì phải được hoàn tự động)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ + fix bug KH r9, r18 + Sửa bill tiền univapay r18. "
            "🔴 Spec RA-02/RP-02: KHÔNG có khoá DB, arbiter chỉ bắt request TRÙNG TỚI GIÂY và chỉ xét "
            "status = 1 ⇒ rủi ro FAIL cao. Xem thêm TC Bug KH #38280 ở nhóm Đồng thời & verify API."),

    # ══════════════════ 決済 — UnivaPay & webhook ══════════════════
    tc("決済 — UnivaPay & webhook", "ENV-003", "Normal",
       "UnivaPay môi trường TEST vs PRODUCT: thẻ thật và thẻ test",
       CAL + "\n- Calendar chọn UnivaPay, course Cp giá 5.000 yên",
       "1. Môi trường TEST: U1 nhập thẻ thật → quan sát; U2 nhập thẻ test → quan sát\n"
       "2. Môi trường PRODUCT: U3 nhập thẻ thật → quan sát; U4 nhập thẻ test → quan sát\n"
       "3. Kiểm dashboard UnivaPay tương ứng",
       "2 môi trường × 2 loại thẻ",
       "- TEST + thẻ thật: bill LỖI · TEST + thẻ test: bill THÀNH CÔNG\n"
       "- PRODUCT + thẻ thật: bill THÀNH CÔNG · PRODUCT + thẻ test: bill LỖI",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r31-r33, r37-r39."),

    tc("決済 — UnivaPay & webhook", "PAY-STATE-001", "Normal",
       "UnivaPay: ma trận 11 luồng khi ENABLE bill + course có giá / không giá",
       CAL + "\n- Calendar ENABLE bill UnivaPay, thẻ test 4242424242424242",
       "Lặp cho course Cf (không giá) và course Cp (có giá), thực hiện 11 luồng:\n"
       "admin book · user book approve ngay · user book chờ approve · admin approve · admin từ chối · "
       "approve đồng loạt · từ chối đồng loạt · admin cancel · user cancel approve ngay · "
       "user cancel chờ approve · admin approve/từ chối request cancel",
       "2 course × 11 luồng",
       "- Course Cf: TẤT CẢ 11 luồng đều KHÔNG thu tiền\n"
       "- Course Cp: CHỈ thu tiền ở luồng「user book approve ngay」·「admin approve」·"
       "「approve đồng loạt (các booking được approve)」; 8 luồng còn lại KHÔNG thu tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r104-r129 (2 khối 13 dòng → gộp 1 TC ma trận, đủ điểm ở "
            "cột Các bước)."),

    tc("決済 — UnivaPay & webhook", "PAY-STATE-001", "Abnormal",
       "UnivaPay: thẻ 4111 1111 1111 1111 → báo lỗi",
       CAL + "\n- Calendar ENABLE bill UnivaPay, course Cp giá 5.000 yên",
       "1. U1 book, nhập thẻ 4111 1111 1111 1111 → quan sát\n2. Query DB và kiểm UnivaPay",
       "Thẻ invalid",
       "- Báo lỗi ngay lúc submit thẻ (thẻ không tồn tại)\n"
       "- KHÔNG tạo booking chiếm chỗ, không thu tiền",
       env="PRODUCTION",
       note="Nguồn: Liên kết bill tiền r130 + Sửa bill tiền univapay r74. ⚠️ TC gốc r130 ghi "
            "「báo lỗi card ko tồn tại ?」— có dấu hỏi. Xem MT-46."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "UnivaPay callback: booking mới — luồng 2 pha (tạo trước, cập nhật sau)",
       CAL + "\n- Calendar ENABLE bill UnivaPay, setting approve ngay, course Cp giá 5.000 yên\n"
             "- Slot S1 `total_booking` = 0",
       "1. U1 bấm nút booking ở màn confirm → NGAY LẬP TỨC query "
       "`calendar_course_bookings` và `calendar_course_receptions`\n"
       "2. Cho callback SUCCESS về trong khoảng 3-5 phút → query lại + kiểm tin LINE U1\n"
       "3. Với U2: cho callback FAIL về → query lại + kiểm tin",
       "1 success + 1 fail",
       "- Bước 1: phía user hiện loading; DB có booking với `payment_status` = 0, "
       "`status_webhook` = 0, đã lưu thông tin bill; `total_booking` +1, `total_approve` +1\n"
       "- Bước 2: `payment_status` = 1, `status_webhook` = 1, lưu thêm charge id; "
       "GỬI action booking + ADD remind + SYNC Google; bộ đếm GIỮ NGUYÊN; "
       "U1 nhận msg「決済が完了しました。」\n"
       "- Bước 3: `payment_status` = 0, `status_webhook` = 2 + mã lỗi ⇒ XÓA booking; "
       "không gửi action/remind/sync; `total_booking` −1, `total_approve` −1; "
       "U2 nhận msg「決済に失敗しました。 カードのご利用枠や有効期限などをご確認いただき再度、"
       "購入手続きを行なってください。」",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r2, r9-r10, r15-r16. RULE-07: verify DB + bộ đếm + "
            "action + remind + Google + tin LINE."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Boundary",
       "UnivaPay: callback về TRƯỚC 2 phút — 2 nhánh success/fail (đã đổi spec không gửi msg)",
       CAL + "\n- Calendar ENABLE bill UnivaPay, setting approve ngay",
       "1. U1 book, cho callback SUCCESS về TRƯỚC 2 phút → quan sát màn hình U1 và tin LINE\n"
       "2. U2 book, cho callback FAIL về TRƯỚC 2 phút → quan sát",
       "Callback < 2 phút",
       "- Success: hiện màn booking success bình thường; theo SPEC ĐÃ SỬA — KHÔNG gửi msg "
       "「決済が完了しました。」\n"
       "- Fail: hiện message thông báo lỗi, VẪN ở màn confirm cuối để user bấm back về màn nhập "
       "thẻ nhập lại; theo SPEC ĐÃ SỬA — KHÔNG gửi msg「決済に失敗しました。」",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r11-r12 (ghi rõ「=> sửa lại case này không send message "
            "…nữa」). ⚠️ MÂU THUẪN với r15-r16 (callback 3-5 phút thì CÓ gửi msg). Xem MT-47."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-002", "Boundary",
       "UnivaPay: quá 2 phút chưa có callback → màn chờ; quá 5 phút → status_webhook = 4",
       CAL + "\n- Calendar ENABLE bill UnivaPay",
       "1. U1 book, chặn callback → chờ quá 2 phút → quan sát màn hình U1\n"
       "2. Bấm「画面を閉じる」→ quan sát\n3. Chờ quá 5 phút → query `status_webhook`\n"
       "4. Sau đó cho callback SUCCESS về → query lại + kiểm tin LINE\n"
       "5. Với U2: sau 5 phút cho callback FAIL về → query lại + kiểm tin",
       "Callback trễ > 5 phút",
       "- Bước 1: hiện màn thông báo「決済処理を行っています」theo design\n- Bước 2: đóng màn hình\n"
       "- Bước 3: `status_webhook` = 4\n"
       "- Bước 4: cập nhật như case bill success — `payment_status` = 1, `status_webhook` = 1, "
       "charge id; gửi action + remind + sync Google; U1 nhận msg「決済が完了しました。」\n"
       "- Bước 5 (theo LOGIC MỚI): XÓA booking; `total_booking` −1, `total_approve` −1; "
       "U2 nhận msg thanh toán fail",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r13-r14, r19-r21. ⚠️ r21 ghi 2 hành vi chồng nhau: "
            "logic cũ「update status = 7, payment_status = 2」và「=> sửa lại theo logic mới sẽ XÓA "
            "booking」— đã lấy theo logic MỚI. Xem MT-48."),

    tc("決済 — UnivaPay & webhook", "PAY-ABANDON-001", "Normal",
       "UnivaPay: user đóng màn hình khi đang loading → vẫn xử lý theo callback",
       CAL + "\n- Calendar ENABLE bill UnivaPay",
       "1. U1 bấm booking, trong lúc đang loading thì ĐÓNG màn hình LIFF\n"
       "2. Cho callback SUCCESS về → query DB + kiểm tin LINE U1",
       "Đóng màn giữa chừng",
       "- Màn hình đóng bình thường (không treo)\n"
       "- Khi callback về: hệ thống VẪN xử lý đúng theo kết quả callback "
       "(booking được cập nhật hoặc xóa tương ứng)",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r22."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Boundary",
       "Bug #29846: full slot rồi book lại — msg 決済が完了しました phụ thuộc mốc 2 phút",
       CAL + "\n- Calendar ENABLE bill UnivaPay, bật 空き枠通知受け取り設定\n- Slot S1 đã full",
       "1. U1 đăng ký nhận thông báo ở S1 → query DB\n"
       "2. Khi có chỗ trống, U1 booking lại\n"
       "3. Cho callback SUCCESS về NGAY (< 2 phút) → kiểm tin LINE + query bộ đếm\n"
       "4. Với U2: callback SUCCESS về SAU 2 phút → kiểm\n"
       "5. Với U3: callback FAIL về TRƯỚC 2 phút → kiểm\n"
       "6. Với U4: callback FAIL về SAU 2 phút → kiểm",
       "4 mốc callback",
       "- Bước 1: booking status = 3, `payment_status` = 2, `payment_system` = NULL, "
       "`payment_amount` = 0, `status_webhook` = 1; user nhận msg đăng ký full slot\n"
       "- Bước 3: booking success, KHÔNG gửi msg「決済が完了しました。」\n"
       "- Bước 4: booking success, CÓ gửi msg「決済が完了しました。」\n"
       "- Bước 5: XÓA booking, KHÔNG gửi msg thanh toán fail\n"
       "- Bước 6: XÓA booking, CÓ gửi msg thanh toán fail\n"
       "- Bộ đếm: `total_booking` và `total_approve` update NGAY lúc booking lại; "
       "`total_request_booking_wait_cancel` CHỈ update SAU khi có callback",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r24-r29, r69-r72 (Refer Bug #29846 — truy nguồn msg "
            "決済が完了しました không rõ trigger)."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "UnivaPay: admin approve ở WEB — callback trước/sau 2 phút",
       CAL + "\n- Calendar ENABLE bill UnivaPay, setting リクエスト制\n"
             "- Có booking B1 đang リクエスト với thẻ đã lưu",
       "1. Admin bấm approve B1 → NGAY query `status_webhook`\n"
       "2. Cho callback SUCCESS về < 2 phút → query DB + reload màn hình + kiểm tin LINE + "
       "kiểm chat 1:1 + Google Sheet\n"
       "3. Với B2: callback FAIL về < 2 phút → query\n"
       "4. Với B3: chờ quá 2 phút chưa có callback → quan sát màn hình admin\n"
       "5. Sau đó cho callback SUCCESS về → query; với B4 cho callback FAIL → query",
       "4 booking, 4 kịch bản",
       "- Bước 1: `status_webhook` = 0\n"
       "- Bước 2: `status_webhook` = 1, `status` = 1, `payment_status` = 1 + charge id; "
       "gửi action + add remind (KIỂM TRIGGER hiển thị trên CHAT 1:1) + sync Google; "
       "KHÔNG gửi msg bill thành công (khác case book mới); `total_booking` +1, `total_approve` +1, "
       "`total_request` −1\n"
       "- Bước 3: báo lỗi, `status_webhook` = 2; KHÔNG đổi status booking, không đổi "
       "`payment_status`, không gửi action/remind/sync; bộ đếm GIỮ NGUYÊN\n"
       "- Bước 4: hiện message「この処理には2~3分かかる場合があります。画面を閉じてお待ちください」, "
       "reload màn hình, KHÔNG update booking\n"
       "- Bước 5: xử lý giống bước 2 và 3 tương ứng",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r30-r35."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "UnivaPay: admin approve ở APP MOBILE — 2 lối vào detail booking",
       CAL + "\n- Calendar ENABLE bill UnivaPay, setting リクエスト制\n"
             "- App mobile admin đã đăng nhập bot A",
       "Với CẢ 2 lối vào (từ màn list booking của lesson VÀ từ màn notify):\n"
       "1. Mở detail booking → bấm approve → NGAY query `status_webhook`\n"
       "2. Cho callback SUCCESS về < 5 phút → query + kiểm action/remind/Google\n"
       "3. Cho callback FAIL → query\n"
       "4. Chờ quá 2 phút chưa có callback → quan sát app\n"
       "5. Trong lúc `status_webhook` = 0, bấm approve hoặc deny lần nữa → quan sát",
       "2 lối vào × 5 bước",
       "- Bước 1: thực hiện bill tiền, `status_webhook` = 0\n"
       "- Bước 2: `status_webhook` = 1, approve success; action/remind/sync Google chạy bình thường\n"
       "- Bước 3: báo lỗi bill fail, `status_webhook` = 2; KHÔNG update status booking; "
       "không gửi action/remind/sync\n"
       "- Bước 4, 5: hiện message「この処理には2~3分かかる場合があります。画面を閉じてお待ちください。」, "
       "reload màn hình, KHÔNG update booking",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r49-r58."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "UnivaPay: approve đồng loạt nhiều booking — xử lý TUẦN TỰ, gặp lỗi thì dừng",
       CAL + "\n- Calendar ENABLE bill UnivaPay\n"
             "- 3 booking B1, B2, B3 đang リクエスト; B1 và B3 có bill tiền, B2 course free",
       "1. Tick 3 booking → approve đồng loạt → NGAY query `status_webhook` của cả 3\n"
       "2. Cho callback của B1 SUCCESS → query\n"
       "3. Cho callback của B3 FAIL → quan sát message và query\n"
       "4. Chờ quá 2 phút không có callback → quan sát màn hình",
       "3 booking, xử lý tuần tự",
       "- Bước 1: booking CÓ bill tiền được set `status_webhook` = 0; booking KHÔNG bill tiền "
       "(B2) đổi status ngay không cần `status_webhook`\n"
       "- Bước 2: B1 → `status_webhook` = 1, `status` = 1, `payment_status` = 1 + charge id; "
       "gửi action + remind (kiểm trigger trên chat 1:1) + sync Google; KHÔNG gửi msg bill thành công; "
       "bộ đếm +1/+1/−1\n"
       "- Bước 3: B3 → `status_webhook` = 2; KHÔNG đổi status; báo lỗi "
       "「一般エラーが発生しました。詳細情報は管理画面で確認できます」và DỪNG, không approve tiếp\n"
       "- Bước 4: hiện「この処理には2~3分かかる場合があります。画面を閉じてお待ちください。」, "
       "reload màn hình, KHÔNG update booking, KHÔNG approve tiếp các booking sau",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r36-r39."),

    tc("決済 — UnivaPay & webhook", "COMPAT-LEGACY-001", "Normal",
       "Bill kiểu CŨ (s_strip_bot.status_webhook = NULL): job quét kết quả 15 phút/lần",
       CAL + "\n- Bot có `s_strip_bot.status_webhook` = NULL (cấu hình bill kiểu cũ)\n"
             "- Calendar ENABLE bill tiền, course Cp giá 5.000 yên",
       "1. U1 book có bill tiền → NGAY query `status_webhook` của booking\n"
       "2. Cho kết quả bill SUCCESS trong vòng < 5 phút → query + kiểm action/remind/Google\n"
       "3. Với U2: kết quả bill FAIL → query bộ đếm\n"
       "4. Với U3: quá 5 phút chưa có kết quả → query\n"
       "5. Chờ job (15 phút/lần) chạy: lần 1 chưa có kết quả → query; "
       "khi có kết quả SUCCESS → query + kiểm tin; khi FAIL → query + kiểm tin",
       "Bill kiểu cũ",
       "- Bước 1: tạo booking với `status_webhook` = 3\n"
       "- Bước 2: `status_webhook` = 1; action/remind/sync Google chạy bình thường\n"
       "- Bước 3: XÓA booking, update `total_booking` và `total_approve`\n"
       "- Bước 4: KHÔNG xóa booking, chờ job quét\n"
       "- Bước 5: job lần 1 chưa có kết quả ⇒ giữ nguyên booking, đợi 15 phút sau chạy lại; "
       "job có kết quả SUCCESS ⇒ `status_webhook` = 1 + gửi msg「決済が完了しました。」; "
       "job có kết quả FAIL ⇒ xóa booking + trừ bộ đếm + gửi msg「決済に失敗しました。…」",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r59-r65. RULE-08: job nền test PRODUCTION."),

    tc("決済 — UnivaPay & webhook", "STATE-001", "Normal",
       "Ẩn booking đang chờ xử lý thanh toán phía LINE user — ma trận status_webhook",
       CAL + "\n- Chuẩn bị booking ở đủ tổ hợp (status, status_webhook) cho cả bill kiểu CŨ và CALLBACK",
       "Với từng tổ hợp, mở màn lịch sử booking phía LINE user và ghi kết quả:\n"
       "Bill kiểu CŨ: (status 1, sw 3) · (1, 1) · (1, NULL) · (0, đang thanh toán) · (0, bill success) · "
       "(0, bill fail)\n"
       "Bill CALLBACK: (1, sw 0) · (1, 1) · (1, 4) · (1, NULL) · (0, sw 0) · (1, sw 1 sau khi success) · "
       "(0, sw 2)",
       "13 tổ hợp",
       "- KHÔNG hiển thị ở lịch sử: (status 1, sw 3) · (status 1, sw 0) · (status 1, sw 4)\n"
       "- CÓ hiển thị: tất cả tổ hợp còn lại\n"
       "⇒ Chỉ ẩn booking đã approve mà đang chờ webhook",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r75-r88."),

    tc("決済 — UnivaPay & webhook", "STATE-001", "Abnormal",
       "Khóa thao tác admin khi booking đang chờ webhook — ma trận status_webhook (web)",
       CAL + "\n- Chuẩn bị booking ở đủ tổ hợp status × status_webhook",
       "Với từng tổ hợp, thử bấm cancel (booking đã approve) hoặc approve/deny (booking chờ approve) "
       "ở màn WEB và ghi kết quả:\n"
       "Bill kiểu CŨ: (status 1, sw 3) · (1, 1) · (1, NULL) · (0, đang thanh toán) · (0, bill success) · "
       "(0, bill fail)\n"
       "Bill CALLBACK: (1, sw 0) · (1, 1) · (1, 4) · (1, NULL) · (0, sw 0) · (0, sw 1) · (0, sw 2)",
       "13 tổ hợp",
       "- BỊ KHÓA (báo lỗi「決済処理を行っていますので、操作できません。」): "
       "(status 1, sw 3) · (1, sw 0) · (1, sw 4) · (0, đang thanh toán kiểu cũ) · (0, sw 0)\n"
       "- CHO PHÉP thao tác: tất cả tổ hợp còn lại\n"
       "- Lưu ý: bill kiểu cũ vẫn dùng cơ chế loading tới khi có kết quả (không đổi "
       "`status_webhook`), nên nếu user reload màn hình giữa chừng thì VẪN vào detail bấm "
       "approve/deny được",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r95-r107 + spec BR-23 / BR-P19. "
            "⚠️ Spec RP-04: booking kẹt `status_webhook` = 4 bị KHÓA VĨNH VIỄN với admin và ẨN khỏi "
            "lịch sử của khách, không có đường thoát tự động. Xem MT-49."),

    tc("決済 — UnivaPay & webhook", "STATE-001", "Abnormal",
       "Khóa thao tác trên APP MOBILE khi đang chờ webhook",
       CAL + "\n- App mobile admin đã đăng nhập bot A",
       "Trên APP MOBILE, với từng tổ hợp thử bấm cancel / approve / deny:\n"
       "Booking approve ngay (status 1): sw = 3 · 0 · 4 · 1 · NULL\n"
       "Booking chờ approve (status 0): sw = 0 · 1 · 2 · NULL",
       "9 tổ hợp",
       "- Booking status 1 với sw = 3, 0, 4: KHÔNG cho cancel, báo lỗi "
       "「決済処理を行っていますので、操作できません。」\n"
       "- Booking status 1 với sw = 1, NULL: CHO PHÉP cancel\n"
       "- Booking status 0 với sw = 0: KHÔNG cho approve/deny, báo cùng message\n"
       "- Booking status 0 với sw = 1, 2, NULL: CHO PHÉP approve/deny",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r108-r116."),

    tc("決済 — UnivaPay & webhook", "PERM-003", "Normal",
       "metadata trên UnivaPay có bot_id — callback sai bot_id thì KHÔNG update booking",
       CAL + "\n- Có 2 bot A và B đều liên kết UnivaPay",
       "1. LINE user booking ở bot A → kiểm metadata giao dịch trên UnivaPay\n"
       "2. Gửi callback ĐÚNG bot_id với kết quả success → query booking\n"
       "3. Gửi callback ĐÚNG bot_id với kết quả fail → query\n"
       "4. Gửi callback SAI bot_id (bot B) với kết quả success → query\n"
       "5. Gửi callback SAI bot_id với kết quả fail → query\n"
       "6. Lặp bước 1-5 cho luồng admin approve (web và app)",
       "2 bot, 4 kiểu callback",
       "- Bước 1: metadata trên UnivaPay có chứa `bot_id` (dạng mã hoá, ví dụ「m9EjWEyNWQJL」)\n"
       "- Bước 2, 3: CÓ update booking theo kết quả callback\n"
       "- Bước 4, 5: KHÔNG update booking (bỏ qua callback sai bot)\n"
       "- Bước 6: kết quả tương tự cho luồng approve",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r118-r129. ⚠️ Spec RP-07: webhook UnivaPay KHÔNG xác thực "
            "chữ ký / IP / secret ⇒ chỉ có bot_id trong metadata làm rào chắn. Xem MT-50."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "Bug Tester #38077: UnivaPay status = Authorized được coi là bill SUCCESS",
       CAL + "\n- Calendar ENABLE bill UnivaPay",
       "1. Tạo booking mới, cho giao dịch trên UnivaPay có status = **Successful** → chờ job quét → "
       "query DB + kiểm tin LINE\n"
       "2. Với booking khác, status = **Failed** → chờ job → query + kiểm tin\n"
       "3. Với booking khác, status = **Authorized** → chờ job → query + kiểm tin\n"
       "4. Lặp bước 1-3 cho luồng ADMIN APPROVE booking",
       "3 status × 2 luồng",
       "- Successful và **Authorized** cho KẾT QUẢ GIỐNG NHAU:\n"
       "  · Booking mới: `payment_status` = 1, `status_webhook` = 1 + charge id; gửi action + "
       "add remind (KIỂM TRIGGER hiển thị trên CHAT 1:1) + sync Google; user nhận msg"
       "「決済が完了しました。」; bộ đếm GIỮ NGUYÊN\n"
       "  · Admin approve: `status_webhook` = 1, `status` = 1, `payment_status` = 1; gửi action + "
       "remind + sync Google; KHÔNG gửi msg bill thành công; bộ đếm +1/+1/−1\n"
       "- Failed: XÓA booking; không gửi action/remind; `total_booking` −1, `total_approve` −1; "
       "user nhận msg「決済に失敗しました。…」",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r167-r171 (Bug Tester #38077, 06/2026 — "
            "KHỐI MỚI NHẤT của tab này)."),

    tc("決済 — UnivaPay & webhook", "PAY-STATE-001", "Normal",
       "SpecImprove #34857 (UnivaPay): description hiển thị tên course — 8 kiểu ký tự",
       CAL + "\n- Calendar ENABLE bill UnivaPay, setting approve ngay",
       "Với 8 kiểu tên course (giống bộ test của Stripe: ký tự 0 · space trước/sau/giữa · "
       "ký tự đặc biệt latin · ký tự đặc biệt Nhật · hiragana+katakana+kanji · Nhật+latin+emoji), "
       "cho user booking + bill thành công rồi kiểm dashboard UnivaPay",
       "8 kiểu tên course",
       "- Cả 8 kiểu: booking thành công; trên UnivaPay hiển thị thông tin booking có TÊN COURSE\n"
       "- Space đầu/cuối tự trim khi lưu course; space ở giữa được clear khi hiển thị và "
       "trong description",
       env="PRODUCTION",
       note="Nguồn: Sửa bill tiền univapay r140-r148."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-002", "Abnormal",
       "Setting không có Webhook ID → cần chốt hành vi",
       CAL + "\n- Calendar liên kết UnivaPay nhưng CHƯA cấu hình Webhook ID",
       "1. Cho U1 booking có bill tiền → quan sát\n"
       "2. Query `status_webhook` sau 5 phút\n3. Kiểm giao dịch trên UnivaPay",
       "Thiếu Webhook ID",
       "- Cần chốt: hệ thống có chặn bật bill tiền khi thiếu Webhook ID, hay vẫn cho booking "
       "rồi rơi vào trạng thái chờ callback vĩnh viễn (`status_webhook` = 4)",
       spec="Đã hỏi leader",
       note="Nguồn: Sửa bill tiền univapay r164 — TC gốc CHỈ CÓ TIÊU ĐỀ「Check setting không "
            "Webhook ID」, không có kết quả mong đợi. Xem MT-51."),

    tc("決済 — UnivaPay & webhook", "PERM-002", "Normal",
       "Account staff thao tác approve booking có bill tiền",
       CAL + "\n- Calendar ENABLE bill UnivaPay\n- Có staff S1 được cấp quyền route レッスン予約",
       "1. Đăng nhập staff S1 → mở detail booking đang リクエスト có bill tiền\n"
       "2. Bấm approve → theo dõi callback → query DB\n3. Kiểm lịch sử booking",
       "Account staff",
       "- Staff approve được, luồng bill tiền hoạt động giống admin chính\n"
       "- Lịch sử booking ghi người thao tác là「スタッフA」",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Sửa bill tiền univapay r165, Improve bill tiền stripe r61 — "
            "TC gốc CHỈ CÓ TIÊU ĐỀ「Check account staff」. Kết quả mong đợi do AI bổ sung. "
            "Cần Leader xác nhận staff có được phép thao tác bill tiền không."),

    tc("決済 — UnivaPay & webhook", "PAY-STATE-001", "Normal",
       "SpecImprove #34895: giảm sleep check UnivaPay — poll 5 lần × 1 giây",
       CAL + "\n- Calendar ENABLE bill UnivaPay",
       "1. U1 book có bill tiền, đo thời gian từ lúc bấm nút tới khi hiện kết quả\n"
       "2. Trường hợp UnivaPay trả kết quả nhanh (< 5 giây) → quan sát\n"
       "3. Trường hợp không có kết quả trong 5 giây → quan sát và query `status_webhook`",
       "2 kịch bản tốc độ",
       "- Bước 2: hiện kết quả ngay khi có (không chờ đủ 5 giây)\n"
       "- Bước 3: sau 5 lần poll (5 giây), trả về trạng thái pending và chuyển sang màn chờ; "
       "`status_webhook` = 4",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Info r34 (SpecImprove #34895, 03/2026) + spec BR-P24. Corpus lesson KHÔNG có TC "
            "riêng cho ticket này (link trỏ sang tab bill univapay chung) ⇒ TC do AI viết theo spec. "
            "Cần Leader xác nhận."),

    tc("決済 — UnivaPay & webhook", "INTG-HOOK-001", "Normal",
       "Bug KH #33787: thanh toán trùng lặp liên tiếp",
       CAL + "\n- Calendar ENABLE bill UnivaPay",
       "1. U1 thực hiện booking có bill tiền\n"
       "2. Gửi LẠI cùng 1 callback (cùng charge id) 2 lần liên tiếp → query DB và UnivaPay\n"
       "3. Đếm số giao dịch trên UnivaPay và số booking trong DB",
       "Callback lặp",
       "- Callback thứ 2 bị BỎ QUA (khi `status_webhook` đã ∈ {1, 2})\n"
       "- Chỉ có ĐÚNG 1 giao dịch trên UnivaPay và 1 booking trong DB\n"
       "- User KHÔNG bị trừ tiền 2 lần",
       env="PRODUCTION",
       note="Nguồn: Info r29 (Bug KH #33787, 01/2026) + spec BR-P26 (webhook idempotency — "
            "「cơ chế idempotency DUY NHẤT của toàn bộ tính năng」). Corpus lesson chỉ có cột kết quả "
            "ở tab bill univapay, không có TC mô tả — TC do AI viết theo spec. Cần Leader xác nhận."),
]
