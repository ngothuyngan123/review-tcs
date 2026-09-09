# -*- coding: utf-8 -*-
"""FA-019 レッスン予約 — TC LẤP GAP quan điểm test.

Sau khi gom 610 TC từ corpus, đối chiếu 80 quan điểm của framework/checklist-lme.md thấy
24 quan điểm CHƯA có TC nào. File này bổ sung TC cho các quan điểm ÁP DỤNG ĐƯỢC với FA-019.

⚠️ TOÀN BỘ TC trong file này KHÔNG có trong corpus gốc — do AI suy luận từ
`framework/checklist-lme.md` + `spec-features/admin/lesson-booking/`. Cần Leader duyệt trước khi giao.

Quan điểm KHÔNG áp dụng (đã loại có lý do):
· INTG-CAL-001 (đồng bộ 2 chiều lịch ngoài) — spec §1.2 khẳng định FA-019 **KHÔNG có bất kỳ tích hợp
  Google Calendar nào**, đã kiểm chứng 2 nguồn độc lập (job-spec §12 và db-mapping §0:
  `google_calendar_id` NULL ở 174/174 bản ghi). Đây là khác biệt cơ bản với FA-020.
· PAY-CONFIRM-001 (tạm tính → chính thức) — FA-019 không có bước báo giá/tạm tính; số tiền là
  `calendar_course.amount` cố định tại thời điểm booking (BR-29).
· UI-004 (usability người mới) — mức Thấp, để Leader quyết có cần không.
"""
from _common import tc

CAL = ("- Đăng nhập admin bot A gói standard\n"
       "- Lesson calendar「レッスンA」(id 21) đang ON, course C1「初心者」1h00, 5.000 yên\n"
       "- Có LINE user U1 là bạn của bot A")

