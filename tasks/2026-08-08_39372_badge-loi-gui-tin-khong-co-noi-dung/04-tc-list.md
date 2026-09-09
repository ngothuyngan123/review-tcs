<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=10976066#gid=10976066 | sheet=[AI]TCs_UI | anchor=<CẦN XÁC NHẬN — xem §Cảnh báo sync config> -->
<!-- sync-target: https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=10976066#gid=10976066 -->

# 04 — TC List (fetch từ Google Sheet — READ-ONLY)

> ⚠️ **File này KHÔNG phải TC do member/AI viết.** Đây là **TC hiện có trên Sheet master**, fetch nguyên trạng từ Redmine #39372 → Link TCs. **KHÔNG sửa** nội dung TC nếu chưa confirm với Leader.
>
> Nếu cần sinh TC mới theo 16 cột canonical → chạy `/write-tc tasks/2026-08-08_39372_badge-loi-gui-tin-khong-co-noi-dung/`.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` — TC hiện có trên Sheet do QA team viết + AI Review bổ sung (RV-xx) |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/16jTfvTg2irjVp4fqX6CUordAOit_EwkjLBhVAM4IXNo/edit?gid=10976066#gid=10976066 |
| Tab | `[AI]TCs_UI` (gid `10976066` — đã resolve khớp) |
| Range fetch | `A285:Z312` (Redmine ghi `Row: 285~312`) — **28 dòng** |

---

## ⚠️ Cảnh báo về format

**Sheet `[AI]TCs_UI` KHÔNG dùng 16 cột canonical, cũng không dùng 10 cột cũ.** Đây là sheet UI-checklist dạng **merged-cell** — cột `Main Function` / `Sub Function` chỉ điền ở dòng đầu mỗi block, các dòng sau để trống và kế thừa giá trị phía trên. Bảng dưới **giữ nguyên trạng** giá trị từng ô, kèm số dòng gốc để đối chiếu.

Header thật của tab (dòng 1):

`A=TCs ID · B=Feature · C=Category · D=Scenario · E=Type · F=Priority · G=Precondition · H=Steps · I=Expected Result · J=Status · K=Bug KH #39372 · L=Assigned To · M=Assigned Automation · N=Notes · O=Result AI test · P=Staging`

Nhưng **khối 285–312 dùng cột lệch semantic so với header dòng 1** (sheet tái sử dụng cột cho cây menu UI): `D` = nhóm menu, `E` = Main Function, `F` = Sub Function / tiêu đề case, `G` = nội dung check / steps, `H` = điều kiện & data, `I` = kết quả mong đợi, `J` = Status, `K` = cột kết quả riêng của ticket này (`Bug KH #39372`). Tên cột ở bảng dưới đặt theo **nội dung thực tế**, chữ trong ngoặc là **cột gốc trên Sheet**.

### ⚠️ Cảnh báo sync config

Dòng `<!-- sync-tcs: ... -->` ở đầu file **chưa dùng được ngay**: `scripts/push_tc_anchored.py` cần một ô header tên đúng bằng `anchor` trong 15 dòng đầu của tab, nhưng tab `[AI]TCs_UI` **không có cột nào tên `Main Function`** (xem header dòng 1 ở trên). Chưa có cột nào cho ra đúng bộ 5 cột liền kề `TC No. / Tiêu đề / Điều kiện tiền đề / Các bước / Kết quả mong đợi`.

→ **Leader/QA phải chốt cột anchor + `--row <n>` trước khi chạy `/sync-ai-tc` hoặc `/sync-review-tc`.** Để nguyên như hiện tại thì script sẽ **fail loud** (không ghi nhầm ô) — đó là hành vi an toàn, đừng điền đại một tên cột.

---

## TC List (nguyên trạng từ Sheet)

