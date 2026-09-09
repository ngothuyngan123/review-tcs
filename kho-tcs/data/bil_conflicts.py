# -*- coding: utf-8 -*-
"""FA-026 商品販売 (Bill tiền item) — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ đang CHỜ QUYẾT ĐỊNH của Leader (chưa mục nào được chốt).

Nguồn TCs: 12. TCsLine_Item (7 tab) + TCsLine_Improve chung / Monitor bill tiền (khối item).
Nguồn spec: spec-features/admin/bill-item/ (feature-spec.md · web/logic-spec.md · job/job-spec.md ·
            db/db-mapping.md · ui/ui-spec.md).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", W,
     "Giá tối thiểu của sản phẩm là 50円 hay 100円?",
     "「Quản lý sản phẩm」r37 (02/2023, tab master):「Giá tiền bill — bắt buộc nhập, **>= 50 yên**」.\n"
     "Không có TC nào trong corpus kiểm biên 100円.",
     "`feature-spec.md:761` BR-02: V2 `amount` ≥ **100** — nhưng ⚠ **CHỈ CLIENT** "
     "(`add-single-item.js:600-655`). V1 mới có server-side min **50**.\n"
     "`feature-spec.md:695` Field Matrix #7: 「商品価格」required, **min 100 (client)**; BR-05 ghi "
     "「V1 chỉ min 50 ở server」.",
     "TC gốc viết từ 02/2023 — thời điểm màn hình còn là bản V1 (min 50). Màn hiện hành là V2 (min 100). "
     "Nếu member chạy theo TC cũ sẽ báo PASS khi tạo được sản phẩm 50円, trong khi V2 lẽ ra phải chặn. "
     "Ngược lại nếu server thật sự không validate (BR-15) thì CẢ HAI mốc đều không được enforce.",
     "『Tạo/sửa 単品 — 基本設定』TC「商品価格 = 99 / 100 / 50 → biên giá tối thiểu 100円」",
     "",
     "① Xác nhận với dev mốc tối thiểu hiện hành của màn 商品販売 V2 (100 hay 50).\n"
     "② Nếu chốt 100: giữ nguyên expected của TC, thêm chú thích TC gốc 50円 đã lỗi thời.\n"
     "③ Chạy kèm TC gọi API trực tiếp (MT-02) để biết server có chặn hay không.\n"
     "④ Sửa `feature-spec.md:761` ghi rõ mốc áp dụng cho từng thế hệ màn hình."],

    ["MT-02", "CAO", W,
     "Ràng buộc CHỈ có ở client — có đưa TC gọi thẳng API vào bộ chạy không?",
     "Toàn bộ corpus 12. TCsLine_Item **KHÔNG có TC nào** thao tác ở tầng API. "
     "Mọi TC validate đều thao tác qua giao diện (r37, r74, r89, r94, r104-r108).",
     "`feature-spec.md:778-790` §5.2 liệt kê 7 rule CHỈ enforce ở client: giá tối thiểu 100円 · giới hạn "
     "ký tự 20/50/30/15/10 · khoá 決済システム sau khi lưu · **購入上限 max_per_person** · số ảnh tối đa 5 · "
     "định dạng URL.\n"
     "`feature-spec.md:1162` R6: saveItem không validation server, `/ajax/*` **được miễn CSRF** → "
     "giá 0円, tên 10.000 ký tự đều được chấp nhận.\n"
     "`feature-spec.md:1163` R7: `max_per_person` **không enforce ở server**.\n"
     "`feature-spec.md:762` BR-03: 決済システム khoá **chỉ ở client**.",
     "Nếu chỉ test qua giao diện thì bộ TC sẽ PASS toàn bộ trong khi hệ thống vẫn có thể bị tạo sản phẩm "
     "0円 hoặc bị mua vượt 購入上限 bằng cách gọi API. Đây là rủi ro TIỀN BẠC trực tiếp. Ngược lại, TC tầng API "
     "cần công cụ và kỹ năng khác với manual test thông thường → phải Leader quyết có đưa vào scope không.",
     "『Tạo/sửa 単品 — 基本設定』TC「決済システム bị khóa sau lần lưu đầu tiên」· "
     "『Tồn kho & 購入上限』TC「Gọi thẳng API mua vượt 購入上限」· "
     "『Phân quyền & môi trường』TC「Gọi API lưu sản phẩm với dữ liệu vi phạm ràng buộc client」",
     "",
     "① Quyết định phạm vi: chỉ test UI, hay test cả tầng API.\n"
     "② Nếu có test API: chỉ định người có công cụ (DevTools/Postman) và môi trường được phép.\n"
     "③ Nếu KHÔNG test API: ghi rõ vào báo cáo rằng 7 rule ở §5.2 là RỦI RO CHƯA ĐƯỢC PHỦ.\n"
     "④ Đề xuất dev bổ sung validation server cho `saveItem` và `max_per_person`."],

    ["MT-03", "CAO", W,
     "Kỳ định kỳ bill theo GIÁ HIỆN TẠI hay GIÁ LÚC ĐĂNG KÝ?",
     "「Quản lý sản phẩm」r346 (Stripe):「case sửa giá sản phẩm ⇒ **bill theo giá mới**」— Test Result OK.\n"
     "「Quản lý sản phẩm」r362 (UnivaPay):「check case thay đổi giá sản phẩm ⇒ **univapay không update được "
     "giá bill ⇒ bill theo giá cũ**; các user mua mới thì bill theo giá mới」— Test Result OK.\n"
     "→ CÙNG 1 TAB, CÙNG NIÊN ĐẠI, 2 cổng cho 2 kết quả NGƯỢC NHAU.",
     "`feature-spec.md:764` BR-05: ★ Kỳ tiếp theo (cron) = **`s_items.amount` HIỆN TẠI × `quantity_purchased`** "
     "— **KHÔNG** dùng `amount_item`. Áp cho **CẢ 2 cron** (`HandleBillStripe.php:173,186`; "
     "`HandleSendActionTrialV2.php:180,189`).\n"
     "`feature-spec.md:1157` R1 xếp đây là rủi ro NGHIÊM TRỌNG: khách bị trừ giá mới mà không được thông báo; "
     "placeholder `AMOUNT_ORDER` trong tin nhắn action cũng đọc giá hiện tại.\n"
     "`feature-spec.md:740` Field Matrix #53: 「販売価格」継続 = `status_bill == 1 ? s_items.amount : amount_item`.",
     "⚠ **Quy tắc『ưu tiên TC mới nhất』KHÔNG áp dụng được ở đây** — 2 dòng mâu thuẫn nằm trong CÙNG 1 TAB, "
     "CÙNG 1 đợt test. Đây là mâu thuẫn theo CỔNG THANH TOÁN chứ không phải theo thời gian. "
     "Spec khẳng định cả 2 cổng đều dùng giá hiện tại, tức r362 (UnivaPay bill giá cũ) có thể đã lỗi thời sau "
     "khi UnivaPay chuyển sang bill bằng job (xem MT-13). Đây là vấn đề TIỀN BẠC ảnh hưởng trực tiếp khách hàng "
     "cuối: đổi giá 3.000 → 5.000円 thì khách cũ bị trừ bao nhiêu?",
     "『Job bill định kỳ』TC「Admin ĐỔI GIÁ sản phẩm sau khi khách đã đăng ký」· "
     "『Màn 販売履歴』TC「販売価格 của hợp đồng ĐANG CHẠY hiển thị giá HIỆN TẠI」· "
     "『アクション設定』TC「Action text có chèn thông tin đơn hàng」",
     "",
     "① Chốt nghiệp vụ: hợp đồng đã ký có bị áp giá mới không (đây là câu hỏi PHÁP LÝ, không chỉ kỹ thuật).\n"
     "② Nếu chốt 'giá lúc đăng ký': đây là BUG hiện tại, cần raise và sửa cả 2 cron + placeholder AMOUNT_ORDER.\n"
     "③ Nếu chốt 'giá hiện tại': cần bổ sung luồng THÔNG BÁO cho khách trước khi đổi giá.\n"
     "④ Sửa r362 của tab gốc (hoặc ghi chú đã lỗi thời) và cập nhật expected của TC."],

    ["MT-04", "CAO", W,
     "Xóa sản phẩm đã có đơn / đang có hợp đồng chạy → xử lý dữ liệu lịch sử thế nào?",
     "「Quản lý sản phẩm」r21 / r105:「Xóa sản phẩm ⇒ hiện màn comfirm xóa sản phẩm → nhấn comfirm xóa thì "
     "thực hiện **xóa toàn bộ data của sản phẩm**」— KHÔNG nói gì về đơn hàng và hợp đồng đã tồn tại.\n"
     "Corpus **KHÔNG có TC** nào xóa sản phẩm đang có đơn / đang có hợp đồng chạy.",
     "`feature-spec.md:168-177` SCR-BIL-03: ★ **HARD DELETE** — `s_items` không có `deleted_at`. "
     "⚠ Hệ quả xoá: `s_order_history` / `s_cycle_order_history` **chỉ được ghi log, không xoá** → trở thành "
     "bản ghi **mồ côi** (`item_id` trỏ vào sản phẩm không còn tồn tại). Xoá folder xoá TOÀN BỘ sản phẩm bên trong.\n"
     "`feature-spec.md:1171` R15: **không có FOREIGN KEY constraint nào**; xoá cứng `b_c_info_setting` và "
     "**xoá file ảnh vật lý**.\n"
     "`job/job-spec.md` J1/J2 quét `s_cycle_order_history` JOIN `s_items` — spec không nói rõ hành vi khi item đã bị xoá.",
     "Đây là mảng TRỐNG của cả corpus lẫn spec. Rủi ro thực tế: (a) doanh thu đã thu mất truy vết vì màn "
     "販売履歴 join sang sản phẩm không còn tồn tại; (b) hợp đồng định kỳ của sản phẩm đã xoá — job còn tiếp tục "
     "trừ tiền khách hay dừng? Nếu còn trừ tiền thì khách không có cách nào tự huỷ (link 解約 sẽ báo sản phẩm "
     "không tồn tại). Cả 2 nhánh đều ảnh hưởng TIỀN của người dùng cuối.",
     "『Copy & xóa sản phẩm』TC「Xóa sản phẩm ĐÃ CÓ ĐƠN」· TC「Xóa sản phẩm 継続 đang CÓ hợp đồng chạy」· "
     "『Folder sản phẩm』TC「Xóa folder đang chứa sản phẩm」",
     "",
     "① Chạy TC thăm dò trên môi trường test để biết hành vi THẬT (đặc biệt là job bill sau khi xoá).\n"
     "② Nếu job vẫn trừ tiền → BLOCKER, raise ngay.\n"
     "③ Chốt nghiệp vụ: có nên CHẶN xoá sản phẩm đang có hợp đồng chạy không.\n"
     "④ Bổ sung mục này vào `feature-spec.md` §2.1 SCR-BIL-03 và vào ma trận rủi ro §10."],

    ["MT-05", "TRUNG BÌNH", W,
     "一括フォルダ変更 — thứ tự sản phẩm ở folder đích có xác định không?",
     "「Quản lý sản phẩm」r23 / r107:「Change folder」— TC gốc **chỉ có tiêu đề, KHÔNG có kết quả mong đợi**.",
     "`feature-spec.md:1194` R33: `moveItem` đẩy **mọi item lên cùng một giá trị** `max(position)+1` "
     "(`:416-436`) → thứ tự trong folder đích **không xác định**.\n"
     "`feature-spec.md:151` §2.1 bước 6 lặp lại cảnh báo này.",
     "TC gốc không có expected nên member sẽ tự đánh giá PASS bằng cảm tính. Với 2 sản phẩm trở lên, thứ tự "
     "hiển thị có thể đổi mỗi lần load (không deterministic) → member test 1 lần thấy đúng nhưng khách hàng "
     "gặp thứ tự lộn xộn. Cần chốt: đây là bug cần sửa hay hành vi chấp nhận được.",
     "『Folder sản phẩm』TC「一括フォルダ変更 nhiều sản phẩm sang folder khác」",
     "",
     "① Chạy TC với ≥ 3 sản phẩm, load lại 3 lần, ghi thứ tự từng lần.\n"
     "② Nếu thứ tự đổi giữa các lần → raise bug, đề xuất dev gán position tăng dần.\n"
     "③ Chốt expected cho TC (thứ tự giữ nguyên như folder cũ, hay xếp cuối theo thứ tự chọn)."],

    ["MT-06", "TRUNG BÌNH", W,
     "Cột 販売数 có tính cả đơn ĐÃ HOÀN TIỀN không?",
     "「Quản lý sản phẩm」r17:「số đã bán」— TC gốc **chỉ có tiêu đề**, không nêu quy tắc đếm. "
     "Corpus KHÔNG có TC nào kiểm 販売数 sau khi hoàn tiền.",
     "`feature-spec.md:165` §2.1: 「販売数」là `SUM(quantity_purchased)` runtime, **không lọc `status_order`** → "
     "đơn đã hoàn tiền vẫn được tính.\n"
     "`feature-spec.md:731` Field Matrix #42 xác nhận lại: Aggregated runtime, **không lọc status_order**.\n"
     "Đối chiếu: BR-04 (`:763`) tính TỒN KHO thì **CÓ** lọc `status_order = 1`.",
     "Cùng 1 màn hình nhưng 2 con số dùng 2 quy tắc khác nhau: 販売数 đếm cả đơn hoàn tiền, còn tồn kho thì "
     "không. Admin nhìn 「販売数 = 10 / 在庫数 = 3」 trên sản phẩm stock 12 sẽ không hiểu vì sao. "
     "Đây là số liệu kinh doanh admin dùng để ra quyết định.",
     "『Màn list sản phẩm』TC「販売数 vẫn tính cả đơn ĐÃ HOÀN TIỀN」· TC「Cột 販売数/在庫数 khi CÓ set tồn kho」",
     "",
     "① Chạy TC thăm dò để xác nhận con số thật.\n"
     "② Chốt: 販売数 nên đếm gì (tất cả đơn / chỉ đơn thành công).\n"
     "③ Nếu giữ nguyên: đề xuất đổi nhãn cột hoặc thêm tooltip giải thích.\n"
     "④ Sửa expected của TC theo quyết định."],

    ["MT-07", "TRUNG BÌNH", W,
     "Đổi 管理名 sản phẩm → lịch sử bán hàng có giữ TÊN LÚC MUA không?",
     "Corpus **KHÔNG có TC** nào đổi tên sản phẩm rồi kiểm tra màn 販売履歴.",
     "`feature-spec.md:189` §2.1 SCR-BIL-05: **đổi `name` → đồng bộ ngược `name_item`** sang toàn bộ "
     "`s_order_history` + `s_cycle_order_history`.\n"
     "`feature-spec.md:689` Field Matrix #1 và `:739` #49 xác nhận: `name_item` là **snapshot**, nhưng "
     "**đồng bộ ngược** khi đổi `s_items.name`.",
     "Spec tự mô tả `name_item` là 'snapshot' nhưng lại đồng bộ ngược — 2 khái niệm loại trừ nhau. "
     "Hệ quả nghiệp vụ: hoá đơn/lịch sử của giao dịch đã hoàn tất bị đổi tên sản phẩm hồi tố. "
     "Với 特商法 và đối soát kế toán, việc lịch sử giao dịch thay đổi sau khi phát sinh là RỦI RO.",
     "『Tạo/sửa 継続 — 基本設定』TC「Đổi 管理名 sản phẩm đã có đơn」· 『Export CSV lịch sử』các TC export",
     "",
     "① Chạy TC xác nhận hành vi thật (kể cả file CSV export sau khi đổi tên).\n"
     "② Chốt nghiệp vụ: lịch sử nên giữ tên lúc mua hay theo tên hiện tại.\n"
     "③ Nếu chốt 'giữ tên lúc mua' → raise bug, và cần bàn cách xử lý dữ liệu đã bị ghi đè.\n"
     "④ Sửa `feature-spec.md:689` bỏ chữ 'snapshot' nếu giữ hành vi đồng bộ ngược."],

    ["MT-08", "CAO", W,
     "Sản phẩm UnivaPay có setting thuế nhưng thuế không được xử lý — UI vẫn hiện「（税込）」",
     "「Test invoice (stripe)」r4 / r6 / r8 / r10: màn tạo sản phẩm **CÓ hiện setting thuế cho cả UnivaPay**, "
     "mặc định 10%, lưu được vào DB — Test Result OK.\n"
     "r22-r23:「check item bill univapay bill được bình thường」— chỉ kiểm bill được, **KHÔNG kiểm thuế/hoá đơn**.\n"
     "→ Corpus xác nhận setting thuế TỒN TẠI cho UnivaPay nhưng chưa từng verify nó có tác dụng gì.",
     "`feature-spec.md:767` BR-08: ⚠ **UnivaPay hoàn toàn không xử lý thuế** — `createDataInvoice()` "
     "**chỉ gọi ở nhánh Stripe**.\n"
     "`feature-spec.md:1199` R38 xếp là rủi ro Trung bình: `tax_item` vẫn được lưu và UI vẫn hiện「（税込）」 "
     "(`:6311-6324`).\n"
     "`feature-spec.md:703` Field Matrix #15 lặp lại cảnh báo.",
     "Admin chọn 8% hay 10% cho sản phẩm UnivaPay đều KHÔNG có tác dụng, nhưng UI không hề báo. "
     "Màn 販売履歴 vẫn ghi「決済金額（税込）」→ admin và khách hàng đều tin rằng số tiền đã gồm thuế và "
     "có hoá đơn. Đây là rủi ro về THUẾ và HOÁ ĐƠN (có thể liên quan 適格請求書/インボイス制度).",
     "『Thuế & hóa đơn』TC「Sản phẩm UnivaPay có setting thuế → có sinh hóa đơn thuế không?」· "
     "『Tạo/sửa 単品 — 基本設定』TC「消費税率: chọn 10% / 8%」",
     "",
     "① Chạy TC thăm dò trên UnivaPay để xác nhận có hoá đơn thuế hay không.\n"
     "② Chốt: ẩn setting thuế khi chọn UnivaPay, hay bổ sung xử lý thuế cho UnivaPay.\n"
     "③ Nếu giữ nguyên: bỏ nhãn「（税込）」ở màn lịch sử của đơn UnivaPay.\n"
     "④ Xác nhận với bộ phận kế toán/pháp chế trước khi chốt."],

    ["MT-09", "TRUNG BÌNH", W,
     "Hợp đồng 継続 bị bill lỗi hiển thị badge gì? Có badge「決済エラー」không?",
     "「Quản lý sản phẩm」r173 liệt kê trạng thái「**bill lỗi**」là 1 trong 5 trạng thái của lịch sử mua "
     "sản phẩm 継続 — Test Result OK.\nr225 cũng có filter theo trạng thái「bill lỗi」.",
     "`feature-spec.md:1099` §9.1 mục 8: 「**Không có badge 「決済エラー」**; 「決済終了」 = `status_bill = 2`」.\n"
     "`feature-spec.md:770` BR-11: `s_cycle_order_history.status_bill` chỉ có `1` 継続中 · `2` 決済終了 · "
     "`3` キャンセル済 — KHÔNG có giá trị riêng cho 'bill lỗi'.\n"
     "`feature-spec.md:741` Field Matrix #55: 「決済ステータス」継続 là **composite 6 nhánh** từ "
     "`status_trial` + `status_bill` + `last_bill_id` + `status_order`.",
     "Corpus nói có trạng thái 'bill lỗi', spec nói không có badge 決済エラー mà chỉ có 6 nhánh composite. "
     "Member sẽ không biết badge THẬT hiển thị chữ gì (延滞中? 決済エラー? hay vẫn 継続中?). "
     "Không chốt được nhãn thì không viết được expected đo lường được, và filter theo trạng thái cũng không "
     "verify được.",
     "『Màn 販売履歴』TC「Modal 絞り込み 継続 — lọc theo trạng thái hợp đồng」· "
     "『Màn 商品詳細 & Preview』TC「商品詳細 継続 — status hợp đồng đủ 5 trạng thái」",
     "",
     "① Chụp màn hình thật của 1 hợp đồng đang bill lỗi để lấy NHÃN CHÍNH XÁC.\n"
     "② Liệt kê đủ 6 nhánh composite kèm nhãn tương ứng, bổ sung vào `db/db-mapping.md` §5.2.\n"
     "③ Sửa expected của TC theo nhãn thật.\n"
     "④ Đối chiếu tên nhãn ở filter với tên nhãn ở cột trạng thái (phải khớp nhau)."],

    ["MT-10", "THẤP", W,
     "Coupon code ở trang mua 継続 — có thuộc phạm vi FA-026 không?",
     "「Quản lý sản phẩm」r303:「coupon code」ở khối『Check màn nhập friend infor』của sản phẩm 継続 — "
     "Test Result =「**Cần Comfirm**」, TC gốc chỉ có tiêu đề, KHÔNG có kết quả mong đợi và CHƯA có kết luận.",
     "`spec-features/admin/bill-item/` **KHÔNG nhắc tới coupon** ở bất kỳ file nào "
     "(feature-spec / logic-spec / api-spec / db-mapping / ui-spec).\n"
     "`feature-spec.md:35-42` §1.3 Phạm vi cũng không liệt kê coupon.",
     "TC gốc để ngỏ từ 2023 và chưa ai chốt. Nếu tính năng coupon có thật mà spec bỏ sót → spec thiếu; "
     "nếu không có → TC rác cần loại. Không chốt thì member sẽ tốn thời gian đi tìm ô coupon không tồn tại.",
     "『LINE user — nhập friend info』TC「Trang 友だち情報 継続商品 — có ô nhập coupon code」",
     "",
     "① Mở trang mua 継続 thật, xác nhận có ô coupon hay không.\n"
     "② Nếu CÓ: đây là Gap của spec → bổ sung vào `feature-spec.md` và viết đủ TC (mã hợp lệ / hết hạn / "
     "sai / dùng lại).\n"
     "③ Nếu KHÔNG: loại TC khỏi kho và ghi vào mục 'nguồn đã loại'."],

    ["MT-11", "THẤP", W,
     "TC 3D Secure ghi kết quả mong đợi vào SAI BẢNG dữ liệu",
     "「improve bill tiền 3D secure」r13-r14 (item bill 1 lần, thẻ 4242 và thẻ AMEX):\n"
     "「hiển thị navigation của browser / DB: tbl **`b_user_booking`.status_payment = 0**」\n"
     "Trong khi các dòng lân cận (r6, r10, r18) đều ghi đúng: 「DB: tbl `s_order_history`.status_order = 1」.",
     "`feature-spec.md:504-514` §3.1: bảng giao dịch của FA-026 là `s_order_history` / "
     "`s_cycle_order_history`.\n"
     "`b_user_booking` là bảng của **Booking Event** (nhắc tới ở「Improve bill tiền univapay」r224 "
     "「booking event ⇒ lưu thông tin bill tiền vào tbl b_user_booking」).",
     "Lỗi copy-paste của TC gốc (khối 3D secure được viết chung cho nhiều tính năng có bill tiền). "
     "Member đọc TC này sẽ đi kiểm bảng của tính năng khác và không tìm thấy dữ liệu → báo FAIL nhầm.",
     "『LINE user — nhập thẻ & 3D Secure』TC「Thẻ KHÔNG hỗ trợ 3DS (AMEX)」",
     "",
     "① Xác nhận đây là lỗi copy-paste (khả năng rất cao).\n"
     "② Đã viết lại expected theo bảng đúng của bill item — Leader duyệt cách viết này.\n"
     "③ Ghi chú vào tab gốc để không lặp lại khi tái sử dụng khối 3D secure cho tính năng khác."],

    ["MT-12", "THẤP", W,
     "「次回決済予定日」hiển thị giờ「07:00」— là dữ liệu thật hay chuỗi cứng?",
     "Corpus KHÔNG có TC nào kiểm phần GIỜ của 次回決済予定日. "
     "「Quản lý sản phẩm」r311 chỉ ghi「bill theo chu kỳ khác nhau」kèm note của tester "
     "「mới check bill tháng và bill tuần」.",
     "`feature-spec.md:308` SCR-BIL-19: ★ chuỗi「07:00」là **văn bản hard-code trong blade** "
     "(`cycle-history-detail.blade.php:146`), **không đọc từ DB**; có nhánh fallback "
     "`moment(trial_expired_time).add(1,'day')` khi `c_expired_date` rỗng.\n"
     "`feature-spec.md:765` BR-06: chu kỳ weekly ép giờ **`06:58:59`** (trước cron 07:00).\n"
     "`feature-spec.md:743` Field Matrix #57 lặp lại.",
     "Với chu kỳ 毎週, giờ thật trong dữ liệu là 06:58:59 nhưng màn hình luôn hiện 07:00 → member đối chiếu "
     "sẽ thấy 'sai' và raise bug nhầm. Ngược lại nếu ngày bị rỗng thì màn hình vẫn hiện một ngày (từ nhánh "
     "fallback) khiến không phát hiện được dữ liệu lỗi. Cần chốt để viết expected đúng.",
     "『LINE user — mua 継続』TC「Mua 継続 với chu kỳ 毎週」",
     "",
     "① Xác nhận với dev chuỗi 07:00 có phải hard-code không.\n"
     "② Chốt expected: TC chỉ verify phần NGÀY, phần giờ ghi chú là hiển thị cố định.\n"
     "③ Đề xuất dev hiển thị giờ thật hoặc bỏ hẳn phần giờ để tránh gây hiểu nhầm."],

    ["MT-13", "CAO", W,
     "Bill định kỳ UnivaPay dùng SUBSCRIPTION của cổng hay dùng JOB của LME?",
     "「Quản lý sản phẩm」r314-r323 (khối cũ):「check thanh toán bằng univapay: check tạo bill tiền chu kỳ "
     "(**subcriptions**) trên univapay」với ánh xạ chu kỳ period = monthly / weekly / Quarterly / "
     "Semiannually / Annually — Test Result OK.\n"
     "r347-r362:「Check bill univapay (**logic bill mới theo tự động bill của univapay**)」— OK.\n"
     "r388 (khối MỚI NHẤT của tab):「**Update spec: bill tiền chu kỳ bằng univapay chuyển qua bill job như "
     "stripe (không dùng subcription nữa)**」→ r389-r415 viết lại toàn bộ theo cơ chế job.",
     "`feature-spec.md:970-975` §7.2: **J2** `handle:HandleSendActionTrialV2` chạy `dailyAt('07:00')` — "
     "「(B) **Thanh toán định kỳ qua UNIVAPAY**」; `billItemUnivapay()` gắn `metadata.module = 'sales_job'`.\n"
     "`feature-spec.md:977-984` §7.3 khẳng định phân công **J1 = Stripe / J2 = UnivaPay**, cả 2 đều là cron "
     "của LME chủ động bill.\n"
     "→ Spec KHỚP với r388 (bản mới nhất), KHÔNG khớp với r314-r362.",
     "Đây là mâu thuẫn NIÊN ĐẠI trong cùng 1 tab: 2 khối TC mô tả 2 kiến trúc bill hoàn toàn khác nhau. "
     "Toàn bộ TC subscription (r314-r323) đã bị khối r388+ thay thế. Nếu member chạy nhầm khối cũ sẽ đi tìm "
     "subscription trên UnivaPay không tồn tại và báo FAIL hàng loạt. Cần chốt để loại dứt điểm khối cũ.",
     "『Job bill định kỳ』TC「Update spec — UnivaPay chuyển từ SUBSCRIPTION sang bill bằng JOB」· "
     "『LINE user — mua 継続』TC「Mua 継続 bằng UnivaPay — kiểm tra dữ liệu ghi nhận trên UnivaPay」",
     "",
     "① Xác nhận với dev: hiện tại UnivaPay còn tạo subscription không.\n"
     "② Nếu đã bỏ (khả năng cao): chốt loại toàn bộ TC subscription r314-r323 khỏi kho, ghi vào mục "
     "'nguồn đã loại'.\n"
     "③ Với hợp đồng CŨ đã có subscription trên UnivaPay: cần TC riêng xác nhận không bị bill 2 lần "
     "(subscription cũ + job mới).\n"
     "④ Ghi chú 'đã lỗi thời' vào khối r314-r362 của tab gốc."],

    ["MT-14", "THẤP", W,
     "Số lượng mua của hợp đồng 継続 không hiển thị ở bất kỳ màn nào",
     "「Quản lý sản phẩm」r312 / r320 / r363 / r396 đều có TC「check bill số lượng >1」cho sản phẩm 継続 — "
     "Test Result OK. Nhưng **không TC nào nói số lượng đó hiển thị ở đâu**.",
     "`feature-spec.md:1216` R50: `s_cycle_order_history.quantity_purchased` **không hiển thị ở bất kỳ đâu** "
     "dù có tham gia tính tồn kho — thiếu sót UI.\n"
     "Đối chiếu: `feature-spec.md:737` Field Matrix #51 — với 単品 thì 「購入個数」 CÓ hiển thị ở SCR-BIL-15/18.",
     "Admin không có cách nào biết 1 hợp đồng 継続 đang đăng ký bao nhiêu sản phẩm, dù số đó quyết định "
     "số tiền bị trừ mỗi kỳ và trừ vào tồn kho. Member không verify được TC 'bill số lượng > 1' bằng giao diện, "
     "chỉ có thể suy ra qua số tiền.",
     "『LINE user — mua 継続』TC「Mua 継続 số lượng > 1」· 『Job bill định kỳ』TC「Job bill hợp đồng có SỐ LƯỢNG > 1」",
     "",
     "① Xác nhận trên UI thật: có màn nào hiện số lượng của hợp đồng 継続 không.\n"
     "② Nếu không có: chốt cách verify (suy từ số tiền = đơn giá × số lượng) và ghi vào expected.\n"
     "③ Đề xuất dev bổ sung cột 購入個数 vào màn 注文詳細 継続."],

    ["MT-15", "TRUNG BÌNH", W,
     "Đổi thẻ BILL FAIL — thông tin thẻ có được cập nhật sang thẻ mới không?",
     "「Improve bill tiền stripe」r42-r43 (bill fail):「thông tin card: **update thông tin card mới** "
     "(logic cũ từ trước case fail vẫn update lại thông tin card)」— Test Result OK.\n"
     "「Improve bill tiền univapay」r232 / r258 (nhập card sai):「thông tin card: **vẫn giữ nguyên thông tin "
     "card cũ** ~~update thông tin card mới~~」— trong CÙNG 1 ô có 2 câu chồng nhau, câu sau bị gạch/ghi đè.",
     "`feature-spec.md:482-500` §2.5 mô tả luồng đổi thẻ nhưng **không nói rõ** trường hợp bill lại thất bại "
     "thì thẻ được cập nhật hay giữ nguyên. Chỉ ghi: 「Chỉ đổi thẻ → update `c_strip_*`/`c_univapay_*`」 và "
     "「Bill lại THẤT BẠI → `count_bill_error += 1` → kiểm tra auto-cancel」.",
     "2 cổng cho 2 hành vi khác nhau, và bản thân ô ghi chú của UnivaPay tự mâu thuẫn (dấu hiệu tester sửa "
     "dở dang). Hệ quả: nếu thẻ mới KHÔNG được lưu khi bill fail thì job bill kỳ sau vẫn dùng thẻ cũ đã hỏng → "
     "khách đổi thẻ xong vẫn bị lỗi mãi. Đây là vấn đề trải nghiệm + tiền bạc.",
     "『LINE user — đổi thẻ』TC「Đổi thẻ có bill lại nhưng BILL FAIL」· TC「Đổi thẻ nhập SAI THẺ (4111…)」",
     "",
     "① Chạy TC thăm dò riêng cho từng cổng (Stripe và UnivaPay), ghi lại 4 số cuối thẻ sau khi fail.\n"
     "② Chốt hành vi mong muốn (khuyến nghị: vẫn lưu thẻ mới để lần retry sau dùng được).\n"
     "③ Nếu 2 cổng khác nhau → thống nhất về 1 hành vi, raise task cho dev.\n"
     "④ Bổ sung mục này vào `feature-spec.md` §2.5."],

    ["MT-16", "TRUNG BÌNH", W,
     "Thẻ 3DS yêu cầu xác thực MỌI giao dịch → job bill định kỳ có bill được không?",
     "「improve bill tiền 3D secure」r37 / r45 (đổi thẻ sang thẻ 4000 0000 0000 3220):\n"
     "「sửa trial_expired_date < hiện tại / job bill lại trên dev chạy 5p 1 lần / **bill lại theo card mới - "
     "job sẽ bill lỗi do card này cần authen** / ⇒ **đã báo cho a Thắng trên group skype SNSLINE**」\n"
     "→ TC gốc ghi nhận hiện tượng nhưng CHƯA có kết luận xử lý.",
     "`feature-spec.md:968` §7.2 J1: charge bằng `autoPaymentIntents()` **off-session (không 3DS)**.\n"
     "Spec **không nêu** cách xử lý khi thẻ đã lưu bắt buộc xác thực từng giao dịch.\n"
     "`feature-spec.md:766` BR-07: bill lỗi 3 lần + `auto_cancel = 1` → huỷ hợp đồng.",
     "Khách dùng thẻ yêu cầu 3DS mọi giao dịch sẽ bị bill lỗi ở MỌI kỳ, và nếu bot bật tự động huỷ thì "
     "hợp đồng bị huỷ sau 3 kỳ dù thẻ của khách hoàn toàn hợp lệ. Hiện chưa có cơ chế báo cho khách biết "
     "'thẻ này không dùng được cho thanh toán định kỳ'. Đây là mất doanh thu + trải nghiệm xấu.",
     "『LINE user — đổi thẻ』TC「Đổi thẻ sang thẻ 3DS cần xác thực → job bill kỳ sau」",
     "",
     "① Hỏi dev kết luận của trao đổi trên Skype (TC gốc ghi 'đã báo a Thắng' nhưng không có kết luận).\n"
     "② Chốt: có chặn loại thẻ này ngay lúc đăng ký/đổi thẻ không.\n"
     "③ Nếu không chặn được: cần thông báo cho khách khi bill lỗi vì lý do 3DS (message riêng).\n"
     "④ Bổ sung giới hạn này vào `feature-spec.md` §7.2."],

    ["MT-17", "CAO", W,
     "Huỷ hợp đồng ở LME có huỷ luôn subscription/token bên cổng thanh toán không?",
     "「Quản lý sản phẩm」r357 (bill lỗi 3 lần + auto cancel):「1. change status của order sang hủy hợp đồng "
     "**2. Hủy bill tiền trên univapay**」— Test Result OK (note: 'trên dev ok, chưa test staging').\n"
     "r359-r360:「check user cancel bill tiền / check admin cancel bill tiền ⇒ **cancel bill tiền trên univapay**」"
     "— OK.\n"
     "→ Corpus khẳng định CÓ huỷ bên cổng.",
     "`feature-spec.md:471` §2.5: ⚠ **KHÔNG gọi API huỷ subscription bên cổng thanh toán** ở nhánh "
     "`cancelCycleOrderItem`. `UnivapayPayment::cancelSubcriptionSale()` chỉ được gọi từ 3 nơi phía web "
     "trong nhánh auto-cancel — **không** trong `cancelCycle()` của 2 cron.\n"
     "`feature-spec.md:1166` R10: `cancelCycle()` của **cả 2 cron KHÔNG gọi API huỷ subscription** "
     "(`HandleBillStripe.php:757`, `HandleSendActionTrialV2.php:737`) → hợp đồng bị cron tự huỷ **có thể còn "
     "subscription sống** ở cổng, **tiếp tục trừ tiền khách**.",
     "Corpus (2023-2025) nói có huỷ, spec (08/2026, đọc từ code) nói cron KHÔNG huỷ. Nếu spec đúng thì khách "
     "bị huỷ hợp đồng do bill lỗi 3 lần VẪN CÓ THỂ tiếp tục bị trừ tiền — đây là mức độ nghiêm trọng nhất "
     "trong toàn bộ danh sách. Lưu ý spec phân biệt rõ 2 nhánh: huỷ từ WEB (có gọi API) vs huỷ từ CRON "
     "(không gọi) — corpus không phân biệt điều này.",
     "『Job bill định kỳ』TC「Bill LỖI 3 lần liên tiếp + CÓ set tự động hủy」· "
     "『LINE user — hủy hợp đồng』TC「User bấm hủy ở trang 解約用ページ」· "
     "『Hoàn tiền & hủy phía admin』TC「一括解約実行」",
     "",
     "① ƯU TIÊN CAO NHẤT: chạy TC auto-cancel do bill lỗi 3 lần, sau đó kiểm tra dashboard cổng thanh toán "
     "xem subscription/recurring token còn sống không.\n"
     "② Chờ qua kỳ tiếp theo, kiểm tra khách có bị trừ tiền không.\n"
     "③ Nếu còn trừ tiền → BLOCKER, raise ngay và dừng phát hành.\n"
     "④ Phân biệt rõ trong spec 3 nguồn huỷ (web admin / web user / cron) và hành vi từng nguồn."],

    ["MT-18", "TRUNG BÌNH", W,
     "Bot chưa nhập nội dung 特商法 — trang public hiển thị gì?",
     "「Quản lý sản phẩm」r256:「Setting thông tin cửa hàng」— TC gốc **chỉ có tiêu đề**.\n"
     "r278 / r301:「thông tin cửa hàng ⇒ nhấn vào text thì mở thông tin của hàng」— chỉ kiểm khi ĐÃ có nội dung.\n"
     "Corpus **KHÔNG có TC** cho trường hợp bot chưa nhập.",
     "`feature-spec.md:330` §2.3: ★ **Không có bản ghi mặc định cấp hệ thống**. Nội dung phong phú quan sát "
     "trên trang public là **template mặc định do editor tự nạp khi tạo mới**.\n"
     "`feature-spec.md:1105` §9.1 mục 15 xác nhận: `detailStoreInfo():545` chỉ đọc `s_store_settings` của bot "
     "rồi render thẳng.",
     "特定商取引法 là yêu cầu PHÁP LUẬT với mọi giao dịch thương mại điện tử tại Nhật. Nếu bot bán hàng mà "
     "trang 特商法 trống thì đây là vi phạm pháp lý của khách hàng (chủ bot), không chỉ là lỗi hiển thị. "
     "Hệ thống hiện không chặn và không cảnh báo.",
     "『Trang hoàn tất & 特商法 public』TC「Bot CHƯA nhập nội dung 特商法」· "
     "『各種設定 — 特商法』TC「Nhập & lưu 事業者・特商法設定」",
     "",
     "① Chạy TC thăm dò xem trang trả về gì khi chưa nhập.\n"
     "② Chốt: có nên CHẶN công khai sản phẩm khi bot chưa nhập 特商法 không.\n"
     "③ Nếu không chặn: ít nhất cần cảnh báo ở màn quản lý sản phẩm.\n"
     "④ Xác nhận với bộ phận pháp chế trước khi chốt."],

    ["MT-19", "CAO", W,
     "Tin nhắn LINE báo thanh toán định kỳ THÀNH CÔNG có thực sự được gửi không?",
     "「Improve bill tiền univapay」r8 / r18 / r205 và「Improve bill tiền stripe」r9:\n"
     "「- send message thanh toán thành công cho user **決済が完了しました。**」— Test Result OK "
     "(nhưng chỉ ở luồng MUA/ĐỔI THẺ trên UI, không phải luồng JOB).\n"
     "Corpus **KHÔNG có TC** kiểm tin nhắn thành công ở luồng JOB BILL ĐỊNH KỲ.",
     "`feature-spec.md:1169` R13: **Tin nhắn LINE báo thanh toán định kỳ THÀNH CÔNG không bao giờ được gửi** — "
     "`sendBillInfoMessage` chỉ gửi `$textNew` (biến này chỉ được gán ở nhánh `'error'`); `$textStart` "
     "(prefix cảnh báo test) và `$textEnd` (chi tiết đơn) **không bao giờ được dùng**. Ngoài ra "
     "`sendBillInfoMessage(type='success')` cũng không được gọi ở đâu trong `handle()` "
     "(`HandleBillStripe.php:874-903`).\n"
     "`feature-spec.md:93` §1.6: tin nhắn ở môi trường test có prefix「【ご注意】これはテスト決済なので実際には"
     "課金されません」— chính là `$textStart` mà R13 nói không bao giờ được dùng.",
     "Khách đăng ký định kỳ bị trừ tiền hằng tháng mà KHÔNG nhận được thông báo nào từ LINE. Đồng thời, "
     "giao dịch ở môi trường テスト cũng không có prefix cảnh báo → khách hàng thử nghiệm có thể tưởng là "
     "giao dịch thật. Đây là 2 vấn đề riêng biệt cùng một gốc code.",
     "『Trang hoàn tất & 特商法 public』TC「Sản phẩm thuộc テスト環境 → tin nhắn LINE có prefix cảnh báo」· "
     "『Job bill định kỳ』các TC bill kỳ tiếp · 『Action & notify theo sự kiện』TC「Notify phía admin tách riêng」",
     "",
     "① Chạy job bill định kỳ trên môi trường thật, kiểm tra chat 1:1 của khách xem có tin nào không.\n"
     "② Kiểm riêng prefix cảnh báo テスト決済 ở cả luồng mua UI và luồng job.\n"
     "③ Nếu xác nhận không gửi → raise bug, mức độ CAO (khách bị trừ tiền im lặng).\n"
     "④ Chốt nội dung tin nhắn cần gửi ở luồng job (thành công / thất bại)."],

    ["MT-20", "TRUNG BÌNH", W,
     "Message lỗi thanh toán hiển thị cho khách — có nêu được lý do thật không?",
     "「Improve bill tiền univapay」r315 (TC-NEW-06 card declined):「Hiển thị message lỗi **rõ ràng** cho user "
     "(vd: 'Thẻ bị từ chối, vui lòng dùng thẻ khác'). KHÔNG silent fail」— TC mới, CHƯA có kết quả chạy.\n"
     "r316 (insufficient funds): tester ghi「**MT test không test được case lỗi do k đủ số dư**」.\n"
     "「test fix bug」r79:「báo lỗi **tiếng anh** (do bên univapay/ stripe trả về)」— Test Result OK.",
     "`feature-spec.md:1179` R18: `getMessageError` fallback **luôn rơi vào `processing_error`** → "
     "**message gốc của Stripe bị nuốt**, Admin/khách không biết lý do thật "
     "(`SalesStripePaymentController.php:1832-1836`).\n"
     "`feature-spec.md:1215` R49: `msg_error_bill`, `error_message`, `error_code` **không có màn hình nào "
     "hiển thị** → Admin không xem được lý do thanh toán thất bại.",
     "3 nguồn nói 3 kiểu: TC mới kỳ vọng message rõ ràng tiếng Việt/Nhật; TC cũ ghi nhận message tiếng Anh thô "
     "từ cổng; spec nói message gốc bị nuốt hoàn toàn. Không chốt được thì không viết được expected. "
     "Ảnh hưởng: khách không biết vì sao không mua được → mất đơn; admin không hỗ trợ được khách.",
     "『Bill UnivaPay — callback & webhook』TC「Thẻ bị từ chối (card declined)」· "
     "TC「Thẻ không đủ số dư」· 『LINE user — đổi thẻ』TC「Đổi thẻ nhập SAI THẺ」",
     "",
     "① Chạy thử vài mã lỗi phổ biến, chụp lại message THẬT hiển thị cho khách.\n"
     "② Chốt bộ message chuẩn (tiếng Nhật) cho từng nhóm lỗi.\n"
     "③ Đề xuất dev bổ sung màn hiển thị lý do lỗi cho admin (R49).\n"
     "④ Quyết định có chạy case insufficient funds không (cần môi trường sandbox riêng)."],

    ["MT-21", "TRUNG BÌNH", W,
     "Thao tác hàng loạt luôn báo thành công dù có bản ghi thất bại",
     "「Quản lý sản phẩm」r370-r373:「hủy từng hợp đồng và nhiều hợp đồng của cả stripe và univapay」— "
     "Test Result OK, nhưng KHÔNG có TC nào trộn bản ghi hợp lệ với bản ghi bị chặn.\n"
     "「Improve bill tiền univapay」r181:「các order cycle có status_webhook = 0,3,4 (đợi xử lý) thì không cho "
     "cancel ⇒ khi nhấn cancel thì **bỏ qua các order này không làm gì**」— không nói admin có được báo không.\n"
     "「ListBug」r25 ghi bug cũ:「ở màn list lịch sử tick chọn ord…」(nội dung bị cắt) — trạng thái 'Cần Re-fix'.",
     "`feature-spec.md:1193` R32: Thao tác hàng loạt **luôn trả `{\"success\": true}`** dù từng đơn lỗi; "
     "exception mỗi phần tử chỉ ghi log ⇒ Admin **không biết đơn nào thất bại** (`:3528`, `:3557`).\n"
     "`feature-spec.md:266-267` §2.2 bước 4-5 xác nhận: `cancelOrderMultiple` **luôn trả success**; "
     "`cancelCycleOrderMultiple` chỉ xử lý bản ghi `status_bill == 1 && cycle_payment != 0`.",
     "Admin tick 10 hợp đồng bấm huỷ hàng loạt, hệ thống báo thành công nhưng thực tế chỉ huỷ 7. "
     "3 hợp đồng còn lại tiếp tục bị trừ tiền mà admin tin là đã huỷ. Đây là vấn đề TIỀN BẠC và cũng là "
     "vấn đề tin cậy của thao tác hàng loạt (áp cho cả 一括返金実行 và 一括解約実行).",
     "『Hoàn tiền & hủy phía admin』TC「一括解約実行」· TC「Không cho hoàn tiền đơn đang chờ xử lý」· "
     "『Bill UnivaPay — callback & webhook』TC「Màn list 販売履歴 継続 — không cho HỦY hợp đồng đang chờ webhook」",
     "",
     "① Chạy TC trộn: tick 3 bản ghi hợp lệ + 2 bản ghi bị chặn, ghi lại thông báo và kết quả thật.\n"
     "② Chốt: hệ thống phải báo rõ 'thành công N / thất bại M' hay chỉ cần báo chung.\n"
     "③ Nếu chốt phải báo rõ → raise task cho dev.\n"
     "④ Sửa expected của TC theo quyết định."],

    ["MT-22", "THẤP", W,
     "Admin không thấy được số lần bill lỗi của hợp đồng trước khi bị tự động huỷ",
     "「Quản lý sản phẩm」r343-r345 và「Improve bill tiền univapay」r138-r154 mô tả kỹ diễn biến "
     "count_bill_error 1 → 2 → 3, nhưng toàn bộ đều verify bằng cách **đọc dữ liệu**, "
     "KHÔNG có TC nào verify qua GIAO DIỆN.",
     "`feature-spec.md:1214` R48: ⚠ **Gap UX**: `count_bill_error` **không hiển thị ở đâu** → Admin **không "
     "biết** hợp đồng đã lỗi bao nhiêu lần trước khi bị auto-cancel, chỉ thấy badge 「延滞中」.\n"
     "`feature-spec.md:766` BR-07: 3 lần lỗi liên tiếp + `auto_cancel = 1` → huỷ hợp đồng.",
     "Theo quy tắc『TC từ góc nhìn manual tester』, TC không nên dẫn bằng truy vấn dữ liệu. Nhưng nếu giao diện "
     "không hiển thị số lần lỗi thì member KHÔNG CÓ CÁCH nào verify các TC bill lỗi lần 1/2/3 bằng UI. "
     "Cần chốt cách verify thay thế (VD: đếm số dòng lỗi trong bảng 決済履歴).",
     "『Job bill định kỳ』TC「Bill LỖI lần 1」· TC「Bill LỖI lần 2 liên tiếp」· "
     "TC「Bill LỖI 3 lần liên tiếp + KHÔNG set tự động hủy」",
     "",
     "① Xác nhận trên UI: có đếm được số lần lỗi qua số dòng lỗi ở bảng 決済履歴 không.\n"
     "② Nếu được: chốt cách verify này và sửa expected của TC cho thuần UI.\n"
     "③ Nếu không: chấp nhận TC phải đọc dữ liệu, ghi rõ lý do ngoại lệ.\n"
     "④ Đề xuất dev hiển thị số lần lỗi ở màn 注文詳細."],

    ["MT-23", "CAO", W,
     "Bot đã hết hạn hợp đồng LME — job bill item của bot đó còn chạy không?",
     "「Quản lý sản phẩm」Sheet2 (khối test riêng):\n"
     "「Bot còn hạn | uni: job bill success OK | stripe: job bill success OK」\n"
     "「Bot hết hạn | uni: **job ko bill nữa** OK | stripe: **job ko bill nữa** OK」\n"
     "Tab Info dòng 12/2023:「**Bot hết hạn thì sẽ ko bill chu kỳ job hàng tháng**」.\n"
     "→ Corpus khẳng định CẢ 2 CỔNG đều dừng bill.",
     "`feature-spec.md:977-984` §7.3: **J1 (Stripe)** — `HandleBillStripe.php:102-106` bỏ qua bot "
     "`plan_type == 1 && expired_date < now() − 7 ngày` → ✅ **Đang chạy** (có 7 ngày ân hạn).\n"
     "**J2 (UnivaPay)** — `HandleSendActionTrialV2.php:165-169` → ❌ **Đã comment out**.\n"
     "⇒ 「**J2 vẫn tiếp tục trừ tiền khách hàng của những bot đã hết hạn hợp đồng LME, trong khi J1 thì không.**」\n"
     "`feature-spec.md:1159` R3 xếp là rủi ro NGHIÊM TRỌNG (thanh toán + pháp lý).",
     "⚠ **Quy tắc『ưu tiên TC mới nhất』là căn cứ YẾU ở đây**: corpus Sheet2 không ghi ngày, dòng Info liên quan "
     "là 12/2023 — CŨ hơn spec (08/2026 đọc trực tiếp từ code). Nhưng spec cũng có thể đọc nhầm nhánh comment. "
     "Lý do THẬT SỰ chọn spec làm giả thuyết ưu tiên: spec chỉ đích danh file:line của khối bị comment và "
     "phân biệt được 2 cron, trong khi corpus chỉ ghi kết quả OK ở mức 'không bill nữa' mà không nói cơ chế. "
     "Đây là rủi ro trừ tiền khách của bot đã ngừng dịch vụ → mức pháp lý.",
     "『Job bill định kỳ』TC「Bot HẾT HẠN hợp đồng LME → job bill định kỳ của item còn chạy hay dừng」· "
     "『LINE user — mở trang mua』TC「Bot HẾT HẠN hợp đồng LME quá 7 ngày → chặn trang mua」",
     "",
     "① ƯU TIÊN CAO: chạy TC riêng cho TỪNG cổng trên môi trường thật với bot đã hết hạn.\n"
     "② Nếu UnivaPay vẫn bill → BLOCKER, raise ngay.\n"
     "③ Chốt nghiệp vụ: bot hết hạn thì hợp đồng item của khách xử lý thế nào (dừng bill? huỷ? thông báo?).\n"
     "④ Xác nhận mốc ân hạn 7 ngày có áp cho cả 2 cổng không."],

    ["MT-24", "TRUNG BÌNH", W,
     "Job cứu đơn treo có thể bị chặn bởi lỗi ở tính năng khác",
     "Corpus **KHÔNG có TC** nào kiểm tình huống job cứu đơn treo gặp lỗi ở phần booking.\n"
     "「Improve bill tiền univapay」r222-r224 chỉ kiểm regression 3 tính năng booking chạy đúng, "
     "không kiểm ảnh hưởng ngược khi booking lỗi.",
     "`feature-spec.md:1190` R29: `getOrderTimeout()` đứng **cuối** `RecoverPaymentUnivapayTimeout::handle()` "
     "và **không có try/catch** → lỗi ở lesson/salon/event **chặn luôn phần sales** "
     "(`RecoverPaymentUnivapayTimeout.php:60-63`).\n"
     "`feature-spec.md:973` §7.2 J4: cứu đơn treo > 15 phút, chạy mỗi 5 phút.",
     "Nếu đúng như spec thì một lỗi dữ liệu ở booking salon có thể khiến TOÀN BỘ đơn bill item bị treo vĩnh viễn "
     "(khách đã bị trừ tiền nhưng đơn không bao giờ chuyển sang thành công). Đây là phụ thuộc chéo nguy hiểm "
     "mà corpus không phủ.",
     "『Job cứu đơn treo & quét kết quả』TC「Job quét gặp lỗi ở đơn của tính năng khác」",
     "",
     "① Chốt có đưa TC này vào bộ chạy không (cần tạo dữ liệu lỗi ở booking — có thể khó).\n"
     "② Nếu không chạy được: đề xuất dev bọc try/catch riêng cho từng phần và đảo thứ tự xử lý.\n"
     "③ Bổ sung TC monitor phát hiện đơn treo lâu bất thường."],

    ["MT-25", "TRUNG BÌNH", W,
     "Action「2回目以降決済時」có bắn ở kỳ 3, 4, 5… không?",
     "「Quản lý sản phẩm」r365:「action khi bill lần 2 ⇒ **gửi action bill lần 2 cho user nếu có**」— OK.\n"
     "「Quản lý sản phẩm」r366:「khi bill các lần tiếp theo (sau lần 2) ⇒ **không action**」— OK.\n"
     "→ 2 dòng LIỀN NHAU trong cùng tab, cùng đợt test, nói ngược nhau về ý nghĩa của slot.",
     "`feature-spec.md:229` SCR-BIL-13: slot tên là 「**2回目以降**決済時」 (từ kỳ 2 TRỞ ĐI).\n"
     "`feature-spec.md:726` Field Matrix #38: 「稼働回数」 ×7 — `1` = 1度のみ (mặc định) → **chỉ bắn khi "
     "`count_action_* == 0`**; `0` = 何度でも.\n"
     "→ Theo spec, việc bắn ở kỳ 3+ phụ thuộc setting 稼働回数, KHÔNG phải quy tắc cứng.",
     "Tên slot nói 'từ lần 2 trở đi' nhưng r366 nói chỉ bắn đúng lần 2. Nhiều khả năng r366 mô tả trường hợp "
     "稼働回数 =「1度のみ」(mặc định) và tester tưởng đó là quy tắc chung. Nếu không chốt, member sẽ viết "
     "expected sai cho cấu hình 何度でも và bỏ sót bug thật.",
     "『Action & notify theo sự kiện』TC「Action 2回目以降決済時 bắn từ kỳ 2 trở đi」· "
     "TC「Action 2回目以降決済時 ở kỳ 3 trở đi CÓ bắn không?」",
     "",
     "① Chạy ma trận: kỳ 2/3/4 × 稼働回数 (1度のみ / 何度でも) = 6 lượt, ghi kết quả từng lượt.\n"
     "② Chốt hành vi đúng và sửa expected.\n"
     "③ Ghi chú vào tab gốc rằng r366 chỉ đúng với cấu hình 1度のみ (nếu xác nhận đúng vậy)."],

    ["MT-26", "TRUNG BÌNH", W,
     "Thông báo cho app mobile có thực sự được gửi không?",
     "「Quản lý sản phẩm」r381-r387 liệt kê 7 sự kiện cần notify (mua thành công/thất bại của 単品 và 継続, "
     "cancel, thanh toán định kỳ thành công/lỗi) — nhưng r382 và r384 (**mua không thành công**) "
     "**KHÔNG có Test Result** → chưa từng được test.\n"
     "「ListBug」r8 ghi bug cũ:「case bill fail không thấy có notify (check bảng mobile_notify không có bản ghi)」"
     "— trạng thái Fixed/OK.",
     "`feature-spec.md:1197` R36: ⚠ **`ENABLE_HANDLE_PUSH_MESSAGE_NOTIFY` mặc định TẮT** → thông báo do "
     "sales ghi ra **tồn đọng** nếu không có instance khác bật cờ này "
     "(`ConfigFile.java:121`, `AppMain.java:224-226`).\n"
     "`feature-spec.md:1011` §7.5 S2: 「⚠ **TẮT mặc định**」.\n"
     "`feature-spec.md:1053` §7.6: 「⚠ S2 tắt ⇒ `mobile_notify` do sales ghi ra sẽ **tồn đọng**」.",
     "TC kiểm notify sẽ FAIL trên môi trường có cờ tắt và PASS trên môi trường bật — kết quả không tái lập được. "
     "Member không biết FAIL là do bug hay do cấu hình môi trường. Cần chốt môi trường chuẩn để chạy nhóm TC này.",
     "『Action & notify theo sự kiện』TC「Notify phía admin tách riêng theo 単品 và 継続, đủ 5 sự kiện」",
     "",
     "① Xác nhận với dev/vận hành cờ này đang bật hay tắt trên môi trường sẽ chạy test.\n"
     "② Nếu tắt: chốt bật trước khi chạy, hoặc loại nhóm TC notify khỏi bộ chạy và ghi rõ lý do.\n"
     "③ Bổ sung điều kiện tiền đề 'cờ push notify đang bật' vào các TC liên quan."],

    ["MT-27", "TRUNG BÌNH", W,
     "MUA MỚI 継続 thất bại — có gửi action「決済エラー発生時」không?",
     "「test fix bug」r51 / r57 (Bug #26850, 10/2024):「Check sp bill chu kỳ / mua fail ⇒ "
     "**không gửi action của bill fail**」— Test Result OK ở cả Stripe và UnivaPay.\n"
     "「Improve bill tiền stripe」r17-r18 / r25-r26 / r33-r34 (10/2025, MỚI HƠN):「mua mới fail ⇒ "
     "Xóa bản ghi 2 bảng ... **- send action case bill fail** - send notify case bill fail」— Test Result OK.\n"
     "→ 2 đợt test cách nhau 1 năm cho 2 kết quả NGƯỢC NHAU.",
     "`feature-spec.md:1149-1150` §10 và bảng slot action (`:229`) không nêu rõ ranh giới giữa 'lỗi khi MUA MỚI' "
     "và 'lỗi khi BILL ĐỊNH KỲ'.\n"
     "`feature-spec.md:766` BR-07 chỉ mô tả action `bill_error` trong ngữ cảnh 請求エラー của kỳ định kỳ.",
     "Bug #26850 ra đời chính vì khách nhận nhầm tin báo lỗi thanh toán — nếu bản 10/2025 khôi phục việc gửi "
     "action khi mua mới thất bại thì có nguy cơ TÁI PHÁT bug cũ. Quy tắc『ưu tiên TC mới nhất』nghiêng về "
     "bản 10/2025, nhưng bản cũ là kết quả của một BUG ĐÃ SỬA → cần Leader cân nhắc chứ không áp máy móc.",
     "『Action & notify theo sự kiện』TC「Bug #26850 — mua THẤT BẠI thì KHÔNG được gửi action mua thành công」· "
     "『Bill Stripe — tạo order trước』TC「Stripe 継続 — bill FAIL khi mua mới」· "
     "『LINE user — mua 継続』TC「Mua 継続 thất bại」",
     "",
     "① Đọc lại nội dung Bug #26850 để biết chính xác hành vi đã được chốt năm 2024.\n"
     "② Chạy TC thăm dò: mua mới 継続 thất bại, kiểm tra chat 1:1 của khách.\n"
     "③ Chốt: mua mới thất bại có gửi action bill lỗi không.\n"
     "④ Nếu chốt 'không gửi' mà thực tế có gửi → raise bug tái phát #26850."],

    ["MT-28", "THẤP", W,
     "Job monitor — ngưỡng lệch ngày gia hạn của ITEM là bao nhiêu?",
     "「Monitor bill tiền」khối **BOT** r61-r64 quy định rõ ngưỡng: lệch **< 7 ngày → không notify**, "
     "**= 7 ngày → không notify**, **> 7 ngày → có notify**.\n"
     "「Monitor bill tiền」khối **ITEM** r89-r90 chỉ ghi:「expired_date đúng ⇒ không notify / expired_date "
     "**không đúng** ⇒ có notify」— **KHÔNG nêu ngưỡng**.",
     "`spec-features/admin/bill-item/job/job-spec.md` mô tả 5 cron của FA-026 (J1-J5) nhưng "
     "**KHÔNG có job monitor** này — job monitor nằm ở phạm vi khác (giám sát chung bot + item).\n"
     "`feature-spec.md:964-976` §7.2 liệt kê 5 cron, không có cron monitor.",
     "Vùng mù giữa 2 phạm vi: job monitor giám sát CẢ hợp đồng bot (FA-031) lẫn hợp đồng item (FA-026), "
     "nhưng spec của FA-026 không mô tả nó. Không có ngưỡng thì member không biết lệch 1 ngày có phải bug không "
     "→ expected không đo lường được. Cảnh báo sai/thiếu đều làm giảm giá trị của hệ thống giám sát tiền.",
     "『Job monitor bill tiền』TC「Monitor — item bill thành công nhưng NGÀY GIA HẠN sai」",
     "",
     "① Xác nhận với dev ngưỡng áp cho phần ITEM (có dùng chung ngưỡng 7 ngày với phần BOT không).\n"
     "② Chốt và ghi vào expected của TC.\n"
     "③ Quyết định: job monitor thuộc kho TCs của tính năng nào (đề xuất tách kho riêng cho JOB giám sát)."],

    ["MT-29", "THẤP", W,
     "Job monitor có cảnh báo khi item bill THẤT BẠI không?",
     "「Monitor bill tiền」r6 (bản **2023**):「Check bill tiền item chu kỳ / case bill fail ⇒ **có notify**」— OK.\n"
     "「Monitor bill tiền」r91 (bản **11/2025**):「Check case item bill fail ⇒ **Không notify case bill fail nữa**」.\n"
     "→ Mâu thuẫn niên đại rõ ràng, cách nhau 2 năm.",
     "Spec của FA-026 **không mô tả job monitor** (xem MT-28) nên không có căn cứ đối chiếu.",
     "Đây là trường hợp quy tắc『ưu tiên TC mới nhất』áp dụng ĐƯỢC và RÕ RÀNG (2023 vs 11/2025, khác nhau 2 năm, "
     "khối 11/2025 là bản viết lại toàn bộ). Đưa vào bảng vì việc bỏ cảnh báo bill fail là thay đổi HÀNH VI "
     "GIÁM SÁT — nếu bỏ nhầm thì vận hành mất khả năng phát hiện sự cố thanh toán hàng loạt.",
     "『Job monitor bill tiền』TC「Monitor — item bill FAIL thì KHÔNG cảnh báo nữa」",
     "",
     "① Xác nhận lý do bỏ cảnh báo bill fail (có thể do quá nhiều cảnh báo nhiễu).\n"
     "② Chốt: giữ nguyên (không cảnh báo) hay cảnh báo có ngưỡng (VD > N đơn fail/ngày).\n"
     "③ Loại TC r6 (bản 2023) khỏi kho, ghi vào mục 'nguồn đã loại'."],

    ["MT-30", "THẤP", W,
     "販売履歴 hiển thị ngày theo cột A nhưng LỌC theo cột B",
     "「Quản lý sản phẩm」r190 / r216:「filter theo ngày bill」— TC gốc **chỉ có tiêu đề**, không nêu lọc theo "
     "trường nào.",
     "`feature-spec.md:733` Field Matrix #46: 「販売日時」danh sách đọc từ `created_at`, ⚠ nhưng "
     "**lọc khoảng ngày lại dùng `payment_date`** (単品) hoặc điều kiện OR giữa `last_bill_time` và "
     "`c_register_date` (継続).\n"
     "`feature-spec.md:253-254` §2.2 xác nhận lại cho từng nhánh truy vấn.\n"
     "`feature-spec.md:244` SCR-BIL-14: màn 商品詳細 lại lọc theo **THÁNG** và dùng `payment_date` để hiển thị.",
     "Cột hiển thị và cột lọc khác nhau → đơn nằm ở ranh giới ngày có thể hiện ngày X nhưng không xuất hiện khi "
     "lọc đúng ngày X. Ngoài ra cùng một đơn hiển thị ngày KHÁC NHAU giữa màn 販売履歴 và màn 商品詳細. "
     "Member đối chiếu 2 màn sẽ raise bug nhầm.",
     "『Màn 販売履歴』TC「Filter theo KHOẢNG NGÀY bill」· "
     "『Màn 商品詳細 & Preview』TC「商品詳細 — bảng 販売履歴 lọc theo THÁNG」",
     "",
     "① Chạy TC biên: tạo đơn có 2 mốc thời gian lệch nhau, lọc đúng ngày và kiểm tra.\n"
     "② Chốt: thống nhất về 1 trường (khuyến nghị dùng cùng trường cho cả hiển thị và lọc).\n"
     "③ Nếu giữ nguyên: ghi rõ vào expected để member không raise nhầm."],

    ["MT-31", "THẤP", W,
     "Danh sách folder trong modal 絞り込み khác với panel folder ở màn danh sách",
     "「Quản lý sản phẩm」r193 / r219:「Modal filter / filter theo sản phẩm (chọn sp cần filter)」— "
     "TC gốc **chỉ có tiêu đề**, không kiểm thứ tự và phạm vi folder.",
     "`feature-spec.md:265` §2.2 bước 2: ⚠ modal 絞り込み dùng `ORDER BY position ASC`, **KHÔNG lọc "
     "`type_payment`** → thứ tự folder khác panel sidebar (`ORDER BY position DESC, id DESC`, có lọc).\n"
     "`feature-spec.md:159` §2.1: folder 単品 và 継続 **tách biệt hoàn toàn** theo `type_payment`.",
     "Ở sub-tab 単品, modal lọc lại hiện cả folder của 継続 (và ngược lại), thứ tự cũng đảo so với panel bên trái. "
     "Admin dễ chọn nhầm folder. Đây là lỗi nhất quán UI, mức độ thấp nhưng gây khó chịu khi dùng thường xuyên.",
     "『Màn 販売履歴』TC「Modal 絞り込み — lọc theo SẢN PHẨM cụ thể」",
     "",
     "① Chạy TC bổ sung: mở modal ở sub-tab 単品, kiểm tra có folder của 継続 không và thứ tự folder.\n"
     "② Nếu đúng như spec → raise bug mức MINOR.\n"
     "③ Bổ sung expected về thứ tự và phạm vi folder vào TC."],

    ["MT-32", "TRUNG BÌNH", W,
     "Cột「決済回数」ở bảng 決済履歴 có phản ánh đúng số kỳ đã thanh toán không?",
     "「Quản lý sản phẩm」r229:「List các lần bill tiền」— TC gốc **chỉ có tiêu đề**, không nêu ý nghĩa cột "
     "決済回数.\nCorpus KHÔNG có TC nào kiểm 決済回数 khi hợp đồng có kỳ lỗi xen giữa.",
     "`feature-spec.md:304` SCR-BIL-19 bảng cột: 「決済回数」★ **KHÔNG có cột dữ liệu** — chỉ là `index + 1` "
     "trong vòng lặp hiển thị. ⚠ Nếu 1 kỳ lỗi sinh nhiều bản ghi thì số này **không phản ánh** `number_payment`.\n"
     "`feature-spec.md:744` Field Matrix #58 lặp lại.\n"
     "`feature-spec.md:1211` L2: db-hint từng ghi nhầm đây là cột `INT`.",
     "Hợp đồng bill lỗi 2 lần rồi thành công sẽ hiện 決済回数 = 3 ở dòng cuối, trong khi khách mới thanh toán "
     "được 1 kỳ. Với hợp đồng có giới hạn số lần bill, admin nhìn số này sẽ tưởng hợp đồng sắp kết thúc. "
     "Ảnh hưởng trực tiếp tới việc đối soát số kỳ đã thu tiền.",
     "『Màn 販売履歴』TC「決済回数 khi hợp đồng có kỳ LỖI xen giữa」· TC「注文詳細 継続 hiển thị bảng 決済履歴」",
     "",
     "① Tạo hợp đồng có kỳ lỗi xen giữa, chụp lại bảng 決済履歴.\n"
     "② Chốt: cột này nên hiển thị số thứ tự dòng hay số kỳ đã thanh toán thành công.\n"
     "③ Nếu đổi ý nghĩa → raise task cho dev.\n"
     "④ Sửa expected của TC theo quyết định."],

    ["MT-33", "TRUNG BÌNH", W,
     "Thống kê doanh số theo tháng KHÔNG được cập nhật khi hoàn tiền / huỷ",
     "「Quản lý sản phẩm」r202-r204 (hoàn tiền) và r230-r231 (huỷ hợp đồng) — Test Result OK, "
     "nhưng **KHÔNG có TC nào kiểm số liệu thống kê tháng sau khi hoàn tiền**.",
     "`feature-spec.md:1165` R9: **Cập nhật `s_monthly_item` khi refund/huỷ đã bị comment out ở V2** → "
     "**thống kê tháng sai lệch có hệ thống** (`:3120-3189`, `:3578-3617`). Nhánh V1 vẫn còn logic này.\n"
     "`feature-spec.md:1217` R51: `s_monthly_item` **không xuất hiện trên bất kỳ màn hình V2 nào** → "
     "kết hợp R9 ⇒ dữ liệu bảng này ở V2 **không đáng tin**.\n"
     "`feature-spec.md:291` §2.1 xác nhận trong sơ đồ luồng hoàn tiền.",
     "Nếu bảng thống kê tháng không hiển thị ở màn hình V2 nào thì member KHÔNG THỂ verify bằng UI, và cũng "
     "không rõ dữ liệu sai này có bị dùng ở báo cáo nào khác (admin portal? xuất hoá đơn?) hay không. "
     "Cần chốt phạm vi ảnh hưởng trước khi quyết có test hay không.",
     "『Hoàn tiền & hủy phía admin』TC「Hoàn tiền — chọn thực hiện trả tiền tự động」· "
     "TC「Sau khi admin hủy hợp đồng → các bộ đếm của sản phẩm cập nhật đúng」",
     "",
     "① Xác nhận với dev: dữ liệu thống kê tháng còn được dùng ở đâu (admin portal, báo cáo doanh thu?).\n"
     "② Nếu còn dùng → raise bug mức CAO (số liệu doanh thu sai có hệ thống).\n"
     "③ Nếu không dùng → chốt bỏ khỏi phạm vi test, ghi rõ vào báo cáo.\n"
     "④ Đối chiếu với các bộ đếm CÓ hiển thị (販売数, sum_sales) xem có bị ảnh hưởng không."],

    ["MT-34", "THẤP", W,
     "Danh sách cột của file CSV xuất chưa được xác định",
     "「test fix bug」r299-r335 (Bug #32729) chỉ kiểm **TÊN FILE** với các ký tự đặc biệt, "
     "**KHÔNG có TC nào kiểm NỘI DUNG cột** của file CSV.\n"
     "「Quản lý sản phẩm」r245-r248 (Feature #30651) chỉ kiểm 2 cột MỚI được thêm "
     "(số lượng mua và tổng số tiền bill) cho 単品.",
     "`feature-spec.md:1120` §9.2 mục 16: ⚠ **Một phần** — đã biết định dạng tên file và class xuất, "
     "**Chưa liệt kê đủ danh sách cột**. Đề xuất: đọc trọn `CycleOrderHistoryExportV2.php` + "
     "`OrderHistoryExportV2.php`.",
     "Không có danh sách cột chuẩn thì không viết được TC verify nội dung file — member chỉ kiểm được "
     "'tải về được' chứ không kiểm được 'đúng dữ liệu'. File CSV này được dùng để đối soát doanh thu, "
     "sai cột hoặc thiếu cột là rủi ro thật.",
     "『Export CSV lịch sử』TC「Export CSV 販売履歴 単品」· TC「Export CSV 販売履歴 継続」· "
     "TC「Export CSV chỉ các đơn ĐÃ TICK CHỌN」",
     "",
     "① Xuất 1 file CSV mẫu của mỗi loại (単品 / 継続), liệt kê đủ cột thật.\n"
     "② Bổ sung danh sách cột vào `feature-spec.md` §9.2 mục 16 → đóng Gap này của spec.\n"
     "③ Viết bổ sung TC verify nội dung từng cột (đặc biệt cột số tiền và ngày).\n"
     "④ Đối chiếu cột CSV với cột hiển thị trên màn 販売履歴."],

    ["MT-35", "THẤP", W,
     "Export CSV có thể trả file rỗng khi tên hiển thị của bot trống",
     "Corpus **KHÔNG có TC** nào cho trường hợp tên hiển thị của bot rỗng. "
     "Toàn bộ TC của Bug #32729 đều giả định bot CÓ tên.",
     "`feature-spec.md:1180` R19: **Export CSV trả `null`** khi `bots.view_name` rỗng → `$fileName` không "
     "được gán, trình duyệt nhận **response rỗng** (`:6944`, `:6975`).",
     "Đây là trường hợp biên mà cả corpus lẫn TC mới đều bỏ sót. Nếu tái hiện được thì admin bấm xuất CSV "
     "không thấy gì xảy ra và không có thông báo lỗi — rất khó hỗ trợ khi khách báo. "
     "Cần chốt xem tên hiển thị của bot có thể rỗng trong thực tế không.",
     "『Export CSV lịch sử』TC「Bot có view_name RỖNG → export CSV có bị trả file rỗng không」",
     "",
     "① Xác nhận: hệ thống có cho phép bot có tên hiển thị rỗng không.\n"
     "② Nếu có thể rỗng: chạy TC, nếu tái hiện thì raise bug.\n"
     "③ Nếu không thể rỗng: loại TC khỏi bộ chạy, ghi rõ lý do."],

    ["MT-36", "CAO", W,
     "Nội dung 特商法 được render thẳng — có nguy cơ XSS không?",
     "Corpus **KHÔNG có TC bảo mật** nào cho editor 特商法. "
     "「Quản lý sản phẩm」r46 chỉ có TC「nhập Source code」ở editor 商品情報 với expected "
     "「màn preview và phía user hiển thị đúng」— tức kỳ vọng HTML được render, không kiểm tính an toàn.",
     "`feature-spec.md:440-443` SCR-BIL-25: `@detailStoreInfo():545` đọc `s_store_settings.info_store` và "
     "**render thẳng `{!! !!}`** (cú pháp không escape của Blade).\n"
     "`feature-spec.md:1196` R35: `saveSettings` nhận **toàn bộ `$request->input()`**, model `$guarded = []` → "
     "**mass assignment không giới hạn** (`:776-790`).\n"
     "`feature-spec.md:346` §2.4: ⚠ toàn bộ prefix `/v2` **KHÔNG có middleware xác thực**.",
     "Trang 特商法 là trang PUBLIC mà mọi khách hàng LINE đều mở. Nếu nội dung không được lọc thì một admin "
     "(hoặc staff, hoặc kẻ chiếm được phiên admin) có thể chèn mã chạy trên trình duyệt của mọi khách hàng. "
     "Đây là rủi ro bảo mật ảnh hưởng người dùng cuối, không chỉ nội bộ.",
     "『各種設定 — 特商法』TC「Editor 特商法 hỗ trợ nhập Source code → kiểm tra nội dung HTML được render an toàn」",
     "",
     "① Chốt có đưa TC bảo mật vào bộ chạy không (liên quan MT-02).\n"
     "② Nếu chạy: thực hiện trên môi trường test, KHÔNG chạy trên môi trường thật.\n"
     "③ Nếu tái hiện → raise bug mức BLOCKER, đề xuất dev lọc HTML đầu vào (whitelist thẻ).\n"
     "④ Áp cùng cách xử lý cho các editor khác của tính năng (商品案内, ご確認事項, 解約案内)."],

    ["MT-37", "THẤP", W,
     "Huỷ liên kết cổng thanh toán không xoá hết khoá của môi trường test",
     "Corpus **KHÔNG có TC** nào cho thao tác huỷ liên kết cổng thanh toán. "
     "「Màn liên kết bill tiền」r8 chỉ nhắc「check hủy liên kết -> liên kết lại ⇒ vẫn theo setting cũ khi chưa "
     "xóa liên kết」ở ngữ cảnh setting brand card.",
     "`feature-spec.md:1201` R40: `unlinkPaymentMethod` **không xoá nhóm khoá test UnivaPay** "
     "(`univapay_app_test_id`, `univapay_app_token_test`, `univapay_secret_test` vẫn còn sau khi 'huỷ liên kết') "
     "(`:6867-6890`).\n"
     "`feature-spec.md:337` §2.3: 「⚠ **Không xoá nhóm khoá test UnivaPay**」.",
     "Admin nghĩ đã ngắt hoàn toàn kết nối với cổng thanh toán nhưng khoá môi trường test vẫn còn lưu. "
     "Nếu bot được chuyển giao cho chủ khác thì đây là rò rỉ thông tin xác thực. Mức độ thấp vì là khoá test, "
     "nhưng vẫn là dữ liệu nhạy cảm.",
     "『Liên kết UnivaPay』TC「Hủy liên kết cổng thanh toán — yêu cầu nhập mật khẩu admin」",
     "",
     "① Chạy TC huỷ liên kết, sau đó kiểm tra màn hình liên kết còn hiện thông tin môi trường test không.\n"
     "② Nếu còn → raise bug mức MINOR.\n"
     "③ Bổ sung TC huỷ liên kết cho cả Stripe (spec nói Stripe xoá 6 cột, UnivaPay xoá 4 cột)."],

    ["MT-38", "TRUNG BÌNH", W,
     "Danh sách màn hình / thao tác mà tài khoản Staff được phép — chưa xác định",
     "「Màn liên kết bill tiền」r31 / r41 / r71 ·「Improve bill tiền stripe」r62 ·「Improve bill tiền univapay」"
     "r274 / r290 đều có dòng「**Check account staff**」— TC gốc **CHỈ CÓ TIÊU ĐỀ**, "
     "KHÔNG có kết quả mong đợi, KHÔNG có Test Result.",
     "`feature-spec.md:31` §1.2: Staff bị chặn theo **whitelist route** (`BasicAccess.php:38-51`); route ngoài "
     "whitelist → redirect kèm 「この権限は許可されていません。」. ⚠ Quyền là **all-or-nothing theo route** — "
     "không có phân quyền chi tiết xem/sửa/xoá. 「Danh sách route cụ thể **chưa xác minh** (tin cậy Trung bình)」.\n"
     "`feature-spec.md:1104` §9.1 mục 14 và `:1146` §9.4 mục 3 xác nhận lại: **chưa xác minh**.",
     "Đây là vùng trống của CẢ corpus lẫn spec. Staff là vai trò thật đang được dùng. Không biết staff được "
     "làm gì thì không viết được expected — 6 TC 'Check account staff' trong corpus sẽ mãi không chạy được. "
     "Rủi ro thực tế: staff có thể hoàn tiền / huỷ hợp đồng / đổi liên kết cổng thanh toán mà không ai kiểm soát.",
     "『Phân quyền & môi trường』TC「Tài khoản STAFF truy cập màn 商品販売」",
     "",
     "① Lấy danh sách route trong whitelist từ dev (hoặc test thực nghiệm từng thao tác bằng tài khoản staff).\n"
     "② Lập bảng ma trận: thao tác × vai trò (chủ tài khoản / staff), chốt với Leader.\n"
     "③ Bổ sung bảng này vào `feature-spec.md` §1.2 → đóng Gap §9.4 mục 3.\n"
     "④ Viết lại 6 TC 'Check account staff' với expected cụ thể theo bảng đã chốt."],

    ["MT-39", "CAO", W,
     "Endpoint thanh toán và bill-item không có lớp xác thực — rủi ro thao tác chéo bot",
     "Corpus **KHÔNG có TC** nào ở tầng API cho bill item.",
     "`feature-spec.md:1161` R5: **Endpoint thanh toán + bill-item AJAX hoàn toàn KHÔNG có middleware auth** — "
     "nhóm route `web.php:3824-3962` gồm cả endpoint **huỷ/hoàn tiền 1 đơn** (`:3849`). "
     "Chỉ dựa vào `botIdCurrent` gửi từ client.\n"
     "`feature-spec.md:1168` R12: **IDOR** — `orderHistoryDetail` không lọc `bot_id` (`:1099`); nhiều endpoint V1 "
     "update không lọc `bot_id`.\n"
     "`feature-spec.md:290` §2.1: ⚠ EP-25 POST `/ajax/cancel-order-v2` **KHÔNG có middleware auth**.\n"
     "`feature-spec.md:1224` R58: middleware `https_protocol` hiện là **no-op**.",
     "Nếu đúng như spec thì bất kỳ ai biết id đơn hàng đều có thể HOÀN TIỀN hoặc HUỶ HỢP ĐỒNG của bot khác — "
     "tác động tiền bạc trực tiếp và không cần đăng nhập. Đây là mức nghiêm trọng cao nhất về bảo mật trong "
     "danh sách. Corpus hoàn toàn không phủ vùng này.\n"
     "★ Lưu ý quy tắc dự án: bug quyền ở tầng API phải rà **TẤT CẢ màn sibling cùng lưới phân quyền ở TẦNG API**, "
     "không chỉ màn 商品販売.",
     "『Phân quyền & môi trường』TC「Truy cập TRỰC TIẾP API bill-item bằng tài khoản không có quyền」",
     "",
     "① ƯU TIÊN CAO: chốt có đưa TC này vào bộ chạy không (liên quan MT-02, MT-36).\n"
     "② Nếu chạy và tái hiện được → BLOCKER, raise ngay, cân nhắc dừng phát hành.\n"
     "③ Mở rộng rà soát sang các màn khác dùng chung nhóm route không auth (booking event/salon/lesson).\n"
     "④ Đề xuất dev bổ sung middleware auth + kiểm tra bot_id ở mọi endpoint ghi dữ liệu."],

    ["MT-40", "CAO", W,
     "Upload ảnh sản phẩm không kiểm tra loại file trước khi lưu",
     "「Quản lý sản phẩm」r419-r420 có 2 TC biên: ảnh **0KB** (báo lỗi, không upload) và ảnh **không có phần "
     "mở rộng** (upload thành công, hiển thị được) — Test Result OK step.\n"
     "→ Corpus xác nhận file KHÔNG CÓ ĐUÔI vẫn upload được, nhưng **KHÔNG có TC** thử file không phải ảnh.",
     "`feature-spec.md:1195` R34: `uploadFile` **không validate MIME/kích thước trước khi `move()`** — "
     "chỉ kiểm tra **sau khi** đã lưu vào thư mục `0777` (`:569-588`).\n"
     "`feature-spec.md:220` §2.1: lưu vào `public_path(...)`, tạo thư mục `0777`, resize 2048px, "
     "bỏ qua `image/svg+xml`. ⚠ **Không validate MIME/kích thước trước khi `move()`**.\n"
     "`feature-spec.md:711` Field Matrix #16: ≤5 ảnh **(client)**; resize 2048px (server).",
     "Kết hợp 2 dữ kiện: (a) corpus xác nhận file không đuôi vẫn upload được, (b) spec nói không kiểm MIME "
     "trước khi lưu vào thư mục public quyền 0777. Nếu file mã nguồn được lưu vào thư mục public và truy cập "
     "được qua trình duyệt thì đây là lỗ hổng thực thi mã từ xa. Cần xác minh gấp.",
     "『Phân quyền & môi trường』TC「Upload file KHÔNG PHẢI ảnh qua ô upload ảnh sản phẩm」· "
     "『Ảnh sản phẩm』TC「Upload ảnh KHÔNG có phần mở rộng」",
     "",
     "① ƯU TIÊN CAO: chạy TC thăm dò trên môi trường TEST (không chạy trên môi trường thật).\n"
     "② Kiểm 2 điều kiện: file có lưu được không, và có truy cập trực tiếp qua URL được không.\n"
     "③ Nếu cả 2 đều đúng → BLOCKER, raise ngay.\n"
     "④ Đề xuất dev: kiểm MIME trước khi lưu + đặt quyền thư mục chặt hơn + chặn thực thi ở thư mục upload."],
]
