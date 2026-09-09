<!-- AUTO-GENERATED bởi scripts/build_indexes.py từ framework/catalog-lme.md — KHÔNG sửa tay. Sửa file gốc rồi chạy lại script. -->

# Index catalog LME — tầng 2 (138 mục)

> Dùng sau khi đã chọn quan điểm ở [checklist-lme.index.md](checklist-lme.index.md).
> **Tick ◯ một quan điểm ở tầng 1 → BẮT BUỘC mở đúng mục catalog tương ứng ở đây.** Bỏ bước hai là chỗ bug lọt.
>
> ```
> sed -n '<Dòng>p' framework/catalog-lme.md
> ```
>
> **KHÔNG nạp toàn văn** [catalog-lme.md](catalog-lme.md) (375 dòng ≈ 14k token).

## 1. Khối catalog

| Khối | Nội dung | Dòng |
|---|---|---|
| **Catalog A** | Ma trận dữ liệu nhập theo kiểu input | 22,157 |
| **Catalog B** | Checklist giao diện theo thành phần | 159,181 |
| **Catalog C** | Bản đồ tính năng dùng chung | 183,301 |
| **Catalog D** | Khác biệt Dev / Staging / Production | 303,322 |
| **Catalog D2** | Checklist tầng job nền | 324,337 |
| **Catalog E** | Giới hạn và ma trận media | 339,375 |

## 2. Tra ngược — quan điểm ◯ thì phải mở mục catalog nào

