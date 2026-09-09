# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 18-20: job xử lý callback follow (chống trùng,
gộp event, đổi domain callback), đổi bot / job recover / dữ liệu đời cũ, và phân
quyền staff + môi trường.

Nguồn:
- TCsLine_JOB (= TCsLine_Improve chung) → tab「Test callback friend」(11/2025 →
  08/2026, tab master còn sống, 4 cột ticket: Feature #38620 · Bug tự detect #38694 ·
  Bug KH #38447 · SpecImprove #36986) — chỉ lấy phần callback follow/unfollow.
- 15.3 TCsLine_ChangeBot → tab「Change bot」r206-r207, r242-r249.
- 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」r341-r345 (job
  recover action unblock), r116/r254/r347 (Check acc staff — chỉ có tiêu đề).
- TCsLine_QLStaff → tab「Improve 7/10/2024」r82-r83 và tab「Comment Improve staff
  (logic) 28/10/2024」r154-r155 (mục『setting add friend — tạo/edit』).
"""
from _common import tc

JOBBASE = ("- Bot đã liên kết LINE OA thật, callback hoạt động\n"
           "- Cả 3 trang あいさつメッセージ đã cài tin nhắn + action, đã bấm 保存\n"
           "- Có quyền tạo/chỉnh dữ liệu test ở tầng hạ tầng (dùng công cụ gửi request)")

S7 = [
    # ═══════════ 18. Job callback follow & chống trùng ═══════════
    tc("Job callback follow & chống trùng", "JOB-001", "Normal",
       "Callback kết bạn 3 loại đều gửi được action chào mừng",
       JOBBASE,
       "1. Dùng 3 tài khoản LINE test tương ứng 3 loại: bạn mới · bạn cũ · bỏ block\n"
       "2. Cho từng tài khoản thực hiện kết bạn / kết bạn lại / bỏ block\n"
       "3. Với mỗi tài khoản: kiểm tra friend hiện lên tool và nhận đúng tin + action",
       "3 loại: add new fr · add old fr · unblock fr",
       "- Cả 3 loại: friend được thêm/hiện lại trên tool\n"
       "- Cả 3 loại: nhận đúng tin nhắn + action của trang tương ứng\n"
       "- Không friend nào bị trùng lặp trong danh sách bạn bè\n"
       "- Không action nào bị gửi 2 lần",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r30-r32, r53-r55 và r379-r381 "
            "(『Add được friend, send action add friend nếu có — check không bị duplicate friend, "
            "không bị send duplicate action』)."),

    tc("Job callback follow & chống trùng", "JOB-001", "Normal",
       "Kết bạn qua landing — callback ghi nhận lượt click và gửi action quét QR",
       JOBBASE + "\n- Có 1 landing QR đang bật",
       "1. Dùng tài khoản LINE test quét QR landing để kết bạn\n"
       "2. Về admin kiểm tra màn thống kê của landing đó\n"
       "3. Kiểm tra tin nhắn + action friend nhận được\n"
       "4. Lặp lại khi có 2 lượt kết bạn qua landing gần như cùng lúc (2 tài khoản test)",
       "1 lượt kết bạn qua landing, sau đó 2 lượt đồng thời",
       "- Lượt click landing được ghi nhận đúng số lượng (1 rồi 3)\n"
       "- Friend nhận đúng action của landing\n"
       "- Trường hợp 2 lượt đồng thời: cả 2 friend đều được xử lý, không ai bị bỏ sót",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r33, r56, r382, r383 (『1 thời điểm có 1 "
            "callback』/『1 thời điểm có 2 callback』)."),

    tc("Job callback follow & chống trùng", "CONC-001", "Abnormal",
       "Hai callback kết bạn trùng nhau (LINE gửi lại) — chỉ xử lý 1, không gửi action 2 lần",
       JOBBASE + "\n- Bot đã BẬT tùy chọn gửi lại webhook trên LINE Developers Console",
       "1. Tạo 2 callback bỏ block trùng định danh sự kiện, đưa vào hệ thống cùng lúc\n"
       "2. Chờ hệ thống xử lý xong\n"
       "3. Kiểm tra tin nhắn friend nhận trên app LINE và action đã chạy",
       "2 callback unblock trùng định danh sự kiện",
       "- Chỉ 1 callback được xử lý, callback còn lại bị đánh dấu bỏ qua\n"
       "- Friend nhận ĐÚNG 1 tin nhắn chào mừng, action chạy ĐÚNG 1 lần (không duplicate)",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r165 (『Dummy 2 callback unblock → chỉ xử "
            "lý 1 callback, callback còn lại set status = 11; check action không bị gửi "
            "duplicate』)."),

    tc("Job callback follow & chống trùng", "CONC-001", "Abnormal",
       "Callback kết bạn cũ đã xử lý rồi lại tới lần nữa — không xử lý lại, không gửi action",
       JOBBASE,
       "1. Thực hiện 1 lượt kết bạn lại (bạn cũ) bình thường, ghi lại tin nhận được\n"
       "2. Đưa vào hệ thống 1 callback kết bạn cũ có ĐÚNG định danh sự kiện đã xử lý ở bước 1\n"
       "3. Kiểm tra tin nhắn friend nhận trên app LINE",
       "1 callback kết bạn old friend trùng định danh sự kiện đã xử lý",
       "- Callback lặp KHÔNG được xử lý lại\n"
       "- Friend KHÔNG nhận thêm tin nhắn/action nào (tổng vẫn đúng 1 lần)",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r171 (『insert 1 callback cùng "
            "webhook_event_id mà trước đó đã được xử lý rồi → Không xử lý callback này, Không gửi "
            "action nữa』)."),

    tc("Job callback follow & chống trùng", "CONC-001", "Abnormal",
       "Nhiều callback kết bạn được đẩy vào cùng lúc — chỉ xử lý 1, action không duplicate",
       JOBBASE,
       "1. Dùng công cụ gửi request tạo nhiều callback kết bạn của CÙNG 1 friend cùng lúc\n"
       "2. Chờ xử lý xong\n"
       "3. Kiểm tra tin nhắn friend nhận và số lần action chạy\n"
       "4. Kiểm tra danh sách bạn bè xem friend có bị nhân đôi không",
       "5 callback kết bạn của cùng 1 friend, đẩy đồng thời",
       "- Chỉ 1 callback được xử lý, các callback còn lại bị đánh dấu bỏ qua\n"
       "- Friend nhận đúng 1 tin nhắn chào mừng, action chạy đúng 1 lần\n"
       "- Friend chỉ xuất hiện 1 lần trong danh sách bạn bè",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r180 (『Dùng postman để call tạo nhiều "
            "callback cùng lúc — Callback add friend → chỉ xử lý 1, check action không bị gửi "
            "duplicate』)."),

    tc("Job callback follow & chống trùng", "CONC-001", "Normal",
       "Hai friend cùng kết bạn/bỏ block cùng lúc — cả hai đều được xử lý đúng",
       JOBBASE + "\n- Có 2 tài khoản LINE test",
       "1. Cho 2 tài khoản test cùng lúc thực hiện: kết bạn mới / kết bạn lại / block / bỏ block\n"
       "2. Về admin mở chat 1:1 của cả 2 friend\n"
       "3. Kiểm tra tin nhắn, action và trigger của từng friend\n"
       "4. Lặp lại nhưng 2 friend thuộc 2 BOT khác nhau",
       "2 friend cùng bot; sau đó 2 friend ở 2 bot khác nhau",
       "- Cả 2 friend đều nhận đúng tin + action, không ai bị bỏ sót\n"
       "- Trigger hiển thị đúng loại cho từng friend trên cả web và app mobile\n"
       "- Trường hợp 2 bot: mỗi friend nhận đúng cấu hình của bot mình, KHÔNG lẫn sang bot kia",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r186 và r194 (『Có 2 friend kết bạn mới/"
            "kết bạn cũ/block/unblock (ở 2 bot) → hiển thị được trigger tương ứng trên chat 1:1 web "
            "và app đúng của mỗi bot』). Bao trùm cả SEC-ISO-001 (cách ly dữ liệu 2 bot)."),

    tc("Job callback follow & chống trùng", "INTG-HOOK-001", "Normal",
       "LINE gộp nhiều sự kiện vào 1 callback — sự kiện follow vẫn được xử lý, không bị miss",
       JOBBASE,
       "1. Tạo callback gộp gồm nhiều sự kiện theo các tổ hợp ở cột Dữ liệu nhập\n"
       "2. Với mỗi tổ hợp: chờ xử lý xong\n"
       "3. Kiểm tra friend có nhận tin + action chào mừng không, và tin nhắn/ảnh có hiện ở chat 1:1",
       "6 tổ hợp: (message + follow) · (follow + message) · (message + unfollow) · "
       "(unfollow + follow) · (media + follow) · (follow + media)",
       "- Ở MỌI tổ hợp, sự kiện follow đều được xử lý → friend nhận đúng tin + action chào mừng\n"
       "- Các sự kiện khác trong cùng callback cũng được xử lý đủ, không bị miss",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r247-r258 (『Tất cả các event đều được xử "
            "lý, không bị miss』). Gộp 6 tổ hợp vì cùng 1 kết quả mong đợi."),

    tc("Job callback follow & chống trùng", "INTG-HOOK-001", "Normal",
       "Callback gộp 3-4 sự kiện vòng đời 1 friend — xử lý đủ theo đúng thứ tự",
       JOBBASE,
       "1. Tạo callback gộp gồm chuỗi: follow → message → unfollow của cùng 1 friend\n"
       "2. Chờ xử lý xong, kiểm tra tin nhắn chào mừng, tin friend gửi, trạng thái block\n"
       "3. Lặp lại với tổ hợp 4 sự kiện hỗn hợp (message + postback + follow + videoPlayComplete)",
       "Chuỗi 3 sự kiện vòng đời; và tổ hợp 4 sự kiện hỗn hợp",
       "- Sự kiện follow chạy đúng cấu hình chào mừng\n"
       "- Sự kiện message hiện đúng ở chat 1:1\n"
       "- Sự kiện unfollow cập nhật đúng trạng thái friend đã block\n"
       "- Không sự kiện nào bị bỏ sót",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r262-r264."),

    tc("Job callback follow & chống trùng", "MSG-003", "Abnormal",
       "Callback follow của friend đang bị bot block — bỏ qua, trạng thái block không đổi",
       JOBBASE + "\n- Có 1 friend đang bị BOT block",
       "1. Tạo callback follow của friend đang bị bot block\n"
       "2. Chờ xử lý xong\n"
       "3. Kiểm tra trạng thái block của friend ở màn chi tiết friend\n"
       "4. Kiểm tra friend có nhận tin chào mừng không\n"
       "5. Lặp lại với callback gộp: 2 callback follow của cùng friend đó",
       "Friend đang bị bot block · callback follow đơn và gộp 2",
       "- Callback bị bỏ qua, KHÔNG gửi tin/action chào mừng\n"
       "- Trạng thái block của friend KHÔNG bị thay đổi\n"
       "- Trường hợp gộp 2 callback follow: cả 2 đều bị bỏ qua",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r217 và r245 (『nếu user bị bot block thì "
            "expect là cả 2 callback đều bị ignore => is_block của friend không bị thay đổi』) + "
            "job-spec.md §State machine (trạng thái 7 = bị bot block)."),

    tc("Job callback follow & chống trùng", "ENV-001", "Abnormal",
       "Server LME lỗi lúc friend kết bạn, sau đó phục hồi — callback gửi lại vẫn chạy chào mừng",
       JOBBASE + "\n- Bot BẬT tùy chọn gửi lại webhook trên LINE Developers Console",
       "1. Làm server LME tạm lỗi (hoặc phối hợp dev dựng lỗi 500)\n"
       "2. Trong lúc lỗi: dùng tài khoản LINE test kết bạn với bot\n"
       "3. Khôi phục server\n"
       "4. Chờ LINE gửi lại callback, kiểm tra friend trên tool và tin nhắn nhận được",
       "1 lượt kết bạn trong lúc server lỗi",
       "- Lần đầu không nhận được callback\n"
       "- Sau khi phục hồi, callback gửi lại được xử lý → friend hiện trên tool và nhận đúng tin + "
       "action chào mừng\n"
       "- Không bị gửi trùng nhiều lần",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r162, r184 (case gửi lại webhook). "
            "TC đã thu hẹp về phạm vi FA-007 (kết bạn) thay vì tin nhắn."),

    tc("Job callback follow & chống trùng", "ENV-002", "Normal",
       "Đổi domain callback của bot — kết bạn 3 loại vẫn chạy đúng cấu hình chào mừng",
       JOBBASE,
       "1. Ghi lại domain callback hiện tại của bot\n"
       "2. Đổi sang domain callback mới theo quy trình\n"
       "3. Lần lượt test 3 loại: kết bạn mới · kết bạn lại · bỏ block\n"
       "4. Kiểm tra tin nhắn + action từng loại\n"
       "5. Đổi lại domain cũ và test lại 1 lượt kết bạn mới",
       "Domain callback cũ và mới",
       "- Sau khi đổi domain: cả 3 loại kết bạn đều nhận đúng tin + action chào mừng\n"
       "- Sau khi đổi lại domain cũ: vẫn chạy đúng\n"
       "- Không có lượt kết bạn nào bị mất trong lúc chuyển đổi",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r30-r33 (domain cũ) vs r53-r56 (domain "
            "mới), và r379-r388 (đợt 08/2026 với 2 domain cb-1/cb-3). TC đã thu hẹp về phạm vi "
            "FA-007. ⚠️ Bài test hạ tầng — phối hợp dev khi chạy."),

    tc("Job callback follow & chống trùng", "ENV-001", "Abnormal",
       "Bot không còn tồn tại trên hệ thống — callback kết bạn bị bỏ qua, không lỗi dây chuyền",
       "- Có 1 bot test có thể xóa được\n"
       "- Bot đó đã cài cấu hình chào mừng",
       "1. Xóa bot khỏi エルメ (hoặc trỏ callback tới định danh bot không tồn tại)\n"
       "2. Dùng tài khoản LINE test kết bạn với LINE OA đó\n"
       "3. Kiểm tra hệ thống có sinh lỗi hàng loạt không\n"
       "4. Kiểm tra các bot KHÁC vẫn nhận và xử lý callback bình thường",
       "Bot không tồn tại trong hệ thống",
       "- Callback bị đánh dấu bỏ qua (không tìm thấy bot), không gửi tin/action\n"
       "- Không sinh lỗi dây chuyền: các bot khác vẫn xử lý callback kết bạn bình thường",
       env="PRODUCTION",
       note="Nguồn: TCsLine_JOB/tab「Test callback friend」r410 (『Case bot không tồn tại trong DB』) "
            "+ job-spec.md §State machine (trạng thái 6 = không tìm thấy bot)."),

    tc("Job callback follow & chống trùng", "ENV-001", "Abnormal",
       "Bot đã hết hạn hợp đồng quá 7 ngày — callback kết bạn bị bỏ qua",
       "- Có 1 bot ở trạng thái hết hạn hợp đồng quá 7 ngày\n"
       "- Bot đó đã cài cấu hình chào mừng",
       "1. Đưa bot về trạng thái hết hạn quá 7 ngày\n"
       "2. Dùng tài khoản LINE test kết bạn với LINE OA của bot đó\n"
       "3. Kiểm tra tin nhắn phía friend và trạng thái xử lý",
       "Bot hết hạn > 7 ngày",
       "- Friend KHÔNG nhận tin nhắn/action chào mừng\n"
       "- Callback được đánh dấu bỏ qua vì bot hết hạn, không sinh lỗi",
       env="PRODUCTION",
       note="Nguồn: job-spec.md §Edge cases + §State machine (trạng thái 8 = bot hết hạn). "
            "Corpus TCs KHÔNG có case này — TC do AI bổ sung từ spec. Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    # ═══════════ 19. Đổi bot, recover & legacy ═══════════
    tc("Đổi bot, recover & legacy", "DATA-BACKUP-001", "Normal",
       "Đổi bot (change bot) — cấu hình あいさつメッセージ của bot cũ được giữ nguyên",
       "- Bot A đã cài đủ cấu hình ở cả 3 trang あいさつメッセージ\n"
       "- Chuẩn bị thực hiện quy trình đổi bot (change bot) cho bot A",
       "1. Ghi lại tin nhắn + danh sách action của cả 3 trang của bot A\n"
       "2. Thực hiện quy trình đổi bot\n"
       "3. Sau khi đổi xong, mở lại cả 3 trang あいさつメッセージ\n"
       "4. So sánh với bản ghi ở bước 1",
       "Cấu hình 3 trang của bot A trước và sau khi đổi bot",
       "- Tin nhắn và danh sách action của cả 3 trang GIỮ NGUYÊN sau khi đổi bot",
       env="PRODUCTION",
       note="Nguồn: 15.3 TCsLine_ChangeBot → tab「Change bot」r206 (『Setting kết bạn — Check web → "
            "Giữ nguyên setting của bot cũ』)."),

    tc("Đổi bot, recover & legacy", "REG-SHARED-001", "Normal",
       "Sau khi đổi bot — friend kết bạn với bot mới vẫn chạy đúng cấu hình chào mừng",
       "- Vừa hoàn tất quy trình đổi bot cho 1 bot đã cài cấu hình chào mừng\n"
       "- Có 3 tài khoản LINE test cho 3 loại: bạn mới · bạn cũ · bỏ block",
       "1. Sau khi đổi bot xong, kiểm tra URL kết bạn và QR mới\n"
       "2. Lần lượt test 3 loại: kết bạn mới · kết bạn lại · bỏ block\n"
       "3. Lặp lại bằng 2 đường: URL kết bạn và quét QR\n"
       "4. Lặp lại bằng landing QR cũ (tạo trước khi đổi bot) và landing QR mới",
       "3 loại friend × 2 đường vào (URL / QR) + 2 loại landing (cũ / mới)",
       "- Mọi tổ hợp: friend kết bạn thành công và nhận đúng tin + action đã cài\n"
       "- Landing QR cũ (tạo trước khi đổi bot) vẫn kết bạn được",
       env="PRODUCTION",
       note="Nguồn: 15.3 TCsLine_ChangeBot → tab「Change bot」r207 (『Kết bạn new friend / old "
            "friend / Unblock → thực hiện action đã setting; kết bạn qua url kết bạn, qua QR』) và "
            "r217-r218 (landing cũ / mới)."),

    tc("Đổi bot, recover & legacy", "PAY-PLAN-001", "Normal",
       "Thêm bot mới hoặc đổi bot ở mọi gói dịch vụ — cấu hình chào mừng vẫn chạy",
       "- Có tài khoản test có thể thêm/đổi bot ở 3 gói: free · standard · pro",
       "1. Với từng gói: thêm bot mới, cài tin nhắn + action ở trang 新規友だち用\n"
       "2. Dùng tài khoản LINE test kết bạn, kiểm tra tin + action\n"
       "3. Với từng gói: thực hiện đổi bot, kiểm tra lại kết bạn và action\n"
       "4. Sau khi đổi bot, kiểm tra danh sách bạn bè",
       "3 gói: free · standard · pro",
       "- Cả 3 gói: thêm bot thành công, friend kết bạn được, action chào mừng chạy bình thường\n"
       "- Cả 3 gói: sau đổi bot, action vẫn chạy và KHÔNG hiển thị friend của bot cũ",
       env="PRODUCTION",
       note="Nguồn: 15.3 TCsLine_ChangeBot → tab「Change bot」r242-r249."),

    tc("Đổi bot, recover & legacy", "DATA-MIG-001", "Normal",
       "Job khôi phục action cho trang ブロック解除時用 — cấu hình cũ hiện đúng ở 3 menu",
       "- Có bot đã cài action từ đợt cũ (chỉ có 2 loại: bạn hiện tại và mọi friend)\n"
       "- Job khôi phục action cho loại unblock chuẩn bị chạy",
       "1. Trước khi chạy job: ghi lại action đang cài ở mục『bạn bè hiện tại』và『mọi friend』\n"
       "2. Chạy job khôi phục action unblock\n"
       "3. Sau khi job xong: mở lần lượt 3 trang あいさつメッセージ\n"
       "4. Đối chiếu action ở từng trang với bản ghi bước 1",
       "Cấu hình action đời cũ",
       "- Action của『bạn bè hiện tại』hiện đúng ở trang 新規友だち用\n"
       "- Action của『mọi friend』hiện đúng ở trang 既存友だち用 VÀ trang ブロック解除時用\n"
       "- Không mất action nào, không nhân đôi action",
       env="PRODUCTION",
       note="⚠️ MT-10. Nguồn: r341-r345 (『job recover action của unblock』). Spec FA-007 KHÔNG có "
            "mô tả nào về job này — đề xuất bổ sung vào job-spec.md. TC chỉ chạy được ở đợt "
            "migration; giữ lại làm hồ sơ.",
       spec="Spec không ghi"),

    tc("Đổi bot, recover & legacy", "COMPAT-LEGACY-001", "Abnormal",
       "Bot chỉ có cấu hình đời cũ (tag/scenario V1), chưa có action V2 — hành vi khi friend kết bạn",
       "- Có 1 bot dữ liệu đời cũ: chưa cài action ở màn あいさつメッセージ V2 nhưng còn cấu hình "
       "gắn tag / khởi động scenario của phiên bản cũ\n"
       "- Có tài khoản LINE test chưa từng kết bạn",
       "1. Xác nhận trang 新規友だち用 hiển thị「エルメアクションは登録されていません」\n"
       "2. Dùng tài khoản LINE test kết bạn với bot\n"
       "3. Kiểm tra friend có bị gắn tag / vào scenario nào không\n"
       "4. Đối chiếu với cấu hình đời cũ",
       "Bot có cấu hình V1 (tag + scenario), không có action V2",
       "- Ghi lại chính xác: friend CÓ hay KHÔNG được gắn tag / vào scenario theo cấu hình đời cũ\n"
       "- Nếu CÓ chạy: màn admin phải cho admin thấy được cấu hình đó (không phải cấu hình ẩn "
       "chạy ngầm mà UI báo『chưa đăng ký action nào』)",
       env="PRODUCTION",
       note="⚠️ MT-11. Nguồn: feature-spec.md §5 BR-10 (『Khi action_new_id/action_old_id = null, "
            "job fallback sang new_tag_id/old_tag_id và new_scenario_id/old_scenario_id — chưa "
            "được expose trên UI V2』, mức tin cậy Trung bình; spec tự ghi nhận VĐ-TBC-01 chưa "
            "document đủ). Corpus TCs KHÔNG có case này. Rủi ro: UI nói không có action nhưng thực "
            "tế vẫn chạy. CẦN LEADER CHỐT.",
       spec="Đã hỏi leader"),

    # ═══════════ 20. Phân quyền & môi trường ═══════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff ĐƯỢC cấp quyền màn あいさつメッセージ — vào được và lưu được cấu hình",
       "- Có tài khoản staff đã được mời và chấp nhận vào bot\n"
       "- Quyền màn『setting add friend』đang được BẬT cho staff đó",
       "1. Đăng nhập bằng tài khoản staff, chọn bot\n"
       "2. Mở lần lượt 3 trang あいさつメッセージ\n"
       "3. Sửa tin nhắn và cài 1 action, bấm 保存\n"
       "4. F5 kiểm tra đã lưu chưa\n"
       "5. Đăng nhập lại bằng tài khoản 主管理者, kiểm tra cấu hình staff vừa lưu",
       "Staff có quyền màn setting add friend",
       "- Staff vào được cả 3 trang, không bị chặn\n"
       "- Staff lưu (tạo/sửa) được tin nhắn và action\n"
       "- Cấu hình staff lưu hiển thị đúng khi 主管理者 mở lại",
       note="Nguồn: TCsLine_QLStaff → tab「Improve 7/10/2024」r82-r83 và tab「Comment Improve staff "
            "(logic)」r154-r155 (mục『setting add friend — tạo / edit』; cột kết quả mong đợi TRỐNG, "
            "expected do AI viết). ⚠️ r83 (thao tác EDIT) có kết quả **NG ở môi trường dev** — "
            "cần verify lại. Đóng Gap #8 của feature-spec.md §9.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & môi trường", "PERM-001", "Abnormal",
       "Staff KHÔNG được cấp quyền — menu あいさつメッセージ bị chặn và có thông báo rõ",
       "- Có tài khoản staff đã vào bot\n"
       "- Quyền màn『setting add friend』đang TẮT cho staff đó",
       "1. Đăng nhập bằng tài khoản staff, chọn bot\n"
       "2. Rê chuột lên mục menu「あいさつメッセージ」\n"
       "3. Thử click vào mục menu đó",
       "Staff KHÔNG có quyền màn setting add friend",
       "- Menu ở trạng thái bị chặn (mờ / không click được)\n"
       "- Hover hiện thông báo「操作できません。この機能の操作権限が付与されていません。"
       "主管理者に操作権限の付与を依頼してください。」\n"
       "- Không vào được trang",
       note="Nguồn: TCsLine_Improve chung → tab「Phân quyền」r4, r7, r12, r17 (nội dung thông báo "
            "chuẩn của toàn tool). Áp cho màn あいさつメッセージ — do AI ánh xạ, cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "Staff không có quyền nhưng gọi thẳng URL / API — phải bị chặn ở tầng server",
       "- Có tài khoản staff KHÔNG có quyền màn『setting add friend』\n"
       "- Đã ghi lại cấu hình hiện tại của cả 3 trang",
       "1. Đăng nhập bằng tài khoản staff không có quyền\n"
       "2. Gõ thẳng URL /basic/setting-add-friend vào thanh địa chỉ\n"
       "3. Lặp lại với /basic/setting-add-friend-old và /basic/setting-add-friend-unblock\n"
       "4. Dùng công cụ gửi request gọi thẳng API lấy cấu hình và API lưu cấu hình\n"
       "5. Đăng nhập lại bằng 主管理者 và đối chiếu cấu hình 3 trang",
       "3 URL trực tiếp + 2 API (lấy cấu hình, lưu cấu hình)",
       "- Gõ URL trực tiếp: bị chặn hoặc chuyển hướng, KHÔNG vào được trang\n"
       "- Gọi API: trả lỗi phân quyền, KHÔNG trả về dữ liệu cấu hình và KHÔNG ghi được\n"
       "- Cấu hình 3 trang giữ nguyên",
       note="TC do AI bổ sung theo PERM-002 (『không được bypass quyền bằng API/URL trực tiếp』) + "
            "feature-spec.md §5 BR-09 (middleware basic_access). Corpus chỉ test ở tầng menu UI. "
            "Rủi ro CAO. Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & môi trường", "PERM-004", "Normal",
       "Thu hồi quyền khi staff đang mở màn あいさつメッセージ — thao tác tiếp theo bị chặn",
       "- Staff đang ĐƯỢC cấp quyền và đang mở trang 新規友だち用",
       "1. Staff mở trang 新規友だち用 và sửa tin nhắn (chưa bấm 保存)\n"
       "2. Ở tài khoản 主管理者: TẮT quyền màn『setting add friend』của staff đó\n"
       "3. Staff bấm「保存」\n"
       "4. Staff F5 lại trang\n"
       "5. 主管理者 kiểm tra tin nhắn hiện tại",
       "Thu hồi quyền giữa lúc staff đang thao tác",
       "- Bấm 保存 bị chặn với thông báo lỗi rõ ràng (không lưu âm thầm)\n"
       "- Sau F5, staff không vào được trang nữa\n"
       "- Tin nhắn của bot KHÔNG bị đổi",
       note="TC do AI bổ sung theo PERM-004. Corpus có TC thu hồi quyền tổng quát ở tab「Phân quyền」"
            "r22-r34 nhưng không gắn với màn này. Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Phân quyền & môi trường", "SEC-ISO-001", "Abnormal",
       "Gọi API lấy cấu hình của bot mà tài khoản không có quyền — không lộ dữ liệu bot khác",
       "- Tài khoản Admin A chỉ quản lý bot A\n"
       "- Tồn tại bot B của tài khoản khác, bot B có cấu hình chào mừng",
       "1. Đăng nhập bằng tài khoản A\n"
       "2. Bắt request lấy cấu hình của trang 新規友だち用 (bot A)\n"
       "3. Gửi lại request nhưng đổi định danh bot sang bot B\n"
       "4. Đọc response\n"
       "5. Thử tương tự với API lưu cấu hình",
       "Định danh bot B (không thuộc tài khoản A)",
       "- Response KHÔNG chứa tin nhắn/action/URL kết bạn của bot B\n"
       "- API lưu bị chặn, cấu hình bot B không bị sửa",
       note="TC do AI bổ sung theo SEC-ISO-001 + PERM-003. Corpus không có. Rủi ro CAO (lộ dữ liệu "
            "chéo tài khoản). Cần Leader xác nhận.",
       spec="Spec không ghi"),

    tc("Phân quyền & môi trường", "ENV-003", "Normal",
       "Đối chiếu dev / staging / production — cấu hình chào mừng chạy giống nhau",
       "- Có cùng 1 kịch bản cấu hình dựng được ở cả 3 môi trường\n"
       "- Mỗi môi trường có 1 bot test và tài khoản LINE test riêng",
       "1. Ở mỗi môi trường: cài cùng 1 tin nhắn + cùng 1 action ở trang 新規友だち用\n"
       "2. Ở mỗi môi trường: dùng tài khoản LINE test kết bạn\n"
       "3. Ghi lại: nội dung tin nhận, thời gian trễ, action đã chạy, ảnh QR có hiện không\n"
       "4. So sánh 3 môi trường",
       "Cùng 1 tin nhắn + 1 action, chạy ở dev · staging · production",
       "- Nội dung tin nhắn và action chạy giống nhau ở cả 3 môi trường\n"
       "- Ảnh QR hiển thị được ở cả 3 (nếu môi trường nào không có media server thì ghi rõ khác "
       "biệt này làm hồ sơ)\n"
       "- Ghi lại chênh lệch thời gian trễ giữa 3 môi trường",
       env="PRODUCTION",
       note="TC do AI bổ sung theo ENV-003 + RULE-08 (ảnh QR lấy từ media server → khác biệt môi "
            "trường là rủi ro có thật). Corpus không có TC đối chiếu môi trường cho màn này.",
       spec="Spec không ghi"),
]
