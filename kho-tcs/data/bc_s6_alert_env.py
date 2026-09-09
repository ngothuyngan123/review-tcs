# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 27-31: 配信数上限アラート (#36436), Broadcast cũ &
tương thích, Phân quyền & môi trường.

⚠️ Toàn bộ nhóm 配信数上限アラート phụ thuộc MT-20: feature này KHÔNG có trong
spec-features/admin/message-send-all/ (spec chốt 2026-03-26, ticket #36436 sau đó).
Nếu chưa release thì các TC nhóm này chưa giao được cho member.
"""
from _common import tc

AL = ("- Đăng nhập Admin, đang ở màn SCR-BC-04 (/basic/add-broadcast-v2?broadcast_id=XXX)\n"
      "- Broadcast đã cấu hình đủ: tiêu đề, tin nhắn, đối tượng nhận")
MT20 = "⚠️ Phụ thuộc MT-20 — feature #36436 chưa có trong spec-features. "

S6 = [
    # ═══════════ 27. 配信数上限アラート — trigger & modal ═══════════
    tc("配信数上限アラート — trigger & modal", "FUNC-001", "Normal",
       "Cả 2 dịch vụ đều trong giới hạn — KHÔNG hiện modal, đăng ký thẳng",
       AL + "\n- LINE OA còn quota đủ cho lượt gửi này\n- エルメ còn quota đủ cho lượt gửi này",
       "1. Cấu hình broadcast với số đối tượng nhỏ hơn quota còn lại của cả 2 dịch vụ\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Quan sát màn hình",
       "配信対象 nhỏ hơn 配信可能数 của cả LINE OA và エルメ",
       "- KHÔNG hiện modal「配信数上限アラート」\n"
       "- Broadcast được đăng ký thẳng, chuyển vào tab tương ứng với kiểu gửi\n"
       "- Không có bước xác nhận thừa",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r2 (TC-BAL-001) + tab「UI Tests 36436」r6."),

    tc("配信数上限アラート — trigger & modal", "MSG-005", "Normal",
       "Chỉ LINE OA vượt giới hạn — hiện modal, chỉ card LINE ở trạng thái 超過",
       AL + "\n- LINE OA đã dùng gần hết quota tháng\n- エルメ còn trong giới hạn",
       "1. Cấu hình broadcast có số đối tượng làm LINE OA vượt quota\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Quan sát modal hiện ra: card LINE và card エルメ",
       "LINE OA: 配信済み=4,200 / 月間上限=5,000, 配信対象 làm vượt · エルメ 上限内",
       "- Hiện modal「配信数上限アラート」\n"
       "- Card LINE có badge「● {N}通 超過」màu đỏ, nền highlight vàng nhạt\n"
       "- Card エルメ có badge「上限内」màu xám, nền trắng\n"
       "- Câu mô tả là câu dành cho trường hợp 1 dịch vụ vượt, nêu đúng tên dịch vụ và số N",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r3, r13-r15, r17-r19, r28 (TC-BAL-002, 012-014, "
            "016-018, 027) + tab「UI Tests 36436」r3-r4."),

    tc("配信数上限アラート — trigger & modal", "MSG-005", "Normal",
       "Chỉ エルメ vượt giới hạn — hiện modal, chỉ card エルメ ở trạng thái 超過",
       AL + "\n- エルメ gói Free đã dùng gần hết 1,000 tin/tháng\n- LINE OA còn trong giới hạn",
       "1. Cấu hình broadcast có số đối tượng làm エルメ vượt quota\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Quan sát 2 card và khối upgrade",
       "エルメ フリープラン: gần hết 1,000 tin · LINE OA 上限内",
       "- Hiện modal, card エルメ có badge 超過 màu đỏ, card LINE có badge「上限内」\n"
       "- Card エルメ フリープラン hiển thị thanh usage đủ 3 đoạn màu\n"
       "- Dòng LINE trong khối upgrade KHÔNG hiển thị (vì LINE không vượt)",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r4, r16, r20, r24 (TC-BAL-003, 015, 019, 023) + "
            "tab「UI Tests 36436」r5, r14."),

    tc("配信数上限アラート — trigger & modal", "MSG-005", "Normal",
       "Cả 2 dịch vụ đều vượt — modal hiển thị đủ 2 card 超過 và câu mô tả riêng",
       AL + "\n- Cả LINE OA và エルメ đều sắp hết quota",
       "1. Cấu hình broadcast có số đối tượng làm cả 2 dịch vụ vượt\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Đọc từng phần của modal: 2 card, badge, câu mô tả, khối upgrade",
       "LINE OA: 配信済み=4,000 / 上限=5,000 · エルメ フリープラン gần hết · 配信対象 làm cả 2 vượt",
       "- Cả 2 card đều có badge「● {N}通 超過」với số N riêng của từng dịch vụ\n"
       "- Cả 2 card đều có nền highlight vàng nhạt\n"
       "- Câu mô tả là câu dành cho trường hợp CẢ HAI vượt (khác câu 1 dịch vụ vượt)\n"
       "- Khối upgrade hiển thị cả dòng LINE và dòng エルメ",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r5, r12, r22-r25, r27 (TC-BAL-004, 011, 021-024, 026) "
            "+ tab「UI Tests 36436」r2, r16, r23."),

    tc("配信数上限アラート — trigger & modal", "PAY-LIMIT-001", "Normal",
       "エルメ gói trả phí không giới hạn — card rút gọn, ẩn thanh usage",
       AL + "\n- Bot đang ở gói エルメ 有料プラン (không giới hạn)\n- LINE OA vượt quota",
       "1. Cấu hình broadcast làm LINE OA vượt quota\n"
       "2. Bấm lưu để hiện modal\n"
       "3. Quan sát card エルメ",
       "エルメ 有料プラン (無制限) · LINE OA vượt",
       "- Card エルメ hiển thị ở dạng RÚT GỌN\n"
       "- KHÔNG hiển thị thanh usage (vì không có giới hạn để đo)\n"
       "- KHÔNG hiển thị badge 超過 cho エルメ",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r22 (TC-BAL-021) + tab「UI Tests 36436」r18."),

    tc("配信数上限アラート — trigger & modal", "MSG-005", "Boundary",
       "Ranh giới quota — bằng đúng giới hạn, vượt 1 tin, thiếu 1 tin",
       AL + "\n- Biết chính xác 配信可能数 còn lại của エルメ",
       "1. Cấu hình broadcast có 今回の配信予定数 = 配信可能数 → bấm lưu → ghi kết quả\n"
       "2. Cấu hình 今回の配信予定数 = 配信可能数 + 1 → bấm lưu → ghi kết quả\n"
       "3. Cấu hình 今回の配信予定数 = 配信可能数 − 1 → bấm lưu → ghi kết quả",
       "3 mốc: bằng đúng giới hạn · vượt đúng 1 tin · thiếu đúng 1 tin",
       "- Bằng đúng giới hạn: KHÔNG hiện modal\n"
       "- Vượt đúng 1 tin: HIỆN modal, badge ghi「● 1通 超過」\n"
       "- Thiếu đúng 1 tin: KHÔNG hiện modal",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r6-r8 (TC-BAL-005 → 007). 3 mốc có 3 kết quả KHÁC "
            "NHAU nhưng là chuỗi đo cùng 1 ranh giới — giữ chung 1 TC theo dạng bảng ranh giới."),

    tc("配信数上限アラート — trigger & modal", "FUNC-001", "Normal",
       "Modal xuất hiện cho cả luồng gửi ngay và luồng đặt lịch",
       AL + "\n- Quota ở trạng thái sẽ vượt",
       "1. Cấu hình broadcast「メッセージ登録後すぐに配信」→ bấm lưu → ghi kết quả\n"
       "2. Cấu hình broadcast「配信予約」thời gian tương lai → bấm lưu → ghi kết quả",
       "2 kiểu gửi: gửi ngay · đặt lịch",
       "- Cả 2 luồng đều hiện modal「配信数上限アラート」\n"
       "- Nội dung modal giống nhau",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r9-r10 (TC-BAL-008, 009)."),

    tc("配信数上限アラート — trigger & modal", "DATA-COUNT-001", "Normal",
       "Số liệu trong modal khớp công thức và khớp header màn danh sách",
       AL + "\n- Ghi lại số ở header màn list trước khi thao tác",
       "1. Ghi số ở header: L Message x/y và LINE公式アカウント a/b\n"
       "2. Trigger modal\n"
       "3. Tính tay: 配信可能数 = 月間上限 − 配信済み\n"
       "4. Tính tay: 超過 = max(0, 今回の配信予定数 − 配信可能数)\n"
       "5. Tính tay: 今回の配信(上限内) = min(配信可能数, 今回の配信予定数)\n"
       "6. So từng số trong modal với kết quả tính tay và với header",
       "Ví dụ LINE: 月間上限 5,000 · 配信済み 4,000 · 今回の配信予定数 1,500 "
       "→ 配信可能数 1,000 · 上限内 1,000 · 超過 500",
       "- Mọi số trong modal khớp đúng kết quả tính tay\n"
       "- Số 配信済み và 月間上限 khớp với header màn danh sách (cùng nguồn dữ liệu)\n"
       "- Số ≥ 1,000 đều có dấu phẩy phân cách hàng nghìn",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r26, r29-r32, r36 (TC-BAL-025, 028-031, 035) + "
            "tab「UI Tests 36436」r20-r22.",
       group="Data"),

    tc("配信数上限アラート — trigger & modal", "DATA-COUNT-001", "Normal",
       "配信対象 hiển thị trong modal khớp số người nhận thực tế theo filter",
       AL + "\n- Broadcast có filter tag T, tag T gắn cho 6 friend",
       "1. Đặt filter tag T, bấm「再計算」ghi lại 配信数 = 6\n"
       "2. Trigger modal\n"
       "3. Đọc 配信対象 trong modal\n"
       "4. Đăng ký gửi, chờ job gửi xong, đọc 配信数 ở tab「配信履歴」",
       "Tag T = 6 friend",
       "- 配信対象 trong modal = 6, khớp với 配信数 ở màn edit\n"
       "- Sau khi gửi, số thực gửi khớp với số hiển thị (trừ phần bị cắt do vượt quota)",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r38 (TC-BAL-037). RULE-08: quota + job → PRODUCTION.",
       group="Data"),

    tc("配信数上限アラート — trigger & modal", "FUNC-DATE-001", "Boundary",
       "Chu kỳ reset 配信済み của エルメ — cuối tháng so với đầu tháng",
       "- Bot ở gói エルメ フリープラン, đã dùng gần hết 1,000 tin trong tháng",
       "1. Vào ngày cuối tháng: ghi lại 配信済み và trigger modal, ghi số liệu\n"
       "2. Sang ngày đầu tháng kế tiếp: ghi lại 配信済み và trigger modal, ghi số liệu\n"
       "3. So sánh 2 lần đo",
       "Đo ở ngày cuối tháng và ngày 1 tháng sau (dương lịch)",
       "- Cuối tháng: 配信済み giữ nguyên số đã dùng\n"
       "- Đầu tháng mới: 配信済み reset về 0, 配信可能数 quay lại 1,000\n"
       "- Modal không còn hiện nếu đối tượng nhận nằm trong quota mới",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r35 (TC-BAL-034). ⚠️ Chu kỳ reset là dương lịch hay "
            "theo ngày ký hợp đồng — spec KHÔNG ghi rõ, cần Leader xác nhận. RULE-08: bill/quota → PRODUCTION.",
       group="Data"),

    tc("配信数上限アラート — trigger & modal", "UI-003", "Abnormal",
       "Lỗi mạng khi kiểm tra quota — hiện lỗi rõ ràng, KHÔNG đăng ký nhầm",
       AL,
       "1. Dùng DevTools chặn/giả lập lỗi 500 cho request kiểm tra quota\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Quan sát thông báo và trạng thái broadcast\n"
       "4. Về màn list kiểm tra broadcast có bị đăng ký không",
       "Giả lập lỗi 500 hoặc mất mạng ở bước kiểm tra quota",
       "- Hiện thông báo lỗi rõ ràng cho người dùng\n"
       "- KHÔNG đăng ký broadcast (không nhảy sang tab 配信予約/配信履歴)\n"
       "- Cấu hình broadcast phía sau giữ nguyên, người dùng thử lại được",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r88 (TC-BAL-087) + tab「UI Tests 36436」r15."),

    # ═══════════ 28. 配信数上限アラート — nút thao tác ═══════════
    tc("配信数上限アラート — nút thao tác", "FUNC-001", "Normal",
       "Nút「×」đóng modal, KHÔNG đăng ký, cấu hình phía sau giữ nguyên",
       AL + "\n- Modal「配信数上限アラート」đang hiển thị",
       "1. Ghi lại cấu hình broadcast trước khi trigger modal\n"
       "2. Bấm nút「×」\n"
       "3. Quan sát màn hình phía sau modal\n"
       "4. Về màn list kiểm tra broadcast có bị đăng ký không",
       "Modal đang hiển thị ở bất kỳ variant nào",
       "- Modal đóng, quay về màn SCR-BC-04\n"
       "- Tiêu đề, tin nhắn, filter, người gửi giữ nguyên như trước\n"
       "- Broadcast KHÔNG chuyển sang tab「配信予約」hay「配信履歴」",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r39, r42 (TC-BAL-038, 041) + tab「UI Tests 36436」r7."),

    tc("配信数上限アラート — nút thao tác", "UI-001", "Normal",
       "Đóng modal bằng phím Esc và click ra ngoài — hành vi nhất quán với nút「×」",
       AL + "\n- Modal đang hiển thị",
       "1. Nhấn phím Esc → ghi lại hành vi\n"
       "2. Trigger lại modal, click vào vùng nền tối bên ngoài modal → ghi lại hành vi\n"
       "3. Mỗi lần đều kiểm tra broadcast có bị đăng ký không",
       "Phím Esc · click vùng overlay",
       "- Ghi rõ hành vi thực tế của từng cách\n"
       "- Nếu đóng được: phải giống hệt nút「×」— không đăng ký, giữ cấu hình\n"
       "- Nếu không đóng được: modal vẫn nguyên, không có lỗi",
       spec="Đã hỏi leader",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r40-r41 (TC-BAL-039, 040) — TC gốc ghi『kiểm tra hành "
            "vi』chứ không chốt kết quả. Cần Leader chốt Esc/overlay có được phép đóng modal không."),

    tc("配信数上限アラート — nút thao tác", "FUNC-001", "Normal",
       "Nút「配信対象を見直す」— quay về đúng khối 配信先絞込み, giữ nguyên cấu hình khác",
       AL + "\n- Modal đang hiển thị, broadcast đã cấu hình đầy đủ",
       "1. Ghi lại tiêu đề, tin nhắn, người gửi trước khi trigger modal\n"
       "2. Bấm「配信対象を見直す」\n"
       "3. Quan sát vị trí màn hình cuộn tới\n"
       "4. Kiểm tra các khối cấu hình khác",
       "Modal đang hiển thị",
       "- Modal đóng, màn hình cuộn tới đúng khối「配信先絞込み」\n"
       "- Tiêu đề, tin nhắn, người gửi giữ nguyên\n"
       "- Broadcast chưa được đăng ký",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r43 (TC-BAL-042) + tab「UI Tests 36436」r8."),

    tc("配信数上限アラート — nút thao tác", "FUNC-001", "Normal",
       "Sau 見直す, đổi filter rồi bấm 再計算 → đăng ký lại KHÔNG còn hiện modal",
       AL + "\n- Modal đang hiển thị do đối tượng quá lớn",
       "1. Bấm「配信対象を見直す」\n"
       "2. Thu hẹp filter để số đối tượng nhỏ hơn quota còn lại\n"
       "3. Bấm「再計算」— xác nhận 配信数 giảm đúng\n"
       "4. Bấm「配信内容を確認して送信に進む」lần nữa",
       "Filter thu hẹp từ 1,500 người xuống 500 người, quota còn 1,000",
       "- Sau 再計算: 配信数 cập nhật thành 500\n"
       "- Bấm lưu lần 2: KHÔNG hiện modal nữa\n"
       "- Broadcast được đăng ký thẳng",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r44-r45 (TC-BAL-043, 044)."),

    tc("配信数上限アラート — nút thao tác", "FUNC-DRAFT-001", "Normal",
       "Nút「下書き保存する」— lưu nháp, KHÔNG gửi, KHÔNG trừ quota",
       AL + "\n- Modal đang hiển thị do エルメ vượt quota\n- Đã ghi lại số 配信済み hiện tại",
       "1. Ghi lại 配信済み của エルメ ở header\n"
       "2. Bấm「下書き保存する」trên modal\n"
       "3. Về màn list kiểm tra tab「下書き」\n"
       "4. Reload trang, đọc lại 配信済み ở header\n"
       "5. Kiểm tra app LINE của friend trong đối tượng nhận",
       "エルメ フリープラン đang vượt quota",
       "- Broadcast xuất hiện ở tab「下書き」với status = 'draft'\n"
       "- 配信済み KHÔNG tăng (bảng bots: free_send_count không đổi)\n"
       "- KHÔNG friend nào nhận được tin nhắn",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r46, r65 (TC-BAL-045, 064) + tab「API Tests 36436」"
            "r12, r18, r23. RULE-08: bill/quota → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — nút thao tác", "FUNC-001", "Normal",
       "Nút「このまま登録する」khi gửi ngay — đăng ký ngay, KHÔNG hỏi xác nhận thêm",
       AL + "\n- Modal đang hiển thị, broadcast cấu hình gửi ngay",
       "1. Bấm「このまま登録する」\n"
       "2. Quan sát có hộp thoại xác nhận thứ hai không\n"
       "3. Về màn list kiểm tra broadcast nằm ở tab nào\n"
       "4. Đọc status trong DB",
       "Broadcast cấu hình「メッセージ登録後すぐに配信」",
       "- KHÔNG hiện thêm hộp thoại xác nhận nào\n"
       "- Broadcast được đăng ký với status = 'wait_to_send'\n"
       "- Sau khi job chạy, broadcast vào tab「配信履歴」",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r48 (TC-BAL-047) + tab「UI Tests 36436」r10 + "
            "tab「API Tests 36436」r11. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — nút thao tác", "FUNC-001", "Normal",
       "Nút「このまま登録する」khi đặt lịch — broadcast vào tab 配信予約",
       AL + "\n- Modal đang hiển thị, broadcast cấu hình đặt lịch tương lai",
       "1. Bấm「このまま登録する」\n"
       "2. Về màn list kiểm tra tab「配信予約」\n"
       "3. Đọc thời gian gửi hiển thị",
       "Broadcast đặt lịch mai 10:00",
       "- Broadcast nằm ở tab「配信予約」với đúng thời gian mai 10:00\n"
       "- status = 'wait_to_send'",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r60 (TC-BAL-059) + tab「UI Tests 36436」r11."),

    tc("配信数上限アラート — nút thao tác", "CONC-001", "Abnormal",
       "Double click「このまま登録する」— chỉ đăng ký 1 broadcast",
       AL + "\n- Modal đang hiển thị",
       "1. Double click nhanh vào「このまま登録する」\n"
       "2. Về màn list đếm số bản ghi trùng tên\n"
       "3. Mở DevTools → Network đếm số request đăng ký",
       "Double click trong < 1 giây",
       "- Chỉ 1 request được gửi (hoặc request thứ 2 bị chặn)\n"
       "- Chỉ 1 broadcast được đăng ký, không nhân đôi",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r49 (TC-BAL-048).",
       group="API"),

    tc("配信数上限アラート — nút thao tác", "CONC-003", "Abnormal",
       "Mở 2 tab cùng broadcast, cả 2 cùng bấm「このまま登録する」",
       "- Cùng 1 broadcast mở trên 2 tab trình duyệt\n- Cả 2 tab đều đang hiện modal",
       "1. Trigger modal ở cả 2 tab\n"
       "2. Bấm「このまま登録する」ở tab 1, ngay sau đó bấm ở tab 2\n"
       "3. Về màn list đếm số bản ghi\n"
       "4. Kiểm tra app LINE của friend xem có nhận trùng không",
       "2 tab cùng broadcast_id, bấm gần đồng thời",
       "- Chỉ 1 broadcast được đăng ký (không sinh 2 bản ghi)\n"
       "- Friend nhận tin đúng 1 lần, không bị gửi trùng",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r50 (TC-BAL-049). RULE-08: race condition → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — nút thao tác", "STATE-001", "Abnormal",
       "Ngắt kết nối ngay sau khi bấm nút — trạng thái broadcast nhất quán",
       AL + "\n- Modal đang hiển thị",
       "1. Bấm「このまま登録する」rồi ngắt mạng/đóng tab ngay trước khi có phản hồi\n"
       "2. Kết nối lại, vào màn list kiểm tra broadcast ở tab nào và status gì\n"
       "3. Lặp lại quy trình với nút「下書き保存する」",
       "Ngắt mạng ngay sau khi bấm, với cả 2 nút",
       "- Broadcast ở đúng 1 trong 2 trạng thái rõ ràng: đã đăng ký HOẶC chưa đăng ký\n"
       "- KHÔNG rơi vào trạng thái nửa vời (VD status wait_to_send nhưng thiếu filter/template)\n"
       "- Nếu đã đăng ký thì job vẫn gửi được bình thường",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r54-r55 (TC-BAL-053, 054). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — nút thao tác", "UI-003", "Normal",
       "Trong lúc đang xử lý — toàn bộ nút của modal bị disable, có spinner",
       AL + "\n- Modal đang hiển thị",
       "1. Dùng DevTools làm chậm request đăng ký (throttle mạng)\n"
       "2. Bấm「このまま登録する」\n"
       "3. Trong lúc đang chờ phản hồi, thử bấm các nút khác trên modal\n"
       "4. Quan sát trạng thái nút và spinner",
       "Throttle mạng để request kéo dài ≥3 giây",
       "- Cả 3 nút footer và 2 nút upgrade đều bị disable\n"
       "- Có spinner hoặc chỉ báo đang xử lý\n"
       "- Bấm nút khác không tạo thêm request",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r87 (TC-BAL-086) + tab「UI Tests 36436」r24."),

    tc("配信数上限アラート — nút thao tác", "UI-003", "Abnormal",
       "Sau khi đăng ký lỗi — nút modal enable trở lại, modal vẫn mở",
       AL + "\n- Modal đang hiển thị",
       "1. Dùng DevTools giả lập lỗi 500 cho request đăng ký\n"
       "2. Bấm「このまま登録する」\n"
       "3. Sau khi lỗi trả về, quan sát trạng thái modal và các nút",
       "Giả lập lỗi 500 ở request đăng ký",
       "- Modal VẪN mở (không đóng mất cấu hình)\n"
       "- Các nút quay lại trạng thái enable, bấm lại được\n"
       "- Có thông báo lỗi rõ ràng",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r88 + tab「UI Tests 36436」r25."),

    tc("配信数上限アラート — nút thao tác", "UI-001", "Normal",
       "Nút upgrade — chỉ hiện đúng dịch vụ vượt, mở tab mới",
       AL,
       "1. Trigger modal ở trạng thái chỉ LINE vượt → kiểm tra 2 nút upgrade\n"
       "2. Trigger modal ở trạng thái chỉ エルメ vượt → kiểm tra 2 nút upgrade\n"
       "3. Trigger modal ở trạng thái cả 2 vượt → kiểm tra 2 nút upgrade\n"
       "4. Bấm từng nút, quan sát tab mở ra",
       "3 trạng thái: chỉ LINE vượt · chỉ エルメ vượt · cả 2 vượt",
       "- Nút「LINE Official Account Manager で変更」chỉ hiện khi LINE vượt\n"
       "- Nút「プラン詳細を見る」chỉ hiện khi エルメ vượt\n"
       "- Cả 2 vượt: hiện cả 2 nút, thao tác độc lập\n"
       "- Bấm nút: mở tab MỚI, tab hiện tại vẫn giữ modal",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r51-r53 (TC-BAL-050 → 052) + tab「UI Tests 36436」"
            "r12-r13, r29."),

    tc("配信数上限アラート — nút thao tác", "UI-004", "Normal",
       "Thứ tự Tab/focus trong modal đi đúng thứ tự các nút",
       AL + "\n- Modal đang hiển thị ở trạng thái cả 2 dịch vụ vượt",
       "1. Nhấn phím Tab liên tục từ khi modal mở\n"
       "2. Ghi lại thứ tự phần tử được focus",
       "Modal variant cả 2 dịch vụ vượt (nhiều nút nhất)",
       "- Thứ tự focus: nút「×」→ các nút upgrade → 3 nút footer\n"
       "- Focus không thoát ra ngoài modal khi Tab tới cuối\n"
       "- Nhấn Enter trên nút đang focus thực thi đúng nút đó",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r91 (TC-BAL-090)."),

    # ═══════════ 29. 配信数上限アラート — quota & job cắt vượt ═══════════
    tc("配信数上限アラート — quota & job cắt vượt", "MSG-005", "Normal",
       "Đăng ký vượt quota — job gửi phần trong giới hạn, phần vượt bị bỏ qua và ghi log",
       "- Bot ở gói エルメ フリープラン, 配信可能数 còn 100 tin\n"
       "- Broadcast có 150 đối tượng nhận, đã đăng ký qua「このまま登録する」",
       "1. Chờ job gửi xong\n"
       "2. Đếm số friend thực nhận được tin (lấy mẫu hoặc đọc 配信数)\n"
       "3. Đọc bảng message_error tìm bản ghi có code liên quan giới hạn\n"
       "4. Đọc 配信済み ở header sau khi gửi",
       "配信可能数 = 100 · 配信対象 = 150",
       "- Đúng 100 friend nhận được tin\n"
       "- 50 friend còn lại KHÔNG nhận được\n"
       "- Bảng message_error có bản ghi với code REACH_LIMIT_FREE_PLAN cho phần vượt\n"
       "- 配信済み tăng đúng 100, không tăng 150",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r57, r67-r68 (TC-BAL-056, 066, 067) + "
            "job-spec.md:559-560. RULE-08: bill/quota + job → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "MSG-005", "Normal",
       "Vượt quota phía LINE OA — job bỏ qua phần vượt và ghi code REACH_LIMIT_LINE",
       "- LINE OA còn quota 100 tin\n- Broadcast có 150 đối tượng nhận, đã đăng ký",
       "1. Chờ job gửi xong\n"
       "2. Đếm số friend thực nhận\n"
       "3. Đọc bảng message_error",
       "LINE OA 配信可能数 = 100 · 配信対象 = 150",
       "- Đúng 100 friend nhận được tin\n"
       "- Bảng message_error có bản ghi code REACH_LIMIT_LINE cho 50 trường hợp còn lại\n"
       "- Job KHÔNG retry cho lỗi này",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r69 (TC-BAL-068) + job-spec.md:414, 560. "
            "RULE-08: bill/quota + job → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "CONC-001", "Boundary",
       "Quota thay đổi giữa lúc hiện modal và lúc job chạy — cắt phần vượt tại thời điểm job",
       "- Bot gói Free, 配信可能数 còn 200 tin\n- Broadcast 150 đối tượng, đặt lịch sau 20 phút",
       "1. Đăng ký broadcast khi quota còn 200 (không hiện modal vì 150 < 200)\n"
       "2. Trước giờ gửi, dùng tính năng khác gửi 100 tin để quota còn 100\n"
       "3. Chờ job gửi broadcast\n"
       "4. Đếm số friend thực nhận và đọc message_error",
       "Lúc đăng ký: quota 200, đối tượng 150 · lúc job chạy: quota còn 100",
       "- Job chỉ gửi 100 tin (cắt theo quota TẠI THỜI ĐIỂM JOB CHẠY, không theo lúc đăng ký)\n"
       "- 50 trường hợp còn lại ghi message_error code giới hạn\n"
       "- Việc cắt diễn ra theo từng người, tuần tự theo danh sách đã lọc",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r70, r72 (TC-BAL-069, 071). "
            "RULE-08: race condition + bill/quota → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "SEC-001", "Abnormal",
       "Gọi thẳng API đăng ký bỏ qua modal — vẫn bị job cắt phần vượt quota",
       "- Session Admin hợp lệ\n- Broadcast hợp lệ có 150 đối tượng, quota còn 100",
       "1. Dùng DevTools/công cụ API gọi thẳng endpoint đăng ký broadcast với status wait_to_send, "
       "KHÔNG gọi endpoint kiểm tra quota trước\n"
       "2. Kiểm tra broadcast có được đăng ký không\n"
       "3. Chờ job gửi, đếm số friend thực nhận",
       "配信可能数 = 100 · 配信対象 = 150 · bỏ qua bước kiểm tra quota",
       "- Broadcast đăng ký được (API đăng ký không phụ thuộc bước kiểm tra quota)\n"
       "- NHƯNG job vẫn chỉ gửi 100 tin, phần vượt bị cắt\n"
       "- Không có cách nào vượt quota bằng cách bỏ qua modal",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r71 (TC-BAL-070) + tab「API Tests 36436」r16. "
            "RULE-08: bill/quota + job → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "DATA-COUNT-001", "Boundary",
       "Đăng ký 2 broadcast liên tiếp cùng tháng, mỗi lần đều vượt — quota tích lũy đúng",
       "- Bot gói Free, đầu tháng 配信済み = 0, quota 1,000 tin",
       "1. Đăng ký và gửi broadcast 1 cho 600 friend → chờ gửi xong, ghi 配信済み\n"
       "2. Đăng ký broadcast 2 cho 600 friend → ghi lại modal có hiện không và số 配信可能数\n"
       "3. Chờ gửi xong, đọc số friend thực nhận và 配信済み cuối",
       "Quota 1,000 · broadcast 1: 600 người · broadcast 2: 600 người",
       "- Sau broadcast 1: 配信済み = 600, không hiện modal (600 < 1,000)\n"
       "- Broadcast 2: HIỆN modal, 配信可能数 = 400, 超過 = 200\n"
       "- Broadcast 2 chỉ gửi được 400 tin\n"
       "- 配信済み cuối = 1,000, không vượt quá",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r63 (TC-BAL-062). RULE-08: bill/quota → PRODUCTION.",
       group="Data"),

    tc("配信数上限アラート — quota & job cắt vượt", "DATA-COUNT-001", "Boundary",
       "Gửi lại broadcast lần 2 cùng cấu hình — quota trừ đúng, không đếm trùng",
       "- Broadcast đã gửi xong cho 100 friend, 配信済み đã tăng 100",
       "1. Ghi lại 配信済み sau lần gửi 1\n"
       "2. Copy broadcast đó và gửi lại cùng cấu hình\n"
       "3. Chờ gửi xong, đọc 配信済み\n"
       "4. Kiểm tra friend có nhận đủ 2 lần không",
       "Broadcast 100 friend, gửi 2 lần",
       "- 配信済み tăng thêm đúng 100 (tổng 200), không double-count\n"
       "- Friend nhận đủ 2 lần tin nhắn (đây là 2 lượt gửi riêng biệt)",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r74 (TC-BAL-073). RULE-08: bill/quota → PRODUCTION.",
       group="Data"),

    tc("配信数上限アラート — quota & job cắt vượt", "STATE-DEP-001", "Boundary",
       "Nâng cấp gói LINE OA sau khi đăng ký, trước khi job chạy — quota tính theo gói mới",
       "- Bot ở gói LINE OA nhỏ, broadcast đã đăng ký vượt quota, đặt lịch sau 30 phút",
       "1. Đăng ký broadcast vượt quota gói hiện tại\n"
       "2. Trước giờ gửi, nâng cấp gói LINE OA lên mức cao hơn\n"
       "3. Chờ job gửi\n"
       "4. Đếm số friend thực nhận",
       "Gói cũ quota 200 · broadcast 500 người · nâng cấp lên gói quota 5,000",
       "- Job gửi đủ 500 người (tính theo quota gói MỚI tại thời điểm job chạy)\n"
       "- Không bị cắt theo quota gói cũ",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r75 (TC-BAL-074). ⚠️ Corpus không ghi kết quả đã "
            "verify; cần Leader xác nhận hành vi mong muốn. RULE-08: bill/quota + job → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "MSG-003", "Normal",
       "Đối tượng nhận có người đã block — không làm hỏng lượt gửi và số đếm quota",
       "- Broadcast có 20 đối tượng nhận, trong đó 5 người đã block LOA",
       "1. Chờ job gửi xong\n"
       "2. Đếm số friend thực nhận\n"
       "3. Đọc 配信数 ở lịch sử và 配信済み ở header\n"
       "4. Đọc bảng message_error",
       "20 đối tượng, 5 người is_blocked = 1",
       "- 15 friend chưa block nhận được tin\n"
       "- Job không dừng giữa chừng vì gặp người block\n"
       "- 配信済み tăng theo số thực gửi thành công, không tính 5 người block",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r61 (TC-BAL-060). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "OUT-TRUTH-001", "Normal",
       "Thông báo sau khi bấm nút khớp đúng trạng thái thật của broadcast",
       AL + "\n- Modal đang hiển thị",
       "1. Bấm「このまま登録する」→ đọc thông báo → về màn list xác nhận trạng thái thật\n"
       "2. Trigger lại modal, bấm「下書き保存する」→ đọc thông báo → xác nhận trạng thái thật",
       "2 nút: このまま登録する · 下書き保存する",
       "- Thông báo sau「このまま登録する」nói broadcast đã đăng ký — và thực tế broadcast ở "
       "tab「配信予約」/「配信履歴」\n"
       "- Thông báo sau「下書き保存する」nói đã lưu nháp — và thực tế broadcast ở tab「下書き」\n"
       "- KHÔNG có trường hợp báo thành công nhưng broadcast không tồn tại",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r64-r65 (TC-BAL-063, 064)."),

    tc("配信数上限アラート — quota & job cắt vượt", "REG-SHARED-001", "Normal",
       "Hồi quy — luồng broadcast KHÔNG vượt quota vẫn hoạt động y như trước",
       "- Bot có quota dư dả\n- Đã có sẵn broadcast wait_to_send tạo TRƯỚC khi triển khai tính năng alert",
       "1. Tạo broadcast mới không vượt quota, đi hết luồng: bước 1 → tin nhắn → đăng ký → job gửi\n"
       "2. Kiểm tra các validate cũ vẫn chạy: thiếu tên · thiếu ngày · sửa trong 5 phút\n"
       "3. Kiểm tra broadcast wait_to_send cũ có được job gửi bình thường không\n"
       "4. Kiểm tra tab「下書き」hiển thị đủ cả nháp tạo qua modal mới lẫn nháp cũ\n"
       "5. Kiểm tra header quota và nút「再計算」",
       "Broadcast mới không vượt quota · broadcast cũ tạo trước deploy",
       "- Toàn bộ luồng cũ chạy đúng, không bị chặn bởi tính năng alert\n"
       "- 3 validate cũ vẫn hoạt động và hiện đúng thông báo\n"
       "- Broadcast cũ vẫn được job gửi bình thường sau deploy\n"
       "- Tab「下書き」hiển thị đủ cả 2 loại nháp\n"
       "- Header quota và nút「再計算」không đổi hành vi",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r94-r100 (TC-BAL-093 → 099) + tab「API Tests 36436」"
            "r28-r30. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "REG-SHARED-001", "Normal",
       "Hồi quy — job gửi step/scenario dùng chung hạ tầng KHÔNG bị ảnh hưởng",
       "- Có scenario đang chạy và có remind đang hoạt động\n- Đã triển khai tính năng alert",
       "1. Trigger 1 scenario cho friend, kiểm tra friend nhận đủ step message\n"
       "2. Trigger 1 remind, kiểm tra friend nhận tin nhắc\n"
       "3. So sánh hành vi với trước khi triển khai (nếu có bản ghi cũ)",
       "1 scenario nhiều step · 1 remind",
       "- Scenario gửi đủ step, đúng thời gian, không bị chặn bởi logic quota mới\n"
       "- Remind gửi bình thường\n"
       "- Không xuất hiện modal alert ở các luồng này",
       env="PRODUCTION",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r100 (TC-BAL-099). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("配信数上限アラート — quota & job cắt vượt", "COMPAT-BROWSER-001", "Normal",
       "Modal hiển thị đúng trên Chrome (Windows) và Safari (Mac), ở 1366×768 và 1280px",
       "- Chuẩn bị Windows + Chrome và Mac + Safari\n- Quota ở trạng thái sẽ vượt",
       "1. Trên Windows/Chrome ở 1366×768: trigger modal, kiểm tra bố cục và các nút\n"
       "2. Thu cửa sổ còn 1280px: kiểm tra cuộn dọc trong modal\n"
       "3. Lặp lại toàn bộ trên Mac/Safari\n"
       "4. Kiểm tra câu mô tả dài nhất (variant cả 2 dịch vụ vượt) có vỡ layout không",
       "2 trình duyệt × 2 kích thước · variant có câu mô tả dài nhất",
       "- Modal hiển thị đủ nội dung ở cả 4 tổ hợp\n"
       "- Ở 1280px: modal cuộn dọc được, không mất nút footer\n"
       "- Câu mô tả dài xuống dòng đúng, không tràn khỏi card\n"
       "- Hover trên các nút đổi màu và con trỏ thành hình bàn tay",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r84-r86, r89-r90 (TC-BAL-083 → 085, 088, 089) + "
            "tab「UI Tests 36436」r28, r30."),

    tc("配信数上限アラート — quota & job cắt vượt", "STATE-CLEAN-001", "Abnormal",
       "Đóng/mở modal nhiều lần — không để lại lớp phủ chồng nhau",
       AL,
       "1. Trigger modal rồi đóng bằng「×」, lặp lại 5 lần liên tiếp\n"
       "2. Sau lần cuối, kiểm tra màn hình có bị mờ/khóa thao tác không\n"
       "3. Dùng DevTools kiểm tra số phần tử overlay còn lại trong DOM",
       "Đóng/mở 5 lần liên tiếp",
       "- Sau khi đóng, màn hình thao tác bình thường, không bị lớp phủ khóa\n"
       "- Trong DOM không còn overlay thừa chồng lên nhau",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r93 (TC-BAL-092)."),

    tc("配信数上限アラート — quota & job cắt vượt", "FUNC-SEQ-001", "Boundary",
       "Chuỗi thao tác dài quanh modal — trạng thái nhất quán sau F5",
       AL,
       "1. Trigger modal → đóng bằng「×」→ đổi đối tượng nhận → trigger modal lại → "
       "「このまま登録する」→ F5 reload\n"
       "2. Kiểm tra broadcast ở tab nào, cấu hình có đúng lần đổi cuối không\n"
       "3. Chuỗi thứ hai:「配信対象を見直す」→ đổi filter →「再計算」→「このまま登録する」→ F5",
       "2 chuỗi thao tác liên tiếp",
       "- Sau F5, broadcast ở đúng tab tương ứng trạng thái đã đăng ký\n"
       "- Cấu hình lưu là lần đổi CUỐI CÙNG, không phải cấu hình trước đó\n"
       "- Không sinh bản ghi thừa",
       note=MT20 + "Nguồn: 03/tab「[AI] alert_limit」r58-r59 (TC-BAL-057, 058). Giữ chung 1 TC vì là "
            "chuỗi thao tác liên tiếp không tách rời (FUNC-SEQ)."),

    # ═══════════ 30. Broadcast cũ & tương thích ═══════════
    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ chưa gửi, CHƯA có tin nhắn — hiển thị đúng ở giao diện mới",
       "- Có broadcast tạo TRƯỚC đợt release giao diện mới (02/2024), chưa gửi, chưa có tin nhắn",
       "1. Mở màn list, tìm broadcast cũ đó\n"
       "2. Ghi lại tab chứa nó\n"
       "3. Thử bấm gửi thử ở bản ghi đó",
       "Broadcast legacy chưa gửi, template_ids rỗng",
       "- Hiển thị ở tab dành cho broadcast chưa gửi\n"
       "- Bấm gửi thử KHÔNG gửi gì (vì không có nội dung)\n"
       "- Không lỗi trang, không mất bản ghi",
       note="Nguồn: r777 + file 03/tab function r5. Corpus ghi rõ khác biệt: bản cũ tạo broadcast rồi mới "
            "tạo tin nhắn nên chưa có nút gửi thử; bản mới bắt buộc có tin nhắn nên hiện luôn phần gửi thử."),

    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ chưa gửi, ĐÃ có tin nhắn — hiển thị ở tab chờ gửi",
       "- Có broadcast legacy chưa gửi, đã có tin nhắn",
       "1. Mở màn list, tìm broadcast cũ đó\n"
       "2. Ghi lại tab chứa nó và các cột hiển thị",
       "Broadcast legacy có template_ids",
       "- Hiển thị ở tab broadcast chưa gửi\n"
       "- Các cột hiển thị đủ dữ liệu, không có ô lỗi",
       note="Nguồn: r778 + file 03/tab function r6."),

    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ kiểu gửi bằng nút bấm — ở giao diện mới phải vào edit nhập tiêu đề rồi lưu mới gửi",
       "- Có broadcast legacy dạng『gửi khi bấm nút』, chưa gửi",
       "1. Mở broadcast đó ở màn list\n"
       "2. Quan sát tab và cách gửi\n"
       "3. Vào màn edit, nhập tiêu đề rồi bấm lưu\n"
       "4. Kiểm tra broadcast có được gửi không\n"
       "5. Kiểm tra danh sách tin nhắn con, filter, người gửi và action rich menu",
       "Broadcast legacy kiểu click-to-send, chưa có tiêu đề",
       "- Hiển thị ở tab chờ gửi\n"
       "- Vào edit nhập tiêu đề rồi lưu là gửi ngay\n"
       "- Tin nhắn con, filter, người gửi giữ nguyên như dữ liệu cũ\n"
       "- Action rich menu (chọn và xóa) vẫn chạy đúng",
       env="PRODUCTION",
       note="Nguồn: r779-r784 + file 03/tab function r7. r783 ghi nhận『cần chạy recover』cho action rich "
            "menu. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ đặt lịch, KHÔNG có tiêu đề — đến giờ vẫn gửi bình thường",
       "- Có broadcast legacy đặt lịch tương lai, trường tiêu đề = NULL",
       "1. Xác nhận broadcast có send_day/send_time tương lai và name = NULL\n"
       "2. Chờ tới giờ gửi\n"
       "3. Kiểm tra app LINE của friend nhận\n"
       "4. Kiểm tra tin nhắn con, filter, người gửi, action rich menu",
       "Broadcast legacy: name = NULL, đặt lịch tương lai",
       "- Đến giờ, job gửi bình thường dù không có tiêu đề\n"
       "- Friend nhận đủ tin nhắn\n"
       "- Filter, người gửi, action rich menu đều đúng như dữ liệu cũ",
       env="PRODUCTION",
       note="Nguồn: r785-r790 + file 03/tab function r8 (『bản cũ: ko có trường title; bản mới: trường "
            "title null; đến giờ vẫn send bthg』). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ ĐÃ gửi — hiển thị ở tab lịch sử, mở xem được đầy đủ",
       "- Có broadcast legacy đã gửi xong",
       "1. Mở tab「配信履歴」, tìm broadcast cũ\n"
       "2. Thử mở màn edit/xem chi tiết\n"
       "3. Kiểm tra tin nhắn con, filter, người gửi, action rich menu\n"
       "4. Thử copy và preview",
       "Broadcast legacy đã gửi",
       "- Hiển thị ở tab「配信履歴」\n"
       "- Xem được đủ tin nhắn con, filter, người gửi\n"
       "- Copy và preview hoạt động bình thường",
       note="Nguồn: r791-r804 — r792 ghi『Not test — ko vào dc mh edit』. "
            "⚠️ MT-21: broadcast legacy đã gửi có mở được màn chi tiết không? Cần Leader xác nhận."),

    tc("Broadcast cũ & tương thích", "COMPAT-LEGACY-001", "Normal",
       "Broadcast cũ — quy tắc xóa theo trạng thái giống broadcast mới",
       "- Có broadcast legacy ở cả 3 trạng thái: chờ gửi, nháp, đã gửi",
       "1. Thử xóa broadcast legacy đang chờ gửi\n"
       "2. Thử xóa broadcast legacy ở nháp\n"
       "3. Thử xóa broadcast legacy đã gửi",
       "3 broadcast legacy ở 3 trạng thái",
       "- Chờ gửi: xóa thành công\n"
       "- Nháp: xóa thành công\n"
       "- Đã gửi: KHÔNG xóa được",
       note="Nguồn: r805-r807."),

    tc("Broadcast cũ & tương thích", "REG-SPEC-001", "Normal",
       "Chuỗi ký tự và URL trong tin nhắn không bị thêm khoảng trắng thừa",
       "- Đã triển khai fix SpecImprove #35253 (27/03/2026)",
       "1. Ở màn broadcast, tạo tin nhắn text chứa URL dài, KHÔNG gõ space trước URL → lưu\n"
       "2. Tạo tin có text rồi Enter rồi URL dài → lưu\n"
       "3. Tạo tin có 2 URL liên tiếp cách nhau bằng space và bằng Enter → lưu\n"
       "4. Sửa và lưu lại tin nhắn 3 lần liên tiếp\n"
       "5. Sau mỗi bước: xem preview, gửi thử cho friend, xem tin trên app LINE và chat 1:1",
       "URL dài không space trước · text+Enter+URL · URL_1[Space]URL_2 · URL_1[Enter]URL_2 · "
       "lưu lại 3 lần",
       "- Preview: URL hiển thị đúng như đã nhập, KHÔNG bị thêm space ở đầu\n"
       "- URL sau Enter bắt đầu ngay đầu dòng mới, không có khoảng trắng thừa\n"
       "- 2 URL liên tiếp giữ đúng dấu phân tách đã nhập\n"
       "- Sau 3 lần lưu lại vẫn không tích lũy thêm space\n"
       "- Tin trên app LINE và chat 1:1 khớp với preview",
       env="PRODUCTION",
       note="Nguồn: r875-r880 (SpecImprove #35253). ⚠️ Fix này áp dụng cho NHIỀU màn (template, scenario, "
            "remind, multi action, chat 1:1, schedule) — kho FA-008 chỉ giữ phần của màn broadcast; "
            "phần các màn khác xem mục『Đã loại』. RULE-08: URL/domain → PRODUCTION."),

    tc("Broadcast cũ & tương thích", "REG-SPEC-001", "Normal",
       "Gửi thử ở màn broadcast — URL không bị thêm khoảng trắng thừa",
       "- Broadcast có tin nhắn chứa URL dài, đã triển khai fix #35253",
       "1. Gửi thử từng friend bằng「テスト送信」\n"
       "2. Gửi thử nhiều friend bằng「一括テスト送信」\n"
       "3. Ở mỗi lần: mở app LINE và chat 1:1 kiểm tra URL",
       "Tin nhắn có URL dài, gửi thử 2 kiểu",
       "- Cả 2 kiểu gửi thử: URL trên app LINE và chat 1:1 đúng như đã nhập\n"
       "- Không có khoảng trắng thừa ở đầu URL",
       env="PRODUCTION",
       note="Nguồn: r879-r880 (SpecImprove #35253). RULE-08: URL/domain → PRODUCTION."),

    # ═══════════ 31. Phân quyền & môi trường ═══════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff CÓ quyền broadcast — thao tác được đầy đủ như Admin",
       "- Bot có 1 staff được Admin cấp quyền truy cập màn broadcast",
       "1. Đăng nhập bằng staff đó\n"
       "2. Mở màn「メッセージ配信」\n"
       "3. Thử: tạo mới · sửa · copy · xóa · gửi thử · hover vào 配信数 và bấm nút tính lại\n"
       "4. Kiểm tra kết quả từng thao tác",
       "Staff có quyền broadcast",
       "- Vào được màn broadcast, thấy đủ 3 tab\n"
       "- Cả 6 thao tác đều thực hiện được thành công\n"
       "- Nút tính lại số gửi hoạt động bình thường",
       note="Nguồn: r872, r951 (Bug KH #36730 — 『Account staff có quyền broadcast: click/hover vào hiển "
            "thị được thông tin thao tác send all』) + [AI] alert_limit r78 (TC-BAL-077).",
       group="API"),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "Staff KHÔNG có quyền broadcast — không vào được, gọi thẳng URL cũng bị chặn",
       "- Bot có 1 staff KHÔNG được cấp quyền truy cập màn broadcast",
       "1. Đăng nhập bằng staff đó\n"
       "2. Kiểm tra Sidebar có mục「メッセージ配信」không\n"
       "3. Gõ thẳng URL /basic/message-send-all vào thanh địa chỉ\n"
       "4. Gõ thẳng URL màn edit /basic/add-broadcast-v2?broadcast_id=XXX với id có thật",
       "Staff không có quyền broadcast · id broadcast có thật của bot đó",
       "- Sidebar KHÔNG hiển thị mục「メッセージ配信」\n"
       "- Gõ thẳng URL: hiển thị thông báo không có quyền hoặc redirect về dashboard\n"
       "- KHÔNG hiển thị nội dung broadcast trong bất kỳ trường hợp nào\n"
       "- Direct URL không bypass được phân quyền",
       note="Nguồn: r952 (Bug KH #36730) + [AI] alert_limit r79 (TC-BAL-078). "
            "⚠️ MT-22 — feature-spec.md §6 ghi『Tất cả routes broadcast dùng middleware chung web + auth. "
            "KHÔNG có middleware access control riêng』, tức spec KHÔNG khẳng định có chặn ở tầng route.",
       group="API"),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "Gọi thẳng API broadcast bằng session staff không quyền — bị từ chối",
       "- Staff không có quyền broadcast, có session hợp lệ",
       "1. Đăng nhập staff không quyền, lấy session\n"
       "2. Dùng công cụ API gọi thẳng endpoint lưu broadcast với session đó\n"
       "3. Gọi thẳng endpoint lấy danh sách broadcast\n"
       "4. Gọi thẳng endpoint xóa broadcast\n"
       "5. Với mỗi lời gọi: ghi mã trạng thái trả về và kiểm tra dữ liệu có bị thay đổi không",
       "Session staff không quyền · 3 endpoint: lưu · lấy danh sách · xóa",
       "- Cả 3 lời gọi đều bị từ chối (403 hoặc redirect về đăng nhập)\n"
       "- KHÔNG endpoint nào trả về dữ liệu broadcast\n"
       "- Dữ liệu trong DB không bị thay đổi",
       note="Nguồn: [AI] alert_limit r80-r81 (TC-BAL-079, 080) + tab「API Tests 36436」r9. "
            "⚠️ Liên quan MT-22. Đây là điểm hay lọt bug: UI ẩn menu nhưng API không enforce.",
       group="API"),

    tc("Phân quyền & môi trường", "SEC-ISO-001", "Abnormal",
       "Gọi API broadcast với id thuộc bot KHÁC — bị từ chối, không lộ dữ liệu",
       "- Có 2 tài khoản Admin thuộc 2 bot khác nhau: Admin A (bot A) và Admin B (bot B)\n"
       "- Biết một broadcast_id có thật của bot B",
       "1. Đăng nhập Admin A\n"
       "2. Gọi thẳng endpoint lấy chi tiết broadcast với broadcast_id của bot B\n"
       "3. Gọi thẳng endpoint lưu/sửa broadcast với id đó\n"
       "4. Gọi thẳng endpoint xóa với id đó\n"
       "5. Kiểm tra dữ liệu bot B có bị đổi không",
       "Admin A (bot A) · broadcast_id thuộc bot B",
       "- Cả 3 lời gọi đều trả 403 hoặc lỗi không tìm thấy\n"
       "- KHÔNG trả về nội dung broadcast của bot B (không lộ tiêu đề, tin nhắn, danh sách friend)\n"
       "- Dữ liệu bot B không bị sửa hoặc xóa",
       note="Nguồn: [AI] alert_limit r82-r83 (TC-BAL-081, 082) + tab「API Tests 36436」r6, r10, r25.",
       group="API"),

    tc("Phân quyền & môi trường", "SEC-002", "Abnormal",
       "Gọi API broadcast khi chưa đăng nhập — bị chặn",
       "- Không có session (đã đăng xuất hoặc cookie hết hạn)\n- Biết một broadcast_id có thật",
       "1. Đăng xuất hoàn toàn\n"
       "2. Gọi thẳng endpoint lấy danh sách broadcast\n"
       "3. Gọi thẳng endpoint lưu broadcast\n"
       "4. Ghi lại mã trạng thái trả về",
       "Không session · broadcast_id có thật",
       "- Trả về 401 hoặc redirect về màn đăng nhập\n"
       "- Không trả về dữ liệu broadcast\n"
       "- Không tạo/sửa được bản ghi nào",
       note="Nguồn: 03/tab「API Tests 36436」r8 (TC-BAL-037).",
       group="API"),

    tc("Phân quyền & môi trường", "ENV-001", "Normal",
       "Đối chiếu hành vi giữa staging và production cho các luồng gửi tin",
       "- Có cùng bộ dữ liệu test trên staging và production",
       "1. Trên staging: chạy luồng tạo → đăng ký → job gửi, ghi lại kết quả\n"
       "2. Trên production: chạy đúng luồng đó với dữ liệu tương đương\n"
       "3. So sánh: thời điểm gửi thực tế · nội dung tin friend nhận · số 配信数 · avatar người gửi",
       "Cùng cấu hình broadcast trên 2 môi trường",
       "- Nội dung tin nhắn và số 配信数 giống nhau ở cả 2 môi trường\n"
       "- Nếu có khác biệt (thời gian gửi, đường dẫn ảnh, domain URL) phải ghi rõ và giải thích được",
       env="PRODUCTION",
       note="Nguồn: cột「staging」và「Note (staging)」của tab master — nhiều TC có kết quả khác nhau giữa "
            "dev và staging (VD file 03/tab function r13『loading mãi success』trên staging, 『dev k bị』). "
            "RULE-08: job nền + media + domain → bắt buộc đối chiếu PRODUCTION.",
       group="API"),

    tc("Phân quyền & môi trường", "COMPAT-BROWSER-001", "Normal",
       "Toàn màn broadcast hoạt động trên Chrome (Windows) và Safari (Mac)",
       "- Chuẩn bị Windows + Chrome và Mac + Safari",
       "1. Trên mỗi trình duyệt, chạy luồng: vào màn list → 3 tab → tạo mới → thêm tin nhắn → "
       "đặt filter → preview & gửi thử → lưu\n"
       "2. Kiểm tra hover vào 配信数, kéo thả sắp xếp tin nhắn, date picker\n"
       "3. So sánh 2 trình duyệt",
       "Chrome trên Windows · Safari trên macOS",
       "- Cả luồng chạy được trên cả 2 trình duyệt\n"
       "- Hover popover, kéo thả, date picker hoạt động ở cả 2\n"
       "- Không có khác biệt làm mất chức năng",
       note="Nguồn: r936, r947 (Bug KH #36730 — 『Check hover trên safari máy mac』/『chrome máy win』) + "
            "[AI] alert_limit r86 (TC-BAL-085)."),

    tc("Phân quyền & môi trường", "UI-002", "Normal",
       "Màn broadcast là PC-web — xác nhận không có bản mobile app/LIFF riêng",
       "- Có app mobile của LME",
       "1. Mở app mobile, tìm chức năng gửi tin hàng loạt\n"
       "2. Mở màn broadcast trên trình duyệt điện thoại\n"
       "3. Ghi lại hành vi thực tế",
       "App mobile LME · trình duyệt trên điện thoại",
       "- Ghi rõ: app mobile có hay không có luồng tạo/đăng ký broadcast\n"
       "- Nếu mở trên trình duyệt điện thoại: ghi rõ có dùng được hay hiển thị lỗi/khuyến cáo dùng PC",
       spec="Đã hỏi leader",
       note="Nguồn: [AI] alert_limit r92 (TC-BAL-091 —『Xác nhận phạm vi surface: đăng ký broadcast là "
            "PC-web only, KHÔNG có mobile app/LIFF riêng cho luồng này』). ⚠️ Spec KHÔNG nói về phạm vi "
            "thiết bị — cần Leader xác nhận."),

    tc("Phân quyền & môi trường", "NOTI-MAIL-001", "Normal",
       "Thông báo mobile khi broadcast gửi xong",
       "- Admin đã bật nhận thông báo trên app mobile\n- Broadcast đặt lịch gửi cho ≥3 friend",
       "1. Bật thông báo mobile cho Admin\n"
       "2. Chờ job gửi broadcast xong\n"
       "3. Kiểm tra app mobile của Admin có nhận thông báo không\n"
       "4. Đọc nội dung thông báo",
       "Broadcast 3 friend, Admin bật notify mobile",
       "- Admin nhận được thông báo trên app mobile sau khi gửi xong\n"
       "- Nội dung thông báo nêu đúng tên broadcast và trạng thái hoàn tất",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: feature-spec.md §2 bước 8 (『Notification mobile (nếu bật)』) + §7 (『User cuối: gửi "
            "mobile notification + cập nhật summary stats』). ⚠️ Corpus KHÔNG có TC cho nhánh này — "
            "TC do AI bổ sung từ spec, cần Leader xác nhận. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Phân quyền & môi trường", "DEPLOY-LIVE-001", "Boundary",
       "Deploy giữa lúc có broadcast đang chờ gửi — không mất lịch, không gửi trùng",
       "- Có ≥3 broadcast wait_to_send đặt lịch rải trong 30 phút tới\n- Sắp có đợt deploy",
       "1. Ghi lại danh sách broadcast wait_to_send và giờ gửi của từng cái\n"
       "2. Thực hiện deploy trong khoảng thời gian đó\n"
       "3. Sau deploy, kiểm tra danh sách broadcast wait_to_send còn nguyên không\n"
       "4. Chờ qua tất cả các mốc, kiểm tra app LINE của friend nhận\n"
       "5. Đọc 配信数 và status của từng broadcast",
       "3 broadcast wait_to_send rải trong 30 phút · 1 đợt deploy",
       "- Không broadcast nào biến mất khỏi tab「配信予約」sau deploy\n"
       "- Tất cả đều được gửi (có thể trễ trong khoảng cảnh báo 5-15 phút)\n"
       "- Friend KHÔNG nhận trùng tin của cùng 1 broadcast\n"
       "- Không broadcast nào bị chuyển sang send_false vì quá hạn do downtime",
       env="PRODUCTION",
       note="Nguồn: feature-spec.md §5 BR-11 (『Tránh gửi broadcast quá cũ khi service bị down』) + §7 "
            "(resume sau restart). ⚠️ Corpus KHÔNG có TC cho nhánh deploy — TC do AI bổ sung, quan trọng "
            "vì downtime > 15 phút sẽ làm broadcast chuyển send_false. RULE-08: deploy + job → PRODUCTION.",
       group="API"),
]
