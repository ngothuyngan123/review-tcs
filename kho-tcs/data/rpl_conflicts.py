# -*- coding: utf-8 -*-
"""FA-003 自動応答 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ CHỜ QUYẾT ĐỊNH của Leader.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

CONFLICTS = [
    ["MT-01", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Giới hạn 30 ký tự của keyword — spec KHÔNG ghi rule này ở bất kỳ đâu",
     "Bug tự detect #38413 (07/2026, Ver1.0 r174-r197 — khối MỚI NHẤT của tab master):\n"
     "• Nhập 200 ký tự → DB chỉ lưu 30 ký tự đầu\n• 31 ký tự → cắt còn 30; đúng 30 → giữ nguyên\n"
     "• Tiếng Nhật 200 ký tự → cắt còn 30 KÝ TỰ (không phải 30 byte)\n"
     "• Sửa keyword đã có, nhập 50 ký tự → update cũng chỉ 30\n"
     "• 5 keyword dài 10/20/31/50/300 → lưu 10/20/30/30/30 (cắt độc lập)",
     "• `db/db-mapping.md:101`: cột `keyword` = varchar(200), mô tả CHỈ ghi 'Duy nhất trong toàn bot'\n"
     "• `feature-spec.md` §4 Field Traceability #8「キーワード」: Validation = 'Bắt buộc ≥1 khi keyword mode'\n"
     "• `web/logic-spec.md:606-612` Validation Flow V2: KHÔNG có rule độ dài keyword\n"
     "→ Spec KHÔNG có chỗ nào nói tới con số 30",
     "Người đọc spec sẽ nhập keyword tới 200 ký tự (theo varchar(200)) và tin là lưu đủ. Thực tế hệ thống "
     "CẮT ÂM THẦM còn 30 → keyword người dùng LINE gõ sẽ KHÔNG BAO GIỜ khớp. Đây là mất chức năng, không phải lỗi UI.",
     "TC-RPL-* nhóm『Keyword — độ dài & trim』(9 TC)",
     "",
     "Nếu 30 ký tự là đúng: bổ sung vào feature-spec.md §4 field #8 + §5 Business Rules + logic-spec.md "
     "Validation Flow V2, ghi rõ cơ chế là TRUNCATE (cắt âm thầm) chứ không phải báo lỗi; đồng thời cân nhắc "
     "hiển thị cảnh báo trên UI vì cắt âm thầm là rủi ro UX."],

    ["MT-02", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Trim khoảng trắng: TC nói trim ĐẦU khi lưu, spec nói trimEnd khi so khớp — 2 tầng khác nhau, không tầng nào phủ tầng kia",
     "Bug #38413 (Ver1.0 r183-r184, r191-r192, r197):\n"
     "• 'Check case 30 ký tự trong đó có khoảng trắng đầu' → Expect: 'Tự trim khoảng trắng đầu'\n"
     "• 'Check case 40 ký tự trong đó có khoảng trắng đầu' → Expect: 'Tự trim khoảng trắng đầu, count từ ký tự "
     "khác khoảng trắng cho đủ 30 ký tự'\n→ Trim ở tầng LƯU, phía ĐẦU chuỗi",
     "• `job/job-spec.md:304`: 'Text input được `TextUtils.trimEnd()` trước khi truyền vào'\n"
     "• `feature-spec.md` §5 BR-18: 'Text input được TextUtils.trimEnd() trước khi so sánh'\n"
     "→ Trim ở tầng SO KHỚP runtime, phía CUỐI chuỗi",
     "Spec chỉ mô tả trimEnd ở runtime; TC chỉ mô tả trim đầu ở lúc lưu. Nếu keyword lưu là「abc」nhưng "
     "user LINE gõ「␣abc」thì có khớp không? Không tài liệu nào trả lời được. Đây là hành vi match keyword — "
     "ảnh hưởng trực tiếp việc auto reply có chạy hay không.",
     "TC-RPL-*『Keyword — độ dài & trim』(2 TC trim) + TC-RPL-*『Runtime — match keyword & gửi action』"
     "(TC khoảng trắng đầu/cuối)",
     "",
     "Chốt hành vi cho ĐỦ 4 ô: (lưu / so khớp) × (khoảng trắng đầu / cuối). Sau đó bổ sung vào "
     "logic-spec.md Validation Flow V2 (tầng lưu) và job-spec.md §Keyword Matching (tầng so khớp)."],

    ["MT-03", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Nhiều quy tắc cùng khớp 1 tin nhắn: spec nói CHẠY HẾT, TC cũ quyết định KHÔNG TEST",
     "Ver1.0 r25-r28 (khối 07/2023): 4 dòng case kết hợp (quy tắc all-keyword không tick + quy tắc keyword "
     "riêng có tick) đều đánh dấu **'Not test'**, lý do ghi ở cột Note: 'ko cần check case kết hợp này vì mỗi "
     "cái setting action riêng, thỏa mãn cái nào thì send action của setting đó ⇒ tương ứng với từng case check "
     "phía trên rồi'",
     "• `feature-spec.md` §5 BR-15 Multi-rule match: 'Nhiều rules có thể match đồng thời — vòng lặp KHÔNG break "
     "sau match đầu tiên. Mỗi rule match tạo riêng AutoReplyHistory entry' (HandlePostbackTask.java:1532-1628, "
     "tin cậy CAO)\n"
     "• §Ảnh hưởng: 'Nhiều actions có thể chạy cùng lúc cho 1 tin nhắn'",
     "TC cũ giả định các quy tắc độc lập nên không cần test kết hợp. Nhưng BR-15 nói rõ chúng chạy CHỒNG NHAU: "
     "1 tin nhắn có thể sinh N action → người dùng LINE nhận N tin cùng lúc. Đây là hành vi người dùng cuối "
     "nhìn thấy và là rủi ro spam / trùng tin.",
     "TC-RPL-*『Runtime — match keyword & gửi action』(TC BR-15 multi-rule) + "
     "TC-RPL-*『Checkbox 【〇〇】には反応させない』(TC kết hợp 2 quy tắc)",
     "",
     "Nếu chốt là phải test: đưa case multi-rule vào bộ TC chính, và bổ sung hướng dẫn cho khách hàng về rủi ro "
     "cấu hình nhiều quy tắc chồng nhau. Nếu chốt không test: ghi rõ lý do vào spec để lần sau không phải hỏi lại."],

    ["MT-04", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "「1度のみ / 何度でもアクション稼働」— field chính của form nhưng KHÔNG có TC nào ở tầng runtime",
     "Toàn bộ corpus chỉ có 1 dòng nhắc tới:\n"
     "• TCsLine_BackUp / Backup (job) r9: 'Action auto reply / setting action 1 lần/ nhiều lần' — và đây là TC "
     "**backup dữ liệu**, không phải TC hành vi\n"
     "→ KHÔNG có TC nào kiểm tra: friend gửi keyword lần 2 thì có nhận action nữa không",
     "• `feature-spec.md` §4 field #14「1度のみ」/「何度でも」→ `auto_reply.response_number` (0/1)\n"
     "• §5 BR-16 Only once: 'Nếu response_number = 0 và auto_reply_history đã có record cho cặp (lineId, replyId) "
     "→ skip rule' (HandlePostbackTask.java:1534, tin cậy CAO)",
     "Đây là 1 trong 2 radio button chính của Phần 5 trên form. Nếu logic sai, khách hàng cấu hình「1度のみ」"
     "nhưng bot spam mỗi lần user nhắn — hoặc ngược lại, cấu hình「何度でも」mà bot chỉ trả lời 1 lần. "
     "Cả 2 chiều đều là bug nghiêm trọng mà bộ TC hiện tại KHÔNG bắt được.",
     "TC-RPL-*『Form — số lần chạy & lưu quy tắc』(3 TC BR-16)",
     "",
     "Xác nhận 3 TC mới do AI viết có đúng hành vi mong đợi không, đặc biệt: (a) auto_reply_history tính theo "
     "cặp (line_id, reply_id) nên friend KHÁC vẫn nhận được; (b) khi sửa quy tắc thì history có bị xóa không "
     "(liên quan MT-13)."],

    ["MT-05", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "11 loại điều kiện lọc trong spec vs 5 loại có TC — 6 loại chưa từng được test cho auto reply",
     "TCsLine_Modal Filter / tab「Sửa filter autoreply」(08/2023, 86 TC lá) chỉ phủ 5 loại:\n"
     "タグ · ステップ購読状況 · コンバージョン · QRコードアクション · 友だち情報\n"
     "→ KHÔNG có TC cho: 友だち名 · 友だち追加日 · 確認状況 · 対応ステータス · アフィリエイター · 新規・既存友だち",
     "• `feature-spec.md` §SCR-RPL-03 liệt kê ĐỦ 11 loại điều kiện\n"
     "• Riêng loại #7「確認状況」ghi tin cậy **Thấp**: 'không tìm thấy type tương ứng trong FilterV2, có thể đã "
     "deprecated' (Gap TB-04)",
     "Modal filter là shared component SC-003 dùng chung với FA-002/FA-008/FA-009/FA-013/FA-024. "
     "6 loại chưa test cho auto reply có thể đã được test ở tính năng khác — nhưng cũng có thể không. "
     "Riêng「確認状況」còn chưa rõ có tồn tại thật hay không.",
     "TC-RPL-*『Form — lọc đối tượng 絞り込み』(TC đối chiếu 11 loại) + toàn bộ nhóm『Filter — *』",
     "",
     "① Chốt phạm vi: 6 loại còn lại có cần TC riêng cho auto reply, hay chấp nhận đã phủ ở SC-003 chung.\n"
     "② Mở UI thật kiểm tra「確認状況」có trong panel không → nếu không có thì xóa khỏi spec (đóng Gap TB-04)."],

    ["MT-06", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Ô tìm kiếm quy tắc: code có endpoint, UI spec không thấy, TC hoàn toàn không có",
     "Toàn bộ corpus (13 nguồn đã gộp) KHÔNG có bất kỳ TC nào cho chức năng tìm kiếm quy tắc auto reply",
     "• `feature-spec.md` §6 EP-06 có action `searchByKeyWord` (params: keyword, group_id), pseudo-code "
     "'JOIN auto_reply + keyword → LIKE %keyword%'\n"
     "• `ui/ui-spec.md` §SCR-RPL-01 KHÔNG liệt kê ô tìm kiếm nào trong toolbar hay bảng dữ liệu\n"
     "• Gap TB-03: 'Chức năng tìm kiếm keyword tồn tại trong code nhưng UI Spec không liệt kê ô tìm kiếm. "
     "Có thể ẩn khi danh sách trống (0 records)'",
     "Code có, UI chưa xác nhận, TC không có. Nếu ô tìm kiếm tồn tại thật thì đây là chức năng CHƯA BAO GIỜ "
     "được test. Nếu không tồn tại thì code có endpoint chết — vẫn là rủi ro bảo mật/bảo trì.",
     "TC-RPL-*『Tìm kiếm quy tắc』(3 TC do AI viết theo code)",
     "",
     "Mở màn /basic/reply có ≥1 quy tắc, xác nhận ô tìm kiếm có tồn tại không. Có → giữ 3 TC và đóng Gap TB-03; "
     "không → xóa 3 TC, ghi vào spec rằng EP-06 action searchByKeyWord không có lối vào UI."],

    ["MT-07", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Filter コンバージョン ĐK1: nhãn nói「全て」nhưng hành vi TC ghi nhận là「1つ以上」",
     "TCsLine_Modal Filter / Sửa filter autoreply r39-r41:\n"
     "• Tiêu đề điều kiện: 'ĐK1: user đã access **tất cả** các conversion được chọn'\n"
     "• Nhưng r40: 'user access 1 hoặc nhiều conversion nhưng **không phải tất cả**' → Expect: **CÓ action**\n"
     "• Chính người viết TC ghi chú ở cột Main Function: 'Logic hiện tại đang check user access 1 trong các "
     "conversion đã chọn ⇒ check theo logic này và confirm lại a Thắng chỗ filter này'",
     "`feature-spec.md` §SCR-RPL-03 chỉ liệt kê loại #6「コンバージョン」→ filter type `conversion`, KHÔNG mô tả "
     "ngữ nghĩa 4 điều kiện con (全て / 1つ以上 / 除く)",
     "TC tự mâu thuẫn với chính tiêu đề của nó, và người viết TC đã đánh dấu cần confirm nhưng chưa có câu trả lời "
     "trong corpus. Spec không mô tả điều kiện con nên không có căn cứ để phân xử. "
     "⚠️ Quy tắc 'ưu tiên TC mới nhất' KHÔNG áp dụng được ở đây vì chỉ có 1 nguồn duy nhất (08/2023).",
     "TC-RPL-*『Filter — conversion & QRコード』(TC ĐK1 access một phần, TC ĐK2 access một phần)",
     "",
     "Hỏi dev xác nhận ngữ nghĩa ĐK1/ĐK2 của filter conversion, rồi bổ sung bảng 4 điều kiện con vào "
     "feature-spec.md §SCR-RPL-03 (hiện chỉ có tên loại, không có điều kiện con)."],

    ["MT-08", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Keyword 完全一致 phân biệt HOA/THƯỜNG — không có TC nào kiểm tra",
     "Corpus KHÔNG có TC nào gửi keyword khác hoa/thường so với keyword đã đăng ký "
     "(ma trận Ver1.0 r9-r24 chỉ xoay quanh dấu 【】, không đụng tới hoa/thường)",
     "• `feature-spec.md` §5 BR-18: 'Exact match: `val = keyword COLLATE utf8mb4_bin` (**case-sensitive**)'\n"
     "• §7 Keyword Matching (SQL): `ELSE val = keyword.keyword COLLATE 'utf8mb4_bin'`\n"
     "• `job/job-spec.md:303`: 'exact match (so sánh bằng, **case-sensitive** qua utf8mb4_bin collation)'",
     "Người dùng LINE gõ tự do — 'OK' / 'ok' / 'Ok' là 3 chuỗi khác nhau với utf8mb4_bin. Khách hàng đăng ký "
     "keyword「OK」thì user gõ「ok」sẽ KHÔNG được trả lời. Đây là hành vi người dùng cuối gặp hằng ngày nhưng "
     "chưa từng được test.",
     "TC-RPL-*『Form — 利用設定 キーワード』(TC 完全一致 phân biệt hoa/thường)",
     "",
     "Xác nhận case-sensitive là CỐ Ý hay là thiếu sót. Nếu cố ý: bổ sung cảnh báo trên UI form keyword + "
     "ghi vào tài liệu hướng dẫn khách hàng. Nếu không: raise bug đổi collation."],

    ["MT-09", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Rule 'đổi sang 全てのメッセージ thì XÓA HẾT keyword' chỉ có trong TC, spec bỏ sót",
     "Ver1.0 r29-r42 (Bug KH #32967 [02-12-2025][9119]) — cách fix ghi trong TC: "
     "'Xóa hết keyword của auto_reply khi chọn đối ứng all msg'. Có 6 TC verify: đổi 1 keyword → all, "
     "đổi nhiều keyword → all, và mỗi lần đều kiểm tra tạo lại được keyword cũ",
     "`feature-spec.md` §5 Business Rules: BR-04 chỉ nói 'Xóa auto_reply và folder dùng soft delete; xóa keywords "
     "dùng hard delete'. KHÔNG có rule nào nói về việc ĐỔI LOẠI quy tắc thì keyword bị xóa.\n"
     "§SCR-RPL-02 luồng chỉnh sửa cũng chỉ ghi 'Keywords: update existing / create new / delete removed (whereNotIn)'",
     "Rule 'whereNotIn' trong spec chỉ xóa keyword bị gỡ khỏi danh sách. Nó KHÔNG giải thích được việc chuyển sang "
     "全てのメッセージ (lúc đó list_keyword rỗng) thì toàn bộ keyword bị xóa. Đây chính là bug #32967 mà khách hàng "
     "gặp: keyword rác khiến báo「すでに登録しています」dù không thấy keyword đâu.",
     "TC-RPL-*『Form — 利用設定 キーワード』(6 TC chuyển loại quy tắc)",
     "",
     "Bổ sung BR mới vào feature-spec.md §5: 'Khi keyword_reaction_type chuyển từ 1 → 0, hard delete toàn bộ "
     "keyword của quy tắc' (ReplyController@saveDataDetailAutoReply)."],

    ["MT-10", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Nhập nhiều keyword mà 1 dòng bị trùng: reject cả batch hay chỉ báo dòng đó?",
     "Ver1.0 r38 và r40 chỉ có case n=1: 'check tạo mới với keyword B → báo lỗi keyword đã tồn tại'. "
     "KHÔNG có TC cho trường hợp nhập nhiều keyword mà chỉ 1 dòng trùng.",
     "`feature-spec.md` §SCR-RPL-02 bảng Luồng lỗi: 'Keyword đã tồn tại → {success: false, msg: ..., "
     "**arraySameWord: [0,2]**}' — arraySameWord là MẢNG các index, hàm ý có thể nhiều dòng trùng cùng lúc.\n"
     "BR-01 chỉ nói 'Kiểm tra khi tạo mới và cập nhật', không nói xử lý batch.",
     "arraySameWord là mảng ⇒ backend biết dòng nào trùng. Nhưng response `success: false` ⇒ có vẻ reject cả form. "
     "Vậy 2 keyword không trùng trong cùng form có được lưu không? Không tài liệu nào trả lời. "
     "Đây là tình huống người dùng gặp thường xuyên khi nhập nhiều keyword.",
     "TC-RPL-*『Keyword — trùng & đồng bộ bảng keyword』(TC batch có 1 dòng trùng)",
     "",
     "Chốt hành vi, rồi bổ sung vào feature-spec.md §SCR-RPL-02 bảng Luồng lỗi: reject toàn bộ hay lưu phần hợp lệ. "
     "Lưu ý so sánh với quyết định MT-01 của kho FA-012 Tag (Leader đã chốt SKIP tên trùng cho batch tag) — "
     "nếu 2 tính năng xử lý khác nhau thì cần ghi rõ lý do."],

    ["MT-11", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "2 lệnh recover chỉ có trong TC, spec §7 Background Jobs không có",
     "① Ver1.0 r53-r54: lệnh recover dọn keyword của auto_reply dạng all msg (`keyword_reaction_type=0`) và "
     "auto_reply đã xóa (`is_deleted=1`), kèm câu query kiểm tra cụ thể\n"
     "② TCsLine_Improve chung / tab「recover bảng category」r4: 'kind = 1 ⇒ autoreply / bảng autoreply / "
     "xóa bản ghi map theo category_id' (id 3814)",
     "`feature-spec.md` §7 Background Jobs chỉ mô tả HandlePostbackTask (xử lý webhook runtime). "
     "`job/job-spec.md` cũng chỉ có processing chain của callback_event.\n"
     "→ KHÔNG có mục nào về job/command recover dữ liệu.",
     "2 lệnh recover này CHỈNH SỬA DỮ LIỆU THẬT trên production. Không có trong spec nghĩa là: không ai review "
     "được phạm vi ảnh hưởng, không ai biết khi nào chạy, và nếu chạy sai thì mất keyword của khách hàng.",
     "TC-RPL-*『Keyword — trùng & đồng bộ bảng keyword』(TC job recover keyword) + "
     "TC-RPL-*『Folder — xóa & cascade』(TC recover bảng category)",
     "",
     "Bổ sung mục 'Maintenance commands' vào feature-spec.md §7 và job/job-spec.md: tên lệnh, điều kiện chạy, "
     "phạm vi dữ liệu bị tác động, cách rollback."],

    ["MT-12", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "SPEC TỰ MÂU THUẪN: bắt buộc chọn ≥1 曜日 — có ở flow legacy, KHÔNG có ở flow V2",
     "Corpus KHÔNG có TC nào cho trường hợp chọn 反応する曜日・時間 nhưng không tick ngày nào",
     "MÂU THUẪN NGAY TRONG 1 FILE `web/logic-spec.md`:\n"
     "• Dòng 596 — Validation Flow **Legacy**: `week[]` khi trigger_kind=1 → 'Bắt buộc, tối thiểu 1' → "
     "「曜日は最低1つを選択して下さい。」\n"
     "• Dòng 607-612 — Validation Flow **V2** (`saveDataDetailAutoReply`): chỉ có 4 rule "
     "(list_keyword, start_time/end_time, keyword uniqueness, botIdCurrent) — **KHÔNG có rule 曜日**\n"
     "• `feature-spec.md` §SCR-RPL-02 bảng Luồng lỗi V2 cũng chỉ có 4 message, không có message 曜日",
     "Flow V2 là flow đang dùng (view create_v2). Nếu V2 thật sự không validate 曜日 thì user có thể lưu quy tắc "
     "'có lịch trình nhưng không chọn ngày nào' → quy tắc VĨNH VIỄN không bao giờ chạy mà không có cảnh báo nào.",
     "TC-RPL-*『Form — スケジュール設定』(TC không tick ngày nào)",
     "",
     "Chạy TC để xác định hành vi thật của V2. Nếu V2 không validate: quyết định bổ sung validate hay chấp nhận, "
     "rồi sửa logic-spec.md cho 2 flow khớp nhau."],

    ["MT-13", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "BR-08: sửa quy tắc đang TẮT thì hệ thống TỰ BẬT LẠI — không TC nào biết, không tài liệu nào cảnh báo",
     "Corpus KHÔNG có TC nào cho hành vi này. Ngược lại, khối MỚI NHẤT của tab master (Bug KH #38369, 07/2026, "
     "Ver1.0 r107-r121) cho thấy khách hàng RẤT nhạy cảm với thao tác ON/OFF (bug 'tắt auto reply thì màn tự nhảy "
     "sang folder khác' được raise ngay).",
     "• `feature-spec.md` §5 BR-08 V2 auto-enable: 'Khi lưu qua flow V2, is_stopped luôn reset về 0 (bật)' "
     "(ReplyController.php:1020, 1034 — tin cậy **Cao**)\n"
     "• §Ảnh hưởng ghi rõ: 'Quy tắc tự động được bật lại sau mỗi lần sửa'\n"
     "• §SCR-RPL-02 luồng chỉnh sửa: 'AutoReply::update() (**luôn set is_stopped=0** — tự động bật lại)'",
     "Khách hàng tắt 1 quy tắc để dừng gửi tin, sau đó vào sửa nội dung → quy tắc TỰ BẬT và bắt đầu gửi tin cho "
     "user LINE ngay lập tức. Đây là hành vi gửi tin NGOÀI Ý MUỐN — hậu quả trực tiếp với người dùng cuối và "
     "có thể phát sinh chi phí LINE API.",
     "TC-RPL-*『Form — số lần chạy & lưu quy tắc』(TC BR-08 sửa quy tắc đang OFF)",
     "",
     "Xác định đây là hành vi CỐ Ý hay bug. Nếu cố ý: bổ sung cảnh báo trên UI khi lưu quy tắc đang OFF, và ghi "
     "vào tài liệu khách hàng. Nếu là bug: raise ticket sửa `saveDataDetailAutoReply` giữ nguyên is_stopped."],

    ["MT-14", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "BR-02 backup lock: không có TC nào kiểm tra việc CHẶN thao tác trong lúc bot đang backup",
     "TCsLine_BackUp (Backup (job) + Backup 1.0) chỉ test DỮ LIỆU auto reply SAU khi backup xong "
     "(21 dòng, r2-r22). KHÔNG có TC nào thử tạo/sửa/xóa quy tắc TRONG LÚC bot đang backup.",
     "• `feature-spec.md` §5 BR-02 Backup lock: 'Không cho phép tạo/sửa/xóa khi bot đang trong quá trình backup "
     "(BackupHistory status 0/1)' — enforce ở **8 vị trí** trong ReplyController "
     "(dòng 143-149, 456-463, 491-498, 515-522, 569-576, 587-594, 621-629, 940-946), tin cậy **Cao**\n"
     "• Ảnh hưởng: 'Lỗi HTTP 500 + MESSAGE_NOTIFY_BACKUP'",
     "Rule được enforce ở 8 chỗ trong code nghĩa là dev coi nó quan trọng. Nhưng 8 chỗ đó chưa từng được test. "
     "Nếu 1 trong 8 chỗ sót (VD action moveItem hoặc sortFolder), user có thể sửa dữ liệu giữa lúc backup → "
     "backup ra dữ liệu không nhất quán.",
     "TC-RPL-*『Form — số lần chạy & lưu quy tắc』(TC backup lock 4 thao tác)",
     "",
     "Chốt phạm vi: test đủ 8 điểm enforce hay chỉ test 4 thao tác chính. Nếu test đủ 8, cần liệt kê rõ 8 action "
     "tương ứng của EP-06 vào spec."],

    ["MT-15", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Phân trang màn danh sách: spec ghi 'chưa quan sát được', TC không có",
     "Corpus KHÔNG có TC nào cho phân trang / danh sách nhiều quy tắc ở màn /basic/reply",
     "• `ui/ui-spec.md` §SCR-RPL-01 mục Pagination: 'Chưa quan sát được (danh sách trống với 0 records) — "
     "cần kiểm tra khi có dữ liệu'\n"
     "• `feature-spec.md` §9 Gaps #16: 'Pagination khi danh sách có nhiều quy tắc — Mức Thấp'",
     "Spec được reverse-engineer trên màn 0 record nên toàn bộ phần hiển thị bảng đều là suy luận. "
     "Không biết có phân trang hay không, giới hạn bao nhiêu dòng.",
     "TC-RPL-*『Màn list — hiển thị & cột』(TC ≥100 quy tắc)",
     "",
     "Mở màn có ≥100 quy tắc, ghi nhận có phân trang hay không và số dòng/trang, rồi cập nhật ui-spec.md "
     "(đóng Gap #16)."],

    ["MT-16", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Xóa folder: quy tắc bên trong có rơi về 未分類 không?",
     "Ver1.0 r47-r48 chỉ verify: xóa folder ⇒ keyword bị hard delete và tạo lại được keyword đó. "
     "KHÔNG kiểm tra các quy tắc bên trong folder đi đâu.",
     "• `feature-spec.md` §5 BR-07 Cascade delete folder: 'Xóa folder → soft delete tất cả auto_reply bên trong "
     "+ hard delete keywords'\n"
     "• §SCR-RPL-01 luồng xóa folder: `UPDATE auto_reply SET is_deleted=1 WHERE category_id = group_id`\n"
     "→ Spec nói quy tắc bị XÓA MỀM, không nói chuyển về 未分類",
     "Theo spec thì quy tắc bị xóa luôn — nhưng nhiều màn khác của LME lại chuyển item về folder mặc định khi "
     "xóa folder. Khách hàng có thể tưởng chỉ xóa folder mà mất luôn toàn bộ quy tắc bên trong.",
     "TC-RPL-*『Folder — xóa & cascade』(TC quy tắc không rơi về 未分類)",
     "",
     "Xác nhận hành vi mong đợi. Nếu là xóa luôn: bổ sung cảnh báo rõ ràng trên dialog xác nhận xóa folder "
     "('N quy tắc bên trong cũng sẽ bị xóa')."],

    ["MT-17", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Điều hướng sau khi thêm folder mới: về folder đang mở hay folder vừa tạo?",
     "Ver1.0 r119 (Bug KH #38369, 07/2026): 'Đang ở folder A → Thêm folder mới' → "
     "Expect ghi mơ hồ: 'Sau khi thêm, folder đang mở xử lý đúng theo spec (không tự nhảy về 未分類)' — "
     "chính TC cũng đẩy trách nhiệm sang spec.\n"
     "Trong khi Test bug folder all màn r5 lại nói: sau khi tạo folder mới → vào tạo item thì màn tạo mới hiện "
     "chọn sẵn folder MỚI.",
     "`feature-spec.md` §SCR-RPL-01 chỉ mô tả cookie `folder_reply` xác định folder đang chọn, EP-12 "
     "/basic/reply/set-cookie lưu folder. KHÔNG nói sau khi TẠO folder mới thì cookie trỏ vào đâu.",
     "TC nói 'đúng theo spec' nhưng spec không quy định. Hai nguồn corpus gợi ý 2 hành vi khác nhau "
     "(giữ folder A vs chuyển sang folder mới).",
     "TC-RPL-*『Folder — điều hướng & sắp xếp』(TC thêm folder mới)",
     "",
     "Chốt hành vi rồi bổ sung vào feature-spec.md §SCR-RPL-01 (luồng tạo folder + cập nhật cookie folder_reply)."],

    ["MT-18", "THẤP", "⏳ CHỜ QUYẾT ĐỊNH",
     "Sắp xếp folder / sắp xếp quy tắc / chuyển folder hàng loạt — 3 chức năng có endpoint nhưng 0 TC",
     "Corpus KHÔNG có TC nào cho: sortFolder, sortItem, moveItem của màn auto reply",
     "• `feature-spec.md` §6 bảng 'EP-06: Chi tiết các actions' có đủ 3 action: `sortItem`, `moveItem`, `sortFolder`\n"
     "• `ui/ui-spec.md` toolbar có nút「並べ替え」và「一括フォルダ変更」\n"
     "• BR-05 Position ordering có mô tả cơ chế position",
     "3 chức năng hiển thị rõ trên toolbar và có endpoint, nhưng chưa từng có TC. "
     "Riêng 一括フォルダ変更 là thao tác hàng loạt — sai là ảnh hưởng nhiều bản ghi cùng lúc.",
     "TC-RPL-*『Folder — điều hướng & sắp xếp』(TC sortFolder) + "
     "TC-RPL-*『Sắp xếp & chuyển folder quy tắc』(3 TC)",
     "",
     "Xác nhận 4 TC mới do AI viết có đúng hành vi mong đợi không, đặc biệt hành vi khi không chọn bản ghi nào."],

    ["MT-19", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Bot A truy cập URL của bot B: TC chỉ liệt kê URL, không ghi kết quả mong đợi",
     "TCsLine_Improve chung / Improve nhỏ r335-r337 (Bug Tester #33107 — 'Bot A đang access được link của bot B "
     "⇒ Check lại cho all màn'). Khối auto reply liệt kê đúng 3 URL:\n"
     "• /basic/reply/new?group_id=6754 (màn tạo mới)\n• /basic/reply/new?group_id=0&reply_id=18888 (màn edit)\n"
     "• /basic/reply/new?group_id=0&copy_id=18888 (màn copy)\n"
     "→ Cột Expect Result **TRỐNG** cho cả 3 dòng",
     "`web/logic-spec.md` §Authorization chỉ ghi: 'Bot ownership — getBotId() từ session, mọi query đều filter "
     "theo bot_id'. KHÔNG mô tả hành vi khi truy cập URL chứa id của bot khác (redirect / 403 / form trống).",
     "Đây là lỗ hổng truy cập dữ liệu chéo bot — mức nghiêm trọng. Nhưng cả TC lẫn spec đều không nói kết quả "
     "mong đợi là gì, nên tester không biết thế nào là PASS.",
     "TC-RPL-*『Form — số lần chạy & lưu quy tắc』(TC Bug #33107 cross-bot)",
     "",
     "Chốt hành vi mong đợi thống nhất cho toàn hệ thống (redirect về /basic/reply của bot hiện tại, hay báo lỗi "
     "quyền), rồi bổ sung vào logic-spec.md §Authorization."],

    ["MT-20", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Nút COPY quy tắc: spec nói 'chưa quan sát được trên UI', nhưng corpus có 8 TC đã chạy OK",
     "Ver1.0 có **8 dòng『Check copy』đã chạy PASS trên staging** (r59, r63, r66, r69, r75, r81, r87, r93 — "
     "khối Bug KH #35729, 04/2026), nội dung: 'Copy auto reply thành công ⇒ không edit action đã copy' và "
     "'Copy auto reply thành công ⇒ có edit action đã copy'\n"
     "→ Đây là bằng chứng chức năng copy TỒN TẠI VÀ HOẠT ĐỘNG trên UI",
     "• `feature-spec.md` §9 Gap TB-02: 'Chức năng sao chép (copy) quy tắc tồn tại trong code (EP-02 copy_id, "
     "EP-07 copyId) nhưng **chưa quan sát được nút bấm trên giao diện**' — mức Trung bình, trạng thái MỞ\n"
     "• §SCR-RPL-02 luồng sao chép cũng ghi 'vị trí nút trên UI chưa xác nhận — xem TB-02'",
     "Không phải mâu thuẫn về hành vi, mà là spec bị THIẾU thông tin mà TC đã có. Đề xuất dùng TC để ĐÓNG Gap TB-02.\n"
     "Điểm cần chốt thêm: BR-11 nói 'Keywords KHÔNG được clone' — corpus KHÔNG có TC nào verify điều này.",
     "TC-RPL-*『Copy quy tắc』(4 TC)",
     "",
     "① Đóng Gap TB-02 trong feature-spec.md §9, ghi rõ vị trí nút copy trên UI.\n"
     "② Xác nhận hành vi 'copy không clone keyword' — vì nghĩa là mọi bản copy đều PHẢI nhập lại keyword thủ công, "
     "cần cân nhắc có phải trải nghiệm mong muốn không."],

    ["MT-21", "CAO", "⏳ CHỜ QUYẾT ĐỊNH",
     "Giá trị `group_open` / `selected_group_id` trong t_actions_detail: 2 khối TC CÙNG THÁNG nói khác nhau",
     "⚠️ HAI KHỐI TC CÙNG NIÊN ĐẠI 04/2026, NẰM TRONG CÙNG TAB MASTER:\n"
     "**Khối A — Bug KH #35729 (Ver1.0 r55-r96):**\n"
     "• Tạo mới action friend info → 'check db: t_actions_detail có lưu \"group_open\": id'\n"
     "• Edit action friend info → 'check db: t_actions_detail có lưu \"group_open\": **0**'\n"
     "**Khối B — Task #35989 recover (Ver1.0 r97-r106):**\n"
     "• folder default → group_open = **0**\n• folder mặc định hệ thống (tên/SDT/email/ngày sinh) → **-1**\n"
     "• folder địa chỉ (info_id -6→-10) → **-2**\n• folder tự tạo → **group_id**\n"
     "• action scenario → selected_group_id = **0** (khác template = category_id)",
     "`db/db-mapping.md` §t_actions_detail chỉ khai báo cột `data` là JSON. "
     "**KHÔNG liệt kê key `group_open` hay `selected_group_id`**, không có bảng giá trị quy ước, "
     "không giải thích ý nghĩa các giá trị âm -1 / -2.\n"
     "`feature-spec.md` §SCR-RPL-04 ghi tin cậy **Trung bình** cho data structure của action.",
     "Khối A nói EDIT luôn lưu group_open = 0; khối B nói giá trị phụ thuộc LOẠI FOLDER (0 / -1 / -2 / group_id). "
     "Hai khối cách nhau vài dòng trong cùng tab, cùng tháng 04/2026 ⇒ **quy tắc 'ưu tiên TC mới nhất' là căn cứ "
     "YẾU ở đây**. Lý do nghiêng về khối B: chi tiết hơn, phân biệt được 4 loại folder, và chính là nội dung của "
     "task recover dữ liệu (Task #35989) — tức là chuẩn hoá lại giá trị đúng.",
     "TC-RPL-* toàn bộ nhóm『Action — 友だち情報』(7 TC) +『Action — テンプレート & ステップ』(TC selected_group_id)",
     "",
     "① Chốt bảng giá trị chuẩn của `group_open` và `selected_group_id` theo từng loại folder × từng loại action.\n"
     "② Bổ sung bảng đó vào db-mapping.md §t_actions_detail và feature-spec.md §SCR-RPL-04 "
     "(nâng tin cậy từ Trung bình lên Cao).\n"
     "③ Nếu chốt theo khối B: TC edit action friend info (dựa khối A, group_open=0) sẽ **dự kiến FAIL** khi info "
     "thuộc folder tự tạo → cần raise bug."],

    ["MT-22", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Backup có bao gồm FILTER của quy tắc auto reply không? — corpus ghi 'Chưa support' suốt 10 đợt",
     "• TCsLine_BackUp / Backup (job) r20: dòng 'Filter' — cột Test Result = OK nhưng cột staging = "
     "**'Chưa support'**\n"
     "• Backup 1.0 r21: dòng 'Filter' ghi **'Chưa support' ở TOÀN BỘ 10 cột kết quả** của 10 đợt backup",
     "`feature-spec.md` §3 Data Model liệt kê `filters_v2` là bảng chính (17.8MB) của FA-003. "
     "§SCR-RPL-02 mô tả filter được lưu với parent_type='auto_reply'.\n"
     "→ Spec KHÔNG nói gì về phạm vi backup: filter có được backup hay không.",
     "Nếu filter KHÔNG được backup: quy tắc auto reply ở bot mới sẽ chạy cho TOÀN BỘ friend thay vì chỉ nhóm đã lọc "
     "→ gửi tin cho người không nên nhận. Đây là hậu quả trực tiếp với người dùng cuối, không phải chỉ thiếu dữ liệu.",
     "TC-RPL-*『Backup & đổi bot』(TC filter backup)",
     "",
     "Xác định 'Chưa support' là (a) chưa test được hay (b) tính năng chưa hỗ trợ. "
     "Nếu (b): bổ sung cảnh báo cho khách hàng khi backup + ghi vào spec phạm vi backup của FA-003."],

    ["MT-23", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Phân quyền Staff cho màn 自動応答: corpus có 4 dòng 'Check account staff' nhưng ĐỀU BỎ TRỐNG kết quả mong đợi",
     "Ver1.0 có 4 dòng『check acc staff』/『Check account staff』(r52, r96, r121, r199) — nằm ở cuối mỗi khối "
     "ticket. **Cả 4 dòng đều KHÔNG có Expect Result.**\n"
     "Nguồn phân quyền duy nhất là TCsLine_Improve chung / tab「Phân quyền」(11/2023, ~2.8 năm tuổi) — và tab đó "
     "test message quyền DÙNG CHUNG cho mọi màn, chỉ ở tầng ẨN MENU.",
     "• `web/logic-spec.md` §Authorization: '**Không phát hiện kiểm tra quyền Staff (Role/Permission)**. "
     "Tính năng auto-reply có thể bị giới hạn cho Staff qua cơ chế khác — Tin cậy: **Trung bình**'\n"
     "• `feature-spec.md` §6: 'Không phát hiện middleware kiểm tra quyền Staff riêng cho tính năng này'\n"
     "• §9 Gaps #18: 'Cơ chế kiểm tra quyền Staff (Role/Permission) — Trung bình'",
     "Cả spec lẫn TC đều không xác định được quyền Staff cho màn này. Nếu chỉ ẩn menu mà API không chặn thì "
     "staff không có quyền vẫn gọi được EP-06 để xóa quy tắc auto reply của bot.",
     "TC-RPL-*『Phân quyền & môi trường』(4 TC, đặc biệt TC gọi API trực tiếp)",
     "",
     "① Kiểm tra ở TẦNG API (không chỉ UI): staff không quyền gọi trực tiếp /ajax/get-list-group có bị chặn không.\n"
     "② Kết quả cập nhật vào logic-spec.md §Authorization, đóng Gap #18.\n"
     "③ Nếu API không chặn → đây là lỗ hổng phân quyền, raise bug ngay."],

    ["MT-24", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Flow LEGACY (form POST + bảng `filters`) — còn sống hay đã chết? Không TC nào chạm tới",
     "Toàn bộ 13 nguồn corpus KHÔNG có TC nào cho: /basic/reply/edit/{id}, /basic/reply/store, /basic/reply/save, "
     "hay dữ liệu cũ có reply_content base64",
     "• `feature-spec.md` §1 Ghi chú kiến trúc Dual Flow: 'Flow V2 là flow đang được sử dụng (view create_v2). "
     "**Flow Legacy vẫn tồn tại trong code nhưng có thể không còn được dùng trên giao diện mới.** "
     "Tin cậy: **Trung bình**'\n"
     "• §5 BR-13 Filter dual system: 2 hệ thống filter song song (`filters` legacy vs `filters_v2`)\n"
     "• §5 BR-03: reply_content base64_encode/decode (chỉ flow legacy)\n"
     "• §6 vẫn khai báo EP-03/EP-04/EP-05 là endpoint hoạt động",
     "Spec vừa mô tả legacy đầy đủ (3 endpoint + 3 business rule + 1 bảng DB riêng) vừa nói 'có thể không còn "
     "được dùng'. Nếu legacy còn sống mà không ai test: dữ liệu cũ base64 hiển thị sai, hoặc lưu qua legacy làm "
     "MẤT filter_v2 (vì 2 hệ thống filter không đồng bộ).",
     "TC-RPL-*『Phân quyền & môi trường』(2 TC COMPAT-LEGACY)",
     "",
     "Chốt: legacy có nằm trong phạm vi test không.\n"
     "• Nếu KHÔNG: đề nghị dev xác nhận có thể gỡ EP-03/04/05 và bảng `filters`, rồi đánh dấu DEPRECATED trong spec.\n"
     "• Nếu CÓ: cần bổ sung cả bộ TC cho flow legacy (hiện tại chỉ có 2 TC thăm dò)."],

    ["MT-25", "TRUNG BÌNH", "⏳ CHỜ QUYẾT ĐỊNH",
     "Thứ tự XỬ LÝ rule ở runtime KHÁC thứ tự HIỂN THỊ ở màn list",
     "Corpus KHÔNG có TC nào kiểm tra thứ tự nhận được các action khi nhiều quy tắc cùng khớp "
     "(liên quan MT-03 — case multi-rule bị đánh dấu 'Not test')",
     "MÂU THUẪN GIỮA 2 FILE SPEC:\n"
     "• `job/job-spec.md:394`: 'Các rules được load từ DB theo **thứ tự mặc định (không ORDER BY position)**'\n"
     "• `feature-spec.md` §5 BR-05 Position ordering + §SCR-RPL-01: CRUD sắp xếp theo **position DESC**\n"
     "• §9 Gaps NHE-06 đã ghi nhận: 'Thứ tự hiển thị UI có thể khác thứ tự xử lý runtime — "
     "cần kiểm tra AutoReplyRepository.java'",
     "Khách hàng kéo-thả sắp xếp quy tắc trên màn list với kỳ vọng quy tắc trên chạy trước. "
     "Nếu runtime không ORDER BY position thì thứ tự tin nhắn user LINE nhận được là NGẪU NHIÊN theo id — "
     "chức năng「並べ替え」trở nên vô nghĩa ở tầng hành vi.",
     "TC-RPL-*『Phân quyền & môi trường』(TC NHE-06 thứ tự runtime) + "
     "TC-RPL-*『Sắp xếp & chuyển folder quy tắc』(TC sortItem)",
     "",
     "① Kiểm tra `AutoReplyRepository.java` xác nhận có ORDER BY không (spec đã đề xuất việc này ở NHE-06).\n"
     "② Chốt: thứ tự sắp xếp trên UI có PHẢI quyết định thứ tự runtime không.\n"
     "③ Nếu phải mà code chưa có → raise bug; nếu không phải → ghi rõ vào UI rằng 並べ替え chỉ đổi thứ tự hiển thị."],
]
