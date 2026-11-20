# 02 — Review docs Public API v1 · bản `1.3.0` (`16/11/2026`)

> Report cho Leader đọc. File này do `/review-docs-api` sinh ra, nằm ở `API-DOCS/v1.3.0_2026-11-16/`.
> **Không lệnh nào đọc hoặc chặn theo file này.** Docs sai hoặc thiếu thì Leader gửi câu hỏi ở §10 cho WSSJ/dev, rồi cập nhật [public-api-spec.md](../../spec-features/api-public/public-api-spec.md) theo bản đã chốt.
> Chạy lại `/review-docs-api` trên cùng bản → **giữ nguyên** cột `Quyết định Leader` đã điền (merge theo mã `DOC-*`), chỉ thêm dòng mới.
>
> **Cách đọc bảng:** `L<n>` = số dòng trong `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html`; `L<n> bản cũ` = dòng trong `api_v1_1104.html` (bản 1.2.0).
> Mỗi dòng: **Chỗ A** và **Chỗ B** là 2 chỗ trong docs (hoặc docs và spec/TC) nói khác nhau → **Mâu thuẫn là gì** giải thích bằng lời thường → **(A)** và **(B)** là 2 hướng sửa, Leader chọn 1.
> Cột `Quyết định Leader` để trống cho Leader ghi (vd `Theo (A)` · `Theo (B)` · `Khác: …`).

## 0. Nguồn

| Trường | Giá trị |
|---|---|
| Docs mới | `spec-features/api-public/docs/api-detail-spec_vi_v1.3.0.html` · bản `1.3.0` (`16/11/2026`) · nguồn gốc `C:/Users/ngoth/Downloads/api-detail-spec_vi.html` |
| Docs cũ (diff) | `spec-features/api-public/docs/api_v1_1104.html` · bản `1.2.0` |
| Report bản trước | không có (lần đầu chạy `/review-docs-api`) |
| Spec đối chiếu | `admin/api-integration/web/logic-spec.md` (vòng đời key, BR-22, BR-26) · `admin/friend-information/feature-spec.md` (SCR-FRI-05, bảng action theo kiểu field) · `admin/tag-management/feature-spec.md` (BR-07) · `admin/chat-11/feature-spec.md` (BR-07 free plan, BR-09 block) |
| Kho TCs đối chiếu | `kho-tcs/fa012-quanlythe-タグ管理.md` (MT-09, TC-TAG-178, TC-TAG-207) · `kho-tcs/fa015-quanlythongtinbanbe-友だち情報管理.md` (MT-11) |
| TC đối chiếu (DOC-VER) | `tasks/2026-09-16_39641_api-phase-1-lien-ket-ngoai-cua-lme/04-tc-list.md` (Studio task 74, 613 TC, snapshot 2026-09-16) |
| Trạng thái code | Route `/v1/*` **chưa có trong source** ([public-api-spec.md §0](../../spec-features/api-public/public-api-spec.md)) → mọi hành vi trong docs chỉ là expected, chưa có chứng cứ chạy thật |
| File phụ | `_api-inventory.md` · `_api-diff.md` · `_api-check.md` (cùng folder, do script sinh, không sửa tay) |
| Input thiếu | Chưa đối chiếu được với code `/v1` (không có trong source). Spec `api-integration` là reverse-engineer → các dòng dựa trên spec này ghi `(spec reverse, cần kiểm chéo)` |

---

## 1. Tóm tắt

| Hạng mục | Số liệu |
|---|---|
| Inventory | 12 endpoint · 90 dòng param/field · 9 param ID (endpoint) + 5 param ID (action object) · 110 dòng lỗi |
| Diff với bản cũ | 106 thay đổi cấu trúc (ứng viên) · 0 endpoint thêm/bớt. Phần lớn là viết lại tài liệu (bảng lỗi riêng mới, param action chuyển sang mục 6) |
| Check máy | JSON lỗi 0 · phân trang lệch 0 · epoch lệch năm 1 · anchor hỏng 0 · code tabs lệch 0/12 |
| Finding | `[BLOCKER] 2` · `[MAJOR] 16` · `[MINOR] 16` · `[NIT] 5` |

---

## 2. Bảo mật & rủi ro (`DOC-SEC` · `DOC-RISK`)

