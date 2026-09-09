# -*- coding: utf-8 -*-
"""FA-020 サロン・面談予約 (Đặt lịch salon) — Nhóm 1-3: màn list calendar, wizard tạo mới, giới hạn plan.

Nguồn chính: 11.1 TCsLine_SalonCalendar
  - tab「Calendar list」(07/2024 → 2025, 228 TC lá) — màn list + toàn bộ wizard 4 bước
  - tab「Quản lý course&staff」r129-r198 (08/2025) — hard limit 200 course / 200 staff / 100 câu hỏi
  - tab「Test limit booking_V4_2」— đối chiếu limit hiển thị
Bổ sung: TCsLine_Limit all tính năng → tab「Limit Salon」(03/2026).
"""
from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A đã liên kết LINE OA\n"
       "- Bot A đã đăng ký LIFF ID cho tính năng đặt lịch\n"
       "- Mở menu 予約管理 > サロン・面談予約 (/basic/calendar-salon)")
CAL = ADM + "\n- Đã có 1 calendar loại スタッフ tên「サロンA」với 2 staff S1/S2 và 1 course「カットA」(60 phút)"

S1 = [
    # ══════════════ 1. Màn list calendar ══════════════
    tc("Màn list calendar", "FUNC-001", "Normal",
       "Bot chưa có calendar nào → hiện 1 card mẫu rỗng + nút tạo mới",
       ADM + "\n- Bot A CHƯA tạo salon calendar nào (calendar_salon rỗng với bot_id này)",
       "1. Mở /basic/calendar-salon\n2. Quan sát vùng danh sách",
       "0 calendar",
       "- Hiện giao diện 1 calendar default chưa có data\n"
       "- Có nút「サロン・面談予約を新規作成」để tạo calendar mới\n"
       "- Không hiện card salon nào khác",
       note="Nguồn: Calendar list r3. Spec feature-spec.md §2.1 SCR-SLN-01."),

    tc("Màn list calendar", "UI-002", "Normal",
       "Popup hướng dẫn nút 新規作成 hiện lần đầu, bấm X thì tắt vĩnh viễn",
       ADM + "\n- Cột `user.enable_tooltip_calendar_salon` = 1 (chưa bấm tắt lần nào)",
       "1. Mở /basic/calendar-salon lần đầu → quan sát popup\n"
       "2. Bấm icon X trên popup\n"
       "3. Sang màn khác rồi quay lại · logout/login lại · mở bằng cửa sổ ẩn danh",
       "Tài khoản admin A",
       "- Bước 1: hiện popup「新規作成をクリックして、サロン・面談予約を作成しましょう。」\n"
       "- Bước 2: popup ẩn đi, `user.enable_tooltip_calendar_salon` đổi thành 0\n"
       "- Bước 3: cả 3 lối vào đều KHÔNG hiện lại popup",
       note="Nguồn: Calendar list r4-r6 (3 tầng: GUI + DB + 3 lối vào lại — RULE-07)."),

    tc("Màn list calendar", "UI-002", "Normal",
       "Popup hướng dẫn vẫn hiện với account khác chưa bấm X",
       ADM + "\n- Admin B cùng bot A, `enable_tooltip_calendar_salon` = 1",
       "1. Admin A đã bấm X tắt popup\n2. Logout, đăng nhập bằng admin B\n3. Mở /basic/calendar-salon",
       "2 tài khoản admin trên cùng bot",
       "- Admin B VẪN hiện popup hướng dẫn (cờ lưu theo user, không theo bot)",
       note="Nguồn: Calendar list r7."),

    tc("Màn list calendar", "LIST-001", "Normal",
       "Dropdown カレンダータイプ lọc đúng 3 giá trị 全て / 個人 / スタッフ",
       CAL + "\n- Bot có 2 calendar loại 個人 và 3 calendar loại スタッフ",
       "1. Mở màn list\n2. Chọn dropdown「全て」\n3. Chọn「個人」\n4. Chọn「スタッフ」",
       "2 calendar 個人 + 3 calendar スタッフ",
       "- 全て: hiện đủ 5 calendar\n- 個人: chỉ hiện 2 calendar loại 個人\n"
       "- スタッフ: chỉ hiện 3 calendar loại スタッフ",
       note="Nguồn: Calendar list r16-r18. EP-02 tham số staffTypeFilter."),

    tc("Màn list calendar", "UI-001", "Normal",
       "Card salon hiện đủ badge loại / toggle 有効 / ảnh / tên quản lý",
       CAL,
       "1. Mở màn list\n2. Quan sát card của「サロンA」(loại スタッフ) và 1 card loại 個人",
       "1 calendar スタッフ + 1 calendar 個人",
       "- Calendar 個人: hiện icon + text「個人」\n- Calendar スタッフ: hiện icon + text「スタッフ」\n"
       "- Toggle ON/OFF mặc định ON\n- Hiện tên quản lý của calendar tương ứng",
       note="Nguồn: Calendar list r311-r313, r320."),

    tc("Màn list calendar", "FUNC-002", "Abnormal",
       "OFF calendar → link booking và link lịch sử phía LINE user báo lỗi",
       CAL + "\n- LINE user U1 đã kết bạn bot A",
       "1. Ở card「サロンA」gạt toggle sang OFF\n"
       "2. LINE user U1 mở 予約ページURL\n3. LINE user U1 mở 予約履歴ページURL",
       "enable_use_calendar = 0",
       "- Cả 2 link đều hiện màn báo lỗi「この予約は現在利用できませんん。」\n"
       "- Không vào được màn chọn course/slot",
       note="Nguồn: Calendar list r314 + Booking phía line user r4. ⚠ Text lỗi trong corpus có 2 chữ ん "
            "(「利用できませんん」) — nghi lỗi chính tả của tool, cần đối chiếu bản JP thật khi test."),

    tc("Màn list calendar", "UI-001", "Normal",
       "Ảnh calendar: không set → ảnh default; set đúng 1000x500 → không có khoảng trắng 2 bên",
       CAL,
       "1. Card calendar chưa set ảnh → quan sát\n"
       "2. Vào トップ設定 upload ảnh 1000x500 → quay lại màn list\n"
       "3. Upload ảnh tỉ lệ khác (vd 800x800) → quay lại màn list",
       "Ảnh 1000x500 và ảnh 800x800",
       "- Chưa set: hiện ảnh default\n- Ảnh 1000x500: hiển thị vừa khung, không khoảng trắng 2 bên\n"
       "- Ảnh sai tỉ lệ: được resize để không hiện khoảng trắng 2 bên",
       note="Nguồn: Calendar list r318-r319 (đã update theo comment resize)."),

    tc("Màn list calendar", "INTG-SHEET-001", "Normal",
       "Icon Google Spreadsheet chỉ hiện khi calendar đã liên kết, mất khi hủy liên kết",
       CAL,
       "1. Calendar chưa liên kết Google → quan sát card\n"
       "2. Liên kết Googleスプレッドシート → quay lại màn list, bấm icon\n"
       "3. Hủy liên kết → quay lại màn list",
       "Tài khoản Google có quyền tạo Spreadsheet",
       "- Chưa liên kết: KHÔNG hiện icon spreadsheet\n"
       "- Đã liên kết: hiện icon; bấm icon mở đúng file Google Sheet của calendar đó ở tab mới\n"
       "- Sau khi hủy liên kết: icon biến mất",
       note="Nguồn: Calendar list r315-r317."),

    tc("Màn list calendar", "FUNC-003", "Normal",
       "Copy 2 URL 予約ページ và 予約履歴ページ từ card",
       CAL,
       "1. Bấm nút copy cạnh「予約ページURL」→ dán vào ô text\n"
       "2. Bấm nút copy cạnh「予約履歴ページURL」→ dán vào ô text",
       "calendar_salon_id của サロンA",
       "- URL booking dạng `https://liff.line.me/{liff_id}?calendar_salon_id={id}&ts={timestamp}`\n"
       "- URL lịch sử có thêm `&tab=history`\n- Cả 2 URL mở được và ra đúng màn tương ứng",
       note="Nguồn: Calendar list r323-r324. Spec feature-spec.md §2.1 (card salon)."),

    tc("Màn list calendar", "FUNC-004", "Normal",
       "Sắp xếp calendar bằng nút 一番上/一番下 và drag-drop, có lưu thứ tự",
       CAL + "\n- Bot có 4 calendar theo thứ tự C1, C2, C3, C4",
       "1. Bấm nút「並び替え」→ hiện popup sắp xếp\n"
       "2. Kéo C4 lên đầu → bấm lưu\n3. Reload màn list\n"
       "4. Mở lại popup, dùng nút「一番上に移動」cho C3 → lưu → reload",
       "4 calendar C1..C4",
       "- Thứ tự mới được lưu và giữ nguyên sau reload (calendar_salon.order cập nhật)\n"
       "- Cả drag-drop và nút di chuyển đều đổi được vị trí",
       note="Nguồn: Calendar list r82, r84-r86. EP-04."),

    tc("Màn list calendar", "FUNC-004", "Abnormal",
       "Đổi vị trí trong popup sắp xếp rồi KHÔNG lưu → thứ tự giữ nguyên",
       CAL + "\n- Bot có 4 calendar theo thứ tự C1, C2, C3, C4",
       "1. Bấm「並び替え」\n2. Kéo C4 lên đầu\n3. Đóng popup bằng X (không bấm lưu)\n4. Reload màn list",
       "4 calendar C1..C4",
       "- Thứ tự vẫn là C1, C2, C3, C4\n- Bảng calendar_salon cột `order` không đổi",
       note="Nguồn: Calendar list r83."),

    tc("Màn list calendar", "FUNC-004", "Normal",
       "Đổi tên quản lý calendar qua popup — validate rỗng và > 10 ký tự",
       CAL,
       "1. Bấm vào tên quản lý trên card → popup đổi tên hiện tên hiện tại\n"
       "2. Xóa trắng → bấm lưu\n3. Nhập 11 ký tự\n4. Nhập 10 ký tự tiếng Nhật → lưu",
       "Tên rỗng · 11 ký tự · 「サロン管理名」(≤10 ký tự JP)",
       "- Bước 1: popup hiện đúng tên quản lý hiện tại\n"
       "- Bước 2: báo lỗi required, không lưu\n"
       "- Bước 3: không nhập được ký tự thứ 11\n"
       "- Bước 4: lưu thành công, tên mới hiện đúng ở card và các màn khác",
       note="Nguồn: Calendar list r321, r325-r328."),

    tc("Màn list calendar", "FUNC-001", "Normal",
       "Nút 予約管理ページを開く mở đúng trang chi tiết của calendar tương ứng",
       CAL + "\n- Bot có ≥ 2 calendar",
       "1. Bấm「予約管理ページを開く」ở card thứ 2\n2. Đối chiếu tên + id trên URL",
       "2 calendar",
       "- Mở /basic/calendar-salon/{id} đúng của card đã bấm\n"
       "- Header trang hiện đúng tên calendar đó",
       note="Nguồn: Calendar list r322. EP-05."),

    tc("Màn list calendar", "FUNC-001", "Normal",
       "Nút xem trước (プレビュー) và điều hướng vào popup tạo calendar",
       ADM,
       "1. Bấm nút create → mở tab mới hiện popup preview\n"
       "2. Bấm X → 3. Bấm lại create → bấm「新規作成にすすむ」\n"
       "4. Quay lại, bấm「サロン・面談予約の新規作成にすすむ」\n5. Bấm back",
       "-",
       "- Bước 1: mở tab mới hiện popup preview\n- Bước 2: đóng preview, về màn list\n"
       "- Bước 3 và 4: đều mở popup tạo calendar mới\n- Bước 5: đóng preview, về màn list",
       note="Nguồn: Calendar list r87-r91."),

    tc("Màn list calendar", "STATE-001", "Abnormal",
       "Mở 2 tab khi chỉ còn 1 slot calendar — tab 2 phải bị chặn khi tạo",
       ADM + "\n- Bot ở plan chỉ còn đúng 1 slot calendar được tạo",
       "1. Mở màn list trên tab 1 và tab 2\n"
       "2. Tab 1: tạo calendar → thành công (hết slot)\n"
       "3. Tab 2: vào màn chọn loại calendar → bấm「次にすすむ」\n"
       "4. Tab 2: thử tạo từ modal add booking (nếu có lối vào)",
       "Plan còn đúng 1 slot",
       "- Tab 2 KHÔNG tạo thêm được: hiện lỗi giới hạn plan\n"
       "- Cả 2 lối vào (màn chọn loại + modal) đều check max ở server\n"
       "- DB không sinh calendar vượt giới hạn",
       note="Nguồn: Calendar list r55-r56. Race condition — RULE về kiểm tra ở tầng server."),

    # ══════════════ 2. Tạo calendar — wizard ══════════════
    tc("Tạo calendar — wizard", "FUNC-004", "Normal",
       "Popup tạo calendar: validate 2 trường tên (booking ≤30, quản lý ≤10)",
       ADM,
       "1. Bấm create → mở popup tạo calendar\n"
       "2. Bỏ trống「tên hiển thị trên màn booking」→ bấm tạo\n"
       "3. Nhập 31 ký tự vào tên hiển thị\n"
       "4. Bỏ trống tên quản lý → bấm tạo\n5. Nhập 11 ký tự vào tên quản lý\n"
       "6. Nhập tên hiển thị 30 ký tự JP + tên quản lý 10 ký tự JP → bấm tạo",
       "Chuỗi 31 ký tự · chuỗi 11 ký tự · 「サロン・面談予約テスト用カレンダー名」",
       "- Bước 2 và 4: báo required, không tạo\n"
       "- Bước 3 và 5: tự cắt hoặc báo lỗi quá số ký tự cho phép\n"
       "- Bước 6: tạo thành công, đóng popup, sang màn chọn loại calendar; "
       "bảng `calendar_salon` sinh 1 bản ghi mới",
       note="Nguồn: Calendar list r92-r97, r100. ⚠ Corpus ghi「tự động cắt HOẶC báo lỗi」— "
            "hành vi chưa chốt, xem MT-05."),

    tc("Tạo calendar — wizard", "FUNC-DRAFT-001", "Normal",
       "Popup tạo calendar: nút X và nút back không lưu dữ liệu",
       ADM,
       "1. Mở popup tạo, nhập 2 trường tên\n2. Bấm X\n"
       "3. Mở lại popup tạo, nhập tên, bấm back",
       "Tên bất kỳ",
       "- Bấm X: đóng popup, KHÔNG lưu, quay về màn preview\n"
       "- Bấm back: quay về màn preview trước đó\n"
       "- Bảng `calendar_salon` không sinh bản ghi",
       note="Nguồn: Calendar list r98-r99. ⚠ r99 còn để dấu hỏi「từ preview click next ra màn tạo thì "
            "có hiển thị data trước đấy nhập ko?」— hành vi giữ/xóa data chưa chốt."),

    tc("Tạo calendar — wizard", "FUNC-001", "Normal",
       "Chọn loại calendar: default 個人, đi tiếp ra đúng step 2 của từng loại",
       ADM + "\n- Đang ở màn chọn loại calendar (bước 2 của wizard)",
       "1. Quan sát lựa chọn mặc định\n"
       "2. Chọn loại 個人 (1 staff) → bấm「次にすすむ >」\n"
       "3. Làm lại, chọn loại スタッフ (nhiều staff) → bấm「次にすすむ >」",
       "-",
       "- Mặc định chọn loại 個人\n"
       "- Loại 個人 → mở màn set giờ mở cửa (màn 8)\n"
       "- Loại スタッフ → mở màn tạo 2 staff (màn 7)",
       note="Nguồn: Calendar list r102-r104. BR-01 (calendar_staff_type)."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Normal",
       "Loại 個人 — set giờ mở cửa mặc định 10:00-21:00 và validate biên 00:00~23:59",
       ADM + "\n- Đang ở màn set giờ mở cửa của wizard loại 個人",
       "1. Quan sát giờ mặc định\n"
       "2. Nhập giờ bắt đầu lần lượt 00:00 / 00:30 / 15:15 / 23:59 → lưu\n"
       "3. Nhập giờ kết thúc lần lượt 00:00 / 00:30 / 15:15 / 23:59 → lưu",
       "00:00 · 00:30 · 15:15 · 23:59",
       "- Mặc định 10:00 - 21:00\n- Cả 4 giá trị biên ở cả 2 ô đều lưu thành công",
       note="Nguồn: Calendar list r105-r113 (gộp 8 dòng cùng 1 kết quả: lưu thành công — RULE gộp input)."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Boundary",
       "Loại 個人 — giờ bắt đầu > giờ kết thúc = ca qua ngày, được phép lưu",
       ADM + "\n- Đang ở màn set giờ mở cửa của wizard loại 個人",
       "1. Nhập giờ bắt đầu 20:00, giờ kết thúc 08:00 → lưu\n2. Sang màn hiển thị lịch làm việc để đối chiếu",
       "20:00 ~ 08:00",
       "- Lưu thành công (spec đã update: cho phép set giờ làm việc qua ngày)\n"
       "- Lịch làm việc hiển thị đúng ca qua ngày",
       note="Nguồn: Calendar list r115 (đã update:「cho phép nhập => set time làm việc qua ngày」)."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Normal",
       "Loại 個人 — chọn 24h thì disable ô giờ; ngày nghỉ mặc định tick Chủ nhật",
       ADM + "\n- Đang ở màn set giờ mở cửa của wizard loại 個人",
       "1. Tick「営業24時間」→ quan sát 2 ô giờ\n2. Quan sát danh sách thứ trong tuần",
       "-",
       "- Tick 24h → 2 ô chọn giờ bắt đầu/kết thúc bị disable\n"
       "- Danh sách thứ mặc định tick nghỉ Chủ nhật",
       note="Nguồn: Calendar list r116-r117."),

    tc("Tạo calendar — wizard", "UI-001", "Normal",
       "Màn xem trước giờ mở cửa: hiển thị đúng 1 tuần gần nhất, 24h và ngày nghỉ",
       ADM + "\n- Wizard 個人, đã set giờ mở cửa 09:00-18:00, nghỉ Chủ nhật, thứ Tư set 24h",
       "1. Sang màn hiện giờ mở cửa (màn 9)\n2. Đối chiếu từng ngày\n"
       "3. Rê chuột lên 1 ngày\n4. Bấm「編集する」",
       "Giờ 09:00-18:00 · thứ Tư 24h · Chủ nhật nghỉ",
       "- Hiển thị 1 tuần gần nhất tính từ ngày hiện tại\n"
       "- Ngày thường: hiện đúng 09:00-18:00\n- Ngày 24h: hiện 00:00 đến 23:59\n"
       "- Ngày nghỉ: hiện text「休業日」\n- Rê chuột: đổi màu, hiện text + icon edit\n"
       "- Bấm 編集する: mở popup edit giờ",
       note="Nguồn: Calendar list r122-r128."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Abnormal",
       "Popup edit giờ trong wizard — chuỗi khung giờ chồng lấn báo lỗi đúng số thứ tự dòng",
       ADM + "\n- Đang ở popup edit giờ của 1 ngày, đã có T1 09:00~12:00",
       "1. Thêm T2 = 11:30~14:00 → lưu\n"
       "2. Đặt lại T2 = 12:30~14:00 (hợp lệ) rồi thêm T3 = 12:01~15:00 → lưu\n"
       "3. Đặt T2 = 11:30~14:00 và T3 = 07:00~11:00 → lưu",
       "T1 09:00~12:00 · các mốc T2/T3 như mô tả",
       "- Bước 1: lỗi「2項目の開始時間は、他の終了時間より、大きくしてください。」\n"
       "- Bước 2: lỗi「3項目の開始時間は…」\n"
       "- Bước 3: lỗi「2項目の開始時間は…」(báo dòng lỗi ĐẦU TIÊN)\n"
       "- Không dòng nào được lưu",
       note="Nguồn: Calendar list r177-r179 (và r280-r282 lặp lại cho loại スタッフ). "
            "Kiểm tra số thứ tự dòng trong message phải khớp dòng lỗi đầu tiên."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Normal",
       "Popup edit giờ — thêm khung giờ hợp lệ có start nhỏ hơn T1 vẫn add được, không xóa được T1",
       ADM + "\n- Đang ở popup edit giờ, đã có T1 09:00~12:00",
       "1. Thêm T2 = 05:30~08:30 → lưu\n2. Quan sát icon xóa ở dòng T1",
       "T1 09:00~12:00 · T2 05:30~08:30",
       "- T2 thêm thành công (không cần theo thứ tự thời gian)\n"
       "- Dòng đầu tiên KHÔNG có icon xóa → không xóa được T1",
       note="Nguồn: Calendar list r171, r173, r180."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Boundary",
       "Ngày trước có ca qua ngày → ràng buộc giờ của ngày kế tiếp",
       ADM + "\n- Ngày 1 đã có ca qua ngày 20:00~10:00 (ngày 2)",
       "1. Ngày 2: set ca 09:00~12:00 → lưu\n2. Ngày 2: set ca 11:00~12:00 → lưu\n"
       "3. Ngày 2: tick làm việc 24h → lưu\n4. Ngày 2: tick ngày nghỉ → lưu",
       "Ngày 1: 20:00~10:00",
       "- Bước 1 (start < end của ngày 1): báo lỗi\n"
       "- Bước 2 (start ≥ end của ngày 1): cho phép add\n"
       "- Bước 3 (24h): báo lỗi\n- Bước 4 (ngày nghỉ): cho phép, ngày 2 hiện 休業日",
       note="Nguồn: Calendar list r187-r190 (mỗi nhánh 1 kết quả khác nhau → tách riêng nhưng cùng "
            "chuỗi thao tác ràng buộc, giữ chung theo FUNC-SEQ)."),

    tc("Tạo calendar — wizard", "FUNC-DATE-001", "Boundary",
       "Sửa ca của ngày 1 thành qua ngày — chặn khi lấn giờ nhỏ nhất của ngày 2",
       ADM + "\n- Ngày 1 có ca thường; ngày 2 đã có ca 11:00~12:00",
       "1. Sửa ca ngày 1 thành qua ngày với end = 11:00 → lưu\n"
       "2. Sửa ca ngày 1 thành qua ngày với end = 11:30 → lưu\n"
       "3. Đặt ngày 2 thành 24h rồi sửa ca ngày 1 thành qua ngày → lưu",
       "Ngày 2 sớm nhất 11:00",
       "- Bước 1 (end ≤ start nhỏ nhất ngày 2): cho phép\n"
       "- Bước 2 (end > start nhỏ nhất ngày 2): báo lỗi\n"
       "- Bước 3 (ngày 2 đang 24h): báo lỗi",
       note="Nguồn: Calendar list r191-r193."),

    tc("Tạo calendar — wizard", "FUNC-004", "Normal",
       "Wizard tạo course: validate tên (≤50), 所要時間 ≥ 5 phút, số tiền",
       ADM + "\n- Đang ở màn tạo course của wizard (màn 13)",
       "1. Bỏ trống tên course → lưu\n2. Nhập 50 ký tự → lưu\n3. Nhập 51 ký tự → lưu\n"
       "4. Set 所要時間 = 0h00 → lưu\n5. Set 0h05 / 1h00 / 23h55 → lưu\n"
       "6. Bỏ trống số tiền → lưu\n7. Nhập 5000 → lưu\n8. Nhập -100 / 1.5 / abc",
       "Tên 50 và 51 ký tự · 0h00 · 0h05 · 1h00 · 23h55 · 5000 · -100 · 1.5 · abc",
       "- B1: required\n- B2: lưu thành công\n- B3: báo lỗi\n"
       "- B4: lỗi「所要時間は5分以上に設定してください。」\n- B5: cả 3 mốc đều lưu thành công\n"
       "- B6: lưu thành công, tự fill 0 và ngoài list hiện「設定なし」\n"
       "- B7: hiện format 5,000\n- B8: invalid, không lưu",
       note="Nguồn: Calendar list r194-r205. ⚠ Tên course ở wizard = 51 ký tự BÁO LỖI, còn ở màn "
            "コース作成・編集 = TỰ CẮT (Quản lý course&staff r239) → xem MT-05."),

    tc("Tạo calendar — wizard", "FUNC-004", "Normal",
       "Wizard tạo course: nút 基本情報を保存 kết thúc wizard, về màn quản lý calendar",
       ADM + "\n- Đang ở màn tạo course của wizard với dữ liệu hợp lệ",
       "1. Bấm「基本情報を保存」\n2. Quan sát điều hướng và dữ liệu course",
       "Course「カットA」60 phút, 5,000 yên",
       "- Lưu thành công, chuyển sang màn quản lý calendar (予約管理ページ)\n"
       "- Course vừa tạo hiện ở tab コース・スタッフ",
       note="Nguồn: Calendar list r206, r309."),

    tc("Tạo calendar — wizard", "FUNC-004", "Normal",
       "Wizard loại スタッフ: màn tạo staff hiện 2 ô, validate tên và số tiền",
       ADM + "\n- Đang ở màn tạo staff của wizard loại スタッフ (màn 7)",
       "1. Quan sát giao diện\n2. Bỏ trống tên staff → next\n3. Nhập 50 ký tự → next\n"
       "4. Nhập 51 ký tự → next\n5. Bỏ trống số tiền staff → next\n"
       "6. Nhập 5000 → next\n7. Nhập -100 / 1.5 / abc",
       "Tên 50 và 51 ký tự · 5000 · -100 · 1.5 · abc",
       "- B1: hiện đúng 2 ô nhập cho 2 staff\n- B2: required\n- B3: lưu thành công\n"
       "- B4: báo lỗi\n- B5: lưu thành công, tự fill 0, list hiện「設定なし」\n"
       "- B6: format 5,000\n- B7: invalid",
       note="Nguồn: Calendar list r208-r215."),

    tc("Tạo calendar — wizard", "FUNC-002", "Abnormal",
       "Wizard loại スタッフ: chưa set đủ lịch làm việc 2 staff thì không đi tiếp được",
       ADM + "\n- Đang ở màn chọn thời gian làm việc của wizard loại スタッフ (màn 11)",
       "1. Cả 2 staff chưa set giờ → bấm「次にすすむ >」\n"
       "2. Chỉ staff 1 set giờ → bấm next\n3. Chỉ staff 2 set giờ → bấm next\n"
       "4. Cả 2 staff đã set giờ → bấm next",
       "2 staff S1, S2",
       "- B1, B2, B3: lỗi「必ずスタッフ2名の3日分のシフトを登録してください（仮のシフトでも構いません」\n"
       "- B4: mở màn tạo course (màn 14)",
       note="Nguồn: Calendar list r230-r233."),

    tc("Tạo calendar — wizard", "FUNC-002", "Normal",
       "Wizard loại スタッフ: chọn staff nào thì hiện lịch làm việc của staff đó, có nút back",
       ADM + "\n- Đang ở màn chọn thời gian làm việc của wizard loại スタッフ",
       "1. Quan sát staff được chọn mặc định\n2. Bấm chọn staff 2\n3. Bấm「< 戻る」",
       "2 staff S1, S2",
       "- Mặc định hiện staff số 1\n- Chọn staff 2: hiện đúng lịch làm việc của staff 2\n"
       "- Nút back: về màn tạo staff (màn 7)",
       note="Nguồn: Calendar list r218-r219, r235."),

    tc("Tạo calendar — wizard", "FUNC-002", "Normal",
       "Popup edit giờ của staff: hiện đúng default theo trạng thái đã set trước đó",
       ADM + "\n- Đang ở popup edit giờ của staff trong wizard (màn 12)",
       "1. Mở popup cho ngày CHƯA set lịch\n2. Mở popup cho ngày đã set 08:00-17:00\n"
       "3. Mở popup cho ngày đã set 24h\n4. Mở popup cho ngày đã set nghỉ",
       "Các ngày ở 4 trạng thái khác nhau",
       "- Chưa set: hiện giờ default 10:00 ~ 21:00\n- Đã set: hiện đúng giờ bắt đầu - kết thúc\n"
       "- Đã set 24h: hiện tick chọn 24h\n- Ngày nghỉ: hiện tick chọn ngày nghỉ",
       note="Nguồn: Calendar list r236."),

    tc("Tạo calendar — wizard", "FUNC-002", "Boundary",
       "Ngày T7/CN đang là ngày nghỉ, thêm ca qua ngày cho T6 → chỉ hiển thị hết T6",
       ADM + "\n- Trong wizard, T7 và CN đã set là ngày nghỉ",
       "1. Thêm lịch làm việc thứ 6 dạng qua ngày (vd 20:00~06:00)\n"
       "2. Quan sát hiển thị T6 và T7",
       "T6 20:00~06:00 · T7 và CN = ngày nghỉ",
       "- Add thành công nhưng CHỈ hiển thị đến hết thứ 6\n- T7 vẫn hiển thị là ngày nghỉ",
       note="Nguồn: Calendar list r176, r279. ⚠ Quản lý calendar r2429 lại ghi「nếu đã add t7 cn là ngày "
            "nghỉ khi add lịch qua ngày sẽ báo lỗi」— 2 kết quả khác nhau, xem MT-06."),

    # ══════════════ 3. Giới hạn theo plan ══════════════
    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Boundary",
       "Plan free: tối đa 1 calendar 個人 + 1 calendar スタッフ",
       ADM + "\n- Bot A đang ở plan free (hoặc plan_type = 2)\n- Bot A chưa có calendar nào",
       "1. Tạo calendar loại 個人 → thành công\n"
       "2. Tạo tiếp calendar loại 個人 → chọn loại 個人 → bấm next\n"
       "3. Tạo calendar loại スタッフ → thành công\n"
       "4. Khi đã có 2 calendar, bấm nút tạo mới",
       "Plan free",
       "- B1, B3: tạo thành công\n"
       "- B2: màn chọn loại tự nhảy sang loại スタッフ; nếu cố chọn 個人 rồi next → lỗi "
       "「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- B4: báo lỗi ngay, không mở được wizard",
       note="Nguồn: Calendar list r23-r27, r46. Spec BR-01. ⚠ §1.4 feature-spec ghi「2 tổng (bất kỳ loại)」"
            "mâu thuẫn BR-01「tối đa 1 mỗi loại」→ MT-01."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Normal",
       "Plan free: bộ đếm 登録カレンダー数 đúng theo từng filter",
       ADM + "\n- Bot free đã có 1 calendar 個人 và 1 calendar スタッフ",
       "1. Filter 全て → đọc bộ đếm\n2. Filter 個人 → đọc bộ đếm\n3. Filter スタッフ → đọc bộ đếm",
       "1 個人 + 1 スタッフ",
       "- 全て: 2/2\n- 個人: 1/1\n- スタッフ: 1/1",
       note="Nguồn: Calendar list r8, r28-r30."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Boundary",
       "Plan standard mới (flag_contract_new=1): tối đa 3 個人 + 3 スタッフ",
       ADM + "\n- Bot A plan standard, `flag_contract_new` = 1",
       "1. Tạo đủ 3 calendar 個人 → tạo calendar 個人 thứ 4\n"
       "2. Tạo đủ 3 calendar スタッフ → tạo calendar スタッフ thứ 4\n"
       "3. Khi tổng = 6, bấm nút tạo mới\n4. Đọc bộ đếm ở 3 filter",
       "Plan standard flag_contract_new = 1",
       "- B1, B2: báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- B3: báo lỗi ngay khi bấm tạo mới\n"
       "- B4: 全て = n/6, 個人 = n/3, スタッフ = n/3",
       note="Nguồn: Calendar list r10-r11, r31-r38, r74-r81. Spec BR-01."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Boundary",
       "Plan pro / standard cũ (flag_contract_new=0): tối đa 10 個人 + 10 スタッフ",
       ADM + "\n- Bot A plan pro (hoặc standard với flag_contract_new = 0)",
       "1. Tạo đủ 10 calendar 個人 → tạo calendar 個人 thứ 11\n"
       "2. Tạo đủ 10 calendar スタッフ → tạo thứ 11\n"
       "3. Khi tổng = 20, bấm nút tạo mới\n4. Đọc bộ đếm ở 3 filter",
       "Plan pro",
       "- B1, B2: báo lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- B3: báo lỗi ngay\n- B4: 全て = n/20, 個人 = n/10, スタッフ = n/10",
       note="Nguồn: Calendar list r58-r73. Spec BR-01. ⚠ Calendar list r39-r40 lại ghi plan pro "
            "「không giới hạn số calendar, tạo calendar thứ 11 → cho phép」→ MT-02."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Normal",
       "Plan enterprise: giới hạn ăn theo standard hoặc pro tương ứng",
       ADM + "\n- Bot enterprise (standard) và bot enterprise (pro)",
       "1. Bot enterprise (standard): đọc bộ đếm + thử vượt giới hạn\n"
       "2. Bot enterprise (pro): đọc bộ đếm + thử vượt giới hạn",
       "2 bot enterprise khác loại",
       "- enterprise (standard): giống plan standard (3/3)\n"
       "- enterprise (pro): giống plan pro (10/10)",
       note="Nguồn: Calendar list r14-r15, r44-r45."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Boundary",
       "Plan free: tối đa 2 course và 2 staff mỗi calendar",
       CAL + "\n- Bot A plan free",
       "1. Tạo đủ 2 course → bấm「コース作成」lần 3\n"
       "2. Tạo đủ 2 staff → bấm「スタッフ作成」lần 3",
       "Plan free",
       "- Cả 2 bước: chặn tạo, báo lỗi giới hạn plan / yêu cầu upgrade\n"
       "- DB không sinh bản ghi course/staff thứ 3",
       note="Nguồn: Calendar list r47-r48; Quản lý course&staff r136, r142. Spec BR-02."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Boundary",
       "Hard limit 200 course / 200 staff / 100 câu hỏi trên MỌI plan",
       CAL + "\n- Bot A plan pro\n- Calendar đã có 200 course, 200 staff, 100 câu hỏi",
       "1. Bấm tạo course thứ 201 ở màn list (cả trường hợp có menu và không menu)\n"
       "2. Bấm copy 1 course để thành course thứ 201\n"
       "3. Bấm tạo staff thứ 201\n4. Thêm câu hỏi thứ 101 ở 予約時のお客様への質問項目",
       "200 course · 200 staff · 100 câu hỏi",
       "- B1, B2: lỗi「コース数の上限（200）を超えるため、これ以上作成できません。」\n"
       "- B3: lỗi「スタッフ数の上限（200）を超えるため、これ以上作成できません。」\n"
       "- B4: lỗi「質問数の上限（100）を超えるため、これ以上作成できません。」\n"
       "- Không bản ghi nào được tạo",
       note="Nguồn: Quản lý course&staff r132-r135, r140, r146, r152-r159. Spec BR-02. "
            "⚠ Calendar list r49-r54 (bot flag_contract_new=0) ghi「Không giới hạn」→ MT-02."),

    tc("Giới hạn theo plan", "PAY-LIMIT-001", "Normal",
       "Bot plan free bấm bật 決済機能 ở form course → hiện cảnh báo + link upgrade",
       CAL + "\n- Bot A plan free",
       "1. Vào form tạo/sửa course\n2. Quan sát vùng cảnh báo phí\n3. Bấm link「アップグレード」",
       "Plan free",
       "- Hiện text「決済機能の利用は、有料プランにアップグレードする必要があります。」\n"
       "- Bấm アップグレード → mở tab mới /admin/bot-add?upgrade_bot_id={id bot đã mã hóa}",
       note="Nguồn: Quản lý course&staff r260."),
]
