# -*- coding: utf-8 -*-
"""Khung chung cho kho TCs tổng hợp LME — 16 cột canonical (sheet '7. Ví dụ test case').

Đánh số: TC-<PREFIX>-<nn> chạy TUẦN TỰ theo thứ tự nhóm chức năng (SECTIONS),
không đánh lại theo mã quan điểm. Tiêu đề TC luôn mang prefix [<nhóm>].
"""

COLS = [
    "ID", "Nhóm", "Mã quan điểm", "Màn hình/chức năng", "Loại case", "Tên case",
    "Tiền điều kiện", "Các bước thực hiện", "Dữ liệu nhập", "Kết quả mong đợi",
    "Kết quả thực thi", "Ghi chú",
]

# ── Cột "Nhóm" — tầng test của TC: UI / API / Data ───────────────────────────
# Suy ra TỰ ĐỘNG từ mã quan điểm (khớp theo tiền tố DÀI NHẤT trước).
#   UI   — kiểm chứng bằng mắt trên màn hình (admin hoặc LINE user)
#   API  — kiểm chứng ở tầng xử lý phía server: gửi tin, job nền, tích hợp,
#          thanh toán, phân quyền, đồng thời, hiệu năng
#   Data — kiểm chứng ở tầng dữ liệu: DB, đếm số, tham chiếu, migration, legacy
# Ghi đè từng TC bằng tham số group="..." của hàm tc().
GROUP_MAP = (
    ("OUT-PREVIEW",    "UI"),
    ("OUT-EXPORT",     "API"),
    ("OUT-TRUTH",      "API"),
    ("COMPAT-BROWSER", "UI"),
    ("COMPAT-LEGACY",  "Data"),
    ("MEDIA-CLEAN",    "Data"),
    ("DATA-",          "Data"),
    ("UI-",            "UI"),
    ("LIST-",          "UI"),
    ("STATE-",         "UI"),
    ("MEDIA-",         "UI"),
    ("LIFF-",          "UI"),
    ("FRIEND-",        "UI"),
    ("FUNC-",          "UI"),
    ("REG-",           "UI"),
    ("COMPAT-",        "UI"),
    ("MSG-",           "API"),
    ("INTG-",          "API"),
    ("JOB-",           "API"),
    ("SYNC-",          "API"),
    ("NOTI-",          "API"),
    ("OUT-",           "API"),
    ("PAY-",           "API"),
    ("SEC-",           "API"),
    ("PERM-",          "API"),
    ("CONC-",          "API"),
    ("PERF-",          "API"),
    ("BULK-",          "API"),
    ("ENV-",           "API"),
    ("DEPLOY-",        "API"),
    ("TOOL-",          "API"),
)
GROUPS = ("UI", "API", "Data")


def group_of(vp):
    """Suy nhóm (UI/API/Data) từ mã quan điểm. Không khớp tiền tố nào → 'UI'."""
    for pref, g in sorted(GROUP_MAP, key=lambda x: -len(x[0])):
        if vp.startswith(pref):
            return g
    return "UI"

# Thứ tự nhóm chức năng — quyết định thứ tự TC trong sheet và thứ tự đánh số.
# Mỗi tính năng khai báo 1 list riêng; _ORDER là hợp của tất cả (mỗi feature chỉ
# dùng section của mình nên thứ tự tương đối trong feature luôn được giữ đúng).
SECTIONS_TAG = [
    "Tạo folder", "Sửa folder", "Xóa folder", "Sắp xếp folder",
    "Tạo tag", "Edit tag", "Copy tag", "Xóa tag", "Sort tag",
    "Count người gắn tag", "Chuyển folder", "Màn list tag", "Màn tag đã xóa",
    "Action gắn tag", "Phân quyền", "Môi trường & Legacy",
]

SECTIONS_FORM = [
    "Màn list form", "Folder form", "Sort & search form", "Tạo form",
    "Copy form", "Xóa & khôi phục form", "Public & URL form",
    "Màn edit form", "Item hiển thị", "Item câu hỏi — chung",
    "Item ngày giờ", "Item radio & dropdown", "Item checkbox",
    "Item upload file", "Item remind", "Item chẩn đoán",
    "Item thường dùng", "Liên kết friend info & tag",
    "Form rẽ nhánh — page", "Form rẽ nhánh — setting rẽ nhánh",
    "Setting chung của page", "Setting action sau trả lời", "Setting remind",
    "Setting chẩn đoán", "Setting chung của form", "Countdown", "Preview form",
    "Màn kết quả trả lời", "Export CSV", "Liên kết Google Sheet",
    "Sync Google Sheet & job", "LINE user — mở form", "LINE user — nhập & submit",
    "Backup & Recover", "Form cũ & tương thích", "Giới hạn & hiệu năng",
    "Phân quyền & môi trường",
]

