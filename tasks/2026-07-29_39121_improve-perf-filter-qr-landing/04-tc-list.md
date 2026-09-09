<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=703112589#gid=703112589 | sheet=Improve nhỏ  | anchor=Main Function -->
<!-- LƯU Ý: tên tab là "Improve nhỏ " CÓ DẤU CÁCH Ở CUỐI. Khi /sync-review-tc chạy phải giữ đúng trailing space, nếu không API báo "Unable to parse range". -->

# 04 — TC List (fetch read-only từ Sheet human/master)

> ⚠️ **File này KHÔNG phải TC do member/AI mới viết** — đây là **TC người đã có sẵn** trên Sheet master, fetch read-only từ **Link TCs** trong Redmine #39121 (journal của Ngô Thúy Ngần). **KHÔNG sửa nội dung** — chỉ dùng làm input cho `/review-tc` đánh giá coverage.
>
> Sheet nguồn dùng **format phân cấp riêng** (Main Function → Sub1..Sub5 → Expect Result), **không phải 16 cột canonical**. Ô merged đã được **fill-down** để mỗi dòng đọc độc lập — **không chữ nào bị đổi**. Text gốc của cột "Kết quả mong đợi" giữ verbatim trong **Legend** bên dưới.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | Ngô Thúy Ngần (theo Sheet master) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | fetch từ Sheet 2026-07-29 |
| Link TC gốc (nếu có) | https://docs.google.com/spreadsheets/d/1ADqqyfszLKBkXNetsoTbsPgthCCDL_Cj710cUrbONU8/edit?gid=703112589#gid=703112589 — tab **"Improve nhỏ "**, dòng **1197–1259** (block #39121, header ở dòng 1196) |

---

## Legend — Kết quả mong đợi (text verbatim từ cột "Expect Result")

| Mã | Kết quả mong đợi (nguyên văn) |
|---|---|
| **E-IN-1** | `- Thực hiện filter ra friend đã kết bạn qua QR đó` <br> `+ friend new` <br> `+ friend unblock` <br> `db: bảng detail_landing_click.action = 2` |
| **E-IN-N** | `- Thực hiện filter ra các friend đã kết bạn qua các QR đó` <br> `+ friend new / + friend unblock / db: detail_landing_click.action = 2` |
| **E-IN-Nor** | `- Thực hiện filter ra các friend đã kết bạn qua 1 trong các QR đó` <br> `+ friend new / + friend unblock / db: detail_landing_click.action = 2` |
| **E-EX-1** | `- Thực hiện filter loại bỏ friend đã kết bạn qua QR đó` <br> `+ friend new / + friend unblock / db: detail_landing_click.action = 2` |
| **E-EX-N** | `- Thực hiện filter loại bỏ các friend đã kết bạn qua các QR đó` <br> `+ friend new / + friend unblock / db: detail_landing_click.action = 2` |
| **E-EX-Nor** | `- Thực hiện filter loại bỏ các friend đã kết bạn qua 1 trong các QR đó` <br> `+ friend new / + friend unblock / db: detail_landing_click.action = 2` |
| **E-QR** | `- Hiển thị đúng các friend đã add friend qua QR` <br> `+ Detail kết bạn - tab 友だち一覧: cột 友だちの種類 hiển thị 2 loại 友だちの種類 và 新規友だち` <br> `+ Các friend có 2 loại ブロックを解除した友だち và 新規友だち thỏa mãn điều kiện` |
| **E-OLD** | `- Friend old không được tính là kết bạn qua landing` <br> `- db: bảng detail_landing_click.action = 1` |
| **E-STAFF-count** | `Đảm bảo chỉ các friend thỏa mãn điều kiện kết bạn qua QR được filter được count vào phân tích` |
| **E-STAFF-action** | `Đảm bảo chỉ các friend thỏa mãn điều kiện kết bạn qua QR được filter nhận được action bình thường` |

> Cột **KQ #39121** = giá trị nguyên trong cột "Specimprove #39121" (cột I) của Sheet: `OK` = đã đánh dấu / `–` = để trống. **Ý nghĩa (đã test hay chỉ đánh dấu scope) tester xác nhận lại với người viết.**

---

## Block 1 — Main Function: `Check lại hiển thị data khi thực hiện add filter QR với option 選択したQRコードアクションを1つ以上含む友だち` (include — dùng `IN`)

