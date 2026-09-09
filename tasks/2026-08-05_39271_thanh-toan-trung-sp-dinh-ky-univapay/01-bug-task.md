# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-url>` → Claude gọi MCP redmine, tạo folder mới + fill các field bên dưới (cùng với `03-dev-impact.md`). Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".
> 2. **Paste tay** — nếu không có Redmine link, member paste nguyên văn task bug.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39271 — [29712] [OEM] Thanh toán trùng sản phẩm định kỳ「マナフレンズ」` |
| Redmine URL | https://redmine.watermelon.vn/issues/39271 |
| Auto-filled | `2026-08-05 by /new-task` |
| Ngày báo cáo | `2026-08-03` |
| Khách hàng / PM báo | `AI bug detect Lme` (nguồn gốc: OEM tạo task trên Slack — 管理番号 29712, phụ trách 沖原) |
| Module / Màn hình | `Bill tiền tool` (Redmine category) — cụ thể: màn xác nhận đơn mua sản phẩm định kỳ qua UnivaPay (confirm-order) |
| Priority | `Medium` (Redmine priority = Normal) |
| Môi trường phát hiện | `<chưa rõ — tester fill>` (Redmine không ghi env; xem Ghi chú Leader) |

**Trạng thái Redmine hiện tại**: `Fix done - Đợi test` · Assigned to: `Ngô Thúy Ngần` · Commit Date: `2026-08-03`

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 29712
担当: 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1785709586499869

Số quản lý　：29712
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BMDMKNJ8M
Địa chỉ ：ikutommy.mow@gmail.com
Tên LOA　　：[Hiroko公式]マナカード講師
Phụ trách　　 ：沖原
Công cụ　 ：リンク
Nội dung yêu cầu
Đang xảy ra tình trạng thanh toán trùng đối với sản phẩm định kỳ「マナフレンズ」.
```

### 原文 (JP)

```
管理No　：29712
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BMDMKNJ8M
アドレス ：ikutommy.mow@gmail.com
LOA名　　：[Hiroko公式]マナカード講師
担当　　 ：沖原
ツール　 ：リンク
問い合わせ内容
継続商品「マナフレンズ」で重複決済が発生している。
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Nguồn: journal #128115 — Thanh Phương, 2026-08-05T06:51:05Z (nguyên văn) -->

```
** Tái hiện Bug:
- User nhấn mua item chu kỳ nhưng chưa có kết quả thanh toán, phía user hiện màn hình thông báo đợi thanh toán -> User nhấn back ở trình duyệt sau đó nhấn mua lại item
=> Bug User mua được success item lần 2 => User có 2 order của cùng 1 item chu kỳ
```

Diễn giải thành bước (để tester dựng lại — **chưa được confirm lại với người báo**):

1. Friend mở màn xác nhận đơn (confirm-order) của **sản phẩm định kỳ** thanh toán qua **UnivaPay**.
2. Bấm nút mua → màn hình hiện thông báo **đang chờ kết quả thanh toán** (giao dịch chưa có phản hồi từ cổng).
3. Trong lúc giao dịch còn treo, bấm **Back trên trình duyệt** để quay về màn xác nhận đơn.
4. Bấm **mua lại** chính sản phẩm đó.

## Expected result

- Lần bấm mua thứ 2 phải bị **chặn** (không tạo thêm order / không gọi cổng thanh toán) khi giao dịch trước của cùng khách + cùng sản phẩm còn đang chờ kết quả.
- ⚠️ *Redmine KHÔNG ghi rõ Expected — dòng trên suy từ mô tả bug + cách fix của Dev (§2 file 03). Leader confirm trước khi member viết TC.*

## Actual result

- Lần bấm mua thứ 2 **thành công** → user có **2 order của cùng 1 item chu kỳ** → bị **trừ tiền trùng**.
- Khách OEM (LOA 「[Hiroko公式]マナカード講師」, sản phẩm 「マナフレンズ」) báo bị thanh toán trùng.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

*Redmine issue #39271 KHÔNG có attachment nào.*

Link tham chiếu trong ticket:
- Slack thread: https://l-message.slack.com/archives/C0BALS7S73L/p1785709586499869
- Slack list record: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0BMDMKNJ8M
- LME test studio (journal #128067 — Thanh Phương): https://lme-test-studio.melonglobal.net/?screen=task-wizard&task=51
- Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=39271

## Ghi chú thêm của Leader

- **Môi trường**: Redmine không ghi env. Ticket là khiếu nại **khách OEM thật** (LOA 「[Hiroko公式]マナカード講師」, sản phẩm 「マナフレンズ」, bị trừ tiền thật) → **nhiều khả năng phát sinh trên Production**. Tester confirm lại trước khi ghi vào TC. Lưu ý test env cần **cửa hàng UnivaPay test** — Dev báo dev env KHÔNG có (xem §6 VERIFY file 03).

- ⚠️ **Có 3 note Auto-fixbug trong Redmine, hướng fix ĐÃ ĐỔI**:
  - Note #127877 + #127878 (2026-08-03 07:49) — hướng fix **CŨ**: quy đổi trạng thái `authorized` (đã ủy quyền) của UnivaPay thành thanh toán thành công ở job thu tiền định kỳ + webhook. Sửa 3 file.
  - Note #127882 (2026-08-03 08:06) — hướng fix **HIỆN TẠI**: chỉ thêm **guard chặn mua chồng** ở `paymentCreditCardItemV2Univapay`. Sửa **1 file**. Note ghi rõ đã **BỎ** hướng cũ vì "không phải nguyên nhân"; branch dựng lại còn 1 commit `c9f1e6a091`.
  - → `03-dev-impact.md` chỉ lấy nội dung note **#127882** (mới nhất). **KHÔNG viết TC theo 2 note cũ.**

- 🔗 **Task liên quan đã có trong repo**: [tasks/2026-06-24_38077_univapay-authorized-bill-success/](../2026-06-24_38077_univapay-authorized-bill-success/) — đúng chủ đề "authorized = success" (hướng fix cũ của #39271, commit `7fe8a9b986` ngày 24/06 mà note AI có nhắc). Đọc để tránh trùng TC và để biết behavior hiện tại của job đối soát bù.

- ⚠️ **Dev KHÔNG tái hiện được bug trên dev env** (không kết nối được DB, không có cửa hàng UnivaPay test) — verify chỉ dừng ở mức `php -l` + đọc mã. Rủi ro fix chưa được chứng minh chạy đúng → TC phải verify bằng thao tác thật.

- ⚠️ **Recover data**: Dev ghi CÓ cần recover (hoàn tiền + chỉnh `c_expired_date` / `count_bill_error` cho khách đã bị trừ trùng). Code fix KHÔNG tự sửa data cũ → việc này do vận hành/BA làm, **ngoài phạm vi TC fix**, nhưng Leader cần track riêng.

- ⚠️ **Điểm Dev tự nêu là chưa cover**: luồng thẻ **Stripe** của cùng màn xác nhận đơn **chưa có guard tương tự** (Dev ghi "ngoài phạm vi yêu cầu"). Leader quyết định có yêu cầu TC/ticket riêng cho Stripe hay không.