> Đã rà 9 param ID endpoint + 5 param ID trong action object × (bot khác · không tồn tại · đã xoá): docs phủ bằng quy tắc chung L216 (trả 404) và bảng lỗi riêng từng endpoint — không ghi thêm. Còn lại:

| # | Chỗ A | Chỗ B | Vấn đề là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-SEC-1 | **L1725** · Kiểm tra URL media: redirect "Được theo" | **L1734** · chỉ nhận host public, chặn "localhost, IP nội bộ…" | Docs không nói host **sau khi redirect** có bị kiểm lại không. Nếu không, có thể dùng redirect để server gọi vào máy nội bộ (SSRF); lỗi trả về còn lộ mã HTTP, kiểu file, dung lượng của đích (L1736–L1738). IPv6 nội bộ cũng không có trong danh sách chặn | Server đã kiểm lại host sau redirect + chặn IPv6 → docs ghi rõ | Server chưa kiểm → server sửa | `[BLOCKER]` | |
| DOC-SEC-2 | **L1596** · /do_action: thay đổi "ghi nhận như thao tác của người sở hữu API key" | **Spec FA-046 BR-26** · staff được cấp màn API連携 "là được toàn bộ thao tác" | Docs không nói: staff chỉ có quyền màn API連携 có phát hành được key toàn quyền (gửi tin, sửa tag) không; người phát hành rời bot thì key có bị thu hồi không. (spec reverse, cần kiểm chéo) | Server giới hạn key theo quyền người phát hành → docs ghi rõ | Không giới hạn → docs cảnh báo khách tự xoá key khi đổi người | `[MAJOR]` | |
| DOC-RISK-1 | **L1586** · /do_action: timeout client "khuyến nghị ≥ 60 giây" | **L443** · Idempotency: lần đầu "treo quá 60 giây, server … thực thi lại" | Request lớn chạy quá 60 giây là bình thường. Client gửi lại cùng key → server chạy lần 2 → cộng điểm / chạy scenario / gửi tin 2 lần | Docs sửa: timeout client phải ngắn hơn thời gian server giữ key | Server giữ key tới khi lần đầu chạy xong | `[BLOCKER]` | |
| DOC-RISK-2 | **L452** · retry sau lỗi 500: "thường an toàn, trừ point_plus/point_minus và scenario.start" | **L1594** · "scenario.start / resume … gửi message tới friend ngay" | `resume` cũng gửi tin ngay nhưng không có trong danh sách "không an toàn" → khách gửi lại, friend nhận tin 2 lần | Docs thêm `resume` vào danh sách (L452 và L1595) | Server làm `resume` không gửi lại khi chạy 2 lần | `[MAJOR]` | |
| DOC-RISK-3 | **L949** · /messages/push: 200 nghĩa là "đưa message vào hàng đợi gửi" | **L959** · hết hạn mức lúc đang chờ → "message không được gửi"<br>**L1295** · tin gửi lỗi "không được trả về" | Khách nhận 200 nhưng tin không gửi, và API không có chỗ nào cho khách biết | Docs chỉ cách phát hiện | API bổ sung trạng thái gửi | `[MAJOR]` | |
| DOC-RISK-4 | **L216** · mục 1: ID bot khác / không tồn tại "đều trả 404" | **L1588** · /do_action: friend không thuộc bot "bị bỏ qua (không báo lỗi)" | /do_action trả 200 và không liệt kê friend bị bỏ qua → khách tưởng đã áp cho đủ | Docs ghi ngoại lệ này ở mục 1 | Response trả danh sách friend bị bỏ qua | `[MAJOR]` | |
| DOC-RISK-5 | **L430** · Idempotency-Key "duy nhất theo API key" | **L263** · xoay key: phát hành key mới → chuyển sang → xoá key cũ | Đang chuyển key mà gửi lại bằng key mới (cùng Idempotency-Key) → server coi là request mới, chạy lần 2 | Docs cảnh báo ở mục xoay key | Idempotency tính theo bot | `[MINOR]` | |

---

## 3. Mâu thuẫn nội tại (`DOC-INT`)

> Đã rà 7 nhóm quy tắc chung (§1, §2.2, §2.3, §2.4, §2.6, §2.8, §2.9) × 12 endpoint + 7 loại action.

