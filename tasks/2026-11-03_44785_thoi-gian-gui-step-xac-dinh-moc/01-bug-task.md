# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44785 — [30-10-2026][TY-12569] Thời gian gửi Step配信 được xác định dựa trên mốc thời gian nào?` |
| Module / Màn hình | `Step配信 (ステップ配信) — 友だち詳細 tab 「配信」 › ステップ配信 › 「手動変更」 (đăng ký lại chính kịch bản đang chạy từ N日目). Liên quan thêm: mypage cũ, panel phải màn chat 1:1チャット, 友だちリスト 一括アクション「途中から配信」, action/tag khởi động lại Step配信, API nội bộ start-scenario-api, Scenario legacy method=1, Job gửi ステップ配信, bộ lọc ステップ経過日数.` |

## Mô tả bug (bản dịch tiếng Việt)

support@keizaikeiei.jp

Có vẻ như thời gian gửi của Step配信 bị thay đổi khi thực hiện thao tác đăng ký bằng cách thay đổi thủ công (手動変更で登録).
Thời gian gửi Step配信 được xác định dựa trên mốc thời gian nào? Nhờ anh/chị xác nhận giúp về cơ chế hoạt động này.

- Friend: 中ジョー
- Link item Slack (OEM — 管理番号 TY-12569): https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0CDHB4J1LH

<!-- Bản dịch task (AI) từ Journal #149851 — dẫn chiếu thêm context: -->
Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12569. 担当 phía OEM: 筒井 和紀. Email khách: support@keizaikeiei.jp. Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1793336868417239

## Steps to reproduce

<!-- Theo Journal #150217 — Đỗ Quyên (tái hiện bug): -->
1. Scenario có 2 step: `128日後 — 08:00` và `158日後 — 10:00`.
2. Start scenario cho friend.
3. Mở 友だち詳細 → tab 「配信」 → ステップ配信 → 「手動変更」.
4. Chọn lại chính scenario đang chạy.
5. Chọn 「登録されている配信時刻・経過時間」, nhập `128`.
6. Save.

(Điều kiện bug xảy ra: thực hiện bước 6 **sau** giờ 08:00 — tức sau giờ gửi của bước 128日後.)

## Expected result

- Lấy **00:00 ngày hôm sau** làm mốc bắt đầu (`start_datetime`) → step `128日後 — 08:00` được lên lịch vào **hôm sau** đúng giờ 08:00, step `158日後 — 10:00` dời theo tương ứng.

## Actual result

- Step `128日後 — 08:00` bị **bỏ qua** do hệ thống lưu mốc bắt đầu là thời điểm bấm (`Carbon::now()`) — lúc đó giờ 08:00 của ngày 128 đã qua trong ngày → step bị đánh status 5 (không tạo lịch), bước kế tiếp (158日後) bị tính sớm 1 ngày so với kỳ vọng.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response

- `20261029 LINE問合せ (1).pdf` — https://redmine.melonglobal.net/attachments/download/38216/20261029%20LINE%E5%95%8F%E5%90%88%E3%81%9B%20(1).pdf

## Ghi chú thêm của Leader

