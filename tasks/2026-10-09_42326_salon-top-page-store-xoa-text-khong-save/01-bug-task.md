# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine qua `/new-task 42326` (`scripts/redmine_fetch.py`).
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL) tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42326 — [Salon] Setting top page / Setting store: Không thể save khi xóa toàn bộ text` |
| Module / Màn hình | Salon (FA-020 — 「サロン・面談予約」, `/basic/calendar-salon`), module **Admin web**: 予約画面 → 「トップ画面設定」 (Setting top page) và 「店舗・ビジネス情報」 (Setting store) — ô テキスト (TinyMCE). Hai màn dùng chung endpoint lưu `POST /ajax/calendar-salon/save/info` (`CalendarSalonController@saveCalendarInfo`). |

## Mô tả bug (bản dịch tiếng Việt)

> Ticket đã viết bằng tiếng Việt, toàn bộ nội dung là Thao tác / Actual / Expected — chép nguyên văn ở 3 section bên dưới, không diễn giải lại.

Ở màn [Setting top page] / [Setting store] của Salon: xóa toàn bộ text đã nhập rồi nhấn Save thì không lưu được — UI báo Save success nhưng text cũ vẫn còn.

## Steps to reproduce

1. Vào màn [Setting top page] hoặc [Setting store].
2. Nhập text vào field.
3. Nhấn Save.
4. Xóa toàn bộ text đã nhập.
5. Nhấn Save.
6. Reload màn hình và kiểm tra lại dữ liệu.

## Expected result

- Khi xóa toàn bộ text và nhấn Save, hệ thống phải lưu giá trị rỗng và UI sau khi reload không còn text cũ.

## Actual result

- UI hiển thị Save success nhưng text cũ vẫn còn

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- Screenshot27.png — https://redmine.melonglobal.net/attachments/download/32073/Screenshot27.png

## Ghi chú thêm của Leader

- Tracker `Bug tự detect` (team tự phát hiện, không phải khách báo) — description không ghi môi trường phát hiện.
- Toast thành công trên UI: 「編集が保存されました」 (theo Journal #141125). Bug xảy ra 100% khi xoá **hết** テキスト — không phải xác suất.
- ⚠️ **Phạm vi fix đã mở rộng ở vòng v2** (Journal #142199 + #142201, 2026-10-09): ngoài テキスト (D-1), Dev sửa thêm **xoá ảnh ở 店舗・ビジネス情報** (cột `image_calendar`, D-2) — cùng nguyên nhân `isset(null)`. Journal #142201 dẫn chiếu ticket **#42605** cho điểm test xoá ảnh.
- Record lưu text/ảnh **trước** bản fix không được tự sửa — sau release người dùng phải xoá lại (Dev: không cần recover dữ liệu).
- Điểm chưa chốt: テキスト chỉ gồm khoảng trắng / xuống dòng — Journal #141358 ghi "sau lưu coi như trống", nhưng Studio `dev_impact` ghi "code không trim ⇒ có thể lưu `<p>&nbsp;</p>`, không phải NULL" (REQ-009 Studio: expected chờ human chốt).

## Journal / note từ Redmine (nguyên văn)

**Journal #141125 — Dev Studio — 2026-10-08:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
Khi ô テキスト (TinyMCE) bị xoá hết, màn hình gửi `description_top` / `description` là chuỗi rỗng; middleware toàn cục `ConvertEmptyStringsToNull` đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, hai cột này chỉ được đưa vào UPDATE khi `isset(...)` đúng, mà `isset(null)` = false, nên cột bị bỏ qua và text cũ giữ nguyên. Server vẫn trả success nên UI hiện toast 「編集が保存されました」.

Hướng sửa:
- D-1 Ghi cả giá trị rỗng cho テキスト ở hàm lưu thông tin lịch Salon

Ảnh hưởng / rủi ro:
Chỉ ảnh hưởng endpoint lưu thông tin lịch Salon dùng chung cho 2 màn トップ画面設定 và 店舗・ビジネス情報: hai cột テキスト giờ được ghi cả khi rỗng (NULL). Cần test cả việc lưu ở màn này không làm mất text của màn kia, và trang top phía khách hiển thị đúng khi text trống.
```

