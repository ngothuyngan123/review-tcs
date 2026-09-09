<!-- sync-target: https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 -->

# 04 — TC List (fetch từ Redmine #37085 Link TCs)

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền sau khi review>` |
| Ngày submit | `<member điền sau khi review>` |
| Version TCs | `<member điền sau khi review>` |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1p1tI1UUR3f9AEHKEqPZ6YpfInFEa-Us1a7x4oLvRoRk/edit?gid=223705530#gid=223705530 (tab "Quản lý hợp đồng", Line 242-293) |

> ⚠️ **Lưu ý format**: Tab nguồn "Quản lý hợp đồng" dùng layout TC dạng **cây phân cấp (merged cells)**, KHÔNG phải 10 cột chuẩn của template. Bảng dưới giữ NGUYÊN giá trị từ Sheet theo cấu trúc gốc (B→J), ô trống do merge giữ nguyên trống. KHÔNG sửa Expected/Title dù fix đổi behavior. `<br>` = xuống dòng trong cell gốc.

---

## TC List (nguyên văn từ Sheet, Line 242-293)

| Row | Hạng mục (B) | Phân nhóm (C) | Scenario (D) | Case (E) | Thao tác (F) | Thao tác 2 (G) | Expected result (I) | Ghi chú hiện trạng (J) |
|---|---|---|---|---|---|---|---|---|
| 242 | **Feature #37085 Improve plan enterprise**<br>Design: https://www.figma.com/design/enai7WD4z5CPzyUrcN61xQ/01-09-%E5%A5%91%E7%B4%84%E7%AE%A1%E7%90%86?node-id=213-6522 | | | | | | | |
| 243 | Mua mới hợp đồng enterprise | Check UI | | | | | Disable ô lựa chọn account owner trên màn kết nối LOA, mặc định là chọn vào account đang đăng nhập | Hiện tại không có màn tạo mới hợp đồng enterprise |
| 244 | | Check mua hợp đồng success | | | | | Check tạo hợp đồng success, hợp đồng có owner đúng | |
| 245 | | Check mua hợp đồng standard/pro bình thường | Chọn owner là account đang đăng nhập | | | | Check tạo hợp đồng success, hợp đồng có owner đúng | |
| 246 | | | Chọn owner là account khác với account đang đăng nhập | | | | | |
| 247 | Check quản lý hợp đồng enterprise | User owner thao tác | Add bot vào slot trống ở màn list bot | Check hiển thị slot trông ở màn list bot | | | Hiển thị thông báo có slot trống của enterprise ở màn list bot<br>-> Click button 詳細を見る mở màn quản lý slot của enterprise | |
| 248 | | | | Add bot free vào slot trống enterprise | màn list bot nhấn vào button 有料プランを適用 của bot free -> Chọn vào slot enterprise -> save | | Bot free được kết nối vào slot enterprise thành công | |
| 249 | | | Check màn detail hợp đồng (vào màn point-setting -> nhấn mở detail hợp đồng) | Check click button mở màn detail hợp đồng | | | Cho phép mở vào màn detail hợp đồng | |
| 250 | | | | Check hiển thị tên LOA | | | Hợp đồng enterprise không hiển thị tên và ảnh BOT<br>-> hiện text おまとめ割引 kèm số slot của hợp đồng:<br>+ Check hợp đồng 10 slot => Hiển thị 10枠<br>+ Check hợp đồng 20 slot => Hiển thị 20枠 | |
| 251 | | | | Check button おまとめ割引の契約を変更する | | | Nhấn thì mở được sang màn quản lý slot của enterprise<br>/admin/bots/list-bot-enterprise/ | |
| 252 | | | | Check các thao tác ở màn detai hợp đồng enterprise | Change type bill<br>+ tháng -> năm<br>+ năm -> tháng | | - Cho phép thao tác, update được hợp đồng<br>- Check việc lưu lịch sử của từng thao tác trong màn detail hợp đồng | |
| 253 | | | | | extend hợp đồng | | | |
| 254 | | | | | change phương thức bill | | | |
| 255 | | | | | change main card | | | |
| 256 | | | | | change subcard | | | |
| 257 | | | | | change owner hợp đông | | | |
| 258 | | | | | cancel hợp đồng | | | |
| 259 | | | | | Hủy kết nối bot | | | |
| 260 | | | Check vào màn point-setting ở list hợp đồng check click vào text おまとめ割引 của hợp đồng enterprise | | | | Mở màn quản lý slot của enterprise /admin/bots/list-bot-enterprise/ | |
| 261 | | | Check thao tác ở màn quản lý slot của enterprise<br>/admin/bots/list-bot-enterprise/ | Add bot vào slot trông | Add bot mới | | Cho phép thao tác, update được hợp đồng | |
| 262 | | | | | Add bot từ list bot có sẵn | | | |
| 263 | | | | Xóa bot khỏi slot | | | | |
| 264 | | | | Nhấn tăng số slot của enterprise | | | | |
| 265 | | | | Nhấn giảm số slot của enterprise | | | | |
| 266 | | | | Nhấn btn 一括解除 => hủy kết nối nhiều bot cùng lúc | | | | |
| 267 | | User không phải owner thao tác | Check acc staff không được phân quyền màn hình quản lý hợp đồng | Add bot vào slot trống ở màn list bot | Check hiển thị slot trông ở màn list bot | | Không hiện thông báo slot trống của enterprise ở màn hình list bot của account không phải owner | |
| 268 | | | | CHeck màn list hợp đồng (/basic/point-settings) | | | Không hiển thị hợp động enterprise không được phân quyền | |
| 269 | | | | Check user mở bàng url của màn detail hợp đồng | copy link vào trình duyệt<br>https://lme1.watermeru.com/basic/detail-contract/1991 | | Không cho phép mở màn quản lý slot của enterprise => Báo lỗi この権限は許可されていません。 | Hiện tại đang báo lỗi và redirect về màn admin/home |
| 270 | | | | Check user mở bằng url của màn quản lý slot enterprise | copy link vào trình duyệt<br>https://lme1.watermeru.com/admin/bots/list-bot-enterprise/1991 | | Không cho phép mở màn quản lý slot của enterprise => Báo lỗi この権限は許可されていません。 | Hiện tại đang báo lỗi và redirect về màn admin/home |
| 271 | | | Check acc staff được phân quyền màn hình quản lý hợp đồng | Add bot vào slot trống ở màn list bot | Check hiển thị slot trông ở màn list bot | | Không hiện thông báo slot trống của enterprise ở màn hình list bot của account không phải owner | |
| 272 | | | | Check màn detail hợp đồng (vào màn point-setting -> nhấn mở detail hợp đồng) | Check click button mở màn detail hợp đồng | | Màn detail hợp đồng có hiện được hợp đồng enterprise<br>Mở được màn detail hợp đồng enterprise | |
| 273 | | | | | Check hiển thị tên LOA | | Hợp đồng enterprise không hiển thị tên và ảnh BOT<br>-> hiện text おまとめ割引 kèm số slot của hợp đồng:<br>+ Check hợp đồng 10 slot => Hiển thị 10枠<br>+ Check hợp đồng 20 slot => Hiển thị 20枠 | |
| 274 | | | | | Check button おまとめ割引の契約を変更する | | Ẳn button này | Hiện tại đang disable => đã fix ẩn button này |
| 275 | | | | | Check các thao tác ở màn detai hợp đồng enterprise | Change type bill<br>+ tháng -> năm<br>+ năm -> tháng | Cho phép thao tác, update được hợp đồng | |
| 276 | | | | | | extend hợp đồng | | Chỉ check có mở được màn extend thao tác, k check được bill success do số tiền bill lớn > số tiền bill max của univapay |
| 277 | | | | | | change phương thức bill | | |
| 278 | | | | | | change main card | | |
| 279 | | | | | | change subcard | | |
| 280 | | | | | | change owner hợp đông | Không cho phép => disable button | |
| 281 | | | | | | cancel hợp đồng | Không cho phép => disable button | |
| 282 | | | | | | Hủy kết nối bot | Không cho phép => disable button | |
| 283 | | | | Check vào màn point-setting ở list hợp đồng check click vào text おまとめ割引 của hợp đồng enterprise | | | Không cho phép mở màn quản lý slot của enterprise => Báo lỗi この権限は許可されていません。 | Hiện tại đang báo lỗi và redirect về màn admin/home |
| 284 | | | | Check user mở bằng url của màn quản lý slot enterprise | copy link vào trình duyệt<br>https://lme1.watermeru.com/admin/bots/list-bot-enterprise/1991 | | Báo lỗi この権限は許可されていません。 | Hiện tại đang báo lỗi và redirect về màn admin/home |
| 285 | Regression test: Check quản lý hợp đồng standard, pro không bị ảnh hưởng | User owner thao tác | Add bot vào slot trống ở màn list bot | | | | Cho phép thao tác | |
| 286 | | | Check màn detail hợp đồng (vào màn point-setting -> nhấn mở detail hợp đồng) | Check hiển thị tên LOA | | | Hiển thị được tên bot đã kết nối | |
| 287 | | | | Check các thao tác với hợp đồng | | | Cho phép thao tác, update được hợp đồng | |
| 288 | | | Add bot free vào slot trống standard/ pro | màn list bot nhấn vào button 有料プランを適用 của bot free -> Chọn vào slot standard/pro -> save | | | Bot free được kết nối vào slot standard/pro thành công | |
| 289 | | User không phải owner thao tác | Check acc staff không được phân quyền màn hình quản lý hợp đồng | Check hiển thị slot trống ở màn list bot | | | Các slot trống chưa được add bot do vậy cũng chưa được phân quyền<br>=> Không hiện các slot trống của owner khác | |
| 290 | | | | Check màn list hợp đồng | | | bot chưa được phân quyền sẽ không hiện ở màn list hợp đồng | |
| 291 | | | | User mở bằng url của màn detail hợp đồng | | | Báo lỗi この権限は許可されていません。 | Hiện tại đang báo lỗi và redirect về màn admin/home |
| 292 | | | Check acc staff được phân quyền màn hình quản lý hợp đồng | Check hiển thị slot trống ở màn list bot | | | Các slot trống chưa được add bot do vậy cũng chưa được phân quyền<br>=> Không hiện các slot trống của owner khác | |
| 293 | | | | Check màn list hợp đồng | | | Hiện được các bot đã được phân quyền<br>=> click mở được detail hợp đồng | |

---

## Member tự check trước khi submit

> Placeholder — `<member điền sau khi review>`. TCs trên là nguyên văn fetch từ Sheet, member/Leader đối chiếu coverage với `03-dev-impact.md` trước khi review.

<!-- Source: fetched từ Redmine #37085 Link TCs, range A242:J293 tab "Quản lý hợp đồng" lúc 2026-06-20. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
