# 05 — Review Report

> Draft cho Leader verify. Chuẩn đánh giá = **Spec / CR do Leader cung cấp (2026-09-24)** ở `01-bug-task.md` (ưu tiên hơn requirements Studio và mô tả diff). Chỉ ghi phần THIẾU + việc phải làm.
>
> **Cập nhật 2026-09-24 theo Leader chốt**: (1) khối cài đặt của option 予約後のキャンセル不可 **CÓ** 「例文を挿入する」 / 「利用しない」 / 「上記メッセージを必ず1通目に送信する」; (2) tin + action của option này **lưu riêng**; (3) app mobile phải test **phần action** cho **cả Salon và Lesson**.
> ⇒ Code hiện tại (ẩn 3 control, dùng chung cột, không migration) **không đạt** chuẩn → xem §5 I0. Khi Dev push bản sửa, chiều (b) §1 phải đánh giá lại theo diff mới (round 2).
> Leader chốt thêm: cờ 「利用しない」 và 「必ず1通目」 của option này cũng **lưu riêng**; **Lesson không có** 「必ず1通目」 (giữ nguyên spec hiện tại) → chỉ Salon hiện checkbox này.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #325 (ticket 39009, round 1, branch `ai-feature-39009`) |
| Tổng số TC review | 69 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — `03-dev-impact.md` mục 4 (BUG + F1–F8 + D1–D5 + T1–T6) | 16/20 mục có TC — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (12 file + 8 hành vi/rủi ro) | 15/20 điểm có TC — **CHƯA ĐỦ** (diff hiện tại không đạt quyết định Leader → đánh giá lại ở round 2) |

**Kết luận**: 31/40 điểm đủ TC · 3 GAP · 3 RISK (gộp thành 6 dòng dưới).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | T1 / T2 — admin hủy trên **app mobile admin**, **phần action** (Leader chốt: bắt buộc cả Salon và Lesson) · diff: app gọi chung service `adminCancel` | dev-impact + diff code | NEW-61 (Salon, `manual`, **chưa chạy**, chỉ 実行する + 1 action gắn tag) | **Lesson: GAP — 0 TC**. Salon: RISK — chưa chạy, thiếu multi-action, thiếu 実行しない, thiếu 利用しない + action | `[BLOCKER]` |
| G2 | T3 — エルメアクション **multi-action** (tiêu đề ticket: "action text và multiaction") chạy ở mode 3 | dev-impact | NEW-40 (Salon, `skip`) | RISK — Salon chưa chạy; **Lesson 0 TC** multi-action (NEW-31/63 chỉ 1 action gắn tag) | `[MAJOR]` |
| G3 | D2 — cờ `is_send_message` (「利用しない」) và 「必ず1通目」 của option 予約後のキャンセル不可 | dev-impact + diff code | NEW-7, NEW-26 | RISK — 2 TC có **expected sai theo quyết định Leader**: NEW-7 đòi ẩn 「必ず1通目」 (Salon phải hiện); NEW-26 đòi cờ 「利用しない」 dùng chung 2 option (phải độc lập). ✅ **Đã sửa trên Studio 2026-09-24** (NEW-7, NEW-26 → version 2). Các TC còn lại của vùng này (NEW-20→25, 34, 36, 37, 62, 63, 65) đã đúng chuẩn | `[MAJOR]` |
| G4 | Side effect sau hủy — **Lesson**: xóa toàn bộ remind chưa gửi (Leader yêu cầu) · diff: dev_impact "xoá remind EventStepTime pending" | diff code | NEW-38 chỉ Salon | **GAP — Lesson 0 TC** (Lesson không có Google Calendar — spec lesson-booking §1.2) | `[MAJOR]` |
| G5 | Nhánh `doAction = 0` (admin chọn **không** 実行する) — **Lesson** | diff code | NEW-32 chỉ Salon | **GAP — Lesson 0 TC** cho nhánh false của điều kiện mới | `[MAJOR]` |
| G6 | 2 file `setting_calendar_tab/setting_message.blade.php` (Salon + Lesson) — Studio gắn với màn xem trước (REQ-016) | diff code | NEW-55 (Salon, `skip`) | RISK — Salon chưa chạy; **Lesson 0 TC**. Input thiếu: journal không nói file này render màn nào (xem trước hay màn hub 予約・キャンセル時のメッセージと各種設定) → hỏi Dev | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 27 quan điểm Trigger khớp task · 8 chưa cover đủ. Phần lớn nằm trong phạm vi test Leader liệt kê ở `01-bug-task.md`.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `INTG-SHEET-001` / `OUT-EXPORT-001` — **đổi trạng thái booking trên Google Spreadsheet** sau admin hủy ở mode 3 (Leader yêu cầu) | Cao | GAP — 0 TC, cả Salon lẫn Lesson | `[BLOCKER]` |
| Q2 | `DATA-AUDIT-001` — **lưu lịch sử + xem được lịch sử action ở màn detail line user** (Leader yêu cầu) | Cao | GAP — NEW-38/41 chỉ nói "ghi lịch sử" của booking, không TC nào mở màn chi tiết bạn bè → アクション履歴 | `[BLOCKER]` |
| Q3 | `FUNC-001` — **hiển thị trigger action ở chat 1:1** (Leader yêu cầu) | Cao | GAP cho điểm kiểm này — không TC nào mở chat 1:1 của friend sau khi hủy | `[MAJOR]` |
| Q4 | `FUNC-001` / `SYNC-APP-001` — **notify PC / Chatwork / mobile** khi admin có setting (Leader yêu cầu) | Cao | GAP — 0 TC (notify-setting có hạng mục 「予約キャンセル時」 riêng cho サロン・面談予約 và レッスン予約) | `[MAJOR]` |
| Q5 | `MSG-004` — nội dung user nhìn thấy trên LINE thật (RULE-06) | Cao | RISK — NEW-30 (`manual`) chưa chạy; NEW-29/31 kiểm bằng runner. Chỉ Salon | `[MAJOR]` |
| Q6 | `LIFF-ENTRY-001` / `PERM-002` — CR mục 2: **khách không được hủy** ở mode 3 | Cao | RISK — Studio chỉ có NEW-43 (tầng API, lỗi có sẵn L1); không TC nào kiểm màn 予約履歴 phía LINE user ẩn nút hủy. Salon có trong kho, **Lesson không** | `[MAJOR]` |
| Q8 | `FUNC-001` / `MSG-004` — **ma trận cấu hình tin / action** khi admin hủy ở option 予約後のキャンセル不可 (Leader yêu cầu 2026-09-24, xem bảng dưới) | Cao | GAP — thiếu tổ hợp "chỉ tin nhắn" (cả bỏ tick và tick 「利用しない」) ở cả 2 hệ; Lesson thiếu "chỉ multi action" và "không cài gì" | `[BLOCKER]` |
| Q7 | `UI-FIELD-001` / `FUNC-001` — CR mục 4: **nút 「戻る」** | Trung bình | RISK — NEW-67→69 chưa chạy, tiền đề ghi "Lesson hoặc Salon" nên chỉ 1 hệ được kiểm; 12 file diff không nhắc nút này | `[MAJOR]` |

