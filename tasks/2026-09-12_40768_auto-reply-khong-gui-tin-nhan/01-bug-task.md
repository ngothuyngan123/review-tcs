# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40768 — [09-09-2026] [TY-12099] [Auto reply] Tự động phản hồi không gửi tin nhắn cho 2 friend dù đã set từ khóa` |
| Module / Màn hình | `Auto reply (自動応答)` — màn `自動応答` `/basic/reply` + job xử lý sự kiện tin nhắn đến (`HandlePostbackTask`) |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12099
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788942507587389?thread_ts=1788942507.587389&cid=C0BALS7S73L
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12099

Số quản lý　：TY-12099
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C0CGHJYCT
Địa chỉ ：creative@komeko-mirin.co.jp
Tên LOA　　：無添加米粉とみりん
Phụ trách　　 ：沖原
Công cụ　 ：リンク

**Nội dung liên hệ**

Đã cài đặt từ khóa 「【みりんと私】」 cho tự động phản hồi (自動応答), nhưng friend gửi từ khóa lúc 09/05 10:44 lại không nhận được tin nhắn.

Hiện tại tự động phản hồi đang ở trạng thái OFF, nhưng tại thời điểm 09/05 10:44 được cho biết là đang ở trạng thái ON.

◎Tên LINE của những friend mà tự động phản hồi không hoạt động
- Tomoko Sato
- Hiroe Shinkai

