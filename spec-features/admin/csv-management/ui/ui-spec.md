# FA-014 — 「CSV管理」 (Quản lý CSV) — UI Spec

> **Portal**: Admin (LINE OA)
> **Feature folder**: `features/admin/csv-management/`
> **URL gốc**: `/basic/csv-management`
> **Nguồn dữ liệu**: snapshot accessibility tree từ playwright-cli (`raw/features/csv-management/*.yml`) + screenshots + `network-main-app.txt` + source code (blade/JS) cho màn hình không thể quét live
> **Ngày quét**: 2026-09-08 (lần 1) — **quét bổ sung cùng ngày (lần 2)** để khắc phục 3 vấn đề dữ liệu của lần 1 — **quét bổ sung lần 3 (2026-09-09)**: chụp riêng tab 「インポート」 và bổ sung màn hình `SCR-CSV-07`
> **Trạng thái dữ liệu**: **7 màn hình**. 6/7 có snapshot + screenshot live (SCR-CSV-01…06, trong đó SCR-CSV-02 nay có screenshot riêng `import-tab.png`). **SCR-CSV-07 dựng từ source code (blade + JS), chưa quan sát runtime** — không thể quét vì phải upload file thật (vi phạm nguyên tắc không thay đổi dữ liệu)

---

## 1. Tổng quan tính năng

「CSV管理」 là màn hình cho phép Admin **xuất (export)** danh sách bạn bè LINE ra file CSV theo điều kiện lọc tự chọn, và **nhập (import)** lại file CSV đã chỉnh sửa để ghi đè một số thông tin của bạn bè.

Đặc điểm quan sát được:

- Màn hình chính chia làm **2 tab**: 「エクスポート」 (Export) và 「インポート」 (Import).
- Tab Export quản lý các **"định nghĩa file export"** (dạng bản ghi có thể lưu, đặt tên, sửa lại, sắp xếp thứ tự, xoá hàng loạt) — không phải hành động download một lần.
- Mỗi bản ghi export lưu: tên quản lý, điều kiện lọc bạn bè, danh sách cột dữ liệu muốn xuất; và có một **trạng thái tạo file bất đồng bộ** (「作成中」 → sẵn sàng 「CSVダウンロード」).
- Tab Import cho phép chọn file CSV và upload; kèm **lịch sử import** (bảng 「インポート履歴」).
- Ghi chú trên UI xác nhận việc tạo CSV chạy nền: 「※データ量によっては、CSVの作成に数時間かかる場合があります。」 (tuỳ lượng dữ liệu, việc tạo CSV có thể mất vài giờ) → **Độ tin cậy: Cao** cho kết luận có background job.

### Phạm vi dữ liệu export
Người dùng chọn **1 trong 3** nhóm đối tượng (radio, loại trừ nhau):
- 「有効友だち」 (bạn bè đang hoạt động) — có thêm nút 「絞込み」 để lọc chi tiết
- 「ブロックした友だち」 (bạn bè mà OA đã chặn)
- 「ブロックされた友だち」 (bạn bè đã chặn OA)

Và chọn các cột dữ liệu qua 2 nhóm:
- 「単一選択項目」 — 7 checkbox thuộc tính cố định
- 「複数選択項目」 — 「タグ」 (tag) và 「友だち情報」 (trường thông tin bạn bè tự định nghĩa), chọn theo thư mục phân loại

### Phạm vi dữ liệu import
Ghi chú trên tab Import (nguyên văn, độ tin cậy Cao vì đọc trực tiếp từ DOM):
- 「CSVデータのインポートにより個人メモ・タグ・友だち情報の情報を書き換えることができます。」 → chỉ ghi đè được **個別メモ / タグ / 友だち情報**
- 「対応マーク・最終メッセージ受信日時・配信中ステップ・QRコードアクションの情報は書き換えできません。」 → **không** ghi đè được 対応マーク, 最終メッセージ受信日時, 配信中ステップ, QRコードアクション

---

## 2. Actors liên quan

| Actor | Quyền quan sát được | Ghi chú |
|-------|---------------------|---------|
| **Admin (LINE OA)** | Toàn quyền: tạo / sửa / copy / xoá / sắp xếp bản ghi export, tải CSV, upload CSV import | Là actor được dùng để quét |
| **Staff** | Chưa xác nhận | Menu 「CSV管理」 nằm trong nhóm 「お気に入り」 và mục 「データ管理」 của sidebar. Middleware route là `basic_access` (chung cho Admin + Staff) → **suy luận Staff cũng truy cập được nếu được cấp quyền custom role**. Độ tin cậy: **Thấp** — chưa đăng nhập Staff để kiểm chứng |
| **LINE User** | Không liên quan | Tính năng thuần nội bộ, không có trang public |

---

## 3. Danh sách màn hình

| Mã | Tên màn hình | Loại | URL / cách mở |
|----|-------------|------|---------------|
| SCR-CSV-01 | Danh sách export 「CSV管理」 — tab 「エクスポート」 | Trang | `GET /basic/csv-management` (tab mặc định, anchor `#tab-export`) |
| SCR-CSV-02 | Tab 「インポート」 | Tab trong trang | Click tab 「インポート」, anchor `#tab-import` |
| SCR-CSV-03 | Form tạo mới 「エクスポートデータ作成」 | Trang | `GET /basic/csv-management/create-download-file` (từ nút 「新規作成」) |
| SCR-CSV-04 | Form chỉnh sửa 「エクスポートデータ作成」 | Trang | `GET /basic/csv-management/edit-download-file/{id}` (click tên trong cột 管理名) |
| SCR-CSV-05 | Modal 「絞り込み」 (lọc đối tượng export) | Modal | Nút 「絞込み」 trong SCR-CSV-03/04 |
| SCR-CSV-06 | Modal 「【 並べ替え 】」 (sắp xếp danh sách) | Modal | Nút 「並べ替え」 trong SCR-CSV-01 |
| SCR-CSV-07 | Modal 「アクション稼働に関する確認」 (`#modalConfirmAction`) | Modal | **Tự động** mở sau khi chọn file ở SCR-CSV-02, khi `read_file_csv` trả `isShowAction = 1`. ⚠ **Dựng từ source code**, chưa quan sát runtime |
| — | ~~Modal 「対象人数」~~ | — | **KHÔNG TỒN TẠI — nhưng KHÔNG phải vì link hỏng** (đính chính V-05). Link 「N人」 **không mở modal** mà **mở tab mới** sang trang 「友だちリスト」 (`/basic/friendlist`) — `csv_management.js:803-811`. Xem mục 8.1 #1 |
| — | Trang copy 「エクスポートデータ作成」 | Trang | `GET /basic/csv-management/copy-download-file/{id}` — route đã xác nhận, **chưa thao tác** |

---

## SCR-CSV-01 — Danh sách export 「CSV管理」 (tab 「エクスポート」)

### URL / cách mở
- `GET https://form.watermeru.com/basic/csv-management`
- Controller: `CsvManagementController@index` → view `csv_management.csv_management`
- Middleware: `basic_access, https_protocol, is_expire, check_remember_token`
- Điểm vào từ sidebar: mục 「CSV管理」 (nhóm 「お気に入り」 và nhóm 「データ管理」)

### Layout
```
┌────────────────────────────────────────────────────────────┐
│ [h2] CSV管理                                                │
├────────────────────────────────────────────────────────────┤
│ ( エクスポート ) ( インポート )        ← tab bar (anchor)   │
├────────────────────────────────────────────────────────────┤
│ [新規作成]                    [並べ替え] [一括削除(disabled)]│
├────────────────────────────────────────────────────────────┤
│ ☐ | 作成日 | 管理名 | 対象人数 | 最終条件設定 | (actions) |⋮│
│ ☐ |2026.08.11| STUDIOvfyghidecsv | 1人 |2026.08.11|         │
│    |          |                    |     |  [最新情報に更新]│
│    |          |                    |     |  [CSVダウンロード]│
│ ☐ |2026.08.11| STUDIOvfyghidecsv | 0人 |2026.08.11|         │
│    |          |                    |     |  [最新情報に更新]│
│    |          |                    |     |  [作成中](disabled)│
└────────────────────────────────────────────────────────────┘
```
Screenshot: `ui/screenshots/main.png`

**Chi tiết trực quan** (xác nhận từ screenshot lần quét 2 — độ tin cậy **Cao**):
- Hàng tiêu đề bảng **nền xanh dương**, chữ trắng; có 2 cột trống ở cuối (1 cột rộng chứa cụm nút, 1 cột hẹp chứa menu `•••`).
- 「新規作成」 — nút **xanh dương**, góc trái toolbar.
- 「並べ替え」 — nút **xám đậm**; 「一括削除」 — nút **xám nhạt (disabled)**; cả hai ở góc phải toolbar.
- 「最新情報に更新」 — nút **vàng/cam**, có icon xoay vòng (refresh) bên trái nhãn.
- 「CSVダウンロード」 — nút **xanh dương**, có icon tải xuống bên phải nhãn.
- 「作成中」 — nút **xám nhạt, disabled**, không có icon.
- Menu dòng là **icon 3 chấm ngang `•••`**, nằm ở cột cuối cùng.
- Tab 「エクスポート」 đang active hiển thị dạng **tab nền xám đậm chữ trắng**; tab 「インポート」 nền trắng chữ xám.
- 「管理名」 và 「対象人数」 hiển thị dạng **link gạch chân màu xanh**.

### Tabs / Sub-navigation
| Label JP | Anchor | Trạng thái mặc định |
|----------|--------|---------------------|
| 「エクスポート」 | `#tab-export` | Active (mặc định khi mở trang) |
| 「インポート」 | `#tab-import` | Inactive |

> Tab là link anchor client-side (`/url: "#tab-export"`), **không đổi URL trình duyệt** → chuyển tab không reload trang. Độ tin cậy: **Cao**.

### Action Buttons

| Label JP | Loại | Vị trí | Hành vi quan sát được | Độ tin cậy |
|----------|------|--------|----------------------|-----------|
| 「新規作成」 | Button (primary) | Toolbar trái | Điều hướng sang `/basic/csv-management/create-download-file` (SCR-CSV-03) | Cao (đã click) |
| 「並べ替え」 | Button | Toolbar phải | Mở modal 「【 並べ替え 】」 (SCR-CSV-06) | Cao (đã click) |
| 「一括削除」 | Button, **disabled** | Toolbar phải, cạnh 並べ替え | Ở trạng thái không chọn dòng nào → disabled. **Suy luận**: bật khi tick ≥1 checkbox ở cột đầu | Trung bình (chưa tick vì nguyên tắc không đổi dữ liệu) |
| 「 最新情報に更新」 | Button (có icon) | Trong mỗi dòng, cột thao tác | **Chưa click**. Nhãn nghĩa là "cập nhật thông tin mới nhất" → suy luận: kích hoạt job tạo lại file CSV theo điều kiện đã lưu | Trung bình |
| 「CSVダウンロード」 | Button (có icon) | Trong mỗi dòng — chỉ hiện khi file đã sẵn sàng | **Chưa click**. Suy luận: tải file CSV đã tạo | Trung bình |
| 「作成中」 | Button **disabled** | Thay thế 「CSVダウンロード」 ở dòng đang xử lý | Hiển thị khi job chưa hoàn tất; disabled nên không tải được. Ánh xạ `filter_update_status ≠ 30` (xem mục 10) | Cao (đọc trực tiếp `[disabled]` từ snapshot + xác nhận source code) |
| Icon `•••` / menu dòng | Generic clickable (icon 3 chấm ngang, không có nhãn text) | Cột cuối mỗi dòng | **Chưa click**. Suy luận: dropdown thao tác dòng (「コピー」 / 「削除」) — khớp với route `copy-download-file/{id}` đã tồn tại | Trung bình |
| Checkbox header | Checkbox | Cột đầu hàng tiêu đề | Suy luận: chọn tất cả / bỏ chọn tất cả | Trung bình |
| Checkbox dòng | Checkbox | Cột đầu mỗi dòng | Chọn dòng cho thao tác 「一括削除」 | Trung bình |

### Data Table

