# -*- coding: utf-8 -*-
"""FA-039 LINE公式アカウント入れ替え機能 — Nhóm 3-4.

S3 Chọn phương thức đổi LOA (màn「01 入れ替え方法選択」)
S4 Nhập thông tin kết nối (màn「02 接続情報入力」— 4 field Messaging API + LINE Login)

⚠️ MT-13 — 3 biến thể UI. Nhãn nút trong file này lấy theo bản MỚI NHẤT ([AI] v2 /
#37744). Bản #34632 dùng nhãn「次へ進む」/「前のステップに戻る」và tách Messaging API +
LINE Login thành nhiều bước; nếu Leader chốt bản cũ đang chạy production thì phải
đổi nhãn nút ở cột Các bước thực hiện + Kết quả mong đợi.
"""
from _common import tc

PAID = ("- Đăng nhập Admin chủ (主管理者) của bot plan Standard trở lên (bots.plan_type = 1)\n"
        "- Bot đã kết nối, KHÔNG có đặt lịch đổi LOA nào đang active")
SEL = PAID + "\n- Đang ở màn chọn phương thức đổi LOA (「01 入れ替え方法選択」)"
INP = PAID + "\n- Đang ở màn nhập thông tin kết nối (「02 接続情報入力」) với 4 field trống"
LOA_OK = ("- Đã chuẩn bị 1 LOA mới trên LINE Developers: 1 Messaging API channel + 1 LINE Login channel\n"
          "  **CÙNG provider**, lấy sẵn Channel ID + Channel secret của cả 2\n"
          "- LOA mới CHƯA từng kết nối L Message")
MT13 = "⚠️ MT-13 — nhãn nút theo bản UI mới nhất. "

