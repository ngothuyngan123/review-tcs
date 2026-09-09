# Task đã có trong sheet checklist nhưng CHƯA Closed trên Redmine

**Nguồn:** Sheet checklist QA (tab 01.2026 → 07.2026) × Redmine.  
**Parent gốc được chỉ định:** [#26684 — [LME] BUG NỘI BỘ TỰ DETECT](https://redmine.watermelon.vn/issues/26684) (181 task con).  
**Ngày rà:** 2026-07-22.

## Tóm tắt

- Tổng số bug-ID **duy nhất** xuất hiện trong sheet checklist (7 tháng): **250**
- Trong đó **đã Closed** trên Redmine: **143**
- **CHƯA Closed (còn open): 107** ← danh sách cần xử lý

| Trạng thái Redmine | Số task | Ai cần xử lý |
|---|---|---|
| New | 65 | 🔴 **Member/team** (đã test xong nhưng chưa đẩy trạng thái) |
| Fix done - Đợi test | 18 | 🔴 **Member/team** (đã test xong nhưng chưa đẩy trạng thái) |
| Re-open | 1 | 🔴 **Member/team** (đã test xong nhưng chưa đẩy trạng thái) |
| Đang fix | 1 | 🔴 **Member/team** (đã test xong nhưng chưa đẩy trạng thái) |
| Released - đợi KH close | 11 | 🟡 Chờ khách hàng (KH) — bình thường vẫn open |
| Đợi KH confirm | 5 | 🟡 Chờ khách hàng (KH) — bình thường vẫn open |
| KH Feedback | 6 | 🟡 Chờ khách hàng (KH) — bình thường vẫn open |
| **Tổng** | **107** | |

→ **85 task** thuộc nhóm 🔴 (đã có trong checklist = đã test, nhưng trạng thái Redmine vẫn `New`/`Fix done-Đợi test`/`Re-open`/`Đang fix` — member chưa cập nhật/close).  
→ **22 task** thuộc nhóm 🟡 (đang chờ KH confirm/close — thường vẫn để open, không phải lỗi member).  
→ Trong tổng số 107, có **15 task** là con trực tiếp của parent #26684 (đánh dấu ⭐).

## 🔴 Nhóm 1 — Member cần xử lý (test xong nhưng chưa close/đẩy trạng thái) (85)

| Redmine ID | Trạng thái | ⭐26684 | Tiêu đề | Tester (sheet) | Assignee (Redmine) | Tracker | Tháng checklist |
|---|---|:--:|---|---|---|---|---|
| [#38866](https://redmine.watermelon.vn/issues/38866) | Fix done - Đợi test |  | [16-07-2026][T11593][Friend List] Lọc danh sách bạn bè theo 「6期生」 chọn | CucDTK | Ngô Thúy Ngần | Bug KH | 07.2026 |
| [#38859](https://redmine.watermelon.vn/issues/38859) | New |  | [JOB] Sync form trên google sheet chuyến sang batch để tăng tốc độ | ThanhNTP | Thanh Duy Nguyen | SpecImprove | 07.2026 |
| [#38820](https://redmine.watermelon.vn/issues/38820) | Fix done - Đợi test | ⭐ | [Friend info][QR Landing] Khi thực hiện quét QR có chứa param cid, hiể | HanhNTB | Hạnh Nguyễn | Bug tự detect | 07.2026 |
| [#38761](https://redmine.watermelon.vn/issues/38761) | New |  | [14-07-2026][Popup] Chức năng 「ポップアップ」 của LME có bị ảnh hưởng bởi chí | ThanhNTP | Ngô Thúy Ngần | Support | 07.2026 |
| [#38726](https://redmine.watermelon.vn/issues/38726) | Fix done - Đợi test | ⭐ | [lme][call] query messages_v2s bị treo quá 5p | CucDTK | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38694](https://redmine.watermelon.vn/issues/38694) | New |  | [Job] [Callback] Tách xử lý callback theo type của từng event | ThanhNTP | Thanh Duy Nguyen | Bug tự detect | 07.2026 |
| [#38670](https://redmine.watermelon.vn/issues/38670) | New |  | [10-07-2026][T11540][App + API app] Trên app điện thoại, badge chưa đọ | HaoDTB |  | Bug KH | 07.2026 |
| [#38632](https://redmine.watermelon.vn/issues/38632) | Fix done - Đợi test | ⭐ | [Detail friend] Salon, Lesson] Remind không setting action thì không h | AnhPTN | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38629](https://redmine.watermelon.vn/issues/38629) | Fix done - Đợi test | ⭐ | [Salon] khi đặt booking calendar thì xảy ra lỗi "order booking salon: | ThanhNTP | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38605](https://redmine.watermelon.vn/issues/38605) | New |  | [Detail line user] Step message cài đặt nhiều action friend info nhưng | HanhNTB | Thanh Duy Nguyen | Bug tự detect | 07.2026 |
| [#38587](https://redmine.watermelon.vn/issues/38587) | New | ⭐ | [Detail friend Salon/Lession] Preview action không hiển thị msg độc lậ | AnhPTN | Tuấn Anh Trần | Bug tự detect | 07.2026 |
| [#38574](https://redmine.watermelon.vn/issues/38574) | New | ⭐ | [Detail friend] Preview action form không hiển thị message độc lập | AnhPTN | Ngọc Ánh | Bug tự detect | 07.2026 |
| [#38552](https://redmine.watermelon.vn/issues/38552) | New |  | [07-07-2026][TY-11470][Form] Form 六甲お子様アンケートフォーム (ペット有) có 13 câu trả | ThanhNTP | Kieu Son Tung | Bug KH | 07.2026 |
| [#38537](https://redmine.watermelon.vn/issues/38537) | Fix done - Đợi test | ⭐ | [Salon] Tạo lịch làm việc từ 19h-00 giờ, ở app hiển thị O cả ngày hôm | CucDTK | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38536](https://redmine.watermelon.vn/issues/38536) | New |  | [Info friend][Ghi đè điểm] Sửa text lại thống nhất với 2 loại cộng thê | HanhNTB | Ngô Thúy Ngần | Support | 07.2026 |
| [#38519](https://redmine.watermelon.vn/issues/38519) | Fix done - Đợi test |  | [07-07-2026][28823][Salon] Dùng đặt lịch Salon: không thay đổi được th | CucDTK | Ngô Thúy Ngần | Bug KH | 07.2026 |
| [#38390](https://redmine.watermelon.vn/issues/38390) | Fix done - Đợi test | ⭐ | Khi delete friend bị chậm | CucDTK | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38312](https://redmine.watermelon.vn/issues/38312) | New |  | Khi lưu lịch sử thay đổi friend info chưa lưu được action preview | ThanhNTP | Do Van Tu TuDV | Bug Tester | 07.2026 |
| [#38296](https://redmine.watermelon.vn/issues/38296) | New |  | Add Detail friend: remind | ThanhNTP | Do Van Tu TuDV | Feature | 07.2026 |
| [#38155](https://redmine.watermelon.vn/issues/38155) | New |  | Thay vì tự động phản ánh vào lme, change spec thành dạng hiển thị moda | CucDTK | Do Van Tu TuDV | Feature | 07.2026 |
| [#37710](https://redmine.watermelon.vn/issues/37710) | Fix done - Đợi test |  | Modal multi action ở các màn hình xử lý không đúng khi có action bên t | HanhNTB | Ngô Thúy Ngần | Triển khai ngang | 07.2026 |
| [#37410](https://redmine.watermelon.vn/issues/37410) | New |  | [Send mail MyASP] Khi user đăng ký lme → tự động thêm vào danh sách ma | AnhPTN | Ngô Thúy Ngần | Feature | 07.2026 |
| [#35783](https://redmine.watermelon.vn/issues/35783) | New |  | Add thêm phân quyền Change LOA | AnhPTN, ThanhNTP | Do Van Tu TuDV | SpecImprove | 07.2026 |
| [#33106](https://redmine.watermelon.vn/issues/33106) | Fix done - Đợi test | ⭐ | [App mobile] User staff không được phân quyền vẫn vào được màn salon v | NganNT | Ngô Thúy Ngần | Bug tự detect | 07.2026 |
| [#38226](https://redmine.watermelon.vn/issues/38226) | New |  | [Detail friend][Tag] Friend đang có tag được gắn thì mong muốn hiển th | HanhNTB | Hạnh Nguyễn | SpecImprove | 06.2026 |
| [#38206](https://redmine.watermelon.vn/issues/38206) | New |  | [26-06-2026][28626][QL Tag] Thứ tự tag khác nhau giữa Quản lý tag (タグ管 | HanhNTB | Kieu Son Tung | Bug KH | 06.2026 |
| [#38077](https://redmine.watermelon.vn/issues/38077) | New |  | Status authorized trả về khi bill univapay sẽ coi là trường hợp bill s | ThanhNTP |  | Bug Tester | 06.2026 |
| [#38003](https://redmine.watermelon.vn/issues/38003) | New |  | Sửa màn hình lịch sử access bot theo sort theo time_access | ThanhNTP |  | Bug Tester | 06.2026 |
| [#37932](https://redmine.watermelon.vn/issues/37932) | Fix done - Đợi test |  | [19-06-2026][No.11303][Booking Event] Hỏi đổi setting ảnh OGP (OGP画像) | ThanhNTP | Ngô Thúy Ngần | SpecImprove | 06.2026 |
| [#37831](https://redmine.watermelon.vn/issues/37831) | Fix done - Đợi test |  | [18-06-2026][T11287][Template] Khách báo 2 lỗi về Template: template g | ThanhNTP | Kieu Son Tung | Bug KH | 06.2026 |
| [#37743](https://redmine.watermelon.vn/issues/37743) | New |  | User đã login và select bot ngày hôm sau user vào đang không lưu lịch | ThanhNTP | Do Van Tu TuDV | Bug Tester | 06.2026 |
| [#37711](https://redmine.watermelon.vn/issues/37711) | Fix done - Đợi test |  | [16-06-2026][T11271][Scenario] Cùng một khách hiển thị thành 2 tài kho | CucDTK | Ngô Thúy Ngần | Bug KH | 06.2026 |
| [#37606](https://redmine.watermelon.vn/issues/37606) | Fix done - Đợi test |  | [15-06-2026][回答ID：28530][Info friend] Click thông tin bạn bè (友だち情報) t | HanhNTB | Kieu Son Tung | Bug KH | 06.2026 |
| [#37507](https://redmine.watermelon.vn/issues/37507) | New |  | [10-06-2026] [11188] [QR Code]Giá trị của tham số động sid có được tru | CucDTK | Do Van Tu TuDV | Bug KH | 06.2026 |
| [#37398](https://redmine.watermelon.vn/issues/37398) | New |  | [11-06-2026][T11205][QR Landing] Liên kết Google Sheets qua QR Code Ac | AnhPTN |  | SpecImprove | 06.2026 |
| [#37396](https://redmine.watermelon.vn/issues/37396) | New |  | [10-06-2026][11200][QR Landing] QR code action (QRコードアクション)「保留：アルコールse | CucDTK | Kieu Son Tung | Bug KH | 06.2026 |
| [#37316](https://redmine.watermelon.vn/issues/37316) | Fix done - Đợi test |  | [Màn add friend setting old, new, unblock, QR code action ] Khi bấm nú | AnhPTN | Kieu Son Tung | Triển khai ngang | 06.2026 |
| [#37239](https://redmine.watermelon.vn/issues/37239) | New |  | Improve cho màn talk list query bên database read | ThanhNTP | Do Van Tu TuDV | SpecImprove | 06.2026 |
| [#37229](https://redmine.watermelon.vn/issues/37229) | New |  | Feedback task tháng 5 | AnhPTN | Do Van Tu TuDV | Feature | 06.2026 |
| [#37085](https://redmine.watermelon.vn/issues/37085) | New |  | Improve plan enterprise | ThanhNTP | Tuấn Anh Trần | Feature | 06.2026 |
| [#37017](https://redmine.watermelon.vn/issues/37017) | Fix done - Đợi test |  | [03-06-2026] [Menu] Click vào màn ASP từ favourite menu bị lỗi 404 | HanhNTB | Ngô Thúy Ngần | Bug KH | 06.2026 |
| [#36986](https://redmine.watermelon.vn/issues/36986) | New |  | [JOB] Callback webhook bỏ logic query bot để check có tồn tại bot. Giả | ThanhNTP | Thanh Duy Nguyen | SpecImprove | 06.2026 |
| [#36940](https://redmine.watermelon.vn/issues/36940) | New | ⭐ | [Limit] Litmit tạo theo plan | CucDTK | Kieu Son Tung | Bug tự detect | 06.2026 |
| [#36913](https://redmine.watermelon.vn/issues/36913) | New |  | [JOB] Job recover hàng ngày đánh giá lại chuyển sang 1h chạy 1 lần | CucDTK | Thanh Duy Nguyen | SpecImprove | 06.2026 |
| [#36729](https://redmine.watermelon.vn/issues/36729) | New |  | [25-05-2026][11020][Lesson] Lesson: 「キャンセル用URL」 hiện 'đã hủy' nhưng th | ThanhNTP | Kieu Son Tung | Bug KH | 06.2026 |
| [#36493](https://redmine.watermelon.vn/issues/36493) | New |  | [Job] Job get tổng message của bot UpdateLimitMessageLOA | HanhNTB | Thanh Duy Nguyen | SpecImprove | 06.2026 |
| [#36836](https://redmine.watermelon.vn/issues/36836) | Fix done - Đợi test |  | [27-05-2026][QR Landing] Yêu cầu cho đổi tên file / chỉ định nơi lưu t | AnhPTN | Do Van Tu TuDV | SpecImprove | 05.2026 |
| [#36794](https://redmine.watermelon.vn/issues/36794) | New |  | Case bot_contract đã bị xóa, đang không thực hiện refund được | AnhPTN | Ngọc Ánh | Bug Tester | 05.2026 |
| [#36764](https://redmine.watermelon.vn/issues/36764) | New |  | [25-05-2026][11031] Email xác thực (認証メール) khi đăng nhập không gửi đến | CucDTK | Kieu Son Tung | Bug KH | 05.2026 |
| [#36694](https://redmine.watermelon.vn/issues/36694) | New | ⭐ | Mặc dù đã chọn bot rồi nhưng khi access tool vẫn bị vào màn hình chọn | AnhPTN | Ngọc Ánh | Bug tự detect | 05.2026 |
| [#36443](https://redmine.watermelon.vn/issues/36443) | New |  | [15-05-2026][10926][App + API app] [Item] Decision Univapay lỗi — màn | ThanhNTP | AI LME CSS | Bug KH | 05.2026 |
| [#36437](https://redmine.watermelon.vn/issues/36437) | Fix done - Đợi test |  | Khi bật xác thực 2 lớp, logout -> login lại, đang chưa select bot đã c | AnhPTN | Ngọc Ánh | Bug Tester | 05.2026 |
| [#36428](https://redmine.watermelon.vn/issues/36428) | New |  | [15-05-2026][回答ID：28184][Form] Form "初回アンケート" hiển thị "0 người trả lờ | CucDTK | Kieu Son Tung | Bug KH | 05.2026 |
| [#36384](https://redmine.watermelon.vn/issues/36384) | New |  | [12-05-2026][10884][Template] Click vào template folder '定期配信用' (Định | ThanhNTP | AI LME CSS | Bug KH | 05.2026 |
| [#36373](https://redmine.watermelon.vn/issues/36373) | New |  | [12-05-2026][10880][Bill tiền tool] Đã 接続解除 (ngắt kết nối) 2026/04/08 | AnhPTN | Kieu Son Tung | Bug KH | 05.2026 |
| [#36322](https://redmine.watermelon.vn/issues/36322) | New |  | [JOB] Bug tự detect: Backup bot step_message lỗi case start_time >= 24 | ThanhNTP | Thanh Duy Nguyen | Bug Tester | 05.2026 |
| [#36203](https://redmine.watermelon.vn/issues/36203) | New |  | [01-05-2026][Khác] Panel/Button — 2 yêu cầu fix UX (panel right-side m | CucDTK | AI LME CSS | SpecImprove | 05.2026 |
| [#36111](https://redmine.watermelon.vn/issues/36111) | New |  | [28-04-2026][10726][App + API app] App LME mobile không nhận notificat | CucDTK | AI LME CSS | Bug KH | 04.2026 |
| [#35992](https://redmine.watermelon.vn/issues/35992) | New |  | [21-04-2026] [10685] [Item] Mua item bị hiển thị lỗi hết kho 在庫が無いので、購 | ThanhNTP | Thanh Phương | Bug KH | 04.2026 |
| [#35989](https://redmine.watermelon.vn/issues/35989) | New |  | Viết job recover lại data cũ của modal action | CucDTK | Kieu Son Tung | Bug Tester | 04.2026 |
| [#35839](https://redmine.watermelon.vn/issues/35839) | New |  | [Form answer] [Sync google] Bug tự detect: Header ko đúng format thì s | ThanhNTP | Thanh Duy Nguyen | Bug Tester | 04.2026 |
| [#35793](https://redmine.watermelon.vn/issues/35793) | New |  | [10-04-2026][OEM][Admin] Fix feedback liên quan đến màn admin | AnhPTN | Nguyen Ngoc Hai | Bug KH | 04.2026 |
| [#35650](https://redmine.watermelon.vn/issues/35650) | New |  | Bill max friend bill bằng phương thức chuyển khoản | ThanhNTP | Do Van Tu TuDV | Bug Tester | 04.2026 |
| [#35523](https://redmine.watermelon.vn/issues/35523) | New |  | Improve autoRefreshToken bot push message | HanhNTB | Nga Vũ Thị | SpecImprove | 04.2026 |
| [#35389](https://redmine.watermelon.vn/issues/35389) | New |  | Sửa khi send message ko update last message và last time send, Chỉ upd | ThanhNTP | Thanh Duy Nguyen | SpecImprove | 04.2026 |
| [#35316](https://redmine.watermelon.vn/issues/35316) | New |  | [23-03-2026][10390]Admin không hiển thị 4 số cuối của thẻ | AnhPTN | Do Van Tu TuDV | SpecImprove | 04.2026 |
| [#35253](https://redmine.watermelon.vn/issues/35253) | Re-open |  | [19-03-2026][OEM][Send all - test preview] Xóa dòng trắng thừa | AnhPTN |  | SpecImprove | 04.2026 |
| [#34703](https://redmine.watermelon.vn/issues/34703) | Đang fix |  | [02-03-2026] [OEM] [Form] Khi xóa result trả lời form thì cũng xóa bản | ThanhNTP | Do Van Tu TuDV | SpecImprove | 04.2026 |
| [#33647](https://redmine.watermelon.vn/issues/33647) | New |  | [Job] Chuyển job sync câu trả lời của form answer lên google sheet san | ThanhNTP | Toan Nguyen | SpecImprove | 04.2026 |
| [#32210](https://redmine.watermelon.vn/issues/32210) | New |  | [JOB] Bug tự detect: ExportCsv: Improve friend info | CucDTK | Thanh Duy Nguyen | SpecImprove | 04.2026 |
| [#35227](https://redmine.watermelon.vn/issues/35227) | New |  | [CrossAnalysis] Xóa cross analysic item cũ giữ lại item có created_at | HanhNTB | Văn Dũng Đinh | SpecImprove | 03.2026 |
| [#35140](https://redmine.watermelon.vn/issues/35140) | New |  | [Talk list] Improve /ajax/get-talk-list-v2 | ThanhNTP | Nga Vũ Thị | SpecImprove | 03.2026 |
| [#35071](https://redmine.watermelon.vn/issues/35071) | New |  | [16-03-2026] [10308] [Friendlist] Chạy action từ friend list không đượ | ThanhNTP | Do Van Tu TuDV | Bug KH | 03.2026 |
| [#34735](https://redmine.watermelon.vn/issues/34735) | New |  | [Job] [Callback] Improve logic save callback sử dụng thread riêng khôn | NganNT | Thanh Duy Nguyen | SpecImprove | 03.2026 |
| [#33838](https://redmine.watermelon.vn/issues/33838) | New |  | [Job] Chuyển job scan campain + tutorial sang java | AnhPTN | Toan Nguyen | SpecImprove | 03.2026 |
| [#33649](https://redmine.watermelon.vn/issues/33649) | New |  | [Job] Job recover hàng ngày Booking event => count số friend booking | ThanhNTP | Toan Nguyen | SpecImprove | 03.2026 |
| [#33322](https://redmine.watermelon.vn/issues/33322) | New |  | [Action lúc unblock] Trigger hiển thị sai text | HanhNTB | Do Van Tu TuDV | Bug Tester | 03.2026 |
| [#33292](https://redmine.watermelon.vn/issues/33292) | New |  | [Improve] Job mapping device cho landingQR | CucDTK | Toan Nguyen | SpecImprove | 03.2026 |
| [#34533](https://redmine.watermelon.vn/issues/34533) | New |  | Improve performance mở link bill item check kết bạn old friend | ThanhNTP | Thanh Phương | SpecImprove | 02.2026 |
| [#34185](https://redmine.watermelon.vn/issues/34185) | New | ⭐ | [Salon] Bug tự detect Undefined index: end_time | QuyenD | Kieu Son Tung | Bug tự detect | 02.2026 |
| [#33309](https://redmine.watermelon.vn/issues/33309) | New | ⭐ | [QL CSV][Exception] Import csv có setting action friend_info date dạng | QuyenD | Thanh Duy Nguyen | Bug tự detect | 02.2026 |
| [#34055](https://redmine.watermelon.vn/issues/34055) | New | ⭐ | [ASP] Lỗi màn hình ASP aff-money | QuyenD | Do Van Tu TuDV | Bug tự detect | 01.2026 |
| [#33970](https://redmine.watermelon.vn/issues/33970) | New | ⭐ | [Image richmenu] copy image richmenu không copy được ảnh con bên trong | ThanhNTP | Thanh Phương | Bug tự detect | 01.2026 |
| [#33697](https://redmine.watermelon.vn/issues/33697) | New |  | [Friend info]  Validate nếu nhập option value giống nhau thì báo lỗi | CucDTK | Kim Cúc | Triển khai ngang | 01.2026 |
| [#32786](https://redmine.watermelon.vn/issues/32786) | New |  | [11-11-2025][OEM] Về điều kiện hiển thị dòng chữ 「外部サイトに移動したため」( “Đã c | QuyenD | Do Van Tu TuDV | Support | 01.2026 |

## 🟡 Nhóm 2 — Đang chờ KH (thường vẫn để open) (22)

| Redmine ID | Trạng thái | ⭐26684 | Tiêu đề | Tester (sheet) | Assignee (Redmine) | Tracker | Tháng checklist |
|---|---|:--:|---|---|---|---|---|
| [#38447](https://redmine.watermelon.vn/issues/38447) | KH Feedback |  | [03-07-2026][T11463][Chat 1:1] Tin nhắn từ phía đối tác không được phả | ThanhNTP |  | Bug KH | 07.2026 |
| [#38280](https://redmine.watermelon.vn/issues/38280) | KH Feedback |  | [29-06-2026][28719][Lesson] Đặt giới hạn 1 khung/ngày cho đặt lịch học | ThanhNTP | Ngô Thúy Ngần | Bug KH | 07.2026 |
| [#37931](https://redmine.watermelon.vn/issues/37931) | KH Feedback |  | [19-06-2026][No.11297][QR Landing] QRCA parameter export (パラメーターエクスポート | CucDTK | Do Van Tu TuDV | Bug KH | 06.2026 |
| [#36859](https://redmine.watermelon.vn/issues/36859) | KH Feedback |  | [29-05-2026][11073][Chat 1:1] Lịch sử chat 1:1 của friend 「鈴音」 hiển th | ThanhNTP | Kieu Son Tung | Bug KH | 06.2026 |
| [#36835](https://redmine.watermelon.vn/issues/36835) | KH Feedback |  | [28-05-2026][28312][Bill tiền tool] Status chuyển khoản NH đang là "Ch | CucDTK | Kieu Son Tung | Bug KH | 06.2026 |
| [#36107](https://redmine.watermelon.vn/issues/36107) | Released - đợi KH close |  | [27-04-2026][10740][Phân quyền] Staff management: Support permission b | CucDTK | Kieu Son Tung | Bug KH | 04.2026 |
| [#35961](https://redmine.watermelon.vn/issues/35961) | Released - đợi KH close |  | [17-04-2026][27816][Error message] LOA đang là gói standard nhưng xuất | ThanhNTP | Thanh Duy Nguyen | Bug KH | 04.2026 |
| [#35845](https://redmine.watermelon.vn/issues/35845) | Đợi KH confirm |  | [14-04-2026][27769]Đã hủy gói standard nhưng vẫn thực hiện thanh toán | AnhPTN | Nguyen Ngoc Hai | Bug KH | 04.2026 |
| [#35810](https://redmine.watermelon.vn/issues/35810) | Đợi KH confirm |  | [13-04-2026] [10605] Setting notify của form tự nhiên bị OFF | HanhNTB | Nga Vũ Thị | Bug KH | 04.2026 |
| [#35635](https://redmine.watermelon.vn/issues/35635) | Released - đợi KH close |  | [04-04-2026] [10519] [Bill tool] Hợp đồng hiển thị bị cưỡng chế hủy nh | AnhPTN, ThanhNTP | Do Van Tu TuDV | Bug KH | 04.2026 |
| [#35506](https://redmine.watermelon.vn/issues/35506) | Đợi KH confirm |  | [01-04-2026][OEM]Khi click vào số lượng gửi trong lịch sử gửi tin nhắn | AnhPTN | Kieu Son Tung | Bug KH | 04.2026 |
| [#34991](https://redmine.watermelon.vn/issues/34991) | Đợi KH confirm |  | [13-03-2026][10292][Form] Khi tạo form dạng phân nhánh, trên Google Sh | ThanhNTP | Thanh Phương | Bug KH | 03.2026 |
| [#34625](https://redmine.watermelon.vn/issues/34625) | Released - đợi KH close |  | [26-02-2026][10113][Friend infor] Khi copy thông tin friend xảy ra lỗi | CucDTK | Kieu Son Tung | Bug KH | 03.2026 |
| [#34561](https://redmine.watermelon.vn/issues/34561) | Released - đợi KH close |  | [25-02-2026][10050][Lession]Tại màn hình cài đặt chi tiết khóa học và | ThanhNTP | Kieu Son Tung | Bug KH | 03.2026 |
| [#34521](https://redmine.watermelon.vn/issues/34521) | Released - đợi KH close |  | [24-02-2026][9984]Gói standard plan 2 năm chưa hết hạn nhưng hiện tại | CucDTK, HanhNTB | Do Van Tu TuDV | Bug KH | 03.2026 |
| [#34489](https://redmine.watermelon.vn/issues/34489) | Released - đợi KH close |  | [21-02-2026] [10047] [Scenario] Send test nhưng thứ tự gửi msg không đ | ThanhNTP | Kieu Son Tung | Bug KH | 03.2026 |
| [#34414](https://redmine.watermelon.vn/issues/34414) | Released - đợi KH close |  | [11-02-2026][OEM][Form] Về thao tác “Liên kết thông tin trả lời”, tron | CucDTK | Do Van Tu TuDV | SpecImprove | 03.2026 |
| [#34622](https://redmine.watermelon.vn/issues/34622) | Released - đợi KH close |  | [26-02-2026][10105]Hợp đồng 2 năm từ 4/3/2024 chưa hết hạn nhưng lại ở | HanhNTB | Do Van Tu TuDV | Bug KH | 02.2026 |
| [#34475](https://redmine.watermelon.vn/issues/34475) | Released - đợi KH close |  | [13-02-2026] [9951] [QR code] Thông tin đã đăng ký không được convert | CucDTK | Do Van Tu TuDV | Bug KH | 02.2026 |
| [#34311](https://redmine.watermelon.vn/issues/34311) | Released - đợi KH close |  | [09-02-2026] [9888] Vào Chat 1:1 bị trắng màn hình | ThanhNTP | Kieu Son Tung | Bug KH | 02.2026 |
| [#33245](https://redmine.watermelon.vn/issues/33245) | KH Feedback |  | [19-12-2025] [9348] [Form] Không chạy action remind | NganNT, ThanhNTP | Kieu Son Tung | SpecImprove | 01.2026, 02.2026 |
| [#32567](https://redmine.watermelon.vn/issues/32567) | Đợi KH confirm |  | [25-10-2025] [8598] [Salon] Booking request không hiển thị thông tin f | ThanhNTP | Kieu Son Tung | Bug KH | 01.2026 |

---

### Ghi chú phương pháp
- Bug-ID lấy từ cột **"Bug"** của mỗi dòng checklist (pattern `#NNNNN` đầu tiên — các số trong `[...]` như 回答ID/ticket KH bị bỏ qua vì không có tiền tố `#`).
- "Đã Closed" = trạng thái Redmine ∈ {`Closed`, `Closed của re-open`}. Mọi trạng thái khác coi là còn open.
- Checklist bao phủ **250 bug** thuộc nhiều tracker (Bug KH / Bug Tester / Bug tự detect / Support / SpecImprove / Feature / Triển khai ngang) — **rộng hơn** parent #26684 (chỉ 35/250 ID là con của #26684). Đã kiểm tra trạng thái cho **cả 250 ID**, không chỉ 35 con của #26684.