| # | Tiêu đề JP | Nội dung | Kiểu dữ liệu | Dữ liệu mẫu |
|---|-----------|----------|--------------|-------------|
| 1 | (không nhãn) | Checkbox chọn dòng | boolean (UI-only) | — |
| 2 | 「作成日」 | Ngày tạo bản ghi | Date `YYYY.MM.DD` | `2026.08.11` |
| 3 | 「管理名」 | Tên quản lý — **là link** tới `/basic/csv-management/edit-download-file/{id}` | string | `STUDIOvfyghidecsv` (id=890), `STUDIOvfyghidecsv` (id=928) |
| 4 | 「対象人数」 | Số người thuộc đối tượng — hiển thị dạng **link gạch chân**. ✅ **Link hoạt động bình thường** (đính chính V-05): mở **tab mới** sang `/basic/friendlist` (xem Observation 5) | integer + hậu tố 「人」 | `1人`, `0人` |
| 5 | 「最終条件設定」 | Ngày cập nhật điều kiện lần cuối | Date `YYYY.MM.DD` | `2026.08.11` |
| 6 | (không nhãn) | Cụm nút thao tác: 「最新情報に更新」 + (「CSVダウンロード」 \| 「作成中」) | — | — |
| 7 | (không nhãn) | Icon menu dòng | — | — |

> **Quan trọng**: hai bản ghi trong dữ liệu mẫu **trùng tên** 「STUDIOvfyghidecsv」 nhưng khác `id` (890, 928) → tên quản lý **không unique**. Độ tin cậy: **Cao**.

### Observations
1. Cột thao tác dòng thể hiện rõ **state machine bất đồng bộ**: dòng id=890 (1人) hiển thị 「CSVダウンロード」 (file sẵn sàng); dòng id=928 (0人) hiển thị 「作成中」 disabled.
   ✅ **Đính chính (V-06)**: dòng id=928 hiển thị 「作成中」 **KHÔNG phải vì job chưa xong**. Điều kiện bật nút tải là **`filter_update_status == 30` VÀ `total_line_user > 0`** (`csv_management.blade.php:311-312`) — bản ghi ở `30` nhưng `total_line_user = 0` (「0人」) vẫn rơi vào nhánh 「作成中」. Xem thêm mục 10 và `logic-spec.md` BR-09. Độ tin cậy: **Cao**.
2. Không quan sát thấy **phân trang** hay bộ chọn 「表示件数」 trong snapshot (chỉ 2 dòng dữ liệu) → chưa kết luận được có phân trang hay không. Độ tin cậy: **Thấp**.
3. Không có ô tìm kiếm / lọc trên danh sách.
4. Endpoint AJAX bắt được khi load trang: `POST /ajax/init-csv-management` — **rất có thể** là endpoint nạp danh sách bản ghi export (kèm 2 endpoint chung của layout: `GET /ajax/admin/favorite-menu`, `GET /ajax/admin/notify-header`, `POST /ajax/check-init-tutorial`). Độ tin cậy: **Cao** cho việc endpoint tồn tại, **Trung bình** cho vai trò.
5. ✅ **ĐÍNH CHÍNH (V-05) — link 「N人」 ở cột 「対象人数」 HOẠT ĐỘNG BÌNH THƯỜNG, KHÔNG phải dead link.** Kết luận "dead link" ở lần quét trước là **sai**; source code cho thấy có handler thật. Độ tin cậy: **Cao**.
   - **Blade** (`resources/views/csv_management/csv_management.blade.php:301-305`) render **3 nhánh** trong `<td class="line_user_link">` tùy loại đối tượng export:
     - `enable_filter_friend == 1` → `<a href="#" v-on:click="showNumberFilter(item.id)">` — nhánh của bản ghi mẫu `id=890`
     - `enable_bot_block_friend == 1` → `:href="'/basic/friendlist/block'"` (điều hướng thẳng)
     - `enable_friend_block_bot == 1` → `:href="'/basic/friendlist/user-block'"` (điều hướng thẳng)
   - **Handler JS** (`public/js/csv_management/csv_management.js:803-811`): `showNumberFilter(csvId)` → `localStorage.setItem("csv_management_filter_id", csvId)` rồi `window.open("/basic/friendlist", "_blank")` — tức **mở tab mới**, truyền `csv_id` qua `localStorage`. Trang 「友だちリスト」 đọc khóa này rồi gọi **EP-10** `GET /ajax/initDataFilterCsvManagement` để dựng lại bộ lọc.
   - **Vì sao lần quét trước kết luận nhầm**: (a) handler là **Vue directive `v-on:click`** chứ không phải attribute inline — kiểm tra DOM thấy thẻ `<a>` "không có class / id / data-attribute" là **đúng nhưng không chứng minh được là không có handler"; (b) `window.open(..., "_blank")` mở **tab khác**, mà playwright-cli chụp snapshot của **tab hiện tại** nên thấy trang không đổi.
   - **Không có affordance giả** — gạch chân là hợp lý vì link thực sự điều hướng được.
   - Link 「3人」 trong form SCR-CSV-03/04 cùng markup `href="#"` — cũng thuộc cơ chế này.

---

## SCR-CSV-02 — Tab 「インポート」

### URL / cách mở
- Trong trang `/basic/csv-management`, click tab 「インポート」 (anchor `#tab-import`). Không đổi URL.
- Blade: `csv_management.blade.php:340` — `<div id="tab-import" class="tab-pane">`
- Screenshot: `ui/screenshots/import-tab.png` — **chụp riêng ở lần quét 3 (2026-09-09)**, đúng tab 「インポート」 đang active, đã đóng dialog cảnh báo Webhook.
- Snapshot: `raw/features/csv-management/import-tab-snapshot.yml` (cùng thời điểm) — xác nhận `link "インポート" [expanded] [active]` (`:e324`), nút 「アップロード」 `[disabled]` (`:e387`), `rowgroup` (tbody) của bảng 「インポート履歴」 **không có dòng nào**.

### Layout
```
┌────────────────────────────────────────────────────────────┐
│ [h2] CSV管理                                                │
│ ( エクスポート ) ( インポート ← active )                    │
├────────────────────────────────────────────────────────────┤
│ CSVデータのインポートにより個人メモ・タグ・友だち情報の…    │
│ 対応マーク・最終メッセージ受信日時・配信中ステップ・…       │
│                                                            │
│  [ ファイル選択 ]  (tên file hiện ở đây)  [アップロード]    │
│                                            (disabled)      │
│  ※ 4 dòng lưu ý                                            │
│                                                            │
│  インポート履歴                                             │
│  ┌───────────────────────────────────────────────┐         │
│  │ 作成日 |   | 管理名 | 対象人数 | 最終条件設定 │         │
│  │ (tbody rỗng — không có dữ liệu)               │         │
│  └───────────────────────────────────────────────┘         │
└────────────────────────────────────────────────────────────┘
```

### Nội dung hướng dẫn (nguyên văn)
| Vị trí | Text JP |
|--------|---------|
| Mô tả 1 | 「CSVデータのインポートにより個人メモ・タグ・友だち情報の情報を書き換えることができます。」 |
| Mô tả 2 | 「対応マーク・最終メッセージ受信日時・配信中ステップ・QRコードアクションの情報は書き換えできません。」 |
| Lưu ý 1 | 「※CSVデータは必ずエクスポートページからダウンロードしたものをご利用ください。」 |
| Lưu ý 2 | 「※CSVデータの上1・2行目と左1列目は、絶対に編集しないでください。」 |
| Lưu ý 3 | 「※友だち情報タイプ「画像」「PDF」はインポートできません」 |
| Lưu ý 4 | 「※友だち情報タイプ「年月日」は指定フォーマット( YYYY/MM/DD )以外は正常にインポートされません」 |

> Lưu ý 2 xác nhận **format CSV có 2 hàng header và cột đầu tiên là khoá định danh** (nhiều khả năng là LINE user id hoặc friend id). Độ tin cậy: **Cao** (đọc trực tiếp text UI), **Trung bình** cho suy luận nội dung cột 1.

### Form Fields

| Label JP | Loại input | Bắt buộc | Mặc định | Validation quan sát được |
|----------|-----------|----------|----------|--------------------------|
| 「ファイル選択」 | Nhãn `<label for="fileUpload">` bọc `<span class="btn ...">` — **`<input type="file">` thật bị ẩn** (`style="display:none"`), nên accessibility tree chỉ thấy element clickable tuỳ biến | Có (bắt buộc để bật nút upload) | Trống — `<p id="preview_file_name">` rỗng ngay bên phải để hiển thị **tên file** đã chọn | `accept=".csv"` trên input (`csv_management.blade.php:349`) — chỉ **gợi ý** hộp thoại chọn file, **không phải validation**. Ràng buộc thật nằm ở server (whitelist MIME ở `read_file_csv`). ⚠ Đoạn JS kiểm tra đuôi `.csv` phía client **đã bị comment** (`csv_management.js:9-13`) → hiện **không** chặn gì ở client. Độ tin cậy: **Cao** |

> **Cơ chế bind**: `onchange="importCSV(this)"` (`csv_management.blade.php:349`) → chọn file là **gọi ngay** `POST /basic/csv-management/read_file_csv` (`csv_management.js:29-31`, `async: false` → **khoá UI** trong lúc chờ, có overlay `$.LoadingOverlay("show")`). Độ tin cậy: **Cao**.

### Hành vi động sau khi chọn file (dựng từ JS + blade — chưa quan sát runtime)

| Bước | Điều xảy ra trên UI | Bằng chứng |
|------|--------------------|-----------|
| B1 | Overlay loading phủ trang trong khi gọi `read_file_csv` | `csv_management.js:36-38` (`beforeSend` → `$.LoadingOverlay("show")`) |
| B2a | **Thành công** (`a.success`): tên file hiện ở `<p id="preview_file_name">` bên phải nút 「ファイル選択」 | `csv_management.js:44` — `$("#preview_file_name").text(name)` |
| B2b | Dữ liệu đã parse gán vào `csv_management.csv_file`; số dòng gán vào biến `countUser`; **reset** `actionTag = 0`, `actionInForFriend = 0` | `csv_management.js:45-48` |
| B2c | Nút 「アップロード」 **tự bật** — ràng buộc `:disabled="csv_file.length==0"` | `csv_management.blade.php:353` |
| B2d | Nếu `a.isShowAction` truthy → **mở modal `#modalConfirmAction`** (**SCR-CSV-07**) | `csv_management.js:49-51` |
| B3 | **Thất bại**: `alert(a.message)` (thường là 「エラー」), đồng thời **xoá sạch** `#fileUpload` và `#preview_file_name` → nút 「アップロード」 vẫn disabled | `csv_management.js:53-55`; message do controller đặt (`CsvManagementController.php:836`) |

> ⚠ Thông báo lỗi ở B3 là **`alert()` trần với nội dung 「エラー」**, không nói rõ dòng nào / cột nào sai. Độ tin cậy: **Cao** (đọc trực tiếp source), **chưa quan sát runtime**.

### Action Buttons
| Label JP | Loại | Trạng thái quan sát | Hành vi |
|----------|------|---------------------|---------|
| 「ファイル選択」 | Label-button (xanh dương, `btn-sns-line-primary`) | Luôn bật | Mở hộp thoại chọn file → `importCSV()` → `EP-14 POST /basic/csv-management/read_file_csv`. Độ tin cậy: **Cao** (`csv_management.blade.php:346-349`) |
| 「アップロード」 | Button (xanh lá, `btn-sns-line-success`) | **disabled** khi chưa chọn file (xác nhận trên snapshot lần 3: `button "アップロード" [disabled] [ref=e387]`) | `onclick="csvSave()"` → `EP-15 POST /basic/csv-management/save_file_csv`, gửi kèm `csv_file`, `totalUser`, **`actionTag`**, **`actionInForFriend`** (2 giá trị lấy từ SCR-CSV-07). **Chưa thao tác** (nguyên tắc không thay đổi dữ liệu). Độ tin cậy: **Cao** cho cơ chế (`csv_management.blade.php:353`, `csv_management.js:64-76`) |

### Sau khi 「アップロード」 thành công (dựng từ JS)

| Điều xảy ra | Bằng chứng |
|---|---|
| Gọi lại `initDataImportCsvManagement({action:"initData"})` → nạp lại bảng 「インポート履歴」 qua `EP-06 POST /ajax/init-import-csv-management` | `csv_management.js:86`, `:217-241` |
| Bản ghi vừa tạo có `upload_status` = DEFAULT `1` → dòng mới hiện ngay trên đầu bảng với cột cuối là 「**作業中**」 | `csv_management.blade.php:383-384`; `CsvManagementController.php:920-926` (không truyền `upload_status`) |
| Reset trạng thái form: `countUser = 0`, `csv_file = []`, `#fileUpload` và `#preview_file_name` bị xoá → nút 「アップロード」 **trở lại disabled** | `csv_management.js:87-90` |
| **Thất bại**: `alert(a.message)`, **không** reset form | `csv_management.js:92` |

