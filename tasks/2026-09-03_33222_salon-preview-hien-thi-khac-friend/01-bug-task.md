# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#33222 — [Salon] Màn preview đang hiển thị khác với bên friend` |
| Redmine URL | https://redmine.watermelon.vn/issues/33222 |
| Auto-filled | `2026-09-03 by /new-task` |
| Ngày báo cáo | `2025-12-19` |
| Khách hàng / PM báo | `Đỗ Quyên` |
| Module / Màn hình | `Salon` (category Redmine) — màn preview trang đặt lịch salon |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (description không ghi env) |
| Status Redmine | `Fix done - Đợi test` · Tracker `Bug tự detect` · Assignee `Ngô Thúy Ngần` |

## Mô tả bug (nguyên văn từ khách hàng)

```
Preview: đang ko hiển thị lịch lv các ngày từ 19/12 
Friend: hiển thị được lịch lv  
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguyên văn journal #133918 — Đỗ Quyên, 2026-09-03T08:43:48Z -->

```
Cách tái hiện: 

***Bug 1: 
1. setting filter stafF: chỉ hiển thị staff với friend thỏa mãn điều kiện 
2. setting lịch lv cho staff 
3. preview => chọn staff => ko hiển thị được lịch lv do preview ko có friend nên ko thỏa mãn filter 

***Bug 2: 
1. setting staff 1 ko thực hiện course A 
2. preview => chọn course A => vẫn đang hiển thị staff 1
Expect: ko hiển thị staff 1
```

## Expected result

- **Bug 1**: màn preview hiển thị được lịch làm việc của staff (giống bên friend thỏa điều kiện filter).
- **Bug 2**: `ko hiển thị staff 1` — staff không phụ trách course A thì không được xuất hiện khi chọn course A ở preview.

## Actual result

- **Bug 1**: preview không hiển thị lịch làm việc (các ngày từ 19/12), trong khi bên friend hiển thị được.
- **Bug 2**: preview vẫn hiển thị staff 1 dù staff 1 không thực hiện course A.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- https://redmine.watermelon.vn/attachments/download/22196/19-12-2025-01-54-27.png (Đỗ Quyên, 2025-12-19)

## Ghi chú thêm của Leader

- ⚠️ Bug được báo **2025-12-19**, steps tái hiện chỉ được bổ sung **2026-09-03** (sau khi AI đã fix ngày 2026-08-24). Cần đối chiếu lại: bộ TC trên Studio sinh ngày 2026-08-24 **chưa có** steps tái hiện này làm input.
- ⚠️ Ticket có **2 bug** trong 1 ticket (Bug 1 = lịch làm việc trống do filter bạn bè; Bug 2 = staff không phụ trách course vẫn hiện). Coverage phải cover **cả hai**.
- Fix do **AI Auto-fixbug** thực hiện (journal #132590, 2026-08-24), branch `ai_fixbug_33222` (repo `sns-line`, commit `bcc9733e24`, base `release_step_20260805`).
- ⚠️ AI ghi rõ **chưa verify được bằng data thật** (DB dev không kết nối được: `host.docker.internal:3306` bị từ chối) → toàn bộ kết luận fix dựa trên đọc code, chưa chạy thực tế.
