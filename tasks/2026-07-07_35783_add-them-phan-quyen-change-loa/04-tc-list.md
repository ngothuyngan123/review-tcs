<!-- sync-target: https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2061242964 -->
<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2061242964 | sheet=Improve 7/10/2024 | anchor=Main Function --> <!-- ⚠️ verify anchor "Main Function" tồn tại trong sheet trước khi /sync-review-tc -->

# 04 — TC List (fetch từ Redmine #35783 Link TCs)

> ⚠️ **TC read-only fetch từ Google Sheet master** — KHÔNG sửa Title / Steps / Expected. Nếu nghi TC không còn đúng sau fix, ghi vào report (`/review-tc`), confirm với Leader, KHÔNG chỉnh trực tiếp file này.
>
> **Nguồn**: Sheet "Improve 7/10/2024" (gid 2061242964), row 506–517. Bảng gốc dạng **phân cấp merged-cell** (Main Function → User → điều kiện phân quyền → thao tác → Expected). Mỗi row = 1 TC leaf → gán TC001–TC012 theo thứ tự row. Cột `Type`/`Priority`/`Output note`/`Assignee`/`Status` **không có trong sheet gốc** → để trống (KHÔNG bịa). Text giữ nguyên văn (bao gồm cách viết gốc như "Thục hiện", "phần quyền", "k có").

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | fetch từ Sheet master (read-only) |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1z8QfSl5iz5D1W3gboyfirI72bVK6hsYG-o3jjBa3wtE/edit?gid=2061242964 — Sheet "Improve 7/10/2024" row 506–517 |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Check màn setting phân quyền — User chính | | | User chính | Mở vào màn hình (setting phân quyền) | không còn hiển thị mục  「LINE公式アカウント入れ替え」 | | | |
| TC002 | Check màn setting phân quyền — User staff | | | User staff | Mở vào màn hình (setting phân quyền) | không còn hiển thị mục  「LINE公式アカウント入れ替え」 | | | |
| TC003 | Check User access vào hình change bot — User chính, mở từ menu thường | | | User chính access | Nhấn mở màn hình từ menu → Nhấn mở từ menu thường | - User chính access được vào các url của màn change bot<br>- Thục hiện change bot success | | | |
| TC004 | Check User access vào hình change bot — User chính, mở từ menu favorite | | | User chính access | Nhấn mở màn hình từ menu → Nhấn mở từ menu favorite | - User chính access được vào các url của màn change bot<br>- Thục hiện change bot success | | | |
| TC005 | Check User access vào hình change bot — User chính, access các url | | | User chính access | Access các url của màn hình change bot:<br>https://booking.watermeru.com/admin/change-bots-new/E2abBdyZrwvg<br>https://booking.watermeru.com/admin/change-bot-sub/E2abBdyZrwvg?type_change=immediate<br>https://booking.watermeru.com/admin/change-bots-new/E2abBdyZrwvg?type=change_sub&change_success=1<br>https://booking.watermeru.com/admin/change-bot-sub/E2abBdyZrwvg?type_change=scheduled | - User chính access được vào các url của màn change bot<br>- Thục hiện change bot success | | | |
| TC006 | Check User access vào hình change bot — User chính, thực hiện change bot | | | User chính access | Thục hiện change bot | - User chính access được vào các url của màn change bot<br>- Thục hiện change bot success | | | |
| TC007 | Check User access — Staff cũ (trước đó ĐƯỢC phân quyền change bot), mở từ menu thường | | | User staff access → Check các user staff cũ → Trước đó được phân quyền màn hình change bot | Nhấn mở màn hình từ menu → Nhấn mở từ menu thường | Disable menu không cho phép access | | | |
| TC008 | Check User access — Staff cũ (trước đó ĐƯỢC phân quyền change bot), mở từ menu favorite | | | User staff access → Check các user staff cũ → Trước đó được phân quyền màn hình change bot | Nhấn mở màn hình từ menu → Nhấn mở từ menu favorite | Disable menu không cho phép access | Hiện tại menu favorite sẽ không disable (Check các màn khác k được phần quyền cũng vẫn hiển thị như vậy) => Click vào menu thì sẽ redirect sang màn admin/home và hiện msg  この権限は許可されていません。 | | |
| TC009 | Check User access — Staff cũ (trước đó ĐƯỢC phân quyền change bot), access các url | | | User staff access → Check các user staff cũ → Trước đó được phân quyền màn hình change bot | Access các url của màn hình change bot:<br>https://booking.watermeru.com/admin/change-bots-new/E2abBdyZrwvg<br>https://booking.watermeru.com/admin/change-bot-sub/E2abBdyZrwvg?type_change=immediate<br>https://booking.watermeru.com/admin/change-bots-new/E2abBdyZrwvg?type=change_sub&change_success=1<br>https://booking.watermeru.com/admin/change-bot-sub/E2abBdyZrwvg?type_change=scheduled |  Redirect về màn admin/home và hiện message không có quyền この権限は許可されていません。 | | | |
| TC010 | Check User access — Staff cũ (trước đó ĐƯỢC phân quyền change bot), thực hiện change bot | | | User staff access → Check các user staff cũ → Trước đó được phân quyền màn hình change bot | Thục hiện change bot | Không access được màn hình nên cũng không thực hiện được change bot | | | |
| TC011 | Check User access — Staff cũ (trước đó KHÔNG được phân quyền change bot), mở từ menu thường | | | User staff access → Check các user staff cũ → Trước đó không được phân quyền màn change bot | Nhấn mở màn hình từ menu → Nhấn mở từ menu thường | Disable menu không cho phép access | | | |
| TC012 | Check User access — Staff cũ (trước đó KHÔNG được phân quyền change bot), mở từ menu favorite | | | User staff access → Check các user staff cũ → Trước đó không được phân quyền màn change bot | Nhấn mở màn hình từ menu → Nhấn mở từ menu favorite | Disable menu không cho phép access | Hiện tại menu favorite sẽ không disable (Check các màn khác k được phần quyền cũng vẫn hiển thị như vậy) => Click vào menu thì sẽ redirect sang màn admin/home và hiện msg  この権限は許可されていません。 | | |

### Chú thích cột

- **Type / Priority / Output note / Assignee / Status**: sheet gốc dạng phân cấp không có các cột này → để trống. `/review-tc` sẽ suy luận Type (Positive/Negative/Boundary/Regression) từ Steps/Expected.
- **Precondition** dùng dấu `→` để thể hiện phân cấp merged-cell gốc (User → nhóm staff → điều kiện phân quyền trước đó).
- **Expected** của TC003–TC006 dùng chung 1 ô merged trong sheet ("- User chính access... success") → điền lại cho từng TC leaf.

### Environment (note)

Mặc định test trên **Staging** (`staging.lme.jp`). URL trong TC là môi trường `booking.watermeru.com` (theo sheet gốc) — verify lại domain đúng env trước khi run.

---

## Member tự check trước khi submit

`<member điền sau khi review>`

<!-- Source: fetched từ Redmine #35783 Link TCs, range A506:J517 tab "Improve 7/10/2024" lúc 2026-07-07. KHÔNG sửa TCs này nếu chưa confirm với Leader. Bảng gốc dạng phân cấp merged-cell; TC001–TC012 = row 506–517 theo thứ tự. -->
