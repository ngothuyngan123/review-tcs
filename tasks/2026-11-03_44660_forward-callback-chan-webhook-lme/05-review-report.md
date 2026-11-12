# 05 — Review Report

> Draft cho Leader verify. Ticket #44660 · Studio task #526 (round 1, HEAD `676e01b687cc`).

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #526 (ticket 44660, round 1) |
| Tổng số TC review | 18 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 5/7 mục có TC (BUG · F1 · F2 · D1 · T1 · T2 · T3; trừ T4 — cập nhật tài liệu spec, xử lý ở §8 #1) — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` | 6/8 điểm có TC (trừ file `tests/Unit/WebhookUrlValidatorLmeWebhookTest.php` — code test, không phải hành vi; xem §5 I6) — **CHƯA ĐỦ** |

**Kết luận**: 9/11 vùng ảnh hưởng đủ TC · 1 GAP · 1 RISK

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | T3 — job chuyển tiếp (`HandleForwardCallbackEventTask` / `HandleForwardLmeEventTask`) với cấu hình cũ đã lưu URL webhook LME trước bản sửa | `dev-impact` (T3) · `diff code` (câu 5 — nhánh Dev nói "job java không đổi") | không có (NEW-14, NEW-15 chỉ kiểm màn web, ghi chú "job ngoài phạm vi") | GAP — quy tắc mới "không chuyển tiếp về webhook LME" không áp ở job (code job không đổi). Dev khẳng định cấu hình cũ "chỉ bị 401 + hiện 「転送エラー」" (journal #149730, phụ thuộc #43730) nhưng 0 TC chứng minh không vòng lặp | `[MAJOR]` |
| G2 | T1 — tab 「LINE公式アカウントデータ転送」 với bước chuẩn hoá path của bàn giao #2 (`\`, `%5C`, `/line/%2e/`, `..` ở gốc, `.` cuối path) | `dev-impact` (T1) · `diff code` (dev_impact bàn giao #2) | NEW-6 (3 URL, chỉ công tắc TẮT) · bộ đủ chỉ có ở tab LME (NEW-18) | RISK — journal #150058 yêu cầu re-test "cả tab LINE và tab LME, công tắc bật và tắt"; tab LINE thiếu `\` / `%5C` / `%2e` đơn và mọi dòng BẬT | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 13 quan điểm Trigger khớp task · 8 chưa cover đủ (6 dòng dưới · `ENV-003` → §5 I1 · `INTG-HOOK-001` → §1 G1)

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | RISK — luồng chính (lưu URL hợp lệ / chặn URL webhook LME) chỉ cover bởi TC mã lạ: NEW-1, NEW-9 (`TOOL-NEGCTRL-001`), NEW-2, NEW-10 (`TOOL-KNOW-002`). Đổi mã 4 TC này → `FUNC-001`; Boundary ghi lý do "luồng chính không có biên — biên ở FUNC-003/FUNC-004". Không cần TC mới | `[MAJOR]` |
| Q2 | `FUNC-003` | Cao (webhook URL) | RISK — 6 TC (NEW-3, 4, 6, 11, 12, 18) đều Abnormal, thiếu Normal + Boundary (RULE-01); phần gọi thẳng API chỉ ở NEW-16, NEW-17 mang mã lạ. Đổi mã NEW-16 (Normal), NEW-17 (Abnormal) → `FUNC-003` + 1 TC Boundary mới (§7 `TC-FUNC003-02`) | `[MAJOR]` |
| Q3 | `COMPAT-LEGACY-001` | Cao | RISK — cấu hình lưu trước bản sửa (mở → lưu lại) chỉ cover bởi NEW-14, NEW-15 mang mã lạ `TOOL-OLDREC-001`. Nội dung đủ 2 nhánh (giữ URL cũ → chặn · đổi URL hợp lệ → lưu được) → chỉ đổi mã, không cần TC mới | `[MAJOR]` |
| Q4 | `REG-SPEC-001` | Cao | RISK — requirement đổi sau khi đã có TC (bàn giao #2 thêm REQ-009: `./..`, `%2e`, `\`, `%5C`) nhưng TC tab LINE chưa rà lại: NEW-6 vẫn 3 URL, chỉ TẮT, tiêu đề/ghi chú "chờ PO". Lấp bằng §7 `TC-FUNC003-01` + sửa NEW-6/NEW-4/NEW-12 (§5 I2) | `[MAJOR]` |
| Q5 | `FUNC-004` | Cao | RISK — 1 TC (NEW-8, Boundary); 5 pattern thiếu biên−1 (1023 ký tự); không tách Normal/Abnormal, chưa ghi lý do RULE-01. Không đề xuất TC mới (luật độ dài không đổi trong diff): thêm 2 dòng 1023 ký tự (có path webhook LME → chặn · không có → lưu được) vào data NEW-8 + ghi lý do RULE-01 | `[MAJOR]` |
| Q6 | `REG-SHARED-001` | Cao | RISK — NEW-7, NEW-13 đều Abnormal; dòng lưu được (Normal) và URL đúng 1024 ký tự (Boundary) nằm lẫn trong data, chưa ghi lý do RULE-01. Nội dung đủ → ghi lý do ở Ghi chú hoặc tách loại case; không cần TC mới | `[MINOR]` |

**Đã loại khỏi phạm vi** (Trigger khớp tên nhưng không có ảnh hưởng — có kiểm chứng):

| Mã | Lý do loại | Nguồn kiểm chứng |
|---|---|---|
| `DATA-BACKUP-001` | Copy bot không chép `webhook_relay_setting` | `feature-spec.md` §3.6 L617–635: ma trận CRUD không có tác nhân copy bot · grep `webhook_relay` trong `spec-features/` ngoài FA-047 = 0 file |
| `SYNC-APP-001` | App mobile / MCP không ghi cấu hình này | journal #149730 · #150058: "MCP và app mobile không ghi cấu hình này" |
| `JOB-001` | Diff không thêm/sửa job | `spec_delta.files[]` = 2 file PHP web — rủi ro job đã đưa vào G1 |
| `PERM-001` | Diff không chạm controller / middleware quyền | `spec_delta.files[]` = validator + unit test |

---

## 3. TC trùng lặp nội dung

Đã rà 18 TC, không phát hiện trùng lặp.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

- Cặp đã xét, không trùng: NEW-6 / NEW-18 (khác tab) · NEW-7 / NEW-13 (khác tab) · NEW-1 / NEW-16 (UI / API) · NEW-3 / NEW-4 (URL của chính bot vs biến thể).
- **Gate đã chạy**: không có đề nghị xóa → không áp dụng.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-SPEC` | NEW-14 | Bước 6–7: tab LINE lưu URL rỗng + TẮT, F5, đối chiếu DB | "DB endpoint_url = NULL, is_enabled = 0; **cột notify_\*** và signing_secret không đổi" | `feature-spec.md` L31 (§1.1 #4): "**mọi** lần mở cập nhật `errors_refreshed_at`, `notify_errors_refreshed_at`, `updated_at`" · L567: `notify_errors_refreshed_at` | (A) TC ghi quá rộng — ý là `notify_endpoint_url` / `notify_is_enabled` · (B) spec sai về mốc | `[MAJOR]` | Leader |
| C2 | `CONF-SPEC` | 13 TC chặn URL webhook LME: NEW-2…NEW-6, NEW-8, NEW-10…NEW-12, NEW-14, NEW-15, NEW-17, NEW-18 | Lưu 「転送先URL」 có path `/line/callback/add` (https, host public, cổng 443) | Bị chặn, 422 `URL_NOT_ALLOWED` 「このURLは転送先に指定できません。」 | `web/api-spec.md` L143–157 "Luật của 「転送先URL」": chỉ 9 luật — URL như vậy là hợp lệ | **✅ Leader chốt 2026-11-03: TC đúng — update spec (khả năng B)**. Đã thêm luật 8 / BR-11b vào `api-spec.md`, `feature-spec.md` §1.5+§5, `logic-spec.md` §12 (xem §8 #1) | `[MAJOR]` | Dev / PM |

**Đã rà**: 18 TC × `spec-features/admin/webhook-relay/feature-spec.md` (§1.1, §3.2, §3.6, §5 BR-06…BR-50) + `web/api-spec.md` (luật 「転送先URL」, mã lỗi). **kho-tcs chưa có FA-047** — không đối chiếu `CONF-KHO` được. Không có `CONF-TC`. Không có `CONF-IGNORE` (`ignore-features.md` chỉ có IG-01 Booking Manager — không khớp).

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn TC — RULE-08 / ENV-003 | 18/18 pass nhưng **0 TC chạy prd** (16 TC staging do AI chạy, 2 TC manual; local 4 lượt). Task chạm URL / domain webhook của từng env | Chạy lại NEW-2, NEW-10 (URL thật lấy ở 「LOA接続設定」) trên prd bằng bot test nội bộ — chỉ bước bị chặn + đối chứng TẮT. Xin phép trước: mở màn là ghi DB (`feature-spec.md` L31). Rủi ro thực tế thấp: luật dựa trên path, không gọi DNS |
| I2 | `[MAJOR]` | NEW-6 · NEW-4 · NEW-12 | Tiêu đề NEW-6 "(chờ PO chốt: bug sót hay chấp nhận)", Ghi chú "Dev đã thừa nhận bản sửa CHƯA chặn dạng này… không tự tạo bug trước khi PO chốt", requirement `REQ-008` — lỗi thời sau bàn giao #2 (#44843 đã sửa, có `REQ-009`). Ghi chú NEW-4, NEW-12 còn "dot-segment chờ PO". Re-test sau mà dot-segment lọt lại → tester theo ghi chú sẽ không raise bug | `testcase_update` NEW-6: bỏ "chờ PO", đổi sang `REQ-009`, ghi expected chặn là chuẩn (journal #150058). Sửa ghi chú NEW-4, NEW-12 |
| I3 | `[MAJOR]` | NEW-17 — RULE-13 | 2 dòng cuối (`/line/callback/add/%`, `%zz%00`) expected "HTTP 4xx có thông báo lỗi" | Ghi `400 hoặc 422` + `error_code` cụ thể; giữ câu "không 500" |
| I4 | `[MAJOR]` | NEW-2 · NEW-10 — RULE-07 | 2 TC tái hiện bug chỉ kiểm "không lưu" bằng F5 trên màn; DB chỉ kiểm ở NEW-14, NEW-15 (local, cấu hình cũ) | Thêm bước đối chiếu DB trước/sau: kênh 1 `endpoint_url`, `is_enabled` · kênh 2 `notify_endpoint_url`, `notify_is_enabled`, `signing_secret`. Chỉ các cột này — cột mốc đổi mỗi lần mở màn (§4 C1) |
| I5 | `[MINOR]` | NEW-14 | Mốc so `signing_secret` không rõ: seed "ghi thẳng DB" không nói INSERT hay UPDATE. Dòng mới chưa có secret → mở màn ở bước 1 sẽ sinh secret (BR-18, `feature-spec.md` L927) → "signing_secret không đổi" so với lúc seed sẽ sai | Ghi rõ: seed bằng UPDATE dòng đã có secret, hoặc chụp `signing_secret` sau bước 1 làm mốc |
| I6 | `[NIT]` | Unit test | "Điểm cần test" của Dev có "Chạy unit test WebhookUrlValidatorLmeWebhookTest" (29 ca) — không TC / evidence nào | Xin Dev link kết quả CI của HEAD `676e01b687` |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 18 TC — không có TC nào ngoài phạm vi task. NEW-7, NEW-13 (luật cũ), NEW-9, NEW-10 (secret không đổi), NEW-8 (thứ tự luật) đều dẫn được từ rủi ro hồi quy của Dev ("kiểm lại các lỗi cũ…", REQ-004, REQ-005).

| # | TC | Vì sao ngoài phạm vi | Bằng chứng | Đề xuất | Severity |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## 7. TCs đề xuất bổ sung (4)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | kho-tcs chưa có FA-047 — không đối chiếu được (grep `webhook_relay` trong `fa033` copy bot, `fa039` change bot = 0) |
| Vùng regression phát hiện từ kho | Không có |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho | Không |
| Căn cứ TC regression `R<x>` | R1 (TC-FUNC001-01) = happy-path job gửi webhook với URL hợp lệ, cả kênh LINE + kênh LME: RULE-06 (NEW-1/NEW-9 chỉ kiểm URL lưu được, chưa kiểm job forward tới output cuối) + `feature-spec.md` §2.8 / BR-44/45/46. Cũng là đối chứng cho G1 (chứng minh job đang forward trong env). Không có R từ "chặn nhầm URL ngoài" — đã lấp bằng Q2 |
| Xác nhận chống trùng | Đã đối chiếu 18 TC — không TC đề xuất nào trùng. `TC-FUNC003-01` khác NEW-6 (thêm `\` / `%5C` / `%2e` đơn + BẬT) và NEW-18 (tab LME). `TC-FUNC003-02` khác NEW-16, NEW-17 (data ranh giới chưa có) |

**Không đề xuất TC** cho Q1, Q3, Q6 (đủ nội dung, chỉ đổi mã / ghi lý do RULE-01) và Q5 (bổ sung 2 dòng data vào NEW-8).

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-INTGHOOK001-01 | Job | INTG-HOOK-001 | Webhook relay Webhook転送: Job chuyển tiếp với cấu hình cũ trỏ về webhook LME 「/line/callback/add」 | Abnormal | auto | dev, local, prd, staging | job, line-friend, web | Cấu hình cũ (lưu trước bản sửa) trỏ URL đích 「転送先URL」 về chính webhook LME: job chuyển tiếp bị LME từ chối 401, ghi Lỗi chuyển tiếp 「転送エラー」, không sinh callback_event mới (không vòng lặp) ở cả 2 kênh | - Đăng nhập admin chủ bot qua 「/login-v2」, chọn bot test riêng của TC (ghi bot_id khi chạy).<br>- Job chuyển tiếp của env đã bật cờ `ENABLE_FORWARD_WEBHOOK_CALLBACK=1` và `ENABLE_FORWARD_WEBHOOK_LME=1` (hỏi Dev / infra).<br>- Env đã deploy #43730 (xác nhận với Dev). Chưa có → ghi blocked, báo Leader.<br>- Sao chép URL Webhook ở 「LOA接続設定」 của bot test (dạng `<domain webhook>/line/callback/add/<bot_id>`), gọi là URL_LME.<br>- Ghi thẳng DB `webhook_relay_setting` của bot (giả lập cấu hình lưu trước bản sửa, bỏ qua validator): `endpoint_url` = URL_LME, `is_enabled` = 1, `notify_endpoint_url` = URL_LME, `notify_is_enabled` = 1.<br>- Chờ ≥ 60 giây sau khi ghi DB (job đọc cấu hình qua cache 60 giây).<br>- Bạn bè test `システム表示名 RLY_F01` (gọi tắt F01) đã kết bạn với bot.<br>- Bot có tag 「RLY_LOOP_TAG」, F01 chưa gắn tag này.<br>- Ghi lại số dòng `callback_event` của bot và số dòng 「転送エラー」 của 2 tab trước khi chạy. | 1. F01 gửi tin nhắn 「relay-loop-check」 tới bot trên LINE.<br>2. Chờ 2 phút.<br>3. Mở 「接続設定」→「Webhook転送」 (tab 「LINE公式アカウントデータ転送」 mở mặc định), bấm Làm mới 「最新に更新」 ở card 「転送エラー」.<br>4. Đối chiếu DB `callback_event` của bot: đếm dòng mới từ lúc bắt đầu bước 1.<br>5. Trên màn Friend list 友だちリスト, gắn tag 「RLY_LOOP_TAG」 cho F01.<br>6. Chờ 2 phút.<br>7. Bấm tab 「L Messageデータ転送」, bấm 「最新に更新」 ở card 「転送エラー」.<br>8. Đối chiếu DB `callback_event` của bot: đếm dòng mới từ lúc bắt đầu bước 5.<br>9. Recover data: ghi DB `is_enabled` = 0, `notify_is_enabled` = 0, `endpoint_url` / `notify_endpoint_url` về giá trị trước TC. | Tin F01: 「relay-loop-check」<br>Tag: 「RLY_LOOP_TAG」<br>URL_LME = URL Webhook ở 「LOA接続設定」 (ghi URL cụ thể khi chạy) | - Bước 3: card 「転送エラー」 tab LINE có đúng 1 dòng mới — Nội dung lỗi 「エラー内容」 = 「認証エラー」, Mã lỗi 「エラーコード」 = 401, Loại sự kiện 「イベント種別」 = message<br>- Bước 4: `callback_event` của bot tăng đúng 1 dòng (tin F01 gửi ở bước 1); không có dòng nào sinh từ request chuyển tiếp<br>- Bước 7: card 「転送エラー」 tab LME có đúng 1 dòng mới — 「認証エラー」, 401, 「イベント種別」 = tag<br>- Bước 8: `callback_event` của bot không tăng dòng nào (request kênh 2 bị từ chối) | | Lấp G1 · căn cứ: journal Dev #149730 mục Recover dữ liệu ("chỉ khiến lần chuyển tiếp bị 401 và hiện trong card 「転送エラー」") + `feature-spec.md` §3.8.5 (401 → 「認証エラー」, không retry) · Đánh giá spec: Spec không ghi (hành vi 401 thuộc #43730 — cần Dev xác nhận) · ⚠ `callback_event` tăng > 1 dòng trong 2 phút (vòng lặp) → làm ngay bước 9, ghi Không đạt · prd: không ghi DB được → chỉ chạy nếu bot test nội bộ đã có cấu hình cũ (câu SELECT của Dev); Leader quyết · Evidence: ảnh card 「転送エラー」 2 tab + kết quả query `callback_event` trước/sau |
| TC-FUNC003-01 | UI | FUNC-003 | Webhook relay Webhook転送: Tab LINE 「LINE公式アカウントデータ転送」 chặn URL lách bằng ./.., %2e, \, %5C | Abnormal | auto | dev, local, prd, staging | web | Tab LINE: URL lách bằng ./.., %2e, dấu \ hoặc %5C trỏ về webhook LME bị chặn khi công tắc BẬT và TẮT (bàn giao #2, bug #44843) | - Code web ở HEAD 676e01b687 (nhánh ai_studio_fixbug_44660).<br>- Đăng nhập admin chủ bot qua 「/login-v2」, chọn bot test.<br>- Ghi lại cấu hình hiện tại của 2 tab 「Webhook転送」 để khôi phục.<br>- Tab LINE đã lưu sẵn https://8.8.8.8/line-before, công tắc TẮT (lưu qua màn).<br>- Tab LME đã lưu sẵn https://8.8.8.8/notify-keep, công tắc TẮT (lưu qua màn). | 1. Mở 「接続設定」→「Webhook転送」; tab 「LINE公式アカウントデータ転送」 mở mặc định.<br>2. Lấy dòng "bị chặn" đầu tiên trong Dữ liệu nhập: đặt Trạng thái chuyển tiếp 「転送の状態」 như dòng ghi, nhập URL vào ô URL đích 「転送先URL」, bấm Lưu 「保存する」.<br>3. Quan sát vùng lỗi dưới ô URL và toast.<br>4. Nhấn F5, kiểm ô 「転送先URL」 và công tắc của tab LINE.<br>5. Lặp bước 2–4 cho từng dòng "bị chặn" còn lại.<br>6. Với từng dòng "lưu được" (công tắc TẮT): nhập URL, bấm 「保存する」, nhấn F5 và kiểm ô URL.<br>7. Bấm tab 「L Messageデータ転送」, kiểm cấu hình.<br>8. Khôi phục cấu hình 2 tab về giá trị ở tiền điều kiện. | Bị chặn:<br>https://8.8.8.8/line/./callback/add/1 + BẬT<br>https://8.8.8.8/x/../line/callback/add/1 + BẬT<br>https://8.8.8.8/line/%2e/callback/add/1 + TẮT<br>https://8.8.8.8/x/%2e%2e/line/callback/add/1 + BẬT<br>https://8.8.8.8/../line/callback/add/1 + TẮT ('..' ở gốc)<br>https://8.8.8.8/line/callback/add/. + TẮT (đoạn chấm cuối path)<br>https://8.8.8.8/line\callback\add/1 + TẮT (dấu \)<br>https://8.8.8.8/line\callback\add/1 + BẬT<br>https://8.8.8.8/line%5Ccallback%5Cadd/1 + TẮT (%5C)<br>https://8.8.8.8/x\..\line/callback/add/1 + BẬT (\ kèm ..)<br>Lưu được (TẮT):<br>https://8.8.8.8/line/callback/add/../x (rút gọn còn /line/callback/x)<br>https://8.8.8.8/a\b (đổi \ thành / còn /a/b) | - Mỗi dòng bị chặn: dưới ô 「転送先URL」 hiện 「このURLは転送先に指定できません。」; không có toast Đã lưu 「保存しました」<br>- Sau F5 mỗi dòng bị chặn: tab LINE vẫn là https://8.8.8.8/line-before, công tắc TẮT (kể cả dòng BẬT — trạng thái BẬT không được lưu)<br>- Mỗi dòng lưu được: toast 「保存しました」, không có lỗi; sau F5 ô URL hiển thị đúng URL vừa lưu, công tắc TẮT<br>- Bước 7: tab LME vẫn là https://8.8.8.8/notify-keep, công tắc TẮT | | Lấp G2 · Lấp Q4 · căn cứ: journal Dev #150058 ("Tab LINE và tab LME, công tắc bật và tắt") + Studio dev_impact bàn giao #2 · bộ dữ liệu bám NEW-18 (tab LME) để 2 tab cùng chuẩn · dòng BẬT bị chặn thì job không gửi; nếu lưu được phải khôi phục ngay · Đánh giá spec: Spec không ghi (luật mới chưa có trong api-spec — §8 #1) · Evidence: ảnh lỗi dưới ô URL + ảnh sau F5 từng dòng |
| TC-FUNC001-01 | Job | FUNC-001 | Webhook relay Webhook転送: Job chuyển tiếp 1 event tới 転送先URL hợp lệ chạy bình thường — cả kênh LINE và kênh LME | Normal | auto | dev, local, prd, staging | job, line-friend, web | Webhook送信 bình thường: với URL đích hợp lệ, job forward thành công ở cả kênh LINE (webhook LINE) và kênh LME — endpoint ngoài nhận đúng request, không có lỗi ở card 「転送エラー」 | - Code web ở HEAD 676e01b687 (nhánh ai_studio_fixbug_44660); bot test riêng của TC (ghi bot_id khi chạy).<br>- Cờ job đã bật: `ENABLE_FORWARD_WEBHOOK_CALLBACK=1` và `ENABLE_FORWARD_WEBHOOK_LME=1` (hỏi Dev / infra).<br>- Endpoint ngoài do tester kiểm soát (HTTPS hợp lệ, host public, cổng 443) có log/giữ lại request nhận được — vd dịch vụ capture webhook; gọi là URL_OK.<br>- Bạn bè test `システム表示名 RLY_F01` (gọi tắt F01) đã kết bạn với bot.<br>- Bot có tag 「RLY_OK_TAG」, F01 chưa gắn tag này. | 1. Mở 「接続設定」→「Webhook転送」 tab 「LINE公式アカウントデータ転送」: nhập URL_OK vào ô 「転送先URL」, bật 「転送の状態」, bấm 「保存する」.<br>2. Bấm tab 「L Messageデータ転送」: nhập URL_OK, bật 「転送の状態」, bấm 「保存する」.<br>3. Chờ ≥ 60 giây (job đọc cấu hình qua cache 60 giây).<br>4. F01 gửi tin nhắn 「relay-ok-check」 tới bot trên LINE (kích hoạt kênh LINE).<br>5. Chờ ~1 phút, mở log của endpoint ngoài URL_OK.<br>6. Trên màn Friend list 友だちリスト, gắn tag 「RLY_OK_TAG」 cho F01 (kích hoạt kênh LME).<br>7. Chờ ~1 phút, mở log endpoint ngoài URL_OK lần nữa.<br>8. Mở card 「転送エラー」 cả 2 tab, bấm 「最新に更新」.<br>9. Recover data: tắt 2 công tắc, xoá URL_OK khỏi 2 tab, bấm 「保存する」. | URL_OK = endpoint HTTPS do tester kiểm soát (ghi URL cụ thể khi chạy)<br>Tin F01: 「relay-ok-check」<br>Tag: 「RLY_OK_TAG」 | - Bước 1–2: mỗi tab hiện toast 「保存しました」, không có lỗi dưới ô URL<br>- Bước 5 (kênh LINE): endpoint URL_OK nhận đúng 1 POST — body = nguyên văn body webhook LINE của tin F01; header có `Content-Type`, `X-Lme-Timestamp` (epoch ms), `X-Lme-Delivery-Id` (BR-44)<br>- Bước 7 (kênh LME): endpoint URL_OK nhận 1 POST body `{"events":[{...,"type":"tag","action":...,"tag_id":...}]}`; header `X-Lme-Signature` = secret thô `whsec_…` (BR-45/BR-46)<br>- Bước 8: card 「転送エラー」 cả 2 tab KHÔNG có dòng lỗi mới (gửi thành công không ghi lỗi — BR-31) | | Lấp R1 · regression happy-path — webhook send bình thường với URL hợp lệ, cả 2 kênh · căn cứ: RULE-06 (NEW-1/NEW-9 chỉ kiểm URL lưu được, chưa kiểm job forward tới output cuối) + `feature-spec.md` §2.8 / BR-44/45/46; đồng thời là đối chứng cho G1 · ENV-003 / RULE-08: job nền → scope chứa prd · Đánh giá spec: Spec ghi rõ (BR-44/45/46) · env không có endpoint capture → ghi blocked, báo Leader · Evidence: log request tại endpoint ngoài (body + header) + ảnh card 「転送エラー」 2 tab |
| TC-FUNC003-02 | API | FUNC-003 | Webhook relay Webhook転送: API lưu cấu hình POST /admin/webhook-relay/save — ranh giới khớp đường dẫn webhook LME | Boundary | auto | dev, local, prd, staging | api | API lưu cấu hình Webhook転送: ranh giới khớp path /line/callback/add sau chuẩn hoá (rút gọn .., %xx, đoạn path liền kề) ở cả 2 kênh — chặn đúng, không chặn nhầm | - Đăng nhập admin chủ bot qua 「/login-v2」, chọn bot test trên màn; lấy session cookie + CSRF token (`<meta name="csrf-token">`).<br>- Gọi GET `/admin/webhook-relay/config`, ghi lại cấu hình 2 kênh để khôi phục.<br>- Đã lưu sẵn kênh 1 = https://8.8.8.8/api-before-1, kênh 2 = https://8.8.8.8/api-before-2, `is_enabled` = 0. | 1. Gửi POST `/admin/webhook-relay/save` (cookie phiên + CSRF) với bộ tham số dòng 1 của Dữ liệu nhập.<br>2. Kiểm HTTP status và body JSON.<br>3. Gọi GET `/admin/webhook-relay/config`, kiểm kênh vừa gửi và kênh còn lại.<br>4. Với dòng trả 200: gửi lại POST với URL nền của kênh đó (https://8.8.8.8/api-before-1 hoặc https://8.8.8.8/api-before-2) trước khi sang dòng sau.<br>5. Lặp bước 1–4 cho từng dòng còn lại.<br>6. Khôi phục cấu hình 2 kênh như ban đầu. | Mọi dòng `is_enabled` = 0.<br>Bị chặn:<br>channel=1, endpoint_url=https://8.8.8.8/line/callback/add/1/.. → 400 hoặc 422 (rút gọn còn /line/callback/add/)<br>channel=2, endpoint_url=https://8.8.8.8/x/%2E%2E/line/callback/add/1 → 400 hoặc 422 (%2E viết hoa)<br>channel=1, endpoint_url=https://8.8.8.8/line/callback/add%2F1 → 400 hoặc 422 (%2F ngay sau add)<br>channel=2, endpoint_url=https://8.8.8.8/line/callback/%61dd/1 → 400 hoặc 422 (%61 = a)<br>Lưu được:<br>channel=1, endpoint_url=https://8.8.8.8/line/callback/add/.. → 200 (rút gọn còn /line/callback/)<br>channel=2, endpoint_url=https://8.8.8.8/xline/callback/add/1 → 200 (có ký tự liền trước line)<br>channel=1, endpoint_url=https://8.8.8.8/line/callback/add.json → 200 (đoạn add.json khác add)<br>channel=2, endpoint_url=https://8.8.8.8/line/callback/ad/1 → 200<br>channel=1, endpoint_url=https://8.8.8.8/%E9%80%9A%E7%9F%A5/hook?ref=line-callback-add → 200 (path tiếng Nhật đã percent-encoding) | - Dòng bị chặn: HTTP 400 hoặc 422, body `success` = false, `errors[0].field` = `endpoint_url`, `errors[0].error_code` = `URL_NOT_ALLOWED`, `errors[0].message` = 「このURLは転送先に指定できません。」<br>- Dòng bị chặn: GET config sau request — kênh 1 vẫn https://8.8.8.8/api-before-1, kênh 2 vẫn https://8.8.8.8/api-before-2, `is_enabled` = false<br>- Dòng lưu được: HTTP 200, `success` = true; GET config — kênh vừa gửi có `endpoint_url` đúng giá trị gửi lên, kênh còn lại không đổi<br>- Không request nào trả 500 | | Lấp Q2 · căn cứ: Studio dev_impact "chuẩn hoá path — decode %xx, \ và %5C → /, gộp //, bỏ '.', '..' lùi một đoạn" + "URL ngoài khác path (/webhook, /line/callback, /line/callback/addx) phải vẫn lưu được" · catalog DI-05 (URL tiếng Nhật percent-encoding phải lưu được) · dòng `/line/callback/add/..` và `%61dd` suy từ mô tả chuẩn hoá của Dev — kết quả lệch thì hỏi Dev trước khi raise bug · Đánh giá spec: Spec không ghi (luật mới chưa vào api-spec — §8 #1) · Evidence: request + response JSON từng dòng + response GET config |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `web/api-spec.md` "Luật của 「転送先URL」" + `feature-spec.md` §1.5 + §5 + `logic-spec.md` §12 | **✅ ĐÃ CẬP NHẬT 2026-11-03 (Leader chốt C2)**: thêm **luật 8** (api-spec, đẩy DNS→9, public-IP→10) + **BR-11b** (feature-spec §5 + logic-spec §12) — path sau chuẩn hoá (decode `%xx`, `\`/`%5C`→`/`, gộp `//`, rút gọn `./..`) chứa đoạn `/line/callback/add` → `URL_NOT_ALLOWED` 422; mọi domain, mọi bot_id, không phân biệt hoa/thường, áp cả khi TẮT; chạy trước DNS/SSRF. Đã sửa các chỗ ghi "9 luật" → "10 luật". ⚠ Sub-repo `spec-features/` có `.git` riêng — **commit trong sub-repo, không commit từ repo cha** | §4 C2 · journal #149214 | Dev (xác nhận số dòng code) |
| 2 | `feature-spec.md` §1.1 #4 (L31) · NEW-14 | Chốt cột nào "không đổi" khi lưu bị chặn: `endpoint_url` / `is_enabled` / `notify_endpoint_url` / `notify_is_enabled` / `signing_secret`. Mốc `*_errors_refreshed_at` + `updated_at` đổi mỗi lần mở màn | §4 C1 | Leader |
| 3 | Studio `REQ-008` · `feature-spec.md` §5 | Chốt phạm vi chặn: path chứa `/line/callback/add` ở **mọi vị trí** và **mọi domain** (NEW-5: `/api/line/callback/add/1`, `/tenant/abc/line/callback/add` bị chặn) → tool ngoài có path trùng sẽ không cấu hình được | Studio REQ-008 "chờ PO" · NEW-5 | PO |
| 4 | `feature-spec.md` §7 (job) · §1.1 #3 (L30) | Quy tắc "không chuyển tiếp về webhook LME" chưa áp ở job: (a) cấu hình cũ trỏ webhook LME vẫn được job gửi; (b) URL ngoài trả 30x về webhook LME lách được luật lưu vì OkHttp đi theo redirect (L30). Chốt: ticket job riêng (Dev đã đề xuất cho (a)) có gồm (b) không · release có kèm #43730 không | §1 G1 · journal #149730 | Dev / PO |
