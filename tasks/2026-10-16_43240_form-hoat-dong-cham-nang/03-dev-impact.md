# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **INPUT KHÔNG THEO FORMAT CHUẨN.** Redmine #43240 KHÔNG có section "Đánh giá ảnh hưởng" (1. Nguyên nhân / 2. Cách fix / 3. Caller / 4.1-4.3) trong Description. Nội dung dưới đây được `/new-task` **tổng hợp lại** từ 3 Journal "Dev Studio" (format riêng: `Nguyên nhân:` / `Hướng sửa:` / `Ảnh hưởng / rủi ro:`, lặp qua nhiều vòng) — xem nguyên văn đầy đủ ở `01-bug-task.md`. Mỗi bullet dưới đây giữ nguyên câu chữ Dev viết, chỉ xếp lại vào đúng mục của template.
> ⚠️ **Mục 3 và 4.1 có bổ sung từ `requirements` (REQ-001→REQ-014) do Studio task #457 tự rút ra** (không phải Dev tự kê) — các dòng này đánh dấu nguồn `[Studio REQ-xxx]` riêng, KHÔNG lẫn với phần Dev tự viết.
> ⚠️ **BẮT BUỘC Tester/Leader đọc lại 3 Journal gốc** trước khi tick checkbox "Tester verify" — đây là bản dàn lại cấu trúc do AI làm, KHÔNG phải Dev tự điền đúng 4 mục chuẩn.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `<không rõ tên thật>` — 3 Journal ký tên "Dev Studio" (hệ thống tự động); Redmine assignee = trống |
| Commit / Pull Request | `<chưa có — Journal không kèm commit hash>` |
| Branch | `ai_studio_fixbug_43240` (theo Studio task #457) |
| Ngày submit đánh giá | 2026-10-16 (cả 3 Journal #144707 / #144901 / #144955, cùng ngày) |
| Auto-filled | 2026-10-16 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — ⚠️ đọc kỹ cảnh báo ở đầu file trước khi tick: nội dung dưới là bản AI dàn lại từ format journal khác chuẩn, không phải Dev tự điền đúng 4 mục; mục 3/4.1 có trộn thêm requirements Studio tự sinh.

---

## 1. Nguyên nhân

**Vòng 1 (Journal #144707) — root cause chính:**
API `/ajax/get-list-group-tag` (`TagController@ajaxGetListCategoryTag`) không phân trang khi modal 「アクション」 gọi, nên duyệt mọi tag trong folder. Với mỗi tag có action, API dựng lại chi tiết action để xem trước: chạy nhiều truy vấn cho từng dòng action, và mỗi dòng lại nạp toàn bộ tag 未分類 của bot. Modal không dùng dữ liệu này. Từ commit `fixbug_37710` (21/07/2026), mỗi tag tốn thêm nhiều truy vấn, nên bot 895 tag phải chờ 295 giây.

**Vòng 2 (Journal #144901) — phát hiện phụ (CSRF), KHÔNG sửa:**
Middleware CSRF của app miễn kiểm tra cho toàn bộ đường dẫn `/ajax/*` từ trước ticket, nên API mới cũng như mọi API ajax khác không kiểm CSRF token. API chỉ đọc, vẫn đòi phiên đăng nhập và chỉ trả tag của bot trong session, nên người phụ trách đã quyết định không sửa trong ticket này.

**Vòng 3 (Journal #144955) — rà soát bug automation tìm thấy, kết luận KHÔNG phải lỗi sản phẩm:**
Không có lỗi sản phẩm mới. Ba bug do kịch bản đọc trang trước khi render xong hoặc tiền điều kiện sai, ở các màn mà ticket không sửa. Bug về `category_id` là thay đổi có chủ đích của v6. Bug thứ tự chỉ lệch ở các tag trùng `position`: màn quản lý tag không có tiêu chí sắp xếp phụ, còn modal giữ thứ tự `position` giảm, `id` giảm như API cũ.

## 2. Cách fix

**Vòng 1 (Journal #144707):**
- D-1 Modal 「アクション」 tải tag qua API nhẹ có sẵn

**Vòng 2 (Journal #144901):**
- Không sửa code — chỉ ghi nhận quyết định không fix CSRF trong ticket này.

**Vòng 3 (Journal #144955):**
- Không sửa code — chỉ kết luận 3 bug automation tìm thấy không phải lỗi sản phẩm, không nằm trong phạm vi ticket.

> ⚠️ Chỉ **vòng 1** có thay đổi code thật. Theo `[Studio REQ-xxx]` (task #457, không phải Dev tự kê), cách fix cụ thể hơn:
> - `[REQ-001/002/007]` API mới **`/ajax/get-data-for-tag-action`** (`ActionController@ajaxGetDataForTagAction`, `TagRepository::getTagsByBotAndCategory`) — trả tối đa **50 tag/lần**, có `group_id`/`page`, không gửi `page` → trả hết; chỉ tag của bot trong session; tag xoá mềm bị loại.
> - `[REQ-002]` `select_action.js` — hàm `initDataTag` + `scrollLoadMoreTag` (cuộn tải thêm theo trang).
> - `[REQ-003/REQ-014]` `select_action.js` — `selectAll` / `refreshCheckAllBtn` (nút 「以下を全選択」 áp dụng cả folder kể cả trang chưa tải; tick/bỏ tick phản ánh đúng theo tiến độ tải).
> - `[REQ-005]` Guard `group_open_tag` — chặn response trang sau của folder cũ về muộn (tránh lẫn tag khi đổi folder giữa lúc đang tải).
> - `[REQ-006/REQ-013]` Xử lý popup 「タグ新規追加」 hoạt động đúng với danh sách đã phân trang (mọi cách đóng popup không làm tải lại sai / khoá tải thêm).
> - `[REQ-011]` Asset `select_action.js` có **version** (cache-busting) — JS cũ (chưa hard-reload) vẫn chạy được vì API cũ còn giữ nguyên.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Dev **KHÔNG tự liệt kê** mục này trong 3 Journal gốc (chỉ nói chung "khoảng 40 màn include" ở vòng 1). Bảng dưới suy từ `[Studio REQ-008]` (`source: git grep modal_select_action (55 view)`) — **cần Dev xác nhận lại danh sách đầy đủ**, đây KHÔNG phải Dev tự kê.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `TagController@ajaxGetListCategoryTag` (API cũ `/ajax/get-list-group-tag`) | KHÔNG đổi | Dev giữ nguyên để JS cũ (chưa hard-reload) vẫn chạy (REQ-011); màn quản lý タグ vẫn dùng API này |
| 2 | Màn quản lý 「タグ」 | KHÔNG đổi | Dùng API cũ, không đụng tới (vòng 1 xác nhận giữ nguyên) |
| 3 | Modal 絞込 (mở từ tab タグ của modal アクション) | Đổi gián tiếp — dùng chung API nhẹ mới | Vòng 1: "cần kiểm modal lọc vẫn hoạt động (cùng dùng API nhẹ)" |
| 4 | `[Studio REQ-008]` ~55 view include `modal_select_action` (Form cũ + v3, Rich menu, Kịch bản/step, Auto reply, màn quản lý タグ khác) | Gián tiếp — tải tag nhanh hơn qua modal dùng chung | Modal dùng chung JS, không sửa riêng từng màn |
| 5 | `[Studio REQ-009]` Các tab khác của modal アクション (ステップ/テンプレート/リッチメニュー/友だち情報) | KHÔNG đổi (theo yêu cầu) | Chỉ tab タグ đổi cách tải; cần hồi quy các tab khác không bị ảnh hưởng bởi thay đổi service chung |

⚠️ **Input thiếu**: Dev không liệt kê tên file/commit cụ thể nào trong 3 Journal (không có commit hash, không có danh sách file diff) — toàn bộ bảng trên suy từ "khoảng 40 màn include" (vòng 1) + requirements Studio tự sinh. Cần hỏi Dev hoặc đọc diff thật trước khi kết luận coverage đủ ở BƯỚC 2 của `/review-tc` (`task_get_context` sections `spec_delta`/`dev_impact` trên Studio task #457 nếu có).

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Modal 「アクション」 — tab 「タグ」, hàm tải tag | `select_action.js` (`initDataTag`) | Direct | Đổi từ gọi API cũ sang API nhẹ mới (vòng 1) |
| F2 | API mới `/ajax/get-data-for-tag-action` | `ActionController@ajaxGetDataForTagAction`, `TagRepository::getTagsByBotAndCategory` | Direct | `[Studio REQ-007]` — phân trang 50 tag/trang |
| F3 | Cuộn tải thêm (infinite scroll) | `select_action.js` (`scrollLoadMoreTag`) | Direct | `[Studio REQ-002]` |
| F4 | 「以下を全選択」 áp dụng cả folder | `select_action.js` (`selectAll`, `refreshCheckAllBtn`) | Direct | `[Studio REQ-003/014]` |
| F5 | Guard chống lẫn tag khi đổi folder giữa lúc tải | `select_action.js` (`group_open_tag`) | Direct | `[Studio REQ-005]` |
| F6 | Popup 「タグ新規追加」 trong modal | `select_action.js` | Direct | `[Studio REQ-006/013]` — phải hoạt động đúng với list đã phân trang |
| F7 | Modal 絞込 (lọc) — dùng chung API nhẹ mới | — | Indirect | Vòng 1: "cần kiểm modal lọc vẫn hoạt động" |
| F8 | API cũ `/ajax/get-list-group-tag` + màn quản lý 「タグ」 | `TagController@ajaxGetListCategoryTag` | Không đổi | Giữ nguyên để JS cũ chạy được (REQ-011) + màn quản lý tag vẫn dùng |
| F9 | ~55 màn host khác include modal アクション (Form, Rich menu, Kịch bản/step, Auto reply...) | `modal_select_action` (git grep) | Indirect | `[Studio REQ-008]` — tải tag nhanh hơn, cần hồi quy save/mở lại tag đúng |
| F10 | Các tab khác của modal アクション (ステップ/テンプレート/リッチメニュー/友だち情報) | — | Indirect (hồi quy) | `[Studio REQ-009]` — không đổi, chỉ cần xác nhận không bị ảnh hưởng |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Asset `select_action.js` (version/hash cho cache-busting) | UPDATE | `[Studio REQ-011]` — để browser nhận JS mới mà không cần hard-reload; JS cũ vẫn phải chạy được (API cũ còn) |
| D2 | `<không có — không có migration/schema DB nào được Dev nêu>` | — | Fix chỉ đổi query (tránh N+1) + thêm API phân trang + JS client, KHÔNG đổi cấu trúc DB theo 3 Journal. ⚠️ **Input thiếu**: Dev không xác nhận rõ, cần hỏi lại nếu nghi có đổi cache/config khác |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Form v3 — nơi khách TY-12429 phát hiện chậm | F1, F2, F9 | **High** — trực tiếp đường khách báo, bot nhiều tag |
| T2 | Rich menu (tạo/sửa, action タグ) | F9 | Medium — TC Studio `NEW-25` (regression) đang **skip/chưa chạy** |
| T3 | Kịch bản / step (action タグ) | F9 | Medium |
| T4 | Auto reply (action タグ) | F9 | Medium |
| T5 | Màn quản lý 「タグ」 (API cũ) | F8 | Low — Dev xác nhận giữ nguyên, chỉ cần hồi quy nhanh |
| T6 | Modal 絞込 (lọc) | F7 | Medium — dùng chung API nhẹ mới, chưa có test riêng sâu |
| T7 | Form cũ (v2 hoặc trước v3, nếu còn dùng modal chung) | F9 | Medium — cùng rủi ro T1 nhưng chưa xác nhận riêng |
| T8 | Bảo mật API ajax (CSRF) — **ngoài phạm vi ticket, Dev cố ý không sửa** | Journal #144901 | Thấp theo đánh giá Dev (chỉ đọc, cần session, lọc theo bot) — Leader nên ghi nhận làm risk theo dõi riêng, không phải regression của #43240 |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **chưa có commit hash/PR link, cần Dev bổ sung**
- [ ] Mục 3 đã check đủ caller — **bảng hiện tại suy từ Studio REQ, chưa phải Dev tự kê, cần Dev xác nhận**
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
- [ ] Đã đọc 5 ticket bug con mở trong round test Studio (#43316, #43317, #43343, #43344, #43345) — xem `01-bug-task.md`