**Journal #141358 — Dev Studio — 2026-10-08:**

```
Dev handoff — v1 · nhánh ai_studio_fixbug_42326

Nguyên nhân:
Khi ô テキスト (TinyMCE) bị xoá hết, màn hình gửi `description_top` / `description` là chuỗi rỗng; middleware toàn cục `ConvertEmptyStringsToNull` đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, hai cột này chỉ được đưa vào UPDATE khi `isset(...)` đúng, mà `isset(null)` = false, nên cột bị bỏ qua và text cũ giữ nguyên. Server vẫn trả success nên UI hiện toast 「編集が保存されました」.

Nội dung thay đổi:
- Salon → 予約画面 → トップ画面設定: xoá hết テキスト → 保存 → reload: ô trống, プレビュー và trang top LIFF không còn text cũ (og:description quay về tên LINE).
- Salon → 予約画面 → 店舗・ビジネス情報: xoá hết テキスト → 保存 → reload: ô trống, プレビュー không còn text cũ.
- Endpoint lưu thông tin Salon (POST /ajax/calendar-salon/save/info, module web): khoá description/description_top có gửi lên (kể cả rỗng) thì ghi, không gửi thì giữ nguyên.

File đã sửa (php-web):
  app/Http/Controllers/Basic/CalendarSalonController.php | 6 ++++--
  1 file changed, 4 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Một điều kiện ở một hàm, cột nullable, mọi nơi đọc đã xử lý NULL, có harness và kiểm chứng ngược; chưa verify runtime.
- Hai màn トップ画面設定 và 店舗・ビジネス情報 dùng chung một request lưu ⇒ mỗi lần 保存 ghi cả 2 cột theo nội dung hiện có trong 2 editor (đã nạp từ DB khi mở màn); test chéo xoá/sửa ở màn này, text màn kia giữ nguyên.
- Trang đặt lịch phía khách (LIFF) của Salon: khối top page và 店舗情報 hiển thị từ 2 cột này ⇒ kiểm khi cột NULL và khi có text.
- og:description khi share link top page (lấy text top, không có thì tên LINE).
- Preview (プレビュー) của 2 màn.
- API mobile Mobile/CalendarSalonController đọc description_top làm mô tả (đã có !empty) — chỉ cần smoke.
- Lesson (CalendarManagementController) không bị chạm.

Việc cần người làm thêm (ngoài phạm vi task):
- Lỗi riêng cùng nguyên nhân: ở 店舗・ビジネス情報 bấm 削除 ảnh rồi 保存 thì ảnh không bị xoá (cột image_calendar cũng dùng isset, ảnh cũ hiện lại ngay sau khi lưu) — đề xuất tạo ticket riêng.
- Xoá ảnh ở 店舗・ビジネス情報 (image_calendar) cũng dùng isset nên có thể không lưu được. Đây là lỗi riêng, ngoài phạm vi ticket này: cần mở ticket riêng nếu muốn sửa.
- Cùng hàm saveCalendarInfo của Salon: image_calendar vẫn dùng isset ⇒ bấm 削除 ảnh ở 店舗・ビジネス情報 rồi 保存 thì ảnh không bị xoá; mở ticket riêng (đã thống nhất ở thiết kế).

Điểm cần test:
- トップ画面設定: nhập テキスト → 保存 → xoá hết → 保存 → reload: ô テキスト trống; プレビュー và trang top phía khách không còn text cũ.
- 店舗・ビジネス情報: cùng kịch bản với ô テキスト; プレビュー không còn text cũ.
- Xoá text ở トップ画面設定 rồi lưu thì text ở 店舗・ビジネス情報 không bị mất (và ngược lại).
- Nhập mới / sửa text vẫn lưu đúng (hồi quy).
- トップ画面を表示しない + text trống lưu được; 店舗名 trống khi bật trang top vẫn báo 「店舗名を入力してください。」.
- Lịch Salon chưa từng có text (NULL): lưu không lỗi, cột vẫn NULL.
- トップ画面設定: nhập テキスト → 保存 → xoá hết → 保存 → reload: ô trống; プレビュー và trang top LIFF không còn text cũ.
- 店舗・ビジネス情報: cùng kịch bản; プレビュー và khối 店舗情報 phía khách không còn text cũ.
- Xoá テキスト ở トップ画面設定 rồi 保存 ⇒ テキスト ở 店舗・ビジネス情報 không mất (và ngược lại).
- Nhập テキスト mới / sửa テキスト ⇒ lưu và hiển thị đúng (hồi quy).
- テキスト chỉ gồm khoảng trắng/xuống dòng ⇒ sau lưu coi như trống.
- トップ画面を表示しない + テキスト trống ⇒ lưu được; bật trang top mà 店舗名 trống vẫn báo 「店舗名を入力してください。」.
- Lịch Salon chưa từng có テキスト (NULL) ⇒ 保存 ở màn khác không lỗi, ô vẫn trống.
- Share link top page sau khi xoá テキスト ⇒ og:description là tên LINE.

Branch: ai_studio_fixbug_42326
- sns-line: ai_studio_fixbug_42326 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit 1982d6b3fe12cdb06acf6376e7b04d31788ea891)
```

