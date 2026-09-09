# UI Spec — FA-031: Hợp đồng và Thanh toán (契約情報・領収書)

## Tổng quan tính năng

| Thuộc tính | Giá trị |
|-----------|---------|
| Mã tính năng | FA-031 |
| Tên tính năng | Hợp đồng và Thanh toán (Billing Plan) |
| Actor chính | Admin (chủ tài khoản LME) |
| Portal | Admin Portal (`/basic/`, `/admin/`) |
| Mô tả | Quản lý toàn bộ hợp đồng LOA đang sử dụng: xem danh sách hợp đồng, chi tiết từng hợp đồng (plan, phí, phương thức thanh toán, lịch sử hoạt động), lịch sử thanh toán/lãnh thụ thư, lịch sử ngắt kết nối, và phát hành báo giá. |

---

## Sidebar Navigation — Nhóm 「契約関連」

Sidebar chứa nhóm menu「契約関連」(Liên quan hợp đồng) với các mục sau:

| Menu item | Label JP | URL |
|-----------|----------|-----|
| マイページ | マイページ | `/admin/my-page` |
| Hợp đồng & Giải hợp đồng | 契約情報・解約 | `/basic/point-settings` |
| Lãnh thụ thư | 領収書 | `/basic/payment-history` |
| Phát hành báo giá | 見積書発行 | `/admin/plan-estimation` |

Ngoài ra còn có link「お問い合わせ」→ `https://lme.jp/manual/contact/`

**Độ tin cậy**: Cao (quan sát trực tiếp từ snapshots)

---

## Danh sách màn hình

| Mã | Tên màn hình | URL |
|----|-------------|-----|
| SCR-BLP-01 | Danh sách hợp đồng | `/basic/point-settings` |
| SCR-BLP-02 | Chi tiết hợp đồng | `/basic/detail-contract/{id}` |
| SCR-BLP-03 | Lịch sử thanh toán / Lãnh thụ thư | `/basic/payment-history` |
| SCR-BLP-04 | Lịch sử ngắt kết nối LOA | `/basic/disconnect-history` |
| SCR-BLP-05 | Phát hành báo giá | `/admin/plan-estimation` |

---

## SCR-BLP-01: Danh sách hợp đồng

**URL**: `/basic/point-settings`
**Tiêu đề trang**: 「契約情報・領収書」

### Layout

```
[Sidebar] | [Header toolbar] [Main content]
                ↓
           [Tiêu đề + Nút ghi chú điều khoản]
           [Nút phụ: 接続解除履歴 | 領収書の発行]
           [Banner thông báo (nếu có lỗi / upgrade)]
           [Bộ lọc (checkboxes + tìm kiếm)]
           [Bảng danh sách hợp đồng]
           [Phân trang: 100件/ページ]
```

### Toolbar / Header

| Thành phần | Mô tả |
|-----------|-------|
| Tiêu đề | 「契約情報・領収書」 |
| Button 「ご契約に関する注意事項」| Mở modal hiển thị điều khoản hợp đồng (active khi click) |
| Button 「接続解除履歴」 | Điều hướng tới trang `/basic/disconnect-history` |
| Button 「領収書の発行」| Điều hướng tới trang lãnh thụ thư (có icon) |

### Banner thông báo lỗi (hiện theo điều kiện)

Khu vực phía trên bảng hiển thị các banner cảnh báo theo loại:

**1. Banner nâng cấp plan** (アップグレードが必要です):
- Hiển thị khi tổng bạn bè vượt 50,000 người
- Nội dung: 「総友だち数が50,000人を超えました。YYYY/MM/DDまでにプロプランへのアップグレードが必要です。」
- Hiển thị tên bot + LINE ID

**2. Banner lỗi thanh toán** (決済エラー):
- Hiển thị khi bot có lỗi thanh toán
- Nội dung: Deadline cưỡng chế hủy nếu không thanh toán
- Có button 「詳細を確認」→ điều hướng tới chi tiết hợp đồng
- Có thể hiển thị nhiều banner cùng lúc cho nhiều bot

**Độ tin cậy**: Cao

### Bộ lọc

| Thành phần | Loại | Giá trị |
|-----------|------|---------|
| Checkbox 「契約中」 | Checkbox (mặc định checked) | Lọc hiển thị hợp đồng đang hoạt động |
| Checkbox 「解約済み」 | Checkbox (mặc định checked) | Lọc hiển thị hợp đồng đã hủy |
| Ô tìm kiếm | Textbox | Placeholder: 「LINE公式アカウント名・LINE IDで検索」 |
| Nút clear tìm kiếm | Icon button | Xóa nội dung tìm kiếm |

