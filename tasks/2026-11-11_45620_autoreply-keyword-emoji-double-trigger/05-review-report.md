# 05 — Review Report

> Draft cho Leader verify. Chỉ ghi phần THIẾU + việc phải làm.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | (1) Studio task #569 — round 1, branch `ai_studio_fixbug_45620` |
| Tổng số TC review | 24 |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Trả lời**:

| Chiều | Kết quả |
|---|---|
| **(a) dev-impact** — Dev tự kê ở `03-dev-impact.md` mục 4 | 4/4 mục có TC (`BUG` · `F1` · `T1` · `T2`; không có `D*`) — **ĐỦ** |
| **(b) diff code** — Studio `dev_impact` (`diffAvailable=false`, điểm sửa lấy từ file 03 mục 2: 1 file, 1 dòng) | 10/12 điểm có TC — **CHƯA ĐỦ** |

**Kết luận**: 14/16 vùng ảnh hưởng đủ TC · 1 GAP · 1 RISK

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | Job callback production — nhánh `release-callback-t09-2026` (dev_impact: "callback branch chưa có fix") | `diff code` | `NEW-22` (skip, chỉ keyword emoji) | RISK — production xử lý webhook bằng job callback riêng (catalog D `ENV-JOB` dòng 310); 20 PASS đều ở local "1 job all" nên chưa đi qua job này. TC duy nhất là `NEW-22`: chưa chạy, expected còn hợp thức hoá kết quả sai (I2) | `[BLOCKER]` |
| G2 | Trigger detail 「送信トリガー詳細」 ở 1:1チャット (dev_impact: hệ quả phụ cần kiểm) | `diff code` | không có | GAP — 0 TC. Đây đúng là màn KH dùng để phát hiện lỗi (file 01) | `[MAJOR]` |

- **Loại khỏi mẫu số (b)** — dev_impact ghi "Không đổi" nhưng không đi qua câu so khớp: 「全てのメッセージに反応」 (`KEYWORD_ANY` luôn match), khung giờ, filter (job-spec `checkAutoReply` bước 2) → quy tắc so theo byte không áp. Regression kết hợp đề xuất ở `R1`. "Build job sạch lỗi converter-jackson" là lỗi có sẵn ngoài phạm vi, không phải điểm kiểm chứng.
- Điểm (b) đã đủ: điểm sửa `matchingKeyword` 部分一致 · emoji khác không khớp · hoa/thường-kana-độ rộng · action · `auto_reply_history` 1度のみ · AND/OR · tự 確認済み · 完全一致 · bỏ qua 【】 · chỉ lộ trên MySQL 8 (`NEW-1` + `NEW-10` xác nhận local là MySQL 8 tái hiện được lỗi).

---

## 2. Thiếu so với quan điểm test

**Kết luận**: 12 quan điểm Trigger khớp task · 5 loại có lý do (dưới bảng) · **7 chưa cover đủ** (3 `[BLOCKER]`). Nguyên nhân chung: 13/24 TC (kể cả TC kịch bản khách `NEW-9`) gắn mã ngoài checklist nên không được tính.

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `FUNC-001` | Cao | GAP — 0 TC gắn mã. Nội dung có ở `NEW-9` (Abnormal), `NEW-4` (Boundary) nhưng mang mã khác → đổi mã 2 TC này; Normal (màn + output) thiếu → TC-FUNC001-01 | `[BLOCKER]` |
| Q2 | `JOB-001` | Cao ★ | GAP — 0 TC gắn mã. Oracle "mọi sự kiện xử lý hoàn tất không lỗi" có ở `NEW-21` (mã khác); job callback production chưa TC nào chạy (G1) | `[BLOCKER]` |
| Q3 | `REG-RUN-001` | Cao | GAP — dữ liệu từ trước release: `auto_reply_history` ghi do khớp sai (rule 1度のみ + 部分一致) từ 20/10 → sau deploy friend gửi đúng keyword vẫn không được reply. 0 TC; expected chưa chốt (Dev để CS quyết) | `[BLOCKER]` |
| Q4 | `ENV-003` | Cao ★ | RISK — chỉ Normal: `NEW-1` (local) pass, `NEW-22` (prd) skip; 0 TC chạy staging/prd; thiếu Abnormal/Boundary, không ghi lý do (RULE-01) | `[MAJOR]` |
| Q5 | `REG-SHARED-001` | Cao | RISK — Normal `NEW-13/14/15` pass; Abnormal chỉ `#41605` (skip); không có Boundary (RULE-01); chưa có danh sách nơi ảnh hưởng ngoài auto-reply (I4) | `[MAJOR]` |
| Q6 | `DATA-TEXT-001` | Cao (text gửi LINE) | RISK — Boundary `NEW-19/20` pass; Normal chỉ `NEW-11` (skip); thiếu Abnormal | `[MAJOR]` |
| Q7 | `MSG-USER-001` | Cao | RISK — chỉ `NEW-8` (Abnormal, nhánh friend bị bot chặn); thiếu Normal + Boundary, không ghi lý do (RULE-01) | `[MAJOR]` |