> ⚠ **Phát hiện mới — khối `uploadingFilterItems` là code chết**: blade có một khối `<tr v-for>` thứ hai render `uploadingFilterItems` với cột cuối cứng là 「作業中」 (`csv_management.blade.php:387-393`), nhưng biến này **chỉ được khai báo** trong `data` (`csv_management.js:109`) và **không nơi nào gán giá trị** trong toàn bộ JS/blade của tính năng. → Mảng **luôn rỗng**, khối này **không bao giờ render**. Dòng 「作業中」 mà người dùng thấy sau khi upload đến từ `historyUploadFilterItems` (nạp lại từ server), **không phải** từ dòng tạm client-side. Độ tin cậy: **Cao** (grep toàn bộ `public/js/` + `resources/views/` chỉ ra 2 vị trí duy nhất).

### Data Table — 「インポート履歴」 (Lịch sử import)

✅ **Đã đối chiếu source (khép lại nghi vấn của lần quét 1)**: nhãn header **sai hoàn toàn** so với nội dung thực tế render — đây là **bug sản phẩm B-07**, không phải thiếu mapping. Bảng dưới ghi cả hai cột: nhãn hiển thị và **nội dung thật**.

| # | Tiêu đề JP hiển thị | Nội dung THỰC TẾ render | Nguồn dữ liệu | Bằng chứng |
|---|--------------------|------------------------|---------------|-----------|
| 1 | 「作成日」 | **Ngày** tạo bản ghi import — `formatDate()` | `csv_filter_upload_history.created_at` | `csv_management.blade.php:378` |
| 2 | (không nhãn) | ⚠ **Giờ** của cùng `created_at` — `formatTime()`. Không phải cột trống | `csv_filter_upload_history.created_at` | `csv_management.blade.php:379` |
| 3 | 「管理名」 | ⚠ **Tên file CSV** người dùng đã upload (`$file->getClientOriginalName()`), **không** phải "tên quản lý" | `csv_filter_upload_history.name` | `csv_management.blade.php:380`; `CsvManagementController.php:916, 923` |
| 4 | 「対象人数」 | Số dòng dữ liệu + hậu tố 「人」 — ⚠ giá trị do **client tự khai** (`countUser` từ bước preview), server không đối chiếu | `csv_filter_upload_history.number_line_user` | `csv_management.blade.php:381`; `csv_management.js:71`; `CsvManagementController.php:922` |
| 5 | 「最終条件設定」 | ⚠ **KHÔNG phải datetime** — thực chất là **trạng thái xử lý**: `upload_status == 2` → 「**完了済**」; mọi giá trị khác → 「**作業中**」 | `csv_filter_upload_history.upload_status` | `csv_management.blade.php:383-384` |

> `tbody` **rỗng** trên cả 2 lần quét (lần 1 và lần 3 ngày 2026-09-09) → chưa có lịch sử import nào trên tài khoản test. Snapshot lần 3 xác nhận: `rowgroup` thứ hai (tbody) **không có `row` con nào** — **không phát hiện khác biệt** so với mô tả cũ.
>
> Bảng nằm trong `<div style="height:300px; overflow-y:scroll">` → **cuộn dọc cố định 300px**, **không phân trang** (server trả toàn bộ, `orderBy('id','desc')` — BR-17). Độ tin cậy: **Cao** (`csv_management.blade.php:365`).
>
> ⚠ **Bug B-07 (nhãn cột sai)**: header của bảng 「インポート履歴」 dùng **đúng bộ nhãn của bảng export** (作成日 / 管理名 / 対象人数 / 最終条件設定) — nay đã **xác nhận từ source** là blade bị **copy-paste** từ bảng export. Nặng nhất là cột 5: nhãn 「最終条件設定」 (thiết lập điều kiện lần cuối) nhưng render **trạng thái job**. Độ tin cậy: nâng từ **Trung bình** → **Cao**.

### Observations
1. Không thấy nút tải template CSV mẫu — người dùng bắt buộc phải export trước rồi sửa file đó.
2. Không thấy hiển thị tiến trình / kết quả import trên tab này (ngoài bảng lịch sử) — **không có** thanh tiến trình, **không có** báo cáo số dòng thành công / lỗi. Cột `message_error` của bảng là **cột chết**: không thành phần nào ghi, không UI nào đọc.
3. Toàn tab **không có nút 「更新」 / auto-refresh**: sau khi upload, bảng chỉ được nạp lại **một lần** ngay sau `save_file_csv` (`csv_management.js:86`) và khi chuyển sang tab import (`loadInitImportCsv`, blade `:265` `v-on:click` trên tab → `csv_management.js:247-250`). Muốn biết job đã xong hay chưa, người dùng phải **tự chuyển tab hoặc F5**. Độ tin cậy: **Cao**.
4. Luồng import **có thêm một màn hình nữa** không nhìn thấy ở trạng thái tĩnh: modal **SCR-CSV-07** 「アクション稼働に関する確認」, tự bật giữa bước chọn file và bước 「アップロード」.

---

## SCR-CSV-03 — Form tạo mới 「エクスポートデータ作成」

### URL / cách mở
- `GET https://form.watermeru.com/basic/csv-management/create-download-file`
- Controller: `CsvManagementController@createDownloadFile` → view `csv_management.create_download_file`
- Từ SCR-CSV-01, nút 「新規作成」

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│ [h2] エクスポートデータ作成            [< 前ページに戻る]     │
├──────────────────────────────────────────────────────────────┤
│ ▌書き出し名（管理用）                                        │
│   [___________________]  0/50文字                            │
│                                                              │
│ ▌エクスポート対象絞込み                                      │
│   (•) 有効友だち              [ 絞込み ]                     │
│   ┌────────────────────────────────────────┐                │
│   │ 対象人数（有効友だちのみ）      3人 ←link                │
│   │ 絞り込み条件                            │                │
│   └────────────────────────────────────────┘                │
│   ( ) ブロックした友だち                                     │
│   ( ) ブロックされた友だち                                   │
│                                                              │
│ ▌単一選択項目                                                │
│   ☐ ステータスメッセージ  ☐ 個別メモ   ☐ 友だち追加日 ☐対応マーク│
│   ☐ 最終メッセージ受信日時 ☐ 配信中ステップ ☐ 流入経路        │
│                                                              │
│ ▌複数選択項目                                                │
│   タグ                              [選択クリア]             │
│   ┌ [未分類 (4)] ┐ ┌ ☐フォーム未回答 ☐和食 ☐洋食 ☐中華 ┐    │
│   選択した項目                                               │
│   友だち情報                        [選択クリア]             │
│   ┌[未分類 (0)][基本情報 (4)][国内住所 (5)]┐ ┌分類を選択して下さい┐│
│   選択した項目                                               │
│                                                              │
│          [ この条件でCSVを作成・更新 ]                        │
│   ※データ量によっては、CSVの作成に数時間かかる場合があります。│
└──────────────────────────────────────────────────────────────┘
```
Screenshot: `ui/screenshots/create-form.png`

### Form Fields

#### Nhóm 1 — 「書き出し名（管理用）」
| Label JP | Loại | Bắt buộc | Placeholder | Mặc định | Validation quan sát được |
|----------|------|----------|-------------|----------|--------------------------|
| 「書き出し名（管理用）」 | Textbox 1 dòng | Suy luận **Có** (là tên quản lý duy nhất hiển thị trên danh sách) — Độ tin cậy: Trung bình | Không có | Rỗng | **Bộ đếm ký tự 「0/50文字」** hiển thị cạnh ô → giới hạn **tối đa 50 ký tự**. Độ tin cậy: **Cao** |

#### Nhóm 2 — 「エクスポート対象絞込み」 (radio group, chọn 1)
| Giá trị JP | Loại | Mặc định | Phụ thuộc |
|-----------|------|----------|-----------|
| 「有効友だち」 | Radio | **[checked]** (mặc định) | Khi chọn: hiện nút 「絞込み」 + khối tóm tắt 「対象人数（有効友だちのみ）」/「絞り込み条件」 |
| 「ブロックした友だち」 | Radio | Không chọn | Không có nút 絞込み đi kèm trong snapshot |
| 「ブロックされた友だち」 | Radio | Không chọn | Không có nút 絞込み đi kèm trong snapshot |

> Cấu trúc DOM cho thấy nút 「絞込み」 và khối tóm tắt **chỉ gắn với radio 「有効友だち」** → bộ lọc chi tiết chỉ áp dụng cho nhóm bạn bè đang hoạt động. Độ tin cậy: **Cao**.

#### Khối tóm tắt điều kiện (read-only)
| Nhãn JP | Giá trị mẫu | Ghi chú |
|---------|------------|---------|
| 「対象人数（有効友だちのみ）」 | 「3人」 (link `href="#"`) | Số người khớp điều kiện hiện tại. ✅ Cùng dạng link `href="#"` như cột 「対象人数」 trên danh sách — **không phải dead link** (đính chính V-05): handler Vue `v-on:click` mở **tab mới** `/basic/friendlist` (`csv_management.js:803-811`). Độ tin cậy: **Cao** (đọc trực tiếp blade + JS) |
| 「絞り込み条件」 | (rỗng trong snapshot) | Hiển thị tóm tắt điều kiện lọc đã lưu; rỗng vì form tạo mới chưa có điều kiện |

#### Nhóm 3 — 「単一選択項目」 (7 checkbox, độc lập)
| # | Label JP | Mặc định | Ý nghĩa (dịch) |
|---|----------|----------|----------------|
| 1 | 「ステータスメッセージ」 | Không tick | Status message của LINE |
| 2 | 「最終メッセージ受信日時」 | Không tick | Thời điểm nhận tin nhắn cuối |
| 3 | 「個別メモ」 | Không tick | Ghi chú riêng cho từng bạn bè |
| 4 | 「配信中ステップ」 | Không tick | Step delivery đang chạy |
| 5 | 「友だち追加日」 | Không tick | Ngày thêm bạn |
| 6 | 「流入経路」 | Không tick | Nguồn/kênh vào |
| 7 | 「対応マーク」 | Không tick | Mark trạng thái xử lý |

> Layout: 3 cụm 2 checkbox + 1 checkbox lẻ (対応マーク). Tất cả **mặc định không tick**. Độ tin cậy: **Cao**.

#### Nhóm 4 — 「複数選択項目」

**4a. 「タグ」** — chọn tag theo thư mục (dạng 2 cột: folder trái, tag phải)
| Thành phần | Nội dung quan sát |
|-----------|-------------------|
| Nút 「選択クリア」 | Xoá toàn bộ lựa chọn tag |
| Danh sách folder | 1 mục: 「未分類 (4)」 — số trong ngoặc = số tag trong folder |
| Danh sách tag (folder 未分類) | Checkbox: 「フォーム未回答」, 「和食」, 「洋食」, 「中華」 — tổng 4, khớp `(4)` |
| Nhãn 「選択した項目」 | Vùng hiển thị các tag đã chọn (rỗng trong snapshot) |

**4b. 「友だち情報」** — chọn trường thông tin bạn bè theo thư mục
| Thành phần | Nội dung quan sát |
|-----------|-------------------|
| Nút 「選択クリア」 | Xoá toàn bộ lựa chọn trường |
| Danh sách folder | 「未分類 (0)」, 「基本情報 (4)」, 「国内住所 (5)」 |
| Danh sách trường | 「分類を選択して下さい」 (placeholder — chưa chọn folder nào) |
| Nhãn 「選択した項目」 | Vùng hiển thị các trường đã chọn (rỗng trong snapshot) |

> ⚠ Ở nhóm 「タグ」 folder 「未分類 (4)」 đã tự động mở sẵn (hiện 4 tag), còn ở nhóm 「友だち情報」 **chưa folder nào được chọn**. Có thể folder đầu tiên tự mở khi có ≥1 phần tử. Độ tin cậy: **Thấp**.

### Action Buttons
| Label JP | Loại | Vị trí | Hành vi |
|----------|------|--------|---------|
| 「< 前ページに戻る」 | Link | Góc phải header | Về `/basic/csv-management` (SCR-CSV-01). Độ tin cậy: Cao (đọc `/url`) |
| 「絞込み」 | Button | Cạnh radio 「有効友だち」 | Mở modal 「絞り込み」 (SCR-CSV-05). Độ tin cậy: **Cao** (đã click) |
| 「選択クリア」 ×2 | Button | Góc phải khối 「タグ」 và 「友だち情報」 | Bỏ chọn tất cả trong khối tương ứng. Độ tin cậy: Trung bình |
| 「未分類 (4)」 / 「未分類 (0)」 / 「基本情報 (4)」 / 「国内住所 (5)」 | Button (tab folder) | Cột trái mỗi khối | Chuyển folder → nạp danh sách phần tử tương ứng. Độ tin cậy: Trung bình |
| 「この条件でCSVを作成・更新」 | Button (submit, primary) | Cuối form | Lưu bản ghi + khởi tạo tạo file CSV. **Chưa click** (nguyên tắc không đổi dữ liệu). Nhãn 「作成・更新」 cho thấy cùng 1 nút dùng chung cho create và edit. Độ tin cậy nhận định: Trung bình |

### Observations
1. Ghi chú 「※データ量によっては、CSVの作成に数時間かかる場合があります。」 → **xác nhận xử lý nền, không đồng bộ**. Kết hợp với trạng thái 「作成中」 trên danh sách → có background job (khả năng cao là Spring Boot job). Độ tin cậy: **Cao**.
2. Form không có nút 「保存」 riêng biệt — lưu và tạo file là **cùng một hành động**.
3. Không thấy validation message nào hiển thị trong snapshot (form chưa submit).
4. Số 「3人」 trong form khác số 「1人」/「0人」 trên bảng danh sách → số trong form là **đếm real-time theo điều kiện hiện tại**, còn số trên bảng là **snapshot tại lần tạo file cuối**. Độ tin cậy: **Trung bình**.

---

## SCR-CSV-04 — Form chỉnh sửa 「エクスポートデータ作成」

### URL / cách mở
- `GET https://form.watermeru.com/basic/csv-management/edit-download-file/{id}` — ví dụ `/890`
- Controller: `CsvManagementController@editDownloadFile` → view `csv_management.create_download_file` (**dùng chung view với form tạo mới** — xác nhận từ routes index, độ tin cậy **Cao**)
- Từ SCR-CSV-01: click tên trong cột 「管理名」

