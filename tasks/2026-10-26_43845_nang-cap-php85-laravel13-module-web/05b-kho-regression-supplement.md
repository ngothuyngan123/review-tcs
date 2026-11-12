# 05b — Đối chiếu kho-tcs ↔ task #43845 → TC regression bổ sung

> **Mục đích**: so khớp bộ TC task (Studio #507, 2198 TC) với **kho TCs tổng hợp** (`kho-tcs/`, 19 feature · 6.894 TC), **chỉ ở điểm nóng nâng cấp PHP 8.5 / Laravel 13**, để tìm vùng regression còn thiếu. File này là **deliverable phân tích bổ sung** (ngoài bộ 4 file chuẩn) — Leader review 1 lượt; TC được duyệt sẽ gộp vào `§7` batch tương ứng của `05-review-report.md` rồi mới `/sync-review-tc` push Studio. **File này KHÔNG tự push.**
>
> Làm **từng feature, ưu tiên rủi ro cao, DỪNG sau mỗi feature**. **Mọi TC đề xuất gộp ở 1 bảng duy nhất bên dưới** (cập nhật dần theo từng feature); phần "Căn cứ theo feature" giữ bảng đối chiếu + kết luận làm lý do. Cột `Verdict` (phần căn cứ): `COVERED` (task đã có) · `GAP-REG` (đẻ TC) · `CONF-KHO` (mâu thuẫn — nêu 2 khả năng, Leader chốt).
>
> **Điểm nóng (hotspot)**: `$`=tiền/decimal · `D`=ngày/Carbon JST · `C`=CSV · `E`=encoding · `P`=phân trang · `M`=media · `L`=LINE SDK/gateway lib · `S`=sort · `A6`=type juggling · `F2`=query builder mảng · `F13`=phân trang API.
>
> ⚠️ Khi push: tách theo batch — cột `Ghi chú` mỗi dòng mở đầu bằng **`[Bx]`** (batch nguồn). Gộp vào `§7` đúng batch đó của `05-review-report.md`. **ID TC ở đây đã chọn tránh trùng `client_ref` với §7 có sẵn** (vd B3a §7 đã dùng `TC-JOB001-01` → bảng này dùng `-02`/`-03`); trước khi push phải rà lại toàn bộ ID §7 các batch để chắc không đụng.
>
> ✅ **ĐÃ PUSH Studio #507 — 2026-10-30** (6/6 TC mới, `reused:false`): `TC-JOBBILL001-02`→NEW-2898 · `TC-FUNCDATE001-04`→NEW-2899 · `TC-OUTEXPORT001-02`→NEW-2900 · `TC-JOB001-02`→NEW-2901 · `TC-DATACASCADE001-01`→NEW-2902 · `TC-JOB001-03`→NEW-2903. ⚠️ `TC-FUNCDATE001-01` (campaign 初月無料) **đã đổi số → `TC-FUNCDATE001-04`** vì `TC-FUNCDATE001-01` đã bị §7 B4 (chi tiết bạn bè JST) chiếm trên Studio.

## Bảng tổng hợp TC đề xuất bổ sung (6)

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-JOBBILL001-02 | Job | JOB-BILL-001 | Job bill định kỳ 商品(継続) — job **quét kết quả** sau 15 phút đơn pending (UnivaPay Guzzle7) | Abnormal | manual | dev, local, prd, staging | job, api | Job bill kỳ tiếp gọi UnivaPay nhưng 15 phút chưa có kết quả → job quét kết quả tra trạng thái thật từ cổng và xử lý đúng theo success/fail, không bill trùng | Bot test gói trả phí, 1 HĐ sản phẩm 継続 bằng UnivaPay (thẻ test) tới kỳ gia hạn. Dựng được tình huống UnivaPay trả **pending/không kết quả trong 15 phút** cho lần charge của job. Có mốc hành vi production + kho TC-BIL-267. Đã deploy PHP8.5/Laravel13 | 1. Chạy job bill định kỳ cho HĐ → charge UnivaPay rơi vào trạng thái chưa có kết quả.<br>2. Chờ/kích job quét kết quả (sau mốc 15 phút).<br>3. Case A: cổng trả **success** — kiểm gia hạn kỳ + 決済履歴 + action + notify + tin LINE 「決済が完了しました」.<br>4. Case B: cổng trả **fail** — kiểm tăng đếm lỗi + action lỗi + 延滞, KHÔNG gia hạn.<br>5. Kiểm KHÔNG bill trùng (chỉ 1 giao dịch ở cổng).<br>6. So mốc production | HĐ 継続 UnivaPay, lần charge pending 15 phút | Job quét kết quả tra đúng trạng thái thật từ UnivaPay (Guzzle 7 parse response không lỗi): success → gia hạn kỳ + ghi 決済履歴 + gửi action/notify/tin LINE 決済完了; fail → đếm lỗi +1 + action lỗi + 延滞, không gia hạn. KHÔNG bill trùng. KHÔNG 500/TypeError PHP8 (F-10 Throwable) trong job. Trùng khít production | | **[B1]** Lấp GAP §23 — job quét kết quả 15 phút pending (kho TC-BIL-267); NEW-338/339/344 chỉ cover success/error đồng bộ · regression F5 Guzzle7/UnivaPay response parse + job runtime (F-10 `catch Throwable`) · dẫn từ kho TC-BIL-267 · manual vì cần UnivaPay test + dựng pending + prd · ENV chứa prd (RULE-08 bill tiền) · Đánh giá spec: Đã hỏi leader (hành vi production) |
| TC-FUNCDATE001-04 | Data | FUNC-DATE-001 | Campaign 初月無料 — Upgrade free→trả phí: `expired_date +1 tháng @23:59:59` + `初回決済日` biên cuối tháng (A2 Carbon) | Boundary | manual | dev, local, prd, staging | web | Upgrade qua campaign 初月無料 (bot đã verify, trong 7 ngày) → màn confirm hiện 初回決済日 = now+1 tháng + badge 1ヶ月分無料, sau upgrade expired_date = now+1 tháng @23:59:59; biên cuối tháng + khung 00:00–09:00 JST không lệch; ngoài campaign/chưa verify thì KHÔNG +1 tháng | Bot FREE **đã verify phía LINE**, trong **7 ngày** kể từ ngày tạo (has_campaign=1). 1 bot đối chứng: ngoài 7 ngày HOẶC chưa verify. Chuẩn bị case upgrade rơi vào **ngày cuối tháng** (vd 31/1, 30/x) và case trong khung **00:00–09:00 JST**. Có mốc hành vi production (Bug Tester #34889) + kho TC-BLP-354/355/356. Đã deploy PHP8.5/Laravel13 | 1. Bot campaign: mở màn campaign detail/confirm → ghi 初回決済日 + badge 「1ヶ月分無料！」 + số tiền (plan×chu kỳ).<br>2. Upgrade qua campaign (chọn plan) → kiểm DB: `expired_date_contract` = now + 1 tháng, giờ = **23:59:59**; `status_payment`=1; `plan_type` đúng; `bot_slots` có bản ghi.<br>3. Lặp bước 2 với case upgrade **ngày cuối tháng** → +1 tháng ra ngày đúng production (không lệch do Carbon-3 month overflow).<br>4. Lặp trong khung **00:00–09:00 JST** → ngày hết hạn KHÔNG lùi 1 ngày.<br>5. Negative: bot NGOÀI 7 ngày / CHƯA verify → upgrade KHÔNG cộng +1 tháng.<br>6. So từng giá trị với mốc production | bot free verified trong 7 ngày; bot đối chứng ngoài window/chưa verify; mốc ngày cuối tháng + khung 0–9h JST | Màn confirm hiện 初回決済日 = now+1 tháng + badge 1ヶ月分無料 + số tiền đúng. Sau upgrade: `expired_date_contract` = now+1 tháng @**23:59:59** (A2 Carbon addMonth + endOfDay đúng, biên cuối tháng không tràn sai, khung 0–9h JST không lùi ngày — Bug #34889), status_payment=1, plan_type đúng, bot_slots có bản ghi. Bot ngoài campaign/chưa verify: KHÔNG +1 tháng. KHÔNG 500/TypeError PHP8. Trùng khít production | | **[B1]** Lấp GAP §35 Campaign 初月無料 (kho TC-BLP-354/355/356/357); task không có TC campaign (grep chỉ ra signup LP NEW-1912/1927-1930) · regression A2 Carbon addMonth + endOfDay (Bug #34889) dưới PHP8/Carbon-3 · dẫn từ kho TC-BLP-354/355/356/357 · manual vì cần bot verify trong campaign window + dựng mốc ngày + prd (Bug gốc production) · Đánh giá spec: Spec không ghi (campaign KHÔNG có trong feature-spec — kho note ⚠; so mốc production) |
| TC-OUTEXPORT001-02 | API | OUT-EXPORT-001 | チャット設定 — CSV export lịch sử chat **vắt bảng năm** messages_2020→2026 (nhuận 2024, ranh giới DB) | Boundary | manual | dev, local, prd, staging | web, api | Export CSV lịch sử chat với khoảng thời gian trải NHIỀU năm (vắt các bảng messages_2024/2025/2026 + ngày nhuận 29/02/2024) → gộp đủ tin từ các bảng năm, không mất/trùng ở ranh giới, thứ tự + JST + encoding đúng base | Bot test có 1 hội thoại U-MULTI có tin ở **nhiều năm**: ≥1 tin 29/02/2024 (nhuận), tin cuối 2024, đầu 2025, cuối 2025, 2026 — nằm ở các bảng partition `messages_2024`/`messages_2025`/`messages_2026`. Tin có JP/emoji/xuống dòng/dấu phẩy. Có mốc file base release_step_20260930_v2 cùng dữ liệu + kho TC-CST-139→152. Đã deploy PHP8.5/Laravel13 | 1. Mở チャット設定 → チャットのCSVエクスポート.<br>2. Chọn khoảng thời gian **2024-01-01 → 2026-12-31** (vắt 3 bảng năm, gồm 29/02/2024).<br>3. Xuất, chờ xử lý, tải CSV.<br>4. Mở bằng trình đọc CSV + Excel JP: kiểm đủ tin từ cả 3 năm, có tin 29/02/2024, thứ tự thời gian liền mạch qua ranh giới năm, không mất/trùng tin ở giao bảng.<br>5. So cột/dòng/giờ/encoding với file base cùng dữ liệu.<br>6. Lặp với khoảng chỉ 1 năm để đối chứng | khoảng 2024→2026 (3 bảng messages_YYYY) + tin 29/02/2024 | CSV gộp **đủ tin** từ messages_2024/2025/2026 (query builder chọn đúng bảng partition theo năm — F2), tin **29/02/2024** (nhuận) không mất, thứ tự thời gian liền mạch qua ranh giới năm/bảng (không trùng/mất tin ở giao bảng), giờ JST không lệch 9h/đổi ngày, encoding JP/emoji/xuống dòng/dấu phẩy đúng ô — khớp file base. KHÔNG 500/TypeError PHP8 khi routing qua nhiều bảng năm | | **[B6]** Lấp GAP — CSV export chat vắt bảng năm messages_2020→2026 + nhuận 2024 + ranh giới DB (kho TC-CST-139→152, 14 TC); NEW-1357 chỉ test 1 khoảng (encoding/range), NEW-280 chỉ display cuộn qua năm — chưa có CSV vắt partition · regression F2 query builder (routing bảng messages_YYYY) + F4 Carbon year + A5 encoding + F13 · dẫn từ kho TC-CST-139→152 · manual vì cần dữ liệu nhiều năm + prd (RULE-08 CSV) · Đánh giá spec: Spec ghi rõ (FA-041 CSV export theo năm) |
| TC-JOB001-02 | Job | JOB-001 | フォーム作成 — リマインド: đặt lịch **đa item × đa step** (指定日時/経過時間) + job gửi đúng giờ JST (Bug #33245 all-items) | Boundary | manual | dev, local, prd, staging | job, line-friend, web | User trả lời form chọn nhiều item remind → đặt lịch cho TẤT CẢ item đã chọn × mỗi step thỏa giờ gửi (không sót item — #33245); job gửi đúng giờ JST, F01 nhận đủ số tin | Form F có **3 item remind** R1/R2/R3; **Setting remind 2 step**: step-A kiểu 指定日時 (ngày mai 10:00 JST), step-B kiểu 経過時間 (+1 giờ sau khi trả lời). Friend F01 (LINE thật). Có mốc base release_step_20260930_v2 + Bug KH #33245 (12/2025: chỉ tạo lịch item đầu). Đã deploy PHP8.5/Laravel13 | 1. F01 mở form F qua LIFF, trả lời có **chọn R1 + R2 (bỏ R3)**, submit.<br>2. Kiểm DB lịch remind: đặt lịch cho **CẢ R1 và R2** × mỗi step thỏa giờ gửi (KHÔNG chỉ R1 — #33245); R3 không có lịch.<br>3. Kiểm step-A lịch = ngày mai 10:00 JST; step-B = thời điểm trả lời + 1 giờ (経過時間).<br>4. Tới giờ (hoặc chạy job), kiểm F01 nhận **đúng số tin remind** trên LINE, nội dung đúng.<br>5. Trường hợp không chọn item remind → KHÔNG đặt lịch nào.<br>6. So mốc base | form 3 item remind, 2 step (指定日時 + 経過時間); chọn R1,R2 | Đặt lịch cho **TẤT CẢ item đã chọn (R1,R2)** × mỗi step thỏa giờ gửi — không sót item (Bug #33245 fixed); 指定日時 đúng 10:00 JST, 経過時間 = thời điểm trả lời + offset (Carbon add đúng, không lệch 9h). Job gửi đúng giờ, F01 nhận đủ số tin remind (SDK v12). Không chọn item → 0 lịch. KHÔNG 500/TypeError PHP8 (so sánh giờ Carbon). Trùng khít base | | **[B8]** Lấp GAP — form remind đặt lịch + job gửi (kho TC-FORM-283/286/287/288); task KHÔNG có TC form remind (chỉ lesson NEW-57 + popup) · regression D Carbon time-satisfaction + job nền + F6 SDK send; root cause Bug #33245 (chỉ tạo lịch item đầu) · dẫn từ kho TC-FORM-286/287 + memory feedback-reverse-spec-not-oracle (spec "max 1 remind" sai) · manual vì LINE thật + job + prd (RULE-08) · Đánh giá spec: Spec ghi rõ (FA-011 Setting remind) |
| TC-DATACASCADE001-01 | Data | DATA-CASCADE-001 | フォーム作成 — リマインド: sửa/xóa step + cascade (xóa form-result/form/LINE user) cập nhật đúng lịch chưa gửi | Normal | manual | dev, local, prd, staging | web, job | Sửa giờ step → lịch chưa gửi cập nhật, đã gửi giữ nguyên, không-còn-thỏa bị xóa; xóa step/form-result/form/LINE user → hủy lịch tương ứng; khôi phục form → đặt lại lịch nếu còn thỏa | Form F remind đã có lịch đặt cho U1: 1 lịch **đã gửi**, 1 lịch **chưa gửi**. U2 có lịch theo step khác. Admin web + friend U1/U2 (LINE). Có mốc base + kho TC-FORM-289/290/291/292. Đã deploy PHP8.5/Laravel13 | 1. Sửa giờ 1 step remind sang giờ mới (vẫn thỏa) → kiểm lịch **chưa gửi** của U1 cập nhật giờ mới, lịch **đã gửi** không đổi; sửa sang giờ **không còn thỏa** → lịch tương ứng bị **xóa**.<br>2. Xóa 1 step (confirm alert) → xóa setting step + lịch tương ứng của U1, lịch step còn lại giữ.<br>3. Xóa form-result của U1 → xóa toàn bộ lịch của result đó; xóa cả form → xóa lịch mọi result; xóa LINE user U2 → xóa lịch của U2.<br>4. Khôi phục form đã xóa → đặt lại lịch cho step còn thỏa giờ gửi.<br>5. So mốc base | form remind có lịch U1 (đã gửi + chưa gửi), U2 step khác | Sửa step: lịch **chưa gửi** cập nhật, **đã gửi** giữ nguyên, **không còn thỏa** bị xóa (kho TC-FORM-289). Xóa step/form-result/form/LINE user: hủy đúng lịch tương ứng, không đụng lịch khác (290/291). Khôi phục form: đặt lại lịch cho step còn thỏa (292). KHÔNG 500/TypeError PHP8 trong cascade (F2 query builder dưới Laravel13). Trùng khít base | | **[B8]** Lấp GAP — recompute/cascade lịch form remind (kho TC-FORM-289/290/291/292); task KHÔNG có TC form remind · regression F2 query builder cascade + D Carbon recompute giờ gửi dưới PHP8 · dẫn từ kho TC-FORM-289→292 · manual vì cần dựng lịch đã/chưa gửi + prd · Đánh giá spec: Spec ghi rõ (FA-011 Setting remind) |
| TC-JOB001-03 | Job | JOB-001 | テンプレート — Delay message (メッセージを1通ずつ数秒遅延): job gửi tin giãn cách qua `send_random_messages` + profile người gửi (Bug #38987) | Normal | manual | dev, local, prd, staging | job, line-friend, web | Group template bật delay → tin đầu gửi ngay, các tin sau vào `send_random_messages` giãn 2-5s, job gửi đúng thứ tự không duplicate; tên/profile người gửi đúng theo #38987 | Group template G_DELAY có 3 template con (text + panel/button), bật 「メッセージを1通ずつ数秒遅延させて送信する」 (`is_delay_message`=1). Có profile mặc định P0 + profile tùy chỉnh P1. Friend F01 (LINE thật). Worker queue chạy. Có mốc base + Bug KH #38987. Đã deploy PHP8.5/Laravel13 | 1. Gửi G_DELAY qua web (quick test) tới F01 với profile MẶC ĐỊNH P0.<br>2. Kiểm tin ĐẦU gửi ngay; 2 tin sau insert `send_random_messages` với `time_send` tăng dần +2-5s; job gửi đủ, đúng thứ tự template con, KHÔNG duplicate.<br>3. Kiểm trên LINE F01: mọi tin cùng tên người gửi, KHÔNG nhãn 「from アカウント名」 (#38987); `bot_profile_id`=NULL.<br>4. Lặp với profile TÙY CHỈNH P1 → mọi tin (kể cả tin giãn) hiện 「P1 from {tên OA}」, `bot_profile_id`=id P1.<br>5. Đối chứng delay OFF: 3 tin gửi cùng lúc, không sinh `send_random_messages`.<br>6. So mốc base | G_DELAY 3 tin (text+panel), delay ON/OFF; profile P0/P1 | Delay ON: tin đầu gửi ngay, 2 tin sau qua `send_random_messages` (`time_send` +2-5s mỗi tin), job gửi đủ đúng thứ tự, KHÔNG duplicate; SDK v12 build đúng loại tin (text/panel). Profile (#38987): P0 → không nhãn from + `bot_profile_id`=NULL; P1 → nhãn 「P1 from OA」 + `bot_profile_id`=P1. Delay OFF: 3 tin cùng lúc, 0 bản ghi delay. KHÔNG 500/TypeError PHP8 trong job gửi. Trùng khít base | | **[B3a]** Lấp GAP §35 Delay message (kho TC-TMT-348/354/355); task KHÔNG có TC delay (grep 0) — maincase template cũ không sweep delay · regression job `send_random_messages` (F-10 Throwable) + F6 SDK v12 + A2 `time_send` + profile resolution (Bug #38987) · dẫn từ kho TC-TMT-348/354/355 · manual vì LINE thật + job + prd (RULE-08) · Đánh giá spec: Spec không ghi chi tiết (so base + Bug #38987) |

---

# Căn cứ theo feature

## FA-026 商品販売 (Bill item) — batch B1 — T2 High

- **Kho**: `kho-tcs/fa026-billtienitem-商品販売.md` (381 TC / 34 section). Điểm nóng dev-impact áp: F5 Stripe v22/UnivaPay Guzzle7 · A3 tiền · A2 chu kỳ 継続 · C export 販売履歴 · M ảnh SP · L gateway/callback.
- **Task**: subset B1 (183 TC); đã đối chiếu kho theo 8 maincase ở `05-review-report.md` B1 §7 (2026-10-27) → đã ra G1 (TC-FUNC002-05 link SP đã xoá) + G2 (TC-DATADB001-01 mobile notify). Lần này soát **theo 34 section kho**, tập trung các section job/gateway/CSV chưa rà maincase.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC kho tiêu biểu | TC task tương ứng | Verdict |
|---|---|---|---|
| §22 Job bill định kỳ — 次回決済予定日 5 chu kỳ (毎週/毎月/3・6ヶ月/毎年) 🔥D | TC-BIL-254 | NEW-229 (次回決済予定日 theo ngày Tokyo tuần/tháng/cuối tháng) | **COVERED** |
| §22 Job bill định kỳ — charge Stripe kỳ tiếp 🔥$L | TC-BIL-252/253 | NEW-338 (job handle:bill_stripe thu kỳ tiếp) | **COVERED** |
| §22 Job bill định kỳ — charge UnivaPay kỳ tiếp + lỗi thẻ 🔥$L | TC-BIL-253/257 | NEW-344 (job thu UnivaPay: thành công + ghi lỗi thẻ) | **COVERED** |
| §22 Bill lỗi off-session / 延滞 / 決済履歴 lỗi 🔥$L | TC-BIL-257/258 | NEW-339 (bill_stripe off-session từ chối/cần xác thực), NEW-1107 (延滞中 + đơn lỗi 決済履歴, BR-07/BR-11) | **COVERED** |
| §22 Đổi thẻ khi đang nợ kỳ → thu lại ngay 🔥$L | — | NEW-1105 (UnivaPay), NEW-1115 (Stripe) | **COVERED** |
| §22 Callback hủy từ cổng → LME cập nhật 🔥L | TC-BIL-265 | NEW-1111 (webhook status=2 vẫn thu kỳ kế), NEW-331 (đổi thẻ định kỳ 3DS) | **COVERED** |
| §22 Biên ngày 31 → tháng sau ngắn 🔥D | TC-BIL-254 (cuối tháng) | NEW-546 (ngày đầu 31, tháng/năm sau ngắn) | **COVERED** |
| **§23 Job cứu đơn treo — bill xong 15 phút chưa có kết quả → job quét kết quả tra cổng** 🔥$L | **TC-BIL-267** | *(không thấy — NEW-338/339/344 chỉ success/error đồng bộ)* | **GAP-REG → TC-JOBBILL001-02** |
| §22 Số lượng > 1 → amount × quantity 🔥$ | TC-BIL-255 | *(không thấy TC chuyên biệt qty×price định kỳ)* | ứng viên biên (A3, Leader cân nhắc) |
| §22 決済終了 sau khi hết SỐ LẦN giới hạn 🔥 | TC-BIL-256 | *(không thấy)* | ứng viên biên (nghiệp vụ, ít PHP8) |
| §22 Concurrency: job đang bill dở → không bill trùng 🔥 | TC-BIL-266 | *(không thấy TC chuyên biệt)* | ứng viên biên (CONC, Leader cân nhắc) |
| §22 Đổi giá SP sau khi khách đăng ký → kỳ tiếp bill giá nào | TC-BIL-262 (MT-03) | — | **không đẻ** (spec-conflict MT-03 Stripe↔UnivaPay — thuộc kho, không phải regression nâng cấp) |
| §22 UnivaPay bỏ subscription → bill job như Stripe | TC-BIL-264 (MT-13) | NEW-344 (đã test job UnivaPay) | **COVERED** (migration đã phản ánh ở NEW-344) |
| §26 販売履歴 ngày/phân trang 🔥DP · §28 Export CSV lịch sử 🔥C$E · §29 Thuế 🔥$ | TC-BIL (26/28/29) | NEW-230/231/637/1560-1565 (history A2) · NEW-399/400/401/409 (CSV BOM/encoding) · NEW-638 (thuế PDF) | **COVERED** (B1 §2 A2/A3/A5/C "phủ dày") |
| §20/21 Bill UnivaPay callback & webhook · Bill Stripe tạo order trước 🔥$L | TC-BIL (20/21) | NEW-325-331/342/343/741/742 (pay/3DS/sub/receipt) | **COVERED** (B1 §2 B phủ dày) |
| §7 Ảnh SP (Intervention v3) 🔥M | — | NEW-180/182 | **COVERED** |

### Kết luận FA-026

FA-026 là feature **đã được cover tốt nhất** trong các batch (B1 "trưởng thành nhất"); bộ job bill định kỳ sản phẩm của kho gần như khớp hết TC task. Chỉ còn **1 GAP điểm nóng thật**: **job quét kết quả 15 phút** (đơn pending do UnivaPay/Guzzle7 chưa trả kết quả) — chưa có trong task, trong khi đây là mặt tiếp xúc lib nâng cấp (Guzzle 7 parse response + job runtime F-10 Throwable). → **TC-JOBBILL001-02** (bảng tổng hợp).

3 ứng viên biên (TC-BIL-255 qty×price · 256 決済終了 N-limit · 266 concurrency không bill trùng) thiên về **nghiệp vụ/CONC**, ít dính PHP8 trực tiếp → **không tự đẻ**, nêu để Leader quyết nếu muốn chặt hơn.

## FA-031 契約プラン・決済情報 (Bill tiền tool) — batch B1 — T2 High

- **Kho**: `kho-tcs/fa031-billtientool-契約プラン・決済情報.md` (398 TC / 40 section). Điểm nóng áp: A2 expired_date/kỳ thanh toán · A3 tiền/3DS/hoàn tiền · S+P list · L+D job bill/hủy · chuyển khoản.
- **Task**: subset B1; đã đối chiếu kho theo 8 maincase billing (B1 §7 2026-10-27, cluster 105 TC) → MC1 token · MC4 hủy 2 kiểu · MC6 mail STK · MC7 振込キャンセル · MC8 year-billing. Lần này soát **40 section kho**.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC kho tiêu biểu | TC task tương ứng | Verdict |
|---|---|---|---|
| §32 Ngày bill & expired_date — callback gia hạn cuối tháng/năm/tháng ngắn, JST 🔥D | TC-BLP (32) | NEW-225/226/227/229 (hạn HĐ cuối tháng/năm, JST), NEW-543/546/547/548 (biên 31, 00:00–09:00, 29–31 max-friend) | **COVERED** |
| §29/30 Job bill định kỳ thẻ/chuyển khoản + retry 🔥$DL | TC-BLP (29/30) | NEW-344/338 (job thu UnivaPay/Stripe), NEW-1539/1540 (bill cũ success/retry), NEW-866/864/1114 (retry <7 ngày/dọn đơn), NEW-678 (1 HĐ lỗi không chặn HĐ sau) | **COVERED** |
| §31 Job hủy HĐ & retry 🔥DL | TC-BLP (31) | TC-FUNC001-03 (hủy 2 kiểu — B1 §7), NEW-860 (bill lại 延滞 sát mốc cưỡng chế) | **COVERED** (mốc 延滞 cưỡng chế còn chờ chốt — B1 §8-6) |
| §33/34 Bill max friend — cảnh báo & upgrade / thanh toán & job 🔥$D | TC-BLP (33/34) | NEW-340/44 (job thu vượt 100.000 bạn), NEW-548 (bill bạn tối đa gói năm biên 29–31), NEW-544 (hạn chuyển khoản) | **COVERED** |
| §11 Hủy chuyển khoản 🔥$D · §10 Chuyển khoản tạo & STK 🔥$ | TC-BLP (10/11) | TC-FUNC001-04 (ma trận nút 振込キャンセル — B1 §7), TC-NOTIMAIL001-01 (mail STK), NEW-867 (お支払い開始日 = ngày tiền về) | **COVERED** |
| §25/26 Lịch sử thanh toán theo năm / tháng & lọc 🔥D$ · §27/28 領収書/見積書 🔥$ | TC-BLP (25-28) | NEW-637/1560-1565 (領収書/決済履歴 năm/lọc/sort/rỗng), NEW-481/482 (báo giá), NEW-638 (thuế PDF), NEW-1565 (năm rỗng) | **COVERED** |
| §9 Nhập thẻ & 3DS 🔥$L · §15/16 Đổi kỳ/phương thức thanh toán 🔥$D | TC-BLP (9/15/16) | NEW-326/331/543 (3DS/đổi thẻ/đổi phương thức), NEW-45/46 (nâng gói năm chia doanh thu A2) | **COVERED** (đổi-kỳ prorate ⊂ NEW-45/46 upgrade) |
| coupon → 次回決済日 = expired + 1 ngày 🔥D | — | NEW-1116/1119/1120/1126/1128 (coupon, modal, API) | **COVERED** |
| **§35 Campaign 初月無料 — upgrade cộng expired_date +1 tháng @23:59:59 + 初回決済日 (Bug #34889)** 🔥D$ | **TC-BLP-354/355/356/357** | *(không thấy — grep 初月無料 chỉ ra NEW-1912/1927-1930 = signup LP, KHÔNG phải campaign billing)* | **GAP-REG → TC-FUNCDATE001-04** |
| §35 Campaign — job ScanHasCampaign 02:00 set has_campaign | TC-BLP-358/359 | — | **không đẻ** (SpecImprove #33838 chuyển job sang **Java** — ngoài phạm vi module PHP web) |
| §37 Hoàn tiền HĐ 🔥$ | TC-BLP (37) | NEW-335/336 (refund — product/salon) | ứng viên biên (hoàn tiền cấp HĐ/downgrade — Leader cân nhắc) |
| §3 Sắp xếp, tìm kiếm & phân trang list HĐ 🔥SP | TC-BLP (3) | NEW-493/494 (解約一覧 sort + biên khoá trùng A1) | **COVERED** (sort A1 đã có; list HĐ dùng chung cơ chế) |

### Kết luận FA-031

Phần lớn FA-031 **đã cover tốt** (expired_date biên cuối tháng/JST · job bill+retry · max-friend · chuyển khoản/STK · lịch sử/領収書 · coupon). **1 GAP điểm nóng thật**: **Campaign 初月無料** — luồng upgrade PHP cộng `expired_date +1 tháng @ 23:59:59` (Bug #34889) + hiển thị `初回決済日 = now + 1 tháng`; đây là Carbon month-add + endOfDay, biên cuối tháng — điểm nóng A2 nặng, task **không có TC campaign**. → **TC-FUNCDATE001-04** (bảng tổng hợp). (Job has_campaign đã chuyển Java → bỏ. Hoàn tiền cấp HĐ là ứng viên biên, Leader quyết.)

## FA-020 サロン・面談予約 (+ FA-019 レッスン / FA-021 イベント) — batch B2 — T3 High

- **Kho**: `fa020-…` 497 TC/52 section · `fa019-…` 632 TC · `fa021-…` 375 TC. Điểm nóng áp: A2 slot/ca qua đêm/受付開始・締切/remind · $ 決済/返金/3DS · C ca CSV + Google Sheet · L Google sync/job/remind · F8 slot binding.
- **Task**: subset B2 (~152 TC booking). **B2 §7 đã đối chiếu kho đầy đủ theo maincase (2026-10-27)** — Salon 10 maincase → 6 TC, Lesson 8 → 2 TC, Event 6 → 1 TC (tổng **10 TC** trong §7 B2: TC-FUNC001-01/05, FUNC004-01→04, INTGCAL001-01, APICONTRACT001-01, STATE001-01, FRIEND001-02), bám memory salon-limit/#43379/google-cal/app-http/キャンセルリクエスト/overbook/lesson-friend-info-format.

### Bảng đối chiếu (section điểm nóng — lần soát section-level bổ sung)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §15 Hoàn tiền 返金 salon 🔥$ | NEW-336 (refund Stripe event/salon/lesson), NEW-2049 (salon UnivaPay refund), NEW-1256 (queue-mode refund) | **COVERED** |
| §41 決済 thẻ & 3DS 🔥$L | NEW-333 (salon 3DS approve-then-charge), NEW-2016/2017 (salon declined/3DS abort) | **COVERED** |
| §18 Ca qua ngày & biên 00:00 🔥D · §26 前後の空き時間 🔥D | NEW-38/39 (23:00→01:00, đệm không lấn ngày) | **COVERED** |
| §19 Ca làm việc CSV 🔥CD · §38/39 Google Calendar/Sheet 🔥CL | NEW-393/395 (Sheet 11/12 cột), NEW-385-388 (2 chiều + refresh token), salon shift CSV (MC7 ĐỦ) | **COVERED** |
| §29 予約の開始・締切 🔥D · §45 chọn slot 🔥D | NEW-40/41 (受付開始 N ngày biên) | **COVERED** |
| §25 受付上限 店舗・スタッフ · §24 自動割り当て 🔥D | TC-FUNC001-01, TC-FUNC004-02/03 (§7 B2 — option 1.1/1.2/合計/#43379) | **COVERED** (§7 B2) |
| §50 Job nền & monitor · §32/33 リマインド 🔥DL | NEW-1557 + cross-ref B3a (remind job) | **COVERED** |
| §42 現地決済 (trả tại chỗ) | *(không thấy)* | **không đẻ** (chỉ cờ pay-in-person, không charge online → không phải mặt gateway/PHP8) |

### Kết luận FA-020/B2

Cụm booking **đã được đối chiếu kho đầy đủ** (10 TC trong §7 B2 + A2/A1/A3/A4/A6/B/C "phủ dày" ở B2 §2). Soát section-level lần này: mọi section điểm nóng (返金/3DS/ca qua đêm/CSV/Google/受付開始・締切/受付上限/remind) **đều đã COVERED**. Chỉ 現地決済 chưa test nhưng không phải mặt PHP8 → **không đẻ TC**. → **0 TC bổ sung cho B2.**

## FA-001 1:1チャット + FA-041 チャット設定 — batch B6 — T4 High

- **Kho**: `fa001-…` 433 TC/44 section · `fa041-…` 262 TC/20 section. Điểm nóng áp: F7 socket JWT · F6 LINE SDK v12 push/reply/quote · C CSV chat theo năm · E chèn info/text JP · M media · D đặt lịch/delay · A2 giờ JST.
- **Task**: subset B6 chỉ **73 TC** — **B6 §7 = 0, CHƯA từng đối chiếu kho** (khác B1/B2/B4 đã có maincase). Đây là lần đối chiếu kho đầu tiên cho chat.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §40 Realtime socket & typing · socket JWT (F7) 🔥L | NEW-1347 (token socket + refresh 9' + bot-switch 403), NEW-249/253 (realtime JST) | **COVERED** |
| §16/23/25 Gửi text/template/reply + quote (F6 SDK v12) 🔥L | NEW-300 (push+quote), NEW-303 (reply postback), NEW-306 (push bạn chặn), NEW-516-521 (loại tin) | **COVERED** (representative) |
| §19/20/26 Gửi media/PDF + hiển thị (F6/M) 🔥M | NEW-11 (video/mp3→m4a), NEW-169/170 (ảnh resize/EXIF), NEW-304 | **COVERED** |
| C APP_KEY / channel_access_token 🔥 | NEW-307 (401→refresh channel_id/secret), NEW-308 (refresh fail → câu lỗi JP) | **COVERED** |
| §30/31/32 Đặt lịch gửi từ chat + delay & job 🔥DL | NEW-206/207/292/1083/1271 (送信予約/配信予約/delay — **lọt batch B2 §0 nhưng thuộc chat**) | **COVERED** (mis-batch, không đẻ lại) |
| §42 Lịch sử chat CSV — encoding/range 🔥CE | NEW-1357 (CSV JP/emoji/xuống dòng/range/JST), NEW-280 (cuộn tải tin cũ qua năm — display) | **COVERED** (encoding + display) |
| **§42 / FA-041 CSV export chat theo năm — vắt bảng messages_2020→2026 + nhuận 2024 + ranh giới DB** 🔥CDE | *(NEW-1357 chỉ 1 khoảng; NEW-280 chỉ display — không có CSV vắt partition nhiều năm)* | **GAP-REG → TC-OUTEXPORT001-02** |
| §17 Chèn friend info vào tin chat 🔥E | *(không thấy TC chat riêng)* | ứng viên biên — chung engine chèn-token với template (B3a FA-010 "Text—insert"); verify khi chạy B3a, nếu B3a không cover + friend_info array/object (A4) thì đẻ |
| §9-11 Quick action tag/status/block · §34-38 Rightbar · §41 bộ đếm 未確認 | NEW-293-298/415/158 (chat-setting/管理/badge), NEW-1358-1366 (effect cờ) | **COVERED** (representative) |
| §43/44 Giới hạn plan & token · Phân quyền staff | NEW (plan/token/perm trong 73 TC) | **COVERED** |

### Kết luận B6

Dù B6 §7=0 và chưa từng đối chiếu kho, **73 TC task + các TC scheduled-send lọt sang B2 thực tế đã phủ phần lớn điểm nóng chat** (socket F7, SDK v12 F6, APP_KEY, media, CSV encoding, scheduled-send). **1 GAP điểm nóng thật**: **CSV export lịch sử chat VẮT BẢNG NĂM** (messages_2020→2026, nhuận 2024, ranh giới DB) — là đường table-routing (F2 query builder chọn `messages_YYYY`) + Carbon year + encoding, KHÁC path NEW-1357 (1 khoảng) & NEW-280 (display). → **TC-OUTEXPORT001-02**. Chèn friend info vào tin chat (§17) để verify khi chạy B3a (chung engine insert-token).

## FA-011 フォーム作成 — batch B8 — T5/T9 Med

- **Kho**: `fa011-…` 481 TC/37 section. Điểm nóng áp: C export CSV SJIS/Google Sheet/job · E escape/liên kết info/JP · D **remind**/countdown/item ngày giờ · M upload file.
- **Task**: subset B8 chỉ **59 TC** — **B8 §7 = 0, CHƯA đối chiếu kho** (freshly-reviewed snapshot mới). Lần đối chiếu kho đầu tiên cho form.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §29 Export CSV SJIS 🔥CE | NEW-402/496 | **COVERED** |
| §30/31 Liên kết + Sync Google Sheet & job (32 TC kho) 🔥C | NEW-391/392/1030/1031/1035/1036/1039/1034 (OAuth/relink/resync/append job) | **COVERED** (representative) |
| §14 Item upload file · §33 LINE user nhập&submit media 🔥M | NEW-70/735/736/1334 + 12 TC #44065 (upload D-11 / read D-7) | **COVERED** (R1 NEW-70 media-read đang triage) |
| §18 Liên kết friend info & tag · §33 LIFF friend_info 🔥E | NEW-1056/1059/1061/1062 (LIFF friend_info field + 年月日 + action theo giá trị) | **COVERED** |
| §7 Public form escape/CSRF (A5) 🔥E | NEW-649/650/651/652/655 (escape 1 lần, CSRF) | **COVERED** |
| §6 Xóa & khôi phục + hard-delete câu trả lời | NEW-371 (khôi phục form, câu trả lời xóa KHÔNG quay lại — #4173) | **COVERED** (memory form-delete-answers-hard-deleted) |
| §16/24 診断 scoring | NEW-368/819/827 | **COVERED** |
| §4/8/19/20 Form CRUD v1/v2/v3 + 分岐 rẽ nhánh | NEW form CRUD/v3 + 分岐 | **COVERED** |
| **§15 Item remind + §23 Setting remind + job gửi (25 TC kho)** 🔥D | *(không thấy — NEW-57 là lesson remind; NEW-1038 chỉ cleanup remind khi xóa page, không phải đặt lịch/gửi)* | **GAP-REG → TC-JOB001-02 + TC-DATACASCADE001-01** |
| §26 Countdown form 🔥D | *(NEW-624/1197/1207/1198 là **popup** countdown, không phải form)* | ứng viên biên (countdown chủ yếu display-side JS; server chỉ tính deadline — Leader cân nhắc) |
| §11 Item ngày giờ 🔥D | NEW-1061 (LIFF 年月日) | **COVERED** (representative) |

### Kết luận B8

59 TC task phủ tốt CSV/Google Sheet/upload/escape/LIFF/診断/hard-delete. **1 cụm GAP điểm nóng thật: form リマインド** (Item remind + Setting remind + job gửi, ~25 TC kho) — task **0 TC** (chỉ có lesson/popup remind). Đây là cụm D (Carbon time-satisfaction) + job + F6 SDK + F2 cascade, lại **memory-backed** (feedback-reverse-spec-not-oracle "spec max-1-remind sai" + Bug KH #33245 "chỉ tạo lịch item đầu"). → **2 TC**: **TC-JOB001-02** (đặt lịch đa item×đa step + job gửi JST) · **TC-DATACASCADE001-01** (sửa/xóa step + cascade recompute). Countdown form là ứng viên biên (display-side) → không đẻ. Item ngày giờ cover representative qua LIFF 年月日.

## FA-010 テンプレート — batch B3a — T4 High

- **Kho**: `fa010-…` 394 TC/39 section. Điểm nóng áp: M media 3 nhóm · L quick-test/URL scheme/**delay** · E text/insert · D URL-expiry/delay · S sort/folder · P.
- **Task**: subset B3a (319 TC); **FA-010 đã đối chiếu kho theo 8 maincase** (B3a §7 2026-10-27) → 7/8 ĐỦ + 1 TC (TC-FUNCSEQ001-01 A1 sort). Lần này soát **section-level** các section nặng maincase không sweep (§18 URL-expiry, §35 delay).

### Bảng đối chiếu (section điểm nóng — bổ sung section-level)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §14-16 Text soạn/insert/PDF+shortenURL 🔥E · **§15 Text insert 友だち情報** | NEW-32 (insert 友だち情報 template), NEW-360/65/66 (insert/preview), NEW-1882 (không double-encode) | **COVERED** → đồng thời **chốt ứng viên B6** (chèn friend info chat = chung engine insert-token → không đẻ) |
| §7 Sort & search template (A1) 🔥S · §2/3 Folder | TC-FUNCSEQ001-01 (A1 sort/reorder — B3a §7), NEW folder CRUD | **COVERED** (B3a §7) |
| A5 encoding text (& < " ' / emoji) | TC-MSG001-01 (round-trip — B3a §7), NEW-1882/360 | **COVERED** (B3a §7) |
| §18 URL redirect — hết hạn & action (22 TC) 🔥D | NEW-566 (link nút/ảnh có hạn: chưa hết hạn mở đúng, hết hạn chuyển trang) | **COVERED** |
| §29/30/31 Media ảnh/image map/video&audio (Intervention v3) 🔥M | cụm #44065 (B3a R1 / B3b) — 98 TC gắn ticket | **COVERED** (cross-ref B3b #44065, đang [BLOCKER] triage) |
| §11-13 Quick test/preview · §19-27 Panel/Button/LINE URL scheme 🔥L | NEW send-test matrix + Panel/Button (319 TC) | **COVERED** (representative) |
| **§35 Delay message (メッセージを1通ずつ数秒遅延, 23 TC)** 🔥DL | *(grep 遅延/delay = 0 trong task — maincase template không sweep)* | **GAP-REG → TC-JOB001-03** |

### Kết luận FA-010

FA-010 Template **đã đối chiếu kho đầy đủ** (8 maincase, §7 B3a đã có TC-MSG001-01 encoding + TC-FUNCSEQ001-01 sort; insert-token NEW-32; URL-expiry NEW-566; media cross-ref #44065). **1 GAP section-level maincase cũ bỏ sót: §35 Delay message** — job `send_random_messages` giãn 2-5s + SDK v12 + profile người gửi (Bug #38987), task 0 TC. → **TC-JOB001-03**. Đồng thời **đóng ứng viên treo từ B6**: chèn friend info vào tin = chung engine insert-token đã cover ở NEW-32 → **không đẻ TC cho chat insert**.

## FA-004 リッチメニュー — batch B3b — T4 High

- **Kho**: `fa004-…` 488 TC/27 section. Điểm nóng áp: L đăng ký LINE/URL scheme · M ảnh (PNG alpha) · D job hiển thị/dừng theo lịch · S sort/folder.
- **Task**: subset B3b (142 TC). **B3b là batch bổ sung nhiều nhất (§7=14)** + FA-004 đã rà kho theo 10 maincase (G6 format → TC-MEDIA001-01, Q4 null → TC-FUNC002-03, G5 PNG-alpha gỡ theo F-6). Lần này soát section-level các section nặng còn lại.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §6 Step1 Ảnh (format/alpha/resize) 🔥M | TC-MEDIA001-01 (§7 B3b, G6 format), TC-FUNC002-03 (Q4 null), cụm #44065 | **COVERED** (§7 B3b) |
| §20/21 Setting hiển thị/dừng richmenu theo lịch 🔥D · §22 Lịch sử 🔥D | NEW-456 (hẹn giờ hiển thị + huỷ lịch 操作予約), NEW-577 (lịch sử sort 予約操作/実行日時), NEW-769 (điều kiện hiển thị + filter kịch bản/conversion) | **COVERED** |
| §23 Job hiển thị/dừng richmenu **fire** → SDK richMenu link/unlink 🔥DL | TC-FUNCSCHEDULE001-01 (§7 B3a — action-schedule cron fire có action "đổi rich menu" exercise SDK richMenu link); NEW-456 (setting+cancel) | **COVERED** (representative; job-fire-to-LINE = RISK-chạy-prd ở B3b §5, không phải GAP thiết kế) |
| §24 Thống kê tap 🔥L | NEW-1530 (maincase 8 ĐỦ) | **COVERED** |
| §25 Backup & đổi bot — richmenu re-register LINE 🔥L | TC-DATABACKUP001-01 (§7 B4 — rich menu re-register LINE API sau copy) | **COVERED** (cross-ref B4) |
| §13 Step3 LINE URL scheme 🔥L | cụm rich-menu-cluster + template URL scheme (FA-010 §24) | **COVERED** (representative) |
| §10 Action 友だち — text share 900 ký tự (post-encode) | kho MT-01/02 (đã chốt); validation FE/encode, không hotspot PHP8 mạnh | **không đẻ** (kho-internal conflict đã chốt; không phải regression nâng cấp) |
| §3/4 List + Tìm kiếm & sắp xếp (A1) 🔥S | TC-LIST001-01 (§7 B3b — A1 sort richmenu/QR/popup) | **COVERED** (§7 B3b) |

### Kết luận FA-004

FA-004 **đã đối chiếu kho rất đầy đủ** (14 TC §7 B3b + 10 maincase). Soát section-level: display-schedule setting/cancel/history covered (NEW-456/577/769); SDK richMenu link-on-fire cover representative qua TC-FUNCSCHEDULE001-01 (B3a) + re-register qua TC-DATABACKUP001-01 (B4); format/null/sort/media/thống-kê đã trong §7. Phần job-fire-to-LINE là **RISK-chạy-prd** (B3b §5 RULE-08), không phải GAP thiết kế. → **0 TC bổ sung cho FA-004.**

## FA-008 メッセージ配信 (broadcast) — batch B3a — T4 High

- **Kho**: `fa008-…` 345 TC/31 section. Điểm nóng áp: D 配信日時/edit-5-phút/job lifecycle · L job gửi/action/test-send · S+P list · M preview.
- **Task**: subset B3a (broadcast ~30+ TC, chưa maincase-kho riêng). Soát section-level toàn bộ hotspot.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §8/9 配信タイミング gửi ngay/đặt lịch · 配信日時追加 nhiều mốc (vắt 0h) 🔥D | NEW-206 (job Java gửi đúng giờ Tokyo + filter tag), NEW-207 (nhiều mốc vắt 0h = broadcast con), NEW-420 (2 mốc) | **COVERED** |
| §22 Edit broadcast & rule 5 phút 🔥D | NEW-466 (khoá sửa khi <5 phút tới giờ gửi — BR-05/06), NEW-1782 (sửa nháp gửi nội dung mới), NEW-1137 | **COVERED** |
| §25/26/27 Job gửi & vòng đời trạng thái / quá hạn-lỗi-resume / action sau gửi 🔥DL | NEW-510 (job gửi từng loại), NEW-1138 (friend lỗi job không dừng + notify 1 lần), NEW-1145 (ngày gửi con+filter job đúng giờ), NEW-1133 (đặt lịch trước deploy gửi 1 lần), NEW-1783 (xoá lịch trước giờ job không gửi), NEW-1784 (action gắn tag sau gửi) | **COVERED** |
| §17/18 配信先絞込み & 再計算 · 配信数 danh sách 🔥F2 | NEW-421/768/1041/1046/1139 (filter tag/kịch bản/conversion + recalc), NEW-1271/1272 (cột 配信数 mở danh sách lọc) | **COVERED** |
| §14 Ma trận đăng ký & gửi · IDOR V2 🔥L | NEW-737/738/739/740 (IDOR V2 ghi/đọc/sai-kiểu-id), NEW-1140-1145 (API bot A) | **COVERED** |
| §15/16 送信者名 profile khi gửi | NEW-1785/1786/1179 (profile nhân viên/mặc định khi gửi) | **COVERED** |
| §19/21 Preview 3 tab · テスト送信/一括テスト送信 🔥M L | NEW-511 (gửi thử từng loại), NEW-1788 (test chỉ tới tài khoản test) | **COVERED** |
| §5/6 Sắp xếp & lọc theo thời gian (A1/D) · Phân trang (P) 🔥SP | NEW-416 (3 tab lọc kỳ/số dòng/phân trang) | **COVERED** (representative) |
| §28/29 配信数上限アラート trigger & modal 🔥 | NEW-422 (modal cảnh báo vượt giới hạn tháng エルメ超過 → draft), NEW-1134 (modal đường vào 2), NEW-273 (quota header cache), NEW-2192 (notify setting) | **COVERED** (phần PHP) |
| §30 配信数上限アラート — **job cắt vượt quota** khi gửi (alert tin thứ 1.000) 🔥 | *(không thấy job-cut mid-send trong task)* | **không đẻ** (job gửi broadcast là **Java** — NEW-206; quota-cut/alert trong job Java ngoài phạm vi module PHP, như ScanHasCampaign FA-031; memory limit-notify-web-vs-job-scope) |

### Kết luận FA-008

Broadcast là một trong các vùng **cover rộng nhất** của task (schedule/edit-5-phút/job-lifecycle/filter/IDOR/profile/test-send/alert-modal đều có). 配信数上限アラート phần PHP (modal + quota display + notify) covered; phần enforcement/cut trong lúc gửi thuộc **job Java** → ngoài phạm vi upgrade PHP. → **0 TC bổ sung cho FA-008.**

## FA-003 自動応答 — batch B3a — T4 High

- **Kho**: `fa003-…` 285 TC/33 section. Điểm nóng áp: E keyword trim/match · D schedule 時間/曜日 · L runtime callback/action/retry · F9 binding SQL.
- **Task**: subset B3a autoreply (~45 TC) + nhiều TC mới.

### Bảng đối chiếu (section điểm nóng)

| Section kho (🔥) | TC task tương ứng | Verdict |
|---|---|---|
| §15/16 Keyword độ dài/trim · trùng/đồng bộ bảng keyword 🔥E | NEW-803/804/805/806 (từ khoá số "0"/"00"/khoảng trắng/trùng), NEW-1585/1586 (sửa keyword), NEW-1580 (trùng chặn) | **COVERED** |
| §18 Form スケジュール設定 (時間/曜日) 🔥D | NEW-49/51 (khung giờ hợp lệ/đảo/qua nửa đêm), NEW-500/502/503/807 (thứ/Chủ nhật), NEW-557 (API khung giờ biên) | **COVERED** |
| §27/28 Runtime nhận message & callback · match keyword & gửi action 🔥EL | NEW-515 (từ khoá → từng loại tin, job), NEW-945 (keyword khớp → action+notify), NEW-1570-1577 (match AND/partial/nhiều lần) | **COVERED** |
| §9-12 Filter (tag/ステップ/conversion/QR/友だち情報) 🔥F2 | NEW-770 (filter kịch bản job chỉ trả bạn thoả), NEW-1587/1588 (tag), NEW-555 (day_filter trống) | **COVERED** |
| §21-24 Action (友だち情報/テンプレート/ステップ/リッチメニュー/リマインド/tag/block) 🔥L | NEW-515 + cross-ref action chains (template/richmenu/remind đã cover ở FA-010/FA-004) | **COVERED** (representative) |
| §29 Runtime 自動確認済み · §30 friend block/ẩn 🔥 | NEW-1364/1365/2065-2069 (auto-confirm theo loại), NEW-939/940/946 (block対象 chỉ chạy cho block) | **COVERED** |
| F9 binding SQL text/id auto_reply (abnormal ký tự đặc biệt) 🔥 | TC-FUNC001-06 (§7 B3a — keyword chứa `% _ \ "` không mis-match/injection) | **COVERED** (§7 B3a) |
| §31 Runtime lỗi gửi & retry 🔥L | NEW-515/945 (gửi action); retry cross-ref token-refresh NEW-307/308 (chat) | **COVERED** (representative) |

### Kết luận FA-003

Autoreply **cover cực đầy đủ** ở mọi section điểm nóng (keyword E, schedule D, runtime/filter/action L, binding F9 qua TC-FUNC001-06). → **0 TC bổ sung cho FA-003.**

## FA-007 あいさつメッセージ — batch B3a/B7 — T4 High · 0 TC mới

- **Kho** `fa007-…` 172 TC/20 section. Điểm nóng: L follow/unblock/QR action callback · job callback follow chống trùng · M QR/video.
- Task cover đầy đủ: kết bạn mới/cũ/unblock + tin+action (NEW-139/140/141/143/144/145 + E2E), video greeting .mov→.mp4 (NEW-1356/553), **3 nguồn kết bạn (thường/landing/unblock) action đủ không sót** (NEW-929), webhook follow/unfollow/join (NEW-244), giới hạn 5000 ký tự (NEW-142), ưu tiên QR + add_friend_setting fallback (TC-LIFFENTRY001-03 §7 B3b), edge bot hủy HĐ/LME dừng OA (NEW-923/930). → **0 TC mới.**

## B9 Job / Queue / Cron — 0 TC mới

- Cross-cutting (job rải theo nhiều FA). Batch **sạch nhất** (0 fail/0 error, §7=0). Mọi hotspot job covered: A2 diffInDays job (NEW-44/47/48), A3 bill job (NEW-338/339/340/344), queue drain payload 5.5→13 (NEW-204/205), log channel (NEW-203), scheduler JST 51 lịch (NEW-202/671/672), batch-error F-10 (NEW-674), lock job (NEW-278), CSV job SJIS (NEW-405/404). Job-level gap của từng feature đã được bắt ở 05b (TC-JOB001-02 form remind · TC-JOB001-03 delay · TC-JOBBILL001-02 bill · TC-FUNCSCHEDULE001-01 action-schedule §7 B3a). → **0 TC mới.**

## B10 Mail / Notify / Push — 0 TC mới (đã có 2 TC ở §7 B10)

- F12 (SwiftMailer→Symfony Mailer + webpush 13 + FCM) covered toàn diện (routing/SMTP tls-ssl/timeout/MIME JP/VAPID/push_subscriptions/3 kênh App-PC-ChatWork/null-safe). 2 GAP thật **đã nằm sẵn ở §7 B10**: `TC-NOTIMAIL001-02` (deliverability mail đăng ký/2FA/reset — Spam/DKIM) + `TC-NOTIMAIL001-03` (notify trần 100% web-vs-job, memory limit-notify-web-vs-job-scope). Mail chuyển khoản đã có TC-NOTIMAIL001-01 (§7 B1). → **không phát sinh TC mới ngoài §7 B10 có sẵn.**

---

# Tổng kết

**Đã đối chiếu 12 feature kho ↔ task** (bao trùm B1/B2/B3a/B3b/B4/B6/B8/B9/B10). Kết quả: **6 TC bổ sung mới** (ngoài các TC đã có sẵn ở §7 các batch), tất cả nằm đúng **điểm nóng PHP8/Laravel13 mà bộ cũ bỏ sót**, mỗi TC dẫn chiếu ID kho + điểm nóng.

| # | ID | Batch | Điểm nóng | Nguồn kho |
|---|---|---|---|---|
| 1 | TC-JOBBILL001-02 | B1 | F5 Guzzle7/UnivaPay async + job | TC-BIL-267 |
| 2 | TC-FUNCDATE001-04 | B1 | A2 Carbon addMonth+endOfDay (Bug #34889) | TC-BLP-354/355/356/357 |
| 3 | TC-OUTEXPORT001-02 | B6 | F2 routing bảng năm + A5 + F4 | TC-CST-139→152 |
| 4 | TC-JOB001-02 | B8 | D Carbon time + job + F6 SDK (Bug #33245) | TC-FORM-286/287/283 |
| 5 | TC-DATACASCADE001-01 | B8 | F2 cascade + D recompute | TC-FORM-289→292 |
| 6 | TC-JOB001-03 | B3a | job send_random_messages + F6 SDK + A2 (Bug #38987) | TC-TMT-348/354/355 |

**Feature đối chiếu cho 0 TC mới** (đã cover đủ / đã rà kho maincase từ trước): FA-020/019/021 booking (B2), FA-004 richmenu (B3b), FA-008 broadcast · FA-003 autoreply · FA-007 あいさつ (B3a), B9 job, B10 mail (đã có 2 TC §7 sẵn).

**Loại khỏi phạm vi (job Java / ngoài module PHP)**: ScanHasCampaign (FA-031 §35), 配信数上限 job-cut (FA-008 §30), broadcast send job (Java).

**Ứng viên biên — Leader quyết nếu muốn chặt hơn**: FA-026 qty×price/決済終了/concurrency (TC-BIL-255/256/266) · FA-031 hoàn tiền cấp HĐ · FA-011 countdown form.

### Bước tiếp theo (sau khi Leader review)
1. Chốt TC giữ lại trong 6 TC trên.
2. **Rà ID trùng** với §7 tất cả batch của `05-review-report.md` trước khi push (ID ở đây đã né các trùng đã biết: B3a `TC-JOB001-01`, B1 `TC-JOBBILL001-01`, B4 `TC-OUTEXPORT001-01`).
3. Gộp từng TC vào `§7` đúng batch (`[Bx]` ở cột Ghi chú) → chạy `/sync-review-tc` push Studio #507 (surfaces + client_ref idempotent).
