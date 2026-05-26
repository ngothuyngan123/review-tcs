# LME System Spec — Tổng hợp tham chiếu cho review TCs

> **Mục đích**: File này là **reference spec tổng thể** của hệ thống LME (L Message / エルメ).
> Khi review TCs, thay vì paste lại toàn bộ spec vào `02-spec-reference.md`, member/Leader **trích phần liên quan** từ file này và chỉ cần ghi:
>
> ```
> Xem section: [LME-SYSTEM-SPEC.md § 3.8 — FA-008 Gửi tin nhắn hàng loạt](../../templates/LME-SYSTEM-SPEC.md#38-fa-008--gửi-tin-nhắn-hàng-loạt-メッセージ配信)
> ```
>
> **Nguồn**:
> - Thư mục [spec-features/](../spec-features/) — đặc tả reverse-engineer từ source code LME (Laravel 5 + Spring Boot + MySQL 308 tables)
> - [https://lme.jp/manual/](https://lme.jp/manual/) — manual chính thức cho end-user
>
> **Ngày tổng hợp**: 2026-04-23 — dựa trên 19 feature-spec đã hoàn thành.
>
> **Quy ước ngôn ngữ**: VI có dấu cho mô tả, JP trong 「」 cho text UI gốc, tên file/code giữ tiếng Anh.

---

## Mục lục

- [1. Tổng quan hệ thống](#1-tổng-quan-hệ-thống)
- [2. Kiến trúc & Actors](#2-kiến-trúc--actors)
- [3. Danh sách tính năng chi tiết (Admin portal)](#3-danh-sách-tính-năng-chi-tiết-admin-portal)
  - [3.1 Chat 1:1 (FA-001)](#31-fa-001--chat-11-1-1チャット)
  - [3.2 Cài đặt chat (FA-041)](#32-fa-041--cài-đặt-chat-チャット設定)
  - [3.3 Quản lý chat (FA-002)](#33-fa-002--quản-lý-chat-チャット管理)
  - [3.4 Tự động trả lời (FA-003)](#34-fa-003--tự-động-trả-lời-自動応答)
  - [3.5 Rich Menu (FA-004)](#35-fa-004--rich-menu-リッチメニュー)
  - [3.6 Cài đặt thông báo (FA-006)](#36-fa-006--cài-đặt-thông-báo-通知設定)
  - [3.7 Gửi tin nhắn hàng loạt (FA-008)](#37-fa-008--gửi-tin-nhắn-hàng-loạt-メッセージ配信)
  - [3.8 Mẫu tin nhắn (FA-010)](#38-fa-010--mẫu-tin-nhắn-テンプレート)
  - [3.9 Quản lý thẻ (FA-012)](#39-fa-012--quản-lý-thẻ-タグ管理)
  - [3.10 Danh sách bạn bè (FA-013)](#310-fa-013--danh-sách-bạn-bè-友だちリスト)
  - [3.11 Quản lý thông tin bạn bè (FA-015)](#311-fa-015--quản-lý-thông-tin-bạn-bè-友だち情報管理)
  - [3.12 Hợp đồng và thanh toán (FA-031)](#312-fa-031--hợp-đồng-và-thanh-toán-契約プラン決済情報)
  - [3.13 Sao chép dữ liệu (FA-033)](#313-fa-033--sao-chép-dữ-liệu-データコピー)
  - [3.14 Liên kết hệ thống thanh toán (FA-034)](#314-fa-034--liên-kết-hệ-thống-thanh-toán-決済システム連携設定)
  - [3.15 Trang cá nhân (FA-036)](#315-fa-036--trang-cá-nhân-マイページ)
  - [3.16 Cài đặt kết nối LOA (FA-038)](#316-fa-038--cài-đặt-kết-nối-loa-loa接続設定)
  - [3.17 Chi tiết bạn bè (FA-013/FA-038 sub)](#317--chi-tiết-bạn-bè-友だち情報詳細)
  - [3.18 Đăng ký tài khoản (FA-039)](#318-fa-039--đăng-ký-tài-khoản-アカウント登録)
  - [3.19 Đăng nhập (FA-040)](#319-fa-040--đăng-nhập-ログイン)
- [4. Các tính năng chưa có spec chi tiết](#4-các-tính-năng-chưa-có-spec-chi-tiết)
- [5. Shared Components (SC-001 → SC-007)](#5-shared-components-sc-001--sc-007)
- [6. Background Jobs toàn hệ thống](#6-background-jobs-toàn-hệ-thống)
- [7. External integrations](#7-external-integrations)
- [8. Glossary JP ↔ VI ↔ EN](#8-glossary-jp--vi--en)
- [9. Cách dùng file này khi review TCs](#9-cách-dùng-file-này-khi-review-tcs)

---

## 1. Tổng quan hệ thống

**LME (L Message / エルメ)** là nền tảng SaaS quản lý **LINE Official Account** dành cho doanh nghiệp Nhật Bản.

### Môi trường (3 server)

| Môi trường | Domain | Mục đích |
|---|---|---|
| **Production** | `step.lme.jp` | Server chính phục vụ end-user. Bug báo cáo từ khách hàng luôn ở đây. |
| **Staging** | `staging.lme.jp` | Server staging — test QA trước release. |
| **Development** | `form.watermeru.com` | Server dev — đã được dùng để scan toàn bộ spec trong [spec-features/](../spec-features/). |

> **Lưu ý cho TC**: Path URL (ví dụ `/basic/message-send-all`) **nhất quán trên cả 3 môi trường**, chỉ khác domain + data. Khi viết TC, ghi rõ **môi trường test** trong Precondition (mặc định dev → staging → production theo chiều release). Các URL tham chiếu trong file spec này được trích từ dev (`form.watermeru.com`) nhưng áp dụng được cho cả 3.

### Giá trị cốt lõi

- Quản lý chat 1:1 với LINE friends
- Gửi tin nhắn hàng loạt (broadcast) & phát hành theo bước (step delivery)
- Tự động trả lời theo keyword / filter / schedule
- Quản lý bạn bè LINE với tag, custom fields, segment
- Đặt lịch (bài học / salon / sự kiện) + reminder
- Bán hàng đơn lẻ qua LINE + tích hợp Stripe/UnivaPay
- Phân tích URL, chuyển đổi, cross-analytics
- Rich menu, popup, QR code action, form

### Manual chính thức

https://lme.jp/manual/ — chia 9 nhóm:

| # | Nhóm JP | Nhóm VN | URL |
|---|---|---|---|
| 1 | 顧客対応 | Hỗ trợ khách hàng | `/manual/category/customer_service/` |
| 2 | メッセージ | Nhắn tin | `/manual/category/message/` |
| 3 | 情報管理 | Quản lý thông tin | `/manual/category/management/` |
| 4 | 予約管理 | Đặt chỗ | `/manual/category/reserve/` |
| 5 | 販促ツール | Bán hàng | `/manual/category/promotion/` |
| 6 | データ分析 | Phân tích dữ liệu | `/manual/category/analysis/` |
| 7 | システム設定・契約 | Hệ thống & hợp đồng | `/manual/category/system_contract/` |
| 8 | その他システム関連 | Hệ thống khác | `/manual/category/other_system/` |
| 9 | 有料プラン限定 | Gói trả phí giới hạn | `/manual/category/paid/` |

---

## 2. Kiến trúc & Actors

### Tech stack

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Web portal | Laravel 5 + PHP 7.2 | Giao diện Admin/Staff/System Admin |
| Background Jobs | Spring Boot + Java 1.8 | Xử lý nền (gửi tin, đồng bộ LINE, thống kê) |
| Database | MySQL (308 bảng) | Lưu trữ chính |
| Search / Cache | Elasticsearch | Tìm kiếm bạn bè (index `bot_line_user`) |
| Storage media | Dropbox API | Ảnh/video trong template, avatar |
| Push notification | Firebase (App) + Web Push (PC) | Thông báo cho Admin |

### 3 Portals

| Portal | Đối tượng | Mô tả |
|---|---|---|
| **System Admin** | Quản trị hệ thống LME | Quản lý tài khoản, doanh thu, cấu hình |
| **Admin** | Doanh nghiệp (chủ LINE OA) | Toàn quyền trên 1 hoặc nhiều LOA |
| **Staff** | Nhân viên do Admin tạo | Cùng giao diện Admin, bị giới hạn theo `role_access` |

Quan hệ: System Admin → nhiều Admin → mỗi Admin tạo nhiều Staff → LINE User tương tác qua LINE app.

### Actor theo DB

| Actor | `users.role` | `users.level` | Đặc trưng |
|---|---|---|---|
| Super Admin | `-1` | — | Luôn phải qua 2FA |
| Admin (主管理者) | `0` | `0` | Toàn quyền |
| Admin phụ (副管理人) | `0` | `1` | Quyền tương đương Admin |
| Staff | `2` | — | Bị giới hạn theo `role_access` (phân quyền theo FA-036) |
| Affiliater | (bảng riêng `affiliaters`) | — | Guard riêng `/affiliate/*` |

---

## 3. Danh sách tính năng chi tiết (Admin portal)

> Tổng 38 tính năng theo index gốc; 19 tính năng đã có feature-spec đầy đủ được mô tả dưới đây.
> Các tính năng còn lại xem mục [§4](#4-các-tính-năng-chưa-có-spec-chi-tiết).

### 3.1 FA-001 — Chat 1:1 (「1:1チャット」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/chat-v3` |
| Controller | `Basic\ChatController` |
| Số màn hình | 2 |
| Số endpoints | 49 |
| Số bảng DB | 38 (15 primary + 23 secondary) |
| Background jobs | 2 — `ScheduleSendChatTask`, `SyncEsTask` |
| Shared components | SC-001 (Template), SC-002 (Tag), SC-004 (Action), SC-005 (Editor), SC-007 (Schedule) |
| Spec gốc | [spec-features/admin/chat-11/feature-spec.md](../spec-features/admin/chat-11/feature-spec.md) |

**Mục đích**: Chat trực tiếp 1:1 giữa Admin/Staff với từng LINE friend. Layout 3 cột: danh sách bạn bè | khung hội thoại | panel thông tin 5 tabs.

**Màn hình**:
- `SCR-CHT-01` — Chat 1:1 chính — `/basic/chat-v3`
- `SCR-CHT-02` — Cài đặt Chat — `/basic/chat-setting` (xem FA-041)

**Business rules cốt lõi (17 rules)**:
- **BR-07**: Free plan giới hạn `bots.free_send_count < 1000` tin/tháng
- **BR-08**: Nếu `confirm_message_user_send=1` → auto cập nhật unconfirm count khi gửi
- **BR-09**: Conversation có `is_blocked=1` → KHÔNG cho gửi tin
- **BR-15**: Nếu `is_shorten_url=1` → auto chuyển URL thành short URL trước khi gửi

**Loại tin nhắn hỗ trợ**: text, image (resize 1040px), video (tạo thumbnail), audio (convert M4A), PDF, sticker, template, location.

---

### 3.2 FA-041 — Cài đặt chat (「チャット設定」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/chat-setting` |
| Số màn hình | 6 tabs + 1 modal |
| Background jobs | Có — `HandlePostbackTask` (tab 2 auto-confirm) |
| Spec gốc | [spec-features/admin/chat-setting/feature-spec.md](../spec-features/admin/chat-setting/feature-spec.md) |

**Mục đích**: Cài đặt tùy chọn cho Chat 1:1 — response status, auto-confirm đã đọc, phím tắt gửi, rút gọn URL, xem trước, FAQ.

**Màn hình**:
- `SCR-CST-01` — 対応ステータス編集 — Tab 1 (CRUD status)
- `SCR-CST-02` — Modal thêm/sửa status — max 20 ký tự + color picker
- `SCR-CST-03` — Tự động đánh dấu đã đọc — Tab 2, có BG job
- `SCR-CST-04` — 送信ショートカット — Tab 3 (Shift+Enter vs Enter)
- `SCR-CST-05` — 短縮URLの利用 — Tab 4 (toggle)
- (2 tab khác — preview, FAQ)

---

### 3.3 FA-002 — Quản lý chat (「チャット管理」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/talk-list` |
| Controller | `Basic\TalkListController` |
| Số màn hình | 3 (1 trang + 2 modal) |
| Số endpoints | 6 |
| Số bảng DB | 27 |
| Background jobs | Không |
| Spec gốc | [spec-features/admin/chat-management/feature-spec.md](../spec-features/admin/chat-management/feature-spec.md) |

**Mục đích**: Giao diện tổng hợp dạng bảng (list view) để xem, tìm kiếm, lọc toàn bộ tin nhắn nhận từ friends — khác với Chat 1:1 là giao diện hội thoại từng người.

**Tính năng chính**:
- Lọc theo trạng thái (`全て` / `未確認のみ`)
- Lọc theo khoảng thời gian
- Lọc nâng cao (tag, tên, ngày thêm, step, QR code, conversion, thông tin bạn bè) — dùng SC-003
- Thay đổi trạng thái xác nhận hàng loạt

---

### 3.4 FA-003 — Tự động trả lời (「自動応答」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/reply` |
| Số màn hình | 4 |
| Số endpoints | 16 |
| Background jobs | `HandlePostbackTask` (Spring Boot) |
| Shared components | SC-003 (Filter), SC-004 (Action) |
| Spec gốc | [spec-features/admin/auto-reply/feature-spec.md](../spec-features/admin/auto-reply/feature-spec.md) |

**Mục đích**: Thiết lập quy tắc auto-reply dựa trên keyword + lịch trình + filter. Khi LINE user gửi tin match điều kiện → hệ thống tự động thực hiện action (gửi template, gán tag, chuyển step, đổi rich menu).

**Pipeline**:
```
LINE webhook → INSERT `callback_event`
  → Spring Boot `HandlePostbackTask` poll
  → Match keyword (exact/partial, AND/OR)
  → Check schedule (24/7 hoặc giờ cụ thể)
  → Check filter (11 loại điều kiện qua SC-003)
  → Execute action (10 loại qua SC-004)
```

**⚠ Dual flow — LEGACY vs V2**:
- Legacy: form POST, lưu action vào cột `auto_reply.reply_*`, filter ở bảng `filters`
- V2 (hiện hành): AJAX, action ở `t_actions`/`t_actions_detail`, filter ở `filters_v2`
- Khi review TC, **phải xác định flow nào đang được test** — code có thể trigger cả 2.

---

### 3.5 FA-004 — Rich Menu (「リッチメニュー」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/rich-menu` |
| Số màn hình | 8 |
| Số endpoints | 40 |
| Số bảng DB | 11 |
| Background jobs | 3 — `UpdateRichMenuTask`, `SettingDisplayRichMenuHistoriesTask`, `HandleCheckTimeTask` |
| Shared components | SC-004 (Action) |
| Spec gốc | [spec-features/admin/rich-menu/feature-spec.md](../spec-features/admin/rich-menu/feature-spec.md) |

**Mục đích**: Thanh menu cố định ở cuối chat LINE. Admin cấu hình ảnh + vùng tap (area) + action cho từng area.

**Flow chính**:
- CRUD rich menu, upload ảnh, cấu hình area + action (4 bước)
- Hiển thị / dừng ngay hoặc đặt lịch
- Đồng bộ với LINE Platform qua BG job
- Thống kê số lần tap theo area/ngày

**Bảng chính**: `rich_menus`, `rich_menu_items`, `richmenu_update_history`, `detail_click_richmenu`, `setting_display_rich_menu_histories`

**Màn hình tiêu biểu**:
- `SCR-RCM-01` — Danh sách — `/basic/rich-menu`
- `SCR-RCM-02` — Tạo mới (modal)
- `/basic/rich-menu/edit/{id}` — Chỉnh sửa 4 bước
- `/basic/rich-menu/setting-display/{id}` — Hiển thị/dừng

---

### 3.6 FA-006 — Cài đặt thông báo (「通知設定」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/notify-setting` |
| Controller | `Basic\NotifySettingController` (872 dòng) |
| Số màn hình | 1 |
| Số endpoints | 18 |
| Số bảng DB | 3 chính + 5 phụ |
| Background jobs | 4 services + 1 daily task |
| Spec gốc | [spec-features/admin/notify-setting/feature-spec.md](../spec-features/admin/notify-setting/feature-spec.md) |

**Mục đích**: Admin cấu hình cách nhận notification từ LME — qua App (Firebase) / ChatWork / PC Desktop (Web Push).

**Cấu hình**:
- 3 kênh: App, ChatWork, PC — bật/tắt độc lập, tần suất (realtime → 24h)
- 13 hạng mục: chat, bạn bè mới, broadcast, QR code, form, salon/lesson/event booking, bán hàng, action schedule, conversion, ASP, delivery count alert
- ChatWork: nhập room URL + API token + kiểu gửi, có test send
- PC: subscribe/unsubscribe Web Push qua browser

**Background jobs**:
- `HandlePushMessageNotifyService` — poll App notifications
- `HandlePushNotifyChatwork` — poll ChatWork
- `HandlePushNotifyPc` — poll PC
- `HandleCheckNumberOfMessagesSentCurrent` — daily 01:00 AM

---

### 3.7 FA-008 — Gửi tin nhắn hàng loạt (「メッセージ配信」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/message-send-all` |
| Số màn hình | 5 (SCR-BC-01 → SCR-BC-05) |
| Số endpoints | 30+ |
| Background jobs | Có — Spring Boot poll `broadcast` table |
| Shared components | SC-003 (Filter), SC-004 (Action), SC-005 (Editor), SC-006 (Target), SC-007 (Schedule) |
| Spec gốc | [spec-features/admin/message-send-all/feature-spec.md](../spec-features/admin/message-send-all/feature-spec.md) |

**Mục đích**: Broadcast tin nhắn đến toàn bộ hoặc 1 segment bạn bè LINE.

**Đặc điểm**:
- Gửi ngay hoặc đặt lịch (tối đa **10 lịch gửi** khác nhau cho 1 broadcast)
- Lọc đối tượng theo **11 tiêu chí** (tag, tên, ngày thêm, step status,...)
- Soạn 5 loại tin: text, panel/button (Flex), media, sticker, location
- Cấu hình profile người gửi (tên + avatar) — Staff chỉ quản lý profile của mình
- Action sau khi gửi (gán tag, trigger step, đổi rich menu)
- Preview + gửi thử trước broadcast chính thức

**Màn hình**:
- `SCR-BC-01` — Danh sách — `/basic/message-send-all`
- `SCR-BC-02` — Tạo broadcast bước 1 — `/basic/add-broadcast-v2`
- `SCR-BC-03` — Dialog lọc đối tượng (overlay)
- `SCR-BC-04` — Chỉnh sửa broadcast bước 2 — `/basic/add-broadcast-v2?broadcast_id={id}`
- `SCR-BC-05` — Soạn tin nhắn — `/basic/template-v2/add-template?...`

---

### 3.8 FA-010 — Mẫu tin nhắn (「テンプレート」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/message-template` |
| Số màn hình | 10 (SCR-TMT-01 → SCR-TMT-10) |
| Số endpoints | 40+ |
| Số bảng DB | 19 |
| Background jobs | Không core (delay message qua `send_random_messages`) |
| Shared components | **Chính là SC-001** — được dùng bởi FA-001, FA-003, FA-004, FA-007, FA-008, FA-009, FA-013, FA-015 |
| Spec gốc | [spec-features/admin/message-template/feature-spec.md](../spec-features/admin/message-template/feature-spec.md) |

**Mục đích**: Quản lý mẫu tin nhắn tái sử dụng xuyên hệ thống. **Nền tảng của toàn bộ hệ thống messaging LME.**

**5 loại template chính**:
- テキスト — text
- パネル・ボタン — Flex Message panel/button
- 画像・動画・音声 — media
- スタンプ — sticker
- 位置情報 — location

**3 loại legacy**: question, introduction, group.

**Features nổi bật**:
- Folder tổ chức
- Deep clone/copy (recursive cho group template)
- Quick test gửi đến LINE user tester
- URL redirect & tracking cho text template
- Image map cho template ảnh
- Park/Group template (container chứa nhiều template con)

---

### 3.9 FA-012 — Quản lý thẻ (「タグ管理」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/tag` |
| Controllers | `Basic\TagController` (1603 dòng) + `Api\TagController` |
| Số endpoints | ~48 |
| Bảng DB chính | `tags`, `category`, `tag_line_user` |
| Shared components | Được dùng bởi SC-002 (Tag Selector) |
| Validation | 100% pass (78/78) |
| Spec gốc | [spec-features/admin/tag-management/feature-spec.md](../spec-features/admin/tag-management/feature-spec.md) |

**Mục đích**: CRUD tag để phân nhóm bạn bè LINE + cấu hình auto-action khi gán tag.

**Tính năng**:
- CRUD tag + folder (category kind=0)
- Action tự động khi gán tag (qua SC-004)
- Giới hạn số người được gán (`action_limit_tags`)
- Import từ CSV
- Soft delete + khôi phục
- Gán/gỡ tag qua Mobile API
- Đồng bộ Elasticsearch khi thay đổi tag-user (qua `sync_elasticsearch`)

**Màn hình**: `SCR-TAG-01` (danh sách), `SCR-TAG-02` (modal tạo), `SCR-TAG-03` (edit), `SCR-TAG-04` (removed), + 1 SCR folder.

---

### 3.10 FA-013 — Danh sách bạn bè (「友だちリスト」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/friendlist` |
| Controller | `Basic\FriendlistController` (4329 dòng) |
| Số màn hình | 6 |
| Số endpoints | 35 |
| Số bảng DB | 23 (8 primary + 15 secondary) |
| Background jobs | 2 — `ActionScheduleBotTask`, `SyncEsTask` |
| Shared components | SC-002 (Tag), SC-003 (Filter), SC-004 (Action) |
| External services | Elasticsearch, LINE Messaging API, Firebase, Chatwork |
| Spec gốc | [spec-features/admin/friend-list/feature-spec.md](../spec-features/admin/friend-list/feature-spec.md) |

**Mục đích**: Tính năng TRUNG TÂM — quản lý toàn bộ LINE friends đã add bot. Kết nối với hầu hết module khác.

**Màn hình**:
- `SCR-FRL-01` — Danh sách chính — `/basic/friendlist`
- `SCR-FRL-02` — Modal lọc nâng cao
- `SCR-FRL-03` — Chi tiết bạn bè (xem §3.17)
- `SCR-FRL-04` — Bạn bè ẩn
- `SCR-FRL-05` — Bạn bè bị user block
- `SCR-FRL-06` — Bạn bè bị admin block

**Bảng dữ liệu cột chính**: `friend_add_date`, `last_message`, `line_name`, `system_display_name`, tag, scenario status, reminder status.

**Thao tác**: search, filter nâng cao, block/hide/delete, bulk action, import/export CSV.

---

### 3.11 FA-015 — Quản lý thông tin bạn bè (「友だち情報管理」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/friend-information` |
| Số màn hình | 9 |
| Số endpoints | 15 + 6 Mobile API |
| Số bảng DB | 18 (7 primary + 11 secondary) |
| Background jobs | 1 — `NewEventRemindTask` |
| Shared components | SC-004 (Action) |
| Spec gốc | [spec-features/admin/friend-information/feature-spec.md](../spec-features/admin/friend-information/feature-spec.md) |

**Mục đích**: Quản lý **custom fields** gán cho LINE friends.

**6 kiểu dữ liệu custom field**:
1. Lựa chọn (選択)
2. Mô tả (説明)
3. Ngày tháng (日付) — có action scheduling qua `NewEventRemindTask`
4. Hình ảnh (画像)
5. PDF
6. Điểm (ポイント)

**Cũng quản lý**:
- **Default fields**: tên hiển thị, SĐT, email, ngày sinh, tuổi, tỉnh/thành
- **Address fields**: mã bưu điện, quận/huyện, phường/xã, tòa nhà

**Cập nhật giá trị** từ: form, postback, landing page, Mobile API.

---

### 3.12 FA-031 — Hợp đồng và thanh toán (「契約プラン・決済情報」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/point-settings` (danh sách), `/basic/detail-contract/{id}` (chi tiết) |
| Số màn hình | 10 |
| Số endpoints | 38 |
| Số bảng DB | 17 (9 primary + 8 secondary) |
| Background jobs | **7 Laravel Artisan commands** — AutoPaymentJobUnivapay (5 phases), HandleBillStripe, HandleBillMaxFriend, HandleMaxFriendBot, FlowDeleteBot |
| External | Stripe (legacy) + UnivaPay (hiện tại) |
| Spec gốc | [spec-features/admin/detail-contract/feature-spec.md](../spec-features/admin/detail-contract/feature-spec.md) |

**Mục đích**: Tính năng **tài chính quan trọng nhất** — quản lý vòng đời hợp đồng từ đăng ký → huỷ, thanh toán tự động + thủ công, tích hợp 2 PSP.

**Scope chính**:
- Xem danh sách hợp đồng (tất cả LOA)
- Xem chi tiết + lịch sử thao tác
- Đổi kỳ thanh toán (tháng → năm, wizard 3 bước)
- Huỷ plan (11 lý do, wizard 3 bước, xác thực password)
- Ngắt kết nối LOA (xoá vĩnh viễn, xác thực email 2 bước)
- Xem lịch sử thanh toán (tải receipt)
- Đổi thẻ tín dụng (có fallback sub card)
- Tái ký + gia hạn
- Huỷ chuyển khoản (rollback)

**⚠ Known issue (đã flag trong index)**: Phase 2 AutoPaymentJobUnivapay có `continue` dẫn đến unreachable code.

---

### 3.13 FA-033 — Sao chép dữ liệu (「データコピー」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/backup` |
| Số endpoints | 3 |
| Bảng DB chính | `backup_history`, `backup_config`, `backup_config_dung`, `backup_new_id` |
| Background jobs | `HandleBackup` (3 threads, clone 35 bảng) |
| Phạm vi | Clone toàn bộ 13 loại dữ liệu giữa 2 LOA |
| State machine | 5 trạng thái |
| Spec gốc | [spec-features/admin/backup/feature-spec.md](../spec-features/admin/backup/feature-spec.md) |

**Mục đích**: Copy cấu hình từ LOA này sang LOA khác (scenario, template, tag, auto-reply, form, rich menu, event,...).

**Flow 2 bước**:
1. Web check mã code → tạo queue record
2. Spring Boot `HandleBackup` thực thi (deep copy + remap foreign keys + copy media qua Dropbox + đăng ký rich menu với LINE API)

**13 loại dữ liệu được clone**:
| # | JP | VN | Bảng chính |
|---|---|---|---|
| 1 | ステップ配信 | Scenario | `scenario`, `step_message` |
| 2 | テンプレート | Template | `template`, `image_map`, `tmp_button` |
| 3 | タグ | Tag | `tags` |
| 4 | 自動応答 | Auto-reply | `auto_reply`, `keyword` |
| 5 | フォーム作成 | Form | `form_answer`, `form_answer_page` |
| 6 | リッチメニュー | Rich menu | `rich_menus`, `rich_menu_items` |
| 7 | イベント予約 | Event booking | `b_event_detail`, `events`, `event_times` |
| (8-13) | ... | ... | ... (xem spec gốc) |

**Giới hạn**: Free plan bị block bởi JavaScript client-side (alert + redirect).

---

### 3.14 FA-034 — Liên kết hệ thống thanh toán (「決済システム連携設定」)

| Attribute | Value |
|---|---|
| URL chính | `/basic/list-items` |
| Số màn hình | 3 |
| Số endpoints | 10 |
| Bảng DB chính | `s_strip_bot` (30 cột) |
| PSP hỗ trợ | UnivaPay (JWT token manual) + Stripe (OAuth Connect) |
| Spec gốc | [spec-features/admin/payment-system-integration/feature-spec.md](../spec-features/admin/payment-system-integration/feature-spec.md) |

**Mục đích**: Cấu hình liên kết với PSP để xử lý giao dịch sản phẩm/subscription trong LME.

**2 PSP**:
| PSP | Liên kết | Phí | Đặc điểm |
|---|---|---|---|
| **UnivaPay** | Nhập App Token + Secret (JWT) cho test & production | Từ 2.8% | Đề xuất, hỗ trợ trả góp, 0 yen/tháng |
| **Stripe** | OAuth Connect flow | 3.6% | Tự động qua callback, tạo tax rates |

**2 môi trường**: test và production riêng biệt.

**Ngắt liên kết**: yêu cầu xác nhận mật khẩu.

**⚠ Security flag**: Route không có middleware `admin_access` riêng — mọi user đã login đều có thể truy cập (chỉ `getBotId()` giới hạn scope).

---

### 3.15 FA-036 — Trang cá nhân (「マイページ」)

| Attribute | Value |
|---|---|
| URL chính | `/admin/setting` (legacy) + `/admin/my-page` (Vue.js mới) |
| Số endpoints | 21 |
| Số bảng DB | 11 |
| Spec gốc | [spec-features/admin/my-page/feature-spec.md](../spec-features/admin/my-page/feature-spec.md) |

**Mục đích**: Admin/Staff quản lý thông tin tài khoản cá nhân.

**⚠ 2 phiên bản song song**:
| | Legacy | Mới (MyPage) |
|---|---|---|
| URL | `/admin/setting` | `/admin/my-page` |
| Rendering | Server-side Blade | Vue.js SPA |
| Avatar | ❌ | ✓ |
| Activity Log | ❌ | ✓ |
| Xoá tài khoản | ✓ (OTP flow) | ⚠ **Luôn return 422** (chưa hoàn thiện) |
| Validation password | 6-12 ký tự, hoa+thường+số+đặc biệt | ≥ 6 ký tự, 1 đặc biệt (lỏng hơn) |
| Đổi email | Trực tiếp hoặc OTP | **Bắt buộc** OTP 2 bước |
| Lưu dữ liệu | 1 query UPDATE | Từng API riêng cho từng trường |

**Scope**:
- Cập nhật tên, công ty, SĐT
- Đổi email (OTP 2 bước)
- Đổi password
- Upload/xoá avatar (chỉ MyPage mới)
- Xem activity log (chỉ MyPage mới)
- Xoá tài khoản (chỉ legacy hoạt động)

---

### 3.16 FA-038 — Cài đặt kết nối LOA (「LOA接続設定」)

| Attribute | Value |
|---|---|
| URL chính | `/admin/bot-edit?id={id}` (id = Hashids encoded) |
| Entry point | Từ `/admin/home` → nút「接続設定」trên dòng LOA |
| Số màn hình | 4 |
| Số endpoints | 13 |
| Số bảng DB | 13 |
| Background jobs | `HandleCheckStatusConnectBotAndTool` (daily 01:00 AM) |
| Spec gốc | [spec-features/admin/bot-edit/feature-spec.md](../spec-features/admin/bot-edit/feature-spec.md) |

**Mục đích**: Quản lý cấu hình kết nối LME ↔ LINE Platform.

**Scope**:
- Xem/chỉnh sửa tên, avatar, Channel Secret, LIFF credentials
- Kiểm tra 3 lớp: Bot Info API → Webhook URL → Webhook Active
- Quản lý LIFF App (kết nối lại khi đứt)
- Đồng bộ từ LINE Manager (lấy ảnh/tên mới nhất)
- Lấy thông tin bạn bè hiện có (verified only, async ≤ 5h)
- Thay thế LOA (không áp dụng free plan)
- Copy data giữa LOA qua mã「コピーコード」

**Staff access**: Sidebar ẩn nhưng backend **không có middleware chặn rõ ràng** — Staff có thể truy cập nếu biết URL.

---

### 3.17 — Chi tiết bạn bè (「友だち情報詳細」)

| Attribute | Value |
|---|---|
| URL | `/basic/friendlist/my_page/{id}` |
| Tách từ | FA-013 |
| Màn hình | 1 trang + 7 tabs SPA + 4 sub-pages |
| Số endpoints | 37 |
| Background jobs | Không riêng — producer ghi vào 5 queue tables |
| Spec gốc | [spec-features/admin/detail-friend/feature-spec.md](../spec-features/admin/detail-friend/feature-spec.md) |

**Mục đích**: Xem/quản lý chi tiết 1 bạn LINE (line_user × bot context).

**7 tabs**:
1. Basic info — tên LINE, ngày kết bạn, affiliater, rich menu, QR action, last message
2. Custom fields (EAV) — 9+ fields từ FA-015
3. Scenario — đang chạy + lịch sử step
4. Reminder — đang chạy + ngày kết thúc
5. Tags — folder + gắn/gỡ
6. Event bookings — lịch sử event
7. Purchase history — single + subscription
8. Form answers — lịch sử trả lời form

**Actions trên bạn**: Block / Unblock / **Delete (cascade ~30 bảng)**, save memo, edit custom field, add/remove tag, save/stop scenario manually, save rich menu, send message inline, send action.

---

### 3.18 FA-039 — Đăng ký tài khoản (「アカウント登録」)

| Attribute | Value |
|---|---|
| Entry URL | `/register_user` |
| Alias | `/register_user_v2`, `/register_user/{user_id}` (affiliate link) |
| Wizard | 3 bước |
| Background jobs | **Không** — mail chạy đồng bộ trong request |
| Spec gốc | [spec-features/admin/register-user/feature-spec.md](../spec-features/admin/register-user/feature-spec.md) |

**Mục đích**: Entry point duy nhất để doanh nghiệp tạo tài khoản LME. Public, không cần session.

**3 bước wizard**:
1. Nhập email + đồng ý T&C + (non-prod) invite code → gửi mail token 60 ký tự TTL 24h
2. Click link trong mail → điền tên, công ty, SĐT → đặt password (6-12 ký tự, 4 nhóm ký tự) → xác nhận
3. Hoàn thành: INSERT `users` (is_active=1 ngay), phân quyền 34 routes × 3 role, khởi tạo trial 30 ngày, gửi 3 mail thông báo, redirect login

**Affiliate tracking**: `ref_code` tham số URL → stored in `payment_detail_aff`.

**⚠ Legacy flow** (`/register`) vẫn tồn tại trong source nhưng không dùng bởi blade V2 hiện tại.

---

### 3.19 FA-040 — Đăng nhập (「ログイン」)

| Attribute | Value |
|---|---|
| Endpoint login | `/login` (trên cả 3 domain: `step.lme.jp`, `staging.lme.jp`, `form.watermeru.com`) |
| Số màn hình | 8 |
| Số endpoints | 27 |
| Portal | Dùng chung cho Admin / Staff / Super Admin |
| Spec gốc | [spec-features/admin/login-user/feature-spec.md](../spec-features/admin/login-user/feature-spec.md) |

**Mục đích**: Cơ chế xác thực cho mọi actor — email/password + 2FA qua email + phục hồi mật khẩu + tra email qua Channel ID/Secret.

**Màn hình**:
- `SCR-LGN-01` — Login
- `SCR-LGN-02` — Verify OTP 2FA
- `SCR-LGN-03` — Forgot password
- `SCR-LGN-04` — Password reset form
- `SCR-LGN-05` — Check user (Channel ID/Secret)
- + 3 màn hình khác (2FA setup, recovery codes, session management)

**Quy tắc**:
- Super Admin **LUÔN** phải qua 2FA (bất kể `is_two_factor_verified`)
- Staff/Admin: 2FA optional
- V1 legacy flow + V2 AJAX flow song song

**⚠ Known issue** (từ spec): V1 legacy có check `env('PASS_LOGIN')` — backdoor bypass password nếu env var set. **Cần kiểm tra trong TC security.**

---

## 4. Các tính năng chưa có spec chi tiết

Các FA dưới đây có trong index gốc nhưng chưa được scan/spec đầy đủ. Khi review TC cho các tính năng này, cần:
1. Đọc trực tiếp manual: https://lme.jp/manual/
2. Hỏi Dev trước khi viết TCs
3. Cập nhật spec này khi có thông tin mới

| Mã | Tên VI | Tên JP | URL chính | Ghi chú |
|---|---|---|---|---|
| FA-005 | Tạo hình ảnh Rich Menu | 「リッチメニュー画像作成」 | `/basic/image-richmenu` | 1 màn hình |
| FA-007 | Tin nhắn chào mừng | 「あいさつメッセージ」 | `/basic/setting-add-friend` | 3 trang: bạn mới, bạn cũ, unblock |
| FA-009 | Phát hành theo bước | 「ステップ配信」 | `/basic/scenario` | Có BG job gửi tin |
| FA-011 | Tạo biểu mẫu | 「フォーム作成」 | `/basic/form-answer` | — |
| FA-014 | Quản lý CSV | 「CSV管理」 | `/basic/csv-management` | — |
| FA-016 | Lịch hẹn hành động | 「アクションスケジュール実行」 | `/basic/action-schedules` | Có scheduled task |
| FA-017 | QR Code Action | 「QRコードアクション」 | `/basic/landing` | — |
| FA-018 | Popup | 「ポップアップ」 | `/basic/popup-manager` | — |
| FA-019 | Đặt lịch bài học | 「レッスン予約」 | `/basic/calendar-management` | Có reminder/đồng bộ |
| FA-020 | Đặt lịch salon | 「サロン・面談予約」 | `/basic/calendar-salon` | Có reminder/đồng bộ |
| FA-021 | Đặt lịch sự kiện | 「イベント予約」 | `/basic/booking-event-day` | Có reminder/đồng bộ |
| FA-022 | Gửi nhắc lịch | 「リマインド配信」 | `/basic/events` | Có BG job gửi tin |
| FA-023 | Phân tích URL | 「URL分析」 | `/basic/url` | — |
| FA-024 | Phân tích chéo | 「クロス分析」 | `/basic/cross-analysis` | — |
| FA-025 | Chuyển đổi | 「コンバージョン」 | `/basic/conversion` | — |
| FA-026 | Sản phẩm đơn lẻ | 「単品商品」 | `/basic/sales/index` | — |
| FA-027 | Chương trình giới thiệu | 「エルメ紹介プログラム」 | `/admin/manage-affiliate-reward` | Admin level |
| FA-028 | Lỗi phát hành | 「配信エラー」 | `/basic/error-list-v2` | — |
| FA-029 | Tổng hợp số phát hành | 「配信数サマリー」 | `/basic/line/summary-message-send` | — |
| FA-030 | Trang chủ | 「ホーム」 | `/basic/overview` | Dashboard + overview-chart |
| FA-032 | Thêm tài khoản mới | 「新規アカウント追加」 | `/admin/bot-add` | Chọn LOA + plan |
| FA-035 | Quản lý nhân viên | 「スタッフ管理」 | `/admin/employees-management` | — |
| FA-037 | Xác thực 2 yếu tố | 「ログイン時の二段階認証」 | `/basic/setting-two-factor` | — |

---

## 5. Shared Components (SC-001 → SC-007)

Component UI/logic dùng chung xuyên nhiều tính năng. **Bug ở 1 component → ảnh hưởng mọi feature dùng nó** → impact assessment cần chú ý.

| Mã | Tên | Tên JP | Mô tả | Dùng bởi |
|---|---|---|---|---|
| **SC-001** | Template Message | 「テンプレート」 | Mẫu tin nhắn — FA-010 là trang quản lý chính | FA-001, FA-007, FA-008, FA-009, FA-010, FA-012 |
| **SC-002** | Tag Selector | 「タグ」 | Component chọn/gán tag — FA-012 là trang quản lý | FA-001, FA-008, FA-009, FA-012, FA-013 |
| **SC-003** | Friend Filter / Segment | 「絞り込み」 | Bộ lọc bạn bè 11 tiêu chí, AND/OR logic | FA-002, FA-008, FA-009, FA-013, FA-024 |
| **SC-004** | Action Settings | 「アクション設定」 | Cấu hình action tự động (gắn tag, gửi template, chuyển step, đổi rich menu,...) — 10 loại action | FA-001, FA-003, FA-004, FA-007, FA-008, FA-009, FA-011, FA-012, FA-013, FA-015, FA-016, FA-017 |
| **SC-005** | Rich Text Editor | 「メッセージ編集」 | Soạn thảo nội dung tin (text, image, video, Flex) | FA-001, FA-007, FA-008, FA-009, FA-010 |
| **SC-006** | Delivery Target Selector | 「配信先」 | Chọn đối tượng nhận tin | FA-008, FA-009, FA-022 |
| **SC-007** | Schedule / Timer | 「配信日時」 | Cài thời gian gửi | FA-001, FA-008, FA-009, FA-016, FA-022 |

**Lưu ý review TC**:
- SC-004 được dùng ở **12 tính năng** — TC regression cần cover ít nhất 3 tính năng khác nhau khi SC-004 bị sửa.
- SC-001, SC-005 thường đi cùng nhau — TC edit template phải verify cả 2.

---

## 6. Background Jobs toàn hệ thống

| Job | Ngôn ngữ | Owner feature | Trigger | Chức năng |
|---|---|---|---|---|
| `ScheduleSendChatTask` | Spring Boot | FA-001 | Polling | Gửi scheduled chat |
| `SyncEsTask` | Spring Boot | FA-001, FA-013 | On-demand | Đồng bộ Elasticsearch |
| `HandlePostbackTask` | Spring Boot | FA-003, FA-041 | Polling `callback_event` | Match keyword → execute auto-reply action |
| `UpdateRichMenuTask` | Spring Boot | FA-004 | On change | Sync rich menu với LINE Platform |
| `SettingDisplayRichMenuHistoriesTask` | Spring Boot | FA-004 | Scheduled | Hiển thị/dừng rich menu theo lịch |
| `HandleCheckTimeTask` | Spring Boot | FA-004 | Scheduled | Kiểm tra timing |
| `HandlePushMessageNotifyService` | Spring Boot | FA-006 | Polling | Push notification App (Firebase) |
| `HandlePushNotifyChatwork` | Spring Boot | FA-006 | Polling | Push ChatWork |
| `HandlePushNotifyPc` | Spring Boot | FA-006 | Polling | Push PC (Web Push) |
| `HandleCheckNumberOfMessagesSentCurrent` | Spring Boot | FA-006 | Daily 01:00 AM | Cảnh báo delivery count |
| `BroadcastTask` (Spring Boot poll `broadcast`) | Spring Boot | FA-008 | Polling 5 phút | Gửi broadcast đến giờ |
| `ActionScheduleBotTask` | Spring Boot | FA-013 | On-demand | Bulk action trên friends |
| `NewEventRemindTask` | Spring Boot | FA-015 | Scheduled | Action theo custom field ngày tháng |
| `AutoPaymentJobUnivapay` (5 phases) | Laravel Artisan | FA-031 | Daily cron | Auto-charge UnivaPay |
| `HandleBillStripe` | Laravel Artisan | FA-031 | Daily cron | Auto-charge Stripe |
| `HandleBillMaxFriend` | Laravel Artisan | FA-031 | Scheduled | Bill dựa trên max friend |
| `HandleMaxFriendBot` | Laravel Artisan | FA-031 | Scheduled | Kiểm tra max friend |
| `FlowDeleteBot` | Laravel Artisan | FA-031 | Scheduled | Cưỡng chế delete khi quá hạn |
| `HandleBackup` (3 threads) | Spring Boot | FA-033 | On-demand | Deep copy 13 loại dữ liệu, 35 bảng |
| `HandleCheckStatusConnectBotAndTool` | Spring Boot | FA-038 | Daily 01:00 AM | Check LOA connection + refresh token |

**Lưu ý review TC**:
- Bug ở BG job thường **không thể verify chỉ qua UI** — cần kiểm tra DB trước/sau + log.
- Polling jobs có độ trễ — TC cần set `precondition` đợi đủ thời gian.

---

## 7. External integrations

| Service | Dùng cho | Tính năng liên quan |
|---|---|---|
| **LINE Messaging API** | Gửi tin, sync friend, webhook event | Hầu hết tính năng messaging |
| **LINE Platform (Bot)** | Kết nối LOA, LIFF, rich menu register | FA-004, FA-038 |
| **Elasticsearch** | Index `bot_line_user`, search friends | FA-001, FA-013 |
| **Dropbox API** | Storage media (ảnh, video, audio) | FA-010, FA-033 |
| **Firebase (FCM)** | Push notification App | FA-006 |
| **Web Push (VAPID)** | Push notification PC | FA-006 |
| **Chatwork API** | Push notification qua Chatwork | FA-006 |
| **UnivaPay** | PSP chính (subscription, thanh toán) | FA-031, FA-034 |
| **Stripe** | PSP legacy + OAuth Connect | FA-031, FA-034 |
| **Google Forms** | Feature request form | Menu support |
| **Tayori** | Support FAQ + change owner form | FA-031 |
| **MailApiService** (SMTP/HTTP) | Gửi mail verify, reset password, notify | FA-036, FA-039, FA-040 |

**Lưu ý review TC**: Bug liên quan external → TC phải có case **external timeout / error** (ví dụ LINE API 500, Stripe OAuth fail).

---

## 8. Glossary JP ↔ VI ↔ EN

### Tính năng (feature)

| JP | VI | EN | Code |
|---|---|---|---|
| 「1:1チャット」 | Chat 1:1 | 1:1 Chat | FA-001 |
| 「チャット管理」 | Quản lý chat | Chat Management | FA-002 |
| 「チャット設定」 | Cài đặt chat | Chat Settings | FA-041 |
| 「自動応答」 | Tự động trả lời | Auto Reply | FA-003 |
| 「リッチメニュー」 | Rich Menu | Rich Menu | FA-004 |
| 「通知設定」 | Cài đặt thông báo | Notification Settings | FA-006 |
| 「あいさつメッセージ」 | Tin nhắn chào mừng | Greeting Message | FA-007 |
| 「メッセージ配信」 | Gửi tin nhắn hàng loạt | Broadcast Messaging | FA-008 |
| 「ステップ配信」 | Phát hành theo bước | Step Delivery | FA-009 |
| 「テンプレート」 | Mẫu tin nhắn | Message Template | FA-010 |
| 「フォーム作成」 | Tạo biểu mẫu | Form Builder | FA-011 |
| 「タグ管理」 | Quản lý thẻ | Tag Management | FA-012 |
| 「友だちリスト」 | Danh sách bạn bè | Friend List | FA-013 |
| 「友だち情報詳細」 | Chi tiết bạn bè | Friend Detail | — |
| 「CSV管理」 | Quản lý CSV | CSV Management | FA-014 |
| 「友だち情報管理」 | Quản lý thông tin bạn bè | Friend Info Management | FA-015 |
| 「アクションスケジュール実行」 | Lịch hẹn hành động | Action Schedule | FA-016 |
| 「QRコードアクション」 | QR Code Action | QR Code Action | FA-017 |
| 「ポップアップ」 | Popup | Popup | FA-018 |
| 「レッスン予約」 | Đặt lịch bài học | Lesson Reservation | FA-019 |
| 「サロン・面談予約」 | Đặt lịch salon | Salon Reservation | FA-020 |
| 「イベント予約」 | Đặt lịch sự kiện | Event Reservation | FA-021 |
| 「リマインド配信」 | Gửi nhắc lịch | Reminder Delivery | FA-022 |
| 「URL分析」 | Phân tích URL | URL Analysis | FA-023 |
| 「クロス分析」 | Phân tích chéo | Cross Analysis | FA-024 |
| 「コンバージョン」 | Chuyển đổi | Conversion | FA-025 |
| 「単品商品」 | Sản phẩm đơn lẻ | Single Products | FA-026 |
| 「契約プラン・決済情報」 | Hợp đồng và thanh toán | Contract & Billing | FA-031 |
| 「データコピー」 | Sao chép dữ liệu | Data Copy | FA-033 |
| 「決済システム連携設定」 | Liên kết thanh toán | Payment Integration | FA-034 |
| 「スタッフ管理」 | Quản lý nhân viên | Staff Management | FA-035 |
| 「マイページ」 | Trang cá nhân | My Page | FA-036 |
| 「LOA接続設定」 | Cài đặt kết nối LOA | LOA Connection | FA-038 |
| 「アカウント登録」 | Đăng ký tài khoản | Account Registration | FA-039 |
| 「ログイン」 | Đăng nhập | Login | FA-040 |

### Thuật ngữ chung

| JP | VI | EN |
|---|---|---|
| 「友だち」 | Bạn bè (LINE) | LINE Friend |
| 「配信」 |  Gửi tin | Delivery / Broadcast |
| 「絞り込み」 | Lọc / Phân nhóm | Filter / Segment |
| 「アクション」 | Cài đặt action | Multi Action |
| 「タグ」 | Thẻ / Nhãn | Tag |
| 「保存」 | Lưu | Save |
| 「削除」 | Xoá | Delete |
| 「編集」 | Chỉnh sửa | Edit |
| 「新規作成」 | Tạo mới | Create New |
| 「一覧」 | Danh sách | List |
| 「設定」 | Cài đặt | Settings |
| 「未分類」 | Chưa phân loại | Uncategorized |
| 「フォルダ」 | Thư mục | Folder |
| 「並べ替え」 | Sắp xếp | Sort |
| 「一括削除」 | Xoá hàng loạt | Bulk Delete |
| 「検索」 | Tìm kiếm | Search |
| 「人数制限」 | Giới hạn số người | User Limit |
| 「ボット」/「BOT」 | Bot (LOA) | Bot |
| 「確認済」 | Đã xác nhận | Confirmed |
| 「未確認」 | Chưa xác nhận | Unconfirmed |
| 「主管理者」 | Admin chính | Main Admin |
| 「副管理人」 | Admin phụ | Sub Admin |
| 「スタッフ」 | Nhân viên | Staff |
| 「有料プラン」 | Gói trả phí | Paid Plan |
| 「無料プラン」 | Gói miễn phí | Free Plan |
| 「体験プラン」 | Gói trial (30 ngày) | Trial Plan |
| 「コピーコード」 | Mã copy | Copy Code |
| 「接続設定」 | Cài đặt kết nối | Connection Settings |

---

## 9. Cách dùng file này khi review TCs

### Trong file `02-spec-reference.md` của 1 review

Thay vì paste toàn bộ spec, member điền như sau:

```markdown
## Nguồn spec

| Trường | Giá trị |
|---|---|
| Tên spec | LME-SYSTEM-SPEC — § 3.7 FA-008 Gửi tin nhắn hàng loạt |
| Link spec | ../../templates/LME-SYSTEM-SPEC.md#37-fa-008... |
| Version | 2026-04-23 |
| Section liên quan | Business rules về scheduled broadcast + SC-003 filter resolve |

## Trích nội dung spec liên quan

Từ LME-SYSTEM-SPEC.md § 3.7:
> Lọc đối tượng theo 11 tiêu chí (tag, tên, ngày thêm, step status,...)
> Gửi ngay hoặc đặt lịch (tối đa 10 lịch gửi khác nhau)

Từ LME-SYSTEM-SPEC.md § 5 (SC-003):
> Friend Filter/Segment — bộ lọc 11 tiêu chí, AND/OR logic

## Business rules liên quan

- BR-01: (trích từ spec-features/admin/message-send-all/feature-spec.md)
- ...
```

### Checklist khi trích spec cho review

- [ ] Đã xác định đúng tính năng trong danh sách §3 hoặc §4
- [ ] Đã đọc section Business rules trong spec gốc (`spec-features/<feature>/feature-spec.md`)
- [ ] Đã check các **shared components** mà tính năng dùng (§5) — nếu bug ảnh hưởng SC, impact rộng hơn
- [ ] Đã check các **background jobs** liên quan (§6) — nếu có, TC cần cover cả timing
- [ ] Đã check **external integrations** (§7) — nếu có, TC cần case timeout/error
- [ ] Đã note các **known issues** được flag trong spec gốc (search: `⚠`)

### Khi tính năng chưa có spec chi tiết (§4)

1. Đọc manual LME: https://lme.jp/manual/category/{nhóm}/
2. Ghi link manual vào `02-spec-reference.md` làm "spec tạm"
3. Hỏi Dev để confirm business rules trước khi member viết TCs
4. Sau khi review xong, **cập nhật mục §3 của file này** để lần sau không phải lặp lại

### Khi phát hiện spec trong file này bị lỗi thời

File này được tổng hợp ngày 2026-04-23. Nếu phát hiện sai/thiếu khi review:
1. Ghi vào `05-review-report.md` mục "Spec update needed"
2. Cập nhật file này (section tương ứng) — không phải toàn bộ spec gốc
3. Tăng version ở phần đầu file

---

_File được tổng hợp từ 19 feature-spec đã hoàn thành trong [spec-features/admin/](../spec-features/admin/) và manual https://lme.jp/manual/. Các tính năng chưa scan (§4) sẽ được bổ sung khi có spec._
