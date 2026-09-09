# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 15-16: đồng bộ Elasticsearch sau các thao tác ở màn
friendlist, và phân quyền / môi trường.

Nguồn: TCsLine_Improve chung → tab「ESticsearch」(r4, r48, r89, r283 — các dòng thuộc
màn friendlist) và tab「Phân quyền」(r3-r14, TC dùng chung cho mọi màn của tool,
FA-001 cũng đã dùng làm nguồn).

⚠ Phân quyền: feature-spec.md §9 Gaps #7 ghi『controller KHÔNG có middleware phân
quyền riêng』— corpus chỉ có TC tầng UI (ẩn menu + tooltip). Nhóm này bổ sung TC ở
TẦNG API, xem MT-12.
"""
from _common import tc

ADM = ("- Đăng nhập Admin (role 主管理者) của bot đã liên kết LINE OA\n"
       "- Bot có ≥ 10 friend\n"
       "- Mở /basic/friendlist")
PERM = ("- Chuẩn bị 3 tài khoản staff ở 3 role: 副管理者 · 運用者 · và 1 staff bị TẮT quyền "
        "thao tác màn 友だちリスト\n"
        "- Chuẩn bị 1 tài khoản 主管理者 để đối chứng")

S7 = [
    # ═══════════ 15. Đồng bộ Elasticsearch ═══════════
    tc("Đồng bộ Elasticsearch", "SYNC-APP-001", "Normal",
       "Xoá friend ở màn friendlist — hàng đợi đồng bộ ES ghi nhận và tài liệu bị xoá khỏi index",
       ADM + "\n- Chuẩn bị 1 friend có tên đặc trưng, dễ tìm bằng ô tìm kiếm",
       "1. Search tên friend đó ở ô tìm kiếm, xác nhận tìm được\n"
       "2. Xoá friend đó (từ màn friendlist hoặc màn chi tiết)\n"
       "3. Chờ hàng đợi đồng bộ chạy\n"
       "4. Search lại đúng tên friend đó ở ô tìm kiếm\n"
       "5. Kiểm tra bảng hàng đợi đồng bộ có bản ghi tương ứng không",
       "1 friend có tên đặc trưng",
       "- Trước khi xoá: search ra friend\n"
       "- Sau khi xoá và đồng bộ xong: search KHÔNG ra friend đó nữa\n"
       "- Hàng đợi đồng bộ có bản ghi cho thao tác xoá friend này\n"
       "- Ghi lại giá trị `type` thực tế của bản ghi để đối chiếu spec",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: tab「ESticsearch」r4 (『Delete Line user → Xóa ở mypage và friend list → "
            "Tạo bản ghi trong bảng sync_esticsearch, type=2, data_sync NULL』). ⚠ MT-13: "
            "spec feature-spec.md §7.2 ghi TYPE_DELETE_LINE_USER = **11** cho thao tác xoá, "
            "còn type=2 là TYPE_CONVERSATION → 2 nguồn nói 2 con số khác nhau. RULE-08: job → "
            "PRODUCTION."),

    tc("Đồng bộ Elasticsearch", "SYNC-APP-001", "Normal",
       "Block friend ở màn friendlist — trạng thái block được đẩy sang index tìm kiếm",
       ADM,
       "1. Ghi lại tên 1 friend\n"
       "2. Ở màn friendlist, chạy action block friend cho friend đó\n"
       "3. Chờ hàng đợi đồng bộ chạy\n"
       "4. Search tên friend đó ở ô tìm kiếm của danh sách chính\n"
       "5. Kiểm tra bản ghi trong hàng đợi đồng bộ",
       "1 friend bị admin block",
       "- Sau khi đồng bộ: search ở danh sách chính KHÔNG ra friend đó\n"
       "- Hàng đợi đồng bộ có bản ghi với dữ liệu tương ứng "
       "`{\"is_blocked\":1,\"blocked_by\":1}`\n"
       "- Friend vẫn tìm thấy ở màn「ブロックした友だち」",
       env="PRODUCTION",
       note="Nguồn: tab「ESticsearch」r89 (『Friend list → Bot block friend → "
            "{\"is_blocked\":1,\"blocked_by\":1}』) + r46, r47. RULE-08: job → PRODUCTION."),

    tc("Đồng bộ Elasticsearch", "SYNC-APP-001", "Normal",
       "Bỏ ẩn friend ở màn 非表示中の友だち — trạng thái ẩn được đẩy sang index",
       "- Đăng nhập Admin của bot có ≥ 1 friend đang bị ẩn\n"
       "- Ghi lại tên friend đó",
       "1. Search tên friend đó ở danh sách chính — xác nhận KHÔNG ra\n"
       "2. Mở /basic/friendlist/hidden, click「再表示」cho friend đó\n"
       "3. Chờ hàng đợi đồng bộ chạy\n"
       "4. Search lại tên friend đó ở danh sách chính\n"
       "5. Kiểm tra bản ghi hàng đợi đồng bộ",
       "1 friend đang bị ẩn được bỏ ẩn",
       "- Trước khi bỏ ẩn: search ở danh sách chính không ra\n"
       "- Sau khi bỏ ẩn và đồng bộ: search RA friend đó\n"
       "- Hàng đợi đồng bộ có bản ghi với dữ liệu `{\"is_hide\":0}`",
       env="PRODUCTION",
       note="Nguồn: tab「ESticsearch」r283 (『ẩn friend (bảng conversation cột is_hide) → bỏ ẩn "
            "friend → nhấn bỏ ẩn ở màn /basic/friendlist/hidden → {\"is_hide\":0}』). "
            "RULE-08: job → PRODUCTION."),

    tc("Đồng bộ Elasticsearch", "SYNC-APP-001", "Normal",
       "Bulk action đổi trạng thái scenario — trạng thái mới được đẩy sang index",
       ADM + "\n- Đã tạo sẵn scenario「S1」",
       "1. Ở màn friendlist, tích 1 friend chưa đăng ký scenario → chạy action bắt đầu S1\n"
       "2. Chờ hàng đợi đồng bộ chạy\n"
       "3. Dùng bộ lọc「ステップ購読状況」= đang theo dõi S1 → kiểm tra friend có trong kết quả\n"
       "4. Chạy action dừng scenario cho friend đó → chờ đồng bộ\n"
       "5. Lọc lại theo trạng thái dừng → kiểm tra friend",
       "1 friend · scenario S1 · 2 trạng thái start / stop",
       "- Sau khi start và đồng bộ: lọc theo『đang theo dõi S1』ra friend đó\n"
       "- Sau khi stop và đồng bộ: lọc theo『đang theo dõi S1』KHÔNG ra friend đó, "
       "lọc theo trạng thái dừng thì ra\n"
       "- Hàng đợi đồng bộ có bản ghi chứa key trạng thái scenario tương ứng",
       env="PRODUCTION",
       note="Nguồn: tab「ESticsearch」r48 (『Friend list > Scenario / stt=0 stop giữa chừng, "
            "stt=1 đang follow, stt=2 đã follow xong → Tạo bản ghi trong bảng sync_esticsearch "
            "với key SCENARIO_STATUS_*』). RULE-08: job → PRODUCTION."),

    tc("Đồng bộ Elasticsearch", "SYNC-APP-001", "Normal",
       "Bulk action gắn / gỡ tag — kết quả lọc theo tag cập nhật đúng sau đồng bộ",
       ADM + "\n- Đã tạo sẵn 1 tag mới chưa gắn cho ai",
       "1. Ở màn friendlist, tích 3 friend → chạy action gắn tag mới\n"
       "2. Chờ hàng đợi đồng bộ chạy\n"
       "3. Lọc「タグ = tag mới」→ đếm số friend trong kết quả\n"
       "4. Tích 1 trong 3 friend → chạy action gỡ tag → chờ đồng bộ\n"
       "5. Lọc lại theo tag đó → đếm lại",
       "3 friend · 1 tag mới",
       "- Sau bước 3: lọc theo tag ra đúng 3 friend\n"
       "- Sau bước 5: lọc theo tag ra đúng 2 friend\n"
       "- Số ở màn chi tiết tag khớp với số kết quả lọc ở mỗi bước",
       env="PRODUCTION",
       note="Nguồn: tab「ESticsearch」r42, r43, r59 (add/xóa tag → bản ghi `{\"tag_<id>\":1}` / "
            "`{\"tag_<id>\":0}`) + feature-spec.md §7.2 (TYPE_TAG=3). RULE-08: job → PRODUCTION."),

    tc("Đồng bộ Elasticsearch", "ENV-001", "Abnormal",
       "Hàng đợi đồng bộ lỗi — có bản ghi lỗi và cảnh báo, không mất dữ liệu gốc",
       "- Đăng nhập Admin\n"
       "- Phối hợp Dev để tạo tình huống đồng bộ ES thất bại (VD ES tạm không phản hồi)",
       "1. Thực hiện 1 thao tác sinh đồng bộ (xoá friend hoặc block friend)\n"
       "2. Chờ hàng đợi xử lý\n"
       "3. Kiểm tra trạng thái bản ghi trong hàng đợi đồng bộ\n"
       "4. Kiểm tra kênh cảnh báo (Chatwork) có nhận thông báo lỗi không\n"
       "5. Mở màn friendlist kiểm tra dữ liệu friend trên màn có bị mất không",
       "1 thao tác sinh đồng bộ, ES lỗi",
       "- Bản ghi hàng đợi chuyển sang trạng thái lỗi, có ghi message lỗi\n"
       "- Kênh cảnh báo Chatwork nhận được thông báo lỗi\n"
       "- Dữ liệu friend trên màn friendlist KHÔNG bị mất — thao tác gốc vẫn có hiệu lực\n"
       "- Sau khi ES phục hồi, dữ liệu đồng bộ trở lại đúng",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Corpus không có TC lỗi ES — expected bám feature-spec.md §7.2 (status=3 error, "
            "log message_error, Chatwork notification). Cần Leader xác nhận và phối hợp Dev để "
            "dựng được tình huống. RULE-08: job + môi trường → PRODUCTION."),

    # ═══════════ 16. Phân quyền & môi trường ═══════════
    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff KHÔNG có quyền — menu 友だちリスト bị khoá, hover hiện đúng thông báo",
       PERM,
       "1. Đăng nhập bằng staff bị TẮT quyền thao tác màn 友だちリスト\n"
       "2. Ở sidebar, di chuột vào mục「友だちリスト」\n"
       "3. Đọc nguyên văn thông báo hiện ra\n"
       "4. Thử click vào mục đó\n"
       "5. Cuộn trang xuống rồi hover lại, quan sát vị trí thông báo",
       "staff bị tắt quyền màn 友だちリスト",
       "- Hover hiện thông báo đúng nguyên văn:\n"
       "  「操作できません。」\n"
       "  「この機能の操作権限が付与されていません。」\n"
       "  「主管理者に操作権限を付与してもらうことで操作が可能となります。」\n"
       "- Click KHÔNG mở được màn\n"
       "- Khi cuộn trang, thông báo bám đúng vị trí của mục menu, không lệch",
       note="Nguồn: TCsLine_Improve chung → tab「Phân quyền」r4, r5, r7. Đây là TC dùng chung "
            "cho mọi màn của tool, kho FA-013 giữ bản áp riêng cho menu「友だちリスト」."),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff CÓ quyền — mở được màn 友だちリスト và thao tác bình thường",
       PERM,
       "1. Đăng nhập lần lượt bằng staff role 副管理者 và staff role 運用者 (đều được cấp quyền "
       "màn 友だちリスト)\n"
       "2. Hover vào mục「友だちリスト」ở sidebar\n"
       "3. Click vào mục đó\n"
       "4. Thử tìm kiếm, lọc và chạy 1 bulk action gửi text cho 1 friend",
       "2 staff role khác nhau, đều có quyền",
       "- Hover KHÔNG hiện thông báo lỗi quyền\n"
       "- Click mở được /basic/friendlist bình thường\n"
       "- Tìm kiếm, lọc và bulk action đều thực hiện được\n"
       "- Trigger ở chat 1:1 ghi đúng tên staff đã thao tác",
       note="Nguồn: tab「Phân quyền」r6, r8, r10, r13 + tab「Testcase」r14, r30 (staff thao tác → "
            "trigger hiện tên staff)."),

    tc("Phân quyền & môi trường", "PERM-002", "Abnormal",
       "⭐ Staff KHÔNG có quyền gọi THẲNG API của màn friendlist — phải bị chặn ở tầng server",
       PERM + "\n- Chuẩn bị công cụ gọi API trực tiếp (DevTools / Postman) với phiên đăng nhập "
              "của staff bị tắt quyền",
       "1. Đăng nhập bằng staff bị TẮT quyền màn 友だちリスト\n"
       "2. Xác nhận menu「友だちリスト」bị khoá trên giao diện\n"
       "3. Gọi THẲNG lần lượt các endpoint của màn này bằng phiên đăng nhập đó:\n"
       "   a. lấy danh sách bạn bè (post-advance-filter-v2)\n"
       "   b. tìm kiếm (result_search)\n"
       "   c. chạy bulk action (send-action)\n"
       "   d. xoá bạn bè (delete-user-block)\n"
       "   e. bỏ block (unblock-friend)\n"
       "4. Với mỗi endpoint: ghi lại mã trạng thái và nội dung phản hồi\n"
       "5. Kiểm tra dữ liệu thật có bị thay đổi không (friend có bị xoá / nhận action không)",
       "5 endpoint của FriendlistController, gọi bằng phiên staff không có quyền",
       "- Cả 5 endpoint đều TỪ CHỐI: trả về lỗi phân quyền, KHÔNG trả dữ liệu bạn bè\n"
       "- KHÔNG friend nào bị xoá, bị bỏ block hay nhận action\n"
       "- ⚠ Nếu bất kỳ endpoint nào vẫn trả dữ liệu hoặc vẫn thực thi → lỗ hổng phân quyền: "
       "UI ẩn menu nhưng tầng API không chặn",
       spec="Đã hỏi leader",
       note="⭐ TC do AI ĐỀ XUẤT, KHÔNG có trong corpus — corpus (tab「Phân quyền」) chỉ test "
            "tầng UI ẩn menu. Căn cứ: feature-spec.md §9 Gaps #7『Staff permissions — controller "
            "không có middleware phân quyền riêng』. Gắn MT-12, cần Leader xác nhận trước khi "
            "đưa vào bộ chạy chính thức."),

    tc("Phân quyền & môi trường", "PERM-001", "Normal",
       "Staff không thấy thông tin gói giá ở header khi vào màn 友だちリスト",
       PERM,
       "1. Đăng nhập bằng staff có quyền màn 友だちリスト\n"
       "2. Mở /basic/friendlist\n"
       "3. Đọc vùng header phía trên (thông tin 配信数 / gói giá)\n"
       "4. Đăng nhập lại bằng 主管理者, mở cùng màn và so sánh header",
       "1 staff có quyền · 1 主管理者",
       "- Với staff: header KHÔNG hiển thị thông tin gói giá\n"
       "- Với 主管理者: header hiển thị đầy đủ thông tin gói giá và 配信数\n"
       "- Nội dung bảng danh sách bạn bè giống nhau ở cả 2 tài khoản",
       note="Nguồn: TCsLine_Improve chung → tab「Improve nhỏ」r379 (『Check hiển thị các tính "
            "năng khác khi đã chọn bot → 情報管理 → Friend list → Không hiển thị Gói giá tại "
            "header』)."),

    tc("Phân quyền & môi trường", "ENV-003", "Normal",
       "Màn friendlist hoạt động đúng trên PRODUCTION với dữ liệu thật quy mô lớn",
       "- Tài khoản PRODUCTION của bot có > 10.000 friend\n"
       "- Được phép thao tác đọc trên bot này (không chạy action làm ảnh hưởng KH)",
       "1. Mở /basic/friendlist trên PRODUCTION, bấm giờ thời gian tải trang\n"
       "2. Đọc số「検索結果： N人」và đối chiếu với số friend của bot\n"
       "3. Sắp xếp theo「友だち追加日時」và「最新メッセージ」, bấm giờ mỗi lần\n"
       "4. Search 1 keyword, bấm giờ\n"
       "5. Sang trang 2, 3, bấm giờ",
       "bot PRODUCTION > 10.000 friend",
       "- Trang tải xong, không lỗi 500, không timeout\n"
       "- Số N khớp với tổng friend của bot\n"
       "- Sắp xếp, tìm kiếm và chuyển trang đều phản hồi, ghi lại thời gian thực tế\n"
       "- Không có dòng dữ liệu bị lặp hay thiếu khi chuyển trang",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Corpus không có TC môi trường riêng cho FA-013 — TC do AI đề xuất theo RULE-08 "
            "(loadbalance / performance bắt buộc PRODUCTION) và cảnh báo hiệu năng ở "
            "feature-spec.md §10 (N+1 query ở postFilterAdvance: mỗi item trong 200 gọi 3 query "
            "riêng). Ngưỡng thời gian chấp nhận được cần Leader chốt."),

    tc("Phân quyền & môi trường", "PERM-003", "Normal",
       "Đổi bot khi đang ở màn friendlist — dữ liệu chuyển đúng sang bot mới",
       "- Đăng nhập Admin có ≥ 2 bot, mỗi bot có số friend khác nhau\n"
       "- Ghi lại số friend của từng bot",
       "1. Mở /basic/friendlist của bot A, ghi lại số「検索結果」và 3 tên friend đầu\n"
       "2. Dùng chức năng đổi bot, chọn bot B\n"
       "3. Quan sát màn hình sau khi đổi bot\n"
       "4. Ghi lại số「検索結果」và 3 tên friend đầu của bot B\n"
       "5. Tích 1 friend rồi chạy action gửi text, kiểm tra friend của bot B nhận được",
       "2 bot có số friend khác nhau",
       "- Sau khi đổi bot, danh sách hiển thị friend của bot B\n"
       "- Số「検索結果」đúng bằng số friend của bot B\n"
       "- KHÔNG còn friend nào của bot A trong danh sách\n"
       "- Action gửi cho friend của bot B, không gửi nhầm sang friend của bot A",
       spec="Đã hỏi leader",
       note="Corpus không có TC đổi bot riêng cho FA-013 — TC do AI đề xuất, căn cứ "
            "logic-spec.md (mọi query đều lọc theo bot_id lấy từ session) và tiền lệ đổi bot ở "
            "các feature khác. Cần Leader xác nhận."),
]