SECTIONS_RICHMENU = [
    "Folder richmenu", "Sort & ẩn folder", "Màn list richmenu",
    "Tìm kiếm & sắp xếp richmenu", "Tạo richmenu — modal",
    "Step 1 — Ảnh", "Step 2 — Layout vùng tap", "Step 2 — Vùng tap thủ công",
    "Step 3 — Action エルメ", "Step 3 — Action 友だち", "Step 3 — Đổi richmenu",
    "Step 3 — Stop richmenu", "Step 3 — LINE URL scheme",
    "Step 3 — Copy action giữa area", "Step 4 — Chi tiết",
    "Lưu & điều hướng 4 step", "Copy richmenu", "Xóa & khôi phục richmenu",
    "Preview action", "Setting hiển thị richmenu", "Setting stop richmenu",
    "Lịch sử hiển thị/stop", "Job hiển thị/stop", "Thống kê tap",
    "Backup & đổi bot", "Phân quyền & staff", "Richmenu cũ & recover",
]


SECTIONS_FRI = [
    "Màn list thông tin", "Tạo folder", "Sửa folder", "Xóa folder", "Sắp xếp folder",
    "Sắp xếp & chuyển folder item",
    "Tạo info — chung", "Info kiểu Lựa chọn", "Info kiểu Mô tả",
    "Info kiểu Ngày tháng — setting", "Info kiểu Điểm", "Info kiểu Ảnh & PDF",
    "Sửa info", "Copy info", "Xóa info",
    "Màn danh sách câu trả lời", "Export CSV", "Bộ đếm 回答人数",
    "Ghi giá trị từ màn admin", "Ghi giá trị từ tính năng khác",
    "Action gán friend info", "Job action ngày tháng", "Filter theo friend info",
    "Chèn giá trị vào tin nhắn", "Thông tin mặc định & địa chỉ",
    "Backup & recover", "Phân quyền & môi trường",
]


SECTIONS_SCE = [
    "Folder scenario", "Sắp xếp folder", "Màn list scenario",
    "Tìm kiếm & phân trang list", "Tạo scenario", "Sửa scenario",
    "Copy scenario", "Xóa scenario", "Chuyển folder",
    "Màn list step & phân trang", "Filter phân nhánh 配信対象",
    "配信タイミング — thêm & sửa", "Tên quản lý step", "Message trong step",
    "Template từ thư viện", "Action エルメ", "Profile người gửi",
    "Copy message & action", "一括操作", "Preview & send test step",
    "Send test 一括テスト", "Next scenario", "Bộ đếm friend",
    "Màn list friend theo scenario", "Job gửi step & is_last_step",
    "Job khi edit step đang chạy", "Chống lặp vô hạn", "Trùng line_user",
    "Backup & đổi bot", "Phân quyền & môi trường",
]


SECTIONS_BIL = [
    "Folder sản phẩm", "Màn list sản phẩm", "Filter & môi trường list",
    "Tạo/sửa 単品 — 基本設定", "Tạo/sửa 継続 — 基本設定", "Wizard 各種ページ",
    "Ảnh sản phẩm", "アクション設定", "Copy & xóa sản phẩm",
    "Màn 商品詳細 & Preview",
    "LINE user — mở trang mua", "LINE user — nhập friend info",
    "LINE user — nhập thẻ & 3D Secure", "LINE user — mua 単品",
    "LINE user — mua 継続", "Tồn kho & 購入上限",
    "LINE user — đổi thẻ", "LINE user — hủy hợp đồng",
    "Trang hoàn tất & 特商法 public",
    "Bill UnivaPay — callback & webhook", "Bill Stripe — tạo order trước",
    "Job bill định kỳ", "Job cứu đơn treo & quét kết quả",
    "Action & notify theo sự kiện", "Job monitor bill tiền",
    "Màn 販売履歴", "Hoàn tiền & hủy phía admin", "Export CSV lịch sử",
    "Thuế & hóa đơn", "各種設定 — 特商法",
    "Liên kết UnivaPay", "Liên kết Stripe", "Domain LIFF & redirect",
    "Phân quyền & môi trường",
]


