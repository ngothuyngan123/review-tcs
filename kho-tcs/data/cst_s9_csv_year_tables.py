# -*- coding: utf-8 -*-
"""FA-041 チャット設定 — Nhóm 9b: CSV export — dữ liệu theo năm.

⚠️ KIẾN TRÚC LƯU TIN NHẮN (Leader cung cấp 2026-09-22 — xem MT-26):
Lịch sử chat nằm ở **một DB riêng, mỗi năm 1 bảng**:
    messages_2020 · messages_2021 · messages_2022 · messages_2023 ·
    messages_2024 · messages_2025
Riêng năm **2026** tin nhắn vẫn nằm ở bảng **`messages_v2s`** của DB chính.

Hệ quả cho test: mỗi năm là MỘT NGUỒN DỮ LIỆU VẬT LÝ RIÊNG, hỏng độc lập với nhau
⇒ tách mỗi năm 1 TC, KHÔNG gộp thành 1 TC ma trận (nếu gộp, khi fail sẽ không biết
bảng nào hỏng). Ba case nặng nhất là các khoảng VẮT QUA ranh giới bảng, đặc biệt
khoảng 2025→2026 vì vắt qua 2 DB KHÁC NHAU.

⚠️ Spec `spec-features/admin/chat-setting/` §4.1 CHỈ khai `messages_v2s`, KHÔNG biết
6 bảng theo năm và DB riêng tồn tại → toàn bộ nhóm này `spec = Đã hỏi leader`.

⚠️ CHẶN THỰC THI: mọi năm < 2026 đều vượt 180 ngày ⇒ chỉ bot TRẢ PHÍ export được,
mà BUG-024 (MT-06) đang mở — bot trả phí vẫn bị chặn「180日以内」. Phải xử lý BUG-024
trước, hoặc dùng chính nhóm TC này làm bằng chứng bổ sung cho bug đó.
"""
from _common import tc

SEC = "CSV export — dữ liệu theo năm"
BASE = ("- Đăng nhập Admin, bot đang chọn thuộc gói TRẢ PHÍ (gói free bị chặn 180 ngày)\n"
        "- Đang ở `/basic/chat-setting` Tab 2「チャットのCSVエクスポート」sub-tab「データ作成」")
NEW = ("🆕 TC BỔ SUNG 2026-09-22 — corpus KHÔNG có TC nào theo chiều năm dữ liệu. "
       "Kiến trúc bảng theo năm do Leader cung cấp 2026-09-22 (xem MT-26). "
       "⚠️ Bị chặn bởi BUG-024 (MT-06) — bot trả phí đang bị chặn khoảng > 180 ngày. ")


def yr(year, table, db, extra=""):
    """1 TC cho 1 năm — mỗi năm 1 bảng riêng nên tách riêng, không gộp."""
    legacy = year <= 2025
    return tc(
        SEC,
        "COMPAT-LEGACY-001" if legacy else "OUT-EXPORT-001",
        "Normal",
        f"Export dữ liệu chat năm {year} — lấy đúng và đủ tin từ bảng `{table}`",
        BASE + f"\n- Bot có lịch sử chat THẬT trong năm {year} — xác nhận trước trên màn chat 1:1\n"
               f"- Đã đếm sẵn số tin của khoảng sẽ chọn để đối chiếu",
        f"1. Chọn ngày bắt đầu {year}/01/01, ngày kết thúc {year}/12/31\n"
        "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
        "3. Chờ tiến trình đạt 100%, sang sub-tab「作成履歴」và tải file CSV\n"
        "4. Mở file, đếm số dòng dữ liệu và quét toàn bộ cột「送信日」\n"
        f"5. Đối chiếu với lịch sử hiển thị trên màn chat 1:1 của cùng khoảng {year}",
        f"date_from = {year}/01/01, date_to = {year}/12/31",
        "- Job chạy xong, file tải về **CÓ dòng dữ liệu** — không phải chỉ có metadata + tiêu đề cột\n"
        f"- Số dòng khớp số tin đếm được trên màn chat 1:1 của khoảng {year}\n"
        f"- Mọi giá trị「送信日」đều nằm trong năm {year}, không lẫn tin của năm khác\n"
        "- Nội dung tin hiển thị đúng, không rỗng, không lỗi ký tự",
        env="PRODUCTION",
        spec="Đã hỏi leader",
        note=NEW + f"Nguồn dữ liệu: bảng `{table}` ({db}). {extra}"
             "⚠️ Nếu file ra RỖNG trong khi chat 1:1 vẫn hiển thị tin của năm này ⇒ BUG: "
             "CSV export không đọc tới bảng của năm đó. "
             f"Nếu bot test không có dữ liệu năm {year} thì ghi rõ KHÔNG CHẠY ĐƯỢC, "
             "không được ghi Đạt.")


