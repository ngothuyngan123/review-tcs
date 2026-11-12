# Checklist review TC — task nâng version PHP / framework

> **Dùng bởi `/review-tc`** (BƯỚC 1 mục 5) — **chỉ áp khi task là nâng version PHP / Laravel / thư viện nền** (diff chạm `composer.json`/`composer.lock`, đổi version PHP·Laravel, hoặc ticket ghi "nâng cấp"/"upgrade"/"PHP 8"/"Laravel 1x"). Task bug thường KHÔNG áp file này.
>
> Đây là **trục quét BỔ SUNG** cho BƯỚC 2 (coverage) + BƯỚC 3 (quan điểm) + BƯỚC 3a (phạm vi màn), KHÔNG thay thế. Mỗi dòng dưới đây = 1 câu hỏi "bộ TC có cover điểm này không"; thiếu → `GAP`/`RISK` ở §1·§2 hoặc issue §5 theo severity ghi trong bảng.
>
> Nền tảng: **RULE-08 — không kết luận từ dev/staging**. Toàn bộ checklist này mặc định đòi **chạy thật trên server mới (prd/QA PHP 8.5)**; TC chỉ chạy dev/local = `RISK`, chưa xác nhận.

## 0. Ba surface bắt buộc mỗi tính năng (quét ở BƯỚC 3a)

Mỗi tính năng admin phải được test trên **3 mặt tiếp xúc**, thiếu mặt nào = ứng viên `GAP`:

| Surface | Nội dung | Cột `Surface` §7 |
|---|---|---|
| WEB admin | UI quản trị trên browser | `web` |
| APP LME (mục B) | app mobile quản trị | `mobile-app` |
| Phía LINE user / LIFF (mục C) | bạn bè thao tác từ app LINE / trang khách | `line-friend` |

**Thao tác chuẩn mỗi màn** (quét từng cái): folder (tạo/sửa/xóa) · list · tạo mới · edit · copy · xóa · khôi phục · preview · download/export CSV.

**Trục dùng chung phải quét kèm:**
- **Media**: upload/download image·video·audio·PDF (Dropbox) — FA-001,004,005,008,009,010,014,015 + tab friend info.
- **Tích hợp ngoài**: LINE API/Platform (QR, kết bạn, rich menu, webhook) · Stripe/UnivaPay · Google Spreadsheet/Calendar · Firebase/WebPush/Chatwork.
- **Mail**: verify đăng ký · reset pass · 2FA OTP · mail chuyển khoản — check font / tiêu đề / người gửi / **domain mới**.
- **Background job**: gửi tin (broadcast/step/remind) · bill job · sync ES · backup · refresh token LOA.
- **Socket realtime** chat 1:1; **favicon/icon**; **domain URL nhất quán** trên server mới.

## A. ĐIỂM NÓNG PHP 8 — dễ sai âm thầm (ưu tiên CAO, dễ lọt nhất)

| # | Điểm nóng | Ảnh hưởng (tính năng) | Cách test / Lưu ý | Severity nếu thiếu TC |
|---|---|---|---|---|
| A1 | **Thứ tự sort — PHP8 sort thành STABLE** (phần tử bằng nhau giữ thứ tự chèn) | Mọi danh sách: friend list, tag, template, folder, kết quả filter, list booking/broadcast/step | So thứ tự hiển thị **y hệt bản cũ**; soi kỹ chỗ có phần tử bằng khoá sort | `[MAJOR]` |
| A2 | **Ngày giờ & serialize** (T5, T6, trait `LegacyDateSerialization` S-3) | API/JSON mobile, `$dates`, cache TTL, `Carbon::diffIn*` (mới trả **SIGNED**), trial/hết hạn, remind, đặt lịch, lịch sử | Format ngày trong JSON/API giống cũ; timezone **JST** không lệch; `diffIn*` đúng dấu + đúng số | `[MAJOR]` (bill/hết hạn → `[BLOCKER]`) |
| A3 | **Tiền / số thực** (decimal, F-11) | Bill, thuế, 見積書/領収書, UnivaPay, Stripe | **Sai 1 yên = BLOCKER**; `number_format`/`round`; PHP8 cấm ngầm `float→int` | `[BLOCKER]` |
| A4 | **Null & undefined key** — PHP8 nâng warning → `TypeError`/lỗi | Nhánh abnormal / data rỗng ở mọi màn | Test input rỗng/null/thiếu field; **không nổ 500** trên bản mới | `[MAJOR]` |
| A5 | **Encoding / escape HTML** — `htmlspecialchars` PHP8.1 default `ENT_QUOTES` + UTF-8 | Tiếng Nhật, emoji, ký tự đặc biệt trên màn + mail + CSV + tin LINE | Không mojibake, không escape sai (`&quot;` `&#039;`) | `[MAJOR]` |
| A6 | **Type juggling `==`** (PHP8 đổi: `'0'==0`, `''==0` …) | Điều kiện filter / rẽ nhánh | Filter + nhánh logic cho kết quả **giống cũ** | `[MAJOR]` |

