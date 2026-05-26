# [FA-015] Quản lý thông tin bạn bè — UI Spec

## Tổng quan
- **Mã tính năng**: FA-015
- **Tên**: Quản lý thông tin bạn bè
- **Tên JP**: 「友だち情報管理」
- **Mô tả**: Quản lý các trường thông tin tuỳ chỉnh (custom fields) gắn với bạn bè LINE. Admin có thể tạo các trường thông tin với 6 kiểu dữ liệu khác nhau (lựa chọn, mô tả, ngày tháng, hình ảnh, PDF, điểm), tổ chức theo folder, và cấu hình hành động tự động khi giá trị thay đổi.
- **Portal**: Admin
- **URL pattern**: `/basic/friend-information`, `/basic/friend-information/{id}`, `/basic/friend-information/add`, `/basic/friend-information/item/{id}`

## Đối tượng sử dụng (Actors)
| Actor | Vai trò | Quyền truy cập |
|-------|---------|----------------|
| Admin | Quản lý toàn bộ thông tin bạn bè: tạo/sửa/xoá trường thông tin, quản lý folder, xem danh sách câu trả lời | Toàn quyền |
| Staff | Truy cập theo phân quyền custom role | Tuỳ role — có thể bị giới hạn quyền tạo/sửa/xoá |

## Các màn hình

### SCR-FRI-01: Danh sách thông tin bạn bè
- **URL**: `/basic/friend-information`
- **Tiêu đề trang**: 「友だち情報管理」
- **Screenshot**: `screenshots/main.png`

#### Layout tổng thể
Chia 2 panel:
- **Panel trái**: Cây thư mục (Folder tree) — chiếm ~25% chiều rộng
- **Panel phải**: Bảng danh sách thông tin bạn bè + thanh công cụ — chiếm ~75% chiều rộng

Phía trên có mô tả tính năng: 「友だち情報のページや1:1チャットに表示させる情報を追加で登録することができます。」

#### Panel trái — Cây thư mục (「フォルダ」)

| Vị trí | Element | Text JP | Loại | Hành vi |
|--------|---------|---------|------|---------|
| Header | Label | 「フォルダ」 | Text | Tiêu đề panel |
| Header | Icon (+) | — | Icon button | Mở popup tạo folder mới (SCR-FRI-07) |
| Header | Icon (pencil) | — | Icon button | Bật chế độ chỉnh sửa folder |
| Body | Folder item | 「{tên folder} ({số lượng})」 | Clickable item | Click để lọc bảng theo folder. Hiển thị tên folder và số lượng item trong ngoặc |

Danh sách folder quan sát được:
- 「未分類」(28) — folder mặc định, không thể xoá
- 「基本情報」(4)
- 「国内住所」(5)
- 「thanh test」(6)
- 「select」(0)
- 「友だち情報 Ngan test」(13)
- 「test file」(2)
- 「test_1」(8)
- 「test」(4)
- 「test_1506」(2)

#### Panel phải — Thanh công cụ (Action Bar)
| Vị trí | Element | Text JP | Loại | Hành vi |
|--------|---------|---------|------|---------|
| Trái | Button | 「新規作成」 | Button chính | Navigate đến form tạo mới (SCR-FRI-02) |
| Phải | Link | 「並べ替え」 | Link | Chuyển sang chế độ sắp xếp lại thứ tự hiển thị |
| Phải | Button | 「一括フォルダ変更」 | Button | Thay đổi folder cho các item đã chọn (cần chọn checkbox) |
| Phải | Button | 「一括削除」 | Button | Xoá hàng loạt các item đã chọn (cần chọn checkbox) |