**Độ tin cậy**: Cao

### Bảng danh sách hợp đồng

**Cột**:

| Cột | Nhãn JP | Ghi chú |
|-----|---------|---------|
| 1 | LINE公式アカウント名 | Tên bot + LINE ID (@xxx), có avatar thumbnail |
| 2 | ご利用プラン | Plan + chu kỳ thanh toán (ví dụ: プロ / 月払い) |
| 3 | ステータス | Trạng thái hợp đồng |
| 4 | ご利用料金 / 振込情報 | Mức phí hoặc thông tin chuyển khoản (nếu 入金待ち) |
| 5 | 決済方法 | Phương thức thanh toán |
| 6 | 次回決済(更新)日 | Ngày thanh toán/gia hạn tiếp theo |
| 7 | LOA接続日 | Ngày kết nối LINE Official Account |
| 8 | 契約の変更・解約 | Action button |

**Phân trang**: 100件/ページ, hỗ trợ nhiều trang (quan sát thấy có pagination)

### Giá trị Status (Cột ステータス)

| Giá trị JP | Ý nghĩa tiếng Việt | Ghi chú hiển thị |
|-----------|-------------------|-----------------|
| 正常 | Bình thường | Chữ màu bình thường |
| 延滞中 | Đang trễ hạn thanh toán | Hiển thị thông báo cảnh báo trong cột LOA name |
| 入金待ち | Chờ chuyển khoản ngân hàng | Hiển thị icon info, có deadline chuyển khoản và 2 nút |
| 口座発行中 | Đang phát hành tài khoản ngân hàng | Chờ hệ thống tạo tài khoản nhận tiền |
| 解約待ち | Đang chờ hủy hợp đồng | Hợp đồng đã yêu cầu hủy, chưa có hiệu lực |
| 解約済み | Đã hủy hợp đồng | Hợp đồng đã hủy hoàn toàn |
| 強制解約 | Bị cưỡng chế hủy | Hiển thị icon, bị hủy do không thanh toán |

**Độ tin cậy**: Cao (quan sát đầy đủ từ snapshot có data)

### Giá trị Plan (Cột ご利用プラン)

| Tên plan JP | Tên plan | Phí hàng tháng | Phí hàng năm |
|------------|---------|---------------|-------------|
| フリー | Free | ¥0 | - |
| スタンダード | Standard | ¥4,500/月 (毎月払い) | ¥48,600/年 |
| プロ | Pro | ¥33,000/月 (月払い) | ¥356,400/年 |

**Độ tin cậy**: Cao (từ data thực trong bảng)

### Chu kỳ thanh toán (Billing cycle)

| Giá trị JP | Ý nghĩa |
|-----------|---------|
| 月払い | Thanh toán hàng tháng |
| 毎月払い | Thanh toán mỗi tháng (tương đương 月払い) |
| 年間一括払い | Thanh toán một lần mỗi năm |

### Phương thức thanh toán (Cột 決済方法)

| Giá trị JP | Ý nghĩa |
|-----------|---------|
| カード決済（下4桁 XXXX） | Thanh toán thẻ tín dụng — hiển thị 4 số cuối |
| カード決済 | Thanh toán thẻ (không có số thẻ) |
| 銀行振込 | Chuyển khoản ngân hàng |
| - | Không có (plan Free) |

### Cột ご利用料金 (chi tiết theo status)

- **Khi status là 正常 / 延滞中 / 解約待ち**: Hiển thị mức phí (ví dụ: ¥ 33,000 / 月, ¥ 356,400 / 年, ¥ 0)
- **Khi status là 入金待ち**: Hiển thị:
  - Text: 「振込期限」+ ngày giờ deadline (ví dụ: 2026/06/06 23:59)
  - Button 「振込情報」(xem thông tin chuyển khoản)
  - Button 「請求書」(tải hóa đơn)
- **Khi status là 解約済み / 強制解約**: Hiển thị dấu `-`
- **Khi plan Free**: ¥ 0, cột 決済方法 và 次回決済 hiển thị `-`

### Cột 契約の変更・解約 (Action column)

