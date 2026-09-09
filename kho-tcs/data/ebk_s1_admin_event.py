# -*- coding: utf-8 -*-
"""FA-021 イベント予約 (Event booking) — Nhóm 1-6: quản trị event / ngày / slot / plan phía admin.

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Event booking 1.0」(03/2023 → 09/2025) — bộ case gốc toàn bộ màn admin
  - tab「Event booking 2.0」(05/2023 → 10/2025) — setting theo duration + max plan
  - tab「Task nhỏ + fix bug KH」(09/2024 → 07/2026, tab MASTER còn sống) — xoá cascade, bug #26616
  - tab「Sheet4」(Bug #24441, 10/2023) — công thức tính 定員 của 1 ngày
Bổ sung: TCsLine_Improve chung / tab「Test bug folder all màn」r174 (folder trùng tên),
         tab「Improve nhỏ」r454-456 (ảnh header), tab「Improve tiny form」r9 (font selectbox).
"""
from _common import tc

ADM = "- Đăng nhập admin (主管理者) bot A, bot đã đăng ký `liff_app_id_booking`\n- Mở /basic/booking-event-day/list-event"
EV = ADM + "\n- Đã có 1 event「テストイベント」với 1 開催日 + 1 予約枠"

S1 = [
    # ══════════════════ 1. Màn list event (SCR-EBD-01) ══════════════════
    tc("Màn list event", "FUNC-001", "Normal",
       "Mở màn danh sách sự kiện → hiển thị đủ 2 cột panel + 9 cột bảng",
       EV,
       "1. Mở /basic/booking-event-day/list-event\n"
       "2. Quan sát panel trái「フォルダ」và bảng bên phải\n"
       "3. Đối chiếu từng cột với event đã tạo",
       "1 event「テストイベント」, folder 未分類",
       "- Panel trái hiện danh sách folder, panel phải hiện bảng\n"
       "- Bảng có đủ các cột: checkbox |「作成日/管理名」|「イベントページ」|「参加予定」|「定員」|"
       "「承認待ち」|「参加済み」|「参加者リスト」|「予約枠一覧」| ⋯\n"
       "- Dòng event hiện đúng ngày tạo + tên quản lý đã nhập",
       note="Nguồn: Event booking 1.0 r8-r17. Spec feature-spec.md §2.1 (SCR-EBD-01)."),

    tc("Màn list event", "UI-003", "Abnormal",
       "Bot CHƯA đăng ký LIFF ID → cảnh báo đỏ + nút 新規作成 chặn bằng alert",
       "- Đăng nhập admin bot B\n- Bot B có `bots.liff_app_id_booking` = rỗng VÀ `bots.liff_app_id` = rỗng",
       "1. Mở /basic/booking-event-day/list-event\n2. Quan sát vùng trên bảng\n3. Bấm nút「新規作成」",
       "Bot B chưa liên kết LIFF",
       "- Hiện cảnh báo đỏ「LIFF IDを登録してください (登録方法)」\n"
       "- Bấm「新規作成」→ alert「LIFF IDを登録してください」, KHÔNG mở màn tạo event\n"
       "- Không tạo được bản ghi `b_event_detail` nào",
       note="Nguồn: spec feature-spec.md §1.4 (điều kiện tiên quyết LIFF). Corpus KHÔNG có TC này → "
            "TC bổ sung để lấp GAP; cần Leader xác nhận nội dung alert thật. ⚠ RULE-01: quan điểm `UI-003` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 参加予定 = tổng booking đã duyệt của các slot CHƯA diễn ra",
       ADM + "\n- Event E có 2 開催日: ngày quá khứ (đã qua) và ngày tương lai\n"
       "- Ngày tương lai: 3 booking status=1 (承認), 1 booking status=3 (承認待ち)\n"
       "- Ngày quá khứ: 2 booking status=1",
       "1. Mở màn list event\n2. Đọc số ở cột「参加予定」của event E\n"
       "3. Đối chiếu với phép tính tay",
       "Ngày tương lai: 3 booking approve (quantity mỗi booking = 1) → 参加予定 = 3\n"
       "Booking status=3 KHÔNG được tính; 2 booking của ngày quá khứ KHÔNG được tính",
       "- Cột「参加予定」hiện đúng **3**\n- Không cộng nhầm booking 承認待ち và booking của slot đã qua",
       note="Nguồn: Event booking 1.0 r12. Spec BR-05 + Field Matrix #5. ⚠ RULE-01: quan điểm `DATA-COUNT-001` trong bộ này KHÔNG có loại case **Abnormal** — lý do: corpus và spec không mô tả nhánh bất thường nào cho quan điểm này."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 参加予定 VẪN đếm booking đang ở trạng thái request change / request cancel",
       ADM + "\n- Event E, slot tương lai có: 1 booking status=1, 1 booking status=6 (変更リクエスト, "
       "`update_to IS NULL`), 1 booking status=7 (キャンセルリクエスト)",
       "1. Đọc cột「参加予定」\n2. Admin duyệt request cancel\n3. Reload màn list → đọc lại cột「参加予定」",
       "Trước khi duyệt: 3 booking active → 参加予定 = 3\nSau khi duyệt cancel: còn 2",
       "- Trước duyệt: cột「参加予定」= **3** (cả booking 6 và 7 đều được tính)\n"
       "- Sau khi duyệt cancel: cột「参加予定」giảm còn **2**",
       note="Nguồn: Event booking 1.0 r12「Các slot có request change hoặc cancel đang đợi approve vẫn được "
            "count vào đây => sau khi approve change hoặc approve cancel thì trừ đi」. Spec BR-05."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 定員 = tổng 定員 của all slot — slot KHÔNG có plan lấy 定員 slot",
       ADM + "\n- Event E có 1 ngày, 2 slot đều KHÔNG có コース: slot1 定員=10, slot2 定員=5",
       "1. Mở màn list event\n2. Đọc cột「定員」của event E",
       "slot1 = 10, slot2 = 5 → tổng = 15",
       "- Cột「定員」hiện **15**",
       note="Nguồn: Event booking 1.0 r13 + Sheet4 r3-r4 (Bug #24441). Spec Field Matrix #7."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 定員 — slot CÓ plan thì lấy tổng 定員 của các plan, KHÔNG lấy 定員 slot",
       ADM + "\n- Event E có 1 slot 定員=10, bên trong có 3 コース: plan1 定員=2, plan2 定員=3, plan3 定員=4\n"
       "- Cả 3 plan đều KHÔNG tick「予約枠の定員の残数に合わせる」(`using_max_slot = 0`)",
       "1. Mở màn list event\n2. Đọc cột「定員」của event E\n3. Đối chiếu phép tính tay",
       "2 + 3 + 4 = 9 (KHÔNG phải 10 của slot)",
       "- Cột「定員」hiện **9**",
       note="Nguồn: Event booking 1.0 r13 + Sheet4 r6. Spec Field Matrix #7 + BR-07."),

    tc("Màn list event", "DATA-COUNT-001", "Boundary",
       "Cột 定員 — slot 定員 = 無制限 và có ≥1 plan dùng chung 定員 slot → cả event = 無制限 (-)",
       ADM + "\n- Event E có 1 slot để trống 定員 (`number_people = NULL`)\n"
       "- Slot có 2 plan: plan1 tick「予約枠の定員の残数に合わせる」, plan2 定員=3",
       "1. Mở màn list event\n2. Đọc cột「定員」",
       "slot 定員 = NULL (無制限); plan1 `using_max_slot = 1`; plan2 limit = 3",
       "- Cột「定員」hiện dấu **-** (không giới hạn), KHÔNG hiện số 3",
       note="Nguồn: Sheet4 r5 (Bug #24441). Spec BR-07 (`number_people = NULL` → vô hạn). ⚠ Xem MT-05 — "
            "spec Field Matrix #7 chỉ ghi SUM đơn giản, không mô tả nhánh lai này."),

    tc("Màn list event", "DATA-COUNT-001", "Boundary",
       "Cột 定員 — slot CÓ set 定員 + có ≥1 plan dùng chung 定員 slot → 定員 slot + tổng 定員 các plan riêng",
       ADM + "\n- Event E có 1 slot 定員=5\n"
       "- Slot có 3 plan: plan1 tick 予約枠の定員の残数に合わせる, plan2 定員=2, plan3 定員=4",
       "1. Mở màn list event\n2. Đọc cột「定員」\n3. Đối chiếu phép tính tay",
       "5 (定員 slot) + 2 + 4 (2 plan không dùng chung) = 11",
       "- Cột「定員」hiện **11**",
       note="Nguồn: Sheet4 r7 (Bug #24441, 10/2023). ⚠ MT-05 — công thức lai này KHÔNG có trong spec; "
            "TC > 2 năm, CẦN VERIFY LẠI trước khi dùng làm chuẩn."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 承認待ち chỉ đếm status=3, KHÔNG đếm request change / request cancel",
       ADM + "\n- Event E có: 2 booking status=3 (承認待ち), 1 booking status=6, 1 booking status=7",
       "1. Mở màn list event\n2. Đọc cột「承認待ち」",
       "2 booking status=3 → 承認待ち = 2",
       "- Cột「承認待ち」hiện **2** (không cộng status 6 và 7)",
       note="Nguồn: Event booking 1.0 r14「không tính request change và request cancel」. ⚠ MT-35 — "
            "spec BR-06 nói countRequestSlot = status ∈ {3,6,7} → NGƯỢC với TC. Cần Leader chốt."),

    tc("Màn list event", "DATA-COUNT-001", "Normal",
       "Cột 参加済み = số đã duyệt của các slot ĐÃ hết hạn (đã qua ngày sự kiện)",
       ADM + "\n- Event E có 1 ngày quá khứ (2 booking approve) + 1 ngày tương lai (3 booking approve)",
       "1. Mở màn list event\n2. Đọc cột「参加済み」",
       "Ngày quá khứ: 2 booking approve",
       "- Cột「参加済み」hiện **2**\n- Cột「参加予定」hiện **3** (2 cột không lẫn nhau)",
       note="Nguồn: Event booking 1.0 r15."),

    tc("Màn list event", "LIFF-ENTRY-001", "Normal",
       "Cột イベントページ — icon copy sao chép đúng URL LIFF của event",
       EV,
       "1. Ở dòng event, bấm icon copy ở cột「イベントページ」\n"
       "2. Dán nội dung clipboard vào ô text bất kỳ\n"
       "3. Mở URL vừa dán bằng LINE app",
       "URL dạng https://liff.line.me/{liff_app_id_booking}?booking_event_id={id}",
       "- Clipboard chứa đúng URL LIFF của event đang thao tác (đúng `liff_app_id_booking` của bot A "
       "và đúng id event)\n- Mở URL trong LINE → vào đúng trang đặt chỗ của event đó",
       note="Nguồn: Event booking 1.0 r10. Spec Field Matrix #4. ⚠ RULE-01: quan điểm `LIFF-ENTRY-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Màn list event", "OUT-PREVIEW-001", "Normal",
       "Cột イベントページ — icon 👁 preview mở trang xem trước bằng hash id",
       EV,
       "1. Bấm icon 👁 ở cột「イベントページ」\n2. Quan sát URL trên thanh địa chỉ và nội dung trang",
       "Event id = 1118",
       "- Mở tab mới tới trang preview, URL chứa **hash id** (Hashids), KHÔNG lộ id số nguyên 1118\n"
       "- Nội dung trang khớp với setting đang lưu của event",
       note="Nguồn: Event booking 1.0 r11 + r152. Spec BR-25."),

    tc("Màn list event", "LIST-001", "Normal",
       "Sort danh sách event → thứ tự đổi đúng và giữ nguyên sau reload",
       ADM + "\n- Folder 未分類 có 5 event",
       "1. Bấm nút sort, kéo event thứ 5 lên vị trí 1\n2. Lưu\n3. Reload trang (F5)\n"
       "4. Mở lại màn list từ menu",
       "5 event: E1..E5, kéo E5 → vị trí 1",
       "- Ngay sau khi lưu: thứ tự E5, E1, E2, E3, E4\n- Sau reload: thứ tự KHÔNG đổi\n"
       "- Mở lại từ menu: thứ tự vẫn đúng",
       note="Nguồn: Event booking 1.0 r18. TC gốc chỉ có tiêu đề, không có kết quả mong đợi → "
            "kết quả mong đợi do AI viết, cần Leader xác nhận. ⚠ RULE-01: quan điểm `LIST-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Màn list event", "LIST-001", "Normal",
       "Phân trang danh sách event — 20 event/trang",
       ADM + "\n- Folder 未分類 có đúng 25 event",
       "1. Mở màn list event\n2. Đếm số dòng trang 1\n3. Sang trang 2\n4. Đếm số dòng trang 2",
       "25 event",
       "- Trang 1 hiện đúng **20** event\n- Trang 2 hiện **5** event còn lại\n- Không dòng nào lặp giữa 2 trang",
       note="Nguồn: spec §2.1 EP-20 (paginate 20). Corpus KHÔNG có TC phân trang màn list event → "
            "TC bổ sung lấp GAP."),

    tc("Màn list event", "UI-003", "Normal",
       "Empty state — bot chưa có event nào",
       ADM + "\n- Bot A chưa tạo event nào (`b_event_detail` với `type_event_new = 1` = 0 bản ghi)",
       "1. Mở màn list event\n2. Quan sát vùng bảng",
       "0 event",
       "- Bảng hiện thông báo「データがありません。」\n- 4 cột số (参加予定/定員/承認待ち/参加済み) không hiện dòng rác\n"
       "- Nút「新規作成」vẫn bấm được (nếu đã có LIFF ID)",
       note="Nguồn: spec §10.1 (tài khoản test hiển thị 「データがありません。」). Corpus KHÔNG có TC empty state."),

    tc("Màn list event", "UI-001", "Normal",
       "Giao diện màn list ở độ phân giải 1366 x 768 không vỡ layout",
       EV + "\n- Trình duyệt đặt viewport 1366 x 768",
       "1. Mở màn list event ở 1366 x 768\n2. Quan sát panel folder + bảng\n"
       "3. Cuộn ngang / dọc kiểm tra tràn",
       "Viewport 1366 x 768",
       "- Panel folder (20%) và bảng (78%) hiển thị đủ, không chồng lấn\n"
       "- 9 cột bảng đọc được, không bị cắt chữ; không xuất hiện thanh cuộn ngang toàn trang",
       note="Nguồn: Event booking 1.0 r354. TC gốc chỉ có tiêu đề → expected do AI viết, cần Leader xác nhận."),

    # ══════════════════ 2. Folder event ══════════════════
    tc("Folder event", "FUNC-001", "Normal",
       "Tạo folder mới → hiện ở panel trái, ghi `category` với kind = 21",
       ADM,
       "1. Ở panel trái bấm thêm folder mới\n2. Nhập tên「イベントフォルダA」→ Lưu\n3. Reload trang",
       "Tên folder:「イベントフォルダA」",
       "- Folder「イベントフォルダA」xuất hiện ở panel trái\n"
       "- Sau reload folder vẫn còn\n- Folder này KHÔNG xuất hiện ở panel folder của tính năng khác "
       "(tag / form / richmenu)",
       note="Nguồn: Event booking 1.0 r4. Spec BR-24 (`category.kind = 21`)."),

    tc("Folder event", "FUNC-002", "Abnormal",
       "Tạo folder để trống tên → báo lỗi, không tạo bản ghi",
       ADM,
       "1. Bấm thêm folder mới\n2. Để trống ô tên → bấm Lưu\n3. Nhập chuỗi chỉ gồm khoảng trắng → Lưu",
       "Lần 1: rỗng. Lần 2: 3 dấu cách",
       "- Cả 2 lần đều báo lỗi bắt buộc nhập, KHÔNG đóng modal\n"
       "- Panel folder không phát sinh folder mới nào",
       note="Nguồn: TC bổ sung theo FUNC-002 — corpus chỉ có dòng「thêm mới」không có case validate. "
            "⚠ Spec TD-11: hầu hết endpoint save KHÔNG validate server-side → cần chạy kèm TC gọi thẳng API. ⚠ RULE-01: quan điểm `FUNC-002` trong bộ này KHÔNG có loại case **Boundary, Normal** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Folder event", "FUNC-001", "Normal",
       "Sửa tên folder → tên mới hiện ngay, event bên trong giữ nguyên",
       ADM + "\n- Folder「イベントフォルダA」đang chứa 2 event",
       "1. Bấm icon sửa của folder\n2. Đổi tên thành「セミナー」→ Lưu\n3. Reload trang\n"
       "4. Mở folder xem danh sách event",
       "Tên mới:「セミナー」",
       "- Panel folder hiện「セミナー」\n- Sau reload tên vẫn đúng\n"
       "- 2 event bên trong không đổi, không bị chuyển sang 未分類",
       note="Nguồn: Event booking 1.0 r5."),

    tc("Folder event", "FUNC-UNIQ-001", "Abnormal",
       "Tạo folder trùng tên với folder đã có → tạo được bản ghi mới với id mới",
       ADM + "\n- Đã có folder「セミナー」",
       "1. Mở edit folder「セミナー」→ copy text tên → bấm Hủy\n"
       "2. Bấm tạo mới folder → dán tên vừa copy, sửa/để nguyên → bấm Lưu\n"
       "3. Quan sát panel folder",
       "Tên dán vào:「セミナー」(trùng hoàn toàn)",
       "- Tạo folder thành công, sinh **id folder mới** trong DB\n"
       "- Panel hiện 2 folder cùng tên「セミナー」, thao tác vào từng folder đúng folder tương ứng "
       "(không nhầm sang folder kia)",
       note="Nguồn: TCsLine_Improve chung / tab「Test bug folder all màn」r174 (Bug #32468, 10/2025) — "
            "khối「11. Màn booking event」. Đây là hành vi ĐÚNG đã xác nhận: hệ thống cho phép trùng tên."),

    tc("Folder event", "DATA-REF-001", "Abnormal",
       "Xóa folder đang chứa event → folder soft-delete nhưng event bên trong bị XÓA CỨNG",
       ADM + "\n- Folder「削除テスト」chứa đúng 2 event, mỗi event có 1 slot + 1 booking approve",
       "1. Ghi lại id 2 event + id booking trước khi xóa\n"
       "2. Bấm xóa folder「削除テスト」→ xác nhận\n"
       "3. Quan sát panel folder và danh sách event ở folder 未分類\n"
       "4. Kiểm tra 2 event vừa xóa còn mở được bằng URL trực tiếp không",
       "Folder chứa 2 event, mỗi event có booking",
       "- Folder biến mất khỏi panel (DB: `category.is_deleted = 1` — soft delete)\n"
       "- 2 event **KHÔNG** được chuyển về 未分類 mà bị xóa hẳn khỏi danh sách\n"
       "- Mở URL trực tiếp của event đã xóa → không truy cập được / báo không tồn tại",
       note="Nguồn: spec BR-24 (xóa folder = soft delete folder nhưng XÓA CỨNG event bên trong). "
            "Corpus chỉ có dòng「xóa」ở Event booking 1.0 r6 (không có expected) → expected lấy theo spec. "
            "⚠ MT-04: TD-01 cảnh báo KHÔNG có transaction → phải kiểm thêm bản ghi mồ côi (xem TC nhóm này). ⚠ RULE-01: quan điểm `DATA-REF-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Folder event", "DATA-DB-001", "Abnormal",
       "Xóa folder có event → kiểm bản ghi mồ côi ở 6 bảng con (TD-01 không transaction)",
       ADM + "\n- Folder chứa 1 event có: 1 開催日, 2 slot, 3 plan, 4 booking, action đã set ở slot",
       "1. Ghi lại id của event / setting_date / slot / plan / booking / t_actions trước khi xóa\n"
       "2. Xóa folder\n"
       "3. Kiểm tra lần lượt từng bảng con: `b_setting_date_event`, `b_slot`, `b_plan_slot`, "
       "`b_user_booking`, `t_actions`, `t_actions_detail` theo id đã ghi",
       "1 event, 1 ngày, 2 slot, 3 plan, 4 booking, 2 action",
       "- KHÔNG còn bản ghi nào ở 6 bảng con trỏ tới event đã xóa\n"
       "- Không có `b_user_booking.update_to` trỏ vào booking đã bị xóa",
       note="Nguồn: TC bổ sung theo spec TD-01 (🔴 CAO — mọi DB::beginTransaction bị comment out + không có "
            "FOREIGN KEY). Corpus KHÔNG có TC kiểm mồ côi. Evidence bắt buộc: ảnh kết quả query từng bảng. Xem MT-04. ⚠ RULE-01: quan điểm `DATA-DB-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Folder event", "LIST-001", "Normal",
       "Sắp xếp folder → thứ tự giữ đúng sau reload",
       ADM + "\n- Có 4 folder: F1, F2, F3, F4",
       "1. Bấm sort folder, kéo F4 lên đầu\n2. Lưu\n3. Reload trang",
       "4 folder",
       "- Thứ tự sau lưu: F4, F1, F2, F3\n- Sau reload thứ tự không đổi",
       note="Nguồn: Event booking 1.0 r7. TC gốc chỉ có tiêu đề → expected do AI viết."),

    tc("Folder event", "STATE-001", "Normal",
       "Cookie nhớ folder đang chọn — mở lại màn list vào đúng folder cũ",
       ADM + "\n- Có folder「セミナー」khác 未分類",
       "1. Chọn folder「セミナー」ở panel trái\n2. Chuyển sang màn khác (VD màn tag)\n"
       "3. Quay lại /basic/booking-event-day/list-event\n4. Quan sát folder đang được chọn",
       "Folder「セミナー」",
       "- Màn list mở lại ở đúng folder「セミナー」(không nhảy về 未分類)\n"
       "- Danh sách event hiển thị đúng event của folder đó",
       note="Nguồn: spec §2.1 bước 1 — ghi cookie `folder_event_booking_day`, TTL 14.400 phút, "
            "path /basic/booking-event-day/list-event. Corpus KHÔNG có TC này → lấp GAP."),

    tc("Folder event", "STATE-DEP-001", "Abnormal",
       "Cookie trỏ tới folder đã bị xóa → fallback về 未分類, không lỗi trang",
       ADM + "\n- Đang chọn folder「セミナー」(cookie đã ghi)\n- Folder「セミナー」bị xóa từ tab khác / tài khoản khác",
       "1. Ở tab 1 chọn folder「セミナー」\n2. Ở tab 2 xóa folder「セミナー」\n"
       "3. Ở tab 1 reload màn list event",
       "Cookie `folder_event_booking_day` = id folder đã `is_deleted = 1`",
       "- Trang mở bình thường, KHÔNG lỗi 500\n- Tự động chọn về folder 未分類 và hiện đúng danh sách",
       note="Nguồn: spec §2.1「validate folder tồn tại (category.kind = 21, is_deleted = 0)」. TC bổ sung. ⚠ RULE-01: quan điểm `STATE-DEP-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Folder event", "BULK-001", "Normal",
       "Chuyển nhiều event sang folder khác bằng thao tác hàng loạt",
       ADM + "\n- Folder 未分類 có 5 event; đã có folder đích「セミナー」",
       "1. Tick chọn 3 event trong 5\n2. Chọn thao tác chuyển folder →「セミナー」→ xác nhận\n"
       "3. Mở folder「セミナー」đếm số event\n4. Mở lại 未分類 đếm số event",
       "Chọn 3/5 event",
       "- Folder「セミナー」có đúng **3** event vừa chuyển\n- Folder 未分類 còn **2** event\n"
       "- Chỉ 3 event được tick bị chuyển, 2 event còn lại giữ nguyên",
       note="Nguồn: Event booking 1.0 r19. TC gốc chỉ có tiêu đề → expected do AI viết (đếm cụ thể theo BULK-001)."),

    # ══════════════════ 3. Tạo & sửa event — khung ══════════════════
    tc("Tạo & sửa event — khung", "FUNC-001", "Normal",
       "Tạo event mới với đầy đủ thông tin cơ bản → lưu thành công, hiện ở list",
       ADM + "\n- Đã có folder「セミナー」",
       "1. Bấm「新規作成」\n2. Nhập「イベント名（管理用）」=「体験会2026」\n3. Chọn folder =「セミナー」\n"
       "4. Nhập「タイトル」và「説明」hiển thị phía LINE\n5. Thêm 1 開催日 + 1 予約枠\n6. Lưu\n"
       "7. Về màn list, mở folder「セミナー」",
       "Tên quản lý:「体験会2026」· folder「セミナー」· タイトル「無料体験会」",
       "- Lưu thành công, quay về màn list\n- Event「体験会2026」nằm trong folder「セミナー」\n"
       "- Mở lại event: 4 tab giữ đúng dữ liệu vừa nhập",
       note="Nguồn: Event booking 1.0 r23-r25. Spec §2.2 (SCR-EBD-02)."),

    tc("Tạo & sửa event — khung", "FUNC-002", "Abnormal",
       "Lưu event khi CHƯA tạo 予約枠 nào → chặn với message chỉ định",
       ADM,
       "1. Bấm「新規作成」→ nhập tên quản lý\n2. Thêm 開催日 nhưng KHÔNG thêm 予約枠 nào\n3. Bấm Lưu",
       "1 開催日, 0 予約枠",
       "- Hiện message「予約枠は最低1つ以上は登録してください。」\n- KHÔNG lưu, ở lại màn tạo",
       note="Nguồn: spec §1.4 (điều kiện tiên quyết — validation JS khi lưu sự kiện). Corpus KHÔNG có TC này."),

    tc("Tạo & sửa event — khung", "FUNC-004", "Boundary",
       "「イベント名（管理用）」biên 20 ký tự — 20 OK, 21 báo lỗi (validate client)",
       ADM,
       "1. Bấm「新規作成」\n2. Nhập tên quản lý 20 ký tự → Lưu → kiểm tra kết quả\n"
       "3. Tạo event khác, nhập tên 21 ký tự → Lưu\n"
       "4. Gọi thẳng API save với tên 300 ký tự (bypass client)",
       "20 ký tự: 「あいうえおかきくけこさしすせそたちつてと」\n21 ký tự: chuỗi trên + 「な」\n"
       "API: chuỗi 300 ký tự",
       "- 20 ký tự: lưu thành công\n- 21 ký tự: báo lỗi giới hạn ký tự, chặn lưu\n"
       "- Gọi thẳng API 300 ký tự: ghi rõ kết quả thật (DB `b_event_detail.title` là varchar(255) → "
       "nếu ghi được là lỗ hổng validate server-side)",
       env="STAGING",
       note="Nguồn: spec Field Matrix #1 (≤20 client-only, DB varchar(255)) + TD-11. Corpus KHÔNG test biên "
            "→ lấp GAP. Xem MT-16. ⚠ RULE-01: quan điểm `FUNC-004` trong bộ này KHÔNG có loại case **Normal** — lý do: quan điểm này chỉ phát biểu ở tình huống bất thường (race / bỏ trống / lỗi)."),

    tc("Tạo & sửa event — khung", "FUNC-004", "Boundary",
       "「タイトル」/「説明」hiển thị phía LINE — biên 50 ký tự",
       ADM + "\n- Đang ở màn tạo event",
       "1. Nhập「タイトル」50 ký tự → Lưu\n2. Nhập「タイトル」51 ký tự → Lưu\n"
       "3. Lặp lại tương tự với ô「説明」",
       "50 ký tự / 51 ký tự (tiếng Nhật)",
       "- 50 ký tự: lưu được cho cả 2 ô\n- 51 ký tự: báo lỗi giới hạn, chặn lưu",
       note="Nguồn: spec Field Matrix #3 (≤50 client). Corpus Event booking 1.0 r25「check validate」"
            "không nêu con số → lấy theo spec."),

    tc("Tạo & sửa event — khung", "MSG-004", "Normal",
       "「タイトル」/「説明」hiển thị đúng phía LINE user khi gửi link event",
       ADM + "\n- Event E có タイトル「無料体験会」, 説明「初めての方向けです」\n- Có 1 friend thật để nhận tin",
       "1. Gửi link event cho friend qua chat 1:1\n2. Mở LINE app phía friend\n"
       "3. Đối chiếu tiêu đề + mô tả trong card với giá trị đã nhập",
       "タイトル「無料体験会」· 説明「初めての方向けです」",
       "- Card LINE hiện đúng「無料体験会」và「初めての方向けです」\n"
       "- Không bị cắt chữ / hiện text mặc định",
       note="Nguồn: Event booking 1.0 r25「check gửi link event cho user => hiển thị được tên và explain phía user」. "
            "RULE-06 — verify tới output cuối trên LINE app thật. ⚠ RULE-01: quan điểm `MSG-004` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Tạo & sửa event — khung", "DATA-TEXT-001", "Normal",
       "Tên event chứa emoji + ký tự đặc biệt Nhật → lưu và hiển thị đúng ở mọi nơi",
       ADM,
       "1. Tạo event với tên quản lý chứa emoji + ký tự đặc biệt\n2. Lưu → về màn list\n"
       "3. Mở lại event\n4. Đặt 1 booking rồi mở màn 参加者リスト",
       "Tên:「AIボット🤖_Ver1・ー【】～！＠＃」",
       "- Màn list hiện đúng nguyên văn (không mojibake, không mất emoji)\n"
       "- Mở lại màn edit: ô tên giữ nguyên chuỗi\n- Màn danh sách người tham gia hiện đúng tên event",
       note="Nguồn: bộ ký tự lấy từ「Improve bill tiền stripe」r48-r52 (SpecImprove #34857). Gộp 1 TC vì "
            "cùng 1 kết quả mong đợi cho nhiều input."),

    tc("Tạo & sửa event — khung", "FUNC-SEQ-001", "Normal",
       "Sửa event đang có booking → thông tin cập nhật, booking cũ không bị ảnh hưởng",
       ADM + "\n- Event E đang có 3 booking approve",
       "1. Mở edit event E, đổi「タイトル」và「説明」\n2. Lưu\n3. Mở màn 参加者リスト của event E\n"
       "4. Kiểm tra 3 booking cũ",
       "Đổi タイトル từ「無料体験会」→「有料体験会」",
       "- Lưu thành công, tiêu đề mới hiện ở màn LINE user\n"
       "- 3 booking cũ vẫn còn đủ, status / 参加日時 / 参加人数 không đổi",
       note="TC bổ sung — corpus không có ca sửa event khi đã có booking."),

    tc("Tạo & sửa event — khung", "MEDIA-IMG-001", "Normal",
       "Upload ảnh header khi tạo / sửa / copy event → ảnh lưu đúng path và hiện phía LINE user",
       ADM,
       "1. Tạo event mới, upload「ヘッダー画像」(png 3000px)\n2. Lưu → mở trang LIFF phía LINE user\n"
       "3. Mở edit event, đổi sang ảnh khác (jpg) → Lưu → kiểm tra lại phía user\n"
       "4. Copy event → kiểm tra ảnh của bản copy",
       "Ảnh 1: png 3000 x 2000. Ảnh 2: jpg 800 x 600",
       "- Ảnh upload được, resize về tối đa 2048px\n- Trang LIFF hiện đúng ảnh mới nhất sau mỗi lần đổi\n"
       "- Bản copy hiện đúng ảnh của bản gốc (không mất ảnh, không dùng chung file bị xóa nhầm)",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung / tab「Improve nhỏ」r454-456 (Tạo/Edit/Copy event có upload ảnh header). "
            "Spec Field Matrix #8 (png/jpg, resize max 2048px imagick). RULE-08 — media BẮT BUỘC test PRODUCTION."),

    tc("Tạo & sửa event — khung", "UI-002", "Normal",
       "Selectbox chọn font chữ ở màn edit event hiển thị đúng",
       ADM + "\n- Mở /basic/booking-event-day/{id}/edit",
       "1. Mở màn edit event\n2. Mở selectbox chọn font chữ\n3. Chọn 1 font → Lưu → mở lại",
       "Event id bất kỳ",
       "- Selectbox mở được, hiện đủ danh sách font\n- Font đã chọn được lưu và hiện lại đúng khi mở lại màn",
       note="Nguồn: TCsLine_Improve chung / tab「Improve tiny form」r9「Booking event — Check hiển thị selectbox "
            "font chữ」(link staging /basic/booking-event-day/1118/edit). TC gốc chỉ có tiêu đề → expected do AI viết."),

    # ══════════════════ 4. Tab 開催日程 — ngày tổ chức ══════════════════
    tc("Tab 開催日程 — ngày tổ chức", "FUNC-001", "Normal",
       "Nút 開催日追加 mở popup lịch, chọn NHIỀU ngày một lần → lưu đủ vào DB",
       ADM + "\n- Đang ở tab「開催日程」của event mới",
       "1. Bấm nút「開催日追加」\n2. Quan sát popup\n3. Chọn 3 ngày tương lai khác nhau\n"
       "4. Bấm lưu\n5. Quan sát danh sách ngày ở tab",
       "Chọn 3 ngày: 2026-09-01, 2026-09-08, 2026-09-15",
       "- Popup hiện calendar, cho chọn NHIỀU ngày\n- Sau lưu: tab hiện đủ 3 ô ngày tổ chức\n"
       "- DB `b_setting_date_event` có 3 bản ghi với `date_start` đúng 3 ngày trên",
       note="Nguồn: Event booking 1.0 r26-r27."),

    tc("Tab 開催日程 — ngày tổ chức", "FUNC-DATE-001", "Abnormal",
       "Popup chọn ngày disable toàn bộ ngày trong QUÁ KHỨ",
       ADM + "\n- Đang ở tab「開催日程」, ngày hệ thống là 2026-08-21",
       "1. Bấm「開催日追加」\n2. Thử click ngày 2026-08-20 (hôm qua)\n3. Thử click ngày 2026-08-21 (hôm nay)\n"
       "4. Thử click ngày 2026-08-22 (mai)",
       "Hôm qua / hôm nay / ngày mai",
       "- Ngày 2026-08-20: bị disable, không chọn được\n"
       "- Ngày 2026-08-21 và 2026-08-22: chọn được\n(⚠ Nếu hôm nay cũng bị disable → ghi lại làm bug spec)",
       note="Nguồn: Event booking 1.0 r27「disable các ngày trong quá khứ」. Ranh giới 'hôm nay' KHÔNG được "
            "corpus và spec nói rõ → cần Leader xác nhận (xem MT-17)."),

    tc("Tab 開催日程 — ngày tổ chức", "FUNC-UNIQ-001", "Abnormal",
       "Chọn lại ngày đã tồn tại → bỏ qua, KHÔNG tạo bản ghi trùng",
       ADM + "\n- Event đã có 開催日 = 2026-09-01",
       "1. Bấm「開催日追加」\n2. Chọn lại đúng ngày 2026-09-01 + thêm ngày 2026-09-02\n3. Lưu\n"
       "4. Đếm số ô ngày ở tab và số bản ghi `b_setting_date_event`",
       "Chọn 2026-09-01 (đã có) + 2026-09-02 (mới)",
       "- Chỉ thêm 1 ngày mới (2026-09-02)\n- Tổng còn 2 ngày, KHÔNG có 2 bản ghi cùng `date_start = 2026-09-01`\n"
       "- Slot đã tạo ở ngày 2026-09-01 giữ nguyên",
       note="Nguồn: spec Field Matrix #30「Bỏ qua ngày trùng」. Corpus KHÔNG có TC này → lấp GAP."),

    tc("Tab 開催日程 — ngày tổ chức", "UI-003", "Normal",
       "Ô ngày tổ chức CHƯA có 予約枠 → hiện text 開催時間が登録されていません",
       ADM + "\n- Event có 1 開催日 = 2026-09-01, chưa tạo 予約枠",
       "1. Mở tab「開催日程」\n2. Quan sát ô ngày 2026-09-01",
       "0 予約枠",
       "- Ô ngày hiện text「開催時間が登録されていません」",
       note="Nguồn: Event booking 1.0 r28."),

    tc("Tab 開催日程 — ngày tổ chức", "UI-003", "Normal",
       "Ô ngày ĐÃ có 予約枠 → hiện list giờ; slot không set giờ kết thúc hiện đúng định dạng",
       ADM + "\n- Ngày 2026-09-01 có 2 slot: slot1 10:00〜12:00, slot2 14:00 (tick không set giờ kết thúc)",
       "1. Mở tab「開催日程」\n2. Quan sát ô ngày 2026-09-01",
       "slot1 có 時間終了; slot2 `is_hide_time_end = 1`",
       "- Ô ngày hiện 2 dòng giờ\n- slot1 hiện dạng「10:00〜12:00」\n"
       "- slot2 chỉ hiện giờ bắt đầu「14:00」, không hiện dấu 〜 và giờ kết thúc",
       note="Nguồn: Event booking 1.0 r29. Spec Field Matrix #32 (`is_hide_time_end`)."),

    tc("Tab 開催日程 — ngày tổ chức", "UI-INPUT-001", "Normal",
       "Rê chuột vào ô ngày → đổi màu nền; click → mở màn quản lý slot của ngày đó",
       ADM + "\n- Event có 開催日 = 2026-09-01",
       "1. Rê chuột vào ô ngày 2026-09-01\n2. Click vào ô ngày\n3. Quan sát màn hình mở ra",
       "1 開催日",
       "- Rê chuột: ô ngày đổi màu nền (có phản hồi hover)\n"
       "- Click: mở màn「開催日」(SCR-EBD-06) đúng ngày 2026-09-01, hiện danh sách slot của ngày đó",
       note="Nguồn: Event booking 1.0 r30."),

    tc("Tab 開催日程 — ngày tổ chức", "FUNC-001", "Normal",
       "Setting 表示予約 (thời điểm mở bán slot) — lưu theo duration + giờ",
       ADM + "\n- Event có 開催日 = 2026-05-27",
       "1. Ở ô ngày bấm nút setting「表示予約」\n2. Chọn「開催」1「日前の」+ giờ 08:00\n3. Lưu\n"
       "4. Mở lại modal kiểm tra giá trị\n5. Kiểm tra DB `b_setting_date_event`",
       "duration = 1 ngày, time = 08:00, date_start = 2026-05-27",
       "- Modal lưu được, mở lại hiện đúng 1 日前 + 08:00\n"
       "- DB: `duration` = 1, `time_show_slot` = 08:00, `date_show_slot` = **2026-05-26**",
       note="Nguồn: Event booking 2.0 r5-r6 (05/2023). Spec BR-15 (`date_show_slot = date_start − duration`)."),

    tc("Tab 開催日程 — ngày tổ chức", "FUNC-DATE-001", "Boundary",
       "表示予約 — CHƯA setting (thiếu duration hoặc giờ) → 3 cột = NULL, slot mở bán ngay",
       ADM + "\n- Event có 開催日 = 2026-09-01, chưa từng set 表示予約",
       "1. Mở tab「開催日程」quan sát nhãn setting 表示予約 khi chưa set\n"
       "2. Mở modal, chỉ nhập duration, để trống giờ → Lưu\n3. Kiểm tra DB\n"
       "4. Mở trang LIFF phía LINE user xem slot có hiện không",
       "Trường hợp A: chưa set gì. Trường hợp B: có duration, thiếu giờ",
       "- Cả 2 trường hợp: DB `duration`, `time_show_slot`, `date_show_slot` đều = **NULL**\n"
       "- Phía LINE user: slot của ngày đó **hiện ngay**, không bị ẩn",
       note="Nguồn: spec BR-15 + G-05. Corpus Event booking 2.0 r3-r4「chưa setting / sau khi đã set」chỉ có "
            "tiêu đề → expected lấy theo spec, cần Leader xác nhận."),

    tc("Tab 開催日程 — ngày tổ chức", "FUNC-DATE-001", "Boundary",
       "表示予約 — trước/đúng/sau thời điểm mở bán, slot hiện đúng phía LINE user",
       ADM + "\n- Event có 開催日 = 2026-09-01, set 表示予約 = 1 日前 08:00 → mở bán 2026-08-31 08:00\n"
       "- Có tài khoản LINE test",
       "1. Đặt thời điểm test là 2026-08-31 07:59 → mở trang LIFF, quan sát ngày 2026-09-01\n"
       "2. Đặt thời điểm 2026-08-31 08:00 → reload trang LIFF\n"
       "3. Đặt thời điểm 2026-08-31 08:01 → reload trang LIFF",
       "3 mốc: 07:59 / 08:00 / 08:01 ngày 2026-08-31",
       "- 07:59: **KHÔNG hiện** slot nào của ngày 2026-09-01\n"
       "- 08:00 và 08:01: hiện đầy đủ slot của ngày 2026-09-01, chọn được\n"
       "- Các ngày khác không bị ảnh hưởng",
       note="Nguồn: Event booking 1.0 r111 + Event booking 2.0 r6. Spec BR-15. "
            "Đây là ranh giới ngày giờ (FUNC-DATE-001) — bắt buộc test cả 3 mốc."),

    tc("Tab 開催日程 — ngày tổ chức", "STATE-DEP-001", "Normal",
       "Đổi 開催日 → recompute lại toàn bộ mốc suy diễn (締切 / 変更期限 / キャンセル期限 / 表示予約)",
       ADM + "\n- 開催日 = 2026-09-01, slot có: 締切 = 3 日前, 変更期限 = 2 日前, キャンセル期限 = 1 日前; "
       "表示予約 = 5 日前 09:00",
       "1. Ghi lại `date_deadline`, `date_end_change_request`, `date_end_cancel`, `date_show_slot` hiện tại\n"
       "2. Đổi 開催日 sang 2026-09-10\n3. Lưu\n4. Đọc lại 4 cột trên",
       "date_start: 2026-09-01 → 2026-09-10 (dịch +9 ngày)",
       "- `date_deadline` = 2026-09-07 · `date_end_change_request` = 2026-09-08 · "
       "`date_end_cancel` = 2026-09-09 · `date_show_slot` = 2026-09-05\n"
       "- Cả 4 mốc đều dịch theo, KHÔNG còn giữ giá trị tính theo ngày cũ",
       note="Nguồn: spec BR-13 (`:6445-6458` recompute). Corpus Event booking 2.0 r7/r10/r16/r19「check recover」"
            "chỉ có tiêu đề → expected lấy theo spec. Đây là điểm dễ lọt bug nhất của cơ chế duration."),

    tc("Tab 開催日程 — ngày tổ chức", "DATA-REF-001", "Abnormal",
       "Nút 開催日を削除 → popup xác nhận, xóa ngày kèm toàn bộ slot / plan / booking của ngày đó",
       ADM + "\n- Event có 2 開催日: D1 (2 slot, mỗi slot 1 plan, tổng 3 booking) và D2 (1 slot, 2 booking)",
       "1. Ghi lại id slot/plan/booking của D1 và D2\n2. Ở ô ngày D1 bấm「開催日を削除」\n"
       "3. Quan sát popup xác nhận → bấm OK\n4. Kiểm tra DB các bảng con theo id đã ghi",
       "D1: 2 slot, 2 plan, 3 booking. D2: 1 slot, 2 booking",
       "- Hiện popup confirm trước khi xóa\n- Sau OK: D1 biến mất; toàn bộ slot / plan / booking của D1 bị xóa "
       "khỏi `b_slot`, `b_plan_slot`, `b_user_booking`\n"
       "- **D2 nguyên vẹn**: 1 slot + 2 booking vẫn còn đủ",
       note="Nguồn: Event booking 1.0 r112 + Task nhỏ r10-r11「btn xóa all slot 開催日を削除 → xóa all booking "
            "của các plan trong slot; slot khác cùng event vẫn còn trong tbl b_user_booking」."),

    tc("Tab 開催日程 — ngày tổ chức", "DATA-BACKUP-001", "Normal",
       "Copy 開催日 → nhân bản đủ slot + plan, KHÔNG nhân bản booking",
       ADM + "\n- 開催日 D1 = 2026-09-01 có 2 slot, mỗi slot 1 plan, có 3 booking approve",
       "1. Bấm copy ngày D1, chọn ngày đích 2026-09-08\n2. Lưu\n"
       "3. Mở ngày 2026-09-08 kiểm tra slot + plan\n4. Mở màn 参加者リスト lọc theo ngày 2026-09-08",
       "D1 có 2 slot × 1 plan + 3 booking",
       "- Ngày 2026-09-08 có đủ 2 slot với giờ / 定員 / 承認方法 / action giống D1\n"
       "- Mỗi slot có 1 plan giống bản gốc\n"
       "- **KHÔNG có booking nào** ở ngày mới; `use_people` và `remain_limit` của slot/plan mới = 0",
       note="Nguồn: Event booking 1.0 r113「Check copy ngày triển khai」— TC gốc chỉ có tiêu đề → "
            "expected do AI viết theo DATA-BACKUP-001, cần Leader xác nhận (đặc biệt: copy có kéo theo booking không). ⚠ RULE-01: quan điểm `DATA-BACKUP-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    # ══════════════════ 5. Khung giờ 予約枠 ══════════════════
    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "Nút 開催時刻追加 → tạo slot mới với giờ bắt đầu + giờ kết thúc",
       ADM + "\n- Đang ở màn「開催日」của ngày 2026-09-01",
       "1. Bấm「開催時刻追加」\n2. Set giờ bắt đầu 10:00, giờ kết thúc 12:00\n"
       "3. Set 締切日時 (bắt buộc)\n4. Lưu\n5. Quan sát danh sách slot",
       "10:00 〜 12:00",
       "- Slot mới xuất hiện trong danh sách, hiện「10:00〜12:00」\n"
       "- DB `b_slot`: `time_start` = 10:00, `time_end` = 12:00, `is_hide_time_end` = 0",
       note="Nguồn: Event booking 1.0 r31-r32."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "Tick「giờ kết thúc không set」→ slot chỉ hiện giờ bắt đầu ở cả admin và LINE user",
       ADM + "\n- Đang tạo slot mới",
       "1. Set giờ bắt đầu 14:00\n2. Tick checkbox không set giờ kết thúc\n3. Lưu\n"
       "4. Quan sát danh sách slot phía admin\n5. Mở trang LIFF phía LINE user",
       "14:00, không set giờ kết thúc",
       "- Admin: slot hiện「14:00」(không có 〜 và giờ kết thúc)\n- LINE user: cũng chỉ hiện「14:00」\n"
       "- DB `b_slot.is_hide_time_end` = 1",
       note="Nguồn: Event booking 1.0 r33 + r98-r99. RULE-07 — verify cả DB, màn admin và màn LINE user."),

    tc("Khung giờ 予約枠", "FUNC-002", "Abnormal",
       "Lưu slot khi để trống 開催時間 hoặc 締切日時 → báo lỗi chỉ định (EP-37 có validate server)",
       ADM + "\n- Đang tạo slot mới",
       "1. Để trống giờ bắt đầu → Lưu → ghi lại message\n"
       "2. Nhập giờ bắt đầu, để trống 締切日時 → Lưu → ghi lại message\n"
       "3. Nhập giờ bắt đầu 12:00 > giờ kết thúc 10:00 → Lưu",
       "Case A: trống giờ. Case B: trống 締切. Case C: start 12:00 > end 10:00",
       "- Case A: 「開催時間は必ず指定してください。」, chặn lưu\n"
       "- Case B: 「予約期限は必ず指定してください。」, chặn lưu\n"
       "- Case C: báo lỗi giờ bắt đầu lớn hơn giờ kết thúc, chặn lưu",
       note="Nguồn: Event booking 1.0 r34「bắt buộc nhập」+ spec Field Matrix #32/#33 (EP-37 là endpoint "
            "DUY NHẤT có validation server-side). Text message lấy từ spec."),

    tc("Khung giờ 予約枠", "FUNC-004", "Boundary",
       "定員 slot — để trống = 無制限; nhập 0 và nhập 1 cho kết quả khác nhau",
       ADM + "\n- Đang tạo slot mới",
       "1. Để trống ô 定員 → Lưu → mở màn LINE user xem cột 残数\n"
       "2. Nhập 定員 = 0 → Lưu → ghi lại message\n3. Nhập 定員 = 1 → Lưu",
       "Trống / 0 / 1",
       "- Trống: lưu được, `number_people = NULL`; LINE user hiện dấu **-** (không giới hạn)\n"
       "- 0: báo lỗi「定員は0以上入力してください。」/「定員には１以上入力してください」— chặn lưu\n"
       "- 1: lưu được, LINE user hiện 残数 1",
       note="Nguồn: Event booking 1.0 r35-r36 + r100-r101. Spec Field Matrix #34, BR-07. "
            "⚠ Spec ghi 2 message khác nhau cho case 0 → xem MT-18."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "予約承認方法 = 全承認 → booking mới có status = 5 (予約済み), cộng ngay use_people",
       ADM + "\n- Slot S1 定員 = 10, 承認方法 = 全承認 (`approval_system = 0`), không có コース\n"
       "- Có tài khoản LINE test",
       "1. LINE user đặt 1 chỗ ở slot S1 (số lượng = 1)\n2. Kiểm tra `b_user_booking.status`\n"
       "3. Kiểm tra `b_slot.use_people`\n4. Mở màn 参加者リスト phía admin",
       "quantity = 1, 承認方法 = 全承認",
       "- `b_user_booking.status` = **5**\n- `b_slot.use_people` tăng **+1** ngay lập tức\n"
       "- Màn 参加者リスト hiện booking với badge trạng thái đã đặt",
       note="Nguồn: Event booking 1.0 r37 + Task nhỏ r68. Spec BR-18 + BR-08."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "予約承認方法 = リクエスト制 → booking mới status = 3, KHÔNG cộng use_people",
       ADM + "\n- Slot S2 定員 = 10, 承認方法 = リクエスト制 (`approval_system = 1`), không có コース\n"
       "- `use_people` hiện tại = 0",
       "1. LINE user đặt 1 chỗ ở slot S2\n2. Kiểm tra `b_user_booking.status`\n"
       "3. Kiểm tra `b_slot.use_people`\n4. Mở màn list event xem cột 承認待ち",
       "quantity = 1, 承認方法 = リクエスト制",
       "- `b_user_booking.status` = **3** (承認待ち)\n- `b_slot.use_people` vẫn = **0** (chưa cộng)\n"
       "- Cột「承認待ち」ở màn list event tăng lên 1",
       note="Nguồn: Event booking 1.0 r38 + Task nhỏ r69. Spec BR-18."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "Bật リマインド配信 và chọn remind → lưu event_id + remind_id vào slot",
       ADM + "\n- Đã tạo sẵn 1 リマインド ở màn /basic/events với ít nhất 2 step",
       "1. Ở màn setting slot, bật「リマインド配信」\n2. Ở「リマインド選択」chọn remind đã tạo\n3. Lưu\n"
       "4. Mở lại màn setting slot\n5. Kiểm tra DB `b_slot`",
       "Remind「体験会リマインド」",
       "- Mở lại: toggle vẫn bật, dropdown hiện đúng remind đã chọn\n"
       "- DB: `is_use_remind` = 1, `event_id` = id của remind, `remind_id` = id `event_times` tương ứng",
       note="Nguồn: Event booking 1.0 r39. Spec Field Matrix #38, BR-22 (cross-ref FA-022)."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "予約変更 / 予約キャンセル — 3 lựa chọn 全承認 / リクエスト制 / 不可 lưu đúng",
       ADM + "\n- Đang ở màn setting slot",
       "1. Set「予約変更」= 全承認 → Lưu → mở lại kiểm tra\n2. Đổi sang リクエスト制 → Lưu → mở lại\n"
       "3. Đổi sang 不可 → Lưu → mở lại\n4. Lặp lại 3 bước trên với「予約キャンセル」",
       "3 giá trị × 2 setting",
       "- Mỗi lần lưu, mở lại đều hiện đúng giá trị vừa chọn\n"
       "- DB `approval_system_change_request` / `approval_system_cancel` nhận đúng giá trị "
       "(2 = 不可)",
       note="Nguồn: Event booking 1.0 r46-r48, r56-r58. Spec Field Matrix #39. "
            "Gộp 1 TC vì cùng 1 kết quả mong đợi (lưu và hiện lại đúng)."),

    tc("Khung giờ 予約枠", "FUNC-DATE-001", "Normal",
       "締切日時 / 変更受付期限 / キャンセル受付期限 theo duration → tính đúng ngày tuyệt đối",
       ADM + "\n- 開催日 = 2026-09-10, đang ở màn setting slot",
       "1. Set 締切 = 3 日前 18:00 → Lưu\n2. Set 変更受付期限 = 2 日前 12:00 → Lưu\n"
       "3. Set キャンセル受付期限 = 1 日前 09:00 → Lưu\n4. Đọc DB 3 cặp cột duration/time và 3 cột date suy diễn",
       "date_start = 2026-09-10; duration lần lượt 3 / 2 / 1 ngày",
       "- `date_deadline` = 2026-09-07 (kèm `time_deadline` = 18:00)\n"
       "- `date_end_change_request` = 2026-09-08 12:00\n- `date_end_cancel` = 2026-09-09 09:00",
       note="Nguồn: Event booking 2.0 r8, r14, r17. Spec BR-13."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "Tick 期限なし (`is_no_datetime_end_*`) → không áp hạn đổi / hủy",
       ADM + "\n- Slot có 変更受付期限 đã qua (2026-08-01)\n- Có booking approve của LINE user test",
       "1. Ở màn setting slot tick「期限なし」cho 予約変更\n2. Lưu\n"
       "3. Phía LINE user mở lịch sử → detail booking\n4. Quan sát nút đổi lịch",
       "Hạn đổi đã qua nhưng tick 期限なし",
       "- Nút đổi lịch **vẫn hiện** và bấm được (không bị chặn bởi hạn cũ)\n"
       "- Bỏ tick 期限なし → nút đổi lịch biến mất",
       note="Nguồn: spec BR-14 + Field Matrix #40 (`setting_deadline = 0` → luôn cho phép). "
            "Corpus Event booking 1.0 r49/r59「setting time cuối được phép change/cancel booking」không có "
            "expected → expected lấy theo spec."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "予約可能回数 mức slot chỉ có hiệu lực khi 各日程ごとに設定する được bật",
       ADM + "\n- Event: 詳細設定 →「予約可能回数」= 何度でも, ĐANG tick「各日程ごとに設定する」\n"
       "- Slot S1 set「予約可能回数」= 各予約枠 1 回 (`times_booking = 2`)",
       "1. LINE user đặt 1 chỗ ở slot S1 → thành công\n"
       "2. LINE user quay lại trang đặt chỗ, thử đặt tiếp slot S1\n"
       "3. Bỏ tick「各日程ごとに設定する」ở tab 詳細設定 → Lưu\n4. LINE user reload, thử đặt lại slot S1",
       "`is_set_each_booking` = 1 → 0",
       "- Bước 2: slot S1 **bị ẩn / không chọn được** (đã dùng hết lượt của slot)\n"
       "- Bước 4: sau khi bỏ tick, áp setting chung 何度でも → slot S1 **đặt tiếp được**",
       note="Nguồn: Event booking 2.0 r12-r13. Spec BR-11 + BR-12."),

    tc("Khung giờ 予約枠", "FUNC-001", "Normal",
       "Copy slot → nhân bản đủ setting + action, KHÔNG nhân bản booking và bộ đếm",
       ADM + "\n- Slot S1: 10:00〜12:00, 定員 5, `use_people` = 3, 承認方法 リクエスト制, đã set 4 action booking",
       "1. Bấm copy slot S1\n2. Quan sát slot mới sinh ra\n3. Đối chiếu từng setting với S1\n"
       "4. Kiểm tra `use_people` của slot mới",
       "S1 có use_people = 3",
       "- Slot mới có cùng giờ / 定員 / 承認方法 / 4 action đã set\n"
       "- `use_people` của slot mới = **0** (không copy bộ đếm)\n- Không có booking nào thuộc slot mới",
       note="Nguồn: Event booking 1.0 r105「check copy slot」— TC gốc chỉ có tiêu đề → expected do AI viết "
            "theo DATA-BACKUP-001, cần Leader xác nhận."),

    tc("Khung giờ 予約枠", "DATA-REF-001", "Abnormal",
       "Xóa slot → xóa luôn plan và booking của slot đó, slot khác cùng event KHÔNG bị ảnh hưởng",
       ADM + "\n- Ngày D1 có slot A (2 plan, 3 booking) và slot B (1 plan, 2 booking)",
       "1. Ghi lại id plan + booking của slot A và slot B\n2. Xóa slot A\n"
       "3. Query `b_user_booking` theo `slot_id` của A và của B\n4. Query `b_plan_slot` tương tự",
       "slot A: 2 plan + 3 booking. slot B: 1 plan + 2 booking",
       "- Toàn bộ 3 booking của slot A bị xóa khỏi `b_user_booking` (xóa theo `slot_id`, "
       "không phân biệt status)\n- 2 plan của slot A bị xóa\n"
       "- Slot B: 1 plan + 2 booking **vẫn còn nguyên**",
       note="Nguồn: Task nhỏ + fix bug KH r5, r9, r11 (tab master)「Xóa slot thì xóa plan slot và các booking "
            "của plan và slot — tbl b_user_booking xóa theo slot_id nên ko cần check các loại status booking」."),

    tc("Khung giờ 予約枠", "LIST-001", "Normal",
       "Màn 予約枠一覧 — lọc slot đã diễn ra / chưa diễn ra",
       ADM + "\n- Event có 3 slot: 1 slot ngày quá khứ, 2 slot ngày tương lai",
       "1. Mở màn「予約枠一覧」từ màn list event\n2. Chọn filter「chưa triển khai」→ đếm dòng\n"
       "3. Chọn filter「đã triển khai」→ đếm dòng",
       "1 slot quá khứ, 2 slot tương lai",
       "- Filter chưa triển khai: hiện đúng **2** slot tương lai\n"
       "- Filter đã triển khai: hiện đúng **1** slot quá khứ\n- Không slot nào xuất hiện ở cả 2 filter",
       note="Nguồn: Event booking 1.0 r329/r331 + r352「Check màn list slot」. TC gốc chỉ có tiêu đề → "
            "expected do AI viết. Spec §2.6 (SCR-EBD-09)."),

    # ══════════════════ 6. Gói コース (plan) ══════════════════
    tc("Gói コース (plan)", "FUNC-001", "Normal",
       "Tạo コース với tên + 定員 + 料金 → lưu và hiện ở danh sách slot",
       ADM + "\n- Slot S1 đã tồn tại, chưa có コース nào",
       "1. Ở màn setting slot bấm tạo コース\n2. Nhập tên「Aコース」, 定員 = 3, 料金 = 5000\n3. Lưu\n"
       "4. Quan sát danh sách slot ở tab 開催日程",
       "「Aコース」· 定員 3 · 料金 5000円",
       "- コース lưu thành công\n- Danh sách slot hiện đủ 3 thông tin của コース: tên, 定員, 料金\n"
       "- DB `b_plan_slot`: `name` =「Aコース」, `limit` = 3, `price` = 5000",
       note="Nguồn: Event booking 1.0 r72-r74, r103."),

    tc("Gói コース (plan)", "FUNC-004", "Boundary",
       "料金 コース — mặc định để trống; biên 50 円 (49 lỗi / 50 OK)",
       ADM + "\n- Đang tạo コース mới",
       "1. Quan sát giá trị mặc định ô 料金\n2. Nhập 49 → Lưu → ghi message\n3. Nhập 50 → Lưu\n"
       "4. Nhập「5.000」(có dấu chấm) → Lưu → kiểm tra DB",
       "Mặc định trống · 49 · 50 · 5.000",
       "- Mặc định: ô 料金 để trống (blank)\n- 49: báo lỗi「料金は50円以上入力してください。」, chặn lưu\n"
       "- 50: lưu được\n- 「5.000」: lưu vào DB thành **5000** (bỏ dấu chấm)",
       note="Nguồn: Event booking 1.0 r74「Default là không nhập (để blank), validate nhập >50 yên」+ "
            "spec Field Matrix #45. ⚠ Corpus ghi 「>50」 còn spec ghi 「≥50」 → xem MT-19."),

    tc("Gói コース (plan)", "FUNC-004", "Boundary",
       "定員 コース — nhập 0 báo lỗi, nhập 1 lưu được",
       ADM + "\n- Đang tạo コース mới, KHÔNG tick「予約枠の定員の残数に合わせる」",
       "1. Nhập 定員 = 0 → Lưu → ghi message\n2. Nhập 定員 = 1 → Lưu",
       "0 / 1",
       "- 0: báo lỗi「1以上入力してください」, chặn lưu\n- 1: lưu được, `b_plan_slot.limit` = 1",
       note="Nguồn: spec Field Matrix #44. Corpus không test biên → lấp GAP."),

    tc("Gói コース (plan)", "FUNC-001", "Normal",
       "Tick 予約枠の定員の残数に合わせる → コース dùng chung 定員 của slot, LINE user hiện remain theo slot",
       ADM + "\n- Slot S1 定員 = 5, có 1 コース「Aコース」tick「予約枠の定員の残数に合わせる」",
       "1. Kiểm tra DB `b_plan_slot.using_max_slot`\n2. Mở trang LIFF phía LINE user\n"
       "3. Quan sát 残数 của「Aコース」\n4. Đặt 2 chỗ → reload → quan sát lại",
       "Slot 定員 = 5, plan dùng chung",
       "- `using_max_slot` = 1\n- Trước khi đặt: 残数 của コース = **5** (theo slot)\n"
       "- Sau khi đặt 2 chỗ: 残数 = **3**",
       note="Nguồn: Event booking 2.0 r34-r35 + spec BR-07."),

    tc("Gói コース (plan)", "LIST-001", "Normal",
       "Sort コース → thứ tự phía LINE user đổi theo đúng thứ tự đã sắp",
       ADM + "\n- Slot S1 có 3 コース theo thứ tự: A, B, C",
       "1. Ở màn list コース kéo C lên đầu → Lưu\n2. Reload màn admin kiểm tra thứ tự\n"
       "3. Mở trang LIFF phía LINE user, chọn slot S1\n4. Quan sát thứ tự コース",
       "3 コース: A, B, C → sắp lại C, A, B",
       "- Màn admin sau reload: C, A, B\n- **Màn LINE user: cũng là C, A, B** (khớp thứ tự đã sort)",
       note="Nguồn: Event booking 1.0 r108「Sau khi sort xong check bên màn hình phía user hiện đúng theo thứ tự "
            "đã sort hay không」. RULE-07 — verify cả 2 đầu."),

    tc("Gói コース (plan)", "DATA-BACKUP-001", "Normal",
       "Copy コース → nhân bản setting, bộ đếm remain_limit về 0",
       ADM + "\n- コース「Aコース」có 定員 3, 料金 5000, `remain_limit` = 2, đã set 4 action",
       "1. Bấm copy「Aコース」\n2. Đối chiếu setting của bản copy với bản gốc\n"
       "3. Kiểm tra `remain_limit` của bản copy",
       "Bản gốc có remain_limit = 2",
       "- Bản copy có cùng 定員 / 料金 / 4 action\n- `remain_limit` của bản copy = **0**\n"
       "- Không booking nào của bản gốc bị gán sang bản copy",
       note="Nguồn: Event booking 1.0 r109「copy course」— TC gốc chỉ có tiêu đề → expected do AI viết, "
            "cần Leader xác nhận."),

    tc("Gói コース (plan)", "DATA-REF-001", "Abnormal",
       "Xóa コース → chỉ xóa booking của コース đó, コース cùng slot và khác slot đều còn nguyên",
       ADM + "\n- Slot S1 có plan P1 (2 booking) và plan P2 (1 booking)\n- Slot S2 có plan P3 (1 booking)",
       "1. Ghi lại id booking của P1, P2, P3\n2. Xóa plan P1\n"
       "3. Query `b_user_booking` theo `plan_slot_id` của P1, P2, P3",
       "P1: 2 booking · P2: 1 booking · P3: 1 booking",
       "- Booking của P1 (2 bản ghi) bị xóa khỏi `b_user_booking`\n"
       "- Booking của **P2 (cùng slot) vẫn còn**\n- Booking của **P3 (khác slot) vẫn còn**",
       note="Nguồn: Task nhỏ + fix bug KH r6-r8 (tab master)「xóa plan → chỉ xóa data trong tbl b_user_booking "
            "của plan đó, search theo plan_slot_id」."),

    tc("Gói コース (plan)", "UI-003", "Normal",
       "Cảnh báo phụ thuộc 決済 ↔ コース hiển thị đúng ở màn setting",
       ADM + "\n- Event đã bật「決済機能の利用」ở tab 決済設定",
       "1. Mở màn setting slot chưa có コース nào\n2. Quan sát vùng cảnh báo",
       "決済 bật, slot chưa có コース",
       "- Hiện cảnh báo「決済はコースの料金設定に紐づきますので決済を利用する場合は、コース設定が必須となります。」",
       note="Nguồn: spec §1.4 (điều kiện tiên quyết). Corpus KHÔNG có TC này → lấp GAP."),
]

# ── Bổ sung sau BƯỚC 7 (audit coverage vs Field Traceability Matrix) ──────────
S1 += [
    tc("Gói コース (plan)", "FUNC-004", "Boundary",
       "「コース名」biên 50 ký tự",
       ADM + "\n- Đang tạo コース mới ở slot S1",
       "1. Nhập tên コース 50 ký tự → Lưu\n2. Nhập tên コース 51 ký tự → Lưu → ghi message\n"
       "3. Với tên lưu được, mở trang LIFF phía LINE user xem hiển thị",
       "50 / 51 ký tự tiếng Nhật",
       "- 50 ký tự: lưu được, DB `b_plan_slot.name` giữ đủ chuỗi\n"
       "- 51 ký tự: báo lỗi giới hạn ký tự, chặn lưu\n- Trang LIFF hiện đủ tên 50 ký tự, không vỡ layout",
       note="Nguồn: spec Field Matrix #43 (「コース名」≤50). Corpus KHÔNG test biên → bổ sung sau BƯỚC 7 audit."),
]