#### Panel phải — Bảng dữ liệu
| # | Cột | Text JP | Kiểu dữ liệu | Sortable? | Ghi chú |
|---|-----|---------|-------------|----------|---------|
| 0 | Checkbox | — | Checkbox | Không | Chọn item cho thao tác hàng loạt. Header có checkbox chọn tất cả |
| 1 | Ngày tạo | 「作成日」 | Date (YYYY.MM.DD) | Không rõ | Format: 2025.03.07 |
| 2 | Tên quản lý | 「管理名」 | Link text | Không rõ | Click → navigate đến form chỉnh sửa `/basic/friend-information/{id}` |
| 3 | Kiểu thông tin | 「情報タイプ」 | Text (Enum) | Không rõ | Giá trị: 「選択肢」「記述」「年月日」「画像」「PDF」「ポイント」 |
| 4 | Số người trả lời | 「回答人数」 | Link number | Không rõ | Format: "{N}人". Click → navigate đến danh sách câu trả lời `/basic/friend-information/item/{id}` |
| 5 | Menu | — | Icon button (⋯) | Không | Menu ngữ cảnh (suy luận: chỉnh sửa, xoá) |

Dữ liệu mẫu quan sát:

| 作成日 | 管理名 | 情報タイプ | 回答人数 |
|--------|--------|-----------|---------|
| 2025.03.07 | Type Point_EDIT | ポイント | 2人 |
| 2025.03.07 | Type Select_EDIT | 選択肢 | 2人 |
| 2025.01.14 | test release EDIT | 選択肢 | 0人 |
| 2024.10.16 | test act EDIT 16.10 | 年月日 | 2人 |
| 2025.02.07 | date time | 年月日 | 0人 |
| 2026.02.10 | chọn 1 | 選択肢 | 0人 |
| 2025.03.24 | test info select | 選択肢 | 0人 |

---

### SCR-FRI-02: Form tạo/chỉnh sửa — Kiểu「選択肢」(Lựa chọn)
- **URL tạo mới**: `/basic/friend-information/add?folderId={folderId}`
- **URL chỉnh sửa**: `/basic/friend-information/{id}`
- **Tiêu đề trang**: 「友だち情報作成」
- **Screenshot**: `screenshots/create-form.png` (tạo mới), `screenshots/edit-sentakushi.png` (chỉnh sửa)

#### Form fields — Phần chung (chung cho mọi kiểu thông tin)
| # | Label JP | Loại input | Bắt buộc? | Giá trị mặc định | Ghi chú |
|---|---------|-----------|----------|-----------------|---------|
| 1 | 「友だち情報（管理名）」 | Textbox | Có | Trống | Tối đa 20 ký tự. Hiển thị đếm ký tự: "{N}/20文字" |
| 2 | 「フォルダ」 | Dropdown (combobox) | Có | 「未分類」 | Chọn folder chứa item. Options = danh sách folder đã tạo |
| 3 | 「情報タイプ選択」 | Dropdown (combobox) | Có | 「選択肢」 | **Không thể thay đổi sau khi lưu** (disabled ở chế độ edit). Ghi chú: 「※保存後の変更不可」. 6 options: 「選択肢」「記述」「年月日」「画像」「PDF」「ポイント」 |

#### Phần riêng kiểu「選択肢」 — Mục「選択肢・アクション」

**Cấu hình chung:**
| # | Element | Text JP | Loại | Ghi chú |
|---|---------|---------|------|---------|
| 1 | Button | 「追加」 | Button | Thêm một dòng lựa chọn mới vào bảng |
| 2 | Radio group — 「稼働設定」 | 「一度のみ」/「何度でも稼働」 | Radio | Mặc định: 「一度のみ」. Xác định action trigger 1 lần hay nhiều lần |

**Bảng lựa chọn:**
| # | Cột | Text JP | Kiểu | Ghi chú |
|---|-----|---------|------|---------|
| 1 | Tên lựa chọn | 「選択肢」 | Textbox | Nhập tên tuỳ ý |
| 2 | Cài đặt hành động | 「アクション設定」 | Button「設定する」 | Click mở dialog Action Settings (SCR-FRI-06, SC-004) |
| 3 | Controls | — | Icon buttons | 3 icon: di chuyển lên, di chuyển xuống, xoá |

Dữ liệu mẫu (edit mode): "Point 1 diem", "Point 2 diem", "Point 0"

**Nút cuối form:**
| Element | Text JP | Loại | Hành vi |
|---------|---------|------|---------|
| Button | 「保存」 | Button chính | Lưu thông tin bạn bè. Tạo mới hoặc cập nhật tuỳ context |