**Journal #142199 — Dev Studio — 2026-10-09:**

```
Dev Studio · Nguyên nhân & hướng sửa (v2)

Nguyên nhân:
Khi bấm 削除 ảnh ở 店舗・ビジネス情報, màn hình gửi `image_calendar` rỗng; middleware `ConvertEmptyStringsToNull` của Laravel đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, cột `image_calendar` chỉ được ghi khi `isset(...)` đúng, mà `isset(null)` = false, nên ảnh cũ không bị xoá. Server trả bản ghi còn ảnh cũ, JS gán lại vào màn nên ảnh hiện lại ngay. Ô テキスト (đã sửa ở D-1) bị đúng cơ chế này.

Hướng sửa:
- D-1 Ghi cả giá trị rỗng cho テキスト (đã làm ở vòng 1)
- D-2 Lưu được việc xoá ảnh ở 店舗・ビジネス情報

Ảnh hưởng / rủi ro:
Chỉ endpoint lưu thông tin lịch Salon dùng chung cho トップ画面設定 và 店舗・ビジネス情報: cột ảnh 店舗 giờ được ghi theo giá trị trên màn, kể cả rỗng khi bấm 削除. Cần test lưu ở màn này không làm mất ảnh của màn kia, và trang đặt lịch phía khách hiển thị đúng khi không có ảnh.
```

**Journal #142201 — Dev Studio — 2026-10-09:**