| # | Chỗ A | Chỗ B | Mâu thuẫn là gì | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-INT-1 | **L638** · /friends/detail: friend_info "Chỉ gồm field friend đã có dữ liệu" | **L664–L676** · Ví dụ 1 (friend 12345): có tên quản lý + SĐT nhưng friend_info không có -1, -2 | Theo L638 thì phải có -1, -2. Ví dụ 2 (L700–L701) cùng tình huống thì có | Ví dụ 1 sai → thêm -1, -2 | Quy tắc sai → ghi rõ -1/-2 có thể vắng | `[MAJOR]` | |
| DOC-INT-2 | **L345** · mục 2.6: "sai kiểu số" → 400 | **L527** · /friends: `tag_ids=abc` → 422<br>**L1200** · `handling_status_ids=x` → 422 | Cùng lỗi "truyền chữ vào chỗ cần số", chỗ trả 400 (vd `page=abc`, L525), chỗ trả 422 | Docs ghi ngoại lệ cho ID dạng danh sách | Server thống nhất 1 mã | `[MINOR]` | |
| DOC-INT-3 | **L352** · 422 = "Đúng định dạng nhưng giá trị không hợp lệ" | **L975** · gói LME hết hạn → 422<br>**L976** · friend đã chặn OA → 422 | 2 lỗi này là trạng thái tài khoản, không phải giá trị sai. Hết hạn mức (cũng là trạng thái, L348) lại trả 403 | Docs mở rộng định nghĩa 422 | Server đổi 2 lỗi sang 403 | `[MINOR]` | |
| DOC-INT-4 | **L516** · /friends: `line_name` là string, `""` nếu không có | **L633** · /friends/detail: `line_name` là string hoặc null | Friend không có tên LINE: /friends trả `""`, /friends/detail có thể trả `null` | Docs sửa L633 thành string | Server thống nhất 1 giá trị | `[MINOR]` | |
| DOC-INT-5 | **L216** · mục 1: ID không tồn tại "đều trả 404" | **L1906** · scenario.stop: scenario_id sai "không trả 404"<br>**L1915** · detach bỏ qua ID | 2 chỗ gửi ID sai mà không lỗi; mục 1 không nhắc ngoại lệ | Docs liệt kê ngoại lệ ở mục 1 | Server kiểm ID nếu có gửi | `[MINOR]` | |
| DOC-INT-6 | **L1515** · push text, đọc lại = "Nguyên văn text trong request" | **L1761** · token `[FRIEND_INFO_<id>]` "được lưu ở dạng ID đã mã hoá" | Gửi `[FRIEND_INFO_5001]`, đọc lại ra `[FRIEND_INFO_x7Kq2]` → không còn nguyên văn | Docs thêm ngoại lệ vào L1515 | Server lưu nguyên văn | `[MINOR]` | |

---

## 4. Thiếu / mơ hồ (`DOC-MISS`)

> (a) đã rà 90 dòng param/field; các ý `page`/`limit`, sai kiểu JSON, field lạ, enum được mục chung §2.3 / §2.8 phủ → không ghi.
> Nhóm: **(a)** param thiếu thông tin · **(b)** thứ tự lỗi chưa rõ · **(c)** quy tắc LME bắt buộc mà docs không nói · **(d)** "nên…" mà không nói vượt thì sao.

