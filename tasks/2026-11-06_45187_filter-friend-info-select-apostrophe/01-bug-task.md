# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45187 — [JOB][Filter][Info friend] SQLGrammarException khi option của friend info dạng select chứa dấu nháy đơn (') — LineUserModel build IN ('...') bằng nối chuỗi` |
| Module / Màn hình | Job lọc bạn bè FilterV2 (`LineUserModel.buildWhereFilter` / `buildWhereORFilter`) — dùng chung cho 一斉配信 (broadcast), アクション予約 (action schedule), Step kịch bản, 自動応答 (auto-reply), Postback action, リッチメニュー toggle, イベント リマインド, CSV管理 (export CSV), クロス分析 (cross analysis) |

## Mô tả bug (bản dịch tiếng Việt)

Job lọc bạn bè (FilterV2) bị crash khi friend info dạng *select* có option chứa dấu nháy đơn ('), ví dụ `⑧Farmer's Chicken札幌山鼻店`. Mọi broadcast / scenario / action dùng filter này đều không chạy được cho bot đó.

Log production ngày 2026-11-05 (bot 323, filter 150310, user 48928):

```
2026-11-05 11:21:23 INFO  LineUserModel:2145 - #isValidFilterV2: type modal_action - parentFilterId 150310 - sqlString SELECT line_user.* FROM line_user INNER JOIN bot_line_user ON bot_line_user.line_user_id = line_user.id WHERE  bot_line_user.line_user_id = ? AND bot_line_user.bot_id = ? AND bot_line_user.is_blocked = 0 AND (SELECT count(*) from friend_information_value WHERE friend_information_value.bot_id = bot_line_user.bot_id AND friend_information_value.line_id = bot_line_user.line_user_id AND friend_information_value.value IN ('⑧ -','⑧Farmer's Chicken札幌山鼻店')  AND friend_information_value.friend_information_setting_id = 5846)>0 GROUP BY line_user.id ==> 48928,323
2026-11-05 11:21:23 ERROR LineUserModel:2153 - javax.persistence.PersistenceException: org.hibernate.exception.SQLGrammarException: could not extract ResultSet
```

Nguyên nhân (chi tiết kỹ thuật đầy đủ ở [03-dev-impact.md](03-dev-impact.md) mục 1): trong `src/main/java/sns/line/models/LineUserModel.java`, mệnh đề `IN (...)` cho friend info select và cho tỉnh (province) được build bằng cách **nối thẳng giá trị vào chuỗi SQL** (`IN ('" + String.join("','", selectOpList) + "') `) thay vì bind qua placeholder `?`. Giá trị option do khách hàng tự nhập, chứa `'` → câu SQL gãy cú pháp → `SQLGrammarException`. Đây cũng đồng thời là lỗ **SQL injection** vì giá trị không được bind. Các vị trí bị ảnh hưởng (branch `staging-t10-2026`, commit `0475e7081`):
- `buildWhereFilter` (AND): `friend_information_value.value IN` — line 1021, 1024; `line_user.province IN` / `NOT IN` — line 965, 967
- `buildWhereORFilter` (OR): `friend_information_value.value IN` — line 1846, 1849; `line_user.province IN` / `NOT IN` — line 1790, 1792

## Steps to reproduce

(theo Journal #152030 — Đỗ Quyên, 2026-11-06)

1. Tạo 1 friend info type **select** với 3 option: `⑧ -` · `⑧Farmer's Chicken札幌山鼻店` · `TC45187_普通`.
2. Gán thông tin cho 3 friend: Friend 1 = `⑧Farmer's Chicken札幌山鼻店`; Friend 2 = `TC45187_普通`; Friend 3 = không chọn.
3. Màn 友だちリスト (friend list): Filter theo friend info trên, chọn option 1 (`⑧ -`) + option 2 (`⑧Farmer's Chicken札幌山鼻店`) → preview web ra Friend 1 thỏa mãn.
4. Tạo broadcast (一斉配信 — send job) với điều kiện filter theo friend info như bước 3 → hiển thị 1 người.
5. Chờ job gửi (send).

## Expected result

- Job filter chạy được, gửi tin thành công cho friend thỏa mãn điều kiện filter (1 người khớp option chứa dấu `'`).

## Actual result

- Không gửi được. Job FilterV2 crash với `SQLGrammarException` khi build mệnh đề `IN (...)` có option chứa dấu nháy đơn `'`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log production chép nguyên văn ở trên (không phải attachment Redmine, Redmine issue này không có attachment nào — `Attachments (0)`).

## Ghi chú thêm của Leader

- Môi trường phát hiện: **Production** (bot 323, filter 150310, line_user_id 48928), thời điểm lỗi 2026-11-05 11:21:23.
- Bug KHÔNG chỉ là crash mà còn là lỗ hổng **SQL injection** (giá trị option không được bind tham số).
- Branch fix: `ai_studio_fixbug_45187` (service `java-job`, gốc `release-t09-2026` @`a3ce3af2d76b`, commit `75f5c82380d31ee57c22af1f71fd2618d14c22f4`).
- Theo quyết định DungDV (2026-11-05): **KHÔNG recover data**, **KHÔNG lập danh sách bot bị ảnh hưởng** — chỉ sửa code. Tin LINE đã gửi thừa trước đây (do hành vi lỗi cũ: job trả `true`/gửi cho người không khớp filter khi query lỗi) **KHÔNG thu hồi được**.
- ⚠️ **Module web (php-web, `app/Conversation.php` khoảng dòng 781)** build `IN` cho friend info select bằng cách ghép chuỗi trong dấu nháy **kép** (`"`) — sẽ lỗi khi option chứa dấu `"`. Đây là bug riêng, **ngoài phạm vi ticket này**, Dev đề nghị tách ticket riêng cho module web.
- ⚠️ **Module callback** dùng chung file `LineUserModel.java` — **chưa được sửa trong deploy này**, chỉ được sửa sau khi cherry-pick commit `75f5c8238` sang nhánh `release-callback-t09-2026` riêng (không merge cả nhánh task vì nhánh job đi trước callback 37 commit).
- Hành vi lỗi cũ **GIỮ NGUYÊN, không đổi trong ticket này** (ghi rõ trong Journal #151339): `isValidFilterV2` trả `true` khi query lỗi → tin/action vẫn chạy cho người không khớp filter; `getListLineUserFromFilterV2` trả list rỗng khi lỗi. Dev đề xuất cải tiến hành vi an toàn hơn ở ticket khác.
- Branch base `release-t09-2026` hiện thiếu dependency `com.squareup.retrofit2:converter-jackson` trong `build.gradle` → `compileJava` hay lỗi; đội release cần kiểm tra (không thuộc phạm vi task này).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `323` |
| Friend | `line_user_id 48928` |
| Đối tượng cấu hình | `friend_information_setting_id 5846` (filter `parentFilterId 150310`, option chứa dấu `'`: `⑧Farmer's Chicken札幌山鼻店`) |
| Thời điểm lỗi | `2026-11-05 11:21:23` |
| Đối chứng | Không có case đối chứng chạy đúng nêu trong ticket — mọi filter có option chứa dấu `'` đều crash như nhau trước khi fix |

## Journal / note từ Redmine (nguyên văn)

**Journal #151323 — Dev Studio — 2026-11-05:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Trong LineUserModel, hai hàm dựng điều kiện lọc (AND: buildWhereFilter, OR: buildWhereORFilter) tạo mệnh đề IN cho friend info dạng select và cho tỉnh bằng cách ghép thẳng giá trị option vào SQL trong dấu nháy đơn. Option do khách tự nhập có dấu ' (ví dụ ⑧Farmer's Chicken札幌山鼻店) làm câu SQL sai cú pháp, MySQL báo SQLGrammarException. Các nhánh khác trong hai hàm này đã bind tham số qua ?, chỉ 8 chỗ IN này ghép chuỗi (đồng thời là lỗ SQL injection).

Hướng sửa:
- D-1 Thêm helper buildInPlaceholders trong LineUserModel
- D-2 Thay 8 chỗ ghép chuỗi IN bằng placeholder đã bind
- D-3 Unit test không chạm DB cho mệnh đề IN

Ảnh hưởng / rủi ro:
Sửa dùng chung cho mọi luồng lọc FilterV2 của job (broadcast, action, action schedule, step kịch bản, nhắc lịch event, auto-reply, rich menu, export CSV, cross analysis); kết quả lọc không đổi với option thường, option có dấu ' hết lỗi. Rủi ro chính là lệch thứ tự tham số khi trộn AND + OR nhiều option, cần test riêng.
```

**Journal #151339 — Dev Studio — 2026-11-05:**

```
Dev handoff — 05/11 14:07 · nhánh ai_studio_fixbug_45187

Nguyên nhân:
Trong LineUserModel, hai hàm dựng điều kiện lọc (AND: buildWhereFilter, OR: buildWhereORFilter) tạo mệnh đề IN cho friend info dạng select và cho tỉnh bằng cách ghép thẳng giá trị option vào SQL trong dấu nháy đơn. Option do khách tự nhập có dấu ' (ví dụ ⑧Farmer's Chicken札幌山鼻店) làm câu SQL sai cú pháp, MySQL báo SQLGrammarException. Các nhánh khác trong hai hàm này đã bind tham số qua ?, chỉ 8 chỗ IN này ghép chuỗi (đồng thời là lỗ SQL injection).

Nội dung thay đổi:
- Job FilterV2 (dùng chung cho broadcast, action, action schedule, kịch bản, nhắc lịch event, auto-reply/postback/rich menu, export CSV, cross analysis): điều kiện friend info dạng select (含む / 含まない) không còn crash khi option chứa dấu nháy đơn.
- Điều kiện tỉnh (province) thuộc / không thuộc: giá trị được bind tham số; 'không thuộc' vẫn gồm người chưa có tỉnh.
- Log #isValidFilterV2 / #getListLineUserFromFilterV2 nay in IN (?,?) và các option nằm trong danh sách args sau ==>.

File đã sửa (java-job):
  src/main/java/sns/line/models/LineUserModel.java   |  26 ++--
  .../models/LineUserModelFilterInClauseTest.java    | 139 +++++++++++++++++++++
  2 files changed, 157 insertions(+), 8 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Thay đổi cục bộ ở 8 mệnh đề IN, theo đúng pattern bind đã có sẵn trong file; thứ tự tham số đã kiểm bằng unit test và harness AND + OR. Chưa verify runtime với DB thật.
- LineUserModel.isValidFilterV2 (kiểm từng user): action, step kịch bản, auto-reply, action postback, rich menu toggle, nhắc lịch event.
- LineUserModel.getListLineUserFromFilterV2 (lấy danh sách): broadcast, action schedule, export CSV, cross analysis, FilterService.
- Filter trộn AND + OR có thêm điều kiện = ? / LIKE ?: mọi điều kiện dùng chung một danh sách tham số, nên phải kiểm thứ tự.
- Module callback dùng cùng file LineUserModel.java: chỉ được sửa sau khi cherry-pick commit.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — DungDV quyết định ngày 2026-11-05: chỉ sửa code, không recover và không lập danh sách bot bị ảnh hưởng. Tin LINE đã gửi thừa cũng không thu hồi được.

Lưu ý khi deploy:
- Module callback: cherry-pick riêng commit 75f5c8238 sang release-callback-t09-2026 (áp sạch); không merge cả nhánh task.

Việc cần người làm thêm (ngoài phạm vi task):
- Đưa bản sửa sang nhánh release-callback-t09-2026 (DungDV sẽ làm): nên cherry-pick đúng commit sửa vì release-t09-2026 đang hơn nhánh callback 37 commit; file LineUserModel.java hai bên giống hệt nên áp sạch.
- Web (php-web, app/Conversation.php khoảng dòng 781) dựng IN cho friend info select bằng cách ghép trong dấu nháy kép, nên sẽ lỗi khi option có dấu ": cần ticket riêng cho module web.
- Cân nhắc ticket riêng: isValidFilterV2 trả true khi query lỗi khiến tin/action chạy cho người không khớp filter; nên xem lại hành vi an toàn hơn.
- Nhánh base đang thiếu dependency com.squareup.retrofit2:converter-jackson trong build.gradle nên lệnh compileJava thường bị lỗi. Đội release nên kiểm tra lại.
- Các builder FilterV2 vẫn nối thẳng infoSearch (id setting), point và lineId vào SQL. Hiện chưa gây lỗi, nhưng nên mở việc riêng để bind nốt.

Điểm cần test:
- Friend info select có option chứa dấu ' (vd ⑧Farmer's Chicken札幌山鼻店), chọn 含む và 含まない: không còn SQLGrammarException, log in IN (?,?) và args có các option, số người khớp số preview trên web.
- Option chứa ", \, %, _, ?, tiếng Nhật: so khớp đúng nguyên văn.
- Province thuộc / không thuộc nhiều tỉnh: NOT IN vẫn gồm người chưa có tỉnh.
- Filter trộn AND + OR, nhiều option cùng điều kiện = ? / LIKE ?: tham số không lệch thứ tự.
- Luồng lấy danh sách (broadcast, export CSV, cross analysis) và luồng kiểm từng người (action, step kịch bản, auto-reply) đều cho kết quả đúng.
- Filter không dùng option select/province: SQL và kết quả như trước.

Branch: ai_studio_fixbug_45187
- linect-service: ai_studio_fixbug_45187 (nhánh gốc release-t09-2026 @a3ce3af2d76b, commit 75f5c82380d31ee57c22af1f71fd2618d14c22f4)
```

**Journal #152030 — Đỗ Quyên — 2026-11-06:**

```
Tái hiện:
1. Tạo 1 friend infor type select:
Option 1	⑧ -
Option 2	⑧Farmer's Chicken札幌山鼻店
Option 3	TC45187_普通

2. Gán thông tin cho friend
Friend 1: ⑧Farmer's Chicken札幌山鼻店
Friend 2: TC45187_普通
Friend 3: Không chọn

3. MH friend list: Filter theo friend infor trên, chọn option 1+2
=> Sẽ ra friend 1 thỏa mãn

4. Tạo broadcase (send job) với đk filter theo friend infor như Bước 3. => hiển thị 1ng
5. Chờ send

Hiện tại: ko send được
Expect: send success cho friend thỏa mãn
```