---

### SCR-FRI-03: Form tạo/chỉnh sửa — Kiểu「記述」(Mô tả văn bản)
- **URL chỉnh sửa**: `/basic/friend-information/{id}`
- **Tiêu đề trang**: 「友だち情報作成」
- **Screenshot**: `screenshots/edit-kijutsu.png`

#### Form fields
Chỉ gồm phần chung (3 fields: 管理名, フォルダ, 情報タイプ) + nút「保存」.

**Không có phần cấu hình action riêng.** Kiểu「記述」chỉ lưu giá trị text tự do, không trigger action.

---

### SCR-FRI-04: Form tạo/chỉnh sửa — Kiểu「年月日」(Ngày tháng)
- **URL tạo mới**: `/basic/friend-information/add?folderId={folderId}` (chọn type 年月日)
- **URL chỉnh sửa**: `/basic/friend-information/{id}`
- **Tiêu đề trang**: 「友だち情報作成」
- **Screenshot**: `screenshots/create-form-nengappi.png` (tạo mới), `screenshots/edit-nengappi.png` (chỉnh sửa)

#### Phần riêng kiểu「年月日」— Mục「アクション設定」

**Lưu ý quan trọng (hiển thị trên UI):**
- 「登録「月日」を選択した場合、毎年その月日にアクションが稼働します。」 (Nếu chọn "Tháng/Ngày", action sẽ chạy hàng năm vào ngày đó)
- 「登録「年月日」を選択した場合、1度しかアクションは稼働しません。」 (Nếu chọn "Năm/Tháng/Ngày", action chỉ chạy 1 lần)

**Cấu hình action theo lịch:**
| # | Element | Text JP | Loại | Ghi chú |
|---|---------|---------|------|---------|
| 1 | Button | 「追加」 | Button | Thêm một dòng action scheduling mới |
| 2 | Dropdown — 「登録」 | 「月日」/「年月日」 | Combobox | Chọn kiểu ngày: chỉ tháng-ngày (lặp hàng năm) hoặc năm-tháng-ngày (1 lần) |
| 3 | Spinbutton — 「から {N} 日」 | — | Spinbutton | Số ngày offset từ ngày đăng ký |
| 4 | Dropdown — 「前」/「後」 | — | Combobox | Trước hoặc sau ngày đăng ký |
| 5 | Textbox — thời gian | — | Textbox | Format: "HH:mm" (vd: "16:40") |

**Danh sách action đã cấu hình (edit mode):**
Hiển thị dạng list, mỗi dòng gồm:
- Mô tả action: vd 「【テキスト】 test action date」
- Link「編集」→ mở dialog chỉnh sửa action (SC-004)
- Icon xoá

---

### SCR-FRI-05: Form tạo/chỉnh sửa — Kiểu「ポイント」(Điểm)
- **URL tạo mới**: `/basic/friend-information/add?folderId={folderId}` (chọn type ポイント)
- **URL chỉnh sửa**: `/basic/friend-information/{id}`
- **Tiêu đề trang**: 「友だち情報作成」
- **Screenshot**: `screenshots/create-form-point.png` (tạo mới), `screenshots/edit-point.png` (chỉnh sửa)

#### Phần riêng kiểu「ポイント」— Mục「ポイント到達時アクション」

| # | Element | Text JP | Loại | Ghi chú |
|---|---------|---------|------|---------|
| 1 | Button | 「追加」 | Button | Thêm một dòng action khi đạt ngưỡng điểm |
| 2 | Radio group — 「稼働設定」 | 「一度のみ」/「何度でも稼働」 | Radio | Mặc định: 「一度のみ」. Xác định action trigger 1 lần hay nhiều lần khi đạt ngưỡng |

**Lưu ý**: Form tạo mới và edit đều hiển thị cùng cấu trúc. Chưa quan sát được cấu hình chi tiết ngưỡng điểm (threshold) — có thể xuất hiện khi thêm dòng action.

---

### SCR-FRI-06: Dialog cài đặt hành động (Action Settings)
- **Loại**: Modal dialog
- **Tiêu đề**: 「アクション」
- **Screenshot**: `screenshots/action-settings-dialog.png`
- **Shared Component**: **SC-004** (Action Settings) — xác nhận dùng cùng component với FA-003, FA-012, FA-013