- Screenshot: `ui/screenshots/edit-form.png` — bản ghi `id=890`, tên `STUDIOvfyghidecsv`
- **Tiêu đề trang (browser title)**: 「CSV管理（エクスポート編集）」 — **khác** với create; nhưng **heading `<h2>` trên trang vẫn là 「エクスポートデータ作成」** (giống hệt create). Độ tin cậy: **Cao**.

### Quan hệ với SCR-CSV-03
Form edit **dùng chung blade** `csv_management.create_download_file` với form tạo mới (xác nhận từ routes index). Toàn bộ **layout, nhãn, thứ tự khối, nút bấm đều giống hệt SCR-CSV-03** — điểm khác duy nhất là các field được **prefill** theo dữ liệu đã lưu và tiêu đề trang trình duyệt.

> Do đó phần dưới **chỉ liệt kê điểm khác biệt**; cấu trúc đầy đủ xem SCR-CSV-03.

### Trạng thái prefill quan sát được (bản ghi id=890)

| Field | Giá trị trong form edit | So với form create | Độ tin cậy |
|-------|------------------------|-------------------|-----------|
| 「書き出し名（管理用）」 | `STUDIOvfyghidecsv` (textbox có value) | Create: rỗng | **Cao** (đọc trực tiếp `textbox [ref=e323]: STUDIOvfyghidecsv`) |
| Bộ đếm ký tự | **「0/50文字」** ⚠ | Create: 「0/50文字」 | **Cao** — xem Observation 1 (lỗi) |
| Radio 「有効友だち」 | **[checked]** | Create: [checked] (mặc định) | **Cao** |
| Radio 「ブロックした友だち」 | không chọn | giống | Cao |
| Radio 「ブロックされた友だち」 | không chọn | giống | Cao |
| 「対象人数（有効友だちのみ）」 | 「3人」 (link `href="#"`) | giống | Cao |
| 「絞り込み条件」 | **rỗng** | giống (rỗng) | Cao |
| 単一選択項目 → 「個別メモ」 | **[checked]** ✔ | Create: không tick | **Cao** |
| 単一選択項目 → 6 mục còn lại (「ステータスメッセージ」「最終メッセージ受信日時」「配信中ステップ」「友だち追加日」「流入経路」「対応マーク」) | **không tick** | giống | Cao |
| 「タグ」 — folder | 「未分類 (4)」 | giống | Cao |
| 「タグ」 — 4 checkbox tag | **không tick mục nào** | giống | Cao |
| 「友だち情報」 — folder | 「未分類 (0)」/「基本情報 (4)」/「国内住所 (5)」 | giống | Cao |
| 「友だち情報」 — danh sách trường | 「分類を選択して下さい」 (chưa chọn folder) | giống | Cao |
| Nút submit | 「この条件でCSVを作成・更新」 | giống — cùng 1 nút cho cả create và update | Cao |
| 「< 前ページに戻る」 | về `/basic/csv-management` | giống | Cao |

> ✅ **Kết luận cấu hình của bản ghi id=890**: đối tượng = 「有効友だち」, **không có** điều kiện lọc chi tiết, cột dữ liệu xuất chỉ gồm **duy nhất 「個別メモ」**, không chọn tag nào, không chọn trường 友だち情報 nào. Điều này khớp với 「対象人数」 = 「1人」 trên bảng danh sách (không lọc → lấy toàn bộ bạn bè hợp lệ tại thời điểm tạo file).

### Observations

1. ⚠ **Lỗi bộ đếm ký tự**: ô 「書き出し名（管理用）」 đã prefill `STUDIOvfyghidecsv` (17 ký tự) nhưng bộ đếm vẫn hiển thị **「0/50文字」** thay vì 「17/50文字」. Xác nhận trên **cả snapshot lẫn screenshot**. → Bộ đếm chỉ cập nhật khi có sự kiện gõ phím (`input`/`keyup`), **không khởi tạo lúc trang load**. Đây là **bug hiển thị nhỏ** (cosmetic), không ảnh hưởng dữ liệu. Độ tin cậy: **Cao**.
2. **Khối 「絞り込み条件」 rỗng** ở form edit của bản ghi id=890 → bản ghi này **thật sự không có điều kiện lọc nào**, chứ không phải form không load được điều kiện. Xác nhận thêm bởi 「対象人数」 = 3人 (bằng đúng giá trị của form tạo mới, tức toàn bộ bạn bè hợp lệ). Độ tin cậy: **Trung bình** — cần 1 bản ghi CÓ điều kiện lọc để kiểm chứng cách hiển thị tóm tắt.
3. **Số 「3人」 trong form ≠ 「1人」 trên bảng danh sách** cho cùng bản ghi id=890 → khẳng định 2 nguồn số liệu khác nhau: form đếm **real-time**, bảng danh sách hiển thị **snapshot lưu tại lần tạo file gần nhất**. Độ tin cậy: **Cao** (nay đã có đối chứng cùng một bản ghi).
4. Không có nút 「削除」 hay 「コピー」 trong form edit — các thao tác này chỉ có ở menu `•••` trên bảng danh sách. Độ tin cậy: **Cao**.
5. URL dùng `{id}` dạng số nguyên (`/890`); chưa kiểm tra hành vi khi truy cập id không thuộc bot hiện tại (rủi ro IDOR — cần web-analyzer kiểm tra phân quyền). Độ tin cậy cảnh báo: **Thấp**.

---

## SCR-CSV-05 — Modal 「絞り込み」 (lọc đối tượng export)

> 🔗 **Cross-reference shared component**: đây **CHÍNH LÀ** **SC-003 — Friend Filter/Segment** (biến thể **V2**: 11 loại điều kiện, hỗ trợ AND + OR).
> Spec đầy đủ: `features/shared/friend-filter/shared-spec.md` (trạng thái: **ĐÃ SCAN**).
> Phần dưới chỉ ghi nhận **biểu hiện tại FA-014**; không lặp lại chi tiết logic của SC-003.

### URL / cách mở
- Modal client-side (`<dialog>`), mở từ nút 「絞込み」 trong SCR-CSV-03/04. Không đổi URL.
- Screenshot: `ui/screenshots/filter-modal.png`

### Layout
```
┌───────────────────────────────────────────────────────────────┐
│ [×]           絞り込み                                        │
├───────────────────────────────────────────────────────────────┤
│ [「全て満たす」必要がある条件 (and条件)を追加] (active)        │
│ [「どれか1つ以上満たす」必要がある条件 (or条件)を追加]         │
├──────────────────────┬────────────────────────────────────────┤
│ ⊕ タグ               │ 「全て満たす」必要がある条件 (and条件)  │
│ ⊕ 友だち名           │   (khu vực thả điều kiện — rỗng)       │
│ ⊕ 友だち追加日       │                                        │
│ ⊕ ステップ購読状況   ├────────────────────────────────────────┤
│ ⊕ QRコードアクション │ 「どれか1つ以上満たす」必要がある条件   │
│ ⊕ コンバージョン     │  (or条件)                              │
│ ⊕ 確認状況           │   (khu vực thả điều kiện — rỗng)       │
│ ⊕ 友だち情報         │                                        │
│ ⊕ 対応ステータス     │                                        │
│ ⊕ アフィリエイター   │                                        │
│ ⊕ 新規・既存 友だち  │                                        │
├──────────────────────┴────────────────────────────────────────┤
│                      [ 保存 ]                                 │
└───────────────────────────────────────────────────────────────┘
```

### Thành phần
| Thành phần | Label JP | Ghi chú |
|-----------|----------|---------|
| Nút đóng | (icon ×) | Góc trái header modal |
| Tiêu đề | 「絞り込み」 | `heading level=2` |
| Chế độ thêm điều kiện | 「「全て満たす」必要がある条件 (and条件)を追加」 | Nhóm AND — nút đang được nhấn (xanh) trong screenshot |
| Chế độ thêm điều kiện | 「「どれか1つ以上満たす」必要がある条件 (or条件)を追加」 | Nhóm OR |
| Danh sách loại điều kiện | 11 nút (bảng dưới) | Cột trái, mỗi nút có icon ⊕ |
| Vùng chứa AND | 「「全て満たす」必要がある条件 (and条件)」 | Rỗng — chưa có điều kiện |
| Vùng chứa OR | 「「どれか1つ以上満たす」必要がある条件 (or条件)」 | Rỗng |
| Nút lưu | 「保存」 | Cuối modal |

### 11 loại điều kiện (khớp 100% với SC-003 V2)
| # | Label JP | # | Label JP |
|---|----------|---|----------|
| 1 | 「タグ」 | 7 | 「確認状況」 |
| 2 | 「友だち名」 | 8 | 「友だち情報」 |
| 3 | 「友だち追加日」 | 9 | 「対応ステータス」 |
| 4 | 「ステップ購読状況」 | 10 | 「アフィリエイター」 |
| 5 | 「QRコードアクション」 | 11 | 「新規・既存 友だち」 |
| 6 | 「コンバージョン」 | | |

### Observations
1. Danh sách 11 loại điều kiện **trùng khớp chính xác** với biến thể V2 của SC-003 đã ghi nhận tại FA-003, FA-013, FA-041 → khẳng định dùng chung component. Độ tin cậy: **Cao**.
2. **Chưa thao tác** thêm điều kiện nào → không capture được UI chi tiết của từng loại điều kiện (dropdown toán tử, ô nhập giá trị). Chi tiết đó nằm trong spec SC-003.
3. Modal chỉ có nút 「保存」, không có nút 「キャンセル」 riêng (đóng bằng icon ×).

---

## SCR-CSV-06 — Modal 「【 並べ替え 】」 (sắp xếp thứ tự danh sách)

### URL / cách mở
- Modal client-side, mở từ nút 「並べ替え」 trên toolbar SCR-CSV-01. Không đổi URL.
- Screenshot: `ui/screenshots/sort-modal.png` (đã chụp lại đúng ở lần quét 2)

### Layout
```
┌──────────────────────────────────────────────┐
│         【　並べ替え　】                 [×] │
├──────────────────────────────────────────────┤
│  ┌──────────────────────────┐                │
│  │ STUDIOvfyghidecsv        │      ˄         │
│  └──────────────────────────┘      ˅         │
│  ┌──────────────────────────┐                │
│  │ STUDIOvfyghidecsv        │      ˄         │
│  └──────────────────────────┘      ˅         │
│                                              │
│              [   保存   ]                    │
└──────────────────────────────────────────────┘
```

