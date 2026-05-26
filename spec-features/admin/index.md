# Admin Portal — Danh sách tính năng

> Tạo bởi `/scan-admin`
> Ngày quét: 2026-03-24
> Tổng tính năng: 38

## Danh sách tính năng

| Mã | Tên tính năng | Tên JP | Phân loại | Số màn hình | URL chính | UI Scan | Web | Job | DB | Validate | Compile | Ghi chú |
|----|-------------|--------|----------|------------|----------|---------|-----|-----|----|---------|---------|----|
| FA-001 | Chat 1:1 | 「1:1チャット」 | Chat | 2 | /basic/chat-v3 | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 49 endpoints, 2 jobs, 38 tables |
| FA-002 | Quản lý chat | 「チャット管理」 | Hỗ trợ khách hàng | 3 | /basic/talk-list | XONG | XONG | — | XONG | XONG | XONG | HOÀN THÀNH — 6 endpoints, 0 jobs, 27 tables |
| FA-003 | Tự động trả lời | 「自動応答」 | Hỗ trợ khách hàng | 4 | /basic/reply | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 16 endpoints, 1 job (HandlePostbackTask), 14+ tables. Dual flow Legacy/V2. Dùng SC-003 (Filter), SC-004 (Action) |
| FA-004 | Rich Menu | 「リッチメニュー」 | Hỗ trợ khách hàng | 8 | /basic/rich-menu | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 40 endpoints, 3 jobs (UpdateRichMenuTask, SettingDisplayTask, HandleCheckTimeTask), 11 tables. Dùng SC-004 (Action) |
| FA-005 | Tạo hình ảnh Rich Menu | 「リッチメニュー画像作成」 | Hỗ trợ khách hàng | 1 | /basic/image-richmenu | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-006 | Cài đặt thông báo | 「通知設定」 | Hỗ trợ khách hàng | 1 | /basic/notify-setting | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH |
| FA-007 | Tin nhắn chào mừng | 「あいさつメッセージ」 | Tin nhắn chào mừng | 3 | /basic/setting-add-friend | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Gồm 3 trang: bạn mới, bạn cũ, unblock |
| FA-008 | Gửi tin nhắn hàng loạt | 「メッセージ配信」 | Nhắn tin | 1 | /basic/message-send-all | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 30+ endpoints, 1 job (BroadcastTask), 8+ tables. Dùng SC-003 (Filter), SC-004 (Action), SC-005 (Editor), SC-006 (Target), SC-007 (Schedule) |
| FA-009 | Phát hành theo bước | 「ステップ配信」 | Nhắn tin | 1 | /basic/scenario | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có background job gửi tin |
| FA-010 | Mẫu tin nhắn | 「テンプレート」 | Nhắn tin | 10 | /basic/message-template | XONG | XONG | — | XONG | XONG | XONG | HOÀN THÀNH — 40+ endpoints, 0 core jobs (delay message qua send_random_messages), 19 tables. Shared component SC-001. Dùng SC-004 (Action), SC-005 (Editor) |
| FA-011 | Tạo biểu mẫu | 「フォーム作成」 | Nhắn tin | 1 | /basic/form-answer | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-012 | Quản lý thẻ | 「タグ管理」 | Quản lý thông tin | 5 | /basic/tag | XONG | XONG | — | XONG | XONG | XONG | HOÀN THÀNH — Shared component |
| FA-013 | Danh sách bạn bè | 「友だちリスト」 | Quản lý thông tin | 6 | /basic/friendlist | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 35 endpoints, 2 jobs (ActionScheduleBotTask, SyncEsTask), 23 tables. Dùng SC-002 (Tag), SC-003 (Filter), SC-004 (Action) |
| FA-014 | Quản lý CSV | 「CSV管理」 | Quản lý thông tin | 1 | /basic/csv-management | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-015 | Quản lý thông tin bạn bè | 「友だち情報管理」 | Quản lý thông tin | 9 | /basic/friend-information | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 15 endpoints, 1 job (NewEventRemindTask), 18 tables. Dùng SC-004 (Action) |
| FA-016 | Lịch hẹn hành động | 「アクションスケジュール実行」 | Quản lý thông tin | 1 | /basic/action-schedules | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có scheduled task |
| FA-017 | QR Code Action | 「QRコードアクション」 | Quản lý thông tin | 1 | /basic/landing | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-018 | Popup | 「ポップアップ」 | Quản lý thông tin | 1 | /basic/popup-manager | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-019 | Đặt lịch bài học | 「レッスン予約」 | Quản lý đặt chỗ | 1 | /basic/calendar-management | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có reminder/đồng bộ |
| FA-020 | Đặt lịch salon | 「サロン・面談予約」 | Quản lý đặt chỗ | 1 | /basic/calendar-salon | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có reminder/đồng bộ |
| FA-021 | Đặt lịch sự kiện | 「イベント予約」 | Quản lý đặt chỗ | 1 | /basic/booking-event-day | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có reminder/đồng bộ |
| FA-022 | Gửi nhắc lịch | 「リマインド配信」 | Quản lý đặt chỗ | 1 | /basic/events | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | CHƯA | Có background job gửi tin |
| FA-023 | Phân tích URL | 「URL分析」 | Phân tích dữ liệu | 1 | /basic/url | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-024 | Phân tích chéo | 「クロス分析」 | Phân tích dữ liệu | 1 | /basic/cross-analysis | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-025 | Chuyển đổi | 「コンバージョン」 | Phân tích dữ liệu | 1 | /basic/conversion | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-026 | Sản phẩm đơn lẻ | 「単品商品」 | Bán hàng | 1 | /basic/sales/index | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-027 | Chương trình giới thiệu | 「エルメ紹介プログラム」 | Giới thiệu liên kết | 1 | /admin/manage-affiliate-reward | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | Level admin (không phải LOA) |
| FA-028 | Lỗi phát hành | 「配信エラー」 | Quản lý hệ thống | 1 | /basic/error-list-v2 | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-029 | Tổng hợp số phát hành | 「配信数サマリー」 | Quản lý hệ thống | 1 | /basic/line/summary-message-send | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-030 | Trang chủ | 「ホーム」 | Quản lý hệ thống | 2 | /basic/overview | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | Gồm dashboard và overview-chart |
| FA-031 | Hợp đồng và thanh toán | 「契約プラン・決済情報」 | Quản lý hệ thống | 10 | /basic/point-settings | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 38 endpoints, 7 jobs (Laravel Artisan cron: AutoPaymentJobUnivapay 5 phases, HandleBillStripe, HandleBillMaxFriend, HandleMaxFriendBot, FlowDeleteBot), 9+8 tables. Spec tại detail-contract/. Dùng Univapay + Stripe PSP. Bug phát hiện: Phase 2 continue unreachable code |
| FA-032 | Thêm tài khoản mới | 「新規アカウント追加」 | Quản lý hệ thống | 1 | /admin/bot-add | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | Chọn LOA / chọn plan |
| FA-033 | Sao chép dữ liệu | 「データコピー」 | Quản lý hệ thống | 1 | /basic/backup | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 3 endpoints, 1 job (HandleBackup — 3 threads, 35 bảng clone), 4 bảng chính (backup_history, backup_config, backup_config_dung, backup_new_id). State machine 5 trạng thái. Flow 2 bước: check code → execute copy |
| FA-034 | Liên kết hệ thống thanh toán | 「決済システム連携設定」 | Quản lý hệ thống | 3 | /basic/list-items | XONG | XONG | — | XONG | XONG | XONG | HOÀN THÀNH — 10 endpoints, 0 jobs, 1 bảng chính (s_strip_bot). 2 PSP: UnivaPay (token) + Stripe (OAuth Connect) |
| FA-035 | Quản lý nhân viên | 「スタッフ管理」 | Quản lý hệ thống | 1 | /admin/employees-management | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-036 | Trang cá nhân | 「マイページ」 | Quản lý hệ thống | 1 | /admin/setting | XONG | XONG | — | XONG | XONG | XONG | HOÀN THÀNH — 21 endpoints, 0 jobs, 11 tables. 2 phiên bản song song (legacy + Vue.js mới) |
| FA-037 | Xác thực hai yếu tố | 「ログイン時の二段階認証」 | Quản lý hệ thống | 1 | /basic/setting-two-factor | CHƯA | CHƯA | — | CHƯA | CHƯA | CHƯA | |
| FA-038 | Cài đặt kết nối LOA | 「LOA接続設定」 | Quản lý hệ thống | 4 | /admin/bot-edit | XONG | XONG | XONG | XONG | XONG | XONG | HOÀN THÀNH — 13 endpoints, 1 job (HandleCheckStatusConnectBotAndTool), 13 tables. Gồm cả trang LOA入れ替え |

