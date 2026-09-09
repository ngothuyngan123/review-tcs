# 03 — Đánh giá ảnh hưởng từ Dev

> ⚠️ **Redmine #38765 KHÔNG có section "Đánh giá ảnh hưởng phía dev" trong description.** Nội dung dưới đây trích **nguyên văn từ journal của bot `AI LME Fix bug`** (journal #130769 — 2026-08-20, vòng 3, là bản mới nhất; journal #126457 — 2026-07-16 là vòng 1 đã bị thay thế). Đây **không phải** đánh giá do Dev người viết → Tester bắt buộc verify lại trước khi dùng.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | `AI LME Fix bug (Auto-fixbug LME)` — assignee Redmine hiện tại: `Kim Cúc` |
| Commit / Pull Request | `commit d8cbf9c4b7` (vòng 3, 2 file) · vòng 1: `commit 9234b77f8d` · Dashboard: https://dashboard.melonglobal.net/implement-task-small-lme/?id=38765 |
| Branch | `ai_small_38765` (repo `sns-line`, nhánh gốc `release_step_20260623`) |
| Ngày submit đánh giá | `2026-08-20` (vòng 3) — vòng 1: `2026-07-16` |
| Auto-filled | `2026-09-08 by /new-task` |

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại journal #130769 từ Redmine và xác nhận đầy đủ 4 mục (nguyên nhân, cách fix, caller đã check, mục 4.1/4.2/4.3 không sót impact).

### ⚠️ Mâu thuẫn trong chính báo cáo của Dev — phải hỏi lại trước khi test

1. **Mục 2 ghi `Commit d8cbf9c4b7 (chưa push)`** nhưng mục **BRANCH / COMMIT ghi `[đã push]`** cho đúng commit đó → xác nhận với Dev commit đã lên `origin/ai_small_38765` chưa, tránh test nhầm code vòng 1.
2. **Mục 3 vẫn liệt kê `Handler::isQrLandingDomain`** trong khi mục 2 nói hàm này **đã bị thay** bằng `isInvalidLinkDomain` + `invalidLinkDomains` → mục 3 là **bản copy còn sót của vòng 1**, danh sách function không phản ánh code vòng 3.
3. **Mục 4.3 vẫn chỉ ghi 1 tính năng + 1 domain `s.lmes.jp`** trong khi vòng 3 mở rộng ra **3 domain** `s.lmes.jp` / `sl.lmes.jp` / `form.lmes.jp` → **thiếu impact** cho short link (`sl.lmes.jp`) và form (`form.lmes.jp`).
4. **Mục 6 VERIFY chỉ ở mức `lint`** (`php -l`) — không có test chạy thật trên môi trường có domain thật.
5. **Không có đánh giá impact cho việc text đổi theo design BA** (「このリンクは無効です」 → 「お探しのページが見つかりませんでした。」, bỏ nút 「TOPページへ戻る」) dù file `errors/invalid_link.blade.php` bị sửa.

---

## 1. Nguyên nhân

<!-- Nguyên văn journal #130769 mục 1 (giống hệt vòng 1). -->

Trên domain rút gọn/QR (s.lmes.jp), URL không khớp route nào (vd /test) khiến Laravel ném NotFoundHttpException. Bộ xử lý ngoại lệ toàn cục, với người chưa đăng nhập, lại redirect về trang gốc / — chính là màn đăng nhập LME, gây nhầm lẫn cho friend nhận link QR bị hỏng.

## 2. Cách fix

<!-- Nguyên văn journal #130769 mục 2 (vòng 3 — bản mới nhất). -->

Vòng 3 (spec bổ sung của human 20/08): rule hiện trang お探しのページが見つかりませんでした。 áp cho ĐÚNG 3 domain public s.lmes.jp (QR/rút gọn), sl.lmes.jp (short link), form.lmes.jp (form); mọi domain khác kể cả domain quản trị giữ nguyên hành vi cũ (redirect về màn đăng nhập). Thay Handler::isQrLandingDomain (chỉ so 1 host từ URL_OUTSIDE_STEP) bằng isInvalidLinkDomain + invalidLinkDomains: danh sách mặc định 3 host + host suy ra từ URL_OUTSIDE_STEP/URL_OUTSIDE_STEP_V2 cho staging, override toàn bộ bằng env INVALID_LINK_DOMAINS. So khớp host chính xác, không phân biệt hoa thường. Verify: php -l + test 15 case khớp/không khớp domain đều đúng. Commit d8cbf9c4b7 (chưa push).

