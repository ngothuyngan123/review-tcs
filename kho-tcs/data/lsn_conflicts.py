# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: 11.2 TCsLine_LessonCalendar (16 tab) + TCsLine_Improve chung →「add link salon và lesson」.
Nguồn spec: spec-features/admin/lesson-booking/ (feature-spec.md · web/logic-spec.md ·
            web/logic-spec-public.md · web/api-spec.md · job/job-spec.md · db/db-mapping.md ·
            ui/ui-spec.md · ui/ui-spec-liff.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    # ═══════════════════ Nhóm A — 2 tab Quản lý calendar (nền tảng, phải chốt TRƯỚC) ═════════════
    ["MT-11", "CAO", W,
     "🔴 CHỐT TRƯỚC — Tab「Quản lý calendar」hay「Quản lý calendar_new」là bản còn hiệu lực?",
     "File 11.2 có **2 tab song song** mô tả CÙNG màn quản lý đặt chỗ, KHÔNG bao trùm nhau:\n"
     "·「Quản lý calendar」(460 TC lá) — có 4 cột ticket MỚI NHẤT (#32704 11/2025, #29484 04/2025, "
     "#27978 01/2025), có khối『Test security』và『Feature #26528 hiển thị bill tiền』; "
     "57 TC CHỈ có ở tab này.\n"
     "·「Quản lý calendar_new」(478 TC lá) — mô tả GIAO DIỆN MỚI: màn tuần có 2 view コース別/一覧, "
     "modal edit slot, chức năng『xóa nhiều slot 一括削除』, hyperlink「期限なし」; 71 TC CHỈ có ở tab này; "
     "ticket mới nhất chỉ tới 2024.\n"
     "**12 điểm CÙNG đường dẫn nhưng kết quả mong đợi KHÁC NHAU**, gồm: format tiêu đề tuần · "
     "đơn vị đếm「他 xxx 件」(slot hay course) · droplist course ở modal add slot (default chọn "
     "course đầu tiên hay không chọn) · validate không chọn course · slot trùng khi chọn 1 ngày · "
     "hiển thị kỳ hạn 期限なし · import CSV ngày quá khứ.",
     "`ui/ui-spec.md:1264`: `booking_list_week.blade.php` có **2 view「コース別」/「一覧」**"
     " ⇒ khớp bản `_new`.\n"
     "`ui/ui-spec.md:529`: tab 受付枠一覧 có nút「選択した受付枠を一括削除」→ `deleteReceptionList()`"
     " ⇒ khớp bản `_new`.\n"
     "`feature-spec.md` BR-17: xóa hàng loạt kiểm `SUM(total_approve) > 0` ⇒ khớp bản `_new`.\n"
     "`feature-spec.md` BR-15: khung trùng thì **bỏ qua im lặng, không lỗi** ⇒ khớp bản `_new`.\n"
     "NHƯNG `web/api-spec.md` EP-51 (import CSV): **bỏ qua thời điểm đã qua (`isPast()`)** "
     "⇒ khớp bản CŨ, ngược bản `_new`.",
     "Không có tab nào là bản đúng hoàn toàn. Nếu member chỉ đọc 1 tab sẽ báo FAIL oan ở "
     "≥ 12 điểm. Kho TCs hiện GỘP CẢ 2 tab, mỗi điểm xung đột đều lấy theo bên khớp spec và "
     "ghi rõ ở `Ghi chú` — nhưng cần Leader chốt tab nào là nguồn sự thật để lần gom sau "
     "không phải suy luận lại.",
     "Toàn bộ nhóm [Calendar theo ngày] · [Calendar theo tuần] · [Calendar theo tháng] · "
     "[Calendar theo list] · [Modal danh sách booking] · [受付枠 — thêm khung giờ] · "
     "[受付枠 — xóa nhiều] · [受付枠 — CSV export/import]",
     "",
     "Chốt tab nguồn sự thật. Nếu `_new` là bản hiện hành: chuyển 4 khối chỉ-có-ở-tab-cũ "
     "(Test security · Support #32704 scroll · Feature #26528 · Bug #29484) sang tab `_new` "
     "rồi archive tab cũ. Nếu ngược lại: bổ sung 4 khối mới của `_new` vào tab cũ."],

    ["MT-15", "CAO", W,
     "Import CSV gặp dòng có thời điểm QUÁ KHỨ — bỏ qua im lặng hay báo lỗi?",
     "·「Quản lý calendar」r506-r507 (ghi rõ **spec update 8/10/2024**):"
     "「nếu gặp ngày quá khứ thì **bỏ qua k import và k báo lỗi nữa**」\n"
     "·「Quản lý calendar_new」r521-r522:「Msg chuẩn: "
     "**{line}行目の時間は現在より過去になりますので、登録できません。**」(báo lỗi, chặn)",
     "`web/api-spec.md` EP-51: bảng validate KHÔNG có dòng nào cho thời điểm quá khứ; "
     "phần xử lý ghi rõ「Nếu hợp lệ ⇒ với mỗi dòng: **bỏ qua thời điểm đã qua (`isPast()`, :420)**」"
     " ⇒ ĐỨNG VỀ PHÍA TAB CŨ.",
     "Đây là 2 hành vi hoàn toàn trái ngược ở tầng nghiệp vụ: một bên vẫn import các dòng hợp lệ "
     "còn lại, một bên chặn TOÀN BỘ file. Admin import file 100 dòng có 2 dòng quá khứ sẽ nhận "
     "kết quả khác hẳn nhau. Kho TCs viết theo SPEC (bỏ qua im lặng) và đánh dấu nhánh báo lỗi "
     "là FAIL cần escalate.",
     "[受付枠 — CSV export/import] 🔴 Import CSV: dòng có thời điểm QUÁ KHỨ — "
     "bỏ qua im lặng hay báo lỗi?",
     "",
     "Chạy thử import trên môi trường thật để xác định hành vi hiện tại, rồi cập nhật "
     "1 trong 2 tab TC và ghi rõ ngày spec change gần nhất."],

    ["MT-05", "CAO", W,
     "Giới hạn số lesson calendar theo gói — corpus và spec lệch nhau ở 3 gói",
     "「Calendar list」r8-r16 (05/2024):\n"
     "· free = **1** · standard `bot_contract_new` = **0** (hợp đồng CŨ) → **3** · "
     "standard `bot_contract_new` = 1 (hợp đồng MỚI) → **3** · pro → **10** · "
     "enterprise nền standard → **10** · enterprise nền pro → **10**",
     "`feature-spec.md` BR-01 (§8.1): free → **1**; **standard (MỚI) hoặc enterprise → 3**; "
     "**standard (CŨ), pro, enterprise_pro → 10**. Loại khác ⇒ không giới hạn nhưng nút vẫn bật.",
     "Lệch ở **3 gói**: (a) standard hợp đồng CŨ — corpus nói 3, spec nói 10; "
     "(b) enterprise nền standard — corpus nói 10, spec nói 3; (c) spec có nhánh「loại khác ⇒ "
     "không giới hạn」mà corpus không nhắc. Member test theo TC cũ sẽ báo FAIL oan trên bot "
     "standard hợp đồng cũ.",
     "[Giới hạn theo plan] Plan standard (bot_contract_new = 0) · "
     "Plan enterprise (standard) và enterprise (pro)",
     "",
     "Query `bot_contracts.contract_type` + `bots.flag_contract_new` của vài bot thật, "
     "chạy thử tạo calendar vượt hạn, chốt bảng giới hạn rồi sửa 1 trong 2 nguồn."],

    ["MT-63", "CAO", W,
     "🔴 6 lỗ hổng bảo mật mức Nghiêm trọng trong spec — corpus KHÔNG có TC nào",
     "Corpus CHỈ có 2 TC security ở tầng URL calendar:「Quản lý calendar」r3 và"
     "「Quản lý course」r180 (paste URL calendar/course của bot khác → redirect).\n"
     "**KHÔNG có bất kỳ TC nào** gọi trực tiếp API với tham số bị sửa.",
     "`feature-spec.md` §11.1 TOP-12 liệt kê 6 lỗ hổng **Nghiêm trọng**:\n"
     "· **RP-01 / S-04** — client gửi `checkHasPayment`, `amount`, `approve_type`; server KHÔNG "
     "đối chiếu `is_use_payment` / `calendar_course.amount` / kết quả cổng thanh toán "
     "(`Mobile/CalendarController.php:1425-1430`, `:1468-1487`)\n"
     "· **A-01** — nhóm 17 route `/ajax/calendar/*` thiếu `basic_access` + `is_expire` + miễn CSRF "
     "(`routes/web.php:2485`, `VerifyCsrfToken.php:16`)\n"
     "· **A-02** — `POST /{id}/edit` là IDOR ghi + mass assignment `$request->all()` "
     "(`CalendarManagementController.php:154-163`)\n"
     "· **A-06** — middleware CHỈ kiểm `{id}` calendar, KHÔNG kiểm `receptionId`/`bookingId`/`courseId` "
     "(`CheckLessonCalendarBelongToBot.php:20-30`)\n"
     "· **S-01** — IDOR đọc `EP-P16` rò rỉ PII xuyên bot (`Mobile/CalendarController.php:2557-2620`)\n"
     "· **BR-30** — chặn xóa course khi còn booking tương lai CHỈ kiểm ở FRONT-END",
     "Toàn bộ 6 lỗ hổng đều ở TẦNG API, không thể phát hiện qua thao tác UI thông thường. "
     "Bộ TC hiện tại của member 100% là TC thao tác UI ⇒ 6 lỗ hổng này **chưa từng được test**. "
     "Kho TCs đã bổ sung 6 TC verify API, tất cả đều đánh dấu **DỰ KIẾN FAIL**.",
     "[Đồng thời & verify API] 6 TC có tiền tố 🔴 (checkHasPayment · IDOR EP-P16 · id con · "
     "/ajax/calendar/* · POST /{id}/edit · xóa course) + [Phân quyền & môi trường] "
     "🔴 Staff bị cấm route vẫn thao tác được",
     "",
     "Chạy 6 TC này trước tiên. Mỗi TC FAIL phải raise ticket riêng theo mức Nghiêm trọng. "
     "Sau khi fix, đưa 6 TC vào bộ regression bắt buộc của mọi release chạm FA-019."],

    ["MT-61", "CAO", W,
     "Chế độ リクエスト制 nhận yêu cầu VÔ HẠN → duyệt hàng loạt gây overbooking chắc chắn",
     "「Booking phía line user」r557 (Bug KH #38280, 06/2026): slot remain = 1, 2 user bấm cùng lúc "
     "ở chế độ リクエスト制 ⇒「**Cả 2 booking đều book success, trạng thái là request booking**」"
     "— corpus coi đây là hành vi ĐÚNG.\n"
     "「Quản lý calendar_new」r407-r419: approve hàng loạt các booking đang リクエスト ⇒ "
     "kết quả mong đợi chỉ ghi「Trạng thái booking chuyển sang Đã approve」, **KHÔNG có TC nào "
     "kiểm sức chứa khi approve**.",
     "`feature-spec.md` §6.2 hệ quả 1: 🔴「`status = 0` KHÔNG chiếm chỗ ⇒ ở chế độ 「リクエスト制」 "
     "hệ thống **nhận yêu cầu VÔ HẠN**. `approveBooking` lại **không kiểm sức chứa** ⇒ duyệt hàng "
     "loạt là **overbooking chắc chắn**. Đây chính là lý do `MonitorCalendarBookingTask` tồn tại — "
     "và nó **chỉ cảnh báo Chatwork, KHÔNG tự sửa** (B-10)」.\n"
     "§10.4: job còn **BỎ QUA booking `admin_id != null`** và **BỎ QUA `status != 1`** ⇒ "
     "booking do admin tạo không bao giờ được giám sát (RA-02).",
     "Corpus coi「cả 2 đều thành công」là PASS, spec coi đó là nguyên nhân gốc của overbooking. "
     "Nếu Leader chốt theo corpus thì phải chấp nhận rủi ro nghiệp vụ: slot 定員 5 có thể có "
     "50 yêu cầu và admin bấm 承認 hàng loạt sẽ tạo 50 booking chiếm chỗ.",
     "[Đồng thời & verify API] Bug KH #38280: race condition ở chế độ リクエスト制 · "
     "[1人あたりの予約上限] Giới hạn = 1: ma trận 6 trạng thái booking · "
     "[リクエスト一括操作] Approve request booking hàng loạt",
     "",
     "Chốt: có bổ sung kiểm sức chứa ở `approveBooking` không. Nếu KHÔNG, phải viết TC "
     "「approve hàng loạt vượt 定員」với expected là ĐƯỢC PHÉP và ghi rõ đây là thiết kế, "
     "để member không raise bug nhầm."],

    ["MT-26", "CAO", W,
     "🔴 Modal「削除済み予約」: API trả success GIẢ + 2 nút approve/deny bị ĐẢO HANDLER",
     "Corpus **KHÔNG có TC nào** thao tác approve/deny trên modal của booking ĐÃ XÓA. "
     "Tab「Quản lý calendar_new」r920-r979 chỉ có TC xem thông tin và lịch sử.",
     "`feature-spec.md` §11.1 mục 10 (**B-2**): `findById()` = `find()` **thiếu `withTrashed()`** ⇒ "
     "booking đã xóa trả `null` ⇒ `continue` im lặng ⇒ method kết thúc không `return` ⇒ "
     "**API LUÔN trả `success: true`**; front-end `calendar_detail.js:4168` thấy `success` ⇒ "
     "**đóng modal + vẽ lại bảng** ⇒ UI báo thành công, DB không đổi.\n"
     "§11.1 mục 12 (**B-1**): nút 「承認する」/「否認する」 **ĐẢO HANDLER** ở "
     "`modal/history_deleted_booking_status.blade.php:165-174` và bản sao ở "
     "`tabs/booking/modal/…:159, 164` — **cả 2 file đang được `@include`**. "
     "🔴「NẾU SỬA B-2 MÀ KHÔNG SỬA NHÃN, LỖI SẼ NỔ NGAY: bấm 承認する → booking bị TỪ CHỐI. "
     "PHẢI SỬA CÙNG LÚC」.",
     "Đây là cặp lỗi che nhau: hiện tại B-1 vô hại vì B-2 làm mọi thao tác thành no-op. "
     "Nhưng admin đang bị lừa rằng thao tác đã thành công. Và nếu dev fix B-2 trước "
     "thì bấm 承認 sẽ TỪ CHỐI booking của khách.",
     "[Booking đã xóa] 🔴 Modal 削除済み予約: bấm 承認する / 否認する trên booking đã xóa",
     "",
     "Xác nhận modal booking đã xóa CÓ hiện 2 nút approve/deny không. Nếu có: raise 2 ticket "
     "và yêu cầu dev fix ĐỒNG THỜI. Nếu spec sai (modal thực tế không có nút): đính chính spec."],

    ["MT-49", "CAO", W,
     "Booking kẹt `status_webhook = 4` bị KHÓA VĨNH VIỄN với admin và ẨN khỏi lịch sử của khách",
     "「Sửa bill tiền univapay」r84 (LINE user):`status_webhook` = 4 ⇒「không hiện booking này ở màn "
     "lịch sử」· r103 (admin web) và r110 (app):`status_webhook` = 4 ⇒「nhấn cancel báo lỗi "
     "決済処理を行っていますので、操作できません。」\n"
     "Corpus **KHÔNG có TC nào** cho tình huống callback KHÔNG BAO GIỜ về.",
     "`feature-spec.md` §6.5 chốt chặn chung: mọi thao tác đổi trạng thái bị khóa khi "
     "`payment_system = 1` **và** `status_webhook ∈ {0, 3, 4}`. ⚠「Booking kẹt ở `status_webhook = 4` "
     "bị **khóa vĩnh viễn với Admin** và **ẩn khỏi lịch sử của khách** — "
     "**không có đường thoát tự động** (**RP-04**)」.\n"
     "BR-P24: UnivaPay poll **5 lần × 1 giây**, hết mà chưa có kết quả ⇒ `status_webhook = 4`.",
     "Với UnivaPay, chỉ cần webhook trễ hơn 5 giây và sau đó không bao giờ tới (mất mạng, "
     "sai Webhook ID, IP bị chặn) là booking vào trạng thái ma: khách đã trả tiền, không thấy "
     "booking đâu, admin không thao tác được gì. Corpus chỉ test tới mốc「sau 5 phút có callback」.",
     "[決済 — UnivaPay & webhook] UnivaPay: quá 2 phút chưa có callback → màn chờ; "
     "quá 5 phút → status_webhook = 4 · Khóa thao tác admin khi booking đang chờ webhook",
     "",
     "Chốt cơ chế thoát: job dọn booking kẹt sau N giờ, hoặc nút「強制解除」cho admin. "
     "Query production đếm số booking đang có `status_webhook = 4` để biết mức độ thật."],

    ["MT-41", "CAO", W,
     "Mã xác thực XÓA hệ thống đặt lịch: không hết hạn, lưu plaintext, trả thẳng trong response",
     "「Setting calendar」r1552:「nhập mã code đã quá 24h」— **CHỈ CÓ TIÊU ĐỀ, không có kết quả "
     "mong đợi** ⇒ chưa ai chốt mã có hết hạn hay không.\n"
     "r1549-r1551: chỉ test mã rỗng / sai / mã cũ đều báo lỗi.",
     "`feature-spec.md` BR-53:「Xoá hệ thống cần **mã 10 ký tự** gửi email; mã lưu ở `code_delete` "
     "và **không có hạn dùng, không xoá sau khi dùng**」.\n"
     "§11.1 TOP-5 (**A-05**): mã bị **trả THẲNG trong response JSON** (`'code' => $code`, "
     "`CalendarManagementController.php:670`) và lưu **plaintext**. "
     "「Toàn bộ cơ chế xác thực 2 bước bằng email là **hình thức**. "
     "**Dữ liệu thật: 13/174 lịch còn giữ mã trong DB**」.",
     "Hành vi xóa cả hệ thống đặt lịch (kèm toàn bộ course, slot, booking, remind) chỉ được "
     "bảo vệ bằng 1 mã mà bất kỳ ai xem được response HTTP đều lấy được, và mã đó dùng lại "
     "vô thời hạn. Corpus không có TC nào phát hiện được điều này.",
     "[予約システムの削除] Bước 2: validate mã xác thực — 5 tình huống · "
     "Mã xác thực xóa quá 24h → cần chốt còn dùng được không",
     "",
     "Raise ticket bảo mật riêng cho A-05. Chốt: mã hết hạn sau bao lâu, có xóa sau khi dùng không, "
     "có bỏ `'code' => $code` khỏi response không. Sau đó viết lại TC cho đúng."],

    ["MT-07", "CAO", W,
     "Booking của course đã OFF: CÓ hay KHÔNG hiện ở màn lịch sử phía LINE user?",
     "**2 tab nói NGƯỢC NHAU**:\n"
     "·「Quản lý course」r225 (Feature #27496, 01/2024):「Course OFF → Lịch sử book → "
     "**có hiện booking của course đã OFF**」— tiêu đề feature ghi rõ「Sửa để khi OFF course/staff, "
     "**lịch sử vẫn hiển thị**, chỉ ko hiển thị ra cho friend booking nữa」\n"
     "·「Booking phía line user」r62:「Booking đã bị OFF course → **ko hiển thị ở mh history nữa**」"
     "và r139 lặp lại y hệt.",
     "`feature-spec.md` BR-P03: khoá học chỉ hiện khi `booking_page_display = 1` **và** khách "
     "thoả FilterV2 — nhưng rule này nói về **màn CHỌN COURSE**, spec **không nói gì** về màn "
     "LỊCH SỬ khi course OFF.",
     "Đây là mâu thuẫn TRỰC TIẾP về hành vi người dùng cuối. Khách đã đặt và trả tiền cho một "
     "khóa học, admin tắt khóa học đó ⇒ khách còn xem được lịch sử đặt của mình hay không? "
     "Feature #27496 nói CÓ (và đó là mục đích của chính feature này), tab LINE user nói KHÔNG.",
     "[コース — list & hiển thị] Course OFF → LINE user vẫn thấy booking cũ ở lịch sử nhưng "
     "KHÔNG copy được · [LINE user — lịch sử & copy] Booking của course đã OFF / đã XÓA → "
     "không hiện ở lịch sử",
     "",
     "Test thật trên staging, chốt 1 hành vi, sửa TC ở tab còn lại. Nếu đúng là KHÔNG hiện "
     "thì Feature #27496 đã bị hồi quy ⇒ raise bug."],

    ["MT-12", "CAO", W,
     "Course OFF: booking của nó CÓ hay KHÔNG hiện ở 4 màn quản lý của admin?",
     "**2 tab nói NGƯỢC NHAU**:\n"
     "·「Quản lý course」r213-r220, r223 (Feature #27496):「Course OFF → Phía admin → màn today "
     "new booking / theo ngày / tuần / tháng / list / modal detail lịch sử / màn booking đã xóa / "
     "modal filter ⇒ **có hiện course đã OFF**」\n"
     "·「Today&NewBooking」r32-r35:「Logic liên quan đến course → các booking của course đã setting "
     "OFF → theo ngày / tuần / tháng / mh list ⇒ **ẩn các booking đi, check số lượng ở ngoài**」",
     "`feature-spec.md` §9 / `logic-spec.md`: các truy vấn màn quản lý (Today&NewBooking, "
     "danh sách theo list, tab 受付枠一覧) đều có điều kiện **`c.booking_page_display = 1`** "
     "⇒ ĐỨNG VỀ PHÍA tab「Today&NewBooking」(ẩn booking của course OFF).",
     "Ảnh hưởng trực tiếp tới bộ đếm hiển thị trên lưới calendar: nếu ẩn booking thì số "
     "予約確定 / リクエスト ở ô khung giờ cũng phải giảm tương ứng. Nếu Feature #27496 đúng thì "
     "câu query hiện tại đang SAI và admin đang mất dấu booking đã thu tiền.",
     "[コース — list & hiển thị] Course OFF → VẪN hiện ở màn quản lý & lịch sử admin · "
     "[Tab 本日/新着の予約] Course OFF → ẩn booking của course đó khỏi cả 4 chế độ xem",
     "",
     "Đối chiếu câu query thật ở 4 màn, chốt hành vi. Nếu chốt「vẫn hiện」thì phải bỏ điều kiện "
     "`booking_page_display = 1` khỏi query và viết lại TC bộ đếm."],

    ["MT-56", "CAO", W,
     "Validate số điện thoại: LINE user chấp nhận 10-12 số, ADMIN chỉ chấp nhận đúng 11 số",
     "·「Booking phía line user」r329 (phía LINE user):「Nhập < 10 chữ số → Báo lỗi · "
     "**Nhập vào số 10-12 chữ số → Pass**」\n"
     "·「Quản lý calendar_new」r543 (phía ADMIN book):「Nhập vào số 10 chữ số → **Báo lỗi** "
     "携帯電話11桁の数値を入力してください。· Nhập vào số 12 chữ số → **Báo lỗi** · "
     "**Nhập vào số 11 chữ số → Pass**」",
     "`feature-spec.md` §5.5 và `logic-spec-public.md`: rule validate lưu ở "
     "`calendar_setting_send_forms.rule_validation_type`, nhãn UI là "
     "「**電話番号（11桁ハイフンなし）のみ**」 ⇒ tên rule khẳng định **11 chữ số**.",
     "CÙNG 1 câu hỏi, CÙNG 1 rule validate nhưng 2 cổng nhập cho kết quả khác nhau. "
     "Khách nhập số 10 chữ số qua LIFF thì lưu được, admin sửa lại chính giá trị đó thì bị chặn "
     "⇒ dữ liệu bẩn không sửa được. Nhãn UI cũng ghi rõ 11 桁.",
     "[LINE user — nhập form & xác nhận] Form booking: 4 rule validate của item 短文回答 · "
     "[Admin thêm booking thủ công] Admin book: validate 4 kiểu format của câu hỏi short text",
     "",
     "Chốt 1 quy tắc (nhiều khả năng là 11 số theo nhãn UI), sửa phía còn lại và cập nhật TC. "
     "Kiểm dữ liệu production xem có bao nhiêu giá trị 10 hoặc 12 số đang tồn tại."],

    ["MT-04", "CAO", W,
     "Tên course: popup tạo đầu giới hạn 30 ký tự, màn detail lại 50 ký tự",
     "·「Calendar list」r38 (popup tạo course NGAY SAU khi tạo calendar):「nhập ký tự dài ⇒ "
     "**ko giới hạn ký tự => max 30 ký tự**」\n"
     "·「Quản lý course」r28-r29 (popup コース作成 và màn detail):「Nhập 50 ký tự ⇒ **Save success**; "
     "Nhập 51 ký tự ⇒ Không cho phép nhập」kèm ghi chú「**Đã confirm là course name hiển thị bên "
     "booking và nhập max 50 ký tự**」",
     "`web/api-spec.md` FormRequest `CreateCalendarCourse` / `EditCalendarCourse` — spec KHÔNG ghi "
     "cụ thể giới hạn ký tự của `course_name` ở 2 luồng tạo khác nhau.",
     "Cùng 1 trường `calendar_course.course_name` nhưng 2 form nhập giới hạn khác nhau ⇒ "
     "admin tạo course qua wizard bị cắt còn 30 ký tự, tạo qua nút コース作成 thì được 50. "
     "Member không biết dùng con số nào để test.",
     "[Wizard tạo calendar] Tên course ở popup tạo đầu — giới hạn 30 ký tự · "
     "[コース — tạo/sửa/xóa] Tên course ở popup tạo — biên 50 và 51 ký tự",
     "",
     "Chốt 1 giới hạn cho cả 2 form. Kiểm dữ liệu production xem có course nào dài > 30 ký tự "
     "không (nếu có thì 50 là đúng)."],

    ["MT-39", "CAO", W,
     "店舗名 ở màn トップ設定: 30 ký tự hay 100 ký tự?",
     "「Setting calendar」r1281:「Check setting tên cửa hàng 店舗名 => **Change spec** ⇒ "
     "**100 ký tự**」và r1282-r1283 test 100 / 101 ký tự.\n"
     "NHƯNG r1285:「Nhập vào tên cửa hàng valid với **30 ký tự** => Update success」và "
     "r1288:「Nhập vào 31 ký tự ⇒ Báo lỗi **店舗名は30文字以内で入力してください。**」",
     "`ui/ui-spec.md` SCR-LSN-19「店舗・ビジネス情報」— spec liệt kê trường `line_name`/`store_name` "
     "nhưng KHÔNG ghi giới hạn ký tự.",
     "TỰ MÂU THUẪN trong cùng 1 tab, cùng 1 khối TC: dòng trên nói đã đổi spec sang 100 ký tự, "
     "dòng dưới lại có message lỗi hard-code 30 文字以内. Message lỗi tiếng Nhật là bằng chứng "
     "mạnh hơn ⇒ nhiều khả năng 100 ký tự là spec change CHƯA ĐƯỢC IMPLEMENT.",
     "[トップ・店舗情報・利用規約] 店舗名 ở màn トップ設定 — default, validate 30/31 và required",
     "",
     "Xác nhận spec change 100 ký tự đã release chưa. Nếu chưa: xóa dòng r1281 khỏi TC. "
     "Nếu rồi: message lỗi phải đổi thành 100文字以内."],

    ["MT-58", "CAO", W,
     "Đăng ký chờ hủy rồi book lại: booking status = 3 bị UPDATE ĐÈ hay GIỮ NGUYÊN?",
     "·「Booking phía line user」r438 (2024-2025):「Booking có status đợi slot trống sẽ **KHÔNG bị "
     "xóa đi**」kèm câu query đếm số booking status = 3\n"
     "·「Setting calendar」r1232-r1233 (Bug KH #36729, **05/2026 — mới hơn**):「CHeck DB: **không tạo "
     "booking mới mà sẽ update vào booking có status = 3 ban đầu**」",
     "`feature-spec.md` §6.3 bảng chuyển trạng thái: **T-05** (`EP-P10`/`EP-P11` `handleKeepSlot()` "
     "thấy bản `status=3` cùng slot ⇒ **UPDATE đè** → `1`) và **T-06** (`EP-P12` `bookingType = notify` "
     "⇒ UPDATE đè → `1` hoặc `0`) ⇒ ĐỨNG VỀ PHÍA bản 05/2026.",
     "Nếu UPDATE đè thì bản ghi status = 3 KHÔNG CÒN TỒN TẠI sau khi book lại ⇒ câu query của r438 "
     "sẽ trả 0 và member báo FAIL. Đây là 2 mô hình dữ liệu khác nhau, ảnh hưởng cả bộ đếm "
     "`total_request_booking_wait_cancel`.",
     "[LINE user — キャンセル待ち] Nhận thông báo có chỗ trống rồi book lại → booking cũ status 3 "
     "KHÔNG bị xóa · [空き枠通知受け取り設定] Bug KH #36729: nhánh bookingType='notify'",
     "",
     "Chốt theo T-05/T-06 (update đè) và XÓA TC r438 khỏi tab cũ, hoặc chứng minh có 2 luồng "
     "khác nhau (book từ link thông báo vs book mới hoàn toàn) rồi tách rõ 2 TC."],

    ["MT-60", "CAO", W,
     "Đăng ký chờ hủy LẦN 2 cùng slot: hiển thị 1 booking hay BỊ CHẶN kèm message?",
     "·「Booking phía line user」r92, r163 (2024-2025):「check 1 user booking vào 1 slot nhận thông "
     "báo **2 lần** ⇒ **1 user được booking nhiều lần nhưng hiển thị 1 booking**」— tức là CHO PHÉP\n"
     "·「Setting calendar」r1225-r1226 (Bug KH #36729, **05/2026**):「Chặn đăng ký trùng cùng slot "
     "⇒ **Hiển thị message lỗi キャンセル待ち通知受け取りがすでに登録されています**. Không gửi message mới; "
     "Không gửi URL mới; DB không thay đổi」",
     "`feature-spec.md` BR-28 / BR-P11: khách đã có bản `status = 3` cùng slot ⇒ **UPDATE đè** "
     "thay vì tạo dòng mới — nói về luồng ADMIN book và luồng book thật, KHÔNG nói về luồng "
     "đăng ký chờ hủy LẶP LẠI.",
     "Bug KH #36729 là bug THẬT của khách hàng: đăng ký lần 2 vẫn gửi lại キャンセル用URL với "
     "`booking_id` RỖNG, khách bấm vào thấy「予約が解除されました」nhưng đăng ký chưa hủy. "
     "Fix là CHẶN ngay từ đầu. TC cũ (cho phép) đã lỗi thời.",
     "[LINE user — キャンセル待ち] 1 user đăng ký chờ hủy 2 lần cùng slot / 2 slot khác nhau · "
     "[空き枠通知受け取り設定] Bug KH #36729 — tái hiện và 6 TC liên quan",
     "",
     "Xác nhận #36729 đã release. Nếu rồi: sửa TC r92/r163 ở tab「Booking phía line user」thành "
     "「bị chặn kèm message」để member không báo PASS nhầm."],

    ["MT-29", "CAO", W,
     "Giới hạn số lần đặt / 1 khách: booking đang CHỜ APPROVE không tính vào giới hạn",
     "「Setting calendar」r142:「booking sẵn có ở trạng thái **booking chờ approve** ⇒ "
     "**vẫn booking dc**」(tức là status 0 KHÔNG tính vào giới hạn)",
     "`feature-spec.md` BR-P07: trần số lần đặt/khách đếm booking có "
     "**`status ∈ {1,2,5}`** ⇒ **khớp corpus**.\n"
     "NHƯNG §6.2 hệ quả 1 cảnh báo đây chính là lỗ hổng: `status = 0` không chiếm chỗ ⇒ "
     "user có thể gửi VÔ HẠN yêu cầu ở chế độ リクエスト制.",
     "Corpus và spec KHỚP về mặt kỹ thuật, nhưng cả hai đều bỏ ngỏ hệ quả nghiệp vụ: "
     "một khách có thể gửi 100 yêu cầu đặt cùng lúc dù calendar giới hạn 1 lần/khách. "
     "Cần Leader chốt đây là chấp nhận được hay là bug.",
     "[1人あたりの予約上限] Giới hạn = 1: ma trận 6 trạng thái booking sẵn có",
     "",
     "Nếu chấp nhận: ghi rõ vào spec để không ai raise bug. Nếu không: bổ sung status 0 vào "
     "phép đếm của BR-P07 và viết TC mới."],

    ["MT-54", "TRUNG BÌNH", W,
     "Chế độ 月 và 週 hiển thị slot chưa tới giờ mở nhận đặt KHÁC NHAU?",
     "「Booking phía line user」r249-r257 (màn TUẦN) và r273-r281 (màn THÁNG) — "
     "SpecImprove #32808 + #32884 (11/2025): CẢ HAI chế độ đều「**hiển thị -**」khi chưa tới giờ "
     "mở nhận đặt, và「hiển thị ◯」khi đã tới giờ. Không phân biệt tuần/tháng.",
     "`web/logic-spec-public.md:941` **BR-P05**:「Chế độ 「月」 **loại bỏ** slot chưa tới giờ mở "
     "nhận đặt, trong khi chế độ 「週」 chỉ **khoá** nó ⇒ **hai chế độ hiển thị lệch nhau**」"
     "(`MC:2934-2936` vs `:2806-2816`).",
     "「Loại bỏ」và「khoá」cho ra 2 kết quả hiển thị khác nhau ở màn tháng: nếu loại bỏ hết slot "
     "thì ngày đó KHÔNG có slot nào ⇒ ngày bị disable; nếu chỉ khoá thì ngày vẫn enable và "
     "bấm vào thấy slot dấu「-」. Corpus test theo hướng thứ 2.",
     "[LINE user — chọn 受付枠] SpecImprove #32808/#32884: chưa tới giờ MỞ nhận đặt → hiển thị dấu「-」· "
     "Màn THÁNG: 1 ngày có 2 slot — ma trận 8 tổ hợp trạng thái",
     "",
     "Test thật cả 2 chế độ với slot chưa tới giờ mở nhận. Nếu 2 chế độ vẫn lệch ⇒ raise bug "
     "hồi quy của #32884 (ticket này chính là để sửa màn tháng)."],

    ["MT-01", "TRUNG BÌNH", W,
     "Calendar OFF: LINE user thấy lỗi 404 hay message「この予約は現在利用できません。」?",
     "·「Calendar list」r47 (05/2024):「Nếu OFF ⇒ khi user click vào url booking/history ⇒ "
     "**hiển thị 404**」\n"
     "·「Booking phía line user」r4-r5 (mới hơn):「Calendar OFF => Click link booking ⇒ "
     "**Báo lỗi この予約は現在利用できませんん。**」(chú ý typo 2 chữ ん trong TC gốc)",
     "`feature-spec.md` BR-P01: 6 điều kiện chặn trước khi render, điều kiện cuối là "
     "`enable_use_calendar = 1`. `ui/ui-spec-liff.md` SCR-LSN-L21:「この予約は現在利用できません。」"
     "⇒ ĐỨNG VỀ PHÍA tab mới.",
     "404 là trang trắng của trình duyệt, còn message là màn có thiết kế — trải nghiệm khách hàng "
     "khác hẳn. Ngoài ra TC gốc có TYPO「利用できませんん」(2 chữ ん) — cần xác nhận text thật.",
     "[Màn list calendar] OFF calendar → LINE user mở URL booking và URL lịch sử đều bị chặn · "
     "[LINE user — mở link & entry] Calendar ON / OFF / đã xóa → 3 kết quả",
     "",
     "Chụp màn hình thật khi calendar OFF, chốt text chính xác (kiểm cả typo ん), "
     "cập nhật TC ở tab cũ."],

    ["MT-52", "TRUNG BÌNH", W,
     "Calendar ĐÃ XÓA và calendar OFF dùng CÙNG message hay message riêng?",
     "·「Booking phía line user」r4-r5: cả OFF và ĐÃ XÓA đều「Báo lỗi この予約は現在利用できませんん。」\n"
     "·「Setting calendar」r1561-r1562 (khối 予約システムの削除):「User click vào link booking của "
     "calendar đã bị xóa ⇒ Hiển thị msg lỗi **この予約ページはすでに削除されて います。**」",
     "`ui/ui-spec-liff.md` SCR-LSN-L21 liệt kê「この予約は現在利用できません。」và redirect 404/410 — "
     "KHÔNG thấy chuỗi「この予約ページはすでに削除されています。」trong spec.",
     "2 message khác nhau cho 2 tình huống khác nhau là ĐÚNG về UX (khách biết được lịch bị tắt "
     "tạm hay đã xóa hẳn), nhưng tab「Booking phía line user」gộp làm một. Nếu hệ thống thật chỉ "
     "có 1 message thì spec và tab Setting calendar đều sai.",
     "[LINE user — mở link & entry] Calendar ON / OFF / đã xóa → 3 kết quả khi mở URL booking · "
     "[予約システムの削除] LINE user mở URL của calendar đã bị xóa",
     "",
     "Test thật 2 tình huống, chốt message, đồng bộ 2 tab TC và bổ sung chuỗi thiếu vào "
     "`ui-spec-liff.md`."],

    ["MT-02", "TRUNG BÌNH", W,
     "Trường tên vượt giới hạn ký tự: TỰ CẮT hay BÁO LỖI?",
     "「Calendar list」r29 (tên hiển thị bên LINE, 30 ký tự) và r32 (管理名, 10 ký tự) đều ghi "
     "kết quả mong đợi là「**tự động cắt hoặc báo lỗi quá số ký tự cho phép**」— **để ngỏ 2 khả năng**.\n"
     "Trong khi r60 (popup đổi 管理名) lại ghi dứt khoát「**báo lỗi quá số ký tự**」.",
     "`web/api-spec.md`: các endpoint tạo/sửa calendar — spec KHÔNG ghi hành vi khi vượt giới hạn "
     "(cắt hay từ chối).",
     "Đây không phải mâu thuẫn giữa 2 nguồn mà là TC gốc KHÔNG QUYẾT ĐỊNH. Member test sẽ "
     "báo PASS cho cả 2 hành vi ⇒ TC mất tác dụng. Ngoài ra tự cắt âm thầm là hành vi nguy hiểm "
     "(admin không biết tên bị cắt).",
     "[Wizard tạo calendar] Tên hiển thị bên LINE — biên 30 và 31 ký tự · 管理名 lúc tạo — "
     "biên 10 và 11 ký tự",
     "",
     "Chốt 1 hành vi thống nhất cho toàn bộ trường có giới hạn ký tự của FA-019, "
     "sửa lại kết quả mong đợi của 3 TC trên."],

    ["MT-03", "THẤP", W,
     "Bấm Back từ popup tạo calendar rồi vào lại: có giữ data đã nhập không?",
     "「Calendar list」r35:「button back ⇒ back về mh preview trước đó — "
     "**từ mh preview click next ra mh tạo thì có hiển thị data trước đấy nhập ko?**」"
     "— là CÂU HỎI, không phải kết quả mong đợi.",
     "`ui/ui-spec.md` SCR-LSN-02「レッスン予約（新規作成）」— spec mô tả trang giới thiệu + modal "
     "tạo lịch mới, KHÔNG ghi hành vi giữ/xóa data khi back.",
     "TC gốc để ngỏ. Với form chỉ có 2 ô tên thì mức ảnh hưởng thấp, nhưng vẫn cần chốt để "
     "member không phân vân.",
     "[Wizard tạo calendar] Nút X và Back trên popup tạo calendar",
     "",
     "Test thật 1 lần, ghi kết quả vào TC. Ưu tiên thấp."],

    ["MT-08", "TRUNG BÌNH", W,
     "system_name của course để trống: BÁO LỖI required hay TỰ CẮT 10 ký tự từ course name?",
     "「Quản lý course」r41 — kết quả mong đợi ghi **2 Ý TRÁI NGƯỢC trong cùng 1 ô**:\n"
     "「**Save success** và lấy course name cắt lấy 10 ký tự」\n"
     "「**báo lỗi - required nhập**」",
     "`web/api-spec.md` FormRequest `CreateCalendarCourse` / `EditCalendarCourse` — "
     "spec KHÔNG nêu quy tắc cho `system_name` khi rỗng.\n"
     "`feature-spec.md` §7 Field Traceability Matrix: `calendar_course.system_name` được dùng làm "
     "tên hiển thị phía admin ở nhiều màn ⇒ nếu rỗng thì các màn quản lý sẽ hiển thị trống.",
     "TỰ MÂU THUẪN trong 1 ô TC. Hệ quả rất khác nhau: nếu tự cắt thì admin luôn có tên hiển thị; "
     "nếu required thì admin buộc phải nhập. Nhiều màn admin (lưới calendar, CSV, Google Sheet) "
     "đều ưu tiên `system_name`.",
     "[コース — tạo/sửa/xóa] Tab 基本情報: system_name để trống → hành vi chưa chốt",
     "",
     "Test thật, chốt 1 hành vi. Nếu là required thì kiểm dữ liệu production có course nào "
     "`system_name` rỗng không (course cũ có thể chưa có)."],

    ["MT-09", "TRUNG BÌNH", W,
     "Xóa course khi còn booking 予約確定 ở QUÁ KHỨ: có cho xóa không?",
     "**2 khối trong CÙNG tab「Quản lý course」nói ngược nhau**:\n"
     "· r77 (khối cũ):「kể cả có booking **đã qua time rồi nhưng vẫn ở status booking success** "
     "thì vẫn **ko cho xóa** (**đã confirm a Tư**)」\n"
     "· r181-r197 (Support #27091, **11/2024 — mới hơn**):「Sửa để **chỉ validate với các booking "
     "trong tương lai**」và r184「có booking success của admin **trong quá khứ** ⇒ **xóa dc**」",
     "`feature-spec.md` BR-30:「Không xoá được khoá học khi còn đặt chỗ **tương lai** "
     "`status ∉ {4,7}`」⇒ ĐỨNG VỀ PHÍA Support #27091.",
     "Support #27091 chính là ticket sửa hành vi cũ. TC r77 là bản TRƯỚC khi fix nhưng vẫn nằm "
     "trong tab, member đọc nhầm sẽ báo FAIL khi hệ thống cho xóa course có booking quá khứ.",
     "[コース — tạo/sửa/xóa] Xóa course khi còn booking 予約確定 hoặc リクエスト → chặn kèm alert · "
     "Support #27091: chỉ chặn xóa course khi còn booking TƯƠNG LAI",
     "",
     "Xóa/đánh dấu lỗi thời cho câu「kể cả có booking đã qua time」ở r77. Lưu ý BR-30 nói rule này "
     "CHỈ kiểm front-end ⇒ xem thêm MT-63."],

    ["MT-10", "TRUNG BÌNH", W,
     "Bộ đếm 対象人数 của filter: có TRỪ friend đã block / hide / bị block không?",
     "「Quản lý course」r116:「hiển thị **XX人（友だち全員）** — xx là toàn bộ số friend của user "
     "(**trừ friend đã block/ hide/ bị block?**)」— có **DẤU HỎI**, chưa chốt.",
     "`feature-spec.md` §12.1: FilterV2 là **shared component SC-002** — công thức đếm nằm ở "
     "component dùng chung, spec FA-019 KHÔNG mô tả.",
     "Con số này quyết định admin có tin vào filter hay không. Nếu đếm cả friend đã block thì "
     "số hiển thị luôn lớn hơn số người thật sự nhận được action ⇒ admin hiểu nhầm hiệu quả.",
     "[コース — action & filter riêng] Bộ đếm 対象人数 của filter course — case không filter và có filter",
     "",
     "Hỏi dev công thức đếm của FilterV2 (SC-002), ghi vào spec shared component, "
     "rồi viết lại expected có số cụ thể."],

    ["MT-13", "THẤP", W,
     "Màn danh sách slot dạng「一覧」: bấm 詳細 mở danh sách booking hay màn edit slot?",
     "「Quản lý calendar_new」r233 — kết quả mong đợi ghi:「**Mở danh sách booking hay mở MH edit slot?**」"
     "— là CÂU HỎI.\n"
     "r235 (dòng ngay dưới) lại ghi:「Click button detail 詳細 ⇒ **Ra màn hình danh sách booking "
     "theo course tương ứng**」",
     "`ui/ui-spec.md:1264` mô tả `booking_list_week.blade.php` có 2 view nhưng KHÔNG ghi đích đến "
     "của nút 詳細 ở view 一覧.",
     "2 dòng liền nhau trong cùng tab, 1 dòng hỏi và 1 dòng trả lời — nhiều khả năng r235 là "
     "câu trả lời cho r233 nhưng không ai xóa dấu hỏi. Cần xác nhận để tránh member phân vân.",
     "[Modal danh sách booking] Dạng 一覧: dữ liệu hiển thị và nút 詳細",
     "",
     "Xác nhận 1 lần trên staging, xóa dấu hỏi ở r233."],

    ["MT-14", "TRUNG BÌNH", W,
     "Thêm khung giờ theo「chọn ngày cụ thể」: server KHÔNG kiểm ngày quá khứ và giới hạn 1 năm",
     "「Quản lý calendar_new」r271:「Check giao diện calendar ⇒ **Không cho phép chọn ngày quá khứ**」"
     "— chỉ test ở tầng GIAO DIỆN (ngày quá khứ bị disable).\n"
     "Corpus KHÔNG có TC nào gọi API trực tiếp với ngày quá khứ.",
     "`web/logic-spec.md:774` **BR-16**:「Chế độ chọn ngày cụ thể nhận `dateCanBooking` là "
     "**timestamp mili-giây**: `Carbon::createFromTimestamp($date / 1000)` — "
     "**không kiểm quá khứ, không kiểm giới hạn 1 năm**」(`CCRS.php:90-94`).\n"
     "Trong khi chế độ lặp theo thứ (BR-11/12/13) CÓ kiểm cả 2 điều kiện.",
     "2 chế độ thêm slot có mức kiểm soát khác nhau. Client sửa timestamp là tạo được slot "
     "ở năm 1990 hoặc năm 2050 — dữ liệu rác không xóa được qua UI (ngày quá khứ không hiện "
     "trên lịch).",
     "[受付枠 — thêm khung giờ] Calendar chọn ngày: KHÔNG cho chọn ngày quá khứ · "
     "Add slot theo THỨ: validate ngày hết hạn lặp",
     "",
     "Chốt: có bổ sung validate ở server cho chế độ chọn ngày không. Nếu không, "
     "ghi rõ vào spec là chấp nhận rủi ro."],

    ["MT-17", "THẤP", W,
     "定員 khi chọn「có giới hạn」: nhập 0 hoặc để trống → hành vi gì?",
     "「Quản lý calendar_new」r291:「Check chọn set max và **nhập 0, để trống**」— "
     "**CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi**.\n"
     "Trong khi r293 (nhập số < 0 hoặc không phải số) có kết quả rõ:「Invalid」.\n"
     "Ngược lại, import CSV r519 lại ghi rõ:「Nhập total person = 0 ⇒ **import success**」",
     "`web/api-spec.md` EP-51: validate cột sức chứa là `無制限` hoặc `^(0|[1-9]\\d*)$` "
     "⇒ **0 là giá trị HỢP LỆ** ở luồng import CSV.",
     "Luồng import CSV cho phép 定員 = 0 nhưng luồng nhập tay chưa chốt. Nếu 2 luồng khác nhau "
     "thì admin import file có dòng 0 sẽ tạo được slot mà UI không cho tạo.",
     "[受付枠 — thêm khung giờ] 定員: nhập số âm / không phải số → Invalid · "
     "[受付枠 — CSV export/import] Import CSV: 予約上限人数 = 0 → import success",
     "",
     "Chốt hành vi của ô nhập tay cho khớp với import CSV (0 hợp lệ), viết lại expected của r291."],

    ["MT-18", "CAO", W,
     "🔴 `updateReception` (EP-46) LUÔN trả `success: true` kể cả khi reception không tồn tại",
     "「Quản lý calendar_new」r983:「1. Mở 2 tab của 1 detail slot · 2. Tab thứ 1 xóa slot này · "
     "3. Tab thứ 2 vào edit thông tin của slot」— **CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi**.",
     "`feature-spec.md` §11.1 mục 11 (**B-4 / A-23 / M-9(b)**): Service `return false` khi reception "
     "không tồn tại, nhưng **controller VỨT BỎ giá trị trả về và luôn trả `{'success' => true}`** "
     "(`CalendarCourseReceptionService.php:279-283`; `CalendarManagementController.php:374-383`). "
     "「Admin sửa khung giờ, **UI báo thành công, DB không đổi**」.",
     "Đây đúng là kịch bản mà TC r983 muốn kiểm nhưng chưa ai viết kết quả. Admin sửa 定員 rồi "
     "thấy toast thành công, nhưng slot đã bị xóa ở tab khác ⇒ thay đổi bốc hơi. "
     "Lỗi này ĐỘC LẬP với B-2 (modal 削除済み予約).",
     "[受付枠 — sửa 定員 & xóa] Mở 2 tab cùng 1 slot: tab 1 xóa slot, tab 2 vào edit slot đó",
     "",
     "Chạy TC này, xác nhận có trả success giả không, raise ticket B-4. "
     "Chốt hành vi mong muốn: báo lỗi rõ ràng hay tự reload danh sách."],

    ["MT-19", "TRUNG BÌNH", W,
     "Xóa nhiều slot: booking đang REQUEST CANCEL (status 5) có chặn được xóa không?",
     "「Quản lý calendar_new」r1008-r1012 liệt kê 5 nguồn booking approve gây chặn xóa, "
     "**KHÔNG có case booking đang ở status 5 (request cancel)**.\n"
     "Corpus KHÔNG có TC nào cho tình huống này.",
     "`feature-spec.md` **BR-17**: không xoá được khung khi còn 「予約確定」 (**`total_approve > 0`**); "
     "xoá hàng loạt kiểm **`SUM(total_approve) > 0`**.\n"
     "Nhưng §6.2: nhóm CHIẾM CHỖ là **`{1, 2, 5}`** — status 5 VẪN chiếm chỗ và được đếm vào "
     "`total_request_cancel`, KHÔNG vào `total_approve`.",
     "Suy ra từ spec: slot chỉ còn booking status 5 sẽ **XÓA ĐƯỢC** (vì `total_approve` = 0), "
     "dù booking đó đang chiếm chỗ và khách chưa được duyệt hủy. Khách sẽ mất booking mà không "
     "được thông báo. Corpus chưa từng kiểm nhánh này.",
     "[受付枠 — xóa nhiều] Xóa nhiều slot — ma trận 6 nguồn booking approve đều chặn (case 6)",
     "",
     "Test thật, chốt: `total_approve` hay `total_approve + total_request_cancel`. "
     "Nếu xóa được thì cân nhắc bổ sung điều kiện."],

    ["MT-20", "TRUNG BÌNH", W,
     "Import CSV: sai TÊN CỘT vẫn import được (lấy theo thứ tự cột)",
     "「Quản lý calendar_new」r507:「Cột trong file không để đúng name column ⇒ "
     "**sai tên cột vẫn cho vào, dev đang lấy theo thứ tự cột**」",
     "`web/api-spec.md` EP-51: bảng validate chỉ kiểm ĐỊNH DẠNG từng cột theo VỊ TRÍ "
     "(cột 1 ngày, cột 2 giờ bắt đầu, cột 3 giờ kết thúc, cột 4 sức chứa), "
     "**không kiểm header** ⇒ khớp corpus.\n"
     "⚠ Spec còn ghi thêm 2 rủi ro: `fopen($request['file'], 'r')` có nguy cơ **LFI/SSRF** "
     "nếu client gửi chuỗi thay vì file, và **không giới hạn số dòng CSV**.",
     "Đây là hành vi silent-error: admin đổi thứ tự cột trong Excel rồi import ⇒ ngày bị đọc "
     "thành giờ, dữ liệu vào sai hoàn toàn mà không có cảnh báo nào. Corpus ghi nhận nhưng "
     "coi là chấp nhận được.",
     "[受付枠 — CSV export/import] Import CSV: validate file và cột — sai định dạng file, sai tên cột",
     "",
     "Chốt: có bổ sung validate header không. Đồng thời raise 2 rủi ro LFI/SSRF và "
     "không giới hạn số dòng thành ticket riêng."],

    ["MT-21", "THẤP", W,
     "Filter booking theo thời gian: from = to (khác 00:00) và chỉ nhập 1 đầu → chưa chốt",
     "「Quản lý calendar_new」r360 (chọn time from = time to), r362 (chỉ nhập from, to để 00:00), "
     "r363 (chỉ nhập to, from để 00:00) — **CẢ 3 CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi**.\n"
     "Trong khi modal filter SLOT (r461-r463) lại có kết quả rõ:「00:00~00:00 ⇒ Filter all; "
     "start = end khác 00:00 ⇒ Data invalid, ko hiển thị kết quả gì」",
     "`web/logic-spec.md`: spec KHÔNG mô tả hành vi filter theo khoảng giờ khi 2 đầu bằng nhau.",
     "2 modal filter (booking và slot) rất giống nhau nhưng 1 cái đã chốt còn 1 cái chưa. "
     "Có thể áp dụng cùng quy tắc, nhưng cần xác nhận.",
     "[Modal filter booking] Filter booking theo thời gian bắt đầu course — biên và quan hệ from/to",
     "",
     "Áp dụng quy tắc của modal filter slot (r461-r463) cho modal filter booking sau khi test "
     "xác nhận, rồi điền expected."],

    ["MT-22", "TRUNG BÌNH", W,
     "`denyBooking` và `denyCancel` DÙNG CHUNG nội dung từ chối — không tách được",
     "「Quản lý calendar_new」r420-r427 (deny request booking) và r436-r443 (deny request cancel) "
     "mô tả 2 luồng RIÊNG với 2 mẫu message riêng ở tab setting "
     "(「予約リクエスト否認時」và「キャンセルリクエスト否認時」).",
     "`feature-spec.md` **BR-45**: ⚠「`denyBooking` và `denyCancel` **dùng chung** "
     "`setting_action_reject` + `message_send_deny` ⇒ **không tách được** nội dung từ chối đặt "
     "và từ chối huỷ」.",
     "Nếu spec đúng thì việc admin setting 2 nội dung khác nhau ở 2 tab là VÔ NGHĨA — hệ thống "
     "chỉ dùng 1 nội dung cho cả 2 trường hợp. Khách bị từ chối YÊU CẦU HỦY sẽ nhận tin "
     "「予約を受け付けることができませんでした」(từ chối đặt) — sai hoàn toàn ngữ cảnh.",
     "[リクエスト一括操作] Deny request booking hàng loạt · Deny request booking: ưu tiên action · "
     "[予約・キャンセル アクション] 4 loại message của luồng booking",
     "",
     "Test thật: setting 2 nội dung khác nhau rồi deny 1 booking và 1 request cancel, "
     "so sánh tin khách nhận. Nếu giống nhau ⇒ raise bug."],

    ["MT-23", "TRUNG BÌNH", W,
     "Thao tác hàng loạt với booking KHÔNG khớp action: im lặng nhưng API vẫn trả `success: true`",
     "「Quản lý calendar_new」r445:「Booking nào không nằm trong thao tác admin chọn thì **bỏ qua** "
     "(không change trạng thái và không gửi action)」— coi là hành vi ĐÚNG.",
     "`feature-spec.md` **BR-22 / BR-P18**: chỉ **6 cặp guard** (status nguồn, action) hợp lệ; "
     "cặp không khớp ⇒ **không nhánh nào chạy**, nhưng `updateStatusBooking()` + "
     "`countTotalBookingStatus()` **vẫn chạy** và API **vẫn trả `success: true`** (**RA-17**).",
     "Corpus và spec khớp về kết quả nhìn thấy được (booking không đổi), nhưng spec chỉ ra 2 hệ quả "
     "ẩn: (a) admin không có phản hồi nào về việc bao nhiêu booking bị bỏ qua; "
     "(b) `countTotalBookingStatus()` vẫn chạy trên slot đó ⇒ nếu bộ đếm đang lệch thì bị ghi đè "
     "âm thầm.",
     "[リクエスト一括操作] Chọn tập booking có cả loại KHÔNG phù hợp với action",
     "",
     "Chốt: có cần hiện thông báo「X/Y booking đã được xử lý」không. Nếu có, viết TC mới."],

    ["MT-24", "TRUNG BÌNH", W,
     "Bảng mã `calendar_course_booking_history_actions.status`: khối TC thường để TRỐNG nhiều ô",
     "**2 khối trong tab「Quản lý calendar_new」có độ đầy đủ khác nhau**:\n"
     "· r735-r748 (tab 予約履歴 thường): nhiều dòng ghi「status = 」**BỎ TRỐNG** — 予約キャンセル, "
     "キャンセルリクエスト, キャンセルリクエスト 承認/否認, 返金, 受付枠削除による予約削除\n"
     "· r949-r962 (màn booking đã xóa): ĐẦY ĐỦ — 1, 2, 4, 14, 5, 6, 7, 9, 15, 10, 11, 12, 13",
     "`feature-spec.md` §5.5: `…_history_actions.status` (`SBH_*`) có **16 giá trị**, "
     "「UI chỉ hiển thị 13/16 (đúng thiết kế)」.\n"
     "§6.3 bảng 21 chuyển trạng thái có cột `history.status` đầy đủ cho từng chuyển tiếp.",
     "Khối r735-r748 bỏ trống làm member không biết verify DB thế nào. Kho TCs đã lấy theo "
     "khối đầy đủ (r949-r962) và §6.3 của spec.",
     "[Detail booking & lịch sử] Tab 予約履歴: 13 loại nội dung 内容 và mã status tương ứng trong DB",
     "",
     "Điền đủ mã status vào khối r735-r748 theo §6.3 của spec, hoặc xóa khối trùng lặp."],

    ["MT-25", "TRUNG BÌNH", W,
     "Nhãn「キャンセル待ち 登録」và「キャンセルリクエスト」— khác nhau thế nào?",
     "「Quản lý calendar_new」r672 và r760 — kết quả mong đợi ghi: "
     "「**Trạng thái này khác gì trạng thái キャンセルリクエスト?**」— là CÂU HỎI.",
     "`feature-spec.md` §6.1:\n"
     "· `status = 3` `SB_REQUEST_BOOKING_WAIT_CANCEL` — 「キャンセル待ち」 đăng ký nhận thông báo "
     "khi có chỗ, nhãn hiển thị 「通知受取希望」, **KHÔNG chiếm chỗ**\n"
     "· `status = 5` `SB_REQUEST_BOOKING_CANCEL` — khách xin huỷ chờ Admin duyệt, "
     "nhãn 「リクエスト」, **CÓ chiếm chỗ**\n"
     "⚠ §6.1 còn cảnh báo: `0` và `5` **cùng hiện 「リクエスト」** dù ý nghĩa TRÁI NGƯỢC "
     "(xin đặt vs xin huỷ) ⇒ người vận hành không phân biệt được.",
     "2 trạng thái có ý nghĩa hoàn toàn khác nhau (1 là chờ có chỗ, 1 là xin hủy chỗ đã có) "
     "nhưng tên tiếng Nhật gần giống. Cộng thêm cảnh báo của spec về việc gộp nhãn 「リクエスト」, "
     "đây là rủi ro thao tác nhầm của admin.",
     "[Detail booking & lịch sử] Tab 予約履歴: 2 trạng thái dễ nhầm — キャンセル待ち登録 vs "
     "キャンセルリクエスト",
     "",
     "Chốt nhãn hiển thị cho từng status ở màn lịch sử. Cân nhắc đổi nhãn của status 0 và 5 "
     "để phân biệt (spec đã nêu là rủi ro vận hành)."],

    ["MT-27", "THẤP", W,
     "Màn refund: checkbox xác nhận chưa tích → nút bị DISABLE hay VALIDATE báo lỗi?",
     "「Quản lý calendar_new」ghi 2 hành vi KHÁC NHAU cho CÙNG tình huống:\n"
     "· r831 (booking bill UnivaPay):「**KHông check chọn confirm thì không cho phép click button "
     "refund**」(disable)\n"
     "· r844 (booking bill Stripe):「**Validate báo lỗi bắt buộc chọn vào checkbox**」",
     "`ui/ui-spec.md` SCR-LSN màn refund — spec không mô tả trạng thái nút khi chưa tích checkbox.",
     "Cùng 1 màn refund, 2 dòng TC mô tả 2 UX khác nhau. Nhiều khả năng chỉ 1 hành vi là đúng.",
     "[Hoàn tiền 返金] Refund: không tích checkbox xác nhận → không cho bấm nút refund",
     "",
     "Test thật 1 lần, chốt và sửa dòng còn lại."],

    ["MT-28", "THẤP", W,
     "Quan hệ 予約受付開始 / 予約締切: case 4 (start 23:59 kiểu giờ, end 2 ngày lúc 20h) chưa chốt",
     "「Setting calendar」r132:「case 4: time start: 23:59 · time end: 2 ngày lúc 20h」— "
     "**CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi**.\n"
     "3 case còn lại (r129-r131) đều có kết quả rõ: 2 case báo lỗi "
     "「予約締切は予約開始よりも後に設定してください」, 1 case save success.",
     "`web/logic-spec.md`: spec không nêu công thức so sánh khi 2 setting dùng KIỂU KHÁC NHAU "
     "(một bên 日数指定, một bên 時間指定).",
     "Case 4 là tổ hợp trộn 2 kiểu setting — đúng là chỗ dễ có bug nhất vì phải quy đổi về "
     "cùng đơn vị trước khi so sánh. TC gốc bỏ ngỏ đúng chỗ khó nhất.",
     "[予約の開始・締切] Quan hệ 予約受付開始 và 予約締切 — 4 tổ hợp",
     "",
     "Test case 4 và điền expected. Cân nhắc bổ sung thêm các tổ hợp trộn kiểu khác."],

    ["MT-30", "THẤP", W,
     "Ô 補足 của câu hỏi form: giới hạn 200 hay 50 ký tự?",
     "**Cùng tab「Setting calendar」ghi 2 con số khác nhau**:\n"
     "· r311-r312 (item 短文回答):「nhập: **validate 200 ký tự** ⇒ nhập ≤ 200 ⇒ save success; "
     "nhập > 200 ⇒ báo lỗi」\n"
     "· r351-r352 (item 長文回答), r381-r382 (radio), r454-r455 (checkbox), r486-r487 (日時): "
     "tiêu đề ghi「nhập: validate **200** ký tự」nhưng nội dung lại là「nhập ≤ **50** ký tự ⇒ "
     "save success; nhập > **50** ký tự ⇒ báo lỗi」",
     "`web/api-spec.md` EP-54 / `calendar_setting_send_forms.sub_question` — "
     "spec KHÔNG ghi giới hạn ký tự của trường 補足.",
     "4/5 loại item ghi mâu thuẫn NGAY TRONG CHÍNH DÒNG TC (tiêu đề 200, nội dung 50). "
     "Rất có thể là lỗi copy-paste khi soạn TC, nhưng member sẽ test sai.",
     "[予約時のお客様への質問項目] Item 短文回答: validate 質問内容 và 補足",
     "",
     "Test 1 lần cho 1 loại item, chốt con số, sửa đồng loạt 5 khối TC."],

    ["MT-31", "TRUNG BÌNH", W,
     "Marker 必須 / 任意: TC gốc ghi kết quả GIỐNG NHAU cho cả 2 nhánh",
     "「Setting calendar」r323 (default 必須) và r324 (chọn 任意) — **CẢ HAI đều ghi kết quả "
     "mong đợi y hệt**:「có marker **required** ở mục 2 · bên user required tương ứng」.\n"
     "Lỗi này lặp ở r353-r354 (item 長文回答), r383-r384 (radio), r456-r457 (checkbox), "
     "r488-r489 (日時).",
     "`feature-spec.md` §7 Field Traceability Matrix: `calendar_setting_send_forms.required` "
     "quyết định câu hỏi bắt buộc hay không; `logic-spec-public.md` mô tả message "
     "「回答を入力してください」khi bỏ trống câu bắt buộc.",
     "TC không phân biệt được 2 nhánh ⇒ member đọc sẽ tưởng chọn 任意 vẫn hiện marker 必須. "
     "Đây là lỗi soạn TC (copy-paste), lặp ở 5 loại item.",
     "[予約時のお客様への質問項目] Item: option 必須 / 任意 → marker ở khối 2 và required phía LINE user",
     "",
     "Sửa expected của nhánh 任意 thành「marker 任意, phía LINE user bỏ trống vẫn submit được」"
     "ở cả 5 khối."],

    ["MT-32", "TRUNG BÌNH", W,
     "Checkbox「すでに友だち情報が登録されている場合、初めから入力された状態にする」khi KHÔNG tích: "
     "có ghi lại câu trả lời không?",
     "**2 khối trong tab「Setting calendar」ghi kết quả khác nhau cho CÙNG tổ hợp** "
     "(option 自動生成 + KHÔNG tích checkbox + admin book):\n"
     "· r601:「**Lưu thay đổi, không hiển thị bên friend info**」\n"
     "· r618:「**Lưu thay đổi, không ghi lại câu trả lời**」",
     "`feature-spec.md` **BR-P36**: 🟠「Mỗi lần gửi form 「お客様情報」, hệ thống **GHI ĐÈ hồ sơ bạn bè** "
     "(`line_user` + `friend_information_values`), **trừ khi** `link_friend_information == 1`」"
     "⇒ nếu option là 自動生成 (không phải 1) thì VẪN GHI, chỉ là không hiển thị sẵn.",
     "「không hiển thị」và「không ghi lại」là 2 hành vi khác nhau về DỮ LIỆU. Spec đứng về phía r601 "
     "(vẫn ghi, chỉ không prefill). Nếu r618 đúng thì checkbox này điều khiển cả việc ghi DB — "
     "ảnh hưởng lớn tới hồ sơ bạn bè.",
     "[予約時のお客様への質問項目] Checkbox すでに友だち情報が登録されている場合… — 4 tổ hợp",
     "",
     "Test thật: bỏ tích checkbox, admin book, rồi query `friend_information_values`. "
     "Chốt và sửa 1 trong 2 dòng."],

    ["MT-33", "THẤP", W,
     "Format hiển thị remind SAU kiểu duration ghi chữ「前」thay vì「後」",
     "「Setting calendar」r858:「Remind sau khi kết thúc course · time send dạng duration ⇒ "
     "format: **コース終了 yy 時間 zz 分 前**」\n"
     "r870 lặp lại y hệt:「コース終了 yy 時間 zz 分 **前**」\n"
     "Trong khi remind sau kiểu ngày (r857) ghi đúng:「コース終了 xx日**後**の yy時zz分」",
     "`feature-spec.md` **BR-39**: `type_remind = 2` (đếm ngược) — "
     "「`sent = giờ **kết thúc** + HH:mm` (sau)」 ⇒ về mặt LOGIC là SAU, nên nhãn phải là「後」.",
     "Nhiều khả năng là typo trong TC, nhưng cũng có thể là bug hiển thị thật của hệ thống "
     "(nhãn hard-code). Admin setting remind gửi 2 giờ SAU buổi học nhưng màn hình ghi "
     "「2 時間 前」⇒ hiểu nhầm hoàn toàn.",
     "[リマインド — cài đặt] Format hiển thị mốc remind — 2 kiểu timing × trước/sau course",
     "",
     "Chụp màn hình thật màn setting remind. Nếu hệ thống hiện「前」⇒ raise bug hiển thị."],

    ["MT-34", "TRUNG BÌNH", W,
     "SpecImprove #36037: thứ tự remind TRƯỚC khi CÙNG SỐ NGÀY — TC gốc TỰ MÂU THUẪN",
     "「Setting calendar」r840 — kết quả mong đợi ghi **2 CÂU TRÁI NGƯỢC trong cùng 1 ô**:\n"
     "「**giờ lớn hơn hiện ở trên**」\n"
     "「**Giờ nhỏ hơn hiện ở trên**」",
     "`feature-spec.md` **BR-38**: `type_remind = 1` (theo ngày): "
     "`sent = (ngày buổi học + time_send) ∓ before_day`.\n"
     "SpecImprove #36037 (04/2026) chỉ ghi「Sửa lại thứ tự hiển thị remind send trước, "
     "remind nào được send trước thì cho lên đầu, remind nào gần giờ booking thì ở cuối」.",
     "Theo nguyên tắc「gửi trước thì lên đầu」: cùng số ngày TRƯỚC buổi học, giờ NHỎ HƠN được gửi "
     "trước ⇒ phải lên trên. Nhưng TC gốc ghi cả 2. Đây là điểm dễ FAIL nhất của ticket #36037.",
     "[リマインド — cài đặt] SpecImprove #36037: thứ tự hiển thị remind TRƯỚC course",
     "",
     "Suy từ nguyên tắc của ticket: cùng ngày thì giờ NHỎ hơn lên trên. Test xác nhận, "
     "xóa câu sai khỏi TC."],

    ["MT-35", "TRUNG BÌNH", W,
     "Nội dung mẫu remind chứa chuỗi CỨNG「1日前」/「昨日」— không đổi theo setting thật",
     "「Setting calendar」r919: mẫu remind TRƯỚC chứa「ご予約の**【1日前】**となりましたので」\n"
     "r959: mẫu remind SAU chứa「**昨日**はご来店、誠にありがとうございました。」\n"
     "Corpus KHÔNG có TC nào kiểm nội dung khi setting KHÁC 1 ngày.",
     "`feature-spec.md` **BR-43**:「Nội dung mặc định chứa chuỗi **văn bản cứng** "
     "「1日前」/「昨日」 — **không đổi** theo `before_day` thực tế」.",
     "Admin setting remind gửi 3 NGÀY trước buổi học, khách nhận tin ghi「ご予約の【1日前】となりました」"
     "⇒ khách hiểu nhầm ngày học, có thể tới sai ngày. Đây là lỗi ảnh hưởng trực tiếp khách hàng "
     "cuối nhưng chưa từng được test.",
     "[リマインド — cài đặt] Nội dung message remind: mẫu mặc định của remind TRƯỚC và SAU khác nhau",
     "",
     "Bổ sung TC: setting remind 3 ngày trước, chèn mẫu, cho user booking, kiểm tin nhận được. "
     "Nếu vẫn ghi「1日前」⇒ raise bug và cân nhắc thay bằng biến động."],

    ["MT-36", "TRUNG BÌNH", W,
     "空き枠通知 gửi ĐỒNG LOẠT cho mọi người đang chờ, không giới hạn và không thứ tự ưu tiên",
     "「Setting calendar」r1173:「sẽ send cho **all user có stt đang chờ** — "
     "**user nào booking trước thì dc (kể cả user mới)**」— coi là hành vi ĐÚNG.",
     "`feature-spec.md` **BR-33 / BR-P31**:「Gửi cho **mọi** booking `status = 3` của khung — "
     "**không giới hạn số lượng, không xếp thứ tự ưu tiên, gửi đồng loạt**; "
     "bản ghi `status = 3` **giữ nguyên** sau khi gửi」⇒ khớp corpus.",
     "Corpus và spec KHỚP, nhưng đây là rủi ro nghiệp vụ chưa được đánh giá: 1 chỗ trống mà "
     "50 người đang chờ ⇒ 50 người nhận tin, 49 người vào thì hết chỗ. Với khách hàng Nhật, "
     "đây là nguồn khiếu nại thường gặp. Ngoài ra BR-35 còn nói `saveSettingNotifyFull()` "
     "**luôn ép** `use_message_notify_not_full = 0` ⇒ **KHÔNG THỂ TẮT** tin này từ UI.",
     "[空き枠通知受け取り設定] Tab 受付再開時: gửi cho TẤT CẢ user đang chờ khi có chỗ trống",
     "",
     "Chốt: có cần giới hạn số người nhận / xếp thứ tự FIFO không. Đồng thời kiểm BR-35 "
     "(không tắt được tin 空き枠通知) có đúng không — nếu đúng thì raise bug."],

    ["MT-37", "THẤP", W,
     "Lịch sử 変更履歴 của 空き枠通知 CHỈ ghi khi bật/tắt, đổi nội dung KHÔNG để lại dấu vết",
     "「Setting calendar」r1259-r1260: lịch sử chỉ có 2 loại nội dung — "
     "「停止中→受付中 に変更」và「受付中→停止中 に変更」.\n"
     "Corpus KHÔNG có TC nào kiểm lịch sử khi đổi NỘI DUNG message hoặc action.",
     "`feature-spec.md` **BR-36**:「Chỉ ghi lịch sử khi `is_notify_full_slot` **đổi giá trị**; "
     "thay đổi **nội dung/action không** để lại dấu vết」⇒ khớp corpus.",
     "Khớp nhau nhưng là lỗ hổng audit: staff sửa nội dung tin nhắn gửi cho khách mà không ai "
     "truy vết được. Với tính năng có bill tiền và gửi tin hàng loạt, đây là rủi ro vận hành.",
     "[空き枠通知受け取り設定] Màn lịch sử 変更履歴 của setting 空き枠通知",
     "",
     "Chốt: có cần ghi lịch sử cho thay đổi nội dung không. Nếu có, raise ticket cải tiến."],

    ["MT-38", "CAO", W,
     "キャンセル用URL: sửa `booking_id` trên URL có hủy được booking của người khác không?",
     "「Setting calendar」r1235 (Bug KH #36729):「Truy cập Cancel URL không hợp lệ ⇒ "
     "**Hiển thị lỗi phù hợp; Không thay đổi dữ liệu DB**」— là kỳ vọng, chưa có bằng chứng chạy.",
     "`feature-spec.md` §6.5:「**LINE User (LIFF)** — 🔴 **KHÔNG CÓ xác thực** — chỉ cần biết "
     "`booking_id` (số nguyên tự tăng). **Không CSRF, không rate limit** (S-02, S-03)」.\n"
     "§11.2 **S-01**: `booking_id` tự tăng, **không kiểm chủ sở hữu, không kiểm "
     "`booking.calendar_id == calendar_id`**.",
     "Nếu spec đúng thì bất kỳ ai có 1 URL cancel hợp lệ đều có thể sửa `booking_id` thành số "
     "khác để HỦY BOOKING CỦA NGƯỜI KHÁC, xuyên cả bot. TC r1235 kỳ vọng chặn được nhưng "
     "chưa ai chạy.",
     "[空き枠通知受け取り設定] Bug KH #36729: truy cập キャンセル用URL bị sửa booking_id hoặc token",
     "",
     "Chạy TC này NGAY. Nếu hủy được booking người khác ⇒ raise ticket bảo mật mức Nghiêm trọng. "
     "Liên quan MT-63."],

    ["MT-40", "TRUNG BÌNH", W,
     "`store_name` có 0/174 bản ghi trong dump — màn top page phía LINE user có bị rỗng không?",
     "「Setting calendar」r1289 có sẵn 2 câu lệnh recover:\n"
     "`UPDATE calendar_management SET line_name = store_name WHERE store_name IS NOT NULL;`\n"
     "`UPDATE calendar_management SET store_name = line_name WHERE store_name IS NULL;`\n"
     "⇒ chứng tỏ đã biết vấn đề nhưng KHÔNG có TC kiểm kết quả sau recover.",
     "`feature-spec.md` **Gap G-10**:「`calendar_management.store_name` có **0/174 bản ghi** "
     "nhưng LIFF hiển thị `calendar.store_name` (M-4). Chưa xác nhận `CalendarController::index()` "
     "có gán từ `line_name` không. **Nếu không gán ⇒ màn top page LUÔN hiển thị rỗng**」.\n"
     "BR-08:「`store_name` gán bằng `line_name` lúc tạo; về sau ghi **cả hai cột cùng giá trị**」.",
     "Nếu recover chưa chạy trên production thì mọi calendar cũ đều hiển thị tên cửa hàng RỖNG "
     "ở màn đầu tiên khách nhìn thấy. Dump 2026-04-20 cho thấy 0/174 bản ghi có giá trị.",
     "[トップ・店舗情報・利用規約] Recover data 店舗名 cho calendar cũ · "
     "[Wizard tạo calendar] store_name được gán bằng line_name lúc tạo",
     "",
     "Query production `SELECT COUNT(*) FROM calendar_management WHERE store_name IS NULL`. "
     "Nếu > 0 ⇒ chạy recover và kiểm màn top page của vài calendar cũ."],

    ["MT-42", "TRUNG BÌNH", W,
     "`cancelGoogsheet()` xóa token nhưng KHÔNG reset `google_sheet_status`",
     "「Setting calendar」r1476-r1479 test hủy liên kết theo 4 trạng thái `google_sheet_status` "
     "(0/1/2/3) — chỉ trạng thái 2 hủy được.\n"
     "Corpus KHÔNG có TC nào kiểm giá trị `google_sheet_status` SAU KHI hủy liên kết thành công.",
     "`feature-spec.md` **BR-55**:「Google Sheet coi là **lỗi liên kết** khi có token nhưng "
     "`google_sheet_status = 0` ⇒ tự mở modal cảnh báo. **`cancelGoogsheet()` xoá token nhưng "
     "không reset status**」.",
     "Hủy liên kết ở trạng thái 2 ⇒ token bị xóa nhưng status vẫn = 2. Lần liên kết lại tiếp theo "
     "có thể rơi vào trạng thái không nhất quán (có status nhưng không token). Corpus có test "
     "liên kết lại (r1493-r1526) nhưng không kiểm cột status.",
     "[Googleスプレッドシート連携] Hủy liên kết Google theo 4 trạng thái google_sheet_status",
     "",
     "Bổ sung bước query `google_sheet_status` sau khi hủy vào TC. Nếu không reset ⇒ "
     "raise ticket."],

    ["MT-43", "CAO", W,
     "Phân quyền Staff cho FA-019: KHÔNG ai biết staff được cấp những route con nào",
     "Corpus có **6 dòng「Check account staff」rải rác** ở 5 tab khác nhau "
     "(Calendar list r63 · Quản lý calendar r62 · Quản lý course r73, r139 · "
     "Setting calendar r256, r1537 · Sửa bill tiền univapay r165 · Improve bill tiền stripe r61) — "
     "**TẤT CẢ đều CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi nào**.",
     "`feature-spec.md` **BR-56**: 🔴「Quyền Staff xét **theo tên route**. Hai cặp route **trùng tên** "
     "(`calendar.getListCalendar` tại `web.php:1518` & `:1520`; `save.setting.calendar.notify.full` "
     "tại `:3530` & `:3533`) ⇒ **cấp 1 tên là mở 2 URL**」.\n"
     "**Gap G-01** (mức tin cậy **Thấp**):「Dữ liệu `access_feature` / `bot_role_access` cho FA-019 — "
     "**Staff thực sự được cấp những route con nào** — nằm trong DB production, không có trong source」.\n"
     "§1.3:「**Không có một lệnh `checkHasPermission()` nào** trong 2 controller Admin (0/82 endpoint)」.",
     "Không có TC nào cho phân quyền staff, và spec cũng không xác minh được. Cộng thêm A-01 "
     "(17 route `/ajax/calendar/*` nằm ngoài cơ chế phân quyền) ⇒ toàn bộ mảng phân quyền của "
     "FA-019 là VÙNG MÙ hoàn toàn.",
     "[Phân quyền & môi trường] Account staff: các màn của レッスン予約 hiển thị và thao tác được · "
     "🔴 Staff bị cấm route レッスン予約 vẫn thao tác được qua nhóm /ajax/calendar/* · "
     "[Googleスプレッドシート連携] Account staff thao tác liên kết / hủy liên kết Google",
     "",
     "Chạy `SELECT id, route, parent FROM access_feature WHERE route LIKE 'calendar%'` trên "
     "production, lập bảng quyền, rồi viết TC cho từng route. Đồng thời kiểm 2 cặp route trùng tên "
     "của BR-56."],

    ["MT-44", "CAO", W,
     "Bot gói FREE: UI chặn bật bill tiền nhưng server VẪN THU TIỀN nếu client gửi cờ",
     "「Liên kết bill tiền」r6:「Account free enable liên kết bill tiền ⇒ **click enable bill tiền "
     "báo lỗi 決済機能のご利用には有料プランへのアップグレードが必要です。**」— chỉ test ở tầng UI.",
     "`feature-spec.md` **BR-P21**:「Bot gói `free` ⇒ `is_use_payment` bị ép `0` "
     "**chỉ trên object PHP, DB không đổi**. 🔴 **Client vẫn gửi `checkHasPayment=true` thì server "
     "vẫn thu tiền**」.",
     "Bot free từng bật bill tiền rồi bị hạ gói ⇒ `is_use_payment` trong DB vẫn = 1. "
     "Client (hoặc kẻ tấn công) gửi `checkHasPayment=true` là thu được tiền của khách trên bot "
     "không có quyền dùng tính năng thanh toán. Corpus chỉ test nút bấm trên UI.",
     "[決済連携 — cài đặt] Bot gói free bật bill tiền → chặn + message upgrade · "
     "[Đồng thời & verify API] 🔴 Verify API: client gửi checkHasPayment = false",
     "",
     "Query production đếm bot gói free có `is_use_payment = 1`. Chạy TC verify API. "
     "Liên quan MT-63."],

    ["MT-45", "TRUNG BÌNH", W,
     "Hủy liên kết cổng thanh toán sau khi đã có booking chờ approve: có còn thu tiền không?",
     "「Liên kết bill tiền」r59 — kết quả mong đợi ghi:「**vẫn bill tiền do có thông tin card ?**」"
     "— có **DẤU HỎI**, chưa chốt.",
     "`feature-spec.md` **BR-P20**: cổng do `calendar_management.type_payment` quyết định; "
     "**snapshot** vào `booking.payment_system` và `booking.environment` ⇒ "
     "booking đã lưu snapshot cổng nên VẪN thu được.\n"
     "**BR-52**: tab 決済連携 chỉ mở khi bot đã liên kết Stripe hoặc UnivaPay — spec không nói "
     "gì về booking đã tồn tại khi hủy liên kết.",
     "Nếu vẫn thu được thì admin hủy liên kết cổng vẫn tiếp tục bị trừ phí giao dịch mà không "
     "biết. Nếu không thu được thì booking treo vĩnh viễn ở trạng thái chờ approve.",
     "[決済連携 — cài đặt] Hủy liên kết cổng thanh toán SAU KHI calendar đã chọn cổng đó",
     "",
     "Test thật trên môi trường test, chốt hành vi. Cân nhắc cảnh báo admin trước khi hủy "
     "liên kết nếu còn booking chờ."],

    ["MT-46", "THẤP", W,
     "UnivaPay thẻ 4111 1111 1111 1111: message lỗi cụ thể là gì?",
     "·「Liên kết bill tiền」r130:「Check các case bill fail do user nhập vào card invalid "
     "nhập card 4111 1111 1111 1111 ⇒ **báo lỗi card ko tồn tại ?**」— có **DẤU HỎI**\n"
     "·「Sửa bill tiền univapay」r74:「Nhập card 4111 1111 1111 1111 ⇒ "
     "**Hiện tại đang báo lỗi luôn lúc submit card**」— mô tả hiện trạng, không phải kỳ vọng",
     "`feature-spec.md` §5.5 / BR-P23: thanh toán hỏng ở pha 1 ⇒ booking bị **xoá cứng** + đếm lại chỗ. "
     "Spec không liệt kê message lỗi cụ thể của UnivaPay.",
     "TC không nêu message chính xác ⇒ member không biết verify gì. Với thẻ Stripe thì corpus có "
     "message rõ (「Your card was declined」), UnivaPay thì không.",
     "[決済 — UnivaPay & webhook] UnivaPay: thẻ 4111 1111 1111 1111 → báo lỗi",
     "",
     "Chụp lại message thật của UnivaPay, ghi vào TC."],

    ["MT-47", "CAO", W,
     "UnivaPay: callback về TRƯỚC 2 phút — CÓ hay KHÔNG gửi msg「決済が完了しました。」?",
     "**Cùng tab「Sửa bill tiền univapay」ghi ngược nhau**:\n"
     "· r11 (callback < 2 phút, success):「send message báo bill success cho user 決済が完了しました。 "
     "**=> sửa lại case này không send message báo bill success nữa**」\n"
     "· r12 (callback < 2 phút, fail):「send message thanh toán fail **=> sửa lại case này "
     "không send msg này nữa**」\n"
     "· NHƯNG r15 (callback 3-5 phút, success):「- send message thanh toán thành công cho user "
     "**決済が完了しました。**」và r16 (fail): CÓ gửi msg fail\n"
     "· r26-r29 (luồng full slot) khẳng định rõ mốc 2 phút: **< 2 phút KHÔNG gửi, > 2 phút CÓ gửi**",
     "`feature-spec.md` **BR-P37**:「Xử lý > **120 giây** ⇒ gửi tin LINE trấn an (thành công) "
     "hoặc báo lỗi thẻ (thất bại)」⇒ KHỚP với r26-r29 (mốc 2 phút).",
     "3 khối TC trong cùng 1 tab mô tả 3 phiên bản khác nhau của cùng 1 quy tắc. Khối r26-r29 "
     "và spec BR-P37 khớp nhau (mốc 120 giây) ⇒ đây là bản đúng. Nhưng r11-r16 vẫn nằm trong tab "
     "và mâu thuẫn nội bộ.",
     "[決済 — UnivaPay & webhook] UnivaPay: callback về TRƯỚC 2 phút — 2 nhánh success/fail · "
     "Bug #29846: full slot rồi book lại — msg 決済が完了しました phụ thuộc mốc 2 phút",
     "",
     "Chốt theo BR-P37 (mốc 120 giây), sửa/xóa r11-r12 và r15-r16 cho khớp. "
     "Đây chính là gốc của Bug #29846 (「msg 決済が完了しました không trigger được từ đâu」)."],

    ["MT-48", "CAO", W,
     "UnivaPay: callback FAIL về SAU 5 phút — XÓA booking hay chuyển status = 7 (cancel)?",
     "「Sửa bill tiền univapay」r21 — kết quả mong đợi ghi **2 LOGIC CHỒNG NHAU**:\n"
     "「update thông tin booking như case bill lỗi phía trên nhưng **không xóa booking mà update "
     "status booking = cancel**: `payment_status` = 0, `status_webhook` = 2 + mã lỗi ⇒ "
     "check là bill lỗi update **status = 7, payment_status = 2** "
     "**=> sửa lại theo logic mới sẽ XÓA booking**」",
     "`feature-spec.md` **BR-P25**:「Webhook thất bại ⇒ `status = 7` + `payment_status = 2`; "
     "nếu `status_webhook` cũ là `3` (kèm `from_job`) **hoặc `4`** ⇒ **xoá cứng booking**」.\n"
     "⇒ Spec nói CẢ HAI đều đúng tùy `status_webhook` cũ: mặc định là chuyển status 7, "
     "còn nếu đã ở trạng thái 3 hoặc 4 thì XÓA CỨNG.",
     "TC gốc gộp 2 logic vào 1 ô mà không nêu điều kiện phân nhánh. Spec làm rõ điều kiện: "
     "`status_webhook` cũ quyết định. Vì `status_webhook` = 4 chính là trạng thái sau 5 phút "
     "không có callback ⇒ trong TC này (callback > 5 phút) thì XÓA CỨNG là đúng.",
     "[決済 — UnivaPay & webhook] UnivaPay: quá 2 phút chưa có callback → màn chờ; "
     "quá 5 phút → status_webhook = 4",
     "",
     "Viết lại r21 theo BR-P25 với điều kiện rõ ràng: mặc định status 7, "
     "nếu `status_webhook` cũ ∈ {3 (from_job), 4} thì xóa cứng."],

    ["MT-50", "CAO", W,
     "Webhook UnivaPay KHÔNG xác thực chữ ký / IP / secret — chỉ dựa vào bot_id trong metadata",
     "「Sửa bill tiền univapay」r118-r129 test rất kỹ nhánh `bot_id` trong metadata: "
     "callback đúng bot_id ⇒ update booking; callback sai bot_id ⇒ không update.\n"
     "Corpus KHÔNG có TC nào gửi callback GIẢ MẠO từ nguồn khác.",
     "`feature-spec.md` §6.5: **Webhook UnivaPay** — 🔴「**Không xác thực chữ ký / IP / secret** "
     "(RP-07)」.",
     "Nếu không xác thực nguồn thì bất kỳ ai biết `booking_id` và `bot_id` (mã hoá) đều có thể "
     "gửi callback giả với kết quả「thành công」⇒ booking được approve và gửi action mà không có "
     "giao dịch thật. Cơ chế bot_id trong metadata chỉ chống nhầm lẫn giữa các bot, "
     "không chống giả mạo.",
     "[決済 — UnivaPay & webhook] metadata trên UnivaPay có bot_id — callback sai bot_id thì "
     "KHÔNG update booking",
     "",
     "Bổ sung TC: gửi callback giả bằng curl với payload hợp lệ nhưng không phải từ UnivaPay. "
     "Nếu update được ⇒ raise ticket bảo mật. Liên quan MT-63."],

    ["MT-51", "TRUNG BÌNH", W,
     "Calendar liên kết UnivaPay nhưng THIẾU Webhook ID → chưa chốt hành vi",
     "「Sửa bill tiền univapay」r164:「Check setting không Webhook ID」— "
     "**CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi**.",
     "`feature-spec.md` **BR-P24**: UnivaPay có webhook ⇒ server poll **5 lần × 1s**; "
     "hết mà chưa có kết quả ⇒ `status_webhook = 4` + trả `pending`.\n"
     "**BR-52**: tab 決済連携 chỉ mở khi bot đã liên kết Stripe (`status_strip_bot = 3`) hoặc "
     "UnivaPay (có **cả** `univapay_app_id` và `univapay_app_test_id`) — spec KHÔNG nhắc Webhook ID.",
     "Nếu thiếu Webhook ID thì callback KHÔNG BAO GIỜ về ⇒ mọi booking có bill tiền đều rơi vào "
     "`status_webhook = 4` ⇒ bị khóa vĩnh viễn (MT-49). Đây là cấu hình sai dẫn tới hỏng toàn bộ "
     "luồng thanh toán nhưng chưa ai test.",
     "[決済 — UnivaPay & webhook] Setting không có Webhook ID → cần chốt hành vi",
     "",
     "Test thật, chốt: có chặn bật bill tiền khi thiếu Webhook ID không. Nếu không chặn thì "
     "phải có cảnh báo. Liên quan MT-49."],

    ["MT-53", "THẤP", W,
     "Preview OGP khi gửi link booking: TC gốc mô tả hành vi của「Calendar cũ」",
     "「Booking phía line user」r6:「**Calendar cũ**: Nếu nhập vào title và description thì sẽ hiển thị "
     "ở preview · Nếu ko nhập title và description => Thì sẽ hiển thị tên cửa hàng và system name "
     "ở preview」— nói về CALENDAR CŨ.",
     "`ui/ui-spec-liff.md` SCR-LSN-L01「トップページ」— spec mô tả ảnh + `description_top` "
     "nhưng KHÔNG mô tả OGP preview khi gửi link.\n"
     "`feature-spec.md` **M-2**: SCR-LSN-24 Preview 「トッププレビュー」 ⚠ hiển thị `description` "
     "thay vì `description_top` — **bug M-2**.",
     "TC mô tả hành vi của hệ thống calendar THẾ HỆ CŨ (đã bị gỡ khỏi tool từ 07/2025 — "
     "Feature #30540), chưa ai xác nhận với calendar lesson hiện tại. Cộng thêm bug M-2 "
     "(preview lấy nhầm cột) ⇒ preview có thể hiển thị sai nội dung.",
     "[LINE user — mở link & entry] Preview khi admin gửi link booking (OGP)",
     "",
     "Gửi thử link booking lesson qua chat 1:1, chụp preview thật, viết lại TC. "
     "Đồng thời kiểm bug M-2 (preview-top hiển thị `description` hay `description_top`)."],

    ["MT-55", "TRUNG BÌNH", W,
     "Nút「今日」: TC cũ và TC mới mô tả 2 hành vi NGƯỢC NHAU",
     "·「Task nhỏ + fix bug KH」r34, r45 (03/2025):「check user nhấn nút 今日 ⇒ "
     "**hiện tuần gần nhất có lịch làm việc**, giống case khi mở vào màn booking mới」\n"
     "·「Booking phía line user」r307-r318 (SpecImprove #32887, **11/2025 — mới hơn**):"
     "「Hiện tại: Khi click today sẽ nhảy đến tuần next hợp lệ như khi mới vào calendar. "
     "**Expect sau khi fix: Click today thì về tuần chứa today kể cả ko có lịch lv/ đã limit**」",
     "`web/logic-spec-public.md:942` **BR-P06**:「Khi tuần/tháng đang xem không có slot nào, "
     "server **tự nhảy** tối đa 4 tuần / 2 tháng」— spec mô tả cơ chế NHẢY nhưng KHÔNG nói "
     "cơ chế này có áp dụng cho nút 今日 hay không.",
     "SpecImprove #32887 chính là ticket ĐỔI hành vi này. TC cũ ở tab「Task nhỏ」chưa được cập nhật "
     "⇒ member đọc nhầm sẽ báo FAIL. Spec cũng chưa ghi rõ giới hạn phạm vi của BR-P06.",
     "[LINE user — chọn 受付枠] SpecImprove #32887: nút 今日 LUÔN về tuần/tháng chứa hôm nay · "
     "Review #29331: nút next/back và nút 今日 sau khi đã tự nhảy",
     "",
     "Đánh dấu lỗi thời cho r34/r45 ở tab「Task nhỏ + fix bug KH」. Bổ sung vào BR-P06 câu "
     "「cơ chế nhảy CHỈ áp dụng lúc mới mở calendar, không áp dụng cho nút 今日」."],

    ["MT-57", "TRUNG BÌNH", W,
     "Copy booking (同じ内容で予約): 6/7 trạng thái booking nguồn KHÔNG có kết quả mong đợi",
     "「Booking phía line user」r109-r115 và r149-r155:\n"
     "· r109 (booking đang đợi approve):「**Làm giống tương tự bên booking calendar**」"
     "— dẫn chiếu sang tính năng KHÁC, không nêu kết quả\n"
     "· r110 (booking đã approve):「chọn course sẵn và nhảy ra mh slot của course đó」— có kết quả\n"
     "· r111-r115 (denied · request cancel · đã cancel · đăng ký chờ hủy · đã hoàn thành): "
     "**CHỈ CÓ TIÊU ĐỀ**",
     "`ui/ui-spec-liff.md` SCR-LSN-L14「予約履歴」(chi tiết) — spec ghi có nút 「同じ内容で予約」 "
     "nhưng KHÔNG mô tả hành vi theo từng trạng thái booking nguồn.",
     "Nút copy hiện ở mọi booking trong lịch sử. Với 6/7 trạng thái không ai biết kết quả đúng "
     "là gì ⇒ member không test được. Đặc biệt trạng thái「đăng ký chờ hủy」rất mơ hồ "
     "(copy 1 đăng ký chờ hủy nghĩa là gì?).",
     "[LINE user — lịch sử & copy] Copy booking (同じ内容で予約) — 7 trạng thái booking nguồn",
     "",
     "Test đủ 7 trạng thái, điền expected. Cân nhắc ẩn nút copy ở các trạng thái không có ý nghĩa."],

    ["MT-59", "TRUNG BÌNH", W,
     "Booking「đợi nhận thông báo」ở QUÁ KHỨ: LINE user có xóa được không?",
     "**Cùng tab「Booking phía line user」ghi ngược nhau**:\n"
     "· r95:「check booking đã là quá khư ⇒ **không hiển thị button để xóa booking**」\n"
     "· r102:「Check xóa booking **quá khứ** ⇒ **User xóa booking thành công**」\n"
     "(cặp mâu thuẫn lặp lại ở r162 và r172 của khối màn tháng)",
     "`feature-spec.md` §6.3 **T-08**: `status = 3` → LINE User gọi `EP-P14` nhánh 1 — "
     "「通知受け取りを解除」(màn L20) ⇒ **xoá mềm**. Spec KHÔNG nêu điều kiện thời gian.",
     "Nếu nút bị ẩn với booking quá khứ thì TC r102 không thực hiện được. 2 dòng nằm cách nhau "
     "7 dòng trong cùng khối TC ⇒ chắc chắn 1 trong 2 sai.",
     "[LINE user — キャンセル待ち] Feature #35707: LINE user tự xóa booking đợi nhận thông báo",
     "",
     "Test thật, chốt và xóa dòng sai. Lưu ý booking chờ hủy ở quá khứ không còn ý nghĩa "
     "nghiệp vụ nên ẩn nút là hợp lý."],

    ["MT-62", "THẤP", W,
     "TC NEW-06 nhắc「event trên Google Calendar」— nhưng FA-019 KHÔNG có tích hợp Google Calendar",
     "「Booking phía line user」r569 (NEW-06, TC do AI viết trong đợt Bug KH #38280): "
     "bước kiểm gồm「5. Kiểm **Google Calendar**」và expected「KHÔNG có event trên **Google Calendar**」.",
     "`feature-spec.md` §1.2: 🔴「**Điểm phải nhớ khi đọc spec**: FA-019 **KHÔNG có bất kỳ tích hợp "
     "Google Calendar nào**. Đã kiểm chứng bằng 2 nguồn độc lập: (a) `job-spec.md` §12 — "
     "`GoogleCalendarEventTask` chỉ thao tác trên `b_c_*` và `calendar_salon*`; "
     "(b) `db-mapping.md` §0 — cột `calendar_management.google_calendar_id` "
     "**174/174 bản ghi đều NULL**. **Tin cậy: Cao**」.",
     "TC yêu cầu kiểm 1 tích hợp KHÔNG TỒN TẠI ở FA-019 (chỉ FA-020 salon mới có). "
     "Member sẽ mất thời gian tìm hoặc báo kết quả vô nghĩa. Kho TCs đã đổi thành Google Sheet.",
     "[Đồng thời & verify API] NEW-06: user THUA cuộc không được nhận bất kỳ side-effect nào",
     "",
     "Sửa TC NEW-06 ở tab gốc: thay「Google Calendar」bằng「Google Sheet」. "
     "Rà lại các TC khác của lesson xem có nhắc Google Calendar không."],

    ["MT-64", "TRUNG BÌNH", W,
     "Backup rich menu chứa link booking lesson: link trỏ về calendar của BOT GỐC hay bot đích?",
     "「add link salon và lesson」r82:「Check backup rich menu ⇒ **back up được rich menu; "
     "add rich menu cho user hiển thị được và action được bình thường**」— "
     "KHÔNG nêu link trỏ về calendar nào.",
     "`feature-spec.md` §12.4 phụ thuộc hạ tầng: link booking mang dạng "
     "`https://liff.line.me/{liffId}?calendar_id={id}` — `calendar_id` là **id cụ thể của calendar**.\n"
     "Spec FA-019 KHÔNG mô tả hành vi khi rich menu được backup sang bot khác.",
     "Nếu link giữ nguyên `calendar_id` của bot gốc thì friend của bot ĐÍCH bấm vào sẽ mở "
     "trang booking của bot GỐC ⇒ rò rỉ dữ liệu chéo bot và đặt nhầm lịch. "
     "Đây đúng kiểu lỗi đã ghi nhận ở FA-033 Backup (action リマインド còn trỏ id bot gốc).",
     "[Add link booking vào tin nhắn] Support #26549: backup rich menu có chứa link lesson",
     "",
     "Test thật: backup rich menu A→B, bấm vào action mở link, kiểm `calendar_id` trên URL. "
     "Nếu trỏ bot gốc ⇒ raise bug rò rỉ dữ liệu chéo bot."],

    ["MT-65", "TRUNG BÌNH", W,
     "FA-019 dùng CHUNG bảng `calendar_salon_setting_send_messages` với FA-020",
     "「Setting calendar」r135, r150-r151 (setting giới hạn số lần đặt/khách của LESSON) ghi rõ "
     "cột lưu là **`calendar_salon_setting_send_messages.text_limit_book_each_customer`** — "
     "tức là bảng của SALON.\n"
     "Corpus KHÔNG có TC hồi quy nào kiểm việc sửa setting lesson có ảnh hưởng salon không.",
     "`feature-spec.md` §12.2: 🔴「**Phụ thuộc THẬT vào FA-020「サロン・面談予約」**」.\n"
     "§1.2 lại khẳng định 2 tính năng dùng **bảng chính KHÁC NHAU** "
     "(`calendar_management`/`calendar_course*` vs `calendar_salon*`).",
     "Spec vừa nói 2 tính năng độc lập về bảng chính, vừa nói có phụ thuộc THẬT. Corpus xác nhận "
     "ít nhất 1 cột của lesson nằm trong bảng salon. Nếu 2 tính năng ghi vào cùng bản ghi ⇒ "
     "sửa setting lesson có thể phá setting salon của cùng bot.",
     "[Phân quyền & môi trường] Hồi quy: thao tác trên lesson KHÔNG ảnh hưởng salon và event booking · "
     "[1人あたりの予約上限] Validate ô nhập giới hạn và text hiển thị khi đạt giới hạn",
     "",
     "Đọc §12.2 của spec để lấy danh sách ĐẦY ĐỦ các điểm dùng chung với FA-020. "
     "Viết TC hồi quy 2 chiều cho từng điểm. Ưu tiên vì bot có cả lesson và salon là phổ biến."],

    ["MT-16", "CAO", W,
     "`POST /{id}/edit` (đổi 管理名) là IDOR ghi + mass assignment lên toàn bộ calendar_management",
     "「Calendar list」r52, r58-r61: chỉ test đổi 管理名 ở tầng UI "
     "(hiện tên hiện tại · required · biên 10/11 ký tự · tiếng Nhật).\n"
     "Corpus KHÔNG có TC nào gửi thêm trường ngoài 管理名 vào body.",
     "`feature-spec.md` §11.1 TOP-3 (**A-02**): 🔴「**IDOR ghi + mass assignment trên "
     "`POST /{id}/edit`** (EP-29). Route nằm **ngoài** `checkLessonCalendarInBot`; "
     "`editCalendar()` = `where('id',$id)->update($request->all() trừ 'id')` — "
     "**không lọc `bot_id`, không validate trường nào**. Endpoint này chỉ để đổi 「管理名」 "
     "nhưng cho phép sửa **tuỳ ý** bản ghi của **bot khác**: đặt `bot_id`, `is_use_payment`, "
     "`environment`, `google_sheet_access_token`, `code_delete`…」",
     "Một endpoint tưởng như vô hại (đổi tên quản lý) lại cho phép chiếm quyền toàn bộ calendar "
     "của bot khác, gồm cả token OAuth Google và mã xóa hệ thống. Corpus chỉ test đúng "
     "chức năng bề mặt.",
     "[Màn list calendar] Popup đổi 管理名 — hiện tên hiện tại, sửa & lưu thành công · "
     "[Đồng thời & verify API] 🔴 Verify API: POST /{id}/edit là mass assignment",
     "",
     "Chạy TC verify API. Raise ticket A-02 mức Nghiêm trọng. Yêu cầu dev: đưa route vào "
     "middleware `checkLessonCalendarInBot` và whitelist trường được phép sửa. Liên quan MT-63."],

    ["MT-06", "TRUNG BÌNH", W,
     "Giới hạn số COURSE trên 1 lịch: corpus nói「không giới hạn」, spec nói trần cứng 200",
     "「Quản lý course」r20-r24:「plan free ⇒ chỉ tạo dc **2 course**; "
     "**plan standard ⇒ ko giới hạn course**; **plan pro ⇒ ko giới hạn course**」",
     "`feature-spec.md` **BR-04**:「Khoá học tối đa: `bots.plan_type = 2` (free) → **2**/lịch; "
     "**gói khác → trần cứng 200/lịch**」.",
     "Corpus (05/2024) chưa biết tới trần 200. Nếu trần 200 là đúng thì admin tạo course thứ 201 "
     "sẽ bị chặn mà TC hiện tại nói「không giới hạn」⇒ member báo FAIL oan. "
     "So sánh: FA-020 salon có hard limit 200 course / 200 staff / 100 câu hỏi (08/2025) — "
     "nhiều khả năng lesson cũng được áp cùng đợt.",
     "[Giới hạn theo plan] Plan standard / pro: TC gốc nói không giới hạn số course — "
     "cần verify trần cứng 200",
     "",
     "Test tạo course thứ 201 trên bot standard. Chốt con số và cập nhật TC. "
     "Kiểm luôn giới hạn 100 câu hỏi form (BR-05) — corpus cũng không có TC."],
]