| Quan điểm | Mục catalog phải mở | Dòng |
|---|---|---|
| `BULK-001` | DI-12 (Checkbox "Chọn tất cả") | 95,100 |
| `COMPAT-LEGACY-001` | MAP-SEND-03 (Job) · MAP-SEND-04 (Job) · MAP-GS-07 (Chung) · MAP-LIFF-04 (Link cũ và link mới) · ENV-DOMAIN (Domain ứng dụng) | 194 · 195 · 249 · 291 · 313 |
| `CONC-001` | DI-18 (Import CSV) · DI-21 (Toggle / Switch) · MAP-PLAN-04 (Mở 2 tab rồi cùng thao tác tại ngưỡng giới hạn) · MAP-PLAN-05 (Double click ở lần tạo cuối cùng trước khi chạm giới hạn) · JOB-03 (Job callback) | 133,137 · 151,155 · 264 · 265 · 332 |
| `CONC-002` | JOB-06 (Mọi job) | 335 |
| `CONC-003` | DI-20 (Ô tìm kiếm) · UIC-09 (Phân trang & Scroll) · UIC-10 (Tab) | 145,149 · 173 · 174 |
| `DATA-001` | MAP-FI-03 (Web — hiển thị) · MAP-FI-06 (Web — cập nhật) · MAP-TAG-01 (Web — hiển thị) · MAP-TAG-03 (Web — cập nhật) | 220 · 223 · 233 · 235 |
| `DATA-BACKUP-001` | MAP-PLAN-03 (Giới hạn lúc khôi phục dữ liệu đã xóa mềm) | 263 |
| `DATA-CACHE-001` | ENV-POPUP (Cache popup) | 320 |
| `DATA-COUNT-001` | DI-04 (Số) · DI-08 (Ngày / Date picker) | 45,49 · 71,75 |
| `DATA-MIG-001` | ENV-PATH (Path media) | 314 |
| `DATA-REF-001` | DI-14 (Dropdown (chọn 1)) · DI-15 (Select box (chọn nhiều)) · MAP-TAG-01 (Web — hiển thị) · MAP-TAG-05 (Chung) · MED-04 (Template) · MED-07 (Scenario) | 108,112 · 114,118 · 233 · 237 · 367 · 370 |
| `DATA-TEXT-001` | DI-01 (Text (1 dòng)) · DI-03 (Rich text (CKEditor / TinyMCE / Quill)) · DI-18 (Import CSV) · DI-20 (Ô tìm kiếm) · MAP-SEND-21 (Chung) | 27,31 · 39,43 · 133,137 · 145,149 · 212 |
| `DEPLOY-ASSET-001` | UIC-01 (Text) · UIC-15 (Icon / Font / Asset) · ENV-ASSET (Cache & asset) | 165 · 179 · 318 |
| `ENV-001` | ENV-LB (Cân bằng tải) · ENV-NEWSRV (Thêm server mới) | 315 · 319 |
| `ENV-003` | DI-16 (Upload ảnh) · UIC-15 (Icon / Font / Asset) · MAP-LIFF-04 (Link cũ và link mới) · ENV-JOB (Job nền) · ENV-MEDIA-STORE (Lưu trữ media) · ENV-MEDIA-DOMAIN (Domain media) · ENV-PATH (Path media) · ENV-LB (Cân bằng tải) …+3 mục | 120,125 · 179 · 291 · 310 · 311 · 312 · 314 · 315 |
| `FRIEND-001` | MAP-FI-01 (—) · MAP-FI-02 (—) · MAP-FI-03 (Web — hiển thị) · MAP-FI-04 (LINE user — hiển thị) · MAP-FI-06 (Web — cập nhật) · MAP-FI-07 (Job — cập nhật) · MAP-FI-08 (LINE user — cập nhật) · MAP-FI-10 (Chung) …+1 mục | 218 · 219 · 220 · 221 · 223 · 224 · 225 · 227 |
| `FUNC-002` | DI-01 (Text (1 dòng)) · DI-02 (Textarea (nhiều dòng)) · DI-11 (Checkbox) · DI-13 (Radio button) · DI-14 (Dropdown (chọn 1)) · DI-18 (Import CSV) | 27,31 · 33,37 · 89,93 · 102,106 · 108,112 · 133,137 |
| `FUNC-003` | DI-01 (Text (1 dòng)) · DI-03 (Rich text (CKEditor / TinyMCE / Quill)) · DI-04 (Số) · DI-05 (URL) · DI-06 (Email) · DI-07 (Số điện thoại Nhật) · UIC-04 (Ô nhập liệu) | 27,31 · 39,43 · 45,49 · 51,56 · 58,62 · 64,69 · 168 |
| `FUNC-004` | DI-01 (Text (1 dòng)) · DI-02 (Textarea (nhiều dòng)) · DI-03 (Rich text (CKEditor / TinyMCE / Quill)) · DI-04 (Số) · DI-07 (Số điện thoại Nhật) · DI-10 (Khoảng ngày (range)) · DI-18 (Import CSV) · MAP-PLAN-01 (Giới hạn lúc tạo mới) | 27,31 · 33,37 · 39,43 · 45,49 · 64,69 · 83,87 · 133,137 · 261 |
| `FUNC-DATE-001` | DI-08 (Ngày / Date picker) · DI-09 (Giờ / Time) · DI-10 (Khoảng ngày (range)) | 71,75 · 77,81 · 83,87 |
| `FUNC-DRAFT-001` | UIC-05 (Modal / Dialog) | 169 |
| `FUNC-MULTI-001` | DI-11 (Checkbox) · DI-12 (Checkbox "Chọn tất cả") · DI-15 (Select box (chọn nhiều)) | 89,93 · 95,100 · 114,118 |
| `FUNC-SEQ-001` | UIC-10 (Tab) · MAP-SORT-01 (Các màn có sort: folder (nhiều màn) · bot ở overview · chat 1:1 (info friend, trạng thái chat) · My page (info friend) · richmenu · image richmenu · scenario · auto reply · form answer · template · tag · QR code · friend info · action schedule · remind · popup · booking event · salon (course, staff, item form) · lesson (course, item form) · quản lý CSV · quản lý item · quản lý staff · conversion · URL) | 174 · 255 |
| `INTG-HOOK-001` | MAP-PAY-02 (Job) · ENV-HOOK (Webhook) · JOB-03 (Job callback) | 273 · 317 · 332 |
| `INTG-HOOK-002` | ENV-HOOK (Webhook) | 317 |
| `INTG-SHEET-001` | DI-19 (Export CSV / Google Spreadsheet) · MAP-GS-01 (Web) · MAP-GS-02 (Web) · MAP-GS-03 (Web) · MAP-GS-06 (Job) | 139,143 · 243 · 244 · 245 · 248 |
| `JOB-001` | MAP-GS-06 (Job) · ENV-JOB (Job nền) · JOB-01 (Job sync (Java)) · JOB-02 (Job sync (Java)) | 248 · 310 · 330 · 331 |
| `LIFF-ENTRY-001` | DI-05 (URL) · MAP-LIFF-01 (Loại link: form, item, event, salon, lesson, conversion, QR code, popup) · MAP-LIFF-02 (Trạng thái kết bạn) · MAP-LIFF-03 (Điểm vào) | 51,56 · 288 · 289 · 290 |
| `LIST-001` | DI-12 (Checkbox "Chọn tất cả") · DI-20 (Ô tìm kiếm) · UIC-08 (Bảng / Danh sách) · UIC-09 (Phân trang & Scroll) | 95,100 · 145,149 · 172 · 173 |
| `MEDIA-001` | DI-16 (Upload ảnh) · DI-17 (Upload video / audio / PDF) · ENV-MEDIA-DOMAIN (Domain media) · MED-01 (Chat 1:1) · MED-03 (Profile người gửi) · MED-04 (Template) · MED-07 (Scenario) · MED-08 (Broadcast (send all)) …+3 mục | 120,125 · 127,131 · 312 · 364 · 366 · 367 · 370 · 371 |
| `MEDIA-CLEAN-001` | DI-16 (Upload ảnh) · DI-17 (Upload video / audio / PDF) · ENV-MEDIA-STORE (Lưu trữ media) · JOB-05 (Job download media) · MED-02 (Friend info) · MED-11 (Mọi tính năng upload) | 120,125 · 127,131 · 311 · 334 · 365 · 374 |
| `MEDIA-IMG-001` | DI-16 (Upload ảnh) · MED-05 (Richmenu) · MED-06 (Image richmenu) | 120,125 · 368 · 369 |
| `MSG-001` | MAP-SEND-01 (Job) · MAP-SEND-05 (Job) · MAP-SEND-06 (Job) · MAP-SEND-11 (Job) · MAP-SEND-12 (Job) · MAP-SEND-14 (Web) · MAP-SEND-18 (Web) · MAP-TAG-05 (Chung) | 192 · 196 · 197 · 202 · 203 · 205 · 209 · 237 |
| `MSG-002` | MAP-SEND-01 (Job) · MAP-SEND-02 (Job) · MAP-SEND-03 (Job) · MAP-SEND-04 (Job) · MAP-SEND-07 (Job) · MAP-SEND-08 (Job) · MAP-SEND-09 (Job) · MAP-SEND-10 (Job) …+1 mục | 192 · 193 · 194 · 195 · 198 · 199 · 200 · 201 |
| `MSG-003` | MAP-SEND-20 (LINE user) | 211 |
| `MSG-004` | MAP-SEND-13 (Web) · MAP-SEND-15 (Web) · MAP-SEND-16 (Web) · MAP-SEND-19 (App admin) · MAP-SEND-21 (Chung) · MAP-FI-10 (Chung) · MED-03 (Profile người gửi) | 204 · 206 · 207 · 210 · 212 · 227 · 366 |
| `NOTI-MAIL-001` | DI-06 (Email) | 58,62 |
| `OUT-EXPORT-001` | DI-19 (Export CSV / Google Spreadsheet) · MAP-GS-04 (Web) · MAP-GS-05 (Web) · MAP-GS-07 (Chung) | 139,143 · 246 · 247 · 249 |
| `OUT-PREVIEW-001` | MAP-SEND-15 (Web) · MAP-SEND-21 (Chung) · MED-04 (Template) · MED-08 (Broadcast (send all)) · MED-12 (Mọi tính năng upload) | 206 · 212 · 367 · 371 · 375 |
| `OUT-TRUTH-001` | UIC-11 (Loading / Rỗng / Lỗi) · MAP-GS-03 (Web) | 175 · 245 |
| `PAY-ABANDON-001` | MAP-PAY-01 (Web) · MAP-PAY-02 (Job) | 272 · 273 |
| `PAY-LIMIT-001` | MAP-PLAN-01 (Giới hạn lúc tạo mới) · MAP-PLAN-02 (Giới hạn lúc copy / nhân bản) · MAP-PLAN-03 (Giới hạn lúc khôi phục dữ liệu đã xóa mềm) · MAP-PLAN-04 (Mở 2 tab rồi cùng thao tác tại ngưỡng giới hạn) · MAP-PLAN-05 (Double click ở lần tạo cuối cùng trước khi chạm giới hạn) · MAP-PLAN-06 (Chức năng KHÔNG phụ thuộc gói vẫn phải test trên nhiều gói) | 261 · 262 · 263 · 264 · 265 · 266 |
| `PAY-PLAN-001` | MAP-CANCEL-04 (Chung) | 282 |
| `PAY-STATE-001` | MAP-PAY-01 (Web) · ENV-PAY (Bill tiền) | 272 · 316 |
| `PERF-LARGE-001` | DI-19 (Export CSV / Google Spreadsheet) · UIC-08 (Bảng / Danh sách) | 139,143 · 172 |
| `PERM-001` | MAP-PERM-01 (Ma trận tài khoản) | 297 |
| `PERM-002` | MAP-PERM-02 (Đường truy cập khi staff không có quyền) · MAP-PERM-03 (Đổi param ID trên URL sang bot khác hoặc user khác) | 298 · 299 |
| `PERM-003` | MAP-PERM-01 (Ma trận tài khoản) · MAP-PERM-03 (Đổi param ID trên URL sang bot khác hoặc user khác) | 297 · 299 |
| `REG-RUN-001` | JOB-04 (Job broadcast / scenario) | 333 |
| `REG-SHARED-001` | UIC-07 (Tooltip) | 171 |
| `REG-URL-001` | DI-05 (URL) · UIC-03 (Hyperlink) · ENV-DOMAIN (Domain ứng dụng) | 51,56 · 167 · 313 |
| `SEC-001` | DI-07 (Số điện thoại Nhật) | 64,69 |
| `SEC-002` | DI-03 (Rich text (CKEditor / TinyMCE / Quill)) · DI-05 (URL) · DI-20 (Ô tìm kiếm) | 39,43 · 51,56 · 145,149 |
| `STATE-001` | MAP-SEND-08 (Job) | 199 |
| `STATE-CLEAN-001` | MAP-CANCEL-01 (Job) · MAP-CANCEL-02 (Job) · MAP-CANCEL-03 (LINE user) · MAP-CANCEL-04 (Chung) | 279 · 280 · 281 · 282 |
| `STATE-DEP-001` | DI-21 (Toggle / Switch) · MAP-SEND-05 (Job) · MAP-SEND-10 (Job) · MAP-SEND-12 (Job) · MAP-FI-07 (Job — cập nhật) · MED-05 (Richmenu) | 151,155 · 196 · 201 · 203 · 224 · 368 |
| `SYNC-APP-001` | DI-17 (Upload video / audio / PDF) · UIC-13 (Độ phân giải & Trình duyệt) · MAP-SEND-19 (App admin) · MAP-FI-05 (App — hiển thị) · MAP-FI-09 (App — cập nhật) · MAP-FI-10 (Chung) · MAP-TAG-02 (App — hiển thị) · MAP-TAG-04 (App — cập nhật) …+1 mục | 127,131 · 177 · 210 · 222 · 226 · 227 · 234 · 236 |
| `UI-001` | UIC-01 (Text) · UIC-02 (Button) · UIC-03 (Hyperlink) · UIC-05 (Modal / Dialog) · UIC-06 (Box / Card) · UIC-07 (Tooltip) · UIC-12 (Layout & khoảng cách) · UIC-13 (Độ phân giải & Trình duyệt) | 165 · 166 · 167 · 169 · 170 · 171 · 176 · 177 |
| `UI-002` | UIC-13 (Độ phân giải & Trình duyệt) | 177 |
| `UI-003` | UIC-02 (Button) · UIC-11 (Loading / Rỗng / Lỗi) · MAP-GS-02 (Web) | 166 · 175 · 244 |
| `UI-004` | UIC-14 (Bàn phím & Focus) | 178 |
| `UI-FIELD-001` | DI-11 (Checkbox) · DI-13 (Radio button) · DI-14 (Dropdown (chọn 1)) | 89,93 · 102,106 · 108,112 |
| `UI-INPUT-001` | DI-01 (Text (1 dòng)) · DI-02 (Textarea (nhiều dòng)) · UIC-04 (Ô nhập liệu) | 27,31 · 33,37 · 168 |

