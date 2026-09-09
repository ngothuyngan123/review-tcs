# -*- coding: utf-8 -*-
"""FA-010 テンプレート — Nhóm 19-27: loại パネル・ボタン (4 sub-type) + Button ảnh.

Nguồn chính: 02. TCsLine_Template
  - tab「Template button」(2023 → 03/2026, 1619 dòng, 953 TC lá — tab master của loại button;
    cột kết quả SpecImprove #36203, Bug KH #35114/#35112, Bug KH #34923)
  - tab「Task nhỏ+ check Bug Kh」r109-r223 (mã màu), r614-r696 (count URL-encode 900 ký tự)
  - tab「Improve tạo temp」(SpecChange #24890 — title/description 40/60 ký tự; SpecChange #24912 — emoji)
  - tab「Modal action」+「Modal act Text」(nhãn hiển thị của action trong modal)
"""
import re as _re

from _common import tc

ADM = ("- Đăng nhập admin (主管理者) bot A trên môi trường STAGING\n"
       "- Folder F1 có group template G1; đang ở màn tạo template con của G1")
BTN = ADM + "\n- Đã chọn loại tin nhắn「パネル・ボタン」"
STD = BTN + "\n- Đã chọn sub-type「スタンダード」"
U1 = "\n- Đã đăng ký friend U1 làm クイックテストユーザー"

