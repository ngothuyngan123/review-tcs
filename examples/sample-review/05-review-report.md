# 05 — Review Report

> Ví dụ mẫu theo format **rút gọn** (2026-09-05). Report chỉ ghi **phần THIẾU + việc phải làm**.
> Coverage matrix / bảng quan điểm / fix-shape vẫn chạy ở BƯỚC 2 · 3 · 3c nhưng là **nháp nội bộ**, không ghi vào file.

## 0. Nguồn TC

| Trường | Giá trị |
|---|---|
| Nguồn đã dùng | `04-tc-list.md` (Studio: 0 task cho ticket LME-2054) |
| Tổng số TC review | `8` |

---

## 1. Coverage — đánh giá ảnh hưởng Dev + diff code

**Kết luận**: `10/15 vùng ảnh hưởng đủ TC · 3 GAP · 2 RISK`

| # | Vùng thiếu | Chiều | TC hiện có | Thiếu gì | Severity |
|---|---|---|---|---|---|
| G1 | `F4 — FriendTagRepository::findFriendsByTag()` | `dev-impact` | `không có` | `GAP — 0 TC verify query path tại send time; mọi TC hiện có chỉ end-to-end` | `[BLOCKER]` |
| G2 | `D3 — broadcast_send_logs` | `dev-impact` | `không có` | `GAP — 0 TC verify recipient_count ghi vào log` | `[BLOCKER]` |
| G3 | `T5 — nhiều scheduled broadcast chạy đồng thời` | `dev-impact` | `không có` | `GAP — 0 TC smoke concurrency (Dev đã tách load test riêng nhưng vẫn cần 1 case chức năng)` | `[BLOCKER]` |
| G4 | `BroadcastScheduler::enqueueScheduledBroadcast()` — nhánh bỏ ghi cache lúc create | `diff code` | `TC001` | `RISK — chỉ verify gián tiếp lúc send; không TC nào check cached_recipient_ids = null NGAY sau khi tạo` | `[MAJOR]` |
| G5 | `F1 — BroadcastSender::send()` | `dev-impact` | `TC002` | `RISK — chỉ case remove tag; thiếu case mixed (vừa add vừa remove) → không chứng minh được resolve lại toàn bộ tại send time` | `[MAJOR]` |

- Không có TC orphan — 8/8 TC đều map được về `BUG` / `F*` / `D*` / `T*`.
- `D4 — friends_tags read frequency`: Dev đã note tách sang load test riêng → **không tính GAP**.

---

## 2. Thiếu so với quan điểm test

**Kết luận**: `6 quan điểm Trigger khớp task · 2 chưa cover đủ`

| # | Mã quan điểm | Ưu tiên | Thiếu gì | Severity |
|---|---|---|---|---|
| Q1 | `MSG-004` | `Cao` | `RISK — có TC đếm số recipient trên màn admin, nhưng không TC nào nhận tin THẬT trên LINE app (RULE-06: dừng trước output cuối)` | `[MAJOR]` |
| Q2 | `DATA-COUNT-001` | `Cao` | `RISK — chỉ đối chiếu 1 nguồn (màn preview); thiếu đối chiếu send log + phép tính tay 100+30-20` | `[MAJOR]` |

---

## 3. TC trùng lặp nội dung

Đã rà `8` TC, phát hiện 1 nhóm trùng.

| Nhóm trùng | TC giữ lại | TC đề nghị xóa / gộp | Loại trùng | 4 yếu tố trùng nhau | Severity |
|---|---|---|---|---|---|
| DUP-1 | `TC004` | `TC005` | `DUP-SUBSET` | Cùng `MSG-001` × `Normal` × màn chi tiết broadcast × cùng tiền đề bot 100 friend — steps của TC005 nằm trọn trong TC004 | `[MINOR]` |

- **Gate đã chạy**: giả định xóa `TC005` → `T4` vẫn còn `TC004` cover, coverage §1 + quan điểm §2 không đổi → `Có`, giữ đề xuất **xóa**.
- `DUP-INFLATE`: không có. `DUP-CONFLICT`: không có.

---

## 4. Issues khác

| # | Severity | TC / phạm vi | Vấn đề | Đề xuất fix |
|---|---|---|---|---|
| I1 | `[MAJOR]` | Toàn bộ 8 TC | Cột `Kết quả thực thi` rỗng — không xác định được TC đã chạy hay chưa; coverage ở §1 chỉ là trên giấy | Yêu cầu tester chạy + điền kết quả trước vòng 2; mọi kết luận "đủ TC" ở §1 hiện là `RISK` |
| I2 | `[MAJOR]` | `TC005` | Chỉ check field không hiển thị trên UI, không verify API response còn expose `cached_recipient_ids` không (RULE-07) | Thêm bước gọi thẳng `GET /api/broadcasts/<id>` và assert field vắng mặt |
| I3 | `[MINOR]` | `TC001` | `Điều kiện tiền đề` thiếu timezone của bot — bug gốc liên quan JST, người khác dựng lại env có thể lệch | Thêm `bot timezone = JST (Asia/Tokyo)` vào tiền đề |
| I4 | `[MINOR]` | `TC006` | `Kết quả mong đợi` không đo lường được: "complete với 0 recipients, không lỗi" | Sửa thành `status = completed · sent_count = 0 · error = null` |
| I5 | `[NIT]` | Bộ TC | File dùng format 10 cột cũ (có `Priority`, `Type = Regression`) | Task cũ → giữ nguyên, không convert; TC mới viết theo 16 cột canonical |

---

## 5. TCs đề xuất bổ sung

**Đã đối chiếu trước khi viết**:

