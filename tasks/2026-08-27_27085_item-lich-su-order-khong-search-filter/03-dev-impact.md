# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) |
| Commit / Pull Request | commit `094d72da6e` (repo `sns-line`) — Redmine không đính link Github/Gitlab |
| Branch | `ai_fixbug_27085` (nhánh gốc `release_step_20260805`, 1 file) — **đã push** |
| Ngày submit đánh giá | `2026-08-26` |
| Auto-filled | `2026-08-27 by /new-task` |
| Nguồn | Redmine #27085 — journal id `133031` by `AI LME Fix bug` at `2026-08-26T04:33:08Z` |

> ⚠️ **Branch có 2 giá trị khác nhau trong lịch sử ticket — cần Leader xác nhận trước khi test:**
> - Journal `115489` (2026-03-27, by **Nguyen Ngoc Hai**): `branch: fix-bug-27083`
> - Journal `133031` (2026-08-26, by **AI LME Fix bug**): `ai_fixbug_27085`
>
> Task trên MCP LME TEST STUDIO (`task_id=228`) đang khai báo `branch = fix-bug-27083` (branch cũ) — xem cảnh báo ở [04-tc-list.md](04-tc-list.md).

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn từ Redmine journal 133031, mục "■ 1. NGUYÊN NHÂN" -->

Màn Lịch sử order giữ nguyên số trang đang xem khi người dùng bấm tìm kiếm hoặc lọc. Các thao tác đổi điều kiện chỉ gọi lại API danh sách mà không đưa trang về 1, nên request vẫn kèm số trang cũ. Sau khi lọc, kết quả thường chỉ còn 1 trang nên máy chủ trả về trang 2 rỗng: bảng trắng và thanh phân trang biến mất, người dùng tưởng là không tìm/lọc được.

## 2. Cách fix

<!-- Nguyên văn từ Redmine journal 133031, mục "■ 2. CÁCH FIX" -->