**Ma trận Q8 — cấu hình tin / action × kết quả khi admin hủy chọn 実行する (web)**

| # | Cấu hình của option 予約後のキャンセル不可 | Kết quả mong đợi | Salon | Lesson |
|---|---|---|---|---|
| M1 | Chỉ tin nhắn, **bỏ tick** 「利用しない」 | Gửi tin, không chạy action | ❌ GAP → `TC-MSG004-01` | ❌ GAP → `TC-MSG004-02` |
| M2 | Chỉ tin nhắn, **tick** 「利用しない」 | Không gửi gì, hủy vẫn thành công | ❌ GAP → `TC-FUNC001-06` | ❌ GAP → `TC-FUNC001-07` |
| M3 | Tin nhắn + multi action, bỏ tick 「利用しない」 | Gửi tin + chạy action | ✅ NEW-29, NEW-62 (pass; action 1 bước) | ✅ NEW-31, NEW-65 (pass; action 1 bước) |
| M3b | Tin nhắn + multi action, tick 「利用しない」 | Không gửi tin, vẫn chạy action | ✅ NEW-34 (fail do code ẩn 利用しない — §5 I0) | ✅ NEW-63 (fail — §5 I0) |
| M4 | Chỉ multi action (không nhập tin) | Không gửi tin, chạy đủ các bước action | ⚠️ NEW-40 (4 bước, **skip**) — tiền đề chưa ghi rõ "không nhập tin" | ❌ GAP → sửa `TC-FUNC001-02` thành "không nhập tin" |
| M5 | Không cài gì | Không gửi gì, hủy thành công, không lỗi | ✅ NEW-35 (pass) | ❌ GAP → `TC-FUNC001-08` |
| M6 | Có cài đặt nhưng admin chọn **実行しない** | Không gửi gì | ✅ NEW-32 | → `TC-FUNC001-01` (§7) |

- M3 dùng action 1 bước (gắn tag); việc chạy đủ **nhiều bước** được kiểm ở M4 (NEW-40 / `TC-FUNC001-02`) và app (`TC-SYNCAPP001-01`) → không đẻ thêm TC M3.
- App mobile dùng chung service với web (journal ■3) → ma trận chạy đủ ở web; app giữ 5 TC action ở §7 + NEW-61.
- NEW-40: đề nghị sửa tiền đề trên Studio, ghi rõ "không nhập nội dung tin" để đúng tổ hợp M4, rồi chạy (đang `skip`).

**Đã loại khỏi phạm vi** (Trigger khớp nhưng không có bằng chứng ảnh hưởng):
- `JOB-001` / `REG-RUN-001` — job nền LME chạy bên Java, diff chỉ có PHP/JS/blade; journal ■3: grep job Java = 0 kết quả. Notify Chatwork/app (job Java) chỉ giữ smoke ở Q4 vì Leader yêu cầu.
- `INTG-CAL-001` cho Lesson — FA-019 **không có** Google Calendar (spec lesson-booking §1.2). Salon đã có NEW-38.
- 空き枠通知 sau admin hủy (lesson-booking BR-33, `sendNotifyWhenThereIsSlotEmpty`) — code không đổi, Leader không liệt kê.
- `DATA-MIG-001` — diff hiện tại chưa có migration; khi Dev thêm chỗ lưu riêng (§5 I0) thì NEW-20/21 đã cover (có cột mới + không backfill) → không thiếu TC.
- `DATA-BACKUP-001` — copy bot (FA-033) **không** copy lịch salon/lesson (BR-05/BR-06, kho TC-BK-329) → thêm cột mới không cần TC copy bot.
- `PAY-*` — không chạm thanh toán / hoàn tiền.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | NEW-1, 2, 3, 4 (Salon) + NEW-12, 13, 14, 15 (Lesson) | NEW-19 | `DUP-SUBSET` | `UI-FIELD` · Normal · mở khối mode 3 và so heading / chip / toolbar / ô nhập / panel action · calendar chưa cấu hình mode 3 → mọi điểm so đã có ở 8 TC trên | `[MINOR]` |
| DUP-2 | NEW-24 | NEW-22, NEW-23 → **gộp** vào NEW-24 | `DUP-SUBSET` | `REG-SHARED` · Normal · đổi radio 全承認制 ↔ 予約後のキャンセル不可 rồi lưu · 2 chế độ đã có nội dung/action → NEW-24 đã kiểm cả nội dung lẫn action không bị ghi đè | `[MINOR]` |

