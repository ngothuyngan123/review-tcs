# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 5-6.

S5 Cài đặt webhook (màn webhook của wizard)
S6 Xác nhận thông tin kết nối (màn「03 接続情報確認」)

⚠️ TOÀN BỘ nhóm 5 phụ thuộc MT-05 — chưa chốt webhook là MÀN RIÊNG bắt user tick
checkbox (Change bot #34632 r148-r156 + #37744 r284-r293) hay hệ thống TỰ check ở
bước nhập thông tin ([AI] v2 TC-CBF-035 / BR-16). Niên đại 2 nguồn gần nhau
(7/2026 vs 7-8/2026) nên quy tắc "ưu tiên TC mới nhất" là căn cứ YẾU ở đây —
lý do chọn viết cả 2 nhóm: nếu Leader chốt bản tự-check thì nhóm 5 bị loại gọn,
còn nếu chốt bản có màn riêng thì không bị thiếu TC.
"""
from _common import tc

PAID = ("- Đăng nhập Admin chủ (主管理者) của bot plan Standard trở lên (bots.plan_type = 1)\n"
        "- Bot đã kết nối, KHÔNG có đặt lịch đổi LOA nào đang active")
WH = (PAID + "\n- Đã nhập xong 4 field thông tin kết nối hợp lệ (Messaging API + LINE Login cùng provider)\n"
      "- Đang ở màn「Cài đặt webhook」của wizard")
CF = (PAID + "\n- Đã nhập xong 4 field thông tin kết nối hợp lệ và qua được bước webhook\n"
      "- Đang ở màn xác nhận thông tin kết nối (「03 接続情報確認」)")
MT05 = "⚠️ Phụ thuộc MT-05 — chỉ áp dụng nếu Leader chốt bản có MÀN WEBHOOK RIÊNG. "

S5 = [
    # ═══════════════ 5. Cài đặt webhook ═══════════════
    tc("Cài đặt webhook", "FUNC-001", "Normal",
       "Màn webhook lúc mới vào — checkbox chưa tick, nút sang bước tiếp bị disable",
       WH,
       "1. Từ màn nhập thông tin kết nối, bấm nút sang bước tiếp\n"
       "2. Quan sát checkbox「Webhookをオンに設定した」\n"
       "3. Quan sát nút sang bước tiếp\n"
       "4. Bấm thử nút sang bước tiếp",
       "Bot Standard; chưa tick checkbox",
       "- Checkbox ở trạng thái CHƯA tick\n"
       "- Nút sang bước tiếp DISABLED (màu nhạt)\n"
       "- Bấm nút: không có phản ứng, không gọi request, không chuyển màn",
       note=MT05 + "Nguồn: Change bot r148 (step 4 màn 8, TR=OK) + Bill tiền/change_bot r13 "
            "(bản cũ 11/2023: 'button không click được vẫn hiển thị text ※未確認の項目があります'). "
            "Evidence: ảnh màn + Network trống."),

    tc("Cài đặt webhook", "UI-FIELD-001", "Normal",
       "Tick checkbox webhook → đổi màu checkbox + đổi màu nút, nút chuyển enable",
       WH,
       "1. Bấm tick checkbox「Webhookをオンに設定した」\n"
       "2. Quan sát màu/trạng thái checkbox\n"
       "3. Quan sát màu và trạng thái nút sang bước tiếp\n"
       "4. Bỏ tick checkbox → quan sát lại nút",
       "Tick rồi bỏ tick",
       "- Tick: checkbox đổi màu (có dấu tick), nút đổi màu và chuyển ENABLED\n"
       "- Bỏ tick: nút trở lại DISABLED ngay, không cần reload",
       note=MT05 + "Nguồn: Change bot r149 (cột Test Result TRỐNG — chưa chạy) + r115/r117 "
            "(bản #34632 step 1 'đổi màu check box, đổi màu button → enable button next'). "
            "⚠️ RISK: r149 chưa có kết quả chạy. Evidence: ảnh trước/sau tick."),

    tc("Cài đặt webhook", "FUNC-001", "Normal",
       "Webhook URL phát hành hiển thị đúng và nút コピー copy được vào clipboard",
       WH,
       "1. Quan sát khối「発行されたWebhook URL」\n"
       "2. Ghi lại URL hiển thị\n"
       "3. Bấm nút「コピー」\n"
       "4. Quan sát message hiện ra\n"
       "5. Paste clipboard vào ô text bất kỳ để đối chiếu",
       "Bot Standard trên môi trường tương ứng",
       "- Hiển thị URL callback đúng domain của môi trường đang test "
       "(VD https://lme.watermeru.com/line/callback/add/0 trên dev)\n"
       "- Bấm「コピー」: hiện message「Webhook URLをコピーしました。」\n"
       "- Giá trị paste ra KHỚP HOÀN TOÀN với URL hiển thị trên màn (không thiếu/thừa ký tự, không thừa space)",
       env="PRODUCTION",
       note=MT05 + "Nguồn: Change bot r287 + r291 (bản #37744, cột kết quả TRỐNG — chưa chạy). "
            "⚠️ RULE-08 — webhook URL là hạng mục DOMAIN, không được kết luận từ staging: domain callback "
            "khác nhau giữa dev/staging/production. ⚠️ RISK: tính năng copy Webhook URL là MỚI ở #37744, "
            "chưa có nguồn nào chạy. Evidence: ảnh URL + ảnh message + ảnh giá trị paste ra."),

    tc("Cài đặt webhook", "UI-001", "Normal",
       "Các link phụ trên màn webhook mở đúng tab mới, double-click không mở 2 tab",
       WH,
       "1. Bấm「設定動画をスマホで見る」→ quan sát\n"
       "2. Quay lại, bấm「LINE公式アカウント管理画面を表示します」→ quan sát URL tab mới\n"
       "3. Quay lại, bấm「LINE developersを開く」→ quan sát\n"
       "4. Quay lại, bấm「LINE Developersコンソールを開く」→ quan sát URL tab mới\n"
       "5. Với từng link, bấm 2 lần nhanh và đếm số tab",
       "4 link phụ trên màn webhook",
       "-「設定動画をスマホで見る」→ hiển thị ảnh QR code (không mở tab)\n"
       "-「LINE公式アカウント管理画面を表示します」→ mở tab mới https://manager.line.biz/\n"
       "-「LINE developersを開く」→ hiển thị ảnh QR code\n"
       "-「LINE Developersコンソールを開く」→ mở tab mới https://manager.line.biz/\n"
       "- Mỗi link bấm 2 lần nhanh chỉ mở ĐÚNG 1 tab",
       note=MT05 + "Nguồn: Change bot r151-r152 (TR=OK) + r286 + r288 (bản #37744, chưa chạy). "
            "⚠️ r288 ghi nhãn là「LINE Developersコンソール」nhưng URL lại là manager.line.biz (LINE Official "
            "Account Manager) — nhãn và URL KHÔNG khớp nhau, cần Leader xác nhận đây là lỗi nhãn hay lỗi URL. "
            "Evidence: ảnh 4 tab/QR + URL.",
       spec="Đã hỏi leader"),

    tc("Cài đặt webhook", "FUNC-001", "Normal",
       "Bấm nút quay lại bước trước từ màn webhook → dữ liệu 4 field đã nhập VẪN còn",
       WH,
       "1. Ở màn webhook, bấm nút/chữ quay lại bước trước (「前のステップに戻る」hoặc「戻る」)\n"
       "2. Quan sát màn hình đích\n"
       "3. Kiểm tra 4 field thông tin kết nối\n"
       "4. Bấm sang bước tiếp lần nữa, quan sát trạng thái checkbox webhook",
       "4 field đã nhập hợp lệ",
       "- Quay về đúng màn nhập thông tin kết nối\n"
       "- CẢ 4 field giữ nguyên giá trị đã nhập (không bị xóa)\n"
       "- Sang lại màn webhook: checkbox reset về chưa tick (hoặc giữ trạng thái — ghi nhận hành vi thật)",
       note=MT05 + "Nguồn: Change bot r153 (TR=OK, 'quay lại bước trước, thông tin màn trước đó vẫn còn') "
            "+ r289 + r140/r276. Evidence: ảnh 4 field sau khi back."),

    tc("Cài đặt webhook", "CONC-001", "Boundary",
       "Double-click nút sang bước tiếp ở màn webhook → chỉ tính 1 lần, không tạo 2 bản ghi bots",
       WH + "\n- Đã tick checkbox webhook\n- Webhook đã BẬT trên LINE Developer Console",
       "1. Tick checkbox webhook\n"
       "2. Mở DevTools tab Network, xóa log\n"
       "3. Double-click nhanh (<300ms) nút sang bước tiếp\n"
       "4. Đếm số request trong Network\n"
       "5. Query DB: SELECT COUNT(*) FROM bots WHERE is_delete = 2 cho bot đang đổi",
       "Double-click trong 300ms; webhook ON",
       "- Network: ĐÚNG 1 request\n"
       "- DB: ĐÚNG 1 bản ghi bots mới với is_delete = 2 (không phải 2 bản ghi)\n"
       "- Bên LINE: chỉ tạo ĐÚNG 2 LIFF app (không phải 4)\n"
       "- Chỉ chuyển màn 1 lần",
       note=MT05 + "Nguồn: Change bot r154 (TR=OK 'next sang màn 9') + r120 "
            "('double click button 次へ進む → tính 1 lần'). ⚠️ MT-01 — nhánh 'tạo bản ghi bots mới "
            "is_delete=2' theo TCs 2026; TCs 2023 (Bill tiền r22) nói UPDATE tại chỗ vào id bot cũ. "
            "RULE-07 — verify DB. Evidence: Network + query bots + ảnh LIFF list bên LINE."),

    tc("Cài đặt webhook", "INTG-LINE-001", "Normal",
       "Webhook đang BẬT → bấm sang bước tiếp: cập nhật webhook URL bên LINE + tạo 2 LIFF app + tạo bản ghi bots is_delete=2",
       WH + "\n- Đã tick checkbox webhook\n- Webhook của Messaging API channel ĐANG BẬT trên LINE Developer Console",
       "1. Xác nhận webhook ON trên LINE Developer Console\n"
       "2. Ghi lại webhook URL hiện tại của channel bên LINE + số LIFF app hiện có của LINE Login channel\n"
       "3. Tick checkbox, bấm nút sang bước tiếp\n"
       "4. Kiểm tra bên LINE: webhook URL của Messaging API channel + danh sách LIFF app\n"
       "5. Query DB: bảng bots, bot_contract, bot_slots",
       "Webhook ON; LINE Login channel còn ≥2 slot LIFF",
       "- Bên LINE: webhook URL của Messaging API channel được cập nhật sang URL callback của L Message\n"
       "- Bên LINE: LINE Login channel có thêm ĐÚNG 2 LIFF app mới "
       "(エルメ流入アクション用LIFF + エルメ各種フォーム用LIFF)\n"
       "- DB bảng bots: thêm ĐÚNG 1 bản ghi mới với is_delete = 2\n"
       "- DB bảng bot_contract và bot_slots: KHÔNG thêm bản ghi mới ở bước này\n"
       "- Chuyển sang màn quét QR / kiểm tra kết nối",
       env="PRODUCTION",
       note=MT05 + "Nguồn: Change bot r155 (TR=OK, stg=OK) + r292 (bản #37744). "
            "⚠️ MT-01 — kiến trúc bản ghi bot chưa chốt (tạo mới vs update tại chỗ). "
            "RULE-07 (3 tầng: DB + màn hình + bên LINE) + RULE-08 (webhook/domain → PRODUCTION). "
            "Evidence: ảnh webhook URL bên LINE + ảnh 2 LIFF app + query 3 bảng DB."),

    tc("Cài đặt webhook", "INTG-LINE-001", "Abnormal",
       "Webhook đang TẮT → bấm sang bước tiếp: báo lỗi yêu cầu bật webhook, không tạo bản ghi",
       WH + "\n- Đã tick checkbox webhook\n- Webhook của Messaging API channel đang TẮT trên LINE Developer Console",
       "1. Tắt webhook của Messaging API channel trên LINE Developer Console\n"
       "2. Ở màn webhook, tick checkbox「Webhookをオンに設定した」(tick dù thực tế chưa bật)\n"
       "3. Bấm nút sang bước tiếp\n"
       "4. Đọc thông báo lỗi\n"
       "5. Query DB bảng bots đếm bản ghi is_delete = 2",
       "Webhook OFF bên LINE, nhưng checkbox đã tick",
       "- Báo lỗi「Webhookをオンにして下さい。既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」\n"
       "- KHÔNG chuyển màn\n"
       "- DB: KHÔNG thêm bản ghi bots mới\n"
       "- Bên LINE: KHÔNG tạo LIFF app mới",
       env="PRODUCTION",
       note=MT05 + "Nguồn: Change bot r156 (TR=OK) + r293 (TR=OK) + spec bot-edit/web/api-spec.md:375-379 "
            "(EP-07 response flagError 1 với CHÍNH text lỗi này) → đây là điểm TC và spec KHỚP NHAU. "
            "RULE-08. Evidence: ảnh LINE Console webhook OFF + ảnh thông báo lỗi + query bots."),

    tc("Cài đặt webhook", "INTG-LINE-001", "Boundary",
       "Webhook đã bật sẵn từ trước (không tắt-bật lại) → xác nhận hệ thống vẫn nhận đúng trạng thái",
       WH + "\n- Webhook của Messaging API channel đã BẬT từ trước, KHÔNG thao tác tắt-bật lại",
       "1. Xác nhận webhook đang ON (và không tắt-bật lại)\n"
       "2. Tick checkbox, bấm nút sang bước tiếp\n"
       "3. Quan sát: đi tiếp được hay báo lỗi yêu cầu tắt-bật lại\n"
       "4. Nếu báo lỗi: tắt rồi bật lại webhook, thử lại và quan sát",
       "Webhook ON sẵn, không toggle",
       "- Ghi nhận hành vi thực tế: đi tiếp được, HOẶC báo lỗi yêu cầu tắt-bật lại\n"
       "- Nếu báo lỗi thì sau khi tắt-bật lại phải đi tiếp được\n"
       "- Thông báo lỗi (nếu có) phải nêu rõ cách xử lý, không chỉ nói 'lỗi'",
       env="PRODUCTION",
       note=MT05 + "⚠️ Đây là case biên SUY LUẬN từ chính nội dung message lỗi "
            "「既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」(Change bot r156 + spec api-spec.md:377) "
            "— message hàm ý hệ thống có thể KHÔNG nhận được trạng thái ON nếu user không toggle. "
            "Không nguồn TC nào cover nhánh này → cần Leader xác nhận expected. RULE-08. "
            "Evidence: ảnh LINE Console + ảnh kết quả.",
       spec="Đã hỏi leader"),
]

S6 = [
    # ═══════════════ 6. Xác nhận thông tin kết nối ═══════════════
    tc("Xác nhận thông tin kết nối", "FUNC-001", "Normal",
       "Màn xác nhận hiển thị đúng thông tin LOA mới lấy từ LINE API — tên, ID, ảnh, số bạn bè",
       CF,
       "1. Vào màn xác nhận thông tin kết nối\n"
       "2. So sánh tên bot hiển thị với tên LOA mới bên LINE Official Account Manager\n"
       "3. So sánh Bot ID / LINE ID hiển thị với giá trị bên LINE\n"
       "4. So sánh số bạn bè hiển thị với số friend thực tế của LOA mới bên LINE\n"
       "5. Quan sát ảnh đại diện LOA",
       "LOA mới: tên + LINE ID + số friend lấy từ LINE OA Manager",
       "- Tên bot hiển thị KHỚP tên LOA mới bên LINE (không phải tên LOA cũ)\n"
       "- LINE ID / Bot ID hiển thị KHỚP giá trị bên LINE\n"
       "- Số bạn bè hiển thị KHỚP số friend thực tế của LOA mới bên LINE\n"
       "- Ảnh đại diện là ảnh của LOA mới",
       note="Nguồn: Change bot r294-r296 (TR=OK) + TC-CBF-046 (BR-17; Blocked cả 2 env). "
            "RULE-07 — đối chiếu 3 nơi (màn L Message · LINE OA Manager · DB). "
            "Evidence: ảnh màn xác nhận + ảnh LINE OA Manager cùng khung."),

    tc("Xác nhận thông tin kết nối", "FUNC-001", "Normal",
       "Màn xác nhận hiển thị đủ thông tin khối Messaging API channel",
       CF,
       "1. Quan sát khối「メッセージングAPIチャネル」\n"
       "2. Đối chiếu チャネル名 với tên channel bên LINE Developers\n"
       "3. Đối chiếu チャネルID với Channel ID đã nhập ở bước trước\n"
       "4. Đối chiếu チャネルシークレット với secret đã nhập\n"
       "5. Đối chiếu Bot ID với LINE ID của bot",
       "4 giá trị đã nhập ở bước trước",
       "- チャネル名 hiển thị đúng tên channel bên LINE Developers\n"
       "- チャネルID hiển thị ĐÚNG giá trị user vừa nhập\n"
       "- チャネルシークレット hiển thị đúng (theo quy tắc mask ở TC kế tiếp)\n"
       "- Bot ID hiển thị đúng LINE ID của bot",
       note="Nguồn: Change bot r297-r300 (TR=OK). Evidence: ảnh khối メッセージングAPIチャネル + ảnh LINE Developers."),

    tc("Xác nhận thông tin kết nối", "FUNC-001", "Normal",
       "Màn xác nhận hiển thị đủ thông tin khối LINE Login channel",
       CF,
       "1. Quan sát khối「LINEログインチャンネル」\n"
       "2. Đối chiếu チャネルID với Channel ID LINE Login đã nhập\n"
       "3. Đối chiếu チャネルシークレット với secret LINE Login đã nhập",
       "2 giá trị LINE Login đã nhập",
       "- チャネルID hiển thị ĐÚNG giá trị LINE Login user vừa nhập\n"
       "- チャネルシークレット hiển thị đúng theo quy tắc mask\n"
       "- Không lẫn giá trị của Messaging API channel sang khối này",
       note="Nguồn: Change bot r301-r302 (TR=OK). Evidence: ảnh khối LINEログインチャンネル."),

    tc("Xác nhận thông tin kết nối", "SEC-002", "Normal",
       "Channel secret ở màn xác nhận hiển thị dạng masked, KHÔNG có toggle xem đầy đủ",
       CF,
       "1. Quan sát giá trị 2 field Channel secret ở màn xác nhận\n"
       "2. Tìm xem có icon toggle con mắt nào không\n"
       "3. Thử select chuột qua giá trị secret rồi copy, paste ra ô text\n"
       "4. Xem HTML element của field (DevTools Inspect) và response body",
       "Secret 32 ký tự",
       "- Secret hiển thị dạng MASKED (chỉ thấy một phần, VD 4 ký tự đầu + ●●●)\n"
       "- KHÔNG có toggle để xem đầy đủ ở màn này (khác màn nhập)\n"
       "- Copy giá trị hiển thị ra: chỉ được chuỗi đã mask, không phải secret thật\n"
       "- HTML element và response body KHÔNG chứa secret đầy đủ dạng plaintext",
       note="Nguồn: TC-CBF-047 (SEC-002, BR-18; Blocked cả 2 env) + TC-CBF-101 (TD EP-11 'Mask sensitive "
            "data'). ⚠️ MÂU THUẪN NỘI BỘ CẦN LƯU Ý: Change bot r299/r302 ghi expected là "
            "'hiển thị đúng Channel secret' (tức hiển thị đầy đủ) — xem MT-15. "
            "Evidence: ảnh field + ảnh DevTools Inspect + ảnh response body."),

    tc("Xác nhận thông tin kết nối", "FUNC-001", "Normal",
       "Tag trạng thái「有効」và「接続済み」hiển thị đúng trên màn xác nhận",
       CF,
       "1. Quan sát các tag/nhãn trạng thái trên màn xác nhận\n"
       "2. Ghi lại text từng tag\n"
       "3. Đối chiếu với trạng thái thật của channel bên LINE (đang bật/đã kết nối)",
       "LOA mới đã validate thành công",
       "- Hiển thị tag「有効」cho channel đang hoạt động\n"
       "- Hiển thị tag「接続済み」cho phần đã kết nối\n"
       "- Tag khớp trạng thái thật bên LINE, không hiển thị 有効 khi channel đã bị vô hiệu",
       note="Nguồn: TC-CBF-048 (BR-19; Blocked cả 2 env). Evidence: ảnh tag + ảnh trạng thái bên LINE."),

    tc("Xác nhận thông tin kết nối", "UI-003", "Normal",
       "Hộp cảnh báo「入れ替えを実行すると元に戻せません」hiển thị rõ, không bị che khuất",
       CF,
       "1. Vào màn xác nhận thông tin kết nối\n"
       "2. Tìm hộp cảnh báo về việc không thể hoàn tác\n"
       "3. Quan sát ở độ phân giải 1366×768: hộp cảnh báo có bị cắt/che không\n"
       "4. Scroll trang, quan sát hộp cảnh báo có nằm trong vùng nhìn thấy trước nút xác nhận không",
       "Độ phân giải 1366×768",
       "- Hộp cảnh báo hiển thị rõ, chữ đọc được, không bị cắt\n"
       "- Hộp cảnh báo nằm TRƯỚC (phía trên) nút xác nhận trong luồng đọc\n"
       "- Không bị element khác đè lên\n"
       "- Ở 1366×768 vẫn thấy được cảnh báo mà không cần scroll qua nút xác nhận",
       note="Nguồn: TC-CBF-052 (UI-003, BR-20 warning box; Blocked cả 2 env) + TC-CBF-105 (UI-001 + UIC-13, "
            "độ phân giải tối thiểu 1366×768). Đổi LOA là thao tác KHÔNG hoàn tác được nên cảnh báo này là "
            "rào chắn cuối. Evidence: ảnh full màn ở 1366×768."),

    tc("Xác nhận thông tin kết nối", "FUNC-DRAFT-001", "Normal",
       "Bấm「キャンセル」ở màn xác nhận → quay về màn nhập, 4 field GIỮ NGUYÊN giá trị",
       CF,
       "1. Ở màn xác nhận, ghi lại 4 giá trị đang hiển thị\n"
       "2. Bấm nút「キャンセル」\n"
       "3. Quan sát màn hình đích\n"
       "4. Đối chiếu 4 field với giá trị đã ghi ở bước 1",
       "4 field đã validate thành công",
       "- Quay về màn nhập thông tin kết nối\n"
       "- CẢ 4 field GIỮ NGUYÊN giá trị (không bị xóa, không phải nhập lại)\n"
       "- Nút CTA vẫn ở trạng thái ENABLED (vì 4/4 field có data)",
       note="Nguồn: TC-CBF-050 (FUNC-DRAFT-001, BR-21/FN-12, QA-spec-024 CONFIRMED; Blocked cả 2 env) "
            "+ Change bot r303 (bản #37744: 'back về màn 2, data đã nhập trước đó vẫn còn'). "
            "Evidence: ảnh 4 field trước/sau khi bấm キャンセル."),

    tc("Xác nhận thông tin kết nối", "OUT-TRUTH-001", "Normal",
       "Bấm「この内容で接続する」rẽ nhánh ĐÚNG theo phương thức đã chọn ở bước 1",
       CF,
       "1. Chạy luồng với option 1 (đổi ngay) đến màn xác nhận, bấm「この内容で接続する」→ ghi màn đích\n"
       "2. Làm lại từ đầu, chọn option 2 (đặt lịch) đến màn xác nhận, bấm「この内容で接続する」→ ghi màn đích\n"
       "3. Đối chiếu 2 màn đích\n"
       "4. Query DB sau mỗi nhánh: bảng bots và schedule_change_bots",
       "2 lần chạy: option 1 và option 2",
       "- Nhánh option 1 (đổi ngay): sang màn quét QR / tiến trình đổi LOA\n"
       "- Nhánh option 2 (đặt lịch): sang màn đã đặt lịch (「05-A 予約済み」) / màn item đặt lịch\n"
       "- KHÔNG nhánh nào đi sai màn của nhánh kia\n"
       "- Nhánh đặt lịch: DB schedule_change_bots có thêm 1 bản ghi; nhánh đổi ngay thì không",
       note="Nguồn: TC-CBF-049 (OUT-TRUTH-001, BR-20/FN-13, QA-spec-025 CONFIRMED; Blocked cả 2 env) "
            "+ Change bot r304 (bản #37744: 'Next màn sau đó, hiển thị màn item đặt lịch'). "
            "⚠️ MT-11 — tên bảng: spec job ghi `schedule_change_bot` (số ít), TC ghi `schedule_change_bots`. "
            "RULE-07. Evidence: ảnh 2 màn đích + query DB 2 nhánh."),

    tc("Xác nhận thông tin kết nối", "CONC-001", "Boundary",
       "Double-click「この内容で接続する」→ chỉ 1 lần đổi LOA / 1 bản ghi đặt lịch, không trùng",
       CF,
       "1. Mở DevTools tab Network, xóa log\n"
       "2. Double-click nhanh (<300ms) vào nút「この内容で接続する」\n"
       "3. Đếm số request trong Network\n"
       "4. Query DB: đếm bản ghi trong schedule_change_bots (nhánh đặt lịch) hoặc bots is_delete=2 (nhánh đổi ngay)",
       "Double-click trong 300ms",
       "- Network: ĐÚNG 1 request (hoặc request thứ 2 bị server trả lỗi idempotent, không tạo thêm data)\n"
       "- DB: ĐÚNG 1 bản ghi mới, KHÔNG có 2 bản ghi trùng\n"
       "- Không khởi động 2 tiến trình đổi LOA song song",
       note="Nguồn: TC-CBF-051 (CONC-001, cross-ref EP-06/EP-08 idempotency; Blocked cả 2 env). "
            "CONC-001 BẮT BUỘC khi có nút thực thi hành động quan trọng. RULE-07. "
            "Evidence: Network đếm request + query DB."),

    tc("Xác nhận thông tin kết nối", "FUNC-SEQ-001", "Boundary",
       "F5 reload ở màn xác nhận → thông tin đã validate không được giữ, quay về đầu flow",
       CF,
       "1. Ở màn xác nhận, bấm F5\n"
       "2. Quan sát màn hình sau khi load xong\n"
       "3. Nếu về đầu flow: kiểm tra 4 field có còn giá trị không\n"
       "4. Query DB: có bản ghi bots is_delete=2 nào bị bỏ rơi không",
       "F5 tại màn xác nhận",
       "- Ghi nhận hành vi thật: quay về đầu flow (màn chọn phương thức) hoặc giữ màn xác nhận\n"
       "- Nếu quay về đầu flow: 4 field trống, phải nhập lại\n"
       "- DB: KHÔNG để lại bản ghi bots is_delete=2 rác (nếu có thì là bug rác dữ liệu)",
       note="Nguồn: TC-CBF-053 (FUNC-SEQ-001; Blocked cả 2 env). "
            "⚠️ Ghi chú nguồn: 'verify hành vi thực tế, spec không mô tả rõ persistence tại bước này' → "
            "TC này GHI NHẬN hành vi, cần Leader chốt expected chính thức. "
            "Evidence: ảnh màn sau F5 + query bots.",
       spec="Đã hỏi leader"),

    tc("Xác nhận thông tin kết nối", "DATA-REF-001", "Normal",
       "Cảnh báo LIFF ID đổi làm ảnh hưởng các tính năng đã tạo — hiển thị TRƯỚC khi thực hiện đổi LOA",
       CF + "\n- Bot cũ đã có sẵn: ≥1 form, ≥1 item, ≥1 lịch salon/lesson, ≥1 event, ≥1 QR code action",
       "1. Vào màn xác nhận thông tin kết nối\n"
       "2. Đọc toàn bộ nội dung cảnh báo trên màn\n"
       "3. Kiểm tra cảnh báo có nêu rõ các tính năng bị ảnh hưởng do LIFF ID đổi không\n"
       "4. Đếm số tính năng được liệt kê",
       "Bot cũ có đủ 5 loại đối tượng dùng LIFF",
       "- Có cảnh báo về việc LIFF ID thay đổi sau khi đổi LOA\n"
       "- Cảnh báo liệt kê các tính năng bị ảnh hưởng: form trả lời, sản phẩm, đặt lịch calendar, "
       "đặt lịch sự kiện, QR code action (流入アクション)\n"
       "- Cảnh báo xuất hiện TRƯỚC khi user bấm nút xác nhận, không phải sau khi đã đổi",
       note="Nguồn: TC-CBF-065 (DATA-REF-001, TD Section 7.3 + BR-41 + CM-005; Blocked cả 2 env). "
            "⚠️ MT-16 — spec bot-edit/ui-spec.md:208-240 (SCR-BE-04) có CHÍNH nội dung cảnh báo này nhưng "
            "cho thao tác kết nối lại LIFF, KHÔNG phải cho đổi LOA → chưa rõ đổi LOA có cảnh báo tương đương. "
            "DATA-REF-001 BẮT BUỘC khi đối tượng được nơi khác tham chiếu. Evidence: ảnh full cảnh báo."),
]
