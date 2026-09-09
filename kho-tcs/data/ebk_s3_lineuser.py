# -*- coding: utf-8 -*-
"""FA-021 イベント予約 — Nhóm 14-20: toàn bộ luồng phía LINE user (LIFF).

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Event booking 1.0」r153-r194 (mở link, chọn slot, nhập form), r252-r320 (change/cancel),
    r161-r173 (Bug #31908 + disable button khi chưa lấy được line id, 09/2025)
  - tab「SpecChange #26808」(14/10/2024) — TOÀN BỘ ma trận giới hạn số chỗ slot × plan
  - tab「Improve bill tiền univapay」r113-r144 — màn lịch sử booking phía LINE user theo status_webhook
  - tab「Event booking 2.0」r29-r59 — max plan / max slot khi đặt và đổi lịch
Bổ sung: TCsLine_Improve chung / tab「Improve nhỏ」r324, r330 (line user mở link khi là/không là friend).
"""
from _common import tc

USR = "- Có tài khoản LINE test U1 đã kết bạn với bot A\n- Event E đã publish, có link LIFF"
SLOT_OK = USR + "\n- Slot S1 còn hạn, còn chỗ, 承認方法 = 全承認"

S3 = [
    # ══════════════════ 14. LINE user — mở link & entry ══════════════════
    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Normal",
       "Mở link đặt chỗ bằng LINE app (đã là friend) → hiện calendar và chọn slot bình thường",
       SLOT_OK,
       "1. Gửi link LIFF của event E cho U1 qua chat 1:1\n2. U1 bấm link, mở trong LINE app\n"
       "3. Quan sát màn hình\n4. Click chọn 1 slot",
       "U1 là friend của bot A",
       "- Hiện được calendar các 開催日\n- Hiện đúng các setting đã cấu hình ở màn quản lý "
       "(ảnh, tiêu đề, mô tả, nút)\n- Click chọn slot bình thường",
       note="Nguồn: Event booking 1.0 r162. Bổ sung: TCsLine_Improve chung /「Improve nhỏ」r324."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Abnormal",
       "Mở link đặt chỗ khi CHƯA là friend của bot → hiện màn kết bạn",
       "- Tài khoản LINE U2 **CHƯA** kết bạn với bot A\n- Event E đã publish",
       "1. U2 mở link LIFF của event E\n2. Quan sát màn hình\n3. Kết bạn với bot A → mở lại link",
       "U2 chưa là friend",
       "- Hiện **màn hình kết bạn**, không vào được trang đặt chỗ\n"
       "- Sau khi kết bạn, mở lại link: vào được trang đặt chỗ bình thường",
       note="Nguồn: TCsLine_Improve chung /「Improve nhỏ」r330「Line user booking event → Hiển thị màn hình kết bạn」."),

    tc("LINE user — mở link & entry", "LIFF-ENTRY-001", "Abnormal",
       "Mở link bằng app NGOÀI LINE (trình duyệt thường) → vẫn hiện calendar và đặt được",
       SLOT_OK,
       "1. Copy link LIFF, mở bằng Safari/Chrome trên điện thoại (ngoài LINE)\n2. Quan sát màn hình\n"
       "3. Thực hiện đặt 1 chỗ",
       "Mở bằng trình duyệt ngoài LINE",
       "- Sau khi lấy được line id: hiện calendar + đúng setting, click chọn slot bình thường\n"
       "- Đặt chỗ thành công, có gửi action sau khi đặt",
       note="Nguồn: Event booking 1.0 r168-r169「Check mở bằng app ngoài」."),

    tc("LINE user — mở link & entry", "UI-003", "Abnormal",
       "CHƯA lấy được line_id → nút submit bị disable với đúng màu quy định",
       USR + "\n- Mô phỏng trạng thái chưa lấy được line id (chặn/làm chậm bước lấy profile LIFF)",
       "1. Mở link đặt chỗ\n2. Trước khi line id được nạp, quan sát nút submit\n"
       "3. Kiểm tra màu nền và màu chữ của nút (DevTools hoặc so ảnh)",
       "Trạng thái chưa có line_id",
       "- Nút submit **bị disable**, không bấm được\n"
       "- Màu nền = **#F0F0F0**, màu chữ = **#222222**",
       note="Nguồn: Event booking 1.0 r161, r165, r171 (Bug: disable button submit khi chưa lấy line id, 09/2025). "
            "Ảnh chuẩn: https://prnt.sc/dQ3pN8Lglnf0"),

    tc("LINE user — mở link & entry", "STATE-001", "Abnormal",
       "Reload trang khi chưa lấy được line_id → vẫn disable; lấy được thì hiện calendar",
       USR + "\n- Đang ở trạng thái chưa lấy được line id, nút submit đang disable",
       "1. Reload lại link\n2. Nếu vẫn chưa lấy được line id → quan sát nút submit\n"
       "3. Khi đã lấy được line id → quan sát màn hình",
       "2 kết quả reload khác nhau",
       "- Reload mà vẫn chưa có line id: nút **vẫn disable** (#F0F0F0 / #222222)\n"
       "- Reload mà lấy được line id: **hiện calendar**, nút submit bấm được",
       note="Nguồn: Event booking 1.0 r166-r167 và r172-r173."),

    tc("LINE user — mở link & entry", "CONC-001", "Abnormal",
       "Double-click nút đặt chỗ → KHÔNG tạo booking trùng",
       SLOT_OK,
       "1. U1 điền đủ form, tới màn xác nhận\n2. Double-click nhanh (<300ms) nút xác nhận\n"
       "3. Đếm số bản ghi `b_user_booking` của U1 ở slot S1\n4. Đọc `b_slot.use_people`\n"
       "5. Đếm số tin action nhận được trên LINE",
       "1 lần double-click",
       "- Chỉ tạo **1** booking\n- `use_people` chỉ tăng **+1**\n- LINE user nhận **1** tin action",
       note="Nguồn: Event booking 1.0 r164 và r170「Check double click button → Không bị book duplicate」. "
            "RULE-07 — verify 3 tầng: DB, bộ đếm, output LINE. ⚠ RULE-01: quan điểm `CONC-001` trong bộ này KHÔNG có loại case **Boundary, Normal** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("LINE user — mở link & entry", "SEC-ISO-001", "Abnormal",
       "Bot A không mở được link đặt chỗ của event thuộc bot B",
       "- Bot A và bot B là 2 tài khoản LINE OA khác nhau\n- Bot B có event F (id đã biết)\n"
       "- U1 là friend của bot A, KHÔNG phải friend bot B",
       "1. Lấy URL LIFF của event F (bot B)\n2. Đổi phần liff_app_id sang liff_app_id_booking của bot A\n"
       "3. U1 mở URL đã sửa\n4. Quan sát kết quả",
       "URL lai: LIFF bot A + booking_event_id của bot B",
       "- **Không mở được** trang đặt chỗ của event F\n"
       "- Không lộ tiêu đề / mô tả / danh sách slot của event thuộc bot B",
       note="Nguồn: TCsLine_Improve chung /「Improve nhỏ」r304 và khối Bug Tester #33107「Bot A đang access được "
            "link của bot B => Check lại cho all màn」— corpus xác nhận NG ở màn template/item. "
            "TC này áp cho event booking → **có thể FAIL, cần raise bug nếu tái hiện**. Xem MT-09."),

    # ══════════════════ 15. LINE user — chọn slot & plan ══════════════════
    tc("LINE user — chọn slot & plan", "UI-003", "Abnormal",
       "Không có slot nào thỏa điều kiện đặt → hiện message không có slot",
       USR + "\n- Event E có 1 開催日 nhưng toàn bộ slot đã quá 締切, toggle 受付終了 = 非表示",
       "1. U1 mở trang đặt chỗ\n2. Quan sát danh sách slot",
       "0 slot khả dụng",
       "- Hiện message thông báo không có slot nào\n- KHÔNG hiện danh sách trống không lời giải thích\n"
       "- Không lỗi trang",
       note="Nguồn: Event booking 1.0 r176."),

    tc("LINE user — chọn slot & plan", "DATA-COUNT-001", "Normal",
       "Hiện 残数 — slot KHÔNG có コース thì lấy 残数 của slot",
       USR + "\n- Toggle 残数 = 表示\n- Slot S1 KHÔNG có コース, 定員 = 10, đã có 3 chỗ đặt approve",
       "1. U1 mở trang đặt chỗ\n2. Đọc số 残数 của slot S1\n3. Đối chiếu phép tính tay",
       "定員 10 − use_people 3 = 7",
       "- Slot S1 hiện 残数 = **7**",
       note="Nguồn: Event booking 1.0 r180 + r182. Spec Field Matrix #57."),

    tc("LINE user — chọn slot & plan", "DATA-COUNT-001", "Normal",
       "Hiện 残数 — slot CÓ コース thì KHÔNG hiện 残数 của slot mà hiện 残数 từng コース",
       USR + "\n- Toggle 残数 = 表示\n- Slot S2 定員 = 10, có 2 コース: P1 定員 5 (đã dùng 2), P2 定員 3 (đã dùng 0)",
       "1. U1 mở trang đặt chỗ, chọn slot S2\n2. Quan sát vùng 残数 ở dòng slot\n"
       "3. Đọc 残数 của P1 và P2",
       "P1: 5 − 2 = 3 · P2: 3 − 0 = 3",
       "- Dòng slot S2 **KHÔNG hiện** số 残数 riêng của slot\n"
       "- P1 hiện 残数 = **3** · P2 hiện 残数 = **3**",
       note="Nguồn: Event booking 1.0 r180「slot có plan thì không hiện remain của slot mà hiện remain của từng plan」. "
            "⚠ Corpus ghi nhầm cùng 1 câu 2 lần (「slot không có plan」lặp lại) — đã đọc theo ngữ cảnh."),

    tc("LINE user — chọn slot & plan", "DATA-COUNT-001", "Boundary",
       "残数 — slot/コース không set 定員 hiện dấu -, đã full hiện text 満席",
       USR + "\n- Toggle 残数 = 表示, toggle 満席 = 表示\n"
       "- Slot A: 定員 = trống (無制限) · Slot B: 定員 = 2, đã dùng 2",
       "1. U1 mở trang đặt chỗ\n2. Đọc vùng 残数 của slot A\n3. Đọc vùng 残数 của slot B",
       "Slot A: number_people = NULL · Slot B: full",
       "- Slot A hiện dấu **-**\n- Slot B hiện text **「満席」**, không chọn được",
       note="Nguồn: Event booking 1.0 r181 và r183."),

    tc("LINE user — chọn slot & plan", "DATA-COUNT-001", "Normal",
       "残数 tính cả booking đang ở trạng thái request change / request cancel",
       USR + "\n- Toggle 残数 = 表示\n- Slot S1 定員 = 10; hiện có 2 booking status=1, 1 booking status=6 "
       "(`update_to IS NULL`), 1 booking status=7",
       "1. U1 mở trang đặt chỗ, đọc 残数 của S1\n2. Đối chiếu phép tính tay",
       "10 − (2 + 1 + 1) = 6",
       "- 残数 hiện **6** (các booking request change / request cancel VẪN bị trừ vào 残数)",
       note="Nguồn: Event booking 1.0 r182「check các booking ở trạng thái request change và request cancel "
            "vẫn được tính là đã approve」. Spec BR-05."),

    tc("LINE user — chọn slot & plan", "FUNC-001", "Normal",
       "Toggle 残数 = 非表示 → không hiện 残数 của bất kỳ slot và コース nào",
       USR + "\n- Toggle 残数 = 非表示\n- Event có slot không コース và slot có 2 コース",
       "1. U1 mở trang đặt chỗ\n2. Quan sát tất cả slot và コース",
       "Toggle tắt",
       "- **Không slot nào và không コース nào** hiện số 残数\n- Vẫn chọn và đặt chỗ được bình thường",
       note="Nguồn: Event booking 1.0 r179."),

    tc("LINE user — chọn slot & plan", "UI-FIELD-001", "Normal",
       "Slot còn hạn còn chỗ nhưng コース bên trong hết hạn / hết chỗ → xử lý theo từng コース",
       USR + "\n- Slot S1 còn hạn, còn 残数\n- コース P1 còn hạn còn chỗ · コース P2 đã quá 締切 của plan · "
       "コース P3 đã full\n- Toggle 受付終了 = 表示, toggle 満席 = 表示",
       "1. U1 mở trang đặt chỗ, chọn slot S1\n2. Quan sát 3 コース",
       "P1 OK · P2 hết hạn · P3 full",
       "- P1: chọn được\n- P2: hiện nhưng **disable** (hết hạn)\n- P3: hiện text 満席, **disable**\n"
       "- Slot S1 vẫn hiện và chọn được (vì còn P1)",
       note="Nguồn: Event booking 1.0 r178「Slot vẫn thỏa mãn điều kiện book thì check thêm điều kiện của plan; "
            "plan nào còn hạn còn remain thì cho phép book; plan nào hết hạn hoặc hết remain thì ẩn đi hoặc "
            "disable theo setting chung」."),

    tc("LINE user — chọn slot & plan", "FUNC-DATE-001", "Boundary",
       "Trước / đúng / sau 締切日時 của slot — chặn đặt đúng thời điểm",
       USR + "\n- Slot S1 có 締切日時 = 2026-09-07 18:00, còn chỗ\n- Toggle 受付終了 = 表示",
       "1. Ở mốc 2026-09-07 17:59: U1 mở trang, chọn S1, đặt chỗ\n"
       "2. Ở mốc 2026-09-07 18:00: reload, thử đặt\n3. Ở mốc 2026-09-07 18:01: reload, thử đặt",
       "3 mốc quanh 締切 18:00",
       "- 17:59: đặt chỗ **thành công**\n"
       "- 18:00 và 18:01: slot bị disable (hoặc ẩn theo setting), **không đặt được**\n"
       "- Ghi rõ hành vi tại đúng mốc 18:00 (bao gồm hay loại trừ) làm căn cứ spec",
       note="Nguồn: Event booking 1.0 r184-r185 (setting hiện/ẩn slot hết hạn) + spec BR-13. "
            "Ranh giới tại đúng mốc 締切 KHÔNG được spec nói rõ → xem MT-17."),

    # ══════════════════ 16. LINE user — nhập form & quy chế ══════════════════
    tc("LINE user — nhập form & quy chế", "FUNC-001", "Normal",
       "Chọn số lượng đặt chỗ theo setting 1回の予約上限 và đơn vị hiển thị đúng",
       USR + "\n- Event E:「1回の予約上限」= 3, 予約単位 =「名」\n- Slot S1 còn 残数 10",
       "1. U1 mở trang đặt chỗ, chọn S1\n2. Mở dropdown số lượng\n3. Quan sát đơn vị hiển thị bên cạnh",
       "上限 3, đơn vị「名」",
       "- Dropdown hiện đúng **1, 2, 3**\n- Đơn vị hiển thị là **「名」**, không phải「人」",
       note="Nguồn: Event booking 1.0 r189-r190. TC gốc chỉ có tiêu đề → expected do AI viết theo setting đã test ở tab 詳細設定."),

    tc("LINE user — nhập form & quy chế", "FUNC-004", "Abnormal",
       "Đặt số lượng vượt quá 残数 còn lại → báo lỗi, không tạo booking",
       USR + "\n- Slot S1 定員 = 2, `use_people` = 0, 全承認, không có コース\n"
       "-「1回の予約上限」= 3",
       "1. U1 chọn S1, chọn số lượng = 3 → xác nhận\n2. Quan sát thông báo\n"
       "3. Kiểm tra `b_user_booking` xem có bản ghi mới không\n4. Chọn số lượng = 2 → xác nhận",
       "定員 2; thử đặt 3 rồi 2",
       "- Số lượng 3: **báo lỗi**, không cho đặt, KHÔNG tạo bản ghi `b_user_booking`\n"
       "- Số lượng 2: đặt thành công, `use_people` = 2",
       note="Nguồn: Event booking 1.0 r191「Báo lỗi không cho book」+ SpecChange #26808 r6-r8. "
            "⚠ Corpus phân biệt「báo lỗi」và「không cho chọn」— text lỗi cụ thể chưa có ở corpus lẫn spec (MT-18)."),

    tc("LINE user — nhập form & quy chế", "FUNC-002", "Abnormal",
       "Bật checkbox đồng ý quy chế nhưng KHÔNG tick → chặn đặt chỗ",
       USR + "\n- Event E bật hiển thị 利用規約 + bật checkbox đồng ý",
       "1. U1 điền đủ form, KHÔNG tick「利用規約に同意」→ bấm xác nhận\n2. Quan sát thông báo\n"
       "3. Tick checkbox → bấm xác nhận",
       "Chưa tick / đã tick",
       "- Chưa tick: hiện message「利用規約に同意をしてください」, chặn đặt\n- Đã tick: đặt được bình thường",
       note="Nguồn: spec Field Matrix #58 (⚠ validate CLIENT — không lưu DB). Corpus Event booking 1.0 r255-r256 "
            "chỉ có tiêu đề. → Nên chạy kèm TC gọi thẳng API bỏ qua checkbox (TD-11)."),

    tc("LINE user — nhập form & quy chế", "UI-003", "Normal",
       "Màn xác nhận hiện đủ dữ liệu đã chọn trước khi đặt",
       USR + "\n- Slot S1 10:00〜12:00 ngày 2026-09-01, コース P1 5000円\n- Form có 3 item",
       "1. U1 chọn slot + コース + số lượng 2 + điền 3 item\n2. Bấm tiếp tới màn xác nhận\n"
       "3. Đối chiếu từng thông tin trên màn xác nhận với dữ liệu đã chọn",
       "1 slot + 1 コース + 2 chỗ + 3 đáp án form",
       "- Màn xác nhận hiện đủ: ngày 2026-09-01 · giờ 10:00〜12:00 · コース P1 · số lượng 2 · "
       "3 cặp câu hỏi-đáp án · số tiền 10.000円\n- Không thiếu / sai giá trị nào",
       note="Nguồn: Event booking 1.0 r258「Check các data đã chọn」(TC gốc chỉ có tiêu đề) → expected do AI viết."),

    tc("LINE user — nhập form & quy chế", "OUT-TRUTH-001", "Normal",
       "Slot リクエスト制 → màn xác nhận hiện thêm cảnh báo chưa chắc chắn được đặt",
       USR + "\n- Slot S2 承認方法 = リクエスト制",
       "1. U1 chọn slot S2, điền form, tới màn xác nhận\n2. Quan sát phần text phía dưới",
       "S2 リクエスト制",
       "- Màn xác nhận hiện thêm text:\n「この予約はリクエスト制となります」\n"
       "「申し込みをしても予約が確定するわけではありません」",
       note="Nguồn: Event booking 1.0 r259. ⚠ RULE-01: quan điểm `OUT-TRUTH-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    # ══════════════════ 17. LINE user — đặt chỗ & giới hạn số lần ══════════════════
    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-001", "Normal",
       "Đặt chỗ không bill tiền → tạo booking, gửi action, hiện ở màn quản lý phía admin",
       SLOT_OK + "\n- Event KHÔNG bật 決済\n- Slot S1 đã set action「予約完了」",
       "1. U1 đặt 1 chỗ ở S1, xác nhận\n2. Mở LINE app đọc tin nhận được\n"
       "3. Query `b_user_booking`\n4. Mở màn 参加者リスト phía admin",
       "1 chỗ, không bill tiền",
       "- Booking success: `b_user_booking` có 1 bản ghi, `status` = 5, `status_payment` = 0\n"
       "- LINE user nhận đúng tin action「予約完了」\n"
       "- Màn 参加者リスト phía admin hiện booking này",
       note="Nguồn: Event booking 1.0 r260「booking success và gửi action cho user」+ r163. RULE-07 (3 tầng)."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-001", "Normal",
       "Điều kiện duyệt lấy theo setting của slot khi slot KHÔNG có コース",
       USR + "\n- Slot S1 KHÔNG có コース, 承認方法 = リクエスト制",
       "1. U1 đặt 1 chỗ ở S1\n2. Query `b_user_booking.status`",
       "Slot リクエスト制, không có コース",
       "- `status` = **3** (承認待ち) — lấy theo setting của SLOT",
       note="Nguồn: Event booking 1.0 r270「case slot không có plan → lấy theo setting của slot」."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-001", "Normal",
       "Điều kiện duyệt lấy theo setting của コース khi slot CÓ コース (ghi đè setting slot)",
       USR + "\n- Slot S2 承認方法 = 全承認\n- コース P1 thuộc S2 có 承認方法 = リクエスト制",
       "1. U1 đặt 1 chỗ chọn コース P1\n2. Query `b_user_booking.status`",
       "Slot 全承認 vs plan リクエスト制",
       "- `status` = **3** (承認待ち) — lấy theo setting của **コース**, không theo slot",
       note="Nguồn: Event booking 1.0 r271「case slot có plan → lấy theo setting của plan」. "
            "Spec BR-18 (`b_plan_slot.approval_system_booking`)."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Slot KHÔNG コース, 定員 = 2 — ma trận số lượng đặt tại các mức đã dùng khác nhau",
       USR + "\n- Slot S1 KHÔNG có コース, 定員 = 2, 承認方法 = 全承認",
       "1. Khi chưa có booking nào: đặt số lượng 1 → ghi kết quả\n"
       "2. Reset dữ liệu; đặt số lượng 2 → ghi kết quả\n3. Reset; đặt số lượng 3 → ghi kết quả\n"
       "4. Reset về trạng thái đã có 1 booking approve: đặt 1 → 2 → 3, ghi từng kết quả\n"
       "5. Khi đã có 2 booking approve: mở trang đặt chỗ, quan sát slot S1",
       "定員 = 2; các mức đã dùng 0 / 1 / 2 × số lượng chọn 1 / 2 / 3",
       "- Đã dùng 0: chọn 1 → **thành công**; chọn 2 → **thành công**; chọn 3 → **báo lỗi**\n"
       "- Đã dùng 1: chọn 1 → **thành công**; chọn 2 → **báo lỗi**; chọn 3 → **báo lỗi**\n"
       "- Đã dùng 2: slot **không chọn được nữa** (khác với báo lỗi)",
       note="Nguồn: SpecChange #26808 r6-r12 (14/10/2024). ⚠ Ma trận này phân biệt rõ 2 kết quả khác nhau: "
            "「báo lỗi」(chọn được nhưng submit lỗi) vs「không cho chọn」(bị chặn từ UI) — xem MT-18."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Slot 無制限 + 3 コース mỗi コース 定員 1 → mỗi コース đặt tối đa 1, slot hiện dấu -",
       USR + "\n- Slot S 定員 = trống (無制限)\n- 3 コース P1/P2/P3, mỗi コース 定員 = 1, không dùng chung 定員 slot\n"
       "- Toggle 残数 = 表示",
       "1. U1 mở trang đặt chỗ, đọc 残数 của slot và của 3 コース\n"
       "2. Đặt 1 chỗ P1 → thử đặt tiếp P1\n3. Đặt 1 chỗ P2 → đặt 1 chỗ P3",
       "slot NULL; P1/P2/P3 limit = 1",
       "- 残数 slot hiện dấu **-**; 残数 mỗi コース = **1**\n"
       "- Mỗi コース đặt tối đa **1 booking**; sau khi đầy thì コース đó không đặt được nữa\n"
       "- P1 đầy KHÔNG ảnh hưởng P2, P3",
       note="Nguồn: SpecChange #26808 r13-r14."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Slot 無制限 + コース dùng chung 定員 slot → コース đó cũng 無制限",
       USR + "\n- Slot S 定員 = trống (無制限)\n"
       "- P1 定員 = 1 · P2 定員 = 1 · P3 tick「予約枠の定員の残数に合わせる」\n- Toggle 残数 = 表示",
       "1. Đọc 残数 của slot, P1, P2, P3\n2. Đặt liên tiếp 3 lần vào P3\n3. Thử đặt lần 4 vào P3",
       "P3 dùng chung 定員 slot (slot NULL)",
       "- 残数: slot = **-**, P1 = 1, P2 = 1, **P3 = -**\n"
       "- P3 đặt được **không giới hạn** số lần (3 lần đều thành công, lần 4 vẫn được)\n"
       "- P1, P2 vẫn tối đa 1",
       note="Nguồn: SpecChange #26808 r15-r16."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 1, max P1 = 1, max P2 = 1 → tổng slot chặn trước, hết chỗ ở mọi コース",
       USR + "\n- Slot S 定員 = 1; P1 定員 = 1, P2 定員 = 1 (đều không dùng chung 定員 slot)",
       "1. Khi chưa có booking: đặt P1 → ghi kết quả; reset, đặt P2 → ghi kết quả\n"
       "2. Khi đã có 1 booking ở P1: thử chọn P1 → ghi; thử chọn P2 → ghi\n"
       "3. Khi đã có 1 booking ở P2: thử chọn P1 → ghi; thử chọn P2 → ghi",
       "slot 1 / P1 1 / P2 1",
       "- Chưa có booking: chọn P1 **thành công**; chọn P2 **thành công**\n"
       "- Đã có booking P1: chọn P1 → **không cho chọn**; chọn P2 → **báo lỗi**\n"
       "- Đã có booking P2: chọn P1 → **báo lỗi**; chọn P2 → **không cho chọn**",
       note="Nguồn: SpecChange #26808 r17-r22. Đây là điểm mấu chốt của SpecChange: 定員 slot là trần tổng, "
            "コース chỉ là trần con."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 2, max P1 = 2, max P2 = 1 → ma trận 6 tổ hợp trạng thái đã đặt",
       USR + "\n- Slot S 定員 = 2; P1 定員 = 2, P2 定員 = 1",
       "1. Với từng trạng thái đã đặt dưới đây, thử chọn P1 rồi P2 và ghi kết quả\n"
       "2. Reset dữ liệu giữa các trạng thái",
       "Trạng thái: (a) chưa có booking · (b) 1 booking P1 · (c) 1 booking P2 · "
       "(d) 2 booking P1 · (e) 1 booking P1 + 1 booking P2",
       "- (a) P1 **thành công**, P2 **thành công**\n- (b) P1 **thành công**, P2 **thành công**\n"
       "- (c) P1 **thành công**, P2 **không cho chọn**\n- (d) P1 **không cho chọn**, P2 **báo lỗi**\n"
       "- (e) P1 **báo lỗi**, P2 **không cho chọn**",
       note="Nguồn: SpecChange #26808 r25-r34."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 3 > tổng max コース (1+1) → コース chặn trước khi slot đầy",
       USR + "\n- Slot S 定員 = 3; P1 定員 = 1, P2 定員 = 1",
       "1. Với từng trạng thái, thử chọn P1 rồi P2 và ghi kết quả",
       "Trạng thái: (a) chưa có booking · (b) 1 booking P1 · (c) 1 booking P2 · "
       "(d) 1 booking P1 + 1 booking P2",
       "- (a) P1 **thành công**, P2 **thành công**\n- (b) P1 **không cho chọn**, P2 **thành công**\n"
       "- (c) P1 **thành công**, P2 **không cho chọn**\n- (d) P1 **không cho chọn**, P2 **không cho chọn**\n"
       "- Dù slot còn 1 chỗ trống, không コース nào đặt thêm được",
       note="Nguồn: SpecChange #26808 r35-r42."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 3, P1 = 1, P2 dùng chung 定員 slot → P2 hấp thụ phần còn lại của slot",
       USR + "\n- Slot S 定員 = 3; P1 定員 = 1; P2 tick「予約枠の定員の残数に合わせる」",
       "1. Với từng trạng thái, thử chọn P1 rồi P2 và ghi kết quả",
       "Trạng thái: (a) chưa có booking · (b) 1 P1 · (c) 1 P2 · (d) 1 P1 + 1 P2 · (e) 2 P2 · "
       "(f) 1 P1 + 2 P2 · (g) 3 P2",
       "- (a) P1 **thành công**, P2 **thành công**\n- (b) P1 **không cho chọn**, P2 **thành công**\n"
       "- (c) P1 **thành công**, P2 **thành công**\n- (d) P1 **không cho chọn**, P2 **thành công**\n"
       "- (e) P1 **thành công**, P2 **thành công**\n- (f) P1 **không cho chọn**, P2 **không cho chọn**\n"
       "- (g) P1 **báo lỗi**, P2 **không cho chọn**",
       note="Nguồn: SpecChange #26808 r43-r56. ⚠ Case (g): P1 hiện **báo lỗi** chứ không phải「không cho chọn」— "
            "khác biệt tinh vi, giữ nguyên theo corpus."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 1 nhưng max コース = 2 → chọn số lượng 2 bị báo lỗi",
       USR + "\n- Slot S 定員 = 1; P1 定員 = 2\n-「1回の予約上限」cho phép chọn tới 2",
       "1. U1 chọn コース P1, chọn số lượng = 2 → xác nhận\n2. Quan sát kết quả",
       "slot 1 < plan 2, đặt 2 chỗ",
       "- **Báo lỗi**, không đặt được (trần của slot thắng trần của コース)",
       note="Nguồn: SpecChange #26808 r57."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-004", "Boundary",
       "Max slot = 1, P1 = 2, P2 = 1, P3 dùng chung slot → sau 1 booking bất kỳ, mọi コース đều bị chặn",
       USR + "\n- Slot S 定員 = 1; P1 定員 = 2; P2 定員 = 1; P3 tick dùng chung 定員 slot",
       "1. Chưa có booking: thử chọn lần lượt P1, P2, P3 và ghi kết quả\n"
       "2. Khi đã có 1 booking ở P1: thử chọn P1, P2, P3\n"
       "3. Khi đã có 1 booking ở P2: thử chọn P1, P2, P3\n"
       "4. Khi đã có 1 booking ở P3: thử chọn P1, P2, P3",
       "slot 1 · P1 2 · P2 1 · P3 dùng chung",
       "- Chưa có booking: cả 3 コース đều **thành công**\n"
       "- Có 1 booking P1: P1 **báo lỗi**, P2 **báo lỗi**, P3 **không cho chọn**\n"
       "- Có 1 booking P2: P1 **báo lỗi**, P2 **không cho chọn**, P3 **không cho chọn**\n"
       "- Có 1 booking P3: P1 **báo lỗi**, P2 **báo lỗi**, P3 **không cho chọn**",
       note="Nguồn: SpecChange #26808 r58-r69. Ma trận đầy đủ nhất của SpecChange — giữ nguyên phân biệt "
            "「báo lỗi」/「không cho chọn」theo corpus."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "FUNC-001", "Normal",
       "Setting ẩn slot/コース đã full — ẩn theo đúng cấp bị full",
       USR + "\n- Toggle 満席 = 非表示\n- Slot S1: chưa full, có P1 chưa full và P2 đã full\n"
       "- Slot S2: đã full, có P3 chưa full",
       "1. U1 mở trang đặt chỗ\n2. Quan sát slot S1 và các コース bên trong\n3. Tìm slot S2",
       "S1 chưa full (P2 full) · S2 full",
       "- S1 **hiện**, bên trong chỉ hiện P1 (P2 bị ẩn)\n"
       "- S2 **bị ẩn hoàn toàn**, P3 cũng không hiện",
       note="Nguồn: SpecChange #26808 r70-r73."),

    tc("LINE user — đặt chỗ & giới hạn số lần", "CONC-001", "Abnormal",
       "2 LINE user đặt cùng lúc khi còn đúng 1 chỗ → chỉ 1 người đặt được",
       USR + "\n- Slot S1 定員 = 2, `use_people` = 1 (còn đúng 1 chỗ), 全承認\n"
       "- 2 tài khoản LINE U1 và U2 cùng mở màn xác nhận",
       "1. U1 và U2 cùng bấm xác nhận đặt chỗ gần như đồng thời\n"
       "2. Query `b_user_booking` đếm booking của S1\n3. Đọc `b_slot.use_people`\n"
       "4. Quan sát thông báo phía người thất bại",
       "2 user, còn 1 chỗ",
       "- Chỉ **1** booking mới được tạo (tổng 2 booking ở S1)\n"
       "- `use_people` = **2**, KHÔNG vượt 定員\n"
       "- Người còn lại nhận thông báo lỗi rõ ràng (hết chỗ), không bị treo màn hình",
       note="Nguồn: Task nhỏ + fix bug KH r72-r73「check case 2 friend book cùng lúc: chưa bị limit cả 2 đều "
            "book success / số remain =1 => chỉ có 1 friend book được」. ⚠ Spec TD-01 (không transaction) → "
            "đây là điểm rủi ro cao, evidence bắt buộc gồm query DB sau test."),

    # ══════════════════ 18. LINE user — đổi lịch ══════════════════
    tc("LINE user — đổi lịch", "UI-003", "Abnormal",
       "Slot set 予約変更 = 不可 hoặc đã quá hạn đổi → màn detail KHÔNG hiện nút đổi lịch",
       USR + "\n- Booking B1 của U1 ở slot có 予約変更 = 不可\n"
       "- Booking B2 của U1 ở slot cho phép đổi nhưng đã quá 変更受付期限",
       "1. U1 mở màn lịch sử đặt chỗ → mở detail B1\n2. Quan sát vùng nút thao tác\n"
       "3. Mở detail B2 → quan sát",
       "B1: 不可 · B2: quá hạn",
       "- Cả B1 và B2: **KHÔNG hiện nút đổi lịch**\n"
       "- Không có đường vào màn đổi lịch bằng thao tác thường",
       note="Nguồn: Event booking 1.0 r297. Spec BR-14."),

    tc("LINE user — đổi lịch", "FUNC-001", "Normal",
       "Booking đang 承認待ち (status 3) → user đổi lịch được cập nhật NGAY, gửi action chờ duyệt",
       USR + "\n- Booking B của U1 đang `status = 3` ở slot リクエスト制\n"
       "- Slot đích cho phép đổi",
       "1. U1 mở detail B → bấm đổi lịch\n2. Chọn slot khác → xác nhận\n"
       "3. Query `b_user_booking` của U1\n4. Đọc tin nhận được trên LINE",
       "Booking status = 3 khi đổi",
       "- Booking được **update ngay** (không tạo cặp 2 bản ghi)\n"
       "- Gửi action「booking mới đợi approve」\n- Chỉ có 1 bản ghi booking của U1 ở event này",
       note="Nguồn: Event booking 1.0 r298「Được update change luôn -> gửi action của booking mới đợi approve」."),

    tc("LINE user — đổi lịch", "FUNC-001", "Normal",
       "Slot cho phép đổi 全承認 → đổi lịch cập nhật ngay, gửi action change được duyệt ngay",
       USR + "\n- Booking B của U1 `status = 5` ở slot A\n- Slot A và slot B đều 予約変更 = 全承認",
       "1. U1 đổi lịch từ slot A sang slot B\n2. Query `b_user_booking` của U1\n"
       "3. Đọc `b_slot.use_people` của A và B\n4. Đọc tin nhận được trên LINE",
       "A → B, 全承認",
       "- Booking cập nhật ngay: `slot_id` = B, `status` giữ nguyên (1 hoặc 5)\n"
       "- `use_people` của A **giảm 1**, của B **tăng 1**\n"
       "- LINE user nhận action「change booking được approve luôn」",
       note="Nguồn: Event booking 1.0 r299 + Task nhỏ r74. Spec BR-16."),

    tc("LINE user — đổi lịch", "DATA-ID-001", "Normal",
       "Slot cho phép đổi リクエスト制 → tạo CẶP 2 booking status = 6 liên kết bằng update_to",
       USR + "\n- Booking gốc B_old (id = X) của U1 ở slot A, `status = 1`\n"
       "- Slot A có 予約変更 = リクエスト制",
       "1. U1 đổi lịch sang slot B → xác nhận\n"
       "2. Query `b_user_booking` lọc theo line_user U1 và event E\n"
       "3. Đọc `status` và `update_to` của cả 2 bản ghi",
       "Booking gốc id = X",
       "- Có **đúng 2 bản ghi**: B_old (id = X) và B_new\n"
       "- `status` của **cả 2** = **6**\n- `B_new.update_to` = **X** (id của booking gốc)\n"
       "- `B_old.update_to` = NULL",
       note="Nguồn: Event booking 1.0 r300「tạo thêm 1 bản ghi lưu thông tin booking mới → status của 2 booking =6, "
            "booking mới thêm trường update_to lưu booking_id cũ」. Spec BR-16."),

    tc("LINE user — đổi lịch", "FUNC-001", "Normal",
       "Đổi lịch A → B: quy tắc CHO PHÉP đổi lấy theo setting của slot NGUỒN (A)",
       USR + "\n- Chuẩn bị 4 tổ hợp slot: A cho phép đổi / A không cho phép đổi × B cho phép / B không cho phép\n"
       "- U1 có booking ở slot A trong từng tổ hợp",
       "1. Với từng tổ hợp, U1 mở detail booking → thử đổi sang slot B\n2. Ghi lại kết quả",
       "4 tổ hợp: (A cho, B cho) · (A cho, B không) · (A không, B cho) · (A không, B không)",
       "- (A cho, B cho): **đổi được**\n- (A cho, B không): **đổi được**\n"
       "- (A không, B cho): **KHÔNG đổi được**\n- (A không, B không): **KHÔNG đổi được**\n"
       "→ Quy tắc: chỉ setting của slot **NGUỒN (A)** quyết định có cho đổi hay không",
       note="Nguồn: Event booking 2.0 r51-r54 (SpecChange 05/2023). Đây là điểm phản trực giác quan trọng — "
            "spec KHÔNG mô tả rõ nhánh này, xem MT-11."),

    tc("LINE user — đổi lịch", "MSG-004", "Normal",
       "Sau khi đổi lịch, ACTION gửi cho user lấy theo slot ĐÍCH (B)",
       USR + "\n- Slot A set action change A-change; slot B set action change B-change\n"
       "- U1 có booking ở A; A cho phép đổi 全承認",
       "1. U1 đổi lịch A → B\n2. Mở LINE app đọc tin nhận được\n"
       "3. Lặp lại với A set リクエスト制: đổi → đọc tin của bước request",
       "A-change vs B-change",
       "- Trường hợp 全承認: nhận **B-change** (action「change được approve luôn」của slot B)\n"
       "- Trường hợp リクエスト制: nhận action「change đợi approve」**của slot B**",
       note="Nguồn: Event booking 2.0 r55-r56「Gửi action của B」. Kết hợp với TC bug tự detect ở nhóm "
            "アクション設定 (case B có コース) — xem MT-02."),

    tc("LINE user — đổi lịch", "MSG-004", "Normal",
       "Tin nhắn sau khi đổi lịch replace ĐÚNG 5 dữ liệu theo booking MỚI (Bug #32366)",
       USR + "\n- Booking gốc: slot 2026-09-01 10:00, コース P1 5000円, 1 chỗ\n"
       "- Slot đích: 2026-09-08 14:00, コース P2 8000円\n"
       "- Action change có chèn đủ 5 biến: tên event / ngày / giờ / số lượng / số tiền",
       "1. U1 đổi lịch sang slot đích, đổi số lượng thành 2\n2. Mở LINE app đọc tin nhận được\n"
       "3. Đối chiếu 5 giá trị với booking MỚI",
       "Booking mới: 2026-09-08 · 14:00 · 2 chỗ · 16.000円 (8000 × 2)",
       "- Tin nhắn hiện: ngày **2026-09-08**, giờ **14:00**, số lượng **2**, số tiền **16.000円**\n"
       "- **KHÔNG có trường nào bị để trống** và không lấy nhầm dữ liệu booking gốc",
       note="Nguồn: Event booking 2.0 r61-r64 (Bug #32366, 10/2025)：「Khi duyệt yêu cầu thay đổi và gửi tin nhắn, "
            "ngày giờ tổ chức bị để trống」— nguyên nhân: approve/deny xóa 1 booking nên mất data khi replace."),

    tc("LINE user — đổi lịch", "DATA-COUNT-001", "Normal",
       "Đổi lịch 全承認 có コース → cập nhật đủ 4 bộ đếm (slot cũ/mới, plan cũ/mới)",
       USR + "\n- Booking của U1 ở slot A / コース P1 (`use_people` A = 1, `remain_limit` P1 = 1)\n"
       "- Slot B / コース P2 (`use_people` B = 0, `remain_limit` P2 = 0)\n- A cho phép đổi 全承認",
       "1. Ghi lại 4 bộ đếm trước khi đổi\n2. U1 đổi lịch A/P1 → B/P2\n3. Đọc lại 4 bộ đếm",
       "Trước: A=1, P1=1, B=0, P2=0",
       "- Sau: A `use_people` = **0** · P1 `remain_limit` = **0** · B `use_people` = **1** · "
       "P2 `remain_limit` = **1**",
       note="Nguồn: Task nhỏ + fix bug KH r76 + Event booking 2.0 r40-r41. Spec BR-08. "
            "⚠ TD-17: `saveAdminBooking` increment vs `saveActionBooking` recompute → nguy cơ drift."),

    tc("LINE user — đổi lịch", "DATA-COUNT-001", "Normal",
       "Đổi lịch リクエスト制 → CHƯA cập nhật bộ đếm cho tới khi admin duyệt",
       USR + "\n- Booking của U1 ở slot A / コース P1; A có 予約変更 = リクエスト制\n"
       "- Slot B / コース P2 rỗng",
       "1. Ghi lại 4 bộ đếm\n2. U1 gửi request đổi lịch A/P1 → B/P2\n3. Đọc lại 4 bộ đếm\n"
       "4. Admin duyệt request change\n5. Đọc lại 4 bộ đếm",
       "Trước: A=1, P1=1, B=0, P2=0",
       "- Ngay sau request: **4 bộ đếm KHÔNG đổi** (A=1, P1=1, B=0, P2=0)\n"
       "- Sau khi admin duyệt: A=0, P1=0, B=1, P2=1",
       note="Nguồn: Task nhỏ r77, r79 + Event booking 2.0 r42-r44, r46."),

    tc("LINE user — đổi lịch", "DATA-COUNT-001", "Normal",
       "Đổi CHỈ số lượng (không đổi slot/plan) → cập nhật lại bộ đếm; đổi CHỈ friend info → không đổi bộ đếm",
       USR + "\n- Booking của U1 ở slot A / コース P1, số lượng = 1\n- A cho phép đổi 全承認",
       "1. Ghi lại `use_people` A và `remain_limit` P1\n"
       "2. U1 đổi số lượng 1 → 3, không đổi slot/コース → xác nhận → đọc lại 2 bộ đếm\n"
       "3. U1 đổi CHỈ giá trị friend info (không đổi số lượng/slot/コース) → đọc lại 2 bộ đếm",
       "Số lượng 1 → 3; sau đó chỉ đổi friend info",
       "- Sau đổi số lượng: `use_people` A = **3**, `remain_limit` P1 = **3**\n"
       "- Sau khi chỉ đổi friend info: 2 bộ đếm **giữ nguyên = 3**",
       note="Nguồn: Task nhỏ r78, r80-r81 + Event booking 1.0 r303-r306."),

    tc("LINE user — đổi lịch", "STATE-DEP-001", "Normal",
       "Đổi chỉ số lượng / friend info → status và action lấy theo slot & コース ĐANG chọn",
       USR + "\n- Booking của U1 ở slot A / コース P1 (P1 có 承認方法 = リクエスト制 và action riêng)",
       "1. U1 đổi chỉ số lượng (giữ nguyên slot A / コース P1)\n2. Query `status` của booking\n"
       "3. Đọc tin nhận được trên LINE",
       "Không đổi slot/plan, chỉ đổi số lượng",
       "- `status` theo setting của **コース P1 đang chọn** (リクエスト制 → tạo request)\n"
       "- Action gửi cũng là action của コース P1",
       note="Nguồn: Event booking 2.0 r59「status và action theo slot và plan đang chọn」."),

    # ══════════════════ 19. LINE user — hủy ══════════════════
    tc("LINE user — hủy", "UI-003", "Abnormal",
       "Slot set 予約キャンセル = 不可 hoặc quá hạn hủy → màn detail KHÔNG hiện nút hủy",
       USR + "\n- Booking B1 ở slot có キャンセル = 不可\n- Booking B2 ở slot cho hủy nhưng quá キャンセル受付期限",
       "1. U1 mở detail B1 → quan sát nút thao tác\n2. Mở detail B2 → quan sát",
       "B1: 不可 · B2: quá hạn",
       "- Cả B1 và B2: **KHÔNG hiện nút hủy**",
       note="Nguồn: Event booking 1.0 r312. Spec BR-14."),

    tc("LINE user — hủy", "FUNC-001", "Normal",
       "Booking đang 承認待ち → user hủy được ngay, status = 4, gửi action hủy được duyệt ngay",
       USR + "\n- Booking B của U1 `status = 3`, slot cho phép hủy",
       "1. U1 mở detail B → bấm hủy → xác nhận\n2. Query `b_user_booking.status`\n"
       "3. Đọc tin nhận được trên LINE\n4. Đọc `b_slot.use_people`",
       "Booking status = 3 khi hủy",
       "- `status` = **4** (キャンセル)\n- Nhận action「cancel được approve luôn」\n"
       "- `use_people` **KHÔNG đổi** (vì status 3 trước đó chưa được cộng)",
       note="Nguồn: Event booking 1.0 r313 + Task nhỏ r83."),

    tc("LINE user — hủy", "FUNC-001", "Normal",
       "Slot キャンセル = 全承認 → hủy ngay, status = 4, trừ bộ đếm, xóa remind",
       USR + "\n- Booking B của U1 `status = 5` ở slot có キャンセル = 全承認, slot có bật remind\n"
       "- `use_people` = 1, `user_event` có 1 bản ghi remind cho U1",
       "1. U1 hủy booking B\n2. Query `status`\n3. Đọc `use_people` và `remain_limit`\n"
       "4. Query bảng `user_event` của U1\n5. Đọc tin nhận được trên LINE",
       "1 booking, 1 remind",
       "- `status` = **4**\n- `use_people` giảm **-1**, `remain_limit` giảm **-1**\n"
       "- Bản ghi `user_event` remind **bị xóa**\n- Nhận action「cancel được approve luôn」",
       note="Nguồn: Event booking 1.0 r314 + r291 + Task nhỏ r46, r82. RULE-07 (3 tầng)."),

    tc("LINE user — hủy", "FUNC-001", "Normal",
       "Slot キャンセル = リクエスト制 → status = 7, CHƯA trừ bộ đếm, CHƯA xóa remind",
       USR + "\n- Booking B của U1 `status = 5` ở slot có キャンセル = リクエスト制, slot bật remind\n"
       "- `use_people` = 1, có 1 bản ghi `user_event`",
       "1. U1 bấm hủy booking B\n2. Query `status`\n3. Đọc `use_people`\n"
       "4. Query `user_event` của U1\n5. Đọc tin nhận được trên LINE",
       "Hủy dạng request",
       "- `status` = **7** (キャンセルリクエスト)\n- `use_people` **vẫn = 1** (chưa trừ)\n"
       "- Bản ghi `user_event` **vẫn còn**\n- Nhận action「cancel đợi approve」",
       note="Nguồn: Event booking 1.0 r315 + Task nhỏ r47, r83."),

    tc("LINE user — hủy", "STATE-DEP-001", "Normal",
       "Admin từ chối request hủy → status quay về 1, remind KHÔNG bị xóa",
       USR + "\n- Booking B của U1 đang `status = 7`, slot bật remind, `user_event` còn nguyên",
       "1. Admin mở detail booking B → bấm từ chối request cancel\n2. Query `status`\n"
       "3. Query `user_event` của U1\n4. Đọc tin U1 nhận được trên LINE",
       "Request cancel bị từ chối",
       "- `status` = **1** (承認)\n- Bản ghi `user_event` remind **vẫn còn** (U1 vẫn nhận remind)\n"
       "- U1 nhận action「admin từ chối cancel」",
       note="Nguồn: Event booking 1.0 r317 + r294 + Task nhỏ r60."),

    # ══════════════════ 20. LINE user — lịch sử booking ══════════════════
    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Normal",
       "Màn lịch sử — booking KHÔNG bill tiền luôn hiển thị đủ ở mọi status",
       USR + "\n- Event không bật 決済\n- U1 có booking ở các trạng thái: status 3 (`status_webhook` = 1), "
       "status 3 (`status_webhook` = NULL, booking cũ), status 5 (`status_webhook` = 1), "
       "status 5 (`status_webhook` = NULL)",
       "1. U1 mở màn lịch sử đặt chỗ\n2. Đếm số booking hiển thị\n3. Đối chiếu với danh sách đã chuẩn bị",
       "4 booking không bill tiền",
       "- **Cả 4 booking đều hiện** ở màn lịch sử",
       note="Nguồn: Improve bill tiền univapay r114-r117."),

    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Abnormal",
       "Màn lịch sử ẨN booking đang CHỜ THANH TOÁN (status_webhook 0 / 3 / 4)",
       USR + "\n- Event bật 決済\n- U1 có 3 booking `status = 5`, `status_payment = 0` với "
       "`status_webhook` lần lượt = 3 (bill kiểu cũ), 0 (bill kiểu mới), 4 (bill kiểu mới)",
       "1. U1 mở màn lịch sử đặt chỗ\n2. Tìm 3 booking trên",
       "3 booking đang chờ kết quả thanh toán",
       "- **Cả 3 booking đều KHÔNG hiện** ở màn lịch sử\n"
       "- Không hiện dòng trống / dòng lỗi thay thế",
       note="Nguồn: Improve bill tiền univapay r119-r121 (4/2025). Đây là spec quan trọng: user không thấy "
            "booking chưa xác nhận thanh toán, tránh hiểu nhầm đã đặt xong."),

    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Normal",
       "Màn lịch sử HIỆN booking đã thanh toán thành công",
       USR + "\n- U1 có booking `status = 5`, `status_payment = 1`, `status_webhook` = 1 và 1 booking "
       "`status_payment = 1`, `status_webhook` = NULL (booking cũ)",
       "1. U1 mở màn lịch sử đặt chỗ\n2. Tìm 2 booking trên",
       "2 booking đã thanh toán",
       "- **Cả 2 booking đều hiện** ở màn lịch sử với thông tin thanh toán đúng",
       note="Nguồn: Improve bill tiền univapay r122-r123."),

    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Normal",
       "Booking thanh toán FAIL → đã bị xóa nên không còn hiện ở lịch sử",
       USR + "\n- U1 vừa đặt 1 chỗ có bill tiền nhưng thẻ bị từ chối",
       "1. Sau khi bill fail, U1 mở màn lịch sử\n2. Tìm booking vừa thất bại\n"
       "3. Query `b_user_booking` theo line_user U1",
       "Bill fail bằng thẻ 4000 0000 0000 0341",
       "- Booking **không hiện** ở màn lịch sử\n- Bản ghi đã bị xóa khỏi `b_user_booking`\n"
       "- `use_people` / `remain_limit` đã được hoàn lại đúng",
       note="Nguồn: Improve bill tiền univapay r124 + Improve bill tiền stripe r11."),

    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Normal",
       "Màn lịch sử hiện đủ booking ở các trạng thái 1 / 2 / 4 / 6 / 7 và booking do admin đặt hộ",
       USR + "\n- U1 có 6 booking: admin đặt hộ (status 5, `status_webhook` NULL) · status 1 · status 2 (deny) · "
       "status 4 (cancel) · status 6 (request change) · status 7 (request cancel)",
       "1. U1 mở màn lịch sử đặt chỗ\n2. Đếm và đối chiếu từng booking",
       "6 booking ở 6 trạng thái khác nhau",
       "- **Cả 6 booking đều hiện**\n- Mỗi booking hiện đúng badge trạng thái tương ứng",
       note="Nguồn: Improve bill tiền univapay r125-r131."),

    tc("LINE user — lịch sử booking", "OUT-TRUTH-001", "Normal",
       "Booking đang trong luồng ĐỔI có thanh toán (status_webhook 5/6/7) VẪN hiện ở lịch sử",
       USR + "\n- U1 có 3 booking đang đổi lịch với `status_webhook` = 6, 5, 7 và 1 booking bill fail "
       "(`status_webhook` = 2)",
       "1. U1 mở màn lịch sử đặt chỗ\n2. Tìm 4 booking trên",
       "status_webhook 6 / 5 / 7 / 2",
       "- **Cả 4 booking đều hiện** ở màn lịch sử\n"
       "- Khác với booking MỚI đang chờ thanh toán (bị ẩn) — booking ĐANG ĐỔI vẫn hiện vì bản gốc đã hợp lệ",
       note="Nguồn: Improve bill tiền univapay r132-r136. ⚠ Đây là khác biệt tinh vi so với TC ẩn booking mới "
            "chờ thanh toán — đọc kỹ để không gộp nhầm."),

    tc("LINE user — lịch sử booking", "FUNC-001", "Normal",
       "Từ màn lịch sử mở detail booking → hiện đủ thông tin và đúng nút thao tác khả dụng",
       USR + "\n- U1 có 1 booking `status = 1` ở slot cho phép đổi và hủy",
       "1. U1 mở màn lịch sử → bấm vào booking\n2. Đối chiếu thông tin hiển thị với dữ liệu đã đặt\n"
       "3. Quan sát các nút thao tác",
       "1 booking: 2026-09-01 10:00, コース P1, 2 chỗ, đáp án 3 item form",
       "- Detail hiện đủ: ngày / giờ / コース / số lượng / số tiền / 3 đáp án form\n"
       "- Có nút đổi lịch và nút hủy (vì slot cho phép cả 2)",
       note="Nguồn: Event booking 1.0 r297/r312 (suy từ ngữ cảnh nút đổi/hủy ở màn detail). "
            "TC gốc không mô tả nội dung detail → expected do AI viết, cần Leader xác nhận."),
]
