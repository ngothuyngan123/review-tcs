# 05 — Review Report

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) MCP LME TEST STUDIO task #512 (ticket 44186) |
| Tổng số TC review | 17 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 10/10 mục có TC — **ĐỦ** |
| **(b) diff code** — suy từ diff thật (Studio `dev_impact` + `spec_delta`) | 5/6 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 15/16 vùng ảnh hưởng đủ TC · 1 GAP · 1 RISK.

> Chiều (a): `BUG` (path traversal + IDOR) · F1 downloadCsv · F2 csvExport · F3 JS exportCsv · D1 `csv_management` query bot_id · D2 JS asset cache · T1 bản ghi cũ · T2 bản ghi mới · T3 link cũ 404 · T4 export cross-bot — mỗi mục ≥ 1 TC pass.
> Chiều (b): spec_delta 2 file runtime (`CsvManagementController.php`, `csv_management.js`) + các điểm `dev_impact` nêu. 1 điểm Studio `dev_impact` nêu rõ chưa có TC (xem G1).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | EP-09 `download-csv` + EP-12 `export` khi **session chưa chọn bot** (`current_bot_id` rỗng → `getBotId()` null) | `diff code` | không có | GAP — `dev_impact` ghi rõ "scope bot giờ dựa **hoàn toàn** vào session `current_bot_id` → rủi ro khi session **không có bot**/đổi bot". Nhánh "đổi bot" đã có NEW-17; nhánh "không có bot" chưa TC nào. EP-09 chỉ có middleware `check_login` (không `basic_access`) nên trạng thái login-nhưng-chưa-chọn-bot **tới được** endpoint | `[MAJOR]` |
| G2 | Nhánh media redirect `path_new=1` → `URL_SERVER_MEDIA` (`p.lmes.jp`) | `diff code` | NEW-10, NEW-15 | RISK — có TC nhưng chỉ chạy `local` + `staging`, **0 lượt prd**. Catalog D `ENV-MEDIA-DOMAIN`: "nút download mở tab mới thay vì tải file / ảnh 404 — **chỉ sai trên production**" (RULE-08). Không kết luận được từ staging | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: ~12 quan điểm Trigger khớp task · 1 chưa cover đủ (do gắn mã nội bộ, không phải thiếu hành vi).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `SEC-002` (chống lộ token / secret / `.env`) | Cao | RISK — hành vi **đã được test** (NEW-1 chặn tải `.env`/file hệ thống, NEW-20 `fileName` độc hại bị bỏ qua) nhưng 2 TC này gắn **mã nội bộ Studio** (`TOOL-KNOW-002` / `SEC-INJECT-001`), không map được sang `SEC-002`/`SEC-001` của khung LME. Đề nghị đổi `Mã quan điểm liên kết` của NEW-1 → `SEC-002`, NEW-20 → `SEC-001` để coverage security truy ngược được. Không cần viết TC mới | `[MAJOR]` |

> Các quan điểm Cao khác **đã cover đủ** (không ghi dòng): `SEC-001` (NEW-5/NEW-12 cross-bot export+download) · `PERM-002` (NEW-12 bypass API) · `PERM-003` (NEW-5/NEW-17 đa bot) · `PERM-001` (NEW-16 staff có quyền) · `COMPAT-LEGACY-001` (NEW-7/9/14 cũ ⇄ NEW-9/10/15 mới, NEW-4 link cũ 404) · `SEC-ISO-001` (NEW-17) · `DEPLOY-ASSET-001` (NEW-18) · `FUNC-001` (NEW-14/15) · `ENV-003` (NEW-10/15 — nhưng RISK prd, xem G2/§5).
> `DATA-DB-001` **không Trigger**: cả 2 hàm sửa đều read-only, Dev xác nhận không UPDATE/DELETE/migration.

---

## 3. TC trùng lặp nội dung

