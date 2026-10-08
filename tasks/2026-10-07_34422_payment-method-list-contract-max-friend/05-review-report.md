# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #237 (ticket 34422, round 1, `reviewState=leader`) |
| Tổng số TC review | 14 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 2/3 mục có TC (`F1`, `T1` OK · `BUG` RISK) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (1 file `index.blade.php`, +3/−2) + mục 3 file 03 | 4/8 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 6/11 điểm đủ TC · 3 GAP (G2, G3, G4) · 1 RISK (G1 — tính ở cả 2 chiều).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — tái hiện đúng luồng KH: đổi chuyển khoản → trả tháng bằng thẻ qua UI thật (`PointSettingController::changeCard` ghi `payment_method_old`) | `dev-impact` + `diff code` | `NEW-1` (skip) | RISK — TC duy nhất đi luồng UI thật bị **skip**; 13 TC còn lại đều dựng dữ liệu bằng seed DB, nên chưa có bằng chứng luồng thật ghi đúng `payment_method_old` / `univa_last_four_card_old` như seed giả định | `[MAJOR]` |
| G2 | `PointSettingController::changePaymentMethod` (file 03 mục 3 #6) — chiều thẻ → chuyển khoản qua UI thật | `diff code` | `NEW-3` (chỉ seed DB) | GAP — 0 TC đi luồng đổi thật; nhánh này quyết định 4 số cuối thẻ CŨ mà fix đọc | `[MAJOR]` |
| G3 | Rủi ro Studio `dev_impact`: *"job `HandleBillMaxFriend` thu phí max-friend theo `payment_method` MỚI, có thể mâu thuẫn với hướng hiển thị phương thức cũ"* | `diff code` | không có | GAP — chưa TC nào cho ca khoản max-friend **đã thực sự bị thu bằng thẻ mới** trong kỳ chuyển tiếp (kỳ max-friend tới trước ngày hết hạn hợp đồng chính). Đúng điểm Dev xin chốt hướng | `[BLOCKER]` |
| G4 | File 03 mục 2: *"màn chi tiết phí theo số bạn bè cũng còn đọc phương thức mới — ngoài phạm vi ticket"* (câu 5 BƯỚC 2) | `diff code` | `NEW-12` (chỉ màn chi tiết hợp đồng chính) | GAP — quy tắc đã chốt 07/10 *"hai dòng phải đồng nhất"* nhưng nhánh Dev nói "không sửa" có thể **đang sai sẵn**: list hiện 「銀行振込」, màn chi tiết của dòng max-friend hiện thẻ. Kèm 1 dòng §8 | `[MAJOR]` |

> G1 không đẻ TC mới (BƯỚC 5b — `NEW-1` đã đúng nội dung): **chạy `NEW-1`** (manual, staging) rồi mới kết luận BUG.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 12 quan điểm Trigger khớp task · 3 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `OUT-TRUTH-001` (+ `PAY-BATCH-001`) | Cao | RISK — có Normal (`NEW-2`, `NEW-3`) + Boundary (`NEW-10`, `NEW-14`), **thiếu Abnormal** (RULE-01): job bill hợp đồng chính bằng thẻ mới **thất bại**. `NEW-10` / `NEW-14` cố ý không chốt kết quả job, nên không phân biệt được nhánh lỗi — trong khi Dev ghi `AutoPaymentJobUnivapay` xoá phương thức cũ *"sau khi thu tiền"* | `[MAJOR]` |
| Q2 | `COMPAT-LEGACY-001` | Cao | RISK — `NEW-4` / `NEW-5` chỉ là "hợp đồng chưa đổi phương thức", **không phải nhánh đời cũ**. Bill max-friend đã version-up (kho `TC-BLP-344`, `is_old_bill_max_friend` = 1 dùng thẻ riêng ở `bot_card_bill_friend`) → nhánh max-friend kiểu cũ chưa có TC (RULE-09) | `[MAJOR]` |
| Q3 | `PAY-STATE-001` | Cao | RISK — trục trạng thái dòng max-friend (đã thu / lỗi / chờ chuyển khoản / LOA đã huỷ) chỉ được cover bởi `NEW-7`, `NEW-8`, `NEW-9` mang mã Studio lạ (`UI-TABLE-001`, `TOOL-NEGCTRL-001`) → không tính là cover | `[MINOR]` |

> Q3 không đề xuất TC mới — nội dung `NEW-7` / `NEW-8` đã đúng; chỉ cần đổi `viewpoint` trên Studio sang `PAY-STATE-001`.

---

## 3. TC trùng lặp nội dung

Đã rà 14 TC, không phát hiện trùng lặp. (`NEW-12` gần bao `NEW-2` nhưng `NEW-2` còn kiểm nút 「請求書」 không hiện → không phải `DUP-SUBSET`.)

---

## 4. Mâu thuẫn trong TCs

Đã rà 14 TC × `spec-features/admin/detail-contract/{feature-spec.md, ui/ui-spec.md, db/db-mapping.md}` + `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm 15, 16, 33, 34). Không có `CONF-TC`, `CONF-KHO`, `CONF-IGNORE`. Kho `TC-BLP-166` / `TC-BLP-167` **cùng hướng** với TC (trước hạn hiện phương thức cũ, sau job hiện phương thức mới).

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | `NEW-1`, `NEW-2`, `NEW-3`, `NEW-7`, `NEW-12`, `NEW-13` | Cột 「決済方法」 trong kỳ chuyển phương thức | Hiện phương thức **cũ** (`payment_method_old`) đến khi job hợp đồng chính bill theo phương thức mới | `feature-spec.md` §4 Field Traceability #8: 「決済方法 = `bot_contracts.payment_method` + `univa_last_four_card` → 1→カード, 2→銀行振込」 · `db/db-mapping.md`: `payment_method_old` = *"Backup trước khi đổi — rollback only"* (không dùng hiển thị) | TC sai **hoặc** spec cũ hơn hành vi chủ ý từ 2026-01-14 (commit `f5b366217e`). Ủng hộ phía TC: SCR-DC-04 *"áp dụng từ kỳ thanh toán tiếp theo"*, kho `TC-BLP-166`, quyết định ghi trong Studio 07/10 | `[MAJOR]` (đúng rule của root cause, nhưng 3 nguồn độc lập cùng hướng TC nên không để BLOCKER) | PM / Leader |
| C2 | `CONF-SPEC` | `NEW-9` | Dòng max-friend của LOA đã huỷ / giải ước | 「Ghi lại nội dung ô, không kết luận bug」 — chấp nhận mọi giá trị | `ui/ui-spec.md` SCR-DC-01 cột 5: 「LOA đã huỷ/giải ước: hiển thị「-」」. Code dòng max-friend không có nhánh 「-」 (cả trước lẫn sau fix) | TC chưa có chuẩn **hoặc** spec cần ghi rõ ngoại lệ cho dòng max-friend | `[MAJOR]` | Dev / PM |

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Cả bộ (14 TC) | **RULE-08 / ENV-003**: task bill tiền (FA-031) nhưng 14/14 TC chỉ chạy `local`, 0 TC ở staging/prd. `NEW-10`, `NEW-13`, `NEW-14` còn khoá `env_scope = local`. Kho `TC-BLP-167` (job đổi phương thức) yêu cầu PRODUCTION | Chạy lại ít nhất `NEW-1`, `NEW-2`, `NEW-3`, `NEW-12` trên staging; với ca phụ thuộc job, quan sát 1 hợp đồng thật trên prd qua kỳ bill |
| I2 | `[MAJOR]` | Cả bộ (14 TC) | Thiếu đánh giá spec: `spec_status = null` ở 14/14 TC. Ghi chú `NEW-1`, `NEW-2`, `NEW-10`, `NEW-14` nói *"người dùng xác nhận 07/10/2026"* nhưng không ghi **ai** chốt — chính là chuẩn của toàn bộ expected | Ghi `Đã hỏi leader` + tên người chốt quy tắc 07/10 trên Studio |
| I3 | `[MAJOR]` | `NEW-6` | **RULE-13**: TC nhóm `api` gửi thẳng `POST /ajax/point-settings/get-data-contract` nhưng expected không ghi mã HTTP | Thêm `HTTP 200` vào expected |
| I4 | `[MAJOR]` | `NEW-9` | Expected không đo lường được với dòng max-friend ("ghi lại nội dung ô") mà kết quả vẫn **Đạt** | Chốt C2 trước, rồi sửa expected thành 1 giá trị cụ thể và chạy lại |
| I5 | `[MAJOR]` | `NEW-13` | Không atomic: 2 dataset độc lập (A transfer→card, B card→transfer) với 2 expected khác nhau trong 1 TC — 1 bên lỗi thì cả TC Không đạt, khó khoanh vùng | Tách thành 2 TC A / B |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 14 TC — không có TC nào ngoài phạm vi task (mọi TC đều chạm ô 「決済方法」 của dòng max-friend hoặc đường dữ liệu/điều kiện hiển thị của nó).

---

## 7. TCs đề xuất bổ sung (6)

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (nhóm 15 Đổi kỳ thanh toán · 16 Đổi phương thức · 33/34 Bill max friend) |
| Vùng regression phát hiện từ kho | `TC-BLP-169` hoàn tác đổi phương thức (hàm hoàn tác không có trong mục 3 của Dev) · `TC-BLP-343` / `TC-BLP-344` bill max-friend theo phương thức hợp đồng gốc + bot max-friend kiểu cũ |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không |
| Căn cứ TC regression `R<x>` | R1 ← kho `TC-BLP-169` |
| Xác nhận chống trùng | Đã đối chiếu 14 TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** (G1 dùng lại `NEW-1`, Q3 chỉ đổi mã) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-OUTTRUTH001-01 | UI | OUT-TRUTH-001 | Danh sách hợp đồng 契約情報・領収書: Đổi thẻ → chuyển khoản qua UI thật, ô 決済方法 dòng phí theo số bạn bè | Normal | auto | dev, local, prd, staging | Đổi phương thức thẻ → 銀行振込 qua UI (changePaymentMethod) — dòng gói chính và dòng phí theo số bạn bè cùng giữ 「カード決済（下4桁 1234）」 trước kỳ thanh toán tiếp theo | - Đăng nhập tài khoản 主管理者 của hợp đồng<br>- Hợp đồng standard, 年間一括払い, phương thức thẻ đuôi 1234, CHƯA từng đổi phương thức, 「正常」, còn hạn (次回決済日 = D, D sau hôm nay ≥ 30 ngày)<br>- LOA của hợp đồng có > 100.000 bạn bè, khoản phí theo số bạn bè đã thu xong → dưới dòng gói chính có dòng phí theo số bạn bè ở trạng thái 「正常」, có ô 「決済方法」 | 1. Mở 「契約情報・領収書」, ghi lại ô 「決済方法」 của 2 dòng (dòng gói chính + dòng phí theo số bạn bè)<br>2. Bấm 「契約詳細」 ở dòng gói chính<br>3. Bấm nút đổi phương thức sang 「銀行振込」<br>4. Xác nhận ở màn xác nhận, chờ modal hoàn tất<br>5. Quay lại 「契約情報・領収書」, tải lại trang<br>6. Đọc ô 「決済方法」 của 2 dòng<br>7. Bấm 「契約詳細」, đọc mục 「決済方法」 và dòng ghi chú bên dưới | Thẻ hiện hành đuôi 1234; đổi sang 銀行振込 | - Bước 4: đăng ký đổi phương thức thành công<br>- Bước 6: dòng gói chính = 「カード決済（下4桁 1234）」; dòng phí theo số bạn bè = 「カード決済（下4桁 1234）」 — 2 ô giống hệt, không ô nào hiện 「銀行振込」 (đổi chỉ áp dụng từ kỳ sau)<br>- Bước 7: 「決済方法」 = クレジットカード + ghi chú 「次回決済日：<D>から銀行振込に変更されます」 | | Lấp G2 · luồng đổi thật thay cho seed DB của `NEW-3` · Đánh giá spec: Spec ghi rõ (SCR-DC-04 "áp dụng từ kỳ thanh toán tiếp theo"; kho `TC-BLP-165`, `TC-BLP-166`) · Evidence: screenshot list trước/sau + màn chi tiết · prd: dùng hợp đồng test nội bộ, hoàn tác sau test |
| TC-OUTTRUTH001-02 | Job | OUT-TRUTH-001 | Danh sách hợp đồng 契約情報・領収書: Khoản phí theo số bạn bè đã bị job thu bằng thẻ MỚI trong kỳ chuyển tiếp | Boundary | auto | dev, local, prd, staging | Kỳ phí theo số bạn bè tới trước ngày hết hạn hợp đồng chính — job HandleBillMaxFriend thu bằng thẻ mới 4242, list vẫn hiển thị theo quy tắc đã chốt | - Đăng nhập tài khoản 主管理者<br>- Hợp đồng standard 年間一括払い đang 「銀行振込」, đã đăng ký đổi sang thẻ đuôi 4242 (kỳ chuyển tiếp: phương thức cũ = chuyển khoản, phương thức mới = thẻ 4242), 次回決済日 của hợp đồng chính = D1 (sau hôm nay 60 ngày)<br>- LOA > 100.000 bạn bè, khoản phí theo số bạn bè kiểu MỚI (dùng thẻ của hợp đồng), kỳ thu tiếp theo = hôm nay<br>- Job bill hợp đồng chính CHƯA chạy cho kỳ D1 | 1. Mở 「契約情報・領収書」, ghi lại ô 「決済方法」 của 2 dòng<br>2. Chạy job `handle:bill_max_friend` (lịch 06:00)<br>3. Mở 「決済履歴・領収書のダウンロード」, tìm giao dịch phí theo số bạn bè vừa phát sinh, đọc cột 「決済方法」<br>4. Quay lại 「契約情報・領収書」, tải lại trang, đọc ô 「決済方法」 của 2 dòng<br>5. Bấm 「契約詳細」 ở dòng gói chính, đọc mục 「決済方法」 | Thẻ mới đuôi 4242; kỳ phí theo số bạn bè = hôm nay; D1 = hôm nay + 60 ngày | - Bước 3: có giao dịch phí theo số bạn bè, 「決済方法」 = クレジットカード (下4桁 4242) (khoản này thật sự đã thu bằng thẻ mới)<br>- Bước 4 (theo quy tắc 07/10 "giữ phương thức cũ đến khi job hợp đồng CHÍNH bill theo phương thức mới; 2 dòng đồng nhất"): dòng gói chính = 「銀行振込」, dòng phí theo số bạn bè = 「銀行振込」<br>- Bước 5: 「銀行振込」 + ghi chú ngày áp dụng thẻ = D1 | | Lấp G3 · ⚠ expected bước 4 phụ thuộc §8 #3: Leader xác nhận quy tắc 07/10 vẫn áp dụng khi khoản max-friend đã thu bằng thẻ (nếu không → dòng phí theo số bạn bè phải hiện thẻ 4242) · căn cứ: Studio `dev_impact`, kho `TC-BLP-343` · Đánh giá spec: Spec không ghi (cần hỏi leader) · Evidence: log job + 決済履歴 + screenshot list · prd: quan sát ca thật khi kỳ max-friend tới trước ngày hết hạn hợp đồng chính, không chỉnh thời gian |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Chi tiết dòng phí theo số bạn bè (mở từ 「詳細を確認」 trên 契約情報・領収書): 決済方法 trong kỳ chuyển tiếp | Normal | auto | dev, local, prd, staging | Màn chi tiết của dòng phí theo số bạn bè hiển thị cùng phương thức với 2 dòng trên list trong kỳ chuyển chuyển khoản → thẻ | - Đăng nhập tài khoản 主管理者<br>- Hợp đồng standard 年間一括払い đang 「銀行振込」, đã đăng ký đổi sang thẻ đuôi 4242, còn hạn, job hợp đồng chính chưa bill theo phương thức mới<br>- LOA > 100.000 bạn bè, khoản phí theo số bạn bè đang LỖI thu → dòng phí theo số bạn bè có nút 「詳細を確認」 | 1. Mở 「契約情報・領収書」, đọc ô 「決済方法」 của dòng gói chính và dòng phí theo số bạn bè<br>2. Bấm 「詳細を確認」 ở dòng phí theo số bạn bè<br>3. Đọc mục 「決済方法」 trên màn chi tiết vừa mở<br>4. So sánh với 2 giá trị ở bước 1 | Phương thức cũ 銀行振込, thẻ mới đuôi 4242 | - Bước 1: 2 dòng = 「銀行振込」<br>- Bước 3: 「決済方法」 = 「銀行振込」, KHÔNG hiện thẻ 4242<br>- 3 nơi hiển thị cùng 1 giá trị | | Lấp G4 · Dev ghi màn này vẫn đọc phương thức mới, ngoài phạm vi #34422 → nhiều khả năng Không đạt; Leader quyết raise ticket riêng hay đưa vào phạm vi (§8 #3) · Input thiếu: spec chưa mô tả màn chi tiết của dòng phí theo số bạn bè · Đánh giá spec: Spec không ghi (cần hỏi leader) · Evidence: screenshot list + màn chi tiết |
| TC-OUTTRUTH001-03 | Job | OUT-TRUTH-001 | Danh sách hợp đồng 契約情報・領収書: Job bill hợp đồng chính bằng thẻ mới thất bại khi hết kỳ chuyển tiếp | Abnormal | auto | dev, local, staging | Hết hạn, job AutoPaymentJobUnivapay bill hợp đồng chính bằng thẻ mới bị từ chối — ô 決済方法 của 2 dòng theo quy tắc mốc "job đã bill theo phương thức mới" | - Đăng nhập tài khoản 主管理者<br>- Hợp đồng standard 年間一括払い đang 「銀行振込」, đã đăng ký đổi sang thẻ test LUÔN BỊ TỪ CHỐI của cổng UnivaPay (lấy số thẻ theo tài liệu test card mới nhất của UnivaPay — RULE-05; gọi 4 số cuối là XXXX), 次回決済日 = D<br>- LOA > 100.000 bạn bè, khoản phí theo số bạn bè đã thu xong (「正常」, có ô 「決済方法」)<br>- Môi trường cho phép đưa thời gian tới D | 1. Mở 「契約情報・領収書」, xác nhận 2 dòng = 「銀行振込」<br>2. Đưa thời gian tới D, chạy job bill hợp đồng (`AutoPaymentJobUnivapay`)<br>3. Mở 「契約詳細」 → khu 操作履歴, xác nhận có bản ghi bill bằng thẻ XXXX thất bại<br>4. Quay lại 「契約情報・領収書」, tải lại trang, đọc 「ステータス」 và 「決済方法」 của 2 dòng | Thẻ test bị từ chối của UnivaPay (đuôi XXXX); ngày D | - Bước 3: có lịch sử bill thẻ XXXX thất bại<br>- Bước 4: dòng gói chính 「ステータス」 = 「延滞中」<br>- Bước 4: 「決済方法」 của dòng gói chính = 「カード決済（下4桁 XXXX）」, dòng phí theo số bạn bè = 「カード決済（下4桁 XXXX）」 — giống hệt nhau (job đã bill theo phương thức mới, dù lỗi) | | Lấp Q1 · ⚠ Dev ghi `AutoPaymentJobUnivapay` xoá phương thức cũ "sau khi thu tiền" → nếu chỉ xoá khi thành công, thực tế 2 dòng sẽ còn 「銀行振込」; expected theo ghi chú `NEW-10` ("không phụ thuộc thành công/thất bại") — chờ §8 #3 · không chạy prd vì làm hợp đồng thật rơi vào 延滞中 (ngoại lệ RULE-08, Leader duyệt) · Đánh giá spec: Spec không ghi (cần hỏi leader) · Evidence: log job + 操作履歴 + screenshot list |
| TC-COMPATLEGACY001-01 | UI | COMPAT-LEGACY-001 | Danh sách hợp đồng 契約情報・領収書: Dòng phí theo số bạn bè KIỂU CŨ (thẻ riêng) trong kỳ chuyển chuyển khoản → thẻ | Normal | auto | dev, local, prd, staging | Bot có khoản phí theo số bạn bè kiểu cũ (is_old_bill_max_friend = 1, thẻ riêng đuôi 9999) — 2 dòng vẫn đồng nhất 「銀行振込」 trong kỳ chuyển tiếp | - Đăng nhập tài khoản 主管理者<br>- Bot có khoản phí theo số bạn bè từ TRƯỚC đợt improve bill max friend (kiểu cũ: thanh toán bằng thẻ riêng đuôi 9999, không dùng thẻ hợp đồng), đã thu xong, > 100.000 bạn bè<br>- Hợp đồng chính standard 年間一括払い đang 「銀行振込」, đã đăng ký đổi sang thẻ đuôi 4242, còn hạn, job hợp đồng chính chưa bill theo phương thức mới | 1. Mở 「契約情報・領収書」<br>2. Tìm LOA đối tượng<br>3. Đọc ô 「決済方法」 của dòng gói chính<br>4. Đọc ô 「決済方法」 của dòng phí theo số bạn bè | Thẻ riêng của khoản max-friend kiểu cũ đuôi 9999; thẻ mới của hợp đồng đuôi 4242 | - Dòng gói chính = 「銀行振込」<br>- Dòng phí theo số bạn bè = 「銀行振込」<br>- Không ô nào hiện 「下4桁 9999」 hay 「下4桁 4242」 | | Lấp Q2 · nhánh đời cũ của bill max friend (RULE-09), căn cứ kho `TC-BLP-344` · expected theo quy tắc 07/10 "2 dòng đồng nhất" — nếu Leader muốn dòng kiểu cũ hiện thẻ riêng thì sửa expected · Đánh giá spec: Spec không ghi (kho MT-26 còn chờ quyết định) · Evidence: screenshot list · prd: dùng bot cũ có sẵn, chỉ đọc |
| TC-STATEDEP001-01 | UI | STATE-DEP-001 | Chi tiết hợp đồng 契約詳細 → 契約情報・領収書: Hoàn tác đổi phương thức trước hạn, ô 決済方法 dòng phí theo số bạn bè | Normal | auto | dev, local, prd, staging | Hoàn tác đăng ký đổi thẻ → 銀行振込 trước ngày hết hạn — 2 dòng trên list cùng hiện lại 「カード決済（下4桁 1234）」 | - Đăng nhập tài khoản 主管理者<br>- Hợp đồng standard 年間一括払い thẻ đuôi 1234, đã ĐĂNG KÝ đổi sang 「銀行振込」, chưa tới 次回決済日<br>- LOA > 100.000 bạn bè, khoản phí theo số bạn bè đã thu xong (「正常」, có ô 「決済方法」) | 1. Mở 「契約情報・領収書」, ghi lại ô 「決済方法」 của 2 dòng<br>2. Bấm 「契約詳細」 ở dòng gói chính<br>3. Bấm nút hoàn tác đổi phương thức, xác nhận<br>4. Quay lại 「契約情報・領収書」, tải lại trang<br>5. Đọc ô 「決済方法」 của 2 dòng<br>6. Bấm 「契約詳細」, đọc mục 「決済方法」 | Thẻ đuôi 1234 | - Bước 1 và bước 5: 2 dòng = 「カード決済（下4桁 1234）」<br>- Bước 6: 「決済方法」 = クレジットカード, dòng ghi chú 「…から銀行振込に変更されます」 biến mất | | Lấp R1 · regression · dẫn từ kho `TC-BLP-169` · hàm hoàn tác cũng ghi `payment_method` / `payment_method_old` nhưng không có trong file 03 mục 3 · Đánh giá spec: Spec không ghi (kho có nguồn r557, r578) · Evidence: screenshot list trước/sau + màn chi tiết |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/detail-contract/feature-spec.md` §4 Field #8 · `ui/ui-spec.md` SCR-DC-01 cột 5 · `db/db-mapping.md` (`payment_method_old`) | Ghi rõ: trong kỳ chuyển phương thức, 「決済方法」 (dòng gói chính + dòng phí theo số bạn bè + màn chi tiết) hiện phương thức CŨ đến khi job hợp đồng chính bill theo phương thức mới; `payment_method_old` dùng cho hiển thị, không chỉ rollback | C1 `CONF-SPEC` | PM / Leader |
| 2 | `ui/ui-spec.md` SCR-DC-01 cột 5 | Dòng phí theo số bạn bè của LOA đã huỷ / giải ước hiển thị 「-」 hay phương thức thanh toán? | C2 `CONF-SPEC` | Dev / PM |
| 3 | Quy tắc chốt 07/10 (chưa có trong spec) | Phạm vi áp dụng: (a) khoản max-friend đã thu bằng thẻ mới trước hạn hợp đồng chính (G3); (b) màn chi tiết của dòng phí theo số bạn bè (G4 — trong hay ngoài phạm vi #34422); (c) job bill phương thức mới **thất bại** có tính là "đã bill" không (Q1) | G3 · G4 · Q1 (câu 5 BƯỚC 2) | Leader |
