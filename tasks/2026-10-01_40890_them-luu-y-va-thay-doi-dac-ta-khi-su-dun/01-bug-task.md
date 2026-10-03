# 01 — Bug Task từ khách hàng

> 2 cách điền file này:
> 1. **Auto-fill từ Redmine** — chạy `/new-task <redmine-id>` → Claude fetch issue qua Redmine REST API (`scripts/redmine_fetch.py`), tạo folder mới + fill các section bên dưới (cùng với `03-dev-impact.md`).
> 2. **Paste tay** — nếu không có Redmine link, member paste nội dung task bug.
>
> File này **chỉ giữ thông tin cần để viết/review TC**. Metadata Redmine (ngày báo cáo, người báo, priority, URL, môi trường phát hiện) tra thẳng trên Redmine khi cần, KHÔNG chép lại vào đây.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#40890 — Thêm lưu ý và thay đổi đặc tả khi sử dụng chức năng thanh toán trong Booking lession/salon` |
| Module / Màn hình | FA-019 Đặt lịch bài học (`レッスン予約`) + FA-020 Đặt lịch salon (`サロン・面談予約`) — tab `予約設定` › `お客様への質問項目` › panel ③「編集」 |

## Mô tả bug (bản dịch tiếng Việt)

> ⚠️ Đây là ticket tracker **Feature** (không phải Bug) — thay đổi đặc tả / thêm lưu ý, không phải lỗi phát sinh. Nội dung dưới đây dịch sát nguyên văn Redmine (tác giả ticket đã kèm sẵn chú thích VN trong ngoặc).

Tên gốc (JP): `予約機能 決済利用時の注意書き追加と仕様変更`

Thêm lưu ý: `決済機能を利用の場合「お名前」「メールアドレス」項目は決済システム側への連携のため必須回答となります。`
(Khi sử dụng chức năng thanh toán, các mục 「お名前」 (Họ tên) và 「メールアドレス」 (Địa chỉ email) sẽ là thông tin bắt buộc phải trả lời/nhập, vì cần liên kết thông tin này với hệ thống thanh toán.)

- Design gốc: https://xd.adobe.com/view/0c1378a9-3d93-4d4c-962a-ed0464b7f3c8-5940/specs/
- Design clone (Figma): https://www.figma.com/design/nivEuL9ZLEAYOYPBy7ha82/2607-%E4%BB%95%E6%A7%98%E5%A4%89%E6%9B%B4%EF%BC%88%E6%B1%BA%E6%B8%88%E5%88%A9%E7%94%A8%E6%99%82%E3%81%AE%E6%A1%88%E5%86%85%E8%BF%BD%E5%8A%A0%EF%BC%89?node-id=0-1&p=f&t=4fT7ARsSEt0z3WUP-0
- Link task (Missiona): https://missiona-tools.vercel.app/lme-dev/tickets/754784e6-6be6-49c7-adad-28b878c894c9
- Ticket cha: #39193

## Steps to reproduce

<!-- N/A — ticket Feature, không có bug tái hiện. -->

## Expected result

<!-- N/A — xem mô tả bug + 03-dev-impact.md mục "Đánh giá ảnh hưởng" (requirements REQ-001 → REQ-008) -->

## Actual result

<!-- N/A -->

## Ảnh / video / log đính kèm

- [ ] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

<!-- issue.attachments = 0, không có file đính kèm trên Redmine. Design tham khảo ở Adobe XD / Figma link phía trên. -->

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine vì đây là ticket Feature (tracker = Feature, status = New), không phải Bug** — không có section "Tái hiện bug". Yêu cầu bắt nguồn từ thay đổi đặc tả (xem Design link), được AI dev tự implement trên branch `ai-feature-40890`.

✅ **Phạm vi đã chốt (human, 2026-10-01)**: Spec change chỉ là — tại màn setting form 「予約時のお客様への質問項目」 của Salon và Lesson, thêm 1 mục hiển thị ghi chú `決済機能を利用の場合「お名前」「メールアドレス」項目は決済システム側への連携のため必須回答となります。`. **Đối tượng add: 2 item mặc định loại メールアドレス và お名前. Các item khác thì không add.** Không có thay đổi logic validate — việc 2 item này bắt buộc khi bật thanh toán là hành vi có sẵn (spec lesson-booking **BR-50**), banner chỉ thông báo lại.

