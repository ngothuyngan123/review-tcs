# -*- coding: utf-8 -*-
"""FA-021 イベント予約 (Event booking) — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: 11.3 TCsLine_EventBooking (10 tab) + TCsLine_Improve chung + TCsLine_Test Limit theo plan.
Nguồn spec: spec-features/admin/event-booking/ (feature-spec.md · web/logic-spec.md · web/api-spec.md ·
            job/job-spec.md · db/db-mapping.md · ui/ui-spec.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "Duyệt booking ở WEB chọn「không gửi action」thì có gửi action không?",
     "「Task nhỏ + fix bug KH」r125-r140 (khối Bug KH #38200, 06/2026): tiêu đề ghi rõ "
     "「Admin approve booking ở web, **chọn không action**」nhưng cột Expect Result ghi "
     "「- Send được action approve cho user => Check phía line user và hiển thị trên chat 1:1」— "
     "**giống hệt** khối「chọn có action」(r109-r124).\n"
     "Ngược lại khối APP MOBILE r170-r185 cùng ticket ghi「**Không** send action approve cho user」.",
     "`feature-spec.md:690` Field Matrix #54:「予約受付時アクション」(実行する/しない) → "
     "`b_user_booking.action_before_booking`, ⚠ **`0` = CÓ thực thi** (tên cột ngược nghĩa).\n"
     "`feature-spec.md:1214` TD-22 liệt kê `action_before_booking` là 1 trong 3 cột NGƯỢC NGHĨA.\n"
     "Spec KHÔNG mô tả riêng hành vi của nhánh web vs app.",
     "Nếu member chạy theo TC gốc ở web thì sẽ báo PASS khi hệ thống VẪN gửi action dù admin đã chọn "
     "「không action」— tức là bỏ lọt đúng lỗi mà tùy chọn này sinh ra để tránh. Cột ngược nghĩa "
     "`action_before_booking` làm khả năng code hiểu sai giá trị rất cao. Đây là hành vi người dùng cuối "
     "nhìn thấy (nhận hay không nhận tin LINE).",
     "『Admin — duyệt / từ chối booking』TC「Duyệt booking ở WEB chọn KHÔNG gửi action → xác nhận hành vi "
     "gửi action」",
     "",
     "① Hỏi Dev: web và app dùng chung hàm xử lý action hay tách riêng.\n"
     "② Chốt expected chuẩn cho web (theo logic phải giống app: KHÔNG gửi action).\n"
     "③ Nếu chốt「không gửi」→ sửa expected 16 dòng r125-r140 của sheet gốc + ghi chú TC gốc sai.\n"
     "④ Bổ sung vào spec §2.7/§2.8 mô tả rõ hành vi của tùy chọn 実行する/しない ở CẢ web và app."],

    ["MT-02", "CAO", W,
     "Đổi lịch giữa slot CÓ コース ↔ slot KHÔNG コース thì gửi action của slot nào?",
     "「Event booking 2.0」r96-r97 (Bug **TỰ DETECT**, chưa fix):「change từ slot B có plan sang slot A "
     "không có plan => case request change đang send action của slot B??? => **Đúng thì phải send action "
     "của slot A**」.\n"
     "Cùng tab r55-r58 khẳng định quy tắc chung: sau khi đổi thì「Gửi action của **B** (slot đích)」.",
     "`feature-spec.md:723` BR-17: `using_action_slot_booking_v1` (hoặc `_change_request`/`_cancel`) trên "
     "`b_slot` — `= 1` → ưu tiên action của **PLAN**, fallback slot; `= 0` → **chỉ** dùng action của SLOT. "
     "⚠ `b_plan_slot` **không có** cột `using_action_slot_*`.\n"
     "Spec **KHÔNG mô tả** trường hợp đổi lịch giữa 2 slot có cấu hình ưu tiên khác nhau.",
     "Corpus ghi nhận đây là **bug đã tự phát hiện nhưng để lại sửa sau** ('sẽ sửa sau, check bug replace "
     "data của KH trước'). Không rõ đã fix chưa. TC hiện tại nếu chạy sẽ FAIL. Người dùng cuối nhận nhầm "
     "nội dung tin nhắn của gói/khung giờ mình KHÔNG đặt.",
     "『アクション設定』TC「Đổi lịch giữa slot CÓ plan ↔ slot KHÔNG plan (ưu tiên action plan) — action gửi "
     "phải theo slot ĐÍCH」· 『LINE user — đổi lịch』TC「Sau khi đổi lịch, ACTION gửi cho user lấy theo "
     "slot ĐÍCH (B)」",
     "",
     "① Hỏi Dev bug tự detect này đã fix chưa (tìm ticket tương ứng).\n"
     "② Nếu CHƯA fix → chạy TC, xác nhận FAIL, **mở ticket bug chính thức**.\n"
     "③ Nếu ĐÃ fix → xác nhận expected và gỡ cảnh báo dự kiến FAIL.\n"
     "④ Bổ sung BR-17 mô tả nhánh đổi giữa 2 slot khác cấu hình ưu tiên."],

    ["MT-03", "CAO", W,
     "Tên cột `is_hide_remain` ngược nghĩa + giá trị MẶC ĐỊNH của 3 toggle 予約枠表示設定",
     "「Event booking 1.0」r121-r122:「set **có hiển thị** => Check màn hình phía line user: có hiện số "
     "remain / set không hiển thị => không hiện số remain」. Corpus chỉ nói theo NHÃN UI, "
     "**không nhắc tới giá trị DB**.\n"
     "Corpus KHÔNG có TC nào ghi lại giá trị mặc định của 3 toggle khi tạo event mới.",
     "`feature-spec.md:736` BR-23: 3 cờ ở `b_setting_basic_event` đều theo chiều `1` = 表示 / `0` = 非表示; "
     "⚠ **Tên cột `is_hide_remain` NGƯỢC NGHĨA — `1` KHÔNG phải 'ẩn' mà là 表示 (HIỆN)**.\n"
     "`feature-spec.md:1155` G-05: giá trị **default** của 3 toggle 「残数/受付終了/満席」 **CHƯA xác định** "
     "(a11y tree chỉ hiện text ON rời rạc).",
     "Tên cột ngược nghĩa là bẫy kinh điển: dev đọc schema hiểu ngược sẽ đảo hành vi mà test theo nhãn UI "
     "vẫn PASS. Đồng thời giá trị mặc định chưa xác định khiến TC 'tạo event mới' không có expected chuẩn — "
     "mỗi người test ra một kết quả.",
     "『Tab 詳細設定』TC「Toggle 予約枠の残数 — bật/tắt điều khiển việc hiện số 残数 phía LINE user」và "
     "TC「Xác nhận giá trị MẶC ĐỊNH của 3 toggle 予約枠表示設定 khi tạo event mới」",
     "",
     "① Chạy TC xác nhận default → ghi lại giá trị UI + giá trị DB của cả 3 cột.\n"
     "② Chốt: `is_hide_remain = 1` ứng với UI 表示 hay 非表示.\n"
     "③ Cập nhật spec G-05 (đóng gap) và ghi rõ mapping UI ↔ DB vào Field Matrix #23/#24.\n"
     "④ Đề xuất Dev đổi tên cột hoặc thêm COMMENT schema."],

    ["MT-04", "CAO", W,
     "Xóa event / 開催日 / slot / コース KHÔNG có transaction — có cần TC kiểm bản ghi mồ côi không?",
     "「Task nhỏ + fix bug KH」r5-r12 và「Event booking 1.0」r20, r112 mô tả xóa cascade là hành vi ĐÚNG "
     "(xóa slot → xóa plan + booking; xóa event → xóa cả remind `user_event`).\n"
     "Corpus **KHÔNG có TC nào** kiểm bản ghi mồ côi khi thao tác xóa bị lỗi giữa chừng.",
     "`feature-spec.md:1186` TD-01 (🔴 mức CAO nhất): **mọi** `DB::beginTransaction()`/`commit()`/`rollback()` "
     "trong 2 controller chính đều bị **COMMENT OUT** (liệt kê 12+ vị trí), cộng hưởng với xóa cascade thủ công "
     "bằng PHP (6+ bảng) và **KHÔNG có FOREIGN KEY constraint**. Rủi ro: `b_plan_slot`, `b_user_booking`, "
     "`t_actions`, `t_actions_detail` **mồ côi**; `update_to` trỏ vào bản ghi không tồn tại; "
     "`use_people`/`remain_limit` **drift**.",
     "TCs coi cascade là chuyện hiển nhiên; spec khẳng định cơ chế cascade này chạy KHÔNG có bảo vệ nào. "
     "Không phải TCs sai — mà là TCs **thiếu hẳn một chiều kiểm tra** mà spec chỉ ra là rủi ro dữ liệu cao "
     "nhất của tính năng.",
     "『Folder event』TC「Xóa folder có event → kiểm bản ghi mồ côi ở 6 bảng con」· 『Copy & xóa event』"
     "TC「Xóa 1 event → xóa toàn bộ dữ liệu liên quan gồm cả remind user_event」",
     "",
     "① Quyết định có đưa TC kiểm mồ côi vào bộ chạy chính thức không (cần quyền query DB).\n"
     "② Nếu có: thống nhất bộ query chuẩn cho 6 bảng con để member copy dùng.\n"
     "③ Đề xuất Dev bọc transaction cho các thao tác xóa cascade (khuyến nghị #3 của spec §11.4)."],

    ["MT-05", "CAO", W,
     "Công thức tính 定員 tổng của 1 slot khi vừa có 定員 slot vừa có コース dùng chung 定員",
     "「Sheet4」r3-r8 (Bug #24441, 10/2023 — tab BỊ ẨN, noise filter loại khỏi listing):\n"
     "- Slot 無制限 + có ≥1 plan dùng chung 定員 slot → 定員 slot = **無制限 (-)**\n"
     "- Slot 無制限 + không plan nào dùng chung → 定員 = **tổng 定員 all plan**\n"
     "- Slot CÓ 定員 + có ≥1 plan dùng chung → 定員 = **定員 slot + tổng 定員 các plan KHÔNG dùng chung**\n"
     "- Slot CÓ 定員 + không plan nào dùng chung → 定員 = **tổng 定員 all plan**",
     "`feature-spec.md:648` Field Matrix #7:「定員」(tổng event) = *Aggregated*: "
     "`SUM(b_slot.number_people)` **|** `SUM(b_plan_slot.limit)` — chỉ mô tả 2 nhánh đơn giản.\n"
     "`feature-spec.md:722` BR-07 nói `plan.using_max_slot = 1` → plan dùng chung 定員 slot, nhưng "
     "**KHÔNG có công thức lai** như corpus mô tả.",
     "Corpus có công thức 4 nhánh chi tiết (trong đó nhánh lai 定員 slot + tổng plan riêng là phản trực giác), "
     "spec chỉ có 2 nhánh. Nếu spec đúng → TC sai và ngược lại; cột 定員 ở màn list là số Leader/KH nhìn để "
     "biết còn nhận được bao nhiêu người. TC gốc đã **> 2 năm tuổi** (10/2023).",
     "『Màn list event』TC「Cột 定員 — slot 定員 = 無制限 và có ≥1 plan dùng chung」và TC「Cột 定員 — slot CÓ "
     "set 定員 + có ≥1 plan dùng chung 定員 slot」",
     "",
     "① Chạy lại 4 nhánh trên môi trường hiện tại (TC > 2 năm, CẦN VERIFY LẠI).\n"
     "② Chốt công thức đúng.\n"
     "③ Cập nhật `feature-spec.md` Field Matrix #7 + BR-07 với đủ 4 nhánh.\n"
     "④ Xác nhận tab「Sheet4」có thuộc bộ v1 hay v2 (xem MT-33)."],

    ["MT-06", "CAO", W,
     "IDOR ở chức năng hoàn tiền — có đưa TC bảo mật vào bộ chạy không, và chạy ở môi trường nào?",
     "「Task nhỏ + fix bug KH」r307 (TC-NEW-07 do AI đề xuất trong bộ human, 07/2026) và r312 (RV-07) đã nêu "
     "yêu cầu kiểm WHERE scope + phân quyền hoàn tiền, nhưng **chưa có kết quả thực thi**.\n"
     "Corpus của con người (r296-r301) chỉ kiểm luồng hoàn tiền thành công, **không kiểm cách ly bot**.",
     "`feature-spec.md:1188` TD-02 (🔴 BẢO MẬT): **IDOR ở `refundMoneyBookingEvent`** — lấy `bot_id` "
     "**TỪ REQUEST** thay vì `getBotId()` (`BookingEventDayManagementController.php:1797`), nhưng dòng `:1850` "
     "lại dùng `getBotId()` để lấy khoá UnivaPay → **không nhất quán**. Rủi ro: **hoàn tiền booking của bot "
     "khác** bằng cách sửa `bot_id` trong request.",
     "Spec khẳng định lỗ hổng tồn tại ở tầng code; TCs chưa từng kiểm. Đây là thao tác TIỀN THẬT trên "
     "production — nếu lỗ hổng có thật thì hậu quả là hoàn tiền nhầm khách của bot khác. Cần Leader quyết vì "
     "test bảo hổng này đụng tới dữ liệu tiền.",
     "『Hoàn tiền 返金』TC「Hoàn tiền booking của bot A KHÔNG được đụng booking trùng của bot B」",
     "",
     "① Quyết định có chạy TC IDOR không, và chạy ở STAGING hay PRODUCTION.\n"
     "② Nếu tái hiện được → **mở ticket bảo mật mức cao NGAY**, không chờ hết đợt test.\n"
     "③ Đề xuất Dev sửa `:1797` dùng `getBotId()` (khuyến nghị #2 của spec §11.4)."],

    ["MT-07", "CAO", W,
     "Hoàn tiền KHÔNG idempotent — expected khi bấm hoàn tiền 2 lần là gì?",
     "「Task nhỏ + fix bug KH」r304 (TC-NEW-03) và r306 (TC-NEW-06) do AI đề xuất, expected:「GUI báo lỗi đúng "
     "nguyên nhân ('giao dịch đã được hoàn tiền'); Stripe **không phát sinh refund thứ 2**」. "
     "**Chưa có kết quả thực thi**.\n"
     "Corpus của con người không có TC double refund.",
     "`feature-spec.md:1200` TD-10 (🟠 TRUNG BÌNH): **Refund KHÔNG idempotent** — không kiểm tra "
     "`status_payment` hiện tại trước khi gọi API cổng (`BookingEventDayManagementController.php:1794-1902`). "
     "Rủi ro: gọi 2 lần (double-click / retry) → **hoàn tiền 2 lần** ở phía cổng thanh toán.",
     "TC đề xuất kỳ vọng hệ thống chặn; spec nói hệ thống KHÔNG chặn. TC sẽ FAIL. Cần Leader chốt expected "
     "trước khi member chạy, nếu không member sẽ ghi 'Không đạt' mà không biết nên raise bug hay chấp nhận.",
     "『Hoàn tiền 返金』TC「Hoàn tiền LẠI booking đã hoàn → báo lỗi đúng, Stripe không phát sinh refund thứ 2」",
     "",
     "① Chốt expected: hệ thống PHẢI chặn (→ TC FAIL thì raise bug) hay tạm chấp nhận (→ đổi expected).\n"
     "② Nếu chốt phải chặn: xác nhận chặn ở tầng nào (disable nút / kiểm `status_payment` server-side).\n"
     "③ Đề xuất Dev thêm idempotency check (khuyến nghị #5 của spec §11.4)."],

    ["MT-08", "CAO", W,
     "Xóa event khi ĐÃ có booking thanh toán thành công — dữ liệu tiền xử lý ra sao?",
     "Corpus **KHÔNG có TC nào** về việc xóa event/slot/plan khi bên trong đã có booking đã thu tiền. "
     "「Task nhỏ」r5-r12 chỉ nói xóa theo `slot_id` 'nên ko cần check các loại status booking' — tức là "
     "**xóa bất kể trạng thái thanh toán**.",
     "`feature-spec.md:1186` TD-01: xóa cascade thủ công, không transaction, không FK.\n"
     "`feature-spec.md:1088` BR-21 mô tả hoàn tiền là thao tác riêng — spec **KHÔNG mô tả** ràng buộc "
     "'không được xóa booking đã thanh toán'.\n"
     "`feature-spec.md:1174` G-11: bảng `b_user_booking_history` không có trong DB dump → không chắc lịch sử "
     "có tồn tại sau khi booking bị xóa hay không.",
     "Nếu xóa event làm mất luôn booking đã thu tiền và lịch sử của nó, hệ thống mất dấu vết giao dịch trong "
     "khi tiền đã nằm ở Stripe/UnivaPay. Đây là rủi ro nghiệp vụ + đối soát, không chỉ là bug kỹ thuật.",
     "『Copy & xóa event』TC「Xóa event đang có booking ĐÃ thanh toán → xác nhận hành vi với dữ liệu tiền」",
     "",
     "① Chạy TC ghi nhận hành vi thật trên STAGING trước.\n"
     "② Chốt: có cần chặn xóa khi còn booking `status_payment = 1` chưa hoàn tiền không.\n"
     "③ Nếu cần chặn → mở ticket cho Dev + bổ sung BR mới vào spec."],

    ["MT-09", "CAO", W,
     "Truy cập trái phép ở TẦNG API — staff không quyền và truy cập chéo bot (2 bug chưa fix)",
     "TCsLine_Improve chung / tab「Improve nhỏ」r320: 「Account staff không có quyền access màn hình」→ "
     "kết quả **NG**, ghi chú 「**Các màn booking không được phân quyền nhưng vẫn access được**」, "
     "Bug Tester **#33106**.\n"
     "Cùng tab r304 + khối r334: Bug Tester **#33107** 「Bot A đang access được link của bot B => Check lại "
     "cho all màn」— NG ở màn template/item; **danh sách kiểm r335-r349 KHÔNG có màn event booking**.\n"
     "Trong 11.3 TCsLine_EventBooking, **mọi dòng「Check account staff」đều để TRỐNG kết quả mong đợi** "
     "(1.0 r355, 2.0 r80, 3.0 r66, stripe r80, univapay r183, Task nhỏ r65).",
     "`feature-spec.md:1192` TD-03 (🔴 BẢO MẬT): nhóm route AJAX `/ajax` **chỉ có `check_login`** — "
     "KHÔNG có `basic_access`, KHÔNG có `is_expire` (`routes/web.php:2454`). Staff bị chặn ở trang HTML "
     "**vẫn gọi được trực tiếp toàn bộ API AJAX** (tạo/sửa/xoá event, slot, plan, refund…).\n"
     "`feature-spec.md:1158` G-08: **chưa xác định** menu 「イベント予約」 có nằm trong whitelist "
     "`getRouterBotInvite()` hay không.",
     "Corpus có bằng chứng NG từ 2 bug tester nhưng **không có TC hoàn chỉnh nào cho event booking**, còn spec "
     "chỉ ra nguyên nhân gốc ở tầng route. Đây là lỗ hổng cho phép staff bị thu quyền vẫn thao tác được toàn bộ "
     "tính năng, kể cả hoàn tiền.",
     "『Phân quyền & môi trường』TC「Account staff KHÔNG được cấp quyền → chặn ở CẢ giao diện lẫn URL / API trực "
     "tiếp」và TC「Cách ly dữ liệu giữa 2 bot」· 『Hoàn tiền 返金』TC「Phân quyền — account staff không được cấp "
     "quyền KHÔNG được hoàn tiền qua URL trực tiếp」· 『LINE user — mở link & entry』TC「Bot A không mở được link "
     "đặt chỗ của event thuộc bot B」",
     "",
     "① Hỏi Dev trạng thái bug #33106 và #33107 (đã fix chưa, có bao gồm màn event booking không).\n"
     "② Đóng GAP G-08: xác nhận menu イベント予約 có trong `getRouterBotInvite()` không.\n"
     "③ Chạy TC ở TẦNG API (không chỉ UI) theo ghi nhớ dự án về regression phân quyền.\n"
     "④ Nếu tái hiện → raise lại / cập nhật ticket cũ."],

    ["MT-10", "CAO", W,
     "Webhook UnivaPay không xác thực chữ ký — có test giả mạo webhook không?",
     "「Improve bill tiền univapay」r182:「Check setting **không Webhook ID**」— dòng chỉ có tiêu đề, "
     "**không có kết quả mong đợi**.\n"
     "Corpus **KHÔNG có TC nào** thử giả mạo webhook.",
     "`feature-spec.md:1190` TD-05 (🔴 BẢO MẬT): **Webhook UnivaPay KHÔNG xác thực chữ ký** — chỉ dựa vào "
     "`data.metadata.module` (`WebhookUnivapayControler.php:11-41`). Rủi ro: bên thứ ba có thể giả mạo webhook "
     "`charge_finished` → **đánh dấu booking đã thanh toán mà không trả tiền**.",
     "Toàn bộ cơ chế bill UnivaPay kiểu mới dựa trên callback; nếu callback không được xác thực thì mọi TC "
     "'callback success → status_payment = 1' đều đang test một cơ chế có thể bị giả mạo. Corpus không có "
     "chiều kiểm này.",
     "『Thanh toán — UnivaPay』TC「Webhook UnivaPay giả mạo → hệ thống KHÔNG được đánh dấu booking đã thanh "
     "toán」và TC「Bot chưa cấu hình Webhook ID của UnivaPay」",
     "",
     "① Quyết định có chạy TC giả mạo webhook không và chạy ở môi trường nào (KHÔNG chạy trên production).\n"
     "② Bổ sung expected cho r182 (hành vi khi thiếu Webhook ID).\n"
     "③ Đề xuất Dev thêm xác thực chữ ký webhook (khuyến nghị #2 của spec §11.4)."],

    ["MT-11", "CAO", W,
     "Đổi lịch A → B: quy tắc CHO PHÉP đổi lấy theo slot NGUỒN hay slot ĐÍCH?",
     "「Event booking 2.0」r51-r54 (SpecChange 05/2023) khẳng định rõ 4 tổ hợp:\n"
     "- A cho phép đổi + B cho phép → **cho đổi**\n- A cho phép + B KHÔNG cho phép → **vẫn cho đổi**\n"
     "- A KHÔNG cho phép + B cho phép → **không cho đổi**\n- A KHÔNG + B KHÔNG → **không cho đổi**\n"
     "→ Chỉ setting của slot **NGUỒN** quyết định.",
     "`feature-spec.md:730` BR-14 chỉ nói LINE user huỷ/đổi được khi `now() <= date_deadline_change_cancel` "
     "(hoặc `setting_deadline = 0`).\n"
     "`feature-spec.md:729` Field Matrix #39 mô tả `approval_system_change_request` với `2` = 不可 nhưng "
     "**KHÔNG nói theo slot nguồn hay slot đích**.\n"
     "`feature-spec.md:733` BR-16 mô tả cơ chế cặp booking, cũng không nói.",
     "Quy tắc 'theo slot nguồn' rất phản trực giác (user chọn slot đích 不可 vẫn đổi được vào đó). Spec không "
     "ghi → dev sửa code sau này rất dễ đổi thành 'theo slot đích' mà không ai phát hiện. Ảnh hưởng trực tiếp "
     "hành vi người dùng cuối.",
     "『LINE user — đổi lịch』TC「Đổi lịch A → B: quy tắc CHO PHÉP đổi lấy theo setting của slot NGUỒN (A)」",
     "",
     "① Chạy lại 4 tổ hợp trên môi trường hiện tại xác nhận quy tắc còn đúng (TC từ 05/2023).\n"
     "② Chốt quy tắc.\n"
     "③ Bổ sung vào `feature-spec.md` BR-14/BR-16 hoặc tạo BR mới."],

    ["MT-12", "CAO", W,
     "Bill FAIL xử lý ra sao: XÓA booking hay đổi sang CANCEL? Và case đóng trình duyệt ở 3DS",
     "「Improve bill tiền stripe」r11, r14: bill fail → **XÓA booking** + hoàn bộ đếm.\n"
     "「Improve bill tiền univapay」r10, r13 (bill kiểu CŨ): bill fail → **XÓA booking**.\n"
     "「Improve bill tiền univapay」r60 (bill kiểu MỚI): callback fail → 「update thông tin booking như case "
     "bill lỗi phía trên nhưng **không xóa booking mà update status booking = cancel**」.\n"
     "「Improve bill tiền stripe」r15, r35 (3DS đóng trình duyệt): ô expected ghi「10/2025: Change spec: "
     "khi job quét sẽ **không tính là bill fail**: **xóa booking** … **không** send message」— "
     "**tự mâu thuẫn trong cùng 1 ô**.",
     "`feature-spec.md:1040-1077` §8.2 mô tả luồng thanh toán LINE User (`MobileEventBookingController@payment` "
     "`:706-1493`) nhưng **KHÔNG liệt kê rõ ma trận hành vi khi bill fail theo từng cơ chế** (Stripe / "
     "UnivaPay cũ / UnivaPay callback).\n"
     "`feature-spec.md:559` §3.2 liệt kê enum `status_webhook` nhưng không gắn với hành vi xóa/cancel.",
     "Ba cơ chế thanh toán cho ba hành vi khác nhau khi thất bại (xóa / cancel / xóa-nhưng-không-báo). Member "
     "chạy TC rất dễ áp nhầm expected của cơ chế này sang cơ chế kia. Riêng ô r15 tự mâu thuẫn nên không có "
     "expected dùng được.",
     "『Thanh toán — Stripe』TC「Bill Stripe THẤT BẠI → XÓA booking」và TC「3DS — user ĐÓNG TRÌNH DUYỆT ở modal "
     "xác thực」· 『Thanh toán — UnivaPay』TC「Quá 5 phút chưa có callback → status_webhook = 4」",
     "",
     "① Lập bảng ma trận chuẩn: (cơ chế × thời điểm × kết quả) → hành vi với booking / bộ đếm / tin nhắn.\n"
     "② Chốt riêng case 3DS đóng trình duyệt: xóa booking nhưng KHÔNG gửi tin fail — đúng hay sai.\n"
     "③ Bổ sung ma trận vào `feature-spec.md` §8.2.\n"
     "④ Sửa lại ô expected r15/r35 của sheet gốc cho hết mâu thuẫn."],

    ["MT-13", "CAO", W,
     "UnivaPay callback success trong 2 phút — CÓ hay KHÔNG gửi tin 決済が完了しました。?",
     "「Improve bill tiền univapay」r52 (bill kiểu mới): ô expected ghi cả 2 vế —\n"
     "「- booking success back về màn chat\n- send message báo bill success cho user 決済が完了しました。\n"
     "**=> sửa lại case này không send message báo bill success nữa**」.\n"
     "Trong khi r12 (bill kiểu cũ, qua job) và r30/r77 (job quét kết quả) đều ghi **CÓ** gửi "
     "「決済が完了しました。」.",
     "`feature-spec.md:1040-1077` §8.2 **KHÔNG liệt kê** danh sách tin nhắn hệ thống gửi cho LINE user theo "
     "từng nhánh thanh toán. Không có mục nào của spec nhắc tới nội dung 「決済が完了しました。」.",
     "Người dùng cuối có nhận thêm 1 tin LINE hay không là hành vi nhìn thấy được, và còn ảnh hưởng quota tin "
     "nhắn của bot. Ô expected ghi cả hành vi cũ lẫn hướng sửa nên không dùng làm chuẩn được.",
     "『Thanh toán — UnivaPay』TC「Bill kiểu MỚI — callback success trong 2 phút → đóng màn, KHÔNG gửi tin báo "
     "thành công」",
     "",
     "① Xác nhận với Dev bản đã triển khai: callback nhanh có gửi tin không.\n"
     "② Chốt và ghi rõ khác biệt giữa nhánh callback nhanh và nhánh qua job.\n"
     "③ Bổ sung bảng tin nhắn hệ thống vào `feature-spec.md` §8.2.\n"
     "④ Dọn ô expected r52 của sheet gốc."],

    ["MT-14", "TRUNG BÌNH", W,
     "「1回の予約上限」có bị trần 127 do kiểu dữ liệu tinyint không?",
     "「Event booking 1.0」r114-r115 chỉ test giá trị nhỏ (default 1, set 3, khoảng 2〜4). "
     "Corpus **KHÔNG có TC biên** nào cho ô này.",
     "`feature-spec.md:666` Field Matrix #19: `b_setting_basic_event.limit_people`/`.min_people` — "
     "⚠ `tinyint` → **trần 127**.\n"
     "`feature-spec.md:1209` TD-18: **Không đặt được「1回の予約上限」> 127**.",
     "Spec chỉ ra giới hạn kỹ thuật cứng mà UI không cảnh báo. Sự kiện đông người (>127 chỗ/lần đặt) sẽ bị "
     "chặn âm thầm hoặc lưu sai giá trị do tràn kiểu. TCs chưa từng chạm ngưỡng này.",
     "『Tab 詳細設定』TC「1回の予約上限 biên trần kiểu dữ liệu — nhập 127 / 128 / 200」",
     "",
     "① Chạy TC biên 127/128/200 ghi lại giá trị DB thật.\n"
     "② Nếu tràn/cắt âm thầm → mở ticket yêu cầu validate rõ ràng hoặc đổi kiểu cột.\n"
     "③ Ghi giới hạn này vào tài liệu hướng dẫn KH."],

    ["MT-15", "CAO", W,
     "Thu tiền tính theo THỜI ĐIỂM tạo booking hay theo trạng thái liên kết cổng lúc duyệt?",
     "「improve bill tiền 3D secure」r67-r76 (Stripe) và r79-r88 (UnivaPay) mô tả quy tắc:\n"
     "- Chưa liên kết lúc booking → liên kết sau → duyệt: **KHÔNG thanh toán** ('do tính theo thời điểm "
     "booking - ko có thông tin card')\n"
     "- Đã liên kết lúc booking → hủy liên kết → duyệt: **VẪN thanh toán** ('do tính theo thời điểm booking "
     "- có thông tin card')\n"
     "r98-r99: event chọn cổng khác cổng bot đang liên kết → **booking success nhưng KHÔNG bill tiền**.",
     "`feature-spec.md:1028` §8.1 mô tả cấu hình thanh toán trên `b_event_detail`; "
     "`feature-spec.md:70` §1.4 nói dropdown 「利用する決済システム」 không hiện option nếu chưa liên kết cổng.\n"
     "Spec **KHÔNG mô tả** quy tắc 'tính theo thời điểm booking', cũng KHÔNG mô tả hành vi khi event trỏ tới "
     "cổng mà bot đã hủy liên kết.",
     "Quy tắc 'thời điểm booking' quyết định có thu được tiền hay không — đây là doanh thu. Trường hợp "
     "'booking success mà không bill tiền' đặc biệt nguy hiểm: KH nhận đặt chỗ nhưng không thu được tiền, "
     "và không có cảnh báo nào.",
     "『Thanh toán — 3D Secure』TC「Tổ hợp LIÊN KẾT / HỦY LIÊN KẾT cổng thanh toán giữa chừng — Stripe」và "
     "「— UnivaPay」· TC「Event chọn cổng KHÁC với cổng bot đang liên kết」",
     "",
     "① Chạy lại ma trận 7 kịch bản × 2 cổng trên môi trường hiện tại (TC từ 03/2024).\n"
     "② Chốt quy tắc và chốt hành vi mong muốn cho case 'booking success mà không bill tiền'.\n"
     "③ Bổ sung vào `feature-spec.md` §8.1/§8.2.\n"
     "④ Cân nhắc đề xuất cảnh báo cho admin khi event trỏ tới cổng chưa/không còn liên kết."],

    ["MT-16", "TRUNG BÌNH", W,
     "Ràng buộc độ dài / bắt buộc CHỈ có ở client — có đưa TC gọi thẳng API vào bộ chạy không?",
     "Toàn bộ 11.3 TCsLine_EventBooking **KHÔNG có TC nào** thao tác ở tầng API. Mọi TC validate đều qua giao "
     "diện (1.0 r25「check validate」, r34, r74, r198-r248…). Corpus cũng **không test biên** cho "
     "「イベント名（管理用）」(20), 「タイトル/説明」(50), 「表示項目名」(30), 「予約単位」(3), 「ボタン」(10).",
     "`feature-spec.md:1203` TD-11 (🟠): **Hầu hết endpoint save KHÔNG validate server-side** — chỉ EP-37 có. "
     "`validateFormSettingEvent()` (`:1667-1716`) tồn tại nhưng **KHÔNG BAO GIỜ được gọi** (dead code). "
     "Liệt kê 9 hàm save không validate.\n"
     "Field Matrix ghi rõ nhiều ràng buộc là **client-only** (#1 ≤20 client-only, #3 ≤50 client, #11 ≤10, "
     "#22 ≤3, #58 利用規約 validate client — không lưu DB).",
     "Nếu ràng buộc chỉ ở client thì test qua UI luôn PASS trong khi API vẫn ghi được dữ liệu rác vào DB "
     "(title > 255, quantity âm, price < 50). Bộ TC hiện tại không phát hiện được lớp rủi ro này.",
     "『Tạo & sửa event — khung』TC「「イベント名（管理用）」biên 20 ký tự」· 『Form 予約時入力項目』TC「入力フォーマット "
     "chặn đúng dữ liệu sai」· 『Tab 決済設定』TC「利用する決済システム KHÔNG đổi được sau khi đã lưu」",
     "",
     "① Chốt có đưa TC gọi thẳng API vào bộ chạy không (cần công cụ + hướng dẫn cho member).\n"
     "② Nếu có: chọn 3-5 endpoint rủi ro nhất (save event, save slot, save plan, save booking, refund).\n"
     "③ Đề xuất Dev bật lại `validateFormSettingEvent()` (khuyến nghị #5 của spec §11.4)."],

    ["MT-17", "TRUNG BÌNH", W,
     "Ranh giới ngày giờ: 'hôm nay' có chọn được làm 開催日 không, và mốc đúng 締切 có còn đặt được không?",
     "「Event booking 1.0」r27 chỉ nói「disable các ngày trong **quá khứ**」— không nói rõ hôm nay.\n"
     "r184-r185 mô tả hành vi với slot 'đã hết hạn' nhưng **không có TC nào chạy đúng mốc 締切**.",
     "`feature-spec.md:727` BR-13: `date_deadline = date_start − duration_deadline` (mốc suy diễn).\n"
     "`feature-spec.md:730` BR-14: LINE user huỷ được khi `now() <= date_deadline_change_cancel + "
     "time_deadline_change_cancel` — dùng `<=` (bao gồm mốc).\n"
     "Spec **KHÔNG nói** ranh giới của 締切 đặt chỗ (`date_deadline`) là `<` hay `<=`, cũng không nói 'hôm nay' "
     "có chọn được không.",
     "Ranh giới ngày giờ là nhóm bug kinh điển của tính năng đặt lịch (FUNC-DATE-001 mức Cao). Sai 1 phút ở "
     "mốc 締切 là user đặt được chỗ đã đóng, hoặc bị chặn oan.",
     "『Tab 開催日程 — ngày tổ chức』TC「Popup chọn ngày disable toàn bộ ngày trong QUÁ KHỨ」· 『LINE user — chọn "
     "slot & plan』TC「Trước / đúng / sau 締切日時 của slot」",
     "",
     "① Chạy TC 3 mốc (trước / đúng / sau) cho cả 締切 đặt chỗ, hạn đổi, hạn hủy.\n"
     "② Chốt quy ước `<` hay `<=` cho từng mốc.\n"
     "③ Bổ sung vào `feature-spec.md` BR-13/BR-14 và ghi rõ hành vi với ngày 'hôm nay'."],

    ["MT-18", "TRUNG BÌNH", W,
     "Phân biệt「báo lỗi」và「không cho chọn」— nội dung message lỗi cụ thể là gì?",
     "「SpecChange #26808」(14/10/2024) dùng **2 kết quả khác nhau** xuyên suốt ma trận: 「báo lỗi」(r8, r10, "
     "r20, r32, r55, r57, r61…) và 「không cho chọn」(r12, r19, r22, r30, r56, r63…). "
     "**Không dòng nào ghi nội dung message lỗi**.\n"
     "「Event booking 1.0」r191 cũng chỉ ghi「Báo lỗi không cho book」.\n"
     "「Khung giờ 予約枠」: spec ghi 2 message khác nhau cho case 定員 = 0.",
     "`feature-spec.md:669` Field Matrix #34 ghi 2 message cho 定員: 「定員は0以上入力してください。」 **và** "
     "「定員には１以上入力してください」(khi `quantity == 0`).\n"
     "Spec **KHÔNG có** message nào cho case user đặt vượt 残数 hay chọn slot/コース đã đầy.",
     "Hai kết quả này khác nhau về bản chất (chặn từ UI vs submit rồi báo lỗi) nhưng không ai ghi lại text "
     "thật. Member chạy TC sẽ tự diễn giải → kết quả test không so sánh được giữa các đợt. Spec lại có 2 "
     "message chồng nhau cho cùng 1 ô nhập.",
     "『LINE user — đặt chỗ & giới hạn số lần』toàn bộ 7 TC ma trận SpecChange #26808 · 『Khung giờ 予約枠』"
     "TC「定員 slot — để trống = 無制限; nhập 0 và nhập 1」",
     "",
     "① Chạy 1 vòng ma trận, **chụp lại text thật** của từng message.\n"
     "② Lập bảng tra cứu message (giống tab「Message error」của FA-011 Form).\n"
     "③ Chốt điều kiện nào ra「báo lỗi」, điều kiện nào ra「không cho chọn」.\n"
     "④ Cập nhật spec Field Matrix #34 cho hết chồng chéo message."],

    ["MT-19", "THẤP", W,
     "Giá tối thiểu của コース là > 50 円 hay ≥ 50 円?",
     "「Event booking 1.0」r74:「Default là không nhập (để blank), **validate nhập >50 yên**」— dùng dấu "
     "**lớn hơn**.",
     "`feature-spec.md:674` Field Matrix #45:「料金」→ `b_plan_slot.price`, validate "
     "「料金は**50円以上**入力してください。」— tức **≥ 50**.",
     "Lệch đúng 1 giá trị biên (50 円). Nếu chốt sai, TC biên sẽ báo kết quả ngược. Mức thấp vì ít khả năng "
     "KH đặt giá đúng 50 円, nhưng vẫn phải chốt để TC biên có expected đúng.",
     "『Gói コース (plan)』TC「料金 コース — mặc định để trống; biên 50 円 (49 lỗi / 50 OK)」",
     "",
     "① Chạy TC nhập đúng 50 → ghi kết quả thật.\n"
     "② Chốt và sửa 1 trong 2 nguồn cho khớp."],

    ["MT-20", "TRUNG BÌNH", W,
     "Khi TẮT 決済 thì có xóa được 2 item mặc định お名前 / メールアドレス không?",
     "Corpus **KHÔNG có TC nào** về việc xóa 2 item mặc định. "
     "「Event booking 1.0」r136 chỉ nói「Tạo default 2 infor này (tương tự bên quản lý sản phẩm)」.",
     "`feature-spec.md:664` Field Matrix #16 + `feature-spec.md:731` BR-19: mỗi event mới luôn có 2 field bắt "
     "buộc 「お名前」 (`friend_info_id = -1`) và 「メールアドレス」 (`friend_info_id = -3`), `is_default = 1`. "
     "「Khi bật thanh toán → **không xoá được** (cổng TT yêu cầu)」.\n"
     "Spec **KHÔNG nói** hành vi khi 決済 TẮT.",
     "Spec chỉ ràng buộc chiều 'bật 決済'. Nếu tắt 決済 mà xóa được 2 item này rồi bật lại 決済 thì event rơi "
     "vào trạng thái không hợp lệ với cổng thanh toán — không rõ hệ thống có chặn hay không.",
     "『Form 予約時入力項目』TC「Bật 決済 → KHÔNG xóa được 2 item mặc định お名前 / メールアドレス」",
     "",
     "① Chạy TC ghi lại hành vi thật ở cả 2 chiều (決済 bật / tắt).\n"
     "② Chốt: có cho xóa khi tắt 決済 không; nếu cho thì khi bật lại 決済 xử lý thế nào.\n"
     "③ Bổ sung BR-19 mô tả đủ 2 chiều."],

    ["MT-21", "TRUNG BÌNH", W,
     "Xóa / sửa item form SAU KHI đã có booking — đáp án cũ hiển thị ra sao?",
     "Corpus **KHÔNG có TC nào** cho tình huống này. "
     "「Event booking 3.0」r15-r17 chỉ kiểm cột CSV theo setting mới nhất, không kiểm dữ liệu booking cũ.",
     "`feature-spec.md:679` Field Matrix #51:「予約時入力事項」→ `b_user_booking.detail_info_user` "
     "(**JSON inline**), 🔑 **KHÔNG có bảng con đáp án** — cấu trúc `[{id, title, type, value}]` với "
     "`id` = `b_info_setting.id`.\n"
     "Spec **KHÔNG mô tả** hành vi khi `b_info_setting` bị xóa mà đáp án cũ vẫn trỏ `id` đó.",
     "Vì đáp án lưu inline kèm `id` trỏ tới bảng setting, xóa setting sẽ tạo tham chiếu treo. Không rõ màn "
     "detail booking và file export CSV xử lý thế nào — có thể mất dữ liệu đáp án của khách đã đặt.",
     "『Form 予約時入力項目』TC「Xóa / sửa item form SAU KHI đã có booking → đáp án cũ hiển thị thế nào」",
     "",
     "① Chạy TC ghi lại hành vi ở 3 điểm: màn detail booking · màn danh sách · file CSV.\n"
     "② Chốt hành vi mong muốn (giữ đáp án cũ theo `title` đã snapshot / ẩn đi).\n"
     "③ Bổ sung Field Matrix #51 mô tả vòng đời khi setting bị xóa."],

    ["MT-22", "TRUNG BÌNH", W,
     "Cơ chế phân biệt crawler vs user thật (UA detection) có phải chủ đích không?",
     "「Task nhỏ + fix bug KH」r239 (TC-NEW-06 do AI đề xuất trong khối Support #37932, 06/2026): "
     "expected 「User thật → vào trang đặt lịch đầy đủ (booking được). Crawler → nhận **preview_url** "
     "(trang meta OGP nhẹ), không phải trang booking」. **Chưa có kết quả thực thi**.\n"
     "Corpus của con người (r202-r233) chỉ kiểm kết quả preview trên 6 kênh, không nói về cơ chế.",
     "`feature-spec.md` §2.11 (SCR-EBD-20) mô tả trang LIFF là SPA 7 page state. "
     "Spec **KHÔNG nhắc tới** cơ chế nhận diện User-Agent hay endpoint `preview_url` riêng cho crawler.",
     "Nếu cơ chế UA detection có thật mà spec không ghi, thì mọi thay đổi ở trang LIFF sau này đều có nguy cơ "
     "phá vỡ preview OGP mà không ai biết. Ngược lại nếu không có cơ chế này thì TC-NEW-06 đang mô tả một "
     "thiết kế không tồn tại.",
     "『Preview & OGP』TC「Crawler và user thật nhận đúng trang khác nhau (UA detection)」",
     "",
     "① Hỏi Dev cách fix Support #37932 thực tế (UA detection hay sửa thẻ og:image).\n"
     "② Chốt expected của TC-NEW-06.\n"
     "③ Bổ sung mô tả cơ chế OGP vào `feature-spec.md` §2.11."],

    ["MT-23", "TRUNG BÌNH", W,
     "Account STAFF duyệt booking thì KHÔNG gửi action cho user — đúng hay là bug?",
     "「Task nhỏ + fix bug KH」r152:「Check account staff nhấn approve booking → Admin approve được booking "
     "success, **KHÔNG send action approve cho user**, tạo được lịch sử approve booking => hiện đúng tên user "
     "staff thao tác, Send được notify」.",
     "`feature-spec.md:44` §1.2 mô tả Staff dùng **cùng giao diện Admin**, chỉ giới hạn theo custom role "
     "(whitelist route).\n"
     "Spec **KHÔNG mô tả** bất kỳ khác biệt nào về việc gửi action giữa 主管理者 và staff.",
     "Từ góc nhìn khách hàng cuối, việc ai bấm nút duyệt không nên ảnh hưởng tới việc họ có nhận tin xác nhận "
     "hay không. Nếu đây là hành vi cố ý thì spec phải ghi; nếu là bug thì khách của bot dùng staff sẽ không "
     "bao giờ nhận được tin xác nhận đặt chỗ.",
     "『Admin — duyệt / từ chối booking』TC「Account STAFF duyệt booking → duyệt được, KHÔNG gửi action, lịch sử "
     "ghi đúng tên staff」",
     "",
     "① Chạy TC xác nhận hành vi còn đúng.\n"
     "② Hỏi Dev/PO: chủ đích hay bug.\n"
     "③ Nếu chủ đích → bổ sung vào spec §1.2; nếu bug → mở ticket."],

    ["MT-24", "TRUNG BÌNH", W,
     "Danh sách bạn bè ở màn đặt chỗ hộ bị hardcode limit 100",
     "Corpus **KHÔNG có TC nào** cho màn đặt chỗ hộ với bot nhiều bạn bè. "
     "「Event booking 1.0」r351「Admin booking」chỉ có tiêu đề, không có expected.",
     "`feature-spec.md:1205` TD-12: **`ajaxGetAllSlotEvent` hardcode `limit(100)`** cho danh sách bạn bè "
     "(`BookingEventDayManagementController.php:1664`). Rủi ro: bot có > 100 bạn bè → "
     "**không tìm được friend cần đặt hộ** trên SCR-EBD-13.\n"
     "`feature-spec.md:678` Field Matrix #50 cũng ghi ⚠ Danh sách **hardcode `limit(100)`**.",
     "Hầu hết bot thực tế có hơn 100 bạn bè, nghĩa là chức năng đặt chỗ hộ gần như không dùng được với phần "
     "lớn khách hàng. TCs chưa từng chạm tới giới hạn này nên bug im lặng suốt.",
     "『Admin — đặt chỗ hộ & sửa booking』TC「Danh sách friend ở màn đặt chỗ hộ khi bot có > 100 bạn bè」",
     "",
     "① Chạy TC trên bot có > 100 friend, ghi lại số friend thực tế tìm được.\n"
     "② Nếu không tìm được friend ngoài 100 đầu → mở ticket (nên có tìm kiếm server-side).\n"
     "③ Ghi giới hạn vào tài liệu vận hành cho tới khi fix."],

    ["MT-25", "THẤP", W,
     "Lịch sử friend info khi action của value select bị XÓA sau khi lịch sử đã tạo",
     "「Task nhỏ + fix bug KH」r291 (C-NEW-01 do AI đề xuất trong khối Bug Tester #38312, 06/2026) — "
     "**chưa có kết quả thực thi**, expected để mở.\n"
     "Corpus của con người (r243-r290) chỉ kiểm 2 trạng thái: value select **có** action → 「プレビュー」, "
     "**không có** action → 「設定なし」.",
     "`feature-spec.md:734` BR-20 mô tả mapping form → hồ sơ bạn bè và việc ghi `friend_info_history` "
     "(trigger `8001`).\n"
     "Spec **KHÔNG mô tả** cột action của lịch sử lưu snapshot nội dung action hay chỉ lưu tham chiếu.",
     "Nếu lịch sử chỉ lưu tham chiếu, xóa action sẽ làm lịch sử cũ mất preview hoặc lỗi. Nếu lưu snapshot thì "
     "preview vẫn hiện nội dung cũ. Hai hành vi này khác nhau về ý nghĩa audit.",
     "『Admin — đặt chỗ hộ & sửa booking』TC「Lịch sử friend info khi action của value select bị XÓA sau khi "
     "setting」",
     "",
     "① Chạy TC ghi lại hành vi thật.\n"
     "② Chốt hành vi mong muốn cho audit log.\n"
     "③ Bổ sung BR-20 mô tả cột action của `friend_info_history`."],

    ["MT-26", "TRUNG BÌNH", W,
     "Nút export CSV ở màn danh sách người tham gia có tồn tại trên UI không?",
     "「Event booking 3.0」r3-r14 (07/2023) kiểm export ở **3 chỗ**: màn danh sách chế độ lịch, chế độ danh "
     "sách, và màn 予約枠一覧 → detail booking của slot. Kết quả test ghi **OK** ở cả staging và step.",
     "`feature-spec.md:1156` G-06: nút **export CSV** ở SCR-EBD-10/11 — route tồn tại "
     "(**EP-17, EP-51, EP-52**) nhưng **không thấy nút trong Blade**. Cách xác minh đề xuất: grep "
     "`booking_all_slot.js` / `booking_slot.js`.",
     "TCs khẳng định đã test nút export và PASS; spec nói không tìm thấy nút trong Blade. Một trong hai sai, "
     "hoặc nút được render bằng JS nên spec-compiler không thấy. Ảnh hưởng: nếu nút thực sự không có thì 6 TC "
     "export trong kho này không chạy được.",
     "『Export CSV』toàn bộ 6 TC của nhóm",
     "",
     "① Mở màn thật xác nhận nút export có hiển thị không (chụp ảnh).\n"
     "② Nếu có → cập nhật spec G-06 (đóng gap), ghi rõ nút render bằng JS nào.\n"
     "③ Nếu không có → xác nhận với Dev route còn dùng không, và điều chỉnh nhóm TC Export CSV."],

    ["MT-27", "CAO", W,
     "Duyệt booking VƯỢT 定員 — chặn cứng hay hỏi xác nhận?",
     "Corpus **KHÔNG có TC nào** cho tình huống duyệt vượt 定員. "
     "Toàn bộ TC về 定員 trong「SpecChange #26808」đều đứng ở phía LINE user (đặt chỗ), không có phía admin.",
     "`feature-spec.md:724` BR-09: **Vượt 定員 khi duyệt** → **không chặn cứng**, trả `admin_confirm: 1` + "
     "「予約枠を超えています。承認しますか？」; gọi lại với `approveAny = true` sẽ bỏ qua "
     "(`BookingEventDayManagementController.php:3237-3255`).",
     "Spec mô tả một luồng xác nhận quan trọng mà bộ TCs chưa từng kiểm. Nếu luồng này lỗi, admin có thể vô "
     "tình duyệt vượt sức chứa sự kiện, hoặc bị chặn oan không duyệt được. Cũng là chỗ dễ sinh drift bộ đếm "
     "(`use_people` > `number_people`).",
     "『Đếm 定員 & use_people』TC「Duyệt booking VƯỢT 定員 → hệ thống hỏi xác nhận thay vì chặn cứng」",
     "",
     "① Chạy TC xác nhận popup và nội dung message.\n"
     "② Chốt: sau khi duyệt vượt thì `use_people` được phép lớn hơn `number_people` — có đúng ý đồ không.\n"
     "③ Kiểm tra ảnh hưởng tới hiển thị 残数 phía LINE user (số âm?)."],

    ["MT-28", "CAO", W,
     "Bộ đếm use_people / remain_limit — 2 cơ chế cập nhật khác nhau, job chỉ recover được 1 nửa",
     "「Task nhỏ + fix bug KH」r94-r105 (SpecImprove #33649, 03/2026) mô tả job recover đầy đủ quy tắc đếm cho "
     "`b_slot.use_people`.\n"
     "r106 ghi rõ: 「Job hiện tại **không recover số booking của plan**」(`b_plan_slot.remain_limit`).\n"
     "Corpus test từng thao tác riêng lẻ, **không có TC chuỗi thao tác hỗn hợp** để phát hiện drift.",
     "`feature-spec.md:1208` TD-17: **Không nhất quán cập nhật `use_people`/`remain_limit`** — "
     "`saveAdminBooking` dùng **increment** (`:2798-2804`); `saveActionBooking` **recompute** lại từ tổng "
     "`quantity` (`:3606-3637`). Kết hợp TD-01 (không transaction) → 2 cột này có nguy cơ **drift**.\n"
     "`feature-spec.md:722` BR-08 cũng cảnh báo tên cột `remain_limit` ngược nghĩa (thực chất là số ĐÃ DÙNG).",
     "Hai cơ chế cập nhật khác nhau trên cùng 1 cặp cột, không có transaction, và job recover chỉ sửa được "
     "`use_people` chứ không sửa `remain_limit`. Nghĩa là `remain_limit` sai thì sai vĩnh viễn — trực tiếp làm "
     "sai số 残数 mà khách nhìn thấy và sai điều kiện chặn đặt chỗ.",
     "『Đếm 定員 & use_people』TC「Bộ đếm KHÔNG bị drift sau chuỗi thao tác hỗn hợp」· 『Job nền』"
     "TC「Job recover count HIỆN KHÔNG recover số booking của コース (remain_limit)」",
     "",
     "① Chạy TC chuỗi hỗn hợp, đối chiếu bộ đếm với tổng `quantity` booking active.\n"
     "② Nếu phát hiện drift → mở ticket kèm bước tái hiện.\n"
     "③ Đề xuất mở rộng job recover sang `remain_limit`.\n"
     "④ Đề xuất thống nhất 1 cơ chế (recompute) cho cả 2 hàm."],

    ["MT-29", "CAO", W,
     "Người dùng BLOCK bot sau khi đăng ký remind — có bị loại khỏi danh sách gửi không?",
     "Corpus **KHÔNG có TC nào** về user block bot trong toàn bộ 11.3 TCsLine_EventBooking.",
     "`feature-spec.md:735` BR-22: chỉ đăng ký `user_event` khi `conversation.is_blocked = 0` — "
     "tức chỉ chặn ở **thời điểm đăng ký**.\n"
     "`feature-spec.md:1206` TD-14: **Query người nhận remind KHÔNG lọc `bot_id` và KHÔNG lọc user bị block** "
     "— `findAllLineUserByEventTime` chỉ JOIN `user_event.event_time_id` (`LineUserRepository.java:16-17`). "
     "Rủi ro: user **block bot SAU KHI** đăng ký remind vẫn nằm trong danh sách gửi → tốn quota LINE + lỗi API.",
     "Spec chỉ ra 2 vấn đề: (a) không lọc block ở thời điểm GỬI, (b) query **không lọc `bot_id`** — nghĩa là "
     "về lý thuyết có thể gửi nhầm cho user của bot khác nếu `event_time_id` trùng. Cả hai đều chưa có TC.",
     "『Remind リマインド』TC「User BLOCK bot → không đăng ký remind; block SAU KHI đăng ký thì hành vi lúc gửi "
     "ra sao」",
     "",
     "① Chạy TC block-sau-khi-đăng-ký, ghi lại log gọi LINE API.\n"
     "② Kiểm tra riêng vấn đề thiếu lọc `bot_id` (TD-14) — đây là rủi ro gửi nhầm bot.\n"
     "③ Nếu tái hiện → mở ticket; đề xuất thêm điều kiện lọc ở `LineUserRepository`."],

    ["MT-30", "CAO", W,
     "Toàn bộ TC remind chỉ verify tới BẢNG DB, chưa từng verify tin remind THẬT đến LINE",
     "Toàn bộ khối remind của corpus (「Task nhỏ + fix bug KH」r24-r64, 「Event booking 1.0」r281-r295) "
     "chỉ verify: 「thêm/xóa bản ghi bảng `user_event`」, 「insert bản ghi vào tbl `event_step_time`」, "
     "「Check trigger trên chat 1:1」.\n"
     "**KHÔNG có dòng nào** xác nhận LINE user nhận được tin remind thật đúng thời điểm.",
     "`feature-spec.md:1191` TD-06 (🔴 MẤT CHỨC NĂNG HOÀN TOÀN): `ENABLE_EVENT` (khởi động `BotTaskManager`) "
     "**KHÔNG còn xử lý** `event_step_time` (code đã comment out toàn bộ); chỉ `ENABLE_EVENT_REMIND` "
     "(`NewEventRemindTask`) mới xử lý. **Cả 2 flag đều mặc định `false`**. Nếu deploy chỉ bật `ENABLE_EVENT` "
     "→ **toàn bộ tin remind KHÔNG BAO GIỜ được gửi**; record kẹt vĩnh viễn ở `status = 0`.\n"
     "`feature-spec.md:1226` §11.4 khuyến nghị **#1**: kiểm tra ngay `config.properties` production.",
     "Bộ TCs hiện tại sẽ **PASS 100%** ngay cả khi remind không bao giờ được gửi, vì chỉ kiểm tới bảng trung "
     "gian. Vi phạm RULE-06 (phải đi tới output cuối trên LINE app). Đây là rủi ro bỏ lọt bug nghiêm trọng "
     "nhất của nhóm remind.",
     "『Remind リマインド』TC「Tin remind THẬT đến LINE đúng nội dung và đúng thời điểm」· 『Job nền』"
     "TC「Xác nhận cờ ENABLE_EVENT_REMIND trên PRODUCTION」",
     "",
     "① Kiểm tra NGAY `ENABLE_EVENT_REMIND` trên production (khuyến nghị #1 của spec).\n"
     "② Query `event_step_time` tìm bản ghi `status = 0` quá hạn — nếu có là bằng chứng remind đang chết.\n"
     "③ Bổ sung bước 'verify tin thật trên LINE' vào mọi TC remind của bộ human.\n"
     "④ Chốt môi trường chạy (PRODUCTION theo RULE-08)."],

    ["MT-31", "TRUNG BÌNH", W,
     "Toàn bộ TC「Check account staff」trong corpus event booking đều để TRỐNG kết quả mong đợi",
     "6 tab của 11.3 TCsLine_EventBooking đều có dòng cuối 「Check account staff」 nhưng "
     "**KHÔNG dòng nào có Expect Result**: Event booking 1.0 r355 · 2.0 r80 · 3.0 r66 · "
     "Improve bill tiền stripe r80 · Improve bill tiền univapay r183 · Task nhỏ r65.",
     "`feature-spec.md:1158` G-08: **Quyền Staff** — menu 「イベント予約」 có nằm trong whitelist "
     "`getRouterBotInvite()` không? **Chưa xác định**.\n"
     "`feature-spec.md:44` §1.2 chỉ nói Staff dùng cùng giao diện Admin, giới hạn theo custom role.",
     "Cả TCs lẫn spec đều để ngỏ chiều phân quyền staff. Nghĩa là chưa ai từng xác định staff được làm gì "
     "trên tính năng này — trong khi tính năng có thao tác tiền (hoàn tiền) và dữ liệu cá nhân (thông tin "
     "người tham gia).",
     "『Phân quyền & môi trường』TC「Account staff ĐƯỢC cấp quyền → thao tác đầy đủ」và TC「Account staff KHÔNG "
     "được cấp quyền → chặn ở CẢ giao diện lẫn URL / API trực tiếp」",
     "",
     "① Đóng GAP G-08: xác nhận menu イベント予約 trong whitelist `getRouterBotInvite()`.\n"
     "② Chốt ma trận quyền staff cho từng màn / từng thao tác (đặc biệt: hoàn tiền).\n"
     "③ Bổ sung expected cho 6 dòng「Check account staff」ở sheet gốc.\n"
     "④ Bổ sung ma trận quyền vào `feature-spec.md` §1.2."],

    ["MT-32", "CAO", W,
     "Bug #33106 (staff không quyền vẫn access được màn booking) — đã fix chưa và có bao gồm event booking?",
     "TCsLine_Improve chung / tab「Improve nhỏ」r320: kết quả **NG**, ghi chú "
     "「Các màn booking không được phân quyền nhưng vẫn access được」, Bug Tester **#33106**. "
     "Cột kết quả các đợt sau **không cập nhật lại dòng này**.",
     "`feature-spec.md:1192` TD-03 giải thích nguyên nhân gốc ở tầng route (`/ajax` chỉ có `check_login`) và "
     "đây là mục **khuyến nghị ưu tiên #2** của spec §11.4.",
     "Có bằng chứng NG nhưng không có bằng chứng đã fix. Theo RULE-11, chỉ ticket Closed/Resolved/Fix done/"
     "Released mới là bằng chứng hợp lệ — hiện chưa có. Không rõ nên viết TC với expected 'chặn được' "
     "(và chấp nhận FAIL) hay ghi nhận là hạn chế đã biết.",
     "『Phân quyền & môi trường』TC「Account staff KHÔNG được cấp quyền → chặn ở CẢ giao diện lẫn URL / API "
     "trực tiếp」",
     "",
     "① Tra trạng thái ticket #33106 trên Redmine.\n"
     "② Nếu chưa fix → giữ TC với ghi chú **dự kiến FAIL**, ưu tiên đưa vào đợt test gần nhất.\n"
     "③ Nếu đã fix → xác nhận phạm vi fix có bao gồm màn event booking và tầng `/ajax` không."],

    ["MT-33", "TRUNG BÌNH", W,
     "Tab「Improve event cũ 2023.03」và「Sheet4」thuộc bộ event v1 hay v2 — có nên nằm trong kho này?",
     "「Improve event cũ 2023.03」(03/2023, 40 dòng): toàn bộ TC ở dạng **chỉ có tiêu đề, không có kết quả "
     "mong đợi**, nội dung về đổi thông tin booking từ màn list người tham gia / màn list slot.\n"
     "「Sheet4」(Bug #24441, 10/2023, tab BỊ ẨN): công thức tính 定員 của 1 ngày — nội dung này lại **trùng "
     "chủ đề** với「SpecChange #26808」(10/2024) của bộ v2.",
     "`feature-spec.md:56` §1.3 Phạm vi — **Ngoài phạm vi**: bộ **booking_event v1** (`type_event_new = 0`) — "
     "hệ thống sự kiện cũ, **dùng chung bảng nhưng khác controller** (`BookingEventController` / "
     "`BookingEventManagementController`). **Là tính năng riêng**.\n"
     "Spec cũng loại 複数日イベント (code UI đã comment out → đã bị vô hiệu hoá).",
     "Nếu 2 tab này thuộc v1 thì chúng nằm ngoài phạm vi spec FA-021, và các TC lấy từ đó (đặc biệt công thức "
     "定員 ở MT-05) có thể đang mô tả hệ thống cũ. Nhưng「Sheet4」lại trùng chủ đề với SpecChange của v2 nên "
     "không loại được nếu chưa xác minh.",
     "『Màn list event』2 TC công thức 定員 lấy từ「Sheet4」· nội dung「Improve event cũ 2023.03」hiện **CHƯA** "
     "được đưa vào kho (xem cột excluded)",
     "",
     "① Xác minh 2 tab này test trên màn v1 hay v2 (đối chiếu URL trong TC hoặc hỏi tester cũ).\n"
     "② Nếu là v1 → tách sang kho riêng cho tính năng event v1, gỡ 2 TC 定員 khỏi kho này.\n"
     "③ Nếu là v2 → giữ nguyên và chạy verify lại (TC > 2 năm)."],

    ["MT-34", "THẤP", W,
     "Booking có `status = 0` (không có trong định nghĩa) — UI render thế nào?",
     "Corpus **KHÔNG có TC nào** cho `status = 0`. Mọi TC đều chỉ dùng 7 trạng thái 1〜7.",
     "`feature-spec.md:1169` G-12: `b_user_booking.status = 0` — **9 rows** trong dump, "
     "**không có trong `config/sns-line.php:398-407`** (chỉ định nghĩa 1–7). "
     "Ảnh hưởng: Trung bình — trạng thái không xác định, **UI có thể render sai**.\n"
     "`feature-spec.md:1210` TD-19 lặp lại cảnh báo này.",
     "Có dữ liệu thật ở trạng thái không được định nghĩa. Không ai biết những booking đó hiển thị ra sao ở "
     "màn admin, màn lịch sử của LINE user, và file CSV — cũng không biết chúng có được tính vào 定員 không.",
     "『Phân quyền & môi trường』TC「Booking có status = 0 (giá trị không có trong định nghĩa) — UI render ra sao」",
     "",
     "① Query production đếm lại số booking `status = 0` và xem chúng thuộc event nào.\n"
     "② Truy nguồn gốc: dữ liệu cũ migrate hay do luồng nào tạo ra.\n"
     "③ Chốt: bổ sung định nghĩa trạng thái hay dọn dữ liệu."],

    ["MT-35", "TRUNG BÌNH", W,
     "Cột 承認待ち ở màn list event đếm status = 3, hay đếm cả 6 và 7?",
     "「Event booking 1.0」r14:「Cột 承認待ち: Hiện tổng số booking ở trạng thái đang đợi approve "
     "(**không tính request change và request cancel**)」— tức chỉ `status = 3`.",
     "`feature-spec.md:721` BR-06: **Booking 'chờ xử lý'** 「リクエスト中」 (`countRequestSlot`/"
     "`countRequestPlan`) = `status ∈ {3, 6, 7}` (`BookingEventDayManagementController.php:727-733`, "
     "`:772-778`).\n"
     "`feature-spec.md:649` Field Matrix #6:「承認待ち」= *Aggregated*: COUNT WHERE `status ∈ {3,6,7}` → BR-06.",
     "TC nói **loại** 6 và 7; spec nói **bao gồm** 6 và 7. Một trong hai sai. Đây là con số Leader/KH nhìn ở "
     "màn danh sách để biết còn bao nhiêu yêu cầu cần xử lý — đếm sai thì bỏ sót yêu cầu của khách.\n"
     "Lưu ý: có thể `countRequestSlot` (dùng ở màn 予約枠一覧) và cột 承認待ち ở màn list event là **2 số "
     "khác nhau** — cần phân biệt trước khi kết luận.",
     "『Màn list event』TC「Cột 承認待ち chỉ đếm status = 3, KHÔNG đếm request change / request cancel」",
     "",
     "① Dựng dữ liệu có đủ 3 trạng thái 3/6/7 → đọc số ở **cả 2 màn** (list event và 予約枠一覧).\n"
     "② Xác định 2 màn dùng chung công thức hay khác nhau.\n"
     "③ Chốt và cập nhật `feature-spec.md` Field Matrix #6 / BR-06 cho đúng từng màn."],
]
