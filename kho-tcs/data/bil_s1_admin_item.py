# -*- coding: utf-8 -*-
"""FA-026 商品販売 (Bill tiền item) — Nhóm 1-10: Quản trị sản phẩm phía admin.

Nguồn chính: 12. TCsLine_Item / tab「Quản lý sản phẩm」(02/2023 → 02/2026, tab master còn sống).
Bổ sung: tab「test fix bug」(bug #26719 preview, bug #31871 表示設定, bug #33732 ảnh),
         tab「Test invoice (stripe)」(setting thuế), tab「Improve bill tiền stripe」(#35992 stock).
"""
from _common import tc

ADM = "- Đăng nhập admin (主管理者) bot A, mở /basic/sales/index → tab「商品一覧」"
ADM1 = ADM + "\n- Đang ở sub-tab「単品商品」, toggle môi trường =「テスト環境」"
ADM2 = ADM + "\n- Đang ở sub-tab「継続商品」, toggle môi trường =「テスト環境」"
LINKED = "- Bot A đã liên kết CẢ Stripe và UnivaPay (s_strip_bot có đủ khoá test)"

S1 = [
    # ═════════════════════ 1. Folder sản phẩm ═════════════════════
    tc("Folder sản phẩm", "FUNC-001", "Normal",
       "Tạo folder ở tab 単品 → chỉ hiện ở tab 単品, KHÔNG hiện ở tab 継続",
       ADM1,
       "1. Ở panel folder trái click「新規フォルダ」\n2. Nhập tên「単品フォルダA」→ Lưu\n"
       "3. Quan sát panel folder tab 単品\n4. Chuyển sang sub-tab「継続商品」→ quan sát panel folder",
       "Tên folder:「単品フォルダA」",
       "- Tab 単品: folder「単品フォルダA (0)」xuất hiện ở panel trái\n"
       "- Tab 継続: KHÔNG có folder này (folder tách biệt theo loại)\n"
       "- Reload trang, folder vẫn còn đúng tab",
       note="Nguồn: Quản lý sản phẩm r4「Dùng chung folder => chọn loại sp nào thì hiện đúng list sp đấy」. "
            "Spec feature-spec.md §2.1 nói s_categories.type_payment 0=単品 / 2=継続 tách biệt hoàn toàn."),

    tc("Folder sản phẩm", "FUNC-001", "Normal",
       "Tạo folder ở tab 継続 → chỉ hiện ở tab 継続",
       ADM2,
       "1. Click「新規フォルダ」\n2. Nhập tên「継続フォルダB」→ Lưu\n"
       "3. Quan sát panel folder tab 継続\n4. Chuyển sang sub-tab「単品商品」",
       "Tên folder:「継続フォルダB」",
       "- Tab 継続: folder「継続フォルダB (0)」xuất hiện\n- Tab 単品: KHÔNG có folder này",
       note="Nguồn: r4. Đối chiếu spec §9.1 mục 9."),

    tc("Folder sản phẩm", "FUNC-002", "Normal",
       "Đổi tên folder → tên mới hiển thị ngay, số đếm (N) giữ nguyên",
       ADM1 + "\n- Có folder「単品フォルダA」chứa 2 sản phẩm",
       "1. Click icon sửa của folder「単品フォルダA」\n2. Đổi tên thành「セール商品」→ Lưu\n3. Reload trang",
       "Tên mới:「セール商品」(6 ký tự)",
       "- Panel folder hiển thị「セール商品 (2)」\n- Danh sách sản phẩm bên trong không đổi\n"
       "- Sau reload tên vẫn là「セール商品」",
       note="Nguồn: r6「edit」. ⚠ Spec R20 cảnh báo renameGroup update nhầm bảng `category` — "
            "nhánh này UI không dùng (UI dùng addAndEditGroup), cần verify không có side effect sang folder tính năng khác."),

    tc("Folder sản phẩm", "FUNC-004", "Abnormal",
       "Xóa folder đang chứa sản phẩm → xóa luôn TOÀN BỘ sản phẩm bên trong",
       ADM1 + "\n- Folder「削除テスト」chứa đúng 2 sản phẩm 単品 chưa có đơn nào",
       "1. Ghi lại id 2 sản phẩm trong folder\n2. Click icon xóa folder「削除テスト」→ xác nhận\n"
       "3. Quan sát panel folder + bảng sản phẩm\n4. Mở lại URL商品ページ của 2 sản phẩm vừa bị xóa (phía LINE)",
       "Folder「削除テスト」có 2 sản phẩm",
       "- Folder biến mất khỏi panel\n- 2 sản phẩm KHÔNG còn ở bất kỳ folder nào (kể cả 未分類)\n"
       "- Mở link商品ページ của sản phẩm đã xóa → hiện「商品が非公開か、存在していません」",
       note="Nguồn: r7「xóa」. Spec §2.1 SCR-BIL-03: deleteGroup xóa toàn bộ sản phẩm bên trong (HARD DELETE). "
            "TC gốc chỉ có tiêu đề「xóa」— kết quả mong đợi do AI viết theo spec, CẦN LEADER XÁC NHẬN."),

    tc("Folder sản phẩm", "FUNC-005", "Normal",
       "Sắp xếp folder bằng kéo-thả → thứ tự mới giữ sau reload",
       ADM1 + "\n- Có đúng 3 folder 単品: F1, F2, F3 (theo thứ tự hiện tại)",
       "1. Kéo F3 lên vị trí đầu tiên\n2. Lưu / đóng modal sắp xếp\n3. Reload /basic/sales/index\n"
       "4. Đăng nhập bằng trình duyệt khác, mở lại màn hình",
       "Thứ tự mong muốn: F3 → F1 → F2",
       "- Panel folder hiển thị đúng thứ tự F3 → F1 → F2\n- Sau reload thứ tự giữ nguyên\n"
       "- Trình duyệt khác cũng thấy thứ tự mới (đã ghi DB, không phải cookie)",
       note="Nguồn: r8「sort」. TC gốc chỉ có tiêu đề — kết quả mong đợi do AI viết, CẦN LEADER XÁC NHẬN."),

    tc("Folder sản phẩm", "STATE-001", "Normal",
       "Folder đang mở được ghi nhớ qua cookie folder_sales, KHÔNG ghi DB",
       ADM1 + "\n- Có ≥ 2 folder",
       "1. Chọn folder F2\n2. Reload trang → quan sát folder đang mở\n"
       "3. Mở cùng bot bằng trình duyệt ẩn danh (session khác) → quan sát folder đang mở",
       "—",
       "- Sau reload cùng trình duyệt: vẫn đang mở F2\n"
       "- Trình duyệt ẩn danh: mở folder mặc định (không phải F2)",
       note="Suy luận của AI từ spec §2.1 bước 3 + Field Matrix #45 (cookie folder_sales TTL 14400 phút). "
            "Corpus KHÔNG có TC này — CẦN LEADER XÁC NHẬN trước khi đưa vào bộ chạy."),

    tc("Folder sản phẩm", "FUNC-003", "Abnormal",
       "Folder đã bị xóa ở tab khác → khi mở lại màn hình reset về 未分類 thay vì lỗi",
       ADM1 + "\n- Đang mở folder F2 (cookie folder_sales = id F2)",
       "1. Ở tab trình duyệt thứ 2 (cùng session) xóa folder F2\n"
       "2. Quay lại tab 1, reload /basic/sales/index",
       "—",
       "- Trang load bình thường, KHÔNG lỗi 500\n- Folder đang chọn reset về「未分類」",
       note="Suy luận của AI từ spec §2.1 bước 1「nếu folder đã bị xoá → reset 0」. "
            "Corpus không có TC — CẦN LEADER XÁC NHẬN."),

    tc("Folder sản phẩm", "FUNC-006", "Normal",
       "一括フォルダ変更 nhiều sản phẩm sang folder khác",
       ADM1 + "\n- Folder F1 có 3 sản phẩm, folder F2 rỗng",
       "1. Tick chọn cả 3 sản phẩm ở F1\n2. Click「一括フォルダ変更」→ chọn F2 → xác nhận\n"
       "3. Mở F2 quan sát thứ tự 3 sản phẩm\n4. Reload rồi mở lại F2",
       "3 sản phẩm: SP-A, SP-B, SP-C",
       "- Cả 3 sản phẩm nằm trong F2, F1 còn 0 sản phẩm\n- Số đếm (N) của F1 và F2 cập nhật đúng\n"
       "- ⚠ Ghi lại thứ tự 3 sản phẩm trong F2 ở lần load 1 và lần load 2 — nếu KHÁC nhau thì raise bug",
       note="Nguồn: r23 / r107「Change folder」(TC gốc chỉ có tiêu đề). Spec R33: moveItem đẩy mọi item lên "
            "CÙNG một giá trị position → thứ tự không xác định. Đây là điểm MT-05."),

    # ═════════════════════ 2. Màn list sản phẩm ═════════════════════
    tc("Màn list sản phẩm", "UI-001", "Normal",
       "List 単品 hiển thị đủ 6 cột: ảnh · 管理名 · ngày tạo · 商品ページ · 決済システム · 価格",
       ADM1 + "\n- Có ≥ 1 sản phẩm 単品 đã tạo đủ thông tin, có ảnh",
       "1. Mở tab「商品一覧」→ sub-tab「単品商品」\n2. Đối chiếu từng cột với dữ liệu đã setting của sản phẩm",
       "Sản phẩm: 管理名「テスト単品」· giá 1.000円 · Stripe · có 1 ảnh",
       "- Cột ảnh: hiện đúng ảnh main đã upload; sản phẩm không có ảnh → hiện ảnh default\n"
       "- 管理名 hiện đúng, click mở màn detail sản phẩm 単品\n- ngày tạo = ngày tạo sản phẩm\n"
       "- 決済システム hiện đúng「Stripe」\n- 価格 hiện 1.000円",
       note="Nguồn: r9-r16. r10 ghi note「chưa để chữ béo」và r15「sai text」— 2 lỗi UI đã ghi nhận, cần verify lại."),

    tc("Màn list sản phẩm", "UI-001", "Normal",
       "Cột 販売数/在庫数 khi CÓ set tồn kho → hiện「số đã bán / số stock」",
       ADM1 + "\n- SP-1: flag_use_stock = ON, quantity_stock = 10, đã có 3 đơn 決済成功 mỗi đơn 1 sản phẩm",
       "1. Mở list 単品\n2. Đọc giá trị cột 販売数 và 在庫数 của SP-1",
       "quantity_stock = 10, đã bán 3",
       "- 販売数 = 3\n- 在庫数 còn lại = 7",
       note="Nguồn: r17-r18. Công thức spec BR-04: quantity_stock − SUM(quantity_purchased WHERE status_order=1)."),

    tc("Màn list sản phẩm", "UI-001", "Normal",
       "Cột 在庫数 khi KHÔNG set tồn kho → hiện 無制限 (không hiện số)",
       ADM1 + "\n- SP-2: flag_use_stock = OFF",
       "1. Mở list 単品\n2. Đọc cột 在庫数 của SP-2",
       "flag_use_stock = OFF",
       "- Cột 在庫数 hiện「無制限」/ dấu gạch, KHÔNG hiện con số\n- Cột 販売数 vẫn đếm đúng số đã bán",
       note="Nguồn: r19「số stock case không set stock (không giới hạn)」."),

    tc("Màn list sản phẩm", "DATA-COUNT-001", "Abnormal",
       "販売数 vẫn tính cả đơn ĐÃ HOÀN TIỀN (không lọc status_order)",
       ADM1 + "\n- SP-3 có 3 đơn: 2 đơn 決済成功 (mỗi đơn 1 sp) + 1 đơn đã 返金済み (1 sp)",
       "1. Mở list 単品, đọc cột 販売数 của SP-3\n2. Mở tab 販売履歴 đếm số đơn 決済成功 của SP-3",
       "2 đơn thành công + 1 đơn hoàn tiền",
       "- Ghi lại con số thật của cột 販売数\n"
       "- Theo spec §2.1「販売数 là SUM(quantity_purchased) runtime, KHÔNG lọc status_order」→ dự kiến = 3\n"
       "- Nếu hiển thị 2 thì spec sai; nếu hiển thị 3 thì UI đang gây hiểu nhầm cho admin",
       note="Suy luận của AI từ spec §2.1 + Field Matrix #42. Corpus KHÔNG có TC này. Đây là MT-06 — CẦN LEADER QUYẾT."),

    tc("Màn list sản phẩm", "UI-001", "Normal",
       "List 継続 hiển thị thêm 3 cột riêng: 販売価格 · トライアル中 · 継続中",
       ADM2 + "\n- SP-C là 継続商品 có trial, hiện có 2 hợp đồng đang trial và 3 hợp đồng đang bill",
       "1. Mở sub-tab「継続商品」\n2. Đọc các cột của SP-C",
       "2 hợp đồng status_trial=1 · 3 hợp đồng status_bill=1 đã qua trial",
       "- Cột 「トライアル中」= 2\n- Cột số lượng đang bill = 3\n- Cột 販売価格 hiện đúng giá đang setting",
       note="Nguồn: r95-r103. TC gốc chỉ có tiêu đề — kết quả mong đợi do AI cụ thể hóa; CẦN LEADER XÁC NHẬN con số."),

    tc("Màn list sản phẩm", "UI-002", "Normal",
       "Nút「ページURL」của 継続商品 mở modal chứa ĐÚNG 3 URL + thông tin sản phẩm",
       ADM2 + "\n- SP-C là 継続商品 đã lưu, bot A có liff_id hợp lệ",
       "1. Click cột「商品コード」/ nút「ページURL」của SP-C\n2. Đối chiếu 3 URL trong modal\n"
       "3. Copy từng URL, mở trên LINE app",
       "product_id của SP-C",
       "- Modal hiện 3 URL cùng product_id, khác nhau ở param type:\n"
       "  ① type=product-detail (mua) ② type=product-change (đổi thẻ) ③ type=product-cancel (hủy)\n"
       "- Kèm 7 thuộc tính chỉ đọc: 通常販売価格 / トライアル期間・価格 / 支払いサイクル / 請求終了回数 / "
       "販売上限数 / 1人が購入できる上限数 / 本番・テスト\n- Cả 3 URL mở được đúng trang tương ứng",
       note="Nguồn: r98. Spec SCR-BIL-04."),

    tc("Màn list sản phẩm", "UI-002", "Normal",
       "Sản phẩm 単品 chỉ có 1 URL 商品ページ — copy link và mở preview",
       ADM1 + "\n- SP-1 là 単品商品 đã lưu",
       "1. Click icon copy link ở cột「商品ページ」\n2. Dán vào ô nhập, đối chiếu định dạng\n"
       "3. Quay lại, click icon 👁 preview",
       "product_id của SP-1",
       "- Link copy đúng dạng https://liff.line.me/{liff_id}?product_id={id}&type=product-detail&ts={timestamp}\n"
       "- Copy 2 lần liên tiếp → phần ts KHÁC nhau (cache-buster)\n"
       "- Preview mở tab mới hiển thị trang sản phẩm ở chế độ xem trước",
       note="Nguồn: r12-r13. Spec §2.1 bước 7-8, Field Matrix #44."),

    tc("Màn list sản phẩm", "FUNC-005", "Normal",
       "並べ替え sản phẩm trong 1 folder → thứ tự mới đúng sau reload",
       ADM1 + "\n- Folder F1 có đúng 3 sản phẩm SP-A, SP-B, SP-C",
       "1. Click「並べ替え」\n2. Kéo SP-C lên đầu → lưu\n3. Reload trang, mở lại F1",
       "Thứ tự mong muốn: SP-C → SP-A → SP-B",
       "- Bảng hiển thị đúng thứ tự SP-C → SP-A → SP-B\n- Sau reload giữ nguyên thứ tự",
       note="Nguồn: r22 / r106. Spec §2.1 bước 5: position gán theo mảng ĐẢO NGƯỢC khớp ORDER BY position DESC."),

    tc("Màn list sản phẩm", "LIST-001", "Boundary",
       "Folder rỗng → hiện empty state, không lỗi",
       ADM1 + "\n- Có folder F-empty chưa có sản phẩm nào",
       "1. Chọn folder F-empty ở panel trái\n2. Quan sát vùng bảng bên phải",
       "Folder có 0 sản phẩm",
       "- Bảng hiển thị trạng thái rỗng (không có dòng dữ liệu), KHÔNG lỗi JS\n"
       "- Tên folder ở panel hiện số đếm (0)\n- Nút「新規作成」vẫn dùng được",
       note="Suy luận của AI — corpus không có TC empty state. CẦN LEADER XÁC NHẬN nội dung empty state thật."),

    # ═══════════════ 3. Filter & môi trường list ═══════════════
    tc("Filter & môi trường list", "ENV-001", "Normal",
       "Toggle「本番環境」→ chỉ hiện sản phẩm flag_environment = 1",
       ADM + LINKED + "\n- Bot A có 2 sản phẩm 単品 本番 và 3 sản phẩm 単品 テスト",
       "1. Vào tab 商品一覧 → sub-tab 単品商品\n2. Chọn toggle「本番環境」\n"
       "3. Đếm số dòng trong bảng + số đếm (N) trên tên folder",
       "2 sản phẩm 本番 · 3 sản phẩm テスト",
       "- Bảng hiện đúng 2 sản phẩm 本番\n- Số (N) ở tên folder cũng chỉ đếm sản phẩm 本番\n"
       "- Không lẫn sản phẩm テスト",
       note="Nguồn: r24 (kèm cảnh báo của tester「chỗ này vẫn hiện all sp」— cần verify lại) + r108. Spec BR-10."),

    tc("Filter & môi trường list", "ENV-001", "Normal",
       "Toggle「テスト環境」→ chỉ hiện sản phẩm flag_environment = 0 và hiện được danh sách thẻ test",
       ADM + LINKED + "\n- Bot A có 2 sản phẩm 単品 本番 và 3 sản phẩm 単品 テスト",
       "1. Chọn toggle「テスト環境」\n2. Đếm số dòng trong bảng\n3. Mở màn hiển thị thẻ test (#modalFakeCard)",
       "2 sản phẩm 本番 · 3 sản phẩm テスト",
       "- Bảng hiện đúng 3 sản phẩm テスト\n- Mở được màn/modal danh sách thẻ test",
       note="Nguồn: r25-r26 / r109-r110."),

    tc("Filter & môi trường list", "FUNC-FILTER-001", "Normal",
       "Filter 決済システム =「全て」→ hiện cả sản phẩm Stripe và UnivaPay",
       ADM1 + LINKED + "\n- Folder hiện tại có 2 sản phẩm Stripe + 2 sản phẩm UnivaPay",
       "1. Mở dropdown「表示設定」\n2. Chọn「全て」\n3. Đếm số dòng",
       "2 Stripe + 2 UnivaPay",
       "- Bảng hiện đủ 4 sản phẩm",
       note="Nguồn: r27 / r111."),

    tc("Filter & môi trường list", "FUNC-FILTER-001", "Normal",
       "Filter 決済システム = UnivaPay → chỉ hiện sản phẩm payment_method = univapay",
       ADM1 + LINKED + "\n- Folder hiện tại có 2 sản phẩm Stripe + 2 sản phẩm UnivaPay",
       "1. Mở dropdown「表示設定」→ chọn UnivaPay\n2. Đối chiếu cột 決済システム của từng dòng",
       "2 Stripe + 2 UnivaPay",
       "- Chỉ hiện đúng 2 sản phẩm UnivaPay\n- Cột 決済システム tất cả các dòng đều là UnivaPay",
       note="Nguồn: r28 / r112."),

    tc("Filter & môi trường list", "FUNC-FILTER-001", "Normal",
       "Filter 決済システム = Stripe → chỉ hiện sản phẩm payment_method = stripe",
       ADM1 + LINKED + "\n- Folder hiện tại có 2 sản phẩm Stripe + 2 sản phẩm UnivaPay",
       "1. Mở dropdown「表示設定」→ chọn Stripe\n2. Đối chiếu cột 決済システム của từng dòng",
       "2 Stripe + 2 UnivaPay",
       "- Chỉ hiện đúng 2 sản phẩm Stripe",
       note="Nguồn: r29 / r113."),

    tc("Filter & môi trường list", "FUNC-FILTER-002", "Boundary",
       "Kết hợp filter môi trường + 決済システム + folder → giao của cả 3 điều kiện",
       ADM1 + LINKED + "\n- Folder F1 (テスト) có: 1 SP Stripe, 1 SP UnivaPay; folder F2 (テスト) có 1 SP Stripe",
       "1. Chọn toggle「テスト環境」\n2. Chọn folder F1\n3. Chọn 表示設定 = Stripe\n4. Đếm số dòng",
       "F1: 1 Stripe + 1 UnivaPay · F2: 1 Stripe",
       "- Chỉ hiện đúng 1 sản phẩm (Stripe, thuộc F1, テスト)\n- Không lẫn sản phẩm của F2",
       note="Suy luận của AI — corpus chỉ test từng filter riêng lẻ. CẦN LEADER XÁC NHẬN."),

    # ══════════ 4. Tạo/sửa 単品 — 基本設定 ══════════
    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "Tạo mới 単品商品 đầy đủ trường bắt buộc → lưu thành công, hiện ở list đúng folder",
       ADM1 + LINKED,
       "1. Click「新規作成」ở tab 単品\n2. Nhập 管理名 + chọn folder + 表示商品名 + 説明\n"
       "3. Chọn 決済システム = Stripe, 商品価格 = 1000\n4. Nhập đủ tab「各種ページ」bắt buộc\n"
       "5. Click「保存」\n6. Quay lại list, mở lại sản phẩm vừa tạo",
       "管理名「テスト単品01」· folder F1 · 表示商品名「お試しセット」· 説明「説明テキスト」· 価格 1000円",
       "- Lưu thành công, quay về list, sản phẩm mới nằm trong folder F1\n"
       "- Mở lại màn edit: toàn bộ giá trị vừa nhập hiển thị đúng\n"
       "- Sản phẩm có 商品ページ URL mở được phía LINE",
       note="Nguồn: r31-r37, r74-r75. Spec EP-12 saveItem."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-VALID-001", "Abnormal",
       "Bỏ trống trường bắt buộc → nút 保存 báo lỗi, không lưu",
       ADM1 + LINKED,
       "1. Click「新規作成」\n2. Để trống 管理名 và 商品価格\n3. Click「保存」\n4. Reload list",
       "管理名 = rỗng · 商品価格 = rỗng",
       "- Hiện thông báo lỗi tại đúng ô chưa nhập\n- KHÔNG tạo sản phẩm mới ở list sau reload",
       note="Nguồn: r74「Có check validate, chỗ nào chưa nhập thì báo lỗi」. ⚠ Spec BR-15/R6: saveItem KHÔNG có "
            "validation server, chỉ có JS → xem TC gọi API trực tiếp ở nhóm『Phân quyền & môi trường』."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-BOUND-001", "Boundary",
       "商品価格 = 99 / 100 / 50 → biên giá tối thiểu 100円",
       ADM1 + LINKED,
       "1. Tạo mới 単品, nhập 商品価格 = 99 → 保存\n2. Sửa thành 100 → 保存\n3. Tạo sản phẩm khác giá 50 → 保存",
       "Lần 1: 99 · Lần 2: 100 · Lần 3: 50",
       "- 99 và 50: báo lỗi, không lưu được\n- 100: lưu thành công, s_items.amount = 100",
       note="Nguồn: r37「bắt buộc nhập >= 50 yên」— ⚠ MÂU THUẪN với spec BR-02/BR-05 (V2 min 100円, chỉ V1 min 50). "
            "TC viết theo SPEC (100円). Đây là MT-01 — nếu chạy thực tế ra 50 thì raise bug."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-BOUND-001", "Boundary",
       "管理名 20 / 21 ký tự → giới hạn 20 ký tự",
       ADM1 + LINKED,
       "1. Tạo mới 単品, nhập 管理名 đúng 20 ký tự → 保存\n2. Tạo tiếp sản phẩm khác, nhập 21 ký tự → 保存",
       "20 ký tự「あいうえおかきくけこさしすせそたちつてと」· 21 ký tự (thêm 1 ký tự)",
       "- 20 ký tự: lưu thành công, list hiển thị đủ 20 ký tự\n- 21 ký tự: báo lỗi / bị cắt ở 20, không lưu quá 20",
       note="Nguồn: spec BR-02 (client only). Corpus không có TC biên độ dài → AI bổ sung. CẦN LEADER XÁC NHẬN."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "Chọn 決済システム = Stripe hoặc UnivaPay → lưu đúng payment_method",
       ADM1 + LINKED,
       "1. Tạo SP-S chọn Stripe → lưu → mở lại màn edit\n2. Tạo SP-U chọn UnivaPay → lưu → mở lại màn edit\n"
       "3. Đối chiếu cột 決済システム ở list",
       "SP-S = stripe · SP-U = univapay",
       "- Màn edit của SP-S hiện Stripe, SP-U hiện UnivaPay\n- Cột 決済システム ở list khớp",
       note="Nguồn: r35-r36 / r120."),

    tc("Tạo/sửa 単品 — 基本設定", "STATE-002", "Abnormal",
       "決済システム bị khóa sau lần lưu đầu tiên (chỉ khóa ở client)",
       ADM1 + LINKED + "\n- SP-S đã lưu 1 lần với 決済システム = Stripe",
       "1. Mở màn edit SP-S\n2. Thử mở dropdown「利用する決済システム」\n"
       "3. Dùng DevTools bỏ thuộc tính disabled, đổi sang UnivaPay → 保存\n4. Reload và đọc lại giá trị",
       "SP-S: stripe → thử đổi sang univapay",
       "- Bước 2: dropdown ở trạng thái disabled, không chọn được\n"
       "- Bước 3-4: ghi lại kết quả thật. Theo spec BR-03/R6 server VẪN nhận và ghi payment_method\n"
       "  → nếu đổi được thì đây là lỗ hổng cần raise (sản phẩm đã có đơn sẽ lệch charge_id với cổng mới)",
       note="Suy luận của AI từ spec BR-03 + §5.2. Corpus KHÔNG có TC này. Đây là MT-02 — CẦN LEADER QUYẾT "
            "có đưa TC bypass client vào bộ chạy hay không."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "在庫数: bật ON + nhập số → lưu flag_use_stock=1 và quantity_stock",
       ADM1 + LINKED,
       "1. Tạo mới 単品\n2. Bật toggle「在庫数」\n3. Nhập 在庫数 = 10 → 保存\n4. Mở lại màn edit",
       "quantity_stock = 10",
       "- Toggle ở trạng thái ON, ô số hiện 10\n- Cột 在庫数 ở list hiện 10 (chưa bán)",
       note="Nguồn: r38-r41."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "在庫数: tắt OFF → ẩn ô nhập, sản phẩm bán không giới hạn",
       ADM1 + LINKED,
       "1. Tạo mới 単品\n2. Để toggle「在庫数」ở OFF → 保存\n3. Mở lại màn edit\n4. Mở 商品ページ phía LINE",
       "flag_use_stock = OFF",
       "- Màn edit: toggle OFF, ô nhập số bị ẩn\n- List: cột 在庫数 hiện 無制限\n"
       "- Phía LINE: không hiện ô chọn số lượng, mua mặc định 1 sản phẩm",
       note="Nguồn: r38-r41 + r81/r86 (Bug KH #35992). Kết quả phía LINE lấy từ「Improve bill tiền stripe」r81."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "友だち1人当たりの購入上限: bật ON + nhập số → lưu max_per_person",
       ADM1 + LINKED,
       "1. Tạo mới 単品\n2. Bật toggle「友だち1人当たりの購入上限」\n3. Nhập 5 → 保存\n4. Mở lại màn edit",
       "max_per_person = 5",
       "- Toggle ON, ô số hiện 5\n- Phía LINE: ô nhập số lượng có thuộc tính max = 5",
       note="Nguồn: r42-r45. ⚠ Spec R7: max_per_person KHÔNG enforce ở server — xem TC bypass ở nhóm『Tồn kho & 購入上限』."),

    tc("Tạo/sửa 単品 — 基本設定", "FUNC-001", "Normal",
       "消費税率: chọn 10% / 8% → lưu s_items.tax_item tương ứng",
       ADM1 + LINKED,
       "1. Tạo mới 単品 chọn 決済システム = Stripe → quan sát giá trị mặc định của 消費税率\n"
       "2. Chọn 8% → 保存 → mở lại màn edit\n3. Đổi lại 10% → 保存 → mở lại màn edit\n"
       "4. Lặp lại bước 1-3 với 決済システム = UnivaPay",
       "tax_item: mặc định 10 → 8 → 10",
       "- Mặc định chọn sẵn 10%\n- Chọn 8% → lưu và hiển thị lại đúng 8%\n"
       "- Chọn 10% → lưu và hiển thị lại đúng 10%\n- Cả Stripe và UnivaPay đều hiện khối setting thuế",
       note="Nguồn: Test invoice (stripe) r3-r6. ⚠ Spec R38: UnivaPay KHÔNG xử lý thuế dù vẫn lưu tax_item và "
            "UI vẫn hiện「（税込）」→ MT-08."),

    tc("Tạo/sửa 単品 — 基本設定", "COMPAT-LEGACY-001", "Normal",
       "Item cũ (tạo trước khi có setting thuế) mặc định về 10%",
       ADM1 + LINKED + "\n- Có sản phẩm tạo trước đợt thêm setting thuế (tax_item NULL/0 trong DB)",
       "1. Mở màn edit của sản phẩm cũ\n2. Quan sát khối 消費税率",
       "Sản phẩm cũ chưa từng set thuế",
       "- Khối 消費税率 hiện chọn sẵn 10%\n- Lưu lại không lỗi",
       note="Nguồn: Test invoice (stripe) r7-r10「các item cũ default chọn 10%」."),

    # ══════════ 5. Tạo/sửa 継続 — 基本設定 ══════════
    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "Tạo mới 継続商品 đầy đủ trường → lưu thành công, sinh đủ 3 URL",
       ADM2 + LINKED,
       "1. Click「新規作成」ở tab 継続\n2. Nhập 管理名 / folder / 表示商品名 / 説明\n"
       "3. Chọn 決済システム, ① 請求価格 = 1000, ② 請求回数 = 12, 支払いサイクル = 毎月\n"
       "4. Hoàn tất tab 各種ページ (5 trang) → 保存\n5. Ở list click nút「ページURL」",
       "① 請求価格 1000円 · ② 請求回数 12 · 支払いサイクル 毎月",
       "- Lưu thành công, sản phẩm xuất hiện ở tab 継続\n"
       "- Modal ページURL có đủ 3 link (mua / đổi thẻ / hủy)\n- Mở lại màn edit: các giá trị hiển thị đúng",
       note="Nguồn: r114-r123."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "支払いサイクル — lưu đúng 5 giá trị 毎週/毎月/3ヶ月毎/6ヶ月毎/毎年",
       ADM2 + LINKED,
       "1. Tạo 5 sản phẩm 継続, mỗi sản phẩm chọn 1 giá trị 支払いサイクル\n"
       "2. Lưu từng sản phẩm, mở lại màn edit đối chiếu\n3. Mở 商品ページ phía LINE của từng sản phẩm",
       "毎週 · 毎月 · 3ヶ月毎 · 6ヶ月毎 · 毎年",
       "- Cả 5 sản phẩm lưu và hiển thị lại đúng chu kỳ đã chọn\n"
       "- Phía LINE hiện đúng nhãn chu kỳ tương ứng",
       note="Nguồn: r123 + r314-r318. 5 input cùng 1 loại kết quả (lưu & hiển thị đúng) → giữ chung 1 TC. "
            "Ánh xạ số theo spec: 1=毎週 2=毎月 3=3ヶ月毎 4=6ヶ月毎 5=毎年."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "② 請求回数 = 0 (無制限) → hợp đồng bill vô hạn kỳ",
       ADM2 + LINKED,
       "1. Tạo 継続商品, chọn ② 請求回数 =「無制限」→ 保存\n2. Mở 商品ページ phía LINE\n"
       "3. Cho 1 friend mua, mở màn 注文詳細 của hợp đồng",
       "number_charge = 0",
       "- Phía LINE hiện「無制限」ở mục số lần bill\n"
       "- Hợp đồng sau khi mua: số kỳ còn lại hiển thị dạng vô hạn, không đếm lùi về 0",
       note="Nguồn: r122 + r295「1. không giới hạn 無制限」. Spec BR-06: number_charge=0 → number_continue=-1."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "② 請求回数 có giới hạn (VD 4 lần) → phía LINE hiện đúng số lần",
       ADM2 + LINKED,
       "1. Tạo 継続商品, chọn ② 請求回数 = 4 → 保存\n2. Mở 商品ページ phía LINE\n3. Đọc mục số lần bill",
       "number_charge = 4",
       "- Phía LINE hiện đúng số lần bill = 4",
       note="Nguồn: r295「2. có set: hiện số lần tương ứng」."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "請求エラー: chọn「tự động hủy hợp đồng」→ auto_cancel = 1",
       ADM2 + LINKED,
       "1. Tạo 継続商品, ở mục「請求エラー」chọn tự động hủy → 保存\n2. Mở lại màn edit",
       "auto_cancel = 1",
       "- Radio「自動解約する」đang được chọn sau khi mở lại\n"
       "- (hành vi 3 lần lỗi → hủy: xem nhóm『Job bill định kỳ』)",
       note="Nguồn: r124. Spec BR-07."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "請求エラー: chọn「không tự hủy」→ auto_cancel = 0",
       ADM2 + LINKED,
       "1. Tạo 継続商品, ở mục「請求エラー」chọn không tự hủy → 保存\n2. Mở lại màn edit",
       "auto_cancel = 0",
       "- Radio「自動解約しない」đang được chọn sau khi mở lại",
       note="Nguồn: r125."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "トライアル: OFF → sản phẩm không có kỳ dùng thử",
       ADM2 + LINKED,
       "1. Tạo 継続商品, để toggle トライアル ở OFF → 保存\n2. Mở 商品ページ phía LINE\n"
       "3. Cho 1 friend mua, kiểm tra trạng thái hợp đồng ở 注文詳細",
       "flag_trial = 0",
       "- Phía LINE: KHÔNG hiện thông tin thời gian trial\n"
       "- Sau khi mua: trạng thái hợp đồng =「継続中」(không phải トライアル中)",
       note="Nguồn: r134「sản phẩm không được trial」+ r309-r310."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "トライアル: ON + số ngày trial → hợp đồng vào trạng thái トライアル中",
       ADM2 + LINKED,
       "1. Tạo 継続商品, bật トライアル, nhập số ngày = 7 → 保存\n2. Cho 1 friend mua ở 商品ページ\n"
       "3. Mở 注文詳細 của hợp đồng vừa tạo, đọc trạng thái và 次回決済予定日",
       "time_trial = 7 ngày · ngày mua = D",
       "- Trạng thái hợp đồng =「トライアル中」\n"
       "- Ngày hết trial = D + 7 (giờ 23:59:59)\n- Cột「トライアル中」ở list 継続 tăng thêm 1",
       note="Nguồn: r135 + r307-r308. Spec BR-09: hạn trial = now()->addDay(time_trial) ép giờ 23:59:59."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "トライアル価格 CÓ set → kỳ đầu bill đúng số tiền trial",
       ADM2 + LINKED,
       "1. Tạo 継続商品: 請求価格 3000, トライアル 7 ngày, トライアル価格 = 500 → 保存\n"
       "2. Cho friend mua ở 商品ページ, nhập thẻ hợp lệ\n3. Mở 注文詳細 đọc số tiền kỳ đầu",
       "amount = 3000 · amount_first = 500 · time_trial = 7",
       "- Số tiền đã bill kỳ đầu = 500円 (không phải 3000)\n"
       "- Trạng thái =「トライアル中」, ngày hết trial = ngày mua + 7\n"
       "- Số tiền hiển thị ở 決済履歴 và trên dashboard cổng thanh toán đều = 500円",
       note="Nguồn: r136 (tester ghi「Cần Comfirm」) + r307. Spec BR-05."),

    tc("Tạo/sửa 継続 — 基本設定", "FUNC-001", "Normal",
       "トライアル価格 KHÔNG set → kỳ đầu bill 0円 (chỉ lưu thẻ)",
       ADM2 + LINKED,
       "1. Tạo 継続商品: 請求価格 3000, トライアル 7 ngày, KHÔNG set トライアル価格 → 保存\n"
       "2. Cho friend mua ở 商品ページ, nhập thẻ hợp lệ\n3. Mở 注文詳細 + dashboard cổng thanh toán",
       "amount = 3000 · flag_first = 0 · time_trial = 7",
       "- Số tiền đã bill kỳ đầu = 0円\n- Trạng thái =「トライアル中」\n"
       "- Stripe: tạo SetupIntent (lưu thẻ) chứ không phải PaymentIntent\n"
       "- UnivaPay: tạo giao dịch trạng thái Authorized để xác minh thẻ",
       note="Nguồn: r308 (tester ghi「bill số tiền bt hay bill 0đ」— nghi vấn) + r378 + r390. Spec BR-05 nhánh cuối."),

    tc("Tạo/sửa 継続 — 基本設定", "DATA-001", "Abnormal",
       "Đổi 管理名 sản phẩm đã có đơn → đồng bộ ngược name_item ở 2 bảng lịch sử",
       ADM2 + LINKED + "\n- SP-C đã có ≥ 1 đơn 単品/hợp đồng trong 販売履歴",
       "1. Ghi lại 商品名 đang hiển thị ở 販売履歴 của SP-C\n2. Mở màn edit SP-C, đổi 管理名 → 保存\n"
       "3. Quay lại tab 販売履歴, mở cả list và 注文詳細 của đơn cũ",
       "管理名 cũ「旧商品名」→ mới「新商品名」",
       "- Cột 商品名 của đơn CŨ ở list 販売履歴 đổi thành「新商品名」\n"
       "- Màn 注文詳細 của đơn cũ cũng hiện「新商品名」\n"
       "- File CSV export sau đó cũng dùng tên mới",
       note="Suy luận của AI từ spec §2.1 SCR-BIL-05 + Field Matrix #1/#49 (saveItem đồng bộ ngược name_item). "
            "Corpus KHÔNG có TC này. Đây là MT-07 — hành vi này khiến lịch sử MẤT snapshot tên lúc mua."),

    # ══════════ 6. Wizard 各種ページ ══════════
    tc("Wizard 各種ページ", "UI-001", "Normal",
       "Trang 1 商品ページ: nội dung 商品案内 + nhãn/màu nút hiển thị đúng phía LINE",
       ADM1 + LINKED,
       "1. Ở tab「各種ページ」bước 1, nhập nội dung 商品案内 bằng TinyMCE\n"
       "2. Đổi ボタンテキスト, 背景色, 文字色 của nút\n3. 保存 → mở preview → mở 商品ページ trên LINE app",
       "商品案内「商品の説明テキスト」· nhãn nút「購入手続きへ」· nền #FF0000 · chữ #FFFFFF",
       "- Preview và trang phía LINE đều hiện đúng nội dung 商品案内\n"
       "- Nút hiện đúng chữ「購入手続きへ」, nền đỏ, chữ trắng ở CẢ preview và LINE",
       note="Nguồn: r33-r34 (note「chưa hiện phía line」cần verify lại), r53-r55, test fix bug r30-r35."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "在庫数表示 = ON + CÓ set stock → phía LINE hiện số tồn kho còn lại",
       ADM1 + LINKED + "\n- SP có flag_use_stock = ON, quantity_stock = 10, đã bán 3",
       "1. Ở bước 1 wizard bật「在庫数表示」→ 保存\n2. Mở preview\n3. Mở 商品ページ trên LINE app",
       "quantity_stock = 10, đã bán 3",
       "- Cả preview và trang LINE hiện số tồn kho còn lại = 7",
       note="Nguồn: r48 + r266."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "在庫数表示 = ON nhưng KHÔNG set stock → phía LINE không hiện trường tồn kho",
       ADM1 + LINKED + "\n- SP có flag_use_stock = OFF",
       "1. Ở bước 1 wizard bật「在庫数表示」→ 保存\n2. Mở 商品ページ trên LINE app",
       "flag_use_stock = OFF, flag_show_stock = ON",
       "- Trang LINE KHÔNG hiện trường tồn kho",
       note="Nguồn: r267."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "在庫数表示 = OFF → phía LINE ẩn trường tồn kho dù có set stock",
       ADM1 + LINKED + "\n- SP có flag_use_stock = ON, quantity_stock = 10",
       "1. Ở bước 1 wizard tắt「在庫数表示」→ 保存\n2. Mở preview + 商品ページ trên LINE app",
       "flag_use_stock = ON, flag_show_stock = OFF",
       "- Cả preview và trang LINE đều KHÔNG hiện trường tồn kho\n"
       "- Nhưng khi mua vượt tồn kho vẫn bị chặn (rule tồn kho vẫn áp)",
       note="Nguồn: r49 + r265."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "購入制限表示 = ON + CÓ set 購入上限 → phía LINE hiện số lượng tối đa 1 người mua",
       ADM1 + LINKED + "\n- SP có flag_use_max_per_person = ON, max_per_person = 5",
       "1. Ở bước 1 wizard bật「友だち1人当たりの購入制限表示」→ 保存\n2. Mở preview + 商品ページ trên LINE",
       "max_per_person = 5",
       "- Cả preview và trang LINE hiện số tối đa 1 người được mua = 5",
       note="Nguồn: r50 + r269."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "購入制限表示 = OFF hoặc không set 購入上限 → phía LINE ẩn trường này",
       ADM1 + LINKED,
       "1. SP-A: bật 購入制限表示 nhưng KHÔNG set 購入上限 → 保存 → mở LINE\n"
       "2. SP-B: tắt 購入制限表示 dù có set 購入上限 = 5 → 保存 → mở LINE",
       "SP-A: flag_use_max_per_person=OFF · SP-B: flag_show_max_per_person=OFF",
       "- Cả 2 trường hợp: trang LINE KHÔNG hiện trường số lượng tối đa 1 người mua",
       note="Nguồn: r51 + r268 + r270. 2 input cùng 1 kết quả → giữ chung 1 TC."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "Trang 2 友だち情報入力: 2 mục お名前 / メールアドレス luôn có sẵn, bắt buộc, không xóa được",
       ADM1 + LINKED,
       "1. Tạo mới sản phẩm, mở tab 各種ページ bước 2\n2. Quan sát danh sách mục mặc định\n"
       "3. Thử click nút xóa của「お名前」và「メールアドレス」\n4. Thử đổi 必須/任意 của 2 mục này",
       "Sản phẩm mới, chưa thêm mục nào",
       "- Sẵn có đúng 2 mục:「お名前」liên kết system name,「メールアドレス」liên kết email\n"
       "- Cả 2 đều ở trạng thái「必須」\n- Không xóa được (nút xóa bị ẩn/disable)",
       note="Nguồn: r56-r57, r62「tên và email không cho xóa」. Spec: b_c_info_setting.is_default = 1."),

    tc("Wizard 各種ページ", "INTG-001", "Normal",
       "お名前/メールアドレス setting ON liên kết friend info → giá trị lưu vào friend_information_value",
       ADM1 + LINKED + "\n- Friend F1 chưa có giá trị system name / email",
       "1. Ở bước 2 bật liên kết friend info cho「お名前」và「メールアドレス」→ 保存\n"
       "2. Friend F1 mua sản phẩm, nhập tên「山田太郎」và mail「t@example.com」\n"
       "3. Mở màn 友だち詳細 của F1 xem 2 trường tương ứng\n4. Mở 注文詳細 của đơn",
       "Tên「山田太郎」· mail「t@example.com」",
       "- 友だち詳細 của F1: システム表示名 =「山田太郎」, メールアドレス =「t@example.com」\n"
       "- 注文詳細 khối 友だち情報 cũng hiện đúng 2 giá trị",
       note="Nguồn: r58「có liên kết fr infor tương ứng, khi user mua có nhập thông tin thì sẽ lưu vào friend infor value」."),

    tc("Wizard 各種ページ", "INTG-001", "Normal",
       "お名前/メールアドレス setting OFF liên kết → chỉ lưu ở lịch sử mua, KHÔNG ghi friend info",
       ADM1 + LINKED + "\n- Friend F2 chưa có giá trị system name / email",
       "1. Ở bước 2 TẮT liên kết friend info cho「お名前」và「メールアドレス」→ 保存\n"
       "2. Friend F2 mua sản phẩm, nhập tên「鈴木花子」và mail「s@example.com」\n"
       "3. Mở 友だち詳細 của F2\n4. Mở 注文詳細 của đơn",
       "Tên「鈴木花子」· mail「s@example.com」",
       "- 友だち詳細 của F2: 2 trường vẫn TRỐNG (không bị ghi đè)\n"
       "- 注文詳細 khối 友だち情報 vẫn hiện đủ「鈴木花子」/「s@example.com」",
       note="Nguồn: r59."),

    tc("Wizard 各種ページ", "FUNC-001", "Normal",
       "Thêm / sắp xếp / xóa mục 友だち情報入力 tùy chỉnh",
       ADM1 + LINKED,
       "1. Ở bước 2 thêm 3 mục: 電話番号 (必須), 住所 (任意), 備考 (任意)\n"
       "2. Kéo đổi thứ tự đưa 備考 lên trên 住所 → 保存\n3. Mở lại màn edit đối chiếu thứ tự\n"
       "4. Xóa mục 備考 → 保存 → mở lại\n5. Mở trang 友だち情報 phía LINE",
       "3 mục tùy chỉnh, thứ tự sau khi kéo: 電話番号 → 備考 → 住所",
       "- Sau lưu và mở lại: thứ tự đúng 電話番号 → 備考 → 住所\n"
       "- Sau khi xóa 備考: chỉ còn 電話番号 → 住所\n"
       "- Trang 友だち情報 phía LINE hiện đúng thứ tự và trạng thái 必須/任意 tương ứng",
       note="Nguồn: r60-r62 + r279 mục 1. ⚠ Spec: mục thiếu trong payload saveItem bị XÓA CỨNG khỏi b_c_info_setting."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "Trang 3 最終確認ページ: nút「テンプレートを引用」nạp nội dung từ 各種設定",
       ADM1 + LINKED + "\n- Đã nhập nội dung「ご確認事項」ở tab 各種設定 →「最終確認画面」",
       "1. Ở wizard bước 3, click「テンプレートを引用」\n2. Quan sát editor\n3. Chưa 保存, reload màn hình",
       "Template ご確認事項 đã setting sẵn ở cấp bot",
       "- Editor được nạp đúng nội dung template của 各種設定\n"
       "- Reload khi chưa 保存 → nội dung KHÔNG được lưu (editor trống lại)",
       note="Nguồn: r63「Nhấn thì lấy thông tin ở màn comfirm để paste vào」+ spec Field Matrix #29."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "Trang 3: admin tự nhập nội dung ご確認事項 → hiện ở trang 最終確認 phía LINE",
       ADM1 + LINKED,
       "1. Ở wizard bước 3 nhập text tùy chỉnh vào editor → 保存\n"
       "2. Mua sản phẩm phía LINE tới trang 最終確認",
       "Nội dung「返品・キャンセルについて…」",
       "- Trang 最終確認 phía LINE hiện đúng nội dung admin đã nhập",
       note="Nguồn: r64."),

    tc("Wizard 各種ページ", "UI-002", "Normal",
       "★ Nhãn nút cấu hình ở bước 3 hiển thị trên trang NHẬP THẺ (lệch 1 bước)",
       ADM1 + LINKED,
       "1. Ở wizard bước 3 đổi ボタンテキスト thành「最終確認へ進む」→ 保存\n"
       "2. Mua sản phẩm phía LINE: trang 商品 → 友だち情報 → NHẬP THẺ\n"
       "3. Đọc nhãn nút ở trang nhập thẻ và ở trang 最終確認",
       "Nhãn bước 3 =「最終確認へ進む」",
       "- Nút ở trang NHẬP THẺ (SCR-BIL-24) mang nhãn「最終確認へ進む」\n"
       "- KHÔNG phải nút ở trang 最終確認",
       note="Suy luận của AI từ spec §2.1「Tên cột lệch 2 bước so với nhãn wizard」+ Field Matrix #30 "
            "(text_payment_button). Corpus KHÔNG có TC này — đây là bẫy dễ raise bug nhầm. CẦN LEADER XÁC NHẬN."),

    tc("Wizard 各種ページ", "UI-002", "Normal",
       "★ Nhãn nút cấu hình ở bước 4 hiển thị trên trang 最終確認 (lệch 1 bước)",
       ADM1 + LINKED,
       "1. Ở wizard bước 4 đổi ボタンテキスト thành「購入を確定する」→ 保存\n"
       "2. Mua sản phẩm phía LINE đi tới trang 最終確認\n3. Đọc nhãn nút xác nhận mua",
       "Nhãn bước 4 =「購入を確定する」",
       "- Nút「購入する」ở trang 最終確認 mang nhãn「購入を確定する」",
       note="Suy luận của AI từ spec Field Matrix #31 (text_confirm_button). Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN."),

    tc("Wizard 各種ページ", "FUNC-001", "Normal",
       "Trang 4 — Option「トーク画面に戻る」: mua xong quay về màn chat LINE",
       ADM1 + LINKED,
       "1. Ở wizard bước 4 chọn option「トーク画面に戻る」→ 保存\n"
       "2. Friend mua sản phẩm thành công phía LINE\n3. Quan sát màn hình sau khi bấm 購入する",
       "flag_page_end = 2",
       "- Sau khi thanh toán thành công, LIFF đóng và quay về màn hình chat 1:1 của bot",
       note="Nguồn: r65 + r324「mua xong back về màn hình chat của user」. Spec BR-12 flag_page_end=2."),

    tc("Wizard 各種ページ", "FUNC-001", "Normal",
       "Trang 4 — Option「任意ページURL」: mua xong redirect sang URL đã nhập",
       ADM1 + LINKED,
       "1. Ở wizard bước 4 chọn option URL, nhập https://example.com/thanks → 保存\n"
       "2. Friend mua sản phẩm thành công phía LINE",
       "url_page_outsite_end = https://example.com/thanks",
       "- Sau khi thanh toán thành công, trình duyệt chuyển sang https://example.com/thanks",
       note="Nguồn: r66 + r325. Spec BR-12 flag_page_end=1."),

    tc("Wizard 各種ページ", "FUNC-001", "Normal",
       "Trang 4 — Option「テキスト入力」: mua xong hiện trang nội dung đã nhập",
       ADM1 + LINKED,
       "1. Ở wizard bước 4 chọn option テキスト, nhập nội dung cảm ơn → 保存\n"
       "2. Friend mua sản phẩm thành công phía LINE",
       "page_end_simple =「ご購入ありがとうございました」",
       "- Sau khi thanh toán thành công hiện trang có đúng nội dung đã nhập",
       note="Nguồn: r67 + r326. Spec BR-12 flag_page_end=0."),

    tc("Wizard 各種ページ", "FUNC-VALID-001", "Abnormal",
       "Trang 4 — chọn option URL nhưng nhập chuỗi không phải URL → báo lỗi",
       ADM1 + LINKED,
       "1. Ở wizard bước 4 chọn option URL\n2. Nhập「abcxyz」(không phải URL) → 保存",
       "url_page_outsite_end =「abcxyz」",
       "- Hiện lỗi định dạng URL tại ô nhập, KHÔNG lưu được",
       note="Suy luận của AI từ spec Field Matrix #32-33 (validate URL chỉ ở client). Corpus không có TC."),

    tc("Wizard 各種ページ", "UI-001", "Normal",
       "Trang 5 解約用ページ (chỉ 継続): nội dung + nhãn/màu nút hủy hiển thị đúng",
       ADM2 + LINKED,
       "1. Ở wizard bước 5 nhập 解約案内, đổi ボタンテキスト và màu nút → 保存\n"
       "2. Cho friend mua sản phẩm\n3. Mở link type=product-cancel trên LINE app",
       "解約案内「解約時のご注意…」· nhãn nút「解約する」· màu nút #FF0000",
       "- Trang hủy phía LINE hiện đúng nội dung 解約案内\n- Nút hiện đúng chữ và màu đã setting",
       note="Nguồn: r138-r140."),

    tc("Wizard 各種ページ", "FUNC-BOUND-001", "Boundary",
       "Trang 5 — ボタンテキスト tối đa 10 ký tự (khác các trang khác là 15)",
       ADM2 + LINKED,
       "1. Ở wizard bước 5 nhập nhãn nút đúng 10 ký tự → 保存\n"
       "2. Nhập 11 ký tự → 保存\n3. Đối chiếu với bước 1 (nhập 15 ký tự vẫn được)",
       "Bước 5: 10 ký tự「あいうえおかきくけこ」→ 11 ký tự · Bước 1: 15 ký tự",
       "- Bước 5: 10 ký tự lưu OK, 11 ký tự báo lỗi/bị cắt\n- Bước 1: 15 ký tự lưu OK",
       note="Suy luận của AI từ spec BR-02 + Field Matrix #36. Corpus không có TC biên. CẦN LEADER XÁC NHẬN."),

    tc("Wizard 各種ページ", "COMPAT-001", "Normal",
       "Setting 商品情報 (cỡ chữ, màu, đậm, nghiêng, căn lề, URL, source code) hiển thị đúng ở preview và phía LINE",
       ADM1 + LINKED,
       "1. Ở editor 商品案内 lần lượt áp: cỡ chữ · màu chữ · in đậm · in nghiêng · căn trái/phải/giữa/2 bên · "
       "căn lề · chèn URL · nhập trực tiếp Source code\n2. 保存 → mở preview → mở trang phía LINE",
       "10 kiểu định dạng như mô tả ở bước 1",
       "- Preview và trang phía LINE hiển thị GIỐNG NHAU và đúng định dạng đã áp cho cả 10 kiểu\n"
       "- Link chèn bằng 「gắn url」 bấm mở được đúng địa chỉ",
       note="Nguồn: test fix bug r39-r46 (Bug #26719: thông tin sản phẩm hiển thị khác nhau giữa edit và preview — lỗi css). "
            "10 input cùng 1 kết quả (edit ≡ preview ≡ LINE) → giữ chung 1 TC. regression"),

    tc("Wizard 各種ページ", "REG-001", "Normal",
       "Sửa 表示商品名 / 説明 → cập nhật ngay ở list, detail, preview và cả 3 link phía LINE",
       ADM2 + LINKED + "\n- SP-C là 継続商品 đã lưu, đã có 1 friend mua",
       "1. Mở màn edit SP-C, đổi 表示商品名 → 保存\n"
       "2. Đối chiếu ở: màn List Product · màn Detail · màn Preview\n"
       "3. Mở phía LINE cả 3 link: mua mới · đổi thẻ · hủy\n4. Lặp lại bước 1-3 với trường 説明",
       "表示商品名 cũ → mới · 説明 cũ → mới",
       "- Cả 4 điểm phía admin (List / Detail / Preview) và cả 3 link phía LINE đều hiện giá trị MỚI\n"
       "- Không cần clear cache trình duyệt",
       note="Nguồn: test fix bug r253-r298 (Bug #31871: đã edit setting LINEトーク画面 表示設定 nhưng nội dung "
            "không update). Ma trận gốc 46 dòng cùng 1 kết quả mong đợi → gộp thành 1 TC liệt kê đủ điểm kiểm. regression"),

    # ══════════ 7. Ảnh sản phẩm ══════════
    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Upload 1 ảnh hợp lệ → hiện đúng ở màn edit, preview và phía LINE",
       ADM1 + LINKED,
       "1. Tạo mới item, ở bước 1 wizard upload 1 ảnh JPG hợp lệ → 保存\n"
       "2. Mở lại màn edit · mở preview · mở 商品ページ trên LINE app",
       "1 ảnh JPG ~500KB",
       "- Cả 3 nơi (edit / preview / LINE) đều hiện ĐÚNG ảnh vừa upload\n- Ảnh không bị vỡ, không hiện ảnh default",
       env="PRODUCTION",
       note="Nguồn: Quản lý sản phẩm r418 (Bug KH #33732). RULE-08: media test trên PRODUCTION."),

    tc("Ảnh sản phẩm", "MEDIA-002", "Abnormal",
       "Upload ảnh 0KB → báo lỗi, không upload",
       ADM1 + LINKED,
       "1. Tạo file ảnh rỗng 0 byte\n2. Ở bước 1 wizard upload file này",
       "File ảnh 0KB",
       "- Hiện thông báo lỗi\n- Ảnh KHÔNG được thêm vào danh sách ảnh của sản phẩm",
       env="PRODUCTION",
       note="Nguồn: r419."),

    tc("Ảnh sản phẩm", "MEDIA-002", "Abnormal",
       "Upload ảnh KHÔNG có phần mở rộng → vẫn upload được và hiển thị đúng",
       ADM1 + LINKED,
       "1. Đổi tên 1 file ảnh JPG hợp lệ, bỏ đuôi .jpg\n2. Upload ở bước 1 wizard → 保存\n"
       "3. Mở màn detail sản phẩm + trang phía LINE",
       "File ảnh không có extension",
       "- Upload thành công\n- Ảnh hiển thị được ở màn detail và phía LINE",
       env="PRODUCTION",
       note="Nguồn: r420. ⚠ Spec R34: uploadFile KHÔNG validate MIME/kích thước trước khi move() — "
            "cần bổ sung TC bảo mật upload file không phải ảnh (xem nhóm『Phân quyền & môi trường』)."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Tạo item KHÔNG có ảnh → hiển thị ảnh mặc định ở mọi màn",
       ADM1 + LINKED,
       "1. Tạo mới item, không upload ảnh nào → 保存\n2. Xem list · detail · preview · trang phía LINE",
       "0 ảnh",
       "- Tất cả các màn hiện ảnh mặc định, không bị vỡ ảnh / không lỗi 404",
       env="PRODUCTION",
       note="Nguồn: r417 + r78「Case không có ảnh hiện ảnh default」."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Upload nhiều ảnh → ảnh đầu là ảnh main, hiển thị đủ ở preview và phía LINE",
       ADM1 + LINKED,
       "1. Ở bước 1 wizard upload 3 ảnh → 保存\n2. Mở màn edit · preview · trang phía LINE",
       "3 ảnh JPG/PNG",
       "- Màn edit hiện đủ 3 ảnh theo đúng thứ tự upload\n"
       "- List sản phẩm hiện ảnh đầu tiên (ảnh main)\n- Preview và trang LINE hiện đủ 3 ảnh",
       env="PRODUCTION",
       note="Nguồn: r421 + r438."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Boundary",
       "Upload ảnh thứ 6 → chặn ở giới hạn 5 ảnh",
       ADM1 + LINKED,
       "1. Ở bước 1 wizard upload lần lượt 5 ảnh, quan sát counter\n2. Thử upload ảnh thứ 6",
       "6 ảnh JPG",
       "- Sau 5 ảnh counter hiện 5/5\n- Không thêm được ảnh thứ 6 (nút upload bị chặn / báo lỗi)",
       env="PRODUCTION",
       note="Suy luận của AI từ spec Field Matrix #16 + §5.2 (giới hạn 5 ảnh CHỈ ở client). Corpus không có TC biên. "
            "CẦN LEADER XÁC NHẬN."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Thay ảnh: upload ảnh 1 → upload đè ảnh 2 → 保存 → hiển thị ảnh 2",
       ADM1 + LINKED,
       "1. Upload ảnh A ở bước 1 wizard\n2. Upload lại thành ảnh B (chưa lưu giữa chừng)\n3. 保存\n"
       "4. Mở lại màn edit · preview · trang phía LINE",
       "Ảnh A → ảnh B",
       "- Cả 3 nơi đều hiện ảnh B, không còn ảnh A",
       env="PRODUCTION",
       note="Nguồn: r422 + r439."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Upload ảnh → xóa ảnh → 保存 → sản phẩm về trạng thái không ảnh",
       ADM1 + LINKED,
       "1. Upload ảnh A ở bước 1 wizard\n2. Xóa ảnh A\n3. 保存\n4. Mở lại màn edit · preview · trang LINE",
       "Ảnh A rồi xóa",
       "- Không còn ảnh nào ở màn edit\n- List / preview / trang LINE hiện ảnh mặc định",
       env="PRODUCTION",
       note="Nguồn: r423 + r440."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Upload → xóa → upload ảnh khác → 保存 → hiển thị ảnh cuối cùng",
       ADM1 + LINKED,
       "1. Upload ảnh A\n2. Xóa ảnh A\n3. Upload ảnh B\n4. 保存\n5. Mở màn edit · preview · trang LINE",
       "Ảnh A → xóa → ảnh B",
       "- Cả 3 nơi hiện đúng ảnh B",
       env="PRODUCTION",
       note="Nguồn: r424 + r441. Chuỗi thao tác liên tiếp không tách rời → giữ chung 1 TC."),

    tc("Ảnh sản phẩm", "MEDIA-001", "Normal",
       "Edit item: upload ảnh mới / sửa ảnh / xóa 1 ảnh / xóa toàn bộ ảnh",
       ADM1 + LINKED + "\n- Item đã có sẵn 3 ảnh",
       "1. Mở màn edit, upload thêm 1 ảnh → 保存 → kiểm tra 3 nơi\n"
       "2. Thay 1 ảnh bằng ảnh khác → 保存 → kiểm tra\n3. Xóa 1 ảnh → 保存 → kiểm tra\n"
       "4. Xóa toàn bộ ảnh → 保存 → kiểm tra",
       "3 ảnh ban đầu, thao tác lần lượt như bước 1-4",
       "- Sau MỖI lần 保存, cả màn edit · preview · trang phía LINE đều hiện đúng tập ảnh hiện tại\n"
       "- Xóa toàn bộ ảnh → hiện ảnh mặc định",
       env="PRODUCTION",
       note="Nguồn: r425-r429 + r442-r446."),

    tc("Ảnh sản phẩm", "MEDIA-003", "Normal",
       "Copy item CÓ ảnh → ảnh bản copy hiển thị được VÀ có TÊN FILE KHÁC bản gốc",
       ADM1 + LINKED + "\n- Item gốc có 1 ảnh, ảnh đang nằm trên server hiện tại",
       "1. Ở list click ••• → コピー item gốc\n2. Mở màn edit · preview · trang LINE của bản copy\n"
       "3. So sánh đường dẫn/tên file ảnh của bản gốc và bản copy\n4. Xóa item gốc, mở lại ảnh bản copy",
       "Item có 1 ảnh",
       "- Ảnh bản copy hiển thị được ở cả 3 nơi (KHÔNG bị trắng/vỡ)\n"
       "- Tên file ảnh bản copy KHÁC tên file bản gốc\n- Xóa item gốc: ảnh bản copy vẫn hiển thị bình thường",
       env="PRODUCTION",
       note="Nguồn: r430-r431 (Bug KH #33732 — nguyên nhân: copy ảnh không đổi tên file nên CDN ưu tiên "
            "file cũ trên server, tải về file rỗng). Bước 4 là suy luận của AI từ spec §2.1 (xóa item xóa file ảnh vật lý)."),

    tc("Ảnh sản phẩm", "MEDIA-003", "Normal",
       "Copy item CÓ NHIỀU ảnh, ảnh nằm ở SERVER KHÁC → vẫn hiển thị đủ và đổi tên file",
       ADM1 + LINKED + "\n- Item gốc có 3 ảnh, ảnh đang nằm trên server khác (không phải server đang test)",
       "1. Copy item gốc\n2. Mở màn edit · preview · trang LINE của bản copy, đếm số ảnh\n"
       "3. So sánh tên file ảnh gốc và ảnh copy",
       "3 ảnh trên server khác",
       "- Bản copy hiện đủ 3 ảnh ở cả 3 nơi\n- Tên file của 3 ảnh copy đều KHÁC tên file gốc",
       env="PRODUCTION",
       note="Nguồn: r433-r435 + r450-r452."),

    tc("Ảnh sản phẩm", "MEDIA-003", "Normal",
       "Copy item KHÔNG có ảnh → bản copy cũng không ảnh, không lỗi",
       ADM1 + LINKED + "\n- Item gốc không có ảnh nào",
       "1. Copy item gốc\n2. Mở màn edit · preview · trang LINE của bản copy",
       "0 ảnh",
       "- Bản copy hiện ảnh mặc định ở cả 3 nơi, không lỗi 404/500",
       env="PRODUCTION",
       note="Nguồn: r430 + r447."),

    tc("Ảnh sản phẩm", "MEDIA-003", "Normal",
       "Copy item 継続 có ảnh → giống 単品 (đổi tên file, hiển thị đủ)",
       ADM2 + LINKED + "\n- Item 継続 gốc có 3 ảnh",
       "1. Copy item 継続\n2. Mở màn edit · preview · cả 3 link phía LINE của bản copy\n"
       "3. So sánh tên file ảnh",
       "3 ảnh",
       "- Bản copy hiện đủ 3 ảnh ở mọi màn\n- Tên file khác bản gốc",
       env="PRODUCTION",
       note="Nguồn: r447-r452."),

    # ══════════ 8. アクション設定 ══════════
    tc("アクション設定", "FUNC-001", "Normal",
       "単品商品 có ĐÚNG 2 slot action: 商品ページ表示時 và 申込完了時",
       ADM1 + LINKED,
       "1. Mở màn edit 1 単品商品 → tab「アクション設定」\n2. Đếm và đọc tên các slot action",
       "単品商品",
       "- Chỉ có đúng 2 slot:「商品ページ表示時」và「申込完了時」\n"
       "- KHÔNG có các slot トライアル / 初回決済 / 2回目以降 / 決済エラー / 解約",
       note="Nguồn: r68-r73 (単品 chỉ có 2 mục action). Spec SCR-BIL-12."),

    tc("アクション設定", "FUNC-001", "Normal",
       "継続商品 có ĐÚNG 7 slot action theo 3 nhóm 通常時 / 決済時 / エラー・解約時",
       ADM2 + LINKED,
       "1. Mở màn edit 1 継続商品 → tab「アクション設定」\n2. Đếm và đọc tên các slot action",
       "継続商品",
       "- Có đúng 7 slot: ① 商品ページ表示時 ② 申込完了時 ③ トライアル ④ 初回決済時 "
       "⑤ 2回目以降決済時 ⑥ 決済エラー発生時 ⑦ 解約時\n- Slot ③ có thêm ô「終了の N 日前」",
       note="Nguồn: r141-r153. Spec SCR-BIL-13."),

    tc("アクション設定", "FUNC-001", "Normal",
       "稼働回数 =「1度のみ」→ chỉ bắn action ở LẦN ĐẦU, các lần sau không bắn",
       ADM1 + LINKED + "\n- Friend F1 CHƯA từng mở 商品ページ của SP-1",
       "1. Ở slot「商品ページ表示時」gắn action gửi tin nhắn, chọn 稼働回数 =「1度のみ」→ 保存\n"
       "2. F1 mở 商品ページ lần 1 → quan sát chat 1:1\n3. F1 mở lại 商品ページ lần 2 và lần 3",
       "Action = gửi text「ページを開きました」",
       "- Lần 1: F1 nhận tin nhắn\n- Lần 2 và 3: F1 KHÔNG nhận thêm tin nhắn nào",
       note="Nguồn: r69「lần đầu mở -> có action; các lần mở tiếp theo -> không action」."),

    tc("アクション設定", "FUNC-001", "Normal",
       "稼働回数 =「何度でも」→ bắn action mỗi lần mở trang",
       ADM1 + LINKED + "\n- Friend F2 CHƯA từng mở 商品ページ của SP-2",
       "1. Ở slot「商品ページ表示時」gắn action gửi tin, chọn 稼働回数 =「何度でも」→ 保存\n"
       "2. F2 mở 商品ページ 3 lần liên tiếp",
       "Action = gửi text「ページを開きました」",
       "- F2 nhận đúng 3 tin nhắn (mỗi lần mở 1 tin)",
       note="Nguồn: r70「mỗi lần user click mở link sẽ action」."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Action「申込完了時」bắn khi mua thành công — 1度のみ vs 何度でも",
       ADM1 + LINKED + "\n- SP cho phép mua nhiều lần (không set 購入上限)",
       "1. Slot「申込完了時」gắn action, chọn 1度のみ → F1 mua 2 lần → quan sát chat\n"
       "2. Đổi sang 何度でも → F2 mua 2 lần → quan sát chat",
       "F1 mua 2 lần · F2 mua 2 lần",
       "- F1 (1度のみ): nhận 1 tin sau lần mua đầu, lần mua 2 không nhận\n"
       "- F2 (何度でも): nhận 2 tin, mỗi lần mua 1 tin",
       note="Nguồn: r71-r73 + r327-r329."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Action text có chèn thông tin đơn hàng (NAME / AMOUNT_ORDER / ORDER_ID / ORDER_DATE / QUANTITY / CYCLE)",
       ADM1 + LINKED,
       "1. Ở slot「申込完了時」gắn action gửi text chứa đủ 6 mã chèn thông tin đơn\n"
       "2. Friend mua sản phẩm với số lượng 2, giá 1.000円\n3. Đọc tin nhắn nhận được ở chat 1:1\n"
       "4. Đối chiếu với 注文詳細 tương ứng",
       "Giá 1.000円 × 2 sản phẩm = 2.000円",
       "- Tin nhắn hiển thị: tên sản phẩm đúng · số tiền = 2.000円 · 注文番号 khớp với 注文詳細 · "
       "ngày mua đúng · số lượng = 2 · nhãn chu kỳ đúng\n- KHÔNG còn mã chèn thô trong tin nhắn",
       note="Nguồn: r331 (note「comfirm design」) + test fix bug r3-r28 (Bug #26568). Spec §7.7. "
            "⚠ Spec R1: AMOUNT_ORDER tính theo GIÁ HIỆN TẠI của sản phẩm → xem MT-03."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Action「商品ページ表示時」KHÔNG có giá trị mã chèn thông tin đơn (chưa có đơn)",
       ADM2 + LINKED,
       "1. Ở slot「商品ページ表示時」gắn action gửi text chứa mã 金額 và 注文番号\n"
       "2. Friend mở 商品ページ (chưa mua)\n3. Đọc tin nhắn nhận được",
       "Text chứa mã 金額 / 注文番号",
       "- Tin nhắn gửi được nhưng phần giá trị của mã đơn hàng để TRỐNG (không hiện 0円 sai lệch)",
       note="Nguồn: test fix bug r3「send action khi mở page, ko có các value của code order」+ r25."),

    tc("アクション設定", "FUNC-001", "Normal",
       "Slot「トライアル」+ 終了の N 日前 → lưu number_day_action_contract_trial",
       ADM2 + LINKED + "\n- 継続商品 có bật トライアル",
       "1. Ở slot「トライアル」gắn action, nhập「終了の 1 日前」→ 保存\n2. Mở lại tab アクション設定",
       "number_day_action_contract_trial = 1",
       "- Giá trị 1 hiển thị lại đúng sau khi mở lại\n"
       "- (hành vi gửi thật: xem nhóm『Action & notify theo sự kiện』)",
       note="Nguồn: r145 + r364. Spec Field Matrix #39."),

    tc("アクション設定", "STATE-001", "Abnormal",
       "Tắt トライアル của sản phẩm đã gắn action トライアル → action_contract_trial_id bị ép NULL",
       ADM2 + LINKED + "\n- 継続商品 SP-T đang bật トライアル và đã gắn action ở slot「トライアル」",
       "1. Mở màn edit SP-T, tắt toggle トライアル → 保存\n2. Mở lại tab アクション設定\n"
       "3. Bật lại トライアル → 保存 → mở lại tab アクション設定",
       "flag_trial: 1 → 0 → 1",
       "- Sau khi tắt トライアル: slot「トライアル」về trạng thái chưa gắn action\n"
       "- Bật lại: slot vẫn TRỐNG (action cũ không tự khôi phục) → admin phải gắn lại",
       note="Suy luận của AI từ spec Field Matrix #37「action_contract_trial_id ép NULL khi flag_trial != 1」. "
            "Corpus KHÔNG có TC này — đây là điểm dễ mất cấu hình. CẦN LEADER XÁC NHẬN."),

    # ══════════ 9. Copy & xóa sản phẩm ══════════
    tc("Copy & xóa sản phẩm", "FUNC-001", "Normal",
       "Copy sản phẩm → clone đủ setting + 7 action, reset counter về 0, sinh item_code mới",
       ADM2 + LINKED + "\n- SP-C là 継続商品 đã setting đủ 7 action, đã có 3 hợp đồng và số 販売数 > 0",
       "1. Ở list click ••• →「コピー」SP-C\n2. Mở màn edit bản copy: đối chiếu từng tab với bản gốc\n"
       "3. Mở tab アクション設定 bản copy\n4. Xem cột 販売数 / トライアル中 / 継続中 của bản copy ở list\n"
       "5. Mở modal ページURL của bản copy, so sánh URL với bản gốc",
       "SP-C có 7 action + 3 hợp đồng",
       "- Bản copy có đủ setting 基本設定 và 各種ページ giống bản gốc\n"
       "- Đủ 7 slot action được clone (mở ra thấy cấu hình giống bản gốc)\n"
       "- Các cột đếm của bản copy đều = 0\n"
       "- URL của bản copy có product_id KHÁC bản gốc",
       note="Nguồn: r20 / r104. Spec §2.1 SCR-BIL-03 EP-19 (replicate + clone t_actions/t_actions_detail + "
            "reset counter + clone b_c_info_setting + copy file ảnh)."),

    tc("Copy & xóa sản phẩm", "FUNC-001", "Normal",
       "Copy sản phẩm → clone luôn các mục 友だち情報入力 (b_c_info_setting)",
       ADM1 + LINKED + "\n- SP-1 có 5 mục 友だち情報入力 (2 mặc định + 3 tùy chỉnh) theo thứ tự cố định",
       "1. Copy SP-1\n2. Mở màn edit bản copy → wizard bước 2\n3. Đối chiếu số mục, tên, 必須/任意, thứ tự",
       "5 mục 友だち情報入力",
       "- Bản copy có đủ 5 mục, tên/必須/thứ tự giống hệt bản gốc",
       note="Suy luận của AI từ spec EP-19 (clone b_c_info_setting). Corpus không nêu rõ. CẦN LEADER XÁC NHẬN."),

    tc("Copy & xóa sản phẩm", "PERM-001", "Abnormal",
       "Copy khi đã đạt giới hạn số sản phẩm theo gói → báo lỗi, không tạo bản copy",
       ADM1 + "\n- Bot A dùng gói free (contract_type = free) → giới hạn 1 sản phẩm mỗi loại\n"
       "- Đã có đúng 1 sản phẩm 単品",
       "1. Ở list click ••• →「コピー」sản phẩm 単品 hiện có\n2. Đếm số sản phẩm 単品 sau thao tác",
       "Gói free, đã có 1 単品",
       "- Hiện lỗi「現在のプランは利用できない機能です。アップグレードが必要になります。」\n"
       "- Vẫn chỉ có 1 sản phẩm 単品",
       note="Suy luận của AI từ spec BR-01 + §6「Quy ước mã lỗi」. Corpus KHÔNG có TC giới hạn gói cho item. "
            "CẦN LEADER XÁC NHẬN thông điệp lỗi thật."),

    tc("Copy & xóa sản phẩm", "PERM-001", "Boundary",
       "Tạo mới sản phẩm khi đạt/chưa đạt giới hạn gói standard (10 sản phẩm mỗi loại)",
       ADM1 + "\n- Bot A gói standard + flag_contract_new = 1 → giới hạn 10 sản phẩm mỗi loại\n"
       "- Đang có 9 sản phẩm 単品",
       "1. Tạo sản phẩm 単品 thứ 10 → 保存\n2. Tạo tiếp sản phẩm 単品 thứ 11 → 保存\n"
       "3. Tạo 1 sản phẩm 継続 (đang có 0) → 保存",
       "9 → 10 → 11 sản phẩm 単品; 0 → 1 sản phẩm 継続",
       "- Sản phẩm thứ 10: tạo thành công\n- Sản phẩm thứ 11: báo lỗi vượt gói, không tạo được\n"
       "- Sản phẩm 継続 vẫn tạo được (2 loại đếm TÁCH RIÊNG)",
       note="Suy luận của AI từ spec BR-01. Corpus KHÔNG có TC. CẦN LEADER XÁC NHẬN con số giới hạn theo gói hiện hành."),

    tc("Copy & xóa sản phẩm", "FUNC-004", "Abnormal",
       "Xóa sản phẩm → hiện màn confirm; xác nhận thì xóa toàn bộ data của sản phẩm",
       ADM1 + LINKED + "\n- SP-DEL là 単品商品 có 1 ảnh, 3 mục 友だち情報入力, chưa có đơn",
       "1. Ở list click ••• →「削除」SP-DEL\n2. Quan sát màn xác nhận → bấm hủy → kiểm tra SP-DEL còn không\n"
       "3. Lặp lại và bấm xác nhận xóa\n4. Mở link 商品ページ của SP-DEL trên LINE",
       "SP-DEL",
       "- Bước 2: hiện màn confirm; bấm hủy → SP-DEL VẪN còn ở list\n"
       "- Bước 3: SP-DEL biến mất khỏi list, số (N) của folder giảm 1\n"
       "- Bước 4: trang LINE hiện「商品が非公開か、存在していません」",
       note="Nguồn: r21 / r105. Spec §2.1: HARD DELETE, xóa cứng b_c_info_setting + xóa file ảnh vật lý."),

    tc("Copy & xóa sản phẩm", "DATA-001", "Abnormal",
       "Xóa sản phẩm ĐÃ CÓ ĐƠN → lịch sử bán hàng giữ lại, không mất/không lỗi",
       ADM1 + LINKED + "\n- SP-X là 単品商品 đã có ≥ 2 đơn 決済成功 trong 販売履歴",
       "1. Ghi lại 注文番号 của 2 đơn\n2. Xóa SP-X, xác nhận\n3. Mở tab 販売履歴 sub-tab 単品, tìm 2 đơn đó\n"
       "4. Mở 注文詳細 của từng đơn\n5. Export CSV lịch sử của khoảng ngày chứa 2 đơn",
       "2 đơn của SP-X",
       "- Ghi lại kết quả THẬT: 2 đơn còn hiển thị ở 販売履歴 hay biến mất\n"
       "- Mở 注文詳細 không lỗi 500\n- Export CSV không lỗi\n"
       "- Theo spec §2.1: bản ghi lịch sử KHÔNG bị xóa, trở thành bản ghi mồ côi (item_id trỏ vào sản phẩm không còn)",
       note="Suy luận của AI từ spec §2.1 SCR-BIL-03「Hệ quả xoá」+ R15 (không có FK constraint). "
            "Corpus KHÔNG có TC này. Đây là MT-04 — rủi ro mất truy vết doanh thu, CẦN LEADER QUYẾT."),

    tc("Copy & xóa sản phẩm", "DATA-001", "Abnormal",
       "Xóa sản phẩm 継続 đang CÓ hợp đồng chạy → hợp đồng và job bill sau đó xử lý thế nào",
       ADM2 + LINKED + "\n- SP-CY là 継続商品 đang có 1 hợp đồng status「継続中」sắp tới kỳ bill",
       "1. Xóa SP-CY\n2. Mở tab 販売履歴 sub-tab 継続, tìm hợp đồng\n"
       "3. Chờ/chạy job bill định kỳ của kỳ tới\n4. Kiểm tra thẻ khách có bị trừ tiền không + dashboard cổng thanh toán",
       "1 hợp đồng đang chạy của SP-CY",
       "- Ghi lại kết quả THẬT ở cả 3 điểm: màn 販売履歴 · kết quả job · dashboard cổng thanh toán\n"
       "- Nếu job vẫn trừ tiền khách của sản phẩm đã bị xóa → BLOCKER, raise ngay",
       env="PRODUCTION",
       note="Suy luận của AI từ spec §2.1 + §7.2 (J1/J2 quét s_cycle_order_history JOIN s_items). Corpus KHÔNG có TC. "
            "Đây là MT-04 (cùng gốc) — CẦN LEADER QUYẾT trước khi chạy."),

    # ══════════ 10. Màn 商品詳細 & Preview ══════════
    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 単品 hiển thị đủ 8 thông tin sản phẩm",
       ADM1 + LINKED + "\n- SP-1 đã setting đủ: tên, ảnh, giá, stock, môi trường",
       "1. Ở list click 管理名 của SP-1\n2. Đối chiếu từng mục với setting ở màn edit",
       "SP-1: tên「テスト単品」· 1.000円 · stock 10 · Stripe · テスト環境",
       "- Hiện đủ: 商品名 · ảnh (không có ảnh → ảnh default) · ngày tạo · 決済方法 · 金額 · 在庫数 · "
       "link 商品ページ · mode (本番/テスト) — tất cả khớp với setting",
       note="Nguồn: r77-r84."),

    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 継続 hiển thị thêm số ngày trial, giá kỳ đầu và 3 link",
       ADM2 + LINKED + "\n- SP-C: 継続商品 có trial 7 ngày, トライアル価格 500円, giá thường 3.000円",
       "1. Ở list click 管理名 của SP-C\n2. Đối chiếu từng mục",
       "trial 7 ngày · giá kỳ đầu 500円 · giá thường 3.000円",
       "- Hiện đủ: 商品名 · ảnh · ngày tạo · 決済方法 · 金額 3.000円 · số ngày trial 7 · giá kỳ đầu 500円 · "
       "在庫数 · link mua · link đổi thẻ · link hủy · mode",
       note="Nguồn: r154-r165."),

    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 — bảng 販売履歴 lọc theo THÁNG (khác tab 販売履歴 chính lọc theo khoảng ngày)",
       ADM1 + LINKED + "\n- SP-1 có đơn ở 2 tháng khác nhau: tháng này 2 đơn, tháng trước 3 đơn",
       "1. Mở 商品詳細 SP-1\n2. Ở bảng lịch sử chọn tháng hiện tại → đếm số dòng\n"
       "3. Chọn tháng trước → đếm số dòng\n4. Mở tab 販売履歴 chính, quan sát bộ lọc thời gian",
       "Tháng này 2 đơn · tháng trước 3 đơn",
       "- Chọn tháng hiện tại: 2 dòng\n- Chọn tháng trước: 3 dòng\n"
       "- Tab 販売履歴 chính dùng bộ lọc KHOẢNG NGÀY (mặc định 30 ngày gần nhất), không phải tháng",
       note="Nguồn: r93 + r177「filter theo tháng」. Spec §2.1 SCR-BIL-14 nêu rõ khác biệt này."),

    tc("Màn 商品詳細 & Preview", "LIST-002", "Normal",
       "商品詳細 — phân trang bảng 販売履歴 (20 dòng/trang)",
       ADM1 + LINKED + "\n- SP-1 có ≥ 25 đơn trong cùng 1 tháng",
       "1. Mở 商品詳細 SP-1, chọn tháng có ≥ 25 đơn\n2. Đếm số dòng trang 1\n"
       "3. Sang trang 2, đếm số dòng và kiểm tra không trùng đơn với trang 1",
       "25 đơn trong 1 tháng",
       "- Trang 1: đúng 20 dòng\n- Trang 2: 5 dòng còn lại, không trùng 注文番号 với trang 1",
       note="Nguồn: r94 + r178「Check phân trang」. Con số 20/trang lấy từ spec §2.1 EP-22."),

    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 — status của đơn 単品: 決済成功 / 返金済み hiển thị đúng",
       ADM1 + LINKED + "\n- SP-1 có 1 đơn 決済成功 và 1 đơn đã hoàn tiền",
       "1. Mở 商品詳細 SP-1 → bảng lịch sử\n2. Đọc cột status của 2 đơn",
       "1 đơn status_order=1 · 1 đơn status_order=2",
       "- Đơn 1 hiện「決済成功」\n- Đơn 2 hiện「返金済み」với màu nền phân biệt",
       note="Nguồn: r90-r91 (note của tester「sai màu nền」— cần verify lại)."),

    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 継続 — status hợp đồng đủ 5 trạng thái",
       ADM2 + LINKED + "\n- SP-C có 5 hợp đồng ở 5 trạng thái khác nhau",
       "1. Mở 商品詳細 SP-C → bảng lịch sử\n2. Đọc cột status của từng hợp đồng",
       "5 hợp đồng: đang trial · đang hợp đồng · bill lỗi · đã hủy · đã hoàn thành",
       "- Hiện đủ và đúng 5 nhãn trạng thái tương ứng cho 5 hợp đồng",
       note="Nguồn: r171-r175. ⚠ Spec §9.1 mục 8:「KHÔNG có badge 決済エラー」— nhãn cho hợp đồng bill lỗi "
            "cần đối chiếu lại thực tế. Xem MT-09."),

    tc("Màn 商品詳細 & Preview", "UI-001", "Normal",
       "商品詳細 — thông tin friend mua: ảnh + LINE name/system name, click mở màn friend",
       ADM1 + LINKED + "\n- SP-1 có ≥ 1 đơn của friend F1 (F1 có ảnh đại diện và system name)",
       "1. Mở 商品詳細 SP-1 → bảng lịch sử\n2. Đọc cột thông tin friend\n3. Click vào tên friend",
       "F1 có LINE name và system name khác nhau",
       "- Hiện ảnh đại diện + tên friend đúng\n- Click mở được màn 友だち詳細 / mypage của F1",
       note="Nguồn: r86-r87 (note của tester「nhấn chưa mở mypage」— lỗi đã ghi nhận, cần verify lại)."),

    tc("Màn 商品詳細 & Preview", "UI-002", "Normal",
       "Preview từ nút 保存・プレビュー ở màn edit và từ nút 👁 ở màn list cho kết quả GIỐNG NHAU",
       ADM1 + LINKED,
       "1. Mở màn edit SP-1, click「保存・プレビュー」→ chụp màn hình preview\n"
       "2. Quay lại list, click icon 👁 của SP-1 → chụp màn hình preview\n"
       "3. Mở 商品ページ thật trên LINE app → chụp màn hình\n4. So sánh 3 ảnh",
       "SP-1 đã setting đầy đủ nội dung, ảnh, màu nút",
       "- Cả 3 màn hiển thị GIỐNG NHAU về: nội dung 商品案内 · ảnh · giá · nhãn và màu nút · "
       "thông tin tồn kho/購入上限 theo setting",
       note="Nguồn: test fix bug r30-r35 (Bug #26719 — lỗi css khiến edit và preview khác nhau). regression"),

    tc("Màn 商品詳細 & Preview", "UI-002", "Normal",
       "Preview 継続商品 giống trang mua thật phía LINE",
       ADM2 + LINKED,
       "1. Mở màn edit SP-C, click「保存・プレビュー」\n2. Click 👁 ở màn list\n"
       "3. Mở link mua thật trên LINE app\n4. So sánh 3 màn",
       "SP-C có trial + giá kỳ đầu + giới hạn số lần bill",
       "- Cả 3 màn hiển thị giống nhau, gồm cả nhãn giá theo pattern (お支払い価格（初回）/（2~4回目）...)",
       note="Nguồn: test fix bug r33-r35 + r76「Preview sản phẩm đơn」. regression"),
]
