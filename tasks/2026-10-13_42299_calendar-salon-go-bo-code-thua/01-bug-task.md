# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#42299 — calendar salon, gỡ bỏ code thừa` |
| Module / Màn hình | Calendar salon (xoá lịch salon, thêm ca nhân viên salon — web + app) · Chat 1:1 (chat-v2.js, đổi trạng thái hàng loạt) |

## Mô tả bug (bản dịch tiếng Việt)

<!-- Đây KHÔNG phải bug user báo — ticket yêu cầu Dev gỡ bỏ các lớp code mà AI fixbug các lượt trước đã thêm vào, theo quyết định của người phụ trách (TungKS). Dịch sát nguyên văn description Redmine: -->

- Bỏ transaction, try/catch khi delete calendar.
- Bỏ phần check `hasShiftAdjacentToExisting` của function `addWorkScheduleForStaff` (API calendar salon), `addWorkScheduleForStaff` (calendarSalonTimeBookingService).
- Bỏ alert của `showBotSessionChangedNotice` trong chat1:1.
- Bỏ transaction ở `changeStatusSettingCons`, bỏ `lockForUpdate` khi query `$conList` ở `ChatController`.

## Steps to reproduce

<!-- Không có — ticket không yêu cầu tái hiện triệu chứng, chỉ yêu cầu gỡ code. -->

## Expected result

-

## Actual result

-

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #42299: 0 attachment. -->

## Ghi chú thêm của Leader

⚠️ Ticket **không báo triệu chứng** — đây là yêu cầu gỡ bỏ code do 5 lượt AI fixbug trước thêm vào (#41304, #41321, #41258, #41216/#41953, #41228 vòng 2), theo chỉ đạo của người phụ trách (TungKS). Root cause + cách fix đã được Dev confirm đầy đủ qua 3 vòng đánh giá ảnh hưởng (v1 → v2 → v3), xem file `03-dev-impact.md`. TCs nên tập trung verify **hành vi rollback đúng về trước các ticket đã dẫn** + regression các guard/response không đổi, không phải verify 1 bug cụ thể.

- Không có migration / cấu hình đổi kèm.
- QA + user cần **Ctrl+F5** để nạp `chat-v2.js` mới (JS không bump version).
- 4 file PHPUnit lỗi sẵn trên base (`BillingServiceTest`, `ChatMediaSizeValidationTest`, `ContractExpireServiceTest`, `ExampleTest`) — Dev ghi rõ **không thuộc phạm vi ticket này**, không raise ở review này.
- Branch: `ai_studio_fixbug_42299` (nhánh gốc `release_step_20260930_v2` @`bdeac6b86989`).
- Trên **MCP LME TEST STUDIO**: task #375, đã chạy AI 28 TC ở `local` + `staging` (0 TC `prd`) — xem chi tiết + cảnh báo RULE-08 ở đầu `04-tc-list.md`.

## Dữ liệu định danh ca lỗi

<!-- Ticket không có ca lỗi cụ thể (không phải bug tái hiện) — bỏ section theo quy ước. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #140882 — Dev Studio — 2026-10-07:**

```
Dev Studio · Nguyên nhân & hướng sửa (v1)

Nguyên nhân:
Ticket không báo triệu chứng: người phụ trách yêu cầu gỡ 3 lớp code do các lượt AI fixbug trước thêm vào. Gồm: transaction kèm khoá và try/catch trong `deleteCalendarSalon` (#41304, #41321); phép kiểm `hasShiftAdjacentToExisting`, chặn ca mới dính sát ca đã có trong ngày, ở `addWorkScheduleForStaff` của service web và API app (#41258); và băng cảnh báo đổi tài khoản LINE do `showBotSessionChangedNotice` dựng ở chat 1:1 (#41216, #41953). Vị trí code và commit gốc đã xác định chính xác.

Hướng sửa:
- D-1 Bỏ transaction và try/catch khi xoá lịch salon
- D-2 Bỏ kiểm ca liền kề ca đã có ở màn web
- D-3 Bỏ kiểm ca liền kề ca đã có ở API app
- D-4 Xoá các hàm hỗ trợ không còn nơi gọi
- D-5 Bỏ băng cảnh báo đổi tài khoản LINE ở chat 1:1

Ảnh hưởng / rủi ro:
Phạm vi: xoá lịch salon (màn web), thêm ca nhân viên salon (màn web và API app), và JS chat 1:1. Rủi ro: xoá lịch có thể dừng dở dang khi lỗi giữa chừng, lúc đó lỗi đi qua Handler chung. Ca mới dính sát ca cũ lại được ghi đè như trước #41258. Tab chat cũ không còn báo gì khi tab khác đổi tài khoản.
```

**Journal #140959 — Dev Studio — 2026-10-07:**

```
Dev Studio · Nguyên nhân & hướng sửa (v2)

Nguyên nhân:
Ở bản thực thi v1, hàm xoá lịch salon `deleteCalendarSalon` vẫn còn bước đọc lại lịch `$target` và cờ `$lostRace` kèm nhánh trả 404/403/422. Đây là phần sót lại của cơ chế chống xoá song song (#41321). TungKS đã chốt bỏ cơ chế này và chỉ xoá bình thường. Các guard ở đầu hàm độc lập với cơ chế đó nên giữ lại.

Hướng sửa:
- D-6 Bỏ bước đọc lại lịch và cơ chế $lostRace khi xoá lịch salon

Ảnh hưởng / rủi ro:
Chỉ đổi hàm xoá lịch salon trên màn web; route, request và FE giữ nguyên. Hai yêu cầu xoá gửi song song có thể cùng trả 200, yêu cầu sau xoá trúng 0 dòng. Rủi ro của v1 vẫn còn: không rollback khi lỗi giữa chừng.
```

**Journal #140999 — Dev Studio — 2026-10-07:**

```
Dev Studio · Nguyên nhân & hướng sửa (v3)

Nguyên nhân:
Ticket không báo lỗi người dùng gặp, mà yêu cầu gỡ code do lượt AI fixbug #41228 (vòng 2) thêm vào. Commit đó bọc phần ghi của `ChatController::changeStatusSettingCons` trong `DB::transaction` và thêm `lockForUpdate` vào truy vấn `$conList`. Hai lượt bấm song song vì thế phải chờ nhau. Trong `ChatController` chỉ có đúng một transaction và một lockForUpdate, cả hai đều ở hàm này.

Hướng sửa:
- D-7 Bỏ transaction và lockForUpdate ở changeStatusSettingCons

Ảnh hưởng / rủi ro:
Chỉ đổi một hàm web xử lý đổi trạng thái hàng loạt ở chat 1:1. Route, response và JS giữ nguyên. Khi bấm hai lần liên tiếp hoặc thao tác từ hai tab song song, các lượt không còn chờ nhau nên có thể lại gặp lỗi 500 do deadlock như trước #41228. Khi lỗi giữa chừng cũng không còn rollback.
```

<!-- Journal #140966, #141009 là "Dev handoff" trùng nội dung nguyên nhân với #140959/#140999 kèm thêm diffstat/điểm test chi tiết — đã gộp đầy đủ vào file 03-dev-impact.md, không lặp lại nguyên văn ở đây. -->
