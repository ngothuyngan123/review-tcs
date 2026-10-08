# 05 — Review Report

> Draft cho Leader verify. Bug ID + ngày nằm ở tên folder; vòng review = round 1.
> Report chỉ ghi phần THIẾU + việc phải làm. Bảng coverage 2 chiều + bảng quan điểm là nháp nội bộ, không ghi ở đây.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #356 (ticket 41887, round 1, branch `ai_fixbug_41887`) |
| Tổng số TC review | 29 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 9/9 mục có TC (`BUG` · F1–F4 · D1 · T1–T3), 3 mục RISK — **CHƯA ĐỦ** |
| **(b) diff code** — Studio `dev_impact` + `spec_delta` (4 file, +1/−84 dòng) | 11/11 điểm có TC, 3 điểm RISK — **CHƯA ĐỦ** |

**Kết luận**: 14/20 vùng ảnh hưởng đủ TC về mặt thiết kế · 0 GAP · 6 RISK. ⚠️ Trên thực tế **cả 20 vùng đều chưa có kết luận** vì 0/29 TC đã chạy (xem §5 I1) — 14 vùng "đủ" ở đây chỉ là đủ TC thiết kế.

**Đối chiếu 5 nhóm case Leader yêu cầu cover** (bổ sung vòng 1):

