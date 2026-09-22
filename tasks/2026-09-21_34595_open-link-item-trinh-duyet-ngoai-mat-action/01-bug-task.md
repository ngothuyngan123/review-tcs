# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#34595 — Open link item bằng trình duyệt ngoài thì không send được action open link` |
| Module / Màn hình | Single Product / Sales (FA-026) — link sản phẩm (item) mở bằng **trình duyệt ngoài**; liên đới Message Template (FA-010) nút card/carousel + vùng ảnh image map đặt hành động "Mở link", và Action Settings (SC-004) |

## Mô tả bug (bản dịch tiếng Việt)

⚠️ **Description của Redmine #34595 TRỐNG** — ticket thuộc tracker `Bug tự detect`, nội dung bug chỉ nằm ở tiêu đề và được làm rõ dần qua các journal của AI auto-fixbug.

Nội dung bug theo tiêu đề + phân tích root cause của Dev:

> Khi link sản phẩm (item / sale) được mở bằng **trình duyệt ngoài** (ngoài ứng dụng LINE), hành động "Mở link" (action open link) gắn cho link đó **không được gửi**.

Cơ chế (theo journal #137231 — bản fix cuối): luồng mở ngoài LINE chạy vào `LiffController::liffAppCallback` nhánh `product_id`. Nhánh này chỉ dựng lại link LIFF rồi hiện trang "mở bằng ứng dụng LINE" (PC: trang mã QR) — **không nhận diện khách**, nên không lấy được `u_code`. Trong khi đó màn chi tiết sản phẩm **chỉ gửi hành động "khi mở trang" khi URL có `u_code`** → hành động không bao giờ được gửi. Đối chứng: nhánh biểu mẫu (`unique_key`) trong cùng hàm có bước nhận diện khách nên **biểu mẫu mở ngoài trình duyệt vẫn chạy đúng**.

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — description trống. Các bước dưới đây là SUY RA từ journal Dev, tester phải verify lại trước khi dùng. -->

1. Bot có khai channel **LINE Login**.
2. Tạo template (nút card/carousel hoặc vùng ảnh image map) đặt hành động **"Mở link"** trỏ tới **trang sản phẩm / item nội bộ của LME**, có **gắn thêm hành động LME** (action open link).
3. Gửi template cho friend, friend tap link và chọn **mở bằng trình duyệt ngoài** (ngoài app LINE) — thử cả **PC** và **điện thoại**.
4. Kiểm tra hành động gắn cho link có được gửi hay không.

## Expected result

- Hành động (action) gắn cho link "Mở link → sản phẩm/item" **vẫn được gửi** cho khách, kể cả khi link mở ngoài ứng dụng LINE.

## Actual result

- Hành động **không được gửi**. Trang sản phẩm mở ra thiếu `u_code` nên `SalesManagementV2Controller::orderDetail` bỏ qua bước gửi action.
- Đối chứng: cùng cấu hình nhưng link **biểu mẫu (Form)** thì hành động **vẫn chạy** → khẳng định thiếu sót nằm ở nhánh `product_id`.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #34595 KHÔNG có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — description trống, không có Steps/Expected/Actual do khách/QA viết. Root cause do AI auto-fixbug suy từ code và **human xác nhận** ở 2 mốc (2026-08-27 và 2026-09-19). TCs nên tập trung verify **cách fix + regression impact**.
- ⚠️ **Ticket đã qua 4 lượt AI auto-fixbug, hướng fix ĐỔI HẲN giữa lượt 1 và lượt 2** — xem mục "Lịch sử branch" ở `03-dev-impact.md`. Bản fix **có hiệu lực** là journal **#137231** (commit `d552e8292b`, chỉ sửa `LiffController.php`). Bản fix lượt 1 (sửa `TemplateService.php`, gắn/bỏ `openExternalBrowser=1`) **đã bị revert**.
- ⚠️ **31 TC trên Studio task #248 được tạo `2026-08-27`** — tức là theo **bản fix lượt 1 đã bị revert** (template button / image map / `openExternalBrowser`). Bản fix cuối nằm ở nhánh `product_id` của `LiffController`. **Bộ TC hiện có nhiều khả năng lệch phạm vi so với code thật sẽ deploy** → đây là điểm phải soi kỹ nhất khi `/review-tc`.
- **Điều kiện tiên quyết bắt buộc để fix "ăn"**: bot phải khai **channel LINE Login**, và trình duyệt phải **còn cookie access token LINE Login**. Cookie này **chỉ do luồng BIỂU MẪU ghi ra** (`LiffController` dòng 1028, **TTL 360 phút = 6 giờ**). Browser chưa từng đăng nhập qua biểu mẫu trong 6h → cookie rỗng → rơi về hành vi cũ, **action VẪN không gửi**.
- **Phạm vi CHƯA fix (Dev tự khai, cố ý để ngoài ticket)**:
  - Gửi tin **qua job** (broadcast / step / remind — `linect-service MessageBuilder`) còn nguyên pattern cũ → tin tự động vẫn mất hành động. Cần task riêng.
  - Các nhánh **đặt lịch** (booking event / lesson calendar) trong cùng hàm "có thể thiếu y hệt", cố ý không gộp.
  - Chưa có đường khởi tạo LINE Login (redirect authorize + xử lý code) → cần PM/BA + đăng ký `redirect_uri`.
- **Mức verify của Dev chỉ tới `lint`** — không kết nối được DB dev, không gửi được tin LINE trong container → **chưa hề tái hiện / chưa hề chạy thật**. Toàn bộ gánh nặng xác minh dồn cho tester.

## Journal / note từ Redmine (nguyên văn)

**Journal #132272 — Thanh Phương — 2026-08-21:**

```
SpecImprove #34533
```

**Journal #137183 — Kieu Son Tung — 2026-09-19:**

```
branch gốc: release_step_20260827
```

<!--
4 journal còn lại (#133240, #137222, #137225, #137231) là báo cáo AI auto-fixbug — nội dung đã được chép
nguyên văn sang `03-dev-impact.md` (mục 1/2/3/4 + Lịch sử branch), không lặp lại ở đây để tránh trùng.
Nguồn gốc đầy đủ: https://redmine.watermelon.vn/issues/34595
-->
