# -*- coding: utf-8 -*-
"""FA-010 テンプレート (Mẫu tin nhắn) — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: 02. TCsLine_Template (16 tab) + TCsLine_Improve chung (tab「Improve template btn + image map」).
Nguồn spec: spec-features/admin/message-template/ (feature-spec.md · ui/ui-spec.md ·
            web/logic-spec.md · web/api-spec.md · db/db-mapping.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "Giới hạn ký tự TÊN FOLDER template: 15 hay 20?",
     "「Improve list template」r16「Nhập từ 1-15 ký tự」· r26「Nhập lớn hơn 15 ký tự」→ Expect: "
     "「フォルダ名は15文字以内で入力してください。」· r63 và r74 (đổi tên folder) cũng dùng mốc 15.\n"
     "Msg lỗi trong TC ghi rõ con số **15**.",
     "`ui-spec.md:140`「フォルダ名」Textbox — **Max 20 ký tự (hiển thị 0/20)**.\n"
     "`feature-spec.md:278` SCR-TMT-03 — 1 field tên folder (**max 20 ký tự**).\n"
     "`feature-spec.md:619` Field Matrix #7 —「Max 20 ký tự (UI), varchar(100) DB」.\n"
     "`db-mapping.md:471` —「Max 20 ký tự (validate UI, DB cho 100)」.",
     "Lệch 5 ký tự ở validate mà người dùng cuối gặp trực tiếp. Nếu member chạy theo spec (20) thì "
     "TC biên sẽ FAIL oan; nếu chạy theo TC (15) mà code đã đổi lên 20 thì bỏ lọt việc spec/UI không "
     "đồng bộ. Msg lỗi hard-code con số nên nhìn thấy ngay được bên nào đúng.",
     "『Folder template』TC「Tên folder > 15 ký tự → chặn lưu...」· TC「Tên folder đúng 15 ký tự...」· "
     "TC「Đổi tên folder > 15 ký tự...」",
     "",
     "① Mở màn /basic/message-template trên staging, nhập 16 ký tự và đọc nguyên văn msg lỗi.\n"
     "② Nếu code = 15: sửa `ui-spec.md:140`, `feature-spec.md:278`, `feature-spec.md:619`, "
     "`db-mapping.md:471` về 15.\n"
     "③ Nếu code = 20: sửa expected của 3 TC + msg lỗi, và ghi chú TC gốc sheet r16/r26/r63/r74 đã cũ."],

    ["MT-02", "CAO", W,
     "Search template: tìm trong FOLDER đang chọn hay trên TOÀN BỘ folder?",
     "「Task nhỏ+ check Bug Kh」r3 ghi rõ:「mh template: textbox search hiện tại chỉ search trong folder "
     "đang chọn — **expect: search all folder**」· r6 và r9「click vào kết quả search → ra list template "
     "con của template cha tương ứng」(tức kết quả có thể thuộc folder khác).\n"
     "「Improve list template」r179「search all folder, khi hiển thị kq đóng menu folder」.",
     "`logic-spec.md:141` — `searchByKeyWord($group_id, $keyword)`「Tìm template theo tên **trong "
     "folder**, join category...」.\n"
     "`feature-spec.md:198-206` Luồng 2 (Tìm kiếm) — request `{ action: \"searchByKeyWord\", keyword, "
     "group_id }`, DB query `WHERE name LIKE '%keyword%' AND bot_id AND **category_id**`.",
     "Đây là hành vi người dùng cuối nhìn thấy trực tiếp: nếu chỉ search trong folder thì user không "
     "tìm được template ở folder khác. Spec mô tả luồng CŨ (theo `group_id`), TC yêu cầu luồng MỚI "
     "(all folder). Không rõ code hiện tại đã đổi chưa.",
     "『Sort & search template』TC「Search theo 管理名 → tìm được trên TOÀN BỘ folder...」· "
     "TC「Click vào kết quả search → mở đúng list template con...」",
     "",
     "① Test trên staging: đứng ở folder A, search tên template thuộc folder B.\n"
     "② Nếu đã search all folder: cập nhật `logic-spec.md:141` và Luồng 2 của `feature-spec.md` "
     "(bỏ điều kiện `category_id`).\n"
     "③ Nếu vẫn search trong folder: đây là yêu cầu CHƯA làm → raise ticket và ghi vào TC là dự kiến FAIL."],

    ["MT-03", "CAO", W,
     "Giới hạn タイトル / 本文 của panel: 20/40 hay 40/60?",
     "**Khối CŨ** — 「Template button」r53-r55: title「nhập > 20 ký tự → báo lỗi "
     "タイトルは20文字以内で入力してください。」· r70-r72: content「nhập > 40 ký tự → báo lỗi "
     "本文は40文字以内で入力してください。」\n"
     "**Khối MỚI** — 「Improve tạo temp」r2 (SpecChange #24890, 28/12/2023):「Title và Description chuyển "
     "thành 40/60 ký tự. Hiện tại: title và description đang giới hạn 20/40 ⇒ sửa thành 40/60」, r11-r18 "
     "test theo mốc 40 và 60.",
     "`ui-spec.md:259-260`「タイトル」Max **40** ký tự (0/40) ·「本文」Max **60** ký tự (0/60), bắt buộc.\n"
     "`feature-spec.md:375` — tiêu đề (max 40), nội dung (max 60, bắt buộc).\n"
     "`feature-spec.md:627-628` Field Matrix #15/#16 — 40 và 60.",
     "2 khối TC trong CÙNG 1 file mâu thuẫn nhau, và niên đại rất gần: tab「Template button」vẫn còn "
     "được cập nhật tới 03/2026 (cột Bug KH #35114/#34923) trong khi SpecChange #24890 là 12/2023. "
     "**Quy tắc「ưu tiên TC mới nhất」là căn cứ YẾU ở đây** vì tab Template button mới hơn về ngày cập "
     "nhật nhưng khối r53-r85 là nội dung CŨ chưa được sửa sau #24890. Lý do thật sự chọn 40/60: "
     "SpecChange #24890 nói rõ ý định đổi, VÀ spec-features (đọc từ source code, 03/2026) khẳng định 40/60.",
     "『Panel/Button — tiêu đề & nội dung』TC「Title panel: ... ≤40 ký tự lưu OK...」· "
     "TC「Content panel (本文): bắt buộc; ≤60 ký tự lưu OK...」",
     "",
     "① Chốt 40/60 (đề xuất) và xác nhận nguyên văn msg lỗi thật cho mốc 40 và 60 trên staging — TC "
     "hiện dùng msg suy luận「本文は60文字以内で入力してください。」.\n"
     "② Đánh dấu khối「Template button」r53-r85 của sheet gốc là ĐÃ LẠC HẬU (thêm ghi chú vào sheet).\n"
     "③ Nếu code thực tế vẫn là 20/40 → raise ticket vì spec-features và SpecChange #24890 đều nói 40/60."],

    ["MT-04", "CAO", W,
     "Khi title/content có gán [name] thì giới hạn ký tự bị RÚT NGẮN — spec không ghi",
     "「Improve tạo temp」r3「title: hiển thị giới hạn **20/40**, [name] sẽ chiếm 20 ký tự」, note "
     "「khi có [name] thì chuyển thành giới hạn 20 ký tự, khi ko có thì giới hạn 40 ký tự」· "
     "r7「description: hiển thị giới hạn **20/60**, [name] sẽ chiếm 20 ký tự」· r4-r6 và r8-r10 test "
     "mốc <20 / =20 / >20 và <40 / =40 / >40.",
     "`ui-spec.md:259-260` và `feature-spec.md:627-628` chỉ ghi Max 40 / Max 60 **tĩnh**, KHÔNG có "
     "mục nào nói giới hạn thay đổi khi nội dung chứa biến `{name}` / `[name]`.\n"
     "`feature-spec.md:337` chỉ nói chung về friend info auto-insert.",
     "Đây là rule ảnh hưởng trực tiếp việc admin có lưu được template hay không, và là nguồn nhầm lẫn "
     "kinh điển (bộ đếm tự nhảy 20/40 khi chèn [name]). Spec bỏ sót hoàn toàn → tester mới đọc spec sẽ "
     "báo bug oan khi thấy bộ đếm nhảy.",
     "『Panel/Button — tiêu đề & nội dung』TC「Khi title CÓ gán [name]... giới hạn đổi thành 20/40」· "
     "TC「Khi content CÓ gán [name]... 20/60」",
     "",
     "① Xác nhận rule còn đúng trên staging (chèn [name] rồi đọc bộ đếm).\n"
     "② Bổ sung vào `ui-spec.md` mục SCR-TMT-06 và `feature-spec.md` Field Matrix #15/#16 dòng "
     "「khi content chứa {name}/[name] thì biến chiếm 20 ký tự trong bộ đếm」.\n"
     "③ Xác nhận cùng rule có áp cho `{name}` (ngoặc nhọn) hay chỉ `[name]`."],

    ["MT-05", "TRUNG BÌNH", W,
     "Xóa folder: cascade tới đâu? tmp_button / buttons có bị xóa không?",
     "「Improve list template」r78「Bảng category update **is_deleted = 1**」(soft delete) · "
     "r81「update cột is_deleted = 1 bảng category — xóa trong bảng template, tmp_location, "
     "tmp_introduction, tmp_question, image_map, image_map_items, t_actions, t_actions_detail "
     "**( tmp_button, buttons,)** trong ngoặc **từ trước đã không xóa**」.",
     "`feature-spec.md:659` BR-05「Xoá folder → **hard delete** tất cả template bên trong → cascade "
     "xoá template con nếu type=group」·「Mất dữ liệu không phục hồi」.\n"
     "`feature-spec.md:660` BR-06「Hard delete template + cleanup ActionDetail, SendRandomMessage, "
     "TemplateMappingTable」.\n"
     "`logic-spec.md:298`「Khi xoá folder → tất cả template trong folder bị xoá (hard delete)」.",
     "2 điểm lệch: (a) spec nói folder bị hard delete, TC nói `category.is_deleted = 1` (soft delete); "
     "(b) spec ghi cascade cleanup relationships, TC ghi rõ `tmp_button` và `buttons` **KHÔNG** bị xóa "
     "→ để lại dữ liệu mồ côi. Ảnh hưởng: dung lượng DB tăng dần và nguy cơ id bị tái sử dụng sai.",
     "『Folder template』TC「Xóa folder RỖNG → ... category ghi is_deleted = 1」· "
     "TC「Xóa folder CÓ template → cascade xóa... còn tmp_button/buttons thì KHÔNG xóa」",
     "",
     "① Chốt hành vi ĐÚNG cho `tmp_button`/`buttons`: để mồ côi (giữ nguyên) hay bổ sung cleanup.\n"
     "② Sửa `feature-spec.md` BR-05 từ「hard delete folder」thành soft delete (`is_deleted = 1`) "
     "và `logic-spec.md:298` tương ứng.\n"
     "③ Nếu chốt phải cleanup → raise ticket và sửa expected TC."],

    ["MT-06", "CAO", W,
     "Tạo template mới: redirect sang màn EDITOR hay sang màn list TEMPLATE CON?",
     "「Improve list template」r111-r112「Tạo group template success thì **redirect đến MH list của "
     "group template** (để tạo template con)」. Toàn bộ corpus vận hành theo mô hình 2 tầng: "
     "「template cha (group)」chứa「template con」; màn 新規作成 tạo ra template CHA.",
     "`feature-spec.md:262` Luồng SCR-TMT-02:「[Kết quả] **Redirect đến trang editor (SCR-TMT-04~10 "
     "tuỳ loại)**」, request `{ tmp_name, tmp_type: \"text\" (default), tmp_category }`.\n"
     "`feature-spec.md:57` xếp「Park/Group template」vào Scope nhưng mô tả như container phụ, không "
     "phải mô hình chính.",
     "Lệch về MÔ HÌNH DỮ LIỆU, không chỉ về điều hướng. Spec mô tả FA-010 như「1 template = 1 tin "
     "nhắn」còn corpus TC mô tả「1 template cha = nhiều template con (nhiều tin nhắn)」. Nếu spec sai "
     "thì mọi mô tả luồng SCR-TMT-02→10 và Field Matrix đều lệch một tầng; ảnh hưởng cả cách viết TC "
     "cho các tính năng tham chiếu (chat 1:1, broadcast, scenario).",
     "『Tạo group template』TC「Tạo group template thành công → redirect sang màn list template con...」· "
     "toàn bộ nhóm『Màn list group template』và『Màn list template con』",
     "",
     "① Xác nhận trên staging: bấm 新規作成 → nhập tên → 「テンプレートを作成」→ màn hình kế tiếp là gì.\n"
     "② Nếu là màn list template con: sửa `feature-spec.md:262` và bổ sung mô tả rõ 2 tầng "
     "cha/con vào §2 (đề xuất thêm SCR-TMT-01b「danh sách template con」).\n"
     "③ Rà lại `api-spec.md` EP-21 (`/basic/message-template/add`) xem còn dùng hay đã bị EP-30 thay thế."],

    ["MT-07", "TRUNG BÌNH", W,
     "Định dạng file được phép: ảnh có .gif/.jpeg không? audio có .mp3 không? .avif bị chặn?",
     "「Template button」r601「Upload ảnh **jpg, png, gif, jpeg**」(hợp lệ) · r600「Upload file không "
     "phải định dạng image — **Upload ảnh avif**」(báo lỗi).\n"
     "「Type ảnh」r4「chọn ko phải dạng png/jpg → báo lỗi」nhưng r5 note「check với ảnh **jpeg** 12mb」và "
     "r9 note「ảnh dạng **jpeg** đang ko upload dc」.\n"
     "「Type audio」r4 note「**mp3 và m4a giống nhau**」.",
     "`ui-spec.md:350-352` — Hình ảnh: **.png / .jpg** (10MB) · Video: **.mp4** (200MB) · "
     "Âm thanh: **.m4a** (200MB).\n"
     "`feature-spec.md:443` — hỗ trợ .png/.jpg (max 10MB), .mp4 (max 200MB), .m4a (max 200MB).",
     "Spec liệt kê danh sách HẸP hơn corpus. Nếu code thực tế nhận .gif/.jpeg/.mp3 mà spec không ghi "
     "thì tester bỏ qua các định dạng đó; ngược lại nếu code chỉ nhận .png/.jpg thì TC r601 sẽ FAIL. "
     "Riêng .jpeg có dấu hiệu **không nhất quán** giữa 2 tab TC (r601 nói được, r9 note nói không).",
     "『Panel/Button — panel & ảnh』TC「Upload ảnh panel: ... sai định dạng...」· "
     "『Media — ảnh』TC「Upload ảnh sai định dạng hoặc > 10MB...」· "
     "『Media — video & audio』TC「Audio: chọn file KHÔNG phải m4a...」",
     "",
     "① Test trên staging từng định dạng: .png .jpg .jpeg .gif .webp .avif cho ảnh; .m4a .mp3 .wav "
     "cho audio; .mp4 .mov cho video.\n"
     "② Cập nhật `ui-spec.md:350-352` và `feature-spec.md:443` theo danh sách thật.\n"
     "③ Làm rõ nhánh .jpeg (r601 vs r9) — nếu .jpeg lỗi thì raise ticket."],

    ["MT-08", "TRUNG BÌNH", W,
     "Ý nghĩa checkbox URL gốc (is_shorten_url) và rule action THẮNG checkbox",
     "「Template type text」r49「default là **không tick** ⇒ **có** shorten url」· "
     "r51「link ngoài hệ thống, ko tick ⇒ khi send cho user thì shorten url」· "
     "r52「có tick (url ko setting action) ⇒ có tick thì khi gửi **không** shorten url」· "
     "r53「có tick (url **có** setting action) ⇒ **vẫn shorten** để hệ thống send action」· "
     "r50「link trong hệ thống: tick / ko tick đều **vẫn nguyên link**」.",
     "`feature-spec.md:621` Field Matrix #9 —「Checkbox URL gốc → `template.is_shorten_url` · "
     "**Checked=0 (URL gốc), Unchecked=1 (shortened)** **[Trung bình]**」— spec TỰ đánh dấu mức tin cậy "
     "Trung bình.\n"
     "`feature-spec.md:340`「Khi checked, `is_shorten_url = 0` → **mất tracking URL clicks**」.\n"
     "Spec KHÔNG có dòng nào về rule「URL có action thì vẫn shorten」và về URL nội bộ.",
     "TC lấp đúng chỗ spec tự nhận chưa chắc (Field #9), nhưng thêm 2 rule spec bỏ sót: (a) URL có "
     "setting action thì checkbox bị ghi đè → vẫn shorten; (b) URL nội bộ không bị ảnh hưởng bởi "
     "checkbox. Rule (a) quan trọng vì nó là lý do tracking/action vẫn chạy dù admin chọn URL gốc.",
     "『Text — PDF & shorten URL』TC「Checkbox URL gốc mặc định KHÔNG tick...」· "
     "TC「Tick checkbox... KHÔNG setting action → giữ URL gốc」· "
     "TC「Tick checkbox nhưng URL CÓ setting action → vẫn bị shorten」· TC「URL TRONG hệ thống...」",
     "",
     "① Xác nhận mapping `is_shorten_url` (0/1) ứng với checked/unchecked trên DB thật.\n"
     "② Bổ sung vào `feature-spec.md` BR-09 và Field Matrix #9: rule action ghi đè checkbox, "
     "và rule URL nội bộ không shorten.\n"
     "③ Nâng mức tin cậy Field #9 từ [Trung bình] lên [Cao] sau khi xác nhận."],

    ["MT-09", "TRUNG BÌNH", W,
     "Rule ảnh panel「all-or-nothing」— spec không ghi",
     "「Template button」r46「nhiều panel, tất cả panel đều **không** set ảnh → nhấn save ⇒ **lưu success**」· "
     "r47「có nhiều panel trong đó có **ít nhất 1 panel có ảnh** → nhấn save ⇒ **báo lỗi** các panel "
     "không có ảnh: 「パネル<số thứ tự của panel>に画像が登録されておりません。」」· "
     "r48「tất cả các panel đều set ảnh → lưu success」.",
     "`ui-spec.md:258`「画像登録」Image upload, Kích thước khuyến nghị 1024x678 px, **Bắt buộc: Không**.\n"
     "`feature-spec.md:626` Field Matrix #14 — không ghi rule liên panel.\n"
     "`feature-spec.md:663` BR-08 chỉ nói về giới hạn số nút/panel; BR-11 chỉ nói validate image map area.",
     "Rule này chặn admin lưu template và có msg lỗi riêng nhưng spec ghi「Bắt buộc: Không」→ đọc spec "
     "sẽ hiểu là ảnh luôn optional cho từng panel độc lập. Đây là ràng buộc do LINE carousel yêu cầu "
     "(mọi card phải cùng có/không có hero image), nên khả năng cao là rule thật.",
     "『Panel/Button — panel & ảnh』TC「Nếu CÓ panel set ảnh thì TẤT CẢ panel phải set ảnh...」",
     "",
     "① Xác nhận msg lỗi nguyên văn và số thứ tự panel trong msg trên staging.\n"
     "② Bổ sung BR mới vào `feature-spec.md` §5:「Ảnh panel là all-or-nothing trong 1 template」kèm "
     "msg lỗi.\n"
     "③ Sửa `ui-spec.md:258` từ「Bắt buộc: Không」thành「Không, nhưng all-or-nothing trong 1 template」."],

    ["MT-10", "TRUNG BÌNH", W,
     "Công thức resize ảnh nhiều panel theo tỉ lệ ảnh của PANEL 1 — spec không ghi",
     "「Template button」r52「resize ảnh của **all panel** về 1 kích thước theo kích thước của **ảnh "
     "panel 1**: ảnh panel 1 là ảnh vuông hoặc dài thì resize về **1:1**; ảnh panel 1 là ảnh hình chữ "
     "nhật thì resize về **2:3**」.\n"
     "「Template button」r1264-r1408 test ma trận tỉ lệ height/width ≤ 3 và > 3 cho panel 1, 2, 3 ở "
     "cả 4 sub-type và 4 màn tạo.",
     "`logic-spec.md` và `feature-spec.md:399` chỉ nói「Tính `rate_image_button` (aspect ratio) từ ảnh」"
     "— KHÔNG nêu công thức, không nói ảnh panel 1 quyết định toàn bộ.\n"
     "`db-mapping.md` không mô tả giá trị hợp lệ của `rate_image_button`.",
     "Đây là hành vi người dùng cuối thấy trực tiếp (ảnh bị crop/co). Nếu tester không biết rule, sẽ "
     "báo bug「ảnh panel 2 bị méo」trong khi đó là thiết kế. Ma trận tỉ lệ ≤3 / >3 trong TC gợi ý còn "
     "có ngưỡng phụ mà spec không đề cập.",
     "『Panel/Button — panel & ảnh』TC「Resize ảnh nhiều panel theo tỉ lệ ảnh của PANEL 1...」· "
     "TC「Ma trận tỉ lệ ảnh panel: height/width ≤ 3 và > 3...」",
     "",
     "① Đọc source `save()` phần type=form để lấy công thức thật của `rate_image_button` và ngưỡng 3.\n"
     "② Bổ sung công thức vào `logic-spec.md` (mục xử lý ảnh panel) và enum `rate_image_button` vào "
     "`db-mapping.md`.\n"
     "③ Xác nhận ý nghĩa ngưỡng height/width = 3 (tại sao 3?)."],

    ["MT-11", "CAO", W,
     "Spec FA-010 KHÔNG có mục Backup — nhưng corpus có nhiều rule backup quan trọng",
     "「Template type text」r168「Backup được Nội dung message · Backup được setting có shorten url hay "
     "không · **Setting của url redirect KHÔNG support backup**」(note「job chưa sửa」) · "
     "r169-r182: link form-answer/code form/code conversion/link booking event **được replace** sang "
     "bản ghi mới của bot nhận; code friend info basic **giữ nguyên**; friend info tự tạo replace theo "
     "id mã hoá; **link item và link booking calendar chưa support backup nên giữ nguyên** "
     "(r174 note「Nhắn Duy sửa thêm backup cho link booking event」).\n"
     "「Improve list template」r572 mô tả đầy đủ luồng backup bằng コピーコード / データ受信コード.",
     "`feature-spec.md` §7 Background Jobs — ghi「Tính năng Template **không có background job chính**」, "
     "chỉ nhắc `send_random_messages`.\n"
     "`feature-spec.md:658` BR-02 chỉ nói backup **chặn thao tác ghi**.\n"
     "`db-mapping.md:43` liệt kê `backup_history` nhưng KHÔNG mô tả luồng backup template.\n"
     "KHÔNG có mục nào mô tả replace code/link khi backup.",
     "Backup là luồng người dùng cuối thật (chuyển dữ liệu giữa bot) và corpus cho thấy nó có nhiều "
     "trường hợp bán-hỗ trợ (item/calendar/url-redirect chưa support). Spec bỏ trống hoàn toàn → tester "
     "sẽ không biết cái gì được replace, cái gì giữ nguyên, và sẽ báo bug oan cho item/calendar.",
     "『Copy & Backup』cả 3 TC · 『URL redirect — hết hạn & action』TC「Copy / Backup template có URL...」· "
     "『Delay message』TC「Copy và Backup group template có delay...」",
     "",
     "① Xác nhận trạng thái hiện tại của backup: url redirect, link item, link calendar, link booking "
     "event đã support chưa (r174 nói đang nhắn Dev sửa).\n"
     "② Bổ sung mục『Backup / データ移行』vào `feature-spec.md` với bảng「thành phần ↔ có/không backup ↔ "
     "cách replace」.\n"
     "③ Nếu item/calendar vẫn chưa support → ghi vào Gaps & Unknowns của spec để không bị báo bug lặp."],

    ["MT-12", "TRUNG BÌNH", W,
     "Bộ đếm 900 theo URL-encode cho 友だちにテキストをシェアする — spec không ghi",
     "「Task nhỏ+ check Bug Kh」r615 (SpecImprove #33326, 29/08/2025)「Actual: Hiện tại giới hạn ký tự = "
     "**80** ký tự. Expect: Giới hạn ký tự = **800** ký tự」· r616「count 1 ký tự khi nhập 1 ký tự」· "
     "r617-r618「899 ký tự → hiển thị bộ đếm **899/900**; 900 ký tự → **900/900**」· "
     "r664/r667/r692「count **9** ký tự đối với từng text Nhật · **1** ký tự với latinh · **3** ký tự "
     "với space + ký tự đặc biệt · **12** ký tự với emoji」.",
     "`ui-spec.md` mục LINE URL scheme và `feature-spec.md:629` Field Matrix #17-#18 KHÔNG có dòng nào "
     "về giới hạn ký tự của text share, cũng không có bộ đếm 900 hay quy tắc đếm theo URL-encode.\n"
     "`api-spec.md` EP-46 (`init-data-button`) không mô tả field này.",
     "Bộ đếm hiển thị con số 900 trong khi yêu cầu nghiệp vụ là 800 ký tự — chênh lệch là do đếm theo "
     "độ dài URL-encode, không phải số ký tự. Nếu spec không ghi, tester sẽ báo bug「bộ đếm sai, nhập "
     "10 chữ Nhật mà nhảy 90」. Đồng thời con số 800↔900 dễ bị hiểu nhầm là bug.",
     "『Panel/Button — LINE URL scheme』TC「「友だちにテキストをシェアする」: bộ đếm URL-encode 900...」· "
     "TC「Bộ đếm 900 áp cho cả 4 sub-type button, image map... và 3 màn tạo template khác」",
     "",
     "① Xác nhận trọng số đếm thật (JP=9, latinh=1, space/đặc biệt=3, emoji=12) và mốc 900.\n"
     "② Bổ sung vào `ui-spec.md` SCR-TMT-06 (mục LINE URL scheme) và Field Matrix: giới hạn 800 ký tự "
     "nghiệp vụ ↔ bộ đếm 900 đơn vị URL-encode kèm bảng trọng số.\n"
     "③ Giải thích rõ trong spec vì sao hiển thị /900 chứ không /800."],

    ["MT-13", "THẤP", W,
     "Cột「内容」ở bảng danh sách hiển thị gì? (spec để ở mục điểm chưa rõ)",
     "「Improve list template」r349-r353 test cột「内容」theo từng loại template con: Type text / Type "
     "button / Type stemp / Type media / Type loccation.\n"
     "「Improve list template」r94-r95 kiểm giao diện hiển thị của list group template.",
     "`ui-spec.md` mục『Điểm chưa rõ』#2 —「Cột「内容」hiển thị gì? Preview text hay icon loại?」"
     "**[Thấp]**.\n"
     "`feature-spec.md:617` Field Matrix #5 —「`template.content` + `template.type` → Rút gọn content, "
     "icon theo type」(đã suy luận).",
     "Spec tự nhận chưa rõ; corpus có TC cho cả 5 loại → đây là cơ hội ĐÓNG GAP chứ không phải mâu "
     "thuẫn thật. Cần Leader xác nhận nội dung hiển thị thật để chốt.",
     "『Màn list group template』TC「Cột「内容」hiện preview đúng theo từng loại template con」",
     "",
     "① Chụp màn hình cột「内容」cho đủ 5 loại template trên staging.\n"
     "② Cập nhật `ui-spec.md` mục Điểm chưa rõ #2 → chuyển thành mô tả xác nhận.\n"
     "③ Nâng Field Matrix #5 từ suy luận thành [Cao]."],

    ["MT-14", "THẤP", W,
     "Có phân trang ở danh sách template không? (spec để ở mục điểm chưa rõ, mức Trung bình)",
     "「Improve list template」r341「Check phân trang default」· r342「SL bản ghi/1 trang ⇒ **20**」· "
     "r343「Check <, >」· r344「Check chuyển sang trang khác ⇒ Hiển thị data đúng trang đó」· "
     "r345「Check STT trang kế tiếp ⇒ **k có stt**」· r346「Kiểm tra các chức năng chung trên trang đó "
     "⇒ Hoạt động tốt」.",
     "`ui-spec.md` mục『Điểm chưa rõ』#5 —「Có pagination cho danh sách template không?」"
     "**[Trung bình]**.\n"
     "`api-spec.md` EP-20 (`/ajax/init-template`) không mô tả tham số page/limit.",
     "Spec tự nhận chưa rõ; corpus khẳng định CÓ phân trang 20 dòng/trang và KHÔNG có cột STT. "
     "Đây là ĐÓNG GAP. Cần chốt để `api-spec.md` bổ sung tham số phân trang.",
     "『Phân trang』TC「Phân trang mặc định 20 bản ghi / trang...」",
     "",
     "① Xác nhận số dòng/trang thật (20?) và có cho đổi số dòng/trang không.\n"
     "② Cập nhật `ui-spec.md` Điểm chưa rõ #5 và bổ sung tham số phân trang vào `api-spec.md` EP-20.\n"
     "③ Ghi rõ「bảng không có cột STT」vào ui-spec để tránh báo bug thiếu STT."],

    ["MT-15", "THẤP", W,
     "Giới hạn 3 người dùng クイックテスト (quick send) — spec không ghi",
     "「Improve list template」r286「Enable, **tối đa 3 friend**」· r287「Hiển thị thông báo: "
     "**クイックテストユーザーの登録を解除**」· r290「Hiển thị thông báo: "
     "**クイックテストユーザーに登録（3人まで)** — Không được Enable icon tại bản ghi vừa move over vào」· "
     "r424「Enable, tối đa 3 friend được tích quick sen」.",
     "`feature-spec.md:214-236` Luồng 8 (Quick test) và `api-spec.md` EP-70/EP-72 chỉ nói lọc "
     "`is_tester = 1`, `is_blocked = 0`; KHÔNG có giới hạn số lượng.\n"
     "`db-mapping.md:40` nhắc `bot_line_user` có `is_tester` và `is_quick_reply` nhưng không nói "
     "giới hạn 3.",
     "Giới hạn 3 chặn thao tác của admin và có msg tiếng Nhật riêng → là rule nghiệp vụ thật. Spec bỏ "
     "sót nên tester không biết mốc và sẽ không test biên.",
     "『Quick test — tester』TC「Bật quick send cho friend → hiện thông báo, tối đa 3 user được bật」· "
     "TC「Tắt quick send cho friend đang bật...」",
     "",
     "① Xác nhận mốc 3 và nguyên văn 2 msg trên staging.\n"
     "② Bổ sung vào `feature-spec.md` §5 một BR mới:「Tối đa 3 クイックテストユーザー được bật quick send」"
     "và ghi cột DB tương ứng (`bot_line_user.is_quick_reply`?).\n"
     "③ Làm rõ khác nhau giữa「đăng ký account test (is_tester)」và「bật quick send」."],

    ["MT-16", "THẤP", W,
     "Quy định font chữ ô nhập tên (Noto Sans JP / Yu Gothic, bỏ sans-serif) — spec không ghi",
     "「Task nhỏ+ check Bug Kh」r697 (SpecImprove #36385, 12/05/2026「Font sau update khó đọc trên "
     "Windows」) · r698/r700/r703/r706 Expect:「**font-family: 'Noto Sans JP'** · Family name: "
     "**Yu Gothic** · **Bỏ sans-serif**」— áp cho ô tên folder và ô tên template ở màn template và "
     "cover cả scenario / form-answer.",
     "`ui-spec.md` không có mục nào về font-family của ô nhập.\n"
     "`feature-spec.md` không có mục design system / typography.",
     "Đây là yêu cầu spec-improve có kiểm chứng bằng CSS cụ thể, chỉ tái hiện trên Windows. Không ghi "
     "vào spec thì lần refactor CSS sau sẽ vô tình quay lại `sans-serif` mà không ai phát hiện. "
     "Mức THẤP vì không ảnh hưởng dữ liệu.",
     "『Màn list template』TC「Font chữ ô nhập tên folder / tên template dùng Noto Sans JP...」· "
     "TC「Font Noto Sans JP áp cả ở ô tên folder/template của scenario · broadcast · form-answer」",
     "",
     "① Xác nhận CSS hiện tại trên PRODUCTION (SpecImprove #36385 đã release chưa).\n"
     "② Ghi 1 dòng vào `ui-spec.md` mục chung:「ô nhập tên dùng font-family 'Noto Sans JP', "
     "fallback Yu Gothic, không dùng sans-serif」.\n"
     "③ Cân nhắc thêm vào checklist regression khi đổi CSS toàn cục."],

    ["MT-17", "TRUNG BÌNH", W,
     "Template クイックリプライ luôn ở CUỐI danh sách và không sort được — spec không ghi",
     "「Improve list template」r301「Hiển thị theo thứ tự trong màn list template, **Button quick sẽ ở "
     "cuối danh sách**」· r464「Drop&drag template quick reply ⇒ **template quick reply cố định**」.",
     "`feature-spec.md:194-212` Luồng 3 (Sắp xếp template) chỉ nói `sortItem` + `position`, KHÔNG có "
     "ngoại lệ cho quick reply.\n"
     "`db-mapping.md` `template.position` không mô tả ràng buộc theo `type_button`.",
     "Ràng buộc này đến từ LINE (quick reply luôn gắn vào tin cuối) nên khả năng là rule thật, nhưng "
     "spec không ghi → tester sẽ báo bug「không kéo được template quick reply」và admin không hiểu vì "
     "sao thứ tự preview khác thứ tự mình sắp.",
     "『Màn list template con』TC「Template con dạng クイックリプライ luôn nằm CUỐI danh sách, không "
     "kéo-thả được」· 『Quick test — gửi & preview』TC「Preview trong modal hiện đủ template con...」",
     "",
     "① Xác nhận hành vi trên staging (kéo quick reply lên đầu → có bị chặn?).\n"
     "② Bổ sung BR vào `feature-spec.md`:「template con dạng quick reply luôn được xếp cuối group, "
     "không tham gia sort」kèm lý do (ràng buộc LINE).\n"
     "③ Xác nhận preview và tin gửi thật đều theo quy tắc này."],

    ["MT-18", "TRUNG BÌNH", W,
     "Folder mặc định 未分類 (category_id = 0) có NHÁNH CODE RIÊNG — rủi ro lệch hành vi",
     "「Template button」r1049「Preview ở mh edit group temp (**group = 0**) (là folder chưa phân loại — "
     "**do chỗ này code riêng**)」và r1087「Preview ở mh list temp (folder group = 0 ⇒ chính là folder "
     "chưa phân loại ⇒ **do chỗ này code riêng**)」— corpus lặp lại toàn bộ ma trận preview 4 loại "
     "button riêng cho group = 0 và group = 1.\n"
     "「Improve list template」r159/r169/r188 cũng test riêng sort/search/tạo template ở folder 未分類.",
     "`feature-spec.md:290` chỉ ghi「Folder mặc định「未分類」có `category_id = 0` — không có record trong "
     "bảng `category`」và BR-04「không thể xoá」.\n"
     "Spec KHÔNG nói có nhánh xử lý riêng về hiển thị / preview / sort / search cho `category_id = 0`.",
     "Đây là rủi ro regression có hệ thống: mọi tính năng của màn template phải test 2 lần (folder "
     "thường và 未分類). Nếu spec không ghi, tester sẽ chỉ test 1 nhánh và bỏ lọt bug ở nhánh 未分類 "
     "(đúng kiểu bug KH #36384 xảy ra ở folder có tên đặc biệt).",
     "『Preview ở các màn khác』TC「Preview template button ở màn edit group / list template với folder "
     "未分類 (group = 0)...」· 『Sort & search template』TC「Sort ở folder mặc định 未分類...」· "
     "『Recover dữ liệu lỗi』TC「Bug KH #36384 — regression: tạo / edit / copy template ở folder default "
     "và folder khác default」",
     "",
     "① Hỏi Dev: những hàm nào rẽ nhánh theo `category_id = 0` (preview, list, sort, search, create).\n"
     "② Bổ sung mục cảnh báo vào `feature-spec.md` §5 hoặc §9:「`category_id = 0` có nhánh xử lý riêng "
     "— mọi thay đổi màn template phải regression cả 2 nhánh」.\n"
     "③ Đưa vào checklist review cố định của FA-010."],

    ["MT-19", "THẤP", W,
     "Cho phép tạo folder / group TRÙNG TÊN — spec không ghi",
     "「Improve list template」r17「Tạo folder trùng với name folder đã tạo ⇒ **xuống cuối danh sách**」"
     "(tức là tạo thành công) · r64「Change name folder trùng với name folder đã tạo」(cùng nhóm, "
     "không báo lỗi).",
     "`feature-spec.md:280-296` Luồng tạo folder và BR-04 không có ràng buộc unique cho `category.name`.\n"
     "`db-mapping.md:471` `category.name` varchar(100), không nói unique index.",
     "Không phải mâu thuẫn mà là rule chỉ có trong TC. Cần ghi vào spec vì nó ảnh hưởng trải nghiệm "
     "(admin có thể tạo 5 folder cùng tên và không phân biệt được), và ảnh hưởng cách viết TC search "
     "(search trả nhiều folder cùng tên).",
     "『Folder template』TC「Tạo folder TRÙNG tên folder đã có → vẫn tạo thành công」",
     "",
     "① Xác nhận hệ thống thật có chặn trùng tên không (cả folder và group template).\n"
     "② Ghi rõ vào `feature-spec.md` §5:「`category.name` KHÔNG unique — cho phép trùng tên」.\n"
     "③ Hỏi Leader có nên chặn trùng tên hay không (đề xuất cải tiến UX)."],

    ["MT-20", "TRUNG BÌNH", W,
     "Popup sắp xếp KHÔNG reset khi đóng mà không lưu — TC gốc ghi nhận là BUG",
     "「Improve list template」r146「Danh sách template không thay đổi vị trí」kèm note "
     "**「popup không reset」** · r456 note **「thay đổi trong popup chưa lưu >> ngoài màn list đã thay "
     "đổi」** · r45 (folder) cũng cùng nhóm thao tác.",
     "`feature-spec.md:194-212` Luồng 3 chỉ mô tả `sortItem` khi lưu. Spec KHÔNG mô tả hành vi khi "
     "đóng popup mà chưa lưu (state reset hay giữ).",
     "TC gốc ghi Expect là「không thay đổi vị trí」nhưng note cho thấy thực tế popup KHÔNG reset và "
     "thậm chí màn list ngoài đã đổi khi chưa lưu → đây là bug dữ liệu hiển thị. Nếu viết TC theo "
     "note thì hợp thực tế nhưng sai kỳ vọng; nếu theo Expect thì TC dự kiến FAIL.",
     "『Sắp xếp & ẩn folder』TC「Kéo-thả xong nhưng KHÔNG bấm「保存」→ thứ tự folder giữ nguyên」· "
     "『Sort & search template』TC「Kéo-thả group xong đóng popup không lưu → thứ tự ngoài màn list giữ "
     "nguyên」",
     "",
     "① Test lại trên staging: kéo-thả rồi đóng popup không lưu, quan sát popup mở lại và màn list ngoài.\n"
     "② Nếu vẫn lỗi → raise ticket; giữ expected TC theo hành vi ĐÚNG và ghi「dự kiến FAIL」.\n"
     "③ Bổ sung vào spec:「đóng popup sort mà không lưu thì reset toàn bộ thay đổi」."],

    ["MT-21", "TRUNG BÌNH", W,
     "Có tự trim space đầu/cuối ở các ô nhập hay không? — corpus KHÔNG kết luận",
     "「Template type text」r16「Có tự trim space đầu cuối hay không? ⇒ **ko tự strim => đã check trên "
     "stg**」(ô nội dung text).\n"
     "「Improve list template」r6「Các input text đã tự động trim space đầu cuối chưa?」và r103「Check "
     "trim space đầu cuối chưa」— **chỉ có tiêu đề, KHÔNG có Expect Result**.\n"
     "r101「Nhập khoảng trắng ⇒ cảnh báo」(ô 管理名 chỉ gồm space thì bị chặn).\n"
     "「Type ảnh」r3 cũng để câu hỏi tương tự chưa trả lời.",
     "`feature-spec.md:620` Field Matrix #8 —「Textarea nội dung text · **Normalize line breaks**」— "
     "chỉ nói normalize xuống dòng, KHÔNG nói trim space.\n"
     "`db-mapping.md:479` cũng chỉ ghi「Lưu text thuần, normalize line breaks」.",
     "Đây là **vùng mù**: ô nội dung text đã xác nhận KHÔNG trim, nhưng ô 管理名 / tên folder thì corpus "
     "để ngỏ (chỉ biết chuỗi toàn space bị chặn). Không rõ「  ABC  」có bị trim thành「ABC」hay không → "
     "ảnh hưởng search (search「ABC」có ra không) và hiển thị danh sách.",
     "『Text — soạn nội dung』TC「Nội dung text KHÔNG tự trim space đầu/cuối」· "
     "『Tạo group template』TC「管理名 chỉ gồm khoảng trắng → bị chặn」",
     "",
     "① Test riêng từng ô: nội dung text, 管理名, tên folder, ボタンテキスト, title/content panel với "
     "chuỗi「  ABC  」→ đọc DB xem có bị trim.\n"
     "② Ghi kết quả vào Field Traceability Matrix (thêm cột「Trim space」).\n"
     "③ Nếu không trim → bổ sung TC search với keyword có space để làm rõ hành vi."],

    ["MT-22", "TRUNG BÌNH", W,
     "Nội dung SAU khi replace code vượt 5.000 ký tự → lỗi lúc gửi, spec không mô tả",
     "「Template type text」r35「Sau khi insert các data trên, số ký tự quá 5000 thì sao? ⇒ **Case này "
     "khi gửi sẽ bị lỗi và hiện ở màn /basic/error-list**」kèm note「test gắn friend infor dạng mail => "
     "khi send bị quá 5000 ký tự (setting mail quá 30 ký tự)」.",
     "`ui-spec.md:187` — Vùng soạn thảo Max 5.000 ký tự (0/5,000).\n"
     "`feature-spec.md:620` Field Matrix #8 — Max 5.000 ký tự.\n"
     "Spec KHÔNG mô tả điều gì xảy ra khi nội dung SAU khi replace `{name}` / `[FRIEND_INFO_...]` "
     "vượt 5.000.",
     "Validate lúc lưu chỉ đếm chuỗi code (ngắn) nhưng lúc gửi mới replace thành giá trị thật (có thể "
     "rất dài) → tin gửi thất bại mà admin không biết trước. Đây là lỗi người dùng cuối gặp (không "
     "nhận được tin) và chỉ thấy dấu vết ở màn error-list.",
     "『Text — insert dữ liệu』TC「Sau khi insert data mà nội dung vượt 5.000 ký tự khi gửi → tin lỗi, "
     "ghi nhận ở màn /basic/error-list」",
     "",
     "① Xác nhận trên staging: tạo template sát 5.000 ký tự + nhiều friend info dài → gửi → kiểm tra "
     "error-list.\n"
     "② Bổ sung vào `feature-spec.md` §5 BR mới hoặc §9 Gaps:「validate 5.000 ký tự chỉ áp lúc lưu; "
     "nội dung sau replace có thể vượt và gây lỗi gửi, ghi vào error-list」.\n"
     "③ Hỏi Leader có cần cảnh báo trước cho admin (đề xuất cải tiến)."],

    ["MT-23", "THẤP", W,
     "Text preview URL giới hạn 25 ký tự — spec không ghi",
     "「Template type text」r68「default ⇒ tự fill description của link đó」· r69「ko nhập ⇒ **required**」· "
     "r70「nhập **> 25 ký tự** ⇒ **báo lỗi**」.",
     "`db-mapping.md:270` `template_url_redirect.meta_title` varchar(255) · `meta_description` "
     "varchar(255).\n"
     "`feature-spec.md:359-366` mô tả các cột `meta_title` / `meta_image` / `meta_description` là "
     "「OGP metadata cache」— KHÔNG có giới hạn 25 ký tự ở UI.",
     "Lệch lớn giữa giới hạn UI (25) và độ dài cột DB (255). Nếu spec chỉ ghi 255 thì tester không test "
     "biên 25 và không biết ô này là REQUIRED. Cũng chưa rõ ô 25 ký tự map vào `meta_title` hay "
     "`meta_description`.",
     "『URL redirect — preview & metadata』TC「Text preview URL: để rỗng → required; nhập > 25 ký tự → "
     "báo lỗi」· TC「Popup setting hiển thị URL trên LINE: text preview default lấy description...」",
     "",
     "① Xác nhận mốc 25 và nguyên văn msg lỗi; xác định ô đó ghi vào cột DB nào.\n"
     "② Bổ sung vào `ui-spec.md` SCR-TMT-05 và Field Matrix #12: giới hạn 25 ký tự, bắt buộc nhập, "
     "default = OGP description.\n"
     "③ Làm rõ vì sao UI 25 mà DB 255."],

    ["MT-24", "CAO", W,
     "Công thức tính hạn URL kiểu DURATION đã đổi — spec chỉ ghi tên cột, không ghi công thức",
     "「Task nhỏ+ check Bug Kh」r11「sửa lại logic giới hạn open url dạng duration. **Hiện tại: 0 ngày "
     "00:01 thì 1' sau khi gửi sẽ hết hạn. Expect: 1 ngày 00:01 ⇒ vào lúc 00:01 1 ngày sau khi gửi sẽ "
     "hết hạn** (vd time send: 12h ngày 15 thì lúc 00:01 của ngày 16 sẽ hết hạn)」.\n"
     "「Template type text」r145「Ngày hết hạn = **`url_shorten.created_at` + "
     "`duration_from_delivery`** + Giờ hết hạn = **`after_day_time`**」.",
     "`db-mapping.md:263-264` — `duration_from_delivery` int「Số ngày hết hạn tính từ lúc gửi」· "
     "`after_day_time` time「Giờ hết hạn trong ngày」.\n"
     "`feature-spec.md:363` chỉ liệt kê 2 cột này, KHÔNG có công thức và KHÔNG nói mốc tính là "
     "`url_shorten.created_at`.",
     "Đây là logic tính thời điểm hết hạn mà user cuối cảm nhận trực tiếp (link còn/hết hạn). Cách "
     "hiểu cũ (0 ngày = 1 phút sau khi gửi) và cách mới (1 ngày = 00:01 ngày kế tiếp) cho kết quả "
     "lệch tới cả ngày. Spec không có công thức → tester không tính được mốc để test biên.",
     "『URL redirect — hết hạn & action』TC「Setting hết hạn kiểu DURATION → hạn = ngày tạo short link + "
     "số ngày, giờ = after_day_time」",
     "",
     "① Xác nhận công thức trên staging bằng 1 ca cụ thể (gửi 12:00 ngày 15, duration 1 ngày 00:01).\n"
     "② Bổ sung công thức vào `feature-spec.md` §2 SCR-TMT-05 và `db-mapping.md` mục "
     "`template_url_redirect`.\n"
     "③ Làm rõ ý nghĩa giá trị 0 của `duration_from_delivery` (còn hợp lệ không sau khi đổi logic)."],

    ["MT-25", "TRUNG BÌNH", W,
     "Setting số lần bấm KHÔNG áp cho friend action và LINE URL scheme — spec không ghi",
     "「Task nhỏ+ check Bug Kh」r19-r33 (bảng đối chiếu「Check lại những action nào apply với setting số "
     "lần bấm」): **CÓ apply** — multi action (r20) và trường hợp「ko có action nào」(r33). "
     "**KHÔNG apply** — friend action: open url, open link lme, friend send text, open profile LOA, "
     "open LOA add friend, call sdt, open mail (r21-r27); LINE URL scheme: share acc line, share text, "
     "open camera, open camera roll, share location (r28-r32).",
     "`feature-spec.md:631` Field Matrix #19「選択肢のタップ回数」→ `template.answer_type`.\n"
     "`db-mapping.md:589` §4.3 mô tả enum `answer_type`.\n"
     "Spec KHÔNG nói phạm vi áp dụng của tap limit theo LOẠI action.",
     "Rule này quyết định hành vi user thấy: bấm nút lần 2 có mở được URL hay không. Nếu spec không "
     "ghi, tester sẽ báo bug「đã set giới hạn 1 lần mà bấm lần 2 vẫn mở URL」trong khi đó là thiết kế. "
     "Lý do kỹ thuật: friend action/scheme là URL trực tiếp, không đi qua postback nên không đếm được.",
     "『URL redirect — hết hạn & action』TC「Setting số lần bấm của template button KHÔNG áp cho action "
     "mở URL / LINE URL scheme」· 『Panel/Button — action phía LINE user』các TC tap limit",
     "",
     "① Xác nhận lại bảng r19-r33 trên staging (13 loại action).\n"
     "② Bổ sung vào `feature-spec.md` §5 BR mới:「tap limit chỉ áp cho action đi qua postback "
     "(multi action / nút không action); friend action và LINE URL scheme không bị giới hạn」.\n"
     "③ Cân nhắc hiển thị chú thích này ngay trên UI tab 詳細設定."],

    ["MT-26", "CAO", W,
     "Gửi bằng JOB cho NHIỀU user: preview URL chỉ đúng ở user đầu tiên (+ vấn đề cache 1 phút)",
     "「Template type text」r82 note **「phía user đang hiện preview theo bảng url. Khi send nhiều user "
     "thì chỉ có 1 user send đầu t…」** · r114 cùng note · "
     "r118 note **「bên job bị cache -> khi send bị hiện preview Not found => sửa cache thời gian 1p」**.\n"
     "Expect chính của r82/r114/r118:「preview theo data trong `template_url_redirect`」cho MỌI user.",
     "`feature-spec.md:359-366` mô tả `template_url_redirect` lưu `meta_title` / `meta_image` / "
     "`meta_description` làm OGP cache.\n"
     "Spec KHÔNG mô tả cơ chế cache khi job gửi hàng loạt, cũng không nói khác biệt giữa user đầu tiên "
     "và các user sau.",
     "Đây là lỗi user cuối thấy trực tiếp: user thứ 2 trở đi thấy preview sai hoặc「Not found」. Vì là "
     "nhánh job + nhiều user nên rất dễ bỏ lọt khi test trên staging với 1 tester. Note trong TC gốc "
     "cho thấy đã từng xảy ra và có workaround cache 1 phút — không rõ đã fix hẳn chưa.",
     "『URL redirect — hết hạn & action』TC「SAU recover: gửi template cũ qua web / job / app → preview "
     "lấy theo template_url_redirect」· TC「Gửi template chứa NHIỀU URL trong đó có URL đã xóa」",
     "",
     "① Test trên staging: broadcast template có URL cho ≥5 user, kiểm tra preview của TỪNG user.\n"
     "② Hỏi Dev cơ chế cache OGP ở nhánh job (thời gian, key cache) và ghi vào `logic-spec.md`.\n"
     "③ Nếu user thứ 2 trở đi vẫn sai → raise ticket, đánh dấu TC dự kiến FAIL."],

    ["MT-27", "TRUNG BÌNH", W,
     "SpecImprove #36203: menu (...) của panel bị che và xóa panel thiếu modal confirm",
     "「Template button」r45 note **「màn hình hiển thị dc 4 panel; panel thứ 4: khi hover vào btn ... "
     "=> sẽ ko hiển thị dc sub-m…」** · r1577-r1615 (SpecImprove #36203, 01/05/2026) test menu (...) "
     "cho panel 5→10 và modal confirm khi xóa panel (cả panel đã có dữ liệu và panel rỗng, "
     "bấm キャンセル thì không xóa, xóa liên tục).",
     "`ui-spec.md` SCR-TMT-06 KHÔNG mô tả menu (...) của panel, cũng không mô tả modal confirm khi xóa "
     "panel.\n"
     "`feature-spec.md:663` BR-08 chỉ nói giới hạn số panel/nút.",
     "2 yêu cầu UX của SpecImprove #36203 chưa được ghi vào spec → lần thay đổi layout panel sau sẽ "
     "tái phát bug menu bị che. Modal confirm xóa panel là hành vi chống mất dữ liệu, cần được ghi rõ.",
     "『Panel/Button — panel & ảnh』TC「Nút (...) của panel: hover hiện menu copy / di chuyển / xóa」· "
     "TC「SpecImprove #36203: menu (...) của panel thứ 5→10 KHÔNG bị che」· "
     "TC「SpecImprove #36203: xóa panel luôn hiện modal confirm」",
     "",
     "① Xác nhận SpecImprove #36203 đã release lên PRODUCTION chưa.\n"
     "② Bổ sung vào `ui-spec.md` SCR-TMT-06: mô tả menu (...) 4 mục và modal confirm khi xóa panel.\n"
     "③ Ghi rõ hành vi lật hướng menu khi panel ở sát rìa phải."],

    ["MT-28", "THẤP", W,
     "Insert friend info BASIC ở title/content panel: design mới đã BỎ?",
     "「Template button」r59「insert các friend infor basic ⇒ **design mới bỏ đi**」(ô title) · "
     "r75「insert các friend infor basic ⇒ **design mới bỏ phần này**」(ô content).\n"
     "Nhưng r63/r79 vẫn có Expect:「code của friend info basic thay được bằng các thông tin của friend "
     "tương ứng — system name, mail, số đt, ngày sinh, địa chỉ」(tức khi GỬI vẫn replace).",
     "`feature-spec.md:337` mô tả friend info auto-insert với ví dụ "
     "`[FRIEND_INFO_system_name]`, `[FRIEND_INFO_phone]`, `[FRIEND_INFO_{hashId}]` — KHÔNG phân biệt "
     "basic và tự tạo, không nói basic bị bỏ khỏi UI insert.",
     "Lệch giữa「không còn nút insert ở UI」và「vẫn replace khi gửi」: template CŨ đã chèn code basic thì "
     "vẫn cần replace. Nếu spec không ghi, tester sẽ báo bug「thiếu nút insert friend info basic」hoặc "
     "ngược lại bỏ lọt việc code basic không được replace.",
     "『Panel/Button — tiêu đề & nội dung』TC「Insert LINE名 / 友だち情報 / emoji vào title và content」· "
     "TC「Gửi qua WEB → title/content replace đúng {name}, friend info basic...」",
     "",
     "① Xác nhận UI hiện tại: nút insert 友だち情報 ở title/content có liệt kê friend info basic không.\n"
     "② Ghi rõ vào `ui-spec.md` SCR-TMT-06 và `feature-spec.md:337`: basic bị bỏ khỏi UI insert nhưng "
     "vẫn được replace khi gửi (backward compatible).\n"
     "③ Xác nhận cùng hành vi ở ô nội dung template TEXT (có bỏ basic không)."],

    ["MT-29", "TRUNG BÌNH", W,
     "Nút KHÔNG set action nào: báo lỗi hay lưu được? — TC gốc để CẢ HAI Expect",
     "「Template button」r93「không set cả 3 loại action ⇒ **báo lỗi save success**」kèm note "
     "**「design mới cho phép ko cần chọn action nào cũng tạo dc」**— ô Expect chứa cả「báo lỗi」và "
     "「save success」.\n"
     "「Task nhỏ+ check Bug Kh」r33「ko có action nào ⇒ **có apply** (setting số lần bấm)」— hàm ý nút "
     "không action là trạng thái hợp lệ.",
     "`ui-spec.md:271`「ボタンテキスト」bắt buộc; mục Button action type (`feature-spec.md:630` Field "
     "Matrix #18) KHÔNG nói action là bắt buộc.\n"
     "`feature-spec.md` §5 không có BR nào yêu cầu nút phải có action.",
     "Ô Expect của TC gốc tự mâu thuẫn (vừa「báo lỗi」vừa「save success」) → member đọc sẽ không biết "
     "chạy theo cái nào. Note nói design MỚI cho phép, nên đã chọn「lưu được」nhưng cần Leader chốt.",
     "『Panel/Button — nút & action』TC「Nút KHÔNG set action nào → vẫn lưu được (theo design mới)」",
     "",
     "① Xác nhận trên staging: nút chỉ có ボタンテキスト, không action → bấm 保存.\n"
     "② Sửa ô Expect của sheet gốc r93 để bỏ phần「báo lỗi」đã lạc hậu.\n"
     "③ Ghi rõ vào `feature-spec.md` Field Matrix #18:「action không bắt buộc」."],

    ["MT-30", "THẤP", W,
     "Popup action friend info kiểu NGÀY: giá trị ngày đã gán bị TRỐNG khi mở lại",
     "「Modal action」r22「gán ngày hiện tại ⇒ **に当日日付を登録**」kèm note **「ở phần list action khi mở "
     "popup lên: phần ngày gán sẽ bị trống (trên step bản cũ cũng vậy)」**.",
     "`feature-spec.md` §8 xếp Action Settings vào SC-004 (shared component), chỉ tham chiếu không mô "
     "tả chi tiết.\n"
     "`db-mapping.md` `t_actions_detail` chỉ ghi「Chi tiết action (type + data JSON)」.",
     "Đây là lỗi hiển thị: admin mở lại popup thấy ô ngày trống nên tưởng chưa set, có thể vô tình lưu "
     "đè mất giá trị. Note nói「trên step bản cũ cũng vậy」→ lỗi tồn tại từ lâu ở component dùng chung "
     "SC-004, ảnh hưởng nhiều tính năng chứ không chỉ FA-010.",
     "『Panel/Button — nút & action』TC「Nhãn action friend info (text / select / ngày tháng) đúng nguyên "
     "văn」",
     "",
     "① Xác nhận trên staging: set action gán ngày cố định → lưu → mở lại popup xem ô ngày.\n"
     "② Vì là SC-004 dùng chung → raise ticket ở phạm vi shared component, không chỉ FA-010.\n"
     "③ Ghi vào Gaps của spec SC-004 (nếu có file spec riêng cho SC-004)."],

    ["MT-31", "TRUNG BÌNH", W,
     "LINE URL scheme ghi đè 2 loại action còn lại — TC gốc note「chưa apply logic 3」",
     "「Type ảnh」r93「select setting url line ⇒ **khi chọn setting này thì 2 action phía trên sẽ ko "
     "thực hiện**」· r131 cùng Expect kèm note **「chưa apply logic 3」**.\n"
     "`ui-spec.md` label của mục này là「LINE URLスキームを設定する（他アクションとの併用不可）」— "
     "「不可」nghĩa là không dùng chung được.",
     "`feature-spec.md:377` chỉ ghi「loại action (Elme/Friend Action hoặc LINE URL Scheme)」· "
     "`feature-spec.md:630` Field Matrix #18「11 giá trị post_back (0~10)」.\n"
     "Spec KHÔNG mô tả rule loại trừ giữa 3 loại action, cũng không nói ai thắng khi set cả 3.",
     "UI ghi「併用不可」nhưng hệ thống vẫn cho lưu cả 3 loại (MT-29 xác nhận set nhiều loại lưu được) → "
     "cần rule rõ ai thắng khi gửi. Note「chưa apply logic 3」cho thấy có thể chưa implement đúng, "
     "nghĩa là user có thể nhận cả 3 action.",
     "『Panel/Button — LINE URL scheme』TC「Chọn LINE URL scheme → 2 loại action còn lại KHÔNG được thực "
     "thi」",
     "",
     "① Test trên staging: nút set cả multi action + friend action + LINE URL scheme → bấm nút và "
     "đếm action nhận được.\n"
     "② Bổ sung BR vào `feature-spec.md`:「khi có LINE URL scheme thì bỏ qua multi action và friend "
     "action」(hoặc rule thật).\n"
     "③ Nếu chưa apply → raise ticket; cân nhắc chặn ngay ở UI khi lưu."],

    ["MT-32", "TRUNG BÌNH", W,
     "「友だちにテキストをシェアする」: dấu CÁCH trong text share bị đổi thành dấu +",
     "「Template button」r197「https://line.me/R/share?text={text_message} — Phía user hiện màn hình "
     "share, nhấn chọn 1 ng bạn và share ⇒ gửi message text đã setting cho ng bạn đó」kèm note "
     "**「message text chỗ dấu cách lại thành dấu +」**.",
     "`feature-spec.md` và `ui-spec.md` không mô tả cách encode text share.\n"
     "MT-12 cho thấy bộ đếm tính theo URL-encode nhưng spec cũng không ghi.",
     "Đây là lỗi encode: dấu cách phải encode thành `%20` trong query string nhưng đang thành `+` "
     "(kiểu form-encoded). Người bạn nhận được text có dấu `+` thay vì khoảng trắng → nội dung sai. "
     "Ảnh hưởng trực tiếp nội dung user cuối đọc.",
     "『Panel/Button — LINE URL scheme』TC「LINE URL scheme「友だちにテキストをシェアする」→ mở màn share "
     "text đã setting」",
     "",
     "① Test trên LINE thật: text share =「こんにちは 世界」→ xem người bạn nhận được gì.\n"
     "② Nếu còn lỗi → raise ticket (sửa encode `%20` thay vì `+`).\n"
     "③ Ghi rule encode vào `logic-spec.md` mục LINE URL scheme."],

    ["MT-33", "CAO", W,
     "「選択肢のタップ回数」lưu vào cột nào: answer_type hay carousel_action_type? UI 4 option ↔ DB mấy giá trị?",
     "「Template button」r170「default kh tạo button mới là chọn action nhiều lần **無制限**」· "
     "r171-r174「Loại 1 ⇒ **`carousel_action_type` = 1**; Loại 2 ⇒ **= 2**; Loại 3 ⇒ **= 3**; "
     "Loại 4 (無制限) ⇒ **= 0**」· r175-r176「`carousel_action_type` = 0 ⇒ hiện loại 4; = 1 ⇒ hiện loại 1」.",
     "`feature-spec.md:631` Field Matrix #19「選択肢のタップ回数」→ **`template.answer_type`** · "
     "「0=unlimited, 1=panel, 2=carousel **[Trung bình]**」.\n"
     "`db-mapping.md:70` `answer_type` tinyint「0=unlimited, 1=panel 1 click, 2=carousel 1 click」· "
     "`db-mapping.md:520` cũng map vào `answer_type`.\n"
     "`db-mapping.md:76` `carousel_action_type` tinyint「Loại action carousel (cho type=form)」và "
     "`db-mapping.md:697` xếp cột này là「Lưu nội bộ, giao diện không hiển thị trực tiếp」**[Trung bình]**.\n"
     "`feature-spec.md:841` Gaps #1 tự nhận:「UI 4 options nhưng DB `answer_type` chỉ 3 values — "
     "mapping chính xác cần xác nhận thêm」.",
     "TC gốc TRẢ LỜI đúng Gap #1 của spec: cột thật là `carousel_action_type` (4 giá trị 0/1/2/3), "
     "không phải `answer_type` (3 giá trị). Nhưng spec lại xếp `carousel_action_type` là「không hiển thị "
     "trực tiếp」→ ngược hoàn toàn. Đây là mâu thuẫn ở tầng data model: nếu Dev/QA đọc spec sẽ query sai "
     "cột khi verify, và mọi TC tap limit sẽ verify sai.",
     "『Panel/Button — 詳細設定 & tap limit』TC「Tap limit: default là 無制限; 4 lựa chọn lưu vào "
     "carousel_action_type = 1/2/3/0」· TC「Template button CŨ → suy ra loại tap limit theo "
     "carousel_action_type」",
     "",
     "① Xác nhận bằng DB thật: set từng lựa chọn tap limit rồi đọc CẢ `answer_type` và "
     "`carousel_action_type`.\n"
     "② Sửa `feature-spec.md` Field Matrix #19 và `db-mapping.md:520` sang cột đúng; cập nhật enum "
     "4 giá trị.\n"
     "③ ĐÓNG Gaps #1 của `feature-spec.md:841` sau khi xác nhận; ghi rõ `answer_type` còn dùng cho việc gì."],

    ["MT-34", "TRUNG BÌNH", W,
     "Text hiển thị trên PC / khung thông báo: cột DB nào và DEFAULT là gì? (mỗi loại một default khác)",
     "**Panel/Button** —「Template button」r178「khi user bấm quá số lần bấm sẽ hiển thị **msg default**」; "
     "spec ghi default là「タップ回数上限に達しています」cho msg vượt tap.\n"
     "**Media (video/audio)** —「Type video」r15 và「Type audio」r9「nếu ko nhập ⇒ **hiển thị như line "
     "quy định**」kèm note「save tiếng nhật lỗi」.\n"
     "**Introduce** —「Type introduce」r10「ko nhập ⇒ save success, vào edit: **tự fill "
     "LINEアプリよりご覧ください**」.\n"
     "**Ảnh thường** —「Type ảnh」r193 note「ảnh thường spec mới ko tab setting detail (chỉ có image map "
     "mới có tab này, ảnh thường, audio…)」· r231「nếu ko nhập ⇒ **tự fill default**」.",
     "`feature-spec.md:635` Field Matrix #23「PC display text (0/400)」→ `template.content` hoặc "
     "`template.text_video` · Default「**メッセージをご確認ください**」**[Thấp]**.\n"
     "`ui-spec.md:331` cũng ghi default「メッセージをご確認ください」.\n"
     "`feature-spec.md:843` Gaps #3 tự nhận chưa xác nhận cột DB.\n"
     "`db-mapping.md:689` cũng để ở mức [Thấp].",
     "Có tới **3 giá trị default khác nhau** cho cùng khái niệm「text hiển thị trên PC / thông báo」: "
     "「メッセージをご確認ください」(spec, panel), 「LINEアプリよりご覧ください」(introduce), và「theo quy định "
     "LINE」(video/audio). Chưa rõ default phụ thuộc loại template hay spec ghi sai. Thêm nữa chưa rõ "
     "tab 詳細設定 có hiện cho ảnh thường / audio hay chỉ image map.",
     "『Panel/Button — 詳細設定 & tap limit』TC「PC display text ... default và giá trị tự nhập」· "
     "『Media — ảnh』TC「Tab 詳細設定 của ảnh: text hiển thị ngoài màn list LINE user」· "
     "『Media — video & audio』TC「Audio / Video: tab 詳細設定」· "
     "『Template legacy & tương thích』TC「紹介文: ô パソコン版LINEアプリ・通知欄の表示テキスト để trống」",
     "",
     "① Với TỪNG loại template (panel, ảnh thường, image map, video, audio, introduce): kiểm tra tab "
     "詳細設定 có hiện không và default là gì; đọc cột DB thật.\n"
     "② Lập bảng「loại template ↔ có tab 詳細設定 ↔ cột DB ↔ default」và đưa vào `feature-spec.md`.\n"
     "③ ĐÓNG Gaps #3 (`feature-spec.md:843`); xác nhận riêng lỗi「save tiếng nhật lỗi」ở video/audio."],

    ["MT-35", "TRUNG BÌNH", W,
     "Thiếu con số giới hạn ký tự cho ラベル / タイトル của button ảnh và text nút quick reply",
     "「Template button」r602-r617「Validate Label image ラベル」và「Validate title image タイトル」— TC gốc "
     "CHỈ có tiêu đề nhóm, **không ghi con số giới hạn và không ghi nguyên văn msg lỗi**.\n"
     "r819-r820「check validate」của quick reply cũng chỉ có tiêu đề.\n"
     "r818「Nhập text Nhật 5000 ký tự」(ô nội dung quick reply) là con số duy nhất có.",
     "`ui-spec.md` SCR-TMT-06 mục『Điểm chưa rõ』#5 —「UI chưa mô tả chi tiết sub-types Panel khác ngoài "
     "Standard. Chỉ quan sát được「スタンダード」, chưa mô tả「カラーボタン」「画像」「クイックリプライ」」"
     "(`feature-spec.md:849` Gaps #5).\n"
     "`db-mapping.md:151-152` `tmp_button.title` / `.text` varchar(256) nhưng không ghi giới hạn UI cho "
     "sub-type 画像.",
     "**Vùng mù chung của cả TC và spec**: không nguồn nào có con số giới hạn cho ラベル/タイトル của "
     "button ảnh và text nút quick reply. Member sẽ không biết test biên nào. Đây là loại lệch cần bổ "
     "sung ở CẢ 2 phía.",
     "『Button ảnh — label & title』TC「Validate ラベル và タイトル của button ảnh」· "
     "『Quick reply』TC「Validate nội dung / text nút của quick reply」",
     "",
     "① Trên staging, nhập tăng dần vào từng ô của sub-type 画像 và クイックリプライ để tìm mốc thật và "
     "đọc nguyên văn msg lỗi.\n"
     "② Bổ sung vào `ui-spec.md` bảng field cho 3 sub-type còn thiếu (カラーボタン / 画像 / クイックリプライ) "
     "→ ĐÓNG Gaps #5.\n"
     "③ Cập nhật expected của 2 TC sau khi có con số."],

    ["MT-36", "THẤP", W,
     "Setting kích thước ảnh (lớn/trung/bé): design mới đã BỎ?",
     "「Type ảnh」r15-r17 test đủ 3 cỡ (default lớn / trung / bé) với Expect「send cho user hiển thị cỡ "
     "tương ứng」kèm note r16「bên user: sẽ ko sát viền màn hình => này do line hiển thị」.\n"
     "Nhưng「Type ảnh」r226 (khối Edit) note **「design mới bỏ phần này」** cho mục edit size ảnh.",
     "`ui-spec.md` SCR-TMT-08 và `feature-spec.md:443` mô tả upload media nhưng KHÔNG có mục setting "
     "kích thước ảnh 3 cỡ.\n"
     "`db-mapping.md` không có cột nào rõ ràng cho size ảnh hiển thị.",
     "TC gốc tự mâu thuẫn: khối tạo mới vẫn test 3 cỡ, khối edit nói design mới đã bỏ. Nếu tính năng "
     "đã bỏ mà TC vẫn còn thì member sẽ tìm không thấy UI và báo bug oan; nếu chưa bỏ mà spec không "
     "ghi thì bỏ lọt 1 field.",
     "『Media — ảnh』TC「Setting kích thước ảnh hiển thị phía LINE user (lớn / trung / bé)」· "
     "TC「Edit template ảnh: đổi ảnh / cỡ / hình dạng / tab detail」",
     "",
     "① Kiểm tra UI hiện tại của màn tạo/sửa template ảnh: còn mục chọn 3 cỡ không.\n"
     "② Nếu còn → bổ sung field vào `ui-spec.md` SCR-TMT-08 và Field Matrix + cột DB.\n"
     "③ Nếu đã bỏ → xóa/đánh dấu lạc hậu TC tương ứng và ghi vào lịch sử spec."],

    ["MT-37", "TRUNG BÌNH", W,
     "Update ảnh khi đang bật image map → tự chuyển về ảnh thường, MẤT toàn bộ area đã cấu hình",
     "「Type ảnh」r32「button update ảnh ⇒ hiển thị popup update ảnh; update sang ảnh khác ⇒ **chuyển về "
     "dạng ảnh thường (checkbox dùng image map ko check)**」.",
     "`feature-spec.md:455-460` mô tả Image Map khi `is_setting_image_map = 1` nhưng KHÔNG mô tả hành "
     "vi khi đổi ảnh gốc.\n"
     "`feature-spec.md:670` BR-14「Update template → xoá TẤT CẢ relationships cũ → tạo lại mới」— gần "
     "nhưng không nói rõ trường hợp này.",
     "Đây là hành vi MẤT DỮ LIỆU không cảnh báo: admin đã vẽ 6 area + set action, đổi ảnh một cái là "
     "mất hết mà không có confirm (khác với việc đổi option area thì CÓ alert — xem MT chung với "
     "「現在設定されているタップ時アクションが全て削除されますが」). Không nhất quán về UX.",
     "『Media — image map』TC「Update ảnh khác khi đang bật image map → template chuyển về dạng ảnh "
     "thường」· TC「Đổi giữa 3 option area → hiện alert cảnh báo mất action」",
     "",
     "① Xác nhận hành vi trên staging và xem có alert nào không.\n"
     "② Chốt: nên hiện alert giống khi đổi option area, hay giữ nguyên hành vi hiện tại.\n"
     "③ Ghi rõ vào `feature-spec.md` §2 SCR-TMT-08 dù chốt theo hướng nào."],

    ["MT-38", "THẤP", W,
     "Ô nhập TOẠ ĐỘ area image map thủ công: TC gốc note「bỏ phần này」",
     "「Type ảnh」r81「check nhập thông tin tọa độ ⇒ trên ảnh hiển thị vùng đỏ theo tọa độ nhập」kèm note "
     "**「bỏ phần này」** · r125 (khối chọn từ template) cùng nội dung, note tương tự.",
     "`feature-spec.md:641` Field Matrix #28「Image map areas → `image_map_items.x, .y, .width, .height` "
     "· Validation: x,y >= 0, w,h >= 1」→ spec ghi như thể user nhập toạ độ được.\n"
     "`feature-spec.md:664` BR-11「Area: x,y >= 0, width,height >= 1, tất cả numeric ⇒ Error "
     "「エリア{N}: 領域設定が間違っています」」.",
     "Nếu ô nhập toạ độ đã bị bỏ khỏi UI (chỉ còn kéo-thả) thì validate BR-11 và msg lỗi "
     "「エリア{N}: 領域設定が間違っています」không còn đường nào trigger từ UI → tester không test được. "
     "Cần biết validate còn dùng cho API hay đã chết.",
     "『Media — image map』TC「Option 手動で設定する: thêm area bằng kéo-thả, lưu area đúng vị trí」· "
     "TC「Edit area: đổi kích thước, area chèn nhau thì tính theo area PHÍA SAU」",
     "",
     "① Kiểm tra UI popup chọn vùng tap: còn ô nhập toạ độ x/y/width/height không.\n"
     "② Nếu đã bỏ → ghi rõ vào `feature-spec.md` Field Matrix #28 và BR-11 rằng validate chỉ áp ở "
     "tầng API/server.\n"
     "③ Xác nhận msg「エリア{N}: 領域設定が間違っています」còn khả năng xuất hiện không."],

    ["MT-39", "CAO", W,
     "Bug #31454: dedupe action image map theo ngưỡng 3 giây + nhánh「back trình duyệt 2 lần」chưa fix",
     "「Type ảnh」r415 (Bug #31454, 22/08/2025「Không nhấn action gì nhưng friend vẫn nhận được message」; "
     "nguyên nhân「khi friend access vào trình duyệt nó tự reload lại gây action」; cách fix「redirect "
     "sang 1 trang action done」) · r416「redirect tiếp sang 1 trang action done "
     "**このページを閉じてください。**」· r417「**nếu 2 callback cách nhau <3s thì chỉ send 1 action; "
     "2 callback cách nhau >3s thì mỗi callback send 1 action**」· "
     "r422 note **「case user nhấn back trình duyệt 2 lần về màn url action thì vẫn đang action tiếp」**.",
     "`feature-spec.md` và `logic-spec.md` KHÔNG mô tả trang action done, KHÔNG có ngưỡng dedupe 3 giây, "
     "KHÔNG mô tả cơ chế chống action lặp khi reload trình duyệt.",
     "Đây là bug user cuối gặp trực tiếp (nhận tin/được gắn tag mà không bấm gì) và cơ chế fix (redirect "
     "+ dedupe 3s) là logic nghiệp vụ quan trọng. Ngưỡng 3 giây là con số magic không ghi ở đâu. "
     "Quan trọng hơn: note cho thấy nhánh「back 2 lần」VẪN CÒN LỖI → cần biết đã fix chưa.",
     "『Media — image map』TC「Bug #31454: user bấm image map → redirect sang trang action done, "
     "2 callback cách nhau <3s chỉ gửi 1 action」· TC「Bug #31454 trên iOS...」· TC「...trên Android...」",
     "",
     "① Xác nhận trên PRODUCTION: bấm area image map, đo hành vi ở mốc <3s và >3s.\n"
     "② Test riêng nhánh「back trình duyệt 2 lần」; nếu còn action lặp → raise ticket.\n"
     "③ Bổ sung vào `logic-spec.md`: trang action done, nội dung「このページを閉じてください。」và ngưỡng "
     "dedupe 3 giây (kèm lý do chọn 3s)."],

    ["MT-40", "TRUNG BÌNH", W,
     "Template video KHÔNG có thumbnail: lưu được nhưng user KHÔNG xem được video",
     "「Type video」r17「temp có video nhưng ko có ảnh thumbnail ⇒ check save và send」kèm note "
     "**「save ok send cho user thì user ko xem dc」** · r18「temp có ảnh thumbnail nhưng ko có video ⇒ "
     "phải chọn video mới ra dc giao diện type video có ảnh thumbnail」.",
     "`ui-spec.md` SCR-TMT-08 và `feature-spec.md:443-452` mô tả upload video và "
     "「Thumbnail do user upload hoặc **default**」— tức spec nói CÓ thumbnail default.\n"
     "`db-mapping.md` `template.thumbnail_path` nullable.",
     "Spec nói có thumbnail default nhưng TC cho thấy không có thumbnail thì user không xem được video "
     "→ hoặc default không hoạt động, hoặc spec sai. Đây là lỗi user cuối nghiêm trọng (nhận tin nhưng "
     "không phát được video) mà hệ thống vẫn cho lưu → nên chặn ở validate.",
     "『Media — video & audio』TC「Video: lưu khi CÓ video mà KHÔNG có thumbnail → lưu được nhưng user "
     "không xem được」",
     "",
     "① Xác nhận trên staging: lưu template video không thumbnail → gửi → thử phát trên LINE.\n"
     "② Chốt: có bắt buộc thumbnail (chặn lưu) hay dùng thumbnail default.\n"
     "③ Sửa `feature-spec.md:449` nếu thumbnail default không tồn tại; nếu chốt bắt buộc → raise ticket "
     "và sửa expected TC."],

    ["MT-41", "TRUNG BÌNH", W,
     "Màn Location: 3 lỗi UI được ghi trong note TC (search không ra giữa map, nút không phản ứng, edit không hiện map)",
     "「Type location」r7-r8 note **「bug: vị trí đc search chưa hiển thị ra giữa map」** và "
     "**「case coppy và paste vào mục search => ấn e…」** · r9「chưa chọn vị trí nào click button ⇒ "
     "required chọn vị trí」kèm note **「đang ko có phản ứng nào」** · r39「ko edit gì save ⇒ save success」"
     "kèm note **「chưa hiển thị dc map đúng thông tin đã chọn lúc tạo」**.",
     "`ui-spec.md` SCR-TMT-10 mô tả Google Maps embed + search box + nút xác nhận, và mục『Điểm chưa "
     "rõ』#7「Google Maps lỗi — cần API key hợp lệ」**[Trung bình]**.\n"
     "Spec KHÔNG mô tả hành vi mong đợi khi search / khi chưa chọn vị trí / khi mở lại màn edit.",
     "3 note này là 3 bug UI đã được ghi nhận nhưng không rõ đã fix chưa. Nếu member chạy TC theo "
     "Expect (hành vi đúng) thì cả 3 sẽ FAIL; cần biết trước để phân biệt「bug mới」và「bug đã biết」. "
     "Ảnh hưởng người dùng: chọn sai vị trí gửi cho khách.",
     "『Location』TC「Khung search vị trí...」· TC「Bấm nút lấy thông tin vị trí pin khi CHƯA chọn vị "
     "trí」· TC「Edit template location (mới và cũ)」",
     "",
     "① Test lại 3 nhánh trên staging với Google Maps API key hợp lệ.\n"
     "② Với nhánh nào còn lỗi → raise ticket và đánh dấu TC「dự kiến FAIL」.\n"
     "③ Bổ sung hành vi mong đợi vào `ui-spec.md` SCR-TMT-10; ĐÓNG Điểm chưa rõ #7 nếu key đã ổn."],

    ["MT-42", "TRUNG BÌNH", W,
     "位置情報タイトル / 位置情報詳細: auto-fill default, auto-truncate 90 ký tự, xuống dòng lệch web ↔ LINE",
     "「Type location」r17「ko nhập ⇒ **ko required**; nếu lưu khi vào edit sẽ **tự fill data: 位置情報。** "
     "(bản cũ như vậy)」· r18「nhập quá 90 ký tự ⇒ **tự cắt**」· "
     "r20「ko nhập ⇒ ko required; khi vào edit **tự fill クリックして地図を開いてください。。** vào ô search, "
     "trường 位置情報詳細 và bên map nhỏ」· r21「nhập quá 90 ký tự ⇒ **tự cắt**」· "
     "r23「nhập data xuống dòng ⇒ **user: sẽ ko xuống dòng; vào edit: trường này vẫn xuống dòng**」· "
     "r29-r32 mô tả 4 tổ hợp auto-fill, trong đó r30/r32 note「chưa tự fill vào detail」.",
     "`ui-spec.md:408-409`「位置情報タイトル」và「位置情報詳細」Max 90 ký tự, **Suy luận không bắt buộc** — "
     "KHÔNG có default, KHÔNG nói auto-truncate.\n"
     "`feature-spec.md:645-646` Field Matrix #33/#34 → `template.content` (suy luận) **[Thấp]**.\n"
     "`feature-spec.md:842` Gaps #2 tự nhận chưa xác nhận cột DB.",
     "TC lấp đúng Gap #2 và thêm 3 rule spec bỏ sót: default auto-fill (2 chuỗi tiếng Nhật cụ thể), "
     "auto-truncate thay vì báo lỗi (khác hẳn các ô khác trong FA-010 đều báo lỗi khi vượt), và lệch "
     "xuống dòng web ↔ LINE. Riêng r30/r32 note cho thấy auto-fill detail CHƯA hoạt động ở 2 tổ hợp.",
     "『Location』TC「位置情報タイトル: ... để trống thì auto-fill 位置情報。; > 90 ký tự TỰ CẮT」· "
     "TC「位置情報詳細: ... auto-fill クリックして地図を開いてください。。」· "
     "TC「位置情報詳細 nhập XUỐNG DÒNG → phía LINE user KHÔNG xuống dòng」· "
     "TC「Lưu template location với 4 tổ hợp title/detail/pin」",
     "",
     "① Xác nhận cột DB thật của title/detail (đọc `template.content` của 1 template location mẫu) → "
     "ĐÓNG Gaps #2.\n"
     "② Bổ sung vào `ui-spec.md:408-409`: default auto-fill (nguyên văn 2 chuỗi), hành vi auto-truncate, "
     "và lệch xuống dòng.\n"
     "③ Test riêng 2 tổ hợp r30/r32; nếu auto-fill detail chưa chạy → raise ticket."],

    ["MT-43", "THẤP", W,
     "Template 紹介文 (legacy): LINE ID không validate định dạng「@」, xuống dòng lệch web ↔ LINE",
     "「Type introduce」r4「edit LINE ID · ko nhập ⇒ **required**」· r5「nhập tiếng nhật ⇒ **save "
     "success**」· r6「**nhập thiếu「@」⇒ save success**」· "
     "r15「chat 11 ⇒ data trường 紹介文 sẽ **ko xuống dòng**」· r16「bên user ⇒ data trường 紹介文 "
     "**sẽ xuống dòng như khi nhập data**」· r17「user click ⇒ hiển thị mh add bot」.",
     "`feature-spec.md:51` xếp `introduction` vào「3 loại legacy (question, introduction, group)」.\n"
     "`db-mapping.md:30` `tmp_introduction`「Dữ liệu template type=introduction (legacy)」— KHÔNG mô tả "
     "validate LINE ID, không mô tả hành vi xuống dòng.\n"
     "`ui-spec.md` KHÔNG có màn hình nào cho loại 紹介文.",
     "Loại legacy nhưng vẫn còn dữ liệu khách hàng và vẫn gửi được. LINE ID sai định dạng (thiếu @, "
     "text Nhật) vẫn lưu được → link add bot sẽ lỗi phía user. Spec không có màn hình cho loại này → "
     "vùng mù hoàn toàn.",
     "『Template legacy & tương thích』TC「Template loại 紹介文 (introduce) cũ: hiện đủ dữ liệu, edit "
     "LINE ID và 紹介文 lưu đúng」· TC「紹介文: chat 1:1 KHÔNG xuống dòng, phía LINE user CÓ xuống dòng」",
     "",
     "① Xác nhận loại 紹介文 còn tạo mới được hay chỉ còn edit template cũ.\n"
     "② Bổ sung 1 mục ngắn về loại legacy 紹介文 vào `ui-spec.md` / `feature-spec.md` (field, validate, "
     "hành vi gửi).\n"
     "③ Chốt có nên validate định dạng LINE ID (đề xuất: có, vì link lỗi ảnh hưởng user)."],

    ["MT-44", "CAO", W,
     "Phạm vi áp dụng của 送信オプション delay message — spec nói chỉ quick test, TC nói rộng hơn nhưng loại trừ send all/scenario",
     "「Improve list template」r493「Tùy chọn gửi (メッセージを1通ずつ数秒遅延させて送信する) ⇒ "
     "**ko apply với send all / scenario**; chat 11: web send send test: msg đầu tiên web send — "
     "các msg sau fill vào DB bảng random_msg để job send」· "
     "r526-r537 test nhánh CÓ apply: send web (chat 1:1, send test, friend list, tag), remind gửi ngay, "
     "resend message lỗi, talklist · r538-r539「**KO APPLY - vẫn send all cùng 1 lúc - ko bị duplicate**」· "
     "r541-r561 CÓ apply cho action: button, image map, rich menu, form, auto reply, add friend.",
     "`feature-spec.md` §7 Background Jobs —「Delay test message · Trigger: **Quick test template group** "
     "có `is_delay_message=1`」· «Lưu ý: Đây không phải core background job của tính năng Template mà là "
     "**cơ chế hỗ trợ cho group template test**».\n"
     "`logic-spec.md:245` cũng chỉ nói「Khi template group có delay message enabled...」không nêu phạm vi.",
     "Spec thu hẹp delay message thành「chỉ dùng cho quick test」trong khi corpus cho thấy nó áp cho "
     "hàng loạt luồng gửi thật (chat 1:1, action, rich menu, form, auto reply, remind) và **loại trừ** "
     "đúng 2 luồng lớn nhất (send all, scenario). Hiểu sai phạm vi = bỏ lọt toàn bộ regression của "
     "Bug KH #38987 ở nhánh action/remind (chính là vùng fix #2 mà TCS tool không phủ).",
     "『Delay message』TC「Delay ON nhưng KHÔNG áp cho send all và scenario」· "
     "TC「Delay ON áp cho template gắn trong ACTION: button, image map, rich menu, form, auto reply, "
     "add friend」· TC「Delay ON + gửi qua WEB...」· TC「Delay ON + REMIND...」",
     "",
     "① Lập bảng đầy đủ「luồng gửi ↔ delay có/không áp」và xác nhận từng dòng trên staging.\n"
     "② Sửa `feature-spec.md` §7: nâng delay message thành cơ chế có phạm vi rộng, kèm bảng ở bước ①, "
     "và ghi rõ lý do send all/scenario bị loại trừ.\n"
     "③ Xác nhận `logic-spec.md:245` và bổ sung `HelperService::sendAction` vào danh sách nơi sinh bản "
     "ghi `send_random_messages`."],

    ["MT-45", "CAO", W,
     "Bug KH #38987: quy tắc chuẩn hoá send_random_messages.bot_profile_id — spec chỉ liệt kê cột",
     "「Tcs #38987」r8-r9 (NEW-56/NEW-62)「Cột `bot_profile_id` được **chuẩn hoá theo quy tắc profile** "
     "khi ghi bản ghi hàng đợi」·「Chọn profile **mặc định** thì bản ghi hàng đợi lưu `bot_profile_id` "
     "**rỗng/NULL**」· r29 (NEW-63)「Chọn profile **tuỳ chỉnh** thì lưu **đúng ID profile đó**」· "
     "r33 (TC-DLY-011)「Hành vi bám đúng cờ **`is_default` tại thời điểm gửi**, không hardcode id」· "
     "r41 (TC-DLYJ-007) xác nhận cùng quy tắc cho bản ghi sinh từ `HelperService::sendAction`.",
     "`db-mapping.md:390` — `send_random_messages.bot_profile_id` int(11) nullable「**Profile bot gửi**」"
     "— chỉ 1 dòng mô tả, KHÔNG có quy tắc NULL cho profile mặc định.\n"
     "`feature-spec.md` §7 và `logic-spec.md:384` mô tả delay nhưng KHÔNG nhắc `bot_profile_id`.",
     "Chính quy tắc này là ROOT CAUSE của Bug KH #38987 (tin thứ 2 hiện「アカウント名 from アカウント名」). "
     "Spec chỉ ghi tên cột nên không ai biết NULL nghĩa là「dùng profile mặc định, không gắn nhãn "
     "sender」. Nếu không ghi rõ, lần refactor sau rất dễ ghi id của profile mặc định vào cột này và "
     "bug tái phát.",
     "『Delay message』TC「Bug KH #38987: profile MẶC ĐỊNH + delay ON → mọi tin cùng 1 tên người gửi」· "
     "TC「...chống over-fix: profile TUỲ CHỈNH...」· TC「...đổi người gửi giữa 2 lần quick test」· "
     "TC「...đổi cờ is_default...」· TC「Job xử lý bản ghi delay sinh từ multi action / remind」",
     "",
     "① Ghi quy tắc vào `db-mapping.md` mục `send_random_messages`:「NULL = profile mặc định (không gắn "
     "nhãn sender); có giá trị = id profile tuỳ chỉnh」.\n"
     "② Bổ sung vào `logic-spec.md` mô tả nơi chuẩn hoá (`TemplateService::sendTestTemplate` và "
     "`HelperService::sendAction`) + rule query cờ `is_default` runtime.\n"
     "③ Xác nhận trạng thái release của bản fix #38987 trên PRODUCTION trước khi chạy bộ TC này."],

    ["MT-46", "TRUNG BÌNH", W,
     "Xóa template được tạo TẠI màn send all: TC note「chưa thấy xóa trong DB」",
     "「Template type text」r205「check xóa ⇒ **xóa trong bảng temp record tương ứng**」kèm note "
     "**「chưa thấy xóa trong DB」** · r210 (nhánh clone) cùng note.\n"
     "Các nhánh scenario (r229/r252) và remind (r276/r299) có cùng Expect nhưng KHÔNG có note.",
     "`feature-spec.md:660` BR-06「**Hard delete** template (không soft delete) + cleanup ActionDetail, "
     "SendRandomMessage, TemplateMappingTable」.\n"
     "`feature-spec.md:664` BR-12 mô tả position; KHÔNG có ngoại lệ cho template nội bộ "
     "(`category_id` âm: -11 / -111 / -99).",
     "Nếu template nội bộ của send all không bị xóa khỏi DB thì bảng `template` phình dần theo mỗi "
     "broadcast bị xóa, và có nguy cơ template mồ côi bị gửi lại. Note chỉ xuất hiện ở nhánh send all "
     "(không ở scenario/remind) nên khả năng là lỗi riêng của nhánh này.",
     "『Gửi template từ màn khác』TC「Tạo template TẠI màn send all → lưu category_id = -11, name = "
     "broadcast; edit và xóa đúng」",
     "",
     "① Test trên staging: tạo template tại màn send all → xóa → query bảng `template` theo "
     "`category_id = -11`.\n"
     "② Nếu bản ghi còn → raise ticket (rò rỉ dữ liệu template nội bộ).\n"
     "③ Bổ sung vào `feature-spec.md` §5 mô tả vòng đời template nội bộ (`category_id` âm): khi nào "
     "tạo, khi nào xóa."],

    ["MT-47", "TRUNG BÌNH", W,
     "Bảng capture_templates: cấu trúc cột content (2 kiểu lưu text/encode) — spec chỉ ghi 1 dòng",
     "「Template button」r1491「Check recover bảng `capture_templates` (ở Database message) — job recover "
     "bảng `capture_templates` **type = 2** cột `content`, check `thumbnail_path` có dạng "
     "**「//ext-media-s…」**」· r1492「**Case 1: job lưu kiểu text thường**」· "
     "r1495「**Case 2: web lưu kiểu encode**」· r1493/r1496 kèm mẫu `content` dạng JSON "
     "`{\"type_button\":1,\"data\":[{\"buttons\":[{\"label\":\"詳細をみる\",...}]}]}` · "
     "r1494/r1497「Check random một vài `template_capture_id` khác」.",
     "`db-mapping.md:44` — `capture_templates`「**Snapshot template cho version control**」· Audit · "
     "`capture_templates.template_id` → `template.id`.\n"
     "Spec KHÔNG mô tả cột `type`, KHÔNG mô tả cấu trúc `content`, KHÔNG nói có 2 kiểu lưu "
     "(text thường từ job vs encode từ web).",
     "Bảng này là nơi Bug KH #33911 phải recover, và có tới 2 định dạng `content` khác nhau tuỳ nguồn "
     "ghi (job vs web) → job recover phải xử lý cả 2. Spec 1 dòng là không đủ để QA verify hoặc để Dev "
     "sau này viết migration an toàn.",
     "『Recover dữ liệu lỗi』TC「Bug KH #33911: recover bảng capture_templates (type = 2) — "
     "thumbnail_path dạng //ext-media-s...」",
     "",
     "① Bổ sung mục chi tiết cho `capture_templates` vào `db-mapping.md`: danh sách cột, ý nghĩa `type`, "
     "cấu trúc `content` cho từng kiểu lưu.\n"
     "② Ghi rõ nguồn ghi nào tạo kiểu text thường, nguồn nào tạo kiểu encode.\n"
     "③ Xác nhận job recover đã xử lý cả 2 kiểu (test lại trên PRODUCTION theo TC)."],

    ["MT-48", "CAO", W,
     "Bug KH #36384: validate tham số URL (template_child_id) và chặn cross-account ở màn EDIT",
     "「Improve list template」r573 (Bug KH #36384, 12/05/2026「Click vào template folder '定期配信用' hiển "
     "thị error」; nguyên nhân「user sử dụng link này để edit ⇒ **`template_child_id` bị lấy sai** ⇒ "
     "content của template group bị lưu sai `(13305887,13305944/?utm_source=line)`」) · "
     "r630 (TC-NEW-01)「content của template_group X = **chuỗi int CSV**, không chứa `/?utm_source` hay "
     "bất kỳ ký tự non-numeric nào」· r631 (TC-NEW-08)「storeTemplate / updateTemplate / cloneTemplate "
     "cũng **ép int** đúng」· r632 (TC-NEW-04)「user bot A paste URL edit template của bot B ⇒ "
     "**từ chối access** (redirect / 403 / message lỗi), không corrupt data bot B」.",
     "`feature-spec.md:657` BR-03「Bot ID verification: **`store()`** kiểm tra `botIdCurrent == "
     "getBotId()`」— chỉ ở `store()`, không nói gì về màn EDIT (`EP-03`, `EP-05`).\n"
     "`api-spec.md` EP-03/EP-05 không mô tả validate tham số hay kiểm tra chủ sở hữu.\n"
     "`feature-spec.md` không có mục nào về validate/sanitize tham số URL.",
     "2 rủi ro: (a) tham số URL không ép int làm CORRUPT `template.content` của group (bug KH đã xảy "
     "ra thật, gây error khi mở folder); (b) màn edit không kiểm tra chủ sở hữu → user bot A có thể sửa "
     "template bot B (rủi ro bảo mật liên tài khoản). Cả 2 đều không có trong spec.",
     "『Recover dữ liệu lỗi』TC「Bug KH #36384: URL edit template con chứa /?utm_source=... → "
     "template_child_id phải ép int」· TC「storeTemplate / updateTemplate / cloneTemplate cũng phải ép "
     "int」· TC「bảo mật: user bot A paste URL edit template của bot B → bị từ chối」",
     "",
     "① Xác nhận bản fix #36384 đã release chưa và có ép int ở cả 3 function (store/update/clone).\n"
     "② Test riêng nhánh cross-account (TC-NEW-04) — nếu load được template bot B thì raise ticket "
     "SECURITY ưu tiên cao.\n"
     "③ Bổ sung vào `feature-spec.md` §5: BR mới về sanitize tham số URL và kiểm tra chủ sở hữu ở "
     "TẤT CẢ endpoint đọc/ghi template (không chỉ `store()`)."],

    ["MT-49", "CAO", W,
     "Phân quyền staff: spec tự nhận「không thấy trong controller」— có enforce ở tầng API không?",
     "「Template button」r1618「Account staff **có quyền** template: click/hover vào hiển thị được thông "
     "tin thao tác panel」· r1619「Account staff **không quyền** template: Bot có 1 staff KHÔNG được phân "
     "quyền template」(chỉ có tiêu đề, không ghi Expect chi tiết).\n"
     "「Improve list template」r492「Test lại trên account staff」· "
     "「Tcs #38987」r17 (NEW-2)「Nhân viên (staff) được cấp quyền màn template vẫn gửi thử được」.",
     "`feature-spec.md:40` —「Staff · Truy cập template theo quyền được Admin phân · **kiểm tra ở "
     "middleware level [Trung bình]**」.\n"
     "`feature-spec.md:807` —「Staff permission: Kiểm tra ở middleware level (**không thấy trong "
     "controller**) **[Trung bình]**」.\n"
     "`api-spec.md` mục Middleware chỉ liệt kê `web`, `NotifyChatworkRequestTimeSlow`, "
     "`LogRequestMultipart` — KHÔNG có middleware phân quyền theo màn.",
     "Spec TỰ đánh dấu [Trung bình] và nói không thấy kiểm tra trong controller; danh sách middleware "
     "cũng không có middleware phân quyền. Corpus chỉ có TC ở mức tiêu đề cho nhánh「không có quyền」→ "
     "**vùng mù ở cả 2 phía**. Đây là rủi ro bảo mật kiểu「UI ẩn menu nhưng API vẫn cho gọi」.",
     "『Phân quyền & môi trường』TC「Staff ĐƯỢC phân quyền template → thao tác đầy đủ」· "
     "TC「Staff KHÔNG được phân quyền template → chặn cả ở UI và ở tầng API」",
     "",
     "① Hỏi Dev: middleware/cơ chế nào enforce quyền màn template; áp cho những route nào.\n"
     "② Test tầng API bằng staff không quyền: gọi trực tiếp `POST /ajax/init-template` và "
     "`POST /ajax/template-v2/save-template` → nếu ghi được dữ liệu thì raise ticket SECURITY.\n"
     "③ Bổ sung vào `api-spec.md` mục Middleware và `feature-spec.md:807`; nâng mức tin cậy sau khi "
     "xác nhận. Rà cả các màn sibling dùng chung lưới phân quyền."],
]