Đưa danh sách về trang 1 trước khi tải lại ở mọi thao tác đổi điều kiện lọc trên màn Lịch sử order: tìm theo từ khóa, áp dụng bộ lọc, đổi khoảng ngày, đổi môi trường bản chính/thử nghiệm và đổi tab hàng đơn lẻ/hàng định kỳ. Chỉ thao tác bấm số trang mới giữ nguyên trang như cũ. Quét ngang thấy màn Chi tiết sản phẩm còn cùng lỗi khi đổi tháng, đã ghi vào danh sách theo dõi (không sửa vì ngoài phạm vi ticket).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn từ Redmine journal 133031, mục "■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN" -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `getListOrderHistory` — `public/js/sales/v2/list-order-history.js` | Nhận tham số trang | Hàm dùng chung nạp danh sách cho cả 2 tab |
| 2 | `searchByNameFriendOrItem` — `public/js/sales/v2/list-order-history.js` | Đưa về trang 1 trước khi tải lại | Thao tác đổi điều kiện lọc (tìm theo từ khóa) |
| 3 | `filter` — `public/js/sales/v2/list-order-history.js` | Đưa về trang 1 trước khi tải lại | Thao tác đổi điều kiện lọc (modal 絞り込み設定) |
| 4 | `filterByDate` — `public/js/sales/v2/list-order-history.js` | Đưa về trang 1 trước khi tải lại | Thao tác đổi khoảng ngày |
| 5 | `changeEnvironment` — `public/js/sales/v2/list-order-history.js` | Đưa về trang 1 trước khi tải lại | Đổi môi trường bản chính / thử nghiệm |
| 6 | `changeTabTypePayment` — `public/js/sales/v2/list-order-history.js` | Đưa về trang 1 trước khi tải lại | Đổi tab hàng đơn lẻ / hàng định kỳ |
| 7 | `changePage` — `public/js/sales/v2/list-order-history.js` | **Giữ nguyên** | Đây là thao tác đổi trang thật, phải giữ số trang người dùng chọn |
| 8 | `SalesManagementV2Controller::ajaxListOrderHistory` — `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | **Không sửa** — chỉ xác nhận | Xác nhận dùng phân trang 20 bản ghi, đọc số trang từ query string |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Nguyên văn Redmine mục 4.1 chỉ ghi "File thay đổi" (1 file); các function cụ thể lấy từ mục 3 ở trên, KHÔNG bịa thêm. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `searchByNameFriendOrItem` | `public/js/sales/v2/list-order-history.js` | Direct | Reset page = 1 trước khi gọi lại danh sách |
| F2 | `filter` | `public/js/sales/v2/list-order-history.js` | Direct | Reset page = 1 (modal 絞り込み設定 → 決定) |
| F3 | `filterByDate` | `public/js/sales/v2/list-order-history.js` | Direct | Reset page = 1 (đổi ô ngày before/current) |
| F4 | `changeEnvironment` | `public/js/sales/v2/list-order-history.js` | Direct | Reset page = 1 (本番環境 / テスト環境) |
| F5 | `changeTabTypePayment` | `public/js/sales/v2/list-order-history.js` | Direct | Reset page = 1 (単品商品 ↔ 継続商品) |
| F6 | `getListOrderHistory` | `public/js/sales/v2/list-order-history.js` | Direct | Hàm dùng chung — nhận số trang từ caller |
| F7 | `changePage` | `public/js/sales/v2/list-order-history.js` | Indirect | **Không đổi hành vi** — vẫn truyền đúng trang được bấm |
| F8 | `SalesManagementV2Controller::ajaxListOrderHistory` | `app/Http/Controllers/Basic/SalesManagementV2Controller.php` | Indirect | Không sửa code; chỉ đọc `page` từ query string, paginate 20 bản ghi |

**File thay đổi (nguyên văn mục 4.1):**
- `public/js/sales/v2/list-order-history.js` (1 file, 5 dòng thêm)

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn Redmine mục 4.2 -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| — | **Không có** | — | Nguyên văn Dev: "Không có — chỉ sửa mã JavaScript phía giao diện, không đọc/ghi thêm dữ liệu nào" |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn Redmine mục 4.3 -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Single Product / Sales (**FA-026**) — màn Lịch sử bán hàng của **hàng đơn lẻ** và **hàng định kỳ**: tìm kiếm và lọc nay hoạt động đúng ở mọi trang | F1–F7 | `<Dev không ghi mức risk — Leader đánh giá>` |

**Ghi nhận ngoài phạm vi (Dev không sửa):**
- Màn **Chi tiết sản phẩm** còn **cùng lỗi** khi đổi tháng → đã ghi vào danh sách theo dõi, **không fix trong ticket này**.

---

## 5. Recover data

- ✔ **Không cần recover data** (nguyên văn Dev).

## 6. Verify của Dev

| Trường | Giá trị |
|---|---|
| Mức verify | `lint` |
| Lệnh | `node --check public/js/sales/v2/list-order-history.js` → OK (không sửa file PHP nào nên không cần `php -l`)<br>`git diff --stat origin/release_step_20260805...ai_fixbug_27085` → đúng 1 file, 5 dòng thêm, không kéo commit lạ |

**Bằng chứng (nguyên văn):**
- ⚠️ **Không tái hiện được trên dev**: MySQL `host.docker.internal:3306` báo Connection refused nên **không dựng được dữ liệu nhiều trang**.
- Xác minh bằng mã nguồn: `SalesManagementV2Controller::ajaxListOrderHistory` phân trang 20 bản ghi nên lấy số trang từ query string, còn `list-order-history.js` dòng 288 luôn gắn số trang hiện tại vào URL.
- Triệu chứng khớp giao diện: thanh phân trang chỉ hiện khi tổng số trang lớn hơn 1, nên khi trang 2 rỗng thì cả bảng lẫn thanh phân trang cùng biến mất.

## 7. Tự review của AI + rủi ro khi test (nguyên văn)

Fix tối giản đúng nguyên nhân gốc: 5 dòng đưa số trang về 1 ở đúng các thao tác đổi điều kiện lọc, không đụng logic truy vấn hay giao diện. Thao tác bấm số trang vẫn giữ nguyên hành vi cũ. Không bump số phiên bản trong config theo quy định.

**Rủi ro / lưu ý khi test:**
- Người dùng đang ở trang 3 mà đổi khoảng ngày sẽ bị đưa về trang 1 — **đây chính là hành vi mong muốn, không phải hồi quy**.
- Chưa chạy được trên môi trường dev vì MySQL dev không kết nối được, mới xác minh bằng mã nguồn và kiểm tra cú pháp.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] **Xác nhận branch nào là branch fix thật** (`ai_fixbug_27085` vs `fix-bug-27083`) trước khi QA checkout / trước khi chạy lại bộ TC trên Studio
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