| Button | Hiển thị khi nào |
|--------|-----------------|
| 「詳細を確認」 | Status là 延滞中 |
| 「契約詳細」 | Status là 正常, 解約待ち, 入金待ち (có LOA kết nối hoặc chưa kết nối) |
| 「アカウントの操作」 | Status là 解約済み, 強制解約 |
| 「振込キャンセル」 | Status là 入金待ち với đặc điểm nhất định (chưa rõ điều kiện cụ thể) |

**Lưu ý**: Khi LOA chưa kết nối (LINE公式アカウント未接続) nhưng còn slot trống → hiển thị link「LINE公式アカウント未接続」dẫn đến `/admin/bot-add-v2?bot_slot_id={id}` để kết nối bot.

**Độ tin cậy cột action**: Trung bình (quan sát được, nhưng logic phân nhánh đầy đủ chưa xác nhận từ code)

### Modal 「ご契約に関する注意事項」(Điều khoản hợp đồng)

Kích hoạt bằng button 「ご契約に関する注意事項」ở header.

**Nội dung modal** (tiếng Nhật, quan sát từ snapshot):
- クレジットカードのご利用明細には「L Message」「エルメッセージ」と記載されます。
- 解約はいつでも可能です。（日割り計算による返金はございません。）
- 年払いの解約の場合も、残りの契約期間に関わらず返金はいたしません。
- 有料プランから各種プランへダウングレードはできません。
- 有料を解約した場合、登録情報は残りますが、操作・閲覧ができません。
- 有料プラン解約後、再度有料プランをご契約していただくことで、登録情報の操作・閲覧が可能となります。
- 年間一括払いの場合も契約は自動更新となります。
- L Message利用料金は株式会社ユニヴァ・ペイキャストの提供する決済代行システムを利用して請求されます。
- 銀行振込でのお支払いの場合、振込先口座名義は「ｶ)ﾕﾆｳﾞｧﾍﾟｲｷｬｽﾄ」となります。

Có button「閉じる」để đóng modal.

**Độ tin cậy**: Cao

### Màn hình khi chưa có LOA nào kết nối

Hiển thị empty state:
- Icon
- Text: 「アカウントが接続されていません」
- Text: 「アカウント接続後にすべての機能をご利用いただけます」
- Button 「フリープランで接続する」

**Độ tin cậy**: Cao

---

## SCR-BLP-02: Chi tiết hợp đồng

**URL**: `/basic/detail-contract/{id}` (ví dụ: `/basic/detail-contract/1283`)
**Breadcrumb**: 契約情報・領収書 > 契約詳細

### Layout

```
[Breadcrumb: 契約情報・領収書 > 契約詳細]
[Tiêu đề: 契約詳細]
[Banner lỗi thanh toán (nếu có)]
[Thông tin hợp đồng — bảng thông tin]
[Khu vực giải hợp đồng / ngắt kết nối]
[Khu vực: Lịch sử hoạt động (操作履歴)]
[Button 戻る]
```

### Banner lỗi thanh toán (hiện khi có lỗi)

```
[Icon cảnh báo] 決済エラー：MM月DD日までに決済が行われない場合、強制解約となります
[Button: クレジットカードの変更]
```

Kèm theo hướng dẫn:
- 「ご登録のカードが利用できない場合は、クレジットカードの変更を行なってください」
- Link「プリペイド型カード」→ `https://vpc.lifecard.co.jp/`

**Độ tin cậy**: Cao

### Bảng thông tin hợp đồng (Contract Info)

Hiển thị dạng danh sách label — value:

| Label JP | Giá trị ví dụ | Ghi chú |
|---------|--------------|---------|
| (Tên bot, LINE ID) | Dev Booking Hanh / LINE ID: @740shovj | Hiển thị ở đầu trang, không có label riêng |
| ステータス | 延滞中 | Kèm thông báo deadline |
| LINE公式アカウント接続日 | 2025年12月11日 | Ngày kết nối LOA |
| ご契約プラン | プロ (có icon plan) | Tên plan |
| お支払い開始日 | 2026年11月05日 | Ngày bắt đầu thanh toán |
| ご利用料金 | 33,000円 (税込) | Phí sử dụng |
| お支払い期間 | 毎月払い | Chu kỳ thanh toán + button thay đổi |
| 次回決済日 | 2026年06月05日 | Ngày thanh toán tiếp theo |
| 決済方法 | クレジットカード | Phương thức thanh toán |
| メイン決済カード情報 | ****-****-****-4444 | Số thẻ chính (ẩn, hiện 4 số cuối) |
| サブ決済カード情報 | ****-****-****-8431 | Số thẻ phụ (nếu có) |
| クーポンコード | (trống — chỉ có button) | Mã coupon đã áp dụng |
| 主管理者 | 田中 太郎 | Admin chính |

