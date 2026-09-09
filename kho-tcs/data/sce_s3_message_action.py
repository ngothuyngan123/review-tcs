# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 13-19: Tên quản lý step · Message · Template · Action · Profile
· Copy message&action · 一括操作.

Nguồn: tab「Testcase」(master) · tab「Improve update msg scenario」(01/2025, TCsLine_Improve chung)
· tab「text fix bug Kh」(Bug #29551 profile sender, 04/2025).
"""
from _common import tc

STEP = ("- Đăng nhập admin (主管理者), bot A\n- Scenario S1 có step「02時間00分後」đang mở màn đăng ký message "
        "(メッセージ登録)")
SCE_F = ("- Đăng nhập admin (主管理者), bot A\n- Scenario S1 có filter default và 2 filter branch F-A, F-B; "
         "mỗi filter có ≥ 2 step")

S3 = [
    # ══════════════════ 13. Tên quản lý step ══════════════════
    tc("Tên quản lý step", "UI-FIELD-001", "Normal",
       "メッセージ管理名: có placeholder, KHÔNG bắt buộc, nhập 1–10 ký tự lưu thành công",
       STEP,
       "1. Quan sát placeholder của ô「メッセージ管理名」\n2. Để trống → lưu step → quan sát\n"
       "3. Nhập「初回案内」(4 ký tự) → lưu\n4. Query `step_message`.`name`",
       "Để trống ·「初回案内」(4 ký tự)",
       "- Ô có placeholder đúng design\n- Để trống: lưu THÀNH CÔNG (không bắt buộc)\n"
       "- Nhập 4 ký tự: lưu thành công, `step_message`.`name` = '初回案内'",
       note="Nguồn: r466, r467, r472"),

    tc("Tên quản lý step", "DATA-INPUT-001", "Boundary",
       "メッセージ管理名: nhập 11 ký tự → cảnh báo; bộ đếm số ký tự hiển thị đúng",
       STEP,
       "1. Nhập 11 ký tự vào「メッセージ管理名」\n2. Quan sát bộ đếm số ký tự\n3. Bấm lưu\n4. Query `step_message`.`name`",
       "11 ký tự JP「あいうえおかきくけこさ」",
       "- Bộ đếm hiển thị đúng số ký tự đã nhập\n- Hiển thị cảnh báo vượt 10 ký tự, KHÔNG lưu",
       spec="Spec không ghi",
       note="Giới hạn 10 ký tự cho step name — spec (feature-spec §9 Validation Rules) KHÔNG ghi. Nguồn: r468, r470"),

    tc("Tên quản lý step", "DATA-TEXT-001", "Abnormal",
       "メッセージ管理名 nhập TOÀN KHOẢNG TRẮNG → coi như để trống; nhập có space đầu/cuối → trim trước khi lưu",
       STEP,
       "1. Nhập「     」(toàn dấu cách) → lưu → query `step_message`.`name`\n"
       "2. Nhập「  初回案内  」(có space đầu/cuối) → lưu → query `step_message`.`name`",
       "Lần 1:「     」\nLần 2:「  初回案内  」",
       "- Lần 1: `name` lưu rỗng (hoặc NULL), KHÔNG lưu chuỗi toàn space\n"
       "- Lần 2: `name` = '初回案内' (đã trim space đầu/cuối)",
       spec="Đã hỏi leader",
       note="MT-11 — corpus r471 đánh **NG** (trim), r352 ghi『nhập khoảng trắng vẫn đang success』. "
            "TC dự kiến FAIL → cần raise bug. Nguồn: r469, r471, r352"),

    # ══════════════════ 14. Message trong step ══════════════════
    tc("Message trong step", "MSG-001", "Normal",
       "Step chưa có message và chưa có action → hiển thị text hướng dẫn bắt buộc đăng ký 1 trong 2",
       STEP + ", chưa thêm message hay action nào",
       "1. Mở step「02時間00分後」\n2. Quan sát vùng message",
       "Step rỗng",
       "- Hiển thị text:「メッセージ・エルメアクションが登録されていません（どちらかの登録は必須です）」",
       note="Nguồn: r473"),

    tc("Message trong step", "MEDIA-001", "Normal",
       "Thêm message メッセージ追加 đủ 4 loại (text/pdf · button 4 dạng · stamp · location) → lưu và hiển thị đúng",
       STEP,
       "1. Double click nhanh button「メッセージ追加」→ đếm số lần mở màn tạo\n"
       "2. Tạo message dạng text (có file PDF đính kèm) → lưu\n3. Tạo message dạng button, lần lượt 4 dạng button → lưu\n"
       "4. Tạo message dạng stamp → lưu\n5. Tạo message dạng location → lưu\n"
       "6. Quay lại màn step, đếm và kiểm tra hiển thị từng message",
       "text + pdf · button (4 dạng) · stamp · location",
       "- Double click chỉ mở màn tạo 1 lần\n- Cả 4 loại message lưu THÀNH CÔNG\n"
       "- Danh sách message của step hiển thị đủ, đúng loại, đúng nội dung",
       env="PRODUCTION",
       note="RULE-08: media (PDF) → chạy PRODUCTION. 4 loại cùng 1 kết quả (lưu OK) → giữ chung. Nguồn: r474-r478"),

    tc("Message trong step", "FUNC-SORT-001", "Normal",
       "Thứ tự message trong step: message mới nhất xuống CUỐI danh sách",
       STEP + "\n- Step đã có 2 message M1, M2",
       "1. Thêm message M3\n2. Quan sát vị trí M3 trong danh sách message của step",
       "M1, M2 có sẵn; thêm M3",
       "- Thứ tự hiển thị: M1, M2, M3 — M3 ở CUỐI",
       note="Nguồn: r489"),

    tc("Message trong step", "FUNC-SORT-001", "Boundary",
       "Step có message QUICK REPLY → quick reply luôn ở CUỐI; message mới thêm nằm ở vị trí thứ 2 từ dưới lên",
       STEP + "\n- Step đã có: M1 (text), M2 (button quick reply)",
       "1. Thêm message M3 (text)\n2. Quan sát thứ tự danh sách message",
       "M1 (text), M2 (quick reply); thêm M3 (text)",
       "- Thứ tự: M1, M3, M2(quick reply)\n- Quick reply luôn nằm CUỐI\n- M3 ở vị trí thứ 2 từ dưới lên",
       note="Nguồn: r490"),

    tc("Message trong step", "UI-002", "Normal",
       "Icon phân biệt nguồn message: thêm từ メッセージ追加 → icon tin nhắn; thêm từ テンプレートから追加 → icon filte",
       STEP + "\n- Step có 1 message thêm bằng メッセージ追加 và 1 message thêm bằng テンプレートから追加",
       "1. Quan sát icon của từng message trong danh sách\n2. Đối chiếu với design",
       "2 message từ 2 nguồn khác nhau",
       "- Message từ「メッセージ追加」: icon hình tin nhắn\n- Message từ「テンプレートから追加」: icon filte\n- Khớp design",
       note="Nguồn: r491, r492"),

    tc("Message trong step", "UI-002", "Normal",
       "Text mô tả tương ứng với từng loại message hiển thị đúng; click ảnh/audio/video để phóng to",
       STEP + "\n- Step có message các loại: text, image, audio, video, stamp, location",
       "1. Quan sát text mô tả hiển thị cho từng loại message\n2. Click vào hình của message image / audio / video\n"
       "3. Quan sát cửa sổ phóng to",
       "6 loại message",
       "- Mỗi loại hiển thị text mô tả đúng loại tương ứng\n- Click hình mở ra chế độ phóng to, hiển thị đúng media",
       env="PRODUCTION",
       note="RULE-08: media → chạy PRODUCTION. Nguồn: r493, r494"),

    tc("Message trong step", "UI-002", "Normal",
       "Hover icon (...) của message → hiện menu 3 mục: 一番上の移動 / 一番下の移動 / xoá",
       STEP + "\n- Step có 3 message",
       "1. Hover vào icon (...) của message ở giữa\n2. Quan sát menu bật ra",
       "3 message trong step",
       "- Menu hiện đủ 3 mục:「一番上の移動」·「一番下の移動」· xoá",
       note="Nguồn: r495"),

    tc("Message trong step", "FUNC-SORT-001", "Boundary",
       "Message ở vị trí ĐẦU → disable 一番上の移動; message ở CUỐI → disable 一番下の移動",
       STEP + "\n- Step có 4 message M1..M4",
       "1. Hover icon (...) của M1 → quan sát trạng thái 2 nút\n2. Hover icon (...) của M4 → quan sát trạng thái 2 nút",
       "4 message M1..M4",
       "- M1: disable「一番上の移動」, enable「一番下の移動」\n- M4: disable「一番下の移動」, enable「一番上の移動」",
       note="Nguồn: r496, r498"),

    tc("Message trong step", "FUNC-SORT-001", "Normal",
       "Message ở vị trí thứ 2 trở đi: click 一番上の移動 → lên đầu; message thứ 2 từ dưới: click 一番下の移動 → xuống cuối; vị trí các message khác cập nhật đúng",
       STEP + "\n- Step có 4 message M1..M4",
       "1. Chọn M3 → click「一番上の移動」→ quan sát thứ tự cả 4 message\n"
       "2. Chọn message ở vị trí thứ 2 từ dưới → click「一番下の移動」→ quan sát thứ tự\n"
       "3. Reload màn step → kiểm tra thứ tự có giữ nguyên không\n4. Query `step_message`.`template_ids`",
       "4 message M1..M4",
       "- M3 lên vị trí #1, các message khác dịch xuống đúng thứ tự\n"
       "- Message được chọn xuống cuối, các message khác dịch lên đúng\n"
       "- Sau reload thứ tự giữ nguyên; `step_message`.`template_ids` lưu đúng thứ tự mới",
       spec="Đã hỏi leader",
       note="MT-27 — corpus r356 đánh **NG** cho『sort message』ở màn edit scenario. Cần xác nhận sort message còn lỗi không. Nguồn: r497, r499, r356"),

    tc("Message trong step", "FUNC-004", "Normal",
       "Xoá 1 message trong step → hiện popup xác nhận; OK = xoá, Cancel = giữ nguyên",
       STEP + "\n- Step có 3 message M1, M2, M3",
       "1. Hover icon (...) của M2 → click xoá → quan sát popup\n2. Click Cancel → kiểm tra danh sách message\n"
       "3. Lặp lại, click OK → kiểm tra danh sách message + `step_message`.`template_ids`",
       "Xoá M2 trong 3 message",
       "- Hiện popup xác nhận\n- Cancel: vẫn đủ 3 message\n"
       "- OK: còn M1, M3; `template_ids` không còn id của M2",
       note="Nguồn: r500"),

    tc("Message trong step", "FUNC-002", "Normal",
       "Edit message: double click text 編集 → chỉ mở 1 lần màn detail, data đầy đủ; edit đủ 4 dạng đều lưu OK",
       STEP + "\n- Step có 4 message: text, button, stamp, location",
       "1. Double click nhanh text「編集」của message text → đếm số lần mở màn detail\n"
       "2. Kiểm tra data hiển thị ở màn detail\n3. Sửa nội dung → lưu → quay lại kiểm tra\n"
       "4. Lặp bước 3 với message button, stamp, location",
       "4 dạng message",
       "- Chỉ mở màn detail 1 lần\n- Data hiển thị đầy đủ, khớp nội dung đã lưu\n"
       "- Cả 4 dạng sửa và lưu THÀNH CÔNG, nội dung mới hiển thị đúng ở màn step",
       note="Nguồn: r501-r506"),

    # ══════════════════ 15. Template từ thư viện ══════════════════
    tc("Template từ thư viện", "UI-001", "Normal",
       "Double click テンプレートから追加 → chỉ mở 1 popup テンプレート利用選択, hiển thị đúng 2 lựa chọn",
       STEP,
       "1. Double click nhanh button「テンプレートから追加」\n2. Đếm số popup mở ra\n"
       "3. Chọn 1 template → quan sát popup「テンプレート利用選択」",
       "—",
       "- Chỉ mở 1 popup\n- Popup「テンプレート利用選択」hiển thị 2 lựa chọn:"
       "「テンプレートをそのまま利用する」và「テンプレートを引用して編集する」",
       note="Nguồn: r479, r480"),

    tc("Template từ thư viện", "DATA-REF-001", "Normal",
       "テンプレートをそのまま利用する (LINK): sửa từ MÀN TEMPLATE → nội dung bên scenario CŨNG thay đổi",
       STEP + "\n- Thư viện có template T1「案内文」\n- Step đã thêm T1 bằng「テンプレートをそのまま利用する」",
       "1. Vào màn Template, sửa nội dung T1 (thêm/sửa/xoá text)\n2. Quay lại màn step của S1\n"
       "3. Mở message T1 → đối chiếu nội dung\n4. Query `step_message`.`template_ids` → xác nhận vẫn là id gốc của T1",
       "Template T1, sửa nội dung ở màn Template",
       "- Nội dung message trong scenario THAY ĐỔI theo template\n- `template_ids` vẫn giữ id gốc của T1 (không clone)",
       note="TC lấp Gap #8 của spec (feature-spec §12 mục 8:『option_add_template 1=link, 2=copy — không tìm thấy cột DB』). Nguồn: r482"),

    tc("Template từ thư viện", "DATA-REF-001", "Normal",
       "テンプレートをそのまま利用する (LINK): sửa TỪ SCENARIO → template gốc ở thư viện CŨNG thay đổi",
       STEP + "\n- Step đã thêm template T1 bằng「テンプレートをそのまま利用する」",
       "1. Ở màn step, mở message T1 → sửa nội dung → lưu\n2. Vào màn Template, mở T1 → đối chiếu nội dung",
       "Sửa nội dung message T1 từ phía scenario",
       "- Template T1 ở thư viện THAY ĐỔI theo nội dung vừa sửa (2 chiều liên kết)",
       note="Nguồn: r483"),

    tc("Template từ thư viện", "OUT-001", "Normal",
       "テンプレートをそのまま利用する: LINE friend nhận được nội dung MỚI NHẤT của template",
       STEP + "\n- Step「ステップ開始直後」có template T1 dạng LINK; friend test chưa start scenario",
       "1. Sửa nội dung T1 ở màn Template thành「新しい案内」\n2. Start scenario S1 cho friend test\n"
       "3. Mở LINE app của friend, đọc message nhận được\n4. Đối chiếu với nội dung mới nhất của T1",
       "T1 sửa thành「新しい案内」",
       "- LINE app hiển thị message có nội dung「新しい案内」(nội dung mới nhất, không phải nội dung cũ)",
       env="PRODUCTION",
       note="RULE-06 đi tới output cuối (LINE app). Nguồn: r484"),

    tc("Template từ thư viện", "DATA-COPY-001", "Normal",
       "テンプレートを引用して編集する (COPY): sửa từ màn Template → scenario KHÔNG đổi; sửa từ scenario → template KHÔNG đổi",
       STEP + "\n- Thư viện có template T2「案内文2」\n- Step đã thêm T2 bằng「テンプレートを引用して編集する」",
       "1. Query `step_message`.`template_ids` → xác nhận id KHÁC id gốc T2\n"
       "2. Sửa T2 ở màn Template → quay lại scenario kiểm tra nội dung message\n"
       "3. Sửa message trong scenario → vào màn Template kiểm tra T2",
       "Template T2 thêm bằng chế độ COPY",
       "- `template_ids` chứa id MỚI (bản clone), khác id gốc của T2\n"
       "- Sửa T2 ở thư viện: scenario KHÔNG thay đổi\n- Sửa trong scenario: T2 ở thư viện KHÔNG thay đổi",
       note="TC lấp Gap #8 của spec. Nguồn: r485-r487"),

    tc("Template từ thư viện", "OUT-001", "Normal",
       "テンプレートを引用して編集する: LINE friend nhận nội dung MỚI NHẤT của bản clone trong scenario",
       STEP + "\n- Step「ステップ開始直後」có template T2 dạng COPY; friend test chưa start",
       "1. Sửa nội dung message T2 (bản clone) trong scenario thành「引用版案内」\n"
       "2. Start scenario cho friend test\n3. Mở LINE app đọc message nhận được",
       "Bản clone sửa thành「引用版案内」",
       "- LINE app hiển thị「引用版案内」(nội dung bản clone mới nhất), KHÔNG phải nội dung template gốc",
       env="PRODUCTION",
       note="RULE-06. Nguồn: r488"),

    tc("Template từ thư viện", "FUNC-002", "Normal",
       "Edit message thêm từ template: click 編集 → mở màn ステップ内テンプレート編集, thông tin đầy đủ, thao tác thêm/sửa/xoá được với cả 2 chế độ",
       STEP + "\n- Step có template T1 (chế độ LINK) và T2 (chế độ COPY), cả 2 đều là template group",
       "1. Click text「編集」của T1 → quan sát màn mở ra\n2. Kiểm tra thông tin hiển thị trong màn\n"
       "3. Thêm / sửa / xoá template con trong T1 → lưu\n4. Lặp bước 1-3 với T2",
       "T1 (LINK) · T2 (COPY), đều là template group",
       "- Mở đúng màn「ステップ内テンプレート編集」\n- Thông tin hiển thị đầy đủ, đúng nội dung template\n"
       "- Cả 2 chế độ đều thêm/sửa/xoá template con thành công",
       note="Nguồn: r507-r510"),

    tc("Template từ thư viện", "DATA-DB-001", "Normal",
       "Mapping step_message ↔ template_mapping_tables: 1 step_message có bao nhiêu template_ids thì có bấy nhiêu bản ghi mapping",
       STEP + "\n- Step có 3 template trong `template_ids`",
       "1. Query `step_message`.`template_ids` của step\n"
       "2. Query `template_mapping_tables` WHERE table_name = 'step_message' AND table_id = <step_message_id>\n"
       "3. Đối chiếu số bản ghi và giá trị template_id\n4. Chạy job recover → query lại và đối chiếu",
       "3 template trong template_ids",
       "- Số bản ghi `template_mapping_tables` = 3, đúng bằng số template_ids\n"
       "- Mỗi bản ghi: template_id ∈ template_ids, table_name = 'step_message', table_id = step_message_id\n"
       "- Sau job recover: mapping vẫn khớp, không dư/thiếu",
       env="PRODUCTION",
       note="RULE-08: job recover → PRODUCTION. Nguồn:「Improve update msg scenario」r3"),

    tc("Template từ thư viện", "DATA-REF-001", "Normal",
       "Template GROUP dùng thẳng: thêm/sửa/xoá/đổi thứ tự template con → step_message update timestamp; gửi từ web và job đều đúng data mới",
       STEP + "\n- Step có template group TG (chế độ dùng thẳng) chứa 2 template con",
       "1. Ghi lại `step_message`.`update_timestamp`\n2. Thêm 1 template con vào TG → query lại timestamp + `step_message` (số bản ghi)\n"
       "3. Send test cả 1 step từ web → kiểm tra LINE app\n4. Chờ job send thẳng → kiểm tra LINE app\n"
       "5. Lặp bước 2-4 với: sửa template con · xoá template con · đổi thứ tự template con",
       "Template group TG với 2 → 3 template con; 4 loại thao tác",
       "- Sau MỖI thao tác: `step_message`.`update_timestamp` được cập nhật\n"
       "- KHÔNG thêm/xoá bản ghi step_message (bảng này chỉ lưu id cha)\n"
       "- Send từ web VÀ send từ job đều trả đúng data mới nhất trên LINE app",
       env="PRODUCTION",
       note="RULE-07 verify DB + màn hình + output LINE. Nguồn:「Improve update msg scenario」r4-r15"),

    tc("Template từ thư viện", "DATA-CASCADE-001", "Abnormal",
       "Xoá template GROUP ở màn Template → step_message xoá id đó khỏi template_ids + xoá bản ghi mapping",
       STEP + "\n- Step có template group TG (chế độ dùng thẳng)",
       "1. Ghi lại `step_message`.`template_ids` và bản ghi `template_mapping_tables` của TG\n"
       "2. Vào màn Template, xoá TG\n3. Query lại `step_message`.`template_ids`\n"
       "4. Query lại `template_mapping_tables`\n5. Send test step từ web và chờ job send → kiểm tra LINE app",
       "Xoá template group TG ở màn Template",
       "- `step_message`.`template_ids` KHÔNG còn id của TG, `update_timestamp` được cập nhật\n"
       "- `template_mapping_tables`: bản ghi của TG bị xoá\n- Send từ web và job đều KHÔNG gửi nội dung TG",
       spec="Đã hỏi leader",
       note="MT-28 — corpus「Improve update msg scenario」r16 ghi chú:『trong tbl step_message chưa xóa id template đó đi "
            "=> sau 1 time Tùng sẽ check bên step_message id có template ids nào thì sẽ insert tương ứng』→ chưa xoá ngay. "
            "TC có thể FAIL. Nguồn: r16-r18"),

    tc("Template từ thư viện", "COMPAT-LEGACY-001", "Normal",
       "Template ĐƠN (kiểu cũ): add vào step / sửa / xoá → step_message update timestamp + mapping đúng; send từ web và job đúng data",
       STEP + "\n- Thư viện có template ĐƠN kiểu cũ T-old",
       "1. Add T-old vào step → query `step_message`.`update_timestamp` + `template_mapping_tables`\n"
       "2. Send test từ web + chờ job send → kiểm tra LINE app\n"
       "3. Sửa nội dung T-old → lặp bước 1-2\n4. Xoá T-old → query `template_mapping_tables` + send test",
       "Template đơn kiểu cũ T-old",
       "- Add: update_timestamp cập nhật, có bản ghi mapping mới\n- Sửa: update_timestamp cập nhật\n"
       "- Xoá: bản ghi mapping bị xoá khỏi `template_mapping_tables`\n"
       "- Cả 3 trạng thái: send từ web và job đều trả đúng data hiện tại",
       env="PRODUCTION",
       note="Nguồn:「Improve update msg scenario」r19-r27"),

    tc("Template từ thư viện", "DATA-COPY-001", "Normal",
       "Template CLONE (引用して編集): sửa / đổi thứ tự / xoá template con → step_message update timestamp; send web + job đúng data",
       STEP + "\n- Step có template group clone TG-c chứa 3 template con",
       "1. Sửa 1 template con → query `step_message`.`update_timestamp` → send test web + chờ job → kiểm tra LINE\n"
       "2. Đổi vị trí các template con → lặp\n3. Xoá 1 template con → lặp",
       "Template group clone TG-c với 3 template con",
       "- Cả 3 thao tác: `update_timestamp` được cập nhật\n"
       "- Send từ web và job đều trả đúng data sau khi sửa/đổi thứ tự/xoá",
       env="PRODUCTION",
       note="⚠️ Corpus r28 ghi『không test được thêm template con vì temp clone không add được thêm temp con』; "
            "r38-r40 đánh **NG** cho template đơn clone (『vào edit thì không có data để edit — lỗi từ trước, a Tư bảo sửa sau』). "
            "Nguồn:「Improve update msg scenario」r28-r43"),

    # ══════════════════ 16. Action エルメ ══════════════════
    tc("Action エルメ", "UI-002", "Normal",
       "Vùng action: text gạch chân エルメアクションを追加 + mũi tên; chưa có action → hiển thị text エルメアクションが登録されていません",
       STEP + ", chưa thêm action nào",
       "1. Quan sát vùng action: text và mũi tên\n2. Click mũi tên để mở phần add action\n3. Quan sát text khi chưa có action",
       "Step chưa có action",
       "- Text「エルメアクションを追加」có gạch chân, mũi tên hướng XUỐNG\n"
       "- Click mũi tên: mở phần add action, mũi tên chuyển hướng LÊN\n"
       "- Hiển thị text「エルメアクションが登録されていません」",
       note="Nguồn: r557, r558"),

    tc("Action エルメ", "CONC-001", "Abnormal",
       "Double click button アクション登録 → chỉ mở 1 popup tạo action",
       STEP,
       "1. Mở phần add action\n2. Double click nhanh button「アクション登録」\n3. Đếm số popup",
       "—",
       "- Chỉ mở ĐÚNG 1 popup「アクション」",
       note="Nguồn: r559"),

    tc("Action エルメ", "FUNC-MULTI-001", "Normal",
       "Add action KHÔNG filter: chọn nội dung ở 8 option của modal action → lưu đúng vào t_actions_detail",
       STEP,
       "1. Mở popup action, lần lượt thêm action theo 8 option (trừ loại text và template)\n2. Lưu\n"
       "3. Query `t_actions_detail` WHERE action_id IN (<action_id của step>) AND bot_id = <bot A>\n"
       "4. Đối chiếu từng bản ghi với option đã chọn",
       "8 option action của modal (trừ text và template)",
       "- Tất cả 8 action lưu thành công\n- `t_actions_detail` có đúng 8 bản ghi, mỗi bản ghi khớp option đã chọn",
       note="Nguồn: r560, r357"),

    tc("Action エルメ", "UI-002", "Normal",
       "Action CÓ filter → hiển thị text 絞込みあり gạch chân màu xanh; click mở popup filter; edit filter → ghi nhận giá trị mới nhất",
       STEP + "\n- Step có 1 action đã gắn filter (điều kiện tag「A」)",
       "1. Quan sát text bên cạnh action có filter\n2. Click vào text đó → quan sát popup\n"
       "3. Đổi điều kiện filter sang tag「B」→ lưu\n4. Quan sát lại + query `filters_v2` WHERE parent_id = <t_actions_detail.id>",
       "Action có filter tag A → đổi thành tag B",
       "- Hiển thị text「絞込みあり」có gạch chân, màu xanh\n- Click mở popup filter hiển thị đúng điều kiện\n"
       "- Sau edit: ghi nhận điều kiện MỚI NHẤT (tag B), `filters_v2`.`data` cập nhật đúng",
       note="Nguồn: r561, r562"),

    tc("Action エルメ", "LIST-001", "Boundary",
       "Step có NHIỀU action → hiển thị 3 action đầu tiên + text 他 N 件のアクション; double click text → mở popup hiển thị đủ data",
       STEP + "\n- Step có 7 action",
       "1. Quan sát danh sách action hiển thị ngoài step\n2. Đếm số action hiển thị và đọc text ẩn\n"
       "3. Double click nhanh vào text「他 4 件のアクション」\n4. Quan sát popup",
       "7 action trong 1 step",
       "- Hiển thị 3 action đầu tiên\n- Bên trái hiển thị text「他 4 件のアクション」\n"
       "- Double click chỉ mở 1 popup「アクション」, hiển thị đủ 7 action đang có",
       note="Nguồn: r563, r564"),

    tc("Action エルメ", "FUNC-004", "Normal",
       "Xoá action khỏi step → action biến mất, step vẫn giữ message; xoá hết action lẫn message thì hiện lại text bắt buộc",
       STEP + "\n- Step có 2 action và 1 message",
       "1. Xoá 1 action → kiểm tra danh sách action + message còn nguyên\n"
       "2. Xoá nốt action thứ 2 → kiểm tra step vẫn có message\n3. Xoá luôn message → quan sát text hiển thị",
       "2 action + 1 message",
       "- Xoá action không ảnh hưởng message\n- Xoá hết action: step chỉ còn message, vẫn hợp lệ\n"
       "- Xoá cả message: hiện text「メッセージ・エルメアクションが登録されていません（どちらかの登録は必須です）」",
       note="Nguồn: r358, r473"),

    # ══════════════════ 17. Profile người gửi ══════════════════
    tc("Profile người gửi", "UI-001", "Normal",
       "Vùng 送信者名: hiển thị avatar mặc định; double click → chỉ mở 1 popup 送信者名設定 đúng design",
       STEP,
       "1. Quan sát avatar mặc định ở vùng 送信者名\n2. Double click nhanh button 送信者名\n"
       "3. Đếm số popup + đối chiếu design",
       "—",
       "- Avatar mặc định hiển thị đúng\n- Chỉ mở 1 popup「送信者名設定」, khớp design",
       note="Nguồn: r682-r684"),

    tc("Profile người gửi", "FUNC-001", "Normal",
       "Thêm người gửi 送信者追加: thêm bằng tên + ảnh PNG, hoặc chỉ tên → đều lưu; bản mới nằm ở cuối danh sách; thêm được nhiều tên cùng lúc",
       STEP,
       "1. Mở popup「送信者名設定」→ click「送信者追加」\n2. Nhập tên「送信者A」+ upload ảnh PNG → click 登録\n"
       "3. Thêm「送信者B」chỉ nhập tên (không ảnh) → click 登録\n4. Thêm cùng lúc「送信者C」và「送信者D」\n"
       "5. Quan sát danh sách người gửi",
       "送信者A (tên + PNG) · 送信者B (chỉ tên) · 送信者C, 送信者D (cùng lúc)",
       "- Cả 4 người gửi được thêm thành công\n- Người gửi mới nằm ở CUỐI danh sách\n- Ảnh PNG hiển thị đúng cho 送信者A",
       env="PRODUCTION",
       note="RULE-08: upload media → PRODUCTION. Nguồn: r685-r687"),

    tc("Profile người gửi", "DATA-INPUT-001", "Abnormal",
       "Thêm người gửi mà KHÔNG nhập gì → fail, không tạo bản ghi",
       STEP,
       "1. Click「送信者追加」\n2. Không nhập tên, không upload ảnh\n3. Click 登録\n4. Kiểm tra danh sách người gửi",
       "(để trống hoàn toàn)",
       "- Thêm THẤT BẠI, hiển thị cảnh báo\n- Danh sách người gửi không có bản ghi mới",
       note="Nguồn: r688"),

    tc("Profile người gửi", "UI-FIELD-001", "Normal",
       "Chọn người gửi: default tick bot đang đăng nhập; tối đa tích 2; tick người khác + 保存 → lưu; không 保存 → không đổi",
       STEP + "\n- Đã có 4 người gửi trong danh sách",
       "1. Mở popup「送信者名設定」→ quan sát mục được tick mặc định\n"
       "2. Thử tick 3 người gửi → quan sát\n3. Tick 送信者A → click 保存 → kiểm tra vùng 送信者名 của step\n"
       "4. Mở lại popup, tick 送信者B → KHÔNG click 保存, đóng popup → kiểm tra vùng 送信者名",
       "4 người gửi trong danh sách",
       "- Default tick bot đang đăng nhập hệ thống\n- Chỉ tick được TỐI ĐA 2\n"
       "- Bước 3: vùng 送信者名 hiển thị 送信者A, `step_message`.`profile_id` = id của A\n"
       "- Bước 4: vùng 送信者名 vẫn là 送信者A, không đổi sang B",
       note="Nguồn: r689-r691"),

    tc("Profile người gửi", "FUNC-002", "Normal",
       "Edit người gửi: đổi tên + đổi ảnh PNG → lưu OK; ảnh sai định dạng hoặc không xác nhận → fail",
       STEP + "\n- Có người gửi 送信者A với ảnh PNG",
       "1. Edit 送信者A: đổi tên thành「送信者A改」+ upload ảnh PNG mới → lưu\n2. Kiểm tra danh sách và vùng 送信者名\n"
       "3. Edit lại: upload ảnh SAI định dạng (vd .txt / .bmp) → quan sát\n4. Edit tên nhưng không xác nhận đồng ý → quan sát",
       "Ảnh đúng: .png · Ảnh sai: .txt / .bmp",
       "- Bước 1-2: đổi tên và ảnh THÀNH CÔNG, hiển thị đúng\n"
       "- Bước 3: ảnh sai định dạng → FAIL, hiển thị cảnh báo, không lưu\n- Bước 4: không xác nhận → không thay đổi",
       env="PRODUCTION",
       note="RULE-08: media → PRODUCTION. Nguồn: r692, r693"),

    tc("Profile người gửi", "DATA-CASCADE-001", "Normal",
       "Xoá 送信者名: hiện alert; xoá thành công → tự tick profile default; step đang dùng profile bị xoá → hiển thị profile default",
       STEP + "\n- Step S1-step1 và step2 đang dùng 送信者A",
       "1. Mở popup「送信者名設定」, xoá 送信者A → đọc nguyên văn alert\n2. Xác nhận xoá\n"
       "3. Quan sát profile được tick sau khi xoá\n4. Mở lần lượt step1, step2 → quan sát vùng 送信者名\n"
       "5. Query `step_message`.`profile_id` của 2 step",
       "2 step đang dùng 送信者A",
       "- Alert hiển thị:「〜を削除しますがよろしいですか？」\n- Sau xoá: tự tick profile default\n"
       "- Cả step1 và step2 hiển thị profile DEFAULT\n- DB: `step_message`.`profile_id` của 2 step được set về NULL",
       note="Spec BR-07 / logic-spec `deleteProfilesBots` xác nhận hành vi này. Nguồn: r694-r696, r858"),

    tc("Profile người gửi", "FUNC-SORT-001", "Normal",
       "Sắp xếp danh sách người gửi: sort + lưu → thứ tự đổi; sort không lưu → giữ nguyên; list dài có scroll",
       STEP + "\n- Có 12 người gửi trong danh sách",
       "1. Mở popup「送信者名設定」→ scroll danh sách 12 người gửi\n2. Sort đổi vị trí 2 người gửi → lưu → mở lại kiểm tra\n"
       "3. Sort tiếp nhưng KHÔNG lưu, đóng popup → mở lại kiểm tra thứ tự\n4. Kiểm tra list ít bản ghi (3 người) có scroll không",
       "12 người gửi (có scroll) và 3 người gửi (chưa scroll)",
       "- List 12: có scroll, hiển thị đủ\n- Sort + lưu: thứ tự thay đổi đúng và giữ sau khi mở lại\n"
       "- Sort không lưu: thứ tự về như cũ\n- List 3: không có scroll, hiển thị đủ",
       note="Nguồn: r698-r701"),

    tc("Profile người gửi", "DATA-DB-001", "Normal",
       "Thay đổi 送信者名 của step → DB lưu đúng profile_id vừa chọn",
       STEP + "\n- Có ≥ 2 người gửi ngoài default",
       "1. Ghi lại `step_message`.`profile_id` hiện tại\n2. Đổi sang 送信者B → lưu\n"
       "3. Query `step_message`.`profile_id`\n4. Đổi về profile default → query lại",
       "Đổi profile step: default → 送信者B → default",
       "- Sau bước 2-3: `profile_id` = id của 送信者B\n"
       "- Sau bước 4: `profile_id` = NULL (profile is_default = 1 không lưu vào profile_id)",
       note="Spec BR-07. Nguồn: r857, r360"),

    tc("Profile người gửi", "OUT-001", "Normal",
       "Bug #29551: send test TỪNG TEMPLATE của 1 step ở chat 1:1 → dùng sender đang chọn ở CHAT 1:1, KHÔNG dùng sender của step",
       STEP + "\n- Step「02時間00分後」đã set 送信者名 =「ステップ送信者」\n- Màn chat 1:1 có profile default và profile khác",
       "1. Ở màn chat 1:1 chọn profile DEFAULT → send test từng template của step\n2. Kiểm tra sender hiển thị trên LINE app\n"
       "3. Ở màn chat 1:1 chọn profile KHÁC → send test từng template\n4. Kiểm tra sender\n"
       "5. Lặp bước 1-4 bằng account STAFF",
       "Step sender =「ステップ送信者」; chat 1:1 profile default / profile khác; account admin + staff",
       "- Cả 3 trường hợp (default / khác / staff): sender hiển thị trên LINE app là sender ĐANG CHỌN Ở CHAT 1:1\n"
       "- KHÔNG apply sender「ステップ送信者」của step message",
       env="PRODUCTION",
       note="Bug #29551 (14-04-2025). RULE-06 đi tới LINE app. 3 case cùng 1 kết quả → giữ chung. Nguồn:「text fix bug Kh」r3-r5"),

    tc("Profile người gửi", "OUT-001", "Normal",
       "Bug #29551: send test 1 STEP MESSAGE (quick send / テスト送信) → APPLY sender của step message",
       STEP + "\n- Step「02時間00分後」set 送信者名 =「ステップ送信者」",
       "1. Ở màn step, chọn profile DEFAULT cho step → nhấn nút quick send → kiểm tra sender trên LINE app\n"
       "2. Nhấn nút テスト送信 → kiểm tra sender\n3. Đổi step sang profile KHÁC → lặp bước 1-2\n"
       "4. Lặp toàn bộ bằng account STAFF",
       "Step profile default / profile khác; quick send + テスト送信; admin + staff",
       "- Cả 6 tổ hợp: sender trên LINE app APPLY đúng theo sender của STEP MESSAGE",
       env="PRODUCTION",
       note="Bug #29551. 6 tổ hợp cùng 1 kết quả → giữ chung. Nguồn:「text fix bug Kh」r6-r10"),

    tc("Profile người gửi", "REG-SHARED-001", "Normal",
       "Bug #29551 (triển khai ngang): send all → theo sender của send all; template và remind → theo sender đang chọn ở chat 1:1",
       STEP + "\n- Màn send all có setting sender riêng; màn template và remind không có setting sender riêng",
       "1. Màn send all: chọn profile default → quick send + テスト送信 → kiểm tra sender trên LINE app\n"
       "2. Màn send all: chọn profile khác → lặp\n3. Màn template: chat 1:1 chọn profile default / khác → send test → kiểm tra sender\n"
       "4. Màn remind: lặp như bước 3\n5. Lặp toàn bộ bằng account staff",
       "3 màn (send all / template / remind) × 2 profile × admin + staff",
       "- Màn send all: sender APPLY theo sender CỦA SEND ALL (không phải chat 1:1)\n"
       "- Màn template và remind: sender APPLY theo sender ĐANG CHỌN Ở CHAT 1:1\n"
       "- Account staff cho cùng kết quả",
       env="PRODUCTION",
       note="Bug #29551 triển khai ngang. Nguồn:「text fix bug Kh」r11-r24"),

    # ══════════════════ 18. Copy message & action ══════════════════
    tc("Copy message & action", "DATA-COPY-001", "Normal",
       "Copy message & action: chỉ copy MESSAGE và ACTION, KHÔNG copy nội dung filter và số người đã send; modal ẩn chính step đang đứng",
       SCE_F + "\n- Đứng ở step X của filter default; F-A có step Y (2 message + 1 action, đã send 15 người)",
       "1. Ở step X, click icon copy message & action → quan sát danh sách step trong modal\n"
       "2. Chọn step Y → xác nhận copy\n3. Quan sát danh sách message + action của step X\n"
       "4. Kiểm tra nội dung filter của step X\n5. Query `step_message`.`send_count` của step X",
       "Step Y có 2 message + 1 action, send_count = 15",
       "- Modal ẨN chính step X (không cho copy chính nó từ danh sách)\n"
       "- Step X nhận thêm 2 message + 1 action từ Y\n"
       "- Nội dung FILTER của step X KHÔNG bị đổi; `send_count` của X KHÔNG bị copy (giữ giá trị của X)",
       note="Nguồn: r642, r809"),

    tc("Copy message & action", "FUNC-SORT-001", "Boundary",
       "Copy message & action: data mới xuống CUỐI danh sách; nếu step đích có quick reply thì message mới nằm TRÊN quick reply",
       SCE_F + "\n- Step X có: M1 (text), M2 (button quick reply). F-A có step Y với 1 message M3",
       "1. Ở step X, copy message & action từ step Y\n2. Quan sát thứ tự message của step X",
       "Step X: M1, M2(quick reply); copy thêm M3 từ Y",
       "- Thứ tự sau copy: M1, M3, M2(quick reply)\n- M3 nằm TRÊN quick reply, quick reply vẫn ở cuối",
       note="Nguồn: r642, r679"),

    tc("Copy message & action", "DATA-COPY-001", "Normal",
       "Copy message & action: copy 1 step / copy nhiều step → focus vào step đã chọn, data mới xuống cuối",
       SCE_F + "\n- Step X (filter default); F-A có 3 step Y1, Y2, Y3",
       "1. Ở step X, copy từ Y1 → quan sát focus + vị trí message mới\n"
       "2. Ở step X, copy cùng lúc Y2 và Y3 → quan sát\n3. Đếm tổng số message của step X",
       "Copy 1 step (Y1), rồi copy nhiều step (Y2 + Y3)",
       "- Cả 2 lần: hệ thống focus vào step đã chọn, data mới nằm ở CUỐI danh sách\n"
       "- Chỉ copy message và action, tổng số message của X = số cũ + số message của Y1+Y2+Y3",
       note="Nguồn: r643, r644"),

    tc("Copy message & action", "MSG-001", "Abnormal",
       "Copy message & action CHÍNH STEP đang đứng → GHI ĐÈ nội dung, hiển thị cảnh báo",
       SCE_F + "\n- Step X có 2 message",
       "1. Ở step X, mở modal copy → tìm cách chọn chính step X (nếu modal cho phép)\n2. Xác nhận copy\n"
       "3. Đọc nguyên văn cảnh báo\n4. Quan sát danh sách message của step X",
       "Copy chính step X",
       "- Hiển thị cảnh báo:「※引用元の登録内容が上書きされますのでご注意ください」\n"
       "- Nội dung step X bị GHI ĐÈ (không nhân đôi message)",
       note="⚠️ Mâu thuẫn nội bộ: r642 ghi『modal ẩn step của chính nó』nhưng r645 lại mô tả case copy chính nó có "
            "cảnh báo ghi đè, và r75 ghi『Cần Confirm — thấy đóng popup nhưng ko thấy coppy』. Cần verify lại. Nguồn: r645, r75"),

    tc("Copy message & action", "DATA-ID-001", "Normal",
       "Sau khi copy message & action: edit bản copy KHÔNG ảnh hưởng step nguồn và ngược lại; send test bản copy đúng nội dung",
       SCE_F + "\n- Step X vừa copy message & action từ step Y",
       "1. Ở step X, edit filter action + edit message vừa copy → lưu\n2. Mở step Y → đối chiếu nội dung\n"
       "3. Ở step Y, edit message → lưu\n4. Mở step X → đối chiếu nội dung\n5. Send test step X → kiểm tra LINE app",
       "Step X (bản copy) và step Y (nguồn)",
       "- Bước 2: step Y GIỮ NGUYÊN nội dung\n- Bước 4: step X GIỮ NGUYÊN nội dung của nó\n"
       "- Bước 5: LINE app nhận đúng nội dung hiện tại của step X",
       env="PRODUCTION",
       note="RULE-06. Nguồn: r646-r648, r681"),

    tc("Copy message & action", "CONC-001", "Abnormal",
       "Double click icon copy message & action → chỉ mở 1 popup メッセージ・アクションの引用元を選択",
       SCE_F,
       "1. Double click nhanh icon copy message & action\n2. Đếm số popup mở ra",
       "—",
       "- Chỉ mở ĐÚNG 1 popup「メッセージ・アクションの引用元を選択」",
       note="Nguồn: r649"),

    tc("Copy message & action", "UI-FIELD-001", "Normal",
       "Popup copy: dropdown 引用元の配信対象（絞込み先）を選択 default all filter; click 選択してください hiện đủ danh sách filter (kể cả filter mới add), có scroll",
       SCE_F + "\n- S1 có 8 filter branch, trong đó 1 filter vừa add trong phiên hiện tại",
       "1. Mở popup copy message & action\n2. Quan sát giá trị mặc định của dropdown filter\n"
       "3. Click「選択してください」→ quan sát danh sách filter\n4. Scroll danh sách\n"
       "5. Kiểm tra filter vừa add có trong danh sách không\n6. Kiểm tra filter đã xoá có xuất hiện không",
       "8 filter branch (1 filter mới add, 1 filter đã xoá trước đó)",
       "- Default: all filter (để user chọn)\n- Danh sách hiển thị đủ 8 filter, có scroll\n"
       "- Filter mới add CÓ trong danh sách; filter đã xoá KHÔNG xuất hiện",
       note="Nguồn: r651-r656"),

    tc("Copy message & action", "LIST-001", "Normal",
       "Popup copy: sau khi chọn filter → hiển thị các step thuộc filter đó, đúng và đủ",
       SCE_F + "\n- Filter F-A có 4 step; F-B có 2 step",
       "1. Mở popup copy, chọn filter F-A → đếm số step hiển thị\n2. Đổi sang F-B → đếm lại\n"
       "3. Đối chiếu với danh sách step thực tế của mỗi filter",
       "F-A: 4 step · F-B: 2 step",
       "- Chọn F-A: hiển thị đúng 4 step của F-A\n- Chọn F-B: hiển thị đúng 2 step của F-B, không lẫn step của F-A",
       note="Nguồn: r657"),

    tc("Copy message & action", "CONC-001", "Abnormal",
       "Double click button 選択した内容を引用登録する → chỉ copy 1 lần, không nhân đôi message",
       SCE_F + "\n- Step X có 1 message; F-A có step Y với 2 message",
       "1. Mở popup copy, chọn step Y\n2. Double click nhanh button「選択した内容を引用登録する」\n"
       "3. Đếm số message của step X + query `step_message`.`template_ids`",
       "Step X (1 msg) copy từ Y (2 msg)",
       "- Step X có đúng 3 message (1 + 2), KHÔNG nhân đôi thành 5",
       note="Nguồn: r650"),

    tc("Copy message & action", "DATA-COPY-001", "Normal",
       "Copy step giữa các filter: template tự tạo / clone → sinh template_ids MỚI; template dùng thẳng → giữ id gốc",
       SCE_F + "\n- Filter F-A có step Y với 3 message: (a) tự tạo trong step, (b) clone từ template, (c) dùng thẳng template",
       "1. Ghi lại `step_message`.`template_ids` của step Y\n2. Ở filter default, copy step từ F-A (chọn step Y)\n"
       "3. Query `step_message`.`template_ids` của step đích\n4. Đối chiếu từng id với step Y",
       "3 message: tự tạo / clone / dùng thẳng",
       "- (a) và (b): sinh template_id MỚI khác step Y\n- (c): GIỮ NGUYÊN id template gốc\n"
       "- Nội dung 3 message hiển thị giống step Y",
       note="Nguồn: r62-r64, r71-r73, r808, r809"),

    tc("Copy message & action", "DATA-COUNT-001", "Normal",
       "Copy step giữa các filter: send_count của step đích RESET về 0; action sinh action_id mới; profile được copy",
       SCE_F + "\n- Filter F-A có step Y: send_count = 25, có 1 action, có profile 送信者A",
       "1. Ghi lại `step_message` của Y: send_count, action_id, profile_id\n"
       "2. Ở filter default, copy toàn bộ step từ F-A\n3. Query `step_message` của step đích: send_count, action_id, profile_id\n"
       "4. Quan sát UI: số người đã send của step đích",
       "Step Y: send_count = 25, 1 action, profile 送信者A",
       "- Step đích: `send_count` = 0 (reset)\n- `action_id` là id MỚI (khác Y)\n"
       "- `profile_id` được copy sang (cùng 送信者A)",
       note="Nguồn: r61, r66, r65, r808"),

    tc("Copy message & action", "STATE-CLEAN-001", "Normal",
       "Mở popup copy nhưng KHÔNG chọn step nào rồi bấm copy → đóng popup, không thực hiện gì",
       SCE_F + "\n- Step X có 2 message",
       "1. Mở popup copy message & action\n2. Không chọn step nào\n3. Click button copy\n"
       "4. Quan sát popup + đếm message của step X",
       "Không chọn step nào",
       "- Popup đóng, KHÔNG thực hiện copy\n- Step X vẫn 2 message như cũ",
       note="Nguồn: r70"),

    tc("Copy message & action", "FUNC-004", "Normal",
       "Xoá step ĐÃ ĐƯỢC COPY sang filter khác → nội dung filter đích KHÔNG bị ảnh hưởng",
       SCE_F + "\n- Filter default đã copy nội dung từ step Y của F-A",
       "1. Ghi lại danh sách message của step đích ở filter default\n2. Xoá step Y ở filter F-A\n"
       "3. Quay lại filter default, kiểm tra step đích",
       "Xoá step nguồn Y sau khi đã copy",
       "- Step đích ở filter default GIỮ NGUYÊN đầy đủ message và action\n- Không bị mất nội dung",
       note="Nguồn: r704, r772"),

    # ══════════════════ 19. 一括操作 ══════════════════
    tc("一括操作", "CONC-001", "Abnormal",
       "Double click button 一括操作 → chỉ mở 1 lần menu thao tác",
       SCE_F,
       "1. Double click nhanh button「一括操作」\n2. Đếm số menu/popup mở ra",
       "—",
       "- Chỉ mở ĐÚNG 1 lần menu 一括操作",
       note="Nguồn: r713"),

    tc("一括操作", "OUT-PREVIEW-001", "Normal",
       "一括プレビュー: hiển thị toàn bộ step của filter ĐANG CHỌN + toàn bộ step của filter DEFAULT, đúng thứ tự, có scroll",
       SCE_F + "\n- Filter default có 4 step; F-A (đang chọn) có 6 step; F-B có 3 step",
       "1. Đứng ở filter F-A, click「一括操作」→「一括プレビュー」(double click nhanh)\n"
       "2. Đếm số popup mở ra + đối chiếu design\n3. Đếm số step hiển thị và nhóm filter\n4. Scroll danh sách",
       "default: 4 step · F-A: 6 step · F-B: 3 step",
       "- Chỉ mở 1 popup「一括プレビュー」, khớp design\n"
       "- Hiển thị 10 step = 4 (default) + 6 (F-A); KHÔNG hiển thị 3 step của F-B\n"
       "- Step đầy đủ, đúng thứ tự, danh sách dài có scroll",
       note="Nguồn: r714-r716"),

    tc("一括操作", "OUT-PREVIEW-001", "Normal",
       "一括プレビュー → preview từng step: tab メッセージ hiển thị đúng template/message, tab アクション hiển thị đúng action",
       SCE_F + "\n- Filter default có step với: template text dài (JP max length), media (image/video/audio), stamp, "
       "location, button quick reply nhiều button, và 3 action (1 không filter, 2 có filter)",
       "1. Mở「一括プレビュー」→ double click icon preview của 1 step\n"
       "2. Tab1「メッセージ」: kiểm tra hiển thị text (max length + xuống dòng), media, stamp, location, quick reply\n"
       "3. Kiểm tra thứ tự template con (button quick ở cuối), scroll khi nhiều\n"
       "4. Tab2「アクション」: kiểm tra danh sách action, thứ tự, scroll\n"
       "5. Double click action「絞り込みなし」và action「絞り込みあり」",
       "1 step đủ 5 loại message + 3 action",
       "- Tab メッセージ: hiển thị đúng toàn bộ template/message đã setup; template con đúng thứ tự, button quick ở CUỐI; "
       "text dài có scroll; nhiều template có scroll\n"
       "- Tab アクション: hiển thị đủ 3 action, đúng thứ tự, có scroll khi nhiều\n"
       "- Action「絞り込みなし」: KHÔNG click được\n"
       "- Action「絞り込みあり」: mở popup filter, ghi rõ chỉ friend trong bộ lọc mới nhận action",
       env="PRODUCTION",
       note="RULE-08: media → PRODUCTION. Nguồn: r717-r734"),

    tc("一括操作", "OUT-PREVIEW-001", "Normal",
       "Preview: sau khi edit template/message/action/filter action → mở lại preview hiển thị nội dung MỚI",
       SCE_F + "\n- Step có 1 template group và 1 action có filter",
       "1. Mở preview step, ghi lại nội dung\n2. Đóng preview, edit nội dung template con + edit action + edit filter của action\n"
       "3. Mở lại preview → đối chiếu nội dung",
       "Sửa template con, action, filter action",
       "- Preview hiển thị nội dung MỚI NHẤT ở cả tab メッセージ và tab アクション",
       note="Nguồn: r725, r733, r734, r631, r639, r640"),

    tc("一括操作", "STATE-001", "Abnormal",
       "Edit action TỪ TRONG màn preview → thông tin vừa edit phải được ghi nhận",
       SCE_F + "\n- Step có 1 action gắn tag",
       "1. Mở preview step → tab アクション\n2. Edit action ngay trong màn preview (đổi tag) → lưu\n"
       "3. Đóng preview, mở lại step → kiểm tra action\n4. Query `t_actions_detail`",
       "Edit action từ trong preview: đổi tag A → tag B",
       "- Action được cập nhật thành tag B\n- `t_actions_detail` lưu đúng giá trị mới",
       spec="Đã hỏi leader",
       note="MT-29 — corpus r641 và r677 đều ghi chú:『đang không ghi nhận thông tin vừa edit』. "
            "TC dự kiến FAIL → cần raise bug. Nguồn: r641, r677"),

    tc("一括操作", "BULK-001", "Normal",
       "一括引用登録: copy TOÀN BỘ step của filter nguồn sang scenario; KHÔNG copy filter, KHÔNG copy số người đã send",
       SCE_F + "\n- Filter F-A có 4 step (mỗi step có message + action, send_count > 0), filter đích là default (2 step)",
       "1. Đứng ở filter default, click「一括操作」→「一括引用登録」(double click nhanh)\n"
       "2. Đếm số popup + đối chiếu design\n3. Chọn nguồn = F-A → xác nhận\n"
       "4. Đếm số step của filter default sau copy\n5. Kiểm tra nội dung filter của filter default\n"
       "6. Query `step_message`.`send_count` của các step vừa copy",
       "F-A: 4 step · filter default: 2 step",
       "- Chỉ mở 1 popup「一括引用登録」, khớp design\n"
       "- Filter default có 6 step (2 + 4)\n- Nội dung FILTER của filter default KHÔNG bị đổi\n"
       "- `send_count` của step vừa copy = 0",
       note="Nguồn: r735, r740, r741, r808"),

    tc("一括操作", "FUNC-SEQ-001", "Normal",
       "一括引用登録: step nguồn TRÙNG TIME với step đích → gộp message + action vào step đang có, ghi đè cả TÊN STEP và PROFILE",
       SCE_F + "\n- Filter default có step「02時間00分後」tên「元ステップ」, profile 送信者A, 1 message\n"
       "- Filter F-A có step「02時間00分後」tên「引用ステップ」, profile 送信者B, 2 message + 1 action",
       "1. Đứng ở filter default, dùng「一括引用登録」copy từ F-A\n"
       "2. Đếm số step của filter default (có sinh step trùng time mới không)\n"
       "3. Mở step「02時間00分後」: đếm message, kiểm tra action\n4. Kiểm tra TÊN step và PROFILE của step đó",
       "2 step trùng time 02時間00分後 ở 2 filter",
       "- KHÔNG sinh thêm step trùng time; vẫn 1 step「02時間00分後」\n"
       "- Step có 3 message (1 + 2) và 1 action\n"
       "- TÊN step bị GHI ĐÈ thành「引用ステップ」và PROFILE bị GHI ĐÈ thành 送信者B",
       spec="Đã hỏi leader",
       note="MT-24 — spec BR-03 cấm step trùng time nhưng không nêu ngoại lệ copy = gộp; đặc biệt việc GHI ĐÈ tên và "
            "profile của step đích là hành vi mất dữ liệu, spec không ghi. Nguồn: r808, r735"),

    tc("一括操作", "DATA-COPY-001", "Normal",
       "一括引用登録: template『dùng thẳng』KHÔNG được clone (giữ id gốc); template tự tạo/clone thì sinh id mới",
       SCE_F + "\n- Filter F-A có step chứa: 1 template dùng thẳng, 1 template clone, 1 message tự tạo",
       "1. Ghi lại `step_message`.`template_ids` của step nguồn\n2. Dùng「一括引用登録」copy từ F-A sang filter default\n"
       "3. Query `step_message`.`template_ids` của step đích\n4. Đối chiếu từng id",
       "3 message: dùng thẳng / clone / tự tạo",
       "- Template dùng thẳng: GIỮ NGUYÊN id gốc (không cloned)\n- Template clone và tự tạo: sinh id MỚI",
       note="Nguồn: r808, r809, r737"),

    tc("一括操作", "DATA-ID-001", "Normal",
       "一括引用登録: sau khi copy, edit ở filter đích không ảnh hưởng filter nguồn; send test đúng nội dung",
       SCE_F + "\n- Vừa dùng 一括引用登録 copy từ F-A sang filter default",
       "1. Ở filter default, edit message + action vừa copy → lưu\n2. Mở filter F-A → đối chiếu nội dung step nguồn\n"
       "3. Send test step ở filter default → kiểm tra LINE app",
       "Edit message text và action ở bản copy",
       "- Step nguồn ở F-A GIỮ NGUYÊN nội dung\n- LINE app nhận đúng nội dung đã edit của bản copy",
       env="PRODUCTION",
       note="RULE-06. Nguồn: r738, r739"),

    tc("一括操作", "BULK-001", "Normal",
       "一括消去: xoá TOÀN BỘ step trong filter đang chọn; double click chỉ mở 1 popup; phân trang cập nhật",
       SCE_F + "\n- Filter F-A có 60 step (2 trang), đang ở trang 2",
       "1. Đứng ở F-A trang 2, click「一括操作」→ double click nhanh「一括消去」\n"
       "2. Đếm số popup + đối chiếu design\n3. Xác nhận xoá\n4. Quan sát danh sách step + phân trang\n"
       "5. Query `step_message` WHERE scenario_id = <S1> AND filter_manager_id = <F-A>",
       "F-A: 60 step, đang ở trang 2",
       "- Chỉ mở 1 popup「一括消去」, khớp design\n- Sau xoá: F-A không còn step nào (danh sách trống)\n"
       "- Phân trang trở về 1 trang / không hiển thị phân trang\n- DB: không còn bản ghi step_message của F-A",
       note="Nguồn: r768-r771, r825"),

    tc("一括操作", "DATA-ID-001", "Normal",
       "一括消去 ở 1 filter → nội dung của các filter KHÁC (kể cả filter đã copy step từ filter bị xoá) KHÔNG bị ảnh hưởng",
       SCE_F + "\n- Filter default đã copy step từ F-A; F-A có 4 step; F-B có 3 step",
       "1. Ghi lại danh sách step của filter default và F-B\n2. Đứng ở F-A, dùng「一括消去」\n"
       "3. Kiểm tra filter default và F-B\n4. Query `step_message` theo từng filter_manager_id",
       "Xoá toàn bộ step của F-A",
       "- Filter default và F-B GIỮ NGUYÊN đầy đủ step, message và action\n- DB: chỉ step của F-A bị xoá",
       note="Nguồn: r772"),

    tc("一括操作", "DATA-CASCADE-001", "Abnormal",
       "一括消去 khi scenario ĐANG start cho friend (step chưa tới lượt gửi) → friend không nhận message của filter bị xoá",
       SCE_F + "\n- S1 đang có 5 friend chạy; F-A có 3 step chưa tới giờ gửi",
       "1. Ghi lại `scenario_step_time` (status = 0) của các step thuộc F-A\n2. Đứng ở F-A, dùng「一括消去」\n"
       "3. Query lại `scenario_step_time` của các step đó\n4. Chờ qua thời điểm 3 step → kiểm tra LINE app của 5 friend\n"
       "5. Kiểm tra màn my_page của 1 friend",
       "5 friend đang chạy; F-A còn 3 step pending",
       "- Bản ghi `scenario_step_time` (status = 0) của step F-A bị XOÁ\n"
       "- 5 friend KHÔNG nhận message của 3 step thuộc F-A",
       spec="Đã hỏi leader",
       note="MT-30 — MÂU THUẪN NỘI BỘ: r773 (2024) chỉ đánh OK không có kết quả mong đợi; r69 (khối data cũ) ghi "
            "『step đã start cho user → VẪN CÒN data trong scenario_step_time nhưng sẽ không send cho user』, "
            "còn spec logic-spec `deleteFilterManager`/`deleteScenarioStep` ghi XOÁ bản ghi scenario_step_time status=0. "
            "2 mô tả khác nhau về DB. Nguồn: r773, r68, r69"),

    tc("一括操作", "OUT-PREVIEW-001", "Normal",
       "一括引用登録: popup có phần chọn filter nguồn và preview step giống 一括プレビュー",
       SCE_F + "\n- S1 có 6 filter branch, 1 filter vừa add, 1 filter đã xoá trước đó",
       "1. Mở popup「一括引用登録」\n2. Quan sát dropdown「引用元の配信対象（絞込み先）を選択」(default all filter)\n"
       "3. Click「選択してください」→ kiểm tra danh sách filter (mới add có / đã xoá không có), scroll\n"
       "4. Chọn 1 filter → kiểm tra step hiển thị đầy đủ đúng thứ tự\n"
       "5. Double click icon preview của 1 step → kiểm tra tab メッセージ và tab アクション",
       "6 filter branch",
       "- Default all filter; danh sách filter đủ, có scroll; filter mới add có, filter đã xoá không có\n"
       "- Chọn filter → hiển thị đúng các step thuộc filter đó\n"
       "- Preview step: chỉ mở 1 popup, tab メッセージ và tab アクション hiển thị đúng nội dung",
       note="Nguồn: r742-r767"),
]
