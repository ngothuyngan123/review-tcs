# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Các điểm MÂU THUẪN giữa kho TCs tổng hợp và spec-features.
Trạng thái: 2 / 26 ĐÃ CHỐT (MT-01, MT-02 — Leader chốt 2026-09-21), 24 còn CHỜ QUYẾT ĐỊNH.
MT-26 mở 2026-09-22 sau khi Leader cung cấp kiến trúc bảng tin nhắn theo năm.

Nguồn đã gộp và niên đại (chi tiết ở khoá `sources` trong build.py):
• 01. TCsLine_Chat1:1 (Improve 10/2024) → tab「Setting Chat」(10/2024 → 07/2025, `SC`)
• ″ → tab「AI_TCs_Setting_chat_v1」(06/2026, `v1`)
• ″ → tab「[AI] Flow_setting_chat_v2」(06-07/2026 + 2 vòng chạy production 08/2026, `v2`)
• ″ → tab「[AI] Flow_validate_3333」(08/2026, `V3333` — chỉ lấy 3 dòng về 対応ステータス)

⚠️ CẢNH BÁO NIÊN ĐẠI: `v1` và `v2` CÁCH NHAU CHƯA ĐẦY 2 THÁNG (06/2026 vs 07/2026).
Với các mâu thuẫn giữa 2 bản này (MT-03, MT-04, MT-07, MT-17), quy tắc "ưu tiên TC
mới nhất" là CĂN CỨ YẾU. Lý do THỰC SỰ chọn `v2` làm bản viết TC là vì `v2` có
SPEC ID (SCR-01…SCR-08B / EP / BR), có ghi chú sửa expected kèm ngày, và có kết quả
chạy trên CẢ staging lẫn production — KHÔNG phải vì nó mới hơn.

✅ 2 MÂU THUẪN NỀN ĐÃ CHỐT (Leader, 2026-09-21):
• MT-01 — màn có **8 tab** (thêm「チャットのCSVエクスポート」và「重複送信防止機能」).
• MT-02 — CRUD và sắp xếp trạng thái đối ứng là thao tác **INLINE** (＋新規追加 sinh
  dòng nhập, Enter để lưu; đổi màu và kéo thả tự lưu; không có modal, không có nút 保存).
