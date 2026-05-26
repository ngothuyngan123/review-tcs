# LME System Specification — Hướng dẫn sử dụng

> Repo này chứa bộ đặc tả kỹ thuật (specs) được reverse-engineer từ hệ thống **lme.jp** (L Message / エルメ).
> Mọi thông tin được ghi lại bằng **tiếng Việt có dấu**, text UI gốc tiếng Nhật giữ nguyên trong cặp 「」.

---

## 1. Tổng quan hệ thống LME

**LME (L Message / エルメ)** là nền tảng SaaS quản lý LINE Official Account — cho phép doanh nghiệp Nhật Bản quản lý chatbot, gửi tin nhắn hàng loạt, tự động trả lời, quản lý lịch hẹn, bán hàng, và phân tích dữ liệu trên LINE.

### Tech stack gốc

| Thành phần | Công nghệ | Mô tả |
|-----------|-----------|-------|
| Web | Laravel 5 + PHP 7.2 | Ứng dụng web chính — portal Admin, Staff, System Admin |
| Background Jobs | Spring Boot + Java 1.8 | Xử lý nền — gửi tin hàng loạt, đồng bộ LINE, thống kê |
| Database | MySQL (308 bảng) | Cơ sở dữ liệu chính |

### 3 portals (đối tượng sử dụng)

| Portal | Đối tượng | Mô tả |
|--------|----------|-------|
| System Admin | Quản trị hệ thống | Quản lý toàn bộ tài khoản, thống kê doanh thu, cấu hình hệ thống |
| Admin (LINE OA) | Doanh nghiệp | Quản lý LINE Official Account — tạo chiến dịch, chatbot, bạn bè |
| Staff | Nhân viên | Do Admin tạo, truy cập cùng giao diện Admin nhưng bị giới hạn theo role |

**Quan hệ**: System Admin → quản lý nhiều Admin → mỗi Admin tạo nhiều Staff → LINE User tương tác qua LINE app.

---

## 2. Specs bao gồm gì

Mỗi tính năng được phân tích qua 5 lớp (layers):

| Layer | File | Nội dung |
|-------|------|---------|
| **UI** | `ui/ui-spec.md` | Màn hình, layout, form fields, bảng dữ liệu, user flows |
| **API** | `web/api-spec.md` | REST endpoints, request/response params, validation, middleware |
| **Business Logic** | `web/logic-spec.md` | Controllers, models, services, business rules, side effects |
| **Background Jobs** | `job/job-spec.md` | Job classes, triggers, queue, scheduling *(chỉ khi có)* |
| **Database** | `db/db-mapping.md` | Bảng, cột, relationships, enums, field traceability |
| **Tổng hợp** | `feature-spec.md` | Kết hợp tất cả layers — **đọc file này trước** |

### Trạng thái hoàn thành

Xem [index.md](index.md) để biết tổng tiến độ. Xem [admin/index.md](admin/index.md) để biết chi tiết từng tính năng.

**Lưu ý**: 7 shared components (SC-001 → SC-007) đã được phát hiện nhưng chưa có spec riêng — xem [shared/registry.md](shared/registry.md).

---

## 3. Cấu trúc thư mục

```
features/
├── GUIDE.md                    # File này — hướng dẫn sử dụng
├── index.md                    # Tiến độ tổng — link đến từng portal
├── tools/                      # AI skills hỗ trợ đọc spec
│   ├── README.md               # Hướng dẫn cài đặt skills
│   └── read-spec*.md           # 6 skills theo vai trò
│
├── admin/                      # Specs tính năng Admin portal
│   ├── index.md                # Danh sách 37 tính năng + progress
│   └── {feature-name}/         # Mỗi tính năng 1 folder
│       ├── feature-spec.md     # ★ BẮT ĐẦU Ở ĐÂY — spec tổng hợp
│       ├── ui/
│       │   └── ui-spec.md      # Spec giao diện
│       ├── web/
│       │   ├── api-spec.md     # Spec API endpoints
│       │   └── logic-spec.md   # Spec business logic
│       ├── job/
│       │   └── job-spec.md     # Spec background jobs (tuỳ tính năng)
│       ├── db/
│       │   └── db-mapping.md   # Mapping database
│       └── _internal/          # ⚠ FILE NỘI BỘ — bỏ qua
│           ├── db-hint.md      # Dữ liệu cầu nối (dùng khi tạo spec)
│           └── validation-report.md  # Báo cáo kiểm tra chéo
│
├── system-admin/               # Specs tính năng System Admin portal
│   ├── index.md                # (chưa quét)
│   └── {feature-name}/...     # Cùng cấu trúc như admin/
│
└── shared/                     # Shared components dùng chung
    ├── registry.md             # Danh sách 7 shared components
    ├── pending-refs.md         # Tham chiếu chờ xác nhận
    └── {component-name}/
        └── shared-spec.md      # Spec shared component
```

