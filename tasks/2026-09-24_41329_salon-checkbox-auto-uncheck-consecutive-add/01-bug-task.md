# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41329 bởi `/new-task` (2026-09-24). Metadata Redmine tra thẳng trên Redmine khi cần.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41329 — [23-09-2026] [TY-12211] [Salon] Bug: checkbox tự động bỏ chọn khi thêm nhiều đặt lịch Salon liên tiếp` |
| Module / Màn hình | Salon Booking (FA-020) — màn Lịch salon (サロン予約), Tab 「予約カレンダー」 → modal thêm đặt lịch thủ công 「予約追加」, checkbox 「コース所要時間を基準に終了時間を設定」 (tự tính giờ kết thúc theo thời lượng khóa) |

## Mô tả bug (bản dịch tiếng Việt)

Nguồn: OEM tạo task trên Slack (ユーザー問い合わせ — yêu cầu từ người dùng) — 管理番号 (số quản lý) TY-12211
担当 (phụ trách): 沖原
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790125712077139
Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=T12211

Số quản lý: TY-12211
https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C3MKH0BRT
Địa chỉ: bulkclinic@gmail.com
Tên LOA: anaMed clinic
Phụ trách: 沖原
Công cụ: リンク (Link)

Nội dung yêu cầu:
Khi thực hiện thêm đặt lịch thủ công liên tiếp trong サロン予約 (đặt lịch Salon), checkbox 「コース所要時間を基準に終了時間を設定」 (đặt giờ kết thúc theo thời lượng khóa) tự động bị bỏ chọn.

【検証動画】 (video xác minh)
https://www.loom.com/share/d3925d436b754c6a886b310edd3150b5

【注意点】 (lưu ý)
bulkclinic@gmail.com
Vui lòng không thay đổi cài đặt hoặc test hành vi trên tài khoản エルメ của user này.

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" riêng — suy từ mô tả khách hàng + journal Dev, tester verify lại. -->

1. Mở màn Lịch salon → Tab 「予約カレンダー」, mở modal 「予約追加」 (nút toolbar hoặc bấm ô giờ trống).
2. Thêm 1 đặt lịch thủ công (checkbox 「コース所要時間を基準に終了時間を設定」 đang được chọn mặc định) → 登録 thành công.
3. Không tải lại trang, mở lại modal 「予約追加」 để thêm đặt lịch thứ 2.

## Expected result

- Checkbox 「コース所要時間を基準に終了時間を設定」 vẫn ở trạng thái được chọn (giống lần mở đầu tiên); giờ kết thúc tự tính theo giờ bắt đầu + thời lượng khóa.

## Actual result

