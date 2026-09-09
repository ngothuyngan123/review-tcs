# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 3: tìm kiếm theo từ khoá ở ô「友だち名・システム表示名」.

Nguồn chính: 10.3 TCsLine_Friendlist → tab「#38866」(07/2026, tab MỚI NHẤT của tính
năng — Bug KH: lọc 「6期生」 chọn đúng 312 người nhưng action gắn tag lại áp cho toàn
bộ 4.500 người). Số dòng `r<n>` ở Ghi chú là dòng của tab「#38866」trừ khi ghi rõ khác.

⚠ Toàn nhóm này gắn với 3 mâu thuẫn đang chờ Leader: MT-01 (search có khớp cột
メールアドレス không), MT-02 (page size khi search = 50 hay 200), MT-08 (keyword có
bị tách theo dấu cách không).
"""
from _common import tc

BIG = ("- Đăng nhập Admin (role 主管理者) của bot có ~4.500 friend\n"
       "- Trong đó 312 friend có tên chứa「6期生」\n"
       "- Mở /basic/friendlist")
MID = ("- Đăng nhập Admin của bot có ≥ 400 friend\n"
       "- Mở /basic/friendlist")

S2 = [
    # ── Khớp cột nào ──
    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Search khớp cột LINE登録名 — chỉ friend đúng keyword được hiển thị",
       BIG,
       "1. Nhập「6期生」vào ô「友だち名・システム表示名」\n"
       "2. Click nút tìm kiếm\n"
       "3. Đọc số「検索結果： N人」\n"
       "4. Rà cột「LINE登録名」của toàn bộ kết quả",
       "keyword =「6期生」· 312 friend có tên chứa「6期生」/ tổng 4.500 friend",
       "- Hiển thị「検索結果： 312人」, KHÔNG phải 4.500\n"
       "- Mọi dòng trong kết quả đều có「LINE登録名」hoặc「システム表示名」chứa「6期生」\n"
       "- Không friend nào ngoài nhóm 312 lọt vào danh sách",
       note="Nguồn: r9, r62, r64. Đây là con số KH đã xác nhận đúng trước khi bị bug #38866."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Search khớp cột システム表示名 — friend chỉ trùng tên hệ thống vẫn ra kết quả",
       MID + "\n- Chuẩn bị 1 friend có システム表示名 =「kin2」nhưng LINE登録名 KHÔNG chứa「kin2」",
       "1. Nhập「kin2」vào ô tìm kiếm → click nút tìm kiếm\n"
       "2. Kiểm tra friend đã chuẩn bị có trong kết quả không\n"
       "3. Đọc số「検索結果： N人」",
       "keyword =「kin2」· line_user.view_name =「kin2」, line_user.name =「テスト(Tan)」",
       "- Friend đã chuẩn bị CÓ trong danh sách kết quả\n"
       "- Số N tính cả friend này\n"
       "- Placeholder của ô tìm kiếm đã ghi rõ「友だち名・システム表示名」nên đây là hành vi đúng",
       note="Nguồn: r18 (nhóm『Check search theo EMAIL』lấy システム表示名 làm mốc đối chứng) "
            "+ ui-spec.md:48 (placeholder)."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "⭐ Search khớp cột メールアドレス — friend CHỈ trùng email vẫn phải ra kết quả",
       MID + "\n- Chuẩn bị ≥ 5 friend mà keyword CHỈ khớp Email, KHÔNG khớp 友だち名 và システム表示名\n"
             "- Tổng kết quả search ≤ 200",
       "1. Nhập keyword email (VD「tanaka」) vào ô tìm kiếm → click nút tìm kiếm\n"
       "2. Đếm số dòng hiển thị và đọc số「検索結果： N人」\n"
       "3. Tích 全選択 → chạy action Add Tag\n"
       "4. Mở màn chi tiết tag, đếm số friend đã được gắn",
       "keyword =「tanaka」· 5 friend có email chứa 'tanaka' nhưng tên không chứa",
       "- 5 friend khớp qua Email CÓ hiển thị trong danh sách\n"
       "- Số N = số dòng hiển thị\n"
       "- Vì ≤ 200 nên action chạy ngay, KHÔNG tạo action schedule\n"
       "- Số friend được gắn tag = N (đếm ở màn chi tiết tag)",
       spec="Đã hỏi leader",
       note="Nguồn: r18, r21, r22. ⚠ MT-01: placeholder + feature-spec.md §2 nói search chỉ "
            "theo tên, nhưng logic-spec.md:395 + api-spec.md:101 nói có cả email. TC gốc coi "
            "search-khớp-email là hành vi ĐÚNG → viết TC theo TC gốc, chờ Leader chốt."),

    tc("Tìm kiếm theo từ khoá", "DATA-COUNT-001", "Abnormal",
       "⭐ Nhóm kết quả TRỘN tên + email vượt 200 — đếm từng nhóm, không được sót nhóm email",
       MID + "\n- Chuẩn bị: keyword khớp 200 friend qua 友だち名 VÀ 120 friend CHỈ qua Email "
             "(tổng 320, không friend nào trùng cả 2)",
       "1. Search keyword → ghi lại số friend hiển thị\n"
       "2. Tích 全選択 + tích checkbox「条件に当てはまる友だち320人全員を選択」→ ghi lại N\n"
       "3. Chạy action Add Tag với tag mới hoàn toàn (số friend đang gắn = 0)\n"
       "4. Chờ job chạy xong\n"
       "5. Ở màn chi tiết tag, đếm RIÊNG: bao nhiêu friend thuộc nhóm khớp-tên, "
       "bao nhiêu thuộc nhóm chỉ-khớp-email",
       "200 friend khớp 友だち名 + 120 friend chỉ khớp Email = 320",
       "- N hiển thị = 320\n"
       "- Sau khi job xong: đúng 320 friend được gắn tag\n"
       "- Nhóm khớp tên: đủ 200 · Nhóm chỉ khớp email: đủ 120\n"
       "- ⚠ Nếu chỉ 200 friend được gắn → điều kiện lọc lưu cho job THIẾU cột email → FAIL",
       spec="Đã hỏi leader",
       note="Nguồn: r20 — TC gốc đánh dấu『⭐⏳ Bug ẩn — phải đếm từng nhóm』. Đây là case dễ lọt "
            "nhất vì vẫn có friend được gắn tag nên tester dễ tưởng đã OK. Gắn MT-01."),

    tc("Tìm kiếm theo từ khoá", "DATA-COUNT-001", "Abnormal",
       "Search theo DOMAIN email phổ biến (gmail.com) — N rất lớn, số nhận action phải khớp N",
       MID + "\n- Bot có ≥ 500 friend dùng email @gmail.com",
       "1. Nhập「gmail.com」vào ô tìm kiếm → tìm kiếm\n"
       "2. Ghi lại số「検索結果： N人」\n"
       "3. Tích 全選択 + tích checkbox chọn toàn bộ N\n"
       "4. Chạy action Add Tag với tag mới\n"
       "5. Chờ job xong, đếm số friend trên màn chi tiết tag",
       "keyword =「gmail.com」· ≥ 500 friend có email chứa gmail.com",
       "- Số friend được gắn tag = N\n"
       "- ⚠ Nếu điều kiện lọc lưu cho job bỏ cột email → N rất lớn nhưng gần như KHÔNG "
       "friend nào được gắn tag → độ lệch cực lớn, FAIL",
       spec="Đã hỏi leader",
       note="Nguồn: r23 — TC gốc đánh dấu『⏳ Lệch lớn nhất nếu fix thiếu email』. Gắn MT-01."),

    tc("Tìm kiếm theo từ khoá", "DATA-COUNT-001", "Normal",
       "Friend khớp cả Email lẫn 友だち名 chỉ được đếm 1 lần và nhận action 1 lần",
       MID + "\n- Chuẩn bị 1 friend vừa có tên chứa「tanaka」vừa có email chứa「tanaka」",
       "1. Search「tanaka」→ đọc N\n"
       "2. Đếm số dòng của friend đó trong bảng kết quả\n"
       "3. Chạy action Add Tag\n"
       "4. Mở màn chi tiết tag, đếm số lần friend đó xuất hiện",
       "friend có name =「tanaka taro」và email =「tanaka@example.com」",
       "- Friend chỉ xuất hiện ĐÚNG 1 dòng trong bảng kết quả\n"
       "- Chỉ được tính 1 lần vào N (không đếm trùng)\n"
       "- Chỉ nhận action 1 lần — màn chi tiết tag hiện friend đúng 1 lần",
       note="Nguồn: r29, r30. TC gốc ghi chú『Nhóm này KHÔNG lộ bug — dễ gây hiểu nhầm đã OK』, "
            "vì friend vẫn nhận action qua nhánh tên kể cả khi job bỏ cột email."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Abnormal",
       "Friend KHÔNG có email không bị khớp nhầm với bất kỳ keyword nào",
       MID + "\n- Chuẩn bị ≥ 3 friend có cột email trống/NULL",
       "1. Search 1 keyword bất kỳ không liên quan tên 3 friend đó\n"
       "2. Kiểm tra 3 friend có lọt vào kết quả không\n"
       "3. Lặp lại với keyword chỉ gồm 1 dấu cách",
       "3 friend có line_user.email = NULL · keyword thường và keyword =「 」(1 dấu cách)",
       "- 3 friend KHÔNG xuất hiện trong kết quả của cả 2 lần search\n"
       "- KHÔNG bị tính vào N\n"
       "- KHÔNG nhận action khi chạy bulk action",
       note="Nguồn: r31. TC gốc nhấn: keyword rỗng/chỉ dấu cách không được khớp NULL thành match."),

    # ── Ký tự đặc biệt & độ dài ──
    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Keyword chứa ký tự wildcard SQL % _ \\ ' \" không được lọc thừa friend",
       MID,
       "1. Lần lượt nhập 5 keyword vào ô tìm kiếm và tìm kiếm\n"
       "2. Với mỗi lần: ghi lại số「検索結果： N人」\n"
       "3. Với keyword「%」: đối chiếu N với tổng số friend của bot\n"
       "4. Chạy Add Tag cho 1 keyword bất kỳ, đếm số friend được gắn",
       "5 keyword: `%` · `_` · `\\` · `'` · `\"`",
       "- Keyword「%」KHÔNG được hiểu là wildcard → chỉ khớp friend có ký tự % thật trong "
       "tên/email, N ≪ tổng friend của bot\n"
       "- Keyword「_」tương tự, KHÔNG khớp mọi ký tự đơn\n"
       "- Keyword「'」và「\"」không gây lỗi 500, không lỗi SQL\n"
       "- Số friend nhận action = N",
       note="Nguồn: r16 — TC gốc ghi『Rủi ro cao: % là wildcard của LIKE』."),

    tc("Tìm kiếm theo từ khoá", "FUNC-004", "Boundary",
       "Keyword rất dài (> 255 ký tự) không bị cắt âm thầm khi lưu điều kiện lọc",
       MID,
       "1. Nhập keyword dài 300 ký tự vào ô tìm kiếm → tìm kiếm\n"
       "2. Ghi lại N\n"
       "3. Tích 全選択 (+ checkbox nếu N > 200) → chạy Add Tag\n"
       "4. Chờ job xong, đếm số friend được gắn tag",
       "keyword độ dài 300 ký tự",
       "- Keyword KHÔNG bị cắt khi lưu điều kiện lọc\n"
       "- Số friend nhận action = N\n"
       "- ⚠ Nếu keyword bị cắt còn 255 ký tự → điều kiện lọc rộng hơn → lọc sai nhóm friend",
       note="Nguồn: r17."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Keyword email dạng đầy đủ / phần local / có dấu chấm, dấu cộng — lưu nguyên văn",
       MID + "\n- Chuẩn bị friend có email「tanaka.taro+test@example.com」",
       "1. Lần lượt search 3 keyword và ghi N mỗi lần\n"
       "2. Với keyword「tanaka」: kiểm tra kết quả có gồm cả friend TÊN tanaka lẫn friend "
       "EMAIL bắt đầu bằng tanaka không\n"
       "3. Chạy Add Tag ở 1 keyword, đếm số friend được gắn",
       "3 keyword:「tanaka@example.com」·「tanaka」·「tanaka.taro+test@example.com」",
       "- Keyword full email: friend có email trùng khít được tính vào N\n"
       "- Keyword「tanaka」: khớp CẢ friend tên tanaka LẪN friend email bắt đầu bằng tanaka\n"
       "- Ký tự「.」và「+」không bị hiểu sai, keyword lưu nguyên văn\n"
       "- Số friend nhận action = N ở cả 3 trường hợp",
       spec="Đã hỏi leader",
       note="Nguồn: r21, r22, r26. r22 được TC gốc đánh dấu『⏳ Case thực tế dễ gặp nhất』: "
            "KH gõ tên nhưng vô tình khớp luôn email người khác → N phình lên. Gắn MT-01."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Email viết hoa/thường — hành vi lúc đếm và lúc job chạy phải giống nhau",
       MID + "\n- Chuẩn bị friend có email「tanaka@example.com」",
       "1. Search「Tanaka@Example.com」→ ghi N₁ → chạy Add Tag (tag mới) → đếm số friend gắn\n"
       "2. Search「tanaka@example.com」→ ghi N₂ → chạy Add Tag (tag mới khác) → đếm số friend gắn",
       "2 keyword khác nhau về hoa/thường, cùng trỏ tới 1 email",
       "- N₁ = N₂\n"
       "- Số friend nhận action ở cả 2 lần đều bằng N tương ứng\n"
       "- Không xảy ra trường hợp lúc đếm phân biệt hoa/thường mà lúc job chạy thì không "
       "(hoặc ngược lại)",
       note="Nguồn: r25."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Keyword email có dấu cách thừa đầu/cuối (thường và full-width)",
       MID,
       "1. Nhập「　tanaka@example.com　」(có full-width space đầu và cuối) → tìm kiếm\n"
       "2. Ghi lại N và số dòng hiển thị\n"
       "3. Tích 全選択 (+ checkbox nếu cần) → chạy Add Tag\n"
       "4. Đếm số friend được gắn tag",
       "keyword =「　tanaka@example.com　」(U+3000 ở 2 đầu)",
       "- Số friend nhận action = N\n"
       "- ⚠ Dấu cách KHÔNG được làm email bị cắt thành nhiều mảnh → nếu bị cắt, kết quả "
       "lọc sai hoàn toàn\n"
       "- Kết quả tương đương khi search email không có dấu cách thừa",
       spec="Đã hỏi leader",
       note="Nguồn: r27. Gắn MT-06 (dấu cách full-width) và MT-08 (keyword có bị tách theo "
            "dấu cách không)."),

    # ── Dấu cách ──
    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Normal",
       "Keyword có 1 dấu cách thường giữa 2 từ — đếm và job xử lý giống nhau",
       BIG,
       "1. Nhập「6期生 太郎」(1 half-width space) → tìm kiếm\n"
       "2. Ghi lại số friend hiển thị\n"
       "3. Tích 全選択 + tích checkbox → ghi lại N\n"
       "4. Chạy Add Tag với tag mới → chờ job xong\n"
       "5. Đếm số friend trên màn chi tiết tag",
       "keyword =「6期生 太郎」(half-width space)",
       "- Điều kiện lọc lưu ĐÚNG keyword user gõ, giữ nguyên dấu cách\n"
       "- Số friend nhận action = N\n"
       "- ⚠ Lúc đếm và lúc job chạy phải tách keyword GIỐNG NHAU (cùng tách theo space, "
       "hoặc cùng LIKE nguyên chuỗi)",
       spec="Đã hỏi leader",
       note="Nguồn: r35 — TC gốc ghi『⏳ Cần confirm TA — web tách theo space, check job có tách "
            "giống không』. Gắn MT-08: logic-spec.md:395 nói tách theo space nhưng feature-spec.md "
            "§2 nói LIKE '%keyword%' nguyên chuỗi."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "⚠ Keyword có NHIỀU dấu cách thường liên tiếp — không được sinh mảnh rỗng",
       BIG,
       "1. Nhập「6期生   太郎」(3 half-width space liên tiếp) → tìm kiếm\n"
       "2. Ghi lại N\n"
       "3. So sánh N với tổng số friend của bot (4.500)\n"
       "4. Tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword =「6期生   太郎」(3 space liên tiếp)",
       "- N ≪ 4.500 (chỉ friend thật sự khớp)\n"
       "- Số friend nhận action = N\n"
       "- ⚠ Nhiều space liên tiếp KHÔNG được sinh ra mảnh rỗng → nếu sinh mảnh rỗng thì "
       "điều kiện thành LIKE '%%' → khớp TOÀN BỘ 4.500 friend, tái hiện đúng bug #38866",
       note="Nguồn: r36 — TC gốc đánh dấu『⚠ Ưu tiên cao — cơ chế rất gần bug gốc』."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Dấu cách thường ở ĐẦU hoặc CUỐI keyword cho kết quả như không có dấu cách thừa",
       BIG,
       "1. Search「6期生」→ ghi N₀\n"
       "2. Search「 6期生」(space đầu) → ghi N₁\n"
       "3. Search「6期生 」(space cuối) → ghi N₂\n"
       "4. So sánh 3 con số",
       "3 keyword chỉ khác nhau ở dấu cách thừa",
       "- N₀ = N₁ = N₂ = 312\n"
       "- Không lần nào N vọt lên bằng tổng friend của bot\n"
       "- Số friend nhận action = N ở cả 3 lần",
       note="Nguồn: r37, r38."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "⭐ Dấu cách TIẾNG NHẬT (full-width U+3000) giữa 2 từ — trọng điểm của KH Nhật",
       BIG,
       "1. Dùng IME tiếng Nhật nhập「6期生　太郎」(full-width space) → tìm kiếm\n"
       "2. Ghi lại số friend hiển thị và N\n"
       "3. Tích 全選択 + tích checkbox → chạy Add Tag với tag mới\n"
       "4. Chờ job xong → đếm số friend trên màn chi tiết tag\n"
       "5. So sánh với kết quả khi dùng half-width space",
       "keyword =「6期生　太郎」(U+3000)",
       "- Điều kiện lọc lưu ĐÚNG keyword user gõ, giữ nguyên ký tự　\n"
       "- Số friend nhận action = N\n"
       "- ⚠ Nếu lúc đếm coi　là ký tự thường nhưng job coi là dấu tách (hoặc ngược lại) → "
       "số friend nhận action lệch khỏi N → FAIL",
       spec="Đã hỏi leader",
       note="Nguồn: r39 — kết quả gốc **NG**, đã raise bug **#38951**. TC gốc đánh dấu "
            "『⏳⚠ Ưu tiên cao nhất trong nhóm dấu cách』. DỰ KIẾN CÒN FAIL cho tới khi #38951 "
            "được fix — cần verify lại và cập nhật. Gắn MT-06."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Full-width space ở ĐẦU / CUỐI keyword — không được khớp toàn bộ friend",
       BIG,
       "1. Nhập「　　6期生　　」(2 full-width space ở mỗi đầu) → tìm kiếm\n"
       "2. Ghi lại N và so với tổng friend của bot\n"
       "3. Tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword =「　　6期生　　」",
       "- N = 312, KHÔNG phải 4.500\n"
       "- Số friend nhận action = 312\n"
       "- ⚠ Nếu full-width space bị trị như dấu tách và sinh mảnh rỗng → LIKE '%%' → khớp "
       "toàn bộ 4.500 friend, tái hiện đúng bug #38866",
       spec="Đã hỏi leader",
       note="Nguồn: r40 — TC gốc『⚠ Ưu tiên cao』, CHƯA CÓ kết quả test ở mọi cột ticket. "
            "Gắn MT-06, cùng lớp với #38951."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Keyword TRỘN cả half-width lẫn full-width space — xử lý nhất quán",
       BIG,
       "1. Nhập「6期生　太郎 花子」(full-width space rồi half-width space) → tìm kiếm\n"
       "2. Ghi lại N\n"
       "3. Tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword =「6期生　太郎 花子」",
       "- Số friend nhận action = N\n"
       "- Cả 2 loại dấu cách được xử lý NHẤT QUÁN giữa lúc đếm và lúc job chạy\n"
       "- ⚠ Nếu chỉ 1 trong 2 loại được coi là dấu tách → số lệch",
       spec="Đã hỏi leader",
       note="Nguồn: r41 — TC gốc『⏳ Cần confirm TA』, CHƯA CÓ kết quả test. Gắn MT-06/MT-08."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Abnormal",
       "Friend có TÊN chứa dấu cách — search đúng cả cụm「山田 太郎」",
       MID + "\n- Chuẩn bị: 1 friend tên đúng là「山田 太郎」, và các friend khác chỉ có "
             "「山田」hoặc「太郎」riêng lẻ",
       "1. Search「山田 太郎」→ ghi N và liệt kê tên các friend trong kết quả\n"
       "2. Xác định kết quả có gồm cả friend chỉ có「山田」hoặc chỉ có「太郎」không\n"
       "3. Chạy Add Tag → đếm số friend được gắn",
       "keyword =「山田 太郎」",
       "- Ghi lại chính xác kết quả thực tế (tìm ĐÚNG cụm hay tìm 山田 HOẶC 太郎)\n"
       "- Dù theo hướng nào: số friend nhận action = N\n"
       "- ⚠ Nếu dấu cách bị coi là dấu tách → kết quả ra cả 山田* và 太郎* → nhiều hơn "
       "mong đợi của user",
       spec="Đã hỏi leader",
       note="Nguồn: r42 — TC gốc『⏳ Cần confirm BA/KH — mong đợi nghiệp vụ』, CHƯA CÓ kết quả "
            "test. Gắn MT-08: đây chính là chỗ 2 tài liệu spec nói ngược nhau."),

    # ── Ký tự tiếng Nhật ──
    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Normal",
       "Keyword kanji / hiragana / katakana full-width — lưu nguyên vẹn, không mojibake",
       BIG,
       "1. Lần lượt search 3 keyword, mỗi lần ghi lại N và ảnh chụp ô tìm kiếm sau khi search\n"
       "2. Chạy Add Tag ở 1 keyword bất kỳ → đếm số friend được gắn",
       "3 keyword:「期生」(kanji) ·「たろう」(hiragana) ·「タロウ」(katakana full-width)",
       "- Cả 3 keyword hiển thị lại đúng nguyên văn trong ô tìm kiếm sau khi search "
       "(không biến thành ký tự lạ)\n"
       "- Kết quả tìm kiếm khớp đúng nhóm friend tương ứng\n"
       "- Số friend nhận action = N",
       note="Nguồn: r43, r44, r45."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Boundary",
       "Katakana half-width「ﾀﾛｳ」vs full-width「タロウ」— không tự động convert",
       MID + "\n- Chuẩn bị friend có tên chứa「タロウ」(full-width katakana)",
       "1. Search「タロウ」→ ghi N₁ → chạy Add Tag (tag mới) → đếm số friend gắn\n"
       "2. Search「ﾀﾛｳ」→ ghi N₂ → chạy Add Tag (tag mới khác) → đếm số friend gắn\n"
       "3. So sánh N₁, N₂ và 2 số friend được gắn",
       "2 keyword:「タロウ」(full-width) và「ﾀﾛｳ」(half-width)",
       "- Keyword lưu ĐÚNG dạng user gõ, hệ thống KHÔNG tự convert half ↔ full\n"
       "- Hành vi lúc đếm và lúc job chạy giống nhau: số friend nhận action = N trong "
       "cả 2 trường hợp\n"
       "- ⚠ Nếu 1 bên normalize half/full-width mà bên kia không → 2 con số lệch nhau",
       spec="Đã hỏi leader",
       note="Nguồn: r46 — TC gốc『⏳ Cần confirm TA』."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Boundary",
       "Số full-width「６期生」vs half-width「6期生」— IME tiếng Nhật hay ra số full-width",
       BIG,
       "1. Search「6期生」(số half-width) → ghi N₁ và số friend nhận action\n"
       "2. Search「６期生」(số full-width) → ghi N₂ và số friend nhận action\n"
       "3. So sánh 2 cặp số",
       "2 keyword khác nhau ở dạng chữ số",
       "- Keyword lưu ĐÚNG dạng user gõ, không tự động convert\n"
       "- Số friend nhận action = N trong cả 2 trường hợp\n"
       "- Ghi lại rõ N₁ có bằng N₂ không để Leader chốt spec",
       spec="Đã hỏi leader",
       note="Nguồn: r47 — TC gốc『⏳ Cần confirm TA — KH gõ IME tiếng Nhật rất hay ra số "
            "full-width』."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Ký tự đặc biệt tiếng Nhật「〜」「・」「々」「ー」— đặc biệt là「・」",
       MID + "\n- Chuẩn bị friend có tên chứa「・」(VD「山田・太郎」)",
       "1. Lần lượt search 4 keyword:「〜」·「・」·「々」·「ー」\n"
       "2. Ghi lại N mỗi lần\n"
       "3. Với keyword「・」: kiểm tra kết quả có phình ra ngoài nhóm friend có「・」không\n"
       "4. Search「山田・太郎」→ ghi N và so với số friend thật sự có tên đó",
       "4 ký tự đặc biệt JP + keyword「山田・太郎」",
       "- 4 keyword đều lưu nguyên vẹn, không lỗi encoding\n"
       "- Số friend nhận action = N ở mỗi lần\n"
       "- ⚠「・」là ký tự phân cách thường gặp trong tên người Nhật — KHÔNG được trị như "
       "dấu tách; nếu bị tách thì「山田・太郎」sẽ ra cả 山田* và 太郎*",
       spec="Đã hỏi leader",
       note="Nguồn: r48 — TC gốc『⏳ Cần confirm TA —「・」có bị trị như dấu tách?』."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Keyword chứa emoji (4-byte) — không lỗi encoding, collation utf8mb4",
       MID + "\n- Chuẩn bị 1 friend có tên chứa emoji (VD「🌸さくら」)",
       "1. Nhập keyword có emoji「🌸」vào ô tìm kiếm → tìm kiếm\n"
       "2. Kiểm tra friend đã chuẩn bị có trong kết quả không\n"
       "3. Ghi lại N, chạy Add Tag → đếm số friend được gắn",
       "keyword =「🌸」",
       "- Không lỗi 500, không lỗi ký tự (emoji không thành「?」hay ô vuông)\n"
       "- Friend có emoji trong tên xuất hiện đúng trong kết quả\n"
       "- Số friend nhận action = N",
       note="Nguồn: r49 — TC gốc lưu ý check collation DB có hỗ trợ utf8mb4."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Normal",
       "Keyword trộn tiếng Nhật + latin + số「6期生Tanaka」",
       MID,
       "1. Search「6期生Tanaka」→ ghi N\n"
       "2. Rà kết quả xác nhận đều khớp nguyên cụm\n"
       "3. Chạy Add Tag → đếm số friend được gắn",
       "keyword =「6期生Tanaka」",
       "- Keyword lưu nguyên vẹn\n"
       "- Số friend nhận action = N",
       note="Nguồn: r50."),

    # ── Thao tác Enter & vòng đời search ──
    tc("Tìm kiếm theo từ khoá", "UI-INPUT-001", "Normal",
       "Nhấn Enter trong ô tìm kiếm thực thi search, không reload trang",
       BIG,
       "1. Nhập「6期生」vào ô「友だち名・システム表示名」\n"
       "2. Nhấn phím Enter\n"
       "3. Quan sát: bảng có cập nhật không, trang có reload không (icon loading của trình duyệt)",
       "keyword =「6期生」",
       "- Search được thực thi, bảng hiển thị đúng 312 friend khớp keyword\n"
       "- KHÔNG reload toàn trang\n"
       "- KHÔNG submit nhầm form khác trên trang",
       note="Nguồn: r51 — yêu cầu của BA: check thao tác Enter."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Enter và click nút tìm kiếm cho ra điều kiện lọc GIỐNG HỆT nhau",
       BIG,
       "1. Nhập「6期生」→ nhấn Enter → ghi số dòng hiển thị, N, chạy Add Tag (tag A) → "
       "đếm số friend gắn tag A\n"
       "2. Xoá keyword, nhập lại「6期生」→ click nút tìm kiếm → ghi số dòng, N, chạy Add Tag "
       "(tag B) → đếm số friend gắn tag B\n"
       "3. So sánh từng cặp số",
       "cùng keyword「6期生」, 2 cách kích hoạt search",
       "- Số dòng hiển thị: 2 lần bằng nhau\n"
       "- N: 2 lần bằng nhau (312)\n"
       "- Số friend nhận action: 2 lần bằng nhau\n"
       "- ⚠ Nếu Enter không gửi đủ tham số như click nút (VD thiếu keyword) → có thể chính "
       "là nguồn của bug #38866",
       note="Nguồn: r52 — TC gốc ghi『⏳ Nghi ngờ: Enter có thể không gửi đủ param』."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Abnormal",
       "Nhấn Enter khi ô tìm kiếm rỗng — hiển thị toàn bộ friend, không tạo điều kiện thừa",
       BIG,
       "1. Đảm bảo ô tìm kiếm trống\n"
       "2. Nhấn Enter\n"
       "3. Đọc N, tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword rỗng · bot có 4.500 friend",
       "- Hiển thị toàn bộ friend, không lỗi\n"
       "- N = 4.500 (đúng, vì không lọc gì)\n"
       "- Số friend nhận action = 4.500\n"
       "- KHÔNG tạo điều kiện lọc tên thừa trong bản ghi schedule",
       note="Nguồn: r53."),

    tc("Tìm kiếm theo từ khoá", "CONC-001", "Abnormal",
       "Nhấn Enter 5 lần liên tiếp thật nhanh — không nhân đôi dòng, không tạo schedule thừa",
       BIG,
       "1. Nhập「6期生」\n"
       "2. Nhấn Enter 5 lần liên tiếp thật nhanh\n"
       "3. Đếm số dòng trong bảng, đọc N\n"
       "4. Tích 全選択 + checkbox → chạy Add Tag → đếm số bản ghi action schedule được tạo",
       "keyword =「6期生」· nhấn Enter 5 lần",
       "- Kết quả cuối cùng đúng: 312 dòng, không dòng nào bị lặp\n"
       "- N = 312\n"
       "- Chỉ tạo ĐÚNG 1 bản ghi action schedule, không tạo thừa",
       note="Nguồn: r54."),

    tc("Tìm kiếm theo từ khoá", "CONC-003", "Abnormal",
       "Đổi keyword giữa lúc đang load kết quả — bảng và số N phải cùng theo keyword cuối",
       BIG,
       "1. Nhập keyword A「6期生」→ Enter\n"
       "2. Trong lúc bảng đang load, nhập ngay keyword B「7期生」→ Enter\n"
       "3. Chờ ổn định, đọc keyword hiển thị trong ô, số dòng bảng và N\n"
       "4. Chạy Add Tag → đếm số friend được gắn",
       "keyword A =「6期生」(312 friend) → keyword B =「7期生」(500 friend)",
       "- Bảng, số N và ô tìm kiếm đều theo keyword CUỐI CÙNG (B)\n"
       "- ⚠ KHÔNG được: bảng hiển thị theo A nhưng N tính theo B (hoặc ngược lại)\n"
       "- Số friend nhận action = N (500)",
       note="Nguồn: r55 — race condition giữa danh sách và bộ đếm, TC gốc xếp cùng lớp bug #38866."),

    tc("Tìm kiếm theo từ khoá", "UI-INPUT-001", "Abnormal",
       "⚠ Nhấn Enter khi panel 友だち一括アクション đang mở — không được chạy action ngoài ý muốn",
       BIG,
       "1. Tích 全選択 để panel「友だち一括アクション」ở trạng thái có friend được chọn\n"
       "2. Mở panel chọn action\n"
       "3. Đưa con trỏ vào ô tìm kiếm, nhập keyword mới\n"
       "4. Nhấn Enter\n"
       "5. Kiểm tra có action nào được thực thi không (màn chi tiết tag, chat 1:1 của friend)",
       "panel action đang mở + keyword mới trong ô tìm kiếm",
       "- CHỈ search được thực thi\n"
       "- ⚠ KHÔNG submit nhầm panel action — không friend nào nhận action\n"
       "- Màn chat 1:1 của friend bất kỳ KHÔNG xuất hiện trigger 手動操作 mới",
       note="Nguồn: r56 — TC gốc ghi『Rủi ro: Enter trigger action ngoài ý muốn』."),

    tc("Tìm kiếm theo từ khoá", "STATE-001", "Abnormal",
       "⭐ Đang tích 全選択 + checkbox rồi search keyword MỚI — lựa chọn phải được reset",
       BIG,
       "1. Search「6期生」→ 312 kết quả\n"
       "2. Tích 全選択 + tích checkbox「条件に当てはまる友だち312人全員を選択」(N = 312)\n"
       "3. Xoá keyword, nhập「7期生」→ nhấn Enter\n"
       "4. Quan sát trạng thái 2 checkbox và counter của panel\n"
       "5. Chạy Add Tag với tag mới → chờ job → đếm số friend được gắn",
       "keyword「6期生」(312) → keyword「7期生」(500)",
       "- Sau bước 3: cả 全選択 và checkbox đều BỎ TÍCH, panel về「選択中 0人」\n"
       "- Không cho chạy action khi chưa chọn lại, hoặc nếu chọn lại thì số friend nhận "
       "action = N mới\n"
       "- ⚠ Nếu trạng thái chọn-all được giữ ngầm → action apply theo keyword MỚI chứ không "
       "phải nhóm user nhìn thấy lúc chọn → cùng lớp bug #38866",
       spec="Đã hỏi leader",
       note="Nguồn: r57 — TC gốc『⏳ Cần confirm TA — nghi ngờ trạng thái không reset』. "
            "Gắn MT-05. Xem thêm TC cùng nội dung ở nhóm『Chọn friend & checkbox 全選択』(r72)."),

    tc("Tìm kiếm theo từ khoá", "DATA-TEXT-001", "Abnormal",
       "Enter với keyword có dấu cách (thường + full-width) — không làm mất dấu cách",
       BIG,
       "1. Nhập「6期生　太郎」(full-width space) → nhấn Enter → ghi N và số friend nhận action\n"
       "2. Nhập「6期生 太郎」(half-width space) → nhấn Enter → ghi N và số friend nhận action\n"
       "3. Lặp lại cả 2 bằng cách click nút tìm kiếm, so sánh với kết quả khi nhấn Enter",
       "2 keyword khác loại dấu cách, 2 cách kích hoạt search",
       "- Điều kiện lọc lưu GIỐNG HỆT giữa Enter và click nút\n"
       "- Số friend nhận action = N trong cả 4 lần\n"
       "- ⚠ Enter không được làm mất hoặc đổi dấu cách full-width khi gửi request",
       spec="Đã hỏi leader",
       note="Nguồn: r58 — kết quả gốc **NG**. Kết hợp 2 yêu cầu Enter + dấu cách; cùng nhóm "
            "bug #38951. DỰ KIẾN CÒN FAIL — cần verify lại. Gắn MT-06."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Abnormal",
       "Search không khớp friend nào — tuyệt đối không được apply action cho toàn bộ friend",
       BIG,
       "1. Nhập keyword chắc chắn không khớp ai (VD「zzzz_khong_ton_tai」) → tìm kiếm\n"
       "2. Đọc N và số dòng trong bảng\n"
       "3. Tích 全選択 → quan sát checkbox「条件に当てはまる...」có hiện không\n"
       "4. Thử chạy Add Tag → đếm số friend được gắn",
       "keyword =「zzzz_khong_ton_tai」· 0 kết quả",
       "- Bảng rỗng,「検索結果： 0人」\n"
       "- Checkbox「条件に当てはまる...」KHÔNG hiển thị\n"
       "- Không cho thực hiện action, hoặc nếu cho thì 0 friend nhận action\n"
       "- ⚠ TUYỆT ĐỐI không được apply cho toàn bộ 4.500 friend",
       note="Nguồn: r14 — TC gốc ghi rủi ro『điều kiện rỗng → job hiểu là không lọc → apply all』."),

    tc("Tìm kiếm theo từ khoá", "STATE-CLEAN-001", "Normal",
       "Xoá trắng keyword rồi search lại — điều kiện lọc cũ không còn sót",
       BIG,
       "1. Search「6期生」→ 312 kết quả\n"
       "2. Xoá trắng ô tìm kiếm → tìm kiếm lại\n"
       "3. Đọc N\n"
       "4. Tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword「6期生」→ keyword rỗng",
       "- Điều kiện lọc KHÔNG còn keyword cũ\n"
       "- N = toàn bộ friend của bot = 4.500\n"
       "- Số friend nhận action = 4.500",
       note="Nguồn: r12."),

    tc("Tìm kiếm theo từ khoá", "STATE-CLEAN-001", "Normal",
       "Đổi keyword A → B rồi search — điều kiện lọc chỉ chứa B",
       BIG,
       "1. Search keyword A「6期生」→ 312 kết quả\n"
       "2. Đổi thành keyword B「7期生」→ tìm kiếm\n"
       "3. Đọc N\n"
       "4. Tích 全選択 + checkbox → chạy Add Tag → chờ job → kiểm tra danh sách friend "
       "được gắn có ai thuộc nhóm「6期生」không",
       "keyword A =「6期生」(312) → keyword B =「7期生」(500)",
       "- N = 500 (theo B)\n"
       "- Số friend nhận action = 500\n"
       "- KHÔNG còn sót keyword A: không friend nào chỉ khớp「6期生」bị gắn tag",
       note="Nguồn: r13."),

    tc("Tìm kiếm theo từ khoá", "LIST-001", "Normal",
       "Keyword khớp TOÀN BỘ friend của bot — kết quả trùng với không search",
       MID + "\n- Bot mà mọi friend đều có tên chứa「テスト」",
       "1. Search「テスト」→ ghi N₁\n"
       "2. Click「クリア」để bỏ lọc → ghi N₂\n"
       "3. Với lần search: tích 全選択 + checkbox → chạy Add Tag → đếm số friend được gắn",
       "keyword khớp 100% friend của bot",
       "- N₁ = N₂ = tổng friend của bot\n"
       "- Số friend nhận action = N₁ (đúng, vì tất cả đều khớp keyword)\n"
       "- Đường đi khác nhau (có điều kiện lọc vs không) nhưng kết quả trùng nhau",
       note="Nguồn: r15."),

    tc("Tìm kiếm theo từ khoá", "STATE-CLEAN-001", "Normal",
       "Link「クリア」reset toàn bộ bộ lọc, đưa về danh sách đầy đủ",
       BIG,
       "1. Search「6期生」→ 312 kết quả\n"
       "2. Click link「クリア」\n"
       "3. Đọc URL, nội dung ô tìm kiếm và số「検索結果： N人」",
       "keyword =「6期生」",
       "- Điều hướng về /basic/friendlist (không còn tham số lọc)\n"
       "- Ô tìm kiếm trống\n"
       "-「検索結果： 4500人」— quay lại toàn bộ friend\n"
       "- Trạng thái chọn friend cũng được reset về「選択中 0人」",
       spec="Đã hỏi leader",
       note="Nguồn: ui-spec.md (link「クリア」— reset bộ lọc, navigate lại /basic/friendlist). "
            "Corpus không có TC riêng cho「クリア」→ expected do AI viết bám spec, cần Leader "
            "xác nhận, đặc biệt phần reset trạng thái chọn."),
]
