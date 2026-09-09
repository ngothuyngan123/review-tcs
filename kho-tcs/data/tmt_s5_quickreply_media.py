# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 28-33: Quick reply, Media (ảnh / image map / video / audio), Sticker, Location.

Nguồn chính: 02. TCsLine_Template
  - tab「Template button」r815-r1047 (sub-type クイックリプライ + Change design 23/11/2023),
    r1409-r1427 (Bug #29374 ảnh quick reply không hiển thị)
  - tab「Type ảnh」(507 dòng, 400 TC lá — ảnh thường + image map; Bug #31838 replace [name],
    Bug #31454 action lặp khi reload)
  - tab「Type video」·「Type audio」·「Type stamp」·「Type location」(Bug #32364 override vị trí)
  - tab「open url của button image map」(01/2024 — ma trận open url trong/ngoài LINE)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Folder F1 có group template G1; đang ở màn tạo template con của G1")
QR = ADM + "\n- Đã chọn loại「パネル・ボタン」→ sub-type「クイックリプライ」"
IMG = ADM + "\n- Đã chọn loại「画像・動画・音声」→ kiểu 画像"
U1 = "\n- Đã đăng ký friend U1 làm クイックテストユーザー"

S5 = [
    # ═════════════ 28. Quick reply ═════════════
    tc("Quick reply", "UI-001", "Normal",
       "Giao diện sub-type クイックリプライ khớp design; chọn được dạng text và dạng ảnh",
       QR,
       "1. Quan sát giao diện setting của sub-type クイックリプライ\n2. Chọn dạng テキスト → quan sát các ô nhập\n"
       "3. Chọn dạng ảnh → quan sát các ô nhập và vùng upload ảnh",
       "2 dạng: text và ảnh",
       "- Giao diện khớp design mới\n- Dạng text: có ô nội dung + ô text nút\n"
       "- Dạng ảnh: có thêm vùng upload ảnh cho nút",
       note="Nguồn: Template button r815-r816, r1616-r1617."),

    tc("Quick reply", "DATA-TEXT-001", "Normal",
       "Nội dung text của quick reply: nhận text Nhật có enter / multi enter, tối đa 5.000 ký tự",
       QR + U1,
       "1. Nhập nội dung text Nhật có 1 lần enter → 保存 → gửi cho U1 → quan sát\n"
       "2. Nhập nội dung có nhiều dòng trống liên tiếp → 保存 → gửi → quan sát\n"
       "3. Nhập nội dung text Nhật 5.000 ký tự → 保存 → quan sát bộ đếm và kết quả lưu",
       "text Nhật + enter / multi enter / 5.000 ký tự",
       "- Cả 3 trường hợp 保存 thành công\n"
       "- Tin trên LINE hiện đúng nội dung và giữ đúng ngắt dòng (kể cả dòng trống)\n"
       "- Bộ đếm hiển thị đúng ở mốc 5.000 ký tự",
       note="Nguồn: Template button r817-r818."),

    tc("Quick reply", "UI-INPUT-001", "Abnormal",
       "Validate nội dung / text nút của quick reply → chặn khi bỏ trống trường bắt buộc hoặc vượt giới hạn",
       QR,
       "1. Bỏ trống nội dung → 保存 → quan sát\n2. Bỏ trống text nút → 保存 → quan sát\n"
       "3. Nhập text nút vượt giới hạn ký tự → 保存 → quan sát",
       "rỗng nội dung / rỗng text nút / text nút vượt giới hạn",
       "- Trường bắt buộc bỏ trống: báo lỗi và KHÔNG lưu\n- Vượt giới hạn ký tự: báo lỗi và không lưu",
       note="Nguồn: Template button r819-r820. ⚠ TC gốc không ghi nguyên văn msg lỗi và con số giới hạn "
            "của text nút quick reply; spec cũng không ghi → cần Leader xác nhận, xem MT-35."),

    tc("Quick reply", "FUNC-001", "Normal",
       "Insert code vào nội dung quick reply (giống message type text) → chèn và replace đúng",
       QR + "\n- Friend U1 có đủ friend info; bot A có form / item / calendar / event đã tạo" + U1,
       "1. Insert LINE名 → quan sát chuỗi chèn\n2. Insert 日数・日付 (số ngày remain và ngày tháng năm) "
       "→ quan sát\n3. Insert 配信日 → quan sát\n4. Insert link form / 商品販売 / カレンダー予約 / イベント予約\n"
       "5. Insert friend info (basic và tự tạo)\n6. Insert emoji\n7. 保存 → gửi cho U1 → đối chiếu tin trên LINE",
       "7 loại insert",
       "- Mỗi loại chèn đúng code/link vào vị trí con trỏ\n"
       "- Tin trên LINE replace đúng tên LINE, ngày, friend info; link mở đúng trang đích; emoji hiện đúng",
       note="Nguồn: Template button r821-r852 (「check insert code vào text (tương tự message type text)」). "
            "Gộp vì CÙNG 1 kết quả mong đợi."),

    tc("Quick reply", "FUNC-001", "Boundary",
       "Số lượng nút quick reply: thêm được tối đa 10 nút, đủ thì chặn thêm",
       QR + U1,
       "1. Thêm nút quick reply lần lượt tới khi không thêm được nữa → đếm số nút\n"
       "2. Quan sát nút thêm sau khi đã đủ\n3. 保存 → gửi cho U1 → đếm số nút trên LINE",
       "thêm nút tới giới hạn",
       "- Thêm được tối đa 10 nút quick reply\n- Đủ 10 nút: nút thêm bị disable/chặn\n"
       "- Tin trên LINE hiện đủ 10 nút quick reply",
       note="Nguồn: Template button r913-r988 + r1569 (Send template btn 1 panel có 10 btn)."),

    tc("Quick reply", "FUNC-001", "Normal",
       "Setting màu nền / màu chữ nút quick reply → lưu và hiển thị đúng phía user",
       QR + U1,
       "1. Set màu nền nút và màu chữ nút bằng mã màu hợp lệ → 保存\n"
       "2. Gửi cho U1 → quan sát màu nút trên LINE\n3. Đổi màu khác → 保存 → gửi lại → quan sát",
       "2 lượt đổi màu",
       "- Lưu thành công mỗi lượt\n- Nút quick reply trên LINE hiện đúng màu nền và màu chữ đã set",
       note="Nguồn: Template button r915-r917 (Change design + thêm action cho btn quick reply, "
            "23/11/2023)."),

    tc("Quick reply", "DATA-TEXT-001", "Normal",
       "Tên nút quick reply nhận text Nhật, latinh, emoji, ký tự đặc biệt và space ở nhiều vị trí",
       QR + U1,
       "1. Nhập tên nút có space ở đầu → 保存 → gửi → quan sát\n2. Space ở cuối → 保存 → gửi → quan sát\n"
       "3. Nhiều space ở giữa → 保存 → gửi → quan sát\n"
       "4. Ký tự đặc biệt latinh (` ~ ! @ # $ % ^ & ( ) + = _ \" < > { } [] | . , / * \\ : ?) → gửi → quan sát\n"
       "5. Ký tự đặc biệt Nhật (・ー【】～！＠＃＄％＾＆＊（）「」｜￥；。→■∞) → gửi → quan sát\n"
       "6. Hiragana + katakana + kanji (まことボット智恵助) → gửi → quan sát\n"
       "7. Nhật + latinh + emoji (AIボット🤖_Ver1) → gửi → quan sát\n"
       "8. Ký tự đặc biệt + emoji (こーだい/プレゼント専用🎁) → gửi → quan sát",
       "8 biến thể tên nút (space đầu/cuối/giữa, ký tự đặc biệt latinh và Nhật, hỗn hợp, emoji)",
       "- Mọi biến thể 保存 thành công\n"
       "- Nút trên LINE hiện đúng tên đã nhập, KHÔNG bị mất/đổi ký tự, không sinh error message",
       note="Nguồn: Template button r1503-r1522 (khối SpecChange #32577 — text gây error msg). "
            "Gộp 8 biến thể vì CÙNG 1 kết quả mong đợi."),

    tc("Quick reply", "FUNC-001", "Normal",
       "Tạo / sort / copy / xóa action của nút quick reply → dữ liệu đúng và giữ sau lưu",
       QR + U1,
       "1. Tạo action cho 3 nút quick reply (multi action, friend action, LINE URL scheme) → 保存\n"
       "2. Sort đổi thứ tự nút → 保存 → vào edit đối chiếu\n"
       "3. Copy 1 nút có action → quan sát nút mới (tên + action)\n4. Xóa 1 nút → 保存 → đối chiếu\n"
       "5. Gửi cho U1 → bấm từng nút → quan sát action nhận được",
       "3 nút với 3 loại action",
       "- Tạo action thành công cho từng nút\n- Sort giữ đúng thứ tự sau 保存\n"
       "- Copy nút giữ nguyên action của nút nguồn\n- Xóa nút không ảnh hưởng nút còn lại\n"
       "- Bấm từng nút trên LINE ra đúng action tương ứng",
       note="Nguồn: Template button r921-r1027."),

    tc("Quick reply", "MEDIA-IMG-001", "Normal",
       "Upload ảnh cho nút quick reply → ảnh hiển thị đúng ở preview và trên LINE",
       QR + "\n- Đã chọn dạng ảnh" + U1,
       "1. Upload ảnh cho nút quick reply → quan sát preview\n2. 保存 → gửi cho U1 → quan sát nút trên LINE\n"
       "3. Đổi sang ảnh khác → 保存 → gửi → quan sát\n4. Thử upload file sai định dạng và ảnh quá dung lượng",
       "ảnh hợp lệ; ảnh sai định dạng; ảnh quá dung lượng",
       "- Ảnh hợp lệ: preview và nút trên LINE hiện đúng ảnh\n"
       "- Đổi ảnh: LINE hiện ảnh mới\n- Sai định dạng / quá dung lượng: bị chặn, báo lỗi",
       note="Nguồn: Template button r976-r986 (Test template button quick image + Check việc upload image)."),

    tc("Quick reply", "MEDIA-IMG-001", "Abnormal",
       "Bug #29374: ảnh nút quick reply KHÔNG bị mất khi tạo mới / cập nhật / bỏ ảnh",
       ADM + U1,
       "1. Tạo mới nút quick reply CÓ ảnh → 保存 → gửi cho U1 → quan sát ảnh trên LINE\n"
       "2. Với template CŨ chưa có ảnh: cập nhật thành CÓ ảnh → 保存 → gửi → quan sát\n"
       "3. Với template cũ đã có ảnh: cập nhật thành ảnh KHÁC → 保存 → gửi → quan sát\n"
       "4. Với template cũ có ảnh: cập nhật thành KHÔNG có ảnh → 保存 → gửi → quan sát\n"
       "5. Lặp lại 4 bước với sub-type standard, color và button ảnh (1 panel và 2 panel)",
       "4 kịch bản ảnh × 4 sub-type; template cũ có `type_button` = 4 và `thumbnail_path` = NULL",
       "- Mọi kịch bản: ảnh nút hiển thị ĐÚNG trên LINE (có ảnh thì hiện, bỏ ảnh thì không hiện)\n"
       "- KHÔNG xảy ra hiện tượng ảnh không hiển thị của Bug #29374",
       note="Nguồn: Template button r1409-r1427 (Bug #29374, 28/03/2025 — Template_Quickreply ảnh ko "
            "hiển thị; effect: test lại all button có ảnh). Bao gồm cả case recover "
            "`type_button = 4 và thumbnail_path = NULL`."),

    tc("Quick reply", "PERM-001", "Normal",
       "Account staff có quyền template → tạo / edit / copy / gửi quick reply bình thường",
       "- Bot A có 1 staff S1 ĐƯỢC phân quyền màn template\n- Đăng nhập bằng account S1" + U1,
       "1. S1 mở màn template → tạo template quick reply → 保存\n2. S1 edit template đó → 保存\n"
       "3. S1 copy template đó\n4. S1 gửi test cho U1 → quan sát tin trên LINE",
       "staff S1 có quyền template",
       "- S1 thực hiện được cả 4 thao tác\n- Tin trên LINE nhận đủ nội dung và nút quick reply",
       note="Nguồn: Template button r965-r975, r1618."),

    # ═════════════ 29. Media — ảnh ═════════════
    tc("Media — ảnh", "UI-001", "Normal",
       "Giao diện màn tạo template ảnh khớp spec, không vỡ layout ở 1366x768",
       IMG,
       "1. Quan sát font-size / font-color / font-family / font-weight / alignment / shadow / padding / "
       "các button / các loại input / hover\n2. Thu nhỏ về 1366x768 → quan sát\n"
       "3. Nhập data maxlength vào các ô → quan sát layout\n4. Kiểm tra các ô input có tự trim space đầu/cuối",
       "—",
       "- Giao diện khớp spec về toàn bộ mục đã liệt kê\n- Ở 1366x768 không vỡ layout\n"
       "- Nhập maxlength không làm vỡ layout",
       note="Nguồn: Type ảnh r3. ⚠ TC gốc để câu hỏi「các input đã tự trim space chưa」chưa có kết luận "
            "→ xem MT-21."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Abnormal",
       "Upload ảnh sai định dạng hoặc > 10MB → báo lỗi 1 lần, không tạo bản ghi (kể cả double click)",
       IMG,
       "1. Chọn file không phải png/jpg → quan sát\n2. Double click nút upload với file sai định dạng → quan sát\n"
       "3. Chọn ảnh png/jpg dung lượng 12MB → quan sát\n4. Double click với ảnh 12MB → quan sát\n"
       "5. Thử với ảnh jpeg 12MB",
       "file .docx; ảnh png 12MB; ảnh jpeg 12MB",
       "- Sai định dạng và quá 10MB đều báo lỗi\n"
       "- Double click CHỈ báo lỗi 1 lần và KHÔNG tạo được bản ghi thành công nào",
       note="Nguồn: Type ảnh r4-r5. ⚠ TC gốc note「check với ảnh jpeg 12mb」và r9 note「ảnh dạng jpeg "
            "đang ko upload dc」→ rủi ro riêng với .jpeg, xem MT-07."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Boundary",
       "Upload ảnh png/jpg ≤10MB (vuông / dọc / ngang) và đúng 10MB → thành công, double click chỉ 1 bản ghi",
       IMG,
       "1. Upload ảnh vuông < 10MB → quan sát; double click nút upload → đếm bản ghi\n"
       "2. Lặp lại với ảnh dọc và ảnh ngang\n3. Upload ảnh đúng 10MB → quan sát",
       "ảnh vuông / dọc / ngang < 10MB; ảnh đúng 10MB",
       "- Cả 4 trường hợp upload thành công\n- Double click CHỈ tạo 1 bản ghi thành công\n"
       "- Sau upload thành công: hiện phần setting media",
       note="Nguồn: Type ảnh r6-r9, r12. ⚠ TC gốc r8 note「upload dc nhưng bị co ảnh」với ảnh ngang "
            "→ cần kiểm lại."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Normal",
       "Upload ảnh bằng kéo-thả và bằng nút chọn → cùng kết quả (hợp lệ OK, không hợp lệ báo lỗi)",
       IMG,
       "1. Kéo-thả 1 ảnh hợp lệ vào vùng upload → quan sát\n2. Kéo-thả 1 ảnh không hợp lệ → quan sát\n"
       "3. Lặp lại 2 bước bằng nút chọn file",
       "ảnh hợp lệ và không hợp lệ; 2 cách upload",
       "- Ảnh hợp lệ: cả 2 cách đều upload thành công\n- Ảnh không hợp lệ: cả 2 cách đều báo lỗi",
       note="Nguồn: Type ảnh r10-r11."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Normal",
       "Nút update ảnh → mở popup chọn ảnh, chọn xong hiện ảnh mới",
       IMG + "\n- Đã upload 1 ảnh thành công",
       "1. Bấm nút update ảnh → quan sát popup\n2. Quan sát các loại file được liệt kê trong popup\n"
       "3. Chọn 1 ảnh khác → quan sát vùng ảnh đã upload",
       "ảnh mới",
       "- Popup chọn ảnh mở ra\n- Chọn ảnh xong: vùng ảnh hiện ẢNH MỚI",
       note="Nguồn: Type ảnh r13-r14. ⚠ TC gốc note「hiện tại đang hiển thị cả các dạng khác chọn thì "
            "báo sai loại file」→ popup nên lọc sẵn định dạng, xem MT-07."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Normal",
       "Setting kích thước ảnh hiển thị phía LINE user (lớn / trung / bé) → LINE hiện đúng cỡ",
       IMG + U1,
       "1. Quan sát giá trị default của mục chọn size ảnh → 保存 → gửi cho U1 → quan sát cỡ ảnh\n"
       "2. Chọn cỡ trung → 保存 → gửi → quan sát\n3. Chọn cỡ bé → 保存 → gửi → quan sát",
       "3 cỡ: lớn (default) / trung / bé",
       "- Default là cỡ LỚN; ảnh trên LINE hiện cỡ lớn\n"
       "- Cỡ trung và cỡ bé: ảnh trên LINE hiện đúng cỡ tương ứng",
       note="Nguồn: Type ảnh r15-r17. ⚠ TC gốc note「bên user: sẽ ko sát viền màn hình => này do line "
            "hiển thị」(cỡ trung) và r226 note「design mới bỏ phần này」→ xem MT-36."),

    tc("Media — ảnh", "MEDIA-IMG-001", "Normal",
       "Setting hình dạng ảnh (giữ nguyên gốc / cắt vuông) → LINE hiện đúng với cả ảnh vuông, dọc, ngang",
       IMG + U1,
       "1. Quan sát default của mục chọn hình dạng ảnh\n"
       "2. Với ảnh vuông: chọn giữ nguyên gốc → 保存 → gửi → quan sát; chọn hình vuông → 保存 → gửi → quan sát\n"
       "3. Lặp lại với ảnh dọc\n4. Lặp lại với ảnh ngang",
       "2 lựa chọn hình dạng × 3 loại tỉ lệ ảnh",
       "- Default là GIỮ NGUYÊN ảnh gốc; LINE hiện ảnh đúng tỉ lệ gốc với cả 3 loại ảnh\n"
       "- Chọn hình vuông: LINE hiện ảnh đã được cắt/resize thành vuông với cả 3 loại ảnh",
       note="Nguồn: Type ảnh r18-r19, r190-r191, r229-r230."),

    tc("Media — ảnh", "MSG-001", "Normal",
       "Gửi template ảnh qua chat 1:1 / send all / scenario / remind → LINE, chat 1:1 và app đều hiện đúng",
       IMG + U1,
       "1. Gửi trực tiếp qua chat 1:1 → quan sát ảnh trên LINE, trên chat 1:1 của tool và trên app mobile\n"
       "2. Gửi qua send all (broadcast) → quan sát 3 nơi trên\n3. Gửi qua scenario → quan sát\n"
       "4. Gửi qua remind → quan sát",
       "4 đường gửi × 3 nơi hiển thị",
       "- Cả 4 đường gửi: ảnh hiển thị đúng ở LINE user, chat 1:1 của tool và app mobile",
       note="Nguồn: Type ảnh r20-r21, r24, r27. RULE-06 + RULE-07."),

    tc("Media — ảnh", "JOB-001", "Abnormal",
       "XÓA template ảnh TRƯỚC giờ job gửi → message đó không gửi, các message khác vẫn gửi",
       IMG + "\n- Đã đặt broadcast/scenario/remind gửi vào thời điểm tương lai, gồm 3 message trong đó "
              "message thứ 2 dùng template ảnh TI",
       "1. Đặt lịch gửi cho U1 lúc T+10 phút\n2. Trước giờ gửi, XÓA template TI\n"
       "3. Chờ tới giờ job chạy\n4. Đếm và đối chiếu message U1 nhận được\n5. Lặp lại ở scenario và remind",
       "3 message, xóa message thứ 2 trước giờ gửi; 3 đường job",
       "- U1 nhận 2 message (thứ 1 và thứ 3), KHÔNG nhận message của template đã xóa\n"
       "- Các message khác vẫn gửi bình thường, không lỗi job",
       note="Nguồn: Type ảnh r22, r25, r28 (Expect gốc:「nếu temp bị xóa trước khi đến giờ send => msg đó "
            "sẽ ko send cho user, các msg khác vẫn send bthg」)."),

    tc("Media — ảnh", "JOB-001", "Normal",
       "CẬP NHẬT ảnh của template TRƯỚC giờ job gửi → message gửi theo nội dung ĐÃ CẬP NHẬT",
       IMG + "\n- Đã đặt broadcast/scenario/remind gửi vào thời điểm tương lai, dùng template ảnh TI",
       "1. Đặt lịch gửi cho U1 lúc T+10 phút\n2. Trước giờ gửi, đổi ảnh của TI sang ảnh khác → 保存\n"
       "3. Chờ tới giờ job chạy\n4. Quan sát ảnh U1 nhận được\n5. Lặp lại ở scenario và remind",
       "đổi ảnh trước giờ gửi; 3 đường job",
       "- U1 nhận message với ẢNH MỚI (thông tin đã cập nhật), không phải ảnh cũ\n"
       "- Các message khác vẫn gửi bình thường",
       note="Nguồn: Type ảnh r23, r26, r29."),

    tc("Media — ảnh", "FUNC-001", "Normal",
       "Edit template ảnh: đổi ảnh / cỡ / hình dạng / tab detail → 保存 và gửi đúng; không đổi gì vẫn lưu được",
       IMG + "\n- Đã có template ảnh thường TI và template image map TM" + U1,
       "1. Mở edit TI → quan sát dữ liệu hiển thị\n2. Không sửa gì → 保存 → quan sát\n"
       "3. Đổi ảnh (thử cả file sai định dạng và >10MB để xác nhận validate) → 保存 → gửi → quan sát\n"
       "4. Đổi cỡ ảnh sang trung, bé, to → 保存 → gửi → quan sát\n"
       "5. Đổi hình dạng ảnh → 保存 → gửi → quan sát\n6. Mở edit TM → quan sát dữ liệu hiển thị",
       "TI ảnh thường và TM image map",
       "- Màn edit hiện đủ thông tin của template tương ứng\n- Không sửa gì: 保存 thành công\n"
       "- Đổi ảnh/cỡ/hình dạng: 保存 thành công và tin trên LINE khớp giá trị mới\n"
       "- File sai định dạng hoặc >10MB vẫn bị chặn ở màn edit",
       note="Nguồn: Type ảnh r178-r195, r218-r234."),

    tc("Media — ảnh", "MSG-004", "Normal",
       "Tab 詳細設定 của ảnh: text hiển thị ngoài màn list LINE user — để trống dùng quy định LINE, có nhập thì hiện đúng",
       IMG + U1,
       "1. Với ảnh thường: quan sát tab 詳細設定 có hiện hay không\n"
       "2. Bật checkbox dùng image map → quan sát tab 詳細設定\n"
       "3. Để trống ô text → 保存 → gửi cho U1 → quan sát text ở khung thông báo / màn list LINE\n"
       "4. Nhập text → 保存 → gửi → quan sát",
       "để trống / có nhập",
       "- Khi KHÔNG bật image map: KHÔNG hiện tab 詳細設定\n- Khi bật image map: HIỆN tab 詳細設定\n"
       "- Để trống: hiện text theo quy định của LINE\n- Có nhập: hiện đúng text đã nhập\n"
       "- Ô này KHÔNG bắt buộc nhập",
       note="Nguồn: Type ảnh r167-r169, r192-r194, r231-r233. ⚠ TC gốc r193 note「ảnh thường spec mới ko "
            "tab setting detail (chỉ có image map mới có tab này, ảnh thường, audio...)」→ xem MT-34."),

    tc("Media — ảnh", "FRIEND-001", "Normal",
       "Tab 詳細設定 của ảnh: gắn {name}, friend info, icon, text Nhật, xuống dòng, link → hiển thị đúng",
       IMG + "\n- Đã bật image map; friend U1 có đủ friend info" + U1,
       "1. Nhập vào ô text của tab 詳細設定: {name}, code friend info, icon emoji, text Nhật, "
       "text có xuống dòng, và 1 link\n2. 保存 → gửi cho U1\n"
       "3. Quan sát text ở khung thông báo và màn list chat của LINE",
       "6 loại nội dung trong 1 ô text",
       "- {name} và friend info được replace đúng giá trị của U1\n"
       "- Icon, text Nhật hiển thị đúng; link hiện dạng text link\n"
       "- Text hiển thị đúng ở khung thông báo và màn list chat",
       note="Nguồn: Type ảnh r170-r176."),

    # ═════════════ 30. Media — image map ═════════════
    tc("Media — image map", "UI-001", "Normal",
       "Bật checkbox dùng image map → hiện phần setting image map với 3 option area",
       IMG + "\n- Đã upload ảnh thành công",
       "1. Tick checkbox sử dụng image map\n2. Quan sát các thành phần hiện ra\n"
       "3. Quan sát vùng preview ảnh và trạng thái nút chọn template area",
       "ảnh đã upload",
       "- Hiện phần setting image map: vùng preview + 3 option (手動で設定する / テンプレートから選ぶ / "
       "không setting action)\n- Vùng preview hiện đúng ảnh vừa upload\n"
       "- Với option mặc định 手動で設定する: nút chọn từ template ở trạng thái DISABLE",
       note="Nguồn: Type ảnh r30-r31, r78."),

    tc("Media — image map", "MEDIA-IMG-001", "Abnormal",
       "Update ảnh khác khi đang bật image map → template chuyển về dạng ảnh thường (bỏ tick image map)",
       IMG + "\n- Đã bật image map và tạo 2 area có action",
       "1. Bấm nút update ảnh → chọn ảnh khác\n2. Quan sát checkbox dùng image map và phần setting area",
       "đổi ảnh khi đã có area",
       "- Checkbox dùng image map bị BỎ TICK, template trở về dạng ảnh thường\n"
       "- Phần setting area không còn hiển thị",
       note="Nguồn: Type ảnh r32. ⚠ Đây là hành vi mất dữ liệu area đã cấu hình → cần Leader xác nhận "
            "có phải hành vi mong muốn, xem MT-37."),

    tc("Media — image map", "FUNC-001", "Normal",
       "Option 手動で設定する: thêm area bằng kéo-thả, lưu area đúng vị trí",
       IMG + "\n- Đã bật image map, chọn option 手動で設定する",
       "1. Bấm nút add area → quan sát popup chọn vùng tap\n2. Với ảnh to, kiểm tra popup có scroll ảnh\n"
       "3. Kéo-thả tạo vùng → quan sát vùng đỏ trên ảnh\n4. Bấm nút X → quan sát\n"
       "5. Kéo-thả lại rồi bấm nút save → quan sát area được tạo",
       "ảnh lớn; 1 area kéo-thả",
       "- Popup chọn vùng tap mở đúng; với ảnh to có scroll ảnh\n"
       "- Kéo-thả hiện vùng ĐỎ theo đúng vùng đã kéo\n- Bấm X: KHÔNG tạo area\n"
       "- Bấm save: tạo area đúng vùng vừa kéo và hiện ở danh sách area bên dưới",
       note="Nguồn: Type ảnh r79-r83. ⚠ TC gốc r81 note「bỏ phần này」cho ô nhập toạ độ thủ công → "
            "xem MT-38."),

    tc("Media — image map", "FUNC-001", "Normal",
       "Edit area: đổi kích thước, area chèn nhau thì tính theo area PHÍA SAU",
       IMG + "\n- Đã có 2 area A1 và A2 trên ảnh" + U1,
       "1. Bấm nút edit area của A1 → quan sát popup edit\n2. Kéo-thả đổi kích thước A1 → bấm X → quan sát\n"
       "3. Kéo-thả lại và lưu → quan sát A1\n"
       "4. Chỉnh A1 CHÈN LÊN một phần A2 → lưu → 保存 template → gửi cho U1\n"
       "5. U1 bấm vào phần chèn nhau → quan sát action nhận được",
       "A1 chèn lên A2",
       "- Popup edit area mở đúng; bấm X thì KHÔNG cập nhật area\n"
       "- Lưu: area đổi kích thước đúng\n"
       "- Vùng chèn nhau: user bấm vào → chạy action của area PHÍA SAU (A2)",
       note="Nguồn: Type ảnh r85-r89, r123-r127."),

    tc("Media — image map", "FUNC-001", "Normal",
       "Xóa area → vùng đó không còn action, các area khác giữ nguyên kích thước",
       IMG + "\n- Đã có 3 area, mỗi area 1 action" + U1,
       "1. Xóa area giữa → quan sát vùng ảnh và danh sách area\n2. 保存 → gửi cho U1\n"
       "3. U1 bấm vào vùng đã xóa → quan sát\n4. U1 bấm 2 area còn lại → quan sát action",
       "3 area, xóa area giữa",
       "- Vùng đã xóa KHÔNG còn action (bấm không có phản ứng)\n"
       "- 2 area còn lại giữ nguyên kích thước và action đúng",
       note="Nguồn: Type ảnh r90, r128."),

    tc("Media — image map", "FUNC-001", "Normal",
       "Option テンプレートから選ぶ: chọn được 8 kiểu layout A→H, mỗi kiểu ra đủ area tương ứng",
       IMG + "\n- Đã bật image map",
       "1. Chọn option テンプレートから選ぶ → quan sát nút chọn template\n"
       "2. Bấm nút chọn template image map → quan sát popup\n"
       "3. Chọn lần lượt kiểu A, B, C, D, E, F, G, H → với mỗi kiểu, đếm và đối chiếu số area sinh ra",
       "8 kiểu layout A→H",
       "- Chọn option này thì nút chọn template ENABLE và đổi màu\n"
       "- Popup chọn template image map mở ra với 8 kiểu\n"
       "- Mỗi kiểu sinh ra đúng số/vị trí area của layout tương ứng",
       note="Nguồn: Type ảnh r112-r121."),

    tc("Media — image map", "FUNC-001", "Normal",
       "Option không setting action → ẩn vùng chọn area, disable nút chọn template, vẫn lưu và gửi được",
       IMG + U1,
       "1. Chọn option không setting action → quan sát vùng ảnh và nút chọn template\n"
       "2. 保存 khi tạo mới → quan sát\n3. Với template đang là 手動で設定する, đổi sang option này → 保存\n"
       "4. Gửi cho U1 → bấm vào ảnh → quan sát",
       "option không setting action",
       "- KHÔNG hiện các vùng chọn trên ảnh; nút chọn template DISABLE\n"
       "- 保存 thành công cả khi tạo mới và khi đổi từ option khác\n"
       "- User bấm vào ảnh trên LINE: không có action nào chạy",
       note="Nguồn: Type ảnh r150-r152."),

    tc("Media — image map", "STATE-CLEAN-001", "Abnormal",
       "Đổi giữa 3 option area → hiện alert cảnh báo mất action; OK thì xóa hết, Cancel thì giữ nguyên",
       IMG + "\n- Đang ở option 手動で設定する với 2 area đã set action",
       "1. Đổi sang option テンプレートから選ぶ → quan sát alert\n2. Bấm Cancel → quan sát option và area\n"
       "3. Đổi lại và bấm OK → quan sát option và area\n"
       "4. Lặp lại với các chiều đổi khác (手動 ⇄ テンプレート ⇄ không setting)",
       "2 area đã set action; 6 chiều đổi option",
       "- Mỗi lần đổi option đều hiện alert: 「現在設定されているタップ時アクションが全て削除されますが"
       "よろしいですか？」\n"
       "- Bấm OK: chuyển option, XÓA hết vùng và action đã set trước đó\n"
       "- Bấm Cancel: GIỮ NGUYÊN option và toàn bộ setting action đang có",
       note="Nguồn: Type ảnh r164-r166, r196-r217."),

    tc("Media — image map", "FUNC-MULTI-001", "Normal",
       "Setting multi action / friend action cho từng area → user bấm area nào ra action của area đó",
       IMG + "\n- Đã có 3 area A1, A2, A3" + U1,
       "1. Set A1 = multi action (gắn tag), A2 = friend action (mở URL), A3 = action LINE URL scheme\n"
       "2. Quan sát danh sách conversion trong phần chọn action user\n3. 保存 → gửi cho U1\n"
       "4. U1 bấm lần lượt A1, A2, A3 → quan sát action nhận được",
       "3 area × 3 loại action",
       "- Danh sách conversion CHỈ hiện conversion có `type` = 2\n"
       "- Bấm A1: được gắn tag; bấm A2: mở URL; bấm A3: chạy LINE URL scheme\n"
       "- Mỗi area ra đúng action của chính nó",
       note="Nguồn: Type ảnh r91-r92, r111, r129-r130, r149."),

    tc("Media — image map", "FRIEND-001", "Normal",
       "Bug #31838: image map replace [name] và {name} đúng ở MỌI đường gửi",
       IMG + "\n- Đã bật image map và nhập [name] vào ô text của tab 詳細設定\n"
              "- Friend U1 tên LINE「テスト太郎」" + U1,
       "1. Với ô text để TRỐNG: gửi qua web (send test, chat 1:1, action ở màn friend list, đặt lịch), "
       "qua app (chat 1:1, đặt lịch), qua job (action auto reply/form/booking, build trước 5p, "
       "broadcast gửi luôn, scenario, remind) → quan sát text cuối\n"
       "2. Đổi ô text = [name] → lặp lại toàn bộ 12 đường gửi trên\n"
       "3. Đổi ô text = {name} → lặp lại toàn bộ 12 đường gửi",
       "3 giá trị ô text (trống / [name] / {name}) × 12 đường gửi",
       "- Ô text để trống: gửi đúng template, text cuối là message DEFAULT\n"
       "- Ô text = [name] hoặc {name}: TẤT CẢ 12 đường gửi đều replace thành tên LINE của friend "
       "(「テスト太郎」), KHÔNG còn chuỗi [name]/{name}",
       note="Nguồn: Type ảnh r34-r65 (Bug #31838, 11/09/2025 — replace [name] bị thiếu ở case image map). "
            "Gộp ma trận vì mỗi giá trị ô text CÙNG 1 kết quả mong đợi."),

    tc("Media — image map", "REG-SHARED-001", "Normal",
       "Bug #31838 — cover: replace [name] đúng ở 4 sub-type button qua web / app / job",
       ADM + "\n- Có 4 template button (standard / image / color / quick reply) đều có [name] "
              "ở ô PC display text" + U1,
       "1. Với từng sub-type: gửi qua web → quan sát text cuối\n2. Gửi qua app mobile → quan sát\n"
       "3. Gửi qua job → quan sát",
       "4 sub-type × 3 đường gửi",
       "- Cả 12 lượt đều replace [name] thành tên LINE của friend",
       note="Nguồn: Type ảnh r66-r77 (khối cover của Bug #31838)."),

    tc("Media — image map", "MSG-001", "Normal",
       "Gửi template image map (3 option area) qua web và job → LINE / chat 1:1 / app hiện đúng, bấm area ra action",
       IMG + U1,
       "1. Với option 手動で設定する: gửi qua chat 1:1, send test, broadcast, scenario, remind → "
       "quan sát ảnh + bấm area\n2. Lặp lại với option テンプレートから選ぶ\n"
       "3. Lặp lại với option không setting action",
       "3 option × 5 đường gửi",
       "- Mọi lượt: ảnh image map hiện đúng ở LINE user, chat 1:1 và app mobile\n"
       "- Bấm area chạy đúng action đã set (option không setting action thì không có action)",
       note="Nguồn: Type ảnh r100-r110, r138-r148, r153-r163."),

    tc("Media — image map", "CONC-002", "Abnormal",
       "Bug #31454: user bấm image map → redirect sang trang action done, 2 callback cách nhau <3s chỉ gửi 1 action",
       IMG + "\n- Template image map TM có area A1 CHỈ set action (không set mở URL)" + U1,
       "1. Gửi TM cho U1 bằng WEB (send test / chat 1:1)\n2. U1 bấm area A1 lần 1 → quan sát trang và action\n"
       "3. U1 bấm A1 lần 2 với khoảng cách < 3 giây → đếm action nhận được\n"
       "4. U1 bấm A1 lần 3 với khoảng cách > 3 giây → đếm action\n"
       "5. U1 bấm 2 area khác nhau → đếm action\n6. Cho 2 user cùng bấm image map → đếm action mỗi user",
       "bấm cùng area <3s và >3s; 2 area khác nhau; 2 user cùng bấm",
       "- Bấm lần 1: sau khi mở URL để action thì redirect tiếp sang trang action done "
       "「このページを閉じてください。」và action được gửi\n"
       "- 2 callback cách nhau < 3s: CHỈ gửi 1 action\n- 2 callback cách nhau > 3s: mỗi lần 1 action\n"
       "- Bấm 2 area khác nhau: gửi 2 action\n- 2 user cùng bấm: mỗi user nhận action riêng",
       note="Nguồn: Type ảnh r416-r419 (Bug #31454, 22/08/2025 — friend nhận message dù không bấm action; "
            "nguyên nhân trình duyệt tự reload). Ngưỡng dedupe 3s KHÔNG có trong spec → xem MT-39."),

    tc("Media — image map", "COMPAT-LEGACY-001", "Normal",
       "Bug #31454 trên iOS: mở trong LINE / browser ngoài → action done; mở lại browser lần nữa KHÔNG action lại",
       IMG + "\n- Template image map TM có area chỉ set action" + U1,
       "1. Trên iPhone, gửi TM cho U1 → bấm area khi mở trong LINE → quan sát trang và action\n"
       "2. Đặt setting mở ở trình duyệt ngoài → bấm area → quan sát\n"
       "3. Sau khi đã mở ở browser ngoài, mở lại trình duyệt lần nữa → quan sát action",
       "iOS; mở trong LINE và browser ngoài",
       "- Mở trong LINE và mở browser ngoài: đều redirect sang trang action done "
       "「このページを閉じてください。」và gửi được action\n"
       "- Mở lại trình duyệt lần nữa: KHÔNG action lại",
       env="PRODUCTION",
       note="Nguồn: Type ảnh r420-r422. ⚠ TC gốc note「case user nhấn back trình duyệt 2 lần về màn url "
            "action thì vẫn đang action tiếp」→ nhánh back 2 lần CHƯA được fix, xem MT-39. "
            "RULE-08: hành vi browser/LINE app phải xác nhận trên PRODUCTION."),

    tc("Media — image map", "COMPAT-LEGACY-001", "Normal",
       "Bug #31454 trên Android: mở trong LINE / browser ngoài → action done; mở lại KHÔNG action lại",
       IMG + "\n- Template image map TM có area chỉ set action" + U1,
       "1. Trên Android, gửi TM cho U1 → bấm area khi mở trong LINE → quan sát\n"
       "2. Bấm area khi mở ở trình duyệt ngoài → quan sát\n3. Mở lại trình duyệt lần nữa → quan sát action",
       "Android; mở trong LINE và browser ngoài",
       "- Cả 2 cách mở: redirect sang trang action done và gửi được action\n"
       "- Mở lại trình duyệt lần nữa: KHÔNG action lại",
       env="PRODUCTION",
       note="Nguồn: Type ảnh r423-r425. ⚠ TC gốc note「android không có setting open ngoài」→ cần Leader "
            "xác nhận Android có tùy chọn mở ngoài hay không."),

    tc("Media — image map", "REG-SHARED-001", "Normal",
       "Bug #31454 — regression: image map CHỈ mở URL / mở URL + action → logic giữ nguyên như cũ",
       IMG + U1,
       "1. Area chỉ set mở URL (không action): thử「LINEブラウザで開く」và「外部ブラウザで開く」; "
       "không set thời hạn và có set thời hạn (ngày giờ cố định, duration)\n"
       "2. Mở URL của tool: link form, event, item, conversion, salon, lesson\n"
       "3. Open khác: gửi text, mở profile LOA khác, mở trang add friend LOA khác, gọi điện, gửi mail\n"
       "4. LINE URL scheme: share LINE OA, share text, mở camera, mở camera roll, gửi vị trí, custom\n"
       "5. Lặp lại toàn bộ với area CÓ set cả action + mở URL\n"
       "6. Lặp lại toàn bộ cho image map gửi bằng JOB",
       "2 tổ hợp (chỉ URL / URL + action) × ~22 loại đích × 2 đường gửi (web, job)",
       "- Toàn bộ giữ LOGIC NHƯ CŨ: mở đúng đích bằng đúng browser, đúng hành vi hết hạn\n"
       "- Trường hợp có cả action: action vẫn được gửi kèm\n- Không nhánh nào bị action lặp",
       note="Nguồn: Type ảnh r426-r507 (Expect gốc đều là「Logic như cũ」). Gộp vì CÙNG 1 kết quả mong đợi; "
            "danh sách đích liệt kê đủ ở cột Các bước."),

    tc("Media — image map", "REG-URL-001", "Normal",
       "Open URL của button và image map: mở trong LINE / browser ngoài × thời hạn chỉ định / đếm ngược",
       ADM + "\n- Có template button và template image map, mỗi cái có action mở URL + multi action" + U1,
       "1. Với image map: set mở trong LINE + thời hạn CHỈ ĐỊNH → gửi test → bấm → quan sát\n"
       "2. Set mở trong LINE + thời hạn ĐẾM NGƯỢC (duration) → gửi test → bấm → quan sát\n"
       "3. Set mở browser NGOÀI + 2 kiểu thời hạn → gửi test → bấm → quan sát\n"
       "4. Lặp lại toàn bộ với template button\n5. Lặp lại qua đường gửi Send 1:1 và Send job (send all)",
       "2 loại template × 2 browser × 2 kiểu thời hạn × 3 đường gửi",
       "- Mỗi tổ hợp: URL mở ở ĐÚNG nơi (trong LINE hoặc browser ngoài)\n"
       "- Thời hạn hoạt động đúng: còn hạn mở được, hết hạn xử lý theo setting\n"
       "- Multi action vẫn được gửi kèm",
       note="Nguồn: open url của button image map r3-r6 và các khối Send 1:1 / Send job tương ứng."),

    tc("Media — image map", "LIFF-ENTRY-001", "Normal",
       "エルメで設定したページを開く từ button / image map → mở trong LINE, bấm X quay về màn chat",
       ADM + "\n- Bot A đã có form, calendar 予約, event 予約 và 商品販売 (1 lần và chu kỳ)" + U1,
       "1. Set action = mở trang フォーム作成 → gửi test → U1 bấm → quan sát trang mở và bấm icon X\n"
       "2. Lặp lại với カレンダー予約\n3. Lặp lại với イベント予約\n"
       "4. Lặp lại với 商品販売ページ: loại 1 lần; loại chu kỳ (order, change thẻ, cancel)\n"
       "5. Lặp lại toàn bộ ở cả template button và image map, qua Send test / Send 1:1 / Send job",
       "7 loại trang LME × 2 loại template × 3 đường gửi",
       "- Mọi tổ hợp: link mở ra TRONG LINE (LIFF)\n"
       "- Bấm icon X → trở về màn CHAT, KHÔNG ra màn trắng",
       note="Nguồn: open url của button image map r7-r13 và các khối tương ứng."),

    # ═════════════ 31. Media — video & audio ═════════════
    tc("Media — video & audio", "MEDIA-001", "Abnormal",
       "Video: chọn file KHÔNG phải mp4 → báo lỗi ファイルの形式が正しくありません。",
       ADM + "\n- Đã chọn loại「画像・動画・音声」→ kiểu 動画",
       "1. Chọn file .MOV → quan sát thông báo lỗi\n2. Bấm nút update video → quan sát popup chọn file",
       "file .MOV",
       "- Báo lỗi chính xác:「ファイルの形式が正しくありません。」, không upload\n"
       "- Popup chọn video đã lọc sẵn (clear) các định dạng không đúng",
       note="Nguồn: Type video r4, r8."),

    tc("Media — video & audio", "MEDIA-001", "Boundary",
       "Video: mp4 > 200MB → báo lỗi 200MBまでのファイルをアップロードできます; ≤200MB → upload thành công",
       ADM + "\n- Đã chọn kiểu 動画",
       "1. Chọn file mp4 210MB → quan sát thông báo\n2. Chọn file mp4 150MB → quan sát\n"
       "3. Sau upload thành công, quan sát phần setting media",
       "mp4 210MB và mp4 150MB",
       "- 210MB: báo lỗi chính xác「200MBまでのファイルをアップロードできます」, không upload\n"
       "- 150MB: upload thành công và hiện video đã upload ở phần setting media",
       note="Nguồn: Type video r5-r7. Khớp spec ui-spec.md:351 (200MB)."),

    tc("Media — video & audio", "MEDIA-001", "Normal",
       "Video: upload / đổi / xóa ảnh thumbnail; chọn định dạng khác bị chặn",
       ADM + "\n- Đã chọn kiểu 動画 và upload 1 video thành công",
       "1. Upload ảnh thumbnail → quan sát\n2. Bấm nút update ảnh → chọn ảnh khác → quan sát\n"
       "3. Trong popup chọn ảnh, thử chọn file video/audio → quan sát\n"
       "4. Bấm nút xóa ảnh khi CHƯA có ảnh → quan sát\n5. Bấm nút xóa ảnh khi ĐÃ có ảnh → quan sát",
       "ảnh thumbnail; file video/audio trong popup chọn ảnh",
       "- Upload/đổi ảnh thumbnail: hiện đúng ảnh tương ứng\n"
       "- Popup chọn ảnh TỰ CHẶN, không hiển thị các định dạng khác\n"
       "- Xóa ảnh khi chưa có ảnh: bấm không phản ứng gì\n- Xóa ảnh khi đã có: xóa đúng ảnh đó",
       note="Nguồn: Type video r9-r13."),

    tc("Media — video & audio", "MEDIA-001", "Abnormal",
       "Video: lưu khi CÓ video mà KHÔNG có thumbnail → lưu được nhưng user không xem được",
       ADM + "\n- Đã chọn kiểu 動画, đã upload video, CHƯA có thumbnail" + U1,
       "1. 保存 khi chỉ có video, không có thumbnail → quan sát\n2. Gửi cho U1 → quan sát tin trên LINE\n"
       "3. Thử trường hợp có thumbnail nhưng CHƯA chọn video → quan sát giao diện\n"
       "4. Trường hợp có đủ video + thumbnail → 保存 → gửi → quan sát",
       "3 tổ hợp: chỉ video / chỉ thumbnail / đủ cả 2",
       "- Chỉ có video: 保存 thành công nhưng user KHÔNG xem được video trên LINE\n"
       "- Chỉ có thumbnail: phải chọn video mới ra được giao diện type video có thumbnail\n"
       "- Đủ cả 2: 保存 và user xem được video bình thường",
       note="Nguồn: Type video r17-r19. ⚠ TC gốc r17 note「save ok send cho user thì user ko xem dc」→ "
            "hệ thống nên chặn lưu khi thiếu thumbnail; spec không ghi → xem MT-40."),

    tc("Media — video & audio", "MEDIA-001", "Normal",
       "Video: gửi qua chat 1:1 / send all / scenario / remind → LINE, chat 1:1 và app hiện đúng",
       ADM + "\n- Có template video TV đủ video + thumbnail" + U1,
       "1. Gửi TV qua chat 1:1 → quan sát video ở LINE, chat 1:1 và app mobile\n"
       "2. Gửi qua send all → quan sát 3 nơi\n3. Gửi qua scenario → quan sát\n4. Gửi qua remind → quan sát",
       "4 đường gửi × 3 nơi hiển thị",
       "- Cả 4 đường: video và thumbnail hiển thị đúng, phát được ở LINE user, chat 1:1 và app",
       note="Nguồn: Type video r20-r23."),

    tc("Media — video & audio", "FUNC-001", "Normal",
       "Video: edit video / thumbnail / action ở cả template mới và template cũ → 保存 và gửi đúng",
       ADM + "\n- Có template video MỚI (TV1) và template video CŨ (TV2)" + U1,
       "1. Với TV1 chưa có thumbnail: thêm thumbnail → 保存 → gửi → quan sát\n"
       "2. TV1 đã có thumbnail: đổi thumbnail khác → 保存 → gửi → quan sát\n"
       "3. TV1: đổi sang video khác (cả trường hợp có/chưa có thumbnail) → 保存 → gửi → quan sát\n"
       "4. TV1: thêm action rồi đổi action → 保存 → gửi → bấm → quan sát\n"
       "5. Lặp lại toàn bộ với TV2 (template cũ)\n6. Kiểm tra các chỗ đang gắn TV1/TV2 (send all, scenario, remind)",
       "template video mới và cũ; 4 loại thao tác edit",
       "- Mọi thao tác edit đều 保存 thành công\n- Tin trên LINE hiện đúng video/thumbnail/action MỚI\n"
       "- Các chỗ đang gắn template được cập nhật theo",
       note="Nguồn: Type video r24-r42."),

    tc("Media — video & audio", "MEDIA-001", "Abnormal",
       "Audio: chọn file KHÔNG phải m4a → báo lỗi ファイルの形式が正しくありません。",
       ADM + "\n- Đã chọn loại「画像・動画・音声」→ kiểu 音声",
       "1. Chọn file .wav → quan sát thông báo lỗi\n2. Thử file .mp3 → quan sát",
       "file .wav và .mp3",
       "- File .wav: báo lỗi chính xác「ファイルの形式が正しくありません。」\n"
       "- File .mp3: hành vi giống .m4a (theo TC gốc「mp3 và m4a giống nhau」)",
       note="Nguồn: Type audio r4. ⚠ Spec ui-spec.md:352 chỉ ghi .m4a; corpus nói .mp3 tương đương "
            "→ cần Leader xác nhận, xem MT-07."),

    tc("Media — video & audio", "MEDIA-001", "Boundary",
       "Audio: m4a > 200MB bị chặn; ≤200MB upload thành công và hiện ở phần setting media",
       ADM + "\n- Đã chọn kiểu 音声",
       "1. Chọn file m4a 210MB → quan sát\n2. Chọn file m4a 100MB → quan sát\n"
       "3. Quan sát phần setting media sau upload\n4. Bấm nút update audio → quan sát popup chọn file",
       "m4a 210MB và m4a 100MB",
       "- 210MB: bị chặn, báo lỗi vượt dung lượng\n- 100MB: upload thành công\n"
       "- Phần setting media hiện audio đã upload\n- Popup chọn audio đã CHẶN sẵn các loại file không đúng",
       note="Nguồn: Type audio r5-r8."),

    tc("Media — video & audio", "MSG-004", "Normal",
       "Audio / Video: tab 詳細設定 — text hiển thị ngoài màn list LINE user (để trống dùng quy định LINE)",
       ADM + "\n- Có template audio TA và template video TV" + U1,
       "1. Với TA: để trống ô text ở tab 詳細設定 → 保存 → gửi cho U1 → quan sát text ở khung thông báo\n"
       "2. Nhập text (gồm cả text Nhật) → 保存 → gửi → quan sát\n3. Lặp lại với TV",
       "để trống / có nhập text Nhật; audio và video",
       "- Để trống: hiện text theo quy định của LINE\n- Có nhập: hiện đúng text đã nhập",
       note="Nguồn: Type audio r9-r10 + Type video r15-r16. ⚠ TC gốc có note「save tiếng nhật lỗi」→ "
            "cần kiểm lại riêng trường hợp text Nhật, xem MT-34."),

    tc("Media — video & audio", "MSG-001", "Normal",
       "Audio: gửi qua chat 1:1 / send all / scenario / remind → phát được ở LINE, chat 1:1 và app",
       ADM + "\n- Có template audio TA" + U1,
       "1. Gửi TA qua chat 1:1 → quan sát và phát audio ở LINE, chat 1:1 và app mobile\n"
       "2. Gửi qua send all → quan sát 3 nơi\n3. Gửi qua scenario → quan sát\n4. Gửi qua remind → quan sát",
       "4 đường gửi × 3 nơi hiển thị",
       "- Cả 4 đường: audio hiển thị và PHÁT ĐƯỢC ở LINE user, chat 1:1 và app mobile",
       note="Nguồn: Type audio r12-r15."),

    tc("Media — video & audio", "FUNC-001", "Normal",
       "Audio: edit audio (mới và cũ), thêm action; chọn audio không hợp lệ bị chặn ở popup",
       ADM + "\n- Có template audio MỚI (TA1) và CŨ (TA2)" + U1,
       "1. TA1: không sửa gì → 保存 → quan sát\n2. TA1: đổi sang audio khác → 保存 → gửi → quan sát\n"
       "3. TA1: thêm action → 保存 → gửi → quan sát\n"
       "4. Trong popup chọn audio, thử chọn file không hợp lệ → quan sát\n"
       "5. Lặp lại với TA2\n6. Kiểm tra các chỗ đang gắn TA1/TA2 (send all, scenario, remind)",
       "template audio mới và cũ",
       "- Không sửa gì: 保存 thành công\n- Đổi audio và thêm action: 保存 và gửi đúng\n"
       "- File không hợp lệ bị CHẶN không hiển thị trong popup chọn\n"
       "- Các chỗ đang gắn template được cập nhật theo",
       note="Nguồn: Type audio r16-r23."),

    tc("Media — video & audio", "DATA-REF-001", "Normal",
       "Xóa template video / audio → mất khỏi màn template và khỏi send all / scenario / remind đang gắn",
       ADM + "\n- Template video TV và audio TA đang được gắn ở 1 broadcast, 1 scenario step, 1 remind",
       "1. Xóa TV ở màn template → quan sát danh sách\n"
       "2. Kiểm tra broadcast / scenario / remind đang gắn TV\n3. Lặp lại với TA",
       "TV và TA đang được gắn ở 3 nơi",
       "- Template mất khỏi màn list\n"
       "- Cả 3 nơi (send all, scenario, remind) đều xóa template tương ứng khỏi nội dung gửi",
       note="Nguồn: Type video r24-r42 (khối xóa) + Type audio r24-r28."),

    # ═════════════ 32. Sticker ═════════════
    tc("Sticker", "FUNC-001", "Normal",
       "Chọn group sticker → hiện sticker của group; chọn 1 sticker → hiện ở vùng đang chọn",
       ADM + "\n- Đã chọn loại「スタンプ」",
       "1. Quan sát giao diện màn chọn sticker\n2. Chọn 1 group stamp → quan sát vùng phía dưới\n"
       "3. Chọn 1 sticker trong group → quan sát vùng sticker đang được chọn",
       "1 group stamp, 1 sticker",
       "- Chọn group: hiện các sticker của group tương ứng ở phía dưới\n"
       "- Chọn sticker: sticker đó hiện ở phần「sticker đang được chọn」",
       note="Nguồn: Type stamp r3-r5. Spec ui-spec SCR-TMT-09 ghi 12 sticker pack LINE official."),

    tc("Sticker", "MSG-001", "Normal",
       "Gửi template sticker qua web (chat 1:1, send test) và job (send all, scenario, remind) → hiện đúng 3 nơi",
       ADM + "\n- Có template sticker TS đã lưu" + U1,
       "1. Gửi TS qua chat 1:1 → quan sát sticker ở LINE, chat 1:1 của tool và app mobile\n"
       "2. Gửi qua send test ở màn send all → quan sát 3 nơi\n3. Gửi qua send all (job) → quan sát\n"
       "4. Gửi qua scenario → quan sát\n5. Gửi qua remind → quan sát",
       "5 đường gửi × 3 nơi hiển thị",
       "- Cả 5 đường: sticker hiển thị đúng ở LINE user, chat 1:1 và app mobile",
       note="Nguồn: Type stamp r7-r11."),

    tc("Sticker", "FUNC-001", "Normal",
       "Edit template sticker (không sửa / đổi sticker cùng group / đổi sang group khác) → lưu và gửi đúng",
       ADM + "\n- Có template sticker MỚI (TS1) và CŨ (TS2)" + U1,
       "1. Mở edit TS1 → quan sát group và sticker đang được chọn\n2. Không sửa gì → 保存 → gửi → quan sát\n"
       "3. Đổi sang sticker khác CÙNG group → 保存 → gửi → quan sát\n"
       "4. Đổi sang sticker của group KHÁC → 保存 → gửi → quan sát\n5. Lặp lại với TS2 (template cũ)",
       "3 kịch bản edit; template mới và cũ",
       "- Màn edit hiện đúng group và sticker đã chọn trước đó\n"
       "- Cả 3 kịch bản 保存 thành công và sticker trên LINE khớp lựa chọn mới",
       note="Nguồn: Type stamp r12-r17."),

    tc("Sticker", "DATA-REF-001", "Normal",
       "Xóa template sticker → mất khỏi màn template và khỏi send all / scenario / remind đang gắn",
       ADM + "\n- Template sticker TS đang được gắn ở 1 broadcast, 1 scenario step, 1 remind",
       "1. Xóa TS ở màn template → quan sát danh sách\n"
       "2. Kiểm tra nội dung broadcast / scenario / remind đang gắn TS\n3. Chạy 3 luồng đó và quan sát tin",
       "TS gắn ở 3 nơi",
       "- TS mất khỏi màn list template\n- Cả 3 nơi đều xóa template tương ứng khỏi nội dung gửi\n"
       "- Tin gửi đi không còn sticker của TS",
       note="Nguồn: Type stamp r27-r31."),

    tc("Sticker", "DATA-BACKUP-001", "Normal",
       "Copy và Backup template sticker (dạng mới và dạng cũ) → dữ liệu sticker được giữ",
       ADM + "\n- Có template sticker dạng MỚI và dạng CŨ" + U1,
       "1. Copy template sticker dạng mới → mở bản copy đối chiếu group + sticker → gửi → quan sát\n"
       "2. Copy template sticker dạng cũ → đối chiếu → gửi → quan sát\n"
       "3. Backup sang bot B: kiểm tra template sticker ở bot B (cả dạng mới và cũ) → gửi → quan sát",
       "sticker dạng mới và cũ; copy và backup",
       "- Bản copy và bản backup đều giữ đúng group + sticker của bản gốc\n"
       "- Gửi được và sticker trên LINE khớp bản gốc",
       note="Nguồn: Type stamp r21-r26. ⚠ TC gốc chỉ có tiêu đề (không Expect Result) → kết quả mong đợi "
            "là SUY LUẬN CỦA AI, cần Leader xác nhận."),

    # ═════════════ 33. Location ═════════════
    tc("Location", "UI-001", "Normal",
       "Bản đồ: zoom bằng con lăn chuột; click 1 lần đặt pin đúng vị trí, pin default còn tới khi vào edit",
       ADM + "\n- Đã chọn loại「位置情報」\n- Google Maps API key hợp lệ",
       "1. Hover vào map, lăn chuột lên/xuống → quan sát\n2. Click 1 lần vào 1 điểm trên map → quan sát pin\n"
       "3. Quan sát pin default có còn hay không\n4. 保存 → vào lại màn edit → quan sát pin default",
       "1 điểm trên map",
       "- Lăn chuột: phóng to / thu nhỏ map\n- Click: pin đến ĐÚNG vị trí đã click\n"
       "- Pin default VẪN CÒN ở màn tạo; chỉ mất khi vào màn edit (giống bản cũ)",
       note="Nguồn: Type location r4-r5."),

    tc("Location", "FUNC-001", "Normal",
       "Khung search vị trí: nhập 1 phần ra gợi ý; chọn gợi ý / nhập toàn phần + Enter → pin và tự fill 送信情報",
       ADM + "\n- Đã chọn loại「位置情報」",
       "1. Nhập 1 phần địa chỉ vào khung search → quan sát danh sách gợi ý\n"
       "2. Chọn 1 gợi ý rồi Enter → quan sát map và mục 送信情報\n"
       "3. Nhập địa chỉ toàn phần rồi Enter → quan sát map và 送信情報\n"
       "4. Copy-paste địa chỉ vào khung search rồi Enter → quan sát",
       "địa chỉ「東京都渋谷区」(1 phần) và địa chỉ đầy đủ",
       "- Nhập 1 phần: hiện danh sách gợi ý chứa phần đã nhập\n"
       "- Chọn gợi ý / nhập toàn phần + Enter: map pin đúng vị trí và ĐƯA VỊ TRÍ PIN RA GIỮA khung map; "
       "mục 2 tự fill thông tin vị trí; phần 送信情報 KHÔNG bị ảnh hưởng",
       note="Nguồn: Type location r6-r8. ⚠ TC gốc note「bug: vị trí đc search chưa hiển thị ra giữa map」"
            "và「case coppy và paste vào mục search => ấn e…」→ 2 nhánh này dự kiến FAIL, xem MT-41."),

    tc("Location", "UI-INPUT-001", "Abnormal",
       "Bấm nút lấy thông tin vị trí pin khi CHƯA chọn vị trí → hiện required chọn vị trí",
       ADM + "\n- Đã chọn loại「位置情報」, chưa click chọn vị trí nào trên map",
       "1. Bấm nút「選択されているピンの位置で決定」\n2. Quan sát thông báo",
       "chưa chọn vị trí",
       "- Hiện thông báo required yêu cầu chọn vị trí\n- KHÔNG fill thông tin vào mục 送信情報",
       note="Nguồn: Type location r9. ⚠ TC gốc note「đang ko có phản ứng nào」→ dự kiến FAIL, xem MT-41."),

    tc("Location", "FUNC-001", "Normal",
       "Chọn vị trí trên map rồi bấm 選択されているピンの位置で決定 → fill map nhỏ + detail vị trí",
       ADM + "\n- Đã chọn loại「位置情報」",
       "1. Click chọn 1 vị trí trên map\n2. Bấm nút「選択されているピンの位置で決定」\n"
       "3. Quan sát mục 2 và phần 送信情報 (map nhỏ, title, detail)",
       "1 vị trí trên map",
       "- Mục 2 hiện thông tin vị trí\n"
       "- Phần 送信情報: map nhỏ hiện vị trí pin tương ứng; detail vị trí hiện ở dưới map và ở ô 位置情報詳細",
       note="Nguồn: Type location r10-r15."),

    tc("Location", "UI-INPUT-001", "Boundary",
       "位置情報タイトル: không bắt buộc, để trống thì auto-fill 位置情報。; nhập > 90 ký tự thì TỰ CẮT",
       ADM + "\n- Đã chọn loại「位置情報」, đã pin 1 vị trí",
       "1. Để trống ô 位置情報タイトル → 保存 → vào lại màn edit → quan sát ô title và phần 送信情報\n"
       "2. Nhập 95 ký tự vào ô title → 保存 → vào edit → đếm số ký tự còn lại\n"
       "3. Nhập text Nhật và text latinh hợp lệ → 保存 → vào edit → đối chiếu",
       "rỗng / 95 ký tự / text Nhật + latinh",
       "- Để trống: KHÔNG required, lưu được; vào edit thì title tự fill「位置情報。」\n"
       "- Nhập 95 ký tự: hệ thống TỰ CẮT còn 90 ký tự (không báo lỗi)\n"
       "- Text Nhật/latinh hợp lệ: lưu thành công và vào edit hiện đúng",
       note="Nguồn: Type location r17-r19. ⚠ Spec ui-spec.md:408 chỉ ghi「Max 90 ký tự」và feature-spec "
            "xếp cột DB vào Gap #2 → TC này lấp Gap (auto-fill + auto-truncate), xem MT-42."),

    tc("Location", "UI-INPUT-001", "Boundary",
       "位置情報詳細: không bắt buộc, để trống thì auto-fill クリックして地図を開いてください。。; > 90 ký tự TỰ CẮT",
       ADM + "\n- Đã chọn loại「位置情報」, đã pin 1 vị trí",
       "1. Để trống ô 位置情報詳細 → 保存 → vào edit → quan sát ô search, ô 位置情報詳細 và map nhỏ\n"
       "2. Nhập 95 ký tự → 保存 → vào edit → đếm ký tự\n3. Nhập text Nhật / latinh → 保存 → vào edit",
       "rỗng / 95 ký tự / text Nhật + latinh",
       "- Để trống: KHÔNG required; vào edit tự fill「クリックして地図を開いてください。。」vào ô search, "
       "ô 位置情報詳細 và phần map nhỏ\n"
       "- 95 ký tự: TỰ CẮT còn 90 ký tự\n- Text Nhật/latinh: lưu thành công và vào edit hiện đúng",
       note="Nguồn: Type location r20-r22. Xem MT-42."),

    tc("Location", "DATA-TEXT-001", "Abnormal",
       "位置情報詳細 nhập XUỐNG DÒNG → phía LINE user KHÔNG xuống dòng, màn edit vẫn giữ xuống dòng",
       ADM + "\n- Đã chọn loại「位置情報」, đã pin 1 vị trí" + U1,
       "1. Nhập ô 位置情報詳細 có 2 dòng → 保存\n2. Gửi cho U1 → quan sát nội dung detail trên LINE\n"
       "3. Vào lại màn edit → quan sát ô 位置情報詳細",
       "detail 2 dòng",
       "- Phía LINE user: nội dung detail KHÔNG xuống dòng (hiện liền 1 dòng)\n"
       "- Màn edit: ô 位置情報詳細 VẪN giữ xuống dòng",
       note="Nguồn: Type location r23. Lệch giữa web và LINE — spec không ghi → xem MT-42."),

    tc("Location", "FUNC-001", "Normal",
       "Nút 送信する位置情報の住所を引用 → fill địa chỉ đang pin vào ô detail (kể cả khi ô đã có data)",
       ADM + "\n- Đã chọn loại「位置情報」",
       "1. Chưa chọn vị trí trên map → bấm nút「送信する位置情報の住所を引用」→ quan sát\n"
       "2. Pin 1 vị trí, ô detail đang TRỐNG → bấm nút → quan sát ô detail\n"
       "3. Ô detail đã CÓ data → bấm nút → quan sát ô detail",
       "3 trạng thái: chưa pin / ô trống / ô có data",
       "- Chưa chọn vị trí: hiện msg required chọn vị trí\n"
       "- Ô trống: fill địa chỉ đang pin vào ô detail\n- Ô đã có data: GHI ĐÈ bằng địa chỉ đang pin",
       note="Nguồn: Type location r26-r28."),

    tc("Location", "STATE-001", "Normal",
       "Sửa ô 位置情報詳細 → mục ② 送信する位置情報を決定する KHÔNG đổi, map nhỏ đổi theo detail",
       ADM + "\n- Đã pin vị trí và đã bấm 選択されているピンの位置で決定",
       "1. Sửa nội dung ô 位置情報詳細 thành text khác\n"
       "2. Quan sát mục ②「送信する位置情報を決定する」\n3. Quan sát phần map nhỏ",
       "sửa detail thành text khác",
       "- Mục ②「送信する位置情報を決定する」: thông tin KHÔNG thay đổi\n"
       "- Map nhỏ: thông tin detail vị trí ĐỔI theo nội dung vừa nhập",
       note="Nguồn: Type location r25."),

    tc("Location", "FUNC-001", "Normal",
       "Lưu template location với 4 tổ hợp title/detail/pin → giá trị auto-fill đúng ở màn edit và 送信情報",
       ADM + "\n- Đã chọn loại「位置情報」",
       "1. Không nhập title và detail, KHÔNG pin vị trí → 保存 → vào edit → quan sát ô search, map, mục 2, "
       "phần 送信情報\n2. Không nhập title và detail, CÓ pin vị trí → 保存 → vào edit → quan sát\n"
       "3. Không nhập title, CÓ nhập detail, có pin → 保存 → vào edit → quan sát\n"
       "4. CÓ nhập title, không nhập detail, có pin → 保存 → vào edit → quan sát",
       "4 tổ hợp title / detail / pin",
       "- TH1: ô search =「クリックして地図を開いてください。。」, map ở vị trí biển, mục 2 = "
       "「クリックして地図を開いてください。。」; 送信情報: map ở biển, title =「位置情報。」, "
       "detail =「クリックして地図を開いてください。。」\n"
       "- TH2: như TH1 nhưng map ở vị trí ĐÃ PIN\n"
       "- TH3: ô search = data đã nhập, map ở vị trí pin, mục 2 TRỐNG; 送信情報: title =「位置情報。」, "
       "detail = data đã nhập\n"
       "- TH4: ô search và mục 2 =「クリックして地図を開いてください。。」; 送信情報: title = data đã nhập, "
       "detail =「クリックして地図を開いてください。。」",
       note="Nguồn: Type location r29-r32. ⚠ TC gốc r30 và r32 có note「chưa tự fill vào detail」→ "
            "2 nhánh này dự kiến FAIL, xem MT-42."),

    tc("Location", "MSG-001", "Normal",
       "Gửi template location qua web và job → chat 1:1 hiện như cũ, LINE user hiện theo format MỚI",
       ADM + "\n- Có template location TL đã lưu đủ title + detail + vị trí" + U1,
       "1. Gửi TL qua chat 1:1 → quan sát ở chat 1:1 của tool, ở LINE user và ở app mobile\n"
       "2. Gửi qua send test ở màn send all → quan sát 3 nơi\n3. Gửi qua send all (job) → quan sát\n"
       "4. Gửi qua scenario → quan sát\n5. Gửi qua remind → quan sát",
       "5 đường gửi × 3 nơi hiển thị",
       "- Chat 1:1 của tool: hiển thị NHƯ CŨ\n- Phía LINE user: hiển thị theo FORMAT MỚI\n"
       "- App mobile: hiển thị đúng\n- Cả 5 đường gửi cùng kết quả",
       note="Nguồn: Type location r33-r37."),

    tc("Location", "FUNC-001", "Normal",
       "Edit template location (mới và cũ): không sửa / sửa không lưu / sửa có lưu",
       ADM + "\n- Có template location MỚI (TL1) và CŨ (TL2)",
       "1. Mở edit TL1, không sửa gì → 保存 → quan sát và vào lại edit\n"
       "2. Sửa vị trí pin nhưng KHÔNG 保存 → thoát → vào lại edit → quan sát\n"
       "3. Sửa vị trí pin → 保存 → vào lại edit → quan sát\n"
       "4. Sửa title / sửa detail lấy theo pin / sửa detail không theo pin → 保存 → quan sát\n"
       "5. Lặp lại 1-3 với TL2\n6. Kiểm tra các chỗ đang gắn TL1/TL2 (send all, scenario, remind)",
       "template location mới và cũ; 3 kịch bản",
       "- Không sửa gì: 保存 thành công, dữ liệu không đổi\n"
       "- Sửa không 保存: KHÔNG lưu thông tin mới\n- Sửa và 保存: lưu đúng thông tin mới\n"
       "- Các chỗ đang gắn template được cập nhật theo",
       note="Nguồn: Type location r38-r51. ⚠ TC gốc r39 note「chưa hiển thị dc map đúng thông tin đã "
            "chọn lúc tạo」→ xem MT-41."),

    tc("Location", "DATA-REF-001", "Normal",
       "Bug #32364 — KHÔNG bật định vị PC: pin vị trí khác vị trí hiện tại → vào edit và gửi vẫn đúng vị trí đã pin",
       ADM + "\n- TẮT quyền định vị (geolocation) của trình duyệt trên PC" + U1,
       "1. Tạo template location, pin vị trí KHÁC vị trí hiện tại → 保存 → vào edit → quan sát vị trí\n"
       "2. Không sửa gì → 保存 → vào edit → quan sát → gửi test cho U1 → quan sát vị trí trên LINE\n"
       "3. Pin sang vị trí KHÁC → 保存 → vào edit → quan sát → gửi từ chat 1:1 → quan sát trên LINE\n"
       "4. Sau khi edit, COPY template → mở bản copy → quan sát vị trí → gửi từ auto reply → quan sát\n"
       "5. Lặp lại toàn bộ với trường hợp pin ở vị trí DEFAULT (gửi từ button của template khác)",
       "định vị PC TẮT; pin vị trí khác vị trí hiện tại và pin vị trí default",
       "- Vào edit luôn hiện ĐÚNG vị trí đã pin ở lần lưu gần nhất, KHÔNG bị ghi đè bởi vị trí hiện tại\n"
       "- Gửi cho user (send test / chat 1:1 / auto reply / button) đều hiện đúng thông tin vị trí đã pin\n"
       "- Bản copy giữ đúng vị trí và gửi đúng",
       note="Nguồn: Type location r52-r60 (Bug #32364, 09/10/2025 — location từ backend bị override bởi "
            "geolocation hiện tại; fix: chỉ gọi getCurrentPosition() khi không có lat_old/lgn_old)."),

    tc("Location", "DATA-REF-001", "Normal",
       "Bug #32364 — CÓ bật định vị PC: pin vị trí khác / pin vị trí hiện tại → không bị override",
       ADM + "\n- BẬT quyền định vị (geolocation) của trình duyệt trên PC" + U1,
       "1. Tạo template location, pin vị trí KHÁC vị trí hiện tại → 保存 → vào edit → quan sát\n"
       "2. Không sửa gì → 保存 → vào edit → gửi cho U1 → quan sát vị trí trên LINE\n"
       "3. Pin sang vị trí khác → 保存 → vào edit → gửi → quan sát\n"
       "4. Copy template sau khi edit → mở bản copy → gửi → quan sát\n"
       "5. Lặp lại toàn bộ với trường hợp pin ĐÚNG vị trí hiện tại",
       "định vị PC BẬT; pin vị trí khác và pin đúng vị trí hiện tại",
       "- Vào edit luôn hiện đúng vị trí đã pin, KHÔNG bị thay bằng vị trí hiện tại của máy\n"
       "- Gửi cho user hiện đúng vị trí đã pin\n- Bản copy giữ đúng vị trí",
       note="Nguồn: Type location r61-r68."),

    tc("Location", "DATA-REF-001", "Normal",
       "Copy / Backup / Xóa template location → dữ liệu vị trí được giữ; xóa thì mất ở mọi nơi gắn",
       ADM + "\n- Template location TL dạng mới và dạng cũ; TL đang gắn ở 1 broadcast, 1 scenario, 1 remind",
       "1. Copy TL (dạng mới và dạng cũ) → mở bản copy đối chiếu vị trí/title/detail → gửi → quan sát\n"
       "2. Backup sang bot B → kiểm tra template location ở bot B → gửi → quan sát\n"
       "3. Xóa TL ở màn template → kiểm tra broadcast / scenario / remind đang gắn",
       "TL dạng mới và cũ; gắn ở 3 nơi",
       "- Bản copy và bản backup giữ đúng vị trí, title, detail; gửi được và LINE hiện đúng\n"
       "- Xóa TL: mất khỏi màn list và bị xóa khỏi cả 3 nơi đang gắn",
       note="Nguồn: Type location r74-r84. ⚠ Phần copy/backup TC gốc chỉ có tiêu đề → kết quả mong đợi "
            "là SUY LUẬN CỦA AI, cần Leader xác nhận."),
]

# ── Cột「Trạng thái đánh giá spec」──
# Quy tắc: TC tham chiếu ít nhất 1 mã MÂU THUẪN thuộc nhóm SPEC-SILENT (spec không ghi / spec tự
# nhậ­n chưa rõ) →「Spec không ghi」. Các MT còn lại là trưồng hợp spec CÓ ghi nhưng LỆCH với TC
# → giữ「Spec ghi rõ」. TC do AI suy luậ­n mà cả corpus và spec đều không có cũng đánh「Spec không ghi」.
_SPEC_SILENT_MT = {
    "MT-04", "MT-08", "MT-09", "MT-10", "MT-11", "MT-12", "MT-13", "MT-14", "MT-15", "MT-16",
    "MT-17", "MT-18", "MT-19", "MT-20", "MT-21", "MT-22", "MT-23", "MT-24", "MT-25", "MT-26",
    "MT-27", "MT-28", "MT-29", "MT-30", "MT-31", "MT-32", "MT-34", "MT-35", "MT-36", "MT-37",
    "MT-39", "MT-41", "MT-42", "MT-43", "MT-45", "MT-47", "MT-48", "MT-49",
}
_AI_INFER = "SUY LUẬN CỦA AI"
for _r in S5:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
