# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 29-32: job bill định kỳ, job hủy hợp đồng, quy tắc ngày bill.

Nguồn chính: TCsLine_Bill tiền_Improve2025 → tab「Màn hình bill tiền」r444-r548 (job bill + ngày
  expired_date), r573-r618 (job stripe/univapay/transfer/max friend), r629-r647 (Bug tự detect #38298).
Bổ sung: TCsLine_Bill tiền → tab「Cố định ngày bill tiền」(07/2023),
         tab「Change bill tiền theo năm」(12/2023 — phân bổ 12 bản ghi),
         TCsLine_Improve chung / TCsLine_JOB → tab「Monitor bill tiền」khối BOT.

⚠ TOÀN BỘ nhóm này để Môi trường test = PRODUCTION theo RULE-08 (job + bill tiền).
"""
from _common import tc

JOB = ("- Có quyền chạy job job:check_auto_payment_univapay (lịch 06:30 hàng ngày)\n"
       "- Chuẩn bị hợp đồng test có expired_date_contract = ngày chạy job")

S6 = [
    # ═════════════ 29. Job bill định kỳ — thẻ ═════════════
    tc("Job bill định kỳ — thẻ", "JOB-001", "Normal",
       "Job bill thẻ thành công (chỉ có thẻ chính) → cập nhật hợp đồng + 3 loại lịch sử",
       JOB + "\n- Hợp đồng standard tháng, bill card, chỉ có thẻ chính hợp lệ",
       "1. Chạy job\n2. Kiểm tra bot_contracts\n3. Mở màn lịch sử hóa đơn của user\n"
       "4. Mở 操作履歴 của hợp đồng\n5. Kiểm tra giao dịch trên UnivaPay",
       "Hợp đồng standard tháng, thẻ chính hợp lệ",
       "- DB: status=1, status_payment=1, expired_date_contract cộng thêm 1 tháng\n"
       "- Lịch sử hóa đơn user có bản ghi mới\n- 操作履歴 có bản ghi「〇〇プラン　更新（毎月）」\n"
       "- UnivaPay: đúng 1 giao dịch Successful của thẻ chính",
       env="PRODUCTION",
       note="Nguồn: r447, r583. RULE-07: DB + màn hình + lịch sử."),

    tc("Job bill định kỳ — thẻ", "JOB-002", "Normal",
       "Job bill: thẻ chính lỗi → tự động fallback sang thẻ phụ, chỉ tạo 1 lịch sử",
       JOB + "\n- Hợp đồng standard tháng có thẻ chính (lỗi) và thẻ phụ (hợp lệ)",
       "1. Chạy job\n2. Kiểm tra giao dịch trên UnivaPay\n3. Kiểm tra payment_histories\n"
       "4. Kiểm tra bot_contracts",
       "Thẻ chính lỗi, thẻ phụ hợp lệ",
       "- UnivaPay: 1 giao dịch fail của thẻ chính + 1 giao dịch Successful của thẻ phụ\n"
       "- payment_histories: CHỈ 1 bản ghi cho giao dịch thành công\n"
       "- DB: status=1, status_payment=1, expired_date cộng đúng 1 kỳ",
       env="PRODUCTION",
       note="Nguồn: r455, r588, r597 + Bug tự detect #38298 TC06."),

    tc("Job bill định kỳ — thẻ", "JOB-002", "Normal",
       "Thẻ chính bill thành công → KHÔNG charge thẻ phụ",
       JOB + "\n- Hợp đồng có cả thẻ chính và thẻ phụ đều hợp lệ",
       "1. Chạy job\n2. Kiểm tra giao dịch trên UnivaPay của cả 2 thẻ",
       "Thẻ chính và thẻ phụ đều hợp lệ",
       "Chỉ có giao dịch của thẻ chính; thẻ phụ KHÔNG bị charge",
       env="PRODUCTION",
       note="Nguồn: r454, r587 + Bug tự detect #38298 TC05."),

    tc("Job bill định kỳ — thẻ", "JOB-002", "Boundary",
       "Bot chỉ có thẻ phụ (không có thẻ chính) → bill bằng thẻ phụ",
       JOB + "\n- Hợp đồng chỉ đăng ký thẻ phụ, không có thẻ chính",
       "1. Chạy job\n2. Kiểm tra giao dịch UnivaPay và bot_contracts",
       "bot_contracts.univa_last_four_card rỗng, subcard_bot_contracts có bản ghi",
       "Bill được bằng thẻ phụ, hợp đồng gia hạn bình thường",
       env="PRODUCTION",
       note="Nguồn: Bug tự detect #38298 TC09. ⚠ Corpus ghi kèm điều kiện 'nếu hệ thống hỗ trợ' — "
            "hành vi chưa chắc chắn, CẦN LEADER XÁC NHẬN. Xem MT-27."),

    tc("Job bill định kỳ — thẻ", "JOB-003", "Abnormal",
       "Job bill thẻ lỗi lần 1 → hợp đồng chuyển 延滞中, gửi mail báo lỗi thanh toán",
       JOB + "\n- Hợp đồng standard tháng, thẻ chính và thẻ phụ đều bị từ chối",
       "1. Chạy job ngày thứ 1\n2. Đọc status ở màn list\n3. Kiểm tra bot_contracts.status_payment_fail\n"
       "4. Mở hộp thư của admin hợp đồng\n5. Mở 操作履歴",
       "status_payment_fail chuyển 0 → 1",
       "- Màn list hiện「延滞中」\n- DB: status=1, status_payment=2, status_payment_fail=1\n"
       "- Admin nhận mail「L Messageの決済失敗のお知らせ」\n"
       "- 操作履歴 ghi bản ghi 決済エラー (type=20); lịch sử bill FAIL không hiện ở màn user",
       env="PRODUCTION",
       note="Nguồn: r448, r584, r589 + BR-03 (feature-spec.md §5). RULE-06: output cuối là email."),

    tc("Job bill định kỳ — thẻ", "JOB-003", "Normal",
       "Bill lỗi ngày 1, ngày 2 bill lại thành công → hợp đồng về 正常",
       JOB + "\n- Hợp đồng đang 延滞中 với status_payment_fail=1, đã đổi thẻ hợp lệ",
       "1. Chạy job ngày thứ 2\n2. Đọc status ở màn list\n3. Kiểm tra bot_contracts và lịch sử",
       "status_payment_fail = 1 → bill lại thành công",
       "- Màn list về「正常」\n- DB: status_payment=1, status_payment_fail reset, expired_date cộng đúng 1 kỳ\n"
       "- Có bản ghi lịch sử bill thành công",
       env="PRODUCTION",
       note="Nguồn: r449, r457, r585, r594."),

    tc("Job bill định kỳ — thẻ", "JOB-003", "Boundary",
       "Lịch retry theo status_payment_fail: ngày 1 → +2 → +5 → +6 → lần 5 cưỡng chế hủy",
       JOB + "\n- Hợp đồng standard tháng, thẻ luôn bị từ chối",
       "1. Chạy job liên tiếp, mỗi lần ghi lại status_payment_fail và ngày retry tiếp theo\n"
       "2. Theo dõi tới lần thất bại thứ 5\n3. Kiểm tra mail gửi ở lần 1, lần 4 và lần 5\n"
       "4. Kiểm tra trạng thái hợp đồng sau lần 5",
       "Thẻ luôn lỗi, theo dõi đủ 5 lần",
       "- fail=1: retry ngay trong ngày (23:59:59) + gửi mail「決済失敗のお知らせ」\n"
       "- fail=2: retry sau +2 ngày · fail=3: retry sau +5 ngày\n"
       "- fail=4: retry sau +6 ngày + gửi mail「エルメ機能停止前日のご連絡」\n"
       "- fail=5: cưỡng chế hủy (status=3), ẩn richmenu + gửi mail「エルメ機能停止のご連絡」",
       env="PRODUCTION",
       note="Nguồn: BR-03 (feature-spec.md §5) + r450-r453, r578, r586, r591. "
            "⚠ Corpus mô tả theo mốc 'ngày 1/2/3/6/7' còn spec mô tả theo status_payment_fail 1-5 — "
            "2 cách đếm KHÔNG khớp nhau, xem MT-28."),

    tc("Job bill định kỳ — thẻ", "JOB-002", "Normal",
       "Job bill năm bằng thẻ: 1 bản ghi cha + 12 bản ghi phân bổ tháng",
       JOB + "\n- Hợp đồng standard NĂM, bill card, thẻ hợp lệ",
       "1. Chạy job\n2. Đếm bản ghi payment_histories mới của hợp đồng\n"
       "3. Kiểm tra cột parent_month của từng bản ghi\n4. Cộng tay 12 bản ghi con so với bản ghi cha\n"
       "5. Mở màn lịch sử thanh toán của user",
       "Hợp đồng standard năm, tổng 116.424円",
       "- 13 bản ghi mới: 1 bản parent_month=1 (số tiền tổng) + 12 bản parent_month=0 (mỗi bản 1/12)\n"
       "- Tổng 12 bản con = số tiền bản cha\n"
       "- Màn lịch sử user CHỈ hiện bản ghi cha (parent_month=1), không hiện 12 bản phân bổ",
       env="PRODUCTION",
       note="Nguồn: tab「Change bill tiền theo năm」r3-r14 + BR-04, BR-06 (feature-spec.md §5)."),

    tc("Job bill định kỳ — thẻ", "PERF-002", "Boundary",
       "Nhiều bot dùng CHUNG 1 thẻ trong cùng lượt job → tất cả đều bill được, không delay bất thường",
       JOB + "\n- Chuẩn bị 5 hợp đồng dùng chung 1 thẻ chính, cùng đến kỳ bill",
       "1. Chạy job\n2. Đếm số bot bill thành công\n3. Đo thời gian chạy job\n"
       "4. Kiểm tra UnivaPay có lỗi rate limit không",
       "5 hợp đồng dùng chung 1 thẻ",
       "- Cả 5 bot đều được bill thành công\n- Không phát sinh lỗi rate limit từ UnivaPay\n"
       "- Thời gian chạy không kéo dài bất thường do cơ chế sleep chống trùng thẻ",
       env="PRODUCTION",
       note="Nguồn: Bug tự detect #38298 TC02, TC10, TC11 + ghi chú spec: Univapay sleep 330 giây khi "
            "nhiều hợp đồng dùng chung thẻ (feature-spec.md §7). RULE-08: performance → PRODUCTION."),

    tc("Job bill định kỳ — thẻ", "JOB-004", "Abnormal",
       "Hợp đồng hết hạn quá 6 giờ vẫn phải được job bill (không bị bỏ sót)",
       JOB + "\n- Chuẩn bị 4 bot_contract, trong đó có bot đã hết hạn quá 6 giờ trước thời điểm job chạy",
       "1. Chạy job\n2. Đối chiếu danh sách hợp đồng được bill với danh sách hợp đồng đến kỳ\n"
       "3. Kiểm tra riêng hợp đồng hết hạn quá 6 giờ",
       "4 hợp đồng, 1 hợp đồng quá hạn > 6 giờ",
       "Tất cả hợp đồng đến kỳ đều được bill, kể cả hợp đồng hết hạn quá 6 giờ; "
       "không có hợp đồng nào bị bỏ sót",
       env="PRODUCTION",
       note="Nguồn: r629 (Bug tự detect #38298 — tiêu đề bug chính là hiện tượng bỏ sót)."),

    tc("Job bill định kỳ — thẻ", "JOB-004", "Normal",
       "Chạy song song job bill Card và job bill Transfer → không xung đột",
       JOB + "\n- Có bot dùng thẻ và bot dùng chuyển khoản cùng đến kỳ bill",
       "1. Chạy job billing\n2. Kiểm tra kết quả của cả 2 nhóm bot\n"
       "3. Kiểm tra payment_histories có bản ghi trùng không",
       "≥ 2 bot card + ≥ 2 bot transfer cùng kỳ",
       "- Bot card được charge thẻ; bot transfer được tạo bill chuyển khoản\n"
       "- Không nhóm nào bị bỏ sót, không sinh bản ghi trùng",
       env="PRODUCTION",
       note="Nguồn: Bug tự detect #38298 TC16, TC17."),

    tc("Job bill định kỳ — thẻ", "COMPAT-LEGACY-001", "Normal",
       "Job bill Stripe (legacy) vẫn chạy đúng cho hợp đồng còn dùng Stripe",
       JOB + "\n- Có hợp đồng LOA vẫn dùng Stripe (chưa migrate sang UnivaPay)",
       "1. Chạy job\n2. Kiểm tra giao dịch trên Stripe\n3. Kiểm tra bot_contracts, lịch sử bill và 操作履歴\n"
       "4. Lặp lại kịch bản bill lỗi ngày 1 và lỗi tới ngày 7",
       "Hợp đồng dùng Stripe, bill tháng và bill năm",
       "- Bill thành công: hợp đồng cập nhật, có lịch sử bill + lịch sử hoạt động, Stripe có 1 giao dịch\n"
       "- Bill lỗi ngày 1: hợp đồng chuyển overdue, lịch sử bill fail KHÔNG hiện ở màn user\n"
       "- Lỗi tới ngày 7: status=3, cưỡng chế hủy, hôm sau job không bill lại",
       env="PRODUCTION",
       note="Nguồn: r575-r582. ⚠ feature-spec.md §7 ghi AutoPaymentJob (Stripe) 'Đã comment — không chạy' "
            "nhưng Phase 1 của AutoPaymentJobUnivapay lại vẫn charge Stripe; corpus có TC thật cho job Stripe. "
            "Mâu thuẫn — xem MT-29."),

    # ═════════════ 30. Job bill định kỳ — chuyển khoản ═════════════
    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Boundary",
       "Job tạo bill chuyển khoản đúng mốc TRƯỚC 30 ngày, không tạo lại ở các mốc khác",
       JOB + "\n- Hợp đồng standard NĂM, bill transfer",
       "1. Set expired_date − ngày hiện tại = 31 ngày → chạy job → kiểm tra UnivaPay\n"
       "2. Set = 30 ngày → chạy job → kiểm tra\n3. Set = 29 ngày → chạy job → kiểm tra\n"
       "4. Set = 7 ngày → chạy job → kiểm tra\n5. Set = 0 ngày → chạy job → kiểm tra",
       "5 mốc: 31, 30, 29, 7, 0 ngày trước hạn",
       "- 31 ngày: KHÔNG tạo bill chuyển khoản\n"
       "- 30 ngày: TẠO bill chuyển khoản trên UnivaPay với Payment deadline = expired_date + 7 ngày; "
       "phía user hiện 入金待ち (status_payment=5) + thông tin số tài khoản\n"
       "- 29 / 7 / 0 ngày: KHÔNG tạo lại bill chuyển khoản (tránh trùng)",
       env="PRODUCTION",
       note="Nguồn: r477-r481, r601. Đây là quan điểm ưu tiên Cao → đã có đủ Normal (mốc 30), "
            "Abnormal (mốc 31) và Boundary (29/7/0) trong cùng chuỗi thao tác liên tiếp."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Boundary",
       "User chuyển khoản trong khoảng expired_date → expired_date + 7 ngày → hợp đồng gia hạn thành công",
       "- Hợp đồng standard năm bill transfer đang 入金待ち, expired_date = 2026/03/01",
       "1. Chuyển khoản TRƯỚC hạn (28/02) → kiểm tra hợp đồng\n"
       "2. Kịch bản: chuyển đúng ngày hạn (01/03)\n3. +1 ngày (02/03)\n"
       "4. +3 ngày (04/03)\n5. +6 ngày (07/03)\n6. +7 ngày (08/03)",
       "6 mốc chuyển khoản: trước hạn, đúng hạn, +1, +3, +6, +7 ngày",
       "Cả 6 mốc: hợp đồng được gia hạn thành công, status_payment=1, hiển thị được lịch sử bill tiền",
       env="PRODUCTION",
       note="Nguồn: r482-r487 (6 dòng CÙNG expected → gộp, liệt kê đủ 6 mốc ở Dữ liệu test)."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Boundary",
       "Chuyển khoản sau expired_date + 8 ngày → không còn hiệu lực",
       "- Hợp đồng standard năm bill transfer, expired_date = 2026/03/01, đã quá hạn 8 ngày",
       "1. Thử chuyển khoản vào ngày 09/03\n2. Kiểm tra trạng thái hợp đồng và giao dịch UnivaPay",
       "Ngày chuyển khoản = expired_date + 8 ngày",
       "Hợp đồng đã bị cưỡng chế hủy (status=3); khoản chuyển không kích hoạt lại hợp đồng",
       env="PRODUCTION",
       note="Nguồn: r488 (corpus KHÔNG ghi expected cho mốc +8 ngày) + r492. "
            "⚠ Kết quả mong đợi do AI suy luận từ mốc 7 ngày — CẦN LEADER XÁC NHẬN cách xử lý khoản tiền "
            "user đã chuyển sau khi hợp đồng bị hủy. Xem MT-30."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Boundary",
       "Chưa tới hạn 7 ngày mà user không chuyển khoản → CHƯA có callback fail, hợp đồng chưa bị hủy",
       "- Hợp đồng bill transfer đang 入金待ち, expired_date = 2026/03/01",
       "1. Tới ngày 01/03 chưa chuyển khoản → kiểm tra status\n"
       "2. Quá hạn 1 ngày (02/03) → kiểm tra\n3. Quá hạn 6 ngày (07/03) → kiểm tra",
       "3 mốc: đúng hạn, +1, +6 ngày",
       "Cả 3 mốc: chưa có callback fail từ UnivaPay, status=1, bot CHƯA bị hủy hợp đồng",
       env="PRODUCTION",
       note="Nguồn: r489-r491 (3 dòng cùng expected → gộp)."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Boundary",
       "Quá hạn 7 ngày không chuyển khoản → callback fail → cưỡng chế hủy",
       "- Hợp đồng bill transfer đang 入金待ち, expired_date = 2026/03/01, không chuyển khoản",
       "1. Tới ngày 08/03, chờ callback fail từ UnivaPay\n2. Kiểm tra status ở màn list\n"
       "3. Kiểm tra bot_contracts và 操作履歴\n4. Kiểm tra richmenu của bot trên LINE app",
       "Quá hạn đúng 7 ngày",
       "- Có callback fail từ UnivaPay\n- DB: status=3 (cưỡng chế hủy), cancel_by=0\n"
       "- Richmenu của bot bị ẩn trên LINE app\n- 操作履歴 ghi 強制解約",
       env="PRODUCTION",
       note="Nguồn: r492, r603. RULE-06: output cuối là LINE app."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-005", "Abnormal",
       "Quá hạn 7 ngày mà CHƯA nhận được callback fail → job cancel vẫn phải hủy hợp đồng",
       "- Hợp đồng bill transfer quá hạn 8 ngày, UnivaPay chưa gửi callback fail",
       "1. Chạy job job:check_auto_payment_univapay\n2. Kiểm tra trạng thái hợp đồng\n"
       "3. Kiểm tra charge transfer trên UnivaPay\n4. Mở 操作履歴",
       "Quá hạn 8 ngày, chưa có callback",
       "- Job cancel hợp đồng: trạng thái「強制解約」\n"
       "- Charge transfer trên UnivaPay được hủy (Canceled)\n- 操作履歴 có bản ghi hủy",
       env="PRODUCTION",
       note="Nguồn: r604. Đây là nhánh fallback khi webhook không tới — điểm hay lọt bug."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-006", "Normal",
       "Job recover thông tin ngân hàng (5 phút/lần) xử lý request_get_bank_transfer status=0",
       "- Có bản ghi request_get_bank_transfer với status=0\n"
       "- bot_contracts tương ứng có univa_account_number IS NULL",
       "1. Chạy job recover:RecoverUpdateInfoUnivapay (hoặc chờ 5 phút)\n"
       "2. Kiểm tra bot_contracts.univa_account_number\n3. Kiểm tra request_get_bank_transfer.status\n"
       "4. Kiểm tra mail gửi cho admin",
       "1 bản ghi request_get_bank_transfer status=0",
       "- univa_account_number được ghi giá trị từ UnivaPay\n"
       "- request_get_bank_transfer.status chuyển sang trạng thái đã xử lý\n"
       "- Admin nhận mail thông báo số tài khoản (SendMailUpdateAccountNumber)",
       env="PRODUCTION",
       note="Nguồn: feature-spec.md §7 (RecoverUpdateInfoUnivapay) + r323. "
            "Corpus KHÔNG có TC riêng cho job này → TC do AI viết theo spec, CẦN LEADER XÁC NHẬN. Xem MT-21."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-006", "Normal",
       "Job kiểm tra webhook UnivaPay (01:00 hàng ngày) tự sửa cấu hình sai + notify Chatwork",
       "- Có bot có univapay_app_id và univapay_webhook_id\n"
       "- Cố tình sửa sai URL webhook hoặc tắt active",
       "1. Chạy job univapay:check_status_webhook\n2. Kiểm tra cấu hình webhook trên UnivaPay\n"
       "3. Kiểm tra kênh Chatwork nhận thông báo",
       "1 bot có webhook cấu hình sai",
       "- Job phát hiện sai và gọi updateWebhook để sửa lại (URL đúng, active=true, "
       "trigger charge_finished)\n- Có thông báo lỗi gửi vào Chatwork",
       env="PRODUCTION",
       note="Nguồn: feature-spec.md §7 (CheckStatusWebhook). Corpus KHÔNG có TC → AI viết theo spec, "
            "CẦN LEADER XÁC NHẬN. Xem MT-21."),

    tc("Job bill định kỳ — chuyển khoản", "JOB-007", "Normal",
       "Job monitor bill tiền BOT: đối soát giao dịch hợp đồng với UnivaPay/Stripe",
       "- Có ≥ 3 hợp đồng bot vừa bill trong ngày (card và transfer)",
       "1. Chạy job monitor bill tiền (khối「Check bill tiền bot」)\n"
       "2. Đối chiếu danh sách giao dịch trên UnivaPay/Stripe với payment_histories\n"
       "3. Cố tình tạo lệch (xóa 1 bản ghi payment_histories) rồi chạy lại job",
       "3 hợp đồng vừa bill + 1 case cố tình lệch",
       "- Khớp: job không báo lỗi\n"
       "- Có lệch: job phát hiện và cảnh báo đúng giao dịch bị lệch",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung / TCsLine_JOB → tab「Monitor bill tiền」khối『Check bill tiền bot』"
            "r11-r65 (khối này đã bị FA-026 loại khỏi phạm vi vì thuộc FA-031). "
            "⚠ Kho FA-031 chưa đọc chi tiết khối này → TC là khung, cần bổ sung chi tiết. Xem MT-31."),

    # ═════════════ 31. Job hủy hợp đồng & retry ═════════════
    tc("Job hủy hợp đồng & retry", "JOB-001", "Normal",
       "Job Phase 2: gia hạn bot free hết hạn (không bill tiền)",
       JOB + "\n- Bot plan free có expired_date_free_plan = hôm nay",
       "1. Chạy job\n2. Kiểm tra bots.expired_date_free_plan và bot_contracts.expired_date_contract\n"
       "3. Kiểm tra bộ đếm số tin nhắn free của bot\n4. Kiểm tra UnivaPay có charge không\n"
       "5. Kiểm tra payment_detail_aff",
       "Bot free hết hạn hôm nay, có user affiliate",
       "- KHÔNG bill tiền (UnivaPay không có giao dịch)\n"
       "- expired_date của bot + 1 tháng; bộ đếm tin nhắn free được reset\n"
       "- payment_detail_aff có bản ghi amount = 0 (nếu có affiliate)",
       env="PRODUCTION",
       note="Nguồn: r445, r574 + job-spec Phase 2 (feature-spec.md §7)."),

    tc("Job hủy hợp đồng & retry", "JOB-001", "Normal",
       "Job Phase 5: hợp đồng không còn bot_slot → XÓA bot_slots + bot_contracts",
       JOB + "\n- Hợp đồng đến kỳ hủy và KHÔNG còn bot_slot nào gắn với bot",
       "1. Chạy job\n2. Kiểm tra bot_slots và bot_contracts\n3. Kiểm tra màn /basic/point-settings",
       "Hợp đồng không còn bot_slot",
       "- Bản ghi bot_slots và bot_contracts bị XÓA khỏi DB\n"
       "- Dòng biến mất khỏi màn quản lý hợp đồng (không để lại dòng 解約済み)",
       env="PRODUCTION",
       note="Nguồn: job-spec Phase 5 (feature-spec.md §7) + r605. "
            "⚠ Đối lập với case còn bot_slot (giữ lại dòng 解約済み) — điểm dễ nhầm."),

    tc("Job hủy hợp đồng & retry", "JOB-001", "Normal",
       "Job Phase 5: clearDataCancelContract — dữ liệu liên quan bot bị vô hiệu hóa",
       JOB + "\n- Bot có richmenu đang hiển thị, có scenario/broadcast đang chạy\n"
       "- Hợp đồng của bot đến kỳ cưỡng chế hủy",
       "1. Ghi lại trạng thái richmenu / scenario / broadcast trước khi chạy job\n2. Chạy job\n"
       "3. Kiểm tra rich_menus của bot\n4. Kiểm tra trên LINE app: richmenu còn hiện không\n"
       "5. Kiểm tra các tính năng khác của bot",
       "Bot đang có richmenu + scenario hoạt động",
       "- rich_menus: status_line=0, status_link=2, is_updated=2\n"
       "- Trên LINE app: richmenu KHÔNG còn hiển thị\n"
       "- Các dữ liệu liên quan bot bị vô hiệu hóa theo clearDataCancelContract",
       env="PRODUCTION",
       note="Nguồn: job-spec Phase 5 + Bug #32358 (10/10/2025 — hủy tự động không clear richmenu). "
            "RULE-06: output cuối là LINE app. ⚠ Spec §9 [N9] tự nhận side effect rich_menus chưa documented đầy đủ."),

    tc("Job hủy hợp đồng & retry", "REG-002", "Normal",
       "Hủy tự động ở CẢ plan standard/pro VÀ plan enterprise đều clear richmenu",
       JOB + "\n- 1 hợp đồng standard/pro và 1 hợp đồng enterprise, cả 2 đến kỳ cưỡng chế hủy\n"
       "- Cả 2 bot đều có richmenu đang hiển thị",
       "1. Chạy job\n2. Với từng bot: kiểm tra rich_menus và richmenu trên LINE app\n"
       "3. Với enterprise: kiểm tra toàn bộ bot trong các slot",
       "1 hợp đồng standard/pro + 1 hợp đồng EP nhiều slot",
       "- Cả 2 loại hợp đồng: richmenu bị ẩn trên DB và trên LINE app\n"
       "- Với enterprise: TẤT CẢ bot trong các slot đều bị clear richmenu",
       env="PRODUCTION",
       note="Nguồn: r526-r554 (Bug #32358, tab Improve bill tiền 12/2024 — test cả plan standard/pro và EP). "
            "Ghi 'regression'."),

    tc("Job hủy hợp đồng & retry", "INTG-001", "Normal",
       "Bill thành công → INSERT payment_detail_aff cho affiliate",
       JOB + "\n- Hợp đồng của user có affiliate giới thiệu",
       "1. Chạy job bill thành công\n2. Kiểm tra payment_detail_aff\n"
       "3. Mở màn quản lý affiliate phía user và phía admin",
       "User có affiliate",
       "- payment_detail_aff có bản ghi hoa hồng mới cho đúng hợp đồng\n"
       "- Màn quản lý affiliate của user và admin đều hiển thị hoa hồng tương ứng",
       env="PRODUCTION",
       note="Nguồn: r361, r364 + Bug #32681 (03/11/2025 — chương trình giới thiệu chưa được phản ánh) "
            "r555-r630 (tab Improve bill tiền 12/2024). RULE-06: đi tới màn affiliate."),

    tc("Job hủy hợp đồng & retry", "INTG-001", "Abnormal",
       "Bill chuyển khoản CHƯA thanh toán → KHÔNG tạo hoa hồng affiliate",
       JOB + "\n- Hợp đồng bill transfer vừa tạo, chưa chuyển khoản; user có affiliate",
       "1. Kiểm tra payment_detail_aff\n2. Mở màn quản lý affiliate",
       "Hợp đồng transfer chưa thanh toán",
       "- KHÔNG có bản ghi hoa hồng\n- Màn affiliate không hiện khoản hoa hồng nào cho hợp đồng này",
       note="Nguồn: r363, r367, r374, r378."),

    # ═════════════ 32. Ngày bill & expired_date ═════════════
    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Tạo mới bot_contract: ghi datetime_first_payment và tính expired_date",
       "- Chuẩn bị mua mới hợp đồng standard",
       "1. Mua mới hợp đồng bill THÁNG → kiểm tra datetime_payment và expired_date_contract\n"
       "2. Mua mới hợp đồng bill NĂM → kiểm tra tương tự",
       "2 hợp đồng: bill tháng và bill năm, mua ngày 2026/08/24",
       "- Cả 2: bot_contracts.datetime_payment/datetime_first_payment = ngày hiện tại (2026/08/24)\n"
       "- Bill tháng: expired_date_contract = ngày hiện tại + 1 tháng\n"
       "- Bill năm: expired_date_contract = ngày hiện tại + 1 năm (2027/08/24)",
       note="Nguồn: tab「Cố định ngày bill tiền」r2, r3 (07/2023). ⚠ TC > 2 năm tuổi — CẦN VERIFY LẠI."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "datetime_first_payment là ngày 1~28 → các tháng sau bill đúng ngày đó",
       JOB + "\n- Hợp đồng standard tháng có datetime_first_payment lần lượt là ngày 02, 10, 28",
       "1. Với từng hợp đồng, chạy job bill của tháng tiếp theo\n"
       "2. Kiểm tra expired_date_contract sau mỗi lần bill",
       "3 hợp đồng: datetime_first_payment = ngày 02, 10, 28",
       "expired_date_contract của tháng tiếp theo luôn rơi đúng ngày 02 / 10 / 28 tương ứng "
       "(giữ nguyên ngày của datetime_first_payment)",
       env="PRODUCTION",
       note="Nguồn: r494-r496, tab「Cố định ngày bill tiền」r4 (3 mốc cùng quy tắc → gộp)."),

    tc("Ngày bill & expired_date", "DATA-005", "Boundary",
       "datetime_first_payment = ngày 29 → tháng 2 lùi về 27/28, tháng khác giữ 28",
       JOB + "\n- Hợp đồng standard tháng, datetime_first_payment = ngày 29",
       "1. Chạy job bill lần lượt các tháng 2→12 và tháng 1\n"
       "2. Ghi lại expired_date_contract sau mỗi lần\n"
       "3. Thử ở năm có tháng 2 = 28 ngày và năm nhuận (29 ngày)",
       "datetime_first_payment = ngày 29; 2 kịch bản: tháng 2 có 28 và 29 ngày",
       "- Bill tháng 2 → expired_date = 29/3; các tháng còn lại expired_date = ngày 28 của tháng kế\n"
       "- Bill tháng 1 khi tháng 2 có 28 ngày → expired_date = 27/2\n"
       "- Bill tháng 1 khi tháng 2 có 29 ngày → expired_date = 28/2",
       env="PRODUCTION",
       note="Nguồn: r497-r511. ⚠ Corpus mô tả 'Bill đúng vào ngày 29 → next expired_date = ngày 28' — "
            "quy tắc lùi 1 ngày này KHÔNG có trong spec, xem MT-32."),

    tc("Ngày bill & expired_date", "DATA-005", "Boundary",
       "datetime_first_payment = ngày 30 → tháng 2 lùi, các tháng 30/31 ngày cho kết quả khác nhau",
       JOB + "\n- Hợp đồng standard tháng, datetime_first_payment = ngày 30",
       "1. Chạy job bill lần lượt 12 tháng\n2. Ghi lại expired_date_contract mỗi lần",
       "datetime_first_payment = ngày 30",
       "- Bill tháng 2 → 30/3 · tháng 3 → 29/4 · tháng 4 → 30/5 · tháng 5 → 29/6 · tháng 6 → 30/7\n"
       "- tháng 7 → 30/8 · tháng 8 → 29/9 · tháng 9 → 30/10 · tháng 10 → 29/11 · tháng 11 → 30/12\n"
       "- tháng 12 → 30/01 · tháng 1 (tháng 2 có 28 ngày) → 28/2; (tháng 2 có 29 ngày) → 29/2",
       env="PRODUCTION",
       note="Nguồn: r525-r537. ⚠ Chuỗi giá trị này KHÔNG suy ra được từ 1 công thức đơn giản "
            "(lúc 29 lúc 30) — cần Dev xác nhận công thức, xem MT-32."),

    tc("Ngày bill & expired_date", "DATA-005", "Boundary",
       "datetime_first_payment = ngày 31 → tháng thiếu lùi về ngày cuối, tháng đủ quay lại 31",
       JOB + "\n- Hợp đồng standard tháng, datetime_first_payment = ngày 31",
       "1. Chạy job bill lần lượt 12 tháng\n2. Ghi lại expired_date_contract mỗi lần",
       "datetime_first_payment = ngày 31",
       "- Bill tháng 2 → 31/3 · tháng 3 → 30/4 · tháng 4 → 31/5 · tháng 5 → 30/6 · tháng 6 → 31/7\n"
       "- tháng 7 → 31/8 · tháng 8 → 30/9 · tháng 9 → 31/10 · tháng 10 → 30/11 · tháng 11 → 31/12\n"
       "- tháng 12 → 31/01 · tháng 1 → 28/2 (hoặc 29/2 năm nhuận)\n"
       "- Tháng thiếu lùi về ngày cuối tháng, tháng sau có ngày 31 thì QUAY LẠI ngày 31",
       env="PRODUCTION",
       note="Nguồn: r538-r548, tab「Cố định ngày bill tiền」r5, r6."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Bill lỗi rồi bill lại thành công (chưa quá 7 ngày) → expired_date vẫn theo datetime_first_payment",
       JOB + "\n- Hợp đồng standard tháng bị bill lỗi, chưa quá 7 ngày",
       "1. Kịch bản A: job bill lại thành công\n"
       "2. Kịch bản B: user bấm nút bill lại ở màn list bot\n"
       "3. Kịch bản C: user bấm nút bill lại ở màn point-setting\n"
       "4. Sau mỗi kịch bản kiểm tra expired_date_contract",
       "3 kịch bản bill lại; datetime_first_payment = ngày 10",
       "Cả 3 kịch bản: ngày của expired_date_contract vẫn lấy theo datetime_first_payment (ngày 10), "
       "KHÔNG bị dịch theo ngày bill lại",
       env="PRODUCTION",
       note="Nguồn: tab「Cố định ngày bill tiền」r7-r9 (3 dòng cùng expected → gộp)."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Upgrade từ free lên plan trả phí → tạo contract mới với mốc ngày MỚI",
       "- Bot free, upgrade lên standard/pro (cả tháng và năm)",
       "1. Upgrade free → standard tháng → kiểm tra expired_date và datetime_first_payment\n"
       "2. Lặp lại với standard năm, pro tháng, pro năm",
       "4 tổ hợp upgrade từ free",
       "Cả 4 tổ hợp: tạo contract mới với datetime_first_payment = ngày hiện tại, "
       "expired_date tính theo ngày hiện tại",
       note="Nguồn: tab「Cố định ngày bill tiền」r21-r24. ⚠ TC 07/2023 — CẦN VERIFY LẠI."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Upgrade standard → pro giữa kỳ → GIỮ NGUYÊN expired_date và datetime_first_payment",
       "- Bot standard tháng đang còn hạn, datetime_first_payment = ngày 10",
       "1. Upgrade lên pro\n2. Kiểm tra expired_date_contract và datetime_first_payment",
       "Bot standard tháng còn hạn",
       "expired_date_contract và datetime_first_payment GIỮ NGUYÊN (không reset theo ngày upgrade)",
       note="Nguồn: tab「Cố định ngày bill tiền」r25."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Bill năm: 12 bản ghi phân bổ có payment_date theo mốc từng tháng",
       JOB + "\n- Hợp đồng standard NĂM bắt đầu ngày 30/11",
       "1. Bill hợp đồng năm (qua web và qua job)\n"
       "2. Liệt kê payment_date của 12 bản ghi phân bổ trong payment_histories\n"
       "3. Kiểm tra payment_detail_aff tương ứng",
       "Ngày bắt đầu 30/11, plan standard năm",
       "- 12 bản ghi có payment_date lần lượt: 30/11, 30/12, 30/01, 28/02, 30/03, … "
       "(lùi về ngày cuối tháng khi tháng thiếu)\n"
       "- payment_detail_aff có bản ghi tương ứng cho từng tháng",
       env="PRODUCTION",
       note="Nguồn: tab「Change bill tiền theo năm」r3-r14 (12/2023). "
            "⚠ TC > 2 năm tuổi — CẦN VERIFY LẠI danh sách ngày phân bổ."),

    tc("Ngày bill & expired_date", "DATA-005", "Normal",
       "Bill transfer: payment_date ghi theo ngày CHUYỂN TIỀN, không phải ngày tạo bill",
       "- Hợp đồng bill transfer tạo bill ngày 01/03, user chuyển khoản ngày 03/03",
       "1. Tạo bill transfer ngày 01/03 → kiểm tra payment_histories\n"
       "2. Chuyển khoản ngày 03/03 (callback success) → kiểm tra lại payment_date và created_at\n"
       "3. Đối chiếu cột 契約(更新)日 trên màn lịch sử thanh toán",
       "Ngày tạo bill 01/03, ngày chuyển khoản 03/03",
       "- payment_date = 03/03 (ngày chuyển khoản)\n"
       "- Màn lịch sử thanh toán hiện 契約(更新)日 = 03/03",
       env="PRODUCTION",
       note="Nguồn: tab「Task nhỏ」r1 (12/2023 — 'Change logic bill transfer update paymentdate theo ngày "
            "chuyển tiền'). ⚠ Field Matrix #28 ghi 'payment_date có thể NULL, confidence Trung bình' — "
            "TC này lấp gap của spec."),
]
