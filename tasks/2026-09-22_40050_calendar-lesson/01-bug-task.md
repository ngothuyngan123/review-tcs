# 01 — Bug Task từ khách hàng

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40050 — calendar lesson` |
| Module / Màn hình | `Lesson (category Redmine) — màn quản trị Lịch bài học (Lesson / Calendar Booking, FA-019): Danh sách lịch · Chi tiết lịch (tab 全体設定 / コース設定 / 予約カレンダー) · modal 受付枠 / 予約 / CSV管理 · màn tạo-sửa khoá học · bước nhắc lịch (remind) · hoàn tiền (refund)` |

## Mô tả bug (bản dịch tiếng Việt)

Nội dung yêu cầu trong ticket (nguyên văn, tiếng Việt):

- Sửa lại HTTP code cho đúng ý nghĩa với các API, ajax.
- Validate required đầu vào.
- Mọi query đều **PHẢI** ràng buộc theo bot đang đăng nhập.

Đây là ticket tracker **Bug API** dạng yêu cầu chuẩn hoá (không phải báo lỗi từ khách hàng), phạm vi = toàn bộ endpoint ajax của màn quản trị lịch bài học (Lesson). Cùng khuôn với #39566 đã làm cho lịch Salon.

Yêu cầu bổ sung do human chốt trong quá trình review (ghi trong journal AI auto-fixbug):
- Toàn bộ thông báo lỗi hiển thị cho người dùng ở màn lịch Lesson phải là **tiếng Nhật** (yêu cầu 2026-08-20).
- Không được đụng `config/sns-line.php` (bỏ thao tác bump số hiệu phiên bản tài nguyên tĩnh ở mỗi lần fix).

## Steps to reproduce

<!-- Redmine không có section "Tái hiện bug" — xem Ghi chú thêm của Leader. -->

## Expected result

<!-- trống — ticket không mô tả theo dạng expected/actual -->

## Actual result

<!-- trống — ticket không mô tả theo dạng expected/actual -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- Redmine #40050 không có attachment nào. -->

## Ghi chú thêm của Leader

- ⚠️ **Bug không tái hiện được trong Redmine** (không có section "Tái hiện bug", không có Steps/Expected/Actual). Root cause + cách fix đã được Dev/AI confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix** + **regression impact**.
- Ticket đã qua **3 vòng AI auto-fixbug** (#134734 → #136534 → #136541). Chỉ vòng cuối (#136541, commit `f1c9a55319`) là bản hiện hành — vòng 1 & 2 **chưa có** phần (3) ràng buộc bot và (4) sửa thứ tự xoá dây chuyền.
- **Branch để QA checkout**: `ai_fixbug_40050` (repo `sns-line`, nhánh gốc `release_step_20260805`, commit `f1c9a55319`, 17 file).
- ⚠️ **Cảnh báo dữ liệu**: bản dựng từ commit `adad1a4191` (push 2026-09-15) có lỗi chuỗi xoá dây chuyền không chạy → nếu đã thử xoá lịch / xoá khoá học trên bản đó thì DB có thể còn dữ liệu con mồ côi (khoá học · 受付枠 · đơn đặt chỗ · cài đặt của lịch đã xoá) cần rà / dọn tay trước khi test lại.
- ⚠️ **Môi trường**: bộ 80 TC trên MCP LME TEST STUDIO (task #280) **chạy toàn bộ ở env `local`** (3 run, run cuối 2026-09-21 bởi `vinth`), 0 TC chạy ở `staging` / `prd`. Theo **RULE-08**, các điểm liên quan hoàn tiền (bill tiền / cổng thanh toán), CSV import (media), asset version (domain) **không** được kết luận từ local.
- Điểm Dev tự đánh dấu là chỗ QA nên tập trung: (a) thao tác trên bản ghi **cũ trong DB** vs **item vừa thêm chưa lưu** trong modal (rủi ro validate required chặn nhầm); (b) bấm lại **toàn màn** để không còn thao tác nào "im lặng" sau khi HTTP 200 → 4xx.
- Dev **cố ý KHÔNG** ràng buộc bot ở service/repository dùng chung với **màn LIFF của khách · API · job nền** (hàm lấy bot đọc từ session nên ở các luồng đó sẽ rỗng) → luồng khách LINE đặt lịch phải còn chạy đúng.

## Journal / note từ Redmine (nguyên văn)

Cả 3 journal đều là báo cáo **AI AUTO-FIXBUG** (author `AI LME Fix bug`), nội dung chính là Section "Đánh giá ảnh hưởng" → đã chép nguyên văn vào [03-dev-impact.md](03-dev-impact.md) (dùng bản **vòng 3**, mới nhất). Ở đây chỉ ghi lại mốc để trace:

| Journal | Ngày | Commit đã push | Nội dung khác biệt so với vòng sau |
|---|---|---|---|
| `#134734` | 2026-09-07 | `f2f10e65cf` | Vòng refix 1: chỉ có (1) chuẩn hoá HTTP code + validate required và (2) thông báo tiếng Nhật. **Chưa có** ràng buộc bot. |
| `#136534` | 2026-09-15 | `adad1a4191` | Thêm (3) ràng buộc mọi query theo bot đang đăng nhập (96 điểm truy vấn). **Chứa lỗi** chuỗi xoá dây chuyền không chạy → dữ liệu con mồ côi. |
| `#136541` | 2026-09-15 | `f1c9a55319` | **Bản hiện hành.** Thêm (4) sửa 2 lỗi do phần (3) gây ra: xoá bản ghi cha xuống cuối chuỗi ở xoá lịch + xoá khoá học; ràng buộc nốt 8 chỗ tra khoá học theo id thô. |

- Phiên xử lý AI: `https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=438d5564-0c16-471d-9f43-dcb964ce17e5`
- Dashboard fixbug: `https://dashboard.melonglobal.net/fixbug-lme/?id=40050`