SECTIONS_EBK = [
    "Màn list event", "Folder event", "Tạo & sửa event — khung",
    "Tab 開催日程 — ngày tổ chức", "Khung giờ 予約枠", "Gói コース (plan)",
    "アクション設定", "Tab 各種ページ", "Form 予約時入力項目",
    "Tab 詳細設定", "Tab 決済設定", "Copy & xóa event", "Preview & OGP",
    "LINE user — mở link & entry", "LINE user — chọn slot & plan",
    "LINE user — nhập form & quy chế", "LINE user — đặt chỗ & giới hạn số lần",
    "LINE user — đổi lịch", "LINE user — hủy", "LINE user — lịch sử booking",
    "Thanh toán — Stripe", "Thanh toán — UnivaPay", "Thanh toán — 3D Secure",
    "Hoàn tiền 返金",
    "Admin — duyệt / từ chối booking", "Admin — đặt chỗ hộ & sửa booking",
    "Admin — danh sách người tham gia", "Export CSV",
    "Đếm 定員 & use_people", "Remind リマインド", "Job nền",
    "Notify & app mobile", "Giới hạn theo gói", "Phân quyền & môi trường",
]



SECTIONS_BLP = [
    "Màn list hợp đồng — hiển thị & lọc", "Cột & trạng thái hợp đồng",
    "Sắp xếp, tìm kiếm & phân trang", "Banner cảnh báo & modal ở màn list",
    "Màn chọn plan", "Rule slot trống & bot free",
    "Xác nhận plan — mua mới", "Xác nhận plan — upgrade",
    "Nhập thẻ & 3D Secure", "Chuyển khoản — tạo & thông tin tài khoản",
    "Hủy chuyển khoản", "Detail hợp đồng — plan free",
    "Detail hợp đồng — standard/pro", "Detail hợp đồng — enterprise",
    "Đổi kỳ thanh toán", "Đổi phương thức thanh toán", "Thẻ chính & thẻ phụ",
    "Gia hạn hợp đồng", "Hủy hợp đồng & chờ hủy", "Cưỡng chế hủy & màn account đã hủy",
    "Hợp đồng lại", "Ngắt kết nối LOA & xóa account", "Lịch sử thao tác hợp đồng",
    "Lịch sử ngắt kết nối LOA", "Lịch sử thanh toán — theo năm",
    "Lịch sử thanh toán — theo tháng & lọc", "Tải lãnh thụ thư",
    "Phát hành báo giá", "Job bill định kỳ — thẻ", "Job bill định kỳ — chuyển khoản",
    "Job hủy hợp đồng & retry", "Ngày bill & expired_date",
    "Bill max friend — cảnh báo & upgrade", "Bill max friend — thanh toán & job",
    "Campaign 初月無料", "Redirect sau bill success", "Hoàn tiền",
    "Hợp đồng hết hạn ảnh hưởng tính năng", "Phân quyền & staff",
    "Môi trường & regression",
]


SECTIONS_TMT = [
    "Màn list template", "Folder template", "Sắp xếp & ẩn folder",
    "Màn list group template", "Tạo group template", "Sửa & xóa group template",
    "Sort & search template", "Chuyển folder & xóa hàng loạt", "Phân trang",
    "Màn list template con",
    "Quick test — tester", "Quick test — gửi & preview", "Preview ở các màn khác",
    "Text — soạn nội dung", "Text — insert dữ liệu", "Text — PDF & shorten URL",
    "URL redirect — preview & metadata", "URL redirect — hết hạn & action",
    "Panel/Button — chọn loại", "Panel/Button — panel & ảnh",
    "Panel/Button — tiêu đề & nội dung", "Panel/Button — nút & action",
    "Panel/Button — mã màu", "Panel/Button — LINE URL scheme",
    "Panel/Button — 詳細設定 & tap limit", "Panel/Button — action phía LINE user",
    "Button ảnh — label & title", "Quick reply",
    "Media — ảnh", "Media — image map", "Media — video & audio",
    "Sticker", "Location",
    "Template legacy & tương thích", "Delay message", "Gửi template từ màn khác",
    "Copy & Backup", "Recover dữ liệu lỗi", "App mobile", "Phân quyền & môi trường",
]


