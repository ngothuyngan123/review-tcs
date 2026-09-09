<!-- sync-target: https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=898638988#gid=898638988 -->
# 04 — TC List (do member viết)

> File này là **output của member**, **input của Leader**.
> ⚠️ **Nguồn:** fetch read-only từ Redmine #35968 Link TCs, tab `#35968` (gid 898638988) — KHÔNG có `Row:` range trong Redmine nên fetch toàn bộ tab.
> ⚠️ **Lưu ý format:** Sheet gốc dùng format phân cấp cũ (Main Function → Sub1..6 → Expect Result → Status), KHÔNG phải 10 cột chuẩn team. Đã reconstruct mỗi leaf-row thành 1 TC, forward-fill ô merge, **giữ NGUYÊN giá trị cell** (kể cả lỗi chính tả gốc, vd "Tag B", "scen B" ở màn Form/Cross). Cột Type / Priority / Output note / Assignee để trống (Sheet gốc không có) — member/Leader bổ sung. Cột Status lấy verbatim từ Sheet (đa số đã pass Staging).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `v1` (fetch từ Sheet) |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=898638988#gid=898638988 (tab `#35968`) |

---

## TC List

> Bảng TC dùng **10 cột chuẩn team**. Khi `/sync-tc` push lên Google Sheet master, cột Status sẽ có dropdown 4 giá trị: `OK` / `NG` / `Not test` / `NG -> Đã fix`.