**Đã loại khỏi phạm vi (Trigger khớp nhưng diff không chạm)**:

| Mã | Lý do loại | Căn cứ |
|---|---|---|
| `INTG-LINE-001` | Diff không chạm gọi LINE API / nhận webhook; lỗi gửi & retry không đổi | kho FA-003 nhóm 31 · file 03 mục 2 |
| `DEPLOY-LIVE-001` | Kiểm tra dành cho client cũ gọi server mới; auto-reply không có màn phía client, tin đến lúc deploy nằm ở `callback_event`. Rủi ro deploy lệch job/callback → TC-ENV003-01 | checklist dòng 547–550 |
| `MSG-001` | Filter kiểm riêng (`checkFilterV2`), code không đổi, quy tắc so theo byte không áp | job-spec `checkAutoReply` bước 2 |
| `MSG-004` | Nội dung tin trả lời không bị diff chạm; có/không reply đã kiểm trên app LINE ở `NEW-9`, `NEW-11`, `NEW-12` | file 03 mục 2 |
| `COMPAT-LEGACY-001` | Flow legacy/V2 cùng lưu bảng `keyword`, query so khớp không phân biệt flow; rule tạo trước fix đã kiểm ở `NEW-9` | job-spec dòng 69, 282–304 |

---

## 3. TC trùng lặp nội dung

Đã rà 24 TC, **không phát hiện trùng lặp**.

- Các cặp giống dữ liệu nhưng **khác tầng oracle** (không tính trùng, bổ trợ nhau theo RULE-07): `NEW-2` (DB local) ↔ `NEW-5` (app LINE) · `NEW-3` (DB local) ↔ `NEW-9` / `NEW-6` (màn + app LINE) · `NEW-4` (bảng 14 tin, DB local) ↔ `NEW-17/18/19/20` (app LINE).
- `NEW-9` ↔ `NEW-22`: cùng kịch bản khách nhưng khác môi trường (job 1-tiến-trình vs job callback production) → không trùng.

---

## 4. Mâu thuẫn trong TCs

**Đã rà**: 24 TC × `spec-features/admin/auto-reply/feature-spec.md` (BR-15 → BR-19, §7 Keyword Matching dòng 777–787) + `job/job-spec.md` (`checkAutoReply` dòng 211–240, `matchingKeyword` dòng 282–304) + `kho-tcs/fa003-tudongtraloi-自動応答.md` (nhóm 14–17, 19, 27–31; MT-01/02/03/04/08; TC-RPL-222, 226–228, 234, 242–247) — **không phát hiện mâu thuẫn**.

- `NEW-9` ↔ `NEW-10` expected ngược nhau nhưng tiền đề khác (bản fix vs bản base) → không phải `CONF-TC`.
- `NEW-12` (2 rule cùng trả lời) khớp BR-15 + kho TC-RPL-227; `NEW-16` tin 4 (khoảng trắng cuối) khớp BR-18 trimEnd + kho TC-RPL-228.
- Spec tự mâu thuẫn về nghĩa `auto_reply.logical` (0 = AND hay OR) — là spec vs spec, TC `NEW-14/15` chấm theo nhãn UI → ghi §8 #3, không phải `CONF-SPEC`.
- Không có tính năng IGNORE (`IG-01`) trong đánh giá ảnh hưởng / diff.

