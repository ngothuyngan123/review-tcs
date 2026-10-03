# 05 — Review Report (round 2)

> Draft cho Leader verify. Ticket #41448 · Studio task #339 · review lại 2026-09-30 sau khi Dev cập nhật (Journal #139287 + #139421, commit `d199db2c03` → `e8931817a2`). Report vòng 1: `05-review-report.md`.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #339 (ticket 41448, round 1, branch `ai_fixbug_41448`) |
| Tổng số TC review | 61 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` (refresh theo #139287 + #139421): `BUG` + F1–F9 + T1–T9 = 19 mục | 9/19 mục đủ TC có kết quả Đạt · 4 GAP · 6 RISK — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` (computedAt 2026-09-30 08:51Z, diff sạch `69eeb2a6be..e8931817a2`, 4 file prod) | 5/14 điểm đủ · 4 GAP · 5 RISK (loại 1 điểm có lý do) — **CHƯA ĐỦ** |

**Kết luận**: 14/33 vùng ảnh hưởng đủ TC · 8 GAP · 11 RISK.
- 12 dòng G của vòng 1 **đã đóng hết**: 25 TC đề xuất đã lên Studio (NEW-22 → NEW-46) và pass staging. Riêng NEW-41 (xác nhận trên bot khách) bị blocked vì chưa release, và TC-REGSHARED001-02 (NEW-39) đã bị xóa khỏi Studio (NEW-18 viết lại đã cover đúng ý).
- GAP mới đều đến từ **4 commit sau** (`c6adf066a8` · `23492bfad5` · `e8931817a2` + job + thanh toán). Dev tự sửa lại: khai báo cũ "chỉ đổi option 上限を設定する + 指名なし" **không còn đúng**.
- RISK chủ yếu do TC đã viết nhưng **chưa chạy** (10 TC mới NEW-47 → NEW-57) hoặc chạy **trước** khi Dev báo commit cuối. Nhóm này không cần TC mới, xử lý ở §5 I1 / I2.

### 1b. Ma trận option × luồng (Dev #139421: "retest CẢ BA option, ở cả hai luồng")

| Option 受付上限 | 指名なし | 指名 (chọn đích danh) |
|---|---|---|
| 上限を設定する | ✓ Đủ ma trận Leader chốt 2026-09-29 (NEW-22 → NEW-36, pass staging) | NEW-19, NEW-28, #20824 pass · NEW-50 (đầu ca) chưa chạy · **thiếu**: ca của NV khác trong phần 片付け → G3 |
| 上限を設定しない | NEW-18 pass (cuối ca) · NEW-51 (đầu ca) chưa chạy · **thiếu**: nhận trọn khoảng + đếm lượt đồng thời → G1 | NEW-55 chưa chạy |
| 上限をその時間に受付可能なスタッフ数の合計にする + シフトの合算をしない | #20822 pass · #20844 skip | NEW-56 chưa chạy |
| **Calendar 個人** (chỉ có option 上限を設定しない / 上限を設定する) | **0 TC** → G5 | — (không có bước chọn staff) |
| 上限をその時間に受付可能なスタッフ数の合計にする + シフトの合算をする | NEW-37 (tiếp sức), NEW-38 pass · #20843 skip · **thiếu**: case Abnormal của tiếp sức → G2 | NEW-57 chưa chạy |

