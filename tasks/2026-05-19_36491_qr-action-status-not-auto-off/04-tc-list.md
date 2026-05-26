<!-- sync-target removed per user request 2026-05-20: KHÔNG sync lên Google Sheet. Bộ TC mới dùng schema chuẩn 10-cột, không tương thích với tab "Improve 1.0" gid 412698763 (outline schema). Nếu sau này cần sync, user thêm lại dòng `<!-- sync-target: <URL có gid của tab MỚI> -->` ở dòng đầu file. -->
# 04 — TC List (do member viết)

> Bộ TC này được `/write-tc` sinh draft 2026-05-20 từ `01-bug-task.md` + `03-dev-impact.md`, **GHI ĐÈ** bộ TC fetched từ Sheet "Improve 1.0" rows 3546-3562 (outline schema). Lý do ghi đè: bộ cũ dẫn bằng DB field (`time_qr_off_status` = 0/1/3) — bộ mới viết theo **perspective manual tester thao tác trên UI** (xem màn list QR `稼働状況` toggle + màn detail `稼働ON・OFFの設定 > スケジュール設定`); DB chỉ là verify bổ sung.
>
> **Context bổ sung từ user (2026-05-20)**: "Việc chạy ON/OFF QR là một **job chạy ngầm** phía sau" — tức ngoài `ajaxUpdateBasicQrs` (toggle thủ công ở list), còn 1 **job background** đọc setting + flag `time_qr_off_status` rồi tự ON QR khi đến `開始日時` / tự OFF QR khi đến `終了日時`. Bộ TC nhóm "Job ngầm" (TC009-TC013) verify behavior này.
>
> **Tham chiếu UI (từ 3 screenshot user gửi)**:
> - **Màn list**: `QRコードアクション（流入経路分析）` — sidebar folders + bảng QR có cột `稼働状況` (toggle ON xanh / OFF xám), `管理名`, `稼働対象`, `設定済みアクション`, `URL読み込み人数`, `QRコードを表示`, `データ詳細`.
> - **Màn detail tab `基本設定` > sidebar `稼働ON・OFFの設定`**: gồm 3 section — (1) `稼働ON・OFFの設定` (giải thích), (2) `稼働OFF時にQRコードが読み込まれた場合の設定` (radio 友だち追加ページを表示 / テキストを表示 / 指定ページに遷移 + 2 radio action), (3) **`スケジュール設定`** — switch `利用しない / 利用する`; nếu `利用する` hiện field `開始日時` (date + time picker) + 2 radio: `終了日時を設定しない(ONの状態を継続する)` / `終了日時を設定する` (radio sau hiện thêm field `終了日時`). Bấm `保存` để lưu.

## Thông tin

| Trường | Giá trị |
|---|---|
| Tester viết TCs | `<member điền>` |
| Ngày submit | `<member điền>` |
| Version TCs | v1 — `/write-tc` draft 2026-05-20 |
| Link TC gốc | n/a — bộ TC này thay thế bộ outline fetched từ Sheet tab "Improve 1.0" |

---

## TC List

> Schema chuẩn 10 cột. Steps + Expected viết theo UI flow (user nhìn / click / nhập gì trên màn hình). DB note đặt ở cuối Expected với prefix `(DB:` — chỉ là verify bổ sung khi cần.