**Separator** (đường phân cách) được dùng để nhóm các phần: thông tin cơ bản / thanh toán / coupon / quản trị / hành động hủy.

**Độ tin cậy**: Cao

### Action buttons trên trang chi tiết

| Button JP | Hành vi | Hiển thị khi nào |
|----------|---------|-----------------|
| 「次回決済から年払いに変更する」 | Thay đổi chu kỳ sang thanh toán năm (từ tháng sang năm) | Khi đang ở chu kỳ 毎月払い |
| 「メインカード情報を変更する」 | Mở form/modal thay đổi thẻ chính | Luôn hiển thị nếu có thẻ |
| 「サブカード情報を変更する」 | Mở form/modal thay đổi thẻ phụ | Khi có thẻ phụ |
| 「カード情報を削除」 | Xóa thông tin thẻ phụ | Khi có thẻ phụ |
| 「クーポンコードを入力する」 | Mở input nhập coupon | Luôn hiển thị |
| 「主管理者を変更する」 | Mở form/modal thay đổi admin chính | Luôn hiển thị |
| 「有料プラン解約へ進む」 | Bắt đầu luồng hủy plan trả phí | Trong section 解約する |
| 「接続解除へ進む」 | Bắt đầu luồng ngắt kết nối LOA | Trong section 接続解除 |
| 「戻る」 | Quay lại trang danh sách hợp đồng | Footer |

**Lưu ý section 解約する**: Text hướng dẫn: 「有料プランを解約できます。ダウングレードはできません」
**Lưu ý section 接続解除**: Text cảnh báo: 「接続を解除すると、エルメ上のデータが全て消去されます」 + link 「よくある質問を見る」

**Độ tin cậy**: Cao (các button quan sát trực tiếp)

### Khu vực Lịch sử hoạt động (操作履歴)

**Tiêu đề**: 「操作履歴」

**Bộ lọc hoạt động**:
- Button「全件表示」(hiển thị tất cả)
- Bộ lọc ngày: textbox 「開始日」và 「終了日」(date picker)
- Bộ lọc loại sự kiện (checkbox/tag dạng filter):
  - 「…開始」(các sự kiện bắt đầu)
  - 「…決済」(các sự kiện thanh toán)
  - 「…変更」(các sự kiện thay đổi)
  - 「…解約・エラー」(các sự kiện hủy và lỗi)

**Danh sách log (アクティビティログ)**:

Mỗi entry hiển thị: tên sự kiện (clickable) + ngày giờ

Các loại sự kiện quan sát được:

| Tên sự kiện JP | Ý nghĩa |
|---------------|---------|
| 決済エラー | Lỗi thanh toán |
| クーポンコードの適用 | Áp dụng mã coupon |
| プロプラン 更新（毎月） | Gia hạn plan Pro (hàng tháng) |
| メインクレジットカード変更 | Thay đổi thẻ tín dụng chính |
| サブクレジットカード変更 | Thay đổi thẻ tín dụng phụ |
| サブクレジットカード登録 | Đăng ký thẻ tín dụng phụ |
| 支払い期間変更申し込み(年間一括 → 毎月) | Đăng ký thay đổi chu kỳ từ năm sang tháng |
| 支払い期間変更申し込み(毎月 → 年間一括) | Đăng ký thay đổi chu kỳ từ tháng sang năm |

**Phân trang**: 100件/ページ

**Độ tin cậy log types**: Cao (quan sát từ data thực)

---

## SCR-BLP-03: Lịch sử thanh toán / Lãnh thụ thư

**URL**: `/basic/payment-history`
**Tiêu đề trang**: 「決済履歴・領収書のダウンロード」

### Layout

```
[Tiêu đề: 決済履歴・領収書のダウンロード]
[Hai panel nằm ngang]
  [Panel trái: 年間決済一覧]    [Panel phải: Chi tiết tháng đã chọn]
```

### Panel trái — 年間決済一覧 (Tổng quan thanh toán theo năm)

**Navigation năm**: Nút prev/next năm + hiển thị năm hiện tại (ví dụ: 2026年)
**Kèm toggle**: 「年間決済一覧」

**Bảng**:

