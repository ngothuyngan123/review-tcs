# -*- coding: utf-8 -*-
"""FA-007 あいさつメッセージ — Nhóm 12-14: hành vi THẬT phía LINE user khi kết bạn
mới, kết bạn lại (bạn cũ) và hủy chặn.

Nguồn chính: 05. TCsLine_Setting kết bạn → tab「Improve setting add fr 2.0」:
r51-r62, r91-r93 (新規); r148-r162, r191-r192 (既存); r286-r297, r327-r328 (unblock).
Toàn bộ nhóm này chạy trên môi trường có LINE OA thật (RULE-08).
"""
from _common import tc

BASE_NEW = ("- Bot đã liên kết LINE OA thật, callback hoạt động\n"
            "- Trang 新規友だち用 đã lưu tin nhắn + action, đã bấm 保存\n"
            "- Có tài khoản LINE test CHƯA TỪNG kết bạn với bot (chưa có trên エルメ)")
BASE_OLD = ("- Bot đã liên kết LINE OA thật\n"
            "- Trang 既存友だち用 đã lưu tin nhắn + action, đã bấm 保存\n"
            "- Có tài khoản LINE test ĐÃ từng là bạn của bot (đã có bản ghi trên エルメ)")
BASE_UNB = ("- Bot đã liên kết LINE OA thật\n"
            "- Trang ブロック解除時用 đã lưu tin nhắn + action, đã bấm 保存\n"
            "- Có tài khoản LINE test đang BLOCK bot")