Kho đã viết TC theo đúng 2 quyết định này nên KHÔNG phải sửa expected — chỉ gỡ các
cảnh báo phụ thuộc trong cột Ghi chú.
⚠️ Hệ quả: spec-features/admin/chat-setting/ (quét theo giao diện 2025) nay ĐÃ XÁC ĐỊNH
là LẠC HẬU — danh sách việc phải sửa spec nằm ở cột "Việc phải làm tiếp" của MT-01/MT-02.
"""

COLS = ["ID", "Mức độ", "Trạng thái", "Chủ đề", "TCs nói gì (nguồn)", "Spec nói gì (nguồn)",
        "Vì sao mâu thuẫn", "TC liên quan", "QUYẾT ĐỊNH CỦA LEADER",
        "Việc phải làm tiếp"]

W = "⏳ CHỜ QUYẾT ĐỊNH"

CONFLICTS = [
    ["MT-01", "CAO", "✅ ĐÃ CHỐT",
     "SỐ TAB CỦA MÀN — 6 tab hay 8 tab? Phải chốt TRƯỚC vì quyết định ~90 TC của "
     "2 tab mới có nằm trong phạm vi FA-041 hay không",
     "Corpus 2026 (v2 r2 / TC-SC-001, Pass CẢ staging lẫn production; v1 r2 cùng nội dung):\n"
     "sidebar có ĐÚNG 8 tab theo thứ tự 1「対応ステータス編集」· 2「チャットのCSVエクスポート」· "
     "3「メッセージの自動確認済み変更」· 4「送信ショートカット」· 5「短縮URLの利用」· "
     "6「送信プレビュー」· 7「既読情報の表示」· 8「重複送信防止機能」.\n"
     "Ghi chú của v2 nói rõ『FA-041 sidebar mở rộng từ 6 → 8 tab, thứ tự đã xác nhận QA-026』.\n"
     "Tab「Setting Chat」(2025) KHÔNG có 2 tab CSV và 重複送信防止.",
     "feature-spec.md:38-45 (bảng 7 màn: SCR-CST-01…07) · feature-spec.md:24 "
     "(『Phạm vi | 6 tab + 1 modal add/edit status』) · ui-spec.md:4-11 (『6 tab cấu hình』) · "
     "ui-spec.md:47 (『Tab bar: 6 tab ngang 対応ステータス編集 | メッセージの自動確認済み変更 | "
     "送信ショートカット | 短縮URLの利用 | 送信プレビュー | 既読情報の表示』).\n"
     "Spec KHÔNG có bất kỳ dòng nào về CSV export hay 重複送信防止機能.",
     "Spec được quét theo giao diện 2025. Nếu 8 tab là đúng thì spec FA-041 thiếu hẳn "
     "2 màn + ~19 business rule (BR-CSV-01…13, BR-08B-01…05) + ~9 endpoint. "
     "Việc đánh số tab cũng lệch 1: spec gọi auto-confirm là『Tab 2』, corpus gọi là『Tab 3』.",
     "Toàn bộ nhóm『Vào màn & điều hướng tab』·『CSV export — tạo dữ liệu』·"
     "『CSV export — lịch sử tạo』·『CSV export — nội dung file』·『Chống gửi trùng — cài đặt』·"
     "『Chống gửi trùng — chặn gửi thực tế』(≈ 90 TC)",
     "**Màn có 8 tab.** (Leader chốt 2026-09-21)",
     "TCs: KHÔNG phải sửa — kho đã viết theo bản 8 tab. Đã gỡ cảnh báo phụ thuộc MT-01 khỏi "
     "ghi chú của ~90 TC (2026-09-21). "
     "SPEC phải cập nhật: (1) quét bổ sung 2 màn SCR-02/SCR-03「チャットのCSVエクスポート」và "
     "SCR-08B「重複送信防止機能」vào spec-features/admin/chat-setting/; (2) bổ sung BR-CSV-01…13 "
     "và BR-08B-01…05 vào feature-spec §6; (3) bổ sung các endpoint của 2 màn này vào api-spec; "
     "(4) ĐÁNH SỐ LẠI tab trong feature-spec §2 và ui-spec (auto-confirm từ『Tab 2』→『Tab 3』, "
     "shortcut →『Tab 4』, shorten URL →『Tab 5』, preview →『Tab 6』, FAQ →『Tab 7』); "
     "(5) sửa feature-spec:24『Phạm vi | 6 tab + 1 modal』và ui-spec:4-11 · :47."],

    ["MT-02", "CAO", "✅ ĐÃ CHỐT",
     "CƠ CHẾ CRUD TRẠNG THÁI ĐỐI ỨNG — modal + nút「保存」hay danh sách inline + Enter? "
     "Phải chốt TRƯỚC vì ảnh hưởng bước thao tác của toàn bộ nhóm 3-5",
     "Corpus 2026 (v2 r5-r13 / TC-SC-004…009, Pass cả 2 môi trường):\n"
     "• nút「＋ 新規追加」sinh 1 DÒNG NHẬP ở cuối danh sách (placeholder「対応ステータス（Enterで保存）」"
     "+ bộ đếm 0/20), nhấn Enter là lưu (BR-15)\n"
     "• sửa tên: bấm thẳng vào ô nhập trên dòng, Enter để lưu (blur KHÔNG lưu — BUG-017 Closed)\n"
     "• đổi màu: bấm bộ chọn màu trên dòng → tự lưu ngay, có toast\n"
     "• sắp xếp: kéo tay cầm (⠿) ngay trên danh sách → tự lưu\n"
     "• KHÔNG có nút「保存」riêng cho Tab 1\n"
     "• ghi chú v2 r7 nêu endpoint thực tế là `POST /ajax/create-status-item`\n\n"
     "Tab「Setting Chat」(07/2025, SC r103-r171, OK + staging OK) lại tả ĐÚNG như spec: "
     "nút「追加」mở modal「対応ステータス新規追加」, có nút「保存」và「閉じる」, nút「並べ替え」mở "
     "modal sắp xếp riêng có nút Save.",
     "ui-spec.md:52 (『2 nút hành động:「追加」(primary, icon +) và「並べ替え」(secondary, icon sort)』) · "
     "ui-spec.md:59 (『Không có form inline — chỉnh sửa qua modal SCR-CST-02』) · "
     "ui-spec.md:64-68 (bảng action: 追加 → mở modal · Edit row (icon pencil) → mở modal pre-filled) · "
     "ui-spec.md:79-99 (mô tả modal SCR-CST-02 với nút 閉じる / 保存) · "
     "feature-spec.md §3.2 (EP-06 `POST /ajax/save-item-status-v2` gửi TOÀN BỘ list status).",
     "Đây là 2 giao diện KHÁC HẲN nhau, không phải khác biệt nhỏ. Spec + TC 2025 khớp nhau "
     "(modal), corpus 2026 khớp nhau (inline). Nếu bản inline là bản đang chạy thì spec FA-041 "
     "lạc hậu về cả giao diện lẫn endpoint; nếu bản modal vẫn đang chạy thì ~40 TC nhóm 3-5 "
     "phải viết lại bước thao tác.",
     "Toàn bộ nhóm『Danh sách trạng thái đối ứng』·『Thêm & sửa trạng thái』·"
     "『Sắp xếp trạng thái』·『Xóa trạng thái』(≈ 45 TC)",
     "**CRUD và sắp xếp trạng thái đối ứng là thao tác INLINE.** (Leader chốt 2026-09-21)",
     "TCs: KHÔNG phải sửa — kho đã viết theo bản inline. Đã gỡ cảnh báo phụ thuộc MT-02 khỏi "
     "ghi chú của ~45 TC (2026-09-21). Phần MT-11 về cơ chế 並べ替え cũng đóng theo quyết định "
     "này (kéo thả trực tiếp, tự lưu, không có modal sắp xếp). "
     "SPEC phải cập nhật: (1) viết lại ui-spec SCR-CST-01 (bỏ『Không có form inline』ở :59, bỏ "
     "2 nút「追加」/「並べ替え」ở :52, thay bằng nút「＋ 新規追加」sinh dòng nhập + tay cầm kéo ⠿ + "
     "bộ chọn màu trên từng dòng); (2) GỠ hoặc đánh dấu legacy màn SCR-CST-02 (modal "
     "「対応ステータス新規追加」, ui-spec:79-99); (3) thêm BR-15 (dòng nhập chỉ xuất hiện sau khi "
     "bấm ＋新規追加) và rule『Enter lưu, blur KHÔNG lưu』(BUG-017 Closed) vào feature-spec §6; "
     "(4) XÁC NHẬN LẠI danh sách endpoint — corpus ghi `POST /ajax/create-status-item`, spec ghi "
     "EP-06 `POST /ajax/save-item-status-v2` gửi cả list; endpoint nào không còn dùng thì đánh "
     "dấu legacy (liên quan BR-08, xem MT-11); (5) đóng câu hỏi mở ui-spec §10.2 số 1."],

    ["MT-26", "CAO", W,
     "SPEC KHÔNG BIẾT LỊCH SỬ CHAT NẰM Ở DB RIÊNG, MỖI NĂM 1 BẢNG — chưa rõ CSV export "
     "có đọc tới các bảng năm cũ không",
     "Leader cung cấp 2026-09-22: lịch sử chat được tách sang **một DB riêng, mỗi năm 1 bảng** — "
     "hiện có `messages_2020` · `messages_2021` · `messages_2022` · `messages_2023` · "
     "`messages_2024` · `messages_2025`; riêng năm **2026** tin nhắn vẫn nằm ở `messages_v2s` "
     "của DB chính.\n"
     "Dấu vết trong corpus khớp với kiến trúc này: tab「Job move message」(TCsLine_Improve chung / "
     "TCsLine_JOB, 12 TC lá —『job chuyển tin nhắn sang bảng lưu trữ』) · tab「Improve move "
     "database」(01. TCsLine_Chat1:1 bản cũ, 09/2023) · tab「Tách DB sync gg」(12/2023).\n"
     "TOÀN BỘ 65 TC của 3 nhóm CSV trong corpus KHÔNG có TC nào theo chiều năm dữ liệu: "
     "23 TC nhóm『tạo dữ liệu』đều dùng ngày TƯƠNG ĐỐI, xa nhất là `today−365d`; nhóm『nội dung "
     "file』chỉ có 1 khoảng cụ thể `2026/05/04 ~ 2026/06/04` lấy từ file mẫu.",
     "feature-spec.md §4.1 (bảng Entities chính) CHỈ khai `MessagesV2s` → `messages_v2s` với mô tả "
     "『Tin nhắn chat』. feature-spec.md §4.2 (ER diagram) cũng chỉ có `messages_v2s`. "
     "db/db-mapping.md §Files DB chỉ liệt kê `db/schema/tables/messages_v2s.sql`.\n"
     "Rà toàn bộ 6 file spec của `spec-features/admin/chat-setting/`: KHÔNG có một dòng nào về "
     "archive / lưu trữ / bảng theo năm / DB riêng.",
     "Spec bỏ sót hoàn toàn 6 bảng + 1 DB. Hệ quả nghiêm trọng cho FA-041: nếu CSV export chỉ "
     "truy vấn `messages_v2s` thì mọi khoảng xuất trước 2026 sẽ ra file **chỉ có metadata + tiêu "
     "đề cột** mà job vẫn báo chạy xong bình thường — và bộ TC hiện tại KHÔNG bắt được, vì TC"
     "『Export khi KHÔNG có dữ liệu thỏa điều kiện』đang coi『file chỉ có header』là kết quả ĐÚNG. "
     "Đây là vùng mù giữa 2 feature: job chuyển tin nhắn thuộc FA-001, còn màn xuất CSV thuộc "
     "FA-041, chưa ai rà chỗ giáp ranh.",
     "Toàn bộ nhóm mới『CSV export — dữ liệu theo năm』(14 TC, bổ sung 2026-09-22) · "
     "TC『Export khi KHÔNG có dữ liệu thỏa điều kiện』(đã thêm cảnh báo) · "
     "TC『File chỉ chứa tin trong khoảng ngày đã chọn』· liên quan MT-20 và MT-23",
     "",
     "(1) Xác nhận CSV export có truy vấn các bảng `messages_YYYY` ở DB lưu trữ không, và gộp "
     "nhiều bảng theo cách nào; (2) bổ sung 6 bảng + DB lưu trữ vào feature-spec §4.1/§4.2 và "
     "db-mapping; (3) ghi rõ quy tắc chọn bảng theo khoảng ngày (kể cả khoảng vắt qua 2 DB) thành "
     "1 business rule mới; (4) chốt hành vi khi chọn năm CHƯA có bảng (vd 2019) — chặn hay trả "
     "file rỗng; (5) rà xem còn màn nào khác đọc lịch sử chat theo khoảng ngày mà cũng bỏ sót "
     "các bảng năm không (chat 1:1 FA-001, quản lý chat FA-002)."],

    ["MT-03", "CAO", W,
     "DANH SÁCH CHECKBOX CỦA TAB TỰ ĐỘNG XÁC NHẬN — có checkbox「メディア」không, và "
     "自動応答 là 1 hay 2 checkbox?",
     "v2 r113 (TC-SC-034) liệt kê 4 checkbox: 【○○】メッセージ · スタンプ · **メディア** · "
     "自動応答キーワード (gộp làm 1).\n"
     "v1 r104 (BS_031, OK) mô tả checkbox「メディア（画像・動画・音声・その他ファイル）」và ghi "
     "cột DB là **`bots.auto_confirm_message_media`**.\n"
     "v1 r105-r108 (BS_032, OK) lại TÁCH 自動応答 thành 2 checkbox riêng: "
     "「[すべてのメッセージに反応]」(`confirm_message_autoreply_all`) và "
     "「[設定したキーワードに反応]」(`confirm_message_autoreply_specified`).\n"
     "SC r24 (2025) chỉ có 1 checkbox「自動応答で設定しているキーワード」ghi vào cột "
     "`confirm_message_autoreply` (số ít).",
     "feature-spec.md §5 hàng 6-9 (Field Traceability Matrix) liệt kê ĐÚNG 4 checkbox: "
     "`confirm_message_button` · `confirm_message_stamp` · `confirm_message_autoreply_all` · "
     "`confirm_message_autoreply_specified`. KHÔNG có bất kỳ cột media nào.\n"
     "feature-spec.md §5 mục『Cột side-effect không trên UI』ghi `confirm_message_autoreply` "
     "là **deprecated** (đã comment ở cả Laravel và Spring Boot).\n"
     "job-spec: Spring Boot chỉ đọc 5 cờ, không có cờ media.",
     "3 nguồn mô tả 3 bộ checkbox khác nhau. Cột `auto_confirm_message_media` KHÔNG tồn tại "
     "trong spec/DB-mapping ⇒ hoặc là cột mới chưa được quét, hoặc tester ghi nhầm tên cột. "
     "Nếu media là tính năng thật thì Spring Boot phải có nhánh xử lý tương ứng mà job-spec "
     "chưa hề ghi.",
     "Toàn bộ nhóm『Tự động xác nhận tin nhắn』(≈ 18 TC), đặc biệt TC về checkbox「メディア」và "
     "2 cặp TC bật/tắt 自動応答",
     "",
     "Chốt xong thì: xác nhận tên cột DB thật, cập nhật feature-spec §5 + db-mapping + job-spec "
     "§8.1, và gộp/tách lại các TC 自動応答 cho khớp số checkbox thật."],

    ["MT-04", "CAO", W,
     "GIÁ TRỊ MẶC ĐỊNH CỦA TAB TỰ ĐỘNG XÁC NHẬN — 3 nguồn nói 3 kiểu, TC kiểm mặc định "
     "đang FAIL trên CẢ 2 môi trường",
     "v2 r113 (TC-SC-034): 【○○】メッセージ = **BẬT**, các checkbox còn lại TẮT, 2 toggle TẮT. "
     "Kết quả chạy: **Fail staging + Fail production**.\n"
     "v1 r109 (BS_033): toggle「返信時の自動確認済み変更」mặc định『利用する』nhưng phần expected "
     "lại ghi `confirm_message_user_send = 0` (tự mâu thuẫn trong cùng 1 dòng).\n"
     "v1 r111 (BS_036): toggle「ブロックされた友だちの…」mặc định『利用する』kèm hành vi "
     "`confirm_message_user_block_bot = 1` ⇒ mặc định BẬT.\n"
     "SC r7 · r16 · r24 · r32 · r48 (2025, OK): TẤT CẢ đều『default = 0』(TẮT).",
     "feature-spec.md §4.2 (ER diagram bảng `bots`) và db/db-mapping.md — các cột "
     "`confirm_message_*` là TINYINT; spec chỉ ghi default rõ cho `preview_after_send` = 1. "
     "Các cờ còn lại spec KHÔNG ghi giá trị mặc định.",
     "Giá trị mặc định quyết định hành vi của bot MỚI (và bot sau khi đổi LOA). Việc TC kiểm "
     "mặc định Fail ở cả staging lẫn production cho thấy giá trị thực tế KHÁC với cả 3 mô tả — "
     "chưa ai biết đúng là gì.",
     "TC『Trạng thái mặc định của Tab 3 — 4 checkbox + 2 toggle』(DỰ KIẾN FAIL) và các TC "
     "bật/tắt từng cờ trong nhóm『Tự động xác nhận tin nhắn』",
     "",
     "Đọc giá trị DEFAULT thật trong schema `bots`, đối chiếu với 1 bot mới tạo trên "
     "production, rồi ghi vào feature-spec §5 cho ĐỦ 6 cờ."],

    ["MT-05", "CAO", W,
     "TÊN TRẠNG THÁI ĐỐI ỨNG CÓ BỊ CẤM TRÙNG KHÔNG?",
     "V3333 r225 (NEW-232, 19/08/2026, gắn『QA-01 mục 1, BR-C1』— danh sách 21 mục do BA chốt): "
     "『không tạo trạng thái trùng tên và có thông báo lỗi』. TC ở trạng thái `skip` kèm ghi chú "
     "『⚠ NGHI THIẾU: mục này nằm trong danh sách 21 mục QA-01 nhưng KHÔNG có trong phần code "
     "sửa lần này. Nếu tạo được trùng ⇒ hạng mục còn thiếu, báo cáo leader』. "
     "(r223/NEW-66 và r224/NEW-145 là 2 bản trùng của cùng TC này.)\n"
     "v2 và v1 (06-07/2026) KHÔNG có TC nào về trùng tên.\n"
     "SC r123 chỉ nói về TRÙNG MÀU: 『Cho phép trùng』.",
     "feature-spec.md §6 BR-07 chỉ nói về giới hạn ĐỘ DÀI (UI 20 / EP-06 không validate / "
     "EP-08 validate 10). KHÔNG có business rule nào về tính duy nhất của `name_status`. "
     "db/db-mapping.md không có unique index trên `status_chat.name_status`.",
     "Nếu BA đã chốt cấm trùng tên (QA-01) thì đây là rule BẮT BUỘC mà cả spec lẫn code đều "
     "chưa có. Nếu không cấm thì TC NEW-232 phải bị loại khỏi phạm vi, không để ở trạng thái "
     "`skip` gây hiểu nhầm là chưa chạy được.",
     "TC『Tạo trạng thái trùng tên với trạng thái đã có — phải bị chặn』(đánh dấu DỰ KIẾN FAIL)",
     "",
     "Nếu chốt CẤM trùng: bổ sung BR mới vào feature-spec §6, thêm unique index hoặc validate "
     "ở EP tạo/sửa, và raise ticket vì hiện chưa có. Nếu chốt CHO PHÉP: xóa TC và đóng mục "
     "QA-01 số 1."],

    ["MT-06", "CAO", W,
     "GIỚI HẠN 180 NGÀY CỦA GÓI FREE Ở CSV EXPORT — mốc cắt sai và gói TRẢ PHÍ bị áp nhầm",
     "BR-CSV-02 (corpus) nói: gói Free chỉ xuất được dữ liệu trong 180 ngày lùi từ hôm nay, "
     "gói trả phí KHÔNG giới hạn (QA-005).\n"
     "Thực tế đo được:\n"
     "• v2 r53 (TC-SC-020) — khoảng ĐÚNG 180 ngày bị chặn bởi lỗi「180日以内で指定」, 179 ngày "
     "thì qua ⇒ **BUG-023 (Open, Low)**. Kết quả: Fail staging / Pass production.\n"
     "• v2 r54 (TC-SC-021) — bot gói TRẢ PHÍ (562, user đã xác nhận trực tiếp đúng là paid) "
     "VẪN bị chặn『180日以内』với khoảng 1 năm ⇒ **BUG-024 (Open, HIGH)**. "
     "Kết quả: Fail staging / Skipped production.",
     "spec-features/admin/chat-setting/ KHÔNG có tab CSV nên KHÔNG có rule nào về giới hạn "
     "180 ngày (hệ quả của MT-01). Rule gần nhất trong hệ thống là giới hạn xem lịch sử chat "
     "180 ngày của bot free (Feature #28859, thuộc FA-001).",
     "2 bug cùng vùng nhưng ngược hướng: 1 bên cắt sớm 1 ngày, 1 bên áp nhầm giới hạn cho "
     "khách TRẢ TIỀN. BUG-024 ảnh hưởng trực tiếp khách trả phí nên mức CAO. Cả 2 đều đang mở.",
     "TC『Gói Free — khoảng đúng 180 ngày…』· TC『Gói TRẢ PHÍ — khoảng ngày vượt 180 ngày…』"
     "(cả 2 đánh dấu DỰ KIẾN FAIL) · TC『Gói Free — khoảng đúng 180 ngày nhưng KHÔNG kết thúc "
     "ở hôm nay』",
     "",
     "Chốt mốc chuẩn (180 hay 179, tính theo độ dài khoảng hay tính lùi từ hôm nay), xác nhận "
     "lại BUG-024 trên production, rồi ghi BR-CSV-02 vào spec theo việc (2) của MT-01 (quét bổ sung 2 màn vào spec)."],

    ["MT-07", "TRUNG BÌNH", W,
     "TÊN TRẠNG THÁI CÓ ĐƯỢC CẮT KHOẢNG TRẮNG ĐẦU/CUỐI KHÔNG?",
     "v1 r12 (BS_002, **Pass** trên staging): nhập『   abc   』→ expected『Auto trim → abc』.\n"
     "v2 r24 (TC-SC-079, Pass): expected viết nước đôi — 『đã được trim … HOẶC nếu spec không "
     "trim thì giá trị hiển thị nhất quán với giá trị đã lưu』, kèm ghi chú "
     "『⚠ Spec chưa ghi rõ có trim hay không — verify hành vi thực tế』.\n"
     "v2 r28 (TC-SC-083, Pass): nhập TOÀN khoảng trắng thì『sau trim thành chuỗi rỗng』⇒ hàm ý "
     "CÓ trim.",
     "feature-spec.md §5 hàng 1 chỉ ghi validation độ dài (UI counter max 20, EP-06 không "
     "validate, EP-08 legacy max 10). KHÔNG có dòng nào về trim.",
     "TC『nhập toàn khoảng trắng』chỉ đúng khi CÓ trim, nên 2 TC của chính v2 ngầm mâu thuẫn "
     "nhau về việc trim có phải hành vi chính thức hay không. Nếu không trim thì tên có khoảng "
     "trắng đầu/cuối sẽ lệch hiển thị ở dropdown và modal lọc của màn chat 1:1.",
     "TC『Tên có khoảng trắng đầu/cuối — được cắt bỏ trước khi lưu』· TC『Nhập toàn khoảng trắng "
     "rồi Enter — xử lý như bỏ trống』",
     "",
     "Chốt xong thì ghi rõ quy tắc trim vào feature-spec §5 hàng 1 và đồng bộ validate ở cả "
     "client lẫn server."],

    ["MT-08", "TRUNG BÌNH", W,
     "GIỚI HẠN 20 KÝ TỰ CỦA TÊN TRẠNG THÁI KHÔNG ĐƯỢC ÁP NHẤT QUÁN (3 mức ở 3 nơi)",
     "v2 r14 / r40 (TC-SC-010, TC-SC-142, Pass cả 2 môi trường): gõ tay thì ký tự thứ 21 bị "
     "chặn hoàn toàn, bộ đếm dừng ở 20/20.\n"
     "v2 r25 (TC-SC-080, Pass): DÁN 25 ký tự — expected viết nước đôi, ghi rõ 『EP-06 xác nhận "
     "KHÔNG có validation phía server ⇒ giá trị vượt 20 ký tự CÓ THỂ được lưu thẳng vào DB』 "
     "và 『nếu phát hiện paste bypass → báo bug』.",
     "feature-spec.md §6 BR-07 (『Validation không nhất quán 3 nguồn』, mức 🟠 Trung bình): "
     "UI counter max 20 · EP-06 KHÔNG validate · EP-08 legacy validate max 10. "
     "feature-spec.md §10.3 cũng liệt kê『KHÔNG có FormRequest validation — toàn bộ dựa vào "
     "client JS』(app/Http/Requests/ không có class nào cho chat-setting).",
     "Spec đã TỰ NHẬN đây là lỗ hổng nhưng chưa có quyết định sửa. Hệ quả: dán/gọi API trực "
     "tiếp có thể ghi tên dài bất kỳ vào DB, làm vỡ hiển thị ở dropdown và modal lọc của "
     "FA-001/FA-002 (nơi chỉ cắt còn ~10 ký tự).",
     "TC『Dán 25 ký tự bằng chuột phải — kiểm tra có lọt qua giới hạn 20 không』",
     "",
     "Chốt giới hạn chuẩn (20), thêm validate phía server ở endpoint đang dùng, và quyết định "
     "số phận EP-08 legacy (validate 10) — giữ hay gỡ."],

    ["MT-09", "CAO", W,
     "XÓA TRẠNG THÁI CÓ CẢNH BÁO KHÔNG — spec nói KHÔNG, TC nói CÓ modal cảnh báo đầy đủ",
     "SC r178-r180 (07/2025, OK + staging OK) mô tả modal xóa có:\n"
     "• tiêu đề「【〇〇〇〇〇〇〇〇〇〇】を削除しますか？」(〇 là tên trạng thái)\n"
     "• nội dung「削除する場合、友だちに登録されているこの対応ステータスに関する情報が全て削除され"
     "ますのでご注意ください。」\n"
     "• 2 nút「削除する」/「キャンセル」\n"
     "v2 r11 / r17 (TC-SC-008, TC-SC-013, Pass cả 2 môi trường) xác nhận modal tồn tại và có "
     "thêm checkbox「次から表示しない」.\n"
     "v2 r13 (TC-SC-009b) lại viết expected『Không có cảnh báo số hội thoại bị ảnh hưởng (theo "
     "BR-02: hard delete không báo trước)』.",
     "feature-spec.md §3.4 (『User click icon trash trên row → **không có confirm dialog BE**; "
     "FE có modal xác nhận (cần verify)』) · feature-spec.md §6 BR-02 (『Xoá hard, … không có "
     "cảnh báo UI』) · feature-spec.md §10.2 mục 4-5 (2 câu hỏi mở: có confirm dialog không, "
     "có cảnh báo khi xoá status đang được gán không).",
     "Spec để ngỏ 2 câu hỏi mà TC 2025 đã trả lời rõ từ lâu (CÓ modal, CÓ nội dung cảnh báo). "
     "Phần『cảnh báo SỐ hội thoại bị ảnh hưởng』thì đúng là không có — cần tách bạch 2 ý này "
     "để BR-02 không bị hiểu là『xóa không hỏi gì』.",
     "TC『Modal xóa hiển thị đúng tên trạng thái và nội dung cảnh báo』· "
     "TC『Modal xóa có checkbox「次から表示しない」』· TC『Xóa trạng thái đang gán cho hội thoại』",
     "",
     "Cập nhật feature-spec §3.4 + BR-02: ghi rõ CÓ modal xác nhận phía FE kèm nguyên văn "
     "tiêu đề/nội dung, và ghi riêng rằng KHÔNG hiển thị số hội thoại bị ảnh hưởng. "
     "Đóng 2 câu hỏi mở số 4-5 ở §10.2."],

    ["MT-10", "TRUNG BÌNH", W,
     "BẢNG MÀU CỦA TRẠNG THÁI — bao nhiêu màu, màu mặc định là gì?",
     "SC r119-r120 (07/2025, OK + staging OK): 『Số lượng màu = 7』, 『Màu default = Đỏ "
     "#F44336』.\n"
     "SC r123: cho phép 2 trạng thái trùng màu.\n"
     "v2 r35 (TC-SC-130, **Not Tested**): expected chỉ ghi chung『Bảng màu hiển thị các màu "
     "chọn được theo design』kèm ghi chú『⚠ Verify số lượng/màu default với Figma』.",
     "db/db-mapping.md §5.1 chỉ có 4 hex mẫu · feature-spec.md §6 BR-11 (`status_chat.color` "
     "VARCHAR(255) chứa CẢ hex `#F44336` lẫn số `'1'`, `'2'` của bảng màu v1 legacy) · "
     "feature-spec.md §10.1 ghi『DB-mapping §5.1 thiếu palette màu chuẩn đầy đủ — cần snapshot "
     "color picker modal để lấy full 15-20 màu』· §10.2 câu hỏi 2 và 10 vẫn mở.",
     "Spec ƯỚC LƯỢNG 15-20 màu, TC 2025 đo được 7 màu, TC 2026 chưa test. Không ai biết con "
     "số đúng. Thêm nữa BR-11 cho biết dữ liệu cũ còn lưu màu dạng số ⇒ cần biết bảng màu "
     "chuẩn mới quyết được có phải migrate hay không.",
     "TC『Bảng màu — số lượng màu chọn được và màu mặc định』· TC『Cho phép 2 trạng thái trùng màu』",
     "",
     "Chụp lại bộ chọn màu trên bản đang chạy, ghi đủ danh sách hex vào db-mapping §5.1, "
     "đóng câu hỏi §10.2 số 2 và 10, và quyết định có migrate dữ liệu màu legacy '1'/'2' không."],

    ["MT-11", "TRUNG BÌNH", W,
     "POSITION 0-BASED HAY 1-BASED — các endpoint ghi `status_chat.position` theo 2 hệ khác nhau. "
     "(Phần『modal sắp xếp hay kéo thả trực tiếp』ĐÃ ĐÓNG theo MT-02: kéo thả trực tiếp, tự lưu)",
     "SC r160-r171 (07/2025, OK + staging OK): nút「並べ替え」MỞ MODAL「並べ替え」riêng, kéo thả "
     "trong modal, có bước『Sort nhưng không ấn Save → không update』⇒ modal có nút Save.\n"
     "v2 r10 (TC-SC-007, Pass cả 2 môi trường): kéo tay cầm (⠿) NGAY TRÊN danh sách, "
     "tự lưu, có toast『保存しました』, KHÔNG có modal và KHÔNG có nút Save.",
     "ui-spec.md:65 (『Sắp xếp | 並べ替え | Bật chế độ kéo-thả / mở dialog sắp xếp | **Chưa xác "
     "nhận — cần click thử**』) · ui-spec.md:266-268 (『Kịch bản 2: Mở modal riêng với list cho "
     "phép kéo thả』) · ui-spec.md:326 (câu hỏi mở số 1) · feature-spec.md §6 BR-08 "
     "(『Position 0-based vs 1-based』: EP-06 dùng index bắt đầu 0, EP-07/08/09 legacy dùng "
     "index + 1).",
     "Phần giao diện đã được MT-02 đóng (kéo thả trực tiếp). Phần CÒN LẠI: BR-08 cho thấy các "
     "endpoint đang ghi `position` theo 2 hệ khác nhau — nếu còn đường nào gọi endpoint legacy "
     "thì thứ tự hiển thị sẽ lệch 1 bậc so với đường chính. Corpus KHÔNG có TC nào kiểm điểm này.",
     "Toàn bộ nhóm『Sắp xếp trạng thái』(7 TC) — các TC hiện chỉ kiểm THỨ TỰ HIỂN THỊ sau F5, "
     "chưa kiểm giá trị `position` ghi xuống DB",
     "",
     "Rà xem còn đường nào gọi EP-07/08/09 không. Nếu không còn thì đánh dấu deprecated và "
     "BR-08 hết ý nghĩa; nếu còn thì phải thống nhất 1 hệ đánh số và bổ sung 1 TC kiểm giá trị "
     "`position` sau khi kéo thả. Gắn cùng việc (4) của MT-02 (xác nhận lại danh sách endpoint)."],

    ["MT-12", "CAO", W,
     "BUG-021 — CHUỖI KÉO THẢ LIÊN TIẾP LÀM MẤT 2/3 TRẠNG THÁI: bug thật hay lỗi công cụ test?",
     "v2 r21 (TC-SC-076『Sort → Sort tiếp (không reload) → F5』): **Fail staging + Fail "
     "production**. Ghi chú: 『Reproducible ≥ 3 lần qua Playwright automation (expect.poll, "
     "không false positive), KHÔNG tái hiện thủ công qua CLI (chậm hơn) → nghi race condition "
     "thật, đã log bug để dev điều tra thêm』.\n"
     "v2 r20 (TC-SC-075『Sort → Edit tên → F5』): Skipped cả 2 môi trường, cùng root cause; "
     "ghi chú nêu 2 nguyên nhân — nguyên nhân 1 (thiếu timeout mặc định) ĐÃ fix, nguyên nhân 2 "
     "(mất 2/3 trạng thái sau chuỗi thêm + kéo) CHƯA fix, đã chuyển sang test.fixme.\n"
     "Ghi chú vòng production round2 lại nghiêng về『test-infra thiếu waitForResponse, không "
     "phải bug app mới, cần /heal-test』.",
     "spec-features KHÔNG có phần nào về sắp xếp liên tiếp. Liên quan gần nhất: "
     "feature-spec.md §6 BR-09 (『Không transaction khi bulk save status — `DB::beginTransaction()` "
     "bị comment ở EP-06 → fail giữa chừng → inconsistent state』, mức Thấp).",
     "Nếu là bug thật thì đây là MẤT DỮ LIỆU người dùng, và BR-09 (không có transaction) là "
     "lời giải thích rất khớp — nên mức Thấp của BR-09 có thể đang bị đánh giá nhẹ. Nếu là "
     "lỗi công cụ test thì phải sửa test và gỡ dấu DỰ KIẾN FAIL. Hiện 2 ghi chú trong cùng "
     "bộ v2 kết luận ngược nhau.",
     "TC『Kéo thả 2 lần liên tiếp không reload rồi F5』· TC『Thêm liên tiếp rồi kéo thả ngay』"
     "(cả 2 đánh dấu DỰ KIẾN FAIL)",
     "",
     "Chạy TAY (không dùng automation) chuỗi thêm + kéo liên tiếp trên staging và production, "
     "đếm số bản ghi trước/sau. Nếu tái hiện: raise bug mất dữ liệu và nâng mức BR-09."],

    ["MT-13", "TRUNG BÌNH", W,
     "PHÂN TRANG TAB 1 — bao nhiêu bản ghi mỗi trang và có đổi được không?",
     "v2 r30 (TC-SC-125, Not Tested) dùng『> 100 status (≥ 2 trang)』⇒ hàm ý 100/trang, và "
     "nêu BR-14『kéo thả chỉ sắp xếp trong phạm vi trang hiện tại』.\n"
     "v1 r16-r17 (BS_006, BS_007) lại ghi rõ『phân trang 10 bản ghi』.\n"
     "SC r188-r191 chỉ kiểm bấm trang đầu / trang N / trang cuối, không nói số bản ghi.",
     "ui-spec.md:18 và :56 (`GET /ajax/init-status-chat-v2?page=1&per_page=10` — "
     "『Pagination: button「10/page」(dropdown page size)』) · ui-spec.md:68 (『Dropdown page "
     "size | 10/page | Đổi số item mỗi trang』) · ui-spec.md:330 (câu hỏi mở số 5: "
     "『Pagination tab 1: chỉ có 10/page hay đổi được?』) · ui-spec.md:73 (『Chưa rõ giới hạn "
     "tối đa số status』).",
     "3 con số khác nhau (10 theo spec + v1, 100 theo v2) và không ai biết dropdown đổi được "
     "hay không. Ảnh hưởng trực tiếp tới cách dựng dữ liệu của 3 TC phân trang và TC kéo thả "
     "giới hạn trong trang.",
     "TC『Phân trang danh sách — bấm trang đầu / trang giữa / trang cuối』· TC『Kéo thả sắp xếp "
     "chỉ có hiệu lực trong trang đang xem』· TC『Bấm「＋ 新規追加」khi trang hiện tại đã đủ 10 "
     "trạng thái』· TC『Xóa trạng thái làm rỗng trang cuối』",
     "",
     "Mở dropdown page size trên bản đang chạy, ghi số mặc định + các lựa chọn vào ui-spec, "
     "đóng câu hỏi mở số 5, và chốt có giới hạn tối đa số trạng thái hay không."],

    ["MT-14", "CAO", W,
     "QUYỀN STAFF VỚI MÀN CÀI ĐẶT CHAT — backend KHÔNG kiểm quyền, và chưa ai từng test",
     "v2 r163 (TC-SC-102, **Not Tested**): expected bỏ ngỏ — 『⚠ Custom role FA-036 kiểm soát "
     "quyền cụ thể cho từng tab (đọc/ghi) chưa được xác nhận từ reviewer — Expected Result "
     "chưa thể chốt chi tiết』, ⏳ Pending QA-027, và ghi rõ cần bổ sung test bypass URL/API "
     "khi có ma trận quyền.\n"
     "SC r220 (2025) chỉ có đúng 1 dòng『Check thao tác bằng account staff』với kết quả OK, "
     "KHÔNG có kết quả mong đợi.\n"
     "Toàn corpus KHÔNG có TC nào gọi thẳng API bằng phiên của Staff không có quyền.",
     "feature-spec.md §6 BR-06 (『**Không có Staff authorization check** — BE chỉ check login + "
     "bot ownership, không check custom role permission. Mọi user truy cập được đều có thể "
     "CRUD full settings. UI ẩn menu phụ thuộc FE only』, mức 🟡 Trung bình, nguồn §6.2 "
     "logic-spec) · feature-spec.md §10.3 lặp lại cảnh báo này · §10.2 câu hỏi mở số 6.",
     "Spec khẳng định backend KHÔNG chặn, giao diện chỉ ẩn menu. Đây đúng là dạng lỗi "
     "『API không enforce quyền dù UI ẩn menu』. Chưa TC nào kiểm ở tầng API ⇒ rủi ro bỏ lọt "
     "hoàn toàn.",
     "TC『Staff theo vai trò tùy chỉnh — tab không có quyền phải ẩn hoặc chỉ đọc』· "
     "TC『Staff KHÔNG có quyền — gọi thẳng API cũng phải bị chặn』(TC BỔ SUNG, DỰ KIẾN FAIL)",
     "",
     "Lấy ma trận quyền từ FA-036 (QA-027), chốt mức quyền cho từng tab, rồi rà TẦNG API cho "
     "TẤT CẢ endpoint của FA-041 — không chỉ màn cài đặt chat mà cả các màn cùng lưới phân quyền."],

    ["MT-15", "CAO", W,
     "2 LỖ HỔNG SPEC ĐÃ CHỈ ĐÍCH DANH NHƯNG KHÔNG TC NÀO KIỂM: mass assignment và IDOR",
     "Toàn bộ corpus (SC 2025 · v1 · v2 · V3333) KHÔNG có bất kỳ TC nào:\n"
     "• gửi thêm trường lạ vào API lưu cấu hình để kiểm mass assignment;\n"
     "• gọi API sắp xếp trạng thái với `id` thuộc bot khác để kiểm IDOR.\n"
     "Đây là GAP, không phải mâu thuẫn nội dung.",
     "feature-spec.md §6 BR-03 (mức 🔴 **Nghiêm trọng**): `Bots::where('id',$botId)->update("
     "$request->all())` với `$guarded = []` ⇒ client có thể ghi đè BẤT KỲ cột nào của `bots` "
     "(`admin_id`, `plan_type`, `line_channel_secret`, `free_send_count`, `is_active`…), "
     "nguồn `ChatController.php:3950-3961`, `Bots.php:15`.\n"
     "feature-spec.md §6 BR-04 (mức 🟠 Cao): EP-09 `/ajax/sort-status-chat` KHÔNG lọc `bot_id` "
     "⇒ đổi được `position` trạng thái của bot khác, nguồn `ChatController.php:771-787`.\n"
     "feature-spec.md §10.3 liệt kê lại cả 2.",
     "Spec đánh giá 1 lỗ hổng NGHIÊM TRỌNG và 1 lỗ hổng CAO nhưng bộ TC hoàn toàn im lặng. "
     "Theo thang mức độ của kho, GAP ở mức Nghiêm trọng phải được xử lý trước các mâu thuẫn "
     "về giao diện.",
     "TC『Gửi thêm trường lạ vào API lưu cấu hình』· TC『Gọi API sắp xếp trạng thái với id của "
     "bot KHÁC』(cả 2 là TC BỔ SUNG do AI viết từ spec, DỰ KIẾN FAIL)",
     "",
     "Quyết định có đưa 2 TC bảo mật này vào bộ chạy chính thức không (và chạy ở môi trường "
     "nào). Nếu tái hiện: raise ticket cho Dev thêm `$fillable`/whitelist cho `bots` và thêm "
     "lọc `bot_id` cho EP-09 (hoặc gỡ hẳn endpoint legacy)."],

    ["MT-16", "TRUNG BÌNH", W,
     "CHẶN GỬI TRÙNG CÓ ÁP CHO ADMIN KHÔNG, hay chỉ áp cho「他のスタッフ」?",
     "v2 r154 (TC-SC-151, Not Tested): 『Modal hiện cho Admin chính (Admin cũng bị chặn, KHÔNG "
     "ngoại lệ)』, ghi chú『Per user spec 2026-06-05: Admin KHÔNG được miễn chặn — cần làm rõ "
     "spec「他のスタッフ」』.\n"
     "v2 r152 (TC-SC-149): Admin gửi trước thì Staff bị chặn, Admin vẫn gửi tiếp được.\n"
     "Cả 2 đều ⏳ Pending QA-027.",
     "spec-features KHÔNG có SCR-08B (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01). Chuỗi「他のスタッフ」chỉ xuất hiện trong "
     "mô tả màn của corpus, không có trong spec chính thức.",
     "Chữ「スタッフ」trong tiếng Nhật thường chỉ nhân viên, không bao gồm chủ tài khoản. Nếu "
     "giao diện nói「他のスタッフ」mà thực tế chặn cả Admin thì chuỗi hiển thị sai nghĩa; ngược "
     "lại nếu Admin được miễn thì 2 TC trên phải viết lại.",
     "TC『Admin gửi trước — 1 Staff khác bị chặn』· TC『Staff gửi trước — Admin chủ cũng bị chặn』",
     "",
     "Chốt phạm vi áp dụng, sau đó sửa chuỗi hiển thị trên màn Tab 8 cho khớp và ghi vào spec "
     "theo việc (2) của MT-01 (quét bổ sung 2 màn vào spec)."],

    ["MT-17", "TRUNG BÌNH", W,
     "GIÁ TRỊ MẶC ĐỊNH CỦA TOGGLE「重複送信防止機能」",
     "v2 r148 (TC-SC-098, **Skipped cả staging lẫn production**): expected ghi rõ 『⚠ Giá trị "
     "default chưa được xác nhận chính thức. TA đề xuất default = OFF (QA-011 qa-dev, để nhất "
     "quán với các cờ khác trong bảng `bots`) nhưng CHƯA confirm từ reviewer』. "
     "⏳ Pending QA-021 / QA-011.",
     "spec-features KHÔNG có SCR-08B (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01) nên không có giá trị mặc định nào.",
     "Tính năng này CHẶN thao tác gửi tin của người dùng. Nếu mặc định BẬT mà khách không "
     "biết thì staff sẽ bất ngờ không gửi được tin — rủi ro nghiệp vụ trực tiếp. Chưa ai xác "
     "nhận được giá trị thật vì TC bị Skipped ở cả 2 môi trường.",
     "TC『Trạng thái mặc định của Tab 8 khi bot chưa từng cấu hình』",
     "",
     "Tạo 1 bot mới trên staging, mở Tab 8 lần đầu và ghi lại giá trị thật của cả toggle lẫn "
     "ô「送信停止時間」; đưa vào spec theo việc (2) của MT-01 (quét bổ sung 2 màn vào spec)."],

    ["MT-18", "THẤP", W,
     "Ô「送信停止時間」KHI TOGGLE TẮT — ẩn hoàn toàn hay vẫn hiện nhưng bị khóa?",
     "v2 r149 (TC-SC-099, Pass cả 2 môi trường): expected viết nước đôi 『(A) ẩn hoàn toàn, "
     "hoặc (B) vẫn hiện nhưng disabled』, ⏳ Pending QA-023.\n"
     "v2 r160 (TC-SC-157, Pass cả 2 môi trường) lại khẳng định ở bước 5: 『xác nhận ô "
     "「送信停止時間」ẩn hoàn toàn』, và ghi chú liên quan BUG-011 (Closed — 『input ẩn khi OFF "
     "đã xác nhận fix』).",
     "spec-features KHÔNG có SCR-08B (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01).",
     "2 TC trong CÙNG bộ v2 mô tả 2 hành vi khác nhau cho cùng 1 ô nhập, dù cả 2 đều Pass — "
     "nghĩa là ít nhất 1 trong 2 expected quá lỏng để bắt lỗi.",
     "TC『Toggle TẮT — ô「送信停止時間」ẩn hoặc bị khóa』· TC『Tắt rồi bật lại toggle — ô giữ "
     "nguyên giá trị』",
     "",
     "Chốt 1 trong 2 hành vi (BUG-011 Closed nghiêng về『ẩn』), sửa expected của TC-SC-099 cho "
     "hết nước đôi, đóng QA-023."],

    ["MT-19", "TRUNG BÌNH", W,
     "FRIEND BLOCK BOT THÌ `confirm_count` CÓ VỀ 0 KHÔNG?",
     "Tab「improve count comfirm_message」(TCsLine_Improve chung, 10/2023, OK + staging + step "
     "OK) r20 · r58 · r96: 『user block bot → **confirm_count vẫn giữ nguyên**』; r21-r22: "
     "block rồi unblock cũng giữ nguyên, chỉ tăng khi friend nhắn tin mới.\n"
     "v2 r189 (TC-SC-189, Not Tested) và SC r49-r51 (2025, OK): khi toggle「ブロックされた友だちの"
     "自動確認済み変更」BẬT thì toàn bộ `unconfirm_message` của hội thoại bị xóa và "
     "`conversation.confirm_count` = 0.",
     "feature-spec.md §6 BR-13 (『`confirm_message_user_block_bot` áp CẢ unfollow lẫn leave "
     "group』) · feature-spec.md §3.6 sequence diagram (nhánh `confirm_message_user_block_bot "
     "= 1` → DELETE `unconfirm_message` + reset `confirm_count = 0` + `has_status_1 = 1`) · "
     "job-spec §8.1 (HandlePostbackTask.java:1945-1966, 414-428).",
     "Hai mô tả CHỈ dung hòa được nếu tab 2023 chạy trong trạng thái cờ TẮT. Nhưng tab 2023 "
     "KHÔNG ghi trạng thái cờ, nên đọc riêng nó sẽ hiểu nhầm là hành vi mặc định của hệ thống. "
     "Lưu ý tab này đã được gom vào kho FA-001 nên rủi ro 2 kho mô tả ngược nhau.",
     "TC『Bật toggle「ブロックされた友だちの…」』· TC『TẮT toggle「ブロックされた友だちの…」』",
     "",
     "Xác nhận trạng thái cờ khi tab 2023 được chạy; nếu đúng là cờ TẮT thì bổ sung điều kiện "
     "『với cờ = 0』vào các TC tương ứng BÊN KHO FA-001 để 2 kho không mâu thuẫn."],

    ["MT-20", "TRUNG BÌNH", W,
     "NỘI DUNG FILE CSV — giá trị target (QA-030/031/032) khác với file mẫu thật",
     "v2 r67 (TC-SC-059) ·  r68 (TC-SC-060): expected theo QA-032 là 送信者タイプ ∈ "
     "{「友だち」,「LOAアカウント」} và 送信者名 luôn là tên thật; nhưng ghi chú nói rõ "
     "『⚠ File mẫu cũ hiển thị「User」/「Account」(legacy)』và『file mẫu cũ hiển thị「Unknown」cho "
     "mọi tin Account』.\n"
     "v2 r76 (TC-SC-068): QA-030 chốt encoding UTF-8 with BOM, thay cho giả định SHIFT-JIS cũ.\n"
     "v2 r78 (TC-SC-070『Tin đã thu hồi』): Kết quả thực thi = **Fail**.\n"
     "v2 r77 (TC-SC-069) tự nó vẫn ghi 送信者タイプ =「Account」(giá trị legacy) ⇒ mâu thuẫn "
     "nội bộ với TC-SC-059.",
     "spec-features KHÔNG có tab CSV (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01) nên không có mô tả nội dung file nào.",
     "Bộ TC được viết theo giá trị TARGET, trong khi bằng chứng duy nhất (file mẫu) cho giá "
     "trị LEGACY. Toàn bộ nhóm『CSV export — nội dung file』vì thế DỰ KIẾN FAIL nếu bản đang "
     "chạy chưa cập nhật. Riêng TC tin đã thu hồi đã Fail thật — đây là rủi ro LỘ NỘI DUNG "
     "người dùng đã thu hồi.",
     "Toàn bộ nhóm『CSV export — nội dung file』(25 TC), nặng nhất là TC『Tin đã thu hồi』, "
     "TC『送信者タイプ』, TC『送信者名』",
     "",
     "Tạo 1 file CSV mới trên bản đang chạy rồi đối chiếu 3 điểm: giá trị 送信者タイプ, "
     "送信者名 và dòng của tin đã thu hồi. Nếu vẫn legacy thì raise ticket; nếu đã đổi thì gỡ "
     "dấu DỰ KIẾN FAIL và sửa TC-SC-069 cho khớp QA-032."],

    ["MT-21", "TRUNG BÌNH", W,
     "XUẤT CSV CHO NHIỀU FRIEND ĐƯỢC ĐÓNG GÓI THẾ NÀO — 1 file gộp hay nhiều file per-friend?",
     "v2 r79 (TC-SC-071, Not Tested): tên file theo mẫu `{friendId}_{start}_{end}_{tên "
     "friend}.csv` ⇒ mỗi friend 1 file; nhưng ghi chú nói rõ『⚠ Cách đóng gói bulk (1 file gộp "
     "hay ZIP nhiều file per-friend) reviewer chưa xác nhận rõ — giữ theo file mẫu per-friend』.\n"
     "Trong khi đó v2 r96 (TC-SC-088) cho thấy màn tạo CSV có「対象人数」— tức là xuất cho "
     "NHIỀU friend cùng lúc.",
     "spec-features KHÔNG có tab CSV (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01).",
     "Màn cho lọc ra N friend nhưng tên file lại theo từng friend ⇒ chưa rõ khi N > 1 thì người "
     "dùng nhận được gì. Ảnh hưởng tới cách viết bước『tải và mở file』của 6 TC xuất dữ liệu.",
     "TC『Tên file tải về đúng mẫu per-friend』· TC『Export khi CÓ dữ liệu thỏa điều kiện』· "
     "TC『Export khi KHÔNG có dữ liệu thỏa điều kiện』· 3 TC checkbox loại trừ",
     "",
     "Tạo 1 CSV với bộ lọc khớp ≥ 2 friend rồi tải về xem nhận được 1 file hay 1 file nén; "
     "ghi vào BR-CSV-09 theo việc (2) của MT-01 (quét bổ sung 2 màn vào spec)."],

    ["MT-22", "THẤP", W,
     "DRAWER「絞り込み履歴」— đã bị khách bỏ khỏi thiết kế nhưng TC cũ vẫn còn kiểm",
     "v2 r56 (TC-SC-023, Pass cả 2 môi trường): expected là KHÔNG có icon đồng hồ, KHÔNG có "
     "drawer「絞り込み履歴」; ghi chú『REMOVED 2026-07-23: drawer + icon đồng hồ bị khách bỏ khỏi "
     "design SCR-02 (quyết định khách — test-plan/spec đã cập nhật)』.\n"
     "Bản TC-SC-024 CŨ ở v1 lại kiểm nút「確認」bên trong chính drawer đó; v2 r64 đã thay nội "
     "dung TC-SC-024 thành『Lưu tối đa 100 file CSV』.",
     "spec-features KHÔNG có tab CSV (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01) nên không có mô tả drawer nào.",
     "Đây là quyết định của khách đã có hiệu lực, không phải mâu thuẫn kỹ thuật — nhưng cần "
     "Leader xác nhận để chốt rằng TC kiểm『KHÔNG có drawer』là đúng phạm vi và không cần khôi "
     "phục nhóm TC cũ.",
     "TC『Không còn icon lịch sử lọc và drawer「絞り込み履歴」』· TC『Lịch sử chỉ giữ tối đa 100 file』",
     "",
     "Xác nhận quyết định bỏ drawer là chính thức; nếu đúng thì đóng mục này và không khôi "
     "phục nhóm TC drawer của v1."],

    ["MT-23", "CAO", W,
     "「対象人数」Ở MÀN TẠO CSV ĐANG SAI TRÊN PRODUCTION",
     "v2 r96 (TC-SC-088『対象人数 cập nhật đúng sau khi lưu điều kiện lọc』): "
     "Blocked trên staging và **Fail trên production**. Expected: số hiển thị phải khớp số "
     "friend thực tế khớp điều kiện lọc và chỉ cập nhật sau khi lưu filter (BR-CSV-06).",
     "spec-features KHÔNG có tab CSV (hệ quả MT-01 — việc quét bổ sung nằm ở MT-01) nên không có công thức đếm nào để đối chiếu.",
     "「対象人数」là con số người dùng dựa vào để quyết định có xuất hay không. Sai số này dẫn "
     "tới xuất thiếu/thừa dữ liệu mà không ai phát hiện. Đang Fail trên MÔI TRƯỜNG THẬT nhưng "
     "chưa có ticket nào được nêu trong corpus.",
     "TC『対象人数 cập nhật đúng sau khi lưu điều kiện lọc』(DỰ KIẾN FAIL) · "
     "TC『Lọc theo シナリオ』· TC『Kết hợp scenario + tag』",
     "",
     "Chạy lại trên production với 1 bộ lọc có số friend biết trước, so số hiển thị với số "
     "đếm tay ở màn danh sách bạn bè. Nếu lệch: raise ticket mức Cao và xác định công thức đếm."],

    ["MT-24", "TRUNG BÌNH", W,
     "Ô TÍCH「không hiển thị preview nữa」TRONG MODAL XEM TRƯỚC CÓ TẮT LUÔN TOGGLE TAB 6 KHÔNG?",
     "v1 r125 (BS_049, Pass OK STG): tích ô này trong modal xem trước ⇒ 『Toggle = OFF』ở màn "
     "cài đặt, và từ đó bấm gửi không còn hiện modal.\n"
     "v1 r126 (BS_050, Pass OK STG): bật lại toggle thì modal hiện lại.\n"
     "v2 (06-07/2026) KHÔNG có TC nào về ô tích này.",
     "feature-spec.md §3.9 chỉ mô tả toggle ở Tab 5 (theo cách đánh số của spec) ghi "
     "`bots.preview_after_send`, áp dụng phía client (`chat-v2.js:3237, 3244, 3250, 3584-3589`). "
     "KHÔNG có dòng nào về ô tích trong modal xem trước.",
     "Đây là đường GHI THỨ HAI vào cùng 1 cột cấu hình, nằm ở màn KHÁC (chat 1:1) — dạng rất "
     "dễ lọt khi chỉ test ở màn cài đặt. Spec hoàn toàn không biết đường này tồn tại.",
     "TC『Tích「không hiển thị preview nữa」trong modal — toggle Tab 6 chuyển sang TẮT』· "
     "TC『Bật lại toggle sau khi đã tích ô này』",
     "",
     "Xác nhận ô tích còn tồn tại trên bản đang chạy; nếu còn thì bổ sung vào feature-spec §3.9 "
     "và §5 (ghi rõ cột `preview_after_send` có 2 đường ghi)."],

    ["MT-25", "THẤP", W,
     "ĐÍCH ĐẾN CỦA CÁC LINK FAQ — 3 URL tayori cụ thể và link「詳細を見る」vs「こちら」",
     "SC r89-r91 (2025, OK) ghi 3 URL tayori.com cụ thể cho 3 câu hỏi của Tab「既読情報の表示」.\n"
     "SC r87 (OK + staging + step OK) ghi link「こちら」trong khung「ご注意」của Tab xem trước "
     "trỏ tới `tayori.com/faq/.../0a5aee0439630290b4f...`.\n"
     "v2 r131 (TC-SC-139, Pass cả 2 môi trường) lại ghi link trong khung「ご注意」tên là "
     "「詳細を見る」và trỏ tới `https://lme.jp/manual/cancel_sent_message/`.\n"
     "v2 r134 (TC-SC-140, Pass) dùng lại 3 URL tayori của v1 nhưng ghi chú 『⚠ screens/SCR-08 "
     "chỉ ghi chung「tayori.com FAQ」— verify lại URL chính xác khi automation』.",
     "ui-spec.md phần SCR-CST-07 và feature-spec.md §2 chỉ ghi『Read-only FAQ』, KHÔNG liệt kê "
     "URL đích cụ thể nào.",
     "Không rõ「詳細を見る」và「こちら」là 2 link khác nhau hay cùng 1 link đã đổi đích (từ "
     "tayori sang lme.jp/manual). Nếu là 1 link đã đổi thì TC của SC đã lạc hậu; nếu là 2 link "
     "thì đang thiếu TC cho 1 trong 2.",
     "TC『3 link「詳細はこちら」mở đúng 3 trang FAQ tương ứng』· TC『Link「こちら」trong khung "
     "「ご注意」của Tab 6』· TC『Link「詳細を見る」trong khung「ご注意」』",
     "",
     "Mở từng link trên bản đang chạy, ghi đủ URL đích vào ui-spec SCR-CST-06/07, rồi gộp hoặc "
     "tách 2 TC link của khung「ご注意」cho khớp thực tế."],
]