### Thành phần
| Thành phần | Nội dung | Ghi chú |
|-----------|----------|---------|
| Nút đóng | Icon `×` đen | **Góc trên bên phải** modal (xác nhận từ screenshot; accessibility tree liệt kê trước heading nhưng vị trí render là bên phải) |
| Tiêu đề | 「【　並べ替え　】」 | `heading level=2`, căn giữa, có khoảng trắng rộng bên trong ngoặc 【 】 |
| Danh sách item | 2 dòng, mỗi dòng là **ô viền chữ nhật (dạng textbox)** chứa 「STUDIOvfyghidecsv」 | Số dòng **khớp số bản ghi** trên bảng danh sách (2). Chỉ hiển thị 管理名, không có ngày/số người |
| Điều khiển mỗi dòng | **2 icon chevron: `˄` (lên) và `˅` (xuống)**, xếp dọc ở bên phải mỗi ô | Đổi vị trí item lên/xuống 1 bậc. Độ tin cậy: **Cao** (xác nhận trực quan từ screenshot — lần quét 1 chỉ suy luận được) |
| Nút lưu | 「保存」 — nút **bo tròn màu xanh lá**, căn giữa dưới cùng | Lưu thứ tự mới |

> ⚠ **Không phải drag-and-drop thật**: modal dùng **cặp nút mũi tên lên/xuống**, không có drag handle (`fa-bars`) như biến thể ở FA-017/FA-035. Đây là **biến thể "Arrow-based Reorder"** của cùng họ component sắp xếp. Độ tin cậy: **Cao**.

### Observations
1. Modal chỉ hiển thị **管理名**, không hiển thị ngày hay số người → xác nhận chỉ dùng để đổi thứ tự hiển thị.
2. Cấu trúc (dialog + heading + list item có điều khiển + nút lưu) trùng khuôn với **Sortable List** đã ghi nhận tại FA-035 (SCR-EMP-05 modal 「並べ替え」) và FA-017 (2 modal `sort_folder` / `sort_qr`) → đây là ứng viên shared component (chưa có mã SC). Đã bổ sung vào `features/shared/pending-refs.md`.
3. Khác biệt so với FA-035/FA-017 (**xác nhận trực quan ở lần quét 2**):
   - Cơ chế đổi thứ tự: **nút chevron lên/xuống** (FA-014) vs **drag handle `fa-bars` + dropdown ⋮** (FA-017/FA-035).
   - Nút lưu: 「保存」 xanh lá bo tròn (FA-014) vs 「変更を保存」 (FA-017/FA-035).
   - Tiêu đề bọc ngoặc 【 】 với khoảng trắng rộng.
   - Item hiển thị trong **ô viền dạng textbox** thay vì dòng list phẳng.
4. Chưa xác nhận **chiều sắp xếp** gửi lên server (ASC hay DESC) — FA-017 có tiền lệ client đảo ngược mảng vì query `ORDER BY position DESC`.

---

## SCR-CSV-07 — Modal 「アクション稼働に関する確認」 (`#modalConfirmAction`)

> ⚠ **Màn hình này được dựng hoàn toàn từ SOURCE CODE (blade + JS), CHƯA quan sát runtime.**
> Lý do: chỉ có thể mở bằng cách **upload file CSV thật** lên hệ thống lme.jp → vi phạm nguyên tắc "KHÔNG thay đổi dữ liệu". Mọi mô tả layout/nhãn/hành vi dưới đây đọc trực tiếp từ `csv_management.blade.php:434-485` và `csv_management.js:44-51, 64-76` → **độ tin cậy Cao** cho *nội dung*; **chưa xác nhận** cách trình duyệt render thực tế (kích thước, vị trí chính xác, animation).
> **Không có screenshot.**

### Vì sao đây là một màn hình đáng đặc tả
Modal này là **điểm quyết định duy nhất** trong toàn hệ thống cho phép người dùng bật/tắt việc **kích hoạt action khi import** — mà action ở LME **có thể gửi tin nhắn LINE hàng loạt** tới toàn bộ bạn bè có trong file CSV. Hai lựa chọn ở đây ghi thẳng vào 2 cột `is_action_tag` / `is_action_info_friend` của `csv_filter_upload_history`, và job Spring Boot đọc lại để gọi `ActionModel.doActionWithRequestSent()`.

### URL / cách mở
- Modal Bootstrap client-side (`<div class="modal fade" id="modalConfirmAction">`), **không đổi URL** (`csv_management.blade.php:434`).
- **Không có nút nào mở nó.** Mở **tự động** bởi JS: sau khi `EP-14 POST /basic/csv-management/read_file_csv` trả về `success = true` **và** `isShowAction` truthy → `$('#modalConfirmAction').modal('show')` (`csv_management.js:49-51`).
- Nằm giữa **SCR-CSV-02 bước chọn file** và **SCR-CSV-02 bước bấm 「アップロード」**.

### Điều kiện xuất hiện — `isShowAction` được tính thế nào

Controller `CsvManagementController@readFileCsv` khởi tạo `$isShowAction = 0` (`:675`) rồi đặt `= 1` **ngay khi** phát hiện file CSV có bất kỳ cột nào thuộc các nhóm sau (quét **hàng header thứ nhất** `$row0` và **hàng header thứ hai** `$row`):

| # | Điều kiện phát hiện | Nguồn | Dòng |
|---|---------------------|-------|------|
| 1 | Header hàng 1 chứa chuỗi 「タグ」 (dạng `タグ_{id}`) | `strpos($row0[$i], "タグ") !== false` | `:731-732` |
| 2 | Header hàng 2 = 「システム表示名」 | `switch ($value)` | `:742-743` |
| 3 | Header hàng 2 = 「携帯電話」 | | `:748-749` |
| 4 | Header hàng 2 = 「メールアドレス」 | | `:754-755` |
| 5 | Header hàng 2 = 「生年月日」 | | `:760-761` |
| 6 | Header hàng 2 = 「年齢」 | | `:766-767` |
| 7 | Header hàng 2 = 「都道府県」 | | `:772-773` |
| 8 | Header hàng 1 chứa chuỗi 「友だち情報」 (dạng `友だち情報_{id}`) | `strpos($row0[$i], "友だち情報") !== false` | `:781-782` |

Giá trị trả về client trong response: `'isShowAction' => $isShowAction` (`:844`).

> ⚠ **`isShowAction` là cờ GỘP, không tách theo nhóm**: file chỉ có cột 「タグ」 (không có 友だち情報), hoặc ngược lại, đều làm modal hiện **cả hai** nhóm radio. Người dùng vẫn phải trả lời câu hỏi cho nhóm không tồn tại trong file. Độ tin cậy: **Cao**.
> ⚠ Mục 2–7 là **6 trường 友だち情報 mặc định** (nhóm 「基本情報」) nhưng lại được kiểm bằng **nhãn tiếng Nhật hard-code** trong `switch`, không qua config — sửa nhãn ở nơi khác sẽ làm mất tính năng này.
> ⚠ Nếu file **không** có cột tag/友だち情報 nào (ví dụ chỉ export 「個別メモ」 như bản ghi mẫu `id=890`) → `isShowAction = 0` → **modal không hiện**, và `actionTag`/`actionInForFriend` giữ nguyên `0` (đã reset ở `csv_management.js:47-48`) → **không action nào chạy**.

### Layout
```
┌──────────────────────────────────────────────────────────────┐
│  ⚠ アクション稼働に関する確認                            [×] │
├──────────────────────────────────────────────────────────────┤
│  インポートする情報にタグ・友だち情報が含まれています。      │
│  タグ追加時アクション・友だち情報の登録時アクションが        │
│  設定されている場合の                                        │
│  アクション稼働について選択してください。                    │
│                                                              │
│  タグ追加時アクション                                        │
│    ( ) 稼働させない        ( ) 稼働させる                    │
│                                                              │
│  友だち情報 登録時アクション                                 │
│    ( ) 稼働させない        ( ) 稼働させる                    │
│                                                              │
│                          [ 閉じる ]  [ インポートする ]      │
└──────────────────────────────────────────────────────────────┘
```

**Chi tiết trực quan** (đọc từ CSS inline / style block — độ tin cậy **Cao** cho khai báo, **Trung bình** cho kết quả render):
- Modal **căn giữa màn hình tuyệt đối**: `.modal-dialog { margin: unset; top: 50%; left: 50%; transform: translate(-50%,-50%) }` (`csv_management.blade.php:225-230`) — khác các modal khác của trang (mặc định căn trên).
- Nền phủ ngoài: `background-color: rgba(136,136,136,0.64)` — **xám mờ** thay vì đen mặc định của Bootstrap (`:232-234`).
- Header **không có đường viền** (`border: 0`), tiêu đề `<h2>` 18px, đậm 600, màu `#222222`, có **icon cảnh báo `far fa-exclamation-circle` màu cam `#FEA600`** đứng trước (`:440`).
- Nút `×` (`fal fa-times`, 32px, màu `#222222`) ở **góc trên bên phải** (`:438-439`).
- Body font 14px, weight 300, line-height 24px, padding trái/phải 47px (`:443-444`).
- Radio đã chọn: chữ chuyển **màu xanh lá `#08BF5A` + in đậm** (`:220-223`) — dấu hiệu trực quan duy nhất phân biệt lựa chọn.
- `data-keyboard="false"` (`:434`) → **phím ESC không đóng được** modal. Không khai báo `data-backdrop="static"` → click ra nền ngoài **vẫn đóng** (mặc định Bootstrap). Độ tin cậy: **Cao** cho `data-keyboard`, **Trung bình** cho hành vi backdrop.

### Nội dung hướng dẫn (nguyên văn)
| Vị trí | Text JP | Dòng |
|--------|---------|------|
| Tiêu đề | 「アクション稼働に関する確認」 | `:440` |
| Mô tả 1 | 「インポートする情報にタグ・友だち情報が含まれています。」 | `:445` |
| Mô tả 2 | 「タグ追加時アクション・友だち情報の登録時アクションが設定されている場合の」 | `:446` |
| Mô tả 3 | 「アクション稼働について選択してください。」 | `:447` |

### Form Fields — 2 nhóm radio (mỗi nhóm chọn 1)

| Nhóm | Nhãn nhóm JP | Lựa chọn | `value` | Vue model | Mặc định | Dòng |
|------|-------------|----------|---------|-----------|----------|------|
| 1 | 「タグ追加時アクション」 | 「稼働させない」 (không kích hoạt) | `"0"` | `actionTag` | **`0`** — reset về 0 mỗi lần chọn file (`csv_management.js:47`) | `:451-455` |
| 1 | | 「稼働させる」 (có kích hoạt) | `"1"` | `actionTag` | | `:457-459` |
| 2 | 「友だち情報 登録時アクション」 | 「稼働させない」 | `"0"` | `actionInForFriend` | **`0`** (`csv_management.js:48`) | `:463-467` |
| 2 | | 「稼働させる」 | `"1"` | `actionInForFriend` | | `:469-471` |

> ⚠ **Không radio nào có thuộc tính `checked` trong blade** → khi modal vừa mở, **hình như không có lựa chọn nào được tô sáng**. Nhưng `data` của Vue khởi tạo `actionTag: 0` / `actionInForFriend: 0` (**kiểu số**, `csv_management.js:122-123`) trong khi `value` của radio là **chuỗi** `"0"`. Với `v-model` của Vue 2 trên radio, so sánh là `===` **loose theo giá trị đã cast**? — thực tế Vue 2 so sánh bằng `looseEqual`, `0 == "0"` → **có** tô sáng 「稼働させない」. Độ tin cậy: **Trung bình** (chưa quan sát runtime; cần kiểm chứng bằng ảnh chụp thật).
> ⚠ Sau khi người dùng click radio, `v-model` gán **chuỗi** `"0"`/`"1"` (không phải số) → giá trị gửi lên server là chuỗi. Server nhận `$request->actionTag ?? 0` (`CsvManagementController.php:925`) — chuỗi `"0"` **không** phải null nên được lưu nguyên, MySQL ép về int. Không gây lỗi. Độ tin cậy: **Cao**.

### Action Buttons

| Label JP | Loại | Vị trí | Hành vi THỰC TẾ | Dòng |
|----------|------|--------|-----------------|------|
| `×` (icon `fal fa-times`) | Icon button | Header, góc phải | `data-dismiss="modal"` — **chỉ đóng modal**, không có handler JS. Giá trị 2 radio **được giữ nguyên** | `:438-439` |
| 「閉じる」 (Đóng) | Button **xám nhạt** (`background:#F8F8F8`, chữ `#222222`), rộng 120px | Footer, bên trái | `data-dismiss="modal"` — **chỉ đóng modal**, **không có `v-on:click`, không có `onclick`** | `:481` |
| 「インポートする」 (Import) | Button **xanh lá** (`btn-sns-line-success`), rộng 150px | Footer, bên phải | ⚠ **CŨNG chỉ có `data-dismiss="modal"`** — **KHÔNG gọi `csvSave()`**, **KHÔNG gửi request nào** | `:482` |