### File nào đọc trước?

1. **`feature-spec.md`** — Luôn bắt đầu ở đây. File tổng hợp toàn bộ thông tin.
2. Đọc tiếp file chi tiết theo vai trò (xem mục 4).
3. **`_internal/`** — Bỏ qua. Đây là file trung gian dùng trong quá trình tạo spec.

---

## 4. Cách đọc specs theo vai trò

| Vai trò | Đọc theo thứ tự | Skill hỗ trợ |
|---------|-----------------|-------------|
| **Tech Lead** | `feature-spec.md` (overview, scope, cross-refs) | `/read-spec` |
| **Frontend Dev** | `feature-spec.md` → `ui/ui-spec.md` → shared components | `/read-spec-ui` |
| **Backend API Dev** | `feature-spec.md` → `web/api-spec.md` | `/read-spec-api` |
| **Backend Logic Dev** | `feature-spec.md` → `web/logic-spec.md` → `job/job-spec.md` | `/read-spec-logic` |
| **DBA / Backend DB** | `feature-spec.md` → `db/db-mapping.md` | `/read-spec-db` |
| **QA / Tester** | `feature-spec.md` → `ui/ui-spec.md` (flows) → `web/api-spec.md` (errors) | `/read-spec-test` |

---

## 5. Quy ước đọc specs

### 5.1 Hệ thống mã ID

| Prefix | Ý nghĩa | Phạm vi duy nhất | Ví dụ |
|--------|---------|------------------|-------|
| `FA-XXX` | Tính năng Admin portal | Toàn dự án | FA-001: Chat 1:1 |
| `FS-XXX` | Tính năng System Admin portal | Toàn dự án | FS-001 |
| `SC-XXX` | Shared component | Toàn dự án | SC-004: Action Settings |
| `SCR-{viết tắt}-XX` | Màn hình cụ thể | Trong tính năng | SCR-TAG-01: Danh sách tag |
| `EP-XX` | API endpoint | Trong tính năng | EP-01: GET /basic/tag |
| `BR-XX` | Business rule | Trong tính năng | BR-01: Tên tag không được trùng |

### 5.2 Ngôn ngữ

| Nội dung | Ngôn ngữ | Ví dụ |
|---------|---------|-------|
| Mô tả, ghi chú, nhận xét | Tiếng Việt có dấu | "Màn hình danh sách tag" |
| Text UI gốc của ứng dụng | Tiếng Nhật trong 「」 | 「タグ管理」,「保存」 |
| Tên file, folder | Tiếng Anh, kebab-case | `tag-management`, `broadcast-messaging` |
| Mã ID | Tiếng Anh, viết hoa | `FA-012`, `SCR-TAG-01` |
| Tên bảng, cột DB | Giữ nguyên từ schema | `tags`, `created_at` |
| Tên class, method | Giữ nguyên từ source code | `TagController@index` |

### 5.3 Mức độ tin cậy (Confidence Levels)

Mỗi thông tin trong spec có ghi mức độ tin cậy:

| Mức độ | Ý nghĩa | Nguồn xác minh |
|--------|---------|---------------|
| **Cao** | Xác nhận chính xác | Đọc trực tiếp từ source code hoặc DB schema |
| **Trung bình** | Có cơ sở hợp lý | Suy luận từ UI + code, chưa xác nhận 100% |
| **Thấp** | Phỏng đoán | Chỉ quan sát từ UI, chưa tìm thấy trong code/DB |

> Khi implement: thông tin **Thấp** cần kiểm tra lại. Thông tin **Trung bình** có thể cần xác nhận edge cases.

### 5.4 Shared Components

Một số UI/logic components xuất hiện ở nhiều tính năng khác nhau. Chúng được đăng ký trong [shared/registry.md](shared/registry.md).

Khi đọc spec một tính năng, bạn có thể gặp tham chiếu dạng `SC-004 Action Settings` — nghĩa là phần đó dùng component dùng chung, chi tiết nằm ở `shared/{component-name}/shared-spec.md` (nếu đã scan).

7 shared components hiện tại:

