# -*- coding: utf-8 -*-
"""FA-021 イベント予約 — Nhóm 30-34: remind · job nền · notify & app mobile · giới hạn gói ·
phân quyền & môi trường.

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Task nhỏ + fix bug KH」r2-r4 (đổi thời gian remind về tương lai), r24-r64 (Bug KH #34738,
    03/2026 — change booking không update remind), r93-r106 (SpecImprove #33649, 03/2026 — job recover
    count số friend booking, chuyển từ job PHP sang job Java)
  - tab「Event booking 1.0」r281-r295 (add/change/xóa remind theo thao tác)
Bổ sung:
  - TCsLine_Test Limit theo plan / tab「[AI] Test limit v2」r81-r95 (TC-LMT-058→069, 224→226 — giới hạn
    số event theo gói)
  - TCsLine_Improve chung / tab「Improve nhỏ」r320 (Bug Tester #33106 — màn booking không phân quyền vẫn
    access được), r386 (header không hiện gói giá ở màn Booking event)
"""
from _common import tc

ADM = "- Đăng nhập admin (主管理者) bot A\n- Event E có slot S1 đã bật「リマインド配信」và chọn 1 remind"
REM = ADM + "\n- Remind có ít nhất 2 step, có step gửi trước ngày sự kiện\n- Có LINE user U1 là friend"

