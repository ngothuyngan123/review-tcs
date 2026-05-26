# 04 — TC List (do member viết)

> **Note**: File này được auto-convert từ Google Sheet `Improve 1.0` rows 3492-3548 (column J = "Bug KH #36243") ngày 2026-05-13. **Format gốc sheet là nested checklist (Main / Sub1-4 / Expected)**, KHÔNG phải 10-cột chuẩn — đã convert best-effort. Nhiều ô Expected trống do sheet visual inherit (sub-case dùng chung expected của parent).

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | _<chưa xác định — sheet không có cột Assignee fill>_ |
| Ngày submit | 2026-05-13 (đồng bộ với dev impact journal) |
| Version TCs | v1 |
| Link TC gốc | [Google Sheet — Improve 1.0!A3492:O3548](https://docs.google.com/spreadsheets/d/15QEYkgp3OhzQyA5CLADvpQu_CAGovQIREuNjxPnBbOk/edit?gid=412698763#gid=412698763) |

---

## TC List

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-01 | Tái hiện case KH — Android quét QR landing, tap btn kết bạn | Regression | High | Device Android (LINE 26.6.0/26.6.1) | KH dùng device Android quét QR landing để add friend → click vào btn kết bạn | Click btn kết bạn phải **phản hồi** và add friend thành công (sau fix) | (sheet không ghi) | | |
| TC-02 | Landing all — Friend chưa accept LIFF app, chưa nhấn add bot | Positive | Medium | Friend chưa từng accept LIFF app của bot | Click vào accept LIFF app | Friend click vào accept LIFF app thành công | Done step | | |
| TC-03 | Landing all — Friend đã accept LIFF, chưa add bot, click ở Android | Positive | High | Friend đã accept LIFF nhưng chưa add bot, device Android | Click btn add bot | _<expected sheet rỗng — inherit>_ | Done step | | |
| TC-04 | Landing all — Friend đã accept LIFF, chưa add bot, click ở iOS | Positive | High | Friend đã accept LIFF nhưng chưa add bot, device iOS | Click btn add bot | _<expected sheet rỗng — inherit>_ | Done step | | |
| TC-05 | Landing all — Nhấn add bot sau khi đã accept LIFF | Positive | High | Friend đã accept LIFF app | Nhấn add bot | Chỉ hiển thị bản ghi mới khi đã add bot. Không hiển thị bản ghi khi nhấn/quét QR nhưng chưa add bot | Done step | | |
| TC-06 | Landing all — Quét khi landing off | Negative | Medium | Landing đã được set off (disabled) | Quét QR landing | _<expected sheet rỗng>_ | | | |
| TC-07 | Friend new — Quét QR ở màn list, device iOS | Positive | High | Friend mới, chưa add bot | Quét QR landing ở màn list bằng device iOS | (a) Friend nhấn add bot thành công<br>(b) Sau add bot có send action thành công cho user<br>(c) Send cả msg, action ở màn `setting-add-friend`<br>(d) Count vào màn list, 4 tab detail bình thường<br>(e) Check DB: `detail_landing_click` | | | |
| TC-08 | Friend new — Quét QR ở màn detail, device Android | Positive | High | Friend mới, device Android | Quét QR landing ở màn detail | _<expected sheet rỗng — inherit TC-07>_ | Done step | | |
| TC-09 | Friend new — Quét landing có LP (post code) | Positive | Medium | Friend mới, landing có gắn LP | Quét QR landing có LP | _<expected sheet rỗng — inherit TC-07>_ | | | |
| TC-10 | Friend new — Mở link ở PC → user nhấn quét ở device | Positive | Medium | Friend mới, link landing được mở ở PC trước | PC mở link → user dùng device quét | _<expected sheet rỗng — inherit TC-07>_ | Done step | | |
| TC-11 | Friend new — Nhấn vào link QR (ở màn list, device Android) | Positive | High | Friend mới, có link QR ở màn list | Click vào link QR ở màn list bằng device Android | (a) Friend nhấn add bot thành công<br>(b) Send action OK<br>(c) Send msg + action ở `setting-add-friend`<br>(d) Count màn list + 4 tab detail<br>(e) Check DB: `detail_landing_click` | Done step | | |
| TC-12 | Friend new — Nhấn link QR (ở màn detail, device iOS) | Positive | High | Friend mới, link ở màn detail | Click link ở màn detail bằng device iOS | _<expected sheet rỗng — inherit TC-11>_ | Done step | | |
| TC-13 | Friend new — Nhấn link landing có LP | Positive | Medium | Link landing có LP | Click link | _<expected sheet rỗng — inherit TC-11>_ | | | |
| TC-14 | Friend new — Mở app LINE | Positive | Medium | _<chưa rõ — sheet ngắn gọn>_ | Open LINE app | _<expected sheet rỗng>_ | | | |
| TC-15 | Friend new — Mở ngoài app LINE | Positive | Medium | Click link landing từ ngoài LINE app (vd browser) | Open ngoài app LINE | _<expected sheet rỗng>_ | | | |
| TC-16 | Friend new — Quét QR khi landing off | Negative | Medium | Landing đã set off | Quét QR landing | _<expected sheet rỗng>_ | | | |
| TC-17 | Friend old (chưa tồn tại trên tool) — Quét QR màn list, device iOS | Positive | High | Friend "cũ" trên LINE nhưng chưa từng có record trên tool LME | Quét QR landing ở màn list bằng iOS | (a) Friend nhấn add bot thành công<br>(b) Send action OK<br>(c) Send msg + action ở `setting-add-friend-old`<br>(d) Count màn list + 4 tab detail<br>(e) Check DB: `detail_landing_click` | | | |
| TC-18 | Friend old (chưa tồn tại) — Quét QR màn detail, device Android | Positive | High | Friend old, chưa tồn tại tool, Android | Quét QR ở màn detail | _<expected sheet rỗng — inherit TC-17>_ | | | |
| TC-19 | Friend old (chưa tồn tại) — Quét landing có LP | Positive | Medium | Friend old, landing có LP | Quét QR | _<expected sheet rỗng — inherit TC-17>_ | | | |
| TC-20 | Friend old (chưa tồn tại) — Mở link PC, quét device | Positive | Medium | Friend old, link mở PC | PC mở → device quét | _<expected sheet rỗng — inherit TC-17>_ | | | |
| TC-21 | Friend old (chưa tồn tại) — Nhấn link QR màn list, Android | Positive | High | Friend old, link ở list, Android | Click link | (a) Friend nhấn add bot thành công<br>(b) Send action OK<br>(c) Send msg + action ở `setting-add-friend-old`<br>(d) Count màn list + 4 tab detail<br>(e) Check DB: `detail_landing_click` | | | |
| TC-22 | Friend old (chưa tồn tại) — Nhấn link QR màn detail, iOS | Positive | High | Friend old, link detail, iOS | Click link | _<expected sheet rỗng — inherit TC-21>_ | | | |
| TC-23 | Friend old (chưa tồn tại) — Nhấn link landing có LP | Positive | Medium | | Click link có LP | _<expected sheet rỗng — inherit TC-21>_ | | | |
| TC-24 | Friend old (chưa tồn tại) — Open app LINE | Positive | Medium | | Open LINE | _<expected sheet rỗng>_ | | | |
| TC-25 | Friend old (chưa tồn tại) — Open ngoài app LINE | Positive | Medium | | Open ngoài LINE | _<expected sheet rỗng>_ | | | |
| TC-26 | Friend old (chưa tồn tại) — Quét khi landing off | Negative | Medium | | Quét QR | _<expected sheet rỗng>_ | | | |
| TC-27 | Friend old (đã tồn tại) — Quét QR màn list, iOS | Positive | High | Friend đã có record trên tool LME | Quét QR màn list iOS | (a) Friend quét QR thành công<br>(b) Send action OK sau add bot<br>(c) Count màn list + 4 tab detail<br>(d) Check DB: `detail_landing_click` | | | |
| TC-28 | Friend old (đã tồn tại) — Quét QR màn detail, Android | Positive | High | Friend old đã tồn tại, Android | Quét QR | _<expected sheet rỗng — inherit TC-27>_ | | | |
| TC-29 | Friend old (đã tồn tại) — Quét landing có LP | Positive | Medium | | Quét QR có LP | _<expected sheet rỗng — inherit TC-27>_ | | | |
| TC-30 | Friend old (đã tồn tại) — Mở link PC, quét device | Positive | Medium | | PC → device quét | _<expected sheet rỗng — inherit TC-27>_ | | | |
| TC-31 | Friend old (đã tồn tại) — Nhấn link QR màn list, Android | Positive | High | Friend old đã tồn tại, link list, Android | Click link | (a) Friend quét QR thành công<br>(b) Send action OK<br>(c) Count màn list + 4 tab detail<br>(d) Check DB: `detail_landing_click` | | | |
| TC-32 | Friend old (đã tồn tại) — Nhấn link QR màn detail, iOS | Positive | High | | Click link | _<expected sheet rỗng — inherit TC-31>_ | | | |
| TC-33 | Friend old (đã tồn tại) — Nhấn link landing có LP | Positive | Medium | | Click link có LP | _<expected sheet rỗng — inherit TC-31>_ | | | |
| TC-34 | Friend old (đã tồn tại) — Open app LINE | Positive | Medium | | Open LINE | _<expected sheet rỗng>_ | | | |
| TC-35 | Friend old (đã tồn tại) — Open ngoài app LINE | Positive | Medium | | Open ngoài LINE | _<expected sheet rỗng>_ | | | |
| TC-36 | Friend old (đã tồn tại) — Quét khi landing off | Negative | Medium | | Quét QR | _<expected sheet rỗng>_ | | | |
| TC-37 | Friend unblock — Quét QR màn list, iOS | Positive | High | Friend đang block bot, unblock qua quét QR | Quét QR màn list iOS | (a) Friend nhấn unblock thành công<br>(b) Send action OK sau add bot<br>(c) Send msg + action ở `setting-add-friend-unblock`<br>(d) Count màn list + 4 tab detail<br>(e) Check DB: `detail_landing_click` | Done step | | |
| TC-38 | Friend unblock — Quét QR màn detail, Android | Positive | High | Friend unblock, Android | Quét QR | _<expected sheet rỗng — inherit TC-37>_ | Done step | | |
| TC-39 | Friend unblock — Quét landing có LP | Positive | Medium | | Quét QR có LP | _<expected sheet rỗng — inherit TC-37>_ | | | |
| TC-40 | Friend unblock — Mở link PC, quét device | Positive | Medium | | PC mở → device quét | _<expected sheet rỗng — inherit TC-37>_ | Done step | | |
| TC-41 | Friend unblock — Nhấn link QR màn list, Android | Positive | High | Friend unblock, link list, Android | Click link | (a) Friend nhấn add bot thành công<br>(b) Send action OK<br>(c) Send msg + action ở `setting-add-friend-unblock`<br>(d) Count màn list + 4 tab detail<br>(e) Check DB: `detail_landing_click` | | | |
| TC-42 | Friend unblock — Nhấn link QR màn detail, iOS | Positive | High | | Click link | _<expected sheet rỗng — inherit TC-41>_ | | | |
| TC-43 | Friend unblock — Nhấn link landing có LP | Positive | Medium | | Click link có LP | _<expected sheet rỗng — inherit TC-41>_ | | | |
| TC-44 | Friend unblock — Open app LINE | Positive | Medium | | Open LINE | _<expected sheet rỗng>_ | | | |
| TC-45 | Friend unblock — Open ngoài app LINE | Positive | Medium | | Open ngoài LINE | _<expected sheet rỗng>_ | | | |
| TC-46 | Friend unblock — Quét khi landing off | Negative | Medium | | Quét QR | _<expected sheet rỗng>_ | | | |
| TC-47 | Landing new friend | _<rỗng>_ | _<rỗng>_ | _<rỗng>_ | _<sheet chỉ có title>_ | _<expected sheet rỗng>_ | Done step | | |
| TC-48 | Landing Copy | _<rỗng>_ | _<rỗng>_ | _<rỗng>_ | _<sheet chỉ có title>_ | _<expected sheet rỗng>_ | | | |
| TC-49 | Check account staff | _<rỗng>_ | _<rỗng>_ | _<rỗng>_ | _<sheet chỉ có title>_ | _<expected sheet rỗng>_ | Done step | | |

### Chú thích cột

- **Type**:
  - `Positive` — happy path đúng theo fix
  - `Negative` — input sai / điều kiện sai, verify xử lý lỗi
  - `Boundary` — giá trị biên (min/max, null, empty, max length, race condition, multi-tab)
  - `Regression` — verify tính năng cũ không bị ảnh hưởng

### Environment (note)

Sheet không note env. Suy luận: test trên **Staging** (theo journal #117754 — Ngần đã reproduce trên staging với URL `https://go.lmes.jp/landing-qr/2002341759-JRn2awBD?uLand=7nUI4Q`).

Tuy nhiên **bug fix specific cho LINE Android 26.6.0/26.6.1** → cần device thật, không thể test trên emulator. Khi test Android cần xác nhận LINE version cụ thể.

---

## Member tự check trước khi submit

### Coverage check

- [ ] Đã đọc kỹ `01-bug-task.md`
- [ ] Đã đọc kỹ `02-spec-reference.md` (không có file riêng — fallback `LME-SYSTEM-SPEC.md`)
- [ ] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục
- [ ] **Mỗi impact** (F1, T1, T2, T3) có ít nhất 1 TC verify
- [ ] Có ít nhất 1 TC reproduce KH (TC-01)
- [ ] Có TC regression cho tính năng cũ (T1 landing QR — TC-02 đến TC-46 cover)
- [ ] Mọi TC có steps + expected rõ ràng — **HIỆN TẠI: nhiều TC inherit expected, ô rỗng**
- [ ] Title TC chứa keyword giúp Leader map impact

### Base checklist LME

**§A Checklist web**:
- [ ] A.1 Function checklist — CL1 (sort), CL2 (reload after save), CL3 (permission), CL11 (CRUD account context), CL18 (load + submit after refresh)
- [ ] A.2 Non-function: Compatibility (Android/iOS device matrix — **trực tiếp liên quan bug**), Regression

**§B Checklist job**:
- [ ] B.1 Job callback — LIFF callback có liên quan
- [ ] B.2 Job sync Java — N/A

**§C Các tính năng chung**:
- [ ] C.1 Bill tiền — N/A
- [ ] C.2 Send message — gián tiếp (send action sau khi friend add bot — xem expected TC-07/TC-11)
- [ ] C.3 Friend info — N/A
- [ ] C.4 Tag — N/A
- [ ] C.5 Google sheet — N/A
- [ ] C.6 Google calendar — N/A
- [ ] C.7 Plan limits — N/A
- [ ] C.8 Sort — N/A