## Phân loại

| Phân loại | Tên JP | Mô tả | Số tính năng |
|----------|--------|-------|-------------|
| Chat | 「1:1チャット」 | Chat trực tiếp 1:1 với bạn bè LINE | 1 |
| Hỗ trợ khách hàng | 「顧客対応」 | Quản lý chat, tự động trả lời, Rich Menu, thông báo | 5 |
| Tin nhắn chào mừng | 「あいさつメッセージ」 | Tin nhắn tự động khi thêm bạn mới, bạn cũ, unblock | 1 |
| Nhắn tin | 「メッセージ」 | Gửi tin hàng loạt, phát hành theo bước, mẫu tin nhắn, biểu mẫu | 4 |
| Quản lý thông tin | 「情報管理」 | Thẻ, danh sách bạn bè, CSV, thông tin bạn bè, lịch hẹn, QR code, popup | 7 |
| Quản lý đặt chỗ | 「予約管理」 | Đặt lịch bài học, salon, sự kiện, nhắc lịch | 4 |
| Phân tích dữ liệu | 「データ分析」 | Phân tích URL, phân tích chéo, chuyển đổi | 3 |
| Bán hàng | 「商品販売」 | Sản phẩm đơn lẻ | 1 |
| Giới thiệu liên kết | 「エルメ紹介プログラム」 | Chương trình giới thiệu Elme (affiliate) | 1 |
| Quản lý hệ thống | 「システム管理関連」 | Cài đặt hệ thống, hợp đồng, nhân viên, trang cá nhân, lỗi, xác thực, kết nối LOA | 11 |