#### Nội dung dialog
10 loại action, hiển thị dạng button grid:

| # | Action | Text JP | Icon |
|---|--------|---------|------|
| 1 | Step delivery | 「ステップ」 | Có |
| 2 | Template message | 「テンプレート」 | Có |
| 3 | Text message | 「テキスト」 | Có |
| 4 | Reminder | 「リマインド」 | Có |
| 5 | Tag | 「タグ」 | Có |
| 6 | Rich Menu | 「リッチメニュー」 | Có |
| 7 | Bookmark | 「ブックマーク」 | Có |
| 8 | Friend Info | 「友だち情報」 | Có |
| 9 | Status | 「対応ステータス」 | Có |
| 10 | Block | 「ブロック」 | Có |

| Element | Text JP | Hành vi |
|---------|---------|---------|
| Close button (X) | — | Đóng dialog không lưu |
| Button | 「保存」 | Lưu action đã cấu hình |

---

### SCR-FRI-07: Popup tạo folder
- **Loại**: Popup/Overlay trong trang danh sách
- **Screenshot**: `screenshots/folder-create.png`

#### Form fields
| # | Label JP | Loại input | Bắt buộc? | Giá trị mặc định | Ghi chú |
|---|---------|-----------|----------|-----------------|---------|
| 1 | 「フォルダ名」 | Textbox | Có | Trống | Tối đa 15 ký tự. Hiển thị đếm: "{N}/15" |

#### Buttons
| Element | Text JP | Hành vi |
|---------|---------|---------|
| Button | 「決定」 | Tạo folder mới, đóng popup |
| Button | 「キャンセル」 | Đóng popup, không tạo |

---

### SCR-FRI-08: Danh sách câu trả lời (情報一覧) — Kiểu ngày tháng
- **URL**: `/basic/friend-information/item/{id}`
- **Tiêu đề trang**: 「情報一覧」
- **Screenshot**: `screenshots/item-list-date.png`

#### Header
| Vị trí | Element | Text JP | Loại | Hành vi |
|--------|---------|---------|------|---------|
| Trái | Label | 「情報」 | Text | Nhãn |
| Trái | Text | {tên thông tin} | Text | Tên trường thông tin (vd: "date 1") |
| Phải | Button | 「CSV書き出し」 | Button | Xuất dữ liệu ra file CSV |
| Phải | Button | 「一括削除」 | Button | Xoá hàng loạt dữ liệu đã chọn |

#### Bảng dữ liệu
| # | Cột | Text JP | Kiểu dữ liệu | Ghi chú |
|---|-----|---------|-------------|---------|
| 0 | Checkbox | — | Checkbox | Chọn item. Header có checkbox chọn tất cả |
| 1 | Tên bạn bè | 「友だち名」 | Link text | Click → navigate đến trang chi tiết bạn bè `/basic/friendlist/my_page/{friendId}` |
| 2 | Thông tin | 「情報」 | Text | Giá trị đã ghi nhận. Với kiểu「年月日」: format YYYY-MM-DD |

Dữ liệu mẫu (kiểu ngày tháng):

| 友だち名 | 情報 |
|---------|------|
| テスト | 2026-01-01 |
| テスト(Tan) | 2025-10-06 |
| テストkk | 2025-11-06 |
| Nguyen The Phuc | 2025-11-06 |
| Thinh Nguyen | 2025-09-30 |
| Duy | 2025-09-20 |
| Thanh /... | 2025-10-31 |
| テスト'T | 2026-03-10 |

---

### SCR-FRI-09: Danh sách câu trả lời (情報一覧) — Kiểu lựa chọn
- **URL**: `/basic/friend-information/item/{id}`
- **Tiêu đề trang**: 「情報一覧」
- **Screenshot**: `screenshots/item-list-select.png`

#### Bảng dữ liệu
Cùng cấu trúc như SCR-FRI-08 nhưng cột「情報」hiển thị giá trị lựa chọn (text tên option đã chọn).