| # | Nhóm | Endpoint · param / hành vi | Docs ghi (L) | Thiếu gì | Câu hỏi cho WSSJ / dev | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-MISS-1 | `(b)` | Mọi POST · routing | `L264–L277` thứ tự 11 bước · `L234: sai method → 404` | Thứ tự không có bước routing | Key `read` gọi `POST /v1/friends` (path không tồn tại): 403 read-only hay 404 endpoint? | `[MAJOR]` | |
| DOC-MISS-2 | `(b)` | `POST /messages/push`, `/messages/template` | `L961: "friend → mảng messages → từng message"` | Không nói quota 403, bot hết hạn 422, friend chặn 422 đứng ở đâu so với validate message (gồm cả kiểm URL media mất tới 5s/URL) | Request vừa hết quota vừa có URL media lỗi → trả lỗi nào? Kiểm URL có chạy khi đã hết quota? | `[MINOR]` | |
| DOC-MISS-3 | `(c)` | `/do_action` · `tag.add` | `L1846–L1847`: chỉ có lỗi rỗng / không tồn tại | Tag đã đạt giới hạn số người (人数上限). Kho `TC-TAG-207`: tag đầy → không điểm gắn nào gắn thêm được | `tag.add` vào tag đã đầy: 422, bỏ qua im lặng, hay vẫn gắn? | `[MAJOR]` | |
| DOC-MISS-4 | `(c)` | `/do_action` · `friend_info.set` / `point_*` / `today` | `L1591–L1596` Tác dụng phụ: chỉ có `tag.add`, `scenario` | Web: field 選択肢 có action theo option, 年月日 hẹn lịch ± N ngày, ポイント chạy action khi đạt ngưỡng (`friend-information/feature-spec.md` SCR-FRI-05 + bảng kiểu field; kho fa015 MT-11 chưa chốt). (spec reverse, cần kiểm chéo) | Ghi friend info qua API có chạy action / hẹn lịch của field không? Có tính vào hạn mức gửi tin không? | `[MAJOR]` | |
| DOC-MISS-5 | `(c)` | `/do_action` · hạn mức gửi tin | `L1593`, `L1594: "tính vào hạn mức gửi tin"` · bảng lỗi `L1617+` không có 403 `quota_exceeded` | Cách đếm (theo friend? theo action?) và hành vi khi hết hạn mức giữa chừng 100 friend | Gói free: `/do_action` 100 friend chạy action gửi tin tính mấy tin? Hết hạn mức giữa chừng thì trả gì? | `[MAJOR]` | |
| DOC-MISS-6 | `(c)` | Gửi tin qua API · thông báo trần hạn mức | `L956` cách đếm free | Không nói gửi qua API có bắn thông báo 80% / 100% hạn mức như web không | Gửi qua API chạm 1.000 tin có gửi thông báo trần cho admin không? | `[MINOR]` | |
| DOC-MISS-7 | `(c)` | `/messages/push`, `/messages/template` · friend bị LME chặn | `L976` chỉ nói `blocked` (friend chặn OA) · `L2009` có 3 giá trị | `block_status = "block"` (LME chặn friend) thì gửi được không. Web: `chat-11` BR-09 kiểm block trước mọi lần gửi | Gửi cho friend `block_status = "block"`: 200 hay 422? | `[MINOR]` | |
| DOC-MISS-8 | `(a)` | `friend_info.set` TEXT / POINT | `L862: "API không giới hạn độ dài"` · `L863: "không giới hạn min/max"` | Không nói vượt giới hạn lưu trữ thì sao; web có giới hạn thì API phải chặn như web (400/422) | TEXT dài 100.000 ký tự / POINT vượt int32: lưu, cắt, hay lỗi gì? | `[MAJOR]` | |
| DOC-MISS-9 | `(d)` | `POST /messages/template` · `templates[].edited_content` | `L1057: "Nên giữ ≤ 5.000 ký tự"` | Không nói vượt 5.000 thì sao | `edited_content` > 5.000 ký tự: 422, tự cắt, hay để LINE từ chối (200 rồi không gửi)? | `[MAJOR]` | |
| DOC-MISS-10 | `(a)` | Nhiều param số / CSV / ngày | `L1898 start_from ≥ 0` · `L1808 duration` · `L500–L502` filter CSV · `L503–L504` ngày | Không có max: `start_from` vượt số ngày scenario, `duration` rất lớn, số giá trị CSV / độ dài query; ngày đúng định dạng nhưng không tồn tại (`2026-02-30`) | Các trường hợp trên trả gì? | `[MINOR]` | |
| DOC-MISS-11 | `(c)` | Token `[FRIEND_INFO_<field_id>]` | `L1753` · `L1758: "Friend chưa có giá trị → chuỗi rỗng"` | `field_id` thuộc bot khác / không tồn tại | Token với `field_id` bot khác: thay rỗng, giữ nguyên chuỗi, hay 422? | `[MINOR]` | |

---

## 5. Trái nghiệp vụ LME (`DOC-SPEC`)

| # | Docs ghi | Spec / kho ghi | Khác nhau ở đâu | (A) | (B) | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|
| DOC-SPEC-1 | **L1593** · tag.add chạy action của tag, "Chỉ áp cho friend chưa có tag đó" | **BR-07** (tag-management): 1度のみ chỉ chạy ở lần gắn đầu, 何度でも chạy mỗi lần gắn<br>Kho **TC-TAG-178**, **MT-09** | Tag chế độ 1度のみ, friend từng có tag rồi bị gỡ, gắn lại qua API: theo docs → chạy action; theo web → không chạy | Docs bổ sung quy tắc theo 2 chế độ | API cố ý khác web → kho thêm "API" là 1 điểm gắn tag riêng | `[MAJOR]` | |
| DOC-SPEC-2 | **L259** · key bị vô hiệu hoá → "Kích hoạt lại trên LME" | **Spec FA-046** "Vòng đời API key": chỉ có phát hành và xoá, không có kích hoạt lại | Docs hướng dẫn khách làm một việc mà màn quản lý key không có. (spec reverse, cần kiểm chéo) | Docs bỏ "Kích hoạt lại" | Web sẽ có chức năng này → cập nhật spec | `[MAJOR]` | |