S3 = [
    # ═══════════════ 3. Chọn phương thức đổi LOA ═══════════════
    tc("Chọn phương thức đổi LOA", "FUNC-001", "Normal",
       "Bot trả phí, không campaign — cả 2 option mở, CTA disabled cho đến khi chọn 1 option",
       SEL,
       "1. Vào màn chọn phương thức đổi LOA bằng bot Standard (không campaign)\n"
       "2. Quan sát trạng thái 2 option và nút CTA ngay khi trang load (chưa bấm gì)\n"
       "3. Thử bấm nút CTA\n"
       "4. Quan sát có điều hướng hay không",
       "Bot Standard, không campaign",
       "- Cả 2 option đều ở trạng thái mở: không overlay xám, không icon khoá\n"
       "- Chưa option nào được highlight border\n"
       "- Nút CTA ở trạng thái DISABLED (màu nhạt, con trỏ không phải tay)\n"
       "- Bấm CTA: không có phản ứng, không điều hướng, không gọi request",
       note="Nguồn: TC-CBF-017 (BR-08 Section 4 State 2; Pass dev + staging). "
            "Evidence: ảnh màn lúc load + ảnh Network trống khi bấm CTA."),

    tc("Chọn phương thức đổi LOA", "FUNC-001", "Normal",
       "Bot Free trong campaign — option đặt lịch bị khoá bằng overlay xám + icon khoá",
       ("- Đăng nhập Admin chủ bot Free (plan_type = 2) add chưa quá 1 tháng\n"
        "- Campaign「1ヶ月無料開放」đang active\n"
        "- Đang ở màn chọn phương thức đổi LOA"),
       "1. Vào màn chọn phương thức bằng bot Free trong campaign\n"
       "2. Quan sát option 1「すぐにLINE公式アカウントを入れ替える」\n"
       "3. Quan sát option 2「LINE公式アカウント入れ替え予約をする」\n"
       "4. Bấm thử vào option 2",
       "Bot Free trong campaign",
       "- Option 1 mở, chọn được\n"
       "- Option 2 có overlay màu xám phủ lên + icon khoá hiển thị rõ\n"
       "- Bấm option 2: KHÔNG được chọn, border không highlight, CTA không đổi text\n"
       "- Có banner campaign hiển thị phía trên",
       note="⚠️ MT-03 (campaign còn dùng?) + MT-04. Nguồn: TC-CBF-016 (BR-08 Section 4 State 1; "
            "Pass dev + staging) + Change bot r92. Evidence: ảnh 2 option cạnh nhau."),

    tc("Chọn phương thức đổi LOA", "PAY-LIMIT-001", "Abnormal",
       "Bot Free cố chọn option đặt lịch trong kỳ campaign — giới hạn theo gói KHÔNG được tạm mở",
       ("- Đăng nhập Admin chủ bot Free add chưa quá 1 tháng\n"
        "- Campaign đang active\n"
        "- Đang ở màn chọn phương thức"),
       "1. Bấm vào option 2「LINE公式アカウント入れ替え予約をする」\n"
       "2. Mở DevTools, thử bỏ thuộc tính disabled của option 2 bằng tay rồi bấm chọn\n"
       "3. Bấm CTA và quan sát request + response\n"
       "4. Kiểm tra DB bảng schedule_change_bots",
       "Bot Free trong campaign; bypass disabled bằng DevTools",
       "- Không chọn được option 2 qua UI\n"
       "- Khi bypass bằng DevTools và gửi request: server REJECT (không tạo đặt lịch)\n"
       "- DB: KHÔNG có bản ghi mới trong schedule_change_bots\n"
       "- Giới hạn theo gói không bị tạm mở trong kỳ campaign",
       note="Nguồn: TC-CBF-020 (PAY-LIMIT-001, BR-08; QA-spec-030 CONFIRMED 'restriction không được tạm mở "
            "kể cả trong campaign'; Pass dev + staging). RULE-07 — verify DB. "
            "Evidence: ảnh DevTools + Network response + query schedule_change_bots."),

    tc("Chọn phương thức đổi LOA", "UI-FIELD-001", "Normal",
       "Chọn option đổi ngay → border highlight + CTA đổi text thành「入れ替え設定に進む」và enable",
       SEL,
       "1. Ở màn chọn phương thức, ghi lại text nút CTA ban đầu\n"
       "2. Bấm chọn option 1「すぐにLINE公式アカウントを入れ替える」\n"
       "3. Quan sát border của option 1 và text + trạng thái nút CTA\n"
       "4. Bấm CTA và quan sát màn tiếp theo",
       "Bot Standard",
       "- Option 1 có border highlight rõ (khác màu/độ dày so với option 2)\n"
       "- Nút CTA đổi text thành「入れ替え設定に進む」\n"
       "- Nút CTA chuyển sang ENABLED (đổi màu, con trỏ hình tay)\n"
       "- Bấm CTA → sang màn nhập thông tin kết nối",
       note="Nguồn: TC-CBF-018 (UI-FIELD-001, BR-09 Section 4 State 3; Pass dev + staging) + "
            "Change bot r102/r251 ('mở ra màn change bot nhập LINE Official Account'). " + MT13
            + "Evidence: ảnh trước/sau khi chọn option."),

    tc("Chọn phương thức đổi LOA", "UI-FIELD-001", "Normal",
       "Chọn option đặt lịch → border highlight + CTA đổi text thành「入れ替え予約設定に進む」và enable",
       SEL,
       "1. Ở màn chọn phương thức, bấm chọn option 2「LINE公式アカウント入れ替え予約をする」\n"
       "2. Quan sát border option 2 và text + trạng thái nút CTA\n"
       "3. Bấm CTA và quan sát màn tiếp theo",
       "Bot Standard",
       "- Option 2 có border highlight rõ\n"
       "- Nút CTA đổi text thành「入れ替え予約設定に進む」và ENABLED\n"
       "- Bấm CTA → sang màn nhập thông tin kết nối (cùng màn với luồng đổi ngay)",
       note="Nguồn: TC-CBF-019 (UI-FIELD-001, BR-10 Section 4 State 4; Pass dev + staging) + "
            "Change bot r103/r252. " + MT13 + "Evidence: ảnh trước/sau khi chọn option."),

    tc("Chọn phương thức đổi LOA", "UI-FIELD-001", "Boundary",
       "Đổi qua lại 2 option nhiều lần → text CTA luôn khớp lựa chọn CUỐI CÙNG",
       SEL,
       "1. Bấm option 1 → ghi text CTA\n"
       "2. Bấm option 2 → ghi text CTA\n"
       "3. Lặp lại bước 1-2 thêm 3 vòng\n"
       "4. Kết thúc ở option 1, ghi text CTA cuối cùng",
       "4 vòng đổi qua lại; lựa chọn cuối = option 1",
       "- Mỗi lần đổi, text CTA đổi đúng theo option vừa chọn\n"
       "- Text CTA cuối cùng là「入れ替え設定に進む」(khớp option 1)\n"
       "- CHỈ 1 option được highlight tại mọi thời điểm, không bao giờ có 2 option cùng highlight",
       note="Nguồn: TC-CBF-022 (UI-FIELD-001, BR-09/BR-10; Pass dev + staging). "
            "Evidence: ảnh sau mỗi lần đổi (4 ảnh)."),

    tc("Chọn phương thức đổi LOA", "CONC-003", "Boundary",
       "Bấm nhanh liên tiếp đổi option → trạng thái cuối đúng, không có 2 option cùng highlight",
       SEL,
       "1. Bấm liên tiếp option 1 → option 2 → option 1 → option 2 trong vòng 1 giây\n"
       "2. Dừng lại, quan sát ngay trạng thái 2 option\n"
       "3. Quan sát text CTA\n"
       "4. Kiểm tra Console có lỗi JS không",
       "4 lần bấm trong 1 giây; lần cuối = option 2",
       "- Chỉ option 2 được highlight, option 1 mất highlight hoàn toàn\n"
       "- Text CTA =「入れ替え予約設定に進む」\n"
       "- Không có trạng thái nửa vời (cả 2 highlight hoặc không option nào highlight)\n"
       "- Console không lỗi JS",
       note="Nguồn: TC-CBF-025 (CONC-003 — race tầng client; Pass dev + staging). "
            "Evidence: ảnh trạng thái cuối + ảnh Console."),

    tc("Chọn phương thức đổi LOA", "FUNC-SEQ-001", "Boundary",
       "Chọn option rồi F5 reload → lựa chọn KHÔNG được giữ, reset về trạng thái chưa chọn",
       SEL,
       "1. Bấm chọn option 2, xác nhận CTA đã enable\n"
       "2. Bấm F5 reload trang\n"
       "3. Quan sát trạng thái 2 option và nút CTA sau khi load xong",
       "Bot Standard; chọn option 2 rồi F5",
       "- Sau reload: KHÔNG option nào được highlight\n"
       "- Nút CTA trở lại DISABLED\n"
       "- Text CTA trở lại text mặc định ban đầu\n"
       "- Không có thông báo 'dữ liệu chưa lưu'",
       note="Nguồn: TC-CBF-028 (FUNC-SEQ-001; Pass dev + staging). Evidence: ảnh trước/sau F5."),

    tc("Chọn phương thức đổi LOA", "FUNC-001", "Boundary",
       "Đóng banner campaign bằng × → hành vi khi reload trang",
       ("- Đăng nhập Admin chủ bot Free trong campaign\n"
        "- Đang ở màn chọn phương thức, banner campaign đang hiển thị"),
       "1. Bấm nút × trên banner campaign\n"
       "2. Quan sát banner và layout màn hình\n"
       "3. Bấm F5 reload trang\n"
       "4. Quan sát banner có hiện lại không",
       "Bot Free trong campaign",
       "- Bấm × : banner biến mất, layout màn hình không bị vỡ (các option không bị đè)\n"
       "- Sau reload: ghi nhận hành vi thực tế (hiện lại / không hiện lại)\n"
       "- Trạng thái 2 option KHÔNG đổi sau khi đóng banner",
       note="⚠️ MT-03 + BR-11 CHƯA XÁC ĐỊNH hành vi sau reload (TC-CBF-024 Blocked cả 2 env, "
            "liên quan QA-spec-009). TC này dùng để GHI NHẬN hành vi thật, không assert cứng — "
            "cần Leader chốt rồi cập nhật Kết quả mong đợi. Evidence: ảnh trước/sau × + sau reload.",
       spec="Đã hỏi leader"),

    tc("Chọn phương thức đổi LOA", "PERM-002", "Abnormal",
       "Staff truy cập thẳng URL màn chọn phương thức (bypass menu) → không có quyền",
       ("- Có tài khoản Staff thuộc cùng bot Standard\n"
        "- Biết URL màn chọn phương thức đổi LOA"),
       "1. Đăng nhập bằng tài khoản Staff\n"
       "2. Xác nhận sidebar KHÔNG có mục「LINE公式アカウント入れ替え」\n"
       "3. Dán URL màn chọn phương thức, Enter\n"
       "4. Quan sát response (403 / redirect) và nội dung trang",
       "Tài khoản Staff của bot Standard",
       "- Sidebar Staff không có mục đổi LOA\n"
       "- Truy cập URL trực tiếp: bị chặn theo đúng kết luận MT-02 (403 hoặc redirect /basic/overview)\n"
       "- KHÔNG render màn chọn phương thức\n"
       "- Response không chứa Channel ID / thông tin bot",
       note="⚠️ MT-02 — quyền Staff đang mâu thuẫn 3 nguồn (AddBot r342-344 'Account staff vẫn thao tác "
            "change bot bt' · Change bot r227-229 'được access bình thường' · TC-CBF-026/092 '403'). "
            "⏳ Loại response cụ thể: QA-spec-032 chưa chốt. Nguồn: TC-CBF-026 (Pass dev + staging). "
            "Evidence: ảnh sidebar Staff + Network response.",
       spec="Đã hỏi leader"),

    tc("Chọn phương thức đổi LOA", "PERM-001", "Normal",
       "Ma trận quyền — Admin chủ bot Free vs bot Standard+ thấy menu và trạng thái option đúng",
       ("- Có 2 tài khoản Admin chủ: 1 bot Free (trong campaign), 1 bot Standard\n"
        "- Biết trước kết luận mong đợi của từng gói"),
       "1. Đăng nhập Admin chủ bot Free → kiểm tra sidebar có mục đổi LOA ở nhóm nào\n"
       "2. Vào màn chọn phương thức, ghi trạng thái 2 option\n"
       "3. Đăng xuất, đăng nhập Admin chủ bot Standard\n"
       "4. Lặp bước 1-2 và đối chiếu",
       "Bot Free (campaign) vs bot Standard",
       "- Bot Free: mục menu nằm ở nhóm「有料プラン限定」; option 1 mở, option 2 khoá\n"
       "- Bot Standard: mục menu ở nhóm thường; cả 2 option mở\n"
       "- Không bot nào thấy thêm/thiếu option so với gói của mình",
       note="Nguồn: TC-CBF-097 (PERM-001 + MAP-PERM-01, TD Section 5 Access Control; Pass dev + staging) "
            "+ Change bot r84 (menu「有料プラン限定」). ⚠️ MT-04. Evidence: ảnh sidebar + ảnh option của 2 gói."),
]