> ⚠⚠ **Phát hiện quan trọng — 3 nút của modal có hành vi HOÀN TOÀN GIỐNG NHAU**: cả `×`, 「閉じる」 và 「インポートする」 đều chỉ mang `data-dismiss="modal"`, **không nút nào có handler**. Modal này **thuần tuý là bộ thu thập 2 giá trị `actionTag` / `actionInForFriend`** thông qua `v-model`; việc import **vẫn phải do người dùng tự bấm nút 「アップロード」 ở SCR-CSV-02** sau khi modal đóng.
>
> Hệ quả UX (**bug tiềm ẩn**, độ tin cậy **Cao** vì đọc trực tiếp source):
> - Nhãn 「インポートする」 (= "Thực hiện import") **hứa hẹn sai**: bấm nó **không** import gì cả. Người dùng có thể tưởng đã import xong rồi rời trang → **import không bao giờ chạy**.
> - 「閉じる」 (= "Đóng", ngụ ý huỷ) **không huỷ gì cả**: lựa chọn radio vẫn được giữ và vẫn gửi lên khi bấm 「アップロード」. Không có đường "huỷ bỏ file đã chọn" từ modal.
> - Không có nút nào **bắt buộc** người dùng trả lời — đóng modal ngay lập tức (bằng `×` hoặc click nền) vẫn cho phép upload với giá trị mặc định `0/0`.

### Hệ quả xuống DB và background job

| Lựa chọn trên modal | Param gửi lên (`EP-15`) | Cột DB | Job Spring Boot đọc và làm gì |
|---------------------|------------------------|--------|-------------------------------|
| 「タグ追加時アクション」 = 「稼働させる」 | `actionTag = "1"` (`csv_management.js:72`) | `csv_filter_upload_history.is_action_tag` (`CsvManagementController.php:925`) | `csv.getIsActionTag() == ACTION_YES` → gọi `ActionModel.doActionWithRequestSent()` cho **từng bạn bè được gán tag mới** (`HandleImportCsvTask.java:298, 309` → `:302`) |
| 「タグ追加時アクション」 = 「稼働させない」 | `actionTag = "0"` | `is_action_tag = 0` | Bỏ qua nhánh gọi action |
| 「友だち情報 登録時アクション」 = 「稼働させる」 | `actionInForFriend = "1"` (`csv_management.js:73`) | `csv_filter_upload_history.is_action_info_friend` (`CsvManagementController.php:926`) | `csv.getIsActionInfoFriend() == ACTION_YES` → chạy action khi **ghi giá trị mới** (`INSERT_VALUE`) hoặc **đổi giá trị** (`CHANGE_VALUE`) của trường 友だち情報, kể cả trường kiểu **điểm** (`TYPE_DATA_POINT`) (`HandleImportCsvTask.java:148, 361, 377, 388, 400, 446` → `:424`) |
| 「友だち情報 登録時アクション」 = 「稼働させない」 | `actionInForFriend = "0"` | `is_action_info_friend = 0` | Bỏ qua nhánh gọi action |

Hằng số Java: `CsvFilterUploadHistory.ACTION_NO = 0`, `ACTION_YES = 1`; getter trả `ACTION_NO` khi cột `NULL` (`CsvFilterUploadHistory.java:16-17, 136-141`) → **NULL được coi là "không chạy action"** (an toàn theo mặc định). Độ tin cậy: **Cao**.

> 🔴 **Mức ảnh hưởng**: `ActionModel.doActionWithRequestSent()` là hàm dùng chung để **thực thi action** của LME — bao gồm **gửi tin nhắn LINE**, gán/gỡ tag, chạy step, ghi conversion… Chọn 「稼働させる」 trên một file CSV chứa hàng nghìn dòng đồng nghĩa với **gửi tin nhắn hàng loạt** cho từng dòng. Đây là lý do modal này tồn tại — và cũng là lý do việc 3 nút của nó không phân biệt hành vi là **rủi ro thật sự**, không chỉ là lỗi thẩm mỹ.

### Observations
1. Modal **không hiển thị bất kỳ số liệu nào** để người dùng ước lượng tác động: không nói file có bao nhiêu dòng, bao nhiêu tag, có bao nhiêu tag/trường đang gắn action. Người dùng chọn 「稼働させる」 **mù**.
2. Modal **không phân biệt** file chỉ có tag với file chỉ có 友だち情報 (cờ `isShowAction` gộp chung) → luôn hỏi cả 2 câu.
3. **Không có bước xác nhận thứ hai** trước khi thực sự import (nút 「アップロード」 gọi `csvSave()` thẳng, không confirm) — trong khi thao tác ghi đè dữ liệu bạn bè + có thể gửi tin hàng loạt.
4. Modal **không có trạng thái "đã trả lời"**: sau khi đóng, SCR-CSV-02 không hiển thị lại lựa chọn đã chọn. Muốn xem/đổi, người dùng phải **chọn lại file** (thao tác này reset `actionTag`/`actionInForFriend` về `0` — `csv_management.js:47-48`).
5. Chưa xác nhận được: modal có bị đóng/mở lại đúng cách khi người dùng chọn file lần thứ hai không; giao diện thật ở màn hình nhỏ (`.modal-dialog` bị ép `transform` cứng, không responsive rõ ràng).

---

## 4. User Flows

### Flow A — Tạo file export mới (happy path)
```
1. Admin vào sidebar → 「CSV管理」  → SCR-CSV-01 (tab エクスポート)
2. Click 「新規作成」                → SCR-CSV-03
3. Nhập 「書き出し名（管理用）」 (≤50 ký tự)
4. Chọn radio đối tượng:
   4a. 「有効友だち」 → (tuỳ chọn) click 「絞込み」 → SCR-CSV-05
       → thêm điều kiện AND/OR → 「保存」 → quay lại form,
         khối 「絞り込み条件」 + 「対象人数」 cập nhật
   4b. hoặc 「ブロックした友だち」 / 「ブロックされた友だち」
5. Tick các cột cần xuất ở 「単一選択項目」 (7 lựa chọn)
6. Chọn 「タグ」: chọn folder → tick các tag
7. Chọn 「友だち情報」: chọn folder (基本情報 / 国内住所 / 未分類) → tick các trường
8. Click 「この条件でCSVを作成・更新」
9. Hệ thống lưu bản ghi + đưa vào hàng đợi tạo file
10. Quay về SCR-CSV-01 → dòng mới xuất hiện với trạng thái 「作成中」
```

### Flow B — Tải file CSV
```
1. SCR-CSV-01 → tìm dòng cần tải
2. Nếu nút hiển thị 「作成中」 (disabled) → file chưa sẵn sàng, chờ
3. Khi nút chuyển thành 「CSVダウンロード」 → click → tải file
   (chưa xác nhận: tải trực tiếp hay qua endpoint riêng)
```

### Flow C — Cập nhật dữ liệu mới nhất 「最新情報に更新」
```
1. SCR-CSV-01 → dòng bản ghi đã có file
2. Click 「 最新情報に更新」
3. Suy luận: hệ thống chạy lại truy vấn theo điều kiện đã lưu,
   tạo lại file CSV → trạng thái chuyển về 「作成中」
4. Khi xong → trở lại 「CSVダウンロード」, cột 「対象人数」 và
   「最終条件設定」 được cập nhật
```
> Toàn bộ Flow C là **suy luận từ nhãn nút + state machine quan sát được**. Độ tin cậy: **Trung bình**. Chưa click vì nguyên tắc không thay đổi dữ liệu.

### Flow D — Import CSV
```
1. SCR-CSV-01 → click tab 「インポート」 → SCR-CSV-02
2. Click 「ファイル選択」 → chọn file CSV (phải là file đã export từ hệ thống)
   → gọi POST /basic/csv-management/read_file_csv (đọc & kiểm tra nội dung)
3. Tên file hiển thị ở <p id="preview_file_name">; nút 「アップロード」 disabled → enabled
3b. NẾU file có cột タグ / 友だち情報 (isShowAction = 1)
   → TỰ ĐỘNG mở SCR-CSV-07 「アクション稼働に関する確認」
   → chọn 稼働させる / 稼働させない cho từng nhóm
   → đóng modal (cả 3 nút ×/閉じる/インポートする đều CHỈ đóng, không import)
4. Click 「アップロード」 → hàm JS csvSave()
   (gửi kèm actionTag / actionInForFriend lấy từ SCR-CSV-07)
   → gọi POST /basic/csv-management/save_file_csv
5. Hệ thống ghi đè 個別メモ / タグ / 友だち情報 của các bạn bè trong file
6. Bản ghi mới trong csv_filter_upload_history — LUỒNG HIỆN HÀNH (Spring Boot):
   upload_status 1 (chờ) → 100 (IN_QUEUE) → 77 (đang chạy) → 2 (kết thúc)
   ⚠ Java đặt 2 ở MỌI nhánh kết thúc, KỂ CẢ khi lỗi → UI báo 「完了済」
   → hiển thị ở bảng 「インポート履歴」

   LUỒNG PHP DI SẢN (Laravel command handle:import_csv, đã ngừng từ ~2023-02):
   upload_status 1 → 77 → 2 (xong) hoặc 103 (lỗi)
   ⚠ 103 CHỈ luồng này mới ghi — Java không bao giờ ghi 103
```
> Endpoint ở bước 2 và 4 + enum `upload_status`: **xác nhận từ source code** (độ tin cậy **Cao**). Cách UI phản hồi kết quả import: **chưa quan sát được** — chưa upload vì nguyên tắc không thay đổi dữ liệu.
>
> ⚠ **Bổ sung (V-07)**: giá trị `100` = `STATUS_IN_QUEUE` **chỉ Spring Boot ghi** (`HandleImportCsvManager.java:63`, hằng số `CsvFilterUploadHistory.java:13`); Laravel không ghi, không poll (`HandleImportCsv.php:69` chỉ poll `1`). Blade không phân biệt `100` → hiển thị 「作業中」.

### Flow E — Chỉnh sửa / Copy / Sắp xếp / Xoá
```
E1 Chỉnh sửa: SCR-CSV-01 → click 「管理名」 → SCR-CSV-04 → sửa → 「この条件でCSVを作成・更新」
E2 Copy:      SCR-CSV-01 → icon menu dòng → 「コピー」(?) → /copy-download-file/{id}
              (route đã xác nhận; nhãn menu CHƯA xác nhận)
E3 Sắp xếp:   SCR-CSV-01 → 「並べ替え」 → SCR-CSV-06 → đổi thứ tự → 「保存」
E4 Xoá:       SCR-CSV-01 → tick checkbox ≥1 dòng → 「一括削除」 (bật) → (dialog xác nhận?)
```

---

## 5. Flow Diagram

```mermaid
flowchart TD
    SB[Sidebar: CSV管理] --> L[SCR-CSV-01<br/>Danh sách export<br/>tab エクスポート]

    L -- "tab インポート" --> I[SCR-CSV-02<br/>Tab Import]
    I -- "tab エクスポート" --> L

    L -- "新規作成" --> C[SCR-CSV-03<br/>Form tạo mới]
    L -- "click 管理名" --> E[SCR-CSV-04<br/>Form chỉnh sửa /{id}]
    L -- "menu dòng → コピー (?)" --> CP[/copy-download-file/{id}<br/>chưa xác nhận/]
    L -- "並べ替え" --> S[SCR-CSV-06<br/>Modal 並べ替え]
    L -- "click N人 → window.open(_blank)" --> FL[/basic/friendlist<br/>tab mới — csv_id qua<br/>localStorage.csv_management_filter_id/]
    L -- "tick ☐ + 一括削除" --> D{Xoá hàng loạt}

    C -- "絞込み" --> F[SCR-CSV-05<br/>Modal 絞り込み = SC-003 V2]
    E -- "絞込み" --> F
    F -- "保存" --> C

    C -- "この条件でCSVを作成・更新" --> Q[[Hàng đợi tạo CSV<br/>background job]]
    E -- "この条件でCSVを作成・更新" --> Q
    L -- "最新情報に更新" --> Q

    Q --> ST1["filter_update_status<br/>1 / 20 / 2 / 88<br/>→ nút 作成中 disabled"]
    ST1 -- "job DONE" --> ST2["filter_update_status = 30<br/>→ nút CSVダウンロード bật"]
    ST1 -. "job FAILURE = 40" .-> ST3["Vẫn hiển thị 作成中<br/>(UI không phân biệt lỗi)"]
    ST2 -- "click" --> DL[/Tải file CSV/]

    I -- "ファイル選択" --> RF[POST /basic/csv-management/read_file_csv]
    RF -- "isShowAction = 1<br/>(file có タグ / 友だち情報)" --> AC["SCR-CSV-07<br/>Modal アクション稼働に関する確認<br/>(dựng từ source, chưa quan sát runtime)"]
    AC -- "×/閉じる/インポートする<br/>đều CHỈ đóng modal" --> RF2["Quay lại SCR-CSV-02<br/>actionTag / actionInForFriend đã đặt"]
    RF -- "isShowAction = 0" --> RF2
    RF2 -- "アップロード" --> UP[[POST /basic/csv-management/save_file_csv<br/>ghi đè 個別メモ/タグ/友だち情報<br/>+ is_action_tag / is_action_info_friend]]
    UP -. "is_action_* = 1" .-> ACT["Job gọi ActionModel.doActionWithRequestSent()<br/>⚠ CÓ THỂ GỬI TIN NHẮN LINE HÀNG LOẠT"]
    UP --> H["Bảng インポート履歴<br/>csv_filter_upload_history.upload_status<br/>Java: 1 → 100 → 77 → 2 (kể cả khi lỗi)<br/>PHP di sản: 1 → 77 → 2 / 103"]
    H -. "lỗi vẫn về 2" .-> HB["UI hiển thị 完了済<br/>(báo sai thành công)"]

    S -- "保存" --> L
```

