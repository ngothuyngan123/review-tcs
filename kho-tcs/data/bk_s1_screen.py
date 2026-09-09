# -*- coding: utf-8 -*-
"""FA-033 データコピー — Nhóm 1-8: màn hình, mã copy, xác nhận, modal, processing,
lịch sử, phân quyền & plan.

⚠️ Toàn bộ nhóm này phụ thuộc MT-00 (spec tả UI cũ 1 màn / corpus tả UI mới 7 màn)
và MT-01 (chiều copy). Quy ước dùng trong file: **bot A = bot đang đăng nhập (bên thao tác)**,
**bot B = bot còn lại**. Chiều dữ liệu A→B viết theo spec; nếu Leader chốt MT-01 ngược lại
thì đảo vai A/B ở phần điều kiện tiền đề.
"""
from _common import tc

A = ("- Đăng nhập Admin của bot A (plan Standard hoặc Pro)\n"
     "- Vào Sidebar →「システム管理関連」→「データコピー」(/basic/backup)")
AB = (A + "\n- Có bot B là LOA khác trong hệ thống, biết mã copy của bot B\n"
      "- Không có bản ghi lịch sử nào đang ở trạng thái「処理中」")
MT00 = "⚠️ Phụ thuộc MT-00 — nếu bản UI cũ đang chạy production thì TC này chưa áp dụng. "
MT01 = "⚠️ Phụ thuộc MT-01 — chiều copy (ai là nguồn / ai là đích) chưa chốt. "

