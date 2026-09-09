# FA-042 — Add Bot Router (「新規LOA接続」)

## Tổng quan

| Thuộc tính | Giá trị |
|------------|---------|
| Mã tính năng | FA-042 |
| Tên hiển thị | 「新規LOA接続」/ Add Bot Router |
| URL chính | `/admin/bot-add-v2` |
| Portal | Admin |
| Loại màn hình | Vue.js SPA (Single Page Application) — toàn bộ wizard chạy trong 1 trang |
| Mô tả | Wizard hướng dẫn Admin kết nối LINE Official Account (LOA) mới với hệ thống LME. Gồm 6 bước chính (currentStep 1-6), trong đó bước 3 là wizard con 5 roadStep. |

**Mức độ tin cậy chung**: **Cao** — phân tích trực tiếp từ Blade template `bot_add_v3.blade.php` và JS file `add_bot.js`.

---

## Actors

| Actor | Mô tả |
|-------|-------|
| Admin | Người dùng chính — thực hiện toàn bộ wizard kết nối LOA |
| Staff | Không có quyền truy cập tính năng này (chỉ Admin mới tạo bot) |

---

## Danh sách màn hình

| Mã | Tên màn hình | State (Vue) | Mô tả |
|----|-------------|-------------|-------|
| SCR-BAV-01 | Màn hình chào mừng | `currentStep === 1` | Hiển thị khi Admin lần đầu kết nối LOA — giới thiệu tính năng LME |
| SCR-BAV-02 | Điều kiện tiên quyết | `currentStep === 2` | Video hướng dẫn + 4 điều kiện phải đọc trước khi kết nối |
| SCR-BAV-03 | Wizard — Step 1: Xác nhận thông tin | `currentStep === 3, roadStep === 1` | Xác nhận Channel ID giống nhau giữa LINE OA Manager và LINE Developers |
| SCR-BAV-04 | Wizard — Step 2: Tạo LINE Login Channel | `currentStep === 3, roadStep === 2` | Hướng dẫn 9 bước tạo LINE Login Channel + 4 checkbox xác nhận |
| SCR-BAV-05 | Wizard — Step 3: Nhập thông tin API | `currentStep === 3, roadStep === 3` | Form nhập 4 thông tin Messaging API và LINE Login Channel |
| SCR-BAV-06 | Wizard — Step 4: Cài đặt Webhook | `currentStep === 3, roadStep === 4` | Hướng dẫn bật Webhook + xác nhận checkbox + kiểm tra qua API |
| SCR-BAV-07 | Wizard — Step 5: Kiểm tra kết nối (QR) | `currentStep === 3, roadStep === 5` | Hiển thị QR code, đếm ngược 3 phút, polling xác nhận kết nối |
| SCR-BAV-08 | Hoàn thành kết nối | `currentStep === 4` | Chúc mừng — kết nối thành công |
| SCR-BAV-09 | Lỗi kết nối | `currentStep === 5` | Hiển thị khi QR test timeout — cho phép thử lại |
| SCR-BAV-10 | Cảnh báo tài khoản chưa xác thực | `currentStep === 6` | Cảnh báo 未認証アカウント — giải thích hạn chế |

---

## Chi tiết từng màn hình

### SCR-BAV-01 — Màn hình chào mừng

**State**: `currentStep === 1`
**Screenshot**: `ui/screenshots/SCR-BAV-01-welcome.png`

#### Layout
- Header toàn trang: L Message logo (link tới `/basic/overview`), icon「サポート」, icon「お知らせ」, tên user + icon dropdown
- Nội dung: Layout 2 cột (left/right)

#### Cột trái — Feature Highlights (3 cards)
Mỗi card gồm icon hình minh họa + tiêu đề + mô tả:

| Card | Tiêu đề | Mô tả |
|------|---------|-------|
| 1 | 「メッセージをセグメント配信」 | 特定の友だちを絞り込んでメッセージ配信ができます。もちろん、配信日時を指定して予約することも可能です。 |
| 2 | 「予約を簡単管理」 | 美容室やマッサージ、ヨガや料理教室やパソコンスクールなど様々なビジネスの予約を管理することができます。 |
| 3 | 「LINE上で決済も完結」 | 単品商品やサブスク商品の決済までエルメで完結。購入者のみにアクションを稼働させることもできます。 |

