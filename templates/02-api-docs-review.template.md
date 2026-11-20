# 02 — Review docs Public API v1 · bản `<version>` (`<dd/mm/yyyy>`)

> Report cho Leader đọc. File này do `/review-docs-api` sinh ra, nằm ở `API-DOCS/v<version>_<YYYY-MM-DD>/`.
> **Không lệnh nào đọc hoặc chặn theo file này.** Docs sai hoặc thiếu thì Leader gửi câu hỏi ở §9 cho WSSJ/dev, rồi cập nhật [public-api-spec.md](../../spec-features/api-public/public-api-spec.md) theo bản đã chốt.
> Chạy lại `/review-docs-api` trên cùng bản → **giữ nguyên** cột `Quyết định Leader` đã điền (merge theo mã `DOC-*`), chỉ thêm dòng mới.
>
> **Thứ tự section = thứ tự ưu tiên review:** ① §2 mâu thuẫn trong docs (cả ví dụ) · ② §3 khớp spec · ③ §4 chưa rõ / dễ hiểu sai · ④ §5 dễ đọc · sau đó mới tới phần ưu tiên thấp (§6 – §8).
>
> **Cách đọc bảng:** `L<n>` = số dòng trong `spec-features/api-public/docs/<file bản mới>`; `L<n> bản cũ` = dòng trong file HTML bản cũ.
> Bảng có **Chỗ A / Chỗ B**: 2 chỗ nói khác nhau → **Mâu thuẫn là gì** giải thích bằng lời thường → **(A)** và **(B)** là 2 hướng sửa, Leader chọn 1.
> Cột `Quyết định Leader` để trống cho Leader ghi (vd `Theo (A)` · `Theo (B)` · `Khác: …`).

<!--
CÁCH VIẾT Ô (bắt buộc cho mọi bảng). Leader đã phản hồi 2 lần là ô nén khó hiểu.
- Mỗi ô 1 ý, ngắn. KHÔNG nhồi nhiều ý / nhiều tham chiếu vào 1 ô; thật cần 2 chỗ thì xuống dòng bằng <br>.
- Chỗ A / Chỗ B = **L<n>** · <mục hoặc endpoint hoặc "Ví dụ N (friend X)"> : "<trích nguyên văn ngắn>".
  Luôn ghi tên mục — số dòng một mình không giúp người đọc biết đang ở đâu.
- "Mâu thuẫn là gì" / "Client có thể hiểu sai thế nào" = 1–2 câu tiếng Việt thường, nói ra hậu quả cụ thể (vd "friend nhận tin 2 lần").
  Không dùng mã finding, không viết tắt kiểu "A≠B", không chuỗi ký hiệu "→" dài.
- (A) và (B) là 2 CỘT RIÊNG, mỗi cột 1 việc cụ thể: ai sửa gì. KHÔNG gộp "(A) … / (B) …" vào 1 ô.
-->

## 0. Nguồn

| Trường | Giá trị |
|---|---|
| Docs mới | `spec-features/api-public/docs/<file>` · bản `<version>` (`<ngày>`) · nguồn gốc `<đường dẫn human đưa>` |
| Docs cũ (diff) | `spec-features/api-public/docs/<file>` · bản `<version>` (không có thì ghi `không có, bỏ diff`) |
| Report bản trước | `API-DOCS/v<version cũ>_<ngày>/02-api-docs-review.md` (không có thì ghi `không có`) |
| Spec đối chiếu | Liệt kê file spec + rule đã đọc (chi tiết ở bảng phạm vi §3). Spec reverse-engineer **không phải oracle**: rule chỉ có ở spec thì ghi `(spec reverse, cần kiểm chéo)` |
| Kho TCs đối chiếu | `kho-tcs/fa<xxx>-*.md` đã đọc (liệt kê) |
| Trạng thái code | Route `/v1/*` **chưa có trong source** ([public-api-spec.md §0](../../spec-features/api-public/public-api-spec.md)) → mọi hành vi trong docs chỉ là expected, chưa có chứng cứ chạy thật. Human đã dán kết quả chạy thì ghi ở đây |
| File phụ | `_api-inventory.md` · `_api-diff.md` · `_api-check.md` (cùng folder, do script sinh, không sửa tay) |
| Input thiếu | `<…>` hoặc `—` |

---

## 1. Tóm tắt