S19 = [
    # ══════════ Từng bảng năm — mỗi năm 1 nguồn vật lý riêng ══════════
    yr(2020, "messages_2020", "DB lưu trữ riêng",
       "Bảng CŨ NHẤT đang tồn tại — rủi ro schema đời đầu khác các bảng sau. "),
    yr(2021, "messages_2021", "DB lưu trữ riêng"),
    yr(2022, "messages_2022", "DB lưu trữ riêng"),
    yr(2023, "messages_2023", "DB lưu trữ riêng",
       "⚠️ 2023 là năm có 2 đợt đổi hạ tầng (tab「Improve move database」09/2023 và "
       "「Tách DB sync gg」12/2023 của TCsLine_Improve chung) — ưu tiên chạy sớm. "),
    yr(2024, "messages_2024", "DB lưu trữ riêng"),
    yr(2025, "messages_2025", "DB lưu trữ riêng",
       "Bảng năm MỚI NHẤT trong DB lưu trữ — liền kề ranh giới sang `messages_v2s`. "),
    yr(2026, "messages_v2s", "DB chính",
       "⚠️ Năm HIỆN HÀNH, bảng nằm ở DB KHÁC hẳn 6 bảng trên. "),

    # ══════════ Vắt qua ranh giới bảng — vùng nặng nhất ══════════
    tc(SEC, "DATA-DB-001", "Boundary",
       "Khoảng xuất vắt qua giao thừa 2025→2026 — gộp dữ liệu từ 2 DB KHÁC NHAU",
       BASE + "\n- Bot có tin nhắn thật ở CẢ cuối 12/2025 lẫn đầu 01/2026\n"
              "- Đã đếm sẵn số tin của từng phía (phần 2025 và phần 2026)",
       "1. Chọn ngày bắt đầu 2025/12/25, ngày kết thúc 2026/01/05\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100%, tải file CSV\n"
       "4. Đếm riêng số dòng có「送信日」thuộc 2025 và số dòng thuộc 2026\n"
       "5. Đọc lần lượt từ trên xuống, kiểm thứ tự thời gian qua mốc đổi năm",
       "date_from = 2025/12/25, date_to = 2026/01/05",
       "- File chứa ĐỦ tin của CẢ 2 phía: phần 2025 (bảng `messages_2025`, DB lưu trữ)\n"
       "  và phần 2026 (bảng `messages_v2s`, DB chính)\n"
       "- Số dòng mỗi phía khớp số đã đếm trước — KHÔNG mất phía nào\n"
       "- Thứ tự thời gian tăng dần LIÊN TỤC qua mốc 2025/12/31 → 2026/01/01,\n"
       "  không có cụm tin bị dồn xuống cuối file hay đảo ngược\n"
       "- Không có dòng nào bị lặp 2 lần",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "⚠️ CASE NẶNG NHẤT của nhóm: vắt qua 2 DB khác nhau ⇒ phải gộp 2 nguồn rồi "
            "sắp xếp lại. Lỗi hay gặp: mất hẳn 1 phía, hoặc gộp được nhưng sai thứ tự vì mỗi "
            "nguồn được sắp riêng rồi nối đuôi nhau"),

    tc(SEC, "DATA-DB-001", "Boundary",
       "Khoảng xuất vắt qua giao thừa 2023→2024 — gộp 2 bảng trong cùng DB lưu trữ",
       BASE + "\n- Bot có tin nhắn thật ở CẢ cuối 12/2023 lẫn đầu 01/2024\n"
              "- Đã đếm sẵn số tin của từng phía",
       "1. Chọn ngày bắt đầu 2023/12/25, ngày kết thúc 2024/01/05\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100%, tải file CSV\n"
       "4. Đếm riêng số dòng thuộc 2023 và thuộc 2024\n"
       "5. Kiểm thứ tự thời gian qua mốc đổi năm",
       "date_from = 2023/12/25, date_to = 2024/01/05",
       "- File chứa đủ tin của cả `messages_2023` lẫn `messages_2024`\n"
       "- Số dòng mỗi phía khớp số đã đếm trước\n"
       "- Thứ tự thời gian tăng dần liên tục qua mốc đổi năm\n"
       "- Không có dòng nào bị lặp",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "Đối chứng với case 2025→2026: ở đây 2 bảng nằm CÙNG 1 DB. Nếu case này Đạt "
            "mà case 2025→2026 Không đạt ⇒ khoanh được lỗi nằm ở chỗ gộp giữa 2 DB"),

    tc(SEC, "DATA-DB-001", "Boundary",
       "Khoảng xuất trải 6 năm 2021→2026 — gộp đủ 6 bảng năm và `messages_v2s`",
       BASE + "\n- Bot có lịch sử chat thật trải đủ từ 2021 đến 2026\n"
              "- Đã đếm sẵn số tin của TỪNG NĂM để đối chiếu",
       "1. Chọn ngày bắt đầu 2021/01/01, ngày kết thúc 2026/12/31\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100%, tải file CSV\n"
       "4. Nhóm các dòng theo năm của「送信日」và đếm số dòng từng năm\n"
       "5. Đối chiếu từng năm với số đã đếm ở tiền điều kiện\n"
       "6. Kiểm thứ tự thời gian toàn file",
       "date_from = 2021/01/01, date_to = 2026/12/31",
       "- File chứa dữ liệu của ĐỦ 6 năm, KHÔNG thiếu năm nào\n"
       "- Số dòng từng năm khớp số đã đếm — không năm nào bằng 0 trong khi thực tế có tin\n"
       "- Thứ tự thời gian tăng dần xuyên suốt toàn file, không bị chia khối theo bảng\n"
       "- Job chạy xong không timeout, không lỗi",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "Kiểm gộp 7 nguồn cùng lúc (6 bảng năm + `messages_v2s` ở DB khác). "
            "Ngoài tính đúng còn là phép thử hiệu năng: đây là khoảng xuất lớn nhất có thể"),

    # ══════════ Biên & bất thường ══════════
    tc(SEC, "FUNC-DATE-001", "Boundary",
       "Khoảng xuất chứa ngày 29/02 của năm nhuận 2024",
       BASE + "\n- Bot có tin nhắn thật trong ngày 2024/02/29",
       "1. Chọn ngày bắt đầu 2024/02/25, ngày kết thúc 2024/03/05\n"
       "2. Bấm「エクスポート条件の確認に進む」→「作業開始」\n"
       "3. Chờ 100%, tải file CSV\n"
       "4. Tìm các dòng có「送信日」=「2024/02/29」",
       "date_from = 2024/02/25, date_to = 2024/03/05",
       "- Bộ chọn ngày cho chọn được 2024/02/29 (ngày có thật của năm nhuận)\n"
       "- File chứa đủ tin của ngày 2024/02/29, hiển thị đúng「2024/02/29」\n"
       "- Không có tin nào bị rơi mất ở mốc ngày nhuận",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "DI-10 boundary ngày nhuận. 2024 là năm nhuận duy nhất trong dải 2020-2026 "
            "có bảng riêng (2020 cũng nhuận — nếu bot có dữ liệu 2020/02/29 thì chạy thêm)"),

    tc(SEC, "DATA-DB-001", "Abnormal",
       "Chọn năm CHƯA có bảng dữ liệu (2019) — báo rõ hoặc trả file rỗng, KHÔNG lỗi hệ thống",
       BASE + "\n- Năm 2019 không có bảng `messages_2019` trong DB lưu trữ",
       "1. Chọn ngày bắt đầu 2019/01/01, ngày kết thúc 2019/12/31\n"
       "2. Bấm「エクスポート条件の確認に進む」\n"
       "3. Nếu cho qua thì bấm「作業開始」và chờ kết quả\n"
       "4. Quan sát trạng thái job ở sub-tab「作成履歴」",
       "date_from = 2019/01/01, date_to = 2019/12/31",
       "- Hoặc bị chặn ngay ở bước chọn ngày với thông báo rõ ràng,\n"
       "  hoặc job chạy xong và trả file chỉ có metadata + tiêu đề cột\n"
       "- TUYỆT ĐỐI không lỗi hệ thống (500 / màn trắng) do truy vấn bảng không tồn tại\n"
       "- Job không kẹt vĩnh viễn ở trạng thái「作成中」",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "Truy vấn bảng không tồn tại là lỗi hay gặp với kiến trúc 1 bảng/năm. "
            "⚠️ Hành vi đúng (chặn hay trả rỗng) CHƯA được chốt — ghi nhận thực tế rồi hỏi Leader"),

    tc(SEC, "DATA-COUNT-001", "Normal",
       "対象人数 đúng khi khoảng xuất trải nhiều năm",
       BASE + "\n- Đã biết trước số friend có phát sinh chat trong khoảng 2023→2026\n"
              "- Có friend chỉ phát sinh chat ở năm cũ và không còn chat ở năm gần đây",
       "1. Chọn ngày bắt đầu 2023/01/01, ngày kết thúc 2026/12/31\n"
       "2. Đọc giá trị「対象人数」\n"
       "3. Đối chiếu với số friend đếm tay ở màn danh sách bạn bè / chat 1:1\n"
       "4. Tạo CSV, tải file và đếm số friend thực sự có trong file",
       "date_from = 2023/01/01, date_to = 2026/12/31",
       "-「対象人数」bằng đúng số friend có phát sinh chat trong toàn khoảng,\n"
       "  tính gộp cả friend chỉ có chat ở các năm cũ\n"
       "- Số friend trong file CSV khớp với「対象人数」",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "⚠️ Chồng lên MT-23 (「対象人数」đang Fail trên production). TC này thêm chiều "
            "nhiều bảng: nếu số đếm chỉ tính `messages_v2s` thì friend cũ sẽ bị bỏ sót"),

    tc(SEC, "COMPAT-LEGACY-001", "Boundary",
       "Dữ liệu ở bảng năm cũ — 送信者タイプ và 送信者名 có bị giá trị legacy không",
       BASE + "\n- Đã tải file CSV của 1 năm cũ (2021-2023) và 1 file của năm 2026 để đối chiếu",
       "1. Mở file CSV của năm cũ, quét toàn bộ cột「送信者タイプ」và「送信者名」\n"
       "2. Mở file CSV của năm 2026, quét 2 cột tương ứng\n"
       "3. So sánh tập giá trị xuất hiện ở 2 file",
       "1 file năm cũ (2021-2023) + 1 file năm 2026",
       "- File năm cũ dùng CÙNG tập giá trị với file 2026:\n"
       " 「送信者タイプ」∈ {「友だち」,「LOAアカウント」} và「送信者名」là tên người gửi thật\n"
       "- KHÔNG xuất hiện giá trị legacy「User」/「Account」/「Unknown」ở file năm cũ",
       env="PRODUCTION", spec="Đã hỏi leader",
       note=NEW + "⚠️ Nối thẳng với MT-20: file mẫu cũ của tester hiển thị「User」/「Account」/"
            "「Unknown」. Rất có thể các giá trị legacy đó đến từ CHÍNH các bảng năm cũ ⇒ TC này "
            "khoanh được nguồn gốc của MT-20. DỰ KIẾN FAIL"),
]