#### Cột phải — Thẻ chào mừng
- Tiêu đề: `{username} 様` (tên user từ server)
- Dòng 1: 「L Message（エルメ）に」
- Dòng 2: 「ようこそ！」
- Logo LME (ảnh pelican `/images/logo_icon.png`)
- Text phụ: 「（アヒルじゃなくてペリカンだよ！）」
- Button:「無料で利用開始 ›」(class: `btn-sns-line-success btn-sns-line-lg`, width: 250px) → click gọi `nextStep()` → `currentStep++` (chuyển sang SCR-BAV-02)

#### Ghi chú kỹ thuật
- Trang có `<div class="triangle">` hiển thị khi `currentStep <= 2 || currentStep === 4 || currentStep === 5` — decorative element
- Data Vue: `currentStep = 1`, `roadStep = 1` (init)
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template + snapshot

---

### SCR-BAV-02 — Điều kiện tiên quyết

**State**: `currentStep === 2`
**Screenshot**: `ui/screenshots/SCR-BAV-02-preconditions.png`

#### Layout
- 2 cột: cột trái chiếm 7/12, cột phải chiếm 5/12

#### Cột trái — Video hướng dẫn
- Title: 「エルメのご利用開始にあたり必ずご覧ください (時間：約2分)」
- Video Vimeo embed: `https://player.vimeo.com/video/1012371771?h=a72281943f` (video ~2 phút, tiêu đề: "L Message（エルメ）のご利用にあたって")

#### Cột phải — 4 điều kiện bắt buộc
Danh sách có đánh số (1-4):