---

## 6. Khẳng định cần chạy thật (`DOC-CODE`)

> Route chưa có code nên các câu dưới đây **chưa có chứng cứ**. POST gửi tin chỉ chạy trên staging. AI không gọi API.

| # | Khẳng định (L + trích) | Request tối thiểu để kiểm | Expected theo docs | Vì sao ưu tiên | Môi trường | Kết quả (tester điền) |
|---|---|---|---|---|---|---|
| DOC-CODE-1 | `L1293: "Mới nhất trước"` · `L1295` không trả message ERROR | `GET /v1/conversations/detail` friend có ≥ 3 tin + 1 tin gửi lỗi | `messages[0]` mới nhất; không có tin lỗi | Đính chính ⑨ | staging | |
| DOC-CODE-2 | `L638: friend_info chỉ gồm field đã có dữ liệu` | `GET /v1/friends/detail` friend có 1 field custom trống, 1 field có giá trị; và friend có tên quản lý + SĐT | Field trống không có trong mảng (không phải `value: null`); có / không có `-1`, `-2` → chốt `DOC-INT-1` | Đính chính ⑩ · TC NEW-391/513/537 đang expect ngược | staging | |
| DOC-CODE-3 | `L956: "1 request gửi thành công = 1 tin"` | Bot free: `POST /v1/messages/push` 5 message → so `free_send_count` trước/sau | Tăng đúng 1 | Đính chính ⑬ · TC NEW-662 expect tăng theo số message | staging | |
| DOC-CODE-4 | `L1753`, `L1761`: token được thay khi gửi, lịch sử lưu trước khi thay | push text `"{name}様 [FRIEND_INFO_5001]"` | LINE nhận tên + giá trị; `/conversations/detail` trả `{name}様 [FRIEND_INFO_<mã hoá>]` | Đính chính ⑬ | staging | |
| DOC-CODE-5 | `L1796`: video thiếu `preview_url` → ảnh bìa mặc định | push video không `preview_url` | 200; LINE hiện ảnh "no thumbnail" | Đính chính ⑬ | staging | |
| DOC-CODE-6 | `L976`: friend chặn OA → 422 | push tới friend `block_status = "blocked"` | 422 `ブロックしていますので送信できません。` | Đính chính ⑬ | staging | |
| DOC-CODE-7 | `L1906`, `L1907`: `scenario.stop` dừng tất cả, `scenario_id` không kiểm; chỉ action scenario cuối có hiệu lực | `/do_action` `[scenario.start 88, scenario.stop + scenario_id 999999]` | 200; friend không còn scenario nào đang chạy; không 404 | Đính chính ⑭ | staging | |
| DOC-CODE-8 | `L1593`: `tag.add` chạy action của tag, chỉ cho friend chưa có tag | Tag 1度のみ có action gửi template; friend từng có tag rồi bị gỡ; `/do_action tag.add` | Theo docs: action chạy (friend chưa có tag). Theo BR-07: không chạy → chốt bên nào | Đính chính ⑭ + DOC-SPEC-1 | staging | |
| DOC-CODE-9 | `L443`: in-progress quá 60s → nhả khoá; `L429` trim key; `L441` replay | `/do_action` 100 friend × 10 action (chạy lâu) + retry cùng key sau 61s | Theo docs: lần 2 chạy lại → kiểm điểm có cộng 2 lần | DOC-RISK-1 | staging | |
| DOC-CODE-10 | `L264–L277` thứ tự kiểm tra | Key `read` + `POST /v1/friends`; key `read` + POST thiếu Content-Type | Ghi lại mã thật để chốt DOC-MISS-1 | Hành vi chỉ docs nói | staging | |
| DOC-CODE-11 | `L1725`: `url` được theo redirect | push image với `url` public trả 302 → `http://127.0.0.1/` | 422 "must be a public URL" (không lộ status/kiểu đích) | DOC-SEC-1 | staging | |
| DOC-CODE-12 | `L1588`: friend bot khác bị bỏ qua | `/do_action` `[friend bot A, friend bot B]` + `tag.add` | 200; chỉ friend bot A có tag; friend bot B không đổi | DOC-RISK-4 · bảo mật bot A↔B | staging | |
| DOC-CODE-13 | `L1294`: lịch sử free 180 ngày, trả phí 365 ngày | `/conversations/detail` bot free có tin 181 ngày trước | Tin 181 ngày không trả về | Hành vi chỉ docs nói | staging | |
| DOC-CODE-14 | `L1602–L1603`: > 100 friend / > 10 action → 422 (giới hạn cứng) | `/do_action` 101 friend; 11 action | 422, không friend nào bị đổi | Đính chính ⑧ | staging | |

