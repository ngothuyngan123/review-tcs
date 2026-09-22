# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ ĐANG CHỜ QUYẾT ĐỊNH của Leader (2026-09-12).

Nguồn đã gộp và niên đại (xem chi tiết ở khoá `sources` trong build.py):
• 15.3 TCsLine_ChangeBot → tab「Change bot」(317 dòng — 3 đợt chồng lên nhau: #34632 04/2026,
  #36420 get-old-friend, #37744 07/2026) ·「[AI] TCs_change_bot_v2」(116 TC, 07-08/2026,
  có kết quả chạy cả dev + staging) ·「Improve xxx」(#37229 06/2026, 8 dòng feedback text)
• TCsLine_Bill tiền → tab「change_bot」(11/2023 — bộ TC GỐC, ~2,8 năm tuổi)
• TCsLine_AddBot → tab「Testcase」khối change bot (r135-r136, r227-r252, r276-r344, r473)

⚠️ CẢNH BÁO NIÊN ĐẠI: 3 nguồn mới nhất (「Change bot」#37744 7/2026 ·「Improve xxx」6/2026 ·
「[AI] TCs_change_bot_v2」7-8/2026) CÁCH NHAU CHỈ 1-2 THÁNG. Với các mâu thuẫn giữa chúng
(MT-03, MT-05, MT-13, MT-14, MT-15) quy tắc "ưu tiên TC mới nhất" là CĂN CỨ YẾU — lý do
thực sự chọn bản [AI] v2 làm bản viết TC là vì nó chi tiết hơn (có SPEC ID / BR / kết quả
chạy trên cả 2 môi trường), KHÔNG phải vì nó mới hơn.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "KIẾN TRÚC BẢN GHI BOT — đổi LOA là UPDATE tại chỗ vào bot_id CŨ, hay TẠO bản ghi bots MỚI? "
     "Phải chốt TRƯỚC vì ảnh hưởng quyền Staff, mọi khóa ngoại, báo cáo và bill tiền",
     "Bộ TC GỐC (TCsLine_Bill tiền/change_bot r20-r22, 11/2023, TR=OK + stg=OK):\n"
     "• r20: quét QR → 'tạo 1 bản ghi ở bảng bot có cột `id_bot_change` = id bot định change'\n"
     "• r22: 'các thông tin của bot MỚI sẽ UPDATE VÀO ID CỦA BOT CŨ' — liệt kê đủ 9 cột: line_id, "
     "view_name, bot_image, url_add_friend, liff_app_id (エルメ流入アクション用LIFF), liff_app_id_booking "
     "(エルメ各種フォーム用LIFF), liff_callback_unique, channel_id, channel_secret\n"
     "⇒ bot_id KHÔNG đổi.\n\n"
     "Bộ TC 2026 (Change bot r155 · r165 · r292 · r312, TR=OK + stg=OK):\n"
     "• r155/r292: bấm tạo QR → 'tạo thêm bản ghi MỚI bảng bots (is_delete = 2); bảng bot_contract và "
     "bot_slots KHÔNG thêm bản ghi mới'\n"
     "• r165/r312: kết nối thành công → 'bảng bots: update is_delete = 0; THÊM bản ghi bảng bot_contract "
     "và bot_slots map với bot VỪA TẠO'\n"
     "• r163/r166/r310/r313: thất bại → 'XÓA bản ghi bảng bots đã tạo trước đó'\n"
     "⇒ bot_id ĐỔI sang bản ghi mới.",
     "spec-features/admin/bot-edit/db/db-mapping.md:51 — chỉ khai báo cột "
     "`id_bot_change | int(11) | NULL | ID bot thay thế (LOA入れ替え) | EP-08`, KHÔNG nói cơ chế.\n"
     "spec-features/admin/bot-edit/db/db-mapping.md:358-366 (§4.4 SCR-BE-03) — chỉ 2 dòng mapping: "
     "`bots.id`, `bots.view_name` (Direct) và `bot_slots.id` (truyền qua URL param). KHÔNG có "
     "`is_delete`, KHÔNG có `bot_contract`, KHÔNG mô tả vòng đời bản ghi.\n"
     "spec-features/admin/bot-edit/web/api-spec.md:382-400 (EP-08) — chỉ là GET trả view "
     "`admin.bots.bot_add_v3`, KHÔNG có endpoint ghi dữ liệu nào.\n"
     "⇒ Spec KHÔNG trả lời được câu hỏi này.",
     "Hai cơ chế cho kết quả NGƯỢC nhau ở mọi chỗ tham chiếu bot_id: nếu TẠO BẢN GHI MỚI thì "
     "(a) quyền Staff map theo bot_id cũ có nguy cơ mất (xem MT-02 và TC-CBF-064), "
     "(b) bot_contract/bot_slots phải tạo lại → ảnh hưởng hợp đồng và bill tiền, "
     "(c) mọi bảng còn trỏ bot_id cũ thành dữ liệu mồ côi. Nếu UPDATE TẠI CHỖ thì ngược lại: "
     "khóa ngoại an toàn nhưng không có đường truy vết LOA nào từng gắn với bot. "
     "Ngoài ra cột `id_bot_change` tồn tại trong schema gợi ý cơ chế CŨ vẫn còn trong code → "
     "có thể đang chạy SONG SONG 2 cơ chế (RULE-09).",
     "Toàn bộ nhóm 7 (Quét QR & kiểm tra kết nối) · nhóm 8 (Tiến trình & hoàn tất) · "
     "nhóm 5 TC webhook tạo bản ghi · TC-CBF-064 (quyền Staff sau swap) · TC nhóm 14 về cột legacy",
     "",
     "Chốt xong phải: ① ghi rõ cơ chế nào đang chạy trên PRODUCTION và cột `id_bot_change` còn dùng "
     "hay đã chết; ② viết lại db-mapping.md §4.4 với vòng đời bản ghi bots (is_delete 2 → 0 → xóa) "
     "và quan hệ bot_contract/bot_slots; ③ nếu là TẠO MỚI thì bổ sung TC kiểm quyền Staff + hợp đồng "
     "+ dữ liệu mồ côi theo bot_id cũ."],

    ["MT-02", "CAO", W,
     "QUYỀN STAFF với màn đổi LOA — 3 nguồn nói 3 kiểu, trong đó 1 nguồn tự ghi nhận là KHÁC expected",
     "Nguồn A — Change bot r224-r229 (04/2026):\n"
     "• Staff KHÔNG được cấp quyền: 'Không được phép access từ menu' (thường + favourite); vào URL "
     "trực tiếp → 'Báo lỗi và quay lại màn hình home /basic/overview'\n"
     "• Staff ĐƯỢC cấp quyền: cả 3 vai trò 副管理人 · 運用者 · サポート → 'Được access từ menu và "
     "thao tác change bot BÌNH THƯỜNG'\n\n"
     "Nguồn B — AddBot/Testcase r342-r344 (main case, TR=OK step):\n"
     "• expected ghi '副管理人: Không được chang bot', '運用者: ko có quyền', 'サポート: ko có quyền'\n"
     "• NHƯNG cùng ô ghi nhận thực tế: '**Account staff VẪN thao tác change bot bt**'\n"
     "• kèm comment của tester: 'Check lại TCs này, c thấy account staff vẫn change đc? => Confirm lại a Tư'\n"
     "⇒ nguồn này TỰ ghi nhận expected ≠ thực tế và CHƯA được trả lời.\n\n"
     "Nguồn C — [AI] TCs_change_bot_v2 TC-CBF-092/093/099 (07-08/2026, Pass trên dev):\n"
     "• 'Staff KHÔNG thấy menu tính năng thay đổi bot trong sidebar' (BR-45)\n"
     "• 'Staff gọi thẳng API bất kỳ endpoint bot-swap (bypass UI) → 403'\n"
     "• 'Staff cố gọi thẳng EP-10 DELETE reservation qua devtools → 403'",
     "spec-features/admin/index.md:48 — FA-038 chỉ ghi 'Gồm cả trang LOA入れ替え', không có bảng quyền.\n"
     "spec-features/admin/bot-edit/feature-spec.md:251-263 (§2.3 SCR-BE-03) — luồng EP-08 chỉ có 3 bước "
     "(decode id → redirect nếu plan_type=2 → render view), KHÔNG có check quyền Staff nào.\n"
     "spec-features/admin/bot-edit/web/api-spec.md:382-400 (EP-08) — middleware chỉ ghi "
     "`web, NotifyChatworkRequestTimeSlow`, KHÔNG có middleware phân quyền.\n"
     "⇒ Spec KHÔNG có ràng buộc quyền Staff cho màn này.",
     "Đổi LOA là thao tác KHÔNG HOÀN TÁC ĐƯỢC, xóa toàn bộ dữ liệu friend của LOA cũ ở ~35 bảng. "
     "Nếu thực tế Staff làm được (nguồn B ghi nhận) mà lẽ ra không được (nguồn C + expected của nguồn B) "
     "thì đây là LỖ HỔNG PHÂN QUYỀN NẶNG đã tồn tại ít nhất từ thời điểm nguồn B được viết và CHƯA ai "
     "trả lời. Ngược lại nếu nguồn A đúng (Staff được cấp quyền thì thao tác được) thì nguồn C sai và "
     "BR-45 phải sửa. Thêm nữa: spec không có middleware phân quyền cho EP-08 nghiêng về phía "
     "'không chặn ở tầng server' — đúng với ghi nhận thực tế của nguồn B.",
     "Nhóm 13 toàn bộ (Phân quyền & bảo mật) · nhóm 3 TC Staff truy cập URL · nhóm 9 TC Staff gọi API "
     "xóa đặt lịch · TC-CBF-064 (Staff sau swap)",
     "",
     "Chốt xong phải: ① xác định trên PRODUCTION Staff 3 vai trò có thao tác đổi LOA được hay không "
     "(test thật, không suy từ spec); ② nếu Staff làm được mà không nên → RAISE BUG phân quyền ngay, "
     "rà cả tầng API không chỉ UI; ③ bổ sung bảng Access Control vào bot-edit/web/api-spec.md cho EP-08 "
     "và các endpoint mới; ④ trả lời comment treo ở AddBot/Testcase r342."],

    ["MT-03", "CAO", W,
     "CAMPAIGN「1ヶ月無料開放」— còn dùng hay KH đã BỎ? Ảnh hưởng ~18 TC nhóm 2 + nhóm 1",
     "Nguồn A — Change bot r83-r100 (04/2026, TR=OK): campaign là tính năng CHÍNH của đợt này. "
     "Tab Info r2 ghi nội dung đợt 04/2026: 'Improve màn hình change bot: Tách riêng ra 1 menu mới; "
     "THÊM TÍNH NĂNG CAMPAIGN trong 1 tháng đầu tiên với bot free; Thêm tính năng đặt hẹn change bot'. "
     "TCs gồm: modal suggest bot free (r83) · màn campaign + countdown realtime (r88-r90) · "
     "banner campaign (r92) · bot free change nhiều lần trong tháng campaign (r96-r98) · "
     "hết campaign thì disable 2 button (r99-r100).\n\n"
     "Nguồn B — Improve xxx r4 (#37229, 06/2026, OK staging): 'Comment 3: Check hiển thị banner campaign "
     "change bot → **Không hiển thị nữa**'.\n\n"
     "Nguồn C — [AI] v2 TC-CBF-001/005/006 (07-08/2026, Skip cả dev + staging). Tester ghi nguyên văn: "
     "'modal SCR-01 đáng lẽ hiển thị ở MỌI màn hình khi campaign active, NHƯNG **khách hàng đã BỎ, "
     "không dùng tính năng này nữa → feature đã ngưng**, không còn active để hiển thị trên môi trường. "
     "Đây là lý do dựng đủ điều kiện (Free + created_at<30 + campaign active) mà modal vẫn không hiện — "
     "KHÔNG phải bug, KHÔNG phải test-gap, mà tính năng đã ngưng dùng.'\n\n"
     "NHƯNG cùng bộ [AI] v2: TC-CBF-016 ('State 1: Campaign active + BOT Free → Option 2 khoá bằng overlay "
     "xám + icon khoá') và TC-CBF-020/027 đều **Pass trên CẢ dev + staging** ⇒ LOGIC campaign VẪN CÒN "
     "TRONG CODE, chỉ phần modal promo (SCR-01/SCR-02) là không dùng.",
     "Spec KHÔNG nhắc campaign ở bất kỳ file nào của bot-edit (feature-spec.md · ui-spec.md · "
     "api-spec.md · db-mapping.md). Màn SCR-BE-03 trong spec là landing page marketing 3 block "
     "(ui-spec.md:208-240), không có campaign / countdown / banner.\n"
     "⇒ Spec không biết tính năng campaign tồn tại (xem MT-12).",
     "3 nguồn cách nhau 2-4 tháng và nói 3 mức độ khác nhau: CÓ (04/2026) → BỎ BANNER (06/2026) → "
     "NGƯNG HẲN (07-08/2026). Vì niên đại gần, quy tắc 'ưu tiên TC mới nhất' là CĂN CỨ YẾU. "
     "Vấn đề thực sự: phần nào đã bị XÓA KHỎI CODE và phần nào chỉ TẮT DỮ LIỆU campaign? "
     "Bằng chứng TC-CBF-016/020/027 Pass cho thấy nhánh 'campaign active + bot Free' vẫn chạy được khi "
     "có dữ liệu campaign ⇒ nếu chỉ tắt dữ liệu thì mọi TC campaign vẫn hợp lệ và phải giữ; "
     "nếu đã xóa code thì ~18 TC phải loại khỏi kho.",
     "Nhóm 2 toàn bộ (18 TC) · nhóm 1 TC bot Free trong/ngoài 1 tháng · nhóm 3 TC State 1 + banner × · "
     "nhóm 12 TC đổi LOA ở 3 gói",
     "",
     "Chốt xong phải: ① xác định rõ 3 mức — code campaign còn/đã xóa · dữ liệu campaign có bản ghi active "
     "nào trên production không · banner/modal có bị xóa khỏi view không; ② nếu code còn mà dữ liệu tắt → "
     "GIỮ TC campaign, ghi rõ tiền điều kiện 'phải seed bản ghi campaign active'; ③ nếu code đã xóa → "
     "loại ~18 TC và ghi vào `excluded`; ④ làm rõ luôn MT-04 vì 2 mâu thuẫn này dính nhau."],

    ["MT-04", "CAO", W,
     "BOT FREE có được đổi LOA hay không — spec nói redirect home, TCs 04/2026 nói được trong 1 tháng",
     "Nguồn A — AddBot/Testcase r135 (TR=OK, stg=OK, step=OK): 'Change bot type free: vào màn hình "
     "admin home, chọn tab 接続済 → bot フリー (plan_type=2) → nhấn button 接続設定 → **KHÔNG CÓ chức năng "
     "changer bot**'. AddBot/Testcase r136: 'bot trả phí plan_type=1 thì CÓ chức năng changer bot'.\n"
     "AddBot/Bug Logic r28 (**Not fix**, OK): 'bot free chưa có button change bot' → ghi chú 'để hỏi lại "
     "chị Quyên / bot trả phí thì được changer bot plan_type=1'.\n\n"
     "Nguồn B — Change bot r84-r100 (04/2026, TR=OK + step=OK) chia bot Free thành 3 nhóm:\n"
     "• bot free CŨ tạo trước 2021-07-01 → vào được màn nhưng 'Bị disable phần select change bot' (r84-r86)\n"
     "• bot free tạo sau 2021-07-01 và TRONG 1 tháng → 'Vào màn hình change bot sẽ hiển thị campaign' + "
     "được change (r88-r90, r96-r98)\n"
     "• bot free ĐÃ QUÁ 1 tháng → 'Bị disable cả 2 button type chọn change bot' (r91, r99)\n\n"
     "Nguồn C — [AI] v2 TC-CBF-002/112: bot Free NGOÀI 30 ngày + URL cũ → 'redirect về admin/home "
     "(hành vi GIỮ NGUYÊN của EP-08)'. ⚠️ NHƯNG cả 2 TC đều **Blocked trên cả dev + staging**, ghi chú dev: "
     "'set created_at>30 ngày trên dev VẪN VÀO SCR-03, KHÔNG reproduce redirect. Trigger opaque.'",
     "spec-features/admin/bot-edit/feature-spec.md:258-262 (§2.3, luồng EP-08) — bước 2 ghi rõ: "
     "'Nếu plan_type = 2 (free) → **redirect về /admin/home**'.\n"
     "spec-features/admin/bot-edit/web/logic-spec.md:25 — `adminChangeNewBot()` : 'Load trang thay thế LOA "
     "— **redirect nếu bot free**'.\n"
     "spec-features/admin/bot-edit/db/db-mapping.md:361 — 'Redirect nếu `plan_type = 2` (free)'.\n"
     "⇒ Spec (quét 2026-03-24) nói bot Free KHÔNG vào được màn, KHỚP nguồn A (2024-2026).",
     "3 trạng thái khác nhau theo mốc thời gian: trước 04/2026 bot Free bị redirect (spec + nguồn A khớp "
     "nhau) → 04/2026 mở cho bot Free trong 1 tháng campaign (nguồn B) → 07-08/2026 nguồn C nói vẫn "
     "redirect nhưng KHÔNG REPRODUCE ĐƯỢC, dev ghi 'trigger opaque'. Việc dev không dựng được nhánh "
     "redirect là RISK riêng: hoặc điều kiện redirect đã đổi mà không ai biết, hoặc nhánh đó đã chết. "
     "Mâu thuẫn này dính chặt MT-03: nếu campaign đã ngưng thì điều kiện 'bot Free trong 1 tháng' còn "
     "nghĩa gì không?",
     "Nhóm 1 (7 TC về điều kiện gói) · nhóm 2 toàn bộ · nhóm 3 TC State 1 + bot Free chọn option 2 · "
     "nhóm 12 TC đổi LOA ở 3 gói",
     "",
     "Chốt xong phải: ① test thật trên PRODUCTION với 3 loại bot Free (tạo trước 2021-07-01 · trong "
     "1 tháng · quá 1 tháng) và ghi lại hành vi; ② làm rõ 'trigger opaque' mà dev không dựng được — "
     "điều kiện redirect thực tế là gì; ③ sửa feature-spec.md §2.3 bước 2 + logic-spec.md:25 + "
     "db-mapping.md:361 theo kết luận; ④ nếu mốc 2021-07-01 còn hiệu lực thì ghi vào spec (hiện KHÔNG có "
     "ở bất kỳ file spec nào)."],

    ["MT-05", "TRUNG BÌNH", W,
     "WEBHOOK — có MÀN RIÊNG bắt user tick checkbox, hay hệ thống TỰ CHECK ở bước nhập thông tin?",
     "Nguồn A — Change bot r148-r156 (#34632 step 4 màn 8) và r284-r293 (#37744 màn 2): có MÀN WEBHOOK "
     "RIÊNG với:\n"
     "• checkbox「Webhookをオンに設定した」, chưa tick thì disable nút next (r148)\n"
     "• khối「発行されたWebhook URL」+ nút「コピー」→ message「Webhook URLをコピーしました。」(r287, r291)\n"
     "• webhook ON → cập nhật webhook URL bên LINE + tạo 2 LIFF app + tạo bản ghi bots is_delete=2 (r155, r292)\n"
     "• webhook OFF → lỗi「Webhookをオンにして下さい。既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」"
     "(r156, r293 — cả 2 TR=OK)\n\n"
     "Nguồn B — [AI] v2 TC-CBF-035 (BR-16, QA-spec-013 CONFIRMED; Blocked cả 2 env vì ENV-HOOK "
     "'webhook chỉ nhận đầy đủ tín hiệu ở production'): 'Webhook chưa bật trên LINE Developer Console → "
     "**hệ thống TỰ ĐỘNG CHECK**, chặn bằng toast lỗi' — nằm ở màn SCR-04 (nhập thông tin), KHÔNG có màn "
     "webhook riêng trong danh sách SCR-01…SCR-10.",
     "spec-features/admin/bot-edit/web/api-spec.md:375-379 (EP-07 response) — có ĐÚNG text lỗi của nguồn A: "
     "`200 | success: false, flagError: 1 | 'Webhookをオンにして下さい。既にオンの場合は、一度オフにしてから"
     "再度オンに変更して下さい。' | Bot không tồn tại, webhook tắt, hoặc webhook URL sai`.\n"
     "⇒ Spec KHỚP nguồn A ở phần message lỗi, nhưng EP-07 là endpoint của màn LOA接続設定 (kiểm tra kết nối), "
     "KHÔNG phải của wizard đổi LOA. Spec không mô tả bước webhook trong wizard.",
     "Niên đại 2 nguồn GẦN NHAU (#37744 tháng 7/2026 vs [AI] v2 tháng 7-8/2026) nên không thể dùng quy tắc "
     "'TC mới nhất thắng'. Khác biệt không chỉ là 1 màn: nó đổi cả (a) số bước của wizard, (b) thời điểm tạo "
     "bản ghi bots is_delete=2 và 2 LIFF app (ở bước webhook theo nguồn A, hay ở bước xác nhận theo nguồn B), "
     "(c) có hay không tính năng copy Webhook URL — tính năng MỚI ở #37744 mà KHÔNG nguồn nào đã chạy.",
     "Nhóm 5 toàn bộ (9 TC) · nhóm 4 TC webhook tự check · nhóm 6 TC rẽ nhánh sau xác nhận",
     "",
     "Chốt xong phải: ① xác định wizard trên PRODUCTION có mấy màn và webhook ở đâu; ② nếu có màn webhook "
     "riêng thì GIỮ nhóm 5 và bổ sung TC copy Webhook URL vào bộ chạy (hiện chưa nguồn nào chạy); "
     "③ nếu tự check thì loại nhóm 5, chuyển TC webhook về nhóm 4; ④ bổ sung bước webhook vào "
     "bot-edit/web/api-spec.md (hiện chỉ có EP-07 của màn khác)."],

    ["MT-06", "TRUNG BÌNH", W,
     "TEXT THÔNG BÁO LỖI khi Channel ID/secret sai — 2 bộ text hoàn toàn khác nhau",
     "Bộ CŨ — TCsLine_Bill tiền/change_bot r11 + r17 (11/2023, TR=OK + stg=OK): "
     "「入力した情報が間違っています。WEBブラウザの自動翻訳機能が原因の可能性がございますので、"
     "自動翻訳を無効にした状態でお試しください。」(gợi ý nguyên nhân là chức năng tự dịch của trình duyệt).\n"
     "Bộ CŨ cũng dùng cơ chế text cảnh báo thay vì disable nút: r8-r9 'nhập cả 2 → ẩn text "
     "「※未記入の項目があります」/ nhập 1 trong 2 hoặc không nhập → hiển thị text「※未記入の項目があります」'; "
     "r12-r13 '「※未確認の項目があります」'.\n\n"
     "Bộ MỚI — Change bot r129/r135 (#34632) + r265/r271 (#37744), tất cả TR=OK: "
     "「入力した情報に誤りがありますので、入力情報を再度ご確認ください。ご不明な場合は、サポート窓口までお問い合わせください。」"
     "+ bấm「サポート窓口」mở tab mới https://page.line.me/770yphxr?openQrModal=true.\n"
     "Bộ MỚI dùng cơ chế DISABLE nút (r125/r132/r261/r268: 'không nhập → disable nút next'), "
     "khớp [AI] v2 TC-CBF-029/030 (Pass cả 2 env).\n\n"
     "Thêm 1 text riêng cho trường hợp trùng channel: 「このLINE公式アカウントは、すでにL Messageに接続されて"
     "います。ご不明な場合は、サポート窓口までお問い合わせください」+ link https://step.lme.jp/check-user "
     "(Change bot r127/r263).",
     "Spec KHÔNG ghi text lỗi nào cho wizard đổi LOA. "
     "spec-features/admin/bot-edit/web/api-spec.md chỉ có text lỗi của EP-07 (webhook) — xem MT-05.\n"
     "⇒ Spec không có cơ sở đối chiếu.",
     "Cách nhau ~2,5 năm nên ở đây quy tắc 'ưu tiên TC mới nhất' là CĂN CỨ MẠNH — bộ mới thắng. "
     "Ghi vào bảng này để TRUY VẾT: nếu có ticket cũ tham chiếu text 「自動翻訳機能が原因…」thì biết đó là "
     "bản đã bị thay. Đồng thời phải xác nhận 2 link hỗ trợ (page.line.me/770yphxr và step.lme.jp/check-user) "
     "còn sống — đây là URL marketing, dễ đổi mà không ai cập nhật TC (RULE-05).",
     "Nhóm 4: TC Messaging API sai · TC LINE Login sai · TC channel trùng bot đang hoạt động",
     "",
     "Chốt xong phải: ① xác nhận text lỗi hiện hành trên PRODUCTION (chụp ảnh); ② kiểm 2 link hỗ trợ còn "
     "sống; ③ ghi bộ text lỗi vào api-spec.md của các endpoint mới để TC sau không phải đoán."],

    ["MT-07", "CAO", W,
     "BẢNG `event_step_time` — đổi LOA có XÓA bản ghi nhắc lịch của friend LOA cũ hay KHÔNG?",
     "Nguồn A — Change bot, 5 dòng đều TR=OK + stg=OK + step=OK, nói XÓA:\n"
     "• r29 (Form remind): 'check db: - xóa event_step_time'\n"
     "• r51 (Lesson remind): 'check db: - xóa event_step_time'\n"
     "• r54 (Salon remind): 'check db: => xóa event_step_time'\n"
     "• r57 (Event remind): 'check db: => xóa event_step_time'\n"
     "• r59 (màn Remind): '- event_step_time => xóa bản ghi'\n\n"
     "Nguồn B — TCsLine_Bill tiền/change_bot r47 (11/2023), trong danh sách 14 bảng bị xóa: "
     "'11. event_step_time → **bảng này k xóa**' (ô Test Result để trống).\n\n"
     "Nguồn C — [AI] v2 TC-CBF-089 (QA-spec-016 CONFIRMED 'xóa các remind đã đặt lịch trên tool lme', "
     "MAP-CANCEL-02; Blocked cả 2 env): 'Sau swap: remind đã đặt lịch bị hủy/xóa — friend cũ KHÔNG nhận "
     "được remind sau swap'.",
     "spec-features/admin/lesson-booking/job/job-spec.md:333-356 (§3.5 ChangeBotTask / ChangeBotJob) — "
     "bước 6 của job dọn dữ liệu CHỈ gồm 2 lệnh (ChangeBotJob.java:326-333): "
     "`deleteCalendarCourseBookingByBotId(botId)` + `resetCalendarCourseReceptionsByBotId(botId)`, "
     "SQL thật ở ChangeBotDataCleanupRepository.java:285-298. Confidence: Cao.\n"
     "job-spec.md:579 — bảng tác động: 'Toàn bộ đặt chỗ lesson của bot bị xoá, calendar_course_receptions reset'.\n"
     "⇒ Spec job KHÔNG NHẮC event_step_time ở bước dọn dữ liệu đổi LOA, dù event_step_time chính là hàng đợi "
     "nhắc lịch của FA-019 (job-spec.md §4.1: CalendarCourseBookingService::addActionRemind() INSERT "
     "event_step_time status=0).",
     "Nếu KHÔNG xóa (nguồn B): `NewEventRemindTask` sẽ tiếp tục quét event_step_time status=0 tới mốc "
     "sent_date_time và GỬI NHẮC LỊCH cho friend của LOA cũ — những người không còn là bạn của bot, "
     "qua channel mới. Hậu quả: gửi tin sai người / lỗi gửi tin hàng loạt / tiêu quota tin nhắn. "
     "Nếu CÓ xóa (nguồn A + C) thì spec job đang THIẾU mô tả — người đọc spec sẽ kết luận sai là không xóa. "
     "Đặc biệt nguy hiểm vì bước 6 của job chỉ xóa `calendar_course_bookings` mà booking là GỐC của remind: "
     "xóa booking mà để lại event_step_time là tạo bản ghi mồ côi trỏ user_booking_id không còn tồn tại.",
     "Nhóm 10: TC remind biểu mẫu · TC remind bài học · TC đặt lịch salon · TC đặt lịch sự kiện · "
     "TC màn Gửi nhắc lịch (5 TC)",
     "",
     "Chốt xong phải: ① query event_step_time trên PRODUCTION sau 1 lần đổi LOA thật để xác nhận; "
     "② nếu job KHÔNG xóa → RAISE BUG mức cao (gửi tin sai người) và rà cả bản ghi mồ côi hiện có; "
     "③ bổ sung event_step_time vào lesson-booking/job/job-spec.md §3.5 danh sách bảng bị dọn, "
     "hoặc ghi rõ là CỐ Ý không xóa kèm lý do."],

    ["MT-08", "CAO", W,
     "LINK DOWNLOAD CSV CŨ sau khi đổi LOA — expected nói 404 nhưng thực tế VẪN TẢI ĐƯỢC và dev nói "
     "'logic cũ đã như vậy'",
     "Change bot r37 — expected: '- Xóa các file csv của file cũ. Cách test: 1. Trước khi change bot: "
     "Lưu lại link download file CSV cũ. 2. Sau khi change bot: Truy cập lại link download file CSV cũ "
     "=> **Ra lỗi 404**'. Đánh giá: TR=OK, stg=OK, step=OK.\n"
     "NHƯNG cùng dòng r37 ghi chú thực tế: 'nhấn reset => download lại data mới rồi **nhưng khi down link "
     "cũ vẫn down được** (anh Tư bảo logic cũ đã như vậy) — **Bug Tester #33938**'.\n"
     "AddBot/Testcase r299 — CÙNG nội dung TC, cùng ghi chú, nhưng đánh giá **NG**.\n"
     "Link mẫu lưu trong TC: https://staging.lme.jp/msg_template/csv/829/CSV_210_20260123170404.csv\n\n"
     "Cùng kiểu vấn đề với Change bot r46 (QR code cũ) — TC chỉ ghi CÁCH TEST, KHÔNG ghi expected.",
     "Spec KHÔNG mô tả vòng đời file CSV đã xuất của FA-014 khi đổi LOA. "
     "spec-features/admin/ không có thư mục csv-management (FA-014 trạng thái CHƯA scan theo index.md).\n"
     "⇒ Không có cơ sở spec.",
     "Ba điểm mâu thuẫn chồng nhau: (a) expected trong TC ≠ hành vi thực tế; (b) 2 nguồn đánh giá cùng 1 "
     "TC khác nhau (OK vs NG); (c) dev tuyên bố 'logic cũ đã như vậy' tức coi là hành vi đúng, nhưng có "
     "ticket Bug Tester #33938 đã mở. Rủi ro thực chất là RÒ RỈ DỮ LIỆU: file CSV xuất từ LOA cũ chứa "
     "thông tin friend (PII); nếu link vẫn tải được sau khi đổi LOA thì dữ liệu friend LOA cũ vẫn truy "
     "xuất được — CHÍNH vấn đề mà SpecImprove #33154 (AddBot/Testcase r227, 21/01/2026) đã phải fix cho "
     "friend info: 'Sau khi change LOA, có thể truy xuất ngược lại data friend infor trong vòng 1 tháng "
     "không? Nguyên nhân: khi change bot chưa clear data friend của bot cũ'.",
     "Nhóm 10: TC link CSV cũ · TC số người đối tượng CSV · TC QR code cũ (3 TC)",
     "",
     "Chốt xong phải: ① tra trạng thái Bug Tester #33938 (theo RULE-11 chỉ Closed/Resolved/Fix done/"
     "Released mới là bằng chứng hợp lệ); ② chốt expected: phải 404 hay được phép tải; ③ nếu được phép "
     "tải thì phải đánh giá rủi ro PII và ghi vào spec; ④ đồng bộ lại đánh giá OK/NG giữa Change bot r37 "
     "và AddBot/Testcase r299; ⑤ viết expected cho Change bot r46 (QR cũ) — hiện chỉ có cách test."],

    ["MT-09", "TRUNG BÌNH", W,
     "LIÊN KẾT GOOGLE sau khi đổi LOA — mất liên kết phải nối lại, hay vẫn đồng bộ bình thường? "
     "Hai dòng trong CÙNG 1 tab nói khác nhau",
     "Change bot r32 (Form, TR=OK + stg=OK + step=OK): 'check sync google: - bot cũ đã liên kết, sau khi "
     "change sẽ **BỊ MẤT LIÊN KẾT => phải liên kết lại** / - sync data bình thường / - **sync vào spread MỚI** "
     "/ (anh Tư bảo logic cũ đã như vậy)'.\n\n"
     "Change bot r212 (Booking salon, TR=OK + stg=OK + devnote=OK): '- Bot mới gửi link booking cho friend "
     "mới => Friend booking thành công / - Sau khi booking success => **Check việc sync google spread và "
     "google calendar BÌNH THƯỜNG**'. Không nhắc phải liên kết lại.\n"
     "Change bot r213 (Booking lesson): tương tự r212.",
     "spec-features/admin/ không có file nào mô tả vòng đời liên kết Google khi đổi LOA. "
     "FA-019/FA-020 có spec nhưng phần sync Google không nói tới thao tác đổi LOA.\n"
     "⇒ Không có cơ sở spec.",
     "Nếu r32 đúng (mất liên kết) thì r212/r213 đang TEST THIẾU BƯỚC: người test sẽ thấy 'sync không chạy' "
     "và báo bug, trong khi thực ra phải liên kết lại trước. Nếu r212/r213 đúng (còn liên kết) thì r32 sai "
     "và người test sẽ liên kết lại một cách vô ích, đồng thời tạo spreadsheet mới trong khi spreadsheet cũ "
     "vẫn đang nhận dữ liệu → dữ liệu khách hàng bị chia 2 nơi. Cũng cần làm rõ liên kết Google là cấu hình "
     "MỨC BOT hay MỨC TÍNH NĂNG (form riêng, lịch riêng) — vì r32 nói về form còn r212/r213 nói về booking.",
     "Nhóm 10: TC liên kết Google của biểu mẫu · Nhóm 12: TC đặt lịch salon (Google Calendar + Spreadsheet) · "
     "TC đặt lịch bài học (Spreadsheet) (3 TC)",
     "",
     "Chốt xong phải: ① test thật 1 lần đổi LOA rồi kiểm trạng thái liên kết Google của CẢ form, lịch salon, "
     "lịch bài học; ② chốt liên kết là mức bot hay mức tính năng; ③ nếu mất liên kết thì thêm bước "
     "'liên kết lại' vào tiền điều kiện của TC r212/r213; ④ ghi vào spec-features của FA-011/FA-019/FA-020."],

    ["MT-10", "TRUNG BÌNH", W,
     "LỊCH SỬ GỬI TIN HÀNG LOẠT / phát hành theo bước — GIỮ lại hay XÓA sau khi đổi LOA?",
     "Nguồn A — Change bot r22 (TR=OK + stg=OK + step=OK): 'tab lịch sử send: tab đặt lịch send, tab draft "
     "/ - update cột send_count = 0 / - **vẫn GIỮ LẠI lịch sử** / => spec cũ hiện tại như vậy, chỉ update "
     "send_count = 0'. r23 bổ sung: GUI tab đã send, trường 配信数 → 'không hiển thị số friend nào'.\n\n"
     "Nguồn B — [AI] v2 TC-CBF-086 (QA-spec-016; Blocked cả 2 env): 'Sau swap: danh sách message lỗi cũ + "
     "**lịch sử broadcast/step delivery/scenario BỊ XÓA**'.",
     "Spec KHÔNG mô tả. spec-features/admin/message-send-all/ có spec FA-008 nhưng không nói tới đổi LOA.\n"
     "⇒ Không có cơ sở spec.",
     "Hai nguồn nói NGƯỢC NHAU hoàn toàn về cùng một đối tượng. Nguồn A tự dẫn 'spec cũ hiện tại như vậy' "
     "⇒ là hành vi đã được xác nhận tại thời điểm 04/2026. Nguồn B là tuyên bố của đợt 07-08/2026 nhưng "
     "CHƯA CHẠY ĐƯỢC trên môi trường nào. Ảnh hưởng thực tế: nếu xóa lịch sử thì Admin mất toàn bộ hồ sơ "
     "các lần gửi tin trước đây (có thể cần cho đối soát quota/khiếu nại); nếu giữ thì phải bảo đảm lịch sử "
     "KHÔNG chứa dữ liệu friend LOA cũ (PII) — liên quan MT-08.",
     "Nhóm 10: TC gửi tin hàng loạt (send_count + số dòng lịch sử) · TC lỗi phát hành (2 TC)",
     "",
     "Chốt xong phải: ① query số dòng lịch sử gửi tin trước/sau 1 lần đổi LOA thật trên PRODUCTION; "
     "② nếu GIỮ lịch sử → kiểm xem lịch sử có lộ thông tin friend LOA cũ không; ③ ghi kết luận vào "
     "spec-features/admin/message-send-all/ và bổ sung vào danh sách bảng của job dọn dữ liệu."],

    ["MT-11", "THẤP", W,
     "TÊN BẢNG hàng đợi đổi LOA — `schedule_change_bot` (số ít, spec job) vs `schedule_change_bots` "
     "(số nhiều, TCs)",
     "Change bot r4 (TR=OK + stg=OK): 'Check khi nhấn change bot → check db → bảng: "
     "**`schedule_change_bots`**'.\n"
     "Change bot r191 (TR=OK + stg=OK): '- check db: **schedule_change_bots**'.",
     "spec-features/admin/lesson-booking/job/job-spec.md:206-212 (§2.6) — "
     "'**`schedule_change_bot`** — Hàng đợi đổi bot (gián tiếp). Entity JPA: `ScheduleChangeBot`; "
     "poll `findTop50ByStatusOrderByIdAsc(ScheduleChangeBot.STATUS_WAITING)` (`task/ChangeBotTask.java:82-83`), "
     "nhịp `ChangeBotConstants.SCAN_INTERVAL_MS` / `PER_RECORD_DELAY_MS`, lỗi → `ERROR_BACKOFF_MS`. "
     "Confidence: Cao'.\n"
     "spec-features/admin/qr-landing/db/db-mapping.md:54 + 1563 — ghi `schedule_change_bot` và nêu "
     "'**thiếu trong dump** nhưng có entity ScheduleChangeBot.java + ScheduleChangeBotRepository.java "
     "trong src/job' ⇒ dump schema không phủ hết (nhiều database: linedb/backenddb/historydb, "
     "Laravel mysql_callback).",
     "Tên bảng sai 1 ký tự làm người test query ra 'bảng không tồn tại' rồi kết luận sai là job không ghi "
     "dữ liệu. Nghiêm trọng hơn: db-mapping.md:1563 đã ghi nhận bảng này KHÔNG CÓ trong dump schema 308 bảng "
     "của `lme_db` ⇒ người test có thể query đúng tên mà vẫn không thấy bảng vì nó nằm ở database khác. "
     "Cần chốt cả TÊN và DATABASE để TC query được.",
     "Nhóm 10: TC sinh bản ghi hàng đợi · Nhóm 9: TC đặt lịch (toàn bộ TC query bảng này) · "
     "Nhóm 14: TC job dọn dữ liệu nhiều bản ghi",
     "",
     "Chốt xong phải: ① xác nhận tên bảng thật + database chứa nó; ② sửa thống nhất trong TC và spec; "
     "③ theo khuyến nghị sẵn có ở qr-landing/db/db-mapping.md §7.4, yêu cầu DBA export bổ sung dump của "
     "database chứa bảng này để TC có cơ sở query."],

    ["MT-12", "CAO", W,
     "SPEC LẠC HẬU NGHIÊM TRỌNG — spec tả màn đổi LOA là LANDING PAGE MARKETING 1 màn, corpus tả WIZARD "
     "10 màn + campaign + đặt lịch + tiến trình",
     "Corpus 04/2026 → 08/2026 mô tả một tính năng hoàn chỉnh:\n"
     "• [AI] v2 liệt kê 10 màn: SCR-01 modal promo · SCR-02 trang campaign · SCR-03「01 入れ替え方法選択」· "
     "SCR-04「02 接続情報入力」· SCR-05「03 接続情報確認」· SCR-06「06 入れ替え中」· SCR-07「04 接続完了」· "
     "SCR-08「05-A 予約済み」· SCR-09 modal xóa đặt lịch · SCR-10 modal xác nhận thực hiện\n"
     "• 11 endpoint EP-01…EP-11 (validate channel, tạo/xóa đặt lịch, polling tiến độ, thực hiện đổi)\n"
     "• 46 business rule BR-01…BR-46\n"
     "• cột DB mới: `swap_status`, `has_campaign` (TD Section 3 Altered Tables — TC-CBF-116)\n"
     "• Tab Info r2 (04/2026): 'Tách riêng ra 1 menu mới' ⇒ đã là menu độc lập, không còn là màn con\n"
     "• Change bot r101-r197 (#34632) và r249-r317 (#37744): wizard nhiều bước với quét QR 3 phút",
     "spec-features/admin/bot-edit/ui/ui-spec.md:208-240 (SCR-BE-03, quét 2026-03-24) — tả NGUYÊN VĂN: "
     "'Landing page giới thiệu tính năng — 3 blocks giới thiệu: メッセージをセグメント配信 / 予約を簡単管理 / "
     "LINE上で決済も完結; Chào mừng: テスト：ゴー・トゥイ・ガン 様; [無料で利用開始]'. Action Buttons: ĐÚNG 1 nút "
     "「無料で利用開始」. Observations: 'Trang này là landing page marketing... Sau khi nhấn「無料で利用開始」→ "
     "quy trình kết nối LOA mới (**nằm ngoài scope tính năng bot-edit**)'.\n"
     "spec-features/admin/bot-edit/feature-spec.md:251-263 (§2.3) — luồng EP-08 3 bước, "
     "'User nhấn「無料で利用開始」→ bắt đầu quy trình đăng ký LOA mới (**ngoài scope**)'.\n"
     "spec-features/admin/bot-edit/web/api-spec.md:21 + 382-400 — ĐÚNG 1 endpoint EP-08 GET, trả view "
     "`admin.bots.bot_add_v3`.\n"
     "spec-features/admin/bot-edit/db/db-mapping.md:358-366 (§4.4) — ĐÚNG 2 dòng mapping.\n"
     "spec-features/admin/index.md:48 — FA-038 đánh dấu 'HOÀN THÀNH — 13 endpoints, 1 job, 13 tables. "
     "Gồm cả trang LOA入れ替え' ⇒ spec TỰ TIN là đã xong.",
     "Spec được reverse-engineer ngày 2026-03-24, ngay TRƯỚC đợt improve 04/2026. Toàn bộ tính năng "
     "(campaign · wizard · đặt lịch · tiến trình · job dọn dữ liệu mở rộng) được thêm SAU đó và spec "
     "CHƯA CẬP NHẬT. Hậu quả với công việc review TC: bất kỳ ai đối chiếu TC với spec cũng sẽ kết luận "
     "sai là 'TC viết sai / viết cho màn không tồn tại'. Nguy hiểm hơn: spec tự đánh dấu HOÀN THÀNH và "
     "ghi 'ngoài scope' cho chính phần nghiệp vụ nặng nhất ⇒ không ai biết là đang thiếu. "
     "Đây KHÔNG phải mâu thuẫn về hành vi mà là mâu thuẫn về PHẠM VI — phải chốt trước khi dùng spec "
     "làm căn cứ cho bất kỳ MT nào khác.",
     "TOÀN BỘ 14 nhóm của tab FA-039",
     "",
     "Chốt xong phải: ① quyết định tách FA-039 thành spec-features riêng hay viết thêm vào bot-edit; "
     "② chạy reverse-scan lại màn đổi LOA trên PRODUCTION (ui · web · job · db); ③ bỏ chữ 'ngoài scope' "
     "ở feature-spec.md §2.3 và ui-spec.md SCR-BE-03; ④ hạ trạng thái FA-038 ở index.md:48 khỏi 'HOÀN THÀNH' "
     "cho phần LOA入れ替え; ⑤ bổ sung EP-01…EP-11, BR-01…BR-46, cột swap_status/has_campaign vào spec."],

    ["MT-13", "TRUNG BÌNH", W,
     "SỐ MÀN VÀ NHÃN NÚT của wizard — 3 biến thể UI cùng tồn tại trong corpus, niên đại gần nhau",
     "Biến thể 1 — Change bot r101-r197 (Feature #34632, 04/2026): hướng dẫn màn 1 → màn 2 → "
     "step 1「kiểm tra thông tin kết nối」(màn 3, có checkbox「チャネルIDが同一であることを確認した」+ 3 ô) → "
     "step 3「Messaging APIとLINEログインの接続情報を入力します」(màn 7) → step 4 webhook (màn 8) → "
     "step 5 kiểm tra kết nối/QR (màn 9) → màn 10 thành công → màn 11 chưa xác thực → màn 12 hướng dẫn. "
     "Nhãn:「次へ進む」·「前のステップに戻る」·「無料で利用開始」.\n\n"
     "Biến thể 2 — Change bot r249-r317 (Feature #37744, 07/2026, Figma 入れ替え機能 1ヶ月無料開放): "
     "màn 1「nhập Messaging APIチャネル」→ màn 2「Cài đặt webhook」(có khối 発行されたWebhook URL + nút コピー) → "
     "màn 3「Kiểm tra thông tin bot」(hiển thị tên bot, LINE ID, số friend, khối メッセージングAPIチャネル + "
     "LINEログインチャンネル, nút「この内容で接続する」) → màn item đặt lịch → step 5 QR. "
     "Nhãn:「次に進む」·「戻る」·「キャンセル」·「接続情報の確認にすすむ」·「この内容で接続する」.\n\n"
     "Biến thể 3 — [AI] v2 (07-08/2026): 10 màn SCR-01…SCR-10 như MT-12, KHÔNG có màn webhook riêng "
     "(xem MT-05). Nhãn:「接続情報の確認に進む」·「この内容で接続する」·「入れ替えを実行する」·「削除する」·"
     "「入れ替え設定に進む」·「入れ替え予約設定に進む」.",
     "spec-features/admin/bot-edit/ui/ui-spec.md:208-240 — chỉ 1 màn landing + 1 nút「無料で利用開始」 "
     "(xem MT-12). Không có wizard nào.",
     "Ba biến thể cách nhau 1-3 tháng nên 'ưu tiên TC mới nhất' là CĂN CỨ YẾU. Lý do chọn biến thể 3 để "
     "viết TC: nó có SPEC ID + BR + kết quả chạy trên CẢ dev và staging (kiểm chứng được), trong khi biến "
     "thể 2 có nhiều dòng cột kết quả TRỐNG (chưa chạy) và biến thể 1 đã bị #37744 thay giao diện. "
     "Nhưng biến thể 2 chứa 2 thứ biến thể 3 KHÔNG có: màn webhook riêng (MT-05) và tính năng copy Webhook "
     "URL. Nếu chốt sai biến thể thì nhãn nút trong ~60 TC sẽ không khớp màn thật và member sẽ báo bug oan.",
     "Nhóm 3 · 4 · 5 · 6 · 7 · 8 (mọi TC có nhãn nút cụ thể, ~60 TC)",
     "",
     "Chốt xong phải: ① chụp ảnh từng màn wizard trên PRODUCTION và đánh số; ② lập bảng đối chiếu "
     "'màn thật ↔ SCR-xx của biến thể 3 ↔ màn N của biến thể 1/2'; ③ sửa nhãn nút trong TC theo bản thật; "
     "④ ghi bộ nhãn chuẩn vào ui-spec.md để lần sau không phải đoán."],

    ["MT-14", "THẤP", W,
     "NÚT「使い方を見る」mở TRANG MANUAL hay mở VIDEO hướng dẫn?",
     "Nguồn A — Change bot r105 (#34632) · r254 · r255 (#37744, TR=OK): "
     "'CHeck khi click vào text: 使い方を見る → direct tới link **https://lme.jp/manual/loa_replacement/**' "
     "và 'double click button 使い方を見る → direct open new tab: https://lme.jp/manual/loa_replacement/'.\n"
     "Change bot r284 (màn webhook): cùng link manual.\n\n"
     "Nguồn B — [AI] v2 TC-CBF-023 (Pass dev + staging): 'Nút「使い方を見る」mở **VIDEO hướng dẫn**'.",
     "Spec KHÔNG nhắc nút này (xem MT-12).",
     "Khác biệt nhỏ về hành vi nhưng ảnh hưởng trực tiếp tới expected của TC. Đáng lưu ý thêm: CLAUDE.md "
     "của repo ghi rõ KHÔNG WebFetch https://lme.jp/manual/ (bỏ từ 2026-09-08) ⇒ không thể tự kiểm link "
     "này còn sống hay không; phải do người test mở thật.",
     "Nhóm 1: TC nút 使い方を見る · Nhóm 4: TC link phụ màn nhập thông tin · Nhóm 5: TC link phụ màn webhook",
     "",
     "Chốt xong phải: ① mở thật nút này trên PRODUCTION và ghi nhận đích (trang manual / video / cả hai); "
     "② kiểm link https://lme.jp/manual/loa_replacement/ còn sống; ③ sửa expected của 3 TC liên quan."],

    ["MT-15", "TRUNG BÌNH", W,
     "CHANNEL SECRET ở màn xác nhận thông tin — hiển thị ĐẦY ĐỦ hay MASKED?",
     "Nguồn A — Change bot r299 (TR=OK): 'チャネルシークレット: Channel secret → **hiển thị đúng Channel "
     "secret**'. r302 (TR=OK): 'チャネルシークレット: Channel secret của LIne login → **hiển thị đúng "
     "Channel secret**'. ⇒ expected là hiển thị giá trị thật để đối chiếu.\n\n"
     "Nguồn B — [AI] v2 TC-CBF-047 (SEC-002, BR-18; Blocked cả 2 env): 'Channel Secret hiển thị dạng "
     "**partial-masked, KHÔNG có toggle** để xem đầy đủ'. TC-CBF-101 (TD EP-11 'Mask sensitive data "
     "(channel secret)'; Pass dev): chi tiết đặt lịch hiển thị channel info ở dạng masked.",
     "Spec KHÔNG mô tả màn xác nhận (xem MT-12). "
     "spec-features/admin/bot-edit/db/db-mapping.md không ghi quy tắc mask cho cột channel_secret.",
     "Hai nguồn nói ngược nhau về một dữ liệu NHẠY CẢM. Nguồn A (04-07/2026) coi việc hiển thị đầy đủ là "
     "ĐÚNG để người dùng đối chiếu với LINE Developers; nguồn B (07-08/2026) coi đó là vi phạm SEC-002. "
     "Cần chốt vì: nếu phải mask mà thực tế hiển thị đầy đủ → lỗ hổng lộ credential ở màn admin "
     "(ai xem màn hình cũng đọc được secret); nếu được phép hiển thị mà TC lại assert masked → người test "
     "báo bug oan. Lưu ý nguồn B cũng không đồng nhất: TC-CBF-042 nói màn NHẬP có toggle hiện/ẩn secret, "
     "TC-CBF-047 nói màn XÁC NHẬN không có toggle ⇒ quy tắc khác nhau theo màn, cần ghi rõ từng màn.",
     "Nhóm 6: TC mask channel secret · TC hiển thị khối Messaging API · TC hiển thị khối LINE Login · "
     "Nhóm 9: TC mask channel info ở chi tiết đặt lịch",
     "",
     "Chốt xong phải: ① chụp ảnh màn xác nhận trên PRODUCTION để xác định hành vi thật; ② chốt quy tắc "
     "mask cho TỪNG màn (nhập · xác nhận · chi tiết đặt lịch); ③ nếu đang hiển thị đầy đủ mà phải mask → "
     "RAISE BUG bảo mật; ④ ghi quy tắc mask vào api-spec.md của các endpoint trả channel info."],

    ["MT-16", "TRUNG BÌNH", W,
     "CẢNH BÁO LIFF ID ĐỔI — đổi LOA có hiển thị cảnh báo ảnh hưởng 5 tính năng như thao tác kết nối lại "
     "LIFF hay không?",
     "[AI] v2 TC-CBF-065 (DATA-REF-001, TD Section 7.3 + BR-41 + CM-005; Blocked cả 2 env): "
     "'Cảnh báo LIFF ID thay đổi ảnh hưởng **5 tính năng** hiển thị TRƯỚC khi thực hiện swap'.\n"
     "TC-CBF-090: 'Sau swap: link form đã tạo trước đó (dùng LIFF ID cũ) không còn mở đúng'.\n"
     "Change bot r30 (TR=OK + stg=OK + step=OK): 'Check việc access link từ friend cũ → user line hiển thị "
     "lỗi 404' ⇒ xác nhận link cũ chết, nhưng KHÔNG nguồn nào ghi có cảnh báo trước khi đổi.\n"
     "Bill tiền/change_bot r22: liệt kê `liff_app_id` (エルメ流入アクション用LIFF — cho landing) và "
     "`liff_app_id_booking` (エルメ各種フォーム用LIFF — form, booking) bị update ⇒ LIFF ID đổi là chắc chắn.",
     "spec-features/admin/bot-edit/ui/ui-spec.md:208-240 + feature-spec.md:270-280 (SCR-BE-04 "
     "「LIFFアプリ接続確認ダイアログ」) — có CHÍNH nội dung cảnh báo cần thiết: "
     "「LIFFアプリの接続が切れているため再接続処理を行います。再接続処理を行なった場合、すでに作成済みの"
     "**回答フォーム、商品、カレンダー予約、イベント予約、流入アクション**が利用できなくなる場合があります。」"
     "⇒ ĐÚNG 5 tính năng. NHƯNG dialog này thuộc thao tác KẾT NỐI LẠI LIFF trên màn LOA接続設定 (EP-06), "
     "KHÔNG phải thao tác đổi LOA.",
     "Đổi LOA gây hậu quả GIỐNG HỆT thao tác kết nối lại LIFF (LIFF ID mới ⇒ form/sản phẩm/lịch/sự kiện/"
     "QR action cũ chết) nhưng spec chỉ yêu cầu cảnh báo ở thao tác kia. Nếu đổi LOA KHÔNG cảnh báo thì "
     "Admin mất dữ liệu truy cập của 5 tính năng mà không được báo trước — đúng hậu quả đã ghi nhận ở "
     "Change bot r30 (link form cũ 404). Đây là vùng mù GIỮA 2 spec: FA-038 có cảnh báo cho LIFF reconnect, "
     "FA-039 chưa có spec nên không ai kiểm.",
     "Nhóm 6: TC cảnh báo LIFF ID đổi · Nhóm 10: TC link form cũ 404 · TC QR cũ · "
     "Nhóm 12: TC form cũ gửi lại cho friend mới (4 TC)",
     "",
     "Chốt xong phải: ① kiểm màn xác nhận đổi LOA trên PRODUCTION có cảnh báo LIFF không; ② nếu KHÔNG → "
     "đề xuất bổ sung cảnh báo với ĐÚNG 5 tính năng như SCR-BE-04; ③ ghi vào spec FA-039 (sau khi giải "
     "quyết MT-12) mục cảnh báo trước khi thực hiện; ④ bổ sung TC cho cả 5 tính năng (hiện corpus chỉ "
     "cover form và QR)."],
]
