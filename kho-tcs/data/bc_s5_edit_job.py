# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 21-26: Edit broadcast & rule 5 phút, Copy broadcast,
Xóa & xóa hàng loạt, Job gửi & vòng đời trạng thái, Job quá hạn/lỗi/resume,
Job action sau khi gửi.
"""
from _common import tc

L = ("- Đăng nhập Admin của 1 bot đã liên kết LOA\n"
     "- Ở màn /basic/message-send-all, tab「配信予約」")
E = L + "\n- Có broadcast「編集テスト」wait_to_send, giờ gửi còn cách hiện tại > 30 phút"

S5 = [
    # ═══════════ 21. Edit broadcast & rule 5 phút ═══════════
    tc("Edit broadcast & rule 5 phút", "FUNC-001", "Normal",
       "Bấm vào bất kỳ chỗ nào trong dòng bản ghi — mở màn edit",
       E,
       "1. Bấm vào cột「管理用タイトル」của bản ghi → quan sát\n"
       "2. Quay lại, bấm vào cột「送信者名」→ quan sát\n"
       "3. Quay lại, bấm vào nút「編集」ở cột「操作」→ quan sát",
       "Bấm ở 3 vị trí khác nhau trong cùng 1 dòng",
       "- Cả 3 lần đều mở màn edit của đúng broadcast đó (SCR-BC-04, có ?broadcast_id=)\n"
       "- Không mở nhầm broadcast khác",
       note="Nguồn: r250-r251."),

    tc("Edit broadcast & rule 5 phút", "CONC-002", "Abnormal",
       "Double click nút「編集」— chỉ mở 1 màn edit",
       E,
       "1. Double click nhanh vào nút「編集」\n"
       "2. Quan sát số tab/màn mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 màn edit",
       note="Nguồn: r252."),

    tc("Edit broadcast & rule 5 phút", "DATA-001", "Normal",
       "Mở màn edit — hiển thị đầy đủ dữ liệu ban đầu của broadcast",
       E + "\n- Broadcast có: tiêu đề, 2 mốc gửi, filter tag T, 3 tin nhắn, 2 action, profile「送信者A」",
       "1. Mở màn edit của broadcast\n"
       "2. Đối chiếu từng khối với dữ liệu đã lưu: 管理用タイトル · 配信タイミング設定 · "
       "メッセージ登録 · エルメアクション · 送信者名 · 配信先絞込み",
       "Tiêu đề「編集テスト」· 2 mốc gửi · filter tag T · 3 tin nhắn · 2 action · profile「送信者A」",
       "- Cả 6 khối đều hiển thị đúng giá trị đã lưu\n"
       "- Số 配信数 khớp với số ở màn list\n"
       "- Không có khối nào bị trống hoặc mất dữ liệu",
       note="Nguồn: r253."),

    tc("Edit broadcast & rule 5 phút", "FUNC-001", "Normal",
       "Sửa từng thành phần của broadcast và lưu — thay đổi phản ánh ở màn list và tin friend nhận",
       E + "\n- Có 1 friend trong đối tượng nhận để verify",
       "1. Mở màn edit, lần lượt sửa: filter · tin nhắn · action · tên quản lý · người gửi\n"
       "2. Bấm「配信内容を確認して送信に進む」lưu lại\n"
       "3. Về màn list, đối chiếu từng cột với giá trị mới\n"
       "4. Chờ job gửi, kiểm tra tin friend nhận được",
       "Đổi filter tag T → tag U · sửa nội dung tin nhắn · đổi action gán tag · "
       "đổi tiêu đề · đổi profile「送信者A」→「送信者B」",
       "- Màn list: cột 配信先絞込み · 管理用タイトル · 送信者名 · アクション · 配信数 đều cập nhật theo giá trị mới\n"
       "- Friend nhận tin với nội dung mới, người gửi là「送信者B」, action mới được thực thi",
       env="PRODUCTION",
       note="Nguồn: r254-r261. RULE-06 + RULE-07: verify cả màn list và output LINE. "
            "RULE-08: job gửi thật → PRODUCTION."),

    tc("Edit broadcast & rule 5 phút", "FUNC-001", "Abnormal",
       "Sửa thiếu trường bắt buộc — không lưu được",
       E,
       "1. Mở màn edit, xóa trắng「管理用タイトル」\n"
       "2. Bấm「配信内容を確認して送信に進む」\n"
       "3. Về màn list kiểm tra tiêu đề của broadcast",
       "管理用タイトル = trống",
       "- Hiện validate báo thiếu trường bắt buộc\n"
       "- KHÔNG lưu, tiêu đề ở màn list giữ nguyên giá trị cũ",
       note="Nguồn: r263."),

    tc("Edit broadcast & rule 5 phút", "STATE-CLEAN-001", "Abnormal",
       "Sửa đủ trường nhưng KHÔNG lưu — dữ liệu giữ nguyên như cũ",
       E,
       "1. Mở màn edit, đổi tiêu đề thành「変更した」\n"
       "2. KHÔNG bấm lưu, bấm「メッセージ配信一覧に戻る」→ chọn「中断する」ở popup\n"
       "3. Về màn list đọc tiêu đề",
       "Đổi tiêu đề nhưng không lưu",
       "- Tiêu đề ở màn list vẫn là「編集テスト」\n"
       "- Bảng broadcast: name không đổi",
       note="Nguồn: r264, r269-r270. Lưu ý: filter và tin nhắn KHÔNG theo quy tắc này — xem TC riêng "
            "về filter tự lưu ở modal (MT-10)."),

    tc("Edit broadcast & rule 5 phút", "UI-001", "Normal",
       "Đang sửa mà bấm back/reset — hiện popup 作業を中断しますか？",
       E,
       "1. Mở màn edit, đổi 1 trường bất kỳ\n"
       "2. Bấm「メッセージ配信一覧に戻る」\n"
       "3. Quan sát popup hiện ra",
       "Đã sửa 1 trường, chưa lưu",
       "- Hiện popup có tiêu đề「作業を中断しますか？」\n"
       "- Popup có nút「中断する」và link「作業に戻る」có gạch chân\n"
       "- Bố cục khớp design",
       note="Nguồn: r265-r267, r271."),

    tc("Edit broadcast & rule 5 phút", "FUNC-001", "Normal",
       "Bấm「中断する」— đóng popup, về màn list, thay đổi bị hủy",
       E,
       "1. Mở màn edit, đổi tiêu đề thành「変更した」\n"
       "2. Bấm「メッセージ配信一覧に戻る」→ popup hiện ra\n"
       "3. Bấm「中断する」\n"
       "4. Đọc tiêu đề ở màn list\n"
       "5. Mở lại màn edit đọc giá trị trong ô",
       "Đổi tiêu đề, chọn 中断する",
       "- Popup đóng, chuyển về màn list\n"
       "- Tiêu đề vẫn là「編集テスト」(thay đổi bị reset)\n"
       "- Mở lại màn edit cũng là giá trị cũ",
       note="Nguồn: r269-r270."),

    tc("Edit broadcast & rule 5 phút", "CONC-002", "Abnormal",
       "Double click「中断する」và「作業に戻る」— chỉ tính 1 lần",
       E,
       "1. Mở popup「作業を中断しますか？」\n"
       "2. Double click nhanh vào「中断する」→ quan sát\n"
       "3. Lặp lại quy trình, double click nhanh vào「作業に戻る」→ quan sát",
       "Double click trong < 1 giây",
       "- Mỗi nút chỉ thực thi 1 lần\n"
       "- Không chuyển màn 2 lần hoặc đóng/mở popup lặp",
       note="Nguồn: r268, r272."),

    tc("Edit broadcast & rule 5 phút", "STATE-001", "Normal",
       "Bấm「作業に戻る」— đóng popup, tiếp tục sửa, dữ liệu đã nhập còn nguyên",
       E,
       "1. Mở màn edit, đổi tiêu đề thành「変更した」\n"
       "2. Bấm「メッセージ配信一覧に戻る」→ popup hiện\n"
       "3. Bấm「作業に戻る」\n"
       "4. Đọc giá trị trong ô「管理用タイトル」",
       "Đổi tiêu đề, chọn 作業に戻る",
       "- Popup đóng, vẫn ở màn edit\n"
       "- Ô「管理用タイトル」vẫn giữ「変更した」(dữ liệu chưa lưu không bị mất)",
       note="Nguồn: r273."),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Broadcast gửi ngay (click send) — vẫn cho sửa filter",
       L + "\n- Có broadcast đang ở luồng gửi ngay, chưa bấm gửi",
       "1. Tạo broadcast chọn「メッセージ登録後すぐに配信」\n"
       "2. Mở màn edit, thử sửa điều kiện filter\n"
       "3. Lưu và kiểm tra filter đã đổi chưa",
       "Broadcast gửi ngay, đổi filter tag T → tag U",
       "- Sửa filter được bình thường, không bị chặn\n"
       "- Sau khi lưu, filter cập nhật thành tag U",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r19."),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Broadcast đặt lịch, còn HƠN 5 phút tới giờ gửi — cho sửa filter",
       L + "\n- Broadcast wait_to_send, giờ gửi cách hiện tại 10 phút",
       "1. Tạo broadcast đặt lịch sau 10 phút\n"
       "2. Mở màn edit, sửa điều kiện filter\n"
       "3. Lưu và kiểm tra filter đã cập nhật chưa",
       "Giờ gửi = hiện tại + 10 phút · đổi filter tag T → tag U",
       "- Sửa filter được, không hiện thông báo chặn\n"
       "- Filter cập nhật thành tag U",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r20."),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Broadcast đặt lịch, còn DƯỚI 5 phút tới giờ gửi — chặn sửa, hiện đúng thông báo",
       L + "\n- Broadcast wait_to_send, giờ gửi cách hiện tại 3 phút",
       "1. Tạo broadcast đặt lịch sau 20 phút\n"
       "2. Chờ tới khi còn 3 phút trước giờ gửi\n"
       "3. Mở màn edit, thử sửa filter và bấm lưu\n"
       "4. Đọc thông báo hiện ra",
       "Giờ gửi = hiện tại + 3 phút",
       "- Hiện đúng nguyên văn thông báo「配信予定日時5分前からは配信内容の編集はできません。」\n"
       "- KHÔNG lưu được thay đổi",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r21 + r262 + logic-spec.md:491-495. "
            "⚠️ MT-16 — UI nói「5分前」nhưng code dùng subMinutes(6), tức thực tế chặn từ 6 phút."),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Ranh giới 5 phút vs 6 phút — xác định mốc chặn thực tế",
       L,
       "1. Tạo broadcast đặt lịch sau 20 phút\n"
       "2. Ở mốc còn đúng 7 phút: thử sửa và lưu → ghi lại kết quả\n"
       "3. Ở mốc còn đúng 6 phút: thử sửa và lưu → ghi lại kết quả\n"
       "4. Ở mốc còn đúng 5 phút: thử sửa và lưu → ghi lại kết quả\n"
       "5. Ở mốc còn đúng 4 phút: thử sửa và lưu → ghi lại kết quả",
       "4 mốc thời gian: còn 7 / 6 / 5 / 4 phút trước giờ gửi",
       "- Ghi rõ mốc đầu tiên bị chặn là 6 phút hay 5 phút\n"
       "- Kết quả phải nhất quán với con số ghi trong thông báo lỗi",
       spec="Đã hỏi leader",
       note="⚠️ MT-16 — logic-spec.md:495 ghi『Thực tế trong code: subMinutes(6) (buffer thêm 1 phút)』"
            "trong khi UI và thông báo lỗi đều nói 5分前. Corpus chỉ test 2 mốc thô (>5p / <5p). "
            "TC này do AI bổ sung để đo mốc thật; cần Leader chốt con số đúng."),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Sửa filter trong cửa sổ đóng băng — job vẫn gửi theo filter CŨ",
       L + "\n- Broadcast wait_to_send đặt lịch, filter tag T (5 friend)",
       "1. Tạo broadcast filter tag T, đặt lịch sau 20 phút\n"
       "2. Khi còn < 10 phút trước giờ gửi: gỡ tag T khỏi 2 friend\n"
       "3. Chờ job gửi\n"
       "4. Kiểm tra app LINE của cả 5 friend\n"
       "5. Đọc 配信数 ở tab「配信履歴」",
       "Tag T = 5 friend, gỡ 2 người khi còn < 10 phút trước giờ gửi",
       "- Cả 5 friend đều nhận được tin (job dùng filter đã pre-cache, không theo thay đổi mới)\n"
       "- Bảng filters_v2 vẫn ghi nhận filter mới, nhưng job gửi theo danh sách cũ\n"
       "- 配信数 ở lịch sử = 5",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r11 (『broadcast setting time - update "
            "filter trong vòng 10p trước time send → vẫn send cho user đó, ko update filter』). "
            "⚠️ MT-17 — corpus nói cửa sổ đóng băng của BROADCAST là 10 phút, của SCENARIO STEP là 5 phút; "
            "job-spec.md:195 chỉ ghi hằng số `PREPARE_FILTER_BROADCAST_BEFORE` mà KHÔNG ghi giá trị. "
            "RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Sửa filter NGOÀI cửa sổ đóng băng — job gửi theo filter MỚI",
       L + "\n- Broadcast wait_to_send đặt lịch, filter tag T (5 friend)",
       "1. Tạo broadcast filter tag T, đặt lịch sau 30 phút\n"
       "2. Khi còn > 10 phút trước giờ gửi: gỡ tag T khỏi 2 friend\n"
       "3. Chờ job gửi\n"
       "4. Kiểm tra app LINE của cả 5 friend\n"
       "5. Đọc 配信数 ở tab「配信履歴」",
       "Tag T = 5 friend, gỡ 2 người khi còn > 10 phút trước giờ gửi",
       "- Chỉ 3 friend còn tag T nhận được tin\n"
       "- 2 friend đã gỡ tag KHÔNG nhận được\n"
       "- 配信数 ở lịch sử = 3",
       env="PRODUCTION",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r12. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Đổi giờ gửi làm broadcast rơi vào/ra khỏi cửa sổ đóng băng",
       L,
       "1. Tạo broadcast filter tag T, đặt lịch sau 30 phút (ngoài cửa sổ)\n"
       "2. Đổi filter, rồi đổi giờ gửi thành sau 5 phút (vào trong cửa sổ) → lưu, chờ gửi\n"
       "3. Tạo broadcast thứ 2 đặt lịch sau 5 phút (trong cửa sổ)\n"
       "4. Đổi filter, rồi đổi giờ gửi thành sau 30 phút (ra ngoài cửa sổ) → lưu, chờ gửi\n"
       "5. So danh sách friend nhận được với filter mới ở cả 2 trường hợp",
       "TH1: >10p → đổi filter → đổi giờ thành <10p · TH2: <10p → đổi filter → đổi giờ thành >10p",
       "- Cả 2 trường hợp: job gửi theo filter MỚI (vì thời điểm pre-filter được tính lại theo giờ gửi mới)\n"
       "- Friend không còn thỏa filter mới KHÔNG nhận được tin",
       env="PRODUCTION",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r13-r14. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Edit broadcast & rule 5 phút", "STATE-DEP-001", "Boundary",
       "Tạo broadcast sát giờ gửi (< 10 phút) — filter cập nhật liên tục",
       L,
       "1. Tạo broadcast mới, đặt lịch sau 3 phút, filter tag T\n"
       "2. Ngay sau khi lưu, đổi tag của 1 friend\n"
       "3. Bấm「再計算」quan sát số\n"
       "4. Chờ job gửi, kiểm tra ai nhận được tin",
       "Giờ gửi = hiện tại + 3 phút, tag T = 4 friend",
       "- Số 配信数 cập nhật được ngay khi bấm 再計算\n"
       "- Job gửi đúng cho nhóm friend thỏa filter tại thời điểm job chạy",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r17 (『case tạo gần với time send <10p "
            "→ update filter liên tục』). ⚠️ Hành vi này mâu thuẫn với TC đóng băng filter ở trên — "
            "xem MT-17.",
       group="API"),

    # ═══════════ 22. Copy broadcast ═══════════
    tc("Copy broadcast", "UI-001", "Normal",
       "Icon/text コピー hiển thị đúng design ở cả 3 tab",
       L + "\n- Mỗi tab có ≥1 broadcast",
       "1. Quan sát icon/text「コピー」ở cột「操作」của tab「配信予約」\n"
       "2. Lặp lại ở tab「下書き」và tab「配信履歴」",
       "1 broadcast mỗi tab",
       "- Cả 3 tab đều có nút copy ở cột「操作」\n"
       "- Hình dạng và vị trí khớp design",
       note="Nguồn: r348, r749 + file 03/tab function r24-r26."),

    tc("Copy broadcast", "CONC-002", "Abnormal",
       "Double click コピー — chỉ tạo 1 bản copy",
       E,
       "1. Double click nhanh vào「コピー」\n"
       "2. Về tab「下書き」đếm số bản copy được tạo",
       "Double click trong < 1 giây",
       "- Chỉ tạo đúng 1 bản copy\n"
       "- Không sinh 2 bản trùng nhau",
       note="Nguồn: r349, r750.",
       group="API"),

    tc("Copy broadcast", "FUNC-001", "Normal",
       "Copy thành công — bản mới nằm ở tab 下書き và mở luôn màn edit",
       E,
       "1. Bấm「コピー」ở broadcast「編集テスト」\n"
       "2. Quan sát màn hình ngay sau khi copy\n"
       "3. Về màn list kiểm tra tab「下書き」và tab gốc",
       "Broadcast gốc「編集テスト」ở tab 配信予約",
       "- Sau khi copy: mở thẳng ra màn edit của bản copy\n"
       "- Bản copy nằm ở tab「下書き」với status = 'draft'\n"
       "- Broadcast gốc vẫn ở tab「配信予約」, không bị đổi",
       note="Nguồn: r350, r751 + file 03/tab「Bug Task Small Send All update 14/6」r10 — ghi nhận bug "
            "『tạo broadcast success đang redirect sang tab nháp, expect: mở luôn ra phần dưới』. "
            "TC viết theo hành vi ĐÚNG."),

    tc("Copy broadcast", "FUNC-001", "Normal",
       "Copy từ màn 配信履歴 bằng nút「同じ内容でメッセージを作成する」",
       L + "\n- Có broadcast đã gửi xong ở tab「配信履歴」",
       "1. Mở preview của broadcast đã gửi\n"
       "2. Bấm nút「同じ内容でメッセージを作成する」\n"
       "3. Quan sát màn hình và tab「下書き」",
       "Broadcast delivered「配信済みテスト」",
       "- Tạo 1 bản mới ở tab「下書き」\n"
       "- Mở ra màn thông tin chi tiết của bản mới\n"
       "- Nội dung tin nhắn, filter, action, người gửi giống bản gốc",
       note="Nguồn: r716-r717 — r717 ghi kết quả NG. TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa "
            "fix → cần raise bug."),

    tc("Copy broadcast", "DATA-REF-001", "Normal",
       "Copy — template riêng của broadcast được clone, template dùng chung giữ reference",
       L + "\n- Broadcast có 1 tin nhắn soạn trực tiếp (category -11) và 1 template từ thư viện",
       "1. Copy broadcast\n"
       "2. Ở bản copy, sửa nội dung tin nhắn soạn trực tiếp\n"
       "3. Mở broadcast GỐC, kiểm tra nội dung tin đó\n"
       "4. Sửa template thư viện ở màn「テンプレート」\n"
       "5. Mở bản copy, kiểm tra tin dùng template thư viện",
       "1 tin soạn trực tiếp (category_id = -11) · 1 template thư viện (category_id ≥ 0)",
       "- Sửa tin soạn trực tiếp ở bản copy KHÔNG ảnh hưởng broadcast gốc (đã clone)\n"
       "- Sửa template thư viện thì bản copy ĐỔI THEO (giữ reference)\n"
       "- Bảng template: có bản clone mới cho tin category -11",
       note="Nguồn: feature-spec.md §5 BR-07 + logic-spec.md:186-188.",
       group="Data"),

    tc("Copy broadcast", "STATE-DEP-001", "Normal",
       "Bản copy KHÔNG sửa được filter trước khi lưu lần đầu",
       L + "\n- Broadcast gốc có filter tag T",
       "1. Copy broadcast\n"
       "2. Ở màn edit bản copy (chưa bấm lưu lần nào), thử mở popup filter và đổi điều kiện\n"
       "3. Ghi lại hành vi\n"
       "4. Bấm lưu bản copy\n"
       "5. Thử lại việc sửa filter",
       "Bản copy chưa lưu · filter gốc = tag T",
       "- Trước khi lưu: KHÔNG sửa được filter, bản copy giữ nguyên filter của bản gốc\n"
       "- Sau khi lưu: sửa filter được bình thường",
       spec="Đã hỏi leader",
       note="Nguồn: r852-r862 (Bug #32229, 02/10/2025 —『Khi chưa nhấn save broadcast thì không edit được "
            "filter => setting filter của broadcast mới sẽ giống broadcast gốc』). "
            "⚠️ MT-18 — spec KHÔNG mô tả ràng buộc này; đây là hành vi phát sinh từ fix bug #32229."),

    tc("Copy broadcast", "DATA-REF-001", "Normal",
       "Copy broadcast KHÔNG filter — bản copy cũng không filter",
       L + "\n- Broadcast gốc chọn すべての友だち",
       "1. Copy broadcast\n"
       "2. Không đổi gì, bấm lưu bản copy\n"
       "3. Về màn list kiểm tra cột「配信先絞込み」của bản copy",
       "Broadcast gốc flag_setting_filter = 0",
       "- Bản copy cũng ở trạng thái không filter\n"
       "- Màn list hiển thị「未設定（全員）」\n"
       "- Khi gửi, tin đến TOÀN BỘ bạn bè",
       note="Nguồn: r851 (Bug #32229).",
       group="Data"),

    tc("Copy broadcast", "DATA-REF-001", "Normal",
       "Copy broadcast CÓ filter — bản copy giữ nguyên filter, KHÔNG gửi cho all friend",
       L + "\n- Broadcast gốc có filter tag T (4 friend), bot có 10 bạn bè",
       "1. Copy broadcast\n"
       "2. Không đổi gì, bấm lưu bản copy\n"
       "3. Kiểm tra 配信先絞込み và 配信数 của bản copy\n"
       "4. Đặt lịch gửi bản copy, chờ job gửi\n"
       "5. Kiểm tra app LINE của cả 10 bạn bè",
       "Broadcast gốc filter tag T = 4 friend · bot có 10 bạn bè",
       "- Bản copy hiển thị「設定済み」, 配信数 = 4\n"
       "- Chỉ 4 friend có tag T nhận được tin\n"
       "- 6 friend còn lại KHÔNG nhận được",
       env="PRODUCTION",
       note="Nguồn: r857 + r809 (Bug #32229 — 『Copy từ broadcast có filter sau đó đặt lịch gửi, nhưng "
            "broadcast copy lại bị gửi cho all friend』). Đây là TC tái hiện bug gốc. "
            "RULE-08: job gửi thật → PRODUCTION.",
       group="API"),

    tc("Copy broadcast", "FUNC-001", "Normal",
       "Sửa bản copy rồi lưu — đích đến đúng theo kiểu gửi đã chọn",
       L + "\n- Vừa copy 1 broadcast, đang ở màn edit bản copy",
       "1. Sửa thông tin bản copy, chọn「メッセージ登録後すぐに配信」→ lưu → kiểm tra tab\n"
       "2. Copy lại, chọn đặt lịch thời gian TƯƠNG LAI → lưu → kiểm tra tab\n"
       "3. Copy lại, chọn đặt lịch thời gian QUÁ KHỨ → lưu → ghi lại alert và tab kết quả\n"
       "4. Copy lại, bấm「下書きとして保存」→ kiểm tra tab",
       "4 kiểu lưu: gửi ngay · đặt lịch tương lai · đặt lịch quá khứ · lưu nháp",
       "- Gửi ngay → bản copy vào tab「配信履歴」\n"
       "- Đặt lịch tương lai → vào tab「配信予約」\n"
       "- Đặt lịch quá khứ → hiện alert 配信日時に現在時刻より前の時間… , chọn OK thì gửi ngay\n"
       "- Lưu nháp → vào tab「下書き」",
       env="PRODUCTION",
       note="Nguồn: r351-r360, r718-r731, r752-r765. Đây là ma trận 4 điểm có 4 KẾT QUẢ KHÁC NHAU nhưng "
            "cùng 1 quy tắc『đích đến theo kiểu gửi』— giữ chung 1 TC vì là chuỗi thao tác liên tiếp trên "
            "cùng bản copy; nếu Leader muốn tách thì tách thành 4."),

    tc("Copy broadcast", "FUNC-001", "Abnormal",
       "Lưu bản copy khi thiếu trường bắt buộc — hiện alert",
       L + "\n- Vừa copy 1 broadcast, đang ở màn edit bản copy",
       "1. Xóa trắng「管理用タイトル」của bản copy\n"
       "2. Bấm「下書きとして保存」→ ghi lại thông báo\n"
       "3. Bấm「配信内容を確認して送信に進む」→ ghi lại thông báo",
       "管理用タイトル = trống",
       "- Cả 2 nút đều hiện alert báo thiếu trường bắt buộc\n"
       "- KHÔNG lưu bản copy",
       note="Nguồn: r355, r722, r724, r756, r758."),

    tc("Copy broadcast", "FUNC-001", "Normal",
       "Copy từ bản ghi CHA, bản ghi CON và từ chính bản copy",
       L + "\n- Broadcast「親テスト」có 3 mốc gửi (1 cha + 2 con) ở tab「配信予約」",
       "1. Copy từ dòng bản ghi CHA → kiểm tra bản copy có mấy mốc gửi\n"
       "2. Copy từ dòng bản ghi CON → kiểm tra bản copy có mấy mốc gửi\n"
       "3. Copy từ chính bản copy vừa tạo → kiểm tra kết quả\n"
       "4. Lặp lại toàn bộ ở tab「下書き」và tab「配信履歴」",
       "Broadcast 3 mốc gửi · thực hiện ở cả 3 tab",
       "- Copy từ CHA: bản copy giữ đủ các mốc gửi (cha + con)\n"
       "- Copy từ CON: bản copy chỉ chứa thông tin của mốc con đó\n"
       "- Copy từ bản copy: tạo được bản mới, không lỗi\n"
       "- Hành vi nhất quán ở cả 3 tab",
       note="Nguồn: file 03/tab function r124-r133 (『màn draft: tạo broadcast success rồi back ra ngoài, "
            "nhiều time → sẽ hiển thị các bản ghi bao gồm cha: chứa các thằng con, con: chỉ chứa thông tin "
            "của con』). ⚠️ r126 ghi nhận bug『trong modal xác nhận lưu đang hiển danh sách số friend không "
            "khớp vs bên ngoài』."),

    tc("Copy broadcast", "DATA-COUNT-001", "Abnormal",
       "Số friend ở màn nháp của bản copy phải khớp với màn chi tiết",
       L + "\n- Broadcast gốc ở tab「配信履歴」có filter tag T (4 friend)",
       "1. Copy broadcast từ tab「配信履歴」\n"
       "2. Về tab「下書き」, đọc số ở cột「配信数」của bản copy\n"
       "3. Mở màn chi tiết bản copy, đọc số ở khối「配信先絞込み」\n"
       "4. Bấm vào số ở màn list để xem danh sách friend, đếm số dòng",
       "Filter tag T = 4 friend",
       "- Cả 3 chỗ đều hiển thị số 4, khớp nhau\n"
       "- Danh sách friend có đúng 4 dòng",
       note="Nguồn: file 03/tab「Bug Task Small Send All update 14/6」r11 (『số lượng friend ngoài màn nháp "
            "không khớp với màn detail; expect: ngoài màn nháp phải hiển thị số friend thỏa mãn』). "
            "TC viết theo hành vi ĐÚNG.",
       group="Data"),

    tc("Copy broadcast", "FUNC-001", "Normal",
       "Copy ở trang không phải trang 1 — copy đúng bản ghi được chọn",
       L + "\n- Tab「配信予約」có ≥2 trang bản ghi",
       "1. Chuyển sang trang 2\n"
       "2. Ghi lại tiêu đề của bản ghi thứ 3 trên trang 2\n"
       "3. Bấm copy ở bản ghi đó\n"
       "4. Kiểm tra tiêu đề và nội dung bản copy\n"
       "5. Lặp lại ở tab「下書き」và「配信履歴」",
       "≥2 trang bản ghi, copy ở trang 2",
       "- Bản copy có nội dung của đúng bản ghi đã chọn ở trang 2\n"
       "- Không copy nhầm bản ghi ở trang 1\n"
       "- Hành vi đúng ở cả 3 tab",
       note="Nguồn: file 03/tab function r213-r215 + Small Send All r23-r25."),

    tc("Copy broadcast", "CONC-003", "Abnormal",
       "Mở 2 tab cùng copy 1 broadcast — tạo 2 bản copy độc lập",
       L + "\n- Broadcast gốc「編集テスト」có filter tag T",
       "1. Mở 2 tab trình duyệt cùng vào màn list\n"
       "2. Ở mỗi tab bấm copy broadcast「編集テスト」\n"
       "3. Về tab「下書き」đếm số bản copy\n"
       "4. Kiểm tra filter của từng bản copy",
       "2 tab cùng copy 1 broadcast",
       "- Tạo được 2 bản copy độc lập\n"
       "- Cả 2 bản đều giữ đúng filter tag T\n"
       "- Không bản nào bị mất filter hoặc trỏ nhầm sang bản kia",
       note="Nguồn: r856, r862 (Bug #32229).",
       group="API"),

    # ═══════════ 23. Xóa & xóa hàng loạt ═══════════
    tc("Xóa & xóa hàng loạt", "CONC-002", "Abnormal",
       "Double click nút 削除 — chỉ xóa 1 lần",
       E,
       "1. Double click nhanh vào nút「削除」ở 1 bản ghi\n"
       "2. Quan sát số lượng hộp thoại xác nhận\n"
       "3. Xác nhận xóa và đếm bản ghi còn lại",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 hộp thoại xác nhận\n"
       "- Chỉ xóa đúng 1 bản ghi",
       note="Nguồn: r362."),

    tc("Xóa & xóa hàng loạt", "FUNC-001", "Normal",
       "Xóa 1 broadcast — biến mất khỏi màn list",
       E,
       "1. Ghi lại tổng số bản ghi ở tab「配信予約」\n"
       "2. Bấm「削除」ở broadcast「編集テスト」, xác nhận\n"
       "3. Đếm lại số bản ghi và tìm「編集テスト」",
       "1 broadcast wait_to_send",
       "- Broadcast「編集テスト」biến mất khỏi danh sách\n"
       "- Tổng số bản ghi giảm đúng 1\n"
       "- Bảng broadcast: bản ghi bị xóa, các template category broadcast của nó cũng bị xóa",
       note="Nguồn: r361, r363-r364 + logic-spec.md:81-83."),

    tc("Xóa & xóa hàng loạt", "STATE-001", "Normal",
       "Button 一括削除 mặc định disable, enable khi tích bản ghi",
       L + "\n- Tab「配信予約」có ≥2 bản ghi",
       "1. Quan sát button「一括削除」khi chưa tích bản ghi nào\n"
       "2. Tích 1 bản ghi → quan sát lại\n"
       "3. Bỏ tích → quan sát lại",
       "2 bản ghi",
       "- Chưa tích: button disable\n"
       "- Tích ≥1: button enable\n"
       "- Bỏ tích hết: quay lại disable",
       note="Nguồn: r373-r374."),

    tc("Xóa & xóa hàng loạt", "BULK-001", "Normal",
       "Xóa hàng loạt nhiều bản ghi ở tab 配信予約 và 下書き",
       L + "\n- Tab「配信予約」có 5 bản ghi, tab「下書き」có 5 bản ghi",
       "1. Ở tab「配信予約」tích 3 bản ghi → bấm「一括削除」→ xác nhận\n"
       "2. Đếm bản ghi còn lại và kiểm tra button\n"
       "3. Lặp lại ở tab「下書き」",
       "5 bản ghi mỗi tab, xóa 3",
       "- Sau khi xóa: mỗi tab còn 2 bản ghi, đúng 3 bản đã tích biến mất\n"
       "- Button「一括削除」quay về disable\n"
       "- Bảng broadcast: 3 bản ghi bị xóa cùng template thuộc về chúng",
       note="Nguồn: r373-r377 + file 03/tab function r73-r76."),

    tc("Xóa & xóa hàng loạt", "CONC-002", "Abnormal",
       "Double click「一括削除」— chỉ xóa 1 lần, không xóa nhầm bản ghi khác",
       L + "\n- Tab「配信予約」có 5 bản ghi, đã tích 2 bản",
       "1. Double click nhanh vào「一括削除」\n"
       "2. Xác nhận xóa\n"
       "3. Đếm bản ghi còn lại",
       "Double click trong < 1 giây, đã tích 2 bản",
       "- Chỉ xóa đúng 2 bản đã tích\n"
       "- Còn lại 3 bản, không mất thêm bản nào",
       note="Nguồn: r375.",
       group="API"),

    tc("Xóa & xóa hàng loạt", "STATE-DEP-001", "Boundary",
       "Xóa broadcast wait_to_send còn dưới 5 phút tới giờ gửi — bị chặn",
       L + "\n- Broadcast wait_to_send, giờ gửi cách hiện tại 3 phút",
       "1. Tạo broadcast đặt lịch sau 20 phút\n"
       "2. Chờ tới khi còn 3 phút trước giờ gửi\n"
       "3. Thử xóa đơn lẻ → ghi lại thông báo\n"
       "4. Thử tích rồi「一括削除」→ ghi lại thông báo",
       "Giờ gửi = hiện tại + 3 phút",
       "- Cả 2 cách xóa đều bị chặn với thông báo「配信予定日時5分前からは配信内容の編集はできません。」\n"
       "- Broadcast vẫn còn trong danh sách và vẫn được gửi đúng giờ",
       env="PRODUCTION",
       note="Nguồn: logic-spec.md:81, r157, r204 (『Kiểm tra 5 phút rule cho wait_to_send, xoá templates "
            "+ broadcast』). ⚠️ Corpus KHÔNG test trực tiếp nhánh xóa trong 5 phút — TC do AI bổ sung từ "
            "spec, cần Leader xác nhận. RULE-08: job nền → PRODUCTION."),

    tc("Xóa & xóa hàng loạt", "STATE-DEP-001", "Normal",
       "Xóa broadcast theo trạng thái — chờ gửi và nháp xóa được, đã gửi KHÔNG xóa được",
       L + "\n- Có broadcast ở cả 3 tab",
       "1. Xóa 1 broadcast ở tab「配信予約」→ ghi kết quả\n"
       "2. Xóa 1 broadcast ở tab「下書き」→ ghi kết quả\n"
       "3. Thử xóa 1 broadcast ở tab「配信履歴」→ ghi kết quả",
       "3 broadcast: wait_to_send · draft · delivered",
       "- Broadcast chờ gửi: xóa thành công\n"
       "- Broadcast nháp: xóa thành công\n"
       "- Broadcast đã gửi: KHÔNG xóa được (không có nút xóa hoặc bị chặn)",
       note="Nguồn: r805-r807 + feature-spec.md §5 BR-01 (『Không thể chỉnh sửa/xoá broadcast khi "
            "delivering hoặc delivered』)."),

    # ═══════════ 24. Job gửi & vòng đời trạng thái ═══════════
    tc("Job gửi & vòng đời trạng thái", "STATE-001", "Normal",
       "Vòng đời trạng thái đầy đủ từ tạo mới đến gửi xong",
       L + "\n- Chuẩn bị broadcast đặt lịch sau 5 phút, có tin nhắn, filter 3 friend",
       "1. Tạo broadcast chưa có tin nhắn → đọc status ở DB và tab hiển thị\n"
       "2. Thêm tin nhắn + xác nhận gửi → đọc status và tab\n"
       "3. Đúng giờ gửi, theo dõi liên tục → đọc status khi job đang chạy\n"
       "4. Sau khi gửi xong → đọc status và tab",
       "Broadcast 3 friend nhận, đặt lịch sau 5 phút",
       "- Chưa có tin nhắn: status là draft hoặc unregistered, ở tab「下書き」\n"
       "- Có tin nhắn + đặt lịch: status = 'wait_to_send', ở tab「配信予約」\n"
       "- Đang gửi: status = 'delivering', ở tab「配信履歴」\n"
       "- Gửi xong: status = 'delivered', send_count = 3, ở tab「配信履歴」",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r17-r21, r394-r398 + feature-spec.md §3 state machine. ⚠️ MT-03 — corpus gọi trạng "
            "thái chưa có tin nhắn là『unregistered』, feature-spec §5 BR-01 nói tạo mới là『draft』, "
            "db-mapping.md:223 lại nói unregistered『(không hiển thị)』chứ không phải tab 下書き. "
            "RULE-08: job nền → PRODUCTION.",
       group="Data"),

    tc("Job gửi & vòng đời trạng thái", "JOB-001", "Normal",
       "Job gửi đúng giờ đã đặt — sai số nằm trong khoảng cảnh báo 5-15 phút",
       L + "\n- Broadcast wait_to_send đặt lịch chính xác 1 mốc giờ, có 3 friend nhận",
       "1. Đặt lịch gửi vào 1 thời điểm cụ thể (VD 14:30:00)\n"
       "2. Theo dõi app LINE của 3 friend từ 14:28\n"
       "3. Ghi lại thời điểm friend đầu tiên và cuối cùng nhận được tin\n"
       "4. Đọc status ở tab「配信履歴」",
       "Giờ gửi 14:30:00, 3 friend nhận",
       "- Friend nhận được tin trong khoảng 14:30 đến 14:45 (đúng cảnh báo trễ 5-15 phút của màn list)\n"
       "- Status chuyển sang 'delivered'\n"
       "- Tất cả 3 friend đều nhận được",
       env="PRODUCTION",
       note="Nguồn: ui-spec.md:71 (cảnh báo「通信状況により配信予定時間から5~15分遅れて配信される場合が"
            "あります。」) + job-spec.md:107 (poll mỗi 5 giây). RULE-06 + RULE-08.",
       group="API"),

    tc("Job gửi & vòng đời trạng thái", "JOB-001", "Normal",
       "Broadcast nhiều mốc gửi — job gửi đủ tại từng mốc",
       L + "\n- Broadcast 3 mốc gửi cách nhau 5 phút, mỗi mốc gửi cho cùng 2 friend",
       "1. Tạo broadcast 3 mốc: +5 phút, +10 phút, +15 phút\n"
       "2. Theo dõi app LINE của 2 friend qua cả 3 mốc\n"
       "3. Đếm số lần mỗi friend nhận được tin\n"
       "4. Đọc trạng thái từng dòng ở màn list sau mỗi mốc",
       "3 mốc gửi cách nhau 5 phút, 2 friend nhận",
       "- Mỗi friend nhận đúng 3 lần, mỗi lần tại 1 mốc\n"
       "- Sau mỗi mốc, dòng tương ứng chuyển từ「配信予約」sang「配信履歴」\n"
       "- Các mốc chưa tới giờ vẫn ở tab「配信予約」",
       env="PRODUCTION",
       note="Nguồn: r48-r59 + file 03/tab function r181-r191. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job gửi & vòng đời trạng thái", "JOB-001", "Normal",
       "Job gửi cho broadcast có filter — chỉ friend thỏa điều kiện nhận được",
       L + "\n- Bot có 10 bạn bè, 4 người có tag T\n- Broadcast filter tag T, đặt lịch sau 5 phút",
       "1. Chờ job gửi\n"
       "2. Kiểm tra app LINE của cả 10 bạn bè\n"
       "3. Đọc 配信数 ở tab「配信履歴」\n"
       "4. Bấm vào số để xem danh sách friend đã gửi",
       "10 bạn bè, 4 người tag T",
       "- Đúng 4 friend có tag T nhận được tin\n"
       "- 6 friend còn lại KHÔNG nhận được\n"
       "- 配信数 = 4, danh sách friend đúng 4 người đó",
       env="PRODUCTION",
       note="Nguồn: Improve chung/tab「Move job send all」r4, r6 + r25. RULE-06 + RULE-07.",
       group="API"),

    tc("Job gửi & vòng đời trạng thái", "JOB-001", "Normal",
       "Job gửi cho broadcast KHÔNG filter — toàn bộ bạn bè nhận được",
       L + "\n- Bot có 10 bạn bè, 2 người đã block\n- Broadcast không filter, đặt lịch sau 5 phút",
       "1. Chờ job gửi\n"
       "2. Kiểm tra app LINE của 8 friend chưa block\n"
       "3. Đọc 配信数 ở tab「配信履歴」\n"
       "4. Kiểm tra bảng message_error có bản ghi cho 2 người block không",
       "10 bạn bè, 2 người is_blocked = 1",
       "- 8 friend chưa block đều nhận được tin\n"
       "- 2 friend đã block KHÔNG nhận được, không làm hỏng lượt gửi của người khác\n"
       "- 配信数 phản ánh số thực gửi",
       env="PRODUCTION",
       note="Nguồn: Improve chung/tab「Move job send all」r3, r5 + file 03/tab function r174 "
            "(『check chặn friend — bảng bot_line_user: is_blocked=1』). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job gửi & vòng đời trạng thái", "DATA-001", "Normal",
       "Status 'delivered' nghĩa là ĐÃ ĐƯA VÀO HÀNG ĐỢI, không phải LINE đã xác nhận gửi xong",
       L + "\n- Broadcast gửi cho ≥500 friend, đặt lịch sau 5 phút",
       "1. Chờ tới giờ gửi\n"
       "2. Ngay khi status chuyển thành 'delivered', ghi lại thời điểm\n"
       "3. Tiếp tục theo dõi app LINE của các friend cuối danh sách\n"
       "4. Ghi lại thời điểm friend cuối cùng thực sự nhận được tin",
       "500 friend nhận",
       "- Status 'delivered' xuất hiện TRƯỚC khi friend cuối cùng nhận được tin\n"
       "- Ghi rõ độ trễ giữa 2 thời điểm để làm căn cứ đánh giá\n"
       "- Cuối cùng tất cả friend đều nhận được",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: feature-spec.md §7 (『status='delivered' được set ngay sau khi đẩy hết requests vào "
            "in-memory queue — KHÔNG phải sau khi LINE API xác nhận gửi xong』) + §9 M-02 (『có thể gây "
            "hiểu nhầm cho tester』). ⚠️ MT-19 — tester dễ kết luận sai『đã gửi xong』. "
            "RULE-08: job nền + hiệu năng → PRODUCTION.",
       group="API"),

    tc("Job gửi & vòng đời trạng thái", "PERF-LARGE-001", "Boundary",
       "Gửi broadcast quy mô lớn — không timeout, không sót friend",
       L + "\n- Bot có số bạn bè ở quy mô lớn nhất của khách hàng thực tế",
       "1. Tạo broadcast gửi cho toàn bộ bạn bè, đặt lịch\n"
       "2. Ghi lại thời điểm bắt đầu và kết thúc job\n"
       "3. So sánh 配信数 với tổng số bạn bè không bị block\n"
       "4. Kiểm tra bảng message_error xem có lỗi hàng loạt không\n"
       "5. Lấy mẫu ngẫu nhiên 10 friend kiểm tra app LINE",
       "Toàn bộ bạn bè của bot lớn nhất",
       "- Job chạy xong, không bị treo hoặc restart giữa chừng\n"
       "- 配信数 = tổng bạn bè không block, không sót ai\n"
       "- 10 friend lấy mẫu đều nhận đủ tin\n"
       "- Không có lỗi hàng loạt trong message_error",
       env="PRODUCTION",
       note="Nguồn: job-spec.md §Concurrency (『Nếu 1 bot job treo > 30 phút → System.exit(0)』). "
            "RULE-08: performance + job nền → bắt buộc PRODUCTION.",
       group="API"),

    # ═══════════ 25. Job — quá hạn, lỗi & resume ═══════════
    tc("Job — quá hạn, lỗi & resume", "JOB-001", "Boundary",
       "Broadcast quá hạn DƯỚI 15 phút — vẫn gửi bình thường",
       "- Có quyền sửa DB trên môi trường test\n- Có broadcast đã chạy trong DB để làm mẫu",
       "1. Sửa 1 broadcast trong DB: đặt send_time và updated_at nhỏ hơn hiện tại 5 phút, "
       "status = 'wait_to_send'\n"
       "2. Chờ job poll (≤ 1 phút)\n"
       "3. Kiểm tra app LINE của friend nhận\n"
       "4. Đọc status của broadcast\n"
       "5. Lặp lại với mốc nhỏ hơn hiện tại 14 phút",
       "Mốc quá hạn: 5 phút · 14 phút (đều dưới ngưỡng 15 phút)",
       "- Cả 2 mốc: job vẫn gửi bình thường\n"
       "- Friend nhận được tin\n"
       "- Status chuyển sang 'delivered'",
       env="PRODUCTION",
       note="Nguồn: file 03/tab「broadcaset」r6-r7 (18/09/2024 — 『Broadcase quá giờ sẽ không gửi mà hiện "
            "msg lỗi』). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — quá hạn, lỗi & resume", "JOB-001", "Boundary",
       "Broadcast quá hạn TỪ 15 phút trở lên — KHÔNG gửi, chuyển sang lỗi",
       "- Có quyền sửa DB trên môi trường test",
       "1. Sửa 1 broadcast trong DB: send_time và updated_at nhỏ hơn hiện tại 15 phút, "
       "status = 'wait_to_send'\n"
       "2. Chờ job poll\n"
       "3. Kiểm tra app LINE của friend nhận\n"
       "4. Đọc status và nội dung hiển thị ở tab「配信履歴」\n"
       "5. Lặp lại với mốc quá hạn 30 phút",
       "Mốc quá hạn: 15 phút · 30 phút",
       "- Cả 2 mốc: friend KHÔNG nhận được tin\n"
       "- Status chuyển sang 'send_false'\n"
       "- Ở tab「配信履歴」hiển thị thông báo dưới tên broadcast: "
       "「配信できませんでした。配信スケジュールを再度設定してください。」",
       env="PRODUCTION",
       note="Nguồn: file 03/tab「broadcaset」r8-r10 + feature-spec.md §5 BR-11 (『nếu sendTime + 15 phút "
            "< NOW() VÀ updatedAt + 15 phút < NOW() → set send_false』). RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — quá hạn, lỗi & resume", "JOB-001", "Boundary",
       "Chỉ send_time quá hạn nhưng updated_at mới — vẫn gửi (điều kiện AND)",
       "- Có quyền sửa DB trên môi trường test",
       "1. Sửa 1 broadcast: send_time nhỏ hơn hiện tại 30 phút NHƯNG updated_at = hiện tại, "
       "status = 'wait_to_send'\n"
       "2. Chờ job poll\n"
       "3. Kiểm tra app LINE và status",
       "send_time quá hạn 30 phút · updated_at = hiện tại",
       "- Job VẪN gửi (vì điều kiện quá hạn là AND của cả 2 trường)\n"
       "- Friend nhận được tin, status = 'delivered'",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: feature-spec.md §5 BR-11 (điều kiện dùng『VÀ』). ⚠️ Corpus chỉ test trường hợp CẢ HAI "
            "cùng quá hạn (broadcaset r6-r9) — nhánh chỉ 1 trường quá hạn CHƯA được test. TC do AI bổ "
            "sung từ spec, cần Leader xác nhận. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — quá hạn, lỗi & resume", "MSG-005", "Abnormal",
       "Broadcast có filter hỏng dữ liệu — không gửi, ghi lỗi rõ ràng",
       "- Có quyền sửa DB trên môi trường test\n- Có broadcast wait_to_send với filter hợp lệ",
       "1. Sửa dữ liệu filter_v2 của broadcast thành cấu trúc lỗi "
       "(VD đổi status_chat_filter_type từ số thành chuỗi rỗng)\n"
       "2. Chờ job tới giờ gửi\n"
       "3. Kiểm tra app LINE của friend\n"
       "4. Đọc status và bảng message_error",
       "filters_v2.data: {\"active\":true,\"status_chat_filter_type\":0,\"status_chat_search\":[4046]} "
       "→ đổi status_chat_filter_type thành \"\"",
       "- Job KHÔNG gửi cho ai\n"
       "- Status chuyển sang 'send_false' (không treo ở 'delivering')\n"
       "- Ghi lỗi vào bảng message_error, không làm job crash toàn bộ service",
       env="PRODUCTION",
       note="Nguồn: file 03/tab「broadcaset」r11 (『bản ghi mới, sửa cho lỗi không send được』). "
            "RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — quá hạn, lỗi & resume", "JOB-001", "Abnormal",
       "Service job restart giữa chừng — resume từ friend cuối cùng đã gửi",
       "- Broadcast đang gửi cho ≥200 friend\n- Có quyền restart service job trên môi trường test",
       "1. Bắt đầu gửi broadcast cho 200 friend\n"
       "2. Khi đang gửi (status = 'delivering'), restart service job\n"
       "3. Chờ service khởi động lại\n"
       "4. Kiểm tra app LINE của toàn bộ 200 friend\n"
       "5. Đọc 配信数 cuối cùng",
       "200 friend, restart giữa chừng",
       "- Job tự tìm broadcast đang 'delivering' và tiếp tục từ friend cuối cùng đã gửi\n"
       "- Không friend nào bị GỬI TRÙNG 2 lần\n"
       "- Không friend nào bị BỎ SÓT\n"
       "- 配信数 cuối = 200",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: feature-spec.md §7 (『Khi service khởi động lại, BroadcastTask tự tìm broadcasts đang "
            "delivering và resume từ user cuối cùng đã gửi』). ⚠️ Corpus KHÔNG có TC cho nhánh này — "
            "TC do AI bổ sung từ spec, cần Leader xác nhận cách restart an toàn. "
            "RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — quá hạn, lỗi & resume", "MSG-005", "Abnormal",
       "LINE API rate limit — job retry và cuối cùng vẫn gửi được",
       "- Broadcast gửi cho số lượng friend đủ lớn để chạm rate limit của LINE API",
       "1. Gửi broadcast cho lượng friend lớn trong thời gian ngắn\n"
       "2. Theo dõi log job xem có lỗi rate limit không\n"
       "3. Sau khi job kết thúc, kiểm tra 配信数 và mẫu 10 friend\n"
       "4. Đọc bảng message_error",
       "Số friend đủ lớn để chạm rate limit",
       "- Khi gặp rate limit, job đẩy request vào hàng đợi retry, chờ 3 giây, thử lại tối đa 10 lần\n"
       "- Sau retry, friend vẫn nhận được tin\n"
       "- Chỉ ghi message_error cho những trường hợp thất bại sau 10 lần retry",
       env="PRODUCTION",
       note="Nguồn: job-spec.md:311, 557 (『Status 1000 (rate limit) → đẩy lại retryRequestQueue, "
            "chờ 3s, max 10 lần』). RULE-08: job nền + performance → PRODUCTION.",
       group="API"),

    # ═══════════ 26. Job — action sau khi gửi ═══════════
    tc("Job — action sau khi gửi", "MSG-004", "Normal",
       "Action đổi rich menu chạy sau khi gửi — rich menu của friend đổi đúng",
       L + "\n- Bot có rich menu R1 (đang hiển thị) và R2\n- Broadcast có action đổi sang rich menu R2",
       "1. Xác nhận friend đang thấy rich menu R1 trong app LINE\n"
       "2. Đặt lịch gửi broadcast có action đổi sang R2\n"
       "3. Chờ job gửi xong\n"
       "4. Mở app LINE của friend, quan sát rich menu",
       "Rich menu R1 → R2",
       "- Sau khi nhận tin, rich menu của friend đổi thành R2\n"
       "- Bảng bot_line_user: rich menu id cập nhật thành R2",
       env="PRODUCTION",
       note="Nguồn: r783, r789, r795, r800 (khối CHECK COVER CASE CŨ). RULE-06: verify tới app LINE. "
            "RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — action sau khi gửi", "MSG-004", "Normal",
       "Action xóa rich menu chạy sau khi gửi — friend không còn rich menu",
       L + "\n- Friend đang có rich menu R1\n- Broadcast có action xóa rich menu",
       "1. Xác nhận friend đang thấy rich menu R1\n"
       "2. Đặt lịch gửi broadcast có action xóa rich menu\n"
       "3. Chờ job gửi xong\n"
       "4. Mở app LINE của friend, quan sát khu vực rich menu",
       "Action「リッチメニュー削除」",
       "- Sau khi nhận tin, friend KHÔNG còn thấy rich menu\n"
       "- Bảng bot_line_user: rich menu id được xóa/null",
       env="PRODUCTION",
       note="Nguồn: r784, r790, r796, r801. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — action sau khi gửi", "MSG-004", "Normal",
       "Action trigger step (ステップ) sau khi gửi — có filter và không filter",
       L + "\n- Đã tạo 1 scenario S có bước gửi ngay",
       "1. Tạo broadcast có action trigger scenario S, chọn「絞り込みなし」\n"
       "2. Chờ job gửi xong, kiểm tra app LINE: friend nhận tin broadcast rồi nhận tin của scenario S\n"
       "3. Lặp lại với action trigger scenario S nhưng chọn「絞り込みあり」điều kiện có tag T",
       "Scenario S · action 絞り込みなし và 絞り込みあり (tag T)",
       "- Với 絞り込みなし: mọi friend nhận tin đều được trigger scenario S\n"
       "- Với 絞り込みあり: chỉ friend có tag T được trigger scenario S\n"
       "- Bảng theo dõi scenario ghi nhận đúng danh sách friend được trigger",
       env="PRODUCTION",
       note="Nguồn: file 03/tab function r176-r177. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — action sau khi gửi", "MSG-004", "Normal",
       "Action trigger remind (リマインド) sau khi gửi — có filter và không filter",
       L + "\n- Đã tạo 1 remind R",
       "1. Tạo broadcast có action trigger remind R, chọn「絞り込みなし」\n"
       "2. Chờ job gửi xong, kiểm tra friend đã được đăng ký vào remind R chưa\n"
       "3. Lặp lại với「絞り込みあり」điều kiện có tag T",
       "Remind R · action 絞り込みなし và 絞り込みあり (tag T)",
       "- Với 絞り込みなし: mọi friend nhận tin đều được đăng ký remind R\n"
       "- Với 絞り込みあり: chỉ friend có tag T được đăng ký\n"
       "- Đến giờ remind, đúng nhóm friend đó nhận được tin nhắn nhắc",
       env="PRODUCTION",
       note="Nguồn: file 03/tab function r178-r179. RULE-08: job nền → PRODUCTION.",
       group="API"),

    tc("Job — action sau khi gửi", "DATA-001", "Normal",
       "Friend được tích quick reply mới — cờ quick reply của bản cũ bị gỡ",
       L + "\n- Bot có friend F1 đang là quick tester",
       "1. Kiểm tra bảng bot_line_user: F1 có is_quick_reply = 1\n"
       "2. Tích chọn friend F2 làm quick tester (khi đã đủ 3 hoặc thay thế F1)\n"
       "3. Đọc lại is_quick_reply của F1 và F2",
       "F1 đang là quick tester, chuyển sang F2",
       "- F2: is_quick_reply = 1\n"
       "- F1: is_quick_reply = 0 (bị gỡ, không giữ cờ cũ)",
       note="Nguồn: file 03/tab function r175 (『check khi tích chọn quick reply mới — bảng bot_line_user: "
            "is_quick_reply của thằng cũ = 0』).",
       group="Data"),
]