- Leader chốt 2026-09-29 giữ tối thiểu 3 option ngoài 上限を設定する, với lý do "code nhánh các option này không đổi". Lý do này **không còn đúng**.
- Vòng này §7 chỉ bổ sung **đúng những điểm Dev vừa đổi** (G1–G3). Các ô giữa ca cộng dồn / qua ngày / không cài nghỉ của các option còn lại vẫn để Leader quyết (§5 I3).

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Option 「上限を設定しない」 — Dev #139421: cổng kiểm mới `hasStaffCanTakeWholeRange` (≥ 1 NV nhận **trọn** khoảng) + cách đếm hạn mức theo **lượt đồng thời** nay áp cho cả option này (F5, F6, T6) | `dev-impact` + `diff code` | NEW-18 (cuối ca, pass) · NEW-51 (đầu ca, chưa chạy). NEW-47 / NEW-48 chỉ ở option 上限を設定する | **GAP** — 0 TC kiểm 2 cổng mới ở option này. Thiếu Abnormal "2 NV bận lệch nửa khung → TẮT" và Boundary "2 đơn nối tiếp còn suất / chồng giờ hết suất". Đây là quan điểm Cao (FUNC-004), RULE-01 cần đủ N/A/B | `[BLOCKER]` |
| G2 | Option 「シフトの合算をする」 — nay gộp ca liền nhau, 1 buổi do nhiều NV **thay phiên** (T7). Dev: "thay đổi hành vi rõ rệt nhất, cần QA xác nhận" · lateral_scan: "chế độ gộp ca còn 27 chặn oan / 3 lỗ hổng" | `diff code` | NEW-37 (tiếp sức được, Normal) · NEW-38 (Boundary cuối ca) — pass | **GAP** — chưa có Abnormal: ca có **khoảng hở** giữa 2 NV, hoặc NV nối ca **đang bận** phần sau → phải TẮT. Đây đúng là hướng "lỗ hổng" (mở oan → đặt trùng) Dev còn ghi nhận | `[BLOCKER]` |
| G3 | Nhánh 指名 — `checkLimitHasStaff` nay **đã sửa** (commit `23492bfad5`): "xét ca của những người KHÁC tại mốc giờ phục vụ" (F4, T8). Mục 3 của Dev vẫn ghi "KHÔNG sửa" | `diff code` (câu 1 + 3) | NEW-19, NEW-28, #20824 (chỉ kiểm ca của chính NV được chọn) · NEW-50, NEW-55/56/57 chưa chạy | **GAP** — chưa TC nào dựng NV **khác** tan ca nằm trong phần 片付け của khung đang xét, là đúng điểm sửa của commit này | `[MAJOR]` |
| G4 | Luồng đặt lịch **có thanh toán** — phép kiểm lại chỗ trống được chèn vào `createOrderPayment`, chạy trên đơn tạm **trước** bước trừ tiền (Stripe `paymentStripe:1588` · UnivaPay `paymentUnivapay:1824` · "trả sau") (F8, T3) | `dev-impact` + `diff code` | NEW-52 (2 khách tranh khung cuối, **1 cổng** "Stripe hoặc Univapay", local, chưa chạy) · NEW-53 (lịch bị tắt giữa lúc thanh toán, local, chưa chạy) | **GAP** — 0 TC cho **happy path**: 1 khách đặt có thanh toán vẫn thành công và bị trừ tiền đúng 1 lần sau khi chèn phép kiểm lại. 2 cổng đi 2 đường code khác nhau. Phần "trả sau" không có trong kho / spec FA-020 → §5 I7 | `[BLOCKER]` |
| G5 | **Calendar loại 個人** (1 staff 運営者; chỉ có 2 option: 上限を設定しない / 上限を設定する) | `diff code` (ma trận option) | **0 TC** — 61/61 TC Studio đều dùng calendar nhiều nhân viên | **GAP** — vòng 1 loại calendar 個人 với lý do "không thể có NV lệch ca". Lý do đó chỉ đúng cho bug gốc. Các thay đổi mới vẫn đi qua calendar 個人: mốc đầu / cuối ca bỏ +1 phút (#41746), nghỉ trước (#41742), limit tính theo lượt đồng thời (c6adf066a8), cổng "≥ 1 staff nhận trọn khoảng" áp cho option 上限を設定しない (#139421). Rủi ro lớn nhất: kho `TC-SLN-290` ghi 個人 + 上限を設定しない **đặt được nhiều booking cùng khung** — cổng mới có thể chặn oan booking thứ 2 vì 個人 chỉ có 1 staff | `[BLOCKER]` |

> Đã loại 1 điểm của chiều (b), có lý do:
> - Điểm "job phía khách bỏ +1 phút" (Dev #139421 mục 4) không dựng được qua UI. Course trên UI chỉ tăng theo bước 5 phút (NEW-7, NEW-32), nên không tạo được buổi kết thúc lệch 1 phút so với giờ tan ca.
> - Studio NEW-54 cũng ghi rằng việc bỏ +1 phút ở job và ở phép kiểm triệt tiêu nhau.
> - Nhờ Dev xác nhận bằng unit test (§5 I12), không đẻ TC.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 16 quan điểm Trigger khớp task (thêm `PAY-STATE-001`, `PAY-ABANDON-001` vì luồng thanh toán bị chạm) · 3 chưa cover đủ. 4 Q của vòng 1: Q1 `CONC-001` / Q2 `INTG-CAL-001` / Q3 `SYNC-APP-001` đã đóng (NEW-42/43, NEW-44/45, NEW-46 pass staging). Q4 còn nguyên.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `PAY-STATE-001` | Cao | **RISK** — trigger mới vì Dev đổi luồng thanh toán (#139421 mục 5). Hiện chỉ có NEW-52 (Abnormal, chưa chạy) và NEW-53 (mã lạ `TOOL-ERRHYG-001`, chưa chạy). Thiếu Normal → `TC-PAYSTATE001-01`/`-02` ở §7 (trùng G4) | `[MAJOR]` |
| Q2 | `PAY-ABANDON-001` | Cao | **GAP — 0 TC**. Phép kiểm lại nay chạy trên **đơn tạm** trước bước trừ tiền. Khách bỏ dở hoặc hủy ở bước 3D Secure thì đơn tạm có còn giữ khung (chặn oan khách sau) không? **Không đề xuất TC**: oracle chưa có. Kho `TC-SLN-407` nhánh hủy chỉ ghi "KHÔNG tạo booking (hoặc booking không được thanh toán)", nên không biết đơn chưa thanh toán có chiếm khung hay không → §8 #5 | `[MAJOR]` |
| Q3 | `JOB-001` | Cao | **RISK — chỉ được cover bởi mã lạ** (còn nguyên từ vòng 1). NEW-1 / NEW-2 / NEW-54 / #20829 gắn `JOB-002`; NEW-3 gắn `RULE-TOOL-028`. Nội dung đủ N/A/B → **không đẻ TC**, chỉ cần đổi mã quan điểm trên Studio sang `JOB-001` | `[MAJOR]` |

Đã loại khỏi phạm vi (nháp nội bộ; mỗi mã 1 lý do):
- `PAY-REFUND-*` / hoàn tiền — không đổi dòng code nào ở luồng 返金. Đơn bị hủy do chống trùng bị chặn **trước** bước trừ tiền, nên không phát sinh hoàn tiền.
- `DATA-DB-001` — Dev 4.2 không đổi dữ liệu. Phần xoá đơn tạo sau (#41743) đã có NEW-43 / NEW-52 kiểm "chỉ còn đúng 1 đơn".
- Các mã đã loại ở vòng 1 (`LIFF-ENTRY-001`, `MSG-*`, `INTG-SHEET-001`, `OUT-EXPORT-001`, `COMPAT-LEGACY-001`, `REG-RUN-001`, `DEPLOY-LIVE-001`, `DATA-COUNT-001`, `CONC-003`) — 4 commit mới không chạm, giữ nguyên lý do.

---

## 3. TC trùng lặp nội dung

Đã rà 61 TC theo 4 yếu tố — **không phát hiện trùng lặp** (không có DUP-EXACT / DUP-SUBSET / DUP-INFLATE).

- Các cặp dễ nhầm đã xét và không tính là trùng:
  - `NEW-18` / `NEW-55`: cùng dữ liệu nhưng khác luồng (指名なし / 指名).
  - `NEW-19` / `NEW-28`: cùng option 上限を設定する + 指名 nhưng khác bộ nghỉ (chỉ nghỉ sau 60' / nghỉ trước + sau 30') và khác vị trí (cuối ca / giữa ca).
  - `NEW-48` / `#20844`: cùng ý "đơn nối tiếp không làm hết suất" nhưng khác option.
  - `NEW-13` / `NEW-24`: khác cấu hình (NV lệch ca có người bận / 1 NV).
- NEW-21 (vòng 1 đề nghị thay bằng TC-FUNCDATE001-11) đã được xóa trên Studio. NEW-32 thay thế, dùng bước 5 phút.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: 61 TC × `spec-features/admin/salon-booking/feature-spec.md` (§2.4.3, §2.4.4, BR) + `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` (nhóm 受付上限, 前後の空き時間, スタッフ自動割り当て, 決済 — thẻ & 3D Secure, Admin thêm booking thủ công, Modal lý do; `TC-SLN-115`, `TC-SLN-122`, `TC-SLN-293`, `TC-SLN-402`, `TC-SLN-407`, `TC-SLN-413`) + quy tắc Leader chốt 2026-09-29 + quyết định reject bug Studio #1509 → **2 mâu thuẫn**.

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` (còn từ vòng 1) | `NEW-22`, `NEW-23`, `NEW-26`, `NEW-27` (đầu ca / giữa ca, pass staging) | Khung trước / sau quanh 1 đơn có sẵn khi cài **cả** nghỉ trước và sau | Theo Leader: đầu ca không tính nghỉ trước. Giữa ca cộng dồn nghỉ sau + nghỉ trước (đơn 10:00–12:00, nghỉ 30'/30' → đơn tiếp từ 13:00) | Kho `TC-SLN-293` nhánh "Cả 2": slot sau **10:45** (tính nghỉ 1 lần); slot trước 07:45 < giờ mở cửa → **disable hết** | Nay đã có bằng chứng: 4 TC theo quy tắc Leader **pass** trên staging, tức code đang chạy theo quy tắc Leader. Khả năng cao là **kho viết theo hành vi cũ** → cần sửa kho. Khả năng còn lại: staging chưa phải build cuối (§5 I1) | `[MAJOR]` | Leader (kho) |
| C2 | `CONF-TC` | `#20823` ↔ `NEW-40` (+ reject bug Studio #1509) | Lưới admin 予約管理 ở khung mà LIFF đang TẮT | `#20823`: "Lưới admin 予約管理 nhất quán: **không còn nhận đặt ở 19:00**" | `NEW-40` (viết lại 2026-09-30): admin calendar **không** dùng thời lượng Course để cắt slot. Bug #1509 ("lưới 予約管理 đánh dấu khung còn nhận đặt trong khi LIFF ẩn") bị reject, lý do: *"admin sẽ hiển thị ON đến hết time lv"* | #20823 viết theo giả định cũ (lưới admin phải khớp LIFF) → sai, cần sửa expected. Hoặc quyết định reject #1509 chưa được Leader duyệt | `[MAJOR]` | Leader |

- `CONF-SPEC`: **không đánh giá được** — spec FA-020 vẫn không có Business rule về cách tính khung trống (§5 I14 + §8 #1).
- `CONF-TC` khác đã xét, không mâu thuẫn:
  - NEW-57 (1.2 + 指名: không tiếp sức sang NV-B) ↔ NEW-37 (1.2 + 指名なし: tiếp sức được). Khớp quy tắc Leader "1.2 áp khi 指名なし".
  - NEW-18 ↔ NEW-55 cùng expected cho 18:00 / 18:30.
- `CONF-KHO` khác: NEW-47 / TC-FUNC004-06 ("1 NV làm trọn vẹn") khớp quy tắc Leader "上限を設定しない giống 1.1". NEW-3 khớp `TC-SLN-115` (admin book bỏ qua validate).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ bộ TC | **42/61 TC Đạt (68,9%) — dưới ngưỡng 80%**. 19 TC chưa có kết luận: 10 chưa chạy (NEW-47 → NEW-57), 8 skip, 1 blocked. Thêm vào đó:<br>- Run staging #2396 kết thúc lúc 06:27Z, **trước** journal Dev báo commit `e8931817a2` (08:18Z). Studio `dev_impact` ghi tip branch đã merge `release_step_20260930`.<br>- Không xác nhận được 42 pass chạy trên build nào.<br>- Các TC chạm đúng 4 commit mới (đồng thời, 指名, hạn mức, job) đều pass **trước** mốc đó: NEW-43, NEW-19, #20824, NEW-1/2/3, #20829, NEW-46, NEW-37 | Chờ run staging #2431 (đang queued) xong, đối chiếu commit đã deploy = `e8931817a2` hoặc tip `8fd8a99592`. Chạy lại manual nhóm TC trên, và chạy lần đầu 10 TC mới |
| I2 | `[MAJOR]` | Job — NEW-1, NEW-2, NEW-3, NEW-54, #20829 | Auto runner skip toàn bộ TC job: `[SOURCE_BLOCKED] job: SOURCE_BRANCH_MISSING: project job chưa có branch run`. NEW-54 (job + nghỉ trước, trúng thay đổi `breakTimeFirstApplied` của cả 2 job) **chưa chạy lần nào**. 4 TC job còn lại chỉ có manual pass trước commit cuối | Cấu hình branch cho project job trên runner, hoặc chạy manual trên staging sau khi deploy `e8931817a2` |
| I3 | `[MAJOR]` | Phạm vi Leader chốt 2026-09-29 (report vòng 1 §1b) | Leader thu hẹp 3 option ngoài 上限を設定する vì "code nhánh không đổi". Dev #139287 + #139421 nói ngược lại: cả 3 option × 2 luồng đều bị chạm. Các ô **giữa ca cộng dồn nghỉ** / **qua ngày** / **không cài nghỉ** của 上限を設定しない và 合算する hiện 0 TC | Leader quyết lại: (a) giữ phạm vi, chỉ thêm G1–G3; hoặc (b) mở rộng các ô trên sang 上限を設定しない + 合算する. Quy tắc "option 3 fail ô nào → mở rộng ô đó" của vòng 1 không áp được, vì lý do thu hẹp đã mất |
| I4 | `[MAJOR]` | RULE-08 / ENV-003 — NEW-43, NEW-52, NEW-53, job | Task chạm **job nền**, **chống đặt trùng nhiều server** và **bill tiền**, nhưng 0 TC chạy production. NEW-43 (2 khách đồng thời, bug #41743) chỉ pass staging | Sau release: chạy NEW-43 trên product. Luồng thanh toán product theo kho `TC-SLN-412` |
| I5 | `[MAJOR]` | `NEW-12` (TC tái hiện bug bắt buộc) | **Mâu thuẫn nội bộ**:<br>- Steps + Expected đã đổi sang bộ dữ liệu của chị Quyên (NV-A 12:00–20:30, NV-B 12:00–18:30, đơn NV-A 17:30, xem khung 16:00 / 16:30).<br>- Precondition + Dữ liệu + Tên TC vẫn là bộ N1 cũ (NV-A 12:00–20:00, NV-B 14:30–21:00 bận 19:30–21:00, xem khung 17:30).<br>- Không biết lần pass run #2396 chạy theo bộ nào | Sửa Precondition + Dữ liệu + Tên theo đúng Journal #139305, rồi chạy lại. Đây là TC tái hiện chính thức, đang có oracle BẬT/TẮT từ Dev #139421 |
| I6 | `[MAJOR]` | `NEW-18`, `NEW-19`, `#20843`, `#20844` | Expected đã viết lại theo quy tắc, nhưng `env_scope` vẫn = `local` và precondition NEW-18 / NEW-19 còn dòng "cần có sẵn nhánh release và nhánh fix trên local để so sánh". #20843 / #20844 bị skip trên staging vì lý do này | Đổi `env_scope` = Tất cả, xóa dòng so 2 nhánh. #20843 / #20844 đổi `tc_group` sang `ui` (các bước đều thao tác trên LIFF), rồi chạy trên staging |
| I7 | `[MAJOR]` | `NEW-52` · luồng "trả sau" | NEW-52 ghi "Stripe **hoặc** Univapay". Hai cổng đi 2 đường code khác nhau (`paymentStripe:1588` / `paymentUnivapay:1824`), chạy 1 cổng thì bỏ sót cổng kia. Dev #139421 còn nêu "tra sau", nhưng kho FA-020 (nhóm 決済) và spec không có luồng trả sau cho salon → `Input thiếu: "trả sau" là luồng nào` | Chạy NEW-52 **2 lần** (Stripe + UnivaPay), ghi rõ cổng vào kết quả. Hỏi Dev "trả sau" là luồng / màn nào; có thật thì bổ sung 1 lần chạy nữa |
| I8 | `[MAJOR]` | `NEW-49`, `NEW-52`, `NEW-53` | `env_scope` = `local`. NEW-52 / NEW-53 dùng khoá thử cổng thanh toán, mà kho `TC-SLN-402` đã chạy được Stripe TEST trên môi trường test. Để local thì luồng thanh toán không bao giờ được xác nhận ngoài máy dev | NEW-52 / NEW-53: đổi `env_scope` gồm staging. NEW-49 cần dừng hàng đợi nên giữ local là hợp lý |
| I9 | `[MAJOR]` | Số đo của Dev | Journal #139287 tự mâu thuẫn: phần verify ghi "chế độ gộp ca còn **27 chặn oan / 3 lỗ hổng**", phần 4.3 ghi "0 nới sai". Journal #139421: "chặn oan 1491 → **8**". Chưa rõ 8 ô chặn oan và 3 lỗ hổng gộp ca (mở oan = có thể đặt trùng) còn ở `e8931817a2` không | Hỏi Dev danh sách cụ thể 8 ô + 3 ô gộp ca. Ô nào còn → đẻ TC Boundary cho đúng ô đó. G2 ở §7 mới chỉ phủ 2 hướng tổng quát |
| I10 | `[MAJOR]` | `#20823`, `#20824`, `#20822` (còn từ vòng 1, I6) | Tiền điều kiện vẫn không dựng lại được: #20823 ghi "Đã deploy nhánh **ai_fixbug_40128**". #20824 tham chiếu `client_ref task213…` của task khác. #20822 ghi "Cùng cấu hình như TC khung 19:00", không khai option 受付上限. Expected phần admin của #20823 → §4 C2 | Sửa trên Studio như đề xuất vòng 1 |
| I11 | `[MAJOR]` | `NEW-1` (còn từ vòng 1, I11), `NEW-6` (I9) | NEW-1: "chỉ định thứ tự **hoặc** ngẫu nhiên" làm expected không xác định. NEW-6 vẫn gộp 2 bộ dữ liệu D1 / D2 (không atomic). NEW-7 đã sửa xong (K125), đóng | NEW-1: chốt 優先順位 với NV-B đứng đầu (như NEW-46). NEW-6: tách D1 / D2 |
| I12 | `[NIT]` | Job phía khách — bỏ +1 phút (Dev #139421 mục 4) | Không dựng được qua UI (bước course 5 phút). Studio NEW-54 ghi 2 thay đổi triệt tiêu nhau | Nhờ Dev xác nhận đã có unit test cho mốc này (PHPUnit 69/69), không đẻ TC |
| I13 | `[MINOR]` | `NEW-55`, `NEW-56`, `NEW-57`, `NEW-20` | Thiếu Mã quan điểm liên kết (viewpoint trống). NEW-55/56/57 đặt `exec_mode = manual` nhưng không thuộc 4 lý do cho phép (đều là thao tác LIFF) | Gắn `REG-SHARED-001` (NEW-55/56/57) và `FUNC-001` (NEW-20). Đổi sang `auto` |
| I14 | `[MAJOR]` | Spec FA-020 (còn từ vòng 1, I2) | Vẫn không có spec cho quy tắc tính khung trống. Toàn bộ oracle dựa trên quy tắc Leader chốt 2026-09-29 + journal Dev | §8 #1 |
| I15 | `[NIT]` | Mục 3 của Dev (Journal #139287) | Danh sách caller chưa cập nhật theo 4.1: `checkLimitHasStaff` ghi "KHÔNG sửa" nhưng 4.1 + #139421 ghi đã sửa | Nhờ Dev cập nhật mục 3 cho khớp |
| I16 | `[NIT]` | NEW-41 · rủi ro OEM | NEW-41 blocked là đúng (chỉ chạy sau release, cần CS/OEM 31074 đồng ý). Dev vẫn khuyến nghị báo trước OEM: lịch sẽ "thoáng" hơn, nay áp cả 3 option | Theo dõi sau release. Nhắc CS trước khi release |

---

## 6. TCs thừa / ngoài phạm vi task

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| X1 | `NEW-2` (còn từ vòng 1) | Test **layer không bị chạm**: chạy lại job cho đơn đã có NV không gán lại / không nhân đôi. 2 dòng đổi ở job (`breakTimeFirstApplied`, bỏ +1 phút) chỉ đổi phép kiểm khả dụng, không đổi tính idempotent | Dev 4.1: job +2/−1 dòng mỗi file | Chuyển sang bộ regression chung của kho (nhóm スタッフ自動割り当て) | `[NIT]` |
| X2 | `NEW-40` | Test **lưới admin 予約カレンダー**, không có dòng code nào đổi trong 4.1 của Dev. Sau khi reject bug #1509, TC này chỉ còn xác nhận hành vi cũ "admin không cắt slot theo Course" | Dev 4.1 (4 file prod, không có `Basic/CalendarSalonController`) · reject #1509 | Chuyển sang kho, nhóm "Admin thêm booking thủ công" (cạnh `TC-SLN-115`) | `[NIT]` |

- **Rút lại X2 → X7 của vòng 1** (NEW-18, #20843, #20844, #20823, #20824, NEW-19). Vòng 1 đề nghị bỏ 6 TC này vì "option khác option 3 / 指名 không đổi code". Dev nay xác nhận cả 3 option × 2 luồng đều bị chạm, và các TC này đã được viết lại theo quy tắc → **giữ lại** (sửa theo §5 I6 / I10).
- **Gate đã chạy**:
  - NEW-2 không phải TC duy nhất cover T4 (còn NEW-1, NEW-54, #20829).
  - NEW-40 không phải TC duy nhất cover lưới admin (#20823 cũng có, sau khi sửa theo C2).

---

## 7. TCs đề xuất bổ sung (12)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa020-datlichsalon-サロン・面談予約.md` — nhóm 受付上限 (TC-SLN-277..290), 前後の空き時間 (291..294), 決済 — thẻ & 3D Secure (402..414), Admin thêm booking thủ công (115), Modal lý do (122) |
| Vùng regression phát hiện từ kho | `TC-SLN-402` (Stripe TEST đặt lịch có thanh toán) · `TC-SLN-407` (Stripe 3D Secure) · `TC-SLN-413` (UnivaPay có / không webhook) — luồng thanh toán nay có phép kiểm lại chèn trước bước trừ tiền |
| Conflict expected vs kho | Không có TC đề xuất nào trái kho. C1 (TC-SLN-293) chỉ liên quan TC đã có trên Studio |
| GAP dùng lại TC kho (không viết mới) | Không. Kho `TC-SLN-402` / `413` dùng cấu hình không có 受付上限 / NV lệch ca, nên chỉ lấy luồng làm căn cứ, viết lại trên cấu hình N1 của bug |
| Căn cứ TC regression `R<x>` | Không có TC R riêng. Phần regression thanh toán gộp vào G4 (dẫn từ `TC-SLN-402` / `407` / `413`) |
| Xác nhận chống trùng | Đã đối chiếu 61 TC ở BƯỚC 0 + kho FA-020 — **không TC đề xuất nào trùng**:<br>- `TC-FUNC004-06` / `-07` là bản ở option 上限を設定しない của NEW-47 / NEW-48 (2 TC đó chỉ ở option 上限を設定する).<br>- `TC-FUNC004-08` / `-09` là đối chứng âm của NEW-37.<br>- `TC-FUNCDATE001-12` khác NEW-19 / NEW-28 ở chỗ NV **khác** tan ca trong phần 片付け.<br>- `TC-PAYSTATE001-01` / `-02` là happy path; NEW-52 / 53 chỉ có nhánh lỗi.<br>- `TC-FUNC004-10` / `-11` và `TC-FUNCDATE001-13` / `-14` / `-15` (calendar 個人): 0 TC Studio dùng calendar 個人. `-10` / `-11` viết lại kịch bản kho `TC-SLN-290` trên dữ liệu có mốc giờ cụ thể; kho TC đó để tiền điều kiện lẫn lộn (ghi cả loại スタッフ lẫn 個人) nên không dùng lại nguyên được |

> Quy ước **Option limit** (Leader chốt 2026-09-29): **1.1** = シフトの合算をしない · **1.2** = シフトの合算をする · **2** = 上限を設定しない · **3** = 上限を設定する (kèm setting limit N). "Staff A set limit 1" = スタッフごとの同時受付上限 của Staff A = 上限を設定する 1.

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-FUNC004-06 | UI | FUNC-004 | LINE user — chọn slot | Abnormal | auto | Tất cả | Option 2: 2 staff bận lệch nửa khung → khung OFF | - Option limit: 2<br>- Staff A set limit 1, Staff B set limit 1<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h (Staff A, B cùng phụ trách)<br>- Ngày X: Staff A ca 12:00–21:00, có booking 19:00–20:00 · Staff B ca 12:00–21:00, có booking 18:00–19:00 | 1. LIFF: chọn course 2h, 指名なし, ngày X<br>2. Xem khung 18:00 và 16:00 | Course 2h · 指名なし · ngày X | - 18:00: OFF (không staff nào rảnh trọn 18:00–20:00)<br>- 16:00: ON |  | Lấp G1 · Dev #139421: cổng hasStaffCanTakeWholeRange áp cả option 2 · bản option 2 của NEW-47 · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 (option 2 giống 1.1: 1 staff làm trọn vẹn) · Evidence: ảnh lưới LIFF + 予約管理 ngày X |
| TC-FUNC004-07 | UI | FUNC-004 | 受付上限 — 店舗・スタッフ | Boundary | auto | Tất cả | Option 2: limit staff tính theo số booking cùng lúc — 2 booking nối tiếp còn suất, 2 booking chồng giờ hết suất | - Option limit: 2<br>- Staff A set limit 2, Staff B set limit 1<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h (Staff A, B cùng phụ trách)<br>- Ngày X: Staff A ca 12:00–21:00 · Staff B ca 12:00–21:00, có booking 18:00–20:00 | 1. 予約管理: tạo cho Staff A 2 booking nối tiếp 18:00–19:00 và 19:00–20:00<br>2. LIFF: chọn course 2h, 指名なし, ngày X → xem khung 18:00<br>3. 予約管理: sửa booking thứ 2 của Staff A thành 18:30–19:30<br>4. Tải lại LIFF → xem lại khung 18:00 | Course 2h · 指名なし · ngày X | - Bước 2: 18:00 ON (Staff A lúc nào cũng chỉ bận 1 booking)<br>- Bước 4: 18:00 OFF (Staff A bận 2 booking cùng lúc 18:30–19:00, Staff B đã hết limit) |  | Lấp G1 · Dev #139421 mục 1 (commit c6adf066a8) + cách đếm limit áp cả option 2 · bản option 2 của NEW-48 · Môi trường: Tất cả · Spec không ghi — theo journal Dev · Evidence: ảnh LIFF bước 2 + bước 4 |
| TC-FUNC004-08 | UI | FUNC-004 | 受付上限 — 店舗・スタッフ | Abnormal | auto | Tất cả | Option 1.2: 2 ca có khoảng hở 30 phút → không tiếp sức được, khung OFF | - Option limit: 1.2<br>- Staff A set limit 1, Staff B set limit 1<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h (Staff A, B cùng phụ trách)<br>- Ngày X: Staff A ca 10:00–11:00 · Staff B ca 11:30–13:30 · chưa có booking | 1. LIFF: chọn course 2h, 指名なし, ngày X<br>2. Xem khung 10:00, 10:30, 11:30 | Course 2h · 指名なし · ngày X | - 10:00: OFF<br>- 10:30: OFF (11:00–11:30 không staff nào trong ca)<br>- 11:30: ON (Staff B làm trọn) |  | Lấp G2 · đối chứng âm của NEW-37 · Dev #139287: gộp ca áp cả 合算をする + lateral_scan "gộp ca còn 3 lỗ hổng" · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 (1.2 = staff tiếp sức nhau) · Evidence: ảnh lưới LIFF ngày X |
| TC-FUNC004-09 | UI | FUNC-004 | 受付上限 — 店舗・スタッフ | Abnormal | auto | Tất cả | Option 1.2: staff nối ca đang bận phần sau → không tiếp sức được, khung OFF | - Option limit: 1.2<br>- Staff A set limit 1, Staff B set limit 1<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h (Staff A, B cùng phụ trách)<br>- Ngày Y: Staff A ca 10:00–11:00 · Staff B ca 11:00–12:00, có booking 11:00–12:00 | 1. LIFF: chọn course 2h, 指名なし, ngày Y → xem khung 10:00<br>2. 予約管理: xóa booking 11:00–12:00 của Staff B<br>3. Tải lại LIFF → xem lại khung 10:00 | Course 2h · 指名なし · ngày Y | - Bước 1: 10:00 OFF (Staff B bận, không ai nối tiếp Staff A)<br>- Bước 3: 10:00 ON (Staff A 10:00–11:00 → Staff B 11:00–12:00) |  | Lấp G2 · đối chứng âm của NEW-37 (cùng ca, chỉ thêm booking bận) · Dev #139287 lateral_scan "gộp ca còn 3 lỗ hổng" · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 · Evidence: ảnh LIFF bước 1 + bước 3 |
| TC-FUNCDATE001-12 | UI | FUNC-DATE-001 | LINE user — chọn コース/スタッフ | Boundary | auto | Tất cả | Option 3 + chọn đích danh Staff A: staff khác tan ca trong thời gian nghỉ sau không làm OFF khung của Staff A | - Option limit: 3, setting limit 2<br>- Staff A set limit 1, Staff B set limit 1<br>- Nghỉ sau 60 phút<br>- Đơn vị nhận đặt 30 phút · Course 2h (Staff A, B cùng phụ trách)<br>- Ngày X: Staff A ca 12:00–21:00, rảnh · Staff B ca 12:00–20:00, có booking 18:30–19:30 (nghỉ sau tới 20:30, tràn qua giờ tan ca) | 1. LIFF: chọn course 2h, chọn đích danh Staff A, ngày X<br>2. Xem khung 18:00, 19:00, 19:30<br>3. Đặt khung 18:00 → mở booking trên 予約管理 | Course 2h · Staff A · ngày X | - 18:00: ON · 19:00: ON<br>- 19:30: OFF (phục vụ tới 21:30, vượt ca Staff A)<br>- Booking tạo ra: Staff A, 18:00–20:00 |  | Lấp G3 · Dev #139421 mục 2 (commit 23492bfad5: nhánh 指名 xét ca staff khác tại mốc giờ phục vụ) · Studio dev_impact "checkLimitHasStaff NAY cũng sửa" · Môi trường: Tất cả · Spec không ghi — quy tắc #40128 / Leader 2026-09-29 (nghỉ sau được tràn qua giờ tan ca) · Evidence: ảnh LIFF + chi tiết booking |
| TC-PAYSTATE001-01 | UI | PAY-STATE-001 | 決済 — thẻ & 3D Secure | Normal | auto | Tất cả | Đặt lịch có thanh toán Stripe (3D Secure) ở khung vừa mở: thành công, trừ tiền 1 lần | - Bot plan có phí (standard trở lên)<br>- Option limit: 3, setting limit 2<br>- Staff A set limit 1, Staff B set limit 1<br>- Nghỉ sau 60 phút<br>- Đơn vị nhận đặt 30 phút · Course 2h giá 5,000 yên (Staff A, B cùng phụ trách)<br>- 決済連携: bật Stripe, môi trường テスト · 質問項目: bật 名前 + メール<br>- Ngày X: Staff A ca 12:00–20:00, rảnh · Staff B ca 14:30–21:00, có booking 19:30–21:00 | 1. LIFF: chọn course 2h, 指名なし, ngày X, khung 18:00<br>2. Điền form, nhập thẻ test Stripe có 3D Secure, xác thực xong<br>3. Xem màn hoàn tất + tin nhắn LINE<br>4. 予約管理: mở booking, xem staff + tab 決済情報<br>5. Dashboard Stripe (test): đếm giao dịch | Thẻ test Stripe có 3D Secure · khung 18:00 ngày X | - Đặt thành công, không hiện 予約がいっぱいです。別の枠を予約してください。<br>- Đúng 1 booking 18:00–20:00, staff A<br>- 決済金額 5,000 yên, hệ thống thanh toán Stripe<br>- Stripe có đúng 1 giao dịch 5,000 yên<br>- LINE user nhận tin hoàn tất |  | Lấp G4 · Lấp Q1 · regression — dẫn từ TC-SLN-402, TC-SLN-407 · Dev #139421 mục 5 (kiểm lại chỗ trống trước bước trừ tiền, paymentStripe) · Môi trường: Tất cả với khoá test; product theo TC-SLN-412 sau release (RULE-08) · Spec không ghi · Evidence: màn hoàn tất + tab 決済情報 + dashboard Stripe |
| TC-PAYSTATE001-02 | UI | PAY-STATE-001 | 決済 — thẻ & 3D Secure | Normal | auto | Tất cả | Đặt lịch có thanh toán UnivaPay ở khung vừa mở: thành công, trừ tiền 1 lần | - Giống TC-PAYSTATE001-01, chỉ khác:<br>- 決済連携: bật UnivaPay (môi trường test, có webhook)<br>- Dùng ngày Y (ca + booking giống ngày X) | 1. LIFF: chọn course 2h, 指名なし, ngày Y, khung 18:00<br>2. Điền form, nhập thẻ test UnivaPay, xác nhận<br>3. Xem màn hoàn tất (không treo) + tin nhắn LINE<br>4. 予約管理: mở booking, xem tab 決済情報<br>5. Màn quản lý UnivaPay (test): đếm giao dịch | Thẻ test UnivaPay · khung 18:00 ngày Y | - Đặt thành công, không hiện 予約がいっぱいです。別の枠を予約してください。<br>- Đúng 1 booking 18:00–20:00<br>- 決済金額 5,000 yên, hệ thống thanh toán UnivaPay<br>- UnivaPay có đúng 1 giao dịch 5,000 yên<br>- LINE user nhận tin hoàn tất |  | Lấp G4 · Lấp Q1 · regression — dẫn từ TC-SLN-413, TC-SLN-145 · Dev #139421 mục 5 (paymentUnivapay) · Môi trường: Tất cả với khoá test; product theo TC-SLN-412 sau release · Spec không ghi · Evidence: màn hoàn tất + tab 決済情報 + màn UnivaPay |
| TC-FUNC004-10 | UI | FUNC-004 | 受付上限 — 店舗・スタッフ | Normal | auto | Tất cả | Calendar 個人 · Option 2: nhiều booking cùng khung vẫn đặt được | - Calendar loại 個人 (chỉ có staff 運営者)<br>- Option limit: 2<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h<br>- Giờ làm việc ngày X: 12:00–20:00 · chưa có booking<br>- 3 LINE user U1, U2, U3 | 1. U1: LIFF chọn course 2h, ngày X, đặt khung 14:00<br>2. U2: làm giống U1, đặt khung 14:00<br>3. U3: làm giống U1, xem khung 14:00 rồi đặt<br>4. 予約管理 ngày X: đếm booking khung 14:00 | Course 2h · ngày X · khung 14:00 | - U1, U2, U3 đều đặt thành công, khung 14:00 luôn ON<br>- 予約管理 có 3 booking 14:00–16:00 |  | Lấp G5 · regression — dẫn từ TC-SLN-290 (個人 + không giới hạn: đặt được nhiều booking cùng khung) · Dev #139421: cổng hasStaffCanTakeWholeRange + đếm limit theo lượt đồng thời áp cả option 2 → nguy cơ chặn oan booking thứ 2 vì 個人 chỉ có 1 staff · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF của U3 + 予約管理 |
| TC-FUNC004-11 | UI | FUNC-004 | 受付上限 — 店舗・スタッフ | Boundary | auto | Tất cả | Calendar 個人 · Option 3 limit 2: booking thứ 3 cùng khung bị chặn, khung nối tiếp vẫn ON | - Calendar loại 個人 (chỉ có staff 運営者)<br>- Option limit: 3, setting limit 2<br>- Không cài thời gian nghỉ trước / sau<br>- Đơn vị nhận đặt 30 phút · Course 2h<br>- Giờ làm việc ngày X: 12:00–20:00 · chưa có booking | 1. U1, U2 lần lượt đặt khung 14:00 ngày X<br>2. U3: LIFF chọn course 2h, ngày X, xem khung 12:00, 12:30, 14:00, 15:30, 16:00 | Course 2h · ngày X | - Bước 1: U1, U2 đều đặt thành công<br>- 12:00: ON (kết thúc đúng 14:00, nối tiếp)<br>- 12:30: OFF · 14:00: OFF · 15:30: OFF (chồng 2 booking = đủ limit 2)<br>- 16:00: ON (nối tiếp sau booking) |  | Lấp G5 · regression — dẫn từ TC-SLN-290 (個人 + limit 2: booking thứ 3 bị chặn) · Dev #139421 mục 1: limit tính theo số booking cùng lúc (2 booking nối tiếp không làm hết suất) · Môi trường: Tất cả · Spec không ghi · Evidence: ảnh LIFF của U3 |
| TC-FUNCDATE001-13 | UI | FUNC-DATE-001 | LINE user — chọn slot | Boundary | auto | Tất cả | Calendar 個人 · Option 3 limit 1: khung kết thúc đúng giờ làm việc vẫn ON, nghỉ sau được tràn | - Calendar loại 個人 (chỉ có staff 運営者)<br>- Option limit: 3, setting limit 1<br>- Nghỉ sau 60 phút<br>- Đơn vị nhận đặt 30 phút · Course 2h<br>- Giờ làm việc ngày X: 12:00–20:00 · chưa có booking | 1. LIFF: chọn course 2h, ngày X<br>2. Xem khung 18:00 và 18:30<br>3. Đặt khung 18:00 → mở booking trên 予約管理 | Course 2h · ngày X | - 18:00: ON, đặt thành công (phục vụ 18:00–20:00 trong giờ làm, cuối ca không tính nghỉ sau)<br>- 18:30: OFF (phục vụ tới 20:30, vượt giờ làm)<br>- Booking tạo ra: 18:00–20:00 |  | Lấp G5 · Dev #139287 (#41746: khung cuối ca không bị ẩn, bỏ +1 phút) · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 (cuối ca không tính nghỉ sau) · Evidence: ảnh LIFF + chi tiết booking |
| TC-FUNCDATE001-14 | UI | FUNC-DATE-001 | 前後の空き時間 | Boundary | auto | Tất cả | Calendar 個人 · Option 2: đầu giờ không tính nghỉ trước, cuối giờ không tính nghỉ sau | - Calendar loại 個人 (chỉ có staff 運営者)<br>- Option limit: 2<br>- Nghỉ trước 30 phút + nghỉ sau 30 phút<br>- Đơn vị nhận đặt 30 phút · Course 2h<br>- Giờ làm việc ngày X: 12:00–20:00 · chưa có booking | 1. LIFF: chọn course 2h, ngày X<br>2. Xem khung 12:00, 18:00, 18:30<br>3. Đặt khung 12:00 → mở booking trên 予約管理 | Course 2h · ngày X | - 12:00: ON, đặt thành công (đầu ca không tính nghỉ trước)<br>- 18:00: ON (cuối ca không tính nghỉ sau)<br>- 18:30: OFF (phục vụ tới 20:30, vượt giờ làm)<br>- Booking tạo ra: 12:00–14:00 |  | Lấp G5 · Dev #139287 (#41742: nghỉ trước được nằm trước giờ vào ca; #41746: khung cuối ca) + #139421 (áp cả option 2) · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 · ⚠ kho TC-SLN-293 ghi ngược (§4 C1) · Evidence: ảnh LIFF + chi tiết booking |
| TC-FUNCDATE001-15 | UI | FUNC-DATE-001 | 前後の空き時間 | Boundary | auto | Tất cả | Calendar 個人 · Option 3 limit 1: giữa ca cộng dồn nghỉ sau + nghỉ trước (booking 10:00–12:00 → khung tiếp theo 13:00) | - Calendar loại 個人 (chỉ có staff 運営者)<br>- Option limit: 3, setting limit 1<br>- Nghỉ trước 30 phút + nghỉ sau 30 phút<br>- Đơn vị nhận đặt 30 phút · Course 2h<br>- Giờ làm việc ngày X: 10:00–20:00 · có booking 10:00–12:00 | 1. LIFF: chọn course 2h, ngày X<br>2. Xem khung 12:00, 12:30, 13:00<br>3. Đặt khung 13:00 → mở booking trên 予約管理 | Course 2h · ngày X | - 12:00: OFF · 12:30: OFF (chưa đủ nghỉ sau 30' + nghỉ trước 30')<br>- 13:00: ON, đặt thành công<br>- Booking tạo ra: 13:00–15:00 |  | Lấp G5 · bản calendar 個人 của NEW-23 · Môi trường: Tất cả · Spec không ghi — quy tắc Leader chốt 2026-09-29 (giữa ca cộng dồn, ví dụ của Leader) · ⚠ kho TC-SLN-293 ghi ngược (§4 C1) · Evidence: ảnh LIFF + chi tiết booking |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/salon-booking/feature-spec.md` §2.4.3 + §2.4.4 + §5 Business Rules (còn từ vòng 1) | Ghi quy tắc Leader chốt 2026-09-29 thành BR:<br>- Giờ PHỤC VỤ phải nằm trọn trong ca, 片付け / chuẩn bị được tràn ra ngoài ca.<br>- Đầu ca bỏ nghỉ trước, cuối ca bỏ nghỉ sau, giữa ca cộng dồn.<br>- 4 option 受付上限: シフトの合算をしない / 上限を設定しない = 1 staff trọn vẹn · シフトの合算をする = tiếp sức · 上限を設定する = cả limit calendar + staff, không tiếp sức.<br>- Hạn mức staff = số lượt **đồng thời** (mới, #139421) | §5 I14 | Leader |
| 2 | `kho-tcs/data/fa020_*.py` → `TC-SLN-293` (còn từ vòng 1) | Sửa expected nhánh "Cả 2" theo quy tắc Leader: slot sau = hết đơn + nghỉ sau + nghỉ trước. Slot đầu ca đặt được, không tính nghỉ trước. NEW-22 / 23 / 26 / 27 đã pass staging theo quy tắc này. Build lại kho (`python kho-tcs/build.py md` + `sheet`) | §4 C1 | Leader |
| 3 | Spec §2 (予約カレンダー admin) + Studio `#20823` | Ghi rule "lưới admin 予約カレンダー hiển thị khung ON đến hết giờ làm việc, không cắt theo thời lượng Course". Nguồn: lý do reject bug Studio #1509. Sửa expected phần admin của #20823 cho khớp | §4 C2 | Leader |
| 4 | Spec §5 BR — option 上限を設定しない | Dev #139421: khung đặt **sát nhau** (buổi kết thúc đúng lúc lượt sau bắt đầu) ở option 上限を設定しない vẫn bị chặn, "có thể là buffer cố ý, chờ BA xác nhận". Chốt đây là thiết kế hay bug. Là bug → raise ticket riêng, không chặn release #41448 | Dev #139287 4.3 "CÒN TỒN" | PM / Leader |
| 5 | Spec 決済 — luồng hủy / bỏ dở thanh toán | Chốt oracle: khách hủy / bỏ dở ở bước nhập thẻ hoặc 3D Secure thì đơn tạm có còn **giữ khung** không, sau bao lâu thì nhả. Nay phép kiểm lại chỗ trống đếm cả đơn có id nhỏ hơn, nên đơn tạm treo có thể chặn oan khách sau. Kho `TC-SLN-407` đang ghi 2 khả năng ("không tạo booking hoặc booking không được thanh toán") | §2 Q2 | Dev / Leader |
| 6 | Journal Dev #139421 mục 5 | Làm rõ "tra sau" (trả sau) là luồng thanh toán nào của salon. Kho + spec FA-020 chỉ có Stripe / UnivaPay | §5 I7 | Dev |