S6 = [
    # ══════════════════ 30. Remind リマインド ══════════════════
    tc("Remind リマインド", "MSG-002", "Normal",
       "Đặt chỗ mới được duyệt ngay → thêm bản ghi remind vào user_event, trigger hiện ở chat 1:1",
       REM + "\n- Slot S1 承認方法 = 全承認",
       "1. U1 đặt 1 chỗ ở slot S1\n2. Query bảng `user_event` lọc theo U1\n"
       "3. Mở màn chat 1:1 của U1 phía admin xem trigger",
       "1 booking 全承認, slot bật remind",
       "- Có **thêm bản ghi** vào `user_event` cho U1\n"
       "- Trigger remind hiển thị được ở màn chat 1:1",
       note="Nguồn: Event booking 1.0 r281 + Task nhỏ r24 (Bug KH #34738). Spec BR-22. ⚠ RULE-01: quan điểm `MSG-002` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Remind リマインド", "MSG-002", "Normal",
       "Đặt chỗ CHỜ DUYỆT → KHÔNG thêm remind; admin duyệt mới thêm; admin từ chối thì không thêm",
       REM + "\n- Slot S1 承認方法 = リクエスト制",
       "1. U1 gửi request đặt chỗ → query `user_event`\n2. Admin duyệt request → query lại `user_event`\n"
       "3. Với booking khác: admin **từ chối** request → query `user_event`\n"
       "4. Với booking đã từ chối: admin đổi sang duyệt → query `user_event`",
       "リクエスト制, 4 bước trạng thái",
       "- Khi nhận request: **KHÔNG** thêm bản ghi `user_event`\n"
       "- Admin duyệt: **có** thêm bản ghi + trigger hiện ở chat 1:1\n"
       "- Admin từ chối: **KHÔNG** thêm\n"
       "- Từ chối rồi đổi sang duyệt: **có** thêm bản ghi",
       note="Nguồn: Task nhỏ r25-r28 + Event booking 1.0 r282-r284."),

    tc("Remind リマインド", "MSG-002", "Normal",
       "Admin đặt chỗ hộ (web và app) → thêm remind cho user",
       REM,
       "1. Admin đặt chỗ hộ cho U1 trên **web** → query `user_event` + xem chat 1:1\n"
       "2. Admin đặt chỗ hộ cho U2 trên **app mobile** → query `user_event` + xem chat 1:1\n"
       "3. Admin duyệt 1 request booking trên **app mobile** → query `user_event`\n"
       "4. Admin từ chối 1 booking trên **app mobile** → query `user_event`",
       "4 thao tác trên 2 nền tảng",
       "- Đặt hộ ở web: có thêm remind + trigger chat 1:1\n- Đặt hộ ở app: có thêm remind + trigger\n"
       "- Duyệt ở app: có thêm remind + trigger\n- Từ chối ở app: **KHÔNG** thêm remind",
       note="Nguồn: Task nhỏ r29-r32 + Event booking 1.0 r285."),

    tc("Remind リマインド", "STATE-DEP-001", "Normal",
       "User đổi lịch được duyệt ngay → TẠO remind mới và XÓA remind cũ",
       REM + "\n- U1 có **đúng 1** booking ở slot S1 (đã được add 1 remind)\n"
       "- Slot cho phép đổi 全承認, slot đích S2 cũng bật remind",
       "1. Ghi lại bản ghi `user_event` hiện có của U1\n2. U1 đổi lịch từ S1 sang S2\n"
       "3. Query `user_event` của U1\n4. Xem trigger ở màn chat 1:1",
       "1 booking → đổi slot",
       "- `user_event`: **tạo bản ghi cho remind mới** và **xóa bản ghi remind cũ**\n"
       "- Chỉ còn 1 bản ghi remind, ứng với slot S2\n- Trigger hiện đúng ở chat 1:1",
       note="Nguồn: Task nhỏ r33 (Bug KH #34738 — bug gốc: change booking nhưng không update lại remind của "
            "booking đã change) + Event booking 1.0 r286."),

    tc("Remind リマインド", "STATE-DEP-001", "Normal",
       "User gửi REQUEST đổi lịch → chưa đổi remind; duyệt thì đổi, từ chối thì giữ nguyên",
       REM + "\n- U1 có 1 booking ở slot S1; slot có 予約変更 = リクエスト制",
       "1. U1 gửi request đổi lịch sang S2 → query `user_event`\n"
       "2. Admin duyệt request change (từ màn detail của booking MỚI) → query `user_event`\n"
       "3. Chuẩn bị cặp khác, admin duyệt từ màn detail của booking GỐC → query `user_event`\n"
       "4. Chuẩn bị cặp khác, admin **từ chối** request (từ booking mới và từ booking gốc) → "
       "query `user_event` + chờ tới giờ remind của slot BAN ĐẦU",
       "リクエスト制, duyệt/từ chối từ 2 điểm thao tác",
       "- Khi gửi request: **KHÔNG** đổi remind\n"
       "- Duyệt (từ booking mới hoặc gốc): tạo remind mới + xóa remind cũ; trigger hiện ở chat 1:1\n"
       "- Từ chối (từ booking mới hoặc gốc): **KHÔNG update** `user_event` → "
       "**vẫn gửi remind theo ngày giờ của slot BAN ĐẦU**",
       note="Nguồn: Task nhỏ r34-r39 + Event booking 1.0 r287-r289."),

    tc("Remind リマインド", "STATE-DEP-001", "Normal",
       "Admin đổi lịch — CÓ đổi slot thì đổi remind; KHÔNG đổi slot thì giữ nguyên remind",
       REM + "\n- U1 có 1 booking ở slot S1 / コース P1, đã có 1 remind",
       "1. Admin đổi booking sang slot S2 → query `user_event`\n"
       "2. Với booking khác: admin đổi sang コース khác **cùng slot** → query `user_event`\n"
       "3. Với booking khác: admin đổi **chỉ số lượng** → query `user_event`\n"
       "4. Với booking khác: admin đổi **chỉ friend info** → query `user_event`",
       "4 loại thay đổi",
       "- Đổi slot: tạo remind mới + xóa remind cũ; trigger hiện ở chat 1:1\n"
       "- Đổi コース cùng slot: **KHÔNG update** remind\n"
       "- Đổi chỉ số lượng: **KHÔNG update** remind\n- Đổi chỉ friend info: **KHÔNG update** remind",
       note="Nguồn: Task nhỏ r41-r44 + Event booking 1.0 r290. Quy tắc: remind gắn với SLOT, "
            "chỉ đổi khi slot đổi."),

    tc("Remind リマインド", "STATE-DEP-001", "Normal",
       "Hủy đặt chỗ → xóa remind theo đúng trạng thái duyệt của thao tác hủy",
       REM + "\n- U1 có 1 booking đã được add remind",
       "1. User hủy, slot cho hủy 全承認 → query `user_event`\n"
       "2. Với booking khác, user hủy dạng request (chờ duyệt) → query `user_event`\n"
       "3. Admin duyệt request cancel → query `user_event`\n"
       "4. Với booking khác, admin từ chối request cancel → query `user_event`\n"
       "5. Với booking khác, admin trực tiếp hủy → query `user_event`",
       "5 nhánh hủy",
       "- User hủy 全承認: **xóa** remind\n- User hủy dạng request: **KHÔNG xóa** remind\n"
       "- Admin duyệt request cancel: **xóa** remind\n"
       "- Admin từ chối request cancel: **KHÔNG xóa** remind\n- Admin hủy trực tiếp: **xóa** remind",
       note="Nguồn: Task nhỏ r46-r50, r58-r60 + Event booking 1.0 r291-r295."),

    tc("Remind リマインド", "STATE-DEP-001", "Normal",
       "Admin đổi trạng thái booking từ キャンセル (4) sang 承認 (5) → thêm lại remind",
       REM + "\n- U1 có booking `status = 4` (đã hủy), remind đã bị xóa",
       "1. Admin đổi trạng thái booking sang đã duyệt\n2. Query `user_event`\n3. Xem trigger ở chat 1:1",
       "status 4 → 5",
       "- **Thêm lại bản ghi remind** tương ứng cho booking đó\n- Trigger hiện đúng ở chat 1:1",
       note="Nguồn: Task nhỏ r51."),

    tc("Remind リマインド", "DATA-COUNT-001", "Boundary",
       "User có NHIỀU booking cùng 1 slot → chỉ dùng CHUNG 1 remind, không xóa nhầm",
       REM + "\n- U1 có **2 booking cùng slot S1**, cả 2 đều `status ∈ {1,5}` → chỉ có 1 bản ghi remind chung",
       "1. Ghi lại bản ghi `user_event` của U1\n"
       "2. U1 đổi lịch **1 trong 2** booking sang slot S2 → query `user_event`\n"
       "3. Reset dữ liệu; admin đổi 1 booking sang slot S2 → query `user_event`\n"
       "4. Reset; U1 hủy 1 booking → query `user_event`\n5. Reset; admin hủy 1 booking → query `user_event`",
       "2 booking cùng slot, chung 1 remind",
       "- Đổi lịch (user hoặc admin): **tạo bản ghi remind mới** cho slot S2 nhưng "
       "**KHÔNG xóa bản ghi remind cũ** (vì booking còn lại vẫn cần)\n"
       "- Hủy (user hoặc admin): **KHÔNG xóa** bản ghi remind (booking còn lại vẫn cần)\n"
       "- Trigger hiện đúng ở chat 1:1",
       note="Nguồn: Task nhỏ r61-r64「check case user có nhiều booking cùng book 1 slot => nhiều booking nhưng chỉ "
            "add chung 1 remind — Nếu user có ít nhất 1 booking khác có status = 1,5 đang được add remind đó」. "
            "Đây là case dễ lọt bug nhất của cơ chế remind."),

    tc("Remind リマインド", "MSG-003", "Abnormal",
       "User BLOCK bot → không đăng ký remind; block SAU KHI đăng ký thì hành vi lúc gửi ra sao",
       REM,
       "1. U_block block bot A → đặt chỗ hộ cho U_block (hoặc U_block đặt trước rồi block)\n"
       "2. Query `user_event` xem có bản ghi cho U_block không\n"
       "3. Với U2: đặt chỗ khi CHƯA block (có remind) → sau đó U2 block bot\n"
       "4. Chờ tới giờ remind → kiểm tra bản ghi `event_step_time` và log gửi tin",
       "U_block: block trước khi đặt · U2: block sau khi đặt",
       "- U_block (block trước): **KHÔNG** đăng ký `user_event` (theo BR-22: chỉ đăng ký khi "
       "`conversation.is_blocked = 0`)\n"
       "- U2 (block sau): ghi rõ hành vi thật lúc gửi — nếu vẫn nằm trong danh sách gửi và gọi LINE API lỗi "
       "→ **RAISE BUG** (tốn quota + lỗi API)",
       env="PRODUCTION",
       note="Nguồn: spec BR-22 + TD-14 (`findAllLineUserByEventTime` KHÔNG lọc `bot_id` và KHÔNG lọc user bị "
            "block). Corpus KHÔNG có TC block → GAP, xem MT-29. RULE-08 — job BẮT BUỘC PRODUCTION."),

    tc("Remind リマインド", "MSG-002", "Normal",
       "Step remind before_day = -1 gửi NGAY khi đặt chỗ (đồng bộ, không qua job)",
       REM + "\n- Remind có 1 step cấu hình `before_day = -1` (gửi ngay) và 1 step gửi trước 1 ngày",
       "1. U1 đặt 1 chỗ ở slot S1 (全承認)\n2. Mở LINE app phía U1 **ngay lập tức**\n"
       "3. Query `event_step_time` xem step nào được đẩy vào\n4. Chờ tới mốc trước 1 ngày → kiểm tra lại",
       "Step -1 (gửi ngay) và step trước 1 ngày",
       "- Step `-1`: U1 nhận tin **ngay khi đặt chỗ** (qua Laravel, không chờ job)\n"
       "- Step trước 1 ngày: được đẩy vào `event_step_time` khi **lưu slot** (không phải khi đặt chỗ), "
       "và gửi đúng mốc",
       env="PRODUCTION",
       note="Nguồn: spec BR-22 (`:4199-4288`, `functions.php:9463-9506`). Corpus KHÔNG phân biệt step -1 → "
            "lấp GAP. RULE-06 — verify tới tin thật trên LINE."),

    tc("Remind リマインド", "FUNC-DATE-001", "Normal",
       "Đổi thời gian step remind từ QUÁ KHỨ sang TƯƠNG LAI → vẫn gửi được khi tới giờ",
       ADM + "\n- Ở màn remind (/basic/events): đã setting remind, gắn remind vào event booking, "
       "đã gửi remind cho user",
       "1. Ở màn remind, sửa thời gian của các step thành **tương lai**\n"
       "2. Trường hợp A: step ở quá khứ và **chưa** gửi → sửa thành tương lai\n"
       "3. Trường hợp B: step ở quá khứ và **đã** gửi → sửa thành tương lai\n"
       "4. Chờ tới giờ đã sửa → kiểm tra tin trên LINE + query `event_step_time`",
       "2 trường hợp: quá khứ-chưa gửi · quá khứ-đã gửi",
       "- **Cả 2 trường hợp**: đến giờ đã sửa **vẫn gửi remind** cho user\n"
       "- DB: **insert bản ghi mới** vào bảng `event_step_time`",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r2-r4「Hiện tại: Khi change remind đã send rồi thì ko send nữa. "
            "Sửa: Nếu change về tương lai thì vẫn cho send tiếp khi đến time」. Cách test nguyên văn của tester "
            "đã giữ ở cột Các bước."),

    tc("Remind リマインド", "MSG-002", "Normal",
       "Tin remind THẬT đến LINE đúng nội dung và đúng thời điểm (verify output cuối)",
       REM + "\n- Remind có 1 step gửi trước sự kiện 1 ngày lúc 09:00\n"
       "- 開催日 = ngày mai + 1; U1 đã có booking được duyệt",
       "1. Xác nhận `user_event` có bản ghi của U1 và `event_step_time` có bản ghi tới hạn\n"
       "2. Chờ tới đúng 09:00 ngày trước sự kiện\n3. Mở LINE app phía U1\n"
       "4. Đối chiếu nội dung tin với template remind đã soạn\n5. Query `event_step_time.status`",
       "Step gửi trước 1 ngày lúc 09:00",
       "- U1 **nhận được tin remind THẬT trên LINE** đúng 09:00 (sai số chấp nhận theo chu kỳ job)\n"
       "- Nội dung tin khớp template đã soạn\n- `event_step_time.status` chuyển sang đã gửi",
       env="PRODUCTION",
       note="⚠ MT-30 — TOÀN BỘ corpus chỉ verify tới bảng `user_event` / `event_step_time`, **KHÔNG có TC nào "
            "verify tin remind thật đến LINE**. Vi phạm RULE-06. TC này bổ sung để đóng GAP; liên quan spec "
            "TD-06 (flag `ENABLE_EVENT_REMIND` mặc định false → nếu deploy sai thì remind KHÔNG BAO GIỜ gửi)."),

    # ══════════════════ 31. Job nền ══════════════════
    tc("Job nền", "JOB-001", "Normal",
       "Job recover count — đếm ĐÚNG booking theo trạng thái cho slot KHÔNG có コース",
       ADM + "\n- Slot S1 KHÔNG có コース\n"
       "- Cố tình làm sai `b_slot.use_people` (VD set = 0 dù thực tế có booking)\n"
       "- Chuẩn bị booking ở đủ các trạng thái theo cột Dữ liệu test",
       "1. Chờ job recover chạy (hoặc kích hoạt thủ công)\n2. Đọc lại `b_slot.use_people`\n"
       "3. Đối chiếu với phép tính tay theo quy tắc trạng thái",
       "Booking `status ∈ {1,5,7}` (承認 / 予約済み / キャンセルリクエスト): **ĐƯỢC** tính\n"
       "Booking `status ∈ {2,3,4}` (否認 / 承認待ち / キャンセル): **KHÔNG** tính\n"
       "Booking `status = 6` (変更リクエスト): tồn tại 2 bản ghi nhưng chỉ tính **1**, tính cho slot của "
       "booking GỐC",
       "- `use_people` được recover về đúng tổng số booking hợp lệ\n"
       "- Booking status 2/3/4 không bị cộng nhầm\n"
       "- Cặp booking status 6 chỉ tính 1 lần và tính cho slot gốc",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r94-r96 (SpecImprove #33649, 03/2026 — job recover hằng ngày, đã chuyển từ job PHP "
            "sang job Java, branch t12-recover-count-booking). RULE-08 — job BẮT BUỘC PRODUCTION."),

    tc("Job nền", "JOB-001", "Normal",
       "Job recover count — cộng theo QUANTITY của từng booking, không phải theo số booking",
       ADM + "\n- Slot S1 (không コース) có 3 booking `status = 1` với `quantity` = 1, 2, 10\n"
       "- Cố tình set sai `use_people`",
       "1. Chờ job recover chạy\n2. Đọc `use_people`\n3. Đối chiếu phép tính tay",
       "quantity = 1 + 2 + 10 = **13**",
       "- `use_people` = **13** (không phải 3)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r97-r99."),

    tc("Job nền", "JOB-001", "Normal",
       "Job recover count — áp dụng đúng cả với slot CÓ コース",
       ADM + "\n- Slot S2 CÓ コース, chuẩn bị booking ở các trạng thái và quantity như 2 TC trên\n"
       "- Cố tình set sai `use_people` của slot",
       "1. Chờ job recover chạy\n2. Đọc `b_slot.use_people` của S2\n3. Đối chiếu phép tính tay\n"
       "4. Đọc `b_plan_slot.remain_limit` của các コース",
       "Booking status 1/5/7 được tính; 2/3/4 không; 6 tính 1 lần cho slot gốc; cộng theo quantity",
       "- `use_people` của slot S2 được recover đúng theo cùng quy tắc như slot không コース\n"
       "- ⚠ `remain_limit` của コース **KHÔNG được job recover** (xem TC kế tiếp)",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r100-r105."),

    tc("Job nền", "JOB-001", "Abnormal",
       "Job recover count HIỆN KHÔNG recover số booking của コース (remain_limit)",
       ADM + "\n- Slot S2 có コース P1; cố tình set sai `b_plan_slot.remain_limit` (VD = 0 dù có 3 booking)",
       "1. Chờ job recover chạy\n2. Đọc `b_plan_slot.remain_limit`\n"
       "3. So sánh với tổng quantity booking hợp lệ của コース",
       "remain_limit set sai = 0, thực tế = 3",
       "- `remain_limit` **KHÔNG được job sửa lại** (vẫn = 0) — đúng theo phạm vi hiện tại của job\n"
       "- Ghi nhận đây là **giới hạn đã biết**: nếu `remain_limit` bị drift thì không có cơ chế tự phục hồi",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r106「Job hiện tại không recover số booking của plan」. ⚠ Kết hợp TD-17 (2 cơ chế "
            "cập nhật bộ đếm khác nhau) và TD-01 (không transaction) → `remain_limit` là điểm rủi ro cao nhất, "
            "xem MT-28."),

    tc("Job nền", "ENV-003", "Abnormal",
       "Xác nhận cờ ENABLE_EVENT_REMIND trên PRODUCTION — nếu tắt thì remind KHÔNG BAO GIỜ gửi",
       "- Có quyền xem `config.properties` của service Spring Boot trên production (hoặc hỏi Dev/Infra)\n"
       "- Có 1 event với remind đã đăng ký, tới hạn gửi",
       "1. Kiểm tra giá trị cờ `ENABLE_EVENT_REMIND` và `ENABLE_EVENT` trên production\n"
       "2. Query `event_step_time` tìm bản ghi `status = 0` đã quá hạn gửi\n"
       "3. Nếu có bản ghi kẹt → đối chiếu với cờ",
       "config.properties production",
       "- `ENABLE_EVENT_REMIND` phải = **1/true**\n"
       "- KHÔNG có bản ghi `event_step_time` `status = 0` kẹt quá hạn\n"
       "- Nếu chỉ bật `ENABLE_EVENT` mà tắt `ENABLE_EVENT_REMIND` → **RAISE NGAY**: toàn bộ tin remind "
       "không được gửi mà không có cảnh báo",
       env="PRODUCTION",
       note="Nguồn: spec TD-06 (🔴 CAO — `ENABLE_EVENT` khởi động `BotTaskManager` nhưng code xử lý "
            "`event_step_time` đã bị comment out; chỉ `NewEventRemindTask` mới xử lý; **cả 2 cờ mặc định false**). "
            "Corpus KHÔNG có TC này → GAP nghiêm trọng, xem MT-30."),

    tc("Job nền", "JOB-001", "Abnormal",
       "Job remind KHÔNG có cơ chế retry — bản ghi lỗi gửi có được xử lý lại không",
       "- Có quyền tác động `event_step_time` trên môi trường test\n"
       "- Mô phỏng 1 lần gửi lỗi (VD LINE API trả lỗi tạm thời)",
       "1. Tạo tình huống gửi remind lỗi → query `event_step_time.status`\n"
       "2. Chờ ít nhất 2 chu kỳ job\n3. Query lại status của bản ghi đó\n"
       "4. Kiểm tra user có nhận được tin ở lần chạy sau không",
       "1 bản ghi remind gửi lỗi",
       "- Ghi rõ hành vi thật: bản ghi chuyển `STATUS_SEND_ERROR (3)` và **KHÔNG bao giờ được xử lý lại**\n"
       "- User **không nhận được** tin remind đó\n"
       "- Chỉ có cảnh báo Chatwork, không có retry → ghi nhận là rủi ro mất tin vĩnh viễn",
       env="STAGING",
       note="Nguồn: spec TD-15 (KHÔNG có cơ chế retry — `event_step_time.STATUS_SEND_ERROR (3)` và "
            "`action_lineuser.STATUS_FAILURE (3)` không bao giờ được xử lý lại). Corpus KHÔNG có TC → GAP."),

    tc("Job nền", "PERF-LARGE-001", "Abnormal",
       "Job remind quét TOÀN BỘ bản ghi đến hạn của MỌI bot — rủi ro tồn đọng lớn",
       "- Môi trường test có thể tạo lượng lớn bản ghi `event_step_time` đến hạn (VD 50.000 bản ghi)\n"
       "- Có quyền theo dõi bộ nhớ / log của service Spring Boot",
       "1. Tạo lượng lớn bản ghi `event_step_time` đến hạn cùng lúc\n"
       "2. Kích hoạt job remind\n3. Theo dõi mức tiêu thụ bộ nhớ + thời gian chạy + log lỗi\n"
       "4. Kiểm tra số tin thực gửi so với số bản ghi",
       "50.000 bản ghi đến hạn cùng lúc",
       "- Job chạy hết mà **không OOM / không crash service**\n"
       "- Số tin gửi khớp số bản ghi đến hạn\n"
       "- Nếu OOM hoặc treo → **RAISE BUG** (job này không dùng `findTop100/200` như các task khác)",
       env="STAGING",
       note="Nguồn: spec TD-16 (`findAllByStatusAndSentDateTimeLessThanEqual()` lấy TOÀN BỘ record đến hạn của "
            "MỌI bot vào bộ nhớ 1 lần). Corpus KHÔNG có TC hiệu năng job → GAP."),

    tc("Job nền", "JOB-001", "Abnormal",
       "Action booking mất khi service restart giữa chừng (ActionService không recovery)",
       "- Có quyền restart service xử lý action trên môi trường test\n"
       "- Chuẩn bị 1 booking sẽ kích hoạt action (gắn tag / gửi tin xác nhận)",
       "1. Đặt chỗ để sinh bản ghi action ở hàng đợi\n"
       "2. Restart service **ngay khi** bản ghi đang ở trạng thái đang xử lý (`STATUS_IN_QUEUE`)\n"
       "3. Chờ service khởi động lại và chạy vài chu kỳ\n"
       "4. Kiểm tra: user có nhận action không, tag có được gắn không, trạng thái bản ghi",
       "1 action kẹt ở STATUS_IN_QUEUE",
       "- Ghi rõ hành vi thật: nếu bản ghi kẹt vĩnh viễn ở `STATUS_IN_QUEUE` và user **không nhận được "
       "action** → xác nhận đúng mô tả TD-07, RAISE làm rủi ro mất dữ liệu\n"
       "- So sánh với `NewEventRemindTask` (có `findAllByStatus(STATUS_SENDING)` để phục hồi)",
       env="STAGING",
       note="Nguồn: spec TD-07 (🔴 MẤT DỮ LIỆU — `ActionService` chỉ query `STATUS_NEW (0)`, không recovery). "
            "Corpus KHÔNG có TC → GAP."),

    # ══════════════════ 32. Notify & app mobile ══════════════════
    tc("Notify & app mobile", "SYNC-APP-001", "Normal",
       "App mobile nhận notify cho đủ 3 loại yêu cầu: đặt chỗ / đổi lịch / hủy",
       "- Đã cài app mobile, đăng nhập tài khoản admin bot A, đã bật nhận notify\n"
       "- Event E có slot リクエスト制, cho phép đổi và hủy dạng request",
       "1. U1 gửi request đặt chỗ → kiểm tra notify trên app\n"
       "2. U1 gửi request đổi lịch → kiểm tra notify\n3. U1 gửi request hủy → kiểm tra notify\n"
       "4. Mở từng notify → kiểm tra dẫn tới đúng booking",
       "3 loại request",
       "- Cả 3 loại đều **có notify** trên app mobile\n"
       "- Mở notify dẫn tới đúng booking tương ứng, thao tác duyệt/từ chối được ngay",
       note="Nguồn: Task nhỏ r196-r198 + toàn bộ khối #38200 (mỗi TC đều yêu cầu「Send được notify qua app mobile」)."),

    tc("Notify & app mobile", "SYNC-APP-001", "Normal",
       "Trạng thái booking đồng bộ giữa WEB và APP ngay sau thao tác",
       "- Đã cài app mobile\n- Có 1 booking `status = 3` chờ duyệt",
       "1. Mở màn quản lý booking trên **web** và trên **app** cùng lúc\n"
       "2. Duyệt booking trên **web**\n3. Reload màn app → đọc trạng thái\n"
       "4. Với booking khác: từ chối trên **app** → reload màn web → đọc trạng thái",
       "1 booking duyệt ở web, 1 booking từ chối ở app",
       "- Sau thao tác ở web, app hiện đúng trạng thái mới (承認)\n"
       "- Sau thao tác ở app, web hiện đúng trạng thái mới (否認)\n"
       "- Không có màn nào hiện trạng thái cũ (stale)",
       note="TC bổ sung theo SYNC-APP-001 — corpus có nhiều TC thao tác ở app nhưng KHÔNG có TC đối chiếu "
            "đồng bộ 2 chiều web ⇔ app."),

    tc("Notify & app mobile", "UI-003", "Normal",
       "Màn Booking event KHÔNG hiển thị gói giá ở header (sau SpecImprove #33297)",
       "- Đã chọn bot ở màn home\n- Mở màn Booking event (menu 予約管理 → Booking event)",
       "1. Mở màn quản lý Booking event\n2. Quan sát vùng header\n"
       "3. Lặp lại với các loại bot: Free / Standard / Pro / enterprise",
       "4 loại gói bot",
       "- Header **KHÔNG hiển thị Gói giá** ở mọi loại bot",
       note="Nguồn: TCsLine_Improve chung / tab「Improve nhỏ」r386 (SpecImprove #33297, 12/2025 — "
            "xóa hiển thị plan type trên header, áp cho toàn bộ màn)."),

    # ══════════════════ 33. Giới hạn theo gói ══════════════════
    tc("Giới hạn theo gói", "PAY-LIMIT-001", "Boundary",
       "[Free mới] Tạo event đến đúng giới hạn 2, chặn ở bản ghi thứ 3",
       "- Bot ở plan **Free mới** (`flag_contract_new = 1`)\n- Admin đã đăng nhập; hiện có 0/2 event",
       "1. Vào màn quản lý Event booking (イベント予約)\n"
       "2. Tạo mới lần lượt đủ 2 event (đến khi đạt giới hạn của gói)\n"
       "3. Tạo thêm 1 event nữa (bản ghi thứ 3)",
       "Bot Free mới; giới hạn = 2",
       "- Tạo được đúng **2** event thành công (bản ghi thứ 2 = biên trên vẫn OK)\n"
       "- Bản ghi thứ 3: hệ thống **CHẶN**, không tạo thêm\n"
       "- Hiện thông báo **「現在のプランは利用できない機能です。アップグレードが必要になります。」**\n"
       "- Tổng số event active sau thao tác = **2**",
       note="Nguồn: TCsLine_Test Limit theo plan / tab「[AI] Test limit v2」r81 (TC-LMT-058). Spec BR-01."),

    tc("Giới hạn theo gói", "CONC-001", "Abnormal",
       "[Free mới] Mở 2 tab ở slot cuối (đang 1/2) → tạo event đồng thời chỉ 1 tab thành công",
       "- Bot ở plan **Free mới**; đang có đúng 1/2 event (còn 1 slot cuối)\n"
       "- Đăng nhập cùng 1 tài khoản trên 2 tab",
       "1. Tab A và Tab B cùng mở màn tạo mới event\n2. Nhập dữ liệu hợp lệ ở cả 2 tab\n"
       "3. Bấm lưu/tạo ở Tab A rồi Tab B gần như đồng thời",
       "Bot Free mới; giới hạn = 2",
       "- Chỉ **1** trong 2 thao tác tạo thành công → tổng event = **2**\n"
       "- Thao tác còn lại bị **CHẶN** với thông báo 「現在のプランは利用できない機能です。"
       "アップグレードが必要になります。」\n- **KHÔNG tạo ra bản ghi thứ 3**",
       note="Nguồn: [AI] Test limit v2 r82 (TC-LMT-059). Spec BR-02 (re-check ở MỌI step tạo của wizard "
            "để chặn bypass — ticket #37292)."),

    tc("Giới hạn theo gói", "CONC-001", "Abnormal",
       "[Free mới] Double-click nút tạo ở slot cuối → không tạo trùng vượt giới hạn",
       "- Bot ở plan **Free mới**; đang có đúng 1/2 event (còn 1 slot cuối)",
       "1. Vào màn tạo mới event, nhập dữ liệu hợp lệ\n"
       "2. Double-click (nhấn nhanh 2 lần <300ms) vào nút lưu/tạo",
       "Bot Free mới; giới hạn = 2",
       "- Chỉ tạo đúng **1** event → tổng = **2**\n- **KHÔNG** tạo 2 bản ghi (không vượt 3)\n"
       "- Nếu lần nhấn thứ 2 chạm giới hạn thì hiện thông báo「現在のプランは利用できない機能です。"
       "アップグレードが必要になります。」",
       note="Nguồn: [AI] Test limit v2 r83 (TC-LMT-060)."),

    tc("Giới hạn theo gói", "PAY-LIMIT-001", "Abnormal",
       "[Free mới] Copy event khi đang ở giới hạn 2 → bị chặn",
       "- Bot ở plan **Free mới**; đang có đúng 2/2 event (đã đạt giới hạn); có ≥1 event để copy",
       "1. Vào màn quản lý Event booking (イベント予約)\n2. Chọn 1 event hiện có → nhấn Copy/Nhân bản",
       "Bot Free mới; giới hạn = 2",
       "- Hệ thống **CHẶN** thao tác copy (vì sẽ vượt 2)\n"
       "- Hiện thông báo 「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- Tổng event vẫn = **2**",
       note="Nguồn: [AI] Test limit v2 r84 (TC-LMT-061). Đường copy cũng phải bị chặn — điểm hay bị bỏ sót."),

    tc("Giới hạn theo gói", "CONC-001", "Abnormal",
       "[Free mới] Copy event đồng thời từ 2 tab / double-click nút Copy ở slot cuối",
       "- Bot ở plan **Free mới**; đang có đúng 1/2 event (còn 1 slot)",
       "1. Tab A và Tab B cùng chọn 1 event để copy → bấm Copy gần như đồng thời → kiểm tra tổng event\n"
       "2. Reset về 1/2 event; chọn 1 event → double-click nút Copy (<300ms) → kiểm tra tổng event",
       "Bot Free mới; giới hạn = 2",
       "- Cả 2 kịch bản: chỉ **1** bản copy được tạo → tổng = **2**\n"
       "- Không tạo bản ghi thứ 3; thao tác bị chặn hiện đúng thông báo giới hạn gói",
       note="Nguồn: [AI] Test limit v2 r85-r86 (TC-LMT-062, TC-LMT-063). 2 kịch bản race cùng 1 kết quả → gộp."),

    tc("Giới hạn theo gói", "PAY-LIMIT-001", "Boundary",
       "[Standard mới] Tạo event đến đúng giới hạn 10, chặn ở bản ghi thứ 11",
       "- Bot ở plan **Standard mới** (`flag_contract_new = 1`)\n- Admin đã đăng nhập; hiện có 0/10 event",
       "1. Vào màn quản lý Event booking\n2. Tạo mới lần lượt đủ 10 event\n3. Tạo thêm 1 event nữa (thứ 11)",
       "Bot Standard mới; giới hạn = 10",
       "- Tạo được đúng **10** event (bản ghi thứ 10 = biên trên vẫn OK)\n"
       "- Bản ghi thứ 11: **CHẶN**, hiện thông báo **「スタンダードプランの上限に達しています。"
       "制限を解除する場合は、プロプランへの変更が必要になります。」**\n- Tổng event = **10**",
       note="Nguồn: [AI] Test limit v2 r87 (TC-LMT-064). Spec BR-01 — chú ý message KHÁC với gói Free."),

    tc("Giới hạn theo gói", "CONC-001", "Abnormal",
       "[Standard mới] Race ở slot cuối (đang 9/10) — 2 tab tạo / double-click / 2 tab copy / double-click copy",
       "- Bot ở plan **Standard mới**; đang có đúng 9/10 event (còn 1 slot cuối)",
       "1. 2 tab cùng tạo event → kiểm tra tổng\n2. Reset về 9/10; double-click nút tạo → kiểm tra tổng\n"
       "3. Reset về 9/10; 2 tab cùng copy 1 event → kiểm tra tổng\n"
       "4. Reset về 9/10; double-click nút Copy → kiểm tra tổng",
       "Bot Standard mới; giới hạn = 10; 4 kịch bản race",
       "- Cả 4 kịch bản: chỉ **1** bản ghi được tạo → tổng = **10**\n"
       "- **KHÔNG** tạo bản ghi thứ 11\n"
       "- Thao tác bị chặn hiện thông báo giới hạn gói Standard",
       note="Nguồn: [AI] Test limit v2 r88-r92 (TC-LMT-065 → TC-LMT-069). 4 kịch bản cùng 1 kết quả → gộp 1 TC."),

    tc("Giới hạn theo gói", "PAY-LIMIT-001", "Normal",
       "[Free cũ / Standard cũ / Pro] KHÔNG giới hạn số event",
       "- Chuẩn bị 3 bot: Free cũ (`created < 2021-07-01` HOẶC `flag_contract_new = 0`), "
       "Standard cũ (`flag_contract_new = 0`, tạo trước 2021-07), và Pro\n- Mỗi bot hiện có 0 event",
       "1. Với từng bot: vào màn quản lý Event booking\n"
       "2. Tạo mới liên tiếp vượt ngưỡng của gói mới tương ứng (Free cũ: >2, Standard cũ: >10, Pro: >10)\n"
       "3. Ghi lại có bị chặn ở mốc nào không",
       "3 bot: Free cũ · Standard cũ · Pro",
       "- **Cả 3 bot đều KHÔNG bị chặn** — tạo được vượt ngưỡng của gói mới\n"
       "- Không hiện thông báo giới hạn gói",
       note="Nguồn: [AI] Test limit v2 r93-r95 (TC-LMT-224, TC-LMT-225, TC-LMT-226). Spec BR-01 "
            "(giới hạn chỉ áp khi `flag_contract_new = 1`; gói Pro không giới hạn)."),

    tc("Giới hạn theo gói", "PAY-LIMIT-001", "Abnormal",
       "Bypass giới hạn gói bằng cách mở link trực tiếp từng step của wizard tạo event",
       "- Bot ở plan **Free mới**, đang có đúng 2/2 event (đã đạt giới hạn)\n"
       "- Biết URL từng step của wizard (basic / step2 / step3 / bill4 / previewTermBill / addDateSlot)",
       "1. Mở trực tiếp URL của từng step (không đi qua màn list)\n"
       "2. Với mỗi step, thử lưu dữ liệu hợp lệ\n3. Đếm số event sau mỗi lần thử",
       "6 điểm vào wizard, bot đã đạt giới hạn",
       "- **Mọi step đều bị chặn**, hiện thông báo giới hạn gói\n"
       "- Tổng event vẫn = **2**, không tạo được event thứ 3 qua bất kỳ đường nào",
       note="Nguồn: spec BR-02 (re-check ở MỌI step tạo — `:1269-1275`, `:548-554`, `:649-655`, `:712-718`, "
            "`:769-775`, `:6315-6321`; ticket #37292). TC bổ sung — corpus [AI] Test limit v2 chỉ test 2 tab và "
            "double-click, chưa test bypass qua URL trực tiếp."),

    # ══════════════════ 34. Phân quyền & môi trường ══════════════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Account staff ĐƯỢC cấp quyền → thao tác đầy đủ trên các màn event booking",
       "- Bot A có account staff Y **được cấp quyền** màn event booking\n- Event E có sẵn slot và booking",
       "1. Đăng nhập bằng staff Y\n2. Mở lần lượt: màn list event · màn edit event · màn 開催日 · "
       "màn 予約枠一覧 · màn 参加者リスト · màn detail booking\n"
       "3. Thực hiện 1 thao tác ghi ở mỗi màn (tạo folder / sửa slot / duyệt booking)",
       "staff Y có quyền",
       "- Mở được toàn bộ các màn, hiển thị dữ liệu bình thường\n"
       "- Thao tác ghi thành công; lịch sử ghi đúng tên staff Y",
       note="Nguồn: TCsLine_Improve chung /「Improve nhỏ」r319 + các dòng「Check account staff」rải rác trong "
            "corpus event booking (Event booking 1.0 r355, 2.0 r80, 3.0 r66, stripe r80, univapay r183 — "
            "**tất cả đều KHÔNG có kết quả mong đợi**). Expected do AI viết → xem MT-31."),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "Account staff KHÔNG được cấp quyền → chặn ở CẢ giao diện lẫn URL / API trực tiếp",
       "- Bot A có account staff X **KHÔNG được cấp quyền** màn event booking\n"
       "- Biết URL các màn event booking và các endpoint `/ajax/...` tương ứng",
       "1. Đăng nhập staff X → kiểm tra menu 予約管理 có hiện mục イベント予約 không\n"
       "2. Dán trực tiếp URL màn list event → quan sát\n3. Dán URL màn edit event → quan sát\n"
       "4. Gọi thẳng endpoint `/ajax/get-list-event-day` và 1 endpoint GHI (tạo/sửa/xóa slot) "
       "bằng session của staff X\n5. Query DB kiểm tra có bản ghi nào bị tạo/sửa không",
       "staff X không có quyền · 2 URL màn hình · 2 endpoint AJAX (1 đọc, 1 ghi)",
       "- Menu KHÔNG hiện mục イベント予約\n"
       "- Dán URL: **không truy cập được**\n"
       "- Gọi thẳng endpoint AJAX: **bị từ chối**; KHÔNG đọc được dữ liệu event; KHÔNG ghi được bản ghi nào\n"
       "⚠ **Dự kiến FAIL** — nếu vào được thì đúng bug đã ghi nhận, RAISE lại",
       note="⚠ MT-32. Nguồn: TCsLine_Improve chung /「Improve nhỏ」r320 — kết quả **NG**, ghi chú "
            "「Các màn booking không được phân quyền nhưng vẫn access được」, Bug Tester **#33106** (chưa thấy fix). "
            "Spec TD-03 (🔴 nhóm route `/ajax` chỉ có `check_login`, KHÔNG có `basic_access`) + G-08 "
            "(chưa xác định menu イベント予約 có trong `getRouterBotInvite()` không). "
            "Ghi nhớ dự án: bug phân quyền phải rà ở TẦNG API, không chỉ UI."),

    tc("Phân quyền & môi trường", "SEC-ISO-001", "Abnormal",
       "Cách ly dữ liệu giữa 2 bot — bot A không thao tác được lên event / slot / booking của bot B",
       "- Bot A và bot B đều của cùng 1 tài khoản đăng nhập\n"
       "- Bot B có event F (biết id), slot (biết id), booking (biết id)",
       "1. Đăng nhập, chọn **bot A**\n2. Mở trực tiếp URL màn edit event của **bot B** → quan sát\n"
       "3. Gọi endpoint sửa slot với `slot_id` của bot B → query DB kiểm tra\n"
       "4. Gọi endpoint duyệt booking với `booking_id` của bot B → query DB\n"
       "5. Gọi endpoint hoàn tiền với `bot_id` sửa thành bot B → query DB",
       "4 điểm thao tác chéo bot",
       "- Cả 4 điểm: **bị từ chối**, không đọc và không ghi được dữ liệu của bot B\n"
       "⚠ Riêng hoàn tiền: spec TD-02 xác nhận `bot_id` lấy TỪ REQUEST → **dự kiến FAIL**, RAISE NGAY",
       env="STAGING",
       note="Nguồn: TCsLine_Improve chung /「Improve nhỏ」r304 + khối Bug Tester #33107「Bot A đang access được "
            "link của bot B => Check lại cho all màn」(NG ở màn template/item) + spec TD-02 (IDOR refund). "
            "Xem MT-06 và MT-09."),

    tc("Phân quyền & môi trường", "SEC-001", "Abnormal",
       "Endpoint set-cookie nằm ngoài group auth — truy cập khi CHƯA đăng nhập",
       "- Đăng xuất hoàn toàn (xóa session)\n- Biết URL `GET /basic/event-booking-day/set-cookie`",
       "1. Ở trạng thái chưa đăng nhập, gọi trực tiếp URL set-cookie\n2. Quan sát response\n"
       "3. Kiểm tra cookie được ghi\n4. Thử truyền tham số bất thường (bot_id lạ) → quan sát",
       "Chưa đăng nhập, gọi EP-18 trực tiếp",
       "- Ghi rõ hành vi thật: endpoint có trả 200 và ghi cookie không\n"
       "- **KHÔNG được lộ dữ liệu** nào của bot (danh sách event, folder…)\n"
       "- Nếu ghi được cookie mà không cần đăng nhập → ghi nhận đúng TD-04, RAISE ở mức thông tin",
       env="STAGING",
       note="Nguồn: spec TD-04 (🔴 route `GET /basic/event-booking-day/set-cookie` (EP-18) nằm NGOÀI mọi group "
            "auth — `routes/web.php:3720`). Corpus KHÔNG có TC → GAP bảo mật."),

    tc("Phân quyền & môi trường", "STATE-CLEAN-001", "Abnormal",
       "Bot đang BACKUP / RESTORE → mọi thao tác GHI ở event booking bị chặn",
       "- Bot A có bản ghi `backup_history` với `code = bot.transfer_code` và `status ∈ {0, 1}` "
       "(đang backup/restore)",
       "1. Mở màn list event → thử tạo folder mới\n2. Thử tạo/sửa event\n3. Thử tạo/sửa slot\n"
       "4. Thử duyệt 1 booking\n5. Thử hoàn tiền 1 booking\n6. Quan sát thông báo ở từng bước",
       "5 thao tác ghi khi bot đang backup",
       "- **Cả 5 thao tác đều bị chặn**, trả HTTP 500 kèm nội dung `MESSAGE_NOTIFY_BACKUP`\n"
       "- Không bản ghi nào bị tạo/sửa trong DB\n- Thao tác ĐỌC (xem danh sách) vẫn hoạt động",
       env="STAGING",
       note="Nguồn: spec BR-03 (áp dụng cho MỌI action ghi, có `file:line` ở 16 vị trí). "
            "Corpus KHÔNG có TC backup cho event booking → GAP."),

    tc("Phân quyền & môi trường", "DATA-BACKUP-001", "Normal",
       "Backup / Recover bot → dữ liệu event booking được khôi phục đầy đủ và đúng liên kết",
       "- Bot A có event E đầy đủ: 2 開催日, 3 slot, 4 コース, action đã set, 5 booking, remind\n"
       "- Có quyền thực hiện backup và recover trên môi trường test",
       "1. Ghi lại toàn bộ id + số liệu của event E\n2. Thực hiện backup bot A\n"
       "3. Recover sang bot mới (hoặc khôi phục lại bot A)\n"
       "4. Đối chiếu: số event / số ngày / số slot / số コース / action / danh sách CSV các plan_ids\n"
       "5. Kiểm tra `b_slot.plan_ids` có trỏ đúng id コース mới không",
       "1 event đầy đủ 4 tầng dữ liệu",
       "- Sau recover: đủ 2 開催日, 3 slot, 4 コース, action giữ nguyên nội dung\n"
       "- **`b_slot.plan_ids` (CSV) trỏ đúng id コース mới sau remap**, không trỏ id cũ\n"
       "- Ghi rõ booking và remind có được khôi phục không",
       env="STAGING",
       note="Nguồn: spec TD-24 (`b_slot.plan_ids` là CSV denormalized — `BackupBotTask.java:623-633` phải remap "
            "thủ công → nguy cơ lệch). Corpus KHÔNG có TC backup event booking → GAP."),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Event đời cũ (v1, type_event_new = 0) chạy song song không xung đột với event v2",
       "- Bot A có cả event v1 (`type_event_new = 0`) và event v2 (`type_event_new = 1`)",
       "1. Mở màn quản lý event v2 (/basic/booking-event-day/list-event) → đếm số event hiển thị\n"
       "2. Kiểm tra event v1 có bị lọt vào danh sách v2 không\n"
       "3. Mở màn quản lý event v1 (nếu còn) → kiểm tra ngược lại\n"
       "4. Thao tác sửa/xóa 1 event v2 → kiểm tra event v1 không bị ảnh hưởng",
       "1 event v1 + 2 event v2",
       "- Màn v2 chỉ hiện **2** event v2, KHÔNG hiện event v1\n"
       "- Thao tác trên v2 không làm thay đổi dữ liệu event v1 (2 bộ dùng chung bảng nhưng khác controller)",
       note="Nguồn: spec §1.3 (event v1 dùng chung bảng nhưng khác controller — `BookingEventController` / "
            "`BookingEventManagementController`, là tính năng riêng). Corpus có tab「Improve event cũ 2023.03」và "
            "「Sheet4」thuộc bộ v1 → xem MT-33 về phạm vi."),

    tc("Phân quyền & môi trường", "DATA-MIG-001", "Abnormal",
       "Booking có status = 0 (giá trị không có trong định nghĩa) — UI render ra sao",
       "- Có quyền query / tạo bản ghi test trên môi trường test\n"
       "- Tạo 1 booking với `b_user_booking.status = 0`",
       "1. Query production đếm số booking `status = 0` (đối chiếu 9 rows spec ghi nhận)\n"
       "2. Trên môi trường test, tạo 1 booking `status = 0`\n"
       "3. Mở màn 参加者リスト và màn detail booking → quan sát badge trạng thái\n"
       "4. Mở màn lịch sử phía LINE user → quan sát\n5. Export CSV → quan sát cột trạng thái",
       "status = 0 (không có trong `config/sns-line.php:398-407`)",
       "- Ghi rõ hành vi thật ở 4 điểm hiển thị: badge trống / hiện nhãn sai / lỗi trang\n"
       "- **KHÔNG được lỗi 500** ở bất kỳ màn nào\n"
       "- Nếu render sai nhãn → RAISE để bổ sung định nghĩa trạng thái",
       env="STAGING",
       note="Nguồn: spec G-12 / TD-19 (`b_user_booking.status = 0` — 9 rows trong dump, không có trong config). "
            "Corpus KHÔNG có TC → GAP, xem MT-34."),

    tc("Phân quyền & môi trường", "ENV-003", "Normal",
       "Khác biệt dev / staging / production ở các điểm phụ thuộc hạ tầng",
       "- Có quyền truy cập cả staging và production\n- Event E tương đương ở cả 2 môi trường",
       "1. So sánh domain LIFF của link đặt chỗ ở staging và production\n"
       "2. So sánh cổng thanh toán (khóa test / live) ở 2 môi trường\n"
       "3. So sánh trạng thái job remind / job recover count ở 2 môi trường\n"
       "4. Ghi lại điểm khác biệt nào có thể làm TC pass ở staging nhưng fail ở production",
       "staging vs production",
       "- Ghi rõ bảng đối chiếu 3 điểm: domain LIFF · cổng thanh toán · job nền\n"
       "- Mọi TC gắn nhãn PRODUCTION trong bộ này đều có lý do rõ ràng dựa trên bảng đối chiếu",
       env="PRODUCTION",
       note="TC bổ sung theo ENV-003 + RULE-08. Corpus có cột kết quả「staging」riêng cho mọi tab → xác nhận "
            "team đã có thói quen test 2 môi trường, nhưng KHÔNG có TC ghi lại điểm khác biệt."),

    tc("Phân quyền & môi trường", "DEPLOY-ASSET-001", "Normal",
       "Sau release — asset JS/CSS của màn event booking được nạp bản mới, không dính cache cũ",
       "- Vừa có release chạm code màn event booking\n- Trình duyệt đã từng mở màn này trước release",
       "1. Mở màn quản lý event booking bằng trình duyệt CÓ cache cũ (không hard refresh)\n"
       "2. Mở DevTools → tab Network, kiểm tra version/hash của file JS/CSS được nạp\n"
       "3. Thao tác 1 chức năng vừa được sửa trong release\n4. Hard refresh và so sánh",
       "Trình duyệt có cache trước release",
       "- File JS/CSS nạp về là **bản mới** (khác hash/version so với trước release)\n"
       "- Chức năng vừa sửa hoạt động đúng **mà không cần hard refresh**\n"
       "- Không xuất hiện lỗi JS do lẫn bản cũ và bản mới",
       env="PRODUCTION",
       note="TC bổ sung theo DEPLOY-ASSET-001. Corpus KHÔNG có TC deploy cho event booking → GAP."),
]

