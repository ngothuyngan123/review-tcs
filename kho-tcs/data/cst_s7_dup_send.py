# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 15-16: Tab 8「重複送信防止機能」.

S15 Chống gửi trùng — cài đặt (màn Tab 8)
S16 Chống gửi trùng — chặn gửi thực tế (side-effect ở FA-001 web + app mobile admin)

✅ MT-01 đã chốt 2026-09-21: màn có 8 tab ⇒ Tab 8 NẰM TRONG phạm vi FA-041.
⚠️ Nhưng spec CHƯA quét màn SCR-08B — chưa có bản spec chính thức để đối chiếu.
⚠️ Có 2 CƠ CHẾ KHÁC NHAU chạy cùng lúc, không được lẫn lộn:
  (a) send-lock nội bộ — chặn double-submit của CHÍNH người đang gửi (bảng
      `chat_send_locks`), luôn bật, không liên quan Tab 8;
  (b) chặn chéo theo BR-08B-02 — trong N phút sau khi 1 người gửi, NGƯỜI KHÁC
      không gửi được cho cùng hội thoại; chỉ hoạt động khi Tab 8 = ON.
"""
from _common import tc

T8 = ("- Đăng nhập Admin của LOA, đã chọn 1 bot\n"
      "- Đang ở `/basic/chat-setting` Tab 8「重複送信防止機能」")
T8_ON = T8 + "\n- Toggle「重複送信防止機能」đang BẬT"
NOSPEC = "⚠️ Tab 8 trong phạm vi (MT-01 đã chốt 8 tab) nhưng spec CHƯA quét. "

S15 = [
    tc("Chống gửi trùng — cài đặt", "UI-003", "Normal",
       "Trạng thái mặc định của Tab 8 khi bot chưa từng cấu hình",
       T8 + "\n- Bot mới, chưa từng cấu hình Tab 8",
       "1. Mở Tab 8「重複送信防止機能」lần đầu\n"
       "2. Quan sát toggle và ô nhập「送信停止時間」",
       "—",
       "- Ghi nhận giá trị mặc định thực tế của toggle\n"
       "- Đối chiếu với các cờ khác trong bảng `bots` (`confirm_message_*` = 0, `is_shorten_url` = 0)",
       spec="Đã hỏi leader",
       note=NOSPEC + "⚠️ Phụ thuộc MT-17 — giá trị mặc định CHƯA được chốt (⏳ QA-021 / QA-011). "
            "TA đề xuất mặc định TẮT cho nhất quán nhưng reviewer chưa xác nhận. "
            "Nguồn: v2 r148 (TC-SC-098, Skipped cả 2 môi trường)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-001", "Normal",
       "Bật toggle — tự lưu ngay, không có nút「保存」riêng",
       T8 + "\n- Toggle đang TẮT",
       "1. Quan sát toàn bộ trang Tab 8, xác nhận không có nút「保存」độc lập\n"
       "2. Bấm toggle「重複送信防止機能」sang BẬT",
       "—",
       "- Bước 1: xác nhận KHÔNG có nút「保存」riêng trên trang\n"
       "- Bước 2: toast「保存しました」xuất hiện ngay sau khi toggle đổi trạng thái\n"
       "- Cài đặt được lưu tự động, không cần thao tác nào thêm",
       note=NOSPEC + "BR-08B-04 (QA-024). ⚠️ Khác hẳn Tab 3-6 (có nút「保存」). "
            "Nguồn: v2 r135 (TC-SC-044, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-001", "Normal",
       "Tắt toggle — tự lưu ngay",
       T8_ON,
       "1. Bấm toggle「重複送信防止機能」sang TẮT",
       "—",
       "- Toast「保存しました」xuất hiện\n"
       "- Toggle ở trạng thái TẮT",
       note=NOSPEC + "Nguồn: v2 r136 (TC-SC-045, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-001", "Normal",
       "Đổi giá trị「送信停止時間」— tự lưu khi rời ô nhập",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị 15\n"
       "3. Bấm ra ngoài ô nhập (blur)",
       "15",
       "- Toast「保存しました」xuất hiện\n"
       "- Giá trị 15 phút được lưu",
       note=NOSPEC + "Nguồn: v2 r137 (TC-SC-046, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-004", "Boundary",
       "Nhập 1 phút — giá trị biên nhỏ nhất hợp lệ",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị 1\n"
       "3. Bấm ra ngoài ô nhập",
       "1",
       "- Toast「保存しました」xuất hiện\n"
       "- Giá trị 1 phút lưu thành công, không báo lỗi",
       note=NOSPEC + "BR-08B-03 (QA-022). Nguồn: v2 r140 (TC-SC-049, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-004", "Boundary",
       "Nhập 60 phút — giá trị biên lớn nhất hợp lệ",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị 60\n"
       "3. Bấm ra ngoài ô nhập",
       "60",
       "- Toast「保存しました」xuất hiện\n"
       "- Giá trị 60 phút lưu thành công, không báo lỗi",
       note=NOSPEC + "BR-08B-03. Nguồn: v2 r141 (TC-SC-050, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-004", "Abnormal",
       "Nhập 0 phút — báo lỗi dưới giá trị nhỏ nhất",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị 0\n"
       "3. Bấm ra ngoài ô nhập",
       "0",
       "- Hiển thị lỗi validation (nhỏ nhất là 1 phút)\n"
       "- Giá trị 0 KHÔNG được lưu",
       note=NOSPEC + "BR-08B-03. Nguồn: v2 r138 (TC-SC-047, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-004", "Abnormal",
       "Nhập 61 phút — báo lỗi vượt giá trị lớn nhất",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị 61\n"
       "3. Bấm ra ngoài ô nhập",
       "61",
       "- Hiển thị lỗi validation (lớn nhất là 60 phút)\n"
       "- Giá trị 61 KHÔNG được lưu",
       note=NOSPEC + "BR-08B-03. Nguồn: v2 r139 (TC-SC-048, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-002", "Abnormal",
       "Xóa trắng ô「送信停止時間」khi toggle BẬT — báo bắt buộc, giữ giá trị cũ",
       T8_ON + " và đang có giá trị hợp lệ",
       "1. Xóa toàn bộ giá trị trong ô「送信停止時間」, để trống\n"
       "2. Bấm ra ngoài ô nhập\n"
       "3. Nhấn F5 và quan sát lại giá trị",
       "(để trống)",
       "- Hiển thị lỗi bắt buộc nhập (ô này bắt buộc khi toggle BẬT)\n"
       "- Giá trị KHÔNG được lưu\n"
       "- Sau F5 vẫn là giá trị hợp lệ trước đó",
       note=NOSPEC + "Nguồn: v2 r145 (TC-SC-095, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-003", "Abnormal",
       "Nhập chữ vào ô「送信停止時間」— bị chặn hoặc báo lỗi",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Cố nhập「abc」vào ô",
       "abc",
       "- Ô nhập chặn ký tự chữ, hoặc báo lỗi validation khi rời ô\n"
       "- Giá trị không hợp lệ KHÔNG được lưu",
       note=NOSPEC + "DI-04: nhập sai định dạng vào ô số. Nguồn: v2 r146 (TC-SC-096, Pass staging + "
            "production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-003", "Abnormal",
       "Nhập số âm vào ô「送信停止時間」— báo lỗi",
       T8_ON,
       "1. Xóa giá trị hiện tại trong ô「送信停止時間」\n"
       "2. Nhập giá trị -5\n"
       "3. Bấm ra ngoài ô nhập",
       "-5",
       "- Hiển thị lỗi validation (giá trị phải ≥ 1)\n"
       "- Giá trị -5 KHÔNG được lưu",
       note=NOSPEC + "Nguồn: v2 r147 (TC-SC-097, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "UI-FIELD-001", "Normal",
       "Toggle TẮT — ô「送信停止時間」ẩn hoặc bị khóa",
       T8_ON + " và đang có giá trị hợp lệ",
       "1. Bấm toggle「重複送信防止機能」sang TẮT\n"
       "2. Quan sát ô「送信停止時間」",
       "—",
       "- Ghi nhận hành vi thực tế: ô nhập ẩn hoàn toàn HOẶC vẫn hiện nhưng bị khóa (xám)\n"
       "- Dù theo cách nào cũng KHÔNG sửa được giá trị khi toggle đang TẮT",
       spec="Đã hỏi leader",
       note=NOSPEC + "⚠️ Phụ thuộc MT-18 — ⏳ QA-023 chưa chốt ẩn hay khóa. Nguồn: v2 r149 "
            "(TC-SC-099, Pass staging + production); v2 r160 (TC-SC-157) lại ghi『ẩn hoàn toàn』"),

    tc("Chống gửi trùng — cài đặt", "UI-FIELD-001", "Normal",
       "Tắt rồi bật lại toggle — ô「送信停止時間」giữ nguyên giá trị đã nhập trước đó",
       T8_ON,
       "1. Xóa giá trị hiện tại, nhập 30 (khác mặc định)\n"
       "2. Bấm ra ngoài ô nhập để tự lưu\n"
       "3. Tắt toggle「重複送信防止機能」\n"
       "4. Bật lại toggle\n"
       "5. Quan sát ô「送信停止時間」",
       "30",
       "- Ô「送信停止時間」hiện trở lại sau khi bật lại toggle\n"
       "- Giá trị là 30 — GIỮ NGUYÊN giá trị đã nhập trước đó\n"
       "- KHÔNG bị đặt lại về giá trị mặc định",
       spec="Đã hỏi leader",
       note=NOSPEC + "⏳ QA-034 (mở 2026-07-23) — hành vi giữ giá trị là SUY LUẬN, chưa chốt. "
            "Liên quan BUG-011 (Closed — đã xác nhận ô nhập ẩn khi TẮT). "
            "Nguồn: v2 r160 (TC-SC-157, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "CONC-001", "Boundary",
       "Bật/tắt toggle 4 lần thật nhanh — chỉ ghi nhận trạng thái CUỐI",
       T8 + "\n- Toggle đang TẮT",
       "1. Bấm toggle BẬT → TẮT → BẬT → TẮT thật nhanh liên tiếp (4 lần trong ~2 giây)\n"
       "2. Chờ 3 giây rồi nhấn F5\n"
       "3. Quan sát toggle",
       "—",
       "- Chỉ trạng thái CUỐI CÙNG (TẮT) được lưu vào DB\n"
       "- Không có hiện tượng 4 request tự lưu ghi đè nhau sai thứ tự\n"
       "- Sau F5: toggle hiển thị đúng TẮT, khớp thao tác cuối",
       note=NOSPEC + "CONC-001 + DI-21 (toggle). Nguồn: v2 r144 (TC-SC-094, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "FUNC-SEQ-001", "Normal",
       "Bật toggle rồi F5 — trạng thái và giá trị phút vẫn giữ",
       T8 + "\n- Toggle đang TẮT",
       "1. Bấm toggle「重複送信防止機能」sang BẬT, chờ toast「保存しました」\n"
       "2. Nhấn F5 rồi quay lại Tab 8",
       "—",
       "- Sau F5: toggle vẫn BẬT\n"
       "- Giá trị ô「送信停止時間」giữ nguyên như trước khi reload",
       note=NOSPEC + "Nguồn: v2 r150 (TC-SC-100, Pass staging + production)"),

    tc("Chống gửi trùng — cài đặt", "CONC-002", "Normal",
       "Đổi số phút giữa lúc đang trong thời gian chặn — áp ngay giá trị mới",
       "- Tab 8 = ON, số phút = 10\n"
       "- Staff A vừa gửi tin cho hội thoại X (thời điểm T)\n"
       "- Staff B đang mở hội thoại X ở màn chat 1:1",
       "1. Tại phút thứ 6 kể từ T, Staff B thử gửi tin cho hội thoại X — xác nhận bị chặn\n"
       "2. Staff B vào Tab 8, đổi số phút từ 10 xuống 5, chờ tự lưu\n"
       "3. Staff B quay lại hội thoại X và gửi tin",
       "10 phút → 5 phút",
       "- Bước 1: Staff B bị chặn (hiện thông báo không gửi được)\n"
       "- Sau bước 2: giá trị thời gian chặn của bot = 5 (giá trị của lần lưu cuối)\n"
       "- Bước 3: Staff B gửi được bình thường (đã quá 5 phút kể từ T)\n"
       "- Từ lúc này mọi người kể cả admin đều áp mốc 5 phút",
       note=NOSPEC + "Nguồn: v1 r152 (BS_051, OK)"),
]

S16 = [
    tc("Chống gửi trùng — chặn gửi thực tế", "OUT-TRUTH-001", "Abnormal",
       "Tab 8 BẬT — người khác gửi trong thời gian chặn thì hiện thông báo không gửi được",
       "- Tab 8 = ON, số phút = 5\n"
       "- Staff A vừa gửi tin cho hội thoại X trong vòng 5 phút\n"
       "- Staff B đang mở hội thoại X ở màn chat 1:1 (FA-001)",
       "1. Staff B mở hội thoại X tại màn chat 1:1\n"
       "2. Staff B nhập nội dung tin nhắn\n"
       "3. Staff B bấm nút gửi\n"
       "4. Reload hội thoại và đếm số tin",
       "テスト送信",
       "- Modal「現在、メッセージの送信ができません」hiện ra TẠI MÀN CHAT 1:1 (không phải màn cài đặt)\n"
       "- Tin của Staff B KHÔNG được gửi\n"
       "- Sau reload, hội thoại không tăng tin nào",
       note=NOSPEC + "BR-08B-02. Nguồn: v2 r142 (TC-SC-051, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "OUT-TRUTH-001", "Abnormal",
       "Thông báo chặn hiển thị đúng tên người đã gửi gần nhất",
       "- Tab 8 = ON\n"
       "- Staff A có tên hiển thị「田中」vừa gửi tin cho hội thoại X trong thời gian chặn\n"
       "- Staff B đang mở hội thoại X",
       "1. Staff B cố gửi tin cho hội thoại X\n"
       "2. Đọc nội dung thông báo hiện ra",
       "—",
       "- Thông báo hiển thị đúng tên:「田中 さんが直前にメッセージを送信したため...」\n"
       "- Tên hiển thị lấy từ `users.username` của Staff A, KHÔNG phải email hay tên hiển thị khác",
       note=NOSPEC + "BR-08B-05 (QA-025). ⚠️ Trường hợp staff đã bị xóa CHƯA xác định (UP-21 còn mở). "
            "Nguồn: v2 r143 (TC-SC-052, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Abnormal",
       "Admin gửi trước — 1 Staff khác bị chặn, Admin vẫn gửi tiếp được",
       "- Tab 8 = ON, số phút = 5\n"
       "- Admin chủ và Staff A cùng mở hội thoại X ở màn chat 1:1",
       "1. Admin chủ gửi tin cho hội thoại X (ghi thời điểm T)\n"
       "2. Trong vòng 5 phút, Staff A mở hội thoại X → nhập nội dung → bấm gửi\n"
       "3. Admin chủ gửi thêm 1 tin nữa cho hội thoại X",
       "テスト送信",
       "- Bước 2: Staff A thấy thông báo「現在、メッセージの送信ができません。」kèm tên Admin chủ\n"
       "  và thời gian chặn 5 phút; tin của Staff A KHÔNG được gửi\n"
       "- Bước 3: Admin chủ (người gửi trước) VẪN gửi được, không tự chặn mình",
       note=NOSPEC + "⚠️ Phụ thuộc MT-16 — spec màn ghi「他のスタッフ」nhưng user đã chốt 2026-06-05 "
            "rằng rule áp cả Admin. Nguồn: v2 r152 (TC-SC-149, Not Tested) · v1 r154 (BS_053)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Abnormal",
       "Staff gửi trước — Admin chủ cũng bị chặn, không được miễn trừ",
       "- Tab 8 = ON, số phút = 5\n"
       "- Staff A vừa gửi tin cho hội thoại X\n"
       "- Admin chủ đang mở hội thoại X",
       "1. Staff A gửi tin cho hội thoại X (thời điểm T)\n"
       "2. Trong thời gian chặn, Admin chủ cố gửi tin cho hội thoại X\n"
       "3. Staff A gửi thêm 1 tin nữa",
       "テスト送信",
       "- Bước 2: Admin chủ thấy thông báo chặn kèm tên Staff A; tin của Admin KHÔNG được gửi\n"
       "- Bước 3: Staff A (người gửi trước) vẫn gửi tiếp được",
       note=NOSPEC + "⚠️ Phụ thuộc MT-16 — Admin KHÔNG được miễn. Nguồn: v2 r154 (TC-SC-151, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Abnormal",
       "Nhiều người cùng bị chặn — trong 1 cửa sổ chỉ 1 người gửi được",
       "- Tab 8 = ON, số phút = 5\n"
       "- Người A (Admin hoặc Staff) vừa gửi tin cho hội thoại X\n"
       "- Staff B và Staff C cùng đang mở hội thoại X",
       "1. Người A gửi tin cho hội thoại X (thời điểm T)\n"
       "2. Staff B cố gửi\n"
       "3. Staff C cố gửi\n"
       "4. Reload hội thoại X và đếm số tin phát sinh",
       "テスト送信",
       "- Cả Staff B và Staff C đều thấy thông báo chặn, đều hiển thị tên Người A\n"
       "- Tin của B và C đều KHÔNG được gửi\n"
       "- Hội thoại X chỉ tăng đúng 1 tin (của Người A) trong cửa sổ chặn",
       note=NOSPEC + "Gộp 2 ma trận vai trò (Admin→2 Staff của v2 r153/TC-SC-150 và Staff A→Staff B,C "
            "của v2 r155/TC-SC-152) vì CÙNG 1 kết quả mong đợi『chỉ 1 người gửi được』. "
            "Cả 2 đều Not Tested"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Normal",
       "Người gửi trước gửi tiếp — đồng hồ chặn tính lại từ lần gửi mới",
       "- Tab 8 = ON, số phút = 10\n"
       "- Staff A và Staff B cùng mở hội thoại X",
       "1. Staff A gửi tin cho hội thoại X (thời điểm T)\n"
       "2. Ở phút thứ 6, Staff B cố gửi — xác nhận bị chặn\n"
       "3. Ở phút thứ 6, Staff A gửi thêm 1 tin nữa (thời điểm T2)\n"
       "4. Ở phút thứ 11 kể từ T (tức phút thứ 5 kể từ T2), Staff B cố gửi lại",
       "—",
       "- Bước 2: Staff B bị chặn\n"
       "- Bước 3: Staff A gửi được; mốc bắt đầu chặn được cập nhật thành T2\n"
       "- Bước 4: Staff B VẪN bị chặn (mới 5 phút kể từ T2, chưa đủ 10 phút)",
       note=NOSPEC + "Nguồn: v1 r154 (BS_053) · v1 r155 (BS_054 — bản trên app). TC gốc ghi expected "
            "ở tầng DB (`chat_send_locks.last_send_at` cập nhật) — ở đây viết lại theo quan sát "
            "được trên màn hình"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Số phút = 1 — chặn đúng 1 phút rồi mở lại",
       "- Tab 8 = ON, số phút = 1 (biên nhỏ nhất)\n"
       "- Người A vừa gửi tin cho hội thoại X, Người B đang mở hội thoại X",
       "1. Người A gửi tin cho hội thoại X (ghi thời điểm T)\n"
       "2. Tại T+30 giây, Người B cố gửi\n"
       "3. Tại T+30 giây, Người A gửi tiếp\n"
       "4. Từ T+1 phút trở đi (tính từ lần gửi cuối của A), Người B gửi lại",
       "Số phút = 1",
       "- Bước 2: Người B bị chặn, tin không gửi được\n"
       "- Bước 3: Người A vẫn gửi được trong cửa sổ chặn\n"
       "- Bước 4: Người B gửi được bình thường — hết thời gian chặn",
       note=NOSPEC + "Biên nhỏ nhất. Nguồn: v2 r156 (TC-SC-153, Not Tested) · v1 r157 (BS_056)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Số phút = 60 — chặn đúng 60 phút rồi mở lại",
       "- Tab 8 = ON, số phút = 60 (biên lớn nhất)\n"
       "- Người A vừa gửi tin cho hội thoại X, Người B đang mở hội thoại X",
       "1. Người A gửi tin cho hội thoại X (ghi thời điểm T)\n"
       "2. Tại T+59 phút, Người B cố gửi; Người A cũng gửi thử\n"
       "3. Từ T+60 phút trở đi, Người B gửi lại",
       "Số phút = 60",
       "- Bước 2: Người B bị chặn; Người A vẫn gửi được\n"
       "- Bước 3: Người B gửi được bình thường — cửa sổ chặn đúng 60 phút",
       note=NOSPEC + "Biên lớn nhất. Có thể đối chiếu bằng mốc thời gian của tin nhắn cuối thay vì "
            "chờ thật 60 phút. Nguồn: v2 r159 (TC-SC-156, Not Tested) · v1 r158 (BS_057). "
            "2 mốc trung gian 2 phút (v2 r157) và 59 phút (v2 r158) cùng quy tắc → không tách TC riêng"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Normal",
       "Chặn tính riêng theo TỪNG hội thoại, không chặn chéo sang friend khác",
       "- Tab 8 = ON, số phút = 5\n"
       "- Staff A vừa gửi tin cho hội thoại X\n"
       "- Staff B đang mở hội thoại Y (friend khác) chưa ai gửi trong 5 phút",
       "1. Staff A gửi tin cho hội thoại X\n"
       "2. Trong thời gian chặn, Staff B gửi tin cho hội thoại Y\n"
       "3. Trong thời gian chặn, Staff B cố gửi tin cho hội thoại X",
       "—",
       "- Bước 2: Staff B gửi được bình thường cho hội thoại Y (không bị chặn nhầm)\n"
       "- Bước 3: Staff B bị chặn ở hội thoại X\n"
       "- Cơ chế chặn tính theo từng hội thoại, không theo toàn bot",
       note=NOSPEC + "Nguồn: v1 r153 (BS_052, OK) · v1 r159 (BS_058 — bản trên app)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "REG-SHARED-001", "Normal",
       "Tab 8 TẮT — 2 người gửi liên tiếp cho cùng hội thoại đều gửi được",
       "- Tab 8「重複送信防止機能」= TẮT (đã lưu)\n"
       "- Staff A và Staff B cùng mở hội thoại X",
       "1. Staff A gửi tin cho hội thoại X qua màn chat 1:1\n"
       "2. Ngay sau đó Staff B cũng gửi tin cho hội thoại X\n"
       "3. Reload hội thoại và kiểm tra phía LINE của friend",
       "メッセージ1 / メッセージ2",
       "- KHÔNG có thông báo「現在、メッセージの送信ができません」\n"
       "- Cả 2 tin đều gửi thành công, hiển thị đúng thứ tự\n"
       "- Friend nhận đủ 2 tin trên LINE",
       note=NOSPEC + "Bảo vệ chống chặn nhầm. Nguồn: v2 r151 (TC-SC-101, Not Tested) · "
            "v2 r176 (TC-SC-176, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "REG-SHARED-001", "Normal",
       "Tab 8 BẬT — chính người gửi đầu double-click thì chỉ ra 1 tin, KHÔNG tự chặn mình",
       "- Tab 8 = ON, số phút = 5\n"
       "- Staff A mở hội thoại X (chưa ai gửi trong 5 phút gần đây)",
       "1. Staff A nhập nội dung rồi double-click nút gửi\n"
       "2. Quan sát màn hình Staff A\n"
       "3. Reload hội thoại và đếm số tin\n"
       "4. Staff B cố gửi cho hội thoại X",
       "テスト送信",
       "- Hội thoại tăng ĐÚNG 1 tin\n"
       "- KHÔNG hiện thông báo chặn cho chính Staff A (người gửi trước không tự chặn mình)\n"
       "- Bước 4: Staff B vẫn bị chặn đúng theo BR-08B-02",
       note=NOSPEC + "⚠️ 2 cơ chế chạy cùng lúc: send-lock (chặn double-submit) và chặn chéo "
            "(BR-08B-02) — không được lẫn lộn. Nguồn: v2 r177 (TC-SC-177, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Double-click gửi TEXT ở chat 1:1 — chỉ 1 tin tới friend",
       "- Mở hội thoại X ở màn chat 1:1 (FA-001)\n"
       "- Ghi lại số tin hiện có trong hội thoại",
       "1. Nhập nội dung tin nhắn\n"
       "2. Double-click nút gửi (2 lần bấm trong < 1 giây)\n"
       "3. Reload hội thoại\n"
       "4. Kiểm tra phía LINE của friend",
       "テスト送信",
       "- Hội thoại tăng ĐÚNG 1 tin, không có 2 tin trùng nội dung\n"
       "- Friend nhận ĐÚNG 1 tin trên LINE",
       note=NOSPEC + "Cơ chế send-lock, KHÁC cơ chế chặn chéo của Tab 8. "
            "Nguồn: v2 r170 (TC-SC-170, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Double-click gửi TEMPLATE ở chat 1:1 — chỉ 1 tin tới friend",
       "- Mở hội thoại X ở màn chat 1:1, có sẵn ≥ 1 template dùng được",
       "1. Chọn 1 template\n"
       "2. Double-click nút gửi\n"
       "3. Reload hội thoại và kiểm tra phía LINE của friend",
       "1 template bất kỳ",
       "- Hội thoại tăng ĐÚNG 1 tin template\n"
       "- Friend nhận ĐÚNG 1 tin\n"
       "- Nội dung template hiển thị và lưu đúng",
       note=NOSPEC + "Nguồn: v2 r171 (TC-SC-171, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Double-click gửi MEDIA ở chat 1:1 — chỉ 1 tin và chỉ 1 file được tải lên",
       "- Mở hội thoại X ở màn chat 1:1, có sẵn file ảnh để gửi",
       "1. Chọn file ảnh\n"
       "2. Double-click nút gửi\n"
       "3. Reload hội thoại\n"
       "4. Kiểm tra file đã tải lên và phía LINE của friend",
       "1 file ảnh",
       "- Hội thoại tăng ĐÚNG 1 tin media\n"
       "- Chỉ 1 file được tải lên / lưu, không sinh 2 bản trùng\n"
       "- Friend nhận ĐÚNG 1 tin",
       env="PRODUCTION",
       note=NOSPEC + "RULE-08: media → chạy PRODUCTION. Nguồn: v2 r172 (TC-SC-172, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Abnormal",
       "Mạng chập chờn khi gửi rồi gửi lại — friend chỉ nhận 1 tin",
       "- Mở hội thoại X ở màn chat 1:1\n"
       "- Chuẩn bị công cụ giả lập mạng chậm / ngắt (DevTools throttling)",
       "1. Nhập nội dung, bấm gửi\n"
       "2. Giả lập request treo / timeout phía trình duyệt\n"
       "3. Bấm gửi lại (hoặc để trình duyệt tự thử lại)\n"
       "4. Khôi phục mạng, reload hội thoại\n"
       "5. Kiểm tra phía LINE của friend",
       "テスト送信",
       "- Friend nhận ĐÚNG 1 tin, không phải 2 tin do thử lại\n"
       "- Hội thoại phía admin hiển thị đúng 1 tin, không có bản trùng\n"
       "- Nếu lần gửi đầu thất bại thật thì chỉ có tin của lần thử lại",
       note=NOSPEC + "Nguồn: v2 r173 (TC-SC-173, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Nhấn phím tắt gửi 2 lần liên tiếp — chỉ 1 tin, phím tắt không vượt được khóa",
       "- Tab 4「送信ショートカット」đã cấu hình phím tắt và đã lưu\n"
       "- Mở hội thoại X ở màn chat 1:1",
       "1. Nhập nội dung tin nhắn\n"
       "2. Nhấn tổ hợp phím tắt đã cấu hình 2 lần liên tiếp thật nhanh\n"
       "3. Reload hội thoại và kiểm tra phía LINE của friend",
       "ショートカットテスト",
       "- Hội thoại tăng ĐÚNG 1 tin\n"
       "- Friend nhận đúng 1 tin\n"
       "- Đường gửi bằng phím tắt vẫn đi qua khóa chống gửi trùng",
       note=NOSPEC + "Nối BR-05-02 (phím tắt là cơ chế phía trình duyệt) với khóa gửi. "
            "Nguồn: v2 r174 (TC-SC-174, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "CONC-001", "Boundary",
       "Preview BẬT — double-click nút xác nhận trong modal xem trước chỉ gửi 1 tin",
       "- Tab 6「送信プレビュー」= BẬT\n"
       "- Mở hội thoại X ở màn chat 1:1",
       "1. Nhập nội dung, bấm gửi → modal xem trước hiện ra\n"
       "2. Double-click nút xác nhận gửi trong modal\n"
       "3. Reload hội thoại và kiểm tra phía LINE của friend",
       "プレビューテスト",
       "- Hội thoại tăng ĐÚNG 1 tin\n"
       "- Modal xem trước đóng đúng 1 lần, không gửi lặp\n"
       "- Friend nhận đúng 1 tin",
       note=NOSPEC + "Nguồn: v2 r175 (TC-SC-175, Pass staging)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "SYNC-APP-001", "Boundary",
       "App mobile admin — double-click gửi text chỉ ra 1 tin, gắn đúng người gửi",
       "- Đăng nhập app mobile admin (KHÔNG phải LIFF) bằng tài khoản Staff A\n"
       "- Mở hội thoại X trên app",
       "1. Nhập nội dung tin nhắn\n"
       "2. Bấm nút gửi 2 lần liên tiếp thật nhanh\n"
       "3. Kéo refresh hội thoại trên app\n"
       "4. Mở cùng hội thoại trên web để đối chiếu",
       "アプリ送信テスト",
       "- Hội thoại tăng ĐÚNG 1 tin, trên cả app lẫn web\n"
       "- Tin gắn đúng người gửi là Staff A\n"
       "- Friend nhận đúng 1 tin trên LINE",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r178 (TC-SC-178, Not Tested). RULE-08: thiết bị thật → PRODUCTION"),

    tc("Chống gửi trùng — chặn gửi thực tế", "SYNC-APP-001", "Boundary",
       "App mobile admin — double-click gửi template chỉ ra 1 tin",
       "- Đăng nhập app mobile admin, mở hội thoại X, có template dùng được",
       "1. Chọn template\n"
       "2. Bấm gửi 2 lần liên tiếp thật nhanh\n"
       "3. Kéo refresh trên app và đối chiếu trên web",
       "1 template bất kỳ",
       "- Tăng ĐÚNG 1 tin template\n"
       "- Nội dung template hiển thị và lưu đúng ở cả app lẫn web\n"
       "- Friend nhận đúng 1 tin",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r179 (TC-SC-179, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "SYNC-APP-001", "Boundary",
       "App mobile admin — double-click gửi media chỉ ra 1 tin, không tải lên 2 file",
       "- Đăng nhập app mobile admin, mở hội thoại X, có ảnh trong máy",
       "1. Chọn ảnh\n"
       "2. Bấm gửi 2 lần liên tiếp thật nhanh\n"
       "3. Kéo refresh trên app và đối chiếu trên web",
       "1 file ảnh",
       "- Tăng ĐÚNG 1 tin media\n"
       "- Chỉ 1 file được tải lên, không có 2 bản trùng\n"
       "- Friend nhận đúng 1 tin",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r180 (TC-SC-180, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "SYNC-APP-001", "Abnormal",
       "App mobile admin — mất mạng giữa lúc gửi rồi gửi lại, friend chỉ nhận 1 tin",
       "- Đăng nhập app mobile admin, mở hội thoại X",
       "1. Bật chế độ máy bay ngay sau khi bấm gửi\n"
       "2. Khôi phục mạng\n"
       "3. Bấm gửi lại (hoặc để app tự thử lại)\n"
       "4. Đối chiếu hội thoại trên app, trên web và phía LINE của friend",
       "アプリ送信テスト",
       "- Friend nhận ĐÚNG 1 tin\n"
       "- Không có tin trùng trên app và web\n"
       "- Nếu lần đầu thất bại thật thì chỉ có tin của lần thử lại",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r181 (TC-SC-181, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "SYNC-APP-001", "Abnormal",
       "Web và app cùng gửi 1 hội thoại trong thời gian chặn — chỉ 1 bên gửi được",
       "- Tab 8 = ON, số phút = 5\n"
       "- Staff A dùng web, Staff B dùng app mobile admin, cùng mở hội thoại X",
       "1. Staff A gửi tin từ web (thời điểm T)\n"
       "2. Trong vòng 5 phút, Staff B bấm gửi trên app\n"
       "3. Quan sát màn hình app của Staff B và hội thoại X",
       "—",
       "- Staff B KHÔNG gửi được; app hiển thị thông báo chặn tương ứng\n"
       "- Hội thoại X chỉ có tin của Staff A\n"
       "- Staff A vẫn gửi tiếp được trong cửa sổ chặn",
       env="PRODUCTION",
       note=NOSPEC + "BR-08B-02 áp cho CẢ web lẫn app mobile. ⚠️ Chuỗi thông báo phía app chưa có "
            "spec mobile để đối chiếu. Nguồn: v2 r182 (TC-SC-182, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "DATA-DB-001", "Boundary",
       "短縮URL BẬT + gửi từ app — link rút gọn đúng và chỉ sinh 1 mã",
       "- Tab 5「短縮URLの利用」= BẬT\n"
       "- Đăng nhập app mobile admin, mở hội thoại X",
       "1. Soạn tin chứa URL dài, bấm gửi 2 lần thật nhanh\n"
       "2. Đối chiếu tin trên web và phía LINE của friend\n"
       "3. Kiểm tra bản ghi link rút gọn ở màn URL分析",
       "https://example.com/very/long/path",
       "- Tin gửi đi chứa URL rút gọn dạng `https://s.lmes.jp/l/xxxxxxxx`\n"
       "- Chỉ 1 tin được gửi và chỉ 1 bản ghi link rút gọn được tạo\n"
       "- Link rút gọn mở đúng URL gốc",
       env="PRODUCTION",
       note=NOSPEC + "BR-06-02 rút gọn ở phía server ⇒ áp cả app. Nguồn: v2 r183 (TC-SC-183, Not Tested)"),

    tc("Chống gửi trùng — chặn gửi thực tế", "REG-SHARED-001", "Normal",
       "Rà đủ 6 đường gửi có dùng khóa chống gửi trùng",
       "- Có bản đồ ảnh hưởng của Dev liệt kê 6 nơi gọi khóa gửi",
       "1. Lập bảng 6 đường gửi: web text · web template/media · web (đường thứ 3) ·\n"
       "   app text · app template · app media\n"
       "2. Gắn TC tương ứng cho từng đường và ghi kết quả chạy\n"
       "3. Ghi rõ các mục nằm ngoài phạm vi đã bàn giao sang task nào",
       "—",
       "- Cả 6 đường gửi đều có TC tương ứng và đã chạy\n"
       "- Các mục ngoài phạm vi được ghi rõ đã bàn giao, KHÔNG bỏ sót âm thầm\n"
       "- Kết quả rà soát lưu kèm bản đồ ảnh hưởng",
       note=NOSPEC + "REG-SHARED-001 yêu cầu danh sách nơi ảnh hưởng do Dev cung cấp + kết quả test "
            "từng nơi. Nguồn: v2 r193 (TC-SC-193, Not Tested)"),
]
