# 03 — Đánh giá ảnh hưởng từ Dev

> Auto-fill từ Redmine #36243 journal #118286 (Ngô Thúy Ngần, 2026-05-13 10:56). Nguyên văn trong [_redmine-36243-raw.json](_redmine-36243-raw.json) journal id `118286`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Dev phụ trách | Ngô Thúy Ngần (id 58) |
| Commit / Pull Request | _<chưa có — chưa link trong journal>_ |
| Branch | _<chưa có>_ |
| Ngày submit đánh giá | 2026-05-13 |

---

## 1. Nguyên nhân

Nguyên văn dev (journal #118286): **"liff và mini app đang lỗi"**.

Bổ sung context từ journal #117779 (LINE-side announcement, do Ngọc Ánh forward từ LINE Developers):
- LINE Android version **26.6.0 / 26.6.1** support **edge-to-edge** (từ LINE Android 26.3.0 trở đi).
- Hệ quả: các nút bottom của **LIFF app / LINE Mini App** bị **chồng lên vùng navigation bar** của Android system → tap không phản hồi.
- LINE iOS 15.13.1 / 15.15.1 **không bị ảnh hưởng**.
- LINE Developers thông báo: https://developers.line.biz/ja/news/2026/05/11/liff-outage/

> **Note**: Dev report sơ sài, chưa nói rõ **logic detect device** (Android version range? user-agent?), **vùng nào của button bị che**, và **giải pháp UI cụ thể**. Leader nên hỏi dev trước khi member viết TC.

## 2. Cách fix

Nguyên văn dev (journal #118286): **"check liff login của liff app khi mở trên Android"**.

> **Note**: Câu mô tả mơ hồ. Khả năng cao là:
> - Khi LIFF app mở trên device Android → check trạng thái LIFF login.
> - Nếu chưa login → trigger lại flow login (workaround tránh button bottom bị che).
> - Hoặc: adjust UI (thêm padding bottom / move button lên trên navigation bar).
>
> Cần dev clarify trước khi review TC.

## 3. Đã check và sửa các function sử dụng đến function/data vừa sửa

| # | Function / File | Thay đổi | Lý do |
|---|---|---|---|
| 1 | `resources/views/liff_callback.blade.php` | _<dev chưa describe cụ thể>_ | View handle LIFF callback sau khi user authorize / login |

> **Note**: Dev chỉ list 1 file. Leader hỏi dev:
> - LIFF login flow có chạy qua controller / service nào khác không (vd `LiffController`, `LiffAuthService`)?
> - JS frontend của LIFF có cần sửa không?

---

## 4. Đánh giá ảnh hưởng

### 4.1. List function bị ảnh hưởng

| # | Function / API / Module | File | Mức độ ảnh hưởng | Ghi chú |
|---|---|---|---|---|
| F1 | LIFF callback view | `resources/views/liff_callback.blade.php` | Direct | View render sau khi user tap button add friend qua LIFF |

### 4.2. List data bị update khi fix bug

| # | Data | Thao tác | Ghi chú |
|---|---|---|---|
| — | _Không có_ | — | Dev xác nhận "4.2 không có" trong journal #118286 |

### 4.3. List tính năng bị ảnh hưởng

| # | Tính năng / Màn hình | Suy ra từ | Nguy cơ regression |
|---|---|---|---|
| T1 | Add friend qua **Landing QR Code** (kết bạn qua landing) | F1 | High |
| T2 | Add friend qua **QR Code Action (QRCA)** | F1 (cùng LIFF callback) | High — KH report đúng case này |
| T3 | Add friend qua **LINE Official Account profile page** (button trực tiếp) | F1 (cùng vùng LIFF) | Medium — LINE-side, có thể không thuộc fix LME |

> **Note dev nguyên văn**: "Test các case kết bạn qua landing qrcode" → dev chỉ scope T1. Leader cần xác nhận T2, T3 có cần test không (vì cùng dùng LIFF callback).

---

## Leader xác nhận trước khi giao TCs

- [ ] Mục 1 (nguyên nhân) rõ ràng — **HIỆN TẠI: chưa rõ logic detect device, vùng button bị che, giải pháp UI**
- [ ] Mục 2 (cách fix) có thể trace về code — **HIỆN TẠI: câu mô tả mơ hồ "check liff login"**
- [ ] Mục 3 đã check đủ caller — **HIỆN TẠI: chỉ list 1 file view, có thể thiếu controller / JS**
- [ ] Mục 4.1 không thiếu function — **HIỆN TẠI: chỉ F1, cần verify với dev**
- [x] Mục 4.2 không thiếu data — dev confirm "không có"
- [ ] Mục 4.3 cover happy + edge — **HIỆN TẠI: dev chỉ scope T1, cần xác nhận T2/T3**
- [ ] Câu hỏi nghi vấn cần hỏi lại Dev:
  - LINE Android version range cụ thể nào bị fix (26.6.0/26.6.1 hay tất cả 26.3.0+)?
  - iOS có regression test không?
  - Fix có cover case "Friend đã add rồi mà tap lại button" không?
  - Behavior change trên Android cụ thể (UI move, padding, hay flow redirect)?
  - L Step đã fix bằng cách gì → có thể tham khảo approach?