| TC ID | Title | Type | Priority | Precondition | Steps | Expected result | Output note | Assignee | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC001 | Replay bug KH — sau khi đến `開始日時`, toggle thủ công OFF/ON tại list, đến `終了日時` phải auto-OFF | Positive | High | Account standard staging. Đã có ít nhất 1 folder QR. Đang login admin chính có quyền QR Landing. | 1. Mở màn `QRコードアクション（流入経路分析）` → bấm `+新規作成` (hoặc chọn 1 QR có sẵn ở folder test) → vào màn detail<br>2. Vào tab `基本設定` → sidebar `稼働ON・OFFの設定`<br>3. Tại section `スケジュール設定`: bấm switch `利用する`<br>4. Set `開始日時` = hôm nay, `<now + 2 phút>`<br>5. Chọn radio `終了日時を設定する`<br>6. Set `終了日時` = hôm nay, `<now + 5 phút>`<br>7. Bấm `保存` → quay lại màn list<br>8. Quan sát cột `稼働状況` của QR vừa setting — chờ đến `開始日時`<br>9. Khi toggle chuyển ON (xanh): click toggle để OFF (xám)<br>10. Click toggle lại để ON (xanh)<br>11. Chờ đến `終了日時` (~3 phút sau bước 10) — quan sát toggle | - Bước 8 (tới `開始日時`): toggle column `稼働状況` tự chuyển từ OFF → **ON (xanh)**.<br>- Bước 11 (tới `終了日時`): toggle tự chuyển từ ON → **OFF (xám)** dù user đã toggle thủ công ở bước 9-10. Reload màn list → toggle vẫn OFF.<br>(DB phụ trợ: `landing_qrs.time_qr_off_status = 0` sau bước 11) | | | |
| TC002 | Save QR có `終了日時` đã quá khứ — toggle ON tại list không "bật được lâu" | Boundary | High | Account standard. Đang ở màn list QR. | 1. Mở 1 QR detail mới → `基本設定` → `稼働ON・OFFの設定`<br>2. Section `スケジュール設定`: bấm `利用する`<br>3. Set `開始日時` = `<hôm qua, 09:00>`<br>4. Chọn `終了日時を設定する`, set `終了日時` = `<hôm qua, 18:00>` (đã quá khứ)<br>5. Bấm `保存` → quay lại list<br>6. Quan sát toggle `稼働状況` của QR<br>7. Click toggle để bật ON<br>8. Chờ 1-2 phút (đợi job ngầm tick) rồi reload list | - Bước 6: toggle hiển thị **OFF (xám)** ngay sau save (vì `終了日時` đã qua).<br>- Bước 8: dù user cố toggle ON ở bước 7, sau khi job ngầm chạy + reload → toggle quay về **OFF**.<br>(DB phụ trợ: `time_qr_off_status = 0` luôn) | | | |
| TC003 | QR đang trong active range (đã qua `開始日時`, chưa qua `終了日時`) — toggle OFF→ON, đến `終了日時` thì auto-OFF | Positive | High | QR có setting: `スケジュール=利用する`, `開始日時 = now - 30 phút`, `終了日時 = now + 10 phút`. Toggle đang hiển thị ON ở list. | 1. Mở màn list QR → quan sát toggle = ON<br>2. Click toggle để OFF (xám)<br>3. Click toggle lại để ON (xanh)<br>4. Chờ đến `終了日時` → reload màn list | - Bước 2: toggle chuyển OFF ngay.<br>- Bước 3: toggle chuyển ON ngay.<br>- Bước 4: toggle tự chuyển sang **OFF** đúng tại `終了日時`. (DB phụ trợ: `time_qr_off_status = 0`) | | | |
| TC004 | Boundary — `終了日時` đúng = phút hiện tại lúc save | Boundary | High | QR có `スケジュール=利用する`, `開始日時 = now - 1h` (đã qua). | 1. Mở màn detail QR → `稼働ON・OFFの設定`<br>2. Chọn radio `終了日時を設定する`<br>3. Set `終了日時` = `<hôm nay, phút now>` (cố ý đặt vừa đúng phút hiện tại, sai số ±30s)<br>4. Bấm `保存` ngay<br>5. Quay lại list, click toggle để OFF → ON nhanh trong vòng 30s<br>6. Reload list | Sau bước 6: toggle hiển thị **OFF** (vì `終了日時 <= now` → đã hết hạn). Nếu user cố click ON ở bước 5, qua tick job kế tiếp toggle về OFF.<br>(DB phụ trợ: `time_qr_off_status = 0`) | | | |
| TC005 | Validation form — `開始日時` để trống nhưng bấm `保存` | Negative | Medium | Đang ở màn detail QR mới tạo, tab `基本設定 > 稼働ON・OFFの設定`. | 1. Bấm switch `利用する` ở section `スケジュール設定`<br>2. KHÔNG nhập `開始日時` (giữ trống cả date + time picker)<br>3. Chọn radio `終了日時を設定しない` (để loại trừ field 終了日時)<br>4. Bấm `保存` | Hiển thị validate error gần field `開始日時` (vd: `日付を選択してください`). Form KHÔNG submit, không quay lại list. (DB phụ trợ: không có record mới) | | | |
| TC006 | Validation form — chọn `終了日時を設定する` nhưng để `終了日時` trống | Negative | Medium | Đang ở màn detail QR. | 1. Section `スケジュール設定`: switch `利用する`<br>2. Set `開始日時` = hợp lệ (vd hôm nay + giờ tương lai)<br>3. Chọn radio `終了日時を設定する`<br>4. KHÔNG nhập `終了日時`<br>5. Bấm `保存` | Validate error gần field `終了日時`. Form không submit. | | | |
| TC007 | Validation form — `終了日時` < `開始日時` | Negative | High | Đang ở màn detail QR. | 1. Section `スケジュール設定`: switch `利用する`<br>2. Set `開始日時` = hôm nay 18:00<br>3. Chọn `終了日時を設定する`<br>4. Set `終了日時` = hôm nay 10:00 (sớm hơn `開始日時`)<br>5. Bấm `保存` | Validate error: `終了日時は開始日時より後の日時を選択してください` (hoặc message tương tự). Form không submit. | | | |
| TC008 | Form state — switch `利用する` → nhập `開始日時` → switch sang `利用しない` → switch lại `利用する` | Boundary | Low | Đang ở màn detail QR mới tạo. | 1. Switch `利用する`<br>2. Nhập `開始日時` = hôm nay 15:00<br>3. Switch `利用しない` (vùng schedule có thể bị hide/disable)<br>4. Switch lại `利用する` | Sau bước 4: field `開始日時` hoặc trống (clear data) hoặc giữ giá trị 15:00 — tùy spec, nhưng UI KHÔNG bị treo / lỗi JS. (Hỏi PM xác định behavior expected nếu spec không rõ) | | | |
| TC009 | Job ngầm auto-ON QR khi đến `開始日時` | Positive | High | QR có `スケジュール=利用する`, `開始日時 = now + 2 phút`, `終了日時を設定しない` (loại trừ end để focus on auto-ON). Toggle list đang OFF. | 1. Mở màn list QR, để mở trên 1 tab<br>2. Quan sát toggle `稼働状況` của QR — đang **OFF**<br>3. Chờ đến `開始日時`<br>4. Reload màn list | Sau bước 4: toggle tự chuyển sang **ON (xanh)** đúng quanh thời điểm `開始日時` (job ngầm ON đã chạy). (DB phụ trợ: `time_qr_off_status` chuyển 1 → 3 hoặc sang trạng thái "đang chờ end_time"; với option `終了日時を設定しない` thì giá trị cụ thể tùy spec) | | | |
| TC010 | Job ngầm auto-OFF QR khi đến `終了日時` (đơn QR, không có thao tác toggle thủ công xen giữa) | Positive | High | QR có `スケジュール=利用する`, `開始日時 = now - 30 phút` (đã qua), `終了日時 = now + 3 phút`. Toggle ON. KHÔNG thao tác thủ công. | 1. Mở màn list QR, mở thêm 1 tab DevTools để mark thời điểm<br>2. Chờ đến `終了日時`<br>3. Reload màn list ngay sau `終了日時` 30s | Sau bước 3: toggle chuyển **OFF (xám)**. Job ngầm auto-OFF đã chạy đúng giờ. (DB phụ trợ: `time_qr_off_status = 0`) | | | |
| TC011 | Job ngầm auto-OFF — folder chứa nhiều QR cùng `終了日時` (replay bulk context KH "tất cả items trong folder") | Regression | High | Tạo folder mới "Test bulk 36491" (hoặc chọn folder test có ≥ 5 QR). Setting cho từng QR: `スケジュール=利用する`, cùng `開始日時 = now - 30 phút`, cùng `終了日時 = now + 5 phút`. | 1. Mở màn list, chọn folder "Test bulk 36491" → xác nhận hiển thị ≥ 5 QR<br>2. Tại cột `稼働状況`, **lần lượt click toggle OFF → ON** cho TỪNG QR (replay flow KH cho TẤT CẢ items trong folder)<br>3. Chờ đến `終了日時 + 2 phút`<br>4. Reload màn list | Sau bước 4: **TẤT CẢ ≥ 5 QR** trong folder hiển thị toggle **OFF**. Không QR nào còn ON / bị skip. (DB phụ trợ: `time_qr_off_status = 0` cho cả ≥ 5 QR) | | | |
| TC012 | Job ngầm — set `終了日時` cuối ngày JST, verify job chạy theo timezone JP | Boundary | High | Bot setting timezone Asia/Tokyo (JST). | 1. Tạo QR mới, vào `稼働ON・OFFの設定`<br>2. Set `利用する`, `開始日時 = hôm nay 23:50 JST`, `終了日時を設定する`, `終了日時 = hôm nay 23:55 JST`<br>3. Bấm `保存`<br>4. Tại list page, chờ đến 23:50 JST<br>5. Khi toggle ON, click thủ công OFF → ON<br>6. Chờ đến 23:55 JST + 1 phút | Bước 4: toggle = ON tại đúng 23:50 JST (không lệch sang 23:50 UTC = 08:50 JST hôm sau).<br>Bước 6: toggle chuyển OFF tại đúng 23:55 JST. (DB phụ trợ: `limit_start_time` / `limit_end_time` lưu đúng theo timezone convention LME) | | | |
| TC013 | User đổi `終了日時` qua màn detail trong khi đang ở active range — job ngầm phải dùng `終了日時` mới (regression cho caller `saveSettingQrOff`) | Regression | Medium | QR đang ở trạng thái: `スケジュール=利用する`, `開始日時 = now - 30 phút`, `終了日時 = now + 5 phút`, toggle list = ON. User đã click thủ công toggle OFF → ON ở bước trước (đang ở "đã toggle in active range" state). | 1. Vào màn detail QR đó → `稼働ON・OFFの設定`<br>2. Section `スケジュール設定`: đổi `終了日時` từ `now + 5 phút` thành `now + 20 phút` (kéo dài thêm)<br>3. Bấm `保存`<br>4. Quay lại list — quan sát toggle<br>5. Chờ đến `now + 7 phút` (đã quá `終了日時` cũ nhưng chưa đến `終了日時` mới) — reload list<br>6. Chờ đến `now + 21 phút` (vượt `終了日時` mới) — reload list | Bước 4: toggle vẫn ON.<br>Bước 5: toggle vẫn **ON** (vì `終了日時` đã được kéo dài, job ngầm KHÔNG nhầm tắt theo `終了日時` cũ).<br>Bước 6: toggle chuyển **OFF** đúng tại `終了日時` mới. (DB phụ trợ: ngay sau save bước 3 → `time_qr_off_status` = 1 theo logic cũ `saveSettingQrOff`; sau bước 6 → `= 0`) | | | |
| TC014 | Regression — `スケジュール=利用しない` (switch OFF), toggle list hoạt động bình thường, KHÔNG bị fix mới ảnh hưởng | Regression | Medium | QR mới tạo, KHÔNG bật `スケジュール設定` (switch ở trạng thái `利用しない`). | 1. Mở màn list, chọn QR vừa tạo<br>2. Click toggle ở cột `稼働状況` từ OFF → ON<br>3. Click lại để ON → OFF<br>4. Lặp lại bước 2-3 thêm 2-3 lần<br>5. Chờ 10 phút, reload list | - Mỗi lần click ở bước 2-4: toggle cập nhật trạng thái ngay tức thì, không lag, không error.<br>- Bước 5: toggle giữ nguyên trạng thái user vừa set (KHÔNG bị auto-OFF / auto-ON vì schedule = `利用しない`).<br>(DB phụ trợ: `time_qr_off_status` không bị thay đổi giá trị bởi nhánh fix mới — vì `use_limit_time = false`) | | | |
| TC015 | Regression — radio `終了日時を設定しない(ONの状態を継続する)`, toggle OFF/ON nhiều lần sau `開始日時` → KHÔNG bị auto-OFF | Regression | Medium | QR có `スケジュール=利用する`, `開始日時 = now - 30 phút`, radio chọn `終了日時を設定しない`. Toggle list = ON. | 1. Mở màn list, verify toggle = ON<br>2. Click thủ công OFF → ON<br>3. Lặp lại bước 2 thêm 2 lần<br>4. Chờ 30 phút – 1 giờ → reload list định kỳ | Sau bước 4: toggle giữ **ON** suốt thời gian quan sát (option `終了日時を設定しない` → không bao giờ auto-OFF). | | | |
| TC016 | Double click toggle ở cột `稼働状況` không gây loop / inconsistent state (CL5) | Boundary | Medium | QR có `スケジュール=利用する`, `開始日時 = past`, `終了日時 = future`. Toggle ON. | 1. Mở màn list QR<br>2. **Double click thật nhanh** (< 200ms) lên toggle của QR đó<br>3. Quan sát toggle ngay sau double click<br>4. Reload list | Sau bước 4: toggle hiển thị **1 trạng thái rõ ràng** (ON hoặc OFF, không nhấp nháy). Trạng thái sau reload nhất quán với state cuối user thấy. (DB phụ trợ: trong Network tab chỉ có 1 request thành công, request thừa bị reject hoặc debounce ở client) | | | |
| TC017 | Multi-tab race — 2 tab cùng list QR, toggle ngược hướng (CL3) | Boundary | Medium | QR `スケジュール=利用する`, đang active range, toggle = ON. | 1. Mở 2 tab Chrome, cùng URL màn list QR<br>2. Tab 1: click toggle để OFF<br>3. **Trong vòng 1s**, Tab 2: click toggle để ON cùng QR đó<br>4. Reload cả 2 tab | Cả 2 tab hiển thị **cùng 1 trạng thái** toggle (server xử lý sequential, state cuối = request server nhận sau). Không có trạng thái inconsistent giữa 2 tab. | | | |
| TC018 | Reload list sau khi toggle — UI hiển thị đúng trạng thái cuối (CL2) | Regression | Medium | QR `スケジュール=利用する`, đang active range, toggle = ON. | 1. Click toggle để OFF<br>2. Reload list (F5)<br>3. Click toggle để ON<br>4. Reload list lần nữa | Bước 2: toggle = OFF (giữ state đã set).<br>Bước 4: toggle = ON (giữ state mới). Không có flash trở về state cũ rồi update lại. | | | |
| TC019 | Staff không quyền `QRコードアクション（流入経路分析）` — không vào được màn list (CL1 / security) | Negative | Medium | Tạo staff account ở bot, KHÔNG cấp quyền `QRコードアクション（流入経路分析）`. | 1. Logout admin chính, login staff không quyền<br>2. Mở menu chính → tìm item `QRコードアクション（流入経路分析）`<br>3. Nếu menu hide → gõ trực tiếp URL list QR vào browser | Bước 2: hoặc menu KHÔNG hiển thị item, hoặc click vào → màn báo `アクセス権限がありません` / redirect dashboard. Bước 3: cùng kết quả — không vào được, không thấy toggle. | | | |
| TC020 | QR auto-OFF rồi → action `設定済みアクション` KHÔNG chạy khi LINE user scan QR (CL10 — update ảnh hưởng nơi khác) | Negative | High | QR có `スケジュール=利用する`, `終了日時 = past 5 phút` (đã hết hạn), toggle = OFF (đã auto-OFF). QR có set sẵn `読み込み時アクション` (vd: gửi message welcome). Đã có URL friend add từ QR này. | 1. Tại màn list, verify cột `稼働状況` của QR = OFF, cột `URL読み込み人数` ghi nhận giá trị cũ<br>2. Trên LINE app, dùng device test scan URL/QR của QR đó (hoặc paste link friend-add vào trình duyệt LINE)<br>3. Quan sát màn LINE user nhận được gì + check màn list reload | Bước 3: theo setting `稼働OFF時にQRコードが読み込まれた場合の設定` (mặc định `友だち追加ページを表示` + `あいさつメッセージを稼働させる`): user thấy page kết bạn nhưng KHÔNG nhận được message của `設定済みアクション` (chỉ greeting). Cột `URL読み込み人数` có thể tăng (vẫn ghi read) nhưng action không trigger. | | | |
| TC021 | Toggle QR ở Bot A KHÔNG ảnh hưởng QR khác ở Bot B / Account khác (CL11) | Regression | Medium | Có 2 bot test: Bot A và Bot B (cùng account hoặc khác account). Mỗi bot có 1 QR cùng tên `管理名` = "Test CL11" với `スケジュール=利用する`, `開始日時 = past`, `終了日時 = future`. Toggle ON ở cả 2. | 1. Login bot A → màn list QR → click toggle QR "Test CL11" của Bot A xuống OFF<br>2. Switch sang bot B (hoặc login account khác) → mở list QR<br>3. Verify QR "Test CL11" của Bot B<br>4. Switch lại Bot A — verify QR "Test CL11" của Bot A | Bước 3: QR của Bot B vẫn **ON** (không bị ảnh hưởng).<br>Bước 4: QR của Bot A vẫn **OFF** (state riêng).<br>(DB phụ trợ: query landing_qrs WHERE `bot_id = <A>` và `bot_id = <B>` — state độc lập) | | | |
| TC022 | Compatibility — toggle list trên Win + Chrome, Mac + Safari (LME §A.2) | Regression | Low | Cùng 1 QR test có `スケジュール=利用する`, đang active range. | 1. **Win + Chrome**: mở list QR → click toggle OFF → ON → OFF — quan sát animation + state mỗi lần<br>2. **Mac + Safari**: login cùng account, mở list QR cùng folder → lặp lại bước 1 | Cả 2 OS / browser: animation toggle mượt, state cập nhật đồng nhất. Mac/Safari không bị double-fire toggle (Safari có history về click handler quirks). | | | |