```
Dev handoff — v2 · nhánh ai_studio_fixbug_42326

Nguyên nhân:
Khi bấm 削除 ảnh ở 店舗・ビジネス情報, màn hình gửi `image_calendar` rỗng; middleware `ConvertEmptyStringsToNull` của Laravel đổi thành null. Trong `CalendarSalonController@saveCalendarInfo`, cột `image_calendar` chỉ được ghi khi `isset(...)` đúng, mà `isset(null)` = false, nên ảnh cũ không bị xoá. Server trả bản ghi còn ảnh cũ, JS gán lại vào màn nên ảnh hiện lại ngay. Ô テキスト (đã sửa ở D-1) bị đúng cơ chế này.

Nội dung thay đổi:
- 予約画面 → トップ画面設定: xoá hết テキスト → 保存 → reload: ô trống; プレビュー và trang top phía khách không còn text cũ (og:description quay về tên LINE).
- 予約画面 → 店舗・ビジネス情報: xoá hết テキスト → 保存 → reload: ô trống; プレビュー và khối 店舗情報 phía khách không còn text cũ.
- 予約画面 → 店舗・ビジネス情報: bấm 削除 ảnh → 保存: ngay sau lưu và sau reload hiện ảnh mặc định + 「設定されていません」; プレビュー và trang khách không còn ảnh.
- Endpoint lưu thông tin Salon (POST /ajax/calendar-salon/save/info, module web): các khoá image_calendar, description, description_top có gửi lên (kể cả rỗng) thì ghi, không gửi thì giữ nguyên.

File đã sửa (php-web):
  app/Http/Controllers/Basic/CalendarSalonController.php | 10 +++++++---
  1 file changed, 7 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ 3 điều kiện ghi trong 1 hàm, các cột đều cho phép NULL, mọi nơi đọc đã xử lý NULL, có harness và kiểm chứng ngược ở 2 mốc; chưa verify runtime.
- Hai màn トップ画面設定 và 店舗・ビジネス情報 dùng chung một request lưu ⇒ mỗi lần 保存 ghi lại テキスト cả 2 màn và ảnh 店舗 theo giá trị đang có trên màn (nạp từ DB khi mở); test chéo để chắc thao tác ở màn này không làm mất dữ liệu màn kia.
- Đổi ảnh (変更/アップロード) ở 店舗・ビジネス情報 và ảnh trang top: nhánh tải ảnh không đổi nhưng nằm cùng hàm, cần smoke.
- Trang đặt lịch phía khách (LIFF) của Salon: khối top page, ảnh và テキスト 店舗情報 hiển thị từ các cột này.
- og:description khi share link trang top (lấy テキスト top, không có thì tên LINE).
- プレビュー của 2 màn.
- API mobile của Salon đọc description_top (đã xử lý rỗng) — smoke.
- Lesson (CalendarManagementController) không bị chạm.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Bug chỉ làm thao tác xoá (テキスト hoặc ảnh) không có hiệu lực: giá trị cũ vẫn còn nguyên, không có dữ liệu bị mất hay hỏng. DB không lưu lại ý định xoá nên cũng không xác định được bản ghi nào bị ảnh hưởng; người dùng xoá lại sau khi bản sửa lên là đủ.

Điểm cần test:
- 店舗・ビジネス情報: có ảnh → 削除 → 保存 → ảnh mặc định + 「設定されていません」 ngay sau khi lưu và sau reload; プレビュー và trang đặt lịch phía khách không còn ảnh.
- 店舗・ビジネス情報: 削除 rồi tải ảnh khác → 保存 thì lưu ảnh mới; 変更 ảnh vẫn đúng.
- Lưu ở トップ画面設定 hoặc lưu 店舗・ビジネス情報 mà không đụng ảnh thì ảnh 店舗 vẫn còn.
- Xoá ảnh ở トップ画面設定 vẫn đúng như trước (hồi quy).
- Hồi quy D-1: xoá hết テキスト ở 2 màn → 保存 → reload không còn text cũ.
- トップ画面設定: nhập テキスト → 保存 → xoá hết → 保存 → reload: ô trống; プレビュー và trang top phía khách không còn text cũ.
- 店舗・ビジネス情報: cùng kịch bản テキスト; プレビュー và khối 店舗情報 phía khách không còn text cũ.
- 店舗・ビジネス情報: có ảnh → 削除 → 保存 → ngay sau lưu và sau reload là ảnh mặc định + 「設定されていません」; プレビュー và trang khách không còn ảnh (#42605).
- 店舗・ビジネス情報: 削除 rồi tải ảnh khác → 保存 ⇒ lưu ảnh mới; 変更 ảnh vẫn đúng.
- 店舗・ビジネス情報: chọn ảnh mới rồi 削除 trước khi 保存 ⇒ sau lưu không còn ảnh.
- Lưu ở トップ画面設定 (không đụng ảnh 店舗) ⇒ ảnh và テキスト 店舗・ビジネス情報 vẫn còn; và ngược lại với テキスト/ảnh trang top.
- Xoá ảnh trang top ở トップ画面設定 vẫn đúng như trước (hồi quy).
- Nhập/sửa テキスト ⇒ lưu đúng; テキスト chỉ khoảng trắng ⇒ coi như trống.
- トップ画面を表示しない + テキスト trống ⇒ lưu được; bật trang top mà 店舗名 trống vẫn báo 「店舗名を入力してください。」.

Branch: ai_studio_fixbug_42326
- sns-line: ai_studio_fixbug_42326 (nhánh gốc release_step_20260930_v2 @657ba962f25d, commit f5217491201dda62494b1ffd9c4c05b29194167f)
```
