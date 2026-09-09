<!-- sync-tcs: url=https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763#gid=412698763 | sheet=Improve 2026.05 | anchor=Main Function -->

# 04 — TC List (fetched từ Sheet — READ ONLY)

> ⚠️ TCs dưới đây **fetch nguyên văn** từ Google Sheet "Improve 2026.05" (KHÔNG sửa expected/title). Đây là sheet TC dạng **phân cấp** (anchor = cột "Main Function"), không phải bảng 10 cột chuẩn — giữ nguyên cấu trúc phân cấp gốc.
>
> 📌 Lưu ý range: Redmine note ghi `row: 828~874`, nhưng row **828–847 thuộc ticket khác (#38226 — tag display)**. Khối TC của **#38263 bắt đầu từ row 848**. File này chỉ trích **row 848–874** (đúng ticket #38263).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | Ngọc Ánh (nguồn Sheet, journal Redmine #38263) |
| Ngày submit | 2026-06-27 |
| Version TCs | v1 (fetched) |
| Link TC gốc | https://docs.google.com/spreadsheets/d/1LNVRUVykGmdrqTSOEHrFzxn1t6bdfEqaGb_k06WE54I/edit?gid=412698763#gid=412698763 (Sheet: Improve 2026.05, row 828~874) |

---

## TC List (phân cấp theo cột "Main Function")

> Ghi chú đầu khối TC trên Sheet (cột Main Function, row 848 — nguyên văn mô tả bug + đánh giá ảnh hưởng):
>
> *Bug KH #38263 — [27-06-2026][T11392][Form] Khách báo action khi hiển thị form không hoạt động. Root cause: action loại "chỉ lần đầu" không kích hoạt do bản 08/05/2026 (multi-capture) nạp lại record lượt mở trước khi check điều kiện "lần đầu". Fix: tách cờ `isFirstOpenForm` trước khi nạp lại record. File: `FormAnswerController.php`. Không đổi data, không ảnh hưởng nhánh 'mọi lần'.*

| Main Function | Nhóm action | Check item | Sub-check | Case / Điều kiện | Expected result | Status |
|---|---|---|---|---|---|---|
| Check action form của form 1 page | Action open form | Check nội dung send action hiển thị ở phía line user, chat 1:1 và preview ở detail line user | check multi action | | - Send đúng action cho line user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check preview action ở màn detail line user hiển thị đúng | OK |
| | | Check việc thực hiện action theo cài đặt | check action 1 lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | OK |
| | | | | Khi open form lần sau | - Không send action<br>- Hiển thị lịch sử send action form ở detail user: Text case này đang để là gì? | OK |
| | | | check action nhiều lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | Action khi trả lời form | Check nội dung send action hiển thị ở phía line user, chat 1:1 và preview ở detail line user | check multi action | | - Send đúng action cho line user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check preview action ở màn detail line user hiển thị đúng | |
| | | | Check action text riêng | Không chọn option 質問と回答のコピーメッセージを送る | - Khi send action cho line user thì chỉ send nội dung text đã nhập<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check hiển thị preview action ở detail line user | |
| | | | | Có tích chọn option 質問と回答のコピーメッセージを送る | - Khi send action cho line user thì send nội dung text đã nhập và nội dung các câu trả lời của user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check hiển thị preview action ở detail line user | |
| | | Check việc thực hiện action theo cài đặt | check action 1 lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | - Không send action<br>- Hiển thị lịch sử send action form ở detail user: Text case này đang để là gì? | |
| | | | check action nhiều lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| Check action form của form rẽ nhánh | Action open form | Check nội dung send action hiển thị ở phía line user, chat 1:1 và preview ở detail line user | check multi action | | - Send đúng action cho line user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check preview action ở màn detail line user hiển thị đúng | |
| | | Check việc thực hiện action theo cài đặt | check action 1 lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | - Không send action<br>- Hiển thị lịch sử send action form ở detail user: Text case này đang để là gì? | |
| | | | check action nhiều lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | Action khi trả lời form | Check nội dung send action hiển thị ở phía line user, chat 1:1 và preview ở detail line user | check multi action | | - Send đúng action cho line user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check preview action ở màn detail line user hiển thị đúng | |
| | | | Check action text riêng | Không chọn option 質問と回答のコピーメッセージを送る | - Khi send action cho line user thì chỉ send nội dung text đã nhập<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check hiển thị preview action ở detail line user | |
| | | | | Có tích chọn option 質問と回答のコピーメッセージを送る | - Khi send action cho line user thì send nội dung text đã nhập và nội dung các câu trả lời của user<br>- Hiển thị đúng nội dung trên chat 1:1<br>- Check hiển thị preview action ở detail line user | |
| | | Check việc thực hiện action theo cài đặt | check action 1 lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | - Không send action<br>- Hiển thị lịch sử send action form ở detail user: Text case này đang để là gì? | |
| | | | check action nhiều lần | Khi open form lần đầu | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| | | | | Khi open form lần sau | Luôn send action chung của form<br>Hiển thị lịch sử send action form ở detail user | |
| Check form không set action | | | | | Form hiển thị bình thường, record lượt mở tạo đúng, không lỗi | |
| Regression test: Check các action khác của form chạy bình thường | Check action chẩn đoán setting cả action text riêng + multi action | | | | - Send đúng action cho line user<br>- Hiển thị đúng nội dung trên chat 1:1 | |

---

## Member tự check trước khi submit

<member điền sau khi review>

### Coverage check
- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (nếu có)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify
- [ ] Có **ít nhất 1 TC** verify trực tiếp bug fix (reproduce flow KH)
- [ ] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3
- [ ] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2
- [ ] Mọi TC đều có steps rõ ràng, expected đo lường được

<!-- Source: fetched từ Redmine #38263 Link TCs (journal Ngọc Ánh), range A828:J874 tab "Improve 2026.05" lúc 2026-06-27. Trích xuất riêng khối #38263 (row 848–874); row 828–847 thuộc ticket #38226 đã loại. KHÔNG sửa TCs này nếu chưa confirm với Leader. -->
