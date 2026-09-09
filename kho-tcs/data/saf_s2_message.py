# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 4-6: khối 送信するメッセージを登録 (nút chèn
biến, ô nhập, bộ đếm ký tự) và việc lưu tin nhắn thành bản ghi template.

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」.
Khối tin nhắn lặp gần như y hệt ở 3 trang: r31-r61 (新規), r128-r158 (既存),
r266-r294 (ブロック解除). TC gộp 3 trang khi kết quả mong đợi giống nhau.
"""
from _common import tc

NEW = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
       "- Mở trang 新規友だち用 (/basic/setting-add-friend), tab メッセージ・アクション設定")
ALL3 = ("- Đăng nhập Admin của 1 bot đã liên kết LINE OA\n"
        "- Chuẩn bị mở lần lượt cả 3 trang: 新規友だち用 · 既存友だち用 · ブロック解除時用")

S2 = [
    # ═══════════ 4. 送信するメッセージ — nút chèn biến ═══════════
    tc("送信するメッセージ — nút chèn biến", "UI-001", "Normal",
       "Khối 送信するメッセージを登録 hiển thị đủ tiêu đề, 2 nút chèn biến, ô nhập, bộ đếm",
       ALL3,
       "1. Mở lần lượt 3 trang あいさつメッセージ\n"
       "2. Quan sát khối đăng ký tin nhắn ở mỗi trang",
       "3 trang: add_new / add_old / unblock",
       "- Có tiêu đề khối「送信するメッセージを登録」\n"
       "- Có 2 nút chèn biến:「＋ LINE名」và「＋ 友だち情報」\n"
       "- Có ô nhập nhiều dòng và bộ đếm ký tự dạng x/5,000\n"
       "- Bố cục giống nhau ở cả 3 trang",
       note="Nguồn: r32, r129, r267 + ui-spec.md:65-73."),

    tc("送信するメッセージ — nút chèn biến", "UI-001", "Normal",
       "Tiêu đề section của mỗi trang khác nhau theo loại friend",
       ALL3,
       "1. Mở trang 新規友だち用 → đọc tiêu đề section chứa khối tin nhắn\n"
       "2. Mở trang 既存友だち用 → đọc tiêu đề section\n"
       "3. Mở trang ブロック解除時用 → đọc tiêu đề section",
       "3 trang",
       "- Trang 新規友だち用:「新規友だち追加時メッセージ・アクション設定」\n"
       "- Trang 既存友だち用:「既存友だちに対するメッセージ・アクション設定」\n"
       "- Trang ブロック解除時用:「ブロック解除時のメッセージ・アクション設定」",
       note="Nguồn: r31 (trang 新規) + ui-spec.md:64, :108, :151. ⚠️ Trong tab master, cột Main "
            "Function của khối trang 既存 (r128) và trang unblock (r266) vẫn ghi tiêu đề của trang "
            "新規 — đây là copy-paste của tab nguồn, không phải kết quả mong đợi thật. Expected lấy "
            "theo ui-spec, CẦN VERIFY LẠI trên môi trường thật."),

    tc("送信するメッセージ — nút chèn biến", "UI-001", "Normal",
       "Hover 2 nút chèn biến — ô nhập đậm viền lên",
       ALL3,
       "1. Mở trang 新規友だち用\n"
       "2. Rê chuột lên nút「＋ LINE名」→ quan sát ô nhập\n"
       "3. Rê chuột lên nút「＋ 友だち情報」→ quan sát ô nhập",
       "Dùng chuột trên PC",
       "- Cả 2 lần: ô nhập tin nhắn đậm viền lên (báo hiệu vùng sẽ được chèn)",
       note="Nguồn: r33, r36, r130, r133, r268, r271."),

    tc("送信するメッセージ — nút chèn biến", "FUNC-001", "Normal",
       "Click ＋ LINE名 — chèn biến {name} vào ô nhập",
       NEW,
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Click nút「＋ LINE名」\n"
       "3. Quan sát nội dung ô nhập và bộ đếm ký tự",
       "Ô nhập đang rỗng",
       "- Ô nhập xuất hiện chuỗi {name}\n"
       "- Bộ đếm tăng đúng bằng số ký tự của chuỗi vừa chèn",
       note="Nguồn: r34, r131, r269. Phần『phía user hiển thị tên user』đã tách sang TC riêng ở "
            "nhóm『Kết bạn mới — gửi tin & action』theo RULE-06."),

    tc("送信するメッセージ — nút chèn biến", "FUNC-MULTI-001", "Normal",
       "Double click ＋ LINE名 — chèn 2 lần biến {name}",
       NEW,
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Double click nút「＋ LINE名」\n"
       "3. Quan sát nội dung ô nhập",
       "Ô nhập đang rỗng, double click",
       "- Ô nhập có ĐÚNG 2 chuỗi {name} liên tiếp\n"
       "- Không mất ký tự, không sinh ký tự lạ",
       note="Nguồn: r35, r132, r270."),

    tc("送信するメッセージ — nút chèn biến", "FUNC-001", "Normal",
       "Click ＋ 友だち情報 — mở khối chọn thông tin bạn bè",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Click nút「＋ 友だち情報」\n"
       "3. Quan sát khối hiện ra",
       "Bot có sẵn folder friend info cơ bản",
       "- Hiện khối/popup chọn 友だち情報\n"
       "- Trong khối có các mục của folder cơ bản để chọn",
       note="Nguồn: r37, r134, r272."),

    tc("送信するメッセージ — nút chèn biến", "FUNC-MULTI-001", "Normal",
       "Double click ＋ 友だち情報 — vẫn chỉ mở 1 khối chọn, không chồng 2 lớp",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Double click nút「＋ 友だち情報」\n"
       "3. Quan sát số lớp khối chọn hiện ra",
       "Double click nhanh",
       "- Chỉ hiện 1 khối chọn 友だち情報 (không chồng 2 lớp, không nhấp nháy)",
       note="Nguồn: r38, r135, r273 (『Double click → Hiển thị box Friend Info』). Vế『không chồng "
            "2 lớp』do AI làm rõ để đo được — cần Leader xác nhận."),

    tc("送信するメッセージ — nút chèn biến", "FRIEND-001", "Normal",
       "Chọn 1 mục 友だち情報 — chèn đúng biến của mục đó vào ô nhập",
       NEW + "\n- Bot có sẵn các mục friend info cơ bản: システム表示名, điện thoại di động, "
             "địa chỉ email, ngày sinh",
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Click「＋ 友だち情報」\n"
       "3. Chọn mục「システム表示名」\n"
       "4. Quan sát ô nhập\n"
       "5. Lặp lại với 3 mục còn lại (điện thoại, email, ngày sinh)",
       "4 mục folder cơ bản: システム表示名 · điện thoại di động · địa chỉ email · ngày sinh",
       "- Mỗi lần chọn, ô nhập được chèn thêm đúng 1 biến tương ứng mục đã chọn\n"
       "- Biến của 4 mục KHÁC nhau, không bị chèn nhầm sang mục khác\n"
       "- Bộ đếm ký tự tăng đúng theo độ dài biến vừa chèn",
       note="Nguồn: r58 (『check khi msg có insert các thông tin ở folder cơ bản』, kết quả gốc ghi "
            "[FRIEND_INFO_system_name]) và r154 (liệt kê 4 mục). Gộp 4 mục vì cùng 1 kết quả kiểm."),

    # ═══════════ 5. 送信するメッセージ — ô nhập & bộ đếm ═══════════
    tc("送信するメッセージ — ô nhập & bộ đếm", "UI-INPUT-001", "Normal",
       "Ô nhập là free text — nhận mọi loại ký tự",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Nhập lần lượt các loại ký tự vào ô nhập\n"
       "3. Bấm 保存, F5 rồi đọc lại nội dung",
       "Chữ Nhật (漢字/ひらがな/カタカナ), chữ Latinh, số, ký tự đặc biệt !@#$%^&*(), "
       "ký tự full-width ＡＢＣ１２３, xuống dòng, khoảng trắng đầu/cuối",
       "- Ô nhập nhận hết, không chặn loại nào\n"
       "- Sau 保存 + F5, nội dung hiện lại đúng nguyên bản kể cả ký tự xuống dòng và full-width",
       note="Nguồn: r39, r136, r274 (『Các ký tự được nhập → Free text』). TC gốc chỉ có tiêu đề, "
            "đã bổ sung danh sách ký tự cụ thể và bước lưu + F5 để đo được."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "DATA-TEXT-001", "Normal",
       "Nhập emoji và ký tự đặc biệt — lưu đúng và hiển thị đúng trên LINE",
       NEW + "\n- Có 1 tài khoản LINE test chưa từng kết bạn với bot",
       "1. Mở trang 新規友だち用\n"
       "2. Nhập tin nhắn có emoji và ký tự đặc biệt\n"
       "3. Bấm 保存, F5 và đọc lại ô nhập\n"
       "4. Dùng tài khoản LINE test kết bạn với bot\n"
       "5. Đọc tin nhắn nhận được trên app LINE",
       "Tin nhắn: 「ようこそ🎉😊 ★☆ ①②③ ～＆＜＞ 改行\\n2行目」",
       "- Sau F5 ô nhập hiển thị đúng emoji và ký tự đặc biệt, không thành ?? hay ô vuông\n"
       "- Tin nhắn nhận trên app LINE hiển thị ĐÚNG như nội dung đã nhập (RULE-07: khớp giữa màn "
       "admin và output cuối trên LINE)",
       env="PRODUCTION",
       note="TC do AI bổ sung theo DATA-TEXT-001 (text được gửi ra LINE → nâng ưu tiên Cao). "
            "Corpus chỉ test free text chung, không tách emoji. Cần Leader xác nhận.",
       spec="Spec không ghi"),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-002", "Normal",
       "Ô nhập KHÔNG bắt buộc — bỏ trống vẫn lưu được",
       NEW,
       "1. Mở trang 新規友だち用\n"
       "2. Xóa sạch nội dung ô nhập\n"
       "3. Bấm 保存\n"
       "4. F5 và quan sát",
       "Ô nhập rỗng",
       "- Không hiện thông báo lỗi bắt buộc nhập\n"
       "- Lưu thành công\n"
       "- Sau F5 ô nhập vẫn rỗng, bộ đếm hiển thị 0/5,000",
       note="Nguồn: r41, r42, r138, r139, r276, r277."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "UI-INPUT-001", "Normal",
       "Bộ đếm ký tự chạy đúng khi rỗng và khi nhập 1 ký tự",
       NEW,
       "1. Mở trang 新規友だち用, xóa sạch ô nhập → đọc bộ đếm\n"
       "2. Gõ 1 ký tự → đọc bộ đếm\n"
       "3. Xóa ký tự đó → đọc bộ đếm",
       "0 ký tự, rồi 1 ký tự (chữ a)",
       "- Khi rỗng: hiển thị 0/5,000\n"
       "- Khi có 1 ký tự: hiển thị 1/5,000\n"
       "- Xóa đi: quay lại 0/5,000",
       note="Nguồn: r43, r44, r140, r141, r278, r279."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "UI-INPUT-001", "Normal",
       "Bộ đếm ký tự chạy đúng với N ký tự bất kỳ (0 < N < 5.000)",
       NEW,
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Dán vào 100 ký tự → đọc bộ đếm\n"
       "3. Dán thêm cho đủ 2.500 ký tự → đọc bộ đếm\n"
       "4. Dán tiếng Nhật 100 ký tự → đọc bộ đếm",
       "N = 100, 2.500 (Latinh) và 100 ký tự tiếng Nhật",
       "- Bộ đếm hiển thị đúng N/5,000 ở mọi mốc\n"
       "- 1 ký tự tiếng Nhật đếm bằng 1 (không đếm thành 2/3 như byte)",
       note="Nguồn: r45, r142, r280. Vế đếm ký tự tiếng Nhật do AI bổ sung để loại rủi ro đếm theo "
            "byte — cần Leader xác nhận."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-004", "Boundary",
       "Nhập đúng 5.000 ký tự — bộ đếm 5000/5,000, lưu và gửi được",
       NEW + "\n- Có 1 tài khoản LINE test chưa kết bạn với bot",
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Dán chính xác 5.000 ký tự\n"
       "3. Đọc bộ đếm, bấm 保存, F5 và đếm lại độ dài nội dung\n"
       "4. Dùng tài khoản LINE test kết bạn với bot\n"
       "5. Đọc tin nhắn nhận được",
       "Chuỗi đúng 5.000 ký tự (VD 1.000 lần chuỗi 5 ký tự 「あいうえお」)",
       "- Bộ đếm hiển thị 5000/5,000\n"
       "- Lưu thành công, sau F5 nội dung vẫn đủ 5.000 ký tự (không bị cắt)\n"
       "- Tin nhắn nhận trên LINE đủ nội dung, không bị cắt cụt",
       env="PRODUCTION",
       note="Nguồn: r46, r143, r281. RULE-01/RULE-06: đã kéo tới output cuối trên app LINE. "
            "⚠️ Lưu ý LINE Messaging API giới hạn 5.000 ký tự/tin — nếu tin bị cắt ở LINE thì đây là "
            "phát hiện quan trọng, cần raise bug."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-004", "Boundary",
       "Nhập quá 5.000 ký tự — chặn ký tự thứ 5.001, bộ đếm dừng ở 5000/5,000",
       NEW,
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Dán 5.000 ký tự rồi gõ thêm 1 ký tự nữa → quan sát\n"
       "3. Thử dán 1 lần 6.000 ký tự → đọc bộ đếm và đếm độ dài thực tế trong ô",
       "5.000 + 1 ký tự; và 1 lần dán 6.000 ký tự",
       "- Gõ thêm: ký tự thứ 5.001 KHÔNG vào được ô nhập\n"
       "- Bộ đếm vẫn 5000/5,000\n"
       "- Dán 6.000: ô nhập chỉ giữ 5.000 ký tự đầu, bộ đếm 5000/5,000",
       note="Nguồn: r47, r144, r282. Vế『dán 1 lần 6.000』do AI bổ sung (dán khác gõ) — cần Leader "
            "xác nhận."),

    tc("送信するメッセージ — ô nhập & bộ đếm", "SEC-001", "Abnormal",
       "Gọi thẳng API lưu với nội dung > 5.000 ký tự — backend phải chặn, không lưu quá hạn mức",
       NEW + "\n- Có công cụ gửi request (DevTools/Postman) và session Admin hợp lệ",
       "1. Mở trang 新規友だち用, bấm 保存 1 lần và bắt request lưu ở tab Network\n"
       "2. Gửi lại request đó nhưng đổi nội dung tin nhắn thành 10.000 ký tự\n"
       "3. Đọc response\n"
       "4. Mở lại trang 新規友だち用 và đếm độ dài nội dung\n"
       "5. Kết bạn bằng tài khoản LINE test và xem tin nhận được",
       "Nội dung 10.000 ký tự",
       "- Backend trả lỗi hoặc cắt về đúng 5.000 ký tự (KHÔNG lưu nguyên 10.000)\n"
       "- Mở lại trang: nội dung tối đa 5.000 ký tự\n"
       "- Không phát sinh lỗi 500 khiến gửi tin thất bại hàng loạt",
       env="PRODUCTION",
       note="⚠️ MT-07. logic-spec.md:319-325 ghi rõ『validation chủ yếu ở frontend』, không có "
            "FormRequest cho FA-007 → chưa rõ backend có chặn không. Corpus KHÔNG có TC này. "
            "TC do AI bổ sung, dự kiến có thể FAIL → nếu FAIL cần raise bug. CHỜ LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-004", "Boundary",
       "Tin nhắn 4.999 ký tự có biến {name} — khi thay tên thật thì tổng vượt 5.000",
       NEW + "\n- Có tài khoản LINE test có tên hiển thị DÀI (≥20 ký tự) và chưa kết bạn với bot",
       "1. Mở trang 新規友だち用, nhập 4.993 ký tự + chèn「＋ LINE名」(chuỗi {name}, 6 ký tự) "
       "→ tổng đúng 4.999 ký tự\n"
       "2. Đọc bộ đếm, bấm 保存\n"
       "3. Dùng tài khoản LINE test có tên hiển thị dài để kết bạn\n"
       "4. Đọc tin nhắn nhận được, đếm độ dài thực tế",
       "4.993 ký tự cố định + {name}; tên LINE test dài 25 ký tự → tổng sau thay thế = 5.018 ký tự",
       "- Bộ đếm trên màn admin hiển thị 4999/5,000 (đếm chuỗi biến, chưa thay tên)\n"
       "- Lưu thành công\n"
       "- Ghi lại chính xác điều gì xảy ra khi gửi: tin đến đủ, tin bị cắt, hay không gửi được và "
       "hiện ở màn 配信エラー\n"
       "- KHÔNG được im lặng bỏ qua (không gửi mà cũng không báo lỗi)",
       env="PRODUCTION",
       note="TC do AI bổ sung — corpus và spec đều chỉ đếm ký tự TRƯỚC khi thay biến, không ai "
            "kiểm trường hợp thay biến làm vượt giới hạn của LINE. Rủi ro: tin chào mừng của "
            "khách bị cắt hoặc không gửi được. CẦN LEADER CHỐT hành vi mong muốn.",
       spec="Đã hỏi leader"),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-DRAFT-001", "Normal",
       "Nhập tin nhắn rồi chuyển sang tab テスト方法 và quay lại — nội dung nháp không mất",
       NEW,
       "1. Mở trang 新規友だち用, nhập 1 tin nhắn nhưng CHƯA bấm 保存\n"
       "2. Click sang tab「テスト方法」\n"
       "3. Click quay lại tab「メッセージ・アクション設定」\n"
       "4. Quan sát ô nhập",
       "Tin nhắn nháp: 「noi dung chua luu」",
       "- Nội dung nháp còn nguyên trong ô nhập\n"
       "- Bộ đếm khớp với độ dài nội dung nháp",
       note="TC do AI bổ sung theo FUNC-DRAFT-001. Corpus không có. Cần Leader xác nhận.",
       spec="Spec không ghi"),

    tc("送信するメッセージ — ô nhập & bộ đếm", "FUNC-001", "Abnormal",
       "Tự động lưu tin nhắn khi click ra ngoài ô nhập — có thật hay không?",
       NEW,
       "1. Mở trang 新規友だち用, ghi lại nội dung đang lưu\n"
       "2. Sửa nội dung ô nhập thành text mới\n"
       "3. Click ra vùng trống ngoài ô nhập (KHÔNG bấm 保存)\n"
       "4. F5 trang, đọc lại nội dung\n"
       "5. Lặp lại với thao tác chèn「＋ LINE名」và chèn「＋ 友だち情報」",
       "3 thao tác: gõ tin nhắn · chèn LINE名 · chèn 友だち情報 — mỗi lần đều click ra ngoài rồi F5",
       "- Chốt được 1 trong 2 hành vi và ghi lại làm chuẩn:\n"
       "  (a) Nếu CÓ auto-save: sau F5 nội dung mới còn nguyên ở cả 3 thao tác\n"
       "  (b) Nếu KHÔNG auto-save: sau F5 quay về nội dung cũ, và phải có cảnh báo rời trang khi "
       "còn thay đổi chưa lưu",
       note="⚠️ MT-06. Nguồn: r48, r49, r50 (và r145-r147, r283-r285) — TC gốc CHỈ CÓ TIÊU ĐỀ "
            "『check tự động save msg khi click ra ngoài』, cột kết quả mong đợi TRỐNG. Spec "
            "(api-spec.md EP-05) chỉ mô tả lưu bằng nút 保存, không nhắc auto-save. Expected do AI "
            "viết dạng 2 nhánh để đo được. CHỜ LEADER CHỐT hành vi đúng.",
       spec="Đã hỏi leader"),

    # ═══════════ 6. Lưu tin nhắn & bản ghi template ═══════════
    tc("Lưu tin nhắn & bản ghi template", "DATA-DB-001", "Normal",
       "Lưu tin nhắn lần đầu — sinh bản ghi tin nhắn chào mừng riêng cho trang 新規友だち用",
       NEW + "\n- Trang 新規友だち用 đang chưa có tin nhắn nào",
       "1. Mở trang 新規友だち用, nhập tin nhắn\n"
       "2. Bấm 保存\n"
       "3. F5 và đọc lại ô nhập\n"
       "4. Mở trang 既存友だち用 và ブロック解除時用, đọc ô nhập của 2 trang này",
       "Tin nhắn trang 新規: 「xin chao new friend」",
       "- Trang 新規友だち用 hiện đúng tin nhắn vừa lưu\n"
       "- Trang 既存友だち用 và ブロック解除時用 KHÔNG bị ghi đè, giữ nguyên nội dung riêng của chúng\n"
       "- (đối chiếu tầng dữ liệu nếu có quyền) bản ghi tin nhắn chào mừng của 3 loại là 3 bản ghi "
       "riêng biệt",
       note="Nguồn: r59 (message_add_new → template_add_new_id), r156, r293 + feature-spec.md §5 "
            "BR-03/BR-08. Viết theo góc nhìn tester: kiểm bằng 3 màn thay vì query DB."),

    tc("Lưu tin nhắn & bản ghi template", "DATA-001", "Normal",
       "Sửa tin nhắn đã lưu — nội dung mới thay nội dung cũ ở cả màn admin và tin gửi ra LINE",
       NEW + "\n- Trang 新規友だち用 đã lưu sẵn tin nhắn cũ\n"
             "- Có 2 tài khoản LINE test chưa từng kết bạn với bot",
       "1. Dùng tài khoản LINE test 1 kết bạn → ghi lại tin nhận được\n"
       "2. Về admin, sửa tin nhắn trang 新規友だち用 thành nội dung mới, bấm 保存\n"
       "3. F5 và đọc lại ô nhập\n"
       "4. Dùng tài khoản LINE test 2 kết bạn → đọc tin nhận được",
       "Tin cũ: 「msg cu」· Tin mới: 「msg moi 2026」",
       "- Sau 保存 + F5, ô nhập hiển thị đúng nội dung mới\n"
       "- Tài khoản test 2 nhận đúng nội dung MỚI (không nhận nội dung cũ)\n"
       "- Tin nhắn cũ mà tài khoản test 1 đã nhận trước đó không bị sửa ngược trong lịch sử chat",
       env="PRODUCTION",
       note="Nguồn: r60 (『edit, update msg → check ở bảng template, update_timestamp, check hiển "
            "thị msg ở chat 1:1』), r157, r294. RULE-06/RULE-07: kéo tới output cuối trên LINE + "
            "màn chat 1:1."),

    tc("Lưu tin nhắn & bản ghi template", "DATA-REF-001", "Normal",
       "Xóa sạch tin nhắn rồi lưu — cấu hình về trạng thái không có tin nhắn",
       NEW + "\n- Trang 新規友だち用 đã lưu sẵn 1 tin nhắn\n"
             "- Có 1 tài khoản LINE test chưa kết bạn",
       "1. Mở trang 新規友だち用, xóa sạch ô nhập\n"
       "2. Bấm 保存\n"
       "3. F5 và quan sát ô nhập + bộ đếm\n"
       "4. Dùng tài khoản LINE test kết bạn với bot\n"
       "5. Quan sát tin nhắn nhận được",
       "Ô nhập rỗng sau khi đã từng có nội dung",
       "- Sau F5, ô nhập rỗng, bộ đếm 0/5,000\n"
       "- Friend mới kết bạn KHÔNG nhận tin nhắn chào mừng của エルメ nữa\n"
       "- Các action đã cài (nếu có) vẫn chạy bình thường — xóa tin nhắn không xóa action",
       env="PRODUCTION",
       note="Nguồn: r61 (『Check khi xóa msg → xóa luôn template_add_new_id => về null』), r158, "
            "và feature-spec.md §5 BR-04. Vế『action vẫn chạy』do AI bổ sung để chặn rủi ro xóa lây "
            "— cần Leader xác nhận."),

    tc("Lưu tin nhắn & bản ghi template", "DATA-001", "Normal",
       "Cấu hình 3 loại độc lập nhau — sửa 1 trang không ảnh hưởng 2 trang còn lại",
       ALL3,
       "1. Ở 3 trang, lưu 3 tin nhắn KHÁC nhau và 3 bộ action KHÁC nhau\n"
       "2. F5 từng trang và ghi lại nội dung\n"
       "3. Vào trang 既存友だち用, đổi tin nhắn và bấm 保存\n"
       "4. Mở lại trang 新規友だち用 và ブロック解除時用",
       "Tin nhắn: 新規=「A」· 既存=「B」→ đổi thành「B2」· unblock=「C」",
       "- Sau bước 4: trang 新規 vẫn là「A」, trang unblock vẫn là「C」\n"
       "- Chỉ trang 既存 đổi thành「B2」\n"
       "- Danh sách action của 3 trang cũng không lẫn sang nhau",
       note="Nguồn: feature-spec.md §3 (3 cấu hình nằm trong 1 bản ghi, phân biệt bằng cột) + "
            "BR-08. Đối chứng live MCP dev 2026-08-26: 3 type add_new/add_old/unblock trả về 3 "
            "actionId và 3 message khác nhau. Corpus không có TC gộp — do AI bổ sung.",
       spec="Đã hỏi leader"),

    tc("Lưu tin nhắn & bản ghi template", "CONC-003", "Abnormal",
       "Mở 2 tab cùng 1 trang, lưu ở tab A rồi lưu ở tab B — không mất nội dung ngoài ý muốn",
       NEW,
       "1. Mở trang 新規友だち用 ở 2 tab trình duyệt (tab A và tab B) cùng lúc\n"
       "2. Ở tab A: sửa tin nhắn thành「AAA」, bấm 保存\n"
       "3. Ở tab B (chưa F5, vẫn giữ nội dung cũ): bấm 保存\n"
       "4. F5 cả 2 tab và đọc nội dung",
       "Tab A lưu「AAA」, tab B đang giữ nội dung cũ「cu」",
       "- Chốt và ghi lại hành vi thật: hoặc tab B ghi đè về「cu」, hoặc hệ thống cảnh báo dữ liệu "
       "đã bị thay đổi ở nơi khác\n"
       "- KHÔNG được xảy ra tình trạng mất cả 2 nội dung, hoặc lưu ra nội dung thứ 3 không ai nhập",
       note="TC do AI bổ sung theo CONC-003 (2 tab cùng gọi API lưu). Corpus không có. "
            "Cần Leader xác nhận hành vi mong muốn.",
       spec="Spec không ghi"),
]
