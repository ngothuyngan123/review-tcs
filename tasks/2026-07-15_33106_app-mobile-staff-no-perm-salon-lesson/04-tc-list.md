<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/140V5efYpOzZuZWrY2WQJyZvJy-0FMCe1CCjQsPXyPYQ/edit?gid=1692154674 | sheet=phân quyền trên app | anchor=Main Function -->
<!-- sync-target: https://docs.google.com/spreadsheets/d/140V5efYpOzZuZWrY2WQJyZvJy-0FMCe1CCjQsPXyPYQ/edit?gid=1692154674 -->

# 04 — TC List (do member viết)

> **Task**: #33106 — [App mobile] User staff không được phân quyền vẫn vào được màn Salon và Lesson.
> **Bản chất fix**: thêm `checkHasPermission` vào 2 API mobile list — `getListCalendarSalon` (key `calendar_salon.index`) và `getListCalendarLesson` (key `calendar.index`). Staff không quyền → data rỗng + `permission=false` + message `この機能の操作権限が付与されていません。`. Không ghi/sửa DB.
> **Đây là DELTA** — chỉ viết case mà tab TC cũ "phân quyền trên app" CHƯA cover (tầng API + backend contract + app cũ). Role matrix / multi-bot / grant-revoke chung đã có ở TC cũ → xem §"Reuse TC cũ" cuối file, KHÔNG viết lại.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | v1 |
| Link TC gốc (nếu có) | Tab "phân quyền trên app" — https://docs.google.com/spreadsheets/d/140V5efYpOzZuZWrY2WQJyZvJy-0FMCe1CCjQsPXyPYQ/edit?gid=1692154674 |