| # | Nhóm case Leader yêu cầu | TC hiện có | Kết quả | Dòng thiếu |
|---|---|---|---|---|
| L1 | Gửi tin cho bạn bè / nhóm trên Chat 1:1 **web** | Bạn bè: `#21736`, `NEW-1`, `NEW-3`, `NEW-8` · Nhóm: `#21737`, `NEW-2`, `NEW-4` | **Đủ** | — |
| L2 | Gửi tin cho bạn bè / nhóm trên Chat 1:1 **mobile** — hiểu theo 2 nghĩa: app Elme và màn chat bản điện thoại trên web (`/chat-mobile/<mã hội thoại>`) | App Elme bạn bè: `NEW-24`, `NEW-23` · Màn chat bản điện thoại: chỉ `NEW-19` (gửi ảnh **khi đang bị khoá**) | **Thiếu** — app Elme chưa có nhóm; màn chat bản điện thoại chưa có ca gửi bình thường | G4, G5 |
| L3 | 重複送信防止 giữa 2 staff vẫn hoạt động | `NEW-16` (text), `NEW-17` (ảnh), `NEW-18` (mẫu tin), `NEW-19` (màn điện thoại) + kho `TC-CST-228` (biên), `TC-CST-243` (app) | **Gần đủ** — chưa có ca khoá trong **hội thoại nhóm LINE** (chính đối tượng của bug) | Q1 |
| L4 | Gửi bị lỗi (vượt hạn mức bot free, vượt hạn mức gói LINE, lỗi token…) → hiện lỗi trên GUI **và** có trong màn 「送信エラー」 | Hạn mức free: `NEW-12` (chỉ kiểm modal), `NEW-22` (API) · Hạn mức gói LINE: **không có** · Token: **không có** · Màn 「送信エラー」: **không TC nào kiểm** | **Thiếu** — Leader chốt chỉ cần **1 case lỗi** → chọn lỗi token (chạy staging, auto, kiểm cả GUI lẫn màn 「送信エラー」) | G2, Q7 |
| L5 | Gửi text, mẫu tin, media bình thường | Bạn bè: text nhiều TC, mẫu tin `NEW-15`, ảnh `NEW-14`, tệp `NEW-27`, sticker `NEW-13` · Nhóm: chỉ text | **Thiếu** — mẫu tin / media vào nhóm LINE | G6 |

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `BUG` — triệu chứng **"cùng một tin bị gửi liên tiếp 3–4 lần"** + biểu tượng 🚫 | `dev-impact` | `NEW-4`, `NEW-8` | RISK — symptom-only (AP-2). Root cause Dev nêu (truy vấn lịch sử chậm) giải thích **độ trễ ~10s** nhưng không giải thích **tin trùng 3–4 lần**: lúc khách gặp lỗi, lớp chặn trùng nội dung 60s của #41605 **đang bật**, vậy mà vẫn trùng ⇒ tin trùng đi qua đường **không** bị lớp đó chặn (vd client tự gửi lại khi request quá lâu, hoặc lỗi timeout → nhân viên gửi lại). `NEW-4`/`NEW-8` chỉ kiểm gửi tuần tự trong 1 tab, không kiểm request bị treo lâu. Giải thích 🚫 trong `NEW-8` (con trỏ cấm khi nút đang khoá) **chưa đối chiếu `screenshot1.png`**. Cần Dev xác nhận nguồn gốc tin trùng. | `[BLOCKER]` |
| G2 | `ajax-error.js` + `ChatService@chatMessage` — các nhánh **gửi bị lỗi**: 5xx, lỗi trả về từ LINE (vượt hạn mức gói LINE OA, token / channel hỏng), và việc **ghi lỗi vào màn 「送信エラー」** | `diff code` | `NEW-12`, `NEW-16`, `#21747`, `NEW-10`, `NEW-22` | RISK — `dev_impact` nêu cần hồi quy các nhánh lỗi nằm sát nhánh `duplicate_content` vừa xoá. Đã có TC cho limit_max / prevent_duplicate / send_uncertain / mất mạng, nhưng **chưa có**: (1) lỗi 5xx; (2) lỗi thật từ LINE; (3) **không TC nào kiểm màn 「送信エラー」** (Leader yêu cầu L4). Leader chốt chỉ cần **1 case lỗi** cho (2) + (3) → dùng lỗi token sai; nhánh (1) 5xx **bỏ, không viết TC theo quyết định Leader**; hạn mức gói LINE OA (`001`/`002`/`003`) và hạn mức 1.000 tin bot free (`004`) **không** viết TC. ⚠ Theo `spec-features/admin/error-message/feature-spec.md` §8.6, 9 nơi ghi lỗi nguồn 「1:1チャット」 (`TYPE_CHAT11`) nằm ở `Api/ChatController`, `Admin/BotController`, `Basic/FormAnswerController` — **không có `ChatService` / web chat-v3** ⇒ chưa chắc lỗi gửi từ web chat-v3 có lên màn 「送信エラー」 ở nguồn 「1:1チャット」 (xem §8 dòng 6). | `[MAJOR]` |
| G3 | Hiệu năng ~10s — `dev_impact`: "chỉ tái hiện được ở production"; Dev: "chưa đo trên production rằng đây là nguồn chậm duy nhất" | `diff code` | `NEW-4` (env all), `NEW-7` (local) | RISK — RULE-08 / ENV-003: không TC nào **chốt chạy ở production**. `NEW-4` chạy staging sẽ ra "không tái hiện được do dữ liệu khác production" và vẫn được tính là xong ⇒ không ai xác nhận bug của khách đã hết. | `[MAJOR]` |
| G4 | `T2` — app Elme gửi tin text vào **nhóm LINE** | `dev-impact` | `NEW-24`, `NEW-23` (chỉ bạn bè 1-1) | RISK — app Elme dùng chung `chatMessage` với web, nhưng 2 TC app chỉ gửi cho bạn bè; bug xảy ra ở nhóm LINE (Leader yêu cầu L2). | `[MAJOR]` |
| G5 | `common.js` (F4) — màn chat bản điện thoại trên web `/chat-mobile/<mã hội thoại>` gửi **bình thường** | `diff code` | `NEW-19` (chỉ ca bị khoá 重複送信防止) | RISK — `common.js` bị sửa và được màn này gọi (`public/js/mobile/chat.js`), nhưng chưa TC nào gửi text / ảnh thành công từ màn này cho bạn bè và nhóm (Leader yêu cầu L2). | `[MAJOR]` |
| G6 | `T3` — gửi **mẫu tin / media vào nhóm LINE** | `dev-impact` | `NEW-15`, `NEW-14`, `NEW-27` (chỉ bạn bè 1-1) | RISK — mẫu tin và media dùng chung handler lỗi `ajax-error.js` / `common.js`, nhưng chỉ được kiểm với bạn bè 1-1 (Leader yêu cầu L5). | `[MAJOR]` |

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 21 quan điểm Trigger khớp task · 7 chưa cover đủ.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `CONC-001` | Cao | RISK — có Normal (`NEW-16`) + Abnormal (`NEW-9`, `#21747`, `NEW-26`), **thiếu Boundary** (RULE-01). `重複送信防止` được Dev khẳng định "giữ nguyên" (câu 5 BƯỚC 2) nhưng không TC nào kiểm biên thời gian khoá; bước 6 của `NEW-16` chỉ thử "sau hơn 5 phút". Ngoài ra `NEW-16`..`NEW-19` đều khoá trên **bạn bè 1-1**, chưa có ca khoá trong **hội thoại nhóm LINE** (Leader yêu cầu L3). | `[MAJOR]` |
| Q2 | `REG-SPEC-001` | Cao | GAP — fix **đảo ngược hành vi của #41605** (trước chặn gửi lại cùng nội dung trong 60s, nay cho gửi). Không có bảng rà TC cũ theo 4 trạng thái `[Giữ nguyên] / [Cần sửa] / [Cần thêm mới] / [Hết hiệu lực]`. TC cũ đang kỳ vọng ngược hành vi mới: kho FA-041 `TC-CST-236`, `TC-CST-242` (xem §4 C2). | `[BLOCKER]` |
| Q3 | `PERF-LARGE-001` | Cao (gửi tin) | RISK — nội dung đã có (`NEW-4`, `NEW-7`) nhưng 2 TC mang mã lạ `TOOL-KNOW-002` / `PERF-LATENCY-001` ⇒ theo quy tắc **tính là chưa cover**. | `[BLOCKER]` |
| Q4 | `OUT-PREVIEW-001` | Cao | RISK — chế độ 「プレビューを確認後、送信」 chỉ được cover bởi `NEW-3` mang mã lạ `TOOL-AXIS-001`. | `[BLOCKER]` |
| Q5 | `ENV-003` | Cao | RISK — 0 TC mang mã này; hạng mục hiệu năng chỉ kết luận được ở production (trùng G3). | `[MAJOR]` |
| Q6 | `DATA-COUNT-001` | Cao | RISK — số tin đã gửi của bot và số tin gửi trong ngày đã kiểm ở `NEW-1`, `NEW-12`; **bộ đếm "chưa xác nhận" khi admin trả lời** (BR-08, chạy ngay trong `ChatService@chatMessage` — hàm bị xoá 62 dòng) không TC nào kiểm. | `[MAJOR]` |
| Q7 | `INTG-LINE-001` | Cao | RISK — Normal có nhiều; Abnormal chỉ có lỗi **giả lập** (`#21747` send_uncertain, `NEW-21` thiếu kênh LINE); **chưa có lỗi thật LINE trả về**. Lấp bằng 1 case Abnormal (token sai). **Boundary** (tin thứ 200 / 201 của gói LINE OA) **bỏ theo quyết định Leader** (chỉ cần 1 case lỗi) — ghi làm lý do thiếu loại case theo RULE-01. | `[MAJOR]` |