Đã rà 17 TC, **không phát hiện trùng lặp**. Các cặp dễ nhầm đã kiểm:
- NEW-3 (csv_id dị dạng → 404) vs NEW-8 (bản ghi hợp lệ nhưng file mất → 404): khác **điều kiện** (validate input vs file tồn tại) → không trùng.
- NEW-1 (không csv_id + `fileName` độc hại → 404) vs NEW-20 (có csv_id hợp lệ + `fileName` độc hại → tải đúng file): bổ sung nhau (vắng/có csv_id) → không trùng.
- NEW-14 (UI bấm nút, bản ghi cũ) vs NEW-7 (API trực tiếp, bản ghi cũ): khác surface (ui/api) — cố ý giữ cả 2 chiều.
- NEW-9 (bản ghi mới có file local) vs NEW-10 (bản ghi mới không file local → redirect media): khác nhánh code.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-1, NEW-7, NEW-14, NEW-4, NEW-20 | EP-13 `download-csv` nhận gì + hành vi file cũ mất | TC: EP-09/EP-13 **chỉ nhận `csv_id`**, `fileName`/`path_new` bị bỏ qua; bản ghi cũ file mất → **404** | `feature-spec.md` §2.2 Bước G + §6 EP-13 + §9 B-05b: EP-13 **nhận `fileName` từ query** nối thẳng `public_path()` (path traversal); file cũ mất → **exception → 500** | Spec mô tả **trạng thái TRƯỚC fix** (chính là lỗ hổng #44186). Bản fix đã đổi sang `csv_id` + 404 → **spec cũ hơn bản fix, cần update** (TC đúng theo bản fix) | `[MAJOR]` | Dev / PM |

**Đã rà**: 17 TC × `spec-features/admin/csv-management/feature-spec.md` (§2.2 / §5 / §6 / §9) + `kho-tcs` — **kho-tcs chưa có `FA-014`** (FA-013 friend-list ghi chú đã dời CSV sang FA-014 nhưng kho FA-014 chưa build) → không đối chiếu được `CONF-KHO`. `CONF-TC`: không có 2 TC expected loại trừ nhau. `CONF-IGNORE`: `ignore-features.md` chỉ có IG-01 (BookingManager cũ) — task không chạm (BookingEventController ≠ BookingManagerController) → sạch.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | NEW-10, NEW-15 (+ chung cho nhánh media) | **RULE-08 / ENV-003**: nhánh `path_new=1` redirect sang media server (`p.lmes.jp`) và toàn bộ luồng tải file chỉ chạy `local` + `staging`, **0 lượt production**. Catalog D `ENV-MEDIA-DOMAIN` + `ENV-PATH`: hành vi media (mở tab vs tải, 404, path qua B2) chỉ lộ đúng trên prd | Chạy lại tối thiểu NEW-10/NEW-14/NEW-15 trên `prd` trước khi release; `env_scope` các TC này giữ `all` nhưng phải có bằng chứng prd |
| I2 | `[MAJOR]` | NEW-7, NEW-8, NEW-9, NEW-10, NEW-11, NEW-20 | 6 TC `skip`/`need-prep` trên staging (thiếu fixture bản ghi cũ/mới, file local/mất). Chỉ có kết luận trên `local`. Với bug **security** + nhánh file cũ/mới là lõi fix, chỉ verify local là mỏng | Chuẩn bị fixture trên staging/prd (bản ghi `file_name` cũ còn file / mất file, `file_name_new` có/không file local) rồi chạy lại 6 TC này; hoặc Leader chấp nhận bằng chứng local + ghi rõ |
| I3 | `[MINOR]` | Phạm vi task (ngoài fix) | **B-06 / BR-21**: Staff bị ẩn menu 「CSV管理」 vẫn gọi thẳng được API CSV (EP-09/EP-12 nhóm `/ajax` + `download-csv` chỉ có `check_login`, không kiểm custom-role). Fix #44186 **không đụng middleware** nên lỗ hổng này vẫn còn; NEW-16 chỉ test staff **có** quyền | Ngoài scope task — Dev đã ghi follow-up. Đề nghị Leader mở ticket riêng cho phân quyền staff trên route AJAX CSV |
| I4 | `[NIT]` | Phạm vi task (ngoài fix) | **REG-SHARED-001**: các hàm `downloadCsv` cùng mẫu path traversal chưa fix — `Basic\BookingEventController::downloadCsv`, `Admin\UserController::downloadCsv*`, `Admin\AffiliateInfoController::downloadCsv`. Dev đã liệt kê trong handoff | Mở ticket bảo mật riêng (Dev đã đề xuất). Không thuộc bộ TC task này |
| I5 | `[NIT]` | NEW-15 | Lượt chạy `local` ra `error` do lỗi Console `PushManager.subscribe` (bug automation **#4026**) — Dev đã xác nhận KHÔNG phải bug thật (`VAPID_PUBLIC_KEY` sai ở local). Lượt staging mới nhất đã `pass` | Khi chấm NEW-15 loại trừ riêng lỗi PushManager.subscribe (đã có bằng chứng base) hoặc chạy trên env có VAPID hợp lệ — như note TC đã ghi |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 17 TC — **không có TC nào ngoài phạm vi task**. Mọi TC map được vào `BUG`/F1–F3/D1–D2/T1–T4 hoặc điểm sửa trong `spec_delta` (`CsvManagementController.php`, `csv_management.js`). NEW-18 (cache JS) map D2 + `dev_impact` "JS không bump version".

---

## 7. TCs đề xuất bổ sung (2)

**Đã đối chiếu trước khi viết** (BƯỚC 5a/5b):

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs` **chưa có `FA-014`** — không đối chiếu được; đã rà FA-012/FA-013/FA-033 (các TC chạm CSV管理 là tag-import / copy-bot, khác nhánh) |
| Vùng regression phát hiện từ kho | Không có (kho FA-014 chưa build) |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | Không có TC R — sibling `downloadCsv` khác (BookingEvent/User/Affiliate) Dev scope sang ticket riêng, không đẻ TC ở task này |
| Xác nhận chống trùng | Đã đối chiếu 17 TC ở BƯỚC 0 — không TC đề xuất nào trùng (G1 kiểm nhánh `current_bot_id` rỗng, chưa TC nào chạm) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-PERM003-01 | API | PERM-003 | EP-09 `GET /basic/csv-management/download-csv`: tải CSV khi phiên **chưa chọn bot** | Abnormal | auto | dev, local, prd, staging | api | `download-csv?csv_id=<id hợp lệ>` khi `current_bot_id` rỗng → 404, không lộ file | - Tài khoản admin hợp lệ, đã đăng nhập thật qua `/login-v2` (có session cookie + CSRF) nhưng **CHƯA chọn bot nào** trong phiên (`current_bot_id` null/rỗng) — VD vừa login, chưa vào màn chọn bot, hoặc session mất `current_bot_id`.<br>- Biết 1 `csv_id` thật của 1 bot bất kỳ (bản ghi `status==30`, đã tải được bởi chủ) để làm dữ liệu gửi. | 1. Trong phiên chưa chọn bot, gửi `GET /basic/csv-management/download-csv?csv_id=<id thật của 1 bot>`.<br>2. Ghi mã HTTP + thân phản hồi; xác nhận không có `Content-Disposition: attachment`. | `csv_id=<id bản ghi CSV thật của 1 bot>` (không có bot trong session) | - HTTP **404** (trang 404), KHÔNG tải file.<br>- Không trả 500, không lộ đường dẫn / nội dung file.<br>- `getBotId()` null → query `where id & bot_id=null` không khớp bản ghi nào → 404. | | Lấp G1 · Đánh giá spec: Spec không ghi (hỏi Dev — `dev_impact` chỉ nêu "rủi ro khi session không có bot", chưa chốt expected) · Evidence: mã HTTP + response của request trực tiếp (RULE-13) |
| TC-PERM003-02 | API | PERM-003 | EP-12 `POST /basic/csv-management/export`: lấy đường dẫn file khi phiên **chưa chọn bot** | Abnormal | auto | dev, local, prd, staging | api | `export` với `csv_id` hợp lệ khi `current_bot_id` rỗng → `file_name` rỗng, không 500 | - Tài khoản admin hợp lệ, đã đăng nhập thật nhưng **CHƯA chọn bot** (`current_bot_id` null/rỗng).<br>- Có CSRF hợp lệ.<br>- Biết 1 `csv_id` thật của 1 bot bất kỳ. | 1. Trong phiên chưa chọn bot, gửi `POST /basic/csv-management/export` với `csv_id=<id thật>` + CSRF.<br>2. Ghi mã HTTP + JSON trả về. | `csv_id=<id bản ghi CSV thật của 1 bot>` (không có bot trong session) | - HTTP **200**, JSON `success=true`, `file_name=''` (rỗng), `path_new=0`.<br>- `where bot_id=getBotId()` với `getBotId()` null → không khớp → trả rỗng, KHÔNG 500, không lộ path của bot nào.<br>- Hệ quả FE: không có đường dẫn để tải. | | Lấp G1 · Đánh giá spec: Spec không ghi (hỏi Dev) · Evidence: mã HTTP + JSON của request trực tiếp (RULE-13) |

> ⚠️ G2 (nhánh media redirect chưa chạy prd) **không đẻ TC mới** — TC đã có (NEW-10/NEW-15), chỉ cần chạy bổ sung trên `prd` (xem §5 I1).

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/csv-management/feature-spec.md` §2.2 Bước G · §6 EP-12/EP-13 · §9 B-05b | Cập nhật theo bản fix #44186: EP-13 `download-csv` **chỉ nhận `csv_id`** (bỏ `fileName`/`path_new`), tra `csv_management` theo `id` + `bot_id` hiện tại; bản ghi cũ file mất → **404** (không còn 500); EP-12 `export` thêm `where bot_id=getBotId()`, bot khác → `file_name` rỗng. §9 B-05b/B-05c (path traversal + IDOR) đã được vá → chuyển từ "lỗ hổng hiện tại" sang "đã fix ở #44186" | C1 (`CONF-SPEC` ở §4) | Dev / PM |
