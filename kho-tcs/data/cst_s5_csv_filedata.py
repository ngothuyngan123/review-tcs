# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 9: CSV export — nội dung file (BR-CSV-12 / BR-CSV-13).

Toàn bộ nhóm này kiểm chứng FILE TẢI VỀ, không phải màn hình → `env=PRODUCTION`
theo RULE-08 (output thật: file tải về).

⚠️ MT-01 đã chốt 8 tab ⇒ tab CSV trong phạm vi, nhưng spec CHƯA quét màn này.
Phần lớn nội dung là OBSERVED từ file mẫu do tester đính kèm, nên mọi chuỗi cố định
đều ghi rõ nguồn.
"""
from _common import tc

HAVE = "- Đã tạo và tải về 1 file CSV chat từ Tab 2 sub-tab「作成履歴」"
SEC = "CSV export — nội dung file"
NOSPEC = "⚠️ Tab CSV trong phạm vi (MT-01 đã chốt 8 tab) nhưng spec CHƯA quét. "


def f(vp, kind, title, pre, steps, data, expect, note):
    return tc(SEC, vp, kind, title, pre, steps, data, expect,
              env="PRODUCTION", note=NOSPEC + note)


S9 = [
    f("OUT-EXPORT-001", "Normal",
      "Metadata header — 3 dòng đầu file",
      HAVE,
      "1. Mở file CSV bằng trình soạn thảo văn bản (UTF-8)\n"
      "2. Quan sát 3 dòng đầu tiên (trước dòng tiêu đề cột)",
      "—",
      "- Dòng 1: `アカウント名,{tên tài khoản bot}` (vd「エルメサポート」)\n"
      "- Dòng 2: `タイムゾーン,'+09:00` — giá trị có dấu nháy đơn `'` đứng trước\n"
      "- Dòng 3: `ダウンロード日時,{yyyy/MM/dd HH:mm}` đúng thời điểm tải file",
      "BR-CSV-12. Nguồn: v2 r65 (TC-SC-057, Not Tested — OBSERVED từ file mẫu)"),

    f("OUT-EXPORT-001", "Normal",
      "Dòng tiêu đề cột — đúng 5 cột đúng thứ tự",
      HAVE,
      "1. Mở file CSV\n"
      "2. Quan sát dòng thứ 4 (dòng tiêu đề cột)",
      "—",
      "- Tiêu đề đúng 5 cột theo thứ tự:「送信者タイプ」·「送信者名」·「送信日」·「送信時刻」·「内容」\n"
      "- Không thừa, không thiếu cột",
      "BR-CSV-12. Nguồn: v2 r66 (TC-SC-058, Not Tested) · v1 r78 (BS_026, OK) · v1 r82 (BS_030)"),

    f("OUT-EXPORT-001", "Normal",
      "送信者タイプ chỉ nhận 2 giá trị「友だち」hoặc「LOAアカウント」",
      HAVE + "\n- File CSV có cả tin từ phía LOA lẫn tin từ friend",
      "1. Mở file CSV\n"
      "2. Quét toàn bộ giá trị cột「送信者タイプ」",
      "—",
      "- Cột chỉ chứa 2 giá trị:「友だち」(tin từ friend LINE) hoặc「LOAアカウント」(tin gửi từ phía OA)\n"
      "- Không xuất hiện giá trị nào khác",
      "⚠️ Phụ thuộc MT-20 — QA-032 chốt giá trị đúng là「友だち」/「LOAアカウント」, nhưng FILE MẪU CŨ "
      "hiển thị「User」/「Account」(legacy) ⇒ DỰ KIẾN FAIL nếu bản đang chạy chưa đổi. "
      "Nguồn: v2 r67 (TC-SC-059, Not Tested)"),

    f("OUT-EXPORT-001", "Normal",
      "送信者名 luôn là tên người gửi thực tế, không có「Unknown」",
      HAVE + "\n- File CSV có cả dòng「友だち」và dòng「LOAアカウント」(có tin do admin và/hoặc staff gửi)",
      "1. Mở file CSV\n"
      "2. Đối chiếu cột「送信者タイプ」với cột「送信者名」trên từng dòng",
      "—",
      "- Dòng「送信者タイプ」=「友だち」: cột「送信者名」là tên hiển thị của friend\n"
      "- Dòng「送信者タイプ」=「LOAアカウント」: cột「送信者名」là tên người gửi thực tế phía OA —\n"
      "  tên admin nếu admin gửi, tên staff nếu staff gửi (lấy từ `users.username`)\n"
      "- KHÔNG có giá trị「Unknown」ở bất kỳ dòng nào",
      "⚠️ Phụ thuộc MT-20 — QA-032; file mẫu cũ hiển thị「Unknown」cho mọi tin Account ⇒ DỰ KIẾN "
      "FAIL nếu bản đang chạy chưa đổi. Nguồn: v2 r68 (TC-SC-060, Not Tested)"),

    f("OUT-EXPORT-001", "Normal",
      "Định dạng 送信日 = yyyy/MM/dd",
      HAVE + "\n- File CSV có ít nhất 1 dòng dữ liệu",
      "1. Mở file CSV\n"
      "2. Quét toàn bộ giá trị cột「送信日」",
      "—",
      "- Mọi giá trị theo dạng `yyyy/MM/dd` (vd「2026/05/04」)\n"
      "- Dùng dấu `/` ngăn cách, KHÔNG phải `-`",
      "BR-CSV-12. Nguồn: v2 r69 (TC-SC-061, Not Tested)"),

    f("OUT-EXPORT-001", "Normal",
      "Định dạng 送信時刻 = HH:mm:ss 24 giờ theo JST",
      HAVE + "\n- File CSV có ít nhất 1 dòng dữ liệu",
      "1. Mở file CSV\n"
      "2. Quét toàn bộ giá trị cột「送信時刻」\n"
      "3. Đối chiếu với giá trị「タイムゾーン」ở metadata header",
      "—",
      "- Mọi giá trị theo dạng `HH:mm:ss` 24 giờ (vd「16:39:02」)\n"
      "- Giờ tính theo múi giờ +09:00 (JST), khớp giá trị「タイムゾーン」ở header",
      "BR-CSV-12. Nguồn: v2 r70 (TC-SC-062, Not Tested)"),

    f("OUT-EXPORT-001", "Normal",
      "File chỉ chứa tin trong khoảng ngày đã chọn",
      "- Đã tạo CSV với khoảng ngày cụ thể (vd 2026/05/04 ~ 2026/06/04) và đã tải file về",
      "1. Mở file CSV\n"
      "2. Kiểm tra「送信日」của dòng đầu tiên và dòng cuối cùng\n"
      "3. Quét toàn bộ cột「送信日」",
      "date_from = 2026/05/04, date_to = 2026/06/04",
      "- Mọi「送信日」nằm trong khoảng [ngày bắt đầu, ngày kết thúc] đã chọn\n"
      "- Không có tin nào trước 2026/05/04 hoặc sau 2026/06/04",
      "BR-CSV-12. Nguồn: v2 r71 (TC-SC-063, Not Tested)"),

    f("OUT-EXPORT-001", "Normal",
      "Thứ tự tin nhắn tăng dần theo thời gian",
      HAVE + "\n- File CSV có nhiều dòng dữ liệu trải qua nhiều ngày",
      "1. Đọc lần lượt các dòng từ trên xuống\n"
      "2. So sánh「送信日」rồi「送信時刻」giữa các dòng liền kề",
      "—",
      "- Tin nhắn sắp xếp tăng dần (cũ → mới) theo「送信日」rồi đến「送信時刻」\n"
      "- Không có dòng nào đảo ngược thứ tự thời gian",
      "BR-CSV-12. Nguồn: v2 r72 (TC-SC-064, Not Tested)"),

    f("OUT-EXPORT-001", "Boundary",
      "Nội dung nhiều dòng — giữ nguyên xuống dòng trong cùng 1 ô",
      HAVE + "\n- File CSV có tin nhắn dài nhiều đoạn (vd tin form/khảo sát)",
      "1. Mở file bằng Excel bản tiếng Nhật\n"
      "2. Tìm dòng có nội dung nhiều đoạn\n"
      "3. Quan sát ô cột「内容」",
      "—",
      "- Toàn bộ nội dung nằm gọn trong 1 ô cột「内容」\n"
      "- Trường được bao bởi dấu nháy kép `\"...\"`, ký tự xuống dòng bên trong giữ nguyên\n"
      "- Mở Excel: hiển thị xuống dòng đúng trong cùng 1 ô, không tách sang dòng/cột khác",
      "BR-CSV-12. Nguồn: v2 r73 (TC-SC-065, Confirm — OBSERVED từ file mẫu)"),

    f("OUT-EXPORT-001", "Boundary",
      "Trường chứa dấu phẩy / nháy kép — escape đúng chuẩn CSV",
      HAVE + "\n- File CSV có tin nhắn chứa dấu phẩy `,` hoặc nháy kép `\"` trong nội dung",
      "1. Mở file bằng trình soạn thảo văn bản\n"
      "2. Tìm trường có ký tự đặc biệt (xuống dòng / `,` / `\"`)\n"
      "3. Mở lại bằng Excel bản tiếng Nhật",
      "—",
      "- Trường chứa xuống dòng / dấu phẩy / nháy kép được bao trong `\"...\"`\n"
      "- Nháy kép bên trong nội dung được escape thành nháy kép đôi `\"\"`\n"
      "- Mở Excel: không bị tách cột sai, nội dung nguyên vẹn",
      "BR-CSV-12. Nguồn: v2 r80 (TC-SC-072, Not Tested) · v1 r80 (BS_028, OK) · v1 r96 (BS_044). "
      "Phần escape `,`/`\"` là INFERRED — cần verify với dữ liệu thật có dấu phẩy ASCII"),

    f("DATA-TEXT-001", "Boundary",
      "Emoji và tiếng Nhật / tiếng Việt trong file — không lỗi ký tự",
      HAVE + "\n- File CSV có tin nhắn / tên chứa emoji, tiếng Nhật và tiếng Việt",
      "1. Mở file bằng Excel bản tiếng Nhật\n"
      "2. Mở lại file bằng trình soạn thảo UTF-8\n"
      "3. Quan sát các ô có emoji ở cột「送信者名」và cột「内容」",
      "—",
      "- Emoji hiển thị đúng nguyên bản ở cả 2 cách mở, không mất, không thành「?」hay「〓」\n"
      "- Tiếng Nhật và tiếng Việt hiển thị đúng, không mojibake",
      "BR-CSV-12. Nguồn: v2 r74 (TC-SC-066, Not Tested) · v1 r79 (BS_027, OK) · v1 r90 (BS_038)"),

    f("SEC-002", "Normal",
      "Chống CSV formula injection — thêm `'` trước giá trị bắt đầu bằng công thức",
      HAVE + "\n- File CSV có tin nhắn bắt đầu bằng ký tự `=` / `+` / `-` / `@` (vd tin form bắt đầu `=========`)",
      "1. Mở file bằng trình soạn thảo văn bản (UTF-8)\n"
      "2. Tìm ô「内容」có nội dung gốc bắt đầu bằng `=`\n"
      "3. Kiểm tra ký tự đầu của trường; kiểm tra thêm giá trị「タイムゾーン」\n"
      "4. Mở lại file bằng Excel",
      "Nội dung gốc: =========",
      "- Giá trị bắt đầu bằng ký tự công thức được thêm dấu nháy đơn `'` đứng trước\n"
      "  (lưu là `'=========`; timezone lưu là `'+09:00`)\n"
      "- Mở Excel: nội dung hiển thị nguyên văn, KHÔNG bị Excel diễn giải thành công thức,\n"
      "  không hiện lỗi `#NAME?`",
      "SEC-002 — chống formula injection. Nguồn: v2 r75 (TC-SC-067, Confirm) · v1 r91 (BS_039)"),

    f("OUT-EXPORT-001", "Boundary",
      "Encoding = UTF-8 with BOM, kết thúc dòng CRLF",
      HAVE,
      "1. Mở file bằng trình xem hex, kiểm tra 3 byte đầu\n"
      "2. Kiểm tra ký tự kết thúc dòng\n"
      "3. Mở file bằng Excel bản tiếng Nhật",
      "—",
      "- 3 byte đầu file là BOM UTF-8 `EF BB BF`\n"
      "- Kết thúc dòng là CRLF (`\\r\\n`)\n"
      "- Mở Excel JP: tiếng Nhật + emoji hiển thị đúng, không mojibake",
      "⚠️ Phụ thuộc MT-20 — QA-030 chốt UTF-8 with BOM (để hiển thị được emoji), BR-CSV-09 đã cập "
      "nhật từ SHIFT-JIS sang UTF-8 BOM. Nguồn: v2 r76 (TC-SC-068, Not Tested) · v1 r92 (BS_040, Pass)"),

    f("OUT-EXPORT-001", "Boundary",
      "Tên file tải về đúng mẫu per-friend",
      HAVE,
      "1. Quan sát tên file đã tải về",
      "—",
      "- Tên file đúng dạng `{friendId}_{startYYYYMMDD}_{endYYYYMMDD}_{tên friend}.csv`\n"
      "  (vd「1_20260504_20260604_さわみ🍓.csv」)",
      "⚠️ Phụ thuộc MT-20 + MT-21 — QA-031 chốt mẫu tên per-friend, nhưng CÁCH ĐÓNG GÓI khi xuất "
      "nhiều friend (1 file gộp hay ZIP nhiều file) reviewer CHƯA xác nhận. "
      "Nguồn: v2 r79 (TC-SC-071, Not Tested) · v1 r95 (BS_043)"),

    f("OUT-EXPORT-001", "Normal",
      "Tin xác nhận hệ thống「メッセージをご確認ください」xuất hiện như 1 dòng dữ liệu",
      HAVE + "\n- Hội thoại có tin「メッセージをご確認ください」",
      "1. Mở file CSV\n"
      "2. Tìm dòng có「内容」=「メッセージをご確認ください」",
      "—",
      "- Tin này xuất hiện như 1 dòng dữ liệu bình thường\n"
      "- Có đủ「送信者タイプ」/「送信日」/「送信時刻」",
      "BR-CSV-12. Nguồn: v2 r77 (TC-SC-069, Not Tested) · v1 r93 (BS_041)"),

    f("OUT-EXPORT-001", "Boundary",
      "Tin đã thu hồi — hiển thị「送信が取り消されたメッセージです」, không lộ nội dung gốc",
      HAVE + "\n- Hội thoại có ít nhất 1 tin đã bị thu hồi (取り消し)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin đã thu hồi\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị「送信が取り消されたメッセージです」\n"
      "- KHÔNG hiển thị nội dung gốc của tin đã thu hồi\n"
      "- Dòng vẫn có đủ「送信者タイプ」/「送信者名」/「送信日」/「送信時刻」",
      "⚠️ DỰ KIẾN FAIL — v2 r78 (TC-SC-070) ghi Kết quả thực thi = **Fail** (OBSERVED ở dòng "
      "2026/05/06 15:06:20 của file mẫu). Đây là rủi ro LỘ NỘI DUNG ĐÃ THU HỒI → ưu tiên chạy lại"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin text — hiển thị nguyên văn nội dung thật",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **text**",
      "1. Mở file CSV (UTF-8)\n"
      "2. Tìm dòng tương ứng tin nhắn text\n"
      "3. Quan sát giá trị cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng nội dung text nguyên văn của tin nhắn\n"
      "- KHÔNG bị thay bằng chuỗi mô tả cố định",
      "BR-CSV-13. Nguồn: v2 r81 (TC-SC-194)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin panel/button →「パネル/ボタンを送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **panel/button** (パネル/ボタン)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin panel/button\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「パネル/ボタンを送信しました。」\n"
      "- KHÔNG hiển thị nội dung / nhãn thật của panel/button",
      "BR-CSV-13 — tool export dùng chuỗi mô tả cố định. Nguồn: v2 r82 (TC-SC-195)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin quick reply →「クイックリプライを送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **quick reply** (クイックリプライ)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin quick reply\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「クイックリプライを送信しました。」\n"
      "- KHÔNG hiển thị nội dung thật của quick reply",
      "BR-CSV-13. Nguồn: v2 r83 (TC-SC-196)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin vị trí →「位置情報を送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **vị trí / địa chỉ** (位置情報)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin vị trí\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「位置情報を送信しました。」\n"
      "- KHÔNG hiển thị tọa độ hay địa chỉ thật",
      "BR-CSV-13. Nguồn: v2 r84 (TC-SC-197)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin ảnh →「写真を送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **ảnh** (写真)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin ảnh\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「写真を送信しました。」\n"
      "- KHÔNG hiển thị URL hay tên file ảnh thật",
      "BR-CSV-13. Nguồn: v2 r85 (TC-SC-198)"),

    f("OUT-EXPORT-001", "Boundary",
      "内容 của tin image map cũng là「写真を送信しました。」— không phân biệt với ảnh",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **image map** (イメージマップ) và có cả tin ảnh thường",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin image map\n"
      "3. So sánh giá trị「内容」với dòng của tin ảnh thường",
      "—",
      "- Cột「内容」hiển thị「写真を送信しました。」— GIỐNG HỆT tin ảnh thường\n"
      "- Tool export KHÔNG phân biệt ảnh và image map: 2 loại dùng chung 1 giá trị",
      "⚠️ BR-CSV-13 — case then chốt: đọc file CSV KHÔNG phân biệt được ảnh và image map. "
      "Nguồn: v2 r86 (TC-SC-199)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin video →「動画を送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **video** (動画)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin video\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「動画を送信しました。」\n"
      "- KHÔNG hiển thị URL hay tên file video thật",
      "BR-CSV-13. Nguồn: v2 r87 (TC-SC-200)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin audio →「音声を送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **audio** (音声)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin audio\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「音声を送信しました。」\n"
      "- KHÔNG hiển thị URL hay tên file audio thật",
      "BR-CSV-13. Nguồn: v2 r88 (TC-SC-201)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin PDF →「PDFを送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **PDF**",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin PDF\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「PDFを送信しました。」\n"
      "- KHÔNG hiển thị URL hay tên file PDF thật",
      "BR-CSV-13. Nguồn: v2 r89 (TC-SC-202)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin file khác →「ファイルを送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **file** (ファイル, khác PDF)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin file\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「ファイルを送信しました。」\n"
      "- KHÔNG hiển thị URL hay tên file thật",
      "BR-CSV-13. Nguồn: v2 r90 (TC-SC-203)"),

    f("OUT-EXPORT-001", "Normal",
      "内容 của tin sticker →「スタンプを送信しました。」",
      HAVE + "\n- Hội thoại 1:1 có tin nhắn **sticker** (スタンプ)",
      "1. Mở file CSV\n"
      "2. Tìm dòng tương ứng tin sticker\n"
      "3. Quan sát cột「内容」",
      "—",
      "- Cột「内容」hiển thị đúng「スタンプを送信しました。」\n"
      "- KHÔNG hiển thị mã sticker hay URL thật",
      "BR-CSV-13. Nguồn: v2 r91 (TC-SC-204)"),
]
