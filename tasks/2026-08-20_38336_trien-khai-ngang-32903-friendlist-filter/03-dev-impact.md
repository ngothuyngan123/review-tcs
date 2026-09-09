# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #38336 (journal `#128996`, 2026-08-13) bởi `/new-task` ngày 2026-08-20.
>
> ⚠️ **Đánh giá này do hệ thống Auto-fixbug LME (AI) sinh tự động**, không phải Dev người viết. Báo cáo gốc dùng cấu trúc 6 mục (1 Nguyên nhân · 2 Cách fix · 3 Đã check · 4 Đánh giá ảnh hưởng · 5 Recover data · 6 Verify) — **mục 4 của báo cáo là 4.1 File thay đổi / 4.2 Data / 4.3 Tính năng**, KHÔNG có mục "4.1 function bị ảnh hưởng" như template. Bảng 4.1 bên dưới được **suy ra từ mục 3** và có đánh dấu rõ.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug` (hệ thống Auto-fixbug LME) — assigned_to hiện tại: `Ngô Thúy Ngần` |
| Commit / Pull Request | `<chưa có PR>` — commit `c94956fb05` · Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38336 |
| Branch | `ai_fixbug_38336` (repo `sns-line`, nhánh gốc `release_step_20260805`) |
| Ngày submit đánh giá | `2026-08-13` |
| Auto-filled | `2026-08-20 by /new-task` |
| Thời gian AI xử lý | 13 phút 36 giây |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

<!-- Nguyên văn mục ■1 báo cáo Auto-fixbug. -->

Bug gốc #32903 là action ở màn danh sách bạn bè không chạy theo bộ lọc khi vào màn này từ nơi khác. Với 4 màn cần triển khai ngang (gửi hàng loạt, quản lý tag, quản lý CSV, rich menu), bộ lọc được chuyển sang danh sách bạn bè bằng localStorage, nhưng **4 điều kiện kiểm tra đầu tiên trong đoạn nạp bộ lọc bị đặt sai dấu ngoặc đóng** nên vế thứ hai luôn đúng khi khoá chưa từng được ghi. Hậu quả: 4 điều kiện này **luôn khớp và nuốt hết các nhánh phía dưới**, bộ lọc bàn giao bị đặt thành rỗng, danh sách hiện toàn bộ bạn bè và action hàng loạt áp cho tất cả thay vì nhóm đã lọc.

## 2. Cách fix

<!-- Nguyên văn mục ■2 báo cáo Auto-fixbug. -->

Sửa dấu ngoặc đóng đặt sai ở **4 điều kiện đầu tiên** trong đoạn nạp bộ lọc bàn giao của màn danh sách bạn bè (khoá trả lời tự động, quản lý CSV, lịch hành động, rich menu), đưa phép so sánh rỗng vào trong ngoặc để điều kiện không còn luôn đúng. Nhờ đó các nhánh nạp bộ lọc của màn gửi hàng loạt, quản lý tag, quản lý CSV và rich menu chạy được, danh sách và action hàng loạt bám đúng bộ lọc từ màn nguồn. **Chỉ sửa 1 file JS, KHÔNG tăng số phiên bản tài nguyên tĩnh (đã bỏ theo yêu cầu human).**

> ⚠️ Đây là **fix dạng generic** (1 sửa đổi chung khôi phục cùng lúc nhiều nhánh). Theo quy ước repo, fix generic bắt buộc cover **≥ 3 trigger khác nhau** + **≥ 1 case không có bàn giao (fallback)**. Ở đây có 4+ trigger (send all / tag / CSV / rich menu) và cần thêm case "không có bộ lọc bàn giao → danh sách mặc định".

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn mục ■3 báo cáo Auto-fixbug, chuyển sang bảng template. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `modal.orderBy` — `public/js/friendlist/modal_filter_v2.js` | ✅ **ĐÃ SỬA** (điểm fix duy nhất) | Nạp bộ lọc bàn giao từ localStorage khi mở danh sách bạn bè |
| 2 | `modal.searchFormAll` — `public/js/friendlist/modal_filter_v2.js` | Không sửa — đã check | Query danh sách theo bộ lọc, set `type_filter=new` |
| 3 | `actionListFriend.sendActionFriends` — `public/js/friendlist/script.js` | Không sửa — đã check | Gửi action hàng loạt kèm `item_search` |
| 4 | `addTag` / `removeTag` / `addRichMenu` / `SendTemplate` — `public/js/friendlist/script.js` | Không sửa — đã check | Các thao tác hàng loạt khác cùng dùng `modal.search_action` |
| 5 | `FriendlistController::sendActionFriend` — `app/Http/Controllers/Basic/FriendlistController.php` | Không sửa — đã check | Áp bộ lọc và **tạo lịch hành động tự sinh khi vượt 200 người** |
| 6 | `FriendlistController::index` — `app/Http/Controllers/Basic/FriendlistController.php` | Không sửa — đã check | Truyền tham số lọc từ URL xuống view |
| 7 | `Conversation::advanceFilterPost` — `app/Conversation.php` | Không sửa — đã check | Dựng câu truy vấn từ `item_search` |
| 8 | `showFriendhasTag` — `public/js/tag/index.js`, `public/js/tag/index_v2.js` | Không sửa — đã check | Điểm bàn giao bộ lọc **màn quản lý tag** |
| 9 | `showNumberFilter` — `public/js/csv_management/csv_management.js`, `public/js/csv_management/create_download_file.js` | Không sửa — đã check | Điểm bàn giao **màn quản lý CSV** (2 điểm vào) |
| 10 | `showNumberFilter` — `public/js/broadcast/add-broadcast.js` | Không sửa — đã check | Điểm bàn giao **màn gửi hàng loạt** |
| 11 | `showNumberFilter` — `public/js/menu_rich/v2/setting_display.js` | Không sửa — đã check | Điểm bàn giao **màn rich menu** |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

> ⚠️ **Báo cáo AI mục 4.1 chỉ liệt kê FILE thay đổi**, nguyên văn:
>
> ```
> • 4.1 File thay đổi:
>   - public/js/friendlist/modal_filter_v2.js
> ```
>
> Bảng dưới đây được **suy ra từ mục 3** (Leader verify lại trước khi giao TC).

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `modal.orderBy` | `public/js/friendlist/modal_filter_v2.js` | **Direct** | Điểm sửa duy nhất — 4 điều kiện sai dấu ngoặc |
| F2 | `modal.searchFormAll` | `public/js/friendlist/modal_filter_v2.js` | Indirect | Nhận bộ lọc từ F1; sau fix mới nhận đúng điều kiện |
| F3 | `actionListFriend.sendActionFriends` | `public/js/friendlist/script.js` | Indirect | Action hàng loạt nay gửi kèm `item_search` đúng |
| F4 | `addTag` / `removeTag` / `addRichMenu` / `SendTemplate` | `public/js/friendlist/script.js` | Indirect | Dùng chung `modal.search_action` |
| F5 | `FriendlistController::sendActionFriend` | `app/Http/Controllers/Basic/FriendlistController.php` | Indirect | Tạo lịch tự sinh khi > 200 người — **nay lưu đúng bộ lọc** |
| F6 | `FriendlistController::index` | `app/Http/Controllers/Basic/FriendlistController.php` | Indirect | Nhánh bàn giao qua **URL param** (đường của bug gốc #32903) |
| F7 | `Conversation::advanceFilterPost` | `app/Conversation.php` | Indirect | Dựng query từ `item_search` |
| F8 | `showFriendhasTag` | `public/js/tag/index.js`, `index_v2.js` | Indirect | Điểm bàn giao màn tag (**2 version file** — RULE-09) |
| F9 | `showNumberFilter` (CSV) | `public/js/csv_management/csv_management.js`, `create_download_file.js` | Indirect | **2 điểm vào** màn CSV |
| F10 | `showNumberFilter` (Broadcast) | `public/js/broadcast/add-broadcast.js` | Indirect | Điểm bàn giao màn gửi hàng loạt |
| F11 | `showNumberFilter` (Rich menu) | `public/js/menu_rich/v2/setting_display.js` | Indirect | Điểm bàn giao màn rich menu |

### 4.2. List data bị update khi fix bug

> Nguyên văn mục ■4.2: *"Không có thay đổi cấu trúc hay dữ liệu. Sau fix, bản ghi lịch hành động tự sinh và bộ lọc kèm theo (khi thao tác trên 200 người) sẽ được tạo với đúng điều kiện lọc thay vì không có điều kiện."*

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | Bản ghi **lịch hành động tự sinh** `【自動生成】友だち一括アクション` + điều kiện lọc kèm theo | CREATE (**nội dung thay đổi**, không đổi schema) | Chỉ phát sinh khi thao tác trên **> 200 người**. Trước fix lưu **rỗng điều kiện** → job chạy sai nhóm. Sau fix lưu đúng điều kiện. **Đây là data impact nguy hiểm nhất** |
| D2 | Khoá **localStorage** bàn giao bộ lọc (reply_filter / reply_filter_or / CSV / lịch hành động / rich menu) | CREATE / DELETE (đọc-rồi-xoá, one-shot) | Không phải DB. Trước fix bị **ghi rỗng oan** ngay cả khi không bàn giao. Cần test **trạng thái tồn đọng từ bản lỗi** (REQ-009) |
| D3 | Schema DB / migration | **KHÔNG có** | Dev khẳng định không thay đổi cấu trúc |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Nguyên văn mục ■4.3 báo cáo Auto-fixbug. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | **Friend List (FA-013)** — khôi phục nạp bộ lọc bàn giao khi mở danh sách bạn bè từ màn khác; danh sách và mọi thao tác hàng loạt (action, gắn/gỡ thẻ, đổi rich menu, gửi mẫu tin) bám đúng nhóm đã lọc | F1, F2, F3, F4, D2 | **High** |
| T2 | **Broadcast (FA-008)** — bấm số người ở màn gửi hàng loạt nay mở danh sách bạn bè đã lọc đúng | F10 | **High** |
| T3 | **Tag Management (FA-012)** — bấm số người của một thẻ nay mở danh sách chỉ gồm bạn có thẻ đó | F8 | **High** |
| T4 | **CSV Management (FA-014)** — bấm số người của bản ghi CSV hoặc màn tạo file tải về nay mở danh sách đã lọc đúng | F9 | **High** |
| T5 | **Rich Menu (FA-004)** — bấm số người đối tượng ở màn cài đặt hiển thị rich menu nay mở danh sách đã lọc đúng | F11 | **High** |
| T6 | **Action Schedule (FA-016)** — lịch hành động tự sinh khi thao tác trên 200 người nay lưu đúng bộ lọc nên job chạy đúng nhóm | F5, D1 | **High** |

> ⚠️ **Impact Dev KHÔNG liệt kê ở 4.3 nhưng nêu ở phần rủi ro** — Leader cân nhắc bổ sung:
>
> | # | Tính năng / Màn hình | Nguồn | Nguy cơ |
> |---|---|---|---|
> | T7 | **自動応答 (khoá trả lời tự động)** + **イベントステップ (bước sự kiện)** | Mục ■2: 1 trong 4 điều kiện sửa là "khoá trả lời tự động"; Studio REQ-007 (human đã xác nhận qua phản biện #53) | **High** — bị bản sửa **chạm trực tiếp** nhưng KHÔNG có tên trong ticket |
> | T8 | **アクションスケジュール (màn thêm/sửa lịch hành động)** | Mục ■2: 1 trong 4 điều kiện sửa là "lịch hành động"; Studio REQ-007 | **High** — như trên |
> | T9 | **クロス分析 (phân tích chéo)** | Mục "Rủi ro / lưu ý khi test": nhánh nạp bộ lọc phân tích chéo *"lần đầu thực sự chạy sau nhiều năm bị chặn"* | Medium–High |
> | T10 | **シナリオ (kịch bản)** — bàn giao qua **URL param** | Mục ■6: đường của bug gốc #32903 (`scenario_unfinish_id`); Studio REQ-011 | Medium — verify fix không làm hỏng cơ chế cũ |

---

## Phụ lục — các mục bổ sung từ báo cáo Auto-fixbug (không có trong template)

### ■5. Recover data

✔ **Không cần recover data.**

### ■6. Verify (do AI tự chạy)

| Mục | Nội dung |
|---|---|
| Mức | **lint** (⚠️ không phải integration/e2e) |
| Lệnh | `node --check public/js/friendlist/modal_filter_v2.js` → OK · Mô phỏng chuỗi điều kiện bằng node cho **9 kịch bản localStorage** · `git diff --stat release_step_20260805...ai_fixbug_38336` → chỉ 1 file |
| Bằng chứng 1 | Quét toàn repo tìm mẫu điều kiện đặt sai ngoặc: **đúng 4 chỗ**, đều trong `modal_filter_v2.js` — đã sửa hết, không sót |
| Bằng chứng 2 | Bug gốc #32903 nằm ở nhánh `fix-bug-32903` (merge `6f24af4732`): xử lý tham số lọc qua **URL** (`scenario_unfinish_id`). 4 màn của ticket này truyền bộ lọc qua **localStorage** → **không được nhánh đó bao phủ** |
| Bằng chứng 3 | **Yêu cầu số 2** của ticket (tên trigger `【自動生成】友だち一括アクション`) **đã đúng sẵn** trên release từ commit `0d54f99d53`, dùng chung cho cả 3 nhánh tạo lịch trong `sendActionFriend` → **không cần sửa** |

> ⚠️ Verify chỉ ở mức **lint + mô phỏng logic bằng node**. **Không có** bằng chứng chạy thật trên browser/staging/production trong báo cáo Dev.

### ■ Tự review (AI)

Fix tối giản đúng nguyên nhân gốc: chỉ dời dấu ngoặc đóng ở 4 điều kiện bị sai trong 1 file JS, không đổi logic nghiệp vụ, không đụng backend, không đụng config. Đã đối chiếu diff với yêu cầu ticket: cả 4 màn được nêu (gửi hàng loạt, quản lý tag, quản lý CSV, rich menu) đều được khôi phục bằng cùng một sửa đổi; yêu cầu số 2 về tên trigger đã đúng sẵn nên không sửa. Đã quét toàn repo để chắc chắn không còn chỗ nào cùng mẫu lỗi.

### ■ Rủi ro / lưu ý khi test (nguyên văn — ĐỌC KỸ TRƯỚC KHI VIẾT TC)

1. **KHÔNG tăng số phiên bản tài nguyên tĩnh** (human yêu cầu bỏ) — file JS được nhúng kèm `?v=config('sns-line.version')` nên **trình duyệt đã cache bản cũ sẽ KHÔNG tự tải bản mới**. Khi release cần tăng version ở lần deploy chung, hoặc dặn tester và khách hàng **tải lại cứng (Ctrl+F5)** thì fix mới có hiệu lực.
2. Sau fix, các nhánh nạp bộ lọc bên dưới (gửi hàng loạt, tag, CSV, rich menu, lịch, **phân tích chéo**) **lần đầu thực sự chạy sau nhiều năm bị chặn** — cần test kỹ từng màn để chắc dữ liệu bộ lọc bàn giao vẫn đúng định dạng hiện tại.
3. Người dùng đang quen cảnh danh sách hiện toàn bộ bạn bè khi bấm số người sẽ thấy **hành vi đổi** (nay chỉ hiện nhóm đã lọc) — đây là **hành vi đúng theo thiết kế**.

### ■ Branch / Commit (để QA checkout)

- `sns-line`: **`ai_fixbug_38336`** (nhánh gốc `release_step_20260805`, commit `c94956fb05`, 1 file) — *đã push*

### ■ Link phiên xử lý AI

- Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=267e8f29-650e-42b6-8f8f-a6a6d0fb16c5
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=38336

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — ⚠️ **bảng 4.1 là suy ra từ mục 3, Dev không tự liệt kê**
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file) — ⚠️ **chú ý D1 (lịch tự sinh > 200 người) và D2 (localStorage tồn đọng)**
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng — ⚠️ **T7–T10 Dev KHÔNG liệt kê ở 4.3, cần quyết định có đưa vào phạm vi test không**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC

### Câu hỏi Leader nên hỏi lại Dev / PM

1. **Phạm vi test có bao gồm T7–T10 không?** Bản sửa chạm 4 điều kiện, trong đó **"khoá trả lời tự động"** và **"lịch hành động"** KHÔNG có tên trong ticket nhưng bị sửa trực tiếp. Studio đã ghi nhận là REQ-007 với ghi chú *"human đã xác nhận xung đột phạm vi qua phản biện #53"*.
2. **Version asset sẽ được tăng ở lần deploy nào?** Nếu không tăng, KH có thể báo "fix không có tác dụng" — cần plan thông báo hard-reload.
3. **Có cần TC trên PRODUCTION không?** Task chạm **job nền** (lịch tự sinh > 200 người) và **asset cache** → theo RULE-08 không kết luận được từ local/staging. Bộ TC Studio hiện có **0 TC chạy trên prd**.
4. **Dữ liệu bộ lọc bàn giao cũ tồn đọng trong localStorage của KH** sẽ xử lý thế nào sau khi deploy?

<!-- Source: Redmine #38336 journal #128996 (2026-08-13T07:56:11Z, author "AI LME Fix bug"), fetch 2026-08-20 bởi /new-task. Mục 1/2/3/4.2/4.3/5/6 chép nguyên văn; bảng 4.1 và T7-T10 là SUY RA, đã đánh dấu rõ. -->