SECTIONS_RPL = [
    "Màn list — hiển thị & cột", "Folder — tạo & sửa", "Folder — xóa & cascade",
    "Folder — điều hướng & sắp xếp",
    "Bật/Tắt quy tắc", "Sắp xếp & chuyển folder quy tắc",
    "Xóa quy tắc & xóa hàng loạt", "Tìm kiếm quy tắc",
    "Form — lọc đối tượng 絞り込み", "Filter — tag & ステップ",
    "Filter — conversion & QRコード", "Filter — 友だち情報",
    "Form — 利用設定 全てのメッセージ", "Form — 利用設定 キーワード",
    "Keyword — độ dài & trim", "Keyword — trùng & đồng bộ bảng keyword",
    "Checkbox 【〇〇】には反応させない",
    "Form — スケジュール設定", "Form — số lần chạy & lưu quy tắc",
    "Copy quy tắc",
    "Action — 友だち情報", "Action — テンプレート & ステップ",
    "Action — リッチメニュー & リマインド",
    "Action — タグ/対応ステータス/ブロック/ブックマーク",
    "Action — dữ liệu gốc bị xóa", "Action — recover & đổi tên",
    "Runtime — nhận message & callback", "Runtime — match keyword & gửi action",
    "Runtime — 自動確認済み (confirm message)", "Runtime — friend bị block / ẩn",
    "Runtime — lỗi gửi & retry",
    "Backup & đổi bot", "Phân quyền & môi trường",
]

SECTIONS_CHT = [
    "Vào màn & layout 3 cột", "Filter danh sách bạn bè",
    "Modal 絞り込み — tag & trạng thái", "全て確認済みに変更",
    "Tìm kiếm bạn bè", "Danh sách bạn bè — hiển thị", "Danh sách nhóm — hiển thị",
    "Load more & chuyển hội thoại",
    "Quick action — bookmark & 対応ステータス", "Quick action — xác nhận, ẩn, block",
    "Quick action — tag & kết hợp action",
    "Profile người gửi — quản lý", "Profile người gửi — áp dụng khi gửi",
    "Header hội thoại", "対応ステータス — CRUD",
    "Gửi text & phím tắt", "Chèn friend info vào tin nhắn", "Shorten URL",
    "Gửi media", "Gửi PDF", "Gửi sticker",
    "Gửi template — chọn & preview", "Gửi template — nội dung & action",
    "Gửi multi action",
    "Reply / quote message", "Hiển thị message — media & định dạng",
    "Message hệ thống — kết bạn, block, ẩn",
    "Marker & modal chi tiết action", "Marker step, remind, broadcast, send test",
    "Đặt lịch gửi — soạn & lưu", "Đặt lịch gửi — preview & send test",
    "Đặt lịch gửi — delay & job", "Preview trước khi gửi",
    "Rightbar — 基本情報", "Rightbar — 友だち情報", "Rightbar — タグ管理",
    "Rightbar — フォーム回答", "Rightbar — メモ",
    "Group chat", "Realtime socket & typing", "Bộ đếm chưa xác nhận",
    "Lịch sử chat & bảng message", "Giới hạn plan & token",
    "Phân quyền staff & môi trường",
]

SECTIONS_BK = [
    # ── Màn hình & API (bản improve — xem MT-00) ──
    "Màn データコピー & danh sách dữ liệu", "Mã copy & phát hành lại",
    "Xác nhận mã & card tài khoản", "Modal xác nhận & bắt đầu copy",
    "Màn processing & polling", "Modal hoàn tất copy", "Tab lịch sử copy",
    "Phân quyền & plan",
    # ── Job nền & đồng thời ──
    "Job BackupBotTask & state machine", "Backup đồng thời & liên tiếp",
    # ── Dữ liệu được copy, theo từng tính năng ──
    "Copy 自動応答", "Copy リッチメニュー", "Copy ステップ配信", "Copy テンプレート",
    "Copy フォーム作成", "Copy タグ", "Copy 友だち情報",
    "Copy イベント予約 & リマインド", "Copy コンバージョン・URL・対応ステータス",
    "Copy 友だち追加時設定", "Copy アクションスケジュール", "Copy フィルタ",
    "Copy クロス分析", "Copy CSV管理",
    # ── Media, ngoại lệ, hồi quy, môi trường ──
    "Media & ảnh khi copy", "Dữ liệu KHÔNG được copy", "Hồi quy sau copy",
    "Môi trường & Legacy",
]

