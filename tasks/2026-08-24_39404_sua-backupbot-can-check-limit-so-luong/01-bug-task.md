# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine bởi `/new-task`. Tester verify rồi tick checkbox "Tester verify auto-fill chính xác".

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#39404 — Sửa backupbot cần check limit số lượng tạo` |
| Redmine URL | https://redmine.watermelon.vn/issues/39404 |
| Auto-filled | `2026-08-24 by /new-task` |
| Ngày báo cáo | `2026-08-05` |
| Khách hàng / PM báo | `Văn Dũng Đinh` |
| Module / Màn hình | `<chưa rõ — tester fill>` (Redmine category trống, không có custom field Module) |
| Priority | `Medium` (Redmine priority = `Normal`) |
| Môi trường phát hiện | `<chưa rõ>` (description không nêu môi trường) |

> Metadata khác từ Redmine: tracker = `Bug Tester` · project = `Lme` · status = `New` · assigned_to = *(trống)* · custom field `Commit Date` = *(trống)* · updated_on = `2026-08-21T09:50:28Z`.

## Mô tả bug (nguyên văn từ khách hàng)

<!-- Paste nguyên văn description. KHÔNG diễn giải lại. -->

```
base branch: release-t07-2026
job backupbot class BackupBotTask
bảng b_event_detail plan standard chỉ cho tạo 10 thôi. giờ cần check bot đích thuộc plan nào. nếu plan standard thì check nếu có bản ghi b_event_detail >=10 cần xóa các bản ghi thừa đi

logic cần thực hiện. vẫn cứ backup bình thường sau khi hoàn tất backup cần check lại
plan và bản ghi bảng b_event_detail (cả bảng có sẵn trong db và bảng mới tạo) nếu quá số lương của plan thì thực hiện gọi api để xóa các bản ghi này
api: api/clear_b_event_detail
truyền lên:
 event_detail_id: {id bảng b_event_detail}
 bot_id:
 _token: ConfigFile.API_CERT_KEY

tham khảo api create rich menu ở class BackupBotTask.createRichmenu
https://docs.google.com/spreadsheets/d/1_GdktZFY3QVP2Vg_z2pu_odIAYPWLRk15Yn9sho3Ksg/edit?gid=0#gid=0
1. plan free đang tính theo 2 điều hiện created < 2021-07-01 hoặc flag_contract_new = 0 thì tính là plan cũ
2. standard tính theo flag_contract_new = 0 là plan cũ, 1 là plan mới
Cái staff bot free trước 11-11-2024 bot free được add 1 staff
xem chi tiết mô tả trong ảnh Screenshot 2026-07-28 201451.png dòng 22
```

## Tester verify (chỉ khi auto-fill từ Redmine)

- [ ] **Tester verify auto-fill chính xác** — chỉ tick khi đã đọc lại description + steps từ Redmine và xác nhận đầy đủ (không sót journal, attachment, custom field quan trọng).

## Steps to reproduce

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Expected result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Actual result

<!-- Redmine KHÔNG có section "Tái hiện bug" — để trống. -->

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

| # | File | URL |
|---|---|---|
| 1 | `Screenshot 2026-07-28 201451.png` | https://redmine.watermelon.vn/attachments/download/28805/Screenshot%202026-07-28%20201451.png |

> Description chỉ đích danh: *"xem chi tiết mô tả trong ảnh Screenshot 2026-07-28 201451.png **dòng 22**"* → tester **bắt buộc** mở ảnh này, nội dung dòng 22 là một phần spec chưa có trong text.

## Ghi chú thêm của Leader

⚠️ **Bug không tái hiện được trong Redmine** — description là **yêu cầu thay đổi logic từ Dev lead**, không phải bug report có steps. Root cause + cách fix đã được confirm qua đánh giá ảnh hưởng (file `03-dev-impact.md`). TCs nên tập trung verify **cách fix + regression impact**, không phải reproduce flow khách hàng.

**Nguồn spec ngoài Redmine (tester cần mở, KHÔNG có trong text ticket):**
- Ảnh `Screenshot 2026-07-28 201451.png` — dòng 22.
- Google Sheet plan/limit: https://docs.google.com/spreadsheets/d/1_GdktZFY3QVP2Vg_z2pu_odIAYPWLRk15Yn9sho3Ksg/edit?gid=0#gid=0
  ⚠️ Đây là **sheet tham chiếu plan/limit**, **KHÔNG phải Link TCs** (không có nhãn `Link TCs`, không có dòng `Row: <start>-<end>`).

---

### Journal bổ sung từ Redmine (nguyên văn — KHÔNG diễn giải)

Ngoài journal "Đánh giá ảnh hưởng" (đã tách sang `03-dev-impact.md`), ticket còn **2 journal** chứa thông tin ảnh hưởng trực tiếp tới TC:

**Journal #128353 — Văn Dũng Đinh — 2026-08-07T03:23:25Z**

```
curl -X POST "$HOST_SNSLINE/api/clear_b_event_detail" \
  -H "Accept: application/json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "event_detail_id=123" \
  --data-urlencode "bot_id=456" \
  --data-urlencode "_token=$API_SERVER_CERT


_token web đã có rồi
```

**Journal #130730 — Văn Dũng Đinh — 2026-08-20T07:57:06Z**

```
CẢNH BÁO: backup_config bảng image_map_items cần sửa lại config đang bị sai cột booking_event_id {"template_id":"template","action_id":"t_actions","form_answer_id":"form_answer","bill_id":"s_items","booking_event_id":"b_event_detail","site_script_id":"site_script","conversion_id":"conversion"}
```

> ⚠️ Journal #130730 (2026-08-20) đến **sau** báo cáo đánh giá ảnh hưởng (2026-08-05) và **không** được phản ánh trong `03-dev-impact.md` mục 4.1/4.2/4.3 → Leader cần xác nhận với Dev xem `backup_config` / `image_map_items.booking_event_id` có nằm trong phạm vi fix của ticket này không, hay là issue riêng.
