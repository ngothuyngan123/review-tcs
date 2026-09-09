# -*- coding: utf-8 -*-
"""FA-001 Chat 1:1 — Nhóm 5: đặt lịch gửi, preview trước khi gửi, panel thông tin bạn bè (5 tab)."""
from _common import tc

BOT = "- Đăng nhập admin (user chính), đang chọn bot A\n- Màn hình /basic/chat-v3, đang mở hội thoại friend A"
SCH = BOT + "\n- Đã click icon 送信予約 để vào màn đặt lịch gửi của friend A"

S5 = [
    # ═══════════════ Đặt lịch gửi — soạn & lưu ═══════════════
    tc("Đặt lịch gửi — soạn & lưu", "UI-001", "Normal",
       "Vào màn đặt lịch gửi — header, đường dẫn quay lại và giá trị ngày giờ mặc định",
       BOT,
       "1. Click icon 送信予約 ở màn chat 1:1\n2. Quan sát header và tiêu đề màn\n"
       "3. Đọc ngày và giờ mặc định\n4. Click vào「1:1チャット」ở header",
       "Mở màn đặt lịch lần đầu, chưa có bản ghi nào",
       "- Chuyển sang màn 送信日時, header hiện đường dẫn「1:1チャット / 送信予約」\n"
       "- Ngày mặc định = ngày hiện tại; giờ mặc định = 3 giờ sau thời điểm hiện tại\n"
       "- Chưa có tin nhắn: hiện「メッセージが登録されていません」\n"
       "- Click「1:1チャット」: quay lại màn chat 1:1",
       note="Nguồn: Rightbar r253-r259, r255"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-DATE-001", "Abnormal",
       "Chọn thời gian gửi trong quá khứ — bị chặn",
       SCH,
       "1. Chọn ngày/giờ TRƯỚC thời điểm hiện tại\n2. Bấm lưu\n3. Quan sát thông báo",
       "Ngày giờ = hôm qua",
       "- Hiện thông báo「日時は現在時刻より前に設定できません」\n- Không lưu được lịch gửi",
       note="Nguồn: Rightbar r260"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Thêm tin nhắn mới cho lịch gửi qua nút メッセージ追加",
       SCH,
       "1. Hover nút メッセージ追加 → quan sát hiệu ứng\n2. Click nút\n"
       "3. Soạn nội dung tin nhắn text → lưu\n4. Quan sát danh sách tin nhắn của lịch gửi\n"
       "5. Double click nút メッセージ追加 → kiểm tra Network",
       "1 tin nhắn text",
       "- Hover: nút đổi màu xanh, chữ trắng\n"
       "- Click: chuyển sang màn soạn nội dung tin nhắn\n"
       "- Sau khi lưu: tin nhắn xuất hiện trong danh sách của lịch gửi\n"
       "- Double click: chỉ 1 request, không tạo 2 bản ghi",
       note="Nguồn: Rightbar r261-r263"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Thêm tin nhắn từ template — 2 chế độ dùng trực tiếp và sao chép nội dung",
       SCH + "\n- Có group template T dạng text",
       "1. Click nút テンプレートから追加\n2. Chọn chế độ「テンプレートをそのまま利用する」→ chọn T → lưu\n"
       "3. Sang màn Quản lý template, SỬA nội dung T → quay lại màn đặt lịch kiểm tra nội dung\n"
       "4. Lặp lại với chế độ「テンプレートを引用して編集する」rồi cũng sửa T gốc → kiểm tra",
       "Template T, 2 chế độ thêm",
       "- Chế độ dùng trực tiếp: nội dung trong lịch gửi ĐỔI THEO khi template gốc bị sửa\n"
       "- Chế độ sao chép: nội dung trong lịch gửi GIỮ NGUYÊN khi template gốc bị sửa",
       note="2 chế độ có kết quả khác hẳn nhưng cùng 1 chuỗi kiểm chứng. Nguồn: Rightbar r264-r268"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-DRAFT-001", "Abnormal",
       "Thêm tin nhắn nhưng KHÔNG lưu rồi quay về chat 1:1 — lưu nháp, không gửi",
       SCH,
       "1. Thêm 1 tin nhắn vào lịch gửi\n2. KHÔNG bấm nút lưu, quay về màn chat 1:1\n"
       "3. Quan sát dòng của friend A: có icon đồng hồ không\n"
       "4. Kiểm tra DB bảng lịch gửi: trường trạng thái\n"
       "5. Mở lại màn đặt lịch → kiểm tra bản ghi còn không",
       "1 tin nhắn chưa lưu",
       "- Dòng friend A: KHÔNG hiện icon đồng hồ ở danh sách\n"
       "- Tin nhắn KHÔNG được gửi cho friend\n"
       "- DB: bản ghi lịch gửi có trạng thái nháp (-1)\n"
       "- Mở lại màn đặt lịch: bản ghi chưa lưu vẫn còn để soạn tiếp",
       note="Khớp spec BR-11 (feature-spec.md:473 — trạng thái -1 là nháp). Nguồn: Rightbar r269-r271"),

    tc("Đặt lịch gửi — soạn & lưu", "SYNC-APP-001", "Abnormal",
       "Bản ghi lịch gửi đang ở trạng thái nháp — thao tác từ app mobile ghi đè thành chờ gửi",
       "- Đã có bản ghi lịch gửi ở trạng thái nháp cho friend A (soạn trên web, chưa lưu)\n"
       "- App mobile LME đăng nhập account admin bot A",
       "1. Ở app mobile: mở icon đặt lịch của friend A, nhập tin nhắn đặt lịch\n"
       "2. Kiểm tra DB bảng lịch gửi: trạng thái bản ghi\n"
       "3. Chờ tới giờ, kiểm tra friend có nhận tin không",
       "Bản ghi nháp trên web + thao tác từ app mobile",
       "- Bản ghi bị ghi đè, trạng thái chuyển thành chờ gửi (0)\n- Tới giờ thì tin được gửi cho friend",
       env="PRODUCTION", spec="Spec không ghi",
       note="Nguồn: Rightbar r272"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Sắp xếp thứ tự tin nhắn trong lịch gửi — kéo thả và nút chuyển lên đầu / xuống cuối",
       SCH + "\n- Lịch gửi đã có ≥4 tin nhắn",
       "1. Bấm nút 並び替え → quan sát danh sách trong modal có khớp danh sách ngoài không\n"
       "2. Kéo tin đầu tiên xuống dưới, kéo tin cuối lên trên, kéo nhiều tin → lưu\n"
       "3. Dùng menu 3 chấm: chuyển 1 tin lên đầu → lưu; chuyển 1 tin xuống cuối → lưu\n"
       "4. Kiểm tra nút 一番上に移動 ở tin đầu và nút 一番下に移動 ở tin cuối\n"
       "5. Kiểm tra thứ tự ngoài màn danh sách",
       "4 tin nhắn trong lịch gửi",
       "- Modal sắp xếp hiển thị đúng danh sách như ngoài màn\n"
       "- Kéo thả và nút chuyển đều đổi đúng vị trí\n"
       "- Tin đang ở đầu: nút 一番上に移動 bị vô hiệu; tin ở cuối: nút 一番下に移動 bị vô hiệu\n"
       "- Sau khi lưu: thứ tự ngoài màn danh sách khớp thứ tự trong modal",
       note="Gộp vì cùng thuộc chức năng sắp xếp. Nguồn: Rightbar r328-r345"),

    tc("Đặt lịch gửi — soạn & lưu", "STATE-CLEAN-001", "Abnormal",
       "Sắp xếp nhưng không lưu — thứ tự giữ nguyên",
       SCH + "\n- Lịch gửi đã có ≥3 tin nhắn",
       "1. Ghi lại thứ tự hiện tại\n2. Mở modal sắp xếp, kéo thả đổi thứ tự\n"
       "3. Bấm X đóng modal (không lưu)\n4. Quan sát thứ tự ngoài màn danh sách",
       "3 tin nhắn, đổi thứ tự rồi đóng X",
       "- Thứ tự ngoài màn danh sách KHÔNG đổi, giữ nguyên như trước",
       note="Nguồn: Rightbar r341, r342, r347"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Xoá từng tin nhắn trong lịch gửi — có xác nhận, không ảnh hưởng tin đã gửi",
       SCH + "\n- Lịch gửi có 3 tin nhắn; friend A đã nhận vài tin trong lịch sử chat",
       "1. Bấm icon xoá 1 tin nhắn\n2. Đọc thông báo xác nhận\n3. Bấm Cancel → kiểm tra tin còn không\n"
       "4. Bấm xoá lại → OK → kiểm tra danh sách\n5. Quay lại chat 1:1 kiểm tra lịch sử tin đã gửi",
       "3 tin nhắn trong lịch gửi",
       "- Thông báo xác nhận hiện「削除しますが、宜しいですか？」\n"
       "- Bấm Cancel: tin vẫn còn; bấm OK: tin biến mất khỏi danh sách\n"
       "- Lịch sử chat 1:1: các tin ĐÃ GỬI cho friend vẫn còn nguyên",
       note="Nguồn: Rightbar r346-r349"),

    tc("Đặt lịch gửi — soạn & lưu", "BULK-001", "Normal",
       "Xoá hàng loạt tin nhắn trong lịch gửi",
       SCH + "\n- Lịch gửi có ≥3 tin nhắn",
       "1. Quan sát nút 一括削除 khi chưa tick tin nào\n2. Tick 1 tin → quan sát nút\n"
       "3. Tick nhiều tin → bấm 一括削除 → quan sát popup xác nhận → xác nhận\n"
       "4. Kiểm tra danh sách và trạng thái nút\n5. Quay lại chat 1:1 kiểm tra tin đã gửi",
       "3 tin nhắn, xoá 2 tin",
       "- Chưa tick: nút 一括削除 vô hiệu; tick ≥1 tin: nút hoạt động\n"
       "- Sau khi xác nhận: các tin đã tick biến mất, nút trở lại vô hiệu\n"
       "- Lịch sử chat 1:1 giữ nguyên các tin đã gửi",
       note="Nguồn: Rightbar r350-r355"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Lưu lịch gửi — lưu được cả khi chưa có tin nhắn nào, sau đó quay về chat 1:1",
       SCH,
       "1. Hover nút 保存 → quan sát\n2. Khi chưa có tin nào: bấm 保存 → quan sát kết quả\n"
       "3. Thêm 2 tin nhắn, chọn ngày giờ hợp lệ → bấm 保存\n"
       "4. Quan sát điều hướng và dòng friend A ở danh sách\n"
       "5. Kiểm tra DB: trạng thái và thời điểm gửi của bản ghi lịch",
       "Lưu khi chưa có tin và khi có 2 tin",
       "- Hover: nút đổi màu xanh\n- Nút 保存 hoạt động kể cả khi chưa có tin nào (lưu ngày giờ)\n"
       "- Sau khi lưu: quay về màn chat 1:1, dòng friend A hiện icon đồng hồ\n"
       "- DB: trạng thái = chờ gửi (0), thời điểm gửi khớp giá trị đã chọn",
       note="Nguồn: Rightbar r356-r358 + spec BR-11"),

    tc("Đặt lịch gửi — soạn & lưu", "FUNC-001", "Normal",
       "Huỷ đặt lịch — nút chỉ hiện khi đang sửa lịch đã lưu, huỷ thì xoá toàn bộ",
       BOT + "\n- Friend A đã có lịch gửi đã lưu với 3 tin nhắn",
       "1. Vào màn đặt lịch khi CHƯA có tin nào → tìm nút 予約を取り消す\n"
       "2. Mở lại lịch gửi đã lưu của friend A → tìm nút\n"
       "3. Bấm 予約を取り消す → quan sát danh sách tin và dòng friend A ở chat 1:1\n"
       "4. Kiểm tra DB",
       "Lịch gửi có 3 tin nhắn đã lưu",
       "- Khi chưa có tin: nút 予約を取り消す KHÔNG hiển thị\n"
       "- Khi đang sửa lịch đã lưu: nút hiển thị\n"
       "- Bấm huỷ: toàn bộ tin nhắn trong lịch bị xoá, icon đồng hồ của friend A biến mất\n"
       "- DB: bản ghi lịch chuyển sang trạng thái đã huỷ hoặc bị xoá",
       note="Nguồn: Rightbar r359-r363"),

    # ═══════════════ Đặt lịch gửi — preview & send test ═══════════════
    tc("Đặt lịch gửi — preview & send test", "UI-001", "Normal",
       "Mở màn xem trước / gửi thử từ lịch gửi",
       SCH + "\n- Lịch gửi đã có ≥1 tin nhắn",
       "1. Hover nút プレビュー・テスト và hover icon tương ứng → quan sát\n"
       "2. Click nút → quan sát màn mở ra\n3. Click vào liên kết「こちら」",
       "Lịch gửi có tin nhắn",
       "- Hover nút: đổi màu xanh, chữ trắng; hover icon: hiện chú thích「プレビュー・テスト」\n"
       "- Click: mở màn xem trước / gửi thử đúng thiết kế\n"
       "- Click「こちら」: mở trang hướng dẫn gửi thử ở tab mới",
       note="Nguồn: Rightbar r273-r277"),

    tc("Đặt lịch gửi — preview & send test", "FUNC-002", "Normal",
       "Tìm kiếm bạn bè để đăng ký tài khoản gửi thử",
       SCH + "\n- Bot A có ≥30 bạn bè",
       "1. Click vào ô tìm kiếm khi chưa gõ gì → quan sát danh sách gợi ý\n"
       "2. Nhập từ khoá: đúng tên, gần đúng, chữ hoa, chữ thường\n"
       "3. Nhập từ khoá có khoảng trắng đầu/cuối\n"
       "4. Nhập tên KHÔNG tồn tại\n5. Với kết quả nhiều: thử cuộn",
       "Từ khoá đúng / gần đúng / hoa / thường / có khoảng trắng thừa / không tồn tại",
       "- Click vào ô tìm kiếm: tự hiện 20 bạn bè đầu tiên\n"
       "- Từ khoá đúng, gần đúng, hoa, thường: đều ra kết quả khớp\n"
       "- Khoảng trắng đầu/cuối được tự cắt bỏ\n"
       "- Tên không tồn tại: không hiện bạn bè nào\n- Kết quả nhiều: có cuộn",
       note="Gộp vì cùng chức năng tìm kiếm. Nguồn: Rightbar r278-r286"),

    tc("Đặt lịch gửi — preview & send test", "FUNC-UNIQ-001", "Normal",
       "Đăng ký và xoá tài khoản gửi thử — không đăng ký trùng",
       SCH,
       "1. Tìm friend A → bấm nút thêm → quan sát danh sách tài khoản test\n"
       "2. Quan sát nút thêm của friend A sau khi đã thêm\n"
       "3. Double click nút thêm khi đang bật và khi đã vô hiệu\n"
       "4. Xoá friend A khỏi danh sách test → quan sát nút thêm của A\n"
       "5. Thêm nhiều tài khoản test → kiểm tra cuộn danh sách",
       "Friend A và ≥10 friend khác",
       "- Sau khi thêm: A xuất hiện trong danh sách tài khoản test, nút thêm của A bị vô hiệu\n"
       "- Double click: chỉ tính 1 lần, không thêm trùng\n"
       "- Sau khi xoá khỏi danh sách test: nút thêm của A hoạt động trở lại\n"
       "- Danh sách dài: có cuộn",
       note="Gộp vì cùng chuỗi thao tác. Nguồn: Rightbar r287-r294, r304-r306"),

    tc("Đặt lịch gửi — preview & send test", "MSG-001", "Normal",
       "Gửi thử tới từng tài khoản và gửi thử hàng loạt",
       SCH + "\n- Lịch gửi có group template nhiều tin con\n- Đã đăng ký ≥3 tài khoản test",
       "1. Bấm nút テスト送信 ở 1 tài khoản → quan sát thông báo → kiểm tra app LINE của tài khoản đó\n"
       "2. Double click nút テスト送信 → kiểm tra số tin nhận\n"
       "3. Khi chưa tick tài khoản nào: quan sát nút 一括テスト送信\n"
       "4. Tick nhiều tài khoản → bấm 一括テスト送信 → kiểm tra app LINE của từng tài khoản",
       "3 tài khoản test, group template có 3 tin con",
       "- Gửi từng tài khoản: hiện thông báo thành công, tài khoản nhận đủ tin trên app LINE\n"
       "- Double click: chỉ gửi 1 lần\n"
       "- Chưa tick: nút 一括テスト送信 vô hiệu; tick ≥1: nút hoạt động\n"
       "- Gửi hàng loạt: mọi tài khoản đã tick đều nhận ĐỦ tin con của group template",
       env="PRODUCTION",
       note="Đi tới output cuối app LINE (RULE-06). Nguồn: Rightbar r295-r303"),

    tc("Đặt lịch gửi — preview & send test", "FUNC-001", "Boundary",
       "Danh sách gửi thử nhanh — tối đa 3 tài khoản, đồng bộ với màn Template",
       SCH + "\n- Đã đăng ký ≥5 tài khoản test",
       "1. Quan sát icon gửi thử nhanh khi chưa chọn tài khoản nào\n"
       "2. Bật gửi thử nhanh cho 3 tài khoản\n"
       "3. Rê chuột vào icon của tài khoản THỨ 4 → đọc thông báo\n"
       "4. Rê chuột vào icon của 1 trong 3 tài khoản đã bật → đọc thông báo → click bỏ\n"
       "5. Sang màn Template, kiểm tra danh sách gửi thử nhanh",
       "5 tài khoản test, giới hạn 3 tài khoản gửi thử nhanh",
       "- Mặc định icon ở trạng thái vô hiệu\n"
       "- Bật được tối đa 3 tài khoản\n"
       "- Tài khoản thứ 4: hiện「クイックテストユーザーに登録（3人まで)」và KHÔNG bật được\n"
       "- Tài khoản đã bật: hiện「クイックテストユーザーの登録を解除」, click thì bị gỡ khỏi danh sách\n"
       "- Màn Template hiển thị ĐỒNG BỘ đúng 3 tài khoản đó",
       note="Nguồn: Rightbar r307-r314"),

    tc("Đặt lịch gửi — preview & send test", "OUT-PREVIEW-001", "Normal",
       "Xem trước nội dung lịch gửi — đủ template con, đúng thứ tự, quick reply ở cuối",
       SCH + "\n- Lịch gửi có group template gồm đủ loại tin con",
       "1. Mở màn xem trước\n2. Kiểm tra hiển thị từng loại tin ở cột Dữ liệu test\n"
       "3. Kiểm tra thứ tự các tin con so với màn danh sách template\n"
       "4. Với nội dung ít: kiểm tra không có cuộn thừa; với nội dung nhiều: kiểm tra cuộn",
       "Template text (tiếng Nhật dài) · button standard / màu / ảnh / quick reply · "
       "media (ảnh, video, audio) · sticker · vị trí",
       "- Xem trước hiển thị ĐỦ các tin con của group template\n"
       "- Thứ tự khớp thứ tự ở màn danh sách template, riêng quick reply luôn nằm CUỐI danh sách\n"
       "- Nội dung dài có cuộn",
       note="Nguồn: Rightbar r315-r327"),

    # ═══════════════ Đặt lịch gửi — delay & job ═══════════════
    tc("Đặt lịch gửi — delay & job", "UI-003", "Normal",
       "Tuỳ chọn gửi giãn cách — mặc định TẮT, bật thì lưu vào cấu hình lịch",
       SCH,
       "1. Quan sát trạng thái mặc định của tuỳ chọn「メッセージを1通ずつ数秒遅延させて送信する」\n"
       "2. Kiểm tra DB trường cấu hình giãn cách của bản ghi lịch\n"
       "3. Bật tuỳ chọn → lưu → kiểm tra lại DB\n"
       "4. Ở màn Template, tắt cấu hình giãn cách của template → kiểm tra DB template",
       "Tuỳ chọn gửi giãn cách của lịch gửi và của template",
       "- Mặc định TẮT, DB lưu giá trị 0\n- Sau khi bật và lưu: DB lưu giá trị 1\n"
       "- Cấu hình của template được lưu riêng, độc lập với cấu hình của lịch gửi",
       note="Nguồn: Rightbar r365-r368"),

    tc("Đặt lịch gửi — delay & job", "JOB-001", "Normal",
       "TẮT gửi giãn cách — mọi tin gửi cùng lúc, không tạo bản ghi hàng đợi",
       SCH + "\n- Lịch gửi đặt vào hôm nay (gần thời điểm hiện tại), có 5 tin đủ loại\n- TẮT tuỳ chọn giãn cách",
       "1. Lưu lịch gửi, chờ tới giờ\n2. Quan sát thứ tự và thời gian các tin ở chat 1:1 web\n"
       "3. Quan sát ở chat 1:1 trên app mobile\n4. Kiểm tra app LINE của friend\n"
       "5. Kiểm tra bảng hàng đợi gửi giãn cách",
       "5 tin: text · button · media · vị trí · sticker · PDF",
       "- Các tin được gửi CÙNG LÚC theo đúng thứ tự đã sắp xếp, không trùng lặp\n"
       "- Hiển thị đúng ở chat 1:1 web, app mobile và app LINE\n"
       "- KHÔNG có bản ghi nào được ghi vào bảng hàng đợi gửi giãn cách",
       env="PRODUCTION",
       note="Job → RULE-08. Nguồn: Rightbar r371-r381"),

    tc("Đặt lịch gửi — delay & job", "JOB-001", "Normal",
       "BẬT gửi giãn cách — tin đầu gửi ngay, các tin sau vào hàng đợi tăng dần thời gian",
       SCH + "\n- Lịch gửi đặt vào hôm nay, có 5 tin đủ loại\n- BẬT tuỳ chọn giãn cách",
       "1. Lưu lịch gửi, chờ tới giờ\n2. Quan sát ở chat 1:1: tin đầu và các tin sau\n"
       "3. Kiểm tra bảng hàng đợi gửi giãn cách: số bản ghi và giá trị thời gian gửi từng bản\n"
       "4. Đo khoảng cách thời gian thực tế giữa các tin trên app LINE của friend",
       "5 tin: text · button · media · vị trí · sticker · PDF",
       "- Tin ĐẦU TIÊN gửi ngay; các tin sau được ghi vào bảng hàng đợi\n"
       "- Thời gian gửi trong hàng đợi TĂNG DẦN theo từng tin\n"
       "- Ghi lại khoảng cách thực tế giữa các tin làm evidence (đối chiếu MT-05: spec 2-4 giây, corpus 2-5 giây)",
       env="PRODUCTION", spec="Đã hỏi leader",
       note="MT-05. Nguồn: Rightbar r382, r383 + spec feature-spec.md:104"),

    tc("Đặt lịch gửi — delay & job", "JOB-001", "Abnormal",
       "Sửa thời gian gửi khi lịch ĐANG gửi dở — các tin còn lại dời theo giờ mới",
       SCH + "\n- Lịch gửi có 5 tin, BẬT giãn cách, đang trong quá trình gửi",
       "1. Trong lúc job đang gửi dở, vào sửa thời gian gửi sang mốc muộn hơn → lưu\n"
       "2. Kiểm tra DB: thời điểm gửi của bản ghi lịch\n"
       "3. Kiểm tra các tin còn lại trong hàng đợi\n"
       "4. Chờ tới mốc mới, kiểm tra friend nhận các tin còn lại",
       "5 tin, sửa giờ khi đang gửi dở",
       "- DB: thời điểm gửi được cập nhật sang mốc mới\n"
       "- Các tin CHƯA gửi vẫn còn trong hàng đợi, KHÔNG bị gửi ở mốc cũ\n"
       "- Tới mốc mới: friend nhận đủ các tin còn lại",
       env="PRODUCTION",
       note="Nguồn: Rightbar r374, r384"),

    tc("Đặt lịch gửi — delay & job", "JOB-001", "Abnormal",
       "Tắt job gửi — tin nằm chờ, bật lại thì gửi tiếp",
       SCH + "\n- Lịch gửi có 3 tin, đã tới giờ gửi\n- Phối hợp với Dev để tắt/bật job",
       "1. Tắt job gửi → chờ qua thời điểm gửi\n"
       "2. Kiểm tra DB: trạng thái bản ghi lịch\n3. Kiểm tra friend có nhận tin không\n"
       "4. Kiểm tra màn đặt lịch trên web còn hiện tin chưa gửi không\n"
       "5. Bật lại job → kiểm tra friend nhận tin",
       "3 tin nhắn, tắt job rồi bật lại",
       "- Khi tắt job: trạng thái bản ghi vẫn là chờ gửi (0), friend CHƯA nhận tin\n"
       "- Màn web vẫn hiển thị các tin chưa gửi\n"
       "- Sau khi bật lại job: friend nhận đủ các tin",
       env="PRODUCTION",
       note="Nguồn: Rightbar r369, r370"),

    tc("Đặt lịch gửi — delay & job", "JOB-001", "Normal",
       "Cấu hình giãn cách của lịch gửi và của template độc lập nhau",
       SCH + "\n- Template T TẮT giãn cách\n- Lịch gửi BẬT giãn cách, dùng template T",
       "1. Lưu lịch gửi (bật giãn cách) với template T (tắt giãn cách)\n"
       "2. Chờ tới giờ gửi\n3. Quan sát khoảng cách thời gian giữa các tin ở chat 1:1 và app LINE\n"
       "4. Ghi nhận cấu hình nào có hiệu lực",
       "Lịch gửi BẬT giãn cách + template TẮT giãn cách",
       "- Ghi nhận hành vi thực tế: các tin gửi cùng lúc hay giãn cách\n"
       "- Đối chiếu với quyết định của Leader nếu 2 cấu hình mâu thuẫn",
       env="PRODUCTION", spec="Spec không ghi",
       note="Spec không mô tả thứ tự ưu tiên giữa cấu hình giãn cách của lịch và của template. Nguồn: Rightbar r391"),

    tc("Đặt lịch gửi — delay & job", "MSG-002", "Normal",
       "Tin gửi bằng lịch — dấu hiệu 予約送信 ở chat 1:1",
       BOT + "\n- Friend A có lịch gửi đã tới giờ và đã gửi xong",
       "1. Mở hội thoại friend A sau khi lịch đã gửi\n2. Quan sát dấu hiệu của các tin do lịch gửi\n"
       "3. Kiểm tra tin trên app LINE của friend",
       "Lịch gửi 2 tin đã gửi xong",
       "- Các tin hiển thị kèm nhãn「予約送信」ở chat 1:1\n- Friend nhận đủ tin trên app LINE",
       env="PRODUCTION",
       note="Nguồn: spec feature-spec.md:117 + Content: Hiển thị msg r866-r870 (Support #29869)"),

    # ═══════════════ Preview trước khi gửi ═══════════════
    tc("Preview trước khi gửi", "UI-003", "Normal",
       "Bật / tắt xem trước ở màn cài đặt chat — quyết định có hiện modal khi gửi",
       BOT,
       "1. Ở màn cài đặt chat: BẬT 送信プレビュー → quay lại chat 1:1, gõ tin và bấm gửi → quan sát\n"
       "2. Ở màn cài đặt chat: TẮT 送信プレビュー → gõ tin và bấm gửi → quan sát",
       "2 trạng thái cài đặt xem trước",
       "- BẬT: hiện modal xem trước trước khi gửi\n- TẮT: gửi thẳng, KHÔNG hiện modal",
       note="Nguồn: Rightbar r395, r396"),

    tc("Preview trước khi gửi", "OUT-PREVIEW-001", "Normal",
       "Modal xem trước — nội dung khớp tin sẽ gửi, hiện đúng tên và ảnh người gửi",
       BOT + "\n- BẬT 送信プレビュー\n- Đang chọn profile người gửi P1",
       "1. Gõ tin nhắn, bấm gửi → modal xem trước hiện ra\n"
       "2. Đối chiếu nội dung trong modal với nội dung đã gõ\n"
       "3. Đọc tên và ảnh người gửi trong modal\n4. Đổi sang profile P2 → lặp lại",
       "Tin text; profile P1 rồi P2",
       "- Modal hiển thị đúng thiết kế, nội dung khớp tin sẽ gửi\n"
       "- Tên và ảnh người gửi khớp profile đang chọn (P1, sau đó P2)",
       note="Nguồn: Rightbar r397, r407, r408"),

    tc("Preview trước khi gửi", "OUT-PREVIEW-001", "Normal",
       "Xem trước — đủ loại nội dung text, URL và media",
       BOT + "\n- BẬT 送信プレビュー\n- Đã tạo sẵn form, lịch calendar/salon/event booking",
       "1. Với mỗi nội dung ở cột Dữ liệu test: gõ/chọn rồi bấm gửi\n2. Quan sát modal xem trước",
       "Text latinh · text tiếng Nhật · text xuống dòng · text + ảnh · URL thường · URL form · "
       "URL calendar booking · URL salon booking · URL event booking · ảnh JPG/PNG · ảnh vuông/dọc/ngang · "
       "nhiều ảnh cùng lúc · audio M4A · video MP4 · file PDF",
       "- Modal xem trước hiển thị đúng và đủ mọi loại nội dung trên\n"
       "- Ảnh được co giãn hợp lý theo khung xem trước\n"
       "- File audio/video/PDF hiện đúng tên và định dạng",
       note="Gộp vì cùng kết quả. Nguồn: Rightbar r409-r425"),

    tc("Preview trước khi gửi", "FUNC-001", "Normal",
       "Gửi từ modal xem trước — tin được gửi và modal tự đóng",
       BOT + "\n- BẬT 送信プレビュー",
       "1. Gõ tin, bấm gửi → modal hiện\n2. Hover nút メッセージ送信 → quan sát\n"
       "3. Bấm メッセージ送信\n4. Quan sát modal và khung hội thoại\n5. Kiểm tra app LINE của friend",
       "1 tin text",
       "- Hover: có hiệu ứng trên nút\n- Bấm gửi: tin được gửi, modal TỰ ĐÓNG\n"
       "- Tin xuất hiện ở chat 1:1 và friend nhận trên app LINE",
       note="Nguồn: Rightbar r399-r401"),

    tc("Preview trước khi gửi", "STATE-CLEAN-001", "Abnormal",
       "Đóng modal xem trước bằng X — tin chưa gửi",
       BOT + "\n- BẬT 送信プレビュー",
       "1. Gõ tin, bấm gửi → modal hiện\n2. Bấm X đóng modal\n"
       "3. Quan sát khung hội thoại và ô nhập\n4. Kiểm tra app LINE của friend",
       "1 tin text, đóng bằng X",
       "- Modal đóng, tin CHƯA được gửi\n- Friend không nhận tin",
       note="Nguồn: Rightbar r398"),

    tc("Preview trước khi gửi", "FUNC-001", "Normal",
       "Ô tích 今後、送信プレビューを表示しない — tắt xem trước cho lần sau",
       BOT + "\n- BẬT 送信プレビュー",
       "1. Gõ tin, bấm gửi → modal hiện\n2. Quan sát trạng thái mặc định của ô tích\n"
       "3. Tích vào ô, bấm gửi\n4. Gõ tin khác, bấm gửi → quan sát có modal không\n"
       "5. Kiểm tra DB trường cấu hình xem trước của bot\n"
       "6. Vào màn cài đặt chat bật lại 送信プレビュー → gửi tin → quan sát",
       "Ô tích tắt xem trước",
       "- Mặc định ô tích KHÔNG được chọn\n"
       "- Sau khi tích và gửi: lần gửi sau KHÔNG hiện modal xem trước\n"
       "- DB: trường cấu hình xem trước của bot chuyển về 0\n"
       "- Bật lại ở màn cài đặt chat: modal xem trước hiện lại",
       note="Nguồn: Rightbar r402-r405"),

    tc("Preview trước khi gửi", "UI-002", "Normal",
       "Icon dấu hỏi trong modal xem trước — chú thích đường dẫn tới cài đặt",
       BOT + "\n- BẬT 送信プレビュー",
       "1. Gõ tin, bấm gửi → modal hiện\n2. Rê chuột vào icon dấu hỏi\n3. Đọc nội dung hiện ra",
       "Modal xem trước đang mở",
       "- Hiện chú thích「送信プレビューは 1:1チャット設定 > 送信プレビューより 表示変更が可能です。」",
       note="Nguồn: Rightbar r406"),

    tc("Preview trước khi gửi", "UI-INPUT-001", "Abnormal",
       "Bấm gửi khi chưa nhập gì — không hiện modal xem trước",
       BOT + "\n- BẬT 送信プレビュー",
       "1. Không nhập nội dung, không chọn file\n2. Bấm nút gửi\n3. Quan sát màn hình",
       "Ô nhập trống",
       "- KHÔNG hiện modal xem trước\n- Không gửi tin nào, không lỗi",
       note="Nguồn: Rightbar r409"),

    # ═══════════════ Rightbar — 基本情報 ═══════════════
    tc("Rightbar — 基本情報", "UI-FIELD-001", "Normal",
       "Tab 基本情報 — hiển thị avatar, tên, thông tin kết bạn và nút cập nhật",
       BOT,
       "1. Rê chuột vào icon tab đầu tiên ở cột phải → đọc tên tab\n"
       "2. Quan sát avatar (friend có ảnh và friend không ảnh)\n"
       "3. Quan sát tên (ngắn và dài)\n4. Đọc dòng thông tin kết bạn\n"
       "5. Rê chuột vào nút cập nhật → đọc chú thích → bấm nút",
       "Friend có/không avatar; tên ngắn/dài",
       "- Rê chuột icon tab: hiện tên tab「基本情報」\n"
       "- Có ảnh: hiện avatar friend; không ảnh: hiện ảnh mặc định\n"
       "- Tên ngắn: hiện 1 hàng; tên dài: xuống dòng\n"
       "- Thông tin kết bạn định dạng 2024.10.15 13:56 新規友だち\n"
       "- Rê chuột nút cập nhật: hiện「情報を更新する」; bấm nút: lấy lại thông tin mới nhất từ LINE",
       note="Nguồn: Rightbar r6-r14"),

    tc("Rightbar — 基本情報", "SYNC-APP-001", "Normal",
       "Nút đồng bộ thông tin từ LINE — lấy lại tên, ảnh và trạng thái mới nhất",
       BOT + "\n- Friend A đã đổi tên LINE, ảnh đại diện và dòng trạng thái trên app LINE",
       "1. Ghi lại tên LINE, ảnh và dòng trạng thái đang hiển thị ở tab 基本情報\n"
       "2. Bấm nút cập nhật thông tin\n"
       "3. So sánh tên, ảnh, dòng trạng thái sau khi cập nhật\n"
       "4. Kiểm tra dòng của friend A ở danh sách bạn bè\n"
       "5. Kiểm tra DB: tên, đường dẫn ảnh và dòng trạng thái của bạn bè",
       "Friend A đổi tên LINE, ảnh đại diện và dòng trạng thái",
       "- Sau khi bấm cập nhật: tên LINE, ảnh và dòng trạng thái đổi sang giá trị MỚI\n"
       "- Danh sách bạn bè cũng cập nhật theo (nếu friend không có システム表示名)\n"
       "- DB lưu đúng giá trị mới",
       note="Khớp spec BR-16 (feature-spec.md:478 — gọi API LINE cập nhật tên, ảnh và trạng thái). "
            "Nguồn: Rightbar r13, r14 + Test fix bug Kh r43"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Sửa システム表示名 ở tab 基本情報 — đồng bộ với danh sách bạn bè",
       BOT,
       "1. Bấm icon sửa cạnh trường システム表示名\n2. Nhập tên mới, nhấn Enter để lưu\n"
       "3. Quan sát tên hiển thị ở tab 基本情報 và ở dòng friend A trong danh sách\n"
       "4. Bấm nút cập nhật → kiểm tra tên vẫn đúng",
       "システム表示名 mới = `テスト表示名2026`",
       "- Tên mới hiển thị ở tab 基本情報\n"
       "- Dòng friend A trong danh sách bạn bè cũng đổi sang tên mới (đồng bộ)\n"
       "- Sau khi bấm cập nhật thông tin: tên hệ thống vẫn giữ giá trị vừa nhập",
       note="Nguồn: Rightbar r15-r17"),

    tc("Rightbar — 基本情報", "UI-FIELD-001", "Normal",
       "流入経路 — hiện tên QR nếu kết bạn qua QR, ngược lại hiện 通常友だち追加",
       BOT + "\n- Friend B kết bạn qua QR landing tên「Youtube広告」\n- Friend C kết bạn qua link thường",
       "1. Mở tab 基本情報 của friend B → đọc trường 流入経路\n2. Lặp lại với friend C\n"
       "3. Rê chuột vào icon sửa → đọc chú thích",
       "B qua QR landing · C qua link thường",
       "- Friend B: hiện tên QR landing「Youtube広告」\n"
       "- Friend C: hiện「通常友だち追加」\n- Rê chuột icon sửa: hiện chú thích「編集する」",
       note="Nguồn: Rightbar r18-r21"),

    tc("Rightbar — 基本情報", "UI-FIELD-001", "Normal",
       "Trường ステップ配信 — hiện tên scenario đang chạy và thời điểm gửi tiếp theo",
       BOT + "\n- Friend A chưa chạy scenario nào\n- Friend B đang chạy scenario tên dài (2 dòng)",
       "1. Mở tab 基本情報 của friend A → đọc trường ステップ配信\n"
       "2. Mở của friend B → đọc tên scenario và dòng thời điểm gửi tiếp theo\n"
       "3. Kiểm tra tên scenario dài có xuống dòng không",
       "A không scenario · B đang chạy scenario tên dài",
       "- A: hiện「配信中のステップなし」\n"
       "- B: hiện tên scenario đang chạy + dòng thời điểm gửi tiếp theo định dạng 次回配信 2024/10/13 14:00\n"
       "- Tên dài: xuống dòng, không vỡ layout",
       note="Nguồn: Rightbar r22-r25"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Bắt đầu scenario từ tab 基本情報 — chọn thư mục và scenario rồi thực thi",
       BOT + "\n- Có thư mục scenario mặc định và thư mục tự tạo; có thư mục CHƯA có scenario nào",
       "1. Bấm icon sửa cạnh ステップ配信 → tích「ステップを開始・変更する」→ bấm tiếp\n"
       "2. Quan sát thư mục mặc định và thư mục chưa có scenario\n"
       "3. Kiểm tra cuộn khi nhiều thư mục / nhiều scenario\n"
       "4. Khi chưa chọn scenario nào: quan sát nút bắt đầu\n"
       "5. Chọn 1 scenario → bấm nút bắt đầu → kiểm tra trường ステップ配信",
       "Thư mục mặc định 未分類, thư mục tự tạo, thư mục rỗng",
       "- Thư mục mặc định hiển thị là「未分類」; thư mục chưa có scenario hiện「分類を選択して下さい」\n"
       "- Nhiều thư mục / scenario: có cuộn\n"
       "- Chưa chọn scenario: nút bắt đầu bị vô hiệu\n"
       "- Sau khi chọn và bắt đầu: trường ステップ配信 hiện tên scenario đang chạy",
       note="Nguồn: Rightbar r26-r32"),

    tc("Rightbar — 基本情報", "UI-INPUT-001", "Boundary",
       "Chọn scenario — chỉ chọn được 1, đổi lựa chọn thì áp dụng cái cuối",
       BOT,
       "1. Mở modal chọn scenario, thử tích 2 scenario cùng lúc\n"
       "2. Chọn scenario A rồi bỏ chọn, chọn scenario B → bấm bắt đầu\n"
       "3. Đổi qua lại nhiều lần rồi bấm bắt đầu\n4. Double click nút bắt đầu",
       "Scenario A và B",
       "- Chỉ chọn được 1 scenario tại một thời điểm\n"
       "- Áp dụng scenario được chọn CUỐI CÙNG\n- Double click: chỉ tính 1 lần",
       note="Nguồn: Rightbar r33-r36"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Bắt đầu scenario từ đầu và từ giữa",
       BOT + "\n- Scenario S nhiều bước; scenario S1 chỉ có 1 bước",
       "1. Mở modal chọn scenario → quan sát tuỳ chọn bắt đầu mặc định\n"
       "2. Chọn S, giữ mặc định → bắt đầu → kiểm tra tin ở chat 1:1\n"
       "3. Chọn S, tích tuỳ chọn bắt đầu từ giữa → quan sát ô nhập số → nhập số ngày → bắt đầu\n"
       "4. Chọn S1 (chỉ 1 bước) + bắt đầu từ giữa → quan sát",
       "Scenario S nhiều bước · S1 chỉ 1 bước",
       "- Mặc định là bắt đầu TỪ ĐẦU\n"
       "- Tích bắt đầu từ giữa: hiện ô nhập số cho phép nhập và tăng giảm\n"
       "- Bắt đầu từ đầu: chat 1:1 hiện tin bắt đầu scenario từ đầu\n"
       "- Bắt đầu từ giữa: chat 1:1 hiện tin bắt đầu từ ngày thứ N\n"
       "- S1 chỉ 1 bước + bắt đầu từ giữa: ghi nhận hiện trạng (chưa có thiết kế hiển thị)",
       spec="Spec không ghi",
       note="Corpus ghi 「chưa có design để hiển thị text step chỉ có 1 bước」. Nguồn: Rightbar r37-r45"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Dừng scenario từ tab 基本情報 — có xác nhận trước khi dừng",
       BOT + "\n- Friend A đang chạy scenario S",
       "1. Bấm icon sửa cạnh ステップ配信 → tích tuỳ chọn dừng\n"
       "2. Hover nút 次にすすむ → quan sát\n3. Bấm nút → đọc thông báo xác nhận\n"
       "4. Bấm Cancel → kiểm tra scenario còn chạy không\n"
       "5. Lặp lại, bấm OK → kiểm tra trường ステップ配信 và tin ở chat 1:1\n"
       "6. Khi đang mở thông báo xác nhận: click ra ngoài màn → quan sát",
       "Friend A đang chạy scenario S",
       "- Hover nút: đổi màu xanh\n- Bấm nút: hiện thông báo xác nhận\n"
       "- Cancel: scenario vẫn chạy\n"
       "- OK: scenario dừng, trường ステップ配信 về「配信中のステップなし」, chat 1:1 có tin dừng scenario\n"
       "- Click ra ngoài khi đang mở xác nhận: thông báo KHÔNG bị đóng",
       note="Nguồn: Rightbar r46-r50"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Gán rich menu cho bạn bè từ tab 基本情報",
       BOT + "\n- Có rich menu R1 tên ngắn, R2 tên dài (30 ký tự), R3 đang tắt, R4 hết thời gian hiển thị",
       "1. Với friend chưa gán rich menu: đọc trường リッチメニュー\n"
       "2. Bấm icon sửa → chọn R1 → bấm nút hiển thị → kiểm tra trường リッチメニュー\n"
       "3. Kiểm tra danh sách chọn: có R3 (đang tắt) không\n"
       "4. Chọn R4 (hết thời gian hiển thị) → quan sát thông báo\n"
       "5. Kiểm tra hiển thị tên R2 (tên dài) và ảnh rich menu",
       "R1 tên ngắn · R2 tên dài 30 ký tự · R3 đang tắt · R4 hết thời gian hiển thị",
       "- Chưa gán: trường リッチメニュー hiện「表示なし」\n"
       "- Gán R1: trường hiện tên R1 + ảnh rich menu\n"
       "- R3 (đang tắt): KHÔNG xuất hiện trong danh sách chọn\n"
       "- Chọn R4: hiện「選択したリッチメニューは表示期間外の設定となっています。表示期間設定をご確認下さい。」\n"
       "- Tên dài 30 ký tự: hiển thị đủ, không vỡ layout",
       note="Nguồn: Rightbar r51-r70"),

    tc("Rightbar — 基本情報", "FUNC-001", "Normal",
       "Dừng hiển thị rich menu — có xác nhận",
       BOT + "\n- Friend A đang được gán rich menu R1",
       "1. Bấm icon sửa cạnh リッチメニュー → tích tuỳ chọn dừng hiển thị\n"
       "2. Hover nút 次にすすむ → bấm nút → đọc thông báo xác nhận\n"
       "3. Bấm Cancel → kiểm tra; bấm lại và chọn OK → kiểm tra\n"
       "4. Kiểm tra rich menu trên app LINE của friend",
       "Friend A đang gán rich menu R1",
       "- Thông báo xác nhận hiện「現在表示されているリッチメニューの表示を停止します」\n"
       "- Cancel: rich menu vẫn còn\n"
       "- OK: trường リッチメニュー về「表示なし」, rich menu biến mất trên app LINE của friend",
       env="PRODUCTION",
       note="Đi tới output cuối app LINE (RULE-06). Nguồn: Rightbar r71-r73"),

    tc("Rightbar — 基本情報", "DATA-001", "Normal",
       "Thao tác ở tab 基本情報 chỉ ảnh hưởng đúng bot đang chọn",
       BOT + "\n- Cùng 1 tài khoản LINE là bạn bè của cả bot A và bot B",
       "1. Ở bot A: gán scenario S và rich menu R cho friend, sửa システム表示名\n"
       "2. Chuyển sang bot B, mở hội thoại cùng tài khoản LINE đó\n"
       "3. Kiểm tra trường ステップ配信, リッチメニュー và システム表示名 ở bot B",
       "Cùng 1 tài khoản LINE ở 2 bot",
       "- Bot B: các trường KHÔNG bị thay đổi theo thao tác ở bot A\n"
       "- Dữ liệu tách biệt hoàn toàn theo bot",
       note="Nguồn: Rightbar r46, r68"),

    # ═══════════════ Rightbar — 友だち情報 ═══════════════
    tc("Rightbar — 友だち情報", "UI-FIELD-001", "Normal",
       "Tab 友だち情報 — hiển thị đủ các mục thông tin đã cấu hình",
       BOT + "\n- Đã cấu hình các mục thông tin: ngày sinh, tỉnh, điểm, ảnh giấy tờ, file tải lên\n"
       "- Friend A đã có giá trị cho các mục này",
       "1. Mở tab 友だち情報 ở cột phải\n2. Đọc từng mục thông tin và giá trị\n"
       "3. Với mục ảnh: bấm icon kính lúp để xem trước\n"
       "4. Với mục file: đọc tên file, bấm mở file trên Chrome và trên Safari\n"
       "5. Khi có nhiều mục: kiểm tra cuộn",
       "Ngày sinh · tỉnh · điểm · ảnh giấy tờ · file tải lên",
       "- Hiển thị đủ các mục cùng giá trị của friend A\n"
       "- Bấm kính lúp: xem trước đúng ảnh friend đã tải lên\n"
       "- Bấm mở file: mở ở TAB MỚI, đúng trên cả Chrome và Safari\n- Nhiều mục: có cuộn",
       note="Nguồn: Rightbar r78-r86"),

    tc("Rightbar — 友だち情報", "UI-FIELD-001", "Normal",
       "Mục thông tin mặc định — email và ngày sinh",
       BOT + "\n- Tab 友だち情報 đang hiển thị 2 mục mặc định: メールアドレス và 生年月日",
       "1. Mở tab 友だち情報 của friend chưa có email và ngày sinh → đọc giá trị hiển thị\n"
       "2. Nhập email hợp lệ và chọn ngày sinh → lưu\n"
       "3. Kiểm tra giá trị hiển thị và DB\n"
       "4. Nhập email SAI định dạng → lưu → ghi nhận kết quả\n"
       "5. Xoá giá trị → lưu → kiểm tra",
       "Email hợp lệ `test@example.com` · email sai định dạng `test@@example` · ngày sinh 1990-01-15",
       "- Chưa có giá trị: hiển thị trạng thái trống, không lỗi\n"
       "- Email hợp lệ và ngày sinh: lưu được, hiển thị đúng, DB lưu đúng giá trị\n"
       "- Email sai định dạng: ghi nhận hệ thống có chặn hay không (spec không ghi validate) và "
       "đối chiếu quyết định của Leader\n"
       "- Xoá giá trị: trở về trạng thái trống",
       spec="Spec không ghi",
       note="Field Traceability §4.4 (feature-spec.md:427-429) liệt kê email và ngày sinh nhưng cột Validation "
            "để TRỐNG; corpus cũng không có TC cho email. TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Rightbar — 友だち情報", "FUNC-001", "Normal",
       "Cấu hình mục thông tin hiển thị — thêm mục từ danh sách ẩn",
       BOT + "\n- Có thư mục mặc định và thư mục tự tạo; có mục chưa thuộc thư mục nào",
       "1. Mở modal cấu hình mục hiển thị → quan sát khối 非表示項目\n"
       "2. Kiểm tra thư mục mặc định và mục chưa có thư mục\n3. Kiểm tra cuộn khi nhiều thư mục\n"
       "4. Bấm dấu cộng để thêm 1 mục → bấm 内容を保存 → kiểm tra ngoài màn\n"
       "5. Thêm nhiều mục cùng lúc → lưu → kiểm tra",
       "Thư mục mặc định 未分類, thư mục tự tạo, mục chưa có thư mục",
       "- Mặc định: mục chưa thêm nằm ở khối ẩn, ngoài màn chưa hiển thị\n"
       "- Thư mục mặc định hiển thị là「未分類」; mục chưa có thư mục nằm trong 未分類\n"
       "- Sau khi thêm và lưu: mục hiển thị ở tab 友だち情報 ngoài màn\n"
       "- Thêm nhiều mục cùng lúc: tất cả đều hiển thị\n"
       "- Modal tự đóng sau khi bấm 内容を保存",
       note="Nguồn: Rightbar r87-r95, r105"),

    tc("Rightbar — 友だち情報", "STATE-CLEAN-001", "Abnormal",
       "Thêm mục nhưng đóng modal bằng X — không lưu",
       BOT,
       "1. Mở modal cấu hình mục hiển thị, thêm 1 mục\n2. KHÔNG bấm 内容を保存, bấm X\n"
       "3. Kiểm tra tab 友だち情報 ngoài màn\n4. Mở lại modal kiểm tra trạng thái",
       "Thêm 1 mục rồi đóng X",
       "- Mục KHÔNG hiển thị ngoài màn\n- Mở lại modal: trạng thái reset về như trước",
       note="Nguồn: Rightbar r93"),

    tc("Rightbar — 友だち情報", "FUNC-001", "Normal",
       "Sắp xếp và xoá mục thông tin đang hiển thị",
       BOT + "\n- Tab 友だち情報 đang hiển thị ≥4 mục",
       "1. Ghi lại thứ tự hiện tại các mục\n2. Kéo thả 1 mục sang vị trí khác → lưu → kiểm tra thứ tự ngoài màn\n"
       "3. Thử kéo nhiều mục cùng lúc\n"
       "4. Bấm icon xoá 1 mục nhưng KHÔNG lưu, bấm X → kiểm tra\n"
       "5. Bấm icon xoá rồi bấm 内容を保存 → kiểm tra\n6. Double click nút xoá",
       "4 mục thông tin",
       "- Thứ tự mặc định theo thứ tự đã thêm\n"
       "- Kéo thả và lưu: thứ tự ngoài màn đổi đúng\n- Mỗi lần chỉ kéo được 1 mục\n"
       "- Xoá nhưng không lưu (đóng X): mục vẫn còn\n- Xoá và lưu: mục biến mất khỏi tab 友だち情報\n"
       "- Double click nút xoá: chỉ tính 1 lần",
       note="Gộp vì cùng thuộc cấu hình mục hiển thị. Nguồn: Rightbar r97-r104"),

    tc("Rightbar — 友だち情報", "UI-INPUT-001", "Normal",
       "Nhập / sửa giá trị thông tin — kiểu lựa chọn, kiểu chữ và kiểu ngày",
       BOT + "\n- Tab 友だち情報 có mục kiểu lựa chọn, kiểu chữ và kiểu ngày",
       "1. Mục kiểu lựa chọn: mở danh sách → kiểm tra đủ lựa chọn đã cấu hình → chọn 1 giá trị → lưu\n"
       "2. Mục kiểu chữ: nhập giá trị mới → lưu → sửa lại → lưu\n"
       "3. Mục kiểu ngày: chọn ngày hiện tại, ngày quá khứ, ngày tương lai → lưu sau mỗi lần\n"
       "4. Sau mỗi lần lưu: kiểm tra giá trị hiển thị ở tab 友だち情報",
       "Kiểu lựa chọn · kiểu chữ · kiểu ngày (hiện tại / quá khứ / tương lai)",
       "- Kiểu lựa chọn: hiện đủ lựa chọn đã cấu hình, chọn và lưu được\n"
       "- Kiểu chữ: nhập và sửa được, giá trị hiển thị đúng\n"
       "- Kiểu ngày: chọn được cả 3 mốc thời gian, hiển thị đúng ngày đã chọn",
       note="Nguồn: Rightbar r106-r110"),

    tc("Rightbar — 友だち情報", "MEDIA-001", "Normal",
       "Mục thông tin kiểu ảnh và kiểu PDF — tải lên, thay, xoá và mở file",
       BOT + "\n- Tab 友だち情報 có mục kiểu ảnh và mục kiểu PDF, friend A chưa có giá trị",
       "1. Khi chưa tải lên: đọc giá trị hiển thị\n"
       "2. Bấm nút 編集 → tải lên 1 file → kiểm tra giá trị hiển thị\n"
       "3. Thử tải lên file sai định dạng → ghi nhận kết quả\n"
       "4. Với mục PDF: bấm mở file → quan sát tab\n"
       "5. Bấm nút 削除 → đọc thông báo xác nhận → bấm Hủy → kiểm tra; bấm lại và chọn OK → kiểm tra",
       "Ảnh PNG và JPG hợp lệ; file PDF; thử thêm file sai định dạng",
       "- Chưa tải lên: hiện「登録なし」\n"
       "- Tải lên PNG/JPG thành công; file sai định dạng bị chặn\n"
       "- Bấm mở file PDF: mở ở TAB MỚI\n"
       "- Bấm xoá: hiện「登録されているデータを削除してよろしいですか？」; Hủy thì giữ file, OK thì xoá thành công",
       spec="Đã hỏi leader",
       note="MT-11: chỗ này nhận PNG và JPG, nhưng ảnh profile người gửi chỉ nhận PNG. "
            "Nguồn: Rightbar r111-r117"),

    tc("Rightbar — 友だち情報", "UI-INPUT-001", "Boundary",
       "Mục thông tin kiểu ĐIỂM — nhận giá trị âm và dương",
       BOT + "\n- Tab 友だち情報 có mục kiểu điểm",
       "1. Nhập giá trị điểm DƯƠNG → lưu → kiểm tra hiển thị và DB\n"
       "2. Nhập giá trị điểm ÂM → lưu → kiểm tra hiển thị và DB\n"
       "3. Kiểm tra ảnh/dữ liệu liên quan có lưu được khi điểm âm không",
       "Điểm dương = 100 · điểm âm = -50",
       "- Cả giá trị dương và âm đều lưu được và hiển thị đúng\n"
       "- DB lưu đúng giá trị bao gồm dấu âm",
       note="Nguồn: Rightbar r118-r120"),

    # ═══════════════ Rightbar — タグ管理 ═══════════════
    tc("Rightbar — タグ管理", "UI-001", "Normal",
       "Tab タグ管理 — hiển thị tag của bạn bè theo thư mục",
       BOT + "\n- Có tag chưa thuộc thư mục nào và tag thuộc thư mục tự tạo\n- Friend A đang gắn cả 2 loại",
       "1. Mở tab タグ管理 ở cột phải → đọc tiêu đề\n"
       "2. Quan sát tag chưa có thư mục và tag có thư mục\n"
       "3. Đối chiếu thứ tự thư mục với màn Quản lý thẻ",
       "Tag chưa có thư mục · tag thuộc thư mục tự tạo",
       "- Tiêu đề hiện「タグ管理」\n"
       "- Tag chưa có thư mục nằm trong thư mục「未分類」\n"
       "- Thứ tự thư mục khớp thứ tự ở màn Quản lý thẻ",
       note="Nguồn: Rightbar r123-r126, r131, r132, r150"),

    tc("Rightbar — タグ管理", "FUNC-001", "Normal",
       "Gỡ tag của bạn bè bằng icon X — có xác nhận",
       BOT + "\n- Friend A đang gắn tag T1",
       "1. Bấm icon X trên tag T1\n2. Đọc thông báo xác nhận\n3. Bấm Cancel → kiểm tra tag còn không\n"
       "4. Bấm lại icon X → OK → kiểm tra tab タグ管理 và DB\n"
       "5. Khi thông báo xác nhận đang mở: click ra ngoài màn → quan sát",
       "Tag T1 đang gắn cho friend A",
       "- Thông báo xác nhận hiện「タグ「〇〇」を外しますがよろしいですか？」\n"
       "- Cancel: tag vẫn còn; OK: tag bị gỡ, biến mất khỏi tab và khỏi DB liên kết tag-bạn bè\n"
       "- Click ra ngoài khi đang mở xác nhận: thông báo KHÔNG bị đóng",
       note="Nguồn: Rightbar r127-r129"),

    tc("Rightbar — タグ管理", "FUNC-001", "Normal",
       "Gắn tag từ tab タグ管理 — mở thư mục, chọn nhiều tag rồi lưu",
       BOT + "\n- Có ≥3 thư mục tag, mỗi thư mục nhiều tag",
       "1. Bấm vào khu vực tag → quan sát trạng thái thư mục mặc định (đóng)\n"
       "2. Bấm ひらく để mở 1 thư mục → quan sát\n3. Kiểm tra cuộn khi nhiều thư mục / nhiều tag\n"
       "4. Chọn 1 tag → bấm 保存 → kiểm tra ngoài màn danh sách tag\n"
       "5. Chọn nhiều tag → 保存 → kiểm tra\n6. Bấm ひらく lần nữa để đóng thư mục → quan sát",
       "3 thư mục tag, chọn 1 tag rồi nhiều tag",
       "- Mặc định thư mục ở trạng thái đóng; bấm ひらく thì mở ra\n"
       "- Chọn được NHIỀU tag cùng lúc\n"
       "- Sau khi lưu: ngoài màn hiển thị các tag đang được chọn\n"
       "- Thư mục đóng: chỉ hiện tên thư mục và nút ひらく",
       note="Nguồn: Rightbar r133-r143"),

    tc("Rightbar — タグ管理", "STATE-CLEAN-001", "Abnormal",
       "Chọn tag rồi đóng thư mục mà không lưu — không gắn tag",
       BOT,
       "1. Mở thư mục tag, chọn 1 tag\n2. KHÔNG bấm 保存, bấm とじる để đóng thư mục\n"
       "3. Kiểm tra danh sách tag của friend ngoài màn",
       "Chọn tag rồi đóng thư mục",
       "- Tag KHÔNG được gắn cho friend\n- Thư mục reset về trạng thái ban đầu",
       note="Nguồn: Rightbar r136"),

    tc("Rightbar — タグ管理", "FUNC-001", "Normal",
       "Modal タグ編集 — chọn tất cả, bỏ chọn tất cả và lưu",
       BOT + "\n- Có ≥3 thư mục tag với nhiều tag",
       "1. Mở modal タグ編集 → quan sát thư mục mặc định\n2. Kiểm tra cuộn khi nhiều thư mục / tag\n"
       "3. Tích ô「以下を全選択」→ quan sát các tag bên dưới\n"
       "4. Bỏ tích ô đó → quan sát\n5. Chọn 1 tag → bấm 内容を保存 → kiểm tra\n"
       "6. Chọn nhiều tag → lưu → kiểm tra\n7. Double click nút 内容を保存",
       "3 thư mục tag",
       "- Thư mục mặc định「未分類」ở trạng thái mở\n"
       "- Tích「以下を全選択」: tự tích toàn bộ tag bên dưới; bỏ tích: tự bỏ toàn bộ\n"
       "- Chọn 1 hoặc nhiều tag rồi lưu: tag được gắn cho friend, hiển thị ngoài màn\n"
       "- Double click nút lưu: chỉ tính 1 lần",
       note="Nguồn: Rightbar r145-r155"),

    tc("Rightbar — タグ管理", "DATA-REF-001", "Normal",
       "Thêm tag mới ở màn Quản lý thẻ — hiển thị ngay trong tab タグ管理",
       BOT,
       "1. Ghi lại danh sách tag hiển thị trong tab タグ管理\n"
       "2. Sang màn Quản lý thẻ: thêm tag mới T_new, sắp xếp lại thứ tự thư mục\n"
       "3. Quay lại chat 1:1, mở lại tab タグ管理\n4. Mở modal タグ編集 kiểm tra",
       "Tag mới T_new; đổi thứ tự thư mục",
       "- Tab タグ管理 và modal タグ編集 đều hiển thị T_new\n- Thứ tự thư mục khớp thứ tự mới",
       note="Nguồn: Rightbar r130, r131, r149, r150"),

    tc("Rightbar — タグ管理", "DATA-001", "Normal",
       "Thao tác tag ở tab タグ管理 chỉ ảnh hưởng đúng bot đang chọn",
       BOT + "\n- Cùng 1 tài khoản LINE là bạn bè của cả bot A và bot B",
       "1. Ở bot A: gắn tag T1 và gỡ tag T2 cho friend\n"
       "2. Chuyển sang bot B, mở hội thoại cùng tài khoản LINE đó\n3. Kiểm tra tab タグ管理 ở bot B",
       "Cùng 1 tài khoản LINE ở 2 bot",
       "- Bot B: danh sách tag KHÔNG bị thay đổi theo thao tác ở bot A",
       note="Nguồn: Rightbar r129, r144"),

    # ═══════════════ Rightbar — フォーム回答 ═══════════════
    tc("Rightbar — フォーム回答", "UI-FIELD-001", "Normal",
       "Tab フォーム回答 — danh sách câu trả lời của bạn bè, mới nhất lên đầu",
       BOT + "\n- Friend A đã trả lời ≥3 form ở các thời điểm khác nhau",
       "1. Mở tab フォーム回答 → đọc tiêu đề\n2. Đọc bộ lọc năm mặc định\n"
       "3. Đọc ngày giờ trả lời và tên form của từng bản ghi\n4. Kiểm tra thứ tự sắp xếp",
       "3 bản ghi trả lời form của friend A",
       "- Tiêu đề hiện「フォーム回答」\n- Bộ lọc năm mặc định = năm hiện tại\n"
       "- Mỗi bản ghi hiện ngày giờ trả lời định dạng 2024.10.04 14:50 + tên form\n"
       "- Bản ghi MỚI NHẤT hiển thị lên đầu",
       note="Nguồn: Rightbar r158-r163"),

    tc("Rightbar — フォーム回答", "LIST-001", "Abnormal",
       "Bạn bè chưa trả lời form nào — không hiển thị bản ghi",
       BOT + "\n- Friend B chưa trả lời form nào",
       "1. Mở hội thoại friend B → mở tab フォーム回答\n2. Quan sát vùng danh sách",
       "Friend B: 0 bản ghi trả lời form",
       "- Không hiển thị bản ghi nào, không lỗi JS",
       note="Nguồn: Rightbar r164"),

    tc("Rightbar — フォーム回答", "DATA-001", "Normal",
       "Tab フォーム回答 chỉ hiển thị dữ liệu đúng bạn bè và đúng bot",
       BOT + "\n- Friend A và friend B đều đã trả lời form (nội dung khác nhau)\n"
       "- Cùng tài khoản LINE của A cũng là bạn bè của bot B và đã trả lời form ở bot B",
       "1. Mở tab フォーム回答 của A → ghi lại danh sách\n2. Mở của B → ghi lại\n"
       "3. Chuyển sang bot B, mở hội thoại cùng tài khoản LINE của A → kiểm tra",
       "A và B có dữ liệu khác nhau; cùng tài khoản ở 2 bot",
       "- Mỗi friend chỉ hiển thị đúng câu trả lời của chính mình\n"
       "- Bot B chỉ hiển thị bản ghi của bot B, không lẫn bản ghi bot A",
       note="Nguồn: Rightbar r165, r171, r187"),

    tc("Rightbar — フォーム回答", "LIST-001", "Normal",
       "Bộ lọc thứ tự và bộ lọc năm ở tab フォーム回答",
       BOT + "\n- Friend A có bản ghi trả lời form ở năm nay và năm ngoái",
       "1. Đọc thứ tự mặc định\n2. Chọn 昇順 → kiểm tra thứ tự\n3. Chọn 降順 → kiểm tra\n"
       "4. Thử chọn 2 bộ lọc cùng lúc\n5. Bấm nút < để lùi năm → kiểm tra danh sách\n"
       "6. Bấm nút > để tiến năm → kiểm tra",
       "Bản ghi ở năm nay và năm ngoái; bộ lọc tăng dần và giảm dần",
       "- Mặc định: bản ghi mới nhất lên đầu, bộ lọc năm = năm hiện tại\n"
       "- Chọn 昇順: sắp xếp tăng dần; chọn 降順: giảm dần\n"
       "- Chỉ chọn được 1 bộ lọc thứ tự tại một thời điểm; đổi thì áp dụng cái cuối\n"
       "- Nút < và >: chuyển đúng sang năm trước / năm sau, danh sách lọc đúng theo năm",
       note="Gộp vì cùng thuộc bộ lọc. Nguồn: Rightbar r166-r174"),

    tc("Rightbar — フォーム回答", "UI-001", "Normal",
       "Modal chi tiết câu trả lời form — câu hỏi, câu trả lời, ảnh và file tải lên",
       BOT + "\n- Friend A đã trả lời 1 form có câu hỏi chữ, câu hỏi tải ảnh và câu hỏi tải PDF",
       "1. Bấm vào 1 bản ghi trả lời form → mở modal chi tiết\n"
       "2. Đọc tên form và ngày giờ trả lời\n3. Rê chuột vào số giờ cần trả lời → đọc chú thích\n"
       "4. Đọc từng câu hỏi và câu trả lời\n5. Với ảnh: bấm icon kính lúp xem trước\n"
       "6. Với PDF: bấm mở file\n7. Đóng modal bằng nút 閉じる và bằng nút X; double click nút 閉じる",
       "Form có câu hỏi chữ, câu hỏi ảnh và câu hỏi PDF",
       "- Modal hiện đúng tên form và ngày giờ trả lời\n"
       "- Rê chuột vào số giờ: hiện「回答所要時間」\n"
       "- Hiển thị đúng từng câu hỏi và câu trả lời của friend\n"
       "- Ảnh: xem trước đúng ảnh friend đã tải lên\n- PDF: mở ở TAB MỚI\n"
       "- Nút 閉じる và X đều đóng modal; double click chỉ tính 1 lần",
       note="Gộp vì cùng thuộc modal chi tiết. Nguồn: Rightbar r175-r186"),

    # ═══════════════ Rightbar — メモ ═══════════════
    tc("Rightbar — メモ", "UI-FIELD-001", "Normal",
       "Tab メモ — danh sách ghi chú với tên quản lý, nội dung rút gọn và ngày cập nhật",
       BOT + "\n- Friend A đã có ≥2 ghi chú, trong đó 1 ghi chú nội dung dài hơn 3 dòng",
       "1. Rê chuột vào icon tab メモ → đọc tên tab\n2. Đọc tên quản lý và nội dung của từng ghi chú\n"
       "3. Với ghi chú dài: đếm số dòng hiển thị\n4. Đọc ngày giờ cập nhật cuối",
       "2 ghi chú, 1 cái nội dung dài",
       "- Rê chuột icon tab: hiện「メモ」\n"
       "- Mỗi ghi chú hiện tên quản lý + nội dung (tối đa 3 dòng) + ngày giờ cập nhật định dạng 2024.10.04 14:50",
       note="Nguồn: Rightbar r192-r195"),

    tc("Rightbar — メモ", "LIST-001", "Abnormal",
       "Bạn bè chưa có ghi chú nào — hiển thị trạng thái trống",
       BOT + "\n- Friend B chưa có ghi chú nào",
       "1. Mở hội thoại friend B → mở tab メモ\n2. Quan sát vùng danh sách ghi chú\n"
       "3. Bấm nút sắp xếp khi chưa có ghi chú nào",
       "Friend B: 0 ghi chú",
       "- Không hiển thị bản ghi nào, không lỗi JS\n"
       "- Nút tạo mới vẫn dùng được; nút sắp xếp không gây lỗi khi danh sách rỗng",
       note="Empty state — corpus KHÔNG có TC, đây là TC lấp GAP do AI viết, CẦN LEADER XÁC NHẬN"),

    tc("Rightbar — メモ", "UI-INPUT-001", "Abnormal",
       "Tạo ghi chú — tên quản lý và nội dung đều bắt buộc",
       BOT,
       "1. Rê chuột nút tạo mới → đọc chú thích → bấm nút\n2. Quan sát giá trị mặc định của 2 trường\n"
       "3. Bỏ trống tên quản lý → bấm 内容を保存 → đọc thông báo\n"
       "4. Bỏ trống nội dung → bấm lưu → đọc thông báo",
       "Bỏ trống lần lượt từng trường",
       "- Rê chuột nút tạo: hiện「新規作成」; 2 trường mặc định để trống\n"
       "- Bỏ trống tên quản lý: hiện「タイトルを入力してください。」, không lưu\n"
       "- Bỏ trống nội dung: hiện「メモ本文を入力してください。」, không lưu",
       note="Nguồn: Rightbar r196-r198, r203, r204, r211"),

    tc("Rightbar — メモ", "UI-INPUT-001", "Boundary",
       "Ghi chú — giới hạn độ dài tên quản lý 20 ký tự và nội dung 1.000 ký tự",
       BOT,
       "1. Nhập tên quản lý lần lượt: 1 ký tự · 20 ký tự · 21 ký tự (thử cả tiếng Nhật, số và chữ)\n"
       "2. Nhập nội dung lần lượt: 1 ký tự · 1.000 ký tự · 1.001 ký tự\n"
       "3. Ghi nhận ký tự thứ mấy thì không gõ được nữa / báo lỗi khi lưu\n"
       "4. Kiểm tra giá trị thực lưu trong DB bảng ghi chú",
       "Tên quản lý: 1 / 20 / 21 ký tự · nội dung: 1 / 1.000 / 1.001 ký tự",
       "- Tên quản lý ≤ 20 ký tự: lưu được; 21 ký tự: KHÔNG nhập được hoặc báo lỗi\n"
       "- Nội dung ≤ 1.000 ký tự: lưu được; vượt 1.000: bị chặn\n"
       "- Giá trị lưu trong DB khớp đúng giá trị hiển thị, KHÔNG bị cắt âm thầm",
       spec="Đã hỏi leader",
       note="MT-16: spec BR-13 (feature-spec.md:475) chỉ nói giới hạn 10 lịch sử, KHÔNG có giới hạn độ dài field. "
            "Nguồn: Rightbar r199-r207"),

    tc("Rightbar — メモ", "STATE-CLEAN-001", "Abnormal",
       "Nhập ghi chú rồi đóng bằng X — không lưu",
       BOT,
       "1. Bấm tạo ghi chú mới, nhập đầy đủ tên quản lý và nội dung\n2. Bấm X đóng\n"
       "3. Kiểm tra danh sách ghi chú của friend A",
       "Nhập đủ 2 trường rồi đóng X",
       "- Ghi chú KHÔNG được tạo, danh sách không đổi",
       note="Nguồn: Rightbar r202, r208, r212"),

    tc("Rightbar — メモ", "FUNC-001", "Normal",
       "Tạo ghi chú thành công và không tạo trùng khi double click",
       BOT,
       "1. Nhập đầy đủ tên quản lý và nội dung → bấm 内容を保存\n"
       "2. Kiểm tra ghi chú xuất hiện trong danh sách\n"
       "3. Tạo ghi chú khác, double click nút 内容を保存 → đếm số bản ghi\n"
       "4. Kiểm tra DB bảng ghi chú",
       "2 ghi chú, lần 2 double click nút lưu",
       "- Ghi chú được tạo, hiển thị trong danh sách với đúng tên và nội dung\n"
       "- Double click: chỉ tạo 1 bản ghi, DB không có bản trùng",
       note="Nguồn: Rightbar r209, r210, r213"),

    tc("Rightbar — メモ", "FUNC-001", "Normal",
       "Sửa ghi chú — sửa riêng từng trường, phản ánh ra danh sách",
       BOT + "\n- Friend A có ghi chú M1 đã có tên và nội dung",
       "1. Bấm icon sửa M1 → kiểm tra tên và nội dung hiển thị đúng\n"
       "2. Quan sát trạng thái 2 trường khi CHƯA bấm icon sửa của từng trường\n"
       "3. Bấm sửa trường tiêu đề: xoá tên cũ để trống → quan sát; nhập tên mới → lưu → kiểm tra danh sách\n"
       "4. Bấm sửa trường nội dung: nhập nội dung mới → lưu → kiểm tra danh sách\n"
       "5. Nhập rồi bấm X → kiểm tra dữ liệu giữ nguyên",
       "Ghi chú M1; sửa tiêu đề rồi sửa nội dung",
       "- Modal sửa hiện đúng tên và nội dung hiện tại\n"
       "- Khi chưa bấm icon sửa của từng trường: 2 trường ở trạng thái không sửa được\n"
       "- Sau khi sửa và lưu: danh sách hiển thị dữ liệu MỚI\n"
       "- Bấm X: đóng modal, dữ liệu giữ nguyên như cũ",
       note="Gộp vì cùng chuỗi sửa ghi chú. Nguồn: Rightbar r214-r228"),

    tc("Rightbar — メモ", "DATA-AUDIT-001", "Boundary",
       "Lịch sử chỉnh sửa ghi chú — chỉ giữ 10 lần gần nhất",
       BOT + "\n- Friend A có ghi chú M1 vừa tạo mới",
       "1. Sửa M1 liên tiếp 12 lần (mỗi lần đổi nội dung khác nhau)\n"
       "2. Bấm vào ngày cập nhật gần nhất của M1 → mở lịch sử\n"
       "3. Đếm số bản ghi lịch sử\n4. Đọc ngày giờ thao tác, loại thao tác và tên người thao tác của từng bản\n"
       "5. Kiểm tra DB bảng lịch sử ghi chú",
       "1 lần tạo + 12 lần sửa = 13 thao tác",
       "- Lịch sử chỉ hiển thị 10 lần gần nhất, các bản cũ hơn bị xoá\n"
       "- Mỗi bản hiện: ngày giờ thao tác, loại thao tác (新規作成 khi tạo mới, 編集 khi sửa), tên người thao tác\n"
       "- DB: bảng lịch sử ghi chú của M1 có tối đa 10 bản ghi",
       note="Khớp spec BR-13 (feature-spec.md:475). Nguồn: Rightbar r230-r234"),

    tc("Rightbar — メモ", "DATA-001", "Normal",
       "Ghi chú và lịch sử chỉ thuộc đúng bot đang chọn",
       BOT + "\n- Cùng 1 tài khoản LINE là bạn bè của cả bot A và bot B",
       "1. Ở bot A: tạo và sửa ghi chú cho friend\n"
       "2. Chuyển sang bot B, mở hội thoại cùng tài khoản LINE đó\n"
       "3. Kiểm tra tab メモ và lịch sử chỉnh sửa ở bot B",
       "Cùng 1 tài khoản LINE ở 2 bot",
       "- Bot B: KHÔNG hiển thị ghi chú và lịch sử của bot A",
       note="Nguồn: Rightbar r213, r229, r235"),

    tc("Rightbar — メモ", "FUNC-001", "Normal",
       "Sắp xếp ghi chú — kéo thả và menu 3 chấm chuyển lên đầu / xuống cuối",
       BOT + "\n- Friend A có ≥4 ghi chú",
       "1. Rê chuột nút sắp xếp → đọc chú thích → bấm nút\n"
       "2. Quan sát thứ tự mặc định\n3. Kéo thả 1 ghi chú sang vị trí khác\n"
       "4. Thử kéo nhiều ghi chú cùng lúc\n"
       "5. Dùng menu 3 chấm: chuyển 1 ghi chú lên đầu → lưu → kiểm tra\n"
       "6. Kiểm tra nút chuyển lên đầu ở ghi chú đang đứng đầu và nút chuyển xuống cuối ở ghi chú cuối\n"
       "7. Chuyển vị trí rồi bấm X không lưu → kiểm tra\n8. Double click nút 変更を保存",
       "4 ghi chú",
       "- Rê chuột nút sắp xếp: hiện「並べ替え」, con trỏ thành hình bàn tay\n"
       "- Thứ tự mặc định: ghi chú mới tạo nhất ở đầu\n"
       "- Kéo thả và menu 3 chấm đều đổi đúng vị trí; mỗi lần chỉ kéo được 1 ghi chú\n"
       "- Ghi chú đang ở đầu: nút chuyển lên đầu bị vô hiệu; ở cuối: nút chuyển xuống cuối bị vô hiệu\n"
       "- Đóng bằng X mà không lưu: thứ tự giữ nguyên\n- Double click nút lưu: chỉ tính 1 lần",
       note="Gộp vì cùng thuộc chức năng sắp xếp. Nguồn: Rightbar r236-r250"),
]
