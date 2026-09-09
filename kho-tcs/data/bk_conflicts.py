# -*- coding: utf-8 -*-
"""FA-033 データコピー — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: TOÀN BỘ ĐANG CHỜ QUYẾT ĐỊNH của Leader (2026-08-25).
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-00", "CAO", W,
     "PHẠM VI — spec đang tả GIAO DIỆN CŨ (1 màn / 3 endpoint), corpus tả GIAO DIỆN MỚI (7 màn / 5 endpoint). "
     "Phải chốt TRƯỚC vì ảnh hưởng ~100 TC",
     "3 tab [AI]UI TCs / [AI]API TCs / [MN]Job TCs (2026) tả bộ màn MỚI:\n"
     "• SCR-01 tab「コピー登録」· SCR-02 card LOA · SCR-03 modal「コピー開始」· SCR-04 màn blocking + progress bar · "
     "SCR-05 tab「コピー履歴」· SCR-06 modal「コピーコードの再発行」· SCR-07 modal「データコピー完了」\n"
     "• Nút:「コードを確認」→「コピー内容の確認に進む」→「データコピーを開始」+ nút「リセット」+ nút「コピーコードの再発行」\n"
     "• 2 endpoint MỚI: EP-04 GET /ajax/backup-status/{id} (polling 5s), EP-05 POST /ajax/reissue-transfer-code\n"
     "• Trường `currentTransferCode` mới trong response EP-01 + pagination\n"
     "Các TC này tự ghi ở cột Notes: 「THAY ĐỔI so với FA-033」/「ENDPOINT MỚI」/「UPDATE EP-01」",
     "feature-spec.md:74-110 §2.1 — CHỈ 1 màn SCR-BK-01, không tab, không modal.\n"
     "ui-spec.md:60-80 Block 3 — chỉ 1 textbox「データ受信コード」+ 1 nút「登録」.\n"
     "feature-spec.md:355-360 §6 — đúng 3 endpoint EP-01/EP-02/EP-03.\n"
     "feature-spec.md §2.2 flow — nhập mã →「登録」(AJAX) →「コピー実行」(submit) → redirect back; "
     "KHÔNG có màn processing, không polling, không modal hoàn tất.",
     "Spec được reverse-engineer ngày 2026-03-30 từ production; bộ TC [AI] viết sau đó cho đợt improve. "
     "Nếu improve ĐÃ release thì spec sai hoàn toàn ở §2.1/§2.2/§6 và ~100 TC nhóm màn hình phải chạy theo bản mới; "
     "nếu CHƯA release thì ~100 TC đó chưa được giao cho member.",
     "TC-BK-05 → TC-BK-06 · TC-BK-08 · TC-BK-10 → TC-BK-12 · TC-BK-14 → TC-BK-21 · TC-BK-25 → TC-BK-27 · TC-BK-30 → TC-BK-32 · TC-BK-34 → TC-BK-35 · TC-BK-37 → TC-BK-39 · TC-BK-50 → TC-BK-51 · TC-BK-57 · TC-BK-63 → TC-BK-64 · TC-BK-86",
     "",
     "Chốt xong phải: ① ghi rõ bản UI nào đang chạy trên PRODUCTION; ② viết lại feature-spec.md §2.1/§2.2/§6 "
     "+ ui-spec.md Block 3-4 theo bản mới; ③ bổ sung EP-04, EP-05 vào api-spec.md."],

    ["MT-01", "CAO", W,
     "CHIỀU COPY BỊ ĐẢO — người thao tác là LOA NGUỒN (spec) hay LOA ĐÍCH (corpus mới)?",
     "Corpus mới gọi ô nhập là「コピー元アカウントのコピーコード」(mã copy của tài khoản NGUỒN) — tức người đang thao tác "
     "nhập mã của bên GỬI dữ liệu ⇒ bot đang đăng nhập là bên NHẬN.\n"
     "Khớp với: [AI]UI r43 (Comment 6) — bot free「コピーコードの取得のみ可能」(chỉ lấy được mã) nhưng vẫn không copy được; "
     "[AI]UI r47 —「backup data từ bot free sang bot có phí ⇒ hiển thị đầy đủ data của bot free tại bot có phí đó」.\n"
     "NHƯNG TC-BK-059 ([AI]API r27) lại ghi「backup_history.bot_id = current_bot_id (đúng session, KHÔNG phải bot đích)」 "
     "— tức current session = nguồn. Tự mâu thuẫn ngay trong cùng bộ TC.",
     "feature-spec.md §2.2 + §3.1 — ô nhập là「データ受信コード」(mã NHẬN dữ liệu) của LOA ĐÍCH; "
     "`backup_history.bot_id` = LOA nguồn = bot đang đăng nhập; `code` = transfer_code của LOA đích; "
     "`line_account` = tên LOA đích (BR-14).\n"
     "feature-spec.md §1.1 —「sao chép dữ liệu ... sang một LOA エルメ khác」.",
     "Đảo chiều làm đổi ý nghĩa của CẢ 3 cột `backup_history` (bot_id / code / line_account), đổi phía bị khoá thao tác "
     "(BR-04), đổi phía được phép dùng plan free, và đổi hoàn toàn cách dựng dữ liệu test. "
     "Không viết được điều kiện tiền đề đúng nếu chưa chốt.",
     "TC-BK-18 · TC-BK-32 · TC-BK-75 · TC-BK-92",
     "",
     "Chốt xong phải: ① thống nhất nhãn ô nhập (データ受信コード hay コピー元アカウントのコピーコード); "
     "② viết lại §3.1 định nghĩa 3 cột backup_history; ③ sửa BR-14; ④ sửa phạm vi BR-04 (xem MT-08)."],

    ["MT-02", "CAO", W,
     "Bot free plan: alert rồi ĐÁ VỀ /admin/home, hay chỉ hiện modal rồi Ở LẠI màn データコピー?",
     "Cùng 1 tab [AI]UI TCs, 2 khối khác nhau:\n"
     "• r26 (TC-BK-025, khối cũ): alert「現在のプランは利用できない機能です。アップグレードが必要になります。」→ "
     "tự động redirect /admin/home\n"
     "• r43-r44 (Comment 6, khối MỚI hơn — Test Result = OK): đổi text sang「フリープランではデータコピーはご利用いただけません。"
     "（コピーコードの取得のみ可能です）」; click OK ⇒「Đóng modal, hiển thị màn hình tại Backup, KHÔNG bị back về màn home」",
     "feature-spec.md:207 BR-03 + §2.2 —「plan_type=2 (free) → alert『現在のプランは利用できない機能です。』→ redirect /admin/home」. "
     "Nguồn: backup_new.blade.php:1001-1004.",
     "Vừa đổi TEXT vừa đổi HÀNH VI (redirect ⇄ ở lại). Ảnh hưởng trực tiếp tới việc bot free có xem/lấy được mã copy "
     "của chính nó hay không — mà theo MT-01 thì đây là điều kiện để bot free làm bên NGUỒN.",
     "TC-BK-72 → TC-BK-75",
     "",
     "Chốt xong phải: sửa BR-03 (text + hành vi), sửa §2.2 nhánh plan_type=2, và nêu rõ bot free được phép làm gì "
     "trên màn データコピー."],

    ["MT-03", "CAO", W,
     "Backup THẤT BẠI (status=3) hiển thị thế nào ở bảng lịch sử?",
     "[AI]UI r17 (TC-BK-016): status=3 hiển thị「エラー」+ nền đỏ nhạt, KHÔNG hiển thị「処理完了済」.\n"
     "[AI]UI r16 (TC-BK-015): status=2 hiển thị「完了」, KHÔNG hiển thị「処理完了済」.\n"
     "Cả 2 TC tự ghi Notes「THAY ĐỔI so với FA-033」.",
     "feature-spec.md:262 BR-08 + §3.1 bảng state machine —「status 0,1,4 →『処理中』; status 2,3 →『処理完了済』」, "
     "kèm cảnh báo in đậm:「Status=3 (thất bại) hiển thị『処理完了済』giống status=2 — người dùng không phân biệt được」. "
     "feature-spec.md §9.3 mục 1 và mục 5 cũng nêu đây là điểm cần confirm.",
     "Hai bên nói ngược nhau về đúng cột người dùng nhìn để biết copy thành công hay hỏng. "
     "Nếu spec đúng thì khách hàng có thể tưởng đã copy xong trong khi dữ liệu chưa sang.",
     "TC-BK-40 · TC-BK-61 → TC-BK-62",
     "",
     "Chốt xong phải: sửa BR-08 + bảng state machine §3.1 (cột『Hiển thị UI』) và đóng §9.3 mục 1 và mục 5."],

    ["MT-04", "CAO", W,
     "Danh sách「コピーされるデータ」là 13 loại hay 15 loại?",
     "[AI]UI r27 (TC-BK-026):「hiển thị đầy đủ ... danh sách 15 loại dữ liệu được copy」.\n"
     "Tab Info r8 (04/2026): SpecImprove #34158 —「[Backup] Có thể thêm『CSV管理・クロス分析』vào tính năng Backup không?」"
     "→ link tới tab [MN]Job TCs line 32.\n"
     "[MN]Job TCs r14-r52 có nguyên khối「1. Check back cross」và r53-r108「2. Check back up csv」.",
     "feature-spec.md:52-73 §1.3 — bảng đúng 13 loại, KHÔNG có クロス分析 và CSV管理.\n"
     "ui-spec.md Block 2 — liệt kê đúng 13 mục.\n"
     "NHƯNG feature-spec.md:535 §7.5 — thứ tự bảng copy có `cross_analysis` (34) và `csv_management` (35), "
     "và db-mapping.md:425-426 ghi cả 2 là `is_enable=1`.",
     "Spec TỰ MÂU THUẪN: §1.3 + ui-spec nói 13 loại, §7.5 + db-mapping nói job vẫn copy cross_analysis + csv_management. "
     "Nếu 2 loại này thực sự được copy mà UI không liệt kê thì user không biết dữ liệu nào đã bị ghi sang bot đích.",
     "TC-BK-02 · TC-BK-279 → TC-BK-280 · TC-BK-295 → TC-BK-314",
     "",
     "Chốt xong phải: ① thống nhất con số trên UI; ② sửa §1.3 + ui-spec Block 2 nếu là 15; "
     "③ nếu vẫn 13 thì phải giải thích vì sao job copy 2 bảng không được khai báo với người dùng."],

    ["MT-05", "CAO", W,
     "Độ dài mã copy: 10 ký tự hay 16 ký tự?",
     "[AI]API r18 (TC-BK-050) và r28 (TC-BK-060):「new_code dài ĐÚNG 10 ký tự alphanumeric」, logic `Str::random(10)`.\n"
     "[AI]UI r3 (TC-BK-002):「mã mới (alphanumeric, dài 10~16 ký tự)」.\n"
     "[AI]UI r24 (TC-BK-023): test nhập 17 ký tự, kỳ vọng FE có `maxlength=16` HOẶC backend không tìm thấy.",
     "feature-spec.md:203 BR-01 + §3.1 — `bots.transfer_code` varchar(16).\n"
     "feature-spec.md §9.1 BK-Q02 —「data thực tế ~10 ký tự alphanumeric (GNBGFMhyBH)」; §9.2 V-API-02 ghi "
     "「Request mẫu EP-02 dùng 16 ký tự — không phản ánh thực tế (~10 ký tự)」.\n"
     "feature-spec.md §9.3 mục 3 —「Cơ chế tạo transfer_code ... định dạng chính xác chưa được xác nhận từ source code」.",
     "3 con số cùng tồn tại (10 / 10~16 / 16). Không chốt thì không viết được TC biên cho ô nhập mã, "
     "cũng không biết `maxlength` trên UI phải là bao nhiêu.",
     "TC-BK-09 · TC-BK-23",
     "",
     "Chốt xong phải: ghi rõ độ dài + tập ký tự + có phân biệt hoa/thường không vào BR-01, và đóng §9.3 mục 3."],

    ["MT-06", "CAO", W,
     "Hai LOA nguồn cùng copy vào MỘT LOA đích trong khi job đang chạy — cho phép cả 2 hay chỉ 1?",
     "3 TC trong CÙNG tab [AI]UI TCs nói ngược nhau:\n"
     "• r37 (TC-BK-036):「Backup từ bot A > bot B; backup tiếp TRONG QUÁ TRÌNH ĐANG XỬ LÝ từ bot C > bot B」"
     "⇒ kỳ vọng「Backup được cả bot A và B」(nguyên văn — tên bot ghi lẫn lộn).\n"
     "• r38 (TC-BK-037):「Backup từ bot 1 > bot 2 với mã A; tab 2 backup từ bot 3 > bot 2 với mã B」"
     "⇒ kỳ vọng「CHỈ backup được từ bot 3 sang bot 2, mã cũ sẽ hiển thị msg lỗi」.\n"
     "• r40 (TC-BK-039):「đang backup bot A > sang backup bot B」⇒「Backup được cả bot A và B」.",
     "feature-spec.md:210 BR-04 — khi LOA đích đang nhận (status 0/1) thì thao tác WRITE trên LOA đó bị khoá "
     "(Popup / Event / RichMenu). KHÔNG có rule nào chặn việc ĐĂNG KÝ thêm một backup thứ 2 vào cùng LOA đích.\n"
     "feature-spec.md §9.1 BK-Q10 —「Có thể sao chép từ nhiều LOA nguồn khác nhau sang cùng 1 LOA đích không? "
     "→ Không có giới hạn trong code — có thể được」(mức Thấp, chưa xác nhận).",
     "Rủi ro mất dữ liệu thật: 2 job cùng ghi vào 1 LOA đích thì bot đích có thể nhận dữ liệu trộn của 2 nguồn, "
     "hoặc nhân đôi folder/tag/template. TC gốc lại tự phủ định nhau nên member không biết đâu là đúng.",
     "TC-BK-88 → TC-BK-90 · TC-BK-92 · TC-BK-346",
     "",
     "Chốt xong phải: bổ sung BR mới về khoá LOA đích khi đang có backup, và đóng BK-Q10."],

    ["MT-07", "TRUNG BÌNH", W,
     "Bảng lịch sử copy có phân trang không? Mặc định bao nhiêu dòng?",
     "[AI]UI r28-r29 (TC-BK-027/028): có pagination; dropdown options 10/20/30/50/100; mặc định 100.\n"
     "[AI]API r5 (TC-BK-037) và r29 (TC-BK-061): `GET /basic/backup?page=2&per_page=10`, "
     "response có `backupHistory.current_page` / `per_page` / `total`; default `per_page=100`.",
     "feature-spec.md §9.1 BK-Q07 —「Bảng lịch sử có phân trang không? → Chưa xác nhận — logic-spec: "
     "`BackupHistory(bot_id, desc created_at)` KHÔNG có LIMIT」(mức Thấp).\n"
     "feature-spec.md §6 EP-01 — danh sách dữ liệu truyền vào view chỉ ghi `backupHistory` (sắp xếp DESC created_at).",
     "TC lấp được đúng gap mà spec tự nhận là chưa biết. Nếu Leader duyệt thì đây là điểm ĐÓNG GAP chứ không phải bug.",
     "TC-BK-65 → TC-BK-66",
     "",
     "Chốt xong phải: đóng BK-Q07, bổ sung tham số `page` / `per_page` vào EP-01 trong api-spec.md."],

    ["MT-08", "CAO", W,
     "Trong lúc copy, bên nào bị khoá thao tác — chỉ LOA đích hay CẢ HAI? Mốc「khoảng 1 giờ」ở đâu ra?",
     "[AI]UI r32 (TC-BK-031): cảnh báo nền vàng trên SCR-01 ghi「trong quá trình copy CẢ tài khoản nguồn VÀ tài khoản đích "
     "có thể không thao tác được trong tối đa KHOẢNG 1 GIỜ」.\n"
     "[AI]UI r33 (TC-BK-032): modal SCR-03 có khối「注意事項」đỏ 3 dòng —「downtime, automation vẫn chạy, và nội dung thứ 3」 "
     "(TC gốc KHÔNG ghi rõ dòng thứ 3 là gì).",
     "feature-spec.md:638-646 §8.2 — bảng 3 controller bị khoá, kèm「**Lưu ý quan trọng**: Block mechanism áp dụng trên "
     "LOA ĐÍCH (account nhận dữ liệu), KHÔNG phải LOA nguồn」.\n"
     "Spec KHÔNG có bất kỳ mốc thời gian nào (1 giờ hay khác) cho quá trình copy.",
     "Spec khẳng định dứt khoát chỉ khoá LOA đích; UI lại cảnh báo khoá cả 2 phía. "
     "Và mốc「1 giờ」là cam kết với khách hàng nhưng không có căn cứ trong code/spec.",
     "TC-BK-04 · TC-BK-29 · TC-BK-93 → TC-BK-95",
     "",
     "Chốt xong phải: ① xác nhận danh sách ĐẦY ĐỦ màn bị khoá (spec mới chỉ liệt kê 3 controller); "
     "② xác nhận có khoá LOA nguồn không; ③ ghi rõ dòng thứ 3 của khối 注意事項; ④ căn cứ cho mốc 1 giờ."],

    ["MT-09", "THẤP", W,
     "Ô nhập mã có tự cắt khoảng trắng đầu/cuối không?",
     "[AI]UI r23 (TC-BK-022) viết kỳ vọng THEO 2 NHÁNH (nếu FE trim thì OK, nếu không trim thì báo không tồn tại) "
     "rồi ghi thêm ở cuối ô:「Tự trim space, hiển thị ra bot backup」và cột Test Result = OK.",
     "feature-spec.md §6 EP-02/EP-03 — validation chỉ có `required|exists:bots`. KHÔNG nhắc trim.",
     "TC viết 2 nhánh là chưa quyết được; ghi chú cuối ô mới là hành vi thật đã đo. Cần chốt để TC có 1 kết quả duy nhất.",
     "TC-BK-22",
     "",
     "Chốt xong phải: bổ sung 1 dòng vào api-spec.md EP-03 nêu rõ có trim hay không."],

    ["MT-10", "CAO", W,
     "`queue_richmenu_id` của richmenu sau khi copy: FILL id richmenu mới hay để NULL?",
     "Backup (job) r59 — TỰ MÂU THUẪN TRONG CÙNG 1 Ô:\n"
     "• Cột đường dẫn:「Nếu ĐÃ được tạo trên line thì lúc backup sẽ tạo richmenu trên bot được backup và "
     "`queue_richmenu_id` FILL id của richmenu đó」\n"
     "• Cột Expect Result:「`queue_richmenu_id` của bot đích sẽ không được trùng bot gốc. "
     "Trường `queue_richmenu_id` không dùng để sử dụng làm j nên ĐỂ NULL (anh Tư chốt spec)」\n"
     "r58:「Nếu CHƯA được tạo trên line thì lúc backup `queue_richmenu_id = NULL`」.",
     "feature-spec.md §7.4 post-processing — có bước「richMenusBackup → createRichmenu() [gọi LINE API internal "
     "/create-richmenu-by-id]」. job-spec.md không nói `queue_richmenu_id` được set thế nào.",
     "Nếu để NULL mà job vẫn gọi LINE API tạo richmenu thật thì richmenu tồn tại trên LINE nhưng tool không tham chiếu "
     "được ⇒ rác trên LINE + không stop/đổi được richmenu ở bot đích.",
     "TC-BK-116 · TC-BK-347",
     "",
     "Chốt xong phải: ghi rõ giá trị `queue_richmenu_id` sau copy vào job-spec.md §6.2 và db-mapping.md."],

    ["MT-11", "TRUNG BÌNH", W,
     "Thời gian hiển thị richmenu (表示予約) có được copy không?",
     "Backup (job) r67-r70 (khối Improve 10/2025 — mới nhất):「chỗ này db không dùng nữa — khi backup KHÔNG backup thời gian "
     "setting ON-OFF richmenu」, áp cho cả `time_display=0`, `time_display=1 + open_date + close_date`, `end_time_display=1`.\n"
     "Backup 1.0 r28-r29 (bản cũ): vẫn liệt kê `time_display` / `open_date` / `close_date` là data PHẢI check sau backup.",
     "feature-spec.md §7.5 — `rich_menus` (order 14) được copy; `reset_columns_value` có trong `backup_config` nhưng "
     "spec KHÔNG liệt kê cột nào bị reset cho `rich_menus`.",
     "Bản cũ bảo phải check, bản mới bảo không copy. Nếu thực tế vẫn copy `open_date/close_date` của bot gốc thì "
     "richmenu ở bot đích có thể tự bật/tắt theo lịch của bot khác.",
     "TC-BK-120",
     "",
     "Chốt xong phải: liệt kê `reset_columns_value` thực tế của `rich_menus` vào db-mapping.md."],

    ["MT-12", "CAO", W,
     "Action richmenu「mở URL salon / lesson」sau copy sẽ ra gì?",
     "Backup (job) r84-r85:「2 cái này sẽ KHÔNG backup được do chưa có job backup của salon và lesson?」 "
     "— nguyên văn CÓ DẤU HỎI, tức người viết cũng chưa chắc, và ô Expect KHÔNG nói bot đích hiển thị ra sao.\n"
     "So sánh: r87-r90 (action mở item) ghi rõ「Item không backup, nên ở drop down chọn item không có item — "
     "chỉ hiển thị focus vào mục action item」.",
     "feature-spec.md §1.3 (13 loại) và §7.5 — KHÔNG nhắc salon hay lesson. "
     "db-mapping.md:406 — `booking_calendar` là `is_enable=0` (disabled).",
     "Có 3 khả năng khác nhau khi mở richmenu ở bot đích: (a) area mất action, (b) area giữ action nhưng trỏ id của bot gốc "
     "(rò rỉ dữ liệu chéo bot), (c) hiển thị dropdown rỗng như item. Chưa chốt thì không viết được kết quả mong đợi.",
     "TC-BK-134 → TC-BK-135",
     "",
     "Chốt xong phải: bổ sung mục『dữ liệu không copy』vào feature-spec §1.3 nêu rõ salon/lesson "
     "+ hành vi của action trỏ tới chúng."],

    ["MT-13", "CAO", W,
     "Filter chứa điều kiện QRコードアクション hoặc アフィリエイター — bỏ RIÊNG điều kiện đó hay bỏ CẢ filter?",
     "Backup (job) r334 (`qr_code`) và r343 (`affiliate`):「không backup ⇒ KHÔNG TẠO BẢN GHI `filter_v2` đối với type này」.\n"
     "[MN]Job TCs r63-r64: trong danh sách điều kiện and/or của CSV ghi「QRコードアクション ⇒ qr k back up được」và "
     "「アフィリエイター ⇒ k back up được」, nhưng ô Expect chung lại ghi「back up thành công ... "
     "hiển thị list friend thỏa mãn theo bot」.",
     "feature-spec.md §7.4 + job-spec.md:367-387 §6.3 —「doBackupFilter() clone tương ứng bảng `filters_v2` (điều kiện lọc)」, "
     "KHÔNG liệt kê loại điều kiện nào bị loại.",
     "Nếu chỉ bỏ 1 điều kiện trong filter AND thì filter ở bot đích sẽ LỎNG hơn bot gốc (khớp nhiều friend hơn) — "
     "gửi tin sai đối tượng. Nếu bỏ cả filter thì broadcast/scenario/CSV gắn filter đó mất điều kiện lọc hoàn toàn.",
     "TC-BK-111 · TC-BK-130 · TC-BK-160 · TC-BK-239 · TC-BK-259 · TC-BK-271 · TC-BK-276 · TC-BK-286 → TC-BK-287 · TC-BK-298 · TC-BK-300 · TC-BK-333 · TC-BK-337",
     "",
     "Chốt xong phải: bổ sung vào job-spec.md §6.3 danh sách type filter bị loại và hành vi với filter cha."],

    ["MT-14", "CAO", W,
     "Ai tính lại「対象人数」của file CSV ở bot đích sau khi copy?",
     "[MN]Job TCs r104 và r106:「sau khi back up 100% JOB SẼ PHẢI TỰ ĐỘNG CHẠY để lấy số user thỏa mãn điều kiện csv "
     "mà KHÔNG cần nhấn vào reload file hoặc edit file mới tính toán — Tự tính toán số friend của bot B theo các điều kiện "
     "filter của từng file CSV」.\n"
     "Tương tự [MN]Job r20: cross analysis「Với mục phân tích = ngày addfriend, tại bot nhận backup sẽ thực hiện COUNT LẠI "
     "các friend nằm trong date from-to」.",
     "job-spec.md — CHỈ mô tả duy nhất `BackupBotTask` (threadPollQueue + threadBackup). "
     "feature-spec.md §7 KHÔNG có job nào tính lại 対象人数 hay chạy lại phân tích cross.",
     "Corpus khẳng định có một job chạy sau backup; spec không biết job đó tồn tại. VÙNG MÙ: nếu job không có thật, "
     "user mở màn CSV ở bot đích sẽ thấy số 対象人数 của bot gốc (số sai) cho tới khi tự bấm reload.",
     "TC-BK-284 · TC-BK-293 · TC-BK-297 · TC-BK-312",
     "",
     "Chốt xong phải: xác định tên job + chu kỳ, bổ sung vào job-spec.md; nếu không có job thì sửa kỳ vọng của TC."],

    ["MT-15", "TRUNG BÌNH", W,
     "Cross analysis: copy điều kiện thôi hay copy cả kết quả phân tích?",
     "[MN]Job TCs r20-r40 lặp lại nhiều lần:「Chỉ back up ĐIỀU KIỆN — KHÔNG back up số friend thỏa mãn — "
     "back up thành công ⇒ edit/thêm/xóa điều kiện ⇒ hiển thị list friend thỏa mãn THEO BOT」.\n"
     "r47:「Kết quả phân tích: Không backup」. r45:「created_at / updated_at: Lấy theo thời điểm backup」. "
     "r46:「số lượng filter_parent_id: Không backup」.\n"
     "r52:「Các cross đã backup sẽ được job chạy đúng với data của bot đích」.",
     "job-spec.md:362 — chỉ có 1 dòng「`cross_analysis.filter_tag_ids` → Remap tag IDs」. "
     "feature-spec.md §1.3 không có クロス分析 (xem MT-04).",
     "Spec không mô tả bảng con nào của cross được copy, cột nào bị reset, kết quả phân tích xử lý ra sao. "
     "Cả một tính năng nằm trong phạm vi copy nhưng gần như không có spec.",
     "TC-BK-279 → TC-BK-294",
     "",
     "Chốt xong phải: viết mục cross_analysis cho job-spec.md §6.2 (cột remap + cột reset) "
     "và bổ sung vào §1.3 nếu MT-04 chốt là 15 loại."],

    ["MT-16", "CAO", W,
     "Action「リマインド」sau copy có còn trỏ id remind của BOT GỐC không? (đã fix hay chưa)",
     "Backup 1.0 (bản cũ) ghi lỗi ở 4 chỗ:\n"
     "• r16 (action remind của autoreply):「`t_action_detail` đang lấy id remind của bot gốc ⇒ Thanh: chỗ này c check lại "
     "thấy VẪN LỖI」\n"
     "• r46 (multi action của richmenu):「`t_action_detail` đang lấy id remind của bot gốc」\n"
     "• r102 (remind của form):「Bảng `form_answer_details`, cột `setting` vẫn đang để id remind của bot gốc "
     "→ form có remind bị thêm lỗi DUPLICATE ITEM」\n"
     "• r237 (remind của slot booking event):「đang bị lấy id remind của bot gốc」\n"
     "Backup (job) — bản MỚI hơn, cùng các dòng r15 / r45 / r189 / r259 — KHÔNG còn ghi chú lỗi.",
     "feature-spec.md §7.4 post-processing — có bước「formAnswerDetailBackups → fix event/remind FK」. "
     "job-spec.md liệt kê `events` (19), `event_step` (20) trong danh sách bảng copy.",
     "Không rõ ghi chú biến mất là vì ĐÃ FIX hay vì tab mới chỉ chưa ghi lại. Đây là lỗi rò rỉ dữ liệu chéo bot "
     "(bot đích gửi remind của bot gốc) nên không được để mập mờ.",
     "TC-BK-107 · TC-BK-126 · TC-BK-194 · TC-BK-204 · TC-BK-231",
     "",
     "Chốt xong phải: xác nhận trạng thái fix; nếu chưa fix thì raise bug; nếu đã fix thì ghi rõ bước remap "
     "`t_action_detail` và `form_answer_details.setting` vào job-spec.md §6.2."],

    ["MT-17", "CAO", W,
     "Conversion sau copy có bị gán nhầm folder của bot gốc không?",
     "Backup 1.0 r254 (Note):「bị backup SAI FOLDER (chưa tạo folder mới mà đang lấy theo folder id của bot cũ)」, "
     "kèm Expect「Chỉ back up các conversion có setting ở action friend (action open link conversion)」.\n"
     "Backup (job) r276 (bản mới hơn) chỉ còn dòng trống「10. Conversion」, không ghi chú, không expect.",
     "feature-spec.md §7.5 — `conversion` là bảng main order 10, được copy. "
     "job-spec.md không mô tả cách remap `folder_id` của conversion.",
     "Giống MT-16: ghi chú lỗi biến mất mà không có bằng chứng đã fix. Folder id trỏ bot gốc = rò rỉ dữ liệu chéo bot. "
     "Ngoài ra phạm vi「chỉ copy conversion có dùng trong action」cũng không có trong spec.",
     "TC-BK-138 · TC-BK-173 · TC-BK-243 → TC-BK-244 · TC-BK-272",
     "",
     "Chốt xong phải: xác nhận trạng thái fix + bổ sung quy tắc remap folder cho conversion vào job-spec.md."],

    ["MT-18", "CAO", W,
     "友だち情報 sau copy: có bị DUPLICATE FOLDER và MẤT setting time action của info kiểu ngày không? "
     "Phạm vi copy là TẤT CẢ info hay chỉ info đang được dùng?",
     "Backup 1.0 r191 (Note):「- Friend infor type date bị MẤT setting time action\n- đang bị DUPLICATE FOLDER」, "
     "kèm Expect「Chỉ back up các friend infor CÓ SETTING Ở FORM VÀ TRONG ACTION」.\n"
     "Backup (job) r208-r213 (bản mới) chỉ liệt kê type text/select/ảnh/file/point/date, không ghi chú.\n"
     "Backup 1.0 r193-r201:「dạng cơ bản sẽ KHÔNG backup — mặc định bot nào cũng sẽ có」"
     "(system name, SĐT, mail, birthday, 5 dạng địa chỉ).",
     "feature-spec.md §7.5 — `friend_information_setting` (+subs) là bảng main order 16.\n"
     "feature-spec.md §1.3 —「友だち情報」nằm trong 13 loại. "
     "Spec KHÔNG nói friend info mặc định bị loại, KHÔNG nói phạm vi「chỉ copy info có dùng trong form/action」.",
     "Phạm vi copy friend info trong corpus HẸP HƠN spec, cộng thêm 2 lỗi chưa rõ đã fix. "
     "Nếu spec đúng thì phải copy toàn bộ info; nếu corpus đúng thì info không dùng sẽ mất khi copy.",
     "TC-BK-214 · TC-BK-216 · TC-BK-221",
     "",
     "Chốt xong phải: ① chốt phạm vi copy friend info; ② xác nhận 2 lỗi duplicate folder / mất time action; "
     "③ ghi rõ nhóm info mặc định không copy vào feature-spec §1.3."],

    ["MT-19", "TRUNG BÌNH", W,
     "Folder của リマインド配信 có được copy không? Message tạo trực tiếp ở màn remind có copy được không?",
     "Backup 1.0 r245 (Note):「9. Remind > folder — CHƯA BACK UP FOLDER」.\n"
     "Backup 1.0 r251 (Note):「message tạo trực tiếp ở màn remind — KHÔNG BACK UP ĐƯỢC MSG」.\n"
     "Backup (job) r267 / r273 (bản mới): vẫn liệt kê「folder」và「message tạo trực tiến ở màn remind」nhưng KHÔNG ghi chú.",
     "feature-spec.md §1.3 —「リマインド配信」nằm trong 13 loại (bảng `events`, `event_step`).\n"
     "§7.5 — `events` (19), `event_step` (20), `event_times` (21). Không có bảng folder riêng cho remind trong danh sách.",
     "Nếu folder remind không được copy thì toàn bộ remind ở bot đích rơi vào folder mặc định — "
     "khách hàng có hàng chục remind sẽ mất hoàn toàn cách sắp xếp. Nếu message không copy thì remind gửi ra rỗng.",
     "TC-BK-236 · TC-BK-240",
     "",
     "Chốt xong phải: xác nhận có bảng folder cho remind không và có nằm trong `backup_config` không."],

    ["MT-20", "TRUNG BÌNH", W,
     "イベント予約: copy 2 folder khác folder mặc định thì có bị nhân đôi 1 folder không? "
     "friend info của event có liên kết được với info cơ bản không?",
     "Backup 1.0 r221 (Note):「setting 2 folder khác folder default thì có 1 folder bị DUPLICATE?」— nguyên văn có dấu hỏi.\n"
     "Backup 1.0 r243 (Note):「friend infor — KHÔNG LIÊN KẾT ĐƯỢC với friend infor basic」.\n"
     "Backup (job) r243 / r265 (bản mới) không ghi chú.",
     "feature-spec.md §7.5 — `b_event_detail` (11), `b_slot` (+`b_plan_slot`) (30), `b_info_setting` (31).\n"
     "Spec không mô tả folder của event nằm ở bảng nào (`category` order 1 với `kind` tương ứng?).",
     "Duplicate folder là lỗi nhìn thấy ngay trên UI bot đích. Ghi chú có dấu hỏi tức chưa ai xác nhận.",
     "TC-BK-225 · TC-BK-234",
     "",
     "Chốt xong phải: xác nhận cơ chế copy `category` theo `kind` cho từng tính năng và bổ sung vào job-spec.md."],

    ["MT-21", "CAO", W,
     "イベント予約 bản mới (予約カレンダー / `booking_calendar`) — không copy, nhưng có tạo bản ghi lỗi ở bot đích không?",
     "Backup 1.0 r256 (Note):「12. Booking event mới (release 29.3) — CHƯA SUPPORT nhưng test thì THẤY CÓ TẠO EVENT "
     "nhưng BỊ LỖI do chỗ `setting_date_id` vẫn lấy id của bot cũ ⇒ Tạm thời sửa để KHÔNG backup event mới」.\n"
     "Backup (job) r278 chỉ còn「12. Booking event mới (release 29.3)」, không expect, không ghi chú.\n"
     "Improve backup media r95: calendar「ko backup」.",
     "db-mapping.md:406 — `booking_calendar` `is_enable=0` (disabled).\n"
     "feature-spec.md §7.5 — `booking_calendar` nằm trong「Bảng disabled ... bỏ qua」.",
     "Spec nói bỏ qua hoàn toàn; corpus từng ghi nhận có tạo bản ghi lỗi rồi「tạm thời sửa để không backup」. "
     "Cần biết bản fix đó có còn hiệu lực sau khi tính năng calendar được phát triển tiếp không.",
     "TC-BK-331 · TC-BK-338",
     "",
     "Chốt xong phải: xác nhận `booking_calendar` (và các bảng con) vẫn `is_enable=0` trên production; "
     "bổ sung mục『Dữ liệu KHÔNG được copy』có kèm tên tính năng người dùng nhìn thấy."],

    ["MT-22", "TRUNG BÌNH", W,
     "Khối 28 dòng TC「13. Popup」trong corpus còn giá trị không?",
     "Backup (job) r280:「13. Popup ⇒ TẠM THỜI KHÔNG BACKUP NỮA」nhưng NGAY SAU đó r281-r308 vẫn liệt kê 28 dòng chi tiết "
     "(folder, list, script nhúng, kiểu hiển thị 3 loại, ảnh, button, redirect, countdown 3 mốc + 3 độ chính xác, "
     "setting môi trường điện thoại/tablet/pc, setting số lần hiện 3 kiểu).\n"
     "r292:「Do không backup qr code nên chỗ id của qr code trong popup rỗng」.\n"
     "Improve backup media r94: popup「ko backup」.",
     "db-mapping.md:415 — `popup` `is_enable=0`. feature-spec.md §7.5 — `popup` nằm trong nhóm disabled.",
     "28 dòng TC được viết cho một tính năng đã bị tắt khỏi phạm vi copy. Nếu giữ nguyên thì member mất công dựng "
     "dữ liệu popup phức tạp cho kết quả duy nhất là「không có gì ở bot đích」.",
     "TC-BK-330",
     "",
     "Chốt xong phải: quyết giữ 2 TC xác nhận-không-copy (đề xuất) hay khôi phục đủ 28 TC nếu popup sẽ được copy lại."],

    ["MT-23", "CAO", W,
     "Đường dẫn ảnh sau khi copy — spec không mô tả, corpus mô tả rất cụ thể",
     "improve url image r21-r26 (24/08/2025):\n"
     "• Ảnh dạng cũ 1: `/msg_template/image/1611379719RRWmi7.png` (ghi rõ「CASE BỊ BUG」) "
     "⇒ sau backup vào `/ext-media-step/media/images/29/105681/image/1611379719RRWmi7.png`\n"
     "• Ảnh dạng cũ 2: `/msg_template/image/16208990343AS/16208990343AS.jpg`\n"
     "• Ảnh dạng mới: `/ext-media-step/media/images/118495/157064/1752577402E2j7Kf/1752577402E2j7Kf.jpg` "
     "⇒ sau backup vào `/ext-media-step/media/images/29/105681/17560624733AoZpg/17560624733AoZpg.jpg`\n"
     "Tab Info r5 (24/08/2025):「[Bug tự detect] Backup template image folder dạng cũ /msg_template/image "
     "BỊ COPY CẢ FOLDER image」.",
     "feature-spec.md BR-12 + §7.4 — chỉ ghi「copy file vật lý (ảnh/video/audio) qua Dropbox API」và "
     "job-spec.md §6.2 liệt kê các cột media được copy. KHÔNG có quy tắc đường dẫn đích, "
     "KHÔNG phân biệt ảnh dạng cũ / dạng mới.",
     "Không có quy tắc đường dẫn thì không kiểm chứng được ảnh đã sang đúng chỗ, và không phát hiện lại được "
     "lỗi「copy cả folder image」từng xảy ra.",
     "TC-BK-114 · TC-BK-317 → TC-BK-320 · TC-BK-322",
     "",
     "Chốt xong phải: viết quy tắc sinh đường dẫn media sau copy (theo bot id / admin id đích) vào job-spec.md §6.2."],

    ["MT-24", "TRUNG BÌNH", W,
     "Thumbnail của template video sau copy: NG hay OK?",
     "Backup image (bản cũ): r28「video - thumbnail > data cũ > check ảnh」= **NG**; "
     "r30「data mới > check ảnh」= **NG**; nhưng r29/r31「hiển thị bên user」= OK.\n"
     "improve url image (bản mới, 24/08/2025): r29/r30「video - thumbnail > data mới > check ảnh / hiển thị bên user」"
     "= **OK Step**; r27/r28 (nhánh data cũ) BỎ TRỐNG kết quả.",
     "job-spec.md §6.2 — có cột media của template được copy; không tách riêng `thumbnail_path` của video.\n"
     "Improve backup media r19/r29 (2024-01) có dòng `template.thumbnail_path`.",
     "Cùng 1 hạng mục, bản cũ FAIL bản mới PASS, và bản mới KHÔNG đo lại nhánh「data cũ」— "
     "nghĩa là nhánh ảnh cũ vẫn có thể còn hỏng.",
     "TC-BK-180 · TC-BK-321",
     "",
     "Chốt xong phải: đo lại nhánh video-thumbnail data cũ; nếu vẫn NG thì raise bug."],

    ["MT-25", "CAO", W,
     "「Backup từ bot staff ⇒ bot chính」— TC lặp 5 lần nhưng KHÔNG có kết quả mong đợi, mà spec nói Staff không có menu",
     "Xuất hiện 5 lần, luôn để TRỐNG ô Expect Result:\n"
     "• Backup 1.0 r186 (sau khối Form), r220 (sau khối Friend infor), r309 (sau khối Setting kết bạn), "
     "r314「Check thao tác của account staff」, r330「Check account staff」\n"
     "• Backup (job) r242, r399",
     "feature-spec.md §1.2 —「Staff: KHÔNG có quyền truy cập. Menu「データコピー」không hiển thị với Staff」.\n"
     "ui-spec.md §2 —「Staff: Không có quyền truy cập (menu không hiển thị với Staff)」.\n"
     "feature-spec.md §9.1 BK-Q08 —「middleware CHƯA VERIFY server-side access control」.",
     "TC giả định tồn tại「bot staff」làm nguồn copy, trong khi spec khẳng định Staff không vào được màn này. "
     "Hai khả năng: (a)「bot staff」ở đây là bot phụ do tài khoản staff quản lý chứ không phải role Staff, "
     "(b) thực tế Staff vẫn thao tác được ⇒ lỗ hổng phân quyền.",
     "TC-BK-69 → TC-BK-71 · TC-BK-359",
     "",
     "Chốt xong phải: ① làm rõ định nghĩa「bot staff」; ② test trực tiếp URL /basic/backup bằng session Staff "
     "để đóng BK-Q08; ③ nếu Staff vào được thì raise bug bảo mật."],

    ["MT-26", "TRUNG BÌNH", W,
     "Bấm「データコピーを開始」2 lần liên tiếp (double submit) — chặn hay tạo 2 bản ghi?",
     "[AI]API r24 (TC-BK-056) viết kỳ vọng THEO 2 NHÁNH và ghi rõ「phụ thuộc QA-010 — CHƯA CÓ ANSWER」, "
     "「No automation vì behavior chưa xác định」.",
     "feature-spec.md §6 EP-02 — không có double-submit check. §9.1 BK-Q06 —「Giới hạn số lần sao chép? Có rate limit không? "
     "→ Chưa tìm thấy giới hạn trong source code — khả năng KHÔNG có」.",
     "Nếu không chặn thì 2 job cùng copy 1 nguồn sang 1 đích ⇒ dữ liệu bị nhân đôi ở bot đích. Liên quan trực tiếp MT-06.",
     "TC-BK-91 · TC-BK-346",
     "",
     "Chốt xong phải: trả lời QA-010, bổ sung BR về double submit, đóng BK-Q06."],

    ["MT-27", "TRUNG BÌNH", W,
     "Đang ở màn processing mà LOGOUT hoặc ĐỔI BOT thì sao?",
     "[AI]UI r41 (TC-BK-040)「Check khi bot đang backup > logout」và r42 (TC-BK-041)「Check khi bot đang backup > đổi bot」"
     "— cả 2 dòng CHỈ CÓ TIÊU ĐỀ, không có bước, không có kết quả mong đợi.",
     "feature-spec.md — không mô tả gì về vòng đời phiên khi đang có backup chạy. "
     "BR-10 chỉ nói web không xử lý đồng bộ (job chạy nền).",
     "Đây là 2 thao tác người dùng thật hay làm khi thấy màn blocking lâu. Không có kết quả mong đợi thì member không chạy được.",
     "TC-BK-42 → TC-BK-45",
     "",
     "Chốt xong phải: chốt hành vi (job vẫn chạy tiếp? quay lại có vào lại được màn processing không?) "
     "và bổ sung vào §2.2 luồng phụ."],

    ["MT-28", "TRUNG BÌNH", W,
     "Danh sách dữ liệu KHÔNG được copy — 3 nguồn liệt kê khác nhau, và mâu thuẫn thẳng ở bảng `url`",
     "Improve backup media r83-r101 (2024-01, đo thực tế trên bot đích): KHÔNG copy = "
     "「tạo ảnh richmenu」·「url redirect trong template text」·「popup」·「calendar (ảnh calendar / staff / course)」· "
     "「item (univapay 1 lần, stripe chu kỳ)」·「ASP ảnh bot」·「item add friend」·「item khác」.\n"
     "Backup (job) r277:「11. url redirect — không support」; r334: `qr_code` không backup; r343: `affiliate` không backup.\n"
     "Backup 1.0 r36-r37:「Đang không support backup item / calendar nên ở đây không có item / calendar」.",
     "feature-spec.md §7.5「Bảng disabled (is_enable=0)」= `s_items`, `booking_calendar`, `add_friend_setting` (xử lý riêng), "
     "`bot_service`, `popup` — ĐÚNG 5 bảng.\n"
     "NHƯNG `url` (order 27) lại là `is_enable=1` trong db-mapping.md:417, trái với「url redirect — không support」.",
     "Danh sách của spec (5 bảng) không phủ hết cái corpus đo được (8 nhóm), và mâu thuẫn thẳng ở `url`: "
     "spec bảo copy, corpus bảo không support.",
     "TC-BK-03 · TC-BK-137 · TC-BK-172 · TC-BK-246 · TC-BK-329 · TC-BK-333 → TC-BK-334 · TC-BK-337",
     "",
     "Chốt xong phải: ① làm rõ `url` (order 27) là URL nào — url rút gọn hay url redirect trong template; "
     "② viết mục『Dữ liệu KHÔNG được copy』bằng NGÔN NGỮ NGƯỜI DÙNG (tên tính năng) chứ không chỉ tên bảng."],

    ["MT-29", "THẤP", W,
     "Spring Boot đọc `backup_config` hay `backup_config_dung`?",
     "Corpus KHÔNG có TC nào chạm 2 bảng này.",
     "feature-spec.md §9.3 mục 4 —「`backup_config` vs `backup_config_dung` — có 2 bảng CÙNG CẤU TRÚC, "
     "Spring Boot đọc từ bảng nào CHƯA RÕ (code đọc entity `BackupConfig` — cần kiểm tra JPA entity mapping)」.\n"
     "feature-spec.md §1 mô tả 4 bảng chính gồm cả `backup_config_dung`.",
     "VÙNG MÙ CẢ 2 PHÍA: spec tự nhận chưa rõ, corpus không có TC. Nếu 2 bảng lệch nhau thì "
     "tập bảng được copy trên môi trường này khác môi trường kia mà không ai phát hiện.",
     "TC-BK-352 → TC-BK-353",
     "",
     "Chốt xong phải: xác định bảng thật sự dùng, xoá/đổi tên bảng còn lại, đóng §9.3 mục 4."],

    ["MT-30", "THẤP", W,
     "Corpus TỰ TRÙNG MÃ TC — TC-BK-034 → TC-BK-039 tồn tại ở 2 tab với nội dung khác hẳn nhau",
     "• [AI]UI TCs r35-r40: TC-BK-034「change mã của bot backup giữa chừng」, TC-BK-035「dùng mã cũ sau khi đổi mã」, "
     "TC-BK-036「backup nhiều bot cùng lúc」, TC-BK-037「2 bot cùng backup vào 1 bot」, TC-BK-038「backup liên tiếp 3 lần」, "
     "TC-BK-039「đang backup bot A > sang backup bot B」\n"
     "• [AI]API TCs r2-r7: TC-BK-034「EP-01 load trang」, TC-BK-035「EP-01 activeBackup」, TC-BK-036「EP-01 redirect login」, "
     "TC-BK-037「EP-01 pagination」, TC-BK-038「EP-02 submit thành công」, TC-BK-039「EP-02 transfer_code rỗng」\n"
     "Ngoài ra [MN]Job TCs nhảy từ TC-BK-067 sang TC-BK-075 (thiếu 068-074).",
     "Không liên quan spec — đây là vấn đề chất lượng corpus.",
     "Không thể trích dẫn「TC-BK-036」mà không nói rõ tab nào; báo cáo kết quả test sẽ bị gộp nhầm.",
     "Toàn bộ TC gộp từ 3 tab [AI]/[MN] — kho đã đánh số lại nên không còn trùng",
     "",
     "Chốt xong phải: khi cập nhật lại 3 tab nguồn thì đánh số lại cho duy nhất, hoặc thêm tiền tố tab (UI/API/JOB)."],
]