**Account test tham khảo (từ header tab TC cũ — STAGING):**
- user chỉ có bot staff: `ngannt22@wru.vn` (bot staff cũ + mới)
- user có bot master: `nguyenthihattttt1999+55@gmail.com` / `Ha@123`
- user vừa master vừa staff: `Thanhntp142@gmail.com` / `12345678`
- staff bot Bot_staging (role 1): `thanhntp94@gmail.com` / `12345678`
- user staff cũ: `dh3802444555449@gmail.com` / `12345678`

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | getListCalendarSalon: staff CÓ quyền calendar_salon.index → xem được list salon (fix không chặn nhầm) | Positive | High | Bot Bot_staging có ≥2 salon. Staff role được cấp quyền màn Salon (`calendar_salon.index` = ON). Login app bằng staff đó. | 1. Owner (web) cấp quyền màn Salon cho staff.<br>2. Staff login app mobile → chọn bot → mở màn Salon (calendar salon).<br>3. Quan sát danh sách + response API `getListCalendarSalon`. | API trả `permission=true`, `data` = đúng danh sách salon của bot (≥2 salon). App mobile hiển thị đầy đủ list salon, thao tác bình thường. KHÔNG hiện message chặn quyền. | Evidence: screenshot màn Salon app thật + response API (`permission=true` + list). Env: Staging. | | |
| TC002 | getListCalendarSalon: staff KHÔNG quyền calendar_salon.index → chặn + message (REPRODUCE #33106) | Negative | High | Bot có ≥1 salon. Staff role KHÔNG được cấp quyền màn Salon (`calendar_salon.index` = OFF). Login app bằng staff đó. | 1. Owner (web) bỏ tick quyền màn Salon của staff → Save.<br>2. Staff login app mobile → chọn bot → mở màn Salon.<br>3. Quan sát màn hình + response API `getListCalendarSalon`. | API trả `permission=false`, `data` **rỗng** (không trả bất kỳ salon nào), `message` = `この機能の操作権限が付与されていません。`. App mobile hiển thị message báo lỗi, **KHÔNG hiển thị list salon**. (Trước fix: vẫn xem được list = bug.) | Evidence: screenshot app thật hiện message + response API (`permission=false`, data rỗng, message đúng chuỗi JP). Env: Staging. | | |
| TC003 | getListCalendarSalon: staff CÓ quyền nhưng bot 0 salon → empty state, KHÔNG nhầm no-permission | Boundary | High | Bot **không có salon nào** (0 record). Staff CÓ quyền màn Salon. | 1. Owner cấp quyền màn Salon cho staff.<br>2. Chuẩn bị bot có 0 salon.<br>3. Staff mở màn Salon trên app → quan sát response + màn hình. | API trả `permission=true`, `data` = rỗng (vì thật sự 0 salon), message empty-list (nếu có). App hiện trạng thái "chưa có salon" (empty state), **KHÔNG** hiện message `この機能の操作権限が付与されていません。`. Phân biệt rõ "rỗng do 0 data" vs "rỗng do không quyền". | Evidence: screenshot app empty state + response API (`permission=true`, data rỗng). Env: Staging. | | |
| TC004 | getListCalendarLesson: staff CÓ quyền calendar.index → xem được list lesson | Positive | High | Bot có ≥2 lesson. Staff role được cấp quyền màn Lesson (`calendar.index` = ON). | 1. Owner cấp quyền màn Lesson cho staff.<br>2. Staff login app → chọn bot → mở màn Lesson (calendar lesson).<br>3. Quan sát danh sách + response `getListCalendarLesson`. | API trả `permission=true`, `data` = đúng list lesson (≥2). App hiển thị đầy đủ list lesson. KHÔNG hiện message chặn. | Evidence: screenshot màn Lesson app thật + response API. Env: Staging. | | |
| TC005 | getListCalendarLesson: staff KHÔNG quyền calendar.index → chặn + message (REPRODUCE #33106) | Negative | High | Bot có ≥1 lesson. Staff role KHÔNG được cấp quyền màn Lesson (`calendar.index` = OFF). | 1. Owner bỏ tick quyền màn Lesson của staff → Save.<br>2. Staff login app → mở màn Lesson.<br>3. Quan sát màn hình + response `getListCalendarLesson`. | API trả `permission=false`, `data` **rỗng**, `message` = `この機能の操作権限が付与されていません。`. App hiển thị message, **KHÔNG hiển thị list lesson**. | Evidence: screenshot app + response API (`permission=false`, data rỗng, message đúng). Env: Staging. | | |
| TC006 | getListCalendarLesson: staff CÓ quyền nhưng bot 0 lesson → empty state, KHÔNG nhầm no-permission | Boundary | High | Bot **không có lesson nào** (0 record). Staff CÓ quyền màn Lesson. | 1. Cấp quyền Lesson cho staff.<br>2. Bot 0 lesson.<br>3. Staff mở màn Lesson → quan sát. | API `permission=true`, `data` rỗng. App hiện empty state "chưa có lesson", KHÔNG hiện message không-quyền. | Evidence: screenshot empty state + response API (`permission=true`, rỗng). Env: Staging. | | |
| TC007 | Quyền Salon/Lesson kiểm ĐỘC LẬP: staff có quyền Salon nhưng KHÔNG quyền Lesson | Boundary | High | Staff được cấp quyền màn Salon (`calendar_salon.index` ON) NHƯNG bỏ quyền màn Lesson (`calendar.index` OFF). Bot có cả salon và lesson. | 1. Owner: tick quyền Salon, bỏ tick quyền Lesson cho staff → Save.<br>2. Staff app → mở màn Salon → mở màn Lesson.<br>3. Quan sát response 2 endpoint. | Màn Salon: `permission=true` + hiện list salon. Màn Lesson: `permission=false` + data rỗng + message `この機能の操作権限が付与されていません。`. 2 endpoint kiểm quyền độc lập, không dùng chung 1 cờ. | Evidence: screenshot cả 2 màn + 2 response API. Env: Staging. | | |
| TC008 | PERM-002 bypass: gọi THẲNG API getListCalendarSalon bằng staff không quyền (bỏ qua UI ẩn menu) | Negative | High | Staff KHÔNG quyền Salon. Có token/session của staff đó. Dùng Postman/proxy bắt request app. | 1. Bắt request `getListCalendarSalon` khi staff có quyền (lấy endpoint + token).<br>2. Bỏ quyền Salon của staff.<br>3. Gọi thẳng endpoint `getListCalendarSalon` bằng token staff (không qua app UI). | API trả `permission=false` + `data` rỗng (KHÔNG trả list salon), message đúng. Xác nhận chặn ở **tầng API**, không chỉ ẩn menu ở app. (TC cũ chỉ test qua UI → gap này là điểm bug lọt.) | Evidence: response API gọi trực tiếp bằng role không quyền (permission=false, data rỗng). Env: Staging. | | |
| TC009 | PERM-002 bypass: gọi THẲNG API getListCalendarLesson bằng staff không quyền | Negative | High | Staff KHÔNG quyền Lesson. Có token staff. Postman/proxy. | 1. Lấy endpoint `getListCalendarLesson` + token staff.<br>2. Bỏ quyền Lesson.<br>3. Gọi thẳng endpoint bằng token staff. | API trả `permission=false` + `data` rỗng, message đúng. Chặn tại tầng API. | Evidence: response API trực tiếp (permission=false, data rỗng). Env: Staging. | | |
| TC010 | PERM-003/SEC-001 scope theo bot: đổi param bot_id sang bot khác staff không thuộc | Boundary | High | Staff thuộc bot A (có quyền Salon ở A), KHÔNG là staff/không quyền bot B. Tạo salon **trùng tên** ở cả bot A và bot B. | 1. Login staff, gọi `getListCalendarSalon` với bot A → OK.<br>2. Đổi param `bot_id`/`master_id` sang bot B, gọi lại bằng token staff.<br>3. Quan sát response. | Bot B: `permission=false`/403, KHÔNG trả salon của bot B. Không lộ salon + booking (PII khách) của tổ chức khác. Salon trùng tên không bị gộp/nhầm giữa 2 bot (WHERE đủ scope bot). | Evidence: response 2 lần gọi (bot A OK, bot B chặn) + xác nhận 2 salon trùng tên độc lập. Env: Staging. | | |
| TC011 | PERM-004: thu hồi quyền Salon khi staff ĐANG đăng nhập app → lần gọi kế tiếp bị chặn | Negative | Medium | Staff đang login app, đang xem màn Salon (có quyền). | 1. Staff mở màn Salon trên app (đang xem list).<br>2. Owner (web) bỏ tick quyền Salon của staff → Save.<br>3. Staff pull-to-refresh / thao tác lại gọi `getListCalendarSalon`. | Lần gọi kế tiếp trả `permission=false` + data rỗng + message. Session cũ KHÔNG còn xem được list salon (quyền thu hồi có hiệu lực ngay ở request tiếp theo). | Evidence: screenshot app trước/sau thu hồi + response API sau thu hồi. Env: Staging. | | |
| TC012 | COMPAT/RULE-09: app mobile bản CŨ (chưa đọc cờ permission) → backend vẫn chặn data | Regression | High | App mobile phiên bản CŨ (build trước fix, chưa đọc field `permission`/`message`). Staff KHÔNG quyền Salon/Lesson. | 1. Cài app bản cũ (hoặc giả lập client cũ chỉ đọc `data`).<br>2. Staff không quyền mở màn Salon và Lesson.<br>3. Quan sát màn hình. | App cũ nhận `data` rỗng từ backend → hiện màn Salon/Lesson **RỖNG**, KHÔNG lộ danh sách salon/lesson (dù app cũ không render message). Backend chặn data an toàn kể cả app chưa đọc cờ. | Evidence: screenshot app bản cũ (màn rỗng, không có list) + response API. Env: Staging + verify bản build cũ thực tế. | | |
| TC013 | REG-SHARED-001: Event booking (getListFolder — mẫu tham chiếu) không bị fix salon/lesson phá | Regression | High | Staff KHÔNG quyền màn Event booking. Bot có event booking. | 1. Bỏ quyền Event booking của staff.<br>2. Staff mở màn Event booking trên app.<br>3. Quan sát. | Event booking vẫn chặn + message `この機能の操作権限が付与されていません。` **như trước fix** (getListFolder không đổi). Fix salon/lesson không gây regression màn event. | Evidence: screenshot màn Event booking app + response. Env: Staging. | | |
| TC014 | REG-SHARED-001 sibling: API KHÁC của salon/lesson (detail, tạo/sửa/xóa/duyệt booking) có enforce quyền? | Regression | High | Staff KHÔNG quyền Salon/Lesson. Bot có salon+lesson+booking. | 1. Bỏ quyền Salon & Lesson của staff.<br>2. Lần lượt gọi/thao tác các API salon-lesson KHÁC list: xem detail salon/lesson, tạo/sửa/xóa booking, duyệt/từ chối booking (app + direct API).<br>3. Quan sát từng endpoint. | Mỗi sibling endpoint hoặc chặn quyền (`permission=false`/403) hoặc — nếu KHÔNG chặn → **ghi nhận NG + báo Dev** (fix #33106 chỉ chạm 2 endpoint list; các endpoint khác có thể vẫn thiếu check quyền). KHÔNG tự kết luận Đạt nếu sibling còn hở. | Evidence: bảng liệt kê từng sibling endpoint + kết quả check quyền. Env: Staging. ⚠️ Hỏi Dev danh sách endpoint salon/lesson đầy đủ (REG-SHARED-001). | | |
| TC015 | SYNC-APP-001: hành vi chặn quyền Salon/Lesson nhất quán giữa Web admin và App mobile | Regression | Medium | Cùng 1 staff KHÔNG quyền Salon/Lesson. | 1. Staff login **web admin** → mở màn Salon & Lesson.<br>2. Cùng staff login **app mobile** → mở màn Salon & Lesson.<br>3. So sánh hành vi 2 surface. | Cả web và app đều chặn + hiển thị message không-quyền. Không còn tình trạng app mobile hở quyền trong khi web chặn (bug gốc là app thiếu check khác web). | Evidence: screenshot cùng thao tác trên web VÀ app. Env: Staging. | | |
| TC016 | REG-SHARED-001 sibling màn Chat 1:1: staff KHÔNG quyền chat11 → list API chặn tại TẦNG API (không chỉ ẩn menu) | Regression | High | Staff KHÔNG quyền màn Chat 1:1 (`chat11` OFF). Bot có hội thoại. Có token staff (Postman/proxy). | 1. Bỏ quyền Chat 1:1 của staff → Save.<br>2. Staff mở màn Chat 1:1 trên app → quan sát.<br>3. **Gọi thẳng list API của màn Chat 1:1** bằng token staff (bỏ qua UI). | App: chặn + message `この機能の操作権限が付与されていません。`. **Direct API: trả `permission=false`/data rỗng** — KHÔNG lộ hội thoại. Nếu API vẫn trả data (chỉ UI ẩn) → NG, cùng lớp bug #33106, báo Dev. | Evidence: response direct API bằng role không quyền + screenshot app. Env: Staging. ⚠️ Hỏi Dev tên endpoint list Chat 1:1. | | |
| TC017 | REG-SHARED-001 sibling màn Form answer: staff KHÔNG quyền formanswer → list API chặn tại TẦNG API | Regression | High | Staff KHÔNG quyền màn Form answer (`formanswer` OFF). Bot có form + answer. Token staff. | 1. Bỏ quyền Form answer của staff → Save.<br>2. Staff mở màn Form answer trên app.<br>3. Gọi thẳng list API màn Form answer bằng token staff. | App: chặn + message. Direct API: `permission=false`/data rỗng — KHÔNG lộ câu trả lời form (PII khách). Nếu API vẫn trả data → NG, báo Dev. | Evidence: response direct API + screenshot app. Env: Staging. ⚠️ Hỏi Dev endpoint list Form answer. | | |
| TC018 | REG-SHARED-001 sibling màn Booking calendar: staff KHÔNG quyền → list API chặn tại TẦNG API | Regression | High | Staff KHÔNG quyền màn Booking calendar (`booking calendar` OFF). Token staff. | 1. Bỏ quyền Booking calendar của staff → Save.<br>2. Staff mở màn Booking calendar trên app.<br>3. Gọi thẳng list API màn Booking calendar bằng token staff. | App: chặn + message. Direct API: `permission=false`/data rỗng. Nếu API vẫn trả data → NG, báo Dev. | Evidence: response direct API + screenshot app. Env: Staging. ⚠️ Hỏi Dev endpoint list Booking calendar. | | |
| TC019 | REG-SHARED-001 màn Notify (list vào được, detail chặn): staff KHÔNG quyền notify → hành vi không regressed | Regression | High | Staff KHÔNG quyền màn Notify (`notify` OFF) — gồm sub: booking calendar / calendar salon / calendar lesson / formanswer / booking event. Token staff. | 1. Bỏ quyền Notify của staff → Save.<br>2. Staff mở màn Notify → vào list → mở từng detail (booking calendar, calendar salon, calendar lesson, formanswer, booking event).<br>3. Gọi thẳng API detail bằng token staff. | Theo spec cũ (tab TC cũ): **vào màn list được**, nhưng **không xem được detail** → hiển thị dòng text đỏ. Direct API detail: `permission=false`/data rỗng. Hành vi này KHÔNG bị fix salon/lesson làm đổi. | Evidence: screenshot list + detail (text đỏ) + response direct API detail. Env: Staging. | | |
| TC020 | REG-SHARED-001: các màn sibling khi staff CÓ quyền vẫn xem bình thường sau fix (không chặn nhầm) | Regression | Medium | Staff được cấp quyền các màn: Chat 1:1, Form answer, Booking calendar, Booking event. Bot có data mỗi màn. | 1. Owner cấp đủ quyền các màn trên cho staff → Save.<br>2. Staff login app → mở lần lượt từng màn.<br>3. Quan sát data + response từng màn. | Mỗi màn có quyền: `permission=true` + hiển thị đầy đủ data, thao tác bình thường. Fix 2 controller salon/lesson KHÔNG gây chặn nhầm ở các màn khác. | Evidence: screenshot từng màn sibling + response `permission=true`. Env: Staging. | | |

### Chú thích cột

- **Type**: `Positive` ≡ Normal · `Negative` ≡ Abnormal · `Boundary` · `Regression` (loại thứ 4).
- **Priority**: theo ưu tiên quan điểm (Cao→High, TB→Medium).
- **Output note**: loại evidence bắt buộc (RULE-02) + env.
- **Assignee/Status**: để trống — QA fill sau khi run.

### Environment (note)

- Mặc định test **Staging** (`staging.lme.jp`) + app mobile trỏ staging.
- **TC012** cần build app **bản cũ thực tế** (verify backend chặn data với client chưa đọc cờ permission).
- **RULE-06 (output cuối chuỗi)**: mọi TC verify tới **màn app mobile thật trên thiết bị** + response API, KHÔNG dừng ở màn admin web.
- **RULE-08**: fix không chạm media/domain/job nền/thanh toán → không bắt buộc verify Production (xem §quan điểm × ENV-003). Nếu Leader muốn chắc do production có loadbalance 2 server → smoke lại TC002/TC005 trên production sau deploy.

---

## Reuse TC cũ (tab "phân quyền trên app" — READ-ONLY, KHÔNG sửa)

Các mảng dưới đây **đã có ở TC cũ** → không viết lại, chỉ tham chiếu:

| Mảng đã cover ở TC cũ | Map quan điểm | Ghi chú |
|---|---|---|
| Cấp quyền / bỏ quyền → vào/không vào các màn (chat11, formanswer, booking calendar, booking event, notify, calendar salon, calendar lesson...) | PERM-001 | TC cũ test **qua UI app** — xem cảnh báo bên dưới |
| Đổi role 1 副管理人 ⇄ 2 運用者 ⇄ 3 サポート (6 hoán vị) | PERM-001 | Reuse toàn bộ, không viết lại |
| Edit quyền: tick→không lưu / đổi tick nhiều lần → save | PERM-001 | Reuse |
| "Spect mới: phân quyền đến từng bot" (multi-bot, chọn bot xem quyền, đồng bộ app) | PERM-003 | Reuse; TC010 chỉ bổ sung chiều **direct-API + WHERE scope theo bot** cho salon/lesson |
| "check list bot" (user master/staff xem list bot) | — | Ngoài scope fix #33106, skip |

⚠️ **TC cũ nghi test THIẾU TẦNG API — member tự verify (KHÔNG sửa TC cũ):**
Các dòng TC cũ "bỏ tick màn → calendar salon / calendar lesson → không vào được" được đánh **OK**, nhưng bug #33106 chứng minh **API list salon/lesson KHÔNG enforce quyền** (chỉ app ẩn menu ở tầng UI). Nghĩa là TC cũ verify qua UI app, chưa verify qua **direct API** → đó là chỗ bug lọt. TC008/TC009/TC012 của file này lấp gap đó. TC cũ giữ nguyên (read-only), member đối chiếu lại thủ công.

⚠️ **MỞ RỘNG REGRESSION SANG CÁC MÀN SIBLING (TC016–TC020):**
Bug #33106 là lớp bug "**list API không enforce quyền dù UI ẩn menu**". Lớp bug này có thể tồn tại ở **mọi màn trong lưới phân quyền app mobile**, không riêng salon/lesson. Toàn bộ các dòng TC cũ đánh OK cho những màn này đều test **qua UI app**, chưa qua **direct API**. Do đó TC016–TC020 rà lại **từng màn sibling ở tầng API**:

| Màn sibling app mobile | TC | Direction chính |
|---|---|---|
| Chat 1:1 (`chat11`) | TC016 | Không quyền → direct API chặn |
| Form answer (`formanswer`) | TC017 | Không quyền → direct API chặn (PII) |
| Booking calendar (`booking calendar`) | TC018 | Không quyền → direct API chặn |
| Notify + sub (booking calendar/salon/lesson/formanswer/event) | TC019 | Không quyền → list vào được, detail chặn (theo spec cũ) |
| Booking event (`getListFolder` — mẫu tham chiếu) | TC013 | Không quyền → chặn như trước fix |
| Tất cả sibling khi CÓ quyền | TC020 | Có quyền → không bị chặn nhầm sau fix |

> Mỗi TC016–TC018 đều ghi ⚠️ **hỏi Dev tên endpoint list** của màn tương ứng (không bịa tên function). Nếu bất kỳ sibling nào direct API vẫn trả data khi không quyền → **NG cùng lớp bug #33106, mở ticket riêng cho Dev**, KHÔNG gộp vào #33106.

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (KHÔNG có file 02 — tham chiếu `templates/LME-SYSTEM-SPEC.md` FA-019 Lesson / FA-020 Salon; member bổ sung file 02 sau)
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [x] Mỗi impact (F1 salon, F2 lesson, T1, T2) có ≥1 TC verify
- [x] Có ≥1 TC reproduce bug (TC002 salon, TC005 lesson)
- [x] Có ≥1 TC regression cho mỗi tính năng 4.3 (T1: TC001-003/012/015; T2: TC004-006/012/015)
- [ ] Member verify lại account test + build app cũ (TC012) trên môi trường thật

### Base quan điểm test LME (2 tầng)

**Tầng 1**: [framework/checklist-lme.md](../../framework/checklist-lme.md) · **Tầng 2**: [framework/catalog-lme.md](../../framework/catalog-lme.md).

| Mã quan điểm | Ưu tiên | ◯/× | Catalog đã mở | TC cover | Lý do nếu × |
|---|---|---|---|---|---|
| FUNC-001 | Cao | ◯ | C | TC001, TC004, TC003, TC006 | Luồng chính: có quyền vẫn xem được list |
| PERM-001 | Cao | ◯ | C (MAP-PERM-01) | TC007 + reuse role matrix TC cũ | Menu/màn theo role |
| PERM-002 | Cao | ◯ | C (MAP-PERM-02/03) | TC002, TC005, TC008, TC009, TC010 | **Core fix**: chặn bypass tầng API |
| PERM-003 | Cao | ◯ | C (MAP-PERM-01/03) | TC010 + reuse "phân quyền từng bot" | Cách ly quyền đa bot |
| PERM-004 | TB (→Cao) | ◯ | — | TC011 | Thu hồi quyền khi đang đăng nhập = đúng root cause |
| SEC-001 | Cao | ◯ | C | TC010 | Cross-account: booking salon/lesson chứa PII khách |
| REG-SHARED-001 | Cao | ◯ | D | TC013, TC014, TC015, **TC016-TC020** | Salon/Lesson/Event là cặp lặp lại; rủi ro sót sibling → rà **mọi màn sibling app** (chat11, formanswer, booking calendar, notify) ở tầng API |
| SYNC-APP-001 | TB | ◯ | C, E | TC015, TC012 | Bug là app mobile khác web |
| COMPAT-LEGACY-001 | Cao | ◯ | C, D | TC012 | App bản cũ chưa đọc cờ permission (RULE-09) |
| DATA-DB-001 | Cao | × | — | — | Fix **read-only**, không UPDATE/DELETE (D1 = không có data change) → không có scope WHERE ghi/xóa để kiểm; scope đọc theo bot đã cover ở TC010 |
| ENV-003 | Cao | × | — | — | Fix thuần logic check quyền tại controller, **không** chạm media/file/domain/job nền/thanh toán/thêm server → không rơi vào trigger RULE-08. *(Leader duyệt: nếu lo loadbalance prod → smoke TC002/005 trên prod.)* |
| LIFF-ENTRY-001 | Cao | × | — | — | Đối tượng là **staff phía quản trị (app admin)**, không phải LINE user access link |
| MSG-* / PAY-* / MEDIA-* / FRIEND-* | — | × | — | — | Fix không chạm gửi tin / thanh toán / media / friend info |
| DATA-001 / DATA-COUNT-001 | Cao | × | — | — | Không cập nhật/không đếm dữ liệu — chỉ thêm cờ check quyền đọc |

- [x] Đã duyệt toàn bộ tầng 1
- [x] Mỗi quan điểm ◯ đã mở catalog tương ứng
- [x] Quan điểm ◯ Cao đủ 3 loại (FUNC/PERM-001/PERM-002/SEC covered Normal+Abnormal+Boundary; REG-SHARED-001 dùng loại Regression — bản chất regression, Normal/Abnormal/Boundary đã cover ở PERM/FUNC)
- [x] Mọi × có lý do; × ở quan điểm Cao (DATA-DB-001, ENV-003, LIFF-ENTRY-001, DATA-001, DATA-COUNT-001) đã ghi lý do cho Leader duyệt (RULE-03)
- [x] TC output ra ngoài → verify tới app mobile thật + response API (RULE-06)
- [ ] RULE-07: fix không có CRUD ghi/xóa → N/A tầng DB write; TC010 kiểm scope đọc theo bot
- [x] Task KHÔNG chạm media/domain/job/bill → ENV-003 × có lý do (RULE-08)
- [x] COMPAT-LEGACY-001: test app cũ + mới (TC012) — RULE-09
- [x] Mỗi TC ghi loại evidence ở Output note (RULE-02)