SECTIONS_SLN = [
    # ── Màn list & tạo calendar ──
    "Màn list calendar", "Tạo calendar — wizard", "Giới hạn theo plan",
    # ── Màn quản lý đặt lịch ──
    "Tab 本日/新着の予約", "Calendar theo ngày", "Calendar theo tuần",
    "Calendar theo tháng", "Hiển thị theo list & tab シフト",
    "Modal filter booking & shift", "リクエスト一括操作",
    "Admin thêm booking thủ công", "Modal lý do không đặt được",
    "Detail booking & lịch sử", "Booking đã xóa", "Hoàn tiền 返金",
    # ── Ca làm việc (シフト) ──
    "Ca làm việc — thêm & ghi đè", "Ca làm việc — sửa & xóa",
    "Ca làm việc — qua ngày & biên 00:00", "Ca làm việc — CSV",
    # ── コース & スタッフ ──
    "コース — list & menu", "コース — tạo/sửa/xóa",
    "スタッフ — list & tạo/sửa/xóa", "Hiển thị コース・スタッフ",
    "スタッフ自動割り当て",
    # ── 予約設定 ──
    "受付上限 — 店舗・スタッフ", "前後の空き時間",
    "予約・キャンセル メッセージ", "予約・キャンセル アクション",
    "予約の開始・締切", "1人あたりの予約上限", "予約時のお客様への質問項目",
    "リマインド — cài đặt", "リマインド — job gửi", "空き枠通知受け取り設定",
    "トップ・店舗情報・利用規約", "システムワード & 予約ページ表示設定",
    "予約ページの非表示 (filter)", "予約システムの削除",
    # ── Liên kết ngoài ──
    "Googleカレンダー連携", "Googleスプレッドシート連携",
    # ── 決済 ──
    "決済連携 — cài đặt", "決済 — thẻ & 3D Secure", "現地決済",
    # ── LINE user ──
    "LINE user — mở link & entry", "LINE user — chọn コース/スタッフ",
    "LINE user — chọn slot", "LINE user — nhập form & xác nhận",
    "LINE user — lịch sử & copy", "LINE user — hủy booking",
    # ── Đồng thời, job, môi trường ──
    "Đồng thời & verify API", "Job nền & monitor", "App mobile",
    "Phân quyền & môi trường", "Dữ liệu cũ & hồi quy",
]

SECTIONS_LSN = [
    # ── Màn list & tạo lịch ──
    "Màn list calendar", "Wizard tạo calendar", "Giới hạn theo plan",
    # ── コース ──
    "コース — list & hiển thị", "コース — tạo/sửa/xóa", "コース — action & filter riêng",
    # ── Quản lý đặt chỗ ──
    "Tab 本日/新着の予約", "Calendar theo ngày", "Calendar theo tuần",
    "Calendar theo tháng", "Calendar theo list",
    "Modal danh sách booking", "Modal filter booking", "Modal filter 受付枠",
    "リクエスト一括操作", "Admin thêm booking thủ công",
    "Detail booking & lịch sử", "Booking đã xóa", "Hoàn tiền 返金",
    # ── 受付枠 ──
    "受付枠 — thêm khung giờ", "受付枠 — sửa 定員 & xóa", "受付枠 — xóa nhiều",
    "受付枠 — CSV export/import",
    # ── 全体設定 ──
    "予約・キャンセル メッセージ", "予約・キャンセル アクション",
    "予約の開始・締切", "1人あたりの予約上限", "予約時のお客様への質問項目",
    "リマインド — cài đặt", "リマインド — job gửi & recover", "空き枠通知受け取り設定",
    "予約ページの表示設定", "予約ページの非表示 (filter)",
    "トップ・店舗情報・利用規約", "予約システムの削除", "Googleスプレッドシート連携",
    # ── 決済 ──
    "決済連携 — cài đặt", "決済 — Stripe", "決済 — UnivaPay & webhook",
    # ── LINE user ──
    "LINE user — mở link & entry", "LINE user — chọn コース",
    "LINE user — chọn 受付枠", "LINE user — nhập form & xác nhận",
    "LINE user — lịch sử & copy", "LINE user — hủy booking",
    "LINE user — キャンセル待ち",
    # ── Đồng thời, app, tích hợp, môi trường ──
    "Đồng thời & verify API", "App mobile", "Add link booking vào tin nhắn",
    "Phân quyền & môi trường",
]

