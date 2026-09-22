# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39263 — [Richmenu] Modal filter: Khi tạo mới richmenu, add action change richmenu và add filter cho richmenu đó, sau khi mở lại modal action không hiển thị filter bên trong` |
| Module / Màn hình | Rich Menu (FA-004) — màn **tạo mới richmenu** (`/basic/rich-menu/create`), bước 3 `タップ時アクション`, tab `リッチメニュー切り替え` → modal `絞込みを設定する` (filter V2 dùng chung với Friend Filter SC-003) |

## Mô tả bug (bản dịch tiếng Việt)

Khi **tạo mới** richmenu, ở bước 3 người dùng gán action `リッチメニュー切り替え` (chuyển richmenu) cho một vùng và chọn richmenu đích, sau đó bấm `絞込みを設定する` (đặt điều kiện lọc) bên dưới richmenu đích đó để mở modal filter và lưu điều kiện lọc. Khi mở lại chính modal filter đó thì **không hiển thị** điều kiện lọc vừa lưu — modal trống.

(Nội dung ticket viết bằng tiếng Việt, thuật ngữ màn hình giữ nguyên tiếng Nhật.)

## Steps to reproduce

1. Tạo mới richmenu
2. Tại bước 3, click tab `リッチメニュー切り替え`
3. Ở tab `表示する`, chọn `表示するリッチメニューを選択` và chọn 1 richmenu cần change
4. Tại richmenu vừa pick, click btn `絞込みを設定する` bên dưới richmenu đó ⇒ mở modal filter
5. Add filter trong modal ⇒ save filter
6. Thực hiện mở lại modal filter đó

## Expected result

- Hiển thị filter đã setting bên trong (modal nạp lại đúng các điều kiện lọc vừa lưu).

## Actual result

- Không hiển thị filter đã setting bên trong (modal mở lại trống).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video
- [ ] Có log / request-response

<!-- Redmine attachments = 0; evidence nằm ở link Google Drive trong description (chưa xác định chính xác là ảnh hay video — mở link để kiểm tra). -->

- Link evidence: https://drive.google.com/file/d/17Q120miZW_uPt-qhkDNjhXLWeySY6Nxu/view?usp=drive_link

## Ghi chú thêm của Leader

- **Phạm vi lỗi chỉ ở luồng TẠO MỚI** richmenu (route `/basic/rich-menu/create`, richmenu chưa có `id`). Luồng **sửa** richmenu đã lưu không bị lỗi này — theo Dev, `parent_id` rỗng + mã vùng âm (`0-1-i`) là điều kiện gây bug.
- Fix còn chạm **cả chiều dọn rác bản nháp**: filter tạm của phiên tạo mới bỏ dở (đóng tab / F5) trước đây nằm lại vĩnh viễn trong DB; sau khi có fix nạp lại filter thì các bản ghi mồ côi này có nguy cơ **hiện lên ở phiên tạo mới sau và bị gắn thật vào richmenu vừa tạo** → đây là vùng regression quan trọng, không chỉ verify happy path.
- **Điều kiện tiên quyết account test**: bot phải thuộc gói **có** tính năng richmenu switching — bot gói miễn phí bị chặn ở nút `絞込みを設定する` bằng modal nâng cấp (knowledge `LIM-027`).
- ⚠️ **Dev KHÔNG tái hiện / KHÔNG verify được trên môi trường chạy thật**: journal ghi `Không tái hiện được trên dev: MySQL host.docker.internal:3306 Connection refused (dev stack không chạy)`. Mức verify chỉ là **lint** (`php -l`) + đọc code. Toàn bộ kết luận đúng/sai của fix **chưa có bằng chứng runtime** → TC phải verify thật, không tin vào mục 6 của Dev.
- ⚠️ **Số file sửa mâu thuẫn trong chính journal**: mục 4.1 + mục 6 ghi **2 file** (`FilterController.php`, `functions.php`), nhưng dòng BRANCH/COMMIT ghi `commit ec1ce93f3b, **4 file**`. Ngoài ra mục 2 mô tả fix nằm ở `UserController::editRichMenuForm` nhưng file `UserController.php` **không có** trong danh sách file thay đổi. Cần hỏi Dev / check diff thật trước khi chốt phạm vi regression.
- Môi trường phát hiện: ticket không ghi rõ env — cần xác nhận với người báo (Hạnh Nguyễn).
- Trạng thái Redmine lúc fetch: `Fix done - Đợi test`, branch fix `ai_fixbug_39263` đã push.

## Journal / note từ Redmine (nguyên văn)

**Journal #133069 — AI LME Fix bug — 2026-08-26:**