### 1) Màn Message Template (Status verbatim: OK Staging)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | [Template] Sort Template — click Template vừa sort (vị trí đầu) | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Click vào Template vừa sort (Template A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng Template xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK Staging |
| TC002 | [Template] Sort Template — click Template ở vị trí số 3 | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Click vào Template ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Template xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC003 | [Template] Sort Template — click Template cuối cùng | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Click vào Template cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC004 | [Template] Sort Template — kéo xuống vị trí số 2, click Template vừa sort | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Kéo Template xuống vị trí số 2<br>3. Click vào Template vừa sort (Template A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC005 | [Template] Sort Template — kéo xuống vị trí số 2, click Template cuối cùng | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Kéo Template xuống vị trí số 2<br>3. Click vào Template cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC006 | [Template] Sort Template — kéo A về vị trí số 1, click Template A | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên<br>2. Kéo Template xuống vị trí số 2<br>3. Kéo Template A về vị trí số 1<br>4. Click vào Template A (Template sort từ dưới lên — Template A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC007 | [Template] Sort Template — click Template B (vị trí số 2) | | | Check khi có 6 Template | (tiếp TC006) Click vào Template B (Template vừa được đảo lộn vị trí với Template A — Template B đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Template xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC008 | [Template] Sort Template — click Template C (vị trí số 3) | | | Check khi có 6 Template | (tiếp TC006) Click vào Template C (Template sort từ dưới lên — Template C đang ở vị trí số 3) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Template xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC009 | [Template] Sort Template — click Template cuối cùng (sau đảo vị trí) | | | Check khi có 6 Template | (tiếp TC006) Click vào Template cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC010 | [Template] Sort Template — kéo vào vị trí số 2, click Template vừa sort | | | Check khi có 6 Template | 1. Kéo Template từ dưới lên vào vị trí số 2<br>2. Click vào Template vừa sort (Template A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Template xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC011 | [Template] Sort Template — click Template ở vị trí số 3 (sau kéo vào vị trí 2) | | | Check khi có 6 Template | (tiếp TC010) Click vào Template ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Template xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC012 | [Template] Sort Template — click Template cuối cùng (sau kéo vào vị trí 2) | | | Check khi có 6 Template | (tiếp TC010) Click vào Template cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC013 | [Template] Sort Template — thao tác liên tục, save list đã sort | | | Check khi có 6 Template | Check thao tác liên tục: save lại list Template đã sort | - Sau khi save hiển thị Template về vị trí mong muốn | | | OK Staging |
| TC014 | [Template] Sort Template — tạo mới Template | | | Check khi có 6 Template | Check thao tác liên tục: Tạo mới Template | - tạo mới Template thành công<br>- hiển thị Template vị trí đầu tiên | | | OK Staging |
| TC015 | [Template] Sort Template — khi có 4 Template | | | Check khi có 4 Template | Thực hiện sort Template | (theo chuẩn sort) | | | OK Staging |
| TC016 | [Template] Sort Template — khi có 10 Template | | | Check khi có 10 Template | Thực hiện sort Template | (theo chuẩn sort) | | | OK Staging |
| TC017 | [Template] Sort Template — khi có phân trang | | | Check sort khi có phân trang | Thực hiện sort Template khi list có phân trang | (theo chuẩn sort) | | | OK Staging |
| TC018 | [Template] Sort Template — search theo tên rồi sort | | | — | Search theo tên Template → Nhấn sort Template | (theo chuẩn sort) | | | OK Staging |
| TC019 | [Template] Sort Template — sort cột 作成日 rồi mở modal sort | | | — | Nhấn sort theo cột 作成日 → nhấn tiếp nút sort Template 並べ替え | - Khi click sort ở màn list => thực hiện lấy theo default sort theo positon => click mở modal sort thì clear data về default ( tức sort theo positon ) | | | OK Staging |
| TC020 | [Template] Sort Template — sort cột 最終編集日 rồi mở modal sort | | | — | Nhấn sort theo cột 最終編集日 → nhấn tiếp nút sort Template 並べ替え | (theo chuẩn sort) | | | OK Staging |
| TC021 | [Template] Sort Template — sort cột 管理名 rồi mở modal sort | | | — | Nhấn sort theo cột 管理名 → nhấn tiếp vào modal sort Template 並べ替え | (theo chuẩn sort) | | | OK Staging |
| TC022 | [Template] Sort folder — click folder vừa sort (vị trí đầu) | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder vừa sort (folder A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng folder xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK Staging |
| TC023 | [Template] Sort folder — click folder ở vị trí số 3 | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC024 | [Template] Sort folder — click folder cuối cùng | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng folder lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC025 | [Template] Sort folder — kéo xuống vị trí số 2, click vừa sort | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Kéo folder xuống vị trí số 2<br>3. Click vào Template vừa sort (Template A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK Staging |
| TC026 | [Template] Sort folder — click folder cuối cùng (sau kéo vị trí 2) | | | Check khi có 6 folder | (tiếp TC025) Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút folder đúng Template lên thành công<br>- Disable nút sort xuống | | | OK Staging |
| TC027 | [Template] Sort folder — thao tác liên tục, save list folder | | | Check khi có 6 folder | Check thao tác liên tục: save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | OK Staging |
| TC028 | [Template] Sort folder — tạo mới folder | | | Check khi có 6 folder | Check thao tác liên tục: Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | OK Staging |
| TC029 | [Template] Check account staff | | | — | Check account staff (sort Template/folder với account staff) | (theo chuẩn) | | | OK Staging |

### 2) Màn QR Landing (Status verbatim: Done staging)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC030 | [QR] Sort QR — click QR vừa sort (vị trí đầu) | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên<br>2. Click vào QR vừa sort (QR A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng QR xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | Done staging |
| TC031 | [QR] Sort QR — click QR ở vị trí số 3 | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên<br>2. Click vào QR ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng QR xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC032 | [QR] Sort QR — click QR cuối cùng | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên<br>2. Click vào QR cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC033 | [QR] Sort QR — kéo xuống vị trí số 2, click QR vừa sort | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên<br>2. Kéo QR xuống vị trí số 2<br>3. Click vào QR vừa sort (QR A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC034 | [QR] Sort QR — kéo xuống vị trí số 2, click QR cuối cùng | | | Check khi có 6 QR | (tiếp TC033) Click vào QR cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC035 | [QR] Sort QR — kéo A về vị trí số 1, click QR A | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên<br>2. Kéo QR xuống vị trí số 2<br>3. Kéo QR A về vị trí số 1<br>4. Click vào QR A (QR sort từ dưới lên — QR A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC036 | [QR] Sort QR — click QR B (vị trí số 2) | | | Check khi có 6 QR | (tiếp TC035) Click vào QR B (QR vừa được đảo lộn vị trí với QR A — QR B đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng QR xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC037 | [QR] Sort QR — click QR C (vị trí số 3) | | | Check khi có 6 QR | (tiếp TC035) Click vào QR C (QR sort từ dưới lên — QR C đang ở vị trí số 3) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng QR xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC038 | [QR] Sort QR — click QR cuối cùng (sau đảo vị trí) | | | Check khi có 6 QR | (tiếp TC035) Click vào QR cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC039 | [QR] Sort QR — kéo vào vị trí số 2, click QR vừa sort | | | Check khi có 6 QR | 1. Kéo QR từ dưới lên vào vị trí số 2<br>2. Click vào QR vừa sort (QR A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng QR xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC040 | [QR] Sort QR — click QR ở vị trí số 3 (sau kéo vào vị trí 2) | | | Check khi có 6 QR | (tiếp TC039) Click vào QR ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng QR xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC041 | [QR] Sort QR — click QR cuối cùng (sau kéo vào vị trí 2) | | | Check khi có 6 QR | (tiếp TC039) Click vào QR cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC042 | [QR] Sort QR — thao tác liên tục, save list đã sort | | | Check khi có 6 QR | Check thao tác liên tục: save lại list QR đã sort | - Sau khi save hiển thị QR về vị trí mong muốn | | | Done staging |
| TC043 | [QR] Sort QR — tạo mới QR | | | Check khi có 6 QR | Check thao tác liên tục: Tạo mới QR | - tạo mới QR thành công<br>- hiển thị QR vị trí đầu tiên | | | Done staging |
| TC044 | [QR] Sort QR — khi có 4 QR | | | Check khi có 4 QR | Thực hiện sort QR | (theo chuẩn sort) | | | Done staging |
| TC045 | [QR] Sort QR — khi có 10 QR | | | Check khi có 10 QR | Thực hiện sort QR | (theo chuẩn sort) | | | Done staging |
| TC046 | [QR] Sort QR — khi có phân trang | | | Check sort khi có phân trang | Thực hiện sort QR khi list có phân trang | (theo chuẩn sort) | | | Done staging |
| TC047 | [QR] Sort QR — search theo tên rồi sort | | | — | Search theo tên QR → Nhấn sort QR | (theo chuẩn sort) | | | Done staging |
| TC048 | [QR] Sort QR — sort cột 作成日 rồi mở modal sort | | | — | Nhấn sort theo cột 作成日 → nhấn tiếp nút sort QR 並べ替え | - Khi click sort ở màn list => thực hiện lấy theo default sort theo positon => click mở modal sort thì clear data về default ( tức sort theo positon ) | | | Done staging |
| TC049 | [QR] Sort QR — sort cột 最終編集日 rồi mở modal sort | | | — | Nhấn sort theo cột 最終編集日 → nhấn tiếp nút sort QR 並べ替え | (theo chuẩn sort) | | | Done staging |
| TC050 | [QR] Sort QR — sort cột 管理名 rồi mở modal sort | | | — | Nhấn sort theo cột 管理名 → nhấn tiếp vào modal sort QR 並べ替え | (theo chuẩn sort) | | | Done staging |
| TC051 | [QR] Sort folder — click folder vừa sort (vị trí đầu) | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder vừa sort (folder A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng folder xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | Done staging |
| TC052 | [QR] Sort folder — click folder ở vị trí số 3 | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC053 | [QR] Sort folder — click folder cuối cùng | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng folder lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC054 | [QR] Sort folder — kéo xuống vị trí số 2, click vừa sort | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Kéo folder xuống vị trí số 2<br>3. Click vào QR vừa sort (QR A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Done staging |
| TC055 | [QR] Sort folder — click folder cuối cùng (sau kéo vị trí 2) | | | Check khi có 6 folder | (tiếp TC054) Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút folder đúng QR lên thành công<br>- Disable nút sort xuống | | | Done staging |
| TC056 | [QR] Sort folder — thao tác liên tục, save list folder | | | Check khi có 6 folder | Check thao tác liên tục: save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | Done staging |
| TC057 | [QR] Sort folder — tạo mới folder | | | Check khi có 6 folder | Check thao tác liên tục: Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | Done staging |
| TC058 | [QR] Check account staff | | | — | Check account staff (sort QR/folder với account staff) | (theo chuẩn) | | | Done staging |

### 3) Màn Form Answer (Status verbatim: OK staging)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC059 | [Form] Sort Form — click Form vừa sort (vị trí đầu) | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên<br>2. Click vào Form vừa sort (Form A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng Form xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK staging |
| TC060 | [Form] Sort Form — click Form ở vị trí số 3 | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên<br>2. Click vào Form ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Form xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC061 | [Form] Sort Form — click Form cuối cùng | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên<br>2. Click vào Form cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC062 | [Form] Sort Form — kéo xuống vị trí số 2, click Form vừa sort | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên 2. Kéo Form xuống vị trí số 2<br>3. Click vào Form vừa sort (Form A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC063 | [Form] Sort Form — kéo xuống vị trí số 2, click Form cuối cùng | | | Check khi có 6 Form | (tiếp TC062) Click vào Form cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC064 | [Form] Sort Form — kéo A về vị trí số 1, click Form A | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên<br>2. Kéo Form xuống vị trí số 2<br>3. Kéo Form A về vị trí số 1<br>4. Click vào Form A (Form sort từ dưới lên — Form A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC065 | [Form] Sort Form — click Form B (vị trí số 2) | | | Check khi có 6 Form | (tiếp TC064) Click vào Form B (Form vừa được đảo lộn vị trí với Form A — "Tag B đang ở vị trí số 2") | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Form xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC066 | [Form] Sort Form — click Form C (vị trí số 3) | | | Check khi có 6 Form | (tiếp TC064) Click vào Form C (Form sort từ dưới lên — Form C đang ở vị trí số 3) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Form xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC067 | [Form] Sort Form — click Form cuối cùng (sau đảo vị trí) | | | Check khi có 6 Form | (tiếp TC064) Click vào Form cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC068 | [Form] Sort Form — kéo vào vị trí số 2, click Form vừa sort | | | Check khi có 6 Form | 1. Kéo Form từ dưới lên vào vị trí số 2<br>2. Click vào Form vừa sort (Form A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Form xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC069 | [Form] Sort Form — click Form ở vị trí số 3 (sau kéo vào vị trí 2) | | | Check khi có 6 Form | (tiếp TC068) Click vào Form ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Form xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC070 | [Form] Sort Form — click Form cuối cùng (sau kéo vào vị trí 2) | | | Check khi có 6 Form | (tiếp TC068) Click vào Form cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC071 | [Form] Sort Form — thao tác liên tục, save list đã sort | | | Check khi có 6 Form | Check thao tác liên tục: save lại list Form đã sort | - Sau khi save hiển thị Form về vị trí mong muốn | | | OK staging |
| TC072 | [Form] Sort Form — tạo mới Form | | | Check khi có 6 Form | Check thao tác liên tục: Tạo mới Form | - tạo mới Form thành công<br>- hiển thị Form vị trí đầu tiên | | | OK staging |
| TC073 | [Form] Sort Form — khi có 4 Form | | | Check khi có 4 Form | Thực hiện sort Form | (theo chuẩn sort) | | | OK staging |
| TC074 | [Form] Sort Form — khi có 10 Form | | | Check khi có 10 Form | Thực hiện sort Form | (theo chuẩn sort) | | | OK staging |
| TC075 | [Form] Sort Form — khi có phân trang | | | Check sort khi có phân trang | Thực hiện sort Form khi list có phân trang | (theo chuẩn sort) | | | OK staging |
| TC076 | [Form] Sort Form — search theo tên rồi sort | | | — | Search theo tên Form → Nhấn sort Form | (theo chuẩn sort) | | | OK staging |
| TC077 | [Form] Sort Form — sort cột 作成日 rồi mở modal sort | | | — | Nhấn sort theo cột 作成日 → nhấn tiếp nút sort Form 並べ替え | - Khi click sort ở màn list => thực hiện lấy theo default sort theo positon => click mở modal sort thì clear data về default ( tức sort theo positon ) | | | OK staging |
| TC078 | [Form] Sort Form — sort cột 最終編集日 rồi mở modal sort | | | — | Nhấn sort theo cột 最終編集日 → nhấn tiếp nút sort Form 並べ替え | (theo chuẩn sort) | | | OK staging |
| TC079 | [Form] Sort Form — sort cột 管理名 rồi mở modal sort | | | — | Nhấn sort theo cột 管理名 → nhấn tiếp vào modal sort Form 並べ替え | (theo chuẩn sort) | | | OK staging |
| TC080 | [Form] Sort folder — click folder vừa sort (vị trí đầu) | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder vừa sort (folder A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng folder xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK staging |
| TC081 | [Form] Sort folder — click folder ở vị trí số 3 | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC082 | [Form] Sort folder — click folder cuối cùng | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng folder lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC083 | [Form] Sort folder — kéo xuống vị trí số 2, click vừa sort | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên 2. Kéo folder xuống vị trí số 2<br>3. Click vào Form vừa sort (Form A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK staging |
| TC084 | [Form] Sort folder — click folder cuối cùng (sau kéo vị trí 2) | | | Check khi có 6 folder | (tiếp TC083) Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút folder đúng Form lên thành công<br>- Disable nút sort xuống | | | OK staging |
| TC085 | [Form] Sort folder — thao tác liên tục, save list folder | | | Check khi có 6 folder | Check thao tác liên tục: save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | OK staging |
| TC086 | [Form] Sort folder — tạo mới folder | | | Check khi có 6 folder | Check thao tác liên tục: Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | OK staging |
| TC087 | [Form] Check account staff | | | — | Check account staff (sort Form/folder với account staff) | (theo chuẩn) | | | OK staging |

### 4) Màn URL analysis (Status verbatim: OK staging)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC088 | [URL] Sort URL — sort 1 url | | | Check khi sort 1 url | Thực hiện sort 1 URL → save | Sau khi save, hiển thị đúng vị trí của URL đã sắp xếp | | | OK staging |
| TC089 | [URL] Sort URL — sort 1 url, save liên tục | | | Check khi sort 1 url | sort => save => sort => save liên tục | (theo chuẩn sort) | | | OK staging |
| TC090 | [URL] Sort URL — sort nhiều url | | | check khi sort nhiều url | Thực hiện sort nhiều URL | (theo chuẩn sort) | | | OK staging |
| TC091 | [URL] Sort URL — sort nhiều url, save liên tục | | | check khi sort nhiều url | sort => save => sort => save liên tục | (theo chuẩn sort) | | | OK staging |
| TC092 | [URL] Sort URL — sort sau khi edit url | | | Check sort sau khi edit url | Edit url → thực hiện sort | (theo chuẩn sort) | | | OK staging |
| TC093 | [URL] Sort URL — thao tác liên tục, save list đã sort | | | Check thao tác liên tục | save lại list URL đã sort | - Sau khi save hiển thị URL về vị trí mong muốn | | | OK staging |
| TC094 | [URL] Sort URL — khi có 4 URL | | | Check khi có 4 URL | Thực hiện sort URL | Sau khi save, hiển thị đúng vị trí của URL đã sắp xếp | | | OK staging |
| TC095 | [URL] Sort URL — khi có 10 URL | | | Check khi có 10 URL | Thực hiện sort URL | (theo chuẩn sort) | | | OK staging |
| TC096 | [URL] Sort folder — sort 1 folder | | | Check khi sort 1 folder | Thực hiện sort 1 folder → save | Sau khi save, hiển thị đúng vị trí của folder đã sắp xếp | | | OK staging |
| TC097 | [URL] Sort folder — sort nhiều folder | | | Check khi sort nhiều folder | Thực hiện sort nhiều folder | (theo chuẩn sort) | | | OK staging |
| TC098 | [URL] Sort folder — tạo mới rồi sort | | | Check tạo mới => sort | Tạo mới folder → sort | (theo chuẩn sort) | | | OK staging |
| TC099 | [URL] Sort folder — sort rồi tạo mới | | | Check tạo mới => sort | sort => tạo mới | (theo chuẩn sort) | | | OK staging |
| TC100 | [URL] Sort folder — tạo mới liên tục rồi sort | | | Check tạo mới => sort | Tạo mới => tạo mới => sort | (theo chuẩn sort) | | | OK staging |
| TC101 | [URL] Sort folder — xóa rồi sort | | | Check xóa => sort | Xóa folder → sort | (theo chuẩn sort) | | | OK staging |
| TC102 | [URL] Sort folder — xóa liên tục rồi sort | | | Check xóa => sort | Xóa => xóa => sort | (theo chuẩn sort) | | | OK staging |
| TC103 | [URL] Sort folder — sort rồi xóa | | | Check xóa => sort | Sort => xóa | (theo chuẩn sort) | | | OK staging |
| TC104 | [URL] Sort folder — thao tác liên tục, save list folder | | | Check thao tác liên tục | save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | OK staging |
| TC105 | [URL] Sort folder — tạo mới folder | | | Check thao tác liên tục | Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | OK staging |
| TC106 | [URL] Check account staff | | | — | Check account staff (sort URL/folder với account staff) | (theo chuẩn) | | | OK staging |

### 5) Màn Scenario (Status verbatim: OK)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC107 | [Scenario] Sort scen — click scen vừa sort (vị trí đầu) | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên<br>2. Click vào scen vừa sort (scen A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng scen xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK |
| TC108 | [Scenario] Sort scen — click scen ở vị trí số 3 | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên<br>2. Click vào scen ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng scen xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC109 | [Scenario] Sort scen — click scen cuối cùng | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên<br>2. Click vào scen cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC110 | [Scenario] Sort scen — kéo xuống vị trí số 2, click scen vừa sort | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên<br>2. Kéo scen xuống vị trí số 2<br>3. Click vào scen vừa sort (scen A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC111 | [Scenario] Sort scen — kéo xuống vị trí số 2, click scen cuối cùng | | | Check khi có 6 scen | (tiếp TC110) Click vào scen cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC112 | [Scenario] Sort scen — kéo A về vị trí số 1, click scen A | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên<br>2. Kéo scen xuống vị trí số 2<br>3. Kéo scen A về vị trí số 1<br>4. Click vào scen A (scen sort từ dưới lên — scen A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen xuống thành công<br>- Disable nút sort lên | | | OK |
| TC113 | [Scenario] Sort scen — click scen B (vị trí số 2) | | | Check khi có 6 scen | (tiếp TC112) Click vào scen B (scen vừa được đảo lộn vị trí với scen A — scen B đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng scen xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC114 | [Scenario] Sort scen — click scen C (vị trí số 3) | | | Check khi có 6 scen | (tiếp TC112) Click vào scen C (scen sort từ dưới lên — scen C đang ở vị trí số 3) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng scen xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC115 | [Scenario] Sort scen — click scen cuối cùng (sau đảo vị trí) | | | Check khi có 6 scen | (tiếp TC112) Click vào scen cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC116 | [Scenario] Sort scen — kéo vào vị trí số 2, click scen vừa sort | | | Check khi có 6 scen | 1. Kéo scen từ dưới lên vào vị trí số 2<br>2. Click vào scen vừa sort (scen A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng scen xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC117 | [Scenario] Sort scen — click scen ở vị trí số 3 (sau kéo vào vị trí 2) | | | Check khi có 6 scen | (tiếp TC116) Click vào scen ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng scen xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC118 | [Scenario] Sort scen — click scen cuối cùng (sau kéo vào vị trí 2) | | | Check khi có 6 scen | (tiếp TC116) Click vào scen cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC119 | [Scenario] Sort scen — thao tác liên tục, save list đã sort | | | Check khi có 6 scen | Check thao tác liên tục: save lại list scen đã sort | - Sau khi save hiển thị scen về vị trí mong muốn | | | OK |
| TC120 | [Scenario] Sort scen — tạo mới scen | | | Check khi có 6 scen | Check thao tác liên tục: Tạo mới scen | - tạo mới scen thành công<br>- hiển thị scen vị trí đầu tiên | | | OK |
| TC121 | [Scenario] Sort scen — khi có 4 scen | | | Check khi có 4 scen | Thực hiện sort scen | (theo chuẩn sort) | | | OK |
| TC122 | [Scenario] Sort scen — khi có 10 scen | | | Check khi có 10 scen | Thực hiện sort scen | (theo chuẩn sort) | | | OK |
| TC123 | [Scenario] Sort scen — khi có phân trang | | | Check sort khi có phân trang | Thực hiện sort scen khi list có phân trang | (theo chuẩn sort) | | | OK |
| TC124 | [Scenario] Sort scen — search theo tên rồi sort | | | — | Search theo tên scen → Nhấn sort scen | (theo chuẩn sort) | | | OK |
| TC125 | [Scenario] Sort folder — click folder vừa sort (vị trí đầu) | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder vừa sort (folder A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng folder xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | OK |
| TC126 | [Scenario] Sort folder — click folder ở vị trí số 3 | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC127 | [Scenario] Sort folder — click folder cuối cùng | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng folder lên thành công<br>- Disable nút sort xuống | | | OK |
| TC128 | [Scenario] Sort folder — kéo xuống vị trí số 2, click vừa sort | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Kéo folder xuống vị trí số 2<br>3. Click vào scen vừa sort (scen A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | OK |
| TC129 | [Scenario] Sort folder — click folder cuối cùng (sau kéo vị trí 2) | | | Check khi có 6 folder | (tiếp TC128) Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút folder đúng scen lên thành công<br>- Disable nút sort xuống | | | OK |
| TC130 | [Scenario] Sort folder — thao tác liên tục, save list folder | | | Check khi có 6 folder | Check thao tác liên tục: save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | OK |
| TC131 | [Scenario] Sort folder — tạo mới folder | | | Check khi có 6 folder | Check thao tác liên tục: Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | OK |
| TC132 | [Scenario] Check account staff | | | — | Check account staff (sort scen/folder với account staff) | (theo chuẩn) | | | OK |

### 6) Màn Cross-analysis (Status verbatim: Ok STG)

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC133 | [Cross] Sort Cross — click Cross vừa sort (vị trí đầu) | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên<br>2. Click vào Cross vừa sort (Cross A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng Cross xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | Ok STG |
| TC134 | [Cross] Sort Cross — click Cross ở vị trí số 3 | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên<br>2. Click vào Cross ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Cross xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC135 | [Cross] Sort Cross — click Cross cuối cùng | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên<br>2. Click vào Cross cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC136 | [Cross] Sort Cross — kéo xuống vị trí số 2, click Cross vừa sort | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên<br>2. Kéo Cross xuống vị trí số 2<br>3. Click vào Cross vừa sort (Cross A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC137 | [Cross] Sort Cross — kéo xuống vị trí số 2, click Cross cuối cùng | | | Check khi có 6 Cross | (tiếp TC136) Click vào Cross cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC138 | [Cross] Sort Cross — kéo A về vị trí số 1, click Cross A | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên<br>2. Kéo Cross xuống vị trí số 2<br>3. Kéo Cross A về vị trí số 1<br>4. Click vào Cross A (Cross sort từ dưới lên — Cross A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC139 | [Cross] Sort Cross — click Cross B (vị trí số 2) | | | Check khi có 6 Cross | (tiếp TC138) Click vào Cross B (Cross vừa được đảo lộn vị trí với Cross A — "scen B đang ở vị trí số 2") | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Cross xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC140 | [Cross] Sort Cross — click Cross C (vị trí số 3) | | | Check khi có 6 Cross | (tiếp TC138) Click vào Cross C (Cross sort từ dưới lên — Cross C đang ở vị trí số 3) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Cross xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC141 | [Cross] Sort Cross — click Cross cuối cùng (sau đảo vị trí) | | | Check khi có 6 Cross | (tiếp TC138) Click vào Cross cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC142 | [Cross] Sort Cross — kéo vào vị trí số 2, click Cross vừa sort | | | Check khi có 6 Cross | 1. Kéo Cross từ dưới lên vào vị trí số 2<br>2. Click vào Cross vừa sort (Cross A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Cross xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC143 | [Cross] Sort Cross — click Cross ở vị trí số 3 (sau kéo vào vị trí 2) | | | Check khi có 6 Cross | (tiếp TC142) Click vào Cross ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng Cross xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC144 | [Cross] Sort Cross — click Cross cuối cùng (sau kéo vào vị trí 2) | | | Check khi có 6 Cross | (tiếp TC142) Click vào Cross cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC145 | [Cross] Sort Cross — thao tác liên tục, save list đã sort | | | Check khi có 6 Cross | Check thao tác liên tục: save lại list Cross đã sort | - Sau khi save hiển thị Cross về vị trí mong muốn | | | Ok STG |
| TC146 | [Cross] Sort Cross — tạo mới Cross | | | Check khi có 6 Cross | Check thao tác liên tục: Tạo mới Cross | - tạo mới Cross thành công<br>- hiển thị Cross vị trí đầu tiên | | | Ok STG |
| TC147 | [Cross] Sort Cross — khi có 4 Cross | | | Check khi có 4 Cross | Thực hiện sort Cross | (theo chuẩn sort) | | | Ok STG |
| TC148 | [Cross] Sort Cross — khi có 10 Cross | | | Check khi có 10 Cross | Thực hiện sort Cross | (theo chuẩn sort) | | | Ok STG |
| TC149 | [Cross] Sort Cross — khi có phân trang | | | Check sort khi có phân trang | Thực hiện sort Cross khi list có phân trang | (theo chuẩn sort) | | | Ok STG |
| TC150 | [Cross] Sort Cross — search theo tên rồi sort | | | — | Search theo tên Cross → Nhấn sort Cross | (theo chuẩn sort) | | | Ok STG |
| TC151 | [Cross] Sort Cross — sort cột 作成日 rồi mở modal sort | | | — | Nhấn sort theo cột 作成日 → nhấn tiếp nút sort Cross 並べ替え | - Khi click sort ở màn list => thực hiện lấy theo default sort theo positon => click mở modal sort thì clear data về default ( tức sort theo positon ) | | | Ok STG |
| TC152 | [Cross] Sort Cross — sort cột 最終編集日 rồi mở modal sort | | | — | Nhấn sort theo cột 最終編集日 → nhấn tiếp nút sort Cross 並べ替え | (theo chuẩn sort) | | | Ok STG |
| TC153 | [Cross] Sort Cross — sort cột 管理名 rồi mở modal sort | | | — | Nhấn sort theo cột 管理名 → nhấn tiếp vào modal sort Cross 並べ替え | (theo chuẩn sort) | | | Ok STG |
| TC154 | [Cross] Sort folder — click folder vừa sort (vị trí đầu) | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder vừa sort (folder A đang ở vị trí đầu tiên) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới<br>- Thực hiện click vào nút sort đúng folder xuống dưới thành công<br>- Sau khi sort hiển thị đúng vị trí<br>- Disable nút sort lên | | | Ok STG |
| TC155 | [Cross] Sort folder — click folder ở vị trí số 3 | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder ở vị trí số 3 | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC156 | [Cross] Sort folder — click folder cuối cùng | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút sort đúng folder lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC157 | [Cross] Sort folder — kéo xuống vị trí số 2, click vừa sort | | | Check khi có 6 folder | 1. Kéo folder từ dưới lên<br>2. Kéo folder xuống vị trí số 2<br>3. Click vào Cross vừa sort (Cross A đang ở vị trí số 2) | - Hover vào icon 3 chấm hiển thị nút sort xuống dưới và lên<br>- Thực hiện click vào nút sort đúng folder xuống dưới/lên thành công<br>- Sau khi sort hiển thị đúng vị trí | | | Ok STG |
| TC158 | [Cross] Sort folder — click folder cuối cùng (sau kéo vị trí 2) | | | Check khi có 6 folder | (tiếp TC157) Click vào folder cuối cùng | - Hover vào icon 3 chấm hiển thị nút sort lên<br>- Thực hiện click vào nút folder đúng Cross lên thành công<br>- Disable nút sort xuống | | | Ok STG |
| TC159 | [Cross] Sort folder — thao tác liên tục, save list folder | | | Check khi có 6 folder | Check thao tác liên tục: save lại list folder đã sort | - Sau khi save hiển thị folder về vị trí mong muốn | | | Ok STG |
| TC160 | [Cross] Sort folder — tạo mới folder | | | Check khi có 6 folder | Check thao tác liên tục: Tạo mới folder | - tạo mới folder thành công<br>- hiển thị folder vị trí đầu tiên | | | Ok STG |
| TC161 | [Cross] Check account staff | | | — | Check account staff (sort Cross/folder với account staff) | (theo chuẩn) | | | Ok STG |

### Chú thích cột

- **Type**: `Positive` / `Negative` / `Boundary` / `Regression` — Sheet gốc không có cột Type → để trống, member/Leader bổ sung khi review.
- **Priority**: `High` / `Medium` / `Low` — Sheet gốc không có cột Priority → để trống.
- **Output note** / **Assignee** / **Status**: Status lấy verbatim từ Sheet. Output note / Assignee để trống.

### Environment (note)

Sheet gốc đánh dấu Status theo **Staging** (`staging.lme.jp`). Fix mới (branch `ai_fixbug_35968`) chưa được test runtime trong container (xem file 03) → cần re-test trên Staging.

---

## Member tự check trước khi submit

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được
- [ ] Title TC chứa **keyword** giúp Leader nhận ra impact TC đó cover

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md). Mark các mục đã áp dụng:

**§A Checklist web**:
- [ ] A.1 Function checklist — rà CL1-CL22
- [ ] A.2 Non-function: URLs đo lường / Regression / Security / Compatibility

**§C Các tính năng chung**:
- [ ] C.8 Sort ← **trọng tâm task này**

<!-- Source: fetched từ Redmine #35968 Link TCs, tab "#35968" (gid 898638988), KHÔNG có Row range → fetch toàn bộ tab, lúc 2026-06-09. KHÔNG sửa TCs này nếu chưa confirm với Leader. Reconstruct từ format phân cấp Sheet gốc sang 10 cột; giữ verbatim giá trị cell (kể cả lỗi typo gốc: "Tag B" ở Form TC065, "scen B" ở Cross TC139, "nút folder đúng X lên" ở các TC folder cuối cùng). -->