**Bổ sung từ khách (Journal #135449) — danh sách đầy đủ 12 biến thể từ khóa auto reply đã cài:**

`【みりんと私】` · `【みりんとわたし】` · `【みりんとワタシ】` · `【ミリンとワタシ】` · `【ミリンとわたし】` · `【ミリンと私】` · `【味醂とわたし】` · `【味醂とワタシ】` · `【味醂と私】` · `【みりん私】` · `【私とみりん】` · `【わたしとみりん】`

**Bổ sung từ khách (Journal #135451):** Đây là chương trình (キャンペーン) chạy ngày 9/5 (thứ 7), nên hiện tại sau khi chương trình kết thúc mới chuyển về trạng thái OFF. **Ngoài 2 friend nói trên thì auto reply đã phản hồi đúng bình thường** cho các friend khác.

## Steps to reproduce

<!-- Redmine KHÔNG có Section "Tái hiện bug" — đây là ticket khách hàng báo trên production, không có bước tái hiện chủ động. -->

1. *(không có trong Redmine)*

## Expected result

- *(không có trong Redmine)* — Suy từ nội dung khách báo: friend gửi từ khóa `【みりんと私】` khi rule auto reply đang **ON** → friend phải nhận được tin nhắn auto reply đã cấu hình.

## Actual result

- *(không có trong Redmine)* — Suy từ nội dung khách báo: 2 friend (Tomoko Sato, Hiroe Shinkai) gửi từ khóa lúc 09/05 10:44 **không nhận được** tin nhắn auto reply; các friend khác cùng thời điểm vẫn nhận bình thường.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- SnapCrab_NoName_2026-9-9_17-27-16_No-00.png — https://redmine.watermelon.vn/attachments/download/30239/SnapCrab_NoName_2026-9-9_17-27-16_No-00.png
- SnapCrab_NoName_2026-9-9_10-34-20_No-00.png — https://redmine.watermelon.vn/attachments/download/30251/SnapCrab_NoName_2026-9-9_10-34-20_No-00.png
- Screenshot_20260909-105158.png — https://redmine.watermelon.vn/attachments/download/30252/Screenshot_20260909-105158.png
- Screenshot_20260909-105140.png — https://redmine.watermelon.vn/attachments/download/30253/Screenshot_20260909-105140.png

> Ảnh khách gửi (Journal #135451 + #135452): screenshot màn chat của friend **có** nhận auto reply và friend **không** nhận auto reply — dùng làm đối chứng.

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file 03). TCs nên tập trung verify cách fix + regression impact.
- ⚠️ **Lỗi mang tính xác suất, KHÔNG phải 100%** — chỉ 2/N friend bị rớt auto reply cùng thời điểm; các friend khác nhận bình thường. Điều kiện kích hoạt là **race condition về lock DB**: `conversation` của chính friend đó đang bị một giao dịch bulk UPDATE khác giữ X-lock > `innodb_lock_wait_timeout` (50s). → TC phải **dựng được điều kiện lock** mới tái hiện được, không thể test bằng đường happy path thường.
- **Môi trường phát hiện**: Production (LOA `無添加米粉とみりん`).
- **Điểm mâu thuẫn cần lưu ý khi test**: support xác nhận rule đang OFF lúc kiểm tra (Journal #135450), khách khẳng định lúc 09/05 10:44 rule đang ON (Journal #135451) → cần TC đối chứng **rule OFF = không gửi (đúng spec, không phải bug)** vs **rule ON = phải gửi**, để loại trừ nguyên nhân cấu hình.
- **Giả thuyết cạnh tranh cần loại trừ**: từ khóa khách dùng đều dạng `【…】` → nhánh tùy chọn 「【〇〇】のメッセージには反応させない」 (không phản hồi tin dạng ngoặc vuông) có thể là nguyên nhân cấu hình thay vì lock. Phải test cả 2 nhánh bật/tắt.
- **Timezone**: thời điểm lỗi khách báo theo giờ JST (09/05 10:44).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `87494` |
| Friend | `Tomoko Sato — line_user_id: 18056767` · `Hiroe Shinkai — line_user_id: 13976226` |
| Đối tượng cấu hình | Rule auto reply với 12 biến thể từ khóa `【みりんと私】` … `【わたしとみりん】` (hiện trạng thái OFF) |
| Thời điểm lỗi | `2026/09/05 10:44` (JST) |
| Đối chứng | Các friend khác cùng bot, cùng thời điểm, **nhận auto reply bình thường** (khách có gửi screenshot) |

> Cửa sổ lock Dev trace được trong log ngày 09/09: `12:00:29 – 12:01:57` — 3 lần `#checkAutoReply Exception` ở bot `49501`, `109213`, `50104` (khác bot khách báo, nhưng cùng cơ chế).

## Journal / note từ Redmine (nguyên văn)

**Journal #135449 — AI bug detect Lme — 2026-09-09:**

```
Comment slack ngày 2026-09-09 09:33:00

お客様
Cảm ơn phản hồi của quý vị.

Xin gửi thông tin như dưới đây.

◎Từ khóa auto reply：
【みりんと私】 • 【みりんとわたし】 • 【みりんとワタシ】 • 【ミリンとワタシ】 • 【ミリンとわたし】 • 【ミリンと私】 • 【味醂とわたし】 • 【味醂とワタシ】 • 【味醂と私】 • 【みりん私】 • 【私とみりん】 • 【わたしとみりん】

◎Tên LINE mà auto reply không hoạt động：
・Tomoko Sato
・Hiroe Shinkai

Mong quý vị xác nhận giúp.
```

**Journal #135450 — AI bug detect Lme — 2026-09-09:**

```
Comment slack ngày 2026-09-09 10:40:00

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã liên hệ.

Sau khi kiểm tra, cài đặt vận hành auto reply hiện đang ở trạng thái OFF.

Quý khách có thể bật cài đặt này lên ON để kích hoạt auto reply.
```

**Journal #135451 — AI bug detect Lme — 2026-09-09:**

```
Comment slack ngày 2026-09-09 10:54:00

お客様
Như đã trao đổi trước đó, đây là chương trình được thực hiện vào ngày 9/5(土), nên hiện tại sau khi chương trình kết thúc thì đang ở trạng thái tắt (OFF).
Ngoài 2 người nói trên thì auto reply đã phản hồi đúng bình thường.

Xin gửi ảnh chụp màn hình trò chuyện của người có và không có auto reply phản hồi.

Mong quý vị xác nhận giúp.
```

**Journal #135456 — Ngọc Ánh — 2026-09-09:**

```
bot_id: 87494
Tomoko Sato: line_user_id: 18056767
Hiroe Shinkai:  line_user_id:13976226
```
