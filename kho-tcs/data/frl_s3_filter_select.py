# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 4-5: modal lọc nâng cao「絞り込み」(mức tóm tắt) và
cơ chế chọn friend qua 2 checkbox 全選択 /「条件に当てはまる友だち{N}人全員を選択」.

⚠ Modal「絞り込み」là SHARED COMPONENT SC-003, dùng chung bởi FA-002, FA-008, FA-009,
FA-013, FA-024. Theo tiền lệ đã áp cho FA-008, kho FA-013 CHỈ giữ TC ở mức『popup mở
được · 11 loại điều kiện lưu được · số 検索結果 khớp · điều kiện được truyền đúng sang
bulk action』. Chi tiết từng loại filter nằm ở TCsLine_Modal Filter (8 tab) — đề xuất
tách feature riêng『SC-003 絞り込み』.

Nguồn: 10.3 TCsLine_Friendlist → tab「#38866」(07/2026) cho nhóm checkbox;
TCsLine_Improve chung → tab「Improve nhỏ」(filter QR) và tab「Improve filter + url」
(danh mục 11 loại filter, CHỈ CÓ TIÊU ĐỀ, không có kết quả mong đợi).
"""
from _common import tc

BIG = ("- Đăng nhập Admin (role 主管理者) của bot có ~4.500 friend\n"
       "- Trong đó 312 friend có tên chứa「6期生」\n"
       "- Mở /basic/friendlist")
MID = ("- Đăng nhập Admin của bot có ≥ 400 friend\n"
       "- Bot đã có sẵn: ≥ 2 tag, ≥ 1 scenario, ≥ 1 QRコードアクション, ≥ 1 friend info, "
       "≥ 1 対応ステータス\n"
       "- Mở /basic/friendlist")

S3 = [
    # ═══════════ 4. Lọc nâng cao 絞り込み (mức tóm tắt SC-003) ═══════════
    tc("Lọc nâng cao 絞り込み", "UI-001", "Normal",
       "Nút 絞込み mở modal 絞り込み với 2 vùng điều kiện AND / OR",
       MID,
       "1. Click nút「絞込み」trên toolbar\n"
       "2. Đọc heading modal, 2 nút thêm điều kiện và nút đóng\n"
       "3. Click nút X đóng modal",
       "Không nhập điều kiện — chỉ mở và đóng",
       "- Modal mở dạng overlay với heading「絞り込み」\n"
       "- Có vùng「「全て満たす」必要がある条件 (and条件)を追加」\n"
       "- Có vùng「「どれか1つ以上満たす」必要がある条件を追加」\n"
       "- Nút đóng (X) ở góc trên phải, click thì modal đóng và danh sách phía sau "
       "KHÔNG bị thay đổi",
       spec="Đã hỏi leader",
       note="Mức tóm tắt SC-003. Nguồn: ui-spec.md (SCR-FRL-02) + feature-spec.md §2. "
            "Corpus TCsLine_Friendlist không có TC cho modal → expected bám spec, cần Leader "
            "xác nhận. Chi tiết từng loại filter: TCsLine_Modal Filter (tách riêng)."),

    tc("Lọc nâng cao 絞り込み", "FUNC-001", "Normal",
       "Modal 絞り込み có đủ 11 loại điều kiện lọc",
       MID,
       "1. Click「絞込み」→ click nút thêm điều kiện AND\n"
       "2. Liệt kê toàn bộ loại điều kiện hiện ra\n"
       "3. Đối chiếu với danh sách 11 loại trong spec",
       "Không nhập điều kiện — chỉ đếm loại",
       "Hiện đủ 11 loại:「タグ」·「友だち名」·「友だち追加日」·「ステップ購読状況」·"
       "「QRコードアクション」·「コンバージョン」·「確認状況」·「友だち情報」·"
       "「対応ステータス」·「アフィリエイター」·「新規・既存 友だち」\n"
       "- Không thiếu, không thừa loại nào\n"
       "- Vùng OR có cùng danh sách loại như vùng AND",
       spec="Đã hỏi leader",
       note="Mức tóm tắt SC-003. Nguồn: feature-spec.md §2 (bảng 11 loại filter) + "
            "TCsLine_Improve chung → tab「Improve filter + url」r3-r18 (danh mục filter tag / "
            "name / ngày add friend / scenario / landing — CHỈ CÓ TIÊU ĐỀ, không có kết quả "
            "mong đợi). Cần Leader xác nhận danh sách hiện tại trên tool."),

    tc("Lọc nâng cao 絞り込み", "DATA-COUNT-001", "Normal",
       "Lưu 1 điều kiện lọc — số 検索結果 và danh sách khớp đúng nhóm friend",
       MID + "\n- Chuẩn bị tag「TagA」đang gắn cho đúng 30 friend",
       "1. Click「絞込み」→ thêm điều kiện AND loại「タグ」→ chọn「TagA」\n"
       "2. Click「保存」\n"
       "3. Đọc số「検索結果： N人」và đếm số dòng trong bảng\n"
       "4. Mở màn chi tiết tag「TagA」đọc số friend đang gắn",
       "TagA gắn cho đúng 30 friend",
       "- Modal đóng, bảng cập nhật\n"
       "-「検索結果： 30人」\n"
       "- Số dòng trong bảng = 30 (nếu ≤ 200 thì hiện hết trên 1 trang)\n"
       "- Số ở màn chi tiết tag TagA cũng là 30 — 3 con số khớp nhau",
       spec="Đã hỏi leader",
       note="Mức tóm tắt SC-003. Corpus không có TC đo số — expected bám feature-spec.md §2 "
            "(luồng lọc nâng cao → hiển thị「検索結果： N人」). Cần Leader xác nhận."),

    tc("Lọc nâng cao 絞り込み", "LIST-001", "Normal",
       "Vùng AND và vùng OR cho ra tập kết quả khác nhau đúng logic",
       MID + "\n- Chuẩn bị: TagA gắn 30 friend, TagB gắn 20 friend, trong đó 5 friend có cả 2 tag",
       "1. Lọc AND: TagA + TagB → đọc N₁\n"
       "2.「クリア」rồi lọc OR: TagA hoặc TagB → đọc N₂\n"
       "3. Đối chiếu 2 con số với phép tính tay",
       "TagA = 30 · TagB = 20 · giao nhau = 5",
       "- Vùng AND (「全て満たす」): N₁ = 5\n"
       "- Vùng OR (「どれか1つ以上満たす」): N₂ = 30 + 20 − 5 = 45\n"
       "- Không friend nào bị đếm 2 lần trong kết quả OR",
       spec="Đã hỏi leader",
       note="Mức tóm tắt SC-003. Corpus không có TC AND/OR ở màn friendlist — expected do AI "
            "tính từ feature-spec.md §2 (logic AND/OR). Cần Leader xác nhận."),

    tc("Lọc nâng cao 絞り込み", "LIST-001", "Normal",
       "Filter QRコードアクション — 2 chiều『có quét』và『loại trừ』",
       MID + "\n- Chuẩn bị 1 QRコードアクション「QR1」, có friend kết bạn mới qua QR1 và "
             "friend cũ unblock qua QR1",
       "1. Lọc AND điều kiện「選択したQRコードアクションを1つ以上含む友だち」→ chọn QR1 → 保存\n"
       "2. Ghi lại danh sách friend trong kết quả\n"
       "3.「クリア」rồi lọc「選択したQRコードアクションを1つ以上含む人を除く友だち」→ chọn QR1 → 保存\n"
       "4. Ghi lại danh sách friend, đối chiếu 2 danh sách",
       "QR1 đã được quét bởi: 3 friend mới + 2 friend unblock",
       "- Chiều『含む』: chỉ 5 friend đã kết bạn qua QR1 hiển thị (gồm cả friend mới và "
       "friend unblock)\n"
       "- Chiều『除く』: đúng 5 friend đó bị loại, các friend còn lại hiển thị\n"
       "- Tổng 2 nhóm = tổng friend của bot, không friend nào lọt cả 2 hoặc rơi ra ngoài",
       note="Nguồn: TCsLine_Improve chung → tab「Improve nhỏ」r1199, r1230, r1268, r1274."),

    tc("Lọc nâng cao 絞り込み", "LIST-001", "Normal",
       "Kết hợp filter QRコードアクション với các loại điều kiện khác",
       MID + "\n- Chuẩn bị QR1, TagA, 1 対応ステータス và 1 friend info có giá trị",
       "1. Lọc AND: điều kiện QR「含む QR1」+ điều kiện「タグ = TagA」→ 保存 → ghi kết quả\n"
       "2.「クリア」rồi lọc AND: QR「除く QR1」+「対応ステータス」+「友だち情報」→ 保存 → ghi kết quả\n"
       "3. Kiểm tra tay từng friend trong kết quả có thoả đủ mọi điều kiện không",
       "Tổ hợp 2 điều kiện và tổ hợp 3 điều kiện",
       "- Lần 1: chỉ friend thoả CẢ 2 điều kiện được hiển thị\n"
       "- Lần 2: chỉ friend thoả CẢ 3 điều kiện được hiển thị\n"
       "- Không friend nào chỉ thoả 1 phần lọt vào kết quả",
       note="Nguồn: TCsLine_Improve chung → tab「Improve nhỏ」r1261, r1262. ⚠ r1262 trong TC "
            "gốc ghi tiêu đề『Check màn broadcast』nhưng các bước lại thao tác trên màn friend "
            "list — kho ghi nhận theo NỘI DUNG các bước (màn friendlist)."),

    tc("Lọc nâng cao 絞り込み", "BULK-001", "Normal",
       "Điều kiện lọc đang áp dụng được truyền đúng sang bulk action",
       MID + "\n- Chuẩn bị TagA gắn cho 250 friend (> 200)",
       "1. Lọc AND「タグ = TagA」→ 保存 → đọc N\n"
       "2. Tích 全選択 + tích checkbox「条件に当てはまる友だち250人全員を選択」\n"
       "3. Chạy action Add Tag với tag mới「TagX」\n"
       "4. Chờ job chạy xong → mở màn chi tiết TagX đếm số friend",
       "TagA = 250 friend (> 200 → đi luồng action schedule)",
       "- N = 250\n"
       "- Bản ghi action schedule được tạo có LƯU điều kiện lọc theo TagA\n"
       "- Sau khi job xong: đúng 250 friend được gắn TagX\n"
       "- Không friend nào ngoài nhóm TagA bị gắn TagX",
       note="Nguồn: #38866 r74 (đường đi chính của bug) + feature-spec.md §7.1 "
            "(ActionScheduleBotTask lấy users từ FilterV2)."),

    # ═══════════ 5. Chọn friend & checkbox 全選択 ═══════════
    tc("Chọn friend & checkbox 全選択", "BULK-001", "Normal",
       "Tích 全選択 chọn toàn bộ friend đang hiển thị trên trang hiện tại",
       BIG,
       "1. Không search gì, mở /basic/friendlist\n"
       "2. Tích checkbox「全選択」ở dòng tiêu đề bảng\n"
       "3. Đếm số dòng có checkbox được tích\n"
       "4. Đọc counter của panel「友だち一括アクション」",
       "Bot 4.500 friend, trang hiện tại hiển thị 200 dòng",
       "- Toàn bộ 200 dòng trên trang đều được tích\n"
       "- Panel hiển thị「選択中 200人」\n"
       "- Số ở counter = số dòng đếm tay",
       note="Nguồn: #38866 r5, r10."),

    tc("Chọn friend & checkbox 全選択", "BULK-001", "Normal",
       "Tích thủ công vài friend — chỉ đúng những friend đã tích được chọn",
       BIG,
       "1. Tích thủ công 7 friend bất kỳ (KHÔNG tích 全選択)\n"
       "2. Đọc counter panel\n"
       "3. Chạy action Add Tag với tag mới → đếm số friend trên màn chi tiết tag",
       "Tích đúng 7 friend",
       "- Panel hiển thị「選択中 7人」\n"
       "- Chỉ 7 friend đã tích nhận action\n"
       "- Số friend được gắn tag = 7",
       note="Nguồn: #38866 r8."),

    tc("Chọn friend & checkbox 全選択", "BULK-001", "Boundary",
       "Điều kiện hiển thị checkbox「条件に当てはまる友だち{N}人全員を選択」— biên 200 / 201",
       "- Đăng nhập Admin\n"
       "- Chuẩn bị 3 tình huống search cho ra ĐÚNG 199 / 200 / 201 kết quả",
       "1. Search ra 199 kết quả → tích 全選択 → quan sát có hiện checkbox không\n"
       "2. Search ra 200 kết quả → tích 全選択 → quan sát\n"
       "3. Search ra 201 kết quả → tích 全選択 → quan sát và đọc nhãn checkbox\n"
       "4. Ở tình huống 201: đọc counter panel khi CHƯA tích checkbox",
       "3 mốc kết quả: 199 · 200 · 201",
       "- 199 kết quả: checkbox KHÔNG hiển thị\n"
       "- 200 kết quả: checkbox KHÔNG hiển thị, panel「選択中 200人」\n"
       "- 201 kết quả: checkbox HIỂN THỊ, nhãn đúng「条件に当てはまる友だち201人全員を選択」\n"
       "- 201 kết quả, chưa tích checkbox: panel vẫn「選択中 200人」(chỉ trang hiện tại)",
       spec="Đã hỏi leader",
       note="Nguồn: #38866 r59, r60, r61. ⚠ r60 ghi『⏳ Cần confirm TA — biên hiển thị khi >200 "
            "hay ≥200』→ gắn MT-07. Spec KHÔNG mô tả checkbox này ở đâu (chỉ có 全選択) → "
            "MT-07 cũng là điểm spec bỏ sót."),

    tc("Chọn friend & checkbox 全選択", "UI-FIELD-001", "Normal",
       "Checkbox「条件に当てはまる...」chỉ xuất hiện SAU khi đã tích 全選択",
       BIG,
       "1. Search「6期生」→ 312 kết quả\n"
       "2. Khi CHƯA tích 全選択: quan sát vùng phía trên bảng\n"
       "3. Tích 全選択 → quan sát lại",
       "312 kết quả (> 200)",
       "- Trước khi tích 全選択: checkbox「条件に当てはまる...」KHÔNG hiển thị\n"
       "- Sau khi tích 全選択: checkbox xuất hiện",
       note="Nguồn: #38866 r63."),

    tc("Chọn friend & checkbox 全選択", "DATA-COUNT-001", "Normal",
       "Số N trên nhãn checkbox = số friend khớp điều kiện, không phải tổng friend của bot",
       BIG,
       "1. Search「6期生」→ tích 全選択\n"
       "2. Đọc con số N trong nhãn「条件に当てはまる友だち{N}人全員を選択」\n"
       "3. Đối chiếu với số「検索結果： N人」và với tổng friend của bot",
       "312 friend khớp「6期生」/ tổng 4.500 friend",
       "- N trên nhãn = 312\n"
       "- N = số ở「検索結果」\n"
       "- ⚠ N TUYỆT ĐỐI không được = 4.500 — đây chính là màn hình KH nhìn thấy đúng "
       "trước khi bug #38866 xảy ra ở bước thực thi",
       note="Nguồn: #38866 r62, r64."),

    tc("Chọn friend & checkbox 全選択", "DATA-COUNT-001", "Normal",
       "Không search gì — N trên nhãn bằng toàn bộ friend của bot",
       BIG,
       "1. Không search, tích 全選択\n"
       "2. Đọc N trên nhãn checkbox\n"
       "3. Đối chiếu với tổng số friend đang kết bạn của bot",
       "Bot có 4.500 friend đang kết bạn",
       "- N = 4.500\n"
       "- Đúng, vì không có điều kiện lọc nào\n"
       "- Friend đang bị ẩn / bị block KHÔNG được tính vào N",
       note="Nguồn: #38866 r65. Phần『friend ẩn/block không tính』suy từ base query "
            "is_blocked=0 (feature-spec.md §2) — cần Leader xác nhận."),

    tc("Chọn friend & checkbox 全選択", "DATA-COUNT-001", "Boundary",
       "N số rất lớn (> 200.000) — nhãn không cắt, không làm tròn, job không timeout",
       "- Đăng nhập Admin của bot PRODUCTION có > 200.000 friend",
       "1. Search 1 keyword cho ra ~217.253 kết quả → tích 全選択\n"
       "2. Đọc nhãn checkbox, kiểm tra layout không bị vỡ\n"
       "3. Tích checkbox → chạy Add Tag với tag mới\n"
       "4. Theo dõi job cho tới khi xong, ghi lại thời gian chạy\n"
       "5. Đọc số friend trên màn chi tiết tag",
       "N = 217.253 friend",
       "- Nhãn hiển thị đúng「条件に当てはまる友だち217253人全員を選択」— không cắt số, "
       "không làm tròn, không vỡ layout\n"
       "- Job chạy tới khi hoàn tất, KHÔNG timeout (giới hạn 30 phút)\n"
       "- Số friend được gắn tag = 217.253",
       env="PRODUCTION",
       note="Nguồn: #38866 r67 (Performance với số lớn). RULE-08: performance + job bắt buộc "
            "chạy PRODUCTION. feature-spec.md §7.1: job timeout 30 phút → process exit + restart."),

    tc("Chọn friend & checkbox 全選択", "BULK-001", "Normal",
       "Tích checkbox — counter panel đổi từ 200 lên N, đúng nhóm đang lọc",
       BIG,
       "1. Search「6期生」→ tích 全選択 (panel「選択中 200人」)\n"
       "2. Tích checkbox「条件に当てはまる友だち312人全員を選択」\n"
       "3. Đọc lại counter panel\n"
       "4. Chạy Add Tag với tag mới → chờ job → đếm số friend được gắn",
       "312 friend khớp「6期生」",
       "- Sau khi tích checkbox: panel hiển thị「選択中 312人」, KHÔNG phải 200\n"
       "- Điều kiện lọc lưu cho job đúng keyword「6期生」\n"
       "- Số friend nhận action = 312",
       note="Nguồn: #38866 r68."),

    tc("Chọn friend & checkbox 全選択", "BULK-001", "Normal",
       "Bỏ tích checkbox (vẫn giữ 全選択) — quay về chỉ chọn trang hiện tại",
       BIG,
       "1. Search「6期生」→ tích 全選択 + tích checkbox (panel「選択中 312人」)\n"
       "2. Bỏ tích checkbox「条件に当てはまる...」, giữ nguyên 全選択\n"
       "3. Đọc counter panel\n"
       "4. Chạy Add Tag với tag mới → đếm số friend được gắn",
       "312 friend khớp, trang hiện tại có 200 dòng",
       "- Panel hiển thị「選択中 200人」\n"
       "- Số friend nhận action = 200\n"
       "- 112 friend còn lại KHÔNG nhận action",
       note="Nguồn: #38866 r69."),

    tc("Chọn friend & checkbox 全選択", "STATE-CLEAN-001", "Abnormal",
       "⚠ Bỏ tích 全選択 khi checkbox đang tích — checkbox phải ẩn VÀ tự bỏ tích",
       BIG,
       "1. Search「6期生」→ tích 全選択 + tích checkbox (panel「選択中 312人」)\n"
       "2. Bỏ tích 全選択\n"
       "3. Quan sát checkbox「条件に当てはまる...」và counter panel\n"
       "4. Thử chạy Add Tag với tag mới → đếm số friend được gắn",
       "312 friend khớp「6期生」",
       "- Checkbox「条件に当てはまる...」ẨN đi VÀ trạng thái tích bị bỏ\n"
       "- Panel hiển thị「選択中 0人」\n"
       "- Không action nào chạy (hoặc 0 friend nhận action)\n"
       "- ⚠ Nếu checkbox ẩn nhưng trạng thái chọn-all vẫn còn ngầm → action apply TOÀN BỘ "
       "friend → lỗi nghiêm trọng cùng lớp bug #38866",
       note="Nguồn: #38866 r70 — TC gốc ghi rủi ro『trạng thái chọn-all không reset khi ẩn "
            "checkbox』."),

    tc("Chọn friend & checkbox 全選択", "BULK-001", "Abnormal",
       "Tích checkbox rồi BỎ TÍCH 1 friend lẻ — friend đã bỏ tích không được nhận action",
       BIG,
       "1. Search「6期生」→ tích 全選択 + tích checkbox (N = 312)\n"
       "2. Bỏ tích 1 friend cụ thể trên danh sách, ghi lại tên friend đó\n"
       "3. Đọc counter panel\n"
       "4. Chạy Add Tag với tag mới → chờ job → kiểm tra friend đó có bị gắn tag không",
       "312 friend khớp, bỏ tích 1 friend",
       "- Panel hiển thị「選択中 311人」(hoặc checkbox tự bỏ tích — ghi lại hành vi thực tế)\n"
       "- Số friend nhận action = số đang được chọn\n"
       "- ⚠ Friend đã bỏ tích TUYỆT ĐỐI không được nhận action",
       spec="Đã hỏi leader",
       note="Nguồn: #38866 r71 — TC gốc『⏳ Cần confirm TA』, spec không ghi. Gắn MT-07."),

    tc("Chọn friend & checkbox 全選択", "STATE-001", "Normal",
       "Tích checkbox rồi chuyển sang trang khác — trạng thái chọn-all được giữ",
       BIG,
       "1. Search「6期生」→ tích 全選択 + tích checkbox (N = 312)\n"
       "2. Chuyển sang trang 2 của kết quả\n"
       "3. Quan sát trạng thái checkbox, nhãn N và counter panel",
       "312 friend khớp, trang 1 có 200 dòng",
       "- Checkbox vẫn tích, nhãn vẫn ghi N = 312\n"
       "- Panel vẫn「選択中 312人」\n"
       "- Số friend nhận action = 312 (không phụ thuộc đang đứng ở trang nào)",
       note="Nguồn: #38866 r73."),

    tc("Chọn friend & checkbox 全選択", "STATE-CLEAN-001", "Abnormal",
       "⭐ Tích checkbox rồi ĐỔI keyword search — lựa chọn phải reset theo nhóm mới",
       BIG,
       "1. Search「6期生」→ 312 kết quả → tích 全選択 + tích checkbox (N = 312)\n"
       "2. Đổi keyword thành「7期生」→ search lại (500 kết quả)\n"
       "3. Quan sát trạng thái 2 checkbox, nhãn N và counter panel\n"
       "4. Chạy Add Tag với tag mới → chờ job → đếm số friend được gắn và kiểm tra "
       "họ thuộc nhóm nào",
       "keyword「6期生」(312) → keyword「7期生」(500)",
       "- Đổi keyword PHẢI reset lựa chọn: 全選択 và checkbox đều bỏ tích, panel「選択中 0人」\n"
       "- ⚠ Nếu trạng thái chọn-all được GIỮ qua lần search mới → action apply theo keyword "
       "MỚI (500 friend) chứ không phải nhóm user thấy lúc chọn (312) → user tưởng gắn cho "
       "312 nhưng thực tế 500",
       spec="Đã hỏi leader",
       note="Nguồn: #38866 r72 — TC gốc『⏳ Cần confirm TA — nghi ngờ trạng thái không reset』. "
            "Gắn MT-05. TC r57 (nhấn Enter) là biến thể cùng nội dung, giữ riêng vì đường "
            "kích hoạt khác nhau."),
]
