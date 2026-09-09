# -*- coding: utf-8 -*-
"""FA-013 友だちリスト — Nhóm 11-14: 3 màn phụ (非表示中の友だち · ブロックされた友だち ·
ブロックした友だち) và luồng xoá bạn bè + cascade.

Nguồn: 10.3 TCsLine_Friendlist → tab「Testcase」r140-r182 (Bug Tester #35742 — xoá
nhiều friend xong không reload được màn; Bug tự detect #38390 — xoá friend bị chậm,
kèm bộ TC kiểm tra cascade + kết bạn lại). Phần khung 3 màn phụ (cột, nút, bộ lọc
期間) KHÔNG có TC gốc → expected bám ui-spec.md và feature-spec.md, có ghi rõ.
"""
from _common import tc

HID = ("- Đăng nhập Admin (role 主管理者) của bot đã liên kết LINE OA\n"
       "- Bot có ≥ 3 friend đang bị ẩn (非表示)\n"
       "- Mở /basic/friendlist →「非表示中の友だち」(/basic/friendlist/hidden)")
UBLK = ("- Đăng nhập Admin của bot đã liên kết LINE OA\n"
        "- Bot có ≥ 3 friend đã block LINE OA từ phía user\n"
        "- Mở /basic/friendlist →「ブロックされた友だち」(/basic/friendlist/user-block)")
ABLK = ("- Đăng nhập Admin của bot đã liên kết LINE OA\n"
        "- Bot có ≥ 3 friend bị admin block\n"
        "- Mở /basic/friendlist →「ブロックした友だち」(/basic/friendlist/block)")
RICH = ("- Đăng nhập Admin của bot đã liên kết LINE OA\n"
        "- Chuẩn bị 1 friend có ĐẦY ĐỦ dữ liệu: đã quét QR có url rút gọn, đã trả lời form, "
        "đã đặt event/lesson/salon, đã mua item đơn và item chu kỳ, có tag, có friend info, "
        "có memo, có lịch sử scenario, có lịch sử hiển thị richmenu\n"
        "- Ghi lại đầy đủ danh sách dữ liệu trên trước khi xoá")