```
★ AI AUTO-FIXBUG — ĐÃ FIX XONG, CHUYỂN TEST
Branch fix đã được duyệt & push lên origin. Chi tiết bên dưới để QA tiếp nhận.
════════════════════════════════════════════════

■ 1. NGUYÊN NHÂN
Khi TẠO MỚI richmenu thì richmenu chưa có id, nên filter của action chuyển richmenu được lưu tạm với parent_id rỗng và mã vùng âm. Phía server, hàm nạp lại filter bỏ qua toàn bộ truy vấn khi parent_id rỗng nên mở lại modal không thấy filter nào. Cùng lý do, khi bấm lưu richmenu mới các filter tạm cũng không được gắn lại vào richmenu/vùng vừa tạo (câu lệnh gắn lại bắt buộc khớp parent_id = id richmenu) nên mở lại từ màn sửa cũng không thấy filter.

■ 2. CÁCH FIX
Sửa theo AI review vòng 2: khi mở form TẠO MỚI richmenu (route /basic/rich-menu/create, không có id), phần dọn filter tạm ở UserController::editRichMenuForm trước đây lọc theo parent_id = null nên không khớp các bản ghi tạm được lưu với parent_id rỗng (cột int, lưu thành 0) — filter tạm của phiên tạo mới bỏ dở (đóng tab/tải lại trang) nằm lại vĩnh viễn, và sau khi có fix nạp lại filter thì chúng hiện lên ở phiên tạo mới sau và bị gắn thật vào richmenu vừa tạo. Nay giữ nguyên nhánh cũ khi có id richmenu (luồng sửa), còn khi không có id thì dọn đúng phạm vi mà phần nạp lại dùng: cùng bot, loại filter chuyển richmenu, mã vùng âm và parent_id rỗng (null hoặc 0). Chỉ sửa trong hàm này, không đụng luồng sửa richmenu.

■ 3. ĐÃ CHECK FUNCTION / DATA LIÊN QUAN
FilterController::initDataFilter (app/Http/Controllers/Basic/FilterController.php)
FilterController::saveFilterV2 (app/Http/Controllers/Basic/FilterController.php)
FilterV2::saveFilter (app/FilterV2.php)
buildAreaRichmenu (app/Helpers/functions.php)
UserController::getRichMenu (app/Http/Controllers/Basic/UserController.php)
UserController::editRichMenuForm (app/Http/Controllers/Basic/UserController.php)
showModalFilterV2RichMenuToggle (public/_assets/modules/rich_menu/js/create.js)
initDataStep3 / prepareFormData (public/_assets/modules/rich_menu/js/create.js)
initDataFilter + saveFilterV2 phía modal (public/js/friendlist/modal_filter_v2.js)
HandlePostbackTask switch richmenu (linect-service, chỉ đọc để xác nhận runtime dùng filter_ids)

■ 4. ĐÁNH GIÁ ẢNH HƯỞNG
 • 4.1 File thay đổi:
   - app/Http/Controllers/Basic/FilterController.php
   - app/Helpers/functions.php
 • 4.2 Data ảnh hưởng:
   - filters_v2.parent_id / filters_v2.rich_menu_item_id — từ nay filter tạo trong lúc tạo mới richmenu được gắn lại đúng richmenu và vùng khi lưu; dữ liệu cũ đã lưu sai vẫn còn mồ côi (xem mục recover)
 • 4.3 Tính năng liên quan:
   - Rich Menu (FA-004) — filter của action chuyển richmenu trong luồng tạo mới richmenu
   - Friend Filter (SC-003) — modal lọc bạn nạp lại điều kiện đã lưu khi chưa có bản ghi cha

■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: lint
   Lệnh: php -l app/Http/Controllers/Basic/FilterController.php: OK; php -l app/Helpers/functions.php: OK; git diff --stat release_step_20260623...ai_fixbug_39263: chỉ 2 file đã sửa
   Bằng chứng: Không tái hiện được trên dev: MySQL host.docker.internal:3306 trả về Connection refused (dev stack không chạy); Đọc code xác nhận luồng tạo mới richmenu không có id richmenu: /basic/rich-menu/create không tạo bản ghi (quickAddRichMenu chỉ update khi đã có id), getRichMenu trả data null nên rich_menu_detail.id rỗng; layout_actions[i].id = 0-1-i (mã vùng âm) trong initDataStep3, khớp với chỗ dọn rác rich_menu_item_id < 0 ở editRichMenuForm

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_39263 (nhánh gốc release_step_20260623, commit ec1ce93f3b, 4 file)  [đã push]

────────────────────────────────────────────────
» Thời gian AI xử lý: 1 phút 7 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=9b89f099-8159-485b-bf2e-de21aa601671
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39263
(Báo cáo tạo tự động bởi hệ thống Auto-fixbug LME)
```