| Cột | Nhãn JP | Ví dụ |
|-----|---------|-------|
| 1 | 年月 | 2026年01月分 |
| 2 | ご請求額 | 20,609,559 円 |
| 3 | (Action) | 「詳細を確認 >」(clickable, chọn tháng để xem chi tiết) |

Hiển thị 12 tháng của năm. Các tháng tương lai có giá trị `-`.

**Độ tin cậy**: Cao

### Panel phải — Chi tiết tháng

**Header**: Tháng đang xem (ví dụ: 2026年06月 詳細) + 2 tab: 「一括発行」/ 「個別発行」
**Button**: 「一括ダウンロード」(tải xuống hàng loạt lãnh thụ thư)

**Bảng chi tiết tháng**:

| Cột | Nhãn JP | Ví dụ |
|-----|---------|-------|
| 1 | 契約(更新)日 | 2026/06/04 (có thể sort) |
| 2 | LINE公式アカウント名 | Bot_lme 011 |
| 3 | 利用料 (税込) | 356,400 円 |
| 4 | 契約プラン | プロ |
| 5 | 支払い | 年間一括払い |
| 6 | 決済方法 | クレジットカード (下4桁 8210) |
| 7 | 備考 | - (ghi chú, thường để trống) |
| 8 | 課金ID | UUID dạng: 11f15ff2-ef3b-a666-94de-2f8f9dec533d |

**Phân trang**: 100 item/trang, có navigation
**Cột 契約(更新)日 có thể sort** (có sort icon).

**Độ tin cậy**: Cao

**API endpoints quan sát**:
- `GET /ajax/payment-history?year={year}&type=1` — tải dữ liệu tổng quan năm
- `GET /ajax/payment-history?year={year}&month={month}&type=2&per_page=100&page=1&order[column]=created_at&order[dir]=DESC` — tải chi tiết tháng

---

## SCR-BLP-04: Lịch sử ngắt kết nối LOA

**URL**: `/basic/disconnect-history`
**Breadcrumb**: TOP > 接続解除履歴

### Layout

```
[Breadcrumb: TOP > 接続解除履歴]
[Tiêu đề: 接続解除履歴]
[Ghi chú cảnh báo]
[Bảng lịch sử]
```

### Ghi chú

Text cảnh báo: 「接続解除したLINE公式アカウントの復元はできません。」(Không thể khôi phục LOA đã ngắt kết nối)

### Bảng lịch sử ngắt kết nối

| Cột | Nhãn JP | Ví dụ |
|-----|---------|-------|
| 1 | 接続解除日時 | 2026/05/28 19:22 (ngày giờ) |
| 2 | LINE公式アカウント名 | Form AnhPTN 2 + @036byblb (có avatar) |
| 3 | 操作したユーザー | 田中 太郎 (tên người thực hiện ngắt kết nối) |

**Không có pagination** quan sát được (dữ liệu hiển thị dạng cuộn).

**API endpoint**: `GET /ajax/bot-life-cycle?page=1&per_page=100&disconnect_account=true`

**Độ tin cậy**: Cao

---

## SCR-BLP-05: Phát hành báo giá

**URL**: `/admin/plan-estimation`
**Tiêu đề**: 「見積書発行」

### Layout

```
[Heading: 見積書発行]
[Mô tả: 見積書の自動発行ができます。]
[Form nhập liệu — 4 bước]
[Button: 料金を計算 / 見積書をダウンロード]
[Khu vực kết quả]
```

### Form nhập liệu (4 bước)

**① 宛名を入力** (Nhập tên người nhận):
- Textbox nhập tên (tự do)
- Combobox chọn kính ngữ (có 3 options — giá trị cụ thể chưa quan sát được từ snapshot do option không có text)

**② お申し込み予定プランを選択** (Chọn plan dự kiến đăng ký):
- Dropdown (combobox) với placeholder 「選択してください」
- Các option: chưa quan sát được giá trị cụ thể (có icon mũi tên dropdown)

**③ 決済期間を選択** (Chọn chu kỳ thanh toán):
- Radio button 「毎月払い」(mặc định checked)
- Radio button 「年間一括払い」

**④ エルメに接続するLINE公式アカウント数（接続枠数）を選択** (Chọn số LOA kết nối):
- Spinbutton (input số), giá trị mặc định = 1

### Buttons và kết quả

| Button | Hành vi |
|--------|---------|
| 「料金を計算」 | Tính toán phí dựa trên form và hiển thị kết quả |
| 「見積書をダウンロード」 | Tải xuống file báo giá (PDF) |

