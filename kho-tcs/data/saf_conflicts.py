# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ ĐANG CHỜ QUYẾT ĐỊNH của Leader (2026-08-26).

Nguồn TCs: 05. TCsLine_Setting kết bạn (3 tab) + TCsLine_JOB/Improve chung (tab
「Test callback friend」) + 15.3 TCsLine_ChangeBot + TCsLine_QLStaff.
Nguồn spec: spec-features/admin/setting-add-friend/ (chốt 2026-05-22).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "QRコードアクション (landing QR) có GHI ĐÈ HOÀN TOÀN cấu hình あいさつメッセージ không? "
     "Phải chốt TRƯỚC vì chi phối ~20 TC của 2 nhóm 15-16",
     "Tab master「Improve setting add fr 2.0」nói CẢ HAI cùng chạy khi landing bật tùy chọn "
     "kích hoạt あいさつメッセージ:\n"
     "• r52: kết bạn mới qua landing → gửi tin+action của landing, VÀ gửi THÊM tin+action của "
     "trang 新規友だち用\n"
     "• r53: landing áp dụng mọi friend → nếu friend là bạn mới thì gửi thêm cấu hình 新規友だち用\n"
     "• r149: friend cũ quét landing → gửi thêm cấu hình 既存友だち用\n"
     "• r287, r289: friend đang block quét landing → gửi thêm cấu hình ブロック解除時用\n"
     "• r55, r56 (và r151-r152, r290-r291): landing thiếu action hoặc thiếu tin nhắn → VẪN dùng "
     "action / tin nhắn của trang あいさつメッセージ\n"
     "• r205 (khối mô tả cách fix): 『Sửa lại thứ tự action của addFriendSetting TRƯỚC rồi đến "
     "action LandingQR để scenario lấy của LandingQR (nếu có)』— tức cả hai đều chạy, chỉ khác "
     "thứ tự",
     "job-spec.md:127: 『if (landingQR != null) → addFriendSetting = null  // Landing QR override "
     "hoàn toàn add_friend_setting』\n"
     "job-spec.md:328: 『Có Landing QR → add_friend_setting bị bỏ qua, chạy action của Landing QR "
     "thay thế』\n"
     "feature-spec.md §7 (khối『Hành vi Landing QR — Điểm quan trọng』): 『Khi người dùng LINE click "
     "vào Landing QR trước khi thêm bạn, toàn bộ cấu hình add_friend_setting bị BỎ QUA HOÀN TOÀN』",
     "Hai nguồn nói NGƯỢC NHAU về hành vi mà LINE user nhìn thấy: theo TC thì friend nhận 2 tin "
     "nhắn (landing + あいさつメッセージ), theo spec thì chỉ nhận 1 tin (landing). Đây là khác biệt "
     "nhìn thấy được bằng mắt ở phía khách hàng cuối. Nhiều khả năng spec bỏ sót tùy chọn "
     "「あいさつメッセージを稼働させる」ở màn QRコードアクション (xem MT-02) — nhưng không được tự "
     "kết luận. Toàn bộ nhóm『Ưu tiên với QRコードアクション』và『Thứ tự & loại action khi trùng "
     "landing』phụ thuộc quyết định này.",
     "Toàn bộ nhóm「Ưu tiên với QRコードアクション」(11 TC) và「Thứ tự & loại action khi trùng "
     "landing」(11 TC)",
     "",
     "Chốt xong phải: ① xác nhận tùy chọn kích hoạt あいさつメッセージ ở màn QRコードアクション có "
     "tồn tại và tên chính xác là gì; ② sửa job-spec.md:122-129 và :328 để mô tả đúng nhánh "
     "『landing có bật tùy chọn → chạy CẢ HAI, add_friend_setting trước, landing sau』; ③ sửa "
     "feature-spec.md §7 khối cảnh báo; ④ nếu chốt theo spec thì đánh dấu ~20 TC là DỰ KIẾN FAIL "
     "và raise bug."],

    ["MT-02", "CAO", W,
     "Tùy chọn「あいさつメッセージを稼働させる」ở màn QRコードアクション KHÔNG có trong spec FA-007",
     "Tab master nhắc tới tùy chọn này nhiều lần:\n"
     "• r93: 『check khi setting ON/OFF chọn vào option \"あいさつメッセージを稼働させる\" → có gửi "
     "action add new friend khi qr đang OFF, và ở landing có chọn option send new friend』\n"
     "• r248-r252 (case 13): 『KHi landing OFF — chọn option: あいさつメッセージを稼働させる』kèm "
     "ma trận 4 dòng cho action scenario\n"
     "• r52-r56, r149-r152, r287-r291 dùng các cờ use_msg_new_friend / use_msg_old_friend / "
     "use_msg_unblock — chính là biểu hiện ở tầng dữ liệu của tùy chọn này",
     "Toàn bộ spec-features/admin/setting-add-friend/ KHÔNG có bất kỳ dòng nào nhắc tới tùy chọn "
     "này. feature-spec.md §8 chỉ ghi『Landing QR (tính năng chưa spec) — Override hoàn toàn "
     "add_friend_setting khi user đến qua Landing QR link』.",
     "Nếu tùy chọn có thật thì spec FA-007 thiếu hẳn một điều kiện quyết định việc tin nhắn chào "
     "mừng có được gửi hay không — tester đọc spec sẽ không bao giờ nghĩ tới việc phải vào màn "
     "QRコードアクション để bật/tắt. Đây cũng là gốc rễ của MT-01.",
     "TC「Landing đang TẮT nhưng có bật tùy chọn kích hoạt あいさつメッセージ」và toàn bộ nhóm "
     "「Ưu tiên với QRコードアクション」",
     "",
     "Chốt xong phải: ① xác nhận tên và vị trí chính xác của tùy chọn trên màn QRコードアクション; "
     "② bổ sung vào feature-spec.md §5 một BR mô tả quan hệ landing ↔ あいさつメッセージ; "
     "③ bổ sung vào job-spec.md nhánh xử lý theo cờ này; ④ cân nhắc gom TC liên quan sang feature "
     "FA-017 QRコードアクション khi màn đó được /collect-tcs."],

    ["MT-03", "TRUNG BÌNH", W,
     "Trang 既存友だち用 CÓ hay KHÔNG có khối「友だち追加URL」+ QR code?",
     "Tab master r355-r374 (khối『check ở màn setting-add-friend-old』) mô tả ĐẦY ĐỦ khối "
     "友だち追加URL trên trang 既存友だち用: Title · URL không edit được · nút Copy (hover/click "
     "1 lần/2 lần) · ảnh QR không click được · nút Download (hover/click 1/2/N lần) · link "
     "「LINE公式アカウントの友だち追加URLとの違い」— tổng 17 dòng, kết quả thực thi đều OK.",
     "ui-spec.md:104: 『Lưu ý khác biệt so với SCR-SAF-01: Trang 既存友だち用 **không** hiển thị "
     "khu vực URL/QR code trong snapshot quan sát được.』\n"
     "ui-spec.md:342 (bảng điểm chưa rõ #2): 『Trang 既存友だち用 có hiển thị URL/QR không? — "
     "Snapshot SCR-SAF-02 không thấy khu vực URL/QR』\n"
     "feature-spec.md §2.2: 『Không hiển thị khu vực URL/QR code (trang bạn cũ không cần deep "
     "link)』\n"
     "feature-spec.md §9 Open Question #3 đặt đúng câu hỏi này.",
     "Spec tự nhận đây là điểm CHƯA CHẮC (dựa trên 1 snapshot), còn TC mô tả rất chi tiết như đã "
     "test thật. Đối chứng thêm: gọi live MCP môi trường dev ngày 2026-08-26, API lấy cấu hình với "
     "type=add_old VẪN trả về urlAddFriend và qrCode → phía server có cấp dữ liệu cho trang này. "
     "Chưa đủ để kết luận UI có render hay không.",
     "TC「Khối 友だち追加URL cũng hiển thị trên trang 既存友だち用 và ブロック解除時用」",
     "",
     "Chốt xong phải: ① chụp lại màn 既存友だち用 trên production; ② sửa ui-spec.md:104 và "
     "feature-spec.md §2.2 cho khớp thực tế; ③ xoá Open Question #3 ở feature-spec.md §9."],

    ["MT-04", "TRUNG BÌNH", W,
     "Tiêu đề khối hướng dẫn ở tab テスト方法 của trang 既存友だち用 và ブロック解除時用 — "
     "có bị dùng chung tiêu đề của trang 新規友だち用 không?",
     "Tab master ghi tiêu đề khối là「新規友だち用アクションのテスト方法」ở CẢ BA trang:\n"
     "• r101 (trang 新規友だち用) — đúng\n"
     "• r193 (khối trang 既存友だち用) — vẫn ghi 新規友だち用アクションのテスト方法\n"
     "• r329 (khối trang ブロック解除時用) — vẫn ghi 新規友だち用アクションのテスト方法\n"
     "Cả 3 dòng đều có kết quả thực thi OK.",
     "ui-spec.md:190: khối hướng dẫn của trang ブロック解除時用 có tiêu đề "
     "「ブロック解除時用アクションのテスト方法」\n"
     "feature-spec.md §2.4 mô tả tab テスト方法 quan sát trên trang ブロック解除時用 với nội dung "
     "riêng (sơ đồ 2 bước ブロック&ブロック解除)\n"
     "tab「Improve setting add fr 1.0」(04/2023) r18 dùng tiêu đề「既存友だち用アクションの"
     "テスト方法」cho trang bạn cũ → tức bản 2023 ĐÃ có tiêu đề riêng cho từng trang",
     "Nếu tab master đúng thì đây là BUG hiển thị: 3 trang dùng chung 1 tiêu đề của trang 新規, "
     "gây hiểu nhầm cho khách hàng đang ở trang 既存/ブロック解除. Nếu ui-spec đúng thì TC gốc chỉ "
     "là copy-paste khi soạn bảng và phải sửa lại. Bản 1.0 (2023) đứng về phía『mỗi trang 1 tiêu "
     "đề riêng』, làm khả năng『TC copy-paste』cao hơn — nhưng không được tự kết luận.",
     "TC「Tab テスト方法 trang ブロック解除時用」và「Tab テスト方法 trang 既存友だち用」",
     "",
     "Chốt xong phải: ① chụp tab テスト方法 của cả 3 trang trên production; ② nếu là bug thì raise "
     "ticket; ③ bổ sung nội dung tab テスト方法 của trang 新規 và 既存 vào ui-spec.md (đóng luôn "
     "Gap #1 ở feature-spec.md §9)."],

    ["MT-05", "TRUNG BÌNH", W,
     "Marker「新規友だち」/「既存友だち」ở khối thông tin đầu trang — click được hay không?",
     "HAI KHỐI TRONG CÙNG 1 TAB NÓI NGƯỢC NHAU:\n"
     "• Khối cũ r7-r8, r28-r29, r121-r122, r125-r126, r259-r260, r263-r264: 『Marker 新規友だち — "
     "Hover: Không hiển thị gì · Click: Không click được』\n"
     "• Khối mới (dưới header r348, có link design aun-mypage + Adobe XD) r353: 『check khi click "
     "vào 新規友だち → hiển thị content: 新規友だちとは？ 初めてLINE公式アカウントを追加した友だち…』"
     "và r357 tương tự cho 既存友だち",
     "ui-spec.md:44-46 và :99-102 chỉ mô tả marker là phần text được tô nổi bật trong info box, "
     "KHÔNG nói marker có click được hay không, cũng không có popup định nghĩa nào.",
     "⚠️ Ở trường hợp này quy tắc『ưu tiên TC mới nhất』là căn cứ YẾU: hai khối nằm trong CÙNG 1 "
     "tab, không khối nào có cột ngày riêng, và tab master trải dài 05/2025 → 03/2026. Lý do thực "
     "sự chọn khối r348+ là: (a) mô tả chi tiết hơn, có nội dung popup cụ thể; (b) đi kèm link "
     "design mới và nằm chung khối với đợt improve『流入経路』— tức là đợt cải tiến sau; (c) khối "
     "cũ chỉ ghi kết quả phủ định chung chung. Spec không giúp phân xử vì im lặng.",
     "TC「Click marker 新規友だち」và「Click marker 既存友だち」",
     "",
     "Chốt xong phải: ① click thử marker trên production; ② bổ sung mô tả popup định nghĩa vào "
     "ui-spec.md §SCR-SAF-01/02; ③ nếu khối cũ đúng thì xoá 2 TC này khỏi kho."],

    ["MT-06", "TRUNG BÌNH", W,
     "Có tự động lưu tin nhắn khi click ra ngoài ô nhập không?",
     "Tab master có 3 dòng lặp ở cả 3 trang, nhưng CỘT KẾT QUẢ MONG ĐỢI ĐỂ TRỐNG:\n"
     "• r48-r50 (trang 新規), r145-r147 (trang 既存), r283-r285 (trang unblock): 『check tự động "
     "save msg khi click ra ngoài』với 3 nhánh: khi chèn LINE名 · khi chèn ＋友だち情報 · khi nhập "
     "msg. Cột kết quả thực thi ghi OK nhưng không nói OK nghĩa là CÓ hay KHÔNG auto-save.",
     "api-spec.md §EP-05: API lưu cấu hình 『Được gọi bằng AJAX khi Admin click nút 「保存」』 — "
     "chỉ có 1 đường lưu duy nhất là nút 保存.\n"
     "ui-spec.md:86, :125, :168: mỗi trang có 1 nút「保存」ở cuối trang.\n"
     "Không chỗ nào trong spec nhắc tới auto-save khi blur.",
     "Đây là hành vi quyết định việc admin có mất dữ liệu hay không khi quên bấm 保存 — nhưng "
     "chính TC gốc cũng không ghi kết quả mong đợi, nên không thể đọc ra từ corpus. Nếu KHÔNG có "
     "auto-save thì cần thêm cảnh báo rời trang khi còn thay đổi chưa lưu (hiện spec cũng không "
     "có).",
     "TC「Tự động lưu tin nhắn khi click ra ngoài ô nhập — có thật hay không?」",
     "",
     "Chốt xong phải: ① test trực tiếp trên production; ② nếu KHÔNG auto-save thì bổ sung yêu cầu "
     "cảnh báo rời trang vào ui-spec.md; ③ nếu CÓ auto-save thì bổ sung vào api-spec.md một đường "
     "lưu nữa và mô tả thời điểm kích hoạt; ④ sửa expected của TC cho khớp."],

    ["MT-07", "TRUNG BÌNH", W,
     "Giới hạn 5.000 ký tự có được kiểm ở tầng server không?",
     "Tab master r47, r144, r282 chỉ kiểm ở tầng giao diện: 『Khi Textbox >5000 ký tự → Chặn nhập "
     "ký tự thứ 5001 tại textbox, Hiển thị 5000/5000』. KHÔNG có TC nào gọi thẳng API.",
     "logic-spec.md:319-321: 『Validation Rules — Mức độ tin cậy: Trung bình — không có Laravel "
     "FormRequest riêng, validation chủ yếu ở frontend』\n"
     "logic-spec.md:325: 『message | Tối đa 5,000 ký tự | Nguồn: Từ UI (counter hiển thị "
     "x/5,000)』\n"
     "logic-spec.md:327: 『Không có validation middleware/FormRequest riêng cho FA-007』\n"
     "api-spec.md:208 chỉ ghi『Tối đa 5,000 ký tự』ở bảng tham số, không nói ai kiểm.",
     "Spec tự nói validation nằm ở frontend → tức backend nhiều khả năng KHÔNG chặn. Nếu vậy có "
     "thể lưu tin nhắn dài hơn giới hạn của LINE Messaging API, dẫn tới lỗi gửi tin cho toàn bộ "
     "friend mới. Corpus không kiểm điểm này nên không có bằng chứng.",
     "TC「Gọi thẳng API lưu với nội dung > 5.000 ký tự」",
     "",
     "Chốt xong phải: ① test gọi thẳng API; ② nếu backend không chặn thì raise ticket bổ sung "
     "validate phía server; ③ ghi rõ kết luận vào logic-spec.md §Validation Rules và nâng mức tin "
     "cậy lên Cao."],

    ["MT-08", "TRUNG BÌNH", W,
     "Giới hạn thời gian sử dụng (của landing) chặn luôn cả tin nhắn/action của あいさつメッセージ "
     "— spec FA-007 không có dòng nào",
     "Tab master lặp ở cả 3 trang: r62, r159, r295: 『check khi setting Có sử dụng giới hạn thời "
     "gian và nằm ngoài khoảng thời gian đó → Không gửi action_id bảng landing VÀ action/msg ở "
     "bảng add_friend_setting』— tức cấu hình chào mừng cũng bị chặn theo.",
     "Toàn bộ spec-features/admin/setting-add-friend/ KHÔNG có mô tả nào về giới hạn thời gian. "
     "job-spec.md §Luồng doHandleFollowEvent 8 bước và §Edge cases đều không nhắc.",
     "Nếu đúng thì có một điều kiện thời gian nằm ngoài màn あいさつメッセージ nhưng lại quyết định "
     "việc tin nhắn chào mừng có được gửi hay không — rủi ro cao là khách hàng cài xong mà tin "
     "không gửi và không hiểu vì sao. Cũng chưa rõ giới hạn này thuộc landing hay thuộc chính "
     "cấu hình chào mừng.",
     "TC「Landing có giới hạn thời gian, quét NGOÀI khoảng — không chạy cả action landing lẫn "
     "chào mừng」",
     "",
     "Chốt xong phải: ① xác định giới hạn thời gian này được cài ở màn nào; ② bổ sung vào "
     "job-spec.md một nhánh điều kiện trong luồng xử lý; ③ nếu là hành vi ngoài ý muốn thì raise "
     "ticket."],

    ["MT-09", "TRUNG BÌNH", W,
     "Nhãn trigger hiển thị kèm multi action ở màn chat 1:1 — spec không có mục nào",
     "Tab master r394-r407 (Bug Tester #33322, 03/2026) mô tả rất cụ thể:\n"
     "• Bạn mới → 『機能名 = 友だち追加時設定 · 詳細 = 新規友だち用アクション』(r404)\n"
     "• Bạn cũ → 『詳細 = 既存友だち用アクション』(r397, r398) — nội dung bug: đang hiện sai thành "
     "『ブロック解除友だち用アクション』(r395)\n"
     "• Bỏ block → 『詳細 = ブロック解除友だち用アクション』(r400-r403)\n"
     "• Qua landing → 『機能名 = QRコードアクション · 詳細 = URL読み込み』(r406, r407)",
     "Toàn bộ spec-features/admin/setting-add-friend/ KHÔNG có mục nào về nhãn trigger hiển thị "
     "phía chat 1:1. ui-spec.md chỉ mô tả 3 màn cấu hình + modal action.",
     "Đây là phần output mà admin nhìn thấy hằng ngày để biết action đến từ đâu, và đã từng có "
     "bug thật (#33322). Spec thiếu hẳn phần này nên lần sau sửa vùng phân loại loại bạn sẽ không "
     "ai biết phải kiểm lại nhãn trigger.",
     "Toàn bộ nhóm「Trigger hiển thị ở chat 1:1」(6 TC)",
     "",
     "Chốt xong phải: ① bổ sung bảng ánh xạ loại bạn ↔ nhãn trigger vào ui-spec.md hoặc "
     "logic-spec.md; ② ghi rõ đây là vùng ảnh hưởng bắt buộc kiểm khi sửa doHandleFollowEvent."],

    ["MT-10", "THẤP", W,
     "Job khôi phục action cho loại unblock — spec không có",
     "Tab master r341-r345: 『job recover action của unblock』với 2 nhánh kiểm: cấu hình cũ ở "
     "『bạn bè hiện tại』và『all friend』; sau khi recover thì action hiện ở menu "
     "setting_add_friend_new, setting old_friend và setting unblock.",
     "job-spec.md chỉ mô tả HandlePostbackTask xử lý callback follow. Không có job migration/"
     "recover nào. feature-spec.md §7 ghi rõ『Tính năng tin nhắn chào mừng không có job riêng』.",
     "Job này chạy 1 lần khi bổ sung loại unblock (trang thứ 3) — không còn chạy định kỳ. Ảnh "
     "hưởng thấp nhưng nếu còn bot chưa được migrate thì cấu hình unblock sẽ trống.",
     "TC「Job khôi phục action cho trang ブロック解除時用」",
     "",
     "Chốt xong phải: ① xác nhận job đã chạy xong cho toàn bộ bot chưa; ② nếu đã xong thì ghi "
     "chú vào job-spec.md như một mục lịch sử migration và đánh dấu TC là hồ sơ."],

    ["MT-11", "TRUNG BÌNH", W,
     "Fallback đời cũ (gắn tag / khởi động scenario theo cấu hình V1) — có còn chạy không, và "
     "UI có cho admin thấy không?",
     "Corpus TCs KHÔNG có bất kỳ TC nào cho nhánh này — không có bằng chứng test.",
     "feature-spec.md §5 BR-10 (mức tin cậy TRUNG BÌNH): 『Khi action_new_id hoặc action_old_id = "
     "null, Spring Boot job fallback sang new_tag_id/old_tag_id (gán tag trực tiếp) và "
     "new_scenario_id/old_scenario_id (khởi động scenario) — Đây là backward compatibility "
     "behavior, chưa được expose trên UI V2』\n"
     "feature-spec.md §9 mục 5: 『Fallback new_tag_id/old_tag_id trong logic-spec chưa được "
     "document』(VĐ-TBC-01, mức Trung bình)\n"
     "db-mapping.md:73: 『Cột new_tag_id, old_tag_id, new_scenario_id, old_scenario_id là hệ "
     "thống cũ (V1 legacy)』",
     "Spec tự nhận đây là điểm chưa document đủ, và corpus TCs cũng không phủ. Rủi ro: màn admin "
     "hiển thị「エルメアクションは登録されていません」nhưng thực tế friend vẫn bị gắn tag / vào "
     "scenario theo cấu hình đời cũ — admin không hiểu vì sao, không tắt được.",
     "TC「Bot chỉ có cấu hình đời cũ (tag/scenario V1), chưa có action V2」",
     "",
     "Chốt xong phải: ① xác nhận còn bot nào đang dùng nhánh fallback không; ② bổ sung mô tả "
     "fallback vào logic-spec.md (đóng VĐ-TBC-01); ③ nếu còn chạy thì quyết định có hiển thị lên "
     "UI V2 hay dọn dữ liệu cũ."],

    ["MT-12", "THẤP", W,
     "Số action tối đa hiển thị dưới nút アクション追加・編集 — 3 hay không giới hạn?",
     "HAI TAB CỦA CÙNG 1 FILE NÓI KHÁC NHAU:\n"
     "• tab「Improve setting add fr 1.0」(04/2023) r7-r8: 『Cho phép hiển thị tối đa 3 action · "
     "Nếu chọn >3 action → vẫn hiển thị detail 3 action set đầu tiên, text hiển thị その他 x 件 "
     "編集』\n"
     "• tab「Improve setting add fr 2.0」(05/2025) r68, r72, r76, r80, r84: 『Setting N action → "
     "Hiển thị CÁC action đã setting bên dưới button アクション追加・編集』— không nhắc giới hạn 3",
     "ui-spec.md:84 chỉ mô tả trạng thái rỗng「エルメアクションは登録されていません」, không nói gì "
     "về giới hạn hiển thị khi có nhiều action.",
     "Niên đại rõ ràng (2023 vs 2025) nên quy tắc『ưu tiên TC mới nhất』áp dụng được: bản 2.0 thắng, "
     "khối r7-r8 của tab 1.0 coi như đã bị đợt improve thay thế. Ghi lại để Leader biết vì sao "
     "TC cũ bị loại.",
     "TC「Cài N action — hiển thị đủ N action, đúng thứ tự đã cài」",
     "",
     "Chốt xong phải: ① đếm thực tế trên production khi cài >3 action; ② bổ sung mô tả cách hiển "
     "thị danh sách action vào ui-spec.md."],

    ["MT-13", "TRUNG BÌNH", W,
     "TC r99 có kết quả NG ở nguồn — landing trong filter đã bị xóa và đã đạt số lần action",
     "Tab master r99: 『check điều kiện khi qr nằm trong filter đó đã bị xóa — check khi landing "
     "đó đã thỏa mãn action = 2 → không send action nữa vì landing nằm trong filter đó đã bị "
     "xóa』. **Cột kết quả thực thi ghi NG** (chưa fix tại thời điểm test).",
     "Spec không mô tả quan hệ giữa filter của action và vòng đời của landing được dùng làm điều "
     "kiện filter.",
     "TC gốc ghi NG nghĩa là hành vi thực tế KHÁC kỳ vọng tại thời điểm test. Không rõ đã fix "
     "chưa. Theo RULE-11 chỉ ticket ở trạng thái đã đóng mới là bằng chứng — ở đây không có số "
     "ticket nào.",
     "TC「Landing trong filter đã bị xóa và landing đó đã đạt số lần action — action không chạy "
     "nữa」",
     "",
     "Chốt xong phải: ① kiểm tra lại trên production xem đã fix chưa; ② nếu chưa thì raise ticket; "
     "③ bổ sung mô tả hành vi vào logic-spec.md."],

    ["MT-14", "TRUNG BÌNH", W,
     "Danh sách 5 nút tắt ở khối「よく使われる項目」— gồm những nút nào?",
     "Tab master r65-r84 (và r165-r184, r300-r319) liệt kê 5 nút: テンプレート · タグ · 友だち情報 "
     "· ステップ配信 · その他 — mỗi nút mở modal action và focus sẵn tab tương ứng (riêng その他 "
     "không focus tab nào).",
     "ui-spec.md:78-83 liệt kê 5 nút KHÁC: 「ステップ配信を開始・停止する」·「リッチメニューを表示する」"
     "·「テンプレートを送信する」·「タグを付け・外しする」·「その他のアクションをみる」\n"
     "feature-spec.md §2.5 lặp lại đúng danh sách của ui-spec.",
     "Hai nguồn lệch ở nút thứ 3: TC ghi 友だち情報, spec ghi リッチメニュー. Ngoài ra cách đặt nhãn "
     "cũng khác (danh từ ngắn vs câu mô tả hành động) — có thể là đợt đổi giao diện giữa 05/2025 "
     "và 05/2026. Ảnh hưởng: 1 TC phải đổi hẳn đối tượng test.",
     "TC「Danh sách 5 nút tắt — đúng nhãn và đúng số lượng」và「Click nút tắt 友だち情報」",
     "",
     "Chốt xong phải: ① chụp khối よく使われる項目 trên production; ② sửa TC hoặc sửa ui-spec.md "
     "cho khớp; ③ đóng luôn Gap #2 của feature-spec.md §9 (behavior của 5 nút tắt) bằng kết quả "
     "TC đã có."],

    ["MT-15", "THẤP", W,
     "Mốc thời gian của link video hướng dẫn ở tab テスト方法 — t=56 hay t=354?",
     "Tab master r373: link 『https://www.youtube.com/watch?si=G27JAyP8DShazZmu&t=56&v="
     "9TTugIBdQGs&feature=youtu.be』 → mốc 56 giây.",
     "ui-spec.md:196 và feature-spec.md §2.4: 『https://youtu.be/9TTugIBdQGs?si="
     "tmu-rgxRz2wAy51z&t=354』 → mốc 354 giây.",
     "Cùng 1 video (id 9TTugIBdQGs) nhưng mốc nhảy tới khác nhau. Nhiều khả năng mỗi trang có mốc "
     "riêng (trang 新規 vs trang ブロック解除), nhưng cả 2 nguồn đều không nói rõ mốc đó thuộc trang "
     "nào.",
     "TC「Link テスト方法を動画で確認 — mở đúng video hướng dẫn trên YouTube」",
     "",
     "Chốt xong phải: ① kiểm tra link ở cả 3 trang trên production và ghi lại mốc của từng trang; "
     "② bổ sung vào ui-spec.md link riêng cho từng trang."],

    ["MT-16", "TRUNG BÌNH", W,
     "Hai câu hỏi treo ở tab「Ngần review」về action loại テキスト — đã xử lý chưa?",
     "File 05. TCsLine_Setting kết bạn → tab「Ngần review」(3 dòng, không có ngày):\n"
     "• r2: 『Action gửi lúc kết bạn — Action text đang bị gửi sau multi action』\n"
     "• r3: 『Chat 1:1 — 1. Action lại hiển thị trước cả tin nhắn của friend? 2. Action text chưa "
     "có trigger send từ đâu』",
     "Spec không mô tả thứ tự gửi giữa action loại テキスト và các action khác, cũng không mô tả "
     "trigger cho action text (liên quan MT-09).",
     "Đây là ghi chú review của Leader chứ không phải TC hoàn chỉnh (không có bước, không có kết "
     "quả mong đợi), nhưng nêu 2 nghi vấn về thứ tự hiển thị mà LINE user và admin nhìn thấy. Nếu "
     "chưa xử lý thì phải thành TC; nếu đã xử lý thì cần biết kết luận để viết expected.",
     "TC「Action loại テキスト ở cả 2 nơi — text của あいさつメッセージ gửi trước, landing sau」và "
     "nhóm「Trigger hiển thị ở chat 1:1」",
     "",
     "Chốt xong phải: ① trả lời 2 câu hỏi ở tab「Ngần review」; ② nếu là bug thì raise ticket; "
     "③ bổ sung thứ tự gửi action vào logic-spec.md."],

    ["MT-17", "TRUNG BÌNH", W,
     "Bot xóa follow rồi friend quét QR kết bạn lại — có tính là kết bạn không?",
     "Tab master r396: 『Check khi bot xóa follow friend — user quét qr kết bạn lại → **Hiện tại** "
     "trên step chưa tính là kết bạn: ko có trigger + ko có action』(kết quả OK STEP)\n"
     "NHƯNG r54 cùng tab lại nói: 『xóa follow => friend vào block bot => quét landing → send đúng "
     "msg … check bảng detail_landing_click: is_old_fried = 0』— tức có chạy và được tính là bạn "
     "mới.",
     "job-spec.md §Bước 1 phân loại 3 nhánh dựa trên: friend chưa tồn tại → bạn mới; friend đang "
     "bị đánh dấu block → unblock; còn lại → bạn cũ. Không mô tả nhánh『admin đã xóa follow』.",
     "Chính TC gốc dùng chữ『Hiện tại』cho thấy người test cũng nghi ngờ đây là hành vi tạm thời. "
     "Nếu đúng là không chạy gì thì admin xóa nhầm friend rồi friend quét QR lại sẽ không nhận "
     "được gì — im lặng, khó phát hiện. Hai dòng r396 và r54 mô tả 2 tình huống gần nhau nhưng "
     "kết luận ngược nhau.",
     "TC「Bot xóa follow, friend quét QR kết bạn lại — chưa tính là kết bạn, không có trigger」",
     "",
     "Chốt xong phải: ① test lại cả 2 tình huống (có/không block xen giữa) trên production; "
     "② bổ sung nhánh『đã xóa follow』vào job-spec.md §Bước 1; ③ nếu là bug thì raise ticket."],

    ["MT-18", "THẤP", W,
     "TC r399 ở trạng thái Pending — chưa có bằng chứng",
     "Tab master r399: 『Check khi bot xóa follow friend — user quét qr có tích option action "
     "friend cũ → Hiển thị trigger: 機能名 = QRコードアクション · 詳細 = URL読み込み』. **Cột kết "
     "quả thực thi ghi Pending** (chưa test xong).",
     "Spec không mô tả tùy chọn『action cho bạn cũ』ở màn QRコードアクション (liên quan MT-02).",
     "TC được giữ nguyên trong kho nhưng phải đánh dấu rõ là CHƯA CÓ BẰNG CHỨNG — không được coi "
     "expected này là hành vi đã xác nhận.",
     "TC「Bot xóa follow, friend quét QR có tích tùy chọn action bạn cũ — trigger nào hiển thị?」",
     "",
     "Chốt xong phải: ① chạy nốt TC này; ② ghi kết quả vào kho và cập nhật spec nếu cần."],
]