---

## 6. Endpoint AJAX quan sát được

| Method | URL | Vai trò suy luận | Độ tin cậy |
|--------|-----|------------------|-----------|
| POST | `/ajax/init-csv-management` | Nạp dữ liệu khởi tạo trang CSV管理 (danh sách bản ghi export + import history) | Trung bình (tên endpoint rõ nghĩa, chưa xem payload) |
| GET | `/ajax/admin/favorite-menu` | Layout chung — menu yêu thích sidebar | Cao (không thuộc FA-014) |
| GET | `/ajax/admin/notify-header` | Layout chung — thông báo header | Cao (không thuộc FA-014) |
| POST | `/ajax/check-init-tutorial` | Layout chung — kiểm tra hiển thị tutorial | Cao (không thuộc FA-014) |

### Bổ sung từ web-analyzer (đọc source Laravel — độ tin cậy **Cao**)
| Method | URL | Vai trò | Kích hoạt từ |
|--------|-----|---------|--------------|
| POST | `/basic/csv-management/read_file_csv` | Đọc & kiểm tra nội dung file CSV vừa chọn (tiền xử lý trước khi lưu) | SCR-CSV-02 — thao tác chọn file ở 「ファイル選択」 |
| POST | `/basic/csv-management/save_file_csv` | Lưu & thực thi import (hàm JS `csvSave()`) | SCR-CSV-02 — nút 「アップロード」 |

> ⚠ **Vẫn chưa bắt được** network của: form create/edit (nạp tag/friend-info folder), modal 絞り込み (chuỗi `init-data-filter`, `get-list-group-tag-filter`... theo mẫu SC-003), modal 並べ替え, nút 最新情報に更新, nút CSVダウンロード. Xem `web/api-spec.md` để có danh sách endpoint đầy đủ từ source code.

---

## 7. Shared Components liên quan

| Mã | Tên | Nơi xuất hiện trong FA-014 | Trạng thái |
|----|-----|---------------------------|-----------|
| **SC-003** | Friend Filter/Segment 「絞り込み」 (biến thể **V2** — 11 loại điều kiện, AND + OR) | SCR-CSV-05, mở từ nút 「絞込み」 trong SCR-CSV-03/04 | **ĐÃ SCAN** — xem `features/shared/friend-filter/shared-spec.md`. Đã bổ sung FA-014 vào cột "Được dùng bởi" của registry |
| **SC-002** | Tag Selector 「タグ」 | SCR-CSV-03/04 — khối 「複数選択項目」 → 「タグ」 (folder 「未分類 (4)」 + 4 tag checkbox + 「選択クリア」 + vùng 「選択した項目」). ⚠ Đây là **biến thể chỉ-đọc-để-lọc-cột** (chọn tag làm cột xuất CSV), không phải gán tag cho bạn bè | **CHƯA SCAN** — đã cập nhật `pending-refs.md` |
| — | **Sortable List — biến thể "arrow-based"** (ứng viên, chưa có mã SC) | SCR-CSV-06 modal 「【 並べ替え 】」 | Ứng viên. Đã thấy trước đó tại FA-035, FA-017, FA-041 nhưng ở đó là **drag handle**; FA-014 dùng **cặp nút chevron lên/xuống** → cùng họ, khác cơ chế tương tác. Đã ghi nhận tại `pending-refs.md` |
| — | **Friend Info Field Selector** 「友だち情報」 (ứng viên mới) | SCR-CSV-03/04 — khối 「複数選択項目」 → 「友だち情報」 với folder 「未分類 (0)」/「基本情報 (4)」/「国内住所 (5)」 | Ứng viên — cùng khuôn 2 cột folder/item với Tag Selector. Đã ghi nhận tại `pending-refs.md` |
| — | **Folder Management Panel** (đã xác nhận là shared từ FA-004/FA-011) | SCR-CSV-03/04 — dạng **tab folder chỉ-đọc** (chỉ chuyển folder, không thêm/sửa/xoá folder) | Biến thể rút gọn — đã ghi chú tại `pending-refs.md` |

---

## 8. Điểm chưa rõ / cần điều tra

### 8.1 Phát hiện & vấn đề còn lại

> ✅ **Đã khắc phục ở lần quét 2**: (a) form edit SCR-CSV-04 nay có snapshot + screenshot thật, (b) `main.png` / `edit-form.png` / `sort-modal.png` đã chụp lại đúng nội dung, (c) đã làm rõ hành vi của link 「対象人数」.

| # | Vấn đề | Chi tiết | Ưu tiên |
|---|--------|----------|---------|
| 1 | ✅ **ĐÃ GIẢI QUYẾT (V-05) — link 「N人」 KHÔNG phải dead link** | Kết luận "dead link" trước đây là **spec sai**, đã đính chính. Link **hoạt động bình thường**: handler Vue `v-on:click="showNumberFilter(item.id)"` (blade `csv_management.blade.php:301-305`; JS `csv_management.js:803-811`) ghi `csv_id` vào `localStorage.csv_management_filter_id` rồi `window.open("/basic/friendlist", "_blank")` → **mở tab mới**. Hai nhánh còn lại trỏ thẳng `/basic/friendlist/block` và `/basic/friendlist/user-block`.<br>→ Snapshot playwright-cli không bắt được vì `window.open` mở **sang tab khác**, còn snapshot chỉ chụp tab hiện tại. Handler là Vue directive nên kiểm tra attribute DOM không thấy.<br>→ **Không cần gỡ gạch chân** — không có affordance giả. Độ tin cậy: **Cao** | — (đã đóng) |
| 2 | **Trang copy chưa thao tác** | Route `GET /basic/csv-management/copy-download-file/{id}` đã xác nhận trong routes index nhưng chưa biết điểm vào trên UI (suy luận: menu `•••` ở cột cuối mỗi dòng) và chưa biết hành vi (copy ngay rồi redirect? hay mở form đã điền sẵn?) | Trung bình |
| 3 | **Chưa có bản ghi CÓ điều kiện lọc để đối chứng** | Cả 2 bản ghi mẫu (890, 928) đều **không có điều kiện lọc** → khối 「絞り込み条件」 luôn rỗng, chưa biết UI hiển thị tóm tắt điều kiện đã lưu như thế nào (text? chip? danh sách?) | Trung bình |
| 4 | **Menu `•••` chưa mở** | Chưa biết danh sách mục trong dropdown (suy luận: 「コピー」 / 「削除」) | Trung bình |
| 5 | ⚠ **Bug bộ đếm ký tự ở form edit** | Ô 「書き出し名（管理用）」 prefill 17 ký tự nhưng bộ đếm vẫn hiển thị 「0/50文字」 — không khởi tạo lúc load, chỉ cập nhật khi gõ. Xác nhận cả trên snapshot lẫn screenshot. Độ tin cậy: **Cao**. Mức độ: cosmetic, không ảnh hưởng dữ liệu | Thấp |
| 6 | **Trạng thái lỗi export không hiển thị trên UI + KHÔNG có đường retry** (bug sản phẩm) | `filter_update_status = 40` (FAILURE) vẫn render nút 「作成中」 giống các trạng thái đang chờ → người dùng **không phân biệt được** file đang tạo và file tạo thất bại (`csv_management.blade.php:309-317` — blade chỉ có 2 nhánh: `== 30` và `v-else`).<br>• **Định lượng thật (V-04)**: **18/208 bản ghi ở `40`** + **4/208 bản ghi ở `10`** (mồ côi) = **22/208 = 10,6%** đang hiển thị 「作成中」 **sai sự thật**.<br>• **Tình tiết tăng nặng**: ở nhánh `v-else`, nút 「最新情報に更新」 **CŨNG bị disabled** → **không có đường retry từ UI**, người dùng bế tắc hoàn toàn.<br>• Không có thông báo lỗi ở bất kỳ nơi nào khác (lỗi chỉ vào log4j / Chatwork).<br>Độ tin cậy: **Cao** (nâng từ Trung bình — nay đã đọc trực tiếp `csv_management.blade.php:309-317`) | **Cao** |
| 7 | **Rủi ro IDOR chưa kiểm tra** | URL edit dùng id số nguyên trực tiếp (`/edit-download-file/890`); chưa kiểm tra hệ thống có chặn truy cập bản ghi thuộc bot khác không. Cần web-analyzer kiểm tra điều kiện `bot_id` trong query | Trung bình |
| 8 | ⚠ **Import lỗi hiển thị 「完了済」 — BÁO SAI THÀNH CÔNG** (bug sản phẩm, V-03) | Luồng **Spring Boot hiện hành** đặt `upload_status = 2` (`STATUS_DONE`) ở **MỌI nhánh kết thúc**, **kể cả khi `readFileCSVV2()` ném exception** (`HandleImportCsvTask.java:79-80` và `:99-100`). Blade chỉ có **2 nhánh**: `v-if="item.upload_status == 2"` → 「完了済」; `v-else` → 「作業中」 (`csv_management.blade.php:383-384`).<br>→ Một lần import **thất bại** vẫn hiển thị 「**完了済**」, người dùng **tin rằng dữ liệu đã được ghi** trong khi không.<br>→ **Nặng hơn mục 6**: mục 6 chỉ **mập mờ** (「作成中」), mục này **báo sai thành công**.<br>→ Cột `message_error` đáng lẽ chứa lý do lỗi thì **không thành phần nào ghi** (0/302 bản ghi) và không UI nào đọc.<br>→ Luồng **PHP di sản** thì ghi `103` → 「作業中」 vĩnh viễn (2 bản ghi thật, 2023-02-01).<br>Độ tin cậy: **Cao** | **Cao** |

### 8.2 Hành động chưa click (nguyên tắc KHÔNG thay đổi dữ liệu)

| Nút | Lý do không click | Điều chưa biết |
|-----|-------------------|----------------|
| 「最新情報に更新」 | Sẽ kích hoạt job tạo lại file → thay đổi dữ liệu | Endpoint gọi là gì; trạng thái chuyển thế nào; có confirm dialog không |
| 「CSVダウンロード」 | Tải file — an toàn về mặt dữ liệu nhưng chưa thực hiện trong phiên quét | URL download; định dạng file; header CSV thực tế (2 hàng header theo lưu ý ở tab import) |
| 「一括削除」 | Xoá dữ liệu | Có dialog xác nhận không; xoá cả file đã tạo không |
| 「コピー」 (menu dòng) | Tạo bản ghi mới | Nhãn thực tế của menu; hành vi sau khi copy |
| 「この条件でCSVを作成・更新」 | Tạo/ghi đè bản ghi | Validation phía client; thông báo lỗi; redirect sau submit |
| 「アップロード」 (import) | Ghi đè dữ liệu bạn bè | Endpoint; validate file; hiển thị kết quả import |
| 「保存」 trong 2 modal | Thay đổi cấu hình | Payload gửi lên |

### 8.3 State machine bất đồng bộ — ĐÃ XÁC NHẬN

Xem chi tiết enum tại **mục 10**. Tóm tắt: cột `csv_management.filter_update_status` có **8 giá trị** (1, 2, 10, 20, 30, 40, 88, 99), UI chỉ render **2 nhánh**.

