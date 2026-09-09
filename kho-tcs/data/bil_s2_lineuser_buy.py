# -*- coding: utf-8 -*-
"""FA-026 商品販売 — Nhóm 11-16: Luồng LINE user mua hàng.

Nguồn chính: 12. TCsLine_Item / tab「test fix bug」(Bug #31068 — 5 điểm mở link × 4 môi trường,
07/2025 → 02/2026, khối lớn nhất của corpus) và tab「Quản lý sản phẩm」r262-r331.
Bổ sung: tab「Improve bill tiền stripe」(Bug KH #35992 tồn kho, 04/2026 — mới nhất),
         tab「improve bill tiền 3D secure」, tab「Improve bill tiền univapay」(Bug KH #36443).
"""
from _common import tc

FR = "- Friend F1 đã kết bạn với bot A, chưa từng mua SP\n- SP là 単品商品 テスト環境, đã setting đủ 4 trang"
FRC = "- Friend F1 đã kết bạn với bot A\n- SP-C là 継続商品 テスト環境, đã setting đủ 5 trang"

S2 = [
    # ══════ 11. LINE user — mở trang mua ══════
    tc("LINE user — mở trang mua", "LIFF-ENTRY-001", "Normal",
       "Mở 商品ページ từ BUTTON của template — đã lấy được line id → nút mua enable",
       FR + "\n- Đã tạo template có button gắn action mở link 商品ページ của SP",
       "1. Bot gửi template chứa button cho F1\n2. F1 bấm button trên LINE app\n"
       "3. Quan sát trang sản phẩm và nút mua\n4. Bấm nút mua",
       "SP 単品, link type=product-detail",
       "- Trang mở đúng sản phẩm, hiện đủ setting đã cấu hình ở màn quản lý (ảnh, giá, nội dung, nhãn nút)\n"
       "- Nút mua ở trạng thái ENABLE với đúng màu đã setting\n- Bấm mua chuyển sang trang 友だち情報 bình thường",
       note="Nguồn: test fix bug r93 (Bug #31068). Đây là 1 trong 5 điểm mở link."),

    tc("LINE user — mở trang mua", "LIFF-ENTRY-001", "Abnormal",
       "Mở 商品ページ từ BUTTON — CHƯA lấy được line id → nút mua bị disable đúng màu, KHÔNG redirect về chat",
       FR + "\n- Mô phỏng LIFF trả line id chậm (throttle network / chặn tạm EP-88)",
       "1. F1 bấm button mở 商品ページ\n2. Ngay khi trang vừa hiện, quan sát nút mua và bấm thử vào nút\n"
       "3. Reload lại link khi vẫn chưa lấy được line id\n4. Sau khi line id về, quan sát lại nút mua",
       "Trạng thái chưa có line id",
       "- Nút mua DISABLE với nền #F0F0F0 và chữ #222222\n"
       "- Bấm vào nút disable: KHÔNG xảy ra thao tác gì, KHÔNG bị redirect về màn chat 1:1\n"
       "- Sau reload mà vẫn chưa có line id: nút vẫn disable\n"
       "- Khi line id về: nút chuyển sang enable đúng màu đã setting",
       note="Nguồn: test fix bug r97-r101 (Bug #31068 — nguyên nhân: click nút mua khi chưa kịp load line id "
            "từ LIFF nên bị về màn chat). Chuỗi thao tác liên tiếp không tách rời → giữ chung 1 TC."),

    tc("LINE user — mở trang mua", "LIFF-ENTRY-001", "Normal",
       "Nút mua có ĐỔI MÀU tùy chỉnh — lúc disable vẫn dùng màu spec, sau khi load dùng màu setting",
       FR + "\n- SP có setting màu nút mua tùy chỉnh (nền #0000FF, chữ #FFFF00)",
       "1. F1 mở 商品ページ, quan sát nút ngay lúc đầu (chưa có line id)\n2. Chờ line id về, quan sát lại nút",
       "Màu setting: nền #0000FF / chữ #FFFF00",
       "- Lúc chưa có line id: nút nền #F0F0F0, chữ #222222 (KHÔNG dùng màu setting)\n"
       "- Sau khi có line id: nút chuyển về đúng nền #0000FF, chữ #FFFF00",
       note="Nguồn: test fix bug r101「check có edit màu ở btn 1」."),

    tc("LINE user — mở trang mua", "CONC-001", "Abnormal",
       "Double click nút mua → chặn event, KHÔNG tạo đơn trùng",
       FR,
       "1. F1 mở 商品ページ, chờ nút enable\n2. Double click thật nhanh vào nút mua (interval < 500ms)\n"
       "3. Hoàn tất luồng mua\n4. Mở 販売履歴 đếm số đơn của F1 cho SP này",
       "Double click < 500ms",
       "- Chỉ có ĐÚNG 1 đơn được tạo\n- KHÔNG có 2 request thanh toán (verify bằng Network tab)\n"
       "- Action「申込完了時」chỉ gửi 1 lần",
       note="Nguồn: test fix bug r96 + Improve bill tiền stripe r85「Mua sucess, chỉ tạo 1 order」"
            "+ Improve bill tiền univapay r299/r312."),

    tc("LINE user — mở trang mua", "LIFF-ENTRY-001", "Normal",
       "Mở 商品ページ từ IMAGE MAP · RICH MENU · LINK trực tiếp · QUÉT MÃ QR → hành vi giống nhau",
       FR + "\n- Đã cấu hình 4 điểm vào: image map · rich menu · link dán trực tiếp trong tin nhắn · mã QR",
       "1. Lần lượt mở 商品ページ từ 4 điểm vào\n2. Ở mỗi điểm: quan sát nút mua khi có/chưa có line id\n"
       "3. Bấm mua và hoàn tất tới bước 友だち情報",
       "4 điểm vào: image map · rich menu · link · QR",
       "- Cả 4 điểm cho kết quả GIỐNG NHAU: trang mở đúng sản phẩm, hiện đủ setting, "
       "nút disable đúng màu khi chưa có line id, enable đúng màu setting khi đã có, bấm mua đi tiếp bình thường",
       note="Nguồn: test fix bug r102-r117 (image map, rich menu), r118-r122 (link), r154-r158 (QR). "
            "4 điểm vào cùng 1 kết quả → giữ chung 1 TC liệt kê đủ điểm ở cột Dữ liệu test."),

    tc("LINE user — mở trang mua", "FRIEND-001", "Normal",
       "Mở link 商品ページ khi CHƯA kết bạn → hiện trang add friend trước, kết bạn xong vào được trang mua",
       "- Tài khoản LINE F2 CHƯA kết bạn với bot A\n- SP là 単品商品 テスト環境",
       "1. F2 mở link 商品ページ trong LINE app\n2. Quan sát màn hình đầu tiên\n"
       "3. Bấm kết bạn\n4. Quan sát màn hình sau khi kết bạn thành công\n5. Hoàn tất mua sản phẩm",
       "F2 chưa kết bạn",
       "- Bước 2: hiện trang kết bạn (add friend) TRƯỚC, không hiện trang sản phẩm\n"
       "- Bước 4: tự động chuyển sang trang mua sản phẩm (KHÔNG về màn chat 1:1)\n"
       "- Bước 5: mua được bình thường, action「商品ページ表示時」có gửi",
       note="Nguồn: test fix bug r123 + r127-r128. Cột「Output thực tế」r123 ghi hiện tượng cũ: "
            "「Khi nhấn button mua mới redirect đến trang kết bạn... Nhấn kết bạn xong thì back về màn hình chat」."),

    tc("LINE user — mở trang mua", "FRIEND-001", "Abnormal",
       "Chưa kết bạn → sau khi bấm add friend mà chưa lấy được line id → nút disable, KHÔNG về màn chat",
       "- Tài khoản LINE F2 CHƯA kết bạn với bot A",
       "1. F2 mở link 商品ページ → bấm nút add friend\n"
       "2. Ngay khi về trang sản phẩm (chưa có line id), quan sát nút mua và bấm vào nút\n"
       "3. Reload lại link, nếu vẫn chưa có line id thì bấm tiếp vào nút disable",
       "F2 vừa kết bạn, line id chưa về",
       "- Nút mua DISABLE nền #F0F0F0 chữ #222222\n"
       "- Bấm nút disable: KHÔNG bị redirect về màn chat 1:1\n- Reload: vẫn disable, vẫn không về màn chat",
       note="Nguồn: test fix bug r124-r126."),

    tc("LINE user — mở trang mua", "FRIEND-002", "Normal",
       "OLD FRIEND (đã kết bạn từ trước khi bot vào tool) mở link mua → tự động add vào tool và mua được",
       "- Tài khoản LINE F3 đã kết bạn với OA từ TRƯỚC khi bot được thêm vào LME (chưa có bot_line_user)",
       "1. F3 mở link 商品ページ trên LINE app\n2. Quan sát nút mua\n3. Hoàn tất luồng mua\n"
       "4. Kiểm tra F3 đã xuất hiện ở danh sách bạn bè trong tool chưa",
       "F3 = old friend chưa có trong tool",
       "- F3 được tự động add vào tool\n- Nút mua enable\n- Đi tiếp được các bước và mua thành công\n"
       "- F3 xuất hiện ở danh sách bạn bè của bot A",
       note="Nguồn: test fix bug r129 / r141 / r153 / r165. Liên quan SpecImprove #34533 (improve performance "
            "check kết bạn old friend, 02/2026)."),

    tc("LINE user — mở trang mua", "FRIEND-002", "Abnormal",
       "OLD FRIEND mở link ĐỔI THẺ / HỦY khi chưa từng mua → báo lỗi 未購入",
       "- Tài khoản LINE F3 = old friend, chưa có bot_line_user_item cho SP-C\n- SP-C là 継続商品",
       "1. F3 mở link type=product-change của SP-C\n2. Quan sát màn hình\n"
       "3. F3 mở link type=product-cancel của SP-C",
       "F3 chưa từng mua SP-C",
       "- Cả 2 link đều hiện màn thông báo lỗi「この商品は購入されていません。」\n"
       "- F3 vẫn được tự động add vào tool",
       note="Nguồn: test fix bug r206-r207 / r220-r221 / r234-r235 / r248-r249. "
            "Spec §2.5 bảng status_contract = 0 unregister."),

    tc("LINE user — mở trang mua", "COMPAT-001", "Normal",
       "Mở 商品ページ trên trình duyệt ngoài LINE app (Safari / Chrome) → hành vi giống trong app",
       FR,
       "1. Copy link 商品ページ, mở bằng Safari trên iPhone\n2. Quan sát nút mua khi chưa/đã có line id\n"
       "3. Hoàn tất mua\n4. Lặp lại toàn bộ bằng Chrome",
       "Safari (iOS) · Chrome",
       "- Cả Safari và Chrome: trang mở đúng, nút disable/enable đúng quy tắc, mua được thành công, "
       "action gửi bình thường",
       note="Nguồn: test fix bug r130-r141 (safari) + r142-r153 (chrome). 2 trình duyệt cùng 1 kết quả → 1 TC."),

    tc("LINE user — mở trang mua", "STATE-001", "Abnormal",
       "Mở link MUA MỚI khi đơn đang chờ webhook (status_webhook 0/3/4) → chặn với message riêng",
       FRC + "\n- F1 đã có hợp đồng SP-C ở trạng thái đang chờ kết quả thanh toán (status_webhook ∈ {0,3,4})",
       "1. F1 mở link type=product-detail của SP-C\n2. Đọc thông báo hiển thị",
       "status_webhook = 3 (và lặp lại với 0, 4)",
       "- Hiện lỗi「決済処理を行っていますので、操作できません。」\n"
       "- KHÔNG cho mua tiếp, KHÔNG tạo đơn mới",
       note="Nguồn: Improve bill tiền univapay r159-r161. Spec BR-14."),

    tc("LINE user — mở trang mua", "STATE-001", "Abnormal",
       "Mở link MUA MỚI khi đã có hợp đồng đang chạy → báo「申込済みの商品です」",
       FRC + "\n- F1 đã mua SP-C, hợp đồng status_bill = 1, status_webhook ∈ {NULL, 1, 2}",
       "1. F1 mở link type=product-detail của SP-C\n2. Đọc thông báo",
       "status_bill = 1 · status_webhook = 1",
       "- Hiện thông báo「申込済みの商品です」\n- Không cho mua lại",
       note="Nguồn: Improve bill tiền univapay r157-r158 + r162."),

    tc("LINE user — mở trang mua", "STATE-001", "Normal",
       "Mở link MUA MỚI sau khi hợp đồng ĐÃ HỦY (status_bill = 3) → cho mua lại",
       FRC + "\n- F1 đã mua SP-C rồi hủy hợp đồng (status_bill = 3)",
       "1. F1 mở link type=product-detail của SP-C\n2. Hoàn tất mua lại",
       "status_bill = 3",
       "- Trang mua mở bình thường\n- Mua lại thành công, tạo hợp đồng MỚI",
       note="Nguồn: Improve bill tiền univapay r163「cho phép mua mới」."),

    tc("LINE user — mở trang mua", "PERM-002", "Abnormal",
       "Bot HẾT HẠN hợp đồng LME quá 7 ngày → chặn trang mua (route 410)",
       "- Bot B có plan_type = 1, expired_date đã quá hạn > 7 ngày\n- SP-B thuộc bot B",
       "1. Friend mở link 商品ページ của SP-B\n2. Quan sát màn hình trả về",
       "expired_date = hôm nay − 10 ngày",
       "- Trang mua KHÔNG mở được, trả về màn 410 (hết hạn)\n- Không tạo được đơn",
       note="Suy luận của AI từ spec §2.4「CHẶN bot hết hạn: plan_type==1 && (expired_date+7d < now || "
            "bot_contract.status==3) → route('410')」. Corpus KHÔNG có TC này. CẦN LEADER XÁC NHẬN nội dung màn 410."),

    tc("LINE user — mở trang mua", "PERM-002", "Abnormal",
       "Friend đã BLOCK bot → mở link 商品ページ bị redirect sang trang kết bạn",
       "- Friend F4 đã block bot A (bot_line_user ở trạng thái block)",
       "1. F4 mở link 商品ページ của SP\n2. Quan sát màn hình",
       "F4 block bot A",
       "- Bị redirect sang URL kết bạn của bot (bots.url_add_friend), không vào được trang mua",
       note="Suy luận của AI từ spec §2.4「bot_line_user không tồn tại/bị block → redirect bots.url_add_friend」. "
            "Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN."),

    tc("LINE user — mở trang mua", "STATE-001", "Abnormal",
       "Sản phẩm đã bị XÓA / không tồn tại → hiện thông báo không công khai",
       "- Ghi lại link 商品ページ của SP-DEL rồi xóa SP-DEL ở màn quản lý",
       "1. Friend mở link 商品ページ của SP-DEL\n2. Đọc thông báo",
       "product_id không còn tồn tại",
       "- Hiện「商品が非公開か、存在していません」\n- Không lỗi 500",
       note="Suy luận của AI từ spec §2.4 EP-60. Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN text."),

    # ══════ 12. LINE user — nhập friend info ══════
    tc("LINE user — nhập friend info", "UI-001", "Normal",
       "Thứ tự và nhãn các mục 友だち情報 phía LINE khớp đúng setting ở wizard bước 2",
       FR + "\n- SP có 5 mục 友だち情報: お名前 · メールアドレス · 電話番号 · 住所 · 備考 (theo thứ tự này)",
       "1. F1 mở 商品ページ → bấm mua → tới trang 友だち情報\n2. Đối chiếu thứ tự, nhãn, dấu 必須 của 5 mục",
       "5 mục theo thứ tự đã setting",
       "- Hiện đúng 5 mục theo đúng thứ tự và nhãn đã setting\n"
       "- Mục 必須 có đánh dấu bắt buộc, mục 任意 không có",
       note="Nguồn: Quản lý sản phẩm r279 mục 1「check thứ tự friend infor đúng theo thứ tự ở setting hay chưa」."),

    tc("LINE user — nhập friend info", "FUNC-001", "Normal",
       "Nhập được đủ các kiểu mục: text 1 dòng · text nhiều dòng · select",
       FR + "\n- SP có 3 mục tùy chỉnh: 1 text 1 dòng, 1 text nhiều dòng, 1 select 3 lựa chọn",
       "1. F1 vào trang 友だち情報\n2. Nhập giá trị cho cả 3 kiểu mục\n3. Bấm sang bước tiếp\n"
       "4. Hoàn tất mua rồi mở 注文詳細 phía admin",
       "Text 1 dòng「東京」· nhiều dòng「1行目\\n2行目」· select「選択肢B」",
       "- Nhập được cả 3 kiểu\n- Sang bước tiếp bình thường\n"
       "- 注文詳細 khối 友だち情報 hiện đủ 3 giá trị đúng như đã nhập (kể cả xuống dòng)",
       note="Nguồn: r279 mục 2."),

    tc("LINE user — nhập friend info", "FUNC-VALID-001", "Abnormal",
       "Validate theo kiểu dữ liệu: kana · kiểu số · số điện thoại · email",
       FR + "\n- SP có 4 mục với 4 kiểu validate: kana, số, số điện thoại, email",
       "1. F1 vào trang 友だち情報\n2. Nhập sai định dạng cho từng mục (kana nhập latinh, số nhập chữ, "
       "số đt nhập chữ, email thiếu @) → bấm sang bước tiếp\n3. Sửa lại đúng định dạng → bấm sang bước tiếp",
       "Sai: kana=「abc」· số=「abc」· đt=「abcd」· mail=「test.com」\nĐúng: 「ヤマダ」·「123」·「09012345678」·「t@example.com」",
       "- Nhập sai: hiện lỗi tại đúng ô, KHÔNG cho sang bước tiếp\n"
       "- Sửa đúng: sang bước tiếp bình thường",
       note="Nguồn: r279 mục 3「check validate data (kana, kiểu số, số đt, mail..)」."),

    tc("LINE user — nhập friend info", "FUNC-VALID-001", "Abnormal",
       "Bỏ trống mục 必須 → không cho sang bước tiếp",
       FR + "\n- SP có mục「お名前」và「メールアドレス」đều 必須",
       "1. F1 vào trang 友だち情報\n2. Để trống お名前 → bấm sang bước tiếp\n"
       "3. Nhập お名前, để trống メールアドレス → bấm sang bước tiếp\n4. Nhập đủ cả 2 → bấm sang bước tiếp",
       "Lần 1: お名前 rỗng · lần 2: mail rỗng · lần 3: đủ",
       "- Lần 1 và 2: báo lỗi bắt buộc nhập tại đúng ô, không sang bước tiếp\n- Lần 3: sang bước tiếp bình thường",
       note="Suy luận của AI từ spec (b_c_info_setting.is_require, 2 mục mặc định luôn 必須). "
            "Corpus không tách case này. CẦN LEADER XÁC NHẬN text lỗi."),

    tc("LINE user — nhập friend info", "INTG-001", "Normal",
       "PREFILL từ hồ sơ bạn bè: mục có liên kết friend info và friend đã có value → tự điền sẵn",
       FR + "\n- SP có mục liên kết với 1 friend info kiểu text\n- F1 ĐÃ có giá trị「既存の値」ở friend info đó",
       "1. F1 mở 商品ページ → bấm mua → tới trang 友だち情報\n2. Quan sát ô của mục có liên kết",
       "friend_information_value của F1 =「既存の値」",
       "- Ô đó tự điền sẵn「既存の値」\n- F1 vẫn sửa được giá trị trước khi đi tiếp",
       note="Nguồn: r279 mục 4「case có setting map với friend infor, khi mua nếu user đã có value thì hiện theo value đó」."),

    tc("LINE user — nhập friend info", "INTG-001", "Normal",
       "PREFILL từ trường hệ thống: システム表示名 · 携帯電話 · メールアドレス · 都道府県",
       FR + "\n- SP có 4 mục liên kết lần lượt tới 4 trường hệ thống (friend_info_id = −1 / −2 / −3 / −6)\n"
       "- F1 đã có sẵn giá trị cho cả 4 trường hệ thống",
       "1. F1 tới trang 友だち情報\n2. Đối chiếu 4 ô với giá trị hiện có ở màn 友だち詳細 của F1\n"
       "3. Riêng mục 都道府県: mở dropdown đếm số lựa chọn",
       "システム表示名「山田」· 携帯「09012345678」· mail「t@example.com」· 都道府県「東京都」",
       "- Cả 4 ô đều tự điền đúng giá trị hiện có của F1\n- Dropdown 都道府県 có đủ 47 đô-đạo-phủ-huyện",
       note="Suy luận của AI từ spec §2.4 SCR-BIL-23 + Field Matrix #23. Corpus chỉ nói chung ở r279 mục 4. "
            "Con số 47 lấy từ spec — CẦN LEADER XÁC NHẬN."),

    tc("LINE user — nhập friend info", "INTG-001", "Normal",
       "Sau khi mua thành công → giá trị đã nhập được ghi vào friend_information_value",
       FR + "\n- SP có mục liên kết friend info, F1 CHƯA có giá trị ở friend info đó",
       "1. F1 mua sản phẩm, nhập giá trị mới「新しい値」ở mục có liên kết\n2. Hoàn tất thanh toán thành công\n"
       "3. Mở màn 友だち詳細 của F1 xem friend info đó\n4. Mở 注文詳細 phía admin",
       "Giá trị nhập:「新しい値」",
       "- 友だち詳細 của F1: friend info đó = 「新しい値」\n- 注文詳細 khối 友だち情報 cũng hiện「新しい値」",
       note="Nguồn: r279 mục 5「sau khi mua thành công có update friend_infor_value chưa」+ r58."),

    tc("LINE user — nhập friend info", "UI-001", "Normal",
       "Trang 友だち情報 継続商品 — có ô nhập coupon code (nếu có setting)",
       FRC,
       "1. F1 mở link mua SP-C → tới trang 友だち情報\n2. Quan sát có/không ô coupon code\n"
       "3. Nếu có: nhập mã hợp lệ và mã không hợp lệ",
       "Mã hợp lệ / mã sai",
       "- Ghi lại kết quả THẬT: ô coupon có xuất hiện không, mã hợp lệ có giảm giá không, "
       "mã sai có báo lỗi không",
       note="Nguồn: r303「coupon code」— tester ghi「Cần Comfirm」, TC gốc chỉ có tiêu đề và CHƯA có kết luận. "
            "Spec-features KHÔNG nhắc tới coupon ở FA-026 → MT-10, CẦN LEADER QUYẾT có nằm trong phạm vi không."),

    # ══════ 13. LINE user — nhập thẻ & 3D Secure ══════
    tc("LINE user — nhập thẻ & 3D Secure", "FUNC-VALID-001", "Abnormal",
       "Nhập số thẻ SAI định dạng → báo lỗi tại màn nhập thẻ",
       FR + "\n- SP dùng cổng Stripe, môi trường テスト",
       "1. F1 tới trang nhập thẻ\n2. Nhập số thẻ thiếu chữ số / ký tự chữ → bấm sang bước tiếp",
       "Số thẻ「4242 4242 4242」(thiếu số) và「abcd」",
       "- Báo lỗi định dạng thẻ ngay tại màn nhập, không sang bước tiếp",
       note="Nguồn: r280「check nhập số card sai」."),

    tc("LINE user — nhập thẻ & 3D Secure", "ENV-002", "Abnormal",
       "Nhập thẻ SAI MÔI TRƯỜNG (sản phẩm 本番 nhưng nhập thẻ test và ngược lại) → báo lỗi",
       "- SP-P là sản phẩm 本番環境, SP-T là sản phẩm テスト環境, cùng bot A",
       "1. Mua SP-P, nhập số thẻ test 4242 4242 4242 4242 → xác nhận mua\n"
       "2. Mua SP-T, nhập số thẻ THẬT → xác nhận mua",
       "Thẻ test: 4242 4242 4242 4242 · thẻ thật",
       "- Cả 2 trường hợp đều BÁO LỖI, không tạo đơn thành công\n"
       "- Không bị trừ tiền ở trường hợp 2",
       env="PRODUCTION",
       note="Nguồn: r282「check nhập card sai môi trường (product nhưng nhập card test và ngược lại) => báo lỗi」. "
            "RULE-08: bill tiền test trên PRODUCTION."),

    tc("LINE user — nhập thẻ & 3D Secure", "SEC-001", "Normal",
       "Thẻ 3D Secure cần xác thực MỌI giao dịch → hiện popup 3DS, bấm complete thì mua thành công",
       FR + "\n- SP dùng Stripe, môi trường テスト",
       "1. F1 tới trang nhập thẻ, nhập 4000 0000 0000 3220 → xác nhận\n2. Quan sát popup 3DS\n"
       "3. Bấm complete trên popup\n4. Mở 注文詳細 phía admin + dashboard Stripe (tra theo charge id)",
       "Thẻ 4000 0000 0000 3220",
       "- Hiện popup 3D Secure\n- Bấm complete: popup đóng, mua thành công\n"
       "- 注文詳細 hiện đơn 決済成功\n- Trên Stripe tra theo charge id thấy giao dịch thành công tương ứng",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r3 + r6."),

    tc("LINE user — nhập thẻ & 3D Secure", "SEC-001", "Abnormal",
       "Popup 3DS bấm CANCEL hoặc FAIL → đóng popup, báo lỗi, quay về màn nhập thẻ và XÓA thông tin thẻ đã nhập",
       FR,
       "1. F1 nhập thẻ 4000 0000 0000 3220 → xác nhận → popup 3DS hiện\n"
       "2. Bấm cancel trên popup → quan sát màn hình và các ô nhập thẻ\n"
       "3. Lặp lại và bấm fail trên popup",
       "Thẻ 4000 0000 0000 3220 · thao tác cancel / fail",
       "- Cả 2 trường hợp: popup đóng, hiện message lỗi\n"
       "- Redirect về màn nhập thẻ\n- Các ô thông tin thẻ đã được XÓA TRẮNG (clear)\n- KHÔNG tạo đơn thành công",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r4-r5. 2 thao tác cùng 1 kết quả → giữ chung 1 TC."),

    tc("LINE user — nhập thẻ & 3D Secure", "SEC-001", "Normal",
       "Thẻ 3DS chỉ cần xác thực 1 LẦN (4000 0038 0000 0446) → lần đầu hiện popup, mua thành công",
       FR,
       "1. F1 nhập thẻ 4000 0038 0000 0446 → xác nhận\n2. Bấm complete trên popup 3DS\n"
       "3. Mở 注文詳細 + dashboard Stripe",
       "Thẻ 4000 0038 0000 0446",
       "- Hiện popup 3DS, complete xong mua thành công\n- Đơn ở trạng thái 決済成功\n"
       "- Tra được giao dịch tương ứng trên Stripe",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r7 + r10."),

    tc("LINE user — nhập thẻ & 3D Secure", "SEC-001", "Abnormal",
       "Thẻ decline (…1629) và thẻ error (…1280) → báo lỗi Your card was declined, nút confirm disable",
       FR,
       "1. F1 nhập thẻ 4000 0084 0000 1629 → xác nhận\n2. Quan sát màn hình và nút confirm\n"
       "3. Quay lại màn nhập thẻ, kiểm tra các ô\n4. Lặp lại với thẻ 4000 0084 0000 1280",
       "Thẻ 4000 0084 0000 1629 (decline) · 4000 0084 0000 1280 (error)",
       "- Cả 2 thẻ: báo lỗi「Your card was declined」\n- Vẫn ở màn xác nhận số tiền, nút confirm bị DISABLE\n"
       "- Back về màn nhập thẻ thì thông tin thẻ đã bị xóa trắng\n- Không tạo đơn thành công",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r11-r12 + r19-r20. 2 thẻ cùng 1 kết quả → 1 TC."),

    tc("LINE user — nhập thẻ & 3D Secure", "SEC-001", "Normal",
       "Thẻ KHÔNG hỗ trợ 3DS (AMEX 378282246310005) → không hiện popup, vẫn bill được",
       FR,
       "1. F1 nhập thẻ 378282246310005 → xác nhận\n2. Quan sát có popup 3DS không\n3. Mở 注文詳細",
       "Thẻ AMEX 378282246310005",
       "- KHÔNG hiện popup 3DS\n- Vẫn bill được, đơn ở trạng thái 決済成功",
       env="PRODUCTION",
       note="Nguồn: improve bill tiền 3D secure r14 / r22「ko support xác thực (vẫn bill được)」. "
            "⚠ r13-r14 ghi expected là「tbl b_user_booking.status_payment = 0」— sai bảng (b_user_booking là "
            "booking event). Expected đã được viết lại theo bảng đúng s_order_history → xem MT-11."),

    tc("LINE user — nhập thẻ & 3D Secure", "UI-001", "Normal",
       "Màn nhập thẻ hiện đúng các brand card đã tick ở màn liên kết bill tiền",
       FR + "\n- SP dùng UnivaPay\n- Ở màn setting liên kết bill tiền đã tick 3 loại brand card",
       "1. F1 tới màn nhập thẻ của SP (単品)\n2. Đối chiếu icon brand card hiển thị\n"
       "3. Lặp lại với SP-C (継続) ở màn mua mới và màn đổi thẻ",
       "3 brand card được tick",
       "- Cả 3 màn (単品 mua · 継続 mua · 継続 đổi thẻ) đều hiện ĐÚNG 3 brand card đã tick, không thừa không thiếu",
       note="Nguồn: Màn liên kết bill tiền r11-r13."),

    tc("LINE user — nhập thẻ & 3D Secure", "UI-001", "Normal",
       "KHÔNG tick brand card nào → màn nhập thẻ không hiện brand card",
       FR + "\n- Ở màn setting liên kết bill tiền đã BỎ TICK toàn bộ brand card (flag_brand_card_univapay = null)",
       "1. F1 tới màn nhập thẻ của SP (単品)\n2. Quan sát khu vực brand card\n"
       "3. Lặp lại với SP-C (継続) ở màn mua mới và màn đổi thẻ",
       "0 brand card được tick",
       "- Cả 3 màn đều KHÔNG hiện brand card nào",
       note="Nguồn: Màn liên kết bill tiền r17-r19. ListBug r5 ghi bug cũ: "
            "「case không setting loại card nào thì ở màn change card đang hiện 2 loại card visa và master」— regression"),

    # ══════ 14. LINE user — mua 単品 ══════
    tc("LINE user — mua 単品", "UI-001", "Normal",
       "Trang 商品ページ 単品 hiển thị đủ: ảnh · tên · giá · tồn kho · giới hạn mua · mô tả · nút mua · 特商法",
       FR + "\n- SP có ảnh, giá 1.000円, stock 10 (hiện), 購入上限 5 (hiện), đã nhập 商品案内",
       "1. F1 mở 商品ページ\n2. Đối chiếu từng mục với setting phía admin\n"
       "3. Bấm vào text thông tin cửa hàng",
       "SP: 1.000円 · stock còn 10 · 購入上限 5",
       "- Hiện đủ và đúng: ảnh sản phẩm · 表示商品名 · giá 1.000円 · tồn kho còn lại 10 · "
       "số lượng tối đa 1 người mua 5 · nội dung 商品案内 · nhãn nút mua theo setting\n"
       "- Bấm text thông tin cửa hàng: mở được trang 特定商取引法に基づく表記",
       note="Nguồn: r262-r278."),

    tc("LINE user — mua 単品", "FUNC-001", "Normal",
       "Ô chọn số lượng chỉ hiện khi BẬT tính năng tồn kho; default = 1",
       FR,
       "1. SP-A bật 在庫数 → F1 mở 商品ページ → quan sát ô chọn số lượng và giá trị mặc định\n"
       "2. SP-B tắt 在庫数 → F1 mở 商品ページ → quan sát\n3. Mua SP-B, mở 注文詳細 xem 購入個数",
       "SP-A: flag_use_stock=ON · SP-B: flag_use_stock=OFF",
       "- SP-A: CÓ ô chọn số lượng, giá trị mặc định = 1, nhập được\n"
       "- SP-B: KHÔNG có ô chọn số lượng\n- Đơn của SP-B có 購入個数 = 1",
       note="Nguồn: r272 + Improve bill tiền stripe r81/r86."),

    tc("LINE user — mua 単品", "FUNC-001", "Normal",
       "Mua 単品 số lượng = 1 → tạo 1 đơn, số tiền = giá sản phẩm",
       FR + "\n- SP giá 1.000円, Stripe, テスト環境",
       "1. F1 mở 商品ページ → chọn số lượng 1 → nhập 友だち情報 → nhập thẻ 4242 4242 4242 4242 → "
       "xác nhận ở màn 最終確認 → bấm 購入する\n2. Mở 販売履歴 単品 phía admin\n3. Mở 注文詳細 của đơn\n"
       "4. Mở dashboard Stripe tra theo charge id",
       "Giá 1.000円 × 1 = 1.000円",
       "- Đơn mới xuất hiện ở 販売履歴 với trạng thái 決済成功\n"
       "- 注文詳細: 購入個数 = 1, 決済金額（税込）= 1.000円\n"
       "- Trên Stripe có giao dịch 1.000円 thành công tương ứng\n"
       "- F1 nhận action「申込完了時」và notify「【bot】<line name> <tên item> が購入されました」",
       env="PRODUCTION",
       note="Nguồn: r284 + r286 + Improve bill tiền stripe r5. RULE-07 (verify DB + màn hình + output) và "
            "RULE-08 (bill tiền → PRODUCTION)."),

    tc("LINE user — mua 単品", "FUNC-001", "Normal",
       "Mua 単品 số lượng > 1 → 決済金額 = đơn giá × số lượng",
       FR + "\n- SP giá 1.000円, bật 在庫数 = 10, 購入上限 = 5",
       "1. F1 mua với số lượng = 3\n2. Mở 注文詳細 đọc 購入個数 và 決済金額\n"
       "3. Mở dashboard cổng thanh toán đối chiếu số tiền\n4. Xem cột 在庫数 ở list sản phẩm",
       "1.000円 × 3 = 3.000円",
       "- 注文詳細: 購入個数 = 3, 決済金額（税込）= 3.000円\n"
       "- Cổng thanh toán ghi nhận đúng 3.000円\n- Tồn kho còn lại giảm còn 7",
       env="PRODUCTION",
       note="Nguồn: r285 + r312. Công thức spec BR-05 (tổng = tiền kỳ đầu × số lượng)."),

    tc("LINE user — mua 単品", "PAY-001", "Normal",
       "Mua 単品 bằng Stripe và bằng UnivaPay đều thành công và ghi đúng cổng",
       FR + "\n- SP-S dùng Stripe, SP-U dùng UnivaPay, cùng giá 1.000円, cùng テスト環境",
       "1. F1 mua SP-S bằng thẻ test Stripe 4242 4242 4242 4242\n2. F1 mua SP-U bằng thẻ test UnivaPay\n"
       "3. Mở 販売履歴, đọc cột 決済システム của 2 đơn\n4. Bấm badge 決済ステータス của từng đơn",
       "Stripe: 4242 4242 4242 4242 · UnivaPay: thẻ test tương ứng",
       "- Cả 2 đơn đều 決済成功, số tiền 1.000円\n- Cột 決済システム hiện đúng Stripe / UnivaPay\n"
       "- Badge 決済ステータス là link mở đúng dashboard của cổng tương ứng",
       env="PRODUCTION",
       note="Nguồn: r286-r287 + test fix bug r166-r167 / r250-r251."),

    tc("LINE user — mua 単品", "FUNC-001", "Normal",
       "Màn 最終確認 hiển thị lại đúng toàn bộ thông tin đã nhập trước khi bấm mua",
       FR + "\n- SP có 5 mục 友だち情報",
       "1. F1 nhập đủ 5 mục 友だち情報 và thông tin thẻ\n2. Tới màn 最終確認\n"
       "3. Đối chiếu từng mục hiển thị với dữ liệu đã nhập\n4. Bấm back về sửa 1 mục rồi tiến lại 最終確認",
       "5 mục friend info + 4 số cuối thẻ",
       "- Màn 最終確認 hiện đủ 5 mục đúng như đã nhập + 4 số cuối thẻ + số tiền + nội dung ご確認事項\n"
       "- Sau khi back sửa 1 mục, màn 最終確認 hiện giá trị ĐÃ SỬA",
       note="Nguồn: r283 + r305-r306."),

    tc("LINE user — mua 単品", "PAY-002", "Abnormal",
       "Mua thất bại do thẻ bị từ chối → hiện message lỗi, KHÔNG tạo đơn thành công, KHÔNG gửi action",
       FR + "\n- SP dùng Stripe テスト環境, đã gắn action ở slot「申込完了時」",
       "1. F1 mua với thẻ fail 4000 0000 0000 0341 → bấm 購入する\n2. Quan sát màn hình phía LINE\n"
       "3. Mở 販売履歴 tìm đơn của F1\n4. Kiểm tra chat 1:1 của F1",
       "Thẻ 4000 0000 0000 0341",
       "- Phía LINE hiện message báo lỗi thanh toán\n"
       "- KHÔNG có đơn 決済成功 nào của F1 ở 販売履歴 (bản ghi tạm đã bị xóa)\n"
       "- F1 KHÔNG nhận action「申込完了時」\n"
       "- Admin nhận notify case bill fail「【bot】<line name> <tên item> の決済に失敗しました」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r7 + test fix bug r49 (Bug #26850 — sửa lại case bill lỗi khi mua thì không action)."),

    # ══════ 15. LINE user — mua 継続 ══════
    tc("LINE user — mua 継続", "UI-001", "Normal",
       "Nhãn giá 継続 — KHÔNG set giá kỳ đầu + KHÔNG giới hạn số lần bill →「お支払い価格」",
       FRC + "\n- SP-C: flag_first = 0, number_charge = 0 (無制限)",
       "1. F1 mở link mua SP-C\n2. Đọc nhãn của mục giá",
       "flag_first=0 · number_charge=0",
       "- Nhãn giá hiển thị「お支払い価格」\n- Mục số lần bill hiện「無制限」",
       note="Nguồn: r291."),

    tc("LINE user — mua 継続", "UI-001", "Normal",
       "Nhãn giá 継続 — KHÔNG set giá kỳ đầu + CÓ giới hạn 4 lần →「お支払い価格（1~4回目）」",
       FRC + "\n- SP-C: flag_first = 0, number_charge = 4",
       "1. F1 mở link mua SP-C\n2. Đọc nhãn của mục giá",
       "flag_first=0 · number_charge=4",
       "- Nhãn giá hiển thị「お支払い価格（1~4回目）」",
       note="Nguồn: r292."),

    tc("LINE user — mua 継続", "UI-001", "Normal",
       "Nhãn giá 継続 — CÓ set giá kỳ đầu + KHÔNG giới hạn →「お支払い価格（初回）」+「お支払い価格（2回目以降）」",
       FRC + "\n- SP-C: flag_first = 1 (amount_first = 500), number_charge = 0",
       "1. F1 mở link mua SP-C\n2. Đọc nhãn và giá trị của cả 2 dòng giá",
       "amount_first=500 · amount=3000 · number_charge=0",
       "- Dòng 1:「お支払い価格（初回）」= 500円\n- Dòng 2:「お支払い価格（2回目以降）」= 3.000円",
       note="Nguồn: r290 + r293."),

    tc("LINE user — mua 継続", "UI-001", "Normal",
       "Nhãn giá 継続 — CÓ set giá kỳ đầu + CÓ giới hạn 4 lần →「お支払い価格（2~4回目）」",
       FRC + "\n- SP-C: flag_first = 1 (amount_first = 500), number_charge = 4",
       "1. F1 mở link mua SP-C\n2. Đọc nhãn và giá trị của cả 2 dòng giá",
       "amount_first=500 · amount=3000 · number_charge=4",
       "- Dòng 1:「お支払い価格（初回）」= 500円\n- Dòng 2:「お支払い価格（2~4回目）」= 3.000円",
       note="Nguồn: r294."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 CÓ trial + CÓ giá kỳ đầu → bill đúng giá kỳ đầu, hạn = ngày mua + số ngày trial, status トライアル中",
       FRC + "\n- SP-C: trial 7 ngày, amount_first = 500, amount = 3.000",
       "1. F1 mua SP-C bằng thẻ hợp lệ, ngày mua = D\n2. Mở 注文詳細 của hợp đồng\n"
       "3. Đối chiếu dashboard cổng thanh toán\n4. Xem cột「トライアル中」ở list 継続",
       "trial 7 ngày · amount_first 500円 · ngày mua D",
       "- Số tiền đã bill = 500円 (khớp cả 注文詳細 và cổng thanh toán)\n"
       "- 次回決済予定日 = D + 7\n- Trạng thái =「トライアル中」\n- Cột トライアル中 của SP-C +1",
       env="PRODUCTION",
       note="Nguồn: r307. Spec BR-05 nhánh flag_trial=1 + flag_first=1 → amount_first."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 CÓ trial + KHÔNG giá kỳ đầu → bill 0円, hạn = ngày mua + trial, status トライアル中",
       FRC + "\n- SP-C: trial 7 ngày, flag_first = 0, amount = 3.000",
       "1. F1 mua SP-C bằng thẻ hợp lệ, ngày mua = D\n2. Mở 注文詳細\n"
       "3. Mở dashboard cổng thanh toán tra giao dịch",
       "trial 7 ngày · flag_first=0 · ngày mua D",
       "- Số tiền đã bill = 0円\n- 次回決済予定日 = D + 7\n- Trạng thái =「トライアル中」\n"
       "- Stripe: có SetupIntent (không có charge tiền); UnivaPay: có giao dịch trạng thái Authorized",
       env="PRODUCTION",
       note="Nguồn: r308 (tester nghi vấn「bill số tiền bt hay bill 0đ」) + r378/r390. Spec BR-05 nhánh cuối = 0."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 KHÔNG trial + CÓ giá kỳ đầu → bill giá kỳ đầu, hạn = ngày mua + 1 chu kỳ, status 継続中",
       FRC + "\n- SP-C: flag_trial = 0, amount_first = 500, amount = 3.000, chu kỳ 毎月",
       "1. F1 mua SP-C bằng thẻ hợp lệ, ngày mua = D\n2. Mở 注文詳細\n3. Đối chiếu cổng thanh toán",
       "flag_trial=0 · amount_first 500円 · chu kỳ 毎月 · ngày mua D",
       "- Số tiền đã bill = 500円\n- 次回決済予定日 = D + 1 tháng\n- Trạng thái =「継続中」",
       env="PRODUCTION",
       note="Nguồn: r309."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 KHÔNG trial + KHÔNG giá kỳ đầu → bill giá thường, hạn = ngày mua + 1 chu kỳ, status 継続中",
       FRC + "\n- SP-C: flag_trial = 0, flag_first = 0, amount = 3.000, chu kỳ 毎月",
       "1. F1 mua SP-C bằng thẻ hợp lệ, ngày mua = D\n2. Mở 注文詳細\n3. Đối chiếu cổng thanh toán",
       "flag_trial=0 · flag_first=0 · amount 3.000円 · chu kỳ 毎月",
       "- Số tiền đã bill = 3.000円\n- 次回決済予定日 = D + 1 tháng\n- Trạng thái =「継続中」",
       env="PRODUCTION",
       note="Nguồn: r310."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 với chu kỳ 毎週 → hạn kỳ kế = ngày mua + 7 ngày (giờ ép 06:58:59, trước cron 07:00)",
       FRC + "\n- SP-C chu kỳ 毎週, không trial",
       "1. F1 mua SP-C ngày D\n2. Mở 注文詳細 đọc 次回決済予定日 (cả ngày và giờ)",
       "chu kỳ 毎週 · ngày mua D",
       "- 次回決済予定日 = D + 7 ngày\n"
       "- Ghi lại phần GIỜ hiển thị. Theo spec BR-06 giờ thực trong DB là 06:58:59, "
       "nhưng blade hard-code chuỗi「07:00」→ nếu UI hiện 07:00 thì đây là hiển thị cứng, không phải giờ thật",
       env="PRODUCTION",
       note="Nguồn: r311 (tester ghi「mới check bill tháng và bill tuần」) + spec BR-06 + Field Matrix #57. "
            "Đây là MT-12 — giờ hiển thị không phản ánh dữ liệu."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 với các chu kỳ 3ヶ月毎 / 6ヶ月毎 / 毎年 → hạn kỳ kế đúng theo chu kỳ",
       FRC + "\n- 3 sản phẩm 継続 chu kỳ 3ヶ月毎 / 6ヶ月毎 / 毎年, không trial",
       "1. F1 mua lần lượt 3 sản phẩm, cùng ngày D\n2. Mở 注文詳細 của từng hợp đồng đọc 次回決済予定日",
       "ngày mua D chung cho cả 3",
       "- Sản phẩm 3ヶ月毎: 次回決済予定日 = D + 3 tháng\n- 6ヶ月毎: D + 6 tháng\n- 毎年: D + 1 năm",
       env="PRODUCTION",
       note="Nguồn: r311 + r338-r340. 3 chu kỳ tuy cùng công thức nhưng KHÁC kết quả cụ thể → "
            "gộp 1 TC vì cùng 1 lần thao tác, kiểm 3 giá trị trong cùng bảng kết quả."),

    tc("LINE user — mua 継続", "PAY-001", "Normal",
       "Mua 継続 bằng UnivaPay — kiểm tra dữ liệu ghi nhận trên UnivaPay khớp chu kỳ",
       FRC + "\n- SP-C dùng UnivaPay, テスト環境, có giới hạn số lần bill = 4",
       "1. F1 mua SP-C với chu kỳ 毎月\n2. Mở dashboard UnivaPay tra giao dịch/recurring token của F1\n"
       "3. Đối chiếu chu kỳ và số lần bill ghi nhận bên UnivaPay",
       "chu kỳ 毎月 · number_charge = 4",
       "- Bên UnivaPay có bản ghi tương ứng với đúng chu kỳ hàng tháng\n"
       "- Có ghi nhận giới hạn số lần bill = 4\n- Badge 決済ステータス ở admin mở đúng trang này",
       env="PRODUCTION",
       note="Nguồn: r314-r321. ⚠ MÂU THUẪN NIÊN ĐẠI: r314-r323 mô tả cơ chế SUBSCRIPTION của UnivaPay "
            "(period=monthly/weekly/Quarterly/...), nhưng r388 ghi「Update spec: bill tiền chu kỳ bằng univapay "
            "chuyển qua bill job như stripe (không dùng subcription nữa)」→ xem MT-13, expected đã viết trung lập."),

    tc("LINE user — mua 継続", "FUNC-001", "Normal",
       "Mua 継続 số lượng > 1 → hợp đồng ghi nhận đúng số lượng, tiền = giá × số lượng",
       FRC + "\n- SP-C giá 1.000円/kỳ, không trial, bật 在庫数 = 10",
       "1. F1 mua SP-C với số lượng = 2\n2. Mở 注文詳細 hợp đồng đọc số lượng và số tiền kỳ đầu\n"
       "3. Đối chiếu cổng thanh toán\n4. Xem tồn kho còn lại ở list",
       "1.000円 × 2 = 2.000円",
       "- Số tiền kỳ đầu = 2.000円 ở cả 注文詳細 và cổng thanh toán\n- Tồn kho còn lại = 8",
       env="PRODUCTION",
       note="Nguồn: r312 + r320 + r363 + r396. ⚠ Spec R50: quantity_purchased của hợp đồng "
            "KHÔNG hiển thị ở bất kỳ đâu trên UI → xem MT-14."),

    tc("LINE user — mua 継続", "PAY-002", "Abnormal",
       "Mua 継続 thất bại → xóa cả bản ghi hợp đồng và kỳ, gửi action bill fail + notify",
       FRC + "\n- SP-C dùng Stripe テスト環境, đã gắn action ở slot「決済エラー発生時」",
       "1. F1 mua SP-C với thẻ fail 4000 0000 0000 0341\n2. Quan sát màn hình phía LINE\n"
       "3. Mở 販売履歴 継続 tìm hợp đồng của F1\n4. Kiểm tra chat 1:1 của F1 và notify admin",
       "Thẻ 4000 0000 0000 0341",
       "- Phía LINE hiện message bill lỗi, quay về màn nhập thẻ\n"
       "- KHÔNG có hợp đồng nào của F1 cho SP-C ở 販売履歴\n"
       "- Có gửi action case bill fail cho F1\n"
       "- Admin nhận notify「【bot】<line name> <tên item> の決済に失敗しました」",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r17-r18 + r25-r26 + r33-r34."),

    # ══════ 16. Tồn kho & 購入上限 ══════
    tc("Tồn kho & 購入上限", "FUNC-BOUND-001", "Boundary",
       "remain = 10, 購入上限 = 5 → mua 4 và 5 OK, mua 6 báo lỗi VƯỢT GIỚI HẠN MUA (không phải lỗi tồn kho)",
       FR + "\n- SP: quantity_stock 10 (chưa bán), max_per_person 5, Stripe テスト環境",
       "1. F1 mua số lượng 4 → quan sát\n2. F2 mua số lượng 5 → quan sát\n"
       "3. F3 nhập số lượng 6 → bấm mua → đọc message lỗi",
       "remain=10 · max_per_person=5 · thử 4 / 5 / 6",
       "- Số lượng 4: mua thành công, tạo đơn\n- Số lượng 5: mua thành công, tạo đơn\n"
       "- Số lượng 6: báo lỗi「<số lượng max được mua>以下入力してください」, KHÔNG tạo đơn",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r87-r89 (Bug KH #35992, 04/2026 — tab MỚI NHẤT về tồn kho)."),

    tc("Tồn kho & 購入上限", "FUNC-BOUND-001", "Boundary",
       "remain = 5, 購入上限 = 6 → mua 4 và 5 OK, mua 6 báo lỗi HẾT KHO",
       FR + "\n- SP: tồn kho còn lại 5, max_per_person 6",
       "1. Mua số lượng 4 → quan sát\n2. Mua số lượng 5 (reset tồn kho về 5 trước khi thử) → quan sát\n"
       "3. Nhập số lượng 6 → bấm mua → đọc message lỗi",
       "remain=5 · max_per_person=6 · thử 4 / 5 / 6",
       "- Số lượng 4 và 5: mua thành công\n"
       "- Số lượng 6: báo lỗi「在庫切りです。<số remain>以下入力してください」— message TỒN KHO, khác message giới hạn mua",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r92-r94. Điểm phân biệt 2 message là quan trọng — nếu ra sai message thì raise."),

    tc("Tồn kho & 購入上限", "FUNC-BOUND-001", "Boundary",
       "remain = 5, 購入上限 = 1 → mua 1 OK, mua 2 bị chặn bằng lỗi GIỚI HẠN MUA",
       FR + "\n- SP: tồn kho còn 5, max_per_person = 1",
       "1. Mua số lượng 1 → quan sát\n2. Nhập số lượng 2 → bấm mua → đọc message lỗi",
       "remain=5 · max_per_person=1 · thử 1 / 2",
       "- Số lượng 1: mua thành công\n"
       "- Số lượng 2: KHÔNG cho mua, hiện lỗi giới hạn mua (KHÔNG phải lỗi tồn kho)",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r95-r96."),

    tc("Tồn kho & 購入上限", "FUNC-BOUND-001", "Boundary",
       "remain = 1 → mua 1 OK (tồn kho về 0), mua 2 báo lỗi hết kho",
       FR + "\n- SP: tồn kho còn đúng 1",
       "1. F1 nhập số lượng 2 → bấm mua → đọc lỗi\n2. F1 nhập số lượng 1 → bấm mua\n"
       "3. Xem cột 在庫数 ở list sản phẩm",
       "remain=1 · thử 2 / 1",
       "- Số lượng 2: báo lỗi「在庫切りです。1以下入力してください」, không tạo đơn\n"
       "- Số lượng 1: mua thành công, tạo đơn\n- Tồn kho còn lại = 0",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r98-r99 + r122-r123."),

    tc("Tồn kho & 購入上限", "FUNC-BOUND-001", "Abnormal",
       "remain = 0 → mua bất kỳ số lượng nào cũng bị chặn",
       FR + "\n- SP: tồn kho còn 0",
       "1. F1 mở 商品ページ, nhập số lượng 1 → bấm mua\n2. Đọc message lỗi\n3. Mở 販売履歴 kiểm tra",
       "remain=0",
       "- Báo lỗi「在庫がないので、購入できません。販売者に連絡してください。」\n- KHÔNG tạo đơn nào",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r103 + r127 + r140 + r146."),

    tc("Tồn kho & 購入上限", "FUNC-VALID-001", "Abnormal",
       "Số lượng nhập không hợp lệ: 0 · số âm · số thập phân · chữ · để trống → cùng 1 message lỗi",
       FR + "\n- SP có bật 在庫数, tồn kho còn 5",
       "1. Lần lượt nhập vào ô số lượng: 0 · −1 · 1.5 · 「abc」· để trống\n2. Sau mỗi lần bấm mua, đọc message",
       "0 · −1 · 1.5 ·「abc」· rỗng",
       "- Cả 5 input đều báo lỗi「数量を入力してください」\n- Không tạo đơn nào",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r104-r108 + r129-r133. 5 input cùng 1 kết quả → giữ chung 1 TC."),

    tc("Tồn kho & 購入上限", "CONC-001", "Abnormal",
       "★ 2 user bấm mua CÙNG LÚC khi remain = 1 → 1 người thành công, 1 người báo lỗi",
       FR + "\n- SP: tồn kho còn đúng 1, Stripe テスト環境\n- Chuẩn bị 2 tài khoản LINE A và B, cùng ở màn 最終確認",
       "1. A và B cùng bấm 購入する trong khoảng < 1 giây (2 máy song song)\n"
       "2. Quan sát màn hình cả 2 máy\n3. Mở 販売履歴 đếm số đơn thành công của SP\n"
       "4. Xem cột 在庫数 ở list sản phẩm",
       "remain=1 · A mua 1 · B mua 1 (đồng thời)",
       "- Đúng MỘT người mua thành công (tạo đơn), người còn lại báo lỗi và KHÔNG tạo đơn\n"
       "- Tổng số đơn thành công = 1, tồn kho còn 0\n- KHÔNG có trường hợp cả 2 cùng thành công",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r100 + r124 + r138 + r144. ⚠ Spec R11: nhánh Stripe kiểm tồn kho "
            "SAU khi tạo bản ghi → race condition đã biết. RULE-08: race condition → PRODUCTION."),

    tc("Tồn kho & 購入上限", "CONC-001", "Abnormal",
       "2 user mua đồng thời, user A CHƯA có kết quả bill ngay → A giữ chỗ, B bị chặn",
       FR + "\n- SP: tồn kho còn đúng 1, cổng thanh toán trả kết quả chậm (mô phỏng bằng cách tắt webhook)",
       "1. A bấm mua, cổng chưa trả kết quả (đơn ở trạng thái chờ)\n"
       "2. Ngay lúc đó B bấm mua số lượng 1\n3. Quan sát màn hình B\n4. Mở 販売履歴 xem trạng thái đơn của A",
       "remain=1 · A đang chờ kết quả · B mua 1",
       "- A: tạo được đơn ở trạng thái đang chờ xử lý thanh toán (決済処理中)\n"
       "- B: báo lỗi hết kho, KHÔNG tạo đơn",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r101 + r125 + r139 + r145."),

    tc("Tồn kho & 購入上限", "CONC-001", "Normal",
       "2 user mua đồng thời, user A BILL FAIL → tồn kho được trả lại, B mua thành công",
       FR + "\n- SP: tồn kho còn đúng 1",
       "1. A bấm mua bằng thẻ fail 4000 0000 0000 0341\n2. Ngay sau đó B bấm mua bằng thẻ hợp lệ\n"
       "3. Quan sát 2 màn hình\n4. Mở 販売履歴 và cột 在庫数",
       "remain=1 · A thẻ fail · B thẻ hợp lệ",
       "- A: hiện thông báo bill lỗi, đơn tạm bị xóa\n- B: mua thành công, tạo đơn\n"
       "- Tổng đơn thành công = 1, tồn kho còn 0",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r102 + r126."),

    tc("Tồn kho & 購入上限", "CONC-001", "Normal",
       "User A HỦY hợp đồng 継続 → tồn kho trả lại, user B mua được",
       FRC + "\n- SP-C 継続: tồn kho đặt 1, A đang có hợp đồng chiếm chỗ duy nhất",
       "1. B mở link mua SP-C → xác nhận bị chặn vì hết kho\n2. A bấm hủy hợp đồng ở link 解約\n"
       "3. B mở lại link mua SP-C và hoàn tất mua",
       "remain=0 (do A đang giữ) → A hủy → remain=1",
       "- Bước 1: B bị báo lỗi hết kho\n- Bước 3: B mua thành công",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r128. Spec BR-04: tồn kho 継続 tính SUM WHERE status_bill <> 3."),

    tc("Tồn kho & 購入上限", "REG-001", "Normal",
       "Sau khi bill thành công KHÔNG được hiện lỗi hết kho sai (bug đã fix #35992)",
       FR + "\n- SP: tồn kho 10, còn hàng, Stripe テスト環境",
       "1. F1 mua thành công số lượng 2\n2. F2 mua tiếp thành công số lượng 3 ngay sau đó\n"
       "3. F2 reload / quay lại trang kết quả sau khi đã mua xong\n4. Xem tồn kho ở list",
       "tồn kho 10 · F1 mua 2 · F2 mua 3",
       "- Cả 2 lần mua đều KHÔNG hiện lỗi「在庫が無いので、購入できません。」\n"
       "- Reload trang kết quả: KHÔNG hiện lỗi hết kho, trạng thái giao dịch KHÔNG bị đổi thành lỗi\n"
       "- Tồn kho giảm đúng: 10 → 8 → 5",
       env="PRODUCTION",
       note="Nguồn: Improve bill tiền stripe r90-r91 (Bug KH #35992: nguyên nhân check số lượng THỪA sau khi "
            "bill thành công; cách fix: bỏ code check tồn kho ở bước sau). regression"),

    tc("Tồn kho & 購入上限", "SEC-002", "Abnormal",
       "★ Gọi thẳng API mua vượt 購入上限 → server có chặn không (spec nói KHÔNG enforce)",
       FR + "\n- SP: max_per_person = 2, tồn kho 100\n- Có công cụ gửi request trực tiếp (Postman/DevTools)",
       "1. F1 mua bình thường qua UI với số lượng 2 → thành công\n"
       "2. Bắt request thanh toán, sửa số lượng thành 10, gửi lại trực tiếp\n"
       "3. Mở 注文詳細 và cột 販売数 kiểm tra kết quả",
       "max_per_person=2 · gửi số lượng 10 qua API",
       "- Ghi lại kết quả THẬT: request có bị từ chối không\n"
       "- Theo spec R7/BR-04, max_per_person KHÔNG được enforce ở server → nếu tạo được đơn 10 sản phẩm "
       "thì đây là lỗ hổng cần raise ngay (BLOCKER)",
       env="PRODUCTION",
       note="Suy luận của AI từ spec R7 + §5.2. Corpus KHÔNG có TC bypass client. Đây là MT-02 (cùng gốc) — "
            "CẦN LEADER QUYẾT có đưa TC tầng API vào bộ chạy không."),
]
