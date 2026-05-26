# 05 — Review Report

## Thông tin

| Trường | Giá trị |
|---|---|
| Bug ID | LME-2054 |
| Reviewer (Leader) | Lê Thị C (Test Leader) |
| Tester được review | Trần Thị B |
| Ngày review | 2026-04-23 |
| Version TCs | v1 |
| Vòng review | Round 1 |

---

## 1. Verdict

- [ ] APPROVED
- [ ] APPROVED WITH CHANGES
- [x] **REJECTED**

**Lý do ngắn gọn**: Bộ TCs cover được phần lớn direct impact và bug fix (TC001, TC002 rất tốt) nhưng còn GAP đáng kể ở F4 (perf), T3, T4, T5, D3 và thiếu chiều negative/boundary. Cần bổ sung 5 TCs trước khi approve.

---

## 2. Tóm tắt cho member

B viết TCs khá chắc ở phần fix chính (TC001 capture rất đúng spirit của bug — test tag thay đổi sau lúc create). Điểm cần bổ sung: (1) thêm regression cho các tính năng phụ T3/T4/T5 mà Dev đã flag trong mục 4.3, (2) thêm negative & boundary cho edge case data (D3 — send log), và (3) self-check đã note thiếu 3 mục, lần tới hãy fix ngay trong vòng đầu để tăng chất lượng bản submit v1.

---

## 3. Coverage Matrix

| Impact | Loại | Priority | TCs map | # TC | Status |
|---|---|---|---|---|---|
| BUG (root cause) | Fix | — | TC001 | 1 | **OK** |
| F1 — `BroadcastSender::send()` | Function | Direct | TC002 | 1 | **RISK** (chỉ positive, thiếu negative) |
| F2 — `BroadcastScheduler::enqueueScheduledBroadcast()` | Function | Direct | TC001 (gián tiếp) | 1 | **RISK** (cần TC riêng verify không còn cache) |
| F3 — `preview()` | Function | Indirect | TC003 | 1 | **OK** |
| F4 — `FriendTagRepository::findFriendsByTag()` | Function | Indirect | — | **0** | **GAP** |
| F5 — `BroadcastRepository::findById()` | Function | Indirect | TC005 | 1 | **OK** |
| D1 — `broadcasts.cached_recipient_ids` | Data | — | TC007 | 1 | **OK** |
| D2 — `broadcasts` read path | Data | — | TC002, TC006 | 2 | **OK** |
| D3 — `broadcast_send_logs` | Data | — | — | **0** | **GAP** |
| D4 — `friends_tags` read frequency | Data | — | — | — | Đã được Dev note là load test riêng — OK bỏ qua |
| T1 — Scheduled broadcast send flow | Feature | High | TC001, TC002, TC008 | 3 | **OK** |
| T2 — Immediate broadcast send flow | Feature | Medium | TC004 | 1 | **OK** |
| T3 — Preview count screen | Feature | Low | TC003 | 1 | **OK** |
| T4 — Broadcast detail screen | Feature | Medium | TC005 | 1 | **RISK** (chỉ check absence, thiếu positive flow đọc broadcast) |
| T5 — Performance multi-broadcast | Feature | Medium | — | **0** | **GAP** (smoke test — theo note Dev ở mục 4, chỉ cần 1 TC) |

### ORPHAN TCs (nếu có)

Không có TC orphan. Mọi TC đều map được.

---

## 4. Issues phát hiện

### 4.1 Blocker

- **[BLOCKER] GAP-1**: Không có TC nào verify F4 (`FriendTagRepository::findFriendsByTag()` được gọi tại send time). Đây là core của fix — cần thêm TC verify trực tiếp query path, không phải chỉ end-to-end. → Thêm `TC-NEW-01`.
- **[BLOCKER] GAP-2**: Không có TC cho D3 (`broadcast_send_logs`). Log record là output quan trọng — nếu số recipients trong log sai, ops team không detect được regression. → Thêm `TC-NEW-02`.
- **[BLOCKER] GAP-3**: Không có smoke test cho T5 (performance). Dev đã confirm load test riêng, nhưng TC chức năng vẫn cần 1 case verify 3+ scheduled broadcast chạy gần nhau không conflict/deadlock. → Thêm `TC-NEW-03`.

### 4.2 Major

- **[MAJOR] TC002**: Chỉ có case remove tag (negative). Cần thêm case mixed: vừa thêm friend mới vào tag, vừa remove khỏi tag khác — verify resolve đúng tại send time. → Thêm `TC-NEW-04`.
- **[MAJOR] GAP-4**: F2 (enqueueScheduledBroadcast) chỉ được verify gián tiếp qua TC001. Nên có TC riêng verify sau khi tạo scheduled, field `cached_recipient_ids` = null ngay tại thời điểm tạo (không đợi đến send mới check). → Thêm `TC-NEW-05`.
- **[MAJOR] TC005**: Chỉ check absence của field trên UI. Cần verify API response cũng không expose field này (backend contract). → Update TC005 thêm bước API check.