S6 = [
    # ═══════════ 11. Màn 非表示中の友だち ═══════════
    tc("Màn 非表示中の友だち", "UI-001", "Normal",
       "Màn 非表示中の友だち hiển thị đúng bộ lọc 期間, 6 cột và panel 一括友だち操作",
       HID,
       "1. Mở /basic/friendlist/hidden\n"
       "2. Đọc heading, bộ lọc khoảng thời gian, dòng tiêu đề bảng và panel dưới bảng",
       "Không nhập gì — chỉ quan sát",
       "- Có bộ lọc「表示期間」gồm 2 ô ngày, ngăn cách bằng「から」\n"
       "- Bảng có 6 cột đúng thứ tự:「全選択」·「非表示にした日時」·「LINE登録名」·"
       "「システム表示名」·「再表示」·「エルメ上から削除」\n"
       "- Cột「非表示にした日時」hiển thị format YYYY/MM/DD HH:MM:SS\n"
       "- Panel dưới bảng có heading「一括友だち操作」với 2 nút「再表示」và「削除」",
       spec="Đã hỏi leader",
       note="Corpus không có TC khung màn — expected bám ui-spec.md (SCR-FRL-04). "
            "Cần Leader xác nhận."),

    tc("Màn 非表示中の友だち", "LIST-001", "Normal",
       "Màn 非表示中の友だち KHÔNG phân trang — hiển thị toàn bộ friend đang ẩn",
       "- Đăng nhập Admin của bot có > 200 friend đang bị ẩn",
       "1. Mở /basic/friendlist/hidden\n"
       "2. Mở rộng bộ lọc「表示期間」để bao trọn mọi ngày đã ẩn\n"
       "3. Cuộn hết trang, đếm số dòng\n"
       "4. Tìm khu vực điều khiển phân trang",
       "> 200 friend đang bị ẩn",
       "- Toàn bộ friend đang ẩn hiển thị trên 1 trang\n"
       "- KHÔNG có nút phân trang\n"
       "- Số dòng đếm tay = tổng số friend đang ẩn",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám logic-spec.md:610 (danh sách hidden: không phân "
            "trang, get all). ⚠ Cần Leader xác nhận rủi ro hiệu năng khi bot có rất nhiều "
            "friend ẩn."),

    tc("Màn 非表示中の友だち", "LIST-001", "Normal",
       "Lọc theo 表示期間 — chỉ friend bị ẩn trong khoảng ngày chọn được hiển thị",
       HID + "\n- Chuẩn bị 3 friend bị ẩn ở 3 ngày khác nhau: 2026/02/20, 2026/03/06, 2026/03/25",
       "1. Mở /basic/friendlist/hidden\n"
       "2. Đặt khoảng lọc 2026/03/01 — 2026/03/10 → áp dụng\n"
       "3. Ghi lại danh sách friend hiển thị\n"
       "4. Đặt lại khoảng 2026/02/01 — 2026/03/31 → áp dụng, ghi lại danh sách",
       "3 friend ẩn ở 3 ngày · 2 khoảng lọc",
       "- Khoảng 03/01-03/10: chỉ friend ẩn ngày 2026/03/06 hiển thị\n"
       "- Khoảng 02/01-03/31: cả 3 friend hiển thị\n"
       "- Friend ẩn ngoài khoảng lọc KHÔNG xuất hiện",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md (Date Range Filter「表示期間」) + "
            "feature-spec.md §2 (filter datetime_hide BETWEEN). Cần Leader xác nhận biên "
            "(inclusive/exclusive) của 2 đầu khoảng."),

    tc("Màn 非表示中の友だち", "FUNC-001", "Normal",
       "Nút 再表示 trên từng dòng — friend quay lại danh sách chính",
       HID,
       "1. Ghi lại tên 1 friend đang ẩn và số「検索結果」ở danh sách chính\n"
       "2. Ở màn hidden, click nút「再表示」trên dòng của friend đó\n"
       "3. Reload màn hidden, tìm friend đó\n"
       "4. Mở danh sách chính, tìm friend đó và đọc lại số「検索結果」",
       "1 friend đang ẩn",
       "- Friend biến mất khỏi màn「非表示中の友だち」\n"
       "- Friend xuất hiện lại ở danh sách chính\n"
       "- Số「検索結果」ở danh sách chính tăng đúng 1\n"
       "- Sau khi bỏ ẩn, friend không còn giá trị「非表示にした日時」",
       note="Nguồn: TCsLine_Improve chung → tab「ESticsearch」r283 (『bỏ ẩn friend → nhấn bỏ ẩn "
            "ở màn /basic/friendlist/hidden』) + feature-spec.md §2 BR-03 (is_hide=0, "
            "datetime_hide=NULL)."),

    tc("Màn 非表示中の友だち", "BULK-001", "Normal",
       "Bulk 再表示 — bỏ ẩn hàng loạt friend đã chọn",
       HID + "\n- Bot có ≥ 5 friend đang bị ẩn",
       "1. Ghi lại số「検索結果」ở danh sách chính và tên 5 friend đang ẩn\n"
       "2. Ở màn hidden, tích「全選択」\n"
       "3. Click nút「再表示」ở panel「一括友だち操作」→ xác nhận\n"
       "4. Kiểm tra màn hidden và danh sách chính",
       "5 friend đang ẩn, chọn toàn bộ",
       "- Cả 5 friend biến mất khỏi màn hidden, bảng trống\n"
       "- Cả 5 friend xuất hiện lại ở danh sách chính\n"
       "- Số「検索結果」ở danh sách chính tăng đúng 5\n"
       "- Màn hidden reload được sau thao tác, không treo",
       spec="Đã hỏi leader",
       note="Corpus không có TC bulk 再表示 — expected bám ui-spec.md (panel「一括友だち操作」) "
            "+ feature-spec.md EP-16 (type=1 → hàng loạt). Phần『reload được sau thao tác』đối "
            "chiếu Bug Tester #35742 (r140-r141) vốn xảy ra ở nút xoá hàng loạt. "
            "Cần Leader xác nhận."),

    # ═══════════ 12. Màn ブロックされた友だち ═══════════
    tc("Màn ブロックされた友だち", "UI-001", "Normal",
       "Màn ブロックされた友だち chỉ có hành động 削除, KHÔNG có 再表示 hay ブロック解除",
       UBLK,
       "1. Mở /basic/friendlist/user-block\n"
       "2. Đọc dòng tiêu đề bảng và các nút trên từng dòng\n"
       "3. Đọc heading và các nút của panel dưới bảng",
       "Không nhập gì — chỉ quan sát",
       "- Bảng có 5 cột:「全選択」·「ブロックされた日時」·「LINE登録名」·「システム表示名」·"
       "「エルメ上から削除」\n"
       "- Trên từng dòng CHỈ có nút「削除」\n"
       "- KHÔNG có nút「再表示」và KHÔNG có nút「ブロック解除」\n"
       "- Panel dưới bảng có heading「一括友だち削除」với đúng 1 nút「削除」",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md (SCR-FRL-05) + feature-spec.md BR-01 "
            "(blocked_by=0 → user tự block, Admin chỉ xoá được, không unblock được). "
            "Cần Leader xác nhận."),

    tc("Màn ブロックされた友だち", "LIST-001", "Boundary",
       "Màn ブロックされた友だち phân trang 50 friend/trang",
       "- Đăng nhập Admin của bot có ≥ 51 friend bị user block",
       "1. Mở /basic/friendlist/user-block\n"
       "2. Mở rộng khoảng「表示期間」để bao trọn mọi ngày\n"
       "3. Đếm số dòng trang 1 và kiểm tra có nút sang trang 2 không\n"
       "4. Sang trang 2, đếm số dòng và đối chiếu không trùng friend với trang 1",
       "≥ 51 friend bị user block",
       "- Trang 1 hiển thị đúng 50 dòng\n"
       "- Có nút sang trang 2\n"
       "- Trang 2 hiển thị các friend còn lại, KHÔNG lặp friend của trang 1",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám logic-spec.md:608 (danh sách user block: 50 "
            "items/page). Cần Leader xác nhận."),

    tc("Màn ブロックされた友だち", "LIST-001", "Normal",
       "Chỉ friend do USER block xuất hiện — không lẫn friend do admin block",
       UBLK + "\n- Chuẩn bị thêm 2 friend bị ADMIN block",
       "1. Ghi lại tên 2 friend bị admin block\n"
       "2. Mở /basic/friendlist/user-block, mở rộng khoảng ngày\n"
       "3. Rà toàn bộ danh sách tìm 2 tên đó\n"
       "4. Mở /basic/friendlist/block, xác nhận 2 friend đó nằm ở đây",
       "3 friend user-block + 2 friend admin-block",
       "- Màn「ブロックされた友だち」chỉ hiện 3 friend do user block\n"
       "- 2 friend do admin block KHÔNG xuất hiện ở màn này\n"
       "- 2 friend đó nằm đúng ở màn「ブロックした友だち」",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md BR-01 (blocked_by=0 vs "
            "blocked_by=1) + §2 (filter của 2 màn). Cần Leader xác nhận."),

    # ═══════════ 13. Màn ブロックした友だち ═══════════
    tc("Màn ブロックした友だち", "UI-001", "Normal",
       "Màn ブロックした友だち có đủ 2 hành động ブロック解除 và 削除",
       ABLK,
       "1. Mở /basic/friendlist/block\n"
       "2. Đọc dòng tiêu đề bảng, các nút trên từng dòng và panel dưới bảng",
       "Không nhập gì — chỉ quan sát",
       "- Bảng có 6 cột:「全選択」·「ブロックした日時」·「LINE登録名」·「システム表示名」·"
       "「ブロック解除」·「エルメ上から削除」\n"
       "- Trên từng dòng có 2 nút:「ブロック解除」và「削除」\n"
       "- Panel dưới bảng có heading「一括友だち操作」với 2 nút「ブロック解除」và「削除」\n"
       "- Khi không có friend nào bị admin block trong khoảng lọc: bảng trống, không lỗi",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám ui-spec.md (SCR-FRL-06, dữ liệu mẫu là bảng "
            "trống). Cần Leader xác nhận."),

    tc("Màn ブロックした友だち", "INTG-LINE-001", "Normal",
       "ブロック解除 khi friend VẪN còn follow LINE OA — bỏ block thành công",
       ABLK + "\n- Chuẩn bị 1 friend bị admin block nhưng CHƯA hủy kết bạn từ phía LINE",
       "1. Ghi lại tên friend và số「検索結果」ở danh sách chính\n"
       "2. Ở màn block, click「ブロック解除」trên dòng friend đó\n"
       "3. Reload màn block và mở danh sách chính tìm friend đó\n"
       "4. Mở màn chat 1:1 của friend đó kiểm tra message hệ thống\n"
       "5. Đọc lại số 未確認 của bot",
       "1 friend bị admin block, vẫn đang follow LINE OA",
       "- Friend biến mất khỏi màn「ブロックした友だち」\n"
       "- Friend xuất hiện lại ở danh sách chính, số「検索結果」tăng 1\n"
       "- Màn chat 1:1 xuất hiện message hệ thống về việc bỏ block\n"
       "- Số 未確認 của bot và badge trên menu được cập nhật lại",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md §2 (luồng bỏ block: gọi LINE API "
            "getProfile, tạo message unblock, cập nhật count_user_unconfirm + updateBadge) + "
            "BR-02. Cần Leader xác nhận."),

    tc("Màn ブロックした友だち", "INTG-LINE-001", "Abnormal",
       "ブロック解除 khi friend ĐÃ hủy kết bạn từ phía LINE — giữ nguyên trạng thái block",
       ABLK + "\n- Chuẩn bị 1 friend bị admin block VÀ đã tự hủy kết bạn / block bot từ app LINE",
       "1. Ghi lại tên friend đó\n"
       "2. Ở màn block, click「ブロック解除」trên dòng friend đó\n"
       "3. Reload màn block, tìm friend đó\n"
       "4. Mở danh sách chính, tìm friend đó",
       "1 friend bị admin block VÀ đã block bot từ phía LINE",
       "- Friend VẪN nằm ở màn「ブロックした友だち」— không bị gỡ block\n"
       "- Friend KHÔNG xuất hiện ở danh sách chính\n"
       "- Hệ thống không lỗi 500; nếu có thông báo cho Admin thì ghi lại nguyên văn",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md BR-02 (bỏ block chỉ thành công "
            "nếu user vẫn follow, kiểm qua LINE API getProfile) + §2 bước 3. Spec KHÔNG ghi hệ "
            "thống báo gì cho Admin trong trường hợp này → cần Leader chốt."),

    tc("Màn ブロックした友だち", "STATE-DEP-001", "Normal",
       "Block friend làm dừng toàn bộ scenario và huỷ các step chưa gửi",
       "- Đăng nhập Admin\n"
       "- Chuẩn bị 1 friend đang chạy scenario S1, còn ít nhất 2 step CHƯA đến giờ gửi\n"
       "- Ghi lại danh sách step chưa gửi và thời điểm dự kiến",
       "1. Ở màn friendlist, tích friend đó → chạy action block friend\n"
       "2. Mở màn「ブロックした友だち」xác nhận friend có ở đó\n"
       "3. Chờ qua thời điểm dự kiến gửi của các step còn lại\n"
       "4. Mở app LINE của friend kiểm tra có nhận message step nào không\n"
       "5. Bỏ block friend, kiểm tra trạng thái scenario của friend",
       "1 friend đang chạy scenario với ≥ 2 step chưa gửi",
       "- Friend chuyển sang màn「ブロックした友だち」\n"
       "- Trạng thái scenario của friend chuyển sang dừng\n"
       "- Friend KHÔNG nhận thêm message step nào sau thời điểm block\n"
       "- Sau khi bỏ block, scenario KHÔNG tự chạy tiếp (các step đã bị huỷ)",
       spec="Đã hỏi leader",
       note="Corpus không có TC — expected bám feature-spec.md BR-08 (block → mọi scenario "
            "is_following=0, xoá scenario_step_time status=0). Cần Leader xác nhận hành vi sau "
            "khi bỏ block."),

    tc("Màn ブロックした友だち", "BULK-001", "Normal",
       "Bulk ブロック解除 — bỏ block hàng loạt friend đã chọn",
       ABLK + "\n- Bot có ≥ 5 friend bị admin block, tất cả vẫn còn follow LINE OA",
       "1. Ghi lại tên 5 friend và số「検索結果」ở danh sách chính\n"
       "2. Ở màn block, tích「全選択」→ click「ブロック解除」ở panel → xác nhận\n"
       "3. Reload màn block và mở danh sách chính",
       "5 friend bị admin block, đều còn follow",
       "- Cả 5 friend biến mất khỏi màn block\n"
       "- Cả 5 friend xuất hiện lại ở danh sách chính, số「検索結果」tăng đúng 5\n"
       "- Màn block reload được sau thao tác, không treo",
       spec="Đã hỏi leader",
       note="Corpus không có TC bulk unblock — expected bám ui-spec.md (panel「一括友だち操作」"
            "có nút「ブロック解除」). Cần Leader xác nhận."),

    # ═══════════ 14. Xoá bạn bè & cascade ═══════════
    tc("Xoá bạn bè & cascade", "DATA-REF-001", "Normal",
       "Xoá hàng loạt ở màn 非表示中の友だち — dữ liệu liên quan bị xoá theo",
       RICH + "\n- Đưa friend đó vào trạng thái ẩn (非表示)",
       "1. Mở /basic/friendlist/hidden\n"
       "2. Tích「全選択」→ click「削除」ở panel → xác nhận\n"
       "3. Chờ thao tác hoàn tất, ghi lại thời gian chờ\n"
       "4. Kiểm tra màn hidden sau khi xoá\n"
       "5. Mở lần lượt: màn URL分析 (url rút gọn của friend), màn kết quả trả lời form, "
       "màn danh sách đặt event — tìm dữ liệu của friend vừa xoá",
       "1 friend đầy đủ dữ liệu, đang bị ẩn",
       "- Friend biến mất khỏi màn hidden\n"
       "- Màn hidden RELOAD được ngay sau khi xoá, không đứng màn\n"
       "- Bản ghi url rút gọn và lượt click của friend không còn được tính\n"
       "- Kết quả trả lời form của friend không còn hiển thị\n"
       "- Lượt đặt event của friend không còn hiển thị",
       env="PRODUCTION",
       note="Nguồn: r145 (『màn hidden → xoá friend hàng loạt → check data sau khi đã xóa』, "
            "kết quả OK step + AI test Pass) + r141 (Bug Tester #35742: nhấn xoá nhiều friend "
            "xong không reload được màn hình). RULE-08: khối lượng lớn + xoá cascade → "
            "PRODUCTION."),

    tc("Xoá bạn bè & cascade", "DATA-REF-001", "Normal",
       "Xoá hàng loạt ở màn ブロックされた友だち và ブロックした友だち",
       RICH + "\n- Chuẩn bị 2 friend đầy đủ dữ liệu: 1 bị user block, 1 bị admin block",
       "1. Mở /basic/friendlist/user-block → tích「全選択」→「削除」→ xác nhận\n"
       "2. Kiểm tra màn reload được và friend đã biến mất\n"
       "3. Mở /basic/friendlist/block → tích「全選択」→「削除」→ xác nhận\n"
       "4. Kiểm tra tương tự\n"
       "5. Với cả 2 friend: kiểm tra url rút gọn, kết quả form, lượt đặt event không còn",
       "2 friend đầy đủ dữ liệu ở 2 màn block khác nhau",
       "- Cả 2 màn đều xoá được hàng loạt và RELOAD được ngay sau đó\n"
       "- 2 friend biến mất khỏi màn tương ứng\n"
       "- Dữ liệu url rút gọn / form / event của cả 2 friend không còn được tính hay hiển thị",
       env="PRODUCTION",
       note="Nguồn: r148, r151."),

    tc("Xoá bạn bè & cascade", "DATA-REF-001", "Normal",
       "Tích chọn toàn bộ rồi chỉ xoá 1 friend — chỉ friend đó bị xoá",
       RICH + "\n- Màn đang có ≥ 5 friend",
       "1. Ở màn hidden (hoặc user-block / block), tích「全選択」\n"
       "2. Click nút「削除」trên DÒNG của 1 friend cụ thể → xác nhận\n"
       "3. Đếm số dòng còn lại trên màn\n"
       "4. Kiểm tra dữ liệu (url rút gọn, form, event) của 4 friend còn lại vẫn nguyên",
       "5 friend, tích toàn bộ nhưng chỉ xoá 1",
       "- Chỉ friend được click nút xoá bị xoá\n"
       "- 4 friend còn lại VẪN nằm trên màn\n"
       "- Dữ liệu của 4 friend còn lại KHÔNG bị xoá theo",
       env="PRODUCTION",
       note="Nguồn: r147, r150, r153 (lặp lại ở cả 3 màn, cùng 1 kết quả mong đợi → gộp 1 TC)."),

    tc("Xoá bạn bè & cascade", "DATA-REF-001", "Normal",
       "Xoá friend từ màn chi tiết bạn bè — dữ liệu liên quan cũng bị xoá",
       RICH,
       "1. Mở màn chi tiết của friend đã chuẩn bị\n"
       "2. Click nút「削除」→ xác nhận trên hộp thoại\n"
       "3. Quan sát điều hướng sau khi xoá\n"
       "4. Tìm friend đó ở danh sách chính\n"
       "5. Kiểm tra url rút gọn, kết quả form, lượt đặt event của friend",
       "1 friend đầy đủ dữ liệu",
       "- Có hộp thoại xác nhận trước khi xoá\n"
       "- Sau khi xác nhận, friend biến mất khỏi danh sách chính\n"
       "- Dữ liệu url rút gọn / form / event của friend không còn hiển thị hay được tính",
       env="PRODUCTION",
       note="Nguồn: r154 (『Xóa friend ở my page』). Chi tiết màn 友だち情報詳細 tách khỏi phạm vi "
            "FA-013 — ở đây chỉ giữ hệ quả xoá nhìn từ FA-013."),

    tc("Xoá bạn bè & cascade", "SYNC-APP-001", "Normal",
       "Xoá friend từ APP MOBILE — hệ quả giống xoá từ web",
       RICH + "\n- Đã cài app mobile quản lý bot và đăng nhập cùng tài khoản",
       "1. Trên app mobile, mở danh sách bạn bè, tìm friend đã chuẩn bị\n"
       "2. Thực hiện xoá friend từ app\n"
       "3. Trên web, mở /basic/friendlist tìm friend đó\n"
       "4. Kiểm tra url rút gọn, kết quả form, lượt đặt event của friend",
       "1 friend đầy đủ dữ liệu, xoá từ app mobile",
       "- Friend biến mất khỏi danh sách chính trên web\n"
       "- Dữ liệu url rút gọn / form / event của friend không còn hiển thị hay được tính\n"
       "- Kết quả giống hệt khi xoá từ web",
       env="PRODUCTION",
       note="Nguồn: r168. RULE-06: kiểm tới output cuối trên cả 2 kênh web và app mobile."),

    tc("Xoá bạn bè & cascade", "DATA-REF-001", "Normal",
       "⭐ Sau khi xoá, friend KẾT BẠN LẠI — dữ liệu cũ không hồi sinh",
       RICH + "\n- Friend đã bị xoá bằng 1 trong các cách ở TC trên",
       "1. Từ app LINE, cho friend kết bạn lại với bot\n"
       "2. Mở màn chi tiết của friend vừa kết bạn lại\n"
       "3. Rà lần lượt các mục: lịch sử kết bạn · lịch sử thay đổi 友だち情報 · メモ · タグ "
       "và lịch sử gắn tag · サロン・面談予約 · レッスン予約 · イベント予約 · 単品商品 · "
       "継続商品 · フォーム回答 · QRコードアクション · リッチメニュー · lịch sử scenario\n"
       "4. Cho friend click lại url rút gọn cũ, trả lời form, đặt event mới",
       "1 friend đã xoá rồi kết bạn lại",
       "- TẤT CẢ 13 mục lịch sử đều TRỐNG, không hiển thị dữ liệu trước khi xoá\n"
       "- Click url rút gọn: lượt click được đếm mới bình thường\n"
       "- Trả lời form: ghi nhận được kết quả mới\n"
       "- Đặt event: đặt được bình thường",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r146, r149, r152, r155-r167 và r169-r182 (2 khối lặp cho web và app "
            "mobile, mỗi khối 13 mục — gộp thành 1 TC vì cùng 1 quy tắc『dữ liệu cũ không hồi "
            "sinh』, liệt kê đủ 13 mục ở cột Kết quả mong đợi). ⚠ Cột「Result AI test 2026-07-09」"
            "ghi『Không test — phụ thuộc LINE re-follow + UI đầy đủ』ở các dòng kết-bạn-lại → "
            "phần này CHƯA có bằng chứng chạy thật, cần chạy tay."),

    tc("Xoá bạn bè & cascade", "PERF-LARGE-001", "Normal",
       "Xoá friend có RẤT NHIỀU dữ liệu không bị treo màn (Bug #38390)",
       "- Đăng nhập Admin\n"
       "- Chuẩn bị 1 friend có lượng dữ liệu lớn: nhiều bản ghi url rút gọn và lượt click, "
       "nhiều kết quả form, nhiều lượt đặt lịch\n"
       "- Ghi lại số lượng bản ghi từng loại",
       "1. Mở màn chi tiết của friend đó\n"
       "2. Click「削除」→ xác nhận\n"
       "3. Bấm giờ từ lúc xác nhận tới lúc màn phản hồi xong\n"
       "4. Quan sát màn hình trong lúc chờ\n"
       "5. Sau khi xong, kiểm tra dữ liệu đã được xoá đủ",
       "1 friend có khối lượng dữ liệu lớn (đặc biệt nhiều bản ghi url rút gọn)",
       "- Màn KHÔNG bị treo ở trạng thái loading vô hạn\n"
       "- Thao tác xoá hoàn tất và màn phản hồi trong thời gian chấp nhận được "
       "(ghi lại con số thực tế để Leader chốt ngưỡng)\n"
       "- Dữ liệu của friend được xoá đầy đủ ở mọi mục",
       env="PRODUCTION",
       spec="Đã hỏi leader",
       note="Nguồn: r143, r144 (Bug tự detect #38390 — tái hiện:『Line user có nhiều data, có "
            "data ở bảng url_shorten_detail → xóa friend → bị chậm load mãi ở màn xóa』). "
            "TC gốc không nêu ngưỡng thời gian → cần Leader chốt. RULE-08: performance → "
            "PRODUCTION."),
]