Dữ liệu mẫu (kiểu lựa chọn):

| 友だち名 | 情報 |
|---------|------|
| テスト(Tan) | dd |
| テストkk | hhh |
| Nguyen The Phuc | dd |
| Thinh Nguyen | dd |
| Duy | dd |
| さ ち代... | hhh |
| Thanh /... | gg |

---

## Kiểu thông tin (情報タイプ) — Tổng hợp 6 loại

| # | Kiểu | Text JP | Có action? | Phần riêng trên form | Ghi chú |
|---|------|---------|-----------|---------------------|---------|
| 1 | Lựa chọn | 「選択肢」 | Có | Bảng lựa chọn + action per option + 稼働設定 | Mỗi option có thể gắn action riêng |
| 2 | Mô tả | 「記述」 | Không | Không có phần riêng | Chỉ lưu text tự do |
| 3 | Ngày tháng | 「年月日」 | Có | Action scheduling (月日/年月日, offset ngày, thời gian) | Action lặp hàng năm hoặc 1 lần tuỳ kiểu ngày |
| 4 | Hình ảnh | 「画像」 | Chưa rõ | Chưa quan sát | Chưa có snapshot cho kiểu này |
| 5 | PDF | 「PDF」 | Chưa rõ | Chưa quan sát | Chưa có snapshot cho kiểu này |
| 6 | Điểm | 「ポイント」 | Có | Action khi đạt ngưỡng + 稼働設定 | Trigger action khi tổng điểm đạt threshold |

---

## Luồng người dùng (User Flows)

### Luồng 1: Tạo trường thông tin mới
1. Tại SCR-FRI-01, click「新規作成」
2. Navigate đến SCR-FRI-02 (URL: `/basic/friend-information/add?folderId={folderId}`)
3. Nhập「管理名」, chọn「フォルダ」, chọn「情報タイプ」
4. Tuỳ kiểu thông tin, cấu hình phần riêng (lựa chọn, action scheduling, hoặc point threshold)
5. Click「保存」→ quay lại SCR-FRI-01

### Luồng 2: Chỉnh sửa trường thông tin
1. Tại SCR-FRI-01, click link「管理名」trên bảng
2. Navigate đến form chỉnh sửa (SCR-FRI-02/03/04/05 tuỳ kiểu)
3. Sửa「管理名」, thay đổi「フォルダ」(情報タイプ KHÔNG thể đổi — dropdown disabled)
4. Cấu hình/sửa phần riêng theo kiểu
5. Click「保存」→ quay lại SCR-FRI-01

### Luồng 3: Cấu hình action cho lựa chọn
1. Tại form kiểu「選択肢」, click「追加」để thêm option
2. Nhập tên lựa chọn
3. Click「設定する」trên dòng option → mở dialog SCR-FRI-06 (SC-004)
4. Chọn loại action (10 loại), cấu hình chi tiết
5. Click「保存」trên dialog → quay lại form
6. Click「保存」trên form chính

### Luồng 4: Cấu hình action cho ngày tháng
1. Tại form kiểu「年月日」, click「追加」
2. Chọn kiểu ngày:「月日」(lặp hàng năm) hoặc「年月日」(1 lần)
3. Cấu hình offset: từ ngày đăng ký, trước/sau N ngày, lúc HH:mm
4. Cấu hình action qua dialog SC-004
5. Click「保存」

### Luồng 5: Xem danh sách câu trả lời
1. Tại SCR-FRI-01, click số「回答人数」
2. Navigate đến SCR-FRI-08/09 (URL: `/basic/friend-information/item/{id}`)
3. Xem bảng danh sách bạn bè và giá trị đã ghi nhận
4. Có thể xuất CSV hoặc xoá hàng loạt
5. Click tên bạn bè → navigate đến trang chi tiết bạn bè (FA-013)

### Luồng 6: Quản lý folder
1. Tại SCR-FRI-01 panel trái, click icon (+) → mở popup SCR-FRI-07
2. Nhập tên folder (tối đa 15 ký tự), click「決定」
3. Folder mới xuất hiện trong cây thư mục
4. Click folder để lọc bảng theo folder đó
5. Dùng「一括フォルダ変更」để chuyển nhiều item sang folder khác

