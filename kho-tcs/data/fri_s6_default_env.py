# -*- coding: utf-8 -*-
"""FA-015 — Nhóm 6: Thông tin mặc định & địa chỉ · Backup & recover · Phân quyền & môi trường.

Nguồn chính:
- 10.2 /「Feature #29832」(06/2025) — thêm folder thông tin địa chỉ (5 trường) vào toàn bộ tính năng.
- 10.2 /「test fix bug」khối Bug #30558 (07/2025) r32-r45 — folder địa chỉ trên app my page.
- TCsLine_Improve chung /「Phân quyền」(11/2023) ·「recover bảng category」(06/2025).
- 10.2 /「Change spec info type select」r73-r84 — backup & recover option select.
"""
from _common import tc

ADM = "- Đăng nhập admin bot A (plan có phí), mở /basic/friend-information"
ADDR5 = "5 trường địa chỉ: 郵便番号 · 都道府県名 · 市区町村名 · 町名/番地 · 建物名・部屋番号"
DEF4 = "4 trường cơ bản: システム表示名 · 携帯電話 · メールアドレス · 生年月日"

S6 = [
    # ══════════════════ Thông tin mặc định & địa chỉ ══════════════════
    tc("Thông tin mặc định & địa chỉ", "UI-001", "Normal",
       "Panel folder hiển thị 2 folder hệ thống: thông tin cơ bản và thông tin địa chỉ, với đủ trường bên trong",
       ADM,
       "1. Quan sát panel folder bên trái\n2. Click folder thông tin cơ bản, đếm trường ở panel phải\n"
       "3. Click folder thông tin địa chỉ, đếm trường\n4. Chụp màn hình cả 2 folder",
       DEF4 + "\n" + ADDR5,
       "- Panel trái có folder thông tin cơ bản và folder thông tin địa chỉ (ngoài「未分類」và folder tự tạo)\n"
       "- Folder cơ bản: hiển thị đủ 4 trường mặc định\n"
       "- Folder địa chỉ: hiển thị đủ 5 trường địa chỉ\n"
       "- Cả 2 folder không có nút xóa/đổi tên",
       note="Evidence: ảnh chụp. Feature #29832 (06/2025 — thêm folder địa chỉ). Nguồn: r3 + spec BR-10."),

    tc("Thông tin mặc định & địa chỉ", "FUNC-001", "Normal",
       "Gán / cập nhật / xóa giá trị 4 trường cơ bản từ màn 友だち詳細 → hiển thị đủ 3 nơi",
       "- Bạn U1 chưa có giá trị ở 4 trường cơ bản",
       "1. Ở 友だち詳細 của U1 nhập giá trị cho từng trường → lưu\n"
       "2. Đọc lại giá trị ở 友だち詳細, right bar chat 1:1 và màn danh sách câu trả lời\n"
       "3. Cập nhật giá trị từng trường → đọc lại\n4. Xóa trắng từng trường → đọc lại",
       DEF4 + "\nVí dụ: システム表示名「山田太郎」· 携帯電話「09012345678」· "
       "メールアドレス「test@example.com」· 生年月日「1990-05-10」",
       "- Sau khi nhập: cả 3 nơi hiển thị đúng giá trị, 回答人数 mỗi trường +1\n"
       "- Sau cập nhật: giá trị mới hiển thị đúng, 回答人数 không đổi\n"
       "- Sau xóa: không còn giá trị và không còn dòng rỗng, 回答人数 -1",
       note="RULE-07. Nguồn: tab「Improve count phía web」r3-r20 + r313-r321 (#38591)."),

    tc("Thông tin mặc định & địa chỉ", "FUNC-001", "Normal",
       "Gán / cập nhật / xóa giá trị 5 trường địa chỉ → hiển thị đủ 3 nơi và count đúng",
       "- Bạn U1 chưa có giá trị ở 5 trường địa chỉ",
       "1. Nhập giá trị cho từng trường địa chỉ ở 友だち詳細 → lưu → đọc 3 nơi và 回答人数\n"
       "2. Cập nhật từng trường → đọc lại\n3. Xóa trắng từng trường → đọc lại",
       ADDR5 + "\nVí dụ: 郵便番号「1500001」· 都道府県名「東京都」· 市区町村名「渋谷区」· "
       "町名/番地「神宮前1-1-1」· 建物名・部屋番号「ABCビル101」",
       "- Nhập: cả 3 nơi hiển thị đúng, mỗi trường 回答人数 +1\n"
       "- Cập nhật: 回答人数 không đổi\n- Xóa: không còn giá trị/dòng rỗng, 回答人数 -1",
       note="Tương ứng RV-02 (r477 — xóa trắng trường địa chỉ cũng xóa hẳn dòng, count -1); "
            "TC gốc RV-02 chỉ có tiêu đề → expected do AI viết. ⚠️ 都道府県名 lưu khác 4 trường còn lại (spec BR-10) "
            "→ xem MT-02."),

    tc("Thông tin mặc định & địa chỉ", "UI-FIELD-001", "Normal",
       "Trường 都道府県名 là kiểu lựa chọn (danh sách tỉnh/thành), 4 trường địa chỉ còn lại là nhập text",
       "- Bạn U1, mở 友だち詳細",
       "1. Mở ô nhập của 都道府県名 → quan sát dạng nhập\n"
       "2. Mở ô nhập của 郵便番号, 市区町村名, 町名/番地, 建物名・部屋番号 → quan sát\n3. Chụp màn hình",
       ADDR5,
       "- 都道府県名: hiển thị danh sách lựa chọn tỉnh/thành để chọn, không phải ô gõ tự do\n"
       "- 4 trường còn lại: ô nhập text tự do",
       note="Spec BR-10 (d_6 type=1 select, còn lại type=2 text) + Feature #29832 r221-r222, r229-r230. "
            "Evidence: ảnh chụp."),

    tc("Thông tin mặc định & địa chỉ", "FUNC-001", "Normal",
       "Trường mặc định KHÔNG cho đổi 管理名, KHÔNG cho xóa; nhưng cấu hình được action (với 生年月日)",
       ADM,
       "1. Click vào 管理名 của từng trường mặc định và địa chỉ\n"
       "2. Quan sát có sửa được tên / xóa được không\n"
       "3. Với 生年月日: mở cấu hình action và thử thêm 1 action lịch → lưu",
       DEF4 + " · " + ADDR5,
       "- Không đổi được 管理名 và không có nút xóa cho 9 trường mặc định/địa chỉ\n"
       "- 生年月日 cấu hình được action lịch và lưu thành công\n"
       "- Sau khi lưu, action chạy đúng cho bạn có ngày sinh",
       note="Spec BR-10 (default fields lưu ở bảng riêng). Corpus không có TC trực tiếp → AI bổ sung, "
            "cần Leader xác nhận trường nào cấu hình được action."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "5 trường địa chỉ xuất hiện ở màn cấu hình xuất/nhập CSV và lưu đúng lựa chọn",
       "- Màn quản lý CSV, tạo mới 1 cấu hình CSV",
       "1. Ở màn tạo CSV: quan sát có folder địa chỉ và 5 trường không\n"
       "2. Tick chọn / bỏ chọn folder friend info → quan sát danh sách trường\n"
       "3. Chọn từng trường địa chỉ → lưu → mở lại màn edit đối chiếu\n"
       "4. Copy cấu hình CSV → kiểm tra lựa chọn được giữ",
       ADDR5,
       "- Màn tạo và màn edit CSV đều hiển thị folder địa chỉ + đủ 5 trường\n"
       "- Tick/bỏ tick hoạt động đúng\n- Lưu và mở lại giữ đúng lựa chọn\n- Bản copy giữ đúng lựa chọn",
       note="Nguồn: Feature #29832 r3-r29."),

    tc("Thông tin mặc định & địa chỉ", "OUT-EXPORT-001", "Normal",
       "Export CSV có chọn trường địa chỉ → file chứa đúng cột và đúng giá trị của từng bạn",
       "- Cấu hình CSV đã chọn 5 trường địa chỉ\n- Có 3 bạn với giá trị địa chỉ khác nhau, 1 bạn không có",
       "1. Chạy export CSV\n2. Tải file, mở bằng Excel\n"
       "3. Đối chiếu 5 cột địa chỉ với giá trị ở 友だち詳細 của 4 bạn",
       "4 bạn (3 có giá trị, 1 không)",
       "- File có đủ 5 cột địa chỉ, tiêu đề cột đúng tên trường\n"
       "- Giá trị 3 bạn khớp 100% với 友だち詳細\n- Bạn không có giá trị: ô trống, không lỗi",
       env="PRODUCTION",
       note="RULE-06 (file tải về) + RULE-08. Nguồn: Feature #29832 r30-r41."),

    tc("Thông tin mặc định & địa chỉ", "COMPAT-LEGACY-001", "Normal",
       "Cấu hình CSV CŨ đã chọn trường địa chỉ cũ → vẫn export/import được như trước",
       "- Có cấu hình CSV tạo trước đợt thêm folder địa chỉ, đang chọn trường 都道府県名 cũ",
       "1. Mở cấu hình CSV cũ, quan sát trường đang được chọn\n2. Chạy export → kiểm tra file\n"
       "3. Chạy import file có cột địa chỉ cũ → kiểm tra giá trị bạn bè",
       "Cấu hình CSV cũ",
       "- Cấu hình cũ vẫn mở được, trường 都道府県名 vẫn được chọn đúng\n"
       "- Export ra đúng cột như trước\n- Import cập nhật đúng giá trị cho bạn bè",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r30, r42."),

    tc("Thông tin mặc định & địa chỉ", "INTG-HOOK-001", "Normal",
       "Import CSV có cột địa chỉ → thêm / cập nhật / xóa giá trị 5 trường địa chỉ đúng",
       "- File CSV có 5 cột địa chỉ, gồm dòng thêm mới, dòng cập nhật và dòng giá trị rỗng",
       "1. Import file\n2. Kiểm tra 友だち詳細 của bạn thêm mới, bạn cập nhật và bạn bị xóa giá trị\n"
       "3. Đọc 回答人数 của 5 trường địa chỉ",
       "3 nhóm dòng: thêm mới · cập nhật · rỗng (xóa)",
       "- Bạn thêm mới có đủ giá trị, 回答人数 tăng\n- Bạn cập nhật có giá trị mới, count không đổi\n"
       "- Bạn dòng rỗng bị xóa giá trị, count giảm",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r42-r44."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "5 trường địa chỉ chọn được trong modal filter ở mọi màn và lọc đúng",
       "- Có bạn với giá trị địa chỉ khác nhau",
       "1. Mở modal filter ở màn danh sách bạn bè, chọn điều kiện theo trường địa chỉ\n"
       "2. Với 都道府県名: lọc theo lựa chọn tỉnh/thành\n"
       "3. Với 4 trường còn lại: lọc theo khớp một phần / toàn phần / có giá trị / không có giá trị\n"
       "4. Đối chiếu danh sách bạn trả về",
       "5 trường địa chỉ × các kiểu điều kiện tương ứng",
       "- 都道府県名 lọc theo kiểu lựa chọn, trả về đúng bạn ở tỉnh/thành đã chọn\n"
       "- 4 trường còn lại lọc theo kiểu text, trả về đúng tập bạn\n"
       "- Điều kiện loại trừ bao gồm cả bạn chưa có giá trị",
       note="Nguồn: Feature #29832 r45 (block note) + Improve filter friend info r25-r27."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "5 trường địa chỉ chọn được trong dialog action ở mọi màn (gán / xóa giá trị)",
       "- Mở dialog action ở màn chat 1:1 và các màn khác",
       "1. Mở dialog action → chọn action 友だち情報 → quan sát danh sách trường\n"
       "2. Tạo action GÁN giá trị cho từng trường địa chỉ → kích hoạt cho 1 bạn → kiểm tra giá trị\n"
       "3. Tạo action XÓA giá trị → kích hoạt → kiểm tra giá trị và 回答人数",
       ADDR5 + " · 2 loại action (gán, xóa)",
       "- Dialog hiển thị đủ folder địa chỉ và 5 trường\n"
       "- Action gán: giá trị ghi đúng vào trường tương ứng, count +1\n"
       "- Action xóa: giá trị bị xóa, count -1",
       note="Nguồn: Feature #29832 r132-r162."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "Action gán trường địa chỉ chạy đúng qua cả lối callback và lối job",
       "- Đã cấu hình action gán trường địa chỉ ở auto-reply (callback) và action schedule (job)",
       "1. Bạn U1 kích hoạt auto-reply → kiểm tra giá trị địa chỉ của U1\n"
       "2. Chờ action schedule chạy cho U2 → kiểm tra giá trị của U2\n"
       "3. Đọc 回答人数 của trường tương ứng",
       "2 lối vào: callback và job",
       "- Cả 2 lối: giá trị địa chỉ ghi đúng, hiển thị ở 友だち詳細 và right bar\n- 回答人数 tăng đúng",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r132-r163."),

    tc("Thông tin mặc định & địa chỉ", "COMPAT-LEGACY-001", "Normal",
       "Action CŨ đang gán trường địa chỉ cũ → logic không đổi sau khi thêm folder địa chỉ mới",
       "- Có action cũ (tạo trước đợt thêm folder địa chỉ) gán trường 都道府県名",
       "1. Mở màn chứa action cũ, đọc preview action\n2. Kích hoạt action cho 1 bạn\n"
       "3. Kiểm tra giá trị 都道府県名 của bạn đó",
       "Action cũ trỏ trường địa chỉ cũ",
       "- Preview action hiển thị đúng trường 都道府県名\n"
       "- Kích hoạt ghi đúng giá trị, logic không đổi so với trước",
       note="Nguồn: Feature #29832 r163 ('vẫn lưu id -6 như cũ ⇒ logic action không đổi')."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "Form nhập của lesson / salon map được với trường địa chỉ (text và lựa chọn)",
       "- Lesson và salon có màn cấu hình form nhập",
       "1. Ở màn cấu hình form nhập của lesson: tạo item kiểu text → mở danh sách trường friend info\n"
       "2. Tạo item kiểu lựa chọn → mở danh sách trường\n3. Lặp với salon",
       "2 tính năng × 2 kiểu item",
       "- Item kiểu text: hiển thị folder địa chỉ và đủ 5 trường để chọn\n"
       "- Item kiểu lựa chọn: hiển thị 都道府県名 và khi chọn thì hiện danh sách tỉnh/thành\n"
       "- Cả lesson và salon đều đúng",
       note="Nguồn: Feature #29832 r221-r222, r229-r230."),

    tc("Thông tin mặc định & địa chỉ", "INTG-HOOK-001", "Normal",
       "Bạn booking lesson / salon nhập trường địa chỉ → giá trị được ghi vào friend info",
       "- Lesson và salon có form nhập map 5 trường địa chỉ",
       "1. Bạn U1 booking lesson và nhập đủ 5 trường địa chỉ → kiểm tra 友だち詳細\n"
       "2. Admin book hộ và nhập địa chỉ → kiểm tra\n3. Lặp với salon\n"
       "4. Trường hợp bạn KHÔNG nhập → kiểm tra giá trị và count",
       "2 tính năng × {bạn book, admin book, không nhập}",
       "- Có nhập: 5 trường địa chỉ được ghi đúng giá trị, 回答人数 tăng\n"
       "- Không nhập: không tạo giá trị, 回答人数 không đổi",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r226-r227, r234-r235."),

    tc("Thông tin mặc định & địa chỉ", "COMPAT-LEGACY-001", "Normal",
       "Item CŨ của form nhập đang liên kết trường địa chỉ cũ → vẫn hoạt động",
       "- Lesson/salon có item cũ liên kết trường địa chỉ cũ",
       "1. Mở màn cấu hình form nhập, quan sát item cũ\n2. Bạn booking qua form đó\n"
       "3. Kiểm tra giá trị friend info được ghi",
       "Item cũ liên kết trường địa chỉ cũ",
       "- Item cũ hiển thị đúng liên kết, không bị mất\n- Bạn booking vẫn ghi được giá trị đúng trường",
       note="Nguồn: Feature #29832 r223, r228, r231, r236."),

    tc("Thông tin mặc định & địa chỉ", "REG-SHARED-001", "Normal",
       "Màn phân tích chéo chọn được trường địa chỉ làm trục tham chiếu và chạy đúng",
       "- Màn phân tích chéo, có bạn với giá trị ở các trường friend info",
       "1. Tạo phân tích chéo mới, chọn trục là trường địa chỉ (từng trường trong 5 trường)\n"
       "2. Lưu và chạy phân tích → đọc kết quả\n"
       "3. Mở màn edit đối chiếu lựa chọn đã lưu\n4. Copy phân tích chéo → kiểm tra bản copy\n"
       "5. Kiểm tra kết quả sau khi job chạy",
       ADDR5 + " + các trường khác (tên, email, số điện thoại, ngày sinh, text, select, ngày, điểm, ảnh, pdf)",
       "- Chọn được đủ các trường ở phần cấu hình trục\n- Lưu và mở lại giữ đúng lựa chọn\n"
       "- Kết quả phân tích khớp số bạn thực tế có giá trị tương ứng\n- Bản copy giữ đúng cấu hình",
       env="PRODUCTION",
       note="Nguồn: Feature #29832 r241-r276."),

    tc("Thông tin mặc định & địa chỉ", "SYNC-APP-001", "Normal",
       "Folder địa chỉ hiển thị đúng trên app my page (lỗi gốc Bug #30558)",
       "- App mobile đăng nhập cùng bot A\n- Bạn U1 có giá trị ở 5 trường địa chỉ",
       "1. Trên app mở my page của U1\n2. Quan sát folder địa chỉ và 5 trường có hiển thị không\n"
       "3. Đối chiếu giá trị với 友だち詳細 phía web\n4. Chụp màn hình app",
       ADDR5,
       "- App hiển thị đủ 5 trường địa chỉ trong danh sách thông tin\n"
       "- Giá trị khớp với web\n- Không trường nào bị thiếu",
       env="PRODUCTION",
       note="Bug #30558 (07/2025). Nguồn: r32-r45."),

    tc("Thông tin mặc định & địa chỉ", "DATA-ID-001", "Boundary",
       "Xóa trắng trường 都道府県名 (lưu khác 4 trường địa chỉ còn lại) → hành vi count và dòng dữ liệu",
       "- Bạn U1 có giá trị ở 都道府県名 và ở 郵便番号",
       "1. Ghi 回答人数 của 2 trường\n2. Xóa trắng 都道府県名 → lưu → đọc count và màn danh sách câu trả lời\n"
       "3. Xóa trắng 郵便番号 → lưu → đọc count và màn danh sách câu trả lời\n"
       "4. So sánh hành vi 2 trường",
       "都道府県名 vs 郵便番号",
       "- Cả 2 trường: U1 biến mất khỏi màn danh sách câu trả lời, 回答人数 giảm 1\n"
       "- Không trường nào để lại dòng giá trị rỗng ở 友だち詳細",
       spec="Đã hỏi leader",
       note="⚠️ MT-02: spec BR-10 nói 都道府県名 lưu ở thông tin bạn (giống 4 trường cơ bản), 4 trường địa chỉ còn lại "
            "lưu như trường tự tạo; corpus RV-02 (r477) yêu cầu CẢ 5 trường địa chỉ đều 'xóa hẳn dòng, count -1'. "
            "Cần Leader chốt hành vi cho 都道府県名."),

    tc("Thông tin mặc định & địa chỉ", "COMPAT-LEGACY-001", "Normal",
       "Bạn đã có giá trị địa chỉ từ trước đợt thêm folder mới → dữ liệu cũ hiển thị đúng, không mất",
       "- Có bạn được nhập địa chỉ trước đợt Feature #29832",
       "1. Mở 友だち詳細 của bạn đó\n2. Đối chiếu giá trị 都道府県名 với dữ liệu cũ\n"
       "3. Mở màn danh sách câu trả lời của trường 都道府県名\n4. Kiểm tra 回答人数",
       "Bạn có dữ liệu địa chỉ cũ",
       "- Giá trị cũ hiển thị đúng, không bị mất hay lệch trường\n"
       "- Bạn xuất hiện ở màn danh sách câu trả lời, 回答人数 tính đủ",
       note="Nguồn: Feature #29832 (xuyên suốt các dòng 'check ... cũ trước đó')."),

    # ══════════════════ Backup & recover ══════════════════
    tc("Backup & recover", "DATA-BACKUP-001", "Normal",
       "Backup bot → toàn bộ trường thông tin và folder được khôi phục đủ ở bot đích",
       "- Bot nguồn có ≥ 3 folder, ≥ 10 trường đủ 6 kiểu, có option và action\n- Bot đích trống",
       "1. Ghi lại danh sách folder + trường (管理名, 情報タイプ, folder) ở bot nguồn\n"
       "2. Chạy backup → khôi phục sang bot đích\n"
       "3. Mở /basic/friend-information của bot đích và đối chiếu từng mục\n"
       "4. Mở màn edit vài trường và đối chiếu option/action",
       "≥ 3 folder, ≥ 10 trường, 6 kiểu",
       "- Bot đích có đủ folder đúng tên, đúng thứ tự\n"
       "- Đủ trường đúng 管理名, đúng 情報タイプ, đúng folder\n"
       "- Option và action của từng trường được khôi phục đúng",
       env="PRODUCTION",
       note="RULE-08. Nguồn: tab「Change spec info type select」r73-r84 + spec BR-07."),

    tc("Backup & recover", "DATA-BACKUP-001", "Normal",
       "Backup → option của trường 選択肢 được khôi phục đủ và các nơi tham chiếu trỏ đúng option mới",
       "- Bot nguồn có trường 選択肢 với 3 option, được tham chiếu ở form answer, booking event, "
       "dialog action và modal filter",
       "1. Backup và khôi phục sang bot đích\n"
       "2. Ở bot đích mở màn edit trường 選択肢 đếm option\n"
       "3. Mở form answer / booking event / dialog action / modal filter và kiểm tra option hiển thị\n"
       "4. Cho 1 bạn ở bot đích chọn option qua form → kiểm tra giá trị friend info",
       "3 option × 4 nơi tham chiếu",
       "- Bot đích có đủ 3 option đúng text và thứ tự\n"
       "- Cả 4 nơi tham chiếu hiển thị đúng 3 option, không nơi nào rỗng hoặc lỗi\n"
       "- Bạn chọn option qua form → giá trị friend info ghi đúng option đó",
       env="PRODUCTION",
       note="Nguồn: tab「Change spec info type select」r73-r84 (recover option select cho 6 bảng liên quan)."),

    tc("Backup & recover", "DATA-BACKUP-001", "Normal",
       "Backup → giá trị friend info của bạn bè ở bot đích khớp với bot nguồn",
       "- Bot nguồn có 5 bạn với giá trị ở nhiều trường",
       "1. Ghi lại 回答人数 từng trường và giá trị của 5 bạn ở bot nguồn\n"
       "2. Backup và khôi phục\n3. Ở bot đích đọc 回答人数 và mở 友だち詳細 của 5 bạn\n"
       "4. Mở màn danh sách câu trả lời của vài trường",
       "5 bạn × nhiều trường",
       "- 回答人数 ở bot đích khớp bot nguồn\n"
       "- Giá trị của 5 bạn khớp 100%\n- Màn danh sách câu trả lời liệt kê đúng bạn",
       env="PRODUCTION",
       note="TC do AI bổ sung theo DATA-BACKUP-001 (corpus chỉ ghi mức bảng dữ liệu), cần Leader xác nhận "
            "phạm vi backup có gồm giá trị bạn bè không."),

    tc("Backup & recover", "DATA-BACKUP-001", "Normal",
       "Backup → cấu hình lịch của trường 年月日 được khôi phục và job gửi đúng ở bot đích",
       "- Bot nguồn có trường 年月日 với cấu hình lịch và bạn đang có giá trị",
       "1. Backup và khôi phục sang bot đích\n2. Ở bot đích mở màn edit trường, đối chiếu cấu hình lịch\n"
       "3. Gán giá trị cho 1 bạn ở bot đích\n4. Chờ tới mốc, kiểm tra LINE app bạn đó",
       "Cấu hình: 登録 月日, trước 3 ngày, 09:00",
       "- Cấu hình lịch ở bot đích giống bot nguồn\n- Gán giá trị sinh lịch đúng mốc\n"
       "- Bạn nhận action đúng thời điểm",
       env="PRODUCTION",
       note="RULE-08 (job). TC do AI bổ sung, cần Leader xác nhận."),

    tc("Backup & recover", "STATE-DEP-001", "Abnormal",
       "Trong lúc bot đang backup → mọi thao tác tạo/sửa/xóa trường và folder đều bị chặn",
       "- Bot A đang có tiến trình backup đang chạy",
       "1. Thử tạo folder mới\n2. Thử tạo trường mới\n3. Thử sửa trường\n"
       "4. Thử xóa trường\n5. Thử chuyển folder hàng loạt\n6. Sau khi backup xong thử lại",
       "5 thao tác ghi trong lúc backup",
       "- Cả 5 thao tác bị chặn với thông báo bot đang backup\n"
       "- Không dữ liệu nào bị thay đổi\n- Sau khi backup xong, cả 5 thao tác thực hiện được bình thường",
       env="PRODUCTION",
       note="Spec BR-07 (backup lock cho mọi thao tác write). Corpus không có TC → AI bổ sung."),

    tc("Backup & recover", "DATA-MIG-001", "Normal",
       "Recover option select cho dữ liệu cũ → option được tạo lại và các bảng liên quan trỏ đúng",
       "- Có dữ liệu cũ tạo trước đợt thêm mã option (Bug #27314)",
       "1. Chạy tiến trình recover option\n2. Mở màn edit trường 選択肢 cũ, đếm option\n"
       "3. Kiểm tra giá trị bạn bè có trỏ đúng option không\n"
       "4. Kiểm tra form answer, form nhập lesson/salon, dialog action, modal filter",
       "Dữ liệu trước Bug #27314 (12/2024)",
       "- Option cũ được tạo lại đầy đủ\n"
       "- Giá trị của bạn bè trỏ đúng option (đổi tên option thì giá trị đổi theo)\n"
       "- 5 nơi tham chiếu đều hoạt động bình thường",
       env="PRODUCTION",
       note="Nguồn: tab「Change spec info type select」r78-r84."),

    tc("Backup & recover", "DATA-MIG-001", "Normal",
       "Recover action điểm cũ (kiểu chỉ định) → khi mở edit mặc định chọn đúng kiểu chỉ định",
       "- Có action điểm cũ tạo trước khi thêm tùy chọn ngẫu nhiên",
       "1. Mở dialog action của các action điểm cũ (ghi đè / cộng / trừ)\n"
       "2. Quan sát tùy chọn kiểu điểm đang được chọn\n3. Lưu lại không sửa gì\n"
       "4. Kích hoạt action cho 1 bạn và kiểm tra giá trị",
       "Action cũ: ghi đè, cộng, trừ điểm",
       "- Mở edit: mặc định chọn đúng kiểu「chỉ định」, giữ nguyên số điểm cũ\n"
       "- Lưu lại không làm đổi giá trị\n- Kích hoạt: bạn nhận đúng số điểm như trước",
       note="Nguồn: ModalAction r60, r108. ⚠️ TC gốc 11/2023 → CẦN VERIFY LẠI."),

    tc("Backup & recover", "DATA-BACKUP-001", "Normal",
       "So sánh backup action/template có action friend info giữa bot nguồn và bot đích",
       "- Bot nguồn có action friend info gắn ở form, template button, kết bạn mới, booking event",
       "1. Backup và khôi phục\n"
       "2. Ở bot đích mở lần lượt 4 nơi, đối chiếu giao diện action với bot nguồn\n"
       "3. Kích hoạt thử action ở mỗi nơi cho 1 bạn và kiểm tra giá trị friend info",
       "4 nơi: form · template button · kết bạn mới · booking event",
       "- Giao diện và preview action ở bot đích giống bot nguồn\n"
       "- Kích hoạt: giá trị friend info ghi đúng ở bot đích, trỏ đúng trường tương ứng của bot đích",
       env="PRODUCTION",
       note="Nguồn: ModalAction r63-r70, r126-r130."),

    tc("Backup & recover", "DATA-BACKUP-001", "Abnormal",
       "Nơi KHÔNG được backup (message pattern của calendar / bill tiền) → ghi nhận rõ để không hiểu nhầm",
       "- Bot nguồn có message pattern của lesson/salon và cấu hình bill tiền chứa action friend info",
       "1. Backup và khôi phục\n2. Ở bot đích mở message pattern của lesson/salon\n"
       "3. Mở cấu hình bill tiền\n4. Ghi nhận nội dung nào không được khôi phục",
       "Message pattern lesson/salon · bill tiền",
       "- Ghi nhận thực tế: các mục này KHÔNG được khôi phục (theo corpus)\n"
       "- Bot đích không văng lỗi khi mở các màn đó",
       spec="Spec không ghi",
       note="Nguồn: ModalAction r69-r70 ('ko backup') + Feature #29832 r218-r219. "
            "⚠️ Spec FA-015 không nêu phạm vi backup → xem MT-18."),

    tc("Backup & recover", "JOB-001", "Normal",
       "Job dọn folder đã xóa (kind=12) không đụng dữ liệu của tính năng khác",
       "- Bot có folder đã xóa ở nhiều tính năng (tag, kịch bản, form, richmenu, friend info…)",
       "1. Xóa 1 folder friend info và 1 folder của tính năng khác\n2. Chờ job dọn chạy\n"
       "3. Kiểm tra màn friend information\n4. Kiểm tra màn của tính năng kia\n"
       "5. Kiểm tra các folder KHÔNG bị xóa vẫn nguyên",
       "Folder friend info + folder tính năng khác",
       "- Trường trong folder friend info đã xóa bị dọn sạch\n"
       "- Dữ liệu của tính năng khác chỉ bị dọn đúng phần folder của nó\n"
       "- Các folder còn sống ở mọi tính năng không bị đụng",
       env="PRODUCTION",
       note="Nguồn: TCsLine_Improve chung /「recover bảng category」(06/2025) — dòng kind=12 friend info."),

    # ══════════════════ Phân quyền & môi trường ══════════════════
    tc("Phân quyền & môi trường", "PERM-001", "Abnormal",
       "Menu 友だち情報管理 với staff không có quyền → hiện message quyền khi rê chuột, không click được",
       "- Account staff (副管理人 hoặc 運用者) chưa được cấp quyền màn friend information",
       "1. Đăng nhập staff, quan sát menu\n2. Rê chuột vào mục 友だち情報管理\n"
       "3. Click vào mục menu\n4. Cuộn trang xuống rồi rê chuột lại để kiểm tra vị trí hiển thị message",
       "Staff chưa cấp quyền",
       "- Rê chuột hiện message:\n操作できません。\nこの機能の操作権限が付与されていません。\n"
       "主管理者に操作権限を付与してもらうことで操作が可能となります。\n"
       "- Không click vào được màn\n- Khi cuộn trang, message hiển thị đúng vị trí mục menu",
       note="Nguồn: TCsLine_Improve chung /「Phân quyền」r4-r7, r12. ⚠️ TC gốc 11/2023 (gần 3 năm) → CẦN VERIFY LẠI."),

    tc("Phân quyền & môi trường", "PERM-002", "Normal",
       "Staff ĐƯỢC cấp quyền màn friend information → vào được và thao tác được",
       "- Account staff đã được cấp quyền màn friend information",
       "1. Đăng nhập staff, rê chuột vào mục menu\n2. Click vào màn\n"
       "3. Thực hiện: tạo folder, tạo trường, sửa trường, xóa trường\n4. Ghi lại thao tác nào bị chặn",
       "Staff đã cấp quyền",
       "- Không hiện message lỗi khi rê chuột, click vào được màn\n"
       "- Các thao tác trong phạm vi quyền thực hiện được và dữ liệu lưu đúng",
       note="Nguồn:「Phân quyền」r6, r8, r10. ⚠️ Spec Gap #2 chưa xác nhận cơ chế phân quyền của FA-015 — xem MT-12."),

    tc("Phân quyền & môi trường", "PERM-003", "Abnormal",
       "Staff gõ thẳng URL màn friend information / màn tạo / màn danh sách câu trả lời khi không có quyền",
       "- Account staff chưa được cấp quyền màn friend information",
       "1. Gõ thẳng /basic/friend-information\n2. Gõ /basic/friend-information/add\n"
       "3. Gõ /basic/friend-information/{id}\n4. Gõ /basic/friend-information/item/{id}",
       "4 URL của FA-015",
       "- Cả 4 URL đều không truy cập được nội dung (chuyển hướng hoặc báo không có quyền)\n"
       "- Không rò rỉ danh sách trường hay dữ liệu bạn bè",
       note="Kiểm tra ở TẦNG URL chứ không chỉ ẩn menu. TC do AI bổ sung theo PERM-003 (spec Gap #2)."),

    tc("Phân quyền & môi trường", "SEC-001", "Abnormal",
       "Gọi trực tiếp API lưu/xóa giá trị friend info với bot hoặc bạn không thuộc quyền → không ghi/xóa nhầm",
       "- Tài khoản admin bot A\n- Biết id bạn và id trường của bot B",
       "1. Ở bot A thực hiện lưu giá trị friend info và bắt request\n"
       "2. Gửi lại request thay id bạn/id trường bằng của bot B\n"
       "3. Kiểm tra dữ liệu bạn bè ở bot B\n4. Lặp với request xóa giá trị",
       "id bạn + id trường của bot B",
       "- Request bị từ chối\n"
       "- Giá trị friend info của bạn thuộc bot B không bị thêm/sửa/xóa\n- 回答人数 của bot B không đổi",
       note="Tương ứng RV-14 (r489) — TC gốc chỉ có tiêu đề; expected do AI viết."),

    tc("Phân quyền & môi trường", "PERM-004", "Normal",
       "Staff thực hiện xóa bạn bè → count friend info cập nhật đúng theo quyền",
       "- Account staff có quyền xóa bạn bè\n- Bạn U1 có giá trị ở 3 trường friend info",
       "1. Đăng nhập staff, xóa bạn U1\n2. Đăng nhập admin, đọc 回答人数 của 3 trường\n"
       "3. Mở màn danh sách câu trả lời của 3 trường",
       "Staff xóa 1 bạn có 3 giá trị",
       "- Xóa bạn thành công\n- 回答人数 của cả 3 trường giảm đúng 1\n"
       "- U1 không còn ở màn danh sách câu trả lời",
       note="⚠️ Corpus r142 ('Check account staff nhấn xóa friend') KHÔNG có kết quả mong đợi → expected do AI viết."),

    tc("Phân quyền & môi trường", "ENV-001", "Normal",
       "Màn friend information hoạt động đúng trên PRODUCTION với dữ liệu thật",
       "- Bot thật trên production có nhiều folder, nhiều trường và lượng bạn lớn",
       "1. Mở /basic/friend-information, đo thời gian load\n2. Click qua các folder\n"
       "3. Mở màn danh sách câu trả lời của trường có nhiều bạn nhất\n"
       "4. Thực hiện 1 thao tác tạo trường và 1 thao tác sửa trường",
       "Bot production có dữ liệu thật",
       "- Màn load xong không timeout, hiển thị đủ folder và trường\n"
       "- Màn danh sách câu trả lời mở được với lượng bạn lớn\n"
       "- Tạo/sửa trường lưu đúng và hiển thị ngay",
       env="PRODUCTION",
       note="RULE-08. TC do AI bổ sung — corpus tách 'môi trường test' và 'môi trường prod' cho các bug folder "
            "(Test bug folder all màn r299-r318)."),

    tc("Phân quyền & môi trường", "ENV-002", "Normal",
       "So sánh hành vi giữa STAGING và PRODUCTION cho các thao tác chính của màn",
       "- Cùng bộ dữ liệu tương đương ở staging và production",
       "1. Thực hiện cùng 1 kịch bản ở cả 2 môi trường: tạo folder → tạo trường 4 kiểu → gán giá trị "
       "cho 1 bạn → xóa giá trị → xóa trường\n2. Ghi lại kết quả từng bước ở mỗi môi trường\n"
       "3. So sánh 2 bảng kết quả",
       "1 kịch bản × 2 môi trường",
       "- Kết quả từng bước giống nhau ở cả 2 môi trường\n"
       "- Nếu khác nhau: ghi rõ bước nào khác và khác thế nào",
       env="PRODUCTION",
       note="TC do AI bổ sung theo ENV-002 (đối chiếu môi trường), cần Leader xác nhận phạm vi chạy trên production."),

    tc("Phân quyền & môi trường", "JOB-001", "Abnormal",
       "Job gửi action ngày tháng bị TẮT → không bạn nào nhận action, dữ liệu lịch vẫn giữ",
       "- Trường 年月日 có action, bạn U1 có lịch tới hạn\n- Cấu hình bật/tắt job đang ở trạng thái TẮT",
       "1. Xác nhận job đang tắt (phối hợp dev)\n2. Chờ qua mốc gửi của U1\n"
       "3. Kiểm tra LINE app U1\n4. Kiểm tra lịch của U1 còn ở trạng thái chờ gửi không\n"
       "5. Bật job lại và theo dõi",
       "Job tắt → bật lại",
       "- Khi job tắt: U1 KHÔNG nhận action, lịch vẫn ở trạng thái chờ gửi (không bị mất)\n"
       "- Sau khi bật lại: lịch tới hạn được xử lý, U1 nhận action",
       env="PRODUCTION",
       note="⚠️ Spec §7 ghi ENABLE_EVENT_REMIND mặc định = 0 (tắt) — nếu môi trường test tắt job thì toàn bộ TC "
            "nhóm「Job action ngày tháng」sẽ không chạy được. Xem MT-17. TC do AI bổ sung."),

    tc("Phân quyền & môi trường", "COMPAT-LEGACY-001", "Normal",
       "Trường thông tin tạo từ rất lâu (trước các đợt improve) vẫn mở, sửa, xóa và gán giá trị được",
       "- Bot có trường friend info tạo từ trước 2024 (trước Bug #27314, #29832, #33697)",
       "1. Mở màn edit trường cũ, đối chiếu dữ liệu hiển thị\n2. Sửa 管理名 và lưu\n"
       "3. Gán giá trị cho 1 bạn\n4. Kiểm tra 回答人数 và màn danh sách câu trả lời\n5. Copy trường cũ",
       "Trường tạo trước 2024",
       "- Màn edit mở bình thường, hiển thị đủ option/action cũ\n"
       "- Sửa và lưu được, giá trị bạn bè cũ không bị mất\n"
       "- Gán giá trị mới hoạt động, 回答人数 tăng đúng\n- Copy được và bản copy đúng cấu hình",
       note="TC do AI bổ sung theo COMPAT-LEGACY-001 — nhiều TC nguồn của FA-015 từ 2023-2024, cần đối chứng "
            "dữ liệu cũ vẫn tương thích."),

    tc("Phân quyền & môi trường", "DEPLOY-ASSET-001", "Normal",
       "Sau khi deploy phiên bản mới → màn friend information không lỗi JS, thao tác chính hoạt động",
       "- Vừa deploy phiên bản mới lên môi trường",
       "1. Mở /basic/friend-information với cache trình duyệt đã xóa\n2. Mở DevTools tab Console\n"
       "3. Thực hiện: tạo folder, tạo trường, mở dialog action, lưu\n"
       "4. Quan sát Console sau mỗi thao tác",
       "Trình duyệt đã xóa cache",
       "- Console không có lỗi JS/404 tài nguyên\n"
       "- Cả 4 thao tác thực hiện được và lưu đúng\n- Giao diện hiển thị đúng, không vỡ layout",
       env="PRODUCTION",
       note="TC do AI bổ sung theo DEPLOY-ASSET-001, cần Leader xác nhận có nằm trong phạm vi test hồi quy không."),
]