---

## 5. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Nguồn — 24/24 TC | RULE-08 / ENV-003: cả 24 TC chỉ chạy `local` (0 staging, 0 prd). Production xử lý webhook bằng job callback riêng (catalog D `ENV-JOB`) → 20 PASS chưa chứng minh production | Chạy lại 19 TC `env_scope=all` (trừ `NEW-22`) trên staging MySQL 8.0.46 trước release; sau deploy chạy `NEW-22` + TC-ENV003-01 trên prd. Hỏi Dev production có >1 server callback không (kho TC-RPL-222: cb.lmes.jp / cb-2.lmes.jp) |
| I2 | `[MAJOR]` | `NEW-22` | Expected tự miễn lỗi: "nếu tin 1 vẫn kích hoạt cả hai… báo Dev, không phải lỗi mới" → tester có thể không chấm Không đạt dù lỗi KH còn trên production. `env_scope=all` nhưng tiền đề là production sau deploy | Sửa expected: tin 1 có reply = **Không đạt**, mở lại #45620. Đổi `env_scope` → `prd`, `exec_mode` → `manual` |
| I3 | `[MAJOR]` | Dữ liệu từ 2026-10-20 | RULE-04: lỗi đã ghi sai `auto_reply_history` cho rule 「1度のみアクション稼働」 + 部分一致 + keyword 4-byte; Dev không Recover data, để CS quyết; chưa có thống kê phạm vi toàn hệ thống | Dev gửi số bot / rule / friend bị ghi lịch sử do khớp sai trước khi đóng ticket; Leader/CS chốt hướng Recover data rồi mới viết TC cho Q3 |
| I4 | `[MAJOR]` | `[AP-6]` file 03 mục 3 | Mục 3 chỉ có `matchingKeyword`. Lỗi gốc là hành vi MySQL 8 (từ 20/10) → có thể lặp ở query khác dùng `LOCATE` / `COLLATE utf8mb4_bin` (vd check keyword trùng BR-01, tìm kiếm quy tắc `searchByKeyWord`) và ở brand dùng chung job (Lwaka / Saruwaka / Lgram) | Hỏi Dev đã grep toàn java-job + web chưa và brand nào dùng chung `AutoReplyKeywordRepository`; có nơi lặp → tách ticket |
| I5 | `[MAJOR]` | `#41604`, `#41605` | 2 TC duy nhất kiểm loại thông báo 1:1 (REQ-008) đều skip. Tiền đề chép từ task #40044 (migration ALTER `callback_event`, cờ `WEBHOOK_RELAY_*`, keyword `キーワード40044`, `NEW-126`); `#41605` dữ liệu không cụ thể ("1 tin gần giống từ khóa", "biết chính xác quy tắc khớp") | Bỏ phần #40044; viết lại theo #45620: rule 🫶 部分一致 + rule ABC 部分一致; `#41605` dùng tin cụ thể `abc` (gần giống) · `😊` (chỉ emoji). Chạy lại |
| I6 | `[MAJOR]` | `NEW-3`, `NEW-4`, `NEW-11`, `NEW-12`, `NEW-13`, `#41605` | TC không tự đầy đủ: tiền đề trỏ sang TC khác ("Như TC kịch bản khách sau fix", "Như TC gửi đúng 🫶", "như các TC trước", "y như TC trước"…); `NEW-12` không ghi action/tag của rule | Chép đủ cấu hình rule (keyword · 部分一致 · 何度でも · action) vào tiền đề từng TC |
| I7 | `[MAJOR]` | 24/24 TC; `NEW-19` | `Trạng thái đánh giá spec` trống cả 24 TC. `NEW-19` tự ghi "cần leader xác nhận 🫶🏻 khớp 🫶" (cùng kỳ vọng ở `NEW-4` dòng 3, 14) nhưng chưa ghi đã hỏi ai | Leader chốt rule emoji + modifier (§8 #2); TC còn lại ghi `Spec ghi rõ` (job-spec dòng 228–230 + handoff Dev) |
| I8 | `[MINOR]` | `NEW-6` | Mã `STATE-DEP-001` (Trigger: hành động phụ thuộc đã lên lịch) không khớp nội dung (tự 確認済み khi khớp keyword) | Đổi sang mã đúng nội dung (vd `FUNC-001`) |

---

## 6. TCs thừa / ngoài phạm vi task

Đã rà 24 TC — **không có TC nào ngoài phạm vi task**.

- Gate: `NEW-21` (ký tự đặc biệt), `NEW-20` (chữ Hán 4-byte), `NEW-7` (bỏ qua 【】), `NEW-8` (friend bị chặn) đều đi qua câu so khớp bị sửa; `#41604` / `#41605` (loại thông báo) là hệ quả trực tiếp của cờ khớp keyword → không thừa.

---

## 7. TCs đề xuất bổ sung (5)

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs/fa003-tudongtraloi-自動応答.md` (bảng Coverage 33 nhóm; nhóm Runtime 27–31) |
| Vùng regression phát hiện từ kho | TC-RPL-234 (trigger hiển thị ở 1:1チャット) → G2 · MT-03 + TC-RPL-227 (case kết hợp 全てのメッセージ + keyword chưa từng test) → R1 · TC-RPL-222 (domain callback cb / cb-2) → G1 · MT-01 (keyword tối đa 30 ký tự) → Q5 |
| Conflict expected vs kho | Không |
| GAP dùng lại TC kho (không viết mới) | Không — TC-RPL-234 chỉ dùng làm khuôn nhãn trigger, không có kịch bản emoji |
| Căn cứ TC regression `R<x>` | R1 ← Studio dev_impact "Không đổi: 全てのメッセージに反応" + kho MT-03 / TC-RPL-227 (mọi TC hiện có đều tạm dừng rule 全てのメッセージ) |
| Xác nhận chống trùng | Đã đối chiếu 24 TC ở BƯỚC 0 + kho — **không TC đề xuất nào trùng** (TC-ENV003-01 khác `NEW-22`: keyword chữ / 完全一致 / AND thay vì emoji) |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Surface | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-ENV003-01 | Job | ENV-003 | Auto reply 自動応答: Job callback production sau deploy — keyword chữ 部分一致 / 完全一致 / AND | Normal | manual | prd | job, line-friend, web | Production sau deploy job + job callback: câu so khớp keyword trên job callback phân biệt katakana / chữ thường, 完全一致 và AND 2 keyword vẫn đúng | - Nhánh release-t09-2026 (có fix #45620) đã merge vào release-callback-t09-2026; job và job callback đã deploy lên production cùng đợt<br>- Đăng nhập admin production, chọn bot test của tester (không dùng bot khách hàng)<br>- 1 user test LINE của tester là bạn bè đang hoạt động: システム表示名 AR45620_F01 (gọi tắt F01)<br>- Tạm dừng Trạng thái hoạt động 「稼働状況」 mọi auto reply khác của bot test, kể cả rule 「全てのメッセージに反応」<br>- Các keyword dưới đây chưa tồn tại trong bot (BR-01)<br>- Tạo ở màn Tự động trả lời 「自動応答」 → 「新規作成」 4 rule, đều 「設定したキーワードに反応」 · 「常に（24時間/365日）反応する」 · 「何度でもアクション稼働」 · action 「テキスト」<br>- Rule N2: keyword にじ 「部分一致」 → REPLY-N2-<RUN><br>- Rule A2: keyword ABC 「部分一致」 → REPLY-A2-<RUN><br>- Rule E3: keyword はれ 「完全一致」 → REPLY-E3-<RUN><br>- Rule AND2: Điều kiện phản ứng 「反応条件」 = 「全てのキーワードに当てはまる時に反応」, 2 keyword 🍎 「部分一致」 + りんご 「部分一致」 → REPLY-AND2-<RUN> | 1. F01 dùng app LINE gửi tin 1, chờ tối đa 60 giây.<br>2. Mở Chat 1:1 「1:1チャット」 của F01, ghi lại tin trả lời mới.<br>3. Lặp bước 1–2 lần lượt với tin 2 → tin 8.<br>4. F01 đếm trên app LINE tổng số tin trả lời tự động đã nhận.<br>5. Ghi commit đang chạy của job và job callback vào kết quả.<br>6. Tạm dừng 4 rule của lượt. | Tin 1: 今日はにじが見えた<br>Tin 2: ニジ<br>Tin 3: xxABCxx<br>Tin 4: abc<br>Tin 5: はれ<br>Tin 6: はれです<br>Tin 7: りんご🍎ください<br>Tin 8: りんご😊 | - Tin 1: đúng 1 REPLY-N2-<RUN><br>- Tin 3: đúng 1 REPLY-A2-<RUN><br>- Tin 5: đúng 1 REPLY-E3-<RUN><br>- Tin 7: đúng 1 REPLY-AND2-<RUN><br>- Tin 2 (katakana), tin 4 (chữ thường), tin 6 (thừa ký tự với 完全一致), tin 8 (😊 không thay được 🍎): không có tin trả lời nào<br>- App LINE F01 nhận tổng đúng 4 tin trả lời, khớp 1:1チャット<br>- Tin 2, 4 hoặc 8 có trả lời = job callback production chưa có fix → Không đạt, mở lại #45620 |  | Lấp G1 · Lấp Q4 · Lấp Q2 (job callback) · regression · căn cứ: catalog D ENV-JOB dòng 310 (production tách job callback) + Studio dev_impact "callback branch chưa có fix" + deploy note Dev · bổ sung cho NEW-22 (chỉ kiểm keyword emoji) · chỉ prd vì job callback tách riêng chỉ có trên production · manual vì môi trường production · production có >1 server callback (kho TC-RPL-222) → chạy 1 bot / server · Đánh giá spec: Spec ghi rõ (job-spec dòng 228–230 + handoff Dev) · Evidence: screenshot 1:1チャット + app LINE F01 + commit 2 job |
| TC-FUNC001-01 | UI | FUNC-001 | Chat 1:1 1:1チャット: Trigger detail 送信トリガー詳細 của tin auto reply 自動応答 keyword emoji 部分一致 | Normal | auto | dev, local, prd, staging | web, line-friend | Trigger detail 「送信トリガー詳細」 ở 1:1チャット: tin không chứa keyword không sinh tin trả lời; tin khớp 🫶 sinh đúng 1 tin trả lời có trigger 「自動応答」 loại keyword | - Job đang chạy bản có fix #45620 trên MySQL 8 (staging / local DB slot MySQL 8 / production sau deploy)<br>- Đăng nhập admin, chọn bot test<br>- 1 user test LINE là bạn bè đang hoạt động: システム表示名 AR45620_F01 (gọi tắt F01)<br>- Tạm dừng Trạng thái hoạt động 「稼働状況」 mọi auto reply khác của bot, kể cả rule 「全てのメッセージに反応」<br>- Tạo ở màn Tự động trả lời 「自動応答」 → 「新規作成」 2 rule, đều 「設定したキーワードに反応」 · 「常に（24時間/365日）反応する」 · 「何度でもアクション稼働」 · action 「テキスト」<br>- Rule H3: keyword 🫶 「部分一致」 → REPLY-H3-<RUN><br>- Rule R3: keyword 🌈 「部分一致」 → REPLY-R3-<RUN> | 1. F01 dùng app LINE gửi tin 1, chờ tối đa 60 giây.<br>2. Mở Chat 1:1 「1:1チャット」 của F01, kiểm các tin bot gửi sau tin 1.<br>3. F01 gửi tin 2, chờ tối đa 60 giây.<br>4. Ở 1:1チャット, bấm xem trigger 「送信トリガー詳細」 của tin REPLY-H3-<RUN> vừa nhận.<br>5. F01 kiểm trên app LINE các tin trả lời đã nhận. | Tin 1: ありがとうございます😊 引き続きよろしくお願いいたします。現在、準備を進めています😭<br>Tin 2: 🫶 | - Sau tin 1: 1:1チャット không có tin nào của bot sau tin của F01 → không có dòng trigger 「自動応答」 nào<br>- Sau tin 2: đúng 1 tin REPLY-H3-<RUN>, không có REPLY-R3-<RUN><br>- Trigger detail của REPLY-H3-<RUN>: tính năng 「自動応答」, loại quy tắc keyword (kho ghi 「キーワード」; KH mô tả 「設定したキーワードに反応」), tên quản lý 「-」<br>- App LINE F01 nhận tổng đúng 1 tin trả lời (REPLY-H3-<RUN>) |  | Lấp G2 · Lấp Q1 · dẫn từ kho TC-RPL-234 (khuôn nhãn trigger) · KH phát hiện lỗi qua 「送信トリガー詳細」 (file 01) · dev chạy MySQL 5.7 không tái hiện lỗi gốc → kết quả dev chỉ là regression · tầng DB `auto_reply_history` đã có ở NEW-2 / NEW-3 · Đánh giá spec: Spec không ghi nhãn trigger — expected theo kho TC-RPL-234, cần Leader xác nhận · Evidence: screenshot trigger detail + app LINE |
| TC-REGSHARED001-01 | Job | REG-SHARED-001 | Auto reply 自動応答: Keyword chữ 部分一致 dài tối đa 30 ký tự ở đầu / cuối / toàn bộ tin | Boundary | auto | dev, local, prd, staging | job, line-friend, web | Câu so khớp 部分一致 theo byte với keyword tiếng Nhật 30 ký tự: khớp khi keyword nằm đầu / cuối / bằng cả tin, không khớp khi thiếu hoặc lệch 1 ký tự | - Job đang chạy bản có fix #45620 trên MySQL 8<br>- Đăng nhập admin, chọn bot test<br>- 1 user test LINE là bạn bè đang hoạt động: システム表示名 AR45620_F01 (gọi tắt F01)<br>- Tạm dừng Trạng thái hoạt động 「稼働状況」 mọi auto reply khác của bot<br>- Tạo ở màn Tự động trả lời 「自動応答」 → 「新規作成」 rule L30: 「設定したキーワードに反応」, keyword あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ (30 ký tự) 「部分一致」, 「常に（24時間/365日）反応する」, 「何度でもアクション稼働」, action 「テキスト」 REPLY-L30-<RUN><br>- Mở lại rule L30 bằng 「編集」, keyword hiển thị đủ 30 ký tự (không bị cắt) | 1. F01 dùng app LINE gửi tin 1, chờ tối đa 60 giây.<br>2. Mở Chat 1:1 「1:1チャット」 của F01, đếm tin REPLY-L30-<RUN> mới.<br>3. Lặp bước 1–2 lần lượt với tin 2 → tin 6.<br>4. F01 đếm trên app LINE tổng số tin trả lời tự động đã nhận. | Tin 1: あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ (bằng keyword)<br>Tin 2: あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほです (keyword ở đầu)<br>Tin 3: 今日はあいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ (keyword ở cuối)<br>Tin 4: あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへ (thiếu ほ cuối, 29 ký tự)<br>Tin 5: いうえおかきくけこさしすせそたちつてとなにぬねのはひふへほ (thiếu あ đầu)<br>Tin 6: あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへホ (ほ → katakana ホ) | - Tin 1, 2, 3: mỗi tin đúng 1 REPLY-L30-<RUN> (keyword nằm nguyên trong tin ở mọi vị trí)<br>- Tin 4, 5, 6: không có tin trả lời (thiếu hoặc lệch 1 ký tự thì không khớp)<br>- App LINE F01 nhận tổng đúng 3 tin trả lời |  | Lấp Q5 · dẫn từ kho MT-01 (keyword lưu tối đa 30 ký tự — đang chờ quyết định, bước 「編集」 xác nhận độ dài thực tế) · biên vị trí của LOCATE theo byte (keyword 90 byte) · Đánh giá spec: Spec ghi rõ (BR-18 LOCATE tìm keyword trong text) · Evidence: screenshot 1:1チャット + app LINE |
| TC-DATATEXT001-01 | Job | DATA-TEXT-001 | Auto reply 自動応答: Tin rất dài toàn ký tự 4-byte khác keyword emoji 部分一致 | Abnormal | auto | dev, local, prd, staging | job, line-friend, web | Tin 1.000 ký tự toàn emoji / chữ Hán 4-byte khác keyword không kích hoạt auto reply 🫶 / 🌈; cùng độ dài có 🫶 ở ký tự cuối thì chỉ rule 🫶 trả lời | - Job đang chạy bản có fix #45620 trên MySQL 8<br>- Đăng nhập admin, chọn bot test<br>- 1 user test LINE là bạn bè đang hoạt động: システム表示名 AR45620_F01 (gọi tắt F01)<br>- Tạm dừng Trạng thái hoạt động 「稼働状況」 mọi auto reply khác của bot<br>- Tạo ở màn Tự động trả lời 「自動応答」 → 「新規作成」 2 rule, đều 「設定したキーワードに反応」 · 「常に（24時間/365日）反応する」 · 「何度でもアクション稼働」 · action 「テキスト」<br>- Rule H4: keyword 🫶 「部分一致」 → REPLY-H4-<RUN><br>- Rule R4: keyword 🌈 「部分一致」 → REPLY-R4-<RUN><br>- Chuẩn bị sẵn 3 chuỗi tin trong file text để copy-paste vào app LINE (không gõ bằng bàn phím emoji) | 1. F01 paste và gửi tin 1, chờ tối đa 60 giây.<br>2. Mở Chat 1:1 「1:1チャット」 của F01: kiểm tin của F01 hiển thị đủ và tin trả lời mới.<br>3. Lặp bước 1–2 với tin 2, rồi tin 3.<br>4. F01 đếm trên app LINE tổng số tin trả lời tự động đã nhận. | Tin 1: chuỗi 😊😭🙇💕🎉 lặp 200 lần (1.000 emoji 4-byte, không có 🫶 / 🌈)<br>Tin 2: chữ Hán 𠮷 (U+20BB7) lặp 1.000 lần<br>Tin 3: chuỗi 😊😭🙇💕🎉 lặp 199 lần + 😊😭🙇💕🫶 (🫶 là ký tự thứ 1.000) | - Tin 1, 2: không có REPLY-H4-<RUN> hay REPLY-R4-<RUN>; tin của F01 hiển thị đủ trong 1:1チャット, không bị cắt<br>- Tin 3: đúng 1 REPLY-H4-<RUN>, không có REPLY-R4-<RUN><br>- App LINE F01 nhận tổng đúng 1 tin trả lời |  | Lấp Q6 · tin toàn ký tự 4-byte = trường hợp xấu nhất của lỗi gốc (utf8mb4_unicode_ci coi mọi ký tự 4-byte bằng nhau) · 1.000 emoji = 2.000 đơn vị UTF-16, dưới giới hạn 5.000 của tin LINE · Đánh giá spec: Spec ghi rõ (BR-18 + handoff Dev "emoji khác nhau không còn bị coi là giống nhau") · Evidence: screenshot 1:1チャット + app LINE |
| TC-REGSHARED001-02 | Job | REG-SHARED-001 | Auto reply 自動応答: Rule 全てのメッセージに反応 chạy cùng rule keyword emoji 部分一致 | Normal | auto | dev, local, prd, staging | job, line-friend, web | Bot có cả rule 「全てのメッセージに反応」 và rule keyword emoji 部分一致: tin không chứa keyword chỉ kích hoạt rule 全てのメッセージ; tin chứa 🫶 kích hoạt cả 2 | - Job đang chạy bản có fix #45620 trên MySQL 8<br>- Đăng nhập admin, chọn bot test<br>- 1 user test LINE là bạn bè đang hoạt động: システム表示名 AR45620_F01 (gọi tắt F01)<br>- Tạm dừng Trạng thái hoạt động 「稼働状況」 mọi auto reply khác của bot<br>- Tạo ở màn Tự động trả lời 「自動応答」 → 「新規作成」 3 rule, đều 「常に（24時間/365日）反応する」 · 「何度でもアクション稼働」 · action 「テキスト」<br>- Rule ALL: 「全てのメッセージに反応」 → REPLY-ALL-<RUN><br>- Rule H5: 「設定したキーワードに反応」, keyword 🫶 「部分一致」 → REPLY-H5-<RUN><br>- Rule R5: 「設定したキーワードに反応」, keyword 🌈 「部分一致」 → REPLY-R5-<RUN> | 1. F01 dùng app LINE gửi tin 1, chờ tối đa 60 giây.<br>2. Mở Chat 1:1 「1:1チャット」 của F01, đếm tin trả lời mới theo từng rule.<br>3. F01 gửi tin 2, chờ tối đa 60 giây.<br>4. Đếm lại tin trả lời mới theo từng rule.<br>5. F01 đếm trên app LINE tổng số tin trả lời tự động đã nhận. | Tin 1: ありがとうございます😊 引き続きよろしくお願いいたします。現在、準備を進めています😭<br>Tin 2: 🫶 | - Tin 1: đúng 1 REPLY-ALL-<RUN>; không có REPLY-H5-<RUN> / REPLY-R5-<RUN><br>- Tin 2: đúng 1 REPLY-ALL-<RUN> và đúng 1 REPLY-H5-<RUN> (2 rule cùng khớp là hợp lệ — BR-15); không có REPLY-R5-<RUN><br>- App LINE F01 nhận tổng đúng 3 tin trả lời |  | Lấp R1 · regression · căn cứ: Studio dev_impact "Không đổi: 全てのメッセージに反応" + kho MT-03 / TC-RPL-227 (case kết hợp 全てのメッセージ + keyword chưa từng test; mọi TC hiện có đều tạm dừng rule 全てのメッセージ) · Đánh giá spec: Spec ghi rõ (BR-15 multi-rule; job-spec `checkAutoReply`: KEYWORD_ANY luôn match) · Evidence: screenshot 1:1チャット + app LINE |

**Q không đề xuất TC mới** (lý do):

| Q | Lý do | Việc cần làm |
|---|---|---|
| Q1 (phần Abnormal + Boundary) | Nội dung đã có, chỉ sai mã | Đổi mã `NEW-9` → `FUNC-001` (Abnormal), `NEW-4` → `FUNC-001` (Boundary) trên Studio |
| Q2 `JOB-001` | Phần retry / backoff / rate limit LINE API không bị diff chạm; "bản ghi vào = bản ghi xử lý" đã có ở `NEW-21`; job callback production do TC-ENV003-01 lấp | Đổi mã `NEW-21` → `JOB-001` + ghi lý do thiếu Normal/Abnormal (RULE-01) |
| Q3 `REG-RUN-001` | Expected phụ thuộc quyết định Recover data (giữ hay xoá `auto_reply_history` ghi sai) — chưa chốt, không tự chọn bên | Dev thống kê phạm vi (I3) → Leader/CS chốt → viết 1 TC `REG-RUN-001` |
| Q7 `MSG-USER-001` | Các trạng thái lifecycle (mới add · 既存友だち取得 · unblock) đi chung 1 câu so khớp với nhánh active đã cover | Ghi lý do RULE-01 vào `NEW-8`, hoặc tách tin 2 (🍀 có reply) thành TC Normal |

---

## 8. Spec update needed

| # | Section spec | Nội dung cần update | Nguồn mâu thuẫn | Ai chốt |
|---|---|---|---|---|
| 1 | `feature-spec.md` §5 BR-18 + §7 Keyword Matching (dòng 777–779); `job/job-spec.md` dòng 228, 292 | Nhánh 部分一致 đổi sang `LOCATE(CAST(keyword AS BINARY), CAST(val AS BINARY))`; ghi rõ 部分一致 phân biệt emoji, hoa/thường, hiragana/katakana, toàn/nửa độ rộng, không phụ thuộc collation / version MySQL | Cách fix #45620 (file 03 mục 2) — spec còn mô tả SQL cũ | Dev |
| 2 | `feature-spec.md` §5 BR-18 | Emoji kèm modifier (tông da U+1F3FB…, U+FE0F) chứa nguyên keyword gốc thì có khớp 部分一致 không (`NEW-19`, `NEW-4` kỳ vọng: có) | `NEW-19` ghi chờ Leader xác nhận (I7) | Leader / PM |
| 3 | `feature-spec.md` dòng 487–489 + `job/job-spec.md` dòng 226–227 vs `feature-spec.md` dòng 604, 786–787, 1005 | Nghĩa `auto_reply.logical`: 2 chỗ ghi 0 = OR, 3 chỗ ghi 0 = AND (「全てのキーワードに当てはまる時に反応」). `NEW-14/15` chấm theo nhãn UI và đã pass | Spec tự mâu thuẫn (Studio finding F5, note `NEW-14`) | Dev (đối chiếu code) |