| Row | Nhom (D) | Main Function (E) | Sub Function / Tieu de (F) | Noi dung check / Steps (G) | Dieu kien / Data (H) | Ket qua mong doi (I) | Status (J) | Bug KH #39372 (K) | Ghi chu (M) | Notes (N) |
|---|---|---|---|---|---|---|---|---|---|---|
| 285 | システム関連 | 送信エラー |  | Check hiển thị các tab<br>未確認エラー/再送登録済み/再送済み履歴/エラー原因一覧 |  | https://staging.lme.jp/basic/error-list-v2 | OK |  |  | x |
| 286 |  |  | Check menu 送信エラー thường | Check việc hiển thị badge ở menu 送信エラー khi bot có message send lỗi | Bot chỉ có message send lỗi ở chat 1:1チャット: 1 msg lỗi (type = 2) | Hiển thị badge số msg send lỗi ở menu 送信エラー là 1 | OK | OK |  |  |
| 287 |  |  |  |  | Bot chỉ có message send lỗi ở broadcast メッセージ配信: 10 msg lỗi (type = 3) | Hiển thị badge số msg send lỗi ở menu 送信エラー là 10 | OK | OK |  |  |
| 288 |  |  |  |  | Bot chỉ có message send lỗi ở ステップ配信: 99 msg lỗi (type = 4) | Hiển thị badge số msg send lỗi ở menu 送信エラー là 99 | OK | OK |  |  |
| 289 |  |  |  |  | Bot chỉ có message send lỗi ở その他メッセージ: 100 msg lỗi (type = 1) | Hiển thị badge số msg send lỗi ở menu 送信エラー là 99+ | OK | OK |  |  |
| 290 |  |  |  |  | Bot có message send lỗi ở nhiều tab tính năng và số message send lỗi = 101 | Hiển thị badge số msg send lỗi ở menu 送信エラー là 99+ | OK | OK |  |  |
| 291 |  |  |  | Check không hiển thị badge ở menu 送信エラー khi bot không có message send lỗi nào |  |  | OK | OK |  |  |
| 292 |  |  |  | Check khi xóa msg lỗi ở bên trong màn error list => Giảm count số lượng msg ở ngoài menu |  |  | NG |  | Bug Tester #38699: Badge 送信エラー không giảm khi xóa/resend ở các case retry-status / tab đã-đặt-lịch / chưa reload |  |
| 293 |  |  |  | Check khi resend success msg ở error list => Giảm count số lượng msg ở ngoài menu |  |  | NG |  |  |  |
| 294 |  |  | Check menu 送信エラー ở mục favourite | Check việc hiển thị badge ở menu 送信エラー khi bot có message send lỗi |  | Hiển thị badge số msg send lỗi ở menu 送信エラー favourite | OK | OK |  |  |
| 295 |  |  |  | Check không hiển thị badge ở menu 送信エラー khi bot không có message send lỗi nào |  |  | OK | OK |  |  |
| 296 |  |  |  | Check khi xóa msg lỗi ở bên trong màn error list => Giảm count số lượng msg ở ngoài menu |  |  | NG |  |  |  |
| 297 |  |  |  | Check khi resend success msg ở error list => Giảm count số lượng msg ở ngoài menu |  |  | NG |  |  |  |
| 298 |  |  | RV-02 — Thêm badge cho 送信エラー KHÔNG làm các mục menu khác trên sidebar v2 mọc badge thừa | 1. Chọn bot có lỗi gửi (badge 送信エラー hiện số).<br>2. Rà toàn bộ các mục menu khác trên sidebar v2 (チャット, テンプレート, メッセージ, ステップ配信, ログアウト...). | Chỉ mục 送信エラー có badge số; tất cả mục khác KHÔNG hiển thị badge nào (đối chứng âm — fix không lan sang mục khác). | [AI Review bổ sung] · Vòng 0 · impact/regression · loại: Regression — đối chứng âm menu · impact: Vòng lặp render menu v2/basic (key 'badge' dùng chung) · regression · ưu tiên High · Render loop v2/basic dùng key 'badge' generic; thêm badge cho 1 mục có thể vô tình ảnh hưởng logic hiển thị badge của mục khác — cần đối chứng âm. | OK |  |  |  |
| 299 |  |  | RV-04 — Hủy lịch resend ở tab 再送登録済み làm badge 送信エラー TĂNG lại (round-trip) | 1. Bot có lỗi; đặt lịch resend cho 1 tin (badge giảm 1 do is_confirmed=1).<br>2. Vào tab 再送登録済み, xóa/hủy thiết lập resend của tin đó (sending_schedule_id=null, is_confirmed=0).<br>3. Điều hướng lại để sidebar render lại, xem badge 送信エラー. | Sau khi hủy lịch, badge 送信エラー tăng lại đúng +1 (tin quay về trạng thái chưa xác nhận) — không giữ số cũ, không đếm âm. | [AI Review bổ sung] · Vòng 0 · impact/regression · loại: Regression — round-trip đếm · impact: EP-06 hủy lịch resend (reset is_confirmed=0) ↔ badge sidebar · regression · ưu tiên Medium · Human chỉ canh chiều GIẢM (xóa/resend), bỏ chiều TĂNG lại khi hủy lịch — vòng tròn is_confirmed quan trọng để badge không kẹt số. | NG |  |  |  |
| 300 |  |  | RV-05 — Staff KHÔNG được cấp quyền 送信エラー — mục menu render nhánh no-permission (không có badge số) | 1. Đăng nhập account staff KHÔNG được cấp quyền vào màn 送信エラー của bot (bot vẫn có lỗi gửi).<br>2. Xem mục 送信エラー trên sidebar v2. | Mục 送信エラー hiển thị trạng thái no-permission (icon cảnh báo/tooltip), KHÔNG hiển thị badge số lỗi và không click vào được — không rò số lỗi cho staff không quyền. | [AI Review bổ sung] · Vòng 1 · checklist · loại: Permission/Role · checklist RVB-02 · ưu tiên High · Nhánh render no-permission trong v2/basic KHÔNG in badge số; đây là trục phân quyền (GOC-13/CL-Func-28) human bỏ hẳn. | NG |  | Bug tự detect #38701: [Menu bar] Màn error list 送信エラー chưa hiển thị đúng giao diện khi staff không được phân quyền |  |
| 301 |  |  | RV-06 — Đối chứng đa-bot — badge chỉ đếm lỗi của bot ĐANG CHỌN | 1. Bot A có 5 lỗi gửi chưa xác nhận; bot B có 0 lỗi.<br>2. Chọn bot B, xem badge mục 送信エラー; rồi chuyển sang bot A, xem lại. | Khi chọn bot B badge ẩn (=0); khi chọn bot A badge hiện 5. Lỗi của bot A KHÔNG làm badge bot B tăng (totalErrorMessage theo getBotId()). | [AI Review bổ sung] · Vòng 1 · checklist · loại: Combine — cách ly đa-bot · checklist RVB-02 · ưu tiên High · Đa tenant where bot_id=getBotId(); human không có TC cách ly bot — rủi ro rò số giữa bot. | OK |  |  |  |
| 302 |  |  | RV-09 — Badge 送信エラー hiển thị đúng khi sidebar ở trạng thái THU GỌN (collapsed) | 1. Bot có lỗi gửi (badge hiện số).<br>2. Bấm nút thu gọn sidebar (collapsed), rồi mở lại. | Ở cả trạng thái mở và thu gọn, badge số của mục 送信エラー vẫn hiển thị đúng vị trí, không bị mất/che/vỡ layout. | [AI Review bổ sung] · Vòng 1 · checklist · loại: UI — trạng thái sidebar · checklist RVB-02 · ưu tiên Low · Sidebar v2 có toggle collapse; badge phải sống ở cả 2 trạng thái (GOC-15/UI-FULL) — human không canh. | OK |  |  |  |
| 303 |  |  | RV-11 — Đối chứng âm — mục ログアウト và mục không có key badge KHÔNG mọc badge | 1. Bot có lỗi gửi (mục 送信エラー có badge).<br>2. Kiểm mục ログアウト (noStar) và vài mục khác cùng nhóm システム関連. | Mục ログアウト và các mục không khai báo badge KHÔNG hiển thị span badge nào (đối chứng âm cho việc thêm key 'badge'). | [AI Review bổ sung] · Vòng 2 · so AI · loại: Đối chứng âm — không lan badge · checklist RVB-02 · ưu tiên Medium · Đối chiếu TC-14 (AI): xác nhận badge chỉ gắn đúng mục errorListV2, tránh regression hiển thị. | OK |  |  |  |
| 304 |  | Check khi có msg chat 1:1 send đến | user nhắn tin cho bot |  |  | - Tăng số notify chưa đọc ở màn chat 1:1<br>- số msg màn error vẫn giữ nguyên |  | OK |  |  |
| 305 |  |  | 1. check màn chat 1 :1 có số msg chưa confirm<br>2. Check màn error không có số msg nào |  |  | - 2 màn hiển thị số msg độc lập<br>- chỉ hiển thị số msg ở màn chat 1:1 |  | OK |  |  |
| 306 |  |  | user bật tư động confirm msg |  |  | - Giảm số msg chưa confirm ở chat 1:1<br>- số msg ở error vẫn giữ nguyên |  | OK |  |  |
| 307 |  |  | bot nhấn confirm số msg |  |  | - Giảm số msg chưa confirm ở chat 1:1<br>- số msg ở error vẫn giữ nguyên |  | OK |  |  |
| 308 |  |  | check khi có tin nhắn job send lỗi |  |  | - tăng số notify ở màn erro<br>- không tăng số notify ở màn chat 1:1<br>- user không nhận được msg |  | OK |  |  |
| 309 |  |  | chec ở chat 1:1 line user đang có nhiều số msg chưa confirm | Xóa line user |  | - Giảm số msg ở chat 1:1<br>- không giảm/ ảnh hưởng số msg ở error |  | OK |  |  |
| 310 |  |  | Check khi click ở button thu hẹp menu | button: メニューを閉じる | check số msg chưa đọc ở chat 1:1 | - Thu hẹp lại menu cũng hiển thị icon có msg chưa confiirm |  | OK |  |  |
| 311 |  |  |  |  | chec khi nhấn confirm hết | - Thu hẹp lại menu cũng không hiển thị số msg chưa confirm |  | OK |  |  |
| 312 |  |  |  |  | check khi có friend nhắn tin đến | - Có realtime hiển thị icon số msg chưa đọc |  | OK |  |  |