### Luồng 7: Xoá hàng loạt
1. Tại SCR-FRI-01, chọn checkbox các item cần xoá
2. Click「一括削除」
3. Xác nhận xoá (suy luận: có dialog confirm)

## Flow Diagram
```
SCR-FRI-01 Danh sách
    │
    ├── [新規作成] ──→ SCR-FRI-02/03/04/05 Form tạo mới
    │                       │
    │                       ├── [設定する] ──→ SCR-FRI-06 Dialog Action (SC-004)
    │                       │                      │
    │                       │                      └── [保存] ──→ Quay lại form
    │                       │
    │                       └── [保存] ──→ Quay lại SCR-FRI-01
    │
    ├── [Click 管理名] ──→ SCR-FRI-02/03/04/05 Form chỉnh sửa
    │                       │
    │                       └── [保存] ──→ Quay lại SCR-FRI-01
    │
    ├── [Click 回答人数] ──→ SCR-FRI-08/09 Danh sách câu trả lời
    │                           │
    │                           ├── [CSV書き出し] ──→ Download file CSV
    │                           ├── [一括削除] ──→ Xoá dữ liệu đã chọn
    │                           └── [Click 友だち名] ──→ FA-013 Trang chi tiết bạn bè
    │
    ├── [Icon +] ──→ SCR-FRI-07 Popup tạo folder
    │                   │
    │                   ├── [決定] ──→ Tạo folder, đóng popup
    │                   └── [キャンセル] ──→ Đóng popup
    │
    ├── [並べ替え] ──→ Chế độ kéo thả sắp xếp
    ├── [一括フォルダ変更] ──→ Chuyển folder hàng loạt
    └── [一括削除] ──→ Xoá hàng loạt
```

## Phụ thuộc chéo (Cross-references)

### Shared Components sử dụng
| Mã SC | Tên | Nơi sử dụng trong FA-015 |
|-------|-----|--------------------------|
| SC-004 | Action Settings | SCR-FRI-06 — Dialog cài đặt hành động. 10 action types: ステップ, テンプレート, テキスト, リマインド, タグ, リッチメニュー, ブックマーク, 友だち情報, 対応ステータス, ブロック |

### Tính năng liên quan
| Mã FA | Tên | Quan hệ |
|-------|-----|---------|
| FA-013 | Danh sách bạn bè | Link từ SCR-FRI-08/09 tên bạn bè → trang chi tiết bạn bè (`/basic/friendlist/my_page/{id}`) |
| FA-001 | Chat 1:1 | Thông tin bạn bè hiển thị trên giao diện chat 1:1 (theo mô tả tính năng) |

## Điểm chưa rõ / Cần xác minh
| # | Nội dung | Mức độ | Ghi chú |
|---|---------|--------|---------|
| 1 | Form kiểu「画像」(Hình ảnh) — chưa có snapshot | Trung bình | Cần quét thêm để xem cấu trúc form kiểu hình ảnh |
| 2 | Form kiểu「PDF」— chưa có snapshot | Trung bình | Cần quét thêm để xem cấu trúc form kiểu PDF |
| 3 | Kiểu「ポイント」— cấu hình ngưỡng điểm chi tiết | Trung bình | Khi click「追加」trong phần ポイント到達時アクション, giao diện cấu hình threshold chưa được chụp |
| 4 | Chế độ sắp xếp (「並べ替え」) hoạt động cụ thể ra sao | Thấp | Có thể là drag-and-drop |
| 5 | Folder: có thể rename/xoá folder không? | Thấp | Icon pencil gợi ý có thể rename, nhưng chưa quan sát được |
| 6 | Menu (⋯) trên mỗi dòng bảng có những action nào | Thấp | Suy luận: chỉnh sửa, xoá |
| 7 | Phân trang (pagination) trên danh sách chính và danh sách câu trả lời | Thấp | Chưa quan sát được — có thể bảng hiện tại chưa đủ dữ liệu để hiện phân trang |
| 8 | Quyền Staff cụ thể với tính năng này | Trung bình | Chưa kiểm tra |
