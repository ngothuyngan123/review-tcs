# -*- coding: utf-8 -*-
"""FA-008 メッセージ配信 — Nhóm 14-17: 送信者名 (quản lý profile người gửi và
áp dụng khi gửi), 配信先絞込み & 再計算, 配信数 & danh sách friend đã gửi.

Nguồn 送信者名 áp dụng khi gửi: TCsLine_Improve chung → tab「Profile sender」
(12/2025, Bug KH #33072/#33052) — bản mới nhất về hành vi profile sender.
"""
from _common import tc

B2 = ("- Đăng nhập Admin, đã tạo broadcast bước 1 thành công\n"
      "- Đang ở màn SCR-BC-04 (/basic/add-broadcast-v2?broadcast_id=XXX)")
P = B2 + "\n- Đã mở popup「送信者名」bằng nút「設定」"

S3 = [
    # ═══════════ 14. 送信者名 — quản lý profile ═══════════
    tc("送信者名 — quản lý profile", "UI-FIELD-001", "Normal",
       "Trường 送信者名 mặc định hiển thị avatar và tên của LOA",
       B2,
       "1. Quan sát khối「送信者名」khi vừa vào màn SCR-BC-04\n"
       "2. So avatar và tên với thông tin LOA ở màn cài đặt bot",
       "Bot chưa tạo profile tùy chỉnh nào",
       "- Hiển thị avatar và tên đúng bằng avatar/tên của LINE Official Account\n"
       "- Avatar hiển thị đúng tỉ lệ, KHÔNG bị méo/vỡ hình\n"
       "- Bảng broadcast: profile_id = NULL",
       note="Nguồn: r122, r449 — r122 ghi nhận『vỡ avt』, file 03/tab function r77 ghi『avt bị biến dạng』. "
            "TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa fix → cần raise bug."),

    tc("送信者名 — quản lý profile", "CONC-002", "Abnormal",
       "Double click nút「設定」của 送信者名 — chỉ mở 1 popup",
       B2,
       "1. Double click nhanh vào nút「設定」ở khối「送信者名」\n"
       "2. Quan sát số popup mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 popup cài đặt người gửi",
       note="Nguồn: r123, r450."),

    tc("送信者名 — quản lý profile", "UI-001", "Normal",
       "Popup cài đặt 送信者名 hiển thị đúng design",
       P,
       "1. Quan sát toàn bộ popup: danh sách profile, nút thêm mới, nút lưu, icon sửa/xóa\n"
       "2. Đối chiếu với design",
       "Bot có 2 profile tùy chỉnh",
       "- Bố cục, màu sắc, vị trí nút khớp design\n"
       "- Có nút「送信者追加」, nút「保存」, mỗi dòng có icon sửa và xóa",
       note="Nguồn: r124, r451. ⚠️ TC từ 02/2024 — CẦN VERIFY LẠI design còn hiệu lực."),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Thêm profile mới — hiển thị ở CUỐI danh sách",
       P + "\n- Đang có 2 profile tùy chỉnh A và B",
       "1. Bấm「送信者追加」\n"
       "2. Nhập tên「送信者C」và chọn avatar\n"
       "3. Bấm「登録」\n"
       "4. Đọc thứ tự danh sách profile",
       "Tên「送信者C」, ảnh PNG 200×200",
       "- Profile C xuất hiện ở CUỐI danh sách (sau A và B)\n"
       "- Bảng bots_profiles có bản ghi mới với nick_name =「送信者C」",
       note="Nguồn: r125-r126, r452-r453."),

    tc("送信者名 — quản lý profile", "MEDIA-IMG-001", "Normal",
       "Thêm profile với ảnh PNG — upload thành công và hiển thị đúng",
       P,
       "1. Bấm「送信者追加」, nhập tên\n"
       "2. Upload ảnh định dạng PNG\n"
       "3. Bấm「登録」\n"
       "4. Quan sát avatar trong danh sách và ở khối「送信者名」",
       "Ảnh PNG 200×200, < 1MB",
       "- Ảnh PNG được chấp nhận, không báo lỗi định dạng\n"
       "- Avatar hiển thị đúng ảnh vừa upload ở cả danh sách và khối 送信者名",
       env="PRODUCTION",
       note="Nguồn: r126, r453 — r126 ghi nhận『không update đc avt』, file 03/tab function r79 ghi "
            "『không up được ảnh dạng png』. TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa fix → "
            "raise bug. RULE-08: media → PRODUCTION."),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Thêm profile chỉ nhập tên, không chọn avatar",
       P,
       "1. Bấm「送信者追加」\n"
       "2. Chỉ nhập tên「名前のみ」, không chọn ảnh\n"
       "3. Bấm「登録」",
       "Tên「名前のみ」, không avatar",
       "- Đăng ký thành công\n"
       "- Avatar dùng ảnh mặc định (của LOA hoặc ảnh trống theo design)",
       note="Nguồn: r127, r454."),

    tc("送信者名 — quản lý profile", "UI-INPUT-001", "Abnormal",
       "Thêm profile không nhập gì — hiện alert, không tạo bản ghi",
       P,
       "1. Bấm「送信者追加」\n"
       "2. Không nhập tên, không chọn ảnh\n"
       "3. Bấm「登録」\n"
       "4. Đếm số profile trong danh sách",
       "Tên = trống, không avatar",
       "- Hiện alert báo thiếu thông tin\n"
       "- Số profile trong danh sách KHÔNG tăng\n"
       "- Bảng bots_profiles không có bản ghi mới",
       note="Nguồn: r128, r455."),

    tc("送信者名 — quản lý profile", "UI-FIELD-001", "Normal",
       "Mặc định profile đang tích là bot đang đăng nhập, chỉ tích được 1",
       P + "\n- Bot có 3 profile tùy chỉnh",
       "1. Quan sát profile nào đang được tích\n"
       "2. Thử tích thêm 1 profile khác\n"
       "3. Đếm số profile đang tích",
       "3 profile tùy chỉnh + profile mặc định của bot",
       "- Mặc định tích profile của bot đang đăng nhập\n"
       "- Khi tích profile khác, profile cũ tự bỏ tích — luôn chỉ có đúng 1 được tích",
       note="Nguồn: r129, r456."),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Đổi profile người gửi rồi bấm「保存」— khối 送信者名 cập nhật",
       P + "\n- Bot có profile「送信者A」",
       "1. Tích chọn「送信者A」\n"
       "2. Bấm「保存」\n"
       "3. Quan sát khối「送信者名」ở màn SCR-BC-04\n"
       "4. Mở lại popup kiểm tra profile nào đang tích",
       "Chọn「送信者A」",
       "- Khối「送信者名」hiển thị avatar và tên của「送信者A」\n"
       "- Mở lại popup vẫn thấy「送信者A」đang được tích\n"
       "- Bảng broadcast: profile_id = id của「送信者A」",
       note="Nguồn: r130, r457 — file 03/tab function r78 ghi nhận bug『chọn xong nhưng ra ngoài lại vẫn "
            "hiển thị avt cũ, click vào thì k thấy tick cái tên nào』. TC viết theo hành vi ĐÚNG."),

    tc("送信者名 — quản lý profile", "STATE-CLEAN-001", "Abnormal",
       "Đổi profile nhưng KHÔNG bấm「保存」— giữ nguyên profile cũ",
       P + "\n- Broadcast đang dùng profile mặc định của bot",
       "1. Tích chọn「送信者A」\n"
       "2. Đóng popup mà KHÔNG bấm「保存」\n"
       "3. Quan sát khối「送信者名」\n"
       "4. Mở lại popup kiểm tra profile đang tích",
       "Chọn「送信者A」nhưng không lưu",
       "- Khối「送信者名」vẫn là profile mặc định của bot\n"
       "- Mở lại popup: profile mặc định vẫn đang được tích\n"
       "- Bảng broadcast: profile_id vẫn NULL",
       note="Nguồn: r131, r458."),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Sửa thông tin profile rồi bấm「登録」— cập nhật thành công",
       P + "\n- Bot có profile「送信者A」với avatar cũ",
       "1. Bấm icon sửa ở「送信者A」\n"
       "2. Đổi tên thành「送信者A2」và đổi avatar\n"
       "3. Bấm「登録」\n"
       "4. Đọc lại danh sách",
       "「送信者A」→「送信者A2」, avatar mới",
       "- Danh sách hiển thị「送信者A2」với avatar mới\n"
       "- Bảng bots_profiles: nick_name đã đổi",
       note="Nguồn: r132, r459 — file 03/tab function r82 ghi nhận『chưa focus vào phần edit』."),

    tc("送信者名 — quản lý profile", "STATE-CLEAN-001", "Abnormal",
       "Sửa profile nhưng KHÔNG bấm「登録」— không lưu thay đổi",
       P + "\n- Bot có profile「送信者A」",
       "1. Bấm icon sửa ở「送信者A」\n"
       "2. Đổi tên thành「送信者XYZ」\n"
       "3. Đóng form sửa mà KHÔNG bấm「登録」\n"
       "4. Đọc lại danh sách",
       "「送信者A」→ nhập「送信者XYZ」nhưng không lưu",
       "- Danh sách vẫn là「送信者A」\n"
       "- Bảng bots_profiles: nick_name không đổi",
       note="Nguồn: r133, r460."),

    tc("送信者名 — quản lý profile", "UI-001", "Normal",
       "Xóa profile — hiện alert xác nhận đúng nguyên văn",
       P + "\n- Bot có profile「送信者A」",
       "1. Bấm icon xóa ở「送信者A」\n"
       "2. Đọc nội dung alert",
       "Xóa「送信者A」",
       "- Hiện alert chứa câu「を削除しますがよろしいですか？」\n"
       "- Alert có nút xác nhận và nút hủy",
       note="Nguồn: r134, r461."),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Xác nhận xóa profile — profile biến mất khỏi danh sách",
       P + "\n- Bot có 3 profile A, B, C",
       "1. Bấm icon xóa ở「送信者B」\n"
       "2. Bấm xác nhận trên alert\n"
       "3. Đọc lại danh sách\n"
       "4. Đóng và mở lại popup",
       "3 profile A, B, C → xóa B",
       "- Danh sách còn A và C, KHÔNG còn B\n"
       "- Mở lại popup vẫn không thấy B (không phải chỉ ẩn tạm ở FE)",
       note="Nguồn: r135, r462 — file 03/tab function r80 ghi nhận bug『xóa success nhưng k mất tên người "
            "bị xóa』. TC viết theo hành vi ĐÚNG."),

    tc("送信者名 — quản lý profile", "STATE-CLEAN-001", "Abnormal",
       "Hủy xóa profile ở alert — profile vẫn còn",
       P + "\n- Bot có 3 profile A, B, C",
       "1. Bấm icon xóa ở「送信者B」\n"
       "2. Bấm nút hủy trên alert\n"
       "3. Đọc lại danh sách",
       "3 profile A, B, C",
       "- Danh sách vẫn đủ 3 profile A, B, C",
       note="Nguồn: r136, r463."),

    tc("送信者名 — quản lý profile", "DATA-REF-001", "Normal",
       "Xóa profile đang được broadcast sử dụng — broadcast fallback về profile mặc định",
       P + "\n- Broadcast đang dùng profile「送信者A」",
       "1. Chọn「送信者A」cho broadcast và lưu\n"
       "2. Mở lại popup, xóa「送信者A」\n"
       "3. Quan sát khối「送信者名」ở màn SCR-BC-04\n"
       "4. Gửi broadcast và kiểm tra tên/avatar phía app LINE",
       "Broadcast dùng「送信者A」, sau đó xóa A",
       "- Khối「送信者名」quay về hiển thị avatar/tên của LOA\n"
       "- Bảng broadcast: profile_id chuyển về NULL\n"
       "- Friend nhận tin với tên/avatar của LOA, không lỗi gửi",
       env="PRODUCTION",
       note="Nguồn: feature-spec.md §5 BR-05 (『Khi xoá profile đang dùng → broadcast tự động fallback về "
            "default』). ⚠️ Corpus KHÔNG có TC cho nhánh này — TC do AI bổ sung từ spec, cần Leader xác nhận.",
       group="Data"),

    tc("送信者名 — quản lý profile", "FUNC-001", "Normal",
       "Sắp xếp thứ tự profile trong danh sách",
       P + "\n- Bot có 3 profile A, B, C theo thứ tự đó",
       "1. Kéo profile C lên vị trí đầu\n"
       "2. Bấm lưu\n"
       "3. Đóng và mở lại popup, đọc thứ tự",
       "3 profile A, B, C → kéo C lên đầu",
       "- Thứ tự sau khi lưu là C, A, B\n"
       "- Mở lại popup vẫn giữ thứ tự C, A, B",
       note="Nguồn: r137, r464."),

    tc("送信者名 — quản lý profile", "STATE-CLEAN-001", "Abnormal",
       "Sắp xếp lại profile nhưng không lưu — giữ thứ tự cũ",
       P + "\n- Bot có 3 profile A, B, C",
       "1. Kéo profile C lên đầu\n"
       "2. Đóng popup không lưu\n"
       "3. Mở lại popup, đọc thứ tự",
       "Kéo C lên đầu nhưng không lưu",
       "- Thứ tự vẫn là A, B, C",
       note="Nguồn: r138, r465."),

    tc("送信者名 — quản lý profile", "LIST-001", "Normal",
       "Danh sách profile ít bản ghi — không có scroll",
       P + "\n- Bot có 3 profile",
       "1. Mở popup「送信者名」\n"
       "2. Quan sát khung danh sách",
       "3 profile",
       "- Toàn bộ 3 profile hiển thị hết, không có thanh cuộn\n"
       "- Popup không bị giãn quá cao",
       note="Nguồn: r139, r466."),

    tc("送信者名 — quản lý profile", "LIST-001", "Boundary",
       "Danh sách profile nhiều bản ghi — có scroll trong khung popup",
       P + "\n- Bot có ≥20 profile",
       "1. Mở popup「送信者名」\n"
       "2. Cuộn trong khung danh sách tới profile cuối cùng",
       "20 profile",
       "- Khung danh sách có thanh cuộn riêng\n"
       "- Cuộn tới cuối vẫn đọc và thao tác được profile cuối\n"
       "- Popup không tràn ra ngoài màn hình",
       note="Nguồn: r140, r467 — file 03/tab function r81 ghi kết quả NG『chưa có』(chưa có scroll). "
            "TC viết theo hành vi ĐÚNG, dự kiến FAIL nếu chưa fix → cần raise bug."),

    tc("送信者名 — quản lý profile", "PERM-001", "Normal",
       "Staff chỉ quản lý được profile của chính mình",
       "- Bot có 2 staff S1 và S2, mỗi người đã tạo 1 profile riêng\n"
       "- Admin cũng có 1 profile riêng",
       "1. Đăng nhập bằng staff S1\n"
       "2. Vào broadcast → mở popup「送信者名」\n"
       "3. Đọc danh sách profile hiển thị\n"
       "4. Thử sửa/xóa profile của S2 và của Admin",
       "3 profile: của Admin, của S1, của S2",
       "- S1 chỉ tạo/sửa/xóa được profile của chính S1\n"
       "- Không sửa/xóa được profile của S2 hoặc của Admin (ẩn hoặc chặn)\n"
       "- Gọi thẳng API sửa/xóa profile của S2 cũng bị từ chối",
       spec="Đã hỏi leader",
       note="Nguồn: feature-spec.md §5 BR-05 (『Staff chỉ tạo/quản lý profile của chính mình』). "
            "⚠️ Corpus KHÔNG có TC cho nhánh này — TC do AI bổ sung từ spec, cần Leader xác nhận cách "
            "hệ thống thể hiện (ẩn hẳn hay hiện nhưng disable).",
       group="API"),

    # ═══════════ 15. 送信者名 — áp dụng khi gửi ═══════════
    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi bằng profile của bot gốc — friend thấy tên/avatar của bot",
       B2 + "\n- Broadcast dùng profile mặc định (profile_id = NULL)\n- Có 1 friend test",
       "1. Thêm tin nhắn loại パネル・ボタン (button standard)\n"
       "2. Mở「プレビューとテスト」, gửi test cho friend\n"
       "3. Mở app LINE của friend, xem tên và avatar người gửi\n"
       "4. Mở chat 1:1 trên web của admin, xem profile hiển thị",
       "Template button standard, profile = bot gốc",
       "- App LINE: tên và avatar hiển thị là của bot gốc\n"
       "- Chat 1:1 trên web: cũng hiển thị profile bot gốc",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r82-r83, r98-r99. RULE-07: khớp cả app LINE và chat 1:1. "
            "RULE-08: media/profile ảnh → PRODUCTION.",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi test bằng profile sender tùy chỉnh — friend thấy tên/avatar của profile đã chọn",
       B2 + "\n- Broadcast đã chọn profile「送信者A」\n- Có 1 friend test",
       "1. Thêm tin nhắn, chọn profile「送信者A」\n"
       "2. Gửi test qua modal preview cho friend\n"
       "3. Mở app LINE của friend xem tên và avatar\n"
       "4. Mở chat 1:1 trên web xem profile",
       "Profile「送信者A」với avatar riêng · lần lượt các loại template: text · sticker · location · media · "
       "giới thiệu (cũ) · button standard 1 panel · button standard nhiều panel · button color · button image · button quick",
       "- Với TẤT CẢ 10 loại template trên: app LINE hiển thị tên và avatar của「送信者A」\n"
       "- Chat 1:1 trên web cũng hiển thị「送信者A」",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r84-r95, r100-r110. Gộp 10 loại template vào 1 TC vì "
            "CÙNG 1 kết quả mong đợi; liệt kê đủ ở cột Dữ liệu nhập.",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Sửa avatar/tên profile đang chọn rồi gửi — friend thấy thông tin ĐÃ SỬA",
       B2 + "\n- Broadcast đang chọn profile「送信者A」",
       "1. Mở popup「送信者名」, sửa tên và avatar của「送信者A」\n"
       "2. Lưu, quay lại gửi test cho friend\n"
       "3. Mở app LINE và chat 1:1 xem tên/avatar",
       "「送信者A」→ đổi tên và ảnh mới · template button standard",
       "- App LINE và chat 1:1 hiển thị tên/avatar MỚI vừa sửa\n"
       "- Không còn hiển thị thông tin cũ (không bị cache)",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r96, r111.",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Đổi sang profile sender khác rồi gửi — friend thấy profile mới",
       B2 + "\n- Broadcast đang chọn profile「送信者A」, bot còn profile「送信者B」",
       "1. Đổi sang「送信者B」, lưu\n"
       "2. Gửi test cho friend\n"
       "3. Mở app LINE và chat 1:1 xem tên/avatar",
       "Đổi「送信者A」→「送信者B」· template button standard",
       "- App LINE và chat 1:1 hiển thị「送信者B」\n"
       "- Không còn dấu vết của「送信者A」",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r97, r112.",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Gửi bằng quick test ở màn list — profile sender áp dụng đúng",
       "- Broadcast wait_to_send đã chọn profile「送信者A」\n- Đã tick 1 friend làm quick tester",
       "1. Ở màn list tab「配信予約」, bấm avatar quick test của broadcast\n"
       "2. Mở app LINE của friend xem tên/avatar người gửi\n"
       "3. Mở chat 1:1 trên web xem profile",
       "Quick test 1 friend · profile「送信者A」· template button color / button image",
       "- App LINE và chat 1:1 hiển thị đúng「送信者A」\n"
       "- Không dùng nhầm profile bot gốc",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r98-r112 (khối『Send test bằng button quicktest ở màn "
            "list broadcast』).",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Normal",
       "Job gửi broadcast thật — profile sender áp dụng đúng cho mọi loại template",
       "- Broadcast wait_to_send đã chọn profile「送信者A」, đặt lịch sau 10 phút\n"
       "- Đối tượng nhận có ≥2 friend",
       "1. Đợi job gửi tới giờ\n"
       "2. Mở app LINE của từng friend xem tên/avatar người gửi\n"
       "3. Mở chat 1:1 trên web, bấm nút「詳細情報」xem profile\n"
       "4. Lặp lại với profile mặc định của bot",
       "Profile「送信者A」· các loại template: location · media · giới thiệu (cũ) · button standard 1 panel · "
       "button standard nhiều panel · button color · button image · button quick",
       "- Chọn profile sender: app LINE và chat 1:1 đều hiển thị「送信者A」\n"
       "- Chọn profile bot: app LINE và chat 1:1 đều hiển thị tên/avatar bot\n"
       "- Với TẤT CẢ các loại template liệt kê, kết quả như nhau",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r157-r164 (khối『Test job / Send all』). "
            "⚠️ Cột kết quả ghi『Chat 1:1 thì Send all hiển thị profile khi click vào button 詳細情報』— "
            "tức profile KHÔNG hiện trực tiếp ở bong bóng chat mà phải bấm 詳細情報. Xem MT-09.",
       group="API"),

    tc("送信者名 — áp dụng khi gửi", "MSG-002", "Abnormal",
       "Gửi test ở màn detail broadcast — không được lỗi「The request body has 1 error(s)」",
       B2 + "\n- Broadcast dùng profile bot gốc, đã thêm template button",
       "1. Mở màn detail của broadcast\n"
       "2. Mở modal preview, bấm「テスト送信」cho 1 friend\n"
       "3. Quan sát thông báo trả về\n"
       "4. Kiểm tra app LINE của friend",
       "Template button standard / button quick · profile bot gốc",
       "- Gửi thành công, hiện thông báo thành công\n"
       "- KHÔNG xuất hiện lỗi「The request body has 1 error(s)」\n"
       "- Friend nhận được tin nhắn",
       env="PRODUCTION",
       note="Nguồn: Improve chung/Profile sender r82-r83 — cột kết quả ghi rõ『Send test ở màn detail "
            "broadcast bị lỗi: \"The request body has 1 error(s)\"』. TC viết theo hành vi ĐÚNG, "
            "dự kiến FAIL nếu chưa fix → cần raise bug.",
       group="API"),

    # ═══════════ 16. 配信先絞込み & 再計算 ═══════════
    tc("配信先絞込み & 再計算", "UI-FIELD-001", "Normal",
       "Mặc định 配信先絞込み tích「すべての友だち」",
       B2,
       "1. Quan sát khối「配信先絞込み」khi vừa vào màn\n"
       "2. Kiểm tra trạng thái nút「設定」và「再計算」",
       "—",
       "- Radio「すべての友だち」đang được tích\n"
       "- Nút「設定」và「再計算」ở trạng thái disable",
       note="Nguồn: r141, r468."),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Normal",
       "Chọn すべての友だち — cột 配信数 = tổng bạn bè của bot (trừ người đã block)",
       B2 + "\n- Bot có 10 bạn bè, trong đó 2 người đã block bot",
       "1. Giữ nguyên「すべての友だち」\n"
       "2. Đọc số ở cột「配信数」\n"
       "3. Đối chiếu với số bạn bè ở màn「友だちリスト」",
       "10 bạn bè, 2 người block (is_blocked=1)",
       "- 配信数 hiển thị 8 (không tính 2 người đã block)\n"
       "- Số khớp với số bạn bè đang hoạt động ở màn 友だちリスト",
       note="Nguồn: r142, r469 + feature-spec.md §2 bước 2 (『Đếm totalUser (bot_line_user không bị block)』)."),

    tc("配信先絞込み & 再計算", "UI-FIELD-001", "Normal",
       "Tích「絞り込み」— enable nút 設定 và 再計算",
       B2,
       "1. Tích radio「絞り込み」\n"
       "2. Quan sát trạng thái nút「設定」và「再計算」",
       "—",
       "- Cả 2 nút chuyển sang enable, bấm được",
       note="Nguồn: r143, r470."),

    tc("配信先絞込み & 再計算", "CONC-002", "Abnormal",
       "Double click nút「設定」của 配信先絞込み — chỉ mở 1 popup filter",
       B2 + "\n- Đã tích「絞り込み」",
       "1. Double click nhanh vào nút「設定」\n"
       "2. Quan sát số popup mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 popup filter (SCR-BC-03)",
       note="Nguồn: r144, r471."),

    tc("配信先絞込み & 再計算", "REG-SHARED-001", "Normal",
       "Popup filter dùng chung vẫn hoạt động đủ 11 loại điều kiện",
       B2 + "\n- Đã tích「絞り込み」và mở popup filter",
       "1. Mở popup filter\n"
       "2. Đếm và đọc tên từng loại điều kiện lọc\n"
       "3. Thử đặt 1 điều kiện của mỗi loại rồi lưu",
       "11 loại: tag · tên bạn bè · ngày thêm bạn · trạng thái step · QR code action · conversion · "
       "xác nhận · thông tin bạn bè · trạng thái xử lý · affiliate · bạn mới/cũ",
       "- Popup hiển thị đủ 11 loại điều kiện\n"
       "- Mỗi loại đặt và lưu được, không lỗi\n"
       "- Sau khi lưu, khối dưới hiển thị đúng điều kiện đã đặt",
       note="Nguồn: r145, r472 + feature-spec.md §5 BR-06 · ui-spec.md §SCR-BC-03. "
            "Chi tiết từng loại filter thuộc shared component SC-003 — xem phần loại trừ."),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Normal",
       "Đặt filter thành công — 配信数 hiển thị đúng số người thỏa điều kiện",
       B2 + "\n- Bot có 10 bạn bè, 4 người có tag T",
       "1. Tích「絞り込み」→「設定」\n"
       "2. Đặt điều kiện: có tag T\n"
       "3. Lưu popup\n"
       "4. Đọc số ở cột「配信数」\n"
       "5. Đối chiếu bằng cách lọc tag T ở màn「友だちリスト」",
       "Tag T gắn cho 4 friend, không ai block",
       "- 配信数 hiển thị 4\n"
       "- Khối phía dưới hiển thị điều kiện filter và kết quả\n"
       "- Số khớp với số friend lọc được ở màn 友だちリスト",
       note="Nguồn: r146-r147, r473-r474."),

    tc("配信先絞込み & 再計算", "CONC-002", "Abnormal",
       "Double click nút「再計算」— chỉ tính 1 lần",
       B2 + "\n- Đã đặt filter, 配信数 đang hiển thị 4",
       "1. Double click nhanh vào「再計算」\n"
       "2. Mở DevTools → tab Network đếm số request\n"
       "3. Đọc số 配信数",
       "Double click trong < 1 giây",
       "- Chỉ gửi 1 request tính lại\n"
       "- 配信数 hiển thị đúng 1 giá trị, không nhấp nháy đổi 2 lần",
       note="Nguồn: r148, r476.",
       group="API"),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Normal",
       "Bấm「再計算」sau khi số friend thỏa filter thay đổi — cập nhật đúng số mới",
       B2 + "\n- Broadcast đã đặt filter tag T, 配信数 đang là 4",
       "1. Ghi lại 配信数 hiện tại = 4\n"
       "2. Sang màn「友だちリスト」, gắn thêm tag T cho 2 friend nữa\n"
       "3. Quay lại broadcast, bấm「再計算」\n"
       "4. Đọc lại 配信数",
       "Tag T: 4 friend → thêm 2 friend = 6",
       "- 配信数 cập nhật thành 6\n"
       "- Bảng broadcast: filter_number = 6, filter_date được cập nhật",
       note="Nguồn: r149, r477 + logic-spec.md:97-103."),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Normal",
       "「再計算」cũng cập nhật số cho các mốc gửi con",
       B2 + "\n- Broadcast 3 mốc gửi, filter tag T, 配信数 đang là 4",
       "1. Gắn thêm tag T cho 2 friend\n"
       "2. Bấm「再計算」ở mốc cha\n"
       "3. Về màn list, đọc 配信数 của cả 3 dòng (cha + 2 con)",
       "Tag T: 4 → 6 friend · broadcast 3 mốc gửi",
       "- Cả 3 dòng đều hiển thị 配信数 = 6\n"
       "- Bảng broadcast: filter_number của các bản ghi con cũng = 6",
       note="Nguồn: logic-spec.md:102 (『Cũng cập nhật cho children broadcasts (cùng parent_id)』). "
            "⚠️ Corpus không test trực tiếp nhánh này — TC do AI bổ sung từ spec, cần Leader xác nhận.",
       group="Data"),

    tc("配信先絞込み & 再計算", "STATE-DEP-001", "Normal",
       "Chưa tạo broadcast — đặt filter rồi chuyển về すべての友だち thì xóa hết điều kiện",
       B2.replace("- Đã tạo broadcast bước 1 thành công\n", "") +
       "\n- Đang ở màn tạo mới SCR-BC-02, CHƯA bấm lưu lần nào",
       "1. Tích「絞り込み」, đặt điều kiện tag T, lưu popup\n"
       "2. Tích lại「すべての友だち」→ đọc 配信数\n"
       "3. Tích lại「絞り込み」→ mở popup xem điều kiện còn không",
       "Filter tag T, chưa lưu broadcast",
       "- Bước 2: 配信数 hiển thị tổng số bạn bè (all)\n"
       "- Bước 3: điều kiện filter đã bị XÓA HẾT, popup rỗng",
       note="Nguồn: file 03/tab「test filte」r6-r7 (『kh chưa tạo broad cast … filte xong tick sang all "
            "friend → hiển thị sl all; sau đấy lại tick lại thu hẹp → hiển thị sl all, xóa bỏ hết đk lọc "
            "trước đó』)."),

    tc("配信先絞込み & 再計算", "STATE-DEP-001", "Normal",
       "ĐÃ tạo broadcast — đặt filter rồi chuyển về すべての友だち thì GIỮ điều kiện cũ",
       B2 + "\n- Broadcast đã lưu, đã đặt filter tag T",
       "1. Ở màn edit, tích「すべての友だち」→ đọc 配信数\n"
       "2. Tích lại「絞り込み」→ mở popup xem điều kiện",
       "Broadcast đã lưu, filter tag T",
       "- Bước 1: 配信数 hiển thị số đã filter (KHÔNG phải all)\n"
       "- Bước 2: popup vẫn giữ nguyên điều kiện tag T",
       spec="Đã hỏi leader",
       note="Nguồn: file 03/tab「test filte」r12-r13 (『Khi tạo xong broad cast … filte xong tick sang all "
            "friend → sau đấy lại tick lại thu hẹp → hiển thị sl đã filte, vẫn giữ đk lọc trước đó』). "
            "⚠️ MT-05 — hành vi KHÁC hẳn trường hợp chưa tạo broadcast, và r6 nói『hiển thị sl all』còn "
            "r12 nói『hiển thị sl đã filte』cho cùng thao tác tick sang all friend."),

    tc("配信先絞込み & 再計算", "STATE-DEP-001", "Normal",
       "Đặt filter rồi chuyển sang すべての友だち trước khi lưu — broadcast lưu là KHÔNG filter",
       B2.replace("- Đã tạo broadcast bước 1 thành công\n", "") +
       "\n- Đang ở màn tạo mới SCR-BC-02",
       "1. Tích「絞り込み」, đặt điều kiện tag T, lưu popup\n"
       "2. Tích lại「すべての友だち」\n"
       "3. Bấm lưu broadcast\n"
       "4. Mở lại broadcast, kiểm tra 配信先絞込み",
       "Filter tag T rồi chuyển về all trước khi lưu",
       "- Broadcast lưu ở trạng thái KHÔNG filter\n"
       "- Bảng broadcast: flag_setting_filter = 0\n"
       "- Màn list hiển thị「未設定（全員）」ở cột 配信先絞込み",
       note="Nguồn: r815 (Bug #32229, 02/10/2025).",
       group="Data"),

    tc("配信先絞込み & 再計算", "STATE-DEP-001", "Normal",
       "Tích 絞り込み nhưng KHÔNG thêm điều kiện nào — broadcast lưu là KHÔNG filter",
       B2.replace("- Đã tạo broadcast bước 1 thành công\n", "") +
       "\n- Đang ở màn tạo mới SCR-BC-02",
       "1. Tích「絞り込み」\n"
       "2. Mở popup nhưng KHÔNG thêm điều kiện nào, đóng popup\n"
       "3. Bấm lưu broadcast\n"
       "4. Kiểm tra 配信先絞込み ở màn list",
       "Tích 絞り込み, 0 điều kiện",
       "- Bảng broadcast: flag_setting_filter = 0 (không filter)\n"
       "- Màn list hiển thị「未設定（全員）」\n"
       "- Broadcast gửi cho toàn bộ bạn bè",
       note="Nguồn: r811 (Bug #32229).",
       group="Data"),

    tc("配信先絞込み & 再計算", "STATE-DEP-001", "Normal",
       "Đặt filter rồi XÓA hết điều kiện trước khi lưu — broadcast lưu là KHÔNG filter",
       B2.replace("- Đã tạo broadcast bước 1 thành công\n", "") +
       "\n- Đang ở màn tạo mới SCR-BC-02",
       "1. Tích「絞り込み」, đặt điều kiện tag T, lưu popup\n"
       "2. Mở lại popup, xóa toàn bộ điều kiện, lưu popup\n"
       "3. Bấm lưu broadcast\n"
       "4. Kiểm tra 配信先絞込み",
       "Filter tag T → xóa hết điều kiện",
       "- Bảng broadcast: flag_setting_filter = 0\n"
       "- Màn list hiển thị「未設定（全員）」",
       note="Nguồn: r814 (Bug #32229).",
       group="Data"),

    tc("配信先絞込み & 再計算", "CONC-003", "Abnormal",
       "Mở 2 tab tạo mới — tab có filter và tab không filter lưu độc lập, không lẫn nhau",
       "- Đăng nhập Admin, mở 2 tab trình duyệt cùng vào /basic/add-broadcast-v2",
       "1. Tab 1: nhập tiêu đề「フィルタあり」, tích 絞り込み, đặt điều kiện tag T\n"
       "2. Tab 2: nhập tiêu đề「フィルタなし」, giữ すべての友だち\n"
       "3. Lưu tab 1 trước, rồi lưu tab 2\n"
       "4. Về màn list kiểm tra 配信先絞込み của cả 2 broadcast",
       "2 tab: tab1 filter tag T, tab2 không filter",
       "- Broadcast「フィルタあり」có filter (設定済み)\n"
       "- Broadcast「フィルタなし」không filter (未設定（全員）)\n"
       "- 2 bản ghi độc lập, không đè filter lên nhau",
       note="Nguồn: r816 (Bug #32229 — nguyên nhân gốc là copy broadcast có filter bị gửi cho all friend).",
       group="API"),

    tc("配信先絞込み & 再計算", "CONC-003", "Abnormal",
       "Sửa cùng 1 broadcast trên 2 tab — tab lưu sau ghi đè theo dữ liệu tab đó",
       "- Có broadcast「編集テスト」status draft, ban đầu KHÔNG filter\n"
       "- Mở 2 tab trình duyệt cùng vào màn edit của broadcast đó",
       "1. Tab 1: chuyển sang「絞り込み」, đặt điều kiện tag T, lưu\n"
       "2. Tab 2 (mở từ trước, chưa reload): giữ「すべての友だち」, bấm lưu\n"
       "3. Reload màn list, đọc 配信先絞込み",
       "Tab1 lưu có filter trước · Tab2 lưu không filter sau",
       "- Kết quả cuối là KHÔNG filter (tab 2 ghi đè)\n"
       "- Không sinh bản ghi filter mồ côi trong bảng filters_v2",
       note="Nguồn: r831. Cặp đối chứng ở r832: nếu tab 1 lưu KHÔNG filter trước rồi tab 2 lưu có filter, "
            "kết quả vẫn là KHÔNG filter vì『khi save tab 1 đã xóa các đk filter cũ rồi』— xem MT-08.",
       group="API"),

    tc("配信先絞込み & 再計算", "STATE-CLEAN-001", "Abnormal",
       "Sửa filter rồi bấm Back về màn list mà không lưu broadcast — filter VẪN được lưu",
       B2 + "\n- Broadcast「編集テスト」status draft, ban đầu KHÔNG filter",
       "1. Mở màn edit, tích「絞り込み」, đặt điều kiện tag T, bấm lưu ở POPUP filter\n"
       "2. KHÔNG bấm lưu broadcast, bấm「メッセージ配信一覧に戻る」\n"
       "3. Mở lại broadcast, kiểm tra 配信先絞込み",
       "Lưu popup filter nhưng không lưu broadcast",
       "- Broadcast VẪN ở trạng thái có filter tag T\n"
       "- Lý do: bấm lưu ở modal filter đã ghi filter vào DB ngay",
       spec="Đã hỏi leader",
       note="Nguồn: r833 (『không lưu thay đổi => Case này sẽ vẫn lưu là có filter vì khi nhấn save ở "
            "modal đã lưu filter rồi』) + file 03/tab function r122 (『filter người nhận, template edit là "
            "được lưu lại luôn không cần nhấn lưu』). ⚠️ Hành vi này dễ gây hiểu nhầm cho người dùng — "
            "xem MT-10.",
       group="Data"),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Normal",
       "Friend bị block sau khi đặt filter — bấm 再計算 thì số giảm đúng",
       B2 + "\n- Broadcast filter tag T, 配信数 = 5",
       "1. Ghi lại 配信数 = 5\n"
       "2. Cho 1 friend trong nhóm đó block bot (hoặc set is_blocked=1)\n"
       "3. Bấm「再計算」\n"
       "4. Đọc lại 配信数, bấm vào số để xem danh sách friend",
       "Tag T = 5 friend, 1 người block",
       "- 配信数 cập nhật thành 4\n"
       "- Danh sách friend khi bấm vào số cũng còn 4 người, không có người đã block",
       note="Nguồn: file 03/tab「test filte」r14-r16."),

    tc("配信先絞込み & 再計算", "DATA-COUNT-001", "Abnormal",
       "Friend bỏ block nhưng CHƯA bấm 再計算 — số ngoài màn list lệch với danh sách chi tiết",
       B2 + "\n- Broadcast filter tag T, 配信数 = 4 (1 người đang block)",
       "1. Cho friend đang block bỏ block bot\n"
       "2. KHÔNG bấm「再計算」\n"
       "3. Đọc số 配信数 ở màn list\n"
       "4. Bấm vào số để mở danh sách friend, đếm số dòng",
       "Tag T = 5 friend, 1 người vừa bỏ block",
       "- Ghi nhận rõ số ngoài màn list và số trong danh sách chi tiết\n"
       "- Nếu 2 số lệch nhau → đây là hành vi cache filter_number, phải bấm「再計算」mới đồng bộ",
       spec="Đã hỏi leader",
       note="Nguồn: file 03/tab「test filte」r17 (『sl bên ngoài vẫn như cũ nhưng khi click vào thì ra sl "
            "không khớp vs bên ngoài』). ⚠️ MT-11 — corpus ghi kết quả OK cho hành vi LỆCH SỐ; cần Leader "
            "chốt đây là bug hay hành vi chấp nhận được.",
       group="Data"),

    tc("配信先絞込み & 再計算", "BULK-001", "Boundary",
       "Số điều kiện filter AND/OR tối đa — vượt giới hạn hiện thông báo",
       B2 + "\n- Đã tích「絞り込み」và mở popup filter",
       "1. Thêm lần lượt điều kiện vào nhóm AND cho tới khi đạt giới hạn\n"
       "2. Thêm thêm 1 điều kiện nữa → ghi lại thông báo\n"
       "3. Lặp lại với nhóm OR\n"
       "4. Thử kết hợp: AND đầy rồi thêm OR, và ngược lại",
       "Ma trận: AND < giới hạn · AND = giới hạn · AND > giới hạn · OR < / = / > giới hạn · "
       "AND đầy + OR < / = / > giới hạn · OR đầy + AND < / = / > giới hạn",
       "- Khi vượt giới hạn: hiện đúng thông báo「これ以上追加できません。」\n"
       "- Khi bằng hoặc dưới giới hạn: thêm được bình thường\n"
       "- Nhóm AND và OR đếm giới hạn ĐỘC LẬP với nhau",
       spec="Đã hỏi leader",
       note="Nguồn: Improve chung/tab「Improve sendall scenario」r22-r34. ⚠️ MT-12 — tiêu đề khối ghi "
            "『filter and và or ko add quá 100 item』nhưng phần test thực tế chỉ chạy với mốc 5 item "
            "(『test với mỗi cái 5 item』). Cần Leader chốt con số giới hạn thật."),

    tc("配信先絞込み & 再計算", "UI-001", "Normal",
       "Nhiều điều kiện filter — popup preview và modal lưu có scroll, không vỡ layout",
       B2 + "\n- Broadcast đã đặt nhiều điều kiện filter (đủ để tràn khung)",
       "1. Ở màn edit, bấm「プレビューとテスト」→ xem khối filter\n"
       "2. Bấm「配信内容を確認して送信に進む」→ xem modal xác nhận\n"
       "3. Về màn list, mở preview ở tab「配信予約」·「下書き」·「配信履歴」\n"
       "4. Ở mỗi chỗ, kiểm tra khối filter có cuộn được không",
       "≥10 điều kiện filter",
       "- Ở cả 5 vị trí, khối filter có thanh cuộn riêng\n"
       "- Popup/modal không bị tràn ra ngoài màn hình\n"
       "- Đọc được điều kiện cuối cùng sau khi cuộn",
       note="Nguồn: file 03/tab function r221-r226 (Bug #29301, 25/03/2025 — 『Broadcast: Hiển thị lỗi "
            "khi có quá nhiều filter』)."),

    # ═══════════ 17. 配信数 & danh sách friend đã gửi ═══════════
    tc("配信数 & danh sách friend đã gửi", "UI-001", "Normal",
       "Hover vào số ở cột 配信数 — hiện popover có nút tính lại",
       "- Có broadcast wait_to_send ở tab「配信予約」",
       "1. Mở tab「配信予約」\n"
       "2. Rê chuột vào số ở cột「配信数」\n"
       "3. Quan sát popover hiện ra",
       "1 broadcast wait_to_send",
       "- Hiện popover chứa nút「現時点での配信予定数を再計算」\n"
       "- Popover KHÔNG biến mất khi di chuột từ số sang nút\n"
       "- Nội dung popover khớp design",
       note="Nguồn: r245-r246, r694-r695 + r927-r928 (Bug KH #36730, 25/05/2026 — nút biến mất khi di "
            "cursor, nguyên nhân style top của popover sai). Đây là bản ghi MỚI NHẤT về hành vi này."),

    tc("配信数 & danh sách friend đã gửi", "UI-001", "Normal",
       "Hover ở bản ghi ĐẦU TIÊN của bảng — popover không bị che, thao tác được",
       "- Tab「配信予約」có ≥2 trang bản ghi",
       "1. Ở trang 1, hover vào 配信数 của bản ghi ĐẦU TIÊN\n"
       "2. Di chuột sang nút「現時点での配信予定数を再計算」và bấm\n"
       "3. Lặp lại ở trang 2",
       "Bản ghi đầu tiên, trang 1 và trang 2",
       "- Popover hiện đủ, không bị header bảng che\n"
       "- Bấm được nút tính lại, số cập nhật theo friend mới nhất thỏa filter",
       note="Nguồn: r937-r938 (Bug KH #36730)."),

    tc("配信数 & danh sách friend đã gửi", "UI-001", "Normal",
       "Hover ở bản ghi CUỐI CÙNG của bảng — popover không bị tràn khỏi khung",
       "- Tab「下書き」có ≥2 trang bản ghi",
       "1. Ở trang 1, hover vào 配信数 của bản ghi CUỐI CÙNG\n"
       "2. Di chuột sang nút tính lại và bấm\n"
       "3. Lặp lại ở trang cuối cùng",
       "Bản ghi cuối cùng, trang 1 và trang cuối",
       "- Popover hiện đủ, không bị cắt bởi mép dưới khung bảng\n"
       "- Bấm được nút tính lại, số cập nhật đúng",
       note="Nguồn: r948-r949 (Bug KH #36730)."),

    tc("配信数 & danh sách friend đã gửi", "COMPAT-BROWSER-001", "Normal",
       "Hover popover hoạt động trên Safari (Mac) và Chrome (Windows)",
       "- Có broadcast wait_to_send\n- Chuẩn bị 2 máy: Mac + Safari, Windows + Chrome",
       "1. Trên Mac/Safari: hover vào 配信数, bấm nút tính lại\n"
       "2. Trên Windows/Chrome: làm tương tự\n"
       "3. So sánh hành vi 2 môi trường",
       "Safari trên macOS · Chrome trên Windows",
       "- Cả 2 trình duyệt đều hiện popover và bấm được nút tính lại\n"
       "- Số cập nhật đúng ở cả 2\n"
       "- Không có khác biệt về vị trí popover gây che khuất nút",
       note="Nguồn: r936, r947 (Bug KH #36730)."),

    tc("配信数 & danh sách friend đã gửi", "CONC-002", "Abnormal",
       "Double click nhanh nút「現時点での配信予定数を再計算」— chỉ tính 1 lần",
       "- Có broadcast wait_to_send, filter tag T = 5 friend",
       "1. Hover vào 配信数, double click nhanh vào nút tính lại\n"
       "2. Mở DevTools → Network đếm số request\n"
       "3. Đọc số 配信数",
       "Double click trong < 1 giây",
       "- Chỉ 1 request được gửi\n"
       "- 配信数 hiển thị đúng 5, không nhấp nháy hoặc sai số",
       note="Nguồn: r247, r696, r939, r950 — r247 ghi nhận『về sl người mặc định』(bị reset sai). "
            "TC viết theo hành vi ĐÚNG.",
       group="API"),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Bấm nút tính lại ở màn list — lấy số friend mới nhất thỏa filter",
       "- Broadcast wait_to_send filter tag T, 配信数 đang hiển thị 3\n"
       "- Test cả 4 tổ hợp: gửi ngay/đặt lịch × có filter/không filter",
       "1. Ghi lại 配信数 hiện tại\n"
       "2. Gắn thêm tag T cho 2 friend\n"
       "3. Hover vào 配信数 → bấm「現時点での配信予定数を再計算」\n"
       "4. Đọc lại số\n"
       "5. Lặp lại cho tổ hợp: gửi ngay+không filter, gửi ngay+có filter, đặt lịch+không filter, đặt lịch+có filter",
       "4 tổ hợp: send ngay/đặt lịch × có/không filter · tag T từ 3 → 5 friend",
       "- Với tổ hợp CÓ filter: số cập nhật từ 3 lên 5\n"
       "- Với tổ hợp KHÔNG filter: số = tổng bạn bè hiện tại của bot\n"
       "- Cả 4 tổ hợp đều tính lại được, không lỗi",
       note="Nguồn: r929-r932, r940-r943 (Bug KH #36730). 4 tổ hợp gộp 1 TC vì cùng 1 kết quả "
            "『lấy số friend mới nhất thỏa mãn』; liệt kê đủ ở Dữ liệu nhập."),

    tc("配信数 & danh sách friend đã gửi", "CONC-002", "Abnormal",
       "Double click vào SỐ ở cột 配信数 — chỉ mở danh sách 1 lần",
       "- Có broadcast wait_to_send, 配信数 = 5",
       "1. Double click nhanh vào số 5\n"
       "2. Quan sát số trang/tab mở ra",
       "Double click trong < 1 giây",
       "- Chỉ mở 1 trang danh sách friend\n"
       "- Danh sách hiển thị đúng 5 friend",
       note="Nguồn: r249, r698 — r249 ghi nhận『hiển thị sai số ng dự định send』. TC viết theo hành vi ĐÚNG."),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Bấm vào số 配信数 — danh sách friend đúng bằng số hiển thị",
       "- Có broadcast wait_to_send, filter tag T, 配信数 = 5",
       "1. Bấm vào số 5 ở cột「配信数」\n"
       "2. Đếm số dòng trong danh sách friend hiện ra\n"
       "3. Đối chiếu từng người với danh sách lọc tag T ở màn「友だちリスト」",
       "Tag T = 5 friend",
       "- Danh sách có đúng 5 dòng\n"
       "- Danh sách người trùng khớp hoàn toàn với kết quả lọc tag T",
       note="Nguồn: r223, r337, r706."),

    tc("配信数 & danh sách friend đã gửi", "FUNC-001", "Normal",
       "Bấm vào 1 friend trong danh sách — chuyển sang màn friendlist",
       "- Đang mở danh sách friend của 1 broadcast",
       "1. Bấm vào tên 1 friend trong danh sách\n"
       "2. Quan sát màn hình mở ra",
       "1 friend bất kỳ trong danh sách",
       "- Chuyển sang màn「友だちリスト」\n"
       "- Hiển thị đúng thông tin của friend vừa bấm",
       note="Nguồn: r934, r945 (Bug KH #36730)."),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Broadcast ĐÃ GỬI — 配信数 lấy theo send_count, không tính lại theo filter",
       "- Broadcast delivered gửi cho 5 friend (filter tag T lúc gửi có 5 người)",
       "1. Sau khi broadcast gửi xong, ghi lại 配信数 ở tab「配信履歴」= 5\n"
       "2. Gắn thêm tag T cho 3 friend mới (thành 8 người thỏa filter)\n"
       "3. Đọc lại 配信数 của broadcast đã gửi\n"
       "4. Bấm vào số, đếm danh sách friend",
       "Lúc gửi: 5 friend · sau khi gửi: thêm 3 friend thỏa filter",
       "- 配信数 vẫn hiển thị 5 (số thực gửi), KHÔNG đổi thành 8\n"
       "- Danh sách friend có đúng 5 người đã nhận\n"
       "- Bảng broadcast: send_count = 5",
       note="Nguồn: r707-r711 (Bug #31527, 07/2025 — 『check count lấy theo send_count bảng broadcast』). "
            "⚠️ MT-13 — r222/r336 ghi ngược lại『spect tính count vẫn như cũ (k count theo send_count)』"
            "cho tab 概要 ở màn preview. Cần Leader chốt.",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Broadcast đã gửi KHÔNG có filter — send_count đúng tổng số bạn bè lúc gửi",
       "- Broadcast delivered gửi cho すべての友だち, lúc gửi bot có 8 bạn bè",
       "1. Ghi lại số bạn bè của bot ngay trước giờ gửi = 8\n"
       "2. Sau khi gửi xong, đọc 配信数 ở tab「配信履歴」\n"
       "3. Thêm 2 bạn bè mới cho bot\n"
       "4. Đọc lại 配信数",
       "8 bạn bè lúc gửi, thêm 2 người sau khi gửi",
       "- 配信数 = 8 ngay sau khi gửi\n"
       "- Sau khi thêm 2 bạn bè mới, 配信数 vẫn là 8 (không đổi thành 10)",
       note="Nguồn: r710 (Bug #31527).",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Copy broadcast — send_count của bản copy tính riêng, không kế thừa bản gốc",
       "- Broadcast gốc delivered với send_count = 5",
       "1. Copy broadcast đó\n"
       "2. Bản copy nằm ở tab「下書き」— đọc 配信数\n"
       "3. Gửi bản copy, chờ job gửi xong\n"
       "4. Đọc 配信数 của bản copy ở tab「配信履歴」",
       "Bản gốc send_count = 5 · lúc gửi bản copy có 7 friend thỏa filter",
       "- Bản copy ở 下書き hiển thị số DỰ KIẾN theo filter hiện tại (7), không phải 5\n"
       "- Sau khi gửi, 配信数 của bản copy = 7 (send_count riêng)",
       env="PRODUCTION",
       note="Nguồn: r711, r935, r946 (Bug #31527 + Bug KH #36730).",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Số đã gửi hiển thị ở chat 1:1 khớp với send_count của broadcast",
       "- Broadcast delivered send_count = 5\n- Mở chat 1:1 của 1 friend trong nhóm đã nhận",
       "1. Mở chat 1:1 của friend đã nhận broadcast\n"
       "2. Bấm vào marker/modal trigger broadcast trong khung chat\n"
       "3. Đọc số user đã gửi hiển thị trong modal\n"
       "4. Bấm vào số đó",
       "Broadcast「配信テスト」send_count = 5",
       "- Modal hiển thị số đã gửi = 5, khớp với 配信数 ở màn 配信履歴\n"
       "- Bấm vào số → chuyển sang màn lịch sử gửi, danh sách đúng 5 friend",
       note="Nguồn: r714-r715 (Bug #31527).",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "COMPAT-LEGACY-001", "Boundary",
       "Danh sách friend đã gửi của broadcast CŨ (trước 15/01/2025) — hành vi khác bản mới",
       "- Có broadcast đã gửi TRƯỚC 08:00 ngày 15/01/2025 (dữ liệu lưu ở bảng message cũ)",
       "1. Mở tab「配信履歴」, tìm broadcast gửi trước 15/01/2025\n"
       "2. Bấm vào số ở cột「配信数」\n"
       "3. Ghi lại màn hình mở ra và nội dung hiển thị",
       "Broadcast gửi trước 08:00 15/01/2025 · message lưu ở bảng `message` "
       "(sender_id = broadcast_id, msg_kind = 3)",
       "- Ghi nhận rõ hành vi: mở màn riêng list friend đã gửi hay chuyển sang màn friendlist chung\n"
       "- Nếu không hỗ trợ dữ liệu cũ, phải hiển thị thông báo rõ ràng thay vì trang trống/lỗi",
       spec="Đã hỏi leader",
       note="Nguồn: file 03/tab「Update list friend đã send」r4 (『ko support => click vào vẫn ra mh "
            "friendlist』). ⚠️ MT-14 — hành vi khác hẳn broadcast mới; cần Leader chốt có phải là hạn chế "
            "được chấp nhận không.",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "DATA-MIG-001", "Normal",
       "Danh sách friend đã gửi của broadcast MỚI (sau 15/01/2025) — đọc từ messages_v2s",
       "- Có broadcast gửi SAU 08:00 ngày 15/01/2025",
       "1. Mở tab「配信履歴」, chọn broadcast gửi sau 15/01/2025\n"
       "2. Ghi lại số ở cột「配信数」\n"
       "3. Bấm vào số, đếm số dòng trong danh sách",
       "Broadcast gửi sau 08:00 15/01/2025 · message lưu ở `messages_v2s` "
       "(source_message_id, msg_kind = 3, type = 14)",
       "- Số ngoài màn list và số dòng trong danh sách KHỚP nhau\n"
       "- Danh sách hiển thị đúng các friend đã thực nhận",
       note="Nguồn: file 03/tab「Update list friend đã send」r5.",
       group="Data"),

    tc("配信数 & danh sách friend đã gửi", "LIST-001", "Normal",
       "Phân trang ở màn danh sách friend đã gửi",
       "- Có broadcast đã gửi cho ≥60 friend",
       "1. Bấm vào số 配信数 để mở danh sách friend\n"
       "2. Kiểm tra có thanh phân trang không\n"
       "3. Chuyển sang trang 2, đếm số dòng\n"
       "4. Cộng số dòng các trang và so với 配信数",
       "60 friend đã nhận",
       "- Có phân trang hoạt động đúng\n"
       "- Tổng số dòng qua các trang = 60, khớp với 配信数\n"
       "- Không bị lặp hoặc thiếu friend giữa các trang",
       note="Nguồn: file 03/tab「Update list friend đã send」r6 — kết quả gốc là NG ở dev, OK ở step. "
            "TC viết theo hành vi ĐÚNG."),

    tc("配信数 & danh sách friend đã gửi", "DATA-COUNT-001", "Normal",
       "Gỡ điều kiện filter khỏi một số friend TRƯỚC giờ gửi — chỉ người còn thỏa mới nhận",
       "- Tạo broadcast filter theo tag T, tag T đang gắn cho 5 friend\n"
       "- Đặt lịch gửi sau 30 phút (ngoài cửa sổ đóng băng filter)",
       "1. Gắn tag T cho 5 friend, tạo broadcast lọc theo tag T\n"
       "2. Trước giờ gửi > 30 phút: gỡ tag T khỏi 2 friend\n"
       "3. Chờ job gửi\n"
       "4. Kiểm tra app LINE của cả 5 friend\n"
       "5. Đọc 配信数 ở tab「配信履歴」và danh sách friend",
       "Tag T: 5 friend → gỡ 2 người trước giờ gửi 30 phút",
       "- Chỉ 3 friend còn tag T nhận được tin\n"
       "- 2 friend đã gỡ tag KHÔNG nhận được\n"
       "- 配信数 ở lịch sử = 3, danh sách friend đúng 3 người đó",
       env="PRODUCTION",
       note="Nguồn: file 03/tab「Update list friend đã send」r3. RULE-06 + RULE-07. "
            "RULE-08: job nền → PRODUCTION.",
       group="API"),
]
