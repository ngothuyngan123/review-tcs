# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 1-2.

S1 Menu & điều kiện truy cập · S2 Modal promo & trang campaign.

⚠️ Phụ thuộc 3 mâu thuẫn NỀN, đọc trước khi chạy:
• MT-04 — bot Free có được đổi LOA hay không (spec nói redirect home, TCs 04/2026 nói
  được trong 1 tháng campaign).
• MT-03 — campaign「1ヶ月無料開放」còn dùng hay KH đã bỏ (tester [AI] v2 ghi "đã ngưng").
• MT-13 — 3 biến thể UI wizard (#34632 · #37744 · [AI] v2). File này viết theo bản
  MỚI NHẤT ([AI] TCs_change_bot_v2, 07-08/2026) vì có kết quả chạy trên cả dev + staging.
"""
from _common import tc

PAID = ("- Đăng nhập Admin chủ (主管理者) của bot plan Standard trở lên (bots.plan_type = 1)\n"
        "- Bot đang ở trạng thái đã kết nối (bots.is_connected = 1)\n"
        "- Bot KHÔNG có bản ghi đặt lịch đổi LOA nào đang active")
FREE_IN = ("- Đăng nhập Admin chủ của bot Free (bots.plan_type = 2)\n"
           "- Bot được add vào tool CHƯA quá 1 tháng (bots.created_at + 1 tháng > hiện tại)\n"
           "- Đang trong kỳ campaign「1ヶ月無料開放」")
FREE_OUT = ("- Đăng nhập Admin chủ của bot Free (bots.plan_type = 2)\n"
            "- Bot được add vào tool ĐÃ quá 1 tháng (bots.created_at + 1 tháng < hiện tại)")
MT03 = "⚠️ Phụ thuộc MT-03 — nếu Leader chốt campaign đã ngưng thì TC này bị loại. "
MT04 = "⚠️ Phụ thuộc MT-04 — điều kiện vào màn của bot Free chưa chốt. "
MT13 = "⚠️ Phụ thuộc MT-13 — viết theo bản UI mới nhất ([AI] v2). "

S1 = [
    # ═══════════════ 1. Menu & điều kiện truy cập ═══════════════
    tc("Menu & điều kiện truy cập", "FUNC-001", "Normal",
       "Bot trả phí — vào màn đổi LOA từ menu thường, hiển thị đúng màn chọn phương thức",
       PAID,
       "1. Đăng nhập Admin chủ của bot Standard\n"
       "2. Mở sidebar, tìm mục「LINE公式アカウント入れ替え」\n"
       "3. Bấm vào mục menu đó\n"
       "4. Quan sát URL và nội dung trang vừa mở",
       "Bot Standard, bot_id dev 46682",
       "- Trang mở được, KHÔNG bị đá về /basic/overview hay /admin/home\n"
       "- URL là trang chọn phương thức đổi LOA (SCR-03「01 入れ替え方法選択」)\n"
       "- Hiển thị 2 option: すぐにLINE公式アカウントを入れ替える và LINE公式アカウント入れ替え予約をする\n"
       "- Có nút「使い方を見る」\n"
       "- Console trình duyệt không có lỗi JavaScript",
       note="Nguồn: Change bot r84 (đối chiếu ngược từ case bot free) + TC-CBF-016/017. " + MT13
            + "Evidence: ảnh full trang + URL."),

    tc("Menu & điều kiện truy cập", "FUNC-001", "Normal",
       "Bot trả phí — vào màn đổi LOA từ menu お気に入り (favourite) cho kết quả giống menu thường",
       PAID + "\n- Đã ghim mục「LINE公式アカウント入れ替え」vào menu favourite",
       "1. Đăng nhập Admin chủ của bot Standard\n"
       "2. Mở khu vực menu favourite\n"
       "3. Bấm mục「LINE公式アカウント入れ替え」đã ghim\n"
       "4. So sánh trang vừa mở với trang mở từ menu thường",
       "Bot Standard",
       "- Mở đúng cùng 1 màn chọn phương thức đổi LOA như vào từ menu thường\n"
       "- Không có khác biệt về nội dung, nút, trạng thái 2 option\n"
       "- URL giống hệt",
       note="Nguồn: Change bot r85 · r228. " + MT13 + "Evidence: ảnh 2 trang đặt cạnh nhau."),

    tc("Menu & điều kiện truy cập", "REG-SHARED-001", "Normal",
       "Entry point cũ — nút「LINE公式アカウント入れ替え」trên toolbar màn LOA接続設定 vẫn dẫn đúng flow mới",
       PAID + "\n- Đang ở màn「LOA接続設定」(/admin/bot-edit?id={id})",
       "1. Vào /admin/home, bấm「接続設定」của bot Standard\n"
       "2. Tìm nút「LINE公式アカウント入れ替え」trên toolbar\n"
       "3. Bấm nút đó\n"
       "4. Quan sát trang đích",
       "Bot Standard",
       "- Điều hướng tới flow đổi LOA MỚI (màn chọn phương thức), KHÔNG phải landing page marketing cũ\n"
       "- Không có lỗi 404/500\n"
       "- Nút vẫn nằm đúng vị trí toolbar như trước (entry point giữ nguyên)",
       note="Nguồn: TC-CBF-113 (REG-SHARED-001, TD Section 7.1 'Entry point GIỮ NGUYÊN') "
            "+ AddBot/Testcase r136 · r473. ⚠️ MT-12 — spec bot-edit/ui-spec.md:91 + 208-240 vẫn tả "
            "SCR-BE-03 là landing page marketing 3 block + nút「無料で利用開始」. Evidence: ảnh toolbar + trang đích."),

    tc("Menu & điều kiện truy cập", "COMPAT-LEGACY-001", "Normal",
       "URL cũ /admin/change-bots-new/{id} vẫn truy cập được và hiển thị wizard MỚI",
       PAID + "\n- Biết URL cũ /admin/change-bots-new/{id} với {id} là Hashids của chính bot đang đăng nhập",
       "1. Đăng nhập Admin chủ của bot Standard\n"
       "2. Dán trực tiếp URL /admin/change-bots-new/{id} vào thanh địa chỉ\n"
       "3. Enter và quan sát trang\n"
       "4. So sánh với trang vào từ menu",
       "{id} = Hashids của bot Standard đang đăng nhập",
       "- Route KHÔNG trả 404 — vẫn sống\n"
       "- Nội dung render là wizard MỚI (màn chọn phương thức), KHÔNG phải landing page cũ có nút「無料で利用開始」\n"
       "- Giống hệt trang vào từ menu",
       note="Nguồn: TC-CBF-111 (Pass dev + staging, QA-spec-021 'GIỮ NGUYÊN route, thay đổi behavior bên trong') "
            "+ Change bot r86. RULE-09 — nhánh cũ & mới song song. Evidence: ảnh trang + URL."),

    tc("Menu & điều kiện truy cập", "PERM-003", "Abnormal",
       "Bot A truy cập URL màn đổi LOA của bot B (LOA khác tenant) → bị chặn, đá về overview",
       "- Đăng nhập Admin chủ của bot A\n"
       "- Biết Hashids id của bot B thuộc tài khoản/tenant KHÁC",
       "1. Đăng nhập Admin chủ bot A\n"
       "2. Dán URL /admin/change-bots-new/{id_botB}\n"
       "3. Enter và quan sát\n"
       "4. Kiểm tra xem có thông tin nào của bot B bị lộ ra không (tên bot, channel id)",
       "{id_botB} = Hashids của bot B (tenant khác)",
       "- KHÔNG được vào màn đổi LOA của bot B\n"
       "- Redirect về /basic/overview (hoặc 403 theo MT-02)\n"
       "- Trang KHÔNG hiển thị bất kỳ thông tin nào của bot B: tên bot, Channel ID, số bạn bè\n"
       "- Response body không chứa dữ liệu bot B",
       note="Nguồn: Change bot r87 (EXP: direct ra màn overview) + TC-CBF-094 (PERM-003, MAP-PERM-03). "
            "PERM-003 trigger ghi rõ 'BẮT BUỘC khi có chức năng change bot'. "
            "⚠️ Loại response (redirect vs 403) chưa chốt — xem MT-02. Evidence: ảnh trang + Network response."),

    tc("Menu & điều kiện truy cập", "PERM-003", "Boundary",
       "Đổi bot_id trên URL GIỮA các bước wizard sang bot khác đang thao tác → chặn, không lẫn dữ liệu",
       PAID + "\n- Admin có 2 bot X và Y, cả 2 đều plan Standard\n"
       "- Đang ở bước nhập thông tin kết nối (SCR-04) của bot X, đã nhập 4 field",
       "1. Ở bước SCR-04 của bot X, mở DevTools tab Network\n"
       "2. Sửa tham số bot_id trên URL từ X sang Y, giữ nguyên dữ liệu đã nhập\n"
       "3. Bấm nút sang bước tiếp theo\n"
       "4. Quan sát response + màn hình\n"
       "5. Kiểm tra DB bảng bots của cả X và Y",
       "bot X = 46682, bot Y = 46548 (cùng Admin)",
       "- Request bị reject HOẶC wizard reset về đầu flow — KHÔNG xử lý tiếp với bot_id đã bị đổi\n"
       "- DB: KHÔNG có bản ghi bots mới nào được tạo cho bot Y\n"
       "- Thông tin 4 field của bot X KHÔNG bị gán sang bot Y\n"
       "- Màn hình không hiển thị lẫn dữ liệu 2 bot",
       note="Nguồn: TC-CBF-095 (SEC-001) + TC-CBF-098 (SEC-ISO-001). RULE-07 — verify cả DB. "
            "Evidence: Network request/response + query DB bảng bots 2 bot."),

    tc("Menu & điều kiện truy cập", "PAY-LIMIT-001", "Abnormal",
       "Bot Free đã quá 1 tháng — vào màn đổi LOA từ menu thì 2 option bị disable, không có banner campaign",
       FREE_OUT,
       "1. Đăng nhập Admin chủ bot Free tạo cách đây hơn 1 tháng\n"
       "2. Vào mục menu「有料プラン限定」→「LINE公式アカウント入れ替え」\n"
       "3. Quan sát có màn campaign không\n"
       "4. Thử bấm vào từng option đổi LOA",
       "Hôm nay 2026-06-13, bot Free tạo 2026-05-12 (quá 1 tháng 1 ngày)",
       "- KHÔNG hiển thị màn/modal campaign\n"
       "- Vào thẳng màn chọn phương thức\n"
       "- KHÔNG hiển thị banner「LINE公式アカウント入れ替え機能　無料開放キャンペーン」\n"
       "- CẢ 2 option đổi LOA bị disable (có overlay xám + icon khoá), bấm không có tác dụng\n"
       "- Bấm vào chữ「スタンダードプラン」→ chuyển sang màn /admin/bot-add",
       note="Nguồn: Change bot r91 (TR=OK) + r99. " + MT04 + MT03
            + "⚠️ Improve xxx r11 (#37229 comment 10,11) sửa thành: text có underline + hyperlink click được "
              "→ chuyển đến trang plan có phí (KHÁC /admin/bot-add) — xem MT-14b. Evidence: ảnh màn + ảnh option bị khoá."),

    tc("Menu & điều kiện truy cập", "PAY-LIMIT-001", "Abnormal",
       "Bot Free đã hết campaign — truy cập TRỰC TIẾP bằng URL bước con thì bị chặn kèm message và đá sang màn add bot",
       FREE_OUT + "\n- Biết URL bước con /admin/change-bot-sub/{id}?type_change=immediate",
       "1. Đăng nhập Admin chủ bot Free đã hết campaign\n"
       "2. Dán URL /admin/change-bot-sub/{id}?type_change=immediate\n"
       "3. Enter, quan sát message hiện ra\n"
       "4. Bấm OK trên message và quan sát trang đích",
       "{id} = Hashids bot Free hết campaign",
       "- KHÔNG cho phép vào màn bước con\n"
       "- Hiển thị message「スタンダードプラン以上のご契約でご利用できます」\n"
       "- Bấm OK → redirect sang /admin/bot-add\n"
       "- Không có bản ghi nào được tạo trong DB",
       note="Nguồn: Change bot r100 (TR=OK). " + MT04 + "Evidence: ảnh message + URL đích."),

    tc("Menu & điều kiện truy cập", "COMPAT-LEGACY-001", "Boundary",
       "Bot Free KHÔNG có campaign truy cập URL cũ → vẫn redirect /admin/home (hành vi giữ nguyên)",
       "- Đăng nhập Admin chủ bot Free (plan_type = 2)\n"
       "- KHÔNG có campaign nào đang active cho bot này",
       "1. Đăng nhập Admin chủ bot Free\n"
       "2. Dán URL cũ /admin/change-bots-new/{id}\n"
       "3. Enter và quan sát URL cuối cùng",
       "{id} = Hashids bot Free",
       "- Bị redirect về /admin/home\n"
       "- KHÔNG render wizard đổi LOA\n"
       "- Hành vi giống hệt trước đợt improve (EP-08 plan_type==2 + no campaign → redirect home)",
       note="Nguồn: TC-CBF-112 (COMPAT-LEGACY-001, TD Section 2 'GIỮ NGUYÊN') + spec "
            "bot-edit/web/logic-spec.md:25 'redirect nếu bot free' + feature-spec.md:258-262 bước 2. "
            "⚠️ [AI] v2 ghi Blocked cả dev + staging: không dựng được bot Free NGOÀI window campaign. "
            "Evidence: URL cuối + Network 302."),

    tc("Menu & điều kiện truy cập", "PAY-LIMIT-001", "Boundary",
       "Biên gói — plan ngay DƯỚI Standard vẫn khoá option đặt lịch; đúng Standard đã mở",
       "- Có 2 bot cùng Admin: bot P plan ngay dưới Standard, bot Q plan đúng Standard\n"
       "- Cả 2 bot đều đã kết nối",
       "1. Đăng nhập Admin, vào màn chọn phương thức của bot P\n"
       "2. Quan sát trạng thái option 2「LINE公式アカウント入れ替え予約をする」\n"
       "3. Chuyển sang bot Q, vào cùng màn\n"
       "4. Quan sát lại option 2 của bot Q",
       "bot P = plan dưới Standard; bot Q = plan Standard",
       "- Bot P: option 2 bị khoá (overlay xám + icon khoá), bấm không chọn được\n"
       "- Bot Q: option 2 mở, bấm chọn được và CTA đổi thành「入れ替え予約設定に進む」\n"
       "- Ranh giới đúng tại mốc Standard, không lệch 1 bậc",
       note="Nguồn: TC-CBF-027 (PAY-LIMIT-001, BR-42 biên 'Standard trở lên'; Pass dev, Blocked staging). "
            "RULE-01 — đây là case Boundary của PAY-LIMIT-001. Evidence: ảnh option 2 của cả 2 bot."),

    tc("Menu & điều kiện truy cập", "STATE-001", "Boundary",
       "Bot đã có đặt lịch đổi LOA active → vào màn đổi LOA bị điều hướng NGAY sang màn đã đặt lịch",
       PAID.replace("- Bot KHÔNG có bản ghi đặt lịch đổi LOA nào đang active",
                    "- Bot ĐÃ có 1 bản ghi đặt lịch đổi LOA đang active (schedule_change_bots)"),
       "1. Đăng nhập Admin chủ bot đã có đặt lịch đổi LOA\n"
       "2. Vào mục menu「LINE公式アカウント入れ替え」\n"
       "3. Quan sát màn hiện ra\n"
       "4. Lặp lại bằng cách vào URL cũ /admin/change-bots-new/{id}",
       "Bot Standard có 1 item đặt lịch đổi LOA",
       "- KHÔNG hiển thị màn chọn phương thức (SCR-03)\n"
       "- Điều hướng NGAY sang màn「05-A 予約済み」(SCR-08) hiển thị thông tin đặt lịch\n"
       "- Vào bằng URL cũ cũng cho cùng kết quả\n"
       "- Không tạo thêm bản ghi đặt lịch thứ 2",
       note="Nguồn: TC-CBF-021 (STATE-001, BR-12/BR-34; Pass dev) + TC-CBF-072 (COMPAT-LEGACY-001; Pass dev) "
            "+ Change bot r104 '1 bot chỉ được 1 item đặt lịch change bot'. Evidence: URL + ảnh màn đích."),

    tc("Menu & điều kiện truy cập", "UI-001", "Normal",
       "Nút「使い方を見る」trên màn chọn phương thức mở đúng nguồn hướng dẫn, ở tab mới",
       PAID + "\n- Đang ở màn chọn phương thức đổi LOA",
       "1. Vào màn chọn phương thức đổi LOA\n"
       "2. Bấm nút/chữ「使い方を見る」1 lần\n"
       "3. Quan sát tab hiện tại và tab mới\n"
       "4. Bấm nhanh 2 lần liên tiếp vào cùng nút đó",
       "Bot Standard",
       "- Mở TAB MỚI, tab hiện tại KHÔNG bị thay thế\n"
       "- Nội dung mở ra đúng nguồn Leader chốt ở MT-14 (trang manual https://lme.jp/manual/loa_replacement/ "
       "HOẶC video hướng dẫn)\n"
       "- Bấm 2 lần nhanh chỉ mở 1 tab, không mở 2 tab trùng",
       note="⚠️ MT-14 — Change bot r105/r254/r255 nói mở link manual loa_replacement; TC-CBF-023 nói mở video "
            "hướng dẫn. CHƯA CHỐT. Nguồn: Change bot r105 · r254 · r255 + TC-CBF-023 (Pass dev + staging). "
            "Evidence: ảnh tab mới + URL."),
]

S2 = [
    # ═══════════════ 2. Modal promo & trang campaign ═══════════════
    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Bot Free trong 1 tháng + campaign đang chạy → modal promo tự hiện dạng overlay trên Dashboard",
       FREE_IN,
       "1. Đăng nhập Admin chủ bot Free mới add trong vòng 1 tháng\n"
       "2. Vào Dashboard (/basic/overview)\n"
       "3. Quan sát màn hình ngay khi trang load xong\n"
       "4. Thử bấm vào một mục bất kỳ của Dashboard phía sau modal",
       "Bot Free created_at = hôm nay - 5 ngày; campaign active (now giữa start_date và end_date)",
       "- Modal「入れ替え機能プロモーション」tự hiển thị dạng overlay che Dashboard, không cần bấm gì\n"
       "- Nút × hiển thị ở góc trên phải modal\n"
       "- Dashboard phía sau bị mờ và KHÔNG bấm được (click không có tác dụng)\n"
       "- Modal chỉ hiện 1 ngày 1 lần cho cùng 1 Admin",
       note=MT03 + "Nguồn: TC-CBF-001 (Skip dev + staging — tester ghi 'KH đã BỎ, không dùng tính năng này "
            "nữa → feature đã ngưng') + Change bot r83 ('hiển thị all màn, modal hiển thị 1 ngày 1 lần'). "
            "Evidence: ảnh Dashboard có overlay + thử click xuyên overlay."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Bot Free trong 1 tháng nhưng KHÔNG có campaign active → modal promo không hiện",
       "- Đăng nhập Admin chủ bot Free (plan_type = 2), bot add chưa quá 1 tháng\n"
       "- KHÔNG có campaign nào active (đang ngoài kỳ campaign)",
       "1. Đăng nhập Admin chủ bot Free\n"
       "2. Vào Dashboard\n"
       "3. Chờ trang load xong hoàn toàn, quan sát 10 giây",
       "Bot Free created_at = hôm nay - 5 ngày; không campaign",
       "- KHÔNG có modal promo nào hiện ra\n"
       "- Dashboard hiển thị và tương tác bình thường\n"
       "- Console không có lỗi JS",
       note=MT03 + "Nguồn: TC-CBF-003 (BR-01; Blocked dev + staging — cần seed campaign_status, DB read-only). "
            "Evidence: ảnh Dashboard sạch."),

    tc("Modal promo & trang campaign", "PAY-LIMIT-001", "Boundary",
       "Bot Free NGOÀI 1 tháng dù campaign hệ thống vẫn chạy → modal promo KHÔNG hiện",
       FREE_OUT + "\n- Campaign hệ thống vẫn đang active",
       "1. Đăng nhập Admin chủ bot Free tạo hơn 1 tháng trước\n"
       "2. Vào Dashboard, quan sát\n"
       "3. Thử truy cập URL cũ /admin/change-bots-new/{id}",
       "Bot Free created_at = hôm nay - 40 ngày; campaign active",
       "- Modal promo KHÔNG hiển thị trên Dashboard\n"
       "- Truy cập URL cũ → redirect /admin/home\n"
       "- Điều kiện 'trong 1 tháng' tính theo bots.created_at, không theo thời hạn campaign hệ thống",
       note=MT03 + MT04 + "Nguồn: TC-CBF-002 (PAY-LIMIT-001, QA-spec-001; Blocked cả 2 env — "
            "'set created_at>30 ngày trên dev vẫn vào SCR-03, không reproduce redirect. Trigger opaque'). "
            "⚠️ Đây là RISK: dev không reproduce được nhánh redirect. Evidence: ảnh Dashboard + URL cuối."),

    tc("Modal promo & trang campaign", "PAY-LIMIT-001", "Boundary",
       "Bot trả phí (Standard trở lên) khi campaign active → xác nhận đối tượng được hưởng ưu đãi",
       PAID + "\n- Campaign「1ヶ月無料開放」đang active",
       "1. Đăng nhập Admin chủ bot Standard\n"
       "2. Vào Dashboard, quan sát có modal promo không\n"
       "3. Vào màn chọn phương thức đổi LOA\n"
       "4. Quan sát có banner campaign không",
       "Bot Standard 46978; campaign active",
       "- Bot trả phí vào THẲNG màn chọn phương thức, KHÔNG qua màn/modal campaign\n"
       "- KHÔNG hiển thị banner campaign\n"
       "- Cả 2 option đổi LOA đều mở (không bị khoá)",
       note="Nguồn: TC-CBF-004 (Pass dev: 'bot Standard 46978 → SCR-03 trực tiếp, KHÔNG campaign'; "
            "tester QA-004 CONFIRMED: campaign chỉ áp dụng Bot Free dùng thử trong vòng 1 tháng). "
            + MT03 + "Evidence: ảnh Dashboard + ảnh màn chọn phương thức."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Đóng modal promo bằng nút × → về Dashboard, không điều hướng, lần vào lại trong ngày không hiện lại",
       FREE_IN + "\n- Modal promo đang hiển thị",
       "1. Modal promo đang hiện trên Dashboard\n"
       "2. Bấm nút × ở góc trên phải modal\n"
       "3. Quan sát màn hình\n"
       "4. Reload Dashboard trong cùng ngày, quan sát lại",
       "Bot Free trong campaign",
       "- Modal đóng, overlay biến mất, Dashboard tương tác bình thường\n"
       "- KHÔNG điều hướng sang trang khác\n"
       "- Reload trong cùng ngày: modal KHÔNG hiện lại (quy tắc 1 ngày 1 lần)",
       note=MT03 + "Nguồn: TC-CBF-005 (BR-03b; Skip cả 2 env vì modal đã ngưng) + Change bot r83 "
            "('khi click button close sẽ không hiển thị lại modal'). Evidence: ảnh trước/sau + ảnh sau reload."),

    tc("Modal promo & trang campaign", "FUNC-001", "Boundary",
       "Bấm vùng overlay NGOÀI modal promo → modal KHÔNG đóng (chỉ nút × mới đóng được)",
       FREE_IN + "\n- Modal promo đang hiển thị",
       "1. Modal promo đang hiện\n"
       "2. Bấm vào vùng overlay mờ bên ngoài modal (góc trái dưới màn hình)\n"
       "3. Quan sát modal\n"
       "4. Bấm tiếp phím Esc, quan sát modal",
       "Bot Free trong campaign",
       "- Modal VẪN hiển thị sau khi bấm overlay — không đóng\n"
       "- Bấm Esc cũng không đóng (hành vi khác modal chuẩn, cố ý theo spec)\n"
       "- Chỉ nút × mới đóng được",
       note=MT03 + "Nguồn: TC-CBF-007 (FUNC-001 + UIC-05, BR-03b 'hành vi khác modal chuẩn, cố ý theo spec'; "
            "Skip cả 2 env). Evidence: video ngắn thao tác click overlay + Esc."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Bấm「詳しくはこちら」trên modal promo → chuyển sang trang campaign",
       FREE_IN + "\n- Modal promo đang hiển thị",
       "1. Modal promo đang hiện\n"
       "2. Bấm nút「詳しくはこちら」\n"
       "3. Quan sát trang đích\n"
       "4. Vào lại Dashboard, quan sát modal có hiện lại không",
       "Bot Free trong campaign",
       "- Chuyển sang trang campaign「キャンペーンページ」\n"
       "- Vào lại Dashboard trong cùng ngày: modal KHÔNG hiện lại",
       note=MT03 + "Nguồn: TC-CBF-006 (BR-03; Skip cả 2 env) + Change bot r83 "
            "('khi click button 詳しくはこちら sẽ không hiển thị lại modal'). Evidence: ảnh trang campaign."),

    tc("Modal promo & trang campaign", "CONC-003", "Boundary",
       "Reload nhanh liên tiếp khi modal promo đang hiện → không hiện trùng 2 modal, không lỗi JS",
       FREE_IN + "\n- Modal promo đang hiển thị",
       "1. Modal promo đang hiện trên Dashboard\n"
       "2. Bấm F5 liên tiếp 5 lần trong 3 giây\n"
       "3. Chờ trang load xong, đếm số modal trên màn hình\n"
       "4. Mở DevTools Console kiểm tra lỗi",
       "Bot Free trong campaign; 5 lần F5 trong 3 giây",
       "- Chỉ có ĐÚNG 1 modal trên màn hình, không xếp lớp 2-3 modal\n"
       "- Console không có lỗi JS\n"
       "- Overlay không bị kẹt (đóng modal thì overlay mất hẳn)",
       note=MT03 + "Nguồn: TC-CBF-008 (CONC-003). Evidence: ảnh màn sau F5 + ảnh Console."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Trang campaign — countdown hiển thị realtime, đếm ngược liên tục đúng số ngày/giờ/phút còn lại",
       FREE_IN + "\n- Đang ở trang campaign「キャンペーンページ」",
       "1. Vào trang campaign\n"
       "2. Ghi lại giá trị countdown hiển thị (ngày/giờ/phút/giây)\n"
       "3. Đứng yên 70 giây, không reload\n"
       "4. Ghi lại giá trị countdown mới\n"
       "5. Đối chiếu với mốc hết hạn tính từ bots.created_at + 1 tháng (hết hạn 23:59)",
       "Bot Free created_at = 2026-05-14, hôm nay 2026-06-13 → còn 1 ngày",
       "- Countdown tự giảm mà KHÔNG cần reload\n"
       "- Sau 70 giây, số phút giảm đúng 1 (hoặc giây giảm đúng 70 nếu có hiển thị giây)\n"
       "- Giá trị khớp phép tính tay: (created_at + 1 tháng, 23:59) − thời điểm hiện tại\n"
       "- Không hiển thị số âm, không nhảy loạn",
       note=MT03 + "Nguồn: TC-CBF-009 (BR-04; Pass dev, Blocked staging) + Change bot r88-r90 "
            "(3 case created_at: chưa quá 1 tháng / đúng ngày này tháng trước / đã quá 1 tháng). "
            "Evidence: 2 ảnh countdown cách nhau 70 giây + phép tính tay."),

    tc("Modal promo & trang campaign", "FUNC-DATE-001", "Boundary",
       "Countdown về đúng 0 → tự động redirect /admin/home ngay, không cần reload",
       "- Đăng nhập Admin chủ bot Free\n"
       "- Mốc hết campaign của bot = thời điểm hiện tại + 2 phút (seed bots.created_at tương ứng)\n"
       "- Đang mở trang campaign, countdown đang chạy",
       "1. Mở trang campaign khi countdown còn ~2 phút\n"
       "2. Để nguyên tab, KHÔNG reload\n"
       "3. Chờ countdown giảm tới 00:00:00\n"
       "4. Quan sát hành vi trang ngay tại thời điểm 0",
       "Mốc hết hạn = now + 2 phút; 23:59 của ngày created_at + 1 tháng",
       "- Tại đúng thời điểm countdown = 0, trang TỰ redirect về /admin/home\n"
       "- Không đứng ở trang campaign với countdown âm\n"
       "- Không cần user reload mới redirect",
       note=MT03 + "Nguồn: TC-CBF-010 (FUNC-DATE-001, BR-05/FN-10; Blocked cả 2 env — "
            "'countdown→0 (26 ngày)/clock-skew chưa dựng được'). ⚠️ RISK: chưa ai chạy được TC này. "
            "Evidence: video từ 00:00:10 đến sau redirect."),

    tc("Modal promo & trang campaign", "FUNC-DATE-001", "Boundary",
       "Lệch giờ server/client (clock-skew) không làm sai countdown",
       "- Đăng nhập Admin chủ bot Free trong campaign\n"
       "- Có thể đổi giờ hệ thống của máy client",
       "1. Mở trang campaign, ghi lại countdown\n"
       "2. Đổi giờ máy client lùi 3 giờ\n"
       "3. Reload trang campaign, ghi lại countdown\n"
       "4. Đổi giờ máy client tiến 3 giờ so với thực tế\n"
       "5. Reload lại, ghi countdown\n"
       "6. Đối chiếu 3 giá trị",
       "Lệch client ±3 giờ so với giờ server",
       "- Countdown ở cả 3 lần KHÔNG lệch quá vài giây so với giá trị đúng theo giờ SERVER\n"
       "- Không xuất hiện countdown âm hay countdown nhảy thêm 3 giờ\n"
       "- Mốc hết hạn luôn tính theo giờ server",
       note=MT03 + "Nguồn: TC-CBF-011 (FUNC-DATE-001; Blocked cả 2 env). ⏳ QA-dev-020 — TA đề xuất "
            "compensate qua server_time, CHƯA CONFIRMED → đây là suy luận cần Leader xác nhận. "
            "Evidence: 3 ảnh countdown + ảnh giờ máy client."),

    tc("Modal promo & trang campaign", "SEC-001", "Abnormal",
       "Chưa đăng nhập truy cập URL trang campaign trực tiếp → redirect màn login, không lộ nội dung",
       "- Đăng xuất hoàn toàn / mở cửa sổ ẩn danh\n"
       "- Biết URL trang campaign",
       "1. Mở cửa sổ ẩn danh\n"
       "2. Dán URL trang campaign, Enter\n"
       "3. Quan sát URL cuối và nội dung trang\n"
       "4. Xem HTML response có chứa thông tin bot/campaign không",
       "URL trang campaign của 1 bot Free cụ thể",
       "- Redirect về màn login\n"
       "- KHÔNG render nội dung campaign (không thấy countdown, không thấy tên bot)\n"
       "- Response HTML không chứa dữ liệu bot",
       note="Nguồn: TC-CBF-012 (SEC-001, BR-06/FN-11; Pass dev + staging). Evidence: URL cuối + "
            "Network response body."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Trang campaign — bấm「トップに戻る」→ về /basic/overview, lần sau vào vẫn hiện modal campaign",
       FREE_IN + "\n- Đang ở trang campaign",
       "1. Ở trang campaign, bấm「トップに戻る」\n"
       "2. Quan sát URL đích\n"
       "3. Vào lại màn đổi LOA\n"
       "4. Quan sát có hiện lại modal/màn campaign không",
       "Bot Free trong campaign",
       "- Redirect về /basic/overview\n"
       "- Vào lại màn đổi LOA: VẪN hiển thị modal/màn campaign (khác với nút bắt đầu đổi LOA)",
       note=MT03 + "Nguồn: Change bot r94-r95 (TR=OK) + TC-CBF-013 (BR-06b/FN-10; Pass dev). "
            "Evidence: URL đích + ảnh lần vào lại."),

    tc("Modal promo & trang campaign", "FUNC-001", "Normal",
       "Trang campaign — bấm「アカウント入れ替えをはじめる」→ vào màn chọn phương thức, lần sau không hiện campaign nữa",
       FREE_IN + "\n- Đang ở trang campaign",
       "1. Ở trang campaign, bấm「アカウント入れ替えをはじめる」\n"
       "2. Quan sát màn hình và trạng thái 2 option\n"
       "3. Quay ra Dashboard rồi vào lại màn đổi LOA\n"
       "4. Quan sát có hiện lại màn campaign không",
       "Bot Free trong campaign",
       "- Vào màn chọn phương thức đổi LOA\n"
       "- Hiển thị banner campaign「LINE公式アカウント入れ替え機能　無料開放キャンペーン」\n"
       "- Option 1「すぐにLINE公式アカウントを入れ替える」ENABLE\n"
       "- Option 2「LINE公式アカウント入れ替え予約をする」DISABLE (bot Free không được đặt lịch)\n"
       "- Vào lại: KHÔNG hiện màn campaign nữa, vào thẳng màn chọn phương thức",
       note=MT03 + "Nguồn: Change bot r92-r93 (TR=OK) + TC-CBF-014 (Pass dev). "
            "⚠️ Improve xxx r4 (#37229 comment 3) ghi 'Check hiển thị banner campaign change bot → Không "
            "hiển thị nữa' → MT-03. Evidence: ảnh màn + ảnh 2 option."),

    tc("Modal promo & trang campaign", "PERM-003", "Abnormal",
       "Sửa param campaign_id/bot_id trên URL trang campaign sang giá trị của tenant khác → reject",
       FREE_IN + "\n- Biết campaign_id/bot_id thuộc tenant khác",
       "1. Mở trang campaign của bot mình, ghi lại URL đầy đủ\n"
       "2. Sửa param bot_id (và campaign_id nếu có) sang giá trị của tenant khác\n"
       "3. Enter và quan sát\n"
       "4. Xem response có chứa thông tin tenant khác không",
       "bot_id của tenant B",
       "- Bị reject (403 hoặc redirect), KHÔNG render trang campaign của tenant khác\n"
       "- Response KHÔNG chứa tên bot / countdown / thông tin plan của tenant B",
       note=MT03 + "Nguồn: TC-CBF-015 (PERM-003, MAP-PERM-03; Blocked cả 2 env). "
            "Evidence: Network response + ảnh trang."),

    tc("Modal promo & trang campaign", "UI-003", "Abnormal",
       "API lấy thông tin campaign lỗi → hiển thị lỗi rõ ràng, KHÔNG trắng màn",
       FREE_IN + "\n- Có DevTools để block request API campaign",
       "1. Mở DevTools tab Network, bật block URL của request lấy thông tin campaign\n"
       "2. Vào Dashboard / trang campaign\n"
       "3. Quan sát màn hình\n"
       "4. Kiểm tra Console",
       "Block request API campaign (trả 500 hoặc fail)",
       "- Hiển thị thông báo lỗi rõ ràng cho user (không phải trang trắng)\n"
       "- Các phần khác của Dashboard vẫn dùng được\n"
       "- KHÔNG hiển thị countdown với giá trị rác (NaN, undefined, số âm)",
       note=MT03 + "Nguồn: TC-CBF-108 (UI-003 + UIC-11, EP-01 campaign info load fail; Blocked cả 2 env). "
            "Evidence: ảnh màn lỗi + ảnh Network bị block."),

    tc("Modal promo & trang campaign", "PAY-LIMIT-001", "Normal",
       "Bot Free được đổi LOA NHIỀU LẦN trong tháng campaign",
       FREE_IN + "\n- Đã chuẩn bị 3 LOA mới hợp lệ (Messaging API + LINE Login cùng provider) để đổi lần lượt",
       "1. Thực hiện đổi LOA lần 1 cho bot Free đến khi hoàn tất\n"
       "2. Vào lại màn đổi LOA, thực hiện đổi LOA lần 2 với LOA khác\n"
       "3. Thực hiện đổi LOA lần n (lần 3)\n"
       "4. Sau mỗi lần, kiểm tra không bị chặn bởi giới hạn số lần",
       "3 LOA mới hợp lệ; bot Free vẫn trong tháng campaign",
       "- CẢ 3 lần đổi LOA đều thực hiện được, không bị chặn\n"
       "- Không có message giới hạn số lần đổi trong kỳ campaign\n"
       "- Sau mỗi lần, bot hoạt động với LOA mới nhất",
       env="PRODUCTION",
       note=MT03 + MT04 + "Nguồn: Change bot r96-r98 (TR=OK, 'Trong tháng campaign được change bot "
            "nhiều lần'). RULE-08 — đổi LOA chạm domain/webhook/job nên không kết luận từ staging. "
            "Evidence: 3 lần ảnh màn hoàn tất + query bots sau mỗi lần."),
]