| Hạng mục | Số liệu |
|---|---|
| Phạm vi đã rà | `<n>` endpoint · `<m>` dòng param/field · `<k>` khối ví dụ · `<f>` tính năng đối chiếu spec |
| Check máy | JSON lỗi `<a>` · phân trang lệch `<b>` · epoch lệch năm `<c>` · code tabs lệch `<d>` · ví dụ ↔ bảng field lệch `<e>` · dữ liệu mẫu lệch `<g>` · mảng ↔ phân trang lệch `<h>` |
| ① – ④ trọng tâm | INT `<..>` · SPEC `<..>` · CLEAR `<..>` · UX `<..>` |
| Ưu tiên thấp | SEC `<..>` · RISK `<..>` · VER `<..>` · CODE `<..>` |
| Severity | `[BLOCKER] <..>` · `[MAJOR] <..>` · `[MINOR] <..>` · `[NIT] <..>` |

---

## 2. ① Docs tự mâu thuẫn (`DOC-INT`)

> Loại: **Quy tắc** (2 quy tắc trong docs nói khác nhau) · **Ví dụ ↔ docs** (ví dụ trái field / kiểu / ràng buộc / quy tắc của docs) · **Ví dụ bất hợp lý** (dữ liệu mẫu lệch giữa các ví dụ, số đếm, ngày giờ, kết quả không thoả điều kiện lọc…).
> Lệch 400 ↔ 422 cho cùng một kiểu lỗi: `[MINOR]`.
> Sạch → "Đã rà `<n>` quy tắc chung × `<m>` endpoint + `<k>` khối ví dụ — không phát hiện."

| # | Loại | Chỗ A | Chỗ B | Mâu thuẫn là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|---|
| DOC-INT-1 | Ví dụ ↔ docs | **L638** · /friends/detail: friend_info "Chỉ gồm field friend đã có dữ liệu" | **L664–L676** · Ví dụ 1 (friend 12345): có tên quản lý + SĐT nhưng friend_info không có -1, -2 | Theo L638 thì phải có -1, -2. Ví dụ 2 (L700–L701) cùng tình huống thì có | Ví dụ 1 sai → thêm -1, -2 | Quy tắc sai → ghi rõ -1/-2 có thể vắng | `[MAJOR]` | |

---

## 3. ② Docs trái spec (`DOC-SPEC`)

### Phạm vi đối chiếu

> Mỗi endpoint / action API chạm → spec + rule đã đọc → kết quả: `Khớp` · `Trái → DOC-SPEC-<n>` · `Docs im lặng → DOC-CLEAR-<n>` · `Spec không nói`.

| Endpoint / action | Spec + rule đã đọc | Kho đã đọc | Kết quả |
|---|---|---|---|
| `<endpoint / action>` | `<feature>/feature-spec.md` BR-01 … BR-nn | `<ID kho>` / `MT-xx` | `<kết quả>` |

### Điểm trái spec

> Khía cạnh: **Logic** (hành vi, validate, giới hạn, tác dụng phụ) · **Câu chữ** (tên màn hình, nhãn JP, tên & nghĩa trạng thái) · **Dữ liệu** (field lấy từ đâu, nghĩa giá trị).
> Quyết định Leader trong kho (`✅ ĐÃ CHỐT`) thắng spec. Rule chỉ có ở spec → thêm `(spec reverse, cần kiểm chéo)` vào cột "Khác nhau ở đâu".
> Sạch → "Đã rà `<n>` tính năng × `<m>` rule — không phát hiện."

| # | Khía cạnh | Docs ghi | Spec / kho ghi | Khác nhau ở đâu | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|---|
| DOC-SPEC-1 | Logic | **L<n>** · <endpoint>: "<trích>" | **BR-<nn>** (<feature>): <nội dung><br>Kho **<ID kho>** / **MT-xx** | <1 tình huống cụ thể: theo docs → …; theo web → …> | Docs / API sửa theo spec | API cố ý khác → spec / kho cập nhật | | |

---

## 4. ③ Chưa rõ / dễ khiến client hiểu sai (`DOC-CLEAR`)

> Nhóm: **(a)** param thiếu thông tin (6 ý: kiểu · bắt buộc · default · min/max · vượt → ? · sai kiểu → ?) · **(b)** thứ tự lỗi chưa định nghĩa · **(c)** quy tắc LME (spec / kho có) mà docs im lặng · **(d)** "nên / khuyến nghị" không nói vượt thì sao · **(e)** câu chữ 2 cách hiểu, ngoại lệ ẩn, tên dễ nhầm.
> Nhóm nào sạch thì ghi 1 dòng "Không có".

| # | Nhóm | Docs ghi | Client có thể hiểu sai thế nào | Cần làm rõ | Câu hỏi cho WSSJ / dev | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-CLEAR-1 | (d) | **L1057** · /messages/template: `edited_content` "Nên giữ ≤ 5.000 ký tự" | Khách tưởng gửi dài hơn vẫn được, hoặc tưởng server tự cắt | Vượt 5.000 thì server làm gì | `edited_content` > 5.000 ký tự: 422, tự cắt, hay để LINE từ chối? | `[MAJOR]` | |

