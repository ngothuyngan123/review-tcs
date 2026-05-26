# 03 — Đánh giá ảnh hưởng từ Dev

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Nguyễn Văn A |
| Commit / Pull Request | PR #1872 — fix(broadcast): refresh tag list at send time |
| Branch | fix/LME-2054-broadcast-tag-refresh |
| Ngày submit đánh giá | 2026-04-22 |

---

## 1. Nguyên nhân

Trong `BroadcastScheduler::enqueueScheduledBroadcast()`, khi scheduled broadcast được đẩy vào queue tại thời điểm tạo, code đang **cache snapshot tag-friend mapping** vào field `broadcast.cached_recipient_ids` để tối ưu performance.

Tại thời điểm send (`BroadcastSender::send()`), code đọc từ `cached_recipient_ids` thay vì query lại `friends_tags` table. Kết quả: friend mới được gắn tag sau thời điểm create không được gửi; đồng thời, 52 friends trong snapshot gốc đã bị remove tag trong khoảng 2 ngày vẫn bị filter bởi 1 double-check pass, nên bị skip với reason `tag_mismatch`.

Vi phạm spec BR-02 (resolve tại send time, không phải create time).

## 2. Cách fix

1. Remove field `broadcast.cached_recipient_ids` khỏi flow scheduled broadcast (vẫn giữ cho immediate broadcast).
2. Trong `BroadcastSender::send()`, luôn query `FriendTagRepository::findFriendsByTag()` tại thời điểm send.
3. Update preview ở create screen: thêm note "Preview count may vary at send time" bên cạnh recipient count.
4. Migration: xóa data cũ trong field `cached_recipient_ids` cho các scheduled broadcast chưa run.

Snippet:

```php
// before (BroadcastSender.php:142)
$recipientIds = $broadcast->cached_recipient_ids;

// after
$recipientIds = $this->tagRepo->findFriendsByTag($broadcast->filter->tagId)
    ->filter(fn($f) => $f->isActive() && !$f->hasOptedOut($broadcast->category))
    ->pluck('id');
```

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `BroadcastScheduler::enqueueScheduledBroadcast()` — BroadcastScheduler.php:87 | Remove logic cache recipient IDs cho scheduled type | Không còn cần cache |
| 2 | `BroadcastSender::send()` — BroadcastSender.php:142 | Switch sang real-time query | Core của fix |
| 3 | `BroadcastCreateController::preview()` — BroadcastController.php:56 | Thêm note "may vary" trong response | UX hint cho user |
| 4 | `BroadcastRepository::findById()` — BroadcastRepository.php:34 | Không còn expose `cached_recipient_ids` | Cleanup field đã deprecate |
| 5 | `Migration 20260422_clear_cached_recipients.php` | New — clear field cho các scheduled broadcast pending | Cleanup data cũ |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | `BroadcastSender::send()` | BroadcastSender.php | Direct | Logic chính được sửa |
| F2 | `BroadcastScheduler::enqueueScheduledBroadcast()` | BroadcastScheduler.php | Direct | Remove cache logic |
| F3 | `BroadcastCreateController::preview()` | BroadcastController.php | Indirect | Thêm note vào response |
| F4 | `FriendTagRepository::findFriendsByTag()` | FriendTagRepository.php | Indirect | Sẽ được gọi thường xuyên hơn (perf) |
| F5 | `BroadcastRepository::findById()` | BroadcastRepository.php | Indirect | Bỏ expose 1 field |

### 4.2. List data bị update khi fix bug

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | `broadcasts.cached_recipient_ids` | MIGRATE (clear to null) | Cho scheduled broadcast có status = pending |
| D2 | `broadcasts` table — read path | UPDATE (no longer reads cached field) | Logic read thay đổi |
| D3 | `broadcast_send_logs` | CREATE | Log record mới có thể khác số recipients so với preview |
| D4 | `friends_tags` — read frequency | — | Frequency tăng tại send time |

### 4.3. List tính năng bị ảnh hưởng

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Scheduled broadcast — send flow | F1, F2, D1, D2 | High |
| T2 | Immediate broadcast — send flow | F1 (shared) | Medium |
| T3 | Broadcast create screen — preview count | F3 | Low (chỉ thêm note) |
| T4 | Broadcast detail screen — recipient list hiển thị | F5, D2 | Medium (bỏ field cũ) |
| T5 | Performance toàn hệ thống khi có nhiều broadcast đồng thời | F4 | Medium (query tăng) |

---

## Leader xác nhận trước khi giao TCs

- [x] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [x] Mục 2 (cách fix) có thể trace về code
- [x] Mục 3 đã check đủ caller
- [x] Mục 4.1 không thiếu function
- [x] Mục 4.2 không thiếu data
- [x] Mục 4.3 cover được cả happy path lẫn edge case
- [x] Đã confirm với Dev: T5 (performance) cần đo bằng load test riêng, TC chức năng chỉ cần smoke
