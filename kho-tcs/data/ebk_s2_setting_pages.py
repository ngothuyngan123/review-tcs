# -*- coding: utf-8 -*-
"""FA-021 イベント予約 — Nhóm 7-13: アクション設定 · 各種ページ · form nhập · 詳細設定 · 決済設定 ·
copy/xóa event · preview & OGP.

Nguồn chính: 11.3 TCsLine_EventBooking
  - tab「Event booking 1.0」r40-r70 (12 action × 3 nhóm), r114-r152 (詳細設定/各種ページ/決済設定)
  - tab「Task nhỏ + fix bug KH」r12 (xóa event), r201-r241 (Support #37932 — OGP khi share URL, 06/2026)
Bổ sung: TCsLine_Improve chung / tab「Improve nhỏ」r1152, r1173 (preview sub action 当日日付を登録).
"""
from _common import tc

ADM = "- Đăng nhập admin (主管理者) bot A đã có LIFF ID\n- Đã có event E với 1 開催日 + 1 予約枠 S1"
SLOT = ADM + "\n- Đang ở màn setting 予約枠 S1 (SCR-EBD-07), phần「アクション設定」"

S2 = [
    # ══════════════════ 7. アクション設定 ══════════════════
    tc("アクション設定", "FUNC-001", "Normal",
       "Nhóm action 予約時 — set đủ 4 action và lưu đúng vào 4 cột action_id_*_v1 của slot",
       SLOT,
       "1. Ở nhóm action「予約時」set lần lượt 4 action: (a) khi booking được duyệt ngay, "
       "(b) khi booking chờ duyệt, (c) khi admin duyệt, (d) khi admin từ chối\n"
       "2. Mỗi action chọn 1 template text khác nhau để phân biệt\n3. Lưu slot\n"
       "4. Mở lại màn setting slot\n5. Kiểm tra DB `b_slot` 4 cột action tương ứng",
       "4 template text: A1「予約完了」/ A2「申込受付」/ A3「承認しました」/ A4「お断りします」",
       "- Mở lại: 4 ô action hiện đúng 4 template đã chọn, không lẫn thứ tự\n"
       "- DB: 4 cột `action_id_*_v1` trỏ tới 4 bản ghi `t_actions` khác nhau, "
       "`t_actions.type = 'booking_event_day'`",
       note="Nguồn: Event booking 1.0 r42-r45. Spec Field Matrix #42 (SC-004) + §2.4."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Nhóm action 予約変更時 — set đủ 4 action và lưu đúng",
       SLOT + "\n-「予約変更」đang để 全承認 hoặc リクエスト制",
       "1. Ở nhóm action「予約変更時」set 4 action: change được duyệt ngay / request change chờ duyệt / "
       "admin duyệt request change / admin từ chối request change\n2. Lưu\n3. Mở lại kiểm tra",
       "4 template text khác nhau B1〜B4",
       "- Mở lại hiện đúng 4 action đã set, không lẫn với nhóm 予約時\n"
       "- DB 4 cột `action_id_*_change_request_v1` trỏ đúng",
       note="Nguồn: Event booking 1.0 r52-r55."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Nhóm action キャンセル時 — set đủ 4 action và lưu đúng",
       SLOT + "\n-「予約キャンセル」đang để 全承認 hoặc リクエスト制",
       "1. Ở nhóm action「キャンセル時」set 4 action: cancel được duyệt ngay / request cancel chờ duyệt / "
       "admin duyệt request cancel / admin từ chối request cancel\n2. Lưu\n3. Mở lại kiểm tra",
       "4 template text khác nhau C1〜C4",
       "- Mở lại hiện đúng 4 action đã set\n- DB 4 cột `action_id_*_cancel_v1` trỏ đúng",
       note="Nguồn: Event booking 1.0 r62-r65."),

    tc("アクション設定", "FUNC-001", "Normal",
       "優先アクション = 予約枠（下記）のアクション → LUÔN gửi action của slot dù plan có set action",
       ADM + "\n- Slot S1 có コース P1; slot set 4 action nhóm 予約時 (A1〜A4)\n"
       "- コース P1 CŨNG set 4 action khác (P1-A1〜P1-A4)\n"
       "- Slot chọn「優先アクション」=「予約枠（下記）のアクション」(`using_action_slot_booking_v1 = 0`)\n"
       "- Slot 承認方法 = 全承認",
       "1. LINE user đặt 1 chỗ chọn コース P1\n2. Mở LINE app phía user xem tin nhận được\n"
       "3. Mở chat 1:1 phía admin xem trigger đã ghi",
       "Slot action A1 vs plan action P1-A1",
       "- LINE user nhận đúng nội dung **A1 (action của SLOT)**, KHÔNG phải P1-A1\n"
       "- Chat 1:1 hiển thị đúng tin A1 đã gửi",
       note="Nguồn: Event booking 1.0 r40 + r272-r275. Spec BR-17 (`= 0` → CHỈ dùng action của SLOT). "
            "RULE-06 — verify tới tin thật trên LINE app."),

    tc("アクション設定", "FUNC-001", "Normal",
       "優先アクション = コース別アクション + plan CÓ set action → gửi action của plan",
       ADM + "\n- Slot S1 có コース P1; slot set A1, plan P1 set P1-A1\n"
       "- Slot chọn「優先アクション」=「コース別アクション」(`using_action_slot_booking_v1 = 1`)\n"
       "- Slot 承認方法 = 全承認",
       "1. LINE user đặt 1 chỗ chọn コース P1\n2. Mở LINE app phía user xem tin nhận được",
       "Slot A1 vs plan P1-A1, ưu tiên plan",
       "- LINE user nhận đúng nội dung **P1-A1 (action của コース)**",
       note="Nguồn: Event booking 1.0 r276-r279. Spec BR-17."),

    tc("アクション設定", "FUNC-001", "Normal",
       "優先アクション = コース別アクション nhưng plan KHÔNG set action → fallback về action của slot",
       ADM + "\n- Slot S1 có コース P2 **chưa set action nào**; slot set A1\n"
       "- Slot chọn「優先アクション」=「コース別アクション」· 承認方法 = 全承認",
       "1. LINE user đặt 1 chỗ chọn コース P2\n2. Mở LINE app phía user xem tin nhận được",
       "plan P2 không có action",
       "- LINE user nhận nội dung **A1 (fallback về action của slot)**\n- KHÔNG bị im lặng (không gửi gì)",
       note="Nguồn: Event booking 1.0 r276「Nếu plan không set action thì gửi action của slot」. Spec BR-17."),

    tc("アクション設定", "STATE-DEP-001", "Abnormal",
       "Đổi lịch giữa slot CÓ plan ↔ slot KHÔNG plan (ưu tiên action plan) — action gửi phải theo slot ĐÍCH",
       ADM + "\n- Slot A: KHÔNG có コース, set action A-change\n"
       "- Slot B: CÓ コース, 優先アクション =「コース別アクション」, コース set action B-change\n"
       "- Cả 2 slot đều cho phép 予約変更 = リクエスト制\n- LINE user đã có 1 booking ở slot A",
       "1. LINE user đổi lịch từ slot A → slot B (request change)\n2. Xem tin nhận được trên LINE app\n"
       "3. Tạo booking khác ở slot B, đổi lịch B → A (request change)\n4. Xem tin nhận được",
       "A (no plan) ↔ B (có plan, ưu tiên plan)",
       "- Đổi A → B: nhận action **của slot B / コース của B**\n"
       "- Đổi B → A: nhận action **của slot A**\n"
       "⚠ **Dự kiến FAIL**: corpus ghi nhận đang gửi nhầm action của slot nguồn → nếu tái hiện, RAISE BUG",
       note="Nguồn: Event booking 2.0 r96-r97 (Bug TỰ DETECT chưa fix)：「change từ slot B có plan sang slot A "
            "không có plan => case request change đang send action của slot B??? => Đúng thì phải send action của "
            "slot A」. Xem MT-02 — spec BR-17 KHÔNG mô tả nhánh chuyển đổi này."),

    tc("アクション設定", "MSG-004", "Normal",
       "Action text chèn được 5 biến của booking và replace đúng giá trị khi gửi",
       ADM + "\n- Slot S1 (全承認) có コース P1 料金 5000円, 開催日 2026-09-01, giờ 10:00〜12:00\n"
       "- Action「予約完了」dùng text có chèn đủ 5 biến: tên event / ngày / giờ / số người / số tiền",
       "1. Soạn action text chèn 5 biến\n2. LINE user đặt 2 chỗ ở コース P1\n"
       "3. Mở LINE app phía user đọc tin nhận được\n4. Đối chiếu từng biến với dữ liệu booking",
       "event「体験会2026」· 2026-09-01 · 10:00〜12:00 · 2人 · 10.000円 (5000 × 2)",
       "- Tin trên LINE replace đủ 5 biến, KHÔNG còn ký hiệu biến thô\n"
       "- Số tiền hiện **10.000円** (khớp phép tính tay 5000 × 2), số người hiện **2**",
       note="Nguồn: Event booking 1.0 r66-r70 (5 biến) + Event booking 2.0 r63 (danh sách 5 data cần replace). "
            "RULE-06 + RULE-07."),

    tc("アクション設定", "OUT-PREVIEW-001", "Normal",
       "Preview sub-action friend info kiểu ngày, option 当日日付を登録 hiển thị đúng text",
       ADM + "\n- Đã có friend info kiểu 日付\n- Đang set multi action ở slot event booking, "
       "thêm sub-action gán friend info kiểu 日付 với option「当日日付を登録」",
       "1. Set sub-action friend info type date, chọn option「当日日付を登録」\n2. Lưu\n"
       "3. Mở lại màn setting action, quan sát text preview của sub-action",
       "Option「当日日付を登録」",
       "- Text preview hiện đúng **「当日日付を登録」**, KHÔNG hiện「'Tên friend info'(年月日):」",
       note="Nguồn: TCsLine_Improve chung / tab「Improve nhỏ」r1152 và r1173 (khối booking event)."),

    tc("アクション設定", "DATA-REF-001", "Abnormal",
       "Xóa template/scenario/tag đang được dùng trong multi action của event → mở detail vẫn bình thường",
       ADM + "\n- Slot S1 có multi action gồm 3 sub-action: 1 template, 1 scenario, 1 tag",
       "1. Xóa template đang được sub-action dùng\n2. Mở lại detail slot S1 → quan sát\n"
       "3. Xóa toàn bộ 3 đối tượng đang được dùng\n4. Mở lại detail slot S1",
       "3 sub-action bị xóa đối tượng đích",
       "- Mở detail slot bình thường, **KHÔNG hiện alert lỗi**\n"
       "- Sub-action bị mất đối tượng không còn hiển thị (hoặc hiển thị trạng thái đã xóa rõ ràng)\n"
       "- Các sub-action còn lại giữ nguyên",
       note="Nguồn: TCsLine_Improve chung / tab「Improve nhỏ」r766-r786 (khối multi action, kiểm tra cho các "
            "màn có set action). Corpus khối đó nêu Events/Remind — TC này áp cho slot event booking, "
            "cần Leader xác nhận phạm vi."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Slot có コース dùng ưu tiên action riêng — 3 nhóm action của コース lưu độc lập với slot",
       ADM + "\n- Slot S1 có コース P1",
       "1. Ở màn setting コース P1, set đủ 12 action (3 nhóm × 4)\n2. Lưu\n3. Mở lại màn setting コース\n"
       "4. Mở màn setting slot kiểm tra 12 action của slot",
       "12 action ở plan, 12 action ở slot",
       "- コース mở lại hiện đủ 12 action đã set\n"
       "- 12 action của **slot không bị ghi đè** bởi thao tác trên コース\n"
       "- DB: `b_plan_slot.action_id_*_v1` (12 cột) và `b_slot.action_id_*_v1` (12 cột) độc lập, "
       "`t_actions.type` lần lượt là `booking_event_day_plan` và `booking_event_day`",
       note="Nguồn: Event booking 1.0 r75-r97 (khối setting action của plan). Spec Field Matrix #42."),

    tc("アクション設定", "UI-FIELD-001", "Normal",
       "Khối アクション設定 mức EVENT (tab 詳細設定) — xác nhận có hiển thị trên UI hay không",
       ADM + "\n- Mở tab「詳細設定」của event E",
       "1. Cuộn hết tab「詳細設定」tìm khối「アクション設定」(`#tabSettingActionBasic`)\n"
       "2. Nếu không thấy, mở DevTools kiểm tra element có bị v-if/v-show ẩn không\n"
       "3. Ghi lại kết luận + ảnh chụp",
       "Tab 詳細設定 của event",
       "- Ghi rõ kết luận: khối này **KHÔNG hiển thị** trên UI (khớp spec) hoặc **CÓ hiển thị** "
       "(→ spec sai, phải cập nhật)\n- Nếu có hiển thị: thử set 1 action → kiểm tra 11 cột action/approval "
       "mức event có được ghi không",
       note="Nguồn: spec G-04 —「DB xác nhận 11 cột action/approval mức event đều là cột chết (419/419 rows = "
            "default) → nhiều khả năng khối này bị v-if ẩn vĩnh viễn」. TC bổ sung để ĐÓNG GAP G-04. ⚠ RULE-01: quan điểm `UI-FIELD-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    # ══════════════════ 8. Tab 各種ページ ══════════════════
    tc("Tab 各種ページ", "FUNC-001", "Normal",
       "Step 1 — thông tin trang đặt chỗ: ảnh, tiêu đề, mô tả trên/dưới lưu và hiện đúng phía LINE user",
       ADM + "\n- Đang ở tab「各種ページ」→ Step 1",
       "1. Upload ảnh header\n2. Nhập「イベントタイトル」\n3. Nhập「詳細情報」上段 và 下段\n4. Lưu\n"
       "5. Mở trang LIFF phía LINE user",
       "タイトル「無料体験会」· 上段「体験会のご案内」· 下段「持ち物：筆記用具」",
       "- Trang LIFF hiện đúng ảnh + tiêu đề + đoạn 上段\n"
       "- Có nút「もっと見る▼」, bấm vào hiện đoạn 下段",
       note="Nguồn: Event booking 1.0 r130-r133 + r153-r156. Spec Field Matrix #8/#9/#10."),

    tc("Tab 各種ページ", "UI-003", "Normal",
       "「詳細情報」下段 để trống → ẩn nút もっと見る▼ phía LINE user",
       ADM + "\n- Event E đã nhập 上段, để trống 下段",
       "1. Lưu setting với 下段 rỗng\n2. Mở trang LIFF phía LINE user\n3. Quan sát vùng mô tả",
       "下段 = rỗng",
       "- Trang LIFF **KHÔNG hiện** nút「もっと見る▼」\n- Chỉ hiện đoạn 上段",
       note="Nguồn: spec Field Matrix #10「下段 rỗng → ẩn 「もっと見る▼」」. Corpus không có TC → lấp GAP."),

    tc("Tab 各種ページ", "FUNC-004", "Boundary",
       "Nút 予約にすすむ — text ≤10 ký tự, màu nền/màu chữ lưu đúng và hiện đúng phía LINE user",
       ADM + "\n- Đang ở tab「各種ページ」→ Step 1, phần nút booking",
       "1. Quan sát giá trị mặc định (text + màu nền + màu chữ)\n2. Nhập text 10 ký tự → Lưu\n"
       "3. Nhập text 11 ký tự → Lưu → ghi message\n4. Đổi màu nền sang #FF0000, màu chữ #000000 → Lưu\n"
       "5. Mở trang LIFF phía LINE user",
       "Mặc định:「予約にすすむ」/ nền #08bf5a / chữ #ffffff · text 10 ký tự / 11 ký tự · nền #FF0000",
       "- Mặc định đúng「予約にすすむ」+ nền #08bf5a + chữ #ffffff\n"
       "- 10 ký tự lưu được; 11 ký tự báo lỗi giới hạn, chặn lưu\n"
       "- Trang LIFF: nút hiện đúng text và **đúng màu #FF0000 / #000000**",
       note="Nguồn: Event booking 1.0 r134-r135 + spec Field Matrix #11."),

    tc("Tab 各種ページ", "FUNC-001", "Normal",
       "Step 3 — 予約完了ページ kiểu「talklistに戻る」→ sau khi đặt xong quay về màn chat LINE",
       ADM + "\n- Step 3 chọn kiểu trang sau khi đặt =「chat/talklist」(`flag_page_end` tương ứng)\n"
       "- Slot 全承認, không bật 決済",
       "1. Lưu setting\n2. LINE user mở link, đặt 1 chỗ, bấm xác nhận\n3. Quan sát màn hình sau khi đặt",
       "flag_page_end = trở về talklist",
       "- Sau khi đặt xong, LIFF tự đóng và quay về **màn chat 1:1 với bot** trong LINE\n"
       "- Booking vẫn được tạo đầy đủ",
       note="Nguồn: Event booking 1.0 r144. Spec Field Matrix #18."),

    tc("Tab 各種ページ", "FUNC-003", "Normal",
       "Step 3 — 予約完了ページ kiểu redirect URL: validate format URL + redirect đúng",
       ADM + "\n- Đang ở Step 3, chọn kiểu = redirect URL",
       "1. Nhập chuỗi không phải URL (VD「abc」) → Lưu → ghi message\n"
       "2. Nhập URL hợp lệ https://example.com/thanks → Lưu\n"
       "3. LINE user đặt 1 chỗ → quan sát trang sau khi đặt",
       "「abc」/ https://example.com/thanks",
       "- Nhập「abc」: báo lỗi「URLのフォーマットで入力してください。」, chặn lưu\n"
       "- URL hợp lệ: lưu được; sau khi user đặt xong, trình duyệt LIFF chuyển tới "
       "https://example.com/thanks",
       note="Nguồn: Event booking 1.0 r145 + spec Field Matrix #18."),

    tc("Tab 各種ページ", "FUNC-001", "Normal",
       "Step 3 — 予約完了ページ kiểu trang xác nhận trong LIFF → hiện trang hoàn tất có nội dung đã set",
       ADM + "\n- Step 3 chọn kiểu = hiện trang confirm trong LIFF, đã nhập nội dung trang hoàn tất",
       "1. Lưu setting\n2. LINE user đặt 1 chỗ\n3. Quan sát trang sau khi đặt",
       "Nội dung trang hoàn tất「お申込みありがとうございました」",
       "- Sau khi đặt, LIFF hiện trang hoàn tất với đúng nội dung đã set\n- KHÔNG tự đóng về talklist",
       note="Nguồn: Event booking 1.0 r146."),

    tc("Tab 各種ページ", "FUNC-001", "Normal",
       "利用規約 — bật/tắt hiển thị và bật/tắt checkbox đồng ý, phía LINE user khớp setting",
       ADM + "\n- Đã nhập nội dung「利用規約文章」",
       "1. Bật hiển thị quy chế + bật checkbox đồng ý → Lưu → mở LIFF quan sát\n"
       "2. Bật hiển thị quy chế + TẮT checkbox → Lưu → mở LIFF quan sát\n"
       "3. TẮT hiển thị quy chế → Lưu → mở LIFF quan sát",
       "3 tổ hợp của `is_use_terms` × `is_use_checkbox`",
       "- (1) LIFF hiện nội dung quy chế + có checkbox「利用規約に同意」\n"
       "- (2) LIFF hiện nội dung quy chế, KHÔNG có checkbox\n"
       "- (3) LIFF KHÔNG hiện quy chế và KHÔNG có checkbox",
       note="Nguồn: Event booking 1.0 r140-r142, r252-r256. Spec Field Matrix #17. "
            "3 state cho 3 kết quả khác nhau nhưng cùng 1 chuỗi thao tác đối chiếu → giữ chung 1 TC ma trận."),

    # ══════════════════ 9. Form 予約時入力項目 ══════════════════
    tc("Form 予約時入力項目", "FUNC-001", "Normal",
       "Event mới luôn có sẵn 2 item mặc định お名前 và メールアドレス",
       ADM + "\n- Vừa tạo event mới, chưa thêm item nào",
       "1. Mở tab「各種ページ」→ Step 2\n2. Quan sát danh sách item\n3. Kiểm tra DB `b_info_setting`",
       "Event mới toanh",
       "- Có sẵn đúng 2 item:「お名前」và「メールアドレス」\n"
       "- Cả 2 đều đánh dấu 必須\n"
       "- DB: 2 bản ghi với `friend_info_id` = **-1** và **-3**, `is_default = 1`, `is_require = 1`, "
       "`is_mapping_info = 1`",
       note="Nguồn: Event booking 1.0 r136「Tạo default 2 infor này (tương tự bên quản lý sản phẩm)」+ spec BR-19."),

    tc("Form 予約時入力項目", "STATE-DEP-001", "Abnormal",
       "Bật 決済 → KHÔNG xóa được 2 item mặc định お名前 / メールアドレス",
       ADM + "\n- Event E đã bật「決済機能の利用」ở tab 決済設定",
       "1. Mở Step 2, thử xóa item「お名前」\n2. Thử xóa item「メールアドレス」\n"
       "3. Tắt 決済 → thử xóa lại 2 item",
       "決済 bật → tắt",
       "- Khi 決済 bật: 2 item không xóa được (nút xóa ẩn/disable hoặc báo lỗi)\n"
       "- Khi 決済 tắt: ghi rõ kết quả thật (xóa được hay vẫn chặn)",
       note="Nguồn: spec BR-19「Khi bật thanh toán → không xoá được (cổng TT yêu cầu)」. "
            "Corpus KHÔNG có TC này → lấp GAP. Hành vi khi TẮT 決済 spec không nói → cần Leader chốt (MT-20)."),

    tc("Form 予約時入力項目", "FUNC-002", "Abnormal",
       "Item お名前 luôn 必須 — bỏ trống / chỉ khoảng trắng đều báo lỗi",
       ADM + "\n- Event E bật item「お名前」(setting ON)\n- Có tài khoản LINE test",
       "1. LINE user mở trang đặt chỗ, để trống ô お名前 → bấm xác nhận\n"
       "2. Nhập 3 dấu cách → bấm xác nhận\n3. Nhập「山田太郎」→ bấm xác nhận",
       "Rỗng / 3 dấu cách /「山田太郎」",
       "- Rỗng: báo lỗi, chặn đặt\n- Chỉ khoảng trắng: **cũng báo lỗi**, chặn đặt\n"
       "-「山田太郎」: đặt chỗ thành công",
       note="Nguồn: Event booking 1.0 r198-r201 (item name)."),

    tc("Form 予約時入力項目", "FUNC-001", "Normal",
       "Item お名前 setting OFF → không hiện phía LINE user, vẫn đặt chỗ được",
       ADM + "\n- Event E tắt item「お名前」",
       "1. LINE user mở trang đặt chỗ → quan sát form\n2. Điền các item còn lại → xác nhận đặt chỗ",
       "item name OFF",
       "- Form phía LINE user KHÔNG hiện ô「お名前」\n- Đặt chỗ thành công bình thường",
       note="Nguồn: Event booking 1.0 r197."),

    tc("Form 予約時入力項目", "FUNC-003", "Abnormal",
       "Item メールアドレス — validate định dạng mail",
       ADM + "\n- Event E bật item「メールアドレス」(luôn 必須)",
       "1. LINE user để trống → xác nhận\n2. Nhập 3 dấu cách → xác nhận\n"
       "3. Nhập「abc」(sai định dạng) → xác nhận\n4. Nhập「test@example.com」→ xác nhận",
       "Rỗng / khoảng trắng /「abc」/「test@example.com」",
       "- 3 trường hợp đầu: báo lỗi, chặn đặt\n- Mail hợp lệ: đặt chỗ thành công",
       note="Nguồn: Event booking 1.0 r206-r209."),

    tc("Form 予約時入力項目", "FUNC-002", "Abnormal",
       "Item 短文回答 setting 必須 — bỏ trống / khoảng trắng báo lỗi; latinh và tiếng Nhật đều đặt được",
       ADM + "\n- Event E có 1 item 短文回答 (1 dòng) setting 必須",
       "1. LINE user để trống ô → xác nhận\n2. Nhập chuỗi khoảng trắng → xác nhận\n"
       "3. Nhập「abc」→ xác nhận\n4. Nhập「あいうえお」→ xác nhận",
       "Rỗng / khoảng trắng /「abc」/「あいうえお」",
       "- Rỗng và khoảng trắng: báo lỗi, chặn đặt\n"
       "- 「abc」và「あいうえお」: đều đặt chỗ thành công, giá trị lưu đúng nguyên văn vào "
       "`b_user_booking.detail_info_user`",
       note="Nguồn: Event booking 1.0 r212-r215. Gộp latinh + tiếng Nhật vào 1 TC vì cùng kết quả (RULE tách TC)."),

    tc("Form 予約時入力項目", "FUNC-001", "Normal",
       "Item 短文回答 setting 任意 — bỏ trống vẫn đặt chỗ được",
       ADM + "\n- Event E có 1 item 短文回答 setting 任意",
       "1. LINE user để trống ô → xác nhận\n2. Nhập chuỗi khoảng trắng → xác nhận\n"
       "3. Nhập「abc」→ xác nhận",
       "Rỗng / khoảng trắng /「abc」",
       "- Cả 3 trường hợp đều **đặt chỗ thành công**\n- Giá trị lưu đúng như đã nhập",
       note="Nguồn: Event booking 1.0 r216-r219."),

    tc("Form 予約時入力項目", "UI-INPUT-001", "Boundary",
       "Item 短文回答 KHÔNG cho xuống dòng, item 長文回答 CHO xuống dòng",
       ADM + "\n- Event E có 1 item 短文回答 và 1 item 長文回答",
       "1. Ở ô 短文回答, nhấn Enter giữa chuỗi → quan sát\n"
       "2. Ở ô 長文回答, nhấn Enter giữa chuỗi → quan sát\n3. Đặt chỗ → mở màn detail booking phía admin",
       "Chuỗi「abc」+ Enter +「def」",
       "- Ô 短文回答: **không xuống dòng được** (Enter bị chặn)\n"
       "- Ô 長文回答: xuống dòng được\n- Màn detail booking phía admin hiện đúng nội dung có/không xuống dòng",
       note="Nguồn: Event booking 1.0 r220 và r238. 2 kết quả mong đợi khác nhau nhưng cùng 1 chuỗi so sánh "
            "đối chứng → giữ chung 1 TC."),

    tc("Form 予約時入力項目", "FUNC-003", "Abnormal",
       "Item 短文回答 — 入力フォーマット (name / kana / email / tel / numeric) chặn đúng dữ liệu sai",
       ADM + "\n- Tạo 5 item 短文回答, mỗi item set 1「入力フォーマット」khác nhau: "
       "name · name (katakana) · email · 電話番号 · 数字",
       "1. Với từng item, nhập giá trị SAI định dạng → xác nhận đặt chỗ → ghi lại message lỗi\n"
       "2. Nhập giá trị ĐÚNG định dạng → xác nhận đặt chỗ\n"
       "3. Gọi thẳng API đặt chỗ với giá trị sai định dạng (bypass client)",
       "kana: nhập「やまだ」(hiragana, sai) vs「ヤマダ」· email:「abc」vs「a@b.jp」· "
       "tel:「abc」vs「09012345678」· numeric:「abc」vs「123」",
       "- Mỗi item: giá trị sai → báo lỗi và chặn đặt; giá trị đúng → đặt được\n"
       "- Gọi thẳng API: ghi rõ kết quả thật (nếu ghi được vào DB → lỗ hổng validate server, RAISE BUG)",
       note="Nguồn: Event booking 1.0 r221-r226「Check validate kiểu dữ liệu nhập」(TC gốc chỉ có tiêu đề, "
            "không có expected) + spec G-07 (`b_info_setting.setting`: none/newname/newkana/tel/numeric) + TD-11. "
            "Danh sách option chính xác vẫn là GAP G-07 → cần Leader/Dev xác nhận."),

    tc("Form 予約時入力項目", "FUNC-002", "Abnormal",
       "Item 選択肢回答 setting 必須 — không chọn đáp án nào thì báo lỗi",
       ADM + "\n- Event E có 1 item 選択肢回答 (3 option) setting 必須",
       "1. LINE user không chọn option nào → xác nhận\n2. Chọn 1 option → xác nhận",
       "0 option / 1 option",
       "- Không chọn: báo lỗi, chặn đặt\n- Có chọn: đặt chỗ thành công, giá trị option lưu đúng",
       note="Nguồn: Event booking 1.0 r242-r243."),

    tc("Form 予約時入力項目", "FRIEND-001", "Normal",
       "Item liên kết friend info → auto-fill giá trị cũ của user vào ô nhập",
       ADM + "\n- Item「お名前」liên kết friend info system name\n"
       "- LINE user U1 ĐÃ có giá trị friend info name =「山田太郎」\n- LINE user U2 CHƯA có giá trị",
       "1. U1 mở trang đặt chỗ → quan sát ô お名前\n2. U2 mở trang đặt chỗ → quan sát ô お名前",
       "U1 có value, U2 không có value",
       "- U1: ô お名前 **tự điền sẵn「山田太郎」**\n- U2: ô お名前 **để trống**, không điền giá trị rác",
       note="Nguồn: Event booking 1.0 r192, r202, r210, r228, r240. Spec BR-20. ⚠ RULE-01: quan điểm `FRIEND-001` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Form 予約時入力項目", "FRIEND-001", "Normal",
       "Item 選択肢 liên kết friend info → option trùng value của user được chọn sẵn",
       ADM + "\n- Item 選択肢 liên kết friend info kiểu select có 3 option A/B/C\n"
       "- U1 đã có value = B; U2 chưa có value",
       "1. U1 mở trang đặt chỗ → quan sát item 選択肢\n2. U2 mở trang đặt chỗ → quan sát",
       "U1 value = B; U2 không có value",
       "- U1: option **B được chọn sẵn**\n- U2: **không option nào** được chọn sẵn",
       note="Nguồn: Event booking 1.0 r247."),

    tc("Form 予約時入力項目", "FRIEND-001", "Normal",
       "Item liên kết friend info → sau khi đặt chỗ, giá trị được GHI vào hồ sơ bạn bè",
       ADM + "\n- Item「お名前」liên kết friend info system name; U1 chưa có value\n"
       "- Slot 全承認",
       "1. U1 đặt chỗ, nhập お名前 =「鈴木花子」\n2. Sau khi đặt xong, mở màn detail friend U1 phía admin\n"
       "3. Quan sát giá trị friend info name\n4. Mở lịch sử thay đổi friend info",
       "「鈴木花子」",
       "- Friend info name của U1 = **「鈴木花子」**\n"
       "- Lịch sử friend info sinh 1 bản ghi mới ghi nhận thay đổi này",
       note="Nguồn: Event booking 1.0 r192「sau khi booking update lại friendinfor value」+ r203, r211. "
            "Spec BR-20 (`friend_info_id` âm → cột `line_user`; dương → `friend_information_value`)."),

    tc("Form 予約時入力項目", "FRIEND-001", "Normal",
       "Item KHÔNG liên kết friend info → không auto-fill và KHÔNG ghi ngược vào hồ sơ",
       ADM + "\n- Item 短文回答「備考」KHÔNG liên kết friend info\n- U1 có nhiều friend info sẵn",
       "1. U1 mở trang đặt chỗ → quan sát ô「備考」\n2. Nhập「テスト」→ đặt chỗ\n"
       "3. Mở màn detail friend U1, so sánh toàn bộ friend info trước/sau",
       "「テスト」",
       "- Ô「備考」**không tự điền** gì\n"
       "- Sau khi đặt: **không friend info nào của U1 bị thay đổi**\n"
       "- Giá trị「テスト」chỉ lưu trong `b_user_booking.detail_info_user`",
       note="Nguồn: Event booking 1.0 r193「không tự động fill, sau khi book cũng không cần update value」."),

    tc("Form 予約時入力項目", "FUNC-004", "Boundary",
       "「表示項目名」biên 30 ký tự",
       ADM + "\n- Đang thêm item mới ở Step 2",
       "1. Nhập tên item 30 ký tự → Lưu\n2. Nhập tên item 31 ký tự → Lưu → ghi message",
       "30 / 31 ký tự tiếng Nhật",
       "- 30 ký tự: lưu được\n- 31 ký tự: báo lỗi「入力項目名は30文字以内で入力してください。」, chặn lưu",
       note="Nguồn: spec Field Matrix #12. Corpus không test biên → lấp GAP."),

    tc("Form 予約時入力項目", "FUNC-002", "Abnormal",
       "Item bắt buộc phải chọn「紐つけ友だち情報」→ để trống thì báo lỗi",
       ADM + "\n- Đang thêm item 選択肢回答 mới",
       "1. Nhập tên item, KHÔNG chọn「紐つけ友だち情報」→ Lưu\n2. Chọn 1 friend info → Lưu",
       "Trống / có chọn",
       "- Để trống: báo lỗi「紐つけ友だち情報を入力してください。」, chặn lưu\n- Có chọn: lưu được",
       note="Nguồn: spec Field Matrix #13 + Event booking 1.0 r246「phía admin luôn bắt buộc liên kết info => "
            "không có case này」(cho item 選択肢)."),

    tc("Form 予約時入力項目", "DATA-DB-001", "Normal",
       "Đáp án form lưu inline JSON trong b_user_booking.detail_info_user, không có bảng con",
       ADM + "\n- Event E có 4 item (name, email, 短文, 選択肢)\n- U1 vừa đặt 1 chỗ điền đủ 4 item",
       "1. Query `b_user_booking.detail_info_user` của booking vừa tạo\n"
       "2. Đối chiếu từng phần tử JSON với giá trị đã nhập\n3. Mở màn detail booking phía admin",
       "4 item với giá trị cụ thể",
       "- Cột `detail_info_user` chứa mảng JSON dạng `[{id, title, type, value}]` với **4 phần tử**\n"
       "- `id` khớp `b_info_setting.id` tương ứng\n"
       "- Màn detail booking phía admin hiện đúng 4 cặp tiêu đề - giá trị",
       note="Nguồn: spec Field Matrix #51 (🔑 KHÔNG có bảng con đáp án). TC bổ sung theo RULE-07."),

    tc("Form 予約時入力項目", "STATE-DEP-001", "Abnormal",
       "Xóa / sửa item form SAU KHI đã có booking → đáp án cũ hiển thị thế nào",
       ADM + "\n- Event E có item「備考」, đã có 2 booking điền giá trị cho item này",
       "1. Ghi lại giá trị「備考」của 2 booking\n2. Xóa item「備考」khỏi Step 2 → Lưu\n"
       "3. Mở màn detail của 2 booking cũ\n4. Export CSV danh sách người tham gia",
       "2 booking đã có đáp án cho item bị xóa",
       "- Ghi rõ hành vi thật: đáp án cũ vẫn hiện / bị mất / hiện tiêu đề rỗng\n"
       "- Trang không lỗi 500\n- File CSV không sinh cột rác hoặc lệch cột",
       note="Nguồn: TC bổ sung theo STATE-DEP-001 + spec Field Matrix #51 (đáp án lưu inline JSON, "
            "`id` trỏ `b_info_setting.id` — item bị xóa thì id trỏ vào bản ghi không tồn tại). "
            "Corpus KHÔNG có TC này. Kết quả cần Leader chốt (MT-21)."),

    # ══════════════════ 10. Tab 詳細設定 ══════════════════
    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "1回の予約上限 = N → dropdown số lượng phía LINE user hiện đúng 1..N",
       ADM + "\n- Tab「詳細設定」→「1回の予約上限」",
       "1. Quan sát giá trị mặc định\n2. Set giá trị = 3 → Lưu\n3. Mở trang LIFF phía LINE user\n"
       "4. Mở dropdown chọn số người",
       "Mặc định · set = 3",
       "- Mặc định = **1**\n- Sau khi set 3: dropdown phía LINE user hiện đúng các giá trị **1, 2, 3**",
       note="Nguồn: Event booking 1.0 r114."),

    tc("Tab 詳細設定", "FUNC-004", "Boundary",
       "1回の予約上限 chỉ định khoảng min〜max → dropdown chỉ hiện trong khoảng",
       ADM + "\n- Tab「詳細設定」, bật「1回の予約上限」dạng khoảng",
       "1. Set min = 2, max = 4 → Lưu\n2. Mở trang LIFF, mở dropdown số người\n"
       "3. Quay lại admin set min = 5, max = 3 → Lưu → ghi message",
       "min 2 / max 4 · min 5 / max 3 (nghịch)",
       "- min 2 max 4: dropdown phía LINE user hiện đúng **2, 3, 4** (không có 1)\n"
       "- min 5 max 3: báo lỗi「最大は、最低より大きな数字を入力してください。」, chặn lưu",
       note="Nguồn: Event booking 1.0 r115 + spec Field Matrix #19."),

    tc("Tab 詳細設定", "FUNC-004", "Boundary",
       "1回の予約上限 biên trần kiểu dữ liệu — nhập 127 / 128 / 200",
       ADM + "\n- Tab「詳細設定」→「1回の予約上限」",
       "1. Nhập 127 → Lưu → đọc DB `b_setting_basic_event.limit_people`\n"
       "2. Nhập 128 → Lưu → đọc DB\n3. Nhập 200 → Lưu → đọc DB\n"
       "4. Với giá trị lưu được, mở dropdown phía LINE user đếm số option",
       "127 / 128 / 200",
       "- 127: lưu đúng 127\n- 128 và 200: ghi rõ kết quả thật — nếu DB lưu sai (tràn tinyint) "
       "hoặc lưu 127 âm thầm → **RAISE BUG**\n- Dropdown phía LINE user khớp giá trị thực trong DB",
       note="Nguồn: spec Field Matrix #19 + TD-18 (`limit_people`/`min_people` là tinyint(4) → trần 127). "
            "Corpus KHÔNG test biên này → lấp GAP. Xem MT-14."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "予約可能回数 = 何度でも → user đặt được nhiều lần ở cùng 1 slot",
       ADM + "\n- Tab 詳細設定:「予約可能回数」= 何度でも, KHÔNG tick 各日程ごとに設定する\n"
       "- Slot S1 定員 = 10 (còn nhiều chỗ)",
       "1. LINE user U1 đặt 1 chỗ ở slot S1 → thành công\n"
       "2. U1 quay lại trang đặt chỗ, đặt tiếp slot S1\n3. Lần 3 tương tự",
       "3 lần đặt cùng slot S1",
       "- Cả 3 lần đều đặt thành công\n- `b_user_booking` có 3 bản ghi của U1 ở slot S1\n"
       "- `use_people` của S1 = 3",
       note="Nguồn: Event booking 2.0 r12「1. không giới hạn số lần book」. Spec BR-11 (`type_times_booking = 1`)."),

    tc("Tab 詳細設定", "FUNC-001", "Abnormal",
       "予約可能回数 = 各予約枠 1 回 → đặt lần 2 cùng slot bị chặn, slot khác vẫn đặt được",
       ADM + "\n- Tab 詳細設定:「予約可能回数」= 各予約枠につき 1 回 (`type_times_booking = 2`)\n"
       "- Event có slot S1 và S2 đều còn chỗ\n- U1 đã đặt 1 chỗ ở S1",
       "1. U1 mở lại trang đặt chỗ → quan sát slot S1\n2. Thử đặt lại slot S1\n3. Đặt slot S2",
       "U1 đã có booking ở S1",
       "- Slot S1: **bị ẩn / không chọn được** (server trả `arraySlotIdUserBook`)\n"
       "- Slot S2: đặt được bình thường",
       note="Nguồn: Event booking 2.0 r12「2. Mỗi slot được book tối đa 1」. Spec BR-11."),

    tc("Tab 詳細設定", "FUNC-001", "Abnormal",
       "予約可能回数 = このイベントにつき 1 回 → đặt 1 lần rồi mọi slot của event đều bị chặn",
       ADM + "\n- Tab 詳細設定:「予約可能回数」= このイベントにつき 1 回 (`type_times_booking = 3`)\n"
       "- Event có slot S1 và S2 đều còn chỗ\n- U1 đã đặt 1 chỗ ở S1",
       "1. U1 mở lại trang đặt chỗ\n2. Quan sát cả S1 và S2\n3. Thử đặt S2",
       "U1 đã có 1 booking trong event",
       "- **Cả S1 và S2 đều bị ẩn / không chọn được**\n- Không đặt thêm được bất kỳ slot nào của event này",
       note="Nguồn: Event booking 2.0 r12「3. Chỉ được book 1 lần duy nhất cho toàn event」. Spec BR-11."),

    tc("Tab 詳細設定", "FUNC-004", "Boundary",
       "予約単位 (đơn vị đặt chỗ) — mặc định 人, biên 3 ký tự",
       ADM + "\n- Tab「詳細設定」→「予約単位変更」",
       "1. Quan sát giá trị mặc định\n2. Nhập 3 ký tự「テスト」→ Lưu\n"
       "3. Nhập 4 ký tự → Lưu → ghi message\n4. Mở trang LIFF phía LINE user xem đơn vị hiển thị",
       "Mặc định · 3 ký tự · 4 ký tự",
       "- Mặc định = **「人」**\n- 3 ký tự: lưu được, LINE user hiện đúng đơn vị mới\n"
       "- 4 ký tự: báo lỗi giới hạn, chặn lưu",
       note="Nguồn: Event booking 1.0 r120「default là 人 → cho phép nhập tối đa 3 ký tự」+ spec Field Matrix #22."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "Toggle 予約枠の残数 — bật/tắt điều khiển việc hiện số 残数 phía LINE user",
       ADM + "\n- Slot S1 定員 = 10, đã dùng 3",
       "1. Bật「予約枠の残数」= 表示 → Lưu → mở LIFF quan sát\n"
       "2. Đổi thành 非表示 → Lưu → reload LIFF quan sát",
       "定員 10, use_people 3 → remain 7",
       "- Khi 表示: LINE user thấy số 残数 = **7**\n- Khi 非表示: LINE user **không thấy** số 残数 nào "
       "(cả ở slot và コース)",
       note="Nguồn: Event booking 1.0 r121-r122 + r179-r180. ⚠ Spec BR-23: cột `is_hide_remain` NGƯỢC NGHĨA "
            "(1 = 表示) — verify cả giá trị DB, xem MT-03."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "Toggle 受付期間終了した予約枠 = 表示 → slot hết hạn vẫn hiện nhưng KHÔNG chọn được",
       ADM + "\n- Event có slot S_exp đã quá 締切日時 và slot S_ok còn hạn\n- Toggle 受付終了 = 表示",
       "1. Mở trang LIFF phía LINE user\n2. Quan sát slot S_exp\n3. Thử tick chọn S_exp\n4. Chọn S_ok",
       "S_exp quá hạn, S_ok còn hạn",
       "- S_exp **vẫn hiện** trong danh sách nhưng bị disable, tick không được\n"
       "- Toàn bộ コース thuộc S_exp cũng bị disable\n- S_ok chọn được bình thường",
       note="Nguồn: Event booking 1.0 r123 + r185. Spec BR-23."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "Toggle 受付期間終了した予約枠 = 非表示 → ẩn hẳn slot hết hạn và toàn bộ コース của nó",
       ADM + "\n- Event có slot S_exp quá 締切 (có 2 コース) và slot S_ok còn hạn\n- Toggle 受付終了 = 非表示",
       "1. Mở trang LIFF phía LINE user\n2. Đếm số slot hiển thị\n3. Tìm 2 コース của S_exp",
       "S_exp có 2 コース",
       "- Chỉ hiện S_ok, **S_exp bị ẩn hoàn toàn**\n- 2 コース của S_exp cũng không hiện",
       note="Nguồn: Event booking 1.0 r124 + r184「slot hết hạn thì cũng ẩn toàn bộ plan của slot đó」."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "Toggle 満席の予約枠 = 表示 → slot full vẫn hiện, hiện text 満席, không chọn được",
       ADM + "\n- Slot S_full 定員 = 2, `use_people` = 2 (đã full)\n- Toggle 満席 = 表示, 残数 = 表示",
       "1. Mở trang LIFF phía LINE user\n2. Quan sát slot S_full\n3. Thử tick chọn",
       "定員 2, đã dùng 2",
       "- S_full **vẫn hiện**, ở vị trí 残数 hiện text **「満席」**\n- Tick chọn không được",
       note="Nguồn: Event booking 1.0 r125 + r183, r187."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "Toggle 満席の予約枠 = 非表示 — slot full bị ẩn; slot có コース thì ẩn theo TỪNG コース",
       ADM + "\n- Slot S_a KHÔNG có コース, đã full\n"
       "- Slot S_b có 2 コース: P1 đã full, P2 còn chỗ\n- Toggle 満席 = 非表示",
       "1. Mở trang LIFF phía LINE user\n2. Tìm S_a\n3. Mở S_b xem danh sách コース",
       "S_a full; S_b: P1 full, P2 còn chỗ",
       "- S_a **bị ẩn hoàn toàn**\n- S_b **vẫn hiện** (vì còn P2)\n"
       "- Trong S_b: コース P1 **bị ẩn**, chỉ hiện P2",
       note="Nguồn: Event booking 1.0 r126 + r186「Case slot có plan thì check theo plan, plan nào full thì ẩn đi」."),

    tc("Tab 詳細設定", "UI-003", "Normal",
       "Xác nhận giá trị MẶC ĐỊNH của 3 toggle 予約枠表示設定 khi tạo event mới",
       ADM + "\n- Vừa tạo event mới, chưa đụng vào tab 詳細設定",
       "1. Mở tab「詳細設定」\n2. Chụp trạng thái 3 toggle: 残数 / 受付期間終了 / 満席\n"
       "3. Đọc DB `b_setting_basic_event`: `is_hide_remain`, `is_show_slot_expire`, `is_show_slot_over`\n"
       "4. Đối chiếu UI ↔ DB",
       "Event mới toanh",
       "- Ghi rõ giá trị mặc định của cả 3 toggle trên UI và giá trị DB tương ứng\n"
       "- Xác nhận `is_hide_remain = 1` tương ứng với UI hiện「表示」(nếu ngược → RAISE BUG spec/tên cột)",
       note="Nguồn: spec G-05 (default 3 toggle CHƯA xác định) + BR-23 (cảnh báo tên cột ngược nghĩa). "
            "TC bổ sung để ĐÓNG GAP G-05. Xem MT-03."),

    tc("Tab 詳細設定", "FUNC-001", "Normal",
       "開催情報 + 地図設定 — chọn địa chỉ trên bản đồ, bật/tắt hiển thị bản đồ phía LINE user",
       ADM + "\n- Tab「詳細設定」→ phần「開催情報」",
       "1. Nhập text 開催情報\n2. Chọn địa chỉ trên bản đồ → Lưu → kiểm tra DB `address`/`lat`/`lng`\n"
       "3. Bật「地図を表示」→ Lưu → mở LIFF quan sát\n4. Tắt「地図を表示」→ Lưu → reload LIFF quan sát",
       "Địa chỉ「東京都渋谷区…」",
       "- DB lưu đúng `address`, `lat`, `lng`\n"
       "- Bật: LIFF hiện **bản đồ kèm địa chỉ**\n- Tắt: LIFF **chỉ hiện địa chỉ dạng text**, không có bản đồ",
       note="Nguồn: Event booking 1.0 r127-r129 + r157-r159. Spec Field Matrix #25 "
            "(⚠ `lat`/`lng` lưu varchar — TD-25)."),

    tc("Tab 詳細設定", "FUNC-004", "Boundary",
       "「開催情報」địa chỉ biên 255 ký tự",
       ADM + "\n- Tab「詳細設定」→ ô địa chỉ",
       "1. Nhập địa chỉ 255 ký tự → Lưu\n2. Nhập 256 ký tự → Lưu → ghi kết quả\n3. Đọc DB `address`",
       "255 / 256 ký tự",
       "- 255: lưu đủ, DB giữ nguyên chuỗi\n"
       "- 256: ghi rõ kết quả thật — nếu bị cắt âm thầm hoặc lỗi SQL → RAISE BUG",
       note="Nguồn: spec Field Matrix #25 (`address` ≤255). Corpus không test biên → lấp GAP."),

    # ══════════════════ 11. Tab 決済設定 ══════════════════
    tc("Tab 決済設定", "FUNC-001", "Normal",
       "Bật / tắt 決済機能の利用 → phía LINE user có / không có bước nhập thẻ",
       ADM + "\n- Bot A đã liên kết Stripe (`status_strip_bot = 3`)\n- Slot S1 có コース P1 料金 5000円",
       "1. Tắt「決済機能の利用」→ Lưu → LINE user đặt 1 chỗ chọn P1\n"
       "2. Bật「決済機能の利用」, chọn Stripe → Lưu → LINE user đặt 1 chỗ chọn P1",
       "コース có 料金 5000円",
       "- Khi TẮT: sau bước xác nhận là đặt xong luôn, **không hiện màn nhập thẻ**\n"
       "- Khi BẬT: sau bước xác nhận **chuyển sang màn nhập thẻ**",
       note="Nguồn: Event booking 1.0 r147-r148 + r260-r261. Spec Field Matrix #26 "
            "(⚠ không có cột `is_use_payment`, suy từ `type_system_bill`)."),

    tc("Tab 決済設定", "UI-FIELD-001", "Abnormal",
       "Dropdown 利用する決済システム chỉ hiện cổng ĐÃ liên kết",
       "- Bot X CHƯA liên kết cổng nào\n- Bot Y chỉ liên kết Stripe (`status_strip_bot = 3`)\n"
       "- Bot Z chỉ liên kết UnivaPay (`univapay_app_id` khác rỗng)",
       "1. Ở bot X mở tab 決済設定, bật 決済 → mở dropdown「利用する決済システム」\n"
       "2. Lặp lại ở bot Y\n3. Lặp lại ở bot Z",
       "3 bot với 3 trạng thái liên kết khác nhau",
       "- Bot X: dropdown **không có** option nào (hoặc chặn bật 決済)\n"
       "- Bot Y: chỉ có option **Stripe**\n- Bot Z: chỉ có option **UnivaPay**",
       note="Nguồn: spec §1.4 (điều kiện tiên quyết cổng thanh toán). Corpus 3D secure r97-r103 có kiểm "
            "tổ hợp liên kết nhưng góc nhìn khác → TC này kiểm chính dropdown."),

    tc("Tab 決済設定", "STATE-DEP-001", "Abnormal",
       "利用する決済システム KHÔNG đổi được sau khi đã lưu",
       ADM + "\n- Event E đã lưu với 決済 = Stripe\n- Bot A liên kết cả Stripe và UnivaPay",
       "1. Mở lại tab 決済設定 của event E\n2. Thử đổi dropdown sang UnivaPay\n"
       "3. Nếu đổi được thì Lưu và kiểm tra DB `type_system_bill`\n"
       "4. Gọi thẳng API save với `type_system_bill = 2`",
       "Stripe (1) → UnivaPay (2)",
       "- Dropdown ở trạng thái **khóa / disable**, không đổi được trên UI\n"
       "- Gọi thẳng API: ghi rõ kết quả — nếu DB đổi được → lỗ hổng validate server (RAISE BUG)",
       note="Nguồn: spec Field Matrix #27「Immutable sau khi lưu」+ TD-11. Corpus KHÔNG có TC này → lấp GAP."),

    tc("Tab 決済設定", "ENV-003", "Normal",
       "販売環境設定 テスト / 本番 — lưu đúng và booking ghi nhận đúng môi trường",
       ADM + "\n- Event E bật 決済 = Stripe\n- Bot A có cả khóa test và khóa live ở `s_strip_bot`",
       "1. Chọn「販売環境設定」= テスト → Lưu → đọc DB `flag_environment`\n"
       "2. LINE user đặt + thanh toán 1 chỗ → kiểm tra giao dịch trên Stripe dashboard TEST\n"
       "3. Đổi sang 本番 → Lưu → đọc DB\n4. Đặt + thanh toán → kiểm tra Stripe dashboard LIVE",
       "flag_environment: 0 (テスト) → 1 (本番)",
       "- テスト: `flag_environment` = 0; giao dịch chỉ xuất hiện ở **dashboard test**\n"
       "- 本番: `flag_environment` = 1; giao dịch xuất hiện ở **dashboard live**\n"
       "- Không có giao dịch nào lọt nhầm môi trường",
       env="PRODUCTION",
       note="Nguồn: spec Field Matrix #28. Corpus Event booking 1.0 r262-r265「MT test / MT product」"
            "(TC gốc chỉ có tiêu đề). RULE-08 — bill tiền BẮT BUỘC test PRODUCTION. ⚠ RULE-01: quan điểm `ENV-003` trong bộ này KHÔNG có loại case **Boundary** — lý do: quan điểm này kiểm hành vi/trạng thái, không có trục giá trị biên để đo."),

    tc("Tab 決済設定", "FUNC-001", "Normal",
       "特定商取引法に基づく表記 — lưu và hiện đúng ở màn nhập thẻ phía LINE user",
       ADM + "\n- Event E bật 決済",
       "1. Nhập nội dung「特定商取引法に基づく表記」bằng TinyMCE\n2. Lưu\n"
       "3. LINE user đặt chỗ tới màn nhập thẻ\n4. Mở link 特商法 trên màn đó",
       "Nội dung 特商法 có xuống dòng + in đậm",
       "- Nội dung lưu vào DB `content_term_bill`\n"
       "- Màn nhập thẻ phía LINE user mở được trang 特商法 với đúng nội dung + định dạng đã soạn",
       note="Nguồn: Event booking 1.0 r151「lưu vào db và hiện ở màn nhập bill tiền」+ spec Field Matrix #29."),

    tc("Tab 決済設定", "SEC-001", "Normal",
       "Trang preview 特商法 dùng Hashids — không lộ id số nguyên của event",
       ADM + "\n- Event E (id = 1118) đã nhập nội dung 特商法",
       "1. Bấm nút preview 特商法\n2. Quan sát URL\n"
       "3. Thử sửa URL thay hash bằng số nguyên 1118 → mở",
       "Event id 1118",
       "- URL preview chứa **chuỗi hash**, không chứa 1118\n"
       "- Thay hash bằng 1118: không mở được nội dung (hoặc báo lỗi), không lộ dữ liệu event khác",
       note="Nguồn: spec BR-25 (`previewTermBill`, `saveAndPreviewTermBill`). Corpus KHÔNG có TC này."),

    # ══════════════════ 12. Copy & xóa event ══════════════════
    tc("Copy & xóa event", "DATA-BACKUP-001", "Normal",
       "Copy event → nhân bản đủ 開催日 / slot / plan / action / setting 4 tab, KHÔNG copy booking",
       ADM + "\n- Event E có: 2 開催日, mỗi ngày 2 slot, mỗi slot 1 コース, đã set action, "
       "3 item form, bật 決済 Stripe, có 5 booking",
       "1. Ở màn list bấm ⋯ →「コピー」cho event E\n2. Mở event bản copy\n"
       "3. Đối chiếu lần lượt 4 tab với bản gốc\n4. Mở màn 参加者リスト của bản copy\n"
       "5. Kiểm tra `use_people` / `remain_limit` của slot/plan bản copy",
       "E có 2 ngày × 2 slot × 1 コース + 5 booking",
       "- Bản copy có đủ 2 ngày, 4 slot, 4 コース, action giống bản gốc\n"
       "- 3 item form + setting 決済 giống bản gốc\n"
       "- **0 booking** ở bản copy; `use_people` và `remain_limit` đều = 0\n"
       "- Bản gốc E không bị thay đổi gì",
       note="Nguồn: Event booking 1.0 r22「copy event」(TC gốc chỉ có tiêu đề) + TCsLine_Improve chung / "
            "「Improve nhỏ」r456, r500 (copy event có ảnh). Expected chi tiết do AI viết theo DATA-BACKUP-001 "
            "→ cần Leader xác nhận (đặc biệt: bản copy có copy setting 決済 không)."),

    tc("Copy & xóa event", "DATA-REF-001", "Abnormal",
       "Xóa 1 event → xóa toàn bộ dữ liệu liên quan gồm cả remind user_event",
       ADM + "\n- Event E có 1 開催日, 2 slot (1 slot bật remind), 2 コース, 4 booking approve, "
       "4 bản ghi `user_event` remind tương ứng",
       "1. Ghi lại id của ngày / slot / plan / booking / user_event\n"
       "2. Ở màn list bấm ⋯ →「削除」cho event E → xác nhận\n"
       "3. Query lần lượt `b_setting_date_event`, `b_slot`, `b_plan_slot`, `b_user_booking`, `user_event`",
       "E có 4 booking + 4 remind",
       "- Không còn bản ghi nào ở 4 bảng đầu trỏ tới event E\n"
       "- **4 bản ghi `user_event` (remind) cũng bị xóa** — LINE user không còn nhận remind của event đã xóa",
       note="Nguồn: Event booking 1.0 r20「Check xóa các thông tin của event: ngày / slot / plan / user booking / "
            "remind: user event」+ Task nhỏ r12. Đây là TC quan trọng nhất của nhóm này."),

    tc("Copy & xóa event", "BULK-001", "Abnormal",
       "Xóa NHIỀU event cùng lúc → chỉ xóa đúng các event được tick",
       ADM + "\n- Folder có 5 event E1..E5, mỗi event có ít nhất 1 booking",
       "1. Tick chọn E2, E4\n2. Bấm xóa hàng loạt → xác nhận\n"
       "3. Đếm số event còn lại ở folder\n4. Kiểm tra booking của E1, E3, E5 còn nguyên không",
       "Tick 2/5 event",
       "- Chỉ E2 và E4 bị xóa; còn lại **3 event** E1, E3, E5\n"
       "- Booking của E1, E3, E5 vẫn còn đủ, không bị xóa lây",
       note="Nguồn: Event booking 1.0 r21「xóa nhiều event」— TC gốc chỉ có tiêu đề → expected do AI viết "
            "theo BULK-001 (phạm vi thao tác hàng loạt)."),

    tc("Copy & xóa event", "PAY-STATE-001", "Abnormal",
       "Xóa event đang có booking ĐÃ thanh toán → xác nhận hành vi với dữ liệu tiền",
       ADM + "\n- Event E có 2 booking đã thanh toán Stripe thành công (`status_payment = 1`)",
       "1. Ghi lại charge id của 2 booking trên Stripe dashboard\n2. Xóa event E\n"
       "3. Kiểm tra `b_user_booking` của 2 booking\n4. Kiểm tra 2 giao dịch trên Stripe dashboard\n"
       "5. Kiểm tra lịch sử booking ở màn detail friend",
       "2 booking đã bill 5000円 mỗi booking",
       "- Ghi rõ hành vi thật: booking bị xóa cứng hay giữ lại\n"
       "- Giao dịch trên Stripe **KHÔNG bị hoàn tiền tự động**\n"
       "- Ghi rõ lịch sử booking ở màn detail friend còn hay mất — nếu mất thì mất dấu vết giao dịch đã thu tiền "
       "→ RAISE làm rủi ro nghiệp vụ",
       env="PRODUCTION",
       note="TC bổ sung theo spec TD-01 (xóa cascade thủ công, không transaction) + BR-21. "
            "Corpus KHÔNG có TC xóa event khi đã thu tiền → GAP nghiêm trọng. Xem MT-08."),

    # ══════════════════ 13. Preview & OGP ══════════════════
    tc("Preview & OGP", "OUT-PREVIEW-001", "Normal",
       "Màn preview event khớp với trang LIFF thật phía LINE user",
       ADM + "\n- Event E đã setting đủ: ảnh header, tiêu đề, mô tả trên/dưới, nút booking màu tùy chỉnh, "
       "quy chế, 開催情報 có bản đồ",
       "1. Bấm nút preview ở màn edit event\n2. Chụp màn preview\n"
       "3. Mở link LIFF thật bằng LINE app\n4. Đối chiếu từng thành phần giữa 2 màn",
       "Event có đủ 6 thành phần hiển thị",
       "- Preview và trang LIFF thật **khớp nhau** ở cả 6 thành phần: ảnh / tiêu đề / mô tả trên / mô tả dưới / "
       "màu + text nút / quy chế + bản đồ\n- Không có thành phần nào chỉ hiện ở 1 bên",
       note="Nguồn: Event booking 1.0 r152「Check màn preview」(TC gốc chỉ có tiêu đề). Expected viết theo "
            "OUT-PREVIEW-001 (preview PHẢI khớp output thật)."),

    tc("Preview & OGP", "REG-URL-001", "Normal",
       "Share URL event lên 6 kênh ngoài → preview hiện đúng title/description, KHÔNG hiện ảnh American Express",
       ADM + "\n- Event E (KHÔNG bật 決済) có title và description rõ ràng\n"
       "- Chưa từng share URL này (chưa bị cache)",
       "1. Copy URL đặt chỗ của event E\n"
       "2. Lần lượt share lên: Facebook (post + comment) · Instagram · X · LINE · Email · Messenger\n"
       "3. Ở mỗi kênh quan sát khối preview",
       "6 kênh × 1 URL event",
       "- Cả 6 kênh: preview hiện **đúng title và description của event**\n"
       "- **KHÔNG kênh nào hiện ảnh American Express**",
       note="Nguồn: Task nhỏ + fix bug KH r202-r207 (Support #37932, 06/2026). "
            "6 kênh cùng 1 kết quả mong đợi → gộp 1 TC, liệt kê đủ 6 điểm ở cột Dữ liệu test."),

    tc("Preview & OGP", "REG-URL-001", "Normal",
       "Share URL event CÓ bật 決済 → preview vẫn đúng, không hiện ảnh American Express",
       ADM + "\n- Event F **CÓ bật 決済** (Stripe hoặc UnivaPay), có title/description\n- Chưa từng share",
       "1. Copy URL đặt chỗ của event F\n"
       "2. Share lên Facebook (post + comment) · Instagram · X · LINE · Email · Messenger\n"
       "3. Quan sát preview ở từng kênh",
       "6 kênh × event có bật 決済",
       "- Cả 6 kênh hiện đúng title + description\n"
       "- **KHÔNG hiện ảnh American Express** (đây là nguyên nhân gốc của Support #37932 — ảnh logo thẻ "
       "trong trang thanh toán bị crawler nhặt làm og:image)",
       note="Nguồn: Task nhỏ r218-r223. Đây là nhánh QUAN TRỌNG nhất của #37932 vì event bật 決済 mới có ảnh "
            "logo thẻ trong HTML."),

    tc("Preview & OGP", "DATA-TEXT-001", "Normal",
       "Preview OGP với title/description dài, tiếng Nhật, emoji → hiển thị đúng, không vỡ",
       ADM + "\n- Chuẩn bị 4 event: (a) title rất dài, (b) description rất dài, (c) tiêu đề tiếng Nhật, "
       "(d) tiêu đề có emoji",
       "1. Share URL của từng event lên Facebook và LINE\n2. Quan sát preview",
       "(a) title 200 ký tự · (b) description 500 ký tự · (c)「無料体験会のご案内」· (d)「体験会🎁🤖」",
       "- Cả 4 event: preview hiện đúng title + description (dài thì bị cắt gọn theo chuẩn của kênh, "
       "không vỡ layout, không mojibake, emoji hiện đúng)\n- Không hiện ảnh American Express",
       note="Nguồn: Task nhỏ r208-r211 và r224-r227. 4 input khác nhau nhưng cùng 1 kết quả → gộp 1 TC."),

    tc("Preview & OGP", "LIFF-ENTRY-001", "Normal",
       "URL đã share — user mở được và đặt chỗ được bình thường ở nhiều môi trường",
       ADM + "\n- URL event đã được share lên FB / LINE / Email",
       "1. Từ mỗi kênh, bấm mở URL bằng: LINE app (iOS), LINE app (Android), trình duyệt PC\n"
       "2. Quan sát trang mở ra\n3. Thực hiện đặt 1 chỗ từ mỗi điểm vào",
       "3 kênh × 3 môi trường mở",
       "- Mọi điểm vào đều mở được **màn đặt chỗ của đúng event**\n- Đặt chỗ thành công ở mọi điểm vào",
       note="Nguồn: Task nhỏ r212-r213 và r228-r229."),

    tc("Preview & OGP", "DATA-CACHE-001", "Normal",
       "Sửa title/description rồi share lại → preview cập nhật theo text mới nhất",
       ADM + "\n- Event E đã share 1 lần với title cũ",
       "1. Sửa title và description của event E\n2. Lưu\n3. Share lại URL lên Facebook\n"
       "4. Nếu vẫn hiện text cũ: mở FB Sharing Debugger → bấm「Scrape Again」→ share lại",
       "Title cũ「体験会」→ mới「有料セミナー」",
       "- Preview hiện text **mới nhất**\n"
       "- Nếu phải re-scrape mới cập nhật: ghi rõ trong evidence + note cho KH biết cần re-share/đợi cache",
       note="Nguồn: Task nhỏ r216, r232 + r238 (TC-NEW-05 do AI đề xuất trong bộ human: FB cache — re-scrape)."),

    tc("Preview & OGP", "UI-003", "Abnormal",
       "Share URL của event ĐÃ BỊ XÓA → không lỗi, mở ra thông báo event đã xóa",
       ADM + "\n- Đã share URL event G lên Facebook, sau đó xóa event G",
       "1. Ở Facebook bấm mở URL của event G đã xóa\n2. Quan sát trang mở ra\n"
       "3. Re-scrape URL đó bằng FB Sharing Debugger",
       "Event đã bị xóa khỏi hệ thống",
       "- Preview trên FB **không hiện lỗi trần** (không 500 / không trang trắng)\n"
       "- Mở URL: hiện thông báo event đã bị xóa / không khả dụng\n- Không lộ thông tin của event khác",
       note="Nguồn: Task nhỏ r217 và r233."),

    tc("Preview & OGP", "REG-SHARED-001", "Normal",
       "Regression — share link của 5 tính năng khác không bị ảnh hưởng bởi fix OGP event",
       ADM + "\n- Chuẩn bị link của 5 tính năng: form · booking salon · booking lesson · QR code · mua item",
       "1. Share từng link lên Facebook / Instagram / X\n2. Quan sát preview của từng link",
       "5 link × 3 kênh",
       "- Mỗi link hiện đúng preview của tính năng tương ứng\n"
       "- Không link nào bị mất preview / hiện nhầm ảnh sau khi fix OGP của event booking",
       note="Nguồn: Task nhỏ r241「Regression test — Check share link của các tính năng khác lên fb/instagram/X "
            "xem có bị lỗi hay không」. Ghi 'regression' theo quy chuẩn Loại case. ⚠ RULE-01: quan điểm `REG-SHARED-001` trong bộ này KHÔNG có loại case **Abnormal, Boundary** — lý do: corpus và spec không mô tả nhánh bất thường nào cho quan điểm này."),

    tc("Preview & OGP", "LIFF-ENTRY-001", "Abnormal",
       "Crawler và user thật nhận đúng trang khác nhau (UA detection)",
       ADM + "\n- Event E bất kỳ đã publish",
       "1. Mở URL bằng trình duyệt thật / LINE app (user)\n"
       "2. Mở URL bằng User-Agent `facebookexternalhit` (qua FB Debugger hoặc curl -A)\n"
       "3. So sánh nội dung 2 response",
       "UA thật vs UA `facebookexternalhit`",
       "- User thật: vào **trang đặt chỗ đầy đủ**, đặt chỗ được\n"
       "- Crawler: nhận **trang meta OGP nhẹ** (preview_url), KHÔNG phải trang booking",
       note="Nguồn: Task nhỏ r239 (TC-NEW-06 do AI đề xuất trong bộ human, Support #37932). "
            "⚠ Cơ chế UA detection cần Dev xác nhận là chủ đích — xem MT-22."),

    tc("Preview & OGP", "SEC-001", "Abnormal",
       "Share URL event disable / đã kết thúc → preview không lộ thông tin ngoài ý muốn",
       ADM + "\n- Event H ở trạng thái đã kết thúc (mọi 開催日 đã qua) hoặc bị tắt",
       "1. Share URL event H lên Facebook\n2. Quan sát preview\n"
       "3. Mở URL bằng LINE app (user thật)",
       "Event đã kết thúc / disable",
       "- Preview không lỗi và không lộ thông tin nội bộ (số booking, thông tin người tham gia)\n"
       "- User mở thấy đúng trạng thái: đã kết thúc / không khả dụng, không đặt chỗ được",
       note="Nguồn: Task nhỏ r240 (TC-NEW-07 do AI đề xuất trong bộ human)."),
]
