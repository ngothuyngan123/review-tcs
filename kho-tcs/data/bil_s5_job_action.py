# -*- coding: utf-8 -*-
"""FA-026 商品販売 — Nhóm 22-25: Job bill định kỳ · Job cứu đơn treo · Action & notify · Job monitor.

Nguồn chính: 12. TCsLine_Item / tab「Quản lý sản phẩm」r334-r415 (bill job Stripe + UnivaPay + update spec
             chuyển UnivaPay sang bill job), tab「Improve bill tiền univapay」r113-r155 (state machine job bill).
Bổ sung: TCsLine_Improve chung / tab「Monitor bill tiền」r66-r91 (job monitor phần ITEM, 11/2025).

⚠ RULE-08: toàn bộ nhóm này là JOB + BILL TIỀN → môi trường test bắt buộc PRODUCTION.
"""
from _common import tc

JOB = ("- Bot A đang hoạt động, hợp đồng LME còn hạn\n"
       "- SP-C là 継続商品 テスト環境, chu kỳ 毎月, đã có hợp đồng của friend F1\n"
       "- Có quyền chạy tay cron bill định kỳ (07:00 hằng ngày)")

S5 = [
    # ══════ 22. Job bill định kỳ ══════
    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Hết hạn TRIAL → job bill kỳ đầu theo GIÁ SẢN PHẨM, chuyển trạng thái 継続中",
       JOB + "\n- Hợp đồng của F1 đang トライアル中, trial hết hạn hôm nay\n"
       "- SP-C: giá thường 3.000円, giá trial 500円",
       "1. Chạy job bill định kỳ\n2. Mở 注文詳細 của hợp đồng: đọc trạng thái, 次回決済予定日, bảng 決済履歴\n"
       "3. Đối chiếu dashboard cổng thanh toán\n4. Kiểm tra chat 1:1 của F1",
       "amount = 3.000円 · amount_first = 500円 · chu kỳ 毎月",
       "- Trạng thái hợp đồng chuyển「継続中」\n"
       "- 決済履歴 có thêm 1 dòng số tiền 3.000円 (GIÁ SẢN PHẨM, KHÔNG phải giá trial 500円)\n"
       "- 次回決済予定日 = ngày bill + 1 tháng\n- Cổng thanh toán ghi nhận đúng 3.000円\n"
       "- F1 nhận action「初回決済時」và notify tương ứng",
       env="PRODUCTION",
       note="Nguồn: Quản lý sản phẩm r334「hết hạn trial thì tiến hành bill tiền theo chu kỳ và số tiền setting "
            "(tất cả đều bill theo số tiền của sp, không bill theo số tiền bill lần đầu như logic cũ)」+ "
            "Improve bill tiền univapay r115. Khớp spec R2 (nhánh amount_first ở cron đã comment out)."),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Hợp đồng KHÔNG trial hết hạn kỳ → job bill kỳ tiếp, gia hạn 次回決済予定日",
       JOB + "\n- Hợp đồng của F1 không trial, đã bill kỳ đầu, c_expired_date là hôm nay",
       "1. Chạy job bill định kỳ\n2. Mở 注文詳細 đọc bảng 決済履歴 và 次回決済予定日\n"
       "3. Đối chiếu dashboard cổng thanh toán\n4. Kiểm tra chat 1:1 của F1",
       "amount = 3.000円 · chu kỳ 毎月",
       "- 決済履歴 có thêm 1 dòng 3.000円 trạng thái thành công\n"
       "- 次回決済予定日 = ngày bill + 1 tháng\n- Số kỳ đã thanh toán tăng 1\n"
       "- Cổng thanh toán ghi nhận đúng giao dịch\n- F1 nhận action「2回目以降決済時」+ notify",
       env="PRODUCTION",
       note="Nguồn: r335 + r395 + Improve bill tiền univapay r131."),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Job bill đúng theo 5 chu kỳ 毎週 / 毎月 / 3ヶ月毎 / 6ヶ月毎 / 毎年",
       JOB + "\n- Có 5 hợp đồng, mỗi hợp đồng 1 chu kỳ, đều tới hạn cùng ngày D",
       "1. Chạy job bill định kỳ\n2. Với từng hợp đồng: mở 注文詳細 đọc 次回決済予定日 mới\n"
       "3. Đối chiếu dashboard cổng thanh toán",
       "5 hợp đồng, cùng ngày bill D",
       "- 毎週: 次回 = D + 7 ngày\n- 毎月: D + 1 tháng\n- 3ヶ月毎: D + 3 tháng\n"
       "- 6ヶ月毎: D + 6 tháng\n- 毎年: D + 1 năm\n"
       "- Cả 5 hợp đồng đều bill thành công, cổng thanh toán ghi nhận đủ 5 giao dịch",
       env="PRODUCTION",
       note="Nguồn: r336-r340 + r397-r401 (tester đánh dấu 6 tháng và 1 năm CHƯA test)."),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Job bill hợp đồng có SỐ LƯỢNG > 1 → số tiền = giá sản phẩm × số lượng",
       JOB + "\n- Hợp đồng của F1 mua số lượng 2, giá sản phẩm 1.000円/kỳ, tới hạn hôm nay",
       "1. Chạy job bill định kỳ\n2. Mở 注文詳細 đọc số tiền dòng mới trong 決済履歴\n"
       "3. Đối chiếu dashboard cổng thanh toán",
       "1.000円 × 2 = 2.000円",
       "- Dòng bill mới có số tiền = 2.000円\n- Cổng thanh toán ghi nhận đúng 2.000円",
       env="PRODUCTION",
       note="Nguồn: r341 + r363 + r396. Spec BR-05: kỳ tiếp = s_items.amount HIỆN TẠI × quantity_purchased."),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Bill hết SỐ LẦN GIỚI HẠN → hợp đồng chuyển 決済終了, không bill nữa ở kỳ sau",
       JOB + "\n- Hợp đồng của F1 có giới hạn 3 lần bill, đã bill 2 lần, kỳ thứ 3 tới hạn hôm nay",
       "1. Chạy job bill định kỳ (lần bill thứ 3)\n2. Mở 注文詳細 đọc trạng thái hợp đồng\n"
       "3. Sang chu kỳ tiếp theo, chạy lại job bill\n4. Kiểm tra thẻ F1 và dashboard cổng thanh toán",
       "number_charge = 3, đã bill 2 lần",
       "- Sau lần bill thứ 3: hợp đồng chuyển trạng thái「決済終了」(đã hoàn thành)\n"
       "- Chạy job kỳ sau: KHÔNG phát sinh giao dịch mới, F1 KHÔNG bị trừ tiền\n"
       "- Cổng thanh toán không có giao dịch mới",
       env="PRODUCTION",
       note="Nguồn: r342「update status = đã hoàn thành」+ r354 + r405「update status_bill =2 (đã hoằn thành)」."),

    tc("Job bill định kỳ", "JOB-001", "Abnormal",
       "Bill LỖI lần 1 → tăng đếm lỗi lên 1, gửi action bill lỗi + notify, KHÔNG gia hạn",
       JOB + "\n- Hợp đồng của F1 tới hạn, thẻ đã bị vô hiệu (bill sẽ fail)\n"
       "- SP-C đã gắn action ở slot「決済エラー発生時」",
       "1. Ghi lại 次回決済予定日 hiện tại\n2. Chạy job bill định kỳ\n"
       "3. Mở 注文詳細: đọc trạng thái hợp đồng, 次回決済予定日, bảng 決済履歴\n"
       "4. Kiểm tra chat 1:1 F1 + notify admin",
       "Thẻ vô hiệu, lần lỗi đầu tiên",
       "- Hợp đồng hiển thị trạng thái bill lỗi / 延滞中\n"
       "- 決済履歴 có thêm 1 dòng ở trạng thái lỗi\n- 次回決済予定日 KHÔNG được gia hạn\n"
       "- F1 nhận action「決済エラー発生時」\n- Admin nhận notify case bill lỗi",
       env="PRODUCTION",
       note="Nguồn: r343「status = bill lỗi」+ r402 + Improve bill tiền univapay r116 (count_bill_error = 1)."),

    tc("Job bill định kỳ", "JOB-001", "Abnormal",
       "Bill LỖI lần 2 liên tiếp → đếm lỗi lên 2, tiếp tục gửi action lỗi, chưa hủy hợp đồng",
       JOB + "\n- Hợp đồng của F1 đã bill lỗi 1 lần ngày hôm trước, thẻ vẫn vô hiệu",
       "1. Chạy job bill định kỳ ngày hôm sau\n2. Mở 注文詳細 đọc trạng thái + số dòng 決済履歴\n"
       "3. Kiểm tra chat 1:1 F1",
       "Lần lỗi thứ 2 liên tiếp",
       "- Hợp đồng vẫn ở trạng thái 延滞中 (CHƯA bị hủy)\n- 決済履歴 có thêm 1 dòng lỗi nữa\n"
       "- F1 nhận action「決済エラー発生時」lần nữa",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r138-r140 (count_bill_error = 2)."),

    tc("Job bill định kỳ", "JOB-001", "Abnormal",
       "Bill LỖI 3 lần liên tiếp + KHÔNG set tự động hủy → hợp đồng vẫn sống, tiếp tục bill kỳ sau",
       JOB + "\n- SP-C có auto_cancel = 0 (không tự động hủy)\n"
       "- Hợp đồng của F1 đã bill lỗi 2 lần, thẻ vẫn vô hiệu",
       "1. Chạy job bill định kỳ (lần lỗi thứ 3)\n2. Mở 注文詳細 đọc trạng thái hợp đồng\n"
       "3. Chạy job ở kỳ tiếp theo\n4. Đọc lại trạng thái + số dòng 決済履歴",
       "auto_cancel = 0 · lần lỗi thứ 3",
       "- Hợp đồng KHÔNG bị hủy, vẫn ở trạng thái 延滞中\n"
       "- Kỳ tiếp theo job VẪN cố bill (sinh thêm dòng lỗi mới)\n"
       "- F1 tiếp tục nhận action「決済エラー発生時」",
       env="PRODUCTION",
       note="Nguồn: r344「không cancel hợp đồng, vẫn tiếp tục bill」+ r356 + r404 + univapay r148/r153. "
            "Spec BR-07: auto_cancel=0 → hợp đồng ở 延滞中 VÔ THỜI HẠN, mỗi kỳ sinh thêm 1 dòng lỗi. "
            "⚠ Spec R48: số lần lỗi KHÔNG hiển thị ở đâu trên UI → admin không biết đã lỗi mấy lần (MT-22)."),

    tc("Job bill định kỳ", "JOB-001", "Abnormal",
       "Bill LỖI 3 lần liên tiếp + CÓ set tự động hủy → hủy hợp đồng, gửi CẢ action lỗi VÀ action hủy",
       JOB + "\n- SP-C có auto_cancel = 1, đã gắn action ở slot「決済エラー発生時」và「解約時」\n"
       "- Hợp đồng của F1 đã bill lỗi 2 lần, thẻ vẫn vô hiệu",
       "1. Chạy job bill định kỳ (lần lỗi thứ 3)\n2. Mở 注文詳細 đọc trạng thái hợp đồng\n"
       "3. Kiểm tra chat 1:1 F1 (đếm số tin nhận được)\n4. Kiểm tra notify admin\n"
       "5. Kiểm tra dashboard cổng thanh toán xem subscription/token còn sống không\n"
       "6. Chạy job ở kỳ tiếp theo, kiểm tra F1 có bị trừ tiền không",
       "auto_cancel = 1 · lần lỗi thứ 3",
       "- Hợp đồng chuyển trạng thái「キャンセル済」\n"
       "- F1 nhận CẢ action「決済エラー発生時」VÀ action「解約時」\n"
       "- Admin nhận 2 notify (bill lỗi + hủy hợp đồng)\n"
       "- ★ Kiểm tra cổng thanh toán: subscription/recurring token phải ở trạng thái đã hủy\n"
       "- Kỳ tiếp theo: KHÔNG phát sinh giao dịch, F1 KHÔNG bị trừ tiền",
       env="PRODUCTION",
       note="Nguồn: r345 + r357「1. change status của order sang hủy hợp đồng 2. Hủy bill tiền trên univapay」"
            "+ r403 + r415 + univapay r149/r154. ⚠ Spec R10: cancelCycle() của cron KHÔNG gọi API hủy "
            "subscription bên cổng → bước 5 và 6 là điểm kiểm QUAN TRỌNG, xem MT-17."),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Bill LẠI THÀNH CÔNG sau khi đã lỗi → reset bộ đếm lỗi, gia hạn kỳ",
       JOB + "\n- Hợp đồng của F1 đã bill lỗi 1-2 lần, sau đó thẻ được kích hoạt lại (hoặc user đổi thẻ)",
       "1. Chạy job bill định kỳ\n2. Mở 注文詳細 đọc trạng thái + 次回決済予定日 + 決済履歴\n"
       "3. Tạo tình huống bill lỗi lại 1 lần → chạy job → kiểm tra hợp đồng KHÔNG bị hủy ngay",
       "Đã lỗi 2 lần → bill thành công → lỗi lại 1 lần",
       "- Bill thành công: hợp đồng thoát trạng thái 延滞, 次回決済予定日 được gia hạn\n"
       "- Bộ đếm lỗi được RESET → lần lỗi kế tiếp chỉ tính là lần 1, hợp đồng KHÔNG bị auto-cancel",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r139「count_bill_error = NULL」. Spec BR-07."),

    tc("Job bill định kỳ", "DATA-001", "Abnormal",
       "★ Admin ĐỔI GIÁ sản phẩm sau khi khách đã đăng ký → kỳ tiếp bill theo GIÁ NÀO?",
       JOB + "\n- F1 đăng ký hợp đồng khi giá là 3.000円/kỳ, đã bill 1 kỳ 3.000円",
       "1. Admin đổi giá SP-C thành 5.000円 → 保存\n2. Đợi/chạy job bill kỳ tiếp\n"
       "3. Mở 注文詳細 của F1: đọc số tiền dòng mới, cột 販売価格 của hợp đồng\n"
       "4. Đối chiếu dashboard cổng thanh toán (số tiền thực trừ)\n"
       "5. Đọc tin nhắn action F1 nhận được (nếu action có chèn mã số tiền)\n"
       "6. Cho friend F2 đăng ký mới → xem F2 bị bill giá nào",
       "Giá cũ 3.000円 → giá mới 5.000円",
       "- Ghi lại số tiền THỰC TRỪ ở cả 3 nơi: 決済履歴 · cổng thanh toán · tin nhắn action\n"
       "- F2 (đăng ký mới): bill 5.000円\n"
       "- ⚠ Nếu F1 bị trừ 5.000円 mà không được thông báo → rủi ro nghiệp vụ NGHIÊM TRỌNG, raise ngay",
       env="PRODUCTION",
       note="★ MÂU THUẪN CORPUS ↔ SPEC (MT-03): r346 (Stripe) ghi「bill theo giá mới」; r362 (UnivaPay) ghi "
            "「univapay không update được giá bill => bill theo giá cũ; các user mua mới thì bill theo giá mới」. "
            "Spec BR-05 + R1 nói CẢ 2 cron đều dùng s_items.amount HIỆN TẠI. Expected để mở — CẦN LEADER QUYẾT."),

    tc("Job bill định kỳ", "ENV-001", "Normal",
       "Bot HẾT HẠN hợp đồng LME → job bill định kỳ của item còn chạy hay dừng (Stripe vs UnivaPay)",
       "- Bot B có plan_type = 1, expired_date đã hết hạn\n"
       "- Bot B có 2 hợp đồng 継続 tới hạn bill: 1 dùng Stripe, 1 dùng UnivaPay",
       "1. Sửa expired_date của bot B cho hết hạn (quá 7 ngày)\n2. Sửa c_expired_date của cả 2 hợp đồng cho tới hạn\n"
       "3. Chạy job bill định kỳ\n4. Mở 注文詳細 của 2 hợp đồng: đếm dòng mới trong 決済履歴\n"
       "5. Đối chiếu dashboard của cả Stripe và UnivaPay xem có giao dịch mới không",
       "Bot hết hạn > 7 ngày · 1 hợp đồng Stripe · 1 hợp đồng UnivaPay",
       "- Ghi lại kết quả THẬT cho TỪNG cổng\n"
       "- Theo corpus (Sheet2 tab Item): cả 2 cổng đều KHÔNG bill nữa\n"
       "- Theo spec R3: J1 (Stripe) bỏ qua bot hết hạn (có 7 ngày ân hạn), nhưng J2 (UnivaPay) "
       "bộ lọc ĐÃ COMMENT OUT → vẫn tiếp tục trừ tiền khách\n"
       "- Nếu UnivaPay vẫn trừ tiền → BLOCKER (rủi ro thanh toán + pháp lý), raise ngay",
       env="PRODUCTION",
       note="★ MÂU THUẪN CORPUS ↔ SPEC (MT-23): corpus Sheet2 r5-r6 ghi「Bot hết hạn | uni: job ko bill nữa OK | "
            "stripe: job ko bill nữa OK」và Info tab 12/2023「Bot hết hạn thì sẽ ko bill chu kỳ job hàng tháng」. "
            "Spec R3 nói ngược lại cho UnivaPay. Corpus 12/2023 CŨ hơn spec 08/2026 → CẦN LEADER QUYẾT."),

    tc("Job bill định kỳ", "COMPAT-001", "Normal",
       "★ Update spec — UnivaPay chuyển từ SUBSCRIPTION sang bill bằng JOB như Stripe",
       JOB + "\n- SP-C dùng cổng UnivaPay",
       "1. F1 mua mới SP-C\n2. Mở dashboard UnivaPay: kiểm tra có tạo subscription (定期課金) hay không\n"
       "3. Sửa c_expired_date cho tới hạn → chạy job bill định kỳ\n"
       "4. Kiểm tra dashboard UnivaPay: giao dịch kỳ mới do LME chủ động tạo hay do UnivaPay tự sinh",
       "SP-C cổng UnivaPay",
       "- Ghi lại kết quả THẬT: có tồn tại subscription trên UnivaPay không\n"
       "- Theo bản ghi MỚI NHẤT của corpus (r388):「bill tiền chu kỳ bằng univapay chuyển qua bill job như "
       "stripe (không dùng subcription nữa)」→ KHÔNG có subscription, job LME chủ động bill từng kỳ",
       env="PRODUCTION",
       note="★ MÂU THUẪN NIÊN ĐẠI (MT-13): r314-r323 mô tả cơ chế subscription (period=monthly/weekly/...), "
            "r347-r362 mô tả「logic bill mới theo tự động bill của univapay」; nhưng r388 tuyên bố ĐÃ BỎ subscription. "
            "Spec §7.2-7.3 khẳng định J2 chủ động bill (billItemUnivapay + metadata.module='sales_job') → "
            "KHỚP với r388. Các TC subscription cũ đã bị loại, ghi ở bảng mâu thuẫn."),

    tc("Job bill định kỳ", "JOB-002", "Normal",
       "Hủy hợp đồng từ phía CỔNG THANH TOÁN → LME nhận callback và cập nhật trạng thái",
       JOB + "\n- Hợp đồng của F1 đang 継続中, cổng UnivaPay",
       "1. Vào dashboard UnivaPay hủy recurring token / subscription của F1\n"
       "2. Chờ callback về LME\n3. Mở 販売履歴 継続 đọc trạng thái hợp đồng\n"
       "4. Chạy job bill ở kỳ tới, kiểm tra F1 có bị trừ tiền không",
       "Hủy từ phía UnivaPay",
       "- Hợp đồng bên LME chuyển trạng thái「キャンセル済」\n"
       "- Kỳ tới job KHÔNG bill, F1 không bị trừ tiền\n- F1 nhận action「解約時」",
       env="PRODUCTION",
       note="Nguồn: r361「Có call back về và update status cycle sang đã cancel」+ r368 mục 4."),

    tc("Job bill định kỳ", "JOB-001", "Abnormal",
       "Job đang bill dở → trạng thái trung gian không cho thao tác, đồng thời không bill trùng",
       JOB + "\n- Hợp đồng của F1 tới hạn, cổng thanh toán trả kết quả chậm",
       "1. Chạy job bill định kỳ\n2. NGAY khi job vừa bắt đầu bill: mở 注文詳細 đọc trạng thái\n"
       "3. Thử bấm hủy hợp đồng ở màn admin\n4. F1 thử mở link đổi thẻ / hủy phía LINE\n"
       "5. Chạy lại job bill lần nữa trong lúc kỳ này chưa có kết quả",
       "Hợp đồng đang chờ kết quả bill của job",
       "- Trạng thái kỳ hiển thị「支払い処理中」, hợp đồng vẫn「継続中」\n"
       "- Admin KHÔNG hủy được hợp đồng (bị bỏ qua)\n"
       "- F1 mở link đổi thẻ/hủy → lỗi「決済処理を行っていますので、操作できません。」\n"
       "- Chạy job lần 2: KHÔNG bill thêm lần nữa (không trừ tiền 2 lần)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r114/r118 (không update expired_date, không action khi đang bill) "
            "+ r166-r168 + ListBug r14「case bill tiền đang đợi xử lý (status_webhook =0,3,4) => khi job chạy "
            "vẫn bị bill tiếp | Fixed | OK」. regression"),

    tc("Job bill định kỳ", "JOB-001", "Normal",
       "Job bill xong 15 phút vẫn chưa có kết quả → chuyển sang cho job quét kết quả xử lý",
       JOB + "\n- Hợp đồng tới hạn, cổng thanh toán không trả kết quả trong 15 phút",
       "1. Chạy job bill định kỳ\n2. Chờ quá 15 phút không có kết quả\n"
       "3. Chạy job quét kết quả bill\n4. Mở 注文詳細 đọc trạng thái + 決済履歴 + chat 1:1 F1",
       "Không có kết quả trong 15 phút",
       "- Job quét kết quả tra được trạng thái thật từ cổng thanh toán\n"
       "- Nếu thật là success: gia hạn kỳ, gửi action + notify + tin LINE 決済が完了しました\n"
       "- Nếu thật là fail: tăng đếm lỗi, gửi action lỗi + notify + tin LINE báo lỗi",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r117 / r121 / r125 / r129 / r133 / r137 / r141 / r145 / r150 / r155 "
            "(TC gốc chỉ có tiêu đề「check 15p chưa có kết quả bill => job chạy check kết quả bill」— "
            "kết quả mong đợi do AI tổng hợp từ các dòng lân cận, CẦN LEADER XÁC NHẬN)."),

    # ══════ 23. Job cứu đơn treo & quét kết quả ══════
    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Normal",
       "Đơn treo quá 15 phút (単品) → job quét tra kết quả thật và cập nhật đúng",
       "- Bot A có đơn 単品 UnivaPay của F1 ở trạng thái「決済処理中」đã quá 15 phút\n"
       "- Trên cổng thanh toán giao dịch thật ở trạng thái thành công",
       "1. Chạy job cứu đơn treo / quét kết quả\n2. Mở 販売履歴 đọc trạng thái đơn\n"
       "3. Kiểm tra chat 1:1 F1 + notify admin\n4. Chạy job lần 2 → kiểm tra không xử lý lặp",
       "Đơn treo > 15 phút, kết quả thật = success",
       "- Đơn chuyển「決済成功」\n- F1 nhận action「申込完了時」+ tin LINE 決済が完了しました\n"
       "- Admin nhận notify が購入されました\n"
       "- Chạy job lần 2: KHÔNG gửi lại action/notify/tin nhắn (idempotent)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r11 + r23 + r205. Spec §7.2 J4 recover:payment_univapay_timeout "
            "chạy mỗi 5 phút, quét đơn treo > 15 phút. Bước 4 (idempotent) là suy luận của AI từ spec §7.4 "
            "「Bảo vệ idempotency của callbackJob()」— CẦN LEADER XÁC NHẬN."),

    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Normal",
       "Đơn treo quá 15 phút, kết quả thật là FAIL → xóa đơn + gửi tin báo lỗi",
       "- Bot A có đơn 単品 của F1 treo quá 15 phút\n- Trên cổng thanh toán giao dịch thật ở trạng thái failed",
       "1. Chạy job quét kết quả\n2. Mở 販売履歴\n3. Kiểm tra chat 1:1 F1 + notify admin",
       "Đơn treo > 15 phút, kết quả thật = fail",
       "- Đơn bị xóa khỏi 販売履歴\n- KHÔNG gửi action「申込完了時」\n"
       "- Admin nhận notify 決済に失敗しました\n- F1 nhận tin LINE báo thanh toán thất bại",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r12 + r24 + r206. Cách tạo data theo tester: bill fail → tạo 1 "
            "bản ghi fake trong s_order_history với order id vừa bị xóa → sửa update_at cho quá 15 phút."),

    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Normal",
       "Đơn treo của HỢP ĐỒNG 継続 (mua mới) → job quét cập nhật cả bản ghi hợp đồng lẫn kỳ",
       "- Bot A có hợp đồng 継続 của F1 vừa mua mới, đang treo quá 15 phút\n"
       "- Kết quả thật trên cổng thanh toán = success",
       "1. Chạy job quét kết quả\n2. Mở 販売履歴 継続 đọc trạng thái hợp đồng\n"
       "3. Mở 注文詳細 đọc bảng 決済履歴\n4. Kiểm tra chat 1:1 F1",
       "Hợp đồng mua mới treo > 15 phút",
       "- Hợp đồng chuyển「継続中」hoặc「トライアル中」đúng theo setting sản phẩm\n"
       "- 決済履歴 có 1 dòng thành công đúng số tiền\n"
       "- F1 nhận action「申込完了時」+「初回決済時」+ tin LINE 決済が完了しました",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r41 / r52 / r220 + r322."),

    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Normal",
       "Đơn treo của luồng ĐỔI THẺ → job quét cập nhật đúng thông tin thẻ và hạn kỳ",
       "- F1 vừa đổi thẻ có bill lại, giao dịch treo quá 15 phút\n- Kết quả thật = success",
       "1. Chạy job quét kết quả\n2. Mở 注文詳細 đọc thông tin thẻ + 次回決済予定日 + 決済履歴\n"
       "3. Kiểm tra chat 1:1 F1",
       "Đổi thẻ treo > 15 phút",
       "- Thông tin thẻ = thẻ mới\n- 次回決済予定日 được gia hạn\n- Đếm lỗi được reset\n"
       "- 決済履歴 có thêm 1 dòng thành công\n- F1 nhận action bill tương ứng",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền univapay r101-r102 / r112 + r325."),

    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Abnormal",
       "Job quét chạy khi KHÔNG có đơn treo nào → chạy xong không lỗi, không tác động dữ liệu",
       "- Bot A không có đơn nào ở trạng thái treo",
       "1. Ghi lại số đơn và trạng thái hiện tại ở 販売履歴\n2. Chạy job quét kết quả\n"
       "3. Đọc lại 販売履歴 và log job",
       "0 đơn treo",
       "- Job chạy xong không lỗi\n- Không có đơn nào bị đổi trạng thái\n- Không gửi action/notify nào",
       env="PRODUCTION",
       note="Suy luận của AI (empty state của job). Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN."),

    tc("Job cứu đơn treo & quét kết quả", "JOB-002", "Abnormal",
       "Job quét gặp lỗi ở đơn của tính năng khác (salon/lesson/event) → KHÔNG chặn phần xử lý item",
       "- Có đồng thời: 1 đơn treo của bill item và 1 booking treo của salon/lesson/event\n"
       "- Tạo tình huống lỗi ở phần booking (VD dữ liệu booking hỏng)",
       "1. Chạy job cứu đơn treo\n2. Kiểm tra đơn item có được xử lý không\n3. Đọc log job",
       "1 đơn item treo + 1 booking treo bị lỗi",
       "- Đơn của bill item VẪN được xử lý đúng dù phần booking lỗi\n"
       "- Log ghi nhận lỗi của phần booking",
       env="PRODUCTION",
       note="Suy luận của AI từ spec R29「getOrderTimeout() đứng CUỐI RecoverPaymentUnivapayTimeout::handle() và "
            "KHÔNG có try/catch → lỗi ở lesson/salon/event CHẶN LUÔN phần sales」. Corpus KHÔNG có TC. "
            "Nếu FAIL thì đây là rủi ro vận hành nghiêm trọng — xem MT-24."),

    # ══════ 24. Action & notify theo sự kiện ══════
    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action「トライアル」gửi trước ngày hết trial đúng N ngày",
       "- SP-C có trial, gắn action ở slot「トライアル」với「終了の 1 日前」\n"
       "- F1 có hợp đồng đang トライアル中, hết trial vào ngày 15/01",
       "1. Đặt ngày hệ thống / chờ tới ngày 14/01\n2. Chạy job gửi action trial\n"
       "3. Kiểm tra chat 1:1 của F1 ngày 14/01 và ngày 15/01",
       "Hết trial 15/01, setting gửi trước 1 ngày",
       "- Ngày 14/01: F1 NHẬN action của slot「トライアル」\n"
       "- Ngày 15/01: KHÔNG gửi lại action này",
       env="PRODUCTION",
       note="Nguồn: r364「Ví dụ: ngày hết hạn trial là 15/01/2023, setting gửi trước 1 ngày => ngày 14/01/2023 "
            "gửi action cho user」+ r410. Spec §7.2 J2 phụ trách việc này cho CẢ 2 cổng."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action「初回決済時」chỉ bắn ở kỳ bill ĐẦU TIÊN",
       "- SP-C gắn action ở slot「初回決済時」\n- F1 mua mới SP-C (không trial, có bill kỳ đầu)",
       "1. F1 mua thành công → kiểm tra chat 1:1\n2. Chạy job bill kỳ 2 → kiểm tra chat 1:1\n"
       "3. Chạy job bill kỳ 3 → kiểm tra chat 1:1",
       "3 kỳ bill liên tiếp",
       "- Kỳ 1: F1 nhận action「初回決済時」\n- Kỳ 2 và 3: KHÔNG nhận action này nữa",
       env="PRODUCTION",
       note="Nguồn: r329「gửi action bill lần 1」+ r347 + Improve bill tiền univapay r115."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action「2回目以降決済時」bắn từ kỳ 2 trở đi",
       "- SP-C gắn action ở slot「2回目以降決済時」, 稼働回数 =「何度でも」\n- F1 có hợp đồng đang chạy",
       "1. Chạy job bill kỳ 2 → kiểm tra chat 1:1\n2. Chạy job bill kỳ 3 → kiểm tra chat 1:1\n"
       "3. Chạy job bill kỳ 4 → kiểm tra chat 1:1",
       "Kỳ 2, 3, 4",
       "- Cả 3 kỳ F1 đều nhận action「2回目以降決済時」",
       env="PRODUCTION",
       note="Nguồn: r365 + r411. ⚠ MÂU THUẪN: r366 ghi「khi bill các lần tiếp theo (sau lần 2) => không action」"
            "— trái với tên slot và với r365. Xem MT-25."),

    tc("Action & notify theo sự kiện", "MSG-001", "Abnormal",
       "★ Action「2回目以降決済時」ở kỳ 3 trở đi CÓ bắn không?",
       "- SP-C gắn action ở slot「2回目以降決済時」với 稼働回数 =「何度でも」\n- F1 có hợp đồng đang chạy",
       "1. Chạy job bill kỳ 2 → ghi nhận có/không action\n2. Chạy job bill kỳ 3 → ghi nhận\n"
       "3. Chạy job bill kỳ 4 → ghi nhận\n4. Lặp lại toàn bộ với 稼働回数 =「1度のみ」",
       "Kỳ 2 / 3 / 4 × 2 setting 稼働回数",
       "- Ghi lại kết quả THẬT cho từng kỳ và từng setting 稼働回数\n"
       "- Nếu 稼働回数「何度でも」mà kỳ 3-4 không bắn → mâu thuẫn với ý nghĩa của setting, cần raise",
       env="PRODUCTION",
       note="★ MÂU THUẪN TRONG CORPUS (MT-25): r365「action khi bill lần 2 => gửi action bill lần 2 cho user nếu có」"
            "vs r366「khi bill các lần tiếp theo (sau lần 2) => không action」. Spec Field Matrix #38 nói 稼働回数 "
            "quyết định (1度のみ vs 何度でも). Expected để mở — CẦN LEADER QUYẾT."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action「決済エラー発生時」bắn khi bill lỗi mà chưa bị hủy hợp đồng",
       "- SP-C gắn action ở slot「決済エラー発生時」, auto_cancel = 0\n- F1 có hợp đồng, thẻ vô hiệu",
       "1. Chạy job bill → bill lỗi lần 1 → kiểm tra chat 1:1\n"
       "2. Chạy job bill → bill lỗi lần 2 → kiểm tra chat 1:1",
       "auto_cancel = 0, lỗi 2 lần",
       "- Cả 2 lần lỗi F1 đều nhận action「決済エラー発生時」\n- Hợp đồng chưa bị hủy",
       env="PRODUCTION",
       note="Nguồn: r367 + r412."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action「解約時」bắn ở CẢ 4 nguồn hủy",
       "- SP-C gắn action ở slot「解約時」\n- Chuẩn bị 4 hợp đồng của 4 friend khác nhau",
       "1. Hợp đồng 1: bill lỗi 3 lần + auto_cancel = 1 → chạy job\n"
       "2. Hợp đồng 2: friend tự bấm hủy ở link 解約\n3. Hợp đồng 3: admin bấm hủy ở màn 注文詳細\n"
       "4. Hợp đồng 4: hủy từ dashboard cổng thanh toán\n5. Kiểm tra chat 1:1 của cả 4 friend",
       "4 nguồn hủy khác nhau",
       "- Cả 4 friend đều nhận action「解約時」\n- Cả 4 hợp đồng đều chuyển「キャンセル済」",
       env="PRODUCTION",
       note="Nguồn: r368 (liệt kê đủ 4 nguồn) + r413-r415. 4 nguồn cùng 1 kết quả → giữ chung 1 TC. "
            "⚠ Ngoại lệ theo spec §2.5: khi admin hủy có tùy chọn KHÔNG chạy action — xem TC riêng ở "
            "nhóm『Hoàn tiền & hủy phía admin』."),

    tc("Action & notify theo sự kiện", "NOTI-MAIL-001", "Normal",
       "Notify phía admin tách riêng theo 単品 và 継続, đủ 5 sự kiện",
       "- Bot A đã bật notify cho tính năng bán hàng\n- Có sẵn SP 単品 và SP-C 継続",
       "1. Mua SP 単品 thành công → kiểm tra notify\n2. Mua SP 単品 thất bại → kiểm tra notify\n"
       "3. Mua SP-C 継続 thành công → kiểm tra notify\n4. Mua SP-C thất bại → kiểm tra notify\n"
       "5. Hủy hợp đồng SP-C → kiểm tra notify\n6. Job bill định kỳ thành công → kiểm tra notify\n"
       "7. Job bill định kỳ lỗi → kiểm tra notify",
       "7 sự kiện như bước 1-7",
       "- Mỗi sự kiện sinh đúng 1 notify, nội dung phân biệt được 単品 hay 継続\n"
       "- Không có sự kiện nào bị thiếu notify",
       env="PRODUCTION",
       note="Nguồn: r381-r387「khi mua hàng các notify của tính năng product sẽ chia thành bill 1 lần và bill "
            "nhiều lần」(r382/r384 chưa được đánh dấu đã test). ⚠ Spec R36: service push notify Spring Boot "
            "MẶC ĐỊNH TẮT → notify có thể tồn đọng, xem MT-26."),

    tc("Action & notify theo sự kiện", "NOTI-MAIL-001", "Abnormal",
       "Bug #26850 — mua THẤT BẠI thì KHÔNG được gửi action mua thành công",
       "- SP 単品 và SP-C 継続 đều gắn action ở slot「申込完了時」\n- SP-C gắn thêm action「決済エラー発生時」",
       "1. F1 mua SP 単品 thất bại (thẻ fail) → kiểm tra chat 1:1\n"
       "2. F1 mua SP-C 継続 thất bại → kiểm tra chat 1:1\n"
       "3. Lặp lại cả 2 với cổng UnivaPay",
       "Thẻ fail, cả Stripe và UnivaPay",
       "- 単品 mua fail: KHÔNG gửi action nào (単品 không có slot action bill lỗi)\n"
       "- 継続 mua fail: KHÔNG gửi action「申込完了時」; action「決済エラー発生時」cũng KHÔNG gửi ở luồng MUA MỚI\n"
       "- Kết quả giống nhau ở cả 2 cổng",
       env="PRODUCTION",
       note="Nguồn: test fix bug r49 / r51 / r55 / r57 (Bug #26850:「Đã thanh toán success nhưng lúc 9h30 8/10 có "
            "msg về lỗi thanh toán cho item được gửi đến friend => sửa lại case bill lỗi khi mua thì không action」). "
            "regression. ⚠ Đối chiếu: Improve bill tiền stripe r17 lại ghi「send action case bill fail」khi mua mới "
            "継続 thất bại → xem MT-27."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Bug #26568 — mã chèn số tiền trong action lấy đúng GIÁ ĐÃ BILL (không phải 0円)",
       "- SP-C có trial với giá trial = 0円, đã gắn action ở các slot bill với text chứa mã số tiền\n"
       "- F1 mua SP-C (trial 0円) rồi để job bill kỳ tiếp",
       "1. F1 mua → đọc tin action nhận được (kỳ trial 0円)\n"
       "2. Chạy job bill kỳ tiếp (giá thật 3.000円) → đọc tin action nhận được\n"
       "3. Chạy job bill kỳ sau nữa → đọc tin action\n"
       "4. Đối chiếu từng số tiền với bảng 決済履歴",
       "trial 0円 → kỳ 2: 3.000円 → kỳ 3: 3.000円",
       "- Tin ở kỳ trial: hiển thị 0円 (đúng số đã bill)\n"
       "- Tin ở kỳ 2 và 3: hiển thị 3.000円 — KHÔNG hiện 0円\n"
       "- Số tiền trong tin khớp với dòng tương ứng trong 決済履歴",
       env="PRODUCTION",
       note="Nguồn: test fix bug r2-r14 (Bug #26568:「Item chu kỳ: Đã setting mã code giá tiền trong action khi "
            "thanh toán từ lần thứ 2 trở đi nhưng bị hiển thị 0 yên trong chat 11」). regression"),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action khi ADMIN hủy / USER hủy — mã số tiền lấy đúng giá đã bill ở mọi pattern trial",
       "- 4 hợp đồng ứng với 4 pattern: trial 0円 · trial có giá · không trial có giá kỳ đầu · không trial không giá kỳ đầu\n"
       "- SP-C gắn action「解約時」có chèn mã số tiền",
       "1. Admin hủy lần lượt 4 hợp đồng → đọc 4 tin action\n"
       "2. Lặp lại với 4 hợp đồng khác, để USER tự hủy → đọc 4 tin action\n"
       "3. Đối chiếu từng số tiền với 決済履歴 của hợp đồng tương ứng",
       "4 pattern × 2 nguồn hủy = 8 lượt",
       "- Cả 8 tin đều hiển thị đúng số tiền ĐÃ BILL của hợp đồng đó\n- Không có tin nào hiện 0円 sai",
       env="PRODUCTION",
       note="Nguồn: test fix bug r15-r22 (Bug #26568). 8 lượt cùng 1 loại kết quả → giữ chung 1 TC."),

    tc("Action & notify theo sự kiện", "MSG-001", "Normal",
       "Action bill LỖI — mã số tiền để trống (không hiện giá trị sai)",
       "- SP-C gắn action「決済エラー発生時」có chèn mã số tiền",
       "1. Tạo tình huống bill lỗi khi MUA MỚI → đọc tin action (nếu có)\n"
       "2. Tạo tình huống job bill lỗi → đọc tin action",
       "2 tình huống bill lỗi",
       "- Tin action bill lỗi: phần mã số tiền để TRỐNG (không có value)\n- Không hiện số tiền sai lệch",
       env="PRODUCTION",
       note="Nguồn: test fix bug r23-r24「send action bill lỗi, giá ko có value」."),

    tc("Action & notify theo sự kiện", "SYNC-APP-001", "Normal",
       "Tự động điền email/tên khi tạo khách hàng bên cổng thanh toán",
       "- SP có mục 友だち情報「お名前」và「メールアドレス」\n- Bot A liên kết cả Stripe và UnivaPay",
       "1. F1 mua sản phẩm UnivaPay, nhập tên「山田太郎」+ mail「t@example.com」\n"
       "2. Mở dashboard UnivaPay tra khách hàng tương ứng\n"
       "3. Lặp lại với sản phẩm Stripe → tra customer bên Stripe\n"
       "4. Chạy job bill kỳ tiếp của hợp đồng Stripe → tra lại customer",
       "Tên「山田太郎」· mail「t@example.com」",
       "- UnivaPay: email của giao dịch = mail user nhập ở form friend info\n"
       "- Stripe: customer có cả name và email đúng như user nhập\n"
       "- Sau job bill kỳ tiếp: thông tin customer Stripe vẫn đúng",
       env="PRODUCTION",
       note="Nguồn: r374-r376."),

    # ══════ 25. Job monitor bill tiền ══════
    tc("Job monitor bill tiền", "JOB-003", "Normal",
       "Monitor — có lịch sử bill trong DB VÀ có giao dịch trên cổng → KHÔNG notify",
       "- Job monitor bill tiền chạy 1 lần/ngày\n- Có 1 hợp đồng item vừa bill thành công qua UnivaPay",
       "1. Đảm bảo lịch sử bill trong hệ thống và giao dịch trên UnivaPay đều tồn tại và khớp\n"
       "2. Chạy job monitor\n3. Kiểm tra kênh nhận cảnh báo",
       "1 giao dịch khớp 2 phía",
       "- KHÔNG phát sinh cảnh báo nào",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r67 (khối「Check bill tiền item」r66-r91, 11/2025)."),

    tc("Job monitor bill tiền", "JOB-003", "Abnormal",
       "Monitor — có lịch sử bill trong DB nhưng KHÔNG có giao dịch trên cổng → CÓ notify",
       "- Có 1 lịch sử bill item với charge id không tồn tại trên cổng thanh toán (fake data)",
       "1. Tạo thêm 1 lịch sử bill cho item với charge id không tồn tại trên UnivaPay\n"
       "2. Chạy job monitor\n3. Kiểm tra kênh nhận cảnh báo\n4. Lặp lại với cổng Stripe",
       "charge id không tồn tại trên cổng",
       "- CÓ cảnh báo được gửi\n- Cảnh báo nêu được id bản ghi bất thường\n"
       "- Kết quả giống nhau ở cả UnivaPay và Stripe",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r68 + r79."),

    tc("Job monitor bill tiền", "JOB-003", "Abnormal",
       "Monitor — trạng thái bill trong DB KHÁC với trạng thái trên cổng → CÓ notify",
       "- Có các cặp dữ liệu lệch trạng thái giữa hệ thống và cổng thanh toán",
       "1. Tạo cặp: DB ghi thành công / cổng ghi thất bại → chạy job monitor\n"
       "2. Tạo cặp: DB ghi thất bại / cổng ghi thành công → chạy job monitor\n"
       "3. Tạo cặp khớp nhau (cùng thành công, cùng thất bại) → chạy job monitor\n"
       "4. Lặp lại cho cả UnivaPay và Stripe",
       "4 tổ hợp trạng thái × 2 cổng",
       "- 2 cặp LỆCH: CÓ cảnh báo\n- 2 cặp KHỚP: KHÔNG cảnh báo\n"
       "- Kết quả giống nhau ở cả 2 cổng",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r69-r72 + r80-r83."),

    tc("Job monitor bill tiền", "JOB-003", "Normal",
       "Monitor — đơn ĐÃ HOÀN TIỀN: chỉ cảnh báo khi cổng báo thất bại",
       "- Có 3 đơn item ở trạng thái đã hoàn tiền trong hệ thống",
       "1. Đơn 1: trên cổng vẫn là giao dịch thành công → chạy job monitor\n"
       "2. Đơn 2: trên cổng ở trạng thái đã hoàn tiền → chạy job monitor\n"
       "3. Đơn 3: trên cổng ở trạng thái thất bại → chạy job monitor",
       "3 trạng thái phía cổng: success · refunded · failed",
       "- Đơn 1 và 2: KHÔNG cảnh báo\n- Đơn 3: CÓ cảnh báo",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r73-r75 + r84-r86."),

    tc("Job monitor bill tiền", "JOB-003", "Abnormal",
       "Monitor — SỐ TIỀN bill trên cổng khác số tiền trong lịch sử → CÓ notify",
       "- Có 2 đơn item: 1 đơn số tiền khớp, 1 đơn số tiền lệch giữa hệ thống và cổng",
       "1. Chạy job monitor\n2. Kiểm tra kênh nhận cảnh báo\n3. Lặp lại cho cả UnivaPay và Stripe",
       "1 đơn khớp số tiền · 1 đơn lệch số tiền",
       "- Đơn khớp: KHÔNG cảnh báo\n- Đơn lệch: CÓ cảnh báo\n- Giống nhau ở cả 2 cổng",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r76-r77 + r87-r88."),

    tc("Job monitor bill tiền", "JOB-003", "Abnormal",
       "Monitor — item bill thành công nhưng NGÀY GIA HẠN sai → CÓ notify",
       "- Có 2 hợp đồng item vừa bill thành công",
       "1. Hợp đồng 1: giữ nguyên ngày gia hạn đúng → chạy job monitor\n"
       "2. Hợp đồng 2: sửa tay 次回決済予定日 cho lệch so với chu kỳ → chạy job monitor",
       "1 hợp đồng ngày đúng · 1 hợp đồng ngày sai",
       "- Hợp đồng 1: KHÔNG cảnh báo\n- Hợp đồng 2: CÓ cảnh báo",
       env="PRODUCTION",
       note="Nguồn: Monitor bill tiền r89-r90 (+ r6-r8 khối cũ). ⚠ Ngưỡng lệch ngày: khối「Check bill tiền bot」"
            "r61-r64 quy định lệch > 7 ngày mới cảnh báo; khối ITEM KHÔNG ghi ngưỡng → xem MT-28."),

    tc("Job monitor bill tiền", "JOB-003", "Normal",
       "Monitor — item bill FAIL thì KHÔNG cảnh báo nữa (đổi so với bản 2023)",
       "- Có 1 hợp đồng item vừa bill thất bại",
       "1. Chạy job monitor\n2. Kiểm tra kênh nhận cảnh báo",
       "1 hợp đồng bill fail",
       "- KHÔNG phát sinh cảnh báo cho case bill fail",
       env="PRODUCTION",
       note="★ MÂU THUẪN NIÊN ĐẠI (MT-29): Monitor bill tiền r6 (bản 2023) ghi「case bill fail => có notify」; "
            "r91 (bản 11/2025) ghi「Không notify case bill fail nữa」. Ưu tiên TC MỚI NHẤT (11/2025)."),
]
