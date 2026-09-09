# -*- coding: utf-8 -*-
"""FA-011 — Các điểm MÂU THUẪN.

Trạng thái: 22/23 mục ĐÃ CHỐT.
  • 2026-08-19 — Leader chốt MT-00 → MT-19 (trừ MT-09).
  • 2026-08-22 — Leader chốt MT-20, MT-21, MT-22 (3 mục phát hiện khi đối chiếu với spec mới bổ sung).
  • CÒN LẠI: **MT-09 chưa có quyết định** — ô QUYẾT ĐỊNH vẫn để trống.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER (2026-08-19 / 2026-08-22)",
        "Việc phải làm tiếp"]

CONFLICTS = [
    ["MT-00", "CAO", "✅ ĐÃ CHỐT",
     "FA-011 CHƯA CÓ SPEC — toàn bộ kho TCs form không có nguồn đối chiếu",
     "Corpus TCs form rất lớn và liên tục cập nhật: tab「Improve form 01/2025」(3828 dòng, 01/2025 → 06/2026), "
     "「Improve form 01/2025 Line user」(1580 dòng), 「Sync google」(519 dòng, tới 07/2026). "
     "Riêng tab Info liệt kê 54 đợt spec-change / bug KH từ 05/2023 tới 07/2026.",
     "TẠI THỜI ĐIỂM GOM: spec-features/admin/index.md dòng 21 ghi FA-011 UI/Web/DB/Validate = CHƯA, "
     "không tồn tại thư mục spec-features/admin/form*.\n"
     "SAU KHI LEADER XỬ LÝ: đã có spec-features/admin/form-answer/ (feature-spec 48K + web/api-spec + "
     "web/logic-spec + db/db-mapping + ui/ui-spec + 3 screenshot), trạng thái HOÀN THÀNH, "
     "10 màn hình · 43 endpoint · 14 business rule · 12 gap.",
     "Không có spec để đối chiếu → mọi 'kết quả mong đợi' trong kho TCs chỉ dựa vào corpus TCs cũ và design XD.",
     "Toàn bộ kho TCs FA-011",
     "Đã bổ sung tính năng này trong spec-features.",
     "✅ ĐÃ XONG: spec-features/admin/form-answer/ đã tồn tại và ở trạng thái HOÀN THÀNH.\n"
     "CÒN LẠI: ① cập nhật spec-features/admin/index.md dòng 21 — FA-011 vẫn đang ghi CHƯA ở cả 6 cột "
     "(UI Scan / Web / Job / DB / Validate / Compile) dù thư mục spec đã HOÀN THÀNH.\n"
     "② Đối chiếu lại kho TCs với spec mới đã phát hiện 3 điểm lệch — xem MT-20, MT-21, MT-22."],

    ["MT-01", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Message lỗi khi 管理名 form bỏ trống / toàn khoảng trắng — 2 message khác nhau",
     "r501: bỏ trống 管理名 → 「管理名を入力して下さい」\n"
     "r506: nhập chuỗi toàn khoảng trắng → 「フォーム名を入力してください」\n"
     "(r512 và r517 ở màn edit lặp lại đúng cặp message này)",
     "feature-spec.md §SCR-FA11-02 bước 2: 'Nhập 管理名, フォーム名, chọn フォルダ, タイプ' → xác nhận modal có 2 ô.\n"
     "ui/ui-spec.md:108「管理名（入力内容はお客様に表示されません）」tối đa 50 ký tự, bắt buộc.\n"
     "ui/ui-spec.md:109「フォーム名（入力内容がお客様に表示されます）」tối đa 20 ký tự, bắt buộc.",
     "Trước khi có spec: tưởng 2 message của CÙNG 1 ô nên mâu thuẫn. Thực chất là 2 ô khác nhau.",
     "[Tạo form] modal 4 vùng · [Tạo form] ô 管理名 bỏ trống · [Tạo form] ô 管理名 toàn khoảng trắng · "
     "[Tạo form] ô フォーム名 bỏ trống · [Tạo form] ô フォーム名 tối đa 20 ký tự",
     "Ở modal tạo form có 2 phần nhập: 管理名（入力内容はお客様に表示されません）và "
     "フォーム名（入力内容がお客様に表示されます）. Khi bỏ trống ô nhập nào thì hiển thị msg tương ứng của ô nhập đấy.",
     "✅ Đã sửa TCs: TC modal tạo form đổi từ 3 vùng → 4 vùng · TC 管理名 ghi rõ message 管理名を入力して下さい · "
     "THÊM 2 TC mới cho ô フォーム名 (bỏ trống → フォーム名を入力してください; giới hạn 20 ký tự).\n"
     "KHÔNG cần sửa spec — spec đã ghi đúng."],

    ["MT-02", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Copy page tạo ra tên page VƯỢT giới hạn 10 ký tự mà không bị chặn",
     "r1085-r1086: tạo page tên > 10 ký tự → báo lỗi, không tạo được.\n"
     "r1128: copy page tên 9 ký tự → tự thêm「コピー」thành 12 ký tự → 'vẫn save được page mới, "
     "khi nào vào edit page nhấn save thì mới báo lỗi quá ký tự'.",
     "feature-spec.md không có BR riêng cho giới hạn tên page; BR-10 chỉ mô tả next_page_type.",
     "Hệ thống cho phép tồn tại page vượt giới hạn qua đường copy nhưng chặn qua đường tạo/edit.",
     "[Form rẽ nhánh — page] Copy page khi tên gốc dài",
     "Giữ nguyên spec copy hiện tại. Khi copy thì vẫn tự động thêm text コピー ở cuối; khi user vào edit "
     "name page mà quá 10 ký tự thì báo lỗi để user tự sửa.",
     "✅ Đã sửa TC: ghi rõ đây là hành vi ĐÚNG SPEC, không raise bug.\n"
     "Đề xuất bổ sung 1 BR vào feature-spec.md: 'Tên page ≤ 10 ký tự khi tạo/edit; copy page không "
     "validate độ dài, chỉ validate lại khi user mở modal edit'."],

    ["MT-03", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Giới hạn số folder / item / ký tự ở bot plan FREE — không có con số nào",
     "Tab「Limit Form answer」liệt kê 8 mục giới hạn (1000 folder, 500 item/page, 20.000 ký tự HTML, "
     "20.000 ký tự CSS/JS, 50 step remind, 1000 khoảng point, 20.000 ký tự page sau trả lời, "
     "20.000 ký tự text countdown). Mỗi mục đều có dòng 'Check limit ở bot free' nhưng KHÔNG ghi con số nào "
     "(r8, r20, r30, r44, r52, r60, r68, r76).",
     "feature-spec.md BR-01: 'Free plan chỉ được tối đa 3 form active. Kiểm tra trước khi tạo mới (storeV3) "
     "và trước khi khôi phục (restoreFormAnswer)'. Spec KHÔNG có BR nào cho 8 mục giới hạn còn lại.",
     "Không biết bot Free có giới hạn riêng hay dùng chung con số với Standard/Pro.",
     "[Folder form] Giới hạn 1000 folder ở bot Free · [Giới hạn & hiệu năng] 8 mục giới hạn áp chung mọi bot",
     "Đây là giới hạn chung cho toàn bộ các bot: bao gồm cả bot free và bot có phí.",
     "✅ Đã sửa 2 TC: mốc chặn của bot Free = bot Standard ở cả 8 mục; ghi rõ riêng SỐ FORM vẫn theo plan "
     "(BR-01: free ≤ 3 form).\n"
     "Đề xuất bổ sung vào feature-spec.md 1 BR mới liệt kê 8 giới hạn dùng chung mọi plan, để phân biệt rõ "
     "với BR-01 (giới hạn theo plan)."],

    ["MT-04", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Modal SORT list form khi form có phân trang hoặc đang search — lấy toàn bộ form hay chỉ form đang hiển thị?",
     "r61: 'check search form → sau đó nhấn sort' và r63-r65: sort ở page 1 / page 2 / page cuối — "
     "kết quả mong đợi chỉ ghi chung chung 'Hiển thị theo system name, sort được đúng data'.",
     "feature-spec.md §SCR-FA11-01 không mô tả chi tiết modal sort.",
     "Không rõ modal sort lấy TOÀN BỘ form của folder hay chỉ form của trang/kết quả search hiện tại — "
     "chỗ dễ ghi đè sai thứ tự các form không liên quan.",
     "[Sort & search form] Sort khi có phân trang · [Sort & search form] Search rồi sort",
     "Modal sort hiện tại đang lấy toàn bộ form của folder.",
     "✅ Đã sửa 2 TC: expected = modal luôn hiển thị đủ toàn bộ form của folder, không phụ thuộc "
     "search hay phân trang.\n"
     "Đề xuất bổ sung mô tả modal sort vào §SCR-FA11-01 của feature-spec.md."],

    ["MT-05", "THẤP", "✅ ĐÃ CHỐT",
     "Chuỗi 'sort option checkbox chưa lưu → sort item ngoài → lưu' — không có kết quả mong đợi",
     "r851 và r878: 'Check case sort checkbox >> không save >> sort item >> save sort checkbox' — "
     "cột Expect Result ĐỂ TRỐNG ở cả 2 dòng.",
     "feature-spec.md EP-05 `/basic/form-answer/save-v3/{id}` — 'Lưu toàn bộ nội dung form (v3)'. "
     "Tên endpoint xác nhận cơ chế lưu là lưu TOÀN BỘ form trong 1 lần gọi.",
     "Không biết thay đổi chưa lưu ở cấp option có bị mất khi lưu ở cấp item hay không.",
     "[Màn edit form] Sort option bên trong item checkbox",
     "Khi click button 保存 hoặc button プレビュー ở màn detail form thì sẽ tự động save lại những thay đổi "
     "của form (bao gồm cả item và các option checkbox).",
     "✅ Đã sửa TC: bổ sung bước kiểm tra cả nút 保存 lẫn nút プレビュー; expected = lưu toàn bộ thay đổi "
     "ở cả 2 mức (option checkbox và item ngoài), không mất thay đổi nào.\n"
     "Đề xuất bổ sung vào feature-spec.md: nút プレビュー cũng trigger EP-05 (hiện spec chỉ mô tả nút lưu)."],

    ["MT-06", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Message giới hạn dung lượng khi LINE user upload audio (200MB) và PDF (50MB)",
     "Line user r570: ảnh > 10MB →「10MBまでのファイルをアップロードできます」(có message rõ)\n"
     "Line user r578: video > 200MB →「200MBまでのファイルをアップロードできます」(có message rõ)\n"
     "Line user r583 (audio > 200MB) và r588 (PDF > 50MB): chỉ ghi 'báo lỗi', KHÔNG ghi nội dung message.",
     "Không có message tiếng Nhật nào trong toàn bộ spec-features/admin/form-answer/ "
     "(đã grep 「を入力してください」/「アップロードできます」 → 0 kết quả).",
     "Tester không đối chiếu được message, dễ pass nhầm khi hệ thống hiện message sai loại.",
     "[Item upload file] Giới hạn dung lượng theo loại file",
     "Upload audio quá 200MB thì báo lỗi「200MBまでのファイルをアップロードできます」.\n"
     "Upload PDF quá 50MB thì báo lỗi「50MBまでのファイルをアップロードできます」.",
     "✅ Đã sửa TC: điền đủ 4 message cho ảnh / video / audio / PDF.\n"
     "Đề xuất bổ sung bảng Validation Messages vào feature-spec.md — spec hiện KHÔNG có message tiếng Nhật nào; "
     "dùng tab「Message error」của file TCs gốc làm nguồn."],

    ["MT-07", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Item 規約 (đồng ý quy chế) có được ghi vào Google Sheet không? — 2 tab nói ngược nhau",
     "Tab「Task nhỏ」r33 và tab master r218, r241: item 'quy chế' → 'Có insert được đúng data vào file CSV'.\n"
     "Tab「Improve form 01/2025 Line user」r800: 'check item quy chế → không ghi vào file google'.",
     "feature-spec.md không mô tả item 規約 trong danh sách loại câu hỏi và không mô tả nội dung sync.",
     "CSV có cột cho item quy chế nhưng Google Sheet thì không — 2 nguồn xuất ra 2 kết quả khác nhau.",
     "[Item thường dùng] Item 規約 · [Export CSV] Cột trong file CSV · [Sync Google Sheet & job] Nội dung sync",
     "Item quy chế CÓ được insert vào file CSV và Google Spread, với data chính là nội dung "
     "チェックボックスの案内文 đã setting trong form.",
     "✅ Đã sửa 3 TC: item 規約 có cột ở CẢ CSV lẫn Google Sheet, giá trị = nội dung チェックボックスの案内文.\n"
     "⚠️ DỰ KIẾN FAIL ở nhánh Google Sheet (corpus r800 ghi hiện trạng là không ghi) → khi chạy nếu thiếu cột "
     "thì RAISE BUG.\n"
     "Đề xuất bổ sung item 規約 vào danh sách loại câu hỏi trong feature-spec.md."],

    ["MT-08", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Tag đã bị xóa mà form vẫn map: hiển thị và hành vi ở form answer",
     "Line user r425, r450, r483: 'Check tag bị xóa' → chỉ ghi 'user mở form và submit được bình thường' "
     "(không nói option còn hiện hay không, không nói có gán tag không).",
     "spec-features/admin/tag-management/db/db-mapping.md:33 và :738 — `form_answer_details` là SIDE EFFECT "
     "của việc ĐỔI TÊN tag. Spec tag KHÔNG cover nhánh XÓA tag.\n"
     "feature-spec.md FA-011 BR-12 chỉ mô tả liên kết friend info, không mô tả liên kết tag bị xóa.",
     "Spec tag chỉ cover nhánh đổi tên (có cascade update) mà không cover nhánh xóa.",
     "[Liên kết friend info & tag] Tag bị xóa — nhánh màn admin · nhánh phía LINE user",
     "Trên màn hình detail tag, không hiển thị được tag đã bị xóa → khi click save thì báo lỗi "
     "「タグを選択してください。」",
     "✅ Đã TÁCH thành 2 TC: (a) màn admin — dropdown không hiện tag đã xóa, nhấn lưu báo "
     "「タグを選択してください。」; (b) phía LINE user — vẫn mở và submit được, không bị gán tag đã xóa.\n"
     "Đề xuất bổ sung hành vi 'tag bị xóa' vào cả feature-spec FA-011 (BR-12) và spec tag-management "
     "(liên kết với MT-10 của kho TCs FA-012)."],

    ["MT-09", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Sửa TEXT option của item rẽ nhánh làm MẤT setting next page — corpus ghi là 'không fix được'",
     "r1202, r1206, r1210, r1214 (cho item radio / dropdown / chẩn đoán / giới tính): "
     "'edit text option → update text option; case edit text label thì đang update lại setting next page về "
     "default => KHÔNG FIX ĐƯỢC do đang map theo text'.\n"
     "Đối lập: r1203, r1207, r1211, r1215 — SORT option thì setting next page GIỮ NGUYÊN.",
     "feature-spec.md BR-10 XÁC NHẬN đúng cơ chế gây ra: 'next_page_setting JSON [{value: \"label\", pageId: N}] "
     "mapping option → trang tiếp. Khi lưu: rebuild next_page_setting từ danh sách option hiện tại để đảm bảo "
     "nhất quán'. Vì mapping neo theo `value` = text label nên đổi label thì mapping cũ không còn khớp và bị reset.",
     "Admin sửa 1 chữ trong nhãn câu trả lời là luồng rẽ nhánh của form bị reset âm thầm, không có cảnh báo. "
     "Mức độ ảnh hưởng hành vi người dùng cuối CAO.",
     "[Form rẽ nhánh — setting rẽ nhánh] Sửa text option làm reset next page",
     "",
     "⏳ CHƯA CÓ QUYẾT ĐỊNH — ô quyết định của Leader còn trống.\n"
     "TC hiện đang viết theo HIỆN TRẠNG và ghi rõ 'chạy để ghi nhận, chưa raise bug'.\n"
     "3 hướng để Leader cân nhắc: ① chấp nhận hiện trạng + thêm cảnh báo khi admin sửa label của item đang "
     "dùng làm điều kiện rẽ nhánh · ② đổi next_page_setting sang neo theo option_id thay vì text label "
     "(sửa BR-10, có migration) · ③ chặn sửa label giống như đang chặn đổi required / đổi kiểu chọn / xóa item "
     "(r1196-r1198)."],

    ["MT-10", "THẤP", "✅ ĐÃ CHỐT",
     "Message giới hạn 10MB của ảnh header khác nhau giữa 2 tab setting",
     "r606 (tab 共通デザイン設定 → ヘッダー・背景): ảnh > 10MB →「10MB以下のをアップしてください。」\n"
     "r894 (tab フォーム編集 → ảnh header của page): ảnh > 10MB →「10MBまでのファイルをアップロードできます」",
     "Spec không có message tiếng Nhật nào.",
     "Cùng 1 loại lỗi nhưng 2 message tiếng Nhật khác nhau ở 2 màn của cùng 1 tính năng.",
     "[Setting chung của page] Ảnh header quá 10MB · [Item hiển thị] Item 画像 quá 10MB",
     "Tạm thời giữ nguyên như hiện tại.",
     "✅ Đã sửa 2 TC: ghi rõ mỗi màn dùng message nào và KHÔNG raise bug về khác biệt này.\n"
     "Ghi nhận là nợ kỹ thuật — nếu sau này thống nhất message thì cập nhật lại 2 TC."],

    ["MT-11", "THẤP", "✅ ĐÃ CHỐT",
     "Message sau trả lời KHÔNG trim space nhưng message remind THÌ CÓ trim",
     "r2309 (message sau khi trả lời form): 'Có tự trim space đầu cuối hay không? → ko tự strim => đã check trên stg'\n"
     "r2480 (message của step remind): 'Có tự trim space đầu cuối hay không? → tự strim'",
     "Spec không mô tả xử lý khoảng trắng của 2 ô này.",
     "Hai ô nhập cùng loại (nội dung tin gửi cho LINE user), cùng giới hạn 5000 ký tự, cùng có nút chèn "
     "LINE名/友だち情報 nhưng xử lý khoảng trắng khác nhau.",
     "[Setting action sau trả lời] Message tự trim · [Setting remind] Message remind tự trim",
     "Thống nhất spec: Tự động trim space đầu cuối.",
     "✅ Đã sửa 2 TC: cả 2 ô đều expected TỰ TRIM.\n"
     "⚠️ DỰ KIẾN FAIL ở nhánh message sau trả lời form (r2309 ghi hiện trạng không trim) → RAISE BUG để dev sửa.\n"
     "Đề xuất bổ sung vào feature-spec.md 1 BR về chuẩn hóa input: trim space đầu-cuối cho mọi ô nội dung tin nhắn."],

    ["MT-12", "THẤP", "✅ ĐÃ CHỐT",
     "Khoảng điểm chẩn đoán có điểm đầu = điểm cuối: cho phép hay không?",
     "r2603: 'Check validate 1 khoảng point → Bằng nhau' → kết quả mong đợi ghi nguyên văn: "
     "'Có cho phép không ạ => Chị nghĩ cho phép được' (chưa chốt chính thức).\n"
     "r2604: điểm đầu > điểm cuối →「終了ポイントは開始ポイントより、大きく入力してください。」",
     "feature-spec.md không có BR cho validate khoảng điểm chẩn đoán.",
     "Message lỗi ở r2604 nói 'điểm cuối phải LỚN HƠN điểm đầu' — theo nghĩa đen thì bằng nhau không hợp lệ, "
     "trái với ghi chú 'chị nghĩ cho phép được'.",
     "[Setting chẩn đoán] Validate khoảng điểm",
     "Có cho phép nhập point start = point end (trường hợp action với point đúng bằng 1 số nào đó).",
     "✅ Đã sửa TC: 5-5 lưu được, bổ sung bước verify action kích hoạt khi user đạt đúng 5 điểm.\n"
     "⚠️ Nếu hệ thống chặn cả 5-5 (theo nghĩa đen của message) thì RAISE BUG.\n"
     "Đề xuất bổ sung BR validate khoảng điểm vào feature-spec.md: start ≤ end (cho phép bằng nhau)."],

    ["MT-13", "THẤP", "✅ ĐÃ CHỐT",
     "Chuyển tab khi chưa lưu ở tab 各種設定 — giữ giá trị đã sửa hay revert?",
     "r355 (TC-NEW-11 của Bug #36428): 'Bước (c): tab 5 nhớ giá trị đã đổi ở (a) (HOẶC revert về saved value "
     "— TUỲ SPEC). Behavior nhất quán.'",
     "feature-spec.md §SCR-FA11-07 mô tả tab 各種設定 nhưng không mô tả hành vi khi chuyển tab chưa lưu.",
     "TC gốc để ngỏ 2 hành vi ngược nhau và chỉ yêu cầu 'nhất quán' → không có kết quả mong đợi đo lường được.",
     "[Setting chung của form] Chuyển tab khi chưa lưu",
     "Nhớ giá trị đã đổi ở tab 各種設定.",
     "✅ Đã sửa TC: expected = tab 各種設定 NHỚ giá trị vừa đổi, không revert.\n"
     "Đề xuất bổ sung hành vi này vào §SCR-FA11-07 của feature-spec.md."],

    ["MT-14", "CAO", "✅ ĐÃ CHỐT",
     "Xóa form rồi khôi phục: số người trả lời về 0 hay giữ nguyên? — 2 dòng trong CÙNG tab master nói ngược nhau",
     "r1940-r1941 (mục Xóa form): 'form-result: XÓA TOÀN BỘ; số count user trả lời form: UPDATE = 0'.\n"
     "r314 (mục Recover count): 'Check khi xóa form => phôi phục → SAU KHI KHÔI PHỤC COUNT FRIEND VẪN NHƯ CŨ'.",
     "feature-spec.md BR-07 (Soft delete 90 ngày) ghi RÕ: 'Khi soft-delete: `count_user_reply` reset về 0.' "
     "→ spec ĐỒNG Ý với r1940-r1941 và BÁC BỎ r314.",
     "Nếu xóa form thực sự xóa hết form-result và đưa count về 0 thì KHÔNG THỂ khôi phục count như cũ. "
     "Hai mô tả loại trừ lẫn nhau. Ảnh hưởng trực tiếp tới dữ liệu khách hàng.",
     "[Xóa & khôi phục form] Khôi phục form · [Màn kết quả trả lời] Xóa form rồi khôi phục",
     "Khi khôi phục form: số người trả lời vẫn bằng 0 (vì khi xóa form là đã phải reset số người trả lời rồi).",
     "✅ Đã sửa 2 TC: expected = sau khôi phục count = 0人, màn kết quả trả lời TRỐNG. Khớp spec BR-07.\n"
     "⚠️ Nếu chạy thấy count được khôi phục lại thì RAISE BUG (r314 mô tả sai).\n"
     "Đề xuất: sửa/xóa dòng r314 trong file TCs gốc để tránh tester khác hiểu nhầm."],

    ["MT-15", "CAO", "✅ ĐÃ CHỐT",
     "Ngắt quyền truy cập Google từ phía Google — có hiển thị cảnh báo mất liên kết không?",
     "r401: Kết quả mong đợi ghi 'Hiển thị alert báo mất liên kết google' nhưng ô kết quả ghi "
     "'CHƯA HIỂN THỊ ALERT'.\n"
     "r435 (Support #32733, 11/2025): cách fix chỉ nói thêm cột lưu email, không nói về alert.",
     "feature-spec.md BR-08 mô tả kết nối Google OAuth và queue đồng bộ nhưng KHÔNG mô tả hành vi khi "
     "quyền bị thu hồi từ phía Google.",
     "Không rõ đây là bug chưa fix hay đã đổi spec sang cơ chế khác. Nếu không cảnh báo thì khách mất sync "
     "Google mà không biết cho tới khi mở file kiểm tra.",
     "[Liên kết Google Sheet] Ngắt quyền truy cập Google",
     "Expect: Khi ngắt quyền truy cập từ phía Google thì CÓ hiển thị modal cảnh báo đã bị mất liên kết.",
     "✅ Đã sửa TC: expected = hiển thị modal cảnh báo mất liên kết, có lối liên kết lại.\n"
     "⚠️ DỰ KIẾN FAIL (r401 ghi hiện trạng chưa hiển thị alert) → RAISE BUG.\n"
     "Đề xuất bổ sung vào BR-08 của feature-spec.md: cơ chế phát hiện mất quyền và modal cảnh báo."],

    ["MT-16", "CAO", "✅ ĐÃ CHỐT",
     "Sheet có ô cột A trống ở GIỮA vùng data — dòng mới có được phép ghi đè dòng phía dưới?",
     "Tab「Sync google」r469 (TC-NEW-02): expected 'Dòng mới ghi vào cuối vùng data... toàn bộ 5 dòng cũ giữ "
     "nguyên' NHƯNG kèm ghi chú '⚠️ Nếu dòng mới ghi đè lên dòng 4/5 → đây là hành vi mà PM ĐÃ CHỐT chấp nhận, "
     "lỗi KH'.\nr470 (TC-NEW-04): 'TC này KHÔNG có expected pass/fail cứng — mục tiêu là đo hành vi'.",
     "feature-spec.md BR-08 + Gap #11: 'Job AddResultFormAnswerToGoogleSpreadSheet hiện bị comment out — "
     "sync có thể đang dùng cơ chế khác' → spec KHÔNG mô tả được cơ chế xác định vị trí ghi dòng mới.",
     "Cùng 1 TC vừa ghi expected 'không ghi đè' vừa ghi 'nếu ghi đè thì PM đã chấp nhận'. Tester không biết "
     "phải raise bug hay pass. Hậu quả: mất dữ liệu câu trả lời trên sheet của khách.",
     "[Sync Google Sheet & job] Sheet có ô cột A trống",
     "Sheet có ô cột A trống ở GIỮA vùng data — dòng mới KHÔNG được phép ghi đè dòng phía dưới. "
     "Expect: sẽ ghi vào từ dòng thứ 6 nếu sheet đang có 5 dòng data.",
     "✅ Đã sửa TC: expected cứng = ghi vào dòng thứ 6 khi sheet có 5 dòng data, TUYỆT ĐỐI không ghi đè.\n"
     "⚠️ Quyết định cũ của PM ('chấp nhận ghi đè, lỗi KH') KHÔNG còn hiệu lực — nếu thấy ghi đè thì RAISE BUG.\n"
     "Đề xuất: cập nhật BR-08 + đóng Gap #11 của feature-spec.md bằng cơ chế sync thực tế (job batch + retry "
     "mô tả ở tab Sync google 07/2026)."],

    ["MT-17", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Kiểu validate 整数 (số nguyên) có chấp nhận số thập phân không?",
     "Line user r166: 'Admin setting Validate input nhập là số nguyên 整数' → chỉ ghi 'Check validate input'.\n"
     "r1281: dropdown 入力制限 liệt kê 5 lựa chọn (カナ / メールアドレス / 電話番号 / 整数 / 日付) — KHÔNG có 数値.\n"
     "Line user r1438 (SpecChange #34855, 03/2026): '[Form] KHÔNG THỂ NHẬP DẤU THẬP PHÂN'.",
     "feature-spec.md BR-11 (Validation rules câu hỏi) chỉ liệt kê: required / email / regex_kana / regex "
     "(số điện thoại) / **numeric: true** — KHÔNG tách 整数 và 数値.",
     "Tên kiểu validate là 整数 (số NGUYÊN) nhưng spec-change lại yêu cầu cho nhập số thập phân. "
     "Spec BR-11 chỉ có 1 kiểu `numeric` nên không diễn tả được yêu cầu mới.",
     "[Item câu hỏi — chung] Dropdown 入力制限 có 6 lựa chọn · [LINE user] Validate 整数 · "
     "[LINE user] Validate 数値 · [LINE user] Validate các kiểu còn lại",
     "Chốt spec: 入力制限 có các giá trị ・整数（小数点なし）・数値（小数点あり）.\n"
     "Validate: ① 整数 (số nguyên) — không có số thập phân; nhập số thập phân/khác số nguyên → "
     "「整数で入力してください」. ② 数値 (số) — có thể nhập số thập phân; nhập sai format → 「半角数字で入力してください」.",
     "✅ Đã TÁCH TC validate thành 3 TC: 整数 · 数値 · các kiểu còn lại; THÊM 1 TC cho dropdown 入力制限 "
     "6 lựa chọn.\n"
     "⚠️ DỰ KIẾN FAIL nếu hệ thống chưa có lựa chọn 数値 → RAISE BUG / ticket triển khai.\n"
     "BẮT BUỘC sửa spec: BR-11 của feature-spec.md phải tách `numeric` thành 2 rule "
     "(整数 không thập phân / 数値 có thập phân) kèm 2 message tương ứng."],

    ["MT-18", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Form mới BỎ setting 'action 1 lần / nhiều lần' vốn có ở form cũ",
     "Line user r960-r963: kết quả mong đợi ghi 'form mới KHÔNG có setting action 1 lần/nhiều lần nên sẽ "
     "LUÔN ACTION được cho user'.\n"
     "Đối lập: r2364-r2367 cho thấy form MỚI VẪN CÓ setting「1度のみアクション稼働」ở tab action.",
     "feature-spec.md §SCR-FA11-05 (tab メッセージ・アクション設定) không mô tả setting số lần chạy action.",
     "Hai chỗ trong cùng corpus nói ngược nhau về việc form mới có setting này hay không.",
     "[Form cũ & tương thích] Form cũ recover thành kiểu action nhiều lần · "
     "[Form cũ & tương thích] Form mới có đủ 2 kiểu action · [Setting action sau trả lời] 1度のみアクション稼働",
     "Human đã viết sai expect. Expect đúng là: form cũ tạo trước 01/2025 KHÔNG có kiểu action 1 lần/nhiều lần. "
     "Form mới thì CÓ chia 2 kiểu này. Nên form cũ sẽ recover sang kiểu action nhiều lần và luôn action được cho user.",
     "✅ Đã sửa và TÁCH thành 2 TC: (a) form cũ trước 01/2025 → recover thành kiểu nhiều lần, luôn action; "
     "(b) form mới → có đủ 2 kiểu, bật 1度のみ thì lần 2 không action.\n"
     "Đề xuất: sửa dòng r960-r963 trong file TCs gốc (expect sai) + bổ sung setting 1度のみアクション稼働 "
     "vào §SCR-FA11-05 của feature-spec.md."],

    ["MT-19", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "Phạm vi quyền của account staff ở màn liên kết Google và ở các thao tác nhạy cảm",
     "r478 (liên kết google), r153 (copy form), r199 (export CSV), r316, r1130-r1133 (tạo form/page), "
     "r2456 (xóa remind), r2970, r3104, r3634-r3637 — TẤT CẢ chỉ có tiêu đề 'Check account staff', "
     "KHÔNG dòng nào ghi kết quả mong đợi.",
     "feature-spec.md §1 Actors ghi: 'Staff — Tùy theo quyền được Admin phân, CÓ THỂ BỊ GIỚI HẠN MỘT SỐ "
     "CHỨC NĂNG' → spec để ngỏ, không liệt kê chức năng nào bị giới hạn.",
     "Không biết staff được phép làm gì và bị chặn ở đâu, đặc biệt với thao tác ảnh hưởng toàn bot như "
     "liên kết/hủy liên kết Google account.",
     "[Liên kết Google Sheet] Account staff · [Phân quyền & môi trường] Staff có quyền Form",
     "Khi staff được cấp quyền truy cập màn quản lý form thì sẽ có quyền thao tác MỌI tính năng trong màn hình "
     "này, bao gồm cả: liên kết google, copy, tạo form...",
     "✅ Đã sửa 2 TC: expected = staff thao tác được đầy đủ, không thao tác nào bị chặn.\n"
     "BẮT BUỘC sửa spec: §1 Actors của feature-spec.md đang ghi 'có thể bị giới hạn một số chức năng' — "
     "phải sửa thành 'staff có quyền form thì thao tác được mọi chức năng trong màn hình form'."],

    ["MT-20", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "MỚI (phát hiện sau khi có spec) — 回答制限 có 2 hay 3 chế độ? corpus và spec không khớp",
     "r2662-r2667: chỉ mô tả 2 nhánh — 'không giới hạn' (reply_kind=0) và 'có giới hạn' với số lần "
     "(limit_reply_friend). r2688-r2689 (form cũ): 'trả lời 1 lần → reply_kind=1' và "
     "'trả lời nhiều lần → reply_kind=0' — tức reply_kind=1 nghĩa là CHỈ 1 LẦN.",
     "feature-spec.md BR-03: `reply_kind=0` vô hạn · `reply_kind=1` CHỈ 1 LẦN (đếm từ form_answer_result) · "
     "`reply_kind=2` giới hạn số lần cụ thể (theo dõi qua form_answer_user_accept).\n"
     "Gap #3 của spec: 'Cột count_reply trong form_answer_user_accept — schema dump KHÔNG thấy cột này "
     "nhưng BR-03 (reply_kind=2) cần nó'.",
     "Corpus mô tả UI chỉ có 2 lựa chọn (không giới hạn / có giới hạn + nhập số) trong khi spec có 3 giá trị "
     "reply_kind. Không rõ khi admin nhập số = 1 thì hệ thống lưu reply_kind=1 hay =2 — 2 nhánh này dùng 2 "
     "cơ chế đếm KHÁC NHAU (form_answer_result vs form_answer_user_accept), nên kết quả có thể khác nhau.",
     "[Setting chung của form] Mục 回答制限 có ĐÚNG 2 setting độc lập · [Setting chung của form] "
     "友だち1人あたりの回答制限 · [Setting chung của form] フォーム全体の回答制限 · "
     "[Setting chung của form] Form cũ setting trả lời 1 lần",
     "GUI có 2 setting giới hạn:\n"
     "+ 友だち1人あたりの回答制限: Giới hạn lượt trả lời form của mỗi friend (có thể setting không giới hạn "
     "hoặc giới hạn một số cụ thể)\n"
     "+ フォーム全体の回答制限: Giới hạn tổng số lượt trả lời của form hiện tại (có thể setting không giới hạn "
     "hoặc giới hạn một số cụ thể)",
     "✅ Đã THÊM 1 TC mới xác nhận mục 回答制限 có ĐÚNG 2 setting độc lập, mỗi setting 2 chế độ; đã gắn tên JP "
     "chính xác cho 3 TC sẵn có (giới hạn theo friend / giới hạn toàn form / form cũ).\n"
     "BẮT BUỘC SỬA SPEC: BR-03 của feature-spec.md đang mô tả MỘT trường `reply_kind` với 3 giá trị (0 vô hạn / "
     "1 chỉ 1 lần / 2 giới hạn số lần) — KHÔNG khớp cấu trúc GUI thật (2 setting độc lập, mỗi setting 2 chế độ). "
     "Phải viết lại BR-03 thành 2 rule riêng và map lại cột DB cho từng setting.\n"
     "Đồng thời đóng Gap #3 của spec (cột đếm của `form_answer_user_accept`) sau khi map lại."],

    ["MT-21", "THẤP", "✅ ĐÃ CHỐT",
     "MỚI (phát hiện sau khi có spec) — BR-10 thiếu kiểu next_page 'chuyển sang trang chỉ định'",
     "r1136-r1139, r1217-r1220, r1232-r1239: form rẽ nhánh có 3 kiểu setting next page — "
     "① next sang page chỉ định (chọn page bất kỳ từ select box) · ② rẽ nhánh theo câu trả lời của item · "
     "③ kết thúc form 回答完了ページ. Feature #29517 (04/2025) sửa spec cho chọn page bất kỳ.",
     "feature-spec.md BR-10 chỉ liệt kê 2 giá trị: `next_page_type = 2` (phân nhánh theo câu trả lời) và "
     "`= 3` (kết thúc form). KHÔNG có giá trị nào cho 'chuyển sang trang chỉ định'.",
     "Spec thiếu 1 trong 3 kiểu next page mà UI đang có (nhiều khả năng là next_page_type=1 nhưng spec "
     "không ghi). Người đọc spec sẽ tưởng form rẽ nhánh chỉ có 2 chế độ.",
     "[Form rẽ nhánh — setting rẽ nhánh] Setting chuyển trang có ĐÚNG 3 kiểu · "
     "[Form rẽ nhánh — setting rẽ nhánh] Chọn next page bất kỳ · "
     "[Form rẽ nhánh — setting rẽ nhánh] LINE user trả lời item rẽ nhánh",
     "Có 3 kiểu rẽ nhánh:\n"
     "+ form_answer_page.next_page_type = 1: Next sang page chỉ định 指定のページ\n"
     "+ form_answer_page.next_page_type = 2: Rẽ nhánh theo câu trả lời của item 指定のページ（分岐を設定する）\n"
     "+ form_answer_page.next_page_type = 3: Kết thúc form 回答完了ページ",
     "✅ Đã THÊM 1 TC mới liệt kê và verify đủ 3 kiểu chuyển trang kèm nhãn JP; đã gắn đúng next_page_type "
     "cho 2 TC sẵn có (type 1 ở TC chọn page bất kỳ, type 2 ở TC LINE user đi theo nhánh).\n"
     "BẮT BUỘC SỬA SPEC: BR-10 của feature-spec.md phải bổ sung `next_page_type = 1` (指定のページ) — hiện chỉ "
     "liệt kê type 2 và 3."],

    ["MT-22", "TRUNG BÌNH", "✅ ĐÃ CHỐT",
     "MỚI (phát hiện sau khi có spec) — spec mô tả cơ chế sync Google Sheet đã LỖI THỜI so với corpus",
     "Tab「Sync google」(03/2026 → 07/2026) mô tả cơ chế HIỆN TẠI rất chi tiết: job sync theo BATCH "
     "(500 record/lần gọi — SpecImprove #38859, 07/2026) · bảng hàng đợi retry với chuỗi backoff "
     "1p→5p→10p→30p→60p · trạng thái PROCESSING được reset khi restart app · lock theo form_id · "
     "config số luồng MAX_SYNC_GOOGLE_SHEET_THREAD mặc định 5.",
     "feature-spec.md BR-08: 'Kết quả submit được đồng bộ qua form_answer_connect_googles queue. "
     "Job AddResultFormAnswerToGoogleSpreadSheet HIỆN BỊ COMMENT OUT — sync có thể đang dùng cơ chế khác.'\n"
     "Gap #11: 'Google Sheets sync mechanism — cơ chế sync thực tế chưa được document đầy đủ'.\n"
     "§9: Background job ghi là `AddResultFormAnswerToGoogleSpreadSheet` (hiện bị comment out).",
     "Spec tự nhận không biết cơ chế sync thực tế, trong khi corpus TCs đã mô tả đầy đủ cơ chế mới. "
     "32 TC nhóm 'Sync Google Sheet & job' đang không có spec để đối chiếu.",
     "Toàn bộ 32 TC nhóm [Sync Google Sheet & job]",
     "Cơ chế sync hiện tại theo BATCH => Chốt update spec theo TCs.",
     "✅ TCs GIỮ NGUYÊN (đã mô tả đúng cơ chế hiện tại) — chỉ bổ sung ghi chú quyết định vào TC job batch.\n"
     "BẮT BUỘC SỬA SPEC — viết lại BR-08 của feature-spec.md theo 32 TC nhóm Sync:\n"
     "① job sync chạy theo BATCH, 500 record / 1 lần gọi ghi (SpecImprove #38859, 07/2026)\n"
     "② bảng hàng đợi retry với chuỗi backoff 1p → 5p → 10p → 30p → 60p, quá 5 lần thì đánh dấu lỗi hẳn\n"
     "③ bản ghi ở trạng thái PROCESSING được reset về NEW khi restart ứng dụng\n"
     "④ lock theo `form_id` — mỗi form chỉ 1 luồng xử lý tại 1 thời điểm\n"
     "⑤ config `MAX_SYNC_GOOGLE_SHEET_THREAD`, mặc định 5 luồng khi thiếu config\n"
     "⑥ xóa mô tả cũ 'job AddResultFormAnswerToGoogleSpreadSheet bị comment out' ở BR-08 và §9\n"
     "⑦ ĐÓNG Gap #11 của feature-spec.md."],
]
