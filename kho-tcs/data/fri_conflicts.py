# -*- coding: utf-8 -*-
"""FA-015 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features/admin/friend-information/.

Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (2026-08-20).
Cột "QUYẾT ĐỊNH CỦA LEADER" để TRỐNG — không tự chọn bên nào.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "Trường kiểu 画像 / PDF: tạo được nhưng có hiển thị ở danh sách theo folder không?",
     "Corpus coi 画像 và PDF là kiểu dùng bình thường:\n"
     "• r201-r202 (Bug KH #36201, 05/2026): 'tạo friend info type image/pdf ⇒ tạo thành công, sau khi tạo "
     "ĐỨNG TẠI FOLDER vừa tạo, gán/tạo value cho friend info thành công'\n"
     "• r326-r327, r341-r342 (#38591, 07/2026): thêm value type ảnh/pdf ⇒ 'Count +1 tại cột 回答人数' — "
     "tức là 2 kiểu này CÓ dòng trên màn list để đọc cột 回答人数\n"
     "• r493, r495: xóa rồi add lại value cho ảnh/pdf ⇒ count +1",
     "web/logic-spec.md:62 — 'getFriendInfoSettingByFolderId() (dòng 85-90) chỉ query "
     "whereIn(type_data, [1,2,3,6]) — LOẠI TRỪ type 4 (image) và 5 (file) khỏi danh sách. Tin cậy: Cao'\n"
     "feature-spec.md §BR-02 — type 4/5: 'Bị ẩn khỏi danh sách folder (whereIn loại trừ)'\n"
     "feature-spec.md §2 SCR-FRI-01 (luồng EP-06) — 'SELECT friend_information_setting WHERE ... "
     "type_data IN (1,2,3,6)'\n"
     "ui-spec.md:95 — dropdown 情報タイプ VẪN có đủ 6 lựa chọn gồm「画像」「PDF」\n"
     "feature-spec.md §9 Gap #1 + Open Question 1 — 'Liệu đây là design intention hay bug?'",
     "Nếu spec đúng: tạo xong trường ảnh/PDF sẽ KHÔNG hiện ở danh sách folder → không có dòng để đọc "
     "回答人数, không click vào được, không sửa/xóa qua UI → toàn bộ TC corpus về ảnh/PDF sai kỳ vọng.\n"
     "Nếu corpus đúng: spec sai ở 3 chỗ và query thực tế phải gồm type 4,5.\n"
     "SPEC CŨNG TỰ MÂU THUẪN: UI cho chọn 6 kiểu nhưng query chỉ lấy 4 kiểu.",
     "TC-FRI-115 → TC-FRI-120 (nhóm「Info kiểu Ảnh & PDF」) · TC-FRI-179 → TC-FRI-182 (bộ đếm 回答人数 — "
     "ảnh/pdf nằm trong Dữ liệu test 15 trường)",
     "",
     "① Chốt: 画像/PDF có hiển thị ở danh sách theo folder không.\n"
     "② Nếu KHÔNG hiển thị → sửa ui-spec.md:95 (bỏ 2 lựa chọn khỏi dropdown hoặc ghi rõ hệ quả), "
     "và sửa expected của TC-FRI-115/116 + bỏ ảnh/pdf khỏi Dữ liệu test của TC-FRI-179 → TC-FRI-182.\n"
     "③ Nếu CÓ hiển thị → đây là BUG code (query thiếu type 4,5); sửa logic-spec.md:62, "
     "feature-spec BR-02 và §2, đóng Gap #1 + Open Question 1."],

    ["MT-02", "CAO", W,
     "Xóa trắng trường 都道府県名: có xóa hẳn dòng dữ liệu và giảm 回答人数 như 4 trường địa chỉ kia không?",
     "RV-02 (r477, AI Review bổ sung trong khối #38591, 07/2026): 'Xóa trắng trường ĐỊA CHỈ "
     "(郵便番号/都道府県/市区町村/町名番地/建物名) → CŨNG XÓA HẲN DÒNG, count -1' — gộp cả 5 trường "
     "địa chỉ vào cùng 1 hành vi.\n"
     "r403-r461 (#38591): xóa value ở màn 友だち詳細/right bar cho 都道府県名 ⇒ 'Count -1 tại cột 回答人数, "
     "click vào 回答人数 không hiển thị friend vừa xóa'",
     "feature-spec.md §BR-10 + web/logic-spec.md §BR-10 — 都道府県名 (d_6) lưu ở `line_user.province` "
     "(cùng nhóm với 4 trường cơ bản), còn -7/-8/-9/-10 lưu ở `friend_information_value`\n"
     "feature-spec.md §2 (luồng EP-11 xoá dữ liệu bạn bè) — 'Default ID d_6/-6: SET line_user.province = NULL' "
     "(KHÔNG có bước giảm total_user_has_value), trong khi 'Custom ID: DELETE friend_information_value "
     "+ GIẢM total_user_has_value'",
     "都道府県名 không có dòng trong bảng giá trị để 'xóa hẳn dòng', và luồng xoá của spec cho d_6 "
     "KHÔNG giảm bộ đếm. Nếu vậy 回答人数 của 都道府県名 sẽ không giảm khi xóa giá trị — trái corpus. "
     "Đây là điểm dễ lọt bug vì 5 trường địa chỉ đứng chung 1 folder, người test dễ coi là cùng hành vi.",
     "TC-FRI-318 (xóa trắng 都道府県名 vs 郵便番号) · TC-FRI-302 (gán/cập nhật/xóa 5 trường địa chỉ) · "
     "TC-FRI-182 (bộ đếm khi xóa — 都道府県名 nằm trong Dữ liệu test)",
     "",
     "① Chốt hành vi 回答人数 của 都道府県名 khi xóa giá trị: có giảm hay không.\n"
     "② Nếu CÓ giảm → bổ sung bước cập nhật bộ đếm cho nhánh d_6 vào feature-spec.md §2 (luồng EP-11).\n"
     "③ Nếu KHÔNG giảm → sửa expected TC-FRI-318 và tách 都道府県名 khỏi nhóm 4 trường địa chỉ trong "
     "TC-FRI-302, đồng thời ghi chú rõ ở spec để tester không hiểu nhầm."],

    ["MT-03", "CAO", W,
     "Phạm vi hành vi 'xóa trắng → xóa hẳn dòng, không để dòng rỗng': chỉ màn 友だち詳細 hay mọi lối ghi giá trị?",
     "RV-01 (r476) — lõi ticket #38591: 'Sau khi xóa trắng giá trị, dữ liệu lưu của trường KHÔNG còn dòng nào "
     "(kể cả dòng rỗng value=NULL)'\n"
     "RV-06 (r481) ghi rõ cảnh báo: 'H-150..157 human cover đúng hướng nhưng expected mơ hồ; FIX CHỈ ĐỤNG "
     "SERVICE MYPAGE nên các path khác CẦN CHỐT SCOPE để không pass oan'\n"
     "RV-07 (r482): 'Path mobile (Api/FriendInformationController) KHÔNG dùng service được fix (yokoten)'\n"
     "r463-r470: value tạo/xóa từ form, QR param, CSV, booking, action salon/friendlist",
     "feature-spec.md §2 (luồng EP-11) chỉ mô tả xoá từ màn 情報一覧 (一括削除).\n"
     "Spec KHÔNG mô tả luồng lưu giá trị từ 友だち詳細 / right bar chat 1:1 / app mobile / form / CSV / "
     "booking — tức KHÔNG có quy tắc 'lưu rỗng thì xóa dòng hay tạo dòng NULL' cho các lối này.\n"
     "feature-spec.md §6 chỉ liệt kê 6 Mobile API, ghi 'ngoài scope Admin portal' (Gap #8).",
     "Cùng 1 hành vi nghiệp vụ (xóa trắng giá trị) đi qua ≥ 7 lối ghi khác nhau; fix của #38591 chỉ đụng "
     "1 lối. Nếu không chốt scope, TC ở các lối còn lại có thể PASS oan (dòng NULL vẫn tồn tại nhưng "
     "màn hình không hiển thị) hoặc FAIL oan (kỳ vọng sai).",
     "TC-FRI-204 (không còn dòng nào sau khi xóa trắng) · TC-FRI-236 (xóa qua chính lối ghi của tính năng khác) · "
     "TC-FRI-191 (app mobile) · TC-FRI-198, TC-FRI-199 (null vs chuỗi rỗng · lưu rỗng khi chưa có giá trị)",
     "",
     "① Chốt danh sách lối ghi giá trị PHẢI tuân quy tắc 'xóa trắng = xóa hẳn dòng + count -1' "
     "(友だち詳細 · right bar chat 1:1 · app mobile · form · QR param · CSV · booking · action).\n"
     "② Bổ sung mục 'Luồng lưu giá trị friend info' vào feature-spec.md (hiện chỉ có luồng xoá EP-11).\n"
     "③ Với lối chưa được fix: ghi rõ ở TC là DỰ KIẾN FAIL → cần raise bug."],

    ["MT-04", "CAO", W,
     "Đổi text option ở màn form nhập của SALON có cập nhật giá trị bạn bè không? (corpus đang đánh NG)",
     "tab「Change spec info type select」(12/2024, Bug #27314):\n"
     "• r30 (lesson): 'check edit value của option ở màn form nhập ⇒ update text option ở các bảng: "
     "friend_information_setting, friend_info_option_selects, calendar_setting_send_form, "
     "update bảng friend_information_value'\n"
     "• r34 (salon): cùng expected nhưng ô kết quả ghi **NG** cho vế update giá trị bạn bè",
     "feature-spec.md §BR-09 + web/logic-spec.md §BR-09 — cascade 7 bảng khi đổi tên option, "
     "trong đó mục 2 là 'Cập nhật friend_information_value.value cho tất cả records có "
     "friend_info_option_id matching'. Spec ghi Tin cậy: **Cao**, KHÔNG phân biệt lesson và salon.",
     "Spec khẳng định cascade luôn cập nhật giá trị bạn bè; corpus lại ghi nhận salon FAIL ở đúng vế đó. "
     "Nếu chưa được fix, bạn bè đang giữ option của salon sẽ hiển thị text CŨ sau khi admin đổi tên — "
     "chính là hiện tượng gốc của Bug #27314 nhưng ở nhánh salon.",
     "TC-FRI-129 (sửa option ở màn form nhập lesson/salon → đồng bộ ngược) · TC-FRI-130 (xóa option ở màn đó)",
     "",
     "① Xác nhận NG ở r34 đã được fix chưa (tra ticket liên quan).\n"
     "② Nếu CHƯA fix → TC-FRI-129 dự kiến FAIL ở nhánh salon → raise bug, và ghi ngoại lệ vào BR-09.\n"
     "③ Nếu ĐÃ fix → cập nhật kết quả ở sheet nguồn để không gây hiểu nhầm cho lần test sau."],

    ["MT-05", "TRUNG BÌNH", W,
     "Validate trùng giá trị dùng chung message「選択肢の表示名が重複しています」cho cả kiểu ポイント",
     "SpecImprove #33697 (01/2026):\n"
     "• r145-r148: trùng option của kiểu 選択肢 ⇒ message「選択肢の表示名が重複しています。"
     "異なる値を入力してください。」\n"
     "• r150-r153: TRÙNG NGƯỠNG của kiểu ポイント ⇒ **cùng message đó**\n"
     "• r147/r152: chỉ khác dấu cách đầu/cuối cũng bị coi là trùng (so sánh có trim)",
     "feature-spec.md §Field Traceability #8 (「選択肢」option name) và #14 (Ngưỡng điểm) — "
     "cột Validation để trống, KHÔNG có rule unique.\n"
     "feature-spec.md §BR-03 — với type 6 (point), `value` = 'Ngưỡng điểm' (số), không phải tên hiển thị.\n"
     "Spec KHÔNG có mục nào ghi message validate này.",
     "① Spec bỏ sót hoàn toàn rule unique (cả select lẫn point).\n"
     "② Message nói về「選択肢の表示名」(tên hiển thị của lựa chọn) nhưng lại bung ra khi trùng NGƯỠNG "
     "ĐIỂM — sai ngữ cảnh với người dùng cuối là admin người Nhật.\n"
     "③ Chưa rõ trim có phải hành vi cố ý không.",
     "TC-FRI-66 → TC-FRI-70 (kiểu Lựa chọn) · TC-FRI-100 → TC-FRI-103 (kiểu Điểm)",
     "",
     "① Bổ sung rule unique + message vào feature-spec.md Field #8 và #14, nêu rõ áp cho cả 2 kiểu và "
     "phạm vi unique là TRONG CÙNG 1 TRƯỜNG (r149/r154 xác nhận 2 trường khác nhau được trùng).\n"
     "② Chốt message cho kiểu ポイント: giữ nguyên message chung hay đổi text riêng cho ngưỡng điểm.\n"
     "③ Chốt hành vi trim (space đầu/cuối) là cố ý."],

    ["MT-06", "TRUNG BÌNH", W,
     "Sau khi lưu ở màn tạo/sửa có đổi folder: màn list mở vào folder ĐÃ CHỌN Ở FORM hay folder ĐỨNG TRƯỚC ĐÓ?",
     "Bug KH #36201 (05/2026) — r214 và r216 ghi 2 vế trong CÙNG 1 ô kết quả:\n"
     "• vế 1: 'tạo mới info success, info mới hiển thị ở đúng folder ĐÃ CHỌN Ở MÀN TẠO MỚI'\n"
     "• vế 2: 'màn list hiển thị mở vào folder ĐÃ CHỌN TRƯỚC KHI nhấn tạo mới info'\n"
     "r215/r217/r225/r226 (không đổi folder): 'màn list hiển thị mở vào folder đã chọn trước đó'",
     "feature-spec.md §BR-12 + web/logic-spec.md §BR-12 — cookie `folder_info_friend` lưu "
     "{bot_id: folder_id}, path /basic/friend_information, max age 14400 phút.\n"
     "feature-spec.md §2 (luồng lưu EP-09) — chỉ ghi 'Redirect về SCR-FRI-01', KHÔNG nói cookie được "
     "set lại theo folder nào khi lưu.",
     "Khi admin đứng ở folder A, tạo trường nhưng chọn folder B ở form: 2 vế của corpus dẫn tới 2 kết quả "
     "trái ngược (mở vào B hay mở vào A). Spec không phân xử được vì không mô tả thời điểm set cookie. "
     "Ảnh hưởng trực tiếp trải nghiệm — chính là chủ đề của ticket #36201.",
     "TC-FRI-10 (đổi folder ở form) · TC-FRI-11 (không đổi folder) · TC-FRI-142 (copy rồi đổi folder)",
     "",
     "① Chốt: sau khi lưu có đổi folder thì list mở vào folder nào.\n"
     "② Bổ sung vào feature-spec.md §2 (luồng EP-09) và BR-12 thời điểm set cookie khi lưu.\n"
     "③ Sửa expected TC-FRI-10 cho khớp quyết định."],

    ["MT-07", "TRUNG BÌNH", W,
     "Giới hạn độ dài (管理名 20 / tên folder 15) enforce ở đâu: chặn nhập, báo lỗi, hay chỉ client?",
     "Corpus KHÔNG có TC cận biên nào cho 2 giới hạn này (đã rà toàn bộ 5 tab của "
     "10.2 TCsLine_friend_information).\n"
     "Tham chiếu ngang màn tag (kho FA-012 MT-03): cùng 1 field nhưng 3 lối vào cho 3 cơ chế khác nhau "
     "(báo lỗi / tự cắt / chặn nhập).",
     "ui-spec.md:93 — 管理名 'Tối đa 20 ký tự. Hiển thị đếm ký tự: {N}/20文字'\n"
     "ui-spec.md:215 — フォルダ名 'Tối đa 15 ký tự. Hiển thị đếm: {N}/15'\n"
     "web/logic-spec.md:210-211 — 'Tên quản lý: tối đa 20 ký tự (THEO UI SPEC)' / "
     "'Tên folder: tối đa 15 ký tự (THEO UI SPEC)'\n"
     "web/logic-spec.md:501 + feature-spec §9 Gap #11 — 'Validation phía client (max length, required) "
     "CHƯA KIỂM TRA JS/Blade. Tin cậy: Trung bình'\n"
     "db-mapping.md:194 — cột name của folder cho phép varchar(100)",
     "Spec chỉ suy giới hạn từ UI, chưa xác nhận có validate phía server. DB cho phép tới 100 ký tự "
     "→ nếu gọi thẳng API có thể lưu tên dài hơn giới hạn UI. Không chốt thì TC cận biên không có oracle.",
     "TC-FRI-16, TC-FRI-17, TC-FRI-32 (tên folder 15 ký tự) · TC-FRI-54, TC-FRI-55 (管理名 20 ký tự) · "
     "TC-FRI-61 (gọi thẳng API đổi type_data)",
     "",
     "① Chốt cơ chế cho từng field: chặn ở input / báo lỗi khi lưu / tự cắt.\n"
     "② Chốt có validate phía server không (test gọi thẳng API).\n"
     "③ Bổ sung message lỗi cụ thể vào ui-spec.md và đóng Gap #11."],

    ["MT-08", "THẤP", W,
     "Tên folder friend info có bắt buộc duy nhất trong 1 bot không?",
     "Corpus không có TC trực tiếp cho friend info. Tab「Test bug folder all màn」(Bug Tester #27083, "
     "04/2026) ghi ở dòng đầu: 'Base theo testcase fix bug MÀN TAG' và khối màn friend info (r106-r122) "
     "là bản sao của khối tag (thậm chí còn ghi nhầm 'tạo TAG trong folder' và kind=0 thay vì kind=12).\n"
     "Ở màn tag: trùng tên folder VẪN cho tạo (kho FA-012 MT-04).",
     "feature-spec.md §BR-01 + Field #6 — chỉ ghi folder lưu ở category (kind=12, is_deleted=0), "
     "max 15 ký tự. KHÔNG có rule unique tên folder.",
     "Nếu suy từ màn tag sang thì trùng tên được phép — nhưng đó là SUY LUẬN chéo tính năng, "
     "chưa có bằng chứng trực tiếp cho FA-015. Trùng tên folder gây khó phân biệt khi chuyển folder hàng loạt.",
     "TC-FRI-21 (copy tên folder → paste không sửa)",
     "",
     "① Chốt: tên folder friend info có cần duy nhất không.\n"
     "② Bổ sung kết luận vào feature-spec.md BR-01.\n"
     "③ Đề xuất tách riêng khối TC folder cho friend info ở sheet nguồn (hiện đang copy nhầm nội dung "
     "của màn tag: 'tạo tag trong folder', kind=0)."],

    ["MT-09", "TRUNG BÌNH", W,
     "Xóa trường 年月日 / xóa folder chứa nó → lịch gửi đã lên có được dọn không?",
     "tab date r390: 'Check xóa action info ⇒ xóa record trong bảng event_step_time' — mới chỉ cover "
     "xóa CẤU HÌNH ACTION, KHÔNG có TC cho xóa cả TRƯỜNG hoặc xóa FOLDER chứa trường.\n"
     "RV-04 (r479) nêu rủi ro cùng hướng: 'xóa dòng mà không dọn lịch sẽ để schedule trỏ dữ liệu đã xóa'.",
     "feature-spec.md §BR-06 (cascade xoá info setting) liệt kê 5 bước DELETE cụ thể, bước 6 ghi: "
     "'Implicit: xoá event_step + event_step_time (type=3)' — chữ 'implicit' cho thấy KHÔNG đọc được "
     "trực tiếp từ code.\n"
     "feature-spec.md §BR-01 (xoá folder) chỉ ghi 'cascade xoá toàn bộ info settings + values + options "
     "+ display settings', KHÔNG nhắc tới lịch gửi.",
     "Nếu lịch không được dọn: bạn bè vẫn nhận action của trường đã bị xóa (tin nhắn ma) — lỗi lộ ra "
     "phía LINE user, khó truy vết. Đây là vùng mà cả corpus lẫn spec đều mỏng.",
     "TC-FRI-35 (xóa folder chứa trường 年月日) · TC-FRI-158 (xóa trường 年月日 có lịch) · "
     "TC-FRI-271 (xóa cấu hình action)",
     "",
     "① Xác nhận trong code: xoá trường và xoá folder có dọn event_step/event_step_time không.\n"
     "② Sửa BR-06 bước 6 từ 'implicit' thành khẳng định có dẫn chứng, và bổ sung vế lịch gửi vào BR-01.\n"
     "③ Nếu chưa dọn → raise bug (TC-FRI-35 và TC-FRI-158 dự kiến FAIL)."],

    ["MT-10", "THẤP", W,
     "Ba điểm cả corpus lẫn spec đều không nói: trường 選択肢 không có option nào · "
     "validate ô số ngày offset · quy tắc đặt tên bản copy",
     "Corpus không có TC cho cả 3 điểm.\n"
     "Suy luận gần nhất: ô random điểm chặn nhập chữ và tự chuyển số Nhật sang latinh "
     "(ModalAction r7, r79 — 11/2023).",
     "feature-spec.md §Field #11 — số ngày offset: 'Integer ≥ 0' (không có message lỗi).\n"
     "feature-spec.md §BR-05 (deep clone) — chỉ ghi 'Reset total_user_has_value = 0, order = max+1', "
     "KHÔNG nói quy tắc đặt 管理名 cho bản copy.\n"
     "Không mục nào của spec nói trường 選択肢 có bắt buộc ≥ 1 option hay không.",
     "Không có oracle để phán TC pass/fail. Riêng bản copy còn chạm giới hạn 20 ký tự của 管理名 "
     "(nếu tự thêm hậu tố vào tên đã đủ 20 ký tự thì sinh ra trường hợp chưa xác định).",
     "TC-FRI-78 (選択肢 không option) · TC-FRI-94 (validate số ngày offset) · TC-FRI-151 (tên bản copy)",
     "",
     "① Chốt 3 hành vi trên.\n"
     "② Bổ sung vào feature-spec.md: Field #8 (option tối thiểu), Field #11 (message validate), "
     "BR-05 (quy tắc đặt tên bản copy).\n"
     "③ Sau khi chốt, sửa expected của 3 TC (hiện đang để 'ghi nhận hành vi thực tế')."],

    ["MT-11", "TRUNG BÌNH", W,
     "Kiểu ポイント: ngưỡng là số nguyên hay cho phép thập phân? Vượt ngưỡng có kích hoạt action không?",
     "ModalAction (11/2023) r8, r80: random điểm 'nhập số thập phân ⇒ lấy giá trị random trong khoảng "
     "THẬP PHÂN đó' → hệ thống có xử lý điểm thập phân.\n"
     "r31 (08/2024): 'khi user được gán số point = số point setting thì có action được bình thường' — "
     "chỉ nói trường hợp BẰNG, không nói vượt ngưỡng.",
     "feature-spec.md §Field #14 — 'Ngưỡng điểm (Point): Integer, Threshold trigger action'\n"
     "feature-spec.md §SCR-FRI-05 — 'Khi TỔNG ĐIỂM của bạn bè ĐẠT ngưỡng → trigger action tương ứng' "
     "(chữ 'đạt' không phân định = hay ≥)\n"
     "feature-spec.md §BR-03 — với type 6, `value` = 'Ngưỡng điểm'",
     "① Spec ghi Integer nhưng corpus cho phép thập phân → nếu admin nhập ngưỡng 10 mà action random "
     "gán 10.5 thì hành vi trigger không xác định.\n"
     "② 'Đạt ngưỡng' hiểu là '= ngưỡng' hay '≥ ngưỡng' cho 2 kết quả khác hẳn khi bạn được cộng dồn "
     "điểm nhảy qua mốc.",
     "TC-FRI-99 (dưới/bằng/vượt ngưỡng) · TC-FRI-106 (random điểm thập phân)",
     "",
     "① Chốt: ngưỡng có nhận số thập phân không; trigger là '=' hay '≥'.\n"
     "② Bổ sung vào feature-spec.md Field #14 và §SCR-FRI-05.\n"
     "③ Sửa expected TC-FRI-99 (hiện để 'ghi nhận hành vi thực tế' cho nhánh vượt ngưỡng)."],

    ["MT-12", "TRUNG BÌNH", W,
     "Phân quyền staff cho FA-015: kiểm ở đâu, staff làm được những gì?",
     "Corpus có nhiều dòng「Check account staff」nhưng TẤT CẢ đều KHÔNG có kết quả mong đợi: "
     "r142 (staff xóa friend), r273, r499, r574 (test fix bug), tab date r189, r356.\n"
     "Nguồn duy nhất có expected là TCsLine_Improve chung /「Phân quyền」(2023-11-10) — message chung "
     "cho MỌI màn:「操作できません。この機能の操作権限が付与されていません。"
     "主管理者に操作権限を付与してもらうことで操作が可能となります。」\n"
     "RV-13 (r488): '[Permission] Account staff xóa friend info' — cũng chỉ có tiêu đề.",
     "feature-spec.md §9 Gap #2 (Trung bình) — 'Staff permissions CHƯA XÁC NHẬN — không phát hiện "
     "Policy/Gate riêng trong controller. Có thể kiểm tra ở route group middleware hoặc Blade view'\n"
     "feature-spec.md §10 Open Question 2 — 'không rõ tính năng FA-015 kiểm tra quyền ở đâu'\n"
     "feature-spec.md §6 Middleware — chỉ liệt kê web, NotifyChatworkRequestTimeSlow, LogRequestMultipart "
     "(KHÔNG có middleware phân quyền)",
     "Nếu quyền chỉ được kiểm ở tầng ẩn menu/Blade mà không kiểm ở tầng route/API thì staff bị ẩn menu "
     "vẫn có thể gõ thẳng URL hoặc gọi API để đọc/sửa dữ liệu bạn bè. Corpus không có TC nào kiểm tầng "
     "URL/API cho FA-015.",
     "TC-FRI-63 (staff không quyền) · TC-FRI-140 (staff sửa trường) · TC-FRI-254 (staff chạy action) · "
     "TC-FRI-330 → TC-FRI-334 (nhóm Phân quyền & môi trường) · TC-FRI-196 (staff change bot)",
     "",
     "① Xác nhận trong code nơi kiểm quyền của FA-015 (route middleware / controller / Blade).\n"
     "② Chốt ma trận quyền: 副管理人 và 運用者 làm được gì trên FA-015.\n"
     "③ Bổ sung vào feature-spec.md §6 và đóng Gap #2 + Open Question 2.\n"
     "④ Ưu tiên chạy TC-FRI-332 (gõ thẳng URL) và TC-FRI-333 (gọi thẳng API) — đây là chiều corpus chưa phủ."],

    ["MT-13", "TRUNG BÌNH", W,
     "Xóa TRƯỜNG thông tin có dọn các bộ lọc đang tham chiếu nó không?",
     "Corpus có TC cascade khi ĐỔI TÊN option (tab「Change spec info type select」r68: xóa option → "
     "'Xóa option tương ứng' ở filter) nhưng KHÔNG có TC nào cho tình huống xóa hẳn cả TRƯỜNG.",
     "feature-spec.md §BR-06 (cascade xoá info setting) liệt kê đúng 5 bảng: t_actions_detail, "
     "friend_information_value, friend_information_setting, setting_display_info_friend_chat11, "
     "friend_info_option_selects — **KHÔNG có filter_v2**.\n"
     "Trong khi feature-spec.md §BR-09 (đổi tên option) LẠI có bước cập nhật filter_v2.",
     "Spec tự bất đối xứng: đổi tên option thì đụng filter, xóa hẳn trường thì không. Bộ lọc trỏ tới "
     "trường đã bị xóa có thể gây lỗi truy vấn hoặc lọc sai âm thầm ở broadcast/auto-reply/CSV — "
     "hậu quả là gửi tin sai tập bạn bè.",
     "TC-FRI-157 (xóa trường đang dùng trong FILTER)",
     "",
     "① Xác nhận code: xoá trường có dọn/vô hiệu hoá filter_v2 tham chiếu không.\n"
     "② Bổ sung filter_v2 vào BR-06 (hoặc ghi rõ là cố ý không đụng, kèm cách hệ thống xử lý filter mồ côi).\n"
     "③ Nếu filter mồ côi gây lỗi → raise bug."],

    ["MT-14", "TRUNG BÌNH", W,
     "Đổi bot (change bot) reset toàn bộ 回答人数 về 0 — spec không ghi",
     "tab「Improve count phía web」(06/2025) r125-r137: 'Check case change bot ⇒ update lại toàn bộ số "
     "count của friend info = 0' cho TẤT CẢ trường (name, email, ngày sinh, số điện thoại, 5 trường "
     "địa chỉ, text, select, point, ngày, ảnh, pdf), kèm 'Check bot khác không bị update'.\n"
     "r138-r142: các tính năng khác (kịch bản, tag, richmenu, landing, form) cũng reset count = 0.",
     "feature-spec.md §Field #4 — 回答人数: 'Đếm tự động, append 人'.\n"
     "db-mapping.md:57 — total_user_has_value: 'Đếm số bạn bè có giá trị'.\n"
     "Spec KHÔNG có mục nào mô tả tính năng change bot hay ảnh hưởng của nó tới bộ đếm.",
     "Đây là hành vi ảnh hưởng trực tiếp cột hiển thị chính của màn FA-015 nhưng không có trong spec. "
     "Tester không biết trước sẽ coi 'count về 0 sau change bot' là BUG.",
     "TC-FRI-195, TC-FRI-196 (change bot bởi admin và bởi staff)",
     "",
     "① Xác nhận hành vi còn đúng ở phiên bản hiện tại (TC gốc 06/2025).\n"
     "② Bổ sung mục 'Ảnh hưởng của change bot tới total_user_has_value' vào feature-spec.md §5 "
     "(hoặc mục Phụ thuộc chéo).\n"
     "③ Chốt: sau change bot count có được tính lại theo dữ liệu mới không, hay giữ 0 vĩnh viễn."],

    ["MT-15", "TRUNG BÌNH", W,
     "Set / cập nhật giá trị điểm trên APP MOBILE — corpus đang ghi NG",
     "Khối 2024-08 (Bug #26541 / #26532) r26-r30: 'Check app mobile / màn mypage':\n"
     "• 'friend chưa có value → set value = 0' ⇒ ghi **NG**\n"
     "• 'friend đã có value → update value 0 sang != 0' ⇒ **NG**\n"
     "• 'value != 0 sang value = 0' ⇒ **NG**\n"
     "(2 cột kết quả khác của cùng dòng lại ghi OK → không rõ đã fix ở đợt nào)\n"
     "RV-07 (r482, 07/2026) tiếp tục cảnh báo: 'Path mobile KHÔNG dùng service được fix (yokoten); "
     "H-160 đã bắt 1 case lỗi'.",
     "feature-spec.md §6 Mobile API — liệt kê 6 endpoint (save-custom-info, save-custom-info-v2, …) "
     "và ghi 'ngoài scope Admin portal'.\n"
     "feature-spec.md §9 Gap #8 — 'Mobile API chỉ liệt kê, CHƯA PHÂN TÍCH CHI TIẾT'.",
     "Path mobile ghi cùng dữ liệu friend info nhưng đi qua controller khác, không dùng service đã được "
     "fix. Spec lại đặt mobile ngoài scope → không ai sở hữu hành vi này. Corpus có 3 dấu NG chưa rõ "
     "đã fix hay chưa.",
     "TC-FRI-216 (set/cập nhật/xóa giá trị điểm trên app) · TC-FRI-191 (bộ đếm khi thao tác trên app) · "
     "TC-FRI-194 (admin book hộ trên app) · TC-FRI-317 (folder địa chỉ trên app my page)",
     "",
     "① Tra lại 3 case NG ở r26-r30 đã fix chưa.\n"
     "② Chốt: hành vi count và row cleanup của path mobile phải giống path web hay được phép khác.\n"
     "③ Nếu phải giống → đưa Mobile API vào scope spec FA-015, đóng Gap #8.\n"
     "④ TC-FRI-216 và TC-FRI-191 dự kiến FAIL nếu chưa fix → raise bug."],

    ["MT-16", "TRUNG BÌNH", W,
     "Import CSV cập nhật giá trị 年月日: có cập nhật lịch gửi không? — corpus tự mâu thuẫn",
     "tab「check setting-action-friend-info-date」(10/2025 → 04/2026) có 2 dòng ngược nhau:\n"
     "• r124: 'Import CSV có update friend info value cho user ⇒ Import CSV sẽ KHÔNG action ⇒ "
     "info type date cũng sẽ không action ⇒ KHÔNG update event_step_time'\n"
     "• r279-r281 (khối Bug KH #34675, mới hơn): 'Import CSV / check update value / value user đang có "
     "không thỏa mãn event → import value thỏa mãn ⇒ **UPDATE LẠI TIME SEND ACTION**' và "
     "'check insert value ⇒ **INSERT vào event_step_time**'",
     "feature-spec.md §7 (Trigger points ngoài Admin portal) — bảng ghi rõ: "
     "'CSV import | HandleImportCsvTask.java | Import date values → **scheduling**'\n"
     "→ Spec đứng về phía r279-r281.",
     "2 khối TC trong CÙNG 1 TAB nói ngược nhau. Niên đại gần nhau (r124 thuộc khối gốc 10/2025, "
     "r279-r281 thuộc khối #34675 03/2026) nên **quy tắc 'ưu tiên TC mới nhất' là căn cứ YẾU ở đây** — "
     "chọn r279-r281 chủ yếu vì spec §7 xác nhận cùng chiều và vì khối này chi tiết hơn (phân biệt "
     "update value thỏa mãn / không thỏa mãn / insert value mới).\n"
     "Hệ quả nếu chọn sai: bạn được import ngày sinh nhật sẽ KHÔNG nhận được lời chúc (thiếu lịch) "
     "hoặc nhận SAI thời điểm.",
     "TC-FRI-253 (import CSV cập nhật giá trị 年月日) · TC-FRI-308 (import CSV có cột địa chỉ) · "
     "TC-FRI-231 (import CSV ghi giá trị) · TC-FRI-232 (import CSV giá trị rỗng)",
     "",
     "① Chốt: import CSV có sinh/cập nhật lịch gửi không, và có kích hoạt action ngay không "
     "(2 câu hỏi KHÁC NHAU — corpus r124 gộp chung).\n"
     "② Nếu chốt theo r279-r281 → đánh dấu r124 là đã lỗi thời ở sheet nguồn.\n"
     "③ TC-FRI-253 hiện viết theo r279-r281 + spec §7; nếu Leader chốt ngược lại thì phải sửa expected."],

    ["MT-17", "TRUNG BÌNH", W,
     "Job gửi action ngày tháng mặc định TẮT — ảnh hưởng toàn bộ TC nhóm job",
     "Toàn bộ tab「check setting-action-friend-info-date」(390 dòng) giả định job đang chạy: "
     "'sau khi job chạy xong, sẽ add thêm bản ghi', 'tới event_step_time mới send action cho user'.\n"
     "Corpus KHÔNG có dòng nào yêu cầu kiểm tra/bật cấu hình job trước khi test.",
     "feature-spec.md §7 (Cấu hình NewEventRemindTask):\n"
     "| ENABLE_EVENT_REMIND | **`0` (off)** | Bật/tắt NewEventRemindTask |\n"
     "→ Spec ghi mặc định là TẮT.",
     "Nếu môi trường test đang để mặc định (tắt) thì mọi TC nhóm「Job action ngày tháng」(≈ 20 TC, "
     "gồm toàn bộ TC boundary của Bug #34675/#35967) sẽ KHÔNG BAO GIỜ pass được, và dễ bị kết luận "
     "nhầm là bug logic thay vì cấu hình môi trường.",
     "TC-FRI-255 → TC-FRI-276 (toàn bộ nhóm「Job action ngày tháng」) · TC-FRI-337 (job bị tắt) · "
     "TC-FRI-84 → TC-FRI-96 (nhóm「Info kiểu Ngày tháng — setting」có kiểm mốc gửi thực tế)",
     "",
     "① Xác nhận giá trị ENABLE_EVENT_REMIND thực tế trên STAGING và PRODUCTION.\n"
     "② Ghi rõ điều kiện tiền đề 'job đang bật' vào tất cả TC nhóm job (hiện chỉ ghi ở TC-FRI-255).\n"
     "③ Nếu staging tắt job → chốt các TC này CHỈ chạy trên PRODUCTION (đã set env=PRODUCTION theo RULE-08)."],

    ["MT-18", "THẤP", W,
     "Phạm vi backup của FA-015 chưa được spec định nghĩa",
     "ModalAction r69-r70: 'so sánh backup / calendar' và 'bill tiền' ⇒ '**ko backup**'.\n"
     "Feature #29832 r218-r219: 'Check backup / backup message pattern / lesson · salon' ⇒ "
     "'**không có backup**'.\n"
     "tab「Change spec info type select」r73-r84: CÓ backup + recover cho friend info select, form answer, "
     "booking event, multi action, filter.",
     "feature-spec.md §BR-07 chỉ nói backup LOCK (chặn thao tác write khi đang backup).\n"
     "Spec KHÔNG có mục nào định nghĩa nội dung nào của FA-015 được backup/khôi phục.\n"
     "db-mapping.md có liệt kê bảng backup_history nhưng chỉ dùng cho lock.",
     "Không rõ khi khôi phục bot thì giá trị friend info của bạn bè, lịch gửi (event_step_time), "
     "và cấu hình hiển thị chat 1:1 có được khôi phục không. Tester không có oracle cho nhóm TC backup.",
     "TC-FRI-320 → TC-FRI-329 (nhóm「Backup & recover」), đặc biệt TC-FRI-322 (giá trị bạn bè) và "
     "TC-FRI-323 (cấu hình lịch) · TC-FRI-328 (nơi không được backup)",
     "",
     "① Chốt danh sách nội dung FA-015 được backup: cấu hình trường · option · action · giá trị bạn bè · "
     "lịch gửi · cấu hình hiển thị chat 1:1.\n"
     "② Bổ sung mục 'Phạm vi backup' vào feature-spec.md §5.\n"
     "③ Sau khi chốt, sửa expected TC-FRI-322 và TC-FRI-323 (hiện ghi là AI bổ sung, cần xác nhận)."],
]