---

## Nhận xét nhanh về bộ TC fetch được (không sửa TC, chỉ note cho Leader)

- **Dòng 285–297** — TC do QA viết cho màn `送信エラー`: chủ yếu canh **badge đếm đúng số lỗi** (1 / 10 / 99 / 99+ theo type) và **badge giảm khi xóa / resend**. 4 dòng đang `NG` (292, 293, 296, 297) và có tham chiếu **Bug Tester #38699**.
- **Dòng 298–303** — TC `RV-xx` do **AI Review bổ sung ở vòng review trước** (metadata ghi ở cột `I`). Trong đó **299 (RV-04)** và **300 (RV-05)** đang `NG`; RV-05 đã raise **Bug #38701** (staff không được phân quyền).
- **Dòng 304–312** — khối TC về **tương tác chat 1:1 ↔ badge error**, đúng trục của bug #39372 (số chưa đọc chat không được lẫn sang badge lỗi). Khối này **chỉ có cột `K` = OK, cột `J` (Status) để trống** — tester confirm xem đây là kết quả của lần test nào.
- Bộ TC này **có trước** khi Dev fix #39372. Cần đối chiếu lại với `03-dev-impact.md`: fix vòng 2 còn chạm **T4 (chấm đỏ sidebar thu gọn)** và **T5 (màn テンプレート — thêm/đổi tên thư mục)** — 2 vùng này **không thấy TC nào trong range 285–312**.

---

## Member tự check trước khi submit

> Checklist đầy đủ (coverage check + base 2 tầng quan điểm LME + 12 RULE) xem [templates/04-tc-list.template.md](../../templates/04-tc-list.template.md). File này là bản fetch read-only nên chưa áp checklist — sẽ áp khi `/write-tc` sinh TC canonical.

- [ ] Đã verify range fetch đúng (`Row: 285~312`, tab `[AI]TCs_UI`)
- [ ] Đã chốt cột `anchor` cho sync config (xem §Cảnh báo sync config)
- [ ] Đã quyết định: dùng bộ TC này để `/review-tc`, hay chạy `/write-tc` sinh bộ canonical trước

<!-- Source: fetched từ Redmine #39372 Link TCs, range A285:Z312 tab "[AI]TCs_UI" (gid 10976066) lúc 2026-08-08. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