| Mã | Tên | Tên JP | Dùng bởi |
|----|-----|--------|----------|
| SC-001 | Template Message | 「テンプレート」 | 6 features |
| SC-002 | Tag Selector | 「タグ」 | 5 features |
| SC-003 | Friend Filter/Segment | 「絞り込み」 | 6 features |
| SC-004 | Action Settings | 「アクション設定」 | 9 features |
| SC-005 | Rich Text / Message Editor | 「メッセージ編集」 | 5 features |
| SC-006 | Delivery Target Selector | 「配信先」 | 3 features |
| SC-007 | Schedule/Timer Settings | 「配信日時」 | 5 features |

---

## 6. AI Skills hỗ trợ đọc spec

Thư mục `tools/` chứa 6 AI skills giúp đọc spec hiệu quả theo vai trò. Mỗi skill là file `.md` để Claude Code (hoặc AI agent tương tự) đọc và trình bày thông tin phù hợp.

| Skill | Dành cho | Mô tả |
|-------|----------|-------|
| `/read-spec` | Tất cả | Tổng quan tính năng, trạng thái hoàn thành, gợi ý skill tiếp |
| `/read-spec-ui` | Frontend dev | Màn hình, form fields, user flows, shared components |
| `/read-spec-api` | Backend dev | Endpoints, params, responses, validation, errors |
| `/read-spec-logic` | Backend dev | Business rules, controllers, models, services, jobs |
| `/read-spec-db` | Backend / DBA | Tables, relationships, enums, field traceability |
| `/read-spec-test` | QA / Tester | Test scenarios, error cases, edge cases, assertions |

Xem [tools/README.md](tools/README.md) để biết cách cài đặt và sử dụng trong project khác.

---

## 7. Glossary (JP → VN → EN)

### Thuật ngữ tính năng

| Tiếng Nhật | Tiếng Việt | English | Ghi chú |
|-----------|-----------|---------|---------|
| 「1:1チャット」 | Chat 1:1 | 1:1 Chat | FA-001 |
| 「チャット管理」 | Quản lý chat | Chat Management | FA-002 |
| 「自動応答」 | Tự động trả lời | Auto Reply | FA-003 |
| 「リッチメニュー」 | Rich Menu | Rich Menu | FA-004 |
| 「通知設定」 | Cài đặt thông báo | Notification Settings | FA-006 |
| 「あいさつメッセージ」 | Tin nhắn chào mừng | Greeting Message | FA-007 |
| 「メッセージ配信」 | Gửi tin nhắn hàng loạt | Broadcast Messaging | FA-008 |
| 「ステップ配信」 | Phát hành theo bước | Step Delivery | FA-009 |
| 「テンプレート」 | Mẫu tin nhắn | Message Template | FA-010, SC-001 |
| 「フォーム作成」 | Tạo biểu mẫu | Form Builder | FA-011 |
| 「タグ管理」 | Quản lý thẻ | Tag Management | FA-012 |
| 「友だちリスト」 | Danh sách bạn bè | Friend List | FA-013 |
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
| 「エルメ紹介プログラム」 | Chương trình giới thiệu | Affiliate Program | FA-027 |
| 「契約プラン・決済情報」 | Hợp đồng và thanh toán | Contract & Billing | FA-031 |
| 「スタッフ管理」 | Quản lý nhân viên | Staff Management | FA-035 |
| 「二段階認証」 | Xác thực hai yếu tố | Two-Factor Auth | FA-037 |

### Thuật ngữ chung trong UI

| Tiếng Nhật | Tiếng Việt | English |
|-----------|-----------|---------|
| 「友だち」 | Bạn bè (LINE) | LINE Friend |
| 「配信」 | Phát hành / Gửi tin | Delivery / Broadcast |
| 「絞り込み」 | Lọc / Phân nhóm | Filter / Segment |
| 「アクション」 | Hành động (tự động) | Action |
| 「タグ」 | Thẻ / Nhãn | Tag |
| 「保存」 | Lưu | Save |
| 「削除」 | Xoá | Delete |
| 「編集」 | Chỉnh sửa | Edit |
| 「新規作成」 | Tạo mới | Create New |
| 「一覧」 | Danh sách | List |
| 「設定」 | Cài đặt | Settings |
| 「未分類」 | Chưa phân loại | Uncategorized |
| 「フォルダ」 | Thư mục | Folder |
| 「並べ替え」 | Sắp xếp | Sort / Reorder |
| 「一括削除」 | Xoá hàng loạt | Bulk Delete |
| 「検索」 | Tìm kiếm | Search |
| 「人数制限」 | Giới hạn số người | User Limit |
| 「ボット」/ 「BOT」 | Bot (LINE Official Account) | Bot |
