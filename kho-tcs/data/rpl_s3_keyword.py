# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Nhóm 3: キーワード設定 (利用設定, độ dài, trùng lặp, checkbox 【〇〇】)."""
from _common import tc

FORM = ("- Đăng nhập admin, bot A\n- Màn /basic/reply/new (form tạo quy tắc auto reply)\n"
        "- Đã cấu hình 1 action gửi text để quan sát được kết quả phía LINE")
FR = "\n- 1 friend LINE đã kết bạn với bot A"

S3 = [
    # ═══════════════ Form — 利用設定 全てのメッセージ ═══════════════
    tc("Form — 利用設定 全てのメッセージ", "FUNC-001", "Normal",
       "利用設定 =「全てのメッセージに反応」⇒ keyword_reaction_type = 0, KHÔNG lưu bản ghi nào vào bảng keyword",
       FORM,
       "1. Ở Phần 3, chọn 利用設定 =「全てのメッセージに反応」\n2. Lưu quy tắc\n"
       "3. Query: SELECT keyword_reaction_type FROM auto_reply WHERE id=<rule>\n"
       "4. Query: SELECT * FROM keyword WHERE auto_reply_id=<rule>",
       "利用設定 =「全てのメッセージに反応」",
       "- DB: auto_reply.keyword_reaction_type = 0\n- Bảng keyword: 0 bản ghi cho quy tắc này\n"
       "- Màn list hiện cột「キーワード」=「全てのメッセージ」",
       note="Nguồn: Ver1.0 r32"),

    tc("Form — 利用設定 全てのメッセージ", "OUT-TRUTH-001", "Normal",
       "Quy tắc 全てのメッセージ: friend gửi BẤT KỲ nội dung nào ⇒ đều nhận được action",
       FORM + FR + "\n- Đã tạo quy tắc 全てのメッセージ với action gửi text「OK」",
       "1. Friend gửi text bất kỳ「あいうえお」\n2. Quan sát LINE app\n3. Friend gửi text khác「12345」\n4. Quan sát LINE app",
       "2 nội dung khác nhau:「あいうえお」và「12345」",
       "- Cả 2 lần friend đều nhận được「OK」trên LINE app\n- Màn chat 1:1 hiện message trả về với trigger 自動応答",
       env="PRODUCTION",
       note="2 input cùng 1 kết quả nên giữ chung. RULE-06 đi tới LINE app. Nguồn: Ver1.0 r32"),

    tc("Form — 利用設定 全てのメッセージ", "UI-002", "Normal",
       "利用設定 =「全てのメッセージに反応」⇒ ẩn「反応条件」và ô nhập キーワード, chỉ hiện checkbox 【〇〇】",
       FORM,
       "1. Chọn 利用設定 =「全てのメッセージに反応」\n2. Quan sát các field trong Phần 3\n"
       "3. Đổi sang「設定したキーワードに反応」\n4. Quan sát lại",
       "2 giá trị của 利用設定",
       "- Khi「全てのメッセージに反応」: CHỈ hiện checkbox「【〇〇】のメッセージには反応させない」; "
       "「反応条件」và「キーワード」bị ẩn\n"
       "- Khi「設定したキーワードに反応」: hiện thêm「反応条件」,「キーワード」và nút (+) thêm keyword",
       note="Conditional display theo ui-spec.md §Phần 3. Corpus KHÔNG có TC ẩn/hiện field ⇒ TC lấp GAP do AI viết"),

    # ═══════════════ Form — 利用設定 キーワード ═══════════════
    tc("Form — 利用設定 キーワード", "FUNC-001", "Normal",
       "利用設定 =「設定したキーワードに反応」với 1 keyword ⇒ INSERT bảng keyword + friend gửi keyword nhận được action",
       FORM + FR,
       "1. Chọn 利用設定 =「設定したキーワードに反応」\n2. Nhập keyword「keyA」\n3. Lưu\n"
       "4. Query: SELECT * FROM keyword WHERE auto_reply_id=<rule>\n5. Friend gửi「keyA」\n6. Quan sát LINE app",
       "Keyword「keyA」",
       "- DB: keyword có 1 bản ghi「keyA」, auto_reply.keyword_reaction_type = 1\n"
       "- Friend gửi「keyA」→ NHẬN được action trên LINE app",
       env="PRODUCTION",
       note="Verify 2 tầng DB + output LINE (RULE-07). Nguồn: Ver1.0 r30"),

    tc("Form — 利用設定 キーワード", "FUNC-MULTI-001", "Normal",
       "Nhiều keyword trong 1 quy tắc ⇒ INSERT đủ bản ghi; friend gửi BẤT KỲ keyword nào cũng nhận được action (mode OR)",
       FORM + FR,
       "1. Chọn「設定したキーワードに反応」, 反応条件 =「どれか1つのキーワードに当てはまる時に反応」\n"
       "2. Nhập 3 keyword: keyA, keyB, keyC (dùng nút (+) thêm dòng)\n3. Lưu\n"
       "4. Query keyword WHERE auto_reply_id=<rule>\n5. Friend gửi「keyB」\n6. Quan sát LINE app",
       "3 keyword: keyA / keyB / keyC, 反応条件 = OR",
       "- DB: bảng keyword có đúng 3 bản ghi\n- Friend gửi「keyB」→ NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r31"),

    tc("Form — 利用設定 キーワード", "UI-FIELD-001", "Normal",
       "反応条件 = AND「全てのキーワードに当てはまる時に反応」⇒ auto_reply.logical = 0, chỉ khớp khi text chứa TẤT CẢ keyword",
       FORM + FR,
       "1. Chọn「設定したキーワードに反応」, 反応条件 =「全てのキーワードに当てはまる時に反応」\n"
       "2. Nhập 2 keyword「予約」và「変更」, cả 2 để 部分一致\n3. Lưu\n"
       "4. Query: SELECT logical FROM auto_reply WHERE id=<rule>\n"
       "5. Friend gửi「予約を変更したい」→ quan sát\n6. Friend gửi「予約したい」→ quan sát",
       "反応条件 = AND; keyword「予約」+「変更」(部分一致)",
       "- DB: auto_reply.logical = 0\n"
       "- Friend gửi「予約を変更したい」(chứa cả 2): NHẬN được action\n"
       "- Friend gửi「予約したい」(thiếu「変更」): KHÔNG nhận được action",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-18 + §7 Keyword Matching: logical=0 (AND) khớp khi totalm == totalk. Corpus KHÔNG có TC cho 反応条件 "
            "AND/OR ⇒ TC lấp GAP do AI viết theo spec. ⚠️ Cột `logical` có nghĩa KHÁC nhau ở bảng auto_reply (AND/OR) "
            "và bảng keyword (完全/部分一致) — NHE-07"),

    tc("Form — 利用設定 キーワード", "UI-FIELD-001", "Normal",
       "反応条件 = OR「どれか1つのキーワードに当てはまる時に反応」⇒ auto_reply.logical = 1, khớp khi có ≥1 keyword",
       FORM + FR,
       "1. Chọn 反応条件 =「どれか1つのキーワードに当てはまる時に反応」\n2. Nhập 2 keyword「予約」và「変更」\n3. Lưu\n"
       "4. Query logical\n5. Friend gửi「予約したい」→ quan sát",
       "反応条件 = OR; keyword「予約」+「変更」",
       "- DB: auto_reply.logical = 1\n- Friend gửi「予約したい」(chỉ khớp 1 keyword): NHẬN được action",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC lấp GAP do AI viết theo §7 Keyword Matching (logical=1 → totalm > 0)"),

    tc("Form — 利用設定 キーワード", "MSG-USER-001", "Normal",
       "keyword.logical = 0「完全一致」⇒ chỉ khớp khi text người dùng BẰNG ĐÚNG keyword (phân biệt hoa/thường)",
       FORM + FR,
       "1. Tạo quy tắc keyword「Key」, chọn「完全一致」\n2. Lưu\n"
       "3. Friend gửi「Key」→ quan sát\n4. Friend gửi「key」(khác hoa/thường) → quan sát\n"
       "5. Friend gửi「Keyword」(chứa nhưng dài hơn) → quan sát",
       "Keyword「Key」完全一致; text gửi:「Key」/「key」/「Keyword」",
       "- Gửi「Key」: NHẬN được action\n- Gửi「key」: KHÔNG nhận (utf8mb4_bin phân biệt hoa/thường)\n"
       "- Gửi「Keyword」: KHÔNG nhận",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="BR-18: exact match dùng COLLATE utf8mb4_bin → CASE-SENSITIVE. Corpus KHÔNG test hoa/thường ⇒ "
            "TC lấp GAP do AI viết theo spec, là điểm rủi ro cao vì người dùng LINE hay gõ hoa/thường tùy ý. MT-08"),

    tc("Form — 利用設定 キーワード", "MSG-USER-001", "Normal",
       "keyword.logical = 1「部分一致」⇒ khớp khi text người dùng CHỨA keyword",
       FORM + FR,
       "1. Tạo quy tắc keyword「予約」, chọn「部分一致」\n2. Lưu\n"
       "3. Friend gửi「予約したいです」→ quan sát\n4. Friend gửi「キャンセル」→ quan sát",
       "Keyword「予約」部分一致",
       "- Gửi「予約したいです」: NHẬN được action (LOCATE > 0)\n- Gửi「キャンセル」: KHÔNG nhận",
       env="PRODUCTION",
       note="BR-18: LOCATE(keyword, val). Nguồn gián tiếp: Ver1.0 r19-r20 (ma trận checkbox 【〇〇】)"),

    tc("Form — 利用設定 キーワード", "UI-INPUT-001", "Abnormal",
       "Chọn「設定したキーワードに反応」nhưng KHÔNG nhập keyword nào ⇒ báo lỗi キーワードを1つ以上設定して下さい。, không lưu",
       FORM,
       "1. Chọn 利用設定 =「設定したキーワードに反応」\n2. Để trống ô keyword\n3. Click「登録」\n"
       "4. Query: SELECT * FROM auto_reply WHERE bot_id=A ORDER BY id DESC LIMIT 1",
       "Ô keyword: (rỗng)",
       "- Hiển thị lỗi「キーワードを1つ以上設定して下さい。」\n- KHÔNG tạo bản ghi auto_reply mới\n- Vẫn ở màn form",
       note="Validation Flow V2 (logic-spec.md:607). Nguồn: Ver1.0 r188 + r193 (Bug #38413, 07/2026) — "
            "corpus test với cả ký tự latinh/đặc biệt và text Nhật, cùng 1 kết quả nên giữ chung"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Bug KH #32967: đổi từ dạng keyword A → 全てのメッセージ ⇒ XÓA keyword A khỏi bảng keyword",
       FORM + FR + "\n- Đã có quy tắc R1 dạng keyword「keyA」",
       "1. Mở edit R1\n2. Đổi 利用設定 sang「全てのメッセージに反応」\n3. Lưu\n"
       "4. Query: SELECT * FROM keyword WHERE auto_reply_id=<R1>\n5. Friend gửi text bất kỳ\n6. Quan sát LINE app",
       "Từ keyword「keyA」→「全てのメッセージに反応」",
       "- Bảng keyword: KHÔNG còn bản ghi「keyA」(bị xóa)\n- Friend gửi text bất kỳ → NHẬN được action",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r33 (Bug KH #32967 [02-12-2025][9119]). Cách fix: 'Xóa hết keyword của auto_reply khi "
            "chọn đối ứng all msg'. ⚠️ Rule này KHÔNG có trong bảng Business Rules của spec ⇒ MT-09"),

    tc("Form — 利用設定 キーワード", "FUNC-UNIQ-001", "Normal",
       "Sau khi R1 chuyển sang 全てのメッセージ → tạo quy tắc MỚI với chính keyword「keyA」⇒ tạo thành công",
       FORM + "\n- Vừa đổi R1 từ keyword「keyA」sang 全てのメッセージ",
       "1. Click「新規作成」\n2. Chọn「設定したキーワードに反応」, nhập「keyA」\n3. Lưu\n"
       "4. Query: SELECT * FROM keyword WHERE keyword='keyA'",
       "Keyword「keyA」",
       "- Tạo thành công, KHÔNG báo「キーワードは既に登録されています。」\n- Bảng keyword có 1 bản ghi「keyA」mới",
       note="Đây chính là bug KH #32967 gốc: keyword cũ không bị xóa nên báo trùng dù user không thấy keyword đâu. "
            "Nguồn: Ver1.0 r34"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Đổi từ dạng NHIỀU keyword → 全てのメッセージ ⇒ xóa TOÀN BỘ keyword của quy tắc",
       FORM + FR + "\n- Quy tắc R2 có 3 keyword: k1, k2, k3",
       "1. Mở edit R2, đổi sang「全てのメッセージに反応」\n2. Lưu\n"
       "3. Query: SELECT * FROM keyword WHERE auto_reply_id=<R2>\n4. Friend gửi text bất kỳ → quan sát",
       "3 keyword k1/k2/k3",
       "- Bảng keyword: 0 bản ghi cho R2\n- Friend gửi text bất kỳ → NHẬN được action",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r35"),

    tc("Form — 利用設定 キーワード", "FUNC-UNIQ-001", "Normal",
       "Sau khi R2 chuyển sang 全てのメッセージ → tạo quy tắc mới với 1 trong các keyword cũ ⇒ tạo thành công",
       FORM + "\n- Vừa đổi R2 (3 keyword) sang 全てのメッセージ",
       "1. Tạo quy tắc mới với keyword「k2」\n2. Lưu\n3. Query bảng keyword",
       "Keyword「k2」",
       "- Tạo thành công, không báo trùng\n- Bảng keyword có bản ghi「k2」mới",
       note="Nguồn: Ver1.0 r36"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Đổi từ 全てのメッセージ → dạng keyword B ⇒ INSERT keyword B; chỉ text khớp B mới nhận action",
       FORM + FR + "\n- Quy tắc R3 đang là 全てのメッセージ",
       "1. Mở edit R3, đổi sang「設定したキーワードに反応」, nhập keyword「keyB」\n2. Lưu\n"
       "3. Query bảng keyword\n4. Friend gửi「keyB」→ quan sát\n5. Friend gửi「xyz」→ quan sát",
       "Keyword「keyB」",
       "- Bảng keyword có bản ghi「keyB」\n- Friend gửi「keyB」: NHẬN được action\n- Friend gửi「xyz」: KHÔNG nhận",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r37"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Đổi từ 全てのメッセージ → dạng NHIỀU keyword ⇒ INSERT đủ keyword; chỉ text khớp mới nhận action",
       FORM + FR + "\n- Quy tắc R4 đang là 全てのメッセージ",
       "1. Mở edit R4, đổi sang「設定したキーワードに反応」, nhập 3 keyword b1/b2/b3\n2. Lưu\n"
       "3. Query bảng keyword\n4. Friend gửi「b2」→ quan sát\n5. Friend gửi「zzz」→ quan sát",
       "3 keyword b1/b2/b3",
       "- Bảng keyword có đủ 3 bản ghi\n- Friend gửi「b2」: NHẬN được action\n- Friend gửi「zzz」: KHÔNG nhận",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r39"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Đổi keyword A → keyword B trong cùng quy tắc ⇒ xóa A, thêm B; A không còn trigger, B trigger được",
       FORM + FR + "\n- Quy tắc R5 dạng keyword「keyA」",
       "1. Mở edit R5, sửa keyword thành「keyB」\n2. Lưu\n"
       "3. Query: SELECT keyword FROM keyword WHERE auto_reply_id=<R5>\n"
       "4. Friend gửi「keyA」→ quan sát\n5. Friend gửi「keyB」→ quan sát",
       "Từ「keyA」→「keyB」",
       "- Bảng keyword: chỉ còn「keyB」, KHÔNG còn「keyA」\n"
       "- Friend gửi「keyA」: KHÔNG nhận action\n- Friend gửi「keyB」: NHẬN được action",
       env="PRODUCTION",
       note="4 bước verify của cùng 1 hành động sửa (RULE-07) nên giữ chung. Nguồn: Ver1.0 r41"),

    tc("Form — 利用設定 キーワード", "FUNC-UNIQ-001", "Normal",
       "Sau khi R5 đổi A → B: tạo quy tắc mới với keyword A ⇒ tạo thành công (A đã được giải phóng)",
       FORM + "\n- Vừa đổi R5 từ keyA sang keyB",
       "1. Tạo quy tắc mới với keyword「keyA」\n2. Lưu\n3. Query bảng keyword",
       "Keyword「keyA」",
       "- Tạo thành công, không báo trùng\n- Bảng keyword có bản ghi「keyA」mới",
       note="Nguồn: Ver1.0 r42"),

    tc("Form — 利用設定 キーワード", "FUNC-SEQ-001", "Normal",
       "Chuyển đi chuyển lại giữa 全てのメッセージ và キーワード nhiều lần rồi lưu ⇒ dữ liệu lưu theo thao tác CUỐI CÙNG",
       FORM + FR,
       "1. Mở form, chọn キーワード, nhập「kX」\n2. Đổi sang 全てのメッセージ\n3. Đổi lại キーワード, nhập「kY」\n"
       "4. Đổi sang 全てのメッセージ lần nữa\n5. Click「登録」\n"
       "6. Query keyword_reaction_type + bảng keyword\n7. Friend gửi text bất kỳ → quan sát",
       "Chuỗi: キーワード(kX) → 全て → キーワード(kY) → 全て → lưu",
       "- DB: keyword_reaction_type = 0\n- Bảng keyword: 0 bản ghi cho quy tắc (cả kX và kY đều không lưu)\n"
       "- Friend gửi text bất kỳ: NHẬN được action",
       env="PRODUCTION",
       note="Chuỗi thao tác liên tiếp (FUNC-SEQ) nên giữ chung. Nguồn: Ver1.0 r51 'Lưu lại thao tác lần cuối cùng'"),

    # ═══════════════ Keyword — độ dài & trim ═══════════════
    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: nhập keyword 200 ký tự ⇒ DB chỉ lưu 30 ký tự đầu; màn list và màn edit hiển thị đúng 30 ký tự",
       FORM,
       "1. Chọn「設定したキーワードに反応」\n2. Nhập keyword dài 200 ký tự\n3. Click ra ngoài ô input, quan sát\n"
       "4. Lưu quy tắc\n5. Query: SELECT keyword, CHAR_LENGTH(keyword) FROM keyword WHERE auto_reply_id=<rule>\n"
       "6. Xem màn list\n7. Mở lại màn edit",
       "Keyword 200 ký tự latinh",
       "- DB: CHAR_LENGTH(keyword) = 30, nội dung = 30 ký tự đầu\n"
       "- Màn list hiển thị đúng 30 ký tự, KHÔNG thừa\n- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r175-r176 + r185 (Bug tự detect #38413, 07/2026). ⚠️ Bug gốc: hệ thống lưu >30 ký tự. "
            "Spec: db-mapping.md:101 khai báo keyword varchar(200), Validation Flow V2 (logic-spec.md:606-612) "
            "KHÔNG có rule 30 ký tự ⇒ MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: keyword ĐÚNG 30 ký tự (biên hợp lệ) ⇒ lưu nguyên 30, không bị cắt bớt",
       FORM,
       "1. Nhập keyword đúng 30 ký tự\n2. Lưu\n3. Query CHAR_LENGTH(keyword)\n4. Xem màn list và màn edit",
       "Keyword đúng 30 ký tự",
       "- DB: lưu nguyên 30 ký tự, không cắt\n- Màn list hiển thị nguyên 30 ký tự, không thừa\n"
       "- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r177 + r187. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: keyword 31 ký tự (ngay trên biên) ⇒ bị cắt còn 30",
       FORM,
       "1. Nhập keyword 31 ký tự\n2. Lưu\n3. Query CHAR_LENGTH(keyword)\n4. Xem màn list và màn edit",
       "Keyword 31 ký tự",
       "- DB: lưu đúng 30 ký tự\n- Màn list hiển thị nguyên 30 ký tự, không thừa\n- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r178 + r186. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Normal",
       "Bug #38413: keyword ngắn (10 ký tự) ⇒ giữ nguyên, không bị đệm/cắt",
       FORM,
       "1. Nhập keyword 10 ký tự\n2. Lưu\n3. Query CHAR_LENGTH(keyword)",
       "Keyword 10 ký tự",
       "- DB: lưu nguyên 10 ký tự",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r179. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "DATA-TEXT-001", "Boundary",
       "Bug #38413: keyword tiếng Nhật 200 ký tự ⇒ cắt theo 30 KÝ TỰ (không phải 30 byte)",
       FORM,
       "1. Nhập keyword tiếng Nhật (full-width) dài 200 ký tự\n2. Lưu\n"
       "3. Query: SELECT CHAR_LENGTH(keyword), LENGTH(keyword) FROM keyword WHERE auto_reply_id=<rule>\n"
       "4. Xem màn list và màn edit",
       "200 ký tự tiếng Nhật full-width, VD「あいうえお…」lặp lại",
       "- DB: CHAR_LENGTH = 30 (đúng 30 ký tự tiếng Nhật), KHÔNG bị cắt nhầm còn 10 ký tự do đếm byte\n"
       "- Màn list hiển thị nguyên 30 ký tự, không thừa\n- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Điểm rủi ro cao nhất của bug #38413 — đếm ký tự vs byte. Nguồn: Ver1.0 r180 + r194-r195. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: SỬA keyword đang có, nhập lại 50 ký tự ⇒ update cũng chỉ lưu 30",
       FORM + "\n- Đã có quy tắc với keyword 10 ký tự",
       "1. Mở edit quy tắc\n2. Xóa keyword cũ, nhập keyword mới 50 ký tự\n3. Lưu\n"
       "4. Query CHAR_LENGTH(keyword)\n5. Xem màn list và màn edit",
       "Keyword mới 50 ký tự",
       "- DB: update còn đúng 30 ký tự\n- Màn list hiển thị nguyên 30 ký tự\n- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Nhánh EDIT (không chỉ CREATE) — dễ lọt. Nguồn: Ver1.0 r181. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: 1 quy tắc có 5 keyword độ dài 10/20/31/50/300 ⇒ cắt ĐỘC LẬP từng keyword",
       FORM,
       "1. Chọn「設定したキーワードに反応」\n2. Thêm 5 dòng keyword lần lượt dài 10 / 20 / 31 / 50 / 300 ký tự\n"
       "3. Lưu\n4. Query: SELECT keyword, CHAR_LENGTH(keyword) FROM keyword WHERE auto_reply_id=<rule> ORDER BY id",
       "5 keyword: 10 / 20 / 31 / 50 / 300 ký tự",
       "- DB lưu lần lượt: 10 / 20 / 30 / 30 / 30 ký tự\n"
       "- Không keyword nào bị cắt sai hoặc bị bỏ qua",
       spec="Spec không ghi",
       note="Ma trận 5 điểm có kết quả tính được từ cùng 1 quy tắc, kết quả từng điểm ghi rõ. "
            "Nguồn: Ver1.0 r182. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "DATA-TEXT-001", "Boundary",
       "Bug #38413: keyword 30 ký tự CÓ khoảng trắng ở ĐẦU ⇒ tự trim khoảng trắng đầu",
       FORM,
       "1. Nhập keyword gồm khoảng trắng đầu + 30 ký tự nội dung\n2. Lưu\n"
       "3. Query: SELECT keyword, CHAR_LENGTH(keyword) — kiểm tra ký tự đầu tiên",
       "Input:「␣␣<30 ký tự nội dung>」",
       "- DB: keyword KHÔNG bắt đầu bằng khoảng trắng (đã trim)\n- Nội dung giữ đủ phần chữ",
       spec="Spec không ghi",
       note="Nguồn: Ver1.0 r183 + r191. ⚠️ Spec job-spec.md:304 chỉ ghi `TextUtils.trimEnd()` (trim CUỐI) ở tầng "
            "SO KHỚP runtime, KHÔNG mô tả trim ĐẦU ở tầng LƯU ⇒ MT-02"),

    tc("Keyword — độ dài & trim", "DATA-TEXT-001", "Boundary",
       "Bug #38413: keyword 40 ký tự CÓ khoảng trắng đầu ⇒ trim khoảng trắng đầu rồi đếm đủ 30 ký tự nội dung",
       FORM,
       "1. Nhập keyword gồm khoảng trắng đầu + 40 ký tự nội dung\n2. Lưu\n"
       "3. Query keyword + CHAR_LENGTH\n4. Xem màn list và màn edit",
       "Input:「␣␣<40 ký tự nội dung>」",
       "- DB: đã trim khoảng trắng đầu, đếm 30 ký tự TỪ ký tự khác khoảng trắng đầu tiên\n"
       "- CHAR_LENGTH = 30\n- Màn list hiển thị nguyên 30 ký tự, không thừa\n- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Đây là biên khó nhất: trim TRƯỚC rồi mới cắt 30. Nguồn: Ver1.0 r184 + r192 + r197. Gắn MT-01, MT-02"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Abnormal",
       "Bug #38413: bỏ trống keyword → báo lỗi → nhập lại 31 ký tự ⇒ lưu đúng 30 ký tự đầu",
       FORM,
       "1. Chọn「設定したキーワードに反応」, để trống keyword, click「登録」→ nhận lỗi\n"
       "2. Nhập keyword 31 ký tự\n3. Click「登録」lại\n4. Query CHAR_LENGTH(keyword)\n5. Xem màn list và màn edit",
       "Lần 1: rỗng (lỗi); lần 2: 31 ký tự",
       "- Lần 1: lỗi「キーワードを1つ以上設定して下さい。」\n"
       "- Lần 2: lưu thành công, DB đúng 30 ký tự đầu\n- Màn list và màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="Chuỗi lỗi → sửa → lưu là 1 thao tác liền mạch. Corpus test riêng cho ký tự latinh/đặc biệt (r189) và "
            "text Nhật (r194) — cùng kết quả nên giữ chung. Gắn MT-01"),

    tc("Keyword — độ dài & trim", "UI-INPUT-001", "Boundary",
       "Bug #38413: bỏ trống keyword → báo lỗi → nhập lại ĐÚNG 30 ký tự ⇒ lưu nguyên 30, không bị ngắt",
       FORM,
       "1. Để trống keyword, click「登録」→ nhận lỗi\n2. Nhập keyword đúng 30 ký tự\n3. Lưu\n"
       "4. Query CHAR_LENGTH\n5. Xem màn list và màn edit",
       "Lần 1: rỗng; lần 2: đúng 30 ký tự (thử cả latinh và tiếng Nhật)",
       "- Lưu nguyên 30 ký tự, không bị ngắt\n- Màn list hiển thị nguyên 30 ký tự, không thừa\n"
       "- Màn edit hiển thị đúng 30 ký tự",
       spec="Spec không ghi",
       note="2 loại ký tự cùng 1 kết quả nên giữ chung. Nguồn: Ver1.0 r190 + r195. Gắn MT-01"),

    # ═══════════════ Keyword — trùng & đồng bộ bảng keyword ═══════════════
    tc("Keyword — trùng & đồng bộ bảng keyword", "FUNC-UNIQ-001", "Abnormal",
       "BR-01: tạo quy tắc mới với keyword ĐÃ tồn tại ở quy tắc khác trong CÙNG bot ⇒ báo キーワードは既に登録されています。",
       FORM + "\n- Quy tắc R1 đang dùng keyword「keyB」",
       "1. Click「新規作成」\n2. Chọn「設定したキーワードに反応」, nhập「keyB」\n3. Click「登録」\n"
       "4. Query: SELECT COUNT(*) FROM auto_reply WHERE bot_id=A AND is_deleted=0",
       "Keyword「keyB」đã tồn tại ở R1",
       "- Báo lỗi「キーワードは既に登録されています。」\n- Response có arraySameWord chỉ đúng index keyword bị trùng\n"
       "- KHÔNG tạo quy tắc mới (COUNT không tăng)",
       note="BR-01. Nguồn: Ver1.0 r38 + r40"),

    tc("Keyword — trùng & đồng bộ bảng keyword", "FUNC-UNIQ-001", "Abnormal",
       "BR-01: nhập nhiều keyword trong đó có 1 keyword trùng ⇒ báo lỗi và chỉ rõ dòng bị trùng, KHÔNG lưu quy tắc",
       FORM + "\n- Quy tắc R1 đang dùng keyword「keyB」",
       "1. Tạo quy tắc mới với 3 keyword: 「new1」,「keyB」,「new3」\n2. Click「登録」\n"
       "3. Quan sát dòng keyword được đánh dấu lỗi\n4. Query bảng keyword tìm「new1」và「new3」",
       "3 keyword: new1 / keyB (trùng) / new3",
       "- Báo lỗi「キーワードは既に登録されています。」\n- Dòng keyword số 2 (keyB) được đánh dấu lỗi (arraySameWord = [1])\n"
       "- KHÔNG lưu quy tắc;「new1」và「new3」cũng KHÔNG được lưu vào bảng keyword",
       spec="Spec không ghi",
       note="Corpus chỉ có case n=1 trùng (r38/r40) — case batch có 1 dòng trùng do AI suy luận từ arraySameWord "
            "là MẢNG index. ĐÂY LÀ SUY LUẬN CỦA AI ⇒ MT-10, CẦN LEADER XÁC NHẬN (reject cả batch hay chỉ bỏ dòng trùng?)"),

    tc("Keyword — trùng & đồng bộ bảng keyword", "SEC-ISO-001", "Normal",
       "BR-01: bot B tạo quy tắc với keyword TRÙNG keyword đang dùng ở bot A ⇒ CHO PHÉP tạo (unique theo bot)",
       "- Bot A đã có quy tắc dùng keyword「共通キー」\n- Đổi sang bot B, mở /basic/reply/new",
       "1. Ở bot B, tạo quy tắc keyword「共通キー」\n2. Lưu\n"
       "3. Query: SELECT k.keyword, a.bot_id FROM keyword k JOIN auto_reply a ON k.auto_reply_id=a.id "
       "WHERE k.keyword='共通キー'",
       "Keyword「共通キー」ở cả bot A và bot B",
       "- Lưu thành công, KHÔNG báo trùng\n- DB có 2 bản ghi keyword「共通キー」thuộc 2 bot khác nhau",
       note="Suy ra từ BR-01 (unique trong bot) + Ver1.0 r50 (đã xác nhận 2 bot có cùng keyword). "
            "Nhánh CREATE do AI viết bổ sung"),

    tc("Keyword — trùng & đồng bộ bảng keyword", "DATA-MIG-001", "Normal",
       "Bug KH #32967 — job recover: dọn keyword rác của các auto_reply dạng 全てのメッセージ (keyword_reaction_type=0) "
       "và auto_reply đã xóa (is_deleted=1)",
       "- Bot có sẵn dữ liệu rác: keyword còn tồn tại của quy tắc dạng 全てのメッセージ và của quy tắc đã bị xóa\n"
       "- Có quy tắc dạng keyword (keyword_reaction_type=1) còn sống để đối chứng",
       "1. Query trước: SELECT * FROM keyword WHERE auto_reply_id IN "
       "(SELECT id FROM auto_reply WHERE bot_id=? AND (keyword_reaction_type=0 OR is_deleted=1))\n"
       "2. Dev chạy lệnh recover\n3. Query lại đúng câu trên\n"
       "4. Query đối chứng: keyword của auto_reply có keyword_reaction_type=1 và is_deleted=0",
       "Câu query kiểm tra: SELECT * FROM keyword WHERE auto_reply_id in "
       "(SELECT id FROM auto_reply WHERE keyword_reaction_type = 0 or is_deleted = 1)",
       "- Sau recover: 0 bản ghi keyword cho các auto_reply dạng 全てのメッセージ và auto_reply đã xóa\n"
       "- Keyword của các auto_reply dạng keyword (type=1, chưa xóa) VẪN CÒN NGUYÊN",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="RULE-08: lệnh recover chạy trên môi trường thật. Nguồn: Ver1.0 r53-r54. "
            "⚠️ Spec §7 Background Jobs KHÔNG mô tả command recover này ⇒ MT-11"),

    # ═══════════════ Checkbox 【〇〇】には反応させない ═══════════════
    tc("Checkbox 【〇〇】には反応させない", "UI-FIELD-001", "Normal",
       "Checkbox「【〇〇】のメッセージには反応させない」nằm dưới khối setting keyword, mặc định KHÔNG tick",
       FORM,
       "1. Mở form tạo mới\n2. Quan sát vị trí và trạng thái mặc định của checkbox trong Phần 3\n"
       "3. Lưu quy tắc không đụng vào checkbox\n4. Query: SELECT is_no_reply_button FROM auto_reply WHERE id=<rule>",
       "Không tick checkbox",
       "- Checkbox nằm phía dưới khối setting keyword, nhãn「【〇〇】のメッセージには反応させない」\n"
       "- Mặc định KHÔNG được tick\n- DB: is_no_reply_button = 0",
       note="Nguồn: Ver1.0 r3-r4"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Normal",
       "Quy tắc 全てのメッセージ + TICK checkbox: friend bấm nút reply (text dạng【xxx】) ⇒ KHÔNG gửi action",
       FORM + FR + "\n- Quy tắc dạng 全てのメッセージ, đã TICK checkbox\n- Có template button với nút reply gửi text「【予約】」",
       "1. Tạo quy tắc 全てのメッセージ, tick checkbox, lưu\n2. Gửi template button cho friend\n"
       "3. Friend bấm nút reply (LINE gửi text「【予約】」)\n4. Quan sát LINE app và màn chat 1:1",
       "Text friend gửi:「【予約】」(dạng nút reply)",
       "- Friend KHÔNG nhận được action auto reply\n- Màn chat 1:1 hiện tin nhắn của friend nhưng KHÔNG có message trả về",
       env="PRODUCTION",
       note="BR-17: text bắt đầu「【」kết thúc「】」→ skip rule. Nguồn: Ver1.0 r5"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Normal",
       "Quy tắc 全てのメッセージ + TICK checkbox: friend gửi text THƯỜNG (không có 【】) ⇒ VẪN gửi action",
       FORM + FR + "\n- Quy tắc 全てのメッセージ, đã tick checkbox",
       "1. Friend gửi text thường「xxx」\n2. Quan sát LINE app",
       "Text:「xxx」(không có 【】)",
       "- Friend NHẬN được action bình thường",
       env="PRODUCTION",
       note="Nguồn: Ver1.0 r6"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Normal",
       "Quy tắc 全てのメッセージ + KHÔNG tick checkbox: cả text【xxx】và text thường ⇒ ĐỀU gửi action",
       FORM + FR + "\n- Quy tắc 全てのメッセージ, KHÔNG tick checkbox",
       "1. Friend bấm nút reply (text「【xxx】」) → quan sát\n2. Friend gửi text thường「xxx」→ quan sát",
       "2 loại text:「【xxx】」và「xxx」",
       "- Cả 2 lần friend đều NHẬN được action",
       env="PRODUCTION",
       note="2 input cùng 1 kết quả nên giữ chung. Nguồn: Ver1.0 r7-r8"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "Ma trận TICK checkbox × keyword「key」(không có 【】) × text người dùng ⇒ mọi text dạng【…】đều bị skip",
       FORM + FR + "\n- Quy tắc dạng keyword, TICK checkbox",
       "1. Setting keyword「key」chế độ 完全一致 → friend gửi「【key】」→ quan sát; friend gửi「key」→ quan sát\n"
       "2. Đổi keyword「key」sang chế độ 部分一致 → friend gửi「【key】」→ quan sát; friend gửi「key」→ quan sát",
       "Keyword「key」(không có ngoặc); text gửi:「【key】」và「key」; 2 chế độ 完全一致 / 部分一致",
       "- 完全一致 + gửi「【key】」: KHÔNG gửi action (bị skip do 【】)\n- 完全一致 + gửi「key」: GỬI action\n"
       "- 部分一致 + gửi「【key】」: KHÔNG gửi action (bị skip do 【】)\n- 部分一致 + gửi「key」: GỬI action",
       env="PRODUCTION",
       note="Ma trận 4 điểm, kết quả từng điểm ghi rõ ở Kết quả mong đợi. Nguồn: Ver1.0 r9-r12"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "Ma trận TICK checkbox × keyword CÓ 【】(「【key】」) × text người dùng ⇒ KHÔNG BAO GIỜ gửi action",
       FORM + FR + "\n- Quy tắc dạng keyword, TICK checkbox",
       "1. Setting keyword「【key】」chế độ 完全一致 → friend gửi「【key】」rồi「key」→ quan sát mỗi lần\n"
       "2. Đổi sang 部分一致 → friend gửi「【key】」rồi「key」→ quan sát mỗi lần",
       "Keyword「【key】」; text gửi:「【key】」và「key」; 2 chế độ so khớp",
       "- Cả 4 tổ hợp đều KHÔNG gửi action:\n"
       "  · gửi「【key】」bị skip vì checkbox đang tick\n  · gửi「key」không khớp keyword「【key】」",
       env="PRODUCTION",
       note="4 điểm cùng 1 kết quả (không gửi) nên giữ chung, nhưng 2 nguyên nhân khác nhau đã ghi rõ. "
            "⚠️ Đây là bẫy cấu hình: tick checkbox + keyword có 【】 ⇒ quy tắc VÔ HIỆU HOÀN TOÀN. "
            "Nguồn: Ver1.0 r13-r16"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "KHÔNG tick checkbox + keyword「key」完全一致: gửi「【key】」⇒ KHÔNG gửi (không khớp exact); gửi「key」⇒ GỬI",
       FORM + FR + "\n- Quy tắc keyword, KHÔNG tick checkbox",
       "1. Setting keyword「key」chế độ 完全一致\n2. Friend gửi「【key】」→ quan sát\n3. Friend gửi「key」→ quan sát",
       "Keyword「key」完全一致; text:「【key】」và「key」",
       "- Gửi「【key】」: KHÔNG gửi action — vì 完全一致 so khớp nguyên chuỗi「key」, còn text có ngoặc nên không bằng\n"
       "- Gửi「key」: GỬI action",
       env="PRODUCTION",
       note="Corpus r17 ghi rõ lý do: 'do setting toàn phần là key mà reply có ngoặc nên ko send; nếu setting toàn "
            "phần là 【key】 thì khi user reply 【key】 sẽ send'. Nguồn: Ver1.0 r17-r18"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "KHÔNG tick checkbox + keyword「key」部分一致: gửi「【key】」và「key」⇒ ĐỀU gửi action",
       FORM + FR + "\n- Quy tắc keyword, KHÔNG tick checkbox",
       "1. Setting keyword「key」chế độ 部分一致\n2. Friend gửi「【key】」→ quan sát\n3. Friend gửi「key」→ quan sát",
       "Keyword「key」部分一致",
       "- Cả 2 lần đều GỬI action (LOCATE tìm được「key」trong「【key】」)",
       env="PRODUCTION",
       note="2 điểm cùng kết quả nên giữ chung. Nguồn: Ver1.0 r19-r20"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "KHÔNG tick checkbox + keyword「【key】」完全一致: gửi「【key】」⇒ GỬI; gửi「key」⇒ KHÔNG gửi",
       FORM + FR + "\n- Quy tắc keyword, KHÔNG tick checkbox",
       "1. Setting keyword「【key】」chế độ 完全一致\n2. Friend gửi「【key】」→ quan sát\n3. Friend gửi「key」→ quan sát",
       "Keyword「【key】」完全一致",
       "- Gửi「【key】」: GỬI action (khớp hoàn toàn, checkbox không tick nên không skip)\n"
       "- Gửi「key」: KHÔNG gửi action",
       env="PRODUCTION",
       note="Đây là cách DUY NHẤT để auto reply phản ứng với tin nhắn từ nút reply. Nguồn: Ver1.0 r21-r22"),

    tc("Checkbox 【〇〇】には反応させない", "MSG-USER-001", "Boundary",
       "KHÔNG tick checkbox + keyword「【key】」部分一致: gửi「abc【key】」⇒ GỬI; gửi「key」⇒ KHÔNG gửi",
       FORM + FR + "\n- Quy tắc keyword, KHÔNG tick checkbox",
       "1. Setting keyword「【key】」chế độ 部分一致\n2. Friend gửi「abc【key】」→ quan sát\n3. Friend gửi「key」→ quan sát",
       "Keyword「【key】」部分一致; text:「abc【key】」và「key」",
       "- Gửi「abc【key】」: GỬI action (chứa nguyên cụm「【key】」)\n"
       "- Gửi「key」: KHÔNG gửi action (không chứa ngoặc)",
       env="PRODUCTION",
       note="Corpus r23 ghi ví dụ「abc[key]」. Nguồn: Ver1.0 r23-r24"),

    tc("Checkbox 【〇〇】には反応させない", "FUNC-MULTI-001", "Abnormal",
       "Kết hợp 2 quy tắc: quy tắc 全てのメッセージ KHÔNG tick + quy tắc keyword CÓ tick ⇒ mỗi quy tắc chạy action riêng của nó",
       FORM + FR + "\n- Quy tắc R_all: 全てのメッセージ, KHÔNG tick checkbox, action gửi text「A」\n"
       "- Quy tắc R_key: keyword「key」, CÓ tick checkbox, action gửi text「K」",
       "1. Friend gửi「【key】」→ quan sát tin nhận được\n2. Friend gửi「key」→ quan sát\n"
       "3. Friend gửi ký tự khác「zzz」→ quan sát",
       "3 loại text:「【key】」/「key」/「zzz」",
       "- Gửi「【key】」: nhận「A」(từ R_all, không tick nên vẫn phản ứng); KHÔNG nhận「K」(R_key bị skip do tick)\n"
       "- Gửi「key」: nhận「A」và「K」(cả 2 quy tắc cùng khớp — BR-15 nhiều rule match đồng thời)\n"
       "- Gửi「zzz」: chỉ nhận「A」",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="⚠️ Corpus Ver1.0 r25-r28 đánh dấu 'Not test' với lý do 'ko cần check case kết hợp này vì mỗi cái setting "
            "action riêng'. Spec BR-15 nói vòng lặp KHÔNG break — NHIỀU rule match đồng thời ⇒ MT-03. "
            "Kết quả mong đợi ở đây là AI SUY LUẬN từ BR-15, CẦN LEADER QUYẾT có test hay không"),
]