**Cách fix vòng 1 (2026-07-16, đã bị thay thế — giữ lại để đối chiếu regression):**

Thêm trang lỗi thân thiện errors/invalid_link.blade.php (「このリンクは無効です」) và bổ sung guard trong Exception Handler: khi request thuộc domain QR/rút gọn (host khớp URL_OUTSIDE_STEP) và lỗi thuộc nhóm không tìm thấy (NotFound/ModelNotFound/MethodNotAllowed/404) thì trả trang này với HTTP 404, thay vì redirect về màn đăng nhập. Domain quản trị chính giữ nguyên hành vi cũ.

**Ghi chú vị trí guard (từ mục TỰ REVIEW của Dev):** guard đặt **sau khối JSON** (request ajax/API vẫn trả JSON) và **trước mọi nhánh `redirect(/)`**. Fallback: `URL_OUTSIDE_STEP` rỗng → `false` → giữ hành vi cũ. Guard chỉ chạy khi **chế độ gỡ lỗi TẮT** (`APP_DEBUG=false`).

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

<!-- Nguyên văn danh sách mục 3 của journal #130769. ⚠️ Danh sách này là bản copy của vòng 1 — xem mâu thuẫn #2 ở trên. -->

| # | Function / File | Thay đổi (nếu có) | Lý do |
|---|---|---|---|
| 1 | `Handler::render` — `app/Exceptions/Handler.php` | Thêm guard domain-aware trước mọi nhánh `redirect(/)` | Chặn case not-found trên domain public trước khi rơi vào nhánh redirect về màn đăng nhập |
| 2 | `Handler::isQrLandingDomain` — `app/Exceptions/Handler.php` | ⚠️ Vòng 3 **thay thế** bằng `isInvalidLinkDomain` + `invalidLinkDomains` (mục 3 của Dev chưa cập nhật tên hàm mới) | Vòng 1 chỉ so 1 host từ `URL_OUTSIDE_STEP`; vòng 3 cần khớp danh sách 3 host |
| 3 | `Handler::isNotFoundLikeException` — `app/Exceptions/Handler.php` | Phân loại lỗi thuộc nhóm không tìm thấy (NotFound / ModelNotFound / MethodNotAllowed / 404) | Chỉ áp trang lỗi mới cho nhóm not-found, lỗi khác giữ nguyên |
| 4 | `errors/invalid_link.blade.php` — `resources/views/errors` | View mới; nội dung đổi theo design BA (bỏ dòng text dưới + nút 「TOPページへ戻る」) | Trang báo link lỗi hiển thị cho friend |

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

<!-- Dev chỉ liệt kê "File thay đổi" (2 file), không liệt kê function-level. Bảng dưới giữ nguyên phạm vi Dev kê, tách theo file + function ở mục 3. -->

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | Exception Handler toàn cục (`Handler::render` + guard domain/not-found) | `app/Exceptions/Handler.php` | Direct | Dev kê ở mục "4.1 File thay đổi". Là **điểm vào chung của MỌI exception toàn hệ thống** → phạm vi ảnh hưởng thực tế rộng hơn 1 tính năng QR Landing |
| F2 | View trang báo link lỗi | `resources/views/errors/invalid_link.blade.php` | Direct | File mới; nội dung phải khớp design BA (1 dòng 「お探しのページが見つかりませんでした。」) |

### 4.2. List data bị update khi fix bug

<!-- Nguyên văn: "Không có". -->