## 3. Toàn bộ mục catalog

| ID | Khối | Tên | Quan điểm liên kết | Dòng |
|---|---|---|---|---|
| `DI-01` | Catalog A | Text (1 dòng) | `FUNC-002`, `FUNC-003`, `FUNC-004`, `UI-INPUT-001`, `DATA-TEXT-001` | 27,31 |
| `DI-02` | Catalog A | Textarea (nhiều dòng) | `FUNC-002`, `FUNC-004`, `UI-INPUT-001` | 33,37 |
| `DI-03` | Catalog A | Rich text (CKEditor / TinyMCE / Quill) | `FUNC-003`, `FUNC-004`, `SEC-002`, `DATA-TEXT-001` | 39,43 |
| `DI-04` | Catalog A | Số | `FUNC-003`, `FUNC-004`, `DATA-COUNT-001` | 45,49 |
| `DI-05` | Catalog A | URL | `FUNC-003`, `SEC-002`, `REG-URL-001`, `LIFF-ENTRY-001` | 51,56 |
| `DI-06` | Catalog A | Email | `FUNC-003`, `NOTI-MAIL-001` | 58,62 |
| `DI-07` | Catalog A | Số điện thoại Nhật | `FUNC-003`, `FUNC-004`, `SEC-001` | 64,69 |
| `DI-08` | Catalog A | Ngày / Date picker | `FUNC-DATE-001`, `DATA-COUNT-001` | 71,75 |
| `DI-09` | Catalog A | Giờ / Time | `FUNC-DATE-001` | 77,81 |
| `DI-10` | Catalog A | Khoảng ngày (range) | `FUNC-DATE-001`, `FUNC-004` | 83,87 |
| `DI-11` | Catalog A | Checkbox | `FUNC-002`, `FUNC-MULTI-001`, `UI-FIELD-001` | 89,93 |
| `DI-12` | Catalog A | Checkbox "Chọn tất cả" | `BULK-001`, `LIST-001`, `FUNC-MULTI-001` | 95,100 |
| `DI-13` | Catalog A | Radio button | `FUNC-002`, `UI-FIELD-001` | 102,106 |
| `DI-14` | Catalog A | Dropdown (chọn 1) | `FUNC-002`, `DATA-REF-001`, `UI-FIELD-001` | 108,112 |
| `DI-15` | Catalog A | Select box (chọn nhiều) | `FUNC-MULTI-001`, `DATA-REF-001` | 114,118 |
| `DI-16` | Catalog A | Upload ảnh | `MEDIA-001`, `MEDIA-IMG-001`, `MEDIA-CLEAN-001`, `ENV-003` | 120,125 |
| `DI-17` | Catalog A | Upload video / audio / PDF | `MEDIA-001`, `MEDIA-CLEAN-001`, `SYNC-APP-001` | 127,131 |
| `DI-18` | Catalog A | Import CSV | `FUNC-002`, `FUNC-004`, `CONC-001`, `DATA-TEXT-001` | 133,137 |
| `DI-19` | Catalog A | Export CSV / Google Spreadsheet | `OUT-EXPORT-001`, `INTG-SHEET-001`, `PERF-LARGE-001` | 139,143 |
| `DI-20` | Catalog A | Ô tìm kiếm | `LIST-001`, `CONC-003`, `DATA-TEXT-001`, `SEC-002` | 145,149 |
| `DI-21` | Catalog A | Toggle / Switch | `CONC-001`, `STATE-DEP-001` | 151,155 |
| `UIC-01` | Catalog B | Text | `UI-001`, `DEPLOY-ASSET-001` | 165 |
| `UIC-02` | Catalog B | Button | `UI-001`, `UI-003` | 166 |
| `UIC-03` | Catalog B | Hyperlink | `UI-001`, `REG-URL-001` | 167 |
| `UIC-04` | Catalog B | Ô nhập liệu | `UI-INPUT-001`, `FUNC-003` | 168 |
| `UIC-05` | Catalog B | Modal / Dialog | `UI-001`, `FUNC-DRAFT-001` | 169 |
| `UIC-06` | Catalog B | Box / Card | `UI-001` | 170 |
| `UIC-07` | Catalog B | Tooltip | `UI-001`, `REG-SHARED-001` | 171 |
| `UIC-08` | Catalog B | Bảng / Danh sách | `LIST-001`, `PERF-LARGE-001` | 172 |
| `UIC-09` | Catalog B | Phân trang & Scroll | `LIST-001`, `CONC-003` | 173 |
| `UIC-10` | Catalog B | Tab | `CONC-003`, `FUNC-SEQ-001` | 174 |
| `UIC-11` | Catalog B | Loading / Rỗng / Lỗi | `UI-003`, `OUT-TRUTH-001` | 175 |
| `UIC-12` | Catalog B | Layout & khoảng cách | `UI-001` | 176 |
| `UIC-13` | Catalog B | Độ phân giải & Trình duyệt | `UI-001`, `UI-002`, `SYNC-APP-001` | 177 |
| `UIC-14` | Catalog B | Bàn phím & Focus | `UI-004` | 178 |
| `UIC-15` | Catalog B | Icon / Font / Asset | `DEPLOY-ASSET-001`, `ENV-003` | 179 |
| `MAP-SEND-01` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-001`, `MSG-002` | 192 |
| `MAP-SEND-02` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002` | 193 |
| `MAP-SEND-03` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002`, `COMPAT-LEGACY-001` | 194 |
| `MAP-SEND-04` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002`, `COMPAT-LEGACY-001` | 195 |
| `MAP-SEND-05` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-001`, `STATE-DEP-001` | 196 |
| `MAP-SEND-06` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-001` | 197 |
| `MAP-SEND-07` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002` | 198 |
| `MAP-SEND-08` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002`, `STATE-001` | 199 |
| `MAP-SEND-09` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002` | 200 |
| `MAP-SEND-10` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-002`, `STATE-DEP-001` | 201 |
| `MAP-SEND-11` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-001` | 202 |
| `MAP-SEND-12` | Catalog C / C.1 Send message — 21 đường gửi tin | Job | `MSG-001`, `STATE-DEP-001` | 203 |
| `MAP-SEND-13` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `MSG-004` | 204 |
| `MAP-SEND-14` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `MSG-001` | 205 |
| `MAP-SEND-15` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `OUT-PREVIEW-001`, `MSG-004` | 206 |
| `MAP-SEND-16` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `MSG-004` | 207 |
| `MAP-SEND-17` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `MSG-002` | 208 |
| `MAP-SEND-18` | Catalog C / C.1 Send message — 21 đường gửi tin | Web | `MSG-001` | 209 |
| `MAP-SEND-19` | Catalog C / C.1 Send message — 21 đường gửi tin | App admin | `SYNC-APP-001`, `MSG-004` | 210 |
| `MAP-SEND-20` | Catalog C / C.1 Send message — 21 đường gửi tin | LINE user | `MSG-003` | 211 |
| `MAP-SEND-21` | Catalog C / C.1 Send message — 21 đường gửi tin | Chung | `MSG-004`, `OUT-PREVIEW-001`, `DATA-TEXT-001` | 212 |
| `MAP-FI-01` | Catalog C / C.2 Friend info | — | `FRIEND-001` | 218 |
| `MAP-FI-02` | Catalog C / C.2 Friend info | — | `FRIEND-001` | 219 |
| `MAP-FI-03` | Catalog C / C.2 Friend info | Web — hiển thị | `FRIEND-001`, `DATA-001` | 220 |
| `MAP-FI-04` | Catalog C / C.2 Friend info | LINE user — hiển thị | `FRIEND-001` | 221 |
| `MAP-FI-05` | Catalog C / C.2 Friend info | App — hiển thị | `SYNC-APP-001` | 222 |
| `MAP-FI-06` | Catalog C / C.2 Friend info | Web — cập nhật | `FRIEND-001`, `DATA-001` | 223 |
| `MAP-FI-07` | Catalog C / C.2 Friend info | Job — cập nhật | `FRIEND-001`, `STATE-DEP-001` | 224 |
| `MAP-FI-08` | Catalog C / C.2 Friend info | LINE user — cập nhật | `FRIEND-001` | 225 |
| `MAP-FI-09` | Catalog C / C.2 Friend info | App — cập nhật | `SYNC-APP-001` | 226 |
| `MAP-FI-10` | Catalog C / C.2 Friend info | Chung | `FRIEND-001`, `MSG-004`, `SYNC-APP-001` | 227 |
| `MAP-TAG-01` | Catalog C / C.3 Tag | Web — hiển thị | `DATA-001`, `DATA-REF-001` | 233 |
| `MAP-TAG-02` | Catalog C / C.3 Tag | App — hiển thị | `SYNC-APP-001` | 234 |
| `MAP-TAG-03` | Catalog C / C.3 Tag | Web — cập nhật | `DATA-001` | 235 |
| `MAP-TAG-04` | Catalog C / C.3 Tag | App — cập nhật | `SYNC-APP-001` | 236 |
| `MAP-TAG-05` | Catalog C / C.3 Tag | Chung | `DATA-REF-001`, `MSG-001` | 237 |
| `MAP-GS-01` | Catalog C / C.4 Google Spreadsheet | Web | `INTG-SHEET-001` | 243 |
| `MAP-GS-02` | Catalog C / C.4 Google Spreadsheet | Web | `INTG-SHEET-001`, `UI-003` | 244 |
| `MAP-GS-03` | Catalog C / C.4 Google Spreadsheet | Web | `INTG-SHEET-001`, `OUT-TRUTH-001` | 245 |
| `MAP-GS-04` | Catalog C / C.4 Google Spreadsheet | Web | `OUT-EXPORT-001` | 246 |
| `MAP-GS-05` | Catalog C / C.4 Google Spreadsheet | Web | `OUT-EXPORT-001` | 247 |
| `MAP-GS-06` | Catalog C / C.4 Google Spreadsheet | Job | `JOB-001`, `INTG-SHEET-001` | 248 |
| `MAP-GS-07` | Catalog C / C.4 Google Spreadsheet | Chung | `COMPAT-LEGACY-001`, `OUT-EXPORT-001` | 249 |
| `MAP-SORT-01` | Catalog C / C.5 Sort — 25 màn | Các màn có sort: folder (nhiều màn) · bot ở overview · chat 1:1 (info… | `FUNC-SEQ-001` | 255 |
| `MAP-PLAN-01` | Catalog C / C.6 Giới hạn theo gói | Giới hạn lúc tạo mới | `PAY-LIMIT-001`, `FUNC-004` | 261 |
| `MAP-PLAN-02` | Catalog C / C.6 Giới hạn theo gói | Giới hạn lúc copy / nhân bản | `PAY-LIMIT-001` | 262 |
| `MAP-PLAN-03` | Catalog C / C.6 Giới hạn theo gói | Giới hạn lúc khôi phục dữ liệu đã xóa mềm | `PAY-LIMIT-001`, `DATA-BACKUP-001` | 263 |
| `MAP-PLAN-04` | Catalog C / C.6 Giới hạn theo gói | Mở 2 tab rồi cùng thao tác tại ngưỡng giới hạn | `CONC-001`, `PAY-LIMIT-001` | 264 |
| `MAP-PLAN-05` | Catalog C / C.6 Giới hạn theo gói | Double click ở lần tạo cuối cùng trước khi chạm giới hạn | `CONC-001`, `PAY-LIMIT-001` | 265 |
| `MAP-PLAN-06` | Catalog C / C.6 Giới hạn theo gói | Chức năng KHÔNG phụ thuộc gói vẫn phải test trên nhiều gói | `PAY-LIMIT-001` | 266 |
| `MAP-PAY-01` | Catalog C / C.7 Bill tiền | Web | `PAY-STATE-001`, `PAY-ABANDON-001` | 272 |
| `MAP-PAY-02` | Catalog C / C.7 Bill tiền | Job | `INTG-HOOK-001`, `PAY-ABANDON-001` | 273 |
| `MAP-CANCEL-01` | Catalog C / C.8 Hủy hợp đồng — danh sách dọn dẹp bắt buộc | Job | `STATE-CLEAN-001` | 279 |
| `MAP-CANCEL-02` | Catalog C / C.8 Hủy hợp đồng — danh sách dọn dẹp bắt buộc | Job | `STATE-CLEAN-001` | 280 |
| `MAP-CANCEL-03` | Catalog C / C.8 Hủy hợp đồng — danh sách dọn dẹp bắt buộc | LINE user | `STATE-CLEAN-001` | 281 |
| `MAP-CANCEL-04` | Catalog C / C.8 Hủy hợp đồng — danh sách dọn dẹp bắt buộc | Chung | `STATE-CLEAN-001`, `PAY-PLAN-001` | 282 |
| `MAP-LIFF-01` | Catalog C / C.9 Link phía LINE user | Loại link: form, item, event, salon, lesson, conversion, QR code, pop… | `LIFF-ENTRY-001` | 288 |
| `MAP-LIFF-02` | Catalog C / C.9 Link phía LINE user | Trạng thái kết bạn | `LIFF-ENTRY-001` | 289 |
| `MAP-LIFF-03` | Catalog C / C.9 Link phía LINE user | Điểm vào | `LIFF-ENTRY-001` | 290 |
| `MAP-LIFF-04` | Catalog C / C.9 Link phía LINE user | Link cũ và link mới | `COMPAT-LEGACY-001`, `ENV-003` | 291 |
| `MAP-PERM-01` | Catalog C / C.10 Phân quyền | Ma trận tài khoản | `PERM-001`, `PERM-003` | 297 |
| `MAP-PERM-02` | Catalog C / C.10 Phân quyền | Đường truy cập khi staff không có quyền | `PERM-002` | 298 |
| `MAP-PERM-03` | Catalog C / C.10 Phân quyền | Đổi param ID trên URL sang bot khác hoặc user khác | `PERM-002`, `PERM-003` | 299 |
| `ENV-JOB` | Catalog D | Job nền | `JOB-001`, `ENV-003` | 310 |
| `ENV-MEDIA-STORE` | Catalog D | Lưu trữ media | `MEDIA-CLEAN-001`, `ENV-003` | 311 |
| `ENV-MEDIA-DOMAIN` | Catalog D | Domain media | `ENV-003`, `MEDIA-001` | 312 |
| `ENV-DOMAIN` | Catalog D | Domain ứng dụng | `COMPAT-LEGACY-001`, `REG-URL-001` | 313 |
| `ENV-PATH` | Catalog D | Path media | `ENV-003`, `DATA-MIG-001` | 314 |
| `ENV-LB` | Catalog D | Cân bằng tải | `ENV-001`, `ENV-003` | 315 |
| `ENV-PAY` | Catalog D | Bill tiền | `PAY-STATE-001` | 316 |
| `ENV-HOOK` | Catalog D | Webhook | `INTG-HOOK-001`, `INTG-HOOK-002` | 317 |
| `ENV-ASSET` | Catalog D | Cache & asset | `DEPLOY-ASSET-001` | 318 |
| `ENV-NEWSRV` | Catalog D | Thêm server mới | `ENV-001`, `ENV-003` | 319 |
| `ENV-POPUP` | Catalog D | Cache popup | `DATA-CACHE-001` | 320 |
| `JOB-01` | Catalog D2 | Job sync (Java) | `JOB-001` | 330 |
| `JOB-02` | Catalog D2 | Job sync (Java) | `JOB-001` | 331 |
| `JOB-03` | Catalog D2 | Job callback | `INTG-HOOK-001`, `CONC-001` | 332 |
| `JOB-04` | Catalog D2 | Job broadcast / scenario | `REG-RUN-001` | 333 |
| `JOB-05` | Catalog D2 | Job download media | `MEDIA-CLEAN-001`, `ENV-003` | 334 |
| `JOB-06` | Catalog D2 | Mọi job | `CONC-002` | 335 |
| `MED-L01` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Chat 1:1 (web & app) | — | 349 |
| `MED-L02` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Chat 1:1 (web & app) | — | 350 |
| `MED-L03` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Chat 1:1 (web & app) | — | 351 |
| `MED-L04` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Chat 1:1 (web & app) | — | 352 |
| `MED-L05` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Friend info | — | 353 |
| `MED-L06` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Friend info | — | 354 |
| `MED-L07` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Template | — | 355 |
| `MED-L08` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Template | — | 356 |
| `MED-L09` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Richmenu | — | 357 |
| `MED-L10` | Catalog E / Khối E1 — Giới hạn dung lượng theo nơi sử dụng | Mọi nơi upload ảnh | — | 358 |
| `MED-01` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Chat 1:1 | `MEDIA-001`, `SYNC-APP-001` | 364 |
| `MED-02` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Friend info | `MEDIA-CLEAN-001`, `FRIEND-001` | 365 |
| `MED-03` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Profile người gửi | `MEDIA-001`, `MSG-004` | 366 |
| `MED-04` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Template | `MEDIA-001`, `DATA-REF-001`, `OUT-PREVIEW-001` | 367 |
| `MED-05` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Richmenu | `MEDIA-IMG-001`, `STATE-DEP-001` | 368 |
| `MED-06` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Image richmenu | `MEDIA-IMG-001` | 369 |
| `MED-07` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Scenario | `DATA-REF-001`, `MEDIA-001` | 370 |
| `MED-08` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Broadcast (send all) | `MEDIA-001`, `OUT-PREVIEW-001` | 371 |
| `MED-09` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Remind | `MEDIA-001` | 372 |
| `MED-10` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | QR code | `ENV-003`, `MEDIA-001` | 373 |
| `MED-11` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Mọi tính năng upload | `MEDIA-CLEAN-001` | 374 |
| `MED-12` | Catalog E / Khối E2 — Ma trận tính năng × thao tác | Mọi tính năng upload | `MEDIA-001`, `OUT-PREVIEW-001` | 375 |