---

## 5. ④ Dễ đọc (`DOC-UX`)

> Gộp lỗi cùng loại thành 1 dòng (liệt kê vị trí). `[NIT]` mặc định, `[MINOR]` khi gây khó dùng thật.

| # | Vị trí | Hiện tại | Gợi ý sửa | Severity | Quyết định Leader |
|---|---|---|---|---|---|
| DOC-UX-1 | **L<n>** · <mục> | <đang viết thế nào> | <nên viết thế nào> | `[NIT]` | |

---

## 6. Bảo mật & rủi ro (`DOC-SEC` · `DOC-RISK`) — ưu tiên thấp

> Chạy nhẹ: chỉ ghi điểm thấy rõ; nguy cơ `[BLOCKER]` (lộ dữ liệu, ghi nhầm bot, gửi trùng tin) thì ghi đủ.

| # | Chỗ A | Chỗ B | Vấn đề là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-RISK-1 | **L1586** · /do_action: timeout client "khuyến nghị ≥ 60 giây" | **L443** · Idempotency: lần đầu "treo quá 60 giây, server … thực thi lại" | Request lớn chạy quá 60 giây là bình thường. Client gửi lại cùng key → server chạy lần 2 → cộng điểm / gửi tin 2 lần | Docs sửa: timeout client phải ngắn hơn thời gian server giữ key | Server giữ key tới khi lần đầu chạy xong | `[BLOCKER]` | |

---

## 7. Version & changelog (`DOC-VER`) — ưu tiên thấp

> Changelog ↔ thân docs · thay đổi trong `_api-diff.md` mà changelog không nói · "không thay đổi API" mà có field / giới hạn mới · hướng dẫn chuyển đổi · TC bị mục "Đính chính" làm sai · finding report bản trước chưa sửa.

| # | Chỗ A | Chỗ B | Vấn đề là gì | (A) | (B) | TC bị ảnh hưởng | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|---|
| DOC-VER-1 | **L<n>** · changelog: "<trích>" | **L<n>** / **L<n> bản cũ** / **TC <ID>**: "<trích>" | <1–2 câu: lệch gì, khách / TC bị ảnh hưởng thế nào> | <hướng 1> | <hướng 2> | <ID TC hoặc —> | | |

---

## 8. Khẳng định cần chạy thật (`DOC-CODE`)

> Route chưa có code nên các câu dưới đây **chưa có chứng cứ**. Gom từ các mục trên (để chốt (A)/(B)) + mục "Đính chính" của changelog + tác dụng phụ.
> Danh sách cho tester chạy hoặc để `/write-tc` viết TC (`Surface = public-api`, `Nhóm = API`). AI **không** tự gọi API. POST gửi tin chỉ chạy staging.

| # | Khẳng định (L + trích) | Request tối thiểu để kiểm | Expected theo docs | Để chốt | Môi trường | Kết quả (tester điền) |
|---|---|---|---|---|---|---|
| DOC-CODE-1 | **L<n>** · <mục>: "<trích>" | <request> | <expected> | <mã finding / đính chính> | staging | |

---

## 9. Tổng hợp

| Severity | ① INT | ② SPEC | ③ CLEAR | ④ UX | SEC | RISK | VER | Tổng |
|---|---|---|---|---|---|---|---|---|
| `[BLOCKER]` | | | | — | | | | |
| `[MAJOR]` | | | | — | | | | |
| `[MINOR]` | | | | | | | | |
| `[NIT]` | | | | | | | | |

`DOC-CODE`: `<n>` khẳng định cần chạy thật (không tính severity).

### Câu hỏi gửi WSSJ / dev (copy được)

> Xếp theo thứ tự ưu tiên ① → ④ rồi phần thấp. Mỗi câu ghi kèm số bản + mục.

1. `[<version> · mục <x>]` <câu hỏi> — `DOC-<mã>`

### Việc sau review

- [ ] Leader chốt các dòng `Quyết định Leader` (ưu tiên §2 → §5).
- [ ] Cập nhật [public-api-spec.md](../../spec-features/api-public/public-api-spec.md) lên bản `<version>` (README `api-public`: markdown là bản workflow đọc, HTML là bản gốc).
- [ ] TC bị ảnh hưởng ở §7 → sửa trên Studio / kho.
- [ ] Chạy `DOC-CODE` ở §8 (hoặc `/write-tc` để viết TC `public-api`).
