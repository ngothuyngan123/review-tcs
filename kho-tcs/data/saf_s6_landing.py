# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 15-17: quan hệ với QRコードアクション (landing QR),
thứ tự chạy action khi cả hai cùng cài, và trigger hiển thị ở màn chat 1:1.

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」:
r52-r56, r62, r93 (新規); r149-r152, r159, r205-r252 (既存 + ma trận 13 case);
r287-r291, r295 (unblock); r394-r407 (Bug Tester #33322, 03/2026).

⚠️ TOÀN BỘ nhóm 15-16 gắn với MÂU THUẪN MT-01/MT-02 — xem saf_conflicts.py.
"""
from _common import tc

LAND = ("- Bot đã liên kết LINE OA thật\n"
        "- Có 1 QRコードアクション (landing) đang bật, đã cài tin nhắn + action riêng\n"
        "- Cả 3 trang あいさつメッセージ đều đã cài tin nhắn + action riêng, đã bấm 保存")

S6 = [
    # ═══════════ 15. Ưu tiên với QRコードアクション ═══════════
    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Friend MỚI kết bạn qua landing chỉ dành cho bạn mới — nhận cả tin của landing và tin chào mừng",
       LAND + "\n- Landing đặt phạm vi CHỈ áp dụng cho bạn mới\n"
              "- Landing có bật tùy chọn kích hoạt あいさつメッセージ\n"
              "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Cài landing: tin nhắn「L-msg」+ action gắn tag TL, phạm vi = chỉ bạn mới, BẬT tùy chọn "
       "cho chạy あいさつメッセージ\n"
       "2. Trang 新規友だち用: tin nhắn「N-msg」+ action gắn tag TN, bấm 保存\n"
       "3. Dùng tài khoản LINE test quét QR của landing để kết bạn\n"
       "4. Đọc TOÀN BỘ tin nhắn nhận trên app LINE, ghi lại thứ tự\n"
       "5. Kiểm tra tag ở màn chi tiết friend",
       "Landing:「L-msg」+ tag TL (chỉ bạn mới, bật あいさつメッセージ) · "
       "新規友だち用:「N-msg」+ tag TN",
       "- Friend nhận CẢ「L-msg」và「N-msg」\n"
       "- Friend được gắn CẢ tag TL và tag TN\n"
       "- Ghi lại thứ tự 2 tin nhắn nhận được để đối chiếu MT-01",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r52 (『qrlanding kết bạn mới → send action_id, general_message; nếu "
            "bật tùy chọn thì send THÊM cấu hình của 新規友だち用』). NGƯỢC với job-spec.md:127 "
            "và :328 (『Landing QR override HOÀN TOÀN add_friend_setting』). CHỜ LEADER CHỐT — "
            "nếu chốt theo spec thì TC này dự kiến FAIL và phải raise bug.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Friend MỚI kết bạn qua landing áp dụng cho MỌI friend — vẫn nhận thêm tin chào mừng bạn mới",
       LAND + "\n- Landing đặt phạm vi áp dụng cho MỌI friend\n"
              "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Cài landing phạm vi = mọi friend, tin nhắn「L-msg」+ tag TL, bật tùy chọn あいさつメッセージ\n"
       "2. Trang 新規友だち用: tin nhắn「N-msg」+ tag TN, bấm 保存\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Đọc toàn bộ tin nhắn nhận và kiểm tra tag",
       "Landing phạm vi mọi friend · friend thuộc loại BẠN MỚI",
       "- Friend nhận「L-msg」\n"
       "- VÌ friend là bạn mới nên nhận THÊM「N-msg」và tag TN",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r53 (『qrlanding kết bạn all friend → send action_id, general_message; "
            "TH1 nếu friend là new friend thì send thêm cấu hình 新規友だち用』). CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Friend CŨ kết bạn lại qua landing — nhận thêm tin của trang 既存友だち用",
       LAND + "\n- Có tài khoản LINE test ĐÃ từng là bạn của bot",
       "1. Ở admin xóa follow của friend test để đưa về trạng thái bạn cũ\n"
       "2. Cài landing phạm vi mọi friend, tin nhắn「L-msg」, bật tùy chọn あいさつメッセージ, "
       "cho phép chạy nhiều lần\n"
       "3. Trang 既存友だち用: tin nhắn「O-msg」+ tag TO, bấm 保存\n"
       "4. Dùng tài khoản LINE test quét QR landing để kết bạn lại\n"
       "5. Đọc toàn bộ tin nhắn nhận và kiểm tra tag",
       "Friend thuộc loại BẠN CŨ, landing cho chạy nhiều lần",
       "- Friend nhận「L-msg」\n"
       "- Nhận THÊM「O-msg」và được gắn tag TO (cấu hình của trang 既存友だち用)",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r149 (『TH2 nếu friend là old friend → send thêm cấu hình 既存友だち用』). "
            "CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Landing chỉ cho chạy 1 lần — friend cũ kết bạn lại vẫn nhận tin của landing đó",
       LAND + "\n- Landing đặt số lần chạy = 1 lần\n"
              "- Có tài khoản LINE test đã từng là bạn của bot",
       "1. Cài landing với giới hạn chạy 1 lần, tin nhắn「L-msg」\n"
       "2. Đưa friend test về trạng thái bạn cũ\n"
       "3. Dùng tài khoản LINE test quét QR landing để kết bạn lại\n"
       "4. Đọc tin nhắn nhận được",
       "Landing giới hạn 1 lần",
       "- Friend VẪN nhận「L-msg」và action của landing đó",
       env="PRODUCTION",
       note="Nguồn: r150 (kết quả OK, cột Note ghi『từ spec cũ vẫn send nếu landing để =1』). "
            "⚠️ Đối chiếu job-spec.md:329 (『Landing QR đã action 2 lần (action_type=1) → CẢ landing "
            "lẫn add_friend_setting đều bị bỏ qua』) — cách diễn đạt 2 nguồn khác nhau, dễ hiểu "
            "nhầm. Liên quan MT-01.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Landing KHÔNG cài action — vẫn chạy action của trang あいさつメッセージ",
       LAND + "\n- Landing chỉ cài tin nhắn, KHÔNG cài action nào",
       "1. Cài landing chỉ có tin nhắn「L-msg」, không cài action\n"
       "2. Trang 新規友だち用 cài action gắn tag TN, bấm 保存\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Kiểm tra tin nhắn và tag của friend",
       "Landing không có action · 新規友だち用 có action gắn tag TN",
       "- Friend nhận「L-msg」\n"
       "- Friend VẪN được gắn tag TN (action của trang 新規友だち用 vẫn chạy)",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r55 (『Check khi landing không setting action → vẫn send action của "
            "setting add new』), r151, r290. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Landing KHÔNG cài tin nhắn — vẫn gửi tin nhắn của trang あいさつメッセージ",
       LAND + "\n- Landing chỉ cài action, KHÔNG cài tin nhắn",
       "1. Cài landing chỉ có action gắn tag TL, không nhập tin nhắn\n"
       "2. Trang 新規友だち用 cài tin nhắn「N-msg」, bấm 保存\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Đọc tin nhắn nhận được và kiểm tra tag",
       "Landing không có tin nhắn · 新規友だち用 có tin nhắn「N-msg」",
       "- Friend được gắn tag TL\n"
       "- Friend VẪN nhận「N-msg」(tin nhắn của trang 新規友だち用)",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r56 (『Check khi landing không setting msg → vẫn send msg của setting "
            "add new』), r152, r291. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-003", "Normal",
       "Friend đang block bot rồi quét landing — vào nhánh unblock, nhận thêm tin của ブロック解除時用",
       LAND + "\n- Có tài khoản LINE test đang BLOCK bot\n"
              "- Landing bật tùy chọn kích hoạt あいさつメッセージ, giới hạn chạy 1 lần",
       "1. Cài landing tin nhắn「L-msg」+ action, giới hạn 1 lần, bật tùy chọn あいさつメッセージ\n"
       "2. Trang ブロック解除時用 cài tin nhắn「U-msg」+ tag TU, bấm 保存\n"
       "3. Dùng tài khoản LINE test đang block bot: quét QR landing\n"
       "4. Đọc tin nhắn nhận được và kiểm tra tag\n"
       "5. Block lại rồi bỏ block lần 2 (KHÔNG quét QR) → đọc tin nhắn",
       "Landing giới hạn 1 lần/1 user",
       "- Lần 1: friend nhận CẢ「L-msg」và「U-msg」, được gắn tag TU\n"
       "- Lần 2 (bỏ block không quét QR): KHÔNG nhận tin nhắn và action của trang ブロック解除時用",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r287 (『chỉ send 1 lần/1 user … use_msg_unblock = 1 send thêm cấu "
            "hình unblock』) và r288 (『check khi unblock lần 2 (không quét qr) → không send cả "
            "msg, action ở màn setting-add-friend-unblock』). Bước 5 là điểm dễ gây tranh cãi: "
            "vì sao lần bỏ block thứ 2 lại KHÔNG chạy cấu hình unblock. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-003", "Normal",
       "Landing cho chạy nhiều lần — mỗi lần block → unblock đều chạy cấu hình ブロック解除時用",
       LAND + "\n- Landing đặt cho chạy NHIỀU lần\n"
              "- Có tài khoản LINE test đang block bot",
       "1. Cài landing cho chạy nhiều lần, bật tùy chọn あいさつメッセージ\n"
       "2. Trang ブロック解除時用 cài tin nhắn「U-msg」+ tag TU\n"
       "3. Friend bỏ block lần 1 → ghi lại tin nhận\n"
       "4. Friend block lại, chờ ~10 giây, bỏ block lần 2 → ghi lại tin nhận",
       "Landing cho chạy nhiều lần",
       "- Cả 2 lần bỏ block friend đều nhận「U-msg」và được gắn tag TU",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r289 (『khi landing để send nhiều lần → có call back block => "
            "unblock sẽ send … send thêm cấu hình unblock』). CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "MSG-001", "Normal",
       "Xóa follow rồi friend vào trạng thái block bot rồi quét landing — vẫn tính là bạn mới",
       LAND + "\n- Có tài khoản LINE test đã từng là bạn",
       "1. Ở admin xóa follow của friend test\n"
       "2. Trên app LINE: friend block bot\n"
       "3. Dùng tài khoản LINE test quét QR landing để kết bạn\n"
       "4. Đọc tin nhắn nhận được và kiểm tra tag\n"
       "5. Về admin kiểm tra bản ghi lượt click landing của friend đó",
       "Xóa follow → block → quét landing",
       "- Friend nhận tin nhắn + action của landing\n"
       "- Friend nhận THÊM tin nhắn + action của trang 新規友だち用 (được tính là BẠN MỚI)\n"
       "- Bản ghi lượt click landing đánh dấu friend này KHÔNG phải bạn cũ",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: r54 (『xóa follow => friend vào block bot => quét landing → send "
            "action_id, general_message; send thêm cấu hình add new; check bảng "
            "detail_landing_click: is_old_fried = 0』). Đã viết lại theo góc nhìn tester. "
            "CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "FUNC-004", "Boundary",
       "Landing giới hạn số lần chạy — lần cuối trong giới hạn và lần vượt giới hạn",
       LAND + "\n- Landing đặt giới hạn chạy N lần (VD 2 lần) trên 1 friend\n"
              "- Có tài khoản LINE test đã từng là bạn",
       "1. Cài landing giới hạn 2 lần, tin nhắn「L-msg」, bật tùy chọn あいさつメッセージ\n"
       "2. Trang 既存友だち用 cài tin nhắn「O-msg」+ tag TO\n"
       "3. Đưa friend test về trạng thái bạn cũ, quét QR landing lần 1 → ghi lại tin nhận\n"
       "4. Lặp lại lần 2 → ghi lại\n"
       "5. Lặp lại lần 3 (VƯỢT giới hạn) → ghi lại",
       "Giới hạn 2 lần; test ở lần 1, lần 2 (sát ngưỡng) và lần 3 (vượt ngưỡng)",
       "- Lần 1 và lần 2: friend nhận「L-msg」và「O-msg」\n"
       "- Lần 3: friend KHÔNG nhận「L-msg」nữa; ghi lại rõ có còn nhận「O-msg」của trang "
       "既存友だち用 hay không",
       env="PRODUCTION",
       note="⚠️ MT-01. TC do AI bổ sung theo RULE-01 (Boundary cho quan điểm ưu tiên Cao). Corpus "
            "chỉ có case 1 lần (r150, r287) và nhiều lần (r289), không có case sát/vượt ngưỡng. "
            "job-spec.md:329 nói khi landing đã đạt giới hạn thì CẢ HAI đều bị bỏ qua — điểm này "
            "chính là chỗ cần đo. CẦN LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "FUNC-DATE-001", "Abnormal",
       "Landing có giới hạn thời gian, quét NGOÀI khoảng — không chạy cả action landing lẫn chào mừng",
       LAND + "\n- Landing đặt giới hạn thời gian sử dụng (VD chỉ chạy từ 01/09 đến 30/09)\n"
              "- Thời điểm test nằm NGOÀI khoảng đó",
       "1. Cài landing có giới hạn thời gian, thời điểm test nằm ngoài khoảng\n"
       "2. Cả 3 trang あいさつメッセージ đều cài tin nhắn + action\n"
       "3. Dùng tài khoản LINE test quét QR landing để kết bạn\n"
       "4. Đọc tin nhắn nhận được và kiểm tra tag\n"
       "5. Lặp lại ở sát mốc: 1 phút TRƯỚC giờ bắt đầu và 1 phút SAU giờ kết thúc",
       "Ngoài khoảng thời gian: trước giờ bắt đầu 1 phút, sau giờ kết thúc 1 phút",
       "- Friend KHÔNG nhận action/tin nhắn của landing\n"
       "- Friend cũng KHÔNG nhận action/tin nhắn của trang あいさつメッセージ\n"
       "- Kết quả giống nhau ở cả 2 mốc sát ranh giới",
       env="PRODUCTION",
       note="⚠️ MT-08. Nguồn: r62, r159, r295 (『check khi setting Có sử dụng giới hạn thời gian và "
            "nằm ngoài khoảng thời gian đó → Không gửi action_id bảng landing và action/msg ở bảng "
            "add_friend_setting』). Spec FA-007 KHÔNG có bất kỳ mô tả nào về giới hạn thời gian. "
            "Bước 5 (mốc sát ranh giới) do AI bổ sung theo FUNC-DATE-001. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Ưu tiên với QRコードアクション", "STATE-DEP-001", "Normal",
       "Landing đang TẮT nhưng có bật tùy chọn kích hoạt あいさつメッセージ — cấu hình chào mừng vẫn chạy",
       LAND + "\n- Landing ở trạng thái TẮT\n"
              "- Landing có bật tùy chọn kích hoạt あいさつメッセージ",
       "1. Tắt landing nhưng giữ bật tùy chọn kích hoạt あいさつメッセージ\n"
       "2. Trang 新規友だち用 cài tin nhắn + action gắn tag TN\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Đọc tin nhắn nhận được và kiểm tra tag",
       "Landing TẮT + bật tùy chọn あいさつメッセージ",
       "- Friend KHÔNG nhận tin nhắn/action của landing (vì landing đang tắt)\n"
       "- Nhưng VẪN nhận tin nhắn + action của trang 新規友だち用 (được gắn tag TN)",
       env="PRODUCTION",
       note="⚠️ MT-02. Nguồn: r93 (『check khi setting ON/OFF chọn vào option \"あいさつメッセージを"
            "稼働させる\" → có gửi action add new friend khi qr đang OFF, và ở landing có chọn "
            "option send new friend』) và khối case 13 (r248-r252). Tùy chọn "
            "「あいさつメッセージを稼働させる」KHÔNG có trong spec FA-007. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    # ═══════════ 16. Thứ tự & loại action khi trùng landing ═══════════
    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Cả landing và あいさつメッセージ đều cài action ステップ配信 — chạy đúng thứ tự đã fix",
       LAND + "\n- Landing cài 1 action bắt đầu scenario SL\n"
              "- Trang 既存友だち用 cài 1 action bắt đầu scenario SO\n"
              "- Cả 2 đều KHÔNG cài tin nhắn",
       "1. Cài landing: 1 action bắt đầu scenario SL, không tin nhắn\n"
       "2. Trang 既存友だち用: 1 action bắt đầu scenario SO, không tin nhắn\n"
       "3. Đưa friend test về trạng thái bạn cũ, quét QR landing kết bạn\n"
       "4. Về admin mở màn ステップ配信 kiểm tra friend đang ở scenario nào\n"
       "5. Đọc tin nhắn friend nhận trên app LINE",
       "1 action scenario ở landing (SL) + 1 action scenario ở 既存友だち用 (SO)",
       "- Cấu hình あいさつメッセージ chạy TRƯỚC, landing chạy SAU\n"
       "- Kết quả cuối: friend nằm ở scenario của LANDING (SL), scenario SO bị bỏ qua\n"
       "- Friend nhận tin của scenario SL",
       env="PRODUCTION",
       note="⚠️ MT-01. Nguồn: khối r205 (nêu rõ cách fix:『Sửa lại thứ tự action của "
            "addFriendSetting TRƯỚC rồi đến action LandingQR để scenario lấy của LandingQR』) + "
            "r206-r208 (『send action của scenario landing trước』/『bỏ qua scen của old friend』). "
            "NGƯỢC với job-spec.md:127. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Cả 2 nơi cài 2 action ステップ配信 và CÓ tin nhắn — thứ tự tin nhắn với action không đảm bảo",
       LAND + "\n- Landing cài 2 action scenario + có tin nhắn\n"
              "- Trang 既存友だち用 cài 2 action scenario + có tin nhắn",
       "1. Cài landing: 2 action scenario + tin nhắn「L-msg」\n"
       "2. Trang 既存友だち用: 2 action scenario + tin nhắn「O-msg」\n"
       "3. Đưa friend test về trạng thái bạn cũ, quét QR landing kết bạn\n"
       "4. Ghi lại THỨ TỰ toàn bộ tin nhắn nhận trên app LINE (chụp màn hình)\n"
       "5. Kiểm tra friend đang ở scenario nào",
       "2 action scenario mỗi bên + 2 tin nhắn",
       "- Friend vào scenario thứ 2 của landing\n"
       "- Tin nhắn của trang 既存友だち用 gửi TRƯỚC, tin nhắn của landing gửi SAU\n"
       "- ⚠️ Thứ tự giữa tin nhắn độc lập và tin nhắn của scenario KHÔNG đảm bảo — chỉ ghi nhận, "
       "không coi là FAIL nếu scenario chen ngang",
       env="PRODUCTION",
       note="Nguồn: r210, r211 (『scenario không đảm bảo được thứ tự send msg trước, action sau; "
            "send msg của kết bạn trước => msg landing sau』, có ảnh chứng prnt.sc/PsHJDTvTEa4E). "
            "Đây là HẠN CHẾ ĐÃ BIẾT, không phải bug — cần Leader xác nhận vẫn giữ nguyên."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Landing KHÔNG có action scenario, あいさつメッセージ có — friend vào scenario của あいさつメッセージ",
       LAND + "\n- Landing KHÔNG cài action loại scenario\n"
              "- Trang 既存友だち用 cài 1 action bắt đầu scenario SO",
       "1. Cài landing không có action scenario\n"
       "2. Trang 既存友だち用 cài action bắt đầu scenario SO\n"
       "3. Đưa friend test về trạng thái bạn cũ, quét QR landing kết bạn\n"
       "4. Kiểm tra friend đang ở scenario nào",
       "Landing không scenario · 既存友だち用 có scenario SO",
       "- Friend được đưa vào scenario SO của trang 既存友だち用",
       env="PRODUCTION",
       note="Nguồn: r214, r215 (Case 3: 『Landing không có type scenario … → Send action scen của "
            "old friend』). Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại テンプレート ở cả 2 nơi — template của あいさつメッセージ gửi trước, landing sau",
       LAND + "\n- Landing cài action gửi template ML\n"
              "- Trang 既存友だち用 cài action gửi template MO",
       "1. Cài landing action gửi template ML\n"
       "2. Trang 既存友だち用 cài action gửi template MO\n"
       "3. Đưa friend test về trạng thái bạn cũ, quét QR landing kết bạn\n"
       "4. Chụp màn hình chat trên app LINE, ghi lại thứ tự\n"
       "5. Lặp lại với cấu hình 2 action template mỗi bên",
       "Case 1 action mỗi bên và case 2 action mỗi bên",
       "- Template của trang 既存友だち用 (MO) gửi TRƯỚC\n"
       "- Template của landing (ML) gửi SAU\n"
       "- Thứ tự giống nhau ở cả case 1 action và case 2 action",
       env="PRODUCTION",
       note="Nguồn: r216-r219 (Case 4: 『send của old friend send trước, landing send sau』). "
            "Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại テキスト ở cả 2 nơi — text của あいさつメッセージ gửi trước, landing sau",
       LAND + "\n- Landing cài action gửi text\n"
              "- Trang 既存友だち用 cài action gửi text",
       "1. Cài landing action text「L-text」\n"
       "2. Trang 既存友だち用 action text「O-text」\n"
       "3. Đưa friend test về bạn cũ, quét QR landing kết bạn\n"
       "4. Chụp màn hình chat, ghi lại thứ tự\n"
       "5. Lặp lại với 2 action text mỗi bên",
       "Case 1 action và case 2 action mỗi bên",
       "- 「O-text」(あいさつメッセージ) gửi trước, 「L-text」(landing) gửi sau",
       env="PRODUCTION",
       note="Nguồn: r220-r223 (Case 5). Liên quan MT-01. ⚠️ Tab「Ngần review」của cùng file ghi 2 "
            "câu hỏi treo:『Action text đang bị gửi sau multi action』và『Action text chưa có "
            "trigger send từ đâu』— cần Leader xác nhận đã fix chưa (MT-16)."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại リマインド ở cả 2 nơi — remind của あいさつメッセージ chạy trước, landing sau",
       LAND + "\n- Landing cài action remind\n"
              "- Trang 既存友だち用 cài action remind\n"
              "- Cả 2 nơi thử cả trường hợp có và không có tin nhắn độc lập",
       "1. Cài landing action remind RL\n"
       "2. Trang 既存友だち用 action remind RO\n"
       "3. Đưa friend test về bạn cũ, quét QR landing kết bạn\n"
       "4. Ghi lại thứ tự remind nhận được\n"
       "5. Lặp lại khi có thêm tin nhắn độc lập ở cả 2 nơi",
       "1 action và 2 action remind mỗi bên · có / không có tin nhắn độc lập",
       "- Remind của trang 既存友だち用 chạy TRƯỚC, remind của landing chạy SAU\n"
       "- ⚠️ Thứ tự giữa tin nhắn độc lập và action remind KHÔNG đảm bảo (giống scenario) — "
       "chỉ ghi nhận",
       env="PRODUCTION",
       note="Nguồn: r224-r228 (Case 6). Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "DATA-REF-001", "Normal",
       "Landing và あいさつメッセージ gắn CÙNG 1 tag — chỉ chạy 1 lần, không gắn 2 lần",
       LAND + "\n- Landing cài action gắn tag TX\n"
              "- Trang 既存友だち用 cũng cài action gắn CHÍNH tag TX đó",
       "1. Cài landing action gắn tag TX\n"
       "2. Trang 既存友だち用 cũng cài action gắn tag TX\n"
       "3. Đưa friend test về bạn cũ, quét QR landing kết bạn\n"
       "4. Mở màn chi tiết friend, đếm số lần tag TX xuất hiện\n"
       "5. Mở màn Quản lý thẻ, xem số người gắn tag TX tăng thêm bao nhiêu",
       "Cùng 1 tag TX ở cả 2 nơi",
       "- Friend chỉ được gắn tag TX 1 lần (không hiện 2 dòng tag trùng)\n"
       "- Bộ đếm số người gắn tag TX chỉ tăng 1",
       env="PRODUCTION",
       note="Nguồn: r229, r234 (『check setting landing + add friend cùng 1 tag xem có setting 2 "
            "action k → chỉ send 1 action』). Bước 5 do AI bổ sung theo DATA-COUNT-001."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại タグ có kèm tin nhắn độc lập — tin nhắn gửi trước action tag",
       LAND + "\n- Landing và trang 既存友だち用 đều cài action gắn tag + tin nhắn độc lập",
       "1. Cài landing: tin nhắn「L-msg」+ action gắn tag TL\n"
       "2. Trang 既存友だち用: tin nhắn「O-msg」+ action gắn tag TO\n"
       "3. Đưa friend test về bạn cũ, quét QR landing kết bạn\n"
       "4. Ghi lại thứ tự tin nhắn nhận và thời điểm tag được gắn",
       "Tin nhắn độc lập + action tag ở cả 2 nơi",
       "- Tin nhắn độc lập gửi TRƯỚC action tag\n"
       "- Cụm của trang 既存友だち用 chạy trước, cụm của landing chạy sau",
       env="PRODUCTION",
       note="Nguồn: r229-r233 (Case 7). Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại リッチメニュー ở cả 2 nơi — richmenu cuối cùng hiển thị là của landing",
       LAND + "\n- Landing cài action hiển thị richmenu RML\n"
              "- Trang 新規友だち用 cài action hiển thị richmenu RMN",
       "1. Cài landing action richmenu RML\n"
       "2. Trang 新規友だち用 action richmenu RMN\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Mở phòng chat với bot trên app LINE, xem richmenu đang hiển thị\n"
       "5. Lặp lại với 2 action richmenu mỗi bên",
       "1 action và 2 action richmenu mỗi bên",
       "- Richmenu hiển thị cuối cùng cho friend là richmenu của LANDING (RML)\n"
       "- Richmenu của trang 新規友だち用 bị ghi đè (chỉ 1 richmenu hiển thị tại 1 thời điểm)",
       env="PRODUCTION",
       note="Nguồn: r235-r239 (Case 8: 『send rich menu của landing trước』/『bỏ qua scen của old "
            "friend』— diễn đạt ở tab nguồn không rõ; expected viết theo nguyên tắc richmenu ghi đè). "
            "CẦN LEADER XÁC NHẬN.",
       spec="Đã hỏi leader"),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại ブックマーク — あいさつメッセージ chạy trước, landing chạy sau ghi đè",
       LAND + "\n- Landing cài action bookmark (gắn)\n"
              "- Trang 新規友だち用 cài action bookmark (xóa)",
       "1. Cài landing action bookmark = GẮN\n"
       "2. Trang 新規友だち用 action bookmark = XÓA\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Mở màn chi tiết friend, kiểm tra trạng thái bookmark",
       "Landing gắn bookmark · 新規友だち用 xóa bookmark",
       "- Cấu hình あいさつメッセージ chạy trước (xóa), landing chạy sau (gắn)\n"
       "- Kết quả cuối: friend ĐANG được gắn bookmark",
       env="PRODUCTION",
       note="Nguồn: r240, r241 (Case 9: 『chạy old friend trước, landing chạy sau => gắn "
            "bookmask』). Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "FRIEND-001", "Normal",
       "Action loại 友だち情報 ở cả 2 nơi — giá trị cuối cùng là của landing",
       LAND + "\n- Landing cài action ghi giá trị vào 1 mục friend info F\n"
              "- Trang 新規友だち用 cài action XÓA giá trị của chính mục F đó",
       "1. Cài landing action ghi F = 「gia tri landing」\n"
       "2. Trang 新規友だち用 action xóa giá trị F\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Mở màn chi tiết friend, đọc giá trị mục F",
       "Landing ghi giá trị · 新規友だち用 xóa giá trị · cùng mục F",
       "- Cấu hình あいさつメッセージ chạy trước (xóa), landing chạy sau (ghi)\n"
       "- Giá trị cuối cùng của mục F là「gia tri landing」",
       env="PRODUCTION",
       note="Nguồn: r242, r243 (Case 10 — cột kết quả mong đợi ở tab nguồn TRỐNG). Expected do AI "
            "viết theo quy tắc thứ tự đã chốt ở Case 9/11. CẦN LEADER XÁC NHẬN.",
       spec="Đã hỏi leader"),

    tc("Thứ tự & loại action khi trùng landing", "FUNC-SEQ-001", "Normal",
       "Action loại 対応ステータス ở cả 2 nơi — trạng thái cuối cùng là của landing",
       LAND + "\n- Landing cài action XÓA trạng thái xử lý\n"
              "- Trang 新規友だち用 cài action GẮN trạng thái xử lý ST",
       "1. Cài landing action xóa 対応ステータス\n"
       "2. Trang 新規友だち用 action gắn 対応ステータス = ST\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Mở màn chat 1:1, kiểm tra trạng thái xử lý của friend",
       "Landing xóa · 新規友だち用 gắn ST",
       "- Cấu hình あいさつメッセージ chạy trước (gắn ST), landing chạy sau (xóa)\n"
       "- Kết quả cuối: friend KHÔNG có trạng thái xử lý nào",
       env="PRODUCTION",
       note="Nguồn: r244, r245 (Case 11: 『chạy old friend trước, landing chạy sau => k gắn "
            "status』). Liên quan MT-01."),

    tc("Thứ tự & loại action khi trùng landing", "MSG-003", "Normal",
       "Action loại ブロック / ẩn friend ở cả 2 nơi — kiểm tra trạng thái cuối cùng của friend",
       LAND + "\n- Landing cài action block friend\n"
              "- Trang 新規友だち用 cài action ẩn friend",
       "1. Cài landing action block friend\n"
       "2. Trang 新規友だち用 action ẩn friend\n"
       "3. Dùng tài khoản LINE test (bạn mới) quét QR landing kết bạn\n"
       "4. Mở màn danh sách bạn bè và chat 1:1, kiểm tra trạng thái friend\n"
       "5. Kiểm tra friend còn nhận được tin nhắn từ bot không",
       "Landing block · 新規友だち用 ẩn",
       "- Ghi lại chính xác trạng thái cuối cùng của friend (block / ẩn / cả hai)\n"
       "- Trạng thái phải NHẤT QUÁN giữa màn danh sách bạn bè và màn chat 1:1\n"
       "- Nếu friend bị block thì các tin nhắn sau đó không gửi được và phải thấy ở màn 配信エラー",
       env="PRODUCTION",
       note="Nguồn: r246, r247 (Case 12 — cột kết quả mong đợi ở tab nguồn TRỐNG). Expected do AI "
            "viết theo RULE-07. CẦN LEADER CHỐT hành vi mong muốn.",
       spec="Đã hỏi leader"),

    # ═══════════ 17. Trigger hiển thị ở chat 1:1 ═══════════
    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Normal",
       "Bạn MỚI kết bạn — trigger ở chat 1:1 ghi 新規友だち用アクション",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang 新規友だち用 đã cài multi action\n"
       "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Cài multi action ở trang 新規友だち用, bấm 保存\n"
       "2. Dùng tài khoản LINE test quét QR kết bạn\n"
       "3. Về admin, mở chat 1:1 của friend đó\n"
       "4. Xem phần trigger hiển thị kèm multi action",
       "Friend mới, kết bạn bằng QR thường",
       "- Trigger hiển thị:「機能名 = 友だち追加時設定」và「詳細 = 新規友だち用アクション」",
       env="PRODUCTION",
       note="⚠️ MT-09. Nguồn: r404 (Bug Tester #33322, 03/2026). Spec FA-007 KHÔNG có bất kỳ mô tả "
            "nào về nhãn trigger hiển thị ở chat 1:1 — đề xuất bổ sung vào ui-spec/logic-spec.",
       spec="Spec không ghi"),

    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Normal",
       "Bạn CŨ kết bạn lại — trigger ở chat 1:1 phải ghi 既存友だち用アクション (bug #33322)",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang あいさつメッセージ đã cài multi action\n"
       "- Có tài khoản LINE test đã từng là bạn (đã xóa follow)",
       "1. Ở admin xóa follow của friend test\n"
       "2. Dùng tài khoản LINE test GỬI TIN NHẮN cho bot (kết bạn lại)\n"
       "3. Về admin mở chat 1:1 của friend đó\n"
       "4. Xem trigger hiển thị kèm multi action\n"
       "5. Lặp lại bằng đường click link item để kết bạn lại",
       "2 đường: friend nhắn tin · friend click link item",
       "- Trigger hiển thị:「機能名 = 友だち追加時設定」và「詳細 = 既存友だち用アクション」\n"
       "- TUYỆT ĐỐI không hiện「ブロック解除友だち用アクション」(đây chính là nội dung bug #33322)",
       env="PRODUCTION",
       note="⚠️ MT-09. Nguồn: r394-r395 (mô tả bug #33322: 『Text old friend hiện tại: "
            "ブロック解除友だち用アクション — Expect: 既存友だち用アクション』) và r397, r398 (kết quả "
            "OK STEP). Đây là TC REGRESSION cho bug đã fix."),

    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Normal",
       "Friend bỏ block — trigger ở chat 1:1 ghi ブロック解除友だち用アクション",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang あいさつメッセージ đã cài multi action\n"
       "- Có tài khoản LINE test đang block bot",
       "1. Dùng tài khoản LINE test đang block bot\n"
       "2. Thực hiện lần lượt 3 đường: quét QR kết bạn · bấm bỏ block trên app LINE · "
       "click link form dẫn tới kết bạn\n"
       "3. Sau mỗi đường, về admin mở chat 1:1 xem trigger",
       "3 đường vào: quét QR · bỏ block trên app · click link form",
       "- Cả 3 đường đều hiển thị「機能名 = 友だち追加時設定」và「詳細 = ブロック解除友だち用アクション」",
       env="PRODUCTION",
       note="⚠️ MT-09. Nguồn: r400, r401, r402 (kết quả OK STEP). Gộp 3 đường vì cùng 1 kết quả."),

    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Normal",
       "Kết bạn qua QRコードアクション — trigger ghi QRコードアクション / URL読み込み",
       "- Bot đã liên kết LINE OA thật\n"
       "- Có landing QR (loại cho mọi friend và loại chỉ bạn mới)\n"
       "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Dùng tài khoản LINE test quét QR của landing loại MỌI FRIEND để kết bạn\n"
       "2. Về admin mở chat 1:1 xem trigger\n"
       "3. Lặp lại với tài khoản test khác, quét QR của landing loại CHỈ BẠN MỚI",
       "2 loại landing: mọi friend · chỉ bạn mới",
       "- Cả 2 trường hợp hiển thị「機能名 = QRコードアクション」và「詳細 = URL読み込み」\n"
       "- KHÔNG hiện「友だち追加時設定」cho phần action đến từ landing",
       env="PRODUCTION",
       note="⚠️ MT-09. Nguồn: r406, r407 (kết quả OK STEP)."),

    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Abnormal",
       "Bot xóa follow, friend quét QR kết bạn lại — chưa tính là kết bạn, không có trigger",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang あいさつメッセージ đã cài multi action\n"
       "- Có tài khoản LINE test đã từng là bạn",
       "1. Ở admin xóa follow của friend test\n"
       "2. Dùng tài khoản LINE test quét QR kết bạn lại\n"
       "3. Về admin mở chat 1:1 xem trigger và action",
       "Xóa follow rồi quét QR kết bạn lại",
       "- KHÔNG hiển thị trigger nào và KHÔNG chạy action nào",
       env="PRODUCTION",
       note="⚠️ Nguồn: r396 (『Hiện tại trên step chưa tính là kết bạn: ko có trigger + ko có "
            "action』, kết quả OK STEP). Đây là hành vi ĐANG CÓ, không rõ có phải mong muốn không "
            "— dòng chữ『Hiện tại』cho thấy chính người test cũng nghi ngờ. CẦN LEADER CHỐT "
            "(MT-17): đúng ra friend quét QR kết bạn lại sau khi bị xóa follow PHẢI được coi là "
            "bạn mới và chạy cấu hình 新規友だち用 (đối chiếu r54 nói is_old_friend = 0).",
       spec="Đã hỏi leader"),

    tc("Trigger hiển thị ở chat 1:1", "OUT-TRUTH-001", "Abnormal",
       "Bot xóa follow, friend quét QR có tích tùy chọn action bạn cũ — trigger nào hiển thị?",
       "- Bot đã liên kết LINE OA thật\n"
       "- Có landing QR bật tùy chọn chạy action cho bạn cũ\n"
       "- Có tài khoản LINE test đã từng là bạn (đã xóa follow)",
       "1. Cài landing bật tùy chọn chạy action cho bạn cũ\n"
       "2. Ở admin xóa follow của friend test\n"
       "3. Dùng tài khoản LINE test quét QR landing đó\n"
       "4. Về admin mở chat 1:1 xem trigger",
       "Landing có tích tùy chọn action bạn cũ",
       "- Trigger hiển thị:「機能名 = QRコードアクション」và「詳細 = URL読み込み」",
       env="PRODUCTION",
       note="⚠️ Nguồn: r399 — kết quả thực thi ở tab nguồn là **Pending** (chưa test xong). "
            "Giữ TC nguyên trạng, đánh dấu CHƯA CÓ BẰNG CHỨNG. CẦN LEADER CHỐT (MT-18).",
       spec="Đã hỏi leader"),
]
