# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 1-2: màn danh sách chính (SCR-FRL-01) — hiển thị,
sắp xếp, phân trang.

Corpus TCs của tính năng này (10.3 TCsLine_Friendlist) CHỈ phủ bulk action + search
+ xoá cascade. Toàn bộ nhóm 1-2 KHÔNG có TC gốc → expected viết bám
spec-features/admin/friend-list/ (ui-spec.md, web/logic-spec.md, db/db-mapping.md).
Mọi TC ở đây đều ghi rõ ở Ghi chú là suy luận từ spec và cần Leader xác nhận.
"""
from _common import tc

MAIN = ("- Đăng nhập Admin (role 主管理者) của 1 bot đã liên kết LINE OA\n"
        "- Bot có ≥ 10 friend, trong đó ≥ 2 friend chưa từng nhắn tin\n"
        "- Sidebar →「情報管理」→「友だちリスト」(/basic/friendlist)")

S1 = [
    # ═══════════ 1. Màn danh sách — hiển thị ═══════════
    tc("Màn danh sách — hiển thị", "UI-001", "Normal",
       "Toolbar màn 友だちリスト hiển thị đủ 5 thành phần đúng nhãn tiếng Nhật",
       MAIN,
       "1. Mở /basic/friendlist\n"
       "2. Đọc heading trang và toàn bộ thanh toolbar phía trên bảng\n"
       "3. Ghi lại placeholder của ô tìm kiếm và nhãn của 4 nút/link còn lại",
       "Không nhập gì — chỉ quan sát",
       "- Heading trang:「友だちリスト」\n"
       "- Ô tìm kiếm có placeholder「友だち名・システム表示名」\n"
       "- Nút tìm kiếm (icon kính lúp) nằm ngay sau ô tìm kiếm\n"
       "- Nút「絞込み」mở modal lọc nâng cao\n"
       "- 3 link:「非表示中の友だち」·「ブロックされた友だち」·「ブロックした友だち」\n"
       "- Click từng link điều hướng đúng: /basic/friendlist/hidden · /user-block · /block\n"
       "- Không lỗi 404/500, console không có lỗi JavaScript",
       spec="Đã hỏi leader",
       note="Corpus KHÔNG có TC cho toolbar — expected do AI viết bám ui-spec.md:44-56, "
            "cần Leader xác nhận. ⚠ Placeholder chỉ ghi 2 cột (友だち名・システム表示名) nhưng "
            "logic-spec.md:395 nói search 3 cột kể cả email — xem MT-01."),

    tc("Màn danh sách — hiển thị", "LIST-001", "Normal",
       "Bảng danh sách hiển thị đủ 7 cột đúng thứ tự và đúng nhãn",
       MAIN,
       "1. Mở /basic/friendlist\n"
       "2. Đọc dòng tiêu đề của bảng từ trái sang phải\n"
       "3. Đối chiếu từng nhãn cột với spec",
       "Không nhập gì — chỉ quan sát",
       "Thứ tự cột đúng: 1「全選択」(checkbox) → 2「友だち追加日時」→ 3「最新メッセージ」→ "
       "4「LINE登録名」→ 5「システム表示名」→ 6「メールアドレス」→ 7「ステップ配信状況」\n"
       "- Cột 2 và 3 có icon sắp xếp; các cột còn lại KHÔNG có\n"
       "- Cột「LINE登録名」là link, click mở /basic/friendlist/my_page/{id}",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md:74-84 + feature-spec.md §2 (bảng dữ "
            "liệu cột chính). Cần Leader xác nhận. Màn chi tiết bạn bè (my_page) đã tách ra "
            "khỏi phạm vi FA-013 — ở đây chỉ verify link mở được."),

    tc("Màn danh sách — hiển thị", "UI-001", "Normal",
       "Giá trị rỗng của システム表示名 và メールアドレス hiển thị dấu「-」chứ không để trắng",
       MAIN + "\n- Chuẩn bị 1 friend CHƯA đặt システム表示名 và CHƯA có メールアドレス",
       "1. Mở /basic/friendlist\n"
       "2. Tìm dòng của friend đã chuẩn bị\n"
       "3. Đọc giá trị 2 cột「システム表示名」và「メールアドレス」",
       "1 friend có line_user.view_name = NULL và line_user.email = NULL",
       "- Cả 2 ô hiển thị đúng ký tự「-」\n"
       "- KHÔNG để ô trắng, KHÔNG hiển thị chữ null / undefined / NaN",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md (cột メールアドレス: 'hiển thị \"-\" "
            "nếu chưa có') + feature-spec.md Field Traceability #4. Cần Leader xác nhận."),

    tc("Màn danh sách — hiển thị", "OUT-TRUTH-001", "Normal",
       "Cột ステップ配信状況 hiển thị đúng theo trạng thái đăng ký scenario của friend",
       MAIN + "\n- Chuẩn bị 3 friend: (a) đang chạy scenario S1, (b) đã dừng scenario, "
              "(c) chưa từng đăng ký scenario nào",
       "1. Mở /basic/friendlist\n"
       "2. Đọc cột「ステップ配信状況」của lần lượt 3 friend đã chuẩn bị",
       "(a) scenario_lineuser.is_following = 1 với scenario tên「S1」\n"
       "(b) scenario_lineuser.is_following = 2\n"
       "(c) không có bản ghi scenario_lineuser",
       "- Friend (a): hiển thị tên scenario「S1」\n"
       "- Friend (b): hiển thị「停止中」\n"
       "- Friend (c): ô để trống hoặc「-」(ghi lại giá trị thực tế để chốt spec)\n"
       "- Tên scenario quá dài bị cắt ngắn kèm dấu … chứ không làm vỡ layout cột",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md Field Traceability #7 "
            "(is_following=2 →「停止中」, =1 → tên scenario). Trường hợp (c) spec KHÔNG ghi → "
            "để mở, tester ghi lại giá trị thực tế cho Leader chốt."),

    tc("Màn danh sách — hiển thị", "DATA-COUNT-001", "Normal",
       "Text「検索結果： N人」và text phân trang khớp đúng số friend thực tế của bot",
       MAIN + "\n- Bot có đúng 24 friend đang kết bạn (chưa ai bị ẩn/bị block)",
       "1. Mở /basic/friendlist\n"
       "2. Đọc text kết quả phía trên bảng và text phân trang phía dưới bảng\n"
       "3. Đếm tay số dòng đang hiển thị trong bảng",
       "Bot có 24 friend (is_blocked = 0, is_hide = 0)",
       "- Hiển thị「検索結果： 24人」\n"
       "- Text phân trang hiển thị「24人中 1 - 24人目を表示中」\n"
       "- Số dòng đếm tay trong bảng = 24\n"
       "- 3 con số trên PHẢI bằng nhau",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md (検索結果： 24人 / 24人中 1 - 24人目を"
            "表示中). RULE-07: đối chiếu số trên màn với số bản ghi thực. Cần Leader xác nhận."),

    tc("Màn danh sách — hiển thị", "LIST-001", "Normal",
       "Friend đang bị ẩn hoặc đang bị block KHÔNG xuất hiện trong danh sách chính",
       MAIN + "\n- Chuẩn bị: 1 friend đã bị ẩn (非表示), 1 friend bị user block, "
              "1 friend bị admin block",
       "1. Ghi lại tên 3 friend đã chuẩn bị\n"
       "2. Mở /basic/friendlist\n"
       "3. Rà toàn bộ các trang của danh sách chính tìm 3 tên đó\n"
       "4. Đọc số「検索結果： N人」",
       "3 friend ở 3 trạng thái: is_hide=1 · is_blocked=1/blocked_by=0 · is_blocked=1/blocked_by=1",
       "- Cả 3 friend KHÔNG xuất hiện ở danh sách chính\n"
       "- Số N ở「検索結果」KHÔNG tính 3 friend này\n"
       "- 3 friend vẫn hiện đúng ở 3 màn phụ tương ứng",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám logic-spec.md:603 (bạn bè ẩn không xuất hiện ở "
            "danh sách chính) + feature-spec.md §2 (base query is_blocked=0). Cần Leader xác nhận."),

    tc("Màn danh sách — hiển thị", "UI-003", "Abnormal",
       "Bot chưa có friend nào — màn hiển thị trạng thái rỗng, không lỗi",
       "- Đăng nhập Admin của 1 bot MỚI, chưa có friend nào kết bạn",
       "1. Mở /basic/friendlist\n"
       "2. Quan sát vùng bảng, text kết quả và panel bulk action",
       "Bot có 0 friend",
       "- Bảng không có dòng dữ liệu nào, KHÔNG hiển thị dòng rác\n"
       "- Text kết quả hiển thị「検索結果： 0人」\n"
       "- Panel「友だち一括アクション」vẫn hiển thị với counter「選択中 0人」\n"
       "- Không lỗi 500, console không có lỗi JavaScript",
       spec="Đã hỏi leader",
       note="Corpus không có TC empty state — expected do AI viết bám ui-spec.md "
            "(bulk action panel luôn hiển thị kể cả khi chưa chọn ai). Cần Leader xác nhận."),

    tc("Màn danh sách — hiển thị", "UI-001", "Normal",
       "Panel 友だち一括アクション hiển thị đủ heading, mô tả, counter và nút アクション選択",
       MAIN,
       "1. Mở /basic/friendlist, cuộn xuống cuối bảng\n"
       "2. Đọc toàn bộ nội dung panel bulk action khi CHƯA chọn friend nào\n"
       "3. Tích 1 friend rồi đọc lại counter",
       "Tích đúng 1 friend bất kỳ",
       "- Heading「友だち一括アクション」\n"
       "- Mô tả「選択中の友だちに一括でアクションを稼働させます。」\n"
       "- Khi chưa chọn: counter「選択中 0人」\n"
       "- Sau khi tích 1 friend: counter đổi thành「選択中 1人」ngay, không cần reload\n"
       "- Nút「アクション選択」mở được modal chọn action",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md:113-120. Spec Gaps #1 ghi 'chưa mở "
            "xem nội dung nút アクション選択' → danh sách action lấy từ TC gốc r35-r43, xem "
            "nhóm『Bulk action — các loại action』và MT-10."),

    # ═══════════ 2. Sắp xếp & phân trang ═══════════
    tc("Sắp xếp & phân trang", "LIST-001", "Normal",
       "Sắp xếp theo 友だち追加日時 tăng dần — friend kết bạn sớm nhất lên đầu",
       MAIN + "\n- Bot có ≥ 5 friend với ngày kết bạn KHÁC nhau",
       "1. Mở /basic/friendlist\n"
       "2. Click icon sắp xếp ở cột「友だち追加日時」cho tới khi ra chiều tăng dần\n"
       "3. Đọc cột「友だち追加日時」của toàn bộ các dòng từ trên xuống",
       "5 friend có followed_at: 2022-09-21 / 2023-03-06 / 2023-05-22 / 2025-01-10 / 2026-02-01",
       "- Dòng đầu là 2022-09-21, dòng cuối là 2026-02-01\n"
       "- Giá trị cột giảm dần không xuất hiện ở bất kỳ vị trí nào (dãy tăng đơn điệu)\n"
       "- Ngày hiển thị đúng format YYYY-MM-DD\n"
       "- Số「検索結果： N人」KHÔNG đổi sau khi sắp xếp",
       spec="Đã hỏi leader",
       note="Corpus không có TC sắp xếp — expected bám feature-spec.md §2 EP-05 "
            "(value=1 → followed_at ASC). Cần Leader xác nhận chiều mặc định của lần click đầu."),

    tc("Sắp xếp & phân trang", "LIST-001", "Normal",
       "Sắp xếp theo 友だち追加日時 giảm dần — friend mới kết bạn nhất lên đầu",
       MAIN + "\n- Bot có ≥ 5 friend với ngày kết bạn KHÁC nhau",
       "1. Mở /basic/friendlist\n"
       "2. Click icon sắp xếp ở cột「友だち追加日時」cho tới khi ra chiều giảm dần\n"
       "3. Đọc cột「友だち追加日時」của toàn bộ các dòng từ trên xuống",
       "5 friend có followed_at: 2022-09-21 / 2023-03-06 / 2023-05-22 / 2025-01-10 / 2026-02-01",
       "- Dòng đầu là 2026-02-01, dòng cuối là 2022-09-21\n"
       "- Dãy giá trị giảm đơn điệu, không có dòng lệch thứ tự\n"
       "- Số「検索結果： N人」KHÔNG đổi sau khi sắp xếp",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md §2 EP-05 (value=2 → "
            "followed_at DESC). Cần Leader xác nhận."),

    tc("Sắp xếp & phân trang", "LIST-001", "Normal",
       "Sắp xếp theo 最新メッセージ giảm dần — friend vừa nhắn tin gần nhất lên đầu",
       MAIN + "\n- Chuẩn bị 3 friend có thời điểm nhận tin cuối khác nhau và "
              "1 friend CHƯA từng có tin nhắn nào",
       "1. Mở /basic/friendlist\n"
       "2. Click icon sắp xếp ở cột「最新メッセージ」\n"
       "3. Đọc cột「最新メッセージ」từ trên xuống, chú ý vị trí friend chưa có tin nhắn",
       "3 friend có last_time_message: 2026-02-27 / 2026-01-15 / 2025-12-01; "
       "1 friend last_time_message = NULL",
       "- 3 friend có tin nhắn xếp giảm dần: 2026-02-27 → 2026-01-15 → 2025-12-01\n"
       "- Friend chưa có tin nhắn hiển thị ô trống/「-」và nằm ở cuối danh sách\n"
       "- Không có dòng nào bị mất khỏi bảng sau khi sắp xếp (tổng số dòng = N)",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md §2 EP-05 (value=3 → "
            "last_time_message DESC). Vị trí của friend NULL spec KHÔNG ghi → tester ghi lại "
            "giá trị thực tế cho Leader chốt."),

    tc("Sắp xếp & phân trang", "LIST-001", "Boundary",
       "Phân trang danh sách chính đúng 200 friend/trang — biên 200 và 201",
       "- Đăng nhập Admin của bot có ĐÚNG 200 friend đang kết bạn (bot A)\n"
       "- Chuẩn bị thêm bot B có ĐÚNG 201 friend đang kết bạn",
       "1. Mở /basic/friendlist của bot A, đếm số dòng và đọc text phân trang\n"
       "2. Kiểm tra có hiện nút sang trang 2 không\n"
       "3. Chuyển sang bot B, lặp lại bước 1-2\n"
       "4. Ở bot B, sang trang 2 và đếm số dòng",
       "Bot A = 200 friend · Bot B = 201 friend",
       "- Bot A: bảng hiện 200 dòng, text「200人中 1 - 200人目を表示中」, KHÔNG có trang 2\n"
       "- Bot B: trang 1 hiện 200 dòng, text「201人中 1 - 200人目を表示中」, CÓ nút sang trang 2\n"
       "- Bot B trang 2: hiện đúng 1 dòng, text「201人中 201 - 201人目を表示中」\n"
       "- Friend ở trang 2 KHÔNG lặp lại friend đã có ở trang 1",
       spec="Đã hỏi leader",
       note="⚠ Gắn MT-02: logic-spec.md:607 ghi danh sách chính 200/page nhưng kết quả TÌM KIẾM "
            "là 50/page, trong khi TC gốc #38866 r59 lại nói『1 page = 200』kể cả khi search. "
            "TC này chỉ đo màn KHÔNG search — biên khi có search xem nhóm『Tìm kiếm theo từ khoá』."),

    tc("Sắp xếp & phân trang", "LIST-001", "Normal",
       "Chuyển trang giữ nguyên điều kiện sắp xếp đang áp dụng",
       "- Đăng nhập Admin của bot có ≥ 250 friend",
       "1. Mở /basic/friendlist\n"
       "2. Sắp xếp theo「友だち追加日時」giảm dần\n"
       "3. Ghi lại ngày của dòng CUỐI trang 1\n"
       "4. Sang trang 2, ghi lại ngày của dòng ĐẦU trang 2",
       "Bot có ≥ 250 friend, ngày kết bạn phân bố rải rác",
       "- Trang 2 vẫn ở chiều giảm dần (icon sắp xếp giữ nguyên trạng thái)\n"
       "- Ngày của dòng đầu trang 2 ≤ ngày của dòng cuối trang 1\n"
       "- Không friend nào xuất hiện ở cả 2 trang",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected do AI viết từ hành vi phân trang chuẩn, spec KHÔNG "
            "ghi rõ sort có được giữ qua trang không. Cần Leader xác nhận."),
]
