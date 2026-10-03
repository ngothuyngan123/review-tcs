# 01 — Bug Task từ khách hàng

> Auto-fill từ Redmine #41448 bởi `/new-task` (2026-09-29) · refresh 2026-09-30 (journal #139287, #139305, #139421) · refresh 2026-10-02 (journal #139595, #139716 — bug MỚI #41822/#41823 phát hiện qua TC round 2). Metadata Redmine tra thẳng trên Redmine khi cần. ⚠️ `REDMINE_URL` đã đổi sang `https://redmine.melonglobal.net` (domain cũ `redmine.watermelon.vn` không còn kết nối được) — đã cập nhật `.env`.

## Thông tin cơ bản

| Trường | Giá trị |
|---|---|
| Bug ID / Ticket | `#41448 — [24-09-2026][31074][Salon] Khách báo ca làm việc mở tới 20h nhưng khung đặt lịch (slot) 2 tiếng chỉ hiển thị được tới 17h.` |
| Module / Màn hình | Hệ thống đặt lịch (予約システム) — Salon (サロン・面談予約, FA-020): màn chọn khung giờ đặt lịch LIFF phía khách |

## Mô tả bug (bản dịch tiếng Việt)

WSSJ ĐÃ TẠO TICKET SLACK

User: imecon.pasoka@gmail.com
Bot Name: イメコンサロンPASOKA名古屋店

Ca làm việc là đến 20h nhưng khung đặt lịch 2 tiếng chỉ hiển thị đến 17h.

Tên friend: 10/14
Chức năng: Hệ thống đặt lịch (予約システム)
Thời điểm phản hồi: 2026/09/24 15:40:00
Ảnh 1: https://go.lmes.jp/msg_template/media/images/3/218/form/1790232000FwwoyU.png
Ảnh 2: https://go.lmes.jp/msg_template/media/images/3/218/form/1790232008xz6Yv0.png

Link dashboard: https://dashboard.melonglobal.net/css-analytics/?id=31074

Ticket Slack do OEM đăng — 管理番号 31074
Link item Slack: https://l-message.slack.com/lists/T01H7J4Q5M1/F0BBUDRHNEP?record_id=Rec0C443N23KL
Link thread Slack: https://l-message.slack.com/archives/C0BALS7S73L/p1790233890691359

Nội dung từ Slack (OEM): シフト (ca làm việc) là tới 20h nhưng 予約枠 (khung đặt lịch) 2 tiếng chỉ hiển thị tới 17h.

## Steps to reproduce

<!-- Redmine description không có section "Tái hiện bug". Steps dưới đây lấy từ Journal #139305 (Đỗ Quyên — assignee, 2026-09-29). -->

1. Lịch salon: staff A ca 12:00–20:30, staff B ca 12:00–18:30.
2. Course 2 tiếng, thời gian nghỉ sau (片付け) 1 tiếng.
3. Setting 受付上限 option 3 (上限を設定する) = 2.
4. Có 1 booking lúc 17:30 ở staff A.
5. Friend chọn course 2 tiếng — 指名なし (NO STAFF), xem khung 16:00 và 16:30.

## Expected result

Khung 16:00 và 16:30 ON — khung 16:30–18:30 vẫn đủ 2 tiếng làm việc của course trong ca staff B (thời gian nghỉ không tính vào thời gian làm việc).

## Actual result

