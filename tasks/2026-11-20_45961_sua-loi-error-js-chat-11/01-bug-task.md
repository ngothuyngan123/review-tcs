# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#45961 — Sửa lỗi error JS chat 11` |
| Module / Màn hình | Chat 1:1 (`chat-v2.js`, màn `/basic/chat-v3`, Studio `SCR-CHT-01`) — bug tự detect từ hệ thống báo lỗi JS (liên kết `#45228` Chat11) |

## Mô tả bug (bản dịch tiếng Việt)

Ticket được tạo tự động từ hệ thống phát hiện lỗi JS phía khách hàng (ticket gốc `[#45228] Chat11`), gồm nhiều nhóm lỗi JS cùng xảy ra trên màn Chat 1:1:

1. **Lỗi `WindowOnError` — "Cannot convert undefined or null to object"**
   ```
   TypeError: Cannot convert undefined or null to object
       at hasOwnProperty (<anonymous>)
       at i (https://step.lme.jp/js/media/vue.min.js:6:584)
       at nt.O ［as set］ (https://step.lme.jp/js/media/vue.min.js:6:2725)
       at Object.success (https://step.lme.jp/js/chats/chat-v2.js?v=202611091942:1428:29)
       at i (https://step.lme.jp/js/jquery.min.js:2:28017)
       at Object.fireWith ［as resolveWith］ (https://step.lme.jp/js/jquery.min.js:2:28783)
       at A (https://step.lme.jp/js/jquery.min.js:4:1403
   ```
   URL: `https://step.lme.jp/basic/chat-v3?lastTimeUpdateFriend=0`
   Additional data: `{"source":"https://step.lme.jp/js/media/vue.min.js","lineno":"6","colno":"584"}`

2. **Lỗi `loadFriend_AJAX` — "AJAX Error: error"**
   ```
   Error: AJAX Error: error
       at Object.error (https://step.lme.jp/js/chats/chat-v2.js?v=202611091942:2922:37)
       at i (https://step.lme.jp/js/jquery.min.js:2:28017)
       at Object.fireWith ［as rejectWith］ (https://step.lme.jp/js/jquery.min.js:2:28783)
       at A (https://step.lme.jp/js/jquery.min.js:4:14060)
       at XMLHttpRequest.<anonymous> (https://step.lme.jp/js/jquery.min.js:4:16298)
   ```
   URL: `https://step.lme.jp/basic/chat-v3?lastTimeUpdateFriend=0`
   Additional data: `{"url":"/basic/chat/get-friends","page":"1","botIdCurrent":"92910","status":"0","statusText":"error","filterTypeFriend":"all","hasSearch":"false","listFriendCount":"0","responseText":null}`

3. **Lỗi `UnhandledPromiseRejection` — "Registration failed - could not retrieve the public key"** (Web Push)
   URL: `https://step.lme.jp/basic/chat-v3` — Additional data: `{"promise":"［object Promise］"}` — note gốc: `=> lỗi này k log`.

