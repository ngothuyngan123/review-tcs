# -*- coding: utf-8 -*-
"""FA-031 — Nhóm 33-37: bill max friend, campaign 初月無料, redirect sau bill, hoàn tiền.

Nguồn chính: TCsLine_Bill tiền_Improve2025
  · tab「Bill max friend」(12/2025 → 04/2026, 402 dòng, 319 TC lá — Bug KH #34409, Bug Tester #35650,
    SpecImprove #35441)
  · tab「Campaign + Tutorial」(12/2025 → 03/2026, 265 TC — Bug Tester #34889, SpecImprove #33838)
Bổ sung: TCsLine_Bill tiền → tab「Redirect khi bill success」(09/2024),
         tab「Logic refund」(04/2023) và tab「Refund update 1.0」(05/2023).
"""
from _common import tc

MF = "- Bot đã bị job detect vượt mốc bạn bè, đang hiển thị cảnh báo ở màn point-setting"

S7 = [
    # ═════════════ 33. Bill max friend — cảnh báo & upgrade ═════════════
    tc("Bill max friend — cảnh báo & upgrade", "FRIEND-001", "Normal",
       "Bot free/standard ≤ 50.000 bạn bè → không cảnh báo gì",
       "- Bot plan free (cả bot mới và bot cũ) có tổng bạn bè 49.999",
       "1. Select vào bot ở màn list bot\n2. Select bot ở header\n3. Mở vài màn tính năng của bot",
       "Tổng friend = 49.999",
       "Không hiện màn cảnh báo / banner nào; truy cập mọi màn bình thường",
       note="Nguồn: Bill max friend r4."),

    tc("Bill max friend — cảnh báo & upgrade", "FRIEND-001", "Boundary",
       "Bot free vượt 50.000 bạn bè → chặn 3 lối vào bằng màn cảnh báo",
       "- Bot plan free có tổng bạn bè 50.001",
       "1. Select bot ở màn list bot\n2. Select bot ở header\n3. Truy cập trực tiếp URL 1 màn tính năng của bot",
       "Tổng friend = 50.001",
       "Cả 3 lối vào đều hiện màn thông báo「quá 50.000 friend」và không vào được màn tính năng",
       note="Nguồn: Bill max friend r5-r7 (3 dòng cùng expected → gộp, liệt kê đủ 3 lối vào)."),

    tc("Bill max friend — cảnh báo & upgrade", "FUNC-001", "Normal",
       "2 nút upgrade (アップデート ở point-setting và アップグレードにすすむ ở màn cảnh báo) → cùng mở màn thanh toán pro",
       "- Bot free vượt 50.000 bạn bè",
       "1. Ở màn point-setting, click nút「アップデート」\n"
       "2. Quay lại, ở màn cảnh báo click「アップグレードにすすむ」",
       "Bot free > 50.000 friend",
       "Cả 2 nút đều mở màn thanh toán plan pro (giống luồng upgrade free → pro)",
       note="Nguồn: Bill max friend r9, r10."),

    tc("Bill max friend — cảnh báo & upgrade", "FUNC-006", "Normal",
       "Upgrade free → pro bằng thẻ thành công → gỡ toàn bộ cảnh báo max friend",
       "- Bot free vượt 50.000 bạn bè",
       "1. Upgrade lên pro, nhập thẻ hợp lệ\n2. Mở /basic/point-settings\n"
       "3. Select vào bot\n4. Kiểm tra header\n5. Truy cập màn tính năng",
       "Thẻ hợp lệ",
       "- Màn point-setting hiện plan プロ, trạng thái 正常\n"
       "- Select vào bot KHÔNG còn màn cảnh báo max-friend\n- Header không còn message cảnh báo\n"
       "- Truy cập màn tính năng bình thường",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r11. RULE-08: bill tiền → PRODUCTION."),

    tc("Bill max friend — cảnh báo & upgrade", "FUNC-006", "Abnormal",
       "Upgrade max friend bằng thẻ lỗi → không upgrade, ở lại màn nhập thẻ",
       "- Bot free vượt 50.000 bạn bè",
       "1. Upgrade lên pro, nhập thẻ lỗi\n2. Quan sát màn hình\n3. Kiểm tra plan của bot",
       "Thẻ lỗi 4111 1111 1111 1111",
       "Báo lỗi, KHÔNG upgrade plan, vẫn hiển thị màn nhập thẻ để nhập lại",
       note="Nguồn: Bill max friend r12, r64."),

    tc("Bill max friend — cảnh báo & upgrade", "STATE-003", "Normal",
       "Upgrade max friend bằng chuyển khoản, chưa chuyển tiền → chặn truy cập, redirect về point-setting",
       "- Bot free vượt 50.000 bạn bè, đã đăng ký upgrade pro bằng 銀行振込",
       "1. Mở /basic/point-settings → đọc status\n2. Select vào bot\n3. Truy cập 1 màn tính năng của bot",
       "Đăng ký transfer, chưa chuyển khoản",
       "- Màn point-setting hiện trạng thái đang đợi chuyển khoản + nút hủy chuyển khoản\n"
       "- Select vào bot hoặc mở màn tính năng → redirect về màn point-setting",
       note="Nguồn: Bill max friend r14."),

    tc("Bill max friend — cảnh báo & upgrade", "STATE-003", "Abnormal",
       "Upgrade max friend transfer bị hủy / callback fail → bot GIỮ plan pro nhưng chuyển cancel hợp đồng",
       "- Bot free vượt 50.000 bạn bè, đã đăng ký upgrade pro bằng 銀行振込",
       "1. Kịch bản A: bấm nút hủy chuyển khoản\n2. Kịch bản B: không chuyển khoản → callback fail\n"
       "3. Mỗi kịch bản: đọc status ở màn point-setting và kiểm tra bot_contracts\n"
       "4. Select vào bot và mở màn tính năng",
       "2 kịch bản: hủy chuyển khoản / callback fail",
       "- Cả 2: bot GIỮ NGUYÊN plan pro nhưng hợp đồng chuyển sang trạng thái cancel (upgrade fail)\n"
       "- Select vào bot / mở màn tính năng → redirect về màn point-setting\n"
       "- Màn detail hợp đồng hiện giống hợp đồng cưỡng chế hủy",
       note="Nguồn: Bill max friend r15, r17, r18, r22. ⚠ Hành vi này NGƯỢC với luồng upgrade thường "
            "(callback fail thì về plan free) — xem MT-10."),

    tc("Bill max friend — cảnh báo & upgrade", "FRIEND-001", "Boundary",
       "Bot free vượt 100.000 bạn bè → màn cảnh báo mốc 100k",
       "- Bot plan free có tổng bạn bè 100.001",
       "1. Select bot ở màn list bot\n2. Select bot ở header\n3. Mở màn tính năng\n"
       "4. Ở màn point-setting quan sát alert và nút アップグレード",
       "Tổng friend = 100.001",
       "- 3 lối vào đều hiện màn thông báo mốc 100.000 friend\n"
       "- Màn point-setting hiện alert cần upgrade plan + nút アップグレード mở màn thanh toán pro",
       note="Nguồn: Bill max friend r45-r50."),

    tc("Bill max friend — cảnh báo & upgrade", "FRIEND-001", "Boundary",
       "Bot standard/pro vượt 100.000 → cho dùng bình thường 30 ngày, ngày thứ 31 mới chặn",
       "- Bot standard cũ (flag_contract_new=0) hoặc bot pro, tổng bạn bè 100.001\n"
       "- Job detect max friend đã chạy ngày D",
       "1. Ngày D+29: mở màn tính năng của bot\n2. Ngày D+30: mở màn tính năng\n"
       "3. Ngày D+31: mở màn tính năng\n4. Ở mỗi mốc kiểm tra màn point-setting",
       "3 mốc: 29, 30, 31 ngày sau ngày detect",
       "- D+29 và D+30: truy cập các màn BÌNH THƯỜNG\n"
       "- D+31: KHÔNG truy cập được, redirect về màn point-setting\n"
       "- Màn point-setting hiển thị alert bill tiền max friend",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r99-r103, r140-r145. Mốc 30 ngày này KHÔNG có trong feature-spec.md "
            "(BR-02 chỉ nêu >100.000 thì tính phí) — xem MT-33."),

    tc("Bill max friend — cảnh báo & upgrade", "FRIEND-001", "Normal",
       "Bot standard MỚI (flag_contract_new=1) vượt 50.000 → cảnh báo và mở luồng upgrade lên pro",
       "- Bot standard có flag_contract_new = 1, tổng bạn bè 50.001",
       "1. Select bot ở list bot / header / mở màn tính năng\n"
       "2. Ở màn point-setting click「アップデート」\n3. Ở header click「確認する」\n"
       "4. Ở màn cảnh báo click「アップグレードにすすむ」",
       "flag_contract_new = 1, friend = 50.001",
       "- Cả 3 lối vào hiện màn thông báo quá 50.000 friend\n"
       "- Cả 3 nút (アップデート / 確認する / アップグレードにすすむ) đều mở màn upgrade standard → pro",
       note="Nguồn: Bill max friend r56-r62."),

    tc("Bill max friend — cảnh báo & upgrade", "REG-002", "Normal",
       "Job detect max friend chỉ cảnh báo khi ĐÃ vượt mốc thật",
       "- Bot có tổng bạn bè 99.999 (chưa đạt 100.000)",
       "1. Chạy job detect max friend\n2. Select vào bot và mở màn point-setting\n"
       "3. Đọc nội dung thông báo (nếu có)",
       "Tổng friend = 99.999",
       "KHÔNG hiện thông báo「đã đạt 100.000 người」; bot dùng bình thường",
       note="Nguồn: Bill max friend r348-r357 (Bug KH #34409, 11/02/2026 — hiện nhầm mốc 100.000 "
            "khi chưa đạt). Ghi 'regression'."),

    # ═════════════ 34. Bill max friend — thanh toán & job ═════════════
    tc("Bill max friend — thanh toán & job", "DATA-002", "Normal",
       "Màn confirm thanh toán max friend: hiện đúng bậc bạn bè + số ngày + số tiền theo ngày",
       MF + "\n- Bot pro có 150.000 bạn bè, còn 356 ngày tới expired_date",
       "1. Click「決済にすすむ」→ mở step 1\n2. Đọc mục số friend, thời hạn, 日割り và số tiền\n"
       "3. Tự tính: 361円 × số ngày remain\n4. Lặp lại với bot có 250.000 bạn bè",
       "Bot 150.000 friend (remain 356 ngày) và bot 250.000 friend",
       "- 150.000 friend: hiện「総友だち数　10~20万人」\n- 250.000 friend: hiện「総友だち数　20~30万人」\n"
       "- Thời hạn hiện「ngày hiện tại ~ expired_date」\n- 日割り hiện đúng số ngày remain (356日分)\n"
       "- Số tiền = 361円 × 356 = 128.516円 (税込), khớp phép tính tay",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r105-r109, r147-r151. RULE-08: bill tiền → PRODUCTION."),

    tc("Bill max friend — thanh toán & job", "DATA-001", "Normal",
       "Màn confirm max friend: phương thức thanh toán khóa theo phương thức của hợp đồng gốc",
       MF + "\n- 2 bot: 1 hợp đồng bill card, 1 hợp đồng bill transfer",
       "1. Mở màn confirm của bot bill card → đọc mục phương thức\n"
       "2. Mở màn confirm của bot bill transfer → đọc mục phương thức",
       "2 bot: card và transfer",
       "- Bot bill card: chỉ hiện phương thức thẻ + thông tin thẻ chính\n"
       "- Bot bill transfer: chỉ hiện 銀行振込, KHÔNG hiện số thẻ\n"
       "- Không cho chọn phương thức khác phương thức của hợp đồng gốc",
       note="Nguồn: Bill max friend r110, r152, r153. Đây là SpecImprove: 'bill max friend bill theo "
            "phương thức bill của bot'."),

    tc("Bill max friend — thanh toán & job", "FUNC-006", "Normal",
       "Bill max friend bằng thẻ chính thành công → gỡ chặn + ghi 3 nơi",
       MF + "\n- Bot pro bill card, thẻ chính hợp lệ",
       "1. Qua step 1 → step 2 → bấm「決済する」\n2. Quan sát step 3\n"
       "3. Kiểm tra bot_card_bill_friend và bots.max_friend_plan\n"
       "4. Mở lịch sử hóa đơn và 操作履歴\n5. Select vào bot",
       "Thẻ chính hợp lệ",
       "- Hiện màn bill thành công (step 3), bấm「ホームに戻る」về /admin/home\n"
       "- DB: bot_card_bill_friend.status=0, expired_date = expired_date của bot; bots.max_friend_plan=1\n"
       "- Lịch sử hóa đơn có bản ghi「従量課金」; 操作履歴 có「友だち数別の従量課金」\n"
       "- Select vào bot không còn bị chặn",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r117-r119, r162. RULE-07 + RULE-08."),

    tc("Bill max friend — thanh toán & job", "FUNC-006", "Abnormal",
       "Bill max friend bằng thẻ chính lỗi → mở màn nhập thẻ mới (KHÔNG tự fallback sang thẻ phụ)",
       MF + "\n- Bot pro bill card, thẻ chính bị từ chối, có cả thẻ phụ",
       "1. Bấm「決済する」ở step 2\n2. Quan sát màn hình\n3. Kiểm tra giao dịch của thẻ phụ trên UnivaPay\n"
       "4. Nhập thẻ mới hợp lệ và bill lại",
       "Thẻ chính lỗi, có thẻ phụ hợp lệ",
       "- Báo lỗi và mở màn nhập thẻ mới\n"
       "- Thẻ phụ KHÔNG bị charge (khác với job bill định kỳ có fallback thẻ phụ)\n"
       "- Nhập thẻ mới hợp lệ: bill thành công, sang step 3",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r120, r122, r163, r165 (ghi chú của tester: "
            "'Bill maincard fail không chuyển sang bill subcard à? => Không nhé'). "
            "⚠ Khác hẳn job bill định kỳ — xem MT-34."),

    tc("Bill max friend — thanh toán & job", "STATE-003", "Normal",
       "Bill max friend bằng chuyển khoản: 3 trạng thái theo callback",
       MF + "\n- Bot pro bill năm, phương thức transfer",
       "1. Bấm 決済する → quan sát khi tài khoản đang phát hành và khi đã phát hành\n"
       "2. Đọc trạng thái ở màn point-setting\n"
       "3. Kịch bản A: user chuyển khoản → callback success\n"
       "4. Kịch bản B: user không chuyển khoản → callback fail\n"
       "5. Kịch bản C: user bấm hủy chuyển khoản\n"
       "6. Mỗi kịch bản kiểm tra bots.max_friend_plan và bot_card_bill_friend.status",
       "3 kịch bản callback",
       "- Chưa chuyển: màn hiện thông tin/chờ phát hành STK, point-setting hiện đợi chuyển khoản, "
       "bot_card_bill_friend.status=4\n"
       "- Callback success: trạng thái đang hợp đồng, tạo lịch sử bill + lịch sử hoạt động\n"
       "- Callback fail HOẶC hủy chuyển khoản: max_friend_plan=3, bot_card_bill_friend.status=1, "
       "KHÔNG tạo lịch sử bill, màn point-setting hiện trạng thái bill lỗi max friend",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r123-r135, r166-r178, r192-r195."),

    tc("Bill max friend — thanh toán & job", "JOB-008", "Normal",
       "Job bill max friend (06:00) bằng thẻ: có fallback thẻ phụ",
       "- Bot đã accept bill max friend, tới kỳ bill; có thẻ chính và thẻ phụ\n"
       "- Quyền chạy job handle:bill_max_friend",
       "1. Kịch bản A: thẻ chính hợp lệ → chạy job\n"
       "2. Kịch bản B: thẻ chính lỗi, thẻ phụ hợp lệ → chạy job\n"
       "3. Kịch bản C: cả 2 thẻ lỗi → chạy job\n"
       "4. Mỗi kịch bản kiểm tra bot_card_bill_friend, bots.max_friend_plan, lịch sử bill, màn point-setting",
       "3 kịch bản thẻ",
       "- A và B: số tiền = số ngày remain × 361円; bot_card_bill_friend.status=0, "
       "expired_date = expired_date của bot; tạo lịch sử bill + lịch sử hoạt động\n"
       "- C: bots.max_friend_plan=3, bot_card_bill_friend.status=1, KHÔNG tạo lịch sử bill, "
       "màn point-setting hiện dòng bill lỗi max friend",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r182-r191 + feature-spec.md §7 (HandleBillMaxFriend). RULE-08."),

    tc("Bill max friend — thanh toán & job", "DATA-002", "Normal",
       "Bill max friend theo kỳ tiếp theo = 11.000円/tháng (không còn tính theo ngày)",
       "- Bot đã bill max friend lần đầu, tới kỳ bill tiếp theo",
       "1. Chạy job bill max friend kỳ tiếp theo\n2. Đọc số tiền trong payment_histories\n"
       "3. Kiểm tra bot_card_bill_friend\n4. Lặp lại với hợp đồng bill năm (kiểm tra phân bổ)",
       "Bot bill tháng và bot bill năm",
       "- Bill tháng: số tiền = 11.000円\n"
       "- Bill năm: số tiền = 11.000円, có phân bổ theo số tháng remain\n"
       "- bot_card_bill_friend.status=0, expired_date = expired_date của bot",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r196-r205. ⚠ Con số 11.000円 và công thức 361円/ngày KHÔNG có trong "
            "feature-spec.md (BR-02 chỉ nêu calculateBillMaxFriend()) — xem MT-35."),

    tc("Bill max friend — thanh toán & job", "JOB-008", "Boundary",
       "Job bill max friend bằng transfer cũng tạo bill trước 30 ngày",
       "- Bot bill năm, phương thức transfer, đã accept bill max friend",
       "1. Set expired_date − hôm nay = 31 ngày → chạy job\n2. = 30 ngày → chạy job\n"
       "3. = 29 ngày → chạy job\n4. Kiểm tra UnivaPay sau mỗi lần",
       "3 mốc: 31, 30, 29 ngày",
       "- 31 ngày: không tạo bill chuyển khoản\n- 30 ngày: TẠO bill chuyển khoản\n"
       "- 29 ngày: không tạo lại (giống quy tắc job bill hợp đồng)",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r206-r208."),

    tc("Bill max friend — thanh toán & job", "DATA-004", "Normal",
       "Đổi phương thức bill của hợp đồng gốc → phương thức bill max friend đổi theo",
       "- Bot đang có bill max friend hoạt động, hợp đồng gốc bill transfer",
       "1. Đổi phương thức hợp đồng gốc từ transfer sang card\n"
       "2. Kiểm tra phương thức của bản ghi bot_card_bill_friend\n3. Chạy job bill max friend kỳ sau",
       "Hợp đồng gốc đổi transfer → card",
       "- bot_card_bill_friend.payment_method đổi theo hợp đồng gốc\n"
       "- Kỳ bill max friend tiếp theo được charge bằng thẻ",
       env="PRODUCTION",
       note="Nguồn: Bill max friend r302-r330 (Bug Tester #35650, 04/2026 — bill max friend bill bằng "
            "phương thức chuyển khoản dù hợp đồng đã đổi)."),

    tc("Bill max friend — thanh toán & job", "COMPAT-LEGACY-002", "Normal",
       "Bot CŨ đã có bill max friend trước đây → thẻ bill max friend dùng chung thẻ hợp đồng",
       "- Bot đã có bill max friend từ trước đợt improve (bot bill tháng và bot bill năm)",
       "1. Đổi thẻ chính của hợp đồng\n2. Kiểm tra thẻ dùng cho bill max friend ở kỳ tiếp theo\n"
       "3. Với bot cũ: kiểm tra bảng bot_card_bill_friend có được update thẻ không",
       "2 bot cũ: bill tháng và bill năm",
       "- Recover: thẻ bill max friend dùng chung với thẻ bill hợp đồng\n"
       "- Với bot bill max friend CŨ: đổi thẻ chính KHÔNG update thông tin thẻ ở bot_card_bill_friend",
       note="Nguồn: Bill max friend r213, r214, r223. ⚠ 2 phát biểu này mâu thuẫn nhau trong cùng tab — "
            "xem MT-36."),

    tc("Bill max friend — thanh toán & job", "UI-004", "Normal",
       "Bill max friend hiển thị như 1 dòng phụ dưới hợp đồng gốc ở màn list",
       "- Bot đã bill max friend thành công và bot bị bill lỗi max friend",
       "1. Mở /basic/point-settings\n2. Quan sát dòng của bot đã bill thành công\n"
       "3. Quan sát dòng của bot bill lỗi\n4. Click「詳細を確認」ở dòng bill lỗi",
       "2 bot: max_friend_plan = 1 và = 3",
       "- Bill max friend hiển thị như 1 dòng riêng, nằm ngay dưới hợp đồng gốc của bot\n"
       "- Bot bill lỗi: dòng phụ hiện trạng thái 延滞中, có nút「詳細を確認」mở màn detail",
       note="Nguồn: Bill max friend r215, r239, r240 + BR-02 (feature-spec.md §5: item phụ "
            "contract_max_friend=1)."),

    tc("Bill max friend — thanh toán & job", "FRIEND-001", "Abnormal",
       "Bot bị bill LỖI max friend → chặn truy cập, redirect về point-setting",
       "- Bot có bots.max_friend_plan = 3 (bill lỗi max friend)",
       "1. Select vào bot\n2. Mở màn tính năng bất kỳ của bot\n3. Quan sát alert ở màn point-setting",
       "max_friend_plan = 3",
       "- Select bot / mở màn tính năng đều redirect về /basic/point-settings\n"
       "- Màn point-setting hiện alert bill lỗi max friend",
       note="Nguồn: Bill max friend r237, r238."),

    # ═════════════ 35. Campaign 初月無料 ═════════════
    tc("Campaign 初月無料", "FUNC-008", "Normal",
       "Add bot free ĐÃ verify phía LINE → hiện modal campaign sau khi add xong",
       "- Đăng nhập owner, chuẩn bị bot free đã verify phía LINE",
       "1. Add bot free đã verify\n2. Quan sát sau khi hoàn tất add bot\n"
       "3. Lặp lại với bot free CHƯA verify",
       "2 bot free: đã verify và chưa verify",
       "- Bot đã verify: sau khi add xong hiện modal campaign\n"
       "- Bot chưa verify: KHÔNG hiện màn campaign",
       note="Nguồn: Campaign r5, r6."),

    tc("Campaign 初月無料", "FUNC-008", "Abnormal",
       "Add bot standard/pro/enterprise (từ slot có sẵn) → KHÔNG hiện campaign, không bill tiền",
       "- Có slot trống của standard, pro và enterprise\n- Có bot đã verify và chưa verify",
       "1. Add bot standard vào slot (cả 2 trạng thái verify)\n2. Lặp với pro\n3. Lặp với enterprise\n"
       "4. Sau mỗi lần quan sát màn hình và kiểm tra có bill tiền không",
       "6 tổ hợp: 3 loại slot × 2 trạng thái verify",
       "Cả 6 tổ hợp: KHÔNG hiện màn campaign, add bot bình thường và KHÔNG bill tiền",
       note="Nguồn: Campaign r7-r12 (6 dòng cùng expected → gộp)."),

    tc("Campaign 初月無料", "FUNC-008", "Normal",
       "Upgrade bot free ĐÃ verify từ màn TOP → mở màn campaign detail",
       "- Bot free đã verify phía LINE, trong thời gian campaign",
       "1. Từ màn TOP bấm upgrade bot free lên standard\n2. Quan sát màn hình\n"
       "3. Lặp lại với pro\n4. Lặp lại với bot free CHƯA verify",
       "Bot free verify (→standard, →pro) và bot free chưa verify",
       "- Bot đã verify: hiện màn campaign detail\n- Bot chưa verify: KHÔNG hiện campaign",
       note="Nguồn: Campaign r13-r15."),

    tc("Campaign 初月無料", "STATE-002", "Normal",
       "Màn campaign lần đầu: giữ hiển thị khi reload/mở tab mới; đóng thì chuyển sang floating",
       "- Bot free vừa add, đã verify, has_campaign = 1",
       "1. Chưa bấm đóng: tắt tab và mở lại tool ở tab mới → quan sát\n2. Reload trang → quan sát\n"
       "3. Bấm nút đóng → quan sát\n4. Reload / mở tab mới / logout-login → quan sát",
       "has_campaign = 1",
       "- Chưa đóng: reload và mở tab mới đều VẪN hiện màn campaign\n"
       "- Bấm đóng: hiện popup tutorial + floating của campaign\n"
       "- Sau khi đóng: reload / tab mới / logout-login đều hiện FLOATING (không hiện lại màn campaign đầy đủ)",
       note="Nguồn: Campaign r34-r39."),

    tc("Campaign 初月無料", "STATE-002", "Normal",
       "Floating campaign: đóng thì ẩn tới 00:00 hôm sau",
       "- Đang hiển thị floating campaign",
       "1. Bấm nút X trên floating\n2. Reload trang → quan sát\n3. Tắt/mở tab mới → quan sát\n"
       "4. Logout và login lại → quan sát\n5. Sang ngày mới → quan sát",
       "—",
       "- Bấm X: đóng banner, hẹn hiển thị lại vào 00:00 ngày mai\n"
       "- Reload / tab mới / logout-login trong cùng ngày: KHÔNG hiện lại floating\n"
       "- Sang ngày mới: floating hiện lại",
       note="Nguồn: Campaign r47-r50, r54."),

    tc("Campaign 初月無料", "DATA-003", "Boundary",
       "Điều kiện hiển thị floating theo mốc 7 ngày kể từ ngày tạo",
       "- Bot free đã verify, ghi nhận created_at",
       "1. Ở mốc now − created_at = 6 ngày → mở tool, quan sát floating\n"
       "2. Ở mốc = 7 ngày → quan sát\n3. Ở mốc = 8 ngày → quan sát",
       "3 mốc: 6, 7, 8 ngày sau ngày tạo",
       "- ≤ 7 ngày: hiển thị floating ở các màn\n- > 7 ngày: KHÔNG hiển thị floating",
       note="Nguồn: Campaign r52, r53."),

    tc("Campaign 初月無料", "DATA-003", "Normal",
       "Màn campaign detail: nội dung + countdown 4 block ngày/giờ/phút/giây",
       "- Bot free đã verify, đang trong thời gian campaign",
       "1. Mở màn campaign detail\n2. Đọc mục キャンペーン期間, キャンペーン内容, ご注意\n"
       "3. Quan sát khối countdown\n4. Theo dõi countdown đếm lùi 1 phút",
       "Campaign còn 3 ngày 5 giờ",
       "- キャンペーン期間 hiện「LINE公式アカウント接続日（本日）から1週間後の23:59まで」\n"
       "- キャンペーン内容 nêu rõ ưu đãi 初月無料 và ví dụ 1月1日 → 初回決済日 2月1日\n"
       "- ご注意 nêu: hủy trước ngày thanh toán đầu thì không bị tính phí; sau khi hủy plan trả phí "
       "không dùng lại free cho cùng LOA\n"
       "- Countdown 4 block [日][時間][分][秒], mỗi đơn vị luôn 2 chữ số, đếm lùi đúng theo thời gian thực",
       note="Nguồn: Campaign r61-r70."),

    tc("Campaign 初月無料", "DATA-002", "Normal",
       "Màn confirm campaign: ngày thanh toán đầu tiên = ngày hiện tại + 1 tháng, có badge 1ヶ月分無料",
       "- Bot free đã verify, mở màn confirm đăng ký plan có phí qua campaign\n"
       "- Ngày hiện tại = 2025/11/18",
       "1. Đọc mục ngày thanh toán lần đầu\n2. Quan sát badge\n"
       "3. Đọc số tiền theo plan và chu kỳ",
       "Ngày hiện tại 2025/11/18",
       "- Hiện「2025年11月18日 → 2025年12月18日」(ngày hiện tại → 1 tháng sau)\n"
       "- Badge màu cam「1ヶ月分無料！」hiển thị đúng vị trí, không che text khác\n"
       "- Số tiền đúng theo plan × chu kỳ đã chọn",
       note="Nguồn: Campaign r105-r108."),

    tc("Campaign 初月無料", "DATA-005", "Normal",
       "Upgrade qua campaign thành công → expired_date + 1 tháng và về CUỐI NGÀY 23:59:59",
       "- Bot free đã verify, trong thời gian campaign",
       "1. Upgrade bot free → standard qua campaign, thanh toán thành công\n"
       "2. Kiểm tra bot_contracts.expired_date_contract (cả phần giờ)\n"
       "3. Mở 操作履歴 xem lịch sử hợp đồng\n4. Lặp lại với upgrade lên pro",
       "2 kịch bản: free→standard và free→pro qua campaign",
       "- Upgrade thành công, có bản ghi lịch sử hợp đồng\n"
       "- expired_date_contract = ngày hiện tại + 1 tháng, phần giờ = 23:59:59 (cuối ngày)",
       env="PRODUCTION",
       note="Nguồn: Campaign r302, r303 (Bug Tester #34889, 10/03/2026). RULE-08."),

    tc("Campaign 初月無料", "DATA-005", "Abnormal",
       "Upgrade NGOÀI thời gian campaign hoặc bot CHƯA verify → không cộng thêm 1 tháng",
       "- Kịch bản A: bot free đã verify nhưng đã quá 7 ngày\n"
       "- Kịch bản B: bot free CHƯA verify, trong thời gian campaign",
       "1. Với mỗi kịch bản: upgrade lên standard/pro, thanh toán thành công\n"
       "2. Kiểm tra expired_date_contract",
       "2 kịch bản như tiền đề",
       "Cả 2: upgrade thành công nhưng expired_date KHÔNG được cộng thêm 1 tháng miễn phí",
       env="PRODUCTION",
       note="Nguồn: Campaign r27, r304."),

    tc("Campaign 初月無料", "DATA-001", "Normal",
       "Sau khi hợp đồng campaign thành công → DB cập nhật đúng ở 3 bảng",
       "- Vừa upgrade thành công qua campaign",
       "1. Kiểm tra bot_contracts (status_payment, expired_date, plan)\n"
       "2. Kiểm tra bots.plan_type\n3. Kiểm tra bot_slots xem bot đã map với hợp đồng mới chưa\n"
       "4. Lặp lại cho 5 tổ hợp: standard tháng/card, standard năm/card, standard năm/transfer, "
       "pro tháng/card, pro năm/transfer",
       "5 tổ hợp plan × chu kỳ × phương thức",
       "Cả 5 tổ hợp: bot_contracts.status_payment=1, expired_date +1 tháng (ưu đãi campaign), "
       "plan_type đúng plan đã mua; bot_slots có bản ghi map bot với hợp đồng mới",
       env="PRODUCTION",
       note="Nguồn: Campaign r139-r144 (5 dòng cùng nhóm expected → gộp)."),

    tc("Campaign 初月無料", "JOB-009", "Normal",
       "Job ScanHasCampaign (02:00 hằng ngày) set has_campaign đúng theo plan và tuổi bot",
       "- Chuẩn bị 3 bot: plan_type != 2; plan_type = 2 tạo > 7 ngày; plan_type = 2 tạo < 7 ngày",
       "1. Chạy job job:ScanHasCampaign\n2. Kiểm tra cột has_campaign của từng bot",
       "3 bot như tiền đề",
       "- plan_type != 2 → has_campaign = 0\n- plan_type = 2 và now − created_at > 7 ngày → has_campaign = 0\n"
       "- plan_type = 2 và now − created_at < 7 ngày → has_campaign = 1",
       env="PRODUCTION",
       note="Nguồn: Campaign r145-r147, r307-r309 (SpecImprove #33838 — chuyển job sang Java). "
            "⚠ Job này KHÔNG có trong feature-spec.md §7 — xem MT-37."),

    tc("Campaign 初月無料", "JOB-009", "Normal",
       "Job recover campaign: chỉ set has_campaign=1 cho bot FREE đã VERIFY và thỏa mốc thời gian",
       "- Chuẩn bị 4 bot: free-verify thỏa mốc, free-verify không thỏa mốc, "
       "free-chưa verify thỏa mốc, pro/standard-verify thỏa mốc",
       "1. Chạy job recover\n2. Kiểm tra has_campaign của từng bot",
       "4 bot như tiền đề",
       "- free + verify + thỏa mốc thời gian → has_campaign = 1\n"
       "- 3 trường hợp còn lại → has_campaign = 0",
       env="PRODUCTION",
       note="Nguồn: Campaign r148-r151, r310-r313."),

    # ═════════════ 36. Redirect sau bill success ═════════════
    tc("Redirect sau bill success", "OUT-001", "Normal",
       "Mua mới hợp đồng bằng thẻ → redirect đúng URL theo plan × chu kỳ",
       "- Chuẩn bị mua mới 4 tổ hợp: standard tháng, standard năm, pro tháng, pro năm (đều bill card)",
       "1. Với mỗi tổ hợp, hoàn tất mua mới bằng thẻ hợp lệ\n2. Ghi lại URL được redirect sau khi bill success",
       "4 tổ hợp plan × chu kỳ, bill card",
       "- standard tháng → https://step.lme.jp/monthly/standard_success\n"
       "- standard năm → https://step.lme.jp/yearly/standard_success\n"
       "- pro tháng → https://step.lme.jp/monthly/pro_success\n"
       "- pro năm → https://step.lme.jp/yearly/pro_success",
       env="PRODUCTION",
       note="Nguồn: tab「Redirect khi bill success」r4-r8 (09/2024). RULE-08: bill tiền → PRODUCTION."),

    tc("Redirect sau bill success", "OUT-001", "Abnormal",
       "Các case KHÔNG bill tiền → KHÔNG redirect",
       "- Chuẩn bị: tạo bot free; mua mới bằng chuyển khoản (standard năm, pro năm); "
       "đổi thẻ khi hợp đồng CÒN HẠN (4 tổ hợp plan × chu kỳ); enterprise",
       "1. Thực hiện lần lượt từng thao tác\n2. Sau mỗi thao tác kiểm tra có bị redirect ra step.lme.jp không",
       "8 thao tác không phát sinh bill tiền",
       "Cả 8 thao tác đều KHÔNG redirect sang step.lme.jp",
       env="PRODUCTION",
       note="Nguồn: tab Redirect r3, r6, r9-r14, r31, r32 + r305-r315 (Màn hình bill tiền)."),

    tc("Redirect sau bill success", "OUT-001", "Normal",
       "Bill lại / đổi thẻ khi hết hạn / hợp đồng lại / upgrade → đều redirect đúng URL",
       "- Chuẩn bị các bot ở 4 tổ hợp plan × chu kỳ cho từng luồng",
       "1. Bot hết hạn → đổi thẻ để bill\n2. Bấm nút bill lại ở màn list bot\n"
       "3. Bấm nút bill lại ở màn point-setting\n4. Hợp đồng lại bằng thẻ\n"
       "5. Upgrade standard→pro và free→standard/pro\n"
       "6. Sau mỗi lần ghi lại URL redirect",
       "5 luồng × 4 tổ hợp plan/chu kỳ",
       "Mọi luồng có bill tiền thành công đều redirect về đúng "
       "https://step.lme.jp/{monthly|yearly}/{standard|pro}_success theo plan và chu kỳ SAU khi bill",
       env="PRODUCTION",
       note="Nguồn: tab Redirect r15-r38 (nhiều dòng cùng quy tắc → gộp, liệt kê đủ 5 luồng)."),

    tc("Redirect sau bill success", "OUT-002", "Normal",
       "Bill success phải đi qua router bill-success TRƯỚC rồi mới về màn hoàn tất",
       "- Chuẩn bị các luồng: mua mới, upgrade, bill lại overdue (card và transfer), "
       "bill lại hợp đồng đã hủy, extend, thanh toán thẻ qua campaign",
       "1. Với mỗi luồng, mở DevTools → tab Network trước khi bấm thanh toán\n"
       "2. Bấm thanh toán và ghi lại chuỗi điều hướng\n3. Kiểm tra có đi qua router bill-success không",
       "7 luồng thanh toán",
       "Mọi luồng bill thành công đều điều hướng qua router bill-success trước, "
       "sau đó mới quay về màn bill thành công của tool",
       env="PRODUCTION",
       note="Nguồn: r256-r304 (Bug tự detect #38957, tab Màn hình bill tiền). "
            "Evidence bắt buộc: ảnh chụp tab Network."),

    # ═════════════ 37. Hoàn tiền ═════════════
    tc("Hoàn tiền", "PAY-001", "Normal",
       "Bản ghi refund hiển thị ở đủ 4 màn với tên plan là refund",
       "- Đã thực hiện 1 giao dịch refund cho hợp đồng standard bill tháng",
       "1. Mở màn bill tiền (admin)\n2. Mở màn bill tiền phân bổ\n3. Mở màn bill success\n"
       "4. Mở màn quản lý affiliate (cả phía user và phía admin)\n"
       "5. Kiểm tra tên plan của bản ghi refund ở từng màn",
       "1 giao dịch refund",
       "Cả 4 màn đều có bản ghi với tên plan là「refund」, số tiền là giá trị âm",
       env="PRODUCTION",
       note="Nguồn: tab「Logic refund」r16 (04/2023). ⚠ TC > 2 năm tuổi — CẦN VERIFY LẠI. "
            "⚠ Thao tác refund nằm ở ADMIN PORTAL nội bộ, không thuộc 5 màn của FA-031 — "
            "cần Leader xác nhận có giữ nhóm này trong kho FA-031 không. Xem MT-38."),

    tc("Hoàn tiền", "PAY-001", "Normal",
       "Refund hợp đồng bill THÁNG → số tiền refund = giá trị đã nhập lúc tạo refund",
       "- Hợp đồng standard bill tháng đã bill thành công",
       "1. Tạo refund với số tiền X\n2. Mở màn bill tiền chung và màn phân bổ\n"
       "3. Đối chiếu số tiền hiển thị với X\n4. Kiểm tra cột amount_refund trong payment_histories",
       "Số tiền refund X = 5.000円",
       "- Màn bill tiền chung và màn phân bổ đều hiện đúng 5.000円 (refund_amount)\n"
       "- Bản ghi refund gắn đúng tháng tương ứng",
       env="PRODUCTION",
       note="Nguồn: tab Logic refund r20, r31-r33."),

    tc("Hoàn tiền", "PAY-001", "Normal",
       "Refund hợp đồng bill NĂM → màn phân bổ hiện theo số tiền ĐÃ PHÂN BỔ, các tháng sau bị xóa",
       "- Hợp đồng standard bill năm đã bill và đã sử dụng 2 tháng",
       "1. Tạo refund\n2. Mở màn bill tiền chung → đọc số tiền\n3. Mở màn phân bổ → đọc số tiền\n"
       "4. Kiểm tra các bản ghi phân bổ của các tháng CHƯA tới\n5. Kiểm tra số tiền ở màn TOP",
       "Hợp đồng năm, đã dùng 2 tháng",
       "- Màn bill tiền chung: hiện số tiền refund đã nhập (refund_amount)\n"
       "- Màn phân bổ: hiện số tiền theo phân bổ (amount)\n"
       "- Các bản ghi phân bổ của tháng chưa tới bị XÓA, không bill tiếp\n"
       "- Màn TOP: tổng tiền trừ đi phần đã phân bổ",
       env="PRODUCTION",
       note="Nguồn: tab Logic refund r17-r19, r34. ⚠ 2 màn hiển thị 2 con số khác nhau cho cùng 1 refund — "
            "dễ bị hiểu là lệch dữ liệu; xem MT-39."),

    tc("Hoàn tiền", "PAY-001", "Abnormal",
       "Không refund cho tháng đã sử dụng",
       "- Hợp đồng bill năm đã bill và đã sử dụng tháng 1, 2, 3",
       "1. Thử tạo refund cho tháng 1 (đã sử dụng)\n2. Quan sát kết quả",
       "Tháng 1 đã sử dụng",
       "Hệ thống KHÔNG cho refund phần tháng đã sử dụng",
       env="PRODUCTION",
       note="Nguồn: tab Logic refund r4. ⚠ TC gốc chỉ có mô tả trong ghi chú, không có expected chuẩn — "
            "kết quả mong đợi do AI viết lại, CẦN LEADER XÁC NHẬN."),

    tc("Hoàn tiền", "DATA-004", "Normal",
       "Refund plan standard/pro → xử lý bot theo tình trạng bot free của user",
       "- Chuẩn bị 4 user: (a) chưa có bot free & chưa có bot nào; (b) chưa có bot free & đã có bot trả phí; "
       "(c) có bot free & chưa có bot trả phí; (d) có bot free & có bot trả phí",
       "1. Với mỗi user, refund hợp đồng standard bill tháng\n"
       "2. Kiểm tra bot_contracts (status, contract_type, expired_date) và bots\n"
       "3. Lặp lại toàn bộ với plan pro",
       "4 tình huống × 2 plan (standard, pro)",
       "- (a): bot_contracts.status=3, expired_date lùi về kỳ trước (vd bill 17/5 → expired 17/6 → sau refund = 17/5)\n"
       "- (b): chuyển thành bot free — contract_type=free, contract_bill_type=month, expired_date +1 tháng từ hôm nay\n"
       "- (c) và (d): hủy hợp đồng của bot_contract_id đã mua; bot free vẫn dùng bình thường; "
       "(d) vào bot đã hủy thì ra màn /basic/point-settings",
       env="PRODUCTION",
       note="Nguồn: tab「Refund update 1.0」r3-r10 (17/05/2023). ⚠ TC > 2 năm tuổi — CẦN VERIFY LẠI."),

    tc("Hoàn tiền", "DATA-004", "Normal",
       "Refund plan ENTERPRISE → tách thành N hợp đồng standard/pro theo số bot đã kết nối",
       "- Hợp đồng EP standard 10 slot đã kết nối 2 bot; và 1 hợp đồng EP chưa kết nối bot nào",
       "1. Refund hợp đồng EP chưa kết nối bot → kiểm tra bot_contracts\n"
       "2. Refund hợp đồng EP đã kết nối 2 bot → kiểm tra bot_contracts\n"
       "3. Lặp lại với EP pro",
       "EP standard/EP pro; 0 bot và 2 bot đã kết nối",
       "- EP chưa kết nối bot: XÓA bot_contract_id tương ứng\n"
       "- EP đã kết nối 2 bot: xóa bot_contract_id tổng của EP, TẠO 2 bot_contract mới "
       "có contract_type = standard (hoặc pro) tương ứng",
       env="PRODUCTION",
       note="Nguồn: tab Refund update 1.0 r11-r14. ⚠ TC 05/2023 — CẦN VERIFY LẠI."),

    tc("Hoàn tiền", "DATA-004", "Normal",
       "Đổi rate hoa hồng: bill CŨ giữ rate cũ, bill MỚI theo rate mới",
       "- Có bản ghi payment_detail_aff đã tạo theo rate cũ",
       "1. Đổi sang rate mới\n2. Kiểm tra các bản ghi bill CŨ\n3. Thực hiện bill mới → kiểm tra rate\n"
       "4. Xóa rate mới → bill lại → kiểm tra rate\n"
       "5. Với hợp đồng bill năm: đổi rate giữa chừng → kiểm tra tháng trước và tháng sau",
       "Rate cũ và rate mới",
       "- Bill cũ: giữ nguyên rate và số tiền tương ứng\n- Bill mới: theo rate mới\n"
       "- Xóa rate mới: bill mới quay lại theo rate cũ\n"
       "- Bill năm: tháng trước theo rate cũ, tháng tới theo rate mới",
       env="PRODUCTION",
       note="Nguồn: tab Logic refund r10-r15. ⚠ TC 04/2023 — CẦN VERIFY LẠI. "
            "Thuộc tính năng Affiliate (không phải 5 màn FA-031) — xem MT-38."),
]
