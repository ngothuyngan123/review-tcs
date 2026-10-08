# 05 — Review Report

> Draft cho Leader verify — chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #360 (round 1, branch `ai_fixbug_41004`, run 2709 staging 2026-10-05 11:01) |
| Tổng số TC review | 15 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 | 1/7 mục có TC đạt chuẩn — **CHƯA ĐỦ** (BUG/F1/F3/T1/F6 hạ RISK do expected trái quy tắc chốt 2026-10-05; F2/D2/T2/T3 loại khỏi mẫu số — GAP giả G1) |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (`SalesManagementV2Controller.php` +4/−1) | 1/5 điểm có TC đạt chuẩn — **CHƯA ĐỦ** (3 điểm về SP ẩn loại khỏi mẫu số — GAP giả G1/G2) |

**Kết luận**: 2/12 vùng ảnh hưởng đủ TC (F4 + điểm diff "view không còn `?? 0`", cùng cover bởi NEW-14/NEW-17) · 4 GAP (G3, G5, G6, G8) · 2 RISK (G4, G7) · 2 GAP giả đã loại (G1, G2 — SP ẩn, 7 mục).
Mẫu số (a) = BUG + F1–F6 + D2 + T1–T3 (F7 không tính — Dev ghi "yokoten, chưa sửa", xem §5 I6). Mẫu số (b) = 8 dòng `dev_impact` của Studio: nhánh SP không tồn tại · chặn SP ẩn khi có u_code · không chặn preview/link không u_code · thay đổi nghiệp vụ khách đang hợp đồng · thứ tự kiểm 410 · hồi quy khách đã đăng ký · hồi quy các thông báo lỗi khác · view mất lớp `?? 0`.