| Dòng | Sub1 (màn) | Sub2 | Sub3 | Sub4 | Kết quả mong đợi | KQ #39121 |
|---|---|---|---|---|---|---|
| 1197 | Tại màn friendlist | Filter and | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1198 | Tại màn friendlist | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-IN-N | OK |
| 1199 | Tại màn friendlist | filter OR | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1200 | Tại màn friendlist | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-IN-Nor | OK |
| 1201 | Tại màn QR | Check lại data friend đã kết bạn qua QR đó | Friend new | — | E-QR | OK |
| 1202 | Tại màn QR | Check lại data friend đã kết bạn qua QR đó | Friend unblock | — | 〃 E-QR (ô merged) | OK |
| 1203 | Tại màn QR | Check case friend old quét qr có được tính là đã kết bạn qua landing A không | — | — | E-OLD | OK |
| 1204 | Tại Broadcast | Filter and | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1205 | Tại Broadcast | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-IN-N | OK |
| 1206 | Tại Broadcast | filter OR | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1207 | Tại Broadcast | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-IN-Nor | OK |
| 1208 | Tại scenario — Set filter tại 選択中の配信対象 | Filter and | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1209 | Tại scenario — Set filter tại 選択中の配信対象 | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-IN-N | OK |
| 1210 | Tại scenario — Set filter tại 選択中の配信対象 | filter OR | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1211 | Tại scenario — Set filter tại 選択中の配信対象 | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-IN-Nor | OK |
| 1212 | Tại Auto reply | Filter and | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1213 | Tại Auto reply | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-IN-N | OK |
| 1214 | Tại Auto reply | filter OR | Khi tích filter 1 QR | — | E-IN-1 | OK |
| 1215 | Tại Auto reply | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-IN-Nor | OK |
| 1216 | Tại Action schedule | Filter and | Khi tích filter 1 QR | — | E-IN-1 | – |
| 1217 | Tại Action schedule | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-IN-N | – |
| 1218 | Tại Action schedule | filter OR | Khi tích filter 1 QR | — | E-IN-1 | – |
| 1219 | Tại Action schedule | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-IN-Nor | – |
| 1220 | Tại Cross analysis | Filter cha | Filter and — Khi tích filter 1 QR | — | E-IN-1 | – |
| 1221 | Tại Cross analysis | Filter cha | Filter and — Khi tích filter nhiều QR | — | E-IN-N | – |
| 1222 | Tại Cross analysis | Filter cha | filter OR — Khi tích filter 1 QR | — | E-IN-1 | – |
| 1223 | Tại Cross analysis | Filter cha | filter OR — Khi tích filter nhiều QR | — | E-IN-N | – |
| 1224 | Tại Cross analysis | Filter điều kiện phân tích | Filter and — Khi tích filter 1 QR | — | E-IN-1 | – |
| 1225 | Tại Cross analysis | Filter điều kiện phân tích | Filter and — Khi tích filter nhiều QR | — | E-IN-N | – |
| 1226 | Tại Cross analysis | Filter điều kiện phân tích | filter OR — Khi tích filter 1 QR | — | E-IN-1 | – |
| 1227 | Tại Cross analysis | Filter điều kiện phân tích | filter OR — Khi tích filter nhiều QR | — | E-IN-N | – |

> Cross analysis (1220–1227): Sheet lồng thêm 1 tầng (`Filter cha` / `Filter điều kiện phân tích`) → cột Sub3 gộp `Filter and/OR` + `1 QR / nhiều QR`; không có cột "Pick n QR".

## Block 2 — Main Function: `Check lại hiển thị data khi thực hiện add filter QR với option 選択したQRコードアクションを1つ以上含む人を除く友だち` (exclude — dùng `NOT IN`)

