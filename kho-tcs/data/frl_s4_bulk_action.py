# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 6-8: 友だち一括アクション — ngưỡng 200 & action schedule,
các loại action, trigger hiển thị ở chat 1:1 và profile gửi.

Nguồn chính: 10.3 TCsLine_Friendlist → tab「Testcase」(02/2026 → 07/2026, tab master
còn sống, 6 cột ticket: SpecImprove #34438 · #34720 · Bug KH #35071 · SpecImprove
#35389 · Bug #38390 · Bug KH #38866). Số dòng `r<n>` là dòng của tab「Testcase」
trừ khi ghi rõ tab khác.

⚠ Modal chọn action là SHARED COMPONENT SC-004 (エルメアクション), dùng chung bởi 12
tính năng. Kho FA-013 chỉ giữ TC『action đăng ký được và thực thi đúng khi chạy từ
màn friendlist』; chi tiết cấu hình từng loại action thuộc TCsLine_ModalAction (7 tab)
— đề xuất tách feature riêng『SC-004 エルメアクション』.
"""
from _common import tc

BOT = ("- Đăng nhập Admin (role 主管理者) của bot đã liên kết LINE OA\n"
       "- Bot có ≥ 250 friend đang kết bạn\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai (để đếm chính xác)\n"
       "- Mở /basic/friendlist")
BOT_SMALL = ("- Đăng nhập Admin của bot có ĐÚNG 200 friend đang kết bạn\n"
             "- Đã tạo sẵn 1 tag mới chưa gắn cho ai\n"
             "- Mở /basic/friendlist")
STAFF = ("- Chuẩn bị 2 tài khoản: 1 主管理者 và 1 staff có quyền thao tác màn 友だちリスト\n"
         "- Bot có ≥ 10 friend\n"
         "- Mở /basic/friendlist")

S4 = [
    # ═══════════ 6. Bulk action — ngưỡng 200 & schedule ═══════════
    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Normal",
       "Chọn thủ công 1 friend — action chạy ngay, không tạo action schedule",
       BOT,
       "1. Không lọc, không search\n"
       "2. Tích 1 friend bất kỳ (KHÔNG tích 全選択)\n"
       "3. Chọn action Add Tag với tag mới → thực thi\n"
       "4. Mở màn danh sách アクションスケジュール実行 kiểm tra có bản ghi mới không\n"
       "5. Mở màn chi tiết tag đếm số friend",
       "1 friend được chọn",
       "- Action chạy NGAY cho friend đã chọn\n"
       "- KHÔNG tạo bản ghi「【自動生成】友だち一括アクション」ở màn action schedule\n"
       "- Màn chi tiết tag hiển thị đúng 1 friend",
       spec="Đã hỏi leader",
       note="Nguồn: r5. ⚠ MT-04: trong CÙNG ô kết quả mong đợi có 2 tầng — tầng cũ『send "
            "action luôn, không tạo schedule』và tầng SpecImprove #34720 (03/2026)『KHÔNG send "
            "luôn, ghi bảng action_lineuser (type='friendList', type_start_scenario=15001), "
            "job send』. Spec KHÔNG nhắc bảng action_lineuser (grep 0 hit). Chờ Leader chốt."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Chọn thủ công trong cùng 1 trang — biên 199 và 200 friend",
       BOT,
       "1. Tích thủ công đúng 199 friend trong cùng 1 trang → chạy Add Tag (tag mới A)\n"
       "2. Kiểm tra màn action schedule + đếm friend gắn tag A\n"
       "3. Reload, tích 全選択 (200 friend của trang) → chạy Add Tag (tag mới B)\n"
       "4. Kiểm tra màn action schedule + đếm friend gắn tag B",
       "199 friend · 200 friend (đều ≤ ngưỡng 200)",
       "- Cả 2 lần: action chạy NGAY, KHÔNG tạo bản ghi action schedule\n"
       "- Tag A gắn cho đúng 199 friend\n"
       "- Tag B gắn cho đúng 200 friend",
       spec="Đã hỏi leader",
       note="Nguồn: r6, r7. Ghi chú TC gốc r6:『check chọn nhiều friend cùng lúc, số fr < 200』. "
            "Gắn MT-04."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Không thể chọn quá 200 friend trong CÙNG 1 trang (1 trang tối đa 200 dòng)",
       BOT,
       "1. Mở 1 trang bất kỳ của danh sách\n"
       "2. Tích 全選択 → đếm số friend được chọn\n"
       "3. Thử tích thêm friend thứ 201 trong cùng trang đó",
       "1 trang danh sách chính",
       "- Số friend chọn được tối đa trong 1 trang = 200\n"
       "- Không tồn tại friend thứ 201 trong cùng trang để tích\n"
       "- Muốn vượt 200 phải chọn qua nhiều trang hoặc dùng checkbox chọn toàn bộ",
       spec="Đã hỏi leader",
       note="Nguồn: r8, r24 — TC gốc ghi kết quả thực tế『Không có case này do số user 1 page "
            "max là 200』và đánh Reject ở cả 2 cột ticket. Kho giữ lại dưới dạng TC xác nhận "
            "ràng buộc phân trang, vì đây là căn cứ cho biên 200/201 ở nhóm checkbox. "
            "Gắn MT-02 (page size khi có search)."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Chọn thủ công friend ở NHIỀU trang khác nhau — 199 / 200 / 201 friend",
       BOT + "\n- Bot có ≥ 400 friend để chọn được qua nhiều trang",
       "1. Tích friend rải qua nhiều trang cho tới khi counter = 199 → chạy Add Tag (tag A)\n"
       "2. Lặp lại cho counter = 200 → chạy Add Tag (tag B)\n"
       "3. Lặp lại cho counter = 201 → chạy Add Tag (tag C)\n"
       "4. Với mỗi lần: kiểm tra màn action schedule và đếm friend gắn tag tương ứng",
       "199 · 200 · 201 friend chọn qua nhiều trang",
       "- Cả 3 lần: action chạy NGAY cho các friend đã chọn, KHÔNG tạo action schedule "
       "(vì đi luồng chọn từng friend, không phải luồng chọn-toàn-bộ)\n"
       "- Tag A = 199 friend · Tag B = 200 friend · Tag C = 201 friend\n"
       "- Trạng thái tích của trang trước KHÔNG bị mất khi sang trang sau",
       spec="Đã hỏi leader",
       note="Nguồn: r9, r10, r11. Gắn MT-04."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Chọn thủ công 1.000 friend qua nhiều trang — vẫn đi luồng chọn từng friend",
       BOT + "\n- Bot có ≥ 1.100 friend",
       "1. Tích friend qua nhiều trang cho tới khi counter = 1.000\n"
       "2. Chạy Add Tag với tag mới → ghi lại thời gian phản hồi\n"
       "3. Kiểm tra màn action schedule\n"
       "4. Đếm số friend trên màn chi tiết tag",
       "1.000 friend chọn thủ công qua nhiều trang",
       "- Action gửi cho đủ 1.000 friend đã chọn\n"
       "- Ghi lại thực tế có tạo action schedule hay không để Leader chốt\n"
       "- Số friend được gắn tag = 1.000",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r12, r13 — cột SpecImprove #34720 đánh **Reject**, cột #34438 đánh OK. "
            "2 cột ticket cho 2 kết quả khác nhau trên cùng 1 dòng → gắn MT-04, cần Leader "
            "chốt luồng hiện hành. RULE-08: khối lượng lớn + job → chạy PRODUCTION."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Tích checkbox chọn toàn bộ khi bot có ĐÚNG 200 friend — không tạo schedule",
       BOT_SMALL,
       "1. Không search, tích 全選択\n"
       "2. Quan sát checkbox「条件に当てはまる...」\n"
       "3. Chạy Add Tag với tag mới\n"
       "4. Kiểm tra màn action schedule và đếm friend gắn tag",
       "Bot có ĐÚNG 200 friend",
       "- Checkbox「条件に当てはまる...」KHÔNG hiển thị (200 ≤ ngưỡng)\n"
       "- Action chạy NGAY, KHÔNG tạo bản ghi action schedule\n"
       "- Tag gắn cho đúng 200 friend",
       spec="Đã hỏi leader",
       note="Nguồn: r18, #38866 r6. ⚠ MT-04: thông báo hiển thị cho user theo logic-spec.md:252 "
            "là「対象の友だち数が200人以上の場合、処理に時間がかかる場合があります。」(≥200) "
            "trong khi logic là >200 — lệch 1 đơn vị ở chính con số biên này."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Tích checkbox chọn toàn bộ khi bot có 201 friend — tạo action schedule",
       "- Đăng nhập Admin của bot có ĐÚNG 201 friend đang kết bạn\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai\n"
       "- Mở /basic/friendlist",
       "1. Không search, tích 全選択 → tích checkbox「条件に当てはまる友だち201人全員を選択」\n"
       "2. Chạy Add Tag với tag mới, ghi lại thông báo hiển thị cho user\n"
       "3. Mở màn アクションスケジュール実行 tìm bản ghi mới\n"
       "4. Chờ job chạy xong → đếm số friend trên màn chi tiết tag\n"
       "5. Kiểm tra bản ghi schedule sau khi chạy xong",
       "Bot có ĐÚNG 201 friend",
       "- KHÔNG send action ngay\n"
       "- Tạo bản ghi action schedule tên「【自動生成】友だち一括アクション」\n"
       "- Job chạy và gửi action cho đủ 201 friend — tag gắn cho 201 friend\n"
       "- Bản ghi schedule bị XOÁ sau khi chạy xong (chạy 1 lần)",
       env="PRODUCTION",
       note="Nguồn: r19 (ghi chú TC gốc:『trên step test bot của KH có 250 friend』) + "
            "feature-spec.md §7.1 (tên record, one-time execution). RULE-08: job → PRODUCTION."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Tích checkbox chọn toàn bộ với 1.000 / 1.001 friend — job gửi đủ, không sót",
       "- Đăng nhập Admin của bot có ≥ 1.001 friend\n"
       "- Đã tạo sẵn 2 tag mới chưa gắn cho ai\n"
       "- Mở /basic/friendlist",
       "1. Ở bot có 1.000 friend: tích 全選択 + checkbox → Add Tag (tag A) → chờ job xong → "
       "đếm friend gắn tag A\n"
       "2. Ở bot có 1.001 friend: lặp lại với tag B → đếm friend gắn tag B\n"
       "3. Với mỗi lần: kiểm tra màn 配信エラー xem có message lỗi nào không",
       "1.000 friend · 1.001 friend",
       "- Cả 2 lần đều tạo action schedule, không gửi ngay\n"
       "- Tag A gắn cho đủ 1.000 friend · Tag B gắn cho đủ 1.001 friend\n"
       "- Không friend nào bị sót, không friend nào nhận action 2 lần\n"
       "- Màn 配信エラー không có bản ghi lỗi mới",
       env="PRODUCTION",
       note="Nguồn: r20, r21 — cột SpecImprove #34720 đánh Reject, cột #34438 đánh OK. "
            "Gắn MT-04. RULE-08: job + khối lượng lớn → PRODUCTION."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Normal",
       "Có filter + tích thủ công friend — chỉ friend đã tích nhận action",
       BOT + "\n- Chuẩn bị TagA gắn cho ≥ 250 friend",
       "1. Lọc「タグ = TagA」→ 保存\n"
       "2. Tích thủ công 5 friend trong kết quả (KHÔNG tích 全選択)\n"
       "3. Chạy Add Tag với tag mới → đếm số friend được gắn\n"
       "4. Kiểm tra màn action schedule",
       "TagA = 250 friend, tích thủ công 5",
       "- Chỉ 5 friend đã tích nhận action\n"
       "- KHÔNG tạo action schedule\n"
       "- 245 friend còn lại của TagA KHÔNG nhận action",
       note="Nguồn: r22-r29 (nhóm『Check case có filter → tick chọn friend và send action』)."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Boundary",
       "Có filter + chọn toàn bộ — biên 200 / 201 friend thoả filter",
       BOT + "\n- Chuẩn bị TagA gắn ĐÚNG 200 friend, TagB gắn ĐÚNG 201 friend",
       "1. Lọc「タグ = TagA」→ tích 全選択 (+ checkbox nếu hiện) → Add Tag (tag mới X) → "
       "kiểm tra action schedule + đếm friend gắn X\n"
       "2.「クリア」rồi lọc「タグ = TagB」→ tích 全選択 + checkbox → Add Tag (tag mới Y) → "
       "kiểm tra action schedule + đếm friend gắn Y",
       "TagA = 200 friend · TagB = 201 friend",
       "- TagA (200): action chạy ngay, KHÔNG tạo schedule, tag X gắn cho 200 friend\n"
       "- TagB (201): TẠO action schedule, job gửi cho 201 friend, tag Y gắn cho 201 friend\n"
       "- Không friend nào ngoài nhóm thoả filter bị gắn tag",
       env="PRODUCTION",
       note="Nguồn: r31, r32."),

    tc("Bulk action — ngưỡng 200 & schedule", "DATA-COUNT-001", "Normal",
       "⭐ Case tái hiện bug KH #38866 — search 312 người, đúng 312 người nhận action",
       "- Đăng nhập Admin của bot có ~4.500 friend, trong đó 312 friend tên chứa「6期生」\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai\n"
       "- Mở /basic/friendlist",
       "1. Nhập「6期生」vào ô tìm kiếm → tìm kiếm\n"
       "2. Tích 全選択 → tích checkbox「条件に当てはまる友だち312人全員を選択」\n"
       "3. Chạy action Add Tag với tag mới\n"
       "4. Chờ job chạy xong\n"
       "5. Mở màn chi tiết tag đọc số friend đang gắn\n"
       "6. Kiểm tra ngẫu nhiên 5 friend KHÔNG khớp「6期生」xem có bị gắn tag không",
       "312 friend khớp「6期生」/ tổng 4.500 friend",
       "- Điều kiện lọc lưu cho job ĐÚNG keyword「6期生」\n"
       "- Màn chi tiết tag hiển thị **312**, KHÔNG phải 4.504\n"
       "- 5 friend không khớp keyword đều KHÔNG có tag mới\n"
       "- Số N trên nhãn checkbox = số friend thực tế nhận action",
       env="PRODUCTION",
       note="Nguồn: 10.3 TCsLine_Friendlist → tab「#38866」r9 (case tái hiện chính của KH) + r66 "
            "(『⭐ ASSERTION QUAN TRỌNG NHẤT: bug gốc N=312 nhưng 4.504 friend nhận action, lệch "
            "4.192』). RULE-08: job + bill/khối lượng lớn → PRODUCTION."),

    tc("Bulk action — ngưỡng 200 & schedule", "DATA-COUNT-001", "Normal",
       "⭐ TC chẩn đoán — 4 con số phải bằng nhau khi có friend khớp qua email",
       "- Đăng nhập Admin của bot có > 200 friend khớp keyword qua CẢ tên lẫn email\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai\n"
       "- Mở /basic/friendlist",
       "1. Search keyword khớp cả tên lẫn email, cho ra > 200 kết quả\n"
       "2. Đếm số friend hiển thị trong danh sách (số 1)\n"
       "3. Tích 全選択 + checkbox → đọc N trên nhãn (số 2)\n"
       "4. Đọc counter panel「選択中 N人」(số 3)\n"
       "5. Chạy Add Tag → chờ job → đếm số friend trên màn chi tiết tag (số 4)",
       "keyword khớp cả 友だち名 lẫn メールアドレス, tổng > 200",
       "- CẢ 4 con số PHẢI BẰNG NHAU\n"
       "- Nếu lệch, xác định đúng điểm lệch: số 1 ≠ số 2 → lệch giữa API hiển thị danh sách "
       "và API đếm; số 2 ≠ số 4 → lệch giữa lúc đếm và điều kiện lọc lưu cho job",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: tab「#38866」r32 —『⭐ TC chẩn đoán — khoanh vùng điểm lệch』. Gắn MT-01."),

    tc("Bulk action — ngưỡng 200 & schedule", "REG-SHARED-001", "Normal",
       "Regression — keyword chỉ khớp TÊN, không dính email: mốc đối chứng phải đúng tuyệt đối",
       "- Đăng nhập Admin của bot có > 200 friend khớp keyword qua 友だち名, "
       "KHÔNG friend nào khớp qua email\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai",
       "1. Search keyword đó → ghi N\n"
       "2. Tích 全選択 + checkbox → chạy Add Tag\n"
       "3. Chờ job xong → đếm số friend trên màn chi tiết tag",
       "> 200 friend khớp CHỈ qua 友だち名",
       "- Số friend nhận action = N\n"
       "- Nhóm không liên quan email phải đúng tuyệt đối\n"
       "- Nếu case này còn FAIL thì fix của #38866 sai từ gốc",
       env="PRODUCTION",
       note="Nguồn: tab「#38866」r34 —『Mốc đối chứng cho nhóm email』."),

    tc("Bulk action — ngưỡng 200 & schedule", "JOB-001", "Normal",
       "Đặt lịch chạy action với điều kiện lọc theo keyword — job chạy đúng số friend",
       "- Đăng nhập Admin của bot có > 200 friend khớp keyword\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai",
       "1. Search keyword (> 200 kết quả) → tích 全選択 + checkbox → ghi N\n"
       "2. Chọn action Add Tag, đặt lịch chạy sau 10 phút\n"
       "3. Mở màn アクションスケジュール実行 kiểm tra bản ghi vừa tạo (tên, thời gian chạy, "
       "điều kiện lọc)\n"
       "4. Chờ đến giờ, theo dõi job chạy\n"
       "5. Đếm số friend trên màn chi tiết tag; kiểm tra bản ghi schedule sau khi chạy",
       "keyword khớp > 200 friend, đặt lịch now + 10 phút",
       "- Bản ghi action schedule được tạo với điều kiện lọc ĐÚNG keyword user nhập\n"
       "- Đến giờ, job chạy và gắn tag cho đúng N friend\n"
       "- Sau khi chạy xong, bản ghi schedule bị xoá\n"
       "- ⚠ Nếu điều kiện lọc không lưu cột email → nhóm friend chỉ-khớp-email bị sót",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: tab「#38866」r33 —『⏳ Kết hợp email + đặt lịch』. Gắn MT-01. RULE-08: job → "
            "PRODUCTION."),

    tc("Bulk action — ngưỡng 200 & schedule", "BULK-001", "Normal",
       "Regression — tích 全選択 nhưng KHÔNG tích checkbox: chỉ trang hiện tại nhận action",
       "- Đăng nhập Admin của bot có ~4.500 friend, 312 friend khớp「6期生」\n"
       "- Đã tạo sẵn 1 tag mới chưa gắn cho ai",
       "1. Search「6期生」→ 312 kết quả\n"
       "2. Tích 全選択, KHÔNG tích checkbox「条件に当てはまる...」\n"
       "3. Chạy Add Tag với tag mới\n"
       "4. Kiểm tra màn action schedule + đếm friend trên màn chi tiết tag",
       "312 friend khớp, chỉ tích 全選択",
       "- Chỉ 200 friend của trang hiện tại nhận action\n"
       "- KHÔNG tạo action schedule (đi luồng chọn từng friend)\n"
       "- 112 friend còn lại KHÔNG nhận action\n"
       "- Số friend gắn tag = 200",
       spec="Đã hỏi leader",
       note="Nguồn: tab「#38866」r10, r75 —『Regression — phân biệt rõ 2 checkbox』. "
            "Gắn MT-02 (nếu kết quả search thật sự 50/trang thì con số 200 ở đây phải là 50)."),

    # ═══════════ 7. Bulk action — các loại action ═══════════
    tc("Bulk action — các loại action", "MSG-004", "Normal",
       "Action gửi tin nhắn text — friend nhận đúng nội dung trên LINE",
       BOT,
       "1. Tích 3 friend test (có thể xem được LINE thật)\n"
       "2. Chọn action gửi text với nội dung「テスト送信です」→ thực thi\n"
       "3. Mở app LINE của 3 friend kiểm tra tin nhắn nhận được\n"
       "4. Mở màn chat 1:1 của từng friend kiểm tra tin đã gửi",
       "3 friend · nội dung text「テスト送信です」",
       "- Cả 3 friend nhận được tin nhắn đúng nội dung「テスト送信です」trên app LINE\n"
       "- Màn chat 1:1 của cả 3 friend hiển thị tin đã gửi\n"
       "- Không friend nào ngoài 3 friend đã chọn nhận tin",
       note="Nguồn: r35 + r14 (『Check account staff thao tác』). RULE-06: verify tới output "
            "cuối là app LINE, không chỉ dừng ở màn admin."),

    tc("Bulk action — các loại action", "MSG-004", "Normal",
       "Action gửi template — friend nhận đủ mọi message trong template",
       BOT + "\n- Đã tạo sẵn 1 template gồm 3 message (text + ảnh + panel button)",
       "1. Tích 3 friend test\n"
       "2. Chọn action gửi template đã chuẩn bị → thực thi\n"
       "3. Mở app LINE của 3 friend, đếm số message nhận được và kiểm tra thứ tự\n"
       "4. Mở màn chat 1:1 đối chiếu",
       "template gồm 3 message: text → ảnh → panel button",
       "- Mỗi friend nhận đúng 3 message, đúng thứ tự text → ảnh → panel button\n"
       "- Ảnh hiển thị được, panel button bấm được\n"
       "- Màn chat 1:1 hiển thị đủ 3 message",
       note="Nguồn: r36. Chi tiết ma trận action của panel button thuộc FA-010 Mẫu tin nhắn — "
            "kho FA-013 chỉ giữ mức『gửi template có action → friend bấm thì action chạy』."),

    tc("Bulk action — các loại action", "MSG-002", "Normal",
       "Action bắt đầu / dừng ステップ配信 — trạng thái scenario của friend đổi đúng",
       BOT + "\n- Đã tạo sẵn scenario「S1」có message gửi ngay ở step đầu",
       "1. Tích 3 friend chưa đăng ký scenario nào\n"
       "2. Chọn action bắt đầu scenario S1 → thực thi\n"
       "3. Kiểm tra cột「ステップ配信状況」của 3 friend trên màn friendlist\n"
       "4. Kiểm tra app LINE có nhận message gửi ngay của step đầu không\n"
       "5. Tích lại 3 friend, chọn action dừng scenario → kiểm tra lại cột trạng thái",
       "3 friend · scenario S1 có message send ngay",
       "- Sau bước 2: cột「ステップ配信状況」của 3 friend hiển thị tên「S1」\n"
       "- Cả 3 friend nhận được message gửi ngay của step đầu trên app LINE\n"
       "- Sau bước 5: cột「ステップ配信状況」hiển thị「停止中」",
       note="Nguồn: r37 + r112, r113 (trigger start/stop scenario)."),

    tc("Bulk action — các loại action", "MSG-002", "Normal",
       "Action bắt đầu / dừng リマインド配信 — trạng thái remind của friend đổi đúng",
       BOT + "\n- Đã tạo sẵn 1 remind「R1」có message gửi ngay",
       "1. Tích 3 friend\n"
       "2. Chọn action bắt đầu remind R1 → thực thi\n"
       "3. Kiểm tra app LINE của 3 friend\n"
       "4. Tích lại 3 friend, chọn action dừng remind → kiểm tra trạng thái",
       "3 friend · remind R1",
       "- 3 friend nhận được message gửi ngay của remind trên app LINE\n"
       "- Trạng thái remind của friend chuyển sang đang chạy\n"
       "- Sau khi dừng: remind không còn chạy, friend không nhận message tiếp theo",
       note="Nguồn: r38 + r114, r115."),

    tc("Bulk action — các loại action", "FUNC-001", "Normal",
       "Action ẩn friend (非表示) — friend rời danh sách chính sang màn 非表示中の友だち",
       BOT,
       "1. Tích 2 friend, ghi lại tên\n"
       "2. Chọn action ẩn friend → thực thi\n"
       "3. Reload danh sách chính, tìm 2 friend đó\n"
       "4. Mở /basic/friendlist/hidden tìm 2 friend đó\n"
       "5. Mở màn chat 1:1 của 2 friend kiểm tra có message hệ thống về việc ẩn không",
       "2 friend bị ẩn",
       "- 2 friend biến mất khỏi danh sách chính, số「検索結果」giảm 2\n"
       "- 2 friend xuất hiện ở màn「非表示中の友だち」với cột「非表示にした日時」đúng thời điểm ẩn\n"
       "- Màn chat 1:1 KHÔNG hiển thị message về việc ẩn friend",
       note="Nguồn: r39 (『Action ẩn friend → Ẩn được friend / Màn chat 1:1 không có message "
            "ẩn friend』). ⭐ TC này LẤP GAP #2 của spec (feature-spec.md §9: cơ chế trigger ẩn "
            "bạn bè chưa rõ) — xem MT-09."),

    tc("Bulk action — các loại action", "FUNC-001", "Normal",
       "Action block friend — friend chuyển sang màn ブロックした友だち",
       BOT,
       "1. Tích 2 friend, ghi lại tên\n"
       "2. Chọn action block friend → thực thi\n"
       "3. Reload danh sách chính, tìm 2 friend đó\n"
       "4. Mở /basic/friendlist/block tìm 2 friend đó\n"
       "5. Mở màn chat 1:1 của 2 friend kiểm tra có message hệ thống không",
       "2 friend bị admin block",
       "- 2 friend biến mất khỏi danh sách chính\n"
       "- 2 friend xuất hiện ở màn「ブロックした友だち」với「ブロックした日時」đúng\n"
       "- Màn chat 1:1 KHÔNG hiển thị message về việc block friend",
       note="Nguồn: r40. ⚠ Đối chiếu r116/r117: khi action chạy QUA JOB (action schedule) thì "
            "màn chat 1:1 LẠI hiển thị message block friend kèm tên user thao tác — 2 đường đi "
            "cho 2 kết quả khác nhau, xem TC riêng ở nhóm『trigger & profile gửi』."),

    tc("Bulk action — các loại action", "FUNC-001", "Normal",
       "Action bỏ ẩn (unhide) và bỏ block (unblock) từ bulk action",
       BOT + "\n- Chuẩn bị 2 friend đang bị ẩn và 2 friend đang bị admin block",
       "1. Ở màn「非表示中の友だち」tích 2 friend đang ẩn → chạy action unhide → kiểm tra "
       "danh sách chính\n"
       "2. Ở màn「ブロックした友だち」tích 2 friend đang block → chạy action unblock → "
       "kiểm tra danh sách chính",
       "2 friend ẩn · 2 friend admin block",
       "- 2 friend được bỏ ẩn quay lại danh sách chính, biến mất khỏi màn 非表示中\n"
       "- 2 friend được bỏ block quay lại danh sách chính, biến mất khỏi màn ブロックした\n"
       "- Số「検索結果」ở danh sách chính tăng đúng 4",
       note="Nguồn: r41, r42."),

    tc("Bulk action — các loại action", "FUNC-001", "Normal",
       "Các loại action còn lại: tag · richmenu · friend info · bookmark · 対応ステータス",
       BOT + "\n- Đã tạo sẵn: 1 tag mới, 1 richmenu, 1 friend info kiểu Mô tả, 1 対応ステータス",
       "1. Với mỗi loại action, tích cùng 3 friend rồi thực thi lần lượt:\n"
       "   a. Gắn tag → kiểm tra màn chi tiết tag\n"
       "   b. Gán richmenu → mở app LINE của friend xem richmenu hiển thị\n"
       "   c. Ghi giá trị friend info → mở màn chi tiết bạn bè xem giá trị\n"
       "   d. Bookmark → kiểm tra trạng thái bookmark\n"
       "   e. Gán 対応ステータス → kiểm tra trạng thái ở màn chat 1:1",
       "3 friend · 5 loại action",
       "- a. Màn chi tiết tag hiển thị đúng 3 friend\n"
       "- b. App LINE của 3 friend hiển thị đúng richmenu mới\n"
       "- c. Giá trị friend info được ghi đúng cho cả 3 friend\n"
       "- d. 3 friend được đánh dấu bookmark\n"
       "- e. 3 friend có 対応ステータス mới ở màn chat 1:1",
       note="Nguồn: r43 (『Check random các action khác: tag, richmenu, friend info, bookmark, "
            "add status』) + r126. ⭐ Nhóm TC này LẤP GAP #1 của spec (feature-spec.md §9: nội "
            "dung nút「アクション選択」chưa thu thập) — xem MT-10."),

    tc("Bulk action — các loại action", "REG-SHARED-001", "Normal",
       "Action của tính năng khác (form, booking) gọi từ friendlist chạy đúng",
       BOT + "\n- Đã tạo sẵn 1 form và 1 lịch booking có action gắn kèm",
       "1. Tích 3 friend\n"
       "2. Chạy lần lượt các action thuộc tính năng form / booking\n"
       "3. Kiểm tra app LINE của friend và màn chat 1:1",
       "3 friend · action của form và booking",
       "- Action được thực thi cho cả 3 friend\n"
       "- Màn chat 1:1 hiển thị đúng trigger của tính năng có action đó\n"
       "- Message gửi cho friend dùng profile default",
       note="Nguồn: r35-r38 (『Check random 1 số action của tính năng khác (form, booking, ...)』)."),

    # ═══════════ 8. Bulk action — trigger & profile gửi ═══════════
    tc("Bulk action — trigger & profile gửi", "DATA-AUDIT-001", "Normal",
       "Trigger ở chat 1:1 hiển thị 手動操作 kèm tên tài khoản chính đã thao tác",
       STAFF,
       "1. Đăng nhập tài khoản 主管理者\n"
       "2. Ở màn friendlist tích 1 friend → chạy action gửi text\n"
       "3. Mở màn chat 1:1 của friend đó\n"
       "4. Click vào khối trigger, đọc từng trường",
       "1 friend · action gửi text · người thao tác là 主管理者",
       "Khối trigger hiển thị:\n"
       "-「機能名」=「手動操作」\n"
       "-「管理名」=「-」\n"
       "-「詳細」= tên tài khoản 主管理者 đã thao tác\n"
       "-「トリガー稼働日時」= thời điểm chạy action, format「2026年03月03日（火） 17:50」",
       note="Nguồn: r93 + r4 (khối mô tả nội dung trigger khi send action ở friendlist)."),

    tc("Bulk action — trigger & profile gửi", "DATA-AUDIT-001", "Normal",
       "Trigger ở chat 1:1 hiển thị đúng tên STAFF khi staff thao tác",
       STAFF,
       "1. Đăng nhập tài khoản staff\n"
       "2. Ở màn friendlist tích 1 friend → chạy action gửi text\n"
       "3. Đăng nhập lại bằng 主管理者, mở màn chat 1:1 của friend đó\n"
       "4. Đọc trường「詳細」của khối trigger",
       "1 friend · action gửi text · người thao tác là staff",
       "-「詳細」hiển thị tên tài khoản STAFF đã thao tác, KHÔNG phải tên 主管理者\n"
       "-「機能名」vẫn là「手動操作」",
       note="Nguồn: r14, r30, r94."),

    tc("Bulk action — trigger & profile gửi", "MSG-004", "Normal",
       "Profile gửi lấy theo profile đang chọn ở màn chat 1:1 — trường hợp profile default",
       BOT + "\n- Bot có ≥ 2 profile gửi (1 default + 1 khác)\n"
             "- Ở màn chat 1:1 đang chọn profile DEFAULT",
       "1. Mở màn chat 1:1, xác nhận profile đang chọn là default\n"
       "2. Sang màn friendlist, tích 1 friend → chạy action gửi text\n"
       "3. Mở app LINE của friend xem tên/ảnh người gửi\n"
       "4. Mở màn chat 1:1 xem profile của message vừa gửi",
       "profile đang chọn = default",
       "- Phía LINE user: message hiện profile DEFAULT (đúng tên + ảnh)\n"
       "- Màn chat 1:1: message hiện profile DEFAULT",
       note="Nguồn: r15 (logic: send ở friendlist lấy profile đang chọn ở màn chat 1:1) + r95."),

    tc("Bulk action — trigger & profile gửi", "MSG-004", "Normal",
       "Profile gửi lấy theo profile đang chọn ở màn chat 1:1 — trường hợp KHÁC default",
       BOT + "\n- Bot có ≥ 2 profile gửi\n"
             "- Ở màn chat 1:1 đã chọn 1 profile KHÁC default",
       "1. Mở màn chat 1:1, chọn profile khác default, ghi lại tên/ảnh profile đó\n"
       "2. Sang màn friendlist, tích 1 friend → chạy action gửi text\n"
       "3. Mở app LINE của friend xem tên/ảnh người gửi\n"
       "4. Mở màn chat 1:1 xem profile của message vừa gửi",
       "profile đang chọn ≠ default",
       "- Phía LINE user: message hiện đúng profile ĐÃ CHỌN\n"
       "- Màn chat 1:1: message hiện đúng profile ĐÃ CHỌN",
       note="Nguồn: r16, r17, r96."),

    tc("Bulk action — trigger & profile gửi", "MSG-004", "Normal",
       "Staff thao tác — profile gửi theo profile staff đang chọn ở chat 1:1",
       STAFF + "\n- Bot có ≥ 2 profile gửi, staff có profile riêng",
       "1. Đăng nhập staff, mở màn chat 1:1, chọn profile của tài khoản staff\n"
       "2. Sang màn friendlist, tích 1 friend → chạy action gửi text\n"
       "3. Mở app LINE của friend xem tên/ảnh người gửi\n"
       "4. Lặp lại với profile default",
       "staff thao tác · 2 lần với 2 profile khác nhau",
       "- Lần chọn profile staff: LINE user thấy profile của staff\n"
       "- Lần chọn profile default: LINE user thấy profile default\n"
       "- Màn chat 1:1 hiển thị profile khớp với phía LINE user",
       note="Nguồn: r97, r98."),

    tc("Bulk action — trigger & profile gửi", "JOB-001", "Normal",
       "Action chạy QUA JOB (action schedule) — trigger và profile giữ đúng như chạy trực tiếp",
       "- Đăng nhập Admin của bot có > 200 friend\n"
       "- Ở màn chat 1:1 đang chọn 1 profile KHÁC default\n"
       "- Mở /basic/friendlist",
       "1. Tích 全選択 + checkbox chọn toàn bộ (> 200 friend) → chạy action gửi text\n"
       "2. Chờ job chạy xong\n"
       "3. Mở màn chat 1:1 của 3 friend ngẫu nhiên, đọc khối trigger và profile message\n"
       "4. Mở app LINE của 1 friend test xem profile người gửi",
       "> 200 friend → đi luồng action schedule",
       "- Khối trigger hiển thị「機能名」=「手動操作」,「詳細」= tên user đã thao tác\n"
       "- Message dùng đúng profile ĐÃ CHỌN ở màn chat 1:1 (không tự rơi về default)\n"
       "- Phía LINE user thấy đúng profile đó",
       env="PRODUCTION",
       note="Nguồn: r93-r98 (nhóm『Check case friendlist không filter → Tạo action schedule "
            "send cho all friend』)."),

    tc("Bulk action — trigger & profile gửi", "DATA-AUDIT-001", "Normal",
       "Action block / ẩn friend chạy QUA JOB — chat 1:1 CÓ hiển thị message thao tác",
       "- Đăng nhập Admin của bot có > 200 friend\n"
       "- Mở /basic/friendlist",
       "1. Tích 全選択 + checkbox (> 200 friend) → chạy action block friend\n"
       "2. Chờ job chạy xong\n"
       "3. Mở màn chat 1:1 của 1 friend bị block, đọc message hệ thống\n"
       "4. Lặp lại bước 1-3 với action ẩn friend (dùng nhóm friend khác)\n"
       "5. Lặp lại toàn bộ với tài khoản staff thao tác",
       "> 200 friend · action block và action ẩn · 2 loại tài khoản thao tác",
       "- Action block qua job: chat 1:1 HIỂN THỊ message block friend kèm tên user thao tác\n"
       "- Action ẩn qua job: chat 1:1 HIỂN THỊ message ẩn friend kèm tên user thao tác\n"
       "- Tên user hiển thị đúng theo tài khoản đã thao tác (chính hoặc staff)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r116-r119. ⚠ NGƯỢC với r39/r40 (chạy trực tiếp ≤200 thì chat 1:1 KHÔNG có "
            "message block/ẩn). Hai đường đi cho 2 kết quả khác nhau — spec không ghi. "
            "Gắn MT-14, cần Leader xác nhận đây là cố ý hay lỗi."),

    tc("Bulk action — trigger & profile gửi", "REG-SHARED-001", "Normal",
       "Regression — action schedule tạo TAY (màn アクションスケジュール実行) có hành vi khác",
       "- Đăng nhập Admin\n"
       "- Mở /basic/action-schedules, tạo tay 1 action schedule",
       "1. Tạo action schedule THỦ CÔNG ở màn アクションスケジュール実行 với action gửi text + template\n"
       "2. Chờ job chạy\n"
       "3. Mở màn chat 1:1 của friend nhận action, đọc khối trigger và profile\n"
       "4. Kiểm tra last message và trạng thái xác nhận của friend\n"
       "5. Lặp lại với action start/stop scenario, start/stop remind, block friend, ẩn friend",
       "action schedule tạo tay (KHÔNG phải từ màn friendlist)",
       "- Trigger ở chat 1:1 hiển thị trigger của ACTION SCHEDULE, không phải「手動操作」\n"
       "- Profile gửi LUÔN là profile default (không lấy theo màn chat 1:1)\n"
       "- KHÔNG update last message\n"
       "- KHÔNG tự động xác nhận message\n"
       "- Action block friend / ẩn friend: KHÔNG tạo message trigger ở chat 1:1",
       env="PRODUCTION",
       note="Nguồn: r134-r139. Đây là nhóm ĐỐI CHỨNG: 2 nguồn cùng dùng bảng action_schedules "
            "nhưng hành vi khác nhau — fix ở friendlist làm hỏng nhánh này là hồi quy. Chi tiết "
            "màn アクションスケジュール実行 thuộc FA-016, gom riêng."),
]
