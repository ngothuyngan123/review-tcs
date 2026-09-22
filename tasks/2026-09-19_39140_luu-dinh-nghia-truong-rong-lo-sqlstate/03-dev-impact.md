# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #39140 bởi `/new-task`. Nguồn: **Journal #137195** (AI LME Fix bug — tự review v3, 2026-09-19). Bản này **thay thế** Journal #131890 (vòng 1, 2026-08-21).
>
> ⚠️ **Mâu thuẫn trong report Dev** — cần hỏi lại trước khi test:
> - Mục CẬP NHẬT ghi commit guard chéo bot `fff7807509` **"CHƯA PUSH"**, nhưng mục BRANCH / COMMIT ghi `fff7807509 ... [đã push]`.
> - Mục 6 VERIFY vẫn là số liệu vòng 1 (`git diff --stat release_step_20260623...`: 1 file, 20 thêm / 1 xóa), **chưa cập nhật** sau khi thêm guard chéo bot.
> - Mục TỰ REVIEW vẫn ghi "Cả **3** màn giao diện gọi API này", mâu thuẫn với đính chính v3 (chỉ **1** caller sống).

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | AI LME Fix bug (Auto-fixbug) · assignee Redmine: Ngọc Ánh |
| Commit / Pull Request | `sns-line` commit `fff7807509` (guard chéo bot, v3) · `c800d79495` (fix vòng 1) · merge release `74015bf5ad` (tungks). Chưa có link PR |
| Branch | `ai_fixbug_39140` (base `release_step_20260827`) |
| Ngày submit đánh giá | 2026-09-19 (Journal #137195) |
| Auto-filled | 2026-09-19 by /new-task |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại Section "Đánh giá ảnh hưởng" từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

---

## 1. Nguyên nhân

Chức năng lưu định nghĩa trường thông tin bạn bè chỉ kiểm tra bắt buộc tên quản lý ở giao diện, phía máy chủ không kiểm tra lại. Khi gọi thẳng API với tên rỗng, chuỗi rỗng bị hệ thống tự chuyển thành null rồi ghi xuống cột không cho phép null nên lỗi rơi xuống tầng cơ sở dữ liệu. Khối bắt lỗi của chức năng lại trả nguyên văn thông báo lỗi cơ sở dữ liệu (kèm mã lỗi, tên bảng và câu lệnh thêm mới) về cho client, vừa khó hiểu với người dùng vừa lộ cấu trúc bảng.

Bằng chứng (mục 6 của Dev): `friend_information_setting.title` varchar(255) NOT NULL, không default; `app/Http/Kernel.php:24-25` bật `TrimStrings` + `ConvertEmptyStringsToNull` → title rỗng thành null trước khi tới controller; `action_info_friend_default.title` cũng NOT NULL → nhánh trường mặc định 生年月日 (d_4) cũng bị chặn cùng lúc.

## 2. Cách fix

Thêm kiểm tra phía máy chủ cho tên quản lý ngay đầu nhánh xử lý trường tùy chỉnh của chức năng lưu định nghĩa trường thông tin bạn bè: bỏ trống thì trả thông báo nghiệp vụ 友だち情報（管理名）を1つ以上設定して下さい。, dài quá 20 ký tự thì trả 友だち情報（管理名）は20文字以内で入力してください。 Đồng thời khối bắt lỗi của chức năng không trả nguyên văn thông báo lỗi hệ thống ra client nữa mà trả thông báo lỗi hệ thống chung theo mẫu sẵn có của dự án, chi tiết lỗi vẫn ghi đầy đủ vào log. Về quan hệ ticket: Redmine khai cha là #38905 nhưng ticket cha đã đẩy mã nguồn và đóng từ 27/07/2026, nguyên nhân gốc cũng khác hẳn, nên sửa độc lập trên nhánh riêng ai_fixbug_39140.

**CẬP NHẬT 2026-09-19 (tự review v3):**
1. Nhánh đã được merge release mới nhất `release_step_20260827` (commit `74015bf5ad` do tungks thực hiện) — nhánh nay 0 commit behind release, merge sạch, không làm rơi fix; fix VẪN CHƯA vào release nên cần human merge PR `ai_fixbug_39140` → `release_step_20260827`.
2. THEO YÊU CẦU HUMAN, đã fix thêm lỗi BẢO MẬT phát hiện khi tự review (commit `fff7807509`, CHƯA PUSH): endpoint lưu định nghĩa trường chỉ có middleware basic_access và lấy id trần từ request mà không kiểm chủ sở hữu — câu update chính có lọc bot_id nhưng các câu kèm theo thì không, nên admin của bot A gửi id của bot B là sửa/xoá được dữ liệu bot B (set null cột action, xoá option/value, ghi đè bộ đếm). Dùng lại helper `isInfoSettingOfCurrentBot()` mà #40697 đã thêm làm guard ngay cửa vào hàm, trả HTTP 404 (không dùng abort() vì sẽ bị khối catch nuốt thành lỗi hệ thống 200); mã mặc định d_x, mã âm và trường hợp tạo mới vẫn đi tiếp như cũ. Đã kiểm không hồi quy: màn sửa (editInfo) vốn đã kiểm chủ sở hữu bằng đúng 2 nguồn của helper trước khi render id ra trang, nên guard là no-op với mọi luồng hợp lệ.
3. ĐÍNH CHÍNH report: hàm `saveInforFriend` trong `public/js/tag/add_tag.js` và `public/js/tag/edit_v2.js` là CODE CHẾT (không nơi nào gọi; nút 保存 của 2 màn thẻ gọi `saveTag()` → `/ajax/save-tag`), nên caller sống duy nhất của endpoint này là màn 友だち情報管理 (`create.js`) — Tag Management KHÔNG bị ảnh hưởng như report ban đầu khai.

Tự review của Dev: đặt kiểm tra bên trong nhánh trường tùy chỉnh nên không ảnh hưởng quy tắc bỏ qua các trường mặc định d_1/d_2/d_3/d_6 (vẫn trả thành công như cũ). Giới hạn 20 ký tự vượt ngoài yêu cầu ticket, người review quyết định GIỮ LẠI (21/08/2026).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

> Số dòng theo base `release_step_20260827`.

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `FriendInformationController::saveSettingInfoFriend` (`app/Http/Controllers/Basic/FriendInformationController.php:1039`) | **Điểm sửa**: guard chủ sở hữu tại :1045-1057, validate 管理名 tại :1070-1082, catch tại :1577-1584 | Root fix |
| 2 | `FriendInformationController::isInfoSettingOfCurrentBot` (:113) | Không sửa — dùng lại làm guard | Helper của #40697; mã `d_x` / mã âm / id rỗng vẫn cho qua |
| 3 | `FriendInformationController::editInfo` (:79) | Không | Đã kiểm cùng 2 nguồn với helper ⇒ `id_setting` render ra màn sửa LUÔN thuộc bot hiện tại ⇒ guard là no-op với luồng hợp lệ |
| 4 | `FriendInformationController::addInfo` (:59) / `copyInfo` (:123) | Không | Không render `id_setting` ⇒ gửi id rỗng ⇒ guard cho qua |
| 5 | `FriendInformationController::initDataInfo` (:147) | Không | Nạp dữ liệu màn sửa; #40697 đã vá scope bot_id |
| 6 | `saveInforFriend` (`public/js/infor_friend/create.js:233`, gọi API tại :268) | Không | **CALLER SỐNG DUY NHẤT** của endpoint; nút 保存 tại `resources/views/basic/friend_information/create.blade.php:532`; id gửi lên = `#id_setting` (id `friend_information_setting` của chính bot, hoặc `d_x`, hoặc rỗng) |
| 7 | `saveInforFriend` (`public/js/tag/add_tag.js:109`) | Không | ⚠ CODE CHẾT: nút 保存 của màn thêm thẻ gọi `saveTag()` (`add_tag.blade.php:193`) → `/ajax/save-tag`. Trên màn này `#id_setting` là TAG id |
| 8 | `saveInforFriend` (`public/js/tag/edit_v2.js:124`) | Không | ⚠ CODE CHẾT: nút 保存 gọi `saveTag()` (`tag/v2/edit.blade.php:666`); `id_setting` = tag id do `TagController::editTag` truyền vào |
| 9 | `routes/web.php:1205` | Không | Route duy nhất gọi endpoint (group middleware basic_access / https_protocol / is_expire / check_remember_token tại `routes/web.php:933`) |
| 10 | `FriendInfoMobileController::saveFriendInfoField` (`app/Http/Controllers/Api/Mobile/FriendInfoMobileController.php:240`) | **Không sửa** | Cùng lỗi (thiếu validate + rò `getMessage` + không guard bot), thuộc mobile, **ngoài phạm vi** |

---

## 4. Đánh giá ảnh hưởng

> Dev khai 4.1 dạng "File thay đổi" (1 file: `app/Http/Controllers/Basic/FriendInformationController.php`). Bảng F* dưới đây gom từ mục 3 + 4 của Dev để map coverage.

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `saveSettingInfoFriend` — validate 管理名 (rỗng / > 20 ký tự) ở nhánh trường tùy chỉnh | `app/Http/Controllers/Basic/FriendInformationController.php` | Direct | :1070-1082 |
| F2 | `saveSettingInfoFriend` — catch trả message chung `システムエラーが発生しました。/ 管理者へ問い合わせください。`, chi tiết ghi log `saveSettingInfoFriend failure >>` | cùng file | Direct | :1577-1584 |
| F3 | `saveSettingInfoFriend` — guard chủ sở hữu chéo bot qua `isInfoSettingOfCurrentBot()` → HTTP 404 `設定が見つかりません` | cùng file | Direct | :1045-1057 · bổ sung v3 · log `saveSettingInfoFriend bị chặn: ...` |
| F4 | `saveInforFriend` (`create.js`) — caller UI duy nhất | `public/js/infor_friend/create.js` | Indirect | FE đã chặn sẵn rỗng / > 20 ký tự |
| F5 | `editInfo` / `addInfo` / `copyInfo` / `initDataInfo` — nguồn `id_setting` gửi lên endpoint | `FriendInformationController.php` | Indirect | Dev khẳng định guard là no-op với luồng hợp lệ |
| F6 | `FriendInfoMobileController::saveFriendInfoField` | `app/Http/Controllers/Api/Mobile/FriendInfoMobileController.php` | Không sửa (cùng lỗi) | Ngoài phạm vi |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `friend_information_setting.title` (varchar(255) NOT NULL) | Không ghi mới — chặn trước khi ghi | Từ nay không nhận NULL hoặc chuỗi > 20 ký tự qua endpoint này; bản ghi cũ giữ nguyên |
| D2 | `action_info_friend_default.title` (nhánh trường mặc định d_4 生年月日) | Không ghi mới — chặn trước khi ghi | Cùng được chặn |
| D3 | **Hợp đồng response** `POST /basic/save-setting-info-friend` — trường `msg` | Đổi nội dung | Trước trả nguyên văn exception (SQLSTATE + câu SQL), nay trả message nghiệp vụ tiếng Nhật hoặc `システムエラーが発生しました。/ 管理者へ問い合わせください。` cho MỌI ngoại lệ. `status` + HTTP code không đổi → FE không vỡ; TC tự động khớp chuỗi `msg` cũ sẽ fail |
| D4 | Guard chéo bot — `friend_information_value.action` (set null) · `friend_information_value` + `friend_info_option_selects` (xoá) · `friend_information_setting.total_user_has_value` (ghi đè) của **bot khác** | Chặn (HTTP 404) | Trước fix: request mang id bot khác âm thầm ghi/xoá dữ liệu bot nạn nhân. Không có ca hợp lệ nào bị chặn thêm |

Dữ liệu đã lưu: **KHÔNG đổi** — không INSERT/UPDATE/migration nào. ✔ Không cần recover data.

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Friend Information Management (FA-015) — chặn lưu trường khi thiếu / quá dài 管理名, trả message nghiệp vụ thay vì lỗi DB | F1, F2, F4, D1, D3 | Medium (Dev không ghi mức) |
| T2 | FA-015 — chặn ghi/xoá chéo bot ở đường lưu định nghĩa trường | F3, F5, D4 | High (bảo mật; Dev không ghi mức) |
| T3 | Trường mặc định 生年月日 (d_4) của FA-015 — không nằm trong danh sách bỏ qua nên đi qua validate mới; mã `d_x` được guard cho qua | F1, F3, D2 | Medium (Dev không ghi mức) |
| T4 | Tag Management (FA-012) — ⚠ **ĐÍNH CHÍNH v3**: KHÔNG gọi endpoint này ⇒ KHÔNG bị ảnh hưởng | — | Low |
| T5 | Vận hành QA/support — lỗi hệ thống ở màn này chỉ hiện message chung, phải tra log theo mốc `saveSettingInfoFriend failure >>`; request chéo bot ghi log `saveSettingInfoFriend bị chặn: ...` | F2, F3, D3 | Low (Dev không ghi mức) |

**Rủi ro / lưu ý khi test (Dev ghi):**
- Nếu sau này có luồng nội bộ nào gọi API này với tên quản lý > 20 ký tự thì sẽ bị chặn — 3 màn giao diện hiện có đều giới hạn 20 ký tự nên rủi ro thấp.
- Thông báo lỗi hệ thống chung làm mất chi tiết lỗi ở màn hình khi có lỗi khác; chi tiết vẫn còn đủ trong log.

**Verify của Dev:** mức `lint` (`php -l` không lỗi cú pháp) — chưa có test runtime.

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code
- [ ] Mục 3 đã check đủ caller (hỏi Dev nếu nghi ngờ sót)
- [ ] Mục 4.1 không thiếu function (so với mục 3)
- [ ] Mục 4.2 không thiếu data (đặc biệt: cache, log, export file)
- [ ] Mục 4.3 cover được cả **happy path lẫn edge case** của tính năng
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