## Cấu trúc menu

Sidebar Admin portal có 2 phần chính:

### 1. Danh sách link trực tiếp (phía trên)
Menu dạng list các URL trực tiếp, chia theo nhóm (mỗi nhóm là 1 `<list>`):
- **Nhóm 1 — Chat**: 「1:1チャット」, 「チャット設定」
- **Nhóm 2 — Hỗ trợ khách hàng**: 「チャット管理」, 「自動応答」, 「リッチメニュー」, 「リッチメニュー画像作成」, 「スマホアプリ」 (link manual), 「通知設定」
- **Nhóm 3 — Chào mừng**: 「新規友だち用」, 「既存友だち用」, 「ブロック解除友だち用」
- **Nhóm 4 — Nhắn tin**: 「メッセージ配信」, 「ステップ配信」, 「テンプレート」, 「フォーム作成」
- **Nhóm 5 — Thông tin**: 「タグ管理」, 「友だちリスト」, 「CSV管理」, 「友だち情報管理」, 「アクションスケジュール実行」, 「QRコードアクション」, 「ポップアップ」
- **Nhóm 6 — Đặt chỗ**: 「レッスン予約」, 「サロン・面談予約」, 「イベント予約」, 「リマインド配信」
- **Nhóm 7 — Phân tích**: 「URL分析」, 「クロス分析」, 「コンバージョン」
- **Nhóm 8 — Bán hàng**: (trống trong link list — chỉ có trong category menu)
- **Nhóm 9 — Giới thiệu**: 「紹介者登録」, 「紹介リンク・成約状況」 (redirect về home)
- **Nhóm 10 — Hệ thống**: 「アカウント選択」, 「チュートリアル」 (link manual), 「配信数サマリー」, 「契約プラン・決済情報」, 「見積書発行」, 「新規アカウント追加」, 「データコピー」, 「決済システム連携設定」, 「スタッフ管理」, 「マイページ」, 「ログイン時の二段階認証」
- **Nhóm 11 — LINE OA Manager**: 「クーポン」, 「ショップカード」, 「アカウント設定」, 「プロフィール」 → link đến manager.line.biz (bên ngoài)
- **Nhóm 12 — Hỗ trợ**: 「マニュアル」, 「機能改善リクエスト」 (Google Forms), 「お問合せ」 (link manual)