⚠️ **Điểm AI tự quyết cần BA/TA xác nhận** (journal #138551 mục 5, D-01 mức medium): AI tách banner thành 1 partial dùng chung (`payment_required_notice.blade.php`) include vào cả 2 file `setting_form.blade.php` (lesson + salon) thay vì dán markup trùng lặp vào từng file như technical-spec §1 chỉ định ban đầu → thành 3 file thay vì 2 như checklist TD-11 ghi. Về mặt test không đổi hành vi UI, nhưng leader nên biết sai lệch so với TD gốc.

⚠️ **Discrepancy màu viền banner đã biết** (từ MCP LME TEST STUDIO, xem `03-dev-impact.md`): code hiện dựng viền `#91CAFF`, trong khi quyết định thiết kế QA-tech-003 (2026-09-15) chốt viền `#1677FF` (trùng màu chữ/icon). Đã có 2 TC Studio fail vì lệch này (NEW-4, NEW-18) và đã raise bug **#41666** — không phải lỗi mới phát hiện khi review.

## Dữ liệu định danh ca lỗi

<!-- Bỏ — ticket Feature, không có ca lỗi cụ thể. -->

## Journal / note từ Redmine (nguyên văn)

**Journal #138551 — Do Van Tu TuDV — 2026-09-25:**

```
★ BÁO CÁO TIẾN ĐỘ AI DEV — #40890 Thêm lưu ý và thay đổi đặc tả khi sử dụng chức năng thanh toán trong Booking lession/salon  (25/09/2026)
(Comment TỰ ĐỘNG do workflow AI implement sinh ra từ trạng thái thật của branch —
 không phải ý kiến cá nhân viết tay.)
════════════════════════════════════════════════

Branch: ai-feature-40890 · base: 131bde0f22 · HEAD: f0fbccea6e
Sprint: sprint-2026-09 · UPDATE — FA-019 「レッスン予約」 + FA-020 「サロン・面談予約」
Trạng thái: completed (100%) — Hoàn tất — CR-01 banner 決済連携 đã thêm cho cả 2 hệ (レッスン + サロン)

■ 1. ĐÃ LÀM
 • CR-01 / BR-C01-01..03 — banner lưu ý 決済連携 trong panel ③「編集」 (レッスン + サロン)
 • Màn đã làm: SCR-01

■ 2. THAY ĐỔI CODE TRÊN BRANCH
 • 31bd44d4bc — feat(40890): update implementation — payment_required_notice.blade.php, setting_form.blade.php, setting_form.blade.php (spec 7a9f9fb943614d82) (3 file, +23/-0)

■ 3. ĐÃ KIỂM TỚI ĐÂU
 • Checklist: 11 mục — pass 10 / manual 1
 • ⚠ Container dev KHÔNG có DB/Redis ⇒ chỉ verify tới mức compile/lint + kiểm tĩnh; hành vi thật cần QA runtime.

■ 4. CẦN QA RUNTIME / CÒN HỞ
Cần QA kiểm tay:
 • [TD-11] Không có thay đổi nào ngoài 2 file blade

■ 5. ĐIỂM AI TỰ QUYẾT — CẦN BA/TA XÁC NHẬN
 • [D-01][medium] Tách banner thành partial dùng chung thay vì inline 2 bản như TD chỉ định
   → đã chọn: Tạo resources/views/basic/calendar_management/tabs/setting_calendar_tab/components/payment_required_notice.blade.php, @include từ cả 2 file setting_form (lesson + salon). TD §1 nói dán nguyên xi markup sang file thứ hai (2 file, checklist TD-11 ghi "không có thay đổi nào ngoài 2 file blade") — thực tế thành 3 file.
   → căn cứ: technical-spec §1 Vị trí chèn + §11 checklist + RK-01
 • (+ 2 quyết định mức low — xem tab ⚖ Quyết định trên dashboard)

────────────────────────────────────────────────
Sinh tự động lúc 2026-09-25T09:30:37.570Z từ artifact của task "40890_them-luu-y-va-thay-doi-dac-ta-khi-su-dun".
```

<!-- Journal #136495 (2026-09-15) không có notes — chỉ đổi status, đã bỏ qua theo quy tắc. -->
