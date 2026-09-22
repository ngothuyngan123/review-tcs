# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40909 — Lỗi performance chậm khi save template` |
| Module / Màn hình | Message Template (FA-010) — màn soạn/lưu template Text có URL (テキスト登録); endpoint `/ajax/template-v2/save-template`. Liên đới: Template Message qua API mobile (SC-001), URL Analytics (FA-023). |

## Mô tả bug (bản dịch tiếng Việt)

> Description Redmine viết sẵn bằng tiếng Việt (tác giả ticket tự điều tra root cause) — chép nguyên văn. Dòng log JSON đầu bài rất dài, phần payload cắt bớt và giữ nguyên phần định danh.

Log production ghi nhận 1 request lưu template mất **246 giây**:

```
[2026-09-13 14:24:46] production.INFO: RequestTime1: 246s --> userId: 22658 ---> botId: 41216
{"url":"https://step.lme.jp/ajax/template-v2/save-template","method":"POST","data":{"data":"{\"type\":\"text\",
\"message_button\":{},\"message_media\":{},\"message_stamp\":{},\"message_location\":{},
\"message_text\":{\"content\":\"こんにちは、エクシアホワイトニング新小岩です。 …
```

**Nguyên nhân (tác giả ticket nêu)**

1. **Dedupe không bao giờ khớp → mỗi lần save nhân đôi số bản ghi**

   `TemplateV2Service.php:821` chống trùng bằng cột `url`:

   ```php
   $templateUrlRedirect = TemplateUrlRedirect::query()
       ->where('template_id', $templateId)->where('bot_id', getBotId())
       ->where('url', $itemUrl->url)->first();
   ```

   Nhưng cột đó là `varchar(255)` — migration `2025_09_30_152713:17` — trong khi URL thực tế của bot này dài **769 ký tự** (link HotPepper kèm utm/yclid/gclid). Vì `config/database.php:53` đặt `'strict' => false`, MySQL cắt âm thầm xuống 255 ký tự khi ghi. Lần save sau so sánh URL đầy đủ 769 ký tự với giá trị đã bị cắt → không khớp → nhảy vào nhánh `create()` thay vì `update()`.

2. **Mỗi bản ghi trùng lại gọi HTTP ra ngoài — kể cả khi đã có cache**

   `TemplateV2Service.php:746` gọi `getMetadataContent()` vô điều kiện, ngay cả khi `$urlById->metadata` đã có sẵn (đoạn 731-738 ngay phía trên vừa mới kiểm tra cache xong rồi bỏ qua kết quả):

   ```php
   if ($urlById) {
       $idUrl = $urlById->id;
       $existUrl = Url::query()->find($idUrl);
       $metadataUrl = getMetadataContent($itemUrl->url);   // ← luôn fetch lại
   ```

   Mỗi lần gọi = 2 lượt curl blocking tới host ngoài (`Metadata.php:104,113`): 1 lượt lấy header (timeout 10s) + 1 lượt tải HTML (timeout 60s), không cache, không retry-limit.

   → Request 246s đã bắn **374 HTTP request** tới `beauty.hotpepper.jp` cho cùng một URL. Trường hợp xấu nhất 1 phần tử có thể treo 70s.

3. **Log khuếch đại thêm**

   `TemplateV2Controller.php:518,525` dump nguyên payload 2 lần (311KB × 2), cộng `Log::debug($itemUrl)` cho từng phần tử trong vòng lặp (`:695`). File log ngày 13/09 nặng **5.4GB** — riêng cửa sổ 21 phút quanh sự cố đã là 117MB. Đây là chi phí I/O phụ, không phải nguyên nhân chính, nhưng khiến mọi thứ tệ hơn và làm log gần như không dùng được.

**Đề xuất sửa (theo thứ tự ưu tiên — tác giả ticket nêu)**