| Dòng | Sub1 (màn) | Sub2 | Sub3 | Sub4 | Kết quả mong đợi | KQ #39121 |
|---|---|---|---|---|---|---|
| 1228 | Tại màn friendlist | Filter and | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1229 | Tại màn friendlist | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-EX-N | – |
| 1230 | Tại màn friendlist | filter OR | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1231 | Tại màn friendlist | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-EX-Nor | – |
| 1232 | Tại màn QR | Check lại data friend đã kết bạn qua QR đó | Friend new | — | E-QR | – |
| 1233 | Tại màn QR | Check lại data friend đã kết bạn qua QR đó | Friend unblock | — | 〃 E-QR (ô merged) | – |
| 1234 | Tại màn QR | Check case friend old quét qr có được tính là đã kết bạn qua landing A không | — | — | E-OLD | – |
| 1235 | Tại Broadcast | Filter and | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1236 | Tại Broadcast | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-EX-N | – |
| 1237 | Tại Broadcast | filter OR | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1238 | Tại Broadcast | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-EX-Nor | – |
| 1239 | Tại scenario | Filter and | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1240 | Tại scenario | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-EX-N | – |
| 1241 | Tại scenario | filter OR | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1242 | Tại scenario | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-EX-Nor | – |
| 1243 | Tại Auto reply | Filter and | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1244 | Tại Auto reply | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-EX-N | – |
| 1245 | Tại Auto reply | filter OR | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1246 | Tại Auto reply | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-EX-Nor | – |
| 1247 | Tại Action schedule | Filter and | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1248 | Tại Action schedule | Filter and | Khi tích filter nhiều QR | Pick 2 QR | E-EX-N | – |
| 1249 | Tại Action schedule | filter OR | Khi tích filter 1 QR | — | E-EX-1 | – |
| 1250 | Tại Action schedule | filter OR | Khi tích filter nhiều QR | pick 3 QR | E-EX-Nor | – |
| 1251 | Tại Cross analysis | Filter cha | Filter and — Khi tích filter 1 QR | — | E-EX-1 | – |
| 1252 | Tại Cross analysis | Filter cha | Filter and — Khi tích filter nhiều QR | — | E-EX-N | – |
| 1253 | Tại Cross analysis | Filter cha | filter OR — Khi tích filter 1 QR | — | E-EX-1 | – |
| 1254 | Tại Cross analysis | Filter cha | filter OR — Khi tích filter nhiều QR | — | E-EX-N | – |
| 1255 | Tại Cross analysis | Filter điều kiện phân tích | Filter and — Khi tích filter 1 QR | — | E-EX-1 | – |
| 1256 | Tại Cross analysis | Filter điều kiện phân tích | Filter and — Khi tích filter nhiều QR | — | E-EX-N | – |
| 1257 | Tại Cross analysis | Filter điều kiện phân tích | filter OR — Khi tích filter 1 QR | — | E-EX-1 | – |
| 1258 | Tại Cross analysis | Filter điều kiện phân tích | filter OR — Khi tích filter nhiều QR | — | E-EX-N | – |

## Block 3 — Main Function: `Check account staff` (phân quyền staff)

| Dòng | Sub1 | Sub2 | Sub3 | Kết quả mong đợi | KQ #39121 |
|---|---|---|---|---|---|
| 1259 | Check cover tại staff các friend thỏa mãn điều kiện tương ứng được nhận action bình thường | Với action `選択したQRコードアクションを1つ以上含む友だち` | Cross analysis | E-STAFF-count | – |
| 1260 | Check cover tại staff các friend thỏa mãn điều kiện tương ứng được nhận action bình thường | Với action `選択したQRコードアクションを1つ以上含む友だち` | Action schedule | E-STAFF-action | OK |

> Ghi chú: dòng 1260 (Action schedule) nằm ngay sau range QA link (1197–1259) nhưng vẫn thuộc block "Check account staff" của #39121 → giữ để đủ ngữ cảnh.

---

## Nhận xét nhanh coverage (để `/review-tc` soi tiếp — KHÔNG phải kết luận)

- Ma trận human phủ **2 option filter** (include `IN` / exclude `NOT IN`) × **7 surface** (friendlist, QR screen, Broadcast, scenario, Auto reply, Action schedule, Cross analysis) × **{AND, OR}** × **{1 QR, nhiều QR}** → khớp với 6 chỗ fix (`Conversation` + `ConversationReplicate`, AND + OR).
- ⚠️ **Thiếu chiều PERFORMANCE**: đây là ticket *Improve performance* nhưng **không có TC nào đo thời gian / bot lớn / EXPLAIN** — trong khi Dev nêu rõ chưa đo được thời gian thật và rủi ro materialization ở prod (file 03 §5).
- ⚠️ **Thiếu boundary/abnormal**: chưa thấy TC cho **danh sách mã QR rỗng** (`in ()` — Dev nói giữ nguyên lỗi cũ), **friend có `line_id` NULL** (Dev thêm `line_id is not null`), **so khớp số bạn bè trước/sau fix** trên cùng bot.
- ⚠️ **Loại QR web** (`is_action_web`) được fix nhưng TC chỉ nhắc `action = 2` (QR đăng ký bạn) — chưa rõ có cover QR thao tác web không.
- Cột #39121 "OK" chỉ đánh ở Block 1 màn friendlist→Auto reply (1197–1215) + 1 dòng staff (1260); Action schedule/Cross analysis của Block 1 và **toàn bộ Block 2 (exclude)** đang `–`.

<!-- Source: fetch từ Redmine #39121 Link TCs (journal Ngô Thúy Ngần), tab "Improve nhỏ " (gid 703112589), dòng 1196–1260, lúc 2026-07-29. Sheet dùng service-account (google-sheets MCP không kết nối được thời điểm chạy → fetch bằng scripts service-account). KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
