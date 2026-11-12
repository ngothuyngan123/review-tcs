# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42842 — [13-10-2026][T12401][App + API app] Khách không phát hành được API key trong màn hình liên kết API của L Message (báo "APIキーの発行に失敗しました"), danh sách key vẫn 0 mục.` |
| Module / Màn hình | Màn liên kết API (API連携) — mục "Về xác thực・API key／access token" (認証・APIキー／アクセストークンについて) — thao tác phát hành (発行) API key |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Ticket do khách hàng báo qua Slack (OEM) → WSSJ tạo lại trên Redmine, nội dung đã ở dạng tiếng Việt (không có block 原文 JP riêng — chỉ có <pre> JP là bản gốc câu hỏi tiếng Nhật của khách, không chép lại ở đây theo rule). -->

Tôi đang cố phát hành API key từ màn hình liên kết API của L Message nhưng key không được tạo và hiển thị "APIキーの発行に失敗しました". Cả khi đặt tên key bằng tiếng Nhật lẫn bằng chữ-số (nico-test-1day) đều cho kết quả giống nhau. Tôi đã thiết lập quyền hạn・thời hạn rồi thực hiện thao tác phát hành, nhưng danh sách key vẫn 0 mục. Mục đích dùng API key là kiểm tra khả năng liên kết với hệ thống đặt lịch・quản lý bệnh nhân đang dùng trong phòng khám. Trong phạm vi có thể xem trên màn hình thì không biết được HTTP status hay nội dung phản hồi của giao tiếp. Vui lòng hướng dẫn những điểm cần kiểm tra để điều tra và nguyên nhân không phát hành được API key.

Chức năng (theo ticket Slack): Về xác thực・API key／access token (認証・APIキー／アクセストークンについて)
Thời điểm khách phản hồi/báo lỗi: 2026/10/13 06:57:48

## Steps to reproduce