1. **Chặn nhân đôi**: đổi `template_url_redirect.url` sang TEXT, hoặc tốt hơn — bỏ hẳn điều kiện `where('url', ...)`, dedupe theo `(template_id, url_id)` vốn đã chuẩn xác (`url_id` luôn đúng). Nên thêm unique index `(template_id, url_id)`.
2. **Dọn dữ liệu rác**: chạy command xoá bản ghi trùng `(template_id, url_id)` giữ lại bản mới nhất — nếu không, template của bot 41216 lần save kế tiếp sẽ mất ~500s và các bot khác cũng đang tích tụ âm thầm.
3. **Bỏ fetch thừa**: ở `:746` và `:769`, chỉ gọi `getMetadataContent()` khi metadata rỗng; gộp/memoize theo URL trong phạm vi 1 request.
4. **Giảm log**: bỏ 2 dòng dump payload ở controller và `Log::debug($itemUrl)` trong vòng lặp, hoặc hạ xuống level chỉ bật khi debug.

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — ticket là báo cáo điều tra performance từ log production. -->

1. `<Redmine không ghi — xem "Ghi chú thêm của Leader">`

## Expected result

- `<Redmine không ghi expected tường minh — chỉ có "Đề xuất sửa">`

## Actual result

- 1 request `POST /ajax/template-v2/save-template` mất **246 giây** (bot 41216, 2026-09-13 14:24:46 production).
- Mỗi lần lưu lại template sinh thêm bản ghi `template_url_redirect` thay vì update bản cũ → số bản ghi nhân đôi liên tục.
- Request 246s bắn **374 HTTP request** tới `beauty.hotpepper.jp` cho cùng 1 URL.
- File log ngày 13/09 nặng **5.4GB** (117MB riêng cửa sổ 21 phút quanh sự cố).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log production dán **trong description** (không có file attachment trên Redmine).

## Ghi chú thêm của Leader

- **Môi trường phát hiện: Production** (`step.lme.jp`) — bug phát hiện qua log `production.INFO`, KHÔNG tái hiện trên dev/staging.
- ⚠️ **Bug không có steps tái hiện trong Redmine** — ticket là báo cáo điều tra performance, root cause đã được tác giả ticket + Dev confirm bằng code/schema (xem file 03). TCs nên tập trung verify **cách fix + regression impact**, và phải **tự dựng lại điều kiện tái hiện**: template Text chứa URL **dài > 255 ký tự**, lưu lại nhiều lần rồi đếm số bản ghi `template_url_redirect`.
- Điều kiện tiên quyết để thấy bug: URL dài vượt `varchar(255)` + DB đặt `strict => false` (cắt chuỗi âm thầm, không báo lỗi). URL ngắn (≤ 255 ký tự) **KHÔNG** tái hiện được.
- Tần suất: **100%** với template có URL dài — mỗi lần lưu lại đều nhân thêm bản ghi (tích luỹ, càng lưu càng chậm).
- ⚠️ Fix có **migration + command dọn dữ liệu** → cần test cả 2 thao tác vận hành (ALTER khoá bảng, chạy giờ thấp điểm) chứ không chỉ test màn hình.
- ⚠️ Dev ghi nhận **rủi ro còn lại**: cột `url.url` là `varchar(500)` — URL dài hơn 500 ký tự vẫn có thể trượt khi tra bảng `url` và sinh `url_id` mới mỗi lần lưu; khi đó dedupe theo `url_id` **vẫn chưa đủ**. Đã thêm log cảnh báo để xác nhận trên môi trường thật.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `41216` (nặng nhất trong ticket) |
| userId | `22658` |
| Đối tượng cấu hình | Template Text chứa URL HotPepper (`beauty.hotpepper.jp`) kèm `utm/yclid/gclid` — **dài 769 ký tự** |
| Endpoint | `POST https://step.lme.jp/ajax/template-v2/save-template` (production) |
| Thời điểm lỗi | `2026-09-13 14:24:46` (RequestTime1: 246s) |
| Đối chứng | Template có URL **≤ 255 ký tự** → dedupe khớp, lưu bình thường |

## Journal / note từ Redmine (nguyên văn)

- **Journal #136301 — AI LME Fix bug — 2026-09-14**: báo cáo AI AUTO-FIXBUG (đã fix xong, chuyển test). Đây chính là **Section "Đánh giá ảnh hưởng phía dev"** → đã chép nguyên văn sang [03-dev-impact.md](03-dev-impact.md), không lặp lại ở đây.
