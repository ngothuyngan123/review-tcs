# 01 — Bug Task từ khách hàng

> ⚠️ **Đây KHÔNG phải ticket Bug** — Redmine #39641 là **Tracker = Feature** (tính năng mới), status `New`, done_ratio 94%.
> Các section "Steps to reproduce" / "Expected result" / "Actual result" để trống vì ticket không có phần "Tái hiện bug".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39641 — [API] API Phase 1 liên kết ngoài của LME` |
| Module / Màn hình | Redmine **không set category**. Suy từ nội dung ticket + snapshot Studio (file 04): **Public API `/v1` của LME (Phase 1)** + màn quản trị API key 「API連携」 (SCR-01 danh sách / SCR-02 phát hành / SCR-03 kết quả / SCR-04 xoá / SCR-05 lịch sử thao tác) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Description Redmine vốn đã là tiếng Việt → chép NGUYÊN VĂN, không dịch lại, không tóm tắt. -->

```
Branch base: release-product
Api viết trong package controller
update repositories: thêm package và config connect vào db chính để update
Nội dung chi tiết đọc ở file đính kèm: api-detail-spec-proposal_vi (7).html

======================================================
*** Tìm trong bảng access_key_api where theo secret_key, check nếu ko thỏa mãn 1 trong các điều kiện thì không được access api:
- role_access: Nếu read chỉ được access api read
- expired_date: >= now() hoặc NULL (không giới hạn)
- status: 1 (enable)
```

## Steps to reproduce

<!-- Redmine #39641 KHÔNG có section "Tái hiện bug" (ticket Feature). -->

## Expected result

<!-- Không có. Kết quả mong đợi nằm trong spec đính kèm `api-detail-spec-proposal_vi.html`, không ở description. -->

## Actual result

<!-- Không có. -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response
- [x] Có **file spec đính kèm** (6 file — 5 bản HTML spec + 1 Postman collection)

| # | Filename | Size | Link |
|---|---|---|---|
| 1 | `api-detail-spec-proposal_vi (7).html` | 63.087 B | https://redmine.watermelon.vn/attachments/download/29045/api-detail-spec-proposal_vi%20(7).html |
| 2 | `LME Public API.postman_collection.json` | 7.579 B | https://redmine.watermelon.vn/attachments/download/29219/LME%20Public%20API.postman_collection.json |
| 3 | `api-detail-spec-proposal_vi.html` | 65.234 B | https://redmine.watermelon.vn/attachments/download/29727/api-detail-spec-proposal_vi.html |
| 4 | `api-detail-spec-proposal_vi.html` | 66.782 B | https://redmine.watermelon.vn/attachments/download/29927/api-detail-spec-proposal_vi.html |
| 5 | `api-detail-spec-proposal_vi.html` | 60.812 B | https://redmine.watermelon.vn/attachments/download/30313/api-detail-spec-proposal_vi.html |
| 6 | **`api-detail-spec-proposal_vi.html` (MỚI NHẤT)** | 58.487 B | https://redmine.watermelon.vn/attachments/download/30325/api-detail-spec-proposal_vi.html |

⚠️ **5 bản spec cùng tên, khác kích thước** — description chỉ trỏ tới bản #1 `api-detail-spec-proposal_vi (7).html` (upload sớm nhất). Bản #6 là bản mới nhất (attachment id 30325). **Phải confirm với Dev/PM bản nào là bản chốt** trước khi viết/review TC, vì expected result phụ thuộc hoàn toàn vào spec này.

## Ghi chú thêm của Leader

- **Loại ticket**: Feature (tính năng mới), **không phải bug** → TC là **TC chức năng mới cho public API**, không phải TC verify fix + regression. Quan điểm test phải bám spec đính kèm, không bám "cách fix".
- **Ticket cha**: #40041 (API key gốc `lme_live_sk_<32hex>`, cấp theo bot — theo spec đính kèm).
- **Môi trường / branch** (từ Journal #130732): branch `feature/docs-api`, server tham chiếu `http://lme6.watermeru.com/`. Branch base ghi trong description là `release-product`.
- **Rate limit đã chốt** (từ Journal #134147, ngày 2026-09-04): **300 req/phút cho GET, 60 req/phút cho POST**, tính **theo bot**, không tính theo từng key.
- ⚠️ **Mâu thuẫn tầng tính quota cần chốt**: Journal #134147 ghi rate limit tính **theo bot**; trong khi requirement `SESSION-216-E644012` trên Studio (file 04) ghi rate limit **theo `api_key_id`**. Hai cách hiểu này cho kết quả test khác nhau (2 key cùng bot: dùng chung quota hay mỗi key 1 quota). **Phải chốt với Dev trước khi chạy TC rate limit.**
- ⚠️ **Mâu thuẫn tên bảng cần chốt**: description ghi bảng `access_key_api` với các cột `secret_key` / `role_access` / `expired_date` / `status`; spec đính kèm + toàn bộ TC trên Studio dùng bảng `api_keys` với `key_lookup_hash` / `expires_at` / `is_deleted`. Description có vẻ là ghi chú sớm, đã bị spec sau ghi đè — **cần Dev xác nhận schema thực tế**.
- ⚠️ **Cơ chế xác thực đã bị đảo ngược giữa chừng**: requirement `SESSION-216-E644036` (2026-08-25) chốt HMAC 3-header (`X-LME-Channel-Id` / `X-LME-Timestamp` / `X-LME-Signature`); nhưng ghi chú trong TC `NEW-551` nói phương án 3-header **"đã bị đảo ngược ngày 04/09"**, quay về 1 header `X-LME-API-KEY`. **Phải xác nhận cơ chế cuối cùng** — hiện Studio còn TC của cả 2 phương án.
- **Không có ca lỗi cụ thể** (ticket Feature) → đã bỏ section "Dữ liệu định danh ca lỗi".

## Journal / note từ Redmine (nguyên văn)

**Journal #130732 — Văn Đức Nguyễn — 2026-08-20:**

```
branch: feature/docs-api
server: http://lme6.watermeru.com/
```

**Journal #134147 — Thanh Duy Nguyen — 2026-09-04:**

```
Đề xuất limit rate:
300/phút cho endpoint GET, 60/phút cho endpoint POST
Limit sẽ tính theo bot, ko tính theo từng key
```