S4 = [
    # ═══════════════ 4. Nhập thông tin kết nối ═══════════════
    tc("Nhập thông tin kết nối", "FUNC-002", "Normal",
       "Màn nhập thông tin kết nối lúc mới vào — 4 field trống, hiển thị đúng placeholder",
       INP,
       "1. Từ màn chọn phương thức, chọn option 1 rồi bấm CTA\n"
       "2. Quan sát 4 field: Messaging API Channel ID / Channel secret, LINE Login Channel ID / Channel secret\n"
       "3. Đọc placeholder của từng field\n"
       "4. Quan sát nút CTA「接続情報の確認に進む」",
       "Bot Standard, chưa nhập gì",
       "- 4 field đều trống, không có giá trị mặc định\n"
       "- Field Channel ID có placeholder dạng ví dụ số (VD「例: 1234567890」)\n"
       "- Field Channel secret có placeholder dạng「チャネルシークレットを入力」\n"
       "- Cả 4 field đều được đánh dấu là trường bắt buộc\n"
       "- Nút CTA ở trạng thái DISABLED",
       note="Nguồn: Change bot r122-r123 (step 3 bản #34632) + r257-r258 (màn 1 bản #37744) + "
            "TC-CBF-029 (Pass dev + staging). " + MT13 + "Evidence: ảnh full màn + zoom placeholder."),

    tc("Nhập thông tin kết nối", "FUNC-002", "Abnormal",
       "CTA vẫn disabled khi cả 4 field còn rỗng",
       INP,
       "1. Không nhập gì vào 4 field\n"
       "2. Bấm nút CTA「接続情報の確認に進む」\n"
       "3. Mở DevTools Network, kiểm tra có request nào được gửi không",
       "4 field rỗng",
       "- Nút CTA disabled, bấm không có phản ứng\n"
       "- Network: KHÔNG có request validate nào được gửi\n"
       "- Không chuyển màn",
       note="Nguồn: TC-CBF-029 (FUNC-002 + DI-01, QA-spec-009 CONFIRMED; Pass dev + staging) + "
            "Change bot r125/r132/r261/r268 ('không nhập → disable nút next'). "
            "Evidence: ảnh nút disabled + Network trống."),

    tc("Nhập thông tin kết nối", "FUNC-002", "Boundary",
       "CTA chỉ enable khi ĐỦ 4/4 field có data — test từng nấc 1/4, 2/4, 3/4, 4/4",
       INP,
       "1. Nhập Messaging API Channel ID → quan sát CTA (1/4)\n"
       "2. Nhập thêm Messaging API Channel secret → quan sát CTA (2/4)\n"
       "3. Nhập thêm LINE Login Channel ID → quan sát CTA (3/4)\n"
       "4. Nhập thêm LINE Login Channel secret → quan sát CTA (4/4)\n"
       "5. Xóa 1 field bất kỳ → quan sát CTA trở lại trạng thái nào",
       "Lần lượt 1/4 → 2/4 → 3/4 → 4/4 rồi xóa 1 field về 3/4",
       "- 1/4, 2/4, 3/4: CTA vẫn DISABLED\n"
       "- Đúng 4/4: CTA chuyển ENABLED, đổi màu\n"
       "- Xóa 1 field về 3/4: CTA trở lại DISABLED ngay (không cần blur/submit)",
       note="Nguồn: TC-CBF-030 (FUNC-002, DI-01 pattern min-1/min; Pass dev + staging) + "
            "Change bot r124/r260. ⚠️ MT-13: bản cũ (Bill tiền r8-r9, 11/2023) KHÔNG disable nút mà "
            "hiển thị/ẩn text「※未記入の項目があります」— xem MT-06b. Evidence: 5 ảnh theo từng nấc."),

    tc("Nhập thông tin kết nối", "UI-INPUT-001", "Normal",
       "Paste bằng chuột phải (Win + Mac) kích hoạt validate/enable giống Ctrl+V",
       INP + "\n- Có sẵn 4 giá trị hợp lệ trong clipboard\n"
       "- Có máy Windows (Chrome) và máy Mac (Safari)",
       "1. Trên Win Chrome: paste 4 giá trị bằng Ctrl+V → quan sát CTA\n"
       "2. Xóa hết, paste lại 4 giá trị bằng chuột phải → Paste → quan sát CTA\n"
       "3. Lặp lại bước 1-2 trên Mac Safari (Cmd+V và chuột phải)\n"
       "4. Đối chiếu 4 kết quả",
       "4 giá trị Channel ID/secret hợp lệ; Win Chrome + Mac Safari",
       "- Cả 4 trường hợp: CTA đều chuyển ENABLED\n"
       "- Paste bằng chuột phải cho kết quả GIỐNG paste bằng bàn phím\n"
       "- Không trường hợp nào CTA vẫn disabled dù 4 field đã có data",
       note="Nguồn: TC-CBF-031 (UI-INPUT-001 + DI-01; Blocked cả 2 env). "
            "Lỗi thường gặp: JS chỉ nghe keyboard event → paste chuột không trigger. "
            "UI-INPUT-001 là quan điểm BẮT BUỘC với mọi màn có ô nhập text. Evidence: 4 ảnh CTA."),

    tc("Nhập thông tin kết nối", "UI-INPUT-001", "Normal",
       "Giá trị có khoảng trắng đầu/cuối → tự động trim trước khi validate",
       INP + "\n" + LOA_OK,
       "1. Nhập Messaging API Channel ID có thêm 2 space ở đầu và 3 space ở cuối\n"
       "2. Nhập Channel secret tương tự (có space đầu/cuối)\n"
       "3. Nhập 2 field LINE Login cũng có space đầu/cuối\n"
       "4. Bấm CTA\n"
       "5. Kiểm tra giá trị thực tế được gửi trong Network request payload",
       "'  1234567890   ' (2 space đầu, 3 space cuối) cho từng field",
       "- Validate THÀNH CÔNG, không báo lỗi sai thông tin\n"
       "- Network payload chứa giá trị ĐÃ trim (không còn space đầu/cuối)\n"
       "- Sang được màn xác nhận thông tin kết nối",
       note="Nguồn: TC-CBF-032 (UI-INPUT-001 + DI-01, TD EP-04 'channel_secret trim whitespace'; "
            "Pass dev + staging) + Change bot r126/r133 (bản #34632 để TRỐNG expected) + "
            "r262/r269 (bản #37744 ghi rõ 'Expect: tự động trim space đầu cuối'). Evidence: Network payload."),

    tc("Nhập thông tin kết nối", "FUNC-004", "Boundary",
       "Paste chuỗi rất dài vào field → không vỡ layout, xử lý theo giới hạn cột DB",
       INP,
       "1. Paste chuỗi 500 ký tự vào field Messaging API Channel ID\n"
       "2. Quan sát layout màn hình và field\n"
       "3. Paste chuỗi 500 ký tự vào field Channel secret\n"
       "4. Bấm CTA, quan sát thông báo lỗi\n"
       "5. Kiểm tra giá trị gửi lên trong Network payload",
       "Chuỗi 500 ký tự (vượt giới hạn cột DB 128 ký tự của messaging_channel_id)",
       "- Layout KHÔNG vỡ: field không tràn ra ngoài khung, các nút không bị đẩy lệch\n"
       "- Hoặc field cắt ở giới hạn, hoặc server báo lỗi rõ ràng — KHÔNG lưu tràn cột DB\n"
       "- KHÔNG có lỗi 500 từ server",
       note="Nguồn: TC-CBF-033 (FUNC-004 + DI-01; Pass dev + staging). "
            "⚠️ Spec KHÔNG công bố max-length cho 4 field này (QA-spec-010/011); test theo boundary cột DB "
            "(TD: messaging_channel_id varchar(128)). Đây là suy luận từ cột DB, cần Leader xác nhận "
            "max-length chính thức. Evidence: ảnh layout + Network payload.",
       spec="Đã hỏi leader"),

    tc("Nhập thông tin kết nối", "DATA-TEXT-001", "Boundary",
       "Nhập ký tự full-width/half-width tiếng Nhật + ký tự đặc biệt → hiển thị đúng, không vỡ font",
       INP,
       "1. Nhập「１２３４５６７８９０」(số full-width) vào field Channel ID\n"
       "2. Nhập「テスト＠＃＄％」vào field Channel secret\n"
       "3. Nhập emoji 😀 và ký tự <script>alert(1)</script> vào field còn lại\n"
       "4. Quan sát hiển thị trong field và thông báo lỗi khi bấm CTA",
       "Số full-width 「１２３４５６７８９０」· 「テスト＠＃＄％」· emoji · thẻ script",
       "- Tất cả ký tự hiển thị ĐÚNG trong field, không thành dấu ? hay ô vuông\n"
       "- Không vỡ font, không vỡ layout\n"
       "- Bấm CTA: báo lỗi sai thông tin (không pass validate)\n"
       "- Thẻ script KHÔNG được thực thi (không có alert popup)",
       note="Nguồn: TC-CBF-034 (DATA-TEXT-001 + DI-01; Pass dev + staging). "
            "Case script là bổ sung của AI theo SEC — cần Leader xác nhận có đưa vào bộ chính thức. "
            "Evidence: ảnh 4 field + ảnh thông báo lỗi."),

    tc("Nhập thông tin kết nối", "FUNC-001", "Normal",
       "Toggle hiển thị/ẩn Channel secret hoạt động đúng cho CẢ 2 field secret",
       INP,
       "1. Nhập giá trị vào field Messaging API Channel secret\n"
       "2. Quan sát mặc định: ký tự bị che hay hiện rõ\n"
       "3. Bấm icon toggle con mắt của field đó → quan sát\n"
       "4. Bấm lại lần nữa → quan sát\n"
       "5. Lặp bước 1-4 cho field LINE Login Channel secret",
       "Giá trị secret 32 ký tự",
       "- Mặc định cả 2 field secret đều CHE ký tự (dạng ●●●)\n"
       "- Bấm toggle: hiện rõ toàn bộ giá trị đã nhập\n"
       "- Bấm lại: che lại\n"
       "- 2 field hoạt động ĐỘC LẬP (toggle field này không ảnh hưởng field kia)",
       note="Nguồn: TC-CBF-042 (FUNC-001 + UIC-04, BR-14; Pass dev + staging). "
            "Evidence: 4 ảnh trạng thái che/hiện của 2 field."),

    tc("Nhập thông tin kết nối", "SEC-002", "Abnormal",
       "Thông báo lỗi và Console/Network KHÔNG lộ giá trị thật của Channel secret",
       INP,
       "1. Mở DevTools (Console + Network)\n"
       "2. Nhập 4 field với Channel secret sai nhưng dễ nhận diện (VD 'SECRET_TEST_12345')\n"
       "3. Bấm CTA để server trả lỗi\n"
       "4. Đọc nội dung thông báo lỗi trên màn hình\n"
       "5. Tìm chuỗi 'SECRET_TEST_12345' trong Console log và trong response body",
       "Channel secret = 'SECRET_TEST_12345' (sai)",
       "- Thông báo lỗi trên màn hình KHÔNG chứa giá trị secret\n"
       "- Console log KHÔNG in ra secret dạng plaintext\n"
       "- Response body KHÔNG echo lại secret\n"
       "- (Request payload có secret là bình thường — chỉ kiểm log/response)",
       note="Nguồn: TC-CBF-041 + TC-CBF-096 (SEC-002; Blocked cả 2 env). SEC-002 BẮT BUỘC khi chức năng "
            "xử lý credential/token. Evidence: ảnh Console + ảnh response body (Ctrl+F chuỗi secret)."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Abnormal",
       "Messaging API Channel ID/secret SAI → LINE API reject → báo lỗi, ở lại màn nhập",
       INP,
       "1. Nhập Messaging API Channel ID + secret SAI (không tồn tại trên LINE)\n"
       "2. Nhập LINE Login Channel ID + secret hợp lệ\n"
       "3. Bấm CTA\n"
       "4. Quan sát thông báo lỗi và màn hình hiện tại\n"
       "5. Kiểm tra DB bảng bots",
       "Messaging API Channel ID = 9999999999, secret = 'abc123sai'",
       "- Hiển thị thông báo lỗi:「入力した情報に誤りがありますので、入力情報を再度ご確認ください。"
       "ご不明な場合は、サポート窓口までお問い合わせください。」\n"
       "- Bấm vào chữ「サポート窓口」→ mở TAB MỚI tới trang hỗ trợ LINE\n"
       "- VẪN ở màn nhập thông tin kết nối, 4 field giữ nguyên giá trị đã nhập\n"
       "- DB: KHÔNG tạo bản ghi bots mới",
       note="Nguồn: Change bot r129/r135/r265/r271 (04-07/2026, text lỗi + link サポート窓口 "
            "https://page.line.me/770yphxr?openQrModal=true) + TC-CBF-036 (BR-13, QA-spec-012 CONFIRMED; "
            "Pass dev). ⚠️ MT-06 — text lỗi cũ (Bill tiền r11/r17, 11/2023) khác hoàn toàn. "
            "RULE-05 — đối chiếu tài liệu LINE mới nhất. Evidence: ảnh thông báo lỗi + query bots."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Abnormal",
       "LINE Login Channel ID/secret SAI hoặc không cùng provider → báo lỗi",
       INP,
       "1. Nhập Messaging API Channel ID + secret HỢP LỆ\n"
       "2. Nhập LINE Login Channel ID + secret của provider KHÁC\n"
       "3. Bấm CTA\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Kiểm tra DB bảng bots + kiểm tra bên LINE Developers có LIFF app mới nào được tạo không",
       "LINE Login channel thuộc provider khác với Messaging API channel",
       "- Hiển thị thông báo lỗi「入力した情報に誤りがありますので、入力情報を再度ご確認ください。…」\n"
       "- DB: KHÔNG tạo bản ghi bots mới\n"
       "- Bên LINE: KHÔNG có LIFF app nào được tạo thêm",
       note="Nguồn: Change bot r129/r135/r265/r271 + TC-CBF-037 (BR-13; Pass dev). "
            "⚠️ MT-05b — Change bot r134/r270 nói nhánh 'LINE Login nhập của dạng Messaging API' KHÔNG báo lỗi "
            "ngay mà tạo LIFF app luôn, chỉ báo lỗi ở bước webhook (「ステップ3の入力内容に誤りがあります」). "
            "Evidence: ảnh lỗi + query bots + ảnh LINE Developers LIFF list."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Abnormal",
       "Nhập LINE Login channel KHÔNG phải loại LINE Login → lỗi xuất hiện MUỘN ở bước sau, quay về đúng bước",
       INP,
       "1. Nhập Messaging API Channel ID + secret hợp lệ\n"
       "2. Ở 2 field LINE Login, nhập Channel ID + secret của 1 channel dạng Messaging API\n"
       "3. Bấm CTA và quan sát: có báo lỗi ngay không\n"
       "4. Đi tiếp đến bước webhook, tick checkbox rồi bấm nút sang bước tiếp\n"
       "5. Quan sát thông báo lỗi và màn hình sau khi bấm OK",
       "LINE Login field nhập bằng Channel ID/secret của Messaging API channel",
       "- Bước nhập thông tin: KHÔNG báo lỗi ngay (vì hệ thống tạo LIFF app luôn)\n"
       "- Đến bước webhook, bấm sang bước tiếp: báo lỗi「ステップ3の入力内容に誤りがあります。再確認してください。」\n"
       "- Bấm OK → quay về đúng bước nhập thông tin kết nối\n"
       "- 4 field giữ nguyên giá trị để user sửa",
       note="Nguồn: Change bot r134 (bản #34632) + r270 (bản #37744), cả 2 TR=OK. "
            "⚠️ Đây là hành vi 'lỗi muộn' — UI-003 rủi ro false-success ở bước nhập. "
            "Evidence: ảnh bước nhập (không lỗi) + ảnh thông báo lỗi ở bước webhook."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Abnormal",
       "LINE Login channel đã HẾT slot LIFF app → báo lỗi ở bước tạo QR",
       INP + "\n- Có LINE Login channel đã dùng hết toàn bộ slot LIFF app",
       "1. Nhập Messaging API hợp lệ + LINE Login channel đã hết slot LIFF\n"
       "2. Bấm CTA, quan sát có lỗi ngay không\n"
       "3. Đi tiếp tới bước webhook, bấm nút tạo QR code\n"
       "4. Quan sát thông báo lỗi và màn hình sau khi bấm OK",
       "LINE Login channel: 0 slot LIFF trống",
       "- Bước nhập: KHÔNG báo lỗi ngay\n"
       "- Bấm tạo QR code: báo lỗi「ステップ3の入力内容に誤りがあります。再確認してください。」\n"
       "- Bấm OK → quay về bước nhập thông tin kết nối",
       note="Nguồn: Change bot r136 (TR=OK) + r272. Evidence: ảnh thông báo lỗi + ảnh LIFF list bên LINE."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Boundary",
       "LINE Login channel còn ĐÚNG 1 slot LIFF trống (cần 2 slot) → báo lỗi riêng",
       INP + "\n- Có LINE Login channel còn đúng 1 slot LIFF app trống",
       "1. Nhập Messaging API hợp lệ + LINE Login channel còn đúng 1 slot LIFF\n"
       "2. Bấm CTA đi tiếp\n"
       "3. Thực hiện tới bước tạo LIFF app\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Kiểm tra bên LINE: có bao nhiêu LIFF app được tạo thành công",
       "LINE Login channel: đúng 1 slot LIFF trống; hệ thống cần tạo 2 LIFF app",
       "- Hiển thị message「LINEログイン設定情報に誤りがあります。再確認してください。」\n"
       "- Bên LINE: không để lại LIFF app tạo dở (tạo 1 rồi fail 1) — nếu có thì phải ghi nhận là bug rác dữ liệu\n"
       "- Không tạo bản ghi bots mới trong DB",
       note="Nguồn: Change bot r137 (bản #34632, CỘT Test Result TRỐNG — chưa ai chạy) + r273. "
            "⚠️ RISK: đây là case biên quan trọng (cần 2 LIFF: エルメ流入アクション用 + エルメ各種フォーム用) "
            "nhưng chưa có kết quả chạy ở bất kỳ nguồn nào. Evidence: ảnh message + ảnh LIFF list bên LINE."),

    tc("Nhập thông tin kết nối", "PERM-003", "Abnormal",
       "Channel ID đã kết nối với bot ĐANG HOẠT ĐỘNG trong L Message (is_delete=0) → chặn, báo lỗi đã kết nối",
       INP + "\n- Biết Channel ID của 1 bot khác đang hoạt động trong L Message (bots.is_delete = 0)",
       "1. Nhập Messaging API Channel ID = Channel ID của bot đang hoạt động khác\n"
       "2. Nhập 3 field còn lại\n"
       "3. Bấm CTA\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Bấm vào chữ「サポート窓口」trong thông báo",
       "Channel ID của bot khác có bots.is_delete = 0",
       "- Báo lỗi「このLINE公式アカウントは、すでにL Messageに接続されています。"
       "ご不明な場合は、サポート窓口までお問い合わせください」\n"
       "- Bấm「サポート窓口」→ mở TAB MỚI tới https://step.lme.jp/check-user\n"
       "- KHÔNG cho đi tiếp bước sau\n"
       "- DB: không tạo bản ghi bots mới",
       note="Nguồn: Change bot r127 (TR=OK) + r263 + TC-CBF-039/100 (PERM-003, TD EP-04 Server Validation; "
            "Blocked cả 2 env). PERM-003 trigger: 'BẮT BUỘC khi có chức năng change bot'. "
            "Evidence: ảnh thông báo lỗi + URL tab mới + query bots."),

    tc("Nhập thông tin kết nối", "COMPAT-LEGACY-001", "Boundary",
       "Channel ID trùng với bot ĐÃ XÓA trong L Message (is_delete=1) → CHO PHÉP nhập, check tiếp điều kiện khác",
       INP + "\n- Biết Channel ID của 1 bot đã bị xóa trong L Message (bots.is_delete = 1)",
       "1. Nhập Messaging API Channel ID = Channel ID của bot đã xóa (is_delete = 1)\n"
       "2. Nhập 3 field còn lại hợp lệ, cùng provider\n"
       "3. Bấm CTA\n"
       "4. Quan sát có báo lỗi 'đã kết nối' không\n"
       "5. Đi tiếp các bước và xác nhận flow chạy bình thường",
       "Channel ID của bot có bots.is_delete = 1",
       "- KHÔNG báo lỗi「すでにL Messageに接続されています」\n"
       "- Cho phép đi tiếp, hệ thống check các điều kiện khác (provider, loại channel)\n"
       "- Nếu các điều kiện khác hợp lệ thì hoàn tất đổi LOA được",
       note="Nguồn: Change bot r128 (bản #34632, TR=**Not test**) + r264 (bản #37744, cột kết quả TRỐNG). "
            "⚠️ RISK: case này CHƯA ĐƯỢC CHẠY ở bất kỳ nguồn nào — đây là nhánh legacy quan trọng "
            "(RULE-09 cũ & mới song song). Evidence: ảnh màn + query bots trước/sau."),

    tc("Nhập thông tin kết nối", "FUNC-UNIQ-001", "Boundary",
       "Channel ID trùng với CHÍNH channel hiện tại của bot đang đổi → hệ thống chặn (không cho 'đổi về chính nó')",
       INP,
       "1. Lấy Channel ID + secret HIỆN TẠI của chính bot đang đăng nhập (query bảng bots)\n"
       "2. Nhập đúng 4 giá trị đó vào 4 field\n"
       "3. Bấm CTA\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Kiểm tra DB: có bản ghi bots mới nào không",
       "4 field = chính channel_id/channel_secret hiện tại của bot",
       "- Hệ thống CHẶN, báo lỗi rõ ràng (không cho đổi sang chính LOA đang dùng)\n"
       "- DB: KHÔNG tạo bản ghi bots mới, KHÔNG đổi gì trên bot hiện tại\n"
       "- Bên LINE: không tạo LIFF app mới",
       note="Nguồn: TC-CBF-040 (FUNC-UNIQ-001; Blocked cả 2 env). "
            "⚠️ Ghi chú của nguồn: 'khác nghĩa FUNC-UNIQ-001 gốc — ở đây chặn trùng với CHÍNH record hiện tại "
            "vì đây là thao tác đổi sang bot khác'. Hành vi mong đợi là SUY LUẬN của AI, chưa có nguồn "
            "spec/TC cũ xác nhận → cần Leader chốt (chặn hay cho phép đổi về chính nó).",
       spec="Đã hỏi leader"),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Abnormal",
       "LINE API timeout / lỗi 5xx khi validate → báo lỗi rõ, KHÔNG báo thành công giả",
       INP + "\n- Có thể can thiệp mạng (DevTools throttle / block domain LINE API)",
       "1. Nhập 4 field hợp lệ\n"
       "2. Mở DevTools, chặn request tới domain LINE API (hoặc set throttle Offline sau khi bấm)\n"
       "3. Bấm CTA\n"
       "4. Quan sát màn hình và thông báo\n"
       "5. Kiểm tra DB bảng bots",
       "Block api.line.me / throttle Offline",
       "- Hiển thị thông báo lỗi rõ ràng (lỗi kết nối / thử lại)\n"
       "- TUYỆT ĐỐI KHÔNG hiển thị 'thành công' rồi sang màn xác nhận\n"
       "- DB: KHÔNG tạo bản ghi bots mới\n"
       "- Không đứng màn trắng / spinner vô hạn",
       note="Nguồn: TC-CBF-038 (INTG-LINE-001, 'false-success là lỗi nghiêm trọng theo catalog'; Pass dev) "
            "+ TC-CBF-104 (UI-003 + UIC-11 mất kết nối mạng; Pass dev + staging). "
            "RULE-05 + UI-003 nâng Cao khi có rủi ro false success. Evidence: ảnh màn lỗi + query bots."),

    tc("Nhập thông tin kết nối", "INTG-LINE-001", "Normal",
       "Webhook chưa bật trên LINE Developer Console → hệ thống tự check và chặn bằng thông báo lỗi",
       INP + "\n- LOA mới có webhook đang TẮT trên LINE Developer Console",
       "1. Tắt webhook của Messaging API channel trên LINE Developer Console\n"
       "2. Nhập 4 field hợp lệ của LOA đó\n"
       "3. Bấm CTA\n"
       "4. Quan sát thông báo lỗi\n"
       "5. Bật webhook lên rồi thử lại",
       "Webhook OFF trên LINE Developer Console",
       "- Hệ thống phát hiện webhook chưa bật và chặn lại bằng thông báo lỗi\n"
       "- Thông báo nêu rõ phải bật webhook\n"
       "- Sau khi bật webhook và thử lại: đi tiếp được",
       env="PRODUCTION",
       note="⚠️ MT-05 — CHƯA CHỐT cơ chế: TC-CBF-035 (BR-16, QA-spec-013 CONFIRMED) nói hệ thống TỰ "
            "check ở bước nhập; Change bot r148-r156/r284-r293 nói có MÀN RIÊNG bắt user tick checkbox "
            "「Webhookをオンに設定した」. Niên đại 2 nguồn GẦN NHAU (7/2026 vs 7-8/2026) → quy tắc 'TC mới nhất' "
            "là căn cứ YẾU ở đây. TC-CBF-035 Blocked cả 2 env vì 'webhook chỉ nhận đầy đủ tín hiệu ở production' "
            "(ENV-HOOK). RULE-08. Evidence: ảnh LINE Console + ảnh thông báo lỗi.",
       spec="Đã hỏi leader"),

    tc("Nhập thông tin kết nối", "UI-003", "Normal",
       "Loading state hiển thị rõ trong lúc chờ server validate channel",
       INP + "\n- Có DevTools để throttle mạng về Slow 3G",
       "1. Mở DevTools, set Network throttle = Slow 3G\n"
       "2. Nhập 4 field hợp lệ\n"
       "3. Bấm CTA và quan sát màn hình trong suốt thời gian chờ response\n"
       "4. Thử bấm CTA lần 2 trong lúc đang chờ",
       "Throttle Slow 3G; 4 field hợp lệ",
       "- Trong lúc chờ: có chỉ báo loading rõ ràng (spinner / nút chuyển trạng thái loading)\n"
       "- Nút CTA bị khóa trong lúc chờ → bấm lần 2 không gửi request thứ 2\n"
       "- Khi có response: loading tắt, chuyển màn hoặc hiện lỗi",
       note="Nguồn: TC-CBF-103 (UI-003 + UIC-11; Blocked cả 2 env) + TC-CBF-045 (CONC-001 double-click; "
            "Pass dev). Evidence: video thao tác + ảnh Network (đếm số request)."),

    tc("Nhập thông tin kết nối", "CONC-001", "Boundary",
       "Double-click nút CTA → chỉ 1 request validate được gửi, không tạo 2 bản ghi",
       INP + "\n" + LOA_OK,
       "1. Nhập 4 field hợp lệ\n"
       "2. Mở DevTools tab Network, xóa log cũ\n"
       "3. Double-click nhanh (trong <300ms) vào nút CTA\n"
       "4. Đếm số request validate trong Network\n"
       "5. Kiểm tra DB bảng bots đếm số bản ghi mới",
       "Double-click trong 300ms",
       "- Network: ĐÚNG 1 request validate được gửi (không phải 2)\n"
       "- DB: ĐÚNG 1 bản ghi bots mới (hoặc 0 nếu bước này chưa tạo bản ghi)\n"
       "- Không có thông báo lỗi trùng lặp\n"
       "- Chỉ chuyển màn 1 lần",
       note="Nguồn: TC-CBF-045 (CONC-001; Pass dev) + Change bot r141/r277 "
            "('double click button 次へ進む → tính 1 lần'). CONC-001 BẮT BUỘC khi có nút thực thi hành động "
            "quan trọng. RULE-07 — verify DB. Evidence: ảnh Network đếm request + query bots."),

    tc("Nhập thông tin kết nối", "FUNC-001", "Normal",
       "Bấm「キャンセル」ở màn nhập thông tin → quay về màn chọn phương thức",
       INP + "\n- Đã nhập sẵn 4 field",
       "1. Nhập 4 field bất kỳ\n"
       "2. Bấm nút「キャンセル」\n"
       "3. Quan sát màn hình đích\n"
       "4. Quan sát trạng thái lựa chọn option ở màn chọn phương thức",
       "4 field đã có data",
       "- Quay về màn chọn phương thức đổi LOA\n"
       "- Không gọi request validate nào\n"
       "- Không tạo bản ghi DB nào",
       note="Nguồn: TC-CBF-043 (BR-15; Blocked cả 2 env) + Change bot r259 "
            "(bản #37744: 'check btn キャンセル → back về màn chọn type change bot'). " + MT13
            + "Evidence: ảnh màn đích + Network trống."),

    tc("Nhập thông tin kết nối", "FUNC-DRAFT-001", "Boundary",
       "Reload trang khi đang nhập dở → dữ liệu 4 field bị mất (không có cơ chế lưu tạm)",
       INP,
       "1. Nhập đủ 4 field nhưng CHƯA bấm CTA\n"
       "2. Bấm F5 reload trang\n"
       "3. Quan sát 4 field sau khi load xong\n"
       "4. Quan sát trạng thái nút CTA",
       "4 field đã nhập đầy đủ, chưa submit",
       "- Sau reload: 4 field TRỐNG HẾT (mất dữ liệu)\n"
       "- Nút CTA trở lại DISABLED\n"
       "- Không có thông báo 'có dữ liệu chưa lưu' trước khi reload",
       note="Nguồn: TC-CBF-044 (FUNC-DRAFT-001; Pass dev + staging — xác nhận KHÔNG có lưu tạm). "
            "Evidence: ảnh trước/sau F5."),

    tc("Nhập thông tin kết nối", "UI-001", "Normal",
       "Cảnh báo rời trang khi đóng tab / đóng trình duyệt lúc đang nhập dở",
       INP + "\n- Đã nhập dở 2/4 field",
       "1. Nhập 2 field rồi thử đóng tab bằng nút × của tab\n"
       "2. Quan sát hộp thoại hiện ra\n"
       "3. Bấm「キャンセル」→ quan sát\n"
       "4. Lặp lại và bấm「このページを離れる」→ quan sát",
       "2/4 field đã nhập",
       "- Hiện hộp thoại「このサイトを離れますか?」+「行った変更が保存されない可能性があります。」với 2 nút\n"
       "- Bấm「キャンセル」: hộp thoại đóng, VẪN ở màn cũ, 2 field giữ nguyên giá trị\n"
       "- Bấm「このページを離れる」: tab đóng",
       note="Nguồn: Change bot r184-r186 (màn 5, TR=OK) + AddBot/Testcase r224-r226. "
            "⚠️ Text hộp thoại do trình duyệt render nên có thể khác theo locale trình duyệt. "
            "Evidence: ảnh hộp thoại."),

    tc("Nhập thông tin kết nối", "CONC-003", "Boundary",
       "Dùng Back/Forward trình duyệt qua lại giữa màn chọn phương thức và màn nhập → không sai hiển thị",
       INP,
       "1. Từ màn chọn phương thức (chọn option 1) sang màn nhập thông tin\n"
       "2. Nhập 2 field\n"
       "3. Bấm nút Back của trình duyệt → quan sát màn hình\n"
       "4. Bấm nút Forward → quan sát màn hình và 4 field\n"
       "5. Lặp lại Back/Forward 3 lần, quan sát có lẫn dữ liệu không",
       "3 vòng Back/Forward",
       "- Back: về đúng màn chọn phương thức, không hiện màn rỗng/trắng\n"
       "- Forward: về đúng màn nhập thông tin\n"
       "- KHÔNG hiển thị dữ liệu sai/lẫn của bước khác\n"
       "- Không có lỗi JS trên Console",
       note="Nguồn: TC-CBF-107 (CONC-003 + UIC-10; Pass dev + staging). Evidence: ảnh từng bước + Console."),

    tc("Nhập thông tin kết nối", "UI-001", "Normal",
       "Link phụ trên màn nhập thông tin mở đúng tab mới, bấm 2 lần không mở 2 tab",
       INP,
       "1. Bấm chữ/nút「使い方を見る」→ quan sát tab mới và URL\n"
       "2. Quay lại, bấm「設定動画をスマホで見る」→ quan sát\n"
       "3. Quay lại, bấm link「LINE developers」→ quan sát URL tab mới\n"
       "4. Với từng link, bấm 2 lần nhanh liên tiếp và đếm số tab mở ra",
       "3 link phụ trên màn nhập thông tin",
       "-「使い方を見る」→ mở tab mới tới https://lme.jp/manual/loa_replacement/\n"
       "-「設定動画をスマホで見る」→ hiển thị ảnh QR code, quét được bằng LINE/camera để xem video\n"
       "-「LINE developers」→ mở tab mới tới https://developers.line.biz/ja/\n"
       "- Mỗi link bấm 2 lần nhanh chỉ mở ĐÚNG 1 tab",
       note="Nguồn: Change bot r119/r139/r255/r275 (TR=OK) + r109-r111. ⚠️ MT-14 — "
            "nguồn [AI] v2 mô tả「使い方を見る」mở video chứ không phải trang manual. "
            "Evidence: ảnh 3 tab mới + URL + đếm tab khi double-click."),
]
