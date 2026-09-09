# -*- coding: utf-8 -*-
"""FA-021 イベント予約 — Nhóm 25-29: admin duyệt/từ chối · đặt hộ & sửa booking ·
danh sách người tham gia · export CSV · đếm 定員.

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Task nhỏ + fix bug KH」r13-r19 (Bug #26616 — highlight thông tin đã đổi),
    r109-r199 (Bug KH #38200, 06/2026 — ma trận duyệt/từ chối × loại friend info × web/app),
    r243-r293 (Bug Tester #38312, 06/2026 — lịch sử friend info + action preview),
    r68-r92 (bộ đếm use_people / remain_limit)
  - tab「Event booking 1.0」r318-r351 (màn danh sách người tham gia, detail, admin đặt hộ)
  - tab「Event booking 2.0」r81-r93 (Bug tự detect — đổi slot không hiện list コース)
  - tab「Event booking 3.0」r3-r17 (07/2023 — export CSV thêm cột friend info)
"""
from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A\n"
       "- Event E có 開催日 2026-09-01, slot S1 10:00〜12:00 với コース P1")
REQ = ADM + "\n- Slot S1 承認方法 = リクエスト制, đang có booking `status = 3` của LINE user U1"

S5 = [
    # ══════════════════ 25. Admin — duyệt / từ chối booking ══════════════════
    tc("Admin — duyệt / từ chối booking", "FUNC-001", "Normal",
       "Duyệt booking ở WEB có chọn gửi action → duyệt thành công, gửi action, ghi lịch sử, đẩy notify app",
       REQ + "\n- Slot đã set action「admin duyệt」\n- Đã cài app mobile nhận notify",
       "1. Admin mở màn 参加者リスト → chọn booking của U1 → bấm duyệt, chọn **có** gửi action\n"
       "2. Quan sát badge trạng thái booking\n3. Mở LINE app phía U1 đọc tin\n"
       "4. Mở chat 1:1 phía admin xem trigger\n5. Mở màn detail friend U1 xem lịch sử\n"
       "6. Kiểm tra notify trên app mobile",
       "Duyệt ở web, chọn có action",
       "- Duyệt thành công, badge chuyển sang trạng thái đã duyệt\n"
       "- U1 **nhận được action duyệt** trên LINE, chat 1:1 hiển thị tin đã gửi\n"
       "- Lịch sử duyệt được tạo, xem được ở màn detail LINE user\n- App mobile nhận notify",
       note="Nguồn: Task nhỏ + fix bug KH r109 (Bug KH #38200, 06/2026). RULE-06 + RULE-07."),

    tc("Admin — duyệt / từ chối booking", "FUNC-001", "Normal",
       "Duyệt booking ở WEB — hoạt động đúng với MỌI loại friend info trong form (12 biến thể)",
       REQ + "\n- Chuẩn bị các booking với cấu hình form khác nhau theo cột Dữ liệu test",
       "1. Với từng biến thể, admin duyệt booking ở web (chọn có action)\n"
       "2. Kiểm tra: trạng thái booking / action gửi cho user / lịch sử duyệt / notify app",
       "(1) chỉ info số điện thoại (-2) · (2) chỉ ngày sinh (-4) · (3) chỉ tỉnh (-6) · "
       "(4) đủ cả 3 info trên · (5) chỉ info thường (text, select, địa chỉ -7/-8/-9/-10) · "
       "(6) chỉ name + email · (7) có tất cả loại info · (8) không có info nào · "
       "(9) giá trị số điện thoại rỗng · (10) giá trị ngày sinh rỗng · (11) giá trị tỉnh rỗng · "
       "(12) số điện thoại chứa ký tự đặc biệt (dấu - + khoảng trắng)",
       "- **Cả 12 biến thể**: duyệt thành công, badge chuyển đã duyệt\n"
       "- Gửi được action duyệt cho user (kiểm ở LINE + chat 1:1)\n"
       "- Tạo được lịch sử duyệt, xem ở màn detail LINE user\n- Gửi được notify qua app mobile",
       note="Nguồn: Task nhỏ r109-r120 (Bug KH #38200 — bug gốc: đặt chỗ event hiện「đã đặt」phía user dù admin "
            "chưa duyệt, với リクエスト制). 12 input cùng 1 kết quả mong đợi → gộp 1 TC theo quy tắc tách TC."),

    tc("Admin — duyệt / từ chối booking", "FUNC-001", "Normal",
       "Duyệt booking ở WEB sau khi ADMIN SỬA friend info trong booking → vẫn duyệt và gửi action đúng",
       REQ + "\n- Booking của U1 có các info: số điện thoại, ngày sinh, tỉnh, info khác",
       "1. Admin mở booking, sửa giá trị số điện thoại → bấm duyệt (có action)\n"
       "2. Lặp lại với: sửa ngày sinh / sửa tỉnh / sửa info khác\n"
       "3. Mỗi lần kiểm tra: trạng thái booking / action / lịch sử / notify",
       "4 loại field bị sửa trước khi duyệt",
       "- Cả 4 trường hợp: duyệt thành công, gửi action, tạo lịch sử, gửi notify\n"
       "- Giá trị info đã sửa được lưu đúng vào booking",
       note="Nguồn: Task nhỏ r121-r124."),

    tc("Admin — duyệt / từ chối booking", "MSG-004", "Normal",
       "Duyệt booking ở WEB chọn KHÔNG gửi action → xác nhận hành vi gửi action",
       REQ + "\n- Slot đã set action「admin duyệt」",
       "1. Admin duyệt booking, chọn **không** gửi action\n2. Mở LINE app phía U1 kiểm tra có tin không\n"
       "3. Mở chat 1:1 phía admin\n4. Kiểm tra lịch sử duyệt + notify app\n"
       "5. Lặp lại thao tác tương tự trên **app mobile** để đối chứng",
       "Web: chọn không action · App: chọn không action",
       "- **App mobile (đã xác nhận trong corpus)**: KHÔNG gửi action cho user; vẫn tạo lịch sử + notify\n"
       "- **Web**: ghi rõ hành vi thật — theo logic phải KHÔNG gửi action giống app\n"
       "⚠ Nếu web VẪN gửi action khi chọn「không action」→ **RAISE BUG**",
       note="⚠ MT-01 — corpus TỰ MÂU THUẪN: khối web「chọn không action」(Task nhỏ r125-r140) ghi expected "
            "「Send được action approve cho user」giống hệt khối「chọn có action」(r109-r124), trong khi khối app "
            "(r170-r185) ghi「Không send action」. Spec Field Matrix #54 cảnh báo `action_before_booking` "
            "**`0` = CÓ thực thi** (tên ngược nghĩa). CẦN LEADER CHỐT trước khi chạy."),

    tc("Admin — duyệt / từ chối booking", "SYNC-APP-001", "Normal",
       "Duyệt booking ở APP MOBILE (màn quản lý event) chọn CÓ action — đúng với mọi loại friend info",
       REQ + "\n- Đã cài app mobile, đăng nhập cùng tài khoản admin\n- Booking chờ duyệt của U1",
       "1. Mở app mobile → màn quản lý event booking → chọn booking\n"
       "2. Bấm duyệt, chọn **có** gửi action\n"
       "3. Lặp lại với 12 biến thể friend info như bộ TC ở web\n"
       "4. Mỗi lần kiểm tra: trạng thái / action / lịch sử / notify",
       "12 biến thể friend info (giống ma trận web)",
       "- Cả 12 biến thể: duyệt thành công, badge đã duyệt\n"
       "- Gửi được action duyệt cho user\n- Tạo được lịch sử duyệt\n- Gửi được notify",
       note="Nguồn: Task nhỏ r154-r169. ⚠ RULE-01: quan điểm `SYNC-APP-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Admin — duyệt / từ chối booking", "SYNC-APP-001", "Normal",
       "Duyệt booking ở APP MOBILE chọn KHÔNG action → KHÔNG gửi action nhưng vẫn tạo lịch sử + notify",
       REQ + "\n- Đã cài app mobile\n- Slot đã set action「admin duyệt」",
       "1. Ở app mobile duyệt booking, chọn **không** gửi action\n"
       "2. Mở LINE app phía U1 kiểm tra\n3. Kiểm tra lịch sử duyệt ở màn detail friend\n4. Kiểm tra notify",
       "App mobile, chọn không action, 12 biến thể friend info",
       "- Duyệt thành công, badge đã duyệt\n- **KHÔNG gửi action** cho U1 (LINE không có tin mới)\n"
       "- **Vẫn tạo lịch sử** duyệt và **vẫn gửi notify**",
       note="Nguồn: Task nhỏ r170-r185. Đây là hành vi đã được xác nhận rõ trong corpus, dùng làm căn cứ đối "
            "chứng cho MT-01."),

    tc("Admin — duyệt / từ chối booking", "MSG-004", "Normal",
       "Từ chối booking — có / không gửi action, preview action ở lịch sử khác nhau",
       REQ + "\n- Event có setting info default và U1 đã nhập thông tin đó\n"
       "- Slot đã set action「admin từ chối」",
       "1. Admin từ chối booking, chọn **có** action → kiểm tra LINE + lịch sử + notify\n"
       "2. Với booking khác, từ chối chọn **không** action → kiểm tra tương tự\n"
       "3. Ở mỗi trường hợp mở màn detail LINE user xem cột preview action của lịch sử",
       "Từ chối + có action · Từ chối + không action",
       "- Có action: badge chuyển 否認; **gửi action từ chối** cho U1; lịch sử từ chối được tạo và "
       "**preview action HIỆN nội dung action**; gửi notify\n"
       "- Không action: badge chuyển 否認; **KHÔNG gửi action**; lịch sử vẫn được tạo nhưng "
       "**preview action KHÔNG hiện nội dung action**; vẫn gửi notify",
       note="Nguồn: Task nhỏ r141-r142 (web) và r186-r187 (app mobile). 2 nhánh giữ chung 1 TC vì là cặp "
            "đối chứng của cùng 1 hành động."),

    tc("Admin — duyệt / từ chối booking", "MSG-004", "Normal",
       "Xử lý request ĐỔI LỊCH — 4 tổ hợp duyệt/từ chối × có/không action",
       ADM + "\n- U1 có cặp booking `status = 6` (request change)\n"
       "- Slot đã set 4 action nhóm 予約変更時",
       "1. Duyệt request change + **có** action → kiểm tra booking / LINE / lịch sử+preview / notify\n"
       "2. Duyệt request change + **không** action → kiểm tra tương tự\n"
       "3. Từ chối request change + **có** action → kiểm tra\n"
       "4. Từ chối request change + **không** action → kiểm tra",
       "4 tổ hợp",
       "- Duyệt + có action: booking được duyệt đổi; **gửi action duyệt đổi**; lịch sử có preview action; có notify\n"
       "- Duyệt + không action: booking được duyệt đổi; **KHÔNG gửi action**; lịch sử KHÔNG có preview action; có notify\n"
       "- Từ chối + có action: booking **KHÔNG được duyệt đổi**; gửi action từ chối; lịch sử có preview; có notify\n"
       "- Từ chối + không action: booking KHÔNG được duyệt đổi; KHÔNG gửi action; lịch sử không preview; có notify",
       note="Nguồn: Task nhỏ r143-r146 (web) và r188-r191 (app mobile)."),

    tc("Admin — duyệt / từ chối booking", "MSG-004", "Normal",
       "Xử lý request HỦY — 4 tổ hợp duyệt/từ chối × có/không action",
       ADM + "\n- U1 có booking `status = 7` (request cancel)\n- Slot đã set 4 action nhóm キャンセル時",
       "1. Duyệt request cancel + **có** action → kiểm tra booking / LINE / lịch sử+preview / notify\n"
       "2. Duyệt request cancel + **không** action → kiểm tra\n"
       "3. Từ chối request cancel + **có** action → kiểm tra\n"
       "4. Từ chối request cancel + **không** action → kiểm tra",
       "4 tổ hợp",
       "- Duyệt + có action: booking được duyệt hủy; gửi action duyệt hủy; lịch sử có preview; có notify\n"
       "- Duyệt + không action: được duyệt hủy; KHÔNG gửi action; lịch sử không preview; có notify\n"
       "- Từ chối + có action: booking **KHÔNG được hủy**; gửi action từ chối hủy; lịch sử có preview; có notify\n"
       "- Từ chối + không action: KHÔNG được hủy; KHÔNG gửi action; lịch sử không preview; có notify",
       note="Nguồn: Task nhỏ r147-r150 (web) và r192-r195 (app mobile)."),

    tc("Admin — duyệt / từ chối booking", "STATE-DEP-001", "Normal",
       "Đổi trạng thái booking từ 否認 sang 承認 → gửi action, tạo lịch sử, thêm lại remind",
       ADM + "\n- Booking của U1 đang `status = 2` (否認)\n- Slot bật remind và đã set action",
       "1. Admin mở booking → đổi trạng thái sang 承認\n2. Query `status`\n"
       "3. Query bảng `user_event`\n4. Đọc tin trên LINE app + chat 1:1\n5. Kiểm tra lịch sử + notify",
       "status 2 → 1",
       "- `status` = **1**\n- Có gửi action đổi booking\n"
       "- **Có thêm bản ghi remind** vào `user_event`\n- Tạo được lịch sử + gửi notify",
       note="Nguồn: Task nhỏ r151 + r51「admin change status từ cancel (status =4) sang đã approve (status = 5) "
            "=> add remind tương ứng cho booking đó」."),

    tc("Admin — duyệt / từ chối booking", "PERM-004", "Normal",
       "Account STAFF duyệt booking → duyệt được, KHÔNG gửi action, lịch sử ghi đúng tên staff",
       ADM + "\n- Có account staff Y được cấp quyền màn event booking\n"
       "- Booking `status = 3` của U1, slot đã set action「admin duyệt」",
       "1. Đăng nhập bằng account staff Y\n2. Duyệt booking của U1\n"
       "3. Mở LINE app phía U1 kiểm tra có tin action không\n"
       "4. Mở màn detail friend U1 → xem lịch sử, đọc tên người thao tác\n5. Kiểm tra notify",
       "Account staff Y",
       "- Duyệt thành công, badge đã duyệt\n- **KHÔNG gửi action** duyệt cho U1\n"
       "- Lịch sử duyệt hiện **đúng tên user staff** đã thao tác\n- Có gửi notify",
       note="Nguồn: Task nhỏ r152「Check account staff nhấn approve booking → Admin approve được booking success, "
            "KHÔNG send action approve cho user, tạo được lịch sử approve booking hiện đúng tên user staff thao tác」. "
            "⚠ Hành vi 'staff duyệt thì không gửi action' rất phản trực giác → xem MT-23."),

    tc("Admin — duyệt / từ chối booking", "CONC-001", "Abnormal",
       "Bấm duyệt NHIỀU booking liên tiếp → không phát sinh lỗi, mọi booking đều được xử lý đúng",
       ADM + "\n- Có 10 booking `status = 3` ở cùng slot, `use_people` ban đầu = 0",
       "1. Admin bấm duyệt liên tiếp 10 booking (không chờ mỗi lần xong)\n"
       "2. Đếm số booking `status = 1`\n3. Đọc `b_slot.use_people`\n"
       "4. Đếm số tin action U1..U10 nhận được\n5. Lặp lại thao tác này trên app mobile",
       "10 booking, mỗi booking quantity = 1",
       "- Không phát sinh lỗi trên GUI\n- **Đủ 10** booking chuyển `status = 1`\n"
       "- `use_people` = **10** (khớp phép tính tay), không thiếu không thừa\n"
       "- Mỗi user nhận đúng 1 tin action",
       note="Nguồn: Task nhỏ r153 (web) và r199 (app mobile). Expected về bộ đếm do AI bổ sung theo CONC-001 "
            "+ spec TD-01/TD-17 (không transaction, 2 cơ chế cập nhật bộ đếm khác nhau → nguy cơ drift)."),

    tc("Admin — duyệt / từ chối booking", "SYNC-APP-001", "Normal",
       "Xử lý request booking / change / cancel từ MÀN NOTIFY của app mobile",
       ADM + "\n- Đã cài app mobile\n- Có 3 booking: 1 chờ duyệt, 1 request change, 1 request cancel\n"
       "- App đã nhận đủ 3 notify",
       "1. Mở app → màn notify → mở notify của booking chờ duyệt → thao tác duyệt\n"
       "2. Mở notify của request change → thao tác duyệt\n3. Mở notify của request cancel → thao tác duyệt\n"
       "4. Sau mỗi lần, kiểm tra trạng thái booking + tin trên LINE của user",
       "3 loại request, thao tác từ màn notify",
       "- Cả 3 loại đều thao tác được từ màn notify\n"
       "- Trạng thái booking và tin action gửi cho user **giống hệt** khi thao tác từ màn quản lý event",
       note="Nguồn: Task nhỏ r196-r198 (TC gốc chỉ có tiêu đề, không có expected) → expected do AI viết theo "
            "SYNC-APP-001, cần Leader xác nhận."),

    tc("Admin — duyệt / từ chối booking", "SYNC-APP-001", "Abnormal",
       "App mobile KHÔNG cho đổi lịch, chỉ có nút duyệt / từ chối",
       ADM + "\n- Đã cài app mobile\n- Có 1 booking bất kỳ",
       "1. Mở app → màn quản lý event booking → mở detail booking\n2. Quan sát các nút thao tác\n"
       "3. Lặp lại khi mở từ màn notify",
       "App mobile, cả 2 điểm vào",
       "- **KHÔNG có chức năng đổi lịch (change booking)** trên app\n"
       "- Chỉ có nút duyệt / từ chối",
       note="Nguồn: Event booking 2.0 r70 và r75「ở app không cho change booking, chỉ có nút để approve/deny」."),

    tc("Admin — duyệt / từ chối booking", "MSG-004", "Normal",
       "Tin gửi khi duyệt / từ chối request đổi lấy dữ liệu từ đúng booking (Bug #32366)",
       ADM + "\n- U1 có cặp booking `status = 6`: gốc (2026-09-01 10:00, コース P_a 3000円, 1 chỗ) và "
       "mới (2026-09-08 14:00, コース P_b 8000円, 2 chỗ)\n- Action change có chèn đủ 5 biến",
       "1. Admin mở detail booking **GỐC** → bấm duyệt → đọc tin U1 nhận được\n"
       "2. Chuẩn bị cặp tương tự, mở detail booking **MỚI** → bấm duyệt → đọc tin\n"
       "3. Chuẩn bị cặp tương tự, mở booking **GỐC** → bấm **từ chối** → đọc tin\n"
       "4. Chuẩn bị cặp tương tự, mở booking **MỚI** → bấm **từ chối** → đọc tin\n"
       "5. Lặp lại toàn bộ 4 bước trên app mobile",
       "Booking gốc: 2026-09-01 · 10:00 · 1 chỗ · 3.000円\n"
       "Booking mới: 2026-09-08 · 14:00 · 2 chỗ · 16.000円",
       "- **Duyệt** (từ gốc hoặc từ mới): tin replace theo **booking MỚI** — 2026-09-08 / 14:00 / 2 / 16.000円\n"
       "- **Từ chối** (từ gốc hoặc từ mới): tin replace theo **booking GỐC** — 2026-09-01 / 10:00 / 1 / 3.000円\n"
       "- **KHÔNG trường nào bị để trống** (đây chính là hiện tượng của bug #32366)",
       note="Nguồn: Event booking 2.0 r65-r79 (Bug #32366, 10/2025 — nguyên nhân: approve/deny xóa 1 booking "
            "nên mất data khi replace). 8 điểm thao tác nhưng chỉ 2 kết quả khác nhau → gộp thành 1 TC ma trận."),

    # ══════════════════ 26. Admin — đặt chỗ hộ & sửa booking ══════════════════
    tc("Admin — đặt chỗ hộ & sửa booking", "FUNC-001", "Normal",
       "Admin đặt chỗ hộ cho friend → tạo booking, LUÔN gửi action của luồng được duyệt ngay",
       ADM + "\n- Slot S1 承認方法 = リクエスト制 (chờ duyệt)\n"
       "- Slot đã set action「booking được duyệt ngay」và action「booking chờ duyệt」khác nhau\n"
       "- Có friend U1 trong danh sách",
       "1. Admin mở màn đặt chỗ hộ (SCR-EBD-13)\n2. Chọn friend U1, chọn ngày/slot/コース/số lượng\n"
       "3. Điền form → lưu\n4. Query `b_user_booking`\n5. Đọc tin U1 nhận được trên LINE",
       "Slot リクエスト制 nhưng admin đặt hộ",
       "- Booking được tạo\n"
       "- U1 nhận **action của「booking được approve luôn」**, KHÔNG phải action chờ duyệt",
       note="Nguồn: Event booking 1.0 r280「check admin book mới → Luôn gửi action của booking được approve luôn」."),

    tc("Admin — đặt chỗ hộ & sửa booking", "FUNC-002", "Abnormal",
       "Đặt chỗ hộ — validate các trường bắt buộc",
       ADM + "\n- Đang ở màn đặt chỗ hộ",
       "1. Không chọn friend → lưu → ghi message\n2. Không chọn ngày → lưu → ghi message\n"
       "3. Không chọn giờ (slot) → lưu → ghi message\n4. Slot có コース nhưng không chọn コース → lưu\n"
       "5. Nhập số lượng = 0 → lưu → ghi message",
       "5 trường bắt buộc để trống lần lượt",
       "- Không chọn friend:「友だち名は必須です」\n- Không chọn ngày:「日程を選択してください」\n"
       "- Không chọn giờ:「開催時間は必ず指定してください。」\n- Không chọn コース:「コースは必須です。」\n"
       "- Số lượng 0:「参加人数は1以上にしてください。」\n- Cả 5 trường hợp đều **chặn lưu**",
       note="Nguồn: spec Field Matrix #47/#48/#49/#50. Corpus Event booking 1.0 r351「Admin booking」chỉ có "
            "tiêu đề → expected lấy text message từ spec."),

    tc("Admin — đặt chỗ hộ & sửa booking", "LIST-001", "Abnormal",
       "Danh sách friend ở màn đặt chỗ hộ khi bot có > 100 bạn bè",
       "- Bot A có **hơn 100** friend\n- Có 1 friend tên đặc trưng nằm ngoài 100 friend đầu tiên "
       "(VD friend thứ 150 theo thứ tự trả về)",
       "1. Mở màn đặt chỗ hộ\n2. Mở dropdown chọn friend, đếm số friend hiển thị\n"
       "3. Gõ tìm kiếm tên friend thứ 150\n4. Quan sát kết quả",
       "Bot có >100 friend; tìm friend thứ 150",
       "- Ghi rõ số friend thực tế hiển thị trong dropdown\n"
       "- Nếu **không tìm được** friend thứ 150 → **RAISE BUG**: không đặt chỗ hộ được cho phần lớn friend",
       note="Nguồn: spec TD-12 (`ajaxGetAllSlotEvent` hardcode `limit(100)` cho danh sách bạn bè) + "
            "Field Matrix #50 (⚠ Danh sách hardcode limit(100)). Corpus KHÔNG có TC này → GAP, xem MT-24."),

    tc("Admin — đặt chỗ hộ & sửa booking", "UI-003", "Normal",
       "Sửa booking — thông tin ĐÃ THAY ĐỔI hiện màu ĐỎ, thông tin không đổi hiện màu xám",
       ADM + "\n- Booking B của U1 đã có: ngày 2026-09-01, giờ 10:00, コース P1, số lượng 1, friend info đã điền\n"
       "- Ngày 2026-09-01 có nhiều slot giờ khác nhau",
       "1. Admin mở màn sửa booking B\n2. Lần lượt thực hiện 5 thao tác và quan sát màu chữ mỗi lần:\n"
       "   đổi ngày · đổi giờ (slot khác cùng ngày) · đổi コース · đổi số lượng · đổi friend info\n"
       "3. Mở lại màn sửa, KHÔNG đổi gì → quan sát màu chữ",
       "5 loại thay đổi + 1 trường hợp không đổi",
       "- Cả 5 loại thay đổi: thông tin bị đổi hiện **màu ĐỎ**\n"
       "- Không đổi gì: thông tin hiện **màu XÁM**\n"
       "- Đặc biệt: đổi sang **slot giờ khác trong cùng 1 ngày** cũng phải hiện màu đỏ",
       note="Nguồn: Task nhỏ r13-r19 (Bug #26616, 09/2024)：「1 ngày có nhiều slot time khác nhau thì khi change "
            "sang time khác chưa hiển thị text màu đỏ」. Đây là bug đã fix, giữ làm regression."),

    tc("Admin — đặt chỗ hộ & sửa booking", "UI-FIELD-001", "Normal",
       "Sửa booking — đổi slot thì ô chọn コース hiện/ẩn và load đúng danh sách コース của slot mới",
       ADM + "\n- Chuẩn bị 4 tổ hợp: booking ban đầu ở slot KHÔNG コース / CÓ コース × đổi sang slot "
       "KHÔNG コース / CÓ コース\n- Booking đang ở `status = 1` (đã duyệt)",
       "1. Với từng tổ hợp: mở màn sửa booking, đổi slot\n2. Quan sát ô chọn コース\n"
       "3. Nếu có ô chọn コース thì click mở xem danh sách\n4. Lưu booking → kiểm tra slot/コース đã update",
       "4 tổ hợp slot nguồn × slot đích",
       "- Đổi sang slot **KHÔNG có コース**: **không hiện** ô chọn コース\n"
       "- Đổi sang slot **CÓ コース**: **hiện** ô chọn コース, click vào **load được danh sách コース của "
       "slot đang chọn** (không phải slot cũ)\n- Lưu xong: slot/コース cập nhật đúng",
       note="Nguồn: Event booking 2.0 r81-r84 (Bug TỰ DETECT：「Admin change booking chọn sang slot có plan "
            "nhưng không hiện được list plan」)."),

    tc("Admin — đặt chỗ hộ & sửa booking", "STATE-001", "Normal",
       "Sửa slot/コース của booking — cho phép với status 1/2/3/4/5, CHẶN với status 6/7",
       ADM + "\n- Chuẩn bị 7 booking của U1 với `status` lần lượt = 1, 2, 3, 4, 5, 6, 7",
       "1. Với từng booking, admin mở màn detail/sửa\n2. Quan sát ô chọn slot và コース\n"
       "3. Nếu sửa được thì đổi slot/コース → lưu → kiểm tra kết quả",
       "7 booking ở 7 trạng thái",
       "- `status` = 1, 2, 3, 4, 5: **sửa được** slot/コース; lưu xong cập nhật đúng\n"
       "- `status` = **6 (変更リクエスト)** và **7 (キャンセルリクエスト)**: "
       "**KHÔNG cho phép sửa** slot/コース",
       note="Nguồn: Event booking 2.0 r81, r85, r89-r93. 7 trạng thái nhưng chỉ 2 kết quả → gộp 1 TC ma trận."),

    tc("Admin — đặt chỗ hộ & sửa booking", "FUNC-001", "Normal",
       "Admin đổi lịch cho user → cập nhật NGAY, không tạo request",
       ADM + "\n- Booking B của U1 `status = 1` ở slot A, slot A có 予約変更 = リクエスト制",
       "1. Admin mở màn sửa booking B, đổi sang slot B → lưu\n"
       "2. Đếm số bản ghi `b_user_booking` của U1 trong event\n3. Query `status`",
       "Admin đổi lịch khi slot là リクエスト制",
       "- Chỉ có **1** bản ghi booking (KHÔNG tạo cặp status = 6)\n"
       "- `status` giữ nguyên = 1, `slot_id` = slot B\n"
       "- Admin thao tác được update luôn, không cần chờ duyệt",
       note="Nguồn: Event booking 1.0 r296「admin change thì sẽ được update luôn」."),

    tc("Admin — đặt chỗ hộ & sửa booking", "FUNC-001", "Normal",
       "Admin hủy booking → status = 4, gửi action hủy được duyệt ngay, trừ bộ đếm, xóa remind",
       ADM + "\n- Booking B của U1 `status = 5`, slot bật remind, `use_people` = 1",
       "1. Admin mở booking B → bấm hủy\n2. Query `status`\n3. Đọc `use_people` / `remain_limit`\n"
       "4. Query `user_event`\n5. Đọc tin U1 nhận được trên LINE",
       "Admin hủy 1 booking",
       "- `status` = **4**\n- Gửi **action「cancel được approve luôn」**\n"
       "- `use_people` / `remain_limit` giảm đúng\n- Bản ghi `user_event` remind **bị xóa**",
       note="Nguồn: Event booking 1.0 r311 + r295 + Task nhỏ r50."),

    tc("Admin — đặt chỗ hộ & sửa booking", "FRIEND-001", "Normal",
       "Admin đặt hộ / duyệt / sửa booking — ghi friend info và tạo lịch sử với cột action đúng",
       ADM + "\n- Event có form gồm các item liên kết friend info theo cột Dữ liệu test\n"
       "- Có friend U1 chưa có giá trị các info đó",
       "1. Admin đặt chỗ hộ cho U1 với đủ các loại info → mở màn lịch sử friend info của U1\n"
       "2. Đọc cột action của từng bản ghi lịch sử\n"
       "3. Với info select có setting action, click vào cột action\n"
       "4. Lặp lại toàn bộ với thao tác **duyệt booking** và **sửa friend info của booking**",
       "Info liên kết: name · email · số điện thoại · tỉnh · text · select KHÔNG có action ở value · "
       "select CÓ action ở value",
       "- Mọi loại info: booking/duyệt/sửa thành công, **gán được giá trị info cho user**\n"
       "- Lịch sử friend info được tạo; cột action hiện **「設定なし」** với các info không có action\n"
       "- Riêng **select có setting action ở value**: cột action hiện **「プレビュー」**, "
       "click vào **hiện được preview action**",
       note="Nguồn: Task nhỏ r243-r266 (Bug Tester #38312, 06/2026 —「Khi lưu lịch sử thay đổi friend info chưa "
            "lưu được action preview」). 3 luồng (đặt hộ / duyệt / sửa) × 7 loại info nhưng chỉ 2 kết quả khác "
            "nhau → gộp 1 TC ma trận."),

    tc("Admin — đặt chỗ hộ & sửa booking", "FRIEND-001", "Normal",
       "Event có info KHÔNG liên kết friend info → booking thành công nhưng KHÔNG gán hồ sơ",
       ADM + "\n- Event E có form gồm các item KHÔNG liên kết friend info",
       "1. Admin đặt chỗ hộ cho U1 → mở màn detail friend U1\n"
       "2. So sánh toàn bộ friend info trước/sau\n3. Kiểm tra lịch sử friend info\n"
       "4. Lặp lại với thao tác duyệt booking và sửa booking",
       "Form không liên kết friend info nào",
       "- Booking thành công ở cả 3 luồng\n- **KHÔNG gán friend info** nào cho U1\n"
       "- **KHÔNG sinh bản ghi lịch sử** friend info",
       note="Nguồn: Task nhỏ r243, r251, r259, r267, r275, r283."),

    tc("Admin — đặt chỗ hộ & sửa booking", "SYNC-APP-001", "Normal",
       "App mobile — admin đặt chỗ hộ và duyệt booking cũng ghi friend info + lịch sử đúng",
       ADM + "\n- Đã cài app mobile (⚠ app KHÔNG có chức năng sửa booking)\n"
       "- Event có form liên kết đủ 7 loại friend info",
       "1. Ở app mobile: admin đặt chỗ hộ cho U1 → kiểm tra friend info + lịch sử + cột action\n"
       "2. Ở app mobile: admin duyệt 1 booking chờ duyệt → kiểm tra tương tự",
       "7 loại info, 2 luồng trên app",
       "- Cả 2 luồng: gán được giá trị info, tạo lịch sử\n"
       "- Cột action: **「設定なし」** với info không có action; **「プレビュー」** click ra được preview "
       "với select có action",
       note="Nguồn: Task nhỏ r267-r282."),

    tc("Admin — đặt chỗ hộ & sửa booking", "STATE-DEP-001", "Abnormal",
       "Lịch sử friend info khi action của value select bị XÓA sau khi đã tạo lịch sử",
       ADM + "\n- Event booking có form link friend info dạng select; 1 value của select đã setting action",
       "1. Setting friend info select value có action\n"
       "2. Admin đặt chỗ hộ cho U1 gán đúng value đó → tạo lịch sử\n"
       "3. Vào màn setting friend info **xóa action** của value đó\n"
       "4. Mở lại màn lịch sử friend info của U1 → quan sát cột action\n5. Click vào cột action",
       "Value select có action → xóa action",
       "- Màn lịch sử **mở được bình thường, không lỗi 500**\n"
       "- Ghi rõ hành vi thật của cột action: vẫn hiện「プレビュー」(preview nội dung cũ đã lưu) "
       "hay chuyển thành「設定なし」\n- Click vào không gây lỗi",
       note="Nguồn: Task nhỏ r291 (C-NEW-01 do AI đề xuất trong bộ human). Kết quả cần Leader chốt — xem MT-25."),

    tc("Admin — đặt chỗ hộ & sửa booking", "REG-SHARED-001", "Normal",
       "Regression — info KHÔNG có action vẫn hiển thị 設定なし ổn định sau fix #38312",
       ADM + "\n- Friend info các loại KHÔNG setting action: name / email / số điện thoại / tỉnh / text / "
       "select-không-action",
       "1. Gán các info không-action qua luồng event booking (đặt hộ / duyệt / sửa / callback bill)\n"
       "2. Mở màn lịch sử friend info → đọc cột action của từng bản ghi",
       "6 loại info không có action × 4 luồng ghi",
       "- Cột action hiển thị **「設定なし」** đúng ở mọi bản ghi\n"
       "- Không bị đổi nhầm thành「プレビュー」sau khi fix #38312",
       note="Nguồn: Task nhỏ r293 (TC-NEW-03 do AI đề xuất). Ghi 'regression' theo quy chuẩn Loại case."),

    tc("Admin — đặt chỗ hộ & sửa booking", "REG-SHARED-001", "Normal",
       "Regression — lịch sử action preview ở các luồng gán friend info KHÁC (lesson/salon/item/form/multi-action)",
       "- ⚠ CHỈ chạy sau khi Dev xác nhận luồng đó cũng gán friend info select-có-action\n"
       "- Mỗi luồng có form / multi-action liên kết friend info select value có action",
       "1. Thực hiện luồng tương ứng (đặt lịch Lesson / Salon, mua Item, trả lời Form, hoặc chạy multi-action) "
       "gán value select có action\n2. Mở màn lịch sử friend info → đọc cột action\n3. Click vào cột action",
       "5 luồng: Lesson · Salon · Item · Form · multi-action",
       "- Mỗi luồng Dev xác nhận có gán: cột action hiện **「プレビュー」**, click ra được preview\n"
       "- Luồng nào Dev xác nhận KHÔNG gán → ghi rõ là ngoài phạm vi, KHÔNG tạo TC",
       note="Nguồn: Task nhỏ r292 (TC-NEW-02 do AI đề xuất, có ghi rõ điều kiện「CHỈ tạo sau khi Dev xác nhận」). "
            "⚠ Ghi nhớ dự án: bug nhiều layer — nếu layer downstream không bị chạm code thì không đề xuất TC."),

    # ══════════════════ 27. Admin — danh sách người tham gia ══════════════════
    tc("Admin — danh sách người tham gia", "FUNC-001", "Normal",
       "Màn hiển thị dạng LỊCH — hiện đúng các ngày là 開催日 và số booking theo trạng thái",
       ADM + "\n- Event E có 3 開催日 trong tháng 9/2026\n"
       "- Ngày 2026-09-01 có: 3 booking đã duyệt, 2 booking chờ duyệt, 1 booking đã hủy",
       "1. Mở màn 参加者リスト → chọn chế độ hiển thị theo lịch\n"
       "2. Quan sát các ô ngày trong tháng 9\n3. Đọc số booking hiển thị ở ô ngày 2026-09-01",
       "3 開催日; ngày 01: 3 duyệt / 2 chờ / 1 hủy",
       "- Chỉ 3 ngày là 開催日 được đánh dấu, các ngày khác trống\n"
       "- Ô ngày 2026-09-01 hiện đúng số booking theo từng trạng thái: **3 đã duyệt / 2 chờ duyệt / 1 hủy**",
       note="Nguồn: Event booking 1.0 r318-r321 (TC gốc chỉ có tiêu đề) → expected do AI viết với số liệu cụ thể "
            "theo DATA-COUNT-001, cần Leader xác nhận cách hiển thị thực tế."),

    tc("Admin — danh sách người tham gia", "FUNC-001", "Normal",
       "Click vào 1 ngày trên lịch → hiện danh sách booking của ngày đó đủ 4 thông tin",
       ADM + "\n- Ngày 2026-09-01 có 2 slot, mỗi slot 1 コース, tổng 5 booking",
       "1. Ở chế độ lịch, click vào ô ngày 2026-09-01\n"
       "2. Quan sát danh sách hiện ra\n3. Đối chiếu từng dòng với dữ liệu booking",
       "5 booking ở 2 slot",
       "- Danh sách hiện đủ 5 booking\n"
       "- Mỗi dòng hiện: **ngày tổ chức · giờ slot · コース (nếu có) · số người đã đặt (đã duyệt) / 定員**",
       note="Nguồn: Event booking 1.0 r322-r325 (TC gốc chỉ có tiêu đề) → expected do AI viết."),

    tc("Admin — danh sách người tham gia", "LIST-001", "Normal",
       "Tìm kiếm theo LINE name / system name ở màn danh sách người tham gia",
       ADM + "\n- Có 10 booking của 10 friend khác nhau; 1 friend có LINE name「山田」và system name「YAMADA」",
       "1. Mở màn danh sách người tham gia\n2. Gõ「山田」vào ô tìm kiếm → đếm kết quả\n"
       "3. Xóa, gõ「YAMADA」→ đếm kết quả\n4. Gõ chuỗi không tồn tại → quan sát",
       "「山田」·「YAMADA」· chuỗi không tồn tại",
       "- Tìm bằng LINE name và bằng system name **đều ra đúng booking của friend đó**\n"
       "- Chuỗi không tồn tại: hiện danh sách rỗng có thông báo, không lỗi",
       note="Nguồn: Event booking 1.0 r326 và r336 (TC gốc chỉ có tiêu đề) → expected do AI viết theo LIST-001."),

    tc("Admin — danh sách người tham gia", "LIST-001", "Normal",
       "Lọc theo trạng thái booking → chỉ hiện đúng booking của trạng thái đã chọn",
       ADM + "\n- Có booking ở đủ các trạng thái: 承認 / 否認 / 承認待ち / キャンセル / 予約済み / "
       "変更リクエスト / キャンセルリクエスト (mỗi loại ≥1)",
       "1. Chọn lần lượt từng trạng thái ở bộ lọc\n2. Với mỗi lần, đếm số dòng và kiểm tra badge trạng thái",
       "7 trạng thái",
       "- Mỗi lần lọc: chỉ hiện booking đúng trạng thái đã chọn\n"
       "- Tổng số booking qua 7 lần lọc = tổng số booking của event",
       note="Nguồn: Event booking 1.0 r327 và r337 (TC gốc chỉ có tiêu đề) → expected do AI viết. "
            "Spec BR-04 (7 trạng thái)."),

    tc("Admin — danh sách người tham gia", "LIST-001", "Normal",
       "Lọc slot đã diễn ra / chưa diễn ra ở cả 2 chế độ hiển thị (lịch và danh sách)",
       ADM + "\n- Event có slot ngày quá khứ và slot ngày tương lai, mỗi loại có booking",
       "1. Ở chế độ lịch: chọn lọc「chưa triển khai」→ đếm; chọn「đã triển khai」→ đếm\n"
       "2. Chuyển sang chế độ danh sách: lặp lại 2 lần lọc",
       "1 slot quá khứ, 2 slot tương lai",
       "- Cả 2 chế độ: lọc「chưa triển khai」ra đúng 2 slot tương lai; lọc「đã triển khai」ra 1 slot quá khứ\n"
       "- Kết quả 2 chế độ **nhất quán với nhau**",
       note="Nguồn: Event booking 1.0 r329 và r331 (TC gốc chỉ có tiêu đề) → expected do AI viết."),

    tc("Admin — danh sách người tham gia", "LIST-001", "Normal",
       "Sắp xếp theo ngày tổ chức tăng dần / giảm dần ở chế độ danh sách",
       ADM + "\n- Có booking ở 3 開催日 khác nhau: 2026-09-01, 2026-09-08, 2026-09-15",
       "1. Ở chế độ danh sách chọn sắp xếp ngày **tăng dần** → đọc thứ tự ngày\n"
       "2. Chọn **giảm dần** → đọc thứ tự ngày\n3. Sang trang 2 (nếu có) kiểm tra thứ tự tiếp nối",
       "3 ngày tổ chức",
       "- Tăng dần: 09-01 → 09-08 → 09-15\n- Giảm dần: 09-15 → 09-08 → 09-01\n"
       "- Thứ tự **đúng liên tục qua các trang**, không bị reset ở trang 2",
       note="Nguồn: Event booking 1.0 r338-r339 (TC gốc chỉ có tiêu đề) → expected do AI viết theo LIST-001."),

    tc("Admin — danh sách người tham gia", "LIST-001", "Normal",
       "Phân trang danh sách người tham gia — không lặp / không sót bản ghi",
       ADM + "\n- Event E có đúng 45 booking",
       "1. Mở màn danh sách người tham gia\n2. Ghi lại id booking ở trang 1\n"
       "3. Sang trang 2, 3 → ghi lại id\n4. Đối chiếu tổng số id duy nhất",
       "45 booking",
       "- Tổng id duy nhất qua các trang = **45**\n- **Không id nào xuất hiện ở 2 trang**\n"
       "- Áp dụng cho cả chế độ lịch và chế độ danh sách",
       note="Nguồn: Event booking 1.0 r330 và r341 (TC gốc chỉ có tiêu đề) → expected do AI viết theo LIST-001."),

    tc("Admin — danh sách người tham gia", "FUNC-001", "Normal",
       "Màn detail booking hiện đủ thông tin đặt chỗ của user",
       ADM + "\n- Booking B của U1: 2026-09-01 10:00〜12:00, コース P1 5000円, 2 chỗ, 3 đáp án form, "
       "đã thanh toán",
       "1. Mở màn detail booking B\n2. Đối chiếu từng thông tin với dữ liệu đặt chỗ",
       "1 booking đầy đủ thông tin",
       "- Hiện đủ: friend name · 参加日時 (ngày + giờ) · コース · 参加人数 · 決済金額 · badge trạng thái · "
       "3 cặp câu hỏi-đáp án form\n- 決済金額 hiển thị **readonly**, đúng 10.000円 (5000 × 2)",
       note="Nguồn: Event booking 1.0 r342 (TC gốc chỉ có tiêu đề) + spec Field Matrix #47-#53."),

    tc("Admin — danh sách người tham gia", "UI-003", "Normal",
       "Empty state — event chưa có booking nào",
       ADM + "\n- Event mới, chưa có booking nào",
       "1. Mở màn 参加者リスト ở chế độ lịch → quan sát\n2. Chuyển sang chế độ danh sách → quan sát\n"
       "3. Mở màn 予約枠一覧 → quan sát",
       "0 booking",
       "- Cả 3 màn: hiện thông báo không có dữ liệu, KHÔNG hiện dòng rác\n"
       "- Các cột số đếm hiện 0, không hiện NULL / undefined",
       note="TC bổ sung theo UI-003 — corpus KHÔNG có TC empty state cho các màn quản lý booking."),

    # ══════════════════ 28. Export CSV ══════════════════
    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV ở màn danh sách người tham gia — cả chế độ lịch và chế độ danh sách",
       ADM + "\n- Event E có 5 booking với đầy đủ thông tin",
       "1. Ở chế độ **lịch**: bấm nút export → mở file CSV\n"
       "2. Ở chế độ **danh sách**: bấm nút export → mở file CSV\n"
       "3. Đối chiếu số dòng dữ liệu với số booking\n4. Đối chiếu nội dung từng cột",
       "5 booking",
       "- Cả 2 chế độ: tải được file CSV\n- File có đúng **5** dòng dữ liệu (không kể header)\n"
       "- Các cột cũ **đều có mặt** trong file CSV mới",
       note="Nguồn: Event booking 3.0 r3-r10 (07/2023). ⚠ MT-26 — spec G-06 nói route export tồn tại "
            "(EP-17/EP-51/EP-52) nhưng **KHÔNG thấy nút trong Blade** → cần xác nhận nút có thật hay không. ⚠ RULE-01: quan điểm `OUT-EXPORT-001` trong bộ này KHÔNG có loại case **Abnormal** — lý do: corpus và spec không mô tả nhánh bất thường nào cho quan điểm này."),

    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV có thêm các cột friend info — đúng tiêu đề cột và đúng dữ liệu",
       ADM + "\n- Event E có 3 item form liên kết friend info: name, email, 1 info text tùy chỉnh\n"
       "- 5 booking đã điền đủ 3 item",
       "1. Bấm export CSV ở màn danh sách người tham gia\n2. Mở file, đọc dòng tiêu đề\n"
       "3. Đối chiếu giá trị từng cột friend info với dữ liệu booking",
       "3 item friend info × 5 booking",
       "- Dòng tiêu đề có đủ **3 cột friend info** với tên đúng như setting\n"
       "- Giá trị từng ô khớp với đáp án đã nhập của từng booking",
       note="Nguồn: Event booking 3.0 r5-r6, r9-r10 (mục đích chính của đợt improve 3.0)."),

    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV ở màn 予約枠一覧 → detail booking của slot",
       ADM + "\n- Slot S1 có 4 booking",
       "1. Mở màn 予約枠一覧 → mở detail booking của slot S1\n2. Bấm export CSV\n"
       "3. Mở file, đối chiếu số dòng và nội dung cột (gồm cột friend info mới)",
       "4 booking ở slot S1",
       "- Tải được file CSV\n- Đúng **4** dòng dữ liệu (chỉ booking của slot S1, không lẫn slot khác)\n"
       "- Có đủ các cột cũ + các cột friend info",
       note="Nguồn: Event booking 3.0 r11-r14."),

    tc("Export CSV", "STATE-DEP-001", "Normal",
       "Thay đổi setting friend info rồi export lại → cột CSV theo setting MỚI NHẤT",
       ADM + "\n- Event E đang có 3 item form liên kết friend info, đã có booking",
       "1. Export CSV lần 1 → ghi lại danh sách cột\n"
       "2. **Thêm** 1 item friend info mới → export lại → đối chiếu cột\n"
       "3. **Sửa tên** 1 item → export lại → đối chiếu\n"
       "4. **Xóa** 1 item → export lại → đối chiếu",
       "Thêm / sửa / xóa item friend info",
       "- Sau mỗi thay đổi, file CSV mới có các cột theo **setting mới nhất**\n"
       "- Thêm item: có cột mới\n- Sửa tên: tiêu đề cột đổi theo\n- Xóa item: cột biến mất\n"
       "- Dữ liệu các cột còn lại không bị lệch cột",
       note="Nguồn: Event booking 3.0 r15-r17「file csv mới các cột sẽ theo setting mới nhất」."),

    tc("Export CSV", "DATA-TEXT-001", "Normal",
       "Export CSV với dữ liệu chứa ký tự đặc biệt / emoji / xuống dòng → mở đúng, không lệch cột",
       ADM + "\n- Có booking với đáp án form chứa: dấu phẩy, dấu nháy kép, emoji, ký tự Nhật đặc biệt, "
       "và 1 đáp án 長文回答 có xuống dòng",
       "1. Export CSV\n2. Mở file bằng Excel và bằng trình soạn thảo text\n"
       "3. Đối chiếu từng ô với dữ liệu gốc",
       "「テスト,データ」·「\"引用\"」·「体験会🎁」· ・ー【】～ · đáp án có 2 dòng",
       "- Dữ liệu hiển thị **đúng nguyên văn**, không mojibake, emoji không mất\n"
       "- Dấu phẩy và dấu nháy kép **không làm lệch cột**\n"
       "- Đáp án có xuống dòng nằm gọn trong 1 ô, không tách thành dòng mới",
       note="TC bổ sung theo OUT-EXPORT-001 + DATA-TEXT-001. Corpus KHÔNG test ký tự đặc biệt khi export "
            "ở event booking (chỉ có ở feature item) → lấp GAP."),

    tc("Export CSV", "OUT-EXPORT-001", "Normal",
       "Export CSV sau khi lọc / tìm kiếm → chỉ export đúng phạm vi đang lọc",
       ADM + "\n- Event E có 20 booking, trong đó 5 booking ở trạng thái 承認待ち",
       "1. Lọc trạng thái = 承認待ち → đếm số dòng trên màn\n2. Bấm export CSV\n"
       "3. Đếm số dòng dữ liệu trong file\n4. Bỏ lọc → export lại → đếm số dòng",
       "20 booking, lọc còn 5",
       "- File export sau khi lọc có đúng **5** dòng (khớp màn hình)\n"
       "- File export khi bỏ lọc có **20** dòng\n"
       "- Nếu export ra đủ 20 dòng khi đang lọc 5 → **RAISE BUG** (BULK-001)",
       note="TC bổ sung theo BULK-001/OUT-EXPORT-001 — corpus KHÔNG kiểm phạm vi export sau lọc ở event booking."),

    # ══════════════════ 29. Đếm 定員 & use_people ══════════════════
    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Normal",
       "Booking mới KHÔNG có コース — cộng use_people theo số lượng đặt khi được duyệt ngay",
       ADM + "\n- Slot S1 KHÔNG có コース, 全承認, `use_people` = 0",
       "1. U1 đặt 1 chỗ số lượng = 1 → đọc `use_people`\n"
       "2. U2 đặt 1 chỗ số lượng = 3 → đọc `use_people`\n3. Đối chiếu phép tính tay",
       "quantity 1 rồi quantity 3",
       "- Sau lần 1: `use_people` = **1**\n- Sau lần 2: `use_people` = **4** (1 + 3)\n"
       "- Cộng theo `quantity`, không phải theo số booking",
       note="Nguồn: Task nhỏ r68「bảng b_slot update use_people + n (n = số lượng user book)」."),

    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Normal",
       "Booking mới CÓ コース — cộng cả use_people của slot và remain_limit của コース",
       ADM + "\n- Slot S2 定員 = 10 có コース P1 定員 = 5, 全承認\n"
       "- `use_people` = 0, `remain_limit` = 0",
       "1. U1 đặt 2 chỗ ở コース P1\n2. Đọc `b_slot.use_people` và `b_plan_slot.remain_limit`",
       "quantity = 2",
       "- `use_people` = **2** và `remain_limit` = **2** (cả 2 bộ đếm đều cộng)",
       note="Nguồn: Task nhỏ r70."),

    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Normal",
       "Booking CHỜ DUYỆT → KHÔNG cộng bộ đếm; duyệt xong mới cộng",
       ADM + "\n- Slot S3 リクエスト制 có コース P2, `use_people` = 0, `remain_limit` = 0",
       "1. U1 đặt 2 chỗ ở コース P2 (booking `status = 3`)\n2. Đọc 2 bộ đếm\n"
       "3. Admin duyệt booking\n4. Đọc lại 2 bộ đếm\n5. Với booking khác, admin **từ chối** → đọc bộ đếm",
       "quantity = 2, リクエスト制",
       "- Ngay sau khi đặt: `use_people` = **0**, `remain_limit` = **0**\n"
       "- Sau khi duyệt: `use_people` = **2**, `remain_limit` = **2**\n"
       "- Trường hợp từ chối: 2 bộ đếm **giữ nguyên 0**",
       note="Nguồn: Task nhỏ r69, r71 + Event booking 2.0 r30-r32."),

    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Normal",
       "Hủy booking → trừ bộ đếm khi đã duyệt; không trừ khi đang chờ duyệt",
       ADM + "\n- Slot S2 có 2 booking: B1 `status = 5` (đã cộng đếm), B2 `status = 3` (chưa cộng)\n"
       "- `use_people` = 1, `remain_limit` = 1",
       "1. Hủy B1 → đọc 2 bộ đếm\n2. Hủy B2 → đọc 2 bộ đếm",
       "B1 đã duyệt, B2 chờ duyệt",
       "- Sau hủy B1: `use_people` = **0**, `remain_limit` = **0** (trừ đi)\n"
       "- Sau hủy B2: 2 bộ đếm **không đổi**, vẫn = 0",
       note="Nguồn: Task nhỏ r82-r83 + Event booking 2.0 r47-r48."),

    tc("Đếm 定員 & use_people", "PAY-STATE-001", "Normal",
       "Event KHÔNG bill tiền — cộng bộ đếm theo chế độ duyệt",
       ADM + "\n- Event KHÔNG bật 決済",
       "1. Slot リクエスト制: U1 đặt chỗ → đọc bộ đếm\n2. Slot 全承認: U1 đặt chỗ → đọc bộ đếm",
       "2 chế độ duyệt, không bill tiền",
       "- リクエスト制: booking success, tạo booking mới, **không cập nhật** bộ đếm\n"
       "- 全承認: booking success, tạo booking mới, **cập nhật bộ đếm đúng**",
       note="Nguồn: Task nhỏ r85-r86."),

    tc("Đếm 定員 & use_people", "PAY-STATE-001", "Abnormal",
       "Event CÓ bill tiền — bill fail thì XÓA booking và hoàn lại bộ đếm (cả UnivaPay và Stripe)",
       ADM + "\n- Event bật 決済, slot 全承認, コース có 料金",
       "1. Với UnivaPay: U1 đặt chỗ, bill thành công → đọc bộ đếm + kiểm tra thông tin thanh toán\n"
       "2. Với UnivaPay: U1 đặt chỗ, bill thất bại → đọc bộ đếm + kiểm tra booking còn không\n"
       "3. Lặp lại 2 bước trên với Stripe",
       "2 cổng × (bill success / bill fail)",
       "- Bill success (cả 2 cổng): tạo booking mới, thông tin thanh toán cập nhật đúng, "
       "**bộ đếm cập nhật đúng**\n"
       "- Bill fail (cả 2 cổng): **xóa booking vừa tạo** khỏi `b_user_booking`, "
       "**hoàn lại bộ đếm về giá trị trước khi đặt**",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r87-r92. RULE-08 — bill tiền BẮT BUỘC test PRODUCTION."),

    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Normal",
       "Đặt chỗ khi slot リクエスト制 nhưng CÓ bill tiền → không cộng bộ đếm cho tới khi duyệt",
       ADM + "\n- Event bật 決済, slot リクエスト制, コース có 料金",
       "1. U1 đặt chỗ, nhập thẻ → đọc bộ đếm ngay sau khi đặt\n2. Admin duyệt → đọc lại bộ đếm",
       "リクエスト制 + có bill tiền",
       "- Ngay sau khi đặt: bộ đếm **không đổi**\n"
       "- Sau khi admin duyệt và thu tiền thành công: `use_people` +n, `remain_limit` +n",
       env="PRODUCTION",
       note="Nguồn: Task nhỏ r87, r90 + Improve bill tiền univapay r37."),

    tc("Đếm 定員 & use_people", "DATA-COUNT-001", "Boundary",
       "Duyệt booking VƯỢT 定員 → hệ thống hỏi xác nhận thay vì chặn cứng",
       ADM + "\n- Slot S1 定員 = 2, `use_people` = 2 (đã đầy)\n"
       "- Còn 1 booking `status = 3` chờ duyệt (quantity = 1)",
       "1. Admin bấm duyệt booking chờ duyệt\n2. Quan sát thông báo hiện ra\n"
       "3. Bấm đồng ý → query `status` và `use_people`\n"
       "4. Với booking khác, bấm duyệt rồi bấm hủy ở popup → query lại",
       "定員 2, đã dùng 2, duyệt thêm 1",
       "- Hiện confirm **「予約枠を超えています。承認しますか？」**, KHÔNG chặn cứng\n"
       "- Bấm đồng ý: duyệt thành công, `use_people` = **3** (vượt 定員)\n"
       "- Bấm hủy ở popup: booking giữ nguyên `status = 3`, `use_people` vẫn = 2",
       note="Nguồn: spec BR-09 (`:3237-3255` — trả `admin_confirm: 1`, gọi lại với `approveAny = true` sẽ bỏ qua). "
            "Corpus **KHÔNG có TC nào** cho popup này → GAP quan trọng, xem MT-27."),

    tc("Đếm 定員 & use_people", "DATA-DB-001", "Normal",
       "Bộ đếm KHÔNG bị drift sau chuỗi thao tác hỗn hợp",
       ADM + "\n- Slot S 定員 = 20 có コース P 定員 = 20, `use_people` = 0, `remain_limit` = 0",
       "1. Thực hiện tuần tự: 3 user đặt (mỗi người 2 chỗ) → admin đặt hộ 1 booking 3 chỗ → "
       "1 user đổi số lượng từ 2 lên 4 → 1 user hủy (2 chỗ) → admin hủy 1 booking (3 chỗ)\n"
       "2. Tính tay giá trị mong đợi\n3. Query `use_people` và `remain_limit`\n"
       "4. Query tổng `quantity` của các booking active (`status ∈ {1,5}` hoặc 6 với `update_to IS NULL` hoặc 7)",
       "Chuỗi: +2 +2 +2 +3 (admin) → sửa 2→4 (+2) → hủy 2 (−2) → admin hủy 3 (−3)\n"
       "Tính tay: 2+2+2+3+2−2−3 = **6**",
       "- `use_people` = **6** và `remain_limit` = **6**\n"
       "- Giá trị bộ đếm = tổng `quantity` của booking active (query đối chiếu khớp nhau)",
       note="TC bổ sung theo spec TD-17 (`saveAdminBooking` dùng increment, `saveActionBooking` recompute → "
            "nguy cơ **drift**) + TD-01 (không transaction). Corpus test từng thao tác riêng lẻ nhưng KHÔNG có "
            "TC chuỗi hỗn hợp → GAP, xem MT-28."),
]