SECTIONS_BC = [
    # ── Màn danh sách (SCR-BC-01) ──
    "Màn list — layout & Check UI", "Tab 配信予約 — cột & hiển thị",
    "Tab 下書き — cột & hiển thị", "Tab 配信履歴 — cột & hiển thị",
    "Sắp xếp & lọc theo thời gian", "Phân trang & số dòng hiển thị",
    # ── Tạo broadcast bước 1 (SCR-BC-02) ──
    "管理用タイトル & validate", "配信タイミング設定 — gửi ngay/đặt lịch",
    "配信日時追加 — nhiều lịch gửi", "Lưu & điều hướng bước 1",
    # ── Đăng ký tin nhắn bước 2 (SCR-BC-04/05) ──
    "メッセージ登録 — thêm/sửa/xóa", "テンプレートから追加",
    "エルメアクション — đăng ký & filter", "Ma trận đăng ký & gửi",
    "送信者名 — quản lý profile", "送信者名 — áp dụng khi gửi",
    # ── Đối tượng nhận ──
    "配信先絞込み & 再計算", "配信数 & danh sách friend đã gửi",
    # ── Preview & gửi thử ──
    "Preview — 3 tab nội dung", "Tài khoản test & quick test",
    "テスト送信 & 一括テスト送信",
    # ── Thao tác trên broadcast ──
    "Edit broadcast & rule 5 phút", "Copy broadcast", "Xóa & xóa hàng loạt",
    # ── Job nền ──
    "Job gửi & vòng đời trạng thái", "Job — quá hạn, lỗi & resume",
    "Job — action sau khi gửi",
    # ── Alert giới hạn số gửi (#36436) ──
    "配信数上限アラート — trigger & modal", "配信数上限アラート — nút thao tác",
    "配信数上限アラート — quota & job cắt vượt",
    # ── Legacy, phân quyền, môi trường ──
    "Broadcast cũ & tương thích", "Phân quyền & môi trường",
]

SECTIONS_SAF = [
    # ── Khung 3 trang (SCR-SAF-01/02/03) ──
    "Điều hướng & khung 3 trang", "Khối thông tin đầu trang", "友だち追加URL & QR",
    # ── Đăng ký tin nhắn ──
    "送信するメッセージ — nút chèn biến", "送信するメッセージ — ô nhập & bộ đếm",
    "Lưu tin nhắn & bản ghi template",
    # ── Đăng ký action (SCR-SAF-05) ──
    "Đăng ký action — 5 nút tắt", "Đăng ký action — modal & danh sách",
    "Nút 保存 & bảo vệ đổi bot",
    # ── Tab hướng dẫn test ──
    "Tab テスト方法", "ご注意事項 & link ngoài",
    # ── Chạy thật phía LINE user ──
    "Kết bạn mới — gửi tin & action", "Kết bạn cũ — gửi tin & action",
    "Hủy chặn — gửi tin & action",
    "Ưu tiên với QRコードアクション", "Thứ tự & loại action khi trùng landing",
    "Trigger hiển thị ở chat 1:1",
    # ── Job, môi trường, legacy ──
    "Job callback follow & chống trùng", "Đổi bot, recover & legacy",
    "Phân quyền & môi trường",
]

SECTIONS_FRL = [
    # ── Màn danh sách chính (SCR-FRL-01) ──
    "Màn danh sách — hiển thị", "Sắp xếp & phân trang", "Tìm kiếm theo từ khoá",
    "Lọc nâng cao 絞り込み", "Chọn friend & checkbox 全選択",
    # ── 友だち一括アクション ──
    "Bulk action — ngưỡng 200 & schedule", "Bulk action — các loại action",
    "Bulk action — trigger & profile gửi",
    "Bulk action — last message & bộ đếm 未確認", "Bulk action — lỗi & hiệu năng",
    # ── 3 màn phụ (SCR-FRL-04/05/06) ──
    "Màn 非表示中の友だち", "Màn ブロックされた友だち", "Màn ブロックした友だち",
    # ── Xoá, đồng bộ, phân quyền ──
    "Xoá bạn bè & cascade", "Đồng bộ Elasticsearch", "Phân quyền & môi trường",
]

