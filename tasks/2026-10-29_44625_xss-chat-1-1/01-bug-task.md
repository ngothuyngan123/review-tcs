# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#44625 — Lỗi XSS ở chat 1-1` |
| Module / Màn hình | Chat 1:1 PC (`/chat-v3`) · chat 1:1 mobile (`/chat-mobile/{id}`) · talk list (`/talk-list`) · danh sách tin lỗi v2 (`/error-list-v2`) · chat nhóm (`/chat-v3` bộ lọc 「グループ」) · chi tiết tin lỗi (`/basic/error-list-setting/{id}`) — khâu render tin text thành link |

## Mô tả bug (bản dịch tiếng Việt)

Lỗ hổng XSS ở màn chat 1-1. Hàm biến URL trong tin nhắn thành link (`showMessageText`) ghép link kiểu `href=` + URL mà **không bọc nháy**. Ngoài ra hàm lại tìm URL **sau khi đã escape**. Regex cho link `line.me/R/ti/p/%40…` chỉ dừng ở dấu cách thường hoặc xuống dòng, nên khi gặp **tab (TAB)** hay **NBSP** thì nó khớp luôn phần phía sau. Trình duyệt sau đó tách phần `href` không có nháy thành các attribute mới (`style=animation:spin`, `onanimationstart=fetch(...)`) rồi chạy đoạn JS đó qua `v-html`.

Đoạn code lỗi này bị copy ra 6 chỗ:
- Chat 1-1 trên PC: `chat-v2.js` (gồm `showMessageText` và phần preview).
- Màn chat cũ: `chat.js`.
- Chat 1-1 trên mobile: `mobile/chat.js` — chỗ này **trước đây không escape gì cả**, nên chỉ cần gửi một thẻ `<img onerror>` thông thường là JS đã chạy.
- `talk_list/index.js` và `error_list/index_v2.js`.
- Hàm `displayMessageFromData` trong `common.js`, dùng cho chat nhóm và màn chi tiết lỗi (cũng không escape).

## Steps to reproduce

1. Mở chat 1:1 PC (`/chat-v3`) của bot test.
2. Khách gửi tin text: `https://line.me/R/ti/p/%40abc` + **TAB** + `style=animation-name:spin;animation-duration:1s` + **TAB** + `onanimationstart=alert(1)`.
3. Quan sát khi tin được render.
4. Lặp lại với **CR** thay cho TAB; và với payload `<img src=x onerror=alert(1)>` (đặc biệt ở chat mobile / chat nhóm / chi tiết tin lỗi — các màn trước đây không escape).

## Expected result

- Tin hiện **nguyên thành chữ**, ký tự đặc biệt không bị diễn giải thành HTML.
- Không có popup/JS nào chạy (`alert(1)` không xuất hiện).
- Phần link chỉ gồm URL hợp lệ, vẫn bấm được.

## Actual result

- Trình duyệt tách `href` không bọc nháy thành attribute mới → đoạn JS (`onanimationstart=alert(1)`, `onerror=alert(1)`) **chạy**.

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #44625 không có attachment. -->

## Ghi chú thêm của Leader

