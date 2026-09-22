# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 3-5.

S3 Thêm & sửa trạng thái · S4 Sắp xếp trạng thái · S5 Xóa trạng thái.

✅ MT-02 đã được Leader chốt 2026-09-21: CRUD và sắp xếp trạng thái đối ứng là thao
tác INLINE — nút「＋ 新規追加」sinh 1 dòng nhập → gõ tên → Enter để lưu; đổi màu và
kéo thả tự lưu ngay, KHÔNG có nút「保存」riêng cho Tab 1.
Toàn bộ nhóm 3-5 đã viết đúng theo quyết định này. Bản MODAL của spec + tab
「Setting Chat」07/2025 nay là bản LẠC HẬU, chỉ giữ làm nguồn đối chiếu.
"""
from _common import tc

TAB1 = ("- Đăng nhập Admin của LOA, đã chọn 1 bot\n"
        "- Đang ở `/basic/chat-setting`, Tab 1「対応ステータス編集」")
HAS1 = TAB1 + "\n- Danh sách có ít nhất 1 trạng thái"
MT02 = "✅ MT-02 đã chốt 2026-09-21: thao tác inline. "

S3 = [
    tc("Thêm & sửa trạng thái", "FUNC-001", "Normal",
       "Bấm「＋ 新規追加」— xuất hiện đúng 1 dòng nhập trống, chưa gọi API",
       TAB1,
       "1. Quan sát cuối danh sách TRƯỚC khi bấm\n"
       "2. Bấm nút「＋ 新規追加」\n"
       "3. Quan sát dòng vừa xuất hiện\n"
       "4. Nhấn F5 ngay (chưa nhập gì)",
       "—",
       "- Trước bấm: cuối danh sách KHÔNG có dòng nhập trống, chỉ có nút「＋ 新規追加」\n"
       "- Sau bấm: xuất hiện đúng 1 dòng nhập trống ở cuối danh sách\n"
       "- Dòng mới có placeholder「対応ステータス（Enterで保存）」và bộ đếm「0/20」\n"
       "- Chưa có toast「保存しました」, chưa tạo bản ghi nào\n"
       "- Sau F5: dòng nhập biến mất, không sinh trạng thái rỗng",
       note=MT02 + "Nguồn: v2 r6 (TC-SC-004b, Pass staging + production) — BR-15"),

    tc("Thêm & sửa trạng thái", "FUNC-001", "Normal",
       "Thêm trạng thái mới — nhập tên rồi Enter, lưu thành công và còn sau F5",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập tên「テスト」vào dòng vừa xuất hiện\n"
       "3. Nhấn Enter\n"
       "4. Nhấn F5 reload trang",
       "テスト",
       "- Toast「保存しました」xuất hiện\n"
       "- Trạng thái「テスト」hiển thị trong danh sách\n"
       "- Sau F5 trạng thái vẫn còn (đã ghi bảng `status_chat`, cột `name_status`)",
       note=MT02 + "Nguồn: v2 r5 (TC-SC-004, Pass staging + production) · SC r113 · SC r125"),

    tc("Thêm & sửa trạng thái", "FUNC-001", "Normal",
       "Sửa tên trạng thái đang có — Enter là lưu, tên đổi ngay",
       HAS1,
       "1. Bấm vào ô nhập tên của 1 trạng thái bất kỳ\n"
       "2. Xóa tên cũ, nhập「更新テスト」\n"
       "3. Nhấn Enter",
       "更新テスト",
       "- Toast「保存しました」xuất hiện\n"
       "- Tên trạng thái hiển thị thành「更新テスト」",
       note=MT02 + "Nguồn: v2 r8 (TC-SC-005, Pass staging + production). ⚠️ Từ BUG-017 (Closed "
            "2026-06-18) blur KHÔNG còn trigger lưu — chỉ Enter mới lưu"),

    tc("Thêm & sửa trạng thái", "FUNC-001", "Normal",
       "Đổi màu trạng thái — tự lưu ngay, không cần bấm nút nào khác",
       HAS1,
       "1. Bấm bộ chọn màu của 1 trạng thái bất kỳ\n"
       "2. Chọn 1 màu khác màu hiện tại",
       "—",
       "- Toast「保存しました」xuất hiện ngay sau khi chọn màu\n"
       "- Màu của trạng thái đổi theo màu vừa chọn\n"
       "- Giá trị lưu vào cột `color` bảng `status_chat`",
       note=MT02 + "Nguồn: v2 r9 (TC-SC-006, Pass staging + production) · SC r121"),

    tc("Thêm & sửa trạng thái", "UI-003", "Normal",
       "Bảng màu — số lượng màu chọn được và màu mặc định",
       HAS1,
       "1. Bấm bộ chọn màu của 1 trạng thái\n"
       "2. Đếm số ô màu trong bảng\n"
       "3. Quan sát màu đang được tích",
       "—",
       "- Bảng màu hiển thị đủ 7 màu chọn được\n"
       "- Màu mặc định của trạng thái mới là đỏ `#F44336`\n"
       "- Ô màu đang dùng được đánh dấu tích",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-10 (số màu + màu default chưa verify với Figma 2026). "
            "Nguồn: SC r119-r120 (7 màu, default đỏ #F44336 — 2025) · v2 r35 (TC-SC-130, Not Tested, "
            "ghi rõ『⚠ Verify số lượng/màu default với Figma』)"),

    tc("Thêm & sửa trạng thái", "FUNC-001", "Normal",
       "Cho phép 2 trạng thái trùng màu",
       HAS1 + "\n- Có ít nhất 2 trạng thái",
       "1. Bấm bộ chọn màu của trạng thái A\n"
       "2. Chọn đúng màu mà trạng thái B đang dùng\n"
       "3. Quan sát danh sách",
       "—",
       "- Hệ thống KHÔNG chặn, cho phép trùng màu\n"
       "- Toast「保存しました」xuất hiện, cả 2 trạng thái cùng màu",
       note="Nguồn: SC r123 (『Cho phép trùng』, OK + staging OK) · v2 r35 (TC-SC-130)"),

    tc("Thêm & sửa trạng thái", "UI-003", "Normal",
       "Đóng bảng màu bằng cách bấm ra ngoài",
       HAS1,
       "1. Bấm bộ chọn màu để mở bảng màu\n"
       "2. Bấm ra vùng trống bên ngoài bảng màu",
       "—",
       "- Bảng màu đóng lại\n"
       "- Màu của trạng thái giữ nguyên như trước khi mở (không lưu màu nào)",
       note="Nguồn: v1 r15 (BS_005, Pass) — TC gốc chỉ ghi『Tắt picker』, phần『màu giữ nguyên』"
            " là SUY LUẬN của AI, cần Leader xác nhận",
       spec="Đã hỏi leader"),

    tc("Thêm & sửa trạng thái", "FUNC-004", "Boundary",
       "Nhập đúng 20 ký tự — bộ đếm 20/20 và lưu được",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập đúng 20 ký tự「あ」\n"
       "3. Nhấn Enter",
       "あ × 20",
       "- Bộ đếm hiển thị「20/20」\n"
       "- Lưu thành công, toast「保存しました」\n"
       "- Tên trạng thái hiển thị đủ 20 ký tự",
       note="Nguồn: v2 r15 (TC-SC-011, Pass staging + production) · SC r117"),

    tc("Thêm & sửa trạng thái", "FUNC-004", "Abnormal",
       "Gõ ký tự thứ 21 khi tạo mới — bị chặn hoàn toàn",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Cố gõ chuỗi 21 ký tự「あ」liên tiếp\n"
       "3. Quan sát ô nhập và bộ đếm",
       "あ × 21",
       "- Chỉ nhập được tối đa 20 ký tự\n"
       "- Ký tự thứ 21 không hiện trong ô nhập\n"
       "- Bộ đếm dừng ở「20/20」",
       note="Nguồn: v2 r14 (TC-SC-010, Pass staging + production) · SC r118"),

    tc("Thêm & sửa trạng thái", "FUNC-004", "Abnormal",
       "Gõ ký tự thứ 21 khi SỬA trạng thái đang có — bị chặn hoàn toàn",
       HAS1,
       "1. Bấm vào ô nhập tên của 1 trạng thái đang có\n"
       "2. Xóa tên cũ, cố gõ chuỗi 21 ký tự「あ」",
       "あ × 21",
       "- Chỉ nhập được tối đa 20 ký tự\n"
       "- Ký tự thứ 21 bị chặn, không hiện trong ô nhập\n"
       "- Bộ đếm hiển thị「20/20」",
       note="Nguồn: v2 r40 (TC-SC-142, Pass staging + production; BUG-007 counter fix đã Closed). "
            "Đối xứng với TC tạo mới — giữ riêng vì luồng sửa từng lọt lỗi bộ đếm"),

    tc("Thêm & sửa trạng thái", "FUNC-004", "Boundary",
       "Sửa tên trạng thái đang có thành đúng 20 ký tự — lưu được",
       HAS1,
       "1. Bấm vào ô nhập tên của 1 trạng thái đang có\n"
       "2. Xóa tên cũ, nhập đúng 20 ký tự「あ」\n"
       "3. Nhấn Enter",
       "あ × 20",
       "- Bộ đếm hiển thị「20/20」\n"
       "- Lưu thành công, toast「保存しました」\n"
       "- Tên trạng thái cập nhật đủ 20 ký tự",
       note="Nguồn: v2 r41 (TC-SC-143, Pass staging + production)"),

    tc("Thêm & sửa trạng thái", "UI-003", "Normal",
       "Bộ đếm ký tự chạy đúng theo số ký tự đang gõ",
       TAB1,
       "1. Bấm「＋ 新規追加」, quan sát bộ đếm khi chưa gõ gì\n"
       "2. Gõ 1 ký tự, quan sát bộ đếm\n"
       "3. Gõ tiếp đến 10 ký tự, quan sát bộ đếm",
       "1 ký tự → 10 ký tự",
       "- Chưa gõ: hiển thị「0/20」\n"
       "- Gõ 1 ký tự: hiển thị「1/20」\n"
       "- Gõ 10 ký tự: hiển thị「10/20」",
       note="Nguồn: SC r114-r116 (OK + staging OK). Gộp 3 mốc vì cùng 1 quy tắc hiển thị N/20"),

    tc("Thêm & sửa trạng thái", "UI-INPUT-001", "Abnormal",
       "Dán 25 ký tự bằng chuột phải — kiểm tra có lọt qua giới hạn 20 không",
       TAB1 + "\n- Clipboard đang chứa chuỗi 25 ký tự「あ」",
       "1. Bấm「＋ 新規追加」\n"
       "2. Chuột phải > Paste chuỗi 25 ký tự vào ô nhập\n"
       "3. Quan sát ô nhập ngay sau khi dán\n"
       "4. Nếu ô nhập nhận > 20 ký tự thì nhấn Enter, F5 và xem lại tên đã lưu",
       "あ × 25",
       "- Ô nhập chỉ còn 20 ký tự, hành vi giống khi gõ tay\n"
       "- KHÔNG lưu được tên dài quá 20 ký tự xuống DB\n"
       "- Nếu quan sát thấy lưu được > 20 ký tự → báo bug (server EP-06 không validate)",
       note="⚠️ Phụ thuộc MT-08 (UI 20 / EP-06 không validate / EP-08 legacy validate 10). "
            "Nguồn: v2 r25 (TC-SC-080, Pass staging + production) — grounded từ Backend Context SCR-01"),

    tc("Thêm & sửa trạng thái", "UI-INPUT-001", "Normal",
       "Dán tên bằng chuột phải — vẫn lưu được như khi gõ tay (Windows + Mac)",
       TAB1 + "\n- Clipboard đang chứa chuỗi「ペーストテスト」",
       "1. Bấm「＋ 新規追加」\n"
       "2. Chuột phải > Paste (KHÔNG dùng Ctrl+V / Cmd+V)\n"
       "3. Nhấn Enter\n"
       "4. Lặp lại toàn bộ trên trình duyệt ở máy Mac",
       "ペーストテスト",
       "- Nội dung được dán vào ô nhập đúng như clipboard\n"
       "- Sau Enter lưu thành công, toast「保存しました」— giống hệt khi dán bằng phím tắt hoặc gõ tay\n"
       "- Không gặp trường hợp thao tác lưu \"im lặng\" không chạy do JS chỉ nghe sự kiện bàn phím\n"
       "- Kết quả giống nhau trên cả Windows và Mac",
       note="Nguồn: v2 r23 (TC-SC-078, Pass staging + production) — UI-INPUT-001"),

    tc("Thêm & sửa trạng thái", "UI-INPUT-001", "Boundary",
       "Tên có khoảng trắng đầu/cuối — được cắt bỏ trước khi lưu",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập「　テスト　」(có khoảng trắng full-width ở đầu và cuối)\n"
       "3. Nhấn Enter\n"
       "4. Nhấn F5, quan sát lại tên đã lưu",
       "　テスト　 (space đầu/cuối)",
       "- Lưu thành công\n"
       "- Sau F5 tên hiển thị là「テスト」— khoảng trắng đầu/cuối đã bị cắt",
       note="⚠️ Phụ thuộc MT-07 — v1 r12 (BS_002, Pass) khẳng định AUTO TRIM; v2 r24 (TC-SC-079, "
            "Pass) lại ghi『spec chưa ghi rõ có trim hay không』. TC viết theo bản khẳng định có trim"),

    tc("Thêm & sửa trạng thái", "DATA-TEXT-001", "Boundary",
       "Tên chứa emoji và ký tự đặc biệt — lưu và hiển thị nguyên vẹn",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập「①②③㈱😀」\n"
       "3. Nhấn Enter\n"
       "4. Nhấn F5, quan sát lại tên trạng thái",
       "①②③㈱😀",
       "- Lưu thành công, tên hiển thị nguyên vẹn「①②③㈱😀」\n"
       "- Không mất ký tự nào, không lỗi font\n"
       "- Sau F5 vẫn nguyên vẹn, không bị mojibake (〓 hoặc ?)",
       note="Nguồn: v2 r26 (TC-SC-081, Pass staging + production) · v1 r13 (BS_003, Pass — 「😁😁😁#^$%」)"),

    tc("Thêm & sửa trạng thái", "FUNC-002", "Abnormal",
       "Enter khi ô nhập tên đang trống — không tạo trạng thái nào",
       TAB1,
       "1. Bấm「＋ 新規追加」, KHÔNG nhập gì\n"
       "2. Nhấn Enter",
       "(để trống)",
       "- Không có trạng thái mới nào được tạo\n"
       "- Không có toast「保存しました」\n"
       "- Hiển thị thông báo yêu cầu nhập tên「ステータス名を入力してください」\n"
       "- Không có lỗi JS trên console",
       note="Nguồn: v2 r27 (TC-SC-082) + v2 r33 (TC-SC-128, Pass staging + production, BUG-006 Closed "
            "2026-06-09) · SC r110-r112. ⚠️ v2 r33 ghi『cần verify nguyên văn message với Figma — chuỗi "
            "này chỉ thấy trong TC/bug report, không có trong spec chính thức』"),

    tc("Thêm & sửa trạng thái", "FUNC-002", "Abnormal",
       "Nhập toàn khoảng trắng rồi Enter — xử lý như bỏ trống",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập 3 khoảng trắng「　　　」\n"
       "3. Nhấn Enter",
       "(chỉ space)",
       "- Sau khi cắt khoảng trắng còn chuỗi rỗng → xử lý như trường bắt buộc bỏ trống\n"
       "- Không tạo trạng thái mới, không có toast thành công\n"
       "- Không sinh trạng thái có tên trống / không nhìn thấy trong danh sách",
       note="Nguồn: v2 r28 (TC-SC-083, Pass staging + production) · SC r111"),

    tc("Thêm & sửa trạng thái", "FUNC-002", "Abnormal",
       "Xóa hết tên của trạng thái đang có rồi Enter — không ghi đè tên cũ thành rỗng",
       HAS1,
       "1. Bấm vào ô nhập tên của 1 trạng thái đang có\n"
       "2. Xóa hết tên (hoặc chỉ để lại khoảng trắng)\n"
       "3. Nhấn Enter\n"
       "4. Nhấn F5, quan sát lại tên trạng thái đó",
       "(để trống hoặc chỉ space)",
       "- Không lưu được tên rỗng\n"
       "- Hiển thị lỗi「ステータス名を入力してください」\n"
       "- Tên trạng thái KHÔNG bị ghi đè thành rỗng\n"
       "- Sau F5 hiển thị lại đúng tên cũ trước khi xóa",
       note="Nguồn: v2 r39 (TC-SC-141, Pass staging + production) · v1 r11 (BS_001, Pass — "
            "『reload → hiển thị lại tên status cũ』)"),

    tc("Thêm & sửa trạng thái", "CONC-001", "Boundary",
       "Nhấn Enter 2 lần thật nhanh khi thêm mới — chỉ tạo 1 trạng thái",
       TAB1,
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập「重複防止」\n"
       "3. Nhấn Enter 2 lần liên tiếp thật nhanh\n"
       "4. Nhấn F5 và đếm lại số dòng tên「重複防止」",
       "重複防止",
       "- Chỉ có đúng 1 trạng thái「重複防止」trong danh sách\n"
       "- Sau F5 vẫn đúng 1 bản ghi, không có bản trùng\n"
       "- Toast「保存しました」chỉ hiện 1 lần",
       note="Nguồn: v2 r22 (TC-SC-077, Pass staging + production) · v1 r14 (BS_004, Pass — "
            "『Chỉ toast 1 noti save duy nhất』)"),

    tc("Thêm & sửa trạng thái", "FUNC-UNIQ-001", "Abnormal",
       "Tạo trạng thái trùng tên với trạng thái đã có — phải bị chặn",
       TAB1 + "\n- Bot đang chọn đã có 1 trạng thái tên「ST_DUP_{RUN}」({RUN} = 4 ký tự ngẫu nhiên của lần chạy)",
       "1. Bấm「＋ 新規追加」\n"
       "2. Nhập đúng tên「ST_DUP_{RUN}」đã tồn tại\n"
       "3. Nhấn Enter, quan sát thông báo\n"
       "4. Đếm số dòng cùng tên trong danh sách",
       "ST_DUP_{RUN}",
       "- KHÔNG tạo được trạng thái trùng tên\n"
       "- Hiển thị thông báo lỗi\n"
       "- Danh sách chỉ có đúng 1 dòng tên「ST_DUP_{RUN}」",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-05 — rule này CHỈ có ở V3333 r225 (NEW-232, 08/2026, QA-01 mục 1 do BA "
            "chốt), TC đang ở trạng thái `skip` kèm ghi chú『NGHI THIẾU: mục nằm trong 21 mục QA-01 "
            "nhưng KHÔNG có trong code sửa lần này』. Spec FA-041 và corpus [AI] 06-07/2026 KHÔNG có "
            "rule unique. DỰ KIẾN FAIL trên bản đang chạy → nếu tạo được trùng thì là hạng mục còn "
            "thiếu, báo Leader, không tính bug mới. V3333 r223 (NEW-66) và r224 (NEW-145) là bản trùng"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Boundary",
       "Thêm 2 trạng thái liên tiếp không reload rồi F5 — cả 2 đều còn, đúng thứ tự",
       TAB1 + "\n- Danh sách có sẵn ≥ 1 trạng thái",
       "1. Bấm「＋ 新規追加」→ nhập「連続1」+ Enter (không reload)\n"
       "2. Ngay sau đó bấm「＋ 新規追加」→ nhập「連続2」+ Enter (không reload)\n"
       "3. Nhấn F5 reload trang",
       "連続1, 連続2",
       "- Sau bước 2: cả「連続1」và「連続2」đều hiển thị, không mất bản ghi nào\n"
       "- Sau F5: danh sách y hệt trạng thái ngay sau bước 2, đúng thứ tự đã thêm",
       note="Nguồn: v2 r18 (TC-SC-073, Pass staging + production) — FUNC-SEQ-001"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Boundary",
       "Xóa rồi thêm mới ngay, không reload — bản ghi mới không nhận nhầm vị trí bản vừa xóa",
       TAB1 + "\n- Có ≥ 2 trạng thái, trạng thái thứ 2 tên「削除対象」",
       "1. Xóa trạng thái「削除対象」qua modal xác nhận (không reload)\n"
       "2. Ngay sau đó bấm「＋ 新規追加」→ nhập「テスト追加」+ Enter (không reload)\n"
       "3. Nhấn F5 reload trang",
       "テスト追加",
       "- Sau bước 2:「削除対象」không còn,「テスト追加」nằm ở CUỐI danh sách\n"
       "-「テスト追加」KHÔNG nhận vị trí hay thuộc tính của bản ghi vừa xóa\n"
       "- Sau F5: danh sách khớp y hệt trạng thái ngay sau bước 2",
       note="Nguồn: v2 r19 (TC-SC-074, Pass staging + production)"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Boundary",
       "Thêm → Sửa → Xóa liên tiếp không reload — không lỗi JS, nút vẫn dùng được",
       TAB1,
       "1. Bấm「＋ 新規追加」→ nhập「A」+ Enter\n"
       "2. Ngay sau đó sửa tên「A」thành「B」+ Enter\n"
       "3. Ngay sau đó bấm icon xóa「B」→「削除する」\n"
       "4. Bấm「＋ 新規追加」lần nữa",
       "A → B",
       "- Mỗi bước có toast đúng:「保存しました」/「削除されました」\n"
       "- KHÔNG có lỗi JavaScript trên console trong suốt chuỗi\n"
       "- Sau xóa: danh sách cập nhật đúng, không còn「B」\n"
       "- Bước 4: nút「＋ 新規追加」vẫn sinh được dòng nhập mới (handler không bị stale)",
       note="Nguồn: v2 r42 (TC-SC-144, Pass staging + production; BUG-008 click-nuốt Closed)"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Normal",
       "Sửa → F5 → sửa tiếp chính trạng thái đó — không lỗi JS sau reload",
       HAS1,
       "1. Sửa tên + màu của trạng thái「Y」→ toast「保存しました」\n"
       "2. Nhấn F5\n"
       "3. Sau reload, sửa tiếp tên/màu của「Y」lần nữa",
       "Y",
       "- Sau F5:「Y」hiển thị đúng giá trị đã sửa ở bước 1\n"
       "- Bước 3 sửa tiếp thành công, toast「保存しました」, dữ liệu cập nhật đúng\n"
       "- KHÔNG lỗi JS trên console; ô nhập và bộ chọn màu vẫn dùng được sau reload",
       note="Nguồn: v2 r44 (TC-SC-146, Pass staging + production)"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Boundary",
       "Thêm → F5 → xóa chính trạng thái vừa thêm",
       TAB1,
       "1. Thêm trạng thái「Z」→ toast「保存しました」\n"
       "2. Nhấn F5\n"
       "3. Sau reload bấm icon xóa「Z」→「削除する」",
       "Z",
       "- Sau F5:「Z」vẫn còn trong danh sách (đã lưu DB)\n"
       "- Bước 3: xóa「Z」thành công, toast「削除されました」\n"
       "- KHÔNG lỗi JS; danh sách cập nhật đúng, không còn「Z」",
       note="Nguồn: v2 r45 (TC-SC-147, Pass staging + production)"),

    tc("Thêm & sửa trạng thái", "FUNC-SEQ-001", "Boundary",
       "Nhập dở chưa Enter rồi F5 — dữ liệu đang gõ bị mất, không lưu nhầm",
       TAB1,
       "1. Bấm「＋ 新規追加」→ gõ text vào dòng nhập mới nhưng KHÔNG nhấn Enter\n"
       "2. Nhấn F5\n"
       "3. Quan sát danh sách",
       "テスト",
       "- Text nhập dở bị mất, không được lưu\n"
       "- Danh sách không có trạng thái mới nào\n"
       "- Dòng nhập trống cũng biến mất",
       note="Nguồn: v2 r34 (TC-SC-129, Pass staging + production) · SC r134"),

    tc("Thêm & sửa trạng thái", "CONC-001", "Boundary",
       "Bấm「＋ 新規追加」3 lần liên tiếp khi chưa lưu dòng nào — không sinh trạng thái rỗng",
       TAB1 + "\n- Danh sách đang có < 10 trạng thái",
       "1. Bấm「＋ 新規追加」lần 1 → xuất hiện dòng nhập trống\n"
       "2. KHÔNG nhập gì, bấm tiếp「＋ 新規追加」lần 2 và lần 3\n"
       "3. Đếm số dòng nhập trống ở cuối danh sách\n"
       "4. Nhập「テスト」vào 1 dòng bất kỳ + Enter\n"
       "5. Nhấn F5 reload",
       "テスト",
       "- Sau bước 4: chỉ tạo đúng 1 trạng thái「テスト」\n"
       "- KHÔNG tạo trạng thái rỗng nào từ các dòng nhập trống còn lại\n"
       "- Sau F5: các dòng nhập trống chưa lưu biến mất, danh sách chỉ còn trạng thái thật\n"
       "- Không có lỗi JS trên console",
       spec="Đã hỏi leader",
       note="⏳ Số dòng trống được phép sinh (nhiều dòng hay tối đa 1) CHƯA chốt — QA-035. "
            "Nguồn: v2 r7 (TC-SC-004c, Pass staging + production) · v1 r16 (BS_006, chưa có kết quả). "
            "Ghi nhận thực tế qua CLI: 3 lần bấm sinh 3 dòng client-side, 0 XHR"),

    tc("Thêm & sửa trạng thái", "LIST-001", "Boundary",
       "Bấm「＋ 新規追加」khi trang hiện tại đã đủ 10 trạng thái",
       TAB1 + "\n- Trang hiện tại đã có đúng 10 trạng thái (đầy 1 trang phân trang)",
       "1. Bấm「＋ 新規追加」\n"
       "2. Quan sát vị trí dòng nhập mới và phân trang\n"
       "3. Nhập tên + Enter\n"
       "4. Quan sát trạng thái vừa tạo nằm ở trang nào",
       "10 trạng thái sẵn có + 1 trạng thái mới",
       "- Ghi nhận hành vi thực tế: dòng nhập mới xuất hiện ở trang hiện tại hay hệ thống\n"
       "  tự chuyển sang trang kế\n"
       "- Sau khi lưu: trạng thái mới xuất hiện đúng 1 lần, không nhân đôi giữa 2 trang\n"
       "- Phân trang cập nhật thành 2 trang",
       spec="Đã hỏi leader",
       note="⚠️ Phụ thuộc MT-13. Nguồn: v1 r17 (BS_007, Pass nhưng Expected gốc chỉ ghi『Confirm』) — "
            "kết quả mong đợi do AI viết, CẦN LEADER XÁC NHẬN"),
]

S4 = [
    tc("Sắp xếp trạng thái", "FUNC-001", "Normal",
       "Kéo thả đổi vị trí 1 trạng thái — tự lưu ngay",
       TAB1 + "\n- Danh sách có ít nhất 2 trạng thái",
       "1. Giữ tay cầm kéo (⠿) của trạng thái đầu tiên\n"
       "2. Thả xuống vị trí thứ 2\n"
       "3. Nhấn F5",
       "—",
       "- Toast「保存しました」xuất hiện\n"
       "- Thứ tự hiển thị đổi đúng theo vị trí vừa thả\n"
       "- Sau F5 thứ tự vẫn đúng (đã ghi cột `position` bảng `status_chat`)",
       note=MT02 + "Nguồn: v2 r10 (TC-SC-007, Pass staging + production) · SC r164. ⚠️ Kỹ thuật kéo: "
            "Sortable.js dùng pointer event thật — automation phải dùng mouse.move/down/up, `dragTo()` "
            "không ăn"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Boundary",
       "Kéo thả 2 lần liên tiếp không reload rồi F5 — thứ tự phản ánh đúng cả 2 lần",
       TAB1 + "\n- Danh sách có ≥ 3 trạng thái",
       "1. Kéo trạng thái ở vị trí 1 xuống vị trí 3 (không reload)\n"
       "2. Ngay sau đó kéo trạng thái đang ở vị trí 1 xuống vị trí 2 (không reload)\n"
       "3. Nhấn F5 reload trang\n"
       "4. Đếm lại tổng số trạng thái",
       "—",
       "- Sau bước 2: thứ tự phản ánh đúng cả 2 lần kéo\n"
       "- Sau F5: thứ tự khớp y hệt trạng thái ngay sau bước 2, không bị đảo lại\n"
       "- Tổng số trạng thái KHÔNG thay đổi — không mất bản ghi nào",
       note="⚠️ Phụ thuộc MT-12 — BUG-021 (Open): v2 r21 (TC-SC-076) FAIL cả staging lẫn production, "
            "chuỗi kéo liên tiếp làm MẤT 2/3 trạng thái. Lặp lại được ≥ 3 lần qua automation nhưng "
            "KHÔNG tái hiện khi thao tác tay. DỰ KIẾN FAIL → chạy tay trước khi kết luận"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Boundary",
       "Thêm liên tiếp rồi kéo thả ngay — không mất trạng thái nào",
       TAB1 + "\n- Danh sách có ≥ 3 trạng thái",
       "1. Thêm liên tiếp 2-3 trạng thái mới (mỗi lần: ＋新規追加 → nhập tên → Enter), không reload\n"
       "2. Ngay sau đó kéo trạng thái đầu tiên xuống vị trí cuối (không reload)\n"
       "3. Sửa tên trạng thái hiện đang ở vị trí đầu thành「編集済み」(không reload)\n"
       "4. Nhấn F5 và đếm lại tổng số trạng thái",
       "編集済み",
       "- Sau bước 3: thứ tự đúng theo bước 2, tên sửa đúng, không trạng thái nào nhảy về chỗ cũ\n"
       "- Sau F5: thứ tự VÀ tên khớp y hệt trạng thái ngay sau bước 3\n"
       "- Tổng số trạng thái không giảm — KHÔNG mất bản ghi nào",
       note="⚠️ Phụ thuộc MT-12 — v2 r20 (TC-SC-075, Skipped cả 2 môi trường). Cùng root cause "
            "BUG-021: sau chuỗi thêm liên tiếp + kéo, mất 2/3 trạng thái. DỰ KIẾN FAIL"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Boundary",
       "Kéo thả → F5 → kéo thả lần nữa — tay cầm kéo vẫn hoạt động sau reload",
       TAB1 + "\n- Danh sách có ≥ 3 trạng thái",
       "1. Kéo thả đổi thứ tự (vd item 1 ↔ item 3) → toast\n"
       "2. Nhấn F5\n"
       "3. Sau reload kéo thả đổi thứ tự lần nữa",
       "—",
       "- Sau F5: danh sách giữ đúng thứ tự đã sắp ở bước 1\n"
       "- Bước 3: kéo thả lần nữa thành công, thứ tự cập nhật đúng\n"
       "- KHÔNG lỗi JS; tay cầm kéo vẫn hoạt động sau reload",
       note="Nguồn: v2 r46 (TC-SC-148, Not Tested)"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Normal",
       "Sắp xếp xong rồi thêm 1 trạng thái mới — trạng thái mới xuống cuối, thứ tự cũ giữ nguyên",
       TAB1 + "\n- Đã kéo thả sắp xếp lại danh sách và đã lưu",
       "1. Bấm「＋ 新規追加」→ nhập tên + Enter\n"
       "2. Quan sát vị trí trạng thái mới và thứ tự các trạng thái cũ\n"
       "3. Nhấn F5",
       "新規ソート後",
       "- Trạng thái mới nằm ở CUỐI danh sách\n"
       "- Thứ tự các trạng thái cũ giữ nguyên như đã sắp xếp\n"
       "- Sau F5 giữ nguyên",
       note="Nguồn: SC r167 (OK + staging OK) · SC r135"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Normal",
       "Sắp xếp xong rồi sửa 1 trạng thái — dữ liệu đổi nhưng thứ tự giữ nguyên",
       TAB1 + "\n- Đã kéo thả sắp xếp lại danh sách và đã lưu",
       "1. Sửa tên + màu của 1 trạng thái ở giữa danh sách + Enter\n"
       "2. Quan sát thứ tự danh sách\n"
       "3. Nhấn F5",
       "ソート後編集",
       "- Tên và màu cập nhật đúng\n"
       "- Trạng thái vừa sửa vẫn nằm đúng vị trí đã sắp xếp, không nhảy chỗ\n"
       "- Sau F5 giữ nguyên",
       note="Nguồn: SC r168 (OK + staging OK) · SC r155-r156"),

    tc("Sắp xếp trạng thái", "FUNC-SEQ-001", "Normal",
       "Sắp xếp xong rồi xóa 1 trạng thái — các trạng thái còn lại giữ đúng thứ tự",
       TAB1 + "\n- Đã kéo thả sắp xếp lại danh sách và đã lưu, có ≥ 3 trạng thái",
       "1. Xóa 1 trạng thái ở giữa danh sách\n"
       "2. Quan sát thứ tự các trạng thái còn lại\n"
       "3. Nhấn F5",
       "—",
       "- Trạng thái bị xóa biến mất khỏi danh sách và khỏi bảng `status_chat`\n"
       "- Các trạng thái còn lại giữ đúng thứ tự đã sắp xếp, không đảo vị trí\n"
       "- Sau F5 giữ nguyên",
       note="Nguồn: SC r166 (OK + staging OK) · SC r182"),
]

S5 = [
    tc("Xóa trạng thái", "FUNC-001", "Normal",
       "Xóa trạng thái — xác nhận trong modal thì xóa thật",
       HAS1,
       "1. Bấm icon xóa (🗑) của 1 trạng thái bất kỳ\n"
       "2. Quan sát modal xác nhận\n"
       "3. Bấm「削除する」\n"
       "4. Nhấn F5",
       "—",
       "- Modal đóng lại, toast「削除されました」\n"
       "- Trạng thái biến mất khỏi danh sách\n"
       "- Sau F5 vẫn không còn (đã xóa bản ghi bảng `status_chat` — hard delete, BR-10)",
       note="Nguồn: v2 r11 (TC-SC-008, Pass staging + production) · SC r181 · SC r185"),

    tc("Xóa trạng thái", "FUNC-001", "Abnormal",
       "Xóa trạng thái — bấm「キャンセル」thì không xóa gì",
       HAS1,
       "1. Bấm icon xóa (🗑) của 1 trạng thái bất kỳ\n"
       "2. Modal xác nhận hiện ra\n"
       "3. Bấm「キャンセル」",
       "—",
       "- Modal đóng lại\n"
       "- Trạng thái vẫn còn trong danh sách, không bị xóa\n"
       "- Không có thay đổi nào trong danh sách",
       note="Nguồn: v2 r12 (TC-SC-009, Pass staging + production)"),

    tc("Xóa trạng thái", "UI-003", "Normal",
       "Modal xóa hiển thị đúng tên trạng thái và nội dung cảnh báo",
       HAS1 + "\n- Trạng thái cần xóa tên「対応完了」",
       "1. Bấm icon xóa (🗑) của trạng thái「対応完了」\n"
       "2. Quan sát tiêu đề và nội dung modal",
       "対応完了",
       "- Tiêu đề modal:「【対応完了】を削除しますか？」— phần trong 【】 là tên trạng thái đang xóa\n"
       "- Nội dung:「削除する場合、友だちに登録されているこの対応ステータスに関する情報が全て削除されます"
       "のでご注意ください。」\n"
       "- Có 2 nút:「削除する」và「キャンセル」\n"
       "- Nền ngoài modal bị làm tối",
       note="⚠️ Phụ thuộc MT-09 — spec feature-spec.md BR-02 ghi『không có cảnh báo UI』, trong khi "
            "SC r178-r180 (OK + staging OK) mô tả đầy đủ modal cảnh báo. Nguồn: SC r178-r180"),

    tc("Xóa trạng thái", "UI-003", "Normal",
       "Modal xóa có checkbox「次から表示しない」, mặc định chưa tích",
       HAS1,
       "1. Bấm icon xóa (🗑) của 1 trạng thái bất kỳ\n"
       "2. Quan sát modal",
       "—",
       "- Modal xác nhận hiện ra\n"
       "- Có checkbox「次から表示しない」trong modal\n"
       "- Checkbox ở trạng thái CHƯA tích",
       note="Nguồn: v2 r17 (TC-SC-013, Pass staging + production). Checkbox này KHÔNG có trong spec"),

    tc("Xóa trạng thái", "STATE-001", "Normal",
       "Tích「次から表示しない」— lần xóa sau không hiện modal nữa, chỉ trong cùng trình duyệt",
       HAS1 + "\n- Có ≥ 2 trạng thái để xóa 2 lần",
       "1. Bấm icon xóa (🗑) của trạng thái A\n"
       "2. Tích checkbox「次から表示しない」\n"
       "3. Bấm「削除する」\n"
       "4. Bấm icon xóa (🗑) của trạng thái B trong cùng phiên\n"
       "5. Nhấn F5 rồi bấm icon xóa 1 trạng thái khác\n"
       "6. Mở cùng trang bằng trình duyệt KHÁC (hoặc cửa sổ ẩn danh) và bấm icon xóa",
       "—",
       "- Bước 4: modal xác nhận KHÔNG hiện lại, trạng thái B bị xóa ngay\n"
       "- Bước 5: sau F5 vẫn giữ lựa chọn, modal vẫn không hiện\n"
       "- Bước 6: ở trình duyệt khác modal VẪN hiện — lựa chọn chỉ lưu theo trình duyệt (localStorage),\n"
       "  không đồng bộ sang phiên/trình duyệt khác",
       note="Nguồn: v2 r29 (TC-SC-121, Pass staging + production; BUG-022 Closed 2026-07-29 — dev đã "
            "fix, ghi đúng localStorage)"),

    tc("Xóa trạng thái", "DATA-REF-001", "Normal",
       "Xóa trạng thái đang gán cho hội thoại — không cảnh báo, hội thoại được gỡ trạng thái",
       TAB1 + "\n- Có ít nhất 1 trạng thái đang được gán cho ít nhất 1 hội thoại của LOA",
       "1. Bấm icon xóa (🗑) của trạng thái đang được gán cho hội thoại\n"
       "2. Quan sát modal có cảnh báo số hội thoại bị ảnh hưởng không\n"
       "3. Bấm「削除する」\n"
       "4. Kiểm tra lại các hội thoại từng gán trạng thái đó",
       "—",
       "- KHÔNG có cảnh báo số hội thoại bị ảnh hưởng (BR-02 — hard delete, không báo trước)\n"
       "- Modal đóng, trạng thái bị xóa khỏi danh sách\n"
       "- Các hội thoại từng gán trạng thái này có `conversation.id_status` được đặt về NULL",
       note="Nguồn: v2 r13 (TC-SC-009b, Pass staging) — BR-02 / BR-10. "
            "Phần hiển thị ở màn chat 1:1 tách sang nhóm『Đồng bộ trạng thái sang nơi dùng』"),

    tc("Xóa trạng thái", "FUNC-SEQ-001", "Normal",
       "Xóa liên tiếp 2 trạng thái không reload — cả 2 đều mất, không lỗi",
       TAB1 + "\n- Có ≥ 3 trạng thái",
       "1. Xóa trạng thái A (xác nhận modal)\n"
       "2. Ngay sau đó xóa trạng thái B (không reload)\n"
       "3. Nhấn F5",
       "—",
       "- Cả A và B đều biến mất khỏi danh sách\n"
       "- Sau F5 vẫn không còn cả 2\n"
       "- Không lỗi JS, các trạng thái còn lại không bị xóa nhầm",
       note="Nguồn: SC r183 (OK + staging OK)"),

    tc("Xóa trạng thái", "FUNC-SEQ-001", "Normal",
       "Xóa xong rồi thêm mới ngay — trạng thái mới tạo đúng, không kế thừa bản vừa xóa",
       TAB1 + "\n- Có ≥ 2 trạng thái",
       "1. Xóa 1 trạng thái\n"
       "2. Ngay sau đó bấm「＋ 新規追加」→ nhập tên mới + Enter\n"
       "3. Nhấn F5",
       "削除後追加",
       "- Trạng thái mới được tạo với màu mặc định, nằm cuối danh sách\n"
       "- KHÔNG mang tên/màu/vị trí của trạng thái vừa xóa\n"
       "- Sau F5 giữ nguyên",
       note="Nguồn: SC r184 (OK + staging OK)"),
]