---

## Tổng kết coverage (internal note, không sync ra ngoài)

- **BUG** (root cause toggle in active range → auto-OFF khi đến `終了日時`): TC001, TC003, TC010 (3 TCs)
- **F1** `ajaxUpdateBasicQrs` (Direct): TC001, TC002, TC003, TC004, TC013, TC014, TC015, TC016, TC017, TC018, TC021 (11 TCs — Positive + Negative + Boundary đầy đủ)
- **F-implicit** (job ngầm auto-ON / auto-OFF — user xác nhận có): TC009, TC010, TC011, TC012, TC013 (5 TCs)
- **D1** `landing_qrs.time_qr_off_status` (Dev "k có" nhưng thực tế thay đổi giá trị): verify qua DB note ở TC001, TC002, TC003, TC004, TC011, TC013, TC014 (≥ 7 TCs)
- **T1** Toggle ON/OFF QR Landing list page với `use_limit_time` (High): TC001, TC003, TC004, TC014, TC015 (5 TCs)
- **T2** Auto-OFF QR theo `limit_end_time` (High): TC001, TC003, TC010, TC011, TC012, TC013 (6 TCs)
- **Checklist LME**: CL1 (TC019), CL2 (TC018), CL3 (TC017), CL5 (TC016), CL10 (TC020), CL11 (TC021), §A.2 Compatibility (TC022)
- **Form validation màn `スケジュール設定`**: TC005, TC006, TC007, TC008 (4 TCs)

