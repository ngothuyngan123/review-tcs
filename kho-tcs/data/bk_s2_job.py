# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 9-10: job nền BackupBotTask, vòng đời trạng thái,
và các tình huống copy đồng thời / liên tiếp.

Toàn bộ nhóm này đặt Môi trường test = PRODUCTION theo RULE-08 (job nền + race condition).
"""
from _common import tc

JOB = ("- Job nền BackupBotTask đang bật (cờ ENABLE_BACKUP_BOT = true)\n"
       "- Đăng nhập Admin bot A (plan Standard/Pro), biết mã copy của bot B\n"
       "- Có quyền xem trạng thái bản ghi backup ở phía máy chủ để đối chiếu")
P = "PRODUCTION"

S2 = [
    # ═══════════════ 9. Job BackupBotTask & state machine ═══════════════
    tc("Job BackupBotTask & state machine", "JOB-001", "Normal",
       "Job nhặt yêu cầu mới và đưa vào hàng đợi trong vài giây",
       JOB,
       "1. Từ bot A, bấm「データコピーを開始」sang bot B\n"
       "2. Bấm đồng hồ bấm giờ ngay lúc bấm\n"
       "3. Theo dõi trạng thái bản ghi vừa tạo mỗi 1 giây trong 10 giây đầu\n"
       "4. Ghi lại mốc thời gian trạng thái đổi từ「chờ」sang「đã vào hàng đợi」",
       "Bấm giờ, ghi log mỗi 1 giây",
       "- Trạng thái chuyển từ chờ (0) sang đã-vào-hàng-đợi (4) trong vòng 2–3 giây\n"
       "- Không có bản ghi nào bị bỏ sót\n"
       "- Thời điểm cập nhật của bản ghi được ghi lại mỗi lần đổi trạng thái",
       env=P,
       note="Nguồn: [MN]Job TCs r2 (TC-BK-062) — threadPollQueue poll mỗi 2 giây. TC hồi quy FA-033."),

    tc("Job BackupBotTask & state machine", "JOB-001", "Normal",
       "Job thực hiện copy và đi hết vòng đời trạng thái tới hoàn tất",
       JOB + "\n- Bot A có sẵn dữ liệu của cả 13 loại được copy",
       "1. Bấm bắt đầu copy A → B\n"
       "2. Ghi lại từng lần trạng thái đổi cho tới khi kết thúc\n"
       "3. Sau khi xong, mở màn tag / template / scenario của bot B để đối chiếu",
       "Bot A: ≥5 tag, ≥5 template, ≥2 scenario, ≥2 form, ≥1 richmenu",
       "- Trạng thái đi đúng: đã-vào-hàng-đợi → đang-thực-hiện → hoàn-tất\n"
       "- Sau khi hoàn tất, dữ liệu của cả 5 loại trên xuất hiện đầy đủ ở bot B\n"
       "- KHÔNG có thông báo lỗi nào gửi lên Chatwork",
       env=P,
       note="Nguồn: [MN]Job TCs r4 (TC-BK-064). TC hồi quy FA-033."),

    tc("Job BackupBotTask & state machine", "JOB-001", "Abnormal",
       "Khởi động lại dịch vụ job giữa chừng — công việc đang trong hàng đợi vẫn chạy tiếp",
       JOB + "\n- Có thể khởi động lại dịch vụ job trên môi trường test",
       "1. Tạo yêu cầu copy, chờ tới khi trạng thái là đã-vào-hàng-đợi\n"
       "2. Khởi động lại dịch vụ job\n"
       "3. Theo dõi trạng thái bản ghi trong 5 phút sau đó\n"
       "4. Kiểm tra dữ liệu ở bot B",
       "1 bản ghi đang ở hàng đợi lúc restart",
       "- Ngay khi dịch vụ khởi động lại, bản ghi được nạp lại vào hàng đợi\n"
       "- Trạng thái tiếp tục đi tới đang-thực-hiện rồi hoàn-tất (hoặc thất bại)\n"
       "- KHÔNG bị kẹt vĩnh viễn ở trạng thái hàng đợi\n"
       "- Dữ liệu ở bot B KHÔNG bị nhân đôi (không xử lý 2 lần)",
       env=P,
       note="Nguồn: [MN]Job TCs r3 (TC-BK-063). TC hồi quy FA-033 — cơ chế recovery."),

    tc("Job BackupBotTask & state machine", "JOB-001", "Abnormal",
       "Job gặp lỗi giữa chừng — chuyển sang trạng thái thất bại và báo Chatwork",
       JOB + "\n- Dựng được tình huống lỗi (nhờ Dev)\n- Có quyền xem phòng Chatwork nhận cảnh báo",
       "1. Tạo yêu cầu copy trên dữ liệu gây lỗi\n"
       "2. Theo dõi trạng thái bản ghi\n"
       "3. Mở phòng Chatwork nhận cảnh báo và tìm thông báo mới\n"
       "4. Theo dõi tiếp 10 phút xem có tự chạy lại không",
       "Dữ liệu nguồn có bản ghi hỏng",
       "- Trạng thái chuyển sang thất bại\n"
       "- Có thông báo lỗi gửi vào phòng Chatwork [To:6395420]\n"
       "- KHÔNG tự chạy lại — thất bại là trạng thái cuối\n"
       "- Bảng lịch sử ở màn admin phản ánh đúng (xem MT-03 về nhãn hiển thị)",
       env=P,
       note="Nguồn: [MN]Job TCs r6 (TC-BK-066). TC hồi quy FA-033."),

    tc("Job BackupBotTask & state machine", "JOB-001", "Abnormal",
       "Tắt cờ bật job — yêu cầu copy nằm im, không có gì xảy ra",
       "- Có thể sửa cấu hình và khởi động lại dịch vụ job trên môi trường test\n"
       "- Đăng nhập Admin bot A, biết mã copy bot B",
       "1. Tắt cờ ENABLE_BACKUP_BOT, khởi động lại dịch vụ job\n"
       "2. Từ bot A bấm bắt đầu copy sang bot B\n"
       "3. Đứng ở màn xử lý và theo dõi 30 giây\n"
       "4. Kiểm tra dữ liệu bot B",
       "Cờ = false",
       "- Trạng thái bản ghi đứng yên ở chờ suốt 30 giây\n"
       "- Thanh tiến trình đứng ở 0%, không bao giờ hiện modal hoàn tất\n"
       "- Bot B KHÔNG nhận được dữ liệu nào\n"
       "- Nhật ký dịch vụ job không có dòng nào liên quan BackupBotTask",
       env=P,
       note="Nguồn: [MN]Job TCs r7 (TC-BK-067). TC hồi quy FA-033 — cần chạy trước mỗi lần release."),

    tc("Job BackupBotTask & state machine", "STATE-DEP-001", "Abnormal",
       "Vòng đời trạng thái không có bước nhảy bất hợp lệ",
       JOB + "\n- Ghi lại được toàn bộ lịch sử đổi trạng thái của bản ghi",
       "1. Thực hiện 3 lần copy: 1 lần thành công, 1 lần thất bại, 1 lần khởi động lại giữa chừng\n"
       "2. Với mỗi lần, ghi lại dãy trạng thái đầy đủ\n"
       "3. Đối chiếu với vòng đời cho phép",
       "3 kịch bản khác nhau",
       "- Chỉ có 2 dãy hợp lệ: chờ → hàng đợi → đang chạy → hoàn tất, "
       "hoặc chờ → hàng đợi → đang chạy → thất bại\n"
       "- Không có bước lùi (hoàn tất → đang chạy, thất bại → hàng đợi)\n"
       "- Không nhảy cóc (chờ → hoàn tất, hàng đợi → hoàn tất)\n"
       "- Không xuất hiện giá trị trạng thái ngoài 5 giá trị đã định nghĩa",
       env=P,
       note="Nguồn: [MN]Job TCs r9 (TC-BK-076). TC hồi quy FA-033 — chốt state machine."),

    tc("Job BackupBotTask & state machine", "DATA-ID-001", "Normal",
       "Job ghi lại bảng ánh xạ id cũ → id mới cho từng bản ghi đã copy",
       JOB,
       "1. Ghi lại id của 3 tag, 3 template ở bot A trước khi copy\n"
       "2. Thực hiện copy A → B\n"
       "3. Sau khi xong, mở màn tag / template ở bot B và ghi lại id mới\n"
       "4. Verify bổ sung: đối chiếu bảng ánh xạ `backup_new_id`",
       "3 tag + 3 template, ghi rõ id",
       "- Mọi bản ghi đã copy đều có 1 dòng ánh xạ id cũ → id mới\n"
       "- Dòng ánh xạ ghi đúng bot gửi và bot nhận\n"
       "- id mới KHÔNG trùng id cũ",
       env=P,
       note="Nguồn: [MN]Job TCs r4 (TC-BK-064) + r8 (TC-BK-075); feature-spec §7.4."),

    tc("Job BackupBotTask & state machine", "DATA-REF-001", "Abnormal",
       "Bản ghi tham chiếu không còn tồn tại khi copy — bỏ qua chứ không làm hỏng cả job",
       JOB + "\n- Ở bot A có 1 action trỏ tới bản ghi đã bị xoá cứng (nhờ Dev dựng)",
       "1. Dựng dữ liệu có tham chiếu treo ở bot A\n"
       "2. Thực hiện copy A → B\n"
       "3. Theo dõi trạng thái tới khi kết thúc\n"
       "4. Kiểm tra dữ liệu bot B",
       "1 tham chiếu treo",
       "- Job KHÔNG dừng giữa chừng vì 1 bản ghi hỏng\n"
       "- Bản ghi hỏng bị bỏ qua, có ghi nhật ký và có thông báo Chatwork\n"
       "- Các dữ liệu còn lại vẫn copy đủ sang bot B\n"
       "- Trạng thái cuối cùng vẫn là hoàn tất",
       env=P,
       note="Nguồn: feature-spec §2.2 bảng luồng lỗi (cloneRow → result.wasNull → log + notify + skip). "
            "Corpus KHÔNG có TC này — do AI bổ sung để phủ nhánh lỗi spec mô tả. Cần Leader duyệt."),

    tc("Job BackupBotTask & state machine", "CONC-002", "Normal",
       "Hai luồng xử lý chạy song song 2 yêu cầu copy khác nhau",
       JOB + "\n- Có 4 bot: A→B và C→D, hoàn toàn không giao nhau",
       "1. Từ bot A bấm copy sang B\n"
       "2. Trong vòng 5 giây, từ bot C bấm copy sang D\n"
       "3. Theo dõi trạng thái cả 2 bản ghi\n"
       "4. Sau khi xong, kiểm tra dữ liệu ở B và D",
       "A→B và C→D, mỗi bot nguồn có ≥5 tag + ≥3 template khác tên nhau",
       "- Cả 2 yêu cầu đều được xử lý, không cái nào bị bỏ\n"
       "- Bot B chỉ nhận dữ liệu của A, bot D chỉ nhận dữ liệu của C — KHÔNG lẫn lộn\n"
       "- Không có tag/template nào của A xuất hiện ở D và ngược lại",
       env=P,
       note="Nguồn: feature-spec §7.3 (2 worker threadBackup). Corpus có TC gần nhất là [AI]UI r39 "
            "(TC-BK-038 backup liên tiếp). TC cách ly chéo do AI bổ sung — cần Leader duyệt."),

    tc("Job BackupBotTask & state machine", "REG-RUN-001", "Normal",
       "Job vẫn chạy đúng sau khi giao diện và API đổi",
       JOB + "\n- Môi trường đã triển khai bản có màn xử lý mới và các endpoint mới",
       "1. Thực hiện 1 lần copy đầy đủ trên bản mới\n"
       "2. Ghi lại dãy trạng thái và thời gian mỗi bước\n"
       "3. So sánh với dãy trạng thái của bản cũ (nếu có số liệu)\n"
       "4. Kiểm tra bảng ánh xạ id sau khi xong",
       "1 lần copy đầy đủ trên bản mới",
       "- Chu kỳ nhặt việc vẫn ~2 giây như bản cũ\n"
       "- Dãy trạng thái giữ nguyên, không có bước lạ\n"
       "- Bảng ánh xạ id vẫn được ghi đầy đủ\n"
       "- Không có tác dụng phụ nào từ việc thêm màn xử lý và endpoint mới",
       env=P,
       spec="Đã hỏi leader",
       note="MT-00 — [MN]Job TCs r8 (TC-BK-075). Chỉ chạy được sau khi Leader chốt MT-00."),

    # ═══════════════ 10. Backup đồng thời & liên tiếp ═══════════════
    tc("Backup đồng thời & liên tiếp", "FUNC-SEQ-001", "Normal",
       "Copy liên tiếp 3 lần cùng một cặp bot — cả 3 lần đều ghi nhận",
       JOB,
       "1. Thực hiện copy A → B lần 1, chờ hoàn tất\n"
       "2. Thực hiện copy A → B lần 2, chờ hoàn tất\n"
       "3. Thực hiện copy A → B lần 3, chờ hoàn tất\n"
       "4. Mở tab「コピー履歴」và kiểm tra dữ liệu ở bot B",
       "3 lần liên tiếp, mỗi lần chờ xong mới làm tiếp",
       "- Cả 3 lần đều hoàn tất, bảng lịch sử có đủ 3 dòng\n"
       "- Ghi rõ dữ liệu ở bot B sau 3 lần: bị nhân 3 hay bị ghi đè (đây là điểm cần Leader xác nhận)\n"
       "- Tải file CSV lịch sử (nếu có) vẫn tải được bình thường",
       env=P,
       spec="Đã hỏi leader",
       note="Nguồn: [AI]UI r39 (TC-BK-038) — nguyên văn「Backup all cả 3 lần, hiển thị đủ cross backup, "
            "hiển thị kết quả bình thuownfgh. download csv bình thường」. ⚠️ TC gốc KHÔNG nói dữ liệu ở bot đích "
            "sau 3 lần ra sao — đây là rủi ro nhân bản dữ liệu, cần Leader chốt."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Hai LOA nguồn khác nhau cùng copy vào MỘT LOA đích khi job đang chạy",
       JOB + "\n- Có 3 bot: A, C (nguồn) và B (đích)\n- Dữ liệu ở A và C khác tên nhau rõ rệt",
       "1. Từ bot A bấm copy sang B\n"
       "2. Trong khi trạng thái còn đang xử lý, mở tab khác, từ bot C bấm copy sang B\n"
       "3. Quan sát phản hồi ở bước 2\n"
       "4. Chờ tất cả kết thúc, kiểm tra dữ liệu ở bot B",
       "A có tag 「A-tag-01..05」, C có tag「C-tag-01..05」",
       "- Kết quả theo quyết định MT-06:\n"
       "  · nếu chốt CHẶN: bước 2 báo lỗi, bot B chỉ nhận dữ liệu của A\n"
       "  · nếu chốt CHO PHÉP: bot B nhận đủ 10 tag của cả A và C, không mất bản ghi nào\n"
       "- Trong mọi trường hợp: KHÔNG có bản ghi bị mất hay bị ghi đè im lặng",
       env=P,
       spec="Đã hỏi leader",
       note="MT-06 — [AI]UI r37 (TC-BK-036) nói cho phép cả 2, r38 (TC-BK-037) nói chỉ 1 cái chạy được. "
            "Hai TC gốc mâu thuẫn nhau. KHÔNG giao member cho tới khi Leader chốt."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Hai tab cùng lúc: mỗi tab dùng một mã copy khác nhau của cùng một LOA",
       JOB + "\n- Có 3 bot: bot 1, bot 3 (nguồn) và bot 2 (đích)",
       "1. Ở tab 1: từ bot 1 xác nhận mã A của bot 2, dừng trước khi bấm bắt đầu\n"
       "2. Ở bot 2: phát hành lại mã, được mã B\n"
       "3. Ở tab 2: từ bot 3 xác nhận mã B của bot 2 và bấm bắt đầu copy\n"
       "4. Quay lại tab 1 bấm bắt đầu copy với mã A",
       "Mã A (cũ) và mã B (mới) của cùng bot 2",
       "- Yêu cầu ở tab 2 (mã B) được chấp nhận\n"
       "- Yêu cầu ở tab 1 (mã A đã cũ) BỊ TỪ CHỐI kèm thông báo lỗi mã không tồn tại\n"
       "- Bot 2 chỉ nhận dữ liệu của bot 3",
       env=P,
       spec="Đã hỏi leader",
       note="MT-06 — [AI]UI r38 (TC-BK-037) nguyên văn「Chỉ backup đc từ bot 3 sang bot 2, mã cũ sẽ hiển thị msg lỗi」. "
            "Mâu thuẫn với r37. Cần chốt cùng MT-06."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Một LOA nguồn copy sang 2 LOA đích khác nhau gần như cùng lúc",
       JOB + "\n- Có bot A (nguồn) và bot B, bot D (2 đích)",
       "1. Từ bot A bấm copy sang B\n"
       "2. Trong khi đang xử lý, từ bot A (tab khác) bấm copy sang D\n"
       "3. Quan sát phản hồi ở bước 2\n"
       "4. Chờ xong, kiểm tra dữ liệu ở cả B và D",
       "Bot A có ≥5 tag + ≥3 template",
       "- Ghi rõ hệ thống cho phép hay chặn yêu cầu thứ 2\n"
       "- Nếu cho phép: cả B và D đều nhận ĐỦ dữ liệu của A, không cái nào thiếu\n"
       "- Dữ liệu ở B và D độc lập — sửa ở B không ảnh hưởng D",
       env=P,
       spec="Đã hỏi leader",
       note="MT-06 — [AI]UI r40 (TC-BK-039) nguyên văn「Backup được cả bot A và B, lưu db: backup_history」. "
            "Liên quan BK-Q10 mà spec tự nhận chưa xác nhận."),

    tc("Backup đồng thời & liên tiếp", "CONC-003", "Abnormal",
       "Bấm「データコピーを開始」2 lần trong dưới 1 giây",
       JOB + "\n- Đã xác nhận mã, modal xác nhận đang mở",
       "1. Ghi lại số dòng ở tab「コピー履歴」\n"
       "2. Bấm「データコピーを開始」rồi bấm thêm lần nữa ngay lập tức (dưới 1 giây)\n"
       "3. Chờ tất cả kết thúc\n"
       "4. Đếm lại số dòng lịch sử và kiểm tra dữ liệu ở bot B",
       "2 lần bấm cách nhau <1 giây",
       "- Kết quả theo quyết định MT-26:\n"
       "  · nếu CÓ chặn: chỉ tăng 1 dòng, lần 2 báo lỗi\n"
       "  · nếu KHÔNG chặn: tăng 2 dòng và dữ liệu ở bot B BỊ NHÂN ĐÔI\n"
       "- Bắt buộc ghi rõ dữ liệu ở bot B có bị nhân đôi không",
       env=P,
       spec="Đã hỏi leader",
       note="MT-26 — [AI]API r24 (TC-BK-056) ghi rõ「phụ thuộc QA-010 chưa có answer」. "
            "Đây là rủi ro nhân bản dữ liệu, ưu tiên chốt sớm."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Đổi mã copy của LOA kia trong khi job đang chạy",
       JOB,
       "1. Từ bot A bấm copy sang B, chờ tới khi trạng thái là đang thực hiện\n"
       "2. Đăng nhập bot B, thử phát hành lại mã copy\n"
       "3. Quan sát phản hồi\n"
       "4. Chờ job kết thúc, kiểm tra dữ liệu bot B",
       "—",
       "- Bước 3: theo quyết định MT-01 — nếu bot B là bên đang nhận thì thao tác phát hành lại phải BỊ CHẶN "
       "kèm thông báo「バックアップ処理中のため、コードの再発行はできません。」\n"
       "- Job đang chạy KHÔNG bị hỏng dở dang\n"
       "- Dữ liệu ở bot B đầy đủ như bình thường",
       env=P,
       spec="Đã hỏi leader",
       note="MT-01 + MT-06 — ghép từ [AI]UI r7 (TC-BK-006) và r35 (TC-BK-034). "
            "Corpus không có TC nào thử đổi mã KHI job đã chạy."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Thao tác ghi dữ liệu trên LOA ĐANG NHẬN trong lúc copy",
       JOB + "\n- Đang có backup vào bot B ở trạng thái đang thực hiện",
       "1. Trong lúc job đang chạy, đăng nhập bot B\n"
       "2. Thử tạo mới 1 popup\n"
       "3. Thử tạo mới 1 sự kiện đặt lịch\n"
       "4. Thử sửa 1 richmenu\n"
       "5. Thử tạo mới 1 tag và 1 template",
       "5 thao tác ghi ở 5 màn khác nhau",
       "- Bước 2, 3, 4: bị chặn kèm thông báo tương ứng (3 màn spec đã liệt kê)\n"
       "- Bước 5: ghi lại kết quả thực tế — spec KHÔNG liệt kê tag/template trong danh sách bị chặn, "
       "cần đối chiếu với quyết định MT-08\n"
       "- Không có thao tác nào gây lỗi 500 hay làm hỏng job đang chạy",
       env=P,
       spec="Đã hỏi leader",
       note="MT-08 — feature-spec §8.2 chỉ liệt kê 3 nơi bị chặn (Popup / Event / RichMenu). "
            "Bước 5 là để kiểm tra danh sách đó đã đủ chưa. Corpus không có TC cho phần này."),

    tc("Backup đồng thời & liên tiếp", "CONC-001", "Abnormal",
       "Thao tác ghi dữ liệu trên LOA ĐANG GỬI trong lúc copy",
       JOB + "\n- Đang có backup từ bot A ở trạng thái đang thực hiện",
       "1. Trong lúc job đang chạy, ở bot A thử sửa tên 1 tag đang được copy\n"
       "2. Thử xoá 1 template đang được copy\n"
       "3. Thử tạo mới 1 scenario\n"
       "4. Chờ job kết thúc, đối chiếu dữ liệu ở bot B với bot A",
       "Sửa/xoá đúng bản ghi đang trong tầm copy",
       "- Theo spec §8.2 thì LOA gửi KHÔNG bị chặn — các thao tác trên đều thực hiện được\n"
       "- Ghi rõ dữ liệu ở bot B nhận được là bản TRƯỚC hay SAU khi sửa\n"
       "- Job KHÔNG bị lỗi vì bản ghi nguồn bị xoá giữa chừng\n"
       "- Đối chiếu với cảnh báo trên UI ở MT-08 (UI nói cả 2 phía đều bị khoá)",
       env=P,
       spec="Đã hỏi leader",
       note="MT-08 — mâu thuẫn thẳng giữa feature-spec §8.2 (chỉ khoá LOA đích) và cảnh báo vàng ở "
            "[AI]UI r32 (khoá cả 2 phía). TC này để đo hiện trạng thật."),

    tc("Backup đồng thời & liên tiếp", "PERF-LARGE-001", "Boundary",
       "Copy LOA có khối lượng dữ liệu lớn — đo thời gian hoàn tất",
       JOB + "\n- Bot A có khối lượng dữ liệu lớn (xem cột dữ liệu test)",
       "1. Ghi lại thời điểm bấm bắt đầu copy\n"
       "2. Theo dõi tới khi hoàn tất, ghi lại thời điểm kết thúc\n"
       "3. Tính thời gian chạy\n"
       "4. Đối chiếu số lượng từng loại dữ liệu ở bot B với bot A",
       "Bot A: ≥200 tag · ≥300 template (có ảnh) · ≥30 scenario · ≥20 form · ≥10 richmenu · ≥50 friend info",
       "- Copy hoàn tất, KHÔNG chuyển sang trạng thái thất bại vì quá thời gian\n"
       "- Thời gian chạy nằm trong mốc cam kết với khách hàng (xem MT-08 —「khoảng 1 giờ」)\n"
       "- Số lượng từng loại ở bot B khớp CHÍNH XÁC với bot A\n"
       "- Không có bản ghi nào bị thiếu ở cuối danh sách",
       env=P,
       spec="Đã hỏi leader",
       note="MT-08 — corpus KHÔNG có TC hiệu năng cho backup, spec cũng không có ngưỡng. "
            "TC do AI bổ sung vì mốc「1 giờ」đã ghi trên UI cho khách hàng. Cần Leader duyệt."),
]