### 2. Menu categories (phía dưới, toggle)
Chia theo nhóm với tên tiếng Nhật:
- **「メインサービス」** (Main Services):
  - 「1:1チャット」 → chat-v3, chat-setting
  - 「顧客対応」 → talk-list, reply, rich-menu, image-richmenu, notify-setting
  - 「あいさつメッセージ」 → setting-add-friend, setting-add-friend-old, setting-add-friend-unblock
  - 「メッセージ」 → message-send-all, scenario, message-template, form-answer
  - 「情報管理」 → tag, friendlist, csv-management, friend-information, action-schedules, landing, popup-manager
  - 「予約管理」 → calendar-management, calendar-salon, booking-event-day, events
  - 「商品販売」 → sales/index
  - 「データ分析」 → url, cross-analysis, conversion
  - 「ASP管理」 → (chưa xác định trang cụ thể)
- **「エルメ紹介プログラム」** (Affiliate Program) → manage-affiliate-reward
- **「システム管理関連」** (System Management):
  - 「エルメシステム設定」 → point-settings, plan-estimation, bot-add, backup, list-items, employees-management, setting, setting-two-factor
  - 「LINE公式アカウント設定」 → link đến manager.line.biz
  - 「エラーメッセージ」 → error-list-v2
  - 「サポート」 → manual, contact
  - 「ログアウト」

## Ghi chú
- Trang `register-info-aff` và `manage-payment-status` redirect về home — cần kiểm tra lại khi có quyền truy cập khác
- Menu ngoài: 「スマホアプリ」 (link manual), 「チュートリアル」 (link manual), 「機能改善リクエスト」 (Google Forms), 「お問合せ」 (link manual)
- LINE OA Manager links: 「クーポン」, 「ショップカード」, 「アカウント設定」, 「プロフィール」 → dẫn đến manager.line.biz (bên ngoài, không thuộc LME)
- 「LOA接続設定」 (FA-038) truy cập qua nút「接続設定」trên trang「アカウント選択」(/admin/home), không có trong sidebar trực tiếp
- Category 「ASP管理」 xuất hiện trong menu category nhưng không có trang nào được quét — có thể là tính năng ẩn hoặc chưa được bật cho tài khoản này
- Category 「商品販売」 chỉ link đến `/basic/sales/index` (trang 「単品商品」) — có thể có thêm trang con khi tạo sản phẩm
- Tính năng messaging (FA-008, FA-009, FA-022) và reservation (FA-019, FA-020, FA-021) có khả năng cao dùng background jobs (gửi tin, đồng bộ, nhắc lịch)
- FA-016 Action Schedule có scheduled task nên Job = CHƯA
- FA-007 Tin nhắn chào mừng có thể dùng background job khi gửi tin nhắn chào mừng tự động