| # | Data (table.column / key / collection) | Thao tác | Ghi chú |
|---|---|---|---|
| D1 | — | — | Dev kê **"Không có"**. Không đụng DB, không đụng hot path click-tracking |
| D2 | `URL_OUTSIDE_STEP`, `URL_OUTSIDE_STEP_V2`, `INVALID_LINK_DOMAINS` (biến môi trường) | READ / CONFIG | ⚠️ **Dev KHÔNG kê** — nhưng cách fix vòng 3 đọc trực tiếp 3 env này để dựng danh sách domain. Khai `INVALID_LINK_DOMAINS` sẽ **thay thế toàn bộ** danh sách mặc định → khai thiếu ở môi trường thật là mất tính năng |
| D3 | Cache config (`config:cache`) | INVALIDATE | ⚠️ **Dev KHÔNG kê** — precondition test yêu cầu xoá cache sau khi sửa `APP_DEBUG` / env domain |

### 4.3. List tính năng bị ảnh hưởng (dựa vào 4.1 + 4.2)

<!-- Dev chỉ kê T1. T2/T3 là impact suy trực tiếp từ mục 2 vòng 3 (3 domain) — đánh dấu rõ là Dev CHƯA kê. -->

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | QR Code Action / Landing (FA-017) — URL không hợp lệ trên domain rút gọn `s.lmes.jp` hiện trang báo link lỗi thay vì màn đăng nhập | F1, F2 | **Dev kê: (không ghi mức)** — đánh giá lại: High |
| T2 | Short link `sl.lmes.jp` — mọi URL không khớp route trên domain này đổi từ redirect sang trang lỗi 404 | F1 (mục 2 vòng 3) | ⚠️ **Dev CHƯA kê** — High |
| T3 | Form `form.lmes.jp` — mọi URL không khớp route trên domain này đổi từ redirect sang trang lỗi 404 | F1 (mục 2 vòng 3) | ⚠️ **Dev CHƯA kê** — High |
| T4 | Domain quản trị `step.lme.jp` + mọi domain ngoài danh sách — phải **giữ nguyên** hành vi redirect cũ | F1 | ⚠️ **Dev CHƯA kê thành tính năng riêng** — High (vùng regression chính) |
| T5 | Request ajax/JSON trên domain public — vẫn phải trả JSON như trước fix (guard đặt sau khối JSON) | F1 | ⚠️ **Dev CHƯA kê** — High |
| T6 | Các lỗi KHÔNG thuộc nhóm not-found trên domain public (yêu cầu đăng nhập, lỗi hệ thống, lỗi phiên) — không được đổi thành trang báo link lỗi | F1 | ⚠️ **Dev CHƯA kê** — Medium |

---

## 5. Recover data

✔ Không cần recover data *(nguyên văn Dev)*

## 6. Verify của Dev

| Mục | Nội dung |
|---|---|
| Mức | `lint` |
| Lệnh | `php -l app/Exceptions/Handler.php` → No syntax errors; blade view mới không cần lint runtime. Vòng 3 bổ sung: "test 15 case khớp/không khớp domain đều đúng" |
| Bằng chứng | Guard đặt TRƯỚC mọi nhánh `redirect(/)` trong Handler nên chặn hết case not-found trên domain QR |
| Rủi ro Dev tự nêu | Nếu `URL_OUTSIDE_STEP` không phải `s.lmes.jp` ở một môi trường nào đó thì cần kiểm lại giá trị env |

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng, đủ chi tiết để viết TC verify fix
- [ ] Mục 2 (cách fix) có thể trace về code — **đã xác nhận commit `d8cbf9c4b7` đã push hay chưa** (mâu thuẫn #1)
- [ ] Mục 3 đã check đủ caller — **đã hỏi Dev về tên hàm `isQrLandingDomain` vs `isInvalidLinkDomain`** (mâu thuẫn #2)
- [ ] Mục 4.1 không thiếu function (so với mục 3) — lưu ý `Handler::render` là điểm vào chung toàn hệ thống
- [ ] Mục 4.2 không thiếu data — **bổ sung env `INVALID_LINK_DOMAINS` + cache config** (D2, D3)
- [ ] Mục 4.3 cover được cả happy path lẫn edge case — **bổ sung T2..T6 Dev chưa kê**
- [ ] Nếu có điểm nghi vấn → đã hỏi lại Dev trước khi member viết TC