S5 = [
    # ═══════════ 12. Kết bạn mới — gửi tin & action ═══════════
    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Normal",
       "Friend mới quét QR kết bạn — nhận đúng tin nhắn đã cài ở trang 新規友だち用",
       BASE_NEW,
       "1. Ở admin, trang 新規友だち用: lưu tin nhắn「xin chao ban moi」, bấm 保存\n"
       "2. Dùng tài khoản LINE test quét QR kết bạn của bot\n"
       "3. Đọc tin nhắn nhận được trên app LINE (bấm giờ từ lúc kết bạn)\n"
       "4. Về admin mở màn chat 1:1, tìm friend vừa kết bạn",
       "Tin nhắn: 「xin chao ban moi」",
       "- Trên app LINE nhận đúng nội dung「xin chao ban moi」\n"
       "- Thời gian từ lúc kết bạn tới lúc nhận tin thường dưới 2-3 giây\n"
       "- Ở màn chat 1:1 của admin cũng hiển thị đúng tin nhắn đã gửi cho friend đó\n"
       "- Friend chỉ nhận ĐÚNG 1 lần (không bị gửi lặp)",
       env="PRODUCTION",
       note="Nguồn: r51 (『check send msg cho user sau khi add kết bạn → đúng msg đã setting』) + "
            "job-spec.md『độ trễ tổng thường < 2-3 giây』. RULE-07: khớp app LINE + màn chat 1:1."),

    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Normal",
       "Tin nhắn có biến {name} — hiển thị đúng tên LINE của friend ở cả app LINE và màn chat 1:1",
       BASE_NEW,
       "1. Trang 新規友だち用: nhập tin nhắn có chèn「＋ LINE名」, VD「{name}さん、はじめまして」\n"
       "2. Bấm 保存\n"
       "3. Dùng tài khoản LINE test (tên hiển thị: Nguyen Test) quét QR kết bạn\n"
       "4. Đọc tin nhắn trên app LINE\n"
       "5. Về admin, mở chat 1:1 của friend đó và đọc tin đã gửi",
       "Tin nhắn: 「{name}さん、はじめまして」· Tên LINE của tài khoản test: Nguyen Test",
       "- Trên app LINE hiển thị「Nguyen Testさん、はじめまして」(biến đã được thay bằng tên thật)\n"
       "- Ở màn chat 1:1 của admin cũng hiển thị tên đã được thay, KHÔNG còn chuỗi {name}",
       env="PRODUCTION",
       note="Nguồn: r57 (『check khi msg có replace name → có hiển thị được tên friend phía web, "
            "line user』), r92."),

    tc("Kết bạn mới — gửi tin & action", "FRIEND-001", "Normal",
       "Tin nhắn chèn 友だち情報 nhưng friend mới CHƯA có dữ liệu — không hiển thị chuỗi biến thô",
       BASE_NEW,
       "1. Trang 新規友だち用: nhập tin nhắn có chèn 友だち情報「システム表示名」và「địa chỉ email」\n"
       "2. Bấm 保存\n"
       "3. Dùng tài khoản LINE test kết bạn (friend mới → chưa có email)\n"
       "4. Đọc tin nhắn trên app LINE",
       "Tin nhắn có 2 biến friend info; friend mới chưa có giá trị email",
       "- Chỗ có dữ liệu (システム表示名) hiển thị đúng giá trị\n"
       "- Chỗ CHƯA có dữ liệu (email) hiển thị rỗng hoặc giá trị mặc định — TUYỆT ĐỐI không hiện "
       "chuỗi biến thô kiểu [FRIEND_INFO_xxx] cho LINE user",
       env="PRODUCTION",
       note="Nguồn: r58 (kết quả gốc chỉ ghi 『[FRIEND_INFO_system_name]』, không nói hiển thị ra "
            "sao khi rỗng) — expected do AI viết cho đo được. CẦN LEADER XÁC NHẬN giá trị hiển thị "
            "khi friend info rỗng.",
       spec="Đã hỏi leader"),

    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Normal",
       "Friend mới kết bạn — các action đã cài chạy đúng và đủ",
       BASE_NEW + "\n- Trang 新規友だち用 đã cài 3 action: gắn tag TX · gửi template M · "
                  "bắt đầu scenario S",
       "1. Kiểm tra lại 3 action ở trang 新規友だち用, bấm 保存\n"
       "2. Dùng tài khoản LINE test quét QR kết bạn\n"
       "3. Đọc toàn bộ tin nhắn nhận trên app LINE\n"
       "4. Về admin mở màn chi tiết friend: kiểm tra tag\n"
       "5. Mở màn ステップ配信 kiểm tra friend đã vào scenario S chưa",
       "3 action: tag TX · template M · scenario S",
       "- Friend được gắn tag TX (thấy ở màn chi tiết friend)\n"
       "- Friend nhận nội dung của template M trên app LINE\n"
       "- Friend đã được đưa vào scenario S và nhận bước đầu theo lịch của scenario\n"
       "- Không action nào bị bỏ sót, không action nào chạy 2 lần",
       env="PRODUCTION",
       note="Nguồn: r91 (『check job send action cho user sau khi add kết bạn → đúng action đã "
            "setting』). RULE-07: kiểm 3 tầng — app LINE + màn chi tiết friend + màn scenario."),

    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Normal",
       "Chỉ cài action, KHÔNG cài tin nhắn — friend chỉ nhận action, không nhận tin chào mừng",
       BASE_NEW + "\n- Trang 新規友だち用: ô tin nhắn để TRỐNG, chỉ cài 1 action gắn tag TX",
       "1. Xóa sạch tin nhắn ở trang 新規友だち用, giữ 1 action gắn tag TX, bấm 保存\n"
       "2. Dùng tài khoản LINE test kết bạn\n"
       "3. Đọc tin nhắn nhận trên app LINE\n"
       "4. Kiểm tra tag ở màn chi tiết friend",
       "Tin nhắn rỗng + 1 action gắn tag TX",
       "- Friend KHÔNG nhận tin nhắn chào mừng nào từ エルメ\n"
       "- Nhưng vẫn được gắn tag TX",
       env="PRODUCTION",
       note="TC do AI bổ sung (ma trận có/không tin nhắn × có/không action). Corpus chỉ có case đủ "
            "cả 2. Cần Leader xác nhận.",
       spec="Spec không ghi"),

    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Normal",
       "Không cài gì ở trang 新規友だち用 — friend mới không nhận gì từ エルメ, vẫn hiện trên tool",
       BASE_NEW + "\n- Trang 新規友だち用: tin nhắn TRỐNG và KHÔNG có action nào",
       "1. Xóa sạch tin nhắn và action ở trang 新規友だち用, bấm 保存\n"
       "2. Dùng tài khoản LINE test kết bạn\n"
       "3. Đọc tin nhắn trên app LINE\n"
       "4. Về admin mở màn danh sách bạn bè và chat 1:1",
       "Không cấu hình gì",
       "- Friend KHÔNG nhận tin nhắn nào từ エルメ\n"
       "- Nhưng friend VẪN xuất hiện trong danh sách bạn bè và có phòng chat 1:1 (lịch sử kết bạn "
       "vẫn được ghi nhận)",
       env="PRODUCTION",
       note="Nguồn: job-spec.md §Edge cases (『add_friend_setting không tồn tại → không gửi tin, "
            "chỉ ghi lịch sử』) + tab「Improve setting add fr 1.0」r10 (『k set act thì k thực hiện "
            "act』). Corpus không có TC riêng — do AI bổ sung."),

    tc("Kết bạn mới — gửi tin & action", "MSG-USER-001", "Abnormal",
       "Friend MỚI kết bạn — KHÔNG chạy nhầm cấu hình của trang 既存友だち用 / ブロック解除時用",
       BASE_NEW + "\n- Cả 3 trang đều cài tin nhắn và tag KHÁC nhau: "
                  "新規=tag T1+msg「M1」· 既存=tag T2+msg「M2」· unblock=tag T3+msg「M3」",
       "1. Cài đủ 3 trang như tiền điều kiện, bấm 保存 từng trang\n"
       "2. Dùng tài khoản LINE test CHƯA từng kết bạn để quét QR kết bạn\n"
       "3. Đọc tin nhắn trên app LINE\n"
       "4. Kiểm tra tag của friend ở màn chi tiết friend",
       "3 bộ cấu hình khác nhau: (T1,M1) · (T2,M2) · (T3,M3)",
       "- Friend chỉ nhận「M1」và chỉ được gắn tag T1\n"
       "- KHÔNG nhận「M2」/「M3」, KHÔNG bị gắn T2/T3",
       env="PRODUCTION",
       note="Nguồn: tab「Improve setting add fr 1.0」r10 (『Nếu old fr thì thực hiện act set cho "
            "old fr』) + job-spec.md §Bước 1 (phân loại loại bạn). Đây là TC phân loại quan trọng "
            "nhất của tính năng — do AI dựng lại thành ma trận đối chứng đủ 3 loại."),

    tc("Kết bạn mới — gửi tin & action", "INTG-LINE-001", "Normal",
       "Tin nhắn chào mừng gửi ngay sau kết bạn — dùng được cả khi quá cửa sổ trả lời của LINE",
       BASE_NEW,
       "1. Cài tin nhắn chào mừng ở trang 新規友だち用\n"
       "2. Dùng tài khoản LINE test kết bạn, đo thời gian nhận tin\n"
       "3. Lặp lại với tài khoản test khác vào lúc hệ thống đang tải nặng (hoặc dựng độ trễ)\n"
       "4. So sánh 2 lần",
       "2 lần kết bạn: bình thường và khi có độ trễ",
       "- Cả 2 lần friend đều nhận được tin nhắn chào mừng\n"
       "- Trường hợp trễ quá 30 giây vẫn nhận được tin (hệ thống chuyển sang cách gửi chủ động)\n"
       "- Không có tin nào bị mất im lặng; nếu lỗi thì phải thấy ở màn 配信エラー",
       env="PRODUCTION",
       note="TC do AI bổ sung theo job-spec.md §Bước 6 (『replyMessage nếu còn trong 30 giây, "
            "ngược lại pushMessage』) + INTG-LINE-001. Corpus không có. Cần Leader xác nhận.",
       spec="Đã hỏi leader"),

    tc("Kết bạn mới — gửi tin & action", "MSG-005", "Abnormal",
       "Bot đã hết quota tin nhắn tháng — tin chào mừng không gửi được thì phải thấy lỗi",
       "- Bot dùng gói có giới hạn số tin/tháng và ĐÃ dùng hết quota\n"
       "- Trang 新規友だち用 đã cài tin nhắn chào mừng\n"
       "- Có tài khoản LINE test chưa kết bạn",
       "1. Đưa bot về trạng thái hết quota tin nhắn tháng\n"
       "2. Dùng tài khoản LINE test kết bạn\n"
       "3. Kiểm tra tin nhắn trên app LINE\n"
       "4. Về admin mở màn 配信エラー và màn chat 1:1",
       "Bot hết quota tin nhắn tháng",
       "- Không gửi được tin thì phải có bản ghi lỗi ở màn 配信エラー (không im lặng bỏ qua)\n"
       "- Màn chat 1:1 KHÔNG hiển thị tin như thể đã gửi thành công (chống false success)\n"
       "- Các action không gửi tin (VD gắn tag) vẫn chạy bình thường",
       env="PRODUCTION",
       note="TC do AI bổ sung theo MSG-005 + OUT-TRUTH-001. Corpus KHÔNG có case hết quota ở màn "
            "này. Cần Leader xác nhận.",
       spec="Spec không ghi"),

    # ═══════════ 13. Kết bạn cũ — gửi tin & action ═══════════
    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Friend cũ kết bạn lại — nhận đúng tin nhắn của trang 既存友だち用",
       BASE_OLD,
       "1. Ở admin: xóa friend test ở màn chi tiết friend (nút 削除) để đưa về trạng thái bạn cũ "
       "theo hướng dẫn tab テスト方法\n"
       "2. Trang 既存友だち用 lưu tin nhắn「chao ban cu」, bấm 保存\n"
       "3. Dùng tài khoản LINE test kết bạn lại với bot\n"
       "4. Đọc tin nhắn trên app LINE\n"
       "5. Về admin mở chat 1:1 của friend đó",
       "Tin nhắn: 「chao ban cu」",
       "- Friend nhận đúng「chao ban cu」(KHÔNG nhận tin của trang 新規友だち用)\n"
       "- Màn chat 1:1 hiển thị đúng tin vừa gửi",
       env="PRODUCTION",
       note="Nguồn: r148 (『check line user sau khi kết bạn lại → hiển thị đúng msg khi setting』)."),

    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Friend cũ kết bạn lại — các action của trang 既存友だち用 chạy đúng",
       BASE_OLD + "\n- Trang 既存友だち用 đã cài 2 action: gắn tag TO · gửi template MO",
       "1. Đưa friend test về trạng thái bạn cũ\n"
       "2. Kiểm tra 2 action ở trang 既存友だち用, bấm 保存\n"
       "3. Dùng tài khoản LINE test kết bạn lại\n"
       "4. Đọc tin nhắn trên app LINE, kiểm tra tag ở màn chi tiết friend",
       "2 action: tag TO · template MO",
       "- Friend được gắn tag TO\n"
       "- Friend nhận nội dung template MO\n"
       "- Không chạy action của trang 新規友だち用",
       env="PRODUCTION",
       note="Nguồn: r191 (『check job send action cho user sau khi kết bạn lại → đúng msg đã "
            "setting』), r192."),

    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Tin nhắn trang 既存友だち用 có biến {name} và 友だち情報 — hiển thị đúng giá trị",
       BASE_OLD + "\n- Friend test đã có sẵn dữ liệu friend info: システム表示名, điện thoại di động, "
                  "địa chỉ email, ngày sinh",
       "1. Trang 既存友だち用: chèn「＋ LINE名」và 4 mục 友だち情報 vào tin nhắn, bấm 保存\n"
       "2. Đưa friend test về trạng thái bạn cũ\n"
       "3. Dùng tài khoản LINE test kết bạn lại\n"
       "4. Đọc tin nhắn trên app LINE và đối chiếu từng giá trị với màn chi tiết friend",
       "4 mục: システム表示名 · điện thoại di động · địa chỉ email · ngày sinh",
       "- Tên LINE hiển thị đúng\n"
       "- Cả 4 mục 友だち情報 hiển thị ĐÚNG giá trị đang lưu ở màn chi tiết friend\n"
       "- Không còn chuỗi biến thô trong tin nhắn",
       env="PRODUCTION",
       note="Nguồn: r153, r154 (liệt kê đúng 4 mục). RULE-07: đối chiếu app LINE với màn chi tiết "
            "friend."),

    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Bot đã xóa friend, friend nhắn tin lại — hiện lên tool và chạy cấu hình bạn cũ",
       BASE_OLD,
       "1. Ở admin, xóa friend test ở màn chi tiết friend\n"
       "2. Trang 既存友だち用 lưu tin nhắn + 1 action gắn tag TO\n"
       "3. Dùng tài khoản LINE test GỬI TIN NHẮN TEXT cho bot (không kết bạn lại bằng QR)\n"
       "4. Về admin mở màn danh sách bạn bè và chat 1:1\n"
       "5. Kiểm tra tin nhắn friend nhận được và tag của friend",
       "Friend gửi tin nhắn text cho bot sau khi bị xóa khỏi tool",
       "- Friend hiện lại trên tool (có trong danh sách bạn bè, có phòng chat 1:1)\n"
       "- Friend nhận tin nhắn chào mừng của trang 既存友だち用\n"
       "- Friend được gắn tag TO",
       env="PRODUCTION",
       note="Nguồn: r160 (『check khi bot xóa friend → friend send ảnh cho bot => hiển thị friend "
            "lên tool mình → có send msg cho line user』). TC gốc dùng ảnh; đã tách theo loại nội "
            "dung ở TC kế tiếp."),

    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Bot đã xóa friend, friend gửi ảnh / file / sticker — vẫn hiện lên tool như bạn cũ",
       BASE_OLD,
       "1. Ở admin, xóa friend test ở màn chi tiết friend\n"
       "2. Dùng tài khoản LINE test gửi lần lượt: 1 ảnh, 1 file, 1 sticker cho bot\n"
       "3. Sau mỗi loại: về admin kiểm tra màn danh sách bạn bè và chat 1:1\n"
       "4. Kiểm tra tin nhắn chào mừng phía friend",
       "3 loại nội dung: ảnh · file · sticker (và tin nhắn text ở TC trước)",
       "- Cả 3 loại đều làm friend hiện lại trên tool\n"
       "- Nội dung friend gửi hiển thị đúng ở chat 1:1 (không mất, không lỗi hiển thị)\n"
       "- Cấu hình trang 既存友だち用 chạy giống nhau ở cả 3 loại",
       env="PRODUCTION",
       note="Nguồn: r160, r161, r162 (『friend send file』/『friend nhắn tin, gửi stamp』— cột kết "
            "quả mong đợi TRỐNG, expected suy từ r160). Gộp 3 loại vì cùng 1 kết quả. "
            "Cần Leader xác nhận."),

    tc("Kết bạn cũ — gửi tin & action", "MSG-USER-001", "Normal",
       "Friend cũ kết bạn qua link item / link đặt lịch — vẫn chạy cấu hình 既存友だち用",
       BASE_OLD,
       "1. Đưa friend test về trạng thái bạn cũ (xóa follow)\n"
       "2. Trang 既存友だち用 cài tin nhắn + action, bấm 保存\n"
       "3. Dùng tài khoản LINE test click link 商品販売 (item) dẫn tới kết bạn\n"
       "4. Kiểm tra tin nhắn và action nhận được\n"
       "5. Lặp lại bằng link đặt lịch salon / lesson",
       "2 đường vào: link item · link booking salon-lesson",
       "- Cả 2 đường đều chạy cấu hình của trang 既存友だち用\n"
       "- Friend nhận đúng tin nhắn và action của bạn cũ",
       env="PRODUCTION",
       note="Nguồn: r398 (『Friend Click link item => Kết bạn』) và r405 (『Friend Click link "
            "booking salon-lesson => Kết bạn』, cột expected TRỐNG). Đóng góc LIFF-ENTRY-001 "
            "(nhiều điểm vào). Cần Leader xác nhận cho đường link booking."),

    # ═══════════ 14. Hủy chặn — gửi tin & action ═══════════
    tc("Hủy chặn — gửi tin & action", "MSG-003", "Normal",
       "Friend bỏ block trên app LINE — nhận đúng tin nhắn của trang ブロック解除時用",
       BASE_UNB,
       "1. Trang ブロック解除時用 lưu tin nhắn「chao unblock」+ 1 action gắn tag TU, bấm 保存\n"
       "2. Dùng tài khoản LINE test đang block bot: bỏ block trên app LINE (chờ ~10 giây sau khi "
       "block như hướng dẫn tab テスト方法)\n"
       "3. Đọc tin nhắn nhận được trên app LINE\n"
       "4. Về admin kiểm tra tag của friend và màn chat 1:1",
       "Tin nhắn: 「chao unblock」· action gắn tag TU",
       "- Friend nhận đúng「chao unblock」\n"
       "- Friend được gắn tag TU\n"
       "- KHÔNG nhận tin của trang 新規友だち用 hay 既存友だち用\n"
       "- Màn chat 1:1 không còn hiển thị trạng thái đang bị block",
       env="PRODUCTION",
       note="Nguồn: r286 (『check line user sau khi unblock → hiển thị đúng msg khi setting』), "
            "r327, r328."),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Normal",
       "Tin nhắn trang ブロック解除時用 có biến {name} — hiển thị đúng tên friend",
       BASE_UNB,
       "1. Trang ブロック解除時用: chèn「＋ LINE名」vào tin nhắn, bấm 保存\n"
       "2. Dùng tài khoản LINE test bỏ block\n"
       "3. Đọc tin nhắn trên app LINE và ở màn chat 1:1",
       "Tin nhắn: 「{name}さん、おかえりなさい」",
       "- Cả app LINE và màn chat 1:1 hiển thị tên LINE thật của friend, không còn chuỗi {name}",
       env="PRODUCTION",
       note="Nguồn: r292, r328."),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Abnormal",
       "Bot chủ động block friend — KHÔNG chạy action chào mừng",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang ブロック解除時用 đã cài tin nhắn + action gắn tag TU\n"
       "- Có 1 friend đang là bạn bình thường của bot",
       "1. Ở admin, dùng chức năng block friend từ phía bot (màn chi tiết friend / chat 1:1)\n"
       "2. Quan sát tin nhắn phía friend trên app LINE\n"
       "3. Kiểm tra tag của friend",
       "Bot block friend (không phải friend block bot)",
       "- Friend KHÔNG nhận tin nhắn chào mừng nào\n"
       "- KHÔNG bị gắn tag TU\n"
       "- Không phát sinh action nào của FA-007",
       env="PRODUCTION",
       note="Nguồn: r296 (『check khi bot block friend → không send action』)."),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Abnormal",
       "Bot bỏ block friend từ phía admin — KHÔNG chạy action của trang ブロック解除時用",
       "- Bot đã liên kết LINE OA thật\n"
       "- Trang ブロック解除時用 đã cài tin nhắn + action gắn tag TU\n"
       "- Có 1 friend đang bị BOT block",
       "1. Ở admin, bỏ block friend từ phía bot\n"
       "2. Quan sát tin nhắn phía friend trên app LINE\n"
       "3. Kiểm tra tag của friend",
       "Bot unblock friend (thao tác từ admin, không phải friend bỏ block)",
       "- Friend KHÔNG nhận tin nhắn chào mừng\n"
       "- KHÔNG bị gắn tag TU",
       env="PRODUCTION",
       note="Nguồn: r297 (『khi bot unblock friend → không send action』). Đây là điểm dễ nhầm: "
            "chỉ hành động BỎ BLOCK TỪ PHÍA LINE USER mới kích hoạt cấu hình unblock."),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Abnormal",
       "Friend bị bot block rồi kết bạn lại — chạy nhánh nào?",
       "- Bot đã liên kết LINE OA thật\n"
       "- Cả 3 trang đều cài tin nhắn khác nhau: 新規=「M1」· 既存=「M2」· unblock=「M3」\n"
       "- Có 1 friend đang bị BOT block",
       "1. Cài đủ 3 trang, bấm 保存\n"
       "2. Ở admin bỏ block friend\n"
       "3. Dùng tài khoản LINE test đó gửi tin nhắn cho bot\n"
       "4. Đọc tin nhắn friend nhận được",
       "3 nội dung khác nhau (M1/M2/M3)",
       "- Ghi lại chính xác friend nhận nội dung nào\n"
       "- Kết quả phải NHẤT QUÁN qua nhiều lần lặp (không lúc M2 lúc M3)",
       env="PRODUCTION",
       note="TC do AI bổ sung — corpus và spec đều KHÔNG mô tả nhánh này (bot block ≠ friend "
            "block). job-spec.md §Bước 1 chỉ phân loại theo trạng thái bị block của friend. "
            "CẦN LEADER CHỐT hành vi đúng.",
       spec="Đã hỏi leader"),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Boundary",
       "Block rồi bỏ block QUÁ NHANH (dưới 10 giây) — có còn chạy cấu hình ブロック解除時用 không?",
       BASE_UNB,
       "1. Trang ブロック解除時用 cài tin nhắn「U-msg」+ tag TU, bấm 保存\n"
       "2. Friend block bot rồi bỏ block NGAY (dưới 3 giây) → ghi lại tin nhận\n"
       "3. Lặp lại với khoảng cách đúng 10 giây → ghi lại\n"
       "4. Lặp lại với khoảng cách 30 giây → ghi lại\n"
       "5. So sánh 3 lần",
       "3 mốc khoảng cách block → unblock: < 3 giây · 10 giây · 30 giây",
       "- Mốc 10 giây và 30 giây: friend nhận「U-msg」và được gắn tag TU\n"
       "- Mốc < 3 giây: ghi lại chính xác kết quả — nếu KHÔNG chạy thì đây là lý do vì sao hướng "
       "dẫn ở tab テスト方法 yêu cầu chờ ~10 giây, và phải ghi vào spec",
       env="PRODUCTION",
       note="TC do AI bổ sung theo FUNC-DATE-001/RULE-01 (Boundary). Căn cứ: tab「Improve setting "
            "add fr 1.0」r9 và r18 ghi『ブロック→ブロック解除操作は10秒間ほど間をおいて行なって"
            "ください』— tức đã biết có ngưỡng thời gian nhưng chưa ai test sát ngưỡng. "
            "CẦN LEADER CHỐT.",
       spec="Đã hỏi leader"),

    tc("Hủy chặn — gửi tin & action", "MSG-003", "Normal",
       "Friend bỏ block rồi lại block rồi bỏ block lần nữa — mỗi lần bỏ block đều chạy cấu hình",
       BASE_UNB,
       "1. Trang ブロック解除時用 cài tin nhắn「M3」, bấm 保存\n"
       "2. Friend bỏ block lần 1 → ghi lại tin nhận được\n"
       "3. Friend block lại bot, chờ ~10 giây\n"
       "4. Friend bỏ block lần 2 → ghi lại tin nhận được\n"
       "5. Lặp thêm lần 3",
       "3 vòng block → unblock, mỗi vòng cách nhau ≥10 giây",
       "- Cả 3 lần bỏ block friend đều nhận「M3」\n"
       "- Không lần nào bị bỏ sót, không lần nào nhận 2 tin",
       env="PRODUCTION",
       note="TC do AI bổ sung. Corpus có r288 nói『unblock lần 2 (không quét qr) → không send』"
            "NHƯNG đó là trong bối cảnh kết bạn qua QRコードアクション có giới hạn 1 lần — "
            "khác hoàn toàn case unblock thuần. CẦN LEADER CHỐT.",
       spec="Đã hỏi leader"),
]