- Q3, Q4: **không cần TC mới** — đổi `Mã quan điểm` trên Studio (`testcase_update`): `NEW-7` → `PERF-LARGE-001`, `NEW-4` → `PERF-LARGE-001` (hoặc `FUNC-001`), `NEW-3` → `OUT-PREVIEW-001`. Sửa nhãn xong là đóng.
- Q2: không đẻ TC — việc cần làm là rà TC cũ (danh sách gợi ý ở §8 dòng 2).
- Đã xét và loại (không phải ảnh hưởng của task): `SEC-ISO-001`, `DATA-DB-001`, `FRIEND-001`, `DATA-TEXT-001` — diff chỉ xoá bước tra trùng, không đổi luồng hiển thị nhiều hội thoại / UPDATE-DELETE / biến friend info / xử lý nội dung text. Gửi tin hẹn giờ (Luồng 4 – Spring Boot `ScheduleSendChatTask`) không đi qua `ChatService@chatMessage` ⇒ hướng "job nền" không bị chạm.

---

## 3. TC trùng lặp nội dung

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `NEW-1` | `#21736` | `DUP-SUBSET` | `FUNC-001` × Normal × gửi text tới bạn bè 1-1 × tiền đề bot + bạn bè chưa chặn → `NEW-1` đã kiểm đủ khung hội thoại + dòng bên trái + DB + mã 200 của lượt gửi 1 | `[MINOR]` |
| DUP-2 | `NEW-5` | `NEW-21` | `DUP-SUBSET` | mã `TOOL-KNOW-002` × Normal × gửi lại cùng nội dung trong 60s với bản ghi dựng sẵn ở local × expected "không bị chặn, có thêm 1 bản ghi" | `[MINOR]` |

- **Gate đã chạy**: xóa `#21736` → không mất cover (FUNC-001 còn `NEW-1`). Bỏ `NEW-21` → REQ-007 (API) còn `NEW-20`, `NEW-22`; đề nghị **gộp**: thêm 1 dòng expected "HTTP 200 (có kênh LINE thật) / 502 hoặc 200 + send_uncertain (không có)" vào `NEW-5` rồi mới xóa `NEW-21`.
- `#21736` là TC smoke tái dùng từ kho (`C1-230`). Nếu Leader muốn giữ bộ smoke cố định (RULE-12) thì giữ lại, bỏ DUP-1.
- Không có `DUP-INFLATE`.

---

## 4. Mâu thuẫn trong TCs

