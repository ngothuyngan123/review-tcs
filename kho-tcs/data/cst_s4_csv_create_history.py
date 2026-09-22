# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 7-8: Tab 2「チャットのCSVエクスポート」.

S7 CSV export — tạo dữ liệu (SCR-02「データ作成」)
S8 CSV export — lịch sử tạo (SCR-03「作成履歴」)

✅ MT-01 đã chốt 2026-09-21: màn có 8 tab ⇒ tab CSV NẰM TRONG phạm vi FA-041.
⚠️ Nhưng spec-features/admin/chat-setting/ CHƯA quét 2 màn SCR-02/SCR-03 — mọi rule
BR-CSV-xx dưới đây lấy từ corpus [AI] 06-07/2026, chưa có bản spec chính thức để
đối chiếu. Việc quét bổ sung nằm ở cột "Việc phải làm tiếp" của MT-01.
"""
from _common import tc

T2 = ("- Đăng nhập Admin của LOA, đã chọn 1 bot\n"
      "- Đang ở `/basic/chat-setting` Tab 2「チャットのCSVエクスポート」sub-tab「データ作成」")
T2_FREE = T2.replace("đã chọn 1 bot", "bot đang chọn thuộc gói FREE")
T2_PAID = T2.replace("đã chọn 1 bot", "bot đang chọn thuộc gói TRẢ PHÍ (standard hoặc pro)")
T3 = ("- Đăng nhập Admin của LOA, đã chọn 1 bot\n"
      "- Đang ở Tab 2「チャットのCSVエクスポート」sub-tab「作成履歴」")
NOSPEC = "⚠️ Tab CSV trong phạm vi (MT-01 đã chốt 8 tab) nhưng spec CHƯA quét. "

S7 = [
    tc("CSV export — tạo dữ liệu", "UI-003", "Normal",
       "Trạng thái mặc định của form tạo CSV",
       T2 + "\n- Không có job CSV nào đang chạy",
       "1. Quan sát toàn bộ form tạo CSV",
       "—",
       "- Ô chọn ngày bắt đầu: placeholder「日付を選択」\n"
       "- Ô chọn ngày kết thúc: placeholder「日付を選択」\n"
       "- Khu vực điều kiện lọc: trạng thái trống「絞り込み条件が登録されていません」\n"
       "- Checkbox「全ての1:1チャット」: đã tích và bị khóa (không đổi được)\n"
       "- Checkbox「一斉配信を除く」: CHƯA tích\n"
       "- Checkbox「ステップ配信を除く」: ĐÃ tích",
       note=NOSPEC + "Nguồn: v2 r55 (TC-SC-022, Pass staging + production)"),

    tc("CSV export — tạo dữ liệu", "UI-003", "Normal",
       "Không còn icon lịch sử lọc và drawer「絞り込み履歴」",
       T2,
       "1. Quan sát khu vực điều kiện lọc",
       "—",
       "- KHÔNG hiển thị icon đồng hồ (🕐) hay nút「履歴を表示」\n"
       "- KHÔNG có drawer「絞り込み履歴」hay bất kỳ UI lịch sử lọc nào\n"
       "- Không có thao tác nào mở được lịch sử lọc",
       note=NOSPEC + "⚠️ Liên quan MT-22 — tính năng này bị KHÁCH BỎ khỏi thiết kế SCR-02 "
            "(quyết định 2026-07-23). Nguồn: v2 r56 (TC-SC-023, Pass staging + production)"),

    tc("CSV export — tạo dữ liệu", "FUNC-001", "Normal",
       "Chọn khoảng ngày hợp lệ → modal xác nhận → bắt đầu tạo CSV",
       T2_PAID + "\n- Không có job CSV nào đang chạy",
       "1. Chọn ngày bắt đầu (cách hôm nay khoảng 30 ngày)\n"
       "2. Chọn ngày kết thúc (cách hôm nay khoảng 20 ngày)\n"
       "3. Bấm「エクスポート条件の確認に進む」\n"
       "4. Đối chiếu khoảng ngày hiển thị trong modal「CSVデータの作成確認」\n"
       "5. Bấm「作業開始」",
       "date_from = today−30d, date_to = today−20d",
       "- Bước 3: modal「CSVデータの作成確認」hiện ra, hiển thị đúng khoảng ngày vừa chọn\n"
       "- Bước 5: modal đóng lại\n"
       "- Hiển thị loading kèm thanh tiến trình và spinner\n"
       "- Có link hủy trong vùng loading\n"
       "- Nút「エクスポート条件の確認に進む」không còn bấm được khi đang loading",
       note=NOSPEC + "Nguồn: v2 r47 (TC-SC-014, Fail staging / Pass production — Redmine #39052; "
            "fail do TC cũ hardcode ngày 2025 đã quá 180 ngày, đã đổi sang ngày động)"),

    tc("CSV export — tạo dữ liệu", "FUNC-001", "Normal",
       "Job tạo CSV chạy xong — tự chuyển sang sub-tab「作成履歴」",
       T2 + "\n- Đang ở trạng thái loading, job sắp xong (dùng bot có ít dữ liệu)",
       "1. Quan sát vùng loading ở sub-tab「データ作成」\n"
       "2. Chờ thanh tiến trình đạt 100%",
       "—",
       "- Khi job xong: trang TỰ chuyển sang sub-tab「作成履歴」\n"
       "- Dòng CSV vừa tạo xuất hiện trong bảng lịch sử với trạng thái hoàn thành và đủ nút thao tác",
       note=NOSPEC + "Nguồn: v2 r48 (TC-SC-015, Not Tested — cần chờ job async chạy xong thật)"),

    tc("CSV export — tạo dữ liệu", "FUNC-001", "Normal",
       "Hủy job CSV đang chạy — quay lại form trống",
       T2 + "\n- Đang có job CSV chạy dở (đang loading)",
       "1. Bấm link hủy trong vùng loading\n"
       "2. Quan sát modal「CSVデータの作成をキャンセル」\n"
       "3. Bấm「キャンセルする」",
       "—",
       "- Bước 2: modal hủy hiện ra với nội dung xác nhận\n"
       "- Bước 3: modal đóng, quay lại form tạo CSV TRỐNG (hết loading)\n"
       "- Nút「エクスポート条件の確認に進む」hiện lại bình thường",
       note=NOSPEC + "Nguồn: v2 r49 (TC-SC-016, Pass staging + production)"),

    tc("CSV export — tạo dữ liệu", "FUNC-001", "Normal",
       "Mở modal hủy rồi bấm「戻る」— job vẫn chạy tiếp",
       T2 + "\n- Đang có job CSV chạy dở (đang loading)",
       "1. Bấm link hủy trong vùng loading\n"
       "2. Modal「CSVデータの作成をキャンセル」hiện ra\n"
       "3. Bấm「戻る」",
       "—",
       "- Modal hủy đóng lại\n"
       "- Quay về vùng loading, thanh tiến trình TIẾP TỤC chạy\n"
       "- Job KHÔNG bị hủy",
       note=NOSPEC + "Nguồn: v2 r50 (TC-SC-017, Not Tested — cần bắt đúng lúc job đang processing)"),

    tc("CSV export — tạo dữ liệu", "CONC-001", "Abnormal",
       "Tạo CSV khi đã có 1 job đang chạy — báo giới hạn 1 job cùng lúc",
       T2 + "\n- Đang có job CSV ở trạng thái processing hoặc pending cho CHÍNH bot đang dùng",
       "1. Vào sub-tab「データ作成」\n"
       "2. Chọn khoảng ngày hợp lệ\n"
       "3. Bấm「エクスポート条件の確認に進む」\n"
       "4. Trong modal bấm「作業開始」",
       "date_from = today−30d, date_to = today−20d",
       "- Hiển thị cảnh báo「同時に作成できるCSVデータは1つまでです。」\n"
       "- KHÔNG tạo job CSV mới (bảng lịch sử không thêm dòng)",
       note=NOSPEC + "BR-CSV-01. Nguồn: v2 r51 (TC-SC-018, Not Tested — cần dựng 2 job đồng thời)"),

    tc("CSV export — tạo dữ liệu", "CONC-001", "Boundary",
       "Double-click「作業開始」trong modal xác nhận — chỉ tạo 1 job",
       T2 + "\n- Đang mở modal「CSVデータの作成確認」với khoảng ngày hợp lệ\n- Không có job nào đang chạy",
       "1. Double-click thật nhanh vào nút「作業開始」(2 lần trong < 1 giây)\n"
       "2. Sang sub-tab「作成履歴」và đếm số dòng vừa sinh",
       "—",
       "- Chỉ có đúng 1 job CSV được tạo (1 dòng trong lịch sử, 1 lần chuyển sang loading)\n"
       "- KHÔNG tạo 2 job trùng nhau\n"
       "- Không hiển thị lỗi 409 cho người dùng",
       note=NOSPEC + "Nguồn: v2 r92 (TC-SC-084, Blocked staging / Pass production) — CONC-001"),

    tc("CSV export — tạo dữ liệu", "FUNC-002", "Abnormal",
       "Bấm「エクスポート条件の確認に進む」khi chưa chọn khoảng ngày",
       T2 + "\n- Chưa chọn ngày bắt đầu và ngày kết thúc",
       "1. Không chọn ngày nào\n"
       "2. Bấm nút「エクスポート条件の確認に進む」",
       "(để trống cả 2 ngày)",
       "- Nút vẫn bấm được và có phản hồi\n"
       "- Hiển thị lỗi validation yêu cầu chọn khoảng ngày\n"
       "- KHÔNG mở modal「CSVデータの作成確認」",
       spec="Đã hỏi leader",
       note=NOSPEC + "⏳ QA-004 chưa chốt: nút bị disable (phương án A) hay enabled + báo lỗi "
            "(phương án B). TC viết theo phương án B. Nguồn: v2 r93 (TC-SC-085, Pass) + "
            "v2 r97 (TC-SC-122, Not Tested)"),

    tc("CSV export — tạo dữ liệu", "FUNC-DATE-001", "Boundary",
       "Ngày bắt đầu = ngày kết thúc (khoảng 1 ngày) — vẫn tạo được",
       T2,
       "1. Chọn ngày bắt đầu là hôm nay\n"
       "2. Chọn ngày kết thúc cũng là hôm nay\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = date_to = hôm nay",
       "- Modal xác nhận hiện ra bình thường với khoảng「<hôm nay> から <hôm nay> まで」\n"
       "- Không báo lỗi, tiếp tục tạo CSV được",
       note=NOSPEC + "Nguồn: v2 r94 (TC-SC-086, Pass staging + production) — DI-10 boundary"),

    tc("CSV export — tạo dữ liệu", "FUNC-DATE-001", "Abnormal",
       "Ngày kết thúc trước ngày bắt đầu — không được tạo CSV im lặng",
       T2,
       "1. Chọn ngày bắt đầu là hôm nay\n"
       "2. Chọn ngày kết thúc là 3 tuần trước\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = hôm nay, date_to = today−21d",
       "- Hệ thống chặn: báo lỗi validation HOẶC tự điều chỉnh lại khoảng ngày\n"
       "- TUYỆT ĐỐI không tạo job CSV với khoảng ngày đảo ngược mà không báo gì",
       spec="Đã hỏi leader",
       note=NOSPEC + "⏳ QA-033 chưa chốt hành vi cụ thể. Nguồn: v2 r95 (TC-SC-087, Pass staging + "
            "production)"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Abnormal",
       "Gói Free — khoảng ngày vượt 180 ngày thì bị chặn",
       T2_FREE,
       "1. Chọn ngày bắt đầu cách hôm nay 240 ngày\n"
       "2. Chọn ngày kết thúc là hôm nay (khoảng > 180 ngày)\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−240d, date_to = today",
       "- Hiển thị lỗi「エクスポート対象期間は180日以内で指定してください。」\n"
       "- KHÔNG mở modal xác nhận, không tạo được CSV",
       note=NOSPEC + "BR-CSV-02. Nguồn: v2 r52 (TC-SC-019, Pass staging + production)"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Boundary",
       "Gói Free — khoảng đúng 180 ngày tính lùi từ hôm nay thì phải cho qua",
       T2_FREE,
       "1. Chọn ngày bắt đầu cách hôm nay đúng 180 ngày\n"
       "2. Chọn ngày kết thúc là hôm nay\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−180d, date_to = today",
       "- Modal「CSVデータの作成確認」hiện ra bình thường\n"
       "- KHÔNG có lỗi liên quan giới hạn gói\n"
       "- Tiếp tục tạo CSV được",
       note=NOSPEC + "⚠️ Phụ thuộc MT-06 — DỰ KIẾN FAIL: BUG-023 (Open, Low) xác nhận app chặn ở "
            "179 ngày, đúng 180 ngày bị chặn nhầm lỗi「180日以内で指定」. Nguồn: v2 r53 (TC-SC-020, "
            "Fail staging / Pass production — kết quả 2 môi trường KHÁC NHAU)"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Abnormal",
       "Gói Free — khoảng đúng 180 ngày nhưng KHÔNG kết thúc ở hôm nay thì vẫn bị chặn",
       T2_FREE,
       "1. Chọn ngày bắt đầu cách hôm nay 240 ngày\n"
       "2. Chọn ngày kết thúc cách hôm nay 60 ngày (độ dài khoảng vẫn đúng 180 ngày)\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−240d, date_to = today−60d",
       "- Hiển thị lỗi「エクスポート対象期間は180日以内で指定してください。」\n"
       "- Modal「CSVデータの作成確認」KHÔNG hiện ra",
       note=NOSPEC + "⚠️ Làm rõ BR-CSV-02: giới hạn 180 ngày tính LÙI TỪ HÔM NAY, không phải độ dài "
            "khoảng. Nguồn: v2 r99 (TC-SC-158, nguồn v1 BS_008, Not Tested)"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Normal",
       "Gói Free — khoảng < 180 ngày và kết thúc TRƯỚC hôm nay thì cho qua",
       T2_FREE,
       "1. Chọn ngày bắt đầu cách hôm nay 90 ngày\n"
       "2. Chọn ngày kết thúc cách hôm nay 30 ngày\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−90d, date_to = today−30d",
       "- Modal「CSVデータの作成確認」hiện ra bình thường\n"
       "- Không lỗi giới hạn gói, tạo CSV được",
       note=NOSPEC + "Nguồn: v2 r100 (TC-SC-159, nguồn v1 BS_009, Not Tested)"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Normal",
       "Gói Free — khoảng < 180 ngày và kết thúc đúng hôm nay thì cho qua",
       T2_FREE,
       "1. Chọn ngày bắt đầu cách hôm nay 120 ngày\n"
       "2. Chọn ngày kết thúc là hôm nay\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−120d, date_to = today",
       "- Modal「CSVデータの作成確認」hiện ra bình thường\n"
       "- Không lỗi giới hạn gói, tạo CSV được",
       note=NOSPEC + "Nguồn: v2 r101 (TC-SC-160, nguồn v1 BS_010, Not Tested). ⚠️ v1 ghi ngày mẫu "
            "`2026-02-33` (ngày không tồn tại) → đã chuẩn hóa sang ngày tương đối"),

    tc("CSV export — tạo dữ liệu", "PAY-LIMIT-001", "Normal",
       "Gói TRẢ PHÍ — khoảng ngày vượt 180 ngày vẫn phải tạo được",
       T2_PAID,
       "1. Chọn ngày bắt đầu cách hôm nay 1 năm\n"
       "2. Chọn ngày kết thúc là hôm nay\n"
       "3. Bấm「エクスポート条件の確認に進む」",
       "date_from = today−365d, date_to = today",
       "- Modal「CSVデータの作成確認」hiện ra bình thường, KHÔNG báo lỗi giới hạn gói\n"
       "- Tiếp tục tạo CSV được",
       note=NOSPEC + "⚠️ Phụ thuộc MT-06 — DỰ KIẾN FAIL: BUG-024 (Open, HIGH) xác nhận bot gói TRẢ "
            "PHÍ vẫn bị chặn「180日以内」như gói Free. Nguồn: v2 r54 (TC-SC-021, Fail staging / "
            "Skipped production; user đã xác nhận trực tiếp bot 562 đúng là paid plan)"),

    tc("CSV export — tạo dữ liệu", "DATA-COUNT-001", "Normal",
       "対象人数 cập nhật đúng sau khi lưu điều kiện lọc",
       T2 + "\n- Biết trước số friend khớp 1 điều kiện lọc cụ thể (VD 3 friend có tag「テスト」)",
       "1. Ghi lại giá trị「対象人数」ban đầu (chưa có filter)\n"
       "2. Bấm「絞り込み条件 登録・編集」, đặt điều kiện lọc theo tag「テスト」, bấm lưu\n"
       "3. Quan sát lại giá trị「対象人数」",
       "Filter: tag = テスト (biết trước = 3 friend)",
       "-「対象人数」cập nhật đúng bằng số friend thực tế khớp điều kiện lọc (3人)\n"
       "- Khớp với số đếm tay ở màn danh sách bạn bè\n"
       "- KHÔNG cập nhật realtime khi đang chỉnh filter — chỉ cập nhật sau khi bấm lưu (BR-CSV-06)",
       note=NOSPEC + "⚠️ Phụ thuộc MT-23 — DỰ KIẾN FAIL: v2 r96 (TC-SC-088) Blocked staging và "
            "**Fail production**"),

    tc("CSV export — tạo dữ liệu", "UI-003", "Normal",
       "Thời gian dự kiến tạo CSV thay đổi theo lượng dữ liệu",
       T2,
       "1. Chọn khoảng ngày nhỏ (1 ngày), quan sát thời gian dự kiến\n"
       "2. Chọn khoảng ngày lớn hơn hoặc thêm điều kiện lọc để tăng lượng dữ liệu\n"
       "3. Quan sát lại thời gian dự kiến",
       "1 ngày → 90 ngày",
       "- Thời gian dự kiến KHÔNG cố định mà thay đổi theo lượng dữ liệu được chọn\n"
       "- Khoảng rộng hơn cho thời gian dự kiến lớn hơn, không hiển thị cùng một giá trị cứng",
       note=NOSPEC + "Nguồn: v2 r98 (TC-SC-123, nguồn v1, Not Tested)"),

    tc("CSV export — tạo dữ liệu", "FUNC-SEQ-001", "Normal",
       "Đóng modal xác nhận bằng nút X — giữ nguyên ngày và filter đã chọn",
       T2 + "\n- Đang hiển thị modal「CSVデータの作成確認」sau khi đã chọn ngày và điều kiện lọc",
       "1. Bấm nút X trên modal「CSVデータの作成確認」\n"
       "2. Quan sát form ở sub-tab「データ作成」",
       "—",
       "- Modal đóng lại, quay về sub-tab「データ作成」\n"
       "- Khoảng ngày và điều kiện lọc đã chọn được GIỮ NGUYÊN, không bị xóa",
       note=NOSPEC + "Nguồn: v2 r102 (TC-SC-161, nguồn v1 BS_011, đã Pass)"),

    tc("CSV export — tạo dữ liệu", "FUNC-SEQ-001", "Normal",
       "Reload trang khi đã chọn ngày và filter — dữ liệu bị xóa hết",
       T2 + "\n- Đã chọn khoảng ngày và điều kiện lọc, chưa bấm tạo",
       "1. Nhấn F5 reload trang\n"
       "2. Quay lại Tab 2 sub-tab「データ作成」",
       "—",
       "- Khoảng ngày và điều kiện lọc bị XÓA HẾT, form về trạng thái mặc định\n"
       "- Không giữ lại dữ liệu đang nhập dở",
       note=NOSPEC + "Nguồn: v2 r103 (TC-SC-162, nguồn v1 BS_012, đã Pass). Đối chiếu TC đóng modal "
            "bằng X: đóng modal thì GIỮ, reload thì XÓA"),

    tc("CSV export — tạo dữ liệu", "REG-SHARED-001", "Normal",
       "Lọc theo シナリオ ở CSV export — 対象人数 và nội dung file khớp đúng tập friend",
       T2 + "\n- Có ≥ 1 scenario với tập friend đã biết trước (đếm sẵn ở màn danh sách bạn bè)",
       "1. Bấm「絞り込み条件 登録・編集」→ modal lọc dùng chung mở ra\n"
       "2. Chọn điều kiện scenario đã chuẩn bị → bấm「保存」\n"
       "3. Đọc「対象人数」\n"
       "4. Tạo CSV → tải file → đếm số friend trong file",
       "Filter: scenario đã chuẩn bị",
       "-「対象人数」khớp số friend thực tế của scenario đã chọn\n"
       "- File CSV chứa đúng tập friend đó, không thừa không thiếu",
       note=NOSPEC + "Modal lọc là component DÙNG CHUNG (BR-CSV-05) — sửa ở FilterMobileController "
            "có thể làm nhánh scenario trả sai tập. Nguồn: v2 r191 (TC-SC-191, Not Tested)"),

    tc("CSV export — tạo dữ liệu", "LIST-001", "Boundary",
       "Kết hợp scenario + tag — 対象人数 là tập GIAO, không phải tập hợp",
       T2 + "\n- Đã biết trước tập giao của 1 scenario và 1 tag",
       "1. Mở modal lọc → chọn điều kiện scenario VÀ điều kiện tag\n"
       "2. Bấm「保存」→ đọc「対象人数」\n"
       "3. Tạo CSV → tải file → đối chiếu danh sách friend",
       "Filter: scenario AND tag",
       "-「対象人数」bằng đúng tập GIAO của 2 điều kiện (KHÔNG phải tập hợp)\n"
       "- File CSV khớp đúng danh sách đó\n"
       "- Không bản ghi nào bị thiếu hoặc lọt thêm",
       note=NOSPEC + "Nguồn: v2 r192 (TC-SC-192, Not Tested)"),
]

S8 = [
    tc("CSV export — lịch sử tạo", "UI-003", "Normal",
       "Dòng đang「作成中」— chỉ có text và % tiến trình, không có nút thao tác",
       T3 + "\n- Có job CSV đang processing",
       "1. Quan sát dòng có trạng thái「作成中」trong bảng lịch sử",
       "—",
       "- Dòng chỉ hiển thị text「作成中」và % tiến trình\n"
       "- KHÔNG có icon preview (▶)\n"
       "- KHÔNG có icon xóa (🗑)\n"
       "- KHÔNG có nút「ダウンロード」",
       note=NOSPEC + "BR-CSV-04. Nguồn: v2 r61 (TC-SC-029, Skipped cả 2 môi trường — cần bắt đúng "
            "lúc job đang chạy, timing-sensitive)"),

    tc("CSV export — lịch sử tạo", "UI-FIELD-001", "Normal",
       "Dòng đang「作成中」— bấm vào không mở được gì",
       T3 + "\n- Có job CSV đang processing, tiến trình chưa đạt 100%",
       "1. Bấm vào dòng có trạng thái「作成中」",
       "—",
       "- Dòng「作成中」KHÔNG bấm được, không mở preview, không tải file\n"
       "- Không có nút thao tác nào khả dụng trên dòng này",
       note=NOSPEC + "Nguồn: v2 r105 (TC-SC-164, nguồn v1 BS_014, đã Pass)"),

    tc("CSV export — lịch sử tạo", "UI-003", "Normal",
       "Dòng đã hoàn thành — hiển thị đủ 3 nút thao tác",
       T3 + "\n- Có ít nhất 1 bản ghi CSV trạng thái hoàn thành",
       "1. Quan sát dòng có trạng thái hoàn thành trong bảng",
       "—",
       "- Dòng hiển thị đủ 3 nút: icon preview (▶) · icon xóa (🗑) · nút「ダウンロード」(nền xanh lá)",
       note=NOSPEC + "Nguồn: v2 r62 (TC-SC-030, Pass staging / Skipped production)"),

    tc("CSV export — lịch sử tạo", "UI-003", "Normal",
       "% tiến trình tự cập nhật, không cần F5",
       T3 + "\n- Có dòng「作成中」đang chạy",
       "1. Quan sát dòng「作成中」khoảng 30 giây, KHÔNG reload trang và không bấm nút nào",
       "—",
       "- Giá trị % tự tăng dần mà không cần F5\n"
       "- Khi job xong: dòng tự đổi sang trạng thái hoàn thành kèm đủ 3 nút thao tác",
       note=NOSPEC + "BR-CSV-08 (web poll API lấy %). Nguồn: v2 r63 (TC-SC-031, Not Tested)"),

    tc("CSV export — lịch sử tạo", "FUNC-SEQ-001", "Normal",
       "Job chưa đạt 100% mà chuyển sang tab「作成履歴」— vẫn thấy dòng「作成中」",
       "- Đăng nhập Admin, đang ở Tab 2 sub-tab「データ作成」\n"
       "- Đang hiển thị「CSVデータを作成中です。」, tiến trình chưa đạt 100%",
       "1. Bấm sang sub-tab「作成履歴」",
       "—",
       "- Chuyển sang sub-tab「作成履歴」thành công\n"
       "- Trong bảng có bản ghi tương ứng với trạng thái「作成中」",
       note=NOSPEC + "Nguồn: v2 r104 (TC-SC-163, nguồn v1 BS_013, đã Pass)"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Normal",
       "Tải file CSV — tên file và encoding đúng",
       T3 + "\n- Có ít nhất 1 bản ghi CSV trạng thái hoàn thành",
       "1. Bấm nút「ダウンロード」của dòng đã hoàn thành\n"
       "2. Quan sát tên file tải về\n"
       "3. Mở file bằng Excel bản tiếng Nhật",
       "—",
       "- File bắt đầu tải về trình duyệt\n"
       "- Tên file đúng dạng `{friendId}_{startYYYYMMDD}_{endYYYYMMDD}_{tên friend}.csv`\n"
       "- Mở bằng Excel JP: tiếng Nhật hiển thị đúng, không lỗi ký tự (UTF-8 with BOM)",
       env="PRODUCTION",
       note=NOSPEC + "⚠️ Phụ thuộc MT-20 — QA-030/031 đã chốt UTF-8 with BOM + tên file per-friend, "
            "thay cho giả định SHIFT-JIS cũ. Nguồn: v2 r57 (TC-SC-025, Not Tested). "
            "Môi trường PRODUCTION theo RULE-08 (tải file thật)"),

    tc("CSV export — lịch sử tạo", "FUNC-001", "Normal",
       "Preview CSV — modal chỉ hiển thị điều kiện xuất, không hiển thị nội dung file",
       T3 + "\n- Có ít nhất 1 bản ghi CSV trạng thái hoàn thành",
       "1. Bấm icon preview (▶) của dòng đã hoàn thành\n"
       "2. Quan sát nội dung modal",
       "—",
       "- Modal「CSVエクスポート条件」hiện ra\n"
       "- Hiển thị 期間 (khoảng thời gian xuất) và 対象 (điều kiện lọc đã dùng khi tạo)\n"
       "- KHÔNG hiển thị nội dung dữ liệu bên trong file CSV\n"
       "- Chỉ có nút「閉じる」",
       note=NOSPEC + "QA-011 đã chốt: metadata only. Nguồn: v2 r58 (TC-SC-026, Pass staging / "
            "Skipped production)"),

    tc("CSV export — lịch sử tạo", "FUNC-001", "Normal",
       "Xóa bản ghi CSV — xác nhận trong popover thì xóa",
       T3 + "\n- Có ít nhất 1 bản ghi CSV trạng thái hoàn thành",
       "1. Bấm icon xóa (🗑) của dòng đã hoàn thành\n"
       "2. Quan sát popover xác nhận\n"
       "3. Bấm「削除する」",
       "—",
       "- Toast thông báo thành công\n"
       "- Dòng bị xóa khỏi bảng lịch sử\n"
       "- Popover xóa CSV KHÔNG có checkbox「次から表示しない」(khác modal xóa trạng thái ở Tab 1)",
       note=NOSPEC + "BR-CSV-11. Nguồn: v2 r59 (TC-SC-027, Pass staging / Skipped production)"),

    tc("CSV export — lịch sử tạo", "FUNC-001", "Abnormal",
       "Xóa bản ghi CSV — bấm「閉じる」thì không xóa",
       T3 + "\n- Có ít nhất 1 bản ghi CSV bất kỳ",
       "1. Bấm icon xóa (🗑) của 1 dòng bất kỳ\n"
       "2. Popover xác nhận hiện ra\n"
       "3. Bấm「閉じる」",
       "—",
       "- Popover đóng lại\n"
       "- Dòng vẫn còn trong bảng lịch sử, không bị xóa\n"
       "- Không có thay đổi nào trong danh sách",
       note=NOSPEC + "Nguồn: v2 r60 (TC-SC-028, Pass staging / Skipped production)"),

    tc("CSV export — lịch sử tạo", "LIST-001", "Boundary",
       "Lịch sử chỉ giữ tối đa 100 file — file thứ 101 đẩy file cũ nhất ra",
       T3 + "\n- Đã có 100 bản ghi CSV trong lịch sử",
       "1. Ghi lại bản ghi CŨ NHẤT trong danh sách\n"
       "2. Tạo thêm 1 file CSV mới (bản ghi thứ 101)\n"
       "3. Quan sát lại danh sách「作成履歴」",
       "100 bản ghi sẵn có + 1 bản ghi mới",
       "- Danh sách chỉ hiển thị tối đa 100 file gần nhất\n"
       "- Bản ghi cũ nhất ghi ở bước 1 đã bị loại khỏi danh sách",
       note=NOSPEC + "Nguồn: v2 r64 (TC-SC-024, Not Tested). ⚠️ Nội dung TC-SC-024 đã bị THAY: bản "
            "trước test「確認」trong drawer「絞り込み履歴」— tính năng khách đã bỏ (MT-22)"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Normal",
       "Export khi CÓ dữ liệu thỏa điều kiện — file chứa đúng tập đã lọc",
       ("- Đăng nhập Admin, Tab 2「チャットのCSVエクスポート」\n"
        "- Đã chọn khoảng ngày + điều kiện lọc mà VẪN CÓ friend thỏa mãn"),
       "1. Bấm「エクスポート条件の確認に進む」\n"
       "2. Bấm「作業開始」trong modal「CSVデータの作成確認」\n"
       "3. Chờ tiến trình đạt 100% rồi bấm sub-tab「作成履歴」\n"
       "4. Tải và mở file CSV",
       "—",
       "- Hiển thị loading「CSVデータを作成中です。」\n"
       "- Job chạy xong, file CSV tải về thành công\n"
       "- Dữ liệu trong file khớp đúng điều kiện lọc + khoảng ngày đã chọn",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r106 (TC-SC-165, nguồn v1 BS_021, Not Tested)"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Boundary",
       "Export khi KHÔNG có dữ liệu thỏa điều kiện — file chỉ có header, job vẫn chạy xong",
       ("- Đăng nhập Admin, Tab 2「チャットのCSVエクスポート」\n"
        "- Đã chọn khoảng ngày + điều kiện lọc mà KHÔNG có friend nào thỏa mãn"),
       "1. Bấm「エクスポート条件の確認に進む」\n"
       "2. Bấm「作業開始」\n"
       "3. Chờ tiến trình đạt 100% rồi bấm sub-tab「作成履歴」\n"
       "4. Tải và mở file CSV",
       "—",
       "- Job vẫn chạy xong và tạo file CSV thành công, KHÔNG báo lỗi\n"
       "- File CSV không có dòng dữ liệu nào, chỉ còn metadata header + dòng tiêu đề cột",
       env="PRODUCTION",
       note=NOSPEC + "Empty state của output export. Nguồn: v2 r107 (TC-SC-166, nguồn v1 BS_022, "
            "Not Tested). ⚠️ CẢNH BÁO 2026-09-22 (MT-26): TC này coi『file chỉ có header』là "
            "kết quả ĐÚNG, nên nó KHÔNG phân biệt được với lỗi CSV export không đọc tới các "
            "bảng `messages_YYYY` của DB lưu trữ. Khi chạy phải xác nhận trước rằng khoảng "
            "ngày chọn THỰC SỰ không có tin nào ở mọi bảng năm liên quan"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Normal",
       "Tích「一斉配信を除く」— file không còn tin gửi hàng loạt",
       ("- Đăng nhập Admin, Tab 2 sub-tab「データ作成」\n"
        "- Trong khoảng ngày chọn có CẢ tin gửi hàng loạt (一斉配信) lẫn tin thường"),
       "1. Tích checkbox「一斉配信を除く」\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100% rồi tải file CSV từ sub-tab「作成履歴」\n"
       "4. Mở file và rà toàn bộ nội dung",
       "—",
       "- File CSV tạo thành công\n"
       "- Trong file KHÔNG có tin nhắn thuộc diện gửi hàng loạt (一斉配信)\n"
       "- Các tin nhắn khác vẫn còn đầy đủ",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r108 (TC-SC-167, nguồn v1 BS_023, Not Tested). ⚠️ Tiền điều kiện "
            "của v1 ghi『không có friend thỏa mãn』— mâu thuẫn mục đích test, đã sửa lại"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Normal",
       "Tích「ステップ配信を除く」— file không còn tin từ kịch bản theo bước",
       ("- Đăng nhập Admin, Tab 2 sub-tab「データ作成」\n"
        "- Trong khoảng ngày chọn có CẢ tin từ ステップ配信 lẫn tin thường"),
       "1. Tích checkbox「ステップ配信を除く」\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100% rồi tải file CSV\n"
       "4. Mở file và rà toàn bộ nội dung",
       "—",
       "- File CSV tạo thành công\n"
       "- Trong file KHÔNG có tin nhắn thuộc ステップ配信\n"
       "- Các tin nhắn khác vẫn còn đầy đủ",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r109 (TC-SC-168, nguồn v1 BS_024, Not Tested)"),

    tc("CSV export — lịch sử tạo", "OUT-EXPORT-001", "Normal",
       "Tích CẢ HAI checkbox loại trừ — file chỉ còn tin 1:1 thường",
       ("- Đăng nhập Admin, Tab 2 sub-tab「データ作成」\n"
        "- Trong khoảng ngày chọn có đủ tin 一斉配信, tin ステップ配信 và tin 1:1 thường"),
       "1. Tích cả「一斉配信を除く」và「ステップ配信を除く」tại khu vực「エクスポート対象の選択」\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100% rồi tải file CSV\n"
       "4. Mở file và rà toàn bộ nội dung",
       "—",
       "- File CSV tạo thành công\n"
       "- Trong file KHÔNG có tin 一斉配信 VÀ KHÔNG có tin ステップ配信\n"
       "- Chỉ còn lại tin nhắn 1:1 thông thường",
       env="PRODUCTION",
       note=NOSPEC + "Nguồn: v2 r110 (TC-SC-169, nguồn v1 BS_025, Not Tested)"),
]