S4 = [
    # ═════════════ 19. Panel/Button — chọn loại ═════════════
    tc("Panel/Button — chọn loại", "FUNC-001", "Normal",
       "Chọn từng sub-type button → hiện đúng giao diện setting và lưu đúng type_button 1/2/3/4",
       BTN,
       "1. Chọn sub-type「スタンダード」→ quan sát giao diện setting panel và nút\n"
       "2. Lần lượt chọn「カラーボタン」,「画像」,「クイックリプライ」→ quan sát giao diện mỗi loại\n"
       "3. Với mỗi loại: nhập dữ liệu tối thiểu và 保存\n4. Kiểm tra cột `template.type_button`",
       "4 sub-type",
       "- Chọn loại nào thì hiện giao diện setting panel/nút tương ứng của loại đó\n"
       "- `template.type_button`: standard = 1, カラーボタン = 2, 画像 = 3, クイックリプライ = 4",
       note="Nguồn: Template button r5."),

    tc("Panel/Button — chọn loại", "UI-001", "Normal",
       "Tab sub-type đang chọn hiện chữ đậm, tab không chọn hiện chữ thường; hover/click có hiệu ứng",
       BTN,
       "1. Quan sát 4 tab sub-type khi chưa chọn gì\n2. Chọn「スタンダード」→ quan sát tab được chọn và 3 tab còn lại\n"
       "3. Hover chuột lên từng tab → quan sát hiệu ứng\n4. Click sang tab khác → quan sát",
       "4 tab sub-type",
       "- Tab đang được chọn hiển thị chữ ĐẬM; tab không chọn hiển thị chữ thường\n"
       "- Hover và click có hiệu ứng đúng design",
       note="Nguồn: Template button r6-r7, r11."),

    tc("Panel/Button — chọn loại", "STATE-DEP-001", "Abnormal",
       "Màn edit KHÔNG cho đổi sub-type button — 3 loại còn lại bị disable",
       BTN + "\n- Đã lưu template button TB sub-type「スタンダード」",
       "1. Mở màn edit của TB\n2. Quan sát mục「メッセージタイプ」\n3. Quan sát 4 tab sub-type\n"
       "4. Thử click sang tab「カラーボタン」",
       "TB sub-type standard",
       "- Mục「メッセージタイプ」hiện text「パネル・ボタン」(không phải dropdown)\n"
       "- Tab「スタンダード」đang được control; 3 tab còn lại DISABLE, không click được\n"
       "- Không đổi được sub-type",
       note="Nguồn: Template button r8-r10. Spec BR-01 (message type bất biến)."),

    tc("Panel/Button — chọn loại", "COMPAT-LEGACY-001", "Normal",
       "Mở edit template button CŨ → hiện đúng sub-type theo type_button, các loại khác disable",
       ADM + "\n- Có template button cũ với `type_button` = 1 (standard)",
       "1. Mở màn edit template button cũ đó\n2. Quan sát tab sub-type đang được control\n"
       "3. Quan sát 3 tab còn lại",
       "template cũ `type_button` = 1",
       "- Màn edit hiển thị đúng sub-type「スタンダード」\n- 3 tab sub-type khác ở trạng thái disable",
       note="Nguồn: Template button r12."),

    tc("Panel/Button — chọn loại", "COMPAT-LEGACY-001", "Normal",
       "Template button cũ dạng template ĐƠN (không thuộc pack) → hiện, edit, gửi đều đúng",
       ADM + "\n- Có template button cũ dạng template ĐƠN (không nằm trong group/pack)" + U1,
       "1. Mở edit template đó, đối chiếu toàn bộ dữ liệu với bản gốc bên LME\n"
       "2. Sửa title / description → 保存 → gửi cho U1\n3. Thêm rồi xóa 1 panel → 保存 → gửi\n"
       "4. Thêm rồi xóa 1 nút → 保存 → gửi\n5. Sửa action của nút → 保存 → gửi\n"
       "6. Sửa msg hiển thị ở list → 保存 → quan sát cột「内容」\n"
       "7. Gửi qua job (broadcast) và qua web (chat 1:1)",
       "template button cũ dạng đơn; 5 loại thao tác edit",
       "- Màn edit hiện ĐỦ dữ liệu của template cũ\n"
       "- Cả 5 thao tác edit đều 保存 thành công và tin trên LINE khớp nội dung đã sửa\n"
       "- Gửi được cả qua job và qua web",
       note="Nguồn: Template button r13-r22. Gộp các thao tác vì CÙNG 1 kết quả mong đợi "
            "(save success + send cho user ok)."),

    tc("Panel/Button — chọn loại", "COMPAT-LEGACY-001", "Normal",
       "Template button cũ dạng PACK template → hiện, edit (kể cả thêm template dạng mới vào pack), gửi đúng",
       ADM + "\n- Có pack template cũ chứa template button (1 panel và nhiều panel)" + U1,
       "1. Mở pack, đối chiếu dữ liệu template button bên trong (1 panel và nhiều panel)\n"
       "2. Gửi pack cho U1 → quan sát tin trên LINE\n3. Sửa title/description → 保存 → gửi\n"
       "4. Thêm/xóa panel → 保存 → gửi\n5. Thêm/xóa nút → 保存 → gửi\n6. Sửa action → 保存 → gửi\n"
       "7. Thêm 1 template dạng MỚI vào pack → 保存 → gửi\n8. Gửi pack qua job và qua web (chat 1:1)",
       "pack template cũ; thêm template dạng mới vào pack",
       "- Dữ liệu template button trong pack hiện đủ ở màn edit\n"
       "- Mọi thao tác edit đều 保存 thành công; tin trên LINE khớp nội dung sau sửa\n"
       "- Thêm được template dạng mới vào pack cũ và gửi được\n- Gửi được cả qua job và web",
       note="Nguồn: Template button r23-r32."),

    # ═════════════ 20. Panel/Button — panel & ảnh ═════════════
    tc("Panel/Button — panel & ảnh", "UI-001", "Normal",
       "Vùng preview panel: hiện tối đa 4 panel, >4 panel thì scroll ngang",
       STD,
       "1. Tạo template có 3 panel → quan sát vùng preview panel\n"
       "2. Thêm panel tới 6 panel → quan sát vùng preview\n3. Scroll ngang vùng preview",
       "3 panel rồi 6 panel",
       "- Với 3 panel: hiện đủ 3 panel, không có scroll ngang\n"
       "- Với 6 panel: màn hình hiện tối đa 4 panel và xuất hiện SCROLL NGANG, scroll xem được 6 panel",
       note="Nguồn: Template button r36."),

    tc("Panel/Button — panel & ảnh", "UI-003", "Normal",
       "Preview panel khi CHƯA set data → hiện ảnh default và placeholder cho title/content/nút",
       STD,
       "1. Tạo panel mới, không nhập gì\n2. Quan sát khối preview của panel đó",
       "panel rỗng",
       "- Vùng ảnh hiện ẢNH DEFAULT\n- Vùng title, content để trống\n"
       "- Vùng title/explain và tên nút hiện PLACEHOLDER",
       note="Nguồn: Template button r37."),

    tc("Panel/Button — panel & ảnh", "OUT-PREVIEW-001", "Normal",
       "Preview panel khi ĐÃ set data → hiện đúng ảnh, title, content (content chữ đậm), list nút",
       STD,
       "1. Set ảnh cho panel → quan sát preview\n2. Nhập title (gồm 1 dòng và 1 trường hợp có xuống dòng) "
       "→ quan sát preview\n3. Nhập content (gồm trường hợp xuống dòng) → quan sát preview\n"
       "4. Thêm 3 nút với text khác nhau → quan sát preview",
       "ảnh 1024x678, title 2 dòng, content 2 dòng, 3 nút",
       "- Preview hiện đúng ảnh đã set\n- Title hiện đúng nội dung, giữ ngắt dòng\n"
       "- Content hiện đúng nội dung, giữ ngắt dòng và hiển thị CHỮ ĐẬM\n"
       "- Hiện đủ list 3 nút với đúng text từng nút",
       note="Nguồn: Template button r38-r41."),

    tc("Panel/Button — panel & ảnh", "UI-001", "Normal",
       "Nút「編集中」của panel: hover đổi màu, click thì tự scroll xuống vùng nhập data của panel đó",
       STD + "\n- Template đang có 4 panel",
       "1. Hover chuột vào nút「編集中」của panel 3 → quan sát màu nút\n2. Click nút đó\n"
       "3. Quan sát vị trí scroll của trang",
       "4 panel, tác động panel 3",
       "- Hover: nút đổi màu\n- Click: trang tự động scroll xuống phần nhập data của ĐÚNG panel 3",
       note="Nguồn: Template button r42-r43."),

    tc("Panel/Button — panel & ảnh", "UI-001", "Normal",
       "Nút (...) của panel: hover hiện menu copy panel / di chuyển trái / di chuyển phải / xóa panel",
       STD + "\n- Template đang có 4 panel",
       "1. Hover vào nút (...) của panel 1 → quan sát menu\n2. Đếm và đối chiếu các mục trong menu\n"
       "3. Hover vào nút (...) của panel 4 (panel cuối trong vùng hiển thị) → quan sát menu",
       "4 panel",
       "- Menu hiện đủ 4 mục: copy panel, di chuyển panel sang trái, di chuyển panel sang phải, xóa panel\n"
       "- Nút (...) đổi màu khi hover\n- Menu của panel 4 vẫn hiện đầy đủ, KHÔNG bị che/cắt",
       note="Nguồn: Template button r44-r45. ⚠ TC gốc có note「panel thứ 4: khi hover vào btn ... "
            "=> sẽ ko hiển thị dc sub-menu」→ chính là 1 trong 2 yêu cầu của SpecImprove #36203, "
            "xem MT-27."),

    tc("Panel/Button — panel & ảnh", "UI-001", "Normal",
       "SpecImprove #36203: menu (...) của panel thứ 5→10 KHÔNG bị che khi hover",
       STD,
       "1. Tạo template có 5 panel → hover nút (...) của panel 5 → quan sát menu\n"
       "2. Tăng dần lên 6, 7, 8, 9, 10 panel; mỗi lần hover nút (...) của panel ngoài cùng bên phải\n"
       "3. Với mỗi lần, kiểm tra menu có hiện đủ 4 mục và có bị tràn ra ngoài vùng hiển thị hay không",
       "template có 5, 6, 7, 8, 9, 10 panel",
       "- Ở mọi số lượng panel, menu (...) hiện ĐỦ 4 mục và KHÔNG bị che bởi viền vùng preview\n"
       "- Menu tự lật hướng khi panel ở sát rìa phải",
       note="Nguồn: Template button r1577-r1583 (SpecImprove #36203, 01/05/2026 — yêu cầu 1: "
            "panel right-side menu bị che). Áp cho cả button standard / color / image (r1590, r1603)."),

    tc("Panel/Button — panel & ảnh", "UI-001", "Normal",
       "SpecImprove #36203: xóa panel luôn hiện modal confirm; bấm キャンセル thì không xóa",
       STD + "\n- Template có 5 panel, panel 3 đã có ảnh + nút + action, panel 4 chưa có gì",
       "1. Hover (...) panel 3 (đã có dữ liệu) → chọn xóa → quan sát modal confirm\n"
       "2. Bấm「キャンセル」→ quan sát panel 3\n3. Lặp lại với panel 4 (chưa có dữ liệu)\n"
       "4. Xóa liên tục 2 panel: xóa panel 1, xác nhận; xóa tiếp panel 2, xác nhận\n"
       "5. Quan sát số panel còn lại và thứ tự",
       "panel đã có dữ liệu / panel rỗng / xóa liên tục 2 panel",
       "- CẢ 2 trường hợp (panel có dữ liệu và panel rỗng) đều hiện modal confirm xóa\n"
       "- Bấm「キャンセル」→ modal đóng, panel KHÔNG bị xóa, dữ liệu panel giữ nguyên\n"
       "- Xóa liên tục: mỗi lần đều hiện modal confirm; sau 2 lần còn đúng 3 panel, thứ tự dồn đúng",
       note="Nguồn: Template button r1584-r1615 (SpecImprove #36203 — yêu cầu 2: delete confirm)."),

    tc("Panel/Button — panel & ảnh", "UI-INPUT-001", "Abnormal",
       "Nếu CÓ panel set ảnh thì TẤT CẢ panel phải set ảnh — thiếu thì báo lỗi パネル{N}に画像が登録されておりません。",
       STD,
       "1. Tạo template 3 panel, KHÔNG panel nào set ảnh → 保存 → quan sát\n"
       "2. Set ảnh cho panel 1, để panel 2 và 3 không ảnh → 保存 → quan sát thông báo lỗi\n"
       "3. Set ảnh cho cả 3 panel → 保存 → quan sát",
       "3 panel; 0 ảnh / 1 ảnh / 3 ảnh",
       "- Không panel nào có ảnh: LƯU THÀNH CÔNG\n"
       "- Có ít nhất 1 panel có ảnh mà panel khác thiếu: báo lỗi cho từng panel thiếu, nội dung "
       "「パネル<số thứ tự của panel>に画像が登録されておりません。」và KHÔNG lưu\n"
       "- Cả 3 panel đều có ảnh: LƯU THÀNH CÔNG",
       note="Nguồn: Template button r46-r48. Rule all-or-nothing này KHÔNG có trong spec → xem MT-09."),

    tc("Panel/Button — panel & ảnh", "MEDIA-IMG-001", "Normal",
       "Resize ảnh nhiều panel theo tỉ lệ ảnh của PANEL 1 (vuông/dài → 1:1, chữ nhật → 2:3)",
       STD + U1,
       "1. Tạo template 3 panel, panel 1 dùng ảnh VUÔNG, panel 2-3 dùng ảnh khác tỉ lệ → 保存 → gửi cho U1\n"
       "2. Quan sát tỉ lệ ảnh 3 panel trên LINE\n"
       "3. Tạo template khác: panel 1 dùng ảnh HÌNH CHỮ NHẬT → 保存 → gửi → quan sát tỉ lệ",
       "panel 1 ảnh vuông (1000x1000) / panel 1 ảnh chữ nhật (1024x678)",
       "- Panel 1 ảnh vuông hoặc dài: ảnh của TẤT CẢ panel được resize về tỉ lệ 1:1\n"
       "- Panel 1 ảnh hình chữ nhật: ảnh của tất cả panel resize về tỉ lệ 2:3\n"
       "- Tin trên LINE hiện đúng tỉ lệ đã resize cho mọi panel",
       note="Nguồn: Template button r52. Spec chỉ nhắc `rate_image_button` mà không nêu công thức "
            "→ xem MT-10."),

    tc("Panel/Button — panel & ảnh", "MEDIA-IMG-001", "Normal",
       "Ma trận tỉ lệ ảnh panel: height/width ≤ 3 và > 3 → tạo/sửa ở 4 sub-type và 4 màn đều hiển thị đúng",
       ADM + U1,
       "1. Với template button standard: set ảnh panel 1 có tỉ lệ height/width ≤ 3 → 保存 → gửi → quan sát\n"
       "2. Đổi ảnh panel 1 sang tỉ lệ height/width > 3 → 保存 → gửi → quan sát\n"
       "3. Lặp lại cho panel 2, 3\n4. Lặp lại toàn bộ với sub-type カラーボタン / 画像 / クイックリプライ "
       "(gồm cả trường hợp KHÔNG set ảnh)\n"
       "5. Lặp lại ở màn tạo template của scenario / broadcast (send all) / remind\n"
       "6. Vào edit từng template rồi 保存 lại → gửi → quan sát",
       "2 mốc tỉ lệ (≤3 và >3) × 4 sub-type × 4 màn tạo × tạo/edit; gồm cả case không set ảnh",
       "- Mọi tổ hợp: ảnh hiển thị đúng trong preview và trong tin trên LINE, KHÔNG bị méo/mất ảnh\n"
       "- Trường hợp không set ảnh: panel hiện không có ảnh, không lỗi",
       note="Nguồn: Template button r1264-r1408 (Bug #26507 — error msg khi tỉ lệ ảnh bất thường). "
            "Gộp ma trận vì CÙNG 1 kết quả mong đợi."),

    tc("Panel/Button — panel & ảnh", "FUNC-001", "Normal",
       "Copy panel: copy 1 panel và nhiều panel, copy giữ cả action; ≥10 panel thì chặn copy",
       STD,
       "1. Template có 3 panel, panel 2 đã set ảnh + 2 nút có action → hover (...) panel 2 → copy panel\n"
       "2. Quan sát panel mới: ảnh, title, content, nút và action\n3. Copy tiếp 2 panel khác\n"
       "4. Tạo template có 10 panel → bấm copy panel → quan sát\n5. Double click nút copy panel",
       "3 panel rồi 10 panel; panel nguồn có action",
       "- Copy panel: panel mới có đủ ảnh/title/content/nút và ACTION giống panel nguồn\n"
       "- Copy được nhiều panel liên tiếp\n- Khi đã có 10 panel: nút copy panel bị chặn/disable\n"
       "- Double click copy chỉ tạo 1 panel",
       note="Nguồn: Template button r159-r162, r536-r544."),

    tc("Panel/Button — panel & ảnh", "FUNC-001", "Normal",
       "Sort panel: di chuyển trái/phải giữa các vị trí, kể cả template 10 panel",
       STD + "\n- Template có 3 panel P1, P2, P3",
       "1. Di chuyển P2 → vị trí 1 → quan sát thứ tự\n2. Di chuyển P1 → vị trí 3 → quan sát\n"
       "3. Sắp lại toàn bộ 3 panel theo thứ tự mới → 保存 → vào edit lại\n"
       "4. Tạo template 10 panel: di chuyển panel giữa → cuối, panel giữa → đầu, panel cuối → đầu, "
       "đổi 2 panel cạnh nhau (1-2, 5-6, 9-10)",
       "template 3 panel và template 10 panel",
       "- Mỗi lần di chuyển, panel về đúng vị trí và các panel khác dịch đúng bậc\n"
       "- Sau 保存 và vào edit lại, thứ tự panel giữ đúng\n- Tin trên LINE hiện panel theo thứ tự mới",
       note="Nguồn: Template button r163-r166, r545-r557."),

    tc("Panel/Button — panel & ảnh", "FUNC-001", "Normal",
       "Xóa panel → panel mất, các panel còn lại giữ nguyên dữ liệu và dồn thứ tự đúng",
       STD + "\n- Template có 3 panel, mỗi panel có ảnh + 2 nút có action",
       "1. Xóa panel 2 → xác nhận\n2. Quan sát số panel còn lại và dữ liệu từng panel\n"
       "3. 保存 → vào edit lại → đối chiếu\n4. Gửi cho U1 → quan sát tin trên LINE",
       "3 panel, xóa panel giữa",
       "- Còn 2 panel (P1, P3), dữ liệu ảnh/nút/action của 2 panel này KHÔNG bị đổi\n"
       "- Sau 保存 và edit lại: vẫn đúng 2 panel\n- Tin trên LINE chỉ có 2 panel",
       note="Nguồn: Template button r167-r169, r558-r560."),

    tc("Panel/Button — panel & ảnh", "MEDIA-IMG-001", "Boundary",
       "Upload ảnh panel: đúng/không đúng 1000x1000, >10MB, sai định dạng, tên file có ký tự Nhật/space",
       BTN + "\n- Đã chọn sub-type「画像」",
       "1. Upload ảnh KHÔNG phải 1000x1000 → quan sát\n2. Upload ảnh đúng 1000x1000 → quan sát\n"
       "3. Upload ảnh > 10MB → quan sát thông báo\n"
       "4. Upload file không phải ảnh và ảnh định dạng .avif → quan sát\n"
       "5. Upload ảnh .jpg / .png / .gif / .jpeg → quan sát\n"
       "6. Upload ảnh có tên file chứa text Nhật và chứa dấu space → quan sát",
       "ảnh 1000x1000 và khác; 12MB; .avif và file không phải ảnh; .jpg/.png/.gif/.jpeg; "
       "tên file「テスト画像 01.png」",
       "- Ảnh không đúng 1000x1000: vẫn upload được (hệ thống tự resize theo tỉ lệ panel 1)\n"
       "- Ảnh > 10MB: báo lỗi vượt dung lượng, không upload\n"
       "- File không phải ảnh và .avif: bị chặn\n- .jpg / .png / .gif / .jpeg: upload thành công\n"
       "- Tên file chứa text Nhật/space: upload thành công, ảnh hiển thị đúng",
       note="Nguồn: Template button r595-r601. ⚠ Corpus cho phép .gif/.jpeg trong khi spec ui-spec.md:350 "
            "chỉ ghi .png/.jpg → xem MT-07."),

    tc("Panel/Button — panel & ảnh", "CONC-001", "Abnormal",
       "Double click nút「保存」template button → chỉ tạo 1 bản ghi template",
       STD,
       "1. Cấu hình đủ 1 panel + 1 nút\n2. Double click nhanh nút「保存」\n"
       "3. Về màn list template con và đếm số template",
       "double click",
       "- Chỉ tạo ĐÚNG 1 template button, không có bản ghi trùng lặp",
       note="Nguồn: Improve list template r601, r629 (Check nhấn duplicate button save template)."),

    # ═════════════ 21. Panel/Button — tiêu đề & nội dung ═════════════
    tc("Panel/Button — tiêu đề & nội dung", "UI-INPUT-001", "Boundary",
       "Title panel: không nhập vẫn gửi được; ≤40 ký tự lưu OK; >40 báo lỗi タイトルは40文字以内で入力してください。",
       STD + U1,
       "1. Bỏ trống title, nhập content hợp lệ → 保存 → gửi cho U1 → quan sát\n"
       "2. Nhập title 40 ký tự → 保存 → quan sát\n3. Nhập title 41 ký tự → 保存 → quan sát thông báo lỗi",
       "title: rỗng / 40 ký tự / 41 ký tự",
       "- Title rỗng: lưu thành công và gửi được button bình thường (title không bắt buộc)\n"
       "- 40 ký tự: lưu thành công\n"
       "- 41 ký tự: báo lỗi「タイトルは40文字以内で入力してください。」và không lưu",
       note="Nguồn: Improve tạo temp r11-r14 (SpecChange #24890, 28/12/2023 — đổi title từ 20 lên 40) "
            "+ Template button r53-r55 (khối CŨ ghi 20 ký tự). ⚠ 2 khối TC mâu thuẫn, đã chọn theo "
            "khối MỚI HƠN và khớp spec (40) → xem MT-03."),

    tc("Panel/Button — tiêu đề & nội dung", "UI-INPUT-001", "Boundary",
       "Content panel (本文): bắt buộc; ≤60 ký tự lưu OK; >60 báo lỗi 本文は60文字以内で入力してください。",
       STD,
       "1. Bỏ trống content → 保存 → quan sát\n2. Nhập content 60 ký tự → 保存 → quan sát\n"
       "3. Nhập content 61 ký tự → 保存 → quan sát thông báo lỗi",
       "content: rỗng / 60 ký tự / 61 ký tự",
       "- Content rỗng: báo lỗi bắt buộc nhập, KHÔNG lưu\n- 60 ký tự: lưu thành công\n"
       "- 61 ký tự: báo lỗi「本文は60文字以内で入力してください。」và không lưu",
       note="Nguồn: Improve tạo temp r15-r18 (SpecChange #24890 — đổi description từ 40 lên 60) "
            "+ Template button r70-r72 (khối CŨ ghi 40 ký tự). ⚠ xem MT-03. "
            "Nội dung msg lỗi 60 ký tự là SUY LUẬN theo mẫu msg 40 ký tự của TC gốc — cần Leader xác nhận."),

    tc("Panel/Button — tiêu đề & nội dung", "UI-INPUT-001", "Boundary",
       "Khi title CÓ gán [name] hoặc {name} → giới hạn hiển thị đổi thành 20/40 và [name] chiếm 20 ký tự",
       STD,
       "1. Nhập title chưa có [name] → quan sát bộ đếm\n2. Chèn [name] vào title → quan sát bộ đếm\n"
       "3. Nhập thêm cho tổng phần text (ngoài [name]) < 20 ký tự → 保存 → quan sát\n"
       "4. Nhập đúng 20 ký tự → 保存 → quan sát\n5. Nhập 21 ký tự → 保存 → quan sát",
       "title có [name]; phần text: <20 / =20 / >20 ký tự",
       "- Chưa có [name]: bộ đếm hiện 0/40\n"
       "- Sau khi chèn [name]: bộ đếm chuyển thành 20/40 ([name] tính là 20 ký tự)\n"
       "- Phần text <20 và =20: lưu thành công\n- Phần text >20: báo lỗi, không lưu",
       note="Nguồn: Improve tạo temp r3-r6 (SpecChange #24890). "
            "Rule [name] chiếm 20 ký tự KHÔNG có trong spec → xem MT-04."),

    tc("Panel/Button — tiêu đề & nội dung", "UI-INPUT-001", "Boundary",
       "Khi content CÓ gán [name] → giới hạn hiển thị đổi thành 20/60, phần text tối đa 40 ký tự",
       STD,
       "1. Chèn [name] vào content → quan sát bộ đếm\n"
       "2. Nhập phần text < 40 ký tự → 保存 → quan sát\n3. Nhập đúng 40 ký tự → 保存 → quan sát\n"
       "4. Nhập 41 ký tự → 保存 → quan sát",
       "content có [name]; phần text: <40 / =40 / >40 ký tự",
       "- Sau khi chèn [name]: bộ đếm hiện 20/60\n- Phần text <40 và =40: lưu thành công\n"
       "- Phần text >40: báo lỗi, không lưu",
       note="Nguồn: Improve tạo temp r7-r10 (SpecChange #24890). Xem MT-04."),

    tc("Panel/Button — tiêu đề & nội dung", "DATA-TEXT-001", "Normal",
       "Title / content cho phép xuống dòng → preview và tin trên LINE giữ đúng ngắt dòng",
       STD + U1,
       "1. Nhập title có 2 dòng → quan sát preview panel\n2. Nhập content có 2 dòng → quan sát preview\n"
       "3. 保存 → gửi cho U1 → quan sát tin trên LINE",
       "title 2 dòng, content 2 dòng",
       "- Cho phép nhập xuống dòng ở cả title và content\n"
       "- Preview hiện đúng text đã xuống dòng\n- Tin trên LINE hiện đúng ngắt dòng",
       note="Nguồn: Template button r56, r73."),

    tc("Panel/Button — tiêu đề & nội dung", "UI-002", "Normal",
       "Icon「?」cạnh nút hiện tooltip đúng nguyên văn về cơ chế tự gửi ボタンテキスト",
       STD,
       "1. Hover / click vào icon「?」ở phần nút\n2. Đối chiếu nội dung tooltip",
       "—",
       "- Tooltip hiện ĐÚNG nguyên văn: 「ボタンタップ時、【ボタンテキスト】が友だち側から自動送信されます。"
       "なお、友だちアクション・LINE URLスキームが設定されている場合は送信されません。」",
       note="Nguồn: Template button r57."),

    tc("Panel/Button — tiêu đề & nội dung", "FUNC-001", "Normal",
       "Insert LINE名 / 友だち情報 / emoji vào title và content → chèn đúng vị trí con trỏ",
       STD + "\n- Bot A có ≥2 friend info tự tạo",
       "1. Đặt con trỏ giữa title → bấm insert「LINE名」→ quan sát chuỗi\n"
       "2. Bấm insert「友だち情報」→ chọn 1 friend info tự tạo → quan sát chuỗi\n"
       "3. Bấm insert icon (emoji) → chọn 1 emoji → quan sát\n4. Lặp lại 3 bước với ô content",
       "3 loại insert × 2 ô (title, content)",
       "- Mỗi lần insert đều chèn code/emoji vào ĐÚNG vị trí con trỏ chuột, không chèn ở cuối\n"
       "- Chuỗi chèn cho LINE名 là `{name}`; friend info là code dạng `[FRIEND_INFO_...]`",
       note="Nguồn: Template button r58-r61, r74-r77 + Improve tạo temp r19 (SpecChange #24912 — "
            "thêm emoji vào template mới). ⚠ TC gốc r59/r75 ghi「design mới bỏ đi」phần insert friend "
            "info BASIC → xem MT-28."),

    tc("Panel/Button — tiêu đề & nội dung", "FRIEND-001", "Normal",
       "Gửi qua WEB → title/content replace đúng {name}, friend info basic, friend info tự tạo và emoji",
       STD + "\n- Friend U1 tên LINE「テスト太郎」, có đủ friend info basic (system name, mail, số đt, "
             "ngày sinh, địa chỉ) và 1 friend info tự tạo" + U1,
       "1. Tạo template button có title/content chèn {name} + friend info basic + friend info tự tạo + emoji\n"
       "2. 保存\n3. Gửi qua web: send test / chat 1:1 / gửi bằng action ở màn friend list\n"
       "4. Quan sát title và content trong tin trên LINE",
       "U1 có đủ giá trị friend info",
       "- `{name}` được thay bằng tên LINE「テスト太郎」\n"
       "- Code friend info basic thay bằng giá trị tương ứng của U1\n"
       "- Code friend info tự tạo thay bằng `friendinfo_value` của U1\n- Emoji hiển thị đúng",
       note="Nguồn: Template button r62-r65, r78-r81."),

    tc("Panel/Button — tiêu đề & nội dung", "FRIEND-001", "Normal",
       "Gửi qua JOB (tạo mới / get thẳng / clone) → title/content replace đúng như gửi qua web",
       STD + "\n- Friend U2 có đủ friend info; template button có chèn {name} + friend info + emoji",
       "1. Gắn template vào broadcast/scenario theo 3 cách: tạo mới tại màn đó, get thẳng từ template, "
       "clone từ template\n2. Chờ job gửi cho U2\n3. Quan sát title và content trong tin trên LINE",
       "3 cách gắn template × job gửi",
       "- Cả 3 cách: `{name}`, friend info basic, friend info tự tạo và emoji đều được replace đúng "
       "giá trị của U2\n- Kết quả giống nhánh gửi qua web",
       note="Nguồn: Template button r66-r69, r82-r85."),

    tc("Panel/Button — tiêu đề & nội dung", "FRIEND-001", "Abnormal",
       "Friend THIẾU giá trị friend info → phần code bị bỏ qua, KHÔNG hiện chuỗi code trên LINE",
       STD + "\n- Friend U3 KHÔNG có giá trị cho「電話番号」và 1 friend info tự tạo",
       "1. Gửi template button (title/content có chèn 2 code trên) cho U3 qua web\n"
       "2. Quan sát title/content trong tin trên LINE\n3. Lặp lại qua job",
       "U3 thiếu 2 giá trị friend info",
       "- Tin trên LINE KHÔNG hiện chuỗi code, phần thiếu giá trị được bỏ trống\n"
       "- Các phần text khác của title/content vẫn hiện bình thường",
       note="Nguồn: Template button r63-r64, r79-r80 (「nếu không có thông tin thì bỏ qua, cũng sẽ k "
            "hiện text của code」)."),

    tc("Panel/Button — tiêu đề & nội dung", "MSG-002", "Abnormal",
       "Nhập text là số 0 ở 本文 / ボタンテキスト / ラベル / タイトル → gửi được, không sinh error message",
       ADM + U1,
       "1. Template Quick reply: set ラベル(nút) = 0, nội dung câu hỏi = 0, và trường hợp type image "
       "với ラベル = 0 → 保存 → gửi qua job send all → quan sát\n"
       "2. Template Standard: 本文 = 0; ボタンテキスト = 0 với 1 panel và với 2 panel → 保存 → gửi job → quan sát\n"
       "3. Template Button color: 本文 = 0; ボタンテキスト = 0 → 保存 → gửi job → quan sát\n"
       "4. Template Button image: ラベル = 0; タイトル = 0 → 保存 → gửi qua action / send all / "
       "step_message → quan sát\n5. Kiểm tra màn /basic/error-list",
       "chuỗi「0」ở 本文 / ボタンテキスト / ラベル / タイトル; 4 sub-type; nhiều đường gửi",
       "- Mọi trường hợp: 保存 thành công và tin ĐẾN ĐƯỢC LINE user, hiện đúng ký tự「0」\n"
       "- Màn /basic/error-list KHÔNG phát sinh bản ghi lỗi mới",
       note="Nguồn: Template button r1501-r1539 (khối SpecChange #32577 / Bug KH — text là số 0 gây "
            "error msg). Gộp vì CÙNG 1 kết quả mong đợi."),

    tc("Panel/Button — tiêu đề & nội dung", "MSG-002", "Abnormal",
       "altText của template button là DẤU CÁCH → không sinh error message ở mọi đường gửi",
       ADM + U1,
       "1. Tạo template button standard, set altText (PC display text) = 1 dấu cách → 保存\n"
       "2. Gửi qua chat 1:1 và qua đặt lịch (job) → quan sát tin trên LINE và /basic/error-list\n"
       "3. Lặp lại với button color, button ảnh, button quick, image map (send test)\n"
       "4. Đổi altText = data thật rồi gửi lại → quan sát",
       "altText = 1 dấu cách; 4 sub-type + image map; gửi web và job",
       "- Mọi trường hợp gửi được tin, LINE user nhận được đầy đủ\n"
       "- KHÔNG phát sinh bản ghi lỗi ở /basic/error-list\n- altText = data thật vẫn gửi bình thường",
       note="Nguồn: Template button r1428-r1443 (Bug #29838, 12/05/2025 — altText = dấu cách gây error msg)."),

    # ═════════════ 22. Panel/Button — nút & action ═════════════
    tc("Panel/Button — nút & action", "FUNC-001", "Normal",
       "Mặc định mỗi panel có 1 nút; bấm「ボタン追加」thêm nút xuống dưới",
       STD,
       "1. Tạo panel mới → đếm số nút mặc định\n2. Bấm「ボタン追加」→ quan sát vị trí nút mới",
       "panel mới",
       "- Mặc định mỗi panel có 1 nút\n- Bấm「ボタン追加」thêm 1 nút xuống PHÍA DƯỚI nút hiện có",
       note="Nguồn: Template button r86."),

    tc("Panel/Button — nút & action", "FUNC-001", "Boundary",
       "Giới hạn nút: 1 panel → tối đa 4 nút; ≥2 panel → tối đa 3 nút/panel, đủ thì disable ボタン追加 và copy",
       STD,
       "1. Template chỉ có 1 panel: bấm「ボタン追加」tới khi không thêm được nữa → đếm số nút\n"
       "2. Quan sát nút「ボタン追加」và nút copy sau khi đủ\n"
       "3. Thêm panel thứ 2 → với mỗi panel, bấm「ボタン追加」tới khi không thêm được → đếm số nút\n"
       "4. Quan sát 2 nút trên",
       "template 1 panel và template 2 panel",
       "- 1 panel: thêm được tối đa 4 nút; đủ 4 thì「ボタン追加」và nút copy đều DISABLE\n"
       "- ≥2 panel: mỗi panel thêm được tối đa 3 nút; đủ 3 thì「ボタン追加」và nút copy DISABLE",
       note="Nguồn: Template button r87-r88. Khớp spec BR-08."),

    tc("Panel/Button — nút & action", "UI-INPUT-001", "Boundary",
       "ボタンテキスト: bắt buộc; ≤20 ký tự lưu OK; >20 báo lỗi",
       STD,
       "1. Bỏ trống ボタンテキスト → 保存 → quan sát\n2. Nhập đúng 20 ký tự → 保存 → quan sát\n"
       "3. Nhập 21 ký tự → 保存 → quan sát",
       "rỗng / 20 ký tự / 21 ký tự",
       "- Rỗng: báo lỗi bắt buộc nhập, không lưu\n- 20 ký tự: lưu thành công\n"
       "- 21 ký tự: báo lỗi vượt giới hạn, không lưu",
       note="Nguồn: Template button r90-r92 (TC gốc kèm link tài liệu LINE Messaging API xác nhận "
            "max 20 ký tự). Khớp spec ui-spec.md:271."),

    tc("Panel/Button — nút & action", "UI-001", "Normal",
       "Nút「パネル選択に戻る」→ trang tự scroll lên phần chọn panel",
       STD + "\n- Template có 4 panel, đang scroll ở phần nhập data của panel 4",
       "1. Bấm nút「パネル選択に戻る」\n2. Quan sát vị trí scroll",
       "4 panel",
       "- Trang tự scroll lên đúng phần chọn panel ở đầu màn hình",
       note="Nguồn: Template button r89."),

    tc("Panel/Button — nút & action", "FUNC-001", "Normal",
       "Nút KHÔNG set action nào → vẫn lưu được (theo design mới)",
       STD,
       "1. Cấu hình 1 panel, 1 nút có ボタンテキスト, KHÔNG set bất kỳ loại action nào\n2. 保存",
       "nút không có action",
       "- Lưu thành công, KHÔNG báo lỗi",
       note="Nguồn: Template button r93 (「design mới cho phép ko cần chọn action nào cũng tạo dc」). "
            "⚠ TC gốc để cả Expect cũ「báo lỗi」và mới「save success」→ đã chọn theo design MỚI, "
            "xem MT-29."),

    tc("Panel/Button — nút & action", "FUNC-MULTI-001", "Normal",
       "Set 1 trong 3 loại action hoặc set nhiều loại cùng lúc → đều lưu được",
       STD,
       "1. Chỉ set multi action (エルメアクション) → 保存 → quan sát\n"
       "2. Chỉ set friend action → 保存 → quan sát\n3. Chỉ set LINE URL scheme → 保存 → quan sát\n"
       "4. Set cùng lúc multi action + friend action → 保存 → quan sát",
       "4 tổ hợp action",
       "- Cả 4 tổ hợp đều lưu thành công, KHÔNG báo lỗi",
       note="Nguồn: Template button r94-r95."),

    tc("Panel/Button — nút & action", "FUNC-MULTI-001", "Normal",
       "Tạo / edit / xóa multi action cho nút; action có filter; lưu đúng vào t_actions",
       STD,
       "1. Bấm「アクション登録・編集」→ quan sát giao diện khi chưa có action\n"
       "2. Tạo 2 action (VD gắn tag + gửi template) → quan sát khối preview action đã tạo\n"
       "3. Kiểm tra bản ghi `t_actions` và `t_actions_detail`\n4. Tạo thêm 1 action CÓ set filter\n"
       "5. Edit 1 action → quan sát preview\n6. Xóa 1 action → quan sát preview",
       "3 action, trong đó 1 action có filter",
       "- Tạo/edit/xóa action đều phản ánh đúng ở khối preview action\n"
       "- Bản ghi `t_actions` + `t_actions_detail` khớp với action đã cấu hình (kể cả filter)\n"
       "- Preview action hiện theo giao diện mới (đúng nhãn từng loại action)",
       note="Nguồn: Template button r96-r102. ⚠ TC gốc r97 note「bug ở sheet Modal action」→ "
            "nhãn action xem nhóm dưới."),

    tc("Panel/Button — nút & action", "UI-001", "Normal",
       "Nhãn hiển thị của action trong modal và tab 詳細設定 đúng cho nhóm template / rich menu / step",
       STD + "\n- Bot A có ≥1 template, ≥1 rich menu, ≥1 scenario (step) để chọn trong action",
       "1. Tạo action loại「テンプレート送信」→ quan sát nhãn ở list action và ở tab setting detail của nút\n"
       "2. Tạo action rich menu: hiển thị / dừng hiển thị → quan sát nhãn\n"
       "3. Tạo action step: dừng, start từ đầu, start từ ngày xx → quan sát nhãn\n"
       "4. Tạo action「テキスト送信」→ quan sát nhãn\n5. Lặp lại toàn bộ với 4 sub-type button",
       "4 sub-type button × 2 vị trí hiển thị (list action, tab 詳細設定)",
       "- Nhãn hiển thị đúng nguyên văn: template →「を送信」· rich menu hiển thị →「を表示」· "
       "rich menu dừng →「表示を停止」· step dừng →「停止」· step start từ đầu →「を開始」· "
       "step start từ xx →「をxx日目から再開」· text →「を送信」\n"
       "- Nhãn giống nhau ở cả 2 vị trí hiển thị và ở cả 4 sub-type",
       note="Nguồn: Modal action r3-r9, r36-r42 + Modal act Text r3-r9. Gộp theo nhóm action vì "
            "mỗi nhóm được verify trong 1 lượt; nhãn từng biến thể liệt kê đủ ở KQ mong đợi."),

    tc("Panel/Button — nút & action", "UI-001", "Normal",
       "Nhãn action nhóm remind / tag / bookmark / status đối ứng / block đúng nguyên văn",
       STD + "\n- Bot A có ≥1 remind, ≥1 tag, ≥1 status đối ứng",
       "1. Tạo action remind: start / dừng → quan sát nhãn ở list action và tab 詳細設定\n"
       "2. Tạo action tag: gắn / gỡ → quan sát nhãn\n3. Tạo action bookmark: gắn / remove → quan sát nhãn\n"
       "4. Tạo action status đối ứng: set / gỡ → quan sát nhãn\n"
       "5. Tạo action block: block / unblock / ẩn user / hiển thị lại user → quan sát nhãn",
       "12 biến thể action, 2 vị trí hiển thị",
       "- Nhãn đúng nguyên văn: remind start →「を開始」· remind dừng →「を停止」· gắn tag →「をつける」· "
       "gỡ tag →「をはずす」· bookmark gắn →「つける」· bookmark remove →「外す」· status set →「をつける」· "
       "status gỡ →「外す」· block →「ブロックする」· unblock →「ブロック解除」· ẩn user →「非表示にする」· "
       "hiển thị lại →「再表示する」\n- Nhãn giống nhau ở cả 2 vị trí hiển thị",
       note="Nguồn: Modal action r10-r15, r30-r35, r43-r48, r63-r68."),

    tc("Panel/Button — nút & action", "UI-001", "Normal",
       "Nhãn action friend info (text / select / ngày tháng) đúng nguyên văn",
       STD + "\n- Bot A có friend info kiểu Mô tả, kiểu Lựa chọn, kiểu Ngày tháng",
       "1. Tạo action friend info kiểu text: xóa thông tin đăng ký / gán giá trị → quan sát nhãn\n"
       "2. Lặp lại với friend info kiểu select\n"
       "3. Với friend info kiểu ngày tháng: xóa thông tin / gán ngày cố định / gán ngày hiện tại → quan sát nhãn\n"
       "4. Mở lại popup action và kiểm tra giá trị ngày đã gán có hiện lại hay không",
       "3 kiểu friend info, 7 biến thể action",
       "- Nhãn đúng nguyên văn: xóa thông tin →「の登録情報を削除」· gán giá trị (text/select) →"
       "「に〇〇〇〇〇〇〇〇…を登録」· gán ngày cố định →「にyyyy/mm/dd…を登録」· gán ngày hiện tại →"
       "「に当日日付を登録」\n"
       "- Nhãn giống nhau ở list action và tab 詳細設定",
       note="Nguồn: Modal action r16-r22, r49-r55. ⚠ TC gốc r22 note「ở phần list action khi mở popup "
            "lên: phần ngày gán sẽ bị trống (trên step bản cũ cũng vậy)」→ xem MT-30."),

    tc("Panel/Button — nút & action", "UI-001", "Normal",
       "Nhãn action friend info kiểu ĐIỂM (6 biến thể gán/cộng/trừ, chỉ định và random) đúng nguyên văn",
       STD + "\n- Bot A có friend info kiểu Điểm",
       "1. Tạo action friend info điểm: xóa thông tin đăng ký → quan sát nhãn\n"
       "2. Gán giá trị chỉ định / gán giá trị random → quan sát nhãn\n"
       "3. Cộng giá trị chỉ định / cộng random → quan sát nhãn\n"
       "4. Trừ giá trị chỉ định / trừ random → quan sát nhãn\n5. Đối chiếu ở cả tab 詳細設定",
       "7 biến thể action điểm",
       "- Nhãn đúng nguyên văn: xóa →「の登録情報を削除」· gán chỉ định →「に〇を登録」· "
       "gán random →「に〇~〇(ランダム)を登録」· cộng chỉ định →「に〇をプラス」· "
       "cộng random →「に〇~〇(ランダム)をプラス」· trừ chỉ định →「に〇をマイナス」· "
       "trừ random →「に〇~〇(ランダム)をマイナス」\n- Nhãn giống nhau ở cả 2 vị trí hiển thị",
       note="Nguồn: Modal action r23-r29, r56-r62."),

    tc("Panel/Button — nút & action", "FUNC-DATE-001", "Abnormal",
       "Friend action — validate thời hạn mở URL: ngày quá khứ bị chặn, khoảng thời gian phải nhập ngày",
       STD,
       "1. Set friend action mở URL, chọn thời hạn kiểu chỉ định ngày giờ → chọn ngày trong QUÁ KHỨ → quan sát\n"
       "2. Chọn ngày hôm nay nhưng giờ đã qua → 保存 → quan sát\n"
       "3. Chọn thời hạn kiểu khoảng thời gian, KHÔNG nhập số ngày → 保存 → quan sát\n"
       "4. Nhập số ngày = 0 rồi > 0 → 保存 → quan sát",
       "ngày quá khứ / giờ đã qua / số ngày rỗng / 0 / >0",
       "- Ô ngày KHÔNG chọn được ngày trong quá khứ\n"
       "- Giờ đã qua trong ngày hôm nay: vẫn chọn được và 保存 thành công\n"
       "- Khoảng thời gian bỏ trống số ngày: báo lỗi, không lưu\n"
       "- Số ngày = 0 và > 0: lưu thành công",
       note="Nguồn: Template button r103-r105."),

    tc("Panel/Button — nút & action", "REG-URL-001", "Normal",
       "Friend action mở URL: 4 tổ hợp browser × thời hạn lưu đúng cột buttons và hoạt động đúng phía user",
       STD + U1,
       "1. Set mở URL, chọn「LINEブラウザで開く」+ KHÔNG set thời hạn → 保存 → kiểm tra cột `buttons` "
       "→ gửi cho U1 → bấm nút\n"
       "2. Chọn「LINEブラウザで開く」+ thời hạn CHỈ ĐỊNH ngày giờ → 保存 → kiểm tra cột → bấm nút trước "
       "và sau hạn\n"
       "3. Chọn「LINEブラウザで開く」+ thời hạn KHOẢNG TIME → 保存 → kiểm tra cột → bấm trước và sau hạn\n"
       "4. Lặp lại 3 bước với「外部ブラウザで開く」",
       "2 loại browser × 3 kiểu thời hạn",
       "- `buttons.flag_open_url_in_browser` = 0 khi mở trong LINE, = 1 khi mở browser ngoài\n"
       "- Không set thời hạn: `is_setting_url_expired_date` = 0, bấm nút luôn mở được URL\n"
       "- Thời hạn chỉ định: `is_setting_url_expired_date` = 1, lưu `date_url_expired_date` + "
       "`time_url_expired_date`; trước hạn mở được URL bằng đúng browser đã chọn, sau hạn bấm KHÔNG có phản ứng\n"
       "- Thời hạn khoảng time: lưu `number_day_url_expired_date` + `time_url_expired_date`; "
       "hết hạn sau xx ngày yy giờ tính từ lúc gửi, sau hạn bấm không phản ứng",
       note="Nguồn: Template button r106-r109 và các dòng tiếp theo của khối「check tạo action friend」."),

    tc("Panel/Button — nút & action", "FUNC-001", "Normal",
       "Sort / copy / xóa nút trong panel → thứ tự và dữ liệu (kể cả action) đúng",
       STD + "\n- Panel 1 có 3 nút, nút 2 đã set multi action + friend action",
       "1. Sort đổi thứ tự 3 nút → quan sát\n2. Copy nút 2 → quan sát nút mới (text + action)\n"
       "3. Ở màn TẠO mới: copy nút rồi 保存 → vào edit đối chiếu\n"
       "4. Ở màn EDIT: copy nút rồi 保存 → vào edit đối chiếu\n5. Xóa 1 nút → 保存 → vào edit đối chiếu",
       "3 nút, nút 2 có action",
       "- Sort: thứ tự nút đổi đúng và giữ sau 保存\n"
       "- Copy nút: nút mới có đủ ボタンテキスト và ACTION giống nút nguồn\n"
       "- Copy ở cả màn tạo và màn edit đều lưu đúng\n- Xóa nút: nút mất, các nút còn lại không đổi",
       note="Nguồn: Template button r135-r144."),

    tc("Panel/Button — nút & action", "COMPAT-LEGACY-001", "Normal",
       "Template button CŨ: friend action vẫn hiện, edit và gửi đúng",
       ADM + "\n- Có template button cũ đã set friend action (mở URL + call số điện thoại)" + U1,
       "1. Mở edit template cũ → quan sát friend action đã set\n2. Sửa friend action → 保存\n"
       "3. Gửi cho U1 → bấm nút → quan sát hành vi",
       "template button cũ có friend action",
       "- Màn edit hiện đúng friend action đã lưu\n- Sửa và 保存 thành công\n"
       "- Bấm nút trên LINE thực hiện đúng friend action mới",
       note="Nguồn: Template button r145-r158, r356-r373, r515-r534."),

    # ═════════════ 23. Panel/Button — mã màu ═════════════
    tc("Panel/Button — mã màu", "UI-INPUT-001", "Normal",
       "Mã màu HỢP LỆ (hoa / thường / hoa-thường lẫn, số, chữ, copy-paste) → lưu OK và LINE hiện đúng màu",
       BTN + "\n- Đã chọn sub-type「カラーボタン」" + U1,
       "1. Ở ô mã màu của タイトル: nhập #FFFFFF (toàn hoa) → 保存 → gửi cho U1 → quan sát màu\n"
       "2. Nhập #ffffff (toàn thường) → 保存 → gửi → quan sát\n3. Nhập #0aF9C3 (hoa lẫn thường) → 保存 → gửi\n"
       "4. Nhập mã toàn số (#123456), toàn chữ (#abcdef), số + chữ (#12ab34) → 保存 → gửi\n"
       "5. Copy-paste 1 mã màu hợp lệ vào ô → 保存 → gửi",
       "#FFFFFF · #ffffff · #0aF9C3 · #123456 · #abcdef · #12ab34 · mã copy-paste",
       "- Mọi mã hợp lệ đều 保存 thành công\n"
       "- Màn web hiển thị nội dung đúng mã màu đã chọn\n- Phía LINE user hiển thị ĐÚNG mã màu đã chọn",
       note="Nguồn: Task nhỏ+ check Bug Kh r110-r114 (SpecChange #32577 / khối「Check các ô cho phép "
            "nhập mã màu」). Gộp các biến thể input vì CÙNG 1 kết quả mong đợi."),

    tc("Panel/Button — mã màu", "UI-INPUT-001", "Normal",
       "Nhập mã màu nhiều lần trước khi lưu → lưu theo mã CUỐI CÙNG",
       BTN + "\n- Đã chọn sub-type「カラーボタン」" + U1,
       "1. Nhập mã màu hợp lệ #111111\n2. Nhập tiếp mã hợp lệ khác #222222\n3. Bấm「保存」\n"
       "4. Vào edit kiểm tra mã màu\n5. Gửi cho U1 → quan sát màu trên LINE",
       "#111111 rồi #222222",
       "- 保存 thành công với mã màu ở BƯỚC 2 (#222222)\n"
       "- Màn edit và màu trên LINE đều là #222222",
       note="Nguồn: Task nhỏ+ check Bug Kh r115."),

    tc("Panel/Button — mã màu", "UI-INPUT-001", "Normal",
       "Edit mã màu nhiều lượt (vào detail → lưu → vào lại → lưu) → mỗi lượt lưu đúng",
       BTN + "\n- Đã có template button color TC1" + U1,
       "1. Vào màn detail TC1, nhập mã màu hợp lệ #333333 → 保存 → quan sát\n"
       "2. Vào lại màn detail, nhập mã màu hợp lệ khác #444444 → 保存 → quan sát\n"
       "3. Gửi cho U1 sau mỗi lần lưu → quan sát màu trên LINE",
       "#333333 rồi #444444",
       "- Lần 1: 保存 thành công với #333333, LINE hiện #333333\n"
       "- Lần 2: 保存 thành công với #444444, LINE hiện #444444",
       note="Nguồn: Task nhỏ+ check Bug Kh r116."),

    tc("Panel/Button — mã màu", "UI-INPUT-001", "Abnormal",
       "Mã màu SAI định dạng → chặn lưu, msg 入力されたカラーコードは正常なものではありません。カラーコードを再確認してください。",
       BTN + "\n- Đã chọn sub-type「カラーボタン」",
       "1. Nhập mã màu hợp lệ nhưng CÓ space đầu/cuối (「 #FFFFFF 」) → 保存 → quan sát\n"
       "2. Nhập > 6 ký tự (#FFFFFFF) → 保存 → quan sát\n3. Nhập < 6 ký tự (#FFF) → 保存 → quan sát\n"
       "4. Nhập không có dấu # ở đầu (FFFFFF) → 保存 → quan sát\n"
       "5. Nhập ký tự ngoài khoảng A-F (#08BZ5A) → 保存 → quan sát\n"
       "6. Nhập ký tự đặc biệt (#00000@) → 保存 → quan sát",
       "「 #FFFFFF 」· #FFFFFFF · #FFF · FFFFFF · #08BZ5A · #00000@",
       "- Cả 6 trường hợp KHÔNG lưu được\n"
       "- Hiện msg lỗi chính xác: 「入力されたカラーコードは正常なものではありません。"
       "カラーコードを再確認してください。」",
       note="Nguồn: Task nhỏ+ check Bug Kh r117-r121. Gộp 6 input vì CÙNG 1 msg lỗi."),

    tc("Panel/Button — mã màu", "UI-INPUT-001", "Abnormal",
       "Ô mã màu để RỖNG → báo lỗi カラーコードを入力してください",
       BTN + "\n- Đã chọn sub-type「カラーボタン」",
       "1. Xóa trắng ô mã màu → 保存\n2. Quan sát thông báo lỗi",
       "ô mã màu rỗng",
       "- KHÔNG lưu được\n- Hiện msg lỗi chính xác:「カラーコードを入力してください」",
       note="Nguồn: Task nhỏ+ check Bug Kh r122."),

    tc("Panel/Button — mã màu", "UI-FIELD-001", "Normal",
       "Toàn bộ ô nhập mã màu của sub-type カラーボタン và 画像 đều áp cùng bộ validate",
       BTN + U1,
       "1. Với sub-type「カラーボタン」, lặp bộ kiểm tra mã màu (hợp lệ + 6 dạng sai + rỗng) ở các ô: "
       "タイトル, 本文, ボタン編集 → màu nền nút (ボタン), ボタン編集 → màu chữ (テキスト)\n"
       "2. Với sub-type「画像」, lặp bộ kiểm tra ở các ô: ラベル → 背景, ラベル → テキスト, "
       "タイトル → 背景, タイトル → テキスト\n"
       "3. Kiểm tra thêm ở case nhiều nút, case nhiều panel, case edit nhiều lần, "
       "case edit title/text nút, case edit → 保存 → edit → 保存",
       "8 ô nhập mã màu × bộ input (hợp lệ / 6 dạng sai / rỗng); nhiều nút · nhiều panel · edit nhiều lần",
       "- Mọi ô đều áp CÙNG bộ validate: mã hợp lệ lưu OK và LINE hiện đúng màu; 6 dạng sai báo "
       "「入力されたカラーコードは正常なものではありません。カラーコードを再確認してください。」; "
       "rỗng báo「カラーコードを入力してください」\n"
       "- Không ô nào bỏ sót validate",
       note="Nguồn: Task nhỏ+ check Bug Kh r123-r223 (ma trận 8 ô × bộ input, kết quả giống nhau). "
            "Gộp vì CÙNG 1 kết quả mong đợi cho mỗi loại input; danh sách ô liệt kê đủ ở cột Các bước."),

    tc("Panel/Button — mã màu", "REG-SHARED-001", "Normal",
       "Ô nhập mã màu ở màn QR landing và Form-Answer áp cùng bộ validate (triển khai ngang)",
       "- Đăng nhập admin bot A\n- Có 1 QR landing và 1 form đã tạo",
       "1. Màn QR landing → tab「オプション設定」→ ô「QRコードカラー」: lặp bộ kiểm tra mã màu\n"
       "2. Màn Form-Answer → tab「共通デザイン設定」: lặp bộ kiểm tra ở toàn bộ ô mã màu\n"
       "3. Màn Form-Answer → tab「フォーム編集」và tab「各種設定」: lặp bộ kiểm tra\n"
       "4. Kiểm tra các hiệu ứng khác của 2 màn sau khi đổi màu",
       "bộ input mã màu (hợp lệ / 6 dạng sai / rỗng) áp cho ô màu của 2 màn khác",
       "- Cả 2 màn áp CÙNG bộ validate và CÙNG nội dung msg lỗi như màn template\n"
       "- Đổi màu thành công thì màu hiển thị đúng ở trang public tương ứng",
       note="Nguồn: Task nhỏ+ check Bug Kh r224-r478 (khối triển khai ngang QR landing + Form-Answer). "
            "⚠ Phần chi tiết của 2 màn này thuộc FA-009 QR Landing và FA-011 Form — ở đây chỉ giữ 1 TC "
            "regression, xem `excluded` của feature."),

    # ═════════════ 24. Panel/Button — LINE URL scheme ═════════════
    tc("Panel/Button — LINE URL scheme", "FUNC-001", "Abnormal",
       "Chọn LINE URL scheme → 2 loại action còn lại KHÔNG được thực thi",
       STD + U1,
       "1. Set nút có CẢ multi action + friend action + LINE URL scheme → 保存\n2. Gửi cho U1\n"
       "3. U1 bấm nút → quan sát hành vi và các action nhận được",
       "nút có 3 loại action, trong đó có LINE URL scheme",
       "- Chỉ LINE URL scheme được thực thi\n- Multi action và friend action KHÔNG được thực thi",
       note="Nguồn: Type ảnh r93, r131 (「khi chọn setting này thì 2 action phía trên sẽ ko thực hiện」) "
            "— cùng cơ chế cho button và image map. ⚠ TC gốc r131 note「chưa apply logic 3」→ xem MT-31."),

    tc("Panel/Button — LINE URL scheme", "INTG-LINE-001", "Normal",
       "LINE URL scheme「友だちにLINE公式アカウントをシェアする」→ mở màn share hồ sơ Bot",
       STD + U1,
       "1. Set nút = LINE URL scheme「友だちにLINE公式アカウントをシェアする」→ 保存\n2. Gửi cho U1\n"
       "3. U1 bấm nút trên LINE\n4. Chọn 1 người bạn và share",
       "LINE ID của bot A",
       "- Mở link https://line.me/R/nv/recommendOA/{Percent-encoded LINE ID}\n"
       "- Phía user hiện màn share LINE ID của bot\n- Chọn 1 người bạn và share → người đó nhận được "
       "hồ sơ của Bot",
       note="Nguồn: Template button r196 + Type ảnh r94, r132."),

    tc("Panel/Button — LINE URL scheme", "INTG-LINE-001", "Normal",
       "LINE URL scheme「友だちにテキストをシェアする」→ mở màn share text đã setting",
       STD + U1,
       "1. Set nút = LINE URL scheme「友だちにテキストをシェアする」, nhập text share → 保存\n"
       "2. Gửi cho U1\n3. U1 bấm nút → chọn 1 người bạn và share\n4. Kiểm tra tin người bạn nhận được",
       "text share =「おすすめです」",
       "- Mở link https://line.me/R/share?text={text_message}\n"
       "- Phía user hiện màn share; chọn 1 người bạn và share → người đó nhận đúng text đã setting",
       note="Nguồn: Template button r197 + Type ảnh r95, r133. ⚠ TC gốc r197 note「message text chỗ "
            "dấu cách lại thành dấu +」→ lỗi encode dấu cách, xem MT-32."),

    tc("Panel/Button — LINE URL scheme", "INTG-LINE-001", "Normal",
       "LINE URL scheme mở camera / camera roll / share location → mở đúng màn và gửi lại được cho bot",
       STD + U1,
       "1. Set nút = 「カメラを起動させる」→ 保存 → gửi → U1 bấm nút → chụp ảnh và gửi lại\n"
       "2. Set nút = 「カメラロールを開かせる」→ gửi → U1 bấm nút → chọn ảnh và gửi lại\n"
       "3. Set nút = 「位置情報を送らせる」→ gửi → U1 bấm nút → chọn vị trí và share lại",
       "3 loại scheme",
       "- 「カメラを起動させる」: mở https://line.me/R/nv/camera/ → camera mở, chụp ảnh gửi lại được cho bot\n"
       "- 「カメラロールを開かせる」: mở https://line.me/R/nv/cameraRoll/multi → chọn ảnh gửi lại được\n"
       "- 「位置情報を送らせる」: mở https://line.me/R/nv/location/ → chia sẻ vị trí lại được cho bot\n"
       "- Nội dung user gửi lại xuất hiện ở chat 1:1 của bot",
       note="Nguồn: Template button r198-r200 + Type ảnh r96-r98, r134-r136."),

    tc("Panel/Button — LINE URL scheme", "INTG-LINE-001", "Normal",
       "LINE URL scheme「カスタム（上級者向け）」→ nhập URL scheme tự do và mở đúng",
       BTN + "\n- Đã chọn sub-type「カラーボタン」" + U1,
       "1. Set nút = 「カスタム（上級者向け）」→ nhập 1 LINE URL scheme hợp lệ → 保存\n"
       "2. Gửi cho U1 → U1 bấm nút → quan sát hành vi",
       "URL scheme tự nhập",
       "- Lưu thành công\n- U1 bấm nút → LINE mở đúng theo scheme đã nhập",
       note="Nguồn: Template button r349-r352."),

    tc("Panel/Button — LINE URL scheme", "UI-INPUT-001", "Boundary",
       "「友だちにテキストをシェアする」: bộ đếm URL-encode 900, count JP=9 · latinh=1 · space/ký tự đặc biệt=3 · emoji=12",
       STD,
       "1. Nhập 1 ký tự latinh vào ô text share → quan sát bộ đếm\n"
       "2. Nhập 1 ký tự Nhật → quan sát bộ đếm\n3. Nhập 1 dấu space và 1 ký tự đặc biệt → quan sát\n"
       "4. Nhập 1 emoji → quan sát\n5. Nhập cho tới 899 rồi 900 đơn vị → quan sát bộ đếm và 保存\n"
       "6. Nhập vượt 900 → quan sát",
       "1 latinh / 1 JP / 1 space / 1 ký tự đặc biệt / 1 emoji; mốc 899 và 900",
       "- Bộ đếm: latinh = 1, text Nhật = 9, space và ký tự đặc biệt = 3, emoji = 12 đơn vị\n"
       "- 899 đơn vị: cho nhập, hiện 899/900\n- 900 đơn vị: cho nhập, hiện 900/900 và 保存 thành công\n"
       "- Vượt 900: bị chặn",
       note="Nguồn: Task nhỏ+ check Bug Kh r614-r618, r664 (SpecImprove #33326, 29/08/2025 — đổi giới "
            "hạn từ 80 lên 800 ký tự, bộ đếm hiển thị theo URL-encode /900). Spec KHÔNG ghi rule này "
            "→ xem MT-12."),

    tc("Panel/Button — LINE URL scheme", "REG-SHARED-001", "Normal",
       "Bộ đếm 900 áp cho cả 4 sub-type button, image map (2 kiểu area) và 3 màn tạo template khác",
       ADM + U1,
       "1. Lặp bộ kiểm tra bộ đếm ở sub-type スタンダード / カラーボタン / 画像 / クイックリプライ "
       "(cả tạo mới và edit)\n"
       "2. Lặp ở template image map: loại area「手動で設定する」và「テンプレートから選ぶ」(tạo mới và edit)\n"
       "3. Lặp ở màn tạo template button standard trong BROADCAST\n"
       "4. Lặp ở màn tạo template button color trong SCENARIO\n5. Lặp ở màn tạo template image map trong REMIND\n"
       "6. Với mỗi trường hợp: nhập text valid → 保存 → gửi cho U1 → bấm nút/vùng ảnh → kiểm tra text share",
       "4 sub-type button + 2 kiểu area image map + 3 màn khác; tạo mới và edit",
       "- Mọi điểm đều đếm đúng theo quy tắc URL-encode (JP=9, latinh=1, space/đặc biệt=3, emoji=12)\n"
       "- Lưu action thành công; phía LINE friend bấm vào thực hiện action với ĐÚNG text đã nhập",
       note="Nguồn: Task nhỏ+ check Bug Kh r616-r696. Gộp vì CÙNG 1 kết quả mong đợi."),

    # ═════════════ 25. Panel/Button — 詳細設定 & tap limit ═════════════
    tc("Panel/Button — 詳細設定 & tap limit", "FUNC-001", "Normal",
       "Tap limit: default là 無制限; 4 lựa chọn lưu vào carousel_action_type = 1/2/3/0",
       STD,
       "1. Tạo nút mới → mở tab「詳細設定」→ quan sát lựa chọn tap limit mặc định\n"
       "2. Chọn loại 1 (toàn bộ nút của all panel chỉ action 1 lần) → 保存 → kiểm tra "
       "`template.carousel_action_type`\n"
       "3. Chọn loại 2 (mỗi panel 1 nút 1 lần) → 保存 → kiểm tra cột\n"
       "4. Chọn loại 3 (mỗi nút action 1 lần) → 保存 → kiểm tra cột\n"
       "5. Chọn loại 4「無制限」→ 保存 → kiểm tra cột",
       "4 lựa chọn tap limit",
       "- Mặc định khi tạo nút mới là action NHIỀU LẦN「無制限」\n"
       "- `template.carousel_action_type`: loại 1 → 1, loại 2 → 2, loại 3 → 3, loại 4「無制限」→ 0",
       note="Nguồn: Template button r170-r176. ⚠ MÂU THUẪN spec: spec Field Matrix #19 và "
            "db-mapping.md:520 map「選択肢のタップ回数」vào `template.answer_type` (3 giá trị 0/1/2), "
            "trong khi TC ghi `carousel_action_type` (4 giá trị) → xem MT-33 (đồng thời lấp Gap #1 của spec)."),

    tc("Panel/Button — 詳細設定 & tap limit", "COMPAT-LEGACY-001", "Normal",
       "Template button CŨ → suy ra loại tap limit theo carousel_action_type đang lưu",
       ADM + "\n- Có template button cũ với `carousel_action_type` = 0 và 1 template khác = 1",
       "1. Mở edit template cũ có `carousel_action_type` = 0 → quan sát lựa chọn tap limit\n"
       "2. Mở edit template cũ có `carousel_action_type` = 1 → quan sát lựa chọn tap limit",
       "template cũ với `carousel_action_type` = 0 và 1",
       "- `carousel_action_type` = 0 → hiện loại 4「無制限」\n- `carousel_action_type` = 1 → hiện loại 1",
       note="Nguồn: Template button r175-r176."),

    tc("Panel/Button — 詳細設定 & tap limit", "MSG-004", "Normal",
       "Toggle「設定タップ数を超えた時の送信メッセージ」: 送信しない / default / message tự set",
       STD + U1,
       "1. Set tap limit loại 1, toggle「送信しない」→ 保存 → gửi cho U1 → bấm nút 2 lần → quan sát\n"
       "2. Đổi toggle sang「送信する」, KHÔNG nhập message → 保存 → gửi → bấm 2 lần → quan sát\n"
       "3. Nhập message tự set → 保存 → gửi → bấm 2 lần → quan sát",
       "3 cấu hình: không gửi / gửi msg default / gửi msg tự set",
       "- 「送信しない」: bấm quá số lần → hệ thống KHÔNG làm gì, không gửi tin\n"
       "- 「送信する」không nhập message: gửi message DEFAULT「タップ回数上限に達しています」\n"
       "- Có nhập message: gửi ĐÚNG message đã setting",
       note="Nguồn: Template button r177-r179. Spec Field Matrix #20-#21 khớp về default message."),

    tc("Panel/Button — 詳細設定 & tap limit", "UI-INPUT-001", "Boundary",
       "Message khi vượt tap: max 400 ký tự; hỗ trợ text Nhật, {name}, icon, friend info, ký tự đặc biệt, xuống dòng",
       STD + U1,
       "1. Nhập message 400 ký tự → 保存 → quan sát\n2. Nhập 401 ký tự → 保存 → quan sát\n"
       "3. Nhập message có: text Nhật, {name}, icon emoji, code friend info, ký tự đặc biệt, xuống dòng "
       "→ 保存 → gửi cho U1 → bấm nút quá số lần → quan sát tin nhận được",
       "400 / 401 ký tự; 6 loại nội dung",
       "- 400 ký tự: lưu thành công; 401 ký tự: bị chặn\n"
       "- Tin vượt tap nhận được replace đúng {name} và friend info, hiện đúng emoji, ký tự đặc biệt "
       "và ngắt dòng",
       note="Nguồn: Template button r181, r187. Khớp spec ui-spec.md:322 (max 400)."),

    tc("Panel/Button — 詳細設定 & tap limit", "FUNC-001", "Normal",
       "Elme action khi vượt tap (action_id_when_exceed_click) → được thực thi khi user bấm quá số lần",
       STD + U1,
       "1. Set tap limit loại 1, toggle「送信する」và chọn Elme action = gắn tag T → 保存\n"
       "2. Gửi cho U1 → U1 bấm nút lần 1 → quan sát\n3. U1 bấm nút lần 2 → quan sát tag của U1",
       "Elme action khi vượt tap = gắn tag T",
       "- Lần 1: action bình thường của nút chạy, KHÔNG gắn tag T\n"
       "- Lần 2 (vượt tap): U1 được gắn tag T và nhận message vượt tap",
       note="Nguồn: Template button r181 + spec Field Matrix #22 (`action_id_when_exceed_click`)."),

    tc("Panel/Button — 詳細設定 & tap limit", "MSG-004", "Normal",
       "PC display text (パソコン版・通知欄の表示テキスト): default và giá trị tự nhập hiện đúng trên PC / thông báo",
       STD + U1,
       "1. Mở tab「詳細設定」, để trống ô PC display text → 保存 → gửi cho U1\n"
       "2. Quan sát text hiển thị ở LINE bản PC và ở khung thông báo (notification)\n"
       "3. Nhập text tự set 400 ký tự → 保存 → gửi → quan sát\n4. Nhập 401 ký tự → 保存 → quan sát",
       "để trống / 400 ký tự / 401 ký tự",
       "- Để trống: LINE PC và thông báo hiện text DEFAULT「メッセージをご確認ください」\n"
       "- Có nhập: hiện đúng text đã nhập\n- 400 ký tự lưu OK, 401 ký tự bị chặn",
       note="Nguồn: Template button r181-r187 + spec Field Matrix #23. ⚠ Spec tự đánh dấu [Thấp] cho "
            "cột DB của field này; các loại media/introduce lại có default KHÁC → xem MT-34."),

    # ═════════════ 26. Panel/Button — action phía LINE user ═════════════
    tc("Panel/Button — action phía LINE user", "FUNC-MULTI-001", "Normal",
       "User bấm nút chỉ có multi action → nhận đủ action đã set (có postback)",
       STD + U1 + "\n- Nút 1 đã set 2 multi action: gắn tag T + gửi template TX",
       "1. Gửi template cho U1\n2. U1 bấm nút 1 trên LINE\n3. Quan sát tag của U1 và tin nhận được\n"
       "4. Kiểm tra bản ghi `user_button`",
       "2 multi action",
       "- U1 được gắn tag T và nhận tin của template TX\n"
       "- Có postback ghi nhận lần bấm (bản ghi `user_button` được tạo)",
       note="Nguồn: Template button r193."),

    tc("Panel/Button — action phía LINE user", "FUNC-001", "Normal",
       "User bấm nút chỉ có friend action → mở đúng đích theo từng loại (URL, form, item, event, conversion, tel, mail, LINE ID, text)",
       STD + U1,
       "1. Set nút = friend action mở URL → gửi → U1 bấm → quan sát\n"
       "2. Lần lượt đổi sang: mở form, mở item (link mua / link đổi thẻ / link hủy), mở booking event, "
       "mở link conversion, gọi số điện thoại, gửi mail, mở LINE ID, gửi text\n"
       "3. Với mỗi loại: gửi lại template và cho U1 bấm nút, quan sát hành vi trên LINE",
       "9 loại friend action",
       "- Mỗi loại mở đúng đích tương ứng: trang web / trang form / trang mua-đổi thẻ-hủy của item / "
       "trang booking event / link conversion / màn gọi điện / màn soạn mail / hồ sơ LINE / "
       "text được điền vào khung gửi",
       note="Nguồn: Template button r194."),

    tc("Panel/Button — action phía LINE user", "FUNC-MULTI-001", "Normal",
       "Nút set CẢ multi action và friend action → mở được link friend action ĐỒNG THỜI nhận multi action",
       STD + U1 + "\n- Nút 1 set friend action mở URL + 2 multi action (gắn tag + gửi template)",
       "1. Gửi template cho U1\n2. U1 bấm nút 1\n3. Quan sát trang mở ra và các action nhận được",
       "friend action mở URL + 2 multi action",
       "- Trang URL mở ra đúng\n- ĐỒNG THỜI U1 nhận đủ multi action (được gắn tag và nhận template)",
       note="Nguồn: Template button r195."),

    tc("Panel/Button — action phía LINE user", "FUNC-001", "Normal",
       "Tap limit loại 1 (toàn bộ nút của mọi panel chỉ 1 lần) → nút thứ 2 bấm không có action",
       STD + U1 + "\n- Template có 2 panel, mỗi panel 2 nút, tất cả nút đều có action\n"
                  "- Tap limit = loại 1, toggle gửi message vượt tap = 送信する (msg default)",
       "1. Gửi template cho U1\n2. U1 bấm 1 nút bất kỳ → quan sát action\n"
       "3. U1 bấm nút khác (cùng panel) → quan sát\n4. U1 bấm nút ở panel khác → quan sát",
       "2 panel × 2 nút; tap limit loại 1",
       "- Lần bấm ĐẦU TIÊN: action chạy bình thường\n"
       "- Mọi lần bấm sau (kể cả nút khác, panel khác): KHÔNG action, chỉ nhận message vượt tap\n"
       "- Không set message → gửi「タップ回数上限に達しています」; có set → gửi message đã set",
       note="Nguồn: Template button r201-r204, r419-r421."),

    tc("Panel/Button — action phía LINE user", "FUNC-001", "Normal",
       "Tap limit loại 2 (mỗi panel 1 nút 1 lần) → hết lượt của panel này vẫn action được ở panel khác",
       STD + U1 + "\n- Template có 2 panel, mỗi panel 2 nút; tap limit = loại 2",
       "1. Gửi template cho U1\n2. U1 bấm nút A của panel 1 → quan sát action\n"
       "3. U1 bấm nút B của panel 1 → quan sát\n4. U1 bấm nút C của panel 2 → quan sát",
       "2 panel × 2 nút; tap limit loại 2",
       "- Bấm nút A (panel 1): action chạy\n"
       "- Bấm nút B (cùng panel 1): KHÔNG action, nhận message vượt tap\n"
       "- Bấm nút C (panel 2 — chưa dùng lượt): action CHẠY tiếp",
       note="Nguồn: Template button r205-r208, r422-r425."),

    tc("Panel/Button — action phía LINE user", "FUNC-001", "Normal",
       "Tap limit loại 3 (mỗi nút action 1 lần) → mỗi nút riêng biệt có 1 lượt",
       STD + U1 + "\n- Template có 2 panel, mỗi panel 2 nút; tap limit = loại 3",
       "1. Gửi template cho U1\n2. U1 bấm nút A → quan sát\n3. U1 bấm lại nút A → quan sát\n"
       "4. U1 bấm nút B (chưa từng bấm) → quan sát",
       "2 panel × 2 nút; tap limit loại 3",
       "- Bấm nút A lần đầu: action chạy\n- Bấm lại nút A: KHÔNG action, nhận message vượt tap\n"
       "- Bấm nút B (chưa từng bấm): action CHẠY",
       note="Nguồn: Template button r209-r212, r426-r429."),

    tc("Panel/Button — action phía LINE user", "FUNC-001", "Normal",
       "Tap limit loại 4 (無制限) → mỗi lần bấm đều có action",
       STD + U1 + "\n- Template 1 panel, 2 nút; tap limit = loại 4「無制限」",
       "1. Gửi template cho U1\n2. U1 bấm nút A 3 lần liên tiếp → đếm action nhận được\n"
       "3. U1 bấm nút B 2 lần → đếm action",
       "tap limit loại 4; bấm nhiều lần",
       "- Mỗi lần bấm (cả nút A và B) đều gửi action cho user, không có giới hạn",
       note="Nguồn: Template button r213, r430."),

    tc("Panel/Button — action phía LINE user", "STATE-001", "Normal",
       "Gửi LẠI cùng template → lượt tap limit được tính lại từ đầu",
       STD + U1 + "\n- Template tap limit = loại 1, đã gửi cho U1 và U1 đã dùng hết lượt",
       "1. Xác nhận U1 bấm nút không còn action (đã hết lượt)\n2. Gửi LẠI template đó cho U1\n"
       "3. U1 bấm nút ở tin nhắn MỚI → quan sát action\n4. U1 bấm nút ở tin nhắn CŨ → quan sát",
       "gửi lại template lần 2",
       "- Bấm nút ở tin MỚI: action CHẠY (lượt tính lại từ đầu — action ăn theo message)\n"
       "- Bấm nút ở tin CŨ: vẫn hết lượt, không action",
       note="Nguồn: Template button r214, r431 (「Action sẽ ăn theo message nên mỗi khi gửi lại "
            "message sẽ tính action từ đầu」)."),

    tc("Panel/Button — action phía LINE user", "MSG-001", "Normal",
       "Gửi template button qua 4 sub-type × web/job → LINE user nhận đúng, bấm nút ra đúng action",
       ADM + U1,
       "1. Với mỗi sub-type (standard / color / image / quick reply): gửi qua web (send test, chat 1:1)\n"
       "2. Gửi qua job (broadcast, scenario step, remind)\n"
       "3. Với mỗi lượt: quan sát tin trên LINE và bấm nút để kiểm tra action",
       "4 sub-type × 5 đường gửi",
       "- Mọi lượt gửi: LINE user nhận đúng panel/ảnh/title/nội dung/nút của từng sub-type\n"
       "- Bấm nút thực hiện đúng action đã set",
       note="Nguồn: Template button r188-r192, r405-r409, r648-r697, r886-r899. Gộp vì CÙNG 1 kết quả."),

    tc("Panel/Button — action phía LINE user", "MSG-004", "Normal",
       "Send template button ở màn send all: standard và color → nội dung và action đúng phía user",
       ADM + "\n- Đang ở màn broadcast (send all)" + U1,
       "1. Tại màn send all, tạo mới template button standard → cấu hình panel + nút + action → lưu\n"
       "2. Gửi broadcast cho U1 → quan sát tin trên LINE → bấm nút\n"
       "3. Lặp lại với template button color\n4. Kiểm tra cột `template.category_id` của template vừa tạo",
       "2 sub-type tạo tại màn send all",
       "- Tin trên LINE hiện đúng panel/nút của từng sub-type; bấm nút ra đúng action\n"
       "- Template tạo tại màn send all có `category_id` = -11 (nội bộ broadcast)",
       note="Nguồn: Template button r1210-r1262 + Template type text r201 (category = -11)."),

    # ═════════════ 27. Button ảnh — label & title ═════════════
    tc("Button ảnh — label & title", "UI-INPUT-001", "Normal",
       "Sub-type 画像: tạo được từ 1 đến 10 panel, mỗi panel có ảnh riêng",
       BTN + "\n- Đã chọn sub-type「画像」" + U1,
       "1. Tạo template 1 panel có ảnh → 保存 → gửi → quan sát\n"
       "2. Lần lượt tăng số panel: 2, 3, 4, 5, 6, 7, 8, 9, 10 panel; mỗi panel set 1 ảnh → 保存 → gửi\n"
       "3. Với mỗi số panel, quan sát tin trên LINE",
       "template có 1 → 10 panel",
       "- Mọi số panel từ 1 đến 10 đều lưu và gửi thành công\n"
       "- Tin trên LINE hiện đủ số panel với đúng ảnh từng panel (dạng carousel)",
       note="Nguồn: Template button r434-r444."),

    tc("Button ảnh — label & title", "UI-INPUT-001", "Normal",
       "Label ラベル và Title タイトル của button ảnh: nhập giá trị hợp lệ → lưu và hiển thị đúng",
       BTN + "\n- Đã chọn sub-type「画像」" + U1,
       "1. Nhập ラベル hợp lệ → quan sát preview → 保存 → gửi cho U1 → quan sát tin\n"
       "2. Nhập タイトル hợp lệ → quan sát preview → 保存 → gửi → quan sát\n"
       "3. Thử với text Nhật, latinh, emoji và xuống dòng",
       "ラベル và タイトル với 4 dạng nội dung",
       "- Preview hiện đúng ラベル và タイトル đã nhập\n"
       "- Tin trên LINE hiện đúng nội dung, đúng emoji và ngắt dòng",
       note="Nguồn: Template button r454-r469."),

    tc("Button ảnh — label & title", "UI-INPUT-001", "Abnormal",
       "Validate ラベル và タイトル của button ảnh → chặn khi vượt giới hạn hoặc bỏ trống trường bắt buộc",
       BTN + "\n- Đã chọn sub-type「画像」",
       "1. Bỏ trống ラベル → 保存 → quan sát\n2. Nhập ラベル vượt giới hạn ký tự → 保存 → quan sát\n"
       "3. Bỏ trống タイトル → 保存 → quan sát\n4. Nhập タイトル vượt giới hạn → 保存 → quan sát\n"
       "5. Tick chọn KHÔNG dùng ラベル và タイトル → 保存 → quan sát",
       "rỗng / vượt giới hạn / tick không dùng",
       "- Vượt giới hạn ký tự: báo lỗi và KHÔNG lưu\n"
       "- Tick chọn không dùng ラベル/タイトル: lưu thành công, tin trên LINE không hiện 2 phần này",
       note="Nguồn: Template button r602-r617. ⚠ TC gốc KHÔNG ghi con số giới hạn cụ thể và nguyên văn "
            "msg lỗi cho ラベル/タイトル của button ảnh; spec cũng không ghi → cần Leader xác nhận, xem MT-35."),

    tc("Button ảnh — label & title", "FUNC-001", "Normal",
       "Setting action của button ảnh: set 1 trong 3 loại hoặc nhiều loại → đều lưu được",
       BTN + "\n- Đã chọn sub-type「画像」",
       "1. Không set action nào → 保存 → quan sát\n2. Set 1 trong 3 loại action, 2 loại còn lại để trống "
       "→ 保存 → quan sát\n3. Set cùng lúc nhiều loại action → 保存 → quan sát",
       "3 tổ hợp action",
       "- Cả 3 tổ hợp đều lưu thành công, không báo lỗi",
       note="Nguồn: Template button r618-r620."),

    tc("Button ảnh — label & title", "MSG-004", "Normal",
       "Setting メッセージタイトル của button ảnh lưu vào template.content và hiện đúng phía user",
       BTN + "\n- Đã chọn sub-type「画像」" + U1,
       "1. Nhập メッセージタイトル → 保存 → kiểm tra cột `template.content`\n"
       "2. Gửi cho U1 → quan sát text hiển thị trên LINE PC và khung thông báo\n"
       "3. Bỏ trống メッセージタイトル → 保存 → gửi → quan sát",
       "có nhập / bỏ trống メッセージタイトル",
       "- Có nhập: `template.content` lưu đúng giá trị; LINE PC và thông báo hiện đúng text\n"
       "- Bỏ trống: hiện text default của hệ thống",
       note="Nguồn: Template button r621-r625."),

    tc("Button ảnh — label & title", "MEDIA-IMG-001", "Normal",
       "Setting パネルサイズ (kích thước ảnh khi gửi) → LINE hiện đúng kích thước đã chọn",
       BTN + "\n- Đã chọn sub-type「画像」" + U1,
       "1. Mở phần setting パネルサイズ → quan sát các lựa chọn và giá trị default\n"
       "2. Chọn từng kích thước → 保存 → gửi cho U1 → quan sát kích thước ảnh trên LINE",
       "các lựa chọn パネルサイズ",
       "- Tin trên LINE hiện ảnh panel theo ĐÚNG kích thước đã chọn ở mỗi lượt",
       note="Nguồn: Template button r626-r628. ⚠ TC gốc chỉ có tiêu đề, KHÔNG có Expect Result → "
            "kết quả mong đợi ở đây là SUY LUẬN CỦA AI, cần Leader xác nhận danh sách lựa chọn thật."),

    tc("Button ảnh — label & title", "FUNC-001", "Normal",
       "Button ảnh: tap limit 選択肢のタップ回数 và message vượt tap hoạt động như sub-type khác",
       BTN + "\n- Đã chọn sub-type「画像」" + U1,
       "1. Set tap limit từng loại (1/2/3/4) → 保存 → gửi → bấm vùng ảnh nhiều lần → quan sát action\n"
       "2. Set 設定タップ数を超えた時の送信メッセージ (không nhập / có nhập) → gửi → bấm quá số lần → quan sát",
       "4 loại tap limit; message vượt tap default và tự set",
       "- Hành vi tap limit giống sub-type standard: đúng phạm vi giới hạn của từng loại\n"
       "- Vượt tap: nhận message default「タップ回数上限に達しています」hoặc message đã set",
       note="Nguồn: Template button r629-r638."),

    tc("Button ảnh — label & title", "REG-SHARED-001", "Normal",
       "Tạo button ảnh ở màn scenario / send all / remind: tạo mới, clone, get thẳng → gửi và action đúng",
       ADM + U1,
       "1. Ở màn scenario: tạo mới template button ảnh trong step → 保存 → gửi → bấm vùng ảnh\n"
       "2. Ở màn scenario: clone từ template có sẵn rồi edit → gửi → bấm\n"
       "3. Ở màn scenario: get thẳng template từ thư viện → gửi → bấm\n"
       "4. Lặp lại 3 cách ở màn send all và màn remind\n5. Lặp lại với template dạng CŨ (clone và get thẳng)",
       "3 cách gắn × 3 màn; thêm template dạng cũ",
       "- Mọi tổ hợp: gửi được tin, tin trên LINE hiện đúng ảnh/label/title\n"
       "- Bấm vùng ảnh thực hiện đúng action đã set",
       note="Nguồn: Template button r754-r806. Gộp vì CÙNG 1 kết quả mong đợi."),

    tc("Button ảnh — label & title", "FUNC-001", "Normal",
       "Copy template button ảnh và copy group chứa button ảnh (1 panel / nhiều panel / nhiều loại) → dữ liệu đầy đủ",
       ADM + U1,
       "1. Copy 1 template button ảnh đơn → mở bản copy đối chiếu ảnh/label/title/action\n"
       "2. Copy group có 1 template button ảnh và 1 panel → đối chiếu\n"
       "3. Copy group có 1 template button ảnh và nhiều panel → đối chiếu\n"
       "4. Copy group có nhiều template button ảnh → đối chiếu\n"
       "5. Copy group có nhiều template khác loại → đối chiếu\n6. Gửi từng bản copy cho U1 → bấm vùng ảnh",
       "5 kịch bản copy",
       "- Mọi bản copy có đủ ảnh, label, title, action giống bản gốc\n"
       "- Gửi được và bấm vùng ảnh ra đúng action\n- Sửa bản copy KHÔNG ảnh hưởng bản gốc",
       note="Nguồn: Template button r736-r746."),

    tc("Button ảnh — label & title", "REG-URL-001", "Normal",
       "Button ảnh: access link của action → mở đúng đích, kể cả khi mở lại nhiều lần",
       BTN + "\n- Đã chọn sub-type「画像」, đã set action mở URL" + U1,
       "1. Gửi cho U1 → U1 bấm vùng ảnh → quan sát trang mở ra\n2. U1 back rồi bấm lại → quan sát\n"
       "3. Kiểm tra action nhận được ở mỗi lần",
       "action mở URL, bấm nhiều lần",
       "- Lần đầu mở đúng trang đích\n- Bấm lại: hành vi đúng theo setting tap limit đang áp",
       note="Nguồn: Template button r807-r809."),
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
for _r in S4:
    _mts = set(_re.findall(r"MT-\d+", _r["note"]))
    if _mts & _SPEC_SILENT_MT or _AI_INFER in _r["note"]:
        _r["spec"] = "Spec không ghi"