Trong quá trình điều tra (nhiều vòng fix, xem Journal), hệ thống `ai-exception detect-bug` còn tự gộp thêm nhiều nhóm lỗi JS **cùng nguyên nhân** vào ticket này (đã có người review xác nhận, không tạo ticket mới):
- `Can't find variable: EmptyRanges` (Safari nội bộ, `filename: undefined`)
- `_ is not defined` (dòng `chat-v2.js:1399`)
- `Cannot read properties of undefined (reading 'id')` (dòng `chat-v2.js:3381`)
- `Fancybox is not defined`
- `undefined is not an object (evaluating 'i(e,t)')` (dòng `chat-v2.js:1428`, cùng gốc lỗi 1)
- `［vee-validate］ Validating a non-existant field: "step_id_0"` — **Dev xác nhận (Journal #154799): lỗi có sẵn ở base, ngoài phạm vi ticket** (modal chọn action dùng chung `modal_select_action`)
- `loadFriend_AJAX` lặp lại với nhiều `botIdCurrent` khác (trang 1, trang 2, có/không search)
- `loadFriend_SKIPPED_PAGE` — bug Studio #5849/#5985 phát sinh **trong lúc fix** (xem mục Journal)
- `Failed to connect to MetaMask` (extension trình duyệt) — **không phải lỗi sản phẩm**, Dev xác nhận lọc bỏ ở vòng fix cuối
- `VeeValidate is not defined` (`friendlist/modal_filter_v2.js`)

⚠️ Đây là bug **được fix qua nhiều vòng lặp (9 round, tag D-1 → D-15)** vì mỗi vòng fix lại phát sinh case mới do hệ thống tự detect bắt tiếp hoặc do Dev/QA phát hiện thêm trong lúc test. Xem đầy đủ diễn biến ở mục Journal bên dưới — đây là input chính cho `03-dev-impact.md`.

## Steps to reproduce

<!-- Lấy từ Journal #156355 (Đỗ Quyên, 2026-11-19) — tái hiện lỗi 1 (TypeError gốc). -->

1. Mở màn Chat 1:1 (`/basic/chat-v3`) → F12 mở DevTools → Network throttle = **Slow 3G**.
2. Chọn một bạn bất kỳ ở vị trí thứ 2 trong danh sách (hoặc bạn có nhiều tin nhắn, để lịch sử tải chậm).
3. Ngay khi lịch sử đang tải, lập tức đổi dropdown loại bạn sang `非表示中` (hoặc gõ/xoá từ khoá tìm kiếm, hoặc đổi bộ lọc tag).

## Expected result

- Không có `TypeError: Cannot convert undefined or null to object` ở tab Console.
- Không gửi báo lỗi JS lên API `/api/notify-exception-chat11`.
- Danh sách bạn tải xong thì hội thoại đầu danh sách mới được tự chọn, lịch sử hiển thị đúng.
- Lỗi Web Push "Registration failed …", lỗi script nội bộ trình duyệt không có file (`EmptyRanges`...), lỗi nguồn extension (`MetaMask`...) **không** được báo; lỗi JS thật của trang (có file) **vẫn phải** được báo.
- `loadFriend_AJAX` không báo khi request bị huỷ do rời trang/reload; báo sau ~3s khi mất mạng; báo ngay khi lỗi có mã HTTP.

## Actual result

- Tab Console hiển thị `TypeError: Cannot convert undefined or null to object` (gốc tại `chat-v2.js:1428`, do `Vue.set(listFriend[index])` không kiểm `index = -1` khi hội thoại đang chọn không còn trong danh sách bạn sau khi đổi bộ lọc/tìm kiếm).
- Hệ thống tự động còn ghi nhận nhiều nhóm lỗi JS khác cùng xảy ra trên màn này (xem Mô tả bug).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [x] Có log / request-response — log lỗi JS nguyên văn trong Description + các journal `ai-exception detect-bug` (link dashboard từng nhóm lỗi, xem Journal).

(Redmine ghi `Attachments (0)` — không có file đính kèm thật, chỉ có log text trong Description/Journal.)

## Ghi chú thêm của Leader

- Ticket do hệ thống **tự detect** tạo (Tracker: `Bug tự detect`), không phải khách hàng report trực tiếp — không có thông tin "tần suất % user gặp" theo nghĩa thông thường, nhưng các journal `ai-exception detect-bug` có ghi "Số lần cảnh báo" / "Số user lỗi" cộng dồn khá lớn cho từng nhóm lỗi (vd nhóm `EmptyRanges` cộng dồn 286 lần, nhóm `loadFriend_AJAX` một biến thể cộng dồn 216 lần) — tất cả ghi `Số user lỗi: 0` (không chặn user thao tác, chỉ là lỗi JS/log).
- **JS chỉ có hiệu lực sau khi release tăng `sns-line.version`** (cache-busting `?v=`) — tester phải Ctrl+F5 khi verify trên môi trường đã release. Tính đến journal cuối (18/11), **production vẫn đang chạy bản chưa gộp nhánh fix** (`v=202611171542`) nên các lỗi đã fix (D-1…D-14) vẫn còn được báo trên prod cho tới khi release gộp nhánh + bump version.
- Có 1 quyết định nghiệp vụ của PIC ticket (TungKS) cần Leader xác nhận lại: bug Studio **#5805** (lẫn tin hội thoại cũ khi đổi bộ lọc/tìm kiếm lúc lịch sử đang tải) được chốt là **hành vi có sẵn ở base, chấp nhận không fix** (gỡ hẳn điều kiện D-5 ở vòng 6) — xem Journal #154799. Cần Leader xác nhận lại quyết định này trước khi chốt expected của TC liên quan.
- Testcase Studio **NEW-17** (báo lỗi tải danh sách bạn, kỳ vọng `loadFriend_SKIPPED_PAGE` khi trang lỗi) đã **lỗi thời** theo Dev (Journal #155776) vì hành vi mới (D-15, vòng 8) là lùi số trang khi lỗi → không còn `SKIPPED_PAGE`. Dev đề nghị Test Studio cập nhật lại kỳ vọng TC này.
- Nhiều "Việc cần làm thêm (ngoài phạm vi task)" Dev liệt kê qua các vòng — không fix trong ticket này, cân nhắc mở ticket riêng nếu Leader muốn theo dõi (đã liệt kê trong `03-dev-impact.md` mục 3 / Ghi chú).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id (ca lỗi gốc) | `92910` (lỗi `loadFriend_AJAX` đầu tiên trong Description) |
| bot_id (các ca lỗi khác ghi nhận qua journal `ai-exception`) | `171574`, `166736`, `88566`, `166175`, `196424`, `224691`, `8731`, `140049`, `64155`, `36549`, `191802` |
| URL lỗi | `https://step.lme.jp/basic/chat-v3?lastTimeUpdateFriend=0` (và các giá trị `lastTimeUpdateFriend` khác) |
| Thời điểm lỗi | Rải từ `2026-11-09` đến `2026-11-18` (nhiều lần, xem journal `ai-exception detect-bug`) |
| Đối chứng | Harness tái hiện của Dev: `evidence/tests/repro-45961-v8.js` (Journal #155714) — Dev dùng harness này để regression test qua các vòng |
| Testcase Studio liên quan trực tiếp (bug automation) | `#5805`, `#5806`, `#5807`, `#5814`, `#5849`, `#5985` (mã bug Test Studio, khác số ticket Redmine) |

## Journal / note từ Redmine (nguyên văn)

<!-- Chỉ chép các journal có nội dung điều tra/giá trị tham chiếu cho review; các journal "ai-exception detect-bug" tự động gộp nhóm lỗi trùng nguyên nhân (10 journal, #155642 → #155687) đã được tóm tắt vào mục "Mô tả bug" + "Dữ liệu định danh ca lỗi" phía trên để tránh trùng lặp, không chép nguyên văn toàn bộ. -->

**Journal #154537 — Dev Studio — 2026-11-13:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Lỗi 1: trong `refresh()` (chat-v2.js), khi lịch sử tin về, code tìm hội thoại đang chọn trong danh sách bạn rồi gọi `Vue.set(listFriend[index])` mà không kiểm index. Đổi bộ lọc hoặc tìm kiếm thì danh sách bị xoá để tải lại nhưng hội thoại đang chọn vẫn giữ, nên index = -1 và Vue 2.2.6 văng `Cannot convert undefined or null to object`. Lỗi 3: lệnh `pushManager.subscribe` trong layout chung không có catch, còn bộ lọc lỗi push của chat-v2.js không khớp thông điệp `Registration failed - could not retrieve the public key`. Lỗi 2: status 0 nghĩa là trình duyệt không nhận được response (trang đang rời đi hoặc mất mạng), và nhánh error của loadFriend gửi báo trong cả hai trường hợp.

Hướng sửa:
- D-1 refresh(): bỏ qua Vue.set khi hội thoại đang chọn không có trong danh sách bạn
- D-2 Không gửi báo lỗi đăng ký Web Push 'Registration failed - ...'
- D-3 loadFriend: không báo loadFriend_AJAX khi request bị huỷ vì trang đang rời đi

Ảnh hưởng / rủi ro:
Chỉ đổi JS của màn Chat 1:1 (chat-v2.js); API, DB và layout chung không đổi. Cần kiểm lại việc tải lịch sử khi đổi bộ lọc hoặc tìm kiếm, cuộn tải tin cũ, banner bạn bị chặn, và việc báo loadFriend vẫn hoạt động khi mất mạng hoặc server trả 5xx. Phần JS chỉ có hiệu lực khi release tăng version asset.
```

**Journal #154548 — Dev Studio — 2026-11-13 (handoff vòng 1):**

```
Dev handoff — 13/11 15:49 · nhánh ai_studio_fixbug_45961

Nội dung thay đổi:
- Chat 1:1, tải lịch sử tin: khi hội thoại đang chọn không có trong danh sách bạn (đang đổi bộ lọc hoặc tìm kiếm) thì không còn văng lỗi JS; trạng thái chặn, cờ đã xoá tin và tin hẹn giờ vẫn được cập nhật.
- Chat 1:1, báo lỗi JS: bỏ qua mọi lỗi "Registration failed …" của Web Push, không gửi báo.
- Chat 1:1, danh sách bạn: không gửi báo loadFriend_AJAX khi request bị huỷ do trang reload hoặc rời đi; mất mạng khi trang còn mở vẫn gửi báo.

File đã sửa (php-web):
  public/js/chats/chat-v2.js | 23 ++++++++++++++++++++---
  1 file changed, 20 insertions(+), 3 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi một file JS của màn Chat 1:1, thêm guard và điều kiện bỏ qua báo lỗi; không đổi API, DB hay layout chung.
- Hàm refresh() chạy mỗi lần chọn hội thoại và khi cuộn lên tải tin cũ: kiểm hiển thị lịch sử, banner chặn, cờ đã xoá tin.
- Bộ lọc unhandledrejection của chat-v2.js: các lỗi promise khác vẫn phải được báo.
- Hai listener mới beforeunload/pagehide nằm cạnh listener beforeunload sẵn có của socket (gửi stop-typing): chỉ đặt cờ, không chặn rời trang, không hiện hộp xác nhận.
- Nhánh lỗi của loadFriend: cơ chế ghi lastFailedFriendPage để báo trang bị bỏ qua (#45228) vẫn chạy.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).
Recover dữ liệu: Không cần recover — Cả 3 lỗi chỉ nằm ở trình duyệt (hiển thị và log chẩn đoán), không có thao tác ghi DB hay gửi tin nào bị bỏ sót.

Lưu ý khi deploy:
- JS chỉ có hiệu lực khi release tăng sns-line.version (cache-busting ?v=); tester cần Ctrl+F5.

Việc cần người làm thêm (ngoài phạm vi task):
- Cùng kiểu lỗi Vue.set(listFriend[index]) không kiểm -1 còn ở các thao tác khác của Chat 1:1: đổi trạng thái hội thoại (changeStatus, chat-v2.js ~2343/2380), đánh dấu đã đọc/chưa đọc (~4607), lưu thông tin bạn (~6189). Nên mở ticket riêng nếu muốn xử lý.
- layout/basic/header.blade.php và footer.blade.php gọi pushManager.subscribe không có catch, nên mọi màn đều có thể sinh unhandledrejection. Đây là cải tiến riêng cho layout chung.

Điểm cần test:
- Bật Slow 3G, chọn một bạn rồi lập tức đổi dropdown loại bạn, gõ tìm kiếm hoặc xoá bộ lọc: console không còn TypeError và không có POST /api/notify-exception-chat11; danh sách tải xong thì hội thoại đầu được chọn, lịch sử hiển thị đúng.
- Chọn bạn bình thường rồi cuộn lên đầu khung chat: tin cũ được nối đúng; bạn bị chặn vẫn hiện banner chặn, cờ đã xoá tin vẫn đúng.
- Chạy Promise.reject(new DOMException('Registration failed - could not retrieve the public key','AbortError')) trong console: không có POST báo lỗi. Chạy Promise.reject(new Error('test')): vẫn có POST UnhandledPromiseRejection.
- Bật Slow 3G, đang tải /basic/chat/get-friends thì bấm F5 hoặc confirm tất cả (trang reload): không có tin loadFriend_AJAX.
- Chuyển DevTools sang Offline rồi cuộn tải trang 2 danh sách bạn: vẫn có tin loadFriend_AJAX status 0. Cho get-friends trả 500: vẫn có tin.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit d6e3cb60f5083ef2e82bd0713a721a36aace849e)
```

**Journal #154615 — Dev Studio — 2026-11-13 (handoff vòng 2):**

```
Dev handoff — 13/11 17:35 · nhánh ai_studio_fixbug_45961

Nguyên nhân:
Đổi bộ lọc hoặc tìm kiếm thì danh sách bạn, lịch sử và số trang bị xoá nhưng hội thoại đang chọn vẫn giữ. Guard của `refresh()` chỉ so conversation_id nên response lịch sử cũ vẫn được áp dụng: trước đây nó gây TypeError của ticket, sau D-1 nó làm khung lẫn tin cũ (#5805). D-3 của vòng 1 bật cờ ở `beforeunload`, sự kiện này vẫn bắn khi điều hướng bị huỷ, và cờ không bao giờ được hạ (#5806). Nhánh error của `loadFriend` không hạ `isFetching`/`isLoadingSearch`, nên sau một lần lỗi tìm kiếm không tải lại danh sách (#5807).

Nội dung thay đổi:
- Chat 1:1, lịch sử tin: đổi loại bạn, tìm kiếm hoặc bộ lọc tag khi lịch sử đang tải thì không lỗi JS và không lẫn tin của hội thoại cũ; khung hiện lịch sử của hội thoại đầu danh sách mới.
- Chat 1:1, báo lỗi JS: bỏ qua lỗi Web Push "Registration failed …".
- Chat 1:1, báo lỗi tải danh sách bạn: request bị huỷ do trang reload hoặc rời đi thì không báo; mất mạng khi trang còn mở (kể cả sau một điều hướng bị huỷ hoặc khôi phục bằng Back) vẫn báo, chậm khoảng 3 giây; lỗi có mã HTTP báo ngay.
- Chat 1:1, danh sách bạn: sau khi get-friends lỗi vẫn tìm kiếm hoặc lọc lại được, không kẹt trạng thái đang tìm.

Bug automation Test Studio:
- Bug #5805 đã sửa (commit sns-line@847363b21341, sns-line@d6e3cb60f508): refresh() bỏ response lịch sử khi danh sách bạn đã bị tải lại (đổi loại bạn/tìm kiếm/bộ lọc), nên khung không còn lẫn tin hội thoại cũ. TypeError của base đã hết từ commit vòng 1.
- Bug #5806 đã sửa (commit sns-line@847363b21341): Bỏ cờ đặt ở beforeunload. Lỗi status 0 chờ 3 giây và chỉ bị bỏ khi trang thật sự bị ẩn (pagehide), nên sau một điều hướng bị huỷ (204) mất mạng vẫn được báo, đến sau khoảng 3 giây.
- Bug #5807 đã sửa (commit sns-line@847363b21341): Nhánh lỗi get-friends hạ cờ đang tải (isFetching, isLoadingSearch), nên sau lỗi 500, xoá từ khoá sẽ tải lại 20 hội thoại đầu.

File đã sửa (php-web):
  public/js/chats/chat-v2.js | 41 ++++++++++++++++++++++++++++++++++++-----
  1 file changed, 36 insertions(+), 5 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi một file JS của màn Chat 1:1, gồm guard và điều kiện bỏ qua báo lỗi; không đổi API, DB hay layout chung. Bước bỏ response cũ dựa trên việc mọi luồng reset danh sách đều gán mảng mới, reviewer đã rà và thấy đúng.
- refresh() chạy mỗi lần chọn hội thoại và khi cuộn lên tải tin cũ: kiểm lịch sử, banner chặn, cờ đã xoá tin, tin hẹn giờ, nhất là khi cuộn danh sách bạn trong lúc lịch sử đang tải.
- Các luồng reset danh sách bạn (tìm kiếm, dropdown loại bạn, lưu/xoá/đóng bộ lọc tag): sau khi reset phải tự chọn hội thoại đầu và hiện đúng lịch sử.
- Nhánh lỗi của loadFriend: cờ đang tải được hạ; cơ chế lastFailedFriendPage và báo trang bị bỏ qua (#45228) vẫn chạy.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).
Recover dữ liệu: Không cần recover — Tất cả chỉ là hiển thị và log ở trình duyệt, không có thao tác ghi DB hay gửi tin.

Việc cần người làm thêm (ngoài phạm vi task):
- Xoá hết từ khoá trong lúc get-friends đang chạy: pendingTerm rỗng bị coi là không có nên danh sách không tải lại (có sẵn ở base, ngoài phạm vi).
- Cùng kiểu lỗi Vue.set(listFriend[index]) không kiểm -1 còn ở luồng changeStatus và vài chỗ khác trong chat-v2.js.
- Layout chung gọi pushManager.subscribe không có catch, nên mọi màn đều có thể sinh unhandledrejection.

Điểm cần test:
- #5805: lịch sử chậm 3s, danh sách bạn chậm 8s; chọn hội thoại dòng 2 rồi trong vòng 1 giây đổi 「非表示中」 hoặc gõ/xoá từ khoá: không lỗi JS, không có notify, khung chỉ có tin của hội thoại đầu danh sách mới, tin mới nhất ở cuối.
- #5806: cho /basic/message-template trả 204, bấm 「テンプレート」, chặn get-friends page=2 rồi cuộn: có đúng 1 tin loadFriend_AJAX page=2 status=0 (sau khoảng 3 giây).
- Offline rồi cuộn tải trang 2: có tin. get-friends trả 500: có tin ngay. Bấm F5 hoặc confirm tất cả khi get-friends đang chạy: không có tin.
- #5807: get-friends trả 500 rồi gõ từ khoá: có tin báo, không chứa từ khoá. Bỏ lỗi rồi xoá từ khoá: 20 hội thoại đầu hiện lại, không kẹt trạng thái đang tìm.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit 847363b21341...)
```

**Journal #154643 — Dev Studio — 2026-11-16 (handoff vòng 3):**

```
Dev handoff — 16/11 09:08 · nhánh ai_studio_fixbug_45961

Nguyên nhân:
Bản vòng 2 chỉ dựa vào `pagehide`: request lỗi status 0 thì chờ 3 giây, rồi báo nếu trang chưa bị ẩn. Có trình duyệt huỷ request của trang cũ ngay khi bắt đầu điều hướng (sau `beforeunload`), còn `pagehide` chỉ chạy khi trang mới thay trang cũ. Trang đích phản hồi lâu hơn 3 giây thì timer chạy trước và gửi báo nhầm.

Nội dung thay đổi: (giữ như vòng 2, cộng:)
- Chat 1:1, báo lỗi tải danh sách bạn: rời trang hoặc reload trong lúc danh sách đang tải (kể cả khi trang đích chậm) thì không báo.

Bug automation Test Studio:
- Bug #5814 đã sửa (commit sns-line@7d3e3264b1e8): Request đang chạy mà trang bắt đầu rời đi (beforeunload) thì lỗi status 0 không được báo, dù trang đích chậm hay nhanh. Request gửi sau một điều hướng bị huỷ vẫn báo như #5806.

File đã sửa (php-web):
  public/js/chats/chat-v2.js | 52 +++++++++++++++++++++++++++++++++++++++++-----
  1 file changed, 47 insertions(+), 5 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi một file JS của màn Chat 1:1; vòng 3 chỉ thêm một điều kiện bỏ qua tin báo status 0; không đổi API, DB hay layout chung.
- Listener beforeunload và pagehide mới nằm cạnh listener beforeunload sẵn có của socket (stop-typing): chỉ tăng bộ đếm, không chặn rời trang, không hiện hộp xác nhận.

Điểm cần test:
- #5814: get-friends chậm 15 giây, trang 「テンプレート」 chậm 6 giây; trong lúc đang tải bấm 「テンプレート」: không có tin loadFriend_AJAX, kể cả ở trình duyệt huỷ request ngay khi bắt đầu điều hướng. Kiểm tương tự với F5.
- #5806 kiểm lại: cho /basic/message-template trả 204, bấm 「テンプレート」, chặn get-friends page=2 rồi cuộn: vẫn có đúng 1 tin page=2 status=0.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit 7d3e3264b1e807877e4beade8d890de19c8b32a4)
```

**Journal #154722 — Kieu Son Tung (PIC ticket) — 2026-11-16:** (bổ sung các lỗi JS mới phát hiện trong lúc test, cùng format Description — gồm `EmptyRanges`, `_ is not defined`, `Cannot read properties of undefined (reading 'id')`, `Fancybox is not defined`, `undefined is not an object`, `vee-validate step_id_0`, `loadFriend_AJAX` với `botIdCurrent=191802`.)

**Journal #154799 — Dev Studio — 2026-11-16 (handoff vòng 6):**

```
Dev handoff — 16/11 11:17 · nhánh ai_studio_fixbug_45961

Nguyên nhân:
Không có nguyên nhân mới: vòng này gỡ điều kiện so tham chiếu `listFriend` (mục D-5) theo yêu cầu của TungKS. TypeError dòng 1428 vẫn bị chặn nhờ phần kiểm `index > -1` (D-1). Khi không còn D-5, response lịch sử cũ lại được áp dụng sau khi đổi bộ lọc, nên hiện tượng lẫn tin cũ của base quay lại.

Nội dung thay đổi:
- Chat 1:1, lịch sử tin: đổi loại bạn, tìm kiếm hoặc bộ lọc tag khi lịch sử đang tải thì không còn lỗi JS (TypeError); hiển thị giữ như base (có thể lẫn tin cũ — đã chấp nhận).
- Chat 1:1, báo lỗi JS: bỏ qua lỗi Web Push "Registration failed …" và lỗi từ script nội bộ của trình duyệt không có file (vd EmptyRanges của Safari).
- Chat 1:1, hồ sơ người gửi: khi phiên bị đăng xuất (token đổi) thì không còn lỗi JS khi tải hồ sơ.
- API báo lỗi /api/notify-exception-chat11: tin Chatwork có thêm dòng "User agent" (tối đa 200 ký tự).

Bug automation Test Studio:
- Bug #5849 không phải bug: URL chat-v2.js?v=202611091942 không đổi vì fix bug không tự tăng version (quy ước dự án, việc của đội release), nên F5 thường dùng bản cache. Log của bug cho thấy bản sửa đã chạy. Re-test bằng Ctrl+F5 hoặc sau khi bản phát hành tăng version.

File đã sửa (php-web):
  app/Http/Controllers/Basic/ChatController.php |  2 +
  public/js/chats/chat-v2.js                    | 56 +++++++++++++++++++++++----
  2 files changed, 51 insertions(+), 7 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp:
- Bộ lọc lỗi JS (window.onerror, listener error, unhandledrejection): lỗi JS thật có file vẫn phải được báo.
- getBotProfile() gọi khi mở trang và sau khi thêm/sửa/xoá hồ sơ.
- Basic\ChatController::notifyExceptionChat11: nội dung tin Chatwork của room chat11.

Việc cần người làm thêm (ngoài phạm vi task):
- Bug Test Studio #5805 (lẫn tin hội thoại cũ khi đổi bộ lọc lúc lịch sử đang tải) sẽ fail lại. Cần trả lời là bỏ theo quyết định của TungKS ngày 16/11, vì đây là hành vi có sẵn ở base.
- Lỗi vee-validate step_id_0 trong modal chọn action dùng chung, và lỗi pendingTerm rỗng không tải lại danh sách, đều có sẵn ở base và nằm ngoài phạm vi; có thể làm ticket riêng.
- Sau khi lên production: dùng dòng User agent trong tin báo để chẩn đoán lỗi '_ is not defined' và 'Fancybox is not defined'.

Điểm cần test:
- Chọn hội thoại khi lịch sử tải chậm rồi đổi loại bạn hoặc tìm kiếm: không có TypeError và không có tin báo lỗi JS. Việc lẫn tin cũ là hành vi base đã chấp nhận.
- Vòng 5: lỗi EmptyRanges (filename 'undefined') không báo, lỗi JS thật vẫn báo; getBotProfile trả {success:false} không TypeError; tin Chatwork có dòng User agent.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit e71d3dc832a0916583c2f049527eb5c1dfaa4021)
```

**Journal #155702 — Dev Studio — 2026-11-18 (vòng 8, nguyên nhân):**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
MetaMask: bộ bắt unhandledrejection của chat-v2.js chỉ lọc lỗi push/permission, không lọc promise bị reject trong script của extension (stack bắt đầu bằng chrome-extension://), nên lỗi bị gửi vào Chatwork. SKIPPED_PAGE: khi cuộn tới đáy, handler tăng friendCurrentPage trước khi gọi loadFriend(), còn nhánh error không lùi số trang. Vì vậy lần cuộn sau xin trang N+1 và bạn của trang N không bao giờ được tải; nếu trang N+1 rỗng thì danh sách dừng hẳn (is_more_friend=false). Các lỗi đã sửa ở vòng trước vẫn được báo vì release đang chạy chưa gộp nhánh task.

Hướng sửa:
- D-14 Bỏ qua lỗi JS và promise reject có nguồn là extension trình duyệt (MetaMask…)
- D-15 loadFriend lỗi thì lùi số trang để lần cuộn sau tải lại đúng trang lỗi
```

**Journal #155714 — Dev Studio — 2026-11-18 (handoff vòng 8, đầy đủ):**

```
Dev handoff — 18/11 10:49 · nhánh ai_studio_fixbug_45961

Nội dung thay đổi:
- Chat 1:1, báo lỗi JS: bỏ qua lỗi Web Push 'Registration failed …', lỗi từ script nội bộ trình duyệt không có file (EmptyRanges của Safari) và lỗi có nguồn là extension trình duyệt (MetaMask…).
- Chat 1:1, danh sách bạn: sau khi get-friends lỗi vẫn tìm kiếm hoặc lọc lại được; trang tải thêm bị lỗi thì lần cuộn sau tải lại đúng trang đó, không mất bạn.

File đã sửa (php-web):
  app/Http/Controllers/Basic/ChatController.php |  2 +
  public/js/chats/chat-v2.js                    | 81 ++++++++++++++++++++++++---
  2 files changed, 76 insertions(+), 7 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Vòng 8 chỉ thêm điều kiện bỏ qua báo lỗi theo nguồn extension và một bước lùi số trang có điều kiện trong nhánh lỗi. API, DB và layout chung không đổi.
- Bộ lọc lỗi JS của toàn trang Chat 1:1 (window.onerror, listener error, unhandledrejection): lỗi thật của trang phải vẫn được báo.
- Cuộn tải thêm danh sách bạn (loadFriend và handler cuộn): số trang khi lỗi, khi cuộn nhanh, khi đổi bộ lọc hoặc tìm kiếm; tin loadFriend_SKIPPED_PAGE.
- 'Đánh dấu tất cả đã đọc' (changeConfirm) gửi page bằng số trang hiện tại, sau một trang lỗi có thể nhỏ hơn 1 đơn vị (luôn ≥ 1).

Migration / thay đổi dữ liệu: không có (đã kiểm diff).
Recover dữ liệu: Không cần recover — Cả hai lỗi chỉ ảnh hưởng tin chẩn đoán gửi từ trình duyệt và danh sách bạn đang hiển thị: không ghi DB, không có tin nào tới khách bị bỏ sót. Danh sách thiếu sẽ đủ lại khi người dùng tải lại trang.

Việc cần người làm thêm (ngoài phạm vi task):
- Release cần gộp nhánh ai_studio_fixbug_45961 và tăng sns-line.version. Bản đang chạy (v=202611171542) chưa có nhánh này, nên EmptyRanges, Registration failed và lỗi dòng 1428 vẫn còn được báo.
- Nếu hai request trang chạy song song mà request trước lỗi thì vẫn có thể nhảy trang như base. Thiết kế v8 đã chấp nhận rủi ro này; nếu muốn chặn thì cần một ticket riêng.

Điểm cần test:
- Unhandledrejection có frame đầu là chrome-extension:// (MetaMask) thì không có POST /api/notify-exception-chat11. Promise reject từ code chat-v2.js vẫn được báo.
- Bot có hơn 20 hội thoại: chặn page=2 rồi cuộn tới đáy thì có 1 tin loadFriend_AJAX. Bỏ chặn rồi cuộn lại: request là page=2, bạn 21–40 hiện đủ, không có SKIPPED_PAGE. Cuộn tiếp thì xin page=3.
- Regression: các harness v5 và v6 vẫn pass. Harness tái hiện evidence/tests/repro-45961-v8.js không còn báo MetaMask và lần cuộn thứ hai xin lại page 2.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit be42361322af53b8ff3e67ae784f8a872625a0f0)
```

**Journal #155776 — Dev Studio — 2026-11-18 (vòng 9 — không có commit mới, chỉ phản hồi bug Studio #5985):**

```
Dev handoff — 18/11 12:26 · nhánh ai_studio_fixbug_45961

Nguyên nhân:
Testcase NEW-17 của Test Studio vẫn kỳ vọng hành vi cũ: trang 2 lỗi thì lần cuộn sau nhảy sang trang 3 (rỗng) và gửi loadFriend_SKIPPED_PAGE. Vòng 8 (D-15) cố ý lùi số trang khi trang lỗi, nên lần cuộn sau xin lại trang 2. Không còn trang bị bỏ qua thì không còn tin SKIPPED_PAGE. Đây là testcase lỗi thời, không phải lỗi sản phẩm.

Không có commit mới so với lần bàn giao trước (18/11 10:49): nhánh giữ nguyên commit đã bàn giao.

Bug automation Test Studio:
- Bug #5985 không phải bug: Từ vòng 8 (D-15, theo yêu cầu TungKS ngày 18/11), trang bị lỗi được tải lại ở lần cuộn sau. Log lượt #7942: page=2 lỗi rồi được xin lại và nhận 200, sau đó mới tới page=3; chỉ có 1 tin loadFriend_AJAX, không trang nào bị bỏ sót nên không có SKIPPED_PAGE. Đề nghị đổi kỳ vọng NEW-17: page=2 được xin lại và nhận 200, đủ 30 hội thoại, không có SKIPPED_PAGE.

Việc cần người làm thêm (ngoài phạm vi task):
- Test Studio cần cập nhật testcase NEW-17 (Chat 1:1, báo lỗi tải danh sách bạn) theo hành vi mới: sau khi trang 2 lỗi, lần cuộn sau tải lại trang 2 và không còn tin loadFriend_SKIPPED_PAGE.

Điểm cần test:
- Làm theo các bước của #5985 (tìm 'QA61P2-', chặn page=2, cuộn, bỏ chặn, cuộn lại). Kết quả phải là: page=2 được xin lại và nhận 200, đủ 30 hội thoại, đúng 1 tin loadFriend_AJAX page 2, không có loadFriend_SKIPPED_PAGE.

Branch: ai_studio_fixbug_45961
- sns-line: ai_studio_fixbug_45961 (nhánh gốc release_step_20261106 @5badcb9a89f3, commit be42361322af53b8ff3e67ae784f8a872625a0f0 — giữ nguyên, không đổi)
```

**Journal #156355 — Đỗ Quyên — 2026-11-19 (tái hiện lỗi 1):**

```
Tái hiện:
1. Lỗi Cannot convert undefined or null to object
- chat 11 => f12: network chọn 3G
- chọn friend thứ 2 (hoặc friend nào nhiều tin nhắn)
- chọn ngay sang filter theo 非表示中
=> tab Console hiển thị lỗi TypeError: Cannot convert undefined or null to object.
```