<!-- Không có bước tái hiện tường minh — khách chỉ kể lại thao tác đã làm (xem Mô tả bug). Support đã thử phát hành lại trên CÙNG account/bot và KHÔNG tái hiện được (Journal #143405). -->

## Expected result

-

## Actual result

-

⚠️ Bug KHÔNG tái hiện được — cả support (Journal #143405: "đã kiểm tra, phát hành API key bình thường được") và Dev (Journal #143744/#143820: "Không xác định được") đều không xác định được nguyên nhân gốc. Câu lỗi 「APIキーの発行に失敗しました」 là message mặc định của màn API連携 cho MỌI lỗi non-business (hết phiên, exception server, lỗi mạng) — không phân biệt được khách rơi vào trường hợp nào vì KHÔNG có log Laravel tương ứng. Dev fix KHÔNG sửa root cause (vì chưa biết root cause là gì) — chỉ bổ sung cơ chế ghi log + retry + báo Chatwork để **lần sau** có đủ thông tin chẩn đoán. TCs nên tập trung verify các cơ chế mới (retry, logging, báo lỗi Chatwork, phân biệt "trùng tên nhưng đã tạo" / "404 nhưng đã xoá" khi retry), KHÔNG thể verify "bug đã hết" vì nguyên nhân gốc chưa xác định.

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- スクリーンショット 2026-10-13 11.29.17.png — https://redmine.melonglobal.net/attachments/download/33133/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88%202026-10-13%2011.29.17.png

## Ghi chú thêm của Leader

- **Bug không tái hiện được** — xem cảnh báo ở section Actual result. Đây là ticket dạng "khách báo lỗi 1 lần, không lặp lại khi support test lại" — không có bằng chứng root cause nào khác ngoài suy luận của Dev.
- Tần suất: không rõ (chỉ 1 lần report, support test lại 2 lần (cả 2 account) đều KHÔNG lặp lại).
- Môi trường phát hiện: Production (khách hàng thật — `nicokotuban.jp@gmail.com`, bot `nico情報発信`, dashboard `https://dashboard.melonglobal.net/css-analytics/?id=T12401`).
- Mục đích khách dùng API key: kiểm tra khả năng liên kết với hệ thống đặt lịch・quản lý bệnh nhân của phòng khám (ngoài phạm vi của fix này — chỉ liên quan tới việc khách CÓ phát hành được key hay không).
- Ticket Slack nguồn: `管理番号 TY-12401` — Link item: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C8PCRH74J — Link thread: https://l-message.slack.com/archives/C0BALS7S73L/p1791846102361019
- Branch code: `ai_studio_fixbug_42842` (gốc `release_step_20260930_v2` @`c65e6e832037`, commit `d4bbc72274dc685138b769f8ba31066d4f7285f1`).
- **Follow-up Dev nêu rõ là CHƯA làm** (ngoài phạm vi task, xem Journal #143820):
  - Màn API連携 chưa phân biệt hết phiên (401 SESSION_EXPIRED) với lỗi server — vẫn hiện câu lỗi chung như cũ.
  - Lỗi JS ném ra trong method Vue chạy từ handler sự kiện bị Vue tự bắt, chỉ in `console.error`, KHÔNG tới `window.onerror` → D-4 (bắt lỗi JS) không bắt được loại lỗi này.
  - Nhánh "xoá key, lần thử lại nhận 404 ⇒ coi là thành công" bị làm **chặt hơn thiết kế gốc**: đòi thêm `error_code=resource_not_found` (vì Handler chung có thể trả 404 cho exception bất kỳ).
- **Lưu ý deploy** (từ Journal #143820): chạy `php artisan view:clear` (đổi Blade); bump `sns-line.version` để browser nạp `index.js` mới; queue worker connection `database` phải đang chạy (dùng chung báo lỗi booking event) thì tin Chatwork mới đi.
- Khi deploy xong mà khách gặp lại lỗi → Chatwork sẽ nhận tin `[API連携]` kèm HTTP status / error_code / chẩn đoán → mở lại điều tra, đối chiếu log Laravel dòng `'[#42842][API連携] client error'`.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | Không có số cụ thể trong ticket — chỉ có Bot Name: `nico情報発信` |
| Friend / User | User (email khách): `nicokotuban.jp@gmail.com` (tài khoản admin L Message, không phải LINE friend) |
| Đối tượng cấu hình | API key dự định phát hành — 2 lần thử: tên tiếng Nhật và tên `nico-test-1day` (cả 2 đều fail, đã thiết lập quyền hạn + thời hạn) |
| Thời điểm lỗi | 2026/10/13 06:57:48 (thời điểm khách phản hồi theo ticket Slack) |
| Đối chứng | Support (鈴木 隆宏) phát hành thử trên **cùng tài khoản + bot** của khách → **thành công** (Journal #143405); key test đã được xoá sau khi kiểm tra |

## Journal / note từ Redmine (nguyên văn)

**Journal #143375 — AI bug detect Lme — 2026-10-13:**

```
Comment slack ngày 2026-10-13 11:31:33

鈴木 隆宏
Chúng tôi đã xác nhận phát hành API key bình thường nên đã trả lời khách rồi. Có vẻ không cần điều tra.
```

**Journal #143405 — AI bug detect Lme — 2026-10-13:**

```
Comment slack ngày 2026-10-13 11:31:00

鈴木 隆宏（エルメサポート）
骨盤整体nico
Ông/Bà 橋崎

Cảm ơn quý khách đã luôn sử dụng エルメ.
Đây là bộ phận hỗ trợ エルメ.

Xin trả lời về nội dung quý khách đã hỏi.

■ Về việc không phát hành được API key
Sau khi bên chúng tôi kiểm tra, đã phát hành API key bình thường được.
Có khả năng đã xảy ra lỗi tạm thời, nên phiền quý khách xóa cache trình duyệt v.v. rồi kiểm tra phát hành lại API key giúp.

■ Về API key do bên chúng tôi phát hành thử
API key do bên chúng tôi phát hành thử để kiểm tra đã được xóa.
```

**Journal #143744 — Dev Studio — 2026-10-13:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
Không xác định được. Câu 「APIキーの発行に失敗しました」 là câu mặc định của màn API連携, hiện ra cho mọi lỗi không phải lỗi nghiệp vụ: hết phiên, exception phía server, hoặc lỗi mạng. Support phát hành thành công trên cùng tài khoản và bot, và không có log Laravel (TungKS xác nhận), nên không biết khách rơi vào trường hợp nào. Theo yêu cầu của TungKS, thiết kế bổ sung phần ghi log frontend và retry để lần sau chẩn đoán được.

Hướng sửa:
- D-1 Thêm route public nhận báo lỗi frontend của màn API連携
- D-2 Controller và service ghi log, chặn trùng, đẩy Chatwork qua job có sẵn
- D-3 Thêm bộ báo lỗi và thu thập chẩn đoán xhr ở JS của màn
- D-4 Bắt lỗi JS của riêng màn API連携 và báo Chatwork
- D-5 Tự gửi lại 1 lần sau 800ms khi request mất kết nối (status 0)
- D-6 Báo Chatwork mỗi khi màn phải hiện câu lỗi chung

Ảnh hưởng / rủi ro:
Thay đổi chỉ nằm ở màn API連携: JS, blade, controller, một service mới và một route public mới. Không đổi contract các endpoint hiện có, Handler hay job/helper dùng chung. Cần kiểm kỹ: retry khi phát hành/xoá không tạo trùng, chặn spam Chatwork, và không gửi API key trong báo lỗi.
```

**Journal #143820 — Dev Studio — 2026-10-13:**

```
Dev handoff — v1 · nhánh ai_studio_fixbug_42842

Nguyên nhân:
Không xác định được. Câu 「APIキーの発行に失敗しました」 là câu mặc định của màn API連携, hiện ra cho mọi lỗi không phải lỗi nghiệp vụ: hết phiên, exception phía server, hoặc lỗi mạng. Support phát hành thành công trên cùng tài khoản và bot, và không có log Laravel (TungKS xác nhận), nên không biết khách rơi vào trường hợp nào. Theo yêu cầu của TungKS, thiết kế bổ sung phần ghi log frontend và retry để lần sau chẩn đoán được.

Nội dung thay đổi:
- Màn API連携: mất kết nối khi tải danh sách key, bấm 👁, mở 操作履歴, phát hành hoặc xoá ⇒ tự thử lại 1 lần sau ~0.8s; nút giữ trạng thái khoá trong lúc chờ.
- Màn API連携 – phát hành: nếu lần thử lại báo trùng tên (lần đầu thực ra đã tạo key) ⇒ hiện lỗi trùng tên như cũ và tự tải lại danh sách để key hiện ra.
- Màn API連携 – xoá: nếu lần thử lại nhận 「対象のAPIキーが見つかりません」 (lần đầu đã xoá) ⇒ coi là xoá thành công.
- Màn API連携: mỗi lần hiện câu lỗi chung (発行/取得/表示/削除/操作履歴) ⇒ gửi báo lỗi vào log + Chatwork (chặn trùng 10 phút); lỗi JS của chính màn cũng được báo.
- API mới POST /ajax/api-integration/report-client-error: không cần đăng nhập, giới hạn 10 lần/phút, ghi log và đẩy job Chatwork qua queue database.

File đã sửa (php-web):
  .../Controllers/Basic/ApiIntegrationController.php |  27 ++
  .../ApiIntegration/ClientErrorReportService.php    | 101 +++++
  public/_assets/modules/api_integration/js/index.js | 446 +++++++++++++++++++--
  .../views/basic/api_integration/index.blade.php    |   5 +-
  routes/web.php                                     |   4 +
  .../ApiIntegrationClientErrorReportTest.php        | 159 ++++++++
  6 files changed, 711 insertions(+), 31 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đụng một màn, không đổi contract hay DB. Việc thử lại POST/DELETE đã được server khoá theo bot và trả đúng mã lỗi. Rủi ro chính là có thêm tin Chatwork và nguyên nhân gốc vẫn chưa được sửa.
- Toàn bộ thao tác của màn API連携 (danh sách, tìm kiếm/lọc, 👁, phát hành, xoá, 操作履歴): mọi request đã chuyển sang hàm có thử lại ⇒ cần test luồng bình thường, lỗi nghiệp vụ, đổi bộ lọc liên tục.
- Job SendJsErrorToChatwork và room Chatwork báo lỗi JS (dùng chung với báo lỗi của màn đặt lịch event): sẽ có thêm tin 「[API連携]」.
- Throttle: endpoint mới dùng chung bộ đếm (theo user khi đã đăng nhập) với 👁 hiện key (30 lần/phút) và với endpoint báo lỗi booking event.
- routes/web.php: thêm 1 route nằm ngoài nhóm cần đăng nhập, cạnh route báo lỗi booking ⇒ kiểm tên route không trùng.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Mỗi lượt phát hành chạy trong một transaction nên lần lỗi không ghi gì vào DB; không có dữ liệu hỏng hay bị bỏ sót. Khách chỉ cần phát hành lại.

Lưu ý khi deploy:
- Chạy php artisan view:clear (có đổi Blade).
- Tăng sns-line.version theo quy trình release để trình duyệt nạp index.js mới.
- Queue worker connection database phải đang chạy (đã dùng cho báo lỗi booking event).

Việc cần người làm thêm (ngoài phạm vi task):
- Báo khách (qua support) là chưa xác định được nguyên nhân. Nếu gặp lại, bản cập nhật này sẽ tự gửi lỗi về Chatwork; nhờ khách ghi lại thời điểm để đối chiếu.
- Deploy: queue `database` cần có worker đang chạy thì tin Chatwork mới đi (cùng điều kiện với booking event); chạy `php artisan view:clear`; không bump version JS nên tester phải Ctrl+F5 màn API連携.
- Tester kiểm theo các điểm kiểm thử của docs/design/v1.md: tắt mạng bằng DevTools rồi phát hành/xoá/xem danh sách, xoá cookie phiên rồi phát hành, lặp cùng một lỗi trong 10 phút. Dùng bot test; tin sẽ vào room Chatwork thật của team.
- Lỗi ném ra trong method Vue chạy từ handler sự kiện bị Vue tự bắt và chỉ in ra console.error, nên không tới window.onerror. Theo đúng thiết kế, D-4 không bắt được loại lỗi này; muốn bắt thì cần một thiết kế bổ sung (ví dụ errorCaptured ở root).
- Khi xoá, nhánh 'lần thử lại nhận 404 thì coi là thành công' được làm chặt hơn thiết kế, vì Handler chung có thể trả 404 cho exception bất kỳ.
- Cải tiến riêng (follow-up cũ): màn API連携 chưa phân biệt hết phiên (401 SESSION_EXPIRED) với lỗi server, vẫn hiện câu lỗi chung như cũ.
- Khi Chatwork nhận tin [API連携] từ khách gặp lại lỗi: mở lại điều tra #42842 bằng HTTP status/error_code/chẩn đoán trong tin, đối chiếu log Laravel (dòng '[#42842][API連携] client error').
- Có thể tách bộ đếm throttle của các endpoint báo lỗi public (API連携, booking event) khỏi các route throttle khác: Laravel 5.5 khoá throttle theo user/IP, không theo route.

Điểm cần test:
- Ngắt mạng rồi bấm 「発行する」: request được gửi 2 lần, cách nhau khoảng 0,8 giây; vẫn hỏng thì hiện câu lỗi cũ, có 1 log info và 1 log error, Chatwork nhận đúng 1 tin [API連携].
- Lần 1 mất mạng, lần 2 thông: phát hành thành công, chỉ có log info, không có tin Chatwork.
- Hết phiên (xoá cookie phiên) rồi phát hành: câu lỗi như cũ; endpoint báo lỗi vẫn nhận được và Chatwork có tin kèm SESSION_EXPIRED.
- Trùng tên, quá 10 key, tên rỗng: message như cũ, không gọi endpoint báo lỗi.
- Cùng một lỗi lặp lại trong 10 phút: chỉ 1 tin Chatwork. Quá 10 request/phút/IP: endpoint trả 429, màn không bị ảnh hưởng.
- Lần thử lại của phát hành nhận name_duplicated: hiện lỗi inline và danh sách tải lại có key mới; không có 2 key.
- Xoá key khi mất mạng ở lần 1, lần 2 nhận 404: hiện thành công và key biến khỏi danh sách.
- Danh sách key, 👁 và 操作履歴 khi mất mạng: retry 1 lần. Danh sách bị timeout 10 giây: không retry.
- Lỗi JS từ script khác trên trang: không báo. Lỗi trong JS của màn API連携: báo.
- Báo lỗi không chứa full API key (kiểm nội dung log và tin Chatwork).
- DevTools Offline rồi bấm 「発行する」: request phát hành đi 2 lần cách nhau ~0.8s, nút vẫn khoá; nếu vẫn hỏng thì hiện câu lỗi cũ và Chatwork nhận đúng 1 tin 「[API連携] フロントエンドエラー」 (action: issue, status=0, retried=1).
- Offline ở lần 1, bật mạng lại trước lần 2 ⇒ phát hành thành công, không có tin Chatwork.
- Response phát hành bị mất sau khi server đã tạo key ⇒ lần thử lại hiện lỗi trùng tên dưới ô tên, danh sách tự tải lại và key mới hiện ra.
- Hết phiên rồi bấm phát hành ⇒ màn hiện câu lỗi như cũ; Chatwork nhận tin có SESSION_EXPIRED hoặc status 401.
- Trùng tên, quá 10 key, tên rỗng hoặc quá 50 ký tự ⇒ thông báo như cũ, không có request tới /ajax/api-integration/report-client-error.
- Cùng một lỗi lặp lại nhiều lần trong 10 phút ⇒ chỉ có 1 tin Chatwork.
- Xoá key: offline ở lần 1, lần 2 nhận 404 ⇒ toast 「APIキーを削除しました」 và key biến khỏi danh sách.
- Danh sách / 👁 / 操作履歴 khi offline ⇒ thử lại 1 lần; danh sách treo tới timeout 10s ⇒ không thử lại, hiện 「APIキーの取得がタイムアウトしました」.
- Đổi bộ lọc trong lúc danh sách đang chờ thử lại ⇒ chỉ request mới chạy, không có tin báo cho request cũ.
- Lỗi JS từ script khác trên trang (header/layout) ⇒ không báo.
- Tin Chatwork và laravel.log không chứa full API key.

Branch: ai_studio_fixbug_42842
- sns-line: ai_studio_fixbug_42842 (nhánh gốc release_step_20260930_v2 @c65e6e832037, commit d4bbc72274dc685138b769f8ba31066d4f7285f1)
```

<!-- Journal #144580 (AI bug detect Lme, 2026-10-15) bị bỏ qua — chỉ đổi status Slack sang "クローズ待ち", không có giá trị điều tra. -->