- **Gate đã chạy**: bỏ NEW-19 / NEW-22 / NEW-23 → §1 và §2 không mất cover. DUP-2 đề nghị **gộp** (chuyển phần kiểm DB của NEW-22/23 vào NEW-24), không xóa trắng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check | Expected A | Nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` — **ĐÃ CHỐT** | NEW-7 · NEW-14 · (NEW-3, 5, 34, 63 đúng) | Thanh công cụ của khối option 予約後のキャンセル不可 | Studio REQ-003 / NEW-7: **ẩn** 「必ず1通目」 | Leader chốt: **CÓ** đủ 3 control giống 全承認制 → **NEW-7 sai**, phải sửa thành "hiển thị 「必ず1通目」 và lưu riêng". NEW-14 (Lesson) ghi không render 「必ず1通目」 → **đúng** (Leader chốt: Lesson không có checkbox này). Code ẩn cả 3 → **code sai** (§5 I0) | TC sai (NEW-7) + code sai | `[BLOCKER]` | Dev |
| C2 | `CONF-SPEC` — **ĐÃ CHỐT** | NEW-26 · (NEW-4, 15, 20→25, 36, 37, 62, 65 đúng) | Chỗ lưu tin + action + cờ của option này | Studio REQ-020 / NEW-26: cờ 「利用しない」 **dùng chung** 2 option | Leader chốt: **lưu riêng** → NEW-26 sai, phải sửa thành "cờ 2 option độc lập". Code dùng chung cột, không migration → **code sai** (§5 I0). W1 hết hiệu lực khi lưu riêng (không backfill = NEW-21/36/37) | TC sai (NEW-26) + code sai | `[BLOCKER]` | Dev |
| C3 | `CONF-SPEC` | NEW-29, 31, 34, 61, 62, 63, 65 | Admin hủy ở mode 3 có gửi tin/action không | Gửi tin + chạy action đã cấu hình | `spec-features/admin/lesson-booking/feature-spec.md` §4.4 d2 + **BR-46**: "`3` không cho huỷ → **KHÔNG gửi gì**" | Spec cũ hơn CR → cần update (TC đúng theo CR) | `[MAJOR]` | Leader |
| C4 | `CONF-KHO` | NEW-31 (Lesson) | Như C3 | Như C3 | `kho-tcs/fa019` **TC-LSN-222** "Admin cancel … Nhánh 3: KHÔNG gửi gì" | Kho cũ hơn CR → cần update | `[MAJOR]` | Leader |

**Đã rà**: 69 TC × `spec-features/admin/salon-booking` + `lesson-booking/feature-spec.md` (mục adminCancel / approve_type) + `kho-tcs/fa020` + `fa019` (nhóm 予約・キャンセル メッセージ/アクション, Detail booking, リマインド, Google, App mobile). Kho FA-020 không mâu thuẫn (TC-SLN-300/303 chỉ kiểm khách không hủy được). Không phát hiện `CONF-TC` giữa 2 TC.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I0 | `[BLOCKER]` | Code `ai-feature-39009` | Diff hiện tại **không đạt quyết định Leader**: ẩn 例文を挿入する / 利用しない / 必ず1通目 ở option 予約後のキャンセル不可; dùng chung `message_send_end` / `setting_action_id` / `is_send_message` với 全承認制, không migration | Dev sửa: hiện đủ 3 control; thêm chỗ lưu riêng (tin + action + cờ) + migration, không backfill. Sau đó chạy lại toàn bộ bộ TC (round 2) |
| I1 | `[BLOCKER]` | Nguồn — 28 TC `fail` | Cả 28 TC fail đều có `bug_tickets` rỗng → **chưa raise ticket** (Studio `openBugs=28`) | Theo quyết định Leader, fail của **NEW-3, 5, 9, 14, 16, 20, 21, 22, 23, 24, 25, 27, 34, 36, 37, 63** là bug thật của I0 → raise ticket gắn #39009. NEW-26 fail do expected sai (G3) → sửa TC, không raise. Fail của NEW-43/51/58/59/60 → ticket riêng (§6). Còn lại (NEW-28, 45, 47, 50, 52, 53) cần đọc log run để phân loại |
| I2 | `[BLOCKER]` | Nguồn — kết quả | Chỉ 33/69 TC `pass` (47,8% < 50%); 2 `skip`, 6 chưa chạy (NEW-30, 40, 48, 55, 61, 67, 68, 69) | Chạy lại sau khi chốt C1/C2; chạy đủ 8 TC còn thiếu kết quả |
| I3 | `[MAJOR]` | Nguồn — môi trường | 63/69 TC chỉ chạy ở `local`, 0 TC ở staging/production. Task gửi tin LINE thật + đồng bộ Google Calendar/Sheet + notify Chatwork → RULE-08 / ENV-003 | Chạy lại nhóm hủy đơn (NEW-29, 31, 38, 61 + TC §7) trên staging; kết luận cuối cần 1 lượt production |
| I4 | `[MAJOR]` ✅ đã sửa | NEW-26 | Expected không đo được: "ghi lại kết quả quan sát … để leader đối chiếu" — không có tiêu chí Đạt/Không đạt | Sau khi chốt C2, viết lại thành 1 expected cụ thể |
| I4b | `[MAJOR]` | NEW-61 | App mobile Salon chỉ kiểm 実行する + 1 action gắn tag; Leader yêu cầu đảm bảo **phần action** trên app | Đổi action của NEW-61 thành multi-action (gắn tag + gỡ tag + シナリオ + 友だち情報) và kiểm từng bước ở màn chi tiết bạn bè; 実行しない và 利用しない + action → TC mới §7 |
| I5 | `[MAJOR]` | NEW-67, 68, 69 | Tiền đề ghi "Calendar **Lesson hoặc Salon**" → không lặp lại được, chỉ kiểm được 1 hệ | Ghi rõ Salon trong 3 TC này; Lesson thêm TC riêng (§7 `TC-UIFIELD001-01`) |
| I6 | `[MINOR]` | NEW-62, 63, 65, 66, 67, 68, 69 | `requirement_keys` rỗng → Studio không map được coverage | Gắn REQ tương ứng trên Studio |
| I7 | `[MINOR]` | NEW-64 | Cột mã quan điểm ghi 2 mã `MSG-USER-001, RULE-TOOL-028` | Giữ 1 mã `MSG-USER-001` |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | NEW-58 | Test lỗi **có sẵn** W3 (ghi NULL `message_outside_filter`) — không do #39009 gây ra | Studio `dev_impact`: "Lỗi pre-existing trong hàm đã sửa (ngoài scope)"; journal ■7 đề nghị ticket riêng | Chuyển sang ticket riêng; fail không tính vào #39009 | `[MINOR]` |
| X2 | NEW-59 | Lỗi có sẵn W4 (Lesson ghi nhầm bảng Salon) | Như X1 | Như X1 | `[MINOR]` |
| X3 | NEW-60 | Lỗi có sẵn W7 (thiếu `bot_id` ở bản Salon) | Như X1 | Như X1 | `[MINOR]` |
| X4 | NEW-51 | Tab 予約時 (`moment='booking'`) — ticket không sửa validate của tab này (W8 / 横展開 L3) | Journal ■5 L3: "TRONG-scope: không → chuẩn hoá dần" | Chuyển sang ticket chuẩn hoá validate | `[MINOR]` |
| X5 | NEW-43 | API hủy phía khách không chặn mode 3 — lỗi có sẵn (横展開 L1) | Journal ■5 L1: "TRONG-scope: không → tách ticket" | Giữ TC nhưng gắn ticket riêng; phần giao diện của CR mục 2 xem Q6 | `[NIT]` |

- **Gate đã chạy**: không TC nào ở trên là TC duy nhất cover một mục F/D/T hay quan điểm trong phạm vi task. NEW-43 là TC duy nhất ở tầng API cho CR mục 2 → chỉ `[NIT]`, không đề nghị bỏ.

---

## 7. TCs đề xuất bổ sung (22)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` · `kho-tcs/fa019-datlichbaihoc-レッスン予約.md` (targeted, theo nhóm) |
| Vùng regression phát hiện từ kho | TC-SLN-331 (xóa remind khi hủy) · TC-SLN-362 (Google Calendar khi hủy) · TC-SLN-380/382 (Sheet: admin hủy = 「キャンセル（手動）」) · TC-LSN-222 (admin cancel theo approve_type) · TC-LSN-616 (notify app) |
| Conflict expected vs kho | TC-LSN-222 nhánh 3 → `CONF-KHO` C4, đã đưa §4 + §8 |
| GAP dùng lại TC kho | Q6 phía Salon → dùng lại **TC-SLN-300** / **TC-SLN-303** (mode 3: LINE user không có nút hủy), chạy trên calendar đã cấu hình tin + action mode 3 |
| Căn cứ TC regression `R<x>` | Không có TC R riêng — các regression cần thiết đã nằm trong Q1–Q7 |
| Xác nhận chống trùng | Đã đối chiếu 69 TC ở Studio + 2 file kho — không TC đề xuất nào trùng |
| Không đẻ TC mới | **G3**: TC đã có, chỉ sai expected → sửa trên Studio: **NEW-7** (Salon: 「必ず1通目」 phải hiển thị ở option 予約後のキャンセル不可 và lưu riêng, không ảnh hưởng 全承認制) · **NEW-26** (tick 「利用しない」 ở option 予約後のキャンセル不可 **không** đổi cờ của 全承認制). **G1 Salon 実行する**: mở rộng NEW-61 (§5 I4b). **G2 / G6 phía Salon**, **Q5**: chạy NEW-40 / NEW-55 / NEW-30, không cần TC mới |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-SYNCAPP001-01 | UI | SYNC-APP-001 | App mobile — hủy booking Lesson | Normal | manual | Tất cả | Lesson — admin hủy trên app mobile, chọn 実行する → gửi tin và chạy đủ multi-action của option 予約後のキャンセル不可 | Calendar Lesson 「TC39009-LS-APP」 ở 予約キャンセル時の各種設定 = 予約後のキャンセル不可, đã lưu tin 「LS-APP-MSG ＋LINE名」 + エルメアクション: gắn tag 「LS-APP-ADD」, gỡ tag 「LS-APP-OLD」, bắt đầu シナリオ 「LS-APP-SC」, ghi 友だち情報 「予約状態 = キャンセル」. Friend A (đã liên kết LINE, đang có tag 「LS-APP-OLD」) có 1 booking 予約確定. Đăng nhập app mobile admin (iOS hoặc Android) | 1. Trên app mobile mở レッスン予約 → calendar 「TC39009-LS-APP」 → booking của A<br>2. Chọn hủy booking, chọn 実行する, xác nhận<br>3. Mở LINE của A<br>4. Trên web mở màn chi tiết bạn bè của A: tab タグ, 友だち情報, 配信, アクション履歴 | — | A nhận đúng 1 tin 「LS-APP-MSG <tên LINE>」; có tag 「LS-APP-ADD」, mất tag 「LS-APP-OLD」, đang ở シナリオ 「LS-APP-SC」, 「予約状態」 = キャンセル; mỗi action chạy đúng 1 lần; booking = キャンセル (手動) | | Lấp G1 · Leader chốt: app phải test phần action cả Salon + Lesson · manual vì cần app mobile admin trên thiết bị thật · Evidence: ảnh app + LINE + các tab màn chi tiết bạn bè |
| TC-SYNCAPP001-02 | UI | SYNC-APP-001 | App mobile — hủy booking Lesson | Abnormal | manual | Tất cả | Lesson — admin hủy trên app mobile, chọn 実行しない → không gửi tin, không chạy action | Như TC-SYNCAPP001-01, dùng friend B có 1 booking 予約確定 và đang có tag 「LS-APP-OLD」 | 1. Trên app mobile mở booking của B → hủy, chọn **実行しない**, xác nhận<br>2. Mở LINE của B<br>3. Trên web mở màn chi tiết bạn bè của B | — | Booking = キャンセル (手動); B **không** nhận tin; tag, シナリオ, 友だち情報 của B **giữ nguyên** như trước khi hủy | | Lấp G1 · manual vì cần app mobile admin trên thiết bị thật · Evidence: ảnh LINE + tab タグ trước/sau |
| TC-SYNCAPP001-03 | UI | SYNC-APP-001 | App mobile — hủy booking Lesson | Normal | manual | Tất cả | Lesson — option 予約後のキャンセル不可 tick 「利用しない」: admin hủy trên app, chọn 実行する → không gửi tin nhưng vẫn chạy action | Calendar Lesson 「TC39009-LS-APP2」 = 予約後のキャンセル不可, **tick 「利用しない」**, có tin 「LS-APP2-MSG」 + action gắn tag 「LS-APP2-TAG」. Friend C có 1 booking 予約確定 | 1. Trên app mobile hủy booking của C, chọn 実行する<br>2. Mở LINE của C<br>3. Trên web mở màn chi tiết bạn bè của C → tab タグ | — | C **không** nhận tin 「LS-APP2-MSG」; C **có** tag 「LS-APP2-TAG」; booking = キャンセル (手動) | | Lấp G1 · dẫn từ TC-SLN-297 (利用しない: không gửi text, multi action vẫn chạy) · manual vì cần app mobile thật · Evidence: ảnh LINE + tab タグ |
| TC-SYNCAPP001-04 | UI | SYNC-APP-001 | App mobile — hủy booking Salon | Abnormal | manual | Tất cả | Salon — admin hủy trên app mobile, chọn 実行しない → không gửi tin, không chạy action | Calendar Salon 「TC39009-SL-APP」 = 予約後のキャンセル不可, đã lưu tin 「SL-APP-MSG」 + action gắn tag 「SL-APP-TAG」. Friend D (đã liên kết LINE) có 1 booking 予約確定 | 1. Trên app mobile mở サロン・面談予約 → booking của D → hủy, chọn **実行しない**, xác nhận<br>2. Mở LINE của D<br>3. Trên web mở màn chi tiết bạn bè của D → tab タグ | — | Booking = キャンセル (手動); D **không** nhận tin; **không** có tag 「SL-APP-TAG」 | | Lấp G1 · Salon 実行する + multi-action: mở rộng NEW-61 (§5 I4b) · manual vì cần app mobile thật · Evidence: ảnh LINE + tab タグ |
| TC-SYNCAPP001-05 | UI | SYNC-APP-001 | App mobile — hủy booking Salon | Normal | manual | Tất cả | Salon — option 予約後のキャンセル不可 tick 「利用しない」: admin hủy trên app, chọn 実行する → không gửi tin nhưng vẫn chạy action | Calendar Salon 「TC39009-SL-APP2」 = 予約後のキャンセル不可, **tick 「利用しない」**, có tin 「SL-APP2-MSG」 + action gắn tag 「SL-APP2-TAG」. Friend E có 1 booking 予約確定 | 1. Trên app mobile hủy booking của E, chọn 実行する<br>2. Mở LINE của E<br>3. Trên web mở màn chi tiết bạn bè của E → tab タグ | — | E **không** nhận tin 「SL-APP2-MSG」; E **có** tag 「SL-APP2-TAG」; booking = キャンセル (手動) | | Lấp G1 · dẫn từ TC-SLN-297 · web tương ứng: NEW-34 · manual vì cần app mobile thật · Evidence: ảnh LINE + tab タグ |
| TC-FUNC001-01 | UI | FUNC-001 | Detail booking — hủy thủ công (Lesson) | Abnormal | auto | Tất cả | Lesson — admin hủy booking ở mode 予約後のキャンセル不可, chọn 実行しない → không gửi tin, không chạy action | Calendar Lesson 「TC39009-LS-NOACT」 = 予約後のキャンセル不可, đã lưu tin 「TC39009-LS-NOACT-MSG」 + action gắn tag 「TC39009-LS-NOACT-TAG」. 1 booking 予約確定 của friend đã liên kết LINE | 1. Mở chi tiết booking → hủy, chọn **実行しない**, xác nhận<br>2. Mở LINE của friend<br>3. Mở màn chi tiết bạn bè → tab タグ | — | Booking = キャンセル (手動); friend **không** nhận tin; **không** có tag 「TC39009-LS-NOACT-TAG」 | | Lấp G5 · đối xứng NEW-32 (Salon) · Đánh giá spec: CR Leader mục 3 · Evidence: ảnh LINE + tab タグ |
| TC-STATEDEP001-01 | UI | STATE-DEP-001 | Detail booking — hủy thủ công (Lesson) | Normal | auto | Tất cả | Lesson — admin hủy booking ở mode 予約後のキャンセル不可 → xóa toàn bộ remind CHƯA gửi, giữ remind đã gửi | Calendar Lesson 「TC39009-LS-REMIND」 = 予約後のキャンセル不可, có 3 remind: 3 ngày trước / 1 ngày trước / 1 giờ trước. 1 booking 予約確定 hẹn sau 2 ngày → remind "3 ngày trước" đã gửi, 2 remind còn lại đang chờ | 1. Hủy booking, chọn 実行する<br>2. Chờ qua mốc remind "1 ngày trước" (hoặc chỉnh giờ hẹn cho mốc tới sớm)<br>3. Mở LINE của friend | — | Friend **không** nhận 2 remind còn lại sau khi hủy; remind "3 ngày trước" đã nhận vẫn còn trong lịch sử chat | | Lấp G4 · Leader yêu cầu "xóa toàn bộ remind chưa gửi" · đối xứng NEW-38 (Salon) · dẫn từ TC-SLN-331 · Evidence: ảnh LINE qua mốc remind |
| TC-FUNC001-02 | UI | FUNC-001 | Detail booking — hủy thủ công (Lesson) | Normal | auto | Tất cả | Lesson — chỉ cài multi action (không có tin): admin hủy → không gửi tin, chạy đủ mọi bước action | Calendar Lesson 「TC39009-LS-MULTI」 = 予約後のキャンセル不可, **KHÔNG nhập nội dung tin**, エルメアクション gồm: gắn tag 「LS-MULTI-ADD」, gỡ tag 「LS-MULTI-OLD」, bắt đầu シナリオ 「LS-MULTI-SC」, ghi 友だち情報 「予約状態 = キャンセル」. Friend (đã liên kết LINE) đang có tag 「LS-MULTI-OLD」, có 1 booking 予約確定 | 1. Hủy booking, chọn 実行する<br>2. Mở LINE của friend<br>3. Mở màn chi tiết bạn bè: tab タグ, 友だち情報, 配信 (シナリオ) | — | Friend **không** nhận tin hủy nào; đủ 4 bước chạy đúng 1 lần: có 「LS-MULTI-ADD」, mất 「LS-MULTI-OLD」, friend đang ở シナリオ 「LS-MULTI-SC」, 友だち情報 「予約状態」 = キャンセル | | Lấp G2 + Q8 (M4) · Salon: chạy NEW-40 (đang skip) · Evidence: ảnh LINE + các tab màn chi tiết bạn bè |
| TC-OUTPREVIEW001-01 | UI | OUT-PREVIEW-001 | 予約・キャンセル メッセージ (Lesson) | Normal | auto | Tất cả | Lesson — sau khi lưu mode 予約後のキャンセル不可, màn 予約・キャンセル時のメッセージと各種設定 và màn xem trước hiển thị đúng cấu hình mode này | Calendar Lesson 「TC39009-LS-PV」 đã lưu mode 予約後のキャンセル不可 với tin 「LS-PV-MSG」 + action gắn tag 「LS-PV-TAG」 | 1. Mở màn 予約・キャンセル時のメッセージと各種設定 → xem thẻ キャンセル<br>2. Mở xem trước tin nhắn / action của mode này (nếu có) | — | Thẻ キャンセル hiển thị 「予約後のキャンセル不可」; xem trước hiển thị 「LS-PV-MSG」 và action 「LS-PV-TAG」, không hiển thị tin/action của 全承認制 | | Lấp G6 · cần Dev xác nhận `setting_message.blade.php` render màn nào · Salon: chạy NEW-55 · dẫn từ TC-LSN-320 · Evidence: ảnh màn |
| TC-INTGSHEET001-01 | UI | INTG-SHEET-001 | Googleスプレッドシート連携 (Salon) | Normal | auto | Tất cả | Salon — admin hủy booking ở mode 予約後のキャンセル不可 → trạng thái booking trên Google Spreadsheet đổi sang 「キャンセル（手動）」 | Calendar Salon 「TC39009-SL-SHEET」 = 予約後のキャンセル不可 (có tin + action), đã liên kết Google Spreadsheet. 1 booking 予約確定 đã có dòng trên Sheet | 1. Hủy booking, chọn 実行する<br>2. Mở file Google Spreadsheet của calendar, tìm dòng booking | — | Dòng của booking đó cập nhật ステータス = 「キャンセル（手動）」, không sinh dòng mới | | Lấp Q1 · Leader yêu cầu · dẫn từ TC-SLN-380/382 · RULE-01: chỉ Normal vì code sync Sheet không đổi, đây là smoke E2E · RULE-08 → kết luận cuối cần 1 lượt production · Evidence: ảnh Sheet trước/sau |
| TC-INTGSHEET001-02 | UI | INTG-SHEET-001 | Googleスプレッドシート連携 (Lesson) | Normal | auto | Tất cả | Lesson — admin hủy booking ở mode 予約後のキャンセル不可 → trạng thái booking trên Google Spreadsheet được cập nhật | Calendar Lesson 「TC39009-LS-SHEET」 = 予約後のキャンセル不可 (có tin + action), đã liên kết Google Spreadsheet. 1 booking 予約確定 đã có dòng trên Sheet | 1. Hủy booking, chọn 実行する<br>2. Mở file Google Spreadsheet, tìm dòng booking | — | Dòng của booking đó cập nhật trạng thái hủy do admin (cùng giá trị như khi hủy ở mode 全承認制), không sinh dòng mới | | Lấp Q1 · Leader yêu cầu · RULE-08 → cần 1 lượt production · Evidence: ảnh Sheet trước/sau |
| TC-DATAAUDIT001-01 | UI | DATA-AUDIT-001 | Detail booking — hủy thủ công (Salon) | Normal | auto | Tất cả | Salon — sau khi admin hủy ở mode 予約後のキャンセル不可, lịch sử booking và lịch sử action hiển thị ở màn chi tiết bạn bè | Calendar Salon 「TC39009-SL-HIS」 = 予約後のキャンセル不可, tin 「SL-HIS-MSG」 + action gắn tag 「SL-HIS-TAG」. 1 booking 予約確定 của friend đã liên kết LINE | 1. Hủy booking, chọn 実行する<br>2. Mở màn chi tiết bạn bè → 予約管理 và アクション履歴 | — | 予約管理: booking hiển thị キャンセル, có dòng lịch sử 「手動予約キャンセル」. アクション履歴: có dòng action gắn tag 「SL-HIS-TAG」 kèm thời điểm hủy | | Lấp Q2 · Leader yêu cầu · Lesson dùng chung cơ chế action → chạy lại cùng TC trên 1 calendar Lesson nếu Leader cần · Evidence: ảnh 2 tab |
| TC-FUNC001-03 | UI | FUNC-001 | Chat 1:1 (Salon) | Normal | auto | Tất cả | Salon — sau khi admin hủy ở mode 予約後のキャンセル不可, chat 1:1 của friend hiển thị tin hủy và trigger action | Như TC-DATAAUDIT001-01 (calendar 「TC39009-SL-HIS」) | 1. Hủy booking, chọn 実行する<br>2. Mở chat 1:1 của friend | — | Chat 1:1 hiển thị tin 「SL-HIS-MSG」 đã gửi và dòng trigger action của lần hủy này | | Lấp Q3 · Leader yêu cầu · Evidence: ảnh chat 1:1 |
| TC-FUNC001-04 | UI | FUNC-001 | Notify admin (Salon) | Normal | manual | Tất cả | Salon — admin hủy booking ở mode 予約後のキャンセル不可 → notify app / PC / Chatwork theo 通知設定 | Màn 通知設定: サロン・面談予約 bật 「予約キャンセル時」; bật 3 kênh スマートフォンアプリ / PCデスクトップ / ChatWork (có room URL), 通知タイミング = ngay. Calendar Salon = 予約後のキャンセル不可. 1 booking 予約確定 | 1. Hủy booking, chọn 実行する<br>2. Kiểm tra notify trên app mobile, trình duyệt PC, phòng Chatwork (chờ chu kỳ gửi Chatwork)<br>3. Tắt 「予約キャンセル時」, hủy 1 booking khác, kiểm tra lại | — | Bước 2: nhận notify hủy booking ở cả 3 kênh. Bước 3: không nhận notify nào | | Lấp Q4 · Leader yêu cầu · manual vì cần app mobile thật + phòng Chatwork thật · Evidence: ảnh 3 kênh |
| TC-FUNC001-05 | UI | FUNC-001 | Notify admin (Lesson) | Normal | manual | Tất cả | Lesson — admin hủy booking ở mode 予約後のキャンセル不可 → notify app / PC / Chatwork theo 通知設定 | Như TC-FUNC001-04 nhưng hạng mục レッスン予約 → 「予約キャンセル時」, calendar Lesson = 予約後のキャンセル不可 | Như TC-FUNC001-04 | — | Như TC-FUNC001-04 | | Lấp Q4 · Leader yêu cầu · manual vì cần app mobile thật + phòng Chatwork thật · dẫn từ TC-LSN-616 · Evidence: ảnh 3 kênh |
| TC-MSG004-01 | UI | MSG-004 | Detail booking — hủy thủ công (Salon) | Normal | auto | Tất cả | Salon — chỉ cài tin nhắn (bỏ tick 「利用しない」, không có action): admin hủy → gửi tin, không chạy action | Calendar Salon 「TC39009-SL-TXT」 = 予約後のキャンセル不可, tin 「SL-TXT-MSG ＋LINE名」, 「利用しない」 **bỏ tick**, **không** đăng ký エルメアクション. Friend đã liên kết LINE có 1 booking 予約確定 | 1. Hủy booking, chọn 実行する<br>2. Mở LINE của friend<br>3. Mở màn chi tiết bạn bè: tab タグ, アクション履歴 | Tin: 「SL-TXT-MSG ＋LINE名」 | Friend nhận đúng 1 tin 「SL-TXT-MSG <tên LINE>」; tag và アクション履歴 **không** phát sinh gì mới; booking = キャンセル (手動) | | Lấp Q8 (M1) · Evidence: ảnh LINE + tab タグ |
| TC-MSG004-02 | UI | MSG-004 | Detail booking — hủy thủ công (Lesson) | Normal | auto | Tất cả | Lesson — chỉ cài tin nhắn (bỏ tick 「利用しない」, không có action): admin hủy → gửi tin, không chạy action | Như TC-MSG004-01 nhưng calendar Lesson 「TC39009-LS-TXT」, tin 「LS-TXT-MSG ＋LINE名」 | Như TC-MSG004-01 | Tin: 「LS-TXT-MSG ＋LINE名」 | Friend nhận đúng 1 tin 「LS-TXT-MSG <tên LINE>」; tag và アクション履歴 **không** phát sinh gì mới; booking = キャンセル (手動) | | Lấp Q8 (M1) · Evidence: ảnh LINE + tab タグ |
| TC-FUNC001-06 | UI | FUNC-001 | Detail booking — hủy thủ công (Salon) | Abnormal | auto | Tất cả | Salon — chỉ cài tin nhắn nhưng **tick 「利用しない」**, không có action: admin hủy → không gửi gì, hủy vẫn thành công | Calendar Salon 「TC39009-SL-TXT2」 = 予約後のキャンセル不可, tin 「SL-TXT2-MSG」, 「利用しない」 **tick**, **không** đăng ký エルメアクション. Friend đã liên kết LINE có 1 booking 予約確定 | 1. Hủy booking, chọn 実行する<br>2. Mở LINE của friend<br>3. Mở màn chi tiết bạn bè: tab タグ, アクション履歴 | — | Booking = キャンセル (手動), màn không báo lỗi; friend **không** nhận tin; tag và アクション履歴 không phát sinh gì mới | | Lấp Q8 (M2) · Evidence: ảnh LINE + màn booking |
| TC-FUNC001-07 | UI | FUNC-001 | Detail booking — hủy thủ công (Lesson) | Abnormal | auto | Tất cả | Lesson — chỉ cài tin nhắn nhưng **tick 「利用しない」**, không có action: admin hủy → không gửi gì, hủy vẫn thành công | Như TC-FUNC001-06 nhưng calendar Lesson 「TC39009-LS-TXT2」, tin 「LS-TXT2-MSG」 | Như TC-FUNC001-06 | — | Booking = キャンセル (手動), màn không báo lỗi; friend **không** nhận tin; tag và アクション履歴 không phát sinh gì mới | | Lấp Q8 (M2) · Evidence: ảnh LINE + màn booking |
| TC-FUNC001-08 | UI | FUNC-001 | Detail booking — hủy thủ công (Lesson) | Abnormal | auto | Tất cả | Lesson — option 予約後のキャンセル不可 không cài tin, không cài action: admin hủy → không gửi gì, không lỗi | Calendar Lesson 「TC39009-LS-EMPTY」 chọn 予約後のキャンセル不可 và bấm 「保存」, **không** nhập tin, **không** đăng ký action. Friend đã liên kết LINE có 1 booking 予約確定 | 1. Hủy booking, chọn 実行する<br>2. Mở LINE của friend<br>3. Mở màn chi tiết bạn bè: tab タグ, アクション履歴 | — | Booking = キャンセル (手動), màn không báo lỗi; friend **không** nhận tin; không phát sinh action | | Lấp Q8 (M5) · đối xứng NEW-35 (Salon) · Evidence: ảnh LINE + màn booking |
| TC-LIFFENTRY001-01 | UI | LIFF-ENTRY-001 | LINE user — hủy booking (Lesson) | Abnormal | auto | Tất cả | Lesson — calendar ở mode 予約後のキャンセル不可 có cấu hình tin + action: LINE user vẫn không thấy nút hủy | Calendar Lesson 「TC39009-LS-LIFF」 = 予約後のキャンセル不可, đã lưu tin + action. Friend có 1 booking 予約確定 | 1. Friend mở LIFF 予約履歴 → mở booking<br>2. Mở URL hủy trong tin xác nhận đặt lịch (nếu có) | — | Không có nút hủy ở màn chi tiết booking; booking vẫn 予約確定; không phát sinh tin/action hủy | | Lấp Q6 · CR Leader mục 2 · regression: bật khối action mode 3 không làm hiện nút hủy · Salon dùng lại TC-SLN-300/303 · Evidence: ảnh LIFF |
| TC-UIFIELD001-01 | UI | UI-FIELD-001 | 予約・キャンセル メッセージ (Lesson) | Normal | auto | Tất cả | Lesson — nút 「戻る」 ở màn 予約キャンセル時の各種設定 quay về 予約・キャンセル時のメッセージと各種設定, không lưu thay đổi chưa bấm 保存 | Calendar Lesson đã lưu mode 予約後のキャンセル不可 với tin 「LS-BACK-OLD」 | 1. Mở 予約キャンセル時の各種設定, sửa tin thành 「LS-BACK-NEW」, không bấm 保存<br>2. Bấm 「戻る」<br>3. Mở lại màn | — | Bước 2: về màn 予約・キャンセル時のメッセージと各種設定. Bước 3: tin vẫn là 「LS-BACK-OLD」 | | Lấp Q7 · CR Leader mục 4 · NEW-67→69 ghi rõ Salon (I5) · cần Dev xác nhận nút 戻る đã có trong diff · Evidence: ảnh màn |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-change-cancel-action.md` + Studio REQ-003 / REQ-020 | **Leader đã chốt**: option 予約後のキャンセル不可 **có** 「例文を挿入する」 / 「利用しない」 / 「必ず1通目」 → sửa REQ-003 (bỏ "không render 必ず1通目") và REQ-020 (cờ độc lập). Cờ 「利用しない」 / 「必ず1通目」 của option này **lưu riêng**; 「必ず1通目」 **chỉ có ở Salon**, Lesson giữ nguyên spec hiện tại (không có) | C1 CONF-SPEC | Leader |
| 2 | `spec-change-cancel-action.md` + Studio REQ-005 / REQ-009 | **Leader đã chốt: lưu riêng** → giữ REQ-005/009; ghi rõ vào spec change; Dev implement lại (§5 I0). Bỏ khuyến nghị audit W1 khi đã lưu riêng + không backfill | C2 CONF-SPEC | Leader + Dev |
| 3 | `spec-features/admin/lesson-booking/feature-spec.md` §4.4 d2 + BR-46; `salon-booking/feature-spec.md` (luồng adminCancel) | `approve_type = 3` khi admin hủy: **gửi** tin + chạy action đã cấu hình (theo quyết định #2), thay cho "KHÔNG gửi gì"; bổ sung nút 「戻る」 ở màn 予約キャンセル時の各種設定 | C3 CONF-SPEC | Leader |
| 4 | `kho-tcs/data/` FA-019 (TC-LSN-222) + FA-020 (TC-SLN-300) | TC-LSN-222 nhánh 3: đổi "KHÔNG gửi gì" thành gửi tin + action mode 3; thêm nhánh admin hủy mode 3 vào TC-SLN-300 | C4 CONF-KHO | Leader |