---

## 7. Version & changelog (`DOC-VER`)

> Diff 1.2.0 → 1.3.0: 106 ứng viên ở `_api-diff.md`. Dòng "chuyển sang mục object", bảng lỗi riêng mới và đổi tên tiêu đề là viết lại tài liệu → không ghi. Không có report bản trước.

| # | Chỗ A | Chỗ B | Vấn đề là gì | (A) | (B) | TC bị ảnh hưởng | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|---|---|
| DOC-VER-1 | **L2025** · changelog 1.3.0: "Không thay đổi API" | **L1057** · `edited_content` gắn nhãn "mới"<br>**L1602** · 100 friend là "Giới hạn cứng" (bản cũ ghi "đề xuất") | Nói không đổi API nhưng có field mới và giới hạn chuyển từ đề xuất sang bắt buộc → khách gửi > 100 friend sẽ bắt đầu bị 422 | Server vốn như vậy, chỉ bổ sung mô tả → changelog ghi rõ | Thay đổi thật → changelog ghi là thay đổi API | — | `[MAJOR]` | |
| DOC-VER-2 | **L638** · đính chính ⑩: friend_info chỉ có field đã có dữ liệu<br>**L640** · type có 6 loại (thêm IMAGE, FILE) | **NEW-391**, **NEW-513** · field chưa nhập trả `null`<br>**NEW-537** · type chỉ 4 loại | 3 TC đang expect theo bản cũ → server đúng docs mới thì TC Fail. Hướng dẫn chuyển đổi (L2047) không nhắc | TC cũ → sửa expected trên Studio | Docs đính chính sai → giữ TC | NEW-391, NEW-513, NEW-537 (Studio task 74) | `[MAJOR]` | |
| DOC-VER-3 | **L956** · đính chính ⑬: gói free "1 request gửi thành công = 1 tin" | **NEW-662** · gửi 2 message → free_send_count "tăng đúng 2" | TC đếm theo số message, docs mới đếm theo số request | TC cũ → sửa expected | Docs đính chính sai → giữ TC | NEW-662 (Studio task 74) | `[MAJOR]` | |
| DOC-VER-4 | **Bản 1.3.0** · `line_friend_id`, `added_time`, `last_message`, `last_message_date` có thể `null` (L515, L520, L632, L1186, L1189, L1190) | **Bản 1.2.0** · các field này không null (L215, L217, L260, L695, L698, L699 bản cũ) | Đổi thành "có thể null" nhưng changelog và hướng dẫn chuyển đổi không nhắc → client khai báo kiểu chặt có thể lỗi | Server vốn trả null → changelog ghi rõ | Thay đổi thật → ghi là thay đổi API | — | `[MINOR]` | |

---

## 8. Ví dụ (`DOC-EX`)

> Đã rà toàn bộ ~100 khối ví dụ theo 2 lớp:
> (1) Máy: `_api-check.md` (75 JSON parse được, 0 lỗi; số học phân trang; epoch; 12/12 code tabs khớp request mẫu) + so từng field / kiểu / enum của ví dụ với bảng field của endpoint → không lệch.
> (2) Tay: thứ tự sắp xếp, ràng buộc request, quy tắc riêng endpoint, định dạng `request_id`, thứ trong tuần của ngày mẫu, và dữ liệu mẫu giữa các endpoint (friend, tag, field, trạng thái xử lý, scenario).
> Lệch `friend_info` của Ví dụ 1 `/friends/detail` đã ghi ở `DOC-INT-1`, không lặp ở đây.