| # | Loại | TC liên quan | Nội dung check trùng nhau | Expected A | Expected B / nguồn đối chiếu | Khả năng sai | Severity | Ai chốt |
|---|---|---|---|---|---|---|---|---|
| C1 | `CONF-KHO` | `#21736`, `NEW-1`, `NEW-2`, `NEW-13`, `NEW-14` | Admin gửi tin từ Chat 1:1 → dòng bạn bè / nhóm ở danh sách bên trái | "Dòng bạn bè bên trái cập nhật nội dung tin cuối / hiển thị X với giờ gửi mới nhất" (cũng là mục retest 1 của Dev) | kho `TC-CHT-162` "Gửi text từ LME — KHÔNG cập nhật tin nhắn cuối của bạn bè" (+ `TC-CHT-164`, `TC-CHT-165`), theo SpecImprove #35389 (4/2026); kho FA-001 `MT-01` đang **⏳ chờ quyết định**. `feature-spec.md` §2.1 Luồng 1 bước 3 lại ghi `UPDATE conversation (last_message, last_time_message)` — khớp TC Studio. | TC Studio sai (hành vi đã đổi từ 4/2026) / kho + #35389 không còn đúng | `[MAJOR]` | Leader / PM |
| C2 | `CONF-KHO` | `#21747` | Lỗi khi gửi (mạng chập chờn / không chắc đã gửi) rồi nhân viên **gửi lại** cùng nội dung | "Lượt gửi lại được xử lý như lượt mới; nếu lượt đầu đã đi thì có thể có **2 tin Z**" (rủi ro Dev đã chấp nhận) | kho FA-041 `TC-CST-236` "Mạng chập chờn khi gửi rồi gửi lại — friend chỉ nhận **ĐÚNG 1 tin**, không phải 2 tin do thử lại"; `TC-CST-242` (app mobile) cùng expected | Kho viết theo hành vi #41605 (nay đã gỡ) → cần update / hoặc gỡ #41605 là sai yêu cầu nghiệp vụ, phải giữ chống trùng bằng cách khác | `[MAJOR]` | PM / PO |
| C3 | `CONF-SPEC` | `NEW-22` | Mã HTTP các nhánh lỗi của `POST /basic/send-message-v2` | Hạn mức gói → **402** + `limit_max`; chặn / rỗng / 重複送信防止 → 422; ngoài quyền → 403; không tồn tại → 404 | (1) Bảng mã HTTP RULE-13 (`checklist-lme.md` §1.1): **hạn mức gói = 422**, không có 402. (2) `feature-spec.md` §6 EP-08 vẫn ghi lỗi trả `200 + success:false` (TC ghi chú: mã đã đổi ở #40051). | TC ghi theo code (402) thay vì quy ước / code #40051 lệch quy ước nên phải báo Dev; spec EP-08 cũ hơn #40051 | `[MAJOR]` | Dev / Leader |

**Đã rà**: 29 TC × `spec-features/admin/chat-11/feature-spec.md` (§2.1 Luồng 1–4, §5 BR-07/08/09/15, §6 EP-08..11) + `kho-tcs/fa001-chat11-11チャット.md` (nhóm "Gửi text & phím tắt", "Shorten URL", "Bộ đếm chưa xác nhận") + `kho-tcs/fa041-caidatchat-チャット設定.md` (nhóm "Chống gửi trùng — chặn gửi thực tế") — phát hiện C1..C3. Không có `CONF-TC` giữa các TC Studio với nhau.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[BLOCKER]` | Toàn bộ 29 TC | **0/29 TC đã chạy** (0% pass; Studio `exec.untested = 29`, `envAuto` 0 run ở mọi env). Mọi vùng ở §1 / §2 chưa có kết luận. | Chạy bộ TC trước khi Leader duyệt; TC `local` (`NEW-5`, `NEW-7`, `NEW-11`, `NEW-12`, `NEW-21`, `NEW-22`, `#21747`) chạy ở local, phần còn lại ở staging + G3 ở production. |
| I2 | `[MAJOR]` | `[AP-2]` — `BUG` | Symptom-only: khách báo 3 triệu chứng, Dev sửa 1 root cause (xem G1). | Hỏi Dev nguồn gốc tin trùng 3–4 lần trước khi chốt fix; chạy TC G1. |
| I3 | `[MAJOR]` | `[AP-6]` — `03-dev-impact.md` mục 3 | Dev không liệt kê nơi gọi `ChatService@chatMessage`; mục 4.3 ghi sticker "không ảnh hưởng" trong khi Studio xác định sticker đi qua chính hàm bị sửa (`dev_impact` dòng 1). Studio đã bù bằng `NEW-13`. | Dev xác nhận danh sách đầy đủ nơi gọi `chatMessage` (web text · web sticker · app text · nơi khác nếu có). |
| I4 | `[MAJOR]` | `NEW-23` | RULE-13: TC gọi thẳng `POST /api/mobile/chat/send-message-text` nhưng expected chỉ ghi `success = true`, **không ghi mã HTTP**. | Thêm "HTTP 200" vào expected. |
| I5 | `[MAJOR]` | `NEW-26`, `#21747` | Expected không đo lường được: "cả hai request **có thể** được xử lý thành hai lượt", "**có thể** có 2 tin Z" — TC nào cũng Đạt. | Chốt 1 kết quả (2 tin hay 1 tin) sau khi PO trả lời §8 dòng 5. |
| I6 | `[MAJOR]` | `NEW-4`, `NEW-7` | Expected đo hiệu năng không có ngưỡng: "nhanh hơn rõ rệt", "chênh không đáng kể". | Ghi ngưỡng cụ thể (vd hội thoại lớn ≤ hội thoại đối chứng + 1 giây) — Dev/Leader chốt. |
| I7 | `[MAJOR]` | `#21747`, `NEW-23`, `NEW-19` | Người khác không dựng lại được env: `#21747` không nêu **cách** giả lập trạng thái "gửi không chắc chắn"; `NEW-23` "xác nhận với Dev cách lấy token app"; `NEW-19` "xác nhận đường dẫn đầy đủ trên môi trường". | Ghi cụ thể công cụ / cờ giả lập, cách lấy token, URL đầy đủ. |
| I8 | `[MAJOR]` | `NEW-16` | Không atomic: gộp kiểm màn 「チャット設定」 load + lưu (SRC-REGRESSION-018) với 4 phán quyết khoá 重複送信防止. Fail ở bước 1 sẽ che kết quả các bước sau. | Tách bước 1 thành TC riêng cho màn 「チャット設定」. |
| I9 | `[MAJOR]` | Toàn bộ 29 TC | Cột `Trạng thái đánh giá spec` trống ở cả 29 TC (`spec_status = null`), trong khi nhiều TC ghi chú "spec chưa có / chờ PO xác nhận". | Điền `Spec ghi rõ` / `Spec không ghi` / `Đã hỏi leader` cho từng TC. |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 29 TC — không có TC nào ngoài phạm vi task. Mọi TC map được vào `BUG` / F1–F4 / T1–T3 hoặc vào rủi ro hồi quy Studio nêu (`dev_impact` dòng 3–6). Các TC regression sticker / ảnh / tệp / mẫu tin (`NEW-13`, `NEW-14`, `NEW-27`, `NEW-15`, `NEW-17`, `NEW-18`) dẫn được từ việc dùng chung `chatMessage` / `ajax-error.js` ⇒ không phải thừa.

---

## 7. TCs đề xuất bổ sung (7)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa001-chat11-11チャット.md`, `kho-tcs/fa041-caidatchat-チャット設定.md` · spec màn lỗi `spec-features/admin/error-message/feature-spec.md` (§1.5 bảng mã lỗi, §2.2 tab 「未確認エラー」, §3.5, §8.6) |
| Vùng regression phát hiện từ kho | FA-001 "Bộ đếm chưa xác nhận" (`TC-CHT-408`), "Shorten URL" (`TC-CHT-183`), "Giới hạn plan & token" (`TC-CHT-418`, `TC-CHT-421`); FA-041 "Chống gửi trùng — chặn gửi thực tế" (`TC-CST-228`, `TC-CST-243`, `TC-CST-245`) |
| Conflict expected vs kho | `TC-CHT-162/164/165` → C1; `TC-CST-236/242` → C2 — đã đưa §4 + §8 |
| GAP dùng lại TC kho (không viết mới) | **Q1** → `TC-CST-228` "Số phút = 1 — chặn đúng 1 phút rồi mở lại" (chạy trên branch fix, đối chiếu biên trước/sau 1 phút) · **Q6** → `TC-CHT-408` (chỉ cần trường hợp "bot trả lời tin thường" bằng tin text từ Chat 1:1) |
| Căn cứ TC regression `R<x>` | **R1** → dùng lại `TC-CHT-183` "BẬT 短縮URLの利用 — chat 1:1 hiện URL GỐC, app LINE nhận URL rút gọn" — căn cứ: rút gọn URL (BR-15) là bước 5 của `ChatService@chatMessage` (`feature-spec.md` §2.1 Luồng 1), cùng hàm bị xoá 62 dòng. **R2** → dùng lại `TC-CST-243` "Web và app cùng gửi 1 hội thoại trong thời gian chặn" — căn cứ: kho `TC-CST-245` xếp "app text" là 1 trong 6 đường gửi có khoá 重複送信防止, và app text đi qua `chatMessage` (`dev_impact` dòng 1); bộ Studio chỉ kiểm khoá trên web. |
| Xác nhận chống trùng | Đã đối chiếu 29 TC ở BƯỚC 0 + 2 file kho — không TC đề xuất nào trùng (`NEW-8` = mạng chậm phía client, không phải server xử lý chậm; `NEW-10` = offline, không phải 5xx; `TC-INTGLINE001-01` khác kho `TC-CHT-421` ở chỗ kiểm thông báo trên web chat-v3 + dòng ở tab 「未確認エラー」 + gửi lại sau khi sửa token). L4 theo quyết định Leader chỉ 1 case lỗi → **không** viết TC hạn mức gói LINE OA / hạn mức 1.000 tin bot free. |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-CONC001-01 | API | CONC-001 | Gửi text & phím tắt | Abnormal | auto | Tất cả | Máy chủ xử lý gửi tin chậm ≥ 15 giây — bấm gửi 1 lần vào nhóm LINE chỉ sinh đúng 1 request, 1 tin, không tự gửi lại | - Đăng nhập admin, chọn bot kiểm thử có kênh LINE thật<br>- Bot tham gia 1 nhóm LINE kiểm thử; 「プレビューを確認後、送信」 tắt; 重複送信防止 tắt<br>- Giữ response của `POST /basic/send-message-v2` lại 15 giây bằng Playwright `route` / proxy (không cần sửa server — chạy được ở mọi env)<br>- Mở DevTools tab Network | 1. Mở Chat 1:1, chọn nhóm kiểm thử<br>2. Nhập X, bấm nút gửi **1 lần**, không thao tác thêm<br>3. Chờ tới khi request kết thúc (hoặc màn báo lỗi)<br>4. Đếm số request `send-message-v2` trên tab Network<br>5. Rê chuột lên nút gửi trong lúc chờ, ghi dạng con trỏ, chụp màn hình so với `screenshot1.png` của ticket<br>6. Tải lại trang, đếm tin X trong nhóm; đếm bản ghi tin X trong dữ liệu; đếm tin X thành viên nhóm nhận trên LINE | X = `t41887-<mã lần chạy>-slow`<br>Độ trễ giả lập: 15 giây | - Tab Network có **đúng 1** request `send-message-v2` (không có request gửi lại tự động)<br>- Trong lúc chờ: nút gửi bị khoá, con trỏ dạng cấm (🚫); hình khớp / không khớp `screenshot1.png` được ghi lại<br>- Kết thúc thành công: đúng 1 tin X trong nhóm, đúng 1 bản ghi, thành viên nhận đúng 1 tin<br>- Nếu màn báo lỗi timeout: thông báo phải kèm câu 「送信できたかどうかは、画面を再読み込みしてトーク履歴をご確認ください。」 và dữ liệu vẫn chỉ có ≤ 1 bản ghi X |  | Lấp G1 · Đánh giá spec: Spec không ghi — cần Dev xác nhận nguồn gốc tin trùng 3–4 lần · Evidence: HAR tab Network + ảnh màn hình + số bản ghi DB · staging (không chọn product vì phải giả lập độ trễ; kết luận hiệu năng thật nằm ở TC-ENV003-01) |
| TC-ENV003-01 | API | ENV-003 | Gửi text & phím tắt | Normal | manual | product | Sau phát hành trên production — thời gian xử lý gửi tin vào nhóm LINE của khách không còn ~10 giây, không còn tin trùng | - Bản fix #41887 đã phát hành production<br>- Dev có quyền đọc log thời gian xử lý `POST /basic/send-message-v2` (APM / access log) của bot `転職エージェントナビ by circus`<br>- KHÔNG gửi tin thử vào nhóm của khách | 1. Lấy thời gian xử lý các request gửi tin text vào hội thoại nhóm 「転職エージェントナビ面談チーム」 trong 3 ngày **trước** phát hành<br>2. Lấy cùng số liệu trong 3 ngày **sau** phát hành<br>3. Lấy số liệu cùng kỳ của 1 hội thoại bạn bè 1-1 ít tin của cùng bot làm đối chứng<br>4. Đếm số cặp tin text cùng nội dung, cùng người gửi, cách nhau < 10 giây trong nhóm trước / sau phát hành<br>5. Nhờ CS hỏi lại khách còn gặp trễ / trùng / 🚫 không | Bot: `転職エージェントナビ by circus`<br>Nhóm: 「転職エージェントナビ面談チーム」<br>Khoảng đo: 3 ngày trước / sau | - Sau phát hành: thời gian xử lý của nhóm ≤ ngưỡng Dev/Leader chốt (đề xuất: không vượt hội thoại đối chứng quá 1 giây); trước phát hành ghi lại mức ~10 giây để so<br>- Không còn cặp tin trùng do 1 lần bấm (bước 4)<br>- Khách xác nhận hết lỗi qua CS |  | Lấp G3 + Q5 · RULE-08 (performance chỉ kết luận ở production) · manual vì môi trường production · Đánh giá spec: Spec không ghi · Evidence: bảng số đo trước/sau + truy vấn đếm tin trùng + phản hồi CS |
| TC-INTGLINE001-01 | API | INTG-LINE-001 | Giới hạn plan & token | Abnormal | auto | dev / local / staging | Token kết nối LINE của bot bị hỏng — gửi text báo lỗi trên màn chat và ghi vào màn 「送信エラー」; sửa token xong gửi lại được | - Môi trường dev / local / staging — **KHÔNG chạy trên production**<br>- Bot kiểm thử riêng có 1 bạn bè 1-1 chưa chặn bot<br>- Dev đổi channel access token **và** channel secret của bot thành giá trị sai (để việc tự làm mới token cũng thất bại — như kho `TC-CHT-421`)<br>- 「プレビューを確認後、送信」 tắt | 1. Mở Chat 1:1 (`/basic/chat-v3`), chọn bạn bè, gửi X<br>2. Ghi nguyên văn thông báo, trạng thái ô soạn, khung hội thoại<br>3. Mở 「システム関連」→「送信エラー」, tab 「未確認エラー」; bấm 「詳細」 ở dòng mới<br>4. Dev khôi phục token đúng; quay lại Chat 1:1 gửi lại X | X = `t41887-<mã lần chạy>-tok` | - Bước 1: màn chat hiện thông báo lỗi gửi (ghi nguyên văn), **không** phải 「同じ内容のメッセージが直前に送信済みです。トーク履歴をご確認ください。」, không treo lớp phủ; bạn bè **không** nhận tin<br>- Bước 3: tab 「未確認エラー」 có 1 dòng mới — 「友だち名」 = bạn bè kiểm thử, 「メッセージ」 = X, 「エラーコード」 = `005`; modal 「詳細」 hiện 「LINE公式アカウント凍結、もしくは誤操作により現在設定されているchannel secretが利用できなくなりました。…」<br>- Bước 4: gửi thành công, không bị chặn vì "trùng nội dung" với lượt lỗi trước; bạn bè nhận 1 tin X |  | Lấp G2 + Q7 · Leader yêu cầu L4 — **case lỗi duy nhất** (Leader chốt 1 case) · dẫn từ kho `TC-CHT-421` · Đánh giá spec: mã `005` cho lỗi token theo `error-message/feature-spec.md` §8.6 là ánh xạ phía **job**; chat 1:1 ghi lỗi ở Laravel — Dev xác nhận mã hiển thị (`005` hay 「エルメサポートまで」) và nguồn (§8 dòng 6) · Evidence: ảnh màn chat + tab 「未確認エラー」 + modal |
| TC-CONC001-02 | API | CONC-001 | Group chat | Abnormal | auto | Tất cả | 重複送信防止 trong hội thoại nhóm LINE — nhân viên B bị chặn khi A vừa gửi vào nhóm; A gửi lại cùng nội dung vẫn được | - 2 tài khoản nhân viên A, B cùng quyền vào bot kiểm thử (ghi username của A)<br>- Bot có kênh LINE thật, đang tham gia 1 nhóm LINE kiểm thử G<br>- 「チャット設定」 → 「重複送信防止機能」 = 「利用する」, 5 phút<br>- A và B đăng nhập ở 2 trình duyệt riêng | 1. A mở Chat 1:1, chọn nhóm G, gửi X<br>2. Trong vòng 5 phút, B mở nhóm G, gửi Y; ghi modal; bấm 「閉じる」<br>3. A gửi lại đúng X<br>4. Tải lại, đếm tin trong nhóm G; đối chiếu dữ liệu và app LINE của 1 thành viên nhóm | X = `t41887-<mã lần chạy>-grpA`<br>Y = `t41887-<mã lần chạy>-grpB`<br>重複送信防止: 5 phút | - Bước 2: B thấy modal 「現在、メッセージの送信ができません。」 với nội dung 「<username A> さんが直前にメッセージを送信したため、この友たちには5分間メッセージの送信ができません。」; ô soạn của B giữ Y; không có tin Y nào được tạo / gửi<br>- Bước 3: A gửi thành công, không có thông báo 「同じ内容のメッセージが直前に送信済みです。トーク履歴をご確認ください。」<br>- Tổng cuối nhóm G: đúng 2 tin X của A, 0 tin Y |  | Lấp Q1 · Leader yêu cầu L3 · câu modal trích từ `NEW-16` (chữ 「友たち」 là lỗi chính tả có sẵn) · Đánh giá spec: Spec không ghi (spec chat-11 chưa có 重複送信防止 — §8 dòng 4) · Evidence: ảnh modal + đếm tin nhóm + DB |
| TC-SYNCAPP001-01 | API | SYNC-APP-001 | Group chat | Normal | manual | Tất cả | App Elme gửi cùng nội dung text 2 lần liên tiếp vào nhóm LINE — cả 2 tin đi, khớp web và LINE | - Thiết bị thật cài app Elme, đăng nhập nhân viên của bot kiểm thử<br>- Bot có kênh LINE thật, đang tham gia 1 nhóm LINE kiểm thử<br>- Chỉ 1 nhân viên thao tác | 1. Trên app Elme mở Chat 1:1, chọn nhóm kiểm thử<br>2. Gửi X; chờ tin hiện<br>3. Trong vòng 60 giây gửi lại đúng X<br>4. Quan sát thông báo trên app<br>5. Mở Chat 1:1 trên web cùng nhóm, đếm tin X; đối chiếu app LINE của 1 thành viên nhóm | X = `t41887-<mã lần chạy>-appgrp` | - Cả 2 lần gửi thành công trên app, không có thông báo lỗi / trùng nội dung<br>- App và web đều hiện đúng 2 tin X trong nhóm<br>- Thành viên nhóm nhận đúng 2 tin |  | Lấp G4 · Leader yêu cầu L2 · manual vì thiết bị thật (app Elme) · Đánh giá spec: Spec không ghi · Evidence: quay màn hình app + ảnh web + ảnh app LINE |
| TC-REGSHARED001-01 | UI | REG-SHARED-001 | Gửi text & phím tắt | Normal | auto | Tất cả | Màn chat bản điện thoại trên web (`/chat-mobile/<mã hội thoại>`) — gửi text và ảnh bình thường cho bạn bè và nhóm LINE | - Đăng nhập admin, chọn bot kiểm thử có kênh LINE thật<br>- Có 1 bạn bè 1-1 chưa chặn bot và 1 nhóm LINE kiểm thử<br>- 重複送信防止 tắt<br>- DevTools bật chế độ giả lập điện thoại<br>- Dev cung cấp URL đầy đủ của màn chat bản điện thoại (route `/chat-mobile/{conversation_id}`) | 1. Mở màn chat bản điện thoại của bạn bè kiểm thử<br>2. Gửi text X; chờ tin hiện<br>3. Gửi ảnh P<br>4. Lặp bước 2–3 với nhóm LINE kiểm thử<br>5. Tải lại từng hội thoại; mở cùng hội thoại trên `/basic/chat-v3` để đối chiếu; kiểm app LINE phía nhận | X = `t41887-<mã lần chạy>-mob`<br>Ảnh P = `t41887.jpg` (JPG ~200KB)<br>4 tổ hợp: (bạn bè, nhóm) × (text, ảnh) | - Cả 4 lượt gửi thành công, không có alert, lớp phủ đang tải tắt<br>- Mỗi hội thoại hiện đúng 1 tin X + 1 ảnh P, khớp với `/basic/chat-v3` sau khi tải lại<br>- Dữ liệu có đúng 2 bản ghi mỗi hội thoại; bạn bè / thành viên nhóm nhận đủ |  | Lấp G5 · Leader yêu cầu L2 · `common.js` (sendMedia) bị sửa và được `public/js/mobile/chat.js` gọi (ghi chú `NEW-19`) · nếu màn bản điện thoại không hỗ trợ nhóm thì ghi `không áp dụng` cho 2 tổ hợp nhóm kèm xác nhận của Dev · Đánh giá spec: Spec không ghi (spec chat-11 không mô tả màn này) · Evidence: ảnh 4 lượt + đếm DB |
| TC-FUNC001-01 | UI | FUNC-001 | Group chat | Normal | auto | Tất cả | Gửi mẫu tin và ảnh vào nhóm LINE từ Chat 1:1 web — gửi bình thường, nhóm nhận đủ | - Đăng nhập admin, chọn bot kiểm thử có kênh LINE thật<br>- Bot đang tham gia 1 nhóm LINE kiểm thử<br>- Bot có mẫu tin văn bản M<br>- 重複送信防止 tắt; 「プレビューを確認後、送信」 tắt | 1. Mở `/basic/chat-v3`, lọc sang hội thoại nhóm, chọn nhóm kiểm thử<br>2. Mở khối chọn mẫu tin, chọn M, bấm gửi; chờ tin hiện<br>3. Bấm 「メディア送信」, chọn ảnh P, bấm gửi; chờ ảnh hiện<br>4. Tải lại, đếm tin; đối chiếu dữ liệu và app LINE của 1 thành viên nhóm | Mẫu tin M = mẫu văn bản `t41887-<mã lần chạy>-tplgrp`<br>Ảnh P = `t41887.jpg` | - Cả 2 lượt gửi thành công, không có alert hay modal<br>- Nhóm hiện 1 tin nội dung M + 1 ảnh P (vẫn đủ sau tải lại); ghi lại dòng nhóm bên trái có cập nhật tin cuối hay không (quy tắc đang chờ Leader/PM chốt — kho FA-001 `MT-01`)<br>- Dữ liệu có 2 bản ghi tương ứng; thành viên nhóm nhận đủ 2 tin |  | Lấp G6 · Leader yêu cầu L5 · regression vì mẫu tin / media dùng chung `ajax-error.js` / `common.js` (dev_impact dòng 5) · Đánh giá spec: Spec ghi rõ (`chat-11/feature-spec.md` §2.1 Luồng 2, 3) · Evidence: ảnh hội thoại nhóm + DB + ảnh app LINE |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `spec-features/admin/chat-11/feature-spec.md` §2.1 Luồng 1 bước 3 + `db/db-mapping.md:879` (+ kho FA-001 `MT-01`) | Chốt: admin gửi tin từ LME có cập nhật `last_message` / `last_time_message` của bạn bè không. Sau khi chốt, sửa spec **hoặc** sửa expected 5 TC Studio (`#21736`, `NEW-1`, `NEW-2`, `NEW-13`, `NEW-14`). | C1 `CONF-KHO` | Leader / PM |
| 2 | `kho-tcs/fa041-caidatchat-チャット設定.md` nhóm "Chống gửi trùng — chặn gửi thực tế" (+ spec chat-setting nếu bổ sung tab 重複送信防止) | Gỡ lớp chặn của #41605 ⇒ gửi lại sau lỗi có thể tạo tin trùng. Rà theo REG-SPEC-001: `TC-CST-236`, `TC-CST-242` → `[Cần sửa]` (hoặc `[Hết hiệu lực]`) nếu PO chấp nhận rủi ro; `TC-CST-233/234/235/237/238/239/240/241` (double-click → 1 tin, lớp khoá phía màn vẫn còn) → `[Giữ nguyên]`. | C2 `CONF-KHO` + Q2 | PM / PO |
| 3 | `feature-spec.md` §6 EP-08 (response) | Cập nhật mã HTTP các nhánh lỗi theo #40051; Dev xác nhận hạn mức gói trả 402 hay đổi sang 422 theo bảng RULE-13 — không sửa expected cho khớp code. | C3 `CONF-SPEC` | Dev / Leader |
| 4 | `feature-spec.md` §2.1 Luồng 1 + §5 Business Rules | Spec Chat 1:1 chưa có bước khoá 重複送信防止 (`tryAcquireSendLock`) trong luồng gửi text / media / template, cũng không ghi rõ "không chặn gửi trùng nội dung". Bổ sung BR. | ghi chú `NEW-16` | Dev |
| 5 | Yêu cầu nghiệp vụ #41605 vs #41887 | PO xác nhận chính thức việc **đảo mục tiêu #41605**: cùng 1 nhân viên gửi lại cùng nội dung (2 tab, web + app, sau lỗi) đều cho đi. Cần trả lời trước khi chốt expected `NEW-1`, `NEW-9`, `NEW-26`, `#21747` (I5). | ghi chú `NEW-1` / `NEW-9` / `NEW-26` | PO |
| 6 | `spec-features/admin/error-message/feature-spec.md` §8.6 (danh sách 9 nơi truyền `TYPE_CHAT11`) | Spec chỉ liệt kê `Api/ChatController`, `Admin/BotController`, `Basic/FormAnswerController` — **không có `ChatService` / web chat-v3**. Dev xác nhận: lỗi gửi từ `/basic/send-message-v2` có ghi `message_error` không, ghi với `type` nào (hiện ở nguồn 「1:1チャット」 hay 「その他メッセージ」), và mã hiển thị cho lỗi token. Expected của `TC-INTGLINE001-01` phụ thuộc câu trả lời này. | Leader yêu cầu L4 (G2) | Dev |
