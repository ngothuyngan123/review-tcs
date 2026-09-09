# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40151 — [25-08-2026] [TY-11973] [Admin] Copy code copy dữ liệu không hiển thị dù đã nhấn cấp lại` |
| Redmine URL | https://redmine.watermelon.vn/issues/40151 |
| Auto-filled | `2026-08-25 by /new-task` |
| Ngày báo cáo | `2026-08-25` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn gốc: OEM tạo task trên Slack — ユーザー問い合わせ, 管理番号 **TY-11973**, phụ trách 沖原) |
| Module / Màn hình | `Admin` (Redmine category) — màn **Sao chép dữ liệu / データコピー (backup)** |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — Redmine không ghi env>`. Là inquiry của khách hàng thật (アドレス info@workingpleasure.net, LOA名 RVパークDEMO) nên nhiều khả năng **Production**. Tester confirm lại. |

**Trạng thái Redmine hiện tại:** `Fix done - Đợi test` · Assignee: `Hạnh Nguyễn` · Commit Date: `2026-08-25`

## Mô tả bug (nguyên văn từ khách hàng)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-11973
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1787628439303299
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T11973

Mã quản lý　：TY-11973
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BSK56H7S8
Địa chỉ ：info@workingpleasure.net
Tên LOA　　：RVパークDEMO
Phụ trách　　 ：沖原
Công cụ　 ：リンク
Nội dung yêu cầu
Tôi thấy có ghi rằng ngay cả gói miễn phí cũng lấy được copy code để copy dữ liệu, nhưng copy code lại không hiển thị. Dù nhấn nút cấp lại copy code thì ô copy code vẫn trống.

---
h3. 原文 (JP)
<pre>管理No　：TY-11973
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BSK56H7S8
アドレス ：info@workingpleasure.net
LOA名　　：RVパークDEMO
担当　　 ：沖原
ツール　 ：リンク
問い合わせ内容
フリープランでもデータコピーのコピーコードを取得できるとの記載を拝見しましたが、コピーコードが表示がされません。コピーコードの再発行ボタンを押してもコピーコード欄は空欄のままです。</pre>

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

> ⚠️ Redmine **không có** section "Tái hiện bug" / 再現手順. Các bước dưới đây **suy ra từ nội dung inquiry của khách hàng** (không phải Dev/QA viết) — tester verify lại trước khi dùng.

1. Đăng nhập admin bằng tài khoản có bot thuộc **gói miễn phí (フリープラン)**.
2. Mở màn 「データコピー」 (Sao chép dữ liệu).
3. Quan sát ô 「コピーコード」 (mã sao chép) của tài khoản.
4. Bấm nút 「コピーコードの再発行」 (cấp lại mã sao chép).

## Expected result

> Nguồn: **comment BA của Nguyen Ngoc Hai trên Redmine ngày 2026-08-25 04:41:56Z** (journal #2) — trích nguyên văn:

> hiện tại với trường hợp bot free thì đang trống khá nhiều thông tin, cần fill thêm các vùng này, các logic khác không đổi: mã transfer (cùng với đó là button copy mã và chức năng thay đổi mã cũng sẽ dùng được với bot free), danh sách các chức năng backup, thông tin bot đích

Ngoài ra, quy định được ghi rõ trong popup có sẵn trên màn (theo báo cáo Dev): gói miễn phí **VẪN lấy được mã sao chép** để làm tài khoản nguồn, chỉ **không dùng được thao tác sao chép dữ liệu**.

## Actual result

> Nguồn: nguyên văn inquiry của khách hàng trong description.

- Ô mã sao chép (コピーコード) **trống**, không hiển thị gì.
- Bấm nút cấp lại mã (再発行) thì ô mã sao chép **vẫn trống** — không có tác dụng, cũng không báo lỗi gì ra giao diện.
- (Theo báo cáo Dev bổ sung) danh sách dữ liệu sẽ được sao chép và thông tin tài khoản đích **cũng trống**.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

> Redmine issue #40151 **không có attachment** nào. Link tham chiếu ngoài:
> - Slack thread: https://l-message.slack.com/archives/C0BALS7S73L/p1787628439303299
> - Dashboard CSS analytics: https://dashboard.melonglobal.net/css-analytics/?id=T11973

## Ghi chú thêm của Leader

⚠️ **Bug không có section "Tái hiện bug" trong Redmine** — root cause đã được Dev confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**.

**Điều kiện tiên quyết quan trọng để dựng env test** (rút từ báo cáo Dev — xem file 03):

- Bug là **regression do ticket #39230** — ticket đó thêm chốt chặn ở phần khởi tạo (`__construct`) của màn Sao chép dữ liệu, chặn TOÀN BỘ ajax của màn với tài khoản gói miễn phí (trả 403).
- Cần **2 loại tài khoản free** để test đủ:
  - **Free "cũ"** — `plan_type = 2`.
  - **Free "kiểu mới"** — `plan_type ≠ 2` nhưng `bot_slots → bot_contracts.contract_type = 'free'`. Loại này **trước fix bị lọt** (giao diện không khoá ô nhập mã nguồn, không hiện popup nâng cấp).
- Cần thêm **1 bot gói có phí** (standard/pro) để verify regression không hỏng luồng sao chép thật.
- ⚠️ Dev ghi rõ **không kiểm chứng được trên MySQL dev** (cổng 3306 từ chối kết nối trong container) → phần verify DB (`bots.transfer_code`) **chưa có bằng chứng thật**, QA phải tự verify.
- ⚠️ Dev nêu rủi ro: nếu bot **chưa từng có** `transfer_code` thì ô mã vẫn trống cho tới khi bấm cấp lại mã — cần phân biệt case này với bug.
