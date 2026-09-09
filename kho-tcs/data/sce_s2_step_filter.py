# -*- coding: utf-8 -*-
"""FA-009 ステップ配信 — Nhóm 10-12: Màn list step · Filter phân nhánh 配信対象 · 配信タイミング.

Nguồn: tab「Testcase」(master) · tab「improve sce 20/6」(20/6/2024, giới hạn 100 step + màn preview)
· tab「21/11」(order_number) · tab「text fix bug Kh」(Bug #32587 10/2025)
· tab「Job scenario」(Bug #32802 11/2025 — alert sửa time nhỏ hơn).
"""
from _common import tc

SCE = "- Đăng nhập admin (主管理者), bot A\n- Có scenario S1, đang ở màn list step /step-message/list-message/{S1}"
SCE_F = SCE + "\n- S1 đã có filter default 友だち全員(絞り込みなし) và 2 filter branch F-A, F-B"

S2 = [
    # ══════════════════ 10. Màn list step & phân trang ══════════════════
    tc("Màn list step & phân trang", "FUNC-001", "Normal",
       "Double click text ステップ配信一覧へ戻る → quay về màn list scenario, chỉ điều hướng 1 lần",
       SCE,
       "1. Double click nhanh text「ステップ配信一覧へ戻る」\n2. Quan sát trang được điều hướng tới",
       "—",
       "- Chỉ điều hướng 1 lần, về đúng màn list scenario /basic/scenario\n- Folder đang chọn giữ đúng như trước khi vào",
       note="Nguồn: r400"),

    tc("Màn list step & phân trang", "UI-FIELD-001", "Normal",
       "Màn tạo/list step: default filter = 友だち全員(絞り込みなし); hiển thị đúng folder và 管理名 của scenario",
       SCE + "\n- S1 tên「テストシナリオ」thuộc folder「F1」, chưa tạo filter branch nào",
       "1. Mở màn list step của S1\n2. Quan sát vùng 配信対象 (filter)\n3. Quan sát header: tên folder + 管理名",
       "S1「テストシナリオ」ở folder F1",
       "- Filter mặc định hiển thị「友だち全員(絞り込みなし)」\n"
       "- Header hiển thị đúng folder「F1」và 管理名「テストシナリオ」",
       note="Nguồn: r401, r402"),

    tc("Màn list step & phân trang", "LIST-001", "Normal",
       "Phân trang màn list step: default 50 bản ghi/trang, option chọn 50 / 100 / 200",
       SCE + "\n- Filter default của S1 có 60 step",
       "1. Mở màn list step\n2. Đếm số step hiển thị ở trang 1\n3. Mở selector số items/trang, liệt kê các option\n"
       "4. Click nút > sang trang 2 và đếm",
       "60 step trong 1 filter",
       "- Trang 1 hiển thị đúng 50 step\n- Selector có 3 option: 50 · 100 · 200 (default 50)\n- Trang 2 hiển thị 10 step còn lại",
       spec="Spec không ghi",
       note="⚠️ r709 ghi option 50/100/200, nhưng các TC phía sau (r862-r865, improve sce 20/6 r11-r12) chỉ test 50↔100 "
            "→ option 200 CHƯA CÓ TC, cần verify lại có thật không. Nguồn: r709, r859"),

    tc("Màn list step & phân trang", "LIST-001", "Normal",
       "Chuyển trang list step → data đúng trang đó, số thứ tự step (N通目) tiếp nối đúng",
       SCE + "\n- Filter default có 120 step",
       "1. Ở trang 1 (50 step), ghi lại step cuối cùng và số thứ tự\n2. Click > sang trang 2\n"
       "3. Kiểm tra step đầu trang 2 và số thứ tự\n4. Sang trang 3",
       "120 step, 50/trang → 3 trang",
       "- Data mỗi trang đúng, không lặp, không thiếu step\n"
       "- Số thứ tự N通目 ở trang 2 tiếp nối trang 1 (51通目, 52通目...), không reset về 1",
       note="Nguồn: r710, r711, r860, r861"),

    tc("Màn list step & phân trang", "LIST-001", "Normal",
       "Đang ở trang sau, đổi từ 50 → 100 bản ghi/trang: nếu tổng < 100 → về trang 1; nếu > 100 → còn 2 trang",
       SCE + "\n- Chuẩn bị 2 filter: F-A có 80 step; F-B có 150 step",
       "1. Ở F-A: sang trang 2 (50/trang) → đổi selector sang 100 → quan sát\n"
       "2. Ở F-B: sang trang 2 → đổi selector sang 100 → quan sát số trang, số thứ tự, time của từng step",
       "F-A: 80 step (< 100) · F-B: 150 step (> 100)",
       "- F-A: hiển thị trang 1 duy nhất với đủ 80 step\n"
       "- F-B: chia 2 trang (100 + 50); số thứ tự và thời gian gửi của step vẫn đúng, không lệch",
       note="Nguồn: r862, r863"),

    tc("Màn list step & phân trang", "STATE-CLEAN-001", "Normal",
       "Reset phân trang: filter 1 chọn 100/trang → sang trang 2 → quay lại trang 1 → về lại 50 bản ghi/trang",
       SCE + "\n- Filter F-A có 150 step",
       "1. Ở F-A chọn 100 bản ghi/trang\n2. Sang trang 2\n3. Quay lại trang 1\n4. Đếm số step hiển thị ở trang 1",
       "F-A: 150 step",
       "- Trang 1 hiển thị lại 50 bản ghi/trang (reset về default)",
       note="Nguồn: r864"),

    tc("Màn list step & phân trang", "STATE-001", "Abnormal",
       "Đổi số bản ghi từ 100 → 50 ở filter branch → phải GIỮ NGUYÊN filter đang chọn, không redirect về filter default",
       SCE_F + "\n- Đang đứng ở filter branch F-A (không phải filter default), đang để 100 bản ghi/trang",
       "1. Đứng ở filter F-A, chọn 100 bản ghi/trang\n2. Đổi selector từ 100 xuống 50\n"
       "3. Quan sát filter đang được chọn và danh sách step",
       "Filter F-A với > 50 step",
       "- Vẫn ở filter F-A, hiển thị step của F-A với 50 bản ghi/trang\n- KHÔNG bị nhảy về filter default 友だち全員",
       spec="Đã hỏi leader",
       note="MT-13 — corpus r875 và「improve sce 20/6」r12 đều đánh **NG**:『khi chuyển từ 100 về 50 đang redirect sang "
            "filter default』. TC dự kiến FAIL → cần raise bug. Nguồn: r875,「improve sce 20/6」r12"),

    tc("Màn list step & phân trang", "STATE-001", "Abnormal",
       "Đang ở trang 2 của filter branch → click sang filter default → dữ liệu không được rỗng",
       SCE_F + "\n- Filter F-A có 80 step (2 trang); filter default có 10 step",
       "1. Đứng ở F-A, sang trang 2\n2. Click sang filter default 友だち全員(絞り込みなし)\n3. Quan sát danh sách step",
       "F-A trang 2 → filter default (10 step)",
       "- Filter default hiển thị đủ 10 step, KHÔNG bị trống\n- Phân trang reset về trang 1",
       note="Nguồn:「21/11」r24 —『khi ở page 2 của filter khác default => click vào filter default => đang bị mất data』"),

    tc("Màn list step & phân trang", "BULK-LIMIT-001", "Boundary",
       "Giới hạn 100 step/filter: copy all vào 1 filter khi tổng DƯỚI 100 → success; khi VƯỢT 100 → cảnh báo",
       SCE_F + "\n- Filter đích F-A đã có 60 step; filter nguồn F-B có 30 step (case dưới max) và 50 step (case trên max)",
       "1. Ở F-A, dùng 一括引用登録 copy toàn bộ step từ F-B (30 step) → quan sát\n"
       "2. Chuẩn bị lại: F-A có 60 step, F-B có 50 step → copy toàn bộ → quan sát cảnh báo\n"
       "3. Đếm số step thực tế trong F-A sau mỗi lần",
       "Lần 1: 60 + 30 = 90 (≤ 100)\nLần 2: 60 + 50 = 110 (> 100)",
       "- Lần 1: copy success, F-A có 90 step\n"
       "- Lần 2: hiển thị cảnh báo「100以上登録できません。」, KHÔNG copy, F-A vẫn 60 step",
       spec="Đã hỏi leader",
       note="MT-14 — text cảnh báo trong corpus (06/2024) là「100以上登録できません。」nhưng spec BR-11 (feature-spec §7 mục 11 "
            "+ §9 Validation Rules) ghi「1つの配信対象に登録できる配信タイミングは100までです。」. Nguồn:「improve sce 20/6」r5-r6, r868-r869"),

    tc("Màn list step & phân trang", "BULK-LIMIT-001", "Boundary",
       "Filter đạt ĐÚNG 100 step: vẫn edit được time của step; nhiều filter cùng đạt 100 step vẫn hoạt động; start scenario friend nhận msg",
       SCE_F + "\n- Filter default có đúng 100 step; F-A cũng có đúng 100 step",
       "1. Ở filter default (100 step): edit time của 1 step → lưu\n2. Kiểm tra F-A cũng 100 step → mở màn, phân trang\n"
       "3. Start scenario cho 1 friend test\n4. Quan sát LINE app của friend + query `scenario_step_time`",
       "2 filter × 100 step",
       "- Edit time step thành công (không bị chặn bởi giới hạn 100)\n"
       "- Cả 2 filter đều mở được, phân trang đúng (2 trang / 50 bản ghi)\n"
       "- Friend nhận được message theo đúng timing của step",
       env="PRODUCTION",
       note="RULE-08: 100 step × nhiều filter là case hiệu năng → cần chạy PRODUCTION. Nguồn:「improve sce 20/6」r7-r10, r870-r873"),

    tc("Màn list step & phân trang", "PERF-LARGE-001", "Boundary",
       "Màn preview 一括プレビュー với filter 100 step → hiển thị 20 bản ghi đầu, click さらに20件表示 tải thêm đúng 20",
       SCE_F + "\n- Filter default có 100 step",
       "1. Mở màn preview (一括プレビュー)\n2. Đếm số step hiển thị lần đầu\n3. Click「さらに20件表示」\n"
       "4. Đếm lại, lặp tới khi hết 100 step",
       "100 step",
       "- Lần đầu hiển thị 20 bản ghi\n- Mỗi lần click「さらに20件表示」tải thêm đúng 20 bản ghi\n"
       "- Sau 5 lần hiển thị đủ 100 step, không lặp, không thiếu",
       note="Nguồn:「improve sce 20/6」r20-r21"),

    tc("Màn list step & phân trang", "FUNC-DATE-001", "Normal",
       "Màn preview: lọc theo mốc thời gian 全て表示 / 1週目 / 2週目 / 3週目 / 4週目 / カスタム → hiển thị đúng step trong mốc",
       SCE_F + "\n- Filter default có step rải từ ngày 0 đến ngày 30",
       "1. Mở màn preview, chọn 1 filter\n2. Lần lượt chọn từng mốc: 全て表示 · 1週目（開始~7日目）· 2週目（8~14日目）· "
       "3週目（15~21日目）· 4週目（22~28日目）\n3. Với mỗi mốc, đối chiếu step hiển thị với ngày setting",
       "Step ở các ngày 0, 3, 7, 8, 12, 15, 20, 22, 27, 30",
       "- 全て表示: đủ 10 step\n- 1週目: step ngày 0, 3, 7\n- 2週目: step ngày 8, 12\n"
       "- 3週目: step ngày 15, 20\n- 4週目: step ngày 22, 27\n- Step ngày 30 chỉ hiện ở 全て表示 hoặc カスタム",
       note="Nguồn:「improve sce 20/6」r22-r26"),

    tc("Màn list step & phân trang", "FUNC-DATE-001", "Boundary",
       "Màn preview カスタム: từ ngày < đến ngày → success; từ ngày = đến ngày → success; 0 ngày → 0 ngày → hiển thị data trong ngày",
       SCE_F + "\n- Filter default có step ở ngày 0, 3, 7, 15",
       "1. Chọn カスタム, nhập từ ngày 0 đến ngày 7 → quan sát\n2. Nhập từ 3 đến 3 → quan sát\n3. Nhập từ 0 đến 0 → quan sát",
       "Lần 1: 0 → 7\nLần 2: 3 → 3\nLần 3: 0 → 0",
       "- Lần 1: hiển thị step ngày 0, 3, 7\n- Lần 2: chỉ hiển thị step ngày 3\n- Lần 3: chỉ hiển thị step ngày 0 (trong ngày)",
       note="Nguồn:「improve sce 20/6」r28-r29, r32"),

    tc("Màn list step & phân trang", "DATA-INPUT-001", "Abnormal",
       "Màn preview カスタム: từ ngày > đến ngày, hoặc nhập text / ký tự / số âm → fail",
       SCE_F,
       "1. Chọn カスタム, nhập từ 7 đến 0 → quan sát\n2. Nhập text「abc」→ quan sát\n"
       "3. Nhập ký tự đặc biệt「@#」→ quan sát\n4. Nhập số âm「-1」→ quan sát",
       "Lần 1: 7 → 0\nLần 2:「abc」\nLần 3:「@#」\nLần 4:「-1」",
       "- Cả 4 lần đều FAIL: không lọc được, hiển thị cảnh báo / không nhận giá trị\n- Không crash màn preview",
       note="4 input cùng 1 kết quả (fail) → giữ chung. Nguồn:「improve sce 20/6」r30-r31"),

    tc("Màn list step & phân trang", "FUNC-001", "Normal",
       "Màn preview: click icon cây bút → sang màn edit step; click button アクションを編集する → sang màn edit action",
       SCE_F + "\n- Filter default có ≥ 2 step, 1 step có action",
       "1. Mở màn preview\n2. Click icon hình cây bút của 1 step\n3. Quan sát màn được mở, sửa msg / time / action → lưu\n"
       "4. Kiểm tra 最終編集日時 của step\n5. Quay lại preview, click button「アクションを編集する」",
       "Step có 1 message text và 1 action gắn tag",
       "- Bước 2-3: mở đúng màn edit step, sửa được message/time/action và lưu thành công\n"
       "- Bước 4: 最終編集日時 cập nhật đúng\n- Bước 5: mở đúng màn edit action",
       note="Nguồn:「improve sce 20/6」r33-r36"),

    tc("Màn list step & phân trang", "UI-002", "Normal",
       "Màn preview: check UI, modal filter (dữ liệu, bỏ tick, nhiều filter có scroll), button back ステップ編集画面に戻る, đóng/mở phần trên",
       SCE_F + "\n- S1 có 6 filter branch",
       "1. Mở màn preview, đối chiếu UI với design\n2. Mở modal filter → kiểm tra dữ liệu hiển thị\n"
       "3. Bỏ tick 1 filter → quan sát\n4. Scroll danh sách 6 filter trong modal\n"
       "5. Click button「ステップ編集画面に戻る」\n6. Click đóng/mở phần trên của màn preview",
       "6 filter branch",
       "- UI khớp design\n- Modal filter hiển thị đủ 6 filter, có scroll\n- Bỏ tick filter → step của filter đó không hiển thị\n"
       "- Button back quay về đúng màn chỉnh sửa bước\n- Đóng/mở phần trên hoạt động bình thường",
       note="Nguồn:「improve sce 20/6」r14-r19"),

    tc("Màn list step & phân trang", "CONC-001", "Abnormal",
       "Màn preview: double click các button → chỉ tính 1 lần",
       SCE_F,
       "1. Double click nhanh từng button trên màn preview (さらに20件表示, ステップ編集画面に戻る, アクションを編集する)\n"
       "2. Quan sát số lần thực thi",
       "—",
       "- Mỗi button chỉ thực thi 1 lần, không nhân đôi kết quả",
       note="Nguồn:「improve sce 20/6」r38"),

    # ══════════════════ 11. Filter phân nhánh 配信対象 ══════════════════
    tc("Filter phân nhánh 配信対象", "FUNC-001", "Normal",
       "Click 絞込みオプション → mở phần add filter, default 友だち全員(絞り込みなし); DB ghi filter_manager type='scenario'",
       SCE + "\n- S1 chưa có filter branch nào",
       "1. Double click nhanh text/mũi tên「絞込みオプション」\n2. Quan sát phần add filter và hướng mũi tên\n"
       "3. Thêm 1 filter branch, đặt tên và nội dung → lưu\n"
       "4. Query `filter_manager` WHERE parent_id = <S1> AND type = 'scenario'\n"
       "5. Query `filters_v2` WHERE parent_type = 'filter_manager' AND parent_id = <filter_manager.id>",
       "Filter branch「絞込み条件1」, điều kiện: có tag「テストタグ」",
       "- Chỉ mở 1 lần; phần add filter hiện ra, default「友だち全員(絞り込みなし)」, mũi tên chuyển hướng LÊN\n"
       "- DB `filter_manager`: name = tên filter, type = 'scenario', parent_id = id scenario\n"
       "- DB `filters_v2`: lưu data chi tiết của điều kiện filter",
       note="Nguồn: r403"),

    tc("Filter phân nhánh 配信対象", "LIST-001", "Normal",
       "Filter default 友だち全員(絞り込みなし) → hiển thị các step KHÔNG có filter (filter_manager_id = NULL)",
       SCE_F + "\n- Filter default có 3 step; F-A có 2 step",
       "1. Chọn filter default\n2. Đếm số step hiển thị\n3. Query `step_message` WHERE scenario_id = <S1> AND filter_manager_id IS NULL",
       "Filter default: 3 step · F-A: 2 step",
       "- Chỉ hiển thị 3 step của filter default, KHÔNG hiển thị step của F-A\n- DB: 3 bản ghi step_message có filter_manager_id NULL",
       note="Nguồn: r404"),

    tc("Filter phân nhánh 配信対象", "FUNC-MULTI-001", "Normal",
       "Click 絞り込み条件追加 N lần → tạo đúng N filter branch, mỗi cái có ô nhập tên + nội dung filter",
       SCE,
       "1. Double click nhanh「絞り込み条件追加」→ đếm số filter tạo ra\n2. Click thêm 2 lần nữa\n3. Đếm tổng số filter branch",
       "Click 3 lần (trong đó 1 lần double click)",
       "- Double click chỉ tạo 1 filter\n- Tổng cộng có đúng 3 filter branch, mỗi cái có ô nhập tên điều kiện và vùng nội dung filter",
       note="Nguồn: r405"),

    tc("Filter phân nhánh 配信対象", "UI-FIELD-001", "Normal",
       "Tên điều kiện filter: default hiển thị sẵn 絞込み条件N; chấp nhận tiếng Nhật và ký tự đặc biệt",
       SCE,
       "1. Thêm filter branch mới → quan sát tên mặc định\n2. Đổi tên thành tiếng Nhật「タグ絞込」→ lưu\n"
       "3. Đổi tên thành ký tự đặc biệt「@#$%」→ lưu\n4. Query `filter_manager`.`name`",
       "Default:「絞込み条件1」· JP:「タグ絞込」· đặc biệt:「@#$%」",
       "- Default hiển thị sẵn「絞込み条件1」(muốn đổi thì vào edit)\n"
       "- Cả tiếng Nhật và ký tự đặc biệt đều được CHẤP NHẬN, lưu đúng vào `filter_manager.name`",
       note="Nguồn: r406, r408, r410"),

    tc("Filter phân nhánh 配信対象", "DATA-INPUT-001", "Boundary",
       "Tên điều kiện filter: tối đa 10 ký tự → nhập 11 ký tự phải bị chặn/cảnh báo; space đầu-cuối phải được trim",
       SCE,
       "1. Thêm filter branch, nhập 11 ký tự vào tên điều kiện → lưu\n2. Nhập đúng 10 ký tự → lưu\n"
       "3. Nhập「  タグ  」(có space đầu/cuối) → lưu\n4. Query `filter_manager`.`name`",
       "Lần 1: 11 ký tự\nLần 2: 10 ký tự「あいうえおかきくけこ」\nLần 3:「  タグ  」",
       "- 11 ký tự: bị chặn hoặc hiển thị cảnh báo, KHÔNG lưu\n- 10 ký tự: lưu thành công\n"
       "- DB lưu「タグ」(đã trim space đầu/cuối)",
       spec="Đã hỏi leader",
       note="MT-11 — corpus r407 (max 10 ký tự) và r409 (trim) đều đánh **NG**; r335/r336 khi EDIT filter cũng NG. "
            "TC dự kiến FAIL → cần raise bug. Spec không ghi giới hạn 10 ký tự này. Nguồn: r407, r409, r335, r336"),

    tc("Filter phân nhánh 配信対象", "FUNC-002", "Normal",
       "Edit filter: mở 絞込みオプション → hiển thị đầy đủ chính xác thông tin filter đang chọn; sửa nội dung filter → lưu đúng",
       SCE_F + "\n- Filter F-A có điều kiện: có tag「A」AND ngày kết bạn trong 7 ngày",
       "1. Chọn F-A, click「絞込みオプション」mở phần detail\n2. Đối chiếu điều kiện hiển thị với điều kiện đã set\n"
       "3. Sửa nội dung filter: đổi tag「A」thành tag「B」→ lưu\n"
       "4. Query `filters_v2` WHERE parent_type = 'filter_manager' AND parent_id = <F-A>",
       "F-A: tag A AND ngày kết bạn ≤ 7 ngày → đổi thành tag B",
       "- Bước 2: hiển thị đầy đủ, chính xác 2 điều kiện\n"
       "- Bước 3-4: nội dung filter cập nhật thành tag B, `filters_v2`.`data` lưu đúng giá trị mới",
       note="Nguồn: r412, r414, r415, r853"),

    tc("Filter phân nhánh 配信対象", "STATE-001", "Abnormal",
       "Edit TÊN điều kiện filter → nội dung filter phải giữ nguyên, KHÔNG bị mất",
       SCE_F + "\n- Filter F-A có tên「条件A」và điều kiện: có tag「テストタグ」",
       "1. Chọn F-A, sửa tên điều kiện từ「条件A」thành「条件A改」\n2. QUAN SÁT vùng nội dung filter (chưa reload)\n"
       "3. Reload trang → quan sát lại nội dung filter",
       "Đổi tên「条件A」→「条件A改」",
       "- Ngay sau khi đổi tên: nội dung filter (tag「テストタグ」) VẪN HIỂN THỊ, không bị trắng\n"
       "- Sau reload: nội dung filter vẫn đúng",
       spec="Đã hỏi leader",
       note="MT-15 — corpus r413 đánh OK nhưng ghi chú『edit tên đk filter mất nội dung filter, reset mới hiển thị lại nd』. "
            "TC dự kiến FAIL → cần raise bug. Nguồn: r413"),

    tc("Filter phân nhánh 配信対象", "FUNC-004", "Abnormal",
       "Filter default 友だち全員(絞り込みなし) KHÔNG có chức năng xoá",
       SCE_F,
       "1. Chọn filter default\n2. Tìm nút/icon xoá filter\n3. Thử thao tác xoá (nếu có)",
       "Filter default",
       "- KHÔNG hiển thị nút/icon xoá cho filter default\n- Không có cách nào xoá filter default khỏi scenario",
       note="Nguồn: r417"),

    tc("Filter phân nhánh 配信対象", "MSG-001", "Normal",
       "Xoá filter branch → hiện alert cảnh báo xoá luôn message và action; click OK → xoá, focus về filter default",
       SCE_F + "\n- Filter F-A có 3 step, mỗi step có message + action",
       "1. Chọn F-A, click xoá filter「配信対象削除」\n2. Đọc nguyên văn text alert\n3. Click OK\n"
       "4. Quan sát danh sách filter và filter đang được focus\n"
       "5. Query `filter_manager` / `filters_v2` / `step_message` WHERE filter_manager_id = <F-A>",
       "F-A với 3 step (message + action)",
       "- Alert hiển thị đúng nguyên văn:「絞り込み条件を削除すると、この配信対象に対して登録されている メッセージやアクションも全て削除されますがよろしいですか？」\n"
       "- Sau OK: F-A biến mất khỏi danh sách filter\n- Hệ thống focus về filter default「友だち全員(絞り込みなし)」\n"
       "- DB: filter_manager, filters_v2 và toàn bộ 3 step_message của F-A bị xoá",
       spec="Đã hỏi leader",
       note="MT-16 — corpus r421 đánh OK nhưng ghi chú『đang focus filter bên cạnh』(không phải filter default). "
            "Quy tắc focus sau khi xoá filter chưa chốt. Nguồn: r420, r421, r423, r854"),

    tc("Filter phân nhánh 配信対象", "STATE-CLEAN-001", "Normal",
       "Alert xoá filter → click Cancel → đóng popup, filter vẫn còn nguyên cùng toàn bộ step",
       SCE_F + "\n- Filter F-A có 3 step",
       "1. Chọn F-A, click xoá filter\n2. Click Cancel ở alert\n3. Kiểm tra danh sách filter và số step của F-A",
       "F-A với 3 step",
       "- Popup đóng, F-A vẫn còn trong danh sách\n- 3 step của F-A còn nguyên",
       note="Nguồn: r422"),

    tc("Filter phân nhánh 配信対象", "UI-002", "Abnormal",
       "Click icon xoá filter chỉ 1 LẦN → phải hiện ngay popup confirm (không phải click 2 lần)",
       SCE_F + "\n- Filter F-A vừa được add trong phiên hiện tại (chưa reload)",
       "1. Add filter F-A mới, không reload trang\n2. Click 1 lần vào icon xoá filter F-A\n3. Quan sát có popup confirm hay không",
       "Filter vừa add trong cùng phiên",
       "- Popup confirm xuất hiện ngay sau click LẦN 1",
       spec="Đã hỏi leader",
       note="MT-17 — corpus r418 đánh OK nhưng ghi chú『đang phải click đến lần 2 mới hiển thị popup confirm xóa』, "
            "chỉ xảy ra với filter vừa add (r419 filter cũ thì bình thường). Nguồn: r418, r419"),

    tc("Filter phân nhánh 配信対象", "DATA-CASCADE-001", "Abnormal",
       "Xoá filter của scenario ĐANG start cho friend → step pending của filter đó bị xoá, friend không nhận thêm msg của nhánh này",
       SCE_F + "\n- S1 đang có 5 friend chạy; filter F-A có 2 step chưa tới giờ gửi",
       "1. Ghi lại `scenario_step_time` (status = 0) của các step thuộc F-A\n2. Xoá filter F-A → OK\n"
       "3. Query lại `scenario_step_time` của các step đó\n4. Chờ qua thời điểm 2 step → kiểm tra LINE app của 5 friend\n"
       "5. Kiểm tra `scenario_lineuser`.`is_following` của 5 friend",
       "5 friend đang chạy; F-A còn 2 step pending",
       "- Bản ghi `scenario_step_time` (status = 0) của step thuộc F-A bị XOÁ\n"
       "- 5 friend KHÔNG nhận message của 2 step thuộc F-A\n"
       "- Nếu không còn step nào khác pending: `scenario_lineuser.is_following` chuyển sang 2",
       spec="Đã hỏi leader",
       note="MT-18 — corpus r424 chỉ ghi『Cần Confirm — xóa luôn』, không có kết quả mong đợi chi tiết. "
            "Kết quả mong đợi suy từ spec BR-06 + logic-spec `deleteFilterManager`. CẦN LEADER XÁC NHẬN. Nguồn: r424"),

    tc("Filter phân nhánh 配信対象", "FUNC-001", "Normal",
       "Add filter CÓ nội dung → mở màn edit filter luôn, lưu success thì mở button add step",
       SCE,
       "1. Click「絞り込み条件追加」\n2. Quan sát: hệ thống có tự mở màn edit filter không\n"
       "3. Nhập nội dung filter (có tag「A」) → lưu\n4. Quan sát button thêm 配信タイミング\n"
       "5. Query `filters_v2` WHERE parent_id = <filter_manager.id>",
       "Điều kiện: có tag「A」",
       "- Sau khi add, hệ thống MỞ NGAY màn edit filter\n- Lưu filter success → button add step (配信タイミングを追加する) HIỆN RA\n"
       "- DB: `filters_v2` có bản ghi với parent_id = filter_manager.id",
       note="Nguồn: r847"),

    tc("Filter phân nhánh 配信対象", "DATA-INPUT-001", "Abnormal",
       "Add filter KHÔNG có nội dung → alert không cho save; không lưu DB; ẩn button add step",
       SCE,
       "1. Click「絞り込み条件追加」→ màn edit filter mở ra\n2. Không nhập nội dung filter nào, bấm lưu\n"
       "3. Quan sát alert và button add step\n4. Query `filters_v2` WHERE parent_id = <filter_manager.id>",
       "(không nhập điều kiện filter nào)",
       "- Hiển thị alert không cho save\n- DB `filters_v2`: KHÔNG có bản ghi\n- Button add step bị ẨN",
       note="Nguồn: r848"),

    tc("Filter phân nhánh 配信対象", "STATE-DEP-001", "Abnormal",
       "Xoá trắng nội dung filter rồi click sang filter khác / add filter mới → hiện alert; OK = xoá cả filter, Cancel = ở lại",
       SCE_F + "\n- Filter F-A đang có điều kiện: tag「A」",
       "1. Chọn F-A, xoá trắng nội dung filter, KHÔNG nhập nội dung mới\n"
       "2. Click sang filter F-B → quan sát alert → click OK\n3. Kiểm tra danh sách filter + DB\n"
       "4. Lặp lại với 1 filter khác, lần này click Cancel → quan sát",
       "F-A: xoá trắng điều kiện tag A",
       "- Hiện alert cảnh báo\n- Click OK: XOÁ LUÔN filter đó (cả filter_manager và filters_v2)\n"
       "- Click Cancel: đóng popup, vẫn ở filter đó chờ nhập nội dung filter",
       note="Nguồn: r849"),

    tc("Filter phân nhánh 配信対象", "STATE-DEP-001", "Abnormal",
       "Xoá trắng nội dung filter rồi click back / ステップ配信一覧へ戻る → validate; OK = back và xoá filter",
       SCE_F + "\n- Filter F-A đang có điều kiện: tag「A」",
       "1. Chọn F-A, xoá trắng nội dung filter\n2. Click nút back trình duyệt hoặc「ステップ配信一覧へ戻る」\n"
       "3. Quan sát validate → click OK\n4. Quay lại màn step, kiểm tra danh sách filter + DB",
       "F-A: xoá trắng điều kiện",
       "- Hiện validate cảnh báo\n- Click OK: back ra ngoài VÀ xoá luôn filter F-A\n- DB: filter_manager + filters_v2 của F-A bị xoá",
       note="Nguồn: r850"),

    tc("Filter phân nhánh 配信対象", "STATE-DEP-001", "Abnormal",
       "Reset / tự động back / back ở ngoài màn detail → CHẤP NHẬN filter không có nội dung; start scenario thì filter rỗng gửi cho ALL friend",
       SCE_F + "\n- Filter F-A xoá trắng nội dung, thoát qua đường reset/tự động back",
       "1. Chọn F-A, xoá trắng nội dung filter\n2. Thoát qua đường reset / tự động back / back ở ngoài màn detail\n"
       "3. Quay lại màn step → kiểm tra F-A còn tồn tại không, nội dung filter thế nào\n"
       "4. Thêm 1 step vào F-A với message text\n5. Start scenario cho 3 friend có thuộc tính khác nhau\n"
       "6. Kiểm tra LINE app của cả 3 friend",
       "3 friend: friend1 có tag A, friend2 có tag B, friend3 không tag",
       "- F-A vẫn tồn tại với nội dung filter RỖNG (được chấp nhận)\n"
       "- Khi start: CẢ 3 friend đều nhận được message của F-A (filter rỗng = không lọc)",
       spec="Đã hỏi leader",
       note="MT-19 — 3 lối thoát khỏi màn filter cho 3 hành vi KHÁC nhau (r849 alert+xoá · r850 validate+xoá · "
            "r851 chấp nhận filter rỗng). Spec không ghi quy tắc này. Nguồn: r851, r852"),

    tc("Filter phân nhánh 配信対象", "FUNC-001", "Normal",
       "Start scenario có filter mới add → chỉ friend thoả mãn điều kiện filter nhận được message",
       SCE_F + "\n- Filter F-A: điều kiện có tag「A」; F-A có 1 step send ngay với message text",
       "1. Chuẩn bị 3 friend: friend1 có tag A, friend2 có tag B, friend3 không tag\n"
       "2. Start scenario S1 cho cả 3 friend\n3. Kiểm tra LINE app của từng friend\n"
       "4. Kiểm tra trigger ở màn chat 1:1 của từng friend",
       "friend1 (tag A) · friend2 (tag B) · friend3 (không tag)",
       "- friend1: NHẬN được message của F-A\n- friend2, friend3: KHÔNG nhận message của F-A\n"
       "- Chat 1:1 của friend2/friend3 hiển thị:「このメッセージは配信（絞り込み）対象外のため送信されていません。」",
       note="Nguồn: r855, r1057"),

    tc("Filter phân nhánh 配信対象", "DATA-MIG-001", "Normal",
       "Scenario data cũ: step KHÔNG filter → gom vào folder default; step CÙNG điều kiện filter → gộp 1 folder filter; KHÁC điều kiện → tách folder riêng",
       SCE + "\n- Bot có scenario data cũ (tạo trước bản improve filter) gồm: 3 step không filter, "
       "2 step cùng điều kiện filter X, 2 step khác điều kiện filter Y",
       "1. Mở màn list step của scenario data cũ\n2. Quan sát danh sách filter branch được sinh ra\n"
       "3. Mở từng filter branch, đếm số step",
       "3 step no filter · 2 step filter X · 2 step filter Y",
       "- Folder default (no filter): 3 step\n- Sinh ra 1 folder filter cho điều kiện X chứa 2 step\n"
       "- Sinh ra 1 folder filter riêng cho điều kiện Y chứa 2 step",
       note="⚠️ Corpus r19 ghi chú:『khi mới vào mh edit => ko hợp lý. Do đang chọn thẳng vào phần no filter "
            "=> nên hiển thị tất cả các phần filter ra và marker đang chọn vào no filter』. Nguồn: r19-r21"),

    tc("Filter phân nhánh 配信対象", "FUNC-UNIQ-001", "Normal",
       "Edit filter: 4 tổ hợp trùng/khác tên × trùng/khác nội dung → đều lưu được (filter không unique)",
       SCE_F + "\n- Đã có filter「条件A」với điều kiện tag X",
       "1. Tạo filter mới tên「条件B」, nội dung tag Y (khác tên khác nội dung) → lưu\n"
       "2. Tạo filter「条件C」, nội dung tag X (khác tên cùng nội dung) → lưu\n"
       "3. Tạo filter「条件A」, nội dung tag X (cùng tên cùng nội dung) → lưu\n"
       "4. Tạo filter「条件A」, nội dung tag Z (cùng tên khác nội dung) → lưu\n"
       "5. Đếm số filter branch + query `filter_manager`",
       "4 tổ hợp: khác/khác · khác/cùng · cùng/cùng · cùng/khác",
       "- Cả 4 trường hợp đều lưu THÀNH CÔNG, không báo lỗi trùng\n- Có tổng 5 filter branch, mỗi cái 1 id riêng",
       note="4 input cùng 1 kết quả → giữ chung. Nguồn: r337-r340"),

    tc("Filter phân nhánh 配信対象", "DATA-INPUT-001", "Abnormal",
       "Edit filter để trống nội dung → validate không cho lưu",
       SCE_F + "\n- Filter F-A có điều kiện tag A",
       "1. Chọn F-A, mở edit filter, xoá hết điều kiện\n2. Bấm lưu\n3. Quan sát validate",
       "(để trống điều kiện)",
       "- Hiển thị validate, không cho lưu filter rỗng",
       note="Nguồn: r334"),

    tc("Filter phân nhánh 配信対象", "UI-002", "Normal",
       "Nội dung filter hiển thị đúng với từ khoá đã chọn; popup filter đầy đủ và hoạt động tốt; đóng màn detail filter bình thường",
       SCE_F,
       "1. Mở popup filter, chọn điều kiện: tag「テストタグ」+ ngày kết bạn 7 ngày\n2. Lưu\n"
       "3. Quan sát text preview nội dung filter hiển thị ngoài\n4. Click đóng màn detail filter",
       "Điều kiện: tag「テストタグ」AND ngày kết bạn ≤ 7 ngày",
       "- Text preview hiển thị ĐÚNG từ khoá đã chọn (tên tag, số ngày)\n"
       "- Popup filter có đủ các nhóm điều kiện, thao tác được\n- Đóng màn detail filter bình thường, không mất data đã lưu",
       note="Nguồn: r341, r411, r416"),

    # ══════════════════ 12. 配信タイミング — thêm & sửa ══════════════════
    tc("配信タイミング — thêm & sửa", "UI-002", "Normal",
       "Tooltip nút 配信タイミングを追加する: mouse over hiển thị đúng text hướng dẫn",
       SCE + "\n- S1 chưa có step nào",
       "1. Mouse over nút「配信タイミングを追加する」\n2. Đọc nguyên văn tooltip, đối chiếu design",
       "—",
       "- Tooltip hiển thị:「配信タイミングを追加して、メッセージの登録をしましょう」, khớp design",
       note="Nguồn: r425"),

    tc("配信タイミング — thêm & sửa", "STATE-001", "Normal",
       "Tooltip 配信タイミング: sau khi ấn X tắt tooltip → sang màn khác quay lại / logout-login đều KHÔNG hiện lại; account khác vẫn hiện",
       SCE + "\n- Tài khoản admin A chưa từng tắt tooltip; có sẵn tài khoản admin B",
       "1. Tài khoản A: chưa ấn X → sang màn khác rồi quay lại, mouse over → quan sát tooltip\n"
       "2. Tài khoản A: logout → login lại, mouse over → quan sát\n"
       "3. Tài khoản A: ấn X tắt tooltip → sang màn khác quay lại, mouse over → quan sát\n"
       "4. Tài khoản A: logout → login lại, mouse over → quan sát\n"
       "5. Login tài khoản B, mouse over → quan sát",
       "Tài khoản A (đã ấn X) và tài khoản B (chưa ấn X)",
       "- Bước 1, 2 (chưa ấn X): tooltip VẪN hiện\n- Bước 3, 4 (đã ấn X): tooltip KHÔNG hiện nữa\n"
       "- Bước 5 (account khác): tooltip VẪN hiện",
       spec="Spec không ghi",
       note="⚠️ Corpus r426-r430 đều để『Cần Confirm / để làm sau』, CHƯA TEST. Spec logic-spec `markCloseAlert` ghi "
            "『Insert setting_alert với user_id = Auth::id() và key』→ đúng theo TC này (lưu theo user). "
            "Đây là **TC lấp Gap** — cần Leader xác nhận trước khi chạy. Nguồn: r426-r430"),

    tc("配信タイミング — thêm & sửa", "UI-001", "Normal",
       "Double click 配信タイミングを追加する → chỉ mở 1 popup 配信タイミング選択, default chọn 日時で指定",
       SCE,
       "1. Double click nhanh nút「配信タイミングを追加する」\n2. Đếm số popup mở ra\n"
       "3. Quan sát option nào được chọn mặc định + đối chiếu design",
       "—",
       "- Chỉ mở ĐÚNG 1 popup「配信タイミング選択」\n- Popup khớp design, default chọn「日時で指定」",
       note="Nguồn: r431, r432"),

    tc("配信タイミング — thêm & sửa", "FUNC-UNIQ-001", "Abnormal",
       "Trong 1 filter chỉ được tạo ĐÚNG 1 step「ステップ開始直後」(send ngay)",
       SCE_F + "\n- Filter default đã có 1 step「ステップ開始直後」",
       "1. Ở filter default, click「配信タイミングを追加する」\n2. Quan sát option「ステップ開始直後」\n"
       "3. Nếu chọn được thì bấm 決定 → quan sát kết quả\n4. Chuyển sang filter F-A, thử tạo step「ステップ開始直後」",
       "Filter default: đã có 1 step send ngay · F-A: chưa có step send ngay",
       "- Ở filter default: option「ステップ開始直後」bị DISABLE hoặc báo lỗi, không tạo được step thứ 2\n"
       "- Ở filter F-A: tạo được step「ステップ開始直後」bình thường (giới hạn theo TỪNG filter, không theo scenario)",
       spec="Đã hỏi leader",
       note="MT-20 — corpus MÂU THUẪN NỘI BỘ: r433/r459 ghi『trong 1 ground scenario chỉ được 1 lần chọn send ngay』"
            "(theo SCENARIO), r800 ghi『mỗi filter cho phép tạo 1 send ngay』(theo FILTER). Spec BR-03 dùng khoá unique "
            "(delay_type, start_day, start_time, filter_manager_id) → nghiêng về theo FILTER. Nguồn: r433, r459, r800"),

    tc("配信タイミング — thêm & sửa", "FUNC-DATE-001", "Normal",
       "Kiểu 日時で指定 (delay_type=0): tạo step trong ngày start (0日後), khác ngày (N日後), và 0日後00:00",
       SCE,
       "1. Tạo step「日時で指定」với ステップ開始から = 0 ngày, giờ 18:00 → lưu\n"
       "2. Tạo step「日時で指定」với 3 ngày, giờ 09:30 → lưu\n3. Tạo step「日時で指定」với 0 ngày, giờ 00:00 → lưu\n"
       "4. Query `step_message` WHERE scenario_id = <S1>: delay_type, start_day, start_time",
       "Lần 1: 0日後 18:00\nLần 2: 3日後 09:30\nLần 3: 0日後 00:00",
       "- Cả 3 step tạo thành công, hiển thị đúng ở màn list step\n"
       "- DB: delay_type = 0; start_day = 0 / 3 / 0; start_time = '18:00:00' / '09:30:00' / '00:00:00'",
       note="3 input cùng 1 kết quả (đều lưu OK) → giữ chung. Nguồn: r434-r436, r23"),

    tc("配信タイミング — thêm & sửa", "DATA-DB-001", "Normal",
       "DB lưu 3 loại timing: send ngay → start_day/start_time = NULL; 日時で指定 → start_day = N, start_time = HH:MM:SS; 経過時間 → start_day = NULL, start_time = HH:MM:SS",
       SCE + "\n- Tạo 3 step đủ 3 loại timing",
       "1. Tạo step「ステップ開始直後」\n2. Tạo step「日時で指定」2日後 15:30\n3. Tạo step「経過時間で指定」05時間20分後\n"
       "4. Query `step_message` WHERE scenario_id = <S1>: delay_type, start_day, start_time",
       "3 step: send ngay · 2日後15:30 · 05時間20分後",
       "- Step 1: delay_type = 1, start_day = NULL, start_time = NULL\n"
       "- Step 2: delay_type = 0, start_day = 2, start_time = '15:30:00'\n"
       "- Step 3: delay_type = 2, start_day = NULL, start_time = '05:20:00'",
       spec="Đã hỏi leader",
       note="MT-21 — `web/logic-spec.md` BR-03 và bảng trường StepMessage ghi delay_type=2 lưu start_time dạng "
            "**'mm:ss:00' (phút:giây)**; còn `feature-spec.md` §6 và `db/db-mapping.md:86,109` ghi **'HH:MM:00' (giờ:phút)**. "
            "Corpus (Feature #30571) chứng minh là GIỜ:PHÚT. Nguồn: r22-r24, r989-r994"),

    tc("配信タイミング — thêm & sửa", "DATA-INPUT-001", "Abnormal",
       "Kiểu 経過時間で指定: nhập 00 giờ 00 phút → validate, không tạo được step",
       SCE,
       "1. Click「配信タイミングを追加する」→ chọn「経過時間で指定」\n2. Nhập 00 giờ 00 phút\n3. Bấm 決定",
       "00時間00分後",
       "- Hiển thị validate, KHÔNG tạo step\n- DB không có bản ghi step_message mới",
       note="Nguồn: r438"),

    tc("配信タイミング — thêm & sửa", "UI-001", "Normal",
       "Feature #30571: màu chữ time ở modal add timing chuyển thành #222222 cho cả 2 loại; label 経過時間 update 24 → 72 giờ",
       SCE,
       "1. Mở modal「配信タイミング選択」\n2. Dùng DevTools kiểm tra màu chữ của phần time loại「日時で指定」\n"
       "3. Kiểm tra màu chữ phần time loại「経過時間で指定」\n4. Đọc label/hint giới hạn giờ\n"
       "5. Mở màn ở folder filter → kiểm tra đã apply UI mới chưa",
       "—",
       "- Cả 2 loại time đều có màu chữ #222222\n- Label giới hạn hiển thị 72 (không còn 24); giới hạn phút hiển thị 72h00 (không còn 23h59)\n"
       "- Folder filter cũng đã apply UI mới",
       note="Feature #30571 (03-07-2025). Evidence: DevTools + ảnh chụp. Nguồn: r984-r987"),

    tc("配信タイミング — thêm & sửa", "DATA-INPUT-001", "Boundary",
       "Feature #30571: 経過時間で指定 nhập trong dải hợp lệ 00:01 → 72:00 → lưu đúng vào start_time",
       SCE,
       "1. Tạo lần lượt 6 step「経過時間で指定」với các giá trị dưới\n2. Sau mỗi lần, mở màn detail kiểm tra hiển thị\n"
       "3. Query `step_message`.`start_time` của từng step",
       "① 00 giờ 01 phút → 00:01\n② 01 giờ 00 phút → 01:00\n③ 23 giờ 59 phút → 23:59\n"
       "④ 24 giờ 00 phút → 24:00\n⑤ 47 giờ 59 phút → 47:59\n⑥ 72 giờ 00 phút → 72:00",
       "- Cả 6 giá trị đều tạo step THÀNH CÔNG, hiển thị đúng ở màn detail\n"
       "- DB `step_message`.`start_time` lưu đúng: 00:01 · 01:00 · 23:59 · 24:00 · 47:59 · 72:00",
       spec="Spec không ghi",
       note="Giới hạn 72h là kết quả Feature #30571 (03-07-2025) — **spec KHÔNG ghi ở bất kỳ đâu** (MT-22). "
            "6 giá trị cùng 1 kết quả (lưu OK) → giữ chung. Nguồn: r986, r989-r994"),

    tc("配信タイミング — thêm & sửa", "DATA-INPUT-001", "Boundary",
       "Feature #30571: 経過時間で指定 nhập VƯỢT 72 giờ (72:01 và 73:00) → báo lỗi, không tạo step",
       SCE,
       "1. Tạo step「経過時間で指定」nhập 72 giờ 01 phút → bấm 決定\n2. Nhập 73 giờ 00 phút → bấm 決定\n"
       "3. Query `step_message` kiểm tra không có bản ghi mới",
       "① 72 giờ 01 phút\n② 73 giờ 00 phút",
       "- Cả 2 lần đều BÁO LỖI, không tạo step\n- DB không có bản ghi step_message mới",
       spec="Spec không ghi",
       note="MT-22 — spec không ghi giới hạn 72h. 2 input cùng kết quả → giữ chung. Nguồn: r995, r996"),

    tc("配信タイミング — thêm & sửa", "FUNC-002", "Normal",
       "Chuyển đổi qua lại giữa 3 loại timing khi EDIT step → lưu đúng loại mới",
       SCE + "\n- S1 có 3 step: A = send ngay, B = 日時で指定 (2日後 10:00), C = 経過時間 (03時間00分後)",
       "1. Edit A: send ngay → 日時で指定 → lưu → kiểm tra DB\n2. Edit A: → 経過時間で指定 → lưu → kiểm tra DB\n"
       "3. Edit B: 日時で指定 → send ngay → lưu; rồi → 経過時間で指定 → lưu\n"
       "4. Edit C: 経過時間 → send ngay → lưu; rồi → 日時で指定 → lưu\n"
       "5. Sau mỗi lần: query `step_message` (delay_type, start_day, start_time) và kiểm tra thứ tự hiển thị",
       "6 hướng chuyển đổi giữa 3 loại timing",
       "- Cả 6 hướng chuyển đổi đều lưu THÀNH CÔNG\n"
       "- DB cập nhật đúng delay_type / start_day / start_time cho loại mới\n"
       "- Thứ tự step trên màn list được reorder lại đúng theo (start_day ASC, start_time ASC, id ASC)",
       note="Nguồn: r342, r343, r346, r347, r349, r350, r1002-r1015"),

    tc("配信タイミング — thêm & sửa", "FUNC-004", "Normal",
       "Xoá time send ngay rồi add lại → thành công (1 filter chỉ có 1 send ngay)",
       SCE + "\n- Filter default có step「ステップ開始直後」",
       "1. Xoá step「ステップ開始直後」\n2. Click「配信タイミングを追加する」→ chọn「ステップ開始直後」→ 決定\n"
       "3. Kiểm tra danh sách step + query `step_message`",
       "Xoá rồi add lại step send ngay",
       "- Xoá thành công\n- Add lại thành công (option không còn bị disable)\n- Filter có đúng 1 step delay_type = 1",
       note="Nguồn: r344, r345"),

    tc("配信タイミング — thêm & sửa", "DATA-CASCADE-001", "Normal",
       "Xoá time 経過時間で指定 → toàn bộ cụm liên quan tới time đó (message, action) cũng bị xoá",
       SCE + "\n- Step「03時間00分後」có 2 message và 1 action",
       "1. Ghi lại `step_message`.`id`, `template_ids`, `action_id` của step\n2. Xoá step「03時間00分後」\n"
       "3. Kiểm tra màn list step\n4. Query `step_message` / `template` (category_id = -111) / `t_actions` liên quan",
       "Step 03時間00分後 với 2 message + 1 action",
       "- Step biến mất khỏi danh sách\n- Message và action gắn với step đó cũng bị xoá (không mồ côi)",
       note="Nguồn: r351, r1016, r1017"),

    tc("配信タイミング — thêm & sửa", "FUNC-SORT-001", "Normal",
       "order_number trong DB luôn khớp thứ tự hiển thị ngoài màn — sau add / edit time / nhiều filter / nhiều trang",
       SCE_F + "\n- Filter default và F-A đều có ≥ 5 step",
       "1. Add step mới ở filter default → đối chiếu thứ tự hiển thị với `step_message`.`order_number`\n"
       "2. Add step ở filter F-A → đối chiếu\n3. Ở filter default, sửa time step: bằng time hiện tại / bé hơn time cũ "
       "(time tương lai) / lớn hơn time cũ (khác giờ-phút, khác ngày, khác tháng, khác năm) → sau MỖI lần đối chiếu order_number\n"
       "4. Lặp bước 3 ở filter F-A\n5. Tạo scenario có > 50 step (nhiều trang), sửa time → đối chiếu order_number",
       "≥ 5 step/filter; 6 kiểu sửa time; 1 scenario > 50 step",
       "- Sau MỌI thao tác, `step_message`.`order_number` luôn khớp đúng thứ tự đang hiển thị ngoài màn\n"
       "- Đúng cả ở filter default lẫn filter branch, đúng cả khi có phân trang",
       note="Nguồn:「21/11」r3-r21"),

    tc("配信タイミング — thêm & sửa", "JOB-001", "Normal",
       "Job cập nhật order_number cho scenario data cũ (order_number = NULL) → điền đúng thứ tự",
       SCE + "\n- Bot có scenario data cũ với `step_message`.`order_number` = NULL",
       "1. Query `step_message` WHERE scenario_id = <sce cũ> → xác nhận order_number = NULL\n"
       "2. Bật job cập nhật order_number\n3. Query lại `step_message`.`order_number`\n"
       "4. Mở màn list step, đối chiếu thứ tự hiển thị",
       "Scenario data cũ (bot 705 sce 10643 filter 153; bot 451 sce 10145 theo corpus)",
       "- `order_number` từ NULL được điền thành số thứ tự đúng theo (start_day ASC, start_time ASC, id ASC)\n"
       "- Thứ tự hiển thị ngoài màn khớp order_number trong DB",
       env="PRODUCTION",
       note="RULE-08: job nền → cần chạy PRODUCTION. Nguồn:「21/11」r25-r28"),

    tc("配信タイミング — thêm & sửa", "FUNC-DATE-001", "Normal",
       "Scenario có cả time quá khứ và time tương lai → time nhỏ hơn giờ hiện tại được cộng thêm 1 ngày",
       SCE + "\n- Thời điểm start scenario: 15:00. Filter default có step 0日後 10:00 (quá khứ), 0日後 18:00 (tương lai), 0日後 23:59",
       "1. Start scenario cho 1 friend lúc 15:00\n2. Query `scenario_step_time`.`send_time` của từng step\n"
       "3. Quan sát thời điểm thực tế friend nhận message",
       "Start lúc 15:00; step 0日後10:00 · 0日後18:00 · 0日後23:59",
       "- Step 0日後 10:00 (quá khứ): send_time = NGÀY MAI 10:00 (+1 ngày)\n"
       "- Step 0日後 18:00 (tương lai): send_time = HÔM NAY 18:00\n"
       "- Step 0日後 23:59: send_time = HÔM NAY 23:59\n"
       "- Các step sau đó tính đến 23h59 đều cộng thêm 1 ngày theo mốc đã dịch",
       env="PRODUCTION",
       note="RULE-08: phụ thuộc job nền → chạy PRODUCTION. Nguồn: r797, r1026, r1027"),

    tc("配信タイミング — thêm & sửa", "STATE-CLEAN-001", "Abnormal",
       "Edit time rồi thêm message: template『dùng luôn』→ time chưa lưu KHÔNG mất; template clone hoặc tạo mới → time vừa chọn BỊ MẤT",
       SCE + "\n- Step「03時間00分後」đang mở màn edit",
       "1. Edit time step thành「05時間00分後」nhưng CHƯA lưu\n"
       "2. Click「テンプレートから追加」→ chọn「テンプレートをそのまま利用する」→ quay lại màn step\n"
       "3. Quan sát time hiển thị\n4. Lặp lại: edit time chưa lưu → thêm template bằng「テンプレートを引用して編集する」→ quan sát\n"
       "5. Lặp lại: edit time chưa lưu → thêm message mới bằng「メッセージ追加」→ quan sát",
       "Edit time từ 03時間00分後 → 05時間00分後 (chưa lưu)",
       "- Bước 2-3 (template dùng luôn): time「05時間00分後」VẪN CÒN\n"
       "- Bước 4 (template clone): time vừa chọn BỊ MẤT, quay về「03時間00分後」\n"
       "- Bước 5 (tạo msg mới): time vừa chọn BỊ MẤT",
       spec="Đã hỏi leader",
       note="MT-23 — 3 lối thêm message cho 2 hành vi KHÁC nhau với time chưa lưu. Corpus r801 mô tả là hiện trạng, "
            "không nói đúng/sai. Spec không ghi. Nguồn: r801"),

    tc("配信タイミング — thêm & sửa", "FUNC-SEQ-001", "Normal",
       "Copy step TRÙNG TIME với step đã có → GỘP message của step nguồn vào step đích (không báo lỗi trùng)",
       SCE_F + "\n- Filter default có step「02時間00分後」với 1 message A; filter F-A có step「02時間00分後」với 1 message B",
       "1. Ở filter default, dùng chức năng copy step từ F-A\n2. Quan sát danh sách step của filter default\n"
       "3. Mở step「02時間00分後」xem danh sách message\n4. Query `step_message` WHERE scenario_id = <S1> AND filter_manager_id IS NULL",
       "Step trùng time 02時間00分後 ở 2 filter",
       "- Filter default KHÔNG sinh thêm step mới trùng time\n- Step「02時間00分後」có CẢ 2 message A và B\n"
       "- DB: chỉ 1 bản ghi step_message cho time đó, `template_ids` chứa cả 2 template",
       spec="Đã hỏi leader",
       note="MT-24 — spec BR-03 + §9 Validation Rules ghi『không cho phép 2 step trùng (delay_type, start_day, start_time, "
            "filter_manager_id)』với message lỗi「設定した時間に配信するメッセージが既に存在しています。」nhưng KHÔNG nêu ngoại lệ "
            "COPY = gộp. Nguồn: r60, r799, r735"),

    tc("配信タイミング — thêm & sửa", "OUT-001", "Normal",
       "Bug #32587: option ステップ開始直後 bị DISABLE vẫn click được 2 hyperlink ステップ開始時のトリガー và こちら → mở đúng URL manual",
       SCE_F + "\n- Filter default ĐÃ CÓ step「ステップ開始直後」(nên option này bị disable ở modal)",
       "1. Ở màn Edit Step, click nút「+配信タイミング」→ thấy option「ステップ開始直後」bị disable\n"
       "2. Click hyperlink「ステップ開始時のトリガー」→ quan sát tab mới\n3. Click hyperlink「こちら」→ quan sát tab mới\n"
       "4. Lặp bước 1-3 với nút「次の配信タイミングを追加」\n"
       "5. Lặp toàn bộ ở màn Setting filter\n6. Lặp toàn bộ với trạng thái CHƯA setting ステップ開始直後",
       "2 màn (Edit Step / Setting filter) × 2 nút (+配信タイミング / 次の配信タイミングを追加) × "
       "2 trạng thái (đã / chưa setting send ngay) × 2 hyperlink = 16 tổ hợp",
       "- Cả 16 tổ hợp: click mở TAB MỚI đúng URL\n"
       "-「ステップ開始時のトリガー」→ https://lme.jp/manual/lmeaction_friendaction/#toc7\n"
       "-「こちら」→ https://lme.jp/manual/step_delivery/#stepdelivery_addfriend",
       note="Bug #32587 (27-10-2025, OEM). 16 tổ hợp cùng 1 kết quả (mở đúng URL) → giữ chung. Nguồn:「text fix bug Kh」r63-r77"),

    tc("配信タイミング — thêm & sửa", "MSG-001", "Normal",
       "Bug #32802: sửa time step NHỎ HƠN time đã setting → hiện modal confirm; nhấn 変更する = lưu + tính lại time gửi",
       SCE + "\n- Scenario đang start cho 1 friend; step「経過時間 10時間00分後」chưa tới giờ gửi",
       "1. Ghi lại `scenario_step_time`.`send_time` của step\n2. Edit time step từ 10時間00分後 xuống 03時間00分後\n"
       "3. Bấm lưu → quan sát modal confirm\n4. Nhấn「変更する」\n5. Query lại `scenario_step_time`.`send_time`\n"
       "6. Đối chiếu UI alert với design",
       "Sửa 10時間00分後 → 03時間00分後 (nhỏ hơn)",
       "- HIỆN modal confirm (đúng format, đúng text, đúng vị trí theo design XD)\n"
       "- Nhấn「変更する」: lưu thay đổi VÀ tính toán lại send_time của step trong `scenario_step_time`",
       note="Bug #32802 update 20/11/2025. Evidence: ảnh chụp alert. Nguồn:「Job scenario」r109, r167, r182, r184, r186"),

    tc("配信タイミング — thêm & sửa", "STATE-CLEAN-001", "Normal",
       "Bug #32802: modal confirm sửa time → nhấn 閉じる → KHÔNG update step message, KHÔNG tính lại time gửi",
       SCE + "\n- Scenario đang start cho 1 friend; step「経過時間 10時間00分後」chưa tới giờ gửi",
       "1. Ghi lại `step_message`.`start_time` và `scenario_step_time`.`send_time`\n"
       "2. Sửa time xuống 03時間00分後 → lưu → modal confirm hiện\n3. Nhấn「閉じる」\n"
       "4. Query lại `step_message`.`start_time` và `scenario_step_time`.`send_time`",
       "Sửa 10時間00分後 → 03時間00分後, rồi nhấn 閉じる",
       "- `step_message`.`start_time` GIỮ NGUYÊN 10:00\n- `scenario_step_time`.`send_time` KHÔNG bị tính lại",
       note="Nguồn:「Job scenario」r134-r136, r167"),

    tc("配信タイミング — thêm & sửa", "MSG-001", "Normal",
       "Bug #32802: sửa time step LỚN HƠN time ban đầu → KHÔNG hiện alert, lưu thẳng và tính lại time gửi",
       SCE + "\n- Scenario đang start; step「経過時間 03時間00分後」chưa tới giờ gửi",
       "1. Sửa time từ 03時間00分後 lên 10時間00分後 → lưu\n2. Quan sát có modal confirm không\n"
       "3. Query `step_message`.`start_time` và `scenario_step_time`.`send_time`\n"
       "4. Lặp với loại 日時で指定: sửa ngày lớn hơn, và giữ nguyên ngày sửa giờ lớn hơn",
       "経過時間: 03:00 → 10:00 · 日時で指定: 1日後 → 3日後 · 1日後10:00 → 1日後18:00",
       "- KHÔNG hiện alert ở cả 3 trường hợp\n- Lưu thay đổi và tính toán lại send_time trong `scenario_step_time`",
       note="Nguồn:「Job scenario」r168, r183, r185"),

    tc("配信タイミング — thêm & sửa", "STATE-CLEAN-001", "Abnormal",
       "Bug #32802: KHÔNG sửa gì rồi nhấn save → không hiện alert, KHÔNG update step message, KHÔNG tính lại time gửi",
       SCE + "\n- Scenario đang start; step「経過時間 03時間00分後」",
       "1. Mở modal edit time, KHÔNG thay đổi gì\n2. Nhấn save\n3. Quan sát có alert không\n"
       "4. Query `step_message`.`is_new` và `update_timestamp`\n5. Kiểm tra job có chạy tính lại send_time không",
       "Không sửa gì, nhấn save",
       "- Không hiện alert\n- `step_message` KHÔNG bị update (is_new giữ nguyên, update_timestamp không đổi)\n"
       "- Job KHÔNG chạy tính toán lại send_time",
       spec="Đã hỏi leader",
       note="MT-25 — corpus「Job scenario」r169/r181 ghi chú:『Hiện tại vẫn đang update is_new = 2 và job CÓ chạy để "
            "tính toán lại』→ trái với kết quả mong đợi. TC dự kiến FAIL → cần raise bug. Nguồn:「Job scenario」r169, r181"),

    tc("配信タイミング — thêm & sửa", "CONC-001", "Abnormal",
       "Bug KH #36365: tab 1 xoá filter, tab 2 tạo step trong filter đó → tạo step FAIL + message JP, friend không nhận msg",
       SCE + "\n- Mở 2 tab trình duyệt cùng scenario S1\n- S1 có 1 filter branch F-A",
       "1. Tab 1: xoá filter F-A\n2. Tab 2 (chưa reload): trong màn filter F-A, tạo step「ステップ開始直後」→ quan sát\n"
       "3. Lặp với「日時で指定」và「経過時間で指定」\n"
       "4. Query `step_message` xem có bản ghi mới với filter_manager_id đã xoá không\n"
       "5. Query `filter_manager` xác nhận filter đã bị xoá khỏi DB\n6. Kiểm tra LINE app của friend test",
       "3 loại step timing × filter đã bị xoá ở tab khác",
       "- Cả 3 loại: tạo step THẤT BẠI\n- Hiển thị message:「絞り込み条件が削除されたため、画面を再読み込みしてください」\n"
       "- DB `step_message`: KHÔNG có bản ghi mới với filter_manager_id đã xoá\n"
       "- DB `filter_manager`: filter đã bị xoá hẳn\n- LINE user: KHÔNG nhận message của step đó",
       spec="Đã hỏi leader",
       note="MT-26 — mô tả cách fix ở r964 ghi text lỗi là「フィルターが削除されたため、画面を再読み込みしてください」, "
            "còn kết quả mong đợi của TC (r966-r971) ghi「絞り込み条件が削除されたため…」— 2 text KHÁC nhau. "
            "Bug KH #36365 (11-05-2026). 3 loại step cùng 1 kết quả → giữ chung. Nguồn: r964-r971"),

    tc("配信タイミング — thêm & sửa", "CONC-001", "Abnormal",
       "Bug KH #36365: scenario có 2 filter, xoá 1 filter ở màn khác rồi tạo step trong filter đó → cùng lỗi",
       SCE_F + "\n- Mở 2 màn cùng scenario S1; S1 có 2 filter F-A, F-B",
       "1. Màn 1: xoá filter F-A\n2. Màn 2 (chưa reload): tạo step trong F-A, lần lượt 3 loại timing\n"
       "3. Quan sát message lỗi\n4. Kiểm tra filter F-B còn hoạt động bình thường không",
       "2 filter, xoá F-A, tạo step ở F-A · 3 loại timing",
       "- Tạo step thất bại, hiển thị「絞り込み条件が削除されたため、画面を再読み込みしてください」\n"
       "- Filter F-B KHÔNG bị ảnh hưởng, vẫn tạo step bình thường",
       note="Nguồn: r969-r971"),

    tc("配信タイミング — thêm & sửa", "STATE-CLEAN-001", "Normal",
       "Bug KH #36365: sau khi gặp lỗi, reload trang theo hướng dẫn → dropdown filter không còn filter đã xoá, tạo step với filter còn lại thành công",
       SCE + "\n- Vừa gặp lỗi「絞り込み条件が削除されたため…」ở màn tạo step",
       "1. Reload trang (F5)\n2. Mở lại modal tạo step\n3. Quan sát dropdown/danh sách filter\n"
       "4. Chọn filter còn tồn tại → tạo step\n5. Kiểm tra GUI còn cảnh báo JP không",
       "Filter đã xoá + 1 filter còn lại",
       "- Sau reload: danh sách filter KHÔNG còn filter đã xoá\n- Tạo step với filter còn lại THÀNH CÔNG\n"
       "- GUI không còn hiển thị cảnh báo JP",
       note="TC-NEW-06 do AI viết trong corpus (05/2026), đã có kết quả test『OK step』. Nguồn: r975"),

    tc("配信タイミング — thêm & sửa", "FUNC-001", "Normal",
       "Bug KH #36365 (happy path): tạo step với filter CÒN TỒN TẠI → thành công, DB đúng filter_id và start_time",
       SCE + "\n- S1 có 1 filter branch F-A còn tồn tại (basic filter)",
       "1. Mở modal tạo step trong F-A\n2. Chọn「経過時間で指定」, nhập 01 giờ 00 phút\n3. Bấm 決定\n"
       "4. Quan sát modal + danh sách step\n5. Query `step_message` WHERE scenario_id = <S1> ORDER BY id DESC LIMIT 1",
       "Filter F-A còn sống · step 01時間00分後",
       "- Tạo step thành công, modal đóng\n- Step hiển thị trong list step của F-A\n"
       "- DB: bản ghi mới có filter_manager_id đúng của F-A, start_time = '01:00:00'\n- KHÔNG có message lỗi JP",
       note="TC-NEW-01 do AI viết trong corpus, kết quả『OK step』. Nguồn: r972"),

    tc("配信タイミング — thêm & sửa", "CONC-001", "Abnormal",
       "Bug KH #36365: EDIT step khi filter đã bị xoá ở tab khác → submit fail, step_message không bị update",
       SCE + "\n- S1 có step active thuộc filter X; mở 2 tab cùng edit step đó",
       "1. Ghi lại `step_message` của step (template_ids, start_time)\n2. Tab 1: xoá filter X\n"
       "3. Tab 2: edit step (đổi message body hoặc time) → submit\n4. Quan sát message lỗi\n"
       "5. Query `step_message` của scenario đó",
       "2 tab cùng edit 1 step; filter X bị xoá ở tab 1",
       "- Submit FAIL, hiển thị message JP tương tự case tạo step\n"
       "- DB `step_message` của scenario KHÔNG bị update\n- Các step_message thuộc filter X đã bị xoá cùng filter",
       note="TC-NEW-04 do AI viết trong corpus, kết quả『OK step』. Nguồn: r974"),

    tc("配信タイミング — thêm & sửa", "CONC-001", "Abnormal",
       "Bug KH #36365: double click submit tạo step → chỉ tạo 1 step, không duplicate",
       SCE + "\n- S1 có 1 filter active",
       "1. Mở modal tạo step, fill đủ thông tin\n2. Click button submit 2 lần liên tiếp thật nhanh\n"
       "3. Query `step_message` WHERE scenario_id = <S1> AND start_time = '<time vừa nhập>'",
       "Double click submit",
       "- Chỉ tạo ĐÚNG 1 step trong DB, KHÔNG duplicate\n- Hoặc button được disable ngay sau click đầu",
       note="TC-NEW-07 do AI viết trong corpus, kết quả『OK step』. Nguồn: r976"),

    tc("配信タイミング — thêm & sửa", "CONC-001", "Abnormal",
       "Bug KH #36365: copy step của filter ĐÃ BỊ XOÁ → báo lỗi 選択したステップが削除されたため、画面を再読み込みしてください",
       SCE_F + "\n- Mở 2 màn; F-A có 2 step; F-B là filter đích",
       "1. Màn 1: xoá filter F-A\n2. Màn 2 (chưa reload): ở F-B, dùng copy step, chọn nguồn là step của F-A → xác nhận\n"
       "3. Quan sát message lỗi\n4. Kiểm tra F-B có bị thêm step nào không",
       "Copy step từ filter F-A đã bị xoá",
       "- Hiển thị message:「選択したステップが削除されたため、画面を再読み込みしてください」\n"
       "- F-B KHÔNG bị thêm step nào",
       note="Nguồn: r977"),

    tc("配信タイミング — thêm & sửa", "REG-RUN-001", "Normal",
       "Bug KH #36365 (regression): scenario chạy step với filter còn tồn tại → message gửi ĐÚNG 1 LẦN, không duplicate",
       SCE + "\n- Đã tạo step「01時間00分後」với filter F-A còn tồn tại\n- Friend test「さや」thoả mãn điều kiện F-A, đã start scenario",
       "1. Chờ tới mốc 01時間00分後\n2. Quan sát LINE app của friend「さや」\n"
       "3. Query `step_message_history` của step này cho friend đó\n4. Query `scenario_step_time`",
       "Friend「さや」thoả mãn filter F-A; step 01時間00分後",
       "- LINE app nhận ĐÚNG 1 message ở mốc 01時間00分後 (không gửi 2 lần)\n"
       "- DB `step_message_history`: chỉ 1 bản ghi cho step này với friend đó\n"
       "- `scenario_step_time`: bản ghi được xử lý xong và xoá đúng",
       env="PRODUCTION",
       note="TC-NEW-02 do AI viết trong corpus, kết quả『OK step』. RULE-08: job nền → chạy PRODUCTION. Nguồn: r973"),
]
