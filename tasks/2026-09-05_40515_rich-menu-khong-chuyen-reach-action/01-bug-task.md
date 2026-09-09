# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40515 — [04-09-2026] [TY-12071] [Info friend] Rich menu không chuyển ở 到達アクション của friend info với ~2-3% friend` |
| Module / Màn hình | `Info friend` (category Redmine) — cụ thể: 到達アクション của friend info + リッチメニュー表示 |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: WSSJ Add DB CS → OEM đăng card trên Slack (ユーザー問い合わせ) — 管理番号 TY-12071
担当: 沖原, WSS管理者
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1788516107700779
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12071

【操作方法に関するお問い合わせフォーム】
【友だち情報の到達アクションでリッチメニュー切替が反映されない事例について】

Khách đang dùng 到達アクション (hành động khi đạt giá trị, các giá trị 1〜5) của friend info「ポイント」(ID 300700・何度でも稼働) để thiết lập hiển thị rich menu có lọc theo tag cửa hàng. Với hầu hết friend thì rich menu chuyển đổi bình thường, nhưng khoảng 2〜3% friend gặp hiện tượng「値は到達しているのにリッチメニューが切り替わらない（元のメニューのまま）」(giá trị đã đạt tới nhưng rich menu không đổi, vẫn giữ menu cũ).

Ví dụ cụ thể:
・Friend: ファンファン（友だちID 41160486）
・Lúc 2026/09/03 17:04:54 friend này quét QR code action「1ポイント付与」(ID 441494) → điểm tăng 0→1 và text trong cùng action đó vẫn được gửi tới
・Nhưng hiển thị「博多_ポイント①」của 到達アクション (giá trị 1) lại không được áp dụng, mục「表示中リッチメニュー」trên màn hình quản trị vẫn là「博多_リッチ」(điều kiện lọc của dòng đó là tag「ゆめタウン博多店」, và friend này có giữ tag đó)
・Khoảng 90 friend khác cùng điều kiện thì chuyển đổi bình thường

Do trong cùng một QR code action còn có「ステップ停止」「ステップ開始」「タグ付与/解除」chạy đồng thời, khách nghi ngờ khả năng xung đột xử lý, hoặc lỗi tạm thời phía LINE API mà không được thử lại (retry).

Các điểm khách muốn được xác nhận:
1. Với friend nêu trên tại thời điểm đó, việc chuyển đổi rich menu của 到達アクション có được thực thi hay không, có còn log lỗi hay không
2. Điều kiện dẫn tới thất bại (xung đột do chạy đồng thời, giới hạn API…) và thiết lập khuyến nghị để tránh
3. Có cách nào tự động áp dụng lại sau cho những friend chưa được phản ánh hay không

## Steps to reproduce

<!-- ⚠️ Redmine #40515 KHÔNG có section "Tái hiện bug" / "再現手順". Không tự suy diễn steps. -->

1.
2.
3.

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine #40515 **không có attachment nào** (`attachments: []`). Bằng chứng duy nhất nằm ở phần mô tả + journal.

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — Redmine không có section "Tái hiện bug", và cũng **chưa có** section "Đánh giá ảnh hưởng" (ticket còn ở status `New`, chưa assign Dev). TCs nên tập trung verify cách fix + regression impact **sau khi Dev bổ sung `03-dev-impact.md`**.

⚠️ Đây là bug **xác suất ~2〜3% friend**, KHÔNG phải lỗi 100% → khi viết / review TC phải tính tới yếu tố **chạy đồng thời (concurrency)** và **retry**, không chỉ happy path.

⚠️ **Môi trường phát hiện chưa xác nhận** — Redmine KHÔNG ghi env. Dấu hiệu gợi ý **Production** (ticket khách hàng thật, `bot_id: 153327`, link dashboard `dashboard.melonglobal.net/css-analytics/?id=T12071`) nhưng chưa được xác nhận trong ticket → tester confirm trước khi dùng.

## Dữ liệu định danh ca lỗi

<!-- Từ description + journal — dùng để dựng env test. -->

| Mục | Giá trị |
|---|---|
| bot_id | `153327` |
| Friend | ファンファン — friend ID / line_user_id `41160486` |
| Friend info | 「ポイント」 ID `300700`, chế độ 何度でも稼働 (chạy được nhiều lần) |
| 到達アクション | giá trị `1〜5`; dòng giá trị `1` = hiển thị richmenu 「博多_ポイント①」 (richmenu ID `738325`), điều kiện lọc = tag 「ゆめタウン博多店」 |
| QR code action | 「1ポイント付与」 ID `441494` |
| Thời điểm lỗi | 2026/09/03 17:04:54 |
| Richmenu thực tế hiển thị | 「博多_リッチ」 (menu cũ, không đổi) |
| Đối chứng | ~90 friend cùng điều kiện chuyển đổi bình thường |
| Action chạy đồng thời trong cùng QR action | 「ステップ停止」・「ステップ開始」・「タグ付与/解除」 |

## Journal / note từ Redmine (nguyên văn)

**Journal #134203 — AI bug detect Lme — 2026-09-04:**

```
Thông tin bổ sung:
bot_id: 153327
line_id: 41160486
Friend này đã quét QR 1ポイント付与 (id 441494) lúc 2026/09/03 (木) 17:04 và được action friend info ポイント (id 300700) cộng 1 point => Nhưng không thấy chạy action của info đó là gắn richmenu 博多_ポイント① (id 738325)

SELECT * FROM `action_lineuser` WHERE `bot_id` = 153327 AND `line_user_id` = 41160486
```

**Journal #134205 — AI bug detect Lme — 2026-09-04:**

```
Comment slack ngày 2026-09-04 19:23:36

WSSサポーターBOT
Chúng tôi sẽ tiến hành xác nhận việc này.
Sau khi xác nhận xong, chúng tôi sẽ liên hệ lại quý khách nên rất mong quý khách đợi thêm một chút ạ.
```