| # | Nội dung | Ghi chú đặc biệt |
|---|----------|-----------------|
| 1 | エルメはLINE公式アカウントの拡張機能となります。**エルメのみでのご利用はできません。** | Link「こちら」→ `https://lme.jp/media/line/account-open/` (mở tab mới) |
| 2 | **エルメのご利用にはパソコンが必須となります。** タブレット・スマートフォンのみのご利用はできません。 | Text màu đỏ (#F44336), font-weight 600 |
| 3 | 他社システムからの乗り換えの場合に関しましては... | Link「こちら」→ Vimeo `https://vimeo.com/1012367856/3a81e2434a?share=copy` (tab mới) |
| 4 | 総友だち数(※)が 10万人以上の方は接続設定の前に「利用申請フォーム」より申請をお願いいたします。 | Link「利用申請フォーム」→ Tayori form (tab mới) |

**Chú thích cuối** (font-size 10px, font-weight 300):
> (※) エルメとLINE公式アカウントの接続時にLINE公式アカウント上の「友だち追加数 - ブロック」の数がエルメ上で「総友だち数」として表示されます。

#### CTA
- Button: 「接続設定に進む ›」(class: `btn-sns-line-success btn-sns-line-lg`, width: 250px) → click `nextStep()` → `currentStep++` (chuyển sang SCR-BAV-03, `roadStep = 1`)

#### Ghi chú kỹ thuật
- Không có điều kiện chặn — Admin có thể click tiếp mà không cần xem video
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template + snapshot

---

### SCR-BAV-03 — Wizard Step 1: Xác nhận thông tin kết nối

**State**: `currentStep === 3, roadStep === 1`
**Screenshot**: `ui/screenshots/SCR-BAV-03-connect-step1.png`, `ui/screenshots/SCR-BAV-03-connect-step1-checked.png`

#### Layout
- Layout 2 cột: Cột trái (nội dung hướng dẫn + video + progress bar thu gọn), Cột phải (hành động xác nhận)

#### Cột trái — Tiêu đề và Video

**Header tiêu đề**:
- 「LINE公式アカウントとエルメの接続設定」(font-size 18px, font-weight 600)

**Mục đang active**:
- Title: 「Step1.接続情報の確認」(bold)
- Subtitle: 「接続に必要な情報が表示されているかを確認します。」
- Video Vimeo embed: `https://player.vimeo.com/video/1013001947?h=d5e11cd3a6` (4:48, tiêu đề: "L Message（エルメ）の新規接続方法STEP１")
- Link: 「設定動画をスマホで見る」→ click mở modal QR code với URL video

**Progress sidebar — các step phía sau (thu gọn)**:
| Step | Label |
|------|-------|
| 2 | 「LINEログインチャネル作成」|
| 3 | 「API情報入力」|
| 4 | 「Webhook設定」|
| 5 | 「接続テスト」|

#### Cột phải — Xác nhận

**2 links mở trang bên ngoài** (mỗi link có icon external-link + label「ページを表示」):
- 「LINE公式アカウント管理画面」→ `https://account.line.biz/login?redirectUri=https%3A%2F%2Fmanager.line.biz%2F` (tab mới)
  - Ảnh minh họa: `/images/messaging_api.png` (min-height 188px)
- 「LINE developers」→ `https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2F` (tab mới)
  - Ảnh minh họa: `/images/Line_developers.png` (min-height 172px)

**Checkbox xác nhận**:
- `checkboxes.step1Checkbox1`: 「チャネルIDが同一であることを確認した」
- Toggle click: check/uncheck, text đổi màu xanh khi checked

**Nút và link**:
- Button「次へ進む」: disabled khi `!checkboxes.step1Checkbox1` → click: reset checkbox, `roadStep++` (→ roadStep=2, SCR-BAV-04)
- Link「同一のチャネルIDが見つからなかった場合」→ `https://youtu.be/CGtUSZrIksI?si=5N2bNiErBNdRBnra` (tab mới)

#### Ghi chú kỹ thuật
- Đây là bước đầu tiên trong wizard con `roadStep`
- `checkboxes.step1Checkbox1` được reset về `false` sau khi chuyển sang bước tiếp theo
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template, JS, và snapshot

---

### SCR-BAV-04 — Wizard Step 2: Tạo LINE Login Channel

**State**: `currentStep === 3, roadStep === 2`
**Screenshot**: `ui/screenshots/SCR-BAV-04-connect-step2.png`

#### Layout
- 2 cột: Cột trái (video + 9 bước hướng dẫn), Cột phải (4 checkbox xác nhận)

#### Cột trái — Video và hướng dẫn

**Header**:
- 「LINE公式アカウントとエルメの接続設定」
- 「Step2.LINEログインチャネル作成」(bold)
- 「LINEログインチャネルを新規作成してください」

**Video**: Vimeo `https://player.vimeo.com/video/1012986183?h=7548f434ef` (3:52, "L Message（エルメ）の新規接続方法STEP2")

**Link mobile**: 「設定動画をスマホで見る」→ modal QR

**9 bước hướng dẫn** (numbered instruction list với ảnh minh họa):

| # | Nội dung | Ảnh |
|---|----------|-----|
| 1 | Link「LINE developers」→ `https://developers.line.biz/ja/` | — |
| 2 | 画面右上の「コンソール」をクリックします | — |
| 3 | 画面左から、ステップ1で作成したプロバイダーをクリックします | — |
| 4 | チャネル設定＞「新規チャネル作成」をクリックします | `step3_1.png` |
| 5 | チャネルの種類は「LINEログイン」を選択します | `step3_2.png` |
| 6 | 必要項目を入力して「作成」をクリックします | — |
| 7 | 画面上部にある「開発中」をクリックして「公開済み」に変更します | `step3_3_new.png` |
| 8 | 友だち追加オプション/リンクされたLINE公式アカウントの「編集」をクリックし接続中のLINE公式アカウントを選択後「更新」をクリックします。※LINE公式アカウント名が表示されない場合、ステップ1の確認内容に誤りがあります。(text màu đỏ) | `step3_4_new.png` |
| 9 | プロバイダーのトップに戻り「Messaging API」と「LINEログイン」の2つのパネルがあるか確認します。 | `step3_5_new.png` |

#### Cột phải — 4 Checkbox xác nhận

Title: 「全てを確認してチェックを入れてください」

| # | Checkbox (v-model) | Nội dung | Ảnh minh họa |
|---|-------------------|----------|-------------|
| ① | `checkboxes.step2Checkbox1` | LINEログインチャネルの新規作成が完了した | — |
| ② | `checkboxes.step2Checkbox2` | チャネルを「開発中」から「公開済み」にした | `step3_6.png` |
| ③ | `checkboxes.step2Checkbox3` | 友だち追加オプション/リンクされたLINE公式アカウントを設定した。（左画面⑧の操作） | `step3_8.png` |
| ④ | `checkboxes.step2Checkbox4` | プロバイダーのトップに「Messaging API」と「LINEログイン」の2つのパネルがあるか確認した。 | `step3_7.png` |

**Nút và link**:
- Button「次へ進む」: disabled khi bất kỳ trong 4 checkbox chưa được check → click `roadStep++` (→ roadStep=3, SCR-BAV-05)
- Link「前のステップに戻る」→ click `backRoadStep()` → `roadStep--` (→ roadStep=1, SCR-BAV-03)

#### Ghi chú kỹ thuật
- Tất cả 4 checkbox phải được check: `!step2Checkbox1 || !step2Checkbox2 || !step2Checkbox3 || !step2Checkbox4`
- Khi Back từ SCR-BAV-05 → 4 checkboxes bị reset về `false`
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template, JS, và snapshot

---

### SCR-BAV-05 — Wizard Step 3: Nhập thông tin API

**State**: `currentStep === 3, roadStep === 3`
**Screenshot**: `ui/screenshots/SCR-BAV-05-api-form.png`

#### Layout
- 2 cột: Cột trái (video + 6 bước hướng dẫn), Cột phải (form nhập 4 thông tin API)

#### Cột trái — Video và hướng dẫn

**Header**:
- 「LINE公式アカウントとエルメの接続設定」
- 「Step3.API情報入力」(bold)
- 「Messaging APIとLINEログインの接続情報を入力します。」

**Video**: Vimeo `https://player.vimeo.com/video/1013027981?h=aec0ac7e9a` (2:15, "L Message（エルメ）の新規接続方法STEP3")

**Link mobile**: 「設定動画をスマホで見る」→ modal QR

**6 bước hướng dẫn** (với ảnh minh họa):

| # | Nội dung | Ảnh |
|---|----------|-----|
| 1 | Step1で作成したMessaging APIをクリックします | `step4_1_new.png` |
| 2 | 「チャネル基本設定」>「基本情報」にあるチャネルIDをコピーして「Messaging APIのチャネルID」の入力欄にペーストします。 | `step4_2.png` |
| 3 | 下にスクロールをしていき、チャネルシークレットをコピーして「Messaging APIのチャネルシークレット」の欄にペーストします。 | `step4_3_new.png` |
| 4 | プロバイダーのトップに戻りStep2で作成した「LINEログイン」をクリックします。 | `step4_4.png` |
| 5 | 「チャネル基本設定」>「基本情報」にあるチャネルIDをコピーして「LINEログインのチャネルID」の入力欄にペーストします。 | `step4_5_new.png` |
| 6 | 下にスクロールをしていき、チャネルシークレットをコピーして「LINEログインのチャネルシークレット」の欄にペーストします。 | `step4_6_new.png` |

#### Cột phải — Form nhập API

**Tiêu đề form**: 「Messaging APIとLINEログインの接続情報を入力してください。」

**Section Messaging API**:
- Label: 「Messaging API」
- Ảnh minh họa: `step4_1_new.png`
- Input 1: placeholder「Messaging APIのチャネルID」, v-model: `channelId`, badge「必須」
- Input 2: placeholder「Messaging APIのチャネルシークレット」, v-model: `channelSecret`, badge「必須」

**Error messages cho Messaging API** (hiển thị bằng `v-show`):
- `errors.channel === 'channel_id_exist'`: 「このLINE公式アカウントはすでにL Messageに接続されています。こちらから、エルメ登録メールアドレスをご確認いただけます。」 — Link「こちら」→ `https://step.lme.jp/check-user` (tab mới)
- `errors.channel === 'access_token_error'`: 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。ご不明な場合は、サポート窓口までお問い合わせください。」 — Link「サポート窓口」→ LINE chat `https://line.me/R/ti/p/%40770yphxr`

**Section LINE Login**:
- Label: 「LINEログイン」
- Ảnh minh họa: `step4_4.png`
- Input 3: placeholder「LINEログインのチャネルID」, v-model: `lineChannelId`, badge「必須」
- Input 4: placeholder「LINEログインのチャネルシークレット」, v-model: `lineChannelSecret`, badge「必須」

**Error message cho LINE Login** (hiển thị bằng `v-if`):
- `errors.client` (truthy): 「入力した情報に誤りがありますので、入力情報を再度ご確認ください。ご不明な場合は、サポート窓口までお問い合わせください。」 (màu đỏ, font-size 12px)

**Nút và link**:
- Button「次へ進む」: disabled khi bất kỳ trong 4 input trống → click: gọi `submitForm()`
- Link「前のステップに戻る」→ click: `roadStep--` và reset 4 checkboxes step2 về `false`

#### Luồng gọi API khi submit

```
submitForm()
  ├── validateChannel(channelId, channelSecret)
  │     └── POST /admin/step2-check-validate  {channel_id, channel_secret, type: 'channel'}
  │           ├── success → lưu channel_access_token, tiếp tục
  │           └── fail → errors.channel = response.msg, dừng
  └── validateClient(lineChannelId, lineChannelSecret)
        └── POST /admin/step2-check-validate  {channel_id, channel_secret, type: 'client'}
              ├── success → lưu client_access_token, roadStep++ (→ roadStep=4, SCR-BAV-06)
              └── fail → errors.client = response.msg, dừng
```

#### Ghi chú kỹ thuật
- Validation 2 API call tuần tự (Promise chain)
- `channel_access_token` và `client_access_token` được lưu trong Vue data, dùng ở bước tiếp theo
- Watch tự động trim whitespace cho cả 4 input
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template, JS, và snapshot

---

### SCR-BAV-06 — Wizard Step 4: Cài đặt Webhook

**State**: `currentStep === 3, roadStep === 4`

#### Layout
- 2 cột: Cột trái (video + 4 bước hướng dẫn), Cột phải (hướng dẫn + checkbox + nút)

#### Cột trái — Video và hướng dẫn

**Header**:
- 「LINE公式アカウントとエルメの接続設定」
- 「Step4.Webhook設定」(bold)
- 「Webhookの設定を行います。」

**Video**: Vimeo `https://player.vimeo.com/video/1013935484?h=f891a298df` ("L Message（エルメ）の新規接続方法STEP4")

**Link mobile**: 「設定動画をスマホで見る」→ modal QR

**4 bước hướng dẫn**:

| # | Nội dung |
|---|----------|
| 1 | Link 「LINE公式アカウント管理画面」→ `https://account.line.biz/login?...` |
| 2 | LINE公式アカウント管理画面の右上にある「設定」をクリック |
| 3 | 左の項目一覧から「応答設定」をクリック |
| 4 | ① チャット（ON 推奨）, ② あいさつメッセージ（OFF 推奨）, ③ **Webhook（ON 必須）** (text màu đỏ, bold) を下記画像のように設定してください。 |

Ảnh minh họa (bước 4): `add_bot_step_2.png` (max-width: 446px)

#### Cột phải — Xác nhận Webhook

**Hướng dẫn tóm tắt**:
- 「LINE公式アカウント管理画面の「設定」>「応答設定」より設定内容を変更してWebhookをオンにしてください。」
- Ảnh: `enable_button.png`
- Ghi chú: 「※ チャット・あいさつメッセージはON・OFFを逆に設定しても問題ありません。」

**Checkbox**:
- `canNext`: 「Webhookをオンに設定した」
- Toggle click: check/uncheck

**Error** (khi API trả về thất bại):
- `errorWebhook` (truthy): 「Webhookをオンにして下さい。既にオンの場合は、一度オフにしてから再度オンに変更して下さい。」(màu đỏ)

**Nút và link**:
- Button「次へ進む」: disabled khi `!canNext` → click: gọi `checkWebhook()`
- Link「前のステップに戻る」→ click: `roadStep--` (→ roadStep=3, SCR-BAV-05)

#### Luồng gọi API khi submit

```
checkWebhook()
  └── POST /admin/check-enable-use-webhook  {channel_access_token}
        ├── success (response.data.success) → errorWebhook = '', gọi showQrCode()
        │     └── showQrCode()
        │           └── POST /admin/step2-check  {channel_id_new, channel_secret_new, client_id_new, client_secret_new, bot_slot_id, type, botIdChange, ids}
        │                 ├── success → roadStep++ (→ roadStep=5, SCR-BAV-07), lưu qrCode, bot_new_id, bắt đầu countdown(180s)
        │                 └── fail → alert(msg), roadStep = 3
        └── fail → errorWebhook = response.data.msg (hiển thị error)
```

#### Ghi chú kỹ thuật
- `channel_access_token` được lấy từ bước SCR-BAV-05 (đã lưu trong Vue data)
- `canNext` được dùng lại cho cả bước này (khác với `checkboxes.*` ở các bước trước)
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template và JS

---

### SCR-BAV-07 — Wizard Step 5: Kiểm tra kết nối (QR Code)

**State**: `currentStep === 3, roadStep === 5`

#### Layout
- 2 cột: Cột trái (video + 2 bước hướng dẫn), Cột phải (QR code + đếm ngược)

#### Cột trái — Video và hướng dẫn

**Header**:
- 「LINE公式アカウントとエルメの接続設定」
- 「Step5.接続テスト」(bold)
- 「接続テストを行います。」

**Video**: Vimeo `https://player.vimeo.com/video/1013935129?h=7e5831df22` ("L Message（エルメ）の新規接続方法STEP5")

**Link mobile**: 「設定動画をスマホで見る」→ modal QR

**2 bước hướng dẫn**:

| # | Nội dung |
|---|----------|
| 1 | 画面に表示されているQRコードを読み取ってください。スマートフォン（Android・iPhone）版LINEのQRコードリーダーを起動して、QRコードをスキャンしてください。 |
| 2 | LINE公式アカウントにお好きなスタンプを送信してください。**下記のメッセージが届いたら接続テスト完了です。** (màu đỏ, bold) + Ảnh minh họa: `bot_add_modal_4_2.png` |

#### Cột phải — QR Code và Polling

**Tiêu đề**:
- 「スマートフォンを準備して」
- 「QRコードを読み取ってください」

**QR Code**:
- Ảnh hướng dẫn scan: `scan_qr_instruction.png`
- QR code động: `<img :src="qrCode">` (width: 150px, URL từ server trả về ở bước trước)

**Thông báo chờ** (text màu xanh lá #08BF5A):
- 「接続完了のメッセージがLINEに届いたら」
- 「自動で画面が切り替わります。」

**Cơ chế polling (đếm ngược và kiểm tra)**:
- Tổng thời gian: 180 giây (3 phút)
- Interval: `setInterval(..., 1000)` — mỗi giây giảm `time--`
- Kiểm tra mỗi 5 giây: `if (this.time % 5 === 0)` → gọi `checkFriend()`
- Khi hết 180 giây (`time === 0`): gọi `deleteBot()` → `currentStep = 5` (SCR-BAV-09)

**API polling**:
```
checkFriend()
  └── POST /admin/step2-check-friend  {bot_id, bot_slot_id, type, botIdChange, landing_id}
        ├── res.success === 'fail_provider' → deleteBot() → currentStep = 5 (SCR-BAV-09)
        ├── res.success (thành công) + botIdChange → saveStep1() (đổi bot)
        └── res.success (thành công) → clearInterval, currentStep = 4 (SCR-BAV-08)
```

**Nút trợ giúp và link**:
- Section「テストがうまくできない場合」(icon headphones):
  - Link「サポートに問い合わせ」→ ChatPlus `https://app.chatplus.jp/chat/visitor/e3f8121b_1?t=btn` (tab mới)
- Link「前のステップに戻る」→ click `backToChecking()`: `roadStep--` và `isCounting = false` (dừng countdown)

#### Ghi chú kỹ thuật
- QR Code URL được lấy từ response của `/admin/step2-check` ở bước Webhook
- `bot_new_id` cũng được lưu từ response đó
- Khi timeout: `deleteBot()` gọi `POST /admin/step2-delete-bot {bot_id}` để xóa bot đã tạo
- **Mức độ tin cậy**: **Cao** — xác nhận từ JS

---

### SCR-BAV-08 — Màn hình hoàn thành kết nối

**State**: `currentStep === 4`

#### Layout — Centered, layout đơn giản

**Thông điệp chúc mừng**:
- H2: 「おめでとうございます！」(text-center)
- H3: 「接続が完了しました」

**Ảnh minh họa** (3 ảnh inline):
- Bot avatar: `avatar_bot.png`
- Link icon: `link-light.png` (mini)
- LINE avatar: `line_avatar.png`

**CTA**:
- Button「エルメの設定に進む ›」→ click: gọi `checkAuthBot()`

#### Luồng sau khi click

```
checkAuthBot()
  └── POST /admin/check-auth-bot  {bot_id}
        ├── response.data.success → redirect sang /manual/tutorial?botId={bot_new_id}
        └── !response.data.success → lưu bot_name, currentStep = 6 (SCR-BAV-10)
```

#### Ghi chú kỹ thuật
- Màn hình này cũng được hiển thị khi URL có `?status=successful` (reload sau khi connect thành công) — xử lý trong `mounted()`
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template và JS

---

### SCR-BAV-09 — Lỗi kết nối

**State**: `currentStep === 5`

#### Nội dung (layout centered, đơn giản)

- Title: 「接続テストがうまくいかなかった場合」(text-center, font-size 20px, font-weight 700)
- Mô tả: 「ステップ1に戻り設定内容を再確認するか有料の接続サポートをお申し込みください。」
- Button: 「ステップ1に戻って再設定」→ click `addFriendAgain()`:
  - `currentStep = 3, roadStep = 1`
  - Reset tất cả checkboxes về `false`
- Link (font-size 14px): 「有料の接続サポートを申し込む」→ `https://go.lmes.jp/landing-qr/1656886828-yoaLLZlp?uLand=YysU16` (tab mới)

#### Ghi chú kỹ thuật
- Màn hình này được kích hoạt khi: (1) countdown 180s hết / (2) `fail_provider` từ checkFriend API / (3) `deleteBot()` hoàn tất
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template và JS

---

### SCR-BAV-10 — Cảnh báo tài khoản chưa xác thực

**State**: `currentStep === 6`

#### Layout
- 2 cột: cột trái chiếm 60%, cột phải chiếm 40%
- `min-width: 1000px; min-height: 450px`

#### Cột trái — Video

- Title: 「未認証アカウントの場合の注意点」
- Video Vimeo embed: `https://player.vimeo.com/video/1012371326?h=b6037f4541` (chưa biết độ dài)
- Link dưới video: 「関連マニュアル：既存友だち追加方法」→ `https://lme.jp/manual/add_existing_friends/` (tab mới)

#### Cột phải — Cảnh báo

**Header cảnh báo**:
- Icon: `fas fa-exclamation-triangle` (màu vàng/warning)
- 「ちょっと待って！」(font-size 18px)

**Thông tin bot**:
- Icon shield: `shield.png` (50x50px)
- Tên bot: `@{{ bot_name }}` (font-size 16px, font-weight 600) — tên thực từ server

**Nội dung cảnh báo**:
- Link: 「未認証アカウント」→ `https://www.lycbiz.com/jp/column/line-official-account/technique/20190726/` (tab mới, bold, underline)
- Text: 「では**すぐにエルメから友だち全員にメッセージを送ることはできません。**」
- Text phụ: 「詳細は左の動画をご覧ください」

**CTA**:
- Button 2 dòng:「動画の内容を理解したのでエルメの設定に進む」→ click `redirectToManual()`: redirect sang `/manual/tutorial?botId={bot_new_id}`

#### Ghi chú kỹ thuật
- `bot_name` được lấy từ response của `/admin/check-auth-bot` (bước SCR-BAV-08)
- Màn hình này xuất hiện khi LINE OA chưa được LINE Corp xác thực (未認証 vs 認証済み)
- **Mức độ tin cậy**: **Cao** — xác nhận từ Blade template và JS

---

## Modal phụ — QR Video (dùng chung)

**Trigger**: Click link「設定動画をスマホで見る」tại bất kỳ roadStep nào

**Nội dung modal** (`showModal === true`):
- Icon đóng: `fa-times` → click đóng modal (`showModal = false`)
- Title: 「スマートフォンを準備して」
- Subtitle: 「QRコードを読み取ってください」
- Ảnh: `scan_qr_instruction.png`
- QR code (div `#qrcode`): tạo dynamically bằng thư viện `qrcodejs`, màu xanh lá `#08BF5A`, size 128x128
- Footer text: 「設定動画が表示されます」

**QR content**: URL video Vimeo tương ứng với roadStep đang active

**Mức độ tin cậy**: **Cao**

---

## URL Parameters

| Parameter | Kiểu | Mô tả |
|-----------|------|-------|
| `bot_slot_id` | string | ID của slot bot trong hợp đồng đã mua — bắt buộc khi kết nối bot mới |
| `hash_id` | string | Hash ID (optional) |
| `type` | string | Loại kết nối: `type=2` là enterprise |
| `typeChange` (camelCase trong JS) | string | Loại thay đổi khi đổi bot |
| `status` | string | `status=successful` → tự động chuyển sang `currentStep = 4` khi reload |
| `user_access_link_invite` | string | Trigger modal xác nhận chấp nhận lời mời Staff |
| `user_access_link_edit_owner_bot` | string | Trigger modal xác nhận đổi owner bot |
| `code_invite` | string | Mã invite (dùng cùng `user_access_link_invite`) |
| `type_invite` | string | Loại invite |
| `error_message` | string | Thông báo lỗi hiển thị qua `alert()` |

---

## User Flows

### Flow 1 — Kết nối LOA mới (Happy Path)
```
SCR-BAV-01 (Welcome)
  → [click 「無料で利用開始」] →
SCR-BAV-02 (Điều kiện tiên quyết)
  → [click 「接続設定に進む」] →
SCR-BAV-03 (Step1: Xác nhận Channel ID, check checkbox)
  → [click 「次へ進む」] →
SCR-BAV-04 (Step2: Tạo LINE Login Channel, check 4 checkbox)
  → [click 「次へ進む」] →
SCR-BAV-05 (Step3: Nhập 4 thông tin API, submit)
  → [API validate thành công] →
SCR-BAV-06 (Step4: Webhook, check checkbox, submit)
  → [API webhook OK + QR code tạo thành công] →
SCR-BAV-07 (Step5: Scan QR, gửi sticker)
  → [checkFriend polling thành công trong 180s] →
SCR-BAV-08 (Hoàn thành)
  → [click 「エルメの設定に進む」] →
  ├── [Bot đã xác thực] → /manual/tutorial?botId=X
  └── [Bot chưa xác thực] → SCR-BAV-10 (Cảnh báo)
        → [click button] → /manual/tutorial?botId=X
```

### Flow 2 — QR Test timeout
```
SCR-BAV-07 (Step5: Scan QR)
  → [Countdown 180s hết hoặc fail_provider] →
  → [deleteBot() API] →
SCR-BAV-09 (Lỗi kết nối)
  ├── [click 「ステップ1に戻って再設定」] → SCR-BAV-03 (Step1, reset)
  └── [click link có phí] → trang ngoài (tab mới)
```

### Flow 3 — Back navigation trong wizard
```
Từ bất kỳ roadStep (2-5) → click「前のステップに戻る」→ roadStep - 1
Đặc biệt:
  - Back từ SCR-BAV-04 → SCR-BAV-03: không reset checkbox step1
  - Back từ SCR-BAV-05 → SCR-BAV-04: reset 4 checkbox step2 về false
  - Back từ SCR-BAV-07 → SCR-BAV-06: dừng countdown (isCounting = false)
```

### Flow 4 — API error ở Step 3
```
SCR-BAV-05 (Step3: Nhập API)
  → [submit, API lỗi]
  ├── errors.channel = 'channel_id_exist' → hiển thị "LOA đã kết nối với LME rồi"
  ├── errors.channel = 'access_token_error' → hiển thị "Thông tin nhập sai"
  └── errors.client (truthy) → hiển thị "Thông tin LINE Login sai"
  → [User sửa và thử lại]
```

### Flow 5 — Mời Staff / Đổi owner (phụ, qua URL params)
```
Khi truy cập URL có ?user_access_link_invite=true
  → Modal「確認アカウントの承認」hiện tự động (jQuery modal)
Khi truy cập URL có ?user_access_link_edit_owner_bot=true
  → Modal「Owner Bot変更の承認」hiện tự động
```

---

## Flow Diagram (Mermaid)

```mermaid
flowchart TD
    A[SCR-BAV-01\nWelcome] -->|click 無料で利用開始| B[SCR-BAV-02\n前提条件]
    B -->|click 接続設定に進む| C[SCR-BAV-03\nStep1 Channel確認]
    C -->|checkbox check + 次へ進む| D[SCR-BAV-04\nStep2 LINE Login作成]
    D -->|4 checkboxes + 次へ進む| E[SCR-BAV-05\nStep3 API入力]
    D -->|前のステップに戻る| C
    E -->|API validate OK + 次へ進む| F[SCR-BAV-06\nStep4 Webhook設定]
    E -->|前のステップに戻る| D
    E -->|API error channel_id_exist| E
    E -->|API error access_token_error| E
    F -->|webhook OK + QR生成| G[SCR-BAV-07\nStep5 QR Test]
    F -->|前のステップに戻る| E
    G -->|polling 成功 180s以内| H[SCR-BAV-08\n接続完了]
    G -->|timeout / fail_provider| I[deleteBot API]
    I --> J[SCR-BAV-09\n接続失敗]
    G -->|前のステップに戻る| F
    J -->|ステップ1に戻る| C
    H -->|click エルメ設定へ → check-auth-bot| K{Bot 認証済み?}
    K -->|Yes| L[/manual/tutorial]
    K -->|No| M[SCR-BAV-10\n未認証アカウント警告]
    M -->|click 設定に進む| L
```

---

## Điểm chưa rõ

| # | Điểm cần làm rõ | Nguồn cần kiểm tra |
|---|-----------------|-------------------|
| 1 | Thời lượng video Step4 và Step5 (Vimeo 1013935484 và 1013935129) chưa biết chính xác | Vimeo API hoặc xem trực tiếp |
| 2 | Màn hình SCR-BAV-07 có hiển thị bộ đếm ngược `{minute}:{second}` trực quan không? Blade template không thấy element đó rõ ràng | Chụp screenshot thực tế |
| 3 | `typeChange` và `HASH_ID` được dùng như thế nào trong flow đổi bot — chưa thấy rõ logic | Đọc controller và API `/admin/step2-check` |
| 4 | Modal「確認アカウントの承認」và「Owner Bot変更」— chi tiết UI chưa được phân tích | Include files: `admin.employee.modal-confirm-approve-invite-staff` và `modal-confirm-approve-change-owner-bot` |
| 5 | `/admin/step2-check-validate` và `/admin/check-enable-use-webhook` — response schema đầy đủ chưa rõ | Phân tích controller tương ứng |
| 6 | Khi `botIdChange` có giá trị (đổi bot thay vì thêm mới) — `saveStep1()` chạy 6 lần (step 1→6), logic từng step chưa rõ | Đọc controller `/ajax/admin/step1-change-new-bot` |
