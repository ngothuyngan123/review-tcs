# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42771 — Category service V2 – Sort position` |
| Module / Màn hình | `V2\CategoryService — hàm sắp xếp vị trí (updatePosition) dùng chung cho: thư mục rich menu, rich menu, danh sách hợp đồng (point-settings), LP super admin, thư mục LP super admin` |

## Mô tả bug (bản dịch tiếng Việt)

Controller: `V2\CategoryService`
Nguồn: security audit IDOR (Template / Broadcast / Scenario)

1. IDOR-MSG-22 (2/10) [Low] — Category service V2 · Sort position chéo bot

* Vị trí: `V2\CategoryService.php:89-91`
* Route: — (middleware: —)
* Vấn đề / Fix: `whereIn('id')->update(['position'])` → thiếu lọc theo `bot_id`

⚠️ Đây là finding từ **security audit IDOR**, không phải bug do khách hàng/CS báo qua ticket thường — không có Section "Tái hiện bug" (Steps to reproduce) riêng trong description. Nội dung điều tra + đánh giá ảnh hưởng nằm trong 2 journal của Dev Studio (xem bên dưới) — đã dùng làm nguồn cho `03-dev-impact.md`.

## Steps to reproduce

1. (Không có trong Redmine — xem "Điểm cần test" ở Journal #143108 để tái hiện kịch bản IDOR cụ thể, vd gửi tay request sort chèn id của bot khác)
2.
3.

## Expected result

-

## Actual result

- Trước fix: hàm `updatePosition` dùng chung (`V2\CategoryService.php:89-91`) chạy `whereIn('id')->update(['position'])` không lọc theo `bot_id`/scope user → có thể ghi đè `position` của bản ghi thuộc bot khác hoặc hợp đồng của user khác (IDOR).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

(Redmine #42771 không có attachment — `Attachments (0)`.)

## Ghi chú thêm của Leader

- ⚠️ Bug không tái hiện được dạng cổ điển (không có Steps/Expected/Actual) — root cause + hướng fix đã được Dev Studio confirm qua 2 journal (file `03-dev-impact.md`). TCs nên tập trung verify cách fix (chặn IDOR + validate id) + regression của 5 chức năng sort dùng chung hàm `updatePosition`.
- Môi trường phát hiện: audit nội bộ (không ghi rõ Production/Staging/Dev).
- Severity gốc: `[Low]` (2/10) theo audit — nhưng impact thực tế là IDOR trên dữ liệu `position`, ảnh hưởng hồi quy rộng vì hàm dùng chung cho 5 chức năng.
- Branch fix: `ai_studio_implement_42771` (gốc `release_step_20260930_v2@0637cd04f7c1`, commit `1581ac16c6f42833ee0b0f7647d8d8e63d3176a9`).
- Vấn đề phát sinh **ngoài phạm vi ticket** (Dev ghi rõ, không fix trong task này): `PathIntroController::sort` (super admin) truyền `'desc'` chữ thường nên `updatePosition` không đảo thứ tự (so sánh `== 'DESC'`) — cần raise ticket riêng nếu cần fix, **không** đưa vào coverage của task #42771.

## Dữ liệu định danh ca lỗi

<!-- Ticket không có ca lỗi cụ thể (bot_id / friend / thời điểm) — đây là audit finding, không phải bug report theo ca cụ thể. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #143085 — Dev Studio — 2026-10-12:**

```
Dev Studio · Nội dung thực hiện (v1)

Thiết kế v1 xong, có thể thực thi. Hàm sắp xếp vị trí dùng chung sẽ chỉ nhận id dạng số (hiện id bị nối thẳng vào SQL) và nhận thêm bot để lọc. Sắp xếp thư mục/rich menu chỉ ghi dữ liệu của bot hiện tại. Sắp xếp hợp đồng không lọc theo bot hiện tại, vì danh sách hợp đồng gồm nhiều bot và gần một nửa hợp đồng không có bot_id; thay vào đó chỉ lấy các hợp đồng mà user đang thấy. Id nằm ngoài phạm vi bị bỏ qua và response vẫn như cũ.

Hướng sửa:
- D-1 updatePosition chỉ nhận id số và lọc theo bot khi được truyền bot
- D-2 Sắp xếp thư mục và rich menu v2 truyền bot hiện tại
- D-3 Sắp xếp hợp đồng chỉ ghi hợp đồng user đang thấy

Ảnh hưởng / rủi ro:
Ảnh hưởng thao tác sắp xếp thư mục và rich menu ở màn danh sách rich menu v2, modal sắp xếp ở danh sách hợp đồng, và sắp xếp LP của super admin (chỉ thêm validate id). Không đổi schema, route, FE hay response khi thành công. Rủi ro chính là lọc nhầm hợp đồng hợp lệ ở D-3, nên cần test với user có hợp đồng của nhiều bot.
```

**Journal #143108 — Dev Studio — 2026-10-12:**

```
Dev handoff — v1 · nhánh ai_studio_implement_42771

Tóm tắt:
Vá lỗ hổng IDOR-MSG-22 ở hàm sắp xếp vị trí dùng chung. Sắp xếp thư mục và rich menu giờ chỉ ghi bản ghi của bot đang chọn; sắp xếp hợp đồng chỉ ghi hợp đồng nằm trong danh sách user đang thấy; id không phải số bị chặn trước khi tạo SQL. Không đổi giao diện, route hay response. Khi test cần chú ý nhất: user có hợp đồng của nhiều bot hoặc hợp đồng chưa gắn bot vẫn sắp xếp và lưu đúng thứ tự.

Nội dung thay đổi:
- Rich menu v2, sắp xếp thư mục và sắp xếp rich menu: chỉ cập nhật vị trí của bản ghi thuộc bot đang chọn; id của bot khác bị bỏ qua.
- Danh sách hợp đồng (point-settings), modal sắp xếp: chỉ cập nhật hợp đồng thuộc danh sách của user (chủ hợp đồng hoặc staff có quyền pointSettings); id ngoài phạm vi bị bỏ qua và ghi log; id không phải số thì trả status false.
- Super admin, sắp xếp LP và thư mục LP: chỉ thêm kiểm tra id phải là số, hành vi không đổi.

File đã sửa (php-web):
  .../Controllers/V2/Bill/ListPageController.php     | 42 ++++++++++++++++++++--
  app/Services/V2/CategoryService.php                | 15 ++++++--
  app/Services/V2/RichMenuService.php                |  4 +--
  3 files changed, 55 insertions(+), 6 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi nhỏ ở 3 file, điều kiện lọc trùng với truy vấn danh sách đang có nên thao tác hợp lệ không bị ảnh hưởng; không có migration.
- CategoryService::updatePosition là hàm dùng chung của 5 chức năng sắp xếp (thư mục rich menu, rich menu, hợp đồng, LP, thư mục LP), nên cần test hồi quy cả 5.
- Cột position của các bảng category, rich_menus, bot_contracts, path_intro_data, category_super_admin; updated_at vẫn không đổi khi sắp xếp.
- Thứ tự hiển thị của danh sách hợp đồng (sắp theo position giảm dần) và của danh sách thư mục / rich menu.
- Nhánh #42428 (chặn sắp xếp rich menu ở controller) và #42427 (sửa RichMenuService ở chỗ khác): đã thử merge, không xung đột; khi gộp sẽ thành hai lớp bảo vệ.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Việc cần người làm thêm (ngoài phạm vi task):
- Caller super admin PathIntroController::sort truyền 'desc' chữ thường nên updatePosition không đảo thứ tự (so sánh == 'DESC'). Lỗi này nằm ngoài ticket, nên kiểm riêng nếu thứ tự LP bị ngược.

Điểm cần test:
- Bot A sắp xếp thư mục rich menu và rich menu ở màn danh sách rich menu v2: thứ tự lưu đúng như trước.
- Sửa tay request sort (thư mục / rich menu), chèn id của bot B: position của bot B không đổi, id của bot A vẫn được lưu, response như cũ.
- User có hợp đồng của nhiều bot (kể cả hợp đồng bot_id NULL) sắp xếp ở modal 保存 của danh sách hợp đồng: thứ tự lưu đúng.
- Sửa tay request save-contract-position, chèn id hợp đồng của user khác: hợp đồng đó không đổi position, response status true.
- Gửi id không phải số (abc, '1 THEN 0 END') ở cả sort rich menu và sort hợp đồng: không chạy SQL, response status false, không lỗi 500.
- Super admin sắp xếp LP và thư mục LP: hoạt động như cũ.
- Rich menu v2: sắp xếp thư mục bằng modal 並べ替え rồi reload, thứ tự phải giữ đúng như đã kéo.
- Rich menu v2, trong một thư mục: sắp xếp rich menu rồi reload, thứ tự phải giữ đúng.
- Gửi tay POST /ajax/folder/rich-menu/sort và /ajax/rich-menu/list/sort có chèn id của bot B: position của bot B không đổi, id của bot A vẫn lưu đúng (API vẫn trả status true).
- Danh sách hợp đồng (point-settings): thử với user có hợp đồng của nhiều bot, có hợp đồng chưa gắn bot (LINE公式アカウント未接続) và với staff có quyền pointSettings. Sắp xếp ở modal 並べ替え, bấm 保存 rồi reload: thứ tự phải đúng.
- Gửi tay POST /ajax/point-settings/save-contract-position có id hợp đồng của user khác: hợp đồng đó không đổi position, response status true, log có dòng 'saveContractPosition skip contract ids out of scope'.
- Gửi id dạng '1 THEN 0 END--' hoặc 'abc' vào API sắp xếp hợp đồng: response status false, không lỗi 500, không bản ghi nào đổi.
- Super admin: sắp xếp LP và thư mục LP vẫn chạy như trước.
- Khi bot đang backup: hai API sắp xếp rich menu vẫn trả thông báo backup như cũ.

Branch: ai_studio_implement_42771
- sns-line: ai_studio_implement_42771 (nhánh gốc release_step_20260930_v2 @0637cd04f7c1, commit 1581ac16c6f42833ee0b0f7647d8d8e63d3176a9)
```