⚠️ Case **sản phẩm ẩn** đã loại khỏi phạm vi test (human chốt 2026-10-05): spec FA-026 xác nhận V2 không có UI ẩn (`feature-spec.md:82`, `:191`, `:729`), kho FA-026 không có TC ẩn; chỉ V1 legacy có nút ẩn (EP-33) nhưng link public change/cancel của V1 trả 404 (`:884`). Nhánh `status_valid != 1` mà #42041 thêm vào code gần như là code chết → hỏi Dev ở §8 S3.

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | F2 / D2 `s_items.status_valid` / T2 / T3 — `orderChange` có u_code + SP `status_valid != 1` → chặn form đổi thẻ (#42041) | dev-impact + diff code | không có | **GAP giả — loại khỏi phạm vi test (human chốt 2026-10-05).** Căn cứ: spec FA-026 `:82`, `:191`, `:729` — V2 không có UI ẩn, `saveItem` luôn ghi `status_valid = 1`; kho FA-026 không có TC ẩn sản phẩm; V1 public link change/cancel trả 404 (`:884`). Không đề xuất TC — chuyển sang §8 S3 hỏi Dev giữ hay gỡ nhánh chết | — |
| G2 | #42041 không chặn nhầm preview / link không u_code khi SP ẩn | diff code | không có | **GAP giả — cùng căn cứ G1** (không tạo được SP ẩn từ UI V2). Không đề xuất TC | — |
| G3 | Thứ tự kiểm: SP không tồn tại → bot hết hạn (410) → SP ẩn → trạng thái hợp đồng | diff code | không có | GAP — chưa TC Boundary nào ghép SP ẩn/xoá với bot `plan_type=1` hết hạn > 7 ngày | `[MAJOR]` |
| G4 | Hồi quy: SP công khai + khách **đã đăng ký** mở link đổi thẻ (có u_code) → vẫn hiện form | diff code | NEW-6 (chỉ preview admin, không có u_code khách) | RISK — điều kiện mới chèn ngay trước nhánh kiểm hợp đồng, nhưng chưa TC nào đi qua nhánh có u_code khách hợp lệ | `[MAJOR]` |
| G5 | Hồi quy: các thông báo lỗi khác của `orderChange` (u_code không tồn tại / chưa mua / `status_contract` 2, 3) không đổi + SP ẩn được báo **trước** "không lấy được thông tin khách" | diff code | không có (NEW-8 bản cũ đã đổi thành case link mua) | GAP | `[MAJOR]` |
| G6 | F5 — `viewEnterFriendInfo` (màn cùng mẫu, Dev lần 1 ghi "chưa bọc mặc định") | dev-impact | không có (NEW-11 đã xoá; REQ-005 còn active nhưng 0 TC) | GAP | `[MAJOR]` |
| G7 | BUG / F1 / F3 / T1 + diff "nhánh SP không tồn tại": mọi link của SP đã xoá phải báo 「この商品ページはすでに削除されています。」 (quy tắc chốt 2026-10-05) | dev-impact + diff code | NEW-1, NEW-2, NEW-3, NEW-4, NEW-12 (expected sai chuẩn — §4 C1–C3); NEW-7/8/9/10/15 (expected không có text — §5 I3) | RISK — có TC và đã PASS, nhưng đều chấm theo chuẩn cũ hoặc theo chuẩn mơ hồ, nên không còn kết luận được | `[BLOCKER]` |
| G8 | F6 / T1 — **link huỷ** (`orderCancel`) có u_code khách của SP đã xoá | dev-impact | NEW-16 (chỉ preview, expected không có text) | GAP — quy tắc chốt có nhắc link huỷ nhưng chưa TC nào mở link huỷ của khách | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 10 quan điểm Trigger khớp task (FUNC-001, DATA-REF-001, LIFF-ENTRY-001, MSG-USER-001, INTG-LINE-001, OUT-PREVIEW-001, REG-SHARED-001, REG-SPEC-001, COMPAT-LEGACY-001, ENV-003) · 4 quan điểm chưa đủ TC (ENV-003 ghi ở §5 I2 theo RULE-08).

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `COMPAT-LEGACY-001` | Cao | GAP — sản phẩm có 2 đời: V1 (`is_product_new=0`, có nút ẩn) và V2. Cả 15 TC chỉ dùng item V2. Chưa có TC cho trang đổi thẻ bản cũ (`SalesManagementController::orderChange`, Dev dùng làm mẫu đối chứng cho #42041) với item V1 bị xoá/ẩn (RULE-09) | `[BLOCKER]` |
| Q2 | `LIFF-ENTRY-001` | Cao | RISK — NEW-7/8/15 chỉ có 1 ô của ma trận (mở trong app LINE + đã kết bạn). Còn thiếu: chưa kết bạn · trình duyệt ngoài · mở từ deep-link `[CHANGE_{item_code}]` trong tin báo lỗi bill (`feature-spec.md:485`) | `[MAJOR]` |
| Q3 | `REG-SHARED-001` | Cao | RISK — 6 TC chỉ có Normal + Abnormal, không có Boundary và không ghi lý do (RULE-01). Thiếu case biên: khách đang mở form đổi thẻ thì admin xoá item, sau đó khách bấm 「変更する」 | `[MAJOR]` |
| Q4 | `REG-SPEC-001` | Cao | RISK — requirement đổi sau khi đã có TC (bỏ case ẩn, gộp #42041) nhưng chưa ghi 4 trạng thái cho các TC cũ. Nhãn trên Studio bị lệch: NEW-15 gắn REQ-006 nhưng test "link mua item đơn"; NEW-16 gắn REQ-007 nhưng test "trang huỷ đăng ký"; REQ-005/006/007 vẫn active nhưng không có TC nào test đúng nội dung | `[MAJOR]` |

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-8 | NEW-15 → **gộp** vào NEW-8 thành 1 TC dạng bảng (2 dòng: item chu kỳ / item đơn) | DUP-EXACT | Abnormal · LINE user mở lại link mua sau khi item bị xoá cứng · tiền đề tương đương · expected giống nhau từng chữ. Item đã xoá cứng nên `type_payment` không còn, cả 2 đi chung nhánh "không tìm thấy item" | `[MINOR]` |
| DUP-2 | NEW-9 | NEW-10 → **gộp** vào NEW-9 (2 dòng chu kỳ / đơn) | DUP-EXACT | Abnormal · admin xem trước trang mua của item đã xoá ở tab khác · expected giống nhau từng chữ. Cùng lý do xoá cứng như DUP-1 | `[MINOR]` |

- **Gate đã chạy**: khi gộp (không xoá) thì coverage ở §1/§2 vẫn giữ nguyên. Đề xuất **gộp** vì human chủ ý tách 2 loại item để dễ theo dõi, nhưng code không phân nhánh theo loại item sau khi đã xoá.
- Đã rà 15 TC. NEW-14/NEW-17 (mua 継続 / 単品 khi item còn tồn tại) **không** trùng nhau vì luồng thanh toán của 2 loại khác nhau. NEW-2 (đường dẫn 3) / NEW-3 **không** trùng vì NEW-3 đi qua điểm vào thật trên admin.

---

## 4. Mâu thuẫn trong TCs

> ✅ **Quy tắc human chốt ngày 2026-10-05 (giải quyết C1/C2/C3)**: khi **sản phẩm đã bị xoá**, user bấm bất kỳ link nào — **mua · đổi thẻ (change) · huỷ · preview** — đều phải báo lỗi **「この商品ページはすでに削除されています。」**.
> Lưu ý: SP bị **xoá cứng** (`s_items` không có `deleted_at`), nên hệ thống không phân biệt được "đã xoá" với "mã chưa từng tồn tại". Các TC dùng mã SP bịa vì vậy cũng phải ra cùng thông báo này.

Theo quy tắc trên thì **cả 2 bên của mâu thuẫn cũ đều sai expected**: NEW-1 ghi 「この**予約**ページ…」 (sai 1 chữ), còn NEW-2/3/4 cùng spec và kho đều ghi 「商品が非公開か、存在していません」. Riêng NEW-12 thì ghi expected là trang 404.

| # | Loại | TC liên quan | Nội dung check | Expected hiện tại | Chuẩn đã chốt | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-1 | Link đổi thẻ (có u_code) của SP đã xoá | popup 「この**予約**ページはすでに削除されています。」 | 「この**商品**ページはすでに削除されています。」 | Hoặc TC ghi sai chữ, hoặc **code đang hiện text của màn đặt lịch** (nếu đúng là màn hình thực tế thì đây là bug). Đã PASS ở run 2709 → cần chạy lại, soi đúng từng chữ | `[BLOCKER]` — TC tái hiện BUG | Dev |
| C2 | `CONF-SPEC` | NEW-2 (4 đường dẫn, gồm cả preview), NEW-3 (preview), NEW-4 (HTML), NEW-5 (bước 2) | Link đổi thẻ / preview của SP không tồn tại | khối 「エラー」 + 「商品が非公開か、存在していません」 | 「この商品ページはすでに削除されています。」 | Cả 4 TC **đã PASS với text cũ** → nếu code thật sự hiện 「商品が非公開か…」 thì **fix chưa đạt quy tắc** (bug). Nếu code hiện text mới thì AI chấm pass sai | `[BLOCKER]` | Dev |
| C3 | `CONF-SPEC` | NEW-12 | Link mua (enter-payment-info) của SP đã xoá | trang 404 sạch | 「この商品ページはすでに削除されています。」 | TC sai, hoặc code chưa đạt quy tắc ở luồng mua | `[MAJOR]` | Dev + Leader |
| C4 | `CONF-SPEC` | Spec FA-026 | Message cho item không tồn tại | `feature-spec.md:359`, `:926`: 「商品が非公開か、存在していません」 cho cả "không tồn tại" và `status_valid != 1` | Tách thành 2 message: xoá → 「この商品ページはすでに削除されています。」; ẩn → chờ S3 | Spec cũ hơn quy tắc → cần cập nhật spec | `[MAJOR]` | Dev |
| C5 | `CONF-KHO` | Kho FA-026 | Mở link SP đã xoá | `TC-BIL-04`, `TC-BIL-95`, `TC-BIL-122`: 「商品が非公開か、存在していません」 | 「この商品ページはすでに削除されています。」 | Kho cũ hơn quy tắc → cập nhật `kho-tcs/data/` rồi build lại | `[MAJOR]` | Leader |

**Đã rà**: 15 TC × `spec-features/admin/bill-item/feature-spec.md` (§2.4 EP-60/EP-63, bảng message, R23) + `kho-tcs/fa026-billtienitem-商品販売.md` (nhóm 9, 11, 17) + quy tắc human chốt 2026-10-05. NEW-7/8/9/10/15/16 không mâu thuẫn trực tiếp vì expected chưa ghi text — nhưng phải bổ sung text theo quy tắc (§5 I3).

⚠️ **Hệ quả**: 6 TC đang ghi PASS (NEW-1/2/3/4/12 + NEW-5 bước 2) không còn kết luận được theo chuẩn mới → các vùng `BUG` / F1 / T1 ở §1 hạ xuống **RISK** cho tới khi chạy lại.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ task | **Chưa chốt được code nào đã được test.** Có 2 branch fix không merge vào nhau: `ai_small_41004` có lớp bảo vệ ở view `$flagCycle ?? 0`; `ai_fixbug_41004` có fix nhánh `orderChange` + #42041. Studio đang chạy `ai_fixbug_41004`, nhưng 7 TC (NEW-1/2/3/4/5/6/12) vẫn ghi tiền đề "Đang chạy branch ai_small_41004". `dev_impact` xác nhận branch mới **không có** lớp `?? 0`, tức các màn cùng mẫu (xác nhận đơn / nhập thông tin bạn bè) không còn được bảo vệ | Dev/Leader chốt branch sẽ release (hoặc gộp cả 2) → sửa tiền đề của 7 TC trên Studio → chạy lại toàn bộ trên đúng branch |
| I2 | `[MAJOR]` | Toàn bộ | RULE-08 / ENV-003: 15/15 TC chỉ chạy trên staging, 0 TC trên production. Task chạm trang thanh toán, và exception gốc bắn trên `step.lme.jp` | Sau release, chạy 1 smoke chỉ đọc trên production (TC R1 ở §7) |
| I3 | `[MAJOR]` | NEW-7, NEW-8, NEW-9, NEW-10, NEW-15, NEW-16 | Expected không đo được: "hiển thị trạng thái/thông báo cho biết item hoặc trang không còn tồn tại" — không có text cụ thể, nên không bắt được việc hiện sai thông báo (đúng loại lỗi ở C1/C2) | Sửa expected trên Studio thành đúng text theo quy tắc chốt 2026-10-05: 「この商品ページはすでに削除されています。」, rồi chạy lại |
| I4 | `[MAJOR]` | NEW-7, NEW-8, NEW-15 | Tiền đề không dựng lại được: không ghi bot, cách lấy link (URL LIFF `type=product-change`/`product-detail` hay deep-link `[CHANGE_…]`), trạng thái hợp đồng của LINE user ("đăng ký phù hợp") | Ghi rõ bot test, dạng URL, `status_contract`/`status_bill` của user |
| I5 | `[MAJOR]` | NEW-1, NEW-2, NEW-3, NEW-4, NEW-5, NEW-12 | Expected trái quy tắc chốt 2026-10-05 (§4 C1–C3), và cả 6 đã PASS theo chuẩn cũ | Sửa expected trên Studio (`testcase_update`) → chạy lại. TC nào vẫn ra 「商品が非公開か…」 / 「この予約ページ…」 / 404 thì raise bug cho Dev, không sửa expected cho khớp code |
| I6 | `[MAJOR]` | F7 — `orderCancel` / `changeCardItem` / `changeCardUnivapay` | Dev ghi "yokoten, chưa sửa": các endpoint này không kiểm `status_valid`, nên khách vẫn POST đổi thẻ / huỷ được với SP ẩn, khác với trang đổi thẻ vừa chặn | PO/Dev chốt có sửa theo không (§8). Nếu không sửa thì ghi rõ là ngoài phạm vi |
| I7 | `[MINOR]` | NEW-5 | `skip` — tiền đề yêu cầu local (đọc log) nhưng lại chạy trên staging. Đây là TC duy nhất kiểm "không còn exception trong log" | Chạy trên local, hoặc thay bằng kiểm room Chatwork `SNSLineException` (xem R1) |
| I8 | `[MINOR]` | NEW-17 | Thiếu `Mã quan điểm liên kết` (viewpoint trống) | Gán `REG-SHARED-001` |
| I9 | `[NIT]` | NEW-4 | Expected chỉ ghi "không 5xx", hợp lệ theo ngoại lệ phủ định của RULE-13. Tuy vậy bảng 1.1 quy ước "dữ liệu không tồn tại → 404", trong khi code đang trả 200 | Ghi mã cụ thể khi PO chốt (§8) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 15 TC — không có TC nào ngoài phạm vi task. NEW-9/10/12/14/17 nằm trên `viewEnterPaymentInfo` / `confirmOrder`, là các caller Dev đã kê ở mục 3; NEW-16 (`orderCancel`) cũng nằm trong danh sách caller Dev đã check → đây là regression có căn cứ.

---

## 7. TCs đề xuất bổ sung (6)

> ✅ **Đã sync lên Studio task #360 (2026-10-05)**: TC-DATAREF001-01 → NEW-19 · TC-REGSHARED001-04 → NEW-20 · TC-REGSHARED001-05 → NEW-21 · TC-REGSHARED001-06 → NEW-22 · TC-LIFFENTRY001-01 → NEW-23 · TC-ENV003-01 → NEW-24.
> Đã loại theo quyết định human: TC-REGSHARED001-03, TC-COMPATLEGACY001-01, TC-COMPATLEGACY001-02 (cùng 3 TC sản phẩm ẩn loại trước đó). TC-REGSHARED001-07 (submit đổi thẻ sau khi xoá) không sync vì trùng NEW-18 (human tạo 11:22).

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa026-billtienitem-商品販売.md` (nhóm 9, 11, 17) |
| Vùng regression phát hiện từ kho | Nhóm 17 "LINE user — đổi thẻ" (TC-BIL-175…180), TC-BIL-115 (old friend chưa mua mở link đổi thẻ → 未購入), TC-BIL-120 (bot hết hạn → 410) |
| Conflict expected vs kho | Kho TC-BIL-04/95/122 trái quy tắc chốt 2026-10-05 → C5 (§4 + §8). TC đề xuất viết theo quy tắc mới |
| GAP dùng lại TC kho | Không — TC-BIL-115/120 chỉ dùng để dẫn chiếu data, kho chưa có case nào cho trang đổi thẻ với SP xoá/ẩn |
| Căn cứ TC regression `R<x>` | R1: exception gốc bắn trên `step.lme.jp` (room SNSLineException) + ENV-003 |
| Xác nhận chống trùng | Đã đối chiếu 15 TC ở BƯỚC 0 + kho FA-026 — không TC đề xuất nào trùng |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-DATAREF001-01 | UI | DATA-REF-001 | Link mua / đổi thẻ / huỷ / preview của SP đã xoá | Abnormal | auto | dev, local, prd, staging | SP định kỳ đã xoá: mọi link (mua · đổi thẻ · huỷ · preview của cả 3) đều báo 「この商品ページはすでに削除されています。」 | - Bot A còn hạn, Stripe test<br>- SP-X 継続 「TC41004-DEL」, F1 đang hợp đồng SP-X (`status_contract=1`)<br>- Đã ghi lại item_code + u_code F1 trước khi xoá | 1. Lúc SP-X còn tồn tại: mở 3 link với u_code F1 để xác nhận mở được<br>2. Xoá SP-X (••• →「削除」→「削除する」)<br>3. Lần lượt mở 6 link trong cột Dữ liệu nhập bằng trình duyệt<br>4. Với mỗi link, đọc thông báo + kiểm không có form | 1. `/v2/order-item/detail/<item_code>/<u_code F1>` (mua)<br>2. `/v2/order-item/change/<item_code>/<u_code F1>` (đổi thẻ)<br>3. `/v2/order-item/cancel/<item_code>/<u_code F1>` (huỷ)<br>4-6. 3 link trên với `/preview` thay cho u_code | Cả 6 link: hiện đúng từng chữ 「この商品ページはすでに削除されています。」; KHÔNG có form mua / 「契約中の商品」 / nút 「変更する」 / nút huỷ; KHÔNG có 「この予約ページ…」, 「商品が非公開か…」; không 500 / Whoops; link preview không hiện dòng 「この画面はプレビューとなります。」 |  | Lấp G7 + G8 · Chuẩn: quy tắc human chốt 2026-10-05 · Môi trường: cả 4 env (trên prd chỉ dùng SP test tự tạo rồi xoá) · Đánh giá spec: Đã hỏi leader (spec FA-026 còn ghi text cũ — §8 S1) · Evidence: screenshot 6 link · TC này thay cho expected đang sai/mơ hồ của NEW-1/2/3/7/8/9/10/15/16 — nếu sửa xong các TC đó thì có thể bỏ TC này |
| TC-REGSHARED001-04 | UI | REG-SHARED-001 | Trang đổi thẻ v2 | Normal | auto | dev, local, prd, staging | Khách đã đăng ký SP định kỳ công khai mở link đổi thẻ → vẫn thấy form đổi thẻ | - Bot A, SP-C 継続 công khai<br>- F1 có `status_contract=1` + `status_bill=1` cho SP-C | 1. Mở `/v2/order-item/change/<item_code SP-C>/<u_code F1>`<br>2. Quan sát | item_code SP-C · u_code F1 | Hiện 「契約中の商品」 với tên SP-C, 「変更カード情報入力」, nút 「変更する」; KHÔNG có 「この画面はプレビューとなります。」, 「エラー」, 「申込済みの商品です」. Không bấm 「変更する」 |  | Lấp G4 · regression · Môi trường: cả 4 env (chỉ đọc, không submit) · Đánh giá spec: Spec ghi rõ (`feature-spec.md:482-500`) · Evidence: screenshot |
| TC-REGSHARED001-05 | UI | REG-SHARED-001 | Trang đổi thẻ v2 — thông báo lỗi | Abnormal | auto | dev, local, staging | Các thông báo lỗi khác của trang đổi thẻ không đổi sau fix | - Bot A, SP-C 継続 công khai<br>- F3 chưa từng mua SP-C · F4 `status_contract=2` · F5 `status_contract=3` | Lần lượt mở `/v2/order-item/change/<item_code SP-C>/<u_code>` với từng dòng dữ liệu | Dòng 1: `tc41004nouser` · Dòng 2: u_code F3 · Dòng 3: u_code F4 · Dòng 4: u_code F5 | - Dòng 1: 「…お客様情報を取得できませんでした」<br>- Dòng 2: 「この商品は購入されていません。」<br>- Dòng 3: 「既にキャンセルしました。」<br>- Dòng 4: 「キャンセル済です」<br>- Mọi dòng: khối 「エラー｜<tên SP-C>」, không form, không 500 |  | Lấp G5 · regression · Căn cứ: `dev_impact` "các thông báo lỗi khác của orderChange không đổi" + kho TC-BIL-115 · Môi trường: dev/local/staging (dựng trạng thái hợp đồng bằng DB) · Đánh giá spec: Spec ghi rõ (`feature-spec.md` bảng status_contract) · Evidence: screenshot 4 dòng |
| TC-REGSHARED001-06 | UI | REG-SHARED-001 | Trang nhập thông tin bạn bè v2 (enter-friend-info) | Abnormal | auto | dev, local, prd, staging | Trang nhập thông tin bạn bè (màn cùng mẫu) với SP đã xoá → không lỗi 500; SP còn tồn tại → form bình thường | - Branch release đã chốt (I1)<br>- SP-F còn tồn tại thuộc bot A<br>- Mã SP bịa `zz41004fi<thời gian>` | 1. Mở `/v2/order-item/enter-friend-info/zz41004fi<thời gian>/tc41004ucode`<br>2. Mở `/v2/order-item/enter-friend-info/<item_code SP-F>/preview` | mã bịa · item_code SP-F | - Bước 1: 「この商品ページはすでに削除されています。」, không 500, không có chuỗi 「Undefined variable」<br>- Bước 2: form nhập thông tin bạn bè + 「この画面はプレビューとなります。」, không có khối 「エラー」 |  | Lấp G6 · Bước 1 áp quy tắc chốt 2026-10-05 ("link mua"); nếu Leader coi trang nhập thông tin bạn bè không thuộc "link mua" thì expected là 404 sạch · Căn cứ: Dev lần 1 "màn cùng mẫu chưa bọc mặc định" + `dev_impact` "branch mới không có `?? 0`" · Môi trường: cả 4 env (chỉ đọc) · Đánh giá spec: Spec ghi rõ EP-65 · Evidence: screenshot |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | Link đổi thẻ phía LINE user | Abnormal | manual | dev, local, prd, staging | Ma trận điểm vào cho link đổi thẻ của SP đã xoá: chưa kết bạn / trình duyệt ngoài / deep-link trong tin báo lỗi bill | - SP-D 継続 đã có link LIFF `type=product-change` và tin báo lỗi bill chứa `[CHANGE_<item_code>]`<br>- Tài khoản LINE L1 đã kết bạn, L2 chưa kết bạn<br>- Xoá SP-D sau khi đã gửi link | 1. L1 mở link LIFF từ app LINE<br>2. L1 copy link, mở bằng Safari/Chrome ngoài LINE<br>3. L2 (chưa kết bạn) mở link LIFF<br>4. L1 bấm deep-link trong tin báo lỗi bill | Link LIFF `type=product-change` của SP-D | - Bước 1, 2, 4: không 500; hiện 「この商品ページはすでに削除されています。」, không form<br>- Bước 3: chuyển sang màn kết bạn của OA |  | Lấp Q2 · manual vì cần app LINE thật trên điện thoại + tài khoản chưa kết bạn · Đánh giá spec: Spec ghi rõ luồng LIFF (`feature-spec.md:346-360`, `:485`) · Evidence: 4 screenshot trên máy thật |
| TC-ENV003-01 | UI | ENV-003 | Trang đổi thẻ v2 — production | Abnormal | manual | prd | Smoke sau release trên production: link đổi thẻ với mã SP không tồn tại không còn 500 và không còn bắn exception | - Đã release lên `step.lme.jp`<br>- Có quyền xem room Chatwork `SNSLineException` | 1. Mở `https://step.lme.jp/v2/order-item/change/zz41004prd<thời gian>/tc41004ucode`<br>2. Mở thêm dạng `/preview` và dạng không u_code<br>3. Theo dõi room SNSLineException trong 24h sau release | Mã bịa (chỉ đọc, không tạo dữ liệu) | - Bước 1-2: 「この商品ページはすでに削除されています。」, không 500<br>- Bước 3: không có cảnh báo mới chứa 「Undefined variable: flagCycle」 |  | Lấp R1 · regression · Mã bịa = SP đã xoá vì xoá cứng · Căn cứ: exception gốc bắn trên `step.lme.jp` (ticket #41004) + RULE-08 · manual vì chỉ chạy trên prd và cần đọc Chatwork · Đánh giá spec: Spec ghi rõ · Evidence: screenshot + ảnh room Chatwork |

- Q4 (REG-SPEC-001): không đề xuất TC. Việc cần làm nằm trên Studio — sửa nhãn `requirement_keys` của NEW-15/NEW-16, tắt hoặc gán lại REQ-005/006/007, và ghi trạng thái `[Giữ nguyên]/[Cần sửa]/[Hết hiệu lực]` cho các TC đã đổi nội dung ngày 2026-10-05.

---

## 8. Spec update needed

| # | Nội dung cần chốt / cập nhật | Nguồn | Ai chốt |
|---|---|---|---|
| S1 | ✅ **Đã chốt 2026-10-05**: SP đã xoá → mọi link mua / đổi thẻ / huỷ / preview báo 「この商品ページはすでに削除されています。」. Việc còn lại: (a) Dev xác nhận code trên branch release ra **đúng** text này ở cả 6 điểm vào — staging đang hiện 「この予約ページ…」 (NEW-1) / 「商品が非公開か…」 (NEW-2/3/4) / 404 (NEW-12) → nếu đúng như vậy thì là bug của fix; (b) cập nhật spec FA-026 `feature-spec.md:359`, `:926` (tách message xoá và message ẩn); (c) cập nhật kho TC-BIL-04/95/122 qua `kho-tcs/data/` + build lại; (d) sửa expected NEW-1/2/3/4/5/12 + bổ sung text cho NEW-7/8/9/10/15/16 trên Studio | C1–C5 · G7 | Dev (a, b) · Leader (c, d) |
| S2 | Branch release cho #41004: `ai_small_41004`, `ai_fixbug_41004` hay gộp cả 2 (có giữ lớp `$flagCycle ?? 0` ở view không) | I1 | Dev + Leader |
| S3 | #42041: SP ẩn **không tạo được từ UI V2** (spec `:82`/`:729`), case ẩn đã loại khỏi test (2026-10-05). Dev xác nhận: (a) giữ hay gỡ nhánh `status_valid != 1` trong `orderChange` (code chết); (b) endpoint V1 `change-valid-item` (EP-33, không lọc `bot_id` — R12) có đổi được `status_valid` của item V2 không; (c) URL `/v2/order-item/change` có phục vụ item V1 không. Nếu (b) hoặc (c) là CÓ → case ẩn thành reachable, cần mở lại G1/G2 | G1 · G2 · T3 | Dev (+ PO nếu nhánh còn giữ) |
| S4 | F7 yokoten: `orderCancel` / `changeCardItem` / `changeCardUnivapay` có cần kiểm `status_valid` giống trang đổi thẻ không | I6 | PO + Dev |
| S5 | Bổ sung vào spec FA-026 §2.4 EP-63: thứ tự kiểm (SP không tồn tại → 410 → SP ẩn → hợp đồng) và quy tắc chặn SP ẩn ở trang đổi thẻ, sau khi S3 được chốt | G3 · `dev_impact` | Dev |
| S6 | Mã HTTP khi mở link sản phẩm không tồn tại: code đang trả 200, quy ước RULE-13 là 404 | I9 | PO |