**Kết quả tính toán**:
- Label: 「お支払い金額（税込）」
- Giá trị: số tiền (ví dụ: `0 円` khi chưa tính)

**Độ tin cậy**: Cao (quan sát trực tiếp form)
**Điểm chưa rõ**: Giá trị cụ thể của combobox kính ngữ và dropdown chọn plan (không visible từ snapshot)

---

## User Flows

### Flow 1: Xem chi tiết hợp đồng (Happy Path)

```
SCR-BLP-01 (Danh sách hợp đồng)
    → Click 「契約詳細」hoặc 「詳細を確認」
    → SCR-BLP-02 (Chi tiết hợp đồng)
    → Xem thông tin plan, phí, thẻ, lịch sử hoạt động
    → Click 「戻る」
    → SCR-BLP-01
```

### Flow 2: Thanh toán lỗi → Thay đổi thẻ tín dụng

```
SCR-BLP-01 — Banner 「決済エラー」xuất hiện
    → Click 「詳細を確認」
    → SCR-BLP-02 — Banner đỏ lỗi thanh toán + deadline
    → Click 「クレジットカードの変更」hoặc「メインカード情報を変更する」
    → [Modal thay đổi thẻ — chưa quan sát được nội dung]
    → Thẻ mới được lưu → status trở về 正常
```

### Flow 3: Hủy plan trả phí

```
SCR-BLP-02 (Chi tiết hợp đồng)
    → Section 「解約する」
    → Click 「有料プラン解約へ進む」
    → [Modal/trang xác nhận hủy — chưa quan sát được]
    → Status chuyển sang 解約待ち (chờ đến hết kỳ)
    → Sau ngày gia hạn: status chuyển sang 解約済み
```

### Flow 4: Ngắt kết nối LOA

```
SCR-BLP-02 (Chi tiết hợp đồng)
    → Section 「接続解除」
    → Click 「接続解除へ進む」
    → [Xác nhận — cảnh báo mất toàn bộ dữ liệu]
    → LOA bị ngắt kết nối
    → Ghi nhận vào SCR-BLP-04 (lịch sử ngắt kết nối)
```

### Flow 5: Xem lãnh thụ thư và tải xuống

```
SCR-BLP-01 → Click 「領収書の発行」
    → SCR-BLP-03 (Lịch sử thanh toán)
    → Chọn năm (prev/next)
    → Click 「詳細を確認 >」của tháng cần xem
    → Panel phải cập nhật danh sách thanh toán của tháng đó
    → Click 「一括ダウンロード」để tải toàn bộ lãnh thụ thư tháng
```

### Flow 6: Phát hành báo giá

```
SCR-BLP-05 (Phát hành báo giá)
    → Nhập tên người nhận (① 宛名)
    → Chọn plan (② お申し込み予定プラン)
    → Chọn chu kỳ thanh toán (③ 決済期間)
    → Nhập số LOA (④ 接続枠数)
    → Click 「料金を計算」→ Hiển thị kết quả phí
    → Click 「見積書をダウンロード」→ Tải file PDF báo giá
```

---

## Điểm chưa rõ / Chưa quan sát được

| Điểm chưa rõ | Lý do |
|-------------|-------|
| Modal thay đổi thẻ tín dụng (メインカード情報を変更する / サブカード情報を変更する) | Chưa click vào button này trong quá trình chụp |
| Modal xác nhận hủy plan (有料プラン解約へ進む) | Không thực hiện thao tác hủy |
| Modal xác nhận ngắt kết nối (接続解除へ進む) | Không thực hiện thao tác ngắt kết nối |
| Form nhập coupon code | Chưa click vào button 「クーポンコードを入力する」 |
| Modal thay đổi admin chính (主管理者を変更する) | Chưa click vào button này |
| Modal thông tin chuyển khoản (振込情報) | Chưa click vào button này |
| Giá trị các option trong dropdown combobox kính ngữ và chọn plan tại SCR-BLP-05 | Không visible từ snapshot YAML |
| Điều kiện hiển thị button 「振込キャンセル」vs「契約詳細」khi status là 入金待ち | Cần xem code để xác định |
| Nội dung trang 「アカウントの操作」khi hợp đồng đã hủy | Chưa navigate vào trang này |
| Logic sắp xếp mặc định của bảng SCR-BLP-01 | Chưa quan sát rõ |