- Môi trường phát hiện: (tra trên Redmine khi cần — ticket không ghi rõ).
- **Bug có thể tái hiện được** bằng payload ở Steps to reproduce; không phải lỗi xác suất.
- **Sau deploy phải hard-reload (Ctrl+F5)** vì có hàm mới `linkifyMessageText` trong `common.js` — browser phải nạp `common.js` mới cùng lúc với các file JS trang (bump `config/sns-line.php` version).
- Payload XSS có thể đã tồn tại trong DB production (tin text chứa `line.me` kèm tab/CR/FF hoặc thẻ `<img/svg on...=>`) → Dev đề nghị đội bảo mật rà DB (ngoài phạm vi task test này).
- 2 việc ngoài phạm vi task (Dev đề nghị mở ticket riêng): (a) màn chat nhóm cũ `/basic/chat/group` trắng trang từ 2022 (bug #4822, `ReferenceError checkFriend`, không liên quan commit này); (b) IDOR ở `/basic/error-list-setting/{id}` (đọc/đổi trạng thái tin theo id không lọc `bot_id`).

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| Payload tấn công 1 (regex) | `https://line.me/R/ti/p/%40abc` + TAB + `style=animation-name:spin;animation-duration:1s` + TAB + `onanimationstart=alert(1)` (và biến thể dùng CR/FF/NBSP) |
| Payload tấn công 2 (không escape) | `<img src=x onerror=alert(1)>` |
| Đối chứng (hồi quy) | Link thường · link có `?a=1&b=2` · link rút gọn hiện `[...(短縮)]` · nhiều link trong 1 tin · xuống dòng · emoji/tiếng Nhật · tin cũ có `&nbsp;` / `&amp;` · biến `{name}` |

## Journal / note từ Redmine (nguyên văn)

**Journal #149123 — Dev Studio — 2026-10-27:**

```
Dev Studio · Nguyên nhân & hướng sửa

Nguyên nhân:
Hàm `showMessageText` (chat 1:1 PC) và các bản sao dựng thẻ `<a ... href=` + URL + `>` mà không bọc nháy. Nhánh regex cho link `line.me/R/ti/p/%40…` chỉ dừng ở dấu cách thường hoặc xuống dòng, nên khi gặp tab/CR/FF nó khớp luôn phần phía sau, và trình duyệt tách phần đó thành attribute mới (`style`, `onanimationstart`…) rồi chạy JS qua `v-html`. Hai bản sao `displayMessageFromDataMB` (chat 1:1 mobile) và `displayMessageFromData` (chat nhóm, chi tiết tin lỗi) còn không escape gì, nên chỉ cần gửi `<img onerror>` là JS chạy.

Hướng sửa:
- D-1 Thêm hàm chung linkifyMessageText vào common.js
- D-2 chat-v2.js: showMessageText và showPreviewMessageText gọi hàm mới
- D-3 talk_list/index.js: showMessageText gọi hàm mới
- D-4 error_list/index_v2.js: showMessageText gọi hàm mới
- D-5 common.js: displayMessageFromData nhánh text gọi hàm mới
- D-6 mobile/chat.js: displayMessageFromDataMB nhánh text gọi hàm mới

Ảnh hưởng / rủi ro:
Chỉ sửa JS hiển thị tin text ở chat 1:1 PC/mobile, talk list, danh sách tin lỗi v2, chat nhóm và chi tiết tin lỗi; không đổi PHP, API hay DB. Cần test hồi quy hiển thị link (có `&`, link rút gọn, nhiều link, xuống dòng, `&nbsp;` cũ, biến `{name}`). Sau deploy cần hard-reload vì có hàm mới trong common.js.
```

**Journal #149147 — Dev Studio — 2026-10-28:**

```
Dev handoff — 28/10 09:24 · nhánh ai_studio_fixbug_44625

File đã sửa (php-web):
  public/js/chats/chat-v2.js       | 14 ++------------
  public/js/common.js              | 30 ++++++++++++++++++++++++------
  public/js/error_list/index_v2.js |  7 +------
  public/js/mobile/chat.js         |  7 +------
  public/js/talk_list/index.js     |  7 +------
  5 files changed, 29 insertions(+), 36 deletions(-)

Đánh giá ảnh hưởng — Rủi ro thấp: Chỉ đổi JS hiển thị, giữ nguyên regex nhận link và quy tắc escape đang dùng, đã fuzz 20.000 chuỗi trên Chromium. Rủi ro còn lại là cache trình duyệt giữa common.js và file JS của trang.
- common.js được nạp ở mọi trang dùng layout basic/admin: chỉ thêm hàm mới và đổi nhánh text của displayMessageFromData (2 nơi gọi: chat nhóm, chi tiết tin lỗi).
- Mọi chỗ v-html của màn chat 1:1 PC đi qua showMessageText (tin thường, trích dẫn, salon/lesson, template trích dẫn): cần test hồi quy hiển thị tin.
- Hiển thị link rút gọn của hệ thống (sl/, s/, l/ hiện [...(短縮)]) dựa vào base_url của trang PC và mobile.
- Tin cũ trong DB có chứa HTML giờ hiện thành chữ ở chat nhóm, chi tiết tin lỗi và chat mobile.

Migration / thay đổi dữ liệu: không có (đã kiểm diff).
Recover dữ liệu: Không cần recover — Lỗi chỉ nằm ở khâu render phía trình duyệt.

Branch: ai_studio_fixbug_44625 (nhánh gốc release_step_20260930_v2 @303a131b9c03, commit 1f9478b246d1849b15fa556b573d21fc288e9d0e)
```

**Journal #149212 — Dev Studio — 2026-10-28 (bổ sung chat nhóm):**

```
Dev handoff — 28/10 11:04 · nhánh ai_studio_fixbug_44625

Bug automation Test Studio:
- Bug #4822 để sau: màn chat nhóm cũ /basic/chat/group trắng trang (ReferenceError checkFriend, có từ 2022, commit 933dfb6c0f), không liên quan commit sửa XSS. Tin nhóm kiểm ở /chat-v3 → 「グループ」, displayMessageFromData kiểm ở /basic/error-list-setting/{id}.

Nội dung thay đổi (giữ nguyên 5 file như v1):
- Chat 1:1 PC (/chat-v3, gồm hội thoại nhóm ở bộ lọc 「グループ」): tạo link an toàn, ký tự đặc biệt hiện thành chữ.
- Talk list (/talk-list) và danh sách tin lỗi v2 (/error-list-v2): hiển thị an toàn.
- Chi tiết tin lỗi (/basic/error-list-setting/{id}) và chat 1:1 mobile (/chat-mobile/{id}): trước không escape, nay escape < > " và tạo link an toàn.

Việc ngoài phạm vi task: ticket riêng cho chat nhóm cũ /basic/chat/group; ticket bảo mật riêng cho IDOR ở /basic/error-list-setting/{id}; đội bảo mật rà DB production; bump config sns-line.version khi deploy.

Branch: ai_studio_fixbug_44625 (commit 1f9478b246d1849b15fa556b573d21fc288e9d0e)
```