- Từ lần thêm thứ 2 trở đi, checkbox tự bị bỏ chọn; bấm chọn khung giờ trống chỉ cập nhật giờ bắt đầu, giờ kết thúc còn sót giá trị của lần đặt trước (theo journal Dev #137865; khách mô tả là "tự động tính giờ kết thúc bị lệch khi đăng ký liên tiếp" — journal #137748).

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [x] Có video — Loom (link trong description, không phải attachment Redmine): https://www.loom.com/share/d3925d436b754c6a886b310edd3150b5
- [ ] Có log / request-response

<!-- Redmine attachments: 0 -->

## Ghi chú thêm của Leader

- ⚠️ Section "Tái hiện bug" không có trong Redmine — Steps/Expected/Actual ở trên suy từ mô tả khách + journal Dev, cần tester verify với video Loom.
- ⚠️ **KHÔNG test / đổi cài đặt trên tài khoản khách `bulkclinic@gmail.com` (anaMed clinic)** — theo 【注意点】 của ticket. Dựng lịch salon test riêng.
- Môi trường phát hiện: Production (tài khoản khách thật).
- Dev (AI auto-fixbug) **không tái hiện được trên dev qua UI** — kết luận dựa trên đọc code (journal #137865 mục 6).
- Điều kiện dựng env: lịch salon có bật sử dụng khóa (コース) + ít nhất 1 khóa + nhân viên có ca làm việc; thêm ≥ 2 đặt lịch liên tiếp **không tải lại trang**.
- Journal #137748 (support trả lời khách) còn 2 câu hỏi khác (2. câu hỏi bắt buộc SĐT theo khóa · 3. ẩn 「指定なし」) — là giải đáp spec, **không thuộc phạm vi fix** của ticket này.

## Journal / note từ Redmine (nguyên văn)

**Journal #137748 — AI bug detect Lme — 2026-09-23:**

```
Comment slack ngày 2026-09-23 10:01:00

沖原 裕樹（エルメサポート）
Cảm ơn quý khách đã luôn ủng hộ.

＞1. Việc tự động tính toán thời gian kết thúc bị lệch khi đăng ký đặt lịch liên tiếp

⇒ Về vấn đề quý khách đã hỏi, hiện chúng tôi đang tiến hành xác nhận nên mong quý khách vui lòng đợi trong giây lát.

＞2. Muốn chỉ đặt số điện thoại là bắt buộc cho khóa học gọi điện trong cùng một lịch

⇒ Về 「お客様への質問事項」, mỗi lịch được tạo chỉ có thể đăng ký một loại duy nhất.
Do đó, không thể thiết lập việc yêu cầu nhập số điện thoại trong câu hỏi khi đặt lịch riêng theo từng khóa học đã đặt.
Nếu nội dung câu hỏi khác nhau theo từng khóa học, quý khách cần tạo một lịch khác trong đặt lịch Salon và thực hiện đặt lịch riêng biệt.

＞3. Không muốn hiển thị 「指定なし」 trên màn hình bệnh nhân đối với đặt lịch sử dụng khung không chỉ định

⇒ Rất tiếc, với thông số kỹ thuật hiện tại của đặt lịch Salon thì không thể ẩn hiển thị đó.
Chúng tôi sẽ xem xét việc đối ứng với trường hợp sử dụng mà quý khách đã liên hệ trong thời gian tới.

Xin cảm ơn quý khách.
```

**Journal #137865 — AI LME Fix bug — 2026-09-23:** (báo cáo auto-fixbug — nội dung 4 mục đã tách sang [03-dev-impact.md](03-dev-impact.md); phần VERIFY + TỰ REVIEW chép nguyên văn dưới đây)

```
■ 6. VERIFY
   Mức: lint
   Lệnh: node --check public/js/calendar_salon/add-new-booking.js: OK (file JS duy nhất bị sửa); php -l: N/A — không sửa file PHP; git diff --stat origin/release_step_20260827...ai_fixbug_41329: 1 file, 1 insertion(+), 1 deletion(-)
   Bằng chứng: Đối chứng trong repo: màn Đặt lịch (予約管理) reset cùng ô này về ĐƯỢC CHỌN — public/js/booking_manager/vue-data-render.js:4177 (setting_time_end_by_course = true), khớp giá trị mặc định ở dòng 511 ⇒ việc reset về 'được chọn' là hành vi đúng của sản phẩm; Giá trị mặc định của chính màn Salon khi mở trang là được chọn: public/js/calendar_salon/add-new-booking.js:20; Không tái hiện được trên dev qua UI (cần tài khoản có lịch salon + khóa; tuyệt đối không đụng tài khoản khách bulkclinic@gmail.com theo ghi chú ticket) — kết luận dựa trên đọc code trạng thái form, luồng rõ ràng và tự chứng

■ TỰ REVIEW (AI)
Fix 1 dòng, đúng root cause: đồng bộ giá trị reset sau khi tạo đặt lịch với giá trị mặc định của form. Không đụng backend, không đổi dữ liệu gửi lên (trường này chỉ dùng phía giao diện để khóa ô giờ kết thúc và tự tính giờ). Sau fix, luồng bấm chọn khung giờ trống (showAddNewBookingDay/Week) cũng tự cập nhật lại giờ kết thúc như lần đầu vì các hàm đó chỉ tính khi ô được chọn.
 • Rủi ro / lưu ý khi test:
   - Người dùng nào cố ý bỏ chọn ô để nhập tay giờ kết thúc thì ở lần thêm kế tiếp ô sẽ trở lại trạng thái được chọn (đúng như khi mới mở trang và giống màn Đặt lịch 予約管理) — đây là hành vi mặc định của màn, không phải hồi quy.
   - Không có rủi ro dữ liệu: giờ kết thúc vẫn do người dùng thấy trên màn trước khi bấm lưu.
```