SECTIONS = SECTIONS_TAG                       # giữ tương thích code cũ
_ALL_SECTIONS = (SECTIONS_TAG + SECTIONS_FORM + SECTIONS_RICHMENU
                 + SECTIONS_FRI + SECTIONS_SCE + SECTIONS_BIL
                 + SECTIONS_EBK + SECTIONS_BLP + SECTIONS_TMT
                 + SECTIONS_RPL + SECTIONS_CHT + SECTIONS_BK
                 + SECTIONS_SLN + SECTIONS_LSN
                 + SECTIONS_BC + SECTIONS_SAF + SECTIONS_FRL)
_ORDER = {s: i for i, s in enumerate(_ALL_SECTIONS)}


def tc(sec, vp, kind, title, pre, steps, data, expect, *, env="STAGING",
       spec="Spec ghi rõ", note="", group=None):
    """Tạo 1 record TC.

    sec   — nhóm chức năng, phải nằm trong SECTIONS. Xuất ra cột "Màn hình/chức năng".
    vp    — mã quan điểm test (checklist-lme.md). Suy ra cột "Nhóm" nếu không truyền `group`.
    kind  — Normal / Abnormal / Boundary.
    group — UI / API / Data. Bỏ trống → suy tự động bằng group_of(vp).
    env   — không còn là cột riêng; khác STAGING thì được ghép vào cột "Ghi chú".
    spec  — không còn là cột riêng; khác "Spec ghi rõ" thì được ghép vào cột "Ghi chú".
    """
    assert sec in _ORDER, f"Nhóm chức năng không hợp lệ: {sec}"
    assert group is None or group in GROUPS, f"Nhóm không hợp lệ: {group}"
    return dict(sec=sec, vp=vp, kind=kind, title=title, pre=pre, steps=steps,
                data=data, expect=expect, env=env, spec=spec, note=note,
                group=group or group_of(vp))


def _order_of(sections):
    """Bảng thứ tự nhóm. Truyền `sections` = list nhóm RIÊNG của feature để tránh
    lệch thứ tự khi tên nhóm trùng với feature khác (vd 'Sắp xếp folder')."""
    if sections is None:
        return _ORDER
    return {s: i for i, s in enumerate(sections)}


def _note_of(r):
    """Gộp Ghi chú + các thông tin không còn cột riêng (môi trường, đánh giá spec).

    Bỏ 2 cột này khỏi bảng không được làm mất RULE-08 (media/domain/job/loadbalance/
    bill tiền/race/performance BẮT BUỘC chạy PRODUCTION) và trạng thái spec.
    """
    extra = []
    if r["env"] and r["env"] != "STAGING":
        extra.append(f"Môi trường: {r['env']}")
    if r["spec"] and r["spec"] != "Spec ghi rõ":
        extra.append(f"Đánh giá spec: {r['spec']}")
    if r["note"]:
        extra.append(r["note"])
    return " · ".join(extra)


def build(records, prefix="TAG", sections=None):
    """Sắp xếp theo SECTIONS (giữ nguyên thứ tự tác giả trong cùng nhóm),
    rồi đánh số tuần tự TC-<prefix>-01, -02, ... theo đúng 12 cột của COLS.

    Tiêu đề GIỮ NGUYÊN nội dung tác giả viết; nhóm chức năng không còn được nhét
    vào tiêu đề dạng [<sec>] nữa mà nằm ở cột riêng "Màn hình/chức năng".
    """
    order = _order_of(sections)
    ordered = sorted(enumerate(records), key=lambda p: (order[p[1]["sec"]], p[0]))
    rows = []
    for i, (_, r) in enumerate(ordered, start=1):
        rows.append([
            f"TC-{prefix}-{i:02d}",
            r.get("group") or group_of(r["vp"]),
            r["vp"], r["sec"], r["kind"], r["title"],
            r["pre"], r["steps"], r["data"], r["expect"],
            "",                      # Kết quả thực thi — luôn để trống cho người test điền
            _note_of(r),
        ])
    return rows


def section_summary(records, sections=None):
    """Đếm TC theo nhóm chức năng, dùng để in bảng coverage."""
    out = {s: 0 for s in (sections if sections is not None else _ALL_SECTIONS)}
    for r in records:
        out[r["sec"]] += 1
    return out