Khung 16:00 và 16:30 đang bị OFF. (Journal #139421 của Dev 2026-09-30: bản release 16:00/16:30 = TẮT; bản `e8931817a2` = BẬT.)

## Ảnh / video / log đính kèm

- [x] Có screenshot
- [ ] Có video
- [ ] Có log / request-response

- screenshot1.png — https://redmine.watermelon.vn/attachments/download/30928/screenshot1.png
- screenshot2.png — https://redmine.watermelon.vn/attachments/download/30929/screenshot2.png
- Screenshot_2.png (kèm Journal #139305) — https://redmine.watermelon.vn/attachments/download/31179/Screenshot_2.png

## Ghi chú thêm của Leader

- Description Redmine không có section tái hiện; ca tái hiện chính thức do assignee Đỗ Quyên bổ sung ở Journal #139305 (đã đưa vào Steps ở trên).
- Môi trường phát hiện: Production (bot khách OEM 31074).
- Điều kiện để lỗi xảy ra (theo Dev, journal #139166) — đủ **cả 4**: (a) 予約受付上限 = 上限を設定する (`type_limit_calendar = 1`); (b) khách chọn 指名なし; (c) lịch có cài 片付け時間 (`time_after > 0`); (d) nhân viên trong ngày lệch giờ tan ca (có nhân viên ca dài hơn đang bận).
- ⚠️ **Cập nhật 2026-09-30** (journal #139287 + #139421): sau khi fix thêm 7 ticket con QA (#41740–#41746) và 4 commit mới, bản vá **chạm cả 3 option 受付上限 × cả 指名なし lẫn 指名** và cả luồng đặt lịch có thanh toán — 4 điều kiện ở trên chỉ còn đúng cho bug gốc, không còn là phạm vi retest. Xem `03-dev-impact.md`.
- Liên quan thiết kế đã chốt ở #40128: 片付け時間 được phép tràn qua giờ tan ca, chỉ giờ PHỤC VỤ bắt buộc nằm trong ca.
- Ticket do "AI bug detect Lme" tạo; fix do "AI LME Fix bug" (auto-fixbug) thực hiện.

## Dữ liệu định danh ca lỗi

| Mục | Giá trị |
|---|---|
| bot_id | `<chưa rõ>` — Bot Name: イメコンサロンPASOKA名古屋店 (user imecon.pasoka@gmail.com) |
| Friend | 10/14 |
| Đối tượng cấu hình | Lịch salon cal 1239 (ca tái hiện của Dev): staff 621 ca 12:00–20:30 đã có đơn 17:30–19:30; staff 622 ca 12:00–20:00 rảnh; ca gộp; 指名なし; giới hạn 2, mỗi NV 1; nghỉ sau (片付け) 60'; khoá 120'; đơn vị 30' |
| Thời điểm lỗi | 2026/09/24 15:40:00 (thời điểm phản hồi); ngày tái hiện 2026-09-26 |
| Đối chứng | Release: khung 17:00 / 17:30 / 18:00 bị ẩn → sau fix hiện; 18:30 vẫn ẩn (đúng nghiệp vụ) |

## Journal / note từ Redmine (nguyên văn)

**Journal #139166 — AI LME Fix bug — 2026-09-29:**

> Nội dung đầy đủ (6 mục: nguyên nhân · cách fix · function đã check · đánh giá ảnh hưởng · recover data · verify) đã tách vào `03-dev-impact.md`. Phần bổ sung không nằm trong 4 mục của file 03:

```
■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Lệnh: php -l: No syntax errors detected; Kịch bản thật cal 1239 (621 ca 12:00-20:30 đã đặt 17:30-19:30, 622 ca 12:00-20:00 rảnh, ca gộp, 指名なし, giới hạn 2, mỗi NV 1, nghỉ sau 60', khoá 120', đơn vị 30'): release = 17:00/17:30/18:00 BỊ LOẠI → sau fix = HIỆN THỊ; 18:30 vẫn BỊ LOẠI (đúng nghiệp vụ); CASE BẪY E21 (623 tan ca 19:30 — mốc LỆCH lưới slot 60', khung 18:00 phục vụ tới 20:00): vẫn CHẶN. Bản 'bỏ hẳn kiểm tra' cho qua (sai) → đã đổi sang 'dời mốc xét'; CASE BẪY E24 (623 có 2 ca rời 12:00-18:00 + 20:00-22:00, phục vụ tới 19:00): vẫn CHẶN; Regression 14 kịch bản (verify/41448/regress_41448.php): 9 ô đổi, tất cả đúng hướng; R2/R3/R4/R6/R7/R8/R9 không đổi; Sweep 37.440 tổ hợp CÓ 片付け (verify/41448/sweep_2083.php — 4 kiểu ca, 4 kiểu booking, 指名なし + chỉ định từng NV, limCal 1/2/5, đơn vị 30'/60', khoá 90'/120', nghỉ 30'/60'): release → fix = 78 khác biệt, 100% theo hướng MỞ khung, 0 siết; tất cả nằm ở type=1 + 指名なし + có 片付け; Bằng chứng bỏ vá checkLimitHasStaff là an toàn: bản CÓ vá vs bản BỎ vá = 0 khác biệt trên cả 14 case lẫn 37.440 tổ hợp, dù dòng đó chạy 36.708 lần và đổi boolean 580 lần; Oracle chống trùng 6552 tổ hợp + ma trận vi sai (brkAfter=0, guard bất hoạt): 0 khác biệt so với release, 18 lỗ hổng có sẵn giữ nguyên
   Bằng chứng: verify/41448/regress_41448.php — 14 kịch bản gồm 2 case bẫy E21/E24: php regress_41448.php <svcA> <svcB>; verify/41448/sweep_2083.php — sweep 37.440 tổ hợp có 片付け, in cả hướng nới/siết; verify/41448/salon_oracle_check.php + salon_diff_matrix.php + probe_real_slots.php; Tài liệu tái hiện + review của human: tmp/1790328305*.md và tmp/1790331879*.md; Không query được DB dev từ container (host.docker.internal:3306 refused)

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41448 (nhánh gốc release_step_20260827, commit 56f6106a67, 1 file)  [đã push]

» Thời gian AI xử lý: 11 phút 10 giây
» Phiên xử lý AI: https://claude-admin.melonglobal.net/?project=fixbug-lme&tab=events&session=e0a8cac2-3173-4e83-99fc-d514387063ee
» Dashboard fixbug: https://dashboard.melonglobal.net/fixbug-lme/?id=41448
```

**Journal #139287 — AI LME Fix bug — 2026-09-29:**

> Báo cáo đầy đủ lần 2 (commit `d199db2c03`, 5 file) — nội dung 4 mục đã tách vào `03-dev-impact.md`. Phần verify:

```
■ 5. RECOVER DATA
   ✔ Không cần recover data

■ 6. VERIFY
   Mức: unit-test
   Regression 14 kịch bản (verify/41448/regress_41448.php): 12 ô đổi, TẤT CẢ theo hướng X→O; 4 case bẫy vẫn chặn đúng — E21 (nhân viên tan ca 19:30 giữa đoạn), E24 (2 ca rời có khoảng nghỉ giữa), R3 (mọi nhân viên đều bận), R1 khung 17:30 (phục vụ vượt ca); Quét 2 biên × 7 chế độ × 3 biến thể nghỉ (boundary_scan.php): 0 ô sai (trước fix: 21/21 sai ở biên cuối ca); Biến thể đơn vị 30' / khoá không chia hết đơn vị / ca qua đêm (boundary_scan3.php): 0 ô sai (trước fix: 4/4 kịch bản sai); 2 nhân viên lệch ca (boundary_scan2.php): 0 ô sai; Oracle chống trùng độc lập 6552 tổ hợp (salon_oracle_check.php): 0 lỗ hổng / 0 chặn oan — release là 18 lỗ hổng / 248 chặn oan; Oracle 2 chiều 5 chế độ (lateral_scan.php, bỏ nhiễu hạn mức toàn lịch bằng limCal=5): 4/5 chế độ đạt 0 lỗ hổng và 0 chặn oan; riêng chế độ gộp ca còn 27 chặn oan / 3 lỗ hổng; Sweep 37.440 tổ hợp có 片付け: 2.447 ô đổi so với release (2.328 nới, 119 siết); phần siết không tạo chặn oan ở 4 chế độ đo được; Ca qua đêm (check_claims.php): A ca 18:00-00:30, khung 22:00 khoá 120' nghỉ 60' → trước fix trả [B], sau fix trả [A,B] đúng
   Bằng chứng: Harness trong verify/41448/ ...; Không query được DB dev từ container (host.docker.internal:3306 refused) nên mọi số liệu là từ harness trích nguyên văn code

■ BRANCH / COMMIT (để QA checkout)
   - sns-line: ai_fixbug_41448 (nhánh gốc release_step_20260827, commit d199db2c03, 5 file)  [đã push]
```

**Journal #139305 — Đỗ Quyên — 2026-09-29:**

```
Tái hiện: 
staff A có lịch lv 12h - 20h30 
staff B có lịch lv 12h - 18h30 
course 2h 
time nghỉ sau 1h 
setting limit option 3 là 2
có 1 booking lúc 17h30 ở staff A 
=> friend chọn course 2h - NO STAFF => khung 16h và 16h30 đang bị OFF 
Expect: ON do khung 16h30 -18h30 vẫn đủ 2h làm việc của course (time nghỉ ko tính vào time lv)
```

**Journal #139421 — AI LME Fix bug — 2026-09-30:**

> Phần "các bản vá thêm" + "phạm vi retest" đã tách vào `03-dev-impact.md`. Phần kiểm lại ca tái hiện + đo lường:

```
■ DA KIEM CA TAI HIEN MOI CUA CHI QUYEN (comment 29/09 13:29) — DA HET LOI
  Du lieu: NV-A 12:00-20:30, NV-B 12:00-18:30, khoa 2 tieng, 片付け sau 60',
           option 3 gioi han 2, NV-A da co 1 booking luc 17:30, khach chon 指名なし.
  Mong doi: khung 16:00 va 16:30 phai BAT (16:30-18:30 van du 2 tieng trong ca NV-B;
            thoi gian nghi khong tinh vao gio lam viec).
  Do lai tren dung du lieu do:
    - Ban release: 16:00 = TAT, 16:30 = TAT   (dung trieu chung chi bao)
      khung BAT: 12:00 12:30 13:00 13:30 14:00 14:30 15:00
    - Ban e8931817a2: 16:00 = BAT, 16:30 = BAT   (dung mong doi)
      khung BAT: 12:00 12:30 13:00 13:30 14:00 14:30 15:00 15:30 16:00 16:30
  => Ca nay da duoc cac ban va hien co xu ly, khong can sua them.

■ DO LUONG TREN BAN e8931817a2
  - Quet 32.960 khung (5 bo ca x 4 bo luot da dat x 4 option x 4 do dai khoa x 5 cau hinh
    前後の空き時間) doi chieu oracle doc lap: lo hong dat trung 161 -> 0; chan oan 1491 -> 8.
  - Quet rieng nhanh chi dinh nhan vien 2.160 cau hinh: 0 khung bi an oan.
  - PHPUnit 69/69.
```

**Journal #139595 — AI LME Fix bug — 2026-10-01:**

> Nội dung đầy đủ đã tách vào `03-dev-impact.md` mục 4.4.

```
★ CAP NHAT TIEN DO
Branch: ai_fixbug_41448   commit 7087f665bd (da push)   Base: release_step_20260930

■ Phan viec cu DA VAO RELEASE
  Cac ban va cho #41740-#41746 va phan han muc dem theo so luot DONG THOI da duoc
  release_step_20260930 hap thu. Khong con cho merge.

■ Phan moi tren branch
  commit 7087f665bd — vá #41822 / #41823: lich kieu 個人 dem luot dat staff_id = 0 HAI LAN
  nen 上限を設定する = 2 chi nhan duoc 1 luot moi khung. Loi CO SAN tren release.
```

**Journal #139716 — AI LME Fix bug — 2026-10-01:**

> Nội dung đầy đủ (6 mục) đã tách vào `03-dev-impact.md` mục 4.4. Bug #41822/#41823 phát hiện qua TC-FUNC004-11 — TC do reviewer đề xuất ở report round 2 của task này.