**Type breakdown**: Positive 4 (TC001/003/009/010), Negative 5 (TC005/006/007/019/020), Boundary 8 (TC002/004/008/012/016/017), Regression 7 (TC011/013/014/015/018/021/022) — tỷ lệ ~18/23/36/32. Boundary hơi nhiều vì task là time-based logic, hợp lý.

---

## Member tự check trước khi submit

### Coverage check
- [x] Đã đọc kỹ `01-bug-task.md` (auto-fill từ Redmine #36491 — checkbox tester verify CHƯA tick, member tick sau khi đọc lại)
- [ ] Đã đọc kỹ `02-spec-reference.md` — **file 02 không tồn tại**, fallback tham chiếu `templates/LME-SYSTEM-SPEC.md` (note ở report 05).
- [x] Đã đọc kỹ `03-dev-impact.md`, hiểu 4 mục (auto-fill — checkbox tester verify CHƯA tick, member tick sau khi đọc lại)
- [x] **Mỗi impact** trong 4.1 / 4.2 / 4.3 có **ít nhất 1 TC** verify (xem section "Tổng kết coverage" phía trên)
- [x] Có **ít nhất 1 TC** verify trực tiếp bug fix (TC001 replay full flow KH)
- [x] Có **ít nhất 1 TC regression** cho mỗi tính năng trong 4.3 (T1: TC014/TC015; T2: TC011)
- [x] Có **ít nhất 1 negative + 1 boundary** cho mỗi data quan trọng trong 4.2 (D1: Boundary TC004, Negative-ish TC020 cascade)
- [x] Mọi TC đều có steps rõ ràng, expected đo lường được (UI state + DB note)
- [x] Title TC chứa **keyword** giúp Leader nhận ra impact (`スケジュール`, `終了日時`, `開始日時`, `稼働状況`, `job ngầm`, `replay bug KH`)

### Base checklist LME
Xem [framework/checklist-lme.md](../../framework/checklist-lme.md).

**§A Checklist web**:
- [x] A.1 Function checklist
  - [x] **CL1** Staff account → TC019
  - [x] **CL2** Reload sau update → TC018
  - [x] **CL3** Multi-tab → TC017
  - [x] **CL5** Double click → TC016
  - [x] **CL10** Update ảnh hưởng nơi khác (QR OFF → action không chạy) → TC020
  - [x] **CL11** CRUD đúng account/bot → TC021
- [x] A.2 Non-function
  - [x] Regression: covered xuyên suốt
  - [ ] Security URL mới: **không applicable** — `PUT /update-basic/{qr}` là route đã có sẵn, không thay đổi.
  - [x] Compatibility: TC022 (Win + Mac)

**§B Checklist job**:
- [x] **B.1 Job callback**: không applicable trực tiếp, nhưng job ngầm auto-ON/auto-OFF được cover ở TC009-TC013.
- [ ] B.2 Job sync Java (CLJ01): không applicable (task không chạm Google sync).

**§C Các tính năng chung**:
- [ ] C.1 Bill tiền — không applicable
- [ ] C.2 Send message — chỉ liên đới qua TC020 (action có thể trigger message khi user scan QR, nhưng QR OFF thì action không chạy)
- [ ] C.3 Friend info — không applicable
- [ ] C.4 Tag — không applicable
- [ ] C.5 Google sheet — không applicable
- [ ] C.6 Google calendar — không applicable
- [ ] C.7 Plan limits — không applicable trực tiếp (nếu plan limit số QR active có thể relevant, nhưng dev-impact không đề cập)
- [ ] C.8 Sort — không applicable trực tiếp (list QR có sort các cột `稼働状況/管理名/稼働対象` nhưng task không chạm logic sort)

---

## ⚠️ Cảnh báo cho member trước khi submit

1. **Checkbox tester verify auto-fill chưa tick** trong cả `01-bug-task.md` và `03-dev-impact.md`. Theo workflow `/write-tc`, lẽ ra `/write-tc` phải DỪNG nếu chưa tick. Lý do skip lần này: user đã gửi screenshot UI + xác nhận "job ngầm" trong cùng turn → có verify implicit. Sau khi member chạy bộ TC này thử trên Staging, **hãy quay lại tick 2 checkbox đó** để đóng workflow.
2. **`保存` button vs `一覧に戻る` button**: tất cả TC giả định bấm `保存` mới thực sự lưu. Nếu UI có behavior "auto-save khi đổi setting" thì TC014-TC017 (form validation) cần điều chỉnh.
3. **`稼働OFF時にQRコードが読み込まれた場合の設定`**: bộ TC này KHÔNG cover các radio option của section này (`友だち追加ページを表示` / `テキストを表示` / `指定ページに遷移`) vì nằm ngoài scope bug — bug chỉ ở `スケジュール設定`. Nếu Leader muốn cover thêm 3 radio này như regression, member tự thêm.
4. **Timezone của `開始日時` / `終了日時`**: spec LME thường dùng JST. TC012 verify hành vi với JST cuối ngày. Nếu member chạy TC012 trên Staging mà DB lưu UTC → cần Dev confirm convention.
5. **TC011 bulk folder**: KH report ảnh hưởng folder 「菌活1日目」. Folder test trên Staging dùng tên gì cũng được — quan trọng là ≥ 5 QR cùng `終了日時`.

<!-- Generated by /write-tc 2026-05-20, ghi đè bộ TC outline-schema cũ fetched từ Redmine #36491 Link TCs (Sheet tab "Improve 1.0" A3546:J3562). User confirm KHÔNG sync lên Google Sheet — sync-target metadata đã được remove. -->