| # | Ví dụ ghi (chỗ A) | Trái với (chỗ B) | Lệch gì | Cách sửa | Severity | Quyết định Leader |
|---|---|---|---|---|---|---|
| DOC-EX-1 | **L335** · `X-RateLimit-Reset` = `1763280060` | **L139** · docs phát hành 16/11/2026 | `1763280060` = 16/11/**2025** 17:01 giờ Nhật → sai năm | Dùng `1794816060` (16/11/2026 17:01) | `[MINOR]` | |
| DOC-EX-2 | **L908** · /scenarios Ví dụ 1: `total_items: 1` | **L921** · /scenarios Ví dụ 2: `total_items: 8` | Cùng bot mẫu mà Ví dụ 1 nói có 1 scenario, Ví dụ 2 nói 8 (changelog ⑫ L2025 nói dùng chung 1 bộ dữ liệu) | Ví dụ 1 ghi 8, thêm ghi chú mảng đã rút gọn | `[MINOR]` | |
| DOC-EX-3 | **L540** · /friends Ví dụ 1: 250 friend, limit 100, mảng chỉ có 1<br>**L1148** · /templates Ví dụ 1: 24 template, mảng chỉ có 2 | **L405** · `limit` = "Số record/trang"<br>**L603** · ví dụ khác có ghi "… 500 phần tử …" | In ít hơn số phải có mà không ghi "rút gọn" → người đọc tưởng API trả thiếu | Thêm ghi chú rút gọn | `[MINOR]` | |
| DOC-EX-4 | **L1366–L1371** · /conversations/detail (friend 12345): được cho vào scenario 「新規登録フォロー」 ngày 13/11 | **L677–L678** · /friends/detail (cùng friend 12345): scenarios chỉ có 88 | Friend đã tham gia 「新規登録フォロー」 nhưng chi tiết friend không liệt kê (trái L643 "Scenario friend đã tham gia") | Thêm scenario 12812 vào Ví dụ 1 /friends/detail | `[MINOR]` | |

---

## 9. Dễ đọc (`DOC-UX`) — chỉ `[NIT]`

| # | Vị trí (L) | Gợi ý | Quyết định Leader |
|---|---|---|---|
| DOC-UX-1 | `L1173` · `L2008` · `L1934–L1935` | `confirm_status` có 3 cách viết: query `0/1`, response `read/unread`, action `confirm/unconfirm` — thêm 1 bảng đối chiếu ở §7.5 | |
| DOC-UX-2 | `L943` vs `L289` | `id_type` phân biệt hoa/thường trong khi enum khác thì không — nêu ngoại lệ ngay ở §2.3 | |
| DOC-UX-3 | `L397`, `L526` | Message `"limit must be a positive integer (1..500)"` trong khi > 500 vẫn được (kẹp) — dễ hiểu nhầm là > 500 lỗi | |
| DOC-UX-4 | `L348` | 「月1000通の配信上限が超えました。」 tự nhiên hơn là 「…上限を超えました。」 (nếu là chuỗi server thì sửa ở server) | |
| DOC-UX-5 | `L2009` | `blocked` (friend chặn OA) và `block` (LME chặn friend) chỉ khác 2 chữ — dễ nhầm khi code | |

---

## 10. Tổng hợp

| Severity | SEC | RISK | INT | MISS | SPEC | VER | EX | UX | Tổng |
|---|---|---|---|---|---|---|---|---|---|
| `[BLOCKER]` | 1 | 1 | — | — | — | — | — | — | 2 |
| `[MAJOR]` | 1 | 3 | 1 | 6 | 2 | 3 | — | — | 16 |
| `[MINOR]` | — | 1 | 5 | 5 | — | 1 | 4 | — | 16 |
| `[NIT]` | — | — | — | — | — | — | — | 5 | 5 |

`DOC-CODE`: 14 khẳng định cần chạy thật (không tính severity).

### Câu hỏi gửi WSSJ / dev (copy được)

1. `[1.3.0 · mục 5 Kiểm tra URL media]` `url` được theo redirect: host sau mỗi bước redirect có bị kiểm lại là public không? IPv6 nội bộ (`::1`, `fc00::/7`) có bị chặn không? — `DOC-SEC-1`
2. `[1.3.0 · mục 2.2 / 4 do_action]` Key do staff phát hành có bị giới hạn theo quyền tính năng của staff không? Người phát hành bị xoá khỏi bot / mất quyền thì key còn hiệu lực không? — `DOC-SEC-2`
3. `[1.3.0 · mục 2.9 / 4 do_action]` Request `/do_action` chạy quá 60 giây (đúng khuyến nghị timeout) mà client retry cùng Idempotency-Key thì có bị chạy lại không? — `DOC-RISK-1`
4. `[1.3.0 · mục 2.9 / 4 do_action]` `scenario.resume` có gửi lại step khi retry không? Nếu có, xin thêm vào danh sách "không idempotent". — `DOC-RISK-2`
5. `[1.3.0 · mục 4 messages/push]` Khi tin không gửi vì hết hạn mức lúc chờ trong hàng đợi, khách biết bằng cách nào qua API? — `DOC-RISK-3`
6. `[1.3.0 · mục 1 / 4 do_action]` Có thể trả danh sách friend bị bỏ qua trong response `/do_action` không? Nếu không, xin nêu ngoại lệ này ở mục 1. — `DOC-RISK-4`
7. `[1.3.0 · mục 4 friends/detail]` `friend_info` có luôn gồm `-1`/`-2` khi friend có tên quản lý / SĐT không? Ví dụ 1 và Ví dụ 2 đang khác nhau. — `DOC-INT-1`
8. `[1.3.0 · mục 2.2]` Key `read` gọi `POST /v1/friends` (path không tồn tại) trả 403 hay 404? — `DOC-MISS-1`
9. `[1.3.0 · mục 6 tag]` `tag.add` vào tag đã đạt giới hạn số người thì trả gì? — `DOC-MISS-3`
10. `[1.3.0 · mục 6 friend_info]` Ghi friend info qua API có chạy action của field (theo option / ngày / ngưỡng điểm) như web không? Có tính vào hạn mức gửi tin không? — `DOC-MISS-4`
11. `[1.3.0 · mục 4 do_action]` Gói free: `/do_action` kéo theo gửi tin (tag action, scenario) được đếm thế nào? Hết hạn mức giữa chừng thì trả gì? — `DOC-MISS-5`
12. `[1.3.0 · mục 4 friend-info-fields]` TEXT / POINT "không giới hạn ở bước kiểm tra": vượt giới hạn lưu trữ (rất dài / vượt int32) thì sao? Web có giới hạn thì API có chặn giống web không? — `DOC-MISS-8`
13. `[1.3.0 · mục 4 messages/template]` `edited_content` > 5.000 ký tự thì sao? — `DOC-MISS-9`
14. `[1.3.0 · mục 6 tag]` `tag.add` có xét chế độ 「1度のみ / 何度でも」 của tag không (gỡ rồi gắn lại có chạy action không)? — `DOC-SPEC-1`
15. `[1.3.0 · mục 2.2 Vòng đời key]` Trên LME có thao tác "kích hoạt lại" key bị vô hiệu không? — `DOC-SPEC-2`
16. `[1.3.0 · mục 8 Lịch sử cập nhật]` `edited_content` (nhãn "mới") và giới hạn cứng 100/10 là thay đổi API thật hay chỉ bổ sung mô tả? Các field chuyển sang nullable có phải thay đổi không? — `DOC-VER-1`, `DOC-VER-4`
17. Câu hỏi phụ (`[MINOR]`): thứ tự quota/URL media (`DOC-MISS-2`) · thông báo trần qua API (`DOC-MISS-6`) · gửi cho friend `block` (`DOC-MISS-7`) · max của `start_from` / `duration` / CSV / ngày không tồn tại (`DOC-MISS-10`) · token friend info của bot khác (`DOC-MISS-11`) · 400↔422 (`DOC-INT-2`, `DOC-INT-3`) · kiểu `line_name` (`DOC-INT-4`) · sửa ví dụ (`DOC-EX-1` → `DOC-EX-4`).

### Việc sau review

- [ ] Leader chốt các dòng `Quyết định Leader` (ưu tiên §2).
- [ ] Cập nhật [public-api-spec.md](../../spec-features/api-public/public-api-spec.md) lên bản `1.3.0` (README `api-public`: markdown là bản workflow đọc, HTML là bản gốc).
- [ ] TC bị ảnh hưởng ở §7 (`NEW-391`, `NEW-513`, `NEW-537`, `NEW-662` — Studio task 74) → sửa expected trên Studio.
- [ ] Chạy `DOC-CODE` ở §6 (hoặc `/write-tc` để viết TC `public-api`).