S10 = [
    # ── CONC-002 — Re-sync toàn bộ vs dữ liệu mới ──
    tc("Googleスプレッドシート連携", "CONC-002", "Abnormal",
       "Re-sync toàn bộ lên Google Sheet trong lúc có booking MỚI phát sinh",
       CAL + "\n- Calendar đã liên kết Google và đã có ≥ 500 booking cũ\n"
             "- Chuẩn bị được cách kích hoạt re-sync toàn bộ (xóa sheet đích rồi cho 1 booking mới)",
       "1. Xóa sheet đích để kích hoạt re-sync toàn bộ\n"
       "2. NGAY TRONG LÚC re-sync đang chạy, cho U1 đặt 1 booking MỚI\n"
       "3. Chờ re-sync xong → mở Google Sheet\n"
       "4. Đối chiếu số bản ghi trên Sheet với "
       "`SELECT COUNT(*) FROM calendar_course_bookings WHERE calendar_id = 21 "
       "AND deleted_at IS NULL AND status != 3`",
       "500 booking cũ + 1 booking mới chen giữa",
       "- Số bản ghi trên Sheet = số bản ghi trong DB (501)\n"
       "- Booking mới KHÔNG bị mất và KHÔNG bị ghi 2 lần\n"
       "- Thứ tự booking trên Sheet không bị đảo lộn",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm CONC-002 chưa có TC nào trong corpus. Corpus có test re-sync "
            "(Setting calendar r1466-r1467, r1529) nhưng KHÔNG có nhánh 'dữ liệu mới chen vào giữa'."),

    # ── CONC-003 — Race ở tầng giao diện ──
    tc("Calendar theo list", "CONC-003", "Abnormal",
       "Race tầng giao diện: đổi filter / phân trang liên tiếp nhanh ở màn danh sách booking",
       CAL + "\n- Tab 予約一覧 có 200 booking, phân trang 20 item/trang",
       "1. Bấm sang trang 2 rồi NGAY LẬP TỨC bấm trang 5 (không chờ load xong)\n"
       "2. Quan sát dữ liệu hiển thị và số trang đang active\n"
       "3. Mở modal filter, đổi điều kiện rồi bấm 絞り込み表示 2 lần liên tiếp nhanh\n"
       "4. Gõ nhanh vào ô search rồi xóa ngay trong khi request cũ chưa về",
       "200 booking",
       "- Bước 2: dữ liệu hiển thị PHẢI khớp với trang đang active (trang 5), "
       "KHÔNG hiện dữ liệu của trang 2 đè lên\n"
       "- Bước 3: chỉ áp 1 bộ filter, kết quả khớp điều kiện cuối cùng\n"
       "- Bước 4: kết quả khớp từ khóa cuối cùng trong ô search (không phải kết quả cũ về sau)",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm CONC-003 (race tầng client, response về không đúng thứ tự gửi). "
            "Corpus chỉ test phân trang/filter tuần tự, không có nhánh thao tác chồng."),

    # ── DATA-CACHE-001 — Cache / dữ liệu cũ ──
    tc("受付枠 — thêm khung giờ", "DATA-CACHE-001", "Abnormal",
       "Droplist course trong modal add slot bị cache khi course vừa đổi ở tab khác",
       CAL + "\n- Mở 2 tab: tab 1 màn quản lý calendar, tab 2 màn quản lý course",
       "1. Tab 1: mở modal add slot, ghi nhận danh sách course rồi ĐÓNG modal (không reload trang)\n"
       "2. Tab 2: đổi tên course C1 và tắt course C2 = OFF\n"
       "3. Tab 1 (KHÔNG reload): mở lại modal add slot → quan sát droplist\n"
       "4. Lặp với modal filter course và modal quản lý CSV",
       "1 course đổi tên + 1 course OFF",
       "- Bước 3, 4: droplist hiển thị TÊN MỚI của C1 và KHÔNG còn C2\n"
       "- Không phải reload cả trang mới thấy thay đổi",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm DATA-CACHE-001. Corpus có Quản lý calendar_new r465 "
            "(reload list course khi bấm filter) nhưng chỉ 1 điểm, chưa phủ modal add slot và CSV."),

    # ── DATA-ID-001 — Định danh bằng ID, không bằng tên ──
    tc("コース — tạo/sửa/xóa", "DATA-ID-001", "Normal",
       "Đổi tên course sau khi đã có booking → mọi liên kết vẫn bám ID, không bám tên",
       CAL + "\n- Course C1 tên「初心者向けトレーニング」đã có 3 booking, có remind gắn filter theo C1\n"
             "- Đã liên kết Google Sheet",
       "1. Đổi tên C1 thành「上級者向けトレーニング」và đổi cả `system_name`\n"
       "2. Kiểm 3 booking cũ ở màn quản lý và màn lịch sử phía LINE user\n"
       "3. Kiểm remind có filter theo C1 còn hiệu lực không\n"
       "4. Kiểm cột コース trên Google Sheet của booking cũ\n"
       "5. Tạo course MỚI đặt đúng tên cũ「初心者向けトレーニング」→ kiểm 3 booking cũ",
       "1 course đổi tên + 1 course trùng tên cũ",
       "- Bước 2, 3, 4: mọi liên kết vẫn trỏ đúng course C1 (theo `course_id`), hiển thị TÊN MỚI\n"
       "- Bước 5: 3 booking cũ VẪN thuộc C1, KHÔNG bị nhận nhầm sang course mới trùng tên\n"
       "- Remind filter vẫn gắn đúng C1",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm DATA-ID-001. Corpus có TC đổi tên course nhưng KHÔNG có nhánh "
            "'tạo course mới trùng tên cũ' — đây là chỗ lộ ra nếu code dùng tên thay vì id."),

    # ── DEPLOY-ASSET-001 / DEPLOY-LIVE-001 ──
    tc("Phân quyền & môi trường", "DEPLOY-ASSET-001", "Abnormal",
       "Sau release: file JS/CSS của màn quản lý calendar và LIFF phải nhận bản mới",
       CAL + "\n- Vừa release phiên bản mới có sửa `calendar_detail.js` (258 KB) và "
             "`booking_news/booking.js`",
       "1. Mở màn quản lý calendar bằng trình duyệt ĐÃ TỪNG vào trước release (không xóa cache)\n"
       "2. Mở DevTools → tab Network → kiểm URL của `calendar_detail.js` có tham số version mới không\n"
       "3. Thao tác 1 chức năng vừa sửa → kiểm hoạt động đúng bản mới\n"
       "4. Lặp với LIFF phía LINE user (mở lại link booking từ app LINE)",
       "Trình duyệt còn cache bản cũ",
       "- File JS/CSS được nạp có chuỗi version/hash MỚI (không dùng lại bản cache cũ)\n"
       "- Chức năng vừa sửa hoạt động đúng, không văng lỗi JS\n"
       "- LIFF phía LINE user cũng nhận bản mới (LIFF là SPA Vue nên rất dễ kẹt cache)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm DEPLOY-ASSET-001. Corpus KHÔNG có TC nào. "
            "Rủi ro cao vì spec §3.2 xác nhận toàn bộ LIFF là SPA Vue 2 một trang."),

    tc("Phân quyền & môi trường", "DEPLOY-LIVE-001", "Abnormal",
       "Release KHÔNG lock maintain: LINE user đang booking dở giữa lúc deploy",
       CAL,
       "1. Cho U1 vào màn booking, chọn slot, đang ở bước nhập form\n"
       "2. Trong lúc đó thực hiện deploy (không bật maintain)\n"
       "3. U1 bấm tiếp để hoàn tất booking → quan sát\n"
       "4. Query `calendar_course_bookings` và `calendar_course_receptions`\n"
       "5. Lặp với admin đang ở bước approve hàng loạt",
       "Deploy giữa lúc có giao dịch",
       "- U1 hoặc hoàn tất được booking, hoặc nhận thông báo lỗi rõ ràng để làm lại\n"
       "- TUYỆT ĐỐI KHÔNG được có booking rác: bản ghi tạo dở không có history, "
       "không có remind, bộ đếm `total_booking` lệch\n"
       "- Admin approve hàng loạt: các booking đã xử lý giữ nguyên, không xử lý nửa vời",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm DEPLOY-LIVE-001. 🔴 Rủi ro rất cao vì spec §11.1 TOP-7 (RA-01): "
            "**KHÔNG có DB transaction ở BẤT KỲ luồng ghi nào** — `CCBS::create()` ghi 12 nhóm "
            "trên 8 bảng, lỗi giữa chừng ⇒ booking tồn tại nhưng không history, không remind, "
            "không thông báo."),

    # ── ENV-002 — Đồng bộ thời điểm cấu hình hạ tầng ──
    tc("決済 — UnivaPay & webhook", "ENV-002", "Abnormal",
       "Đổi cấu hình hạ tầng (Webhook URL / LIFF domain) trong lúc đang có giao dịch",
       CAL + "\n- Calendar ENABLE bill UnivaPay, có booking đang chờ callback",
       "1. Cho U1 booking có bill tiền (booking rơi vào `status_webhook` = 0)\n"
       "2. Trong lúc chờ callback, đổi Webhook URL cấu hình phía UnivaPay\n"
       "3. Chờ callback → query `status_webhook` của booking\n"
       "4. Lặp kịch bản đổi LIFF domain trong lúc U1 đang mở màn booking",
       "Đổi cấu hình giữa chừng",
       "- Callback cũ vẫn tới được endpoint cũ HOẶC có cơ chế nhận diện và xử lý\n"
       "- Booking KHÔNG bị kẹt vĩnh viễn ở `status_webhook` ∈ {0, 4}\n"
       "- U1 đang mở LIFF: hoặc hoàn tất được, hoặc báo lỗi rõ để mở lại",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="TC LẤP GAP — quan điểm ENV-002. Liên quan MT-49 (booking kẹt status_webhook = 4 bị "
            "khóa vĩnh viễn) và MT-51 (thiếu Webhook ID). Cần Leader xác nhận có test được không."),

    # ── INTG-LINE-001 — Lỗi từ LINE API / LIFF / webhook ──
    tc("予約・キャンセル アクション", "INTG-LINE-001", "Abnormal",
       "LINE Messaging API trả lỗi khi gửi action booking → hệ thống xử lý ra sao",
       CAL + "\n- Calendar đã setting message + multi action lúc booking\n"
             "- Chuẩn bị được cách làm LINE API trả lỗi (token hết hạn / vượt quota / user đã unfollow)",
       "1. Cho U1 booking khi LINE API đang trả lỗi\n"
       "2. Query `calendar_course_bookings` → booking có được tạo không\n"
       "3. Mở màn エラーメッセージ của tool\n"
       "4. Query bộ đếm `total_booking` / `total_approve`\n"
       "5. Kiểm remind có được add vào `event_step_time` không",
       "LINE API lỗi",
       "- Booking VẪN được tạo và bộ đếm VẪN đúng (không rollback vì lỗi gửi tin)\n"
       "- Lỗi gửi tin được ghi nhận ở màn エラーメッセージ, có nội dung truy được booking nào\n"
       "- Remind vẫn được add bình thường\n"
       "- KHÔNG được: booking mất, hoặc bộ đếm lệch, hoặc lỗi im lặng không ghi ở đâu",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm INTG-LINE-001. Corpus có nhắc màn エラーメッセージ ở TC vượt "
            "5000 ký tự (Setting calendar r37) nhưng KHÔNG có TC nào cho lỗi LINE API nói chung."),

    # ── MEDIA-CLEAN-001 — Dọn file trên server ──
    tc("コース — tạo/sửa/xóa", "MEDIA-CLEAN-001", "Normal",
       "Dọn file ảnh trên server khi thay ảnh / xóa course / xóa calendar",
       CAL + "\n- Course C1 đã upload ảnh A; màn トップ設定 và ビジネス情報 đã upload ảnh B, C",
       "1. Thay ảnh của C1 từ A sang A2 → kiểm file A còn trên server / B2 không\n"
       "2. Bấm icon xóa ảnh của C1 → kiểm file A2\n"
       "3. Xóa course C1 → kiểm file ảnh của C1\n"
       "4. Xóa cả calendar → kiểm file B, C và toàn bộ ảnh course",
       "3 ảnh trên 3 màn",
       "- Sau mỗi bước, file ảnh KHÔNG còn được tham chiếu phải được dọn khỏi server (local + B2)\n"
       "- Ảnh còn đang dùng KHÔNG bị xóa nhầm\n"
       "- Nếu hệ thống KHÔNG dọn: ghi nhận là nợ kỹ thuật, ước lượng dung lượng rác/tháng",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm MEDIA-CLEAN-001. Corpus có TC upload/thay ảnh nhưng KHÔNG có TC "
            "nào kiểm file cũ trên server. Spec §5 danh sách 26 bảng không nhắc bảng quản lý file."),

    # ── MSG-001 — Lọc người nhận gửi ĐÚNG đối tượng ──
    tc("空き枠通知受け取り設定", "MSG-001", "Abnormal",
       "空き枠通知 chỉ gửi cho user của ĐÚNG slot, ĐÚNG bot — không gửi lan sang slot/bot khác",
       CAL + "\n- Bot A có slot S1 và S2 (khác course), bot B có slot S3\n"
             "- U1 chờ hủy ở S1 · U2 chờ hủy ở S2 · U3 chờ hủy ở S3 (bot B)",
       "1. Cho slot S1 có chỗ trống\n2. Kiểm LINE app của U1, U2 và U3\n"
       "3. Query `messages_v2` / lịch sử chat của 3 user",
       "3 user, 3 slot, 2 bot",
       "- CHỈ U1 nhận thông báo có chỗ trống\n- U2 (khác slot cùng bot) KHÔNG nhận\n"
       "- U3 (khác bot) KHÔNG nhận\n- Không có bản ghi gửi tin nào cho U2, U3",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm MSG-001. Corpus có Setting calendar r1206 (chỉ gửi cho user đang "
            "chờ) nhưng KHÔNG có nhánh cách ly theo slot và theo bot."),

    # ── MSG-004 — Preview admin khớp nội dung nhận thật ──
    tc("予約・キャンセル アクション", "MSG-004", "Normal",
       "Preview message ở màn hub PHẢI khớp nội dung tin LINE user nhận thật",
       CAL + "\n- Message booking đã chèn: {name} · 5 mã thông tin booking · 2 friend info · emoji · "
             "xuống dòng · URL hủy",
       "1. Mở màn hub 予約・キャンセル → tab メッセージ của thẻ 予約 → chụp màn preview\n"
       "2. Cho U1 booking → chụp tin LINE U1 nhận được\n"
       "3. So sánh từng dòng: nội dung · thứ tự · xuống dòng · emoji · giá trị đã thay mã",
       "Message đầy đủ mọi loại nội dung",
       "- Preview và tin thật KHỚP về nội dung và thứ tự dòng\n"
       "- Điểm khác biệt HỢP LỆ duy nhất: preview hiện mã (ví dụ「予約日時挿入」) còn tin thật hiện "
       "giá trị đã thay — nếu preview cũng thay giá trị thì phải khớp giá trị của U1\n"
       "- Emoji và xuống dòng hiển thị giống nhau ở cả 2 nơi",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm MSG-004. Corpus có TC preview (Setting calendar r8-r20) và TC "
            "gửi tin riêng, nhưng KHÔNG có TC ĐỐI CHIẾU 2 bên."),

    # ── MSG-005 — Giới hạn số tin theo tháng ──
    tc("予約・キャンセル アクション", "MSG-005", "Normal",
       "Mọi tin FA-019 gửi đi đều tính vào hạn mức tin nhắn của bot",
       CAL + "\n- Bot A có hạn mức gửi tin theo tháng, đang gần chạm hạn\n"
             "- Ghi lại `bots.free_send_count` trước khi test",
       "1. Cho U1 booking (nhận tin action booking) → query `bots.free_send_count`\n"
       "2. Cho remind gửi → query lại\n3. Cho 空き枠通知 gửi → query lại\n"
       "4. Admin approve 1 booking (gửi tin approve) → query lại\n"
       "5. Đối chiếu với màn thống kê số tin đã gửi trong tháng của tool\n"
       "6. Khi đã chạm hạn mức: cho U2 booking → kiểm tin có gửi được không",
       "Bot gần chạm hạn mức",
       "- Mỗi tin gửi đi làm `free_send_count` tăng ĐÚNG 1\n"
       "- Số liệu khớp với màn thống kê số tin đã gửi của tool\n"
       "- Khi chạm hạn: tin KHÔNG gửi được nhưng booking VẪN thành công (không chặn nghiệp vụ)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm MSG-005, suy từ spec **BR-48 / BR-P34** (mọi tin từ FA-019 đều "
            "tăng `bots.free_send_count += 1` và gọi `updateMessageSendCount(botId, hôm nay, 3, 1)`). "
            "⚠️ Spec **RP-11**: dùng `$bot->free_send_count + 1` thay vì `DB::raw` ⇒ **LOST UPDATE** "
            "khi gửi đồng thời — nên bổ sung nhánh gửi nhiều tin cùng lúc rồi đếm lại."),

    # ── MSG-USER-001 — LINE user lifecycle ──
    tc("LINE user — mở link & entry", "MSG-USER-001", "Abnormal",
       "Vòng đời LINE user: booking → unfollow → follow lại → booking đó còn không?",
       CAL + "\n- U1 đã có 2 booking (1 tương lai, 1 quá khứ) và 1 đăng ký chờ hủy",
       "1. U1 UNFOLLOW bot A → query `bot_line_user` và `calendar_course_bookings` của U1\n"
       "2. Chờ tới giờ remind của booking tương lai → kiểm U1 có nhận không\n"
       "3. Admin mở màn quản lý → kiểm booking của U1 còn hiển thị không\n"
       "4. U1 FOLLOW lại bot A → mở màn lịch sử booking\n"
       "5. Chờ remind tiếp theo → kiểm",
       "1 user unfollow rồi follow lại",
       "- Bước 1: booking của U1 KHÔNG bị xóa khỏi DB\n"
       "- Bước 2: KHÔNG gửi remind cho user đã unfollow (hoặc gửi lỗi và ghi nhận, không crash job)\n"
       "- Bước 3: admin VẪN thấy booking của U1\n"
       "- Bước 4: U1 thấy lại đúng lịch sử booking cũ của mình\n"
       "- Bước 5: remind chưa gửi VẪN gửi được sau khi follow lại",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm MSG-USER-001. Corpus có TC entry sau unfollow (Booking phía line "
            "user r21-r23) nhưng KHÔNG theo dõi vòng đời của DỮ LIỆU BOOKING qua unfollow/follow."),

    # ── PAY-BATCH-001 — Batch re-check trạng thái mới nhất ──
    tc("リクエスト一括操作", "PAY-BATCH-001", "Abnormal",
       "Approve hàng loạt: trạng thái booking đổi ở tab khác giữa lúc batch đang chạy",
       CAL + "\n- Calendar ENABLE bill tiền, setting リクエスト制\n"
             "- 5 booking đang リクエスト: B1…B5",
       "1. Tab 1: tick cả 5 booking, bấm approve hàng loạt\n"
       "2. Trong lúc batch đang chạy, tab 2: cho U (chủ B3) tự HỦY booking B3\n"
       "3. Chờ batch xong → query trạng thái 5 booking và dashboard cổng thanh toán\n"
       "4. Lặp kịch bản: trong lúc batch chạy, admin ở tab 2 cancel B4",
       "5 booking, 1 đổi trạng thái giữa chừng",
       "- Batch PHẢI đọc lại trạng thái MỚI NHẤT của từng booking trước khi xử lý\n"
       "- B3 đã bị hủy: KHÔNG bị approve lại, KHÔNG bị thu tiền\n"
       "- 4 booking còn lại approve và thu tiền bình thường\n"
       "- Trên cổng thanh toán chỉ có 4 giao dịch",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm PAY-BATCH-001. Corpus có TC approve hàng loạt (Quản lý "
            "calendar_new r407-r448) nhưng KHÔNG có nhánh trạng thái đổi giữa chừng. "
            "Rủi ro cao vì spec RA-01: không có DB transaction."),

    # ── PAY-PLAN-001 — Đổi gói: reset trạng thái & quyền ──
    tc("Giới hạn theo plan", "PAY-PLAN-001", "Abnormal",
       "Hạ gói pro → free khi đang có 10 calendar, 5 course và bill tiền đang bật",
       "- Bot C gói **pro**, có 10 lesson calendar, mỗi calendar có 5 course\n"
       "- 1 calendar đang ENABLE bill tiền và có booking chưa thanh toán xong",
       "1. Hạ gói bot C từ pro xuống free\n"
       "2. Mở màn list calendar → quan sát bộ đếm và 10 calendar cũ\n"
       "3. Mở 1 calendar → quan sát 5 course và tab 決済連携\n"
       "4. LINE user mở link booking của các calendar cũ\n"
       "5. Query `calendar_management.is_use_payment` của calendar đang bật bill\n"
       "6. Cho user thử booking course có giá",
       "Bot hạ gói pro → free",
       "- 10 calendar cũ KHÔNG bị xóa, nhưng bộ đếm hiển thị vượt hạn (10/1)\n"
       "- KHÔNG tạo được calendar mới\n"
       "- Tab 決済連携 bị tắt / báo cần upgrade\n"
       "- 🔴 Điểm quan trọng: user KHÔNG được bị thu tiền nữa dù `is_use_payment` trong DB "
       "vẫn = 1 — nếu vẫn thu ⇒ FAIL, raise bug (spec BR-P21)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="TC LẤP GAP — quan điểm PAY-PLAN-001. Corpus KHÔNG có TC hạ gói. "
            "Liên quan MT-44 (BR-P21: `is_use_payment` bị ép 0 chỉ trên object PHP, DB không đổi ⇒ "
            "client gửi `checkHasPayment=true` thì server vẫn thu tiền). DỰ KIẾN FAIL ở bước 6."),

    # ── PERM-004 — Thu hồi/đổi quyền có hiệu lực đúng thời điểm ──
    tc("Phân quyền & môi trường", "PERM-004", "Abnormal",
       "Thu hồi quyền レッスン予約 của staff trong lúc staff đang mở màn quản lý",
       CAL + "\n- Staff S1 đang được cấp quyền route レッスン予約 và đang mở màn quản lý calendar",
       "1. Admin chính thu hồi quyền レッスン予約 của S1\n"
       "2. S1 (KHÔNG reload trang) bấm approve 1 booking → quan sát\n"
       "3. S1 bấm xóa 1 slot → quan sát\n4. S1 reload trang → quan sát\n"
       "5. Query DB xem có thao tác nào lọt qua không",
       "Thu hồi quyền giữa chừng",
       "- Bước 2, 3: thao tác PHẢI bị từ chối ở tầng SERVER (không chỉ ẩn menu)\n"
       "- Bước 4: S1 không vào được màn quản lý nữa\n"
       "- DB: KHÔNG có thao tác nào của S1 sau thời điểm thu hồi quyền",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="TC LẤP GAP — quan điểm PERM-004. Corpus KHÔNG có TC nào. Liên quan MT-43 (Gap G-01: "
            "chưa xác minh được dữ liệu phân quyền) và MT-63 (A-01: 17 route /ajax/calendar/* "
            "nằm ngoài cơ chế phân quyền)."),

    # ── REG-RUN-001 — Dữ liệu / job đang chạy dở khi release ──
    tc("リマインド — job gửi & recover", "REG-RUN-001", "Abnormal",
       "Restart job gửi remind trong lúc đang có bản ghi status = 1 (đã nhặt, chưa gửi)",
       CAL + "\n- Có ≥ 50 bản ghi `event_step_time` sắp tới giờ gửi\n"
             "- Có quyền restart tiến trình `NewEventRemindTask`",
       "1. Đợi tới đúng lúc job đang xử lý (có bản ghi `status` = 1) rồi RESTART job\n"
       "2. Query `SELECT status, COUNT(*) FROM event_step_time GROUP BY status`\n"
       "3. Chờ job chạy lại xong → query lại\n"
       "4. Đếm số tin LINE user thực nhận và so với số bản ghi",
       "50 bản ghi sắp gửi",
       "- Sau restart: các bản ghi `status` = 1 được NẠP LẠI vào hàng đợi, không kẹt vĩnh viễn\n"
       "- Cuối cùng mọi bản ghi về `status` = 2 (đã gửi)\n"
       "- Số tin user nhận = số bản ghi (KHÔNG gửi trùng, KHÔNG mất)",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm REG-RUN-001, suy từ spec §10.2: "
            "「`NewEventRemindTask:54-61` nạp lại toàn bộ bản ghi `status = 1` vào queue trước khi vào "
            "vòng lặp ⇒ tránh kẹt vĩnh viễn. ⚠ **`RequestSentQueue` KHÔNG có cơ chế này** (RJ-02)」. "
            "Liên quan Gap G-04 (chưa đếm được số bản ghi kẹt thật trên production)."),

    tc("リマインド — job gửi & recover", "REG-RUN-001", "Abnormal",
       "Job giám sát overbooking thoát hẳn khi gặp exception (try-catch nằm ngoài while)",
       CAL + "\n- Có quyền theo dõi tiến trình `MonitorCalendarBookingTask` và phòng Chatwork nhận cảnh báo",
       "1. Tạo tình huống overbooking thật (slot 定員 1 nhưng có 3 booking status 1)\n"
       "2. Chờ ≤ 60 giây → kiểm phòng Chatwork có cảnh báo không\n"
       "3. Tạo tình huống làm job văng exception (ví dụ `job_config_daily` id = 1 bị xóa)\n"
       "4. Sau đó tạo tiếp 1 overbooking mới → chờ 5 phút → kiểm Chatwork",
       "Overbooking + exception",
       "- Bước 2: nhận được cảnh báo Chatwork\n"
       "- Bước 4: 🔴 nếu KHÔNG nhận được cảnh báo nữa ⇒ job đã thoát hẳn và không tự khởi động lại "
       "⇒ FAIL, raise bug (mất khả năng giám sát overbooking mà không ai biết)",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="TC LẤP GAP — suy từ spec §10.6: 🔴「`MonitorCalendarBookingTask:22-35` — "
            "**try-catch nằm NGOÀI `while(true)`** ⇒ một ngoại lệ làm **thread thoát hẳn**, "
            "không có watchdog khởi động lại ⇒ cảnh báo overbooking **im lặng ngừng hoạt động** "
            "(RJ-03)」. Ngoài ra RJ-04: `findById(1).orElse(null)` có NPE tiềm tàng."),

    # ── REG-SPEC-001 — Spec thay đổi giữa chừng ──
    tc("リマインド — job gửi & recover", "REG-SPEC-001", "Abnormal",
       "Dữ liệu tạo TRƯỚC và SAU spec change #32367 cùng tồn tại — hành vi phải nhất quán",
       CAL + "\n- Có booking cũ (tạo TRƯỚC release #32367, remind SAU tính theo START time)\n"
             "- Có booking mới (tạo SAU release, remind SAU tính theo END time)\n"
             "- Cả 2 booking cùng course, cùng khung giờ, khác ngày",
       "1. Query `event_step_time.sent_date_time` của cả 2 booking\n"
       "2. Chờ tới giờ remind của từng booking → kiểm tin LINE user nhận\n"
       "3. So sánh thời điểm nhận tin thực tế với giờ kết thúc buổi học\n"
       "4. Chạy `recover:remindLesson` → query lại cả 2",
       "2 booking 2 thế hệ dữ liệu",
       "- Trước recover: booking cũ gửi remind SAU lệch so với booking mới (đúng như mô tả bug)\n"
       "- Sau recover: CẢ HAI booking đều có `sent_date_time` tính theo END time, "
       "user nhận tin đúng thời điểm như nhau\n"
       "- KHÔNG có booking nào bị gửi 2 lần hoặc mất remind",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm REG-SPEC-001. Corpus có TC recover từng nhánh (Setting calendar "
            "r1070-r1093) nhưng KHÔNG có TC ĐỐI CHIẾU 2 thế hệ dữ liệu chạy song song."),

    # ── REG-URL-001 — URL đã phát cho khách không được đổi ──
    tc("LINE user — mở link & entry", "REG-URL-001", "Abnormal",
       "URL booking / lịch sử / hủy đã gửi cho khách phải giữ nguyên hiệu lực sau release",
       CAL + "\n- Đã gửi cho U1 các link: URL booking, URL lịch sử, キャンセル用URL của 1 booking\n"
             "- Đã chèn link booking vào 1 rich menu và 1 template đang dùng",
       "1. Lưu lại 3 URL đã gửi cho U1 (và URL trong rich menu / template)\n"
       "2. Sau khi release phiên bản mới, U1 mở lại từng URL cũ\n"
       "3. U1 bấm vào rich menu và mở tin nhắn template cũ\n"
       "4. Kiểm mọi URL có mở đúng màn tương ứng không",
       "5 URL đã phát ra ngoài",
       "- TẤT CẢ URL cũ vẫn mở đúng màn (booking / lịch sử / hủy)\n"
       "- KHÔNG có URL nào trả 404 hoặc redirect sai calendar\n"
       "- Rich menu và template cũ vẫn hoạt động",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="TC LẤP GAP — quan điểm REG-URL-001. Corpus KHÔNG có TC nào. "
            "Rủi ro thật: URL đã nằm trong tin nhắn LINE của khách, không thể gửi lại. "
            "Liên quan MT-64 (backup rich menu chứa link lesson)."),

    # ── SEC-002 — Không lộ token / thông tin thanh toán ──
    tc("Đồng thời & verify API", "SEC-002", "Abnormal",
       "🔴 Rà rò rỉ token OAuth Google, mã xóa calendar và thông tin thẻ trong response API",
       CAL + "\n- Calendar đã liên kết Google Sheet (có `google_sheet_access_token`)\n"
             "- Đã từng bấm gửi mã xóa calendar (có `code_delete`)\n"
             "- Có booking đã thanh toán (có `last4`, `payment_card_expired`, `charge_id`)",
       "1. Mở DevTools → Network, thao tác qua các màn: list calendar · detail calendar · "
       "tab 全体設定 · màn Google連携 · màn xóa calendar · detail booking đã thanh toán\n"
       "2. Với mỗi response JSON, tìm các chuỗi: `access_token` · `refresh_token` · `id_token` · "
       "`code_delete` · `charge_id` · số thẻ đầy đủ\n"
       "3. Kiểm cả response của API phía LIFF (LINE user)",
       "Calendar có đủ dữ liệu nhạy cảm",
       "- KHÔNG response nào chứa `google_sheet_access_token` / `refresh_token` / `id_token`\n"
       "- KHÔNG response nào trả `code_delete`\n"
       "- Thông tin thẻ chỉ được trả dạng che (`XXXXXXXX1234`), KHÔNG có số thẻ đầy đủ\n"
       "- ⚠️ Theo spec §11.1 TOP-5 và TOP-6: `code_delete` bị **trả THẲNG trong response** và "
       "`google_sheet_access_token` lưu **JSON OAuth THÔ không mã hoá** ⇒ TC này DỰ KIẾN FAIL",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 TC LẤP GAP — quan điểm SEC-002. Suy từ spec §11.1 TOP-5 (A-05: `'code' => $code`, "
            "`CalendarManagementController.php:670`) và TOP-6 (token OAuth thô — dữ liệu thật "
            "27/174 lịch có giá trị; A-07/A-08 trả **toàn bộ bản ghi** `calendar_management`). "
            "DỰ KIẾN FAIL. Xem MT-63."),

    # ── SEC-ISO-001 — Cách ly dữ liệu đa phiên ──
    tc("Phân quyền & môi trường", "SEC-ISO-001", "Abnormal",
       "Cách ly đa phiên: 2 admin khác bot đăng nhập cùng trình duyệt / 2 LINE user cùng thiết bị",
       "- Admin X quản lý bot A, admin Y quản lý bot B (2 tài khoản khác nhau)\n"
       "- 2 LINE user U1, U2 dùng chung 1 thiết bị (đăng xuất/đăng nhập LINE)",
       "1. Trình duyệt 1: admin X đăng nhập bot A, mở màn quản lý calendar\n"
       "2. Cùng trình duyệt, tab mới: đăng xuất X rồi đăng nhập Y (bot B)\n"
       "3. Quay lại tab 1 (chưa reload) → thao tác approve 1 booking → query DB\n"
       "4. Trên điện thoại: U1 mở link booking, đặt lịch xong; đăng xuất LINE, đăng nhập U2\n"
       "5. U2 mở màn lịch sử booking của cùng calendar",
       "2 phiên admin + 2 phiên LINE user",
       "- Bước 3: thao tác của tab 1 hoặc bị từ chối (phiên đã đổi), hoặc ghi đúng vào bot A — "
       "TUYỆT ĐỐI KHÔNG ghi nhầm sang bot B\n"
       "- Bước 5: U2 CHỈ thấy booking của chính U2, KHÔNG thấy booking của U1",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="🔴 TC LẤP GAP — quan điểm SEC-ISO-001. Corpus có TC đổi bot 2 tab (Quản lý calendar_new "
            "r981-r982) nhưng KHÔNG có nhánh 2 TÀI KHOẢN khác nhau và 2 LINE user cùng thiết bị. "
            "Spec §1.3: LINE user **không xác thực** — danh tính chỉ dựa vào `line_user_id`/`uCode` "
            "client gửi ⇒ bước 5 có rủi ro thật."),
]