- Bug không do khách hàng report trực tiếp trên Redmine mà do OEM (筒井 和紀 — 管理番号 TY-12569) ghi nhận qua Slack, AI dịch lại task vào Redmine (Journal #149851).
- Đây là lỗi **có điều kiện xác định** (deterministic theo thời điểm thao tác), không phải lỗi xác suất ngẫu nhiên: chỉ xảy ra khi "đăng ký lại cùng kịch bản đang chạy từ ngày N" được thực hiện **sau** giờ gửi cố định của bước ngày N trong ngày hôm đó.
- Môi trường phát hiện: không ghi rõ trong Redmine — bug nằm ở logic tính ngày giờ trong `ChatMessages::changeScenario`, không gắn riêng 1 môi trường.
- ⚠️ Dev **quyết định KHÔNG recover dữ liệu** đã lệch lịch trước khi fix (xem chi tiết ở `03-dev-impact.md` — mục Recover dữ liệu). Bạn bè `中ジョー` bị ảnh hưởng (bước 128日後 đã bị bỏ) sẽ **không được tự sửa lại** sau deploy — nếu khách cần, phải tự 手動変更 lại.
- Việc Support trả lời khách TY-12569 (giải thích cơ chế tính ngày gửi) và việc file riêng cho lỗi fatal có sẵn ở `tests/Feature/ContractExpireServiceTest.php` là **ngoài phạm vi task test** này (theo Dev ghi ở Journal #150208).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ — tra thêm trên Redmine/Studio nếu cần>` |
| Friend | `中ジョー` |
| Đối tượng cấu hình | Scenario Step配信 có 2 bước: `128日後 — 08:00` và `158日後 — 10:00` |
| Thời điểm lỗi | Thao tác `手動変更` đăng ký lại chính kịch bản từ ngày 128, thực hiện **sau** 08:00 (giờ gửi của bước 128日後) |
| Đối chứng | Theo Journal #150208: cùng thao tác thực hiện **trước** 08:00 → không bug (`start_datetime` = lúc bấm, bước 128 gửi đúng hôm nay) |

## Journal / note từ Redmine (nguyên văn)

**Journal #149851 — AI bug detect Lme — 2026-10-30:**
```
h3. Bản dịch task (AI) — TY-12569

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ) — 管理番号 TY-12569
担当: 筒井 和紀
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1793336868417239
Item list: https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0CDHB4J1LH

Có vẻ như khi đăng ký bằng thao tác thay đổi thủ công (手動変更) Step配信 thì ngày giờ gửi bị lệch. Vậy ngày giờ gửi của Step配信 được xác định dựa trên mốc nào theo spec?
Bạn bè: 中ジョー

(担当 OEM: 筒井 和紀 — email khách: support@keizaikeiei.jp)

---
h3. 原文 (JP)
<pre>https://l-message.slack.com/lists/T01H7J4Q5M1/F08DACWUDMM?record_id=Rec0CDHB4J1LH

No.12569

筒井 和紀

support@keizaikeiei.jp

ステップ配信の手動変更で登録で配信日時がずれてしまうようですが、こちらは何を基準にステップ配信日時が決まる仕様になりますでしょか？
友だち：中ジョー</pre>
```

**Journal #150184 — Do Van Tu TuDV — 2026-11-03:**
```
1. Nguyên nhân là bug ở nhánh "đăng ký lại cùng step": mốc 00:00 ngày mai đã được tính ra nhưng không được ghi vào start_datetime.

- Nếu muốn có thêm bằng chứng để gửi khách, có thể xem bản ghi lúc đăng ký trong bảng history. Bản ghi này phải có start_day = 128, start_time = 00:00:00, start_datetime = 17:43:54

2. Hướng sửa đề xuất
- Trong nhánh cùng step, ghi start_datetime bằng mốc đã tính, giống cách nhánh khác step đang làm (ChatMessages.php:2733). Nên rà luôn nhánh không có start_day/start_time (今すぐ) ở dòng 2570-2585 để hai nhánh cho kết quả giống nhau
```

**Journal #150190 — Dev Studio — 2026-11-03:**
```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Trong `ChatMessages::changeScenario`, nhánh đăng ký lại vào chính kịch bản đang chạy với số ngày N tính đúng mốc bắt đầu `$start_datetime` (00:00 hôm sau nếu bước giờ cố định của ngày N đã quá giờ) nhưng lại lưu `start_datetime = Carbon::now()`. Khi lên lịch, bước ngày N có giờ gửi đã qua nên bị đánh status 5 và không được tạo lịch, bước kế tiếp tính từ hôm nay nên sớm 1 ngày. Lỗi do commit 89c279b5e5a (06/05/2026) đưa vào, commit 8e5ed2db273 sửa sót nhánh này; có từ release_staging_20260527.

Hướng sửa:
- D-1 Lưu đúng mốc bắt đầu đã tính khi đăng ký lại vào chính kịch bản đang chạy với N日目

Ảnh hưởng / rủi ro:
Ảnh hưởng mọi lối đăng ký lại vào chính kịch bản đang chạy có số ngày: 友だち詳細 mới, mypage cũ, panel phải màn chat, action/tag/API truyền start_day. Đổi sang kịch bản khác và chế độ 今すぐ không đổi. Dữ liệu đã lỗi trước đó giữ nguyên.
```

**Journal #150208 — Dev Studio — 2026-11-03:**
```
Dev handoff — 03/11 10:26 · nhánh ai_studio_fixbug_44785

Nguyên nhân:
Trong `ChatMessages::changeScenario`, nhánh đăng ký lại vào chính kịch bản đang chạy với số ngày N tính đúng mốc bắt đầu `$start_datetime` (00:00 hôm sau nếu bước giờ cố định của ngày N đã quá giờ) nhưng lại lưu `start_datetime = Carbon::now()`. Khi lên lịch, bước ngày N có giờ gửi đã qua nên bị đánh status 5 và không được tạo lịch, bước kế tiếp tính từ hôm nay nên sớm 1 ngày. Lỗi do commit 89c279b5e5a (06/05/2026) đưa vào, commit 8e5ed2db273 sửa sót nhánh này; có từ release_staging_20260527.

Hướng sửa:
- D-1 Lưu đúng mốc bắt đầu đã tính khi đăng ký lại vào chính kịch bản đang chạy với N日目

Nội dung thay đổi:
- 友だち詳細 (タブ ステップ → 手動変更), mypage cũ và panel phải màn chat: chọn lại chính kịch bản đang 配信中 với N日目 sau giờ của bước ngày N thì bước ngày N gửi ngày mai đúng giờ, scenario_lineuser.start_datetime = ngày mai 00:00:00 (trước đây = lúc bấm và bước ngày N bị bỏ).
- Lịch sử kịch bản (scenario_lineuser_history): dòng mới ghi đúng mốc start_datetime nói trên.

File đã sửa (php-web):
  app/Helpers/ChatMessages.php                       |  3 +-
  .../ChangeScenarioSameScenarioStartDayTest.php     | 91 ++++++++++++++++++++++
  2 files changed, 92 insertions(+), 2 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi một biến trong một nhánh để dùng lại công thức đã có ở nhánh đổi sang kịch bản khác. Không có migration, không đổi API hay UI.
- Mọi lối gọi changeScenario với chính kịch bản đang chạy kèm start_day/start_time (友だち詳細 mới, mypage_v2 cũ, panel chat, action/tag/API truyền start_day) đều đổi theo vì dùng chung một nhánh code.
- Lịch gửi scenario_step_time do createOrUpdateScenarioStepTimeByStartScenario tính từ start_datetime: cần kiểm tra 次回配信 và các bước sau.
- Đổi sang kịch bản khác và chế độ 今すぐ配信する: code không đổi, kết quả phải giữ nguyên.
- Bước kiểu 経過時間 (H時間M分後) tính từ updated_at, không phụ thuộc start_datetime, nên không đổi.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).

Recover dữ liệu: Không cần recover — Có dữ liệu bị ảnh hưởng (bước ngày N không được gửi), nhưng người phụ trách Tu quyết định ngày 03/11/2026 chỉ sửa code, không gửi bù và không chạy script recover.

Việc cần người làm thêm (ngoài phạm vi task):
- Support trả lời khách TY-12569 về mốc tính ngày gửi (bản nháp tiếng Nhật ở docs/investigation/v1.md mục 6). Báo thêm đây là lỗi đang sửa và với 中ジョー bước 128日後 đã bị bỏ; khách tự đăng ký lại nếu cần.
- tests/Feature/ContractExpireServiceTest.php có sẵn lỗi fatal (anonymous class chưa implement đủ BotRepositoryInterface), làm cả bộ PHPUnit dừng giữa chừng. Nên sửa trong một ticket riêng.
- Trả lời khách qua OEM (TY-12569): giải thích cơ chế tính ngày gửi Step配信 (docs/investigation/v1.md mục 8) và báo rằng lịch của bạn bè 中ジョー đã lệch trước bản sửa sẽ không được tự sửa lại (đã quyết định không recover). Nếu khách cần thì hướng dẫn khách 手動変更 lại sau khi deploy.

Điểm cần test:
- Bạn bè đang 配信中 kịch bản có bước 128日後08:00 và 158日後10:00. Sau 08:00, 手動変更 chọn lại chính kịch bản đó với 128日目: bước 128 gửi ngày mai 08:00, bước 158 gửi ngày mai + 30 ngày 10:00, start_datetime = ngày mai 00:00:00.
- Cùng thao tác trước 08:00: bước 128 gửi hôm nay 08:00, start_datetime = lúc bấm.
- Ngày N không có bước giờ cố định: mốc = lúc bấm, lịch không đổi so với trước.
- Đổi sang kịch bản khác với N日目: kết quả không đổi so với trước.
- 今すぐ配信する trên chính kịch bản: không đổi so với trước.
- Thử lại từ panel phải màn chat và mypage cũ.
- Dòng scenario_lineuser_history mới ghi đúng start_datetime đã lưu.
- Kịch bản có bước 「128日後 08:00」 và 「158日後 10:00」, bạn bè đang 配信中. Sau 08:00, 手動変更 chọn lại chính kịch bản, 128日目から: 次回 = ngày mai 08:00, bước 158 = ngày mai + 30 ngày 10:00, start_datetime = ngày mai 00:00:00.
- Làm cùng thao tác trước 08:00: bước 128 gửi hôm nay 08:00, start_datetime = lúc bấm.
- Ngày N không có bước giờ cố định: mốc = lúc bấm, lịch gửi như trước.
- Ngày N có bước 08:00 và 20:00, bấm lúc 17:00: cả hai bước dời sang ngày mai (quy tắc sẵn có).
- Đổi sang kịch bản khác với N日目, cùng giờ: kết quả như trước và giống case đầu.
- Lặp case đầu qua panel phải màn chat và mypage cũ (nếu còn dùng).
- Dòng mới trong scenario_lineuser_history có start_datetime khớp với scenario_lineuser.

Branch: ai_studio_fixbug_44785
- sns-line: ai_studio_fixbug_44785 (nhánh gốc release_step_20260930_v2 @79380b16eeec, commit d4333b125bb197f92b14a9e48a2a969b23759f2d)
```

**Journal #150217 — Đỗ Quyên — 2026-11-03:**
```
Tái hiện:
1. Scenario có 2 step:
- 128日後 — 08:00
- 158日後 — 10:00

2. Start scenario cho friend
3. Mở 友だち詳細 → tab 「配信」 → ステップ配信 → 「手動変更」.
4. Chọn lại chính scenario đang chạy
5. Chọn 「登録されている配信時刻・経過時間」, nhập 128
6. Save

Hiện tại: step 128日後 — 08:00 bị bỏ qua do hiện tại đã quá giờ
Expect: Lấy 00:00 ngày hôm sau làm mốc bắt đầu nên step 128日後 — 08:00 sẽ được lên lịch vào hôm sau
```