| Mục | Kết quả |
|---|---|
| File kho TCs đã đọc | `kho-tcs chưa có FA-004 (Broadcast) — không đối chiếu được` |
| Vùng regression phát hiện từ kho | `không có` |
| Conflict expected vs kho | `Không` |
| GAP dùng lại TC kho (không viết mới) | `Không` |
| Xác nhận chống trùng | Đã đối chiếu `8` TC ở BƯỚC 0 — **không TC đề xuất nào trùng** |

| ID | Nhóm | Mã quan điểm | Màn hình/chức năng | Loại case | Chạy | Phạm vi ENV | Tên case | Tiền điều kiện | Các bước thực hiện | Dữ liệu nhập | Kết quả mong đợi | Kết quả thực thi | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-MSG004-01 | UI | MSG-004 | Gửi broadcast theo tag | Normal | manual | product | Friend nhận được tin thật trên LINE app sau khi tag đổi trước giờ gửi | - Bot timezone JST<br>- 100 friend gắn tag `VIP`<br>- 2 máy thật: iOS + Android đã kết bạn | 1. Tạo scheduled broadcast tag `VIP`, hẹn gửi sau 10 phút.<br>2. Gắn tag `VIP` cho 30 friend mới (gồm 2 máy thật).<br>3. Bỏ tag `VIP` khỏi 20 friend cũ.<br>4. Chờ tới giờ gửi.<br>5. Mở LINE trên 2 máy thật kiểm tra tin. | tag `VIP`, +30 friend, −20 friend | Màn kết quả gửi hiện `110` người · 2 máy thật **đều nhận được** tin trong LINE · 20 friend đã bỏ tag không nhận | | Lấp `G5` · `Q1` · Đánh giá spec: Spec ghi rõ (BR-02) · Evidence: ảnh chụp màn LINE 2 máy + màn kết quả gửi · RULE-06 · RULE-08 |
| TC-DATACOUNT001-01 | Data | DATA-COUNT-001 | Log gửi broadcast | Normal | manual | staging | Số người trong log gửi khớp số friend thực tế tại thời điểm gửi | - Bot có 100 friend tag `VIP`<br>- Quyền xem màn lịch sử gửi | 1. Tạo scheduled broadcast tag `VIP`.<br>2. Gắn thêm tag `VIP` cho 20 friend.<br>3. Chờ gửi xong.<br>4. Mở màn lịch sử gửi của broadcast đó.<br>5. Xuất CSV kết quả gửi, đếm số dòng. | 100 + 20 friend | Màn lịch sử hiện `120` người gửi · CSV có đúng `120` dòng · khớp phép tính tay `100 + 20` | | Lấp `G2` · `Q2` · Đánh giá spec: Spec ghi rõ · Evidence: ảnh màn lịch sử + file CSV · đối chiếu 3 nguồn |
| TC-FUNC002-01 | UI | FUNC-002 | Tạo scheduled broadcast | Normal | manual | staging | Vừa tạo scheduled broadcast xong, danh sách người nhận CHƯA bị chốt | - Bot có ≥ 50 friend tag `VIP` | 1. Tạo scheduled broadcast tag `VIP`, hẹn gửi sau 1 giờ.<br>2. Bấm lưu.<br>3. Mở lại màn chi tiết broadcast vừa tạo.<br>4. Bỏ tag `VIP` khỏi 10 friend.<br>5. Mở lại màn chi tiết lần nữa. | tag `VIP` ≥ 50 friend | Màn chi tiết **không** hiện danh sách người nhận cố định · số dự kiến ở bước 5 giảm đúng 10 so với bước 3 | | Lấp `G4` · Đánh giá spec: Spec ghi rõ · Evidence: ảnh màn chi tiết 2 thời điểm · regression |
| TC-FUNC002-02 | UI | FUNC-002 | Gửi broadcast theo tag | Abnormal | manual | staging | Bỏ tag toàn bộ friend trước giờ gửi → gửi 0 người, không lỗi | - Bot có 30 friend tag `TEST` | 1. Tạo scheduled broadcast tag `TEST`, hẹn gửi sau 5 phút.<br>2. Bỏ tag `TEST` khỏi cả 30 friend.<br>3. Chờ tới giờ gửi.<br>4. Mở màn lịch sử gửi. | 30 → 0 friend | Broadcast chuyển trạng thái `Đã gửi` · số người gửi = `0` · không hiện thông báo lỗi · log không có bản ghi lỗi | | Lấp `G1` · Đánh giá spec: Spec không ghi (đã hỏi Dev Nguyễn A) · Evidence: ảnh màn lịch sử |
| TC-CONC001-01 | UI | CONC-001 | Gửi broadcast theo tag | Boundary | manual | product | 3 scheduled broadcast cùng tag, cùng giờ gửi — không chồng chéo | - Bot có 500 friend tag `VIP` | 1. Tạo 3 scheduled broadcast tag `VIP`, đặt **cùng một giờ gửi**.<br>2. Chờ tới giờ gửi.<br>3. Mở màn lịch sử gửi của cả 3. | 3 broadcast × 500 friend | Cả 3 đều `Đã gửi` · mỗi cái đúng `500` người · không cái nào timeout/lỗi · friend nhận đúng 3 tin, không trùng lặp | | Lấp `G3` · Đánh giá spec: Spec không ghi (đã hỏi Leader) · Evidence: ảnh 3 màn lịch sử + ảnh LINE 1 máy thật · RULE-08 |

---

## 6. Spec update needed

`Không cần update spec.` — Spec v2.3 (BR-02) đã mô tả đúng hành vi; bug là do code sai, không phải spec thiếu.