### 4.3 Minor

- **[MINOR] TC001 — Precondition**: "Bot có 150 friends tag VIP" — nên cụ thể timezone của bot (JST) vì bug gốc liên quan timezone. → Thêm vào precondition.
- **[MINOR] TC006 — Expected**: "Broadcast complete với 0 recipients, không lỗi" — cần cụ thể "status = completed, sent_count = 0, error = null".
- **[MINOR] TC007 — Type**: gán là `Positive` nhưng verify migration là closer tới `Regression` — đổi type cho đúng convention.

### 4.4 Nit

- **[NIT]** Priority phân bổ hơi lệch High: High=5, Medium=2, Low=1. Với bug `High priority`, tỷ lệ này OK — không cần đổi. Ghi nhận để tham khảo.
- **[NIT]** Có thể gộp TC005 và TC004 thành 1 suite regression nhỏ. Giữ nguyên nếu muốn track riêng biệt cũng được.

---

## 5. TCs đề xuất bổ sung

| TC ID gợi ý | Title | Precondition | Steps | Expected | Priority | Type | Map to Impact |
|---|---|---|---|---|---|---|---|
| TC-NEW-01 | Verify send flow gọi FriendTagRepository tại send time, không dùng cache | Bot JST, 10 friends tag "A" | 1. Enable query log DB.<br>2. Tạo scheduled broadcast tag "A", send sau 5 phút.<br>3. Sau khi send xong, check query log. | Có query SELECT từ `friends_tags` trong khoảng ±2s quanh send time, không có đọc từ `cached_recipient_ids`. | High | Positive | F4 |
| TC-NEW-02 | broadcast_send_logs ghi đúng số recipients thực tế tại send time | Bot có 100 friends tag "VIP" | 1. Tạo scheduled broadcast tag "VIP".<br>2. Add 20 friend vào tag VIP.<br>3. Chờ send.<br>4. Query `broadcast_send_logs` cho broadcast này. | Record có `recipient_count = 120`, khớp với số friend thực tế gửi. | High | Positive | D3 |
| TC-NEW-03 | Smoke test — 3 scheduled broadcast trên cùng tag chạy đồng thời | Bot có 500 friends tag "VIP" | 1. Tạo 3 scheduled broadcast tag "VIP", cùng send time.<br>2. Chờ send. | Cả 3 broadcast gửi thành công, mỗi broadcast gửi 500 recipients, không deadlock/timeout. | Medium | Regression | T5 |
| TC-NEW-04 | Mixed tag change — friend vừa thêm vào tag, vừa remove khỏi tag sau lúc create | Bot có 100 friends tag "VIP" | 1. Tạo scheduled broadcast tag "VIP", send sau 10 phút.<br>2. Add 30 friend mới vào VIP.<br>3. Remove tag VIP khỏi 20 friends cũ.<br>4. Chờ send. | Broadcast gửi đến 110 friends (100 + 30 - 20). | High | Positive | F1, D2 |
| TC-NEW-05 | Sau khi tạo scheduled broadcast, field cached_recipient_ids = null ngay lập tức | — | 1. Tạo scheduled broadcast tag "VIP" (≥ 50 friend).<br>2. Query DB ngay sau khi submit. | `broadcasts.cached_recipient_ids IS NULL` cho record vừa tạo. | Medium | Positive | F2, D1 |

---

## 6. Spec update needed

- [x] Không cần update spec
- [ ] Cần update spec

**Ghi chú**: Spec v2.3 (BR-02) đã cover case này — bug là do code sai, không phải spec thiếu.

---

## 7. Checklist đã chạy

- [x] A. Coverage (phát hiện 3 GAP, 3 RISK)
- [x] B. Chất lượng từng TC (1 MINOR về precondition, 1 MINOR về expected, 1 MINOR về type classification)
- [x] C. Chất lượng bộ TC tổng thể (priority distribution OK, type distribution thiếu negative/boundary)
- [x] D. Spec alignment (OK — BR-01 đến BR-05 đều có TC map)
- [x] E. Hành chính (OK)

---

## 8. Ký duyệt

| Người | Tên | Ngày |
|---|---|---|
| Reviewer (Leader) | Lê Thị C | 2026-04-23 |
| Tester | (chờ B ký sau khi đọc feedback) | — |