## B. THƯ VIỆN NÂNG VERSION — map vào tính năng (ưu tiên CAO)

| Lib (task) | Tính năng phải regression | Điểm so khớp / Lưu ý |
|---|---|---|
| **LINE SDK v12** (T16–T18, gateway S-8) | FA-001,003,007,008,009,010,022; rich menu FA-004; backup đăng ký rich menu FA-033 | Mọi loại tin gửi đi (text/image/video/audio/sticker/flex/location) — **so JSON body với mốc S-9**; webhook nhận; chat realtime |
| **Intervention Image v3** (T15) | FA-001,004,005,010,015 (media) | Resize 1040px, thumbnail video, QR png (`makeQrPng` S-4) — **kích thước/chất lượng/EXIF orientation giống cũ** |
| **Stripe bản mới** (T11, F-7) | FA-026, 031, 034 | API version + webhook endpoint **ĐỔI lúc deploy**; mua/subscription/hủy/đổi thẻ/receipt; webhook Stripe khớp endpoint mới |
| **UnivaPay** | FA-026, 031 + auto bill jobs | Tạo STK chuyển khoản, auto-charge, mail chuyển khoản |
| **Mail + Web push** (T12) | FA-006, 036, 037, 039, 040 | Verify/reset/2FA/bill mail: nội dung, tiêu đề, người gửi, font; PC push (VAPID key) |
| **Google / Excel / CSV** (T13) | FA-011, 017, 019, 020, 014 | Sync Google Sheet/Calendar; import/export CSV (**encoding + thứ tự cột + ngày**) |
| **Collective → HTML thuần** (T7, F-9) | Các màn form cũ dùng Laravel Collective | HTML + tham số form **y hệt** (name field, hidden, action) |

## C. AUTH / SESSION / MÃ HOÁ (T10) — rủi ro "mất dữ liệu ngầm"

| Mục | Rủi ro | Lưu ý | Severity |
|---|---|---|---|
| **APP_KEY / encryption** | Data mã hoá cũ trong DB (`channel_access_token`, payment token, Google token) phải **GIẢI MÃ được** trên bản mới | Lệch → bot mất kết nối LINE / thanh toán fail hàng loạt → **TEST NGAY sau deploy** | `[BLOCKER]` |
| **bcrypt 10 vòng, không rehash** (S-5) | Password cũ phải login lại được | Không đổi thuật toán/vòng hash | `[BLOCKER]` |
| **F-12: session cũ bị logout sau deploy** | **ĐỔI CHỦ ĐỘNG — KHÔNG phải bug** | Chỉ test: login lại OK + không mất data | — |
| **2FA / forgot / reset password** | Super Admin **LUÔN** bắt buộc 2FA | Verify OTP mail, reset pass flow | `[MAJOR]` |

## Cách dùng trong report

- Điểm A1–A6 / lib B / auth C khớp màn đang review mà **không có TC** → 1 dòng `§2` (mã `Q<x>`), severity theo bảng; nếu làm mất chuẩn đánh giá cả impact → đẩy lên `§1` dạng `RISK`.
- Mọi điểm chỉ chạy dev/local (chưa prd) → `§5 [MAJOR] RULE-08`, và hạ kết luận "ĐỦ" ở §1 xuống `RISK`.
- 3 surface (mục 0) thiếu mặt nào cho tính năng dùng chung → `GAP` ở §1 như quy tắc 4 hướng đọc của BƯỚC 3a.