> ✅ **Đính chính điều kiện bật nút tải (V-06)** — trước đây ghi "chỉ `= 30` → nút tải bật", **thiếu một vế**. Đúng là (`csv_management.blade.php:309-317`, khớp `logic-spec.md` BR-09):
> - `filter_update_status == 30` **VÀ** `total_line_user > 0` → 「最新情報に更新」 bật + 「CSVダウンロード」 bật (`:311`)
> - `filter_update_status == 30` **VÀ** `total_line_user == 0` → 「最新情報に更新」 bật + badge 「作成中」 disabled (`:312`)
> - mọi giá trị khác `30` → **cả hai** nút disabled (`:314-317`)
>
> → Điều này **giải thích** vì sao dòng `id=928` có 「0人」 lại hiển thị 「作成中」 — **không phải vì job chưa xong**, mà vì `total_line_user = 0`. Độ tin cậy: **Cao**.

Còn cần làm rõ ở bước `/spec-job`:
- Job chạy theo lịch (polling) hay theo hàng đợi; chu kỳ bao lâu
- Cơ chế chuyển `1`/`20` → `2` (IN_QUEUE) → `88` (RUNNING) → `30`/`40` do thành phần nào thực hiện
- File CSV lưu ở đâu (local disk / S3), tên file, TTL bao lâu
- Có retry khi `40` (FAILURE) không; người dùng có được thông báo không

### 8.4 Câu hỏi khác

| # | Câu hỏi | Ghi chú |
|---|---------|---------|
| 1 | Bảng 「インポート履歴」 có đúng bộ cột như header hiển thị không? | Header (作成日/管理名/対象人数/最終条件設定) trùng bảng export — nghi blade bị copy-paste. Bảng dữ liệu đã xác nhận là `csv_filter_upload_history` (từ web-analyzer) → cần đối chiếu cột thật của bảng này với header đang render |
| 2 | Danh sách export có phân trang không? | Chỉ có 2 dòng dữ liệu nên không xác định được |
| 3 | 「書き出し名」 có bắt buộc không, có validate trùng tên không? | 2 bản ghi mẫu **trùng tên hoàn toàn** → gần như chắc chắn **không** validate trùng |
| 4 | Có giới hạn số bản ghi export mỗi tài khoản không? | Chưa quan sát được |
| 5 | Nhóm 「ブロックした友だち」/「ブロックされた友だち」 có được lọc chi tiết không? | Snapshot cho thấy nút 「絞込み」 chỉ gắn với 「有効友だち」 → suy luận **không** |
| 6 | Tính năng có phụ thuộc gói cước (有料プラン) không? | Không thấy badge 有料プラン限定 trên menu 「CSV管理」 → suy luận là tính năng cơ bản. Độ tin cậy: Thấp |

---

## 9. Tổng kết độ phủ

| Hạng mục | Trạng thái |
|----------|-----------|
| Màn hình xác định | **7** (SCR-CSV-01 → 07). Modal 「対象人数」 **không tồn tại** — vì link 「N人」 **mở tab mới** sang `/basic/friendlist` chứ không mở modal (V-05), **không phải vì link hỏng**; còn 1 trang chưa thao tác (copy) |
| Màn hình có snapshot hợp lệ | **6/7** — SCR-CSV-01…06 đều có snapshot live. **SCR-CSV-07 không có** (chỉ mở được sau khi upload file thật) |
| Màn hình có screenshot hợp lệ | **6/7** — `main.png` (SCR-CSV-01), **`import-tab.png` (SCR-CSV-02 — chụp riêng ở lần quét 3, 2026-09-09)**, `create-form.png` (03), `edit-form.png` (04), `filter-modal.png` (05), `sort-modal.png` (06).<br>✅ **Đính chính (lần quét 3)**: khẳng định cũ *"SCR-CSV-02 nằm trong `main.png` (cùng trang, đổi tab)"* là **SAI** — `main.png` chụp tab 「エクスポート」, **không thấy nội dung tab 「インポート」**. Nay SCR-CSV-02 đã có screenshot **riêng** `import-tab.png` (đúng tab インポート, đã đóng dialog cảnh báo Webhook) kèm snapshot `import-tab-snapshot.yml`.<br>⚠ **SCR-CSV-07 KHÔNG có screenshot** — dựng từ source code (`csv_management.blade.php:434-485` + `csv_management.js:44-51`), **chưa quan sát runtime**. Không thể chụp vì phải upload file CSV thật (vi phạm nguyên tắc không thay đổi dữ liệu).<br>⚠ **Đính chính (V-14) giữ nguyên**: `target-count-modal.png` **không** là một màn hình — đó là ảnh chụp trang danh sách sau khi click 「N人」 (hành vi thật là **mở tab mới**, tab hiện tại không đổi; 102.500 bytes ≈ `main.png` 102.505 bytes). Không tính vào số trên |
| Shared components xác nhận | SC-003 (chắc chắn), SC-002 (biến thể) |
| Shared component ứng viên | Sortable List (biến thể **arrow-based**), Friend Info Field Selector, Folder Management Panel (biến thể chỉ-đọc) |
| Background job | **Có** — xác nhận qua ghi chú UI + enum `filter_update_status` (mục 10) |
| Bug/nợ kỹ thuật phát hiện **từ quan sát UI** | **2** — bộ đếm ký tự không init ở form edit; trạng thái FAILURE không hiển thị riêng.<br>⚠ Đã **gỡ "dead link 「N人」"** khỏi danh sách (3 → **2**) — đây là **spec sai**, không phải bug sản phẩm (V-05) |
| Bug sản phẩm **xác nhận từ source + dump** (ngoài quan sát UI) | **3** — (a) `filter_update_status = 40` hiển thị 「作成中」 + **không có đường retry**, **18/208 bản ghi** (§8.1 #6); (b) `filter_update_status = 10` **mồ côi vĩnh viễn**, **4/208 bản ghi** — tổng **22/208 = 10,6%** hiển thị sai sự thật; (c) **import lỗi hiển thị 「完了済」** (báo sai thành công — §8.1 #8) |
| Bug UI phát hiện **từ source code luồng import** (bổ sung lần quét 3) | **3** (đăng ký ở `feature-spec.md` §9 là **B-10 / B-11 / B-12**) — (a) **B-10: 3 nút của SCR-CSV-07 có hành vi giống hệt nhau**: `×`, 「閉じる」, 「インポートする」 đều chỉ `data-dismiss="modal"`, không nút nào import; nhãn 「インポートする」 hứa hẹn sai (`csv_management.blade.php:481-482`); (b) **B-11: khối `uploadingFilterItems` là code chết** — blade render (`:387-393`) nhưng biến không bao giờ được gán (`csv_management.js:109` là nơi khai báo duy nhất); (c) **B-12: kiểm tra đuôi `.csv` phía client đã bị comment** (`csv_management.js:9-13`) → không chặn gì ở client |
| Ước tính độ phủ UI | **~92%** (live) — **Cao**. Còn thiếu **quan sát live**: menu `•••`, trang copy, tóm tắt 「絞り込み条件」 khi có điều kiện, **và toàn bộ SCR-CSV-07** (chỉ có mô tả từ source). Độ phủ **mô tả** (live + source) ~**96%** |

---

## 10. Enum trạng thái (bổ sung từ web-analyzer)

> Nguồn: source code Laravel + hằng số Java. Độ tin cậy: **Cao**.

### `csv_management.filter_update_status` — trạng thái tạo file export (SCR-CSV-01)

| Giá trị | Ý nghĩa | Ai ghi | Số bản ghi trong dump (208) | Nút hiển thị trên UI |
|---------|---------|--------|------------------------------|---------------------|
| `1` | `STATUS_NEW` — mới tạo, chờ job xử lý | Laravel `saveFilter()` (`CsvManagementController.php:565`) | 0 | 「作成中」 (disabled) |
| `2` | `STATUS_IN_QUEUE` — đã vào hàng đợi trong bộ nhớ job | Chỉ Spring Boot (`HandleExportCsvManager.java:66`) | 0 | 「作成中」 (disabled) |
| `10` | ⚠ **Trạng thái MỒ CÔI** — chờ tính lại `total_line_user` (nhánh cũ) | **KHÔNG ai** — writer đã bị gỡ; chỉ còn reader `HandleUpdateLatestInformationCsv.php:48`, command không được `schedule()` (`Kernel.php:98`) | **4** — kẹt vĩnh viễn | 「作成中」 (disabled) **vĩnh viễn**, không có đường thoát |
| `20` | `STATUS_RELOAD` — vừa sửa hoặc vừa bấm 「最新情報に更新」 | Laravel (`:522`, `:949`) | 0 | 「作成中」 (disabled) |
| `30` | **`STATUS_DONE`** — file đã tạo xong | Job | **186** | **「CSVダウンロード」 (enabled) CHỈ KHI `total_line_user > 0`**; nếu `= 0` → 「作成中」 (disabled) |
| `40` | `STATUS_FAILURE` — tạo file thất bại | Chỉ Spring Boot (`HandleExportCsvTask.java:56`) | **18** | 「作成中」 (disabled) ⚠ UI **không phân biệt** với trạng thái đang chờ |
| `88` | `STATUS_RUNNING` — job đang chạy | Job | 0 | 「作成中」 (disabled) |
| `99` | **Marker khoá “đã nhận / đang xử lý”** — **KHÔNG phải lỗi**; đặt **trước** khối `try` (`HandleUpdateLatestInformationCsv.php:56-59`), xong → về `20` | Command Laravel `handle:update_latest_information_csv` | **0** | 「作成中」 (disabled) |

> ✅ **Đính chính điều kiện render (V-06)** — UI chia **2 nhánh** nhưng điều kiện đầy đủ có **2 vế** (`csv_management.blade.php:309-317`, khớp `logic-spec.md` BR-09):
> - `filter_update_status == 30` **VÀ** `total_line_user > 0` → 「最新情報に更新」 + 「CSVダウンロード」 **đều bật** (`:311`)
> - `filter_update_status == 30` **VÀ** `total_line_user == 0` → 「最新情報に更新」 bật, badge 「作成中」 disabled (`:312`)
> - mọi giá trị khác `30` → **cả hai nút disabled** (`:314-317`) → **không có đường retry từ UI**
>
> Dữ liệu mẫu: bản ghi `id=890` ở `30` với `total_line_user = 1` → nút tải bật. Bản ghi `id=928` hiển thị 「0人」 + 「作成中」 → **không phải job chưa xong** mà do `total_line_user = 0`.
>
> ⚠ **Tác động thật (V-04)**: **18 (`40`) + 4 (`10`) = 22/208 = 10,6%** bản ghi đang hiển thị 「作成中」 **sai sự thật**. Độ tin cậy toàn bảng: **Cao**.

### `csv_filter_upload_history.upload_status` — trạng thái import (SCR-CSV-02)

| Giá trị | Hằng số Java | Ý nghĩa | Ai ghi | Số bản ghi trong dump (302) | Blade render |
|---------|--------------|---------|--------|------------------------------|--------------|
| `1` | `STATUS_WAIT` | Chờ xử lý (**DEFAULT của cột**) | Laravel `saveFileCsv()` — không truyền giá trị | 0 | 「作業中」 |
| `100` | `STATUS_IN_QUEUE` | Đã nạp vào queue trong bộ nhớ job | ⚠ **CHỈ Spring Boot** (`HandleImportCsvManager.java:63`; hằng `CsvFilterUploadHistory.java:13`). Laravel không ghi, không poll | 0 | 「作業中」 |
| `77` | `STATUS_RUNNING` | Đang chạy | Cả Laravel command (`HandleImportCsv.php:79`) và Spring Boot | 0 | 「作業中」 |
| `2` | `STATUS_DONE` | Hoàn tất | Laravel command; ⚠ **Spring Boot đặt `2` ở MỌI nhánh kết thúc, KỂ CẢ khi exception** (`HandleImportCsvTask.java:79-80, :99-100`) | **300** | 「完了済」 |
| `103` | — (không có ở Java) | Lỗi | ⚠ **CHỈ Laravel command `handle:import_csv`** (`HandleImportCsv.php:130`, khối `catch`) — luồng di sản | **2** (cả hai từ **2023-02-01**) | 「作業中」 **vĩnh viễn** |

> **Cách render** (`csv_management.blade.php:383-384`) chỉ có **2 nhánh**: `upload_status == 2` → 「完了済」; `v-else` → 「作業中」.
>
> ⚠ **Bổ sung (V-07)**: giá trị `100` trước đây **bị thiếu** trong bảng này — nay đã bổ sung.
> ⚠ **Bug sản phẩm (V-03)**: ở luồng Java hiện hành, import **thất bại** vẫn về `2` → UI hiển thị 「**完了済**」 → **báo sai thành công** (xem §8.1 #8).
>
> Chưa quan sát trực tiếp được trên UI vì bảng 「インポート履歴」 đang rỗng trên tài khoản test — nhưng **enum + cách render đọc trực tiếp từ source, độ tin cậy Cao**.