# ── Bổ sung sau BƯỚC 7 (audit RULE-01: quan điểm ưu tiên Cao phải đủ 3 loại case) ──
S6 += [
    tc("Tạo & sửa event — khung", "FUNC-001", "Boundary",
       "Event có SỐ LƯỢNG LỚN 開催日 / slot / コース → lưu, hiển thị và đặt chỗ vẫn đúng",
       "- Admin bot A (gói Pro, không giới hạn số event)\n"
       "- Chuẩn bị 1 event với 31 開催日, mỗi ngày 10 予約枠, mỗi 予約枠 5 コース",
       "1. Tạo event với quy mô trên (dùng chức năng copy ngày để dựng nhanh)\n"
       "2. Lưu event → đo thời gian lưu\n3. Mở lại tab「開催日程」→ đếm số ô ngày\n"
       "4. Mở màn list event đọc cột 定員 → đối chiếu phép tính tay\n"
       "5. Mở trang LIFF phía LINE user → đếm số ngày/slot/コース hiển thị và đặt thử 1 chỗ",
       "31 ngày × 10 slot × 5 コース = 1.550 コース; mỗi コース 定員 2 → tổng 定員 = 3.100",
       "- Lưu thành công, không timeout / không lỗi 500\n"
       "- Tab 開催日程 hiện đủ **31** ô ngày; mỗi ô hiện đủ 10 dòng giờ\n"
       "- Cột 定員 ở màn list hiện đúng **3.100**\n"
       "- Trang LIFF hiển thị đủ và đặt chỗ thành công",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: FUNC-001 là quan điểm ưu tiên **Cao**, corpus chỉ có "
            "TC Normal, thiếu Boundary. Quy mô 31×10×5 lấy theo giới hạn thực tế (1 tháng sự kiện)."),

    tc("Gói コース (plan)", "PAY-STATE-001", "Boundary",
       "Thanh toán ở biên số tiền — コース 料金 = 50 円 (nhỏ nhất) và số tiền lớn",
       "- Event bật 決済 Stripe, bot A liên kết Stripe\n"
       "- コース P_min 料金 = 50 円 · コース P_max 料金 = 999.999 円\n-「1回の予約上限」= 3",
       "1. U1 đặt 1 chỗ ở コース P_min, thanh toán bằng thẻ hợp lệ → kiểm tra Stripe dashboard\n"
       "2. U1 đặt 3 chỗ ở コース P_max, thanh toán → kiểm tra Stripe dashboard\n"
       "3. Với mỗi lần, đối chiếu `b_user_booking.amount` với phép tính tay",
       "50 円 × 1 chỗ = 50 円\n999.999 円 × 3 chỗ = 2.999.997 円",
       "- Cả 2 giao dịch **thanh toán thành công**\n"
       "- Stripe dashboard hiện đúng **50 JPY** và **2.999.997 JPY**\n"
       "- `amount` trong DB khớp phép tính tay, không làm tròn / không tràn số",
       env="PRODUCTION",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: PAY-STATE-001 ưu tiên **Cao**, corpus có Normal + Abnormal "
            "nhưng thiếu Boundary. Mốc 50 円 lấy theo spec Field Matrix #45 (xem MT-19)."),

    tc("アクション設定", "MSG-004", "Abnormal",
       "Action text chèn biến số tiền nhưng booking KHÔNG có コース và KHÔNG thu tiền",
       "- Slot S_free KHÔNG có コース, event KHÔNG bật 決済, 承認方法 = 全承認\n"
       "- Action「予約完了」có chèn đủ 5 biến (tên event / ngày / giờ / số người / **số tiền**)",
       "1. U1 đặt 1 chỗ ở slot S_free\n2. Mở LINE app đọc tin nhận được\n"
       "3. Quan sát vị trí biến số tiền trong tin",
       "Booking không có コース, không có 料金",
       "- Tin gửi đi **KHÔNG còn ký hiệu biến thô**\n"
       "- Biến số tiền được thay bằng giá trị hợp lý (0 円 / để trống / bỏ dòng) — ghi rõ hành vi thật\n"
       "- Không hiện chuỗi lỗi kiểu null / undefined / ký hiệu biến chưa thay",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: MSG-004 ưu tiên **Cao**, corpus chỉ có TC Normal. "
            "Hành vi thay biến khi không có dữ liệu chưa có ở corpus lẫn spec → cần Leader chốt sau khi chạy."),

    tc("Form 予約時入力項目", "FRIEND-001", "Abnormal",
       "Friend info bị XÓA ở màn quản lý thông tin bạn bè trong khi item form đang liên kết tới nó",
       "- Event E có item form liên kết tới friend info tùy chỉnh「参加動機」\n"
       "- Đã có 2 booking điền giá trị cho item này",
       "1. Vào màn quản lý thông tin bạn bè, **xóa** friend info「参加動機」\n"
       "2. Mở lại tab「各種ページ」→ Step 2 của event E → quan sát item đó\n"
       "3. LINE user mở trang đặt chỗ → quan sát form\n4. Đặt thử 1 chỗ\n"
       "5. Mở màn detail 2 booking cũ → quan sát đáp án",
       "1 friend info bị xóa, đang được 1 item form liên kết",
       "- Màn setting item **mở được, không lỗi 500**\n- Trang đặt chỗ phía LINE user **không lỗi**\n"
       "- Đặt chỗ mới vẫn thành công (ghi rõ item đó còn hiện hay bị ẩn)\n"
       "- 2 booking cũ vẫn xem được đáp án đã lưu",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: FRIEND-001 ưu tiên **Cao**, corpus chỉ có TC Normal. "
            "Spec BR-20 mô tả mapping nhưng KHÔNG mô tả vòng đời khi friend info bị xóa (liên quan MT-21)."),

    tc("Khung giờ 予約枠", "MSG-002", "Abnormal",
       "Remind đang gắn vào slot bị XÓA ở màn /basic/events → booking mới xử lý ra sao",
       "- Slot S1 bật「リマインド配信」và chọn remind R1\n- Đã có 1 booking được add remind theo R1",
       "1. Vào màn quản lý remind /basic/events → **xóa** remind R1\n"
       "2. Mở lại màn setting slot S1 → quan sát dropdown「リマインド選択」\n"
       "3. LINE user đặt 1 chỗ mới ở slot S1 → query `user_event`\n"
       "4. Query `user_event` của booking cũ → kiểm tra còn không\n"
       "5. Chờ tới mốc remind → kiểm tra có tin nào gửi đi không",
       "Remind R1 bị xóa sau khi đã gắn vào slot",
       "- Màn setting slot **mở được, không lỗi 500**; dropdown xử lý được tham chiếu treo\n"
       "- Đặt chỗ mới **vẫn thành công** (ghi rõ có add remind hay không)\n"
       "- Booking cũ: ghi rõ bản ghi `user_event` còn hay bị dọn\n"
       "- **KHÔNG gửi tin remind rỗng / lỗi** cho LINE user",
       env="PRODUCTION",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: MSG-002 ưu tiên **Cao**, corpus chỉ có TC Normal. "
            "Spec Field Matrix #38 (`event_id` → `events.id`, `remind_id` → `event_times.id`) KHÔNG mô tả "
            "ràng buộc khi remind bị xóa."),

    tc("Gói コース (plan)", "DATA-REF-001", "Normal",
       "Đổi TÊN コース đang được booking tham chiếu → mọi nơi hiển thị tên mới",
       "- コース P1「Aコース」có 3 booking đã duyệt",
       "1. Đổi tên コース P1 thành「Bコース」→ Lưu\n"
       "2. Mở màn 参加者リスト → đọc cột コース của 3 booking cũ\n"
       "3. Mở màn detail từng booking → đọc tên コース\n4. Export CSV → đọc cột コース\n"
       "5. Cho 1 user đổi lịch → đọc tin action nhận được trên LINE",
       "「Aコース」→「Bコース」, 3 booking cũ",
       "- Cả 4 điểm hiển thị (danh sách / detail / CSV / tin LINE) đều hiện **「Bコース」**\n"
       "- KHÔNG chỗ nào còn hiện「Aコース」và KHÔNG chỗ nào hiện rỗng\n"
       "- Liên kết đi theo `plan_slot_id` chứ không theo tên (DATA-ID-001)",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: DATA-REF-001 ưu tiên **Cao**, corpus chỉ có TC Abnormal "
            "(xóa). Đây là chiều rename còn thiếu."),

    tc("Export CSV", "OUT-EXPORT-001", "Boundary",
       "Export CSV với số lượng booking LỚN → file đủ dòng, không timeout",
       "- Event E có **5.000 booking** (dựng bằng script trên môi trường test)\n"
       "- Form có 5 item friend info",
       "1. Mở màn danh sách người tham gia → bấm export CSV\n2. Đo thời gian tới khi file tải xong\n"
       "3. Mở file, đếm số dòng dữ liệu\n4. Kiểm tra dòng đầu và dòng cuối có đủ cột không",
       "5.000 booking × (cột cũ + 5 cột friend info)",
       "- File tải về thành công, **không timeout / không lỗi 500**\n"
       "- File có đúng **5.000** dòng dữ liệu (không kể header)\n"
       "- Dòng cuối đủ cột, không bị cắt giữa chừng\n- Ghi lại thời gian export làm mốc hiệu năng",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: OUT-EXPORT-001 là quan điểm **BẮT BUỘC (nâng Cao)** với mọi "
            "chức năng export, corpus chỉ có TC Normal. Ngưỡng 5.000 theo PERF-LARGE-001 (ngưỡng THỰC TẾ)."),

    tc("Copy & xóa event", "DATA-BACKUP-001", "Abnormal",
       "Copy event ngay khi event gốc đang được SỬA ở tab khác (chưa lưu)",
       "- Event E đang mở ở tab 1 (màn edit, đã sửa vài setting nhưng CHƯA lưu)\n"
       "- Tab 2 mở màn list event",
       "1. Ở tab 1: sửa tiêu đề event + thêm 1 slot, **chưa bấm lưu**\n"
       "2. Ở tab 2: bấm copy event E\n3. Mở bản copy → đối chiếu với trạng thái ĐÃ LƯU của E\n"
       "4. Quay lại tab 1 bấm lưu → kiểm tra event E\n5. Mở lại bản copy → kiểm tra có bị ảnh hưởng không",
       "Sửa chưa lưu ở tab 1, copy ở tab 2",
       "- Bản copy phản ánh đúng trạng thái **ĐÃ LƯU** của E (không lấy dữ liệu đang sửa dở)\n"
       "- Sau khi tab 1 lưu: event E cập nhật đúng, **bản copy KHÔNG bị thay đổi theo**\n"
       "- Không phát sinh lỗi ở cả 2 tab",
       note="Bổ sung sau BƯỚC 7 audit — RULE-01: DATA-BACKUP-001 ưu tiên **Cao**, corpus chỉ có TC Normal."),
]
