# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: 11.1 TCsLine_SalonCalendar (25 tab) + TCsLine_Limit all tính năng → tab「Limit Salon」.
Nguồn spec: spec-features/admin/salon-booking/ (feature-spec.md · web/logic-spec.md · web/api-spec.md ·
            job/job-spec.md · db/db-mapping.md · ui/ui-spec.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "TRUNG BÌNH", W,
     "Plan free: 2 calendar bất kỳ loại hay 1 mỗi loại?",
     "「Calendar list」r23-r30: bot free đã có 1 calendar 個人 → màn chọn loại TỰ NHẢY sang loại "
     "スタッフ; nếu cố chọn 個人 rồi next thì báo lỗi upgrade plan. Bộ đếm: filter 全て = n/2, "
     "個人 = n/1, スタッフ = n/1 → tức là **tối đa 1 MỖI LOẠI**.",
     "`feature-spec.md:33` §1.4 bảng hạn chế theo plan ghi free =「**2 tổng (bất kỳ loại)**」.\n"
     "`feature-spec.md:BR-01` lại ghi「Tối đa 2 calendars (tổng cộng, **tối đa 1 mỗi loại**)」.",
     "Spec TỰ MÂU THUẪN giữa §1.4 và BR-01. Nếu member đọc §1.4 sẽ nghĩ tạo 2 calendar 個人 là hợp lệ "
     "→ báo PASS khi hệ thống chặn, hoặc báo FAIL khi hệ thống cho tạo. TCs khẳng định BR-01 đúng.",
     "[Giới hạn theo plan] Plan free: tối đa 1 個人 + 1 スタッフ · Bộ đếm 登録カレンダー数",
     "",
     "Sửa `feature-spec.md` §1.4 cho khớp BR-01 (free = 1 個人 + 1 スタッフ), hoặc ngược lại."],

    ["MT-02", "CAO", W,
     "Bot plan cũ (flag_contract_new = 0) có bị giới hạn số calendar / course / staff không?",
     "Có **2 khối TC nói ngược nhau trong CÙNG tab「Calendar list」**:\n"
     "· r39-r40:「plan pro — **không giới hạn số calendar**; tạo calendar thứ 11 → **cho phép**」\n"
     "· r46-r54: bot `flag_contract_new` = 0 — free = 2 calendar/2 course/2 staff; "
     "**standard và pro =「Không giới hạn」cả calendar, course và staff**\n"
     "· r58-r73 (khối SAU trong cùng tab): plan pro = **tối đa 10 個人 + 10 スタッフ**, "
     "tạo cái thứ 11 → **báo lỗi**; bộ đếm hiện n/20.\n"
     "Ngoài ra「Quản lý course&staff」r129-r159 (08/2025, MỚI HƠN) đặt **hard limit 200 course / "
     "200 staff / 100 câu hỏi** cho MỌI plan.",
     "`feature-spec.md` BR-01: standard cũ / pro / enterprise_pro = **10 個人 + 10 スタッフ**.\n"
     "`feature-spec.md` BR-02: free = 2 course + 2 staff; **mọi plan: hard limit 200 course, "
     "200 staff**; form 100 câu hỏi.\n"
     "Spec KHÔNG nhắc gì đến trường hợp `flag_contract_new` = 0 được「không giới hạn」.",
     "Đây là hành vi người dùng cuối (KH plan cũ có tạo được calendar/course thứ 11, thứ 201 hay không). "
     "Nếu member chạy theo khối r39-r54 sẽ báo FAIL đúng lúc hệ thống chặn hợp lệ — hoặc tệ hơn, "
     "bỏ qua case biên 200 hoàn toàn. Niên đại: khối「không giới hạn」cũ hơn khối 10/10 và hard limit 200.",
     "[Giới hạn theo plan] Plan pro / standard cũ: tối đa 10 個人 + 10 スタッフ · "
     "Hard limit 200 course / 200 staff / 100 câu hỏi",
     "",
     "Chốt bảng giới hạn cuối cùng cho từng plan × `flag_contract_new`; bổ sung vào BR-01/BR-02 "
     "và ghi rõ trường hợp plan cũ."],

    ["MT-03", "CAO", W,
     "Xóa ca làm việc có xóa các booking liên quan không?",
     "· 「Quản lý calendar」r711-r716 (khối CŨ, 2024): xóa ca có booking ở status "
     "deny/cancel/admin-book → hiện confirm, **xóa ca VÀ xóa luôn booking liên quan** "
     "(update `calendar_salon_line_booking.deleted_at`); riêng r710 (admin book) ghi ngược lại: "
     "「xóa lịch làm việc **KHÔNG** xóa booking liên quan」.\n"
     "· r724: các booking bị xóa sẽ vào màn「削除済み予約」.\n"
     "· r3023-r3028 (Bug #29394, **30/03/2025 — MỚI HƠN**):「Check sau khi **bỏ logic** ⇒ "
     "xóa lịch lv sẽ **ko xóa booking**」— ticket phát sinh vì nhiều booking của KH bị xóa nhầm.",
     "`feature-spec.md` BR-12 CHỈ nói: không thể xóa shift nếu còn booking「予約確定」.\n"
     "Spec **KHÔNG mô tả** điều gì xảy ra với booking ở các trạng thái khác khi shift bị xóa.\n"
     "`feature-spec.md` §3.1: `calendar_salon_line_booking` có SoftDelete = Có.",
     "Đây là hành vi phá dữ liệu của khách. Nếu logic cũ còn sót ở nhánh nào đó, xóa 1 ca có thể "
     "xóa hàng loạt booking (đúng như Bug #29394 đã xảy ra thật). Corpus có 2 khối kết luận ngược nhau, "
     "khối mới nói ĐÃ BỎ logic xóa booking nhưng khối cũ vẫn nằm trong bộ TC đang dùng.",
     "[Booking đã xóa] Booking bị xóa do xóa ca làm việc · "
     "[Dữ liệu cũ & hồi quy] Bug #29394: xóa ca làm việc KHÔNG được xóa booking",
     "",
     "Chốt hành vi hiện tại; nếu đã bỏ logic xóa booking thì **loại khối TC r711-r716** khỏi bộ chạy "
     "và bổ sung BR mới vào `feature-spec.md` (kèm ghi chú status 13「受付枠削除による予約削除」còn dùng "
     "cho trường hợp nào)."],

    ["MT-04", "CAO", W,
     "Rule ghi đè / hợp nhất ca làm việc: gộp, ghi đè hay chặn?",
     "Corpus có **4 rule chồng lên nhau theo thời gian**:\n"
     "· SpecChange #28381 (19/02/2025):「add lịch lv từ **merge time ⇒ ghi đè**」\n"
     "· SpecChange #29379 (27/03/2025):「add 9-12h thì **xóa** lịch 13-17h」— và ghi rõ "
     "「chỉ sửa case **add mới / import csv**」\n"
     "· Bug #32568 (27/10/2025): 2 khung **liền nhau** phải **BÁO LỖI** yêu cầu gộp "
     "(「シフトの時間が連続する場合は、合算して登録してください」); khung cách nhau ≥ 1 phút thì tạo 2 ca\n"
     "· #38520 r91-r93 (07/2026): thêm ca chồng giờ ca đã có →「hoặc ghi đè, hoặc gộp, hoặc chặn — "
     "hành vi phải rõ ràng」(để ngỏ cả 3 khả năng)\n"
     "· #38520 r24: import CSV ghi đè ca còn booking →「hoặc ghi đè thành công, hoặc chặn」(để ngỏ)",
     "`feature-spec.md` §2.2 (Modal「シフト追加」) chỉ ghi 1 câu:「Cảnh báo: Nếu đã có shift → "
     "sẽ bị **overwrite**」.\n"
     "Spec KHÔNG có rule hợp nhất ca liên tiếp, KHÔNG phân biệt add-mới vs edit-trực-tiếp, "
     "KHÔNG mô tả hành vi khi ghi đè cắt vào booking 予約確定.",
     "Đây là nhóm thao tác admin dùng hàng ngày và là nguồn của ít nhất 4 ticket. Chưa chốt thì "
     "member không biết case nào PASS: cùng 1 thao tác「thêm ca chồng giờ」có thể mong đợi ghi đè, "
     "gộp, hoặc báo lỗi. Rule còn KHÁC NHAU giữa add mới / edit / import CSV.",
     "[Ca làm việc — thêm & ghi đè] Bug #32568 2 khung liền nhau · Ghi đè xóa ca cũ · "
     "[Ca làm việc — sửa & xóa] Rút ngắn/kéo dài 1 trong 2 ca · [Ca làm việc — CSV] Import ghi đè",
     "",
     "Chốt 1 bảng rule duy nhất: (add mới | edit | import CSV) × (liền nhau | chồng lấn | rời nhau) "
     "× (có | không có booking 予約確定). Bổ sung vào §2.2 và BR mới; ghi rõ 24:00 và 00:00 quy về "
     "cùng 1 giá trị."],

    ["MT-05", "TRUNG BÌNH", W,
     "Tên course vượt độ dài: báo lỗi, tự cắt, hay cho 100 ký tự?",
     "· 「Calendar list」r195-r196 (wizard tạo calendar): 50 ký tự OK, **51 ký tự → BÁO LỖI**\n"
     "· 「Quản lý course&staff」r238-r239 (màn コース作成・編集): 50 ký tự OK, "
     "**51 ký tự → TỰ CẮT còn 50**\n"
     "· Tên calendar ở popup tạo:「> 30 ký tự → **tự động cắt HOẶC báo lỗi**」(r93 — corpus "
     "chính nó cũng chưa chốt)",
     "`feature-spec.md` Field Matrix #32:「コース名 → `calendar_salon_course.course_name`, "
     "**varchar(100)**, bắt buộc」.\n"
     "Field #1: `calendar_salon.calendar_name` **varchar(100)**, bắt buộc.",
     "3 nguồn ra 3 con số/hành vi khác nhau (spec 100 · TCs 50 báo lỗi · TCs 50 tự cắt). "
     "Người dùng cuối nhìn thấy hành vi khác nhau giữa 2 lối vào cùng tạo 1 course. "
     "Tự cắt âm thầm còn nguy hiểm hơn báo lỗi vì KH mất chữ mà không biết.",
     "[Tạo calendar — wizard] Wizard tạo course validate tên · "
     "[コース — tạo/sửa/xóa] Validate tên course TỰ CẮT",
     "",
     "Chốt độ dài tối đa thật (50 hay 100) và hành vi thống nhất (báo lỗi hay tự cắt) cho CẢ 2 lối vào; "
     "sửa Field Matrix #32 và #1 cho khớp."],

    ["MT-06", "TRUNG BÌNH", W,
     "Ca qua ngày khi ngày kế tiếp đã đặt là 休業日: cho phép hay chặn?",
     "· 「Calendar list」r176, r279:「Lịch T7 CN setting là ngày nghỉ, add lịch T6 qua ngày → "
     "**Add success** nhưng chỉ hiển thị đến hết T6; T7 vẫn là ngày nghỉ」\n"
     "· 「Quản lý calendar」r2429 (cùng chủ đề, có ghi chú CONFIRM):「nếu đã add t7 cn là ngày nghỉ "
     "khi add lịch qua ngày sẽ **báo lỗi** t7 là ngày nghỉ nên cần t6 chỉ add đc lịch đến…」\n"
     "· r2500:「Đang confirm: sẽ **validate** nếu ngày 15 đã setting nghỉ thì ngày 14 chỉ đc add "
     "lịch lv đến 0h ngày 15」",
     "Spec KHÔNG có rule nào về tương tác giữa ca qua ngày và ngày nghỉ kế tiếp. "
     "Field #21 chỉ mô tả `is_day_off` 0/1.",
     "Cùng 1 thao tác, corpus có 2 kết quả ngược nhau (add success vs báo lỗi) và 1 dòng ghi rõ "
     "「đang confirm」— tức là chưa từng chốt. Ảnh hưởng trực tiếp việc KH có set được ca đêm "
     "trước ngày nghỉ hay không.",
     "[Tạo calendar — wizard] Ngày T7/CN là ngày nghỉ, thêm ca qua ngày cho T6",
     "",
     "Chốt hành vi; nếu chọn「validate chặn」thì bổ sung message lỗi và cập nhật §2.2 + Field #21."],

    ["MT-07", "THẤP", W,
     "Bảng ánh xạ status của booking chưa có trong feature-spec",
     "Corpus định nghĩa rõ 8 giá trị và cách nhóm hiển thị:\n"
     "· 「Quản lý calendar」r1340-r1344: status 0,5 →「リクエスト」· 1,2 →「予約確定」· 3 →「通知受取希望」· "
     "4,7 →「キャンセル」· 6 →「否認済」\n"
     "· r840-r845: filter 予約確定 = status 1,2; リクエスト中 = 0; キャンセルリクエスト中 = 5; "
     "キャンセル = 4,7; 全選択 = 0,1,2,4,5,7 (KHÔNG gồm 3 và 6)\n"
     "· r2311-r2324: bảng ánh xạ 13 giá trị status của `..._history_actions`",
     "`feature-spec.md` Field #10 chỉ ghi「Enum 0-7」và trỏ sang `db/db-mapping.md`; "
     "phần §2.2a chỉ nói「map status → text JP (xem Enum §3.2)」nhưng §3.2 của feature-spec là "
     "「Queue Tables」, KHÔNG phải bảng enum.",
     "Tham chiếu chéo trong spec bị trỏ sai mục. Member đọc feature-spec sẽ không tra được ý nghĩa "
     "từng status, dễ hiểu nhầm khi verify bộ đếm và filter.",
     "[Detail booking & lịch sử] Nhãn trạng thái ở tab lịch sử · Mã status trong bảng lịch sử · "
     "[Modal filter booking & shift] Filter theo 予約ステータス",
     "",
     "Sửa tham chiếu §3.2 trong feature-spec; đưa bảng enum 8 status + 13 history status vào "
     "feature-spec hoặc trỏ đúng sang db-mapping."],

    ["MT-08", "TRUNG BÌNH", W,
     "Cài đặt hiển thị tên khách chưa áp dụng đúng ở modal admin thêm booking",
     "「Quản lý calendar」r168-r175: với 3/4 tuỳ chọn hiển thị tên "
     "(システム表示名/LINE名 · chỉ LINE名 · chỉ システム表示名), cột kết quả ghi "
     "**「modal admin add booking NG」** — riêng tuỳ chọn mặc định LINE名/システム表示名 ghi OK. "
     "Ghi chú: case user KHÔNG có system name chỉ hiện line name.",
     "`feature-spec.md` Field #11:「お名前 ← `name` hoặc `line_user_name`, "
     "**`setting_display_line_name` quyết định**」— không phân biệt màn nào.\n"
     "EP-54 `change-display-line-name` không mô tả phạm vi áp dụng.",
     "TC gốc đã ghi nhận NG nhưng vẫn nằm trong bộ đang dùng và không có ticket đi kèm. "
     "Nếu member chạy lại sẽ báo FAIL — cần biết đây là bug chưa fix hay là hành vi cố ý "
     "(modal admin luôn hiện LINE name để admin nhận diện khách).",
     "[Calendar theo ngày] Modal 表示変更（LINE名/システム表示名）",
     "",
     "Xác nhận còn NG không; nếu là hành vi cố ý thì ghi ngoại lệ vào Field #11, nếu là bug thì "
     "raise ticket."],

    ["MT-09", "TRUNG BÌNH", W,
     "Ngày KHÔNG có ca: lưới tuần hiện「không thể book」, lưới tháng hiện「có thể book」",
     "「Quản lý calendar」:\n"
     "· r548 (lưới TUẦN):「ko có thời gian làm việc → hiển thị icon **ko thể book**」\n"
     "· r597 (lưới THÁNG):「ko có thời gian làm việc → hiển thị icon **có thể book**」\n"
     "· r598-r599 (lưới THÁNG): staff setting ngày nghỉ, kể cả các staff khác không có ca → "
     "vẫn **có thể book**\n"
     "· r1250 (thứ tự ưu tiên lý do): nhánh「Ko có giờ lv + chưa đến time booking」ghi "
     "「QL ngày OK · QL tuần OK · **QL tháng NG**」",
     "Spec KHÔNG mô tả quy tắc hiển thị icon của lưới tuần/tháng, cũng không nói 2 lưới có quy tắc "
     "khác nhau. §2.2b chỉ nói「theo displayMode: day/week/month」dùng 3 service khác nhau.",
     "3 lưới cùng dữ liệu nhưng ra 3 kết quả khác nhau. Admin nhìn lưới tháng tưởng ngày đó đặt được, "
     "bấm vào thì không. Corpus cũng tự đánh dấu NG cho lưới tháng ở nhánh thứ tự ưu tiên lý do.",
     "[Calendar theo tuần] Icon có thể/không thể book · [Calendar theo tháng] Icon theo trạng thái ca · "
     "[Modal lý do không đặt được] Thứ tự ưu tiên lý do",
     "",
     "Chốt quy tắc icon thống nhất cho 3 lưới; bổ sung vào §2.2b và ui-spec."],

    ["MT-10", "CAO", W,
     "Thứ tự ưu tiên action: course/staff hay action chung của booking?",
     "「Quản lý calendar」r883-r887 và r1115-r1118 mô tả quy tắc 4 nhánh:\n"
     "· course + staff set message và **CÓ sử dụng** → gửi action của course/staff\n"
     "· course + staff **CHỈ set message và chọn KHÔNG sử dụng** → gửi action **CHUNG của booking**\n"
     "· course + staff chỉ set multi action → gửi của course/staff\n"
     "· set cả message + multi action → gửi của course/staff\n"
     "Ngoài ra r1181-r1191:「action của course/staff CHỈ có 2 mốc — lúc booking được duyệt ngay và "
     "lúc admin duyệt request」; các mốc khác (deny, cancel) KHÔNG dùng action course/staff.",
     "`feature-spec.md` §8.1 chỉ nói SC-004 Action Settings được dùng ở「Per-course action "
     "(`action_id_send_after_booking`, `action_id_send_approve_booking`); Per-staff action tương tự」.\n"
     "**KHÔNG có Business Rule nào mô tả thứ tự ưu tiên** giữa action course/staff và action chung.",
     "Đây là hành vi người dùng cuối nhận thấy trực tiếp (nhận tin gì khi đặt lịch). Nhánh "
     "「chỉ set message + chọn không sử dụng thì fallback về action chung」rất phản trực giác và "
     "không có ở bất kỳ đâu trong spec — nếu dev refactor sẽ mất mà không ai phát hiện.",
     "[リクエスト一括操作] Duyệt hàng loạt khi course/staff có action riêng · "
     "[LINE user — nhập form & xác nhận] Course/staff có action riêng · Luồng REQUEST",
     "",
     "Bổ sung BR mới vào `feature-spec.md`: bảng ưu tiên action (4 nhánh × các mốc booking), "
     "ghi rõ mốc nào KHÔNG áp dụng action course/staff."],

    ["MT-11", "TRUNG BÌNH", W,
     "Validate số điện thoại 11 chữ số: 10 chữ số pass hay fail?",
     "「Quản lý calendar」r1053: mô tả validate 電話番号（11桁ハイフンなし）:\n"
     "「Nhập vào số 10 chữ số → Báo lỗi 携帯電話11桁の数値を入力してください。 "
     "**(cho pass giống lesson)**」— vế trước nói báo lỗi, ghi chú trong ngoặc lại nói cho pass.\n"
     "12 chữ số → báo lỗi (OK) · 11 chữ số → pass (OK).",
     "Spec KHÔNG mô tả các kiểu validate của câu hỏi friend info trong màn đặt lịch salon "
     "(Field #47 chỉ ghi「question, text, bắt buộc」).",
     "Ngay trong 1 ô Expected có 2 kết luận trái ngược. Số cố định của Nhật có 10 chữ số nên đây là "
     "case KH gặp thật. Không chốt thì member không biết PASS hay FAIL khi nhập 10 số.",
     "[Admin thêm booking thủ công] Validate 短文回答 theo 4 kiểu ràng buộc",
     "",
     "Chốt: 10 chữ số pass hay fail; đồng bộ với hành vi ở Lesson calendar và ở màn friend info; "
     "bổ sung bảng validate vào spec."],

    ["MT-12", "CAO", W,
     "現地決済 (thanh toán tại chỗ): thiếu hoàn toàn trong spec",
     "Corpus mô tả đầy đủ một tính năng con:\n"
     "· 「Quản lý calendar」r2781-r2809: bật「chọn được cả thanh toán trước và tại chỗ」; "
     "LINE user chọn tại chỗ → booking ở trạng thái「現地決済：未決済」; admin cập nhật thành "
     "「現地決済：決済済み」từ 2 màn; có lịch sử cập nhật\n"
     "· r2823-r2825: modal filter thêm 2 trạng thái, ánh xạ `payment_time` = 2 và "
     "`payment_status` = 0 / 1\n"
     "· 「Setting calendar」r1571-r1581: cột 決済ステータス trong Google Sheet",
     "`feature-spec.md` §9.1 mục 1 ghi đây là **Gap**:「Payment status 「現地決済」và "
     "「現地（決済成功）」xuất hiện trên UI SCR-SLN-02a nhưng **không có constants trong source code** "
     "(chỉ có SP_NOT_PAYMENT=0, SP_PAYMENT=1, SP_NO_PAYMENT=2, SP_REFUND=3). Không rõ giá trị DB thực tế.」\n"
     "Field #15 ghi「Enum 0-3 (+4,5 **chưa xác nhận**)」.",
     "Spec đang bỏ ngỏ đúng phần liên quan đến TIỀN. TCs đã chỉ ra cơ chế thật là tổ hợp "
     "`payment_time` + `payment_status` chứ KHÔNG phải thêm giá trị 4/5 vào `payment_status` — "
     "tức giả định trong spec (+4,5) nhiều khả năng SAI.",
     "[現地決済] toàn bộ nhóm · [Modal filter booking & shift] Filter thêm 2 trạng thái 現地決済",
     "",
     "Đóng Gap §9.1 mục 1: ghi rõ 現地決済 = `payment_time` = 2, trạng thái phân biệt bằng "
     "`payment_status` 0/1; bỏ giả định「+4,5」ở Field #15; bổ sung mục 現地決済 vào §2.5."],

    ["MT-13", "CAO", W,
     "Admin đặt lịch bỏ qua TOÀN BỘ validate — không có trong spec",
     "「Quản lý calendar」r1020 (ghi ngay ở tiêu đề khối):「ADMIN BOOK THÌ SẼ KO CẦN VALIDATE - "
     "GIỜ ĐÓ STAFF CÓ LÀM VIỆC KO - STAFF CÓ THỰC HIỆN COURSE ĐÓ KO」.\n"
     "r1143-r1148: admin book thành công kể cả khi — staff không có ca · staff đã đạt 受付上限 · "
     "calendar đã đạt 受付上限 · khách đã đạt giới hạn số lần đặt · khung trùng block time Google · "
     "course đang bật 決済 (không bill, không tính phí).\n"
     "Test limit booking_V4_2 r46-r95: nhưng booking do admin tạo **VẪN ĐƯỢC TÍNH vào limit**.",
     "`feature-spec.md` §2.2「Luồng thêm đặt lịch thủ công」chỉ mô tả các trường input và "
     "`booking_by` = 1; **KHÔNG có dòng nào** nói admin bỏ qua validate.\n"
     "Không có BR nào cho hành vi này.",
     "Đây là quy tắc nghiệp vụ cốt lõi, ảnh hưởng cả limit và tiền. Không có trong spec nghĩa là "
     "một dev mới hoàn toàn có thể「sửa cho đúng」bằng cách thêm validate → phá luồng đặt hộ của KH. "
     "Đồng thời điểm「admin book bỏ validate NHƯNG vẫn tính vào limit」rất dễ bị hiểu ngược.",
     "[Admin thêm booking thủ công] Admin book KHÔNG bị chặn bởi mọi ràng buộc · "
     "[受付上限 — 店舗・スタッフ] Admin book cưỡng chế vẫn được tính vào limit",
     "",
     "Bổ sung BR mới:「Admin booking bỏ qua toàn bộ validate đặt lịch nhưng vẫn được tính vào "
     "受付上限」; ghi rõ vào §2.2 và EP-10."],

    ["MT-14", "THẤP", W,
     "Booking đã xóa chỉ hiển thị trong 90 ngày — không có trong spec",
     "「Quản lý calendar」r2293:「Check những booking đã bị xóa quá **90 ngày** ⇒ sẽ không hiển thị "
     "ở màn hình lịch sử xóa. Hiện tại đang tính từ ngày quá khứ — VD hôm nay 17/7/2024 thì những "
     "booking có `delete_at` 17/4/2024 sẽ không hiển thị」.",
     "Spec KHÔNG có rule retention nào cho màn「削除済み予約」. EP-53 `get-list-booking-delete` "
     "không mô tả điều kiện lọc theo thời gian.",
     "KH có thể cần tra cứu booking đã xóa quá 90 ngày (khiếu nại, đối soát). Không ghi trong spec "
     "thì không ai biết dữ liệu bị ẩn hay bị xóa hẳn.",
     "[Booking đã xóa] Booking xóa quá 90 ngày không còn hiển thị",
     "",
     "Bổ sung rule retention vào EP-53 + §2.2; xác nhận dữ liệu chỉ bị ẨN hay bị xóa vật lý."],

    ["MT-15", "THẤP", W,
     "Giới hạn số ngày chọn cùng lúc khi thêm ca — chưa có giá trị cụ thể",
     "#38520 r39:「Giới hạn số lượng: chọn nhiều ngày cùng lúc và import CSV ở mức **biên / biên+1** "
     "→ ở đúng biên lưu thành công; vượt biên chặn rõ ràng, không lưu một phần」— "
     "nhưng KHÔNG ghi giá trị biên là bao nhiêu.",
     "Spec KHÔNG có giới hạn nào cho số ngày chọn cùng lúc ở modal thêm ca, cũng không giới hạn "
     "số dòng của file CSV import.",
     "TC không chạy được vì thiếu con số. Nếu thực tế KHÔNG có giới hạn thì cần biết để test "
     "hiệu năng ở mức lớn (chọn cả năm) thay vì tìm biên không tồn tại.",
     "[Ca làm việc — thêm & ghi đè] Chọn nhiều ngày ở mức biên và biên+1",
     "",
     "Xác định giá trị biên thực tế (hoặc xác nhận không có giới hạn) và bổ sung vào EP-19/EP-34."],

    ["MT-16", "TRUNG BÌNH", W,
     "Ca qua ngày ở BIÊN ĐẦU mùa vụ hiển thị lệch giữa admin và LINE user",
     "「Quản lý calendar」r2492:「setting mùa vụ 10/8-20/8, add lịch lv qua ngày 9/8 ⇒ đầu ngày 10/8 "
     "vẫn hiển thị icon đặt được **NG**」— cột kết quả ghi「admin: QL ngày **OK** · "
     "user: tuần/tháng **NG**」.\n"
     "r2493 (biên cuối) thì cả admin và user đều OK.",
     "Spec KHÔNG mô tả tính năng 期間限定 (mùa vụ) ở mức business rule; §2.4 không có mục này.",
     "Admin thấy đặt được, LINE user thấy không (hoặc ngược lại) ở đúng ngày đầu mùa vụ. "
     "TC gốc đã đánh NG nhưng không kèm ticket — cần biết đã fix chưa.",
     "[Ca làm việc — qua ngày & biên 00:00] Ca qua ngày × setting mùa vụ ở 2 biên",
     "",
     "Verify lại trên môi trường hiện tại; bổ sung mục 期間限定 (mùa vụ) vào spec §2.4 kèm rule biên."],

    ["MT-17", "TRUNG BÌNH", W,
     "Import CSV ca làm việc KHÔNG validate tên cột",
     "「Quản lý calendar」r989:「Cột trong file không để đúng name column → "
     "**sai tên cột vẫn cho vào, dev đang lấy theo thứ tự cột**」.",
     "`feature-spec.md` EP-34 `import-csv-staff` không mô tả cơ chế đọc file, "
     "không nói validate header.",
     "KH tự sửa file (đổi tên cột, đảo cột) sẽ tạo ca sai giờ mà hệ thống không cảnh báo — "
     "dữ liệu hỏng âm thầm. Đây là rủi ro dữ liệu, không chỉ là thiếu tiện nghi.",
     "[Ca làm việc — CSV] Import CSV KHÔNG validate tên cột",
     "",
     "Quyết định có bổ sung validate header không; nếu giữ nguyên thì ghi rõ cảnh báo trong "
     "màn import và trong EP-34."],

    ["MT-18", "TRUNG BÌNH", W,
     "Ma trận hiển thị giá course/staff (4 tổ hợp) không có trong spec",
     "「Quản lý course&staff」r5-r10 mô tả đủ ma trận:\n"
     "· Bật 決済: LUÔN hiện phí course, bất kể cờ\n"
     "· Tắt 決済 (0,0): không hiện phí course ở màn chọn/detail course, không hiện phí tổng\n"
     "· (1,0): hiện phí course, KHÔNG hiện phí staff, **VẪN hiện phí tổng (course+staff)** ở màn khác\n"
     "· (0,1): không hiện phí course, có hiện phí staff, vẫn hiện phí tổng\n"
     "· (1,1): hiện phí course và phí tổng",
     "`feature-spec.md` Field #37 chỉ ghi:「display_course_cost 0/1 — **Bắt buộc hiện khi bật payment**」.\n"
     "`display_staff_cost` **không có trong Field Traceability Matrix**.",
     "Nhánh (1,0) và (0,1) rất phản trực giác: tắt hiển thị 1 loại phí nhưng phí TỔNG vẫn hiện ở "
     "các màn khác — KH tưởng đã ẩn giá nhưng thực tế vẫn lộ. Spec thiếu cả 1 field.",
     "[コース — list & menu] Ma trận hiển thị giá course/staff theo 決済 và 2 cờ display_*_cost",
     "",
     "Bổ sung `display_staff_cost` vào Field Matrix và ghi ma trận 4 tổ hợp thành BR mới."],

    ["MT-19", "TRUNG BÌNH", W,
     "Copy staff có copy ca làm việc không? Xóa staff còn booking thì xử lý thế nào?",
     "· 「Quản lý course&staff」r456-r466 (Check copy staff): corpus KHÔNG ghi rõ ca làm việc "
     "có được copy hay không\n"
     "· r467 (Check xóa staff): không mô tả điều kiện chặn\n"
     "· #38520 r46:「Xóa nhân viên đang có ca + booking 予約確定 → hệ thống **hoặc chặn** xóa với "
     "thông báo rõ, **hoặc cho xóa** và hiển thị trạng thái『đã xóa』ở mọi nơi tham chiếu」— để ngỏ",
     "`feature-spec.md` EP-30 `deleteCalendarStaff` ghi「Xóa nhân viên (**force delete**)」.\n"
     "BR-10 chỉ mô tả trường hợp ẩn staff (status = 0), KHÔNG mô tả xóa.\n"
     "Không có BR nào cho copy staff.",
     "「force delete」trong spec nghĩa là xóa cứng — mâu thuẫn với khả năng「hiển thị trạng thái "
     "đã xóa ở mọi nơi tham chiếu」mà TC nêu. Nếu xóa cứng staff còn booking thì các màn tham chiếu "
     "`staff_id` sẽ hỏng.",
     "[スタッフ — list & tạo/sửa/xóa] Copy staff · Xóa staff còn booking chưa cancel",
     "",
     "Chốt: (a) copy staff có kèm ca làm việc không; (b) xóa staff còn booking 予約確定 — chặn hay "
     "cho xóa; bổ sung BR và sửa mô tả EP-30."],

    ["MT-20", "CAO", W,
     "Tính năng スタッフ自動割り当て (random staff) không có trong spec",
     "「Quản lý calendar」r2503-r2880 (Feature #27976, 01/2025) mô tả đầy đủ:\n"
     "· 3 tuỳ chọn: (1) không tự phân công · (2) random tự do · (3) theo thứ tự ưu tiên\n"
     "· Danh sách thứ tự ưu tiên độc lập với thứ tự ở màn QL staff (Bug #32588)\n"
     "· Điều kiện staff khả dụng: có ca · đang ON · thực hiện được course · chưa đạt limit · "
     "không vướng block time / vùng nghỉ\n"
     "· Lịch sử ghi thêm bản ghi 指定なし自動割り当て / 手動スタッフ変更 / 手動割り当て (Review #29803)\n"
     "· Khác biệt admin vs LINE user ở mốc thời gian nhận booking",
     "`feature-spec.md` chỉ nhắc 2 job Laravel `CalendarSalonStaffAssignment` và "
     "`CalendarSalonStaffAssignmentAdmin` trong §7.2 với 1 dòng mô tả「Phân công nhân viên tự động」.\n"
     "**KHÔNG có màn hình, không có BR, không có field** nào cho 3 tuỳ chọn và thứ tự ưu tiên.",
     "Đây là một trong những tính năng phức tạp nhất của salon (≥ 350 TC lá trong corpus, ≥ 5 ticket) "
     "nhưng gần như vô hình trong spec. Bất kỳ ai đọc spec để estimate hay để review sẽ bỏ sót hoàn toàn.",
     "[スタッフ自動割り当て] toàn bộ nhóm (11 TC)",
     "",
     "Bổ sung 1 mục mới vào `feature-spec.md` §2.4 cho スタッフ自動割り当て: 3 tuỳ chọn, field DB, "
     "điều kiện staff khả dụng, thứ tự ưu tiên, lịch sử; bổ sung Field Matrix."],

    ["MT-21", "TRUNG BÌNH", W,
     "受付上限 option 3 đặt LỚN HƠN tổng limit các staff thì tính thế nào?",
     "「Quản lý calendar」r2863-r2878 (SpecChange #32679):「option random 2 - option limit 3 = **4** "
     "(3 staff, mỗi staff limit = 1)」— corpus có khối test nhưng KHÔNG ghi rõ kết quả mong đợi "
     "cuối cùng là chặn ở 3 hay ở 4.",
     "`feature-spec.md` §2.4.4 chỉ có `limit` (0/1) và `limited_quantity`; "
     "KHÔNG mô tả quan hệ giữa limit cửa hàng và tổng limit staff.",
     "Nếu hệ thống cho đặt đến 4 trong khi chỉ có 3 staff mỗi người 1 chỗ thì booking thứ 4 chắc chắn "
     "không có ai phục vụ. Đây là lỗi nghiệp vụ ảnh hưởng KH cuối.",
     "[スタッフ自動割り当て] SpecChange #32679 ma trận random option × limit option",
     "",
     "Chốt: hệ thống lấy min(limit cửa hàng, tổng limit staff khả dụng) hay lấy đúng số đã nhập; "
     "bổ sung vào §2.4.4."],

    ["MT-22", "CAO", W,
     "受付上限 có 4 tuỳ chọn nhưng spec chỉ mô tả 2 giá trị",
     "Corpus mô tả 4 tuỳ chọn:\n"
     "· option 1 — đếm theo số staff, tách **1.1** (1 staff xuyên suốt 1 booking) và **1.2** "
     "(nhiều staff nối tiếp); calendar tạo mới mặc định 1.1, calendar cũ mặc định 1.2 "
     "(「Quản lý calendar」r3117-r3173)\n"
     "· option 2 — 上限を設定しない\n"
     "· option 3 — 上限を設定する (nhập số); V4_2 (02/2026) sửa để **đếm cả booking ngoài giờ làm việc**\n"
     "· tuỳ chọn 上限をその時間に受付可能なスタッフ数の合計にする (「Setting calendar」r1773-r1849)",
     "`feature-spec.md` §2.4.4 và Field #46: `calendar_salon_setting_limit_booking` — "
     "`limit` (**0 = unlimited, 1 = limited**), `limited_quantity`, `setting_staffs_limit` (JSON per-staff).\n"
     "Chỉ có 2 trạng thái, KHÔNG có option 1.1/1.2 và KHÔNG có tuỳ chọn tổng-limit-staff.",
     "Đây là logic quyết định KH có đặt được lịch hay không — phần được test nhiều nhất trong corpus "
     "(> 2500 TC lá ở các tab Test limit booking V1→V4). Spec mô tả thiếu 2 tuỳ chọn và toàn bộ "
     "nhánh 1.1/1.2 → không thể dùng spec để review hay estimate.",
     "[受付上限 — 店舗・スタッフ] 4 tuỳ chọn và giá trị mặc định · Option 1.1 vs 1.2 · "
     "Tuỳ chọn 上限をその時間に受付可能なスタッフ数の合計にする",
     "",
     "Viết lại §2.4.4: liệt kê đủ 4 tuỳ chọn, giá trị DB tương ứng, quy tắc mặc định theo ngày tạo "
     "calendar, và rule đếm của từng option (kèm thay đổi V4_2 về booking ngoài giờ)."],

    ["MT-23", "THẤP", W,
     "Lý do hiển thị khi khung giờ bị chặn bởi block time Google",
     "「Quản lý calendar」r289 (Bug #26908, 14/10/2024): "
     "「Setting limit = 1, ở khung giờ trong ảnh đang hiển thị lý do **Đã limit** ⇒ Sửa để coi lịch "
     "của GG như blocktime giống bên Calendar」— nhưng corpus KHÔNG ghi text lý do đúng phải là gì.",
     "Spec KHÔNG có danh sách các lý do của modal「予約が追加できない日時」.",
     "TC không kiểm chứng được vì không biết text mong đợi. Thứ tự ưu tiên lý do là thông tin quan "
     "trọng để admin hiểu vì sao không đặt được.",
     "[受付上限 — 店舗・スタッフ] Bug #26908 block time Google · "
     "[Modal lý do không đặt được] Thứ tự ưu tiên lý do",
     "",
     "Bổ sung danh sách đầy đủ các lý do + text JP + thứ tự ưu tiên vào spec (§2.2b hoặc ui-spec)."],

    ["MT-24", "THẤP", W,
     "Slot cuối ngày: event Google có bị trừ thời gian nghỉ trước, booking LME thì không?",
     "「Booking phía line user」:\n"
     "· r1297 (booking LME, chỉ set nghỉ TRƯỚC):「slot cuối cùng = time end cửa hàng - time của "
     "course = 16:00」\n"
     "· r1305 (event Google, chỉ set nghỉ TRƯỚC):「slot cuối cùng = time end cửa hàng - time của "
     "course **- time nghỉ trước** = 16:00」\n"
     "Công thức khác nhau nhưng kết quả ví dụ lại ghi cùng 16:00.",
     "Spec §2.4.3 chỉ liệt kê 4 field `time_before`, `time_after`, `time_before_google`, "
     "`time_after_google`; KHÔNG có công thức tính slot.",
     "Hoặc là 1 trong 2 dòng viết sai công thức, hoặc booking LME và event Google thật sự tính khác "
     "nhau. Không chốt thì member không biết slot cuối ngày mong đợi là mấy giờ.",
     "[前後の空き時間] Slot đầu/cuối ngày KHÔNG bị trừ thời gian nghỉ · "
     "Event sync từ Google được xử lý y hệt booking LME",
     "",
     "Chốt 1 công thức duy nhất cho slot đầu/cuối ngày; bổ sung công thức vào §2.4.3."],

    ["MT-25", "THẤP", W,
     "Ô số ngày của 予約締切: nhập 0 nhưng lưu thành 1?",
     "「Setting calendar」r211:「Validate số ngày từ 0 ~ 180 — Nhập vào **0** → Save success ⇒ "
     "Kiểm tra db: `deadline_before_booking_day` = **1**」.\n"
     "r213: bỏ trống → lỗi「0日から入力してください」(tức 0 là hợp lệ).",
     "Spec Field #40 chỉ ghi「start_receive_booking_type + before_booking_day/hour — Complex」; "
     "không mô tả khoảng giá trị hợp lệ của `deadline_before_booking_day`.",
     "Nhập 0 mà lưu 1 nghĩa là hạn hủy/hạn nhận lệch đi 1 ngày so với KH cài — ảnh hưởng trực tiếp "
     "việc KH có đặt/hủy được hay không.",
     "[予約の開始・締切] Validate số ngày dừng nhận (0~180)",
     "",
     "Verify lại giá trị lưu trong DB khi nhập 0; nếu là bug thì raise ticket, nếu cố ý thì ghi rõ "
     "vào Field #40."],

    ["MT-26", "TRUNG BÌNH", W,
     "Text lỗi khi khách đạt giới hạn số lần đặt — 2 chuỗi khác nhau",
     "「Setting calendar」:\n"
     "· r238:「báo lỗi: **この予約の受付制限中ですので、予約できません。**」\n"
     "· r239-r242 (Spec update **2026-03-26**, SpecImprove #35407): calendar cũ chưa set text "
     "`text_limit_book_each_customer` → báo lỗi「**1人あたりの予約受付上限に…**」; calendar có set text "
     "thì hiện text tuỳ chỉnh\n"
     "· 「Booking phía line user」r1239 (luồng verify API) lại dùng chuỗi đầu tiên.",
     "Spec Field #39-#40 và §2.4.1 có `limit_book_each_customer`, `number_limit_booking`, "
     "`text_limit_book_each_customer` nhưng **không ghi text mặc định**.",
     "Cùng 1 tình huống (khách vượt giới hạn) nhưng 2 chuỗi lỗi khác nhau ở 2 thời điểm và 2 luồng "
     "(chọn slot vs bấm xác nhận). Member không biết chuỗi nào là đúng hiện tại.",
     "[1人あたりの予約上限] Text báo lỗi khi đạt giới hạn · "
     "[Đồng thời & verify API] Verify lại dữ liệu ở bước xác nhận",
     "",
     "Chốt text mặc định hiện tại cho từng luồng (chọn slot / bấm xác nhận); ghi vào §2.4.1."],

    ["MT-27", "TRUNG BÌNH", W,
     "Câu hỏi kiểu 日時 CÓ giờ + chọn 自動で友だち情報を生成 — xử lý ra sao?",
     "· 「Quản lý calendar」r1090:「Friend info có cả time ⇒ **Case này sẽ ko thể gán vào friend info "
     "nào trong hệ thống cả**」\n"
     "· 「Setting calendar」r793 (Support #29272, 23/03/2025): tiêu đề ticket ghi「Nếu chọn "
     "**自動で友だち情報を生成して回答を記録** và 日時 thì…」— tức là có nhánh TỰ SINH friend info, "
     "không phải chỉ「không gán được」.",
     "Spec Field #47-#48 chỉ mô tả `question` và `required`; KHÔNG mô tả các kiểu câu hỏi và "
     "cơ chế liên kết friend info.",
     "2 nguồn nói khác nhau về cùng 1 cấu hình. Nếu hệ thống vẫn cho chọn nhưng không lưu được thì "
     "KH mất dữ liệu câu trả lời mà không biết.",
     "[予約時のお客様への質問項目] Support #29272 item 日時 CÓ giờ",
     "",
     "Chốt hành vi (chặn cấu hình / tự sinh friend info kiểu ngày / lưu mất phần giờ); "
     "bổ sung mục các kiểu câu hỏi vào spec §2.4."],

    ["MT-28", "THẤP", W,
     "Thứ tự sắp xếp remind cùng ngày: giờ lớn hơn hay nhỏ hơn ở trên?",
     "「Setting calendar」r998 (nhóm remind TRƯỚC, các remind chỉ định NGÀY, **cùng ngày**):\n"
     "「**giờ lớn hơn hiện ở trên** Giờ nhỏ hơn hiện ở trên」— 2 câu ngược nhau trong CÙNG 1 ô Expected.",
     "Spec BR-08 chỉ mô tả công thức tính `sent_date_time`; KHÔNG có rule sắp xếp hiển thị.\n"
     "SpecImprove #36037 (22/04/2026) là ticket về thứ tự hiển thị nhưng chưa được đưa vào spec.",
     "Ô Expected tự mâu thuẫn → không kiểm chứng được. Thứ tự hiển thị remind ảnh hưởng việc admin "
     "hiểu đúng lịch gửi.",
     "[リマインド — cài đặt] SpecImprove #36037 thứ tự sắp xếp remind",
     "",
     "Chốt quy tắc sắp xếp cho cả 2 nhóm (trước/sau) × 2 kiểu thời gian; bổ sung vào BR-08."],

    ["MT-29", "CAO", W,
     "Job remind có gửi khi course / staff đang OFF không?",
     "「Setting calendar」— 2 khối kết luận NGƯỢC NHAU trong cùng 1 tab:\n"
     "· r1355:「Course đã chọn bị OFF ở MH setting course ⇒ **Thời điểm send remind mà course đang "
     "OFF thì sẽ không send**」; r1361 tương tự cho staff; r1373-r1375:「Đến thời điểm remind "
     "course/staff bị OFF ⇒ **Không send**」\n"
     "· r1382-r1389 (khối SAU, thuộc「Check job send remind」— sau Bug #30544 ngày 02/07/2025): "
     "remind KHÔNG filter →「**Luôn send** remind cho all booking」kể cả course OFF / staff OFF; "
     "remind CÓ filter →「**luôn send** remind cho các booking có course & staff thỏa mãn filter」"
     "ở cả 4 tổ hợp ON/OFF.",
     "Spec BR-08 mô tả filter theo `course_ids` / `staff_ids` khi `is_use_filter` bật; "
     "§7.1.2 mô tả `isUseFilter` 0/1/2/3.\n"
     "**KHÔNG có dòng nào** nói trạng thái ON/OFF của course/staff ảnh hưởng việc gửi remind.",
     "Đây là hành vi người dùng cuối: KH đã đặt lịch có nhận được nhắc lịch hay không khi admin tạm "
     "ẩn course. Nếu chạy theo khối cũ, member sẽ báo FAIL đúng lúc hệ thống gửi (hành vi mới đúng) "
     "— hoặc ngược lại, bỏ lọt case KH không nhận được nhắc lịch. Niên đại: khối r1382+ MỚI HƠN.",
     "[リマインド — job gửi] Job gửi remind khi course/staff bị OFF",
     "",
     "Chốt hành vi hiện tại; **loại hoặc sửa khối TC r1355/r1361/r1373-r1375**; bổ sung vào BR-08 "
     "câu rõ ràng về ảnh hưởng của trạng thái ON/OFF."],

    ["MT-30", "TRUNG BÌNH", W,
     "空き枠通知: gửi cho TẤT CẢ người đang chờ, ai đặt trước thì được",
     "「Setting calendar」r1433-r1437:「khi slot full mà user đăng ký chờ có slot trống thì sẽ send "
     "action này ⇒ sẽ **send cho all user có stt đang chờ**, user nào booking trước thì được」.\n"
     "2 điều kiện kích hoạt: (1) có user cùng slot hủy (được duyệt ngay); (2) admin **nâng số lượng "
     "slot** lên.\n"
     "r1437: nếu tắt chức năng thì user đang chờ KHÔNG nhận được thông báo nữa, "
     "nhưng booking chờ vẫn giữ nguyên trạng thái.",
     "`feature-spec.md` §2.4.5 chỉ có 1 dòng:「受付上限の通知 — EP-55/EP-56 — `is_notify_full_slot`, "
     "`message_notify_full_slot`」.\n"
     "KHÔNG mô tả cơ chế gửi, điều kiện kích hoạt, hay việc gửi cho tất cả người chờ.",
     "Cơ chế「gửi cho tất cả, ai nhanh thì được」ảnh hưởng trải nghiệm KH cuối và có thể gây khiếu nại "
     "(nhận thông báo nhưng vào thì hết chỗ). Không có trong spec nên không ai review được.",
     "[空き枠通知受け取り設定] Action gửi khi có slot trống (受付再開時)",
     "",
     "Bổ sung mô tả đầy đủ cơ chế 空き枠通知 vào §2.4.5: điều kiện kích hoạt, phạm vi gửi, "
     "hành vi khi tắt chức năng."],

    ["MT-31", "THẤP", W,
     "2 màn upload ảnh dùng 2 message lỗi khác nhau cho cùng 1 lỗi định dạng",
     "「Setting calendar」:\n"
     "· r1474 (tab **トップ設定**): file không phải ảnh / ảnh .avif → "
     "「**png, jpg, gif画像を選択してください。**」\n"
     "· r1519 (tab **店舗・ビジネス情報**): cùng tình huống → "
     "「**ファイルの形式が正しくありません。**」\n"
     "「Quản lý course&staff」r249 (form course): dùng chuỗi thứ hai.",
     "Spec KHÔNG có bảng message validate cho upload ảnh.",
     "Không nhất quán trải nghiệm. Ngoài ra chuỗi thứ nhất liệt kê 3 định dạng nhưng corpus lại ghi "
     "jpeg cũng hợp lệ → text có thể sai.",
     "[トップ・店舗情報・利用規約] Upload ảnh ở tab トップ設定 và 店舗・ビジネス情報",
     "",
     "Chốt 1 message thống nhất và danh sách định dạng chính xác; bổ sung bảng message vào spec."],

    ["MT-32", "TRUNG BÌNH", W,
     "店舗名: 30 hay 100 ký tự?",
     "「Setting calendar」:\n"
     "· r1477:「Check setting tên cửa hàng 店舗名 ⇒ **Change spec: 100 ký tự**」\n"
     "· r1481:「Nhập vào tên cửa hàng valid với **30 ký tự** ⇒ Update success」\n"
     "· r1484:「Nhập vào **31 ký tự** ⇒ Báo lỗi **店舗名は30文字以内で入力してください。**」",
     "`feature-spec.md` Field #1: `calendar_salon.calendar_name` **varchar(100)**, bắt buộc.\n"
     "Spec không có field `store_name` riêng trong Field Matrix (chỉ nhắc trong §2.4.5).",
     "TC gốc ghi「change spec 100」nhưng 3 dòng ngay sau lại test và chốt ở 30. Ngoài ra 店舗名 ghi "
     "vào CẢ `calendar_name` và `store_name` (r1481) — nếu 2 cột khác độ dài sẽ cắt dữ liệu.",
     "[トップ・店舗情報・利用規約] Validate tên cửa hàng 店舗名 và đồng bộ với calendar_name",
     "",
     "Chốt độ dài thật; bổ sung `store_name` vào Field Matrix; xác nhận rule đồng bộ 2 cột."],

    ["MT-33", "CAO", W,
     "Khách bị filter chặn: có mở được link LỊCH SỬ và link HỦY không?",
     "· 「Setting calendar」r275-r278 (Update spec **06/11/2025**):「user mở từ link lịch sử + "
     "thỏa mãn filter ⇒ Hiện trang báo lỗi… **Update spec ngày 06/11/2025: User thỏa mãn điều kiện "
     "filter vẫn sẽ hiển thị màn hình canc…**」— tức đã đổi thành CHO PHÉP\n"
     "· 「Booking phía line user」r1324 (cùng chủ đề, khối khác):「user mở từ link lịch sử + "
     "thỏa mãn filter ⇒ **Hiện trang báo lỗi**」\n"
     "· SpecChange #32646 (29/10/2025, r1358-r1374): repro chính là「user booking success ⇒ đc send "
     "action chứa URL cancel; admin add filter ⇒ user không mở được URL hủy」→ ticket sửa để mở được.",
     "Spec KHÔNG mô tả tính năng 予約ページの非表示 (filter chặn trang đặt lịch) ở mức business rule; "
     "chỉ có `filter_calendar_salon_ids` xuất hiện gián tiếp qua §8.3.",
     "Đây là hành vi KH cuối gặp thật (đã thành ticket #32646): khách đặt được rồi bị chặn không hủy "
     "được lịch. 2 khối TC nói ngược nhau; khối cho phép mới hơn.",
     "[予約ページの非表示 (filter)] Update spec 06/11/2025 khách thỏa filter vẫn vào được màn hủy · "
     "[LINE user — hủy booking] SpecChange #32646",
     "",
     "Chốt phạm vi filter chặn (link booking / link lịch sử / link hủy); **sửa khối TC cũ r1324**; "
     "bổ sung mục 予約ページの非表示 vào spec §2.4."],

    ["MT-34", "TRUNG BÌNH", W,
     "2 staff liên kết CHUNG 1 Google Calendar thì block time tính cho ai?",
     "「Sync google calendar」r280-r320 (Bug #26653, 11/09/2024) có khối test đầy đủ nhưng "
     "**không ghi kết luận** cho câu hỏi: event tạo trực tiếp trên calendar dùng chung sẽ sinh "
     "block time cho 1 staff hay CẢ 2 staff.\n"
     "r319-r320: hủy liên kết 1 trong 2 staff — corpus cũng không ghi rõ dữ liệu của staff còn lại "
     "có bị xóa lây không.",
     "`feature-spec.md` BR-09:「Mỗi nhân viên có thể liên kết Google Calendar riêng → **1 record** "
     "trong `b_c_salon_google_calendar`; khi ngắt liên kết → **xóa** `CalendarSalonBookingByGoogle` "
     "+ `BCSalonGoogleCalendar` records」.\n"
     "Spec giả định 1-1 giữa staff và calendar, KHÔNG lường trường hợp dùng chung.",
     "Nếu hủy liên kết staff A mà xóa hết block time của calendar dùng chung thì staff B mất toàn bộ "
     "lịch bận → nhận booking trùng giờ. Đây là kịch bản KH thật (salon nhỏ dùng 1 lịch chung).",
     "[Googleカレンダー連携] Bug #26653 2 staff liên kết CHUNG 1 Google Calendar",
     "",
     "Chốt hành vi cho trường hợp dùng chung; bổ sung ngoại lệ vào BR-09."],

    ["MT-35", "CAO", W,
     "Phân quyền tài khoản Staff: CHƯA từng được test",
     "Corpus ghi nhiều lần rằng không test được:\n"
     "· 「Quản lý calendar」r1866:「trên dev **ko add đủ router quyền staff** nên ko test dc」\n"
     "· r3118:「trên dev acc staff **thiếu quyến salon** nên ko chekc dc」\n"
     "· r3287:「salon acc staff trên dev **chưa add hết quyền** nên ko test」\n"
     "· 「Sync google calendar」r520-r521:「Check account staff」— không có kết quả\n"
     "· Tab「Staff」liệt kê ~30 màn con cần test bằng account staff nhưng cột kết quả TRỐNG HOÀN TOÀN.\n"
     "Ngược lại #38520 r51-r52 (07/2026) đã viết TC đầy đủ cho cả 2 nhánh có/không quyền, "
     "gồm cả chặn ở tầng API.",
     "`feature-spec.md` §9.2 mục 9 ghi thẳng đây là Gap:「**Phân quyền Staff chi tiết** — Staff thấy "
     "được những tab nào? Có thể tạo/sửa booking không?」\n"
     "§1.2 Actors:「Staff — Tùy phân quyền — (chi tiết phân quyền **chưa fully-captured**)」.",
     "Cả spec lẫn corpus đều để trống đúng một vùng: quyền truy cập. Rủi ro là staff không có quyền "
     "vẫn gọi được API xem/sửa booking của salon — đúng kiểu lỗi phân quyền đã từng xảy ra ở các "
     "tính năng khác (UI ẩn menu nhưng API không chặn).",
     "[Phân quyền & môi trường] Staff KHÔNG có quyền màn 予約管理 · Staff CÓ quyền · "
     "Rà soát phân quyền staff trên TẤT CẢ màn con · [Googleカレンダー連携] Tài khoản staff",
     "",
     "Chuẩn bị môi trường có account staff đủ quyền; chạy trọn bộ TC phân quyền (UI + URL + API); "
     "đóng Gap §9.2 mục 9 bằng bảng quyền theo từng màn con."],

    ["MT-36", "THẤP", W,
     "Giá trị `payment_system` khi calendar TẮT 決済 — corpus để dấu hỏi",
     "「Liên kết bill tiền」r90-r97:「Vẫn booking success, ko bill tiền. Sau khi booking thì: "
     "`calendar_salon_line_booking.payment_system` = **NULL?**」— dấu hỏi nằm trong chính "
     "Expected Result, lặp lại ở cả 8 dòng của khối.",
     "`feature-spec.md` §3.3 ER diagram có cột `payment_system varchar` nhưng "
     "**không có trong Field Traceability Matrix** và không mô tả giá trị.",
     "Expected có dấu hỏi thì không kiểm chứng được. Cột này dùng để phân biệt Stripe/UnivaPay khi "
     "hoàn tiền — sai giá trị có thể gọi nhầm API hoàn tiền.",
     "[決済連携 — cài đặt] TẮT 決済 ở account → mọi tổ hợp course/staff đều không bill",
     "",
     "Xác nhận giá trị thật của `payment_system` khi không bill; bổ sung vào Field Matrix."],

    ["MT-37", "TRUNG BÌNH", W,
     "Calendar chọn nhà cung cấp CHƯA liên kết nhưng booking cũ vẫn bill được?",
     "「Liên kết bill tiền」:\n"
     "· r86-r87:「liên kết univapay chọn stripe / liên kết stripe chọn univapay ⇒ ko liên kết thì "
     "sẽ ko hiển thị ra option để chọn」\n"
     "· r88:「User booking mới ⇒ đến mh nhập card sẽ **ko hiển thị dc phần nhập card**」\n"
     "· r89:「User đã booking trước đó, Admin approve ⇒ **vẫn bill tiền do có thông tin card ?**」"
     "— dấu hỏi trong Expected.",
     "`feature-spec.md` BR-05 chỉ mô tả điều kiện BẬT thanh toán; "
     "KHÔNG mô tả điều gì xảy ra khi nhà cung cấp bị hủy liên kết sau đó.\n"
     "§2.5 ghi「sau khi chọn nhà cung cấp và lưu lần đầu → không thể thay đổi」.",
     "Liên quan trực tiếp đến tiền: nếu vẫn bill qua nhà cung cấp đã hủy liên kết thì giao dịch có "
     "thể thất bại hoặc rơi vào tài khoản sai. Expected có dấu hỏi nên không ai chốt được.",
     "[決済 — thẻ & 3D Secure] Chọn nhà cung cấp CHƯA liên kết → không hiện màn nhập thẻ",
     "",
     "Chốt hành vi cho booking cũ khi nhà cung cấp bị hủy liên kết; bổ sung vào §2.5 và BR-05."],

    ["MT-38", "TRUNG BÌNH", W,
     "Trạng thái 現地決済 ghi vào Google Sheet đang bị đánh NG",
     "「Quản lý calendar」r2800:「check sau khi update thành thanh toán thành công ⇒ … "
     "GG sheet_cột L: giá = XXX và stt **現地（決済成功） ⇒ NG**」\n"
     "r2801, r2806: tương tự,「GG sheet_cột L: giá = XXX và stt 現地決済 ⇒ **NG**」.",
     "`feature-spec.md` không mô tả tích hợp Google Spreadsheet ở mức field/giá trị "
     "(chỉ có `google_sheet_id` ở Field #6).",
     "TC gốc đã ghi nhận NG nhưng không kèm ticket. KH dùng Google Sheet để đối soát doanh thu — "
     "trạng thái sai làm sai đối soát tiền mặt tại chỗ.",
     "[現地決済] Admin cập nhật trạng thái 現地決済 từ 2 màn",
     "",
     "Verify lại giá trị ghi vào Google Sheet cho 2 trạng thái 現地決済; nếu còn NG thì raise ticket; "
     "bổ sung bảng cột Google Sheet vào spec."],

    ["MT-39", "CAO", W,
     "Random staff: khách bị tính tiền theo 指定なし dù được gán staff CÓ phụ phí",
     "「Quản lý calendar」r2791-r2792 và r2808-r2809 (CASE RANDOM option 2/3):\n"
     "「USER BOOKING / ADMIN BOOKING ⇒ **lấy giá lúc booking cho no staff** trường `amount` bảng "
     "`salon_line_booking`」.\n"
     "Trong khi「Liên kết bill tiền」r24 quy định số tiền bill = amount của (course + staff).",
     "`feature-spec.md` không mô tả công thức tính tiền của booking, cũng không mô tả tương tác giữa "
     "random staff và phụ phí staff (`calendar_salon_staff.staff_bill` chỉ xuất hiện trong "
     "danh sách field ở §2.3).",
     "Khách chọn 指定なし và được hệ thống tự gán vào staff có phụ phí 1,000 yên nhưng chỉ bị tính "
     "tiền course. Có thể đúng ý đồ (không tính thêm khi khách không chủ động chọn staff) nhưng cũng "
     "có thể là thất thoát doanh thu của KH. Cần chốt vì đây là tiền thật.",
     "[現地決済] Admin book / random staff: lấy giá tại thời điểm booking cho 指定なし",
     "",
     "Chốt ý đồ nghiệp vụ; bổ sung công thức tính `payment_amount` (gồm nhánh random) thành BR mới."],

    ["MT-40", "THẤP", W,
     "Nút 今日 phía LINE user: về tuần/tháng hiện tại hay tuần/tháng có lịch gần nhất?",
     "「Main case」:\n"
     "· r278:「check user nhấn nút 今日 ⇒ hiện tuần gần nhất có lịch làm việc, giống case khi mở vào "
     "màn booking mới. **Spec mới update: Khi click button 今日 sẽ luôn hiển thị tuần hiện tại**」\n"
     "· r287 (chế độ tháng):「hiện tháng gần nhất có lịch lv… **Hiện tháng hiện tại**」\n"
     "Cả 2 ô đều chứa 2 kết luận, phần sau là bản update.",
     "Spec KHÔNG mô tả màn chọn slot phía LINE user (§2.6 chỉ có 6 dòng tóm tắt luồng LIFF).",
     "Ô Expected chứa cả hành vi cũ và mới → member dễ chạy theo bản cũ. Hành vi này KH nhìn thấy "
     "trực tiếp mỗi lần đặt lịch.",
     "[LINE user — chọn slot] Điều hướng tuần/tháng và nút 今日",
     "",
     "Xoá vế cũ khỏi TC gốc; bổ sung mô tả màn chọn slot phía LINE user vào spec §2.6."],

    ["MT-41", "TRUNG BÌNH", W,
     "Job monitor còn giám sát 'booking vượt limit' — spec chỉ mô tả giám sát block time",
     "「Quản lý calendar」r3322-r3343 (Task thêm monitor cho salon + lesson):\n"
     "· salon: cảnh báo khi có booking chèn vào block time\n"
     "· lesson: cảnh báo khi **số lượng booking > limit**\n"
     "· Bộ lọc: CHỈ push khi `admin_id` = NULL **và** status = 1 (friend đặt và thành công); "
     "các status 0, 2, 3 và booking do admin đặt đều KHÔNG cảnh báo",
     "`feature-spec.md` §7.1.4 `MonitorCalendarBookingTask` chỉ mô tả:「Phát hiện **overlap** giữa "
     "booking LME và block time Google Calendar (tính cả `time_before`/`time_after`)… "
     "gửi Chatwork alert (room ID: 316148419). Không tự sửa dữ liệu.」\n"
     "KHÔNG nhắc đến giám sát vượt limit, không nhắc bộ lọc `admin_id`/status.",
     "Bộ lọc `admin_id` = NULL + status = 1 là chi tiết quan trọng: nếu dev sửa nhầm, hệ thống sẽ "
     "spam cảnh báo mỗi lần admin đặt hộ (vốn được phép vượt limit theo MT-13).",
     "[Job nền & monitor] Job monitor phát hiện booking chèn block time · "
     "Job monitor chỉ đếm booking của FRIEND ở trạng thái thành công",
     "",
     "Bổ sung vào §7.1.4: phạm vi giám sát (block time + vượt limit) và bộ lọc `admin_id`/status."],

    ["MT-42", "THẤP", W,
     "Thao tác ca làm việc có ghi audit log không?",
     "#38520 r63:「Thao tác sửa / xóa ca có ghi log đủ: **ai, khi nào, thay đổi gì** (giá trị trước → "
     "sau); truy được người thao tác khi cần」— TC yêu cầu nhưng không dẫn bảng log nào.",
     "`feature-spec.md` §3.1 liệt kê 4 bảng audit: `calendar_salon_history_change_setting_payment`, "
     "`calendar_salon_line_booking_history_actions`, `calendar_salon_line_booking_payment_history`, "
     "`calendar_salon_setting_notify_full_history`.\n"
     "**KHÔNG có bảng lịch sử nào cho `calendar_salon_time_booking` (ca làm việc)**.",
     "Ca làm việc là dữ liệu bị sửa/xóa nhiều nhất và đã gây ít nhất 2 ticket mất dữ liệu "
     "(#29394, #38519). Không có log thì không điều tra được ai xóa ca của KH.",
     "[Phân quyền & môi trường] Ghi log thao tác sửa / xóa ca làm việc",
     "",
     "Xác nhận có bảng log cho ca làm việc không; nếu không có, cân nhắc bổ sung (và ghi rõ trong "
     "spec là KHÔNG có để tester không tìm nhầm)."],
]