S1 = [
    # ═══════════════ 1. Màn データコピー & danh sách dữ liệu ═══════════════
    tc("Màn データコピー & danh sách dữ liệu", "UI-001", "Normal",
       "Vào màn データコピー — hiển thị đủ tiêu đề, mô tả, danh sách dữ liệu, form nhập mã, bảng lịch sử",
       A,
       "1. Đăng nhập Admin bot A\n"
       "2. Mở Sidebar, tìm nhóm「システム管理関連」\n"
       "3. Bấm mục「データコピー」\n"
       "4. Quan sát toàn bộ nội dung trang",
       "Bot A plan Pro",
       "- Trang /basic/backup tải xong, không có alert, không bị đá về màn khác\n"
       "- Có tiêu đề「データコピー」+ mô tả「このアカウントに設定されているデータを他のエルメにコピーすることが出来ます。」\n"
       "- Có khối「コピーされるデータ」liệt kê các loại dữ liệu\n"
       "- Có khối nhập mã và bảng lịch sử copy\n"
       "- Console trình duyệt không có lỗi JavaScript",
       note="Nguồn: [AI]UI TCs r27 (TC-BK-026) + ui-spec.md §3.2. Evidence: ảnh full trang."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-002", "Normal",
       "Khối「コピーされるデータ」liệt kê ĐỦ số loại dữ liệu — đối chiếu với danh sách chốt",
       A,
       "1. Vào màn データコピー\n"
       "2. Đếm số dòng trong khối「コピーされるデータ」\n"
       "3. Đối chiếu từng dòng với danh sách trong feature-spec §1.3",
       "Đếm tay, chụp ảnh cả khối",
       "- Số dòng đúng bằng con số Leader chốt ở MT-04 (13 hoặc 15)\n"
       "- Nếu chốt 15 thì phải có thêm「クロス分析」và「CSV管理」\n"
       "- Thứ tự và tên tiếng Nhật khớp với spec",
       spec="Đã hỏi leader",
       note="MT-04 — [AI]UI r27 nói 15 loại, feature-spec §1.3 + ui-spec Block 2 nói 13 loại. "
            "Evidence: ảnh khối コピーされるデータ."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-002", "Normal",
       "Hiển thị câu chú ý「上記以外のデータはコピーされませんので、手動での設定をお願い致します。」",
       A,
       "1. Vào màn データコピー\n"
       "2. Đọc dòng chú ý ngay dưới khối「コピーされるデータ」",
       "—",
       "- Câu chú ý hiển thị đầy đủ, không bị cắt\n"
       "- Nội dung nói rõ dữ liệu ngoài danh sách sẽ không được copy và phải cài đặt thủ công",
       note="Nguồn: ui-spec.md Block 2. Liên quan MT-28 (danh sách dữ liệu không copy chưa đủ)."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-002", "Normal",
       "Cảnh báo nền vàng — nội dung khoá thao tác và mốc thời gian",
       A,
       "1. Vào màn データコピー, tab「コピー登録」\n"
       "2. Đọc toàn văn khối cảnh báo nền vàng\n"
       "3. Thử tìm nút X để đóng cảnh báo",
       "—",
       "- Cảnh báo nền vàng nhạt hiển thị trong tab「コピー登録」\n"
       "- Nội dung nêu rõ phía nào bị khoá thao tác và trong bao lâu (theo quyết định MT-08)\n"
       "- Cảnh báo LUÔN hiển thị — không có nút đóng",
       spec="Đã hỏi leader",
       note="MT-08 — [AI]UI r32 (TC-BK-031) nói khoá CẢ 2 phía tối đa ~1 giờ; "
            "feature-spec §8.2 nói CHỈ khoá LOA đích và không có mốc thời gian. Evidence: ảnh khối cảnh báo."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-001", "Normal",
       "Chuyển qua lại 2 tab「コピー登録」↔「コピー履歴」",
       A,
       "1. Xác nhận tab「コピー登録」đang active mặc định\n"
       "2. Bấm tab「コピー履歴」\n"
       "3. Bấm lại tab「コピー登録」",
       "—",
       "- Bước 2: tab「コピー履歴」sáng lên, bảng lịch sử hiển thị, tab「コピー登録」mờ đi\n"
       "- Bước 3: quay lại form nhập mã, nội dung đã nhập trước đó không gây lỗi\n"
       "- Không reload toàn trang khi đổi tab",
       note=MT00 + "Nguồn: [AI]UI r30 (TC-BK-029)."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-003", "Normal",
       "Nút「コピー内容の確認に進む」ở trạng thái mờ khi chưa xác nhận mã",
       A,
       "1. Vào màn データコピー, chưa nhập gì\n"
       "2. Quan sát nút「コピー内容の確認に進む」\n"
       "3. Gõ một mã bất kỳ vào ô nhập nhưng CHƯA bấm「コードを確認」\n"
       "4. Bấm thử nút「コピー内容の確認に進む」",
       "Mã gõ vào: bất kỳ, ví dụ ABC123",
       "- Bước 2: nút màu xám, không bấm được\n"
       "- Bước 3: nút VẪN màu xám dù ô nhập đã có nội dung\n"
       "- Bước 4: bấm không có phản hồi, không mở modal, không chuyển màn\n"
       "- Nút chỉ sáng lên sau khi xác nhận mã thành công",
       note=MT00 + "Nguồn: [AI]UI r13 (TC-BK-012)."),

    tc("Màn データコピー & danh sách dữ liệu", "UI-004", "Normal",
       "Hiển thị màn データコピー ở độ phân giải nhỏ — không vỡ layout",
       A,
       "1. Đặt cửa sổ trình duyệt về 1366×768\n"
       "2. Vào màn データコピー, cuộn hết trang\n"
       "3. Đổi sang 1920×1080 và quan sát lại",
       "1366×768 và 1920×1080",
       "- Không tràn ngang, không có thanh cuộn ngang\n"
       "- Bảng lịch sử co giãn hoặc có vùng cuộn riêng, không đè lên khối khác\n"
       "- Chữ tiếng Nhật không bị cắt giữa dòng",
       note="Suy luận của AI theo UI-004 — corpus không có TC responsive cho màn này. Cần Leader xác nhận."),

    # ═══════════════ 2. Mã copy & phát hành lại ═══════════════
    tc("Mã copy & phát hành lại", "UI-FIELD-001", "Normal",
       "Khối「このアカウントのコピーコード」hiển thị đúng mã copy của bot đang đăng nhập",
       A,
       "1. Vào màn データコピー\n"
       "2. Đọc mã ở khối「このアカウントのコピーコード」\n"
       "3. Thử gõ đè lên mã đó",
       "—",
       "- Mã hiển thị là chuỗi chữ + số (ví dụ WA7L9TsEC7)\n"
       "- Mã ở dạng chỉ đọc — không gõ đè được\n"
       "- Bên cạnh mã có icon sao chép",
       note=MT00 + "Nguồn: [AI]UI r12 (TC-BK-011). Verify bổ sung: mã khớp `bots.transfer_code` của bot A."),

    tc("Mã copy & phát hành lại", "DATA-ID-001", "Boundary",
       "Độ dài và tập ký tự của mã copy — đo trên mã thực tế",
       A,
       "1. Vào màn データコピー\n"
       "2. Sao chép mã ở khối「このアカウントのコピーコード」ra notepad\n"
       "3. Đếm số ký tự, ghi nhận có chữ hoa / chữ thường / số / ký tự khác\n"
       "4. Lặp lại với mã của 3 bot khác nhau",
       "4 bot khác nhau (dev + staging)",
       "- Cả 4 mã đều có ĐÚNG độ dài mà Leader chốt ở MT-05\n"
       "- Chỉ gồm chữ cái và chữ số, không có khoảng trắng, không có ký tự đặc biệt\n"
       "- Ghi lại có phân biệt hoa/thường hay không",
       spec="Đã hỏi leader",
       note="MT-05 — corpus nói 10 ký tự ([AI]API r18/r28), 10~16 ([AI]UI r3), spec BR-01 nói varchar(16). "
            "Evidence: ảnh 4 mã đã sao chép."),

    tc("Mã copy & phát hành lại", "UI-001", "Normal",
       "Bấm icon sao chép mã — mã vào clipboard và có phản hồi trên UI",
       A,
       "1. Vào màn データコピー\n"
       "2. Ghi lại mã đang hiển thị\n"
       "3. Bấm icon sao chép bên cạnh mã\n"
       "4. Dán (Ctrl+V) vào một ô nhập bất kỳ",
       "—",
       "- Bước 3: có phản hồi thấy được — đổi màu icon, tooltip「コピーしました」hoặc icon dấu tích\n"
       "- Bước 4: nội dung dán ra đúng bằng mã đã ghi ở bước 2",
       note=MT00 + "Nguồn: [AI]UI r31 (TC-BK-030) + r46 (Comment 7). "
            "Clipboard khó tự động hoá — chạy tay trên Chrome và Edge."),

    tc("Mã copy & phát hành lại", "UI-002", "Normal",
       "Mở modal「コピーコードの再発行」— nội dung cảnh báo và 3 nút",
       AB,
       "1. Vào màn データコピー\n"
       "2. Bấm nút「コピーコードの再発行」\n"
       "3. Đọc toàn bộ nội dung modal",
       "—",
       "- Modal mở với tiêu đề「コピーコードの再発行」\n"
       "- Có cảnh báo「コピーコードを再発行すると既存のコードが利用できなくなりますのでご注意ください。」\n"
       "- Có nút X ở góc trên phải, nút「キャンセル」và nút「再発行する」",
       note=MT00 + "Nguồn: [AI]UI r3 (TC-BK-002) bước 2. Evidence: ảnh modal."),

    tc("Mã copy & phát hành lại", "FUNC-001", "Normal",
       "Bấm「再発行する」— mã copy đổi thành mã mới ngay trên màn",
       AB,
       "1. Ghi lại mã hiện tại ở khối「このアカウントのコピーコード」\n"
       "2. Bấm「コピーコードの再発行」\n"
       "3. Trong modal, bấm「再発行する」\n"
       "4. Đọc lại mã trên màn",
       "Mã cũ ghi ở bước 1",
       "- Modal đóng lại\n"
       "- Mã ở khối「このアカウントのコピーコード」đổi thành chuỗi chữ+số KHÁC mã đã ghi ở bước 1\n"
       "- Mã mới đúng độ dài đã chốt ở MT-05\n"
       "- Verify bổ sung: `bots.transfer_code` của bot A bằng đúng mã mới hiển thị",
       note=MT00 + "Nguồn: [AI]UI r3 (TC-BK-002), [AI]API r18 (TC-BK-050), r28 (TC-BK-060)."),

    tc("Mã copy & phát hành lại", "FUNC-001", "Normal",
       "Bấm「キャンセル」hoặc X trong modal 再発行 — mã KHÔNG đổi",
       AB,
       "1. Ghi lại mã hiện tại\n"
       "2. Bấm「コピーコードの再発行」→ modal mở\n"
       "3. Bấm「キャンセル」\n"
       "4. Mở lại modal, lần này bấm nút X",
       "Mã cũ ghi ở bước 1",
       "- Cả 2 lần modal đều đóng\n"
       "- Mã trên màn vẫn đúng bằng mã đã ghi ở bước 1\n"
       "- Verify bổ sung: `bots.transfer_code` không đổi",
       note="Suy luận của AI theo cặp đối xứng với TC bấm 再発行する — corpus không có TC cho nhánh hủy. "
            "Cần Leader xác nhận."),

    tc("Mã copy & phát hành lại", "STATE-001", "Abnormal",
       "Mã CŨ trở nên vô hiệu ngay sau khi phát hành lại",
       AB + "\n- Đã ghi lại mã cũ của bot A trước khi phát hành lại",
       "1. Ở bot A, phát hành lại mã (mã cũ → mã mới)\n"
       "2. Đăng nhập bot B (LOA khác), vào màn データコピー\n"
       "3. Nhập MÃ CŨ của bot A vào ô nhập mã\n"
       "4. Bấm「コードを確認」",
       "Mã cũ của bot A",
       "- Hiển thị thông báo「バックアップコードが存在しません。」\n"
       "- KHÔNG hiển thị card thông tin tài khoản nào\n"
       "- Nút đi tiếp vẫn ở trạng thái mờ",
       note=MT00 + "Nguồn: [AI]UI r14 (TC-BK-013) + r36 (TC-BK-035); [AI]API r23 (TC-BK-055)."),

    tc("Mã copy & phát hành lại", "CONC-001", "Abnormal",
       "Phát hành lại mã trong khi ĐANG có backup xử lý — bị chặn, mã giữ nguyên",
       A + "\n- Đang có 1 bản ghi ở tab「コピー履歴」hiển thị trạng thái「処理中」",
       "1. Vào tab「コピー履歴」, xác nhận có dòng đang「処理中」\n"
       "2. Quay lại tab「コピー登録」, ghi lại mã hiện tại\n"
       "3. Bấm「コピーコードの再発行」→ bấm「再発行する」",
       "—",
       "- Hiển thị thông báo lỗi「バックアップ処理中のため、コードの再発行はできません。」\n"
       "- Mã ở khối「このアカウントのコピーコード」KHÔNG đổi\n"
       "- Verify bổ sung: `bots.transfer_code` giữ nguyên",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r7 (TC-BK-006); [AI]API r20 (TC-BK-052). "
            "PRODUCTION theo RULE-08 vì phụ thuộc job nền đang chạy."),

    tc("Mã copy & phát hành lại", "FUNC-UNIQ-001", "Boundary",
       "Phát hành lại 5 lần liên tiếp — 5 mã khác nhau, không trùng mã của bot khác",
       AB,
       "1. Phát hành lại mã, ghi lại mã lần 1\n"
       "2. Lặp lại thao tác 4 lần nữa, mỗi lần ghi lại mã\n"
       "3. So sánh 5 mã với nhau\n"
       "4. Thử nhập từng mã trong 5 mã đó ở một bot khác để xem có trỏ về bot nào lạ không",
       "5 lần phát hành liên tiếp",
       "- 5 mã đều khác nhau đôi một\n"
       "- Chỉ mã cuối cùng còn xác nhận được, 4 mã trước đều báo「バックアップコードが存在しません。」\n"
       "- Không có mã nào trỏ về một LOA khác (không đụng mã của bot khác)",
       note=MT00 + "Nguồn: [AI]API r19 (TC-BK-051) — logic Str::random + retry nếu trùng."),

    tc("Mã copy & phát hành lại", "SEC-001", "Abnormal",
       "Gọi thẳng chức năng phát hành lại mã khi chưa đăng nhập",
       "- Trình duyệt ở trạng thái chưa đăng nhập (hoặc phiên đã hết hạn)",
       "1. Đăng xuất khỏi tool\n"
       "2. Gửi thẳng request POST /ajax/reissue-transfer-code (dùng Postman hoặc DevTools)\n"
       "3. Kiểm tra phản hồi\n"
       "4. Đăng nhập lại bot A và xem mã copy",
       "Không gửi cookie phiên",
       "- Hệ thống trả về chuyển hướng về trang đăng nhập hoặc mã lỗi 401\n"
       "- Không trả về mã mới\n"
       "- Bước 4: mã copy của bot A vẫn nguyên như trước",
       note=MT00 + "Nguồn: [AI]API r21 (TC-BK-053). Cần Postman — không tự động hoá qua UI."),

    # ═══════════════ 3. Xác nhận mã & card tài khoản ═══════════════
    tc("Xác nhận mã & card tài khoản", "FUNC-001", "Normal",
       "Nhập mã hợp lệ của LOA khác → hiện card thông tin tài khoản, nút đi tiếp sáng lên",
       AB,
       "1. Vào tab「コピー登録」\n"
       "2. Nhập mã copy của bot B vào ô nhập mã\n"
       "3. Bấm「コードを確認」\n"
       "4. Quan sát khu vực bên dưới ô nhập",
       "Mã hợp lệ của bot B",
       "- Ô nhập được thay bằng card thông tin tài khoản, hiển thị đúng TÊN của bot B\n"
       "- Nút「コピー内容の確認に進む」chuyển sang màu xanh, bấm được\n"
       "- Xuất hiện nút「リセット」",
       note=MT00 + MT01 + "Nguồn: [AI]UI r2 (TC-BK-001) bước 4-5; [AI]API r10 (TC-BK-042)."),

    tc("Xác nhận mã & card tài khoản", "FUNC-001", "Abnormal",
       "Nhập mã không tồn tại trong hệ thống",
       A,
       "1. Vào tab「コピー登録」\n"
       "2. Nhập chuỗi không phải mã của LOA nào, ví dụ INVALID123X\n"
       "3. Bấm「コードを確認」",
       "INVALID123X",
       "- Hiển thị thông báo「バックアップコードが存在しません。」\n"
       "- KHÔNG hiện card thông tin tài khoản\n"
       "- Nút「コピー内容の確認に進む」vẫn mờ\n"
       "- Ô nhập giữ nguyên nội dung đã gõ",
       note=MT00 + "Nguồn: [AI]UI r4 (TC-BK-003); [AI]API r11 (TC-BK-043)."),

    tc("Xác nhận mã & card tài khoản", "FUNC-001", "Abnormal",
       "Nhập chính mã copy của bot đang đăng nhập — bị từ chối",
       A,
       "1. Sao chép mã ở khối「このアカウントのコピーコード」của bot A\n"
       "2. Dán vào ô nhập mã\n"
       "3. Bấm「コードを確認」",
       "Mã của chính bot A",
       "- Hiển thị「現在のアカウントのデータ受信コードは入力できません。別のアカウントのコードを入力してください。」\n"
       "- KHÔNG hiện card thông tin tài khoản\n"
       "- Nút「コピー内容の確認に進む」vẫn mờ",
       note=MT00 + "Nguồn: [AI]UI r5 (TC-BK-004); [AI]API r12 (TC-BK-044); Backup 1.0 r310-r311 "
            "(task 2/2/2026「Validate backup không backup chính bot đó」)."),

    tc("Xác nhận mã & card tài khoản", "UI-INPUT-001", "Abnormal",
       "Bấm「コードを確認」khi ô nhập mã để trống",
       A,
       "1. Vào tab「コピー登録」, để ô nhập mã trống hoàn toàn\n"
       "2. Bấm「コードを確認」",
       "Chuỗi rỗng",
       "- Hiển thị thông báo yêu cầu nhập (「が必要です。」hoặc thông báo tương đương)\n"
       "- KHÔNG hiện card thông tin tài khoản\n"
       "- Nút「コピー内容の確認に進む」vẫn mờ",
       note=MT00 + "Nguồn: [AI]UI r22 (TC-BK-021)."),

    tc("Xác nhận mã & card tài khoản", "UI-INPUT-001", "Abnormal",
       "Nhập mã hợp lệ có kèm khoảng trắng ở đầu và cuối",
       AB,
       "1. Nhập mã của bot B kèm 1 khoảng trắng ở đầu và 1 ở cuối\n"
       "2. Bấm「コードを確認」\n"
       "3. Lặp lại chỉ với khoảng trắng ở cuối\n"
       "4. Lặp lại chỉ với khoảng trắng ở đầu",
       "\" <mã bot B> \" · \"<mã bot B> \" · \" <mã bot B>\"",
       "- Cả 3 lần cho CÙNG một kết quả, đúng theo quyết định MT-09:\n"
       "  · nếu chốt CÓ trim: hiện card thông tin bot B như nhập mã sạch\n"
       "  · nếu chốt KHÔNG trim: báo「バックアップコードが存在しません。」",
       spec="Đã hỏi leader",
       note="MT-09 — [AI]UI r23 (TC-BK-022) viết 2 nhánh, ghi chú cuối ô là「Tự trim space」, Test Result = OK."),

    tc("Xác nhận mã & card tài khoản", "UI-INPUT-001", "Boundary",
       "Nhập mã dài hơn giới hạn cho phép",
       A,
       "1. Gõ chuỗi 17 ký tự vào ô nhập mã (ví dụ ABCDEFGHIJKLMNOPQ)\n"
       "2. Đếm số ký tự thực sự vào được ô nhập\n"
       "3. Bấm「コードを確認」\n"
       "4. Lặp lại với chuỗi 30 ký tự",
       "17 ký tự và 30 ký tự",
       "- Nếu ô nhập có giới hạn: chỉ gõ được đúng số ký tự Leader chốt ở MT-05, ký tự thừa bị chặn\n"
       "- Nếu không có giới hạn: bấm xác nhận báo「バックアップコードが存在しません。」\n"
       "- Không có lỗi 500, không treo trang",
       spec="Đã hỏi leader",
       note="MT-05 — [AI]UI r24 (TC-BK-023). Evidence: quay màn hình lúc gõ."),

    tc("Xác nhận mã & card tài khoản", "UI-INPUT-001", "Abnormal",
       "Nhập mã chứa ký tự đặc biệt, tiếng Nhật hoặc emoji",
       A,
       "1. Nhập lần lượt các chuỗi ở cột dữ liệu vào ô nhập mã\n"
       "2. Mỗi lần bấm「コードを確認」và ghi lại kết quả",
       "① <script>alert(1)</script>\n② コピーコード\n③ ABC🤖123\n④ ' OR '1'='1\n⑤ ＡＢＣ１２３ (full-width)",
       "- Cả 5 lần đều báo「バックアップコードが存在しません。」hoặc thông báo lỗi nhập liệu\n"
       "- KHÔNG có script chạy, không có alert lạ, không lỗi 500\n"
       "- Không hiện card thông tin tài khoản nào",
       note="Gộp 5 input vì CÙNG 1 kết quả mong đợi. Suy luận của AI theo SEC-001 + DI-* — "
            "corpus không có TC ký tự đặc biệt cho ô mã. Cần Leader xác nhận."),

    tc("Xác nhận mã & card tài khoản", "STATE-CLEAN-001", "Normal",
       "Bấm「リセット」sau khi đã xác nhận mã — quay về trạng thái nhập mã",
       AB + "\n- Đã xác nhận mã bot B thành công, card thông tin đang hiển thị",
       "1. Xác nhận card thông tin bot B đang hiển thị và nút đi tiếp đang sáng\n"
       "2. Bấm nút「リセット」",
       "—",
       "- Card thông tin biến mất ngay, không có hộp thoại xác nhận\n"
       "- Ô nhập mã hiện lại và ở trạng thái trống\n"
       "- Nút「コードを確認」hiện lại, nút「リセット」ẩn đi\n"
       "- Nút「コピー内容の確認に進む」trở lại màu xám",
       note=MT00 + "Nguồn: [AI]UI r8 (TC-BK-007). Ô Note gốc ghi「confirm lại câu in đỏ」— "
            "cần Leader xác nhận có câu cảnh báo đỏ nào kèm theo không."),

    tc("Xác nhận mã & card tài khoản", "UI-003", "Normal",
       "Ô nhập mã bị khoá sau khi xác nhận thành công",
       AB,
       "1. Nhập mã bot B, bấm「コードを確認」\n"
       "2. Thử gõ thêm ký tự vào ô nhập mã",
       "Mã bot B",
       "- Sau khi xác nhận, ô nhập mã bị vô hiệu hoá — không gõ thêm hay sửa được\n"
       "- Muốn nhập mã khác phải bấm「リセット」trước",
       note=MT00 + "Nguồn: [AI]UI r45 (Comment 7 —「disable text box」, Test Result = OK)."),

    tc("Xác nhận mã & card tài khoản", "CONC-001", "Abnormal",
       "Mã của LOA kia bị đổi SAU KHI đã xác nhận nhưng TRƯỚC KHI bắt đầu copy",
       AB,
       "1. Ở bot A, nhập mã bot B và bấm「コードを確認」→ card bot B hiện ra\n"
       "2. GIỮ NGUYÊN màn hình bot A\n"
       "3. Mở tab khác, đăng nhập bot B, phát hành lại mã copy của bot B\n"
       "4. Quay lại tab bot A, bấm「コピー内容の確認に進む」rồi bấm「データコピーを開始」",
       "Mã bot B cũ đã bị thay ở bước 3",
       "- Hệ thống kiểm tra lại mã ở tầng máy chủ và báo lỗi mã không tồn tại\n"
       "- KHÔNG tạo bản ghi mới ở tab「コピー履歴」\n"
       "- Không có job copy nào chạy",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r35 (TC-BK-034) —「Validate cả modal confirm backup, hiển thị msg tương ứng」. "
            "TC gốc KHÔNG ghi rõ msg là gì; kết quả mong đợi trên do AI viết, cần Leader xác nhận."),

    tc("Xác nhận mã & card tài khoản", "INTG-HOOK-001", "Normal",
       "Chức năng xác nhận mã luôn trả về HTTP 200 kể cả khi mã sai",
       A,
       "1. Mở DevTools tab Network\n"
       "2. Nhập mã không tồn tại → bấm「コードを確認」→ ghi lại HTTP status\n"
       "3. Nhập mã của chính bot A → bấm「コードを確認」→ ghi lại HTTP status\n"
       "4. Nhập mã hợp lệ của bot B → ghi lại HTTP status",
       "3 loại mã: không tồn tại · của chính mình · hợp lệ",
       "- Cả 3 lần request /ajax/check-transfer-code đều trả HTTP 200\n"
       "- Phân biệt đúng/sai qua trường `success` trong nội dung phản hồi, không qua HTTP status\n"
       "- Không có lần nào trả 4xx hay 5xx",
       note="Nguồn: [AI]API r13 (TC-BK-045) —「quan trọng: không được thay đổi HTTP status」. "
            "Đây là TC hồi quy, giữ nguyên từ bản FA-033."),

    # ═══════════════ 4. Modal xác nhận & bắt đầu copy ═══════════════
    tc("Modal xác nhận & bắt đầu copy", "UI-002", "Normal",
       "Mở modal「コピー開始」— hiển thị 2 card tài khoản và khối cảnh báo đỏ",
       AB + "\n- Đã xác nhận mã bot B thành công",
       "1. Bấm「コピー内容の確認に進む」\n"
       "2. Đọc toàn bộ nội dung modal, đếm số dòng trong khối「注意事項」",
       "—",
       "- Modal mở, hiển thị 2 card tài khoản (bên gửi và bên nhận), mỗi card có tên LOA\n"
       "- Khối「注意事項」hiển thị màu đỏ, ĐỦ 3 dòng, không bị cắt\n"
       "- Có nút X góc trên phải, nút「戻る」và nút「データコピーを開始」",
       spec="Đã hỏi leader",
       note="MT-08 — [AI]UI r33 (TC-BK-032). TC gốc chỉ mô tả 2 dòng đầu (downtime, automation vẫn chạy) "
            "và ghi「và nội dung thứ 3」mà không nói là gì. Evidence: ảnh modal."),

    tc("Modal xác nhận & bắt đầu copy", "STATE-001", "Normal",
       "Đóng modal bằng nút X — giữ nguyên trạng thái đã xác nhận mã",
       AB + "\n- Modal「コピー開始」đang mở",
       "1. Bấm nút X ở góc trên phải modal\n"
       "2. Quan sát màn phía sau\n"
       "3. Bấm lại「コピー内容の確認に進む」",
       "—",
       "- Modal đóng, quay về màn có card thông tin LOA kia vẫn hiển thị\n"
       "- Nút「コピー内容の確認に進む」vẫn sáng\n"
       "- Bước 3: modal mở lại được với nội dung y như cũ",
       note=MT00 + "Nguồn: [AI]UI r10 (TC-BK-009)."),

    tc("Modal xác nhận & bắt đầu copy", "STATE-001", "Normal",
       "Bấm「戻る」trong modal — giữ nguyên trạng thái đã xác nhận mã",
       AB + "\n- Modal「コピー開始」đang mở",
       "1. Bấm nút「戻る」trong modal\n"
       "2. Quan sát màn phía sau\n"
       "3. Bấm lại「コピー内容の確認に進む」",
       "—",
       "- Modal đóng, card thông tin LOA kia còn nguyên\n"
       "- Trạng thái form không đổi, nút đi tiếp vẫn sáng\n"
       "- Bước 3: mở lại được modal",
       note=MT00 + "Nguồn: [AI]UI r11 (TC-BK-010)."),

    tc("Modal xác nhận & bắt đầu copy", "FUNC-SEQ-001", "Normal",
       "Bấm「データコピーを開始」— chuyển sang màn xử lý và sinh 1 dòng lịch sử mới",
       AB + "\n- Modal「コピー開始」đang mở\n- Ghi lại số dòng hiện có ở tab「コピー履歴」",
       "1. Trong modal, bấm「データコピーを開始」\n"
       "2. Quan sát màn hình chuyển sang\n"
       "3. Mở tab trình duyệt thứ 2, đăng nhập cùng bot A, vào tab「コピー履歴」\n"
       "4. Đếm số dòng và đọc dòng đầu tiên",
       "—",
       "- Bước 2: chuyển sang màn xử lý toàn trang (có logo, spinner, thanh tiến trình)\n"
       "- Bước 4: có thêm ĐÚNG 1 dòng so với trước, nằm ở đầu bảng\n"
       "- Dòng mới hiển thị trạng thái「処理中」, đúng mã đã nhập, đúng tên LOA kia, thời điểm là lúc bấm",
       env="PRODUCTION",
       note=MT00 + MT01 + "Nguồn: [AI]UI r2 (TC-BK-001) bước 8-9; [AI]API r27 (TC-BK-059). "
            "PRODUCTION vì có job nền tham gia (RULE-08)."),

    tc("Modal xác nhận & bắt đầu copy", "DATA-001", "Normal",
       "Dòng lịch sử ghi tên LOA là ẢNH CHỤP tại thời điểm bấm — LOA đổi tên sau không làm đổi lịch sử",
       AB,
       "1. Ghi lại tên hiện tại của bot B\n"
       "2. Từ bot A thực hiện copy sang bot B, chờ xong\n"
       "3. Đăng nhập bot B, đổi tên hiển thị của LOA thành tên khác\n"
       "4. Quay lại bot A, mở tab「コピー履歴」và đọc dòng vừa tạo",
       "Tên cũ: 「テストBOT-B」→ tên mới:「テストBOT-B-改名」",
       "- Cột tên tài khoản của dòng lịch sử VẪN hiển thị tên CŨ (テストBOT-B)\n"
       "- KHÔNG tự cập nhật theo tên mới\n"
       "- Verify bổ sung: `backup_history.line_account` giữ nguyên giá trị cũ",
       note="Nguồn: feature-spec BR-14 + [AI]API r27 (TC-BK-059). "
            "Corpus KHÔNG có TC cho tình huống đổi tên sau khi copy — TC này lấp gap, cần Leader xác nhận."),

    tc("Modal xác nhận & bắt đầu copy", "SEC-001", "Abnormal",
       "Xoá mã trong form bằng DevTools rồi bấm bắt đầu copy — máy chủ vẫn chặn",
       AB + "\n- Modal「コピー開始」đang mở",
       "1. Mở DevTools, tìm ô ẩn chứa mã copy trong form\n"
       "2. Xoá trắng giá trị ô ẩn đó\n"
       "3. Bấm「データコピーを開始」\n"
       "4. Vào tab「コピー履歴」đếm số dòng",
       "Ô ẩn transfer_code = rỗng",
       "- Hiển thị thông báo lỗi bắt buộc nhập (「が必要です。」hoặc tương đương)\n"
       "- Quay về màn trước, KHÔNG chuyển sang màn xử lý\n"
       "- Bước 4: số dòng lịch sử KHÔNG tăng",
       note=MT00 + "Nguồn: [AI]UI r6 (TC-BK-005); [AI]API r7 (TC-BK-039). Cần DevTools — chạy tay."),

    tc("Modal xác nhận & bắt đầu copy", "SEC-001", "Abnormal",
       "Sửa mã trong form thành mã KHÔNG tồn tại rồi bấm bắt đầu copy",
       AB + "\n- Modal「コピー開始」đang mở",
       "1. Mở DevTools, đổi giá trị ô ẩn chứa mã thành NOTEXIST999\n"
       "2. Bấm「データコピーを開始」\n"
       "3. Vào tab「コピー履歴」đếm số dòng",
       "NOTEXIST999",
       "- Hiển thị lỗi「バックアップコードが存在しません。」\n"
       "- Không chuyển sang màn xử lý\n"
       "- Số dòng lịch sử KHÔNG tăng, không có job nào chạy",
       note=MT00 + "Nguồn: [AI]API r8 (TC-BK-040) — validate `exists:bots` ở tầng máy chủ."),

    tc("Modal xác nhận & bắt đầu copy", "SEC-001", "Abnormal",
       "Gọi thẳng chức năng bắt đầu copy khi chưa đăng nhập",
       "- Trình duyệt ở trạng thái chưa đăng nhập",
       "1. Đăng xuất\n"
       "2. Gửi thẳng request POST /basic/backup/export-zip kèm một mã hợp lệ (Postman)\n"
       "3. Kiểm tra phản hồi\n"
       "4. Đăng nhập lại và mở tab「コピー履歴」",
       "Mã hợp lệ nhưng không có cookie phiên",
       "- Bị chuyển hướng về trang đăng nhập\n"
       "- Bước 4: KHÔNG có dòng lịch sử mới nào được tạo",
       note="Nguồn: [AI]API r9 (TC-BK-041). TC hồi quy phân quyền."),

    # ═══════════════ 5. Màn processing & polling ═══════════════
    tc("Màn processing & polling", "UI-001", "Normal",
       "Màn xử lý chiếm toàn trang — ẩn sidebar và header",
       AB + "\n- Vừa bấm「データコピーを開始」thành công",
       "1. Quan sát toàn bộ layout màn xử lý\n"
       "2. Tìm sidebar bên trái và header phía trên\n"
       "3. Liệt kê các thành phần nhìn thấy",
       "—",
       "- KHÔNG có sidebar bên trái\n"
       "- KHÔNG có header (tên tài khoản, thống kê 配信数)\n"
       "- Chỉ có: logo L Message, icon + tiêu đề「データコピー登録中」, spinner đang quay, thanh tiến trình, cảnh báo đỏ\n"
       "- Không có link nào dẫn ra màn khác",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r20 (TC-BK-019). Evidence: ảnh full màn."),

    tc("Màn processing & polling", "UI-003", "Normal",
       "Thanh tiến trình nhảy theo trạng thái xử lý",
       AB + "\n- Có quyền xem trạng thái backup ở phía máy chủ để đối chiếu",
       "1. Bấm「データコピーを開始」→ vào màn xử lý\n"
       "2. Ghi lại % ngay khi vừa vào\n"
       "3. Ghi lại % khi công việc được đưa vào hàng đợi\n"
       "4. Ghi lại % khi đang thực hiện copy\n"
       "5. Ghi lại % khi copy xong",
       "Quay màn hình toàn bộ quá trình",
       "- Bước 2: 0%\n"
       "- Bước 3: khoảng 10%\n"
       "- Bước 4: khoảng 33%\n"
       "- Bước 5: 100%\n"
       "- Thanh chỉ tăng, không bao giờ tụt ngược",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=MT00 + "Nguồn: [AI]UI r15 (TC-BK-014) — TC gốc ghi các mốc % là ƯỚC TÍNH theo giả định A-02, "
            "phụ thuộc QA-003 chưa có câu trả lời. Evidence: video quay màn."),

    tc("Màn processing & polling", "INTG-HOOK-001", "Normal",
       "Màn xử lý tự hỏi trạng thái theo chu kỳ, không cần bấm gì",
       AB + "\n- Đang ở màn xử lý",
       "1. Mở DevTools tab Network, lọc theo backup-status\n"
       "2. Đứng yên trên màn xử lý 60 giây, không thao tác gì\n"
       "3. Đếm số request và khoảng cách giữa các request",
       "Đứng yên 60 giây",
       "- Có request lặp lại đều đặn, khoảng cách khoảng 5 giây (≈12 request trong 60 giây)\n"
       "- Mỗi request trả HTTP 200\n"
       "- Nội dung phản hồi có trạng thái và thời điểm tạo\n"
       "- Trang KHÔNG bị reload toàn bộ giữa các lần hỏi",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]API r14 (TC-BK-046), r25 (TC-BK-057); [MN]Job r5 (TC-BK-065)."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Copy thất bại — màn xử lý chuyển sang trạng thái lỗi",
       AB + "\n- Có thể tạo được tình huống job gặp lỗi (nhờ Dev dựng)",
       "1. Bắt đầu copy, đứng ở màn xử lý\n"
       "2. Để job gặp lỗi (hoặc chờ tự nhiên nếu dữ liệu nguồn có bản ghi hỏng)\n"
       "3. Quan sát màn xử lý sau lần hỏi trạng thái kế tiếp",
       "—",
       "- Spinner / thanh tiến trình được thay bằng trạng thái lỗi\n"
       "- Hiển thị「データコピーに失敗しました。」\n"
       "- Có nút hoặc link để rời khỏi màn xử lý\n"
       "- Người dùng KHÔNG bị kẹt lại màn này",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-03 + [AI]UI r9 (TC-BK-008) — TC gốc ghi「hành vi UI cụ thể (modal hay inline) phụ thuộc QA-008 "
            "chưa resolved」. Cần Leader chốt hình thức hiển thị."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Tải lại trang (F5) khi đang ở màn xử lý",
       AB + "\n- Đang ở màn xử lý, job chưa xong",
       "1. Nhấn F5 để tải lại trang\n"
       "2. Quan sát màn hình sau khi tải xong",
       "—",
       "- Vẫn ở màn xử lý, thanh tiến trình tiếp tục từ trạng thái hiện tại\n"
       "- KHÔNG tạo thêm bản ghi lịch sử mới\n"
       "- KHÔNG khởi động lại quá trình copy",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Kết quả mong đợi do AI viết — corpus và spec đều KHÔNG có TC cho F5 ở màn xử lý. "
            "Cần Leader xác nhận."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Bấm nút Back của trình duyệt khi đang ở màn xử lý",
       AB + "\n- Đang ở màn xử lý, job chưa xong",
       "1. Bấm nút Back của trình duyệt\n"
       "2. Quan sát màn hình\n"
       "3. Bấm Forward để quay lại",
       "—",
       "- Không thoát được ra ngoài trong khi job chưa xong, hoặc nếu thoát được thì "
       "job vẫn chạy tiếp và quay lại vẫn thấy đúng tiến độ\n"
       "- Không tạo thêm bản ghi lịch sử",
       env="PRODUCTION",
       spec="Spec không ghi",
       note="Kết quả mong đợi do AI viết theo cùng nhóm với MT-27 — corpus không có TC. Cần Leader chốt cùng MT-27."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Gõ thẳng URL màn khác khi đang có backup chạy",
       AB + "\n- Đang có backup ở trạng thái xử lý",
       "1. Gõ thẳng URL /basic/chat-v3 vào thanh địa chỉ\n"
       "2. Quan sát kết quả\n"
       "3. Gõ lại URL /basic/backup",
       "/basic/chat-v3",
       "- Hoặc bị chặn và đưa về màn xử lý, hoặc vào được nhưng job vẫn chạy tiếp\n"
       "- Bước 3: quay lại /basic/backup thì thấy đúng trạng thái hiện tại của backup\n"
       "- Kết quả phải NHẤT QUÁN với quyết định MT-27",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-27 — corpus [AI]UI r41/r42 chỉ có tiêu đề, không có kết quả mong đợi."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Đăng xuất khi đang có backup chạy",
       AB + "\n- Đang có backup ở trạng thái xử lý",
       "1. Đang ở màn xử lý, mở menu tài khoản và bấm đăng xuất\n"
       "2. Đăng nhập lại bot A\n"
       "3. Vào màn データコピー và tab「コピー履歴」",
       "—",
       "- Job nền KHÔNG bị dừng khi người dùng đăng xuất\n"
       "- Sau khi đăng nhập lại, backup vẫn tiếp tục hoặc đã hoàn tất\n"
       "- Bảng lịch sử phản ánh đúng trạng thái, không có dòng bị kẹt vô thời hạn",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-27 — [AI]UI r41 (TC-BK-040) CHỈ có tiêu đề「Check khi bot đang backup > logout」, "
            "không có bước và không có kết quả mong đợi. Kết quả trên do AI viết."),

    tc("Màn processing & polling", "STATE-001", "Abnormal",
       "Đổi sang bot khác khi đang có backup chạy",
       AB + "\n- Đang có backup ở trạng thái xử lý\n- Tài khoản Admin quản lý nhiều bot",
       "1. Đang ở màn xử lý, dùng chức năng đổi bot trên header để chuyển sang bot C\n"
       "2. Quan sát màn hình\n"
       "3. Đổi ngược lại về bot A, vào màn データコピー",
       "Bot C là bot thứ 3, không liên quan copy",
       "- Job của bot A vẫn chạy tiếp, không bị hủy\n"
       "- Ở bot C, tab「コピー履歴」KHÔNG hiển thị dòng lịch sử của bot A\n"
       "- Bước 3: quay lại bot A thấy đúng trạng thái hiện tại",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-27 — [AI]UI r42 (TC-BK-041) CHỈ có tiêu đề「Check khi bot đang backup > đổi bot」. "
            "Kết quả trên do AI viết, đồng thời phủ thêm cách ly dữ liệu giữa bot (SEC-ISO-001)."),

    tc("Màn processing & polling", "SEC-ISO-001", "Abnormal",
       "Xem trạng thái backup của bot KHÁC — bị từ chối",
       "- Đăng nhập bot A\n- Biết mã định danh bản ghi backup thuộc bot C",
       "1. Lấy id bản ghi backup của bot C\n"
       "2. Đang đăng nhập bot A, gửi request GET /ajax/backup-status/<id của bot C>\n"
       "3. Kiểm tra phản hồi",
       "id backup thuộc bot C",
       "- Trả về mã lỗi 403 kèm thông báo Unauthorized\n"
       "- KHÔNG lộ trạng thái hay thời điểm backup của bot C",
       note="Nguồn: [AI]API r16 (TC-BK-048) + r26 (TC-BK-058). Cần Postman."),

    tc("Màn processing & polling", "FUNC-001", "Abnormal",
       "Xem trạng thái của bản ghi backup không tồn tại",
       A,
       "1. Gửi request GET /ajax/backup-status/99999 (id chắc chắn không có)\n"
       "2. Kiểm tra phản hồi",
       "id = 99999",
       "- Trả về mã lỗi 404 kèm thông báo Record not found\n"
       "- Không lỗi 500",
       note="Nguồn: [AI]API r15 (TC-BK-047). Cần Postman."),

    tc("Màn processing & polling", "SEC-001", "Abnormal",
       "Xem trạng thái backup khi chưa đăng nhập",
       "- Trình duyệt chưa đăng nhập",
       "1. Đăng xuất\n"
       "2. Gửi request GET /ajax/backup-status/1 không kèm cookie phiên\n"
       "3. Kiểm tra phản hồi",
       "Không có cookie phiên",
       "- Bị chuyển hướng về trang đăng nhập hoặc trả 401\n"
       "- KHÔNG trả về thông tin backup nào",
       note="Nguồn: [AI]API r17 (TC-BK-049). TC hồi quy phân quyền."),

    tc("Màn processing & polling", "FUNC-SEQ-001", "Normal",
       "Trình tự trạng thái ghi nhận được qua polling đúng thứ tự, không nhảy cóc",
       AB + "\n- Có công cụ ghi lại toàn bộ phản hồi polling",
       "1. Bắt đầu copy\n"
       "2. Ghi lại giá trị trạng thái ở MỌI lần polling cho tới khi kết thúc\n"
       "3. Xâu chuỗi thành 1 dãy và đối chiếu",
       "Ghi log toàn bộ phiên polling",
       "- Dãy trạng thái chỉ có thể là 0 → 4 → 1 → 2 (thành công) hoặc 0 → 4 → 1 → 3 (thất bại)\n"
       "- Không xuất hiện giá trị ngoài 0/1/2/3/4\n"
       "- Không có bước lùi (2→1, 3→4)\n"
       "- Không nhảy cóc (0→2, 4→2)",
       env="PRODUCTION",
       note="Nguồn: [AI]API r25 (TC-BK-057); [MN]Job r9 (TC-BK-076). "
            "Đây là TC chốt state machine — chạy chung với nhóm Job."),

    # ═══════════════ 6. Modal hoàn tất copy ═══════════════
    tc("Modal hoàn tất copy", "UI-002", "Normal",
       "Modal「データコピー完了」tự hiện khi copy xong, không cần bấm gì",
       AB + "\n- Đang đứng ở màn xử lý, job sắp hoàn tất",
       "1. Đứng yên ở màn xử lý, không thao tác\n"
       "2. Chờ tới khi copy hoàn tất\n"
       "3. Quan sát màn hình",
       "—",
       "- Modal「データコピー完了」tự động hiện ra, không cần bấm bất cứ đâu\n"
       "- Modal có 2 card tài khoản, nút「閉じる」ở dưới và nút X góc trên phải",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r19 (TC-BK-018), r2 (TC-BK-001) bước 11."),

    tc("Modal hoàn tất copy", "UI-002", "Normal",
       "Phân biệt màu nền 2 card trong modal hoàn tất",
       AB + "\n- Modal「データコピー完了」đang hiện",
       "1. Quan sát màu nền của card bên trên và card bên dưới\n"
       "2. Chụp ảnh cả modal",
       "—",
       "- Card LOA gửi có nền xám nhạt\n"
       "- Card LOA nhận có nền XANH LÁ nhạt (đánh dấu thành công)\n"
       "- 2 màu phân biệt rõ bằng mắt thường",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r19 (TC-BK-018). Evidence: ảnh modal."),

    tc("Modal hoàn tất copy", "OUT-TRUTH-001", "Normal",
       "Modal hoàn tất hiển thị TÊN và LINE ID của LOA NHẬN, không phải LOA gửi",
       AB + "\n- Bot A và bot B có TÊN và LINE ID khác hẳn nhau (dễ phân biệt)",
       "1. Ghi lại tên + LINE ID của cả bot A và bot B trước khi copy\n"
       "2. Thực hiện copy A → B, chờ modal hoàn tất hiện\n"
       "3. Đọc tên và LINE ID hiển thị trên modal\n"
       "4. Đối chiếu với 2 giá trị đã ghi",
       "Bot A: 「テストBOT-A」/ @aaa1111\nBot B:「テストBOT-B」/ @bbb2222",
       "- Modal hiển thị TÊN + LINE ID của bot B (bên NHẬN)\n"
       "- KHÔNG hiển thị thông tin của bot A",
       env="PRODUCTION",
       note="Bug tự detect #38411 (7/2026) — Backup 1.0 r315-r316. Nguyên nhân gốc:「hiện tại đang hiển thị "
            "thông tin bot nguồn」. Nhánh sửa: hot-fix-release/modal-backup-info. Đây là TC hồi quy chính của bug."),

    tc("Modal hoàn tất copy", "PAY-PLAN-001", "Normal",
       "Modal hoàn tất hiển thị đúng nhãn plan コミュニケーションプラン của LOA nhận",
       AB + "\n- Bot B đang ở plan LINE có hạn mức gửi tin thuộc nhóm communication",
       "1. Chuẩn bị bot B với hạn mức gửi tin lần lượt là 100, rồi 200, rồi 500\n"
       "2. Mỗi lần thực hiện copy A → B và đọc nhãn plan trên modal hoàn tất",
       "Hạn mức gửi tin của bot B: 100 · 200 · 500",
       "- Cả 3 mức đều hiển thị nhãn「コミュニケーションプラン」\n"
       "- Nhãn lấy theo bot B (bên nhận), không phải bot A\n"
       "- Verify bổ sung: khớp `bots.limit_message_loa` của bot B",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r317-r319 (bug #38411). Gộp 3 mức vì CÙNG 1 kết quả. "
            "PRODUCTION theo RULE-08 (liên quan plan tính tiền)."),

    tc("Modal hoàn tất copy", "PAY-PLAN-001", "Boundary",
       "Nhãn plan đổi từ コミュニケーション sang ライト tại mốc 501",
       AB,
       "1. Đặt hạn mức gửi tin của bot B = 500 → copy A→B → đọc nhãn\n"
       "2. Đặt = 501 → copy → đọc nhãn\n"
       "3. Đặt = 4999 → copy → đọc nhãn\n"
       "4. Đặt = 5000 → copy → đọc nhãn",
       "500 · 501 · 4999 · 5000",
       "- 500 → hiển thị「コミュニケーションプラン」\n"
       "- 501, 4999, 5000 → hiển thị「ライトプラン」\n"
       "- Ranh giới nằm đúng giữa 500 và 501",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r319-r322 (bug #38411). Tách riêng vì đây là TC biên có kết quả KHÁC TC trên."),

    tc("Modal hoàn tất copy", "PAY-PLAN-001", "Boundary",
       "Nhãn plan đổi từ ライト sang スタンダード tại mốc 5001",
       AB,
       "1. Đặt hạn mức gửi tin của bot B = 5000 → copy A→B → đọc nhãn\n"
       "2. Đặt = 5001 → copy → đọc nhãn\n"
       "3. Đặt = 29000 → copy → đọc nhãn\n"
       "4. Đặt = 30000 → copy → đọc nhãn\n"
       "5. Đặt = 31000 → copy → đọc nhãn",
       "5000 · 5001 · 29000 · 30000 · 31000",
       "- 5000 → hiển thị「ライトプラン」\n"
       "- 5001, 29000, 30000, 31000 → hiển thị「スタンダードプラン」\n"
       "- Ranh giới nằm đúng giữa 5000 và 5001",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r322-r326 (bug #38411)."),

    tc("Modal hoàn tất copy", "DATA-COUNT-001", "Normal",
       "Modal hoàn tất hiển thị đúng SỐ BẠN BÈ của LOA nhận",
       AB + "\n- Bot A và bot B có số bạn bè khác nhau rõ rệt",
       "1. Ghi lại số bạn bè hiện tại của bot A và bot B (xem ở màn 友だちリスト)\n"
       "2. Thực hiện copy A → B\n"
       "3. Đọc số bạn bè hiển thị trên modal hoàn tất\n"
       "4. Đối chiếu với 2 số đã ghi",
       "Bot A: 120 bạn · Bot B: 37 bạn",
       "- Modal hiển thị 37 (số của bot B — bên nhận)\n"
       "- KHÔNG hiển thị 120",
       env="PRODUCTION",
       note="Nguồn: Backup 1.0 r327 (bug #38411)."),

    tc("Modal hoàn tất copy", "STATE-CLEAN-001", "Normal",
       "Bấm「閉じる」ở modal hoàn tất — quay về màn データコピー",
       AB + "\n- Modal「データコピー完了」đang hiện",
       "1. Bấm nút「閉じる」\n"
       "2. Quan sát màn hình sau khi modal đóng",
       "—",
       "- Modal đóng\n"
       "- Quay về màn データコピー, tab「コピー登録」đang active\n"
       "- Form nhập mã ở trạng thái trống, sẵn sàng cho lần copy tiếp theo\n"
       "- Sidebar và header hiện lại bình thường",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note=MT00 + "Nguồn: [AI]UI r2 (TC-BK-001) bước 12 — TC gốc ghi rõ đây là GIẢ ĐỊNH A-04, chưa xác nhận."),

    tc("Modal hoàn tất copy", "STATE-CLEAN-001", "Normal",
       "Bấm X ở modal hoàn tất",
       AB + "\n- Modal「データコピー完了」đang hiện",
       "1. Bấm nút X ở góc trên phải modal\n"
       "2. Quan sát màn hình",
       "—",
       "- Modal đóng và cho kết quả GIỐNG nút「閉じる」— quay về màn データコピー\n"
       "- Không bị kẹt lại màn xử lý",
       spec="Spec không ghi",
       note="Kết quả mong đợi do AI viết (đối xứng với nút 閉じる). Corpus chỉ ghi modal CÓ nút X "
            "([AI]UI r19) mà không nói bấm vào thì ra gì. Cần Leader xác nhận."),

    # ═══════════════ 7. Tab lịch sử copy ═══════════════
    tc("Tab lịch sử copy", "LIST-001", "Normal",
       "Bảng「コピー履歴」hiển thị đủ cột và sắp xếp mới nhất lên đầu",
       A + "\n- Bot A đã thực hiện ít nhất 3 lần copy vào các thời điểm khác nhau",
       "1. Vào tab「コピー履歴」\n"
       "2. Đọc tiêu đề các cột\n"
       "3. Đọc cột thời gian của 3 dòng đầu và so sánh",
       "3 bản ghi tạo cách nhau ≥ 1 phút",
       "- Có đủ cột: thời gian copy, mã, tên tài khoản, trạng thái\n"
       "- Thời gian định dạng YYYY.MM.DD HH:mm theo giờ Nhật\n"
       "- Dòng trên cùng là lần copy MỚI NHẤT, giảm dần xuống dưới",
       note="Nguồn: feature-spec §2.1 Block 4 + BR-07; [AI]API r29 (TC-BK-061)."),

    tc("Tab lịch sử copy", "STATE-001", "Normal",
       "Trạng thái đang chờ / đang xử lý / trong hàng đợi đều hiển thị「処理中」",
       A + "\n- Có bản ghi ở cả 3 trạng thái nội bộ: vừa tạo, đang trong hàng đợi, đang thực hiện",
       "1. Tạo 1 backup và mở tab「コピー履歴」ngay lập tức\n"
       "2. Quan sát nhãn trạng thái ở các mốc: vừa tạo → vào hàng đợi → đang copy\n"
       "3. Ghi lại nhãn ở từng mốc",
       "Quay màn hình liên tục trong 30 giây đầu",
       "- Cả 3 mốc đều hiển thị nhãn「処理中」\n"
       "- Nhãn không đổi qua lại giữa các mốc",
       env="PRODUCTION",
       note="Nguồn: [AI]UI r18 (TC-BK-017); feature-spec BR-08 (status 0/1/4 →「処理中」). "
            "Phần này 2 bên KHỚP nhau."),

    tc("Tab lịch sử copy", "STATE-001", "Normal",
       "Copy THÀNH CÔNG hiển thị nhãn gì?",
       A + "\n- Có ít nhất 1 bản ghi đã copy thành công",
       "1. Vào tab「コピー履歴」\n"
       "2. Tìm dòng của lần copy đã thành công\n"
       "3. Đọc nhãn trạng thái và ghi lại nguyên văn",
       "—",
       "- Hiển thị đúng nhãn Leader chốt ở MT-03:「完了」(theo corpus) hoặc「処理完了済」(theo spec)\n"
       "- Nhãn có màu phân biệt với các trạng thái khác",
       spec="Đã hỏi leader",
       note="MT-03 — [AI]UI r16 (TC-BK-015) nói「完了」và ghi「THAY ĐỔI so với FA-033」; "
            "feature-spec BR-08 nói「処理完了済」. Ô Note gốc còn ghi「Design không có badge」. "
            "Evidence: ảnh bảng lịch sử."),

    tc("Tab lịch sử copy", "STATE-001", "Abnormal",
       "Copy THẤT BẠI hiển thị gì? — phải phân biệt được với thành công",
       A + "\n- Có ít nhất 1 bản ghi copy đã thất bại (nhờ Dev dựng)",
       "1. Vào tab「コピー履歴」\n"
       "2. Tìm dòng của lần copy thất bại\n"
       "3. Đọc nhãn, quan sát màu nền của dòng\n"
       "4. Đặt cạnh dòng copy thành công để so sánh",
       "1 dòng thất bại + 1 dòng thành công trong cùng bảng",
       "- Người dùng PHÂN BIỆT ĐƯỢC thất bại với thành công chỉ bằng mắt\n"
       "- Theo corpus: nhãn「エラー」+ nền đỏ nhạt\n"
       "- Theo spec hiện tại: cả 2 cùng hiển thị「処理完了済」— nếu đúng như vậy thì đây là điểm phải raise bug",
       spec="Đã hỏi leader",
       note="MT-03 — [AI]UI r17 (TC-BK-016) nói「エラー」nền đỏ; feature-spec BR-08 + §9.3 mục 1 nói "
            "không phân biệt được. ⚠️ DỰ KIẾN FAIL nếu production còn theo spec cũ → raise bug. "
            "Evidence: ảnh 2 dòng cạnh nhau."),

    tc("Tab lịch sử copy", "UI-002", "Normal",
       "Dòng đang xử lý có nền khác dòng đã xong",
       A + "\n- Trong bảng có đồng thời dòng「処理中」và dòng đã hoàn tất",
       "1. Vào tab「コピー履歴」khi đang có 1 backup chạy\n"
       "2. So sánh màu nền dòng đang xử lý với dòng đã xong\n"
       "3. Chụp ảnh cả bảng",
       "—",
       "- Dòng đang xử lý có màu nền nổi bật khác hẳn dòng đã xong\n"
       "- Nhận ra ngay có backup đang chạy mà không cần đọc chữ",
       env="PRODUCTION",
       note=MT00 + "Nguồn: [AI]UI r34 (TC-BK-033) — TC gốc ghi「màu highlight cụ thể cần xác nhận với Figma」."),

    tc("Tab lịch sử copy", "LIST-001", "Boundary",
       "Bot chưa từng copy lần nào — bảng lịch sử trống",
       "- Đăng nhập Admin của một bot MỚI, chưa từng thực hiện copy lần nào",
       "1. Vào màn データコピー\n"
       "2. Bấm tab「コピー履歴」\n"
       "3. Quan sát bảng và khu vực phân trang",
       "Bot mới tinh",
       "- Bảng không có dòng dữ liệu nào\n"
       "- Có thông báo trống (「コピー履歴はありません」hoặc tương đương)\n"
       "- Không có lỗi JavaScript trong console\n"
       "- Phân trang ẩn hoặc ở trạng thái không bấm được",
       note=MT00 + "Nguồn: [AI]UI r21 (TC-BK-020)."),

    tc("Tab lịch sử copy", "LIST-001", "Normal",
       "Chuyển sang trang 2 của bảng lịch sử",
       A + "\n- Bot A có hơn 100 bản ghi lịch sử copy",
       "1. Vào tab「コピー履歴」\n"
       "2. Ghi lại thời gian của dòng cuối trang 1\n"
       "3. Bấm số trang 2 (hoặc mũi tên sang phải)\n"
       "4. Đọc các dòng trang 2",
       ">100 bản ghi",
       "- Trang 2 hiển thị các bản ghi tiếp theo, KHÔNG trùng bản ghi nào của trang 1\n"
       "- Mọi bản ghi trang 2 đều CŨ HƠN dòng cuối trang 1\n"
       "- Số trang đang active đổi thành 2\n"
       "- Không reload toàn trang",
       spec="Đã hỏi leader",
       note="MT-07 — [AI]UI r28 (TC-BK-027); [AI]API r29 (TC-BK-061). "
            "feature-spec BK-Q07 tự nhận CHƯA BIẾT có phân trang không → TC này LẤP GAP."),

    tc("Tab lịch sử copy", "LIST-001", "Normal",
       "Đổi số dòng hiển thị trên mỗi trang",
       A + "\n- Bot A có ít nhất 20 bản ghi lịch sử",
       "1. Vào tab「コピー履歴」\n"
       "2. Đọc giá trị mặc định của ô chọn số dòng/trang\n"
       "3. Mở ô chọn, ghi lại danh sách lựa chọn\n"
       "4. Chọn 10 và đếm số dòng hiển thị",
       "≥20 bản ghi",
       "- Bước 2: giá trị mặc định là 100\n"
       "- Bước 3: danh sách có đủ 10, 20, 30, 50, 100\n"
       "- Bước 4: bảng hiển thị đúng tối đa 10 dòng, số trang tăng tương ứng",
       spec="Đã hỏi leader",
       note="MT-07 — [AI]UI r29 (TC-BK-028), TC gốc ghi「dựa trên giả định A-06, đã có answer QA-012」."),

    tc("Tab lịch sử copy", "SEC-ISO-001", "Abnormal",
       "Bảng lịch sử CHỈ hiển thị bản ghi của bot đang đăng nhập",
       "- Admin quản lý cả bot A và bot C\n- Cả 2 bot đều đã từng thực hiện copy",
       "1. Đăng nhập bot A, vào tab「コピー履歴」, ghi lại toàn bộ danh sách\n"
       "2. Đổi sang bot C, vào tab「コピー履歴」, ghi lại danh sách\n"
       "3. So sánh 2 danh sách",
       "Bot A có 5 bản ghi, bot C có 3 bản ghi",
       "- Bot A chỉ thấy 5 bản ghi của mình\n"
       "- Bot C chỉ thấy 3 bản ghi của mình\n"
       "- Không có bản ghi nào xuất hiện ở cả 2 danh sách",
       note="Suy luận của AI theo SEC-ISO-001 + BR-07 — corpus không có TC cách ly bảng lịch sử. Cần Leader xác nhận."),

    # ═══════════════ 8. Phân quyền & plan ═══════════════
    tc("Phân quyền & plan", "PERM-001", "Abnormal",
       "Tài khoản Staff KHÔNG thấy menu「データコピー」",
       "- Có tài khoản Staff đã được Admin cấp quyền trên bot A\n- Đăng nhập bằng tài khoản Staff",
       "1. Đăng nhập bằng tài khoản Staff\n"
       "2. Mở Sidebar, tìm nhóm「システム管理関連」\n"
       "3. Liệt kê các mục nhìn thấy trong nhóm đó",
       "Tài khoản Staff",
       "- Mục「データコピー」KHÔNG xuất hiện trong Sidebar\n"
       "- Các mục khác của nhóm システム管理関連 hiển thị theo đúng quyền đã cấp",
       note="Nguồn: [AI]UI r25 (TC-BK-024); feature-spec §1.2; ui-spec §2. TC hồi quy."),

    tc("Phân quyền & plan", "PERM-002", "Abnormal",
       "Staff gõ thẳng URL /basic/backup",
       "- Đăng nhập bằng tài khoản Staff của bot A",
       "1. Đăng nhập Staff\n"
       "2. Gõ thẳng /basic/backup vào thanh địa chỉ\n"
       "3. Quan sát kết quả",
       "URL /basic/backup",
       "- Bị chuyển hướng đi nơi khác hoặc nhận thông báo không có quyền\n"
       "- KHÔNG hiển thị nội dung màn データコピー\n"
       "- KHÔNG nhìn thấy mã copy của bot",
       spec="Đã hỏi leader",
       note="MT-25 — [AI]UI r25 (TC-BK-024) bước 3. feature-spec §9.1 BK-Q08 ghi rõ "
            "「middleware CHƯA VERIFY server-side access control」→ TC này ĐÓNG GAP BK-Q08. "
            "⚠️ Nếu Staff vào được thì đây là lỗ hổng phân quyền, phải raise bug."),

    tc("Phân quyền & plan", "PERM-002", "Abnormal",
       "Staff gọi thẳng chức năng bắt đầu copy ở tầng API",
       "- Đăng nhập bằng tài khoản Staff của bot A\n- Biết mã copy hợp lệ của bot B",
       "1. Lấy cookie phiên của tài khoản Staff\n"
       "2. Gửi POST /basic/backup/export-zip kèm mã bot B bằng phiên Staff (Postman)\n"
       "3. Kiểm tra phản hồi\n"
       "4. Đăng nhập Admin, vào tab「コピー履歴」đếm số dòng",
       "Phiên Staff + mã hợp lệ",
       "- Bị từ chối (redirect đăng nhập hoặc lỗi không có quyền)\n"
       "- Bước 4: KHÔNG có dòng lịch sử mới nào được tạo\n"
       "- Không có job copy nào chạy",
       spec="Đã hỏi leader",
       note="MT-25 — chặn ở TẦNG API, không chỉ ẩn menu. Corpus KHÔNG có TC này; "
            "TC do AI bổ sung theo PERM-002 vì spec BK-Q08 tự nhận chưa verify server-side. "
            "Cần Leader duyệt trước khi giao member."),

    tc("Phân quyền & plan", "PERM-001", "Normal",
       "「Backup từ bot staff ⇒ bot chính」— làm rõ định nghĩa bot staff",
       "- Cần Leader làm rõ「bot staff」là gì trước khi chạy (xem MT-25)",
       "1. Xác định đúng đối tượng「bot staff」theo định nghĩa Leader chốt\n"
       "2. Thực hiện copy từ bot staff sang bot chính\n"
       "3. Quan sát toàn bộ luồng và kết quả ở bot chính",
       "Theo định nghĩa Leader chốt",
       "- Kết quả mong đợi CHƯA XÁC ĐỊNH — chờ quyết định MT-25\n"
       "- Nếu「bot staff」là bot phụ do tài khoản staff quản lý: copy chạy bình thường như 2 bot Admin\n"
       "- Nếu là tài khoản role Staff: phải bị chặn theo TC phân quyền ở trên",
       spec="Đã hỏi leader",
       note="MT-25 — TC gốc lặp 5 lần ở Backup 1.0 r186/r220/r309/r314/r330 và Backup (job) r242/r399 "
            "nhưng LUÔN để TRỐNG ô kết quả mong đợi. KHÔNG giao member cho tới khi Leader chốt."),

    tc("Phân quyền & plan", "PAY-PLAN-001", "Abnormal",
       "Bot plan Free vào màn データコピー — nội dung thông báo",
       "- Đăng nhập Admin của một bot đang ở plan Free",
       "1. Đăng nhập Admin bot plan Free\n"
       "2. Bấm menu「データコピー」(hoặc gõ thẳng /basic/backup)\n"
       "3. Đọc nguyên văn thông báo hiện ra",
       "Bot plan Free",
       "- Hiển thị đúng nội dung Leader chốt ở MT-02:\n"
       "  · bản cũ:「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "  · bản mới:「フリープランではデータコピーはご利用いただけません。（コピーコードの取得のみ可能です）」",
       spec="Đã hỏi leader",
       note="MT-02 — [AI]UI r26 (TC-BK-025) vs r43 (Comment 6, Test Result = OK). Evidence: ảnh thông báo."),

    tc("Phân quyền & plan", "PAY-PLAN-001", "Abnormal",
       "Bot plan Free bấm OK ở thông báo — có bị đá về màn home không?",
       "- Đăng nhập Admin của một bot đang ở plan Free\n- Thông báo chặn đang hiển thị",
       "1. Bấm nút OK trên thông báo\n"
       "2. Quan sát URL và nội dung màn hình sau đó",
       "Bot plan Free",
       "- Kết quả theo quyết định MT-02:\n"
       "  · bản cũ: tự động chuyển về /admin/home\n"
       "  · bản mới: đóng thông báo và Ở LẠI màn データコピー, KHÔNG bị back về home",
       spec="Đã hỏi leader",
       note="MT-02 — [AI]UI r44 (Comment 6) ghi rõ「Đóng modal, hiển thị màn hình tại Backup, "
            "Không bị back về màn home」, Test Result = OK. Trái BR-03."),

    tc("Phân quyền & plan", "PAY-PLAN-001", "Abnormal",
       "Bot plan Free vẫn lấy được mã copy của chính nó",
       "- Đăng nhập Admin của một bot đang ở plan Free",
       "1. Vào màn データコピー, đóng thông báo chặn\n"
       "2. Tìm khối「このアカウントのコピーコード」\n"
       "3. Thử sao chép mã\n"
       "4. Thử nhập mã của LOA khác vào ô nhập mã và bấm xác nhận",
       "Bot plan Free",
       "- Bước 2-3: xem và sao chép được mã copy của chính bot Free\n"
       "- Bước 4: KHÔNG thực hiện được thao tác copy dữ liệu",
       spec="Đã hỏi leader",
       note="MT-02 — suy ra từ nguyên văn「（コピーコードの取得のみ可能です）」ở [AI]UI r43. "
            "Đây là SUY LUẬN của AI về hành vi cụ thể, cần Leader xác nhận."),

    tc("Phân quyền & plan", "PAY-PLAN-001", "Normal",
       "Copy dữ liệu từ bot Free sang bot có phí",
       "- Bot F ở plan Free, đã có sẵn tag, template, scenario, form\n"
       "- Bot P ở plan Standard hoặc Pro",
       "1. Ở bot F, lấy mã copy\n"
       "2. Đăng nhập bot P, vào màn データコピー\n"
       "3. Nhập mã của bot F, xác nhận và thực hiện copy\n"
       "4. Sau khi xong, kiểm tra màn tag / template / scenario / form của bot P",
       "Bot F có ≥3 tag, ≥3 template, ≥1 scenario, ≥1 form",
       "- Copy chạy thành công\n"
       "- Bot P hiển thị ĐẦY ĐỦ dữ liệu đã có ở bot F\n"
       "- Số lượng từng loại khớp với bot F",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="MT-01 + MT-02 — [AI]UI r47 (Comment 6, Test Result = OK). TC này là bằng chứng mạnh cho "
            "chiều copy mà MT-01 đang hỏi: bot Free làm bên GỬI."),

    tc("Phân quyền & plan", "PAY-PLAN-001", "Normal",
       "Bot plan Standard / Pro vào màn データコピー bình thường",
       A,
       "1. Đăng nhập Admin bot plan Standard\n"
       "2. Bấm menu「データコピー」\n"
       "3. Quan sát toàn bộ trang\n"
       "4. Lặp lại với bot plan Pro",
       "1 bot Standard + 1 bot Pro",
       "- Cả 2 plan: trang tải bình thường, KHÔNG có thông báo chặn, KHÔNG bị chuyển hướng\n"
       "- Tab「コピー登録」active mặc định\n"
       "- Hiển thị đủ: khối mã copy + danh sách loại dữ liệu + form nhập mã + cảnh báo vàng\n"
       "- Có nút「コピーコードの再発行」",
       note="Gộp 2 plan vì CÙNG 1 kết quả. Nguồn: [AI]UI r27 (TC-BK-026). TC hồi quy."),
]
